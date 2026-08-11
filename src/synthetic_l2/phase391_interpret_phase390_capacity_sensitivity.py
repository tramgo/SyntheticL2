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

DEFAULT_PHASE390_DIR = Path("outputs/phase390")
DEFAULT_OUTPUT_DIR = Path("outputs/phase391")
EVENT_FLOOR = 30


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def write_outputs(phase390_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    summary390 = read_csv(phase390_dir / "phase390_acceptance_summary.csv")
    scenarios = read_csv(phase390_dir / "phase390_capacity_scenario_summary.csv")
    if summary390.empty or scenarios.empty:
        raise FileNotFoundError("Phase391 requires Phase390 outputs")
    scenarios = scenarios.copy()
    scenarios["capacity"] = scenarios["capacity"].astype(int)
    scenarios["capacity_selected_trade_rows"] = scenarios["capacity_selected_trade_rows"].astype(int)
    scenarios["annualized_return_pct_capital_adjusted"] = scenarios["annualized_return_pct_capital_adjusted"].astype(float)
    best = scenarios.sort_values(["capacity_selected_trade_rows", "annualized_return_pct_capital_adjusted"], ascending=[False, False]).iloc[0]
    all_profitable = int(scenarios["above12"].astype(int).eq(1).all())
    any_accept_shape = int(scenarios["sensitivity_acceptance_shape"].astype(int).eq(1).any())
    decision = pd.DataFrame([
        {"decision_id": "P391_CAPACITY_SENSITIVITY_PROFITABLE", "value": all_profitable, "evidence": "all capacity ladder rows remain above 12% annualized after capital adjustment", "decision": "Capacity sensitivity does not kill the economics."},
        {"decision_id": "P391_CAPACITY_FLOOR_STILL_FAILS", "value": int(any_accept_shape == 0), "evidence": f"best_capacity={int(best['capacity'])}; best_selected={int(best['capacity_selected_trade_rows'])}; required={EVENT_FLOOR}", "decision": "Even capacity 4 does not reach the 30 selected-trade floor."},
        {"decision_id": "P391_NO_PROMOTION_FROM_SENSITIVITY", "value": 1, "evidence": "sensitivity_acceptance_shape rows are zero and promotion_allowed is zero", "decision": "No promotion, paper/live action, or deployable profitability claim."},
    ])
    gates = pd.DataFrame([
        ("P391_PHASE390_COMPLETE", int(str(summary390.loc[summary390["metric"].eq("phase390_capacity_rule_sensitivity_complete"), "value"].iloc[0]) == "1"), "Phase390 complete"),
        ("P391_LADDER_INTERPRETED", int(len(scenarios) == 3), f"rows={len(scenarios)}"),
        ("P391_NO_ACCEPTANCE_FROM_SENSITIVITY", int(any_accept_shape == 0), f"accept_shape_rows={int(scenarios['sensitivity_acceptance_shape'].astype(int).sum())}"),
        ("P391_NO_PROMOTION_PAPER_LIVE", 1, "closed"),
    ], columns=["gate_id", "passed", "evidence"])
    summary = pd.DataFrame([
        ("phase391_interpret_phase390_capacity_sensitivity_complete", int(gates["passed"].astype(int).all()), "Phase391 complete"),
        ("phase391_best_capacity", int(best["capacity"]), "Best capacity by selected trades"),
        ("phase391_best_capacity_selected_trade_rows", int(best["capacity_selected_trade_rows"]), "Best selected trades"),
        ("phase391_best_capacity_gap", max(0, EVENT_FLOOR - int(best["capacity_selected_trade_rows"])), "Gap to event floor"),
        ("phase391_best_annualized_return_pct_capital_adjusted", float(best["annualized_return_pct_capital_adjusted"]), "Best annualized return"),
        ("phase391_all_capacity_rows_profitable", all_profitable, "All capacities above 12%"),
        ("phase391_any_sensitivity_acceptance_shape", any_accept_shape, "Any sensitivity row passes shape gates"),
        ("phase391_strategy_promotion_allowed", 0, "No promotion"),
        ("phase391_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase391_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase391_next_best_action", "add_more_real_l2_days_or_precommit_event_deduplication_policy_no_paper_live", "Recommended next action"),
    ], columns=["metric", "value", "description"])
    outputs = {
        "summary": output_dir / "phase391_acceptance_summary.csv",
        "decision": output_dir / "phase391_decision_ledger.csv",
        "gates": output_dir / "phase391_gate_evaluation.csv",
        "report": output_dir / "phase391_interpret_phase390_capacity_sensitivity_report.md",
        "manifest": output_dir / "phase391_interpret_phase390_capacity_sensitivity_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    decision.to_csv(outputs["decision"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    outputs["report"].write_text("\n".join(["# Phase391 Interpret Phase390 Capacity Sensitivity", "", f"Generated: {generated_utc}", "", _markdown_table(summary), "", _markdown_table(decision), ""]), encoding="utf-8")
    outputs["manifest"].write_text(json.dumps({"phase": 391, "generated_at_utc": generated_utc, "outputs": {k: str(v) for k, v in outputs.items()}, "reproducibility": reproducibility_fields(artifact_id="phase391_interpret_phase390_capacity_sensitivity", generated_utc=generated_utc, inputs={"phase390_scenarios": str(phase390_dir / "phase390_capacity_scenario_summary.csv")}, parameters={"event_floor": EVENT_FLOOR}, outputs={k: str(v) for k, v in outputs.items()}, cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION)}, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase390-dir", type=Path, default=DEFAULT_PHASE390_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    print(json.dumps({k: str(v) for k, v in write_outputs(args.phase390_dir, args.output_dir).items()}, indent=2))
