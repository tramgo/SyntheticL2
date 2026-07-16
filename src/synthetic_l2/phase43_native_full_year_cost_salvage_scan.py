from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.phase12_execution_simulator import EXECUTION_PROFILES, _zerodha_order_formula_charges
from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


STRATEGY_IDS = ["S01", "S02", "S05", "S07", "S09"]
THRESHOLD_QUANTILES = [0.90, 0.95, 0.98]
SPREAD_QUANTILES = [0.25, 0.50]
LIQUIDITY_QUANTILES = [0.50, 0.75]
MIN_TRADES_FOR_CANDIDATE = 500


def load_events(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    columns = [
        "annual_event_id",
        "feed_profile",
        "synthetic_year_day",
        "synthetic_trade_date",
        "symbol",
        "regime_code",
        "mid_price",
        "next_mid_price",
        "tick_size",
        "spread_ticks",
        "event_intensity_proxy",
        "is_market_shock_day",
        "is_duplicate",
        "is_disconnect_gap",
        "is_out_of_order_injected",
        "l1_imbalance",
        "l5_imbalance",
        "momentum_3_event",
        "mlofi_qty_event",
        "microprice_dev",
        "next_is_bad_feed",
    ]
    return pq.read_table(path, columns=columns).to_pandas()


def build_variant_catalog(events: pd.DataFrame) -> pd.DataFrame:
    rows = []
    spread_thresholds = {q: float(events["spread_ticks"].quantile(q)) for q in SPREAD_QUANTILES}
    liquidity_thresholds = {q: float(events["event_intensity_proxy"].quantile(q)) for q in LIQUIDITY_QUANTILES}
    for strategy_id in STRATEGY_IDS:
        feature_column = {
            "S01": "momentum_3_event",
            "S02": "mlofi_qty_event",
            "S05": "microprice_dev",
            "S07": "l5_imbalance",
            "S09": "l1_imbalance",
        }[strategy_id]
        abs_values = events[feature_column].astype(float).abs().replace([np.inf, -np.inf], np.nan).dropna()
        for threshold_q in THRESHOLD_QUANTILES:
            threshold_value = float(abs_values.quantile(threshold_q)) if len(abs_values) else 0.0
            for spread_q, spread_limit in spread_thresholds.items():
                for liquidity_q, liquidity_floor in liquidity_thresholds.items():
                    rows.append(
                        {
                            "variant_id": f"{strategy_id}_q{int(threshold_q * 100)}_sp{int(spread_q * 100)}_liq{int(liquidity_q * 100)}",
                            "strategy_id": strategy_id,
                            "feature_column": feature_column,
                            "threshold_quantile": threshold_q,
                            "threshold_value": threshold_value,
                            "spread_quantile": spread_q,
                            "spread_tick_limit": spread_limit,
                            "liquidity_quantile": liquidity_q,
                            "liquidity_floor": liquidity_floor,
                            "variant_scope": "native_full_year_cost_salvage_not_acceptance",
                        }
                    )
    return pd.DataFrame(rows)


def variant_signal(events: pd.DataFrame, variant: dict[str, object]) -> pd.Series:
    strategy_id = str(variant["strategy_id"])
    nontrend = ~events["regime_code"].astype(str).isin(["D03", "D04", "D05", "D06"])
    if strategy_id == "S01":
        raw = np.sign(events["momentum_3_event"]).where(
            (events["momentum_3_event"].abs() >= float(variant["threshold_value"]))
            & (np.sign(events["momentum_3_event"]) == np.sign(events["mlofi_qty_event"])),
            0,
        )
    elif strategy_id == "S02":
        raw = np.sign(events["mlofi_qty_event"]).where(events["mlofi_qty_event"].abs() >= float(variant["threshold_value"]), 0)
    elif strategy_id == "S05":
        raw = np.sign(events["microprice_dev"]).where(events["microprice_dev"].abs() >= float(variant["threshold_value"]), 0)
    elif strategy_id == "S07":
        raw = -np.sign(events["l5_imbalance"]).where(nontrend & (events["l5_imbalance"].abs() >= float(variant["threshold_value"])), 0)
    elif strategy_id == "S09":
        raw = np.sign(events["l1_imbalance"]).where(events["l1_imbalance"].abs() >= float(variant["threshold_value"]), 0)
    else:
        raw = pd.Series(0, index=events.index)
    tradable = events["next_mid_price"].notna()
    tradable &= events["spread_ticks"].astype(float) <= float(variant["spread_tick_limit"])
    tradable &= events["event_intensity_proxy"].astype(float) >= float(variant["liquidity_floor"])
    tradable &= ~events["is_duplicate"].astype(bool)
    tradable &= ~events["is_disconnect_gap"].astype(bool)
    tradable &= ~events["is_out_of_order_injected"].astype(bool)
    return pd.Series(raw, index=events.index).where(tradable, 0).fillna(0).astype("int8")


def latency_shift(events: pd.DataFrame, signal: pd.Series, latency_events: int) -> pd.Series:
    if latency_events <= 0:
        return signal
    return signal.groupby(
        [events["feed_profile"], events["synthetic_year_day"], events["symbol"]],
        sort=False,
    ).shift(latency_events).fillna(0).astype("int8")


def simulate_variant(events: pd.DataFrame, signal: pd.Series, variant: dict[str, object], profile: dict[str, object]) -> dict[str, object]:
    total_latency = int(profile["decision_latency_events"] + profile["broker_latency_events"])
    executable = latency_shift(events, signal, total_latency)
    mask = executable.ne(0) & events["next_mid_price"].notna()
    if bool(profile.get("cancel_on_stale_or_disconnect", False)):
        mask &= ~(
            events["is_disconnect_gap"].astype(bool)
            | events["is_out_of_order_injected"].astype(bool)
            | events["next_is_bad_feed"].astype(bool)
        )
    if not bool(mask.any()):
        return {
            "variant_id": variant["variant_id"],
            "strategy_id": variant["strategy_id"],
            "execution_profile": profile["execution_profile"],
            "trades": 0,
            "annual_net_pnl_inr": 0.0,
            "mean_gross_return": 0.0,
            "mean_cost_return": 0.0,
            "mean_zerodha_charge_return": 0.0,
            "mean_net_return": 0.0,
            "worst_daily_net_pnl_inr": 0.0,
            "max_drawdown_inr": 0.0,
            "positive_day_fraction": 0.0,
            "annualized_sharpe_proxy": 0.0,
        }
    trades = events.loc[
        mask,
        [
            "synthetic_year_day",
            "symbol",
            "mid_price",
            "next_mid_price",
            "spread_ticks",
            "tick_size",
        ],
    ].copy()
    trades["side"] = executable.loc[mask].astype("int8").to_numpy()
    gross_return = trades["side"] * (trades["next_mid_price"] / trades["mid_price"] - 1.0)
    spread_cost = ((trades["spread_ticks"].clip(lower=1) * trades["tick_size"]) / 2.0) / trades["mid_price"]
    slippage_cost = (float(profile["fixed_slippage_ticks"]) * trades["tick_size"]) / trades["mid_price"]
    internal_bps_cost = (float(profile["impact_bps"]) + float(profile["fees_bps"])) / 10_000.0
    charges = _zerodha_order_formula_charges(
        trades,
        order_notional_inr=float(profile.get("order_notional_inr", 100_000.0)),
        apply_charges=bool(profile.get("apply_zerodha_equity_intraday_charges", False)),
    )
    trades["gross_return"] = gross_return
    trades["cost_return"] = spread_cost + slippage_cost + internal_bps_cost + charges["zerodha_charge_return"]
    trades["zerodha_charge_return"] = charges["zerodha_charge_return"]
    trades["net_return"] = trades["gross_return"] - trades["cost_return"]
    trades["net_pnl_inr"] = trades["gross_return"] * charges["entry_notional_inr"] - (
        spread_cost + slippage_cost + internal_bps_cost
    ) * charges["entry_notional_inr"] - charges["zerodha_total_charges_inr"]
    daily = trades.groupby("synthetic_year_day", sort=True).agg(daily_net_pnl_inr=("net_pnl_inr", "sum")).reset_index()
    daily["running_net_pnl_inr"] = daily["daily_net_pnl_inr"].cumsum()
    daily["running_peak_inr"] = daily["running_net_pnl_inr"].cummax()
    daily["drawdown_inr"] = daily["running_net_pnl_inr"] - daily["running_peak_inr"]
    daily_std = float(daily["daily_net_pnl_inr"].std(ddof=1))
    daily_mean = float(daily["daily_net_pnl_inr"].mean())
    sharpe = float((daily_mean / daily_std) * np.sqrt(252)) if daily_std > 0 else 0.0
    return {
        "variant_id": variant["variant_id"],
        "strategy_id": variant["strategy_id"],
        "execution_profile": profile["execution_profile"],
        "threshold_quantile": float(variant["threshold_quantile"]),
        "spread_quantile": float(variant["spread_quantile"]),
        "liquidity_quantile": float(variant["liquidity_quantile"]),
        "trades": int(len(trades)),
        "annual_net_pnl_inr": float(trades["net_pnl_inr"].sum()),
        "mean_gross_return": float(trades["gross_return"].mean()),
        "mean_cost_return": float(trades["cost_return"].mean()),
        "mean_zerodha_charge_return": float(trades["zerodha_charge_return"].mean()),
        "mean_net_return": float(trades["net_return"].mean()),
        "worst_daily_net_pnl_inr": float(daily["daily_net_pnl_inr"].min()),
        "max_drawdown_inr": float(daily["drawdown_inr"].min()),
        "positive_day_fraction": float((daily["daily_net_pnl_inr"] > 0).mean()),
        "annualized_sharpe_proxy": sharpe,
    }


def run_scan(events: pd.DataFrame, catalog: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for variant in catalog.to_dict("records"):
        signal = variant_signal(events, variant)
        for profile in EXECUTION_PROFILES:
            rows.append(simulate_variant(events, signal, variant, profile))
    result = pd.DataFrame(rows)
    result["realistic_profile"] = result["execution_profile"].astype(str).isin(["retail_marketable_default", "stressed_retail"])
    result["positive_after_costs"] = result["annual_net_pnl_inr"] > 0.0
    result["enough_trades"] = result["trades"] >= MIN_TRADES_FOR_CANDIDATE
    result["candidate_for_deeper_synthetic_replay"] = (
        result["realistic_profile"]
        & result["positive_after_costs"]
        & result["enough_trades"]
    )
    return result.sort_values(
        ["candidate_for_deeper_synthetic_replay", "annual_net_pnl_inr", "annualized_sharpe_proxy"],
        ascending=[False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_strategy_rollup(results: pd.DataFrame) -> pd.DataFrame:
    grouped = results.groupby(["strategy_id", "execution_profile"], sort=True)
    return grouped.agg(
        variants=("variant_id", "nunique"),
        positive_rows=("positive_after_costs", "sum"),
        candidate_rows=("candidate_for_deeper_synthetic_replay", "sum"),
        best_annual_net_pnl_inr=("annual_net_pnl_inr", "max"),
        best_mean_net_return=("mean_net_return", "max"),
        min_trades=("trades", "min"),
        max_trades=("trades", "max"),
        best_positive_day_fraction=("positive_day_fraction", "max"),
    ).reset_index().sort_values(["candidate_rows", "best_annual_net_pnl_inr"], ascending=[False, False], kind="mergesort")


def build_summary(events: pd.DataFrame, catalog: pd.DataFrame, results: pd.DataFrame) -> pd.DataFrame:
    realistic = results[results["realistic_profile"]]
    rows = [
        ("phase43_input_event_rows", int(len(events)), "Native full-year L2 event rows scanned"),
        ("phase43_variants_registered", int(len(catalog)), "Cost-aware strategy variants registered"),
        ("phase43_variant_profile_rows", int(len(results)), "Variant/profile rows evaluated"),
        ("phase43_total_variant_trades", int(results["trades"].sum()), "Total simulated trades across variant/profile rows"),
        ("phase43_positive_variant_profile_rows", int(results["positive_after_costs"].sum()), "Annual positive P&L variant/profile rows"),
        ("phase43_positive_realistic_variant_profile_rows", int((realistic["annual_net_pnl_inr"] > 0).sum()), "Annual positive P&L retail/stressed rows"),
        ("phase43_deeper_synthetic_candidate_rows", int(results["candidate_for_deeper_synthetic_replay"].sum()), "Realistic positive rows with enough trades"),
        ("phase43_best_annual_net_pnl_inr", float(results["annual_net_pnl_inr"].max()) if len(results) else 0.0, "Best annual net P&L across all variant profiles"),
        ("phase43_best_realistic_annual_net_pnl_inr", float(realistic["annual_net_pnl_inr"].max()) if len(realistic) else 0.0, "Best annual net P&L across retail/stressed variant profiles"),
        ("phase43_synthetic_full_year_acceptance_ready", 0, "Cost-aware salvage scan is experiment evidence, not acceptance"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase 43 Native Full-Year Cost-Aware Salvage Scan",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This phase scans sparse, high-confidence strategy variants over the native 252-day synthetic L2 event stream.",
        "It tests whether threshold, spread and liquidity filters can rescue full-year economics under Zerodha-style costs. It is not acceptance evidence.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase43_native_full_year_cost_salvage_scan_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase43(events_path: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    events = load_events(events_path)
    catalog = build_variant_catalog(events)
    results = run_scan(events, catalog)
    rollup = build_strategy_rollup(results)
    summary = build_summary(events, catalog, results)
    catalog.to_csv(output_dir / "cost_salvage_variant_catalog.csv", index=False)
    results.to_csv(output_dir / "cost_salvage_variant_results.csv", index=False)
    rollup.to_csv(output_dir / "cost_salvage_strategy_rollup.csv", index=False)
    summary.to_csv(output_dir / "cost_salvage_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Summary": summary,
            "Top Variant Results": results.head(60),
            "Top Realistic Variant Results": results[results["realistic_profile"]].head(60),
            "Strategy Rollup": rollup,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase43_native_full_year_cost_salvage_scan_not_acceptance",
        "variants_registered": int(len(catalog)),
        "variant_profile_rows": int(len(results)),
        "synthetic_full_year_acceptance_ready": 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase43",
            generated_utc=generated_utc,
            inputs={"native_full_year_l2_event_state": str(events_path)},
            parameters={
                "strategy_ids": STRATEGY_IDS,
                "threshold_quantiles": THRESHOLD_QUANTILES,
                "spread_quantiles": SPREAD_QUANTILES,
                "liquidity_quantiles": LIQUIDITY_QUANTILES,
                "minimum_trades_for_candidate": MIN_TRADES_FOR_CANDIDATE,
                "acceptance_boundary": "synthetic_only_experiment_not_acceptance",
            },
            outputs={
                "summary": str(output_dir / "cost_salvage_summary.csv"),
                "variant_catalog": str(output_dir / "cost_salvage_variant_catalog.csv"),
                "variant_results": str(output_dir / "cost_salvage_variant_results.csv"),
                "strategy_rollup": str(output_dir / "cost_salvage_strategy_rollup.csv"),
                "report": str(output_dir / "phase43_native_full_year_cost_salvage_scan_report.md"),
                "manifest": str(output_dir / "phase43_native_full_year_cost_salvage_scan_manifest.json"),
            },
            random_seed="none_deterministic_native_full_year_variant_scan",
            scenario_ids="phase42_native_252_day_l2_event_state_cost_salvage",
            cost_model_version="phase12_zerodha_equity_intraday_cost_model",
            latency_model_version="phase12_execution_profiles",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase43_native_full_year_cost_salvage_scan_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run native full-year cost-aware salvage scan.")
    parser.add_argument("--events", type=Path, default=Path("outputs/phase42/native_full_year_l2_event_state.parquet"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase43"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase43(args.events, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
