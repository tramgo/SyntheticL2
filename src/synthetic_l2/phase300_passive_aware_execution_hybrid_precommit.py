from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE299_DIR = Path("outputs/phase299")
DEFAULT_PHASE298_DIR = Path("outputs/phase298")
DEFAULT_OUTPUT_DIR = Path("outputs/phase300")

SELECTED_ROUTE = "P300_PASSIVE_AWARE_DIRECTIONAL_L2_EXECUTION_HYBRID"
NEXT_ACTION = "run_phase300_passive_aware_execution_hybrid_no_paper_live"
REPAIR_ACTION = "repair_phase300_passive_aware_execution_hybrid_precommit"

ANNUALIZED_THRESHOLD_PCT = 12.0
MIN_EVENT_ROWS = 30
MAX_INITIAL_NOTIONAL_INR = 100000.0


def build_charter() -> pd.DataFrame:
    rows = [
        ("charter_id", "P300_PASSIVE_AWARE_DIRECTIONAL_L2_EXECUTION", "Phase300 precommit charter."),
        ("status", "PRECOMMIT_NO_RESULTS_GENERATED", "Commit this charter before generating Phase300 backtest results."),
        ("thesis", "directional_l2_edge_may_need_passive_aware_execution_to_survive_retail_costs", "Prior taker-style edges were thin versus 2x Zerodha cost stress."),
        ("not_market_making", "1", "This is passive-aware execution of directional signals, not two-sided continuous retail market-making."),
        ("directional_signal_source", "P235;P268;P280;P281;P282;P298_sparse_directional_signal_seeds", "Reuse validated directional signals; no fresh alpha search in Phase300."),
        ("raw_book_state_source", "P51_raw_dense_full_year_lake;P298_schema_audit", "Use top-five market-by-price depth levels 1-5 price/qty/order-count."),
        ("levels_2_to_5_materiality_required", "1", "No L1-only variants."),
        ("cost_model", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha NSE equity intraday cost model."),
        ("cost_stress", "cost200", "2x cost stress required."),
        ("capital_denominator", "fixed_initial_capital", "No unlimited-capital annualization."),
        ("initial_notional_cap", f"lt_{MAX_INITIAL_NOTIONAL_INR:.0f}_INR", "Per-order fixed notional must be below the charter cap."),
        ("isolation_unit", "strategy_symbol_date", "Per strategy, symbol, date isolation is required for scoring diagnostics."),
        ("fill_model", "P(fill|queue_depth,side,horizon)_from_raw_depth_levels_1_to_5", "Passive fills must be probabilistic, not assumed."),
        ("retail_queue_prior", "back_of_queue_pessimistic", "Retail order starts behind displayed queue."),
        ("adverse_selection_penalty", "fill_conditioned_toxicity_penalty_required", "Passive fills are penalized for being more likely when informed flow is against us."),
        ("forced_flatten_cost", "leftover_inventory_pays_taker_spread_plus_full_statutory_costs", "No free spread saving by refusing to exit."),
        ("entry_policy", "passive_limit_entry_wait_cancel_or_cross_if_edge_exceeds_total_cost", "Hybrid entry policy."),
        ("exit_policy", "passive_when_calm_aggressive_when_risk_or_signal_expiry", "Never stay exposed merely to save spread."),
        ("brokerage_and_taxes", "brokerage_per_executed_order_STT_sell_side_txn_GST_SEBI_stamp", "Costs apply to passive and aggressive executions; no maker rebate assumed."),
        ("no_lookahead", "net_edge_live_mask_rows_must_equal_0", "Labels may not be used as live masks."),
        ("acceptance_event_floor", str(MIN_EVENT_ROWS), "A sparse >12% result below 30 events is discovery-only."),
        ("acceptance_annualized_threshold_pct", str(ANNUALIZED_THRESHOLD_PCT), "Cost200 annualized threshold."),
        ("acceptance_breadth", "multi_symbol_and_multi_date_positive", "Not a single-day/single-symbol pocket."),
        ("rank_stability", "rank_stable_1x_to_2x_cost", "No cost-stress ordering reversal."),
        ("kill_switch", "close_if_no_robust_cost200_above12_or_best_below_30_or_only_survives_by_weakening_penalty", "Do not iterate to rescue after honest failure."),
        ("strategy_replay_allowed", "0", "Boundary remains closed."),
        ("strategy_promotion_allowed", "0", "Boundary remains closed."),
        ("paper_or_live_acceptance_allowed", "0", "Boundary remains closed."),
        ("deployable_profitability_claim_allowed", "0", "Boundary remains closed."),
    ]
    return pd.DataFrame(rows, columns=["charter_item", "value", "description"])


def build_input_registry(phase299_summary: pd.DataFrame, phase298_summary: pd.DataFrame, phase298_schema: pd.DataFrame) -> pd.DataFrame:
    if "book_level_present_columns" in phase298_schema.columns:
        book_present = int(pd.to_numeric(phase298_schema["book_level_present_columns"], errors="coerce").fillna(0).min())
    else:
        schema_cols = set(phase298_schema.get("column", pd.Series(dtype=str)).astype(str)) if not phase298_schema.empty else set()
        required_book_cols = []
        for side in ("buy", "sell"):
            for level in range(1, 6):
                required_book_cols.extend([f"{side}_{level}_price", f"{side}_{level}_quantity", f"{side}_{level}_orders"])
        book_present = sum(1 for col in required_book_cols if col in schema_cols)
    rows = [
        ("phase299_work_order", str(metric_value(phase299_summary, "phase299_next_best_action", "")), "Phase299 must route to Phase300."),
        ("phase299_selected_route", str(metric_value(phase299_summary, "phase299_selected_next_route", "")), "Selected next route."),
        ("phase299_directional_signal_seed_rows", as_int(metric_value(phase299_summary, "phase299_directional_signal_seed_rows", 0)), "Directional seeds available."),
        ("phase298_raw_depth_schema_columns_present", book_present, "Required raw levels 1-5 price/qty/order-count columns present in Phase298 schema audit."),
        ("phase298_l1_only_variant_rows", as_int(metric_value(phase298_summary, "phase298_l1_only_variant_rows", 0)), "L1-only rows from Phase298."),
        ("phase298_net_edge_live_mask_rows", as_int(metric_value(phase298_summary, "phase298_net_edge_live_mask_rows", 0)), "Live leakage rows from Phase298."),
        ("cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned cost model."),
        ("raw_dense_source", "raw_synthetic_l2_dense_full_year", "Raw dense lake root."),
        ("execution_result_generation_allowed_by_this_phase", 0, "This precommit does not generate Phase300 backtest results."),
    ]
    return pd.DataFrame(rows, columns=["input_id", "value", "description"])


def build_execution_work_order() -> pd.DataFrame:
    rows = [
        ("1_signal_intake", "load_phase299_directional_signal_seeds", "Reuse directional seeds from prior phases; no new alpha grid."),
        ("2_raw_depth_features", "compute_queue_depth_spread_microprice_depth_slope_replenishment_from_levels_1_to_5", "Feature update uses full top-five market-by-price depth."),
        ("3_passive_entry_model", "estimate_fill_probability_from_queue_depth_side_horizon_with_back_of_queue_prior", "Passive entry cannot fill deterministically."),
        ("4_cancel_or_cross", "cancel_if_market_moves_away_cross_only_if_expected_move_exceeds_total_cost", "Hybrid policy."),
        ("5_adverse_selection", "apply_fill_conditioned_toxicity_penalty_to_all_passive_fills", "Filled passive orders pay toxicity penalty."),
        ("6_exit_policy", "exit_passively_when_calm_aggressively_on_risk_signal_expiry_or_eod", "Do not hold exposure to save spread."),
        ("7_forced_flatten", "charge_taker_spread_and_full_statutory_cost_for_leftover_inventory", "End-of-signal or EOD inventory must be flattened."),
        ("8_cost_scoring", "zerodha_costs_cost200_fixed_initial_capital_initial_notional_lt_100000", "Pinned retail cost model and fixed capital."),
        ("9_acceptance", "events_ge_30_annualized_gt_12_cost200_breadth_rank_stability", "Sparse <30-event sparks are clues only."),
        ("10_boundaries", "replay_0_promotion_0_paper_live_0_profitability_claim_0", "No promotion on Phase300 precommit or training run."),
    ]
    return pd.DataFrame(rows, columns=["step_id", "required_action", "description"])


def build_gate_evaluation(phase299_summary: pd.DataFrame, inputs: pd.DataFrame, charter: pd.DataFrame) -> pd.DataFrame:
    phase299_complete = as_int(metric_value(phase299_summary, "phase299_interpretation_complete", 0))
    phase299_next = str(metric_value(phase299_summary, "phase299_next_best_action", ""))
    seed_rows = as_int(metric_value(phase299_summary, "phase299_directional_signal_seed_rows", 0))
    l1_only_rows = int(inputs.loc[inputs["input_id"].eq("phase298_l1_only_variant_rows"), "value"].iloc[0])
    live_mask_rows = int(inputs.loc[inputs["input_id"].eq("phase298_net_edge_live_mask_rows"), "value"].iloc[0])
    schema_count = int(inputs.loc[inputs["input_id"].eq("phase298_raw_depth_schema_columns_present"), "value"].iloc[0])
    gates = [
        ("P300_PRECOMMIT_PHASE299_WORK_ORDER_PRESENT", phase299_complete == 1 and "phase300" in phase299_next, phase299_next, "Phase299 routes to Phase300"),
        ("P300_PRECOMMIT_INPUTS_VERSION_PINNED", seed_rows > 0 and schema_count >= 30, f"seeds={seed_rows};schema_cols={schema_count}", "directional seeds and raw depth schema present"),
        ("P300_PRECOMMIT_L1_ONLY_FORBIDDEN", l1_only_rows == 0, l1_only_rows, 0),
        ("P300_PRECOMMIT_NO_LOOKAHEAD", live_mask_rows == 0, live_mask_rows, 0),
        ("P300_PRECOMMIT_FILL_MODEL_REQUIRED", charter["charter_item"].astype(str).eq("fill_model").any(), "fill_model", "required"),
        ("P300_PRECOMMIT_ADVERSE_SELECTION_REQUIRED", charter["charter_item"].astype(str).eq("adverse_selection_penalty").any(), "adverse_selection_penalty", "required"),
        ("P300_PRECOMMIT_FORCED_FLATTEN_REQUIRED", charter["charter_item"].astype(str).eq("forced_flatten_cost").any(), "forced_flatten_cost", "required"),
        ("P300_PRECOMMIT_COST200_FIXED_CAPITAL", "cost200" in set(charter["value"].astype(str)) and "fixed_initial_capital" in set(charter["value"].astype(str)), "cost200;fixed_initial_capital", "required"),
        ("P300_PRECOMMIT_BOUNDARIES_CLOSED", all(str(v) == "0" for v in charter.loc[charter["charter_item"].isin(["strategy_replay_allowed", "strategy_promotion_allowed", "paper_or_live_acceptance_allowed", "deployable_profitability_claim_allowed"]), "value"]), "replay=0;promotion=0;paper=0;claim=0", "all zero"),
        ("P300_PRECOMMIT_RESULTS_NOT_GENERATED", int(inputs.loc[inputs["input_id"].eq("execution_result_generation_allowed_by_this_phase"), "value"].iloc[0]) == 0, 0, 0),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(charter: pd.DataFrame, inputs: pd.DataFrame, work_order: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    next_action = NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION
    return pd.DataFrame(
        [
            ("phase300_precommit_complete", 1, "Phase300 passive-aware execution precommit completed"),
            ("phase300_selected_route", SELECTED_ROUTE, "Selected route"),
            ("phase300_charter_rows", len(charter), "Charter rows"),
            ("phase300_input_registry_rows", len(inputs), "Input registry rows"),
            ("phase300_execution_work_order_rows", len(work_order), "Execution work-order rows"),
            ("phase300_directional_signal_seed_rows", int(inputs.loc[inputs["input_id"].eq("phase299_directional_signal_seed_rows"), "value"].iloc[0]), "Directional seed rows from Phase299"),
            ("phase300_raw_depth_schema_columns_present", int(inputs.loc[inputs["input_id"].eq("phase298_raw_depth_schema_columns_present"), "value"].iloc[0]), "Required raw depth columns present"),
            ("phase300_l1_only_variant_rows", int(inputs.loc[inputs["input_id"].eq("phase298_l1_only_variant_rows"), "value"].iloc[0]), "L1-only rows"),
            ("phase300_net_edge_live_mask_rows", int(inputs.loc[inputs["input_id"].eq("phase298_net_edge_live_mask_rows"), "value"].iloc[0]), "Live leakage rows"),
            ("phase300_fill_model_required", 1, "Passive fill model required"),
            ("phase300_adverse_selection_required", 1, "Adverse selection penalty required"),
            ("phase300_forced_flatten_cost_required", 1, "Forced flatten cost required"),
            ("phase300_cost200_required", 1, "2x cost stress required"),
            ("phase300_fixed_capital_required", 1, "Fixed capital denominator required"),
            ("phase300_min_event_rows", MIN_EVENT_ROWS, "Acceptance event floor"),
            ("phase300_annualized_threshold_pct", ANNUALIZED_THRESHOLD_PCT, "Acceptance annualized threshold"),
            ("phase300_results_generated", 0, "Precommit only; no Phase300 results generated"),
            ("phase300_strategy_replay_allowed", 0, "No replay"),
            ("phase300_strategy_promotion_allowed", 0, "No promotion"),
            ("phase300_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase300_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase300_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase300_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase300_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, charter: pd.DataFrame, inputs: pd.DataFrame, work_order: pd.DataFrame, gates: pd.DataFrame, acceptance: pd.DataFrame) -> None:
    lines = [
        "# Phase300 Passive-Aware Execution of Directional L2 Signals Precommit",
        "",
        "Phase300 freezes the execution-realism charter before any Phase300 results are generated.",
        "",
        "This is not market-making. It is passive-aware execution of already-discovered directional top-five-depth signals.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "## Charter",
        "",
        _markdown_table(charter),
        "",
        "## Input Registry",
        "",
        _markdown_table(inputs),
        "",
        "## Execution Work Order",
        "",
        _markdown_table(work_order),
    ]
    (output_dir / "phase300_passive_aware_execution_hybrid_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase299_dir: Path = DEFAULT_PHASE299_DIR, phase298_dir: Path = DEFAULT_PHASE298_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase299_summary = read_csv(phase299_dir / "phase299_acceptance_summary.csv")
    phase298_summary = read_csv(phase298_dir / "phase298_acceptance_summary.csv")
    phase298_schema = read_csv(phase298_dir / "phase298_raw_book_schema_audit.csv")
    if phase299_summary.empty or phase298_summary.empty:
        raise FileNotFoundError(f"Phase299 or Phase298 acceptance summary is missing under {phase299_dir} / {phase298_dir}")
    charter = build_charter()
    inputs = build_input_registry(phase299_summary, phase298_summary, phase298_schema)
    work_order = build_execution_work_order()
    gates = build_gate_evaluation(phase299_summary, inputs, charter)
    acceptance = build_acceptance(charter, inputs, work_order, gates)

    charter.to_csv(output_dir / "phase300_precommit_charter.csv", index=False)
    inputs.to_csv(output_dir / "phase300_input_registry.csv", index=False)
    work_order.to_csv(output_dir / "phase300_execution_work_order.csv", index=False)
    gates.to_csv(output_dir / "phase300_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase300_acceptance_summary.csv", index=False)
    write_report(output_dir, charter, inputs, work_order, gates, acceptance)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase300_passive_aware_execution_hybrid_precommit",
        **reproducibility_fields(
            artifact_id="phase300",
            generated_utc=generated_utc,
            inputs={
                "phase299_acceptance_summary": str(phase299_dir / "phase299_acceptance_summary.csv"),
                "phase298_raw_book_schema_audit": str(phase298_dir / "phase298_raw_book_schema_audit.csv"),
            },
            parameters={
                "selected_route": SELECTED_ROUTE,
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "min_event_rows": MIN_EVENT_ROWS,
                "max_initial_notional_inr": MAX_INITIAL_NOTIONAL_INR,
                "results_generated": 0,
            },
            outputs={"acceptance_summary": str(output_dir / "phase300_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase300_precommit_only",
        ),
    }
    (output_dir / "phase300_passive_aware_execution_hybrid_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase300 passive-aware execution hybrid precommit.")
    parser.add_argument("--phase299-dir", type=Path, default=DEFAULT_PHASE299_DIR)
    parser.add_argument("--phase298-dir", type=Path, default=DEFAULT_PHASE298_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(phase299_dir=args.phase299_dir, phase298_dir=args.phase298_dir, output_dir=args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
