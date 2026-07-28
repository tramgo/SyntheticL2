from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE177_DIR = Path("outputs/phase177")
DEFAULT_PHASE207_DIR = Path("outputs/phase207")
DEFAULT_OUTPUT_DIR = Path("outputs/phase208")
FORBIDDEN_OUTPUTS = "model_fit;strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening"


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


def build_matrix_quality_summary(matrix: pd.DataFrame, partition_quality: pd.DataFrame, coverage: pd.DataFrame) -> pd.DataFrame:
    if matrix.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    coverage_pass = int(coverage["coverage_pass"].astype(int).all()) if not coverage.empty and "coverage_pass" in coverage.columns else 0
    missing_required = int(partition_quality["missing_required_columns"].fillna("").astype(str).str.strip().ne("").sum()) if not partition_quality.empty and "missing_required_columns" in partition_quality.columns else 0
    duplicate_rows = int(pd.to_numeric(partition_quality.get("duplicate_bucket_rows", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not partition_quality.empty else 0
    monotonic_violations = int(pd.to_numeric(partition_quality.get("bucket_monotonic_violations", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not partition_quality.empty else 0
    for (feature_id, horizon), part in matrix.groupby(["phase206_feature_id", "horizon_sec"], sort=True):
        available = int(part["feature_available"].astype(int).min())
        rows.append(
            {
                "quality_id": f"P208_{feature_id}_H{horizon}s",
                "phase206_feature_id": feature_id,
                "horizon_sec": horizon,
                "feature_available": available,
                "trade_dates": as_int(part["trade_dates"].max(), 0),
                "symbols": as_int(part["symbols"].max(), 0),
                "total_feature_rows": as_int(part["total_feature_rows"].max(), 0),
                "coverage_pass": coverage_pass,
                "missing_required_column_partitions": missing_required,
                "duplicate_bucket_rows": duplicate_rows,
                "bucket_monotonic_violations": monotonic_violations,
                "quality_gate_pass": int(
                    available == 1
                    and coverage_pass == 1
                    and missing_required == 0
                    and duplicate_rows == 0
                    and monotonic_violations == 0
                    and as_int(part["trade_dates"].max(), 0) >= 5
                    and as_int(part["symbols"].max(), 0) >= 32
                ),
                "model_fit_allowed": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            }
        )
    return pd.DataFrame(rows)


def build_blocking_gap_ledger(summary: pd.DataFrame, ablations: pd.DataFrame, audit: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if summary.empty:
        rows.append({"gap_id": "P208_MATRIX_MISSING", "blocking": 1, "evidence": "feature matrix missing"})
    else:
        failed = summary.loc[~summary["quality_gate_pass"].astype(int).eq(1)]
        for record in failed.to_dict("records"):
            rows.append(
                {
                    "gap_id": f"P208_QUALITY_GAP_{record.get('quality_id', '')}",
                    "blocking": 1,
                    "evidence": f"available={record.get('feature_available')}; coverage={record.get('coverage_pass')}; missing_required={record.get('missing_required_column_partitions')}; duplicate_rows={record.get('duplicate_bucket_rows')}; monotonic={record.get('bucket_monotonic_violations')}; dates={record.get('trade_dates')}; symbols={record.get('symbols')}",
                }
            )
    if ablations.empty or not ablations.get("required_before_model_fit", pd.Series(dtype=int)).astype(int).eq(1).all():
        rows.append({"gap_id": "P208_ABLATION_SPEC_INCOMPLETE", "blocking": 1, "evidence": f"ablation_rows={len(ablations)}"})
    if audit.empty or not audit.get("audit_pass", pd.Series(dtype=int)).astype(int).all():
        rows.append({"gap_id": "P208_LEAKAGE_TERMINOLOGY_AUDIT_FAILED", "blocking": 1, "evidence": f"audit_rows={len(audit)}"})
    if not rows:
        rows.append({"gap_id": "P208_NO_BLOCKING_GAPS", "blocking": 0, "evidence": "all feature-matrix quality checks passed"})
    out = pd.DataFrame(rows)
    out["model_fit_allowed"] = 0
    out["strategy_replay_allowed"] = 0
    return out


def build_gates(phase207: pd.DataFrame, summary: pd.DataFrame, gaps: pd.DataFrame, ablations: pd.DataFrame, audit: pd.DataFrame) -> pd.DataFrame:
    phase207_complete = as_int(metric_value(phase207, "phase207_feature_matrix_precommit_complete", 0))
    quality_pass_rows = int(summary["quality_gate_pass"].astype(int).sum()) if not summary.empty else 0
    blocking_gaps = int(gaps["blocking"].astype(int).sum()) if not gaps.empty else 1
    forbidden_sum = 0
    for frame in [summary, gaps, ablations, audit]:
        for col in ["model_fit_allowed", "strategy_replay_allowed", "test_replay_allowed_next"]:
            if not frame.empty and col in frame.columns:
                forbidden_sum += int(frame[col].astype(int).sum())
    return pd.DataFrame(
        [
            ("P208_PHASE207_COMPLETE", phase207_complete == 1, f"phase207_complete={phase207_complete}", "hard"),
            ("P208_QUALITY_SUMMARY_RECORDED", len(summary) >= 24, f"quality_rows={len(summary)}", "hard"),
            ("P208_ALL_MATRIX_ROWS_PASS_QUALITY", quality_pass_rows == len(summary) and len(summary) > 0, f"quality_pass_rows={quality_pass_rows}; quality_rows={len(summary)}", "hard"),
            ("P208_NO_BLOCKING_GAPS", blocking_gaps == 0, f"blocking_gaps={blocking_gaps}", "hard"),
            ("P208_ABLATION_AND_TERMINOLOGY_CONTROLS_PRESENT", len(ablations) == 3 and not audit.empty and audit["audit_pass"].astype(int).all(), f"ablation_rows={len(ablations)}; audit_rows={len(audit)}", "hard"),
            ("P208_NO_MODEL_FIT_REPLAY_OR_PROMOTION", forbidden_sum == 0, f"forbidden_flag_sum={forbidden_sum}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(summary: pd.DataFrame, gaps: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    blocking_gaps = int(gaps["blocking"].astype(int).sum()) if not gaps.empty else 1
    return pd.DataFrame(
        [
            ("phase208_quality_summary_rows", len(summary), "Feature/horizon quality rows"),
            ("phase208_quality_pass_rows", int(summary["quality_gate_pass"].astype(int).sum()) if not summary.empty else 0, "Feature/horizon quality rows passed"),
            ("phase208_blocking_gap_rows", blocking_gaps, "Blocking quality gap rows"),
            ("phase208_trade_dates_max", int(summary["trade_dates"].max()) if not summary.empty else 0, "Maximum trade-date coverage"),
            ("phase208_symbols_max", int(summary["symbols"].max()) if not summary.empty else 0, "Maximum symbol coverage"),
            ("phase208_gate_rows", len(gates), "Gates evaluated"),
            ("phase208_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase208_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase208_feature_matrix_quality_gate_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase208 completed"),
            ("phase208_model_fit_allowed", 0, "No model fitting opened"),
            ("phase208_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase208_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase208_promotion_allowed", 0, "No promotion opened"),
            ("phase208_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase208_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase208_next_best_action", "run_phase209_model_fit_precommit_spec_no_execution_no_replay" if blocking_gaps == 0 else "repair_feature_matrix_quality_before_phase209", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase208 Feature Matrix Quality Gate",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase208 validates the Phase207 allowed feature matrix against Phase177 partition-quality evidence.",
        "It does not fit models, run replay, emit orders/fills/P&L, promote anything, or open paper/live acceptance.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase208_feature_matrix_quality_gate_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase208(phase177_dir: Path, phase207_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase207 = read_csv(phase207_dir / "phase207_feature_matrix_acceptance_summary.csv")
    matrix = read_csv(phase207_dir / "phase207_allowed_feature_matrix.csv")
    ablations = read_csv(phase207_dir / "phase207_target_exclusion_ablation_spec.csv")
    audit = read_csv(phase207_dir / "phase207_leakage_terminology_audit.csv")
    partition_quality = read_csv(phase177_dir / "phase177_partition_quality_metrics.csv")
    coverage = read_csv(phase177_dir / "phase177_horizon_date_coverage_metrics.csv")
    summary = build_matrix_quality_summary(matrix, partition_quality, coverage)
    gaps = build_blocking_gap_ledger(summary, ablations, audit)
    gates = build_gates(phase207, summary, gaps, ablations, audit)
    acceptance = build_acceptance(summary, gaps, gates)

    summary.to_csv(output_dir / "phase208_feature_matrix_quality_summary.csv", index=False)
    gaps.to_csv(output_dir / "phase208_blocking_gap_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase208_feature_matrix_quality_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase208_feature_matrix_quality_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Feature Matrix Quality Summary": summary,
            "Blocking Gap Ledger": gaps,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase208_feature_matrix_quality_gate_no_model_no_replay",
        **reproducibility_fields(
            artifact_id="phase208_feature_matrix_quality_gate",
            generated_utc=generated,
            inputs={
                "phase177_partition_quality": str(phase177_dir / "phase177_partition_quality_metrics.csv"),
                "phase177_coverage": str(phase177_dir / "phase177_horizon_date_coverage_metrics.csv"),
                "phase207_acceptance": str(phase207_dir / "phase207_feature_matrix_acceptance_summary.csv"),
                "phase207_matrix": str(phase207_dir / "phase207_allowed_feature_matrix.csv"),
            },
            parameters={
                "quality_scope": "feature_matrix_quality_gate_no_model_no_replay",
                "minimum_trade_dates": "5",
                "minimum_symbols": "32",
                "model_fit_allowed": "0",
                "strategy_replay_allowed": "0",
                "test_replay_allowed_next": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "summary": str(output_dir / "phase208_feature_matrix_quality_summary.csv"),
                "gaps": str(output_dir / "phase208_blocking_gap_ledger.csv"),
                "gates": str(output_dir / "phase208_feature_matrix_quality_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase208_feature_matrix_quality_acceptance_summary.csv"),
                "report": str(output_dir / "phase208_feature_matrix_quality_gate_report.md"),
            },
            scenario_ids="phase208_feature_matrix_quality_gate_no_model_no_replay",
            cost_model_version="not_applicable_no_strategy_replay",
            latency_model_version="not_applicable_no_strategy_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase208_feature_matrix_quality_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase208 feature matrix quality gate without model/replay.")
    parser.add_argument("--phase177-dir", type=Path, default=DEFAULT_PHASE177_DIR)
    parser.add_argument("--phase207-dir", type=Path, default=DEFAULT_PHASE207_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase208(args.phase177_dir, args.phase207_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
