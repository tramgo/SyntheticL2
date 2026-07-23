from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase95_real_anchor_panel_contract import EXPECTED_SYMBOLS
from synthetic_l2.phase96_real_anchor_panel_builder import REQUIRED_ZERODHA_L2_COLUMNS
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_REAL_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_PHASE171_DIR = Path("outputs/phase171")
DEFAULT_OUTPUT_DIR = Path("outputs/phase172")
DEFAULT_EXCHANGE = "NSE"
DEFAULT_MIN_READY_DAYS = 5
RECEIVE_TS_COL = "collector_received_utc"
RECEIVE_MS_COL = "collector_received_utc_ms"
SYMBOL_COL = "tradingsymbol"
TRADE_DATE_COL = "trade_date"
L1_STATE_COLUMNS = ["buy_1_price", "buy_1_quantity", "sell_1_price", "sell_1_quantity"]
DEPTH_QTY_COLUMNS = [f"{side}_{level}_quantity" for side in ("buy", "sell") for level in range(1, 6)]
DEPTH_PRICE_COLUMNS = [f"{side}_{level}_price" for side in ("buy", "sell") for level in range(1, 6)]
REQUIRED_RECEIVE_FLOW_COLUMNS = [
    RECEIVE_TS_COL,
    RECEIVE_MS_COL,
    TRADE_DATE_COL,
    "exchange",
    SYMBOL_COL,
    "last_price",
    "last_traded_quantity",
    "volume_traded",
    *DEPTH_PRICE_COLUMNS,
    *DEPTH_QTY_COLUMNS,
]


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = "") -> Any:
    if frame.empty or "metric" not in frame.columns or "value" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def discover_trade_dates(real_root: Path) -> list[str]:
    if not real_root.exists():
        return []
    dates: list[str] = []
    for path in sorted(real_root.glob("trade_date=*")):
        if path.is_dir():
            dates.append(path.name.split("=", 1)[1])
    return dates


def symbol_dir(real_root: Path, trade_date: str, exchange: str, symbol: str) -> Path:
    return real_root / f"trade_date={trade_date}" / f"exchange={exchange}" / f"symbol={symbol}"


def parse_receive_ts(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce", utc=True)


def session_filter(receive_ts: pd.Series) -> pd.Series:
    ist = receive_ts.dt.tz_convert("Asia/Kolkata")
    minutes = ist.dt.hour * 60 + ist.dt.minute
    return minutes.between(9 * 60 + 15, 15 * 60 + 30, inclusive="both")


def inspect_symbol_day(real_root: Path, trade_date: str, exchange: str, symbol: str) -> tuple[dict[str, Any], pd.DataFrame]:
    path = symbol_dir(real_root, trade_date, exchange, symbol)
    files = sorted(path.glob("*.parquet")) if path.exists() else []
    base_row: dict[str, Any] = {
        "trade_date": trade_date,
        "exchange": exchange,
        "symbol": symbol,
        "symbol_dir": str(path),
        "symbol_dir_exists": path.exists(),
        "parquet_files": int(len(files)),
        "bytes": int(sum(item.stat().st_size for item in files)),
        "rows": 0,
        "read_status": "missing" if not files else "ok",
        "read_error": "",
        "schema_pass": False,
        "missing_receive_flow_columns": "|".join(REQUIRED_RECEIVE_FLOW_COLUMNS),
        "first_receive_utc": "",
        "last_receive_utc": "",
        "session_rows": 0,
        "session_seconds": 0.0,
        "session_tick_rate_per_sec": 0.0,
        "median_gap_sec": "",
        "p90_gap_sec": "",
        "p95_gap_sec": "",
        "gaps_le_100ms": 0,
        "gaps_le_500ms": 0,
        "gaps_le_1s": 0,
        "gaps_gt_5s": 0,
        "duplicate_receive_ms": 0,
        "receive_ms_monotonic_violations": 0,
        "l1_state_change_rows": 0,
        "l1_state_change_fraction": 0.0,
        "depth_qty_change_rows": 0,
        "depth_qty_change_fraction": 0.0,
        "active_1s_buckets": 0,
        "receive_flow_feature_ready": False,
    }
    if not files:
        return base_row, pd.DataFrame(columns=["trade_date", "symbol", "bucket_1s"])
    frames: list[pd.DataFrame] = []
    needed = sorted(set(REQUIRED_RECEIVE_FLOW_COLUMNS + ["collector_received_monotonic_ns"]))
    try:
        for file in files:
            frame = pd.read_parquet(file)
            frames.append(frame[[col for col in needed if col in frame.columns]].copy())
    except Exception as exc:
        base_row.update({"read_status": "failed", "read_error": repr(exc)})
        return base_row, pd.DataFrame(columns=["trade_date", "symbol", "bucket_1s"])
    if not frames:
        return base_row, pd.DataFrame(columns=["trade_date", "symbol", "bucket_1s"])
    data = pd.concat(frames, ignore_index=True)
    missing = sorted(set(REQUIRED_RECEIVE_FLOW_COLUMNS).difference(data.columns))
    receive_ts = parse_receive_ts(data[RECEIVE_TS_COL]) if RECEIVE_TS_COL in data.columns else pd.Series(pd.NaT, index=data.index, dtype="datetime64[ns, UTC]")
    if RECEIVE_MS_COL in data.columns:
        order_cols = [RECEIVE_MS_COL]
        if "collector_received_monotonic_ns" in data.columns:
            order_cols.append("collector_received_monotonic_ns")
        data = data.assign(_receive_ts=receive_ts).sort_values(order_cols, kind="mergesort").reset_index(drop=True)
        receive_ts = data["_receive_ts"]
    else:
        data = data.assign(_receive_ts=receive_ts).sort_values("_receive_ts", kind="mergesort").reset_index(drop=True)
        receive_ts = data["_receive_ts"]
    valid_ts = receive_ts.dropna()
    session_mask = session_filter(receive_ts) if not receive_ts.empty else pd.Series(False, index=data.index)
    session_ts = receive_ts.loc[session_mask].dropna()
    gaps = session_ts.sort_values().diff().dt.total_seconds().dropna()
    session_seconds = float((session_ts.max() - session_ts.min()).total_seconds()) if len(session_ts) >= 2 else 0.0
    l1_change = pd.Series(False, index=data.index)
    if all(col in data.columns for col in L1_STATE_COLUMNS):
        l1_change = data[L1_STATE_COLUMNS].ne(data[L1_STATE_COLUMNS].shift(1)).any(axis=1)
    depth_change = pd.Series(False, index=data.index)
    available_depth_qty_cols = [col for col in DEPTH_QTY_COLUMNS if col in data.columns]
    if available_depth_qty_cols:
        depth_change = data[available_depth_qty_cols].ne(data[available_depth_qty_cols].shift(1)).any(axis=1)
    active = data.loc[session_mask, ["_receive_ts"]].dropna()
    buckets = pd.DataFrame(columns=["trade_date", "symbol", "bucket_1s"])
    if not active.empty:
        buckets = pd.DataFrame(
            {
                "trade_date": trade_date,
                "symbol": symbol,
                "bucket_1s": active["_receive_ts"].dt.floor("1s").astype(str),
            }
        ).drop_duplicates()
    if RECEIVE_MS_COL in data.columns:
        receive_ms = pd.to_numeric(data[RECEIVE_MS_COL], errors="coerce")
        duplicate_ms = int(receive_ms.duplicated().sum())
        monotonic_violations = int(receive_ms.diff().dropna().lt(0).sum())
    else:
        duplicate_ms = 0
        monotonic_violations = 0
    rows = int(len(data))
    session_rows = int(session_mask.sum())
    base_row.update(
        {
            "rows": rows,
            "schema_pass": bool(not missing),
            "missing_receive_flow_columns": "|".join(missing),
            "first_receive_utc": valid_ts.min().isoformat() if not valid_ts.empty else "",
            "last_receive_utc": valid_ts.max().isoformat() if not valid_ts.empty else "",
            "session_rows": session_rows,
            "session_seconds": session_seconds,
            "session_tick_rate_per_sec": float(session_rows / session_seconds) if session_seconds > 0 else 0.0,
            "median_gap_sec": float(gaps.median()) if not gaps.empty else "",
            "p90_gap_sec": float(gaps.quantile(0.90)) if not gaps.empty else "",
            "p95_gap_sec": float(gaps.quantile(0.95)) if not gaps.empty else "",
            "gaps_le_100ms": int(gaps.le(0.1).sum()) if not gaps.empty else 0,
            "gaps_le_500ms": int(gaps.le(0.5).sum()) if not gaps.empty else 0,
            "gaps_le_1s": int(gaps.le(1.0).sum()) if not gaps.empty else 0,
            "gaps_gt_5s": int(gaps.gt(5.0).sum()) if not gaps.empty else 0,
            "duplicate_receive_ms": duplicate_ms,
            "receive_ms_monotonic_violations": monotonic_violations,
            "l1_state_change_rows": int(l1_change.sum()),
            "l1_state_change_fraction": float(l1_change.sum() / rows) if rows else 0.0,
            "depth_qty_change_rows": int(depth_change.sum()),
            "depth_qty_change_fraction": float(depth_change.sum() / rows) if rows else 0.0,
            "active_1s_buckets": int(len(buckets)),
            "receive_flow_feature_ready": bool(not missing and session_rows > 0 and len(buckets) > 0),
        }
    )
    return base_row, buckets


def build_file_inventory(real_root: Path, trade_dates: list[str], exchange: str) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    required = set(REQUIRED_RECEIVE_FLOW_COLUMNS)
    for trade_date in trade_dates:
        for symbol in sorted(EXPECTED_SYMBOLS):
            path = symbol_dir(real_root, trade_date, exchange, symbol)
            files = sorted(path.glob("*.parquet")) if path.exists() else []
            missing = sorted(required)
            schema_pass = False
            read_status = "missing" if not files else "ok"
            read_error = ""
            if files:
                try:
                    sample = pd.read_parquet(files[0])
                    missing = sorted(required.difference(sample.columns))
                    schema_pass = bool(not missing)
                except Exception as exc:
                    read_status = "failed"
                    read_error = repr(exc)
            rows.append(
                {
                    "trade_date": trade_date,
                    "exchange": exchange,
                    "symbol": symbol,
                    "symbol_dir": str(path),
                    "symbol_dir_exists": path.exists(),
                    "parquet_files": int(len(files)),
                    "bytes": int(sum(item.stat().st_size for item in files)),
                    "read_status": read_status,
                    "read_error": read_error,
                    "schema_pass": schema_pass,
                    "missing_receive_flow_columns": "|".join(missing),
                }
            )
    return pd.DataFrame(rows)


def duckdb_glob(real_root: Path, exchange: str, trade_date: str, symbol: str) -> str:
    return str(real_root / f"trade_date={trade_date}" / f"exchange={exchange}" / f"symbol={symbol}" / "*.parquet").replace("\\", "/")


def build_duckdb_receive_stats(real_root: Path, exchange: str, trade_date: str, symbol: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    import duckdb

    glob = duckdb_glob(real_root, exchange, trade_date, symbol)
    con = duckdb.connect(database=":memory:")
    con.execute("PRAGMA threads=4")
    source_sql = f"""
        SELECT
            trade_date::VARCHAR AS trade_date,
            exchange::VARCHAR AS exchange,
            tradingsymbol::VARCHAR AS symbol,
            collector_received_utc_ms::BIGINT AS receive_ms,
            collector_received_monotonic_ns::BIGINT AS receive_mono_ns,
            hash(buy_1_price, buy_1_quantity, sell_1_price, sell_1_quantity) AS l1_hash,
            hash(
                buy_1_quantity, buy_2_quantity, buy_3_quantity, buy_4_quantity, buy_5_quantity,
                sell_1_quantity, sell_2_quantity, sell_3_quantity, sell_4_quantity, sell_5_quantity
            ) AS depth_qty_hash
        FROM read_parquet('{glob}', hive_partitioning = true, union_by_name = true)
    """
    ordered_sql = f"""
        WITH src AS ({source_sql}),
        ordered AS (
            SELECT
                *,
                lag(receive_ms) OVER (
                    PARTITION BY trade_date, exchange, symbol
                    ORDER BY receive_ms, receive_mono_ns
                ) AS prev_receive_ms,
                lag(l1_hash) OVER (
                    PARTITION BY trade_date, exchange, symbol
                    ORDER BY receive_ms, receive_mono_ns
                ) AS prev_l1_hash,
                lag(depth_qty_hash) OVER (
                    PARTITION BY trade_date, exchange, symbol
                    ORDER BY receive_ms, receive_mono_ns
                ) AS prev_depth_qty_hash,
                ((receive_ms + 19800000) % 86400000) AS ist_ms_of_day
            FROM src
        )
        SELECT
            *,
            ist_ms_of_day BETWEEN 33300000 AND 55800000 AS in_session,
            CASE WHEN prev_receive_ms IS NULL THEN NULL ELSE (receive_ms - prev_receive_ms) / 1000.0 END AS gap_sec,
            prev_l1_hash IS NULL OR l1_hash <> prev_l1_hash AS l1_changed,
            prev_depth_qty_hash IS NULL OR depth_qty_hash <> prev_depth_qty_hash AS depth_qty_changed
        FROM ordered
    """
    con.execute(f"CREATE TEMP TABLE phase172_ordered AS {ordered_sql}")
    stats = con.execute(
        """
        SELECT
            trade_date,
            exchange,
            symbol,
            count(*)::BIGINT AS rows,
            min(receive_ms)::BIGINT AS first_receive_ms,
            max(receive_ms)::BIGINT AS last_receive_ms,
            sum(CASE WHEN in_session THEN 1 ELSE 0 END)::BIGINT AS session_rows,
            (max(CASE WHEN in_session THEN receive_ms ELSE NULL END) - min(CASE WHEN in_session THEN receive_ms ELSE NULL END)) / 1000.0 AS session_seconds,
            quantile_cont(CASE WHEN in_session THEN gap_sec ELSE NULL END, 0.50) AS median_gap_sec,
            quantile_cont(CASE WHEN in_session THEN gap_sec ELSE NULL END, 0.90) AS p90_gap_sec,
            quantile_cont(CASE WHEN in_session THEN gap_sec ELSE NULL END, 0.95) AS p95_gap_sec,
            sum(CASE WHEN in_session AND gap_sec <= 0.1 THEN 1 ELSE 0 END)::BIGINT AS gaps_le_100ms,
            sum(CASE WHEN in_session AND gap_sec <= 0.5 THEN 1 ELSE 0 END)::BIGINT AS gaps_le_500ms,
            sum(CASE WHEN in_session AND gap_sec <= 1.0 THEN 1 ELSE 0 END)::BIGINT AS gaps_le_1s,
            sum(CASE WHEN in_session AND gap_sec > 5.0 THEN 1 ELSE 0 END)::BIGINT AS gaps_gt_5s,
            (count(*) - count(DISTINCT receive_ms))::BIGINT AS duplicate_receive_ms,
            sum(CASE WHEN gap_sec < 0 THEN 1 ELSE 0 END)::BIGINT AS receive_ms_monotonic_violations,
            sum(CASE WHEN l1_changed THEN 1 ELSE 0 END)::BIGINT AS l1_state_change_rows,
            sum(CASE WHEN depth_qty_changed THEN 1 ELSE 0 END)::BIGINT AS depth_qty_change_rows,
            count(DISTINCT CASE WHEN in_session THEN floor(receive_ms / 1000) ELSE NULL END)::BIGINT AS active_1s_buckets
        FROM ordered
        GROUP BY trade_date, exchange, symbol
        ORDER BY trade_date, symbol
        """.replace("FROM ordered", "FROM phase172_ordered")
    ).df()
    buckets = con.execute(
        """
        SELECT DISTINCT
            trade_date,
            symbol,
            floor(receive_ms / 1000)::BIGINT AS bucket_1s
        FROM phase172_ordered
        WHERE in_session
        ORDER BY trade_date, bucket_1s, symbol
        """
    ).df()
    con.close()
    if not stats.empty:
        stats["duckdb_read_status"] = "ok"
        stats["duckdb_read_error"] = ""
        stats["first_receive_utc"] = pd.to_datetime(stats["first_receive_ms"], unit="ms", utc=True).astype(str)
        stats["last_receive_utc"] = pd.to_datetime(stats["last_receive_ms"], unit="ms", utc=True).astype(str)
        stats["session_seconds"] = pd.to_numeric(stats["session_seconds"], errors="coerce").fillna(0.0)
        stats["session_tick_rate_per_sec"] = stats["session_rows"].astype(float) / stats["session_seconds"].where(stats["session_seconds"].gt(0), pd.NA)
        stats["session_tick_rate_per_sec"] = stats["session_tick_rate_per_sec"].fillna(0.0)
        stats["l1_state_change_fraction"] = stats["l1_state_change_rows"].astype(float) / stats["rows"].where(stats["rows"].gt(0), pd.NA)
        stats["depth_qty_change_fraction"] = stats["depth_qty_change_rows"].astype(float) / stats["rows"].where(stats["rows"].gt(0), pd.NA)
        stats["l1_state_change_fraction"] = stats["l1_state_change_fraction"].fillna(0.0)
        stats["depth_qty_change_fraction"] = stats["depth_qty_change_fraction"].fillna(0.0)
    return stats, buckets


def build_symbol_day_audit(real_root: Path, trade_dates: list[str], exchange: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    inventory = build_file_inventory(real_root, trade_dates, exchange)
    empty_buckets = pd.DataFrame(columns=["trade_date", "symbol", "bucket_1s"])
    if inventory.empty or not inventory["parquet_files"].astype(int).gt(0).any():
        return inventory, empty_buckets
    stats_frames: list[pd.DataFrame] = []
    bucket_frames: list[pd.DataFrame] = []
    fallback_rows: list[dict[str, Any]] = []
    for item in inventory.to_dict("records"):
        if int(item["parquet_files"]) <= 0:
            continue
        trade_date = str(item["trade_date"])
        symbol = str(item["symbol"])
        try:
            stats, buckets = build_duckdb_receive_stats(real_root, exchange, trade_date, symbol)
            stats_frames.append(stats)
            if not buckets.empty:
                bucket_frames.append(buckets)
        except Exception as exc:
            row, buckets = inspect_symbol_day(real_root, trade_date, exchange, symbol)
            row["duckdb_read_status"] = "failed_pandas_fallback"
            row["duckdb_read_error"] = repr(exc)
            fallback_rows.append(row)
            if not buckets.empty:
                bucket_frames.append(buckets)
    stats = pd.concat(stats_frames, ignore_index=True) if stats_frames else pd.DataFrame()
    bucket_frame = pd.concat(bucket_frames, ignore_index=True) if bucket_frames else empty_buckets
    merged = inventory.merge(stats, on=["trade_date", "exchange", "symbol"], how="left", suffixes=("", "_stats"))
    if fallback_rows:
        fallback = pd.DataFrame(fallback_rows)
        fallback_keys = set(zip(fallback["trade_date"].astype(str), fallback["exchange"].astype(str), fallback["symbol"].astype(str)))
        keep = [
            (str(row.trade_date), str(row.exchange), str(row.symbol)) not in fallback_keys
            for row in merged[["trade_date", "exchange", "symbol"]].itertuples(index=False)
        ]
        merged = pd.concat([merged.loc[keep], fallback], ignore_index=True, sort=False)
    fill_zero_cols = [
        "rows",
        "session_rows",
        "session_seconds",
        "session_tick_rate_per_sec",
        "gaps_le_100ms",
        "gaps_le_500ms",
        "gaps_le_1s",
        "gaps_gt_5s",
        "duplicate_receive_ms",
        "receive_ms_monotonic_violations",
        "l1_state_change_rows",
        "l1_state_change_fraction",
        "depth_qty_change_rows",
        "depth_qty_change_fraction",
        "active_1s_buckets",
    ]
    for col in fill_zero_cols:
        if col not in merged.columns:
            merged[col] = 0
        merged[col] = pd.to_numeric(merged[col], errors="coerce").fillna(0)
    for col in ["median_gap_sec", "p90_gap_sec", "p95_gap_sec"]:
        if col not in merged.columns:
            merged[col] = ""
    for col in ["first_receive_utc", "last_receive_utc"]:
        if col not in merged.columns:
            merged[col] = ""
        merged[col] = merged[col].fillna("")
    merged["receive_flow_feature_ready"] = (
        merged["schema_pass"].astype(bool)
        & merged["session_rows"].astype(int).gt(0)
        & merged["active_1s_buckets"].astype(int).gt(0)
    )
    return merged, bucket_frame


def build_date_audit(symbol_day: pd.DataFrame, bucket_frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for trade_date, frame in symbol_day.groupby("trade_date", sort=True):
        ready_symbols = int(frame["receive_flow_feature_ready"].astype(bool).sum())
        symbols_with_files = int(frame["parquet_files"].astype(int).gt(0).sum())
        schema_pass_symbols = int(frame["schema_pass"].astype(bool).sum())
        date_buckets = bucket_frame[bucket_frame["trade_date"].astype(str).eq(str(trade_date))] if not bucket_frame.empty else pd.DataFrame()
        if date_buckets.empty:
            sync_buckets = 0
            median_symbols_per_1s_bucket = 0.0
            p90_symbols_per_1s_bucket = 0.0
        else:
            counts = date_buckets.groupby("bucket_1s")["symbol"].nunique()
            sync_buckets = int(counts.ge(2).sum())
            median_symbols_per_1s_bucket = float(counts.median())
            p90_symbols_per_1s_bucket = float(counts.quantile(0.90))
        rows.append(
            {
                "trade_date": trade_date,
                "expected_symbols": len(EXPECTED_SYMBOLS),
                "symbols_with_files": symbols_with_files,
                "schema_pass_symbols": schema_pass_symbols,
                "receive_flow_ready_symbols": ready_symbols,
                "parquet_files": int(frame["parquet_files"].astype(int).sum()),
                "rows": int(frame["rows"].astype(int).sum()),
                "bytes": int(frame["bytes"].astype(int).sum()),
                "median_symbol_tick_rate_per_sec": float(frame["session_tick_rate_per_sec"].astype(float).median()) if not frame.empty else 0.0,
                "median_symbol_gap_sec": float(pd.to_numeric(frame["median_gap_sec"], errors="coerce").median()) if not frame.empty else 0.0,
                "median_l1_state_change_fraction": float(frame["l1_state_change_fraction"].astype(float).median()) if not frame.empty else 0.0,
                "median_depth_qty_change_fraction": float(frame["depth_qty_change_fraction"].astype(float).median()) if not frame.empty else 0.0,
                "active_1s_buckets": int(frame["active_1s_buckets"].astype(int).sum()),
                "cross_symbol_sync_1s_buckets": sync_buckets,
                "median_symbols_per_1s_bucket": median_symbols_per_1s_bucket,
                "p90_symbols_per_1s_bucket": p90_symbols_per_1s_bucket,
                "date_receive_flow_ready": bool(ready_symbols == len(EXPECTED_SYMBOLS)),
            }
        )
    return pd.DataFrame(rows)


def build_gate_evaluation(date_audit: pd.DataFrame, symbol_day: pd.DataFrame, min_ready_days: int) -> pd.DataFrame:
    ready_dates = int(date_audit["date_receive_flow_ready"].astype(bool).sum()) if not date_audit.empty else 0
    all_rows_local = bool(symbol_day["symbol_dir"].astype(str).str.contains("real_data_sample", regex=False).all()) if not symbol_day.empty else False
    return pd.DataFrame(
        [
            {
                "gate_id": "P172_LOCAL_PANEL_DISCOVERED",
                "gate_pass": int(not date_audit.empty),
                "evidence": f"trade_dates={len(date_audit)}",
                "severity": "hard",
            },
            {
                "gate_id": "P172_DOWNLOAD_FIRST_LOCAL_ONLY",
                "gate_pass": int(all_rows_local),
                "evidence": "audited local real_data_sample/l2_multiday_panel paths only",
                "severity": "hard",
            },
            {
                "gate_id": "P172_ALL_EXPECTED_SYMBOLS_PRESENT_PER_READY_DATE",
                "gate_pass": int(ready_dates > 0 and date_audit["receive_flow_ready_symbols"].astype(int).max() == len(EXPECTED_SYMBOLS)),
                "evidence": f"max_ready_symbols={int(date_audit['receive_flow_ready_symbols'].astype(int).max()) if not date_audit.empty else 0}",
                "severity": "hard",
            },
            {
                "gate_id": "P172_RECEIVE_FLOW_COLUMNS_PRESENT",
                "gate_pass": int(symbol_day["schema_pass"].astype(bool).all()) if not symbol_day.empty else 0,
                "evidence": f"schema_pass_symbols={int(symbol_day['schema_pass'].astype(bool).sum()) if not symbol_day.empty else 0}/{len(symbol_day)}",
                "severity": "hard",
            },
            {
                "gate_id": "P172_MINIMUM_SOURCE_DAYS_FOR_PHASE171",
                "gate_pass": int(ready_dates >= min_ready_days),
                "evidence": f"ready_dates={ready_dates};minimum={min_ready_days}",
                "severity": "unlock",
            },
            {
                "gate_id": "P172_NO_REPLAY_OR_PROFITABILITY_OUTPUTS",
                "gate_pass": 1,
                "evidence": "availability/cadence/churn/synchrony audit only",
                "severity": "hard",
            },
        ]
    )


def build_acceptance_summary(date_audit: pd.DataFrame, symbol_day: pd.DataFrame, gates: pd.DataFrame, phase171: pd.DataFrame, min_ready_days: int) -> pd.DataFrame:
    ready_dates = int(date_audit["date_receive_flow_ready"].astype(bool).sum()) if not date_audit.empty else 0
    days_needed = max(0, min_ready_days - ready_dates)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    unlock = gates[gates["severity"].astype(str).eq("unlock")]
    selected_source = metric_value(phase171, "phase171_selected_source_id", "missing_phase171_summary")
    replay_allowed = int(ready_dates >= min_ready_days and bool(unlock["gate_pass"].astype(bool).all()) if not unlock.empty else False)
    next_action = (
        "build_phase173_receive_flow_feature_schema_no_replay"
        if replay_allowed
        else "download_at_least_2_additional_real_l2_dates_then_rerun_phase172"
    )
    return pd.DataFrame(
        [
            ("phase172_selected_phase171_source_id", selected_source, "Phase171 source this audit supports"),
            ("phase172_trade_dates_discovered", int(len(date_audit)), "Local trade_date partitions discovered"),
            ("phase172_ready_receive_flow_dates", ready_dates, "Dates with all 32 symbols receive-flow ready"),
            ("phase172_minimum_ready_dates_required", min_ready_days, "Minimum days required by Phase171 source contract"),
            ("phase172_additional_dates_needed", days_needed, "Additional ready real L2 dates required"),
            ("phase172_symbol_day_rows", int(len(symbol_day)), "Symbol/day partitions audited"),
            ("phase172_total_parquet_files", int(symbol_day["parquet_files"].astype(int).sum()) if not symbol_day.empty else 0, "Local Parquet files audited"),
            ("phase172_total_rows", int(symbol_day["rows"].astype(int).sum()) if not symbol_day.empty else 0, "Rows scanned from local Parquet"),
            ("phase172_total_bytes", int(symbol_day["bytes"].astype(int).sum()) if not symbol_day.empty else 0, "Compressed local Parquet bytes"),
            ("phase172_median_symbol_tick_rate_per_sec", float(symbol_day["session_tick_rate_per_sec"].astype(float).median()) if not symbol_day.empty else 0.0, "Median symbol session receive tick rate"),
            ("phase172_median_symbol_gap_sec", float(pd.to_numeric(symbol_day["median_gap_sec"], errors="coerce").median()) if not symbol_day.empty else 0.0, "Median symbol receive gap"),
            ("phase172_median_l1_state_change_fraction", float(symbol_day["l1_state_change_fraction"].astype(float).median()) if not symbol_day.empty else 0.0, "Median L1 state change fraction"),
            ("phase172_median_depth_qty_change_fraction", float(symbol_day["depth_qty_change_fraction"].astype(float).median()) if not symbol_day.empty else 0.0, "Median top-five depth quantity change fraction"),
            ("phase172_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase172_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase172_unlock_gate_rows", int(len(unlock)), "Unlock gates evaluated"),
            ("phase172_unlock_gate_pass_rows", int(unlock["gate_pass"].astype(bool).sum()) if not unlock.empty else 0, "Unlock gates passed"),
            ("phase172_strategy_replay_allowed", replay_allowed, "Strategy replay remains closed unless minimum real-source days pass"),
            ("phase172_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase172_azure_read_policy", "forbidden_for_analysis_download_first_then_local", "Audit uses local downloaded Parquet only"),
            ("phase172_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase172 Real L2 Receive-flow Availability Audit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase172 audits the Phase171 selected source using downloaded local Zerodha top-five market-by-price Parquet only.",
        "It measures local coverage, receive cadence, quote/depth churn availability and cross-symbol 1-second synchrony.",
        "It does not scan Azure, emit signals, simulate orders, run fills, compute P&L, or open paper/live acceptance.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase172_real_l2_receive_flow_availability_audit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase172(
    real_root: Path,
    phase171_dir: Path,
    output_dir: Path,
    base_dir: Path,
    exchange: str,
    min_ready_days: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase171 = read_csv(phase171_dir / "phase171_external_orderflow_source_acceptance_summary.csv")
    trade_dates = discover_trade_dates(real_root)
    symbol_day, buckets = build_symbol_day_audit(real_root, trade_dates, exchange)
    date_audit = build_date_audit(symbol_day, buckets)
    gates = build_gate_evaluation(date_audit, symbol_day, min_ready_days)
    acceptance = build_acceptance_summary(date_audit, symbol_day, gates, phase171, min_ready_days)

    date_audit.to_csv(output_dir / "phase172_date_receive_flow_audit.csv", index=False)
    symbol_day.to_csv(output_dir / "phase172_symbol_day_receive_flow_audit.csv", index=False)
    buckets.to_csv(output_dir / "phase172_symbol_1s_bucket_presence.csv", index=False)
    gates.to_csv(output_dir / "phase172_receive_flow_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase172_real_l2_receive_flow_availability_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Date Receive-flow Audit": date_audit,
            "Symbol-day Receive-flow Audit Sample": symbol_day.head(80),
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase172_real_l2_receive_flow_availability_audit",
        **reproducibility_fields(
            artifact_id="phase172_real_l2_receive_flow_availability_audit",
            generated_utc=generated,
            inputs={
                "real_root": str(real_root),
                "phase171_acceptance": str(phase171_dir / "phase171_external_orderflow_source_acceptance_summary.csv"),
            },
            parameters={
                "exchange": exchange,
                "expected_symbols": len(EXPECTED_SYMBOLS),
                "minimum_ready_days": min_ready_days,
                "receive_flow_columns": REQUIRED_RECEIVE_FLOW_COLUMNS,
                "azure_io_policy": "none; local downloaded Parquet only",
                "strategy_replay_policy": "closed",
            },
            outputs={
                "date_audit": str(output_dir / "phase172_date_receive_flow_audit.csv"),
                "symbol_day_audit": str(output_dir / "phase172_symbol_day_receive_flow_audit.csv"),
                "symbol_1s_bucket_presence": str(output_dir / "phase172_symbol_1s_bucket_presence.csv"),
                "gate_evaluation": str(output_dir / "phase172_receive_flow_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase172_real_l2_receive_flow_availability_acceptance_summary.csv"),
                "report": str(output_dir / "phase172_real_l2_receive_flow_availability_audit_report.md"),
            },
            random_seed="none_deterministic_local_audit",
            scenario_ids="phase171_selected_real_multiday_receive_event_flow_source",
            cost_model_version="not_applicable_no_replay",
            latency_model_version="not_applicable_no_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase172_real_l2_receive_flow_availability_audit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--phase171-dir", type=Path, default=DEFAULT_PHASE171_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--exchange", default=DEFAULT_EXCHANGE)
    parser.add_argument("--min-ready-days", type=int, default=DEFAULT_MIN_READY_DAYS)
    args = parser.parse_args()
    run_phase172(args.real_root, args.phase171_dir, args.output_dir, args.base_dir, args.exchange, args.min_ready_days)


if __name__ == "__main__":
    main()
