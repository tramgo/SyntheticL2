from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from synthetic_l2.phase12_execution_simulator import EXECUTION_PROFILES, _zerodha_order_formula_charges
from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


TRADING_DAYS_PER_YEAR = 252
STRATEGY_IDS = ["S01", "S02", "S05", "S07", "S09"]
SAMPLE_TRADES_PER_PROFILE = 2_000


def load_compact_l2(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    columns = [
        "feed_profile",
        "quarter_profile",
        "scenario_day",
        "trade_date",
        "symbol",
        "receive_sequence",
        "collector_received_utc_ms",
        "source_sequence",
        "regime_code",
        "regime_family",
        "mid_price",
        "tick_size",
        "spread_ticks",
        "spread",
        "event_intensity_proxy",
        "is_market_shock_day",
        "is_symbol_shock",
        "is_duplicate",
        "is_disconnect_gap",
        "is_out_of_order_injected",
        "l1_imbalance",
        "l5_imbalance",
        "microprice_l1",
    ]
    return pq.read_table(path, columns=columns).to_pandas()


def build_annual_l2(compact: pd.DataFrame) -> pd.DataFrame:
    day_keys = (
        compact[["quarter_profile", "scenario_day", "trade_date"]]
        .drop_duplicates()
        .sort_values(["quarter_profile", "scenario_day", "trade_date"], kind="mergesort")
        .reset_index(drop=True)
    )
    schedule_rows = []
    dates = pd.bdate_range("2026-01-01", periods=TRADING_DAYS_PER_YEAR)
    for day_index in range(TRADING_DAYS_PER_YEAR):
        source = day_keys.iloc[day_index % len(day_keys)]
        schedule_rows.append(
            {
                "quarter_profile": source["quarter_profile"],
                "scenario_day": int(source["scenario_day"]),
                "trade_date": source["trade_date"],
                "synthetic_year_day": day_index + 1,
                "synthetic_trade_date": dates[day_index].date().isoformat(),
                "source_cycle_ordinal": day_index // len(day_keys),
            }
        )
    schedule = pd.DataFrame(schedule_rows)
    annual = compact.merge(schedule, on=["quarter_profile", "scenario_day", "trade_date"], how="inner", validate="many_to_many")
    annual = annual.rename(columns={"trade_date": "source_trade_date", "quarter_profile": "source_quarter_profile", "scenario_day": "source_scenario_day"})
    annual["annual_quarter_profile"] = pd.cut(
        annual["synthetic_year_day"],
        bins=[0, 63, 126, 189, 252],
        labels=["Y-Q1", "Y-Q2", "Y-Q3", "Y-Q4"],
        include_lowest=True,
    ).astype(str)
    annual = annual.sort_values(
        ["feed_profile", "synthetic_year_day", "symbol", "receive_sequence"],
        kind="mergesort",
    ).reset_index(drop=True)
    annual["annual_event_id"] = np.arange(1, len(annual) + 1, dtype=np.int64)
    group_cols = ["feed_profile", "synthetic_year_day", "symbol"]
    grouped = annual.groupby(group_cols, sort=False)
    annual["next_mid_price"] = grouped["mid_price"].shift(-1)
    annual["mid_return_event"] = annual["mid_price"] / grouped["mid_price"].shift(1) - 1.0
    annual["momentum_3_event"] = grouped["mid_return_event"].transform(lambda values: values.rolling(3, min_periods=1).sum()).fillna(0.0)
    annual["local_volatility_6_event"] = grouped["mid_return_event"].transform(lambda values: values.rolling(6, min_periods=2).std()).fillna(0.0)
    annual["mlofi_qty_event"] = grouped["l5_imbalance"].diff().fillna(0.0) * annual["event_intensity_proxy"].fillna(0.0)
    annual["microprice_dev"] = (annual["microprice_l1"] - annual["mid_price"]) / annual["mid_price"].replace(0.0, np.nan)
    annual["next_is_bad_feed"] = (
        grouped["is_duplicate"].shift(-1).fillna(False).astype(bool)
        | grouped["is_disconnect_gap"].shift(-1).fillna(False).astype(bool)
        | grouped["is_out_of_order_injected"].shift(-1).fillna(False).astype(bool)
    )
    return annual


def build_signal(events: pd.DataFrame, strategy_id: str) -> pd.Series:
    nontrend = ~events["regime_code"].astype(str).isin(["D03", "D04", "D05", "D06"])
    if strategy_id == "S01":
        threshold = float(events["momentum_3_event"].abs().quantile(0.80))
        signal = np.sign(events["momentum_3_event"]).where(
            (events["momentum_3_event"].abs() >= threshold)
            & (np.sign(events["momentum_3_event"]) == np.sign(events["mlofi_qty_event"]))
            & (events["spread_ticks"].astype(float) <= float(events["spread_ticks"].quantile(0.80))),
            0,
        )
    elif strategy_id == "S02":
        threshold = float(events["mlofi_qty_event"].abs().quantile(0.80))
        signal = np.sign(events["mlofi_qty_event"]).where(events["mlofi_qty_event"].abs() >= threshold, 0)
    elif strategy_id == "S05":
        threshold = float(events["microprice_dev"].abs().quantile(0.80))
        signal = np.sign(events["microprice_dev"]).where(events["microprice_dev"].abs() >= threshold, 0)
    elif strategy_id == "S07":
        threshold = float(events["l5_imbalance"].abs().quantile(0.80))
        signal = -np.sign(events["l5_imbalance"]).where(nontrend & (events["l5_imbalance"].abs() >= threshold), 0)
    elif strategy_id == "S09":
        threshold = float(events["l1_imbalance"].abs().quantile(0.80))
        signal = np.sign(events["l1_imbalance"]).where(events["l1_imbalance"].abs() >= threshold, 0)
    else:
        signal = pd.Series(0, index=events.index)
    tradable = events["next_mid_price"].notna()
    tradable &= ~events["is_duplicate"].astype(bool)
    tradable &= ~events["is_disconnect_gap"].astype(bool)
    tradable &= ~events["is_out_of_order_injected"].astype(bool)
    return pd.Series(signal, index=events.index).where(tradable, 0).fillna(0).astype("int8")


def latency_shift(events: pd.DataFrame, signal: pd.Series, latency_events: int) -> pd.Series:
    if latency_events <= 0:
        return signal
    return signal.groupby(
        [events["feed_profile"], events["synthetic_year_day"], events["symbol"]],
        sort=False,
    ).shift(latency_events).fillna(0).astype("int8")


def summarize_trades(trades: pd.DataFrame, strategy_id: str, profile: dict) -> tuple[dict[str, object], pd.DataFrame]:
    if trades.empty:
        return (
            {
                "strategy_id": strategy_id,
                "execution_profile": profile["execution_profile"],
                "trades": 0,
                "symbols": 0,
                "synthetic_year_days": TRADING_DAYS_PER_YEAR,
                "mean_gross_return": 0.0,
                "mean_cost_return": 0.0,
                "mean_zerodha_charge_return": 0.0,
                "mean_net_return": 0.0,
                "annual_net_pnl_inr": 0.0,
                "worst_daily_net_pnl_inr": 0.0,
                "max_drawdown_inr": 0.0,
                "positive_day_fraction": 0.0,
                "annualized_sharpe_proxy": 0.0,
                "synthetic_full_year_acceptance_ready": False,
            },
            pd.DataFrame(),
        )
    daily = trades.groupby("synthetic_year_day", sort=True).agg(
        daily_net_pnl_inr=("net_pnl_inr", "sum"),
        daily_trades=("net_pnl_inr", "size"),
    ).reset_index()
    daily["running_net_pnl_inr"] = daily["daily_net_pnl_inr"].cumsum()
    daily["running_peak_inr"] = daily["running_net_pnl_inr"].cummax()
    daily["drawdown_inr"] = daily["running_net_pnl_inr"] - daily["running_peak_inr"]
    daily_std = float(daily["daily_net_pnl_inr"].std(ddof=1))
    daily_mean = float(daily["daily_net_pnl_inr"].mean())
    sharpe = float((daily_mean / daily_std) * np.sqrt(TRADING_DAYS_PER_YEAR)) if daily_std > 0 else 0.0
    return (
        {
            "strategy_id": strategy_id,
            "execution_profile": profile["execution_profile"],
            "trades": int(len(trades)),
            "symbols": int(trades["symbol"].nunique()),
            "synthetic_year_days": TRADING_DAYS_PER_YEAR,
            "mean_gross_return": float(trades["gross_return"].mean()),
            "mean_cost_return": float(trades["cost_return"].mean()),
            "mean_zerodha_charge_return": float(trades["zerodha_charge_return"].mean()),
            "mean_net_return": float(trades["net_return"].mean()),
            "annual_net_pnl_inr": float(trades["net_pnl_inr"].sum()),
            "worst_daily_net_pnl_inr": float(daily["daily_net_pnl_inr"].min()),
            "max_drawdown_inr": float(daily["drawdown_inr"].min()),
            "positive_day_fraction": float((daily["daily_net_pnl_inr"] > 0).mean()),
            "annualized_sharpe_proxy": sharpe,
            "synthetic_full_year_acceptance_ready": False,
        },
        daily.assign(strategy_id=strategy_id, execution_profile=profile["execution_profile"]),
    )


def simulate_full_year(events: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    summary_rows = []
    daily_rows = []
    sample_rows = []
    signals = {strategy_id: build_signal(events, strategy_id) for strategy_id in STRATEGY_IDS}
    for strategy_id, signal in signals.items():
        for profile in EXECUTION_PROFILES:
            total_latency = int(profile["decision_latency_events"] + profile["broker_latency_events"])
            executable = latency_shift(events, signal, total_latency)
            mask = executable.ne(0) & events["next_mid_price"].notna()
            if bool(profile.get("cancel_on_stale_or_disconnect", False)):
                mask &= ~(
                    events["is_disconnect_gap"].astype(bool)
                    | events["is_out_of_order_injected"].astype(bool)
                    | events["next_is_bad_feed"].astype(bool)
                )
            trades = events.loc[
                mask,
                [
                    "annual_event_id",
                    "feed_profile",
                    "synthetic_year_day",
                    "synthetic_trade_date",
                    "symbol",
                    "regime_code",
                    "mid_price",
                    "next_mid_price",
                    "spread_ticks",
                    "tick_size",
                    "is_market_shock_day",
                    "is_disconnect_gap",
                ],
            ].copy()
            trades["strategy_id"] = strategy_id
            trades["execution_profile"] = profile["execution_profile"]
            trades["latency_events"] = total_latency
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
            for column in charges.columns:
                trades[column] = charges[column]
            trades["gross_return"] = gross_return
            trades["spread_crossing_cost_return"] = spread_cost
            trades["slippage_cost_return"] = slippage_cost
            trades["internal_bps_cost_return"] = internal_bps_cost
            trades["cost_return"] = spread_cost + slippage_cost + internal_bps_cost + trades["zerodha_charge_return"]
            trades["net_return"] = trades["gross_return"] - trades["cost_return"]
            trades["net_pnl_inr"] = trades["gross_return"] * trades["entry_notional_inr"] - (
                trades["spread_crossing_cost_return"] + trades["slippage_cost_return"] + trades["internal_bps_cost_return"]
            ) * trades["entry_notional_inr"] - trades["zerodha_total_charges_inr"]
            summary, daily = summarize_trades(trades, strategy_id, profile)
            summary_rows.append(summary)
            daily_rows.append(daily)
            if len(trades):
                sample_rows.append(
                    trades.sort_values("annual_event_id", kind="mergesort")
                    .groupby(["strategy_id", "execution_profile"], sort=False)
                    .head(SAMPLE_TRADES_PER_PROFILE)
                )
    summary_frame = pd.DataFrame(summary_rows).sort_values(["annual_net_pnl_inr"], ascending=False, kind="mergesort")
    daily_frame = pd.concat(daily_rows, ignore_index=True) if daily_rows else pd.DataFrame()
    sample_frame = pd.concat(sample_rows, ignore_index=True) if sample_rows else pd.DataFrame()
    return summary_frame, daily_frame, sample_frame


def build_overall_summary(events: pd.DataFrame, summary: pd.DataFrame, sample: pd.DataFrame) -> pd.DataFrame:
    realistic = summary[summary["execution_profile"].astype(str).isin(["retail_marketable_default", "stressed_retail"])]
    rows = [
        ("phase42_native_full_year_event_rows", int(len(events)), "Native 252-day synthetic L2 event-state rows generated"),
        ("phase42_synthetic_year_days", TRADING_DAYS_PER_YEAR, "Synthetic trading days generated"),
        ("phase42_symbols", int(events["symbol"].nunique()), "Symbols represented"),
        ("phase42_feed_profiles", int(events["feed_profile"].nunique()), "Feed profiles represented"),
        ("phase42_strategy_profile_rows", int(len(summary)), "Strategy/profile rows evaluated"),
        ("phase42_total_strategy_trades", int(summary["trades"].sum()), "Total simulated strategy trades across profiles"),
        ("phase42_profitable_strategy_profile_rows", int((summary["annual_net_pnl_inr"] > 0).sum()), "Annual positive P&L rows across all profiles"),
        ("phase42_profitable_realistic_strategy_profile_rows", int((realistic["annual_net_pnl_inr"] > 0).sum()), "Annual positive P&L rows under retail/stressed profiles"),
        ("phase42_best_annual_net_pnl_inr", float(summary["annual_net_pnl_inr"].max()) if len(summary) else 0.0, "Best annual net P&L across all profiles"),
        ("phase42_best_realistic_annual_net_pnl_inr", float(realistic["annual_net_pnl_inr"].max()) if len(realistic) else 0.0, "Best annual net P&L under retail/stressed profiles"),
        ("phase42_sample_trade_rows", int(len(sample)), "Persisted deterministic sample trade rows"),
        ("phase42_synthetic_full_year_acceptance_ready", 0, "Native full-year synthetic run is experiment evidence, not acceptance"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase 42 Native Full-Year Synthetic L2 Experiment",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This phase builds a native 252-trading-day synthetic L2 event-state product from the existing 189-day synthetic universe, recomputes event features, and runs strategy execution directly on those event rows.",
        "It is synthetic-only experiment evidence, not broker/paper/live acceptance.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase42_native_full_year_l2_experiment_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase42(compact_l2_path: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    compact = load_compact_l2(compact_l2_path)
    events = build_annual_l2(compact)
    summary, daily, sample = simulate_full_year(events)
    overall = build_overall_summary(events, summary, sample)
    event_output = output_dir / "native_full_year_l2_event_state.parquet"
    pq.write_table(pa.Table.from_pandas(events, preserve_index=False), event_output, compression="zstd")
    summary.to_csv(output_dir / "native_full_year_strategy_results.csv", index=False)
    daily.to_csv(output_dir / "native_full_year_daily_pnl.csv", index=False)
    pq.write_table(pa.Table.from_pandas(sample, preserve_index=False), output_dir / "native_full_year_trade_sample.parquet", compression="zstd")
    overall.to_csv(output_dir / "native_full_year_l2_experiment_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Overall Summary": overall,
            "Strategy Results": summary,
            "Top Realistic Results": summary[summary["execution_profile"].astype(str).isin(["retail_marketable_default", "stressed_retail"])].head(20),
            "Daily PnL Sample": daily.head(60),
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase42_native_252_day_synthetic_l2_experiment_not_acceptance",
        "native_full_year_event_rows": int(len(events)),
        "strategy_profile_rows": int(len(summary)),
        "total_strategy_trades": int(summary["trades"].sum()),
        "synthetic_full_year_acceptance_ready": 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase42",
            generated_utc=generated_utc,
            inputs={"compact_l2_state": str(compact_l2_path)},
            parameters={
                "trading_days_per_year": TRADING_DAYS_PER_YEAR,
                "source_days": int(compact[["quarter_profile", "scenario_day", "trade_date"]].drop_duplicates().shape[0]),
                "strategy_ids": STRATEGY_IDS,
                "execution_profiles": [profile["execution_profile"] for profile in EXECUTION_PROFILES],
                "acceptance_boundary": "synthetic_only_experiment_not_acceptance",
            },
            outputs={
                "event_state": str(event_output),
                "overall_summary": str(output_dir / "native_full_year_l2_experiment_summary.csv"),
                "strategy_results": str(output_dir / "native_full_year_strategy_results.csv"),
                "daily_pnl": str(output_dir / "native_full_year_daily_pnl.csv"),
                "trade_sample": str(output_dir / "native_full_year_trade_sample.parquet"),
                "report": str(output_dir / "phase42_native_full_year_l2_experiment_report.md"),
                "manifest": str(output_dir / "phase42_native_full_year_l2_experiment_manifest.json"),
            },
            random_seed="none_deterministic_252_day_l2_event_expansion",
            scenario_ids="phase9_tier_b_189_day_l2_universe_expanded_to_252_synthetic_days",
            cost_model_version="phase12_zerodha_equity_intraday_cost_model",
            latency_model_version="phase12_execution_profiles",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase42_native_full_year_l2_experiment_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run native 252-day synthetic L2 experiment.")
    parser.add_argument("--compact-l2", type=Path, default=Path("outputs/phase9/tier_b/compact_l2_state.parquet"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase42"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase42(args.compact_l2, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
