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
DEFAULT_PHASE155_DIR = Path("outputs/phase155")
DEFAULT_PHASE156_DIR = Path("outputs/phase156")
DEFAULT_PHASE106_DIR = Path("outputs/phase106")
DEFAULT_OUTPUT_DIR = Path("outputs/phase157")


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


def as_float(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = frame.copy()
    for column in columns:
        if column in out.columns:
            out[column] = pd.to_numeric(out[column], errors="coerce").astype(float)
    return out


def build_rewire_matrix(
    phase154_symbols: pd.DataFrame,
    phase155_contract: pd.DataFrame,
    phase156_profile: pd.DataFrame,
    phase106_synthetic: pd.DataFrame,
) -> pd.DataFrame:
    anchors = as_float(
        phase154_symbols,
        [
            "rows",
            "median_gap_ms",
            "median_p95_gap_ms",
            "median_gap_le_1s_fraction",
        ],
    ).rename(
        columns={
            "rows": "phase154_full_partition_rows",
            "median_gap_ms": "phase154_target_median_gap_ms",
            "median_p95_gap_ms": "phase154_target_p95_gap_ms",
            "median_gap_le_1s_fraction": "phase154_target_gap_le_1s_fraction",
        }
    )
    contract = as_float(
        phase155_contract,
        [
            "target_median_gap_ms",
            "target_median_p95_gap_ms",
            "phase106_synthetic_p95_gap_ms",
            "phase106_synthetic_gap_le_1s_fraction",
            "synthetic_to_full_p95_ratio",
            "phase106_cadence_contract_pass",
        ],
    )
    smoke = as_float(
        phase156_profile,
        [
            "rows",
            "median_gap_ms",
            "p90_gap_ms",
            "p95_gap_ms",
            "gap_le_1s_fraction",
        ],
    ).rename(
        columns={
            "rows": "phase156_smoke_rows",
            "median_gap_ms": "phase156_synthetic_median_gap_ms",
            "p90_gap_ms": "phase156_synthetic_p90_gap_ms",
            "p95_gap_ms": "phase156_synthetic_p95_gap_ms",
            "gap_le_1s_fraction": "phase156_synthetic_gap_le_1s_fraction",
        }
    )
    synthetic106 = as_float(
        phase106_synthetic[["symbol", "p95_gap_ms", "gap_le_1s_fraction"]].copy(),
        ["p95_gap_ms", "gap_le_1s_fraction"],
    ).rename(
        columns={
            "p95_gap_ms": "phase106_profile_p95_gap_ms",
            "gap_le_1s_fraction": "phase106_profile_gap_le_1s_fraction",
        }
    )
    matrix = (
        anchors[
            [
                "exchange",
                "symbol",
                "phase154_full_partition_rows",
                "phase154_target_median_gap_ms",
                "phase154_target_p95_gap_ms",
                "phase154_target_gap_le_1s_fraction",
            ]
        ]
        .merge(
            contract[
                [
                    "symbol",
                    "target_median_gap_ms",
                    "target_median_p95_gap_ms",
                    "phase106_synthetic_p95_gap_ms",
                    "phase106_synthetic_gap_le_1s_fraction",
                    "synthetic_to_full_p95_ratio",
                    "phase106_cadence_contract_pass",
                ]
            ],
            on="symbol",
            how="left",
        )
        .merge(smoke[["symbol", "phase156_smoke_rows", "phase156_synthetic_median_gap_ms", "phase156_synthetic_p90_gap_ms", "phase156_synthetic_p95_gap_ms", "phase156_synthetic_gap_le_1s_fraction"]], on="symbol", how="left")
        .merge(synthetic106, on="symbol", how="left")
    )
    matrix["target_consistent_with_phase154"] = (
        np.isclose(matrix["target_median_p95_gap_ms"], matrix["phase154_target_p95_gap_ms"], rtol=0.0, atol=1e-6)
        & np.isclose(matrix["target_median_gap_ms"], matrix["phase154_target_median_gap_ms"], rtol=0.0, atol=1e-6)
    ).astype(int)
    matrix["phase156_to_full_p95_ratio"] = matrix["phase156_synthetic_p95_gap_ms"] / matrix["phase154_target_p95_gap_ms"].replace(0, np.nan)
    matrix["phase156_p95_contract_pass"] = matrix["phase156_to_full_p95_ratio"].between(0.5, 2.0, inclusive="both").astype(int)
    matrix["phase156_p95_exact_target_pass"] = np.isclose(
        matrix["phase156_synthetic_p95_gap_ms"],
        matrix["phase154_target_p95_gap_ms"],
        rtol=0.0,
        atol=1.0,
    ).astype(int)
    matrix["phase156_gap_le_1s_delta_vs_phase154"] = matrix["phase156_synthetic_gap_le_1s_fraction"] - matrix["phase154_target_gap_le_1s_fraction"]
    matrix["legacy_phase106_sampled_anchor_stale"] = 1
    matrix["future_cadence_anchor_source"] = "phase154_full_partition_symbol_cadence_anchor"
    matrix["cadence_rewire_pass"] = (
        matrix["target_consistent_with_phase154"].eq(1)
        & matrix["phase156_p95_contract_pass"].eq(1)
        & matrix["phase156_p95_exact_target_pass"].eq(1)
    ).astype(int)
    return matrix.sort_values(["cadence_rewire_pass", "symbol"], ascending=[True, True], kind="mergesort")


def build_metric_gate_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "metric": "median_gap_ms",
                "anchor_source": "phase154_symbol_cadence_anchor.target_median_gap_ms",
                "synthetic_source": "regenerated_synthetic_anchor_profile.median_gap_ms",
                "ratio_gate": "[0.5,2.0]",
                "rewire_status": "ready_for_phase106_style_audit_replacement",
            },
            {
                "metric": "p90_gap_ms",
                "anchor_source": "phase154_partition_cadence_profiles.target_median_p90_gap_ms",
                "synthetic_source": "regenerated_synthetic_anchor_profile.p90_gap_ms",
                "ratio_gate": "[0.5,2.0]",
                "rewire_status": "ready_for_phase106_style_audit_replacement_after_full_profile",
            },
            {
                "metric": "p95_gap_ms",
                "anchor_source": "phase154_symbol_cadence_anchor.target_median_p95_gap_ms",
                "synthetic_source": "regenerated_synthetic_anchor_profile.p95_gap_ms",
                "ratio_gate": "[0.5,2.0]",
                "rewire_status": "ready_for_phase106_style_audit_replacement",
            },
            {
                "metric": "gap_le_1s_fraction",
                "anchor_source": "phase154_symbol_cadence_anchor.target_median_gap_le_1s_fraction",
                "synthetic_source": "regenerated_synthetic_anchor_profile.gap_le_1s_fraction",
                "ratio_gate": "absolute_delta<=0.20",
                "rewire_status": "diagnostic_only_until_dense_frequency_model_is_distributional",
            },
            {
                "metric": "spread_depth_imbalance_volatility",
                "anchor_source": "existing_realism_audit_non_cadence_sources",
                "synthetic_source": "existing_synthetic_anchor_profile",
                "ratio_gate": "unchanged_existing_gates",
                "rewire_status": "not_modified_by_phase157",
            },
        ]
    )


def summarize(matrix: pd.DataFrame, phase154_dir: Path, phase155_dir: Path, phase156_dir: Path, phase106_dir: Path) -> pd.DataFrame:
    symbols = int(matrix["symbol"].nunique()) if not matrix.empty else 0
    rewire_pass = int(matrix["cadence_rewire_pass"].sum()) if not matrix.empty else 0
    p95_pass = int(matrix["phase156_p95_contract_pass"].sum()) if not matrix.empty else 0
    exact_pass = int(matrix["phase156_p95_exact_target_pass"].sum()) if not matrix.empty else 0
    stale_legacy = int(matrix["legacy_phase106_sampled_anchor_stale"].sum()) if not matrix.empty else 0
    return pd.DataFrame(
        [
            ("phase157_phase154_anchor_available", int((phase154_dir / "phase154_symbol_cadence_anchor.csv").exists()), "Phase154 full-partition anchor exists"),
            ("phase157_phase155_contract_available", int((phase155_dir / "phase155_symbol_cadence_calibration_contract.csv").exists()), "Phase155 full-partition cadence contract exists"),
            ("phase157_phase156_smoke_available", int((phase156_dir / "phase156_dense_smoke_cadence_profile.csv").exists()), "Phase156 regenerated synthetic cadence profile exists"),
            ("phase157_phase106_legacy_profile_available", int((phase106_dir / "calibrated_synthetic_anchor_profile.csv").exists()), "Legacy Phase106 synthetic profile exists for comparison"),
            ("phase157_symbols_audited", symbols, "Symbols audited for cadence rewire"),
            ("phase157_p95_contract_pass_symbols", p95_pass, "Symbols whose Phase156 p95 gap is inside the full-partition target band"),
            ("phase157_p95_exact_target_pass_symbols", exact_pass, "Symbols whose Phase156 p95 gap is within 1 ms of the Phase154/155 target"),
            ("phase157_cadence_rewire_pass_symbols", rewire_pass, "Symbols passing all cadence-rewire checks"),
            ("phase157_legacy_sampled_anchor_stale_symbols", stale_legacy, "Symbols for which legacy sampled cadence anchors must not be used"),
            (
                "phase157_inherited_phase154_sample_bias_flag_rows",
                metric_value(phase154_dir / "phase154_full_partition_real_cadence_anchor_acceptance_summary.csv", "phase154_sample_bias_flag_rows"),
                "Inherited Phase154 sample-bias rows",
            ),
            (
                "phase157_inherited_phase156_dense_rows",
                metric_value(phase156_dir / "phase156_symbol_aware_tail_cadence_smoke_acceptance_summary.csv", "phase156_smoke_dense_rows"),
                "Inherited Phase156 dense smoke rows",
            ),
            ("phase157_full_partition_cadence_rewire_ready", int(symbols > 0 and rewire_pass == symbols), "1 means cadence-slice anchor rewire is ready for Phase106-style audits"),
            ("phase157_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase157_next_best_action", "run_phase106_style_full_realism_audit_with_phase157_cadence_contract_and_non_cadence_gates", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase157 Full-partition Cadence Rewire Audit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase157 verifies that cadence targets for future Phase106-style audits can be sourced from Phase154 full local partitions.",
        "It audits cadence only. It does not claim spread, depth, imbalance, volatility, execution, fill, P&L, or strategy readiness.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase157_full_partition_cadence_rewire_audit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase157(
    phase154_dir: Path,
    phase155_dir: Path,
    phase156_dir: Path,
    phase106_dir: Path,
    output_dir: Path,
    base_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase154_symbols = read_csv(phase154_dir / "phase154_symbol_cadence_anchor.csv")
    phase155_contract = read_csv(phase155_dir / "phase155_symbol_cadence_calibration_contract.csv")
    phase156_profile = read_csv(phase156_dir / "phase156_dense_smoke_cadence_profile.csv")
    phase106_synthetic = read_csv(phase106_dir / "calibrated_synthetic_anchor_profile.csv")

    matrix = build_rewire_matrix(phase154_symbols, phase155_contract, phase156_profile, phase106_synthetic)
    metric_contract = build_metric_gate_contract()
    acceptance = summarize(matrix, phase154_dir, phase155_dir, phase156_dir, phase106_dir)

    matrix.to_csv(output_dir / "phase157_symbol_cadence_rewire_matrix.csv", index=False)
    metric_contract.to_csv(output_dir / "phase157_phase106_cadence_metric_source_contract.csv", index=False)
    acceptance.to_csv(output_dir / "phase157_full_partition_cadence_rewire_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Phase106 Cadence Metric Source Contract": metric_contract,
            "Symbol Cadence Rewire Matrix": matrix,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase157_full_partition_cadence_rewire_audit",
        **reproducibility_fields(
            artifact_id="phase157",
            generated_utc=generated_utc,
            inputs={
                "phase154_symbol_cadence_anchor": str(phase154_dir / "phase154_symbol_cadence_anchor.csv"),
                "phase155_symbol_cadence_contract": str(phase155_dir / "phase155_symbol_cadence_calibration_contract.csv"),
                "phase156_dense_smoke_cadence_profile": str(phase156_dir / "phase156_dense_smoke_cadence_profile.csv"),
                "phase106_legacy_synthetic_profile": str(phase106_dir / "calibrated_synthetic_anchor_profile.csv"),
            },
            parameters={
                "cadence_anchor_source": "phase154_full_partition_local_parquet_profiles",
                "legacy_sampled_cadence_anchor_policy": "do_not_use_for_future_cadence_calibration",
                "phase106_rewire_scope": "cadence_metrics_only",
                "strategy_replay_policy": "closed",
            },
            outputs={
                "rewire_matrix": str(output_dir / "phase157_symbol_cadence_rewire_matrix.csv"),
                "metric_source_contract": str(output_dir / "phase157_phase106_cadence_metric_source_contract.csv"),
                "acceptance_summary": str(output_dir / "phase157_full_partition_cadence_rewire_acceptance_summary.csv"),
                "report": str(output_dir / "phase157_full_partition_cadence_rewire_audit_report.md"),
                "manifest": str(output_dir / "phase157_full_partition_cadence_rewire_audit_manifest.json"),
            },
            random_seed="none_deterministic_phase157_rewire_audit",
            scenario_ids="phase157_phase154_phase155_phase156_cadence_rewire",
            cost_model_version="not_applicable",
            latency_model_version="not_applicable_no_execution",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase157_full_partition_cadence_rewire_audit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit full-partition cadence anchor rewire readiness.")
    parser.add_argument("--phase154-dir", type=Path, default=DEFAULT_PHASE154_DIR)
    parser.add_argument("--phase155-dir", type=Path, default=DEFAULT_PHASE155_DIR)
    parser.add_argument("--phase156-dir", type=Path, default=DEFAULT_PHASE156_DIR)
    parser.add_argument("--phase106-dir", type=Path, default=DEFAULT_PHASE106_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase157(args.phase154_dir, args.phase155_dir, args.phase156_dir, args.phase106_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
