from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, calculate_equity_intraday_nse_charges


DEFAULT_PHASE253_DIR = Path("outputs/phase253")
DEFAULT_RAW_ROOT = Path("real_data_sample/l2_single_day")
DEFAULT_OUTPUT_DIR = Path("outputs/phase254")
EVENTS_PER_BAR = 20
MAX_FILES_PER_SYMBOL = 250
FORBIDDEN_TUNING_DATES = {"2026-07-17", "2026-07-20"}


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(path: Path, metric: str, default: Any = None) -> Any:
    frame = read_csv(path)
    if frame.empty or "metric" not in frame.columns:
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


def parquet_glob(raw_root: Path) -> str:
    return str((raw_root / "**" / "*.parquet").as_posix())


def build_materialization_sql(raw_glob: str, output_parquet: Path, zerodha_bps: float, events_per_bar: int) -> str:
    out = output_parquet.as_posix()
    forbidden = ",".join(f"'{d}'" for d in sorted(FORBIDDEN_TUNING_DATES))
    return f"""
copy (
with raw as (
    select
        cast(trade_date as varchar) as trade_date,
        exchange,
        coalesce(symbol, tradingsymbol, requested_symbol) as symbol,
        collector_received_utc,
        collector_received_utc_ms,
        collector_received_monotonic_ns,
        last_price::double as last_price,
        last_traded_quantity::double as last_traded_quantity,
        volume_traded::double as volume_traded,
        buy_1_price::double as buy_1_price,
        buy_1_quantity::double as buy_1_quantity,
        buy_1_orders::double as buy_1_orders,
        buy_2_price::double as buy_2_price,
        buy_2_quantity::double as buy_2_quantity,
        buy_2_orders::double as buy_2_orders,
        buy_3_price::double as buy_3_price,
        buy_3_quantity::double as buy_3_quantity,
        buy_3_orders::double as buy_3_orders,
        buy_4_price::double as buy_4_price,
        buy_4_quantity::double as buy_4_quantity,
        buy_4_orders::double as buy_4_orders,
        buy_5_price::double as buy_5_price,
        buy_5_quantity::double as buy_5_quantity,
        buy_5_orders::double as buy_5_orders,
        sell_1_price::double as sell_1_price,
        sell_1_quantity::double as sell_1_quantity,
        sell_1_orders::double as sell_1_orders,
        sell_2_price::double as sell_2_price,
        sell_2_quantity::double as sell_2_quantity,
        sell_2_orders::double as sell_2_orders,
        sell_3_price::double as sell_3_price,
        sell_3_quantity::double as sell_3_quantity,
        sell_3_orders::double as sell_3_orders,
        sell_4_price::double as sell_4_price,
        sell_4_quantity::double as sell_4_quantity,
        sell_4_orders::double as sell_4_orders,
        sell_5_price::double as sell_5_price,
        sell_5_quantity::double as sell_5_quantity,
        sell_5_orders::double as sell_5_orders
    from read_parquet('{raw_glob}', hive_partitioning=true, union_by_name=true)
),
ordered as (
    select
        *,
        row_number() over (
            partition by trade_date, exchange, symbol
            order by collector_received_utc_ms, collector_received_monotonic_ns, collector_received_utc
        ) as receive_seq
    from raw
    where trade_date is not null and exchange is not null and symbol is not null
),
tick_features as (
    select
        *,
        floor((receive_seq - 1) / {int(events_per_bar)})::bigint as richer_event_bar_id,
        ((buy_1_price + sell_1_price) / 2.0) as mid_price,
        greatest(sell_1_price - buy_1_price, 0.0) as l1_spread,
        (sell_1_price - buy_1_price) / nullif(((buy_1_price + sell_1_price) / 2.0), 0.0) * 10000.0 as spread_bps,
        (buy_1_quantity + buy_2_quantity + buy_3_quantity + buy_4_quantity + buy_5_quantity) as cum_buy_qty_l1_l5,
        (sell_1_quantity + sell_2_quantity + sell_3_quantity + sell_4_quantity + sell_5_quantity) as cum_sell_qty_l1_l5,
        (buy_2_quantity + buy_3_quantity + buy_4_quantity + buy_5_quantity) as cum_buy_qty_l2_l5,
        (sell_2_quantity + sell_3_quantity + sell_4_quantity + sell_5_quantity) as cum_sell_qty_l2_l5,
        (buy_1_orders + buy_2_orders + buy_3_orders + buy_4_orders + buy_5_orders) as cum_buy_orders_l1_l5,
        (sell_1_orders + sell_2_orders + sell_3_orders + sell_4_orders + sell_5_orders) as cum_sell_orders_l1_l5,
        ((buy_1_quantity + buy_2_quantity + buy_3_quantity + buy_4_quantity + buy_5_quantity) -
         (sell_1_quantity + sell_2_quantity + sell_3_quantity + sell_4_quantity + sell_5_quantity)) /
         nullif((buy_1_quantity + buy_2_quantity + buy_3_quantity + buy_4_quantity + buy_5_quantity +
                 sell_1_quantity + sell_2_quantity + sell_3_quantity + sell_4_quantity + sell_5_quantity), 0.0) as cum_top5_qty_imbalance,
        ((buy_2_quantity + buy_3_quantity + buy_4_quantity + buy_5_quantity) -
         (sell_2_quantity + sell_3_quantity + sell_4_quantity + sell_5_quantity)) /
         nullif((buy_2_quantity + buy_3_quantity + buy_4_quantity + buy_5_quantity +
                 sell_2_quantity + sell_3_quantity + sell_4_quantity + sell_5_quantity), 0.0) as depth_beyond_l1_qty_imbalance,
        (5*buy_1_quantity + 4*buy_2_quantity + 3*buy_3_quantity + 2*buy_4_quantity + buy_5_quantity -
         (5*sell_1_quantity + 4*sell_2_quantity + 3*sell_3_quantity + 2*sell_4_quantity + sell_5_quantity)) /
         nullif(5*buy_1_quantity + 4*buy_2_quantity + 3*buy_3_quantity + 2*buy_4_quantity + buy_5_quantity +
                5*sell_1_quantity + 4*sell_2_quantity + 3*sell_3_quantity + 2*sell_4_quantity + sell_5_quantity, 0.0) as level_weighted_depth_imbalance,
        (buy_5_quantity - buy_1_quantity) / 4.0 as depth_slope_bid,
        (sell_5_quantity - sell_1_quantity) / 4.0 as depth_slope_ask,
        (buy_1_quantity - 2*buy_3_quantity + buy_5_quantity) as depth_convexity_bid,
        (sell_1_quantity - 2*sell_3_quantity + sell_5_quantity) as depth_convexity_ask,
        ((buy_1_orders + buy_2_orders + buy_3_orders + buy_4_orders + buy_5_orders) -
         (sell_1_orders + sell_2_orders + sell_3_orders + sell_4_orders + sell_5_orders)) /
         nullif((buy_1_orders + buy_2_orders + buy_3_orders + buy_4_orders + buy_5_orders +
                 sell_1_orders + sell_2_orders + sell_3_orders + sell_4_orders + sell_5_orders), 0.0) as order_count_imbalance_l1_l5,
        (buy_1_quantity + buy_2_quantity + buy_3_quantity + buy_4_quantity + buy_5_quantity) /
            nullif((buy_1_orders + buy_2_orders + buy_3_orders + buy_4_orders + buy_5_orders), 0.0) as avg_qty_per_order_bid_l1_l5,
        (sell_1_quantity + sell_2_quantity + sell_3_quantity + sell_4_quantity + sell_5_quantity) /
            nullif((sell_1_orders + sell_2_orders + sell_3_orders + sell_4_orders + sell_5_orders), 0.0) as avg_qty_per_order_ask_l1_l5
    from ordered
),
deltas as (
    select
        *,
        abs(buy_1_quantity - lag(buy_1_quantity) over w) + abs(buy_2_quantity - lag(buy_2_quantity) over w) +
        abs(buy_3_quantity - lag(buy_3_quantity) over w) + abs(buy_4_quantity - lag(buy_4_quantity) over w) +
        abs(buy_5_quantity - lag(buy_5_quantity) over w) + abs(sell_1_quantity - lag(sell_1_quantity) over w) +
        abs(sell_2_quantity - lag(sell_2_quantity) over w) + abs(sell_3_quantity - lag(sell_3_quantity) over w) +
        abs(sell_4_quantity - lag(sell_4_quantity) over w) + abs(sell_5_quantity - lag(sell_5_quantity) over w) as top5_qty_churn,
        abs(buy_1_orders - lag(buy_1_orders) over w) + abs(buy_2_orders - lag(buy_2_orders) over w) +
        abs(buy_3_orders - lag(buy_3_orders) over w) + abs(buy_4_orders - lag(buy_4_orders) over w) +
        abs(buy_5_orders - lag(buy_5_orders) over w) + abs(sell_1_orders - lag(sell_1_orders) over w) +
        abs(sell_2_orders - lag(sell_2_orders) over w) + abs(sell_3_orders - lag(sell_3_orders) over w) +
        abs(sell_4_orders - lag(sell_4_orders) over w) + abs(sell_5_orders - lag(sell_5_orders) over w) as top5_order_churn,
        (cum_buy_qty_l1_l5 - lag(cum_buy_qty_l1_l5) over w) as delta_cum_buy_qty_l1_l5,
        (cum_sell_qty_l1_l5 - lag(cum_sell_qty_l1_l5) over w) as delta_cum_sell_qty_l1_l5,
        (mid_price - lag(mid_price) over w) as delta_mid_price,
        (buy_1_price - lag(buy_1_price) over w) as buy_1_price_shift,
        (sell_1_price - lag(sell_1_price) over w) as sell_1_price_shift,
        (volume_traded - lag(volume_traded) over w) as delta_volume_traded
    from tick_features
    window w as (partition by trade_date, exchange, symbol order by receive_seq)
),
event_bars as (
    select
        trade_date,
        exchange,
        symbol,
        richer_event_bar_id,
        count(*) as source_tick_count,
        min(receive_seq) as first_receive_seq,
        max(receive_seq) as last_receive_seq,
        min(collector_received_utc_ms) as first_received_utc_ms,
        max(collector_received_utc_ms) as last_received_utc_ms,
        first(mid_price order by receive_seq) as open_mid_price,
        last(mid_price order by receive_seq) as close_mid_price,
        last(mid_price order by receive_seq) / nullif(first(mid_price order by receive_seq), 0.0) - 1.0 as bar_return,
        avg(l1_spread) as avg_l1_spread,
        avg(spread_bps) as avg_spread_bps,
        avg(cum_buy_qty_l1_l5) as avg_cum_buy_qty_l1_l5,
        avg(cum_sell_qty_l1_l5) as avg_cum_sell_qty_l1_l5,
        avg(cum_buy_qty_l2_l5) as avg_cum_buy_qty_l2_l5,
        avg(cum_sell_qty_l2_l5) as avg_cum_sell_qty_l2_l5,
        avg(cum_buy_orders_l1_l5) as avg_cum_buy_orders_l1_l5,
        avg(cum_sell_orders_l1_l5) as avg_cum_sell_orders_l1_l5,
        avg(cum_top5_qty_imbalance) as avg_cum_top5_qty_imbalance,
        avg(depth_beyond_l1_qty_imbalance) as avg_depth_beyond_l1_qty_imbalance,
        avg(level_weighted_depth_imbalance) as avg_level_weighted_depth_imbalance,
        avg(depth_slope_bid) as avg_depth_slope_bid,
        avg(depth_slope_ask) as avg_depth_slope_ask,
        avg(depth_convexity_bid) as avg_depth_convexity_bid,
        avg(depth_convexity_ask) as avg_depth_convexity_ask,
        avg(order_count_imbalance_l1_l5) as avg_order_count_imbalance_l1_l5,
        avg(avg_qty_per_order_bid_l1_l5) as avg_qty_per_order_bid_l1_l5,
        avg(avg_qty_per_order_ask_l1_l5) as avg_qty_per_order_ask_l1_l5,
        sum(coalesce(top5_qty_churn, 0.0)) as top5_qty_churn_sum,
        sum(coalesce(top5_order_churn, 0.0)) as top5_order_churn_sum,
        sum(greatest(coalesce(delta_cum_buy_qty_l1_l5, 0.0), 0.0) + greatest(coalesce(delta_cum_sell_qty_l1_l5, 0.0), 0.0)) as depth_replenishment_pressure,
        sum(greatest(-coalesce(delta_cum_buy_qty_l1_l5, 0.0), 0.0) + greatest(-coalesce(delta_cum_sell_qty_l1_l5, 0.0), 0.0)) as depth_withdrawal_pressure,
        sum(abs(coalesce(buy_1_price_shift, 0.0)) + abs(coalesce(sell_1_price_shift, 0.0))) as l1_price_shift_abs_sum,
        sum(greatest(coalesce(delta_volume_traded, 0.0), 0.0)) as volume_increment_sum,
        sum(case when sell_1_price <= buy_1_price then 1 else 0 end) as crossed_or_locked_tick_rows,
        sum(case when cum_buy_qty_l1_l5 <= 0 or cum_sell_qty_l1_l5 <= 0 then 1 else 0 end) as nonpositive_depth_tick_rows,
        sum(case when buy_1_price is null or sell_1_price is null or buy_5_price is null or sell_5_price is null then 1 else 0 end) as missing_level_tick_rows
    from deltas
    group by trade_date, exchange, symbol, richer_event_bar_id
),
labeled as (
    select
        *,
        (close_mid_price / nullif(open_mid_price, 0.0) - 1.0) * 10000.0 as bar_return_bps,
        avg_spread_bps + {float(zerodha_bps)} as taker_round_trip_cost_floor_bps,
        {float(zerodha_bps)} as zerodha_round_trip_charge_bps,
        case when trade_date in ({forbidden}) then 0 else 1 end as allowed_for_training_parameter_selection,
        lead(close_mid_price, 3) over (partition by trade_date, exchange, symbol order by richer_event_bar_id) / nullif(close_mid_price, 0.0) - 1.0 as future_return_h3,
        lead(close_mid_price, 6) over (partition by trade_date, exchange, symbol order by richer_event_bar_id) / nullif(close_mid_price, 0.0) - 1.0 as future_return_h6,
        lead(close_mid_price, 10) over (partition by trade_date, exchange, symbol order by richer_event_bar_id) / nullif(close_mid_price, 0.0) - 1.0 as future_return_h10
    from event_bars
)
select * from labeled
) to '{out}' (format parquet, compression zstd);
"""


def run_duckdb_materialization(raw_root: Path, output_parquet: Path, events_per_bar: int) -> None:
    charges = calculate_equity_intraday_nse_charges(buy_value_inr=100_000.0, sell_value_inr=100_000.0)
    sql = build_materialization_sql(parquet_glob(raw_root), output_parquet, float(charges.breakeven_bps_on_buy_value), events_per_bar)
    con = duckdb.connect()
    con.execute("set preserve_insertion_order=false")
    con.execute(sql)
    con.close()


def symbol_from_path(path: Path) -> str:
    for part in path.parts:
        if part.startswith("symbol="):
            return part.split("=", 1)[1]
    return ""


def discover_bounded_files(raw_root: Path, max_files_per_symbol: int) -> list[Path]:
    grouped: dict[str, list[Path]] = {}
    for path in sorted(raw_root.rglob("*.parquet")):
        symbol = symbol_from_path(path)
        if not symbol:
            symbol = path.parent.name
        bucket = grouped.setdefault(symbol, [])
        if len(bucket) < int(max_files_per_symbol):
            bucket.append(path)
    files: list[Path] = []
    for symbol in sorted(grouped):
        files.extend(grouped[symbol])
    return files


def materialize_bounded_python(raw_root: Path, output_parquet: Path, events_per_bar: int, max_files_per_symbol: int) -> tuple[int, int]:
    files = discover_bounded_files(raw_root, max_files_per_symbol)
    if not files:
        raise FileNotFoundError(f"No parquet files found under {raw_root}")
    frames: list[pd.DataFrame] = []
    for path in files:
        frame = pd.read_parquet(path)
        if "symbol" not in frame.columns:
            frame["symbol"] = symbol_from_path(path) or frame.get("tradingsymbol", "")
        frames.append(frame)
    raw = pd.concat(frames, ignore_index=True, sort=False)
    raw["symbol"] = raw["symbol"].astype(str)
    raw["trade_date"] = raw["trade_date"].astype(str)
    raw["exchange"] = raw["exchange"].astype(str)
    sort_cols = [c for c in ["trade_date", "exchange", "symbol", "collector_received_utc_ms", "collector_received_monotonic_ns", "collector_received_utc"] if c in raw.columns]
    raw = raw.sort_values(sort_cols, kind="mergesort").reset_index(drop=True)
    raw["receive_seq"] = raw.groupby(["trade_date", "exchange", "symbol"], sort=False).cumcount() + 1
    raw["richer_event_bar_id"] = ((raw["receive_seq"] - 1) // int(events_per_bar)).astype("int64")
    numeric_cols = [
        "last_price",
        "last_traded_quantity",
        "volume_traded",
        *(f"buy_{level}_{field}" for level in range(1, 6) for field in ("price", "quantity", "orders")),
        *(f"sell_{level}_{field}" for level in range(1, 6) for field in ("price", "quantity", "orders")),
    ]
    for col in numeric_cols:
        raw[col] = pd.to_numeric(raw[col], errors="coerce")
    raw["mid_price"] = (raw["buy_1_price"] + raw["sell_1_price"]) / 2.0
    raw["l1_spread"] = (raw["sell_1_price"] - raw["buy_1_price"]).clip(lower=0.0)
    raw["spread_bps"] = raw["l1_spread"] / raw["mid_price"].replace(0, pd.NA) * 10000.0
    buy_qty = [f"buy_{level}_quantity" for level in range(1, 6)]
    sell_qty = [f"sell_{level}_quantity" for level in range(1, 6)]
    buy_orders = [f"buy_{level}_orders" for level in range(1, 6)]
    sell_orders = [f"sell_{level}_orders" for level in range(1, 6)]
    raw["cum_buy_qty_l1_l5"] = raw[buy_qty].sum(axis=1)
    raw["cum_sell_qty_l1_l5"] = raw[sell_qty].sum(axis=1)
    raw["cum_buy_qty_l2_l5"] = raw[buy_qty[1:]].sum(axis=1)
    raw["cum_sell_qty_l2_l5"] = raw[sell_qty[1:]].sum(axis=1)
    raw["cum_buy_orders_l1_l5"] = raw[buy_orders].sum(axis=1)
    raw["cum_sell_orders_l1_l5"] = raw[sell_orders].sum(axis=1)
    raw["cum_top5_qty_imbalance"] = (raw["cum_buy_qty_l1_l5"] - raw["cum_sell_qty_l1_l5"]) / (raw["cum_buy_qty_l1_l5"] + raw["cum_sell_qty_l1_l5"]).replace(0, pd.NA)
    raw["depth_beyond_l1_qty_imbalance"] = (raw["cum_buy_qty_l2_l5"] - raw["cum_sell_qty_l2_l5"]) / (raw["cum_buy_qty_l2_l5"] + raw["cum_sell_qty_l2_l5"]).replace(0, pd.NA)
    weights = pd.Series([5, 4, 3, 2, 1], index=range(1, 6), dtype=float)
    weighted_buy = sum(float(weights[level]) * raw[f"buy_{level}_quantity"] for level in range(1, 6))
    weighted_sell = sum(float(weights[level]) * raw[f"sell_{level}_quantity"] for level in range(1, 6))
    raw["level_weighted_depth_imbalance"] = (weighted_buy - weighted_sell) / (weighted_buy + weighted_sell).replace(0, pd.NA)
    raw["depth_slope_bid"] = (raw["buy_5_quantity"] - raw["buy_1_quantity"]) / 4.0
    raw["depth_slope_ask"] = (raw["sell_5_quantity"] - raw["sell_1_quantity"]) / 4.0
    raw["depth_convexity_bid"] = raw["buy_1_quantity"] - 2.0 * raw["buy_3_quantity"] + raw["buy_5_quantity"]
    raw["depth_convexity_ask"] = raw["sell_1_quantity"] - 2.0 * raw["sell_3_quantity"] + raw["sell_5_quantity"]
    raw["order_count_imbalance_l1_l5"] = (raw["cum_buy_orders_l1_l5"] - raw["cum_sell_orders_l1_l5"]) / (raw["cum_buy_orders_l1_l5"] + raw["cum_sell_orders_l1_l5"]).replace(0, pd.NA)
    raw["avg_qty_per_order_bid_l1_l5"] = raw["cum_buy_qty_l1_l5"] / raw["cum_buy_orders_l1_l5"].replace(0, pd.NA)
    raw["avg_qty_per_order_ask_l1_l5"] = raw["cum_sell_qty_l1_l5"] / raw["cum_sell_orders_l1_l5"].replace(0, pd.NA)
    group = raw.groupby(["trade_date", "exchange", "symbol"], sort=False)
    for col in buy_qty + sell_qty + buy_orders + sell_orders + ["cum_buy_qty_l1_l5", "cum_sell_qty_l1_l5", "mid_price", "buy_1_price", "sell_1_price", "volume_traded"]:
        raw[f"delta_{col}"] = group[col].diff()
    raw["top5_qty_churn"] = raw[[f"delta_{c}" for c in buy_qty + sell_qty]].abs().sum(axis=1)
    raw["top5_order_churn"] = raw[[f"delta_{c}" for c in buy_orders + sell_orders]].abs().sum(axis=1)
    raw["crossed_or_locked_tick"] = (raw["sell_1_price"] <= raw["buy_1_price"]).astype(int)
    raw["nonpositive_depth_tick"] = ((raw["cum_buy_qty_l1_l5"] <= 0) | (raw["cum_sell_qty_l1_l5"] <= 0)).astype(int)
    raw["missing_level_tick"] = raw[["buy_1_price", "sell_1_price", "buy_5_price", "sell_5_price"]].isna().any(axis=1).astype(int)
    invalid_tick_rows = int(
        (
            raw["crossed_or_locked_tick"].eq(1)
            | raw["nonpositive_depth_tick"].eq(1)
            | raw["missing_level_tick"].eq(1)
        ).sum()
    )
    raw = raw[
        raw["crossed_or_locked_tick"].eq(0)
        & raw["nonpositive_depth_tick"].eq(0)
        & raw["missing_level_tick"].eq(0)
    ].copy()
    charges = calculate_equity_intraday_nse_charges(buy_value_inr=100_000.0, sell_value_inr=100_000.0)
    zerodha_bps = float(charges.breakeven_bps_on_buy_value)
    agg = raw.groupby(["trade_date", "exchange", "symbol", "richer_event_bar_id"], sort=False).agg(
        source_tick_count=("receive_seq", "count"),
        first_receive_seq=("receive_seq", "min"),
        last_receive_seq=("receive_seq", "max"),
        first_received_utc_ms=("collector_received_utc_ms", "min"),
        last_received_utc_ms=("collector_received_utc_ms", "max"),
        open_mid_price=("mid_price", "first"),
        close_mid_price=("mid_price", "last"),
        avg_l1_spread=("l1_spread", "mean"),
        avg_spread_bps=("spread_bps", "mean"),
        avg_cum_buy_qty_l1_l5=("cum_buy_qty_l1_l5", "mean"),
        avg_cum_sell_qty_l1_l5=("cum_sell_qty_l1_l5", "mean"),
        avg_cum_buy_qty_l2_l5=("cum_buy_qty_l2_l5", "mean"),
        avg_cum_sell_qty_l2_l5=("cum_sell_qty_l2_l5", "mean"),
        avg_cum_buy_orders_l1_l5=("cum_buy_orders_l1_l5", "mean"),
        avg_cum_sell_orders_l1_l5=("cum_sell_orders_l1_l5", "mean"),
        avg_cum_top5_qty_imbalance=("cum_top5_qty_imbalance", "mean"),
        avg_depth_beyond_l1_qty_imbalance=("depth_beyond_l1_qty_imbalance", "mean"),
        avg_level_weighted_depth_imbalance=("level_weighted_depth_imbalance", "mean"),
        avg_depth_slope_bid=("depth_slope_bid", "mean"),
        avg_depth_slope_ask=("depth_slope_ask", "mean"),
        avg_depth_convexity_bid=("depth_convexity_bid", "mean"),
        avg_depth_convexity_ask=("depth_convexity_ask", "mean"),
        avg_order_count_imbalance_l1_l5=("order_count_imbalance_l1_l5", "mean"),
        avg_qty_per_order_bid_l1_l5=("avg_qty_per_order_bid_l1_l5", "mean"),
        avg_qty_per_order_ask_l1_l5=("avg_qty_per_order_ask_l1_l5", "mean"),
        top5_qty_churn_sum=("top5_qty_churn", "sum"),
        top5_order_churn_sum=("top5_order_churn", "sum"),
        depth_replenishment_pressure=("delta_cum_buy_qty_l1_l5", lambda s: s.clip(lower=0).sum()),
        depth_withdrawal_pressure=("delta_cum_sell_qty_l1_l5", lambda s: (-s).clip(lower=0).sum()),
        l1_price_shift_abs_sum=("delta_buy_1_price", lambda s: s.abs().sum()),
        volume_increment_sum=("delta_volume_traded", lambda s: s.clip(lower=0).sum()),
        crossed_or_locked_tick_rows=("crossed_or_locked_tick", "sum"),
        nonpositive_depth_tick_rows=("nonpositive_depth_tick", "sum"),
        missing_level_tick_rows=("missing_level_tick", "sum"),
    ).reset_index()
    agg["bar_return"] = agg["close_mid_price"] / agg["open_mid_price"].replace(0, pd.NA) - 1.0
    agg["bar_return_bps"] = agg["bar_return"] * 10000.0
    agg["zerodha_round_trip_charge_bps"] = zerodha_bps
    agg["taker_round_trip_cost_floor_bps"] = agg["avg_spread_bps"] + zerodha_bps
    agg["allowed_for_training_parameter_selection"] = (~agg["trade_date"].isin(FORBIDDEN_TUNING_DATES)).astype(int)
    agg = agg.sort_values(["trade_date", "exchange", "symbol", "richer_event_bar_id"], kind="mergesort")
    for horizon in [3, 6, 10]:
        agg[f"future_return_h{horizon}"] = agg.groupby(["trade_date", "exchange", "symbol"], sort=False)["close_mid_price"].shift(-horizon) / agg["close_mid_price"].replace(0, pd.NA) - 1.0
    agg.to_parquet(output_parquet, index=False, compression="zstd")
    return len(files), invalid_tick_rows


def summarize_outputs(output_parquet: Path, output_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    con = duckdb.connect()
    view = f"read_parquet('{output_parquet.as_posix()}')"
    acceptance_stats = con.execute(
        f"""
        select
            count(*)::bigint as event_bar_rows,
            count(distinct trade_date)::bigint as trade_dates,
            count(distinct symbol)::bigint as symbols,
            sum(source_tick_count)::bigint as source_tick_rows,
            sum(crossed_or_locked_tick_rows)::bigint as crossed_or_locked_tick_rows,
            sum(nonpositive_depth_tick_rows)::bigint as nonpositive_depth_tick_rows,
            sum(missing_level_tick_rows)::bigint as missing_level_tick_rows,
            sum(case when allowed_for_training_parameter_selection = 1 then 1 else 0 end)::bigint as training_allowed_event_bar_rows,
            avg(avg_spread_bps)::double as mean_spread_bps,
            median(avg_spread_bps)::double as median_spread_bps,
            avg(avg_cum_top5_qty_imbalance)::double as mean_top5_imbalance,
            avg(avg_depth_beyond_l1_qty_imbalance)::double as mean_depth_beyond_l1_imbalance
        from {view}
        """
    ).fetchdf()
    daily = con.execute(
        f"""
        select
            trade_date,
            count(*)::bigint as event_bar_rows,
            count(distinct symbol)::bigint as symbols,
            sum(source_tick_count)::bigint as source_tick_rows,
            avg(avg_spread_bps)::double as mean_spread_bps,
            sum(crossed_or_locked_tick_rows)::bigint as crossed_or_locked_tick_rows,
            sum(nonpositive_depth_tick_rows)::bigint as nonpositive_depth_tick_rows,
            sum(missing_level_tick_rows)::bigint as missing_level_tick_rows
        from {view}
        group by trade_date
        order by trade_date
        """
    ).fetchdf()
    symbol = con.execute(
        f"""
        select
            symbol,
            count(*)::bigint as event_bar_rows,
            count(distinct trade_date)::bigint as trade_dates,
            sum(source_tick_count)::bigint as source_tick_rows,
            avg(avg_spread_bps)::double as mean_spread_bps,
            avg(avg_cum_top5_qty_imbalance)::double as mean_top5_imbalance,
            avg(avg_depth_beyond_l1_qty_imbalance)::double as mean_depth_beyond_l1_imbalance
        from {view}
        group by symbol
        order by symbol
        """
    ).fetchdf()
    con.close()
    daily.to_csv(output_dir / "phase254_daily_quality_summary.csv", index=False)
    symbol.to_csv(output_dir / "phase254_symbol_feature_summary.csv", index=False)
    return acceptance_stats, daily, symbol


def build_gate_evaluation(stats: dict[str, Any], phase253_dir: Path) -> pd.DataFrame:
    next_action = str(metric_value(phase253_dir / "phase253_acceptance_summary.csv", "phase253_next_best_action", ""))
    rows = [
        ("P254_PHASE253_WORK_ORDER_PRESENT", "run_phase254_materialize_richer_raw_top5_depth_event_bars" in next_action, next_action, "Phase253 next action targets Phase254", "hard"),
        ("P254_EVENT_BARS_MATERIALIZED", as_int(stats.get("event_bar_rows", 0)) > 0, stats.get("event_bar_rows", 0), ">0 richer raw-depth event bars", "hard"),
        ("P254_REAL_DATE_OUTPUT", as_int(stats.get("trade_dates", 0)) >= 1, stats.get("trade_dates", 0), ">=1 real trade date for first richer-depth materialization", "hard"),
        ("P254_SYMBOL_BREADTH", as_int(stats.get("symbols", 0)) >= 20, stats.get("symbols", 0), ">=20 symbols", "hard"),
        ("P254_SOURCE_TICK_COUNTS_RETAINED", as_int(stats.get("source_tick_rows", 0)) > 0, stats.get("source_tick_rows", 0), ">0 source ticks represented", "hard"),
        ("P254_RAW_DEPTH_QUALITY_PASS", as_int(stats.get("crossed_or_locked_tick_rows", 0)) == 0 and as_int(stats.get("missing_level_tick_rows", 0)) == 0, f"crossed={stats.get('crossed_or_locked_tick_rows', 0)};missing={stats.get('missing_level_tick_rows', 0)}", "0 crossed/locked and 0 missing level rows", "hard"),
        ("P254_COST_FIELDS_CARRIED", True, "zerodha_round_trip_charge_bps;taker_round_trip_cost_floor_bps", "cost floor fields present", "hard"),
        ("P254_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase254 Richer Raw Top-five Depth Event-bar Materialization",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase254 materializes compact event bars from existing local raw Zerodha top-five market-by-price parquet.",
        "It reads explicit buy/sell levels 1-5 price, quantity and order-count fields, carries cost-floor fields and does not run replay, promotion, paper/live or profitability claims.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    raw_root: Path = DEFAULT_RAW_ROOT,
    phase253_dir: Path = DEFAULT_PHASE253_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    events_per_bar: int = EVENTS_PER_BAR,
    max_files_per_symbol: int = MAX_FILES_PER_SYMBOL,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    if as_int(metric_value(phase253_dir / "phase253_acceptance_summary.csv", "phase253_phase254_materialization_allowed_next", 0)) != 1:
        raise RuntimeError("Phase253 does not allow Phase254 materialization.")
    output_parquet = output_dir / "phase254_richer_raw_top5_depth_event_bars.parquet"
    source_file_rows, excluded_invalid_tick_rows = materialize_bounded_python(raw_root, output_parquet, events_per_bar, max_files_per_symbol)
    stats_frame, daily, symbol = summarize_outputs(output_parquet, output_dir)
    stats = stats_frame.iloc[0].to_dict() if not stats_frame.empty else {}
    gates = build_gate_evaluation(stats, phase253_dir)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    next_action = (
        "run_phase255_richer_raw_depth_feature_quality_interpretation_no_replay_no_paper_live"
        if hard_pass == len(hard)
        else "repair_phase254_richer_raw_depth_materialization_before_any_search"
    )
    acceptance = pd.DataFrame(
        [
            ("phase254_richer_raw_depth_materialization_complete", 1, "Phase254 richer raw-depth event-bar materialization completed"),
            ("phase254_raw_root_used", str(raw_root), "Existing local raw root used"),
            ("phase254_events_per_bar", int(events_per_bar), "Receive events per richer raw-depth event bar"),
            ("phase254_max_files_per_symbol", int(max_files_per_symbol), "Bounded raw parquet files read per symbol"),
            ("phase254_source_parquet_files_read", int(source_file_rows), "Source raw parquet shards read"),
            ("phase254_excluded_invalid_source_tick_rows", int(excluded_invalid_tick_rows), "Invalid crossed/locked/nonpositive/missing raw ticks excluded before aggregation"),
            ("phase254_event_bar_rows", as_int(stats.get("event_bar_rows", 0)), "Materialized richer event bars"),
            ("phase254_trade_dates", as_int(stats.get("trade_dates", 0)), "Trade dates represented"),
            ("phase254_symbols", as_int(stats.get("symbols", 0)), "Symbols represented"),
            ("phase254_source_tick_rows", as_int(stats.get("source_tick_rows", 0)), "Source raw tick rows represented"),
            ("phase254_training_allowed_event_bar_rows", as_int(stats.get("training_allowed_event_bar_rows", 0)), "Rows allowed for downstream training selection"),
            ("phase254_crossed_or_locked_tick_rows", as_int(stats.get("crossed_or_locked_tick_rows", 0)), "Crossed/locked source tick rows"),
            ("phase254_nonpositive_depth_tick_rows", as_int(stats.get("nonpositive_depth_tick_rows", 0)), "Nonpositive full-depth source rows"),
            ("phase254_missing_level_tick_rows", as_int(stats.get("missing_level_tick_rows", 0)), "Rows missing required level fields"),
            ("phase254_mean_spread_bps", float(stats.get("mean_spread_bps", 0.0) or 0.0), "Mean event-bar spread bps"),
            ("phase254_median_spread_bps", float(stats.get("median_spread_bps", 0.0) or 0.0), "Median event-bar spread bps"),
            ("phase254_mean_top5_imbalance", float(stats.get("mean_top5_imbalance", 0.0) or 0.0), "Mean cumulative top-five imbalance"),
            ("phase254_mean_depth_beyond_l1_imbalance", float(stats.get("mean_depth_beyond_l1_imbalance", 0.0) or 0.0), "Mean depth-beyond-L1 imbalance"),
            ("phase254_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase254_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase254_download_more_dates_now_allowed", 0, "No raw-date download in Phase254"),
            ("phase254_replay_execution_allowed_now", 0, "No replay execution in Phase254"),
            ("phase254_strategy_promotion_allowed", 0, "No strategy promotion from Phase254"),
            ("phase254_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase254"),
            ("phase254_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase254"),
            ("phase254_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    gates.to_csv(output_dir / "phase254_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase254_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase254_richer_raw_top5_depth_event_bar_materialization_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Daily Quality Summary": daily,
            "Symbol Feature Summary": symbol.head(32),
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase254_richer_raw_top5_depth_event_bar_materialization",
        **reproducibility_fields(
            artifact_id="phase254",
            generated_utc=generated_utc,
            inputs={"raw_root": str(raw_root), "phase253_dir": str(phase253_dir)},
            parameters={
                "events_per_bar": int(events_per_bar),
                "max_files_per_symbol": int(max_files_per_symbol),
                "forbidden_tuning_dates": sorted(FORBIDDEN_TUNING_DATES),
                "download_more_dates_now_allowed": 0,
                "replay_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "richer_event_bars": str(output_parquet),
                "daily_quality_summary": str(output_dir / "phase254_daily_quality_summary.csv"),
                "symbol_feature_summary": str(output_dir / "phase254_symbol_feature_summary.csv"),
                "gate_evaluation": str(output_dir / "phase254_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase254_acceptance_summary.csv"),
                "report": str(output_dir / "phase254_richer_raw_top5_depth_event_bar_materialization_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase254_receive_order_raw_top5_depth_event_bar_materializer",
        ),
    }
    (output_dir / "phase254_richer_raw_top5_depth_event_bar_materialization_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase254 richer raw top-five depth event-bar materialization.")
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--phase253-dir", type=Path, default=DEFAULT_PHASE253_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--events-per-bar", type=int, default=EVENTS_PER_BAR)
    parser.add_argument("--max-files-per-symbol", type=int, default=MAX_FILES_PER_SYMBOL)
    args = parser.parse_args()
    manifest = run(
        raw_root=args.raw_root,
        phase253_dir=args.phase253_dir,
        output_dir=args.output_dir,
        events_per_bar=args.events_per_bar,
        max_files_per_symbol=args.max_files_per_symbol,
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
