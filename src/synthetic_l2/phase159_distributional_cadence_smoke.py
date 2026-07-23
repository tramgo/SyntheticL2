from __future__ import annotations

import argparse
import json
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.generator_calibration_profiles import get_calibration_profile
from synthetic_l2.phase156_symbol_aware_tail_cadence_smoke import (
    DEFAULT_COMPACT_ROOT,
    build_comparison,
    dense_profile,
    materialize_smoke,
)
from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase158_phase106_style_full_realism_audit import (
    build_gap_summary,
    build_non_cadence_comparison,
    build_remediation_queue,
    build_rewired_cadence_comparison,
    summarize,
)
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PROFILE_ID = "P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE"
DEFAULT_BASE_PROFILE_ID = "P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE"
DEFAULT_PHASE155_DIR = Path("outputs/phase155")
DEFAULT_PHASE106_DIR = Path("outputs/phase106")
DEFAULT_OUTPUT_DIR = Path("outputs/phase159")
DEFAULT_OUTPUT_ROOT = Path("raw_synthetic_l2_phase159_distributional_cadence_smoke")


def write_phase159_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase159 Distributional Cadence Smoke",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase159 smoke-tests a distributional generator cadence profile built from Phase155 full-partition targets.",
        "It allocates deterministic dense subtick gaps to median, p90, p95, and gap<=1s targets instead of pinning p95 alone.",
        "It materializes a bounded local dense shard only. It does not run strategy replay, fills, P&L, or Azure reads.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase159_distributional_cadence_smoke_report.md").write_text("\n".join(lines), encoding="utf-8")


def load_phase155_distribution_targets(phase155_dir: Path, symbols: list[str]) -> dict[str, dict[str, float]]:
    contract = pd.read_csv(phase155_dir / "phase155_symbol_cadence_calibration_contract.csv")
    if symbols:
        contract = contract[contract["symbol"].astype(str).isin(symbols)].copy()
    targets: dict[str, dict[str, float]] = {}
    for row in contract.to_dict("records"):
        targets[str(row["symbol"])] = {
            "median_gap_ms": float(row["target_median_gap_ms"]),
            "p90_gap_ms": float(row["target_median_p90_gap_ms"]),
            "p95_gap_ms": float(row["target_median_p95_gap_ms"]),
            "gap_le_1s_fraction": float(row["target_median_gap_le_1s_fraction"]),
        }
    return targets


def build_distributional_profile(phase155_dir: Path, symbols: list[str]):
    base = get_calibration_profile(DEFAULT_BASE_PROFILE_ID)
    targets = load_phase155_distribution_targets(phase155_dir, symbols)
    return replace(
        base,
        profile_id=DEFAULT_PROFILE_ID,
        symbol_dense_p95_gap_ms_overrides=None,
        symbol_dense_gap_distribution_overrides=targets,
    )


def run_phase159(
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
    profile = build_distributional_profile(phase155_dir, symbols)
    contract = pd.read_csv(phase155_dir / "phase155_symbol_cadence_calibration_contract.csv")
    contract = contract[contract["symbol"].astype(str).isin(symbols)].copy()
    inventory, elapsed_seconds = materialize_smoke(
        compact_root,
        output_root,
        symbols,
        multiplier,
        max_months,
        profile.profile_id,
        calibration_profile=profile,
    )
    synthetic_profile = dense_profile(inventory)
    cadence_comparison = build_comparison(synthetic_profile, contract)
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
    phase106_comparison = pd.read_csv(phase106_dir / "real_vs_calibrated_synthetic_comparison.csv")
    full_cadence = build_rewired_cadence_comparison(contract, phase157_like_matrix)
    non_cadence = build_non_cadence_comparison(phase106_comparison)
    full_comparison = pd.concat([full_cadence, non_cadence], ignore_index=True, sort=False)
    gaps = build_gap_summary(full_comparison)
    remediation = build_remediation_queue(gaps)
    acceptance = summarize(full_comparison, gaps, Path("outputs/phase157"))
    phase159_rows = pd.DataFrame(
        [
            ("phase159_profile_id", profile.profile_id, "Distributional cadence profile smoke-tested"),
            ("phase159_base_profile_id", DEFAULT_BASE_PROFILE_ID, "Base generator profile inherited"),
            ("phase159_smoke_symbols", int(synthetic_profile["symbol"].nunique()), "Symbols in distributional cadence smoke"),
            ("phase159_smoke_dense_rows", int(inventory["dense_rows"].sum()), "Dense rows materialized"),
            ("phase159_smoke_bytes", int(inventory["bytes"].sum()), "Compressed dense smoke bytes"),
            ("phase159_elapsed_seconds", float(elapsed_seconds), "Dense smoke elapsed seconds"),
        ],
        columns=["metric", "value", "description"],
    )
    acceptance = pd.concat([phase159_rows, acceptance], ignore_index=True)

    inventory.to_csv(output_dir / "phase159_dense_smoke_inventory.csv", index=False)
    synthetic_profile.to_csv(output_dir / "phase159_dense_smoke_cadence_profile.csv", index=False)
    cadence_comparison.to_csv(output_dir / "phase159_phase155_contract_smoke_comparison.csv", index=False)
    full_comparison.to_csv(output_dir / "phase159_rewired_realism_comparison.csv", index=False)
    gaps.to_csv(output_dir / "phase159_rewired_gap_summary.csv", index=False)
    remediation.to_csv(output_dir / "phase159_rewired_remediation_queue.csv", index=False)
    acceptance.to_csv(output_dir / "phase159_distributional_cadence_acceptance_summary.csv", index=False)
    write_phase159_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Distributional Cadence Profile": synthetic_profile,
            "Rewired Gap Summary": gaps,
            "Remediation Queue": remediation,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase159_distributional_cadence_smoke",
        **reproducibility_fields(
            artifact_id="phase159",
            generated_utc=generated_utc,
            inputs={
                "compact_root": str(compact_root),
                "phase155_contract": str(phase155_dir / "phase155_symbol_cadence_calibration_contract.csv"),
                "phase106_non_cadence_comparison": str(phase106_dir / "real_vs_calibrated_synthetic_comparison.csv"),
            },
            parameters={
                "profile_id": profile.profile_id,
                "base_profile_id": DEFAULT_BASE_PROFILE_ID,
                "symbols": symbols,
                "multiplier": multiplier,
                "max_months": max_months,
                "strategy_replay_policy": "closed",
            },
            outputs={
                "inventory": str(output_dir / "phase159_dense_smoke_inventory.csv"),
                "cadence_profile": str(output_dir / "phase159_dense_smoke_cadence_profile.csv"),
                "gap_summary": str(output_dir / "phase159_rewired_gap_summary.csv"),
                "acceptance_summary": str(output_dir / "phase159_distributional_cadence_acceptance_summary.csv"),
                "report": str(output_dir / "phase159_distributional_cadence_smoke_report.md"),
                "manifest": str(output_dir / "phase159_distributional_cadence_smoke_manifest.json"),
            },
            random_seed="none_deterministic_phase159_distributional_cadence",
            scenario_ids="phase159_full_symbol_distributional_cadence_smoke",
            cost_model_version="not_applicable",
            latency_model_version="not_applicable_no_execution",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase159_distributional_cadence_smoke_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase159 distributional cadence smoke.")
    parser.add_argument("--compact-root", type=Path, default=DEFAULT_COMPACT_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--phase155-dir", type=Path, default=DEFAULT_PHASE155_DIR)
    parser.add_argument("--phase106-dir", type=Path, default=DEFAULT_PHASE106_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--symbols", nargs="+", default=[])
    parser.add_argument("--multiplier", type=int, default=64)
    parser.add_argument("--max-months", type=int, default=1)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    symbols = args.symbols
    if not symbols:
        contract = pd.read_csv(args.phase155_dir / "phase155_symbol_cadence_calibration_contract.csv")
        symbols = sorted(contract["symbol"].astype(str).unique())
    run_phase159(args.compact_root, args.output_root, args.phase155_dir, args.phase106_dir, args.output_dir, args.base_dir, symbols, args.multiplier, args.max_months)


if __name__ == "__main__":
    main()
