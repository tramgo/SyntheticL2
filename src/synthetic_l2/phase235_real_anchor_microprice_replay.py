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
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import (
    ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
    calculate_equity_intraday_nse_charges,
)


DEFAULT_PHASE176_INVENTORY = Path("outputs/phase176/phase176_feature_partition_inventory.csv")
DEFAULT_PHASE234_DIR = Path("outputs/phase234")
DEFAULT_OUTPUT_DIR = Path("outputs/phase235")
SOURCE_HORIZON_SEC = 15
SOURCE_BUCKETS_PER_EVENT_BAR = 10
RANDOM_CONTROL_RUNS = 100
RANDOM_SEED = 235


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns or "value" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def load_candidate(phase234_dir: Path) -> dict[str, Any]:
    handoff = read_csv(phase234_dir / "phase234_candidate_handoff.csv")
    if handoff.empty:
        raise FileNotFoundError(phase234_dir / "phase234_candidate_handoff.csv")
    return handoff.iloc[0].to_dict()


def load_source_features(inventory_path: Path, horizon_sec: int = SOURCE_HORIZON_SEC) -> pd.DataFrame:
    inventory = read_csv(inventory_path)
    if inventory.empty:
        raise FileNotFoundError(inventory_path)
    selected = inventory[inventory["horizon_sec"].astype(int).eq(horizon_sec)].copy()
    frames: list[pd.DataFrame] = []
    columns = [
        "bucket_ms",
        "receive_event_count",
        "quote_churn_count",
        "depth_refresh_count",
        "stale_quote_duration_ms",
        "last_price",
        "best_bid",
        "best_ask",
        "spread",
        "l1_qty_imbalance",
        "top5_qty_imbalance",
        "trade_date",
        "exchange",
        "symbol",
        "horizon_sec",
    ]
    for row in selected.to_dict("records"):
        path = Path(str(row["parquet_file"]))
        if not path.exists():
            continue
        part = pd.read_parquet(path, columns=columns)
        frames.append(part)
    if not frames:
        raise FileNotFoundError("No Phase176 source feature parquet files found for Phase235")
    frame = pd.concat(frames, ignore_index=True)
    frame = frame.sort_values(["trade_date", "symbol", "bucket_ms"], kind="mergesort").reset_index(drop=True)
    return frame


def materialize_event_bars(features: pd.DataFrame, buckets_per_event_bar: int = SOURCE_BUCKETS_PER_EVENT_BAR) -> pd.DataFrame:
    frame = features.copy()
    frame["mid_price"] = (frame["best_bid"].astype(float) + frame["best_ask"].astype(float)) / 2.0
    frame["spread"] = frame["spread"].astype(float)
    frame["microprice_dev"] = (
        (frame["spread"] / 2.0)
        * frame["l1_qty_imbalance"].astype(float)
        / frame["mid_price"].replace(0, np.nan).astype(float)
    )
    frame["valid_book"] = (
        frame["mid_price"].gt(0)
        & frame["spread"].ge(0)
        & frame["l1_qty_imbalance"].notna()
        & frame["top5_qty_imbalance"].notna()
    )
    frame = frame[frame["valid_book"]].copy()
    frame["source_bucket_index"] = frame.groupby(["trade_date", "symbol"], sort=False).cumcount()
    frame["source_event_bar_id"] = (frame["source_bucket_index"] // buckets_per_event_bar).astype(int)

    grouped = frame.groupby(["trade_date", "exchange", "symbol", "source_event_bar_id"], sort=True)
    bars = grouped.agg(
        source_buckets_in_bar=("bucket_ms", "size"),
        source_events_in_bar=("receive_event_count", "sum"),
        first_bucket_ms=("bucket_ms", "first"),
        last_bucket_ms=("bucket_ms", "last"),
        open_mid_price=("mid_price", "first"),
        close_mid_price=("mid_price", "last"),
        avg_spread=("spread", "mean"),
        avg_l1_imbalance=("l1_qty_imbalance", "mean"),
        avg_top5_market_by_price_imbalance=("top5_qty_imbalance", "mean"),
        avg_microprice_dev=("microprice_dev", "mean"),
        avg_event_intensity_proxy=("receive_event_count", "sum"),
        quote_churn_count=("quote_churn_count", "sum"),
        depth_refresh_count=("depth_refresh_count", "sum"),
        stale_quote_duration_ms=("stale_quote_duration_ms", "sum"),
    ).reset_index()
    bars["trade_month"] = bars["trade_date"].astype(str).str.slice(0, 7)
    bars["bar_return"] = bars["close_mid_price"] / bars["open_mid_price"].replace(0, np.nan) - 1.0
    charges = calculate_equity_intraday_nse_charges(
        buy_value_inr=DEFAULT_ORDER_NOTIONAL_INR,
        sell_value_inr=DEFAULT_ORDER_NOTIONAL_INR,
        buy_quantity=1.0,
        sell_quantity=1.0,
        buy_orders=1,
        sell_orders=1,
    )
    bars["zerodha_round_trip_charge_bps"] = float(charges.breakeven_bps_on_buy_value)
    bars["spread_bps"] = bars["avg_spread"] / bars["close_mid_price"].replace(0, np.nan) * 10000.0
    bars["taker_round_trip_cost_floor_bps"] = bars["spread_bps"] + bars["zerodha_round_trip_charge_bps"]
    bars["abs_bar_return_bps"] = bars["bar_return"].abs() * 10000.0
    bars["event_window_score"] = (
        bars["abs_bar_return_bps"]
        * np.log1p(bars["avg_event_intensity_proxy"].clip(lower=0).astype(float))
        / bars["taker_round_trip_cost_floor_bps"].replace(0, np.nan).astype(float)
    )
    bars = bars.replace([np.inf, -np.inf], np.nan).dropna(
        subset=["close_mid_price", "avg_microprice_dev", "event_window_score", "taker_round_trip_cost_floor_bps"]
    )
    return bars.sort_values(["trade_date", "symbol", "source_event_bar_id"], kind="mergesort").reset_index(drop=True)


def replay_candidate(bars: pd.DataFrame, candidate: dict[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame]:
    horizon = as_int(candidate.get("horizon_event_bars", 3), 3)
    event_threshold = as_float(candidate.get("event_window_score_threshold", 0.0), 0.0)
    micro_threshold = as_float(candidate.get("abs_microprice_dev_threshold", 0.0), 0.0)
    frame = bars.copy()
    frame[f"future_return_h{horizon}"] = (
        frame.groupby(["trade_date", "symbol"], sort=False)["close_mid_price"].shift(-horizon)
        / frame["close_mid_price"]
        - 1.0
    )
    selected = frame[
        frame[f"future_return_h{horizon}"].notna()
        & frame["event_window_score"].ge(event_threshold)
        & frame["avg_microprice_dev"].abs().ge(micro_threshold)
    ].copy()
    selected["side"] = -np.sign(selected["avg_microprice_dev"].astype(float))
    selected = selected[selected["side"].ne(0)].copy()
    selected["candidate_id"] = str(candidate.get("candidate_id", ""))
    selected["horizon_event_bars"] = horizon
    selected["gross_return"] = selected["side"] * selected[f"future_return_h{horizon}"].astype(float)
    selected["cost_return"] = selected["taker_round_trip_cost_floor_bps"].astype(float) / 10000.0
    selected["net_return"] = selected["gross_return"] - selected["cost_return"]
    selected["gross_pnl_inr"] = selected["gross_return"] * DEFAULT_ORDER_NOTIONAL_INR
    selected["cost_pnl_drag_inr"] = selected["cost_return"] * DEFAULT_ORDER_NOTIONAL_INR
    selected["net_pnl_inr"] = selected["net_return"] * DEFAULT_ORDER_NOTIONAL_INR
    keep = [
        "candidate_id",
        "trade_month",
        "trade_date",
        "exchange",
        "symbol",
        "source_event_bar_id",
        "horizon_event_bars",
        "side",
        "event_window_score",
        "avg_microprice_dev",
        "avg_l1_imbalance",
        "avg_top5_market_by_price_imbalance",
        "close_mid_price",
        "taker_round_trip_cost_floor_bps",
        f"future_return_h{horizon}",
        "gross_return",
        "cost_return",
        "net_return",
        "gross_pnl_inr",
        "cost_pnl_drag_inr",
        "net_pnl_inr",
    ]
    return selected[keep], frame


def summarize_replay(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame(
            [
                {
                    "candidate_id": "",
                    "real_anchor_trades": 0,
                    "real_anchor_net_pnl_inr": 0.0,
                    "real_anchor_gross_pnl_inr": 0.0,
                    "real_anchor_cost_pnl_drag_inr": 0.0,
                    "real_anchor_positive_dates": 0,
                    "real_anchor_dates": 0,
                    "real_anchor_symbols": 0,
                    "real_anchor_min_date_net_pnl_inr": 0.0,
                    "real_anchor_leave_one_date_min_net_pnl_inr": 0.0,
                    "real_anchor_max_date_contribution_abs": np.nan,
                    "real_anchor_max_symbol_contribution_abs": np.nan,
                    "real_anchor_precision_cost_clear": 0.0,
                }
            ]
        )
    net = float(trades["net_pnl_inr"].sum())
    date_net = trades.groupby("trade_date", sort=True)["net_pnl_inr"].sum()
    symbol_net = trades.groupby("symbol", sort=True)["net_pnl_inr"].sum()
    leave_one = [net - float(value) for value in date_net.to_list()]
    denom = abs(net) if abs(net) > 0 else np.nan
    return pd.DataFrame(
        [
            {
                "candidate_id": trades["candidate_id"].iloc[0],
                "real_anchor_trades": int(len(trades)),
                "real_anchor_net_pnl_inr": net,
                "real_anchor_gross_pnl_inr": float(trades["gross_pnl_inr"].sum()),
                "real_anchor_cost_pnl_drag_inr": float(trades["cost_pnl_drag_inr"].sum()),
                "real_anchor_positive_dates": int((date_net > 0).sum()),
                "real_anchor_dates": int(date_net.shape[0]),
                "real_anchor_symbols": int(trades["symbol"].nunique()),
                "real_anchor_min_date_net_pnl_inr": float(date_net.min()),
                "real_anchor_leave_one_date_min_net_pnl_inr": float(min(leave_one)) if leave_one else 0.0,
                "real_anchor_max_date_contribution_abs": float(date_net.abs().max() / denom) if denom and not np.isnan(denom) else np.nan,
                "real_anchor_max_symbol_contribution_abs": float(symbol_net.abs().max() / denom) if denom and not np.isnan(denom) else np.nan,
                "real_anchor_precision_cost_clear": float((trades["net_return"] > 0).mean()),
            }
        ]
    )


def build_controls(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame(
            [
                {"control_id": "SIDE_FLIP", "net_pnl_inr": 0.0, "passed": False},
                {"control_id": "RANDOM_SIDE_100_RUNS", "net_pnl_inr": 0.0, "passed": False},
                {"control_id": "COST_150", "net_pnl_inr": 0.0, "passed": False},
                {"control_id": "COST_200", "net_pnl_inr": 0.0, "passed": False},
            ]
        )
    base_gross = trades["gross_pnl_inr"].to_numpy(dtype=float)
    cost = trades["cost_pnl_drag_inr"].to_numpy(dtype=float)
    side_flip_net = float((-base_gross - cost).sum())
    rng = np.random.default_rng(RANDOM_SEED)
    abs_future = np.abs(trades["gross_return"].to_numpy(dtype=float)) * DEFAULT_ORDER_NOTIONAL_INR
    random_nets = []
    for _ in range(RANDOM_CONTROL_RUNS):
        random_side = rng.choice([-1.0, 1.0], size=len(trades))
        random_nets.append(float((random_side * abs_future - cost).sum()))
    random_nets_arr = np.asarray(random_nets)
    base_net = float(trades["net_pnl_inr"].sum())
    rows = [
        {"control_id": "SIDE_FLIP", "net_pnl_inr": side_flip_net, "passed": bool(side_flip_net < 0)},
        {
            "control_id": "RANDOM_SIDE_100_RUNS",
            "net_pnl_inr": base_net,
            "random_p95_net_pnl_inr": float(np.quantile(random_nets_arr, 0.95)),
            "random_beat_fraction": float((base_net > random_nets_arr).mean()),
            "passed": bool((base_net > random_nets_arr).mean() >= 0.95),
        },
        {
            "control_id": "COST_150",
            "net_pnl_inr": float((base_gross - 1.5 * cost).sum()),
            "passed": bool((base_gross - 1.5 * cost).sum() > 0),
        },
        {
            "control_id": "COST_200",
            "net_pnl_inr": float((base_gross - 2.0 * cost).sum()),
            "passed": bool((base_gross - 2.0 * cost).sum() > 0),
        },
    ]
    return pd.DataFrame(rows)


def summarize_event_bar_coverage(bars: pd.DataFrame) -> pd.DataFrame:
    if bars.empty:
        return pd.DataFrame(
            columns=[
                "trade_date",
                "symbols",
                "real_event_bars",
                "min_symbol_event_bars",
                "median_symbol_event_bars",
                "max_symbol_event_bars",
            ]
        )
    by_symbol = bars.groupby(["trade_date", "symbol"], sort=True).size().reset_index(name="event_bars")
    return (
        by_symbol.groupby("trade_date", sort=True)
        .agg(
            symbols=("symbol", "nunique"),
            real_event_bars=("event_bars", "sum"),
            min_symbol_event_bars=("event_bars", "min"),
            median_symbol_event_bars=("event_bars", "median"),
            max_symbol_event_bars=("event_bars", "max"),
        )
        .reset_index()
    )


def build_gate_evaluation(summary: pd.DataFrame, controls: pd.DataFrame) -> pd.DataFrame:
    row = summary.iloc[0].to_dict() if not summary.empty else {}
    trades = as_int(row.get("real_anchor_trades", 0), 0)
    net = as_float(row.get("real_anchor_net_pnl_inr", 0.0), 0.0)
    dates = as_int(row.get("real_anchor_dates", 0), 0)
    symbols = as_int(row.get("real_anchor_symbols", 0), 0)
    control_passes = int(controls["passed"].astype(bool).sum()) if not controls.empty else 0
    rows = [
        ("P235_REAL_EVENT_BARS_MATERIALIZED", trades > 0, trades, ">0 candidate trades after materialization", "hard"),
        ("P235_REAL_ANCHOR_NET_POSITIVE", net > 0, net, ">0 real-anchor net P&L after costs", "hard"),
        ("P235_REAL_ANCHOR_DATE_BREADTH", dates >= 3, dates, ">=3 real dates represented in selected trades", "hard"),
        ("P235_REAL_ANCHOR_SYMBOL_BREADTH", symbols >= 5, symbols, ">=5 symbols represented in selected trades", "hard"),
        ("P235_CONTROLS_PASS", control_passes >= 3, control_passes, ">=3 / 4 controls pass", "hard"),
        ("P235_NO_PAPER_LIVE_OR_PROMOTION_UNLOCK", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase235 Real-anchor Microprice-reversal Replay Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase235 uses tick-derived Phase176 15-second real receive-flow features, aggregates 10 source buckets per event bar, and replays the frozen Phase234/Phase233 microprice-reversal candidate.",
        "It is a local real-anchor dry run only: no paper/live acceptance, no parameter tuning on real data, and no deployable profitability claim.",
        "",
    ]
    for title, table in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(table), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    inventory_path: Path = DEFAULT_PHASE176_INVENTORY,
    phase234_dir: Path = DEFAULT_PHASE234_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    candidate = load_candidate(phase234_dir)
    source_features = load_source_features(inventory_path)
    bars = materialize_event_bars(source_features)
    trades, labeled_bars = replay_candidate(bars, candidate)
    summary = summarize_replay(trades)
    controls = build_controls(trades)
    coverage = summarize_event_bar_coverage(bars)
    gates = build_gate_evaluation(summary, controls)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    hard_rows = int(len(hard))
    real_pass = int(hard_pass == hard_rows and not hard.empty)
    next_action = (
        "run_phase236_expand_real_anchor_microprice_candidate_validation_no_paper_live"
        if real_pass
        else "run_phase236_close_or_redesign_microprice_reversal_after_real_anchor_failure_no_paper_live"
    )
    acceptance = pd.DataFrame(
        [
            ("phase235_real_anchor_microprice_replay_complete", 1, "Phase235 real-anchor replay completed"),
            ("phase235_parent_candidate_id", candidate.get("candidate_id", ""), "Candidate carried forward from Phase234"),
            ("phase235_source_horizon_sec", SOURCE_HORIZON_SEC, "Phase176 source feature horizon used"),
            ("phase235_source_buckets_per_event_bar", SOURCE_BUCKETS_PER_EVENT_BAR, "Source buckets aggregated per real event bar"),
            ("phase235_source_feature_rows", int(len(source_features)), "Phase176 real source feature rows loaded"),
            ("phase235_real_event_bar_rows", int(len(bars)), "Real event bars materialized"),
            ("phase235_real_anchor_trade_rows", as_int(summary["real_anchor_trades"].iloc[0], 0), "Frozen candidate trades selected on real-anchor bars"),
            ("phase235_real_anchor_net_pnl_inr", as_float(summary["real_anchor_net_pnl_inr"].iloc[0], 0.0), "Real-anchor net P&L after cost floor"),
            ("phase235_real_anchor_dates", as_int(summary["real_anchor_dates"].iloc[0], 0), "Real dates represented in selected trades"),
            ("phase235_real_anchor_symbols", as_int(summary["real_anchor_symbols"].iloc[0], 0), "Symbols represented in selected trades"),
            ("phase235_control_pass_rows", int(controls["passed"].astype(bool).sum()) if not controls.empty else 0, "Controls passed"),
            ("phase235_control_rows", int(len(controls)), "Controls evaluated"),
            ("phase235_hard_gate_pass_rows", hard_pass, "Hard Phase235 gates passed"),
            ("phase235_hard_gate_rows", hard_rows, "Hard Phase235 gates evaluated"),
            ("phase235_real_anchor_replay_pass", real_pass, "Whether the frozen candidate passed the real-anchor dry run"),
            ("phase235_strategy_promotion_allowed", 0, "No strategy promotion from Phase235"),
            ("phase235_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase235"),
            ("phase235_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase235"),
            ("phase235_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )

    bars.to_parquet(output_dir / "phase235_real_event_bars.parquet", index=False)
    labeled_bars.to_parquet(output_dir / "phase235_labeled_real_event_bars.parquet", index=False)
    trades.to_parquet(output_dir / "phase235_real_anchor_trade_ledger.parquet", index=False)
    trades.to_csv(output_dir / "phase235_real_anchor_trade_ledger.csv", index=False)
    coverage.to_csv(output_dir / "phase235_real_event_bar_coverage.csv", index=False)
    summary.to_csv(output_dir / "phase235_real_anchor_replay_summary.csv", index=False)
    controls.to_csv(output_dir / "phase235_control_summary.csv", index=False)
    gates.to_csv(output_dir / "phase235_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase235_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase235_real_anchor_microprice_replay_report.md",
        {
            "Acceptance Summary": acceptance,
            "Replay Summary": summary,
            "Real Event-bar Coverage": coverage,
            "Controls": controls,
            "Gate Evaluation": gates,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase235_real_anchor_microprice_reversal_replay",
        **reproducibility_fields(
            artifact_id="phase235",
            generated_utc=generated_utc,
            inputs={
                "phase176_inventory": str(inventory_path),
                "phase234_candidate_handoff": str(phase234_dir / "phase234_candidate_handoff.csv"),
            },
            parameters={
                "source_horizon_sec": SOURCE_HORIZON_SEC,
                "source_buckets_per_event_bar": SOURCE_BUCKETS_PER_EVENT_BAR,
                "random_control_runs": RANDOM_CONTROL_RUNS,
                "random_seed": RANDOM_SEED,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "real_event_bars": str(output_dir / "phase235_real_event_bars.parquet"),
                "labeled_real_event_bars": str(output_dir / "phase235_labeled_real_event_bars.parquet"),
                "real_anchor_trade_ledger": str(output_dir / "phase235_real_anchor_trade_ledger.parquet"),
                "real_anchor_trade_ledger_csv": str(output_dir / "phase235_real_anchor_trade_ledger.csv"),
                "real_event_bar_coverage": str(output_dir / "phase235_real_event_bar_coverage.csv"),
                "replay_summary": str(output_dir / "phase235_real_anchor_replay_summary.csv"),
                "control_summary": str(output_dir / "phase235_control_summary.csv"),
                "gate_evaluation": str(output_dir / "phase235_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase235_acceptance_summary.csv"),
                "report": str(output_dir / "phase235_real_anchor_microprice_replay_report.md"),
            },
            random_seed=RANDOM_SEED,
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase176_receive_flow_tick_derived_15s_source_bucket_adapter",
        ),
    }
    (output_dir / "phase235_real_anchor_microprice_replay_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase235 real-anchor microprice-reversal replay.")
    parser.add_argument("--inventory-path", type=Path, default=DEFAULT_PHASE176_INVENTORY)
    parser.add_argument("--phase234-dir", type=Path, default=DEFAULT_PHASE234_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(inventory_path=args.inventory_path, phase234_dir=args.phase234_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
