from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase432_geometry_consistent_full_depth_feature_sweep import NEXT_ACTION as PHASE432_NEXT_ACTION
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE432_DIR = Path("outputs/phase432")
DEFAULT_OUTPUT_DIR = Path("outputs/phase433")

VERDICT = "P433_GEOMETRY_CONSISTENT_FULL_DEPTH_SWEEP_REJECTED_NEGATIVE_SPARSE"
NEXT_ACTION = "pause_for_strategy_decision_report_or_precommit_material_new_non_threshold_source"
REPAIR_ACTION = "repair_phase433_interpretation_inputs"


def failed_gates(gates: pd.DataFrame) -> str:
    if gates.empty:
        return ""
    failed = gates.loc[gates["passed"].astype(str).str.lower().isin(["false", "0"])]
    return ";".join(failed["gate_id"].astype(str).tolist())


def build_decision(acceptance432: pd.DataFrame, gates432: pd.DataFrame, syn_summary: pd.DataFrame, real_summary: pd.DataFrame) -> pd.DataFrame:
    active = syn_summary[pd.to_numeric(syn_summary["completed_round_trips"], errors="coerce").fillna(0).gt(0)] if not syn_summary.empty else pd.DataFrame()
    real_active = real_summary[pd.to_numeric(real_summary["completed_round_trips"], errors="coerce").fillna(0).gt(0)] if not real_summary.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("selected_verdict", VERDICT, "After timing repair, the broader full-depth sweep produced active but sparse negative synthetic trades and no survivor.", "terminal_for_this_sweep"),
            ("phase432_next_action_matched", PHASE432_NEXT_ACTION, "Phase433 implements the Phase432 next-action string.", "basis"),
            ("synthetic_grid_rows", metric_value(acceptance432, "phase432_synthetic_grid_rows_evaluated", 0), "Synthetic grid rows evaluated.", "evidence"),
            ("active_synthetic_scenario_rows", len(active), "Scenarios with at least one synthetic trade.", "evidence"),
            ("best_active_scenario_id", metric_value(acceptance432, "phase432_best_scenario_id", ""), "Best active scenario after corrected ranking.", "failure"),
            ("best_active_family_id", metric_value(acceptance432, "phase432_best_family_id", ""), "Best active family.", "failure"),
            ("best_active_round_trips", metric_value(acceptance432, "phase432_best_completed_round_trips", 0), "Sparse versus event floor.", "failure"),
            ("best_active_trade_dates", metric_value(acceptance432, "phase432_best_trade_dates", 0), "Sparse versus date breadth.", "failure"),
            ("best_active_symbols", metric_value(acceptance432, "phase432_best_symbols", 0), "Sparse versus symbol breadth.", "failure"),
            ("best_active_net_pnl_inr", metric_value(acceptance432, "phase432_best_net_pnl_inr", 0), "Negative after cost200.", "failure"),
            ("best_active_annualized_return_pct", metric_value(acceptance432, "phase432_best_annualized_return_pct", 0), "Failed annualized floor.", "failure"),
            ("phase432_failed_hard_gates", failed_gates(gates432), "Explicit failed gate basis.", "basis"),
            ("real_anchor_active_scenario_rows", len(real_active), "Matching real-anchor rows had no active trades.", "real_anchor_gap"),
            ("strategy_promotion_allowed", 0, "No accepted survivor.", "closed"),
            ("paper_or_live_acceptance_allowed", 0, "No paper/live acceptance.", "closed"),
            ("deployable_profitability_claim_allowed", 0, "No deployable claim.", "closed"),
            ("same_threshold_family_tuning_allowed", 0, "Do not tune thresholds after seeing the negative sparse result.", "closed"),
            ("next_action", NEXT_ACTION, "Decide whether to pause or precommit a materially new non-threshold source.", "next"),
        ],
        columns=["decision_id", "decision_value", "evidence", "status"],
    )


def build_gates(acceptance432: pd.DataFrame, gates432: pd.DataFrame, decision: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(acceptance432, "phase432_geometry_consistent_full_depth_sweep_complete", 0))
    hard_rows = int(metric_value(acceptance432, "phase432_hard_gate_rows", 0))
    hard_pass = int(metric_value(acceptance432, "phase432_hard_gate_pass_rows", 0))
    trips = as_int(metric_value(acceptance432, "phase432_best_completed_round_trips", 0))
    ann = float(metric_value(acceptance432, "phase432_best_annualized_return_pct", 0))
    verdict = str(decision.loc[decision["decision_id"].eq("selected_verdict"), "decision_value"].iloc[0])
    gates = [
        ("P433_PHASE432_COMPLETE", complete == 1, complete, 1),
        ("P433_PHASE432_GATES_EVALUATED", hard_rows == 17, hard_rows, 17),
        ("P433_PHASE432_FAILED_GATES_PRESENT", hard_pass < hard_rows and failed_gates(gates432) != "", f"passed={hard_pass}/{hard_rows};failed={failed_gates(gates432)}", "failed_gates_nonempty"),
        ("P433_ACTIVE_BUT_SPARSE_RESULT_RECORDED", trips > 0 and trips < 30, trips, "0<trips<30"),
        ("P433_NEGATIVE_COST200_CONFIRMED", ann < 0, ann, "<0"),
        ("P433_VERDICT_PRESENT", verdict == VERDICT, verdict, VERDICT),
        ("P433_NO_THRESHOLD_TUNING", str(decision.loc[decision["decision_id"].eq("same_threshold_family_tuning_allowed"), "decision_value"].iloc[0]) == "0", 0, 0),
        ("P433_BOUNDARIES_CLOSED", str(decision.loc[decision["decision_id"].eq("paper_or_live_acceptance_allowed"), "decision_value"].iloc[0]) == "0", "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(acceptance432: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("phase433_geometry_consistent_sweep_interpretation_complete", 1, "Phase433 interpretation completed"),
            ("phase433_selected_verdict", VERDICT, "Selected verdict"),
            ("phase433_phase432_best_completed_round_trips", metric_value(acceptance432, "phase432_best_completed_round_trips", 0), "Phase432 best active round trips"),
            ("phase433_phase432_best_annualized_return_pct", metric_value(acceptance432, "phase432_best_annualized_return_pct", 0), "Phase432 best active annualized return"),
            ("phase433_phase432_active_synthetic_scenario_rows", metric_value(acceptance432, "phase432_active_synthetic_scenario_rows", 0), "Phase432 active scenario rows"),
            ("phase433_strategy_promotion_allowed", 0, "No promotion"),
            ("phase433_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase433_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase433_same_threshold_family_tuning_allowed", 0, "No threshold tuning"),
            ("phase433_hard_gate_pass_rows", int(gates["passed"].astype(bool).sum()), "Passed hard gates"),
            ("phase433_hard_gate_rows", len(gates), "Hard gates"),
            ("phase433_next_best_action", NEXT_ACTION if int(gates["passed"].astype(bool).sum()) == len(gates) else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, decision: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase433 Geometry-Consistent Sweep Interpretation",
        "",
        "Phase433 interprets Phase432 as a real negative result after repairing timing geometry.",
        "",
        "The broader full-depth feature sweep produced active synthetic trades, but the best active scenario was sparse and negative after Zerodha cost200. No strategy acceptance or paper/live boundary is opened.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Decision Ledger",
        "",
        _markdown_table(decision),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: do not tune the same threshold-family sweep after seeing this result.",
    ]
    (output_dir / "phase433_geometry_consistent_sweep_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase432_dir: Path = DEFAULT_PHASE432_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    acceptance432 = read_csv(phase432_dir / "phase432_acceptance_summary.csv")
    gates432 = read_csv(phase432_dir / "phase432_gate_evaluation.csv")
    syn_summary = read_csv(phase432_dir / "phase432_synthetic_scenario_summary.csv")
    real_summary = read_csv(phase432_dir / "phase432_real_anchor_scenario_summary.csv")
    if acceptance432.empty or gates432.empty or syn_summary.empty or real_summary.empty:
        raise FileNotFoundError("Phase433 requires Phase432 acceptance, gates and scenario summaries.")
    decision = build_decision(acceptance432, gates432, syn_summary, real_summary)
    gates = build_gates(acceptance432, gates432, decision)
    acceptance = build_acceptance(acceptance432, gates)
    decision.to_csv(output_dir / "phase433_decision_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase433_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase433_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, decision, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase433_geometry_consistent_sweep_interpretation",
        **reproducibility_fields(
            artifact_id="phase433_geometry_consistent_sweep_interpretation",
            generated_utc=generated_utc,
            inputs={"phase432_acceptance_summary": str(phase432_dir / "phase432_acceptance_summary.csv")},
            parameters={"selected_verdict": VERDICT, "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase433_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase431_geometry_consistent_exact_tick",
        ),
    }
    (output_dir / "phase433_geometry_consistent_sweep_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase433 geometry-consistent sweep interpretation.")
    parser.add_argument("--phase432-dir", type=Path, default=DEFAULT_PHASE432_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase432_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
