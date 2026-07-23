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


DEFAULT_OUTPUT_DIR = Path("outputs/phase154")
DEFAULT_REAL_PANEL_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_CATALOG_DB = Path("outputs/phase150/real_l2_catalog.duckdb")
DEFAULT_PHASE106_DIR = Path("outputs/phase106")
DEFAULT_EXCHANGE = "NSE"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def quote_sql(value: str) -> str:
    return value.replace("'", "''")


def partition_glob(root: Path, trade_date: str, exchange: str, symbol: str) -> str:
    return (root / f"trade_date={trade_date}" / f"exchange={exchange}" / f"symbol={symbol}" / "*.parquet").as_posix()


def select_partitions(
    con: duckdb.DuckDBPyConnection,
    exchange: str,
    symbols: list[str] | None,
    trade_dates: list[str] | None,
    latest_date_only: bool,
    max_partitions: int,
) -> pd.DataFrame:
    frame = con.execute(
        """
        SELECT trade_date, exchange, symbol, parquet_files, bytes
        FROM real_l2_date_symbol_summary
        WHERE exchange = ?
        ORDER BY trade_date, symbol
        """,
        [exchange],
    ).fetchdf()
    if latest_date_only and not trade_dates and not frame.empty:
        trade_dates = [str(frame["trade_date"].max())]
    if trade_dates:
        wanted_dates = {str(date) for date in trade_dates}
        frame = frame[frame["trade_date"].astype(str).isin(wanted_dates)].copy()
    if symbols:
        wanted = {symbol.upper() for symbol in symbols}
        frame = frame[frame["symbol"].astype(str).str.upper().isin(wanted)].copy()
    if max_partitions > 0:
        frame = frame.head(max_partitions).copy()
    return frame.reset_index(drop=True)


def profile_partition(con: duckdb.DuckDBPyConnection, root: Path, row: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    trade_date = str(row["trade_date"])
    exchange = str(row["exchange"])
    symbol = str(row["symbol"])
    glob = quote_sql(partition_glob(root, trade_date, exchange, symbol))
    sql = f"""
    WITH ordered AS (
        SELECT
            collector_received_utc_ms,
            collector_received_utc_ms - lag(collector_received_utc_ms) OVER (ORDER BY collector_received_utc_ms) AS gap_ms
        FROM parquet_scan('{glob}', union_by_name=true)
        WHERE collector_received_utc_ms IS NOT NULL
    ),
    gaps AS (
        SELECT * FROM ordered WHERE gap_ms IS NOT NULL
    )
    SELECT
        count(*) AS rows,
        (SELECT count(*) FROM gaps) AS gap_rows,
        min(collector_received_utc_ms) AS min_received_ms,
        max(collector_received_utc_ms) AS max_received_ms,
        (max(collector_received_utc_ms) - min(collector_received_utc_ms)) / 1000.0 AS observed_seconds,
        count(*) / NULLIF(((max(collector_received_utc_ms) - min(collector_received_utc_ms)) / 1000.0), 0) AS ticks_per_second,
        median(gap_ms) FILTER (WHERE gap_ms IS NOT NULL) AS median_gap_ms,
        quantile_cont(gap_ms, 0.75) FILTER (WHERE gap_ms IS NOT NULL) AS p75_gap_ms,
        quantile_cont(gap_ms, 0.90) FILTER (WHERE gap_ms IS NOT NULL) AS p90_gap_ms,
        quantile_cont(gap_ms, 0.95) FILTER (WHERE gap_ms IS NOT NULL) AS p95_gap_ms,
        quantile_cont(gap_ms, 0.99) FILTER (WHERE gap_ms IS NOT NULL) AS p99_gap_ms,
        avg(CASE WHEN gap_ms <= 100 THEN 1 ELSE 0 END) FILTER (WHERE gap_ms IS NOT NULL) AS gap_le_100ms_fraction,
        avg(CASE WHEN gap_ms <= 500 THEN 1 ELSE 0 END) FILTER (WHERE gap_ms IS NOT NULL) AS gap_le_500ms_fraction,
        avg(CASE WHEN gap_ms <= 1000 THEN 1 ELSE 0 END) FILTER (WHERE gap_ms IS NOT NULL) AS gap_le_1s_fraction,
        avg(CASE WHEN gap_ms > 5000 THEN 1 ELSE 0 END) FILTER (WHERE gap_ms IS NOT NULL) AS gap_gt_5s_fraction,
        max(gap_ms) FILTER (WHERE gap_ms IS NOT NULL) AS max_gap_ms
    FROM ordered
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


def build_profiles(
    root: Path,
    db_path: Path,
    exchange: str,
    symbols: list[str] | None,
    trade_dates: list[str] | None,
    latest_date_only: bool,
    max_partitions: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        partitions = select_partitions(con, exchange, symbols, trade_dates, latest_date_only, max_partitions)
        profiles: list[dict[str, Any]] = []
        timings: list[dict[str, Any]] = []
        for row in partitions.to_dict("records"):
            profile, timing = profile_partition(con, root, row)
            profiles.append(profile)
            timings.append(timing)
        return partitions, pd.DataFrame(profiles), pd.DataFrame(timings)
    finally:
        con.close()


def aggregate_symbol_profiles(profiles: pd.DataFrame) -> pd.DataFrame:
    if profiles.empty:
        return pd.DataFrame()
    numeric = profiles.copy()
    metric_cols = [
        "rows",
        "gap_rows",
        "observed_seconds",
        "ticks_per_second",
        "median_gap_ms",
        "p75_gap_ms",
        "p90_gap_ms",
        "p95_gap_ms",
        "p99_gap_ms",
        "gap_le_100ms_fraction",
        "gap_le_500ms_fraction",
        "gap_le_1s_fraction",
        "gap_gt_5s_fraction",
        "max_gap_ms",
    ]
    for column in metric_cols:
        numeric[column] = pd.to_numeric(numeric[column], errors="coerce")
    return (
        numeric.groupby(["exchange", "symbol"], sort=True)
        .agg(
            trade_dates=("trade_date", "nunique"),
            rows=("rows", "sum"),
            gap_rows=("gap_rows", "sum"),
            median_ticks_per_second=("ticks_per_second", "median"),
            min_ticks_per_second=("ticks_per_second", "min"),
            max_ticks_per_second=("ticks_per_second", "max"),
            median_gap_ms=("median_gap_ms", "median"),
            median_p95_gap_ms=("p95_gap_ms", "median"),
            max_p95_gap_ms=("p95_gap_ms", "max"),
            median_gap_le_1s_fraction=("gap_le_1s_fraction", "median"),
            max_gap_gt_5s_fraction=("gap_gt_5s_fraction", "max"),
        )
        .reset_index()
    )


def aggregate_date_profiles(profiles: pd.DataFrame) -> pd.DataFrame:
    if profiles.empty:
        return pd.DataFrame()
    numeric = profiles.copy()
    for column in ["rows", "ticks_per_second", "median_gap_ms", "p95_gap_ms", "gap_le_1s_fraction", "gap_gt_5s_fraction"]:
        numeric[column] = pd.to_numeric(numeric[column], errors="coerce")
    return (
        numeric.groupby(["trade_date", "exchange"], sort=True)
        .agg(
            symbols=("symbol", "nunique"),
            rows=("rows", "sum"),
            median_symbol_ticks_per_second=("ticks_per_second", "median"),
            min_symbol_ticks_per_second=("ticks_per_second", "min"),
            max_symbol_ticks_per_second=("ticks_per_second", "max"),
            median_symbol_gap_ms=("median_gap_ms", "median"),
            max_symbol_p95_gap_ms=("p95_gap_ms", "max"),
            median_gap_le_1s_fraction=("gap_le_1s_fraction", "median"),
            max_gap_gt_5s_fraction=("gap_gt_5s_fraction", "max"),
        )
        .reset_index()
    )


def compare_to_phase106_sampled(profiles: pd.DataFrame, phase106_dir: Path) -> pd.DataFrame:
    sampled = read_csv(phase106_dir / "real_anchor_profile.csv")
    if profiles.empty or sampled.empty:
        return pd.DataFrame()
    sampled = sampled[["symbol", "trade_date", "median_gap_ms", "p90_gap_ms", "p95_gap_ms", "gap_le_1s_fraction"]].copy()
    profiles_subset = profiles[["symbol", "trade_date", "median_gap_ms", "p90_gap_ms", "p95_gap_ms", "gap_le_1s_fraction"]].copy()
    merged = profiles_subset.merge(sampled, on=["symbol", "trade_date"], how="inner", suffixes=("_phase154_full_partition", "_phase106_sampled_files"))
    rows: list[dict[str, Any]] = []
    for item in merged.to_dict("records"):
        for metric in ["median_gap_ms", "p90_gap_ms", "p95_gap_ms", "gap_le_1s_fraction"]:
            full_value = pd.to_numeric(pd.Series([item.get(f"{metric}_phase154_full_partition")]), errors="coerce").iloc[0]
            sampled_value = pd.to_numeric(pd.Series([item.get(f"{metric}_phase106_sampled_files")]), errors="coerce").iloc[0]
            ratio = float(sampled_value) / float(full_value) if pd.notna(full_value) and pd.notna(sampled_value) and float(full_value) != 0.0 else float("nan")
            if pd.isna(ratio):
                flag = "missing"
            elif ratio < 0.50:
                flag = "sampled_low_vs_full"
            elif ratio > 2.00:
                flag = "sampled_high_vs_full"
            else:
                flag = "within_band"
            rows.append(
                {
                    "symbol": item["symbol"],
                    "trade_date": item["trade_date"],
                    "metric": metric,
                    "phase154_full_partition_value": full_value,
                    "phase106_sampled_files_value": sampled_value,
                    "sampled_to_full_ratio": ratio,
                    "sample_bias_flag": flag,
                }
            )
    return pd.DataFrame(rows)


def summarize(
    partitions: pd.DataFrame,
    profiles: pd.DataFrame,
    timings: pd.DataFrame,
    symbol_profiles: pd.DataFrame,
    sample_compare: pd.DataFrame,
    db_path: Path,
) -> pd.DataFrame:
    failures = int((timings["status"].astype(str) != "completed").sum()) if not timings.empty else 1
    total_elapsed = float(pd.to_numeric(timings["elapsed_seconds"], errors="coerce").fillna(0.0).sum()) if not timings.empty else 0.0
    max_elapsed = float(pd.to_numeric(timings["elapsed_seconds"], errors="coerce").fillna(0.0).max()) if not timings.empty else 0.0
    median_symbol_p95 = float(pd.to_numeric(symbol_profiles["median_p95_gap_ms"], errors="coerce").median()) if not symbol_profiles.empty else 0.0
    max_symbol_p95 = float(pd.to_numeric(symbol_profiles["max_p95_gap_ms"], errors="coerce").max()) if not symbol_profiles.empty else 0.0
    median_tick_rate = float(pd.to_numeric(symbol_profiles["median_ticks_per_second"], errors="coerce").median()) if not symbol_profiles.empty else 0.0
    sample_bias_flags = int(sample_compare["sample_bias_flag"].astype(str).ne("within_band").sum()) if not sample_compare.empty else 0
    return pd.DataFrame(
        [
            ("phase154_catalog_db_exists", int(db_path.exists()), "Phase150 DuckDB catalog database exists locally"),
            ("phase154_partitions_selected", int(len(partitions)), "Date/symbol partitions selected for full-partition cadence profiling"),
            ("phase154_partition_profiles_completed", int(len(profiles) - failures), "Partition cadence profiles completed"),
            ("phase154_failed_partition_profiles", failures, "Partition cadence profiles failed"),
            ("phase154_trade_dates_profiled", int(profiles["trade_date"].nunique()) if not profiles.empty else 0, "Trade dates profiled"),
            ("phase154_symbols_profiled", int(profiles["symbol"].nunique()) if not profiles.empty else 0, "Symbols profiled"),
            ("phase154_total_rows_profiled", int(pd.to_numeric(profiles["rows"], errors="coerce").fillna(0).sum()) if not profiles.empty else 0, "Tick/update rows profiled"),
            ("phase154_total_elapsed_seconds", total_elapsed, "Total elapsed seconds across partition cadence profiles"),
            ("phase154_max_partition_elapsed_seconds", max_elapsed, "Slowest partition cadence profile elapsed seconds"),
            ("phase154_median_symbol_ticks_per_second", median_tick_rate, "Median symbol-level tick/update rate across full partitions"),
            ("phase154_median_symbol_p95_gap_ms", median_symbol_p95, "Median symbol-level p95 inter-update gap"),
            ("phase154_max_symbol_p95_gap_ms", max_symbol_p95, "Maximum symbol-level p95 inter-update gap"),
            ("phase154_sample_bias_flag_rows", sample_bias_flags, "Phase106 sampled-file cadence rows outside sampled/full comparison bands"),
            ("phase154_strategy_replay_allowed", 0, "Cadence anchor profiling does not unlock strategy replay"),
            ("phase154_next_best_action", "use_phase154_full_partition_cadence_anchors_for_generator_calibration_contract", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase154 Full-partition Real Cadence Anchor",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase154 recomputes real-anchor received-cadence profiles from full local Parquet partitions using DuckDB.",
        "It replaces sampled-file cadence anchors for calibration diagnostics. It does not contact Azure, generate signals, compute fills, run P&L, or unlock strategy replay.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase154_full_partition_real_cadence_anchor_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase154(
    output_dir: Path,
    base_dir: Path,
    real_panel_root: Path,
    db_path: Path,
    phase106_dir: Path,
    exchange: str,
    symbols: list[str] | None,
    trade_dates: list[str] | None,
    latest_date_only: bool,
    max_partitions: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    partitions, profiles, timings = build_profiles(real_panel_root, db_path, exchange, symbols, trade_dates, latest_date_only, max_partitions)
    symbol_profiles = aggregate_symbol_profiles(profiles)
    date_profiles = aggregate_date_profiles(profiles)
    sample_compare = compare_to_phase106_sampled(profiles, phase106_dir)
    acceptance = summarize(partitions, profiles, timings, symbol_profiles, sample_compare, db_path)

    partitions.to_csv(output_dir / "phase154_profile_partitions.csv", index=False)
    profiles.to_csv(output_dir / "phase154_partition_cadence_profiles.csv", index=False)
    timings.to_csv(output_dir / "phase154_profile_timing_ledger.csv", index=False)
    symbol_profiles.to_csv(output_dir / "phase154_symbol_cadence_anchor.csv", index=False)
    date_profiles.to_csv(output_dir / "phase154_date_cadence_anchor.csv", index=False)
    sample_compare.to_csv(output_dir / "phase154_phase106_sample_bias_audit.csv", index=False)
    acceptance.to_csv(output_dir / "phase154_full_partition_real_cadence_anchor_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Date Cadence Anchor": date_profiles,
            "Symbol Cadence Anchor": symbol_profiles,
            "Phase106 Sample Bias Audit": sample_compare.head(80),
            "Profile Timing Ledger": timings,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase154_full_partition_real_cadence_anchor",
        **reproducibility_fields(
            artifact_id="phase154",
            generated_utc=generated_utc,
            inputs={
                "real_panel_root": str(real_panel_root),
                "duckdb_catalog": str(db_path),
                "phase106_real_anchor_profile": str(phase106_dir / "real_anchor_profile.csv"),
            },
            parameters={
                "exchange": exchange,
                "symbols": symbols or "all_cataloged_symbols",
                "trade_dates": trade_dates or ("latest_cataloged_trade_date_only" if latest_date_only else "all_cataloged_trade_dates"),
                "max_partitions": max_partitions,
                "scan_policy": "full_partition_cadence_columns_only",
                "strategy_replay_policy": "closed",
            },
            outputs={
                "profile_partitions": str(output_dir / "phase154_profile_partitions.csv"),
                "partition_cadence_profiles": str(output_dir / "phase154_partition_cadence_profiles.csv"),
                "profile_timing_ledger": str(output_dir / "phase154_profile_timing_ledger.csv"),
                "symbol_cadence_anchor": str(output_dir / "phase154_symbol_cadence_anchor.csv"),
                "date_cadence_anchor": str(output_dir / "phase154_date_cadence_anchor.csv"),
                "phase106_sample_bias_audit": str(output_dir / "phase154_phase106_sample_bias_audit.csv"),
                "acceptance_summary": str(output_dir / "phase154_full_partition_real_cadence_anchor_acceptance_summary.csv"),
                "report": str(output_dir / "phase154_full_partition_real_cadence_anchor_report.md"),
                "manifest": str(output_dir / "phase154_full_partition_real_cadence_anchor_manifest.json"),
            },
            random_seed="none_deterministic_full_partition_cadence",
            scenario_ids="phase154_full_partition_real_cadence_anchor",
            cost_model_version="not_applicable",
            latency_model_version="not_applicable",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase154_full_partition_real_cadence_anchor_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build full-partition real cadence anchors from local DuckDB/Parquet.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--real-panel-root", type=Path, default=DEFAULT_REAL_PANEL_ROOT)
    parser.add_argument("--db-path", type=Path, default=DEFAULT_CATALOG_DB)
    parser.add_argument("--phase106-dir", type=Path, default=DEFAULT_PHASE106_DIR)
    parser.add_argument("--exchange", default=DEFAULT_EXCHANGE)
    parser.add_argument("--symbols", nargs="*", default=None)
    parser.add_argument("--trade-dates", nargs="*", default=None)
    parser.add_argument("--all-dates", action="store_true", help="Profile all cataloged dates instead of only the latest cataloged date.")
    parser.add_argument("--max-partitions", type=int, default=0, help="0 means all selected catalog partitions.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase154(
        output_dir=args.output_dir,
        base_dir=args.base_dir,
        real_panel_root=args.real_panel_root,
        db_path=args.db_path,
        phase106_dir=args.phase106_dir,
        exchange=args.exchange,
        symbols=args.symbols,
        trade_dates=args.trade_dates,
        latest_date_only=not args.all_dates,
        max_partitions=args.max_partitions,
    )


if __name__ == "__main__":
    main()
