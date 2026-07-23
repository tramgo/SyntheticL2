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


DEFAULT_OUTPUT_DIR = Path("outputs/phase152")
DEFAULT_REAL_PANEL_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_CATALOG_DB = Path("outputs/phase150/real_l2_catalog.duckdb")
DEFAULT_PHASE151_DIR = Path("outputs/phase151")
DEFAULT_EXCHANGE = "NSE"
DEFAULT_TOP_BYTE_PARTITIONS = 4


def quote_sql(value: str) -> str:
    return value.replace("'", "''")


def partition_glob(root: Path, trade_date: str, exchange: str, symbol: str) -> str:
    return (root / f"trade_date={trade_date}" / f"exchange={exchange}" / f"symbol={symbol}" / "*.parquet").as_posix()


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def choose_partitions(con: duckdb.DuckDBPyConnection, phase151_dir: Path, exchange: str, top_n: int) -> pd.DataFrame:
    prior = read_csv(phase151_dir / "phase151_benchmark_partitions.csv")
    if not prior.empty:
        prior = prior[["trade_date", "exchange", "symbol", "parquet_files", "bytes"]].copy()
        prior["selection_reason"] = "phase151_benchmark_partition"
    top = con.execute(
        """
        SELECT trade_date, exchange, symbol, parquet_files, bytes
        FROM real_l2_date_symbol_summary
        WHERE exchange = ?
        ORDER BY bytes DESC, trade_date, symbol
        LIMIT ?
        """,
        [exchange, top_n],
    ).fetchdf()
    if not top.empty:
        top["selection_reason"] = "top_byte_partition_from_phase150_catalog"
    selected = pd.concat([prior, top], ignore_index=True) if not prior.empty else top
    if selected.empty:
        return pd.DataFrame(columns=["trade_date", "exchange", "symbol", "parquet_files", "bytes", "selection_reason"])
    return selected.drop_duplicates(["trade_date", "exchange", "symbol"], keep="first").sort_values(["trade_date", "symbol"]).reset_index(drop=True)


def profile_partition(con: duckdb.DuckDBPyConnection, root: Path, row: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    trade_date = str(row["trade_date"])
    exchange = str(row["exchange"])
    symbol = str(row["symbol"])
    glob = quote_sql(partition_glob(root, trade_date, exchange, symbol))
    sql = f"""
    WITH ticks AS (
        SELECT
            collector_received_utc_ms,
            last_price,
            buy_1_price,
            buy_1_quantity,
            sell_1_price,
            sell_1_quantity,
            buy_5_quantity,
            sell_5_quantity,
            collector_received_utc_ms - lag(collector_received_utc_ms) OVER (ORDER BY collector_received_utc_ms) AS gap_ms
        FROM parquet_scan('{glob}', union_by_name=true)
        WHERE collector_received_utc_ms IS NOT NULL
    )
    SELECT
        count(*) AS rows,
        min(collector_received_utc_ms) AS min_received_ms,
        max(collector_received_utc_ms) AS max_received_ms,
        (max(collector_received_utc_ms) - min(collector_received_utc_ms)) / 1000.0 AS observed_seconds,
        count(*) / NULLIF(((max(collector_received_utc_ms) - min(collector_received_utc_ms)) / 1000.0), 0) AS ticks_per_second,
        median(gap_ms) AS median_gap_ms,
        quantile_cont(gap_ms, 0.90) AS p90_gap_ms,
        quantile_cont(gap_ms, 0.95) AS p95_gap_ms,
        avg(CASE WHEN gap_ms <= 100 THEN 1 ELSE 0 END) AS gap_le_100ms_fraction,
        avg(CASE WHEN gap_ms <= 500 THEN 1 ELSE 0 END) AS gap_le_500ms_fraction,
        avg(CASE WHEN gap_ms <= 1000 THEN 1 ELSE 0 END) AS gap_le_1s_fraction,
        avg(CASE WHEN gap_ms > 5000 THEN 1 ELSE 0 END) AS gap_gt_5s_fraction,
        min(last_price) AS min_last_price,
        max(last_price) AS max_last_price,
        avg(sell_1_price - buy_1_price) AS avg_l1_spread_abs,
        median(sell_1_price - buy_1_price) AS median_l1_spread_abs,
        avg(CASE WHEN buy_1_price > 0 AND sell_1_price >= buy_1_price THEN 1 ELSE 0 END) AS l1_book_valid_fraction,
        avg(CASE WHEN buy_5_quantity > 0 OR sell_5_quantity > 0 THEN 1 ELSE 0 END) AS depth_level_5_present_fraction,
        avg(buy_1_quantity) AS avg_best_bid_qty,
        avg(sell_1_quantity) AS avg_best_ask_qty
    FROM ticks
    """
    started = time.perf_counter()
    status = "completed"
    error = ""
    try:
        result = con.execute(sql).fetchdf().iloc[0].to_dict()
    except Exception as exc:
        result = {}
        status = "failed"
        error = repr(exc)
    elapsed = time.perf_counter() - started
    profile = {
        "trade_date": trade_date,
        "exchange": exchange,
        "symbol": symbol,
        "selection_reason": row.get("selection_reason", ""),
        "parquet_files": int(row.get("parquet_files", 0)),
        "bytes": int(row.get("bytes", 0)),
        **result,
    }
    timing = {
        "trade_date": trade_date,
        "exchange": exchange,
        "symbol": symbol,
        "status": status,
        "elapsed_seconds": elapsed,
        "error": error,
    }
    return profile, timing


def run_profiles(root: Path, db_path: Path, phase151_dir: Path, exchange: str, top_n: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        partitions = choose_partitions(con, phase151_dir, exchange, top_n)
        profiles: list[dict[str, Any]] = []
        timings: list[dict[str, Any]] = []
        for row in partitions.to_dict("records"):
            profile, timing = profile_partition(con, root, row)
            profiles.append(profile)
            timings.append(timing)
        return partitions, pd.DataFrame(profiles), pd.DataFrame(timings)
    finally:
        con.close()


def summarize(partitions: pd.DataFrame, profiles: pd.DataFrame, timings: pd.DataFrame, db_path: Path) -> pd.DataFrame:
    failures = int((timings["status"].astype(str) != "completed").sum()) if not timings.empty else 1
    total_elapsed = float(pd.to_numeric(timings["elapsed_seconds"], errors="coerce").fillna(0.0).sum()) if not timings.empty else 0.0
    max_elapsed = float(pd.to_numeric(timings["elapsed_seconds"], errors="coerce").fillna(0.0).max()) if not timings.empty else 0.0
    min_l1_valid = float(pd.to_numeric(profiles["l1_book_valid_fraction"], errors="coerce").dropna().min()) if not profiles.empty else 0.0
    min_l5 = float(pd.to_numeric(profiles["depth_level_5_present_fraction"], errors="coerce").dropna().min()) if not profiles.empty else 0.0
    min_tick_rate = float(pd.to_numeric(profiles["ticks_per_second"], errors="coerce").dropna().min()) if not profiles.empty else 0.0
    max_p95_gap = float(pd.to_numeric(profiles["p95_gap_ms"], errors="coerce").dropna().max()) if not profiles.empty else 0.0
    return pd.DataFrame(
        [
            ("phase152_catalog_db_exists", int(db_path.exists()), "Phase150 DuckDB catalog database exists locally"),
            ("phase152_profile_partitions", int(len(partitions)), "Bounded date/symbol partitions profiled"),
            ("phase152_failed_partition_profiles", failures, "Partition profile queries failed"),
            ("phase152_total_profile_elapsed_seconds", total_elapsed, "Total elapsed seconds across profile queries"),
            ("phase152_max_profile_elapsed_seconds", max_elapsed, "Slowest bounded profile query elapsed seconds"),
            ("phase152_min_ticks_per_second", min_tick_rate, "Minimum observed tick/update rate among profiled partitions"),
            ("phase152_max_p95_gap_ms", max_p95_gap, "Maximum p95 inter-update gap among profiled partitions"),
            ("phase152_min_l1_book_valid_fraction", min_l1_valid, "Minimum valid L1 book fraction among profiled partitions"),
            ("phase152_min_depth_level_5_present_fraction", min_l5, "Minimum visible level-5 presence among profiled partitions"),
            ("phase152_strategy_replay_allowed", 0, "Microstructure profiling does not unlock strategy replay"),
            ("phase152_next_best_action", "use_profiles_for_real_anchor_diagnostics_after_phase148_downloads_not_strategy_replay", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase152 Real L2 Microstructure Profile",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase152 profiles bounded local real L2 partitions for update cadence, tick gaps, L1 spread sanity, and visible depth-level-5 presence.",
        "It is diagnostics-only: no signals, no order-arrival stream, no fills, no P&L, no Azure I/O, and no replay unlock.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase152_real_l2_microstructure_profile_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase152(output_dir: Path, base_dir: Path, real_panel_root: Path, db_path: Path, phase151_dir: Path, exchange: str, top_n: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    partitions, profiles, timings = run_profiles(real_panel_root, db_path, phase151_dir, exchange, top_n)
    acceptance = summarize(partitions, profiles, timings, db_path)
    partitions.to_csv(output_dir / "phase152_profile_partitions.csv", index=False)
    profiles.to_csv(output_dir / "phase152_microstructure_profiles.csv", index=False)
    timings.to_csv(output_dir / "phase152_profile_timing_ledger.csv", index=False)
    acceptance.to_csv(output_dir / "phase152_real_l2_microstructure_profile_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Profile Partitions": partitions,
            "Microstructure Profiles": profiles,
            "Profile Timing Ledger": timings,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase152_real_l2_microstructure_profile",
        **reproducibility_fields(
            artifact_id="phase152",
            generated_utc=generated_utc,
            inputs={
                "real_panel_root": str(real_panel_root),
                "duckdb_catalog": str(db_path),
                "phase151_partitions": str(phase151_dir / "phase151_benchmark_partitions.csv"),
            },
            parameters={
                "exchange": exchange,
                "top_byte_partitions": top_n,
                "scan_policy": "bounded_partition_scoped_profile",
                "strategy_replay_policy": "closed",
            },
            outputs={
                "profile_partitions": str(output_dir / "phase152_profile_partitions.csv"),
                "microstructure_profiles": str(output_dir / "phase152_microstructure_profiles.csv"),
                "profile_timing_ledger": str(output_dir / "phase152_profile_timing_ledger.csv"),
                "acceptance_summary": str(output_dir / "phase152_real_l2_microstructure_profile_acceptance_summary.csv"),
                "report": str(output_dir / "phase152_real_l2_microstructure_profile_report.md"),
                "manifest": str(output_dir / "phase152_real_l2_microstructure_profile_manifest.json"),
            },
            random_seed="none_deterministic_microstructure_profile",
            scenario_ids="phase152_real_l2_microstructure_profile",
            cost_model_version="not_applicable",
            latency_model_version="not_applicable",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase152_real_l2_microstructure_profile_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Profile bounded real L2 partitions with DuckDB.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--real-panel-root", type=Path, default=DEFAULT_REAL_PANEL_ROOT)
    parser.add_argument("--db-path", type=Path, default=DEFAULT_CATALOG_DB)
    parser.add_argument("--phase151-dir", type=Path, default=DEFAULT_PHASE151_DIR)
    parser.add_argument("--exchange", default=DEFAULT_EXCHANGE)
    parser.add_argument("--top-byte-partitions", type=int, default=DEFAULT_TOP_BYTE_PARTITIONS)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase152(
        output_dir=args.output_dir,
        base_dir=args.base_dir,
        real_panel_root=args.real_panel_root,
        db_path=args.db_path,
        phase151_dir=args.phase151_dir,
        exchange=args.exchange,
        top_n=args.top_byte_partitions,
    )


if __name__ == "__main__":
    main()
