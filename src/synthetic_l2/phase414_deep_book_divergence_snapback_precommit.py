from __future__ import annotations

import argparse
import hashlib
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


DEFAULT_PHASE298_DIR = Path("outputs/phase298")
DEFAULT_PHASE409_DIR = Path("outputs/phase409")
DEFAULT_PHASE412_DIR = Path("outputs/phase412")
DEFAULT_PHASE413_DIR = Path("outputs/phase413")
DEFAULT_OUTPUT_DIR = Path("outputs/phase414")

THESIS_ID = "P414_DEEP_BOOK_DIVERGENCE_SNAPBACK_TAKER_ONLY"
NEXT_ACTION = "run_phase415_deep_book_divergence_snapback_execution_no_paper_live"
REPAIR_ACTION = "repair_phase414_deep_book_divergence_snapback_precommit"

INITIAL_CAPITAL_INR = 1_000_000.0
FIXED_NOTIONAL_INR = 100_000.0
COST_MULTIPLIER = 2.0
MAX_CONCURRENT_POSITIONS = 2
ANNUALIZED_THRESHOLD_PCT = 12.0
MIN_COMPLETED_ROUND_TRIPS = 30
MIN_TRADE_DATES = 5
MIN_SYMBOLS = 3
MIN_POSITIVE_DATE_FRACTION = 0.60

IMPULSE_LOOKBACK_SECONDS = 20
CONFIRM_SECONDS = 5
HORIZON_SECONDS = 120
MIN_ABS_IMPULSE_BPS = 3.0
MIN_OPPOSING_L2_L5_IMBALANCE = 0.08
MAX_TOP5_ALIGNMENT_WITH_IMPULSE = 0.08
MIN_LEVEL_WEIGHTED_DIVERGENCE = 0.05
MAX_SPREAD_BPS = 8.0
MAX_WITHDRAWAL_PRESSURE = 0.25
STOP_BPS = 10.0
TAKE_PROFIT_BPS = 14.0


def sha256_frame(frame: pd.DataFrame) -> str:
    payload = frame.to_csv(index=False, lineterminator="\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    if summary.empty:
        return default
    return metric_value(summary, metric, default)


def build_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("thesis_id", THESIS_ID, "Material-new less-sparse full-depth L2 thesis after Phase413 attribution."),
            ("material_difference", "deep_book_divergence_snapback_not_replenishment_breakout_not_market_making_not_passive", "Uses opposing deeper-book pressure, not aligned replenishment breakout or two-sided quoting."),
            ("phase413_basis", "top5_alignment_and_l2_l5_replenishment_were_sparsity_bottlenecks", "Do not require simultaneous top-five alignment and high replenishment."),
            ("market_hypothesis", "when short_impulse_runs_against_deeper_l2_l5_pressure_and_top5_does_not_confirm_it_price_may_snap_back", "Depth disagreement, not price-bar reversal alone."),
            ("entry_side", "opposite_impulse_toward_deeper_book_pressure", "Taker entry in the deep-book pressure direction."),
            ("execution_profile", "taker_entry_taker_stop_target_or_horizon_exit", "No passive fill model, no maker rebate."),
            ("impulse_lookback_seconds", IMPULSE_LOOKBACK_SECONDS, "Past-only impulse window."),
            ("confirm_seconds", CONFIRM_SECONDS, "Past-only book confirmation window."),
            ("horizon_seconds", HORIZON_SECONDS, "Fixed exit horizon."),
            ("min_abs_impulse_bps", MIN_ABS_IMPULSE_BPS, "Fixed impulse threshold."),
            ("min_opposing_l2_l5_imbalance", MIN_OPPOSING_L2_L5_IMBALANCE, "Required levels 2-5 pressure against impulse."),
            ("max_top5_alignment_with_impulse", MAX_TOP5_ALIGNMENT_WITH_IMPULSE, "Top-of-book must not strongly confirm impulse."),
            ("min_level_weighted_divergence", MIN_LEVEL_WEIGHTED_DIVERGENCE, "Level-weighted pressure must support snapback side."),
            ("max_spread_bps", MAX_SPREAD_BPS, "Avoid wide-spread execution."),
            ("max_withdrawal_pressure", MAX_WITHDRAWAL_PRESSURE, "Reject severe depth pulling."),
            ("stop_bps", STOP_BPS, "Fixed stop."),
            ("take_profit_bps", TAKE_PROFIT_BPS, "Fixed target."),
            ("full_depth_required", "L1_to_L5_book_state_with_levels_2_to_5_directional_pressure", "L1-only variants forbidden."),
            ("cost_model", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha equity intraday NSE formula."),
            ("cost_multiplier", COST_MULTIPLIER, "Cost200 acceptance scoring."),
            ("capital", f"initial={INITIAL_CAPITAL_INR};notional={FIXED_NOTIONAL_INR};max_concurrent={MAX_CONCURRENT_POSITIONS}", "Fixed capital denominator."),
            ("acceptance", f"round_trips>={MIN_COMPLETED_ROUND_TRIPS};dates>={MIN_TRADE_DATES};symbols>={MIN_SYMBOLS};positive_date_fraction>={MIN_POSITIVE_DATE_FRACTION};annualized>={ANNUALIZED_THRESHOLD_PCT}", "Must be profitable with breadth."),
            ("controls", "side_flip;levels_2_to_5_removed;top5_only;spread_gate_removed;real_anchor_sign", "Controls must be reported."),
            ("forbidden", "phase410_threshold_relaxation;market_maker_rescue;passive_fill_rescue;bar_return_reversal_alone;promotion;paper_live;deployable_claim", "Closed boundaries."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def build_parameter_freeze() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("P414_IMPULSE_LOOKBACK_SECONDS", IMPULSE_LOOKBACK_SECONDS, "fixed"),
            ("P414_CONFIRM_SECONDS", CONFIRM_SECONDS, "fixed"),
            ("P414_HORIZON_SECONDS", HORIZON_SECONDS, "fixed"),
            ("P414_MIN_ABS_IMPULSE_BPS", MIN_ABS_IMPULSE_BPS, "fixed"),
            ("P414_MIN_OPPOSING_L2_L5_IMBALANCE", MIN_OPPOSING_L2_L5_IMBALANCE, "fixed"),
            ("P414_MAX_TOP5_ALIGNMENT_WITH_IMPULSE", MAX_TOP5_ALIGNMENT_WITH_IMPULSE, "fixed"),
            ("P414_MIN_LEVEL_WEIGHTED_DIVERGENCE", MIN_LEVEL_WEIGHTED_DIVERGENCE, "fixed"),
            ("P414_MAX_SPREAD_BPS", MAX_SPREAD_BPS, "fixed"),
            ("P414_MAX_WITHDRAWAL_PRESSURE", MAX_WITHDRAWAL_PRESSURE, "fixed"),
            ("P414_STOP_BPS", STOP_BPS, "fixed"),
            ("P414_TAKE_PROFIT_BPS", TAKE_PROFIT_BPS, "fixed"),
        ],
        columns=["parameter_id", "value", "status"],
    )


def build_input_registry(
    phase298: pd.DataFrame,
    schema: pd.DataFrame,
    phase409: pd.DataFrame,
    phase412: pd.DataFrame,
    phase413: pd.DataFrame,
    stage413: pd.DataFrame,
    first413: pd.DataFrame,
) -> pd.DataFrame:
    schema_present = 0
    if not schema.empty and "book_level_present_columns" in schema.columns:
        schema_present = int(pd.to_numeric(schema["book_level_present_columns"], errors="coerce").fillna(0).min())
    synthetic_scan = scalar(phase413, "phase413_synthetic_scan_points", "")
    pass_all = scalar(phase413, "phase413_synthetic_pass_all_filters", "")
    l2_stage = stage413[(stage413["panel"].astype(str).eq("synthetic")) & (stage413["stage"].astype(str).eq("l2_l5_replenishment"))]
    top5_first = first413[(first413["panel"].astype(str).eq("synthetic")) & (first413["first_failure_stage"].astype(str).eq("top5_alignment"))]
    return pd.DataFrame(
        [
            ("phase298_dense_root", scalar(phase298, "phase298_dense_root", ""), "Raw dense source root."),
            ("phase298_full_depth_required", scalar(phase298, "phase298_raw_book_state_l1_l5_required", ""), "Must be one."),
            ("phase298_levels_2_to_5_required", scalar(phase298, "phase298_levels_2_to_5_required", ""), "Must be one."),
            ("phase298_l1_only_variant_rows", scalar(phase298, "phase298_l1_only_variant_rows", ""), "Must be zero."),
            ("phase298_net_edge_live_mask_rows", scalar(phase298, "phase298_net_edge_live_mask_rows", ""), "Must be zero."),
            ("phase298_schema_present_columns_min", schema_present, "Minimum present L1-L5 price/quantity/order columns."),
            ("phase409_maker_route_closed", scalar(phase409, "phase409_selected_verdict", ""), "Closed market-maker context."),
            ("phase412_zero_event_verdict", scalar(phase412, "phase412_selected_verdict", ""), "Closed replenishment-breakout context."),
            ("phase413_synthetic_scan_points", synthetic_scan, "Attribution universe size."),
            ("phase413_synthetic_pass_all_filters", pass_all, "Must be zero for zero-event diagnosis."),
            ("phase413_l2_l5_replenishment_pass_rate", l2_stage["pass_rate"].iloc[0] if not l2_stage.empty else "", "Phase413 bottleneck evidence."),
            ("phase413_top5_alignment_first_failure_count", top5_first["count"].iloc[0] if not top5_first.empty else "", "Phase413 earliest failure evidence."),
            ("execution_results_generated_now", 0, "Precommit only."),
        ],
        columns=["input_id", "value", "description"],
    )


def build_hard_gate_contract() -> pd.DataFrame:
    gates = [
        ("P415_TICK_ORDERED_REPLAY", "Execution must iterate ticks in timestamp order."),
        ("P415_DEEP_BOOK_DIVERGENCE_SIGNAL", "Signal must require levels 2-5 pressure opposing impulse."),
        ("P415_NOT_PHASE410_THRESHOLD_RELAXATION", "No reuse of replenishment-breakout same-family thresholds as a rescue."),
        ("P415_TAKER_ONLY_EXECUTION", "No passive fills, no maker rebate, no two-sided quoting."),
        ("P415_FULL_DEPTH_L1_L5", "Execution must read L1-L5 book state."),
        ("P415_LEVELS_2_TO_5_MATERIAL", "Removing levels 2-5 must be a logged control."),
        ("P415_NO_LOOKAHEAD", "All features must be computed before entry tick."),
        ("P415_COST200_FIXED_CAPITAL", "Use Zerodha cost200 with fixed capital and notional."),
        ("P415_FIXED_PARAMETERS", "No post-result tuning."),
        ("P415_EVENT_FLOOR", f"Completed round trips >= {MIN_COMPLETED_ROUND_TRIPS}."),
        ("P415_DATE_BREADTH", f"Distinct trade dates >= {MIN_TRADE_DATES}."),
        ("P415_SYMBOL_BREADTH", f"Distinct symbols >= {MIN_SYMBOLS}."),
        ("P415_POSITIVE_DATE_FRACTION", f"Positive date fraction >= {MIN_POSITIVE_DATE_FRACTION}."),
        ("P415_ANNUALIZED_FLOOR", f"Annualized fixed-capital return >= {ANNUALIZED_THRESHOLD_PCT} percent."),
        ("P415_SIDE_FLIP_CONTROL", "Side-flip must not dominate primary."),
        ("P415_L2_L5_REMOVED_CONTROL", "Levels 2-5 removed control must degrade or invalidate primary."),
        ("P415_TOP5_ONLY_CONTROL", "Top5-only control must be reported."),
        ("P415_REAL_ANCHOR_CROSS_CHECK", "Synthetic winner sign must be cross-checked on real anchors."),
        ("P415_BOUNDARIES_CLOSED", "No promotion, paper/live acceptance or deployable claim."),
    ]
    return pd.DataFrame(
        [{"gate_id": gate, "requirement": requirement, "severity": "hard", "phase414_precommitted": 1} for gate, requirement in gates]
    )


def build_gate_evaluation(inputs: pd.DataFrame, contract: pd.DataFrame, freeze: pd.DataFrame, hard_contract: pd.DataFrame) -> pd.DataFrame:
    values = dict(zip(inputs["input_id"], inputs["value"]))
    schema_cols = as_int(values.get("phase298_schema_present_columns_min", 0))
    forbidden = ";".join(contract.loc[contract["contract_id"].eq("forbidden"), "contract_value"].astype(str).tolist())
    material = ";".join(contract.loc[contract["contract_id"].eq("material_difference"), "contract_value"].astype(str).tolist())
    gates = [
        ("P414_PHASE298_RAW_DENSE_PRESENT", str(values.get("phase298_dense_root", "")) == "raw_synthetic_l2_dense_full_year", values.get("phase298_dense_root", ""), "raw_synthetic_l2_dense_full_year"),
        ("P414_FULL_DEPTH_SCHEMA_PRESENT", schema_cols >= 30, schema_cols, ">=30"),
        ("P414_LEVELS_2_TO_5_REQUIRED", str(values.get("phase298_levels_2_to_5_required", "")) == "1", values.get("phase298_levels_2_to_5_required", ""), 1),
        ("P414_L1_ONLY_FORBIDDEN", as_int(values.get("phase298_l1_only_variant_rows", 1)) == 0, values.get("phase298_l1_only_variant_rows", ""), 0),
        ("P414_NO_LOOKAHEAD_SOURCE", as_int(values.get("phase298_net_edge_live_mask_rows", 1)) == 0, values.get("phase298_net_edge_live_mask_rows", ""), 0),
        ("P414_MARKET_MAKER_ROUTE_CLOSED", str(values.get("phase409_maker_route_closed", "")) == "P409_CANCEL_RACE_MARKET_MAKER_FALSIFIED", values.get("phase409_maker_route_closed", ""), "P409_CANCEL_RACE_MARKET_MAKER_FALSIFIED"),
        ("P414_REPLENISHMENT_BREAKOUT_CLOSED", str(values.get("phase412_zero_event_verdict", "")) == "P412_REPLENISHMENT_BREAKOUT_REJECTED_AS_ZERO_EVENT_FORM", values.get("phase412_zero_event_verdict", ""), "P412_REPLENISHMENT_BREAKOUT_REJECTED_AS_ZERO_EVENT_FORM"),
        ("P414_PHASE413_ATTRIBUTION_PRESENT", as_int(values.get("phase413_synthetic_scan_points", 0)) > 0 and as_int(values.get("phase413_synthetic_pass_all_filters", 1)) == 0, f"scan={values.get('phase413_synthetic_scan_points', '')};pass_all={values.get('phase413_synthetic_pass_all_filters', '')}", "scan>0;pass_all=0"),
        ("P414_MATERIALLY_DIFFERENT_LESS_SPARSE_FORM", "not_replenishment_breakout" in material and "not_market_making" in material and "not_passive" in material, material, "different_closed_families"),
        ("P414_FULL_DEPTH_DIVERGENCE_REQUIRED", any(contract["contract_id"].astype(str).eq("min_opposing_l2_l5_imbalance")), "opposing_l2_l5_imbalance", "present"),
        ("P414_FIXED_PARAMETERS_FROZEN", len(freeze) >= 11, len(freeze), ">=11"),
        ("P414_TAKER_ONLY_PINNED", "taker_entry_taker_stop_target_or_horizon_exit" in ";".join(contract["contract_value"].astype(str)), "taker_only", "present"),
        ("P414_COST200_FIXED_CAPITAL_PINNED", COST_MULTIPLIER == 2.0 and INITIAL_CAPITAL_INR >= 1_000_000 and FIXED_NOTIONAL_INR <= 100_000, f"cost={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR};notional={FIXED_NOTIONAL_INR}", "cost200_fixed_capital"),
        ("P414_EXECUTION_HARD_GATES_PRECOMMITTED", len(hard_contract) == 19, len(hard_contract), 19),
        ("P414_RESULTS_NOT_GENERATED", as_int(values.get("execution_results_generated_now", 1)) == 0, values.get("execution_results_generated_now", ""), 0),
        ("P414_FORBIDDEN_ROUTES_CLOSED", all(x in forbidden for x in ["phase410_threshold_relaxation", "market_maker_rescue", "passive_fill_rescue", "bar_return_reversal_alone"]), forbidden, "closed_routes_listed"),
        ("P414_BOUNDARIES_CLOSED", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(contract: pd.DataFrame, inputs: pd.DataFrame, freeze: pd.DataFrame, hard_contract: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    freeze_hash = sha256_frame(freeze)
    return pd.DataFrame(
        [
            ("phase414_deep_book_divergence_snapback_precommit_complete", 1, "Phase414 precommit completed"),
            ("phase414_thesis_id", THESIS_ID, "Frozen thesis"),
            ("phase414_material_new_after_phase413", 1, "Deep-book divergence snapback, not Phase410 threshold relaxation"),
            ("phase414_contract_rows", len(contract), "Contract rows"),
            ("phase414_parameter_freeze_rows", len(freeze), "Frozen parameter rows"),
            ("phase414_parameter_freeze_hash", freeze_hash, "Hash of frozen parameter table"),
            ("phase414_phase413_synthetic_scan_points", inputs.loc[inputs["input_id"].eq("phase413_synthetic_scan_points"), "value"].iloc[0], "Phase413 attribution scan points"),
            ("phase414_phase413_l2_l5_replenishment_pass_rate", inputs.loc[inputs["input_id"].eq("phase413_l2_l5_replenishment_pass_rate"), "value"].iloc[0], "Phase413 sparsity clue"),
            ("phase414_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha cost model"),
            ("phase414_cost_multiplier", COST_MULTIPLIER, "Cost200"),
            ("phase414_initial_capital_inr", INITIAL_CAPITAL_INR, "Fixed capital"),
            ("phase414_fixed_notional_inr", FIXED_NOTIONAL_INR, "Fixed notional per trade"),
            ("phase414_execution_results_generated", 0, "Precommit only"),
            ("phase414_strategy_promotion_allowed", 0, "No promotion"),
            ("phase414_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase414_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase414_execution_allowed_next", int(hard_pass == hard_rows), "Whether Phase415 may run"),
            ("phase414_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase414_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase414_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, contract: pd.DataFrame, freeze: pd.DataFrame, inputs: pd.DataFrame, hard_contract: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase414 Deep-Book Divergence Snapback Precommit",
        "",
        "Phase414 freezes a materially new less-sparse full-depth L2 thesis using the Phase413 failure map.",
        "",
        "The thesis trades a short-horizon taker snapback when a price impulse is opposed by levels 2-5 depth pressure and top-five does not strongly confirm the impulse.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Frozen Thesis Contract",
        "",
        _markdown_table(contract),
        "",
        "## Frozen Parameters",
        "",
        _markdown_table(freeze),
        "",
        "## Input Registry",
        "",
        _markdown_table(inputs),
        "",
        "## Phase415 Hard-Gate Contract",
        "",
        _markdown_table(hard_contract),
        "",
        "## Phase414 Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "No strategy result, promotion, paper/live acceptance or deployable profitability claim is generated by Phase414.",
    ]
    (output_dir / "phase414_deep_book_divergence_snapback_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    phase298_dir: Path = DEFAULT_PHASE298_DIR,
    phase409_dir: Path = DEFAULT_PHASE409_DIR,
    phase412_dir: Path = DEFAULT_PHASE412_DIR,
    phase413_dir: Path = DEFAULT_PHASE413_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase298 = read_csv(phase298_dir / "phase298_acceptance_summary.csv")
    schema = read_csv(phase298_dir / "phase298_raw_book_schema_audit.csv")
    phase409 = read_csv(phase409_dir / "phase409_acceptance_summary.csv")
    phase412 = read_csv(phase412_dir / "phase412_acceptance_summary.csv")
    phase413 = read_csv(phase413_dir / "phase413_acceptance_summary.csv")
    stage413 = read_csv(phase413_dir / "phase413_stage_summary.csv")
    first413 = read_csv(phase413_dir / "phase413_first_failure_summary.csv")
    if phase298.empty or schema.empty or phase409.empty or phase412.empty or phase413.empty or stage413.empty or first413.empty:
        raise FileNotFoundError("Phase414 requires Phase298, Phase409, Phase412 and Phase413 evidence.")
    contract = build_contract()
    freeze = build_parameter_freeze()
    inputs = build_input_registry(phase298, schema, phase409, phase412, phase413, stage413, first413)
    hard_contract = build_hard_gate_contract()
    gates = build_gate_evaluation(inputs, contract, freeze, hard_contract)
    acceptance = build_acceptance(contract, inputs, freeze, hard_contract, gates)
    contract.to_csv(output_dir / "phase414_frozen_thesis_contract.csv", index=False)
    freeze.to_csv(output_dir / "phase414_parameter_freeze.csv", index=False)
    inputs.to_csv(output_dir / "phase414_input_registry.csv", index=False)
    hard_contract.to_csv(output_dir / "phase414_execution_hard_gate_contract.csv", index=False)
    gates.to_csv(output_dir / "phase414_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase414_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, contract, freeze, inputs, hard_contract, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase414_deep_book_divergence_snapback_precommit",
        **reproducibility_fields(
            artifact_id="phase414_deep_book_divergence_snapback_precommit",
            generated_utc=generated_utc,
            inputs={
                "phase298_acceptance_summary": str(phase298_dir / "phase298_acceptance_summary.csv"),
                "phase409_acceptance_summary": str(phase409_dir / "phase409_acceptance_summary.csv"),
                "phase412_acceptance_summary": str(phase412_dir / "phase412_acceptance_summary.csv"),
                "phase413_acceptance_summary": str(phase413_dir / "phase413_acceptance_summary.csv"),
            },
            parameters={"thesis_id": THESIS_ID, "parameter_freeze_hash": sha256_frame(freeze), "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase414_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase414_taker_only_next_tick_execution_precommit",
        ),
    }
    (output_dir / "phase414_deep_book_divergence_snapback_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase414 deep-book divergence snapback precommit.")
    parser.add_argument("--phase298-dir", type=Path, default=DEFAULT_PHASE298_DIR)
    parser.add_argument("--phase409-dir", type=Path, default=DEFAULT_PHASE409_DIR)
    parser.add_argument("--phase412-dir", type=Path, default=DEFAULT_PHASE412_DIR)
    parser.add_argument("--phase413-dir", type=Path, default=DEFAULT_PHASE413_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase298_dir, args.phase409_dir, args.phase412_dir, args.phase413_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
