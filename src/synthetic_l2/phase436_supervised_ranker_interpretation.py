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
from synthetic_l2.phase435_supervised_full_depth_event_ranker import NEXT_ACTION as PHASE435_NEXT_ACTION
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE435_DIR = Path("outputs/phase435")
DEFAULT_OUTPUT_DIR = Path("outputs/phase436")

VERDICT = "P436_SUPERVISED_FULL_DEPTH_EVENT_RANKER_REJECTED_COST_DOMINATED"
NEXT_ACTION = "precommit_material_new_lower_turnover_horizon_or_pause_strategy_search"
REPAIR_ACTION = "repair_phase436_interpretation_inputs"


def failed_gates(gates: pd.DataFrame) -> str:
    if gates.empty:
        return ""
    failed = gates.loc[gates["passed"].astype(str).str.lower().isin(["false", "0"])]
    return ";".join(failed["gate_id"].astype(str).tolist())


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def build_decision(acceptance435: pd.DataFrame, gates435: pd.DataFrame, scenario: pd.DataFrame, real: pd.DataFrame) -> pd.DataFrame:
    primary = scenario[scenario["scenario_id"].astype(str).eq("P435_full_depth_ranker_validation")].iloc[0] if not scenario.empty else pd.Series(dtype=object)
    l1 = scenario[scenario["scenario_id"].astype(str).eq("P435_l1_only_ablation_validation")].iloc[0] if not scenario.empty else pd.Series(dtype=object)
    shuffle = scenario[scenario["scenario_id"].astype(str).eq("P435_time_shuffle_control_validation")].iloc[0] if not scenario.empty else pd.Series(dtype=object)
    real_row = real.iloc[0] if not real.empty else pd.Series(dtype=object)
    return pd.DataFrame(
        [
            ("selected_verdict", VERDICT, "The materially new supervised full-depth event ranker produced enough events to test but failed cost200 profitability and controls.", "terminal_for_this_source_form"),
            ("phase435_next_action_matched", PHASE435_NEXT_ACTION, "Phase436 implements the Phase435 next-action string.", "basis"),
            ("synthetic_event_rows", scalar(acceptance435, "phase435_synthetic_event_rows", 0), "Synthetic event-label rows used by Phase435.", "evidence"),
            ("primary_round_trips", primary.get("completed_round_trips", 0), "Primary selected validation trades.", "evidence"),
            ("primary_trade_dates", primary.get("trade_dates", 0), "Validation date breadth.", "failure"),
            ("primary_symbols", primary.get("symbols", 0), "Validation symbol breadth.", "failure"),
            ("primary_gross_pnl_inr", primary.get("gross_pnl_inr", 0), "Gross edge before costs.", "evidence"),
            ("primary_cost200_inr", primary.get("cost200_inr", 0), "Zerodha cost200 charges.", "failure"),
            ("primary_net_pnl_inr", primary.get("net_pnl_inr", 0), "Net P&L after cost200.", "failure"),
            ("primary_annualized_return_pct", primary.get("annualized_return_pct", 0), "Failed annualized floor.", "failure"),
            ("l1_only_annualized_return_pct", l1.get("annualized_return_pct", 0), "L1-only ablation nearly matched primary.", "control_failure"),
            ("time_shuffle_annualized_return_pct", shuffle.get("annualized_return_pct", 0), "Time-shuffle control was less negative than primary.", "control_failure"),
            ("real_anchor_annualized_return_pct", real_row.get("annualized_return_pct", 0), "Real-anchor cross-check preserved negative sign.", "evidence"),
            ("phase435_failed_hard_gates", failed_gates(gates435), "Explicit failed gate basis.", "basis"),
            ("strategy_promotion_allowed", 0, "No accepted survivor.", "closed"),
            ("paper_or_live_acceptance_allowed", 0, "No paper/live acceptance.", "closed"),
            ("deployable_profitability_claim_allowed", 0, "No deployable claim.", "closed"),
            ("same_source_rescue_allowed", 0, "Do not retune this same ranker after seeing validation/control failures.", "closed"),
            ("next_action", NEXT_ACTION, "Move only to a materially lower-turnover/longer-horizon source, or pause strategy search.", "next"),
        ],
        columns=["decision_id", "decision_value", "evidence", "status"],
    )


def build_gates(acceptance435: pd.DataFrame, gates435: pd.DataFrame, decision: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(scalar(acceptance435, "phase435_supervised_full_depth_event_ranker_complete", 0))
    hard_rows = as_int(scalar(acceptance435, "phase435_hard_gate_rows", 0))
    hard_pass = as_int(scalar(acceptance435, "phase435_hard_gate_pass_rows", 0))
    ann = float(scalar(acceptance435, "phase435_best_annualized_return_pct", 0))
    survivors = as_int(scalar(acceptance435, "phase435_cost200_acceptance_survivor_rows", 0))
    verdict = str(decision.loc[decision["decision_id"].eq("selected_verdict"), "decision_value"].iloc[0])
    gates = [
        ("P436_PHASE435_COMPLETE", complete == 1, complete, 1),
        ("P436_PHASE435_GATES_EVALUATED", hard_rows == 14, hard_rows, 14),
        ("P436_PHASE435_FAILED_GATES_PRESENT", hard_pass < hard_rows and failed_gates(gates435) != "", f"passed={hard_pass}/{hard_rows};failed={failed_gates(gates435)}", "failed_gates_nonempty"),
        ("P436_NO_ACCEPTANCE_SURVIVOR_CONFIRMED", survivors == 0, survivors, 0),
        ("P436_NEGATIVE_COST200_CONFIRMED", ann < 0, ann, "<0"),
        ("P436_VERDICT_PRESENT", verdict == VERDICT, verdict, VERDICT),
        ("P436_NO_SAME_SOURCE_RESCUE", str(decision.loc[decision["decision_id"].eq("same_source_rescue_allowed"), "decision_value"].iloc[0]) == "0", 0, 0),
        ("P436_BOUNDARIES_CLOSED", str(decision.loc[decision["decision_id"].eq("paper_or_live_acceptance_allowed"), "decision_value"].iloc[0]) == "0", "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(acceptance435: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase436_supervised_ranker_interpretation_complete", 1, "Phase436 interpretation completed"),
            ("phase436_selected_verdict", VERDICT, "Selected verdict"),
            ("phase436_phase435_best_completed_round_trips", scalar(acceptance435, "phase435_best_completed_round_trips", 0), "Phase435 primary round trips"),
            ("phase436_phase435_best_annualized_return_pct", scalar(acceptance435, "phase435_best_annualized_return_pct", 0), "Phase435 primary annualized return"),
            ("phase436_phase435_acceptance_survivors", scalar(acceptance435, "phase435_cost200_acceptance_survivor_rows", 0), "Phase435 cost200 survivors"),
            ("phase436_strategy_promotion_allowed", 0, "No promotion"),
            ("phase436_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase436_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase436_same_source_rescue_allowed", 0, "No same-source rescue"),
            ("phase436_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase436_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase436_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, decision: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase436 Supervised Ranker Interpretation",
        "",
        "Phase436 formally interprets Phase435 as a negative execution result.",
        "",
        "The supervised full-depth event ranker was materially new and generated enough validation trades to test execution costs, but it did not produce a profitable cost200 strategy and failed important controls.",
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
        "Boundary: do not rescue the same supervised ranker by retuning after seeing the validation result. If strategy search continues, precommit a materially lower-turnover or longer-horizon source before execution.",
    ]
    (output_dir / "phase436_supervised_ranker_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase435_dir: Path = DEFAULT_PHASE435_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    acceptance435 = read_csv(phase435_dir / "phase435_acceptance_summary.csv")
    gates435 = read_csv(phase435_dir / "phase435_gate_evaluation.csv")
    scenario = read_csv(phase435_dir / "phase435_scenario_summary.csv")
    real = read_csv(phase435_dir / "phase435_real_anchor_summary.csv")
    if acceptance435.empty or gates435.empty or scenario.empty:
        raise FileNotFoundError("Phase436 requires Phase435 acceptance, gates and scenario summary.")
    decision = build_decision(acceptance435, gates435, scenario, real)
    gates = build_gates(acceptance435, gates435, decision)
    acceptance = build_acceptance(acceptance435, gates)
    decision.to_csv(output_dir / "phase436_decision_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase436_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase436_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, decision, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase436_supervised_ranker_interpretation",
        **reproducibility_fields(
            artifact_id="phase436_supervised_ranker_interpretation",
            generated_utc=generated_utc,
            inputs={"phase435_acceptance_summary": str(phase435_dir / "phase435_acceptance_summary.csv")},
            parameters={"selected_verdict": VERDICT, "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase436_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase435_exact_tick_forward_label",
        ),
    }
    (output_dir / "phase436_supervised_ranker_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase436 supervised ranker interpretation.")
    parser.add_argument("--phase435-dir", type=Path, default=DEFAULT_PHASE435_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase435_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
