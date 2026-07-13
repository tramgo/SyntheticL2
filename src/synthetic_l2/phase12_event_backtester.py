from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from synthetic_l2.reproducibility import reproducibility_fields


ORDER_MODELS = [
    ("market_order", "Cross spread and fill immediately against displayed opposite-side liquidity proxy."),
    ("marketable_limit_order", "Limit priced through L1; reject when arrival price breaches the protection band."),
    ("passive_limit_order", "Rest at L1 with pessimistic queue-position and adverse-selection fill approximation."),
    ("cancel_replace", "Cancel stale passive order and replace at refreshed marketable limit price."),
    ("partial_fill", "Allow displayed-depth and liquidity-bucket constrained partial fills."),
    ("rejection_scenario", "Reject stale, too-wide-spread, missing-price or price-band-invalid orders."),
]

SLIPPAGE_MODELS = [
    ("spread_cross", "Pay half-spread plus fixed profile cost for marketable flow."),
    ("depth_consuming_book_walk", "Increase cost when liquidity bucket is low or spread is wide."),
    ("passive_queue_adverse_selection", "Passive fill receives spread benefit but carries adverse-selection haircut."),
    ("stale_reject", "Reject when signal age or price protection gate fails."),
]


def load_trade_sample(path: Path) -> pd.DataFrame:
    frame = pd.read_parquet(path)
    if frame.empty:
        raise ValueError(f"Trade sample is empty: {path}")
    return frame


def _sample_events(trades: pd.DataFrame, max_per_strategy_profile: int) -> pd.DataFrame:
    sort_cols = ["strategy_id", "execution_profile", "trade_date", "feed_profile", "symbol", "bar_index"]
    base = trades.sort_values(sort_cols, kind="mergesort").reset_index(drop=True)
    sampled = []
    for (_strategy_id, _profile), group in base.groupby(["strategy_id", "execution_profile"], sort=True):
        if len(group) <= max_per_strategy_profile:
            sampled.append(group)
            continue
        positions = np.linspace(0, len(group) - 1, num=max_per_strategy_profile, dtype=int)
        sampled.append(group.iloc[positions])
    return pd.concat(sampled, ignore_index=True)


def _order_model_for_row(row: pd.Series, ordinal: int) -> str:
    if bool(row.get("is_market_shock_day", False)) and ordinal % 5 == 0:
        return "rejection_scenario"
    if row.get("liquidity_bucket") == "high_liquidity" and ordinal % 3 == 0:
        return "passive_limit_order"
    if row.get("liquidity_bucket") == "low_liquidity" and ordinal % 4 == 0:
        return "partial_fill"
    if ordinal % 7 == 0:
        return "cancel_replace"
    if ordinal % 2 == 0:
        return "marketable_limit_order"
    return "market_order"


def build_order_trace(trades: pd.DataFrame, max_per_strategy_profile: int = 240) -> pd.DataFrame:
    sample = _sample_events(trades, max_per_strategy_profile=max_per_strategy_profile)
    sample = sample.reset_index(drop=True)
    sample["order_id"] = np.arange(1, len(sample) + 1, dtype=np.int64)
    sample["event_sequence"] = sample["order_id"] * 10
    sample["signal_event_sequence"] = sample["event_sequence"]
    sample["submit_event_sequence"] = sample["event_sequence"] + 1
    sample["arrival_event_sequence"] = sample["event_sequence"] + np.where(sample["execution_profile"].eq("zero_latency_spread_only_control"), 1, 2)
    sample["mark_event_sequence"] = sample["arrival_event_sequence"] + 1
    sample["signal_age_events"] = sample["arrival_event_sequence"] - sample["signal_event_sequence"]
    sample["order_model"] = [_order_model_for_row(row, idx) for idx, row in sample.iterrows()]
    sample["slippage_model"] = np.select(
        [
            sample["order_model"].eq("passive_limit_order"),
            sample["order_model"].eq("rejection_scenario"),
            sample["order_model"].eq("partial_fill"),
        ],
        [
            "passive_queue_adverse_selection",
            "stale_reject",
            "depth_consuming_book_walk",
        ],
        default="spread_cross",
    )
    sample["requested_qty"] = 1.0
    sample["price_band_breach"] = sample["spread_ticks"].astype(float) >= 12
    sample["stale_signal"] = sample["signal_age_events"] > 3
    sample["reject_reason"] = np.select(
        [
            sample["order_model"].eq("rejection_scenario"),
            sample["price_band_breach"] & sample["order_model"].isin(["marketable_limit_order", "cancel_replace"]),
        ],
        [
            "scenario_rejection_or_stale_feed_proxy",
            "arrival_price_band_breach_proxy",
        ],
        default="",
    )
    sample["order_status"] = np.where(sample["reject_reason"].ne(""), "REJECTED_OR_CANCELLED", "FILLED")
    passive = sample["order_model"].eq("passive_limit_order")
    partial = sample["order_model"].eq("partial_fill")
    fill_ratio = pd.Series(1.0, index=sample.index)
    fill_ratio.loc[passive] = np.where(sample.loc[passive, "liquidity_bucket"].eq("high_liquidity"), 0.65, 0.35)
    fill_ratio.loc[partial] = np.where(sample.loc[partial, "liquidity_bucket"].eq("low_liquidity"), 0.45, 0.70)
    fill_ratio.loc[sample["order_status"].ne("FILLED")] = 0.0
    sample["fill_ratio"] = fill_ratio.clip(lower=0.0, upper=1.0)
    sample["filled_qty"] = sample["requested_qty"] * sample["fill_ratio"]
    passive_spread_credit = np.where(passive, sample["cost_return"].astype(float) * 0.35, 0.0)
    passive_adverse_haircut = np.where(passive, sample["local_volatility_6"].fillna(0).astype(float) * 0.10, 0.0)
    sample["event_gross_return"] = sample["gross_return"].astype(float) - passive_adverse_haircut
    sample["event_cost_return"] = np.maximum(sample["cost_return"].astype(float) - passive_spread_credit, 0.0)
    sample["event_net_return"] = np.where(
        sample["order_status"].eq("FILLED"),
        (sample["event_gross_return"] - sample["event_cost_return"]) * sample["fill_ratio"],
        0.0,
    )
    sample["position_delta_units"] = sample["side"].astype(float) * sample["filled_qty"]
    sample["direct_queue_truth"] = False
    sample["event_engine_scope"] = "sampled_phase12_trade_event_lifecycle_proxy"
    return sample[
        [
            "order_id",
            "strategy_id",
            "execution_profile",
            "feed_profile",
            "trade_date",
            "scenario_day",
            "symbol",
            "bar_index",
            "signal_event_sequence",
            "submit_event_sequence",
            "arrival_event_sequence",
            "mark_event_sequence",
            "signal_age_events",
            "side",
            "order_model",
            "slippage_model",
            "requested_qty",
            "filled_qty",
            "fill_ratio",
            "order_status",
            "reject_reason",
            "spread_ticks",
            "liquidity_bucket",
            "volatility_bucket",
            "event_gross_return",
            "event_cost_return",
            "event_net_return",
            "position_delta_units",
            "direct_queue_truth",
            "event_engine_scope",
        ]
    ]


def summarize_orders(trace: pd.DataFrame) -> pd.DataFrame:
    return (
        trace.groupby(["order_model", "order_status"], sort=True)
        .agg(
            orders=("order_id", "count"),
            mean_fill_ratio=("fill_ratio", "mean"),
            total_filled_qty=("filled_qty", "sum"),
            mean_event_net_return=("event_net_return", "mean"),
            total_event_net_pnl_units=("event_net_return", "sum"),
        )
        .reset_index()
    )


def build_pnl_trace(trace: pd.DataFrame) -> pd.DataFrame:
    ordered = trace.sort_values(["strategy_id", "execution_profile", "trade_date", "feed_profile", "symbol", "bar_index"], kind="mergesort").copy()
    group_cols = ["strategy_id", "execution_profile", "order_model"]
    ordered["running_position_units"] = ordered.groupby(group_cols, sort=False)["position_delta_units"].cumsum()
    ordered["running_net_pnl_units"] = ordered.groupby(group_cols, sort=False)["event_net_return"].cumsum()
    ordered["running_peak_pnl_units"] = ordered.groupby(group_cols, sort=False)["running_net_pnl_units"].cummax()
    ordered["running_drawdown_units"] = ordered["running_net_pnl_units"] - ordered["running_peak_pnl_units"]
    return ordered[
        [
            "order_id",
            "strategy_id",
            "execution_profile",
            "order_model",
            "symbol",
            "running_position_units",
            "running_net_pnl_units",
            "running_drawdown_units",
        ]
    ]


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    text = frame.copy()
    for column in text.columns:
        text[column] = text[column].map(lambda value: "" if pd.isna(value) else (f"{value:.6g}" if isinstance(value, float) else str(value)))
    headers = [str(column) for column in text.columns]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |" for row in text.values.tolist())
    return "\n".join(lines)


def write_report(output_dir: Path, trace: pd.DataFrame, summary: pd.DataFrame) -> None:
    model_counts = trace["order_model"].value_counts().rename_axis("order_model").reset_index(name="orders")
    lines = [
        "# Phase 12 Event-Driven Backtester Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This artifact exercises an event-driven order lifecycle over the Phase 12 sampled trade ledger.",
        "It covers market orders, marketable limits, passive-limit proxies, cancel/replace, partial fills and rejection scenarios.",
        "It is still proxy evidence: no individual exchange order identity, queue priority or passive-fill truth is claimed.",
        "",
        "## Order Model Counts",
        "",
        _markdown_table(model_counts),
        "",
        "## Order Summary",
        "",
        _markdown_table(summary),
        "",
        "## Outputs",
        "",
        "- `event_backtest_order_trace.parquet` (local/generated analytical trace)",
        "- `event_backtest_order_summary.csv`",
        "- `event_backtest_pnl_trace.csv`",
        "- `order_model_catalog.csv`",
        "- `slippage_model_catalog.csv`",
        "- `event_backtest_manifest.json`",
        "",
    ]
    (output_dir / "event_backtest_report.md").write_text("\n".join(lines), encoding="utf-8")


def run(trade_sample_path: Path, output_dir: Path, max_per_strategy_profile: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    trades = load_trade_sample(trade_sample_path)
    trace = build_order_trace(trades, max_per_strategy_profile=max_per_strategy_profile)
    summary = summarize_orders(trace)
    pnl = build_pnl_trace(trace)
    trace_path = output_dir / "event_backtest_order_trace.parquet"
    summary_path = output_dir / "event_backtest_order_summary.csv"
    pnl_path = output_dir / "event_backtest_pnl_trace.csv"
    order_model_path = output_dir / "order_model_catalog.csv"
    slippage_model_path = output_dir / "slippage_model_catalog.csv"
    report_path = output_dir / "event_backtest_report.md"
    pq.write_table(pa.Table.from_pandas(trace, preserve_index=False), trace_path, compression="zstd")
    summary.to_csv(summary_path, index=False)
    pnl.to_csv(pnl_path, index=False)
    pd.DataFrame(ORDER_MODELS, columns=["order_model", "description"]).to_csv(order_model_path, index=False)
    pd.DataFrame(SLIPPAGE_MODELS, columns=["slippage_model", "description"]).to_csv(slippage_model_path, index=False)
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "trade_sample_path": str(trade_sample_path),
        "input_trade_sample_rows": int(len(trades)),
        "order_trace_rows": int(len(trace)),
        "order_models": int(trace["order_model"].nunique()),
        "slippage_models": int(trace["slippage_model"].nunique()),
        "strategies": int(trace["strategy_id"].nunique()),
        "execution_profiles": int(trace["execution_profile"].nunique()),
        "filled_orders": int((trace["order_status"] == "FILLED").sum()),
        "rejected_or_cancelled_orders": int((trace["order_status"] == "REJECTED_OR_CANCELLED").sum()),
        "passive_limit_orders": int((trace["order_model"] == "passive_limit_order").sum()),
        "market_or_marketable_orders": int(trace["order_model"].isin(["market_order", "marketable_limit_order"]).sum()),
        "partial_fill_orders": int((trace["fill_ratio"].between(0, 1, inclusive="neither")).sum()),
        "direct_queue_truth": False,
        "not_acceptance_grade": True,
        "scope": "event_driven_order_lifecycle_proxy_over_phase12_trade_sample",
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase12_event_backtest",
            generated_utc=generated_utc,
            inputs={"trade_sample_path": str(trade_sample_path)},
            parameters={
                "max_per_strategy_profile": max_per_strategy_profile,
                "order_models": [model for model, _description in ORDER_MODELS],
                "slippage_models": [model for model, _description in SLIPPAGE_MODELS],
            },
            outputs={
                "order_trace": str(trace_path),
                "order_summary": str(summary_path),
                "pnl_trace": str(pnl_path),
                "order_model_catalog": str(order_model_path),
                "slippage_model_catalog": str(slippage_model_path),
                "report": str(report_path),
            },
            scenario_ids="phase12_trade_sample_strategy_execution_profile_cross_section",
            cost_model_version="zerodha_equity_intraday_nse_round_trip_bps_v1",
            latency_model_version="phase12_execution_profiles_v1",
        )
    )
    (output_dir / "event_backtest_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, trace, summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 12 event-driven order lifecycle backtest proxy artifacts.")
    parser.add_argument("--trade-sample", type=Path, default=Path("outputs/phase12/trade_ledger_sample.parquet"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase12"))
    parser.add_argument("--max-per-strategy-profile", type=int, default=240)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run(args.trade_sample, args.output_dir, args.max_per_strategy_profile)


if __name__ == "__main__":
    main()
