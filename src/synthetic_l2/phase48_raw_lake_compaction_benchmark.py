from __future__ import annotations

import argparse
import json
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

import duckdb
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


RAW_VIEW = "raw_l2_ticks"
COMPACT_VIEW = "compact_l2_ticks"


QUERY_TEMPLATES = [
    ("total_rows", "select count(*)::bigint as value from {view}", "Total rows"),
    ("distinct_symbols", "select count(distinct symbol)::bigint as value from {view}", "Distinct symbols"),
    ("distinct_trade_dates", "select count(distinct trade_date)::bigint as value from {view}", "Distinct trade dates"),
    ("distinct_feed_profiles", "select count(distinct feed_profile)::bigint as value from {view}", "Distinct feed profiles"),
    (
        "l1_l5_complete_rows",
        """
        select count(*)::bigint as value
        from {view}
        where buy_1_price is not null and sell_1_price is not null
          and buy_5_price is not null and sell_5_price is not null
          and buy_1_quantity > 0 and sell_1_quantity > 0
          and buy_5_quantity > 0 and sell_5_quantity > 0
        """,
        "Rows with complete L1/L5 price/quantity state",
    ),
    ("hdfcbank_rows", "select count(*)::bigint as value from {view} where symbol = 'HDFCBANK'", "HDFCBANK row count"),
    (
        "sample_microstructure_agg",
        """
        select
            count(*)::bigint as rows,
            avg((sell_1_price + buy_1_price) / 2.0) as avg_mid,
            avg(sell_1_price - buy_1_price) as avg_spread,
            avg((buy_1_quantity - sell_1_quantity)::double / nullif((buy_1_quantity + sell_1_quantity), 0)) as avg_l1_imbalance
        from {view}
        where symbol = 'HDFCBANK'
        """,
        "HDFCBANK microstructure aggregate",
    ),
]


def connect(database_path: Path) -> duckdb.DuckDBPyConnection:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(database_path))
    con.execute("set threads = 4")
    return con


def quoted_pattern(root: Path) -> str:
    return (root / "**" / "*.parquet").as_posix().replace("'", "''")


def create_view(con: duckdb.DuckDBPyConnection, view_name: str, root: Path) -> None:
    con.execute(
        f"create or replace view {view_name} as "
        f"select * from read_parquet('{quoted_pattern(root)}', hive_partitioning=false, union_by_name=true)"
    )


def compact_raw_lake(con: duckdb.DuckDBPyConnection, raw_root: Path, compact_root: Path) -> pd.DataFrame:
    if compact_root.exists():
        shutil.rmtree(compact_root)
    compact_root.mkdir(parents=True, exist_ok=True)
    create_view(con, RAW_VIEW, raw_root)
    months = con.execute(
        f"""
        select distinct substr(cast(trade_date as varchar), 1, 7) as trade_month
        from {RAW_VIEW}
        order by trade_month
        """
    ).fetchdf()["trade_month"].tolist()
    rows = []
    for month in months:
        target_dir = compact_root / f"trade_month={month}"
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / "part-00000.parquet"
        month_literal = str(month).replace("'", "''")
        file_literal = target_file.as_posix().replace("'", "''")
        con.execute(
            f"""
            copy (
                select *
                from {RAW_VIEW}
                where substr(cast(trade_date as varchar), 1, 7) = '{month_literal}'
                order by trade_date, exchange, symbol, feed_profile, annual_event_id
            )
            to '{file_literal}' (format parquet, compression zstd)
            """
        )
        row_count = con.execute(
            f"select count(*)::bigint from {RAW_VIEW} where substr(cast(trade_date as varchar), 1, 7) = '{month_literal}'"
        ).fetchone()[0]
        rows.append(
            {
                "trade_month": month,
                "file_path": str(target_file),
                "rows": int(row_count),
                "bytes": int(target_file.stat().st_size),
            }
        )
    return pd.DataFrame(rows)


def run_benchmarks(con: duckdb.DuckDBPyConnection, view_name: str, label: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    timings = []
    results = []
    for query_id, template, description in QUERY_TEMPLATES:
        sql = template.format(view=view_name)
        started = time.perf_counter()
        frame = con.execute(sql).fetchdf()
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        timings.append(
            {
                "lake_layout": label,
                "query_id": query_id,
                "elapsed_ms": elapsed_ms,
                "result_rows": int(len(frame)),
                "description": description,
                "sql": " ".join(sql.split()),
            }
        )
        first = frame.iloc[0].to_dict() if len(frame) else {}
        for metric, value in first.items():
            results.append(
                {
                    "lake_layout": label,
                    "query_id": query_id,
                    "metric": metric,
                    "value": value,
                    "description": description,
                }
            )
    return pd.DataFrame(timings), pd.DataFrame(results)


def build_comparison(raw_timings: pd.DataFrame, compact_timings: pd.DataFrame) -> pd.DataFrame:
    raw = raw_timings[["query_id", "elapsed_ms"]].rename(columns={"elapsed_ms": "raw_elapsed_ms"})
    compact = compact_timings[["query_id", "elapsed_ms"]].rename(columns={"elapsed_ms": "compact_elapsed_ms"})
    merged = raw.merge(compact, on="query_id", how="inner")
    merged["speedup_ratio"] = merged["raw_elapsed_ms"] / merged["compact_elapsed_ms"].replace(0.0, pd.NA)
    return merged.sort_values("speedup_ratio", ascending=False, kind="mergesort")


def build_summary(
    inventory: pd.DataFrame,
    compact_inventory: pd.DataFrame,
    comparison: pd.DataFrame,
    raw_results: pd.DataFrame,
    compact_results: pd.DataFrame,
    compact_root: Path,
    database_path: Path,
) -> pd.DataFrame:
    raw_total = int(raw_results[(raw_results["query_id"] == "total_rows") & (raw_results["metric"] == "value")]["value"].iloc[0])
    compact_total = int(compact_results[(compact_results["query_id"] == "total_rows") & (compact_results["metric"] == "value")]["value"].iloc[0])
    rows = [
        ("phase48_raw_partition_files", int(len(inventory)), "Original raw date/exchange/symbol parquet files"),
        ("phase48_compact_partition_files", int(len(compact_inventory)), "Compacted monthly parquet files"),
        ("phase48_file_count_reduction_ratio", float(len(inventory) / len(compact_inventory)) if len(compact_inventory) else 0.0, "Original file count divided by compact file count"),
        ("phase48_raw_rows", raw_total, "Rows counted through original raw DuckDB view"),
        ("phase48_compact_rows", compact_total, "Rows counted through compact DuckDB view"),
        ("phase48_row_count_match", int(raw_total == compact_total), "Compacted row count matches raw row count"),
        ("phase48_raw_bytes", int(inventory["bytes"].sum()), "Original raw parquet bytes from Phase45 inventory"),
        ("phase48_compact_bytes", int(compact_inventory["bytes"].sum()), "Compacted parquet bytes"),
        ("phase48_best_query_speedup_ratio", float(comparison["speedup_ratio"].max()) if len(comparison) else 0.0, "Best raw-to-compact query speedup ratio"),
        ("phase48_median_query_speedup_ratio", float(comparison["speedup_ratio"].median()) if len(comparison) else 0.0, "Median raw-to-compact query speedup ratio"),
        ("phase48_compact_root", str(compact_root), "Local compacted raw lake root; ignored by Git"),
        ("phase48_duckdb_database", str(database_path), "Local DuckDB database path; ignored by Git"),
        ("phase48_synthetic_full_year_acceptance_ready", 0, "Compaction benchmark is storage/query infrastructure evidence, not strategy acceptance"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase 48 Raw Lake Compaction Benchmark",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This phase compacts the Phase 45 date/exchange/symbol raw parquet lake into larger monthly parquet files and benchmarks DuckDB SQL queries before and after compaction.",
        "It is storage/query infrastructure evidence, not strategy acceptance evidence.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase48_raw_lake_compaction_benchmark_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase48(
    raw_root: Path,
    inventory_path: Path,
    compact_root: Path,
    database_path: Path,
    output_dir: Path,
    base_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    inventory = pd.read_csv(inventory_path)
    con = connect(database_path)
    try:
        compact_inventory = compact_raw_lake(con, raw_root, compact_root)
        create_view(con, RAW_VIEW, raw_root)
        create_view(con, COMPACT_VIEW, compact_root)
        raw_timings, raw_results = run_benchmarks(con, RAW_VIEW, "raw_symbol_day")
        compact_timings, compact_results = run_benchmarks(con, COMPACT_VIEW, "compact_monthly")
    finally:
        con.close()
    timings = pd.concat([raw_timings, compact_timings], ignore_index=True)
    results = pd.concat([raw_results, compact_results], ignore_index=True)
    comparison = build_comparison(raw_timings, compact_timings)
    summary = build_summary(inventory, compact_inventory, comparison, raw_results, compact_results, compact_root, database_path)
    compact_inventory.to_csv(output_dir / "compact_raw_lake_inventory.csv", index=False)
    timings.to_csv(output_dir / "raw_lake_compaction_benchmark_timings.csv", index=False)
    results.to_csv(output_dir / "raw_lake_compaction_benchmark_results.csv", index=False)
    comparison.to_csv(output_dir / "raw_lake_compaction_speedup_comparison.csv", index=False)
    summary.to_csv(output_dir / "raw_lake_compaction_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Compaction Summary": summary,
            "Speedup Comparison": comparison,
            "Compact Inventory": compact_inventory,
            "Benchmark Timings": timings,
            "Benchmark Results": results,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase48_raw_lake_compaction_benchmark_not_acceptance",
        "raw_files": int(len(inventory)),
        "compact_files": int(len(compact_inventory)),
        "benchmark_queries_per_layout": int(len(QUERY_TEMPLATES)),
        "synthetic_full_year_acceptance_ready": 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase48",
            generated_utc=generated_utc,
            inputs={
                "raw_root": str(raw_root),
                "partition_inventory": str(inventory_path),
            },
            parameters={
                "compaction_layout": "trade_month=YYYY-MM/part-00000.parquet",
                "duckdb_raw_view": RAW_VIEW,
                "duckdb_compact_view": COMPACT_VIEW,
                "benchmark_query_ids": [query_id for query_id, _, _ in QUERY_TEMPLATES],
                "acceptance_boundary": "raw_lake_storage_optimization_not_acceptance",
            },
            outputs={
                "compact_root": str(compact_root),
                "database": str(database_path),
                "summary": str(output_dir / "raw_lake_compaction_summary.csv"),
                "compact_inventory": str(output_dir / "compact_raw_lake_inventory.csv"),
                "benchmark_timings": str(output_dir / "raw_lake_compaction_benchmark_timings.csv"),
                "benchmark_results": str(output_dir / "raw_lake_compaction_benchmark_results.csv"),
                "speedup_comparison": str(output_dir / "raw_lake_compaction_speedup_comparison.csv"),
                "report": str(output_dir / "phase48_raw_lake_compaction_benchmark_report.md"),
                "manifest": str(output_dir / "phase48_raw_lake_compaction_benchmark_manifest.json"),
            },
            random_seed="none_deterministic_duckdb_raw_lake_compaction",
            scenario_ids="phase45_raw_full_year_l2_tick_lake_compacted_monthly",
            cost_model_version="not_applicable_storage_query_no_execution_costs",
            latency_model_version="phase45_raw_callback_sequence_and_l1_l5_depth_schema",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase48_raw_lake_compaction_benchmark_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compact raw L2 parquet lake and benchmark DuckDB scans.")
    parser.add_argument("--raw-root", type=Path, default=Path("raw_synthetic_l2_full_year"))
    parser.add_argument("--inventory", type=Path, default=Path("outputs/phase45/raw_tick_lake_partition_inventory.csv"))
    parser.add_argument("--compact-root", type=Path, default=Path("raw_synthetic_l2_full_year_compact_monthly"))
    parser.add_argument("--database", type=Path, default=Path("outputs/phase48/raw_lake_compaction.duckdb"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase48"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase48(args.raw_root, args.inventory, args.compact_root, args.database, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
