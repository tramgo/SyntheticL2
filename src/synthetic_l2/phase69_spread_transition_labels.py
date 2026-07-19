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
from synthetic_l2.phase56_cost_clearing_label_discovery import DEFAULT_DENSE_ROOT, parquet_files
from synthetic_l2.phase61_lower_frequency_candidate_sweep import _safe_path
from synthetic_l2.phase65_passive_queue_sensitivity import zerodha_roundtrip_bps
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase69")
MARKETABLE_IMPACT_BPS = 0.5
FIXED_SLIPPAGE_TICKS = 1.0


def selected_files(dense_root: Path, limit_shards: int) -> list[tuple[int, Path]]:
    files = parquet_files(dense_root, limit_shards=limit_shards)
    return [(offset, path) for offset, path in enumerate(files, start=1)]


def query_spread_transition_labels(
    path: Path,
    shard_index: int,
    lookback_ticks: int,
    outcome_horizon_ticks: int,
    min_abs_spread_change_bps: float,
    min_abs_recent_return_bps: float,
    max_rows_per_shard: int | None,
) -> pd.DataFrame:
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

    zerodha_bps = zerodha_roundtrip_bps()
    con = duckdb.connect()
    try:
        sql = f"""
        with base as (
            select
                {int(shard_index)}::integer as shard_index,
                trade_date,
                symbol,
                local_sequence_id,
                ((buy_1_price + sell_1_price) / 2.0)::double as mid_price,
                greatest(sell_1_price - buy_1_price, 0.01)::double as spread,
                greatest((sell_1_price - buy_1_price) / nullif(((buy_1_price + sell_1_price) / 2.0), 0.0) * 10000.0, 0.0)::double as spread_bps
            from read_parquet('{_safe_path(path)}', union_by_name=true)
            where {filter_sql}
        ),
        features as (
            select
                *,
                lag(mid_price, {int(lookback_ticks)}) over (order by local_sequence_id)::double as lookback_mid_price,
                lag(spread_bps, {int(lookback_ticks)}) over (order by local_sequence_id)::double as lookback_spread_bps,
                lead(mid_price, {int(outcome_horizon_ticks)}) over (order by local_sequence_id)::double as outcome_mid_price
            from base
        ),
        candidates as (
            select
                *,
                (spread_bps - lookback_spread_bps)::double as spread_change_bps,
                (mid_price / nullif(lookback_mid_price, 0.0) - 1.0) * 10000.0 as recent_return_bps,
                case
                    when spread_bps <= 1.0 then 'S01_le_1bp'
                    when spread_bps <= 2.5 then 'S02_1_2p5bp'
                    when spread_bps <= 5.0 then 'S03_2p5_5bp'
                    else 'S04_gt_5bp'
                end::varchar as spread_bucket,
                case
                    when spread_bps - lookback_spread_bps <= -{float(min_abs_spread_change_bps)} then 'compression'
                    when spread_bps - lookback_spread_bps >= {float(min_abs_spread_change_bps)} then 'expansion'
                    else 'flat'
                end::varchar as transition_type
            from features
            where lookback_mid_price is not null
              and lookback_spread_bps is not null
              and outcome_mid_price is not null
        ),
        signals as (
            select
                shard_index,
                trade_date,
                symbol,
                'P69_SPREAD_TRANSITION_MOMENTUM'::varchar as strategy_id,
                transition_type,
                spread_bucket,
                case
                    when abs(recent_return_bps) >= {float(min_abs_recent_return_bps)} then sign(recent_return_bps)
                    else 0
                end::integer as side,
                mid_price,
                spread_bps,
                spread_change_bps,
                recent_return_bps,
                outcome_mid_price
            from candidates
            union all
            select
                shard_index,
                trade_date,
                symbol,
                'P69_SPREAD_TRANSITION_FADE'::varchar as strategy_id,
                transition_type,
                spread_bucket,
                case
                    when abs(recent_return_bps) >= {float(min_abs_recent_return_bps)} then -sign(recent_return_bps)
                    else 0
                end::integer as side,
                mid_price,
                spread_bps,
                spread_change_bps,
                recent_return_bps,
                outcome_mid_price
            from candidates
        ),
        labels as (
            select
                *,
                (side * (outcome_mid_price / nullif(mid_price, 0.0) - 1.0) * 10000.0)::double as gross_bps,
                ((spread_bps / 2.0) + ({FIXED_SLIPPAGE_TICKS} * greatest(spread_bps, 0.01)) + {MARKETABLE_IMPACT_BPS} + {zerodha_bps})::double as cost_bps
            from signals
            where side != 0
              and transition_type != 'flat'
        ),
        bucketed as (
            select
                *,
                case
                    when abs(spread_change_bps) < 1.0 then 'C01_lt_1bp'
                    when abs(spread_change_bps) < 2.5 then 'C02_1_2p5bp'
                    when abs(spread_change_bps) < 5.0 then 'C03_2p5_5bp'
                    else 'C04_ge_5bp'
                end::varchar as spread_change_bucket,
                case
                    when abs(recent_return_bps) < 2.5 then 'R01_0p25_2p5bp'
                    when abs(recent_return_bps) < 5.0 then 'R02_2p5_5bp'
                    when abs(recent_return_bps) < 10.0 then 'R03_5_10bp'
                    else 'R04_ge_10bp'
                end::varchar as recent_return_bucket
            from labels
        )
        select
            shard_index,
            trade_date,
            symbol,
            strategy_id,
            transition_type,
            side,
            spread_bucket,
            spread_change_bucket,
            recent_return_bucket,
            count(*)::bigint as signal_rows,
            avg(gross_bps)::double as mean_gross_bps,
            median(gross_bps)::double as median_gross_bps,
            avg(gross_bps - cost_bps)::double as mean_after_cost_bps,
            avg(case when gross_bps > cost_bps then 1.0 else 0.0 end)::double as cost_clearing_rate,
            avg(case when gross_bps <= 0 then 1.0 else 0.0 end)::double as adverse_direction_rate,
            min(gross_bps)::double as worst_gross_bps,
            max(gross_bps)::double as best_gross_bps,
            avg(spread_bps)::double as mean_spread_bps,
            avg(spread_change_bps)::double as mean_spread_change_bps,
            avg(abs(recent_return_bps))::double as mean_abs_recent_return_bps,
            avg(cost_bps)::double as mean_cost_bps
        from bucketed
        group by shard_index, trade_date, symbol, strategy_id, transition_type, side, spread_bucket, spread_change_bucket, recent_return_bucket
        """
        return con.execute(sql).fetchdf()
    finally:
        con.close()


def run_labeling(
    dense_root: Path,
    limit_shards: int,
    lookback_ticks: int,
    outcome_horizon_ticks: int,
    min_abs_spread_change_bps: float,
    min_abs_recent_return_bps: float,
    max_rows_per_shard: int | None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    files = selected_files(dense_root, limit_shards)
    frames = [
        query_spread_transition_labels(
            path,
            shard_index,
            lookback_ticks,
            outcome_horizon_ticks,
            min_abs_spread_change_bps,
            min_abs_recent_return_bps,
            max_rows_per_shard,
        )
        for shard_index, path in files
    ]
    labels = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    inventory = pd.DataFrame([{"shard_index": shard_index, "shard_path": str(path)} for shard_index, path in files])
    return labels, inventory


def aggregate_labels(labels: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    if labels.empty:
        return pd.DataFrame()
    grouped = (
        labels.groupby(group_cols, sort=True)
        .agg(
            shard_symbol_label_rows=("signal_rows", "size"),
            symbols=("symbol", "nunique"),
            trade_dates=("trade_date", "nunique"),
            signal_rows=("signal_rows", "sum"),
            mean_gross_bps=("mean_gross_bps", "mean"),
            median_gross_bps=("median_gross_bps", "median"),
            mean_after_cost_bps=("mean_after_cost_bps", "mean"),
            mean_cost_clearing_rate=("cost_clearing_rate", "mean"),
            mean_adverse_direction_rate=("adverse_direction_rate", "mean"),
            worst_gross_bps=("worst_gross_bps", "min"),
            best_gross_bps=("best_gross_bps", "max"),
            mean_spread_bps=("mean_spread_bps", "mean"),
            mean_spread_change_bps=("mean_spread_change_bps", "mean"),
            mean_abs_recent_return_bps=("mean_abs_recent_return_bps", "mean"),
            mean_cost_bps=("mean_cost_bps", "mean"),
        )
        .reset_index()
    )
    grouped["label_candidate"] = (
        (grouped["signal_rows"] >= 500)
        & (grouped["symbols"] >= 2)
        & (grouped["mean_after_cost_bps"] > 0)
        & (grouped["mean_cost_clearing_rate"] >= 0.55)
        & (grouped["mean_adverse_direction_rate"] <= 0.45)
    )
    return grouped.sort_values(
        ["label_candidate", "mean_after_cost_bps", "mean_cost_clearing_rate", "signal_rows"],
        ascending=[False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def summarize(labels: pd.DataFrame, bucket_rollup: pd.DataFrame, inventory: pd.DataFrame, elapsed_seconds: float) -> pd.DataFrame:
    candidate_rows = int(bucket_rollup["label_candidate"].sum()) if not bucket_rollup.empty else 0
    best_after_cost = float(bucket_rollup["mean_after_cost_bps"].max()) if not bucket_rollup.empty else 0.0
    best_cost_clear = float(bucket_rollup["mean_cost_clearing_rate"].max()) if not bucket_rollup.empty else 0.0
    total_signals = int(labels["signal_rows"].sum()) if not labels.empty else 0
    return pd.DataFrame(
        [
            ("phase69_shards_scanned", int(len(inventory)), "Dense shards scanned"),
            ("phase69_label_rows", int(len(labels)), "Shard/symbol/spread-transition label rows"),
            ("phase69_signal_rows", total_signals, "No-lookahead spread-transition signal rows"),
            ("phase69_bucket_rollup_rows", int(len(bucket_rollup)), "Aggregated spread-transition bucket rows"),
            ("phase69_label_candidate_rows", candidate_rows, "Bucket rows passing spread-transition label gate"),
            ("phase69_best_mean_after_cost_bps", best_after_cost, "Best bucket mean after-cost bps"),
            ("phase69_best_cost_clearing_rate", best_cost_clear, "Best bucket cost-clearing rate"),
            ("phase69_survives_spread_transition_gate", int(candidate_rows > 0), "1 means a spread-transition bucket deserves targeted replay"),
            ("phase69_elapsed_seconds", elapsed_seconds, "Elapsed seconds"),
            ("phase69_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha retail intraday cost model"),
            (
                "phase69_recommend_next_action",
                "targeted_spread_transition_replay" if candidate_rows else "advance_to_cross_symbol_lead_lag_feature_family",
                "Recommended next action",
            ),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase69 Spread-Transition Labels",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase69 tests spread compression/expansion as a new feature family after replenishment-after-touch failed.",
        "Labels are no-lookahead received-tick outcomes with marketable retail cost proxies.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase69_spread_transition_labels_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase69(
    dense_root: Path,
    output_dir: Path,
    base_dir: Path,
    limit_shards: int,
    lookback_ticks: int,
    outcome_horizon_ticks: int,
    min_abs_spread_change_bps: float,
    min_abs_recent_return_bps: float,
    max_rows_per_shard: int | None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    labels, inventory = run_labeling(
        dense_root,
        limit_shards,
        lookback_ticks,
        outcome_horizon_ticks,
        min_abs_spread_change_bps,
        min_abs_recent_return_bps,
        max_rows_per_shard,
    )
    elapsed = time.perf_counter() - started
    bucket_rollup = aggregate_labels(labels, ["strategy_id", "transition_type", "side", "spread_bucket", "spread_change_bucket", "recent_return_bucket"])
    transition_rollup = aggregate_labels(labels, ["strategy_id", "transition_type", "side"])
    symbol_rollup = aggregate_labels(labels, ["symbol", "strategy_id", "transition_type", "side"])
    acceptance = summarize(labels, bucket_rollup, inventory, elapsed)

    inventory.to_csv(output_dir / "spread_transition_file_inventory.csv", index=False)
    labels.to_csv(output_dir / "spread_transition_label_rows.csv", index=False)
    bucket_rollup.to_csv(output_dir / "spread_transition_bucket_rollup.csv", index=False)
    transition_rollup.to_csv(output_dir / "spread_transition_strategy_rollup.csv", index=False)
    symbol_rollup.to_csv(output_dir / "spread_transition_symbol_rollup.csv", index=False)
    acceptance.to_csv(output_dir / "spread_transition_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Bucket Rollup": bucket_rollup,
            "Strategy Rollup": transition_rollup,
            "Symbol Rollup": symbol_rollup,
            "Label Rows": labels,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase69_spread_transition_labels",
        "dense_shards_scanned": int(len(inventory)),
        "survives_spread_transition_gate": int(
            acceptance.loc[acceptance["metric"].eq("phase69_survives_spread_transition_gate"), "value"].iloc[0]
        ),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase69",
            generated_utc=generated_utc,
            inputs={
                "phase51_dense_lake": str(dense_root),
                "phase67_feature_design_queue": "outputs/phase67/feature_design_queue.csv",
                "phase68_acceptance": "outputs/phase68/replenishment_acceptance_summary.csv",
            },
            parameters={
                "limit_shards": limit_shards,
                "lookback_ticks": lookback_ticks,
                "outcome_horizon_ticks": outcome_horizon_ticks,
                "min_abs_spread_change_bps": min_abs_spread_change_bps,
                "min_abs_recent_return_bps": min_abs_recent_return_bps,
                "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
                "label_gate": "signals_ge_500_and_symbols_ge_2_and_mean_after_cost_bps_gt_0_and_cost_clear_rate_ge_0_55_and_adverse_direction_rate_le_0_45",
            },
            outputs={
                "file_inventory": str(output_dir / "spread_transition_file_inventory.csv"),
                "label_rows": str(output_dir / "spread_transition_label_rows.csv"),
                "bucket_rollup": str(output_dir / "spread_transition_bucket_rollup.csv"),
                "strategy_rollup": str(output_dir / "spread_transition_strategy_rollup.csv"),
                "symbol_rollup": str(output_dir / "spread_transition_symbol_rollup.csv"),
                "acceptance_summary": str(output_dir / "spread_transition_acceptance_summary.csv"),
                "report": str(output_dir / "phase69_spread_transition_labels_report.md"),
                "manifest": str(output_dir / "phase69_spread_transition_labels_manifest.json"),
            },
            random_seed="none_deterministic_spread_transition_label_rollup",
            scenario_ids="phase69_spread_transition_labels",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase69_received_tick_lookback_outcome_horizons",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase69_spread_transition_labels_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate spread-transition labels from dense synthetic L2 shards.")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--limit-shards", type=int, default=32)
    parser.add_argument("--lookback-ticks", type=int, default=50)
    parser.add_argument("--outcome-horizon-ticks", type=int, default=100)
    parser.add_argument("--min-abs-spread-change-bps", type=float, default=0.001)
    parser.add_argument("--min-abs-recent-return-bps", type=float, default=0.25)
    parser.add_argument("--max-rows-per-shard", type=int, default=250_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase69(
        args.dense_root,
        args.output_dir,
        args.base_dir,
        args.limit_shards,
        args.lookback_ticks,
        args.outcome_horizon_ticks,
        args.min_abs_spread_change_bps,
        args.min_abs_recent_return_bps,
        args.max_rows_per_shard,
    )


if __name__ == "__main__":
    main()
