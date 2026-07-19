from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase56_cost_clearing_label_discovery import DEFAULT_DENSE_ROOT
from synthetic_l2.phase61_lower_frequency_candidate_sweep import load_phase60_candidate, query_candidate_shard
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase63")
DEFAULT_PHASE60_TOP = Path("outputs/phase60/lower_frequency_top_results.csv")
DEFAULT_SYMBOL = "KOTAKBANK"


def kotakbank_files(dense_root: Path, symbol: str = DEFAULT_SYMBOL) -> list[tuple[int, str, Path]]:
    files = sorted(dense_root.glob(f"trade_month=*/symbol={symbol}/part-00000.parquet"))
    selected: list[tuple[int, str, Path]] = []
    for offset, path in enumerate(files, start=1):
        trade_month = path.parent.parent.name.replace("trade_month=", "")
        selected.append((offset, trade_month, path))
    return selected


def run_symbol_probe(
    files: list[tuple[int, str, Path]],
    candidate: dict[str, Any],
    max_rows_per_shard: int | None,
) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for month_index, trade_month, path in files:
        frame = query_candidate_shard(path, month_index, candidate, max_rows_per_shard)
        if not frame.empty:
            frame.insert(1, "trade_month", trade_month)
        frames.append(frame)
    if not frames:
        return pd.DataFrame()
    daily = pd.concat(frames, ignore_index=True)
    if daily.empty:
        return daily
    daily["positive_after_costs"] = daily["net_pnl_inr"] > 0
    return daily


def monthly_rollup(daily: pd.DataFrame, files: list[tuple[int, str, Path]]) -> pd.DataFrame:
    inventory = pd.DataFrame(
        [
            {
                "month_index": month_index,
                "trade_month": trade_month,
                "symbol": DEFAULT_SYMBOL,
                "shard_path": str(path),
            }
            for month_index, trade_month, path in files
        ]
    )
    if daily.empty:
        rollup = inventory.copy()
        for column, value in {
            "trade_dates": 0,
            "trades": 0,
            "net_pnl_inr": 0.0,
            "gross_pnl_proxy_inr": 0.0,
            "cost_pnl_drag_proxy_inr": 0.0,
            "precision_cost_clear": 0.0,
            "positive_after_costs": False,
        }.items():
            rollup[column] = value
        return rollup

    grouped = (
        daily.groupby(["trade_month", "symbol"], sort=True)
        .agg(
            trade_dates=("trade_date", "nunique"),
            trades=("trades", "sum"),
            net_pnl_inr=("net_pnl_inr", "sum"),
            gross_pnl_proxy_inr=("gross_pnl_proxy_inr", "sum"),
            cost_pnl_drag_proxy_inr=("cost_pnl_drag_proxy_inr", "sum"),
            sum_net_return=("sum_net_return", "sum"),
        )
        .reset_index()
    )
    weighted_precision = (
        daily.assign(weighted_precision=daily["precision_cost_clear"] * daily["trades"])
        .groupby(["trade_month", "symbol"], sort=True)
        .agg(weighted_precision=("weighted_precision", "sum"), precision_trades=("trades", "sum"))
        .reset_index()
    )
    grouped = grouped.merge(weighted_precision, on=["trade_month", "symbol"], how="left")
    grouped["precision_cost_clear"] = grouped["weighted_precision"] / grouped["precision_trades"].replace(0, np.nan)
    grouped["precision_cost_clear"] = grouped["precision_cost_clear"].fillna(0.0)
    grouped["positive_after_costs"] = grouped["net_pnl_inr"] > 0
    return inventory.merge(grouped.drop(columns=["weighted_precision", "precision_trades"]), on=["trade_month", "symbol"], how="left").fillna(
        {
            "trade_dates": 0,
            "trades": 0,
            "net_pnl_inr": 0.0,
            "gross_pnl_proxy_inr": 0.0,
            "cost_pnl_drag_proxy_inr": 0.0,
            "sum_net_return": 0.0,
            "precision_cost_clear": 0.0,
            "positive_after_costs": False,
        }
    )


def summarize(
    daily: pd.DataFrame,
    monthly: pd.DataFrame,
    files: list[tuple[int, str, Path]],
    candidate: dict[str, Any],
    elapsed_seconds: float,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    trades = int(monthly["trades"].sum()) if not monthly.empty else 0
    net_pnl = float(monthly["net_pnl_inr"].sum()) if not monthly.empty else 0.0
    gross_pnl = float(monthly["gross_pnl_proxy_inr"].sum()) if not monthly.empty else 0.0
    cost_drag = float(monthly["cost_pnl_drag_proxy_inr"].sum()) if not monthly.empty else 0.0
    active_months = monthly[monthly["trades"] > 0].copy() if not monthly.empty else monthly
    positive_month_fraction = float(monthly["positive_after_costs"].mean()) if not monthly.empty else 0.0
    active_positive_month_fraction = (
        float(active_months["positive_after_costs"].mean()) if active_months is not None and not active_months.empty else 0.0
    )
    precision = (
        float(np.average(daily["precision_cost_clear"], weights=daily["trades"]))
        if not daily.empty and int(daily["trades"].sum()) > 0
        else 0.0
    )
    survives = bool(net_pnl > 0 and trades >= 100 and positive_month_fraction >= 0.50 and active_positive_month_fraction >= 0.50)
    summary = pd.DataFrame(
        [
            {
                "rule_id": str(candidate["rule_id"]),
                "symbol": DEFAULT_SYMBOL,
                "bar_events": int(candidate["bar_events"]),
                "abs_threshold": float(candidate["abs_threshold"]),
                "months_scanned": len(files),
                "active_months": int((monthly["trades"] > 0).sum()) if not monthly.empty else 0,
                "trade_dates": int(daily["trade_date"].nunique()) if not daily.empty else 0,
                "trades": trades,
                "net_pnl_inr": net_pnl,
                "gross_pnl_proxy_inr": gross_pnl,
                "cost_pnl_drag_proxy_inr": cost_drag,
                "positive_months": int(monthly["positive_after_costs"].sum()) if not monthly.empty else 0,
                "positive_month_fraction": positive_month_fraction,
                "active_positive_month_fraction": active_positive_month_fraction,
                "precision_cost_clear": precision,
                "mean_net_pnl_per_trade_inr": net_pnl / trades if trades else 0.0,
                "cost_drag_to_abs_gross_ratio": cost_drag / abs(gross_pnl) if gross_pnl else 0.0,
                "phase63_survives_kotakbank_falsification": survives,
            }
        ]
    )
    acceptance = pd.DataFrame(
        [
            ("phase63_symbol", DEFAULT_SYMBOL, "Single-symbol falsification target from Phase62"),
            ("phase63_months_scanned", len(files), "KOTAKBANK monthly dense shards scanned"),
            ("phase63_active_months", int(summary.iloc[0]["active_months"]), "Months with at least one candidate trade"),
            ("phase63_trades", trades, "Candidate trades generated by the exact Phase60 rule"),
            ("phase63_net_pnl_inr", net_pnl, "After-cost net P&L using the Zerodha retail cost model"),
            ("phase63_gross_pnl_proxy_inr", gross_pnl, "Gross signal P&L proxy before costs"),
            ("phase63_cost_pnl_drag_proxy_inr", cost_drag, "Cost drag proxy including spread/slippage/impact/Zerodha charges"),
            ("phase63_positive_month_fraction", positive_month_fraction, "Fraction of all scanned months positive after costs"),
            ("phase63_active_positive_month_fraction", active_positive_month_fraction, "Fraction of active months positive after costs"),
            ("phase63_precision_cost_clear", precision, "Trade-weighted fraction clearing cost"),
            ("phase63_survives_kotakbank_falsification", int(survives), "1 means the KOTAKBANK-only hypothesis survived"),
            ("phase63_elapsed_seconds", elapsed_seconds, "Elapsed seconds"),
            ("phase63_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha retail intraday cost model"),
            ("phase63_recommend_next_action", "expand_kotakbank_full_rows" if survives else "retire_phase60_candidate_family", "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )
    return summary, acceptance


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase63 KOTAKBANK Falsification Probe",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase63 replays the exact Phase60 event-bar candidate on KOTAKBANK only across all available monthly dense shards.",
        "This is a falsification probe for the only tiny positive aggregate left after Phase62, not a refit.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase63_kotakbank_falsification_probe_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase63(
    dense_root: Path,
    output_dir: Path,
    base_dir: Path,
    phase60_top: Path,
    max_rows_per_shard: int | None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    candidate = load_phase60_candidate(phase60_top)
    files = kotakbank_files(dense_root)
    started = time.perf_counter()
    daily = run_symbol_probe(files, candidate, max_rows_per_shard)
    elapsed = time.perf_counter() - started
    monthly = monthly_rollup(daily, files)
    summary, acceptance = summarize(daily, monthly, files, candidate, elapsed)
    inventory = pd.DataFrame(
        [{"month_index": month_index, "trade_month": trade_month, "shard_path": str(path)} for month_index, trade_month, path in files]
    )

    pd.DataFrame([candidate]).to_csv(output_dir / "phase60_candidate_replayed.csv", index=False)
    inventory.to_csv(output_dir / "kotakbank_file_inventory.csv", index=False)
    daily.to_csv(output_dir / "kotakbank_daily_results.csv", index=False)
    monthly.to_csv(output_dir / "kotakbank_monthly_results.csv", index=False)
    summary.to_csv(output_dir / "kotakbank_summary.csv", index=False)
    acceptance.to_csv(output_dir / "kotakbank_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "KOTAKBANK Summary": summary,
            "Monthly Results": monthly,
            "Daily Results": daily,
            "Replayed Phase60 Candidate": pd.DataFrame([candidate]),
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase63_kotakbank_falsification_probe",
        "symbol": DEFAULT_SYMBOL,
        "months_scanned": len(files),
        "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
        "survives_kotakbank_falsification": int(bool(summary.iloc[0]["phase63_survives_kotakbank_falsification"])),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase63",
            generated_utc=generated_utc,
            inputs={
                "phase51_dense_lake": str(dense_root),
                "phase60_top_results": str(phase60_top),
                "phase62_symbol_dependence_rollup": "outputs/phase62/symbol_dependence_rollup.csv",
            },
            parameters={
                "symbol": DEFAULT_SYMBOL,
                "months_scanned": len(files),
                "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
                "candidate_rule_id": str(candidate["rule_id"]),
                "candidate_bar_events": int(candidate["bar_events"]),
                "candidate_abs_threshold": float(candidate["abs_threshold"]),
                "validation_gate": "net_pnl_gt_0_and_trades_ge_100_and_positive_month_fraction_ge_0_50_and_active_positive_month_fraction_ge_0_50",
            },
            outputs={
                "candidate": str(output_dir / "phase60_candidate_replayed.csv"),
                "file_inventory": str(output_dir / "kotakbank_file_inventory.csv"),
                "daily_results": str(output_dir / "kotakbank_daily_results.csv"),
                "monthly_results": str(output_dir / "kotakbank_monthly_results.csv"),
                "summary": str(output_dir / "kotakbank_summary.csv"),
                "acceptance_summary": str(output_dir / "kotakbank_acceptance_summary.csv"),
                "report": str(output_dir / "phase63_kotakbank_falsification_probe_report.md"),
                "manifest": str(output_dir / "phase63_kotakbank_falsification_probe_manifest.json"),
            },
            random_seed="none_deterministic_fixed_candidate_replay",
            scenario_ids="phase63_kotakbank_all_monthly_dense_shards",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase63_fixed_phase60_event_bar_candidate",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase63_kotakbank_falsification_probe_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replay the Phase60 candidate on KOTAKBANK only across all dense monthly shards.")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--phase60-top", type=Path, default=DEFAULT_PHASE60_TOP)
    parser.add_argument("--max-rows-per-shard", type=int, default=250_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase63(args.dense_root, args.output_dir, args.base_dir, args.phase60_top, args.max_rows_per_shard)


if __name__ == "__main__":
    main()
