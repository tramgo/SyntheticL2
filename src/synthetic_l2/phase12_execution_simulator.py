from __future__ import annotations

import argparse
import math
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from synthetic_l2.phase11_strategy_validation_matrix import build_signals, load_features, strategy_matrix


EXECUTION_PROFILES = [
    {
        "execution_profile": "zero_latency_spread_only_control",
        "decision_latency_events": 0,
        "broker_latency_events": 0,
        "fixed_slippage_ticks": 0.0,
        "impact_bps": 0.0,
        "fees_bps": 0.0,
        "apply_zerodha_equity_intraday_charges": False,
        "cancel_on_stale_or_disconnect": False,
        "description": "Leakage/control profile with zero latency and spread/slippage controls only. Not deployable and excludes statutory/brokerage charges.",
    },
    {
        "execution_profile": "retail_marketable_default",
        "decision_latency_events": 1,
        "broker_latency_events": 1,
        "fixed_slippage_ticks": 1.0,
        "impact_bps": 0.5,
        "fees_bps": 0.0,
        "apply_zerodha_equity_intraday_charges": True,
        "cancel_on_stale_or_disconnect": True,
        "description": "Default marketable retail proxy with next-event latency, Zerodha equity-intraday charge estimate, and internal impact/slippage assumptions.",
    },
    {
        "execution_profile": "stressed_retail",
        "decision_latency_events": 2,
        "broker_latency_events": 2,
        "fixed_slippage_ticks": 2.0,
        "impact_bps": 2.0,
        "fees_bps": 0.0,
        "apply_zerodha_equity_intraday_charges": True,
        "cancel_on_stale_or_disconnect": True,
        "description": "Stress proxy with longer event latency, Zerodha equity-intraday charge estimate, and higher internal impact/slippage assumptions.",
    },
]


ZERODHA_CHARGES_SOURCE_URL = "https://zerodha.com/charges/"
ZERODHA_CHARGES_SOURCE_NAME = "Zerodha charges page"
ZERODHA_CHARGES_ACCESS_DATE = "2026-07-14"
ZERODHA_EQUITY_INTRADAY_NSE_BPS = {
    "brokerage_round_trip_bps": 6.0,  # 0.03% per executed order * buy and sell; ₹20/order cap not modeled without rupee order notional.
    "stt_sell_side_bps": 2.5,  # 0.025% on sell side.
    "transaction_charges_round_trip_bps": 0.614,  # NSE 0.00307% per side * buy and sell.
    "sebi_charges_round_trip_bps": 0.002,  # ₹10/crore = 0.001 bps per side * buy and sell.
    "stamp_duty_buy_side_bps": 0.3,  # 0.003% buy side.
}
ZERODHA_EQUITY_INTRADAY_NSE_BPS["gst_bps"] = 0.18 * (
    ZERODHA_EQUITY_INTRADAY_NSE_BPS["brokerage_round_trip_bps"]
    + ZERODHA_EQUITY_INTRADAY_NSE_BPS["transaction_charges_round_trip_bps"]
    + ZERODHA_EQUITY_INTRADAY_NSE_BPS["sebi_charges_round_trip_bps"]
)
ZERODHA_EQUITY_INTRADAY_TOTAL_BPS = float(sum(ZERODHA_EQUITY_INTRADAY_NSE_BPS.values()))


COST_SCHEDULE = [
    ("profile_fee_bps", "execution_profile.fees_bps", 0.0, "all_profiles", "Internal residual profile fee hook; current profiles set this to zero because verified Zerodha charge rows are modeled separately.", "internal_model", ""),
    ("impact_bps", "execution_profile.impact_bps", None, "all_profiles", "Internal market-impact proxy; not broker/exchange charge.", "internal_model", ""),
    ("half_spread", "spread_ticks * tick_size / 2", None, "all_profiles", "Marketable execution spread-crossing proxy.", "internal_model", ""),
    ("fixed_slippage_ticks", "execution_profile.fixed_slippage_ticks * tick_size / mid_price", None, "all_profiles", "Internal slippage stress parameter.", "internal_model", ""),
    ("partial_fill_opportunity_cost", "phase12_order_lifecycle_proxy", None, "sampled_lifecycle_profiles", "Partial fills and queue-position buckets are modeled in outputs/phase12_order_lifecycle, not as a scalar charge in the base execution summary.", "implemented_proxy", ""),
    ("zerodha_equity_intraday_brokerage", "0.03% or Rs. 20 per executed order, lower; modeled as 0.03% per buy/sell order before cap", ZERODHA_EQUITY_INTRADAY_NSE_BPS["brokerage_round_trip_bps"], "retail_and_stressed_profiles", "Round-trip bps approximation; ₹20/order cap requires rupee order notional and is not applied in the normalized return proxy.", "verified_source_normalized_proxy", ZERODHA_CHARGES_SOURCE_URL),
    ("zerodha_equity_intraday_stt", "0.025% on sell side", ZERODHA_EQUITY_INTRADAY_NSE_BPS["stt_sell_side_bps"], "retail_and_stressed_profiles", "Equity intraday STT applied on sell side.", "verified_source_normalized_proxy", ZERODHA_CHARGES_SOURCE_URL),
    ("zerodha_equity_intraday_nse_transaction_charges", "NSE 0.00307% per side", ZERODHA_EQUITY_INTRADAY_NSE_BPS["transaction_charges_round_trip_bps"], "retail_and_stressed_profiles", "Round-trip NSE transaction-charge approximation.", "verified_source_normalized_proxy", ZERODHA_CHARGES_SOURCE_URL),
    ("zerodha_equity_intraday_sebi_charges", "Rs. 10/crore per side", ZERODHA_EQUITY_INTRADAY_NSE_BPS["sebi_charges_round_trip_bps"], "retail_and_stressed_profiles", "Round-trip SEBI charge approximation.", "verified_source_normalized_proxy", ZERODHA_CHARGES_SOURCE_URL),
    ("zerodha_equity_intraday_stamp_duty", "0.003% buy side", ZERODHA_EQUITY_INTRADAY_NSE_BPS["stamp_duty_buy_side_bps"], "retail_and_stressed_profiles", "Stamp duty applied on buy side.", "verified_source_normalized_proxy", ZERODHA_CHARGES_SOURCE_URL),
    ("zerodha_equity_intraday_gst", "18% on brokerage + SEBI charges + transaction charges", ZERODHA_EQUITY_INTRADAY_NSE_BPS["gst_bps"], "retail_and_stressed_profiles", "GST calculated from modeled brokerage, SEBI and transaction-charge bps.", "verified_source_normalized_proxy", ZERODHA_CHARGES_SOURCE_URL),
    ("statutory_and_brokerage_charges", "verified_zerodha_equity_intraday_nse_round_trip_bps_v1", ZERODHA_EQUITY_INTRADAY_TOTAL_BPS, "retail_and_stressed_profiles", "Total normalized round-trip charge estimate from Zerodha-published equity intraday rows; not acceptance-grade because order-notional cap and contract-note rounding are not modeled.", "verified_source_normalized_proxy", ZERODHA_CHARGES_SOURCE_URL),
]


def execution_profiles() -> pd.DataFrame:
    return pd.DataFrame(EXECUTION_PROFILES)


def cost_schedule() -> pd.DataFrame:
    return pd.DataFrame(
        COST_SCHEDULE,
        columns=["cost_component", "formula_or_source", "basis_points", "applies_to", "note", "evidence_status", "source_url"],
    )


def _strategy_support() -> pd.DataFrame:
    matrix = strategy_matrix()
    return matrix[["strategy_id", "name", "role", "support_level", "caveat"]]


def _prepare_base(features: pd.DataFrame) -> pd.DataFrame:
    ordered = features.sort_values(
        ["feed_profile", "trade_date", "scenario_day", "symbol", "bar_index"],
        kind="mergesort",
    ).reset_index(drop=True)
    group_cols = ["feed_profile", "trade_date", "scenario_day", "symbol"]
    grouped = ordered.groupby(group_cols, sort=False)
    ordered["next_mid_price"] = grouped["mid_price"].shift(-1)
    ordered["next_spread_ticks"] = grouped["spread_ticks"].shift(-1)
    ordered["next_is_bad_feed"] = (
        grouped["is_duplicate"].shift(-1).fillna(False).astype(bool)
        | grouped["is_disconnect_gap"].shift(-1).fillna(False).astype(bool)
        | grouped["is_out_of_order_injected"].shift(-1).fillna(False).astype(bool)
    )
    ordered["row_in_group"] = grouped.cumcount()
    return ordered


def _latency_shift(frame: pd.DataFrame, signal: pd.Series, latency_events: int) -> pd.Series:
    if latency_events <= 0:
        return signal
    group_cols = ["feed_profile", "trade_date", "scenario_day", "symbol"]
    return signal.groupby([frame[col] for col in group_cols], sort=False).shift(latency_events).fillna(0)


def _simulate_strategy_profile(
    base: pd.DataFrame,
    raw_signal: pd.Series,
    strategy_id: str,
    profile: dict,
) -> tuple[dict, pd.DataFrame]:
    total_latency = int(profile["decision_latency_events"] + profile["broker_latency_events"])
    executable_signal = _latency_shift(base, raw_signal, total_latency)
    mask = executable_signal.ne(0) & base["next_mid_price"].notna()
    if profile["cancel_on_stale_or_disconnect"]:
        mask &= ~(base["is_disconnect_gap"] | base["is_out_of_order_injected"] | base["next_is_bad_feed"])

    trades = base.loc[
        mask,
        [
            "feed_profile",
            "quarter_profile",
            "trade_date",
            "scenario_day",
            "bar_index",
            "symbol",
            "regime_code",
            "mid_price",
            "next_mid_price",
            "spread_ticks",
            "local_volatility_6",
            "event_intensity_proxy",
            "is_market_shock_day",
            "is_symbol_shock",
        ],
    ].copy()
    trades["strategy_id"] = strategy_id
    trades["execution_profile"] = profile["execution_profile"]
    trades["side"] = executable_signal.loc[mask].astype("int8").to_numpy()

    gross_return = trades["side"] * (trades["next_mid_price"] / trades["mid_price"] - 1.0)
    tick_size = np.where(trades["mid_price"] < 250, 0.01, 0.05)
    half_spread_return = ((trades["spread_ticks"].clip(lower=1) * tick_size) / 2.0) / trades["mid_price"]
    slippage_return = (float(profile["fixed_slippage_ticks"]) * tick_size) / trades["mid_price"]
    internal_bps_cost_return = (float(profile["impact_bps"]) + float(profile["fees_bps"])) / 10000.0
    zerodha_charge_bps = ZERODHA_EQUITY_INTRADAY_TOTAL_BPS if bool(profile.get("apply_zerodha_equity_intraday_charges", False)) else 0.0
    zerodha_charge_return = zerodha_charge_bps / 10000.0
    trades["gross_return"] = gross_return
    trades["cost_return"] = half_spread_return + slippage_return + internal_bps_cost_return + zerodha_charge_return
    trades["zerodha_equity_intraday_charge_bps"] = zerodha_charge_bps
    trades["net_return"] = trades["gross_return"] - trades["cost_return"]
    trades["notional"] = 1.0
    trades["net_pnl_units"] = trades["net_return"] * trades["notional"]
    trades["volatility_bucket"] = _tertile_bucket(trades["local_volatility_6"], ["low_volatility", "medium_volatility", "high_volatility"])
    liquidity_score = trades["event_intensity_proxy"].astype(float) / trades["spread_ticks"].clip(lower=1).astype(float)
    trades["liquidity_bucket"] = _tertile_bucket(liquidity_score, ["low_liquidity", "medium_liquidity", "high_liquidity"])

    summary = {
        "strategy_id": strategy_id,
        "execution_profile": profile["execution_profile"],
        "latency_events": total_latency,
        "trades": int(len(trades)),
        "symbols": int(trades["symbol"].nunique()) if len(trades) else 0,
        "feed_profiles": int(trades["feed_profile"].nunique()) if len(trades) else 0,
        "mean_gross_return": float(trades["gross_return"].mean()) if len(trades) else None,
        "mean_cost_return": float(trades["cost_return"].mean()) if len(trades) else None,
        "mean_net_return": float(trades["net_return"].mean()) if len(trades) else None,
        "win_rate_net": float((trades["net_return"] > 0).mean()) if len(trades) else None,
        "total_net_pnl_units": float(trades["net_pnl_units"].sum()) if len(trades) else 0.0,
        "market_shock_trade_fraction": float(trades["is_market_shock_day"].mean()) if len(trades) else None,
        "symbol_shock_trade_fraction": float(trades["is_symbol_shock"].mean()) if len(trades) else None,
        "status": "simulated_marketable_proxy_not_acceptance",
    }
    return summary, trades


def _tertile_bucket(values: pd.Series, labels: list[str]) -> pd.Series:
    numeric = values.astype(float).replace([np.inf, -np.inf], np.nan)
    if numeric.notna().sum() == 0 or numeric.nunique(dropna=True) <= 1:
        return pd.Series(labels[1], index=values.index, dtype="object")
    ranked = numeric.rank(method="first")
    try:
        bucket = pd.qcut(ranked, q=3, labels=labels, duplicates="drop")
        return bucket.astype("object").fillna(labels[1])
    except ValueError:
        return pd.Series(labels[1], index=values.index, dtype="object")


def _deterministic_even_sample(frame: pd.DataFrame, max_rows: int) -> pd.DataFrame:
    if len(frame) <= max_rows:
        return frame.copy()
    positions = np.linspace(0, len(frame) - 1, num=max_rows, dtype=int)
    return frame.iloc[positions].copy()


def run_simulation(features: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    support = _strategy_support()
    runnable = set(support[support["support_level"].isin(["runnable_proxy", "partial_missing_required_features"])]["strategy_id"])
    base = _prepare_base(features)
    signals = build_signals(base)
    summary_rows: list[dict] = []
    trade_samples: list[pd.DataFrame] = []
    runnable_signal_count = len([strategy_id for strategy_id in signals if strategy_id in runnable])
    sample_groups = max(1, runnable_signal_count * len(EXECUTION_PROFILES))
    per_group_sample_rows = max(1, math.floor(250_000 / sample_groups))

    for strategy_id, signal in signals.items():
        if strategy_id not in runnable:
            continue
        for profile in EXECUTION_PROFILES:
            summary, trades = _simulate_strategy_profile(base, signal, strategy_id, profile)
            summary_rows.append(summary)
            if len(trades):
                sample = _deterministic_even_sample(trades, per_group_sample_rows)
                trade_samples.append(sample)

    summary_frame = pd.DataFrame(summary_rows).merge(support, on="strategy_id", how="left")
    sample_frame = pd.concat(trade_samples, ignore_index=True) if trade_samples else pd.DataFrame()
    return summary_frame, sample_frame


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    text = frame.copy()
    for column in text.columns:
        text[column] = text[column].map(lambda value: "" if pd.isna(value) else (f"{value:.6g}" if isinstance(value, float) else str(value)))
    headers = [str(column) for column in text.columns]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in text.values.tolist())
    return "\n".join(lines)


def write_report(output_dir: Path, summary: pd.DataFrame) -> None:
    overview = summary.groupby("execution_profile", sort=True).agg(
        strategies=("strategy_id", "nunique"),
        trades=("trades", "sum"),
        mean_net_return=("mean_net_return", "mean"),
        total_net_pnl_units=("total_net_pnl_units", "sum"),
    ).reset_index()
    top_cols = ["strategy_id", "execution_profile", "trades", "mean_gross_return", "mean_cost_return", "mean_net_return", "win_rate_net", "status"]
    lines = [
        "# Phase 12 Execution Simulator Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This is the first marketable-order execution proxy over Phase 9 Tier C feature events and Phase 11 proxy signals.",
        "It applies event-latency shifts, stale/disconnect cancellation, spread/slippage/profile-fee costs and one-step mark-to-next-event P&L.",
        "It is not a tick-accurate queue simulator and must not be used for strategy acceptance.",
        "",
        "## Execution Profile Overview",
        "",
        _markdown_table(overview),
        "",
        "## Strategy/Profile Summary",
        "",
        _markdown_table(summary[top_cols].sort_values(["strategy_id", "execution_profile"])),
        "",
        "## Caveats",
        "",
        "- Current features are 5-minute synthetic feature events, not true tick-level order events.",
        "- Passive orders, partial fills, cancel/replace and order rejections are represented as requirements, not realistic queue simulation.",
        "- Zerodha equity-intraday statutory/brokerage charges are modeled as a normalized bps estimate from the published charges page.",
        "- The Rs. 20/order brokerage cap, DP charges, contract-note rounding and order-notional-specific effects are not modeled in the normalized return proxy.",
        "- Spread crossing, fixed slippage and impact remain internal execution assumptions.",
        "- Zero-latency/spread-only profile is a leakage/control profile, not a deployable model.",
        "",
    ]
    (output_dir / "phase12_execution_simulator_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase12(features_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    features = load_features(features_path)
    summary, trade_sample = run_simulation(features)
    profiles = execution_profiles()
    costs = cost_schedule()

    summary.to_csv(output_dir / "execution_summary.csv", index=False)
    profiles.to_csv(output_dir / "execution_profiles.csv", index=False)
    costs.to_csv(output_dir / "cost_schedule.csv", index=False)
    if len(trade_sample):
        pq.write_table(pa.Table.from_pandas(trade_sample, preserve_index=False), output_dir / "trade_ledger_sample.parquet", compression="zstd")
    else:
        pq.write_table(pa.Table.from_pandas(pd.DataFrame(), preserve_index=False), output_dir / "trade_ledger_sample.parquet", compression="zstd")

    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "features_path": str(features_path),
        "rows_evaluated": int(len(features)),
        "strategies_simulated": int(summary["strategy_id"].nunique()) if len(summary) else 0,
        "execution_profiles": int(len(profiles)),
        "summary_rows": int(len(summary)),
        "trade_sample_rows": int(len(trade_sample)),
        "trade_sample_strategy_profiles": int(trade_sample[["strategy_id", "execution_profile"]].drop_duplicates().shape[0]) if len(trade_sample) else 0,
        "trade_sample_policy": "deterministic_even_stratified_by_strategy_profile",
        "scope": "marketable_order_proxy_over_5m_feature_events",
        "cost_model_version": "zerodha_equity_intraday_nse_round_trip_bps_v1",
        "cost_model_source": ZERODHA_CHARGES_SOURCE_URL,
        "cost_model_source_name": ZERODHA_CHARGES_SOURCE_NAME,
        "cost_model_access_date": ZERODHA_CHARGES_ACCESS_DATE,
        "zerodha_equity_intraday_total_bps": ZERODHA_EQUITY_INTRADAY_TOTAL_BPS,
        "zerodha_equity_intraday_components_bps": ZERODHA_EQUITY_INTRADAY_NSE_BPS,
        "not_acceptance_result": True,
    }
    (output_dir / "execution_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 12 execution simulator proxy over Phase 9 Tier C features.")
    parser.add_argument("--features-path", type=Path, default=Path("outputs/phase9/tier_c/features_5m.parquet"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase12"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase12(args.features_path, args.output_dir)


if __name__ == "__main__":
    main()
