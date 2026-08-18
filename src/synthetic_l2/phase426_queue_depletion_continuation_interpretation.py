from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase425_queue_depletion_continuation_execution import NEXT_ACTION as PHASE425_NEXT_ACTION
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE425_DIR = Path("outputs/phase425")
DEFAULT_OUTPUT_DIR = Path("outputs/phase426")

VERDICT = "P426_QUEUE_DEPLETION_CONTINUATION_REJECTED_ZERO_SYNTHETIC_EVENTS"
NEXT_ACTION = "precommit_broader_full_depth_feature_family_sweep_or_pause_for_decision_report"
REPAIR_ACTION = "repair_phase426_interpretation_inputs"


def failed_gates(gates: pd.DataFrame) -> str:
    if gates.empty:
        return ""
    failed = gates.loc[gates["passed"].astype(str).str.lower().isin(["false", "0"])]
    return ";".join(failed["gate_id"].astype(str).tolist())


def scenario_value(summary: pd.DataFrame, scenario_id: str, column: str, default: object = "") -> object:
    if summary.empty or "scenario_id" not in summary.columns:
        return default
    row = summary[summary["scenario_id"].astype(str).eq(scenario_id)]
    return row[column].iloc[0] if not row.empty and column in summary.columns else default


def build_decision(acceptance425: pd.DataFrame, gates425: pd.DataFrame, synthetic: pd.DataFrame, real_anchor: pd.DataFrame, syn_diag: pd.DataFrame) -> pd.DataFrame:
    scan_points = int(pd.to_numeric(syn_diag.get("candidate_scan_points", pd.Series(dtype=float)), errors="coerce").fillna(0).sum())
    selected = int(pd.to_numeric(syn_diag.get("selected_trades", pd.Series(dtype=float)), errors="coerce").fillna(0).sum())
    real_trades = int(scenario_value(real_anchor, "P425_PRIMARY_QUEUE_DEPLETION_CONTINUATION", "completed_round_trips", 0))
    real_dates = int(scenario_value(real_anchor, "P425_PRIMARY_QUEUE_DEPLETION_CONTINUATION", "trade_dates", 0))
    real_symbols = int(scenario_value(real_anchor, "P425_PRIMARY_QUEUE_DEPLETION_CONTINUATION", "symbols", 0))
    real_net = float(scenario_value(real_anchor, "P425_PRIMARY_QUEUE_DEPLETION_CONTINUATION", "net_pnl_inr", 0))
    real_ann = float(scenario_value(real_anchor, "P425_PRIMARY_QUEUE_DEPLETION_CONTINUATION", "annualized_return_pct", 0))
    return pd.DataFrame(
        [
            ("selected_verdict", VERDICT, "Frozen queue-depletion continuation route produced zero synthetic primary events and negative real-anchor evidence.", "terminal_for_this_route"),
            ("phase425_next_action_matched", PHASE425_NEXT_ACTION, "Phase426 implements the Phase425 next-action string.", "basis"),
            ("synthetic_candidate_scan_points", scan_points, "Bounded synthetic scan breadth.", "evidence"),
            ("synthetic_selected_trades_all_scenarios", selected, "No synthetic scenarios selected trades under frozen thresholds.", "failure"),
            ("synthetic_primary_completed_round_trips", metric_value(acceptance425, "phase425_primary_completed_round_trips", 0), "Primary frozen route event count.", "failure"),
            ("synthetic_primary_annualized_return_pct", metric_value(acceptance425, "phase425_primary_annualized_return_pct", 0), "Fixed-capital annualized return.", "failure"),
            ("phase425_failed_hard_gates", failed_gates(gates425), "Explicit failed gate basis.", "basis"),
            ("real_anchor_primary_completed_round_trips", real_trades, "Real-anchor route had sparse activity.", "real_anchor_negative"),
            ("real_anchor_primary_trade_dates", real_dates, "Real-anchor date breadth.", "real_anchor_negative"),
            ("real_anchor_primary_symbols", real_symbols, "Real-anchor symbol breadth.", "real_anchor_negative"),
            ("real_anchor_primary_net_pnl_inr", real_net, "Real-anchor cost200 net P&L.", "real_anchor_negative"),
            ("real_anchor_primary_annualized_return_pct", real_ann, "Real-anchor fixed-capital annualized return.", "real_anchor_negative"),
            ("exact_forward_tick_executor_preserved", 1, "Phase425 fixed the Phase422 proxy-only tick-gate weakness.", "preserve"),
            ("same_family_tuning_allowed", 0, "Do not rescue the frozen queue-depletion thresholds after seeing zero-event result.", "closed"),
            ("strategy_promotion_allowed", 0, "No accepted survivor.", "closed"),
            ("paper_or_live_acceptance_allowed", 0, "No paper/live acceptance.", "closed"),
            ("deployable_profitability_claim_allowed", 0, "No deployable claim.", "closed"),
            ("next_action", NEXT_ACTION, "Use a broader precommitted feature-family sweep if continuing strategy search.", "next"),
        ],
        columns=["decision_id", "decision_value", "evidence", "status"],
    )


def build_durable_byproducts() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("exact_forward_tick_indexing", "Reusable executor pattern requiring exact post-entry tick index plus elapsed-time hold.", "preserve"),
            ("queue_depletion_feature_functions", "Reusable L2-L5 depth depletion, order-count thinning and replenishment feature functions.", "preserve"),
            ("l1_only_control_pattern", "Depth-removal control is implemented as a first-class scenario.", "preserve"),
            ("real_anchor_single_name_loader", "Local real L2 replay path works for single-name full-depth tests.", "preserve"),
            ("frozen_threshold_route", "The specific Phase424 thresholds are not accepted and should not be rescued by post-result tuning.", "close"),
        ],
        columns=["artifact_id", "description", "status"],
    )


def build_gates(acceptance425: pd.DataFrame, gates425: pd.DataFrame, decision: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(acceptance425, "phase425_queue_depletion_continuation_execution_complete", 0))
    hard_rows = int(metric_value(acceptance425, "phase425_hard_gate_rows", 0))
    hard_pass = int(metric_value(acceptance425, "phase425_hard_gate_pass_rows", 0))
    trips = as_int(metric_value(acceptance425, "phase425_primary_completed_round_trips", 0))
    ann = float(metric_value(acceptance425, "phase425_primary_annualized_return_pct", 0))
    verdict = str(decision.loc[decision["decision_id"].eq("selected_verdict"), "decision_value"].iloc[0])
    gates = [
        ("P426_PHASE425_COMPLETE", complete == 1, complete, 1),
        ("P426_PHASE425_GATES_EVALUATED", hard_rows == 19, hard_rows, 19),
        ("P426_PHASE425_FAILED_GATES_PRESENT", hard_pass < hard_rows and failed_gates(gates425) != "", f"passed={hard_pass}/{hard_rows};failed={failed_gates(gates425)}", "failed_gates_nonempty"),
        ("P426_ZERO_SYNTHETIC_EVENT_FAILURE_RECORDED", trips == 0 and ann == 0.0, f"trips={trips};annualized={ann}", "zero_events_and_zero_return"),
        ("P426_REAL_ANCHOR_NEGATIVE_RECORDED", float(decision.loc[decision["decision_id"].eq("real_anchor_primary_annualized_return_pct"), "decision_value"].iloc[0]) < 0, decision.loc[decision["decision_id"].eq("real_anchor_primary_annualized_return_pct"), "decision_value"].iloc[0], "<0"),
        ("P426_EXACT_FORWARD_TICK_BYPRODUCT_PRESERVED", str(decision.loc[decision["decision_id"].eq("exact_forward_tick_executor_preserved"), "decision_value"].iloc[0]) == "1", 1, 1),
        ("P426_VERDICT_PRESENT", verdict == VERDICT, verdict, VERDICT),
        ("P426_NO_SAME_FAMILY_TUNING", str(decision.loc[decision["decision_id"].eq("same_family_tuning_allowed"), "decision_value"].iloc[0]) == "0", 0, 0),
        ("P426_BOUNDARIES_CLOSED", str(decision.loc[decision["decision_id"].eq("paper_or_live_acceptance_allowed"), "decision_value"].iloc[0]) == "0", "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(acceptance425: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase426_queue_depletion_continuation_interpretation_complete", 1, "Phase426 interpretation completed"),
            ("phase426_selected_verdict", VERDICT, "Selected verdict"),
            ("phase426_phase425_primary_completed_round_trips", metric_value(acceptance425, "phase425_primary_completed_round_trips", 0), "Phase425 synthetic primary round trips"),
            ("phase426_phase425_primary_annualized_return_pct", metric_value(acceptance425, "phase425_primary_annualized_return_pct", 0), "Phase425 synthetic primary annualized return"),
            ("phase426_phase425_hard_gate_pass_rows", metric_value(acceptance425, "phase425_hard_gate_pass_rows", 0), "Phase425 hard gates passed"),
            ("phase426_phase425_hard_gate_rows", metric_value(acceptance425, "phase425_hard_gate_rows", 0), "Phase425 hard gates"),
            ("phase426_queue_depletion_route_preserved", 0, "Frozen route closed for acceptance"),
            ("phase426_same_family_tuning_allowed", 0, "No same-family tuning"),
            ("phase426_strategy_promotion_allowed", 0, "No promotion"),
            ("phase426_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase426_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase426_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase426_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase426_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, decision: pd.DataFrame, byproducts: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase426 Queue-Depletion Continuation Interpretation",
        "",
        "Phase426 formally interprets Phase425: the frozen queue-depletion continuation route is rejected for acceptance.",
        "",
        "The signal selected zero synthetic trades in the bounded dense L1-L5 scan. Real-anchor replay had sparse activity but was negative after Zerodha cost200. The valuable reusable outcome is the exact forward-tick execution machinery, not the Phase424 threshold route.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Decision Ledger",
        "",
        _markdown_table(decision),
        "",
        "## Durable Byproducts",
        "",
        _markdown_table(byproducts),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: do not tune the frozen queue-depletion thresholds after this result. Continue only with a broader precommitted full-depth feature-family sweep or pause for a decision report.",
    ]
    (output_dir / "phase426_queue_depletion_continuation_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase425_dir: Path = DEFAULT_PHASE425_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    acceptance425 = read_csv(phase425_dir / "phase425_acceptance_summary.csv")
    gates425 = read_csv(phase425_dir / "phase425_gate_evaluation.csv")
    synthetic = read_csv(phase425_dir / "phase425_synthetic_scenario_summary.csv")
    real_anchor = read_csv(phase425_dir / "phase425_real_anchor_scenario_summary.csv")
    syn_diag = read_csv(phase425_dir / "phase425_synthetic_scan_diagnostics.csv")
    if acceptance425.empty or gates425.empty or synthetic.empty or real_anchor.empty or syn_diag.empty:
        raise FileNotFoundError("Phase426 requires Phase425 acceptance, gates, summaries and synthetic diagnostics.")
    decision = build_decision(acceptance425, gates425, synthetic, real_anchor, syn_diag)
    byproducts = build_durable_byproducts()
    gates = build_gates(acceptance425, gates425, decision)
    acceptance = build_acceptance(acceptance425, gates)
    decision.to_csv(output_dir / "phase426_decision_ledger.csv", index=False)
    byproducts.to_csv(output_dir / "phase426_durable_byproducts.csv", index=False)
    gates.to_csv(output_dir / "phase426_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase426_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, decision, byproducts, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase426_queue_depletion_continuation_interpretation",
        **reproducibility_fields(
            artifact_id="phase426_queue_depletion_continuation_interpretation",
            generated_utc=generated_utc,
            inputs={
                "phase425_acceptance_summary": str(phase425_dir / "phase425_acceptance_summary.csv"),
                "phase425_gate_evaluation": str(phase425_dir / "phase425_gate_evaluation.csv"),
                "phase425_synthetic_scenario_summary": str(phase425_dir / "phase425_synthetic_scenario_summary.csv"),
                "phase425_real_anchor_scenario_summary": str(phase425_dir / "phase425_real_anchor_scenario_summary.csv"),
            },
            parameters={"selected_verdict": VERDICT, "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase426_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase425_exact_forward_tick_indexing",
        ),
    }
    (output_dir / "phase426_queue_depletion_continuation_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase426 queue-depletion continuation interpretation.")
    parser.add_argument("--phase425-dir", type=Path, default=DEFAULT_PHASE425_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase425_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
