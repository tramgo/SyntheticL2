from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from synthetic_l2.phase104_real_anchor_cadence_profile_audit import DEFAULT_COMPACT_ROOT, DEFAULT_REAL_ROOT, run_phase104


DEFAULT_PROFILE_ID = "P104_HDFCBANK_REAL_ANCHOR_CADENCE_VOL_PRICE_SCALE"
DEFAULT_OUTPUT_DIR = Path("outputs/phase106")
DEFAULT_DENSE_ROOT_BASE = Path("raw_synthetic_l2_phase106_full_symbol_calibrated_realism")
DEFAULT_MAX_REAL_FILES_PER_SYMBOL = 50
DEFAULT_SYMBOLS = [
    "ADANIPORTS",
    "AXISBANK",
    "BAJAJ-AUTO",
    "BANKBEES",
    "BHARTIARTL",
    "BPCL",
    "BRITANNIA",
    "CIPLA",
    "DRREDDY",
    "GOLDBEES",
    "HCLTECH",
    "HDFCBANK",
    "HINDUNILVR",
    "ICICIBANK",
    "INFY",
    "ITBEES",
    "ITC",
    "JUNIORBEES",
    "KOTAKBANK",
    "LT",
    "M&M",
    "MARUTI",
    "NESTLEIND",
    "NIFTYBEES",
    "ONGC",
    "RELIANCE",
    "SBIN",
    "SUNPHARMA",
    "TCS",
    "TECHM",
    "ULTRACEMCO",
    "WIPRO",
]


def rename_phase104_outputs(output_dir: Path) -> None:
    mapping = {
        "phase104_real_anchor_cadence_acceptance_summary.csv": "phase106_full_symbol_calibrated_realism_acceptance_summary.csv",
        "phase104_real_anchor_cadence_profile_audit_manifest.json": "phase106_full_symbol_calibrated_realism_audit_manifest.json",
        "phase104_real_anchor_cadence_profile_audit_report.md": "phase106_full_symbol_calibrated_realism_audit_report.md",
        "phase104_dense_shard_inventory.csv": "phase106_dense_shard_inventory.csv",
    }
    for old, new in mapping.items():
        old_path = output_dir / old
        if old_path.exists():
            old_path.replace(output_dir / new)


def add_phase106_summary(output_dir: Path, profile_id: str, max_real_files_per_symbol: int) -> None:
    acceptance_path = output_dir / "phase106_full_symbol_calibrated_realism_acceptance_summary.csv"
    comparison_path = output_dir / "real_vs_calibrated_synthetic_comparison.csv"
    gap_summary_path = output_dir / "calibrated_gap_summary.csv"
    inventory_path = output_dir / "phase106_dense_shard_inventory.csv"
    acceptance = pd.read_csv(acceptance_path)
    comparison = pd.read_csv(comparison_path)
    gaps = pd.read_csv(gap_summary_path)
    inventory = pd.read_csv(inventory_path)
    comparison["gap_bool"] = comparison["calibration_gap"].astype(str).str.lower().eq("true")
    gap_rows = int(comparison["gap_bool"].sum())
    anchor_rows = int(len(comparison))
    gap_fraction = float(gap_rows / anchor_rows) if anchor_rows else 1.0
    severe_metric_count = int((gaps["gap_fraction"].astype(float) > 0.50).sum()) if not gaps.empty else 0
    compared_symbols = int(comparison["symbol"].nunique()) if not comparison.empty else 0
    pass_full_symbol = bool(compared_symbols >= 32 and gap_fraction <= 0.25 and severe_metric_count == 0)
    failed_metrics = (
        gaps.loc[gaps["gap_count"].astype(float) > 0, "metric"].astype(str).sort_values().tolist()
        if not gaps.empty
        else []
    )
    phase106 = pd.DataFrame(
        [
            ("phase106_profile_id", profile_id, "Calibrated synthetic profile audited across full symbol set"),
            ("phase106_max_real_files_per_symbol", max_real_files_per_symbol, "Bounded real parquet sample per symbol"),
            ("phase106_symbols_compared", compared_symbols, "Symbols present in real and calibrated synthetic anchors"),
            ("phase106_anchor_metric_rows", anchor_rows, "Real-vs-calibrated synthetic anchor metrics compared"),
            ("phase106_calibration_gap_rows", gap_rows, "Anchor metrics outside ratio gates"),
            ("phase106_calibration_gap_fraction", gap_fraction, "Fraction of anchor metrics outside gates"),
            ("phase106_severe_metric_gap_count", severe_metric_count, "Metrics with gap_fraction > 50%"),
            ("phase106_failed_metrics", ";".join(failed_metrics), "Metrics with one or more symbols outside gates"),
            ("phase106_source_rows_densified", int(inventory["source_rows"].sum()), "Source compact rows densified"),
            ("phase106_dense_rows_materialized", int(inventory["dense_rows"].sum()), "Dense rows materialized for audit"),
            ("phase106_dense_bytes", int(inventory["bytes"].sum()), "Local dense parquet bytes materialized"),
            ("phase106_full_symbol_calibrated_realism_pass", int(pass_full_symbol), "1 means full-symbol calibrated realism audit passed"),
            ("phase106_strategy_replay_allowed", 0, "Strategy replay remains closed until full-symbol and multiday gates pass"),
        ],
        columns=["metric", "value", "description"],
    )
    pd.concat([phase106, acceptance], ignore_index=True).to_csv(acceptance_path, index=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run full-symbol calibrated real-vs-synthetic realism audit.")
    parser.add_argument("--compact-root", type=Path, default=DEFAULT_COMPACT_ROOT)
    parser.add_argument("--dense-root-base", type=Path, default=DEFAULT_DENSE_ROOT_BASE)
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--symbols", nargs="+", default=DEFAULT_SYMBOLS)
    parser.add_argument("--profile-id", default=DEFAULT_PROFILE_ID)
    parser.add_argument("--multiplier", type=int, default=8)
    parser.add_argument("--max-real-files-per-symbol", type=int, default=DEFAULT_MAX_REAL_FILES_PER_SYMBOL)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase104(
        args.compact_root,
        args.dense_root_base,
        args.real_root,
        args.output_dir,
        args.base_dir,
        args.symbols,
        args.profile_id,
        args.multiplier,
        args.max_real_files_per_symbol,
    )
    rename_phase104_outputs(args.output_dir)
    add_phase106_summary(args.output_dir, args.profile_id, args.max_real_files_per_symbol)


if __name__ == "__main__":
    main()
