from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase428_broader_full_depth_feature_family_sweep import NEXT_ACTION as PHASE428_NEXT_ACTION
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE428_DIR = Path("outputs/phase428")
DEFAULT_OUTPUT_DIR = Path("outputs/phase429")

VERDICT = "P429_BROADER_FULL_DEPTH_SWEEP_BLOCKED_BY_TIMING_GEOMETRY"
NEXT_ACTION = "precommit_phase430_timing_geometry_audit_before_new_strategy_sweep"
REPAIR_ACTION = "repair_phase429_interpretation_inputs"


def failed_gates(gates: pd.DataFrame) -> str:
    if gates.empty:
        return ""
    failed = gates.loc[gates["passed"].astype(str).str.lower().isin(["false", "0"])]
    return ";".join(failed["gate_id"].astype(str).tolist())


def build_decision(acceptance428: pd.DataFrame, gates428: pd.DataFrame, diag: pd.DataFrame) -> pd.DataFrame:
    scan_points = int(pd.to_numeric(diag.get("candidate_scan_points", pd.Series(dtype=float)), errors="coerce").fillna(0).sum())
    selected = int(pd.to_numeric(diag.get("selected_trades", pd.Series(dtype=float)), errors="coerce").fillna(0).sum())
    empty_reason = ""
    if "empty_reason" in diag.columns:
        reasons = sorted(set(diag["empty_reason"].dropna().astype(str)))
        empty_reason = ";".join(reasons)
    return pd.DataFrame(
        [
            ("selected_verdict", VERDICT, "Phase428 completed but produced zero candidate scan points under the frozen exact-tick plus 250 ms hold geometry.", "blocked_for_strategy_conclusion"),
            ("phase428_next_action_matched", PHASE428_NEXT_ACTION, "Phase429 implements the Phase428 next-action string.", "basis"),
            ("phase428_grid_rows_evaluated", metric_value(acceptance428, "phase428_grid_rows_evaluated", 0), "Frozen grid rows were evaluated.", "evidence"),
            ("synthetic_candidate_scan_points", scan_points, "No synthetic scan point satisfied exit geometry.", "timing_geometry_failure"),
            ("synthetic_selected_trades", selected, "No synthetic trades selected.", "timing_geometry_failure"),
            ("phase428_best_scenario_id", metric_value(acceptance428, "phase428_best_scenario_id", ""), "Best row is arbitrary among zero-return rows.", "diagnostic"),
            ("phase428_best_annualized_return_pct", metric_value(acceptance428, "phase428_best_annualized_return_pct", 0), "Zero return due to zero events.", "failure"),
            ("phase428_failed_hard_gates", failed_gates(gates428), "Explicit failed gate basis.", "basis"),
            ("empty_scan_reason", empty_reason, "Recorded empty-scan reason.", "timing_geometry_failure"),
            ("strategy_signal_conclusion_allowed", 0, "Zero scan points means this is not a discriminating feature-signal result.", "closed"),
            ("timing_geometry_audit_required", 1, "Need to audit timestamp units, tick cadence, max-hold ticks and min-hold ms before new sweeps.", "next"),
            ("strategy_promotion_allowed", 0, "No accepted survivor.", "closed"),
            ("paper_or_live_acceptance_allowed", 0, "No paper/live acceptance.", "closed"),
            ("deployable_profitability_claim_allowed", 0, "No deployable claim.", "closed"),
            ("next_action", NEXT_ACTION, "Precommit timing-geometry audit before another strategy sweep.", "next"),
        ],
        columns=["decision_id", "decision_value", "evidence", "status"],
    )


def build_required_audit() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("timestamp_unit_audit", "Compare exchange_timestamp_ms deltas for synthetic and real L2 panels and detect ms/second/nanosecond semantics.", "required"),
            ("hold_window_feasibility", "For each forward-tick bucket, estimate whether the max-hold window can satisfy the minimum elapsed hold.", "required"),
            ("synthetic_real_cadence_alignment", "Report median/p90/p95 tick gaps separately for synthetic and real-anchor data.", "required"),
            ("parameter_geometry_repair", "If needed, precommit a geometry-consistent max-hold/elapsed-hold grid before strategy execution.", "required"),
            ("no_signal_tuning", "Do not alter feature thresholds while repairing execution geometry.", "closed_boundary"),
        ],
        columns=["audit_id", "requirement", "status"],
    )


def build_gates(acceptance428: pd.DataFrame, gates428: pd.DataFrame, decision: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(acceptance428, "phase428_broader_full_depth_feature_family_sweep_complete", 0))
    grid_rows = as_int(metric_value(acceptance428, "phase428_grid_rows_evaluated", 0))
    scan_points = as_int(decision.loc[decision["decision_id"].eq("synthetic_candidate_scan_points"), "decision_value"].iloc[0])
    verdict = str(decision.loc[decision["decision_id"].eq("selected_verdict"), "decision_value"].iloc[0])
    gates = [
        ("P429_PHASE428_COMPLETE", complete == 1, complete, 1),
        ("P429_PHASE428_GRID_EVALUATED", grid_rows == 1458, grid_rows, 1458),
        ("P429_PHASE428_FAILED_GATES_PRESENT", failed_gates(gates428) != "", failed_gates(gates428), "nonempty"),
        ("P429_ZERO_SCAN_GEOMETRY_RECORDED", scan_points == 0, scan_points, 0),
        ("P429_SIGNAL_CONCLUSION_BLOCKED", str(decision.loc[decision["decision_id"].eq("strategy_signal_conclusion_allowed"), "decision_value"].iloc[0]) == "0", 0, 0),
        ("P429_TIMING_AUDIT_REQUIRED", str(decision.loc[decision["decision_id"].eq("timing_geometry_audit_required"), "decision_value"].iloc[0]) == "1", 1, 1),
        ("P429_VERDICT_PRESENT", verdict == VERDICT, verdict, VERDICT),
        ("P429_BOUNDARIES_CLOSED", str(decision.loc[decision["decision_id"].eq("paper_or_live_acceptance_allowed"), "decision_value"].iloc[0]) == "0", "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(acceptance428: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase429_broader_full_depth_sweep_interpretation_complete", 1, "Phase429 interpretation completed"),
            ("phase429_selected_verdict", VERDICT, "Selected verdict"),
            ("phase429_phase428_grid_rows_evaluated", metric_value(acceptance428, "phase428_grid_rows_evaluated", 0), "Phase428 grid rows"),
            ("phase429_phase428_best_completed_round_trips", metric_value(acceptance428, "phase428_best_completed_round_trips", 0), "Phase428 best round trips"),
            ("phase429_phase428_best_annualized_return_pct", metric_value(acceptance428, "phase428_best_annualized_return_pct", 0), "Phase428 best annualized return"),
            ("phase429_strategy_signal_conclusion_allowed", 0, "Blocked by zero scan geometry"),
            ("phase429_timing_geometry_audit_required", 1, "Precommit Phase430 timing audit"),
            ("phase429_strategy_promotion_allowed", 0, "No promotion"),
            ("phase429_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase429_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase429_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase429_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase429_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, decision: pd.DataFrame, audit: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase429 Broader Full-Depth Sweep Interpretation",
        "",
        "Phase429 interprets Phase428 as a timing-geometry blockage, not as a profitable or unprofitable signal-family conclusion.",
        "",
        "The Phase428 executor evaluated the frozen grid but no synthetic scan point could satisfy the exact forward-tick plus elapsed-hold geometry on the bounded shard. The next useful work is a timing/cadence audit before any new strategy sweep.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Decision Ledger",
        "",
        _markdown_table(decision),
        "",
        "## Required Timing-Geometry Audit",
        "",
        _markdown_table(audit),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: no promotion, paper/live acceptance or deployable profitability claim is allowed.",
    ]
    (output_dir / "phase429_broader_full_depth_sweep_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase428_dir: Path = DEFAULT_PHASE428_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    acceptance428 = read_csv(phase428_dir / "phase428_acceptance_summary.csv")
    gates428 = read_csv(phase428_dir / "phase428_gate_evaluation.csv")
    diag = read_csv(phase428_dir / "phase428_synthetic_scan_diagnostics.csv")
    if acceptance428.empty or gates428.empty or diag.empty:
        raise FileNotFoundError("Phase429 requires Phase428 acceptance, gates and synthetic diagnostics.")
    decision = build_decision(acceptance428, gates428, diag)
    audit = build_required_audit()
    gates = build_gates(acceptance428, gates428, decision)
    acceptance = build_acceptance(acceptance428, gates)
    decision.to_csv(output_dir / "phase429_decision_ledger.csv", index=False)
    audit.to_csv(output_dir / "phase429_required_timing_geometry_audit.csv", index=False)
    gates.to_csv(output_dir / "phase429_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase429_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, decision, audit, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase429_broader_full_depth_sweep_interpretation",
        **reproducibility_fields(
            artifact_id="phase429_broader_full_depth_sweep_interpretation",
            generated_utc=generated_utc,
            inputs={
                "phase428_acceptance_summary": str(phase428_dir / "phase428_acceptance_summary.csv"),
                "phase428_gate_evaluation": str(phase428_dir / "phase428_gate_evaluation.csv"),
                "phase428_synthetic_scan_diagnostics": str(phase428_dir / "phase428_synthetic_scan_diagnostics.csv"),
            },
            parameters={"selected_verdict": VERDICT, "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase429_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase428_exact_forward_tick_grid",
        ),
    }
    (output_dir / "phase429_broader_full_depth_sweep_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase429 broader full-depth sweep interpretation.")
    parser.add_argument("--phase428-dir", type=Path, default=DEFAULT_PHASE428_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase428_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
