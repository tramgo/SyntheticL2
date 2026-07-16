from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import duckdb
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


VIEW_NAME = "raw_l2_ticks"


BENCHMARK_QUERIES = [
    (
        "total_rows",
        f"select count(*)::bigint as value from {VIEW_NAME}",
        "Total rows query over raw L2 parquet view",
    ),
    (
        "distinct_symbols",
        f"select count(distinct symbol)::bigint as value from {VIEW_NAME}",
        "Distinct symbols query over raw L2 parquet view",
    ),
    (
        "distinct_trade_dates",
        f"select count(distinct trade_date)::bigint as value from {VIEW_NAME}",
        "Distinct trade dates query over raw L2 parquet view",
    ),
    (
        "distinct_feed_profiles",
        f"select count(distinct feed_profile)::bigint as value from {VIEW_NAME}",
        "Distinct feed profiles query over raw L2 parquet view",
    ),
    (
        "l1_l5_complete_rows",
        f"""
        select count(*)::bigint as value
        from {VIEW_NAME}
        where buy_1_price is not null and sell_1_price is not null
          and buy_5_price is not null and sell_5_price is not null
          and buy_1_quantity > 0 and sell_1_quantity > 0
          and buy_5_quantity > 0 and sell_5_quantity > 0
        """,
        "Rows with complete L1 and L5 price/quantity state",
    ),
    (
        "hdfcbank_rows",
        f"select count(*)::bigint as value from {VIEW_NAME} where symbol = 'HDFCBANK'",
        "Ticker-filtered raw-row count for HDFCBANK",
    ),
    (
        "sample_microstructure_agg",
        f"""
        select
            count(*)::bigint as rows,
            avg((sell_1_price + buy_1_price) / 2.0) as avg_mid,
            avg(sell_1_price - buy_1_price) as avg_spread,
            avg((buy_1_quantity - sell_1_quantity)::double / nullif((buy_1_quantity + sell_1_quantity), 0)) as avg_l1_imbalance
        from {VIEW_NAME}
        where symbol = 'HDFCBANK'
        """,
        "Ticker-filtered microstructure aggregate for HDFCBANK",
    ),
]


def connect(database_path: Path) -> duckdb.DuckDBPyConnection:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(database_path))
    con.execute("set threads = 4")
    return con


def create_raw_view(con: duckdb.DuckDBPyConnection, raw_root: Path) -> str:
    pattern = (raw_root / "**" / "*.parquet").as_posix()
    literal = pattern.replace("'", "''")
    con.execute(f"create or replace view {VIEW_NAME} as select * from read_parquet('{literal}', hive_partitioning=false, union_by_name=true)")
    return pattern


def schema_frame(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    return con.execute(f"describe {VIEW_NAME}").fetchdf()


def run_benchmarks(con: duckdb.DuckDBPyConnection) -> tuple[pd.DataFrame, pd.DataFrame]:
    benchmark_rows = []
    result_rows = []
    for query_id, sql, description in BENCHMARK_QUERIES:
        started = time.perf_counter()
        frame = con.execute(sql).fetchdf()
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        benchmark_rows.append(
            {
                "query_id": query_id,
                "elapsed_ms": elapsed_ms,
                "result_rows": int(len(frame)),
                "description": description,
                "sql": " ".join(sql.split()),
            }
        )
        first = frame.iloc[0].to_dict() if len(frame) else {}
        for key, value in first.items():
            result_rows.append(
                {
                    "query_id": query_id,
                    "metric": key,
                    "value": value,
                    "description": description,
                }
            )
    return pd.DataFrame(benchmark_rows), pd.DataFrame(result_rows)


def build_catalog_summary(
    inventory: pd.DataFrame,
    benchmark_results: pd.DataFrame,
    benchmark_timings: pd.DataFrame,
    database_path: Path,
    raw_root: Path,
) -> pd.DataFrame:
    result_lookup = {
        (row["query_id"], row["metric"]): row["value"]
        for row in benchmark_results.to_dict("records")
    }
    rows = [
        ("phase47_inventory_partitions", int(len(inventory)), "Raw parquet partitions in Phase45 inventory"),
        ("phase47_inventory_rows", int(inventory["rows"].sum()), "Raw rows declared by Phase45 inventory"),
        ("phase47_duckdb_total_rows", int(result_lookup.get(("total_rows", "value"), 0)), "Rows counted through DuckDB raw view"),
        ("phase47_duckdb_distinct_symbols", int(result_lookup.get(("distinct_symbols", "value"), 0)), "Distinct symbols counted through DuckDB raw view"),
        ("phase47_duckdb_distinct_trade_dates", int(result_lookup.get(("distinct_trade_dates", "value"), 0)), "Distinct trade dates counted through DuckDB raw view"),
        ("phase47_duckdb_distinct_feed_profiles", int(result_lookup.get(("distinct_feed_profiles", "value"), 0)), "Distinct feed profiles counted through DuckDB raw view"),
        ("phase47_duckdb_l1_l5_complete_rows", int(result_lookup.get(("l1_l5_complete_rows", "value"), 0)), "Rows with complete L1/L5 state through DuckDB raw view"),
        ("phase47_benchmark_query_rows", int(len(benchmark_timings)), "DuckDB benchmark queries executed"),
        ("phase47_max_query_elapsed_ms", float(benchmark_timings["elapsed_ms"].max()) if len(benchmark_timings) else 0.0, "Slowest benchmark query elapsed milliseconds"),
        ("phase47_raw_root", str(raw_root), "Raw parquet lake root queried by DuckDB"),
        ("phase47_duckdb_database", str(database_path), "Local DuckDB database path; ignored by Git"),
        ("phase47_synthetic_full_year_acceptance_ready", 0, "DuckDB catalog is storage/query infrastructure evidence, not strategy acceptance"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase 47 Raw Lake DuckDB Catalog",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This phase registers the Phase 45 partitioned raw websocket-like L2 parquet lake as a DuckDB query source and runs benchmark/integrity SQL queries.",
        "It is storage/query infrastructure for future raw-source experiments, not strategy acceptance evidence.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase47_raw_lake_duckdb_catalog_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase47(raw_root: Path, inventory_path: Path, database_path: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    if not raw_root.exists():
        raise FileNotFoundError(raw_root)
    if not inventory_path.exists():
        raise FileNotFoundError(inventory_path)
    inventory = pd.read_csv(inventory_path)
    con = connect(database_path)
    try:
        parquet_pattern = create_raw_view(con, raw_root)
        schema = schema_frame(con)
        benchmark_timings, benchmark_results = run_benchmarks(con)
    finally:
        con.close()
    summary = build_catalog_summary(inventory, benchmark_results, benchmark_timings, database_path, raw_root)
    summary.to_csv(output_dir / "raw_lake_duckdb_catalog_summary.csv", index=False)
    schema.to_csv(output_dir / "raw_lake_duckdb_schema.csv", index=False)
    benchmark_timings.to_csv(output_dir / "raw_lake_duckdb_benchmark_timings.csv", index=False)
    benchmark_results.to_csv(output_dir / "raw_lake_duckdb_benchmark_results.csv", index=False)
    write_report(
        output_dir,
        {
            "Catalog Summary": summary,
            "Benchmark Timings": benchmark_timings,
            "Benchmark Results": benchmark_results,
            "Schema": schema,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase47_raw_lake_duckdb_catalog_not_acceptance",
        "raw_root": str(raw_root),
        "parquet_pattern": parquet_pattern,
        "benchmark_queries": int(len(benchmark_timings)),
        "synthetic_full_year_acceptance_ready": 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase47",
            generated_utc=generated_utc,
            inputs={
                "raw_root": str(raw_root),
                "partition_inventory": str(inventory_path),
            },
            parameters={
                "duckdb_view_name": VIEW_NAME,
                "hive_partitioning": False,
                "union_by_name": True,
                "benchmark_query_ids": [row[0] for row in BENCHMARK_QUERIES],
                "acceptance_boundary": "raw_lake_query_infrastructure_not_acceptance",
            },
            outputs={
                "database": str(database_path),
                "summary": str(output_dir / "raw_lake_duckdb_catalog_summary.csv"),
                "schema": str(output_dir / "raw_lake_duckdb_schema.csv"),
                "benchmark_timings": str(output_dir / "raw_lake_duckdb_benchmark_timings.csv"),
                "benchmark_results": str(output_dir / "raw_lake_duckdb_benchmark_results.csv"),
                "report": str(output_dir / "phase47_raw_lake_duckdb_catalog_report.md"),
                "manifest": str(output_dir / "phase47_raw_lake_duckdb_catalog_manifest.json"),
            },
            random_seed="none_deterministic_duckdb_raw_lake_catalog",
            scenario_ids="phase45_raw_full_year_l2_tick_lake",
            cost_model_version="not_applicable_storage_query_no_execution_costs",
            latency_model_version="phase45_raw_callback_sequence_and_l1_l5_depth_schema",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase47_raw_lake_duckdb_catalog_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build DuckDB catalog over raw L2 tick lake.")
    parser.add_argument("--raw-root", type=Path, default=Path("raw_synthetic_l2_full_year"))
    parser.add_argument("--inventory", type=Path, default=Path("outputs/phase45/raw_tick_lake_partition_inventory.csv"))
    parser.add_argument("--database", type=Path, default=Path("outputs/phase47/raw_lake.duckdb"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase47"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase47(args.raw_root, args.inventory, args.database, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
