from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE418_DIR = Path("outputs/phase418")
DEFAULT_OUTPUT_DIR = Path("outputs/phase419")

VERDICT = "P419_PAIR_SPREAD_CONVERGENCE_POSITIVE_SYNTHETIC_LEAD_NOT_ACCEPTED"
NEXT_ACTION = "repair_full_depth_contribution_and_real_anchor_pair_evidence_before_any_promotion"
REPAIR_ACTION = "repair_phase419_pair_spread_interpretation"


def failed_gates(gates: pd.DataFrame) -> str:
    failed = gates.loc[gates["passed"].astype(str).str.lower().isin(["false", "0"])] if not gates.empty else pd.DataFrame()
    return ";".join(failed["gate_id"].astype(str).tolist())


def scenario_value(scenarios: pd.DataFrame, scenario_id: str, column: str, default: object = "") -> object:
    row = scenarios[scenarios["scenario_id"].astype(str).eq(scenario_id)] if not scenarios.empty and "scenario_id" in scenarios.columns else pd.DataFrame()
    return row[column].iloc[0] if not row.empty and column in row.columns else default


def build_decision(summary: pd.DataFrame, gates418: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    primary_ann = float(metric_value(summary, "phase418_primary_annualized_return_pct", 0))
    l2_removed_ann = float(scenario_value(scenarios, "P418_L2_L5_REMOVED_CONTROL", "annualized_return_pct", 0))
    side_flip_ann = float(scenario_value(scenarios, "P418_SIDE_FLIP_CONTROL", "annualized_return_pct", 0))
    proxy_ann = float(scenario_value(scenarios, "P418_SINGLE_LEG_PROXY_CONTROL", "annualized_return_pct", 0))
    return pd.DataFrame(
        [
            ("selected_verdict", VERDICT, "Positive cost200 synthetic result but failed full-depth contribution gate.", "lead_not_acceptance"),
            ("primary_completed_round_trips", metric_value(summary, "phase418_primary_completed_round_trips", 0), "Event floor passed.", "positive_lead"),
            ("primary_trade_dates", metric_value(summary, "phase418_primary_trade_dates", 0), "Date breadth passed.", "positive_lead"),
            ("primary_pairs", metric_value(summary, "phase418_primary_pairs", 0), "Pair breadth passed.", "positive_lead"),
            ("primary_positive_date_fraction", metric_value(summary, "phase418_primary_positive_date_fraction", 0), "Positive-date gate passed.", "positive_lead"),
            ("primary_net_pnl_inr", metric_value(summary, "phase418_primary_net_pnl_inr", 0), "Synthetic cost200 net P&L.", "positive_lead"),
            ("primary_annualized_return_pct", primary_ann, "Synthetic cost200 annualized return.", "positive_lead"),
            ("side_flip_annualized_return_pct", side_flip_ann, "Side-flip control was strongly worse.", "supportive_control"),
            ("l2_l5_removed_annualized_return_pct", l2_removed_ann, "Levels 2-5 removed control outperformed primary.", "blocking_control"),
            ("single_leg_proxy_annualized_return_pct", proxy_ann, "Single-leg proxy positive but below primary.", "supportive_control"),
            ("phase418_failed_hard_gates", failed_gates(gates418), "Explicit failed gate basis.", "basis"),
            ("full_depth_contribution_proven", int(primary_ann >= l2_removed_ann), "Must be one before acceptance.", "blocked"),
            ("real_anchor_pair_evidence_strong", 0, "Real-anchor pair catalog evidence unavailable/zero in bounded run.", "blocked"),
            ("strategy_promotion_allowed", 0, "Blocked despite positive synthetic lead.", "closed"),
            ("paper_or_live_acceptance_allowed", 0, "No paper/live acceptance.", "closed"),
            ("deployable_profitability_claim_allowed", 0, "No deployable claim.", "closed"),
            ("next_action", NEXT_ACTION, "Repair contribution/evidence first, not paper/live.", "next"),
        ],
        columns=["decision_id", "decision_value", "evidence", "status"],
    )


def build_required_repairs() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("P420_FULL_DEPTH_CONTRIBUTION_REPAIR", "Create a precommitted test where levels 2-5 materially improve or uniquely gate the pair-spread result.", "required_before_acceptance"),
            ("P420_REAL_ANCHOR_PAIR_PANEL_REPAIR", "Verify whether local/Azure real L2 has matching pair symbols and dates, then run pair replay on real anchors if available.", "required_before_acceptance"),
            ("P420_SAME_TIMESTAMP_ALIGNMENT_AUDIT", "Audit same-millisecond aligned entry/exit cases and enforce a minimum forward-tick or elapsed-time rule if needed.", "required_before_acceptance"),
            ("P420_COST100_COST200_RANK_AUDIT", "Record whether the positive lead remains ranked under cost100/cost200 without weakening acceptance.", "required_before_acceptance"),
            ("P420_NO_PAPER_LIVE_BOUNDARY", "No paper/live until contribution, real-anchor and timing realism repairs pass.", "closed_boundary"),
        ],
        columns=["repair_id", "repair_requirement", "status"],
    )


def build_gates(summary: pd.DataFrame, gates418: pd.DataFrame, decision: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(summary, "phase418_pair_spread_convergence_execution_complete", 0))
    primary_ann = float(metric_value(summary, "phase418_primary_annualized_return_pct", 0))
    survivors = as_int(metric_value(summary, "phase418_cost200_acceptance_survivor_rows", 0))
    full_depth = as_int(decision.loc[decision["decision_id"].eq("full_depth_contribution_proven"), "decision_value"].iloc[0])
    gates = [
        ("P419_PHASE418_COMPLETE", complete == 1, complete, 1),
        ("P419_PHASE418_GATES_EVALUATED", len(gates418) == 21, len(gates418), 21),
        ("P419_POSITIVE_SYNTHETIC_LEAD_CONFIRMED", primary_ann >= 12.0 and survivors > 0, f"annualized={primary_ann};survivors={survivors}", "annualized>=12;survivors>0"),
        ("P419_FAILED_GATE_BASIS_PRESENT", failed_gates(gates418) != "", failed_gates(gates418), "nonempty"),
        ("P419_FULL_DEPTH_CONTRIBUTION_BLOCKER_RECORDED", full_depth == 0, full_depth, 0),
        ("P419_REAL_ANCHOR_BLOCKER_RECORDED", str(decision.loc[decision["decision_id"].eq("real_anchor_pair_evidence_strong"), "decision_value"].iloc[0]) == "0", 0, 0),
        ("P419_VERDICT_PRESENT", str(decision.loc[decision["decision_id"].eq("selected_verdict"), "decision_value"].iloc[0]) == VERDICT, VERDICT, VERDICT),
        ("P419_NO_PROMOTION_OR_PAPER_LIVE", str(decision.loc[decision["decision_id"].eq("paper_or_live_acceptance_allowed"), "decision_value"].iloc[0]) == "0", "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase419_pair_spread_convergence_interpretation_complete", 1, "Phase419 interpretation completed"),
            ("phase419_selected_verdict", VERDICT, "Selected verdict"),
            ("phase419_phase418_primary_completed_round_trips", metric_value(summary, "phase418_primary_completed_round_trips", 0), "Primary pair round trips"),
            ("phase419_phase418_primary_positive_date_fraction", metric_value(summary, "phase418_primary_positive_date_fraction", 0), "Positive date fraction"),
            ("phase419_phase418_primary_net_pnl_inr", metric_value(summary, "phase418_primary_net_pnl_inr", 0), "Primary net P&L"),
            ("phase419_phase418_primary_annualized_return_pct", metric_value(summary, "phase418_primary_annualized_return_pct", 0), "Primary annualized return"),
            ("phase419_positive_synthetic_lead_preserved", 1, "Keep as lead"),
            ("phase419_strategy_acceptance_allowed", 0, "Blocked by L2-L5 removed control and real-anchor gap"),
            ("phase419_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase419_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase419_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase419_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase419_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, decision: pd.DataFrame, repairs: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase419 Pair-Spread Convergence Interpretation",
        "",
        "Phase419 interprets the positive synthetic Phase418 pair-spread result as a lead, not an accepted strategy.",
        "",
        "The result passes breadth and annualized-return gates, but promotion remains blocked because the levels 2-5 removed control outperformed the primary and real-anchor pair evidence is not strong yet.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Decision Ledger",
        "",
        _markdown_table(decision),
        "",
        "## Required Repairs Before Acceptance",
        "",
        _markdown_table(repairs),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: positive synthetic lead does not mean paper/live acceptance.",
    ]
    (output_dir / "phase419_pair_spread_convergence_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase418_dir: Path = DEFAULT_PHASE418_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    summary = read_csv(phase418_dir / "phase418_acceptance_summary.csv")
    gates418 = read_csv(phase418_dir / "phase418_gate_evaluation.csv")
    scenarios = read_csv(phase418_dir / "phase418_synthetic_scenario_summary.csv")
    if summary.empty or gates418.empty or scenarios.empty:
        raise FileNotFoundError("Phase419 requires Phase418 summary, gates and scenario summary.")
    decision = build_decision(summary, gates418, scenarios)
    repairs = build_required_repairs()
    gates = build_gates(summary, gates418, decision)
    acceptance = build_acceptance(summary, gates)
    decision.to_csv(output_dir / "phase419_decision_ledger.csv", index=False)
    repairs.to_csv(output_dir / "phase419_required_repairs.csv", index=False)
    gates.to_csv(output_dir / "phase419_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase419_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, decision, repairs, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase419_pair_spread_convergence_interpretation",
        **reproducibility_fields(
            artifact_id="phase419_pair_spread_convergence_interpretation",
            generated_utc=generated_utc,
            inputs={
                "phase418_acceptance_summary": str(phase418_dir / "phase418_acceptance_summary.csv"),
                "phase418_gate_evaluation": str(phase418_dir / "phase418_gate_evaluation.csv"),
                "phase418_synthetic_scenario_summary": str(phase418_dir / "phase418_synthetic_scenario_summary.csv"),
            },
            parameters={"selected_verdict": VERDICT, "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase419_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase418_pair_taker_next_aligned_tick",
        ),
    }
    (output_dir / "phase419_pair_spread_convergence_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase419 pair-spread convergence interpretation.")
    parser.add_argument("--phase418-dir", type=Path, default=DEFAULT_PHASE418_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase418_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
