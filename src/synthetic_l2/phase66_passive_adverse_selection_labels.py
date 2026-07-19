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
from synthetic_l2.phase61_lower_frequency_candidate_sweep import _safe_path
from synthetic_l2.phase65_passive_queue_sensitivity import zerodha_roundtrip_bps
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase66")


def selected_files(dense_root: Path, limit_shards: int) -> list[tuple[int, Path]]:
    files = parquet_files(dense_root, limit_shards=limit_shards)
    return [(offset, path) for offset, path in enumerate(files, start=1)]


def query_label_rollup(
    path: Path,
    shard_index: int,
    touch_horizon_ticks: int,
    outcome_horizon_ticks: int,
    imbalance_threshold: float,
    max_rows_per_shard: int | None,
) -> pd.DataFrame:
    filter_sql = """
        buy_1_price > 0
        and sell_1_price > 0
        and sell_1_price >= buy_1_price
        and buy_1_quantity > 0
        and sell_1_quantity > 0
        and not coalesce(is_duplicate, false)
        and not coalesce(is_disconnect_gap, false)
        and not coalesce(is_out_of_order_injected, false)
    """
    if max_rows_per_shard is not None:
        filter_sql += f" and local_sequence_id <= {int(max_rows_per_shard)}"

    cost_bps = zerodha_roundtrip_bps()
    con = duckdb.connect()
    try:
        sql = f"""
        with base as (
            select
                {int(shard_index)}::integer as shard_index,
                trade_date,
                symbol,
                local_sequence_id,
                buy_1_price,
                sell_1_price,
                last_price,
                buy_1_quantity,
                sell_1_quantity,
                ((buy_1_price + sell_1_price) / 2.0)::double as mid_price,
                greatest(sell_1_price - buy_1_price, 0.01)::double as spread,
                greatest((sell_1_price - buy_1_price) / nullif(((buy_1_price + sell_1_price) / 2.0), 0.0) * 10000.0, 0.0)::double as spread_bps,
                (((buy_1_quantity - sell_1_quantity) / nullif((buy_1_quantity + sell_1_quantity), 0.0)))::double as l1_imbalance
            from read_parquet('{_safe_path(path)}', union_by_name=true)
            where {filter_sql}
        ),
        forward as (
            select
                *,
                lead(mid_price, {int(outcome_horizon_ticks)}) over (order by local_sequence_id)::double as outcome_mid_price,
                min(last_price) over (order by local_sequence_id rows between current row and {int(touch_horizon_ticks)} following)::double as touch_min_last_price,
                max(last_price) over (order by local_sequence_id rows between current row and {int(touch_horizon_ticks)} following)::double as touch_max_last_price,
                min(mid_price) over (order by local_sequence_id rows between current row and {int(touch_horizon_ticks)} following)::double as touch_min_mid_price,
                max(mid_price) over (order by local_sequence_id rows between current row and {int(touch_horizon_ticks)} following)::double as touch_max_mid_price
            from base
        ),
        candidates as (
            select
                shard_index,
                trade_date,
                symbol,
                'P66_JOIN_IMBALANCE'::varchar as strategy_id,
                case
                    when l1_imbalance >= {float(imbalance_threshold)} then 1
                    when l1_imbalance <= -{float(imbalance_threshold)} then -1
                    else 0
                end::integer as side,
                buy_1_price,
                sell_1_price,
                mid_price,
                spread_bps,
                abs(l1_imbalance)::double as abs_l1_imbalance,
                outcome_mid_price,
                touch_min_last_price,
                touch_max_last_price,
                touch_min_mid_price,
                touch_max_mid_price
            from forward
            union all
            select
                shard_index,
                trade_date,
                symbol,
                'P66_FADE_IMBALANCE'::varchar as strategy_id,
                case
                    when l1_imbalance >= {float(imbalance_threshold)} then -1
                    when l1_imbalance <= -{float(imbalance_threshold)} then 1
                    else 0
                end::integer as side,
                buy_1_price,
                sell_1_price,
                mid_price,
                spread_bps,
                abs(l1_imbalance)::double as abs_l1_imbalance,
                outcome_mid_price,
                touch_min_last_price,
                touch_max_last_price,
                touch_min_mid_price,
                touch_max_mid_price
            from forward
        ),
        touched as (
            select
                *,
                case
                    when side = 1 and (touch_min_last_price <= buy_1_price or touch_min_mid_price <= buy_1_price) then true
                    when side = -1 and (touch_max_last_price >= sell_1_price or touch_max_mid_price >= sell_1_price) then true
                    else false
                end as inferred_touch,
                case
                    when side = 1 then buy_1_price
                    when side = -1 then sell_1_price
                    else null
                end::double as assumed_fill_price,
                case
                    when spread_bps <= 1.0 then 'S01_le_1bp'
                    when spread_bps <= 2.5 then 'S02_1_2p5bp'
                    when spread_bps <= 5.0 then 'S03_2p5_5bp'
                    else 'S04_gt_5bp'
                end::varchar as spread_bucket,
                case
                    when abs_l1_imbalance <= 0.40 then 'I01_0p30_0p40'
                    when abs_l1_imbalance <= 0.60 then 'I02_0p40_0p60'
                    when abs_l1_imbalance <= 0.80 then 'I03_0p60_0p80'
                    else 'I04_gt_0p80'
                end::varchar as imbalance_bucket
            from candidates
            where side != 0
              and outcome_mid_price is not null
        ),
        labels as (
            select
                *,
                case
                    when side = 1 then (outcome_mid_price / nullif(assumed_fill_price, 0.0) - 1.0) * 10000.0
                    when side = -1 then (assumed_fill_price / nullif(outcome_mid_price, 0.0) - 1.0) * 10000.0
                    else null
                end::double as gross_bps_if_touched,
                case when inferred_touch then 1 else 0 end::integer as touch_label
            from touched
        )
        select
            shard_index,
            trade_date,
            symbol,
            strategy_id,
            side,
            spread_bucket,
            imbalance_bucket,
            count(*)::bigint as candidate_orders,
            sum(touch_label)::bigint as inferred_touches,
            avg(case when inferred_touch then gross_bps_if_touched else null end)::double as mean_gross_bps_if_touched,
            median(case when inferred_touch then gross_bps_if_touched else null end)::double as median_gross_bps_if_touched,
            avg(case when inferred_touch and gross_bps_if_touched <= 0 then 1.0 when inferred_touch then 0.0 else null end)::double as adverse_selection_rate,
            avg(case when inferred_touch and gross_bps_if_touched > {cost_bps} then 1.0 when inferred_touch then 0.0 else null end)::double as cost_clearing_rate,
            avg(case when inferred_touch then gross_bps_if_touched - {cost_bps} else null end)::double as mean_after_cost_bps_if_touched,
            min(case when inferred_touch then gross_bps_if_touched else null end)::double as worst_gross_bps_if_touched,
            max(case when inferred_touch then gross_bps_if_touched else null end)::double as best_gross_bps_if_touched,
            avg(spread_bps)::double as mean_spread_bps,
            avg(abs_l1_imbalance)::double as mean_abs_l1_imbalance
        from labels
        group by shard_index, trade_date, symbol, strategy_id, side, spread_bucket, imbalance_bucket
        having sum(touch_label) > 0
        """
        return con.execute(sql).fetchdf()
    finally:
        con.close()


def run_labeling(
    dense_root: Path,
    limit_shards: int,
    touch_horizon_ticks: int,
    outcome_horizon_ticks: int,
    imbalance_threshold: float,
    max_rows_per_shard: int | None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    files = selected_files(dense_root, limit_shards)
    frames = [
        query_label_rollup(path, shard_index, touch_horizon_ticks, outcome_horizon_ticks, imbalance_threshold, max_rows_per_shard)
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
            shard_symbol_label_rows=("inferred_touches", "size"),
            symbols=("symbol", "nunique"),
            trade_dates=("trade_date", "nunique"),
            candidate_orders=("candidate_orders", "sum"),
            inferred_touches=("inferred_touches", "sum"),
            mean_gross_bps_if_touched=("mean_gross_bps_if_touched", "mean"),
            median_gross_bps_if_touched=("median_gross_bps_if_touched", "median"),
            mean_after_cost_bps_if_touched=("mean_after_cost_bps_if_touched", "mean"),
            mean_adverse_selection_rate=("adverse_selection_rate", "mean"),
            mean_cost_clearing_rate=("cost_clearing_rate", "mean"),
            worst_gross_bps_if_touched=("worst_gross_bps_if_touched", "min"),
            best_gross_bps_if_touched=("best_gross_bps_if_touched", "max"),
            mean_spread_bps=("mean_spread_bps", "mean"),
            mean_abs_l1_imbalance=("mean_abs_l1_imbalance", "mean"),
        )
        .reset_index()
    )
    grouped["touch_rate"] = grouped["inferred_touches"] / grouped["candidate_orders"].where(grouped["candidate_orders"] != 0, 1)
    grouped["label_candidate"] = (
        (grouped["inferred_touches"] >= 500)
        & (grouped["mean_after_cost_bps_if_touched"] > 0)
        & (grouped["mean_cost_clearing_rate"] >= 0.55)
        & (grouped["mean_adverse_selection_rate"] <= 0.45)
    )
    return grouped.sort_values(
        ["label_candidate", "mean_after_cost_bps_if_touched", "mean_cost_clearing_rate", "inferred_touches"],
        ascending=[False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def summarize(
    labels: pd.DataFrame,
    strategy_rollup: pd.DataFrame,
    bucket_rollup: pd.DataFrame,
    inventory: pd.DataFrame,
    elapsed_seconds: float,
) -> pd.DataFrame:
    candidate_rows = int(bucket_rollup["label_candidate"].sum()) if not bucket_rollup.empty else 0
    best_after_cost = float(bucket_rollup["mean_after_cost_bps_if_touched"].max()) if not bucket_rollup.empty else 0.0
    best_cost_clear = float(bucket_rollup["mean_cost_clearing_rate"].max()) if not bucket_rollup.empty else 0.0
    total_touches = int(labels["inferred_touches"].sum()) if not labels.empty else 0
    total_candidates = int(labels["candidate_orders"].sum()) if not labels.empty else 0
    return pd.DataFrame(
        [
            ("phase66_shards_scanned", int(len(inventory)), "Dense shards scanned"),
            ("phase66_label_rows", int(len(labels)), "Shard/symbol/strategy/side/bucket rows with inferred touches"),
            ("phase66_candidate_orders", total_candidates, "Hypothetical passive order candidates in labeled rows"),
            ("phase66_inferred_touches", total_touches, "Inferred passive touch opportunities"),
            ("phase66_strategy_rollup_rows", int(len(strategy_rollup)), "Strategy/side rollup rows"),
            ("phase66_bucket_rollup_rows", int(len(bucket_rollup)), "Strategy/side/spread/imbalance bucket rollup rows"),
            ("phase66_label_candidate_rows", candidate_rows, "Bucket rows passing adverse-selection label gate"),
            ("phase66_best_mean_after_cost_bps_if_touched", best_after_cost, "Best bucket mean after-cost bps conditional on touch"),
            ("phase66_best_cost_clearing_rate", best_cost_clear, "Best bucket cost-clearing rate conditional on touch"),
            ("phase66_survives_label_gate", int(candidate_rows > 0), "1 means at least one passive label bucket deserves targeted replay"),
            ("phase66_elapsed_seconds", elapsed_seconds, "Elapsed seconds"),
            ("phase66_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha retail intraday cost model"),
            (
                "phase66_recommend_next_action",
                "targeted_passive_bucket_replay" if candidate_rows else "retire_naive_passive_imbalance_and_return_to_feature_design",
                "Recommended next action",
            ),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase66 Passive Adverse-Selection Labels",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase66 labels inferred passive touch opportunities for adverse selection and cost-clearing behavior.",
        "These are not observed broker fills; they are received-tick L2 labels for hypothetical passive orders.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase66_passive_adverse_selection_labels_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase66(
    dense_root: Path,
    output_dir: Path,
    base_dir: Path,
    limit_shards: int,
    touch_horizon_ticks: int,
    outcome_horizon_ticks: int,
    imbalance_threshold: float,
    max_rows_per_shard: int | None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    labels, inventory = run_labeling(
        dense_root,
        limit_shards,
        touch_horizon_ticks,
        outcome_horizon_ticks,
        imbalance_threshold,
        max_rows_per_shard,
    )
    elapsed = time.perf_counter() - started
    strategy_rollup = aggregate_labels(labels, ["strategy_id", "side"])
    bucket_rollup = aggregate_labels(labels, ["strategy_id", "side", "spread_bucket", "imbalance_bucket"])
    symbol_rollup = aggregate_labels(labels, ["symbol", "strategy_id", "side"])
    acceptance = summarize(labels, strategy_rollup, bucket_rollup, inventory, elapsed)

    inventory.to_csv(output_dir / "passive_label_file_inventory.csv", index=False)
    labels.to_csv(output_dir / "passive_adverse_selection_label_rows.csv", index=False)
    strategy_rollup.to_csv(output_dir / "passive_label_strategy_rollup.csv", index=False)
    bucket_rollup.to_csv(output_dir / "passive_label_bucket_rollup.csv", index=False)
    symbol_rollup.to_csv(output_dir / "passive_label_symbol_rollup.csv", index=False)
    acceptance.to_csv(output_dir / "passive_label_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Strategy Rollup": strategy_rollup,
            "Bucket Rollup": bucket_rollup,
            "Symbol Rollup": symbol_rollup,
            "Label Rows": labels,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase66_passive_adverse_selection_labels",
        "dense_shards_scanned": int(len(inventory)),
        "survives_label_gate": int(acceptance.loc[acceptance["metric"].eq("phase66_survives_label_gate"), "value"].iloc[0]),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase66",
            generated_utc=generated_utc,
            inputs={
                "phase51_dense_lake": str(dense_root),
                "phase65_acceptance": "outputs/phase65/passive_acceptance_summary.csv",
            },
            parameters={
                "limit_shards": limit_shards,
                "touch_horizon_ticks": touch_horizon_ticks,
                "outcome_horizon_ticks": outcome_horizon_ticks,
                "imbalance_threshold": imbalance_threshold,
                "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
                "label_gate": "touches_ge_500_and_mean_after_cost_bps_gt_0_and_cost_clear_rate_ge_0_55_and_adverse_selection_rate_le_0_45",
            },
            outputs={
                "file_inventory": str(output_dir / "passive_label_file_inventory.csv"),
                "label_rows": str(output_dir / "passive_adverse_selection_label_rows.csv"),
                "strategy_rollup": str(output_dir / "passive_label_strategy_rollup.csv"),
                "bucket_rollup": str(output_dir / "passive_label_bucket_rollup.csv"),
                "symbol_rollup": str(output_dir / "passive_label_symbol_rollup.csv"),
                "acceptance_summary": str(output_dir / "passive_label_acceptance_summary.csv"),
                "report": str(output_dir / "phase66_passive_adverse_selection_labels_report.md"),
                "manifest": str(output_dir / "phase66_passive_adverse_selection_labels_manifest.json"),
            },
            random_seed="none_deterministic_passive_label_rollup",
            scenario_ids="phase66_first_dense_shards_passive_adverse_selection_labels",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase66_received_tick_touch_and_outcome_horizons",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase66_passive_adverse_selection_labels_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate passive adverse-selection labels from dense synthetic L2 shards.")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--limit-shards", type=int, default=32)
    parser.add_argument("--touch-horizon-ticks", type=int, default=50)
    parser.add_argument("--outcome-horizon-ticks", type=int, default=100)
    parser.add_argument("--imbalance-threshold", type=float, default=0.30)
    parser.add_argument("--max-rows-per-shard", type=int, default=250_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase66(
        args.dense_root,
        args.output_dir,
        args.base_dir,
        args.limit_shards,
        args.touch_horizon_ticks,
        args.outcome_horizon_ticks,
        args.imbalance_threshold,
        args.max_rows_per_shard,
    )


if __name__ == "__main__":
    main()
