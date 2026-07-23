from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

from synthetic_l2.phase12_execution_simulator import EXECUTION_PROFILES
from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase52_dense_lake_strategy_replay import DEFAULT_ORDER_NOTIONAL_INR, _safe_path, profile_cost_bps
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE162_DIR = Path("outputs/phase162")
DEFAULT_PHASE163_DIR = Path("outputs/phase163")
DEFAULT_OUTPUT_DIR = Path("outputs/phase164")
DEFAULT_THRESHOLD_QUANTILE = 0.985

STRATEGIES = [
    {
        "strategy_id": "P164_S01_MLOFI_BREAKOUT",
        "source_strategy_id": "S01",
        "feature_family": "momentum_breakout_mlofi",
        "signal_sql": "case when abs(composite_flow) >= composite_flow_threshold and abs(one_tick_return) >= return_threshold then sign(composite_flow + one_tick_return * 100.0) else 0 end",
        "feature_status": "replayable_from_local_l1_l5_book_state",
    },
    {
        "strategy_id": "P164_S02_MULTI_LEVEL_OFI",
        "source_strategy_id": "S02",
        "feature_family": "multi_level_order_flow_imbalance",
        "signal_sql": "case when abs(l5_imbalance) >= l5_imbalance_threshold and spread_bps <= spread_bps_p75 then sign(l5_imbalance) else 0 end",
        "feature_status": "replayable_from_local_l1_l5_book_state",
    },
    {
        "strategy_id": "P164_S03_LIQUIDITY_VACUUM",
        "source_strategy_id": "S03",
        "feature_family": "liquidity_vacuum_breakout",
        "signal_sql": "case when l5_depth <= l5_depth_p10 and abs(one_tick_return) >= return_threshold then sign(one_tick_return) else 0 end",
        "feature_status": "replayable_from_local_l1_l5_book_state",
    },
    {
        "strategy_id": "P164_S04_TRADE_FLOW_DEPTH",
        "source_strategy_id": "S04",
        "feature_family": "trade_flow_depth_confirmation",
        "signal_sql": "case when abs(one_tick_return) >= return_threshold and sign(one_tick_return) = sign(l5_imbalance) and abs(l5_imbalance) >= l5_imbalance_threshold then sign(one_tick_return) else 0 end",
        "feature_status": "replayable_from_local_l1_l5_book_state",
    },
    {
        "strategy_id": "P164_S05_MICROPRICE_FILTER",
        "source_strategy_id": "S05",
        "feature_family": "microprice_with_depth_filter",
        "signal_sql": "case when abs(microprice_dev) >= microprice_threshold and abs(l1_imbalance) >= l1_imbalance_threshold and spread_bps <= spread_bps_p75 then sign(microprice_dev) else 0 end",
        "feature_status": "replayable_from_local_l1_l5_book_state",
    },
    {
        "strategy_id": "P164_S06_ABSORPTION_REVERSAL",
        "source_strategy_id": "S06",
        "feature_family": "absorption_exhaustion_reversal",
        "signal_sql": "case when abs(one_tick_return) >= return_threshold and sign(one_tick_return) != sign(l1_imbalance) and abs(l1_imbalance) >= l1_imbalance_threshold then -sign(one_tick_return) else 0 end",
        "feature_status": "replayable_from_local_l1_l5_book_state",
    },
    {
        "strategy_id": "P164_S07_IMBALANCE_MEAN_REVERSION",
        "source_strategy_id": "S07",
        "feature_family": "imbalance_mean_reversion",
        "signal_sql": "case when abs(l1_imbalance) >= l1_imbalance_threshold and spread_bps <= spread_bps_p75 then -sign(l1_imbalance) else 0 end",
        "feature_status": "replayable_from_local_l1_l5_book_state",
    },
    {
        "strategy_id": "P164_S08_CROSS_SYMBOL_LEAD_LAG_PLACEHOLDER",
        "source_strategy_id": "S08",
        "feature_family": "cross_symbol_lead_lag",
        "signal_sql": "0",
        "feature_status": "not_replayable_in_isolated_symbol_shard_requires_cross_symbol_month_cache",
    },
    {
        "strategy_id": "P164_S09_QUEUE_IMBALANCE_SCALP",
        "source_strategy_id": "S09",
        "feature_family": "queue_imbalance_scalping_guarded",
        "signal_sql": "case when abs(l1_imbalance) >= greatest(l1_imbalance_threshold, 0.85) and spread_bps <= spread_bps_median then sign(l1_imbalance) else 0 end",
        "feature_status": "replayable_from_local_l1_l5_book_state_guarded_not_phase52_dense_id",
    },
    {
        "strategy_id": "P164_S10_PASSIVE_CONTROL_NO_ALPHA",
        "source_strategy_id": "S10",
        "feature_family": "control_risk_plumbing",
        "signal_sql": "0",
        "feature_status": "control_only_no_alpha_replay",
    },
    {
        "strategy_id": "P164_S11_RISK_FILTER_CONTROL_NO_ALPHA",
        "source_strategy_id": "S11",
        "feature_family": "control_risk_plumbing",
        "signal_sql": "0",
        "feature_status": "control_only_no_alpha_replay",
    },
]


def load_inventory(path: Path, limit_shards: int | None, stop_after_new_shards: int | None, completed_paths: set[str]) -> list[dict[str, Any]]:
    inventory = pd.read_csv(path)
    inventory = inventory.sort_values(["trade_month", "symbol"], kind="mergesort").reset_index(drop=True)
    if limit_shards is not None:
        inventory = inventory.head(limit_shards).copy()
    inventory["_normalized_file_path"] = inventory["file_path"].astype(str).map(normalize_shard_path)
    pending = inventory[~inventory["_normalized_file_path"].isin(completed_paths)].copy()
    if stop_after_new_shards is not None:
        pending = pending.head(stop_after_new_shards).copy()
    pending = pending.drop(columns=["_normalized_file_path"])
    return pending.to_dict("records")


def normalize_shard_path(path: str | Path) -> str:
    return str(path).replace("\\", "/")


def write_progress(
    output_dir: Path,
    *,
    status: str,
    current_shard_index: int,
    completed_new_shards: int,
    path: str,
    started: float,
) -> None:
    progress = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "current_shard_index": current_shard_index,
        "completed_new_shards_this_run": completed_new_shards,
        "current_shard_path": path,
        "elapsed_seconds_this_run": time.perf_counter() - started,
    }
    (output_dir / "phase164_replay_progress.json").write_text(json.dumps(progress, indent=2), encoding="utf-8")


def query_shard(path: Path, shard_index: int, threshold_quantile: float) -> pd.DataFrame:
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
                    10000.0 * greatest(sell_1_price - buy_1_price, 0.01) / nullif(((buy_1_price + sell_1_price) / 2.0), 0.0) as spread_bps,
                    greatest(sell_1_price - buy_1_price, 0.01) as tick_size_proxy,
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
                    (last_price / nullif(lag(last_price) over (order by local_sequence_id), 0.0) - 1.0) as one_tick_return,
                    coalesce(is_duplicate, false) as is_duplicate,
                    coalesce(is_disconnect_gap, false) as is_disconnect_gap,
                    coalesce(is_out_of_order_injected, false) as is_out_of_order_injected
                from read_parquet('{_safe_path(path)}', union_by_name=true)
                where buy_1_price > 0 and sell_1_price > 0 and sell_1_price >= buy_1_price
            ),
            enriched as (
                select
                    *,
                    coalesce(l1_imbalance, 0.0) * 0.6 + coalesce(l5_imbalance, 0.0) * 0.4 as composite_flow
                from base
            ),
            thresholds as (
                select
                    quantile_cont(abs(l1_imbalance), {threshold_quantile}) as l1_imbalance_threshold,
                    quantile_cont(abs(l5_imbalance), {threshold_quantile}) as l5_imbalance_threshold,
                    quantile_cont(abs(composite_flow), {threshold_quantile}) as composite_flow_threshold,
                    quantile_cont(abs(microprice_dev), {threshold_quantile}) as microprice_threshold,
                    quantile_cont(abs(one_tick_return), {threshold_quantile}) as return_threshold,
                    quantile_cont(l5_depth, 0.10) as l5_depth_p10,
                    quantile_cont(spread_bps, 0.50) as spread_bps_median,
                    quantile_cont(spread_bps, 0.75) as spread_bps_p75
                from enriched
            )
            select
                enriched.*,
                {", ".join(f"{strategy['signal_sql']} as signal_{i}" for i, strategy in enumerate(STRATEGIES))}
            from enriched
            cross join thresholds
            """
        )
        union_parts = []
        for i, strategy in enumerate(STRATEGIES):
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
                        {shard_index}::integer as shard_index,
                        '{normalize_shard_path(path)}' as shard_path,
                        trade_date,
                        symbol,
                        '{strategy["strategy_id"]}' as strategy_id,
                        '{strategy["source_strategy_id"]}' as source_strategy_id,
                        '{strategy["feature_family"]}' as feature_family,
                        '{strategy["feature_status"]}' as feature_status,
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
                                lag(signal_{i}, {total_latency}) over (order by local_sequence_id) as executable_signal
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


def summarize(trade_ledger: pd.DataFrame, inventory: pd.DataFrame, elapsed_seconds: float, output_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if trade_ledger.empty:
        empty_summary = pd.DataFrame()
        acceptance = pd.DataFrame(
            [("phase164_replay_trade_rows", 0, "No replay trades generated")],
            columns=["metric", "value", "description"],
        )
        return empty_summary, empty_summary, acceptance

    daily = (
        trade_ledger.groupby(["trade_date", "strategy_id", "source_strategy_id", "feature_family", "feature_status", "execution_profile"], sort=True)
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
    for keys, group in daily.groupby(["strategy_id", "source_strategy_id", "feature_family", "feature_status", "execution_profile"], sort=True):
        strategy_id, source_strategy_id, feature_family, feature_status, execution_profile = keys
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
                "source_strategy_id": source_strategy_id,
                "feature_family": feature_family,
                "feature_status": feature_status,
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
    summary["synthetic_replay_candidate"] = summary["positive_after_costs"] & summary["risk_proxy_pass"]
    summary = summary.sort_values(["annual_net_pnl_inr", "trades"], ascending=[False, False], kind="mergesort").reset_index(drop=True)

    risk = (
        summary.groupby(["source_strategy_id", "feature_family"], sort=True)
        .agg(
            profile_rows=("strategy_id", "count"),
            positive_after_cost_rows=("positive_after_costs", "sum"),
            candidate_rows=("synthetic_replay_candidate", "sum"),
            best_annual_net_pnl_inr=("annual_net_pnl_inr", "max"),
            worst_max_drawdown_inr=("max_drawdown_inr", "min"),
            max_trade_count=("trades", "max"),
        )
        .reset_index()
    )

    shards_scanned = int(trade_ledger["shard_path"].nunique())
    expected_shards = int(len(inventory))
    acceptance = pd.DataFrame(
        [
            ("phase164_contract_id", "P164_SYNTHETIC_ONLY_FULL_YEAR_REPLAY", "Replay contract id inherited from Phase163"),
            ("phase164_shards_scanned", shards_scanned, "Phase162 dense parquet shards scanned in current completed ledger"),
            ("phase164_expected_shards", expected_shards, "Expected Phase162 inventory shards"),
            ("phase164_full_year_replay_complete", int(shards_scanned >= expected_shards and expected_shards > 0), "1 means all Phase162 shards are represented"),
            ("phase164_strategy_profile_rows", int(len(summary)), "Strategy/profile summary rows"),
            ("phase164_replay_trade_rows", int(summary["trades"].sum()), "Aggregate synthetic-only replay trade count"),
            ("phase164_positive_after_cost_rows", int(summary["positive_after_costs"].sum()), "Strategy/profile rows positive after costs"),
            ("phase164_synthetic_replay_candidate_rows", int(summary["synthetic_replay_candidate"].sum()), "Rows positive after costs and risk proxy pass"),
            ("phase164_elapsed_seconds", float(elapsed_seconds), "Elapsed seconds for this runner invocation"),
            ("phase164_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha equity intraday NSE charge formula"),
            ("phase164_strategy_promotion_allowed", 0, "Strategy promotion remains closed"),
            ("phase164_paper_or_live_acceptance_allowed", 0, "Broker/paper/live acceptance remains closed"),
            ("phase164_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from synthetic-only replay"),
            ("phase164_next_best_action", "continue_phase164_until_full_year_complete_then_verdict", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    return summary, risk, acceptance


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase164 Synthetic-only Full-year Replay",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase164 replays guarded S01-S11 diagnostic strategies over the Phase162 full-year dense L2 lake.",
        "This is synthetic-only diagnostic evidence. It is not broker, paper/live, contract-note, promoted-signal, or deployable profitability evidence.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase164_synthetic_only_full_year_replay_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase164(
    phase162_dir: Path,
    phase163_dir: Path,
    output_dir: Path,
    base_dir: Path,
    threshold_quantile: float,
    limit_shards: int | None,
    stop_after_new_shards: int | None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    inventory_path = phase162_dir / "phase162_dense_full_year_inventory.csv"
    inventory = pd.read_csv(inventory_path).sort_values(["trade_month", "symbol"], kind="mergesort").reset_index(drop=True)
    if limit_shards is not None:
        inventory_scope = inventory.head(limit_shards).copy()
    else:
        inventory_scope = inventory.copy()
    ledger_path = output_dir / "phase164_aggregate_trade_ledger.csv"
    completed_paths: set[str] = set()
    if ledger_path.exists():
        completed = pd.read_csv(ledger_path, usecols=["shard_path"])
        completed_paths = set(completed["shard_path"].astype(str).map(normalize_shard_path).unique())
    shards = load_inventory(inventory_path, limit_shards, stop_after_new_shards, completed_paths)
    started = time.perf_counter()
    completed_new = 0
    for record in shards:
        shard_index = int(inventory.index[inventory["file_path"].astype(str).eq(str(record["file_path"]))][0]) + 1
        write_progress(output_dir, status="running", current_shard_index=shard_index, completed_new_shards=completed_new, path=str(record["file_path"]), started=started)
        frame = query_shard(Path(record["file_path"]), shard_index, threshold_quantile)
        if not frame.empty:
            frame.to_csv(ledger_path, mode="a", header=not ledger_path.exists(), index=False)
        completed_new += 1
        write_progress(output_dir, status="checkpointed", current_shard_index=shard_index, completed_new_shards=completed_new, path=str(record["file_path"]), started=started)

    trade_ledger = pd.read_csv(ledger_path) if ledger_path.exists() else pd.DataFrame()
    if not trade_ledger.empty:
        trade_ledger["shard_path"] = trade_ledger["shard_path"].astype(str).map(normalize_shard_path)
        before = len(trade_ledger)
        trade_ledger = trade_ledger.drop_duplicates(
            subset=["shard_path", "trade_date", "symbol", "strategy_id", "execution_profile"],
            keep="last",
        ).sort_values(["shard_index", "trade_date", "symbol", "strategy_id", "execution_profile"], kind="mergesort")
        if len(trade_ledger) != before:
            trade_ledger.to_csv(ledger_path, index=False)
    elapsed = time.perf_counter() - started
    summary, risk, acceptance = summarize(trade_ledger, inventory_scope, elapsed, output_dir)
    summary.to_csv(output_dir / "phase164_strategy_profile_summary.csv", index=False)
    risk.to_csv(output_dir / "phase164_risk_summary.csv", index=False)
    acceptance.to_csv(output_dir / "phase164_synthetic_only_full_year_replay_acceptance_summary.csv", index=False)
    pd.DataFrame(STRATEGIES).to_csv(output_dir / "phase164_strategy_catalog.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Strategy Profile Summary": summary,
            "Risk Summary": risk,
            "Strategy Catalog": pd.DataFrame(STRATEGIES),
            "Aggregate Trade Ledger Sample": trade_ledger.head(120),
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase164_synthetic_only_full_year_replay",
        **reproducibility_fields(
            artifact_id="phase164",
            generated_utc=generated_utc,
            inputs={
                "phase162_inventory": str(inventory_path),
                "phase163_contract": str(phase163_dir / "phase163_phase164_replay_contract.csv"),
                "phase163_work_queue": str(phase163_dir / "phase163_synthetic_only_replay_work_queue.csv"),
            },
            parameters={
                "threshold_quantile": threshold_quantile,
                "limit_shards": limit_shards if limit_shards is not None else "none_full_inventory",
                "stop_after_new_shards": stop_after_new_shards if stop_after_new_shards is not None else "none",
                "strategies": ";".join(strategy["strategy_id"] for strategy in STRATEGIES),
                "execution_profiles": ";".join(str(profile["execution_profile"]) for profile in EXECUTION_PROFILES),
                "strategy_promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "azure_read_policy": "forbidden_for_analysis_download_first_then_local",
            },
            outputs={
                "aggregate_trade_ledger": str(ledger_path),
                "strategy_profile_summary": str(output_dir / "phase164_strategy_profile_summary.csv"),
                "risk_summary": str(output_dir / "phase164_risk_summary.csv"),
                "acceptance_summary": str(output_dir / "phase164_synthetic_only_full_year_replay_acceptance_summary.csv"),
                "strategy_catalog": str(output_dir / "phase164_strategy_catalog.csv"),
                "report": str(output_dir / "phase164_synthetic_only_full_year_replay_report.md"),
                "manifest": str(output_dir / "phase164_synthetic_only_full_year_replay_manifest.json"),
            },
            random_seed="none_deterministic_phase164_sql_replay",
            scenario_ids="phase162_distributional_full_year_dense_l2",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase12_execution_profiles_v1_reused_for_phase164",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase164_synthetic_only_full_year_replay_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    if shards:
        write_progress(
            output_dir,
            status="complete" if int(acceptance.loc[acceptance["metric"].eq("phase164_full_year_replay_complete"), "value"].iloc[0]) == 1 else "partial",
            current_shard_index=int(inventory.index[inventory["file_path"].astype(str).eq(str(shards[-1]["file_path"]))][0]) + 1,
            completed_new_shards=completed_new,
            path=str(shards[-1]["file_path"]),
            started=started,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase164 synthetic-only full-year replay over Phase162 dense L2.")
    parser.add_argument("--phase162-dir", type=Path, default=DEFAULT_PHASE162_DIR)
    parser.add_argument("--phase163-dir", type=Path, default=DEFAULT_PHASE163_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--threshold-quantile", type=float, default=DEFAULT_THRESHOLD_QUANTILE)
    parser.add_argument("--limit-shards", type=int)
    parser.add_argument("--stop-after-new-shards", type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase164(
        args.phase162_dir,
        args.phase163_dir,
        args.output_dir,
        args.base_dir,
        args.threshold_quantile,
        args.limit_shards,
        args.stop_after_new_shards,
    )


if __name__ == "__main__":
    main()
