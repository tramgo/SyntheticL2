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
DEFAULT_PHASE403_DIR = Path("outputs/phase403")
DEFAULT_PHASE409_DIR = Path("outputs/phase409")
DEFAULT_REAL_ANCHOR_ROOTS = [Path("real_data_sample/l2_multiday_panel"), Path("real_data_sample/l2_unseen_validation")]
DEFAULT_OUTPUT_DIR = Path("outputs/phase410")

THESIS_ID = "P410_FULL_DEPTH_REPLENISHMENT_BREAKOUT_TAKER_ONLY"
NEXT_ACTION = "run_phase411_full_depth_replenishment_breakout_execution_no_paper_live"
REPAIR_ACTION = "repair_phase410_full_depth_replenishment_breakout_precommit"

INITIAL_CAPITAL_INR = 1_000_000.0
FIXED_NOTIONAL_INR = 100_000.0
MAX_CONCURRENT_POSITIONS = 2
COST_MULTIPLIER = 2.0
ANNUALIZED_THRESHOLD_PCT = 12.0
MIN_COMPLETED_ROUND_TRIPS = 30
MIN_TRADE_DATES = 5
MIN_SYMBOLS = 3
MIN_POSITIVE_DATE_FRACTION = 0.60

IMPULSE_LOOKBACK_SECONDS = 30
REBUILD_CONFIRM_SECONDS = 20
BREAKOUT_CONFIRM_SECONDS = 10
HORIZON_SECONDS = 180
STOP_BPS = 12.0
TAKE_PROFIT_BPS = 18.0
MIN_ABS_IMPULSE_BPS = 4.0
MIN_LEVELS_2_TO_5_REPLENISHMENT_PRESSURE = 0.12
MIN_TOP5_IMBALANCE_ALIGNMENT = 0.15
MIN_LEVEL_WEIGHTED_IMBALANCE_ALIGNMENT = 0.15
MAX_SPREAD_BPS = 8.0
MAX_DEPTH_WITHDRAWAL_PRESSURE = 0.10


def sha256_frame(frame: pd.DataFrame) -> str:
    payload = frame.to_csv(index=False, lineterminator="\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def real_anchor_dates(roots: list[Path]) -> list[str]:
    dates: set[str] = set()
    for root in roots:
        if not root.exists():
            continue
        for path in root.glob("trade_date=*"):
            if path.is_dir():
                dates.add(path.name.split("=", 1)[1])
    return sorted(dates)


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    if summary.empty:
        return default
    return metric_value(summary, metric, default)


def build_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("thesis_id", THESIS_ID, "Material-new full-depth L2 thesis after Phase409 falsified retail maker route."),
            ("material_difference", "taker_only_replenishment_breakout_not_market_making_not_passive_not_vacuum", "No two-sided quoting, no passive queue rescue, no liquidity-vacuum continuation."),
            ("market_hypothesis", "when impulse is followed by levels_2_to_5_replenishment_and_spread_control_price_breaks_in_impulse_direction", "Strong depth rebuild behind the move may indicate real continuation support."),
            ("event_sequence", "impulse_window_then_rebuild_window_then_breakout_confirmation_window", "Stateful sequence; not a one-bar reversal or same-event shortcut."),
            ("impulse_window_seconds", IMPULSE_LOOKBACK_SECONDS, "Past-only impulse measurement."),
            ("rebuild_confirm_seconds", REBUILD_CONFIRM_SECONDS, "Past-only depth rebuild confirmation window."),
            ("breakout_confirm_seconds", BREAKOUT_CONFIRM_SECONDS, "Past-only confirmation before taker entry."),
            ("horizon_seconds", HORIZON_SECONDS, "Exit horizon if stop/target not reached."),
            ("entry_execution", "taker_entry_after_breakout_confirmation", "No passive fill model and no maker rebate."),
            ("exit_execution", "taker_stop_or_target_or_horizon_exit", "Taker-only close."),
            ("side_rule", "trade_in_impulse_direction_only", "Long after positive impulse; short after negative impulse."),
            ("min_abs_impulse_bps", MIN_ABS_IMPULSE_BPS, "Fixed threshold, no post-result tuning."),
            ("min_levels_2_to_5_replenishment_pressure", MIN_LEVELS_2_TO_5_REPLENISHMENT_PRESSURE, "Core full-depth gate beyond L1."),
            ("min_top5_imbalance_alignment", MIN_TOP5_IMBALANCE_ALIGNMENT, "Top-five alignment with side."),
            ("min_level_weighted_imbalance_alignment", MIN_LEVEL_WEIGHTED_IMBALANCE_ALIGNMENT, "Level-weighted L1-L5 alignment with side."),
            ("max_spread_bps", MAX_SPREAD_BPS, "Avoid wide-spread conditions."),
            ("max_depth_withdrawal_pressure", MAX_DEPTH_WITHDRAWAL_PRESSURE, "Reject cases where visible book is being pulled."),
            ("stop_bps", STOP_BPS, "Fixed stop, not optimized after results."),
            ("take_profit_bps", TAKE_PROFIT_BPS, "Fixed target, not optimized after results."),
            ("full_depth_required", "L1_to_L5_book_state_with_levels_2_to_5_materiality", "L1-only variants forbidden."),
            ("cost_model", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha equity intraday NSE formula."),
            ("cost_multiplier", COST_MULTIPLIER, "Cost200 acceptance scoring."),
            ("capital", f"initial={INITIAL_CAPITAL_INR};notional={FIXED_NOTIONAL_INR};max_concurrent={MAX_CONCURRENT_POSITIONS}", "Fixed capital denominator; no unlimited capital."),
            ("acceptance", f"round_trips>={MIN_COMPLETED_ROUND_TRIPS};dates>={MIN_TRADE_DATES};symbols>={MIN_SYMBOLS};positive_date_fraction>={MIN_POSITIVE_DATE_FRACTION};annualized>={ANNUALIZED_THRESHOLD_PCT}", "Profitability must meet breadth and annualized gates."),
            ("controls", "side_flip;levels_2_to_5_removed;spread_gate_removed;synthetic_vs_real_anchor_sign", "Controls required in execution phase."),
            ("forbidden", "same_family_market_maker_tuning;passive_fill_rescue;liquidity_vacuum_rescue;bar_reversal_rescue;promotion;paper_live;deployable_profit_claim", "Boundaries remain closed."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def build_parameter_freeze() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("P410_FIXED_SIGNAL", "impulse_rebuild_breakout", "single frozen signal form"),
            ("P410_IMPULSE_LOOKBACK_SECONDS", IMPULSE_LOOKBACK_SECONDS, "past-only"),
            ("P410_REBUILD_CONFIRM_SECONDS", REBUILD_CONFIRM_SECONDS, "past-only"),
            ("P410_BREAKOUT_CONFIRM_SECONDS", BREAKOUT_CONFIRM_SECONDS, "past-only"),
            ("P410_HORIZON_SECONDS", HORIZON_SECONDS, "fixed"),
            ("P410_STOP_BPS", STOP_BPS, "fixed"),
            ("P410_TAKE_PROFIT_BPS", TAKE_PROFIT_BPS, "fixed"),
            ("P410_MIN_ABS_IMPULSE_BPS", MIN_ABS_IMPULSE_BPS, "fixed"),
            ("P410_MIN_L2_L5_REPLENISHMENT_PRESSURE", MIN_LEVELS_2_TO_5_REPLENISHMENT_PRESSURE, "fixed"),
            ("P410_MIN_TOP5_IMBALANCE_ALIGNMENT", MIN_TOP5_IMBALANCE_ALIGNMENT, "fixed"),
            ("P410_MIN_LEVEL_WEIGHTED_IMBALANCE_ALIGNMENT", MIN_LEVEL_WEIGHTED_IMBALANCE_ALIGNMENT, "fixed"),
            ("P410_MAX_SPREAD_BPS", MAX_SPREAD_BPS, "fixed"),
            ("P410_MAX_DEPTH_WITHDRAWAL_PRESSURE", MAX_DEPTH_WITHDRAWAL_PRESSURE, "fixed"),
        ],
        columns=["parameter_id", "value", "status"],
    )


def build_input_registry(phase298: pd.DataFrame, schema: pd.DataFrame, phase403: pd.DataFrame, phase409: pd.DataFrame, anchors: list[str]) -> pd.DataFrame:
    schema_present = 0
    if not schema.empty and "book_level_present_columns" in schema.columns:
        schema_present = int(pd.to_numeric(schema["book_level_present_columns"], errors="coerce").fillna(0).min())
    return pd.DataFrame(
        [
            ("phase298_dense_root", scalar(phase298, "phase298_dense_root", ""), "Raw dense source root."),
            ("phase298_raw_book_state_l1_l5_required", scalar(phase298, "phase298_raw_book_state_l1_l5_required", ""), "Full-depth source requirement."),
            ("phase298_levels_2_to_5_required", scalar(phase298, "phase298_levels_2_to_5_required", ""), "Levels 2-5 materiality."),
            ("phase298_l1_only_variant_rows", scalar(phase298, "phase298_l1_only_variant_rows", ""), "Must be zero."),
            ("phase298_net_edge_live_mask_rows", scalar(phase298, "phase298_net_edge_live_mask_rows", ""), "Must be zero."),
            ("phase298_schema_present_columns_min", schema_present, "Minimum present L1-L5 price/quantity/order columns in Phase298 schema audit."),
            ("phase403_material_new_thesis_required", scalar(phase403, "phase403_material_new_thesis_required", ""), "Phase403 material-new requirement."),
            ("phase409_selected_verdict", scalar(phase409, "phase409_selected_verdict", ""), "Phase409 closure context."),
            ("phase409_same_family_tuning_allowed", scalar(phase409, "phase409_same_family_tuning_allowed", ""), "Must be zero."),
            ("real_anchor_dates", ";".join(anchors), "Verified local real L2 anchor dates."),
            ("real_anchor_date_count", len(anchors), "At least 3 required."),
            ("execution_results_generated_now", 0, "Precommit only."),
        ],
        columns=["input_id", "value", "description"],
    )


def build_hard_gate_contract() -> pd.DataFrame:
    gates = [
        ("P411_TICK_ORDERED_REPLAY", "Execution must iterate ticks in timestamp order; no bar-only shortcut."),
        ("P411_STATEFUL_SEQUENCE", "Signal requires impulse then depth rebuild then breakout confirmation."),
        ("P411_TAKER_ONLY_EXECUTION", "No passive fills, no two-sided quoting, no maker rebate."),
        ("P411_FULL_DEPTH_L1_L5", "Execution must read all L1-L5 price/quantity/order fields where available."),
        ("P411_LEVELS_2_TO_5_MATERIAL", "At least one required signal gate must use levels 2-5 excluding L1."),
        ("P411_NO_LOOKAHEAD", "All feature windows must end before order arrival/fill evaluation."),
        ("P411_COST200_FIXED_CAPITAL", "Use Zerodha cost200, fixed initial capital and fixed notional."),
        ("P411_FIXED_PARAMETERS", "No post-result threshold tuning or rescue grid."),
        ("P411_EVENT_FLOOR", f"Completed round trips >= {MIN_COMPLETED_ROUND_TRIPS}."),
        ("P411_DATE_BREADTH", f"Distinct trade dates >= {MIN_TRADE_DATES}."),
        ("P411_SYMBOL_BREADTH", f"Distinct symbols >= {MIN_SYMBOLS}."),
        ("P411_POSITIVE_DATE_FRACTION", f"Positive date fraction >= {MIN_POSITIVE_DATE_FRACTION}."),
        ("P411_ANNUALIZED_FLOOR", f"Annualized fixed-capital return >= {ANNUALIZED_THRESHOLD_PCT} percent."),
        ("P411_SIDE_FLIP_CONTROL", "Side-flip control must not dominate the primary."),
        ("P411_L2_L5_REMOVED_CONTROL", "Removing levels 2-5 must degrade or invalidate the primary."),
        ("P411_SPREAD_GATE_REMOVED_CONTROL", "Spread-gate-removed control must be reported."),
        ("P411_REAL_ANCHOR_CROSS_CHECK", "Synthetic winner sign must be cross-checked on reserved real anchors."),
        ("P411_BOUNDARIES_CLOSED", "No promotion, paper/live acceptance or deployable claim."),
    ]
    return pd.DataFrame(
        [{"gate_id": gate, "requirement": requirement, "severity": "hard", "phase410_precommitted": 1} for gate, requirement in gates]
    )


def build_gate_evaluation(inputs: pd.DataFrame, contract: pd.DataFrame, freeze: pd.DataFrame, hard_contract: pd.DataFrame) -> pd.DataFrame:
    values = dict(zip(inputs["input_id"], inputs["value"]))
    schema_cols = as_int(values.get("phase298_schema_present_columns_min", 0))
    anchor_count = as_int(values.get("real_anchor_date_count", 0))
    forbidden = ";".join(contract.loc[contract["contract_id"].eq("forbidden"), "contract_value"].astype(str).tolist())
    material = ";".join(contract.loc[contract["contract_id"].eq("material_difference"), "contract_value"].astype(str).tolist())
    gates = [
        ("P410_PHASE298_RAW_DENSE_PRESENT", str(values.get("phase298_dense_root", "")) == "raw_synthetic_l2_dense_full_year", values.get("phase298_dense_root", ""), "raw_synthetic_l2_dense_full_year"),
        ("P410_FULL_DEPTH_SCHEMA_PRESENT", schema_cols >= 30, schema_cols, ">=30"),
        ("P410_LEVELS_2_TO_5_REQUIRED", str(values.get("phase298_levels_2_to_5_required", "")) == "1", values.get("phase298_levels_2_to_5_required", ""), 1),
        ("P410_L1_ONLY_FORBIDDEN", as_int(values.get("phase298_l1_only_variant_rows", 1)) == 0, values.get("phase298_l1_only_variant_rows", ""), 0),
        ("P410_NO_LOOKAHEAD_SOURCE", as_int(values.get("phase298_net_edge_live_mask_rows", 1)) == 0, values.get("phase298_net_edge_live_mask_rows", ""), 0),
        ("P410_PHASE403_MATERIAL_NEW_REQUIRED", str(values.get("phase403_material_new_thesis_required", "")) == "1", values.get("phase403_material_new_thesis_required", ""), 1),
        ("P410_PHASE409_MAKER_ROUTE_CLOSED", str(values.get("phase409_selected_verdict", "")) == "P409_CANCEL_RACE_MARKET_MAKER_FALSIFIED", values.get("phase409_selected_verdict", ""), "P409_CANCEL_RACE_MARKET_MAKER_FALSIFIED"),
        ("P410_NO_SAME_FAMILY_TUNING", str(values.get("phase409_same_family_tuning_allowed", "")) == "0", values.get("phase409_same_family_tuning_allowed", ""), 0),
        ("P410_MATERIALLY_DIFFERENT_THESIS", "not_market_making" in material and "not_passive" in material and "not_vacuum" in material, material, "not_closed_family"),
        ("P410_FIXED_PARAMETERS_FROZEN", len(freeze) >= 13, len(freeze), ">=13"),
        ("P410_TAKER_ONLY_PINNED", "taker_entry_after_breakout_confirmation" in ";".join(contract["contract_value"].astype(str)), "taker_only", "present"),
        ("P410_COST200_FIXED_CAPITAL_PINNED", COST_MULTIPLIER == 2.0 and INITIAL_CAPITAL_INR >= 1_000_000 and FIXED_NOTIONAL_INR <= 100_000, f"cost={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR};notional={FIXED_NOTIONAL_INR}", "cost200_fixed_capital"),
        ("P410_REAL_ANCHORS_AT_LEAST_THREE", anchor_count >= 3, anchor_count, ">=3"),
        ("P410_EXECUTION_HARD_GATES_PRECOMMITTED", len(hard_contract) == 18, len(hard_contract), 18),
        ("P410_RESULTS_NOT_GENERATED", as_int(values.get("execution_results_generated_now", 1)) == 0, values.get("execution_results_generated_now", ""), 0),
        ("P410_FORBIDDEN_ROUTES_CLOSED", all(x in forbidden for x in ["same_family_market_maker_tuning", "passive_fill_rescue", "liquidity_vacuum_rescue", "bar_reversal_rescue"]), forbidden, "closed_routes_listed"),
        ("P410_BOUNDARIES_CLOSED", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(contract: pd.DataFrame, inputs: pd.DataFrame, freeze: pd.DataFrame, hard_contract: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    freeze_hash = sha256_frame(freeze)
    return pd.DataFrame(
        [
            ("phase410_full_depth_replenishment_breakout_precommit_complete", 1, "Phase410 precommit completed"),
            ("phase410_thesis_id", THESIS_ID, "Frozen thesis"),
            ("phase410_material_new_after_phase409", 1, "Not market-making, passive rescue, liquidity-vacuum rescue or bar-reversal rescue"),
            ("phase410_contract_rows", len(contract), "Contract rows"),
            ("phase410_parameter_freeze_rows", len(freeze), "Frozen parameter rows"),
            ("phase410_parameter_freeze_hash", freeze_hash, "Hash of frozen parameter table"),
            ("phase410_real_anchor_date_count", inputs.loc[inputs["input_id"].eq("real_anchor_date_count"), "value"].iloc[0], "Local real anchor dates"),
            ("phase410_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha cost model"),
            ("phase410_cost_multiplier", COST_MULTIPLIER, "Cost200"),
            ("phase410_initial_capital_inr", INITIAL_CAPITAL_INR, "Fixed capital"),
            ("phase410_fixed_notional_inr", FIXED_NOTIONAL_INR, "Fixed notional per trade"),
            ("phase410_execution_results_generated", 0, "Precommit only"),
            ("phase410_strategy_promotion_allowed", 0, "No promotion"),
            ("phase410_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase410_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase410_execution_allowed_next", int(hard_pass == hard_rows), "Whether Phase411 may run"),
            ("phase410_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase410_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase410_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(
    output_dir: Path,
    acceptance: pd.DataFrame,
    contract: pd.DataFrame,
    freeze: pd.DataFrame,
    inputs: pd.DataFrame,
    hard_contract: pd.DataFrame,
    gates: pd.DataFrame,
) -> None:
    lines = [
        "# Phase410 Full-Depth Replenishment Breakout Precommit",
        "",
        "Phase410 freezes a materially different full-depth L2 thesis after Phase409 falsified the tested retail two-sided market-maker route.",
        "",
        "The thesis is taker-only continuation after a stateful sequence: impulse, levels 2-5 replenishment, spread control, then breakout confirmation.",
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
        "## Phase411 Hard-Gate Contract",
        "",
        _markdown_table(hard_contract),
        "",
        "## Phase410 Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "No strategy result, promotion, paper/live acceptance or deployable profitability claim is generated by Phase410.",
    ]
    (output_dir / "phase410_full_depth_replenishment_breakout_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    phase298_dir: Path = DEFAULT_PHASE298_DIR,
    phase403_dir: Path = DEFAULT_PHASE403_DIR,
    phase409_dir: Path = DEFAULT_PHASE409_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    real_anchor_roots: list[Path] | None = None,
) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase298 = read_csv(phase298_dir / "phase298_acceptance_summary.csv")
    schema = read_csv(phase298_dir / "phase298_raw_book_schema_audit.csv")
    phase403 = read_csv(phase403_dir / "phase403_acceptance_summary.csv")
    phase409 = read_csv(phase409_dir / "phase409_acceptance_summary.csv")
    if phase298.empty or schema.empty or phase403.empty or phase409.empty:
        raise FileNotFoundError("Phase410 requires Phase298, Phase403 and Phase409 summaries plus Phase298 schema audit.")
    roots = real_anchor_roots if real_anchor_roots is not None else DEFAULT_REAL_ANCHOR_ROOTS
    anchors = real_anchor_dates(roots)
    contract = build_contract()
    freeze = build_parameter_freeze()
    inputs = build_input_registry(phase298, schema, phase403, phase409, anchors)
    hard_contract = build_hard_gate_contract()
    gates = build_gate_evaluation(inputs, contract, freeze, hard_contract)
    acceptance = build_acceptance(contract, inputs, freeze, hard_contract, gates)
    contract.to_csv(output_dir / "phase410_frozen_thesis_contract.csv", index=False)
    freeze.to_csv(output_dir / "phase410_parameter_freeze.csv", index=False)
    inputs.to_csv(output_dir / "phase410_input_registry.csv", index=False)
    hard_contract.to_csv(output_dir / "phase410_execution_hard_gate_contract.csv", index=False)
    gates.to_csv(output_dir / "phase410_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase410_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, contract, freeze, inputs, hard_contract, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase410_full_depth_replenishment_breakout_precommit",
        **reproducibility_fields(
            artifact_id="phase410_full_depth_replenishment_breakout_precommit",
            generated_utc=generated_utc,
            inputs={
                "phase298_acceptance_summary": str(phase298_dir / "phase298_acceptance_summary.csv"),
                "phase298_raw_book_schema_audit": str(phase298_dir / "phase298_raw_book_schema_audit.csv"),
                "phase403_acceptance_summary": str(phase403_dir / "phase403_acceptance_summary.csv"),
                "phase409_acceptance_summary": str(phase409_dir / "phase409_acceptance_summary.csv"),
                "real_anchor_roots": ";".join(str(root) for root in roots),
            },
            parameters={
                "thesis_id": THESIS_ID,
                "parameter_freeze_hash": sha256_frame(freeze),
                "next_action": NEXT_ACTION,
            },
            outputs={"acceptance_summary": str(output_dir / "phase410_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase410_taker_only_order_arrival_no_passive_cancel_race",
        ),
    }
    (output_dir / "phase410_full_depth_replenishment_breakout_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase410 full-depth replenishment breakout precommit.")
    parser.add_argument("--phase298-dir", type=Path, default=DEFAULT_PHASE298_DIR)
    parser.add_argument("--phase403-dir", type=Path, default=DEFAULT_PHASE403_DIR)
    parser.add_argument("--phase409-dir", type=Path, default=DEFAULT_PHASE409_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase298_dir, args.phase403_dir, args.phase409_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
