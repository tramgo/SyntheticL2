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


DEFAULT_PHASE155_DIR = Path("outputs/phase155")
DEFAULT_PHASE157_DIR = Path("outputs/phase157")
DEFAULT_PHASE106_DIR = Path("outputs/phase106")
DEFAULT_OUTPUT_DIR = Path("outputs/phase158")


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


def ratio_gap(ratio: float, lower: float, upper: float) -> bool:
    if pd.isna(ratio) or not np.isfinite(ratio):
        return True
    return bool(ratio < lower or ratio > upper)


def delta_gap(delta: float, threshold: float) -> bool:
    if pd.isna(delta) or not np.isfinite(delta):
        return True
    return bool(abs(delta) > threshold)


def build_rewired_cadence_comparison(phase155_contract: pd.DataFrame, phase157_matrix: pd.DataFrame) -> pd.DataFrame:
    contract = phase155_contract.copy()
    matrix = phase157_matrix.copy()
    numeric_contract = [
        "target_median_gap_ms",
        "target_median_p90_gap_ms",
        "target_median_p95_gap_ms",
        "target_median_gap_le_1s_fraction",
    ]
    numeric_matrix = [
        "phase156_synthetic_median_gap_ms",
        "phase156_synthetic_p90_gap_ms",
        "phase156_synthetic_p95_gap_ms",
        "phase156_synthetic_gap_le_1s_fraction",
    ]
    for column in numeric_contract:
        contract[column] = pd.to_numeric(contract[column], errors="coerce")
    for column in numeric_matrix:
        matrix[column] = pd.to_numeric(matrix[column], errors="coerce")
    merged = contract[
        [
            "symbol",
            "target_median_gap_ms",
            "target_median_p90_gap_ms",
            "target_median_p95_gap_ms",
            "target_median_gap_le_1s_fraction",
        ]
    ].merge(
        matrix[
            [
                "symbol",
                "phase156_synthetic_median_gap_ms",
                "phase156_synthetic_p90_gap_ms",
                "phase156_synthetic_p95_gap_ms",
                "phase156_synthetic_gap_le_1s_fraction",
            ]
        ],
        on="symbol",
        how="inner",
    )
    rows: list[dict[str, Any]] = []
    ratio_metrics = [
        ("median_gap_ms", "target_median_gap_ms", "phase156_synthetic_median_gap_ms", 0.5, 2.0, "rewired received tick cadence"),
        ("p90_gap_ms", "target_median_p90_gap_ms", "phase156_synthetic_p90_gap_ms", 0.5, 2.0, "rewired tail received tick cadence"),
        ("p95_gap_ms", "target_median_p95_gap_ms", "phase156_synthetic_p95_gap_ms", 0.5, 2.0, "rewired tail received tick cadence"),
    ]
    for row in merged.to_dict("records"):
        for metric, real_col, synth_col, lower, upper, category in ratio_metrics:
            real_value = float(row[real_col])
            synthetic_value = float(row[synth_col])
            ratio = synthetic_value / real_value if real_value > 0 else np.nan
            rows.append(
                {
                    "symbol": row["symbol"],
                    "category": category,
                    "metric": metric,
                    "real_value": real_value,
                    "synthetic_value": synthetic_value,
                    "synthetic_to_real_ratio": ratio,
                    "lower_ratio_gate": lower,
                    "upper_ratio_gate": upper,
                    "calibration_gap": ratio_gap(ratio, lower, upper),
                    "anchor_source": "phase154_full_partition_via_phase155_phase157",
                    "synthetic_source": "phase156_symbol_tail_cadence_smoke",
                    "gate_type": "ratio",
                }
            )
        real_fraction = float(row["target_median_gap_le_1s_fraction"])
        synthetic_fraction = float(row["phase156_synthetic_gap_le_1s_fraction"])
        delta = synthetic_fraction - real_fraction
        rows.append(
            {
                "symbol": row["symbol"],
                "category": "rewired received tick cadence distribution",
                "metric": "gap_le_1s_fraction",
                "real_value": real_fraction,
                "synthetic_value": synthetic_fraction,
                "synthetic_to_real_ratio": synthetic_fraction / real_fraction if real_fraction > 0 else np.nan,
                "lower_ratio_gate": -0.20,
                "upper_ratio_gate": 0.20,
                "calibration_gap": delta_gap(delta, 0.20),
                "anchor_source": "phase154_full_partition_via_phase155_phase157",
                "synthetic_source": "phase156_symbol_tail_cadence_smoke",
                "gate_type": "absolute_delta",
                "absolute_delta": delta,
            }
        )
    return pd.DataFrame(rows)


def build_non_cadence_comparison(phase106_comparison: pd.DataFrame) -> pd.DataFrame:
    non_cadence_metrics = {
        "median_spread_bps",
        "p90_spread_bps",
        "median_l1_depth",
        "median_l5_depth",
        "median_abs_l1_imbalance",
        "one_tick_return_std",
    }
    frame = phase106_comparison[phase106_comparison["metric"].astype(str).isin(non_cadence_metrics)].copy()
    frame["anchor_source"] = "phase106_existing_non_cadence_real_anchor"
    frame["synthetic_source"] = "phase106_existing_synthetic_anchor_profile"
    frame["gate_type"] = "ratio"
    if "absolute_delta" not in frame.columns:
        frame["absolute_delta"] = np.nan
    return frame


def build_gap_summary(comparison: pd.DataFrame) -> pd.DataFrame:
    frame = comparison.copy()
    frame["calibration_gap_bool"] = frame["calibration_gap"].astype(str).str.lower().isin(["true", "1"])
    return (
        frame.groupby(["category", "metric", "anchor_source"], sort=True)
        .agg(
            symbol_metrics=("symbol", "count"),
            gap_count=("calibration_gap_bool", "sum"),
            gap_fraction=("calibration_gap_bool", "mean"),
            median_synthetic_to_real_ratio=("synthetic_to_real_ratio", "median"),
            min_synthetic_to_real_ratio=("synthetic_to_real_ratio", "min"),
            max_synthetic_to_real_ratio=("synthetic_to_real_ratio", "max"),
        )
        .reset_index()
    )


def build_remediation_queue(gap_summary: pd.DataFrame) -> pd.DataFrame:
    failed = gap_summary[pd.to_numeric(gap_summary["gap_count"], errors="coerce").gt(0)].copy()
    failed = failed.sort_values(["gap_fraction", "gap_count", "metric"], ascending=[False, False, True], kind="mergesort")
    rows: list[dict[str, Any]] = []
    for priority, row in enumerate(failed.to_dict("records"), start=1):
        metric = str(row["metric"])
        if metric == "p90_gap_ms":
            work_item = "add_distributional_tail_cadence_model_not_only_p95_point_target"
            rationale = "Phase156 pins p95 but leaves p90 too dense for many symbols."
        elif metric == "gap_le_1s_fraction":
            work_item = "calibrate_idle_gap_frequency_to_match_gap_distribution"
            rationale = "Phase156 p95 idle gaps reduce dense-overstatement but the <=1s fraction remains too high/low for part of the universe."
        elif metric == "median_gap_ms":
            work_item = "calibrate_symbol_median_cadence_without_breaking_p95_targets"
            rationale = "Phase156 pins p95 but keeps median gaps at the dense 500ms baseline for slower symbols."
        elif metric in {"median_l1_depth", "median_l5_depth"}:
            work_item = "revisit_symbol_depth_scale_overrides_with_full_partition_non_cadence_anchors"
            rationale = "Existing non-cadence depth gates are preserved and still show symbol failures."
        elif metric == "median_abs_l1_imbalance":
            work_item = "revisit_l1_imbalance_floor_and_side_skew_model"
            rationale = "Existing imbalance gates are preserved and remain a broad non-cadence blocker."
        else:
            work_item = f"remediate_{metric}"
            rationale = "Preserved Phase106-style gate still has failures."
        rows.append(
            {
                "priority": priority,
                "metric": metric,
                "work_item": work_item,
                "gap_count": int(row["gap_count"]),
                "gap_fraction": float(row["gap_fraction"]),
                "rationale": rationale,
            }
        )
    return pd.DataFrame(rows)


def summarize(comparison: pd.DataFrame, gap_summary: pd.DataFrame, phase157_dir: Path) -> pd.DataFrame:
    frame = comparison.copy()
    frame["calibration_gap_bool"] = frame["calibration_gap"].astype(str).str.lower().isin(["true", "1"])
    cadence = frame[frame["anchor_source"].astype(str).str.contains("phase154_full_partition", na=False)]
    non_cadence = frame[~frame.index.isin(cadence.index)]
    compared_symbols = int(frame["symbol"].nunique()) if not frame.empty else 0
    anchor_rows = int(len(frame))
    gap_rows = int(frame["calibration_gap_bool"].sum()) if anchor_rows else 0
    gap_fraction = float(gap_rows / anchor_rows) if anchor_rows else 1.0
    severe_metric_count = int((gap_summary["gap_fraction"].astype(float) > 0.50).sum()) if not gap_summary.empty else 0
    cadence_gap_rows = int(cadence["calibration_gap_bool"].sum()) if not cadence.empty else 0
    non_cadence_gap_rows = int(non_cadence["calibration_gap_bool"].sum()) if not non_cadence.empty else 0
    pass_full = bool(compared_symbols >= 32 and gap_fraction <= 0.25 and severe_metric_count == 0)
    return pd.DataFrame(
        [
            ("phase158_phase157_rewire_ready", metric_value(phase157_dir / "phase157_full_partition_cadence_rewire_acceptance_summary.csv", "phase157_full_partition_cadence_rewire_ready"), "Inherited Phase157 cadence rewire readiness"),
            ("phase158_symbols_compared", compared_symbols, "Symbols present in full rewired realism audit"),
            ("phase158_anchor_metric_rows", anchor_rows, "Symbol/metric anchor rows compared"),
            ("phase158_calibration_gap_rows", gap_rows, "Rows outside Phase158 gates"),
            ("phase158_calibration_gap_fraction", gap_fraction, "Fraction of rows outside Phase158 gates"),
            ("phase158_severe_metric_gap_count", severe_metric_count, "Metrics with gap_fraction > 50%"),
            ("phase158_cadence_gap_rows", cadence_gap_rows, "Cadence rows outside full-partition cadence gates"),
            ("phase158_non_cadence_gap_rows", non_cadence_gap_rows, "Preserved non-cadence rows outside existing gates"),
            ("phase158_full_rewired_realism_pass", int(pass_full), "1 means full rewired realism audit passes"),
            ("phase158_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase158_next_best_action", "fix_phase158_remaining_distributional_cadence_depth_imbalance_gaps_before_strategy_replay", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase158 Phase106-style Full Realism Audit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase158 reruns the Phase106-style realism decision using Phase157 full-partition cadence anchors for cadence metrics and preserved Phase106 non-cadence gates for spread, depth, imbalance, and volatility.",
        "It is an audit only: no strategy replay, no fills, no P&L, and no Azure reads.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase158_phase106_style_full_realism_audit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase158(phase155_dir: Path, phase157_dir: Path, phase106_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase155_contract = read_csv(phase155_dir / "phase155_symbol_cadence_calibration_contract.csv")
    phase157_matrix = read_csv(phase157_dir / "phase157_symbol_cadence_rewire_matrix.csv")
    phase106_comparison = read_csv(phase106_dir / "real_vs_calibrated_synthetic_comparison.csv")
    cadence = build_rewired_cadence_comparison(phase155_contract, phase157_matrix)
    non_cadence = build_non_cadence_comparison(phase106_comparison)
    comparison = pd.concat([cadence, non_cadence], ignore_index=True, sort=False)
    gaps = build_gap_summary(comparison)
    remediation = build_remediation_queue(gaps)
    acceptance = summarize(comparison, gaps, phase157_dir)

    comparison.to_csv(output_dir / "phase158_rewired_realism_comparison.csv", index=False)
    gaps.to_csv(output_dir / "phase158_rewired_gap_summary.csv", index=False)
    remediation.to_csv(output_dir / "phase158_rewired_remediation_queue.csv", index=False)
    acceptance.to_csv(output_dir / "phase158_phase106_style_full_realism_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Gap Summary": gaps,
            "Remediation Queue": remediation,
            "Rewired Realism Comparison": comparison,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase158_phase106_style_full_realism_audit",
        **reproducibility_fields(
            artifact_id="phase158",
            generated_utc=generated_utc,
            inputs={
                "phase155_cadence_contract": str(phase155_dir / "phase155_symbol_cadence_calibration_contract.csv"),
                "phase157_cadence_rewire_matrix": str(phase157_dir / "phase157_symbol_cadence_rewire_matrix.csv"),
                "phase106_legacy_comparison": str(phase106_dir / "real_vs_calibrated_synthetic_comparison.csv"),
            },
            parameters={
                "cadence_metrics": "phase157_full_partition_rewired",
                "non_cadence_metrics": "phase106_existing_gates_preserved",
                "strategy_replay_policy": "closed",
            },
            outputs={
                "comparison": str(output_dir / "phase158_rewired_realism_comparison.csv"),
                "gap_summary": str(output_dir / "phase158_rewired_gap_summary.csv"),
                "remediation_queue": str(output_dir / "phase158_rewired_remediation_queue.csv"),
                "acceptance_summary": str(output_dir / "phase158_phase106_style_full_realism_acceptance_summary.csv"),
                "report": str(output_dir / "phase158_phase106_style_full_realism_audit_report.md"),
                "manifest": str(output_dir / "phase158_phase106_style_full_realism_audit_manifest.json"),
            },
            random_seed="none_deterministic_phase158_audit",
            scenario_ids="phase158_phase157_cadence_plus_phase106_non_cadence",
            cost_model_version="not_applicable",
            latency_model_version="not_applicable_no_execution",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase158_phase106_style_full_realism_audit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase106-style full realism audit with Phase157 rewired cadence metrics.")
    parser.add_argument("--phase155-dir", type=Path, default=DEFAULT_PHASE155_DIR)
    parser.add_argument("--phase157-dir", type=Path, default=DEFAULT_PHASE157_DIR)
    parser.add_argument("--phase106-dir", type=Path, default=DEFAULT_PHASE106_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase158(args.phase155_dir, args.phase157_dir, args.phase106_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
