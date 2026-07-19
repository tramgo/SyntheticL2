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
DEFAULT_OUTPUT_DIR = Path("outputs/phase54")
DEFAULT_ORDER_NOTIONAL_INR = 100_000.0


SELECTIVE_VARIANTS: list[dict[str, Any]] = [
    {
        "variant_id": "S54_MOM_Q995_H20_TRANSITION",
        "feature_family": "one_tick_momentum",
        "raw_signal": "case when abs(one_tick_return) >= momentum_q995 and spread_bps <= spread_bps_q75 then sign(one_tick_return) else 0 end",
        "forward_horizon_events": 20,
        "cooldown_modulus": 25,
        "requires_signal_transition": True,
        "design_intent": "Trade only the strongest momentum bursts, wait twenty dense events, and avoid repeated same-side firing.",
    },
    {
        "variant_id": "S54_MOM_Q999_H50_LOWSPREAD",
        "feature_family": "one_tick_momentum",
        "raw_signal": "case when abs(one_tick_return) >= momentum_q999 and spread_bps <= spread_bps_q50 then sign(one_tick_return) else 0 end",
        "forward_horizon_events": 50,
        "cooldown_modulus": 100,
        "requires_signal_transition": True,
        "design_intent": "Extreme momentum-only gate with a longer horizon and low-spread filter to test whether turnover was the dominant Phase53 failure.",
    },
    {
        "variant_id": "S54_CONTRA_Q995_H20_STRETCH",
        "feature_family": "one_tick_contrarian",
        "raw_signal": "case when abs(one_tick_return) >= momentum_q995 and spread_bps <= spread_bps_q75 then -sign(one_tick_return) else 0 end",
        "forward_horizon_events": 20,
        "cooldown_modulus": 25,
        "requires_signal_transition": True,
        "design_intent": "Contrarian mirror of the strongest momentum bursts, included because Phase53 gross edge was tiny and direction may be unstable.",
    },
    {
        "variant_id": "S54_IMB_Q995_H20_DEPTH",
        "feature_family": "l1_imbalance",
        "raw_signal": "case when abs(l1_imbalance) >= l1_q995 and spread_bps <= spread_bps_q50 and l1_depth_notional >= depth_notional_q50 then sign(l1_imbalance) else 0 end",
        "forward_horizon_events": 20,
        "cooldown_modulus": 50,
        "requires_signal_transition": True,
        "design_intent": "High-confidence L1 imbalance with both low-spread and displayed-depth filters.",
    },
    {
        "variant_id": "S54_MICRO_Q995_H20_LOWSPREAD",
        "feature_family": "microprice",
        "raw_signal": "case when abs(microprice_dev) >= micro_q995 and spread_bps <= spread_bps_q50 then sign(microprice_dev) else 0 end",
        "forward_horizon_events": 20,
        "cooldown_modulus": 50,
        "requires_signal_transition": True,
        "design_intent": "Selective microprice deviation variant with a low-spread guardrail.",
    },
]


def parquet_files(dense_root: Path, limit_shards: int | None = None) -> list[Path]:
    files = sorted(dense_root.glob("trade_month=*/symbol=*/part-00000.parquet"))
    if not files:
        raise FileNotFoundError(f"No dense parquet files under {dense_root}")
    return files[:limit_shards] if limit_shards is not None else files


def _safe_path(path: Path) -> str:
    return path.as_posix().replace("'", "''")


def selected_execution_profiles() -> list[dict[str, Any]]:
    allowed = {"zero_latency_spread_only_control", "retail_marketable_default"}
    return [dict(item) for item in EXECUTION_PROFILES if str(item["execution_profile"]) in allowed]


def profile_cost_bps(profile: dict[str, Any]) -> float:
    if not bool(profile.get("apply_zerodha_equity_intraday_charges", False)):
        return 0.0
    charges = calculate_equity_intraday_nse_charges(
        buy_value_inr=float(profile.get("order_notional_inr", DEFAULT_ORDER_NOTIONAL_INR)),
        sell_value_inr=float(profile.get("order_notional_inr", DEFAULT_ORDER_NOTIONAL_INR)),
    )
    return float(charges.effective_bps_on_buy_value)


def variant_catalog() -> pd.DataFrame:
    return pd.DataFrame(SELECTIVE_VARIANTS)


def _bounded_source_sql(path: Path, max_rows_per_shard: int | None) -> str:
    source = f"read_parquet('{_safe_path(path)}', union_by_name=true)"
    validity_filter = "buy_1_price > 0 and sell_1_price > 0 and sell_1_price >= buy_1_price"
    if max_rows_per_shard is None:
        return f"select * from {source} where {validity_filter}"
    return f"select * from {source} where {validity_filter} and local_sequence_id <= {int(max_rows_per_shard)}"


def query_shard(path: Path, shard_index: int, max_rows_per_shard: int | None) -> pd.DataFrame:
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
            thresholds as (
                select
                    quantile_cont(abs(l1_imbalance), 0.995) as l1_q995,
                    quantile_cont(abs(microprice_dev), 0.995) as micro_q995,
                    quantile_cont(abs(one_tick_return), 0.995) as momentum_q995,
                    quantile_cont(abs(one_tick_return), 0.999) as momentum_q999,
                    quantile_cont(spread_bps, 0.50) as spread_bps_q50,
                    quantile_cont(spread_bps, 0.75) as spread_bps_q75,
                    quantile_cont(l1_depth_notional, 0.50) as depth_notional_q50
                from base
            )
            select base.*, thresholds.*
            from base
            cross join thresholds
            """
        )
        union_parts: list[str] = []
        for variant in SELECTIVE_VARIANTS:
            raw_signal = str(variant["raw_signal"])
            horizon = int(variant["forward_horizon_events"])
            cooldown = int(variant["cooldown_modulus"])
            transition_filter = (
                "and raw_signal != coalesce(lag(raw_signal) over (order by local_sequence_id), 0)"
                if bool(variant["requires_signal_transition"])
                else ""
            )
            for profile in selected_execution_profiles():
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
                        '{variant["variant_id"]}' as variant_id,
                        '{variant["feature_family"]}' as feature_family,
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
                        max((gross_return - cost_return) * {order_notional})::double as best_trade_pnl_inr,
                        {horizon}::integer as forward_horizon_events,
                        {cooldown}::integer as cooldown_modulus,
                        {total_latency}::integer as total_latency_events,
                        {slippage_ticks}::double as fixed_slippage_ticks,
                        {impact_bps}::double as internal_impact_bps,
                        {zerodha_bps}::double as zerodha_charge_bps
                    from (
                        select
                            trade_date,
                            symbol,
                            executable_signal,
                            (executable_signal * (future_mid_price / nullif(mid_price, 0.0) - 1.0)) as gross_return,
                            ((spread / 2.0) / nullif(mid_price, 0.0))
                              + ({slippage_ticks} * tick_size_proxy / nullif(mid_price, 0.0))
                              + ({impact_bps} / 10000.0)
                              + ({zerodha_bps} / 10000.0) as cost_return
                        from (
                            select
                                *,
                                lag(entry_signal, {total_latency}) over (order by local_sequence_id) as executable_signal,
                                lead(mid_price, {horizon}) over (order by local_sequence_id) as future_mid_price
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
    daily = (
        daily_symbol.groupby(["trade_date", "variant_id", "feature_family", "execution_profile"], sort=True)
        .agg(
            trades=("trades", "sum"),
            sum_gross_return=("sum_gross_return", "sum"),
            sum_cost_return=("sum_cost_return", "sum"),
            sum_net_return=("sum_net_return", "sum"),
            net_pnl_inr=("net_pnl_inr", "sum"),
            worst_trade_pnl_inr=("worst_trade_pnl_inr", "min"),
            best_trade_pnl_inr=("best_trade_pnl_inr", "max"),
            forward_horizon_events=("forward_horizon_events", "first"),
            cooldown_modulus=("cooldown_modulus", "first"),
        )
        .reset_index()
    )
    rows: list[dict[str, Any]] = []
    for (variant_id, feature_family, execution_profile), group in daily.groupby(
        ["variant_id", "feature_family", "execution_profile"], sort=True
    ):
        group = group.sort_values("trade_date", kind="mergesort").copy()
        group["running_net_pnl_inr"] = group["net_pnl_inr"].cumsum()
        group["running_peak_inr"] = group["running_net_pnl_inr"].cummax()
        group["drawdown_inr"] = group["running_net_pnl_inr"] - group["running_peak_inr"]
        trades = int(group["trades"].sum())
        daily_std = float(group["net_pnl_inr"].std(ddof=1))
        daily_mean = float(group["net_pnl_inr"].mean())
        sharpe = float((daily_mean / daily_std) * (252.0**0.5)) if daily_std > 0 else 0.0
        rows.append(
            {
                "variant_id": variant_id,
                "feature_family": feature_family,
                "execution_profile": execution_profile,
                "trade_dates": int(group["trade_date"].nunique()),
                "trades": trades,
                "net_pnl_inr": float(group["net_pnl_inr"].sum()),
                "gross_pnl_proxy_inr": float(group["sum_gross_return"].sum() * DEFAULT_ORDER_NOTIONAL_INR),
                "cost_pnl_drag_proxy_inr": float(group["sum_cost_return"].sum() * DEFAULT_ORDER_NOTIONAL_INR),
                "mean_net_return_per_trade": float(group["sum_net_return"].sum() / trades) if trades else 0.0,
                "mean_gross_return_per_trade": float(group["sum_gross_return"].sum() / trades) if trades else 0.0,
                "mean_cost_return_per_trade": float(group["sum_cost_return"].sum() / trades) if trades else 0.0,
                "positive_day_fraction": float((group["net_pnl_inr"] > 0).mean()),
                "positive_daily_rows": int((group["net_pnl_inr"] > 0).sum()),
                "gross_positive_days": int((group["sum_gross_return"] > 0).sum()),
                "worst_daily_net_pnl_inr": float(group["net_pnl_inr"].min()),
                "best_daily_net_pnl_inr": float(group["net_pnl_inr"].max()),
                "max_drawdown_inr": float(group["drawdown_inr"].min()),
                "worst_trade_pnl_inr": float(group["worst_trade_pnl_inr"].min()),
                "best_trade_pnl_inr": float(group["best_trade_pnl_inr"].max()),
                "forward_horizon_events": int(group["forward_horizon_events"].iloc[0]),
                "cooldown_modulus": int(group["cooldown_modulus"].iloc[0]),
                "annualized_sharpe_proxy": sharpe,
            }
        )
    summary = pd.DataFrame(rows)
    summary["positive_after_costs"] = summary["net_pnl_inr"] > 0
    summary["deployable_retail_profile"] = summary["execution_profile"] != "zero_latency_spread_only_control"
    summary["bounded_replay_candidate"] = (
        summary["deployable_retail_profile"]
        & summary["positive_after_costs"]
        & (summary["positive_day_fraction"] >= 0.50)
        & (summary["trades"] >= 50)
        & (summary["max_drawdown_inr"] > -250_000.0)
    )
    summary = summary.sort_values(["net_pnl_inr", "positive_day_fraction"], ascending=[False, False], kind="mergesort").reset_index(
        drop=True
    )
    acceptance = pd.DataFrame(
        [
            ("phase54_dense_shards_scanned", len(files), "Dense parquet shards scanned for bounded redesign validation"),
            ("phase54_strategy_profile_rows", len(summary), "Selective variant/profile result rows"),
            ("phase54_trade_rows", int(summary["trades"].sum()), "Aggregated simulated trade rows"),
            ("phase54_positive_after_cost_rows", int(summary["positive_after_costs"].sum()), "Variant/profile rows positive after costs"),
            (
                "phase54_deployable_positive_after_cost_rows",
                int((summary["deployable_retail_profile"] & summary["positive_after_costs"]).sum()),
                "Deployable retail variant/profile rows positive after costs",
            ),
            (
                "phase54_bounded_replay_candidate_rows",
                int(summary["bounded_replay_candidate"].sum()),
                "Deployable retail rows passing positive, persistence and proxy-risk screens",
            ),
            ("phase54_positive_daily_symbol_rows", int((daily_symbol["net_pnl_inr"] > 0).sum()), "Daily-symbol variant/profile rows positive after costs"),
            ("phase54_best_net_pnl_inr", float(summary["net_pnl_inr"].max()), "Best aggregate variant/profile net P&L"),
            ("phase54_elapsed_seconds", elapsed_seconds, "Replay elapsed seconds"),
            ("phase54_dense_output_root", str(dense_root), "Dense input lake root"),
            ("phase54_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha cost model used for charge bps"),
            (
                "phase54_recommend_scale_to_full_year",
                int(summary["bounded_replay_candidate"].sum() > 0),
                "1 means at least one deployable retail bounded candidate deserves a larger dense replay",
            ),
        ],
        columns=["metric", "value", "description"],
    )
    return summary, acceptance


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase54 Selective Dense Replay",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase54 is the response to the Phase53 finding that the first dense tick-level catalog was not profitable after costs.",
        "It tests a bounded lower-turnover redesign catalog before authorizing any more full-year brute-force replay.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase54_selective_dense_replay_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase54(
    dense_root: Path,
    output_dir: Path,
    base_dir: Path,
    limit_shards: int | None,
    max_rows_per_shard: int | None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    files = parquet_files(dense_root, limit_shards=limit_shards)
    started = time.perf_counter()
    daily_frames: list[pd.DataFrame] = []
    for shard_index, path in enumerate(files, start=1):
        shard_frame = query_shard(path, shard_index, max_rows_per_shard)
        shard_frame.insert(0, "shard_index", shard_index)
        shard_frame.insert(1, "shard_path", str(path))
        daily_frames.append(shard_frame)
    daily_symbol = pd.concat(daily_frames, ignore_index=True) if daily_frames else pd.DataFrame()
    elapsed = time.perf_counter() - started
    summary, acceptance = summarize(daily_symbol, files, elapsed, dense_root)

    catalog = variant_catalog()
    catalog.to_csv(output_dir / "selective_variant_catalog.csv", index=False)
    daily_symbol.to_csv(output_dir / "selective_dense_replay_daily_symbol.csv", index=False)
    summary.to_csv(output_dir / "selective_dense_replay_strategy_summary.csv", index=False)
    acceptance.to_csv(output_dir / "selective_dense_replay_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Selective Variant Catalog": catalog,
            "Strategy Summary": summary,
            "Daily Symbol Sample": daily_symbol.head(120),
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase54_selective_dense_replay_bounded_redesign_gate",
        "dense_shards_scanned": len(files),
        "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
        "variant_profile_rows": int(len(summary)),
        "recommend_scale_to_full_year": int(summary["bounded_replay_candidate"].sum() > 0) if not summary.empty else 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase54",
            generated_utc=generated_utc,
            inputs={
                "phase51_dense_lake": str(dense_root),
                "phase53_edge_diagnostics": "outputs/phase53/phase53_edge_diagnostics_report.md",
            },
            parameters={
                "limit_shards": limit_shards if limit_shards is not None else "none_full_lake",
                "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
                "variants": ";".join(item["variant_id"] for item in SELECTIVE_VARIANTS),
                "execution_profiles": ";".join(item["execution_profile"] for item in selected_execution_profiles()),
                "acceptance_rule": "positive_after_costs_and_positive_day_fraction_ge_0_50_and_trades_ge_50_and_max_drawdown_gt_minus_250000",
            },
            outputs={
                "variant_catalog": str(output_dir / "selective_variant_catalog.csv"),
                "daily_symbol": str(output_dir / "selective_dense_replay_daily_symbol.csv"),
                "strategy_summary": str(output_dir / "selective_dense_replay_strategy_summary.csv"),
                "acceptance_summary": str(output_dir / "selective_dense_replay_acceptance_summary.csv"),
                "report": str(output_dir / "phase54_selective_dense_replay_report.md"),
                "manifest": str(output_dir / "phase54_selective_dense_replay_manifest.json"),
            },
            random_seed="none_deterministic_dense_lake_sql_replay",
            scenario_ids="phase54_bounded_first_shards_from_phase51_dense_lake",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase54_event_row_lag_profiles_from_phase12_execution_profiles",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase54_selective_dense_replay_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run bounded selective dense-lake strategy redesign validation.")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--limit-shards", type=int, default=8)
    parser.add_argument("--max-rows-per-shard", type=int, default=250_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase54(args.dense_root, args.output_dir, args.base_dir, args.limit_shards, args.max_rows_per_shard)


if __name__ == "__main__":
    main()
