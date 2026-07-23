from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE154_DIR = Path("outputs/phase154")
DEFAULT_PHASE106_DIR = Path("outputs/phase106")
DEFAULT_OUTPUT_DIR = Path("outputs/phase155")


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


def to_float(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").astype(float)


def aggregate_partition_targets(partitions: pd.DataFrame) -> pd.DataFrame:
    if partitions.empty:
        return pd.DataFrame(
            columns=[
                "exchange",
                "symbol",
                "target_median_p90_gap_ms",
                "target_max_p90_gap_ms",
                "target_median_p99_gap_ms",
                "target_max_gap_ms",
                "target_median_gap_le_100ms_fraction",
                "target_median_gap_le_500ms_fraction",
            ]
        )
    frame = partitions.copy()
    for column in [
        "p90_gap_ms",
        "p99_gap_ms",
        "max_gap_ms",
        "gap_le_100ms_fraction",
        "gap_le_500ms_fraction",
    ]:
        frame[column] = to_float(frame[column])
    return (
        frame.groupby(["exchange", "symbol"], sort=True)
        .agg(
            target_median_p90_gap_ms=("p90_gap_ms", "median"),
            target_max_p90_gap_ms=("p90_gap_ms", "max"),
            target_median_p99_gap_ms=("p99_gap_ms", "median"),
            target_max_gap_ms=("max_gap_ms", "max"),
            target_median_gap_le_100ms_fraction=("gap_le_100ms_fraction", "median"),
            target_median_gap_le_500ms_fraction=("gap_le_500ms_fraction", "median"),
        )
        .reset_index()
    )


def build_contract(phase154_symbols: pd.DataFrame, phase154_partitions: pd.DataFrame, synthetic: pd.DataFrame) -> pd.DataFrame:
    if phase154_symbols.empty:
        return pd.DataFrame()
    symbols = phase154_symbols.copy()
    for column in [
        "trade_dates",
        "rows",
        "gap_rows",
        "median_ticks_per_second",
        "median_gap_ms",
        "median_p95_gap_ms",
        "max_p95_gap_ms",
        "median_gap_le_1s_fraction",
        "max_gap_gt_5s_fraction",
    ]:
        symbols[column] = to_float(symbols[column])

    partition_targets = aggregate_partition_targets(phase154_partitions)
    contract = symbols.merge(partition_targets, on=["exchange", "symbol"], how="left")

    synthetic_keep = synthetic[
        [
            "symbol",
            "rows",
            "median_gap_ms",
            "p90_gap_ms",
            "p95_gap_ms",
            "gap_le_1s_fraction",
        ]
    ].copy()
    synthetic_keep = synthetic_keep.rename(
        columns={
            "rows": "phase106_synthetic_rows",
            "median_gap_ms": "phase106_synthetic_median_gap_ms",
            "p90_gap_ms": "phase106_synthetic_p90_gap_ms",
            "p95_gap_ms": "phase106_synthetic_p95_gap_ms",
            "gap_le_1s_fraction": "phase106_synthetic_gap_le_1s_fraction",
        }
    )
    for column in synthetic_keep.columns:
        if column != "symbol":
            synthetic_keep[column] = to_float(synthetic_keep[column])
    contract = contract.merge(synthetic_keep, on="symbol", how="left")

    contract = contract.rename(
        columns={
            "trade_dates": "real_anchor_trade_dates",
            "rows": "real_anchor_rows",
            "gap_rows": "real_anchor_gap_rows",
            "median_ticks_per_second": "target_median_ticks_per_second",
            "median_gap_ms": "target_median_gap_ms",
            "median_p95_gap_ms": "target_median_p95_gap_ms",
            "max_p95_gap_ms": "target_max_p95_gap_ms",
            "median_gap_le_1s_fraction": "target_median_gap_le_1s_fraction",
            "max_gap_gt_5s_fraction": "target_max_gap_gt_5s_fraction",
        }
    )

    contract["synthetic_to_full_p95_ratio"] = contract["phase106_synthetic_p95_gap_ms"] / contract["target_median_p95_gap_ms"].replace(0, np.nan)
    contract["synthetic_to_full_median_gap_ratio"] = contract["phase106_synthetic_median_gap_ms"] / contract["target_median_gap_ms"].replace(0, np.nan)
    contract["required_p95_gap_multiplier_vs_phase106"] = contract["target_median_p95_gap_ms"] / contract["phase106_synthetic_p95_gap_ms"].replace(0, np.nan)
    contract["required_p90_gap_multiplier_vs_phase106"] = contract["target_median_p90_gap_ms"] / contract["phase106_synthetic_p90_gap_ms"].replace(0, np.nan)
    contract["gap_le_1s_fraction_delta_vs_phase106"] = contract["phase106_synthetic_gap_le_1s_fraction"] - contract["target_median_gap_le_1s_fraction"]

    p95_ratio = contract["synthetic_to_full_p95_ratio"]
    median_ratio = contract["synthetic_to_full_median_gap_ratio"]
    gap_fraction_delta = contract["gap_le_1s_fraction_delta_vs_phase106"].abs()
    contract["phase106_cadence_contract_pass"] = (
        p95_ratio.between(0.5, 2.0, inclusive="both")
        & median_ratio.between(0.5, 2.0, inclusive="both")
        & gap_fraction_delta.le(0.20)
    ).astype(int)
    contract["cadence_patch_required"] = np.where(contract["phase106_cadence_contract_pass"].eq(1), 0, 1)
    contract["proposed_generator_change"] = np.where(
        contract["cadence_patch_required"].eq(1),
        "replace_global_dense_500ms_cadence_with_symbol_aware_idle_tail_gap_model",
        "keep_existing_cadence_for_symbol_after_verification",
    )
    contract["acceptance_gate"] = (
        "After generator patch, rerun a Phase106-style full-symbol realism audit using Phase154 full-partition cadence anchors; "
        "require p95-gap ratio in [0.5,2.0], median-gap ratio in [0.5,2.0], gap<=1s fraction delta <=0.20, zero failed partitions, and strategy replay still closed."
    )
    columns = [
        "exchange",
        "symbol",
        "real_anchor_trade_dates",
        "real_anchor_rows",
        "target_median_ticks_per_second",
        "target_median_gap_ms",
        "target_median_p90_gap_ms",
        "target_median_p95_gap_ms",
        "target_max_p95_gap_ms",
        "target_median_p99_gap_ms",
        "target_median_gap_le_100ms_fraction",
        "target_median_gap_le_500ms_fraction",
        "target_median_gap_le_1s_fraction",
        "target_max_gap_gt_5s_fraction",
        "phase106_synthetic_median_gap_ms",
        "phase106_synthetic_p90_gap_ms",
        "phase106_synthetic_p95_gap_ms",
        "phase106_synthetic_gap_le_1s_fraction",
        "synthetic_to_full_median_gap_ratio",
        "synthetic_to_full_p95_ratio",
        "gap_le_1s_fraction_delta_vs_phase106",
        "required_p90_gap_multiplier_vs_phase106",
        "required_p95_gap_multiplier_vs_phase106",
        "phase106_cadence_contract_pass",
        "cadence_patch_required",
        "proposed_generator_change",
        "acceptance_gate",
    ]
    return contract[columns].sort_values(["cadence_patch_required", "symbol"], ascending=[False, True], kind="mergesort")


def build_patch_summary(contract: pd.DataFrame) -> pd.DataFrame:
    if contract.empty:
        return pd.DataFrame(columns=["priority", "patch_item", "symbols_affected", "acceptance_gate"])
    patch_required = contract[contract["cadence_patch_required"].eq(1)].copy()
    rows: list[dict[str, Any]] = []
    if not patch_required.empty:
        rows.append(
            {
                "priority": 1,
                "patch_item": "symbol_aware_idle_tail_gap_model",
                "symbols_affected": int(patch_required["symbol"].nunique()),
                "median_required_p95_multiplier_vs_phase106": float(patch_required["required_p95_gap_multiplier_vs_phase106"].median()),
                "max_required_p95_multiplier_vs_phase106": float(patch_required["required_p95_gap_multiplier_vs_phase106"].max()),
                "representative_symbols": ";".join(patch_required.sort_values("required_p95_gap_multiplier_vs_phase106", ascending=False)["symbol"].head(8).astype(str)),
                "acceptance_gate": "Phase155 cadence contract passes after rerun from regenerated synthetic cadence profile; replay remains closed.",
            }
        )
    rows.append(
        {
            "priority": 2,
            "patch_item": "phase106_cadence_anchor_source_rewire",
            "symbols_affected": int(contract["symbol"].nunique()),
            "median_required_p95_multiplier_vs_phase106": "",
            "max_required_p95_multiplier_vs_phase106": "",
            "representative_symbols": "all_symbols",
            "acceptance_gate": "Future Phase106-style audits must use Phase154 full-partition cadence anchors instead of sampled Phase106 real_anchor_profile cadence rows.",
        }
    )
    return pd.DataFrame(rows)


def summarize(contract: pd.DataFrame, patch_summary: pd.DataFrame, phase154_dir: Path, phase106_dir: Path) -> pd.DataFrame:
    patch_required = contract[contract["cadence_patch_required"].eq(1)] if not contract.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("phase155_phase154_anchor_available", int((phase154_dir / "phase154_symbol_cadence_anchor.csv").exists()), "Phase154 full-partition symbol cadence anchors available"),
            ("phase155_phase106_synthetic_profile_available", int((phase106_dir / "calibrated_synthetic_anchor_profile.csv").exists()), "Phase106 calibrated synthetic anchor profile available"),
            ("phase155_symbols_in_contract", int(contract["symbol"].nunique()) if not contract.empty else 0, "Symbols with full-partition cadence contract rows"),
            ("phase155_cadence_patch_required_symbols", int(patch_required["symbol"].nunique()) if not patch_required.empty else 0, "Symbols whose existing Phase106 synthetic cadence fails the Phase154 contract"),
            ("phase155_contract_pass_symbols", int(contract["phase106_cadence_contract_pass"].sum()) if not contract.empty else 0, "Symbols whose existing Phase106 cadence already passes the full-partition contract"),
            ("phase155_patch_items", int(len(patch_summary)), "Patch contract items emitted"),
            (
                "phase155_median_required_p95_multiplier_vs_phase106",
                float(patch_required["required_p95_gap_multiplier_vs_phase106"].median()) if not patch_required.empty else 0.0,
                "Median p95 gap multiplier required versus the existing Phase106 synthetic cadence profile",
            ),
            (
                "phase155_max_required_p95_multiplier_vs_phase106",
                float(patch_required["required_p95_gap_multiplier_vs_phase106"].max()) if not patch_required.empty else 0.0,
                "Maximum p95 gap multiplier required versus the existing Phase106 synthetic cadence profile",
            ),
            (
                "phase155_inherited_phase154_sample_bias_flag_rows",
                metric_value(phase154_dir / "phase154_full_partition_real_cadence_anchor_acceptance_summary.csv", "phase154_sample_bias_flag_rows"),
                "Inherited Phase154 sample-bias rows showing sampled Phase106 cadence anchors are not safe targets",
            ),
            ("phase155_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            (
                "phase155_next_best_action",
                "implement_symbol_aware_idle_tail_gap_model_then_rerun_phase155_contract",
                "Recommended next milestone",
            ),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase155 Full-partition Cadence Calibration Contract",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase155 converts Phase154 full-partition real cadence anchors into a generator calibration contract.",
        "It supersedes sampled-file cadence targets for cadence calibration only.",
        "It does not connect to Azure, generate orders, model fills, compute P&L, or unlock strategy replay.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase155_full_partition_cadence_calibration_contract_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase155(phase154_dir: Path, phase106_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase154_symbols = read_csv(phase154_dir / "phase154_symbol_cadence_anchor.csv")
    phase154_partitions = read_csv(phase154_dir / "phase154_partition_cadence_profiles.csv")
    synthetic = read_csv(phase106_dir / "calibrated_synthetic_anchor_profile.csv")
    contract = build_contract(phase154_symbols, phase154_partitions, synthetic)
    patch_summary = build_patch_summary(contract)
    acceptance = summarize(contract, patch_summary, phase154_dir, phase106_dir)

    contract.to_csv(output_dir / "phase155_symbol_cadence_calibration_contract.csv", index=False)
    patch_summary.to_csv(output_dir / "phase155_generator_patch_contract.csv", index=False)
    acceptance.to_csv(output_dir / "phase155_full_partition_cadence_calibration_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Generator Patch Contract": patch_summary,
            "Symbol Cadence Calibration Contract": contract,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase155_full_partition_cadence_calibration_contract",
        **reproducibility_fields(
            artifact_id="phase155",
            generated_utc=generated_utc,
            inputs={
                "phase154_symbol_cadence_anchor": str(phase154_dir / "phase154_symbol_cadence_anchor.csv"),
                "phase154_partition_cadence_profiles": str(phase154_dir / "phase154_partition_cadence_profiles.csv"),
                "phase106_calibrated_synthetic_anchor_profile": str(phase106_dir / "calibrated_synthetic_anchor_profile.csv"),
            },
            parameters={
                "cadence_anchor_source": "phase154_full_local_partitions",
                "azure_read_policy": "forbidden_for_analysis_download_first_then_duckdb_local",
                "p95_gap_ratio_gate": "[0.5,2.0]",
                "median_gap_ratio_gate": "[0.5,2.0]",
                "gap_le_1s_fraction_delta_gate": "<=0.20",
                "strategy_replay_policy": "closed",
            },
            outputs={
                "symbol_contract": str(output_dir / "phase155_symbol_cadence_calibration_contract.csv"),
                "patch_contract": str(output_dir / "phase155_generator_patch_contract.csv"),
                "acceptance_summary": str(output_dir / "phase155_full_partition_cadence_calibration_acceptance_summary.csv"),
                "report": str(output_dir / "phase155_full_partition_cadence_calibration_contract_report.md"),
                "manifest": str(output_dir / "phase155_full_partition_cadence_calibration_contract_manifest.json"),
            },
            random_seed="none_deterministic_phase155_contract",
            scenario_ids="phase155_from_phase154_full_partition_cadence_anchors",
            cost_model_version="not_applicable",
            latency_model_version="not_applicable_no_execution",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase155_full_partition_cadence_calibration_contract_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build generator cadence calibration contract from Phase154 full-partition anchors.")
    parser.add_argument("--phase154-dir", type=Path, default=DEFAULT_PHASE154_DIR)
    parser.add_argument("--phase106-dir", type=Path, default=DEFAULT_PHASE106_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase155(args.phase154_dir, args.phase106_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
