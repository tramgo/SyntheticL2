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
from synthetic_l2.phase56_cost_clearing_label_discovery import DEFAULT_DENSE_ROOT, DEFAULT_ORDER_NOTIONAL_INR, parquet_files
from synthetic_l2.phase61_lower_frequency_candidate_sweep import _safe_path, profile_cost_bps, retail_profile
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase71")
BAR_EVENTS = [5_000, 10_000]
FEATURE_QUANTILES = [0.50, 0.70, 0.90]
SIGNAL_SPECS = [
    ("SHOCK_MOMENTUM", "sign"),
    ("SHOCK_MEAN_REVERSION", "opposite"),
]


def selected_files(dense_root: Path, limit_shards: int) -> list[tuple[int, Path]]:
    files = parquet_files(dense_root, limit_shards=limit_shards)
    return [(offset, path) for offset, path in enumerate(files, start=1)]


def query_shock_bars(path: Path, shard_index: int, max_rows_per_shard: int | None) -> pd.DataFrame:
    filter_sql = """
        buy_1_price > 0
        and sell_1_price > 0
        and sell_1_price >= buy_1_price
        and not coalesce(is_duplicate, false)
        and not coalesce(is_disconnect_gap, false)
        and not coalesce(is_out_of_order_injected, false)
    """
    if max_rows_per_shard is not None:
        filter_sql += f" and local_sequence_id <= {int(max_rows_per_shard)}"
    con = duckdb.connect()
    try:
        frames: list[pd.DataFrame] = []
        for bar_events in BAR_EVENTS:
            sql = f"""
            with base as (
                select
                    {int(shard_index)}::integer as shard_index,
                    trade_date,
                    trade_month,
                    symbol,
                    local_sequence_id,
                    floor((local_sequence_id - 1) / {int(bar_events)})::integer as bar_id,
                    ((buy_1_price + sell_1_price) / 2.0)::double as mid_price,
                    greatest(sell_1_price - buy_1_price, 0.01)::double as spread,
                    greatest(sell_1_price - buy_1_price, 0.01)::double as tick_size_proxy,
                    ((buy_1_quantity - sell_1_quantity) / nullif((buy_1_quantity + sell_1_quantity), 0.0))::double as l1_imbalance,
                    coalesce(is_market_shock_day, false) as is_market_shock_day,
                    coalesce(is_symbol_shock, false) as is_symbol_shock,
                    regime_code,
                    feed_profile
                from read_parquet('{_safe_path(path)}', union_by_name=true)
                where {filter_sql}
            ),
            bars as (
                select
                    shard_index,
                    trade_date,
                    trade_month,
                    symbol,
                    {int(bar_events)}::integer as bar_events,
                    bar_id,
                    count(*)::bigint as rows_in_bar,
                    first(mid_price order by local_sequence_id)::double as open_mid_price,
                    last(mid_price order by local_sequence_id)::double as close_mid_price,
                    avg(spread)::double as avg_spread,
                    avg(tick_size_proxy)::double as avg_tick_size_proxy,
                    avg(l1_imbalance)::double as avg_l1_imbalance,
                    avg(case when is_market_shock_day then 1.0 else 0.0 end)::double as market_shock_fraction,
                    avg(case when is_symbol_shock then 1.0 else 0.0 end)::double as symbol_shock_fraction,
                    mode(regime_code)::varchar as dominant_regime_code,
                    mode(feed_profile)::varchar as dominant_feed_profile
                from base
                group by shard_index, trade_date, trade_month, symbol, bar_id
                having count(*) >= greatest(10, {int(bar_events)} * 0.50)
            ),
            labeled as (
                select
                    *,
                    close_mid_price / nullif(open_mid_price, 0.0) - 1.0 as bar_return,
                    lag(close_mid_price / nullif(open_mid_price, 0.0) - 1.0) over (order by bar_id) as prev_bar_return,
                    lead(close_mid_price) over (order by bar_id) / nullif(close_mid_price, 0.0) - 1.0 as next_bar_return
                from bars
            )
            select
                *,
                case
                    when symbol_shock_fraction > 0 then 'symbol_shock'
                    when market_shock_fraction > 0 then 'market_shock'
                    else 'no_shock_control'
                end::varchar as shock_bucket
            from labeled
            where prev_bar_return is not null
              and next_bar_return is not null
            """
            frames.append(con.execute(sql).fetchdf())
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    finally:
        con.close()


def load_bars(dense_root: Path, limit_shards: int, max_rows_per_shard: int | None) -> tuple[pd.DataFrame, pd.DataFrame]:
    files = selected_files(dense_root, limit_shards)
    frames = [query_shock_bars(path, shard_index, max_rows_per_shard) for shard_index, path in files]
    bars = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    inventory = pd.DataFrame([{"shard_index": shard_index, "shard_path": str(path)} for shard_index, path in files])
    return bars, inventory


def build_thresholds(bars: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if bars.empty:
        return pd.DataFrame()
    for bar_events in BAR_EVENTS:
        for shock_bucket in sorted(bars["shock_bucket"].dropna().unique()):
            subset = bars[(bars["bar_events"].eq(bar_events)) & (bars["shock_bucket"].eq(shock_bucket))]
            values = subset["prev_bar_return"].astype(float).abs().replace([np.inf, -np.inf], np.nan).dropna()
            if values.empty:
                continue
            for signal_id, side_mode in SIGNAL_SPECS:
                for quantile in FEATURE_QUANTILES:
                    rows.append(
                        {
                            "rule_id": f"P71_{signal_id}_B{bar_events}_{shock_bucket}_Q{int(quantile * 100):02d}",
                            "signal_id": signal_id,
                            "side_mode": side_mode,
                            "bar_events": bar_events,
                            "shock_bucket": shock_bucket,
                            "feature_quantile": quantile,
                            "abs_prev_return_threshold": float(values.quantile(quantile)),
                        }
                    )
    return pd.DataFrame(rows)


def evaluate_rules(bars: pd.DataFrame, thresholds: pd.DataFrame) -> pd.DataFrame:
    if bars.empty or thresholds.empty:
        return pd.DataFrame()
    profile = retail_profile()
    slippage_ticks = float(profile["fixed_slippage_ticks"])
    impact_bps = float(profile["impact_bps"]) + float(profile.get("fees_bps", 0.0))
    zerodha_bps = profile_cost_bps(profile)
    rows: list[dict[str, Any]] = []
    for _, rule in thresholds.iterrows():
        subset = bars[(bars["bar_events"].eq(int(rule["bar_events"]))) & (bars["shock_bucket"].eq(str(rule["shock_bucket"])))].copy()
        if subset.empty:
            continue
        feature = subset["prev_bar_return"].astype(float)
        side = np.sign(feature)
        if str(rule["side_mode"]) == "opposite":
            side = -side
        mask = feature.abs().ge(float(rule["abs_prev_return_threshold"])) & side.ne(0) & subset["next_bar_return"].notna()
        trades = subset.loc[mask].copy()
        if trades.empty:
            continue
        selected_side = side.loc[mask].astype(float)
        gross_return = selected_side * trades["next_bar_return"].astype(float)
        cost_return = (
            ((trades["avg_spread"].astype(float) / 2.0) / trades["close_mid_price"].astype(float))
            + (slippage_ticks * trades["avg_tick_size_proxy"].astype(float) / trades["close_mid_price"].astype(float))
            + (impact_bps / 10000.0)
            + (zerodha_bps / 10000.0)
        )
        net_return = gross_return - cost_return
        symbol_net = pd.DataFrame({"symbol": trades["symbol"], "net": net_return}).groupby("symbol", sort=True)["net"].sum()
        month_net = pd.DataFrame({"trade_month": trades["trade_month"], "net": net_return}).groupby("trade_month", sort=True)["net"].sum()
        rows.append(
            {
                **rule.to_dict(),
                "trades": int(len(trades)),
                "symbols": int(trades["symbol"].nunique()),
                "trade_months": int(trades["trade_month"].nunique()),
                "net_pnl_inr": float(net_return.sum() * DEFAULT_ORDER_NOTIONAL_INR),
                "gross_pnl_proxy_inr": float(gross_return.sum() * DEFAULT_ORDER_NOTIONAL_INR),
                "cost_pnl_drag_proxy_inr": float(cost_return.sum() * DEFAULT_ORDER_NOTIONAL_INR),
                "mean_net_bps": float(net_return.mean() * 10000.0),
                "precision_cost_clear": float((gross_return > cost_return).mean()),
                "positive_symbol_fraction": float((symbol_net > 0).mean()) if int(symbol_net.shape[0]) else 0.0,
                "positive_month_fraction": float((month_net > 0).mean()) if int(month_net.shape[0]) else 0.0,
                "cost_drag_to_abs_gross_ratio": float(cost_return.sum() / abs(gross_return.sum())) if float(abs(gross_return.sum())) > 0 else np.nan,
            }
        )
    results = pd.DataFrame(rows)
    if results.empty:
        return results
    control = (
        results[results["shock_bucket"].eq("no_shock_control")]
        .assign(control_key=lambda df: df["signal_id"] + "|" + df["side_mode"] + "|" + df["bar_events"].astype(str) + "|" + df["feature_quantile"].astype(str))
        [["control_key", "net_pnl_inr"]]
        .rename(columns={"net_pnl_inr": "matched_no_shock_control_net_pnl_inr"})
    )
    results["control_key"] = (
        results["signal_id"] + "|" + results["side_mode"] + "|" + results["bar_events"].astype(str) + "|" + results["feature_quantile"].astype(str)
    )
    results = results.merge(control, on="control_key", how="left").drop(columns=["control_key"])
    results["matched_no_shock_control_net_pnl_inr"] = results["matched_no_shock_control_net_pnl_inr"].fillna(0.0)
    results["label_candidate"] = (
        results["shock_bucket"].ne("no_shock_control")
        & (results["trades"] >= 100)
        & (results["symbols"] >= 2)
        & (results["net_pnl_inr"] > 0)
        & (results["precision_cost_clear"] >= 0.55)
        & (results["positive_symbol_fraction"] >= 0.50)
        & (results["cost_drag_to_abs_gross_ratio"] <= 0.50)
        & (results["matched_no_shock_control_net_pnl_inr"] <= 0)
    )
    return results.sort_values(
        ["label_candidate", "net_pnl_inr", "precision_cost_clear", "trades"],
        ascending=[False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def summarize(results: pd.DataFrame, bars: pd.DataFrame, inventory: pd.DataFrame, elapsed_seconds: float) -> pd.DataFrame:
    candidate_rows = int(results["label_candidate"].sum()) if not results.empty else 0
    best_net = float(results["net_pnl_inr"].max()) if not results.empty else 0.0
    shock_bar_rows = int(bars[bars["shock_bucket"].ne("no_shock_control")].shape[0]) if not bars.empty else 0
    return pd.DataFrame(
        [
            ("phase71_shards_scanned", int(len(inventory)), "Dense shards scanned"),
            ("phase71_bar_rows", int(len(bars)), "Shock/control event-bar rows"),
            ("phase71_shock_bar_rows", shock_bar_rows, "Event-bar rows with market or symbol shock tags"),
            ("phase71_rule_rows", int(len(results)), "Shock resilience rules evaluated"),
            ("phase71_label_candidate_rows", candidate_rows, "Shock rules passing label gate"),
            ("phase71_best_net_pnl_inr", best_net, "Best after-cost rule P&L"),
            ("phase71_survives_shock_resilience_gate", int(candidate_rows > 0), "1 means a shock-resilience rule deserves replay"),
            ("phase71_elapsed_seconds", elapsed_seconds, "Elapsed seconds"),
            ("phase71_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha retail intraday cost model"),
            (
                "phase71_recommend_next_action",
                "targeted_shock_resilience_replay" if candidate_rows else "research_audit_and_generator_assumption_review",
                "Recommended next action",
            ),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase71 Shock-Resilience Labels",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase71 tests whether market/symbol shock tags create lower-frequency momentum or mean-reversion labels that survive costs.",
        "Shock candidates must beat matched no-shock controls before any wider replay.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase71_shock_resilience_labels_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase71(
    dense_root: Path,
    output_dir: Path,
    base_dir: Path,
    limit_shards: int,
    max_rows_per_shard: int | None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    bars, inventory = load_bars(dense_root, limit_shards, max_rows_per_shard)
    thresholds = build_thresholds(bars)
    results = evaluate_rules(bars, thresholds)
    elapsed = time.perf_counter() - started
    acceptance = summarize(results, bars, inventory, elapsed)

    inventory.to_csv(output_dir / "shock_file_inventory.csv", index=False)
    bars.to_csv(output_dir / "shock_bar_rows.csv", index=False)
    thresholds.to_csv(output_dir / "shock_rule_thresholds.csv", index=False)
    results.to_csv(output_dir / "shock_rule_results.csv", index=False)
    acceptance.to_csv(output_dir / "shock_acceptance_summary.csv", index=False)
    write_report(output_dir, {"Acceptance Summary": acceptance, "Top Rule Results": results.head(40), "Rule Thresholds": thresholds})

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase71_shock_resilience_labels",
        "survives_shock_resilience_gate": int(acceptance.loc[acceptance["metric"].eq("phase71_survives_shock_resilience_gate"), "value"].iloc[0]),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase71",
            generated_utc=generated_utc,
            inputs={
                "phase51_dense_lake": str(dense_root),
                "phase67_feature_design_queue": "outputs/phase67/feature_design_queue.csv",
                "phase70_acceptance": "outputs/phase70/lead_lag_acceptance_summary.csv",
            },
            parameters={
                "limit_shards": limit_shards,
                "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
                "bar_events": BAR_EVENTS,
                "feature_quantiles": FEATURE_QUANTILES,
                "label_gate": "shock_bucket_not_control_and_trades_ge_100_and_symbols_ge_2_and_net_pnl_gt_0_and_precision_ge_0_55_and_positive_symbol_fraction_ge_0_50_and_cost_drag_le_0_50_abs_gross_and_no_shock_control_net_le_0",
            },
            outputs={
                "file_inventory": str(output_dir / "shock_file_inventory.csv"),
                "bar_rows": str(output_dir / "shock_bar_rows.csv"),
                "thresholds": str(output_dir / "shock_rule_thresholds.csv"),
                "rule_results": str(output_dir / "shock_rule_results.csv"),
                "acceptance_summary": str(output_dir / "shock_acceptance_summary.csv"),
                "report": str(output_dir / "phase71_shock_resilience_labels_report.md"),
                "manifest": str(output_dir / "phase71_shock_resilience_labels_manifest.json"),
            },
            random_seed="none_deterministic_shock_label_scan",
            scenario_ids="phase71_shock_resilience_event_bar_labels",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase71_event_bar_shock_momentum_mean_reversion",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase71_shock_resilience_labels_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate shock-resilience event-bar labels.")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--limit-shards", type=int, default=128)
    parser.add_argument("--max-rows-per-shard", type=int, default=250_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase71(args.dense_root, args.output_dir, args.base_dir, args.limit_shards, args.max_rows_per_shard)


if __name__ == "__main__":
    main()
