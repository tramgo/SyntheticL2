from __future__ import annotations

import argparse
import json
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase90_cross_symbol_regime_imbalance_precommit import ETF_SYMBOLS, SYMBOL_SECTOR
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE162_DIR = Path("outputs/phase162")
DEFAULT_OUTPUT_ROOT = Path("raw_synthetic_l2_phase166_cross_symbol_lead_lag_cache")
DEFAULT_OUTPUT_DIR = Path("outputs/phase166")
DEFAULT_BUCKET_MS = 5000


def safe_path(path: Path) -> str:
    return path.as_posix().replace("'", "''")


def sector_case_sql() -> str:
    parts = [f"when symbol = '{symbol}' then '{sector}'" for symbol, sector in sorted(SYMBOL_SECTOR.items())]
    return "case " + " ".join(parts) + " else 'unknown' end"


def etf_case_sql() -> str:
    parts = ", ".join(f"'{symbol}'" for symbol in sorted(ETF_SYMBOLS))
    return f"symbol in ({parts})"


def write_month_cache(paths: list[str], trade_month: str, bucket_ms: int, output_root: Path) -> tuple[Path, dict[str, Any], pd.DataFrame]:
    quoted = ", ".join(f"'{safe_path(Path(path))}'" for path in paths)
    target_dir = output_root / f"trade_month={trade_month}"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "part-00000.parquet"
    con = duckdb.connect()
    try:
        con.execute(
            f"""
            copy (
            with raw as (
                select
                    trade_date,
                    symbol,
                    local_sequence_id,
                    callback_received_utc_ms,
                    floor(callback_received_utc_ms / {bucket_ms}) * {bucket_ms} as bucket_start_utc_ms,
                    ((buy_1_price + sell_1_price) / 2.0) as mid_price,
                    greatest(sell_1_price - buy_1_price, 0.01) as spread,
                    10000.0 * greatest(sell_1_price - buy_1_price, 0.01) / nullif(((buy_1_price + sell_1_price) / 2.0), 0.0) as spread_bps,
                    ((buy_1_quantity - sell_1_quantity) / nullif((buy_1_quantity + sell_1_quantity), 0.0)) as l1_imbalance,
                    (
                        (buy_1_quantity + buy_2_quantity + buy_3_quantity + buy_4_quantity + buy_5_quantity)
                        - (sell_1_quantity + sell_2_quantity + sell_3_quantity + sell_4_quantity + sell_5_quantity)
                    ) / nullif(
                        (buy_1_quantity + buy_2_quantity + buy_3_quantity + buy_4_quantity + buy_5_quantity)
                        + (sell_1_quantity + sell_2_quantity + sell_3_quantity + sell_4_quantity + sell_5_quantity),
                        0.0
                    ) as l5_imbalance,
                    (
                        buy_1_quantity + buy_2_quantity + buy_3_quantity + buy_4_quantity + buy_5_quantity
                        + sell_1_quantity + sell_2_quantity + sell_3_quantity + sell_4_quantity + sell_5_quantity
                    ) as l5_depth,
                    (((sell_1_price * buy_1_quantity + buy_1_price * sell_1_quantity) / nullif((buy_1_quantity + sell_1_quantity), 0.0))
                        - ((buy_1_price + sell_1_price) / 2.0)) / nullif(((buy_1_price + sell_1_price) / 2.0), 0.0) as microprice_dev,
                    coalesce(is_duplicate, false) as is_duplicate,
                    coalesce(is_disconnect_gap, false) as is_disconnect_gap,
                    coalesce(is_out_of_order_injected, false) as is_out_of_order_injected
                from read_parquet([{quoted}], union_by_name=true)
                where buy_1_price > 0 and sell_1_price > 0 and sell_1_price >= buy_1_price
            ),
            bucketed as (
            select
                '{trade_month}' as trade_month,
                trade_date,
                symbol,
                bucket_start_utc_ms,
                count(*)::bigint as dense_rows,
                min(callback_received_utc_ms)::bigint as first_callback_received_utc_ms,
                max(callback_received_utc_ms)::bigint as last_callback_received_utc_ms,
                first(mid_price order by local_sequence_id)::double as open_mid_price,
                last(mid_price order by local_sequence_id)::double as close_mid_price,
                avg(spread_bps)::double as avg_spread_bps,
                avg(l1_imbalance)::double as avg_l1_imbalance,
                avg(l5_imbalance)::double as avg_l5_imbalance,
                avg(l5_depth)::double as avg_l5_depth,
                avg(microprice_dev)::double as avg_microprice_dev,
                avg(case when is_duplicate then 1.0 else 0.0 end)::double as duplicate_fraction,
                avg(case when is_disconnect_gap then 1.0 else 0.0 end)::double as disconnect_fraction,
                avg(case when is_out_of_order_injected then 1.0 else 0.0 end)::double as out_of_order_fraction
            from raw
                group by trade_date, symbol, bucket_start_utc_ms
            ),
            tagged as (
                select
                    *,
                    {sector_case_sql()} as sector,
                    {etf_case_sql()} as is_etf,
                    close_mid_price / nullif(open_mid_price, 0.0) - 1.0 as bucket_return,
                    {bucket_ms}::integer as bucket_ms
                from bucketed
            ),
            cross_section as (
                select
                    *,
                    count(*) over (partition by trade_month, trade_date, bucket_start_utc_ms) as market_symbol_count,
                    sum(avg_l1_imbalance) over (partition by trade_month, trade_date, bucket_start_utc_ms) as market_l1_pressure_sum,
                    sum(avg_l5_imbalance) over (partition by trade_month, trade_date, bucket_start_utc_ms) as market_l5_pressure_sum,
                    sum(avg_microprice_dev) over (partition by trade_month, trade_date, bucket_start_utc_ms) as market_microprice_sum,
                    sum(close_mid_price / nullif(open_mid_price, 0.0) - 1.0) over (partition by trade_month, trade_date, bucket_start_utc_ms) as market_return_sum,
                    sum(dense_rows) over (partition by trade_month, trade_date, bucket_start_utc_ms) as market_dense_rows,
                    sum(case when is_etf then 1 else 0 end) over (partition by trade_month, trade_date, bucket_start_utc_ms) as etf_symbol_count,
                    avg(case when is_etf then avg_l5_imbalance else null end) over (partition by trade_month, trade_date, bucket_start_utc_ms) as etf_l5_pressure_mean,
                    avg(case when is_etf then close_mid_price / nullif(open_mid_price, 0.0) - 1.0 else null end) over (partition by trade_month, trade_date, bucket_start_utc_ms) as etf_return_mean,
                    count(*) over (partition by trade_month, trade_date, bucket_start_utc_ms, sector) as sector_symbol_count,
                    sum(avg_l1_imbalance) over (partition by trade_month, trade_date, bucket_start_utc_ms, sector) as sector_l1_pressure_sum,
                    sum(avg_l5_imbalance) over (partition by trade_month, trade_date, bucket_start_utc_ms, sector) as sector_l5_pressure_sum,
                    sum(close_mid_price / nullif(open_mid_price, 0.0) - 1.0) over (partition by trade_month, trade_date, bucket_start_utc_ms, sector) as sector_return_sum,
                    sum(dense_rows) over (partition by trade_month, trade_date, bucket_start_utc_ms, sector) as sector_dense_rows
                from tagged
            ),
            features as (
                select
                    *,
                    (market_l1_pressure_sum - avg_l1_imbalance) / nullif(market_symbol_count - 1.0, 0.0) as x_market_l1_ex_target,
                    (market_l5_pressure_sum - avg_l5_imbalance) / nullif(market_symbol_count - 1.0, 0.0) as x_market_l5_ex_target,
                    (market_microprice_sum - avg_microprice_dev) / nullif(market_symbol_count - 1.0, 0.0) as x_market_microprice_ex_target,
                    (market_return_sum - bucket_return) / nullif(market_symbol_count - 1.0, 0.0) as x_market_return_ex_target,
                    (sector_l1_pressure_sum - avg_l1_imbalance) / nullif(sector_symbol_count - 1.0, 0.0) as x_sector_l1_ex_target,
                    (sector_l5_pressure_sum - avg_l5_imbalance) / nullif(sector_symbol_count - 1.0, 0.0) as x_sector_l5_ex_target,
                    (sector_return_sum - bucket_return) / nullif(sector_symbol_count - 1.0, 0.0) as x_sector_return_ex_target
                from cross_section
            )
            select
                *,
                lag(x_market_l5_ex_target, 1) over (partition by trade_date, symbol order by bucket_start_utc_ms) as x_market_l5_ex_target_lag1_bucket,
                lag(x_market_l5_ex_target, 2) over (partition by trade_date, symbol order by bucket_start_utc_ms) as x_market_l5_ex_target_lag2_bucket,
                lag(x_market_return_ex_target, 1) over (partition by trade_date, symbol order by bucket_start_utc_ms) as x_market_return_ex_target_lag1_bucket,
                lag(x_market_return_ex_target, 2) over (partition by trade_date, symbol order by bucket_start_utc_ms) as x_market_return_ex_target_lag2_bucket,
                lag(x_sector_l5_ex_target, 1) over (partition by trade_date, symbol order by bucket_start_utc_ms) as x_sector_l5_ex_target_lag1_bucket,
                lag(x_sector_l5_ex_target, 2) over (partition by trade_date, symbol order by bucket_start_utc_ms) as x_sector_l5_ex_target_lag2_bucket,
                lag(x_sector_return_ex_target, 1) over (partition by trade_date, symbol order by bucket_start_utc_ms) as x_sector_return_ex_target_lag1_bucket,
                lag(x_sector_return_ex_target, 2) over (partition by trade_date, symbol order by bucket_start_utc_ms) as x_sector_return_ex_target_lag2_bucket,
                lag(etf_l5_pressure_mean, 1) over (partition by trade_date, symbol order by bucket_start_utc_ms) as etf_l5_pressure_mean_lag1_bucket,
                lag(etf_l5_pressure_mean, 2) over (partition by trade_date, symbol order by bucket_start_utc_ms) as etf_l5_pressure_mean_lag2_bucket,
                lag(etf_return_mean, 1) over (partition by trade_date, symbol order by bucket_start_utc_ms) as etf_return_mean_lag1_bucket,
                lag(etf_return_mean, 2) over (partition by trade_date, symbol order by bucket_start_utc_ms) as etf_return_mean_lag2_bucket,
                lead(bucket_return, 1) over (partition by trade_date, symbol order by bucket_start_utc_ms) as target_next_bucket_return,
                'feature_cache_not_strategy_verdict' as cross_symbol_cache_role
            from features
            order by trade_date, bucket_start_utc_ms, symbol
            ) to '{safe_path(target)}' (format parquet, compression zstd)
            """
        )
        stats = con.execute(
            f"""
            select
                count(*)::bigint as bucket_symbol_rows,
                count(distinct symbol)::integer as symbols,
                count(distinct trade_date)::integer as trade_dates,
                sum(dense_rows)::bigint as source_dense_rows,
                min(market_symbol_count)::integer as min_market_symbol_count,
                avg(market_symbol_count)::double as avg_market_symbol_count,
                avg(case when x_market_l5_ex_target_lag1_bucket is not null then 1.0 else 0.0 end)::double as lag1_feature_coverage
            from read_parquet('{safe_path(target)}')
            """
        ).fetchdf().iloc[0].to_dict()
        sample = con.execute(f"select * from read_parquet('{safe_path(target)}') limit 5").fetchdf()
    finally:
        con.close()
    return target, stats, sample


def summarize_inventory(inventory: pd.DataFrame, elapsed_seconds: float, bucket_ms: int) -> pd.DataFrame:
    expected_months = int(inventory["trade_month"].nunique()) if not inventory.empty else 0
    cache_files = int(len(inventory))
    return pd.DataFrame(
        [
            ("phase166_bucket_ms", bucket_ms, "Synchronization bucket size; not a claim that native data is uniformly sampled"),
            ("phase166_months_cached", expected_months, "Synthetic months cached"),
            ("phase166_cache_files", cache_files, "Monthly cache parquet files"),
            ("phase166_symbols_cached", int(inventory["symbols"].max()) if not inventory.empty else 0, "Maximum symbols per monthly cache"),
            ("phase166_min_market_symbol_count", int(inventory["min_market_symbol_count"].min()) if not inventory.empty else 0, "Minimum symbols observed in any synchronization bucket"),
            ("phase166_median_lag1_feature_coverage", float(inventory["lag1_feature_coverage"].median()) if not inventory.empty else 0.0, "Median monthly lag-1 feature availability fraction"),
            ("phase166_bucket_symbol_rows", int(inventory["bucket_symbol_rows"].sum()) if not inventory.empty else 0, "Cached symbol/bucket rows"),
            ("phase166_source_dense_rows_represented", int(inventory["source_dense_rows"].sum()) if not inventory.empty else 0, "Dense input rows represented by monthly cache"),
            ("phase166_cache_bytes", int(inventory["bytes"].sum()) if not inventory.empty else 0, "Compressed cache bytes"),
            ("phase166_elapsed_seconds", float(elapsed_seconds), "Cache materialization elapsed seconds"),
            ("phase166_s08_cache_ready", int(expected_months >= 12 and cache_files >= 12 and int(inventory["symbols"].min()) >= 32 and float(inventory["lag1_feature_coverage"].median()) > 0.90), "1 means S08 cross-symbol replay cache is ready"),
            ("phase166_strategy_replay_allowed", 0, "Phase166 prepares cache only; replay remains for a later phase"),
            ("phase166_azure_read_policy", "forbidden_for_analysis_download_first_then_local", "No direct Python Azure scanning"),
            ("phase166_next_best_action", "precommit_and_run_s08_cross_symbol_lead_lag_replay_using_phase166_cache", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase166 Cross-symbol Lead-lag Cache",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase166 builds a synchronized local feature cache for S08-style cross-symbol lead-lag research from the Phase162 dense L2 lake.",
        "The bucket is an alignment device, not a claim that the source feed is uniformly sampled. This phase does not run a strategy, P&L, or acceptance verdict.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase166_cross_symbol_lead_lag_cache_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase166(
    phase162_dir: Path,
    output_root: Path,
    output_dir: Path,
    base_dir: Path,
    bucket_ms: int,
    max_months: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    phase162_inventory = pd.read_csv(phase162_dir / "phase162_dense_full_year_inventory.csv")
    months = sorted(phase162_inventory["trade_month"].astype(str).unique())
    if max_months > 0:
        months = months[:max_months]
    started = time.perf_counter()
    rows: list[dict[str, Any]] = []
    samples: list[pd.DataFrame] = []
    for trade_month in months:
        month_inventory = phase162_inventory[phase162_inventory["trade_month"].astype(str).eq(trade_month)].copy()
        target, stats, sample = write_month_cache(month_inventory["file_path"].astype(str).tolist(), trade_month, bucket_ms, output_root)
        rows.append(
            {
                "trade_month": trade_month,
                "symbols": int(stats["symbols"]),
                "trade_dates": int(stats["trade_dates"]),
                "bucket_symbol_rows": int(stats["bucket_symbol_rows"]),
                "source_dense_rows": int(stats["source_dense_rows"]),
                "min_market_symbol_count": int(stats["min_market_symbol_count"]),
                "avg_market_symbol_count": float(stats["avg_market_symbol_count"]),
                "lag1_feature_coverage": float(stats["lag1_feature_coverage"]),
                "bucket_ms": int(bucket_ms),
                "file_path": str(target),
                "bytes": int(target.stat().st_size),
            }
        )
        samples.append(sample)
    elapsed = time.perf_counter() - started
    inventory = pd.DataFrame(rows)
    sample = pd.concat(samples, ignore_index=True) if samples else pd.DataFrame()
    acceptance = summarize_inventory(inventory, elapsed, bucket_ms)
    inventory.to_csv(output_dir / "phase166_cross_symbol_cache_inventory.csv", index=False)
    acceptance.to_csv(output_dir / "phase166_cross_symbol_cache_acceptance_summary.csv", index=False)
    sample.to_csv(output_dir / "phase166_cross_symbol_cache_sample.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Cache Inventory": inventory,
            "Cache Sample": sample,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase166_cross_symbol_lead_lag_cache",
        **reproducibility_fields(
            artifact_id="phase166",
            generated_utc=generated_utc,
            inputs={"phase162_inventory": str(phase162_dir / "phase162_dense_full_year_inventory.csv")},
            parameters={
                "bucket_ms": bucket_ms,
                "max_months": max_months,
                "alignment_policy": "bucketed_cross_symbol_cache_not_uniform_sampling_claim",
                "strategy_replay_allowed": 0,
                "azure_read_policy": "forbidden_for_analysis_download_first_then_local",
            },
            outputs={
                "cache_root": str(output_root),
                "inventory": str(output_dir / "phase166_cross_symbol_cache_inventory.csv"),
                "acceptance_summary": str(output_dir / "phase166_cross_symbol_cache_acceptance_summary.csv"),
                "sample": str(output_dir / "phase166_cross_symbol_cache_sample.csv"),
                "report": str(output_dir / "phase166_cross_symbol_lead_lag_cache_report.md"),
                "manifest": str(output_dir / "phase166_cross_symbol_lead_lag_cache_manifest.json"),
            },
            random_seed="none_deterministic_phase166_cache",
            scenario_ids="phase162_distributional_full_year_dense_l2_cross_symbol_cache",
            cost_model_version="not_applicable_no_execution",
            latency_model_version="not_applicable_cache_only",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase166_cross_symbol_lead_lag_cache_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase166 cross-symbol lead-lag cache from Phase162 dense L2.")
    parser.add_argument("--phase162-dir", type=Path, default=DEFAULT_PHASE162_DIR)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--bucket-ms", type=int, default=DEFAULT_BUCKET_MS)
    parser.add_argument("--max-months", type=int, default=0, help="0 means all Phase162 months.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase166(args.phase162_dir, args.output_root, args.output_dir, args.base_dir, args.bucket_ms, args.max_months)


if __name__ == "__main__":
    main()
