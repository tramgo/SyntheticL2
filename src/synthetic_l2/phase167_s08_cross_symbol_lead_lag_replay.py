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
from synthetic_l2.phase52_dense_lake_strategy_replay import DEFAULT_ORDER_NOTIONAL_INR, profile_cost_bps
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, charge_component_catalog


DEFAULT_CACHE_ROOT = Path("raw_synthetic_l2_phase166_cross_symbol_lead_lag_cache")
DEFAULT_PHASE166_DIR = Path("outputs/phase166")
DEFAULT_OUTPUT_DIR = Path("outputs/phase167")
DEFAULT_SCORE_THRESHOLD = 0.42
MIN_MARKET_SYMBOL_COUNT = 8
MAX_AVG_SPREAD_BPS = 10.0
MAX_BAD_FRACTION = 0.25
TRAIN_MONTHS = {"2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"}
TEST_MONTHS = {"2026-07", "2026-08", "2026-09", "2026-10", "2026-11", "2026-12"}
STRATEGY_ID = "P167_S08_CROSS_SYMBOL_LEAD_LAG_CONTINUATION"
SOURCE_STRATEGY_ID = "S08"


def safe_path(path: Path) -> str:
    return path.as_posix().replace("'", "''")


def cache_files(cache_root: Path, max_months: int | None = None) -> list[Path]:
    files = sorted(cache_root.glob("trade_month=*/part-00000.parquet"))
    if max_months is not None:
        files = files[: int(max_months)]
    if not files:
        raise FileNotFoundError(f"No Phase166 cache parquet files found under {cache_root}")
    return files


def quoted_paths(files: list[Path]) -> str:
    return ", ".join(f"'{safe_path(path)}'" for path in files)


def require_phase166_ready(phase166_dir: Path, allow_partial: bool) -> pd.DataFrame:
    summary_path = phase166_dir / "phase166_cross_symbol_cache_acceptance_summary.csv"
    if not summary_path.exists():
        raise FileNotFoundError(summary_path)
    summary = pd.read_csv(summary_path)
    metrics = dict(zip(summary["metric"], summary["value"]))
    ready = str(metrics.get("phase166_s08_cache_ready", "0")) == "1"
    policy = str(metrics.get("phase166_azure_read_policy", ""))
    if not allow_partial and not ready:
        raise RuntimeError("Phase166 S08 cache is not ready; refusing full Phase167 replay.")
    if policy != "forbidden_for_analysis_download_first_then_local":
        raise RuntimeError(f"Unexpected Phase166 Azure policy: {policy}")
    return summary


def profile_rows() -> list[dict[str, Any]]:
    rows = []
    for profile in EXECUTION_PROFILES:
        rows.append(
            {
                "execution_profile": str(profile["execution_profile"]),
                "decision_latency_buckets": int(profile["decision_latency_events"]),
                "broker_latency_buckets": int(profile["broker_latency_events"]),
                "total_latency_buckets": int(profile["decision_latency_events"]) + int(profile["broker_latency_events"]),
                "fixed_slippage_ticks": float(profile["fixed_slippage_ticks"]),
                "internal_impact_bps": float(profile["impact_bps"]) + float(profile.get("fees_bps", 0.0)),
                "zerodha_charge_bps": profile_cost_bps(profile),
                "apply_zerodha_equity_intraday_charges": bool(profile.get("apply_zerodha_equity_intraday_charges", False)),
                "order_notional_inr": float(profile.get("order_notional_inr", DEFAULT_ORDER_NOTIONAL_INR)),
                "cancel_on_stale_or_disconnect": bool(profile.get("cancel_on_stale_or_disconnect", False)),
                "fill_model": "marketable_full_fill_proxy",
                "fill_ratio": 1.0,
                "description": str(profile.get("description", "")),
            }
        )
    return rows


def write_trade_ledger(con: duckdb.DuckDBPyConnection, files: list[Path], output_dir: Path, score_threshold: float) -> Path:
    ledger_path = output_dir / "phase167_s08_cross_symbol_trade_ledger.parquet"
    union_parts = []
    for profile in profile_rows():
        total_latency = int(profile["total_latency_buckets"])
        slippage_ticks = float(profile["fixed_slippage_ticks"])
        impact_bps = float(profile["internal_impact_bps"])
        zerodha_bps = float(profile["zerodha_charge_bps"])
        order_notional = float(profile["order_notional_inr"])
        cancel_filter = (
            f"and duplicate_fraction <= {MAX_BAD_FRACTION} and disconnect_fraction <= {MAX_BAD_FRACTION} and out_of_order_fraction <= {MAX_BAD_FRACTION}"
            if bool(profile["cancel_on_stale_or_disconnect"])
            else ""
        )
        union_parts.append(
            f"""
            select
                trade_month,
                trade_date,
                symbol,
                sector,
                bucket_start_utc_ms as feed_event_bucket_utc_ms,
                bucket_start_utc_ms as feature_update_bucket_utc_ms,
                (bucket_start_utc_ms + ({total_latency} * bucket_ms))::double as order_arrival_bucket_utc_ms,
                '{STRATEGY_ID}' as strategy_id,
                '{SOURCE_STRATEGY_ID}' as source_strategy_id,
                'cross_symbol_lead_lag' as feature_family,
                'precommitted_phase167_single_s08_branch' as feature_status,
                '{profile["execution_profile"]}' as execution_profile,
                '{profile["fill_model"]}' as fill_model,
                {float(profile["fill_ratio"])}::double as fill_ratio,
                {total_latency}::integer as total_latency_buckets,
                {slippage_ticks}::double as fixed_slippage_ticks,
                {impact_bps}::double as internal_impact_bps,
                {zerodha_bps}::double as zerodha_charge_bps,
                {order_notional}::double as order_notional_inr,
                executable_signal::integer as side,
                phase167_score::double as signal_score,
                close_mid_price::double as arrival_mid_price,
                target_next_bucket_return::double as forward_return,
                avg_spread_bps::double as avg_spread_bps,
                ((avg_spread_bps / 20000.0)
                    + ({slippage_ticks} * 0.01 / nullif(close_mid_price, 0.0))
                    + ({impact_bps} / 10000.0)
                    + ({zerodha_bps} / 10000.0))::double as cost_return,
                (executable_signal * target_next_bucket_return)::double as gross_return,
                ((executable_signal * target_next_bucket_return)
                    - ((avg_spread_bps / 20000.0)
                    + ({slippage_ticks} * 0.01 / nullif(close_mid_price, 0.0))
                    + ({impact_bps} / 10000.0)
                    + ({zerodha_bps} / 10000.0)))::double as net_return,
                ((executable_signal * target_next_bucket_return) * {order_notional} * {float(profile["fill_ratio"])})::double as gross_pnl_inr,
                (((avg_spread_bps / 20000.0)
                    + ({slippage_ticks} * 0.01 / nullif(close_mid_price, 0.0))
                    + ({impact_bps} / 10000.0)
                    + ({zerodha_bps} / 10000.0)) * {order_notional} * {float(profile["fill_ratio"])})::double as cost_pnl_drag_inr,
                (((executable_signal * target_next_bucket_return)
                    - ((avg_spread_bps / 20000.0)
                    + ({slippage_ticks} * 0.01 / nullif(close_mid_price, 0.0))
                    + ({impact_bps} / 10000.0)
                    + ({zerodha_bps} / 10000.0))) * {order_notional} * {float(profile["fill_ratio"])})::double as net_pnl_inr,
                x_market_l5_ex_target_lag1_bucket,
                x_sector_l5_ex_target_lag1_bucket,
                etf_l5_pressure_mean_lag1_bucket,
                x_market_return_ex_target_lag1_bucket,
                x_sector_return_ex_target_lag1_bucket,
                etf_return_mean_lag1_bucket,
                market_symbol_count,
                duplicate_fraction,
                disconnect_fraction,
                out_of_order_fraction,
                'feed_bucket_to_feature_to_signal_to_latency_to_order_arrival_to_fill_to_cost_to_pnl' as lifecycle_model
            from (
                select
                    *,
                    lag(raw_signal, {total_latency}) over (partition by trade_date, symbol order by bucket_start_utc_ms) as executable_signal
                from phase167_features
            )
            where executable_signal != 0
                and target_next_bucket_return is not null
                {cancel_filter}
            """
        )
    con.execute(
        f"""
        create or replace temporary view phase167_features as
        with base as (
            select
                *,
                (
                    0.50 * coalesce(x_market_l5_ex_target_lag1_bucket, 0.0)
                    + 0.35 * coalesce(x_sector_l5_ex_target_lag1_bucket, 0.0)
                    + 0.15 * coalesce(etf_l5_pressure_mean_lag1_bucket, 0.0)
                ) as phase167_score
            from read_parquet([{quoted_paths(files)}], union_by_name=true)
            where not is_etf
                and target_next_bucket_return is not null
                and market_symbol_count >= {MIN_MARKET_SYMBOL_COUNT}
                and avg_spread_bps <= {MAX_AVG_SPREAD_BPS}
                and duplicate_fraction <= {MAX_BAD_FRACTION}
                and disconnect_fraction <= {MAX_BAD_FRACTION}
                and out_of_order_fraction <= {MAX_BAD_FRACTION}
        )
        select
            *,
            case
                when abs(phase167_score) >= {score_threshold} then sign(phase167_score)
                else 0
            end::integer as raw_signal
        from base
        """
    )
    con.execute(
        f"""
        copy (
            {" union all ".join(union_parts)}
            order by trade_month, trade_date, symbol, feed_event_bucket_utc_ms, execution_profile
        ) to '{safe_path(ledger_path)}' (format parquet, compression zstd)
        """
    )
    return ledger_path


def concentration(con: duckdb.DuckDBPyConnection, execution_profile: str, by: str, split: str, total_net: float) -> float:
    if abs(total_net) <= 0:
        return 0.0
    result = con.execute(
        f"""
        select max(abs(component_net)) / abs(?) as concentration
        from (
            select {by}, sum(net_pnl_inr) as component_net
            from phase167_trades
            where execution_profile = ? and split = ?
            group by {by}
        )
        """,
        [total_net, execution_profile, split],
    ).fetchone()[0]
    return float(result or 0.0)


def add_split_column(con: duckdb.DuckDBPyConnection, ledger_path: Path) -> None:
    con.execute(
        f"""
        create or replace temporary view phase167_trades as
        select
            *,
            case
                when trade_month in ({", ".join("'" + m + "'" for m in sorted(TRAIN_MONTHS))}) then 'train'
                when trade_month in ({", ".join("'" + m + "'" for m in sorted(TEST_MONTHS))}) then 'test'
                else 'excluded'
            end as split
        from read_parquet('{safe_path(ledger_path)}')
        """
    )


def summarize(
    con: duckdb.DuckDBPyConnection,
    ledger_path: Path,
    elapsed_seconds: float,
    cache_file_count: int,
    source_summary: pd.DataFrame,
    score_threshold: float,
) -> dict[str, pd.DataFrame]:
    add_split_column(con, ledger_path)
    profile_summary = con.execute(
        """
        select
            strategy_id,
            source_strategy_id,
            feature_family,
            feature_status,
            execution_profile,
            count(*)::bigint as trades,
            count(distinct symbol)::integer as symbols,
            count(distinct trade_month)::integer as months,
            count(distinct trade_date)::integer as trade_dates,
            sum(gross_return)::double as sum_gross_return,
            sum(cost_return)::double as sum_cost_return,
            sum(net_return)::double as sum_net_return,
            avg(gross_return)::double as mean_gross_return,
            avg(cost_return)::double as mean_cost_return,
            avg(net_return)::double as mean_net_return,
            sum(gross_pnl_inr)::double as gross_pnl_inr,
            sum(cost_pnl_drag_inr)::double as cost_pnl_drag_inr,
            sum(net_pnl_inr)::double as annual_net_pnl_inr,
            min(net_pnl_inr)::double as worst_trade_pnl_inr,
            avg(case when gross_return > cost_return then 1.0 else 0.0 end)::double as precision_cost_clear,
            avg(avg_spread_bps)::double as mean_spread_bps,
            max(total_latency_buckets)::integer as total_latency_buckets,
            max(fixed_slippage_ticks)::double as fixed_slippage_ticks,
            max(internal_impact_bps)::double as internal_impact_bps,
            max(zerodha_charge_bps)::double as zerodha_charge_bps
        from phase167_trades
        group by strategy_id, source_strategy_id, feature_family, feature_status, execution_profile
        order by annual_net_pnl_inr desc, trades desc
        """
    ).fetchdf()
    split_summary = con.execute(
        """
        select
            execution_profile,
            split,
            count(*)::bigint as trades,
            count(distinct symbol)::integer as symbols,
            count(distinct trade_month)::integer as months,
            sum(gross_pnl_inr)::double as gross_pnl_inr,
            sum(cost_pnl_drag_inr)::double as cost_pnl_drag_inr,
            sum(net_pnl_inr)::double as net_pnl_inr,
            avg(case when gross_return > cost_return then 1.0 else 0.0 end)::double as precision_cost_clear
        from phase167_trades
        group by execution_profile, split
        order by execution_profile, split
        """
    ).fetchdf()
    monthly = con.execute(
        """
        select
            execution_profile,
            split,
            trade_month,
            count(*)::bigint as trades,
            count(distinct symbol)::integer as symbols,
            sum(gross_pnl_inr)::double as gross_pnl_inr,
            sum(cost_pnl_drag_inr)::double as cost_pnl_drag_inr,
            sum(net_pnl_inr)::double as net_pnl_inr,
            avg(case when gross_return > cost_return then 1.0 else 0.0 end)::double as precision_cost_clear
        from phase167_trades
        group by execution_profile, split, trade_month
        order by execution_profile, split, trade_month
        """
    ).fetchdf()
    symbol = con.execute(
        """
        select
            execution_profile,
            split,
            symbol,
            count(*)::bigint as trades,
            count(distinct trade_month)::integer as months,
            sum(gross_pnl_inr)::double as gross_pnl_inr,
            sum(cost_pnl_drag_inr)::double as cost_pnl_drag_inr,
            sum(net_pnl_inr)::double as net_pnl_inr,
            avg(case when gross_return > cost_return then 1.0 else 0.0 end)::double as precision_cost_clear
        from phase167_trades
        group by execution_profile, split, symbol
        order by execution_profile, split, symbol
        """
    ).fetchdf()
    gate_rows = []
    for row in profile_summary.to_dict("records"):
        profile = row["execution_profile"]
        train = split_summary[(split_summary["execution_profile"].eq(profile)) & (split_summary["split"].eq("train"))]
        test = split_summary[(split_summary["execution_profile"].eq(profile)) & (split_summary["split"].eq("test"))]
        train_net = float(train["net_pnl_inr"].iloc[0]) if not train.empty else 0.0
        test_net = float(test["net_pnl_inr"].iloc[0]) if not test.empty else 0.0
        test_trades = int(test["trades"].iloc[0]) if not test.empty else 0
        test_symbols = int(test["symbols"].iloc[0]) if not test.empty else 0
        test_precision = float(test["precision_cost_clear"].iloc[0]) if not test.empty else 0.0
        test_months = monthly[(monthly["execution_profile"].eq(profile)) & (monthly["split"].eq("test"))]
        positive_test_months = int((test_months["net_pnl_inr"] > 0).sum()) if not test_months.empty else 0
        month_conc = concentration(con, profile, "trade_month", "test", test_net)
        symbol_conc = concentration(con, profile, "symbol", "test", test_net)
        gate_rows.append(
            {
                "strategy_id": STRATEGY_ID,
                "execution_profile": profile,
                "train_net_pnl_inr": train_net,
                "test_net_pnl_inr": test_net,
                "test_trades": test_trades,
                "test_symbols": test_symbols,
                "test_positive_months": positive_test_months,
                "test_precision_cost_clear": test_precision,
                "test_max_month_contribution_abs": month_conc,
                "test_max_symbol_contribution_abs": symbol_conc,
                "train_positive_after_costs": train_net > 0,
                "test_positive_after_costs": test_net > 0,
                "coverage_pass": test_trades >= 500 and test_symbols >= 20,
                "stability_pass": positive_test_months >= 4 and month_conc <= 0.35 and symbol_conc <= 0.35,
                "precision_pass": test_precision >= 0.52,
            }
        )
    gates = pd.DataFrame(gate_rows)
    if not gates.empty:
        gates["phase167_profile_pass"] = (
            gates["train_positive_after_costs"]
            & gates["test_positive_after_costs"]
            & gates["coverage_pass"]
            & gates["stability_pass"]
            & gates["precision_pass"]
        )
    candidate_rows = int(gates["phase167_profile_pass"].sum()) if not gates.empty else 0
    best = profile_summary.iloc[0].to_dict() if not profile_summary.empty else {}
    source_metrics = dict(zip(source_summary["metric"], source_summary["value"]))
    acceptance = pd.DataFrame(
        [
            ("phase167_source_cache_ready", int(str(source_metrics.get("phase166_s08_cache_ready", "0")) == "1"), "Inherited Phase166 S08 cache-ready flag"),
            ("phase167_cache_files_scanned", cache_file_count, "Phase166 monthly cache files scanned"),
            ("phase167_strategy_id", STRATEGY_ID, "Exactly one precommitted S08 alpha branch"),
            ("phase167_score_threshold", score_threshold, "Fixed absolute score threshold set before replay"),
            ("phase167_execution_profile_rows", int(len(profile_summary)), "Execution profile variants replayed side by side"),
            ("phase167_trade_rows", int(profile_summary["trades"].sum()) if not profile_summary.empty else 0, "Full trade-level rows written to parquet"),
            ("phase167_positive_after_cost_profile_rows", int((profile_summary["annual_net_pnl_inr"] > 0).sum()) if not profile_summary.empty else 0, "Profile rows positive after all costs"),
            ("phase167_candidate_profile_rows", candidate_rows, "Rows passing positive, coverage, stability and precision gates"),
            ("phase167_best_execution_profile", str(best.get("execution_profile", "none")), "Best profile by annual net P&L"),
            ("phase167_best_annual_net_pnl_inr", float(best.get("annual_net_pnl_inr", 0.0)), "Best annual after-cost net P&L"),
            ("phase167_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha equity intraday NSE charge formula reused"),
            ("phase167_strategy_promotion_allowed", int(candidate_rows > 0), "Synthetic-only promotion gate; paper/live remains closed regardless"),
            ("phase167_paper_or_live_acceptance_allowed", 0, "Broker/paper/live acceptance remains closed"),
            ("phase167_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from synthetic-only replay"),
            ("phase167_azure_read_policy", "forbidden_for_analysis_download_first_then_local", "No direct Python Azure scanning"),
            (
                "phase167_next_best_action",
                "write_s08_dormant_real_l2_handoff_if_candidate_survives" if candidate_rows > 0 else "close_s08_current_form_and_update_blocklist_candidate",
                "Recommended next milestone",
            ),
            ("phase167_elapsed_seconds", float(elapsed_seconds), "Runner elapsed seconds"),
        ],
        columns=["metric", "value", "description"],
    )
    return {
        "acceptance": acceptance,
        "profile_summary": profile_summary,
        "split_summary": split_summary,
        "monthly_summary": monthly,
        "symbol_summary": symbol,
        "gate_evaluation": gates,
        "execution_profile_catalog": pd.DataFrame(profile_rows()),
        "zerodha_charge_component_catalog": charge_component_catalog(),
    }


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame], ledger_path: Path) -> None:
    lines = [
        "# Phase167 S08 Cross-symbol Lead-lag Replay",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase167 runs one precommitted S08 cross-symbol lead-lag branch from the local Phase166 cache.",
        "The replay models feed bucket, feature update, signal, latency, order arrival, fill proxy, Zerodha/internal costs, and P&L/risk update.",
        "This is synthetic-only evidence. Broker/paper/live acceptance and deployable profitability claims remain closed.",
        "",
        f"Full trade-level ledger: `{ledger_path.as_posix()}`",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame.head(80)), ""])
    (output_dir / "phase167_s08_cross_symbol_replay_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase167(
    cache_root: Path,
    phase166_dir: Path,
    output_dir: Path,
    base_dir: Path,
    score_threshold: float,
    max_months: int | None = None,
    reuse_existing_ledger: bool = False,
) -> None:
    started = time.perf_counter()
    output_dir.mkdir(parents=True, exist_ok=True)
    allow_partial = max_months is not None
    source_summary = require_phase166_ready(phase166_dir, allow_partial=allow_partial)
    files = cache_files(cache_root, max_months=max_months)
    con = duckdb.connect()
    try:
        ledger_path = output_dir / "phase167_s08_cross_symbol_trade_ledger.parquet"
        if not (reuse_existing_ledger and ledger_path.exists()):
            ledger_path = write_trade_ledger(con, files, output_dir, score_threshold)
        frames = summarize(con, ledger_path, time.perf_counter() - started, len(files), source_summary, score_threshold)
    finally:
        con.close()
    frames["acceptance"].to_csv(output_dir / "phase167_s08_replay_acceptance_summary.csv", index=False)
    frames["profile_summary"].to_csv(output_dir / "phase167_s08_strategy_profile_summary.csv", index=False)
    frames["split_summary"].to_csv(output_dir / "phase167_s08_split_summary.csv", index=False)
    frames["monthly_summary"].to_csv(output_dir / "phase167_s08_monthly_summary.csv", index=False)
    frames["symbol_summary"].to_csv(output_dir / "phase167_s08_symbol_summary.csv", index=False)
    frames["gate_evaluation"].to_csv(output_dir / "phase167_s08_gate_evaluation.csv", index=False)
    frames["execution_profile_catalog"].to_csv(output_dir / "phase167_execution_profile_catalog.csv", index=False)
    frames["zerodha_charge_component_catalog"].to_csv(output_dir / "phase167_zerodha_charge_component_catalog.csv", index=False)
    write_report(output_dir, frames, ledger_path)
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase167_s08_cross_symbol_lead_lag_replay",
        **reproducibility_fields(
            artifact_id="phase167_s08_cross_symbol_lead_lag_replay",
            generated_utc=generated,
            inputs={
                "phase166_cache_root": str(cache_root),
                "phase166_summary": str(phase166_dir / "phase166_cross_symbol_cache_acceptance_summary.csv"),
                "cache_files_scanned": len(files),
            },
            parameters={
                "strategy_id": STRATEGY_ID,
                "score_threshold": score_threshold,
                "min_market_symbol_count": MIN_MARKET_SYMBOL_COUNT,
                "max_avg_spread_bps": MAX_AVG_SPREAD_BPS,
                "max_bad_fraction": MAX_BAD_FRACTION,
                "execution_profiles": ";".join(row["execution_profile"] for row in profile_rows()),
                "strategy_promotion_allowed": int(frames["gate_evaluation"]["phase167_profile_pass"].sum()) if not frames["gate_evaluation"].empty else 0,
                "paper_or_live_acceptance_allowed": 0,
                "azure_read_policy": "forbidden_for_analysis_download_first_then_local",
            },
            outputs={
                "trade_ledger": str(output_dir / "phase167_s08_cross_symbol_trade_ledger.parquet"),
                "acceptance_summary": str(output_dir / "phase167_s08_replay_acceptance_summary.csv"),
                "profile_summary": str(output_dir / "phase167_s08_strategy_profile_summary.csv"),
                "gate_evaluation": str(output_dir / "phase167_s08_gate_evaluation.csv"),
            },
            random_seed="none_deterministic_phase167_sql_replay",
            scenario_ids="phase166_cross_symbol_lead_lag_cache_from_phase162_distributional_full_year_dense_l2",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase12_execution_profiles_v1_reused_for_phase167_bucket_latency",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase167_s08_cross_symbol_replay_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-root", type=Path, default=DEFAULT_CACHE_ROOT)
    parser.add_argument("--phase166-dir", type=Path, default=DEFAULT_PHASE166_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--score-threshold", type=float, default=DEFAULT_SCORE_THRESHOLD)
    parser.add_argument("--max-months", type=int, default=None)
    parser.add_argument("--reuse-existing-ledger", action="store_true")
    args = parser.parse_args()
    run_phase167(
        args.cache_root,
        args.phase166_dir,
        args.output_dir,
        args.base_dir,
        args.score_threshold,
        args.max_months,
        args.reuse_existing_ledger,
    )


if __name__ == "__main__":
    main()
