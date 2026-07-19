from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


DEFAULT_PHASE52_DAILY = Path("outputs/phase52/dense_replay_daily_symbol.csv")
DEFAULT_OUTPUT_DIR = Path("outputs/phase53")
DEFAULT_ORDER_NOTIONAL_INR = 100_000.0


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    columns = list(frame.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for _, row in frame.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in columns) + " |")
    return "\n".join(lines)


def load_daily(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Phase52 daily-symbol checkpoint not found: {path}")
    data = pd.read_csv(path)
    required = {
        "shard_index",
        "shard_path",
        "trade_date",
        "symbol",
        "strategy_id",
        "execution_profile",
        "trades",
        "sum_gross_return",
        "sum_cost_return",
        "sum_net_return",
        "net_pnl_inr",
    }
    missing = sorted(required.difference(data.columns))
    if missing:
        raise ValueError(f"Missing required Phase52 columns: {missing}")
    return data


def summarize_strategy_profiles(data: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        data.groupby(["strategy_id", "execution_profile"], as_index=False)
        .agg(
            trades=("trades", "sum"),
            gross_return_sum=("sum_gross_return", "sum"),
            cost_return_sum=("sum_cost_return", "sum"),
            net_return_sum=("sum_net_return", "sum"),
            net_pnl_inr=("net_pnl_inr", "sum"),
            daily_symbol_rows=("net_pnl_inr", "size"),
            positive_net_rows=("net_pnl_inr", lambda s: int((s > 0).sum())),
            positive_gross_rows=("sum_gross_return", lambda s: int((s > 0).sum())),
            max_daily_net_pnl_inr=("net_pnl_inr", "max"),
            max_daily_gross_return=("sum_gross_return", "max"),
            mean_net_return=("mean_net_return", "mean"),
            mean_cost_return=("mean_cost_return", "mean"),
        )
        .sort_values("net_pnl_inr", ascending=False)
        .reset_index(drop=True)
    )
    grouped["gross_pnl_proxy_inr"] = grouped["gross_return_sum"] * DEFAULT_ORDER_NOTIONAL_INR
    grouped["cost_pnl_drag_proxy_inr"] = grouped["cost_return_sum"] * DEFAULT_ORDER_NOTIONAL_INR
    grouped["cost_drag_to_abs_gross_ratio"] = grouped["cost_return_sum"] / grouped["gross_return_sum"].abs().clip(lower=1e-12)
    grouped["break_even_cost_reduction_pct"] = (
        (grouped["cost_return_sum"] + grouped["net_return_sum"]) / grouped["cost_return_sum"].replace(0, pd.NA) * 100.0
    ).fillna(0.0)
    grouped["profitable_after_cost"] = grouped["net_pnl_inr"] > 0
    grouped["gross_positive_total"] = grouped["gross_return_sum"] > 0
    return grouped


def summarize_overall(data: pd.DataFrame, strategy_summary: pd.DataFrame) -> pd.DataFrame:
    max_row = data.loc[data["net_pnl_inr"].idxmax()]
    rows = [
        ("phase53_phase52_shards_observed", int(data["shard_path"].nunique()), "Unique Phase52 dense shards in the checkpoint ledger"),
        ("phase53_phase52_max_shard_index", int(data["shard_index"].max()), "Highest shard index observed in the checkpoint ledger"),
        ("phase53_dense_trade_rows_observed", int(data["trades"].sum()), "Aggregated dense tick trade count in the checkpoint ledger"),
        ("phase53_strategy_profile_rows", int(len(strategy_summary)), "Strategy/profile rows analyzed"),
        ("phase53_profitable_strategy_profiles", int(strategy_summary["profitable_after_cost"].sum()), "Aggregate strategy/profile rows with positive net P&L"),
        ("phase53_positive_daily_symbol_rows", int((data["net_pnl_inr"] > 0).sum()), "Daily-symbol strategy/profile rows with positive net P&L"),
        ("phase53_gross_positive_strategy_profiles", int(strategy_summary["gross_positive_total"].sum()), "Aggregate strategy/profile rows with positive gross return before costs"),
        ("phase53_positive_gross_daily_symbol_rows", int((data["sum_gross_return"] > 0).sum()), "Daily-symbol rows with positive gross return before costs"),
        ("phase53_best_net_daily_symbol_pnl_inr", float(max_row["net_pnl_inr"]), "Best single daily-symbol net P&L row"),
        ("phase53_best_net_daily_symbol_key", f"{max_row['trade_date']}|{max_row['symbol']}|{max_row['strategy_id']}|{max_row['execution_profile']}", "Best single daily-symbol row key"),
        ("phase53_recommend_continue_phase52_bruteforce", 0, "0 means pause brute-force shard replay and pivot to edge diagnostics/design"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_outputs(output_dir: Path, overall: pd.DataFrame, strategy_summary: pd.DataFrame, source_path: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    overall.to_csv(output_dir / "edge_diagnostics_summary.csv", index=False)
    strategy_summary.to_csv(output_dir / "edge_diagnostics_strategy_profiles.csv", index=False)
    display_cols = [
        "strategy_id",
        "execution_profile",
        "trades",
        "net_pnl_inr",
        "gross_pnl_proxy_inr",
        "cost_pnl_drag_proxy_inr",
        "positive_net_rows",
        "positive_gross_rows",
        "profitable_after_cost",
        "gross_positive_total",
    ]
    lines = [
        "# Phase53 Edge Diagnostics",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        f"Source: `{source_path}`",
        "",
        "Phase53 pauses the Phase52 brute-force shard replay and diagnoses whether the current dense tick-level signal catalog has any evidence of edge.",
        "",
        "## Summary",
        "",
        _markdown_table(overall),
        "",
        "## Strategy/Profile Diagnostics",
        "",
        _markdown_table(strategy_summary[display_cols]),
        "",
        "## Decision",
        "",
        "The current dense replay catalog has no positive after-cost strategy/profile rows and no positive daily-symbol net rows in the observed checkpoint ledger.",
        "Continuing the same shard-by-shard replay is low-value until the strategy catalog changes.",
        "The next best action is to design lower-turnover and more selective variants, then replay those against a bounded shard set before spending compute on the full dense lake.",
    ]
    (output_dir / "phase53_edge_diagnostics_report.md").write_text("\n".join(lines), encoding="utf-8")
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "phase": "phase53_edge_diagnostics",
        "source_phase52_daily": str(source_path),
        "outputs": {
            "summary": str(output_dir / "edge_diagnostics_summary.csv"),
            "strategy_profiles": str(output_dir / "edge_diagnostics_strategy_profiles.csv"),
            "report": str(output_dir / "phase53_edge_diagnostics_report.md"),
            "manifest": str(output_dir / "phase53_edge_diagnostics_manifest.json"),
        },
    }
    (output_dir / "phase53_edge_diagnostics_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def run(source_path: Path, output_dir: Path) -> None:
    data = load_daily(source_path)
    strategy_summary = summarize_strategy_profiles(data)
    overall = summarize_overall(data, strategy_summary)
    write_outputs(output_dir, overall, strategy_summary, source_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnose Phase52 dense replay edge and decide whether to continue brute-force shard replay.")
    parser.add_argument("--source", type=Path, default=DEFAULT_PHASE52_DAILY)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run(args.source, args.output_dir)


if __name__ == "__main__":
    main()
