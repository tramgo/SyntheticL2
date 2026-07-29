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


DEFAULT_PHASE260_DIR = Path("outputs/phase260")
DEFAULT_INPUT_PARQUET = Path("outputs/phase254/phase254_richer_raw_top5_depth_event_bars.parquet")
DEFAULT_OUTPUT_DIR = Path("outputs/phase261")
SELECTED_ROUTE = "P261_PASSIVE_OPPORTUNITY_BREADTH_AND_FILL_MODEL_REPAIR"


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
                quantile_cont(avg_spread_bps, 0.25)::double as spread_bps_q25,
                quantile_cont(avg_spread_bps, 0.50)::double as spread_bps_q50,
                quantile_cont(avg_spread_bps, 0.75)::double as spread_bps_q75,
                quantile_cont(avg_spread_bps, 0.90)::double as spread_bps_q90,
                avg(avg_cum_buy_qty_l2_l5 / nullif(avg_cum_buy_qty_l1_l5, 0))::double as mean_l2_l5_bid_share,
                avg(avg_cum_sell_qty_l2_l5 / nullif(avg_cum_sell_qty_l1_l5, 0))::double as mean_l2_l5_ask_share,
                median(avg_cum_buy_qty_l2_l5 / nullif(avg_cum_buy_qty_l1_l5, 0))::double as median_l2_l5_bid_share,
                median(avg_cum_sell_qty_l2_l5 / nullif(avg_cum_sell_qty_l1_l5, 0))::double as median_l2_l5_ask_share,
                avg(abs(avg_depth_beyond_l1_qty_imbalance))::double as mean_abs_beyond_l1_imbalance,
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


def build_opportunity_repair_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            (
                "P261_REPAIR_OPPORTUNITY_FILTER",
                "separate_opportunity_filter_from_fill_probability",
                "Generate candidate passive quote opportunities from spread, replenishment and full-depth regime first; score fill probability afterward.",
                "prevents_one_tick_or_one_symbol_overfiltering",
            ),
            (
                "P261_REPAIR_FILL_GRID",
                "calibrated_fill_probability_grid",
                "Search fill-probability assumptions over base fill rate, queue haircuts, churn haircuts, levels 2-5 support boosts and non-fill stress.",
                "prevents_single_formula_overfit",
            ),
            (
                "P261_REPAIR_BREADTH",
                "broaden_spread_replenishment_and_imbalance_thresholds",
                "Include lower spread quantiles and softer replenishment/imbalance thresholds before queue-adversity penalties are applied.",
                "increases_symbol_and_opportunity_breadth",
            ),
            (
                "P261_REPAIR_SIDE_SPACE",
                "bid_ask_both_and_skewed_quote_sides",
                "Keep bid-only, ask-only, two-sided and imbalance-skewed maker candidates so profitable direction is not assumed.",
                "forces_side_controls",
            ),
            (
                "P261_REPAIR_DEPTH_CORE",
                "levels_1_to_5_required_l2_l5_materiality_required",
                "Require top-five quantities/order counts and levels 2-5 shares in every candidate; L1-only variants are invalid by contract.",
                "protects_core_project_objective",
            ),
        ],
        columns=["repair_id", "repair_contract", "description", "why_it_matters"],
    )


def build_fill_probability_grid() -> pd.DataFrame:
    rows: list[tuple[Any, ...]] = []
    for profile_id, base_fill, queue_haircut, churn_haircut, l2_boost, nonfill_stress, adverse_mult in [
        ("conservative_low_fill", 0.08, 0.55, 0.60, 0.05, 1.25, 1.25),
        ("baseline_conservative", 0.14, 0.70, 0.75, 0.08, 1.00, 1.00),
        ("balanced_depth_supported", 0.20, 0.80, 0.85, 0.12, 0.85, 1.00),
        ("optimistic_but_capped", 0.28, 0.90, 0.90, 0.16, 0.70, 0.85),
    ]:
        for queue_adversity in [0.75, 1.00, 1.25]:
            rows.append(
                (
                    f"P261_FILL_{profile_id}_QA{str(queue_adversity).replace('.', 'p')}",
                    profile_id,
                    base_fill,
                    queue_haircut,
                    churn_haircut,
                    l2_boost,
                    nonfill_stress,
                    queue_adversity,
                    adverse_mult,
                    0.35,
                    "fill_probability = capped(base_fill * queue_haircut * churn_haircut + levels_2_to_5_support_boost); unfilled quotes receive no spread capture",
                )
            )
    return pd.DataFrame(
        rows,
        columns=[
            "fill_model_id",
            "profile",
            "base_fill_probability",
            "queue_haircut",
            "churn_haircut",
            "levels_2_to_5_support_boost",
            "nonfill_stress_multiplier",
            "queue_adversity_multiplier",
            "adverse_selection_penalty_multiplier",
            "max_fill_probability_cap",
            "formula_contract",
        ],
    )


def build_broadened_candidate_family_catalog() -> pd.DataFrame:
    rows = [
        (
            "P262_BROAD_PASSIVE_BID_REPLENISHMENT",
            "bid",
            "spread_quantile in [0.25,0.50,0.75]; bid_replenishment_quantile in [0.40,0.60,0.75]; abs_beyond_l1_imbalance >= [0.00,0.03,0.06]",
            "avg_cum_buy_qty_l1_l5;avg_cum_buy_qty_l2_l5;avg_depth_beyond_l1_qty_imbalance;depth_replenishment_pressure;top5_qty_churn_sum;top5_order_churn_sum",
        ),
        (
            "P262_BROAD_PASSIVE_ASK_REPLENISHMENT",
            "ask",
            "spread_quantile in [0.25,0.50,0.75]; ask_replenishment_quantile in [0.40,0.60,0.75]; abs_beyond_l1_imbalance >= [0.00,0.03,0.06]",
            "avg_cum_sell_qty_l1_l5;avg_cum_sell_qty_l2_l5;avg_depth_beyond_l1_qty_imbalance;depth_replenishment_pressure;top5_qty_churn_sum;top5_order_churn_sum",
        ),
        (
            "P262_TWO_SIDED_SPREAD_CAPTURE_LOW_CHURN",
            "both",
            "spread_quantile in [0.50,0.75,0.90]; top5_churn_quantile <= [0.40,0.60,0.75]; price_shift_quantile <= [0.50,0.75]",
            "avg_spread_bps;avg_cum_buy_qty_l1_l5;avg_cum_sell_qty_l1_l5;avg_cum_buy_qty_l2_l5;avg_cum_sell_qty_l2_l5;l1_price_shift_abs_sum",
        ),
        (
            "P262_IMBALANCE_SKEWED_MAKER_BROAD",
            "bid_or_ask",
            "top5 and levels-2-to-5 imbalance agree; imbalance threshold in [0.02,0.05,0.10]; spread_quantile >= [0.25,0.50]",
            "avg_cum_top5_qty_imbalance;avg_depth_beyond_l1_qty_imbalance;avg_order_count_imbalance_l1_l5;avg_spread_bps",
        ),
        (
            "P262_QUEUE_REPAIR_AVOIDANCE_OVERLAY",
            "filter",
            "Block or haircut opportunities with high L1 queue crowding, top-five churn, withdrawal pressure or L1 price shifts.",
            "avg_order_count_imbalance_l1_l5;top5_qty_churn_sum;top5_order_churn_sum;depth_withdrawal_pressure;l1_price_shift_abs_sum",
        ),
    ]
    return pd.DataFrame(
        rows,
        columns=["candidate_family_id", "quote_side", "threshold_grid_contract", "required_full_depth_features"],
    )


def build_control_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("random_side_control", "required", "Every candidate must beat deterministic random side under the same opportunity and fill model grid."),
            ("side_flip_control", "required", "Flipping bid/ask interpretation must degrade or invert edge, not improve it by accident."),
            ("cost_stress", "required", "Evaluate Zerodha statutory/brokerage charges at base, 1.5x and 2x."),
            ("queue_adversity_stress", "required", "Stress L1 queue crowding and top-five churn with fill haircut and adverse-selection penalty multipliers."),
            ("nonfill_stress", "required", "Unfilled passive quotes must earn zero spread capture and may still incur opportunity/latency risk in sensitivity checks."),
            ("opportunity_breadth_floor", "required", "Best candidate must exceed minimum opportunity, symbol and fill-equivalent breadth before any promotion discussion."),
            ("levels_1_to_5_depth_requirement", "required", "Use Zerodha top-five depth rows 1-5; levels 2-5 materiality is mandatory."),
            ("l1_only_candidate_family", "forbidden", "No L1-only strategy, feature, filter or candidate variant can survive."),
            ("paper_live_or_deployable_profitability_claim", "forbidden", "Phase261/262 cannot claim paper/live/deployable profitability."),
        ],
        columns=["control_id", "control_status", "description"],
    )


def build_gate_evaluation(
    phase260_dir: Path,
    input_stats: dict[str, Any],
    repair: pd.DataFrame,
    fill_grid: pd.DataFrame,
    families: pd.DataFrame,
    controls: pd.DataFrame,
) -> pd.DataFrame:
    phase260_next = str(metric_value(phase260_dir / "phase260_acceptance_summary.csv", "phase260_next_best_action", ""))
    route = read_csv(phase260_dir / "phase260_next_route_contract.csv")
    depth_contract_present = int(route["contract_value"].astype(str).str.contains("levels_1_to_5_required", case=False, na=False).sum()) if not route.empty else 0
    required_controls = controls[controls["control_status"].astype(str).eq("required")]
    required_feature_text = ";".join(families["required_full_depth_features"].astype(str).tolist()) if not families.empty else ""
    rows = [
        ("P261_PHASE260_WORK_ORDER_PRESENT", "run_phase261_passive_opportunity_breadth_fill_model_repair_precommit" in phase260_next, phase260_next, "Phase260 next action targets Phase261", "hard"),
        ("P261_PHASE260_DEPTH_CONTRACT_PRESENT", depth_contract_present >= 1, depth_contract_present, "levels_1_to_5_required present in Phase260 route", "hard"),
        ("P261_INPUT_PRESENT", as_int(input_stats.get("input_exists", 0)) == 1, input_stats.get("input_exists", 0), "Phase254 richer raw top-five event bars exist", "hard"),
        ("P261_EVENT_BAR_BREADTH", as_int(input_stats.get("event_bar_rows", 0)) >= 1000 and as_int(input_stats.get("symbols", 0)) >= 20, f"rows={input_stats.get('event_bar_rows', 0)};symbols={input_stats.get('symbols', 0)}", ">=1000 rows and >=20 symbols", "hard"),
        ("P261_REPAIR_CONTRACT_WRITTEN", len(repair) >= 5, len(repair), ">=5 repair contract rows", "hard"),
        ("P261_FILL_GRID_WRITTEN", len(fill_grid) >= 12, len(fill_grid), ">=12 fill grid rows", "hard"),
        ("P261_FULL_DEPTH_FAMILY_CATALOG_WRITTEN", len(families) >= 5 and all(token in required_feature_text for token in ["l1_l5", "l2_l5", "top5"]), len(families), ">=5 families using l1_l5, l2_l5 and top5 features", "hard"),
        ("P261_CONTROLS_WRITTEN", len(required_controls) >= 7, len(required_controls), ">=7 required controls", "hard"),
        ("P261_L1_ONLY_FORBIDDEN", int(controls["control_id"].astype(str).eq("l1_only_candidate_family").sum()) == 1, "l1_only_candidate_family forbidden", "L1-only candidates explicitly forbidden", "hard"),
        ("P261_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase261 Passive Opportunity Breadth and Fill-model Repair Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase261 converts the Phase260 route decision into an executable Phase262 search contract.",
        "The repair is deliberately full-depth: Zerodha top-five market-by-price rows 1-5 remain required, and L1-only variants are forbidden.",
        "It separates opportunity discovery from fill-probability scoring so the next search can test broader passive opportunities without pretending every quote fills.",
        "This is not a replay, not a strategy promotion, not paper/live acceptance and not a deployable profitability claim.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    input_parquet: Path = DEFAULT_INPUT_PARQUET,
    phase260_dir: Path = DEFAULT_PHASE260_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    input_stats = inspect_input(input_parquet)
    repair = build_opportunity_repair_contract()
    fill_grid = build_fill_probability_grid()
    families = build_broadened_candidate_family_catalog()
    controls = build_control_contract()
    gates = build_gate_evaluation(phase260_dir, input_stats, repair, fill_grid, families, controls)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    next_action = (
        "run_phase262_passive_opportunity_breadth_fill_model_training_search_full_top5_depth_no_paper_live"
        if hard_pass == len(hard)
        else "repair_phase261_passive_opportunity_breadth_fill_model_precommit"
    )
    acceptance = pd.DataFrame(
        [
            ("phase261_passive_repair_precommit_complete", 1, "Phase261 passive opportunity breadth and fill-model repair precommit completed"),
            ("phase261_selected_route", SELECTED_ROUTE, "Selected route"),
            ("phase261_input_event_bar_rows", as_int(input_stats.get("event_bar_rows", 0)), "Input richer raw top-five event bars"),
            ("phase261_input_symbols", as_int(input_stats.get("symbols", 0)), "Input symbol breadth"),
            ("phase261_input_trade_dates", as_int(input_stats.get("trade_dates", 0)), "Input trade dates"),
            ("phase261_mean_spread_bps", input_stats.get("mean_spread_bps", 0.0), "Mean spread bps in input"),
            ("phase261_median_spread_bps", input_stats.get("median_spread_bps", 0.0), "Median spread bps in input"),
            ("phase261_mean_l2_l5_bid_share", input_stats.get("mean_l2_l5_bid_share", 0.0), "Mean bid depth share from levels 2-5"),
            ("phase261_mean_l2_l5_ask_share", input_stats.get("mean_l2_l5_ask_share", 0.0), "Mean ask depth share from levels 2-5"),
            ("phase261_repair_contract_rows", len(repair), "Repair contract rows"),
            ("phase261_fill_probability_grid_rows", len(fill_grid), "Fill probability grid rows"),
            ("phase261_candidate_family_rows", len(families), "Broadened candidate family rows"),
            ("phase261_control_contract_rows", len(controls), "Control contract rows"),
            ("phase261_full_top_five_depth_required", 1, "Zerodha top-five rows 1-5 required"),
            ("phase261_levels_2_to_5_materiality_required", 1, "Beyond-L1 depth required"),
            ("phase261_l1_only_candidate_allowed", 0, "L1-only candidate forbidden"),
            ("phase261_download_more_dates_now_allowed", 0, "No new download in Phase261"),
            ("phase261_replay_execution_allowed_now", 0, "No replay execution in Phase261"),
            ("phase261_strategy_promotion_allowed", 0, "No strategy promotion from Phase261"),
            ("phase261_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase261"),
            ("phase261_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase261"),
            ("phase261_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase261_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase261_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    repair.to_csv(output_dir / "phase261_opportunity_repair_contract.csv", index=False)
    fill_grid.to_csv(output_dir / "phase261_fill_probability_grid.csv", index=False)
    families.to_csv(output_dir / "phase261_broadened_candidate_family_catalog.csv", index=False)
    controls.to_csv(output_dir / "phase261_control_contract.csv", index=False)
    gates.to_csv(output_dir / "phase261_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase261_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase261_passive_opportunity_breadth_fill_model_repair_precommit_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Opportunity Repair Contract": repair,
            "Fill Probability Grid": fill_grid,
            "Broadened Candidate Family Catalog": families,
            "Control Contract": controls,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase261_passive_opportunity_breadth_fill_model_repair_precommit",
        **reproducibility_fields(
            artifact_id="phase261",
            generated_utc=generated_utc,
            inputs={"input_parquet": str(input_parquet), "phase260_dir": str(phase260_dir)},
            parameters={
                "selected_route": SELECTED_ROUTE,
                "full_top_five_depth_required": 1,
                "levels_2_to_5_materiality_required": 1,
                "l1_only_candidate_allowed": 0,
                "download_more_dates_now_allowed": 0,
                "replay_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "opportunity_repair_contract": str(output_dir / "phase261_opportunity_repair_contract.csv"),
                "fill_probability_grid": str(output_dir / "phase261_fill_probability_grid.csv"),
                "broadened_candidate_family_catalog": str(output_dir / "phase261_broadened_candidate_family_catalog.csv"),
                "control_contract": str(output_dir / "phase261_control_contract.csv"),
                "gate_evaluation": str(output_dir / "phase261_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase261_acceptance_summary.csv"),
                "report": str(output_dir / "phase261_passive_opportunity_breadth_fill_model_repair_precommit_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase261_precommit_no_replay_fill_model_contract",
        ),
    }
    (output_dir / "phase261_passive_opportunity_breadth_fill_model_repair_precommit_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase261 passive opportunity breadth and fill-model repair precommit.")
    parser.add_argument("--input-parquet", type=Path, default=DEFAULT_INPUT_PARQUET)
    parser.add_argument("--phase260-dir", type=Path, default=DEFAULT_PHASE260_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(input_parquet=args.input_parquet, phase260_dir=args.phase260_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
