from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE210_DIR = Path("outputs/phase210")
DEFAULT_OUTPUT_DIR = Path("outputs/phase211")
FORBIDDEN_OUTPUTS = "strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export"
NEXT_ACTION = "run_phase212_model_family_closure_or_redesign_precommit_no_replay_no_test"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = "") -> Any:
    if frame.empty or "metric" not in frame.columns or "value" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def build_validation_interpretation(metrics: pd.DataFrame, controls: pd.DataFrame) -> pd.DataFrame:
    if metrics.empty:
        return pd.DataFrame()
    validation = metrics[metrics["split_role"].astype(str).eq("validation")].copy()
    controls = controls.copy()
    controls["phase210_model_fit_id"] = controls["phase210_control_id"].astype(str).str.replace("P210_SHUFFLED_", "P210_", regex=False)
    controls = controls.rename(columns={"validation_mse": "control_validation_mse", "validation_binary_accuracy": "control_validation_binary_accuracy"})
    joined = validation.merge(
        controls[["phase210_model_fit_id", "control_validation_mse", "control_validation_binary_accuracy"]],
        on="phase210_model_fit_id",
        how="left",
    )
    joined["validation_mse"] = pd.to_numeric(joined["mse"], errors="coerce")
    joined["control_validation_mse"] = pd.to_numeric(joined["control_validation_mse"], errors="coerce")
    joined["mse_improvement_pct_vs_control"] = ((joined["control_validation_mse"] - joined["validation_mse"]) / joined["control_validation_mse"] * 100.0).fillna(0.0)
    joined["validation_correlation"] = pd.to_numeric(joined["correlation"], errors="coerce").fillna(0.0)
    joined["validation_binary_accuracy"] = pd.to_numeric(joined["binary_accuracy"], errors="coerce")
    joined["control_validation_binary_accuracy"] = pd.to_numeric(joined["control_validation_binary_accuracy"], errors="coerce")
    joined["binary_accuracy_lift_vs_control"] = (joined["validation_binary_accuracy"] - joined["control_validation_binary_accuracy"]).fillna(0.0)
    rows: list[dict[str, Any]] = []
    for record in joined.to_dict("records"):
        target = str(record.get("target_label", ""))
        is_binary = target in {"short_horizon_direction_label", "execution_risk_spread_widen_next_bucket"}
        mse_pass = float(record.get("mse_improvement_pct_vs_control", 0.0)) >= 1.0
        corr_pass = abs(float(record.get("validation_correlation", 0.0))) >= 0.10
        acc_pass = (not is_binary) or float(record.get("binary_accuracy_lift_vs_control", 0.0)) >= 0.005
        interpretation_pass = int(mse_pass and corr_pass and acc_pass)
        if interpretation_pass:
            verdict = "diagnostic_signal_survives_control_screen_but_replay_still_closed"
        elif not mse_pass:
            verdict = "rejected_control_like_or_worse_mse"
        elif is_binary and not acc_pass:
            verdict = "rejected_accuracy_base_rate_control_like"
        else:
            verdict = "rejected_insufficient_validation_correlation"
        rows.append(
            {
                "phase211_interpretation_id": str(record.get("phase210_model_fit_id", "")).replace("P210_", "P211_"),
                "phase210_model_fit_id": record.get("phase210_model_fit_id", ""),
                "phase209_model_spec_id": record.get("phase209_model_spec_id", ""),
                "target_label": target,
                "horizon_sec": as_int(record.get("horizon_sec", 0)),
                "validation_rows": as_int(record.get("rows", 0)),
                "validation_mse": record.get("validation_mse", ""),
                "control_validation_mse": record.get("control_validation_mse", ""),
                "mse_improvement_pct_vs_control": record.get("mse_improvement_pct_vs_control", 0.0),
                "validation_correlation": record.get("validation_correlation", 0.0),
                "validation_binary_accuracy": record.get("validation_binary_accuracy", ""),
                "control_validation_binary_accuracy": record.get("control_validation_binary_accuracy", ""),
                "binary_accuracy_lift_vs_control": record.get("binary_accuracy_lift_vs_control", 0.0),
                "mse_improvement_pass": int(mse_pass),
                "correlation_pass": int(corr_pass),
                "binary_accuracy_lift_pass": int(acc_pass),
                "interpretation_pass": interpretation_pass,
                "verdict": verdict,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "profitability_claim_allowed": 0,
            }
        )
    return pd.DataFrame(rows)


def build_family_summary(interpretation: pd.DataFrame) -> pd.DataFrame:
    if interpretation.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for spec_id, part in interpretation.groupby("phase209_model_spec_id", sort=True):
        pass_rows = int(part["interpretation_pass"].astype(int).sum())
        best_mse = float(pd.to_numeric(part["mse_improvement_pct_vs_control"], errors="coerce").max())
        best_corr = float(pd.to_numeric(part["validation_correlation"], errors="coerce").abs().max())
        best_acc_lift = float(pd.to_numeric(part["binary_accuracy_lift_vs_control"], errors="coerce").fillna(0.0).max())
        rows.append(
            {
                "phase211_family_summary_id": f"P211_FAMILY_{spec_id}",
                "phase209_model_spec_id": spec_id,
                "interpreted_horizon_rows": len(part),
                "passing_interpretation_rows": pass_rows,
                "best_mse_improvement_pct_vs_control": best_mse,
                "best_abs_validation_correlation": best_corr,
                "best_binary_accuracy_lift_vs_control": best_acc_lift,
                "family_verdict": "closed_for_replay_redesign_required" if pass_rows == 0 else "diagnostic_survivor_precommit_required_no_replay",
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            }
        )
    return pd.DataFrame(rows)


def build_decision_ledger(interpretation: pd.DataFrame, family_summary: pd.DataFrame) -> pd.DataFrame:
    pass_rows = int(interpretation["interpretation_pass"].astype(int).sum()) if not interpretation.empty else 0
    return pd.DataFrame(
        [
            {
                "phase211_decision_id": "P211_VALIDATION_INTERPRETATION_DECISION",
                "passing_interpretation_rows": pass_rows,
                "model_families_with_pass": int(family_summary["passing_interpretation_rows"].astype(int).gt(0).sum()) if not family_summary.empty else 0,
                "decision": "no_candidate_opened_for_replay" if pass_rows == 0 else "diagnostic_candidate_requires_future_precommit_before_any_replay",
                "rationale": "Validation dry-run metrics are compared with shuffled-target controls; replay and sealed test remain closed regardless of interpretation.",
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "profitability_claim_allowed": 0,
            }
        ]
    )


def build_forbidden_execution_ledger() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "forbidden_output": item,
                "emitted_in_phase211": 0,
                "allowed_in_phase211": 0,
                "rationale": "Phase211 interprets aggregate validation metrics only and keeps replay, test, P&L, promotion, and paper/live closed.",
            }
            for item in FORBIDDEN_OUTPUTS.split(";")
        ]
    )


def build_gates(phase210: pd.DataFrame, interpretation: pd.DataFrame, family_summary: pd.DataFrame, decision: pd.DataFrame, forbidden: pd.DataFrame) -> pd.DataFrame:
    phase210_complete = as_int(metric_value(phase210, "phase210_train_validation_model_fit_dry_run_complete", 0))
    replay_flags = 0
    for frame in [interpretation, family_summary, decision]:
        for col in ["strategy_replay_allowed", "test_replay_allowed_next", "promotion_allowed", "paper_or_live_acceptance_allowed", "profitability_claim_allowed"]:
            if not frame.empty and col in frame.columns:
                replay_flags += int(pd.to_numeric(frame[col], errors="coerce").fillna(0).sum())
    forbidden_emitted = int(forbidden["emitted_in_phase211"].astype(int).sum()) if not forbidden.empty else 1
    return pd.DataFrame(
        [
            ("P211_PHASE210_COMPLETE", phase210_complete == 1, f"phase210_complete={phase210_complete}", "hard"),
            ("P211_INTERPRETATION_ROWS_RECORDED", len(interpretation) == 12, f"interpretation_rows={len(interpretation)}", "hard"),
            ("P211_FAMILY_SUMMARY_RECORDED", len(family_summary) == 3, f"family_summary_rows={len(family_summary)}", "hard"),
            ("P211_DECISION_LEDGER_RECORDED", len(decision) == 1, f"decision_rows={len(decision)}", "hard"),
            ("P211_FORBIDDEN_OUTPUTS_CLEAN", forbidden_emitted == 0 and replay_flags == 0, f"forbidden_emitted={forbidden_emitted}; replay_flags={replay_flags}", "hard"),
            ("P211_NO_TEST_REPLAY_OR_PROFITABILITY_CLAIM", replay_flags == 0, f"closed_flags_sum={replay_flags}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(interpretation: pd.DataFrame, family_summary: pd.DataFrame, decision: pd.DataFrame, forbidden: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    pass_rows = int(interpretation["interpretation_pass"].astype(int).sum()) if not interpretation.empty else 0
    best_mse = float(pd.to_numeric(interpretation["mse_improvement_pct_vs_control"], errors="coerce").max()) if not interpretation.empty else 0.0
    best_corr = float(pd.to_numeric(interpretation["validation_correlation"], errors="coerce").abs().max()) if not interpretation.empty else 0.0
    best_acc_lift = float(pd.to_numeric(interpretation["binary_accuracy_lift_vs_control"], errors="coerce").fillna(0.0).max()) if not interpretation.empty else 0.0
    return pd.DataFrame(
        [
            ("phase211_interpretation_rows", len(interpretation), "Model/horizon interpretation rows"),
            ("phase211_family_summary_rows", len(family_summary), "Model-family summary rows"),
            ("phase211_passing_interpretation_rows", pass_rows, "Rows passing the control-aware interpretation screen"),
            ("phase211_best_mse_improvement_pct_vs_control", best_mse, "Best validation MSE improvement versus shuffled-target control"),
            ("phase211_best_abs_validation_correlation", best_corr, "Best absolute validation correlation"),
            ("phase211_best_binary_accuracy_lift_vs_control", best_acc_lift, "Best binary accuracy lift versus shuffled-target control"),
            ("phase211_decision_rows", len(decision), "Decision ledger rows"),
            ("phase211_forbidden_execution_rows", len(forbidden), "Forbidden execution rows"),
            ("phase211_gate_rows", len(gates), "Gates evaluated"),
            ("phase211_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase211_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase211_model_fit_validation_interpretation_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase211 completed"),
            ("phase211_candidate_opened_for_replay", 0, "No candidate opened for replay"),
            ("phase211_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase211_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase211_promotion_allowed", 0, "No promotion opened"),
            ("phase211_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase211_profitability_claim_allowed", 0, "No profitability claim is allowed"),
            ("phase211_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase211_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase211 Model-fit Validation Interpretation",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase211 interprets Phase210 aggregate validation metrics against shuffled-target controls.",
        "It does not use sealed test data, run replay, export row-level predictions, emit P&L, promote candidates, or make profitability claims.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase211_model_fit_validation_interpretation_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase211(phase210_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase210 = read_csv(phase210_dir / "phase210_train_validation_model_fit_acceptance_summary.csv")
    metrics = read_csv(phase210_dir / "phase210_train_validation_model_metrics.csv")
    controls = read_csv(phase210_dir / "phase210_negative_control_metrics.csv")
    interpretation = build_validation_interpretation(metrics, controls)
    family_summary = build_family_summary(interpretation)
    decision = build_decision_ledger(interpretation, family_summary)
    forbidden = build_forbidden_execution_ledger()
    gates = build_gates(phase210, interpretation, family_summary, decision, forbidden)
    acceptance = build_acceptance(interpretation, family_summary, decision, forbidden, gates)

    interpretation.to_csv(output_dir / "phase211_validation_interpretation.csv", index=False)
    family_summary.to_csv(output_dir / "phase211_family_interpretation_summary.csv", index=False)
    decision.to_csv(output_dir / "phase211_decision_ledger.csv", index=False)
    forbidden.to_csv(output_dir / "phase211_execution_forbidden_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase211_model_fit_validation_interpretation_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase211_model_fit_validation_interpretation_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Validation Interpretation": interpretation,
            "Family Summary": family_summary,
            "Decision Ledger": decision,
            "Forbidden Execution Ledger": forbidden,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase211_model_fit_validation_interpretation_no_replay_no_test",
        **reproducibility_fields(
            artifact_id="phase211_model_fit_validation_interpretation",
            generated_utc=generated,
            inputs={
                "phase210_acceptance": str(phase210_dir / "phase210_train_validation_model_fit_acceptance_summary.csv"),
                "phase210_metrics": str(phase210_dir / "phase210_train_validation_model_metrics.csv"),
                "phase210_negative_controls": str(phase210_dir / "phase210_negative_control_metrics.csv"),
            },
            parameters={
                "minimum_mse_improvement_pct_vs_control": "1.0",
                "minimum_abs_validation_correlation": "0.10",
                "minimum_binary_accuracy_lift_vs_control": "0.005",
                "strategy_replay_allowed": "0",
                "test_replay_allowed_next": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "interpretation": str(output_dir / "phase211_validation_interpretation.csv"),
                "family_summary": str(output_dir / "phase211_family_interpretation_summary.csv"),
                "decision": str(output_dir / "phase211_decision_ledger.csv"),
                "forbidden": str(output_dir / "phase211_execution_forbidden_ledger.csv"),
                "gates": str(output_dir / "phase211_model_fit_validation_interpretation_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase211_model_fit_validation_interpretation_acceptance_summary.csv"),
                "report": str(output_dir / "phase211_model_fit_validation_interpretation_report.md"),
            },
            scenario_ids="phase211_model_fit_validation_interpretation_no_replay_no_test",
            cost_model_version="not_applicable_no_replay",
            latency_model_version="not_applicable_no_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase211_model_fit_validation_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase211 validation interpretation without replay/test.")
    parser.add_argument("--phase210-dir", type=Path, default=DEFAULT_PHASE210_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase211(args.phase210_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
