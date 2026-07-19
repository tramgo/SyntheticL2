from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from synthetic_l2.generator_calibration_profiles import get_calibration_profile
from synthetic_l2.phase101_calibrated_phase49_shard_quality_audit import DEFAULT_COMPACT_ROOT
from synthetic_l2.phase103_calibrated_realism_rerun import (
    DEFAULT_OUTPUT_DIR as PHASE103_DEFAULT_OUTPUT_DIR,
    DEFAULT_REAL_ROOT,
    DEFAULT_SYMBOLS,
    run_phase103,
)
from synthetic_l2.phase49_dense_tick_rate_expansion import run_dense_expansion
from synthetic_l2.phase94_generator_realism_calibration_audit import (
    DEFAULT_MAX_REAL_FILES_PER_SYMBOL,
    DEFAULT_PHASE79_DIR,
    DEFAULT_PHASE80_DIR,
    DEFAULT_PHASE83_DIR,
    DEFAULT_PHASE93_DIR,
)


DEFAULT_PROFILE_ID = "P103_HDFCBANK_REAL_ANCHOR_CADENCE_VOL"
DEFAULT_OUTPUT_DIR = Path("outputs/phase104")
DEFAULT_DENSE_ROOT_BASE = Path("raw_synthetic_l2_phase104_real_anchor_cadence")


def rename_phase103_outputs(output_dir: Path) -> None:
    mapping = {
        "phase103_calibrated_realism_acceptance_summary.csv": "phase104_real_anchor_cadence_acceptance_summary.csv",
        "phase103_calibrated_realism_rerun_manifest.json": "phase104_real_anchor_cadence_profile_audit_manifest.json",
        "phase103_calibrated_realism_rerun_report.md": "phase104_real_anchor_cadence_profile_audit_report.md",
    }
    for old, new in mapping.items():
        old_path = output_dir / old
        if old_path.exists():
            old_path.replace(output_dir / new)


def add_phase104_summary(output_dir: Path, profile_id: str, inventory: pd.DataFrame, elapsed_seconds: float) -> None:
    acceptance_path = output_dir / "phase104_real_anchor_cadence_acceptance_summary.csv"
    acceptance = pd.read_csv(acceptance_path)
    extra = pd.DataFrame(
        [
            ("phase104_profile_id", profile_id, "Real-anchor cadence calibration profile materialized"),
            ("phase104_source_rows_densified", int(inventory["source_rows"].sum()), "Source compact rows densified"),
            ("phase104_dense_rows_materialized", int(inventory["dense_rows"].sum()), "Dense rows materialized for audit"),
            ("phase104_dense_bytes", int(inventory["bytes"].sum()), "Local dense parquet bytes materialized"),
            ("phase104_dense_elapsed_seconds", float(elapsed_seconds), "Dense materialization elapsed seconds"),
        ],
        columns=["metric", "value", "description"],
    )
    pd.concat([extra, acceptance], ignore_index=True).to_csv(acceptance_path, index=False)
    inventory.to_csv(output_dir / "phase104_dense_shard_inventory.csv", index=False)


def run_phase104(
    compact_root: Path,
    dense_root_base: Path,
    real_root: Path,
    output_dir: Path,
    base_dir: Path,
    symbols: list[str],
    profile_id: str,
    multiplier: int,
    max_real_files_per_symbol: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    profile = get_calibration_profile(profile_id)
    dense_root = dense_root_base / f"profile={profile_id}"
    inventory, elapsed_seconds = run_dense_expansion(
        compact_root,
        dense_root,
        symbols=symbols,
        multiplier=multiplier,
        calibration_profile=profile,
    )
    run_phase103(
        real_root=real_root,
        synthetic_dense_root=dense_root,
        phase79_dir=DEFAULT_PHASE79_DIR,
        phase80_dir=DEFAULT_PHASE80_DIR,
        phase83_dir=DEFAULT_PHASE83_DIR,
        phase93_dir=DEFAULT_PHASE93_DIR,
        output_dir=output_dir,
        base_dir=base_dir,
        symbols=symbols,
        max_real_files_per_symbol=max_real_files_per_symbol,
        profile_id=profile_id,
    )
    rename_phase103_outputs(output_dir)
    add_phase104_summary(output_dir, profile_id, inventory, elapsed_seconds)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize and audit real-anchor cadence calibrated dense profile.")
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


if __name__ == "__main__":
    main()
