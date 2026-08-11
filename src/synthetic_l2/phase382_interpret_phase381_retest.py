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


DEFAULT_PHASE381_DIR = Path("outputs/phase381")
DEFAULT_OUTPUT_DIR = Path("outputs/phase382")
ANNUALIZED_THRESHOLD_PCT = 12.0
EVENT_FLOOR = 30


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    return rows.iloc[0] if not rows.empty else default


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def write_outputs(phase381_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    summary381 = read_csv(phase381_dir / "phase381_acceptance_summary.csv")
    scenarios = read_csv(phase381_dir / "phase381_scenario_summary.csv")
    interpretation381 = read_csv(phase381_dir / "phase381_interpretation_ledger.csv")
    if summary381.empty or scenarios.empty or interpretation381.empty:
        raise FileNotFoundError("Phase382 requires Phase381 retest outputs")

    primary_acceptance = as_int(metric_value(summary381, "phase381_primary_acceptance_candidate"))
    primary_ann = as_float(metric_value(summary381, "phase381_primary_annualized_return_pct"))
    selected_trades = as_int(metric_value(summary381, "phase381_primary_selected_trade_rows"))
    event_floor_met = as_int(metric_value(summary381, "phase381_primary_event_floor_met"))
    breadth_met = as_int(metric_value(summary381, "phase381_primary_breadth_met"))
    side_flip_ann = as_float(metric_value(summary381, "phase381_side_flip_annualized_return_pct"))
    annualized_pass = int(primary_ann > ANNUALIZED_THRESHOLD_PCT)
    side_flip_pass = int(primary_ann > side_flip_ann)
    sparse_gap = max(0, EVENT_FLOOR - selected_trades)

    decision = pd.DataFrame(
        [
            {
                "decision_id": "P382_PROFITABILITY_DIAGNOSTIC_POSITIVE",
                "value": annualized_pass,
                "evidence": f"primary_annualized_return_pct={primary_ann}; threshold={ANNUALIZED_THRESHOLD_PCT}",
                "decision": "The frozen primary remains economically positive after expanding real L2 evidence.",
            },
            {
                "decision_id": "P382_EVENT_FLOOR_FAILS",
                "value": int(event_floor_met == 0),
                "evidence": f"selected_trades={selected_trades}; required={EVENT_FLOOR}; gap={sparse_gap}",
                "decision": "The retest is still too sparse for acceptance.",
            },
            {
                "decision_id": "P382_BREADTH_PASSES",
                "value": breadth_met,
                "evidence": f"breadth_met={breadth_met}",
                "decision": "Breadth is not the blocker in this retest.",
            },
            {
                "decision_id": "P382_SIDE_FLIP_CONTROL_PASSES",
                "value": side_flip_pass,
                "evidence": f"primary_ann={primary_ann}; side_flip_ann={side_flip_ann}",
                "decision": "The reversal direction dominates the same-filter continuation control.",
            },
            {
                "decision_id": "P382_NO_ACCEPTANCE_OR_PROMOTION",
                "value": int(primary_acceptance == 0),
                "evidence": f"acceptance_candidate={primary_acceptance}",
                "decision": "Do not promote, paper trade, or claim deployable profitability.",
            },
        ]
    )
    gates = pd.DataFrame(
        [
            ("P382_PHASE381_COMPLETE", as_int(metric_value(summary381, "phase381_expanded_reversal_acceptance_retest_complete")), "Phase381 complete"),
            ("P382_PROFITABILITY_GATE_CHECKED", 1, f"ann={primary_ann:.3f}; pass={annualized_pass}"),
            ("P382_EVENT_FLOOR_GATE_CHECKED", 1, f"selected={selected_trades}; required={EVENT_FLOOR}; pass={event_floor_met}"),
            ("P382_BREADTH_GATE_CHECKED", 1, f"breadth={breadth_met}"),
            ("P382_CONTROL_GATE_CHECKED", 1, f"side_flip_ann={side_flip_ann:.3f}"),
            ("P382_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "closed"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )
    summary = pd.DataFrame(
        [
            ("phase382_interpret_phase381_retest_complete", int(gates["passed"].astype(int).all()), "Phase382 complete"),
            ("phase382_primary_annualized_return_pct", primary_ann, "Primary annualized return"),
            ("phase382_primary_selected_trade_rows", selected_trades, "Primary capacity-selected trades"),
            ("phase382_event_floor_required", EVENT_FLOOR, "Required selected trades"),
            ("phase382_event_floor_gap", sparse_gap, "Remaining selected-trade gap"),
            ("phase382_profitability_gate_met", annualized_pass, "Annualized return > 12%"),
            ("phase382_event_floor_met", event_floor_met, "Selected-trade floor met"),
            ("phase382_breadth_met", breadth_met, "Breadth met"),
            ("phase382_side_flip_control_passed", side_flip_pass, "Primary beats continuation control"),
            ("phase382_acceptance_candidate", primary_acceptance, "Acceptance candidate"),
            ("phase382_strategy_promotion_allowed", 0, "No promotion"),
            ("phase382_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase382_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase382_hard_gate_pass_rows", int(gates["passed"].astype(int).sum()), "Passed gates"),
            ("phase382_hard_gate_rows", len(gates), "Gates"),
            ("phase382_next_best_action", "precommit_event_density_repair_or_new_material_thesis_no_paper_live", "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )
    outputs = {
        "summary": output_dir / "phase382_acceptance_summary.csv",
        "decision": output_dir / "phase382_decision_ledger.csv",
        "gates": output_dir / "phase382_gate_evaluation.csv",
        "report": output_dir / "phase382_interpret_phase381_retest_report.md",
        "manifest": output_dir / "phase382_interpret_phase381_retest_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    decision.to_csv(outputs["decision"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    report = "\n".join([
        "# Phase382 Interpret Phase381 Retest",
        "",
        f"Generated: {generated_utc}",
        "",
        "Phase382 interprets the expanded real-L2 frozen reversal retest. The primary is profitable and beats the side-flip control, but it is not accepted because the actual capacity-selected event count remains below the 30-trade floor.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(summary),
        "",
        "## Decision ledger",
        "",
        _markdown_table(decision),
        "",
        "## Gate evaluation",
        "",
        _markdown_table(gates),
        "",
        "No promotion, paper/live acceptance, or deployable profitability claim is opened.",
    ])
    outputs["report"].write_text(report + "\n", encoding="utf-8")
    outputs["manifest"].write_text(json.dumps({
        "phase": 382,
        "generated_at_utc": generated_utc,
        "outputs": {k: str(v) for k, v in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase382_interpret_phase381_retest",
            generated_utc=generated_utc,
            inputs={"phase381_summary": str(phase381_dir / "phase381_acceptance_summary.csv"), "phase381_scenarios": str(phase381_dir / "phase381_scenario_summary.csv")},
            parameters={"annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT, "event_floor": EVENT_FLOOR},
            outputs={k: str(v) for k, v in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": "precommit_event_density_repair_or_new_material_thesis_no_paper_live",
    }, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase381-dir", type=Path, default=DEFAULT_PHASE381_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase381_dir, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))
