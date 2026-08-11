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
from synthetic_l2.phase405_liquidity_vacuum_continuation_execution import DEPTH_REMOVED_SCENARIO_ID, PRIMARY_SCENARIO_ID, SIDE_FLIP_SCENARIO_ID
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE405_DIR = Path("outputs/phase405")
DEFAULT_OUTPUT_DIR = Path("outputs/phase406")

SELECTED_DECISION = "P406_LIQUIDITY_VACUUM_CONTINUATION_REJECTED"
NEXT_ACTION = "precommit_next_materially_new_l2_thesis_or_pause_strategy_search_no_paper_live"
REPAIR_ACTION = "repair_phase406_liquidity_vacuum_continuation_interpretation"
ANNUALIZED_THRESHOLD_PCT = 12.0
MIN_SELECTED_EVENT_ROWS = 30


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def scenario_row(scenarios: pd.DataFrame, scenario_id: str) -> pd.Series:
    rows = scenarios[scenarios["scenario_id"].astype(str).eq(scenario_id)] if not scenarios.empty else pd.DataFrame()
    return rows.iloc[0] if not rows.empty else pd.Series(dtype=object)


def build_decision_ledger(summary: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    primary = scenario_row(scenarios, PRIMARY_SCENARIO_ID)
    side = scenario_row(scenarios, SIDE_FLIP_SCENARIO_ID)
    depth_removed = scenario_row(scenarios, DEPTH_REMOVED_SCENARIO_ID)
    primary_ann = to_float(primary.get("annualized_return_pct", 0.0))
    primary_events = as_int(primary.get("capacity_selected_trade_rows", 0))
    primary_acceptance = as_int(primary.get("acceptance_candidate", 0))
    return pd.DataFrame(
        [
            ("selected_decision", SELECTED_DECISION, "Primary thesis is negative after cost200.", "reject"),
            ("primary_profitability", int(primary_ann > ANNUALIZED_THRESHOLD_PCT), f"annualized={primary_ann}", f">{ANNUALIZED_THRESHOLD_PCT}"),
            ("primary_event_floor", int(primary_events >= MIN_SELECTED_EVENT_ROWS), f"selected_events={primary_events}", f">={MIN_SELECTED_EVENT_ROWS}"),
            ("primary_acceptance", primary_acceptance, f"acceptance={primary_acceptance}", "0 means rejected"),
            ("side_flip_control", side.get("annualized_return_pct", 0), "Opposite side does not clear >12 either.", "diagnostic"),
            ("depth_removed_control", depth_removed.get("annualized_return_pct", 0), "Removing levels 2-5 does not rescue the idea.", "diagnostic"),
            ("same_threshold_rescue_allowed", 0, "Fixed-threshold first test failed; no parameter rescue opened.", "forbidden"),
            ("paper_live_or_profit_claim", 0, "promotion=0;paper=0;claim=0", "closed"),
            ("next_action", NEXT_ACTION, "Move only to materially new thesis, or pause strategy search.", "next"),
        ],
        columns=["decision_id", "decision_value", "evidence", "decision_status"],
    )


def build_gate_evaluation(summary: pd.DataFrame, scenarios: pd.DataFrame, decisions: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(summary, "phase405_liquidity_vacuum_continuation_execution_complete", 0))
    primary = scenario_row(scenarios, PRIMARY_SCENARIO_ID)
    primary_acceptance = as_int(primary.get("acceptance_candidate", 0))
    promotion = as_int(metric_value(summary, "phase405_strategy_promotion_allowed", 0))
    paper = as_int(metric_value(summary, "phase405_paper_or_live_acceptance_allowed", 0))
    claim = as_int(metric_value(summary, "phase405_deployable_profitability_claim_allowed", 0))
    gates = [
        ("P406_PHASE405_COMPLETE", complete == 1, complete, 1),
        ("P406_PRIMARY_SCENARIO_INTERPRETED", not primary.empty, int(not primary.empty), 1),
        ("P406_PRIMARY_REJECTED", primary_acceptance == 0, primary_acceptance, 0),
        ("P406_DECISION_REJECTS_BRANCH", str(decisions.loc[decisions["decision_id"].eq("selected_decision"), "decision_value"].iloc[0]) == SELECTED_DECISION, SELECTED_DECISION, SELECTED_DECISION),
        ("P406_NO_PARAMETER_RESCUE", str(decisions.loc[decisions["decision_id"].eq("same_threshold_rescue_allowed"), "decision_value"].iloc[0]) == "0", 0, 0),
        ("P406_BOUNDARIES_CLOSED", promotion == 0 and paper == 0 and claim == 0, f"promotion={promotion};paper={paper};claim={claim}", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(summary: pd.DataFrame, scenarios: pd.DataFrame, decisions: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    primary = scenario_row(scenarios, PRIMARY_SCENARIO_ID)
    side = scenario_row(scenarios, SIDE_FLIP_SCENARIO_ID)
    depth_removed = scenario_row(scenarios, DEPTH_REMOVED_SCENARIO_ID)
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase406_liquidity_vacuum_continuation_interpretation_complete", 1, "Phase406 interpretation completed"),
            ("phase406_selected_decision", SELECTED_DECISION, "Selected decision"),
            ("phase406_primary_raw_candidate_rows", primary.get("raw_candidate_rows", 0), "Primary raw candidates"),
            ("phase406_primary_capacity_selected_trade_rows", primary.get("capacity_selected_trade_rows", 0), "Primary selected trades"),
            ("phase406_primary_net_pnl_inr", primary.get("net_pnl_inr", 0), "Primary net PnL"),
            ("phase406_primary_annualized_return_pct", primary.get("annualized_return_pct", 0), "Primary annualized return"),
            ("phase406_primary_above12", primary.get("above12", 0), "Primary above 12%"),
            ("phase406_primary_event_floor_met", primary.get("event_floor_met", 0), "Primary event floor"),
            ("phase406_primary_breadth_met", primary.get("breadth_met", 0), "Primary breadth"),
            ("phase406_primary_acceptance_candidate", primary.get("acceptance_candidate", 0), "Primary acceptance"),
            ("phase406_side_flip_annualized_return_pct", side.get("annualized_return_pct", 0), "Side flip"),
            ("phase406_depth_removed_annualized_return_pct", depth_removed.get("annualized_return_pct", 0), "Depth removed"),
            ("phase406_same_threshold_rescue_allowed", 0, "No threshold rescue"),
            ("phase406_strategy_promotion_allowed", 0, "No promotion"),
            ("phase406_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase406_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase406_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase406_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase406_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, decisions: pd.DataFrame, gates: pd.DataFrame, scenarios: pd.DataFrame) -> None:
    lines = [
        "# Phase406 Liquidity-Vacuum Continuation Interpretation",
        "",
        "Phase406 interprets the Phase405 fixed-threshold material-new full-depth L2 thesis.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Decision Ledger",
        "",
        _markdown_table(decisions),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "## Scenario Summary",
        "",
        _markdown_table(scenarios),
        "",
        "No promotion, paper/live acceptance, deployable profitability claim, or same-threshold rescue is opened.",
    ]
    (output_dir / "phase406_liquidity_vacuum_continuation_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase405_dir: Path = DEFAULT_PHASE405_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    summary = read_csv(phase405_dir / "phase405_acceptance_summary.csv")
    scenarios = read_csv(phase405_dir / "phase405_scenario_summary.csv")
    if summary.empty or scenarios.empty:
        raise FileNotFoundError("Phase406 requires Phase405 summary and scenario summary.")
    decisions = build_decision_ledger(summary, scenarios)
    gates = build_gate_evaluation(summary, scenarios, decisions)
    acceptance = build_acceptance(summary, scenarios, decisions, gates)
    decisions.to_csv(output_dir / "phase406_decision_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase406_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase406_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, decisions, gates, scenarios)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase406_liquidity_vacuum_continuation_interpretation",
        **reproducibility_fields(
            artifact_id="phase406_liquidity_vacuum_continuation_interpretation",
            generated_utc=generated_utc,
            inputs={
                "phase405_acceptance_summary": str(phase405_dir / "phase405_acceptance_summary.csv"),
                "phase405_scenario_summary": str(phase405_dir / "phase405_scenario_summary.csv"),
            },
            parameters={"selected_decision": SELECTED_DECISION, "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase406_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_interpretation_only",
        ),
    }
    (output_dir / "phase406_liquidity_vacuum_continuation_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase406 liquidity-vacuum continuation interpretation.")
    parser.add_argument("--phase405-dir", type=Path, default=DEFAULT_PHASE405_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase405_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
