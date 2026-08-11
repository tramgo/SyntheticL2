from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE403_DIR = Path("outputs/phase403")
DEFAULT_PHASE401_DIR = Path("outputs/phase401")
DEFAULT_OUTPUT_DIR = Path("outputs/phase404")

THESIS_ID = "P404_CATALYST_LIQUIDITY_VACUUM_CONTINUATION_FULL_DEPTH"
NEXT_ACTION = "run_phase405_liquidity_vacuum_continuation_execution_no_paper_live"
REPAIR_ACTION = "repair_phase404_liquidity_vacuum_continuation_precommit"

INITIAL_CAPITAL_INR = 250_000.0
FIXED_NOTIONAL_INR = 100_000.0
MAX_CONCURRENT_POSITIONS = 2
COST_MULTIPLIER = 2.0
ANNUALIZED_THRESHOLD_PCT = 12.0
MIN_SELECTED_EVENT_ROWS = 30

MIN_ABS_IMPULSE_BPS = 2.5
MIN_ABS_TOP5_IMBALANCE = 0.10
MIN_ABS_L2_L5_IMBALANCE = 0.10
MAX_REPLENISHMENT_RATIO = 0.75
DECISION_DELAY_SECONDS = 120
HORIZON_SECONDS = 900


def build_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("thesis_id", THESIS_ID, "Materially new thesis after Phase403 closure."),
            ("material_difference", "liquidity_vacuum_continuation_not_reversal_not_passive_rescue", "Do not reuse same reversal/passive-aware rescue route."),
            ("entry_side", "continue_catalyst_impulse_side", "Direction follows the post-catalyst impulse."),
            ("impulse_filter", f"abs(impulse_bps)>={MIN_ABS_IMPULSE_BPS}", "Fixed threshold, no search."),
            ("top5_alignment", f"sign(decision_top5_qty_imbalance)==impulse_side and abs>= {MIN_ABS_TOP5_IMBALANCE}", "Full top-five confirmation."),
            ("l2_l5_alignment", f"sign(decision_l2_l5_qty_imbalance)==impulse_side and abs>= {MIN_ABS_L2_L5_IMBALANCE}", "Levels 2-5 materiality required."),
            ("liquidity_vacuum", f"replenishment_ratio<={MAX_REPLENISHMENT_RATIO}", "Continuation only when visible replenishment is weak."),
            ("timing", f"decision_delay={DECISION_DELAY_SECONDS};horizon={HORIZON_SECONDS}", "Reuse current event-feature timing."),
            ("execution_profile", "taker_entry_taker_exit_cost200_fixed_capital", "No passive fill rescue; all-in Zerodha 2x cost stress."),
            ("capital", f"initial={INITIAL_CAPITAL_INR};notional={FIXED_NOTIONAL_INR};max_concurrent={MAX_CONCURRENT_POSITIONS}", "Fixed capital annualization, no unlimited capital."),
            ("acceptance", f"selected_events>={MIN_SELECTED_EVENT_ROWS};annualized>{ANNUALIZED_THRESHOLD_PCT};breadth_multi_symbol_date", "Same acceptance discipline."),
            ("controls", "side_flip_and_depth_removed_controls", "Controls must be logged."),
            ("forbidden", "parameter_search;same_route_rescue;promotion;paper_live;deployable_profit_claim", "Boundaries remain closed."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def build_input_registry(phase403: pd.DataFrame, phase401_events: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("phase403_material_new_required", metric_value(phase403, "phase403_material_new_thesis_required", ""), "Phase403 requires material-new thesis."),
            ("phase403_same_route_rescue_allowed", metric_value(phase403, "phase403_same_route_rescue_allowed", ""), "Must be zero."),
            ("phase401_event_feature_rows", len(phase401_events), "Latest real-L2 event feature rows."),
            ("phase401_ready_event_feature_rows", int(phase401_events["status"].astype(str).eq("ready").sum()) if not phase401_events.empty and "status" in phase401_events.columns else 0, "Ready latest real-L2 event feature rows."),
            ("required_columns_present", required_columns_present(phase401_events), "All columns required for execution."),
            ("cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned cost model."),
        ],
        columns=["input_id", "value", "description"],
    )


def required_columns_present(events: pd.DataFrame) -> int:
    required = {
        "status",
        "symbol",
        "diagnostic_trade_date",
        "decision_ms",
        "exit_ms",
        "impulse_bps",
        "impulse_side_sign",
        "replenishment_ratio",
        "decision_top5_qty_imbalance",
        "decision_l2_l5_qty_imbalance",
        "entry_long_price",
        "exit_long_price",
        "entry_short_price",
        "exit_short_price",
    }
    return int(required.issubset(set(events.columns)))


def build_gate_evaluation(phase403: pd.DataFrame, inputs: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    material_new = str(metric_value(phase403, "phase403_material_new_thesis_required", "0")) == "1"
    same_route_closed = str(metric_value(phase403, "phase403_same_route_rescue_allowed", "1")) == "0"
    ready = int(inputs.loc[inputs["input_id"].eq("phase401_ready_event_feature_rows"), "value"].iloc[0])
    columns_present = int(inputs.loc[inputs["input_id"].eq("required_columns_present"), "value"].iloc[0])
    gates = [
        ("P404_PHASE403_MATERIAL_NEW_REQUIRED", material_new, metric_value(phase403, "phase403_material_new_thesis_required", ""), 1),
        ("P404_SAME_ROUTE_RESCUE_CLOSED", same_route_closed, metric_value(phase403, "phase403_same_route_rescue_allowed", ""), 0),
        ("P404_EVENT_FEATURE_INPUT_PRESENT", ready > 0, ready, ">0"),
        ("P404_REQUIRED_COLUMNS_PRESENT", columns_present == 1, columns_present, 1),
        ("P404_NOT_REVERSAL_OR_PASSIVE_RESCUE", "not_reversal_not_passive_rescue" in ";".join(contract["contract_value"].astype(str)), "liquidity_vacuum_continuation", "material_new"),
        ("P404_FULL_DEPTH_L2_L5_REQUIRED", any(contract["contract_id"].astype(str).eq("l2_l5_alignment")), "l2_l5_alignment", "present"),
        ("P404_FIXED_THRESHOLDS_NO_SEARCH", True, "fixed_thresholds", "no_grid_search"),
        ("P404_COST200_FIXED_CAPITAL", COST_MULTIPLIER == 2.0 and INITIAL_CAPITAL_INR > 0 and FIXED_NOTIONAL_INR <= 100000.0, f"cost={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR};notional={FIXED_NOTIONAL_INR}", "cost200_fixed_capital"),
        ("P404_BOUNDARIES_CLOSED", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(contract: pd.DataFrame, inputs: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    next_action = NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION
    return pd.DataFrame(
        [
            ("phase404_liquidity_vacuum_continuation_precommit_complete", 1, "Phase404 precommit completed"),
            ("phase404_thesis_id", THESIS_ID, "Frozen thesis"),
            ("phase404_material_new_vs_phase403", 1, "Continuation/liquidity-vacuum thesis, not same reversal/passive rescue"),
            ("phase404_contract_rows", len(contract), "Contract rows"),
            ("phase404_phase401_ready_event_feature_rows", inputs.loc[inputs["input_id"].eq("phase401_ready_event_feature_rows"), "value"].iloc[0], "Ready input rows"),
            ("phase404_min_abs_impulse_bps", MIN_ABS_IMPULSE_BPS, "Fixed threshold"),
            ("phase404_min_abs_top5_imbalance", MIN_ABS_TOP5_IMBALANCE, "Fixed threshold"),
            ("phase404_min_abs_l2_l5_imbalance", MIN_ABS_L2_L5_IMBALANCE, "Fixed threshold"),
            ("phase404_max_replenishment_ratio", MAX_REPLENISHMENT_RATIO, "Liquidity-vacuum threshold"),
            ("phase404_parameter_search_allowed", 0, "No search"),
            ("phase404_execution_allowed_next", int(hard_pass == hard_rows), "Whether Phase405 may run"),
            ("phase404_strategy_promotion_allowed", 0, "No promotion"),
            ("phase404_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase404_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase404_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase404_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase404_next_best_action", next_action, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, contract: pd.DataFrame, inputs: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase404 Liquidity-Vacuum Continuation Precommit",
        "",
        "Phase404 freezes a materially new full-depth L2 thesis after Phase403 closed the passive-aware directional rescue route.",
        "",
        "The thesis is continuation under a catalyst liquidity vacuum: trade with the impulse only when top-five and levels 2-5 depth align with that impulse and replenishment is weak.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Contract",
        "",
        _markdown_table(contract),
        "",
        "## Input Registry",
        "",
        _markdown_table(inputs),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "No promotion, paper/live acceptance, deployable profitability claim, or parameter search is opened.",
    ]
    (output_dir / "phase404_liquidity_vacuum_continuation_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase403_dir: Path = DEFAULT_PHASE403_DIR, phase401_dir: Path = DEFAULT_PHASE401_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase403 = read_csv(phase403_dir / "phase403_acceptance_summary.csv")
    events = read_csv(phase401_dir / "phase387_event_feature_ledger.csv")
    if phase403.empty or events.empty:
        raise FileNotFoundError("Phase404 requires Phase403 summary and Phase401 event feature ledger.")
    contract = build_contract()
    inputs = build_input_registry(phase403, events)
    gates = build_gate_evaluation(phase403, inputs, contract)
    acceptance = build_acceptance(contract, inputs, gates)
    contract.to_csv(output_dir / "phase404_frozen_thesis_contract.csv", index=False)
    inputs.to_csv(output_dir / "phase404_input_registry.csv", index=False)
    gates.to_csv(output_dir / "phase404_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase404_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, contract, inputs, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase404_liquidity_vacuum_continuation_precommit",
        **reproducibility_fields(
            artifact_id="phase404_liquidity_vacuum_continuation_precommit",
            generated_utc=generated_utc,
            inputs={
                "phase403_acceptance_summary": str(phase403_dir / "phase403_acceptance_summary.csv"),
                "phase401_event_feature_ledger": str(phase401_dir / "phase387_event_feature_ledger.csv"),
            },
            parameters={
                "thesis_id": THESIS_ID,
                "min_abs_impulse_bps": MIN_ABS_IMPULSE_BPS,
                "min_abs_top5_imbalance": MIN_ABS_TOP5_IMBALANCE,
                "min_abs_l2_l5_imbalance": MIN_ABS_L2_L5_IMBALANCE,
                "max_replenishment_ratio": MAX_REPLENISHMENT_RATIO,
                "next_action": NEXT_ACTION,
            },
            outputs={"acceptance_summary": str(output_dir / "phase404_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase401_event_feature_decision_delay_120s",
        ),
    }
    (output_dir / "phase404_liquidity_vacuum_continuation_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase404 liquidity-vacuum continuation precommit.")
    parser.add_argument("--phase403-dir", type=Path, default=DEFAULT_PHASE403_DIR)
    parser.add_argument("--phase401-dir", type=Path, default=DEFAULT_PHASE401_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase403_dir, args.phase401_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
