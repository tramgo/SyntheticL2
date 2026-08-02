from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, metric_value, read_csv
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE263_DIR = Path("outputs/phase263")
DEFAULT_INPUT_PARQUET = Path("outputs/phase254/phase254_richer_raw_top5_depth_event_bars.parquet")
DEFAULT_OUTPUT_DIR = Path("outputs/phase264")
SELECTED_ROUTE = "P264_FULL_DEPTH_LIQUIDITY_SHOCK_ABSORPTION_EVENT_MODEL"


def inspect_input(input_parquet: Path) -> dict[str, Any]:
    if not input_parquet.exists():
        return {"input_exists": 0}
    con = duckdb.connect()
    try:
        stats = con.execute(
            f"""
            select
                count(*)::bigint as event_bar_rows,
                count(distinct symbol)::bigint as symbols,
                count(distinct trade_date)::bigint as trade_dates,
                avg(avg_spread_bps)::double as mean_spread_bps,
                median(avg_spread_bps)::double as median_spread_bps,
                avg(abs(avg_depth_beyond_l1_qty_imbalance))::double as mean_abs_l2_l5_imbalance,
                avg(abs(avg_level_weighted_depth_imbalance))::double as mean_abs_level_weighted_imbalance,
                avg(avg_cum_buy_qty_l2_l5 / nullif(avg_cum_buy_qty_l1_l5, 0))::double as mean_l2_l5_bid_share,
                avg(avg_cum_sell_qty_l2_l5 / nullif(avg_cum_sell_qty_l1_l5, 0))::double as mean_l2_l5_ask_share,
                avg(depth_replenishment_pressure)::double as mean_replenishment_pressure,
                avg(depth_withdrawal_pressure)::double as mean_withdrawal_pressure,
                avg(top5_qty_churn_sum)::double as mean_top5_qty_churn,
                avg(top5_order_churn_sum)::double as mean_top5_order_churn,
                avg(l1_price_shift_abs_sum)::double as mean_l1_price_shift_abs_sum,
                avg(taker_round_trip_cost_floor_bps)::double as mean_cost_floor_bps
            from read_parquet('{input_parquet.as_posix()}')
            """
        ).fetchdf().iloc[0].to_dict()
    finally:
        con.close()
    return {"input_exists": 1, **stats}


def build_feature_catalog() -> pd.DataFrame:
    rows = [
        ("depth_stock", "avg_cum_buy_qty_l1_l5", "Full visible bid-side quantity across Zerodha top-five rows 1-5"),
        ("depth_stock", "avg_cum_sell_qty_l1_l5", "Full visible ask-side quantity across Zerodha top-five rows 1-5"),
        ("depth_stock", "avg_cum_buy_qty_l2_l5", "Bid depth beyond L1; required levels 2-5 materiality"),
        ("depth_stock", "avg_cum_sell_qty_l2_l5", "Ask depth beyond L1; required levels 2-5 materiality"),
        ("imbalance", "avg_cum_top5_qty_imbalance", "Top-five quantity imbalance"),
        ("imbalance", "avg_depth_beyond_l1_qty_imbalance", "Levels 2-5 quantity imbalance"),
        ("imbalance", "avg_level_weighted_depth_imbalance", "Near-level weighted depth imbalance"),
        ("imbalance", "avg_order_count_imbalance_l1_l5", "Top-five order-count imbalance"),
        ("shock", "depth_replenishment_pressure", "Visible-depth replenishment event pressure"),
        ("shock", "depth_withdrawal_pressure", "Visible-depth withdrawal event pressure"),
        ("shock", "top5_qty_churn_sum", "Top-five quantity churn / instability"),
        ("shock", "top5_order_churn_sum", "Top-five order-count churn / cancel pressure"),
        ("shock", "l1_price_shift_abs_sum", "L1 price movement / spread-book instability proxy"),
        ("liquidity", "avg_spread_bps", "Spread compression/expansion context and cost hurdle context"),
        ("cost", "taker_round_trip_cost_floor_bps", "Zerodha cost floor for directional event hurdle"),
        ("forbidden", "l1_only_depth_imbalance", "No L1-only feature set or candidate family is allowed"),
    ]
    return pd.DataFrame(rows, columns=["feature_group", "feature", "description"])


def build_event_family_catalog() -> pd.DataFrame:
    rows = [
        (
            "P265_L2L5_BID_ABSORPTION_CONTINUATION",
            "long",
            "bid-side levels 2-5 replenish while top-five imbalance and level-weighted imbalance support bids after a liquidity shock",
            "avg_cum_buy_qty_l2_l5;avg_depth_beyond_l1_qty_imbalance;avg_level_weighted_depth_imbalance;depth_replenishment_pressure;top5_qty_churn_sum",
        ),
        (
            "P265_L2L5_ASK_ABSORPTION_CONTINUATION",
            "short",
            "ask-side levels 2-5 replenish while top-five imbalance and level-weighted imbalance support asks after a liquidity shock",
            "avg_cum_sell_qty_l2_l5;avg_depth_beyond_l1_qty_imbalance;avg_level_weighted_depth_imbalance;depth_replenishment_pressure;top5_qty_churn_sum",
        ),
        (
            "P265_WITHDRAWAL_REVERSAL_AFTER_SHOCK",
            "long_or_short",
            "detect aggressive withdrawal/churn events and trade reversal only when opposite-side levels 2-5 absorption appears",
            "depth_withdrawal_pressure;top5_qty_churn_sum;top5_order_churn_sum;avg_cum_buy_qty_l2_l5;avg_cum_sell_qty_l2_l5",
        ),
        (
            "P265_SPREAD_COMPRESSION_ABSORPTION",
            "long_or_short",
            "require spread compression after high churn plus agreement between top-five and levels 2-5 imbalance",
            "avg_spread_bps;l1_price_shift_abs_sum;avg_cum_top5_qty_imbalance;avg_depth_beyond_l1_qty_imbalance",
        ),
        (
            "P265_DEPTH_CHURN_EXHAUSTION_FILTER",
            "filter",
            "filter or downweight events with excessive churn/order-cancel pressure without replenishment confirmation",
            "top5_qty_churn_sum;top5_order_churn_sum;depth_replenishment_pressure;depth_withdrawal_pressure",
        ),
    ]
    return pd.DataFrame(
        rows,
        columns=["event_family_id", "direction_space", "description", "required_full_depth_features"],
    )


def build_label_contract() -> pd.DataFrame:
    rows = [
        ("future_mid_return_h3", "required", "3-event-bar future mid return label"),
        ("future_mid_return_h6", "required", "6-event-bar future mid return label"),
        ("future_mid_return_h10", "required", "10-event-bar future mid return label"),
        ("cost_hurdled_return", "required", "Directional label must exceed Zerodha cost floor at 1x, 1.5x and 2x stress before candidate survival"),
        ("no_future_feature_leakage", "required", "Future labels may not be used as features or filters"),
    ]
    return pd.DataFrame(rows, columns=["label_id", "label_status", "description"])


def build_search_grid_contract() -> pd.DataFrame:
    rows = [
        ("horizons", "3;6;10", "Evaluate the same event horizons available in Phase254"),
        ("imbalance_quantiles", "0.60;0.75;0.90", "Threshold top-five and levels 2-5 imbalance strength"),
        ("shock_quantiles", "0.60;0.75;0.90", "Threshold replenishment, withdrawal and churn event intensity"),
        ("spread_regimes", "low;mid;high;compression", "Separate spread/compression context from directional depth shock"),
        ("cost_multipliers", "1.0;1.5;2.0", "Stress Zerodha statutory/brokerage charges"),
        ("breadth_floors", "opportunities>=30;symbols>=8;dates>=1", "Minimum breadth before any survivor discussion on current available data"),
    ]
    return pd.DataFrame(rows, columns=["grid_component", "contract_value", "description"])


def build_control_contract() -> pd.DataFrame:
    rows = [
        ("random_side_control", "required", "Candidate must beat deterministic random side under the same event mask"),
        ("side_flip_control", "required", "Flipping the liquidity-shock direction should degrade or invert edge"),
        ("cost_stress", "required", "Evaluate base, 1.5x and 2x Zerodha cost floors"),
        ("shuffle_label_control", "required", "Candidate must beat shuffled future-return labels"),
        ("event_breadth_control", "required", "Candidate must clear minimum event, symbol and date breadth floors"),
        ("no_l1_only_control", "required", "Every event family must use top-five and levels 2-5 features"),
        ("threshold_relaxation_only", "forbidden", "Do not continue the failed passive route by merely relaxing thresholds"),
        ("paper_live_or_deployable_profitability_claim", "forbidden", "Phase264/265 cannot claim paper/live/deployable profitability"),
    ]
    return pd.DataFrame(rows, columns=["control_id", "control_status", "description"])


def build_gate_evaluation(
    phase263_dir: Path,
    input_stats: dict[str, Any],
    features: pd.DataFrame,
    families: pd.DataFrame,
    labels: pd.DataFrame,
    grid: pd.DataFrame,
    controls: pd.DataFrame,
) -> pd.DataFrame:
    phase263_next = str(metric_value(phase263_dir / "phase263_acceptance_summary.csv", "phase263_next_best_action", ""))
    route = read_csv(phase263_dir / "phase263_next_route_contract.csv")
    depth_contract_present = int(route["contract_value"].astype(str).str.contains("levels_1_to_5_required_l2_l5_required", case=False, na=False).sum()) if not route.empty else 0
    route_contract_present = int(route["contract_value"].astype(str).str.contains("liquidity_shock_absorption", case=False, na=False).sum()) if not route.empty else 0
    required_feature_text = ";".join(families["required_full_depth_features"].astype(str).tolist()) if not families.empty else ""
    required_controls = controls[controls["control_status"].astype(str).eq("required")]
    rows = [
        ("P264_PHASE263_WORK_ORDER_PRESENT", "run_phase264_full_depth_liquidity_shock_absorption_event_precommit" in phase263_next, phase263_next, "Phase263 next action targets Phase264", "hard"),
        ("P264_PHASE263_DEPTH_CONTRACT_PRESENT", depth_contract_present >= 1, depth_contract_present, "Phase263 route requires levels 1-5 and L2-L5", "hard"),
        ("P264_PHASE263_ROUTE_CONTRACT_PRESENT", route_contract_present >= 1, route_contract_present, "Phase263 route is liquidity-shock/absorption", "hard"),
        ("P264_INPUT_PRESENT", as_int(input_stats.get("input_exists", 0)) == 1, input_stats.get("input_exists", 0), "Phase254 richer raw top-five event bars exist", "hard"),
        ("P264_INPUT_BREADTH", as_int(input_stats.get("event_bar_rows", 0)) >= 1000 and as_int(input_stats.get("symbols", 0)) >= 20, f"rows={input_stats.get('event_bar_rows', 0)};symbols={input_stats.get('symbols', 0)}", ">=1000 rows and >=20 symbols", "hard"),
        ("P264_FEATURE_CATALOG_WRITTEN", len(features) >= 15 and int(features["feature_group"].astype(str).eq("forbidden").sum()) == 1, len(features), ">=15 feature rows plus L1-only forbidden row", "hard"),
        ("P264_FULL_DEPTH_EVENT_FAMILIES_WRITTEN", len(families) >= 5 and all(token in required_feature_text for token in ["l2_l5", "top5"]), len(families), ">=5 event families with L2-L5/top-five features", "hard"),
        ("P264_LABEL_CONTRACT_WRITTEN", len(labels[labels["label_status"].astype(str).eq("required")]) >= 5, len(labels), "required labels and no-leakage contract", "hard"),
        ("P264_SEARCH_GRID_WRITTEN", len(grid) >= 6, len(grid), ">=6 search-grid rows", "hard"),
        ("P264_CONTROLS_WRITTEN", len(required_controls) >= 6 and int(controls["control_status"].astype(str).eq("forbidden").sum()) >= 2, len(controls), "required controls and forbidden continuations", "hard"),
        ("P264_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase264 Full-depth Liquidity-shock Absorption Event Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase264 precommits the next materially different route after Phase263 closed the repaired passive spread-capture/fill-model path.",
        "The route remains full-depth: Zerodha top-five market-by-price rows 1-5 and levels 2-5 features are mandatory, and L1-only variants are forbidden.",
        "This is not replay execution, strategy promotion, paper/live acceptance or a deployable profitability claim.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    input_parquet: Path = DEFAULT_INPUT_PARQUET,
    phase263_dir: Path = DEFAULT_PHASE263_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    input_stats = inspect_input(input_parquet)
    features = build_feature_catalog()
    families = build_event_family_catalog()
    labels = build_label_contract()
    grid = build_search_grid_contract()
    controls = build_control_contract()
    gates = build_gate_evaluation(phase263_dir, input_stats, features, families, labels, grid, controls)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    next_action = (
        "run_phase265_full_depth_liquidity_shock_absorption_event_training_search_no_paper_live"
        if hard_pass == len(hard)
        else "repair_phase264_liquidity_shock_absorption_precommit"
    )
    acceptance = pd.DataFrame(
        [
            ("phase264_liquidity_shock_precommit_complete", 1, "Phase264 full-depth liquidity-shock/absorption event precommit completed"),
            ("phase264_selected_route", SELECTED_ROUTE, "Selected route"),
            ("phase264_input_event_bar_rows", as_int(input_stats.get("event_bar_rows", 0)), "Input event bars"),
            ("phase264_input_symbols", as_int(input_stats.get("symbols", 0)), "Input symbols"),
            ("phase264_input_trade_dates", as_int(input_stats.get("trade_dates", 0)), "Input trade dates"),
            ("phase264_mean_l2_l5_bid_share", input_stats.get("mean_l2_l5_bid_share", 0.0), "Mean bid depth share from levels 2-5"),
            ("phase264_mean_l2_l5_ask_share", input_stats.get("mean_l2_l5_ask_share", 0.0), "Mean ask depth share from levels 2-5"),
            ("phase264_mean_abs_l2_l5_imbalance", input_stats.get("mean_abs_l2_l5_imbalance", 0.0), "Mean absolute L2-L5 imbalance"),
            ("phase264_feature_catalog_rows", len(features), "Feature catalog rows"),
            ("phase264_event_family_rows", len(families), "Event family rows"),
            ("phase264_label_contract_rows", len(labels), "Label contract rows"),
            ("phase264_search_grid_contract_rows", len(grid), "Search grid contract rows"),
            ("phase264_control_contract_rows", len(controls), "Control contract rows"),
            ("phase264_full_top_five_depth_required", 1, "Zerodha top-five rows 1-5 required"),
            ("phase264_levels_2_to_5_materiality_required", 1, "Levels 2-5 features required"),
            ("phase264_l1_only_candidate_allowed", 0, "L1-only candidates forbidden"),
            ("phase264_threshold_relaxation_only_allowed", 0, "Threshold relaxation only forbidden"),
            ("phase264_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase264_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase264_download_more_dates_now_allowed", 0, "No new download in Phase264"),
            ("phase264_replay_execution_allowed_now", 0, "No replay execution in Phase264"),
            ("phase264_strategy_promotion_allowed", 0, "No strategy promotion from Phase264"),
            ("phase264_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase264"),
            ("phase264_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase264"),
            ("phase264_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    features.to_csv(output_dir / "phase264_feature_catalog.csv", index=False)
    families.to_csv(output_dir / "phase264_event_family_catalog.csv", index=False)
    labels.to_csv(output_dir / "phase264_label_contract.csv", index=False)
    grid.to_csv(output_dir / "phase264_search_grid_contract.csv", index=False)
    controls.to_csv(output_dir / "phase264_control_contract.csv", index=False)
    gates.to_csv(output_dir / "phase264_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase264_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase264_full_depth_liquidity_shock_absorption_event_precommit_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Feature Catalog": features,
            "Event Family Catalog": families,
            "Label Contract": labels,
            "Search Grid Contract": grid,
            "Control Contract": controls,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase264_full_depth_liquidity_shock_absorption_event_precommit",
        **reproducibility_fields(
            artifact_id="phase264",
            generated_utc=generated_utc,
            inputs={"input_parquet": str(input_parquet), "phase263_dir": str(phase263_dir)},
            parameters={
                "selected_route": SELECTED_ROUTE,
                "full_top_five_depth_required": 1,
                "levels_2_to_5_materiality_required": 1,
                "l1_only_candidate_allowed": 0,
                "threshold_relaxation_only_allowed": 0,
                "download_more_dates_now_allowed": 0,
                "replay_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "feature_catalog": str(output_dir / "phase264_feature_catalog.csv"),
                "event_family_catalog": str(output_dir / "phase264_event_family_catalog.csv"),
                "label_contract": str(output_dir / "phase264_label_contract.csv"),
                "search_grid_contract": str(output_dir / "phase264_search_grid_contract.csv"),
                "control_contract": str(output_dir / "phase264_control_contract.csv"),
                "gate_evaluation": str(output_dir / "phase264_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase264_acceptance_summary.csv"),
                "report": str(output_dir / "phase264_full_depth_liquidity_shock_absorption_event_precommit_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase264_precommit_no_replay_liquidity_shock_absorption_event_contract",
        ),
    }
    (output_dir / "phase264_full_depth_liquidity_shock_absorption_event_precommit_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase264 full-depth liquidity-shock/absorption event precommit.")
    parser.add_argument("--input-parquet", type=Path, default=DEFAULT_INPUT_PARQUET)
    parser.add_argument("--phase263-dir", type=Path, default=DEFAULT_PHASE263_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(input_parquet=args.input_parquet, phase263_dir=args.phase263_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
