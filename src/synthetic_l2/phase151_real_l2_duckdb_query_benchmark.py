from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_OUTPUT_DIR = Path("outputs/phase151")
DEFAULT_REAL_PANEL_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_CATALOG_DB = Path("outputs/phase150/real_l2_catalog.duckdb")
DEFAULT_SYMBOLS = ["HDFCBANK", "RELIANCE", "ADANIPORTS"]
DEFAULT_EXCHANGE = "NSE"


def quote_sql(value: str) -> str:
    return value.replace("'", "''")


def run_timed_query(con: duckdb.DuckDBPyConnection, query_id: str, sql: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    started = time.perf_counter()
    status = "completed"
    error = ""
    try:
        frame = con.execute(sql).fetchdf()
        rows = int(len(frame))
    except Exception as exc:
        frame = pd.DataFrame()
        rows = 0
        status = "failed"
        error = repr(exc)
    elapsed = time.perf_counter() - started
    return frame, {
        "query_id": query_id,
        "status": status,
        "elapsed_seconds": elapsed,
        "result_rows": rows,
        "sql": sql,
        "error": error,
    }


def partition_glob(root: Path, trade_date: str, exchange: str, symbol: str) -> str:
    return (root / f"trade_date={trade_date}" / f"exchange={exchange}" / f"symbol={symbol}" / "*.parquet").as_posix()


def choose_benchmark_partitions(con: duckdb.DuckDBPyConnection, symbols: list[str], exchange: str) -> pd.DataFrame:
    available = con.execute(
        """
        SELECT trade_date, exchange, symbol, parquet_files, bytes
        FROM real_l2_date_symbol_summary
        WHERE exchange = ?
        ORDER BY bytes DESC, trade_date, symbol
        """,
        [exchange],
    ).fetchdf()
    if available.empty:
        return pd.DataFrame(columns=["trade_date", "exchange", "symbol", "parquet_files", "bytes", "selection_reason"])
    selected: list[pd.DataFrame] = []
    for symbol in symbols:
        rows = available[available["symbol"].astype(str).eq(symbol)].head(1).copy()
        if not rows.empty:
            rows["selection_reason"] = "largest_partition_for_requested_symbol"
            selected.append(rows)
    largest = available.head(1).copy()
    largest["selection_reason"] = "largest_partition_overall"
    selected.append(largest)
    result = pd.concat(selected, ignore_index=True).drop_duplicates(["trade_date", "exchange", "symbol"], keep="first")
    return result.sort_values(["trade_date", "symbol"]).reset_index(drop=True)


def run_partition_benchmarks(root: Path, db_path: Path, symbols: list[str], exchange: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        partitions = choose_benchmark_partitions(con, symbols, exchange)
        query_rows: list[dict[str, Any]] = []
        result_rows: list[dict[str, Any]] = []
        for item in partitions.to_dict("records"):
            trade_date = str(item["trade_date"])
            symbol = str(item["symbol"])
            glob = quote_sql(partition_glob(root, trade_date, exchange, symbol))
            count_sql = f"""
            SELECT
                '{quote_sql(trade_date)}' AS trade_date,
                '{quote_sql(exchange)}' AS exchange,
                '{quote_sql(symbol)}' AS symbol,
                count(*) AS rows,
                min(collector_received_utc_ms) AS min_received_ms,
                max(collector_received_utc_ms) AS max_received_ms,
                min(last_price) AS min_last_price,
                max(last_price) AS max_last_price
            FROM parquet_scan('{glob}', union_by_name=true)
            """
            count_frame, count_meta = run_timed_query(con, f"count_{trade_date}_{symbol}", count_sql)
            query_rows.append(count_meta)
            result_rows.extend(count_frame.to_dict("records"))

            spread_sql = f"""
            SELECT
                '{quote_sql(trade_date)}' AS trade_date,
                '{quote_sql(exchange)}' AS exchange,
                '{quote_sql(symbol)}' AS symbol,
                count(*) AS rows,
                avg(sell_1_price - buy_1_price) AS avg_l1_spread_abs,
                avg(CASE WHEN buy_1_price > 0 AND sell_1_price >= buy_1_price THEN 1 ELSE 0 END) AS l1_book_valid_fraction,
                avg(CASE WHEN buy_5_quantity > 0 OR sell_5_quantity > 0 THEN 1 ELSE 0 END) AS depth_level_5_present_fraction,
                avg(total_buy_quantity) AS avg_total_buy_quantity,
                avg(total_sell_quantity) AS avg_total_sell_quantity
            FROM parquet_scan('{glob}', union_by_name=true)
            """
            spread_frame, spread_meta = run_timed_query(con, f"spread_depth_{trade_date}_{symbol}", spread_sql)
            query_rows.append(spread_meta)
            result_rows.extend(spread_frame.to_dict("records"))
        metadata_sql = """
        SELECT
            count(*) AS cataloged_files,
            sum(bytes) AS cataloged_bytes,
            count(DISTINCT trade_date) AS cataloged_trade_dates,
            count(DISTINCT symbol) AS cataloged_symbols
        FROM real_l2_parquet_files
        """
        metadata_frame, metadata_meta = run_timed_query(con, "metadata_catalog_summary", metadata_sql)
        query_rows.append(metadata_meta)
        result_rows.extend(metadata_frame.to_dict("records"))
        return partitions, pd.DataFrame(query_rows), pd.DataFrame(result_rows)
    finally:
        con.close()


def summarize(partitions: pd.DataFrame, queries: pd.DataFrame, results: pd.DataFrame, db_path: Path) -> pd.DataFrame:
    failures = int((queries["status"].astype(str) != "completed").sum()) if not queries.empty else 1
    total_elapsed = float(pd.to_numeric(queries["elapsed_seconds"], errors="coerce").fillna(0.0).sum()) if not queries.empty else 0.0
    max_elapsed = float(pd.to_numeric(queries["elapsed_seconds"], errors="coerce").fillna(0.0).max()) if not queries.empty else 0.0
    partition_result_rows = results[results["trade_date"].notna()] if not results.empty and "trade_date" in results.columns else pd.DataFrame()
    min_valid_fraction = (
        float(pd.to_numeric(partition_result_rows["l1_book_valid_fraction"], errors="coerce").dropna().min())
        if not partition_result_rows.empty and "l1_book_valid_fraction" in partition_result_rows.columns and not pd.to_numeric(partition_result_rows["l1_book_valid_fraction"], errors="coerce").dropna().empty
        else 0.0
    )
    min_l5_fraction = (
        float(pd.to_numeric(partition_result_rows["depth_level_5_present_fraction"], errors="coerce").dropna().min())
        if not partition_result_rows.empty and "depth_level_5_present_fraction" in partition_result_rows.columns and not pd.to_numeric(partition_result_rows["depth_level_5_present_fraction"], errors="coerce").dropna().empty
        else 0.0
    )
    return pd.DataFrame(
        [
            ("phase151_catalog_db_exists", int(db_path.exists()), "Phase150 DuckDB catalog database exists locally"),
            ("phase151_benchmark_partitions", int(len(partitions)), "Date/symbol partitions selected for bounded benchmark queries"),
            ("phase151_queries_attempted", int(len(queries)), "DuckDB queries attempted"),
            ("phase151_failed_queries", failures, "DuckDB queries failed"),
            ("phase151_total_query_elapsed_seconds", total_elapsed, "Total elapsed seconds across benchmark queries"),
            ("phase151_max_query_elapsed_seconds", max_elapsed, "Slowest bounded benchmark query elapsed seconds"),
            ("phase151_min_l1_book_valid_fraction", min_valid_fraction, "Minimum valid L1 book fraction among spread/depth benchmark partitions"),
            ("phase151_min_depth_level_5_present_fraction", min_l5_fraction, "Minimum visible level-5 presence among benchmark partitions"),
            ("phase151_strategy_replay_allowed", 0, "Query benchmark does not unlock strategy replay"),
            ("phase151_next_best_action", "use_partition_scoped_duckdb_queries_for_local_real_l2_analysis_after_phase148_downloads", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase151 Real L2 DuckDB Query Benchmark",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase151 verifies bounded local DuckDB queries over the real L2 Parquet panel cataloged by Phase150.",
        "It deliberately uses partition-scoped Parquet scans and catalog metadata queries. It does not contact Azure, copy tick rows into DuckDB, or unlock strategy replay.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase151_real_l2_duckdb_query_benchmark_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase151(output_dir: Path, base_dir: Path, real_panel_root: Path, db_path: Path, symbols: list[str], exchange: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    partitions, queries, results = run_partition_benchmarks(real_panel_root, db_path, symbols, exchange)
    acceptance = summarize(partitions, queries, results, db_path)

    partitions.to_csv(output_dir / "phase151_benchmark_partitions.csv", index=False)
    queries.to_csv(output_dir / "phase151_query_timing_ledger.csv", index=False)
    results.to_csv(output_dir / "phase151_query_results.csv", index=False)
    acceptance.to_csv(output_dir / "phase151_real_l2_duckdb_query_benchmark_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Benchmark Partitions": partitions,
            "Query Timing Ledger": queries,
            "Query Results": results,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase151_real_l2_duckdb_query_benchmark",
        **reproducibility_fields(
            artifact_id="phase151",
            generated_utc=generated_utc,
            inputs={"real_panel_root": str(real_panel_root), "duckdb_catalog": str(db_path)},
            parameters={
                "symbols": symbols,
                "exchange": exchange,
                "scan_policy": "partition_scoped_no_full_panel_tick_scan",
                "strategy_replay_policy": "closed",
            },
            outputs={
                "benchmark_partitions": str(output_dir / "phase151_benchmark_partitions.csv"),
                "query_timing_ledger": str(output_dir / "phase151_query_timing_ledger.csv"),
                "query_results": str(output_dir / "phase151_query_results.csv"),
                "acceptance_summary": str(output_dir / "phase151_real_l2_duckdb_query_benchmark_acceptance_summary.csv"),
                "report": str(output_dir / "phase151_real_l2_duckdb_query_benchmark_report.md"),
                "manifest": str(output_dir / "phase151_real_l2_duckdb_query_benchmark_manifest.json"),
            },
            random_seed="none_deterministic_query_benchmark",
            scenario_ids="phase151_real_l2_duckdb_query_benchmark",
            cost_model_version="not_applicable",
            latency_model_version="not_applicable",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase151_real_l2_duckdb_query_benchmark_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run bounded local DuckDB query benchmark over real L2 Parquet.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--real-panel-root", type=Path, default=DEFAULT_REAL_PANEL_ROOT)
    parser.add_argument("--db-path", type=Path, default=DEFAULT_CATALOG_DB)
    parser.add_argument("--symbols", nargs="+", default=DEFAULT_SYMBOLS)
    parser.add_argument("--exchange", default=DEFAULT_EXCHANGE)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase151(args.output_dir, args.base_dir, args.real_panel_root, args.db_path, args.symbols, args.exchange)


if __name__ == "__main__":
    main()
