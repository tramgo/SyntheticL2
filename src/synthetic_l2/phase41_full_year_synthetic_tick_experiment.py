from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


TRADING_DAYS_PER_YEAR = 252


def _read_trade_ledger(path: Path, source_phase: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    columns = [
        "model_id",
        "model_type",
        "execution_profile",
        "trade_date",
        "symbol",
        "net_pnl_inr",
        "net_return",
        "gross_return",
        "cost_return",
        "is_market_shock_day",
        "is_disconnect_gap",
    ]
    schema = pq.read_schema(path)
    available = [column for column in columns if column in schema.names]
    frame = pq.read_table(path, columns=available).to_pandas()
    frame["source_phase"] = source_phase
    if "is_market_shock_day" not in frame.columns:
        frame["is_market_shock_day"] = False
    if "is_disconnect_gap" not in frame.columns:
        frame["is_disconnect_gap"] = False
    return frame


def _daily_summary(trades: pd.DataFrame) -> pd.DataFrame:
    grouped = trades.groupby(["source_phase", "model_id", "model_type", "execution_profile", "trade_date"], sort=True)
    return grouped.agg(
        daily_trades=("net_pnl_inr", "size"),
        symbols=("symbol", "nunique"),
        daily_net_pnl_inr=("net_pnl_inr", "sum"),
        mean_net_return=("net_return", "mean"),
        mean_gross_return=("gross_return", "mean"),
        mean_cost_return=("cost_return", "mean"),
        market_shock_trade_fraction=("is_market_shock_day", "mean"),
        disconnect_trade_fraction=("is_disconnect_gap", "mean"),
    ).reset_index()


def _expand_one_group(group: pd.DataFrame) -> pd.DataFrame:
    ordered = group.sort_values("trade_date", kind="mergesort").reset_index(drop=True)
    rows = []
    for day_index in range(TRADING_DAYS_PER_YEAR):
        source = ordered.iloc[day_index % len(ordered)]
        rows.append(
            {
                "synthetic_year_day": day_index + 1,
                "source_trade_date": source["trade_date"],
                "cycle_ordinal": day_index // len(ordered),
                "daily_trades": int(source["daily_trades"]),
                "symbols": int(source["symbols"]),
                "daily_net_pnl_inr": float(source["daily_net_pnl_inr"]),
                "mean_net_return": float(source["mean_net_return"]),
                "market_shock_trade_fraction": float(source["market_shock_trade_fraction"]),
                "disconnect_trade_fraction": float(source["disconnect_trade_fraction"]),
            }
        )
    expanded = pd.DataFrame(rows)
    expanded["running_net_pnl_inr"] = expanded["daily_net_pnl_inr"].cumsum()
    expanded["running_peak_inr"] = expanded["running_net_pnl_inr"].cummax()
    expanded["drawdown_inr"] = expanded["running_net_pnl_inr"] - expanded["running_peak_inr"]
    return expanded


def build_annual_results(daily: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    result_rows = []
    sample_rows = []
    keys = ["source_phase", "model_id", "model_type", "execution_profile"]
    for key_values, group in daily.groupby(keys, sort=True):
        source_phase, model_id, model_type, execution_profile = key_values
        expanded = _expand_one_group(group)
        daily_std = float(expanded["daily_net_pnl_inr"].std(ddof=1))
        daily_mean = float(expanded["daily_net_pnl_inr"].mean())
        sharpe = float((daily_mean / daily_std) * np.sqrt(TRADING_DAYS_PER_YEAR)) if daily_std > 0 else 0.0
        result_rows.append(
            {
                "source_phase": source_phase,
                "model_id": model_id,
                "model_type": model_type,
                "execution_profile": execution_profile,
                "observed_source_days": int(group["trade_date"].nunique()),
                "synthetic_year_days": TRADING_DAYS_PER_YEAR,
                "annualized_trades": int(expanded["daily_trades"].sum()),
                "annualized_net_pnl_inr": float(expanded["daily_net_pnl_inr"].sum()),
                "mean_daily_net_pnl_inr": daily_mean,
                "worst_daily_net_pnl_inr": float(expanded["daily_net_pnl_inr"].min()),
                "max_drawdown_inr": float(expanded["drawdown_inr"].min()),
                "annualized_sharpe_proxy": sharpe,
                "positive_days": int((expanded["daily_net_pnl_inr"] > 0).sum()),
                "positive_day_fraction": float((expanded["daily_net_pnl_inr"] > 0).mean()),
                "mean_net_return": float(group["mean_net_return"].mean()),
                "mean_market_shock_trade_fraction": float(group["market_shock_trade_fraction"].mean()),
                "mean_disconnect_trade_fraction": float(group["disconnect_trade_fraction"].mean()),
                "synthetic_full_year_acceptance_ready": False,
                "experiment_scope": "deterministic_252_day_tick_trade_ledger_replay_not_acceptance",
            }
        )
        sample = expanded.head(12).copy()
        sample.insert(0, "execution_profile", execution_profile)
        sample.insert(0, "model_type", model_type)
        sample.insert(0, "model_id", model_id)
        sample.insert(0, "source_phase", source_phase)
        sample_rows.append(sample)
    results = pd.DataFrame(result_rows).sort_values(
        ["annualized_net_pnl_inr", "annualized_sharpe_proxy"],
        ascending=[False, False],
        kind="mergesort",
    ).reset_index(drop=True)
    samples = pd.concat(sample_rows, ignore_index=True) if sample_rows else pd.DataFrame()
    return results, samples


def build_summary(trades: pd.DataFrame, daily: pd.DataFrame, results: pd.DataFrame) -> pd.DataFrame:
    realistic = results[results["execution_profile"].astype(str).isin(["retail_marketable_default", "stressed_retail"])]
    rows = [
        ("phase41_trade_rows_loaded", int(len(trades)), "Tick/event trade rows loaded from synthetic replay ledgers"),
        ("phase41_source_phase_count", int(trades["source_phase"].nunique()), "Replay sources included"),
        ("phase41_daily_source_rows", int(len(daily)), "Daily source rows before deterministic annual expansion"),
        ("phase41_model_profile_rows", int(len(results)), "Model/profile full-year experiment rows"),
        ("phase41_synthetic_year_days", TRADING_DAYS_PER_YEAR, "Trading days per deterministic synthetic year"),
        ("phase41_profitable_model_profile_rows", int((results["annualized_net_pnl_inr"] > 0).sum()), "All-profile annualized positive P&L rows"),
        ("phase41_profitable_realistic_model_profile_rows", int((realistic["annualized_net_pnl_inr"] > 0).sum()), "Retail/stressed annualized positive P&L rows"),
        ("phase41_best_annualized_net_pnl_inr", float(results["annualized_net_pnl_inr"].max()) if len(results) else 0.0, "Best annualized net P&L across all profiles"),
        ("phase41_best_realistic_annualized_net_pnl_inr", float(realistic["annualized_net_pnl_inr"].max()) if len(realistic) else 0.0, "Best annualized net P&L across retail/stressed profiles"),
        ("phase41_synthetic_full_year_acceptance_ready", 0, "Immediate full-year replay is not acceptance or broker readiness"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase 41 Full-Year Synthetic Tick Experiment",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This is an immediate deterministic 252-trading-day replay over existing synthetic tick/event trade ledgers.",
        "It is tick-level trade-ledger based, but it is not a newly generated independent 252-day L2 universe and it is not acceptance evidence.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase41_full_year_synthetic_tick_experiment_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase41(paths: dict[str, Path], output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    ledgers = [
        _read_trade_ledger(paths["phase25_trade_ledger"], "phase25_event_replay"),
        _read_trade_ledger(paths["phase26_trade_ledger"], "phase26_strategy_salvage"),
        _read_trade_ledger(paths["phase27_trade_ledger"], "phase27_feature_edge"),
        _read_trade_ledger(paths["phase29_trade_ledger"], "phase29_partial_proxy"),
    ]
    trades = pd.concat(ledgers, ignore_index=True)
    daily = _daily_summary(trades)
    results, samples = build_annual_results(daily)
    summary = build_summary(trades, daily, results)

    top_results = results.head(80)
    realistic_results = results[results["execution_profile"].astype(str).isin(["retail_marketable_default", "stressed_retail"])].head(80)
    frames = {
        "Summary": summary,
        "Top Annualized Results": top_results,
        "Top Realistic Retail/Stressed Results": realistic_results,
        "Daily Path Sample": samples.head(120),
    }

    summary.to_csv(output_dir / "full_year_synthetic_tick_experiment_summary.csv", index=False)
    results.to_csv(output_dir / "full_year_synthetic_tick_experiment_results.csv", index=False)
    realistic_results.to_csv(output_dir / "full_year_synthetic_tick_experiment_realistic_results.csv", index=False)
    samples.to_csv(output_dir / "full_year_synthetic_tick_experiment_daily_path_sample.csv", index=False)
    write_report(output_dir, frames)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase41_immediate_full_year_synthetic_tick_trade_ledger_replay_not_acceptance",
        "trade_rows_loaded": int(len(trades)),
        "model_profile_rows": int(len(results)),
        "synthetic_year_days": TRADING_DAYS_PER_YEAR,
        "synthetic_full_year_acceptance_ready": 0,
        "not_independent_new_252_day_l2_universe": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase41",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={
                "trading_days_per_year": TRADING_DAYS_PER_YEAR,
                "annual_expansion_method": "deterministic_cycle_observed_tick_trade_daily_pnl_paths",
                "source_trade_ledgers": list(paths.keys()),
                "acceptance_boundary": "not_acceptance_not_paper_or_live",
            },
            outputs={
                "summary": str(output_dir / "full_year_synthetic_tick_experiment_summary.csv"),
                "results": str(output_dir / "full_year_synthetic_tick_experiment_results.csv"),
                "realistic_results": str(output_dir / "full_year_synthetic_tick_experiment_realistic_results.csv"),
                "daily_path_sample": str(output_dir / "full_year_synthetic_tick_experiment_daily_path_sample.csv"),
                "report": str(output_dir / "phase41_full_year_synthetic_tick_experiment_report.md"),
                "manifest": str(output_dir / "phase41_full_year_synthetic_tick_experiment_manifest.json"),
            },
            random_seed="none_deterministic_annual_cycle_replay",
            scenario_ids="phase25_phase26_phase27_phase29_tick_trade_ledgers_expanded_to_252_days",
            cost_model_version="source_replay_zerodha_cost_profiles_preserved",
            latency_model_version="source_replay_execution_profiles_preserved",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase41_full_year_synthetic_tick_experiment_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run immediate full-year synthetic tick trade-ledger experiment.")
    parser.add_argument("--phase25-trade-ledger", type=Path, default=Path("outputs/phase25/event_replay_trade_ledger.parquet"))
    parser.add_argument("--phase26-trade-ledger", type=Path, default=Path("outputs/phase26/strategy_salvage_trade_ledger.parquet"))
    parser.add_argument("--phase27-trade-ledger", type=Path, default=Path("outputs/phase27/feature_edge_trade_ledger.parquet"))
    parser.add_argument("--phase29-trade-ledger", type=Path, default=Path("outputs/phase29/partial_strategy_proxy_trade_ledger.parquet"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase41"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase41(
        {
            "phase25_trade_ledger": args.phase25_trade_ledger,
            "phase26_trade_ledger": args.phase26_trade_ledger,
            "phase27_trade_ledger": args.phase27_trade_ledger,
            "phase29_trade_ledger": args.phase29_trade_ledger,
        },
        args.output_dir,
        args.base_dir,
    )


if __name__ == "__main__":
    main()
