from __future__ import annotations

import argparse
import json
import math
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.generator_calibration_profiles import GeneratorCalibrationProfile, get_calibration_profile
from synthetic_l2.reproducibility import reproducibility_fields


TARGET_DENSE_RAW_GB = 83.240
SOURCE_ROWS = 3_012_294
DEFAULT_DENSE_MULTIPLIER = 64
DEFAULT_SYMBOLS = ["HDFCBANK"]


def compact_files(compact_root: Path) -> list[Path]:
    files = sorted(compact_root.glob("trade_month=*/part-00000.parquet"))
    if not files:
        raise FileNotFoundError(f"No compact monthly parquet files under {compact_root}")
    return files


def read_month(path: Path, symbols: list[str]) -> pd.DataFrame:
    table = pq.ParquetFile(path).read()
    frame = table.to_pandas()
    if symbols:
        frame = frame[frame["symbol"].astype(str).isin(symbols)].copy()
    return frame.sort_values(["trade_date", "exchange", "symbol", "feed_profile", "annual_event_id"], kind="mergesort").reset_index(drop=True)


def densify_frame(frame: pd.DataFrame, multiplier: int, calibration_profile: GeneratorCalibrationProfile | None = None) -> pd.DataFrame:
    profile = calibration_profile or get_calibration_profile(None)
    if frame.empty:
        return frame.copy()
    repeated = frame.loc[frame.index.repeat(multiplier)].copy().reset_index(drop=True)
    subtick = np.tile(np.arange(multiplier, dtype=np.int16), len(frame))
    repeated["dense_subtick_id"] = subtick
    repeated["dense_multiplier"] = multiplier
    repeated["source_annual_event_id"] = repeated["annual_event_id"].astype("int64")
    repeated["annual_event_id"] = repeated["annual_event_id"].astype("int64") * multiplier + repeated["dense_subtick_id"].astype("int64")
    repeated["local_sequence_id"] = np.arange(1, len(repeated) + 1, dtype=np.int64)
    repeated["callback_batch_id"] = repeated["local_sequence_id"].floordiv(32).astype("int64")
    source_timing_rank = np.repeat(np.arange(len(frame), dtype=np.int64), multiplier)
    timing_offset = (
        source_timing_rank.astype(float) * float(multiplier) * (float(profile.event_timing_tail_gap_multiplier) - 1.0)
        + repeated["dense_subtick_id"].astype(float) * float(profile.event_timing_tail_gap_multiplier)
    ).round().astype("int64")
    if float(profile.event_timing_burst_throttle_fraction) > 0:
        throttle_step = max(1, int(round(1.0 / float(profile.event_timing_burst_throttle_fraction))))
        timing_offset = timing_offset + (repeated["dense_subtick_id"].astype("int64") // throttle_step)
    tail_overrides = profile.symbol_tail_gap_multiplier_overrides or {}
    if tail_overrides:
        symbol_values = frame["symbol"].astype(str).to_numpy()
        source_extra = np.zeros(len(frame), dtype=np.int64)
        for symbol, raw_multiplier in tail_overrides.items():
            mask = symbol_values == str(symbol)
            positions = np.flatnonzero(mask)
            if len(positions) == 0:
                continue
            target_extra = max(0, int(round(692.0 * (float(raw_multiplier) - 1.0))))
            if target_extra <= 0:
                continue
            source_extra[positions[1:]] = target_extra
        cumulative_extra = np.cumsum(source_extra)
        timing_offset = timing_offset + np.repeat(cumulative_extra, multiplier)
    repeated["callback_received_utc_ms"] = repeated["callback_received_utc_ms"].astype("int64") + timing_offset
    repeated["callback_received_monotonic_ns"] = repeated["callback_received_utc_ms"].astype("int64") * 1_000_000
    repeated["exchange_timestamp_ms"] = repeated["exchange_timestamp_ms"].astype("int64") + timing_offset
    repeated["last_trade_time_ms"] = repeated["exchange_timestamp_ms"]

    if float(profile.source_mid_return_scale) != 1.0:
        original_mid = (repeated["buy_1_price"].astype(float) + repeated["sell_1_price"].astype(float)) / 2.0
        anchor_mid = original_mid.groupby([repeated["trade_date"], repeated["symbol"]], sort=False).transform("first")
        scaled_mid = anchor_mid + (original_mid - anchor_mid) * float(profile.source_mid_return_scale)
        price_delta = scaled_mid - original_mid
        price_columns = ["last_price"]
        for level in range(1, 6):
            price_columns.extend([f"buy_{level}_price", f"sell_{level}_price"])
        for column in price_columns:
            if column in repeated.columns:
                repeated[column] = (repeated[column].astype(float) + price_delta).round(4)

    phase = (repeated["dense_subtick_id"].astype(float) / max(multiplier - 1, 1)) - 0.5
    micro_step = (
        (repeated["sell_1_price"].astype(float) - repeated["buy_1_price"].astype(float)).abs().clip(lower=0.01)
        * float(profile.price_micro_step_spread_fraction)
        * float(profile.price_jump_size_scale)
    )
    if bool(profile.price_anchor_source_events):
        # Calibrated profiles should preserve the source event price at the
        # first dense subtick and damp only generated in-between microstructure
        # noise.  This keeps real source moves intact while making volatility
        # calibration measurable against the legacy synthetic oscillation.
        anchored_phase = np.sin(np.pi * repeated["dense_subtick_id"].astype(float) / max(multiplier - 1, 1))
        direction = np.where((repeated["dense_subtick_id"].astype(int) % 2) == 0, 1.0, -1.0)
        price_delta = direction * anchored_phase * micro_step
    else:
        direction = np.where((repeated["dense_subtick_id"].astype(int) % 2) == 0, 1.0, -1.0)
        price_delta = direction * phase.abs() * micro_step
    repeated["last_price"] = (repeated["last_price"].astype(float) + price_delta).round(4)
    depth_overrides = profile.symbol_depth_scale_overrides or {}
    if depth_overrides:
        symbol_series = repeated["symbol"].astype(str)
        for symbol, scale in depth_overrides.items():
            mask = symbol_series.eq(str(symbol))
            if not bool(mask.any()):
                continue
            scale_value = float(scale)
            quantity_columns = ["total_buy_quantity", "total_sell_quantity"]
            for level in range(1, 6):
                quantity_columns.extend([f"buy_{level}_quantity", f"sell_{level}_quantity"])
            for column in quantity_columns:
                if column in repeated.columns:
                    repeated.loc[mask, column] = np.maximum(
                        1,
                        (repeated.loc[mask, column].astype(float) * scale_value).round(),
                    ).astype("int64")
    imbalance_overrides = profile.symbol_l1_imbalance_scale_overrides or {}
    if imbalance_overrides and {"buy_1_quantity", "sell_1_quantity"}.issubset(repeated.columns):
        symbol_series = repeated["symbol"].astype(str)
        for symbol, scale in imbalance_overrides.items():
            mask = symbol_series.eq(str(symbol))
            if not bool(mask.any()):
                continue
            bid = repeated.loc[mask, "buy_1_quantity"].astype(float)
            ask = repeated.loc[mask, "sell_1_quantity"].astype(float)
            total = (bid + ask).clip(lower=2.0)
            current = (bid - ask) / total
            deterministic_sign = np.where((repeated.loc[mask, "annual_event_id"].astype("int64") % 2) == 0, 1.0, -1.0)
            seeded = np.where(current.abs() < 1e-9, 0.35 * deterministic_sign, current)
            target = pd.Series(seeded, index=current.index).mul(float(scale)).clip(-0.98, 0.98)
            repeated.loc[mask, "buy_1_quantity"] = np.maximum(1, (total * (1.0 + target) / 2.0).round()).astype("int64")
            repeated.loc[mask, "sell_1_quantity"] = np.maximum(1, (total * (1.0 - target) / 2.0).round()).astype("int64")
    repeated["last_traded_quantity"] = np.maximum(1, (repeated["last_traded_quantity"].astype(float) / math.sqrt(multiplier)).round()).astype("int64")
    repeated["volume_traded"] = repeated.groupby(["trade_date", "symbol"], sort=False)["last_traded_quantity"].cumsum().astype("int64")
    return repeated


def write_dense_shard(dense: pd.DataFrame, output_root: Path, trade_month: str, symbol: str) -> Path:
    target_dir = output_root / f"trade_month={trade_month}" / f"symbol={symbol}"
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / "part-00000.parquet"
    pq.write_table(pa.Table.from_pandas(dense, preserve_index=False), target_file, compression="zstd")
    return target_file


def run_dense_expansion(compact_root: Path, output_root: Path, symbols: list[str], multiplier: int, calibration_profile: GeneratorCalibrationProfile | None = None) -> tuple[pd.DataFrame, float]:
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    rows = []
    for path in compact_files(compact_root):
        trade_month = path.parent.name.split("=", 1)[1]
        month = read_month(path, symbols)
        for symbol, symbol_frame in month.groupby("symbol", sort=True):
            dense = densify_frame(symbol_frame, multiplier, calibration_profile=calibration_profile)
            target_file = write_dense_shard(dense, output_root, trade_month, str(symbol))
            rows.append(
                {
                    "trade_month": trade_month,
                    "symbol": str(symbol),
                    "source_rows": int(len(symbol_frame)),
                    "dense_rows": int(len(dense)),
                    "multiplier": int(multiplier),
                    "file_path": str(target_file),
                    "bytes": int(target_file.stat().st_size),
                }
            )
    elapsed = time.perf_counter() - started
    return pd.DataFrame(rows), elapsed


def build_summary(inventory: pd.DataFrame, elapsed_seconds: float, output_root: Path, multiplier: int, symbols: list[str]) -> pd.DataFrame:
    source_rows = int(inventory["source_rows"].sum()) if len(inventory) else 0
    dense_rows = int(inventory["dense_rows"].sum()) if len(inventory) else 0
    dense_bytes = int(inventory["bytes"].sum()) if len(inventory) else 0
    bytes_per_row = dense_bytes / dense_rows if dense_rows else 0.0
    target_bytes = TARGET_DENSE_RAW_GB * (1024**3)
    rows_for_target = target_bytes / bytes_per_row if bytes_per_row else 0.0
    required_full_universe_multiplier = rows_for_target / SOURCE_ROWS if SOURCE_ROWS else 0.0
    rows_per_second = dense_rows / elapsed_seconds if elapsed_seconds > 0 else 0.0
    estimated_seconds_for_target = rows_for_target / rows_per_second if rows_per_second > 0 else 0.0
    disk = shutil.disk_usage(Path(".").resolve())
    rows = [
        ("phase49_dense_shard_symbols", ";".join(symbols), "Symbols included in dense calibration shard"),
        ("phase49_dense_multiplier", multiplier, "Dense subticks generated per source raw event"),
        ("phase49_source_rows_densified", source_rows, "Source compact-raw rows densified"),
        ("phase49_dense_rows_materialized", dense_rows, "Dense raw rows materialized"),
        ("phase49_dense_partition_files", int(len(inventory)), "Dense shard parquet files written"),
        ("phase49_dense_bytes", dense_bytes, "Compressed dense shard bytes"),
        ("phase49_dense_bytes_per_row", bytes_per_row, "Measured compressed dense bytes per row"),
        ("phase49_elapsed_seconds", elapsed_seconds, "Dense shard materialization elapsed seconds"),
        ("phase49_rows_per_second", rows_per_second, "Dense materialization throughput"),
        ("phase49_target_dense_raw_gb", TARGET_DENSE_RAW_GB, "Dense raw target size"),
        ("phase49_estimated_rows_for_target_dense_lake", rows_for_target, "Rows implied by target GB at measured dense compression"),
        ("phase49_estimated_full_universe_multiplier_for_target", required_full_universe_multiplier, "Full-universe source-row multiplier implied by target dense size"),
        ("phase49_estimated_hours_for_target_at_measured_rate", estimated_seconds_for_target / 3600.0, "Rough runtime estimate for target rows at measured shard throughput"),
        ("phase49_available_disk_gb", disk.free / (1024**3), "Free disk after dense shard"),
        ("phase49_dense_output_root", str(output_root), "Local dense shard root; ignored by Git"),
        ("phase49_full_80gb_dense_lake_materialized", 0, "80GB-class dense full-universe lake not yet materialized"),
        ("phase49_synthetic_full_year_acceptance_ready", 0, "Dense generation calibration is storage/input evidence, not strategy acceptance"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase 49 Dense Tick-Rate Expansion Calibration",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This phase turns up the synthetic tick-rate faucet for a controlled dense raw-L2 shard, measures compression and throughput, and estimates the multiplier required for the 80GB-class dense lake.",
        "It is a dense-generation calibration milestone, not strategy acceptance evidence.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase49_dense_tick_rate_expansion_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase49(compact_root: Path, output_root: Path, output_dir: Path, base_dir: Path, symbols: list[str], multiplier: int, calibration_profile_id: str | None) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    calibration_profile = get_calibration_profile(calibration_profile_id)
    inventory, elapsed_seconds = run_dense_expansion(compact_root, output_root, symbols, multiplier, calibration_profile=calibration_profile)
    summary = build_summary(inventory, elapsed_seconds, output_root, multiplier, symbols)
    inventory.to_csv(output_dir / "dense_tick_shard_inventory.csv", index=False)
    summary.to_csv(output_dir / "dense_tick_expansion_summary.csv", index=False)
    write_report(output_dir, {"Dense Expansion Summary": summary, "Dense Shard Inventory": inventory})
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase49_dense_tick_rate_expansion_calibration_not_acceptance",
        "symbols": symbols,
        "dense_multiplier": multiplier,
        "dense_rows": int(inventory["dense_rows"].sum()) if len(inventory) else 0,
        "dense_bytes": int(inventory["bytes"].sum()) if len(inventory) else 0,
        "synthetic_full_year_acceptance_ready": 0,
        "generator_calibration_profile": calibration_profile.to_manifest(),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase49",
            generated_utc=generated_utc,
            inputs={"compact_monthly_raw_lake": str(compact_root)},
            parameters={
                "symbols": symbols,
                "dense_multiplier": multiplier,
                "target_dense_raw_gb": TARGET_DENSE_RAW_GB,
                "source_rows": SOURCE_ROWS,
                "acceptance_boundary": "dense_tick_generation_calibration_not_acceptance",
                "generator_calibration_profile_id": calibration_profile.profile_id,
            },
            outputs={
                "dense_output_root": str(output_root),
                "inventory": str(output_dir / "dense_tick_shard_inventory.csv"),
                "summary": str(output_dir / "dense_tick_expansion_summary.csv"),
                "report": str(output_dir / "phase49_dense_tick_rate_expansion_report.md"),
                "manifest": str(output_dir / "phase49_dense_tick_rate_expansion_manifest.json"),
            },
            random_seed="none_deterministic_dense_subtick_expansion",
            scenario_ids="phase48_compact_monthly_raw_lake_dense_hdfcbank_calibration",
            cost_model_version="not_applicable_dense_storage_generation_no_execution_costs",
            latency_model_version="phase45_raw_callback_sequence_plus_dense_subticks",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase49_dense_tick_rate_expansion_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run dense tick-rate expansion calibration shard.")
    parser.add_argument("--compact-root", type=Path, default=Path("raw_synthetic_l2_full_year_compact_monthly"))
    parser.add_argument("--output-root", type=Path, default=Path("raw_synthetic_l2_dense_phase49_hdfcbank_x64"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase49"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--symbols", nargs="+", default=DEFAULT_SYMBOLS)
    parser.add_argument("--multiplier", type=int, default=DEFAULT_DENSE_MULTIPLIER)
    parser.add_argument("--calibration-profile-id", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase49(args.compact_root, args.output_root, args.output_dir, args.base_dir, args.symbols, args.multiplier, args.calibration_profile_id)


if __name__ == "__main__":
    main()
