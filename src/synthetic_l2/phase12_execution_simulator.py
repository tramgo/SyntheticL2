from __future__ import annotations

import argparse
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
        "cancel_on_stale_or_disconnect": False,
        "description": "Leakage/control profile with zero latency and half-spread marketable execution cost only. Not deployable.",
    },
    {
        "execution_profile": "retail_marketable_default",
        "decision_latency_events": 1,
        "broker_latency_events": 1,
        "fixed_slippage_ticks": 1.0,
        "impact_bps": 0.5,
        "fees_bps": 1.5,
        "cancel_on_stale_or_disconnect": True,
        "description": "Default marketable retail proxy with next-event latency, placeholder profile-level fees, and internal impact/slippage assumptions.",
    },
    {
        "execution_profile": "stressed_retail",
        "decision_latency_events": 2,
        "broker_latency_events": 2,
        "fixed_slippage_ticks": 2.0,
        "impact_bps": 2.0,
        "fees_bps": 3.0,
        "cancel_on_stale_or_disconnect": True,
        "description": "Stress proxy with longer event latency, placeholder profile-level fees, and higher internal impact/slippage assumptions.",
    },
]


COST_SCHEDULE = [
    ("profile_fee_bps", "execution_profile.fees_bps", "Placeholder profile-level fee assumption; not broker/exchange verified."),
    ("impact_bps", "execution_profile.impact_bps", "Internal market-impact proxy; not broker/exchange charge."),
    ("half_spread", "spread_ticks * tick_size / 2", "Marketable execution spread-crossing proxy."),
    ("fixed_slippage_ticks", "execution_profile.fixed_slippage_ticks * tick_size / mid_price", "Internal slippage stress parameter."),
    ("partial_fill_opportunity_cost", "not_modeled_v1", "Passive fills, queue position and partial fills are not modeled in this proxy."),
    ("statutory_and_brokerage_charges", "not_verified_v1", "Brokerage, statutory and exchange charges are placeholders only; refresh from broker/exchange sources before economic claims."),
]


def execution_profiles() -> pd.DataFrame:
    return pd.DataFrame(EXECUTION_PROFILES)


def cost_schedule() -> pd.DataFrame:
    return pd.DataFrame(
        COST_SCHEDULE,
        columns=["cost_component", "formula_or_source", "note"],
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
    trades["gross_return"] = gross_return
    trades["cost_return"] = half_spread_return + slippage_return + internal_bps_cost_return
    trades["net_return"] = trades["gross_return"] - trades["cost_return"]
    trades["notional"] = 1.0
    trades["net_pnl_units"] = trades["net_return"] * trades["notional"]

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


def run_simulation(features: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    support = _strategy_support()
    runnable = set(support[support["support_level"].isin(["runnable_proxy", "partial_missing_required_features"])]["strategy_id"])
    base = _prepare_base(features)
    signals = build_signals(base)
    summary_rows: list[dict] = []
    trade_samples: list[pd.DataFrame] = []
    sample_remaining = 250_000

    for strategy_id, signal in signals.items():
        if strategy_id not in runnable:
            continue
        for profile in EXECUTION_PROFILES:
            summary, trades = _simulate_strategy_profile(base, signal, strategy_id, profile)
            summary_rows.append(summary)
            if sample_remaining > 0 and len(trades):
                sample = trades.head(min(sample_remaining, len(trades))).copy()
                trade_samples.append(sample)
                sample_remaining -= len(sample)

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
        "- Explicit fees are placeholder profile-level bps assumptions, not verified brokerage/statutory/exchange charges.",
        "- Refresh costs from broker/exchange sources before making economic or deployability claims.",
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
        "scope": "marketable_order_proxy_over_5m_feature_events",
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
