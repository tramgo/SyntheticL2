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


DEFAULT_PHASE388_DIR = Path("outputs/phase388")
DEFAULT_OUTPUT_DIR = Path("outputs/phase389")
PRIMARY_SCENARIO_ID = "P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL"
CAPACITY_LADDER = "2;3;4"


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


def write_outputs(phase388_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase388 = read_csv(phase388_dir / "phase388_acceptance_summary.csv")
    if phase388.empty:
        raise FileNotFoundError("Phase389 requires Phase388 interpretation")
    selected = as_int(metric_value(phase388, "phase388_primary_capacity_selected_trades"))
    raw = as_int(metric_value(phase388, "phase388_primary_scheduled_candidates"))
    gap = as_int(metric_value(phase388, "phase388_capacity_selected_gap"))
    contract = pd.DataFrame([{
        "contract_id": "P389_CAPACITY_RULE_SENSITIVITY_PRECOMMIT",
        "source_phase": "Phase388",
        "frozen_primary_scenario_id": PRIMARY_SCENARIO_ID,
        "capacity_ladder": CAPACITY_LADDER,
        "baseline_capacity": 2,
        "baseline_capacity_selected_trades": selected,
        "raw_scheduled_candidates": raw,
        "selected_trade_gap": gap,
        "alpha_parameter_change_allowed": 0,
        "cost_model_change_allowed": 0,
        "depth_rule_change_allowed": 0,
        "capital_adjustment_required_for_capacity_gt_2": 1,
        "promotion_from_sensitivity_allowed": 0,
        "paper_live_or_profit_claim_allowed": 0,
    }])
    gates = pd.DataFrame([
        ("P389_PHASE388_PRESENT", as_int(metric_value(phase388, "phase388_interpret_phase387_retest_complete")), "Phase388 complete"),
        ("P389_CAPACITY_BOTTLENECK_PRESENT", int(gap > 0 and raw >= 30), f"raw={raw}; selected={selected}; gap={gap}"),
        ("P389_ALPHA_COST_DEPTH_FROZEN", 1, "capacity sensitivity only"),
        ("P389_CAPITAL_ADJUSTMENT_REQUIRED", 1, "annualized returns use max(250k, capacity*100k)"),
        ("P389_NO_PROMOTION_PAPER_LIVE", 1, "diagnostic_only"),
    ], columns=["gate_id", "passed", "evidence"])
    summary = pd.DataFrame([
        ("phase389_capacity_sensitivity_precommit_complete", int(gates["passed"].astype(int).all()), "Phase389 complete"),
        ("phase389_capacity_ladder", CAPACITY_LADDER, "Capacities to test"),
        ("phase389_baseline_capacity_selected_trades", selected, "Baseline selected trades"),
        ("phase389_raw_scheduled_candidates", raw, "Raw scheduled candidates"),
        ("phase389_selected_trade_gap", gap, "Selected-trade gap"),
        ("phase389_alpha_parameter_change_allowed", 0, "No alpha parameter changes"),
        ("phase389_promotion_from_sensitivity_allowed", 0, "No promotion from sensitivity"),
        ("phase389_next_best_action", "execute_phase390_capacity_rule_sensitivity_no_paper_live", "Recommended next action"),
    ], columns=["metric", "value", "description"])
    outputs = {
        "summary": output_dir / "phase389_acceptance_summary.csv",
        "contract": output_dir / "phase389_capacity_sensitivity_contract.csv",
        "gates": output_dir / "phase389_gate_evaluation.csv",
        "report": output_dir / "phase389_capacity_sensitivity_precommit_report.md",
        "manifest": output_dir / "phase389_capacity_sensitivity_precommit_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    contract.to_csv(outputs["contract"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    outputs["report"].write_text("\n".join(["# Phase389 Capacity Sensitivity Precommit", "", f"Generated: {generated_utc}", "", _markdown_table(summary), "", _markdown_table(contract), "", _markdown_table(gates), ""]), encoding="utf-8")
    outputs["manifest"].write_text(json.dumps({"phase": 389, "generated_at_utc": generated_utc, "outputs": {k: str(v) for k, v in outputs.items()}, "reproducibility": reproducibility_fields(artifact_id="phase389_capacity_sensitivity_precommit", generated_utc=generated_utc, inputs={"phase388_summary": str(phase388_dir / "phase388_acceptance_summary.csv")}, parameters={"capacity_ladder": CAPACITY_LADDER, "promotion_from_sensitivity_allowed": False}, outputs={k: str(v) for k, v in outputs.items()}, cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION)}, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase388-dir", type=Path, default=DEFAULT_PHASE388_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    print(json.dumps({k: str(v) for k, v in write_outputs(args.phase388_dir, args.output_dir).items()}, indent=2))
