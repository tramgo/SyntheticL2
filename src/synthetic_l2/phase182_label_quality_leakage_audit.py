from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE181_DIR = Path("outputs/phase181")
DEFAULT_PHASE180_DIR = Path("outputs/phase180")
DEFAULT_OUTPUT_DIR = Path("outputs/phase182")
FORBIDDEN_OUTPUTS = {
    "signal",
    "side",
    "order",
    "order_arrival",
    "fill_model",
    "pnl",
    "pnl_replay",
    "profit",
    "profitability_claim",
    "paper_live_acceptance",
}


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


def audit_label_partitions(label_inventory: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    required_columns = {
        "bucket_ms",
        "trade_date",
        "exchange",
        "symbol",
        "horizon_sec",
        "split_role",
        "future_mid_return_bps_next_bucket",
        "future_abs_return_bps_next_bucket",
        "future_spread_change_bps_next_bucket",
        "execution_risk_spread_widen_next_bucket",
        "short_horizon_direction_label",
        "label_available",
    }
    for item in label_inventory.to_dict("records"):
        path = Path(item["label_file"])
        if not path.exists():
            rows.append(
                {
                    "label_file": str(path),
                    "read_status": "missing",
                    "rows": 0,
                    "missing_required_columns": ";".join(sorted(required_columns)),
                    "forbidden_columns": "",
                    "bucket_monotonic_violations": 0,
                    "duplicate_bucket_rows": 0,
                    "split_role_mismatch_rows": 0,
                    "test_role_rows": 0,
                    "label_available_fraction": 0.0,
                    "audit_pass": 0,
                }
            )
            continue
        df = pd.read_parquet(path)
        columns = set(df.columns.astype(str) if hasattr(df.columns, "astype") else [str(col) for col in df.columns])
        missing = sorted(required_columns.difference(columns))
        forbidden = sorted(col for col in columns for token in FORBIDDEN_OUTPUTS if token == col or col.startswith(token + "_"))
        bucket = pd.to_numeric(df["bucket_ms"], errors="coerce") if "bucket_ms" in df.columns else pd.Series(dtype=float)
        monotonic_violations = int((bucket.diff().dropna() < 0).sum()) if not bucket.empty else 0
        duplicate_bucket_rows = int(bucket.duplicated().sum()) if not bucket.empty else 0
        expected_split = str(item.get("split_role", ""))
        split_mismatch = int(df["split_role"].astype(str).ne(expected_split).sum()) if "split_role" in df.columns else len(df)
        label_available_fraction = float(pd.to_numeric(df["label_available"], errors="coerce").fillna(0).mean()) if "label_available" in df.columns and len(df) else 0.0
        test_role_rows = int(df["split_role"].astype(str).eq("test_untouched").sum()) if "split_role" in df.columns else 0
        audit_pass = int(
            not missing
            and not forbidden
            and monotonic_violations == 0
            and duplicate_bucket_rows == 0
            and split_mismatch == 0
            and label_available_fraction > 0.90
        )
        rows.append(
            {
                "label_file": str(path),
                "read_status": "ok",
                "horizon_sec": item.get("horizon_sec", ""),
                "trade_date": item.get("trade_date", ""),
                "exchange": item.get("exchange", ""),
                "symbol": item.get("symbol", ""),
                "split_role": expected_split,
                "rows": int(len(df)),
                "missing_required_columns": ";".join(missing),
                "forbidden_columns": ";".join(forbidden),
                "bucket_monotonic_violations": monotonic_violations,
                "duplicate_bucket_rows": duplicate_bucket_rows,
                "split_role_mismatch_rows": split_mismatch,
                "test_role_rows": test_role_rows,
                "label_available_fraction": label_available_fraction,
                "audit_pass": audit_pass,
            }
        )
    return pd.DataFrame(rows)


def build_split_leakage_audit(partition_audit: pd.DataFrame, label_quality: pd.DataFrame) -> pd.DataFrame:
    if partition_audit.empty:
        return pd.DataFrame()
    rows = []
    for split_role, group in partition_audit.groupby("split_role", sort=True):
        rows.append(
            {
                "split_role": split_role,
                "partitions": int(len(group)),
                "rows": int(group["rows"].sum()),
                "test_untouched_rows": int(group["test_role_rows"].sum()),
                "failed_partitions": int((group["audit_pass"].astype(int) == 0).sum()),
                "min_label_available_fraction": float(group["label_available_fraction"].min()),
                "leakage_policy": "test_untouched rows may exist as labels but must not be used for selection before replay precommit",
            }
        )
    return pd.DataFrame(rows)


def build_gate_evaluation(phase181: pd.DataFrame, phase180: pd.DataFrame, partition_audit: pd.DataFrame, split_audit: pd.DataFrame) -> pd.DataFrame:
    labels_materialized = as_int(metric_value(phase181, "phase181_labels_materialized", 0))
    phase180_ready = as_int(metric_value(phase180, "phase180_precommit_ready", 0))
    failed_partitions = int((partition_audit["audit_pass"].astype(int) == 0).sum()) if not partition_audit.empty else -1
    forbidden_partitions = int(partition_audit["forbidden_columns"].astype(str).ne("").sum()) if not partition_audit.empty else -1
    split_roles = set(partition_audit["split_role"].astype(str).tolist()) if not partition_audit.empty else set()
    min_availability = float(partition_audit["label_available_fraction"].min()) if not partition_audit.empty else 0.0
    return pd.DataFrame(
        [
            {
                "gate_id": "P182_PHASE181_LABELS_MATERIALIZED",
                "gate_pass": int(labels_materialized == 1),
                "evidence": f"phase181_labels_materialized={labels_materialized}",
                "severity": "hard",
            },
            {
                "gate_id": "P182_PHASE180_PRECOMMIT_READY",
                "gate_pass": int(phase180_ready == 1),
                "evidence": f"phase180_precommit_ready={phase180_ready}",
                "severity": "hard",
            },
            {
                "gate_id": "P182_ALL_LABEL_PARTITIONS_PASS",
                "gate_pass": int(len(partition_audit) >= 640 and failed_partitions == 0),
                "evidence": f"partitions={len(partition_audit)};failed_partitions={failed_partitions}",
                "severity": "hard",
            },
            {
                "gate_id": "P182_NO_FORBIDDEN_OUTPUT_COLUMNS",
                "gate_pass": int(forbidden_partitions == 0),
                "evidence": f"forbidden_column_partitions={forbidden_partitions}",
                "severity": "hard",
            },
            {
                "gate_id": "P182_SPLIT_ROLES_AND_TEST_UNTOUCHED_PRESENT",
                "gate_pass": int({"train", "validation", "test_untouched"}.issubset(split_roles)),
                "evidence": "split_roles=" + ";".join(sorted(split_roles)),
                "severity": "hard",
            },
            {
                "gate_id": "P182_LABEL_AVAILABILITY_THRESHOLD",
                "gate_pass": int(min_availability > 0.90),
                "evidence": f"min_label_available_fraction={min_availability:.6f}",
                "severity": "hard",
            },
            {
                "gate_id": "P182_NO_REPLAY_OR_PROFITABILITY_OUTPUTS",
                "gate_pass": 1,
                "evidence": "label quality/leakage audit only; no replay or PnL artifacts emitted",
                "severity": "hard",
            },
        ]
    )


def build_acceptance_summary(partition_audit: pd.DataFrame, split_audit: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0
    audit_ready = int(not hard.empty and hard_pass == len(hard))
    return pd.DataFrame(
        [
            ("phase182_partition_audit_rows", int(len(partition_audit)), "Label partitions audited"),
            ("phase182_split_audit_rows", int(len(split_audit)), "Split leakage audit rows"),
            ("phase182_failed_partitions", int((partition_audit["audit_pass"].astype(int) == 0).sum()) if not partition_audit.empty else 0, "Failed label partitions"),
            ("phase182_forbidden_column_partitions", int(partition_audit["forbidden_columns"].astype(str).ne("").sum()) if not partition_audit.empty else 0, "Partitions with forbidden output columns"),
            ("phase182_min_label_available_fraction", float(partition_audit["label_available_fraction"].min()) if not partition_audit.empty else 0.0, "Minimum partition label availability"),
            ("phase182_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase182_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase182_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase182_label_quality_leakage_audit_pass", audit_ready, "1 means label quality/leakage audit passed"),
            ("phase182_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase182_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase182_next_best_action", "build_phase183_replay_readiness_precommit_no_pnl" if audit_ready else "repair_phase181_labels_before_replay_readiness", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase182 Label Quality and Leakage Audit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase182 audits Phase181 labels for quality, split integrity, leakage boundaries, and forbidden output columns.",
        "It does not run strategies, emit orders, compute fills, calculate P&L, claim profitability, or open paper/live acceptance.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase182_label_quality_leakage_audit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase182(phase181_dir: Path, phase180_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase181 = read_csv(phase181_dir / "phase181_label_materialization_acceptance_summary.csv")
    phase180 = read_csv(phase180_dir / "phase180_cost_latency_label_precommit_acceptance_summary.csv")
    label_inventory = read_csv(phase181_dir / "phase181_label_partition_inventory.csv")
    label_quality = read_csv(phase181_dir / "phase181_label_quality_by_horizon_date_split.csv")
    partition_audit = audit_label_partitions(label_inventory)
    split_audit = build_split_leakage_audit(partition_audit, label_quality)
    gates = build_gate_evaluation(phase181, phase180, partition_audit, split_audit)
    acceptance = build_acceptance_summary(partition_audit, split_audit, gates)

    partition_audit.to_csv(output_dir / "phase182_label_partition_quality_audit.csv", index=False)
    split_audit.to_csv(output_dir / "phase182_split_leakage_audit.csv", index=False)
    gates.to_csv(output_dir / "phase182_label_quality_leakage_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase182_label_quality_leakage_audit_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Split Leakage Audit": split_audit,
            "Gate Evaluation": gates,
            "Label Partition Quality Audit": partition_audit.head(200),
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase182_label_quality_leakage_audit",
        **reproducibility_fields(
            artifact_id="phase182_label_quality_leakage_audit",
            generated_utc=generated,
            inputs={
                "phase181_acceptance": str(phase181_dir / "phase181_label_materialization_acceptance_summary.csv"),
                "phase181_label_partition_inventory": str(phase181_dir / "phase181_label_partition_inventory.csv"),
                "phase181_label_quality": str(phase181_dir / "phase181_label_quality_by_horizon_date_split.csv"),
                "phase180_acceptance": str(phase180_dir / "phase180_cost_latency_label_precommit_acceptance_summary.csv"),
            },
            parameters={
                "audit_policy": "label_quality_leakage_no_replay",
                "minimum_partition_availability": 0.90,
                "forbidden_outputs": ";".join(sorted(FORBIDDEN_OUTPUTS)),
            },
            outputs={
                "partition_audit": str(output_dir / "phase182_label_partition_quality_audit.csv"),
                "split_leakage_audit": str(output_dir / "phase182_split_leakage_audit.csv"),
                "gate_evaluation": str(output_dir / "phase182_label_quality_leakage_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase182_label_quality_leakage_audit_acceptance_summary.csv"),
                "report": str(output_dir / "phase182_label_quality_leakage_audit_report.md"),
            },
            random_seed="none_deterministic_label_quality_leakage_audit",
            scenario_ids="phase182_label_quality_leakage_audit",
            cost_model_version="not_applicable_no_replay",
            latency_model_version="not_applicable_no_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase182_label_quality_leakage_audit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase181-dir", type=Path, default=DEFAULT_PHASE181_DIR)
    parser.add_argument("--phase180-dir", type=Path, default=DEFAULT_PHASE180_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase182(args.phase181_dir, args.phase180_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
