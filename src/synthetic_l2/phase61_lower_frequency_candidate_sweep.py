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


DEFAULT_OUTPUT_DIR = Path("outputs/phase61")
DEFAULT_PHASE60_TOP = Path("outputs/phase60/lower_frequency_top_results.csv")


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


def load_phase60_candidate(path: Path) -> dict[str, Any]:
    frame = pd.read_csv(path)
    candidates = frame[frame["phase60_scale_candidate"].astype(str).str.lower().eq("true")].copy()
    if candidates.empty:
        raise ValueError(f"No Phase60 scale candidate in {path}")
    return candidates.iloc[0].to_dict()


def selected_files(dense_root: Path, start_shard: int, limit_shards: int) -> list[tuple[int, Path]]:
    files = parquet_files(dense_root, limit_shards=None)
    selected = files[int(start_shard) : int(start_shard) + int(limit_shards)]
    return [(int(start_shard) + offset + 1, path) for offset, path in enumerate(selected)]


def query_candidate_shard(path: Path, global_shard_index: int, candidate: dict[str, Any], max_rows_per_shard: int | None) -> pd.DataFrame:
    bar_events = int(candidate["bar_events"])
    threshold = float(candidate["abs_threshold"])
    side_mode = str(candidate["side_mode"])
    filter_sql = "buy_1_price > 0 and sell_1_price > 0 and sell_1_price >= buy_1_price"
    if max_rows_per_shard is not None:
        filter_sql += f" and local_sequence_id <= {int(max_rows_per_shard)}"

    profile = retail_profile()
    slippage_ticks = float(profile["fixed_slippage_ticks"])
    impact_bps = float(profile["impact_bps"]) + float(profile.get("fees_bps", 0.0))
    zerodha_bps = profile_cost_bps(profile)
    signal_multiplier = "-1.0" if side_mode == "opposite" else "1.0"
    con = duckdb.connect()
    try:
        sql = f"""
        with base as (
            select
                {global_shard_index}::integer as shard_index,
                trade_date,
                symbol,
                local_sequence_id,
                floor((local_sequence_id - 1) / {bar_events})::integer as bar_id,
                ((buy_1_price + sell_1_price) / 2.0) as mid_price,
                greatest(sell_1_price - buy_1_price, 0.01) as spread,
                greatest(sell_1_price - buy_1_price, 0.01) as tick_size_proxy,
                coalesce(is_duplicate, false) as is_duplicate,
                coalesce(is_disconnect_gap, false) as is_disconnect_gap,
                coalesce(is_out_of_order_injected, false) as is_out_of_order_injected
            from read_parquet('{_safe_path(path)}', union_by_name=true)
            where {filter_sql}
        ),
        bars as (
            select
                shard_index,
                trade_date,
                symbol,
                {bar_events}::integer as bar_events,
                bar_id,
                count(*)::bigint as rows_in_bar,
                first(mid_price order by local_sequence_id)::double as open_mid_price,
                last(mid_price order by local_sequence_id)::double as close_mid_price,
                avg(spread)::double as avg_spread,
                avg(tick_size_proxy)::double as avg_tick_size_proxy
            from base
            where not is_duplicate
              and not is_disconnect_gap
              and not is_out_of_order_injected
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
        ),
        trades as (
            select
                *,
                ({signal_multiplier} * sign(prev_bar_return))::double as side,
                (({signal_multiplier} * sign(prev_bar_return)) * next_bar_return)::double as gross_return,
                (((avg_spread / 2.0) / nullif(close_mid_price, 0.0))
                  + ({slippage_ticks} * avg_tick_size_proxy / nullif(close_mid_price, 0.0))
                  + ({impact_bps} / 10000.0)
                  + ({zerodha_bps} / 10000.0))::double as cost_return
            from labeled
            where prev_bar_return is not null
              and next_bar_return is not null
              and abs(prev_bar_return) >= {threshold}
              and sign(prev_bar_return) != 0
        )
        select
            shard_index,
            trade_date,
            symbol,
            count(*)::bigint as trades,
            sum(gross_return)::double as sum_gross_return,
            sum(cost_return)::double as sum_cost_return,
            sum(gross_return - cost_return)::double as sum_net_return,
            sum((gross_return - cost_return) * {DEFAULT_ORDER_NOTIONAL_INR})::double as net_pnl_inr,
            sum(gross_return * {DEFAULT_ORDER_NOTIONAL_INR})::double as gross_pnl_proxy_inr,
            sum(cost_return * {DEFAULT_ORDER_NOTIONAL_INR})::double as cost_pnl_drag_proxy_inr,
            avg(gross_return - cost_return)::double as mean_net_return,
            avg(case when gross_return > cost_return then 1.0 else 0.0 end)::double as precision_cost_clear,
            min((gross_return - cost_return) * {DEFAULT_ORDER_NOTIONAL_INR})::double as worst_trade_pnl_inr,
            max((gross_return - cost_return) * {DEFAULT_ORDER_NOTIONAL_INR})::double as best_trade_pnl_inr
        from trades
        group by shard_index, trade_date, symbol
        """
        return con.execute(sql).fetchdf()
    finally:
        con.close()


def run_sweep(files: list[tuple[int, Path]], candidate: dict[str, Any], max_rows_per_shard: int | None) -> pd.DataFrame:
    frames = [query_candidate_shard(path, shard_index, candidate, max_rows_per_shard) for shard_index, path in files]
    if not frames:
        return pd.DataFrame()
    daily = pd.concat(frames, ignore_index=True)
    if daily.empty:
        return daily
    daily["positive_after_costs"] = daily["net_pnl_inr"] > 0
    return daily


def summarize(daily: pd.DataFrame, files: list[tuple[int, Path]], candidate: dict[str, Any], elapsed_seconds: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    if daily.empty:
        summary = pd.DataFrame(
            [
                {
                    "rule_id": str(candidate["rule_id"]),
                    "bar_events": int(candidate["bar_events"]),
                    "abs_threshold": float(candidate["abs_threshold"]),
                    "shards_scanned": len(files),
                    "symbols": 0,
                    "trade_dates": 0,
                    "trades": 0,
                    "net_pnl_inr": 0.0,
                    "gross_pnl_proxy_inr": 0.0,
                    "cost_pnl_drag_proxy_inr": 0.0,
                    "positive_symbol_fraction": 0.0,
                    "positive_shard_fraction": 0.0,
                    "precision_cost_clear": 0.0,
                    "phase61_survives_wider_sweep": False,
                }
            ]
        )
    else:
        symbol_net = daily.groupby("symbol", sort=True)["net_pnl_inr"].sum()
        shard_net = daily.groupby("shard_index", sort=True)["net_pnl_inr"].sum()
        trades = int(daily["trades"].sum())
        summary = pd.DataFrame(
            [
                {
                    "rule_id": str(candidate["rule_id"]),
                    "bar_events": int(candidate["bar_events"]),
                    "abs_threshold": float(candidate["abs_threshold"]),
                    "shards_scanned": len(files),
                    "shard_symbol_rows": int(len(daily)),
                    "symbols": int(symbol_net.shape[0]),
                    "trade_dates": int(daily["trade_date"].nunique()),
                    "trades": trades,
                    "net_pnl_inr": float(daily["net_pnl_inr"].sum()),
                    "gross_pnl_proxy_inr": float(daily["gross_pnl_proxy_inr"].sum()),
                    "cost_pnl_drag_proxy_inr": float(daily["cost_pnl_drag_proxy_inr"].sum()),
                    "positive_symbol_fraction": float((symbol_net > 0).mean()) if int(symbol_net.shape[0]) else 0.0,
                    "positive_shard_fraction": float((shard_net > 0).mean()) if int(shard_net.shape[0]) else 0.0,
                    "positive_symbol_rows": int((symbol_net > 0).sum()),
                    "positive_shard_rows": int((shard_net > 0).sum()),
                    "precision_cost_clear": float(np.average(daily["precision_cost_clear"], weights=daily["trades"])) if trades else 0.0,
                    "mean_net_return": float(daily["sum_net_return"].sum() / trades) if trades else 0.0,
                    "worst_symbol_net_pnl_inr": float(symbol_net.min()) if int(symbol_net.shape[0]) else 0.0,
                    "best_symbol_net_pnl_inr": float(symbol_net.max()) if int(symbol_net.shape[0]) else 0.0,
                    "phase61_survives_wider_sweep": bool(
                        daily["net_pnl_inr"].sum() > 0
                        and trades >= 100
                        and float((symbol_net > 0).mean()) >= 0.50
                        and float((shard_net > 0).mean()) >= 0.50
                    ),
                }
            ]
        )
    acceptance = pd.DataFrame(
        [
            ("phase61_wider_sweep_shards", len(files), "Dense shards scanned after Phase60 discovery/validation windows"),
            ("phase61_trade_rows", int(summary.iloc[0]["trades"]), "Candidate trades in wider sweep"),
            ("phase61_net_pnl_inr", float(summary.iloc[0]["net_pnl_inr"]), "After-cost net P&L in wider sweep"),
            ("phase61_positive_symbol_fraction", float(summary.iloc[0]["positive_symbol_fraction"]), "Fraction of symbols positive after costs"),
            ("phase61_positive_shard_fraction", float(summary.iloc[0]["positive_shard_fraction"]), "Fraction of shards positive after costs"),
            ("phase61_precision_cost_clear", float(summary.iloc[0]["precision_cost_clear"]), "Trade-weighted cost-clearing precision"),
            ("phase61_survives_wider_sweep", int(bool(summary.iloc[0]["phase61_survives_wider_sweep"])), "1 means the Phase60 candidate survived the wider sweep"),
            ("phase61_elapsed_seconds", elapsed_seconds, "Elapsed seconds"),
            ("phase61_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha retail intraday cost model"),
            ("phase61_recommend_full_month_replay", int(bool(summary.iloc[0]["phase61_survives_wider_sweep"])), "1 means promote to broader full-month/full-row replay"),
        ],
        columns=["metric", "value", "description"],
    )
    return summary, acceptance


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase61 Lower-Frequency Candidate Wider Sweep",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase61 replays the exact Phase60 lower-frequency scale candidate on later dense shards.",
        "The candidate threshold is reused without refitting.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase61_lower_frequency_candidate_sweep_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase61(
    dense_root: Path,
    output_dir: Path,
    base_dir: Path,
    phase60_top: Path,
    start_shard: int,
    limit_shards: int,
    max_rows_per_shard: int | None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    candidate = load_phase60_candidate(phase60_top)
    files = selected_files(dense_root, start_shard, limit_shards)
    started = time.perf_counter()
    daily = run_sweep(files, candidate, max_rows_per_shard)
    elapsed = time.perf_counter() - started
    summary, acceptance = summarize(daily, files, candidate, elapsed)
    file_inventory = pd.DataFrame([{"shard_index": index, "shard_path": str(path)} for index, path in files])

    pd.DataFrame([candidate]).to_csv(output_dir / "phase60_candidate_replayed.csv", index=False)
    file_inventory.to_csv(output_dir / "wider_sweep_file_inventory.csv", index=False)
    daily.to_csv(output_dir / "wider_sweep_daily_symbol.csv", index=False)
    summary.to_csv(output_dir / "wider_sweep_summary.csv", index=False)
    acceptance.to_csv(output_dir / "wider_sweep_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Wider Sweep Summary": summary,
            "Daily Symbol Results": daily,
            "Replayed Phase60 Candidate": pd.DataFrame([candidate]),
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase61_lower_frequency_candidate_wider_sweep",
        "start_shard": start_shard,
        "dense_shards_scanned": len(files),
        "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
        "survives_wider_sweep": int(bool(summary.iloc[0]["phase61_survives_wider_sweep"])),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase61",
            generated_utc=generated_utc,
            inputs={
                "phase51_dense_lake": str(dense_root),
                "phase60_top_results": str(phase60_top),
            },
            parameters={
                "start_shard": start_shard,
                "limit_shards": limit_shards,
                "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
                "candidate_rule_id": str(candidate["rule_id"]),
                "candidate_bar_events": int(candidate["bar_events"]),
                "candidate_abs_threshold": float(candidate["abs_threshold"]),
                "validation_gate": "net_pnl_gt_0_and_trades_ge_100_and_positive_symbol_fraction_ge_0_50_and_positive_shard_fraction_ge_0_50",
            },
            outputs={
                "candidate": str(output_dir / "phase60_candidate_replayed.csv"),
                "file_inventory": str(output_dir / "wider_sweep_file_inventory.csv"),
                "daily_symbol": str(output_dir / "wider_sweep_daily_symbol.csv"),
                "summary": str(output_dir / "wider_sweep_summary.csv"),
                "acceptance_summary": str(output_dir / "wider_sweep_acceptance_summary.csv"),
                "report": str(output_dir / "phase61_lower_frequency_candidate_sweep_report.md"),
                "manifest": str(output_dir / "phase61_lower_frequency_candidate_sweep_manifest.json"),
            },
            random_seed="none_deterministic_lower_frequency_candidate_replay",
            scenario_ids="phase61_later_shards_after_phase60_windows",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase61_fixed_phase60_event_bar_candidate",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase61_lower_frequency_candidate_sweep_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replay Phase60 lower-frequency candidate on wider disjoint dense shards.")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--phase60-top", type=Path, default=DEFAULT_PHASE60_TOP)
    parser.add_argument("--start-shard", type=int, default=16)
    parser.add_argument("--limit-shards", type=int, default=48)
    parser.add_argument("--max-rows-per-shard", type=int, default=250_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase61(
        args.dense_root,
        args.output_dir,
        args.base_dir,
        args.phase60_top,
        args.start_shard,
        args.limit_shards,
        args.max_rows_per_shard,
    )


if __name__ == "__main__":
    main()
