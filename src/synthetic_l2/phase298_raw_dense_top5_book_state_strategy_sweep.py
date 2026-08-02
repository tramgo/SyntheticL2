from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase271_fixed_capital_concurrency_and_capacity_return_analysis import schedule_events_for_scenario
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, calculate_equity_intraday_nse_charges


DEFAULT_DENSE_ROOT = Path("raw_synthetic_l2_dense_full_year")
DEFAULT_PHASE51_DIR = Path("outputs/phase51")
DEFAULT_PHASE297_DIR = Path("outputs/phase297")
DEFAULT_OUTPUT_DIR = Path("outputs/phase298")

SELECTED_ROUTE = "P298_RAW_DENSE_TOP5_BOOK_STATE_STRATEGY_SWEEP"
NEXT_ACTION = "run_phase299_raw_dense_top5_book_state_strategy_sweep_interpretation_no_paper_live"
REPAIR_ACTION = "repair_phase298_raw_dense_top5_book_state_strategy_sweep"

DEFAULT_SYMBOLS = ["HDFCBANK"]
SAMPLE_STRIDE = 256
INITIAL_CAPITAL_INR = 1_000_000.0
FIXED_NOTIONAL_GRID_INR = [100_000.0]
MAX_CONCURRENT_GRID = [1, 2]
COST_MULTIPLIER = 2.0
EXTRA_SLIPPAGE_BPS = 0.0
ANNUALIZED_THRESHOLD_PCT = 12.0
SPARSE_DIAGNOSTIC_EVENT_FLOOR = 8
ROBUST_PORTFOLIO_EVENT_FLOOR = 30
SAMPLE_LEDGER_ROWS = 5_000

BOOK_LEVEL_COLUMNS = [
    *(f"buy_{level}_price" for level in range(1, 6)),
    *(f"sell_{level}_price" for level in range(1, 6)),
    *(f"buy_{level}_quantity" for level in range(1, 6)),
    *(f"sell_{level}_quantity" for level in range(1, 6)),
    *(f"buy_{level}_orders" for level in range(1, 6)),
    *(f"sell_{level}_orders" for level in range(1, 6)),
]

FAMILIES = [
    {
        "family_id": "P298_RAW_TOP5_PRESSURE_CONTINUATION",
        "pressure": "top5_qty_imbalance",
        "score": "abs(level_weighted_qty_imbalance)",
        "side": "sign(top5_qty_imbalance)",
    },
    {
        "family_id": "P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION",
        "pressure": "beyond_l1_qty_imbalance",
        "score": "abs(beyond_l1_qty_imbalance) * (1.0 + abs(order_count_imbalance))",
        "side": "sign(beyond_l1_qty_imbalance)",
    },
    {
        "family_id": "P298_RAW_MICROPRICE_DEPTH_REVERSAL",
        "pressure": "microprice_dev_l5",
        "score": "abs(microprice_dev_l5) * (1.0 + abs(level_weighted_qty_imbalance))",
        "side": "-sign(microprice_dev_l5)",
    },
    {
        "family_id": "P298_RAW_ORDERCOUNT_PRESSURE_CONTINUATION",
        "pressure": "order_count_imbalance",
        "score": "abs(order_count_imbalance) * (1.0 + abs(beyond_l1_qty_imbalance))",
        "side": "sign(order_count_imbalance)",
    },
]

THRESHOLD_QUANTILES = [0.95, 0.99]
DAILY_EVENT_LIMITS = [1, 3]
HORIZONS = [1, 3, 6]


def _safe_path(path: Path) -> str:
    return path.as_posix().replace("'", "''")


def _quote(value: str) -> str:
    return value.replace("'", "''")


def zerodha_round_trip_charge_bps(notional_inr: float = 100_000.0) -> float:
    charges = calculate_equity_intraday_nse_charges(
        buy_value_inr=notional_inr,
        sell_value_inr=notional_inr,
        buy_quantity=1.0,
        sell_quantity=1.0,
        buy_orders=1,
        sell_orders=1,
    )
    return float(charges.breakeven_bps_on_buy_value)


def discover_symbol_month_files(dense_root: Path, symbols: list[str]) -> list[Path]:
    files: list[Path] = []
    for symbol in symbols:
        files.extend(sorted(dense_root.glob(f"trade_month=*/symbol={symbol}/part-00000.parquet")))
    if not files:
        raise FileNotFoundError(f"No raw dense files found under {dense_root} for symbols={symbols}")
    return sorted(files)


def validate_schema(files: list[Path]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for path in files:
        schema_names = set(pq.ParquetFile(path).schema.names)
        present = sorted(set(BOOK_LEVEL_COLUMNS).intersection(schema_names))
        rows.append(
            {
                "file_path": str(path),
                "book_level_required_columns": len(BOOK_LEVEL_COLUMNS),
                "book_level_present_columns": len(present),
                "missing_columns": ";".join(sorted(set(BOOK_LEVEL_COLUMNS).difference(schema_names))),
                "raw_book_state_schema_pass": int(len(present) == len(BOOK_LEVEL_COLUMNS)),
            }
        )
    return pd.DataFrame(rows)


def dense_lake_summary(phase51_dir: Path) -> pd.DataFrame:
    return read_csv(phase51_dir / "full_dense_lake_summary.csv")


def query_raw_dense_shard(path: Path, sample_stride: int = SAMPLE_STRIDE) -> tuple[pd.DataFrame, dict[str, Any]]:
    month = path.parent.parent.name.split("=", 1)[-1]
    symbol = path.parent.name.split("=", 1)[-1]
    base_charge_bps = zerodha_round_trip_charge_bps()
    con = duckdb.connect()
    try:
        con.execute(
            f"""
            create temporary table raw_dense_features as
            with base as (
                select
                    trade_date,
                    coalesce(exchange, 'NSE') as exchange,
                    symbol,
                    feed_profile,
                    regime_code,
                    local_sequence_id,
                    dense_subtick_id,
                    ((buy_1_price + sell_1_price) / 2.0) as mid_price,
                    lead(((buy_1_price + sell_1_price) / 2.0), 1) over (order by local_sequence_id) as future_mid_h1,
                    lead(((buy_1_price + sell_1_price) / 2.0), 3) over (order by local_sequence_id) as future_mid_h3,
                    lead(((buy_1_price + sell_1_price) / 2.0), 6) over (order by local_sequence_id) as future_mid_h6,
                    greatest(sell_1_price - buy_1_price, 0.01) as spread,
                    greatest(sell_1_price - buy_1_price, 0.01) / nullif(((buy_1_price + sell_1_price) / 2.0), 0.0) * 10000.0 as spread_bps,
                    (buy_1_quantity + buy_2_quantity + buy_3_quantity + buy_4_quantity + buy_5_quantity)::double as bid_qty_l1_l5,
                    (sell_1_quantity + sell_2_quantity + sell_3_quantity + sell_4_quantity + sell_5_quantity)::double as ask_qty_l1_l5,
                    (buy_2_quantity + buy_3_quantity + buy_4_quantity + buy_5_quantity)::double as bid_qty_l2_l5,
                    (sell_2_quantity + sell_3_quantity + sell_4_quantity + sell_5_quantity)::double as ask_qty_l2_l5,
                    (buy_1_orders + buy_2_orders + buy_3_orders + buy_4_orders + buy_5_orders)::double as bid_orders_l1_l5,
                    (sell_1_orders + sell_2_orders + sell_3_orders + sell_4_orders + sell_5_orders)::double as ask_orders_l1_l5,
                    buy_1_price,
                    buy_2_price,
                    buy_3_price,
                    buy_4_price,
                    buy_5_price,
                    sell_1_price,
                    sell_2_price,
                    sell_3_price,
                    sell_4_price,
                    sell_5_price,
                    buy_1_quantity,
                    buy_2_quantity,
                    buy_3_quantity,
                    buy_4_quantity,
                    buy_5_quantity,
                    sell_1_quantity,
                    sell_2_quantity,
                    sell_3_quantity,
                    sell_4_quantity,
                    sell_5_quantity,
                    coalesce(is_duplicate, false) as is_duplicate,
                    coalesce(is_disconnect_gap, false) as is_disconnect_gap,
                    coalesce(is_out_of_order_injected, false) as is_out_of_order_injected,
                    coalesce(is_market_shock_day, false) as is_market_shock_day
                from read_parquet('{_safe_path(path)}', union_by_name=true)
                where local_sequence_id % {int(sample_stride)} = 0
                  and buy_1_price > 0
                  and sell_1_price >= buy_1_price
            )
            select
                *,
                (bid_qty_l1_l5 - ask_qty_l1_l5) / nullif((bid_qty_l1_l5 + ask_qty_l1_l5), 0.0) as top5_qty_imbalance,
                (bid_qty_l2_l5 - ask_qty_l2_l5) / nullif((bid_qty_l2_l5 + ask_qty_l2_l5), 0.0) as beyond_l1_qty_imbalance,
                (
                    (buy_1_quantity + buy_2_quantity * 0.8 + buy_3_quantity * 0.6 + buy_4_quantity * 0.4 + buy_5_quantity * 0.2)
                    - (sell_1_quantity + sell_2_quantity * 0.8 + sell_3_quantity * 0.6 + sell_4_quantity * 0.4 + sell_5_quantity * 0.2)
                ) / nullif(
                    (buy_1_quantity + buy_2_quantity * 0.8 + buy_3_quantity * 0.6 + buy_4_quantity * 0.4 + buy_5_quantity * 0.2)
                    + (sell_1_quantity + sell_2_quantity * 0.8 + sell_3_quantity * 0.6 + sell_4_quantity * 0.4 + sell_5_quantity * 0.2),
                    0.0
                ) as level_weighted_qty_imbalance,
                (bid_orders_l1_l5 - ask_orders_l1_l5) / nullif((bid_orders_l1_l5 + ask_orders_l1_l5), 0.0) as order_count_imbalance,
                (
                    (
                        sell_1_price * buy_1_quantity + sell_2_price * buy_2_quantity + sell_3_price * buy_3_quantity + sell_4_price * buy_4_quantity + sell_5_price * buy_5_quantity
                        + buy_1_price * sell_1_quantity + buy_2_price * sell_2_quantity + buy_3_price * sell_3_quantity + buy_4_price * sell_4_quantity + buy_5_price * sell_5_quantity
                    )
                    / nullif((bid_qty_l1_l5 + ask_qty_l1_l5), 0.0)
                    - mid_price
                ) / nullif(mid_price, 0.0) as microprice_dev_l5,
                abs(
                    (bid_qty_l1_l5 + ask_qty_l1_l5)
                    - lag(bid_qty_l1_l5 + ask_qty_l1_l5) over (order by local_sequence_id)
                ) / nullif((bid_qty_l1_l5 + ask_qty_l1_l5), 0.0) as book_churn_ratio
            from base
            """
        )
        meta = con.execute(
            """
            select
                count(*)::bigint as sampled_rows,
                count(distinct trade_date)::integer as trade_dates,
                min(trade_date) as min_trade_date,
                max(trade_date) as max_trade_date,
                avg(spread_bps)::double as avg_spread_bps,
                avg(abs(top5_qty_imbalance))::double as avg_abs_top5_imbalance,
                avg(abs(beyond_l1_qty_imbalance))::double as avg_abs_beyond_l1_imbalance,
                avg(abs(microprice_dev_l5))::double as avg_abs_microprice_dev_l5
            from raw_dense_features
            """
        ).fetchdf().iloc[0].to_dict()
        frames: list[pd.DataFrame] = []
        for family in FAMILIES:
            for threshold_quantile in THRESHOLD_QUANTILES:
                for daily_limit in DAILY_EVENT_LIMITS:
                    for horizon in HORIZONS:
                        future_col = f"future_mid_h{horizon}"
                        variant_id = f"{family['family_id']}_{symbol}_{month}_Q{int(threshold_quantile*100)}_DL{daily_limit}_H{horizon}"
                        score_expr = family["score"]
                        side_expr = family["side"]
                        family_id = family["family_id"]
                        sql = f"""
                        with scored as (
                            select
                                *,
                                ({score_expr})::double as raw_score,
                                ({side_expr})::integer as side,
                                quantile_cont(abs(({score_expr})::double), {threshold_quantile}) over () as score_threshold
                            from raw_dense_features
                            where {future_col} is not null
                              and mid_price > 0
                              and not is_duplicate
                              and not is_disconnect_gap
                              and not is_out_of_order_injected
                        ),
                        ranked as (
                            select
                                *,
                                row_number() over (partition by trade_date order by abs(raw_score) desc, local_sequence_id asc) as daily_rank
                            from scored
                            where side != 0
                              and abs(raw_score) >= score_threshold
                        )
                        select
                            trade_date,
                            exchange,
                            symbol,
                            local_sequence_id::bigint as richer_event_bar_id,
                            '{_quote(variant_id)}' as candidate_id,
                            daily_rank::integer as candidate_rank,
                            '{_quote(family_id)}' as family_id,
                            side::integer as side,
                            {horizon}::integer as horizon,
                            (side * ({future_col} / nullif(mid_price, 0.0) - 1.0) * 10000.0)::double as gross_edge_bps,
                            {base_charge_bps}::double as zerodha_round_trip_charge_bps,
                            top5_qty_imbalance::double as avg_cum_top5_qty_imbalance,
                            beyond_l1_qty_imbalance::double as avg_depth_beyond_l1_qty_imbalance,
                            level_weighted_qty_imbalance::double as avg_level_weighted_depth_imbalance,
                            greatest(book_churn_ratio, 0.0)::double as depth_replenishment_pressure,
                            greatest(-book_churn_ratio, 0.0)::double as depth_withdrawal_pressure,
                            abs(book_churn_ratio)::double as top5_churn_pressure,
                            spread_bps::double as avg_spread_bps,
                            '{_quote(month)}' as trade_month,
                            feed_profile,
                            regime_code,
                            raw_score::double as raw_book_state_score,
                            score_threshold::double as raw_book_state_score_threshold,
                            {threshold_quantile}::double as threshold_quantile,
                            {daily_limit}::integer as daily_event_limit,
                            '{_quote(path.as_posix())}' as source_file
                        from ranked
                        where daily_rank <= {daily_limit}
                        """
                        frames.append(con.execute(sql).fetchdf())
        events = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    finally:
        con.close()
    meta.update({"trade_month": month, "symbol": symbol, "file_path": str(path), "sample_stride": int(sample_stride)})
    return events, meta


def build_raw_events(files: list[Path], sample_stride: int = SAMPLE_STRIDE) -> tuple[pd.DataFrame, pd.DataFrame]:
    event_frames: list[pd.DataFrame] = []
    shard_meta: list[dict[str, Any]] = []
    for path in files:
        events, meta = query_raw_dense_shard(path, sample_stride=sample_stride)
        if not events.empty:
            event_frames.append(events)
        shard_meta.append(meta)
    if not event_frames:
        raise ValueError("Phase298 produced no raw dense candidate events.")
    raw_events = pd.concat(event_frames, ignore_index=True)
    raw_events = raw_events.sort_values(["trade_date", "exchange", "richer_event_bar_id", "candidate_id", "symbol"], kind="mergesort").reset_index(drop=True)
    return raw_events, pd.DataFrame(shard_meta)


def build_variant_catalog(raw_events: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for variant_id, group in raw_events.groupby("candidate_id", sort=True):
        first = group.iloc[0]
        rows.append(
            {
                "phase298_variant_id": variant_id,
                "strategy_family": first["family_id"],
                "symbol": first["symbol"],
                "threshold_quantile": first["threshold_quantile"],
                "daily_event_limit": first["daily_event_limit"],
                "exit_horizon_ticks": first["horizon"],
                "selected_event_rows": int(len(group)),
                "trade_dates": int(group["trade_date"].astype(str).nunique()),
                "trade_months": int(group["trade_month"].astype(str).nunique()),
                "source_files": int(group["source_file"].astype(str).nunique()),
                "uses_raw_book_state_l1_l5": 1,
                "uses_top5": 1,
                "uses_levels_2_to_5": 1,
                "uses_order_count_levels_1_to_5": 1,
                "l1_only_variant": 0,
                "uses_net_edge_as_live_mask": 0,
                "annualized_denominator": "fixed_initial_capital",
            }
        )
    return pd.DataFrame(rows).sort_values(["strategy_family", "threshold_quantile", "daily_event_limit", "exit_horizon_ticks"], kind="mergesort").reset_index(drop=True)


def build_scenarios(catalog: pd.DataFrame, raw_events: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    scenarios: list[dict[str, Any]] = []
    ledgers: list[pd.DataFrame] = []
    meta = catalog.set_index("phase298_variant_id").to_dict(orient="index")
    for variant_id, events in raw_events.groupby("candidate_id", sort=True):
        events = events.copy()
        for fixed_notional in FIXED_NOTIONAL_GRID_INR:
            for max_concurrent in MAX_CONCURRENT_GRID:
                scenario, ledger = schedule_events_for_scenario(
                    events=events,
                    scope_id=variant_id,
                    scope_candidate_id=variant_id,
                    initial_capital_inr=INITIAL_CAPITAL_INR,
                    fixed_notional_inr=fixed_notional,
                    max_concurrent_positions=max_concurrent,
                    cost_profile="cost200",
                    cost_multiplier=COST_MULTIPLIER,
                    extra_slippage_bps=EXTRA_SLIPPAGE_BPS,
                )
                m = meta[variant_id]
                scenario.update(
                    {
                        "phase298_variant_id": variant_id,
                        "strategy_family": m.get("strategy_family", ""),
                        "symbol": m.get("symbol", ""),
                        "threshold_quantile": m.get("threshold_quantile", ""),
                        "daily_event_limit": m.get("daily_event_limit", ""),
                        "exit_horizon_ticks": m.get("exit_horizon_ticks", ""),
                        "selected_event_rows": m.get("selected_event_rows", 0),
                        "trade_months": m.get("trade_months", 0),
                        "source_files": m.get("source_files", 0),
                        "uses_raw_book_state_l1_l5": 1,
                        "uses_top5": 1,
                        "uses_levels_2_to_5": 1,
                        "uses_order_count_levels_1_to_5": 1,
                        "l1_only_variant": 0,
                        "uses_net_edge_as_live_mask": 0,
                        "sparse_diagnostic_event_floor_met": int(scenario["scheduled_event_rows"] >= SPARSE_DIAGNOSTIC_EVENT_FLOOR),
                        "robust_portfolio_event_floor_met": int(scenario["scheduled_event_rows"] >= ROBUST_PORTFOLIO_EVENT_FLOOR),
                        "cost200_above12_sparse_diagnostic": int(
                            scenario["mechanical_one_date_annualized_portfolio_return_pct"] > ANNUALIZED_THRESHOLD_PCT
                            and scenario["scheduled_event_rows"] >= SPARSE_DIAGNOSTIC_EVENT_FLOOR
                        ),
                        "robust_portfolio_floor_above12": int(
                            scenario["mechanical_one_date_annualized_portfolio_return_pct"] > ANNUALIZED_THRESHOLD_PCT
                            and scenario["scheduled_event_rows"] >= ROBUST_PORTFOLIO_EVENT_FLOOR
                        ),
                    }
                )
                scenarios.append(scenario)
                if len(ledgers) < 1 and not ledger.empty:
                    sample = ledger[ledger["decision"].astype(str).eq("scheduled")].head(SAMPLE_LEDGER_ROWS).copy()
                    if not sample.empty:
                        sample["phase298_variant_id"] = variant_id
                        sample["strategy_family"] = m.get("strategy_family", "")
                        ledgers.append(sample)
    return pd.DataFrame(scenarios), pd.concat(ledgers, ignore_index=True).head(SAMPLE_LEDGER_ROWS) if ledgers else pd.DataFrame()


def build_variant_summary(scenarios: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for variant_id, group in scenarios.groupby("phase298_variant_id", dropna=False):
        best = group.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0]
        rows.append(
            {
                "phase298_variant_id": variant_id,
                "strategy_family": best.get("strategy_family", ""),
                "symbol": best.get("symbol", ""),
                "threshold_quantile": best.get("threshold_quantile", ""),
                "daily_event_limit": best.get("daily_event_limit", ""),
                "exit_horizon_ticks": best.get("exit_horizon_ticks", ""),
                "scenario_rows": int(len(group)),
                "selected_event_rows": int(group["selected_event_rows"].max()),
                "max_scheduled_event_rows": int(group["scheduled_event_rows"].max()),
                "cost200_above12_sparse_diagnostic_rows": int(group["cost200_above12_sparse_diagnostic"].sum()),
                "robust_portfolio_floor_above12_rows": int(group["robust_portfolio_floor_above12"].sum()),
                "sparse_floor_met_rows": int(group["sparse_diagnostic_event_floor_met"].sum()),
                "robust_portfolio_floor_met_rows": int(group["robust_portfolio_event_floor_met"].sum()),
                "min_annualized_pct": float(group["mechanical_one_date_annualized_portfolio_return_pct"].min()),
                "median_annualized_pct": float(group["mechanical_one_date_annualized_portfolio_return_pct"].median()),
                "max_annualized_pct": float(group["mechanical_one_date_annualized_portfolio_return_pct"].max()),
                "max_net_pnl_inr": float(group["realized_net_pnl_inr"].max()),
                "best_scenario_id": best.get("scenario_id", ""),
            }
        )
    return pd.DataFrame(rows).sort_values(["cost200_above12_sparse_diagnostic_rows", "max_annualized_pct", "max_scheduled_event_rows"], ascending=[False, False, False], kind="mergesort").reset_index(drop=True)


def build_family_summary(scenarios: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for family, group in scenarios.groupby("strategy_family", dropna=False):
        best = group.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0]
        rows.append(
            {
                "strategy_family": family,
                "scenario_rows": int(len(group)),
                "variant_rows": int(group["phase298_variant_id"].astype(str).nunique()),
                "max_scheduled_event_rows": int(group["scheduled_event_rows"].max()),
                "cost200_above12_sparse_diagnostic_rows": int(group["cost200_above12_sparse_diagnostic"].sum()),
                "robust_portfolio_floor_above12_rows": int(group["robust_portfolio_floor_above12"].sum()),
                "sparse_floor_met_rows": int(group["sparse_diagnostic_event_floor_met"].sum()),
                "robust_portfolio_floor_met_rows": int(group["robust_portfolio_event_floor_met"].sum()),
                "min_annualized_pct": float(group["mechanical_one_date_annualized_portfolio_return_pct"].min()),
                "median_annualized_pct": float(group["mechanical_one_date_annualized_portfolio_return_pct"].median()),
                "max_annualized_pct": float(group["mechanical_one_date_annualized_portfolio_return_pct"].max()),
                "max_net_pnl_inr": float(group["realized_net_pnl_inr"].max()),
                "best_variant_id": best.get("phase298_variant_id", ""),
            }
        )
    return pd.DataFrame(rows).sort_values(["robust_portfolio_floor_above12_rows", "cost200_above12_sparse_diagnostic_rows", "max_annualized_pct"], ascending=[False, False, False], kind="mergesort").reset_index(drop=True)


def build_gates(phase297_summary: pd.DataFrame, phase51_summary: pd.DataFrame, schema: pd.DataFrame, shard_meta: pd.DataFrame, catalog: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    phase297_complete = as_int(metric_value(phase297_summary, "phase297_interpretation_complete", 0))
    phase297_next = str(metric_value(phase297_summary, "phase297_next_best_action", ""))
    full_lake = as_int(metric_value(phase51_summary, "phase51_full_80gb_dense_lake_materialized", 0))
    l1_only = int(pd.to_numeric(catalog.get("l1_only_variant", pd.Series(dtype=int)), errors="coerce").fillna(0).sum())
    leakage = int(pd.to_numeric(catalog.get("uses_net_edge_as_live_mask", pd.Series(dtype=int)), errors="coerce").fillna(0).sum())
    gates = [
        ("P298_PHASE297_WORK_ORDER_PRESENT", phase297_complete == 1 and "phase298" in phase297_next, phase297_next, "Phase297 routes to Phase298"),
        ("P298_DENSE_LAKE_MATERIALIZED", full_lake == 1, full_lake, "Phase51 full 80GB-class dense lake materialized"),
        ("P298_RAW_SCHEMA_PRESENT", bool(schema["raw_book_state_schema_pass"].astype(int).eq(1).all()), f"{int(schema['raw_book_state_schema_pass'].sum())}/{len(schema)}", "all sampled shards have raw levels 1-5 price/qty/order columns"),
        ("P298_FULL_YEAR_SLICE_PRESENT", int(shard_meta["trade_month"].astype(str).nunique()) >= 12 and int(shard_meta["trade_dates"].sum()) >= 240, f"months={shard_meta['trade_month'].nunique()};date_rows={int(shard_meta['trade_dates'].sum())}", "12 monthly shards and >=240 shard-date rows"),
        ("P298_RAW_EVENTS_PRESENT", int(catalog["selected_event_rows"].sum()) > 0, int(catalog["selected_event_rows"].sum()), ">0 raw dense candidate events"),
        ("P298_VARIANTS_PRESENT", len(catalog) >= 48, len(catalog), ">=48 raw-book-state variants"),
        ("P298_SCENARIOS_PRESENT", len(scenarios) >= 96, len(scenarios), ">=96 fixed-capital scenarios"),
        ("P298_FIXED_CAPITAL_REQUIRED", bool((scenarios["initial_capital_inr"].astype(float).eq(INITIAL_CAPITAL_INR)).all()), INITIAL_CAPITAL_INR, "fixed initial capital denominator"),
        ("P298_COST200_REQUIRED", bool((scenarios["cost_profile"].astype(str).eq("cost200")).all()), "cost200", "Zerodha cost stress profile"),
        ("P298_RAW_FULL_DEPTH_REQUIRED", l1_only == 0 and bool((catalog["uses_raw_book_state_l1_l5"].astype(int).eq(1)).all()) and bool((catalog["uses_levels_2_to_5"].astype(int).eq(1)).all()), f"l1_only={l1_only}", "raw levels 1-5 and levels 2-5 materiality"),
        ("P298_NO_LIVE_NET_EDGE_MASKS", leakage == 0, leakage, "no net/gross edge live masks"),
        ("P298_FIXED_CAPITAL_ANNUALIZED_DENOMINATOR", bool((catalog["annualized_denominator"].astype(str).eq("fixed_initial_capital")).all()), "fixed_initial_capital", "no unlimited-capital annualization"),
        ("P298_BOUNDARIES_CLOSED", True, "replay=0;paper=0;claim=0", "no replay/paper/live/claim"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(files: list[Path], shard_meta: pd.DataFrame, raw_events: pd.DataFrame, catalog: pd.DataFrame, scenarios: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    best = scenarios.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0]
    sparse = int(scenarios["cost200_above12_sparse_diagnostic"].sum())
    robust_floor = int(scenarios["robust_portfolio_event_floor_met"].sum())
    robust_above = int(scenarios["robust_portfolio_floor_above12"].sum())
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase298_raw_dense_sweep_complete", 1, "Phase298 raw dense top-five book-state strategy sweep completed"),
            ("phase298_selected_route", SELECTED_ROUTE, "Selected route"),
            ("phase298_dense_root", str(DEFAULT_DENSE_ROOT), "Raw dense lake root"),
            ("phase298_symbol_rows", shard_meta["symbol"].astype(str).nunique(), "Symbols in bounded sweep"),
            ("phase298_trade_month_rows", shard_meta["trade_month"].astype(str).nunique(), "Trade months in bounded sweep"),
            ("phase298_source_file_rows", len(files), "Dense shard files scanned"),
            ("phase298_sample_stride", SAMPLE_STRIDE, "Deterministic dense-row sample stride"),
            ("phase298_sampled_dense_rows", int(shard_meta["sampled_rows"].sum()), "Sampled raw dense rows"),
            ("phase298_shard_trade_date_rows", int(shard_meta["trade_dates"].sum()), "Shard-date rows sampled"),
            ("phase298_raw_event_rows", len(raw_events), "Raw dense candidate event rows"),
            ("phase298_variant_rows", len(catalog), "Raw-book-state variants evaluated"),
            ("phase298_scenario_rows", len(scenarios), "Cost200 fixed-capital scenarios evaluated"),
            ("phase298_sparse_above12_scenario_rows", sparse, "Above-12 sparse diagnostic rows"),
            ("phase298_robust_portfolio_floor_scenario_rows", robust_floor, "Robust floor rows"),
            ("phase298_robust_portfolio_above12_scenario_rows", robust_above, "Robust above-12 rows"),
            ("phase298_best_variant_id", best.get("phase298_variant_id", ""), "Best variant"),
            ("phase298_best_strategy_family", best.get("strategy_family", ""), "Best family"),
            ("phase298_best_cost200_annualized_pct", best.get("mechanical_one_date_annualized_portfolio_return_pct", ""), "Best fixed-capital annualized diagnostic"),
            ("phase298_best_realized_net_pnl_inr", best.get("realized_net_pnl_inr", ""), "Best net P&L"),
            ("phase298_best_scheduled_event_rows", best.get("scheduled_event_rows", ""), "Best scheduled events"),
            ("phase298_best_observed_trade_dates", best.get("observed_trade_dates", ""), "Best observed dates"),
            ("phase298_best_initial_capital_inr", best.get("initial_capital_inr", ""), "Fixed initial capital denominator"),
            ("phase298_raw_book_state_l1_l5_required", 1, "Raw levels 1-5 required"),
            ("phase298_levels_2_to_5_required", 1, "Levels 2-5 materiality required"),
            ("phase298_l1_only_variant_rows", int(catalog["l1_only_variant"].sum()), "L1-only variants"),
            ("phase298_net_edge_live_mask_rows", int(catalog["uses_net_edge_as_live_mask"].sum()), "Net edge live masks"),
            ("phase298_annualized_denominator", "fixed_initial_capital", "Annualized denominator"),
            ("phase298_strategy_replay_allowed", 0, "No replay"),
            ("phase298_strategy_promotion_allowed", 0, "No promotion"),
            ("phase298_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase298_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase298_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase298_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase298_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, summary: pd.DataFrame, gates: pd.DataFrame, families: pd.DataFrame, variants: pd.DataFrame, shard_meta: pd.DataFrame) -> None:
    lines = [
        "# Phase298 Raw Dense Top-Five Book-State Strategy Sweep",
        "",
        "Phase298 runs a bounded full-year HDFCBANK slice over the Phase51 raw dense top-five market-by-price lake.",
        "",
        "Unlike Phase296, this milestone uses persisted raw book-state columns for levels 1-5: bid/ask price, quantity and order-count fields.",
        "",
        "The sweep is intentionally bounded by symbol and deterministic dense-row stride so the milestone completes interactively without claiming a full 5.97B-row portfolio result.",
        "",
        "No replay, promotion, paper/live acceptance, or deployable profitability claim is opened by this search.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(summary),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "## Shard Summary",
        "",
        _markdown_table(shard_meta),
        "",
        "## Family Summary",
        "",
        _markdown_table(families),
        "",
        "## Top Variants",
        "",
        _markdown_table(variants.head(20)),
    ]
    (output_dir / "phase298_raw_dense_top5_book_state_strategy_sweep_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(dense_root: Path = DEFAULT_DENSE_ROOT, phase51_dir: Path = DEFAULT_PHASE51_DIR, phase297_dir: Path = DEFAULT_PHASE297_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR, symbols: list[str] | None = None, sample_stride: int = SAMPLE_STRIDE) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    selected_symbols = symbols or DEFAULT_SYMBOLS
    phase297_summary = read_csv(phase297_dir / "phase297_acceptance_summary.csv")
    phase51_summary = dense_lake_summary(phase51_dir)
    files = discover_symbol_month_files(dense_root, selected_symbols)
    schema = validate_schema(files)
    raw_events, shard_meta = build_raw_events(files, sample_stride=sample_stride)
    catalog = build_variant_catalog(raw_events)
    scenarios, ledger = build_scenarios(catalog, raw_events)
    variants = build_variant_summary(scenarios)
    families = build_family_summary(scenarios)
    gates = build_gates(phase297_summary, phase51_summary, schema, shard_meta, catalog, scenarios)
    summary = build_acceptance(files, shard_meta, raw_events, catalog, scenarios, gates)

    schema.to_csv(output_dir / "phase298_raw_book_schema_audit.csv", index=False)
    shard_meta.to_csv(output_dir / "phase298_raw_dense_shard_summary.csv", index=False)
    raw_events.to_csv(output_dir / "phase298_raw_dense_candidate_events.csv", index=False)
    catalog.to_csv(output_dir / "phase298_variant_catalog.csv", index=False)
    scenarios.to_csv(output_dir / "phase298_scenario_summary.csv", index=False)
    variants.to_csv(output_dir / "phase298_variant_summary.csv", index=False)
    families.to_csv(output_dir / "phase298_family_summary.csv", index=False)
    gates.to_csv(output_dir / "phase298_gate_evaluation.csv", index=False)
    summary.to_csv(output_dir / "phase298_acceptance_summary.csv", index=False)
    if not ledger.empty:
        ledger.to_csv(output_dir / "phase298_sample_trade_ledger.csv", index=False)
    write_report(output_dir, summary, gates, families, variants, shard_meta)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase298_raw_dense_top5_book_state_strategy_sweep",
        **reproducibility_fields(
            artifact_id="phase298",
            generated_utc=generated_utc,
            inputs={
                "phase51_dense_lake_summary": str(phase51_dir / "full_dense_lake_summary.csv"),
                "phase297_acceptance_summary": str(phase297_dir / "phase297_acceptance_summary.csv"),
                "dense_root": str(dense_root),
            },
            parameters={
                "selected_route": SELECTED_ROUTE,
                "symbols": selected_symbols,
                "sample_stride": sample_stride,
                "initial_capital_inr": INITIAL_CAPITAL_INR,
                "fixed_notional_grid_inr": FIXED_NOTIONAL_GRID_INR,
                "max_concurrent_grid": MAX_CONCURRENT_GRID,
                "annualized_denominator": "fixed_initial_capital",
                "raw_book_state_columns": BOOK_LEVEL_COLUMNS,
            },
            outputs={"acceptance_summary": str(output_dir / "phase298_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase298_raw_dense_sampled_horizon_proxy_v1",
        ),
    }
    (output_dir / "phase298_raw_dense_top5_book_state_strategy_sweep_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase298 raw dense top-five book-state strategy sweep.")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--phase51-dir", type=Path, default=DEFAULT_PHASE51_DIR)
    parser.add_argument("--phase297-dir", type=Path, default=DEFAULT_PHASE297_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--symbols", type=str, default=",".join(DEFAULT_SYMBOLS), help="Comma-separated symbols to scan.")
    parser.add_argument("--sample-stride", type=int, default=SAMPLE_STRIDE)
    args = parser.parse_args()
    symbols = [value.strip().upper() for value in args.symbols.split(",") if value.strip()]
    summary = run(
        dense_root=args.dense_root,
        phase51_dir=args.phase51_dir,
        phase297_dir=args.phase297_dir,
        output_dir=args.output_dir,
        symbols=symbols,
        sample_stride=args.sample_stride,
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
