from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import duckdb
import pandas as pd

from synthetic_l2.phase12_execution_simulator import EXECUTION_PROFILES
from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, calculate_equity_intraday_nse_charges


DEFAULT_DENSE_ROOT = Path("raw_synthetic_l2_dense_full_year")
DEFAULT_OUTPUT_DIR = Path("outputs/phase52")
DEFAULT_ORDER_NOTIONAL_INR = 100_000.0
STRATEGIES = [
    {
        "strategy_id": "DENSE_S01_L1_IMBALANCE",
        "feature": "l1_imbalance",
        "raw_signal": "case when abs(l1_imbalance) >= l1_threshold then sign(l1_imbalance) else 0 end",
    },
    {
        "strategy_id": "DENSE_S02_MICROPRICE",
        "feature": "microprice_dev",
        "raw_signal": "case when abs(microprice_dev) >= micro_threshold then sign(microprice_dev) else 0 end",
    },
    {
        "strategy_id": "DENSE_S03_1T_MOMENTUM",
        "feature": "one_tick_return",
        "raw_signal": "case when abs(one_tick_return) >= momentum_threshold then sign(one_tick_return) else 0 end",
    },
]


def parquet_files(dense_root: Path, limit_shards: int | None = None) -> list[Path]:
    files = sorted(dense_root.glob("trade_month=*/symbol=*/part-00000.parquet"))
    if not files:
        raise FileNotFoundError(f"No dense parquet files under {dense_root}")
    return files[:limit_shards] if limit_shards is not None else files


def profile_cost_bps(profile: dict[str, object]) -> float:
    if not bool(profile.get("apply_zerodha_equity_intraday_charges", False)):
        return 0.0
    charges = calculate_equity_intraday_nse_charges(
        buy_value_inr=float(profile.get("order_notional_inr", DEFAULT_ORDER_NOTIONAL_INR)),
        sell_value_inr=float(profile.get("order_notional_inr", DEFAULT_ORDER_NOTIONAL_INR)),
    )
    return float(charges.effective_bps_on_buy_value)


def _safe_path(path: Path) -> str:
    return path.as_posix().replace("'", "''")


def query_shard(path: Path, profile: dict[str, object], strategy: dict[str, str], threshold_quantile: float) -> pd.DataFrame:
    total_latency = int(profile["decision_latency_events"]) + int(profile["broker_latency_events"])
    slippage_ticks = float(profile["fixed_slippage_ticks"])
    impact_bps = float(profile["impact_bps"]) + float(profile.get("fees_bps", 0.0))
    zerodha_bps = profile_cost_bps(profile)
    cancel_filter = (
        "and not (coalesce(is_disconnect_gap, false) or coalesce(is_out_of_order_injected, false))"
        if bool(profile.get("cancel_on_stale_or_disconnect", False))
        else ""
    )
    raw_signal = strategy["raw_signal"]
    sql = f"""
    with base as (
        select
            trade_date,
            symbol,
            local_sequence_id,
            dense_subtick_id,
            ((buy_1_price + sell_1_price) / 2.0) as mid_price,
            lead(((buy_1_price + sell_1_price) / 2.0)) over (order by local_sequence_id) as next_mid_price,
            lag(last_price) over (order by local_sequence_id) as prev_last_price,
            greatest(sell_1_price - buy_1_price, 0.01) as spread,
            greatest(sell_1_price - buy_1_price, 0.01) as tick_size_proxy,
            ((buy_1_quantity - sell_1_quantity) / nullif((buy_1_quantity + sell_1_quantity), 0.0)) as l1_imbalance,
            (((sell_1_price * buy_1_quantity + buy_1_price * sell_1_quantity) / nullif((buy_1_quantity + sell_1_quantity), 0.0))
                - ((buy_1_price + sell_1_price) / 2.0)) / nullif(((buy_1_price + sell_1_price) / 2.0), 0.0) as microprice_dev,
            (last_price / nullif(lag(last_price) over (order by local_sequence_id), 0.0) - 1.0) as one_tick_return,
            coalesce(is_duplicate, false) as is_duplicate,
            coalesce(is_disconnect_gap, false) as is_disconnect_gap,
            coalesce(is_out_of_order_injected, false) as is_out_of_order_injected
        from read_parquet('{_safe_path(path)}', union_by_name=true)
        where buy_1_price > 0 and sell_1_price > 0 and sell_1_price >= buy_1_price
    ),
    thresholds as (
        select
            quantile_cont(abs(l1_imbalance), {threshold_quantile}) as l1_threshold,
            quantile_cont(abs(microprice_dev), {threshold_quantile}) as micro_threshold,
            quantile_cont(abs(one_tick_return), {threshold_quantile}) as momentum_threshold
        from base
    ),
    raw as (
        select
            base.*,
            {raw_signal} as raw_signal
        from base
        cross join thresholds
    ),
    executable as (
        select
            *,
            lag(raw_signal, {total_latency}) over (order by local_sequence_id) as executable_signal
        from raw
    ),
    trades as (
        select
            trade_date,
            symbol,
            executable_signal,
            (executable_signal * (next_mid_price / nullif(mid_price, 0.0) - 1.0)) as gross_return,
            ((spread / 2.0) / nullif(mid_price, 0.0))
              + ({slippage_ticks} * tick_size_proxy / nullif(mid_price, 0.0))
              + ({impact_bps} / 10000.0)
              + ({zerodha_bps} / 10000.0) as cost_return
        from executable
        where executable_signal != 0
          and next_mid_price is not null
          and not is_duplicate
          {cancel_filter}
    )
    select
        trade_date,
        symbol,
        '{strategy["strategy_id"]}' as strategy_id,
        '{profile["execution_profile"]}' as execution_profile,
        count(*)::bigint as trades,
        sum(gross_return)::double as sum_gross_return,
        sum(cost_return)::double as sum_cost_return,
        sum(gross_return - cost_return)::double as sum_net_return,
        avg(gross_return)::double as mean_gross_return,
        avg(cost_return)::double as mean_cost_return,
        avg(gross_return - cost_return)::double as mean_net_return,
        sum((gross_return - cost_return) * {float(profile.get("order_notional_inr", DEFAULT_ORDER_NOTIONAL_INR))})::double as net_pnl_inr,
        min((gross_return - cost_return) * {float(profile.get("order_notional_inr", DEFAULT_ORDER_NOTIONAL_INR))})::double as worst_trade_pnl_inr,
        {threshold_quantile}::double as threshold_quantile,
        {total_latency}::integer as total_latency_events,
        {slippage_ticks}::double as fixed_slippage_ticks,
        {impact_bps}::double as internal_impact_bps,
        {zerodha_bps}::double as zerodha_charge_bps
    from trades
    group by trade_date, symbol
    """
    con = duckdb.connect()
    try:
        return con.execute(sql).fetchdf()
    finally:
        con.close()


def query_shard_all(path: Path, threshold_quantile: float) -> pd.DataFrame:
    con = duckdb.connect()
    try:
        con.execute(
            f"""
            create temporary table dense_features as
            with base as (
                select
                    trade_date,
                    symbol,
                    local_sequence_id,
                    ((buy_1_price + sell_1_price) / 2.0) as mid_price,
                    lead(((buy_1_price + sell_1_price) / 2.0)) over (order by local_sequence_id) as next_mid_price,
                    greatest(sell_1_price - buy_1_price, 0.01) as spread,
                    greatest(sell_1_price - buy_1_price, 0.01) as tick_size_proxy,
                    ((buy_1_quantity - sell_1_quantity) / nullif((buy_1_quantity + sell_1_quantity), 0.0)) as l1_imbalance,
                    (((sell_1_price * buy_1_quantity + buy_1_price * sell_1_quantity) / nullif((buy_1_quantity + sell_1_quantity), 0.0))
                        - ((buy_1_price + sell_1_price) / 2.0)) / nullif(((buy_1_price + sell_1_price) / 2.0), 0.0) as microprice_dev,
                    (last_price / nullif(lag(last_price) over (order by local_sequence_id), 0.0) - 1.0) as one_tick_return,
                    coalesce(is_duplicate, false) as is_duplicate,
                    coalesce(is_disconnect_gap, false) as is_disconnect_gap,
                    coalesce(is_out_of_order_injected, false) as is_out_of_order_injected
                from read_parquet('{_safe_path(path)}', union_by_name=true)
                where buy_1_price > 0 and sell_1_price > 0 and sell_1_price >= buy_1_price
            ),
            thresholds as (
                select
                    quantile_cont(abs(l1_imbalance), {threshold_quantile}) as l1_threshold,
                    quantile_cont(abs(microprice_dev), {threshold_quantile}) as micro_threshold,
                    quantile_cont(abs(one_tick_return), {threshold_quantile}) as momentum_threshold
                from base
            )
            select
                base.*,
                case when abs(l1_imbalance) >= l1_threshold then sign(l1_imbalance) else 0 end as signal_l1,
                case when abs(microprice_dev) >= micro_threshold then sign(microprice_dev) else 0 end as signal_micro,
                case when abs(one_tick_return) >= momentum_threshold then sign(one_tick_return) else 0 end as signal_momentum
            from base
            cross join thresholds
            """
        )
        union_parts = []
        for strategy in STRATEGIES:
            signal_column = {
                "DENSE_S01_L1_IMBALANCE": "signal_l1",
                "DENSE_S02_MICROPRICE": "signal_micro",
                "DENSE_S03_1T_MOMENTUM": "signal_momentum",
            }[strategy["strategy_id"]]
            for profile in EXECUTION_PROFILES:
                total_latency = int(profile["decision_latency_events"]) + int(profile["broker_latency_events"])
                slippage_ticks = float(profile["fixed_slippage_ticks"])
                impact_bps = float(profile["impact_bps"]) + float(profile.get("fees_bps", 0.0))
                zerodha_bps = profile_cost_bps(profile)
                order_notional = float(profile.get("order_notional_inr", DEFAULT_ORDER_NOTIONAL_INR))
                cancel_filter = (
                    "and not (coalesce(is_disconnect_gap, false) or coalesce(is_out_of_order_injected, false))"
                    if bool(profile.get("cancel_on_stale_or_disconnect", False))
                    else ""
                )
                union_parts.append(
                    f"""
                    select
                        trade_date,
                        symbol,
                        '{strategy["strategy_id"]}' as strategy_id,
                        '{profile["execution_profile"]}' as execution_profile,
                        count(*)::bigint as trades,
                        sum(gross_return)::double as sum_gross_return,
                        sum(cost_return)::double as sum_cost_return,
                        sum(gross_return - cost_return)::double as sum_net_return,
                        avg(gross_return)::double as mean_gross_return,
                        avg(cost_return)::double as mean_cost_return,
                        avg(gross_return - cost_return)::double as mean_net_return,
                        sum((gross_return - cost_return) * {order_notional})::double as net_pnl_inr,
                        min((gross_return - cost_return) * {order_notional})::double as worst_trade_pnl_inr,
                        {threshold_quantile}::double as threshold_quantile,
                        {total_latency}::integer as total_latency_events,
                        {slippage_ticks}::double as fixed_slippage_ticks,
                        {impact_bps}::double as internal_impact_bps,
                        {zerodha_bps}::double as zerodha_charge_bps
                    from (
                        select
                            trade_date,
                            symbol,
                            executable_signal,
                            (executable_signal * (next_mid_price / nullif(mid_price, 0.0) - 1.0)) as gross_return,
                            ((spread / 2.0) / nullif(mid_price, 0.0))
                              + ({slippage_ticks} * tick_size_proxy / nullif(mid_price, 0.0))
                              + ({impact_bps} / 10000.0)
                              + ({zerodha_bps} / 10000.0) as cost_return
                        from (
                            select
                                *,
                                lag({signal_column}, {total_latency}) over (order by local_sequence_id) as executable_signal
                            from dense_features
                        )
                        where executable_signal != 0
                          and next_mid_price is not null
                          and not is_duplicate
                          {cancel_filter}
                    )
                    group by trade_date, symbol
                    """
                )
        return con.execute("\nunion all\n".join(union_parts)).fetchdf()
    finally:
        con.close()


def summarize(daily_symbol: pd.DataFrame, files: list[Path], elapsed_seconds: float, dense_root: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    if daily_symbol.empty:
        summary = pd.DataFrame()
        acceptance = pd.DataFrame()
        return summary, acceptance
    daily = (
        daily_symbol.groupby(["trade_date", "strategy_id", "execution_profile"], sort=True)
        .agg(
            trades=("trades", "sum"),
            sum_gross_return=("sum_gross_return", "sum"),
            sum_cost_return=("sum_cost_return", "sum"),
            sum_net_return=("sum_net_return", "sum"),
            net_pnl_inr=("net_pnl_inr", "sum"),
            worst_trade_pnl_inr=("worst_trade_pnl_inr", "min"),
        )
        .reset_index()
    )
    rows = []
    for (strategy_id, execution_profile), group in daily.groupby(["strategy_id", "execution_profile"], sort=True):
        group = group.sort_values("trade_date", kind="mergesort").copy()
        group["running_net_pnl_inr"] = group["net_pnl_inr"].cumsum()
        group["running_peak_inr"] = group["running_net_pnl_inr"].cummax()
        group["drawdown_inr"] = group["running_net_pnl_inr"] - group["running_peak_inr"]
        daily_std = float(group["net_pnl_inr"].std(ddof=1))
        daily_mean = float(group["net_pnl_inr"].mean())
        sharpe = float((daily_mean / daily_std) * (252.0**0.5)) if daily_std > 0 else 0.0
        trades = int(group["trades"].sum())
        rows.append(
            {
                "strategy_id": strategy_id,
                "execution_profile": execution_profile,
                "trade_dates": int(group["trade_date"].nunique()),
                "trades": trades,
                "annual_net_pnl_inr": float(group["net_pnl_inr"].sum()),
                "mean_net_return_per_trade": float(group["sum_net_return"].sum() / trades) if trades else 0.0,
                "mean_gross_return_per_trade": float(group["sum_gross_return"].sum() / trades) if trades else 0.0,
                "mean_cost_return_per_trade": float(group["sum_cost_return"].sum() / trades) if trades else 0.0,
                "worst_daily_net_pnl_inr": float(group["net_pnl_inr"].min()),
                "max_drawdown_inr": float(group["drawdown_inr"].min()),
                "worst_trade_pnl_inr": float(group["worst_trade_pnl_inr"].min()),
                "positive_day_fraction": float((group["net_pnl_inr"] > 0).mean()),
                "annualized_sharpe_proxy": sharpe,
            }
        )
    summary = pd.DataFrame(rows)
    summary["positive_after_costs"] = summary["annual_net_pnl_inr"] > 0
    summary["risk_proxy_pass"] = (summary["max_drawdown_inr"] > -250_000.0) & (summary["worst_daily_net_pnl_inr"] > -150_000.0)
    summary["dense_replay_candidate"] = summary["positive_after_costs"] & summary["risk_proxy_pass"]
    summary = summary.sort_values(["annual_net_pnl_inr", "trades"], ascending=[False, False], kind="mergesort").reset_index(drop=True)

    acceptance = pd.DataFrame(
        [
            ("phase52_dense_replay_shards_scanned", len(files), "Dense parquet shards scanned"),
            ("phase52_dense_replay_strategy_profile_rows", len(summary), "Strategy/profile result rows"),
            ("phase52_dense_replay_trade_rows", int(summary["trades"].sum()), "Aggregated dense tick trade count"),
            ("phase52_positive_after_cost_rows", int(summary["positive_after_costs"].sum()), "Strategy/profile rows positive after costs"),
            ("phase52_dense_replay_candidate_rows", int(summary["dense_replay_candidate"].sum()), "Rows passing positive and proxy-risk screens"),
            ("phase52_elapsed_seconds", elapsed_seconds, "Replay elapsed seconds"),
            ("phase52_dense_output_root", str(dense_root), "Dense input lake root"),
            ("phase52_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha cost model used for charge bps"),
            ("phase52_synthetic_full_year_acceptance_ready", 0, "Dense replay is synthetic-only proxy evidence, not broker/real acceptance"),
        ],
        columns=["metric", "value", "description"],
    )
    return summary, acceptance


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase 52 Dense Lake Strategy Replay",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This phase replays simple L1/microprice/momentum strategies directly over the Phase 51 dense full-year parquet lake using vectorized DuckDB scans.",
        "It is synthetic-only dense proxy evidence. Acceptance remains closed until a strategy clears the synthetic-only gates and later real/broker evidence becomes available.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase52_dense_lake_strategy_replay_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase52(dense_root: Path, output_dir: Path, base_dir: Path, threshold_quantile: float, limit_shards: int | None) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    files = parquet_files(dense_root, limit_shards=limit_shards)
    daily_path = output_dir / "dense_replay_daily_symbol.csv"
    started = time.perf_counter()
    completed_paths: set[str] = set()
    if daily_path.exists():
        existing = pd.read_csv(daily_path, usecols=["shard_path"])
        completed_paths = set(existing["shard_path"].astype(str).unique().tolist())
    for shard_index, path in enumerate(files, start=1):
        if str(path) in completed_paths:
            continue
        shard_frame = query_shard_all(path, threshold_quantile)
        shard_frame.insert(0, "shard_index", shard_index)
        shard_frame.insert(1, "shard_path", str(path))
        shard_frame.to_csv(daily_path, mode="a", header=not daily_path.exists(), index=False)
        completed_paths.add(str(path))
        if shard_index % 8 == 0:
            elapsed_partial = time.perf_counter() - started
            current = pd.read_csv(daily_path)
            partial_summary, partial_acceptance = summarize(current, files, elapsed_partial, dense_root)
            partial_summary.to_csv(output_dir / "dense_replay_strategy_summary_partial.csv", index=False)
            partial_acceptance.to_csv(output_dir / "dense_replay_acceptance_summary_partial.csv", index=False)
    daily_symbol = pd.read_csv(daily_path) if daily_path.exists() else pd.DataFrame()
    elapsed = time.perf_counter() - started
    summary, acceptance = summarize(daily_symbol, files, elapsed, dense_root)
    summary.to_csv(output_dir / "dense_replay_strategy_summary.csv", index=False)
    acceptance.to_csv(output_dir / "dense_replay_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Strategy Summary": summary,
            "Daily Symbol Sample": daily_symbol.head(120),
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase52_dense_lake_strategy_replay_synthetic_only_proxy",
        "dense_shards_scanned": len(files),
        "strategy_profile_rows": int(len(summary)),
        "synthetic_full_year_acceptance_ready": 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase52",
            generated_utc=generated_utc,
            inputs={"phase51_dense_lake": str(dense_root)},
            parameters={
                "threshold_quantile": threshold_quantile,
                "strategies": ";".join(item["strategy_id"] for item in STRATEGIES),
                "execution_profiles": ";".join(str(item["execution_profile"]) for item in EXECUTION_PROFILES),
                "limit_shards": limit_shards if limit_shards is not None else "none_full_lake",
            },
            outputs={
                "daily_symbol": str(output_dir / "dense_replay_daily_symbol.csv"),
                "strategy_summary": str(output_dir / "dense_replay_strategy_summary.csv"),
                "acceptance_summary": str(output_dir / "dense_replay_acceptance_summary.csv"),
                "report": str(output_dir / "phase52_dense_lake_strategy_replay_report.md"),
                "manifest": str(output_dir / "phase52_dense_lake_strategy_replay_manifest.json"),
            },
            random_seed="none_deterministic_dense_lake_sql_replay",
            scenario_ids="phase51_full_dense_symbol_month_lake",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase52_event_row_lag_profiles_from_phase12_execution_profiles",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase52_dense_lake_strategy_replay_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replay dense-lake strategies over the Phase51 full dense parquet lake.")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--threshold-quantile", type=float, default=0.95)
    parser.add_argument("--limit-shards", type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase52(args.dense_root, args.output_dir, args.base_dir, args.threshold_quantile, args.limit_shards)


if __name__ == "__main__":
    main()
