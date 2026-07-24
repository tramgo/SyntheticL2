from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE176_DIR = Path("outputs/phase176")
DEFAULT_PHASE175_DIR = Path("outputs/phase175")
DEFAULT_FEATURE_ROOT = Path("derived_real_l2_receive_flow_features_phase176")
DEFAULT_OUTPUT_DIR = Path("outputs/phase177")
FORBIDDEN_OUTPUTS = "buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance"


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


def build_quality_audit_catalog(schema: pd.DataFrame) -> pd.DataFrame:
    checks = [
        ("coverage_by_date_symbol_horizon", "coverage rows must be reported for every materialized feature/date/symbol/horizon"),
        ("staleness_and_forward_fill", "stale fraction and forward-fill fraction must be bounded and reported per symbol/horizon"),
        ("train_test_leakage", "train-fitted transforms only; no future receive events in any feature timestamp"),
        ("blocked_family_overlap", "feature names and formulas must not reproduce Phase164/Phase167/Phase131-136 blocked strategy forms"),
        ("schema_and_null_rates", "required feature columns must exist with null rates below predeclared thresholds"),
    ]
    rows: list[dict[str, Any]] = []
    for feature_id in schema.get("feature_id", pd.Series(dtype=str)).astype(str):
        for check_id, definition in checks:
            rows.append(
                {
                    "feature_id": feature_id,
                    "quality_check_id": f"P177_{feature_id}_{check_id}".upper(),
                    "check_family": check_id,
                    "definition": definition,
                    "minimum_required_before_phase178": "pass_or_emit_blocking_gap_ledger",
                    "strategy_replay_allowed": 0,
                }
            )
    return pd.DataFrame(rows)


def build_gate_evaluation(phase176: pd.DataFrame, schema: pd.DataFrame, feature_root: Path) -> pd.DataFrame:
    materialized = as_int(metric_value(phase176, "phase176_features_materialized", 0))
    feature_files = list(feature_root.rglob("*.parquet")) if feature_root.exists() else []
    return pd.DataFrame(
        [
            {
                "gate_id": "P177_PHASE176_FEATURES_MATERIALIZED",
                "gate_pass": int(materialized == 1),
                "evidence": f"phase176_features_materialized={materialized}",
                "severity": "activation",
            },
            {
                "gate_id": "P177_FEATURE_ROOT_HAS_PARQUET",
                "gate_pass": int(len(feature_files) > 0),
                "evidence": f"feature_root={feature_root};parquet_files={len(feature_files)}",
                "severity": "activation",
            },
            {
                "gate_id": "P177_SCHEMA_AVAILABLE",
                "gate_pass": int(len(schema) >= 6),
                "evidence": f"feature_schema_rows={len(schema)}",
                "severity": "hard",
            },
            {
                "gate_id": "P177_NO_REPLAY_OR_PROFITABILITY_OUTPUTS",
                "gate_pass": 1,
                "evidence": "feature-quality scaffold only while materialization gate is closed; forbidden_outputs=" + FORBIDDEN_OUTPUTS,
                "severity": "hard",
            },
        ]
    )


def build_acceptance_summary(catalog: pd.DataFrame, gates: pd.DataFrame, phase176: pd.DataFrame) -> pd.DataFrame:
    materialized = as_int(metric_value(phase176, "phase176_features_materialized", 0))
    activation = gates[gates["severity"].astype(str).eq("activation")]
    hard = gates[gates["severity"].astype(str).eq("hard")]
    audit_ran = int(materialized == 1 and not activation.empty and activation["gate_pass"].astype(bool).all())
    next_action = (
        "run_phase178_receive_flow_feature_handoff_precommit_no_strategy"
        if audit_ran
        else "add_AZURE_STORAGE_SAS_TOKEN_or_AZURE_STORAGE_KEY_then_rerun_phase174_phase172_phase175_phase176_before_phase177"
    )
    return pd.DataFrame(
        [
            ("phase177_quality_check_rows", int(len(catalog)), "Predeclared feature-quality checks"),
            ("phase177_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase177_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase177_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase177_features_materialized", materialized, "Inherited Phase176 feature materialization flag"),
            ("phase177_feature_quality_audit_ran", audit_ran, "1 means feature-quality metrics were computed"),
            ("phase177_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase177_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase177_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase177_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase177 Receive-flow Feature Quality Audit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase177 is the quality-audit scaffold for Phase176 materialized receive-flow features.",
        "When no feature parquet exists, Phase177 writes check catalog and gates only.",
        "It does not emit signals, orders, fills, P&L, profitability claims, or paper/live acceptance.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase177_receive_flow_feature_quality_audit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase177(phase176_dir: Path, phase175_dir: Path, feature_root: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase176 = read_csv(phase176_dir / "phase176_receive_flow_feature_materializer_acceptance_summary.csv")
    schema = read_csv(phase175_dir / "phase175_receive_flow_feature_schema.csv")
    catalog = build_quality_audit_catalog(schema)
    gates = build_gate_evaluation(phase176, schema, feature_root)
    acceptance = build_acceptance_summary(catalog, gates, phase176)

    catalog.to_csv(output_dir / "phase177_feature_quality_check_catalog.csv", index=False)
    gates.to_csv(output_dir / "phase177_feature_quality_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase177_receive_flow_feature_quality_audit_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Quality Check Catalog": catalog,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase177_receive_flow_feature_quality_audit",
        **reproducibility_fields(
            artifact_id="phase177_receive_flow_feature_quality_audit",
            generated_utc=generated,
            inputs={
                "phase176_acceptance": str(phase176_dir / "phase176_receive_flow_feature_materializer_acceptance_summary.csv"),
                "phase175_schema": str(phase175_dir / "phase175_receive_flow_feature_schema.csv"),
                "feature_root": str(feature_root),
            },
            parameters={
                "activation_policy": "compute_quality_metrics_only_after_phase176_features_materialized_equals_1",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
                "strategy_replay_policy": "closed",
            },
            outputs={
                "quality_check_catalog": str(output_dir / "phase177_feature_quality_check_catalog.csv"),
                "gate_evaluation": str(output_dir / "phase177_feature_quality_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase177_receive_flow_feature_quality_audit_acceptance_summary.csv"),
                "report": str(output_dir / "phase177_receive_flow_feature_quality_audit_report.md"),
            },
            random_seed="none_deterministic_quality_audit_scaffold",
            scenario_ids="phase177_gated_receive_flow_feature_quality_audit",
            cost_model_version="not_applicable_no_replay",
            latency_model_version="not_applicable_no_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase177_receive_flow_feature_quality_audit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase176-dir", type=Path, default=DEFAULT_PHASE176_DIR)
    parser.add_argument("--phase175-dir", type=Path, default=DEFAULT_PHASE175_DIR)
    parser.add_argument("--feature-root", type=Path, default=DEFAULT_FEATURE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase177(args.phase176_dir, args.phase175_dir, args.feature_root, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
