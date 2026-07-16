from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import duckdb
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase49_dense_tick_rate_expansion import run_dense_expansion
from synthetic_l2.reproducibility import reproducibility_fields


TARGET_DENSE_RAW_GB = 83.240
DEFAULT_SELECTED_SYMBOLS = ["HDFCBANK", "RELIANCE", "INFY"]
DEFAULT_SHARD_MULTIPLIER = 64


def read_phase49_calibration(path: Path) -> dict[str, float]:
    if not path.exists():
        raise FileNotFoundError(path)
    frame = pd.read_csv(path)
    values = {row["metric"]: row["value"] for row in frame.to_dict("records")}
    return {
        "bytes_per_row": float(values["phase49_dense_bytes_per_row"]),
        "rows_per_second": float(values["phase49_rows_per_second"]),
        "target_gb": float(values.get("phase49_target_dense_raw_gb", TARGET_DENSE_RAW_GB)),
    }


def collect_symbol_month_rows(compact_root: Path) -> pd.DataFrame:
    pattern = (compact_root / "**" / "*.parquet").as_posix().replace("'", "''")
    con = duckdb.connect()
    try:
        rows = con.execute(
            f"""
            select
                substr(cast(trade_date as varchar), 1, 7) as trade_month,
                symbol,
                count(*)::bigint as source_rows
            from read_parquet('{pattern}', hive_partitioning=false, union_by_name=true)
            group by 1, 2
            order by symbol, trade_month
            """
        ).fetchdf()
    finally:
        con.close()
    return rows


def build_target_schedule(symbol_month: pd.DataFrame, calibration: dict[str, float]) -> tuple[pd.DataFrame, float, float]:
    total_source_rows = int(symbol_month["source_rows"].sum())
    target_bytes = calibration["target_gb"] * (1024**3)
    target_rows = target_bytes / calibration["bytes_per_row"]
    target_multiplier = target_rows / total_source_rows if total_source_rows else 0.0
    schedule = symbol_month.copy()
    schedule["target_dense_multiplier"] = target_multiplier
    schedule["target_dense_rows"] = (schedule["source_rows"] * target_multiplier).round().astype("int64")
    schedule["estimated_dense_bytes"] = schedule["target_dense_rows"] * calibration["bytes_per_row"]
    schedule["estimated_runtime_seconds"] = schedule["target_dense_rows"] / calibration["rows_per_second"]
    schedule["shard_id"] = (
        "dense_target_"
        + schedule["symbol"].astype(str)
        + "_"
        + schedule["trade_month"].astype(str)
    )
    schedule = schedule[
        [
            "shard_id",
            "trade_month",
            "symbol",
            "source_rows",
            "target_dense_multiplier",
            "target_dense_rows",
            "estimated_dense_bytes",
            "estimated_runtime_seconds",
        ]
    ].sort_values(["estimated_dense_bytes", "symbol", "trade_month"], ascending=[False, True, True], kind="mergesort")
    return schedule.reset_index(drop=True), target_rows, target_multiplier


def build_run_plan(schedule: pd.DataFrame, selected_symbols: list[str], shard_multiplier: int) -> pd.DataFrame:
    selected = schedule[schedule["symbol"].isin(selected_symbols)].copy()
    selected["planned_materialization_multiplier"] = shard_multiplier
    selected["planned_dense_rows"] = selected["source_rows"] * shard_multiplier
    selected["materialization_scope"] = "phase50_bounded_multisymbol_validation_shard"
    return selected.sort_values(["symbol", "trade_month"], kind="mergesort").reset_index(drop=True)


def build_summary(
    *,
    schedule: pd.DataFrame,
    run_plan: pd.DataFrame,
    materialized_inventory: pd.DataFrame,
    calibration: dict[str, float],
    target_rows: float,
    target_multiplier: float,
    output_root: Path,
) -> pd.DataFrame:
    dense_rows = int(materialized_inventory["dense_rows"].sum()) if len(materialized_inventory) else 0
    dense_bytes = int(materialized_inventory["bytes"].sum()) if len(materialized_inventory) else 0
    rows = [
        ("phase50_target_dense_raw_gb", calibration["target_gb"], "Target compressed dense raw lake size"),
        ("phase50_target_dense_rows", target_rows, "Dense rows implied by Phase49 measured compression"),
        ("phase50_target_full_universe_multiplier", target_multiplier, "Full-universe multiplier implied by target dense rows"),
        ("phase50_schedule_shards", int(len(schedule)), "Symbol-month shards in full dense target schedule"),
        ("phase50_schedule_source_rows", int(schedule["source_rows"].sum()), "Current compact monthly source rows covered by schedule"),
        ("phase50_schedule_estimated_dense_bytes", float(schedule["estimated_dense_bytes"].sum()), "Estimated compressed bytes for target schedule"),
        ("phase50_schedule_estimated_runtime_hours", float(schedule["estimated_runtime_seconds"].sum() / 3600.0), "Estimated runtime hours at Phase49 measured throughput"),
        ("phase50_selected_symbols", ";".join(sorted(run_plan["symbol"].unique().tolist())) if len(run_plan) else "", "Symbols selected for bounded materialization"),
        ("phase50_selected_shards", int(len(run_plan)), "Selected symbol-month shards for bounded materialization"),
        ("phase50_materialized_dense_rows", dense_rows, "Dense rows materialized in bounded multi-symbol run"),
        ("phase50_materialized_dense_bytes", dense_bytes, "Compressed bytes materialized in bounded multi-symbol run"),
        ("phase50_materialized_partition_files", int(len(materialized_inventory)), "Dense parquet files written in bounded run"),
        ("phase50_dense_output_root", str(output_root), "Local bounded dense output root; ignored by Git"),
        ("phase50_full_80gb_dense_lake_materialized", 0, "80GB-class dense full-universe lake not materialized by Phase50"),
        ("phase50_synthetic_full_year_acceptance_ready", 0, "Dense shard planning is storage/input evidence, not strategy acceptance"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase 50 Dense Lake Shard Planner",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This phase converts the Phase49 dense calibration into a full symbol-month shard schedule for the 80GB-class dense target and validates the plan with a bounded multi-symbol materialization.",
        "It is storage/input orchestration evidence, not strategy acceptance evidence.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase50_dense_lake_shard_planner_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase50(
    compact_root: Path,
    output_root: Path,
    output_dir: Path,
    base_dir: Path,
    selected_symbols: list[str],
    shard_multiplier: int,
    calibration_path: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    calibration = read_phase49_calibration(calibration_path)
    symbol_month = collect_symbol_month_rows(compact_root)
    schedule, target_rows, target_multiplier = build_target_schedule(symbol_month, calibration)
    run_plan = build_run_plan(schedule, selected_symbols, shard_multiplier)
    materialized_inventory, elapsed = run_dense_expansion(compact_root, output_root, selected_symbols, shard_multiplier)
    summary = build_summary(
        schedule=schedule,
        run_plan=run_plan,
        materialized_inventory=materialized_inventory,
        calibration=calibration,
        target_rows=target_rows,
        target_multiplier=target_multiplier,
        output_root=output_root,
    )
    materialized_inventory["elapsed_seconds_total"] = elapsed
    schedule.to_csv(output_dir / "dense_target_shard_schedule.csv", index=False)
    run_plan.to_csv(output_dir / "dense_bounded_run_plan.csv", index=False)
    materialized_inventory.to_csv(output_dir / "dense_bounded_materialization_inventory.csv", index=False)
    summary.to_csv(output_dir / "dense_lake_shard_planner_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Planner Summary": summary,
            "Bounded Run Plan": run_plan,
            "Bounded Materialization Inventory": materialized_inventory,
            "Top Target Schedule Shards": schedule.head(80),
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase50_dense_lake_shard_planner_not_acceptance",
        "target_schedule_shards": int(len(schedule)),
        "selected_symbols": selected_symbols,
        "selected_multiplier": shard_multiplier,
        "materialized_dense_rows": int(materialized_inventory["dense_rows"].sum()) if len(materialized_inventory) else 0,
        "synthetic_full_year_acceptance_ready": 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase50",
            generated_utc=generated_utc,
            inputs={
                "compact_monthly_raw_lake": str(compact_root),
                "phase49_calibration": str(calibration_path),
            },
            parameters={
                "selected_symbols": selected_symbols,
                "selected_multiplier": shard_multiplier,
                "target_dense_raw_gb": calibration["target_gb"],
                "target_multiplier": target_multiplier,
                "acceptance_boundary": "dense_storage_orchestration_not_acceptance",
            },
            outputs={
                "dense_output_root": str(output_root),
                "target_schedule": str(output_dir / "dense_target_shard_schedule.csv"),
                "bounded_run_plan": str(output_dir / "dense_bounded_run_plan.csv"),
                "bounded_inventory": str(output_dir / "dense_bounded_materialization_inventory.csv"),
                "summary": str(output_dir / "dense_lake_shard_planner_summary.csv"),
                "report": str(output_dir / "phase50_dense_lake_shard_planner_report.md"),
                "manifest": str(output_dir / "phase50_dense_lake_shard_planner_manifest.json"),
            },
            random_seed="none_deterministic_dense_shard_planner",
            scenario_ids="phase48_compact_monthly_raw_lake_dense_shard_schedule",
            cost_model_version="not_applicable_dense_storage_planning_no_execution_costs",
            latency_model_version="phase45_raw_callback_sequence_plus_dense_subticks",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase50_dense_lake_shard_planner_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan dense full-lake shards and materialize a bounded validation run.")
    parser.add_argument("--compact-root", type=Path, default=Path("raw_synthetic_l2_full_year_compact_monthly"))
    parser.add_argument("--output-root", type=Path, default=Path("raw_synthetic_l2_dense_phase50_multisymbol_x64"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase50"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--symbols", nargs="+", default=DEFAULT_SELECTED_SYMBOLS)
    parser.add_argument("--multiplier", type=int, default=DEFAULT_SHARD_MULTIPLIER)
    parser.add_argument("--calibration", type=Path, default=Path("outputs/phase49/dense_tick_expansion_summary.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase50(args.compact_root, args.output_root, args.output_dir, args.base_dir, args.symbols, args.multiplier, args.calibration)


if __name__ == "__main__":
    main()
