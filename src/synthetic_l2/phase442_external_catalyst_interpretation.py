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
from synthetic_l2.phase441_external_catalyst_full_depth_confirmation import NEXT_ACTION as PHASE441_NEXT_ACTION
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE441_DIR = Path("outputs/phase441")
DEFAULT_OUTPUT_DIR = Path("outputs/phase442")

VERDICT = "P442_EXTERNAL_CATALYST_REVERSAL_REJECTED_CONTROLS_FAVOR_SIDE_FLIP"
NEXT_ACTION = "precommit_external_catalyst_continuation_or_pause_strategy_search"
REPAIR_ACTION = "repair_phase442_interpretation_inputs"


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def failed_gates(gates: pd.DataFrame) -> str:
    failed = gates.loc[gates["passed"].astype(str).str.lower().isin(["false", "0"])] if not gates.empty else pd.DataFrame()
    return ";".join(failed["gate_id"].astype(str).tolist()) if not failed.empty else ""


def build_decision(acc: pd.DataFrame, gates441: pd.DataFrame, summary: pd.DataFrame, controls: pd.DataFrame) -> pd.DataFrame:
    best_sid = str(scalar(acc, "phase441_best_scenario_id", ""))
    best = summary[summary["scenario_id"].astype(str).eq(best_sid)].iloc[0] if not summary.empty else pd.Series(dtype=object)
    side = controls[controls["control"].astype(str).eq("side_flip")].iloc[0] if not controls.empty else pd.Series(dtype=object)
    l1 = controls[controls["control"].astype(str).eq("l1_only")].iloc[0] if not controls.empty else pd.Series(dtype=object)
    return pd.DataFrame(
        [
            ("selected_verdict", VERDICT, "External catalyst plus full-depth reversal achieved breadth but failed profitability and controls; side flip was much better.", "terminal_for_reversal_form"),
            ("phase441_next_action_matched", PHASE441_NEXT_ACTION, "Phase442 implements the Phase441 next-action string.", "basis"),
            ("source_event_rows", scalar(acc, "phase441_source_event_rows", 0), "Source event floor was available.", "evidence"),
            ("best_scenario_id", best_sid, "Best frozen reversal scenario.", "evidence"),
            ("best_round_trips", best.get("completed_round_trips", 0), "Event floor was met.", "evidence"),
            ("best_trade_dates", best.get("trade_dates", 0), "Date breadth was met.", "evidence"),
            ("best_symbols", best.get("symbols", 0), "Symbol breadth was met.", "evidence"),
            ("best_net_pnl_inr", best.get("net_pnl_inr", 0), "Negative after cost200.", "failure"),
            ("best_annualized_return_pct", best.get("annualized_return_pct", 0), "Failed 12 percent annualized floor.", "failure"),
            ("best_positive_date_fraction", best.get("positive_date_fraction", 0), "Failed positive-date fraction.", "failure"),
            ("side_flip_annualized_return_pct", side.get("annualized_return_pct", 0), "Side flip was better than primary.", "control_failure"),
            ("l1_only_annualized_return_pct", l1.get("annualized_return_pct", 0), "L1-only was also better than primary.", "control_failure"),
            ("phase441_failed_hard_gates", failed_gates(gates441), "Explicit failed gate basis.", "basis"),
            ("strategy_promotion_allowed", 0, "No accepted survivor.", "closed"),
            ("paper_or_live_acceptance_allowed", 0, "No paper/live acceptance.", "closed"),
            ("deployable_profitability_claim_allowed", 0, "No deployable claim.", "closed"),
            ("same_reversal_rescue_allowed", 0, "Do not tune this same reversal form after seeing controls.", "closed"),
            ("side_flip_as_new_precommit_allowed", 1, "Continuation/side-flip may be tested only as a new precommitted source.", "next"),
            ("next_action", NEXT_ACTION, "Precommit catalyst continuation/side-flip as a new source, or pause.", "next"),
        ],
        columns=["decision_id", "decision_value", "evidence", "status"],
    )


def build_gates(acc: pd.DataFrame, gates441: pd.DataFrame, decision: pd.DataFrame) -> pd.DataFrame:
    hard_pass = as_int(scalar(acc, "phase441_hard_gate_pass_rows", 0))
    hard_rows = as_int(scalar(acc, "phase441_hard_gate_rows", 0))
    ann = float(scalar(acc, "phase441_best_annualized_return_pct", 0))
    survivors = as_int(scalar(acc, "phase441_cost200_acceptance_survivor_rows", 0))
    verdict = str(decision.loc[decision["decision_id"].eq("selected_verdict"), "decision_value"].iloc[0])
    gates = [
        ("P442_PHASE441_COMPLETE", as_int(scalar(acc, "phase441_external_catalyst_full_depth_complete", 0)) == 1, scalar(acc, "phase441_external_catalyst_full_depth_complete", 0), 1),
        ("P442_PHASE441_GATES_EVALUATED", hard_rows == 14, hard_rows, 14),
        ("P442_PHASE441_FAILED_GATES_PRESENT", hard_pass < hard_rows and failed_gates(gates441) != "", f"passed={hard_pass}/{hard_rows};failed={failed_gates(gates441)}", "failed_gates_nonempty"),
        ("P442_BREADTH_ACHIEVED_BUT_NOT_ACCEPTED", as_int(scalar(acc, "phase441_best_trade_dates", 0)) >= 5 and survivors == 0, f"dates={scalar(acc, 'phase441_best_trade_dates', 0)};survivors={survivors}", "breadth_without_acceptance"),
        ("P442_NEGATIVE_COST200_CONFIRMED", ann < 0, ann, "<0"),
        ("P442_VERDICT_PRESENT", verdict == VERDICT, verdict, VERDICT),
        ("P442_NO_SAME_REVERSAL_RESCUE", str(decision.loc[decision["decision_id"].eq("same_reversal_rescue_allowed"), "decision_value"].iloc[0]) == "0", 0, 0),
        ("P442_SIDE_FLIP_REQUIRES_NEW_PRECOMMIT", str(decision.loc[decision["decision_id"].eq("side_flip_as_new_precommit_allowed"), "decision_value"].iloc[0]) == "1", 1, 1),
        ("P442_BOUNDARIES_CLOSED", str(decision.loc[decision["decision_id"].eq("paper_or_live_acceptance_allowed"), "decision_value"].iloc[0]) == "0", "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(acc: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase442_external_catalyst_interpretation_complete", 1, "Phase442 interpretation completed"),
            ("phase442_selected_verdict", VERDICT, "Selected verdict"),
            ("phase442_phase441_best_completed_round_trips", scalar(acc, "phase441_best_completed_round_trips", 0), "Phase441 best round trips"),
            ("phase442_phase441_best_annualized_return_pct", scalar(acc, "phase441_best_annualized_return_pct", 0), "Phase441 best annualized return"),
            ("phase442_phase441_acceptance_survivors", scalar(acc, "phase441_cost200_acceptance_survivor_rows", 0), "Phase441 survivors"),
            ("phase442_strategy_promotion_allowed", 0, "No promotion"),
            ("phase442_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase442_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase442_same_reversal_rescue_allowed", 0, "No same-form rescue"),
            ("phase442_side_flip_new_precommit_allowed", 1, "Continuation side may be precommitted as new source"),
            ("phase442_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase442_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase442_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, decision: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase442 External Catalyst Interpretation",
        "",
        "Phase442 formally interprets Phase441 as a rejected catalyst-reversal result.",
        "",
        "The external-catalyst source achieved event/date/symbol breadth, but controls favored the opposite side and profitability stayed below zero after cost200.",
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
        "Boundary: the same catalyst-reversal form is closed. Catalyst continuation/side-flip can only be tested as a new precommitted source.",
    ]
    (output_dir / "phase442_external_catalyst_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase441_dir: Path = DEFAULT_PHASE441_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    acc = read_csv(phase441_dir / "phase441_acceptance_summary.csv")
    gates441 = read_csv(phase441_dir / "phase441_gate_evaluation.csv")
    summary = read_csv(phase441_dir / "phase441_scenario_summary.csv")
    controls = read_csv(phase441_dir / "phase441_best_scenario_controls.csv")
    if acc.empty or gates441.empty or summary.empty:
        raise FileNotFoundError("Phase442 requires Phase441 acceptance, gates and summary.")
    decision = build_decision(acc, gates441, summary, controls)
    gates = build_gates(acc, gates441, decision)
    acceptance = build_acceptance(acc, gates)
    decision.to_csv(output_dir / "phase442_decision_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase442_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase442_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, decision, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase442_external_catalyst_interpretation",
        **reproducibility_fields(
            artifact_id="phase442_external_catalyst_interpretation",
            generated_utc=generated_utc,
            inputs={"phase441_acceptance_summary": str(phase441_dir / "phase441_acceptance_summary.csv")},
            parameters={"selected_verdict": VERDICT, "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase442_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase387_event_feature_fixed_horizon",
        ),
    }
    (output_dir / "phase442_external_catalyst_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase442 external catalyst interpretation.")
    parser.add_argument("--phase441-dir", type=Path, default=DEFAULT_PHASE441_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase441_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
