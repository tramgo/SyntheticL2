from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase56_cost_clearing_label_discovery import DEFAULT_ORDER_NOTIONAL_INR
from synthetic_l2.phase61_lower_frequency_candidate_sweep import profile_cost_bps, retail_profile
from synthetic_l2.phase70_cross_symbol_lead_lag_labels import ETF_SYMBOLS, symbol_universe
from synthetic_l2.phase76_common_overlap_matrix_validator import DEFAULT_LEADER_SYMBOL, DEFAULT_LEADER_THRESHOLD
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase84")
DEFAULT_PHASE83_DIR = Path("outputs/phase83")


def load_bars(phase83_dir: Path) -> pd.DataFrame:
    path = phase83_dir / "stratified_source_event_bars.parquet"
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_parquet(path)


def hdfcbank_recheck(bars: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    target_symbols = [symbol for symbol in symbol_universe() if symbol != DEFAULT_LEADER_SYMBOL and symbol not in ETF_SYMBOLS]
    leader = bars[bars["symbol"].eq(DEFAULT_LEADER_SYMBOL)][
        ["trade_month", "trade_date", "feed_profile", "source_event_bar_id", "bar_return"]
    ].rename(columns={"bar_return": "leader_bar_return"})
    targets = bars[bars["symbol"].isin(target_symbols)].copy()
    joined = targets.merge(leader, on=["trade_month", "trade_date", "feed_profile", "source_event_bar_id"], how="inner")
    joined = joined[joined["next_bar_return"].notna() & joined["leader_bar_return"].abs().ge(float(DEFAULT_LEADER_THRESHOLD))].copy()
    if joined.empty:
        return pd.DataFrame(), pd.DataFrame()
    profile = retail_profile()
    slippage_ticks = float(profile["fixed_slippage_ticks"])
    impact_bps = float(profile["impact_bps"]) + float(profile.get("fees_bps", 0.0))
    zerodha_bps = profile_cost_bps(profile)
    joined["side"] = np.sign(joined["leader_bar_return"].astype(float))
    joined = joined[joined["side"].ne(0)].copy()
    joined["gross_return"] = joined["side"].astype(float) * joined["next_bar_return"].astype(float)
    joined["cost_return"] = (
        ((joined["avg_spread"].astype(float) / 2.0) / joined["close_mid_price"].astype(float))
        + (slippage_ticks * joined["avg_spread"].astype(float) / joined["close_mid_price"].astype(float))
        + (impact_bps / 10000.0)
        + (zerodha_bps / 10000.0)
    )
    joined["net_return"] = joined["gross_return"] - joined["cost_return"]
    joined["gross_pnl_inr"] = joined["gross_return"] * DEFAULT_ORDER_NOTIONAL_INR
    joined["cost_pnl_drag_inr"] = joined["cost_return"] * DEFAULT_ORDER_NOTIONAL_INR
    joined["net_pnl_inr"] = joined["net_return"] * DEFAULT_ORDER_NOTIONAL_INR
    month_rows: list[dict[str, Any]] = []
    for month, group in joined.groupby("trade_month", sort=True):
        symbol_net = group.groupby("symbol", sort=True)["net_return"].sum()
        gross = float(group["gross_pnl_inr"].sum())
        cost = float(group["cost_pnl_drag_inr"].sum())
        month_rows.append(
            {
                "trade_month": month,
                "trades": int(len(group)),
                "target_symbols": int(group["symbol"].nunique()),
                "net_pnl_inr": float(group["net_pnl_inr"].sum()),
                "gross_pnl_proxy_inr": gross,
                "cost_pnl_drag_proxy_inr": cost,
                "precision_cost_clear": float((group["gross_return"] > group["cost_return"]).mean()),
                "positive_target_fraction": float((symbol_net > 0).mean()) if int(symbol_net.shape[0]) else 0.0,
                "cost_drag_to_abs_gross_ratio": cost / abs(gross) if abs(gross) > 0 else np.nan,
            }
        )
    return pd.DataFrame(month_rows), joined


def summarize(monthly: pd.DataFrame, bars: pd.DataFrame) -> pd.DataFrame:
    valid = monthly[monthly["trades"].gt(0)].copy()
    positive_months = int((valid["net_pnl_inr"] > 0).sum()) if not valid.empty else 0
    pass_months = int(
        (
            valid["net_pnl_inr"].gt(0)
            & valid["precision_cost_clear"].ge(0.55)
            & valid["cost_drag_to_abs_gross_ratio"].le(0.50)
            & valid["positive_target_fraction"].ge(0.50)
        ).sum()
    ) if not valid.empty else 0
    total_net = float(valid["net_pnl_inr"].sum()) if not valid.empty else 0.0
    total_trades = int(valid["trades"].sum()) if not valid.empty else 0
    positive_fraction = positive_months / float(len(valid) or 1)
    pass_fraction = pass_months / float(len(valid) or 1)
    aggregate_pass = bool(total_net > 0 and total_trades >= 100 and positive_fraction >= 0.60 and pass_fraction >= 0.60)
    return pd.DataFrame(
        [
            ("phase84_cached_bar_rows", int(len(bars)), "Cached stratified bars read"),
            ("phase84_months_tested", int(bars["trade_month"].nunique()), "Months represented in cached bars"),
            ("phase84_valid_months", int(len(valid)), "Months with HDFCBANK recheck trades"),
            ("phase84_positive_months", positive_months, "Valid months with positive after-cost synthetic P&L"),
            ("phase84_pass_months", pass_months, "Valid months passing quality gates"),
            ("phase84_total_trades", total_trades, "Aggregate HDFCBANK target trades"),
            ("phase84_total_net_pnl_inr", total_net, "Aggregate after-cost synthetic net P&L"),
            ("phase84_positive_month_fraction", positive_fraction, "Positive valid-month fraction"),
            ("phase84_pass_month_fraction", pass_fraction, "Per-month gate pass fraction"),
            ("phase84_cached_stratified_hdfcbank_pass", int(aggregate_pass), "1 means HDFCBANK survives cached stratified retest"),
            (
                "phase84_recommend_next_action",
                "retire_hdfcbank_lead_lag_after_cached_stratified_falsification" if not aggregate_pass else "expand_cached_stratified_hdfcbank_with_risk_controls",
                "Recommended next milestone",
            ),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase84 Cached Stratified HDFCBANK Retest",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase84 retests the HDFCBANK lead-lag clue on the Phase83 coverage-valid cached source-event bars.",
        "This is the fair full stratified retest after the Phase82 timestamp-bucket coverage failure.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase84_cached_stratified_hdfcbank_retest_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase84(phase83_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    bars = load_bars(phase83_dir)
    monthly, trades = hdfcbank_recheck(bars)
    acceptance = summarize(monthly, bars)
    monthly.to_csv(output_dir / "cached_stratified_hdfcbank_monthly.csv", index=False)
    trades.to_csv(output_dir / "cached_stratified_hdfcbank_trades.csv", index=False)
    acceptance.to_csv(output_dir / "cached_stratified_hdfcbank_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Monthly HDFCBANK Recheck": monthly,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase84_cached_stratified_hdfcbank_retest",
        "cached_stratified_hdfcbank_pass": int(
            acceptance.loc[acceptance["metric"].eq("phase84_cached_stratified_hdfcbank_pass"), "value"].iloc[0]
        ),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase84",
            generated_utc=generated_utc,
            inputs={"phase83_bar_cache": str(phase83_dir / "stratified_source_event_bars.parquet")},
            parameters={
                "leader_symbol": DEFAULT_LEADER_SYMBOL,
                "threshold": DEFAULT_LEADER_THRESHOLD,
                "quality_gate": "total_net_positive_total_trades_ge_100_positive_month_fraction_ge_0_60_pass_month_fraction_ge_0_60",
            },
            outputs={
                "monthly": str(output_dir / "cached_stratified_hdfcbank_monthly.csv"),
                "trades": str(output_dir / "cached_stratified_hdfcbank_trades.csv"),
                "acceptance_summary": str(output_dir / "cached_stratified_hdfcbank_acceptance_summary.csv"),
                "report": str(output_dir / "phase84_cached_stratified_hdfcbank_retest_report.md"),
                "manifest": str(output_dir / "phase84_cached_stratified_hdfcbank_retest_manifest.json"),
            },
            random_seed="none_deterministic_cached_stratified_hdfcbank_retest",
            scenario_ids="phase84_phase83_cached_stratified_source_event_bars",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase83_source_event_ordinal_alignment",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase84_cached_stratified_hdfcbank_retest_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retest HDFCBANK lead-lag on cached stratified event bars.")
    parser.add_argument("--phase83-dir", type=Path, default=DEFAULT_PHASE83_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase84(args.phase83_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
