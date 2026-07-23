from __future__ import annotations

import argparse
import json
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase49_dense_tick_rate_expansion import compact_files, densify_frame, read_month
from synthetic_l2.phase156_symbol_aware_tail_cadence_smoke import dense_profile
from synthetic_l2.phase158_phase106_style_full_realism_audit import (
    build_gap_summary as build_rewired_gap_summary,
    build_rewired_cadence_comparison,
)
from synthetic_l2.phase159_distributional_cadence_smoke import (
    DEFAULT_PROFILE_ID,
    build_distributional_profile,
)
from synthetic_l2.phase160_phase159_noncadence_realism_audit import (
    build_comparison as build_noncadence_comparison,
    build_gap_summary as build_noncadence_gap_summary,
    real_noncadence_profile_from_phase106,
    synthetic_noncadence_profile,
)
from synthetic_l2.phase161_combined_realism_handoff_gate import build_combined_metric_gate
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_COMPACT_ROOT = Path("raw_synthetic_l2_full_year_compact_monthly")
DEFAULT_OUTPUT_ROOT = Path("raw_synthetic_l2_phase162_distributional_full_year")
DEFAULT_PHASE155_DIR = Path("outputs/phase155")
DEFAULT_PHASE106_DIR = Path("outputs/phase106")
DEFAULT_OUTPUT_DIR = Path("outputs/phase162")
DEFAULT_MULTIPLIER = 64


def write_dense_shard(dense: pd.DataFrame, output_root: Path, profile_id: str, trade_month: str, symbol: str) -> Path:
    target_dir = output_root / f"profile={profile_id}" / f"trade_month={trade_month}" / f"symbol={symbol}"
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / "part-00000.parquet"
    pq.write_table(pa.Table.from_pandas(dense, preserve_index=False), target_file, compression="zstd")
    return target_file


def materialize_full_year(
    compact_root: Path,
    output_root: Path,
    phase155_dir: Path,
    symbols: list[str],
    multiplier: int,
    max_months: int,
) -> tuple[pd.DataFrame, float]:
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    profile = build_distributional_profile(phase155_dir, symbols)
    selected_files = compact_files(compact_root)
    if max_months > 0:
        selected_files = selected_files[:max_months]

    rows: list[dict[str, Any]] = []
    started = time.perf_counter()
    for path in selected_files:
        trade_month = path.parent.name.split("=", 1)[1]
        month = read_month(path, symbols)
        for symbol, symbol_frame in month.groupby("symbol", sort=True):
            dense = densify_frame(symbol_frame, multiplier, calibration_profile=profile)
            target_file = write_dense_shard(dense, output_root, profile.profile_id, trade_month, str(symbol))
            rows.append(
                {
                    "trade_month": trade_month,
                    "symbol": str(symbol),
                    "source_rows": int(len(symbol_frame)),
                    "dense_rows": int(len(dense)),
                    "multiplier": int(multiplier),
                    "file_path": str(target_file),
                    "bytes": int(target_file.stat().st_size),
                }
            )
    return pd.DataFrame(rows), time.perf_counter() - started


def build_phase162_cadence_comparison(
    phase155_dir: Path,
    phase106_dir: Path,
    inventory: pd.DataFrame,
    synthetic_profile: pd.DataFrame,
    symbols: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    contract = pd.read_csv(phase155_dir / "phase155_symbol_cadence_calibration_contract.csv")
    contract = contract[contract["symbol"].astype(str).isin(symbols)].copy()
    phase157_like_matrix = contract[
        [
            "symbol",
            "target_median_gap_ms",
            "target_median_p90_gap_ms",
            "target_median_p95_gap_ms",
            "target_median_gap_le_1s_fraction",
        ]
    ].merge(
        synthetic_profile.rename(
            columns={
                "median_gap_ms": "phase156_synthetic_median_gap_ms",
                "p90_gap_ms": "phase156_synthetic_p90_gap_ms",
                "p95_gap_ms": "phase156_synthetic_p95_gap_ms",
                "gap_le_1s_fraction": "phase156_synthetic_gap_le_1s_fraction",
            }
        ),
        on="symbol",
        how="inner",
    )
    full_cadence = build_rewired_cadence_comparison(contract, phase157_like_matrix)
    cadence_gaps = build_rewired_gap_summary(full_cadence)
    profile_summary = synthetic_profile.copy()
    profile_summary["months"] = int(inventory["trade_month"].nunique()) if not inventory.empty else 0
    return full_cadence, cadence_gaps, profile_summary


def summarize(
    inventory: pd.DataFrame,
    combined: pd.DataFrame,
    elapsed_seconds: float,
    requested_max_months: int,
) -> pd.DataFrame:
    months = int(inventory["trade_month"].nunique()) if not inventory.empty else 0
    symbols = int(inventory["symbol"].nunique()) if not inventory.empty else 0
    expected_partition_files = months * symbols
    actual_partition_files = int(len(inventory))
    missing_partition_files = int(max(0, expected_partition_files - actual_partition_files))
    total_rows = int(combined["symbol_metrics"].astype(int).sum()) if not combined.empty else 0
    total_gaps = int(combined["gap_count"].astype(int).sum()) if not combined.empty else 0
    gap_fraction = float(total_gaps / total_rows) if total_rows else 1.0
    severe_count = int((combined["gap_fraction"].astype(float) > 0.50).sum()) if not combined.empty else 0
    cadence_gaps = int(combined.loc[combined["metric_family"].eq("cadence"), "gap_count"].sum()) if not combined.empty else 0
    noncadence_gaps = int(combined.loc[combined["metric_family"].eq("generated_non_cadence"), "gap_count"].sum()) if not combined.empty else 0
    full_year_pass = bool(months >= 12 and symbols >= 32 and missing_partition_files == 0 and total_rows > 0 and gap_fraction <= 0.25 and severe_count == 0)
    return pd.DataFrame(
        [
            ("phase162_profile_id", DEFAULT_PROFILE_ID, "Distributional cadence profile materialized"),
            ("phase162_requested_max_months", requested_max_months, "0 means all local compact months"),
            ("phase162_months_materialized", months, "Synthetic months materialized locally"),
            ("phase162_symbols_materialized", symbols, "Symbols materialized"),
            ("phase162_partition_files", actual_partition_files, "Dense partition files written"),
            ("phase162_expected_partition_files", expected_partition_files, "Expected month/symbol shards from observed scope"),
            ("phase162_missing_partition_files", missing_partition_files, "Missing month/symbol shards"),
            ("phase162_dense_rows", int(inventory["dense_rows"].sum()) if not inventory.empty else 0, "Dense rows materialized"),
            ("phase162_dense_bytes", int(inventory["bytes"].sum()) if not inventory.empty else 0, "Compressed dense bytes"),
            ("phase162_elapsed_seconds", float(elapsed_seconds), "Materialization and audit elapsed seconds"),
            ("phase162_combined_anchor_metric_rows", total_rows, "Combined cadence plus generated non-cadence rows"),
            ("phase162_combined_gap_rows", total_gaps, "Combined rows outside gates"),
            ("phase162_combined_gap_fraction", gap_fraction, "Combined full-year gap fraction"),
            ("phase162_combined_severe_metric_gap_count", severe_count, "Combined metrics with gap_fraction > 0.50"),
            ("phase162_cadence_gap_rows", cadence_gaps, "Cadence gaps from full-year distributional audit"),
            ("phase162_generated_noncadence_gap_rows", noncadence_gaps, "Generated non-cadence gaps from full-year parquet"),
            ("phase162_full_year_realism_audit_pass", int(full_year_pass), "1 means full-year materialization/audit passes"),
            ("phase162_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase162_azure_read_policy", "forbidden_for_analysis_download_first_then_local", "No Python direct Azure scanning in this phase"),
            ("phase162_next_best_action", "review_full_year_materialization_then_prepare_synthetic_only_replay_preflight_if_accepted", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase162 Phase159 Full-year Materialization Audit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase162 materializes the Phase159 distributional cadence profile across the local compact full-year synthetic lake.",
        "It reruns cadence and generated non-cadence realism checks from local Parquet only. It does not stream Azure files, run strategy replay, fills, P&L, or profitability claims.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase162_phase159_full_year_materialization_audit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase162(
    compact_root: Path,
    output_root: Path,
    phase155_dir: Path,
    phase106_dir: Path,
    output_dir: Path,
    base_dir: Path,
    symbols: list[str],
    multiplier: int,
    max_months: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    if not symbols:
        contract = pd.read_csv(phase155_dir / "phase155_symbol_cadence_calibration_contract.csv")
        symbols = sorted(contract["symbol"].astype(str).unique())

    inventory, elapsed_seconds = materialize_full_year(compact_root, output_root, phase155_dir, symbols, multiplier, max_months)
    cadence_profile = dense_profile(inventory)
    cadence_comparison, cadence_gaps, cadence_profile_summary = build_phase162_cadence_comparison(
        phase155_dir, phase106_dir, inventory, cadence_profile, symbols
    )
    phase106_comparison = pd.read_csv(phase106_dir / "real_vs_calibrated_synthetic_comparison.csv")
    generated_noncadence = synthetic_noncadence_profile(inventory)
    real_noncadence = real_noncadence_profile_from_phase106(phase106_comparison)
    noncadence_comparison = build_noncadence_comparison(real_noncadence, generated_noncadence)
    noncadence_gaps = build_noncadence_gap_summary(noncadence_comparison)
    combined = build_combined_metric_gate(cadence_gaps, noncadence_gaps)
    acceptance = summarize(inventory, combined, elapsed_seconds, max_months)

    inventory.to_csv(output_dir / "phase162_dense_full_year_inventory.csv", index=False)
    cadence_profile_summary.to_csv(output_dir / "phase162_dense_full_year_cadence_profile.csv", index=False)
    cadence_comparison.to_csv(output_dir / "phase162_full_year_cadence_comparison.csv", index=False)
    cadence_gaps.to_csv(output_dir / "phase162_full_year_cadence_gap_summary.csv", index=False)
    generated_noncadence.to_csv(output_dir / "phase162_generated_noncadence_profile.csv", index=False)
    noncadence_comparison.to_csv(output_dir / "phase162_generated_noncadence_comparison.csv", index=False)
    noncadence_gaps.to_csv(output_dir / "phase162_generated_noncadence_gap_summary.csv", index=False)
    combined.to_csv(output_dir / "phase162_combined_metric_gate.csv", index=False)
    acceptance.to_csv(output_dir / "phase162_full_year_materialization_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Combined Metric Gate": combined,
            "Cadence Gap Summary": cadence_gaps,
            "Generated Non-cadence Gap Summary": noncadence_gaps,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase162_phase159_full_year_materialization_audit",
        **reproducibility_fields(
            artifact_id="phase162",
            generated_utc=generated_utc,
            inputs={
                "compact_root": str(compact_root),
                "phase155_contract": str(phase155_dir / "phase155_symbol_cadence_calibration_contract.csv"),
                "phase106_comparison": str(phase106_dir / "real_vs_calibrated_synthetic_comparison.csv"),
            },
            parameters={
                "profile_id": DEFAULT_PROFILE_ID,
                "symbols": symbols,
                "multiplier": multiplier,
                "max_months": max_months,
                "combined_gap_fraction_gate": "<=0.25",
                "severe_metric_gap_gate": "0",
                "strategy_replay_policy": "closed",
                "azure_read_policy": "forbidden_for_analysis_download_first_then_local",
            },
            outputs={
                "dense_output_root": str(output_root),
                "inventory": str(output_dir / "phase162_dense_full_year_inventory.csv"),
                "cadence_profile": str(output_dir / "phase162_dense_full_year_cadence_profile.csv"),
                "combined_metric_gate": str(output_dir / "phase162_combined_metric_gate.csv"),
                "acceptance_summary": str(output_dir / "phase162_full_year_materialization_acceptance_summary.csv"),
                "report": str(output_dir / "phase162_phase159_full_year_materialization_audit_report.md"),
                "manifest": str(output_dir / "phase162_phase159_full_year_materialization_audit_manifest.json"),
            },
            random_seed="none_deterministic_phase162_full_year_distributional",
            scenario_ids="phase162_phase159_distributional_full_year_materialization",
            cost_model_version="not_applicable",
            latency_model_version="not_applicable_no_execution",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase162_phase159_full_year_materialization_audit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize/audit Phase159 distributional cadence profile across full synthetic year.")
    parser.add_argument("--compact-root", type=Path, default=DEFAULT_COMPACT_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--phase155-dir", type=Path, default=DEFAULT_PHASE155_DIR)
    parser.add_argument("--phase106-dir", type=Path, default=DEFAULT_PHASE106_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--symbols", nargs="+", default=[])
    parser.add_argument("--multiplier", type=int, default=DEFAULT_MULTIPLIER)
    parser.add_argument("--max-months", type=int, default=0, help="0 means all local compact monthly files.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase162(
        args.compact_root,
        args.output_root,
        args.phase155_dir,
        args.phase106_dir,
        args.output_dir,
        args.base_dir,
        args.symbols,
        args.multiplier,
        args.max_months,
    )


if __name__ == "__main__":
    main()
