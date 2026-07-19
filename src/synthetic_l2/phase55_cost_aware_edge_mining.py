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
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, calculate_equity_intraday_nse_charges


DEFAULT_DENSE_ROOT = Path("raw_synthetic_l2_dense_full_year")
DEFAULT_OUTPUT_DIR = Path("outputs/phase55")
DEFAULT_ORDER_NOTIONAL_INR = 100_000.0


COST_AWARE_CANDIDATES: list[dict[str, Any]] = [
    {
        "candidate_id": "S55_MOM_Q995_H20_COST1P25",
        "feature_family": "one_tick_momentum",
        "raw_signal": "case when abs(one_tick_return) >= momentum_q995 and spread_bps <= spread_bps_q75 then sign(one_tick_return) else 0 end",
        "forward_horizon_events": 20,
        "cooldown_modulus": 25,
        "cost_hurdle_multiplier": 1.25,
        "requires_signal_transition": True,
        "candidate_role": "deployable_cost_hurdle_test",
    },
    {
        "candidate_id": "S55_MOM_Q999_H50_COST1P50",
        "feature_family": "one_tick_momentum",
        "raw_signal": "case when abs(one_tick_return) >= momentum_q999 and spread_bps <= spread_bps_q50 then sign(one_tick_return) else 0 end",
        "forward_horizon_events": 50,
        "cooldown_modulus": 100,
        "cost_hurdle_multiplier": 1.50,
        "requires_signal_transition": True,
        "candidate_role": "deployable_cost_hurdle_test",
    },
    {
        "candidate_id": "S55_MOM_Q999_H100_COST1P50",
        "feature_family": "one_tick_momentum",
        "raw_signal": "case when abs(one_tick_return) >= momentum_q999 and spread_bps <= spread_bps_q50 then sign(one_tick_return) else 0 end",
        "forward_horizon_events": 100,
        "cooldown_modulus": 150,
        "cost_hurdle_multiplier": 1.50,
        "requires_signal_transition": True,
        "candidate_role": "deployable_cost_hurdle_test",
    },
    {
        "candidate_id": "S55_IMB_Q999_H50_COST1P50",
        "feature_family": "l1_imbalance",
        "raw_signal": "case when abs(l1_imbalance) >= l1_q999 and spread_bps <= spread_bps_q50 and l1_depth_notional >= depth_notional_q75 then sign(l1_imbalance) else 0 end",
        "forward_horizon_events": 50,
        "cooldown_modulus": 100,
        "cost_hurdle_multiplier": 1.50,
        "requires_signal_transition": True,
        "candidate_role": "deployable_cost_hurdle_test",
    },
    {
        "candidate_id": "S55_MICRO_Q999_H50_COST1P50",
        "feature_family": "microprice",
        "raw_signal": "case when abs(microprice_dev) >= micro_q999 and spread_bps <= spread_bps_q50 then sign(microprice_dev) else 0 end",
        "forward_horizon_events": 50,
        "cooldown_modulus": 100,
        "cost_hurdle_multiplier": 1.50,
        "requires_signal_transition": True,
        "candidate_role": "deployable_cost_hurdle_test",
    },
    {
        "candidate_id": "S55_ORACLE_H20_COST_CEILING",
        "feature_family": "oracle_forward_return",
        "raw_signal": "case when abs(future_return_h20) >= retail_cost_return * 1.25 then sign(future_return_h20) else 0 end",
        "forward_horizon_events": 20,
        "cooldown_modulus": 25,
        "cost_hurdle_multiplier": 1.25,
        "requires_signal_transition": False,
        "candidate_role": "nondeployable_cost_ceiling",
    },
]


def parquet_files(dense_root: Path, limit_shards: int | None = None) -> list[Path]:
    files = sorted(dense_root.glob("trade_month=*/symbol=*/part-00000.parquet"))
    if not files:
        raise FileNotFoundError(f"No dense parquet files under {dense_root}")
    return files[:limit_shards] if limit_shards is not None else files


def _safe_path(path: Path) -> str:
    return path.as_posix().replace("'", "''")


def retail_profile() -> dict[str, Any]:
    for profile in EXECUTION_PROFILES:
        if profile["execution_profile"] == "retail_marketable_default":
            return dict(profile)
    raise KeyError("retail_marketable_default execution profile is missing")


def profile_cost_bps(profile: dict[str, Any]) -> float:
    if not bool(profile.get("apply_zerodha_equity_intraday_charges", False)):
        return 0.0
    charges = calculate_equity_intraday_nse_charges(
        buy_value_inr=float(profile.get("order_notional_inr", DEFAULT_ORDER_NOTIONAL_INR)),
        sell_value_inr=float(profile.get("order_notional_inr", DEFAULT_ORDER_NOTIONAL_INR)),
    )
    return float(charges.effective_bps_on_buy_value)


def candidate_catalog() -> pd.DataFrame:
    return pd.DataFrame(COST_AWARE_CANDIDATES)


def _bounded_source_sql(path: Path, max_rows_per_shard: int | None) -> str:
    source = f"read_parquet('{_safe_path(path)}', union_by_name=true)"
    filter_sql = "buy_1_price > 0 and sell_1_price > 0 and sell_1_price >= buy_1_price"
    if max_rows_per_shard is not None:
        filter_sql += f" and local_sequence_id <= {int(max_rows_per_shard)}"
    return f"select * from {source} where {filter_sql}"


def query_shard(path: Path, max_rows_per_shard: int | None) -> pd.DataFrame:
    profile = retail_profile()
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
                    greatest(sell_1_price - buy_1_price, 0.01) as spread,
                    greatest(sell_1_price - buy_1_price, 0.01) as tick_size_proxy,
                    greatest(((sell_1_price - buy_1_price) / nullif(((buy_1_price + sell_1_price) / 2.0), 0.0)) * 10000.0, 0.0) as spread_bps,
                    (((buy_1_price * buy_1_quantity) + (sell_1_price * sell_1_quantity)) / 2.0) as l1_depth_notional,
                    ((buy_1_quantity - sell_1_quantity) / nullif((buy_1_quantity + sell_1_quantity), 0.0)) as l1_imbalance,
                    (((sell_1_price * buy_1_quantity + buy_1_price * sell_1_quantity) / nullif((buy_1_quantity + sell_1_quantity), 0.0))
                        - ((buy_1_price + sell_1_price) / 2.0)) / nullif(((buy_1_price + sell_1_price) / 2.0), 0.0) as microprice_dev,
                    (last_price / nullif(lag(last_price) over (order by local_sequence_id), 0.0) - 1.0) as one_tick_return,
                    coalesce(is_duplicate, false) as is_duplicate,
                    coalesce(is_disconnect_gap, false) as is_disconnect_gap,
                    coalesce(is_out_of_order_injected, false) as is_out_of_order_injected
                from ({_bounded_source_sql(path, max_rows_per_shard)})
            ),
            enriched as (
                select
                    *,
                    lead(mid_price, 20) over (order by local_sequence_id) / nullif(mid_price, 0.0) - 1.0 as future_return_h20,
                    (((spread / 2.0) / nullif(mid_price, 0.0))
                      + ({slippage_ticks} * tick_size_proxy / nullif(mid_price, 0.0))
                      + ({impact_bps} / 10000.0)
                      + ({zerodha_bps} / 10000.0)) as retail_cost_return
                from base
            ),
            thresholds as (
                select
                    quantile_cont(abs(l1_imbalance), 0.999) as l1_q999,
                    quantile_cont(abs(microprice_dev), 0.999) as micro_q999,
                    quantile_cont(abs(one_tick_return), 0.995) as momentum_q995,
                    quantile_cont(abs(one_tick_return), 0.999) as momentum_q999,
                    quantile_cont(spread_bps, 0.50) as spread_bps_q50,
                    quantile_cont(spread_bps, 0.75) as spread_bps_q75,
                    quantile_cont(l1_depth_notional, 0.75) as depth_notional_q75
                from enriched
            )
            select enriched.*, thresholds.*
            from enriched
            cross join thresholds
            """
        )
        union_parts: list[str] = []
        for candidate in COST_AWARE_CANDIDATES:
            raw_signal = str(candidate["raw_signal"])
            horizon = int(candidate["forward_horizon_events"])
            cooldown = int(candidate["cooldown_modulus"])
            hurdle = float(candidate["cost_hurdle_multiplier"])
            transition_filter = (
                "and raw_signal != coalesce(lag(raw_signal) over (order by local_sequence_id), 0)"
                if bool(candidate["requires_signal_transition"])
                else ""
            )
            union_parts.append(
                f"""
                select
                    trade_date,
                    symbol,
                    '{candidate["candidate_id"]}' as candidate_id,
                    '{candidate["feature_family"]}' as feature_family,
                    '{candidate["candidate_role"]}' as candidate_role,
                    '{profile["execution_profile"]}' as execution_profile,
                    count(*)::bigint as trades,
                    sum(gross_return)::double as sum_gross_return,
                    sum(cost_return)::double as sum_cost_return,
                    sum(edge_over_cost_return)::double as sum_edge_over_cost_return,
                    sum(gross_return - cost_return)::double as sum_net_return,
                    avg(gross_return)::double as mean_gross_return,
                    avg(cost_return)::double as mean_cost_return,
                    avg(edge_over_cost_return)::double as mean_edge_over_cost_return,
                    avg(gross_return - cost_return)::double as mean_net_return,
                    sum((gross_return - cost_return) * {order_notional})::double as net_pnl_inr,
                    min((gross_return - cost_return) * {order_notional})::double as worst_trade_pnl_inr,
                    max((gross_return - cost_return) * {order_notional})::double as best_trade_pnl_inr,
                    {horizon}::integer as forward_horizon_events,
                    {cooldown}::integer as cooldown_modulus,
                    {hurdle}::double as cost_hurdle_multiplier,
                    {total_latency}::integer as total_latency_events,
                    {slippage_ticks}::double as fixed_slippage_ticks,
                    {impact_bps}::double as internal_impact_bps,
                    {zerodha_bps}::double as zerodha_charge_bps
                from (
                    select
                        trade_date,
                        symbol,
                        executable_signal,
                        executable_signal * (future_mid_price / nullif(mid_price, 0.0) - 1.0) as gross_return,
                        cost_return,
                        abs(executable_signal * (future_mid_price / nullif(mid_price, 0.0) - 1.0)) - ({hurdle} * cost_return) as edge_over_cost_return
                    from (
                        select
                            *,
                            lag(entry_signal, {total_latency}) over (order by local_sequence_id) as executable_signal,
                            lead(mid_price, {horizon}) over (order by local_sequence_id) as future_mid_price,
                            (((spread / 2.0) / nullif(mid_price, 0.0))
                              + ({slippage_ticks} * tick_size_proxy / nullif(mid_price, 0.0))
                              + ({impact_bps} / 10000.0)
                              + ({zerodha_bps} / 10000.0)) as cost_return
                        from (
                            select
                                *,
                                case
                                    when raw_signal != 0
                                         and local_sequence_id % {cooldown} = 0
                                         {transition_filter}
                                    then raw_signal
                                    else 0
                                end as entry_signal
                            from (
                                select *, {raw_signal} as raw_signal
                                from dense_features
                            )
                        )
                    )
                    where executable_signal != 0
                      and future_mid_price is not null
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
        return pd.DataFrame(), pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for (candidate_id, feature_family, candidate_role), group in daily_symbol.groupby(
        ["candidate_id", "feature_family", "candidate_role"], sort=True
    ):
        group = group.sort_values(["trade_date", "symbol"], kind="mergesort").copy()
        group["running_net_pnl_inr"] = group["net_pnl_inr"].cumsum()
        group["running_peak_inr"] = group["running_net_pnl_inr"].cummax()
        group["drawdown_inr"] = group["running_net_pnl_inr"] - group["running_peak_inr"]
        trades = int(group["trades"].sum())
        rows.append(
            {
                "candidate_id": candidate_id,
                "feature_family": feature_family,
                "candidate_role": candidate_role,
                "symbols": int(group["symbol"].nunique()),
                "trade_dates": int(group["trade_date"].nunique()),
                "trades": trades,
                "net_pnl_inr": float(group["net_pnl_inr"].sum()),
                "gross_pnl_proxy_inr": float(group["sum_gross_return"].sum() * DEFAULT_ORDER_NOTIONAL_INR),
                "cost_pnl_drag_proxy_inr": float(group["sum_cost_return"].sum() * DEFAULT_ORDER_NOTIONAL_INR),
                "edge_over_cost_proxy_inr": float(group["sum_edge_over_cost_return"].sum() * DEFAULT_ORDER_NOTIONAL_INR),
                "mean_gross_return_per_trade": float(group["sum_gross_return"].sum() / trades) if trades else 0.0,
                "mean_cost_return_per_trade": float(group["sum_cost_return"].sum() / trades) if trades else 0.0,
                "mean_edge_over_cost_return_per_trade": float(group["sum_edge_over_cost_return"].sum() / trades) if trades else 0.0,
                "mean_net_return_per_trade": float(group["sum_net_return"].sum() / trades) if trades else 0.0,
                "positive_symbol_rows": int((group["net_pnl_inr"] > 0).sum()),
                "positive_symbol_fraction": float((group["net_pnl_inr"] > 0).mean()),
                "gross_positive_symbol_rows": int((group["sum_gross_return"] > 0).sum()),
                "edge_over_cost_positive_symbol_rows": int((group["sum_edge_over_cost_return"] > 0).sum()),
                "worst_symbol_net_pnl_inr": float(group["net_pnl_inr"].min()),
                "best_symbol_net_pnl_inr": float(group["net_pnl_inr"].max()),
                "max_drawdown_inr": float(group["drawdown_inr"].min()),
                "worst_trade_pnl_inr": float(group["worst_trade_pnl_inr"].min()),
                "best_trade_pnl_inr": float(group["best_trade_pnl_inr"].max()),
                "forward_horizon_events": int(group["forward_horizon_events"].iloc[0]),
                "cooldown_modulus": int(group["cooldown_modulus"].iloc[0]),
                "cost_hurdle_multiplier": float(group["cost_hurdle_multiplier"].iloc[0]),
            }
        )
    observed = {row["candidate_id"] for row in rows}
    for candidate in COST_AWARE_CANDIDATES:
        if candidate["candidate_id"] in observed:
            continue
        rows.append(
            {
                "candidate_id": candidate["candidate_id"],
                "feature_family": candidate["feature_family"],
                "candidate_role": candidate["candidate_role"],
                "symbols": 0,
                "trade_dates": 0,
                "trades": 0,
                "net_pnl_inr": 0.0,
                "gross_pnl_proxy_inr": 0.0,
                "cost_pnl_drag_proxy_inr": 0.0,
                "edge_over_cost_proxy_inr": 0.0,
                "mean_gross_return_per_trade": 0.0,
                "mean_cost_return_per_trade": 0.0,
                "mean_edge_over_cost_return_per_trade": 0.0,
                "mean_net_return_per_trade": 0.0,
                "positive_symbol_rows": 0,
                "positive_symbol_fraction": 0.0,
                "gross_positive_symbol_rows": 0,
                "edge_over_cost_positive_symbol_rows": 0,
                "worst_symbol_net_pnl_inr": 0.0,
                "best_symbol_net_pnl_inr": 0.0,
                "max_drawdown_inr": 0.0,
                "worst_trade_pnl_inr": 0.0,
                "best_trade_pnl_inr": 0.0,
                "forward_horizon_events": int(candidate["forward_horizon_events"]),
                "cooldown_modulus": int(candidate["cooldown_modulus"]),
                "cost_hurdle_multiplier": float(candidate["cost_hurdle_multiplier"]),
            }
        )
    summary = pd.DataFrame(rows)
    summary["deployable_candidate"] = summary["candidate_role"] == "deployable_cost_hurdle_test"
    summary["positive_after_costs"] = summary["net_pnl_inr"] > 0
    summary["cost_aware_scale_candidate"] = (
        summary["deployable_candidate"]
        & summary["positive_after_costs"]
        & (summary["mean_edge_over_cost_return_per_trade"] > 0)
        & (summary["positive_symbol_fraction"] >= 0.50)
        & (summary["trades"] >= 20)
    )
    summary = summary.sort_values(["net_pnl_inr", "edge_over_cost_proxy_inr"], ascending=[False, False], kind="mergesort").reset_index(
        drop=True
    )
    traded_deployable = summary["deployable_candidate"] & (summary["trades"] > 0)
    acceptance = pd.DataFrame(
        [
            ("phase55_dense_shards_scanned", len(files), "Dense parquet shards scanned"),
            ("phase55_trade_rows", int(summary["trades"].sum()), "Aggregated candidate trade rows"),
            ("phase55_candidate_rows", len(summary), "Candidate result rows"),
            ("phase55_deployable_positive_after_cost_rows", int((summary["deployable_candidate"] & summary["positive_after_costs"]).sum()), "Deployable candidates positive after retail costs"),
            ("phase55_cost_aware_scale_candidate_rows", int(summary["cost_aware_scale_candidate"].sum()), "Deployable candidates passing cost-aware scale gate"),
            ("phase55_non_deployable_oracle_positive_rows", int(((summary["candidate_role"] == "nondeployable_cost_ceiling") & summary["positive_after_costs"]).sum()), "Oracle ceiling rows positive after costs"),
            (
                "phase55_best_traded_deployable_net_pnl_inr",
                float(summary.loc[traded_deployable, "net_pnl_inr"].max()) if bool(traded_deployable.any()) else 0.0,
                "Best deployable candidate net P&L among candidates that emitted at least one trade",
            ),
            ("phase55_best_any_net_pnl_inr", float(summary["net_pnl_inr"].max()), "Best candidate net P&L including nondeployable oracle ceilings"),
            ("phase55_elapsed_seconds", elapsed_seconds, "Replay elapsed seconds"),
            ("phase55_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha cost model used"),
            ("phase55_recommend_scale_deployable_to_full_year", int(summary["cost_aware_scale_candidate"].sum() > 0), "1 means at least one deployable cost-aware candidate deserves a wider dense replay"),
        ],
        columns=["metric", "value", "description"],
    )
    return summary, acceptance


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase55 Cost-Aware Dense Edge Mining",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase55 responds to the Phase53/Phase54 finding that dense marketable retail micro-trading is dominated by costs.",
        "It mines bounded dense shards with explicit cost-hurdle metrics before any full-year replay is authorized.",
        "The oracle ceiling row is nondeployable and exists only to show whether the data contains enough forward movement to beat costs in principle.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase55_cost_aware_edge_mining_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase55(dense_root: Path, output_dir: Path, base_dir: Path, limit_shards: int | None, max_rows_per_shard: int | None) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    files = parquet_files(dense_root, limit_shards=limit_shards)
    started = time.perf_counter()
    frames: list[pd.DataFrame] = []
    for shard_index, path in enumerate(files, start=1):
        shard_frame = query_shard(path, max_rows_per_shard)
        shard_frame.insert(0, "shard_index", shard_index)
        shard_frame.insert(1, "shard_path", str(path))
        frames.append(shard_frame)
    daily_symbol = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    elapsed = time.perf_counter() - started
    summary, acceptance = summarize(daily_symbol, files, elapsed, dense_root)
    catalog = candidate_catalog()

    catalog.to_csv(output_dir / "cost_aware_candidate_catalog.csv", index=False)
    daily_symbol.to_csv(output_dir / "cost_aware_edge_daily_symbol.csv", index=False)
    summary.to_csv(output_dir / "cost_aware_edge_summary.csv", index=False)
    acceptance.to_csv(output_dir / "cost_aware_edge_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Candidate Catalog": catalog,
            "Candidate Summary": summary,
            "Daily Symbol Sample": daily_symbol.head(120),
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase55_cost_aware_dense_edge_mining",
        "dense_shards_scanned": len(files),
        "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
        "recommend_scale_deployable_to_full_year": int(summary["cost_aware_scale_candidate"].sum() > 0) if not summary.empty else 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase55",
            generated_utc=generated_utc,
            inputs={
                "phase51_dense_lake": str(dense_root),
                "phase54_selective_replay": "outputs/phase54/phase54_selective_dense_replay_report.md",
            },
            parameters={
                "limit_shards": limit_shards if limit_shards is not None else "none_full_lake",
                "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
                "candidates": ";".join(item["candidate_id"] for item in COST_AWARE_CANDIDATES),
                "execution_profile": retail_profile()["execution_profile"],
                "scale_gate": "deployable_and_positive_after_costs_and_mean_edge_over_cost_gt_0_and_positive_symbol_fraction_ge_0_50_and_trades_ge_20",
            },
            outputs={
                "candidate_catalog": str(output_dir / "cost_aware_candidate_catalog.csv"),
                "daily_symbol": str(output_dir / "cost_aware_edge_daily_symbol.csv"),
                "summary": str(output_dir / "cost_aware_edge_summary.csv"),
                "acceptance_summary": str(output_dir / "cost_aware_edge_acceptance_summary.csv"),
                "report": str(output_dir / "phase55_cost_aware_edge_mining_report.md"),
                "manifest": str(output_dir / "phase55_cost_aware_edge_mining_manifest.json"),
            },
            random_seed="none_deterministic_dense_lake_sql_mining",
            scenario_ids="phase55_bounded_first_shards_from_phase51_dense_lake",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase55_retail_marketable_default_event_lag",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase55_cost_aware_edge_mining_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mine cost-aware dense edge candidates over bounded dense shards.")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--limit-shards", type=int, default=8)
    parser.add_argument("--max-rows-per-shard", type=int, default=250_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase55(args.dense_root, args.output_dir, args.base_dir, args.limit_shards, args.max_rows_per_shard)


if __name__ == "__main__":
    main()
