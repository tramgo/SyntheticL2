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
from synthetic_l2.phase70_cross_symbol_lead_lag_labels import symbol_universe
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase73")
DEFAULT_TRADE_MONTH = "2026-01"
DEFAULT_TIME_BUCKET_SECONDS = 5_000
DEFAULT_LEADER_SYMBOL = "HDFCBANK"
DEFAULT_LEADER_THRESHOLD = 0.00428699


def monthly_files(dense_root: Path, trade_month: str) -> list[Path]:
    files = sorted((dense_root / f"trade_month={trade_month}").glob("symbol=*/part-00000.parquet"))
    if not files:
        raise FileNotFoundError(f"No dense parquet files for trade_month={trade_month} under {dense_root}")
    return files


def query_timestamp_bars(path: Path, time_bucket_seconds: int, max_rows_per_symbol: int | None) -> pd.DataFrame:
    filter_sql = """
        buy_1_price > 0
        and sell_1_price > 0
        and sell_1_price >= buy_1_price
        and callback_received_utc_ms is not null
        and not coalesce(is_duplicate, false)
        and not coalesce(is_disconnect_gap, false)
        and not coalesce(is_out_of_order_injected, false)
    """
    if max_rows_per_symbol is not None:
        filter_sql += f" and local_sequence_id <= {int(max_rows_per_symbol)}"
    con = duckdb.connect()
    try:
        sql = f"""
        with source as (
            select *
            from read_parquet('{_safe_path(path)}', union_by_name=true)
            where {filter_sql}
        ),
        anchored as (
            select
                *,
                min(callback_received_utc_ms) over () as min_callback_received_utc_ms
            from source
        ),
        base as (
            select
                trade_date,
                trade_month,
                symbol,
                local_sequence_id,
                callback_received_utc_ms,
                floor((callback_received_utc_ms - min_callback_received_utc_ms) / {int(time_bucket_seconds)})::integer as time_bucket_id,
                ((buy_1_price + sell_1_price) / 2.0)::double as mid_price,
                greatest(sell_1_price - buy_1_price, 0.01)::double as spread,
                greatest(sell_1_price - buy_1_price, 0.01)::double as tick_size_proxy,
                ((buy_1_quantity - sell_1_quantity) / nullif((buy_1_quantity + sell_1_quantity), 0.0))::double as l1_imbalance
            from anchored
        ),
        bars as (
            select
                trade_date,
                trade_month,
                symbol,
                {int(time_bucket_seconds)}::integer as time_bucket_seconds,
                time_bucket_id,
                count(*)::bigint as rows_in_bucket,
                min(callback_received_utc_ms)::bigint as bucket_start_utc_s,
                max(callback_received_utc_ms)::bigint as bucket_end_utc_s,
                first(mid_price order by local_sequence_id)::double as open_mid_price,
                last(mid_price order by local_sequence_id)::double as close_mid_price,
                avg(spread)::double as avg_spread,
                avg(tick_size_proxy)::double as avg_tick_size_proxy,
                avg(l1_imbalance)::double as avg_l1_imbalance
            from base
            group by trade_date, trade_month, symbol, time_bucket_id
            having count(*) >= 10
        )
        select
            *,
            close_mid_price / nullif(open_mid_price, 0.0) - 1.0 as bar_return,
            lead(close_mid_price) over (order by time_bucket_id) / nullif(close_mid_price, 0.0) - 1.0 as next_bar_return
        from bars
        """
        return con.execute(sql).fetchdf()
    finally:
        con.close()


def load_timestamp_matrix(
    dense_root: Path,
    trade_month: str,
    time_bucket_seconds: int,
    max_rows_per_symbol: int | None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    files = monthly_files(dense_root, trade_month)
    frames = [query_timestamp_bars(path, time_bucket_seconds, max_rows_per_symbol) for path in files]
    matrix = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    inventory = pd.DataFrame([{"symbol": path.parent.name.replace("symbol=", ""), "shard_path": str(path)} for path in files])
    return matrix, inventory


def evaluate_hdfcbank_near_miss(matrix: pd.DataFrame, threshold: float) -> pd.DataFrame:
    if matrix.empty:
        return pd.DataFrame()
    target_symbols = [symbol for symbol in symbol_universe() if symbol != DEFAULT_LEADER_SYMBOL and symbol not in {"BANKBEES", "GOLDBEES", "ITBEES", "JUNIORBEES", "NIFTYBEES"}]
    leader = matrix[matrix["symbol"].eq(DEFAULT_LEADER_SYMBOL)][["trade_date", "time_bucket_id", "bar_return"]].rename(
        columns={"bar_return": "leader_bar_return"}
    )
    targets = matrix[matrix["symbol"].isin(target_symbols)].copy()
    joined = targets.merge(leader, on=["trade_date", "time_bucket_id"], how="inner")
    joined = joined[joined["next_bar_return"].notna() & joined["leader_bar_return"].abs().ge(float(threshold))].copy()
    if joined.empty:
        return pd.DataFrame()
    profile = retail_profile()
    slippage_ticks = float(profile["fixed_slippage_ticks"])
    impact_bps = float(profile["impact_bps"]) + float(profile.get("fees_bps", 0.0))
    zerodha_bps = profile_cost_bps(profile)
    joined["side"] = np.sign(joined["leader_bar_return"].astype(float))
    joined = joined[joined["side"].ne(0)].copy()
    joined["gross_return"] = joined["side"].astype(float) * joined["next_bar_return"].astype(float)
    joined["cost_return"] = (
        ((joined["avg_spread"].astype(float) / 2.0) / joined["close_mid_price"].astype(float))
        + (slippage_ticks * joined["avg_tick_size_proxy"].astype(float) / joined["close_mid_price"].astype(float))
        + (impact_bps / 10000.0)
        + (zerodha_bps / 10000.0)
    )
    joined["net_return"] = joined["gross_return"] - joined["cost_return"]
    symbol_net = joined.groupby("symbol", sort=True)["net_return"].sum()
    trades = int(len(joined))
    gross = float(joined["gross_return"].sum() * DEFAULT_ORDER_NOTIONAL_INR)
    cost = float(joined["cost_return"].sum() * DEFAULT_ORDER_NOTIONAL_INR)
    return pd.DataFrame(
        [
            {
                "rule_id": "P73_TIMESTAMP_HDFCBANK_MOMENTUM_Q70_RECHECK",
                "phase70_reference_rule_id": "P70_MEGA_HDFCBANK_MOMENTUM_Q70",
                "leader_symbol": DEFAULT_LEADER_SYMBOL,
                "alignment": "timestamp_bucket",
                "threshold": float(threshold),
                "trades": trades,
                "target_symbols": int(joined["symbol"].nunique()),
                "net_pnl_inr": float(joined["net_return"].sum() * DEFAULT_ORDER_NOTIONAL_INR),
                "gross_pnl_proxy_inr": gross,
                "cost_pnl_drag_proxy_inr": cost,
                "precision_cost_clear": float((joined["gross_return"] > joined["cost_return"]).mean()),
                "positive_target_fraction": float((symbol_net > 0).mean()) if int(symbol_net.shape[0]) else 0.0,
                "cost_drag_to_abs_gross_ratio": cost / abs(gross) if abs(gross) > 0 else np.nan,
            }
        ]
    )


def shock_panel_audit(dense_root: Path, limit_shards: int, max_rows_per_shard: int | None) -> tuple[pd.DataFrame, pd.DataFrame]:
    files = parquet_files(dense_root, limit_shards=limit_shards)
    rows: list[dict[str, Any]] = []
    con = duckdb.connect()
    try:
        for shard_index, path in enumerate(files, start=1):
            filter_sql = ""
            if max_rows_per_shard is not None:
                filter_sql = f"where local_sequence_id <= {int(max_rows_per_shard)}"
            sql = f"""
            select
                {int(shard_index)}::integer as shard_index,
                any_value(trade_month)::varchar as trade_month,
                any_value(symbol)::varchar as symbol,
                count(*)::bigint as row_count,
                sum(case when coalesce(is_market_shock_day, false) then 1 else 0 end)::bigint as market_shock_rows,
                sum(case when coalesce(is_symbol_shock, false) then 1 else 0 end)::bigint as symbol_shock_rows,
                count(distinct regime_code)::integer as regime_count,
                mode(regime_code)::varchar as dominant_regime_code,
                mode(feed_profile)::varchar as dominant_feed_profile
            from read_parquet('{_safe_path(path)}', union_by_name=true)
            {filter_sql}
            """
            rows.append(con.execute(sql).fetchdf().iloc[0].to_dict())
    finally:
        con.close()
    detail = pd.DataFrame(rows)
    detail["has_market_shock"] = detail["market_shock_rows"] > 0
    detail["has_symbol_shock"] = detail["symbol_shock_rows"] > 0
    monthly = (
        detail.groupby("trade_month", sort=True)
        .agg(
            shard_count=("shard_index", "size"),
            symbols=("symbol", "nunique"),
            row_count=("row_count", "sum"),
            market_shock_rows=("market_shock_rows", "sum"),
            symbol_shock_rows=("symbol_shock_rows", "sum"),
            market_shock_symbols=("has_market_shock", "sum"),
            symbol_shock_symbols=("has_symbol_shock", "sum"),
            regimes=("dominant_regime_code", "nunique"),
            feed_profiles=("dominant_feed_profile", "nunique"),
        )
        .reset_index()
    )
    monthly["market_shock_symbol_fraction"] = monthly["market_shock_symbols"] / monthly["symbols"].where(monthly["symbols"] != 0, 1)
    monthly["symbol_shock_symbol_fraction"] = monthly["symbol_shock_symbols"] / monthly["symbols"].where(monthly["symbols"] != 0, 1)
    return detail, monthly


def summarize(
    matrix: pd.DataFrame,
    inventory: pd.DataFrame,
    recheck: pd.DataFrame,
    shock_monthly: pd.DataFrame,
    elapsed_seconds: float,
) -> pd.DataFrame:
    recheck_positive = bool(not recheck.empty and float(recheck.iloc[0]["net_pnl_inr"]) > 0)
    recheck_passes = bool(
        recheck_positive
        and float(recheck.iloc[0]["precision_cost_clear"]) >= 0.55
        and float(recheck.iloc[0]["cost_drag_to_abs_gross_ratio"]) <= 0.50
        and float(recheck.iloc[0]["positive_target_fraction"]) >= 0.50
    ) if not recheck.empty else False
    balanced_shock_months = int(
        ((shock_monthly["market_shock_symbol_fraction"] >= 0.50) | (shock_monthly["symbol_shock_symbol_fraction"] >= 0.10)).sum()
    ) if not shock_monthly.empty else 0
    return pd.DataFrame(
        [
            ("phase73_symbols_loaded", int(inventory["symbol"].nunique()) if not inventory.empty else 0, "Symbols loaded for timestamp matrix"),
            ("phase73_timestamp_bar_rows", int(len(matrix)), "Timestamp-aligned symbol bar rows"),
            ("phase73_hdfcbank_recheck_positive", int(recheck_positive), "1 means HDFCBANK lead-lag near-miss remains positive under timestamp alignment"),
            ("phase73_hdfcbank_recheck_passes_gate", int(recheck_passes), "1 means timestamp-aligned HDFCBANK recheck passes quality gates"),
            ("phase73_shock_months_audited", int(len(shock_monthly)), "Trade-month partitions included in shock-panel audit"),
            ("phase73_balanced_shock_months", balanced_shock_months, "Months with broad market shock or meaningful symbol-shock coverage"),
            ("phase73_allow_replay_expansion", int(recheck_passes and balanced_shock_months >= 2), "1 means near-miss replay expansion is allowed"),
            ("phase73_elapsed_seconds", elapsed_seconds, "Elapsed seconds"),
            ("phase73_recommend_next_action", "targeted_replay_after_alignment" if recheck_passes else "generator_alignment_remediation_plan", "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase73 Timestamp Alignment and Shock-Panel Audit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase73 audits the two Phase72 near-misses before any replay expansion.",
        "It rechecks HDFCBANK cross-symbol lead-lag with timestamp-aligned bars and audits shock scenario coverage across bounded dense shards.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase73_timestamp_alignment_shock_panel_audit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase73(
    dense_root: Path,
    output_dir: Path,
    base_dir: Path,
    trade_month: str,
    time_bucket_seconds: int,
    max_rows_per_symbol: int | None,
    shock_limit_shards: int,
    shock_max_rows_per_shard: int | None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    matrix, inventory = load_timestamp_matrix(dense_root, trade_month, time_bucket_seconds, max_rows_per_symbol)
    recheck = evaluate_hdfcbank_near_miss(matrix, DEFAULT_LEADER_THRESHOLD)
    shock_detail, shock_monthly = shock_panel_audit(dense_root, shock_limit_shards, shock_max_rows_per_shard)
    elapsed = time.perf_counter() - started
    acceptance = summarize(matrix, inventory, recheck, shock_monthly, elapsed)

    inventory.to_csv(output_dir / "timestamp_matrix_file_inventory.csv", index=False)
    matrix.to_csv(output_dir / "timestamp_bar_matrix.csv", index=False)
    recheck.to_csv(output_dir / "hdfcbank_timestamp_recheck.csv", index=False)
    shock_detail.to_csv(output_dir / "shock_panel_detail.csv", index=False)
    shock_monthly.to_csv(output_dir / "shock_panel_monthly.csv", index=False)
    acceptance.to_csv(output_dir / "timestamp_alignment_shock_panel_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "HDFCBANK Timestamp Recheck": recheck,
            "Shock Panel Monthly": shock_monthly,
            "Shock Panel Detail Sample": shock_detail.head(80),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase73_timestamp_alignment_shock_panel_audit",
        "allow_replay_expansion": int(acceptance.loc[acceptance["metric"].eq("phase73_allow_replay_expansion"), "value"].iloc[0]),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase73",
            generated_utc=generated_utc,
            inputs={
                "phase51_dense_lake": str(dense_root),
                "phase72_audit": "outputs/phase72/research_audit_acceptance_summary.csv",
                "phase72_near_misses": "outputs/phase72/near_miss_watchlist.csv",
            },
            parameters={
                "trade_month": trade_month,
                "time_bucket_seconds": time_bucket_seconds,
                "max_rows_per_symbol": max_rows_per_symbol if max_rows_per_symbol is not None else "none_full_symbol_scan",
                "hdfcbank_threshold": DEFAULT_LEADER_THRESHOLD,
                "shock_limit_shards": shock_limit_shards,
                "shock_max_rows_per_shard": shock_max_rows_per_shard if shock_max_rows_per_shard is not None else "none_full_shard_scan",
                "replay_gate": "hdfcbank_timestamp_recheck_quality_passes_and_balanced_shock_months_ge_2",
            },
            outputs={
                "timestamp_inventory": str(output_dir / "timestamp_matrix_file_inventory.csv"),
                "timestamp_matrix": str(output_dir / "timestamp_bar_matrix.csv"),
                "hdfcbank_recheck": str(output_dir / "hdfcbank_timestamp_recheck.csv"),
                "shock_detail": str(output_dir / "shock_panel_detail.csv"),
                "shock_monthly": str(output_dir / "shock_panel_monthly.csv"),
                "acceptance_summary": str(output_dir / "timestamp_alignment_shock_panel_acceptance_summary.csv"),
                "report": str(output_dir / "phase73_timestamp_alignment_shock_panel_audit_report.md"),
                "manifest": str(output_dir / "phase73_timestamp_alignment_shock_panel_audit_manifest.json"),
            },
            random_seed="none_deterministic_alignment_audit",
            scenario_ids="phase73_timestamp_alignment_and_shock_panel",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase73_timestamp_bucket_alignment",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase73_timestamp_alignment_shock_panel_audit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit timestamp alignment and shock-panel coverage before replay expansion.")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--trade-month", type=str, default=DEFAULT_TRADE_MONTH)
    parser.add_argument("--time-bucket-seconds", type=int, default=DEFAULT_TIME_BUCKET_SECONDS)
    parser.add_argument("--max-rows-per-symbol", type=int, default=250_000)
    parser.add_argument("--shock-limit-shards", type=int, default=128)
    parser.add_argument("--shock-max-rows-per-shard", type=int, default=250_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase73(
        args.dense_root,
        args.output_dir,
        args.base_dir,
        args.trade_month,
        args.time_bucket_seconds,
        args.max_rows_per_symbol,
        args.shock_limit_shards,
        args.shock_max_rows_per_shard,
    )


if __name__ == "__main__":
    main()
