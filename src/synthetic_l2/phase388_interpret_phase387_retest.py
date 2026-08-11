from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION

DEFAULT_PHASE387_DIR = Path("outputs/phase387")
DEFAULT_OUTPUT_DIR = Path("outputs/phase388")
EVENT_FLOOR = 30
ANNUALIZED_THRESHOLD_PCT = 12.0


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    return rows.iloc[0] if not rows.empty else default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def write_outputs(phase387_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    summary387 = read_csv(phase387_dir / "phase387_acceptance_summary.csv")
    scenarios = read_csv(phase387_dir / "phase387_scenario_summary.csv")
    events = read_csv(phase387_dir / "phase387_event_feature_ledger.csv")
    if summary387.empty or scenarios.empty or events.empty:
        raise FileNotFoundError("Phase388 requires Phase387 outputs")
    primary_sched = int(scenarios.loc[scenarios["scenario_id"].astype(str).str.endswith("REVERSAL_CONTROL"), "scheduled_event_rows"].iloc[0])
    selected = as_int(metric_value(summary387, "phase387_primary_selected_trade_rows"))
    ann = as_float(metric_value(summary387, "phase387_primary_annualized_return_pct"))
    net = as_float(metric_value(summary387, "phase387_primary_net_pnl_inr"))
    event_floor = as_int(metric_value(summary387, "phase387_primary_event_floor_met"))
    breadth = as_int(metric_value(summary387, "phase387_primary_breadth_met"))
    acceptance = as_int(metric_value(summary387, "phase387_primary_acceptance_candidate"))
    side_ann = as_float(metric_value(summary387, "phase387_side_flip_annualized_return_pct"))
    no_start = int(events["status"].astype(str).eq("no_start_tick").sum())
    decision = pd.DataFrame([
        {"decision_id": "P388_PROFITABILITY_STILL_POSITIVE", "value": int(ann > ANNUALIZED_THRESHOLD_PCT), "evidence": f"ann={ann}; net={net}", "decision": "Frozen reversal remains profitable after the Phase384 density repair."},
        {"decision_id": "P388_RAW_CANDIDATE_FLOOR_REACHED", "value": int(primary_sched >= EVENT_FLOOR), "evidence": f"scheduled_candidates={primary_sched}; required={EVENT_FLOOR}", "decision": "Raw filtered candidates now reach the event floor."},
        {"decision_id": "P388_CAPACITY_SELECTED_FLOOR_FAILS", "value": int(event_floor == 0), "evidence": f"capacity_selected={selected}; required={EVENT_FLOOR}; gap={max(0, EVENT_FLOOR-selected)}", "decision": "Capacity selection remains the acceptance blocker."},
        {"decision_id": "P388_SHORT_DAY_EFFECT_RECORDED", "value": int(no_start > 0), "evidence": f"no_start_tick_rows={no_start}", "decision": "The short 2026-07-27 collector window produced some non-ready event rows."},
        {"decision_id": "P388_NO_ACCEPTANCE_OR_PROMOTION", "value": int(acceptance == 0), "evidence": f"acceptance_candidate={acceptance}; breadth={breadth}; side_flip_ann={side_ann}", "decision": "No promotion, paper/live action, or deployable profitability claim."},
    ])
    gates = pd.DataFrame([
        ("P388_PHASE387_COMPLETE", as_int(metric_value(summary387, "phase387_phase385_frozen_retest_complete")), "Phase387 complete"),
        ("P388_PROFITABILITY_GATE_CHECKED", 1, f"ann={ann:.3f}"),
        ("P388_RAW_AND_CAPACITY_EVENT_FLOORS_CHECKED", 1, f"raw={primary_sched}; selected={selected}"),
        ("P388_CONTROL_GATE_CHECKED", 1, f"side_flip_ann={side_ann:.3f}"),
        ("P388_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "closed"),
    ], columns=["gate_id", "passed", "evidence"])
    summary = pd.DataFrame([
        ("phase388_interpret_phase387_retest_complete", int(gates["passed"].astype(int).all()), "Phase388 complete"),
        ("phase388_primary_annualized_return_pct", ann, "Primary annualized return"),
        ("phase388_primary_net_pnl_inr", net, "Primary net PnL"),
        ("phase388_primary_scheduled_candidates", primary_sched, "Raw scheduled candidates"),
        ("phase388_primary_capacity_selected_trades", selected, "Capacity-selected trades"),
        ("phase388_capacity_selected_gap", max(0, EVENT_FLOOR - selected), "Capacity-selected gap"),
        ("phase388_no_start_tick_rows", no_start, "No-start rows"),
        ("phase388_event_floor_met", event_floor, "Selected-trade floor met"),
        ("phase388_breadth_met", breadth, "Breadth met"),
        ("phase388_acceptance_candidate", acceptance, "Acceptance candidate"),
        ("phase388_side_flip_annualized_return_pct", side_ann, "Side-flip annualized return"),
        ("phase388_strategy_promotion_allowed", 0, "No promotion"),
        ("phase388_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase388_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase388_next_best_action", "precommit_capacity_rule_sensitivity_or_add_more_real_l2_no_paper_live", "Recommended next action"),
    ], columns=["metric", "value", "description"])
    outputs = {
        "summary": output_dir / "phase388_acceptance_summary.csv",
        "decision": output_dir / "phase388_decision_ledger.csv",
        "gates": output_dir / "phase388_gate_evaluation.csv",
        "report": output_dir / "phase388_interpret_phase387_retest_report.md",
        "manifest": output_dir / "phase388_interpret_phase387_retest_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    decision.to_csv(outputs["decision"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    outputs["report"].write_text("\n".join(["# Phase388 Interpret Phase387 Retest", "", f"Generated: {generated_utc}", "", _markdown_table(summary), "", _markdown_table(decision), ""]), encoding="utf-8")
    outputs["manifest"].write_text(json.dumps({"phase": 388, "generated_at_utc": generated_utc, "outputs": {k: str(v) for k, v in outputs.items()}, "reproducibility": reproducibility_fields(artifact_id="phase388_interpret_phase387_retest", generated_utc=generated_utc, inputs={"phase387_summary": str(phase387_dir / "phase387_acceptance_summary.csv")}, parameters={"event_floor": EVENT_FLOOR}, outputs={k: str(v) for k, v in outputs.items()}, cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION)}, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase387-dir", type=Path, default=DEFAULT_PHASE387_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    print(json.dumps({k: str(v) for k, v in write_outputs(args.phase387_dir, args.output_dir).items()}, indent=2))
