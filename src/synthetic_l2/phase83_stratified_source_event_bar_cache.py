from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase61_lower_frequency_candidate_sweep import _safe_path
from synthetic_l2.phase70_cross_symbol_lead_lag_labels import symbol_universe
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase83")
DEFAULT_PHASE81_DIR = Path("outputs/phase81")
DEFAULT_COMPACT_ROOT = Path("raw_synthetic_l2_full_year_compact_monthly")
DEFAULT_BAR_SOURCE_EVENTS = 10


def load_selected_dates(phase81_dir: Path) -> pd.DataFrame:
    path = phase81_dir / "stratified_selected_source_dates.csv"
    if not path.exists():
        raise FileNotFoundError(path)
    selected = pd.read_csv(path)
    return selected.rename(columns={"selected_trade_date": "trade_date", "selected_regime_code": "regime_code"})


def build_bar_cache(compact_root: Path, selected_dates: pd.DataFrame, bar_source_events: int) -> pd.DataFrame:
    pattern = (compact_root / "**" / "*.parquet").as_posix().replace("'", "''")
    con = duckdb.connect()
    try:
        con.register("selected_dates", selected_dates[["trade_month", "trade_date", "regime_code"]].drop_duplicates())
        sql = f"""
        with source as (
            select
                substr(cast(c.trade_date as varchar), 1, 7) as trade_month,
                cast(c.trade_date as varchar) as trade_date,
                c.feed_profile,
                c.symbol,
                c.source_sequence,
                c.callback_received_utc_ms,
                c.regime_code,
                c.is_market_shock_day,
                c.is_symbol_shock,
                ((c.buy_1_price + c.sell_1_price) / 2.0)::double as mid_price,
                greatest(c.sell_1_price - c.buy_1_price, 0.01)::double as spread,
                ((c.buy_1_quantity - c.sell_1_quantity) / nullif((c.buy_1_quantity + c.sell_1_quantity), 0.0))::double as l1_imbalance,
                (
                    (
                        (c.buy_1_quantity + c.buy_2_quantity + c.buy_3_quantity + c.buy_4_quantity + c.buy_5_quantity)
                        - (c.sell_1_quantity + c.sell_2_quantity + c.sell_3_quantity + c.sell_4_quantity + c.sell_5_quantity)
                    )
                    / nullif(
                        (
                            c.buy_1_quantity + c.buy_2_quantity + c.buy_3_quantity + c.buy_4_quantity + c.buy_5_quantity
                            + c.sell_1_quantity + c.sell_2_quantity + c.sell_3_quantity + c.sell_4_quantity + c.sell_5_quantity
                        ),
                        0.0
                    )
                )::double as l5_imbalance,
                ((c.buy_1_price * c.sell_1_quantity + c.sell_1_price * c.buy_1_quantity) / nullif((c.buy_1_quantity + c.sell_1_quantity), 0.0))::double as microprice_l1,
                c.last_traded_quantity::double as event_intensity_proxy
            from read_parquet('{pattern}', union_by_name=true) c
            join selected_dates s
              on substr(cast(c.trade_date as varchar), 1, 7) = s.trade_month
             and cast(c.trade_date as varchar) = s.trade_date
             and c.regime_code = s.regime_code
            where c.buy_1_price > 0
              and c.sell_1_price > 0
              and c.sell_1_price >= c.buy_1_price
              and not coalesce(c.is_duplicate, false)
              and not coalesce(c.is_disconnect_gap, false)
              and not coalesce(c.is_out_of_order_injected, false)
        ),
        ordered as (
            select
                *,
                row_number() over (
                    partition by trade_month, trade_date, feed_profile, symbol
                    order by source_sequence
                ) as source_event_ordinal
            from source
        ),
        bars as (
            select
                trade_month,
                trade_date,
                feed_profile,
                symbol,
                regime_code,
                {int(bar_source_events)}::integer as bar_source_events,
                floor((source_event_ordinal - 1) / {int(bar_source_events)})::integer as source_event_bar_id,
                count(*)::bigint as source_events_in_bar,
                min(source_sequence)::bigint as first_source_sequence,
                max(source_sequence)::bigint as last_source_sequence,
                min(callback_received_utc_ms)::bigint as first_callback_received_utc_ms,
                max(callback_received_utc_ms)::bigint as last_callback_received_utc_ms,
                first(mid_price order by source_sequence)::double as open_mid_price,
                last(mid_price order by source_sequence)::double as close_mid_price,
                avg(spread)::double as avg_spread,
                avg(l1_imbalance)::double as avg_l1_imbalance,
                avg(l5_imbalance)::double as avg_l5_imbalance,
                avg((microprice_l1 - mid_price) / nullif(mid_price, 0.0))::double as avg_microprice_dev,
                avg(event_intensity_proxy)::double as avg_event_intensity_proxy,
                max(case when coalesce(is_market_shock_day, false) then 1 else 0 end)::integer as is_market_shock_bar,
                max(case when coalesce(is_symbol_shock, false) then 1 else 0 end)::integer as is_symbol_shock_bar
            from ordered
            group by trade_month, trade_date, feed_profile, symbol, regime_code, floor((source_event_ordinal - 1) / {int(bar_source_events)})
            having count(*) >= greatest(2, {int(bar_source_events)} * 0.50)
        )
        select
            *,
            close_mid_price / nullif(open_mid_price, 0.0) - 1.0 as bar_return
        from bars
        order by trade_month, trade_date, feed_profile, symbol, source_event_bar_id
        """
        bars = con.execute(sql).fetchdf()
    finally:
        con.close()
    if bars.empty:
        return bars
    bars["next_bar_return"] = (
        bars.groupby(["trade_month", "trade_date", "feed_profile", "symbol"], sort=False)["close_mid_price"].shift(-1)
        / bars["close_mid_price"].replace(0, np.nan)
        - 1.0
    )
    return bars


def coverage_summary(bars: pd.DataFrame) -> pd.DataFrame:
    if bars.empty:
        return pd.DataFrame()
    expected_symbols = len(symbol_universe())
    coverage = (
        bars.groupby(["trade_month", "trade_date", "feed_profile", "source_event_bar_id"], sort=True)
        .agg(
            symbols_present=("symbol", "nunique"),
            total_source_events=("source_events_in_bar", "sum"),
            min_source_events_in_bar=("source_events_in_bar", "min"),
            regimes=("regime_code", "nunique"),
            market_shock_bar=("is_market_shock_bar", "max"),
            symbol_shock_symbols=("is_symbol_shock_bar", "sum"),
        )
        .reset_index()
    )
    coverage["expected_symbols"] = expected_symbols
    coverage["coverage_fraction"] = coverage["symbols_present"] / float(expected_symbols)
    coverage["coverage_pass"] = coverage["coverage_fraction"].ge(0.95)
    return coverage


def monthly_summary(bars: pd.DataFrame, coverage: pd.DataFrame) -> pd.DataFrame:
    if bars.empty:
        return pd.DataFrame()
    rows = []
    for month, group in bars.groupby("trade_month", sort=True):
        month_coverage = coverage[coverage["trade_month"].eq(month)]
        rows.append(
            {
                "trade_month": month,
                "bar_rows": int(len(group)),
                "trade_dates": int(group["trade_date"].nunique()),
                "feed_profiles": int(group["feed_profile"].nunique()),
                "regime_codes": int(group["regime_code"].nunique()),
                "symbols": int(group["symbol"].nunique()),
                "coverage_bucket_rows": int(len(month_coverage)),
                "coverage_pass_fraction": float(month_coverage["coverage_pass"].mean()) if not month_coverage.empty else 0.0,
                "median_symbols_present": float(month_coverage["symbols_present"].median()) if not month_coverage.empty else 0.0,
                "market_shock_buckets": int(month_coverage["market_shock_bar"].sum()) if not month_coverage.empty else 0,
                "symbol_shock_symbol_bars": int(group["is_symbol_shock_bar"].sum()),
            }
        )
    return pd.DataFrame(rows)


def core_bar_cache(bars: pd.DataFrame, coverage: pd.DataFrame) -> pd.DataFrame:
    if bars.empty or coverage.empty:
        return pd.DataFrame()
    keys = coverage.loc[
        coverage["coverage_pass"].astype(bool),
        ["trade_month", "trade_date", "feed_profile", "source_event_bar_id"],
    ].copy()
    return bars.merge(keys, on=["trade_month", "trade_date", "feed_profile", "source_event_bar_id"], how="inner")


def summarize(raw_bars: pd.DataFrame, bars: pd.DataFrame, monthly: pd.DataFrame, coverage: pd.DataFrame, elapsed: float) -> pd.DataFrame:
    months = int(monthly["trade_month"].nunique()) if not monthly.empty else 0
    pass_fraction = float(monthly["coverage_pass_fraction"].mean()) if not monthly.empty else 0.0
    min_month_pass = float(monthly["coverage_pass_fraction"].min()) if not monthly.empty else 0.0
    cache_pass = bool(months == 12 and min_month_pass >= 0.95 and int(monthly["symbols"].min()) == len(symbol_universe()))
    retained_fraction = float(len(bars) / len(raw_bars)) if len(raw_bars) else 0.0
    return pd.DataFrame(
        [
            ("phase83_raw_candidate_bar_rows", int(len(raw_bars)), "Raw stratified source-event bars before core coverage trimming"),
            ("phase83_cached_bar_rows", int(len(bars)), "Stratified source-event bars materialized"),
            ("phase83_core_bar_retained_fraction", retained_fraction, "Fraction of raw candidate bars retained after core coverage trimming"),
            ("phase83_months_cached", months, "Months represented in cached bars"),
            ("phase83_coverage_bucket_rows", int(len(coverage)), "Cross-symbol event-bar coverage rows"),
            ("phase83_mean_monthly_coverage_pass_fraction", pass_fraction, "Mean monthly coverage pass fraction"),
            ("phase83_min_monthly_coverage_pass_fraction", min_month_pass, "Worst monthly coverage pass fraction"),
            ("phase83_stratified_bar_cache_pass", int(cache_pass), "1 means cache is ready for full stratified replay"),
            ("phase83_elapsed_seconds", elapsed, "Elapsed seconds"),
            (
                "phase83_recommend_next_action",
                "rerun_hdfcbank_on_cached_stratified_event_bars" if cache_pass else "fix_source_event_bar_cache_coverage",
                "Recommended next milestone",
            ),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase83 Stratified Source-Event Bar Cache",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase83 materializes reusable source-event aligned bars for the Phase81 stratified windows.",
        "This repairs the Phase82 timestamp-bucket coverage issue by aligning on per-symbol source-event ordinal inside each selected source day and feed profile.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase83_stratified_source_event_bar_cache_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase83(compact_root: Path, phase81_dir: Path, output_dir: Path, base_dir: Path, bar_source_events: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    selected = load_selected_dates(phase81_dir)
    raw_bars = build_bar_cache(compact_root, selected, bar_source_events)
    raw_coverage = coverage_summary(raw_bars)
    bars = core_bar_cache(raw_bars, raw_coverage)
    coverage = coverage_summary(bars)
    monthly = monthly_summary(bars, coverage)
    elapsed = time.perf_counter() - started
    acceptance = summarize(raw_bars, bars, monthly, coverage, elapsed)

    pq.write_table(pa.Table.from_pandas(bars, preserve_index=False), output_dir / "stratified_source_event_bars.parquet", compression="zstd")
    raw_coverage.to_csv(output_dir / "stratified_source_event_bar_raw_coverage.csv", index=False)
    selected.to_csv(output_dir / "selected_source_dates_used.csv", index=False)
    coverage.to_csv(output_dir / "stratified_source_event_bar_coverage.csv", index=False)
    monthly.to_csv(output_dir / "stratified_source_event_bar_monthly_summary.csv", index=False)
    acceptance.to_csv(output_dir / "stratified_source_event_bar_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Monthly Summary": monthly,
            "Coverage Sample": coverage.head(120),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase83_stratified_source_event_bar_cache",
        "stratified_bar_cache_pass": int(
            acceptance.loc[acceptance["metric"].eq("phase83_stratified_bar_cache_pass"), "value"].iloc[0]
        ),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase83",
            generated_utc=generated_utc,
            inputs={
                "compact_monthly_raw_lake": str(compact_root),
                "phase81_selected_source_dates": str(phase81_dir / "stratified_selected_source_dates.csv"),
            },
            parameters={
                "bar_source_events": bar_source_events,
                "alignment": "per_symbol_source_event_ordinal_within_trade_date_feed_profile",
                "coverage_gate": "all_12_months_min_monthly_coverage_pass_fraction_ge_0_95",
            },
            outputs={
                "bar_cache": str(output_dir / "stratified_source_event_bars.parquet"),
                "coverage": str(output_dir / "stratified_source_event_bar_coverage.csv"),
                "monthly_summary": str(output_dir / "stratified_source_event_bar_monthly_summary.csv"),
                "acceptance_summary": str(output_dir / "stratified_source_event_bar_acceptance_summary.csv"),
                "report": str(output_dir / "phase83_stratified_source_event_bar_cache_report.md"),
                "manifest": str(output_dir / "phase83_stratified_source_event_bar_cache_manifest.json"),
            },
            random_seed="none_deterministic_source_event_bar_cache",
            scenario_ids="phase83_phase81_stratified_source_event_bars",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase83_source_event_ordinal_alignment",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase83_stratified_source_event_bar_cache_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize stratified source-event aligned bar cache.")
    parser.add_argument("--compact-root", type=Path, default=DEFAULT_COMPACT_ROOT)
    parser.add_argument("--phase81-dir", type=Path, default=DEFAULT_PHASE81_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--bar-source-events", type=int, default=DEFAULT_BAR_SOURCE_EVENTS)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase83(args.compact_root, args.phase81_dir, args.output_dir, args.base_dir, args.bar_source_events)


if __name__ == "__main__":
    main()
