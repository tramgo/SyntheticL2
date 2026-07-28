from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE219_DIR = Path("outputs/phase219")
DEFAULT_OUTPUT_DIR = Path("outputs/phase220")
MIN_VALIDATION_ROWS = 10_000
MIN_MSE_IMPROVEMENT_VS_BASE = 0.003
MIN_MSE_IMPROVEMENT_VS_SHUFFLE = 0.0005
MIN_VALIDATION_CORRELATION = 0.10
FORBIDDEN_OUTPUTS = "strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export"
NEXT_ACTION = "run_phase221_event_only_signal_replay_precommit_or_stop_no_replay_no_test"


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


def build_interpretation(metrics: pd.DataFrame, controls: pd.DataFrame) -> pd.DataFrame:
    if metrics.empty:
        return pd.DataFrame()
    validation = metrics[metrics["split_role"].astype(str).eq("validation")].copy()
    base = controls[controls["control_type"].astype(str).eq("event_only_base_rate")][["phase219_model_fit_id", "validation_mse"]].rename(columns={"validation_mse": "base_control_mse"}) if not controls.empty else pd.DataFrame()
    shuffle = controls[controls["control_type"].astype(str).eq("event_time_shuffle")][["phase219_model_fit_id", "validation_mse"]].rename(columns={"validation_mse": "shuffle_control_mse"}) if not controls.empty else pd.DataFrame()
    if not base.empty:
        validation = validation.merge(base, on="phase219_model_fit_id", how="left")
    if not shuffle.empty:
        validation = validation.merge(shuffle, on="phase219_model_fit_id", how="left")
    for col in ["rows", "mse", "base_rate_mse", "mse_improvement_vs_base", "binary_accuracy", "correlation", "base_control_mse", "shuffle_control_mse"]:
        if col in validation.columns:
            validation[col] = pd.to_numeric(validation[col], errors="coerce")
    validation["improvement_vs_shuffle"] = validation["shuffle_control_mse"] - validation["mse"]
    validation["passes_min_rows"] = (validation["rows"] >= MIN_VALIDATION_ROWS).astype(int)
    validation["passes_base_improvement"] = (validation["mse_improvement_vs_base"] >= MIN_MSE_IMPROVEMENT_VS_BASE).astype(int)
    validation["passes_shuffle_improvement"] = (validation["improvement_vs_shuffle"] >= MIN_MSE_IMPROVEMENT_VS_SHUFFLE).astype(int)
    validation["passes_correlation"] = (validation["correlation"] >= MIN_VALIDATION_CORRELATION).astype(int)
    pass_cols = ["passes_min_rows", "passes_base_improvement", "passes_shuffle_improvement", "passes_correlation"]
    validation["interpretation_pass"] = validation[pass_cols].min(axis=1).astype(int)
    validation["candidate_opened_for_phase221_precommit"] = validation["interpretation_pass"]
    validation["strategy_replay_allowed"] = 0
    validation["test_replay_allowed_next"] = 0
    validation["promotion_allowed"] = 0
    validation["profitability_claim_allowed"] = 0
    validation["verdict"] = validation.apply(lambda r: "phase221_precommit_candidate" if int(r["interpretation_pass"]) == 1 else "insufficient_validation_edge_or_control_failure", axis=1)
    return validation.sort_values(["interpretation_pass", "mse_improvement_vs_base"], ascending=[False, False]).reset_index(drop=True)


def build_family_summary(interpretation: pd.DataFrame) -> pd.DataFrame:
    if interpretation.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for family, part in interpretation.groupby("model_family", sort=True):
        passing = part[pd.to_numeric(part["interpretation_pass"], errors="coerce").fillna(0).astype(int).eq(1)]
        rows.append(
            {
                "model_family": family,
                "validation_rows": len(part),
                "passing_validation_rows": len(passing),
                "best_mse_improvement_vs_base": float(pd.to_numeric(part["mse_improvement_vs_base"], errors="coerce").max()),
                "best_improvement_vs_shuffle": float(pd.to_numeric(part["improvement_vs_shuffle"], errors="coerce").max()),
                "best_correlation": float(pd.to_numeric(part["correlation"], errors="coerce").max()),
                "candidate_family_for_phase221": int(len(passing) > 0),
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            }
        )
    return pd.DataFrame(rows)


def build_phase221_work_order(interpretation: pd.DataFrame) -> pd.DataFrame:
    passing = interpretation[pd.to_numeric(interpretation["interpretation_pass"], errors="coerce").fillna(0).astype(int).eq(1)] if not interpretation.empty else pd.DataFrame()
    candidate_ids = ";".join(passing["phase219_model_fit_id"].astype(str).tolist()) if not passing.empty else ""
    return pd.DataFrame(
        [
            {
                "phase221_work_order_id": "P221_EVENT_ONLY_SIGNAL_REPLAY_PRECOMMIT_OR_STOP",
                "work_order": "Decide whether the Phase220 passing validation candidates can be converted into a replay precommit contract, or stop/redesign without replay.",
                "passing_candidate_rows": len(passing),
                "candidate_model_fit_ids": candidate_ids,
                "allowed_next_scope": "signal_replay_precommit_decision_only_no_replay_no_test",
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "profitability_claim_allowed": 0,
            }
        ]
    )


def build_forbidden_execution_ledger() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "forbidden_output": item,
                "emitted_in_phase220": 0,
                "allowed_in_phase220": 0,
                "rationale": "Phase220 interprets validation metrics only and emits no replay, test, promotion, P&L, prediction export, or profitability artifact.",
            }
            for item in FORBIDDEN_OUTPUTS.split(";")
        ]
    )


def build_gates(phase219: pd.DataFrame, interpretation: pd.DataFrame, summary: pd.DataFrame, work_order: pd.DataFrame, forbidden: pd.DataFrame) -> pd.DataFrame:
    phase219_complete = as_int(metric_value(phase219, "phase219_event_only_train_validation_model_fit_dry_run_complete", 0))
    validation_rows = len(interpretation)
    passing_rows = int(pd.to_numeric(interpretation["interpretation_pass"], errors="coerce").fillna(0).sum()) if not interpretation.empty else 0
    candidate_families = int(pd.to_numeric(summary["candidate_family_for_phase221"], errors="coerce").fillna(0).sum()) if not summary.empty else 0
    forbidden_emitted = int(pd.to_numeric(forbidden["emitted_in_phase220"], errors="coerce").fillna(0).sum()) if not forbidden.empty else 1
    replay_flags = 0
    for frame in [interpretation, summary, work_order]:
        for col in ["strategy_replay_allowed", "test_replay_allowed_next", "promotion_allowed", "profitability_claim_allowed"]:
            if not frame.empty and col in frame.columns:
                replay_flags += int(pd.to_numeric(frame[col], errors="coerce").fillna(0).sum())
    return pd.DataFrame(
        [
            ("P220_PHASE219_COMPLETE", phase219_complete == 1, f"phase219_complete={phase219_complete}", "hard"),
            ("P220_VALIDATION_INTERPRETATION_RECORDED", validation_rows == 21, f"validation_rows={validation_rows}", "hard"),
            ("P220_PASSING_CANDIDATES_RECORDED", passing_rows > 0, f"passing_rows={passing_rows}", "hard"),
            ("P220_CANDIDATE_FAMILY_RECORDED", candidate_families > 0, f"candidate_families={candidate_families}", "hard"),
            ("P220_PHASE221_WORK_ORDER_RECORDED", len(work_order) == 1, f"work_order_rows={len(work_order)}", "hard"),
            ("P220_FORBIDDEN_OUTPUTS_CLEAN", forbidden_emitted == 0 and replay_flags == 0, f"forbidden_emitted={forbidden_emitted}; replay_flags={replay_flags}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(interpretation: pd.DataFrame, summary: pd.DataFrame, work_order: pd.DataFrame, forbidden: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    passing = interpretation[pd.to_numeric(interpretation["interpretation_pass"], errors="coerce").fillna(0).astype(int).eq(1)] if not interpretation.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("phase220_interpretation_rows", len(interpretation), "Validation interpretation rows"),
            ("phase220_passing_candidate_rows", len(passing), "Passing validation candidate rows"),
            ("phase220_candidate_family_rows", int(pd.to_numeric(summary["candidate_family_for_phase221"], errors="coerce").fillna(0).sum()) if not summary.empty else 0, "Candidate model families"),
            ("phase220_best_mse_improvement_vs_base", float(pd.to_numeric(interpretation["mse_improvement_vs_base"], errors="coerce").max()) if not interpretation.empty else 0.0, "Best validation MSE improvement versus base rate"),
            ("phase220_best_improvement_vs_shuffle", float(pd.to_numeric(interpretation["improvement_vs_shuffle"], errors="coerce").max()) if not interpretation.empty else 0.0, "Best validation MSE improvement versus shuffled control"),
            ("phase220_best_validation_correlation", float(pd.to_numeric(interpretation["correlation"], errors="coerce").max()) if not interpretation.empty else 0.0, "Best validation correlation"),
            ("phase220_phase221_work_order_rows", len(work_order), "Phase221 work-order rows"),
            ("phase220_forbidden_execution_rows", len(forbidden), "Forbidden execution rows"),
            ("phase220_gate_rows", len(gates), "Gates evaluated"),
            ("phase220_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase220_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase220_event_only_model_fit_validation_interpretation_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase220 completed"),
            ("phase220_candidate_opened_for_phase221_precommit", int(len(passing) > 0), "1 means Phase221 may precommit or stop a signal/replay contract"),
            ("phase220_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase220_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase220_promotion_allowed", 0, "No promotion opened"),
            ("phase220_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase220_profitability_claim_allowed", 0, "No profitability claim is allowed"),
            ("phase220_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase220_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase220 Event-only Model-fit Validation Interpretation",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase220 interprets Phase219 validation dry-run metrics against base-rate and shuffled controls.",
        "It opens only a Phase221 precommit-or-stop decision for the passing candidates; no replay, sealed test, promotion, paper/live, or profitability claim is opened.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase220_event_only_model_fit_validation_interpretation_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase220(phase219_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase219 = read_csv(phase219_dir / "phase219_model_fit_acceptance_summary.csv")
    metrics = read_csv(phase219_dir / "phase219_train_validation_model_metrics.csv")
    controls = read_csv(phase219_dir / "phase219_control_metrics.csv")
    interpretation = build_interpretation(metrics, controls)
    summary = build_family_summary(interpretation)
    work_order = build_phase221_work_order(interpretation)
    forbidden = build_forbidden_execution_ledger()
    gates = build_gates(phase219, interpretation, summary, work_order, forbidden)
    acceptance = build_acceptance(interpretation, summary, work_order, forbidden, gates)

    interpretation.to_csv(output_dir / "phase220_validation_interpretation.csv", index=False)
    summary.to_csv(output_dir / "phase220_model_family_summary.csv", index=False)
    work_order.to_csv(output_dir / "phase220_phase221_work_order.csv", index=False)
    forbidden.to_csv(output_dir / "phase220_execution_forbidden_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase220_validation_interpretation_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase220_validation_interpretation_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Validation Interpretation": interpretation,
            "Model Family Summary": summary,
            "Phase221 Work Order": work_order,
            "Forbidden Execution Ledger": forbidden,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase220_event_only_model_fit_validation_interpretation_no_replay_no_test",
        **reproducibility_fields(
            artifact_id="phase220_event_only_model_fit_validation_interpretation",
            generated_utc=generated,
            inputs={
                "phase219_acceptance": str(phase219_dir / "phase219_model_fit_acceptance_summary.csv"),
                "phase219_metrics": str(phase219_dir / "phase219_train_validation_model_metrics.csv"),
                "phase219_controls": str(phase219_dir / "phase219_control_metrics.csv"),
            },
            parameters={
                "min_validation_rows": str(MIN_VALIDATION_ROWS),
                "min_mse_improvement_vs_base": str(MIN_MSE_IMPROVEMENT_VS_BASE),
                "min_mse_improvement_vs_shuffle": str(MIN_MSE_IMPROVEMENT_VS_SHUFFLE),
                "min_validation_correlation": str(MIN_VALIDATION_CORRELATION),
                "strategy_replay_allowed": "0",
                "test_replay_allowed_next": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "interpretation": str(output_dir / "phase220_validation_interpretation.csv"),
                "summary": str(output_dir / "phase220_model_family_summary.csv"),
                "work_order": str(output_dir / "phase220_phase221_work_order.csv"),
                "forbidden": str(output_dir / "phase220_execution_forbidden_ledger.csv"),
                "gates": str(output_dir / "phase220_validation_interpretation_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase220_validation_interpretation_acceptance_summary.csv"),
                "report": str(output_dir / "phase220_event_only_model_fit_validation_interpretation_report.md"),
            },
            scenario_ids="phase220_event_only_model_fit_validation_interpretation_no_replay_no_test",
            cost_model_version="not_applicable_no_replay",
            latency_model_version="not_applicable_no_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase220_validation_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase220 event-only validation interpretation without replay/test.")
    parser.add_argument("--phase219-dir", type=Path, default=DEFAULT_PHASE219_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase220(args.phase219_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
