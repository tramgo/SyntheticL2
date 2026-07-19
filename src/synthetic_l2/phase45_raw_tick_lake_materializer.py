from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.generator_calibration_profiles import GeneratorCalibrationProfile, get_calibration_profile
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_TARGET_FULL_RAW_GB = 83.240
DEFAULT_SAMPLE_MAX_EVENTS = 50_000
RAW_ROOT = Path("raw_synthetic_l2_phase45_sample")


def load_events(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    columns = [
        "annual_event_id",
        "feed_profile",
        "synthetic_year_day",
        "synthetic_trade_date",
        "symbol",
        "receive_sequence",
        "collector_received_utc_ms",
        "source_sequence",
        "regime_code",
        "mid_price",
        "tick_size",
        "spread_ticks",
        "spread",
        "event_intensity_proxy",
        "is_market_shock_day",
        "is_symbol_shock",
        "is_duplicate",
        "is_disconnect_gap",
        "is_out_of_order_injected",
        "l1_imbalance",
        "l5_imbalance",
        "microprice_l1",
    ]
    return pq.read_table(path, columns=columns).to_pandas()


def select_sample(events: pd.DataFrame, sample_days: int, sample_symbols: int, sample_feed_profiles: int, sample_max_events: int) -> pd.DataFrame:
    days = sorted(events["synthetic_year_day"].dropna().unique().tolist())[:sample_days]
    symbols = sorted(events["symbol"].dropna().unique().tolist())[:sample_symbols]
    feed_profiles = sorted(events["feed_profile"].dropna().unique().tolist())[:sample_feed_profiles]
    sample = events[
        events["synthetic_year_day"].isin(days)
        & events["symbol"].isin(symbols)
        & events["feed_profile"].isin(feed_profiles)
    ].copy()
    sample = sample.sort_values(["synthetic_year_day", "feed_profile", "symbol", "annual_event_id"], kind="mergesort")
    if sample_max_events > 0:
        sample = sample.head(sample_max_events)
    return sample.reset_index(drop=True)


def add_depth_levels(raw: pd.DataFrame, calibration_profile: GeneratorCalibrationProfile | None = None) -> pd.DataFrame:
    profile = calibration_profile or get_calibration_profile(None)
    mid = raw["mid_price"].astype(float)
    tick = raw["tick_size"].astype(float).replace(0.0, 0.05)
    spread_ticks = raw["spread_ticks"].astype(float).clip(lower=1) * float(profile.spread_preserve_current_scale)
    half_spread = spread_ticks * tick / 2.0
    l1_imb = (raw["l1_imbalance"].astype(float) * float(profile.book_l1_quantity_skew_scale)).clip(-0.98, 0.98).fillna(0.0)
    l5_imb = raw["l5_imbalance"].astype(float).clip(-0.98, 0.98).fillna(0.0)
    intensity = raw["event_intensity_proxy"].astype(float).clip(lower=0.1).fillna(1.0)
    base_qty = ((100 + intensity * 250) * float(profile.book_depth_ladder_multiplier)).round().astype("int64")
    for level in range(1, 6):
        level_weight = (1.0 + 0.35 * (level - 1)) * (float(profile.book_l1_l5_share_ratio) if level == 1 else 1.0)
        imb = l1_imb if level == 1 else (l1_imb * (6 - level) + l5_imb * (level - 1)) / 5.0
        bid_qty = (base_qty * level_weight * (1.0 + imb)).clip(lower=1).round().astype("int64")
        ask_qty = (base_qty * level_weight * (1.0 - imb)).clip(lower=1).round().astype("int64")
        raw[f"buy_{level}_price"] = (mid - half_spread - (level - 1) * tick).round(4)
        raw[f"sell_{level}_price"] = (mid + half_spread + (level - 1) * tick).round(4)
        raw[f"buy_{level}_quantity"] = bid_qty
        raw[f"sell_{level}_quantity"] = ask_qty
        raw[f"buy_{level}_orders"] = np.maximum(1, np.ceil(bid_qty / 200.0)).astype("int64")
        raw[f"sell_{level}_orders"] = np.maximum(1, np.ceil(ask_qty / 200.0)).astype("int64")
    return raw


def build_raw_ticks(events: pd.DataFrame, calibration_profile: GeneratorCalibrationProfile | None = None) -> pd.DataFrame:
    raw = events.copy()
    raw["exchange"] = "NSE"
    raw["instrument_token"] = raw["symbol"].astype("category").cat.codes.astype("int64") + 10_000_000
    raw["collector_run_id"] = "phase45_synthetic_raw_tick_lake_sample"
    raw["session_id"] = "phase45_deterministic_session_001"
    raw["callback_batch_id"] = raw.groupby(["synthetic_trade_date", "feed_profile"], sort=False).cumcount().floordiv(32).astype("int64")
    raw["local_sequence_id"] = np.arange(1, len(raw) + 1, dtype=np.int64)
    raw["callback_received_utc_ms"] = raw["collector_received_utc_ms"].astype("int64")
    raw["callback_received_monotonic_ns"] = raw["callback_received_utc_ms"].astype("int64") * 1_000_000
    raw["exchange_timestamp_ms"] = raw["callback_received_utc_ms"].astype("int64") - 25
    raw["last_price"] = raw["mid_price"].astype(float)
    raw["last_traded_quantity"] = (raw["event_intensity_proxy"].astype(float).clip(lower=0.1) * 100).round().astype("int64")
    raw["volume_traded"] = raw.groupby(["synthetic_trade_date", "symbol"], sort=False)["last_traded_quantity"].cumsum().astype("int64")
    raw["total_buy_quantity"] = (raw["last_traded_quantity"] * (1.0 + raw["l1_imbalance"].astype(float).clip(-0.8, 0.8))).clip(lower=1).round().astype("int64")
    raw["total_sell_quantity"] = (raw["last_traded_quantity"] * (1.0 - raw["l1_imbalance"].astype(float).clip(-0.8, 0.8))).clip(lower=1).round().astype("int64")
    raw["last_trade_time_ms"] = raw["exchange_timestamp_ms"]
    raw["oi"] = 0
    raw["oi_day_high"] = 0
    raw["oi_day_low"] = 0
    raw["average_traded_price"] = raw.groupby(["synthetic_trade_date", "symbol"], sort=False)["last_price"].expanding().mean().reset_index(level=[0, 1], drop=True)
    raw = add_depth_levels(raw, calibration_profile=calibration_profile)
    output_columns = [
        "collector_run_id",
        "session_id",
        "callback_batch_id",
        "local_sequence_id",
        "callback_received_utc_ms",
        "callback_received_monotonic_ns",
        "exchange_timestamp_ms",
        "last_trade_time_ms",
        "synthetic_trade_date",
        "exchange",
        "symbol",
        "instrument_token",
        "feed_profile",
        "annual_event_id",
        "receive_sequence",
        "source_sequence",
        "regime_code",
        "last_price",
        "last_traded_quantity",
        "volume_traded",
        "average_traded_price",
        "total_buy_quantity",
        "total_sell_quantity",
        "oi",
        "oi_day_high",
        "oi_day_low",
        "is_market_shock_day",
        "is_symbol_shock",
        "is_duplicate",
        "is_disconnect_gap",
        "is_out_of_order_injected",
    ]
    for level in range(1, 6):
        output_columns.extend(
            [
                f"buy_{level}_price",
                f"buy_{level}_quantity",
                f"buy_{level}_orders",
                f"sell_{level}_price",
                f"sell_{level}_quantity",
                f"sell_{level}_orders",
            ]
        )
    return raw[output_columns].rename(columns={"synthetic_trade_date": "trade_date"})


def write_partitioned_raw(raw: pd.DataFrame, raw_root: Path) -> pd.DataFrame:
    rows = []
    if raw.empty:
        return pd.DataFrame(columns=["trade_date", "exchange", "symbol", "file_path", "rows", "bytes"])
    for (trade_date, exchange, symbol), group in raw.groupby(["trade_date", "exchange", "symbol"], sort=True):
        directory = raw_root / f"trade_date={trade_date}" / f"exchange={exchange}" / f"symbol={symbol}"
        directory.mkdir(parents=True, exist_ok=True)
        file_path = directory / "part-00000.parquet"
        pq.write_table(pa.Table.from_pandas(group, preserve_index=False), file_path, compression="zstd")
        rows.append(
            {
                "trade_date": trade_date,
                "exchange": exchange,
                "symbol": symbol,
                "file_path": str(file_path),
                "rows": int(len(group)),
                "bytes": int(file_path.stat().st_size),
            }
        )
    return pd.DataFrame(rows)


def build_size_ledger(
    *,
    source_event_rows: int,
    materialized_rows: int,
    materialized_bytes: int,
    target_full_raw_gb: float,
    raw_root: Path,
    full_raw_lake_materialized: bool,
) -> pd.DataFrame:
    usage = shutil.disk_usage(Path(".").resolve())
    measured_bytes_per_row = materialized_bytes / materialized_rows if materialized_rows else 0.0
    target_bytes = target_full_raw_gb * (1024**3)
    estimated_rows_for_target = target_bytes / measured_bytes_per_row if measured_bytes_per_row else 0.0
    estimated_current_full_bytes = source_event_rows * measured_bytes_per_row
    rows = [
        ("phase45_source_compact_event_rows", source_event_rows, "Rows available in Phase 42 compact event-state source"),
        ("phase45_materialized_raw_rows", materialized_rows, "Rows materialized into raw websocket-like partitions"),
        ("phase45_materialized_raw_bytes", materialized_bytes, "Compressed parquet bytes written for the materialized raw lake"),
        ("phase45_measured_compressed_bytes_per_row", measured_bytes_per_row, "Measured raw-lake compressed bytes per row"),
        ("phase45_estimated_current_event_state_raw_gb", estimated_current_full_bytes / (1024**3), "Estimated raw-lake GB if materializing only current 3.0M event rows"),
        ("phase45_target_full_raw_lake_gb", target_full_raw_gb, "Target 80GB-class full-year raw lake size from risk-register expectation"),
        ("phase45_estimated_rows_for_target_full_raw_lake", estimated_rows_for_target, "Rows implied by target GB at measured raw-lake compression"),
        ("phase45_available_disk_gb", usage.free / (1024**3), "Free disk on current workspace drive after materialization"),
        ("phase45_raw_lake_root", str(raw_root), "Local raw-lake root; intentionally ignored by git"),
        ("phase45_full_current_event_lake_materialized", int(full_raw_lake_materialized), "Full current synthetic event universe was materialized as raw websocket-like L2 rows"),
        ("phase45_full_80gb_dense_lake_materialized", 0, "80GB-class densified raw lake was not materialized by Phase45"),
        ("phase45_synthetic_full_year_acceptance_ready", 0, "Raw materialization is storage/infrastructure evidence, not strategy acceptance"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame], raw_root: Path, target_full_raw_gb: float) -> None:
    full_command = (
        "python scripts/run_phase45_raw_tick_lake_materializer.py "
        "--mode full --confirm-full-materialization "
        f"--target-full-raw-gb {target_full_raw_gb:.3f} "
        "--raw-root raw_synthetic_l2_full_year"
    )
    lines = [
        "# Phase 45 Raw Synthetic L2 Tick-Lake Materialization",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This phase makes the raw websocket-like tick-lake layer explicit. The default run materializes a small partitioned proof sample and estimates the 80GB-class full raw lake; it does not pretend that the compact Phase 42 event-state parquet is the raw archive.",
        "",
        f"Sample raw root: `{raw_root}`",
        "",
        f"Guarded full materialization command: `{full_command}`",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase45_raw_tick_lake_materialization_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase45(
    events_path: Path,
    output_dir: Path,
    raw_root: Path,
    base_dir: Path,
    mode: str,
    confirm_full_materialization: bool,
    sample_days: int,
    sample_symbols: int,
    sample_feed_profiles: int,
    sample_max_events: int,
    target_full_raw_gb: float,
    calibration_profile_id: str | None,
) -> None:
    if mode == "full" and not confirm_full_materialization:
        raise ValueError("Full raw tick-lake materialization requires --confirm-full-materialization.")
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_root.mkdir(parents=True, exist_ok=True)
    calibration_profile = get_calibration_profile(calibration_profile_id)
    events = load_events(events_path)
    source_rows = int(len(events))
    if mode == "estimate":
        selected = events.head(0).copy()
    elif mode == "sample":
        selected = select_sample(events, sample_days, sample_symbols, sample_feed_profiles, sample_max_events)
    else:
        selected = events.copy()
    raw = build_raw_ticks(selected, calibration_profile=calibration_profile) if len(selected) else pd.DataFrame()
    inventory = write_partitioned_raw(raw, raw_root) if len(raw) else pd.DataFrame(columns=["trade_date", "exchange", "symbol", "file_path", "rows", "bytes"])
    materialized_rows = int(inventory["rows"].sum()) if len(inventory) else 0
    materialized_bytes = int(inventory["bytes"].sum()) if len(inventory) else 0
    size_ledger = build_size_ledger(
        source_event_rows=source_rows,
        materialized_rows=materialized_rows,
        materialized_bytes=materialized_bytes,
        target_full_raw_gb=target_full_raw_gb,
        raw_root=raw_root,
        full_raw_lake_materialized=mode == "full",
    )
    schema_rows = [{"column": column, "dtype": str(dtype)} for column, dtype in raw.dtypes.items()] if len(raw) else []
    schema = pd.DataFrame(schema_rows)
    inventory.to_csv(output_dir / "raw_tick_lake_partition_inventory.csv", index=False)
    schema.to_csv(output_dir / "raw_tick_lake_schema.csv", index=False)
    size_ledger.to_csv(output_dir / "raw_tick_lake_size_ledger.csv", index=False)
    write_report(
        output_dir,
        {
            "Size Ledger": size_ledger,
            "Partition Inventory": inventory,
            "Raw Schema": schema,
        },
        raw_root,
        target_full_raw_gb,
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase45_raw_synthetic_l2_tick_lake_materialization_not_acceptance",
        "mode": mode,
        "source_event_rows": source_rows,
        "materialized_rows": materialized_rows,
        "materialized_bytes": materialized_bytes,
        "target_full_raw_lake_gb": target_full_raw_gb,
        "full_raw_lake_materialized": int(mode == "full"),
        "synthetic_full_year_acceptance_ready": 0,
        "generator_calibration_profile": calibration_profile.to_manifest(),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase45",
            generated_utc=generated_utc,
            inputs={"native_full_year_l2_event_state": str(events_path)},
            parameters={
                "mode": mode,
                "sample_days": sample_days,
                "sample_symbols": sample_symbols,
                "sample_feed_profiles": sample_feed_profiles,
                "sample_max_events": sample_max_events,
                "target_full_raw_gb": target_full_raw_gb,
                "raw_partition_layout": "trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/part-*.parquet",
                "full_materialization_requires_confirmation": True,
                "generator_calibration_profile_id": calibration_profile.profile_id,
            },
            outputs={
                "raw_root": str(raw_root),
                "partition_inventory": str(output_dir / "raw_tick_lake_partition_inventory.csv"),
                "schema": str(output_dir / "raw_tick_lake_schema.csv"),
                "size_ledger": str(output_dir / "raw_tick_lake_size_ledger.csv"),
                "report": str(output_dir / "phase45_raw_tick_lake_materialization_report.md"),
                "manifest": str(output_dir / "phase45_raw_tick_lake_materialization_manifest.json"),
            },
            random_seed="none_deterministic_raw_tick_lake_materialization",
            scenario_ids="phase42_native_252_day_l2_event_state_raw_tick_lake_materialization",
            cost_model_version="not_applicable_storage_materialization_no_execution_costs",
            latency_model_version="phase36_raw_tick_enrichment_callback_sequence_schema",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase45_raw_tick_lake_materialization_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize/estimate raw synthetic L2 tick lake.")
    parser.add_argument("--events", type=Path, default=Path("outputs/phase42/native_full_year_l2_event_state.parquet"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase45"))
    parser.add_argument("--raw-root", type=Path, default=RAW_ROOT)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--mode", choices=["estimate", "sample", "full"], default="sample")
    parser.add_argument("--confirm-full-materialization", action="store_true")
    parser.add_argument("--sample-days", type=int, default=1)
    parser.add_argument("--sample-symbols", type=int, default=2)
    parser.add_argument("--sample-feed-profiles", type=int, default=1)
    parser.add_argument("--sample-max-events", type=int, default=DEFAULT_SAMPLE_MAX_EVENTS)
    parser.add_argument("--target-full-raw-gb", type=float, default=DEFAULT_TARGET_FULL_RAW_GB)
    parser.add_argument("--calibration-profile-id", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase45(
        args.events,
        args.output_dir,
        args.raw_root,
        args.base_dir,
        args.mode,
        args.confirm_full_materialization,
        args.sample_days,
        args.sample_symbols,
        args.sample_feed_profiles,
        args.sample_max_events,
        args.target_full_raw_gb,
        args.calibration_profile_id,
    )


if __name__ == "__main__":
    main()
