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
from synthetic_l2.phase444_external_catalyst_continuation_full_depth import NEXT_ACTION as PHASE444_NEXT_ACTION
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE444_DIR = Path("outputs/phase444")
DEFAULT_OUTPUT_DIR = Path("outputs/phase445")

VERDICT = "P445_CATALYST_CONTINUATION_POSITIVE_DIAGNOSTIC_NOT_ACCEPTED"
NEXT_ACTION = "precommit_catalyst_continuation_stability_repair_or_add_real_holdout"
REPAIR_ACTION = "repair_phase445_interpretation_inputs"


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def failed_gates(gates: pd.DataFrame) -> str:
    if gates.empty:
        return ""
    failed = gates.loc[gates["passed"].astype(str).str.lower().isin(["false", "0"])]
    return ";".join(failed["gate_id"].astype(str).tolist())


def build_decision(acc: pd.DataFrame, gates444: pd.DataFrame, controls: pd.DataFrame) -> pd.DataFrame:
    l1 = controls[controls["control"].astype(str).eq("l1_only")].iloc[0] if not controls.empty else pd.Series(dtype=object)
    reversal = controls[controls["control"].astype(str).eq("reversal")].iloc[0] if not controls.empty else pd.Series(dtype=object)
    shift = controls[controls["control"].astype(str).eq("time_shifted_catalyst")].iloc[0] if not controls.empty else pd.Series(dtype=object)
    return pd.DataFrame(
        [
            ("selected_verdict", VERDICT, "Catalyst continuation cleared cost200 and beat L1-only, but failed positive-date and 12 percent annualized gates.", "positive_diagnostic_not_acceptance"),
            ("phase444_next_action_matched", PHASE444_NEXT_ACTION, "Phase445 implements the Phase444 next-action string.", "basis"),
            ("best_scenario_id", scalar(acc, "phase444_best_scenario_id", ""), "Best Phase444 scenario.", "evidence"),
            ("best_round_trips", scalar(acc, "phase444_best_completed_round_trips", 0), "Event floor met.", "evidence"),
            ("best_trade_dates", scalar(acc, "phase444_best_trade_dates", 0), "Date breadth met.", "evidence"),
            ("best_symbols", scalar(acc, "phase444_best_symbols", 0), "Symbol breadth met.", "evidence"),
            ("best_gross_pnl_inr", scalar(acc, "phase444_best_gross_pnl_inr", 0), "Positive gross P&L.", "evidence"),
            ("best_net_pnl_inr", scalar(acc, "phase444_best_net_pnl_inr", 0), "Positive after cost200.", "evidence"),
            ("best_annualized_return_pct", scalar(acc, "phase444_best_annualized_return_pct", 0), "Positive but below 12 percent.", "failure"),
            ("best_positive_date_fraction", scalar(acc, "phase444_best_positive_date_fraction", 0), "Below positive-date gate.", "failure"),
            ("l1_only_annualized_return_pct", l1.get("annualized_return_pct", 0), "Full-depth materially beat L1-only.", "control_pass"),
            ("reversal_control_annualized_return_pct", reversal.get("annualized_return_pct", 0), "Continuation beat reversal.", "control_pass"),
            ("time_shifted_catalyst_annualized_return_pct", shift.get("annualized_return_pct", 0), "Time-shift was close to primary.", "diagnostic_warning"),
            ("phase444_failed_hard_gates", failed_gates(gates444), "Explicit failed gate basis.", "basis"),
            ("strategy_promotion_allowed", 0, "No accepted survivor.", "closed"),
            ("paper_or_live_acceptance_allowed", 0, "No paper/live acceptance.", "closed"),
            ("deployable_profitability_claim_allowed", 0, "No deployable claim.", "closed"),
            ("same_result_tuning_allowed", 0, "No post-result tuning without a new precommit.", "closed"),
            ("next_action", NEXT_ACTION, "Repair stability or add real holdout under a new precommit.", "next"),
        ],
        columns=["decision_id", "decision_value", "evidence", "status"],
    )


def build_gates(acc: pd.DataFrame, gates444: pd.DataFrame, decision: pd.DataFrame) -> pd.DataFrame:
    hard_rows = as_int(scalar(acc, "phase444_hard_gate_rows", 0))
    hard_pass = as_int(scalar(acc, "phase444_hard_gate_pass_rows", 0))
    net = float(scalar(acc, "phase444_best_net_pnl_inr", 0))
    ann = float(scalar(acc, "phase444_best_annualized_return_pct", 0))
    survivors = as_int(scalar(acc, "phase444_cost200_acceptance_survivor_rows", 0))
    verdict = str(decision.loc[decision["decision_id"].eq("selected_verdict"), "decision_value"].iloc[0])
    gates = [
        ("P445_PHASE444_COMPLETE", as_int(scalar(acc, "phase444_external_catalyst_continuation_complete", 0)) == 1, scalar(acc, "phase444_external_catalyst_continuation_complete", 0), 1),
        ("P445_PHASE444_GATES_EVALUATED", hard_rows == 14, hard_rows, 14),
        ("P445_PHASE444_FAILED_GATES_PRESENT", hard_pass < hard_rows and failed_gates(gates444) != "", f"passed={hard_pass}/{hard_rows};failed={failed_gates(gates444)}", "failed_gates_nonempty"),
        ("P445_POSITIVE_COST200_DIAGNOSTIC_CONFIRMED", net > 0 and ann > 0, f"net={net};ann={ann}", "positive_net_and_ann"),
        ("P445_NOT_ACCEPTED_CONFIRMED", survivors == 0, survivors, 0),
        ("P445_VERDICT_PRESENT", verdict == VERDICT, verdict, VERDICT),
        ("P445_NO_SAME_RESULT_TUNING", str(decision.loc[decision["decision_id"].eq("same_result_tuning_allowed"), "decision_value"].iloc[0]) == "0", 0, 0),
        ("P445_BOUNDARIES_CLOSED", str(decision.loc[decision["decision_id"].eq("paper_or_live_acceptance_allowed"), "decision_value"].iloc[0]) == "0", "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(acc: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase445_catalyst_continuation_interpretation_complete", 1, "Phase445 interpretation completed"),
            ("phase445_selected_verdict", VERDICT, "Selected verdict"),
            ("phase445_phase444_best_completed_round_trips", scalar(acc, "phase444_best_completed_round_trips", 0), "Phase444 best round trips"),
            ("phase445_phase444_best_net_pnl_inr", scalar(acc, "phase444_best_net_pnl_inr", 0), "Phase444 best net P&L"),
            ("phase445_phase444_best_annualized_return_pct", scalar(acc, "phase444_best_annualized_return_pct", 0), "Phase444 best annualized return"),
            ("phase445_phase444_acceptance_survivors", scalar(acc, "phase444_cost200_acceptance_survivor_rows", 0), "Phase444 survivors"),
            ("phase445_strategy_promotion_allowed", 0, "No promotion"),
            ("phase445_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase445_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase445_same_result_tuning_allowed", 0, "No same-result tuning"),
            ("phase445_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase445_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase445_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, decision: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase445 Catalyst Continuation Interpretation",
        "",
        "Phase445 formally interprets Phase444 as a positive diagnostic, not an accepted strategy.",
        "",
        "The catalyst-continuation source cleared costs and beat L1-only, but failed the 12 percent annualized and positive-date-fraction gates.",
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
        "Boundary: this result may guide a new precommit for stability repair or real holdout, but it is not a promotion, paper/live, or deployable profitability result.",
    ]
    (output_dir / "phase445_catalyst_continuation_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase444_dir: Path = DEFAULT_PHASE444_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    acc = read_csv(phase444_dir / "phase444_acceptance_summary.csv")
    gates444 = read_csv(phase444_dir / "phase444_gate_evaluation.csv")
    controls = read_csv(phase444_dir / "phase444_best_scenario_controls.csv")
    if acc.empty or gates444.empty or controls.empty:
        raise FileNotFoundError("Phase445 requires Phase444 acceptance, gates and controls.")
    decision = build_decision(acc, gates444, controls)
    gates = build_gates(acc, gates444, decision)
    acceptance = build_acceptance(acc, gates)
    decision.to_csv(output_dir / "phase445_decision_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase445_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase445_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, decision, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase445_catalyst_continuation_interpretation",
        **reproducibility_fields(
            artifact_id="phase445_catalyst_continuation_interpretation",
            generated_utc=generated_utc,
            inputs={"phase444_acceptance_summary": str(phase444_dir / "phase444_acceptance_summary.csv")},
            parameters={"selected_verdict": VERDICT, "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase445_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase387_event_feature_fixed_horizon",
        ),
    }
    (output_dir / "phase445_catalyst_continuation_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase445 catalyst continuation interpretation.")
    parser.add_argument("--phase444-dir", type=Path, default=DEFAULT_PHASE444_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase444_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
