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


DEFAULT_OUTPUT_DIR = Path("outputs/phase153")
DEFAULT_PHASE106_DIR = Path("outputs/phase106")
DEFAULT_PHASE152_DIR = Path("outputs/phase152")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    value = rows.iloc[0]
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def safe_ratio(numerator: Any, denominator: Any) -> float:
    num = pd.to_numeric(pd.Series([numerator]), errors="coerce").iloc[0]
    den = pd.to_numeric(pd.Series([denominator]), errors="coerce").iloc[0]
    if pd.isna(num) or pd.isna(den) or float(den) == 0.0:
        return float("nan")
    return float(num) / float(den)


def classify_ratio_gap(ratio: float, lower: float = 0.80, upper: float = 1.25) -> str:
    if pd.isna(ratio):
        return "missing"
    if ratio < lower:
        return "synthetic_low_vs_real"
    if ratio > upper:
        return "synthetic_high_vs_real"
    return "within_band"


def classify_sample_bias(ratio: float, lower: float = 0.50, upper: float = 2.00) -> str:
    if pd.isna(ratio):
        return "missing"
    if ratio < lower:
        return "sampled_low_vs_full"
    if ratio > upper:
        return "sampled_high_vs_full"
    return "within_band"


def build_phase152_vs_phase106_real_sample_audit(phase152: pd.DataFrame, phase106_real: pd.DataFrame) -> pd.DataFrame:
    if phase152.empty or phase106_real.empty:
        return pd.DataFrame()
    left = phase152.copy()
    left["symbol"] = left["symbol"].astype(str)
    right = phase106_real.copy()
    right["symbol"] = right["symbol"].astype(str)
    merged = left.merge(right, on="symbol", suffixes=("_phase152_full_partition", "_phase106_sampled_anchor"), how="inner")
    rows: list[dict[str, Any]] = []
    for item in merged.to_dict("records"):
        for metric in ["median_gap_ms", "p95_gap_ms"]:
            full_value = item.get(f"{metric}_phase152_full_partition")
            sampled_value = item.get(f"{metric}_phase106_sampled_anchor")
            ratio = safe_ratio(sampled_value, full_value)
            rows.append(
                {
                    "symbol": item["symbol"],
                    "metric": metric,
                    "phase152_full_partition_value": full_value,
                    "phase106_sampled_anchor_value": sampled_value,
                    "sampled_to_full_ratio": ratio,
                    "sample_bias_flag": classify_sample_bias(ratio),
                    "interpretation": "older_sampled_anchor_may_overstate_tail_cadence_gap" if metric == "p95_gap_ms" and not pd.isna(ratio) and ratio > 2.0 else "no_large_sample_bias_flag",
                }
            )
    return pd.DataFrame(rows)


def build_real_vs_synthetic_gap(phase152: pd.DataFrame, synthetic: pd.DataFrame) -> pd.DataFrame:
    if phase152.empty or synthetic.empty:
        return pd.DataFrame()
    real = phase152.copy()
    real["symbol"] = real["symbol"].astype(str)
    synth = synthetic.copy()
    synth["symbol"] = synth["symbol"].astype(str)
    merged = real.merge(synth, on="symbol", suffixes=("_real_phase152", "_synthetic_phase106"), how="inner")
    rows: list[dict[str, Any]] = []
    metric_pairs = [
        ("median_gap_ms", "median_gap_ms", "received_tick_cadence_median_gap"),
        ("p95_gap_ms", "p95_gap_ms", "received_tick_cadence_tail_gap"),
    ]
    for item in merged.to_dict("records"):
        for real_metric, synth_metric, category in metric_pairs:
            real_value = item.get(f"{real_metric}_real_phase152")
            synthetic_value = item.get(f"{synth_metric}_synthetic_phase106")
            ratio = safe_ratio(synthetic_value, real_value)
            rows.append(
                {
                    "symbol": item["symbol"],
                    "category": category,
                    "real_metric": real_metric,
                    "synthetic_metric": synth_metric,
                    "real_phase152_value": real_value,
                    "synthetic_phase106_value": synthetic_value,
                    "synthetic_to_real_ratio": ratio,
                    "gap_flag": classify_ratio_gap(ratio),
                    "metric_basis": "phase152_full_local_partition_vs_phase106_calibrated_synthetic_anchor",
                }
            )
        real_l1_depth_proxy = (
            pd.to_numeric(pd.Series([item.get("avg_best_bid_qty")]), errors="coerce").iloc[0]
            + pd.to_numeric(pd.Series([item.get("avg_best_ask_qty")]), errors="coerce").iloc[0]
        )
        synthetic_l1_depth = item.get("median_l1_depth")
        ratio = safe_ratio(synthetic_l1_depth, real_l1_depth_proxy)
        rows.append(
            {
                "symbol": item["symbol"],
                "category": "displayed_l1_depth_scale_proxy",
                "real_metric": "avg_best_bid_qty_plus_avg_best_ask_qty",
                "synthetic_metric": "median_l1_depth",
                "real_phase152_value": real_l1_depth_proxy,
                "synthetic_phase106_value": synthetic_l1_depth,
                "synthetic_to_real_ratio": ratio,
                "gap_flag": classify_ratio_gap(ratio),
                "metric_basis": "proxy_only_depth_aggregation_differs",
            }
        )
    return pd.DataFrame(rows)


def build_recommendations(real_synthetic_gap: pd.DataFrame, sample_bias: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if not sample_bias.empty:
        tail_bias = sample_bias[
            sample_bias["metric"].astype(str).eq("p95_gap_ms")
            & sample_bias["sample_bias_flag"].astype(str).eq("sampled_high_vs_full")
        ]
        rows.append(
            {
                "recommendation_id": "P153_RECOMPUTE_REAL_CADENCE_ANCHORS_FROM_FULL_PARTITIONS",
                "priority": "high" if not tail_bias.empty else "medium",
                "evidence": f"{len(tail_bias)} profiled symbols show older sampled p95 gap much higher than Phase152 full partition p95 gap.",
                "action": "Use Phase152-style full-partition DuckDB profiles for future cadence calibration before changing generator cadence parameters.",
            }
        )
    if not real_synthetic_gap.empty:
        tail_low = real_synthetic_gap[
            real_synthetic_gap["category"].astype(str).eq("received_tick_cadence_tail_gap")
            & real_synthetic_gap["gap_flag"].astype(str).eq("synthetic_low_vs_real")
        ]
        depth_high = real_synthetic_gap[
            real_synthetic_gap["category"].astype(str).eq("displayed_l1_depth_scale_proxy")
            & real_synthetic_gap["gap_flag"].astype(str).eq("synthetic_high_vs_real")
        ]
        rows.append(
            {
                "recommendation_id": "P153_KEEP_REPLAY_CLOSED_USE_GAPS_FOR_GENERATOR_DIAGNOSTICS",
                "priority": "high",
                "evidence": f"tail cadence synthetic_low_vs_real rows={len(tail_low)}; displayed depth synthetic_high_vs_real proxy rows={len(depth_high)}.",
                "action": "Treat gaps as generator diagnostics only; do not open strategy replay or tune strategies to these selected partitions.",
            }
        )
    return pd.DataFrame(rows)


def summarize(real_synthetic_gap: pd.DataFrame, sample_bias: pd.DataFrame, recommendations: pd.DataFrame, phase106_summary: pd.DataFrame) -> pd.DataFrame:
    gap_rows = int(len(real_synthetic_gap))
    gap_flag_rows = int(real_synthetic_gap["gap_flag"].astype(str).ne("within_band").sum()) if not real_synthetic_gap.empty else 0
    sample_bias_rows = int(sample_bias["sample_bias_flag"].astype(str).ne("within_band").sum()) if not sample_bias.empty else 0
    severe_metric_gap_count = metric_value(phase106_summary, "phase106_severe_metric_gap_count", 0)
    return pd.DataFrame(
        [
            ("phase153_overlap_symbols", int(real_synthetic_gap["symbol"].nunique()) if not real_synthetic_gap.empty else 0, "Symbols compared between Phase152 full real profiles and Phase106 synthetic anchor"),
            ("phase153_real_synthetic_gap_rows", gap_rows, "Real-vs-synthetic metric comparison rows"),
            ("phase153_real_synthetic_gap_flag_rows", gap_flag_rows, "Real-vs-synthetic rows outside the 0.80-1.25 ratio band or missing"),
            ("phase153_sample_bias_rows", int(len(sample_bias)), "Phase152 full-partition vs Phase106 sampled-anchor comparison rows"),
            ("phase153_sample_bias_flag_rows", sample_bias_rows, "Sample-bias rows outside the 0.50-2.00 sampled/full ratio band or missing"),
            ("phase153_phase106_severe_metric_gap_count", severe_metric_gap_count, "Inherited Phase106 severe metric gap count"),
            ("phase153_recommendation_rows", int(len(recommendations)), "Generated diagnostic recommendations"),
            ("phase153_strategy_replay_allowed", 0, "Gap audit does not unlock strategy replay"),
            ("phase153_next_best_action", "recompute_real_anchor_cadence_profiles_from_full_partitions_after_phase148_downloads", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase153 Real-vs-synthetic Microstructure Gap Audit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase153 compares bounded Phase152 full-partition real microstructure profiles against Phase106 calibrated synthetic anchor metrics, and audits whether older sampled real-anchor cadence profiles may be biased.",
        "It is diagnostic-only: no strategy, no replay unlock, no P&L, no Azure I/O.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase153_real_synthetic_microstructure_gap_audit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase153(output_dir: Path, base_dir: Path, phase106_dir: Path, phase152_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase152_profiles = read_csv(phase152_dir / "phase152_microstructure_profiles.csv")
    phase106_real = read_csv(phase106_dir / "real_anchor_profile.csv")
    phase106_synthetic = read_csv(phase106_dir / "calibrated_synthetic_anchor_profile.csv")
    phase106_summary = read_csv(phase106_dir / "phase106_full_symbol_calibrated_realism_acceptance_summary.csv")
    sample_bias = build_phase152_vs_phase106_real_sample_audit(phase152_profiles, phase106_real)
    real_synthetic_gap = build_real_vs_synthetic_gap(phase152_profiles, phase106_synthetic)
    recommendations = build_recommendations(real_synthetic_gap, sample_bias)
    acceptance = summarize(real_synthetic_gap, sample_bias, recommendations, phase106_summary)

    sample_bias.to_csv(output_dir / "phase153_phase152_vs_phase106_real_sample_bias.csv", index=False)
    real_synthetic_gap.to_csv(output_dir / "phase153_real_synthetic_gap_matrix.csv", index=False)
    recommendations.to_csv(output_dir / "phase153_diagnostic_recommendations.csv", index=False)
    acceptance.to_csv(output_dir / "phase153_real_synthetic_microstructure_gap_audit_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Diagnostic Recommendations": recommendations,
            "Real-vs-synthetic Gap Matrix": real_synthetic_gap,
            "Phase152 vs Phase106 Real Sample Bias": sample_bias,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase153_real_synthetic_microstructure_gap_audit",
        **reproducibility_fields(
            artifact_id="phase153",
            generated_utc=generated_utc,
            inputs={
                "phase152_profiles": str(phase152_dir / "phase152_microstructure_profiles.csv"),
                "phase106_real_anchor_profile": str(phase106_dir / "real_anchor_profile.csv"),
                "phase106_synthetic_anchor_profile": str(phase106_dir / "calibrated_synthetic_anchor_profile.csv"),
                "phase106_summary": str(phase106_dir / "phase106_full_symbol_calibrated_realism_acceptance_summary.csv"),
            },
            parameters={
                "synthetic_to_real_ratio_band": "0.80_to_1.25",
                "sampled_to_full_ratio_band": "0.50_to_2.00",
                "strategy_replay_policy": "closed",
            },
            outputs={
                "sample_bias": str(output_dir / "phase153_phase152_vs_phase106_real_sample_bias.csv"),
                "real_synthetic_gap": str(output_dir / "phase153_real_synthetic_gap_matrix.csv"),
                "recommendations": str(output_dir / "phase153_diagnostic_recommendations.csv"),
                "acceptance_summary": str(output_dir / "phase153_real_synthetic_microstructure_gap_audit_acceptance_summary.csv"),
                "report": str(output_dir / "phase153_real_synthetic_microstructure_gap_audit_report.md"),
                "manifest": str(output_dir / "phase153_real_synthetic_microstructure_gap_audit_manifest.json"),
            },
            random_seed="none_deterministic_gap_audit",
            scenario_ids="phase153_real_synthetic_microstructure_gap_audit",
            cost_model_version="not_applicable",
            latency_model_version="not_applicable",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase153_real_synthetic_microstructure_gap_audit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit real-vs-synthetic microstructure gaps using Phase152 and Phase106 evidence.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--phase106-dir", type=Path, default=DEFAULT_PHASE106_DIR)
    parser.add_argument("--phase152-dir", type=Path, default=DEFAULT_PHASE152_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase153(args.output_dir, args.base_dir, args.phase106_dir, args.phase152_dir)


if __name__ == "__main__":
    main()
