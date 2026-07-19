from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from synthetic_l2.phase104_real_anchor_cadence_profile_audit import (
    DEFAULT_COMPACT_ROOT,
    DEFAULT_REAL_ROOT,
    DEFAULT_SYMBOLS,
    run_phase104,
)
from synthetic_l2.phase94_generator_realism_calibration_audit import DEFAULT_MAX_REAL_FILES_PER_SYMBOL


DEFAULT_PROFILE_ID = "P104_HDFCBANK_REAL_ANCHOR_CADENCE_VOL_PRICE_SCALE"
DEFAULT_OUTPUT_DIR = Path("outputs/phase105")
DEFAULT_DENSE_ROOT_BASE = Path("raw_synthetic_l2_phase105_source_mid_volatility_scale")


def rename_phase104_outputs(output_dir: Path) -> None:
    mapping = {
        "phase104_real_anchor_cadence_acceptance_summary.csv": "phase105_source_mid_volatility_acceptance_summary.csv",
        "phase104_real_anchor_cadence_profile_audit_manifest.json": "phase105_source_mid_volatility_scale_audit_manifest.json",
        "phase104_real_anchor_cadence_profile_audit_report.md": "phase105_source_mid_volatility_scale_audit_report.md",
        "phase104_dense_shard_inventory.csv": "phase105_dense_shard_inventory.csv",
    }
    for old, new in mapping.items():
        old_path = output_dir / old
        if old_path.exists():
            old_path.replace(output_dir / new)


def add_phase105_summary(output_dir: Path, profile_id: str) -> None:
    acceptance_path = output_dir / "phase105_source_mid_volatility_acceptance_summary.csv"
    comparison_path = output_dir / "real_vs_calibrated_synthetic_comparison.csv"
    acceptance = pd.read_csv(acceptance_path)
    comparison = pd.read_csv(comparison_path)
    gap_rows = int(comparison["calibration_gap"].astype(str).str.lower().eq("true").sum())
    vol_ratio = float(
        comparison.loc[comparison["metric"].astype(str).eq("one_tick_return_std"), "synthetic_to_real_ratio"].iloc[0]
    )
    median_gap_ratio = float(
        comparison.loc[comparison["metric"].astype(str).eq("median_gap_ms"), "synthetic_to_real_ratio"].iloc[0]
    )
    p90_gap_ratio = float(
        comparison.loc[comparison["metric"].astype(str).eq("p90_gap_ms"), "synthetic_to_real_ratio"].iloc[0]
    )
    phase105 = pd.DataFrame(
        [
            ("phase105_profile_id", profile_id, "Source-mid volatility scale profile audited"),
            ("phase105_anchor_metric_rows", int(len(comparison)), "Real-vs-calibrated synthetic anchor metrics compared"),
            ("phase105_calibration_gap_rows", gap_rows, "Anchor metrics outside gates"),
            ("phase105_median_gap_ratio", median_gap_ratio, "Synthetic/real median received tick gap ratio"),
            ("phase105_p90_gap_ratio", p90_gap_ratio, "Synthetic/real p90 received tick gap ratio"),
            ("phase105_one_tick_volatility_ratio", vol_ratio, "Synthetic/real one-tick mid-return volatility ratio"),
            ("phase105_hdfcbank_one_symbol_realism_pass", int(gap_rows == 0), "1 means HDFCBANK one-symbol realism readout has no metric gaps"),
            ("phase105_strategy_replay_allowed", 0, "Strategy replay remains closed until broader-symbol and multiday gates pass"),
        ],
        columns=["metric", "value", "description"],
    )
    pd.concat([phase105, acceptance], ignore_index=True).to_csv(acceptance_path, index=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit source-mid volatility scaled calibrated profile.")
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
    add_phase105_summary(args.output_dir, args.profile_id)


if __name__ == "__main__":
    main()
