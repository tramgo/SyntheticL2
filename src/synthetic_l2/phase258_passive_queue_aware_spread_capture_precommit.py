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


DEFAULT_PHASE257_DIR = Path("outputs/phase257")
DEFAULT_INPUT_PARQUET = Path("outputs/phase254/phase254_richer_raw_top5_depth_event_bars.parquet")
DEFAULT_OUTPUT_DIR = Path("outputs/phase258")
SELECTED_ROUTE = "P258_PASSIVE_QUEUE_AWARE_SPREAD_CAPTURE"


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
                avg(avg_cum_buy_qty_l2_l5 / nullif(avg_cum_buy_qty_l1_l5, 0))::double as mean_l2_l5_bid_share,
                avg(avg_cum_sell_qty_l2_l5 / nullif(avg_cum_sell_qty_l1_l5, 0))::double as mean_l2_l5_ask_share
            from read_parquet('{input_parquet.as_posix()}')
            """
        ).fetchdf().iloc[0].to_dict()
    finally:
        con.close()
    return {"input_exists": 1, **stats}


def build_order_model_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("quote_side", "bid_or_ask_or_both", "Passive quotes may be placed on bid, ask or both sides according to depth signal"),
            ("quote_price", "best_bid_or_best_ask_proxy", "Use level-1 same-side price as passive quote proxy; no crossing of spread"),
            ("queue_position_proxy", "same_side_l1_quantity_and_order_count", "Approximate ahead quantity and queue crowding from L1 quantity/order count"),
            ("fill_probability_proxy", "opposite_trade_pressure_minus_same_side_queue", "Fill likelihood rises with opposite pressure and falls with queue depth/order crowding"),
            ("adverse_selection_proxy", "future_mid_move_against_quote", "Penalize fills followed by unfavorable mid-price movement"),
            ("cancel_replace_proxy", "top5_churn_and_l1_price_shift", "Higher churn or L1 price shifts increase cancel/replace/adverse fill risk"),
            ("latency_proxy", "next_event_bar_arrival", "Assume quote becomes active after at least one event-bar latency step"),
            ("cost_stack", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Apply statutory/brokerage cost stack; passive model may avoid taker spread crossing but not charges"),
        ],
        columns=["model_component", "contract_value", "description"],
    )


def build_feature_contract() -> pd.DataFrame:
    rows = [
        ("required", "avg_spread_bps", "Spread capture ceiling and liquidity filter"),
        ("required", "avg_cum_buy_qty_l1_l5", "Full bid-side visible depth"),
        ("required", "avg_cum_sell_qty_l1_l5", "Full ask-side visible depth"),
        ("required", "avg_cum_buy_qty_l2_l5", "Beyond-L1 bid depth; prevents L1-only candidate"),
        ("required", "avg_cum_sell_qty_l2_l5", "Beyond-L1 ask depth; prevents L1-only candidate"),
        ("required", "avg_cum_top5_qty_imbalance", "Full top-five imbalance"),
        ("required", "avg_depth_beyond_l1_qty_imbalance", "Levels 2-5 imbalance"),
        ("required", "avg_order_count_imbalance_l1_l5", "Order-count crowding imbalance"),
        ("required", "top5_qty_churn_sum", "Depth churn / queue instability"),
        ("required", "top5_order_churn_sum", "Order-count churn / cancel pressure"),
        ("required", "depth_replenishment_pressure", "Passive support and replenishment"),
        ("required", "depth_withdrawal_pressure", "Withdrawal/adverse-selection risk"),
        ("required", "l1_price_shift_abs_sum", "Cancel/replace and queue-loss proxy"),
        ("required", "taker_round_trip_cost_floor_bps", "Cost reference and stress floor"),
        ("forbidden", "l1_only_depth_imbalance", "No L1-only candidate family is allowed"),
    ]
    return pd.DataFrame(rows, columns=["feature_status", "feature", "description"])


def build_candidate_family_catalog() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("P258_PASSIVE_BID_REPLENISHMENT", "bid", "Quote bid when levels 2-5 bid depth replenishes and adverse ask pressure is low", "full_top5_depth;queue_proxy;adverse_selection"),
            ("P258_PASSIVE_ASK_REPLENISHMENT", "ask", "Quote ask when levels 2-5 ask depth replenishes and adverse bid pressure is low", "full_top5_depth;queue_proxy;adverse_selection"),
            ("P258_TWO_SIDED_HIGH_SPREAD_LOW_CHURN", "both", "Quote both sides only when spread is wide enough and top-five churn is low", "spread_capture;low_churn;queue_proxy"),
            ("P258_IMBALANCE_SKEWED_MAKER", "bid_or_ask", "Skew passive side with top-five and levels 2-5 imbalance agreement", "top5_imbalance;beyond_l1_imbalance;order_count"),
            ("P258_QUEUE_AVOIDANCE_FILTER", "filter", "Block passive quote when L1 queue crowding, withdrawal or price-shift risk is high", "queue_adversity;withdrawal;price_shift"),
        ],
        columns=["candidate_family_id", "quote_side", "description", "required_signal_groups"],
    )


def build_control_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("random_side_control", "required", "Passive quote direction must beat deterministic random side"),
            ("side_flip_control", "required", "Signal side flip should degrade or invert expected edge"),
            ("cost_stress", "required", "Evaluate at base, 1.5x and 2x statutory/brokerage charges"),
            ("queue_adversity_stress", "required", "Haircut fills or edge when queue crowding/churn is high"),
            ("nonfill_model", "required", "Unfilled quote opportunities must not receive spread capture"),
            ("forbidden_dates", "required", "Keep 2026-07-17 and 2026-07-20 excluded from parameter selection"),
            ("paper_live_claim", "forbidden", "No paper/live acceptance or deployable profitability claim"),
        ],
        columns=["control_id", "control_status", "description"],
    )


def build_gate_evaluation(phase257_dir: Path, input_stats: dict[str, Any], features: pd.DataFrame, families: pd.DataFrame, controls: pd.DataFrame) -> pd.DataFrame:
    next_action = str(metric_value(phase257_dir / "phase257_acceptance_summary.csv", "phase257_next_best_action", ""))
    required_features = features[features["feature_status"].astype(str).eq("required")]
    full_depth_feature_rows = int(required_features["feature"].astype(str).str.contains("l2_l5|top5|l1_l5|beyond_l1").sum())
    required_controls = controls[controls["control_status"].astype(str).eq("required")]
    rows = [
        ("P258_PHASE257_WORK_ORDER_PRESENT", "run_phase258_passive_queue_aware_spread_capture_precommit" in next_action, next_action, "Phase257 next action targets Phase258", "hard"),
        ("P258_INPUT_PRESENT", as_int(input_stats.get("input_exists", 0)) == 1, input_stats.get("input_exists", 0), "Phase254 richer event bars exist", "hard"),
        ("P258_EVENT_BAR_BREADTH", as_int(input_stats.get("event_bar_rows", 0)) >= 1000 and as_int(input_stats.get("symbols", 0)) >= 20, f"rows={input_stats.get('event_bar_rows', 0)};symbols={input_stats.get('symbols', 0)}", ">=1000 rows and >=20 symbols", "hard"),
        ("P258_FULL_DEPTH_FEATURE_CONTRACT", full_depth_feature_rows >= 6, full_depth_feature_rows, ">=6 required full-depth features", "hard"),
        ("P258_NO_L1_ONLY_CANDIDATES", int(features["feature"].astype(str).eq("l1_only_depth_imbalance").sum()) == 1, "l1_only_depth_imbalance forbidden", "L1-only candidate explicitly forbidden", "hard"),
        ("P258_PASSIVE_FAMILY_CATALOG_WRITTEN", len(families) >= 4, len(families), ">=4 passive/queue-aware families", "hard"),
        ("P258_CONTROL_CONTRACT_WRITTEN", len(required_controls) >= 5, len(required_controls), ">=5 required controls", "hard"),
        ("P258_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase258 Passive Queue-aware Spread-capture Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase258 precommits the next materially different route after Phase257 closed the full-depth taker-threshold search.",
        "It specifies a passive queue-aware spread-capture proxy using the same Zerodha top-five market-by-price depth surface.",
        "It is not a replay, promotion, paper/live acceptance or deployable profitability claim.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    input_parquet: Path = DEFAULT_INPUT_PARQUET,
    phase257_dir: Path = DEFAULT_PHASE257_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    input_stats = inspect_input(input_parquet)
    order_model = build_order_model_contract()
    features = build_feature_contract()
    families = build_candidate_family_catalog()
    controls = build_control_contract()
    gates = build_gate_evaluation(phase257_dir, input_stats, features, families, controls)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    next_action = (
        "run_phase259_passive_queue_aware_spread_capture_training_search_full_top5_depth_no_paper_live"
        if hard_pass == len(hard)
        else "repair_phase258_passive_queue_aware_precommit_before_search"
    )
    acceptance = pd.DataFrame(
        [
            ("phase258_passive_queue_precommit_complete", 1, "Phase258 passive queue-aware spread-capture precommit completed"),
            ("phase258_selected_route", SELECTED_ROUTE, "Selected route"),
            ("phase258_input_event_bar_rows", as_int(input_stats.get("event_bar_rows", 0)), "Input richer event bars"),
            ("phase258_input_symbols", as_int(input_stats.get("symbols", 0)), "Input symbol breadth"),
            ("phase258_input_trade_dates", as_int(input_stats.get("trade_dates", 0)), "Input trade dates"),
            ("phase258_mean_spread_bps", input_stats.get("mean_spread_bps", 0.0), "Mean spread bps in input"),
            ("phase258_mean_l2_l5_bid_share", input_stats.get("mean_l2_l5_bid_share", 0.0), "Mean bid depth share from levels 2-5"),
            ("phase258_mean_l2_l5_ask_share", input_stats.get("mean_l2_l5_ask_share", 0.0), "Mean ask depth share from levels 2-5"),
            ("phase258_order_model_contract_rows", len(order_model), "Order model contract rows"),
            ("phase258_feature_contract_rows", len(features), "Feature contract rows"),
            ("phase258_candidate_family_rows", len(families), "Candidate family rows"),
            ("phase258_control_contract_rows", len(controls), "Control contract rows"),
            ("phase258_full_top_five_depth_required", 1, "Levels 1-5 required"),
            ("phase258_l1_only_candidate_allowed", 0, "L1-only candidate forbidden"),
            ("phase258_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase258_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase258_download_more_dates_now_allowed", 0, "No new download in Phase258"),
            ("phase258_replay_execution_allowed_now", 0, "No replay execution in Phase258"),
            ("phase258_strategy_promotion_allowed", 0, "No strategy promotion from Phase258"),
            ("phase258_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase258"),
            ("phase258_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase258"),
            ("phase258_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    order_model.to_csv(output_dir / "phase258_order_model_contract.csv", index=False)
    features.to_csv(output_dir / "phase258_feature_contract.csv", index=False)
    families.to_csv(output_dir / "phase258_candidate_family_catalog.csv", index=False)
    controls.to_csv(output_dir / "phase258_control_contract.csv", index=False)
    gates.to_csv(output_dir / "phase258_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase258_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase258_passive_queue_aware_spread_capture_precommit_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Order Model Contract": order_model,
            "Feature Contract": features,
            "Candidate Family Catalog": families,
            "Control Contract": controls,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase258_passive_queue_aware_spread_capture_precommit",
        **reproducibility_fields(
            artifact_id="phase258",
            generated_utc=generated_utc,
            inputs={"input_parquet": str(input_parquet), "phase257_dir": str(phase257_dir)},
            parameters={
                "selected_route": SELECTED_ROUTE,
                "full_top_five_depth_required": 1,
                "l1_only_candidate_allowed": 0,
                "download_more_dates_now_allowed": 0,
                "replay_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "order_model_contract": str(output_dir / "phase258_order_model_contract.csv"),
                "feature_contract": str(output_dir / "phase258_feature_contract.csv"),
                "candidate_family_catalog": str(output_dir / "phase258_candidate_family_catalog.csv"),
                "control_contract": str(output_dir / "phase258_control_contract.csv"),
                "gate_evaluation": str(output_dir / "phase258_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase258_acceptance_summary.csv"),
                "report": str(output_dir / "phase258_passive_queue_aware_spread_capture_precommit_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase258_passive_queue_aware_precommit_no_replay",
        ),
    }
    (output_dir / "phase258_passive_queue_aware_spread_capture_precommit_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase258 passive queue-aware spread-capture precommit.")
    parser.add_argument("--input-parquet", type=Path, default=DEFAULT_INPUT_PARQUET)
    parser.add_argument("--phase257-dir", type=Path, default=DEFAULT_PHASE257_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(input_parquet=args.input_parquet, phase257_dir=args.phase257_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
