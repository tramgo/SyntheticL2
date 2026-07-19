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

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase56_cost_clearing_label_discovery import DEFAULT_ORDER_NOTIONAL_INR
from synthetic_l2.phase61_lower_frequency_candidate_sweep import _safe_path, profile_cost_bps, retail_profile
from synthetic_l2.phase70_cross_symbol_lead_lag_labels import ETF_SYMBOLS, symbol_universe
from synthetic_l2.phase76_common_overlap_matrix_validator import DEFAULT_LEADER_SYMBOL, DEFAULT_LEADER_THRESHOLD
from synthetic_l2.phase77_hdfcbank_disjoint_month_retest import available_trade_months
from synthetic_l2.phase81_stratified_dense_window_reader import DEFAULT_DENSE_ROOT
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase82")
DEFAULT_PHASE81_DIR = Path("outputs/phase81")
DEFAULT_TIME_BUCKET_SECONDS = 5_000
DEFAULT_STALENESS_LIMIT_SECONDS = 1_000
DEFAULT_MAX_DENSE_ROWS_PER_STRATUM = 10_000
DEFAULT_EXCLUDE_MONTH = "2026-01"


def load_reader_contract(phase81_dir: Path) -> pd.DataFrame:
    path = phase81_dir / "stratified_dense_reader_contract.csv"
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def dates_and_feeds(contract: pd.DataFrame, trade_month: str) -> tuple[list[str], list[str]]:
    row = contract[contract["trade_month"].astype(str).eq(trade_month)]
    if row.empty:
        raise KeyError(f"No Phase81 reader contract for trade_month={trade_month}")
    item = row.iloc[0]
    dates = [value for value in str(item["selected_trade_dates"]).split("|") if value]
    feeds = [value for value in str(item["feed_profiles"]).split("|") if value]
    return dates, feeds


def symbol_file(dense_root: Path, trade_month: str, symbol: str) -> Path:
    return dense_root / f"trade_month={trade_month}" / f"symbol={symbol}" / "part-00000.parquet"


def query_symbol_stratified_bars(
    path: Path,
    selected_dates: list[str],
    feed_profiles: list[str],
    time_bucket_seconds: int,
    staleness_limit_seconds: int,
    max_dense_rows_per_stratum: int,
) -> pd.DataFrame:
    date_list = ", ".join(f"'{date}'" for date in selected_dates)
    feed_list = ", ".join(f"'{feed}'" for feed in feed_profiles)
    con = duckdb.connect()
    try:
        sql = f"""
        with filtered as (
            select
                *,
                row_number() over (partition by trade_date, feed_profile order by local_sequence_id) as stratum_row_number
            from read_parquet('{_safe_path(path)}', union_by_name=true)
            where trade_date in ({date_list})
              and feed_profile in ({feed_list})
              and callback_received_utc_ms is not null
              and buy_1_price > 0
              and sell_1_price > 0
              and sell_1_price >= buy_1_price
              and not coalesce(is_duplicate, false)
              and not coalesce(is_disconnect_gap, false)
              and not coalesce(is_out_of_order_injected, false)
        ),
        sampled as (
            select *
            from filtered
            where stratum_row_number <= {int(max_dense_rows_per_stratum)}
        ),
        base as (
            select
                trade_month,
                trade_date,
                feed_profile,
                symbol,
                local_sequence_id,
                callback_received_utc_ms::double as timestamp_seconds,
                floor(callback_received_utc_ms::double / {int(time_bucket_seconds)})::bigint as global_time_bucket_id,
                ((buy_1_price + sell_1_price) / 2.0)::double as mid_price,
                greatest(sell_1_price - buy_1_price, 0.01)::double as spread
            from sampled
        )
        select
            trade_month,
            trade_date,
            feed_profile,
            symbol,
            {int(time_bucket_seconds)}::integer as time_bucket_seconds,
            global_time_bucket_id,
            count(*)::bigint as rows_in_bucket,
            min(timestamp_seconds)::double as first_timestamp_seconds,
            max(timestamp_seconds)::double as last_timestamp_seconds,
            first(mid_price order by local_sequence_id)::double as open_mid_price,
            last(mid_price order by local_sequence_id)::double as close_mid_price,
            avg(spread)::double as avg_spread
        from base
        group by trade_month, trade_date, feed_profile, symbol, global_time_bucket_id
        having count(*) >= 10
        order by trade_date, feed_profile, global_time_bucket_id
        """
        bars = con.execute(sql).fetchdf()
    finally:
        con.close()
    if bars.empty:
        return bars
    bars["bucket_end_seconds"] = (bars["global_time_bucket_id"].astype(float) + 1.0) * float(time_bucket_seconds)
    bars["staleness_seconds"] = bars["bucket_end_seconds"] - bars["last_timestamp_seconds"].astype(float)
    bars["fresh_cell"] = bars["staleness_seconds"].le(float(staleness_limit_seconds))
    bars["bar_return"] = bars["close_mid_price"] / bars["open_mid_price"].replace(0, np.nan) - 1.0
    bars = bars.sort_values(["trade_date", "feed_profile", "symbol", "global_time_bucket_id"], kind="mergesort")
    bars["next_bar_return"] = (
        bars.groupby(["trade_date", "feed_profile", "symbol"], sort=False)["close_mid_price"].shift(-1)
        / bars["close_mid_price"].replace(0, np.nan)
        - 1.0
    )
    return bars


def build_month_matrix(
    dense_root: Path,
    trade_month: str,
    selected_dates: list[str],
    feed_profiles: list[str],
    time_bucket_seconds: int,
    staleness_limit_seconds: int,
    max_dense_rows_per_stratum: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    frames: list[pd.DataFrame] = []
    for symbol in symbol_universe():
        path = symbol_file(dense_root, trade_month, symbol)
        if not path.exists():
            continue
        bars = query_symbol_stratified_bars(
            path,
            selected_dates,
            feed_profiles,
            time_bucket_seconds,
            staleness_limit_seconds,
            max_dense_rows_per_stratum,
        )
        if not bars.empty:
            frames.append(bars)
    matrix = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    if matrix.empty:
        return matrix, pd.DataFrame()
    expected_symbols = len(symbol_universe())
    coverage = (
        matrix.groupby(["trade_month", "trade_date", "feed_profile", "global_time_bucket_id"], sort=True)
        .agg(
            symbols_present=("symbol", "nunique"),
            fresh_symbols=("fresh_cell", "sum"),
            total_rows=("rows_in_bucket", "sum"),
            max_staleness_seconds=("staleness_seconds", "max"),
            median_staleness_seconds=("staleness_seconds", "median"),
        )
        .reset_index()
    )
    coverage["expected_symbols"] = expected_symbols
    coverage["coverage_fraction"] = coverage["symbols_present"] / float(expected_symbols)
    coverage["fresh_fraction"] = coverage["fresh_symbols"] / float(expected_symbols)
    coverage["coverage_pass"] = coverage["coverage_fraction"].ge(0.95) & coverage["fresh_fraction"].ge(0.95)
    return matrix, coverage


def hdfcbank_recheck(matrix: pd.DataFrame) -> pd.DataFrame:
    if matrix.empty:
        return pd.DataFrame()
    target_symbols = [symbol for symbol in symbol_universe() if symbol != DEFAULT_LEADER_SYMBOL and symbol not in ETF_SYMBOLS]
    leader = matrix[matrix["symbol"].eq(DEFAULT_LEADER_SYMBOL)][
        ["trade_month", "trade_date", "feed_profile", "global_time_bucket_id", "bar_return"]
    ].rename(columns={"bar_return": "leader_bar_return"})
    targets = matrix[matrix["symbol"].isin(target_symbols)].copy()
    joined = targets.merge(leader, on=["trade_month", "trade_date", "feed_profile", "global_time_bucket_id"], how="inner")
    joined = joined[joined["next_bar_return"].notna() & joined["leader_bar_return"].abs().ge(float(DEFAULT_LEADER_THRESHOLD))].copy()
    if joined.empty:
        return pd.DataFrame()
    profile = retail_profile()
    slippage_ticks = float(profile["fixed_slippage_ticks"])
    impact_bps = float(profile["impact_bps"]) + float(profile.get("fees_bps", 0.0))
    zerodha_bps = profile_cost_bps(profile)
    joined["side"] = np.sign(joined["leader_bar_return"].astype(float))
    joined = joined[joined["side"].ne(0)].copy()
    joined["gross_return"] = joined["side"].astype(float) * joined["next_bar_return"].astype(float)
    joined["cost_return"] = (
        ((joined["avg_spread"].astype(float) / 2.0) / joined["close_mid_price"].astype(float))
        + (slippage_ticks * joined["avg_spread"].astype(float) / joined["close_mid_price"].astype(float))
        + (impact_bps / 10000.0)
        + (zerodha_bps / 10000.0)
    )
    joined["net_return"] = joined["gross_return"] - joined["cost_return"]
    symbol_net = joined.groupby("symbol", sort=True)["net_return"].sum()
    gross = float(joined["gross_return"].sum() * DEFAULT_ORDER_NOTIONAL_INR)
    cost = float(joined["cost_return"].sum() * DEFAULT_ORDER_NOTIONAL_INR)
    return pd.DataFrame(
        [
            {
                "rule_id": "P82_STRATIFIED_HDFCBANK_MOMENTUM_Q70_RECHECK",
                "phase76_reference_rule_id": "P76_COMMON_OVERLAP_HDFCBANK_MOMENTUM_Q70_RECHECK",
                "leader_symbol": DEFAULT_LEADER_SYMBOL,
                "alignment": "stratified_source_day_feed_timestamp_bucket",
                "threshold": float(DEFAULT_LEADER_THRESHOLD),
                "trades": int(len(joined)),
                "target_symbols": int(joined["symbol"].nunique()),
                "net_pnl_inr": float(joined["net_return"].sum() * DEFAULT_ORDER_NOTIONAL_INR),
                "gross_pnl_proxy_inr": gross,
                "cost_pnl_drag_proxy_inr": cost,
                "precision_cost_clear": float((joined["gross_return"] > joined["cost_return"]).mean()),
                "positive_target_fraction": float((symbol_net > 0).mean()) if int(symbol_net.shape[0]) else 0.0,
                "cost_drag_to_abs_gross_ratio": cost / abs(gross) if abs(gross) > 0 else np.nan,
            }
        ]
    )


def summarize_month(trade_month: str, matrix: pd.DataFrame, coverage: pd.DataFrame, recheck: pd.DataFrame, elapsed: float) -> dict[str, Any]:
    coverage_pass_fraction = float(coverage["coverage_pass"].mean()) if not coverage.empty else 0.0
    fresh_cell_fraction = float(matrix["fresh_cell"].mean()) if not matrix.empty and "fresh_cell" in matrix else 0.0
    recheck_pass = bool(
        not recheck.empty
        and float(recheck.iloc[0]["net_pnl_inr"]) > 0
        and float(recheck.iloc[0]["precision_cost_clear"]) >= 0.55
        and float(recheck.iloc[0]["cost_drag_to_abs_gross_ratio"]) <= 0.50
        and float(recheck.iloc[0]["positive_target_fraction"]) >= 0.50
    )
    return {
        "trade_month": trade_month,
        "matrix_rows": int(len(matrix)),
        "coverage_bucket_rows": int(len(coverage)),
        "coverage_pass_fraction": coverage_pass_fraction,
        "fresh_cell_fraction": fresh_cell_fraction,
        "recheck_rows": int(len(recheck)),
        "hdfcbank_recheck_pass": int(recheck_pass),
        "trades": int(recheck.iloc[0]["trades"]) if not recheck.empty else 0,
        "target_symbols": int(recheck.iloc[0]["target_symbols"]) if not recheck.empty else 0,
        "net_pnl_inr": float(recheck.iloc[0]["net_pnl_inr"]) if not recheck.empty else 0.0,
        "gross_pnl_proxy_inr": float(recheck.iloc[0]["gross_pnl_proxy_inr"]) if not recheck.empty else 0.0,
        "cost_pnl_drag_proxy_inr": float(recheck.iloc[0]["cost_pnl_drag_proxy_inr"]) if not recheck.empty else 0.0,
        "precision_cost_clear": float(recheck.iloc[0]["precision_cost_clear"]) if not recheck.empty else 0.0,
        "positive_target_fraction": float(recheck.iloc[0]["positive_target_fraction"]) if not recheck.empty else 0.0,
        "cost_drag_to_abs_gross_ratio": float(recheck.iloc[0]["cost_drag_to_abs_gross_ratio"]) if not recheck.empty else np.nan,
        "elapsed_seconds": elapsed,
    }


def summarize_all(month_detail: pd.DataFrame, min_months: int) -> pd.DataFrame:
    valid = month_detail[
        month_detail["coverage_pass_fraction"].ge(0.95)
        & month_detail["fresh_cell_fraction"].ge(0.95)
        & month_detail["recheck_rows"].gt(0)
    ].copy()
    positive_months = int((valid["net_pnl_inr"] > 0).sum()) if not valid.empty else 0
    pass_months = int(valid["hdfcbank_recheck_pass"].sum()) if not valid.empty else 0
    total_net = float(valid["net_pnl_inr"].sum()) if not valid.empty else 0.0
    total_trades = int(valid["trades"].sum()) if not valid.empty else 0
    positive_month_fraction = positive_months / float(len(valid) or 1)
    pass_month_fraction = pass_months / float(len(valid) or 1)
    aggregate_pass = bool(
        len(month_detail) >= int(min_months)
        and len(valid) >= int(min_months)
        and total_net > 0
        and total_trades >= 100
        and positive_month_fraction >= 0.60
        and pass_month_fraction >= 0.60
    )
    median_coverage = float(month_detail["coverage_pass_fraction"].median()) if not month_detail.empty else 0.0
    if len(valid) < int(min_months):
        next_action = "materialize_cached_stratified_bars_and_fix_alignment_coverage"
    elif aggregate_pass:
        next_action = "expand_stratified_hdfcbank_with_risk_controls"
    else:
        next_action = "retire_hdfcbank_lead_lag_after_stratified_falsification"
    return pd.DataFrame(
        [
            ("phase82_months_tested", int(len(month_detail)), "Stratified months retested"),
            ("phase82_valid_months", int(len(valid)), "Months with coverage/freshness/recheck evidence"),
            ("phase82_positive_months", positive_months, "Valid months with positive synthetic net P&L"),
            ("phase82_pass_months", pass_months, "Valid months passing per-month HDFCBANK gates"),
            ("phase82_total_trades", total_trades, "Aggregate stratified HDFCBANK trades"),
            ("phase82_total_net_pnl_inr", total_net, "Aggregate after-cost synthetic net P&L"),
            ("phase82_positive_month_fraction", positive_month_fraction, "Positive valid-month fraction"),
            ("phase82_pass_month_fraction", pass_month_fraction, "Per-month pass fraction"),
            ("phase82_median_coverage_pass_fraction", median_coverage, "Median monthly timestamp bucket coverage pass fraction"),
            ("phase82_stratified_hdfcbank_retest_pass", int(aggregate_pass), "1 means HDFCBANK survives stratified disjoint retest"),
            ("phase82_recommend_next_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase82 Stratified HDFCBANK Disjoint Retest",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase82 reruns the HDFCBANK lead-lag clue through the Phase81 stratified dense-window reader.",
        "It is a bounded scenario-balanced dense replay, not a full 6B-row sweep.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase82_stratified_hdfcbank_retest_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase82(
    dense_root: Path,
    phase81_dir: Path,
    output_dir: Path,
    base_dir: Path,
    trade_months: list[str],
    exclude_month: str,
    time_bucket_seconds: int,
    staleness_limit_seconds: int,
    max_dense_rows_per_stratum: int,
    min_months: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    contract = load_reader_contract(phase81_dir)
    if not trade_months:
        trade_months = available_trade_months(dense_root, exclude_month)
    month_rows: list[dict[str, Any]] = []
    rechecks: list[pd.DataFrame] = []
    coverages: list[pd.DataFrame] = []
    started = time.perf_counter()
    for trade_month in trade_months:
        month_started = time.perf_counter()
        dates, feeds = dates_and_feeds(contract, trade_month)
        matrix, coverage = build_month_matrix(
            dense_root,
            trade_month,
            dates,
            feeds,
            time_bucket_seconds,
            staleness_limit_seconds,
            max_dense_rows_per_stratum,
        )
        recheck = hdfcbank_recheck(matrix)
        if not recheck.empty:
            recheck.insert(0, "trade_month", trade_month)
            rechecks.append(recheck)
        if not coverage.empty:
            coverages.append(coverage)
        month_rows.append(summarize_month(trade_month, matrix, coverage, recheck, time.perf_counter() - month_started))
    month_detail = pd.DataFrame(month_rows)
    recheck_all = pd.concat(rechecks, ignore_index=True) if rechecks else pd.DataFrame()
    coverage_all = pd.concat(coverages, ignore_index=True) if coverages else pd.DataFrame()
    acceptance = summarize_all(month_detail, min_months)

    month_detail.to_csv(output_dir / "stratified_hdfcbank_month_detail.csv", index=False)
    recheck_all.to_csv(output_dir / "stratified_hdfcbank_recheck_by_month.csv", index=False)
    coverage_all.to_csv(output_dir / "stratified_coverage_by_month.csv", index=False)
    acceptance.to_csv(output_dir / "stratified_hdfcbank_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Month Detail": month_detail,
            "HDFCBANK Recheck By Month": recheck_all,
            "Coverage Sample": coverage_all.head(120),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase82_stratified_hdfcbank_disjoint_retest",
        "stratified_hdfcbank_retest_pass": int(
            acceptance.loc[acceptance["metric"].eq("phase82_stratified_hdfcbank_retest_pass"), "value"].iloc[0]
        ),
        "elapsed_seconds": time.perf_counter() - started,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase82",
            generated_utc=generated_utc,
            inputs={
                "dense_lake": str(dense_root),
                "phase81_reader_contract": str(phase81_dir / "stratified_dense_reader_contract.csv"),
            },
            parameters={
                "exclude_month": exclude_month,
                "trade_months": ",".join(trade_months),
                "time_bucket_seconds": time_bucket_seconds,
                "staleness_limit_seconds": staleness_limit_seconds,
                "max_dense_rows_per_stratum": max_dense_rows_per_stratum,
                "threshold": DEFAULT_LEADER_THRESHOLD,
            },
            outputs={
                "month_detail": str(output_dir / "stratified_hdfcbank_month_detail.csv"),
                "recheck_by_month": str(output_dir / "stratified_hdfcbank_recheck_by_month.csv"),
                "coverage": str(output_dir / "stratified_coverage_by_month.csv"),
                "acceptance_summary": str(output_dir / "stratified_hdfcbank_acceptance_summary.csv"),
                "report": str(output_dir / "phase82_stratified_hdfcbank_retest_report.md"),
                "manifest": str(output_dir / "phase82_stratified_hdfcbank_retest_manifest.json"),
            },
            random_seed="none_deterministic_stratified_hdfcbank_retest",
            scenario_ids="phase82_phase81_stratified_dense_windows",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase82_timestamp_bucket_stratified_dense_windows",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase82_stratified_hdfcbank_retest_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run stratified HDFCBANK disjoint retest.")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--phase81-dir", type=Path, default=DEFAULT_PHASE81_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--trade-months", nargs="*", default=[])
    parser.add_argument("--exclude-month", type=str, default=DEFAULT_EXCLUDE_MONTH)
    parser.add_argument("--time-bucket-seconds", type=int, default=DEFAULT_TIME_BUCKET_SECONDS)
    parser.add_argument("--staleness-limit-seconds", type=int, default=DEFAULT_STALENESS_LIMIT_SECONDS)
    parser.add_argument("--max-dense-rows-per-stratum", type=int, default=DEFAULT_MAX_DENSE_ROWS_PER_STRATUM)
    parser.add_argument("--min-months", type=int, default=3)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase82(
        dense_root=args.dense_root,
        phase81_dir=args.phase81_dir,
        output_dir=args.output_dir,
        base_dir=args.base_dir,
        trade_months=list(args.trade_months),
        exclude_month=args.exclude_month,
        time_bucket_seconds=args.time_bucket_seconds,
        staleness_limit_seconds=args.staleness_limit_seconds,
        max_dense_rows_per_stratum=args.max_dense_rows_per_stratum,
        min_months=args.min_months,
    )


if __name__ == "__main__":
    main()
