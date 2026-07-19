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
from synthetic_l2.phase56_cost_clearing_label_discovery import DEFAULT_DENSE_ROOT, DEFAULT_ORDER_NOTIONAL_INR
from synthetic_l2.phase61_lower_frequency_candidate_sweep import _safe_path, profile_cost_bps, retail_profile
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase70")
DEFAULT_TRADE_MONTH = "2026-01"
DEFAULT_BAR_EVENTS = 5_000
FEATURE_QUANTILES = [0.50, 0.70, 0.90]

BANK_SYMBOLS = {"AXISBANK", "HDFCBANK", "ICICIBANK", "KOTAKBANK", "SBIN"}
IT_SYMBOLS = {"HCLTECH", "INFY", "TCS", "TECHM", "WIPRO"}
ETF_SYMBOLS = {"BANKBEES", "GOLDBEES", "ITBEES", "JUNIORBEES", "NIFTYBEES"}
MEGA_CAP_LEADERS = {"HDFCBANK", "ICICIBANK", "INFY", "RELIANCE", "TCS"}


@dataclass(frozen=True)
class LeadLagSpec:
    group_id: str
    leader_symbol: str
    target_symbols: tuple[str, ...]
    side_mode: str
    description: str


def symbol_universe() -> list[str]:
    return [
        "ADANIPORTS",
        "AXISBANK",
        "BAJAJ-AUTO",
        "BANKBEES",
        "BHARTIARTL",
        "BPCL",
        "BRITANNIA",
        "CIPLA",
        "DRREDDY",
        "GOLDBEES",
        "HCLTECH",
        "HDFCBANK",
        "HINDUNILVR",
        "ICICIBANK",
        "INFY",
        "ITBEES",
        "ITC",
        "JUNIORBEES",
        "KOTAKBANK",
        "LT",
        "M&M",
        "MARUTI",
        "NESTLEIND",
        "NIFTYBEES",
        "ONGC",
        "RELIANCE",
        "SBIN",
        "SUNPHARMA",
        "TCS",
        "TECHM",
        "ULTRACEMCO",
        "WIPRO",
    ]


def lead_lag_specs() -> list[LeadLagSpec]:
    all_symbols = tuple(symbol_universe())
    bank_targets = tuple(sorted(BANK_SYMBOLS))
    it_targets = tuple(sorted(IT_SYMBOLS))
    equity_targets = tuple(symbol for symbol in all_symbols if symbol not in ETF_SYMBOLS)
    specs = [
        LeadLagSpec("ETF_NIFTY_MOMENTUM", "NIFTYBEES", equity_targets, "sign", "NIFTYBEES return leads broad equities."),
        LeadLagSpec("ETF_NIFTY_FADE", "NIFTYBEES", equity_targets, "opposite", "Fade NIFTYBEES return against broad equities."),
        LeadLagSpec("ETF_BANK_MOMENTUM", "BANKBEES", bank_targets, "sign", "BANKBEES return leads banks."),
        LeadLagSpec("ETF_BANK_FADE", "BANKBEES", bank_targets, "opposite", "Fade BANKBEES return against banks."),
        LeadLagSpec("ETF_IT_MOMENTUM", "ITBEES", it_targets, "sign", "ITBEES return leads IT large caps."),
        LeadLagSpec("ETF_IT_FADE", "ITBEES", it_targets, "opposite", "Fade ITBEES return against IT large caps."),
    ]
    for leader in sorted(MEGA_CAP_LEADERS):
        targets = tuple(symbol for symbol in equity_targets if symbol != leader)
        specs.append(LeadLagSpec(f"MEGA_{leader}_MOMENTUM", leader, targets, "sign", f"{leader} return leads other equities."))
        specs.append(LeadLagSpec(f"MEGA_{leader}_FADE", leader, targets, "opposite", f"Fade {leader} return against other equities."))
    return specs


def monthly_files(dense_root: Path, trade_month: str, limit_symbols: int | None) -> list[Path]:
    files = sorted((dense_root / f"trade_month={trade_month}").glob("symbol=*/part-00000.parquet"))
    if not files:
        raise FileNotFoundError(f"No dense parquet files for trade_month={trade_month} under {dense_root}")
    return files[:limit_symbols] if limit_symbols is not None else files


def query_symbol_bars(path: Path, bar_events: int, max_rows_per_symbol: int | None) -> pd.DataFrame:
    filter_sql = """
        buy_1_price > 0
        and sell_1_price > 0
        and sell_1_price >= buy_1_price
        and not coalesce(is_duplicate, false)
        and not coalesce(is_disconnect_gap, false)
        and not coalesce(is_out_of_order_injected, false)
    """
    if max_rows_per_symbol is not None:
        filter_sql += f" and local_sequence_id <= {int(max_rows_per_symbol)}"
    con = duckdb.connect()
    try:
        sql = f"""
        with base as (
            select
                trade_date,
                symbol,
                floor((local_sequence_id - 1) / {int(bar_events)})::integer as bar_id,
                local_sequence_id,
                ((buy_1_price + sell_1_price) / 2.0)::double as mid_price,
                greatest(sell_1_price - buy_1_price, 0.01)::double as spread,
                greatest(sell_1_price - buy_1_price, 0.01)::double as tick_size_proxy,
                ((buy_1_quantity - sell_1_quantity) / nullif((buy_1_quantity + sell_1_quantity), 0.0))::double as l1_imbalance
            from read_parquet('{_safe_path(path)}', union_by_name=true)
            where {filter_sql}
        ),
        bars as (
            select
                trade_date,
                symbol,
                {int(bar_events)}::integer as bar_events,
                bar_id,
                count(*)::bigint as rows_in_bar,
                first(mid_price order by local_sequence_id)::double as open_mid_price,
                last(mid_price order by local_sequence_id)::double as close_mid_price,
                avg(spread)::double as avg_spread,
                avg(tick_size_proxy)::double as avg_tick_size_proxy,
                avg(l1_imbalance)::double as avg_l1_imbalance
            from base
            group by trade_date, symbol, bar_id
            having count(*) >= greatest(10, {int(bar_events)} * 0.50)
        )
        select
            *,
            close_mid_price / nullif(open_mid_price, 0.0) - 1.0 as bar_return,
            lead(close_mid_price) over (order by bar_id) / nullif(close_mid_price, 0.0) - 1.0 as next_bar_return
        from bars
        """
        return con.execute(sql).fetchdf()
    finally:
        con.close()


def load_monthly_bars(dense_root: Path, trade_month: str, bar_events: int, max_rows_per_symbol: int | None, limit_symbols: int | None) -> tuple[pd.DataFrame, pd.DataFrame]:
    files = monthly_files(dense_root, trade_month, limit_symbols)
    frames = [query_symbol_bars(path, bar_events, max_rows_per_symbol) for path in files]
    inventory = pd.DataFrame([{"symbol": path.parent.name.replace("symbol=", ""), "shard_path": str(path)} for path in files])
    bars = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    return bars, inventory


def build_pair_rows(bars: pd.DataFrame) -> pd.DataFrame:
    if bars.empty:
        return pd.DataFrame()
    profile = retail_profile()
    slippage_ticks = float(profile["fixed_slippage_ticks"])
    impact_bps = float(profile["impact_bps"]) + float(profile.get("fees_bps", 0.0))
    zerodha_bps = profile_cost_bps(profile)
    rows: list[pd.DataFrame] = []
    specs = lead_lag_specs()
    for spec in specs:
        leader = bars[bars["symbol"].eq(spec.leader_symbol)][["trade_date", "bar_id", "bar_return"]].rename(
            columns={"bar_return": "leader_bar_return"}
        )
        if leader.empty:
            continue
        targets = bars[bars["symbol"].isin(spec.target_symbols)].copy()
        targets = targets[targets["symbol"].ne(spec.leader_symbol)].copy()
        if targets.empty:
            continue
        merged = targets.merge(leader, on=["trade_date", "bar_id"], how="inner")
        if merged.empty:
            continue
        merged["group_id"] = spec.group_id
        merged["leader_symbol"] = spec.leader_symbol
        merged["target_symbol"] = merged["symbol"]
        merged["side_mode"] = spec.side_mode
        side = np.sign(merged["leader_bar_return"].astype(float))
        if spec.side_mode == "opposite":
            side = -side
        merged["side"] = side
        merged = merged[merged["side"].ne(0) & merged["next_bar_return"].notna()].copy()
        if merged.empty:
            continue
        merged["gross_return"] = merged["side"].astype(float) * merged["next_bar_return"].astype(float)
        merged["cost_return"] = (
            ((merged["avg_spread"].astype(float) / 2.0) / merged["close_mid_price"].astype(float))
            + (slippage_ticks * merged["avg_tick_size_proxy"].astype(float) / merged["close_mid_price"].astype(float))
            + (impact_bps / 10000.0)
            + (zerodha_bps / 10000.0)
        )
        merged["net_return"] = merged["gross_return"] - merged["cost_return"]
        rows.append(
            merged[
                [
                    "trade_date",
                    "bar_events",
                    "bar_id",
                    "group_id",
                    "leader_symbol",
                    "target_symbol",
                    "side_mode",
                    "side",
                    "leader_bar_return",
                    "next_bar_return",
                    "gross_return",
                    "cost_return",
                    "net_return",
                    "avg_spread",
                    "avg_tick_size_proxy",
                    "avg_l1_imbalance",
                    "close_mid_price",
                ]
            ]
        )
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def build_thresholds(pair_rows: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if pair_rows.empty:
        return pd.DataFrame()
    for group_id, subset in pair_rows.groupby("group_id", sort=True):
        values = subset["leader_bar_return"].astype(float).abs().replace([np.inf, -np.inf], np.nan).dropna()
        if values.empty:
            continue
        for quantile in FEATURE_QUANTILES:
            rows.append({"group_id": group_id, "feature_quantile": quantile, "abs_leader_return_threshold": float(values.quantile(quantile))})
    return pd.DataFrame(rows)


def evaluate_thresholds(pair_rows: pd.DataFrame, thresholds: pd.DataFrame) -> pd.DataFrame:
    if pair_rows.empty or thresholds.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for _, threshold in thresholds.iterrows():
        group_id = str(threshold["group_id"])
        abs_threshold = float(threshold["abs_leader_return_threshold"])
        subset = pair_rows[
            pair_rows["group_id"].eq(group_id)
            & pair_rows["leader_bar_return"].astype(float).abs().ge(abs_threshold)
        ].copy()
        if subset.empty:
            continue
        target_net = subset.groupby("target_symbol", sort=True)["net_return"].sum()
        date_net = subset.groupby("trade_date", sort=True)["net_return"].sum()
        trades = int(len(subset))
        rows.append(
            {
                "rule_id": f"P70_{group_id}_Q{int(float(threshold['feature_quantile']) * 100):02d}",
                "group_id": group_id,
                "leader_symbol": str(subset["leader_symbol"].iloc[0]),
                "side_mode": str(subset["side_mode"].iloc[0]),
                "feature_quantile": float(threshold["feature_quantile"]),
                "abs_leader_return_threshold": abs_threshold,
                "trades": trades,
                "target_symbols": int(subset["target_symbol"].nunique()),
                "trade_dates": int(subset["trade_date"].nunique()),
                "net_pnl_inr": float(subset["net_return"].sum() * DEFAULT_ORDER_NOTIONAL_INR),
                "gross_pnl_proxy_inr": float(subset["gross_return"].sum() * DEFAULT_ORDER_NOTIONAL_INR),
                "cost_pnl_drag_proxy_inr": float(subset["cost_return"].sum() * DEFAULT_ORDER_NOTIONAL_INR),
                "mean_net_bps": float(subset["net_return"].mean() * 10000.0),
                "precision_cost_clear": float((subset["gross_return"] > subset["cost_return"]).mean()),
                "positive_target_fraction": float((target_net > 0).mean()) if int(target_net.shape[0]) else 0.0,
                "positive_date_fraction": float((date_net > 0).mean()) if int(date_net.shape[0]) else 0.0,
                "cost_drag_to_abs_gross_ratio": float(subset["cost_return"].sum() / abs(subset["gross_return"].sum()))
                if float(abs(subset["gross_return"].sum())) > 0
                else np.nan,
            }
        )
    results = pd.DataFrame(rows)
    if results.empty:
        return results
    results["label_candidate"] = (
        (results["trades"] >= 100)
        & (results["target_symbols"] >= 2)
        & (results["net_pnl_inr"] > 0)
        & (results["precision_cost_clear"] >= 0.55)
        & (results["positive_target_fraction"] >= 0.50)
        & (results["cost_drag_to_abs_gross_ratio"] <= 0.50)
    )
    return results.sort_values(
        ["label_candidate", "net_pnl_inr", "precision_cost_clear", "trades"],
        ascending=[False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def summarize(results: pd.DataFrame, pair_rows: pd.DataFrame, bars: pd.DataFrame, inventory: pd.DataFrame, elapsed_seconds: float) -> pd.DataFrame:
    candidate_rows = int(results["label_candidate"].sum()) if not results.empty else 0
    best_net = float(results["net_pnl_inr"].max()) if not results.empty else 0.0
    best_precision = float(results["precision_cost_clear"].max()) if not results.empty else 0.0
    return pd.DataFrame(
        [
            ("phase70_trade_month", DEFAULT_TRADE_MONTH, "Dense trade-month partition scanned"),
            ("phase70_symbols_loaded", int(inventory["symbol"].nunique()) if not inventory.empty else 0, "Symbols loaded into event-bar matrix"),
            ("phase70_bar_rows", int(len(bars)), "Symbol event-bar rows"),
            ("phase70_pair_rows", int(len(pair_rows)), "Leader-target pair rows before thresholding"),
            ("phase70_rule_rows", int(len(results)), "Lead-lag threshold rules evaluated"),
            ("phase70_label_candidate_rows", candidate_rows, "Rules passing cross-symbol lead-lag gate"),
            ("phase70_best_net_pnl_inr", best_net, "Best after-cost rule P&L"),
            ("phase70_best_precision_cost_clear", best_precision, "Best cost-clearing precision"),
            ("phase70_survives_cross_symbol_gate", int(candidate_rows > 0), "1 means a lead-lag rule deserves disjoint-month replay"),
            ("phase70_elapsed_seconds", elapsed_seconds, "Elapsed seconds"),
            ("phase70_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha retail intraday cost model"),
            (
                "phase70_recommend_next_action",
                "disjoint_month_lead_lag_replay" if candidate_rows else "advance_to_shock_resilience_feature_family",
                "Recommended next action",
            ),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase70 Cross-Symbol Lead-Lag Labels",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase70 tests whether ETF and mega-cap event-bar returns lead related target symbols at the next event bar.",
        "This is the first cross-symbol feature-family scan after the single-symbol families failed their bounded gates.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase70_cross_symbol_lead_lag_labels_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase70(
    dense_root: Path,
    output_dir: Path,
    base_dir: Path,
    trade_month: str,
    bar_events: int,
    max_rows_per_symbol: int | None,
    limit_symbols: int | None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    bars, inventory = load_monthly_bars(dense_root, trade_month, bar_events, max_rows_per_symbol, limit_symbols)
    pair_rows = build_pair_rows(bars)
    thresholds = build_thresholds(pair_rows)
    results = evaluate_thresholds(pair_rows, thresholds)
    elapsed = time.perf_counter() - started
    acceptance = summarize(results, pair_rows, bars, inventory, elapsed)
    specs = pd.DataFrame([spec.__dict__ for spec in lead_lag_specs()])

    inventory.to_csv(output_dir / "lead_lag_file_inventory.csv", index=False)
    specs.to_csv(output_dir / "lead_lag_spec_catalog.csv", index=False)
    bars.to_csv(output_dir / "lead_lag_bar_matrix.csv", index=False)
    thresholds.to_csv(output_dir / "lead_lag_thresholds.csv", index=False)
    results.to_csv(output_dir / "lead_lag_rule_results.csv", index=False)
    acceptance.to_csv(output_dir / "lead_lag_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Top Rule Results": results.head(30),
            "Lead-Lag Spec Catalog": specs,
            "Thresholds": thresholds,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase70_cross_symbol_lead_lag_labels",
        "trade_month": trade_month,
        "survives_cross_symbol_gate": int(acceptance.loc[acceptance["metric"].eq("phase70_survives_cross_symbol_gate"), "value"].iloc[0]),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase70",
            generated_utc=generated_utc,
            inputs={
                "phase51_dense_lake": str(dense_root),
                "phase67_feature_design_queue": "outputs/phase67/feature_design_queue.csv",
                "phase69_acceptance": "outputs/phase69/spread_transition_acceptance_summary.csv",
            },
            parameters={
                "trade_month": trade_month,
                "bar_events": bar_events,
                "max_rows_per_symbol": max_rows_per_symbol if max_rows_per_symbol is not None else "none_full_symbol_scan",
                "limit_symbols": limit_symbols if limit_symbols is not None else "all_symbols_in_month",
                "feature_quantiles": FEATURE_QUANTILES,
                "label_gate": "trades_ge_100_and_targets_ge_2_and_net_pnl_gt_0_and_precision_ge_0_55_and_positive_target_fraction_ge_0_50_and_cost_drag_le_0_50_abs_gross",
            },
            outputs={
                "file_inventory": str(output_dir / "lead_lag_file_inventory.csv"),
                "spec_catalog": str(output_dir / "lead_lag_spec_catalog.csv"),
                "bar_matrix": str(output_dir / "lead_lag_bar_matrix.csv"),
                "thresholds": str(output_dir / "lead_lag_thresholds.csv"),
                "rule_results": str(output_dir / "lead_lag_rule_results.csv"),
                "acceptance_summary": str(output_dir / "lead_lag_acceptance_summary.csv"),
                "report": str(output_dir / "phase70_cross_symbol_lead_lag_labels_report.md"),
                "manifest": str(output_dir / "phase70_cross_symbol_lead_lag_labels_manifest.json"),
            },
            random_seed="none_deterministic_cross_symbol_label_scan",
            scenario_ids="phase70_one_month_cross_symbol_event_bar_labels",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase70_event_bar_leader_t_to_target_t_plus_1",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase70_cross_symbol_lead_lag_labels_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate cross-symbol lead-lag event-bar labels.")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--trade-month", type=str, default=DEFAULT_TRADE_MONTH)
    parser.add_argument("--bar-events", type=int, default=DEFAULT_BAR_EVENTS)
    parser.add_argument("--max-rows-per-symbol", type=int, default=250_000)
    parser.add_argument("--limit-symbols", type=int, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase70(
        args.dense_root,
        args.output_dir,
        args.base_dir,
        args.trade_month,
        args.bar_events,
        args.max_rows_per_symbol,
        args.limit_symbols,
    )


if __name__ == "__main__":
    main()
