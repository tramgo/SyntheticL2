from __future__ import annotations

import argparse
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase56_cost_clearing_label_discovery import DEFAULT_DENSE_ROOT
from synthetic_l2.phase61_lower_frequency_candidate_sweep import _safe_path
from synthetic_l2.phase70_cross_symbol_lead_lag_labels import symbol_universe
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase79")
DEFAULT_MAX_ROWS_PER_SYMBOL = 250_000
DEFAULT_CORR_BAR_EVENTS = 25_000


def monthly_files(dense_root: Path) -> list[Path]:
    files = sorted(dense_root.glob("trade_month=*/symbol=*/part-00000.parquet"))
    if not files:
        raise FileNotFoundError(f"No dense parquet files found under {dense_root}")
    return files


def path_parts(path: Path) -> tuple[str, str]:
    trade_month = path.parent.parent.name.replace("trade_month=", "")
    symbol = path.parent.name.replace("symbol=", "")
    return trade_month, symbol


def entropy(counts: pd.Series) -> float:
    values = counts.astype(float)
    total = float(values.sum())
    if total <= 0:
        return 0.0
    probs = values[values > 0] / total
    return float(-(probs * np.log2(probs)).sum())


def query_partition_profile(path: Path, max_rows_per_symbol: int | None, corr_bar_events: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    filter_sql = """
        buy_1_price > 0
        and sell_1_price > 0
        and sell_1_price >= buy_1_price
    """
    if max_rows_per_symbol is not None:
        filter_sql += f" and local_sequence_id <= {int(max_rows_per_symbol)}"
    con = duckdb.connect()
    try:
        sql = f"""
        with base as (
            select
                trade_month,
                trade_date,
                symbol,
                local_sequence_id,
                regime_code,
                feed_profile,
                is_market_shock_day,
                is_symbol_shock,
                coalesce(is_duplicate, false) as is_duplicate,
                coalesce(is_disconnect_gap, false) as is_disconnect_gap,
                coalesce(is_out_of_order_injected, false) as is_out_of_order_injected,
                ((buy_1_price + sell_1_price) / 2.0)::double as mid_price,
                greatest(sell_1_price - buy_1_price, 0.01)::double as spread,
                (buy_1_quantity + sell_1_quantity)::double as l1_depth,
                (buy_1_quantity + sell_1_quantity + buy_2_quantity + sell_2_quantity + buy_3_quantity + sell_3_quantity + buy_4_quantity + sell_4_quantity + buy_5_quantity + sell_5_quantity)::double as l5_depth
            from read_parquet('{_safe_path(path)}', union_by_name=true)
            where {filter_sql}
        ),
        stats as (
            select
                any_value(trade_month)::varchar as trade_month,
                any_value(trade_date)::varchar as trade_date,
                any_value(symbol)::varchar as symbol,
                count(*)::bigint as rows_scanned,
                count(distinct regime_code)::integer as regime_count,
                count(distinct feed_profile)::integer as feed_profile_count,
                sum(case when is_market_shock_day then 1 else 0 end)::bigint as market_shock_rows,
                sum(case when is_symbol_shock then 1 else 0 end)::bigint as symbol_shock_rows,
                avg(case when is_duplicate then 1.0 else 0.0 end)::double as duplicate_rate,
                avg(case when is_disconnect_gap then 1.0 else 0.0 end)::double as disconnect_gap_rate,
                avg(case when is_out_of_order_injected then 1.0 else 0.0 end)::double as out_of_order_rate,
                avg(spread / nullif(mid_price, 0.0) * 10000.0)::double as mean_spread_bps,
                quantile_cont(spread / nullif(mid_price, 0.0) * 10000.0, 0.50)::double as median_spread_bps,
                quantile_cont(spread / nullif(mid_price, 0.0) * 10000.0, 0.90)::double as p90_spread_bps,
                avg(l1_depth)::double as mean_l1_depth,
                avg(l5_depth)::double as mean_l5_depth,
                stddev_samp(mid_price / nullif(lag_mid_price, 0.0) - 1.0)::double as one_tick_return_std
            from (
                select *, lag(mid_price) over (order by local_sequence_id) as lag_mid_price
                from base
            )
        )
        select * from stats
        """
        profile = con.execute(sql).fetchdf()
        bar_sql = f"""
        with base as (
            select
                trade_month,
                trade_date,
                symbol,
                floor((local_sequence_id - 1) / {int(corr_bar_events)})::integer as bar_id,
                local_sequence_id,
                ((buy_1_price + sell_1_price) / 2.0)::double as mid_price
            from read_parquet('{_safe_path(path)}', union_by_name=true)
            where {filter_sql}
        ),
        bars as (
            select
                any_value(trade_month)::varchar as trade_month,
                any_value(trade_date)::varchar as trade_date,
                any_value(symbol)::varchar as symbol,
                bar_id,
                first(mid_price order by local_sequence_id)::double as open_mid_price,
                last(mid_price order by local_sequence_id)::double as close_mid_price,
                count(*)::bigint as rows_in_bar
            from base
            group by bar_id
            having count(*) >= greatest(10, {int(corr_bar_events)} * 0.50)
        )
        select
            trade_month,
            trade_date,
            symbol,
            bar_id,
            close_mid_price / nullif(open_mid_price, 0.0) - 1.0 as bar_return,
            rows_in_bar
        from bars
        """
        bars = con.execute(bar_sql).fetchdf()
        return profile, bars
    finally:
        con.close()


def partition_count_tables(profiles: pd.DataFrame, files: list[Path], max_rows_per_symbol: int | None) -> tuple[pd.DataFrame, pd.DataFrame]:
    regime_rows: list[pd.DataFrame] = []
    feed_rows: list[pd.DataFrame] = []
    filter_sql = "buy_1_price > 0 and sell_1_price > 0 and sell_1_price >= buy_1_price"
    if max_rows_per_symbol is not None:
        filter_sql += f" and local_sequence_id <= {int(max_rows_per_symbol)}"
    con = duckdb.connect()
    try:
        for path in files:
            sql_regime = f"""
            select
                any_value(trade_month)::varchar as trade_month,
                any_value(symbol)::varchar as symbol,
                regime_code,
                count(*)::bigint as rows
            from read_parquet('{_safe_path(path)}', union_by_name=true)
            where {filter_sql}
            group by regime_code
            """
            sql_feed = f"""
            select
                any_value(trade_month)::varchar as trade_month,
                any_value(symbol)::varchar as symbol,
                feed_profile,
                count(*)::bigint as rows
            from read_parquet('{_safe_path(path)}', union_by_name=true)
            where {filter_sql}
            group by feed_profile
            """
            regime_rows.append(con.execute(sql_regime).fetchdf())
            feed_rows.append(con.execute(sql_feed).fetchdf())
    finally:
        con.close()
    return (
        pd.concat(regime_rows, ignore_index=True) if regime_rows else pd.DataFrame(),
        pd.concat(feed_rows, ignore_index=True) if feed_rows else pd.DataFrame(),
    )


def monthly_diversity(profiles: pd.DataFrame, regime_counts: pd.DataFrame, feed_counts: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for month, group in profiles.groupby("trade_month", sort=True):
        regimes = regime_counts[regime_counts["trade_month"].eq(month)]
        feeds = feed_counts[feed_counts["trade_month"].eq(month)]
        regime_total = regimes.groupby("regime_code", sort=True)["rows"].sum()
        feed_total = feeds.groupby("feed_profile", sort=True)["rows"].sum()
        spread_cv = float(group["mean_spread_bps"].std(ddof=1) / group["mean_spread_bps"].mean()) if float(group["mean_spread_bps"].mean() or 0.0) > 0 else 0.0
        rows.append(
            {
                "trade_month": month,
                "symbols": int(group["symbol"].nunique()),
                "rows_scanned": int(group["rows_scanned"].sum()),
                "regime_codes": int(regime_total.shape[0]),
                "regime_entropy_bits": entropy(regime_total),
                "feed_profiles": int(feed_total.shape[0]),
                "feed_profile_entropy_bits": entropy(feed_total),
                "market_shock_symbols": int((group["market_shock_rows"] > 0).sum()),
                "symbol_shock_symbols": int((group["symbol_shock_rows"] > 0).sum()),
                "mean_duplicate_rate": float(group["duplicate_rate"].mean()),
                "mean_disconnect_gap_rate": float(group["disconnect_gap_rate"].mean()),
                "mean_out_of_order_rate": float(group["out_of_order_rate"].mean()),
                "median_symbol_spread_bps": float(group["median_spread_bps"].median()),
                "spread_cross_symbol_cv": spread_cv,
                "median_symbol_l1_depth": float(group["mean_l1_depth"].median()),
                "median_symbol_one_tick_return_std": float(group["one_tick_return_std"].median()),
            }
        )
    return pd.DataFrame(rows)


def correlation_diversity(bars: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if bars.empty:
        return pd.DataFrame()
    for month, group in bars.groupby("trade_month", sort=True):
        pivot = group.pivot_table(index="bar_id", columns="symbol", values="bar_return", aggfunc="mean")
        corr = pivot.corr(min_periods=3)
        values = corr.where(~np.eye(corr.shape[0], dtype=bool)).stack().astype(float)
        rows.append(
            {
                "trade_month": month,
                "symbols_in_corr": int(corr.shape[0]),
                "bar_rows": int(pivot.shape[0]),
                "corr_pair_count": int(values.shape[0]),
                "mean_pair_corr": float(values.mean()) if not values.empty else np.nan,
                "median_pair_corr": float(values.median()) if not values.empty else np.nan,
                "std_pair_corr": float(values.std(ddof=1)) if values.shape[0] > 1 else 0.0,
                "min_pair_corr": float(values.min()) if not values.empty else np.nan,
                "max_pair_corr": float(values.max()) if not values.empty else np.nan,
                "negative_corr_fraction": float((values < 0).mean()) if not values.empty else 0.0,
            }
        )
    return pd.DataFrame(rows)


def acceptance_summary(monthly: pd.DataFrame, corr: pd.DataFrame, profiles: pd.DataFrame) -> pd.DataFrame:
    months = int(monthly["trade_month"].nunique()) if not monthly.empty else 0
    expected_symbols = len(symbol_universe())
    complete_month_fraction = float((monthly["symbols"] >= expected_symbols).mean()) if not monthly.empty else 0.0
    min_regime_codes = int(monthly["regime_codes"].min()) if not monthly.empty else 0
    median_regime_entropy = float(monthly["regime_entropy_bits"].median()) if not monthly.empty else 0.0
    min_feed_profiles = int(monthly["feed_profiles"].min()) if not monthly.empty else 0
    market_shock_months = int((monthly["market_shock_symbols"] >= expected_symbols * 0.75).sum()) if not monthly.empty else 0
    symbol_shock_months = int((monthly["symbol_shock_symbols"] > 0).sum()) if not monthly.empty else 0
    median_spread_cv = float(monthly["spread_cross_symbol_cv"].median()) if not monthly.empty else 0.0
    corr_months = int(corr["trade_month"].nunique()) if not corr.empty else 0
    median_corr_std = float(corr["std_pair_corr"].median()) if not corr.empty else 0.0
    negative_corr_months = int((corr["negative_corr_fraction"] > 0.05).sum()) if not corr.empty else 0
    generator_diversity_pass = bool(
        months >= 12
        and complete_month_fraction >= 1.0
        and min_regime_codes >= 4
        and median_regime_entropy >= 1.0
        and min_feed_profiles >= 2
        and market_shock_months >= 1
        and symbol_shock_months >= 6
        and median_spread_cv >= 0.05
        and corr_months >= 12
        and median_corr_std >= 0.05
    )
    return pd.DataFrame(
        [
            ("phase79_months_audited", months, "Distinct synthetic months audited"),
            ("phase79_complete_month_fraction", complete_month_fraction, "Fraction of months with all expected symbols"),
            ("phase79_min_regime_codes_per_month", min_regime_codes, "Minimum distinct regime codes in any month"),
            ("phase79_median_regime_entropy_bits", median_regime_entropy, "Median monthly regime entropy"),
            ("phase79_min_feed_profiles_per_month", min_feed_profiles, "Minimum feed-profile count in any month"),
            ("phase79_market_shock_months", market_shock_months, "Months where market shock flag appears broadly across symbols"),
            ("phase79_symbol_shock_months", symbol_shock_months, "Months with at least one symbol shock"),
            ("phase79_median_spread_cross_symbol_cv", median_spread_cv, "Median monthly cross-symbol coefficient of variation for mean spread bps"),
            ("phase79_corr_months", corr_months, "Months with cross-symbol correlation diagnostics"),
            ("phase79_median_corr_pair_std", median_corr_std, "Median monthly standard deviation of pairwise correlations"),
            ("phase79_negative_corr_months", negative_corr_months, "Months with more than 5 percent negative pair correlations"),
            ("phase79_generator_scenario_diversity_pass", int(generator_diversity_pass), "1 means generator diversity gate passes"),
            (
                "phase79_recommend_next_action",
                "P80_cost_budget_signal_design" if generator_diversity_pass else "generator_scenario_recalibration_before_new_strategy_mining",
                "Recommended next milestone",
            ),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase79 Generator Scenario Diversity Audit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase79 audits whether the dense synthetic year has enough regime, shock, feed-imperfection, spread and correlation diversity to support strategy falsification.",
        "The audit samples a bounded prefix per symbol partition and is not a profitability claim.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase79_generator_scenario_diversity_audit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase79(
    dense_root: Path,
    output_dir: Path,
    base_dir: Path,
    max_rows_per_symbol: int | None,
    corr_bar_events: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    files = monthly_files(dense_root)
    profile_frames: list[pd.DataFrame] = []
    bar_frames: list[pd.DataFrame] = []
    inventory = []
    for path in files:
        trade_month, symbol = path_parts(path)
        profile, bars = query_partition_profile(path, max_rows_per_symbol, corr_bar_events)
        profile_frames.append(profile)
        if not bars.empty:
            bar_frames.append(bars)
        inventory.append({"trade_month": trade_month, "symbol": symbol, "path": str(path)})

    profiles = pd.concat(profile_frames, ignore_index=True) if profile_frames else pd.DataFrame()
    bars = pd.concat(bar_frames, ignore_index=True) if bar_frames else pd.DataFrame()
    regime_counts, feed_counts = partition_count_tables(profiles, files, max_rows_per_symbol)
    monthly = monthly_diversity(profiles, regime_counts, feed_counts)
    corr = correlation_diversity(bars)
    acceptance = acceptance_summary(monthly, corr, profiles)
    elapsed = time.perf_counter() - started
    acceptance.loc[len(acceptance)] = ("phase79_elapsed_seconds", elapsed, "Elapsed seconds")

    pd.DataFrame(inventory).to_csv(output_dir / "generator_file_inventory.csv", index=False)
    profiles.to_csv(output_dir / "partition_scenario_profile.csv", index=False)
    regime_counts.to_csv(output_dir / "regime_code_counts.csv", index=False)
    feed_counts.to_csv(output_dir / "feed_profile_counts.csv", index=False)
    monthly.to_csv(output_dir / "monthly_scenario_diversity.csv", index=False)
    corr.to_csv(output_dir / "monthly_correlation_diversity.csv", index=False)
    acceptance.to_csv(output_dir / "generator_scenario_diversity_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Monthly Scenario Diversity": monthly,
            "Monthly Correlation Diversity": corr,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase79_generator_scenario_diversity_audit",
        "generator_scenario_diversity_pass": int(
            acceptance.loc[acceptance["metric"].eq("phase79_generator_scenario_diversity_pass"), "value"].iloc[0]
        ),
        "elapsed_seconds": elapsed,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase79",
            generated_utc=generated_utc,
            inputs={"phase51_dense_lake": str(dense_root), "phase78_next_queue": "outputs/phase78/next_research_queue.csv"},
            parameters={
                "max_rows_per_symbol": max_rows_per_symbol if max_rows_per_symbol is not None else "none_full_symbol_scan",
                "corr_bar_events": corr_bar_events,
                "diversity_gate": "12_complete_months_min_4_regimes_entropy_ge_1_min_2_feeds_shocks_spread_cv_corr_std",
            },
            outputs={
                "file_inventory": str(output_dir / "generator_file_inventory.csv"),
                "partition_profile": str(output_dir / "partition_scenario_profile.csv"),
                "monthly_diversity": str(output_dir / "monthly_scenario_diversity.csv"),
                "monthly_correlation_diversity": str(output_dir / "monthly_correlation_diversity.csv"),
                "acceptance_summary": str(output_dir / "generator_scenario_diversity_acceptance_summary.csv"),
                "report": str(output_dir / "phase79_generator_scenario_diversity_audit_report.md"),
                "manifest": str(output_dir / "phase79_generator_scenario_diversity_audit_manifest.json"),
            },
            random_seed="none_deterministic_generator_scenario_audit",
            scenario_ids="phase79_dense_full_year_scenario_diversity",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_generator_audit",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase79_generator_scenario_diversity_audit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit dense synthetic generator scenario diversity.")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--max-rows-per-symbol", type=int, default=DEFAULT_MAX_ROWS_PER_SYMBOL)
    parser.add_argument("--corr-bar-events", type=int, default=DEFAULT_CORR_BAR_EVENTS)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase79(
        dense_root=args.dense_root,
        output_dir=args.output_dir,
        base_dir=args.base_dir,
        max_rows_per_symbol=args.max_rows_per_symbol,
        corr_bar_events=args.corr_bar_events,
    )


if __name__ == "__main__":
    main()
