from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.generator_calibration_profiles import DEFAULT_PROFILE_ID, get_calibration_profile
from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase49_dense_tick_rate_expansion import run_dense_expansion
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_COMPACT_ROOT = Path("raw_synthetic_l2_full_year_compact_monthly")
DEFAULT_PHASE100_DIR = Path("outputs/phase100")
DEFAULT_OUTPUT_DIR = Path("outputs/phase101")
DEFAULT_SYMBOLS = ["HDFCBANK"]
DEFAULT_PROFILES = [DEFAULT_PROFILE_ID, "P98_TIMING_VOL_MODERATE", "P98_FULL_BOOK_REBALANCE_BASE"]


def metric_value(path: Path, metric: str, default: Any = None) -> Any:
    if not path.exists():
        return default
    frame = pd.read_csv(path)
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    value = rows.iloc[0]
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def dense_quality_profile(inventory: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for item in inventory.to_dict("records"):
        path = Path(str(item["file_path"]))
        # Use ParquetFile rather than read_table(path) because these files live
        # under Hive-style partition directories such as symbol=HDFCBANK.  The
        # dataset reader tries to merge partition-derived columns with the file
        # columns, which can create large_string vs dictionary type conflicts.
        frame = pq.ParquetFile(path).read().to_pandas()
        frame = frame.sort_values(["trade_date", "symbol", "feed_profile", "local_sequence_id"], kind="mergesort")
        gaps = frame.groupby(["trade_date", "symbol", "feed_profile"], sort=False)["callback_received_utc_ms"].diff().dropna()
        mid = (frame["buy_1_price"].astype(float) + frame["sell_1_price"].astype(float)) / 2.0
        spread_bps = (frame["sell_1_price"].astype(float) - frame["buy_1_price"].astype(float)) / mid.replace(0, np.nan) * 10000.0
        l1_depth = frame["buy_1_quantity"].astype(float) + frame["sell_1_quantity"].astype(float)
        l5_depth = sum(frame[f"buy_{level}_quantity"].astype(float) + frame[f"sell_{level}_quantity"].astype(float) for level in range(1, 6))
        l1_imb = ((frame["buy_1_quantity"].astype(float) - frame["sell_1_quantity"].astype(float)) / l1_depth.replace(0, np.nan)).abs()
        tick_ret = frame.groupby(["trade_date", "symbol", "feed_profile"], sort=False)["last_price"].pct_change().dropna()
        rows.append(
            {
                "profile_id": item["profile_id"],
                "trade_month": item["trade_month"],
                "symbol": item["symbol"],
                "source_rows": int(item["source_rows"]),
                "dense_rows": int(item["dense_rows"]),
                "bytes": int(item["bytes"]),
                "median_gap_ms": float(gaps.median()) if not gaps.empty else np.nan,
                "p90_gap_ms": float(gaps.quantile(0.90)) if not gaps.empty else np.nan,
                "p95_gap_ms": float(gaps.quantile(0.95)) if not gaps.empty else np.nan,
                "one_tick_return_std": float(tick_ret.std(ddof=1)) if len(tick_ret) > 1 else 0.0,
                "median_spread_bps": float(spread_bps.median()),
                "p90_spread_bps": float(spread_bps.quantile(0.90)),
                "median_l1_depth": float(l1_depth.median()),
                "median_l5_depth": float(l5_depth.median()),
                "median_abs_l1_imbalance": float(l1_imb.median()),
            }
        )
    return pd.DataFrame(rows)


def compare_profiles(quality: pd.DataFrame) -> pd.DataFrame:
    legacy = quality[quality["profile_id"].eq(DEFAULT_PROFILE_ID)].copy()
    rows: list[dict[str, Any]] = []
    for profile_id, group in quality[~quality["profile_id"].eq(DEFAULT_PROFILE_ID)].groupby("profile_id", sort=True):
        merged = group.merge(
            legacy,
            on=["trade_month", "symbol"],
            suffixes=("_profile", "_legacy"),
            how="inner",
        )
        rows.append(
            {
                "profile_id": profile_id,
                "month_rows": int(len(merged)),
                "median_p90_gap_ratio": float((merged["p90_gap_ms_profile"] / merged["p90_gap_ms_legacy"]).median()),
                "median_one_tick_vol_ratio": float((merged["one_tick_return_std_profile"] / merged["one_tick_return_std_legacy"].replace(0, np.nan)).median()),
                "median_l1_imbalance_ratio": float((merged["median_abs_l1_imbalance_profile"] / merged["median_abs_l1_imbalance_legacy"].replace(0, np.nan)).median()),
                "median_l5_depth_ratio": float((merged["median_l5_depth_profile"] / merged["median_l5_depth_legacy"].replace(0, np.nan)).median()),
                "median_spread_ratio": float((merged["median_spread_bps_profile"] / merged["median_spread_bps_legacy"].replace(0, np.nan)).median()),
                "tail_gap_improved_month_fraction": float((merged["p90_gap_ms_profile"] > merged["p90_gap_ms_legacy"]).mean()),
                "volatility_not_increased_month_fraction": float((merged["one_tick_return_std_profile"] <= merged["one_tick_return_std_legacy"]).mean()),
                "spread_preserved_month_fraction": float(((merged["median_spread_bps_profile"] / merged["median_spread_bps_legacy"].replace(0, np.nan) - 1.0).abs() <= 0.05).mean()),
            }
        )
    return pd.DataFrame(rows)


def run_profile_shards(
    compact_root: Path,
    output_dir: Path,
    output_root_base: Path,
    symbols: list[str],
    profiles: list[str],
    multiplier: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    all_inventory: list[pd.DataFrame] = []
    elapsed_rows: list[dict[str, Any]] = []
    for profile_id in profiles:
        profile = get_calibration_profile(profile_id)
        output_root = output_root_base / f"profile={profile_id}"
        inventory, elapsed = run_dense_expansion(
            compact_root,
            output_root,
            symbols=symbols,
            multiplier=multiplier,
            calibration_profile=profile,
        )
        inventory["profile_id"] = profile_id
        inventory["output_root"] = str(output_root)
        all_inventory.append(inventory)
        elapsed_rows.append(
            {
                "profile_id": profile_id,
                "elapsed_seconds": float(elapsed),
                "source_rows": int(inventory["source_rows"].sum()) if not inventory.empty else 0,
                "dense_rows": int(inventory["dense_rows"].sum()) if not inventory.empty else 0,
                "bytes": int(inventory["bytes"].sum()) if not inventory.empty else 0,
            }
        )
    return pd.concat(all_inventory, ignore_index=True), pd.DataFrame(elapsed_rows)


def build_checks(profile_comparison: pd.DataFrame, phase100_dir: Path) -> pd.DataFrame:
    phase100_pass = metric_value(phase100_dir / "calibrated_generator_quality_acceptance_summary.csv", "phase100_quality_smoke_pass", 0)
    phase100_replay = metric_value(phase100_dir / "calibrated_generator_quality_acceptance_summary.csv", "phase100_strategy_replay_allowed", 1)
    timing = profile_comparison[profile_comparison["profile_id"].eq("P98_TIMING_VOL_MODERATE")]
    book = profile_comparison[profile_comparison["profile_id"].eq("P98_FULL_BOOK_REBALANCE_BASE")]
    return pd.DataFrame(
        [
            {
                "check_id": "P101_PHASE100_PASS",
                "passed": bool(int(float(phase100_pass)) == 1),
                "detail": f"phase100_quality_smoke_pass={phase100_pass}",
            },
            {
                "check_id": "P101_REPLAY_LOCK_PRESERVED",
                "passed": bool(int(float(phase100_replay)) == 0),
                "detail": f"phase100_strategy_replay_allowed={phase100_replay}",
            },
            {
                "check_id": "P101_TIMING_PROFILE_IMPROVES_ALL_MONTHS",
                "passed": bool(not timing.empty and float(timing.iloc[0]["tail_gap_improved_month_fraction"]) >= 1.0),
                "detail": "P98_TIMING_VOL_MODERATE should improve p90 gap for every HDFCBANK month in shard audit.",
            },
            {
                "check_id": "P101_BOOK_PROFILE_REDUCES_OR_PRESERVES_VOL_ALL_MONTHS",
                "passed": bool(not book.empty and float(book.iloc[0]["volatility_not_increased_month_fraction"]) >= 1.0),
                "detail": "P98_FULL_BOOK_REBALANCE_BASE should not increase one-tick volatility in any audited month.",
            },
            {
                "check_id": "P101_SPREAD_PRESERVED",
                "passed": bool(not profile_comparison.empty and profile_comparison["spread_preserved_month_fraction"].ge(1.0).all()),
                "detail": "All calibrated profiles must preserve median spread within 5% for every audited month.",
            },
        ]
    )


def summarize(inventory: pd.DataFrame, quality: pd.DataFrame, checks: pd.DataFrame, multiplier: int) -> pd.DataFrame:
    passed = int(checks["passed"].astype(bool).sum())
    return pd.DataFrame(
        [
            ("phase101_profiles_audited", int(inventory["profile_id"].nunique()), "Calibration profiles materialized in shard audit"),
            ("phase101_symbols_audited", int(inventory["symbol"].nunique()), "Symbols audited"),
            ("phase101_months_audited", int(inventory["trade_month"].nunique()), "Months audited"),
            ("phase101_dense_multiplier", int(multiplier), "Dense multiplier used for bounded quality audit"),
            ("phase101_dense_rows_materialized", int(inventory["dense_rows"].sum()), "Dense rows materialized locally for quality audit"),
            ("phase101_quality_rows", int(len(quality)), "Profile/month quality rows"),
            ("phase101_quality_check_rows", int(len(checks)), "Quality checks executed"),
            ("phase101_quality_checks_passed", passed, "Quality checks passed"),
            ("phase101_quality_audit_pass", int(passed == len(checks)), "1 means small calibrated Phase49 quality audit passed"),
            ("phase101_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase101_recommend_next_action", "rerun_phase94_on_multiday_real_panel_when_available", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase101 Calibrated Phase49 Shard Quality Audit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase101 materializes small calibrated Phase49 dense shards for generator-quality auditing only.",
        "It compares calibrated profiles against the legacy profile on timing, volatility, spread and book-shape metrics. It does not run strategy replay.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase101_calibrated_phase49_shard_quality_audit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase101(
    compact_root: Path,
    phase100_dir: Path,
    output_dir: Path,
    output_root_base: Path,
    base_dir: Path,
    symbols: list[str],
    profiles: list[str],
    multiplier: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    inventory, elapsed = run_profile_shards(compact_root, output_dir, output_root_base, symbols, profiles, multiplier)
    quality = dense_quality_profile(inventory)
    comparison = compare_profiles(quality)
    checks = build_checks(comparison, phase100_dir)
    acceptance = summarize(inventory, quality, checks, multiplier)

    inventory.to_csv(output_dir / "calibrated_phase49_shard_inventory.csv", index=False)
    elapsed.to_csv(output_dir / "calibrated_phase49_profile_elapsed.csv", index=False)
    quality.to_csv(output_dir / "calibrated_phase49_quality_by_profile_month.csv", index=False)
    comparison.to_csv(output_dir / "calibrated_phase49_profile_comparison.csv", index=False)
    checks.to_csv(output_dir / "calibrated_phase49_quality_checks.csv", index=False)
    acceptance.to_csv(output_dir / "calibrated_phase49_quality_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Quality Checks": checks,
            "Profile Comparison": comparison,
            "Quality by Profile Month": quality,
            "Shard Inventory": inventory,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {"generated_utc": generated_utc, "scope": "phase101_calibrated_phase49_shard_quality_audit"}
    manifest.update(
        reproducibility_fields(
            artifact_id="phase101",
            generated_utc=generated_utc,
            inputs={
                "compact_root": str(compact_root),
                "phase100_acceptance": str(phase100_dir / "calibrated_generator_quality_acceptance_summary.csv"),
            },
            parameters={
                "profiles": profiles,
                "symbols": symbols,
                "dense_multiplier": multiplier,
                "strategy_replay_policy": "closed",
                "local_output_root_base": str(output_root_base),
            },
            outputs={
                "inventory": str(output_dir / "calibrated_phase49_shard_inventory.csv"),
                "elapsed": str(output_dir / "calibrated_phase49_profile_elapsed.csv"),
                "quality": str(output_dir / "calibrated_phase49_quality_by_profile_month.csv"),
                "comparison": str(output_dir / "calibrated_phase49_profile_comparison.csv"),
                "checks": str(output_dir / "calibrated_phase49_quality_checks.csv"),
                "acceptance_summary": str(output_dir / "calibrated_phase49_quality_acceptance_summary.csv"),
                "report": str(output_dir / "phase101_calibrated_phase49_shard_quality_audit_report.md"),
                "manifest": str(output_dir / "phase101_calibrated_phase49_shard_quality_audit_manifest.json"),
            },
            random_seed="none_deterministic_phase49_profile_audit",
            scenario_ids="phase101_hdfcbank_calibrated_phase49_quality_audit",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase98_phase99_phase100_generator_calibration_profiles",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase101_calibrated_phase49_shard_quality_audit_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run calibrated Phase49 shard quality audit without strategy replay.")
    parser.add_argument("--compact-root", type=Path, default=DEFAULT_COMPACT_ROOT)
    parser.add_argument("--phase100-dir", type=Path, default=DEFAULT_PHASE100_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--output-root-base", type=Path, default=Path("raw_synthetic_l2_phase101_calibrated_quality"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--symbols", nargs="+", default=DEFAULT_SYMBOLS)
    parser.add_argument("--profiles", nargs="+", default=DEFAULT_PROFILES)
    parser.add_argument("--multiplier", type=int, default=8)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase101(
        args.compact_root,
        args.phase100_dir,
        args.output_dir,
        args.output_root_base,
        args.base_dir,
        args.symbols,
        args.profiles,
        args.multiplier,
    )


if __name__ == "__main__":
    main()
