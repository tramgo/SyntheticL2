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

from synthetic_l2.phase12_execution_simulator import EXECUTION_PROFILES
from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase56_cost_clearing_label_discovery import DEFAULT_DENSE_ROOT, DEFAULT_ORDER_NOTIONAL_INR, parquet_files
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, calculate_equity_intraday_nse_charges


DEFAULT_OUTPUT_DIR = Path("outputs/phase60")
BAR_EVENT_SIZES = [1_000, 5_000, 10_000]
FEATURE_QUANTILES = [0.50, 0.70, 0.90]

SIGNAL_SPECS = [
    ("BAR_MOMENTUM", "prev_bar_return", "sign"),
    ("BAR_CONTRARIAN", "prev_bar_return", "opposite"),
    ("BAR_IMBALANCE", "avg_l1_imbalance", "sign"),
    ("BAR_MICROPRICE", "avg_microprice_dev", "sign"),
]


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


def selected_files(dense_root: Path, start_shard: int, limit_shards: int) -> list[Path]:
    files = parquet_files(dense_root, limit_shards=None)
    return files[int(start_shard) : int(start_shard) + int(limit_shards)]


def query_shard_bars(path: Path, shard_index: int, max_rows_per_shard: int | None) -> pd.DataFrame:
    filter_sql = "buy_1_price > 0 and sell_1_price > 0 and sell_1_price >= buy_1_price"
    if max_rows_per_shard is not None:
        filter_sql += f" and local_sequence_id <= {int(max_rows_per_shard)}"
    con = duckdb.connect()
    try:
        frames: list[pd.DataFrame] = []
        for bar_events in BAR_EVENT_SIZES:
            sql = f"""
            with base as (
                select
                    {shard_index}::integer as shard_index,
                    trade_date,
                    symbol,
                    local_sequence_id,
                    floor((local_sequence_id - 1) / {bar_events})::integer as bar_id,
                    ((buy_1_price + sell_1_price) / 2.0) as mid_price,
                    greatest(sell_1_price - buy_1_price, 0.01) as spread,
                    greatest(sell_1_price - buy_1_price, 0.01) as tick_size_proxy,
                    ((buy_1_quantity - sell_1_quantity) / nullif((buy_1_quantity + sell_1_quantity), 0.0)) as l1_imbalance,
                    (((sell_1_price * buy_1_quantity + buy_1_price * sell_1_quantity) / nullif((buy_1_quantity + sell_1_quantity), 0.0))
                        - ((buy_1_price + sell_1_price) / 2.0)) / nullif(((buy_1_price + sell_1_price) / 2.0), 0.0) as microprice_dev,
                    (((buy_1_price * buy_1_quantity) + (sell_1_price * sell_1_quantity)) / 2.0) as l1_depth_notional,
                    coalesce(is_duplicate, false) as is_duplicate,
                    coalesce(is_disconnect_gap, false) as is_disconnect_gap,
                    coalesce(is_out_of_order_injected, false) as is_out_of_order_injected
                from read_parquet('{_safe_path(path)}', union_by_name=true)
                where {filter_sql}
            ),
            bar_members as (
                select *
                from base
                where not is_duplicate
                  and not is_disconnect_gap
                  and not is_out_of_order_injected
            ),
            bars as (
                select
                    shard_index,
                    trade_date,
                    symbol,
                    {bar_events}::integer as bar_events,
                    bar_id,
                    min(local_sequence_id)::bigint as first_sequence_id,
                    max(local_sequence_id)::bigint as last_sequence_id,
                    count(*)::bigint as rows_in_bar,
                    first(mid_price order by local_sequence_id)::double as open_mid_price,
                    last(mid_price order by local_sequence_id)::double as close_mid_price,
                    avg(spread)::double as avg_spread,
                    avg(tick_size_proxy)::double as avg_tick_size_proxy,
                    avg(l1_imbalance)::double as avg_l1_imbalance,
                    avg(microprice_dev)::double as avg_microprice_dev,
                    avg(l1_depth_notional)::double as avg_l1_depth_notional
                from bar_members
                group by shard_index, trade_date, symbol, bar_id
                having count(*) >= greatest(10, {bar_events} * 0.50)
            ),
            labeled as (
                select
                    *,
                    close_mid_price / nullif(open_mid_price, 0.0) - 1.0 as bar_return,
                    lag(close_mid_price / nullif(open_mid_price, 0.0) - 1.0) over (order by bar_id) as prev_bar_return,
                    lead(close_mid_price) over (order by bar_id) / nullif(close_mid_price, 0.0) - 1.0 as next_bar_return
                from bars
            )
            select *
            from labeled
            where prev_bar_return is not null
              and next_bar_return is not null
            """
            frames.append(con.execute(sql).fetchdf())
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    finally:
        con.close()


def load_bar_frame(files: list[Path], max_rows_per_shard: int | None) -> pd.DataFrame:
    frames = [query_shard_bars(path, index, max_rows_per_shard) for index, path in enumerate(files, start=1)]
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def build_thresholds(discovery_bars: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for bar_events in BAR_EVENT_SIZES:
        subset = discovery_bars[discovery_bars["bar_events"] == bar_events]
        for signal_id, feature, side_mode in SIGNAL_SPECS:
            values = pd.to_numeric(subset[feature], errors="coerce").abs().replace([np.inf, -np.inf], np.nan).dropna()
            if values.empty:
                continue
            for quantile in FEATURE_QUANTILES:
                rows.append(
                    {
                        "rule_id": f"P60_{signal_id}_B{bar_events}_Q{int(quantile * 100):02d}",
                        "signal_id": signal_id,
                        "feature": feature,
                        "side_mode": side_mode,
                        "bar_events": bar_events,
                        "feature_quantile": quantile,
                        "abs_threshold": float(values.quantile(quantile)),
                    }
                )
    return pd.DataFrame(rows)


def evaluate_rules(bars: pd.DataFrame, rules: pd.DataFrame) -> pd.DataFrame:
    profile = retail_profile()
    slippage_ticks = float(profile["fixed_slippage_ticks"])
    impact_bps = float(profile["impact_bps"]) + float(profile.get("fees_bps", 0.0))
    zerodha_bps = profile_cost_bps(profile)
    rows: list[dict[str, Any]] = []
    for _, rule in rules.iterrows():
        subset = bars[bars["bar_events"] == int(rule["bar_events"])].copy()
        if subset.empty:
            continue
        feature = pd.to_numeric(subset[str(rule["feature"])], errors="coerce")
        side = np.sign(feature)
        if str(rule["side_mode"]) == "opposite":
            side = -side
        mask = feature.abs().ge(float(rule["abs_threshold"])) & side.ne(0) & subset["next_bar_return"].notna()
        trades = subset.loc[mask].copy()
        if trades.empty:
            rows.append(
                {
                    **rule.to_dict(),
                    "trades": 0,
                    "net_pnl_inr": 0.0,
                    "gross_pnl_proxy_inr": 0.0,
                    "cost_pnl_drag_proxy_inr": 0.0,
                    "mean_net_return": 0.0,
                    "precision_cost_clear": 0.0,
                    "symbols": 0,
                    "shards": 0,
                    "positive_symbol_fraction": 0.0,
                    "positive_shard_fraction": 0.0,
                }
            )
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
        symbol_net = pd.DataFrame({"symbol": trades["symbol"], "net": net_return}).groupby("symbol", sort=False)["net"].sum()
        shard_net = pd.DataFrame({"shard_index": trades["shard_index"], "net": net_return}).groupby("shard_index", sort=False)["net"].sum()
        rows.append(
            {
                **rule.to_dict(),
                "trades": int(len(trades)),
                "net_pnl_inr": float(net_return.sum() * DEFAULT_ORDER_NOTIONAL_INR),
                "gross_pnl_proxy_inr": float(gross_return.sum() * DEFAULT_ORDER_NOTIONAL_INR),
                "cost_pnl_drag_proxy_inr": float(cost_return.sum() * DEFAULT_ORDER_NOTIONAL_INR),
                "mean_net_return": float(net_return.mean()),
                "precision_cost_clear": float((gross_return > cost_return).mean()),
                "symbols": int(symbol_net.shape[0]),
                "shards": int(shard_net.shape[0]),
                "positive_symbol_fraction": float((symbol_net > 0).mean()) if int(symbol_net.shape[0]) else 0.0,
                "positive_shard_fraction": float((shard_net > 0).mean()) if int(shard_net.shape[0]) else 0.0,
            }
        )
    results = pd.DataFrame(rows)
    if results.empty:
        return results
    results["positive_after_costs"] = results["net_pnl_inr"] > 0
    return results


def combine_discovery_validation(discovery_results: pd.DataFrame, validation_results: pd.DataFrame) -> pd.DataFrame:
    keys = ["rule_id", "signal_id", "feature", "side_mode", "bar_events", "feature_quantile", "abs_threshold"]
    columns = keys + [
        "trades",
        "net_pnl_inr",
        "gross_pnl_proxy_inr",
        "cost_pnl_drag_proxy_inr",
        "mean_net_return",
        "precision_cost_clear",
        "symbols",
        "shards",
        "positive_symbol_fraction",
        "positive_shard_fraction",
        "positive_after_costs",
    ]
    discovery = discovery_results[columns].rename(columns={column: f"discovery_{column}" for column in columns if column not in keys})
    validation = validation_results[columns].rename(columns={column: f"validation_{column}" for column in columns if column not in keys})
    combined = discovery.merge(validation, on=keys, how="outer")
    for column in combined.columns:
        if column.startswith("discovery_") or column.startswith("validation_"):
            combined[column] = combined[column].fillna(0)
    combined["phase60_scale_candidate"] = (
        combined["discovery_positive_after_costs"].astype(bool)
        & combined["validation_positive_after_costs"].astype(bool)
        & (combined["validation_trades"] >= 10)
        & (combined["validation_positive_symbol_fraction"] >= 0.50)
        & (combined["validation_positive_shard_fraction"] >= 0.50)
    )
    return combined.sort_values(
        ["phase60_scale_candidate", "validation_net_pnl_inr", "discovery_net_pnl_inr"],
        ascending=[False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def oracle_summary(bars: pd.DataFrame, label: str) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    profile = retail_profile()
    slippage_ticks = float(profile["fixed_slippage_ticks"])
    impact_bps = float(profile["impact_bps"]) + float(profile.get("fees_bps", 0.0))
    zerodha_bps = profile_cost_bps(profile)
    for bar_events in BAR_EVENT_SIZES:
        subset = bars[bars["bar_events"] == bar_events].copy()
        if subset.empty:
            continue
        cost_return = (
            ((subset["avg_spread"].astype(float) / 2.0) / subset["close_mid_price"].astype(float))
            + (slippage_ticks * subset["avg_tick_size_proxy"].astype(float) / subset["close_mid_price"].astype(float))
            + (impact_bps / 10000.0)
            + (zerodha_bps / 10000.0)
        )
        gross_return = subset["next_bar_return"].astype(float).abs()
        mask = gross_return > cost_return
        rows.append(
            {
                "split": label,
                "bar_events": bar_events,
                "bars": int(len(subset)),
                "oracle_trades": int(mask.sum()),
                "oracle_trade_fraction": float(mask.mean()) if len(mask) else 0.0,
                "oracle_net_pnl_inr": float((gross_return[mask] - cost_return[mask]).sum() * DEFAULT_ORDER_NOTIONAL_INR),
            }
        )
    return pd.DataFrame(rows)


def acceptance_summary(
    discovery_bars: pd.DataFrame,
    validation_bars: pd.DataFrame,
    combined: pd.DataFrame,
    discovery_files: list[Path],
    validation_files: list[Path],
    elapsed_seconds: float,
) -> pd.DataFrame:
    traded = combined["validation_trades"] > 0 if not combined.empty else pd.Series(dtype=bool)
    rows = [
        ("phase60_discovery_shards", len(discovery_files), "Dense shards used for lower-frequency threshold discovery"),
        ("phase60_validation_shards", len(validation_files), "Disjoint dense shards used for validation"),
        ("phase60_discovery_bar_rows", int(len(discovery_bars)), "Discovery event-bar rows"),
        ("phase60_validation_bar_rows", int(len(validation_bars)), "Validation event-bar rows"),
        ("phase60_rule_rows", int(len(combined)), "Lower-frequency rule rows evaluated"),
        ("phase60_validation_positive_rows", int((combined["validation_net_pnl_inr"] > 0).sum()) if not combined.empty else 0, "Rules positive after retail costs on validation"),
        ("phase60_scale_candidate_rows", int(combined["phase60_scale_candidate"].sum()) if not combined.empty else 0, "Rules passing lower-frequency scale gate"),
        (
            "phase60_best_traded_validation_net_pnl_inr",
            float(combined.loc[traded, "validation_net_pnl_inr"].max()) if (not combined.empty and bool(traded.any())) else 0.0,
            "Best validation net P&L among rows that emitted validation trades",
        ),
        ("phase60_elapsed_seconds", elapsed_seconds, "Elapsed seconds"),
        ("phase60_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha retail intraday cost model"),
        ("phase60_recommend_scale_to_month_sweep", int(combined["phase60_scale_candidate"].sum() > 0) if not combined.empty else 0, "1 means at least one lower-frequency rule deserves a broader month/symbol sweep"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase60 Lower-Frequency Meta Replay",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase60 pivots away from dense marketable micro-trading by aggregating dense ticks into event bars.",
        "Thresholds are fit on discovery bars and tested on disjoint validation bars after Zerodha retail costs.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase60_lower_frequency_meta_replay_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase60(
    dense_root: Path,
    output_dir: Path,
    base_dir: Path,
    discovery_shards: int,
    validation_start_shard: int,
    validation_shards: int,
    max_rows_per_shard: int | None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    discovery_files = selected_files(dense_root, 0, discovery_shards)
    validation_files = selected_files(dense_root, validation_start_shard, validation_shards)
    started = time.perf_counter()
    discovery_bars = load_bar_frame(discovery_files, max_rows_per_shard)
    validation_bars = load_bar_frame(validation_files, max_rows_per_shard)
    thresholds = build_thresholds(discovery_bars)
    discovery_results = evaluate_rules(discovery_bars, thresholds)
    validation_results = evaluate_rules(validation_bars, thresholds)
    combined = combine_discovery_validation(discovery_results, validation_results)
    oracle = pd.concat([oracle_summary(discovery_bars, "discovery"), oracle_summary(validation_bars, "validation")], ignore_index=True)
    elapsed = time.perf_counter() - started
    acceptance = acceptance_summary(discovery_bars, validation_bars, combined, discovery_files, validation_files, elapsed)
    top = combined.head(40)

    discovery_bars.head(5000).to_csv(output_dir / "lower_frequency_discovery_bar_sample.csv", index=False)
    validation_bars.head(5000).to_csv(output_dir / "lower_frequency_validation_bar_sample.csv", index=False)
    thresholds.to_csv(output_dir / "lower_frequency_rule_thresholds.csv", index=False)
    combined.to_csv(output_dir / "lower_frequency_rule_results.csv", index=False)
    top.to_csv(output_dir / "lower_frequency_top_results.csv", index=False)
    oracle.to_csv(output_dir / "lower_frequency_oracle_summary.csv", index=False)
    acceptance.to_csv(output_dir / "lower_frequency_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Top Lower-Frequency Results": top,
            "Oracle Summary": oracle,
            "Rule Thresholds": thresholds,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase60_lower_frequency_meta_replay",
        "discovery_shards": discovery_shards,
        "validation_start_shard": validation_start_shard,
        "validation_shards": validation_shards,
        "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
        "recommend_scale_to_month_sweep": int(combined["phase60_scale_candidate"].sum() > 0) if not combined.empty else 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase60",
            generated_utc=generated_utc,
            inputs={
                "phase51_dense_lake": str(dense_root),
                "phase59_stability_filtered_neighborhoods": "outputs/phase59/phase59_stability_filtered_neighborhoods_report.md",
            },
            parameters={
                "discovery_shards": discovery_shards,
                "validation_start_shard": validation_start_shard,
                "validation_shards": validation_shards,
                "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
                "bar_event_sizes": ";".join(str(item) for item in BAR_EVENT_SIZES),
                "feature_quantiles": ";".join(str(item) for item in FEATURE_QUANTILES),
                "signals": ";".join(item[0] for item in SIGNAL_SPECS),
                "validation_gate": "discovery_positive_and_validation_positive_and_validation_trades_ge_10_and_positive_symbol_fraction_ge_0_50_and_positive_shard_fraction_ge_0_50",
            },
            outputs={
                "discovery_bar_sample": str(output_dir / "lower_frequency_discovery_bar_sample.csv"),
                "validation_bar_sample": str(output_dir / "lower_frequency_validation_bar_sample.csv"),
                "thresholds": str(output_dir / "lower_frequency_rule_thresholds.csv"),
                "rule_results": str(output_dir / "lower_frequency_rule_results.csv"),
                "top_results": str(output_dir / "lower_frequency_top_results.csv"),
                "oracle_summary": str(output_dir / "lower_frequency_oracle_summary.csv"),
                "acceptance_summary": str(output_dir / "lower_frequency_acceptance_summary.csv"),
                "report": str(output_dir / "phase60_lower_frequency_meta_replay_report.md"),
                "manifest": str(output_dir / "phase60_lower_frequency_meta_replay_manifest.json"),
            },
            random_seed="none_deterministic_lower_frequency_replay",
            scenario_ids="phase60_discovery_shards_then_disjoint_validation_shards",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase60_event_bar_next_bar_execution_proxy",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase60_lower_frequency_meta_replay_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run lower-frequency event-bar meta replay over dense L2 shards.")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--discovery-shards", type=int, default=8)
    parser.add_argument("--validation-start-shard", type=int, default=8)
    parser.add_argument("--validation-shards", type=int, default=8)
    parser.add_argument("--max-rows-per-shard", type=int, default=250_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase60(
        args.dense_root,
        args.output_dir,
        args.base_dir,
        args.discovery_shards,
        args.validation_start_shard,
        args.validation_shards,
        args.max_rows_per_shard,
    )


if __name__ == "__main__":
    main()
