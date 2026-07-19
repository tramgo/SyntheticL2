from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from synthetic_l2.phase106_full_symbol_calibrated_realism_audit import (
    DEFAULT_COMPACT_ROOT,
    DEFAULT_DENSE_ROOT_BASE,
    DEFAULT_MAX_REAL_FILES_PER_SYMBOL,
    DEFAULT_REAL_ROOT,
    DEFAULT_SYMBOLS,
    add_phase106_summary,
    rename_phase104_outputs,
)
from synthetic_l2.phase104_real_anchor_cadence_profile_audit import run_phase104


DEFAULT_PROFILE_ID = "P108_SYMBOL_AWARE_CADENCE_DEPTH_IMBALANCE"
DEFAULT_OUTPUT_DIR = Path("outputs/phase108")
DEFAULT_DENSE_ROOT_BASE = Path("raw_synthetic_l2_phase108_symbol_aware_generator_overrides")


def rename_phase106_outputs(output_dir: Path) -> None:
    mapping = {
        "phase106_full_symbol_calibrated_realism_acceptance_summary.csv": "phase108_symbol_aware_generator_override_acceptance_summary.csv",
        "phase106_full_symbol_calibrated_realism_audit_manifest.json": "phase108_symbol_aware_generator_override_audit_manifest.json",
        "phase106_full_symbol_calibrated_realism_audit_report.md": "phase108_symbol_aware_generator_override_audit_report.md",
        "phase106_dense_shard_inventory.csv": "phase108_dense_shard_inventory.csv",
    }
    for old, new in mapping.items():
        old_path = output_dir / old
        if old_path.exists():
            old_path.replace(output_dir / new)


def add_phase108_summary(output_dir: Path, profile_id: str) -> None:
    acceptance_path = output_dir / "phase108_symbol_aware_generator_override_acceptance_summary.csv"
    phase106_style = pd.read_csv(acceptance_path)
    metric = dict(zip(phase106_style["metric"].astype(str), phase106_style["value"].astype(str), strict=False))
    phase108 = pd.DataFrame(
        [
            ("phase108_profile_id", profile_id, "Symbol-aware cadence/depth/imbalance profile audited"),
            ("phase108_symbols_compared", metric.get("phase106_symbols_compared", "missing"), "Symbols compared in inherited Phase106-style audit"),
            ("phase108_anchor_metric_rows", metric.get("phase106_anchor_metric_rows", "missing"), "Anchor metrics compared"),
            ("phase108_calibration_gap_rows", metric.get("phase106_calibration_gap_rows", "missing"), "Anchor metrics outside gates"),
            ("phase108_calibration_gap_fraction", metric.get("phase106_calibration_gap_fraction", "missing"), "Fraction of anchor metrics outside gates"),
            ("phase108_severe_metric_gap_count", metric.get("phase106_severe_metric_gap_count", "missing"), "Metrics with gap_fraction > 50%"),
            ("phase108_failed_metrics", metric.get("phase106_failed_metrics", "missing"), "Metrics with one or more symbols outside gates"),
            ("phase108_full_symbol_calibrated_realism_pass", metric.get("phase106_full_symbol_calibrated_realism_pass", "missing"), "1 means Phase108 full-symbol realism audit passed"),
            ("phase108_strategy_replay_allowed", 0, "Strategy replay remains closed until broader and multiday gates pass"),
        ],
        columns=["metric", "value", "description"],
    )
    pd.concat([phase108, phase106_style], ignore_index=True).to_csv(acceptance_path, index=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase108 symbol-aware generator override audit.")
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
    rename_phase106_outputs(args.output_dir)
    add_phase108_summary(args.output_dir, args.profile_id)


if __name__ == "__main__":
    main()
