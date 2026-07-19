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
from synthetic_l2.phase49_dense_tick_rate_expansion import compact_files, read_month
from synthetic_l2.generator_calibration_profiles import GeneratorCalibrationProfile, get_calibration_profile
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_OUTPUT_ROOT = Path("raw_synthetic_l2_dense_full_year")
DEFAULT_OUTPUT_DIR = Path("outputs/phase51")
DEFAULT_SCHEDULE = Path("outputs/phase50/dense_target_shard_schedule.csv")
DEFAULT_COMPACT_ROOT = Path("raw_synthetic_l2_full_year_compact_monthly")
DEFAULT_CHUNK_SOURCE_ROWS = 512


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be positive")
    return parsed


def _load_schedule(schedule_path: Path, limit_shards: int | None = None) -> pd.DataFrame:
    if not schedule_path.exists():
        raise FileNotFoundError(schedule_path)
    schedule = pd.read_csv(schedule_path)
    required = {"trade_month", "symbol", "source_rows", "target_dense_rows", "target_dense_multiplier"}
    missing = sorted(required.difference(schedule.columns))
    if missing:
        raise ValueError(f"Schedule {schedule_path} is missing required columns: {missing}")
    schedule = schedule.sort_values(["trade_month", "symbol"], kind="mergesort").reset_index(drop=True)
    if limit_shards is not None:
        schedule = schedule.head(limit_shards).copy()
    return schedule


def _existing_inventory(output_dir: Path) -> pd.DataFrame:
    path = output_dir / "full_dense_lake_inventory.csv"
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


def _append_inventory(output_dir: Path, row: dict[str, object]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "full_dense_lake_inventory.csv"
    frame = pd.DataFrame([row])
    frame.to_csv(path, mode="a", header=not path.exists(), index=False)


def _target_file(output_root: Path, trade_month: str, symbol: str) -> Path:
    return output_root / f"trade_month={trade_month}" / f"symbol={symbol}" / "part-00000.parquet"


def _repeat_counts(source_rows: int, target_dense_rows: int) -> np.ndarray:
    base = target_dense_rows // source_rows
    remainder = target_dense_rows - base * source_rows
    counts = np.full(source_rows, base, dtype=np.int32)
    if remainder:
        counts[:remainder] += 1
    return counts


def _densify_chunk(
    chunk: pd.DataFrame,
    repeat_counts: np.ndarray,
    max_repeats: int,
    local_offset: int,
    cumulative_volume: dict[object, int],
    calibration_profile: GeneratorCalibrationProfile | None = None,
) -> pd.DataFrame:
    profile = calibration_profile or get_calibration_profile(None)
    if chunk.empty:
        return chunk.copy()

    repeated = chunk.loc[chunk.index.repeat(repeat_counts)].copy().reset_index(drop=True)
    dense_subtick_id = np.concatenate([np.arange(count, dtype=np.int16) for count in repeat_counts])
    repeated["dense_subtick_id"] = dense_subtick_id
    repeated["dense_multiplier"] = np.repeat(repeat_counts, repeat_counts).astype(np.int32)
    repeated["source_annual_event_id"] = repeated["annual_event_id"].astype("int64")
    repeated["annual_event_id"] = (
        repeated["annual_event_id"].astype("int64") * int(max_repeats)
        + repeated["dense_subtick_id"].astype("int64")
    )
    repeated["local_sequence_id"] = np.arange(local_offset + 1, local_offset + len(repeated) + 1, dtype=np.int64)
    repeated["callback_batch_id"] = repeated["local_sequence_id"].floordiv(32).astype("int64")
    timing_offset = (repeated["dense_subtick_id"].astype(float) * float(profile.event_timing_tail_gap_multiplier)).round().astype("int64")
    if float(profile.event_timing_burst_throttle_fraction) > 0:
        throttle_step = max(1, int(round(1.0 / float(profile.event_timing_burst_throttle_fraction))))
        timing_offset = timing_offset + (repeated["dense_subtick_id"].astype("int64") // throttle_step)
    repeated["callback_received_utc_ms"] = repeated["callback_received_utc_ms"].astype("int64") + timing_offset
    repeated["callback_received_monotonic_ns"] = repeated["callback_received_utc_ms"].astype("int64") * 1_000_000
    repeated["exchange_timestamp_ms"] = repeated["exchange_timestamp_ms"].astype("int64") + timing_offset
    repeated["last_trade_time_ms"] = repeated["exchange_timestamp_ms"]

    phase = (repeated["dense_subtick_id"].astype(float) / max(max_repeats - 1, 1)) - 0.5
    micro_step = (
        (repeated["sell_1_price"].astype(float) - repeated["buy_1_price"].astype(float)).abs().clip(lower=0.01)
        * float(profile.price_micro_step_spread_fraction)
        * float(profile.price_jump_size_scale)
    )
    direction = np.where((repeated["dense_subtick_id"].astype(int) % 2) == 0, 1.0, -1.0)
    repeated["last_price"] = (repeated["last_price"].astype(float) + direction * phase.abs() * micro_step).round(4)
    repeated["last_traded_quantity"] = np.maximum(
        1,
        (repeated["last_traded_quantity"].astype(float) / math.sqrt(max_repeats)).round(),
    ).astype("int64")

    volumes: list[pd.Series] = []
    for trade_date, date_frame in repeated.groupby("trade_date", sort=False):
        start = cumulative_volume.get(trade_date, 0)
        cumsum = date_frame["last_traded_quantity"].cumsum().astype("int64") + int(start)
        cumulative_volume[trade_date] = int(cumsum.iloc[-1])
        volumes.append(cumsum)
    repeated["volume_traded"] = pd.concat(volumes).sort_index().astype("int64")
    return repeated


def _write_dense_shard_chunked(
    symbol_frame: pd.DataFrame,
    target_file: Path,
    target_dense_rows: int,
    chunk_source_rows: int,
    calibration_profile: GeneratorCalibrationProfile | None = None,
) -> tuple[int, int, int]:
    source_rows = len(symbol_frame)
    if source_rows <= 0:
        raise ValueError("Cannot materialize an empty shard")
    if target_dense_rows < source_rows:
        raise ValueError("Target dense rows must be at least source rows")

    target_file.parent.mkdir(parents=True, exist_ok=True)
    if target_file.exists():
        target_file.unlink()

    counts = _repeat_counts(source_rows, target_dense_rows)
    max_repeats = int(counts.max())
    writer: pq.ParquetWriter | None = None
    total_dense_rows = 0
    local_offset = 0
    cumulative_volume: dict[object, int] = {}
    try:
        for start in range(0, source_rows, chunk_source_rows):
            end = min(start + chunk_source_rows, source_rows)
            chunk = symbol_frame.iloc[start:end].copy()
            dense = _densify_chunk(
                chunk,
                counts[start:end],
                max_repeats,
                local_offset=local_offset,
                cumulative_volume=cumulative_volume,
                calibration_profile=calibration_profile,
            )
            table = pa.Table.from_pandas(dense, preserve_index=False)
            if writer is None:
                writer = pq.ParquetWriter(target_file, table.schema, compression="zstd")
            writer.write_table(table)
            dense_rows = len(dense)
            total_dense_rows += dense_rows
            local_offset += dense_rows
            del dense
            del table
    finally:
        if writer is not None:
            writer.close()

    if total_dense_rows != target_dense_rows:
        raise AssertionError(f"Wrote {total_dense_rows} rows, expected {target_dense_rows}")
    return source_rows, total_dense_rows, int(target_file.stat().st_size)


def _write_summary(
    *,
    output_dir: Path,
    output_root: Path,
    schedule: pd.DataFrame,
    inventory: pd.DataFrame,
    elapsed_seconds: float,
    generated_utc: str,
    compact_root: Path,
    schedule_path: Path,
    chunk_source_rows: int,
    base_dir: Path,
    calibration_profile: GeneratorCalibrationProfile,
) -> None:
    dense_rows = int(inventory["dense_rows"].sum()) if len(inventory) else 0
    source_rows = int(inventory["source_rows"].sum()) if len(inventory) else 0
    dense_bytes = int(inventory["bytes"].sum()) if len(inventory) else 0
    partition_files = int(len(inventory))
    target_rows = int(schedule["target_dense_rows"].sum()) if len(schedule) else 0
    target_bytes = float(schedule["estimated_dense_bytes"].sum()) if "estimated_dense_bytes" in schedule else 0.0
    completed = partition_files == len(schedule) and dense_rows == target_rows
    disk = shutil.disk_usage(Path(".").resolve())
    summary = pd.DataFrame(
        [
            ("phase51_schedule_shards", int(len(schedule)), "Scheduled symbol-month dense shards"),
            ("phase51_source_rows", source_rows, "Source compact monthly rows materialized"),
            ("phase51_target_dense_rows", target_rows, "Target dense rows from Phase50 schedule"),
            ("phase51_materialized_dense_rows", dense_rows, "Dense rows actually materialized"),
            ("phase51_materialized_partition_files", partition_files, "Dense parquet files written"),
            ("phase51_materialized_dense_bytes", dense_bytes, "Compressed bytes actually written"),
            ("phase51_estimated_dense_bytes", target_bytes, "Phase50 estimated compressed bytes"),
            ("phase51_bytes_vs_estimate_ratio", dense_bytes / target_bytes if target_bytes else 0.0, "Actual compressed bytes divided by estimate"),
            ("phase51_elapsed_seconds", elapsed_seconds, "Elapsed materialization seconds"),
            ("phase51_rows_per_second", dense_rows / elapsed_seconds if elapsed_seconds > 0 else 0.0, "Observed materialization throughput"),
            ("phase51_available_disk_gb_after_run", disk.free / (1024**3), "Free disk after materialization"),
            ("phase51_dense_output_root", str(output_root), "Local full dense lake root; ignored by Git"),
            ("phase51_full_80gb_dense_lake_materialized", int(completed), "Full 80GB-class dense full-year lake materialized"),
            ("phase51_synthetic_full_year_acceptance_ready", 0, "Dense input lake materialized; strategy acceptance still requires replay results"),
        ],
        columns=["metric", "value", "description"],
    )
    summary.to_csv(output_dir / "full_dense_lake_summary.csv", index=False)

    lines = [
        "# Phase 51 Full Dense Lake Materializer",
        "",
        f"Generated UTC: {generated_utc}",
        "",
        "This phase materializes the Phase50 full symbol-month dense target schedule into a local ignored Parquet lake.",
        "It is the heavy raw-input generation milestone; acceptance remains closed until strategies are replayed on this dense lake.",
        "",
        "## Summary",
        "",
        _markdown_table(summary),
        "",
        "## Materialization Inventory",
        "",
        _markdown_table(inventory.head(120)),
        "",
    ]
    (output_dir / "phase51_full_dense_lake_materializer_report.md").write_text("\n".join(lines), encoding="utf-8")

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase51_full_dense_lake_materialization_not_acceptance",
        "schedule_shards": int(len(schedule)),
        "materialized_partition_files": partition_files,
        "materialized_dense_rows": dense_rows,
        "materialized_dense_bytes": dense_bytes,
        "full_80gb_dense_lake_materialized": int(completed),
        "synthetic_full_year_acceptance_ready": 0,
        "generator_calibration_profile": calibration_profile.to_manifest(),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase51",
            generated_utc=generated_utc,
            inputs={
                "compact_monthly_raw_lake": str(compact_root),
                "phase50_dense_target_schedule": str(schedule_path),
            },
            parameters={
                "chunk_source_rows": chunk_source_rows,
                "materialization_mode": "symbol_month_phase50_target_dense_rows",
                "resume_policy": "skip_existing_file_when_row_count_matches_inventory",
                "generator_calibration_profile_id": calibration_profile.profile_id,
            },
            outputs={
                "dense_output_root": str(output_root),
                "inventory": str(output_dir / "full_dense_lake_inventory.csv"),
                "summary": str(output_dir / "full_dense_lake_summary.csv"),
                "report": str(output_dir / "phase51_full_dense_lake_materializer_report.md"),
                "manifest": str(output_dir / "phase51_full_dense_lake_materializer_manifest.json"),
            },
            random_seed="none_deterministic_phase50_schedule_materialization",
            scenario_ids="phase50_full_symbol_month_dense_target_schedule",
            cost_model_version="not_applicable_dense_storage_generation_no_execution_costs",
            latency_model_version="phase45_raw_callback_sequence_plus_phase51_dense_subticks",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase51_full_dense_lake_materializer_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


def run_phase51(
    *,
    compact_root: Path,
    output_root: Path,
    output_dir: Path,
    schedule_path: Path,
    chunk_source_rows: int,
    reset: bool,
    limit_shards: int | None,
    base_dir: Path,
    calibration_profile_id: str | None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    calibration_profile = get_calibration_profile(calibration_profile_id)
    if reset and output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    if reset:
        inventory_path = output_dir / "full_dense_lake_inventory.csv"
        if inventory_path.exists():
            inventory_path.unlink()

    schedule = _load_schedule(schedule_path, limit_shards=limit_shards)
    existing = _existing_inventory(output_dir)
    completed = set()
    if len(existing):
        completed = {
            (str(row["trade_month"]), str(row["symbol"]))
            for row in existing.to_dict("records")
            if Path(str(row["file_path"])).exists()
            and int(row["dense_rows"]) == int(row["target_dense_rows"])
        }

    started = time.perf_counter()
    month_files = {path.parent.name.split("=", 1)[1]: path for path in compact_files(compact_root)}
    for trade_month, month_schedule in schedule.groupby("trade_month", sort=True):
        month = read_month(month_files[str(trade_month)], [])
        month = month.sort_values(["trade_date", "exchange", "symbol", "feed_profile", "annual_event_id"], kind="mergesort")
        for spec in month_schedule.sort_values("symbol", kind="mergesort").to_dict("records"):
            symbol = str(spec["symbol"])
            key = (str(trade_month), symbol)
            target_file = _target_file(output_root, str(trade_month), symbol)
            if key in completed:
                continue
            symbol_frame = month[month["symbol"].astype(str) == symbol].copy().reset_index(drop=True)
            source_rows, dense_rows, bytes_written = _write_dense_shard_chunked(
                symbol_frame=symbol_frame,
                target_file=target_file,
                target_dense_rows=int(spec["target_dense_rows"]),
                chunk_source_rows=chunk_source_rows,
                calibration_profile=calibration_profile,
            )
            _append_inventory(
                output_dir,
                {
                    "trade_month": str(trade_month),
                    "symbol": symbol,
                    "source_rows": source_rows,
                    "target_dense_rows": int(spec["target_dense_rows"]),
                    "dense_rows": dense_rows,
                    "target_dense_multiplier": float(spec["target_dense_multiplier"]),
                    "file_path": str(target_file),
                    "bytes": bytes_written,
                    "completed_utc": datetime.now(timezone.utc).isoformat(),
                },
            )
        del month

    elapsed_seconds = time.perf_counter() - started
    inventory = _existing_inventory(output_dir)
    if len(inventory):
        inventory = inventory.sort_values(["trade_month", "symbol"], kind="mergesort").reset_index(drop=True)
        inventory.to_csv(output_dir / "full_dense_lake_inventory.csv", index=False)

    generated_utc = datetime.now(timezone.utc).isoformat()
    _write_summary(
        output_dir=output_dir,
        output_root=output_root,
        schedule=schedule,
        inventory=inventory,
        elapsed_seconds=elapsed_seconds,
        generated_utc=generated_utc,
        compact_root=compact_root,
        schedule_path=schedule_path,
        chunk_source_rows=chunk_source_rows,
        base_dir=base_dir,
        calibration_profile=calibration_profile,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize the full Phase50 dense symbol-month lake.")
    parser.add_argument("--compact-root", type=Path, default=DEFAULT_COMPACT_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--schedule", type=Path, default=DEFAULT_SCHEDULE)
    parser.add_argument("--chunk-source-rows", type=_positive_int, default=DEFAULT_CHUNK_SOURCE_ROWS)
    parser.add_argument("--limit-shards", type=_positive_int)
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--calibration-profile-id", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase51(
        compact_root=args.compact_root,
        output_root=args.output_root,
        output_dir=args.output_dir,
        schedule_path=args.schedule,
        chunk_source_rows=args.chunk_source_rows,
        reset=args.reset,
        limit_shards=args.limit_shards,
        base_dir=args.base_dir,
        calibration_profile_id=args.calibration_profile_id,
    )


if __name__ == "__main__":
    main()
