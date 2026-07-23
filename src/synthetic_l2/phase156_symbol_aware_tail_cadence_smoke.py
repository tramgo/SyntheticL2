from __future__ import annotations

import argparse
import json
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from synthetic_l2.generator_calibration_profiles import get_calibration_profile
from synthetic_l2.generator_calibration_profiles import GeneratorCalibrationProfile
from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase49_dense_tick_rate_expansion import compact_files, densify_frame, read_month
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PROFILE_ID = "P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE"
DEFAULT_COMPACT_ROOT = Path("raw_synthetic_l2_full_year_compact_monthly")
DEFAULT_OUTPUT_ROOT = Path("raw_synthetic_l2_phase156_symbol_tail_cadence_smoke")
DEFAULT_PHASE155_DIR = Path("outputs/phase155")
DEFAULT_OUTPUT_DIR = Path("outputs/phase156")
DEFAULT_SYMBOLS = [
    "BRITANNIA",
    "ITBEES",
    "ULTRACEMCO",
    "NESTLEIND",
    "BPCL",
    "CIPLA",
    "BAJAJ-AUTO",
    "HINDUNILVR",
]


def read_contract(path: Path, symbols: list[str]) -> pd.DataFrame:
    contract = pd.read_csv(path)
    contract = contract[contract["symbol"].astype(str).isin(symbols)].copy()
    numeric_columns = [
        "target_median_gap_ms",
        "target_median_p90_gap_ms",
        "target_median_p95_gap_ms",
        "phase106_synthetic_p90_gap_ms",
        "phase106_synthetic_p95_gap_ms",
        "phase106_synthetic_gap_le_1s_fraction",
    ]
    for column in numeric_columns:
        contract[column] = pd.to_numeric(contract[column], errors="coerce")
    return contract


def write_smoke_shard(dense: pd.DataFrame, output_root: Path, trade_month: str, symbol: str) -> Path:
    target_dir = output_root / f"profile={DEFAULT_PROFILE_ID}" / f"trade_month={trade_month}" / f"symbol={symbol}"
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / "part-00000.parquet"
    pq.write_table(pa.Table.from_pandas(dense, preserve_index=False), target_file, compression="zstd")
    return target_file


def materialize_smoke(
    compact_root: Path,
    output_root: Path,
    symbols: list[str],
    multiplier: int,
    max_months: int,
    profile_id: str,
    calibration_profile: GeneratorCalibrationProfile | None = None,
) -> tuple[pd.DataFrame, float]:
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    profile = calibration_profile or get_calibration_profile(profile_id)
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
            target_file = write_smoke_shard(dense, output_root, trade_month, str(symbol))
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


def dense_profile(inventory: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for symbol, group in inventory.groupby("symbol", sort=True):
        frames = []
        for path in group["file_path"].astype(str):
            frame = pd.read_parquet(path, columns=["callback_received_utc_ms", "trade_date", "symbol"])
            frames.append(frame)
        if not frames:
            continue
        dense = pd.concat(frames, ignore_index=True).sort_values(["trade_date", "callback_received_utc_ms"], kind="mergesort")
        dense["gap_ms"] = dense.groupby(["trade_date", "symbol"], sort=False)["callback_received_utc_ms"].diff()
        gaps = dense["gap_ms"].dropna()
        rows.append(
            {
                "symbol": str(symbol),
                "rows": int(len(dense)),
                "trade_dates": int(dense["trade_date"].nunique()),
                "median_gap_ms": float(gaps.median()) if not gaps.empty else np.nan,
                "p90_gap_ms": float(gaps.quantile(0.90)) if not gaps.empty else np.nan,
                "p95_gap_ms": float(gaps.quantile(0.95)) if not gaps.empty else np.nan,
                "gap_le_1s_fraction": float((gaps <= 1000).mean()) if not gaps.empty else np.nan,
            }
        )
    return pd.DataFrame(rows)


def build_comparison(profile: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    comparison = contract.merge(profile, on="symbol", how="left", suffixes=("_target", "_phase156"))
    comparison["phase156_to_target_p95_ratio"] = comparison["p95_gap_ms"] / comparison["target_median_p95_gap_ms"].replace(0, np.nan)
    comparison["phase106_to_target_p95_ratio"] = comparison["phase106_synthetic_p95_gap_ms"] / comparison["target_median_p95_gap_ms"].replace(0, np.nan)
    comparison["p95_gap_improved_vs_phase106"] = (comparison["p95_gap_ms"] > comparison["phase106_synthetic_p95_gap_ms"]).astype(int)
    comparison["p95_contract_band_pass"] = comparison["phase156_to_target_p95_ratio"].between(0.5, 2.0, inclusive="both").astype(int)
    comparison["gap_le_1s_fraction_delta"] = comparison["gap_le_1s_fraction"] - comparison["phase106_synthetic_gap_le_1s_fraction"]
    return comparison[
        [
            "symbol",
            "target_median_p95_gap_ms",
            "phase106_synthetic_p95_gap_ms",
            "p95_gap_ms",
            "phase106_to_target_p95_ratio",
            "phase156_to_target_p95_ratio",
            "p95_gap_improved_vs_phase106",
            "p95_contract_band_pass",
            "phase106_synthetic_gap_le_1s_fraction",
            "gap_le_1s_fraction",
            "gap_le_1s_fraction_delta",
        ]
    ].sort_values(["p95_contract_band_pass", "symbol"], ascending=[True, True], kind="mergesort")


def summarize(inventory: pd.DataFrame, comparison: pd.DataFrame, elapsed_seconds: float, profile_id: str) -> pd.DataFrame:
    symbols = int(comparison["symbol"].nunique()) if not comparison.empty else 0
    improved = int(comparison["p95_gap_improved_vs_phase106"].sum()) if not comparison.empty else 0
    band_pass = int(comparison["p95_contract_band_pass"].sum()) if not comparison.empty else 0
    return pd.DataFrame(
        [
            ("phase156_profile_id", profile_id, "Generator calibration profile smoke-tested"),
            ("phase156_smoke_symbols", symbols, "Representative high-multiplier symbols in bounded smoke"),
            ("phase156_smoke_partition_files", int(len(inventory)), "Dense smoke partition files materialized"),
            ("phase156_smoke_dense_rows", int(inventory["dense_rows"].sum()) if not inventory.empty else 0, "Dense rows materialized"),
            ("phase156_smoke_bytes", int(inventory["bytes"].sum()) if not inventory.empty else 0, "Compressed dense smoke bytes"),
            ("phase156_elapsed_seconds", float(elapsed_seconds), "Smoke materialization/profile elapsed seconds"),
            ("phase156_p95_improved_symbols", improved, "Smoke symbols whose p95 synthetic gap moved above Phase106 synthetic p95"),
            ("phase156_p95_contract_band_pass_symbols", band_pass, "Smoke symbols whose p95 synthetic gap is within [0.5,2.0] of Phase155 target"),
            ("phase156_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase156_next_best_action", "expand_phase156_profile_to_full_symbol_audit_then_rewire_phase106_cadence_anchors", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase156 Symbol-aware Tail Cadence Smoke",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase156 smoke-tests a generator profile whose symbol tail-gap multipliers come from the Phase155 full-partition cadence contract.",
        "It materializes a bounded local dense shard only. It does not run strategy replay, fills, P&L, or Azure reads.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase156_symbol_aware_tail_cadence_smoke_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase156(
    compact_root: Path,
    output_root: Path,
    phase155_dir: Path,
    output_dir: Path,
    base_dir: Path,
    symbols: list[str],
    multiplier: int,
    max_months: int,
    profile_id: str,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    contract = read_contract(phase155_dir / "phase155_symbol_cadence_calibration_contract.csv", symbols)
    inventory, elapsed_seconds = materialize_smoke(compact_root, output_root, symbols, multiplier, max_months, profile_id)
    profile = dense_profile(inventory)
    comparison = build_comparison(profile, contract)
    acceptance = summarize(inventory, comparison, elapsed_seconds, profile_id)

    inventory.to_csv(output_dir / "phase156_dense_smoke_inventory.csv", index=False)
    profile.to_csv(output_dir / "phase156_dense_smoke_cadence_profile.csv", index=False)
    comparison.to_csv(output_dir / "phase156_phase155_contract_smoke_comparison.csv", index=False)
    acceptance.to_csv(output_dir / "phase156_symbol_aware_tail_cadence_smoke_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Phase155 Contract Smoke Comparison": comparison,
            "Dense Smoke Inventory": inventory,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase156_symbol_aware_tail_cadence_smoke",
        **reproducibility_fields(
            artifact_id="phase156",
            generated_utc=generated_utc,
            inputs={
                "compact_root": str(compact_root),
                "phase155_contract": str(phase155_dir / "phase155_symbol_cadence_calibration_contract.csv"),
            },
            parameters={
                "profile_id": profile_id,
                "symbols": symbols,
                "multiplier": multiplier,
                "max_months": max_months,
                "strategy_replay_policy": "closed",
                "azure_read_policy": "forbidden_for_analysis_download_first_then_local",
            },
            outputs={
                "dense_output_root": str(output_root),
                "inventory": str(output_dir / "phase156_dense_smoke_inventory.csv"),
                "cadence_profile": str(output_dir / "phase156_dense_smoke_cadence_profile.csv"),
                "comparison": str(output_dir / "phase156_phase155_contract_smoke_comparison.csv"),
                "acceptance_summary": str(output_dir / "phase156_symbol_aware_tail_cadence_smoke_acceptance_summary.csv"),
                "report": str(output_dir / "phase156_symbol_aware_tail_cadence_smoke_report.md"),
                "manifest": str(output_dir / "phase156_symbol_aware_tail_cadence_smoke_manifest.json"),
            },
            random_seed="none_deterministic_phase156_dense_smoke",
            scenario_ids="phase156_representative_high_tail_gap_symbols",
            cost_model_version="not_applicable",
            latency_model_version="not_applicable_no_execution",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase156_symbol_aware_tail_cadence_smoke_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smoke-test Phase156 symbol-aware tail cadence generator profile.")
    parser.add_argument("--compact-root", type=Path, default=DEFAULT_COMPACT_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--phase155-dir", type=Path, default=DEFAULT_PHASE155_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--symbols", nargs="+", default=DEFAULT_SYMBOLS)
    parser.add_argument("--multiplier", type=int, default=64)
    parser.add_argument("--max-months", type=int, default=1)
    parser.add_argument("--profile-id", default=DEFAULT_PROFILE_ID)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase156(
        args.compact_root,
        args.output_root,
        args.phase155_dir,
        args.output_dir,
        args.base_dir,
        args.symbols,
        args.multiplier,
        args.max_months,
        args.profile_id,
    )


if __name__ == "__main__":
    main()
