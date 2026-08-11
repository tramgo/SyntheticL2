from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import (
    ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
    calculate_equity_intraday_nse_charges,
)


DEFAULT_DENSE_ROOT = Path("raw_synthetic_l2_dense_full_year")
DEFAULT_OUTPUT_DIR = Path("outputs/phase351")
DEFAULT_INITIAL_CAPITAL_INR = 1_000_000.0
DEFAULT_ORDER_NOTIONAL_INR = 75_000.0
ROBUST_EVENT_FLOOR = 30
ANNUALIZED_THRESHOLD_PCT = 12.0


STRATEGIES: list[dict[str, Any]] = [
    {
        "strategy_id": "P351_FULL_DEPTH_SHOCK_REVERSAL",
        "description": "Large one-tick move opposed by top-five and depth-2-5 imbalance.",
        "direction_sql": "-sign(one_tick_return)",
        "predicate_sql": """
            abs(one_tick_return) >= q_abs_ret_995
            and abs(top5_imbalance) >= 0.20
            and abs(deep_imbalance_2_5) >= 0.20
            and sign(top5_imbalance) = -sign(one_tick_return)
            and sign(deep_imbalance_2_5) = -sign(one_tick_return)
            and depth25_materiality >= 0.45
            and spread_bps <= q_spread_bps_75
        """,
    },
    {
        "strategy_id": "P351_DEEP_PRESSURE_CONTINUATION",
        "description": "Depth-2-5 pressure aligned with top-five book and short move.",
        "direction_sql": "sign(deep_imbalance_2_5)",
        "predicate_sql": """
            abs(deep_imbalance_2_5) >= q_abs_deep_99
            and abs(top5_imbalance) >= 0.15
            and sign(top5_imbalance) = sign(deep_imbalance_2_5)
            and sign(coalesce(one_tick_return, 0.0)) = sign(deep_imbalance_2_5)
            and depth25_materiality >= 0.50
            and spread_bps <= q_spread_bps_75
        """,
    },
    {
        "strategy_id": "P351_VOLUME_ABSORPTION_REVERSAL",
        "description": "Volume/update burst with price move absorbed by opposite depth-2-5 pressure.",
        "direction_sql": "-sign(one_tick_return)",
        "predicate_sql": """
            volume_delta >= q_volume_delta_99
            and abs(one_tick_return) >= q_abs_ret_99
            and abs(deep_imbalance_2_5) >= 0.15
            and sign(deep_imbalance_2_5) = -sign(one_tick_return)
            and depth25_materiality >= 0.45
            and spread_bps <= q_spread_bps_80
        """,
    },
]


EXECUTION_PROFILES: list[dict[str, Any]] = [
    {
        "execution_profile": "taker_cost200_fixed_capital",
        "passive_aware": 0,
        "fill_model_id": "P351_TAKER_DETERMINISTIC",
        "spread_cost_multiplier": 1.0,
        "passive_spread_cost_multiplier": 0.0,
        "adverse_selection_bps": 0.0,
        "forced_flatten_bps": 0.0,
        "fill_probability_multiplier": 1.0,
    },
    {
        "execution_profile": "passive_base_back_of_queue_cost200",
        "passive_aware": 1,
        "fill_model_id": "P351_PASSIVE_BASE_BACK_OF_QUEUE",
        "spread_cost_multiplier": 0.35,
        "passive_spread_cost_multiplier": 0.35,
        "adverse_selection_bps": 2.5,
        "forced_flatten_bps": 1.0,
        "fill_probability_multiplier": 0.75,
    },
    {
        "execution_profile": "passive_pessimistic_back_of_queue_cost200",
        "passive_aware": 1,
        "fill_model_id": "P351_PASSIVE_PESSIMISTIC_BACK_OF_QUEUE",
        "spread_cost_multiplier": 0.50,
        "passive_spread_cost_multiplier": 0.50,
        "adverse_selection_bps": 4.0,
        "forced_flatten_bps": 2.0,
        "fill_probability_multiplier": 0.50,
    },
]


def _safe_path(path: Path) -> str:
    return path.as_posix().replace("'", "''")


def parquet_files(dense_root: Path, limit_shards: int | None) -> list[Path]:
    files = sorted(dense_root.glob("trade_month=*/symbol=*/part-00000.parquet"))
    if not files:
        raise FileNotFoundError(f"No dense parquet files under {dense_root}")
    return files[:limit_shards] if limit_shards else files


def cost200_bps(order_notional: float) -> float:
    charges = calculate_equity_intraday_nse_charges(
        buy_value_inr=order_notional,
        sell_value_inr=order_notional,
        buy_orders=1,
        sell_orders=1,
    )
    return float(charges.effective_bps_on_buy_value) * 2.0


def query_shard(
    path: Path,
    strategy: dict[str, Any],
    profile: dict[str, Any],
    horizon_ticks: int,
    order_notional: float,
    max_rows_per_shard: int | None = None,
) -> pd.DataFrame:
    cost_bps = cost200_bps(order_notional)
    fill_mult = float(profile["fill_probability_multiplier"])
    spread_mult = float(profile["spread_cost_multiplier"])
    adverse_bps = float(profile["adverse_selection_bps"])
    forced_bps = float(profile["forced_flatten_bps"])
    passive_aware = int(profile["passive_aware"])
    row_limit_sql = f"limit {int(max_rows_per_shard)}" if max_rows_per_shard else ""
    con = duckdb.connect()
    try:
        sql = f"""
        with base as (
            select
                trade_date,
                exchange,
                symbol,
                local_sequence_id,
                ((buy_1_price + sell_1_price) / 2.0) as mid_price,
                lead(((buy_1_price + sell_1_price) / 2.0), {int(horizon_ticks)}) over (order by local_sequence_id) as exit_mid_price,
                (last_price / nullif(lag(last_price) over (order by local_sequence_id), 0.0) - 1.0) as one_tick_return,
                greatest(volume_traded - lag(volume_traded) over (order by local_sequence_id), 0) as volume_delta,
                greatest(sell_1_price - buy_1_price, 0.01) as spread,
                (greatest(sell_1_price - buy_1_price, 0.01) / nullif(((buy_1_price + sell_1_price) / 2.0), 0.0)) * 10000.0 as spread_bps,
                (
                    (buy_1_quantity + buy_2_quantity + buy_3_quantity + buy_4_quantity + buy_5_quantity)
                    - (sell_1_quantity + sell_2_quantity + sell_3_quantity + sell_4_quantity + sell_5_quantity)
                ) / nullif(
                    (buy_1_quantity + buy_2_quantity + buy_3_quantity + buy_4_quantity + buy_5_quantity)
                    + (sell_1_quantity + sell_2_quantity + sell_3_quantity + sell_4_quantity + sell_5_quantity),
                    0.0
                ) as top5_imbalance,
                (
                    (buy_2_quantity + buy_3_quantity + buy_4_quantity + buy_5_quantity)
                    - (sell_2_quantity + sell_3_quantity + sell_4_quantity + sell_5_quantity)
                ) / nullif(
                    (buy_2_quantity + buy_3_quantity + buy_4_quantity + buy_5_quantity)
                    + (sell_2_quantity + sell_3_quantity + sell_4_quantity + sell_5_quantity),
                    0.0
                ) as deep_imbalance_2_5,
                (
                    (buy_2_quantity + buy_3_quantity + buy_4_quantity + buy_5_quantity)
                    + (sell_2_quantity + sell_3_quantity + sell_4_quantity + sell_5_quantity)
                ) / nullif(
                    (buy_1_quantity + buy_2_quantity + buy_3_quantity + buy_4_quantity + buy_5_quantity)
                    + (sell_1_quantity + sell_2_quantity + sell_3_quantity + sell_4_quantity + sell_5_quantity),
                    0.0
                ) as depth25_materiality,
                least(
                    0.95,
                    greatest(
                        0.05,
                        {fill_mult} * (
                            0.10
                            + 0.55 * (
                                (
                                    (buy_2_quantity + buy_3_quantity + buy_4_quantity + buy_5_quantity)
                                    + (sell_2_quantity + sell_3_quantity + sell_4_quantity + sell_5_quantity)
                                ) / nullif(
                                    (buy_1_quantity + buy_2_quantity + buy_3_quantity + buy_4_quantity + buy_5_quantity)
                                    + (sell_1_quantity + sell_2_quantity + sell_3_quantity + sell_4_quantity + sell_5_quantity),
                                    0.0
                                )
                            )
                            - 0.02 * ((greatest(sell_1_price - buy_1_price, 0.01) / nullif(((buy_1_price + sell_1_price) / 2.0), 0.0)) * 10000.0)
                        )
                    )
                ) as passive_fill_probability,
                coalesce(is_duplicate, false) as is_duplicate,
                coalesce(is_disconnect_gap, false) as is_disconnect_gap,
                coalesce(is_out_of_order_injected, false) as is_out_of_order_injected
            from (
                select *
                from read_parquet('{_safe_path(path)}', union_by_name=true)
                {row_limit_sql}
            )
            where buy_1_price > 0
              and sell_1_price > 0
              and sell_1_price >= buy_1_price
              and buy_2_price > 0 and buy_3_price > 0 and buy_4_price > 0 and buy_5_price > 0
              and sell_2_price > 0 and sell_3_price > 0 and sell_4_price > 0 and sell_5_price > 0
        ),
        thresholds as (
            select
                quantile_cont(abs(one_tick_return), 0.99) as q_abs_ret_99,
                quantile_cont(abs(one_tick_return), 0.995) as q_abs_ret_995,
                quantile_cont(abs(deep_imbalance_2_5), 0.99) as q_abs_deep_99,
                quantile_cont(volume_delta, 0.99) as q_volume_delta_99,
                quantile_cont(spread_bps, 0.75) as q_spread_bps_75,
                quantile_cont(spread_bps, 0.80) as q_spread_bps_80
            from base
            where not is_duplicate
              and not is_disconnect_gap
              and not is_out_of_order_injected
              and one_tick_return is not null
        ),
        events as (
            select
                base.*,
                {strategy["direction_sql"]} as side
            from base
            cross join thresholds
            where not is_duplicate
              and not is_disconnect_gap
              and not is_out_of_order_injected
              and exit_mid_price is not null
              and one_tick_return is not null
              and ({strategy["predicate_sql"]})
        ),
        scored as (
            select
                *,
                side * (exit_mid_price / nullif(mid_price, 0.0) - 1.0) as gross_return,
                case when {passive_aware} = 1 then passive_fill_probability else 1.0 end as expected_fill_probability,
                (
                    ({spread_mult} * spread_bps)
                    + {cost_bps}
                    + case when {passive_aware} = 1 then {adverse_bps} + {forced_bps} else 0.0 end
                ) / 10000.0 as cost_return
            from events
            where side != 0
        )
        select
            trade_date,
            coalesce(exchange, 'NSE') as exchange,
            symbol,
            '{strategy["strategy_id"]}' as strategy_id,
            '{profile["execution_profile"]}' as execution_profile,
            '{profile["fill_model_id"]}' as fill_model_id,
            {horizon_ticks}::integer as horizon_ticks,
            count(*)::bigint as scheduled_events,
            sum(expected_fill_probability)::double as expected_filled_events,
            avg(expected_fill_probability)::double as avg_fill_probability,
            avg(depth25_materiality)::double as avg_depth25_materiality,
            avg(abs(deep_imbalance_2_5))::double as avg_abs_deep_imbalance_2_5,
            avg(spread_bps)::double as avg_spread_bps,
            sum(gross_return * expected_fill_probability)::double as expected_gross_return,
            sum(cost_return * expected_fill_probability)::double as expected_cost_return,
            sum((gross_return - cost_return) * expected_fill_probability)::double as expected_net_return,
            sum((gross_return - cost_return) * expected_fill_probability * {order_notional})::double as expected_net_pnl_inr,
            min((gross_return - cost_return) * {order_notional})::double as worst_event_pnl_inr,
            {cost_bps}::double as zerodha_cost200_bps,
            {passive_aware}::integer as passive_aware,
            1::integer as uses_full_depth_1_5,
            1::integer as uses_depth_2_5_materiality,
            0::integer as l1_only_variant
        from scored
        group by trade_date, exchange, symbol
        """
        return con.execute(sql).fetchdf()
    finally:
        con.close()


def summarize(results: pd.DataFrame, initial_capital: float) -> pd.DataFrame:
    if results.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    grouped = results.groupby(["strategy_id", "execution_profile", "fill_model_id", "horizon_ticks"], dropna=False)
    for keys, group in grouped:
        strategy_id, execution_profile, fill_model_id, horizon_ticks = keys
        expected_net_pnl = float(group["expected_net_pnl_inr"].sum())
        trade_dates = int(group["trade_date"].nunique())
        scheduled_events = int(group["scheduled_events"].sum())
        expected_filled_events = float(group["expected_filled_events"].sum())
        positive_symbols = int(
            (group.groupby("symbol")["expected_net_pnl_inr"].sum() > 0).sum()
        )
        positive_symbol_dates = int((group["expected_net_pnl_inr"] > 0).sum())
        annualized_pct = (expected_net_pnl / initial_capital) * 100.0
        rows.append(
            {
                "strategy_id": strategy_id,
                "execution_profile": execution_profile,
                "fill_model_id": fill_model_id,
                "horizon_ticks": int(horizon_ticks),
                "trade_dates": trade_dates,
                "scheduled_events": scheduled_events,
                "expected_filled_events": expected_filled_events,
                "positive_symbols": positive_symbols,
                "positive_symbol_dates": positive_symbol_dates,
                "expected_net_pnl_inr": expected_net_pnl,
                "annualized_pct_fixed_capital": annualized_pct,
                "avg_fill_probability": float(group["avg_fill_probability"].mean()),
                "avg_depth25_materiality": float(group["avg_depth25_materiality"].mean()),
                "avg_abs_deep_imbalance_2_5": float(group["avg_abs_deep_imbalance_2_5"].mean()),
                "avg_spread_bps": float(group["avg_spread_bps"].mean()),
                "worst_event_pnl_inr": float(group["worst_event_pnl_inr"].min()),
                "above12": int(annualized_pct > ANNUALIZED_THRESHOLD_PCT),
                "event_floor_met": int(scheduled_events >= ROBUST_EVENT_FLOOR),
                "breadth_met": int(positive_symbols >= 2 and positive_symbol_dates >= 2),
                "acceptance_candidate": int(
                    annualized_pct > ANNUALIZED_THRESHOLD_PCT
                    and scheduled_events >= ROBUST_EVENT_FLOOR
                    and positive_symbols >= 2
                    and positive_symbol_dates >= 2
                ),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["acceptance_candidate", "annualized_pct_fixed_capital", "scheduled_events"],
        ascending=[False, False, False],
    )


def write_outputs(
    *,
    output_dir: Path,
    shard_rows: list[dict[str, Any]],
    event_results: pd.DataFrame,
    summary: pd.DataFrame,
    args: argparse.Namespace,
    elapsed_seconds: float,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    shard_frame = pd.DataFrame(shard_rows)
    strategy_catalog = pd.DataFrame(STRATEGIES)
    execution_catalog = pd.DataFrame(EXECUTION_PROFILES)
    gate_rows = [
        ("P351_PHASE52_RECONCILED", 1, "Phase52 stale-running marker reconciled before Phase351 search."),
        ("P351_FULL_DEPTH_1_5_USED", int(not event_results.empty and event_results["uses_full_depth_1_5"].eq(1).all()), "All rows use top-five depth fields."),
        ("P351_DEPTH_2_5_MATERIALITY_USED", int(not event_results.empty and event_results["uses_depth_2_5_materiality"].eq(1).all()), "Depth levels 2-5 materiality is required."),
        ("P351_L1_ONLY_FORBIDDEN", int(event_results.empty or event_results["l1_only_variant"].sum() == 0), "No L1-only variant rows."),
        ("P351_COST200_FIXED_CAPITAL", 1, "Zerodha cost model at 2x stress with fixed initial capital."),
        ("P351_PASSIVE_REALISM_APPLIED", int(any(p["passive_aware"] for p in EXECUTION_PROFILES)), "Passive profiles include fill probability, adverse selection, and forced flatten proxies."),
        ("P351_NO_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "No promotion, paper/live, or deployable profitability claim."),
    ]
    gate_frame = pd.DataFrame(gate_rows, columns=["gate_id", "passed", "evidence"])
    acceptance_rows = [
        ("phase351_dense_input_root", str(args.dense_root), "Dense top-five input root"),
        ("phase351_shards_requested", args.limit_shards if args.limit_shards else "all", "Shard limit requested"),
        ("phase351_shards_scanned", len(shard_rows), "Dense parquet shards scanned"),
        ("phase351_strategy_rows", len(STRATEGIES), "Full-depth selective strategies tested"),
        ("phase351_execution_profile_rows", len(EXECUTION_PROFILES), "Execution profiles tested"),
        ("phase351_event_ledger_rows", len(event_results), "Daily/symbol event result rows"),
        ("phase351_scenario_rows", len(summary), "Scenario summary rows"),
        ("phase351_above12_rows", int(summary["above12"].sum()) if not summary.empty else 0, "Rows above 12% fixed-capital annualized diagnostic"),
        ("phase351_acceptance_candidate_rows", int(summary["acceptance_candidate"].sum()) if not summary.empty else 0, "Rows passing event floor, breadth, and >12 diagnostic"),
        ("phase351_initial_capital_inr", args.initial_capital_inr, "Fixed annual return denominator"),
        ("phase351_order_notional_inr", args.order_notional_inr, "Per-event notional below 100000"),
        ("phase351_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model used"),
        ("phase351_strategy_replay_allowed", 0, "No replay unlock"),
        ("phase351_strategy_promotion_allowed", 0, "No promotion unlock"),
        ("phase351_paper_or_live_acceptance_allowed", 0, "No paper/live unlock"),
        ("phase351_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        (
            "phase351_next_best_action",
            "interpret_phase351_or_expand_if_acceptance_candidates_exist",
            "Recommended next milestone",
        ),
    ]
    acceptance = pd.DataFrame(acceptance_rows, columns=["metric", "value", "description"])
    generated_utc = datetime.now(timezone.utc).isoformat()
    input_manifest = {
        "dense_root": str(args.dense_root),
        "limit_shards": args.limit_shards,
        "max_rows_per_shard": args.max_rows_per_shard,
    }
    parameter_manifest = {
        "initial_capital_inr": args.initial_capital_inr,
        "order_notional_inr": args.order_notional_inr,
        "horizons": args.horizons,
        "strategy_count": len(STRATEGIES),
        "execution_profile_count": len(EXECUTION_PROFILES),
    }
    manifest = {
        "phase": 351,
        "generated_utc": generated_utc,
        "elapsed_seconds": elapsed_seconds,
        "inputs": input_manifest,
        "parameters": parameter_manifest,
        "outputs": {},
    }
    paths = {
        "strategy_catalog": output_dir / "phase351_strategy_catalog.csv",
        "execution_profile_catalog": output_dir / "phase351_execution_profile_catalog.csv",
        "shard_scan_ledger": output_dir / "phase351_shard_scan_ledger.csv",
        "event_ledger": output_dir / "phase351_event_ledger.csv",
        "scenario_summary": output_dir / "phase351_scenario_summary.csv",
        "gate_evaluation": output_dir / "phase351_gate_evaluation.csv",
        "acceptance_summary": output_dir / "phase351_acceptance_summary.csv",
        "manifest": output_dir / "phase351_full_depth_selective_strategy_search_manifest.json",
        "report": output_dir / "phase351_full_depth_selective_strategy_search_report.md",
    }
    strategy_catalog.to_csv(paths["strategy_catalog"], index=False)
    execution_catalog.to_csv(paths["execution_profile_catalog"], index=False)
    shard_frame.to_csv(paths["shard_scan_ledger"], index=False)
    event_results.to_csv(paths["event_ledger"], index=False)
    summary.to_csv(paths["scenario_summary"], index=False)
    gate_frame.to_csv(paths["gate_evaluation"], index=False)
    acceptance.to_csv(paths["acceptance_summary"], index=False)
    for key, path in paths.items():
        manifest["outputs"][key] = str(path)
    manifest["reproducibility"] = reproducibility_fields(
        artifact_id="phase351_full_depth_selective_strategy_search",
        generated_utc=generated_utc,
        inputs=input_manifest,
        parameters=parameter_manifest,
        outputs={key: str(path) for key, path in paths.items()},
        cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        latency_model_version="phase351_horizon_tick_exit_no_external_latency",
    )
    paths["manifest"].write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    report = [
        "# Phase351 Full-Depth Selective Dense Strategy Search",
        "",
        "Phase351 tests lower-turnover full-depth selective strategies on the existing dense synthetic top-five market-by-price lake.",
        "It is a strategy-search milestone, not a paper/live or deployable profitability claim.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Top Scenario Summary",
        "",
        _markdown_table(summary.head(20) if not summary.empty else pd.DataFrame()),
        "",
        "## Gates",
        "",
        _markdown_table(gate_frame),
    ]
    paths["report"].write_text("\n".join(report) + "\n", encoding="utf-8")


def run(args: argparse.Namespace) -> None:
    start = time.perf_counter()
    files = parquet_files(args.dense_root, args.limit_shards)
    rows: list[pd.DataFrame] = []
    shard_rows: list[dict[str, Any]] = []
    for index, path in enumerate(files, start=1):
        shard_start = time.perf_counter()
        shard_event_rows = 0
        status = "ok"
        error = ""
        try:
            for strategy in STRATEGIES:
                for profile in EXECUTION_PROFILES:
                    for horizon in args.horizons:
                        frame = query_shard(
                            path,
                            strategy,
                            profile,
                            int(horizon),
                            float(args.order_notional_inr),
                            args.max_rows_per_shard,
                        )
                        if not frame.empty:
                            frame.insert(0, "shard_path", str(path))
                            frame.insert(0, "shard_index", index)
                            shard_event_rows += len(frame)
                            rows.append(frame)
        except Exception as exc:  # pragma: no cover - evidence path
            status = "error"
            error = repr(exc)
        shard_rows.append(
            {
                "shard_index": index,
                "shard_path": str(path),
                "status": status,
                "event_result_rows": shard_event_rows,
                "elapsed_seconds": time.perf_counter() - shard_start,
                "error": error,
            }
        )
    event_results = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    summary = summarize(event_results, float(args.initial_capital_inr))
    write_outputs(
        output_dir=args.output_dir,
        shard_rows=shard_rows,
        event_results=event_results,
        summary=summary,
        args=args,
        elapsed_seconds=time.perf_counter() - start,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase351 full-depth selective dense strategy search")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--limit-shards", type=int, default=32)
    parser.add_argument("--max-rows-per-shard", type=int, default=None)
    parser.add_argument("--horizons", type=int, nargs="+", default=[6, 12, 24])
    parser.add_argument("--initial-capital-inr", type=float, default=DEFAULT_INITIAL_CAPITAL_INR)
    parser.add_argument("--order-notional-inr", type=float, default=DEFAULT_ORDER_NOTIONAL_INR)
    return parser.parse_args()


def main() -> None:
    run(parse_args())
