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


DEFAULT_PHASE410_DIR = Path("outputs/phase410")
DEFAULT_PHASE411_DIR = Path("outputs/phase411")
DEFAULT_OUTPUT_DIR = Path("outputs/phase412")

VERDICT = "P412_REPLENISHMENT_BREAKOUT_REJECTED_AS_ZERO_EVENT_FORM"
NEXT_ACTION = "precommit_material_new_less_sparse_full_depth_l2_thesis_or_build_filter_failure_attribution_before_execution"
REPAIR_ACTION = "repair_phase412_replenishment_breakout_interpretation"


def build_decision_ledger(summary411: pd.DataFrame, gates411: pd.DataFrame, synthetic_diag: pd.DataFrame) -> pd.DataFrame:
    failed = gates411.loc[gates411["passed"].astype(str).str.lower().isin(["false", "0"])]
    primary_trades = metric_value(summary411, "phase411_primary_completed_round_trips", 0)
    scan_points = 0
    groups = 0
    if not synthetic_diag.empty:
        scan_points = int(pd.to_numeric(synthetic_diag.get("candidate_scan_points", pd.Series(dtype=float)), errors="coerce").fillna(0).sum())
        groups = int(len(synthetic_diag))
    return pd.DataFrame(
        [
            ("selected_verdict", VERDICT, "Primary selected zero trades under frozen Phase410 thresholds.", "terminal_for_this_form"),
            ("phase411_primary_completed_round_trips", primary_trades, "Observed primary completed round trips.", "failed_event_floor"),
            ("phase411_failed_hard_gates", ";".join(failed["gate_id"].astype(str).tolist()), "Explicit Phase411 failed gate basis.", "basis"),
            ("phase411_synthetic_diagnostic_groups", groups, "Execution scanned symbol/date/scenario groups.", "input_not_empty"),
            ("phase411_synthetic_candidate_scan_points", scan_points, "Execution scanned candidate points.", "input_not_empty"),
            ("phase411_zero_event_not_profitability_success", 1, "Zero trades and zero PnL cannot be treated as annualized success.", "guardrail"),
            ("same_family_threshold_relaxation_allowed", 0, "Do not relax Phase410 thresholds after observing zero selected events.", "closed"),
            ("phase410_thesis_replay_allowed_again", 0, "Do not rerun same form shard-after-shard as a rescue.", "closed"),
            ("strategy_promotion_allowed", 0, "No accepted survivor.", "closed"),
            ("paper_or_live_acceptance_allowed", 0, "Backtest failure only.", "closed"),
            ("deployable_profitability_claim_allowed", 0, "No deployable edge claim.", "closed"),
            ("next_action", NEXT_ACTION, "Next work must either attribute filter sparsity or precommit a materially different less-sparse full-depth thesis.", "next"),
        ],
        columns=["decision_id", "decision_value", "evidence", "status"],
    )


def build_failure_attribution(summary411: pd.DataFrame, synthetic_diag: pd.DataFrame, real_diag: pd.DataFrame) -> pd.DataFrame:
    synthetic_scan_points = int(pd.to_numeric(synthetic_diag.get("candidate_scan_points", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()) if not synthetic_diag.empty else 0
    synthetic_selected = int(pd.to_numeric(synthetic_diag.get("selected_trades", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()) if not synthetic_diag.empty else 0
    real_scan_points = int(pd.to_numeric(real_diag.get("candidate_scan_points", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()) if not real_diag.empty else 0
    real_selected = int(pd.to_numeric(real_diag.get("selected_trades", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()) if not real_diag.empty else 0
    return pd.DataFrame(
        [
            ("synthetic_scan_points", synthetic_scan_points, "candidate scan points in synthetic bounded shard"),
            ("synthetic_selected_trades", synthetic_selected, "selected synthetic trades"),
            ("synthetic_selection_rate", synthetic_selected / synthetic_scan_points if synthetic_scan_points else 0.0, "selected / scan points"),
            ("real_anchor_scan_points", real_scan_points, "candidate scan points in real-anchor shard"),
            ("real_anchor_selected_trades", real_selected, "selected real-anchor trades"),
            ("real_anchor_selection_rate", real_selected / real_scan_points if real_scan_points else 0.0, "selected / scan points"),
            ("primary_annualized_return_pct", metric_value(summary411, "phase411_primary_annualized_return_pct", 0), "primary annualized return"),
            ("cost200_acceptance_survivor_rows", metric_value(summary411, "phase411_cost200_acceptance_survivor_rows", 0), "accepted scenarios"),
        ],
        columns=["attribution_id", "value", "description"],
    )


def build_gate_evaluation(summary411: pd.DataFrame, gates411: pd.DataFrame, decision: pd.DataFrame, attribution: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(summary411, "phase411_full_depth_replenishment_breakout_execution_complete", 0))
    primary_trades = as_int(metric_value(summary411, "phase411_primary_completed_round_trips", 0))
    survivors = as_int(metric_value(summary411, "phase411_cost200_acceptance_survivor_rows", 0))
    failed_count = int(len(gates411.loc[gates411["passed"].astype(str).str.lower().isin(["false", "0"])]))
    synthetic_scan_points = as_int(attribution.loc[attribution["attribution_id"].eq("synthetic_scan_points"), "value"].iloc[0])
    gates = [
        ("P412_PHASE411_COMPLETE", complete == 1, complete, 1),
        ("P412_PHASE411_GATES_EVALUATED", len(gates411) == 20, len(gates411), 20),
        ("P412_FAILURE_BASIS_PRESENT", failed_count > 0, failed_count, ">0"),
        ("P412_ZERO_EVENT_FORM_CONFIRMED", primary_trades == 0, primary_trades, 0),
        ("P412_INPUT_SCAN_NONEMPTY", synthetic_scan_points > 0, synthetic_scan_points, ">0"),
        ("P412_NO_COST200_SURVIVORS", survivors == 0, survivors, 0),
        ("P412_VERDICT_PRESENT", str(decision.loc[decision["decision_id"].eq("selected_verdict"), "decision_value"].iloc[0]) == VERDICT, VERDICT, VERDICT),
        ("P412_NO_THRESHOLD_RELAXATION", str(decision.loc[decision["decision_id"].eq("same_family_threshold_relaxation_allowed"), "decision_value"].iloc[0]) == "0", 0, 0),
        ("P412_BOUNDARIES_CLOSED", str(decision.loc[decision["decision_id"].eq("paper_or_live_acceptance_allowed"), "decision_value"].iloc[0]) == "0", "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(summary411: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase412_replenishment_breakout_interpretation_complete", 1, "Phase412 interpretation completed"),
            ("phase412_selected_verdict", VERDICT, "Selected verdict"),
            ("phase412_phase411_primary_completed_round_trips", metric_value(summary411, "phase411_primary_completed_round_trips", 0), "Phase411 primary round trips"),
            ("phase412_phase411_primary_annualized_return_pct", metric_value(summary411, "phase411_primary_annualized_return_pct", 0), "Phase411 primary annualized return"),
            ("phase412_cost200_acceptance_survivor_rows", metric_value(summary411, "phase411_cost200_acceptance_survivor_rows", 0), "Acceptance survivors"),
            ("phase412_same_family_threshold_relaxation_allowed", 0, "No threshold relaxation"),
            ("phase412_strategy_promotion_allowed", 0, "No promotion"),
            ("phase412_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase412_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase412_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase412_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase412_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, decision: pd.DataFrame, attribution: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase412 Replenishment Breakout Interpretation",
        "",
        "Phase412 formally interprets the Phase411 zero-trade execution result.",
        "",
        "The Phase410/P411 replenishment-breakout form is rejected as too sparse in the bounded execution shard. Zero trades is not a profitability success.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Decision Ledger",
        "",
        _markdown_table(decision),
        "",
        "## Failure Attribution",
        "",
        _markdown_table(attribution),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: do not relax Phase410 thresholds after observing the zero-event result.",
    ]
    (output_dir / "phase412_replenishment_breakout_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase410_dir: Path = DEFAULT_PHASE410_DIR, phase411_dir: Path = DEFAULT_PHASE411_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    summary411 = read_csv(phase411_dir / "phase411_acceptance_summary.csv")
    gates411 = read_csv(phase411_dir / "phase411_gate_evaluation.csv")
    synthetic_diag = read_csv(phase411_dir / "phase411_synthetic_scan_diagnostics.csv")
    real_diag = read_csv(phase411_dir / "phase411_real_anchor_scan_diagnostics.csv")
    if summary411.empty or gates411.empty or synthetic_diag.empty:
        raise FileNotFoundError("Phase412 requires Phase411 summary, gate evaluation and diagnostics.")
    decision = build_decision_ledger(summary411, gates411, synthetic_diag)
    attribution = build_failure_attribution(summary411, synthetic_diag, real_diag)
    gates = build_gate_evaluation(summary411, gates411, decision, attribution)
    acceptance = build_acceptance(summary411, gates)
    decision.to_csv(output_dir / "phase412_decision_ledger.csv", index=False)
    attribution.to_csv(output_dir / "phase412_failure_attribution.csv", index=False)
    gates.to_csv(output_dir / "phase412_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase412_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, decision, attribution, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase412_replenishment_breakout_interpretation",
        **reproducibility_fields(
            artifact_id="phase412_replenishment_breakout_interpretation",
            generated_utc=generated_utc,
            inputs={
                "phase410_acceptance_summary": str(phase410_dir / "phase410_acceptance_summary.csv"),
                "phase411_acceptance_summary": str(phase411_dir / "phase411_acceptance_summary.csv"),
                "phase411_gate_evaluation": str(phase411_dir / "phase411_gate_evaluation.csv"),
                "phase411_synthetic_scan_diagnostics": str(phase411_dir / "phase411_synthetic_scan_diagnostics.csv"),
            },
            parameters={"selected_verdict": VERDICT, "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase412_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase411_taker_next_tick_order_arrival",
        ),
    }
    (output_dir / "phase412_replenishment_breakout_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase412 replenishment-breakout interpretation.")
    parser.add_argument("--phase410-dir", type=Path, default=DEFAULT_PHASE410_DIR)
    parser.add_argument("--phase411-dir", type=Path, default=DEFAULT_PHASE411_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase410_dir, args.phase411_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
