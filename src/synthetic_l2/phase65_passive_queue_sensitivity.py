from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase56_cost_clearing_label_discovery import DEFAULT_DENSE_ROOT, DEFAULT_ORDER_NOTIONAL_INR, parquet_files
from synthetic_l2.phase61_lower_frequency_candidate_sweep import _safe_path
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, calculate_equity_intraday_nse_charges


DEFAULT_OUTPUT_DIR = Path("outputs/phase65")


@dataclass(frozen=True)
class PassiveQueueProfile:
    queue_profile: str
    fill_weight: float
    adverse_selection_bps: float
    description: str


PASSIVE_QUEUE_PROFILES = [
    PassiveQueueProfile(
        queue_profile="pessimistic_back_of_queue",
        fill_weight=0.10,
        adverse_selection_bps=5.0,
        description="Assume only 10% of inferred touches fill and filled orders suffer 5 bps adverse selection.",
    ),
    PassiveQueueProfile(
        queue_profile="base_mid_queue",
        fill_weight=0.30,
        adverse_selection_bps=2.0,
        description="Assume 30% of inferred touches fill and filled orders suffer 2 bps adverse selection.",
    ),
    PassiveQueueProfile(
        queue_profile="optimistic_front_queue",
        fill_weight=0.60,
        adverse_selection_bps=0.0,
        description="Assume 60% of inferred touches fill with no extra adverse-selection haircut.",
    ),
]


def zerodha_roundtrip_bps() -> float:
    charges = calculate_equity_intraday_nse_charges(
        buy_value_inr=DEFAULT_ORDER_NOTIONAL_INR,
        sell_value_inr=DEFAULT_ORDER_NOTIONAL_INR,
    )
    return float(charges.effective_bps_on_buy_value)


def selected_files(dense_root: Path, limit_shards: int) -> list[tuple[int, Path]]:
    files = parquet_files(dense_root, limit_shards=limit_shards)
    return [(offset, path) for offset, path in enumerate(files, start=1)]


def query_passive_touch_candidates(
    path: Path,
    shard_index: int,
    horizon_ticks: int,
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
                ((buy_1_price + sell_1_price) / 2.0)::double as mid_price,
                greatest(sell_1_price - buy_1_price, 0.01)::double as spread,
                (((buy_1_quantity - sell_1_quantity) / nullif((buy_1_quantity + sell_1_quantity), 0.0)))::double as l1_imbalance
            from read_parquet('{_safe_path(path)}', union_by_name=true)
            where {filter_sql}
        ),
        forward as (
            select
                *,
                lead(mid_price, {int(horizon_ticks)}) over (order by local_sequence_id)::double as future_mid_price,
                min(last_price) over (order by local_sequence_id rows between current row and {int(horizon_ticks)} following)::double as future_min_last_price,
                max(last_price) over (order by local_sequence_id rows between current row and {int(horizon_ticks)} following)::double as future_max_last_price,
                min(mid_price) over (order by local_sequence_id rows between current row and {int(horizon_ticks)} following)::double as future_min_mid_price,
                max(mid_price) over (order by local_sequence_id rows between current row and {int(horizon_ticks)} following)::double as future_max_mid_price
            from base
        ),
        candidates as (
            select
                shard_index,
                trade_date,
                symbol,
                'P65_JOIN_IMBALANCE'::varchar as strategy_id,
                case
                    when l1_imbalance >= {float(imbalance_threshold)} then 1
                    when l1_imbalance <= -{float(imbalance_threshold)} then -1
                    else 0
                end::integer as side,
                buy_1_price,
                sell_1_price,
                mid_price,
                spread,
                l1_imbalance,
                future_mid_price,
                future_min_last_price,
                future_max_last_price,
                future_min_mid_price,
                future_max_mid_price
            from forward
            union all
            select
                shard_index,
                trade_date,
                symbol,
                'P65_FADE_IMBALANCE'::varchar as strategy_id,
                case
                    when l1_imbalance >= {float(imbalance_threshold)} then -1
                    when l1_imbalance <= -{float(imbalance_threshold)} then 1
                    else 0
                end::integer as side,
                buy_1_price,
                sell_1_price,
                mid_price,
                spread,
                l1_imbalance,
                future_mid_price,
                future_min_last_price,
                future_max_last_price,
                future_min_mid_price,
                future_max_mid_price
            from forward
        ),
        touched as (
            select
                *,
                case
                    when side = 1 and (future_min_last_price <= buy_1_price or future_min_mid_price <= buy_1_price) then true
                    when side = -1 and (future_max_last_price >= sell_1_price or future_max_mid_price >= sell_1_price) then true
                    else false
                end as inferred_touch,
                case
                    when side = 1 then future_mid_price / nullif(buy_1_price, 0.0) - 1.0
                    when side = -1 then sell_1_price / nullif(future_mid_price, 0.0) - 1.0
                    else null
                end::double as gross_return_if_filled
            from candidates
            where side != 0 and future_mid_price is not null
        )
        select
            shard_index,
            trade_date,
            symbol,
            strategy_id,
            count(*)::bigint as candidate_orders,
            sum(case when inferred_touch then 1 else 0 end)::bigint as inferred_touch_orders,
            sum(case when inferred_touch then gross_return_if_filled else 0.0 end)::double as gross_return_on_touches,
            avg(case when inferred_touch then gross_return_if_filled else null end)::double as mean_gross_return_on_touch,
            avg(spread / nullif(mid_price, 0.0) * 10000.0)::double as mean_spread_bps,
            avg(abs(l1_imbalance))::double as mean_abs_l1_imbalance,
            avg(case when inferred_touch and gross_return_if_filled > 0 then 1.0 when inferred_touch then 0.0 else null end)::double as touch_win_rate
        from touched
        group by shard_index, trade_date, symbol, strategy_id
        """
        return con.execute(sql).fetchdf()
    finally:
        con.close()


def expand_profiles(touch_results: pd.DataFrame, profiles: list[PassiveQueueProfile]) -> pd.DataFrame:
    if touch_results.empty:
        return pd.DataFrame()
    cost_bps = zerodha_roundtrip_bps()
    frames: list[pd.DataFrame] = []
    for profile in profiles:
        frame = touch_results.copy()
        frame["queue_profile"] = profile.queue_profile
        frame["fill_weight"] = float(profile.fill_weight)
        frame["adverse_selection_bps"] = float(profile.adverse_selection_bps)
        frame["zerodha_roundtrip_bps"] = cost_bps
        frame["expected_fills"] = frame["inferred_touch_orders"].astype(float) * float(profile.fill_weight)
        frame["expected_gross_pnl_inr"] = frame["gross_return_on_touches"].astype(float) * DEFAULT_ORDER_NOTIONAL_INR * float(profile.fill_weight)
        frame["expected_cost_pnl_drag_inr"] = (
            frame["inferred_touch_orders"].astype(float)
            * float(profile.fill_weight)
            * DEFAULT_ORDER_NOTIONAL_INR
            * ((cost_bps + float(profile.adverse_selection_bps)) / 10000.0)
        )
        frame["expected_net_pnl_inr"] = frame["expected_gross_pnl_inr"] - frame["expected_cost_pnl_drag_inr"]
        frame["queue_profile_description"] = profile.description
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def run_replay(
    dense_root: Path,
    limit_shards: int,
    horizon_ticks: int,
    imbalance_threshold: float,
    max_rows_per_shard: int | None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    files = selected_files(dense_root, limit_shards)
    raw_frames = [
        query_passive_touch_candidates(path, shard_index, horizon_ticks, imbalance_threshold, max_rows_per_shard)
        for shard_index, path in files
    ]
    raw = pd.concat(raw_frames, ignore_index=True) if raw_frames else pd.DataFrame()
    inventory = pd.DataFrame([{"shard_index": shard_index, "shard_path": str(path)} for shard_index, path in files])
    profiled = expand_profiles(raw, PASSIVE_QUEUE_PROFILES)
    if not profiled.empty:
        profiled["positive_after_costs"] = profiled["expected_net_pnl_inr"] > 0
    return profiled, inventory


def summarize(profiled: pd.DataFrame, inventory: pd.DataFrame, elapsed_seconds: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    if profiled.empty:
        summary = pd.DataFrame(
            [
                {
                    "strategy_id": "none",
                    "queue_profile": "none",
                    "shards_scanned": int(len(inventory)),
                    "symbols": 0,
                    "candidate_orders": 0,
                    "inferred_touch_orders": 0,
                    "expected_fills": 0.0,
                    "expected_net_pnl_inr": 0.0,
                    "phase65_survives_passive_sensitivity": False,
                }
            ]
        )
    else:
        summary = (
            profiled.groupby(["strategy_id", "queue_profile"], sort=True)
            .agg(
                shards_scanned=("shard_index", "nunique"),
                symbols=("symbol", "nunique"),
                trade_dates=("trade_date", "nunique"),
                candidate_orders=("candidate_orders", "sum"),
                inferred_touch_orders=("inferred_touch_orders", "sum"),
                expected_fills=("expected_fills", "sum"),
                expected_gross_pnl_inr=("expected_gross_pnl_inr", "sum"),
                expected_cost_pnl_drag_inr=("expected_cost_pnl_drag_inr", "sum"),
                expected_net_pnl_inr=("expected_net_pnl_inr", "sum"),
                positive_rows=("positive_after_costs", "sum"),
                mean_touch_win_rate=("touch_win_rate", "mean"),
                mean_spread_bps=("mean_spread_bps", "mean"),
            )
            .reset_index()
        )
        summary["positive_row_fraction"] = summary["positive_rows"] / summary["shards_scanned"].where(summary["shards_scanned"] != 0, 1)
        summary["expected_net_pnl_per_fill_inr"] = summary["expected_net_pnl_inr"] / summary["expected_fills"].where(
            summary["expected_fills"] != 0,
            np.nan,
        )
        profile_pivot = summary.pivot(index="strategy_id", columns="queue_profile", values="expected_net_pnl_inr")
        survives_by_strategy = (
            (profile_pivot.get("pessimistic_back_of_queue", pd.Series(dtype=float)) > 0)
            & (profile_pivot.get("base_mid_queue", pd.Series(dtype=float)) > 0)
            & (profile_pivot.get("optimistic_front_queue", pd.Series(dtype=float)) > 0)
        )
        summary["phase65_survives_passive_sensitivity"] = summary["strategy_id"].map(survives_by_strategy.to_dict()).fillna(False).astype(bool)
        summary = summary.sort_values(["phase65_survives_passive_sensitivity", "expected_net_pnl_inr"], ascending=[False, False])

    surviving_strategies = int(summary.loc[summary["phase65_survives_passive_sensitivity"], "strategy_id"].nunique())
    best_net = float(summary["expected_net_pnl_inr"].max()) if not summary.empty else 0.0
    if profiled.empty:
        unique_candidate_orders = 0
        unique_touch_orders = 0
    else:
        unique_strategy_rows = profiled.drop_duplicates(["shard_index", "trade_date", "symbol", "strategy_id"])
        unique_candidate_orders = int(unique_strategy_rows["candidate_orders"].sum())
        unique_touch_orders = int(unique_strategy_rows["inferred_touch_orders"].sum())
    acceptance = pd.DataFrame(
        [
            ("phase65_shards_scanned", int(len(inventory)), "Dense shards scanned"),
            ("phase65_strategy_profile_rows", int(len(summary)), "Strategy/queue-profile rows evaluated"),
            ("phase65_unique_candidate_orders", unique_candidate_orders, "Unique hypothetical passive order placements before queue-profile expansion"),
            ("phase65_unique_inferred_touch_orders", unique_touch_orders, "Unique orders whose limit price was touched within the horizon"),
            ("phase65_strategy_profile_expected_fills", float(summary["expected_fills"].sum()) if "expected_fills" in summary else 0.0, "Expected fills summed across strategy/profile rows"),
            ("phase65_best_expected_net_pnl_inr", best_net, "Best expected after-cost P&L across strategy/profile rows"),
            ("phase65_surviving_strategy_count", surviving_strategies, "Strategies positive under pessimistic, base and optimistic queue assumptions"),
            ("phase65_survives_passive_sensitivity", int(surviving_strategies > 0), "1 means at least one passive strategy survived all queue assumptions"),
            ("phase65_elapsed_seconds", elapsed_seconds, "Elapsed seconds"),
            ("phase65_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha retail intraday cost model"),
            (
                "phase65_recommend_next_action",
                "expand_survivor_to_disjoint_months" if surviving_strategies else "build_passive_adverse_selection_labels",
                "Recommended next action",
            ),
        ],
        columns=["metric", "value", "description"],
    )
    return summary, acceptance


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase65 Passive Queue-Capture Sensitivity Replay",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase65 starts the passive/limit-order branch after Phase64 retired the marketable-taker families.",
        "Fills are hypothetical: Zerodha top-five market-by-price data does not reveal true order identity or queue position.",
        "The replay therefore tests pessimistic, base and optimistic queue-fill assumptions instead of claiming observed passive fills.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase65_passive_queue_sensitivity_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase65(
    dense_root: Path,
    output_dir: Path,
    base_dir: Path,
    limit_shards: int,
    horizon_ticks: int,
    imbalance_threshold: float,
    max_rows_per_shard: int | None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    profiled, inventory = run_replay(dense_root, limit_shards, horizon_ticks, imbalance_threshold, max_rows_per_shard)
    elapsed = time.perf_counter() - started
    summary, acceptance = summarize(profiled, inventory, elapsed)
    profile_catalog = pd.DataFrame([profile.__dict__ for profile in PASSIVE_QUEUE_PROFILES])

    inventory.to_csv(output_dir / "passive_file_inventory.csv", index=False)
    profile_catalog.to_csv(output_dir / "passive_queue_profile_catalog.csv", index=False)
    profiled.to_csv(output_dir / "passive_daily_symbol_results.csv", index=False)
    summary.to_csv(output_dir / "passive_strategy_profile_summary.csv", index=False)
    acceptance.to_csv(output_dir / "passive_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Passive Strategy/Profile Summary": summary,
            "Queue Profile Catalog": profile_catalog,
            "Daily Symbol Results": profiled,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase65_passive_queue_sensitivity",
        "dense_shards_scanned": int(len(inventory)),
        "survives_passive_sensitivity": int(
            acceptance.loc[acceptance["metric"].eq("phase65_survives_passive_sensitivity"), "value"].iloc[0]
        ),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase65",
            generated_utc=generated_utc,
            inputs={
                "phase51_dense_lake": str(dense_root),
                "phase64_decision_ledger": "outputs/phase64/strategy_family_decision_ledger.csv",
            },
            parameters={
                "limit_shards": limit_shards,
                "horizon_ticks": horizon_ticks,
                "imbalance_threshold": imbalance_threshold,
                "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
                "fill_inference": "best_bid_or_ask_touch_within_future_horizon_from_received_l2_ticks",
                "survival_gate": "same_strategy_positive_under_pessimistic_base_and_optimistic_queue_profiles",
            },
            outputs={
                "file_inventory": str(output_dir / "passive_file_inventory.csv"),
                "queue_profile_catalog": str(output_dir / "passive_queue_profile_catalog.csv"),
                "daily_symbol_results": str(output_dir / "passive_daily_symbol_results.csv"),
                "summary": str(output_dir / "passive_strategy_profile_summary.csv"),
                "acceptance_summary": str(output_dir / "passive_acceptance_summary.csv"),
                "report": str(output_dir / "phase65_passive_queue_sensitivity_report.md"),
                "manifest": str(output_dir / "phase65_passive_queue_sensitivity_manifest.json"),
            },
            random_seed="none_deterministic_passive_touch_replay",
            scenario_ids="phase65_first_dense_shards_passive_queue_sensitivity",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase65_received_tick_horizon_touch_inference",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase65_passive_queue_sensitivity_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run passive queue-capture sensitivity replay on dense synthetic L2 shards.")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--limit-shards", type=int, default=16)
    parser.add_argument("--horizon-ticks", type=int, default=100)
    parser.add_argument("--imbalance-threshold", type=float, default=0.30)
    parser.add_argument("--max-rows-per-shard", type=int, default=250_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase65(
        args.dense_root,
        args.output_dir,
        args.base_dir,
        args.limit_shards,
        args.horizon_ticks,
        args.imbalance_threshold,
        args.max_rows_per_shard,
    )


if __name__ == "__main__":
    main()
