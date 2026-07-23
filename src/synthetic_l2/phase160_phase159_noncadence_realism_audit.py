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


DEFAULT_PHASE159_DIR = Path("outputs/phase159")
DEFAULT_PHASE106_DIR = Path("outputs/phase106")
DEFAULT_OUTPUT_DIR = Path("outputs/phase160")


NON_CADENCE_METRICS = [
    ("median_spread_bps", 0.25, 4.0, "median spread scale"),
    ("p90_spread_bps", 0.25, 4.0, "tail spread scale"),
    ("median_l1_depth", 0.10, 10.0, "displayed L1 depth scale"),
    ("median_l5_depth", 0.10, 10.0, "displayed L5 depth scale"),
    ("median_abs_l1_imbalance", 0.25, 4.0, "L1 imbalance scale"),
    ("one_tick_return_std", 0.10, 10.0, "one-tick volatility scale"),
]


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


def synthetic_noncadence_profile(inventory: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    columns = [
        "symbol",
        "trade_date",
        "callback_received_utc_ms",
        "buy_1_price",
        "sell_1_price",
        "buy_1_quantity",
        "sell_1_quantity",
        "buy_2_quantity",
        "sell_2_quantity",
        "buy_3_quantity",
        "sell_3_quantity",
        "buy_4_quantity",
        "sell_4_quantity",
        "buy_5_quantity",
        "sell_5_quantity",
    ]
    for symbol, group in inventory.groupby("symbol", sort=True):
        frames = []
        for file_path in group["file_path"].astype(str):
            frames.append(pd.read_parquet(file_path, columns=columns))
        if not frames:
            continue
        raw = pd.concat(frames, ignore_index=True)
        raw = raw[(raw["buy_1_price"] > 0) & (raw["sell_1_price"] > 0) & (raw["sell_1_price"] >= raw["buy_1_price"])].copy()
        raw = raw.sort_values(["trade_date", "callback_received_utc_ms"], kind="mergesort")
        mid = (raw["buy_1_price"].astype(float) + raw["sell_1_price"].astype(float)) / 2.0
        spread = (raw["sell_1_price"].astype(float) - raw["buy_1_price"].astype(float)).clip(lower=0.0)
        l1_depth = raw["buy_1_quantity"].astype(float) + raw["sell_1_quantity"].astype(float)
        l5_depth = sum(raw[f"buy_{level}_quantity"].astype(float) + raw[f"sell_{level}_quantity"].astype(float) for level in range(1, 6))
        l1_imbalance = (raw["buy_1_quantity"].astype(float) - raw["sell_1_quantity"].astype(float)) / l1_depth.replace(0, np.nan)
        tick_return = mid.groupby([raw["trade_date"], raw["symbol"]], sort=False).pct_change()
        rows.append(
            {
                "symbol": str(symbol),
                "rows": int(len(raw)),
                "trade_dates": int(raw["trade_date"].nunique()),
                "median_spread_bps": float((spread / mid.replace(0, np.nan) * 10000.0).median()),
                "p90_spread_bps": float((spread / mid.replace(0, np.nan) * 10000.0).quantile(0.90)),
                "median_l1_depth": float(l1_depth.median()),
                "median_l5_depth": float(l5_depth.median()),
                "median_abs_l1_imbalance": float(l1_imbalance.abs().median()),
                "one_tick_return_std": float(tick_return.std(ddof=1)),
            }
        )
    return pd.DataFrame(rows)


def real_noncadence_profile_from_phase106(comparison: pd.DataFrame) -> pd.DataFrame:
    pivot = comparison[comparison["metric"].isin([metric for metric, *_ in NON_CADENCE_METRICS])].pivot_table(
        index="symbol",
        columns="metric",
        values="real_value",
        aggfunc="first",
    )
    return pivot.reset_index()


def build_comparison(real: pd.DataFrame, synthetic: pd.DataFrame) -> pd.DataFrame:
    merged = real.merge(synthetic, on="symbol", how="inner", suffixes=("_real", "_synthetic"))
    rows: list[dict[str, Any]] = []
    for row in merged.to_dict("records"):
        for metric, lower, upper, category in NON_CADENCE_METRICS:
            real_value = float(row.get(f"{metric}_real") or 0.0)
            synthetic_value = float(row.get(f"{metric}_synthetic") or 0.0)
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
                }
            )
    return pd.DataFrame(rows)


def build_gap_summary(comparison: pd.DataFrame) -> pd.DataFrame:
    frame = comparison.copy()
    frame["gap_bool"] = frame["calibration_gap"].astype(bool)
    return (
        frame.groupby(["category", "metric"], sort=True)
        .agg(
            symbol_metrics=("symbol", "count"),
            gap_count=("gap_bool", "sum"),
            gap_fraction=("gap_bool", "mean"),
            median_synthetic_to_real_ratio=("synthetic_to_real_ratio", "median"),
            min_synthetic_to_real_ratio=("synthetic_to_real_ratio", "min"),
            max_synthetic_to_real_ratio=("synthetic_to_real_ratio", "max"),
        )
        .reset_index()
    )


def build_override_contract(comparison: pd.DataFrame) -> pd.DataFrame:
    failed = comparison[comparison["calibration_gap"].astype(bool)].copy()
    rows: list[dict[str, Any]] = []
    for row in failed.sort_values(["metric", "symbol"], kind="mergesort").to_dict("records"):
        ratio = float(row["synthetic_to_real_ratio"])
        if row["metric"] in {"median_l1_depth", "median_l5_depth"}:
            action = "symbol_depth_scale_override"
            multiplier = 1.0 / ratio if ratio > 0 else np.nan
        elif row["metric"] == "median_abs_l1_imbalance":
            action = "symbol_l1_imbalance_floor_or_skew_override"
            multiplier = 1.0 / ratio if ratio > 0 else 4.0
        else:
            action = f"review_{row['metric']}"
            multiplier = np.nan
        rows.append(
            {
                "symbol": row["symbol"],
                "metric": row["metric"],
                "synthetic_to_real_ratio": ratio,
                "proposed_action": action,
                "proposed_multiplier_or_floor_hint": multiplier,
            }
        )
    return pd.DataFrame(rows)


def summarize(comparison: pd.DataFrame, gaps: pd.DataFrame, inventory: pd.DataFrame) -> pd.DataFrame:
    gap_rows = int(comparison["calibration_gap"].astype(bool).sum()) if not comparison.empty else 0
    anchor_rows = int(len(comparison))
    gap_fraction = float(gap_rows / anchor_rows) if anchor_rows else 1.0
    severe_metric_count = int((gaps["gap_fraction"].astype(float) > 0.50).sum()) if not gaps.empty else 0
    pass_gate = bool(anchor_rows >= 192 and gap_fraction <= 0.25 and severe_metric_count == 0)
    return pd.DataFrame(
        [
            ("phase160_symbols_compared", int(comparison["symbol"].nunique()) if not comparison.empty else 0, "Symbols compared"),
            ("phase160_anchor_metric_rows", anchor_rows, "Non-cadence symbol/metric rows compared"),
            ("phase160_calibration_gap_rows", gap_rows, "Non-cadence rows outside gates"),
            ("phase160_calibration_gap_fraction", gap_fraction, "Fraction of non-cadence rows outside gates"),
            ("phase160_severe_metric_gap_count", severe_metric_count, "Non-cadence metrics with gap_fraction > 50%"),
            ("phase160_phase159_dense_rows_profiled", int(inventory["dense_rows"].sum()) if not inventory.empty else 0, "Phase159 dense rows profiled"),
            ("phase160_generated_noncadence_realism_pass", int(pass_gate), "1 means generated Phase159 non-cadence profile passes Phase106-style gate"),
            ("phase160_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase160_next_best_action", "combine_phase159_cadence_and_phase160_noncadence_acceptance_then_plan_broader_materialization", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase160 Phase159 Non-cadence Realism Audit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase160 profiles spread, visible depth, L1 imbalance, and one-tick volatility from the actual Phase159 generated dense shard.",
        "It replaces stale non-cadence assumptions with generated-shard evidence. It does not run strategy replay, fills, P&L, or Azure reads.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase160_phase159_noncadence_realism_audit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase160(phase159_dir: Path, phase106_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    inventory = pd.read_csv(phase159_dir / "phase159_dense_smoke_inventory.csv")
    phase106_comparison = pd.read_csv(phase106_dir / "real_vs_calibrated_synthetic_comparison.csv")
    synthetic = synthetic_noncadence_profile(inventory)
    real = real_noncadence_profile_from_phase106(phase106_comparison)
    comparison = build_comparison(real, synthetic)
    gaps = build_gap_summary(comparison)
    overrides = build_override_contract(comparison)
    acceptance = summarize(comparison, gaps, inventory)

    synthetic.to_csv(output_dir / "phase160_phase159_generated_noncadence_profile.csv", index=False)
    real.to_csv(output_dir / "phase160_real_noncadence_anchor_profile.csv", index=False)
    comparison.to_csv(output_dir / "phase160_generated_noncadence_comparison.csv", index=False)
    gaps.to_csv(output_dir / "phase160_generated_noncadence_gap_summary.csv", index=False)
    overrides.to_csv(output_dir / "phase160_depth_imbalance_override_contract.csv", index=False)
    acceptance.to_csv(output_dir / "phase160_phase159_noncadence_realism_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Generated Non-cadence Gap Summary": gaps,
            "Depth Imbalance Override Contract": overrides,
            "Generated Non-cadence Comparison": comparison,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase160_phase159_noncadence_realism_audit",
        **reproducibility_fields(
            artifact_id="phase160",
            generated_utc=generated_utc,
            inputs={
                "phase159_inventory": str(phase159_dir / "phase159_dense_smoke_inventory.csv"),
                "phase106_comparison": str(phase106_dir / "real_vs_calibrated_synthetic_comparison.csv"),
            },
            parameters={
                "profiled_metrics": "spread_depth_imbalance_one_tick_volatility",
                "strategy_replay_policy": "closed",
            },
            outputs={
                "synthetic_profile": str(output_dir / "phase160_phase159_generated_noncadence_profile.csv"),
                "comparison": str(output_dir / "phase160_generated_noncadence_comparison.csv"),
                "gap_summary": str(output_dir / "phase160_generated_noncadence_gap_summary.csv"),
                "override_contract": str(output_dir / "phase160_depth_imbalance_override_contract.csv"),
                "acceptance_summary": str(output_dir / "phase160_phase159_noncadence_realism_acceptance_summary.csv"),
                "report": str(output_dir / "phase160_phase159_noncadence_realism_audit_report.md"),
                "manifest": str(output_dir / "phase160_phase159_noncadence_realism_audit_manifest.json"),
            },
            random_seed="none_deterministic_phase160_audit",
            scenario_ids="phase160_phase159_generated_dense_non_cadence",
            cost_model_version="not_applicable",
            latency_model_version="not_applicable_no_execution",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase160_phase159_noncadence_realism_audit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit non-cadence realism from generated Phase159 dense shard.")
    parser.add_argument("--phase159-dir", type=Path, default=DEFAULT_PHASE159_DIR)
    parser.add_argument("--phase106-dir", type=Path, default=DEFAULT_PHASE106_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase160(args.phase159_dir, args.phase106_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
