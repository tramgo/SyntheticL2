from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE159_DIR = Path("outputs/phase159")
DEFAULT_PHASE160_DIR = Path("outputs/phase160")
DEFAULT_OUTPUT_DIR = Path("outputs/phase161")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(path: Path, metric: str, default: Any = "missing") -> Any:
    frame = read_csv(path)
    if frame.empty or "metric" not in frame.columns or "value" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def to_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def build_combined_metric_gate(phase159_gaps: pd.DataFrame, phase160_gaps: pd.DataFrame) -> pd.DataFrame:
    cadence = phase159_gaps[phase159_gaps["anchor_source"].astype(str).str.contains("phase154_full_partition", na=False)].copy()
    cadence["metric_family"] = "cadence"
    cadence["evidence_source"] = "phase159_distributional_generated_cadence"
    noncadence = phase160_gaps.copy()
    noncadence["metric_family"] = "generated_non_cadence"
    noncadence["evidence_source"] = "phase160_generated_phase159_parquet"
    common_columns = [
        "metric_family",
        "category",
        "metric",
        "symbol_metrics",
        "gap_count",
        "gap_fraction",
        "median_synthetic_to_real_ratio",
        "min_synthetic_to_real_ratio",
        "max_synthetic_to_real_ratio",
        "evidence_source",
    ]
    combined = pd.concat([cadence[common_columns], noncadence[common_columns]], ignore_index=True, sort=False)
    combined["gap_count"] = pd.to_numeric(combined["gap_count"], errors="coerce").fillna(0).astype(int)
    combined["gap_fraction"] = pd.to_numeric(combined["gap_fraction"], errors="coerce").fillna(1.0)
    combined["metric_gate_pass"] = ((combined["gap_fraction"] <= 0.50) & (combined["gap_count"] < combined["symbol_metrics"].astype(int))).astype(int)
    return combined.sort_values(["metric_gate_pass", "gap_fraction", "metric"], ascending=[True, False, True], kind="mergesort")


def build_broader_materialization_plan(phase159_inventory: pd.DataFrame) -> pd.DataFrame:
    smoke_months = int(phase159_inventory["trade_month"].nunique()) if not phase159_inventory.empty else 0
    smoke_symbols = int(phase159_inventory["symbol"].nunique()) if not phase159_inventory.empty else 0
    smoke_rows = int(phase159_inventory["dense_rows"].sum()) if not phase159_inventory.empty else 0
    smoke_bytes = int(phase159_inventory["bytes"].sum()) if not phase159_inventory.empty else 0
    estimated_12m_rows = int(smoke_rows * 12 / max(smoke_months, 1))
    estimated_12m_bytes = int(smoke_bytes * 12 / max(smoke_months, 1))
    return pd.DataFrame(
        [
            {
                "priority": 1,
                "work_item": "materialize_phase159_distributional_profile_all_12_months",
                "current_smoke_months": smoke_months,
                "current_smoke_symbols": smoke_symbols,
                "current_smoke_rows": smoke_rows,
                "current_smoke_bytes": smoke_bytes,
                "estimated_12m_rows": estimated_12m_rows,
                "estimated_12m_compressed_bytes": estimated_12m_bytes,
                "acceptance_gate": "All 12 synthetic months materialized locally with P159 distributional cadence profile and no missing symbol/month shards.",
            },
            {
                "priority": 2,
                "work_item": "rerun_phase159_phase160_style_audits_on_broader_materialization",
                "current_smoke_months": smoke_months,
                "current_smoke_symbols": smoke_symbols,
                "current_smoke_rows": smoke_rows,
                "current_smoke_bytes": smoke_bytes,
                "estimated_12m_rows": estimated_12m_rows,
                "estimated_12m_compressed_bytes": estimated_12m_bytes,
                "acceptance_gate": "Combined cadence and generated non-cadence gap fraction remains <=0.25 with zero severe metric gaps across broader materialization.",
            },
            {
                "priority": 3,
                "work_item": "only_then_prepare_synthetic_only_strategy_replay_preflight",
                "current_smoke_months": smoke_months,
                "current_smoke_symbols": smoke_symbols,
                "current_smoke_rows": smoke_rows,
                "current_smoke_bytes": smoke_bytes,
                "estimated_12m_rows": estimated_12m_rows,
                "estimated_12m_compressed_bytes": estimated_12m_bytes,
                "acceptance_gate": "Replay preflight may be considered only after broader materialization/audit passes; this phase itself keeps replay closed.",
            },
        ]
    )


def summarize(
    combined: pd.DataFrame,
    phase159_acceptance_path: Path,
    phase160_acceptance_path: Path,
    phase159_inventory: pd.DataFrame,
) -> pd.DataFrame:
    total_rows = int(combined["symbol_metrics"].astype(int).sum()) if not combined.empty else 0
    total_gaps = int(combined["gap_count"].astype(int).sum()) if not combined.empty else 0
    gap_fraction = float(total_gaps / total_rows) if total_rows else 1.0
    severe_count = int((combined["gap_fraction"].astype(float) > 0.50).sum()) if not combined.empty else 0
    cadence_gaps = int(combined.loc[combined["metric_family"].eq("cadence"), "gap_count"].sum()) if not combined.empty else 0
    noncadence_gaps = int(combined.loc[combined["metric_family"].eq("generated_non_cadence"), "gap_count"].sum()) if not combined.empty else 0
    bounded_pass = bool(total_rows > 0 and gap_fraction <= 0.25 and severe_count == 0)
    smoke_months = int(phase159_inventory["trade_month"].nunique()) if not phase159_inventory.empty else 0
    broader_materialization_required = bool(smoke_months < 12)
    return pd.DataFrame(
        [
            ("phase161_phase159_full_rewired_realism_pass", metric_value(phase159_acceptance_path, "phase158_full_rewired_realism_pass"), "Inherited Phase159 Phase158-style pass"),
            ("phase161_phase160_generated_noncadence_realism_pass", metric_value(phase160_acceptance_path, "phase160_generated_noncadence_realism_pass"), "Inherited Phase160 generated non-cadence pass"),
            ("phase161_combined_symbols", int(phase159_inventory["symbol"].nunique()) if not phase159_inventory.empty else 0, "Symbols in combined bounded handoff"),
            ("phase161_combined_anchor_metric_rows", total_rows, "Combined cadence plus generated non-cadence rows"),
            ("phase161_combined_gap_rows", total_gaps, "Combined rows outside gates"),
            ("phase161_combined_gap_fraction", gap_fraction, "Combined bounded gap fraction"),
            ("phase161_combined_severe_metric_gap_count", severe_count, "Combined metrics with gap_fraction > 0.50"),
            ("phase161_cadence_gap_rows", cadence_gaps, "Cadence gaps from Phase159 distributional audit"),
            ("phase161_generated_noncadence_gap_rows", noncadence_gaps, "Generated non-cadence gaps from Phase160 audit"),
            ("phase161_bounded_realism_handoff_pass", int(bounded_pass), "1 means bounded realism handoff gate passes"),
            ("phase161_smoke_months_materialized", smoke_months, "Synthetic months materialized in current bounded smoke"),
            ("phase161_broader_materialization_required", int(broader_materialization_required), "1 means all-12-month materialization still required"),
            ("phase161_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase161_next_best_action", "materialize_phase159_distributional_profile_all_12_months_then_rerun_combined_audit", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase161 Combined Realism Handoff Gate",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase161 combines Phase159 distributional cadence evidence with Phase160 generated non-cadence evidence.",
        "It decides whether the bounded generated shard is ready for broader materialization/audit. It does not open strategy replay.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase161_combined_realism_handoff_gate_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase161(phase159_dir: Path, phase160_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase159_gaps = read_csv(phase159_dir / "phase159_rewired_gap_summary.csv")
    phase160_gaps = read_csv(phase160_dir / "phase160_generated_noncadence_gap_summary.csv")
    phase159_inventory = read_csv(phase159_dir / "phase159_dense_smoke_inventory.csv")
    combined = build_combined_metric_gate(phase159_gaps, phase160_gaps)
    materialization_plan = build_broader_materialization_plan(phase159_inventory)
    acceptance = summarize(
        combined,
        phase159_dir / "phase159_distributional_cadence_acceptance_summary.csv",
        phase160_dir / "phase160_phase159_noncadence_realism_acceptance_summary.csv",
        phase159_inventory,
    )

    combined.to_csv(output_dir / "phase161_combined_metric_gate.csv", index=False)
    materialization_plan.to_csv(output_dir / "phase161_broader_materialization_plan.csv", index=False)
    acceptance.to_csv(output_dir / "phase161_combined_realism_handoff_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Combined Metric Gate": combined,
            "Broader Materialization Plan": materialization_plan,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase161_combined_realism_handoff_gate",
        **reproducibility_fields(
            artifact_id="phase161",
            generated_utc=generated_utc,
            inputs={
                "phase159_gap_summary": str(phase159_dir / "phase159_rewired_gap_summary.csv"),
                "phase160_gap_summary": str(phase160_dir / "phase160_generated_noncadence_gap_summary.csv"),
                "phase159_inventory": str(phase159_dir / "phase159_dense_smoke_inventory.csv"),
            },
            parameters={
                "handoff_scope": "bounded_one_month_generated_shard_to_broader_materialization",
                "combined_gap_fraction_gate": "<=0.25",
                "severe_metric_gap_gate": "0",
                "strategy_replay_policy": "closed",
            },
            outputs={
                "combined_metric_gate": str(output_dir / "phase161_combined_metric_gate.csv"),
                "broader_materialization_plan": str(output_dir / "phase161_broader_materialization_plan.csv"),
                "acceptance_summary": str(output_dir / "phase161_combined_realism_handoff_acceptance_summary.csv"),
                "report": str(output_dir / "phase161_combined_realism_handoff_gate_report.md"),
                "manifest": str(output_dir / "phase161_combined_realism_handoff_gate_manifest.json"),
            },
            random_seed="none_deterministic_phase161_gate",
            scenario_ids="phase161_phase159_phase160_bounded_handoff",
            cost_model_version="not_applicable",
            latency_model_version="not_applicable_no_execution",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase161_combined_realism_handoff_gate_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Combine Phase159 cadence and Phase160 generated non-cadence realism gates.")
    parser.add_argument("--phase159-dir", type=Path, default=DEFAULT_PHASE159_DIR)
    parser.add_argument("--phase160-dir", type=Path, default=DEFAULT_PHASE160_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase161(args.phase159_dir, args.phase160_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
