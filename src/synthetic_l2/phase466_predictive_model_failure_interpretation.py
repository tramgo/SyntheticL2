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
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE465_DIR = Path("outputs/phase465")
DEFAULT_OUTPUT_DIR = Path("outputs/phase466")

THESIS_ID = "P466_PREDICTIVE_MODEL_FAILURE_INTERPRETATION"
VERDICT = "P466_WEAK_PREDICTIVE_SMELL_NOT_REPLAYABLE"
NEXT_ACTION = "precommit_phase467_richer_past_only_l1_l5_feature_matrix_before_any_replay"

REQUIRED_FAILED_GATE = "P465_AUC_LIFT_VS_SHUFFLED_GE_002"
REJECTED_NEXT_ACTION = "run_phase466_score_to_signal_replay_from_phase465_model"


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def gate_row(gates: pd.DataFrame, gate_id: str) -> pd.Series:
    rows = gates.loc[gates["gate_id"].astype(str).eq(gate_id)]
    if rows.empty:
        return pd.Series(dtype=object)
    return rows.iloc[0]


def build_decision(acceptance: pd.DataFrame, gates: pd.DataFrame, model_summary: pd.DataFrame) -> pd.DataFrame:
    failed = gates.loc[~gates["passed"].astype(bool)].copy()
    primary = model_summary.loc[model_summary["model_id"].astype(str).eq("P465_PRIMARY_CLASS_WEIGHTED_LOGISTIC_L1_L5")].iloc[0]
    shuffled = model_summary.loc[model_summary["model_id"].astype(str).eq("P465_SHUFFLED_LABEL_CONTROL")].iloc[0]
    threshold = model_summary.loc[model_summary["model_id"].astype(str).eq("P465_L25_THRESHOLD_CONTROL")].iloc[0]
    rows = [
        ("selected_verdict", VERDICT, "Phase465 has weak predictive signal but fails the shuffled-label lift gate."),
        ("primary_holdout_auc", float(primary["auc"]), "Primary holdout AUC."),
        ("primary_holdout_balanced_accuracy", float(primary["balanced_accuracy"]), "Primary holdout balanced accuracy."),
        ("shuffled_holdout_auc", float(shuffled["auc"]), "Shuffled-label control holdout AUC."),
        ("auc_lift_vs_shuffled", scalar(acceptance, "phase465_auc_lift_vs_shuffled", ""), "Primary AUC lift versus shuffled-label control."),
        ("l25_threshold_holdout_auc", float(threshold["auc"]), "Single L2-L5 threshold control holdout AUC."),
        ("failed_gate_count", int(len(failed)), "Failed Phase465 hard gates."),
        ("failed_gate_ids", ";".join(failed["gate_id"].astype(str).tolist()), "Failed Phase465 gate ids."),
        ("score_to_signal_replay_allowed", 0, "Phase465 did not allow Phase466 replay."),
        ("same_five_feature_model_rescue_allowed", 0, "Do not retune the same weak feature set after seeing holdout controls."),
        ("materially_richer_past_only_features_allowed", 1, "A new precommitted matrix may add richer past-only L1-L5 window features."),
        ("strategy_promotion_allowed", 0, "No promotion."),
        ("paper_or_live_acceptance_allowed", 0, "No paper/live."),
        ("deployable_profitability_claim_allowed", 0, "No deployable claim."),
    ]
    return pd.DataFrame(rows, columns=["decision_id", "decision_value", "description"])


def richer_feature_plan() -> pd.DataFrame:
    rows = [
        ("depth_curve_shape", "past_only_window", "Use L1-L5 bid/ask ladder slope, convexity and depth concentration over the lookback window.", 1),
        ("ofi_and_depth_churn", "past_only_window", "Use signed changes in L1-L5 quantities and replenishment/withdrawal counts before entry.", 1),
        ("microprice_pressure", "past_only_window", "Use L1 and L2-L5 microprice displacement from mid, computed before entry.", 1),
        ("spread_regime_context", "past_only_window", "Use rolling spread percentile, spread compression/expansion and tight/loose regime flags.", 0),
        ("volume_acceleration", "past_only_window", "Use rolling trade-volume acceleration and volume imbalance proxies before entry.", 0),
        ("time_of_day_context", "known_before_entry", "Use open/midday/close bucket only, not future session outcomes.", 0),
        ("symbol_normalization", "known_before_entry", "Normalize features within symbol/train split to avoid large-price or large-volume domination.", 0),
    ]
    return pd.DataFrame(rows, columns=["feature_family", "timestamp_rule", "description", "uses_l2_l5_depth"])


def build_gates(acceptance: pd.DataFrame, gates: pd.DataFrame, decision: pd.DataFrame) -> pd.DataFrame:
    failed_gate = gate_row(gates, REQUIRED_FAILED_GATE)
    failed_gate_is_failed = (not failed_gate.empty) and (not bool(failed_gate["passed"]))
    hard_failed = int((~gates["passed"].astype(bool)).sum()) if not gates.empty else 0
    decision_values = dict(zip(decision["decision_id"].astype(str), decision["decision_value"]))
    gate_rows = [
        ("P466_PHASE465_COMPLETE", as_int(scalar(acceptance, "phase465_train_holdout_past_only_l1_l5_label_model_complete", 0)) == 1, scalar(acceptance, "phase465_train_holdout_past_only_l1_l5_label_model_complete", 0), 1),
        ("P466_PHASE465_REPLAY_NOT_ALLOWED", as_int(scalar(acceptance, "phase465_phase466_allowed_next", 1)) == 0, scalar(acceptance, "phase465_phase466_allowed_next", 1), 0),
        ("P466_REQUIRED_FAILED_GATE_IDENTIFIED", failed_gate_is_failed, REQUIRED_FAILED_GATE if failed_gate_is_failed else "", REQUIRED_FAILED_GATE),
        ("P466_EXACTLY_ONE_PREDICTIVE_GATE_FAILED", hard_failed == 1, hard_failed, 1),
        ("P466_REPLAY_REJECTED", as_int(decision_values.get("score_to_signal_replay_allowed", 1)) == 0, decision_values.get("score_to_signal_replay_allowed", ""), 0),
        ("P466_SAME_MODEL_RESCUE_REJECTED", as_int(decision_values.get("same_five_feature_model_rescue_allowed", 1)) == 0, decision_values.get("same_five_feature_model_rescue_allowed", ""), 0),
        ("P466_RICHER_PAST_ONLY_FEATURES_SELECTED", as_int(decision_values.get("materially_richer_past_only_features_allowed", 0)) == 1, decision_values.get("materially_richer_past_only_features_allowed", ""), 1),
        ("P466_NO_STRATEGY_PNL", True, "interpretation_only", "no_pnl"),
        ("P466_NO_PAPER_LIVE_OR_CLAIM", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gate_rows])


def build_acceptance(gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    all_pass = int(hard_pass == hard_rows)
    rows = [
        ("phase466_predictive_model_failure_interpretation_complete", 1, "Phase466 interpretation completed"),
        ("phase466_thesis_id", THESIS_ID, "Interpretation thesis"),
        ("phase466_selected_verdict", VERDICT, "Selected verdict"),
        ("phase466_score_to_signal_replay_allowed", 0, "No replay from Phase465 model"),
        ("phase466_same_five_feature_model_rescue_allowed", 0, "No same-model rescue"),
        ("phase466_richer_past_only_feature_precommit_allowed", all_pass, "Allows Phase467 precommit only"),
        ("phase466_strategy_pnl_generated", 0, "No strategy P&L"),
        ("phase466_strategy_promotion_allowed", 0, "No promotion"),
        ("phase466_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase466_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase466_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase466_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase466_next_best_action", NEXT_ACTION if all_pass else "pause_and_reconcile_phase465_failure_evidence", "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, decision: pd.DataFrame, feature_plan: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase466 Predictive Model Failure Interpretation",
        "",
        "Phase466 interprets Phase465 and blocks score-to-signal replay from the weak five-feature model.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Decision Ledger",
        "",
        _markdown_table(decision),
        "",
        "## Richer Past-Only Feature Plan",
        "",
        _markdown_table(feature_plan),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase466 is interpretation only. A richer feature matrix must be precommitted before any additional model fit or P&L replay.",
    ]
    (output_dir / "phase466_predictive_model_failure_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase465_dir: Path = DEFAULT_PHASE465_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    acceptance_in = read_csv(phase465_dir / "phase465_acceptance_summary.csv")
    gates_in = read_csv(phase465_dir / "phase465_gate_evaluation.csv")
    model_summary = read_csv(phase465_dir / "phase465_model_summary.csv")
    decision = build_decision(acceptance_in, gates_in, model_summary)
    feature_plan = richer_feature_plan()
    gates = build_gates(acceptance_in, gates_in, decision)
    acceptance = build_acceptance(gates)
    decision.to_csv(output_dir / "phase466_decision_ledger.csv", index=False)
    feature_plan.to_csv(output_dir / "phase466_richer_past_only_feature_plan.csv", index=False)
    gates.to_csv(output_dir / "phase466_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase466_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, decision, feature_plan, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase466_predictive_model_failure_interpretation",
        **reproducibility_fields(
            artifact_id="phase466_predictive_model_failure_interpretation",
            generated_utc=generated_utc,
            inputs={"phase465_acceptance_summary": str(phase465_dir / "phase465_acceptance_summary.csv")},
            parameters={"thesis_id": THESIS_ID, "verdict": VERDICT, "rejected_next_action": REJECTED_NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase466_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase466_interpretation_no_execution",
        ),
    }
    (output_dir / "phase466_predictive_model_failure_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase466 predictive model failure interpretation.")
    parser.add_argument("--phase465-dir", type=Path, default=DEFAULT_PHASE465_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    out = run(args.phase465_dir, args.output_dir)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
