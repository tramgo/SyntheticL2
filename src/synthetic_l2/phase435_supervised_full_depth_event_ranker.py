from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase428_broader_full_depth_feature_family_sweep import (
    DEFAULT_RAW_ROOT,
    DEFAULT_REAL_ROOTS,
    load_real_anchor_ticks,
    load_synthetic_ticks,
    prepare_group_features,
    score_trade,
)
from synthetic_l2.phase427_broader_full_depth_feature_family_precommit import (
    ANNUALIZED_THRESHOLD_PCT,
    COST_MULTIPLIER,
    INITIAL_CAPITAL_INR,
    MIN_COMPLETED_ROUND_TRIPS,
    MIN_POSITIVE_DATE_FRACTION,
    MIN_SYMBOLS,
    MIN_TRADE_DATES,
    ORDER_NOTIONAL_INR,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE434_DIR = Path("outputs/phase434")
DEFAULT_OUTPUT_DIR = Path("outputs/phase435")

THESIS_ID = "P435_SUPERVISED_FULL_DEPTH_EVENT_RANKER_EXECUTION"
PHASE434_NEXT_ACTION = "run_phase435_supervised_full_depth_event_ranker_no_paper_live"
NEXT_ACTION = "interpret_phase435_supervised_full_depth_event_ranker_no_paper_live"

LOOKBACK_TICKS = 60
FORWARD_TICKS = 3
MIN_HOLD_MS = 250.0
MAX_HOLD_TICKS_SYNTHETIC = 2500
MAX_HOLD_TICKS_REAL = 500
SYNTHETIC_SCAN_STRIDE = 25
REAL_SCAN_STRIDE = 5
MAX_EVENTS_PER_SYMBOL_DATE = 120
TOP_K_PER_SYMBOL_DATE = 8

FULL_DEPTH_FEATURES = [
    "l2_l5_imbalance",
    "top5_imbalance",
    "book_slope",
    "bid_depth_change",
    "ask_depth_change",
    "total_depth_change",
    "order_churn",
    "spread_change",
    "book_slope_change",
]
L1_ONLY_FEATURES = ["l1_imbalance", "spread_bps_feature", "microtrend_bps"]
ALL_FEATURES = L1_ONLY_FEATURES + FULL_DEPTH_FEATURES


def fixed_quantity(price: float) -> int:
    return max(1, int(math.floor(ORDER_NOTIONAL_INR / max(float(price), 0.01))))


def exact_exit_index(group: pd.DataFrame, entry_idx: int, max_hold_ticks: int) -> tuple[int | None, int, float]:
    max_idx = min(len(group) - 1, entry_idx + int(max_hold_ticks))
    for j in range(entry_idx + FORWARD_TICKS, max_idx + 1):
        hold_ms = float(group.iloc[j]["exchange_timestamp_ms"]) - float(group.iloc[entry_idx]["exchange_timestamp_ms"])
        if hold_ms >= MIN_HOLD_MS:
            return j, j - entry_idx, hold_ms
    return None, 0, 0.0


def feature_delta(now: pd.Series, base: pd.Series) -> dict[str, float]:
    bid_base = float(base["l2_l5_bid_qty"])
    bid_now = float(now["l2_l5_bid_qty"])
    ask_base = float(base["l2_l5_ask_qty"])
    ask_now = float(now["l2_l5_ask_qty"])
    orders_base = float(base["l2_l5_bid_orders"] + base["l2_l5_ask_orders"])
    orders_now = float(now["l2_l5_bid_orders"] + now["l2_l5_ask_orders"])
    depth_base = bid_base + ask_base
    depth_now = bid_now + ask_now
    return {
        "bid_depth_change": (bid_now - bid_base) / max(1.0, bid_base),
        "ask_depth_change": (ask_now - ask_base) / max(1.0, ask_base),
        "total_depth_change": (depth_now - depth_base) / max(1.0, depth_base),
        "order_churn": abs(orders_now - orders_base) / max(1.0, orders_base),
        "spread_change": float(now["spread_bps_feature"] - base["spread_bps_feature"]),
        "book_slope_change": float(now["book_slope"] - base["book_slope"]),
        "microtrend_bps": (float(now["mid"]) / max(0.01, float(base["mid"])) - 1.0) * 10_000.0,
    }


def build_events(ticks: pd.DataFrame, *, panel: str, max_hold_ticks: int, stride: int) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if ticks.empty:
        return pd.DataFrame()
    for (trade_date, symbol), raw_group in ticks.groupby(["trade_date", "symbol"], sort=True):
        group = prepare_group_features(raw_group)
        if len(group) <= LOOKBACK_TICKS + FORWARD_TICKS + 2:
            continue
        kept = 0
        last_start = max(LOOKBACK_TICKS + 1, len(group) - FORWARD_TICKS - 2)
        for signal_idx in range(LOOKBACK_TICKS, last_start, stride):
            if kept >= MAX_EVENTS_PER_SYMBOL_DATE:
                break
            entry_idx = signal_idx + 1
            exit_idx, actual_forward, hold_ms = exact_exit_index(group, entry_idx, max_hold_ticks)
            if exit_idx is None:
                continue
            base = group.iloc[signal_idx - LOOKBACK_TICKS]
            now = group.iloc[signal_idx]
            entry = group.iloc[entry_idx]
            exit_row = group.iloc[exit_idx]
            long_entry = float(entry["sell_1_price"])
            long_exit = float(exit_row["buy_1_price"])
            short_entry = float(entry["buy_1_price"])
            short_exit = float(exit_row["sell_1_price"])
            long_qty = fixed_quantity(long_entry)
            short_qty = fixed_quantity(short_entry)
            long_score = score_trade(1, long_entry, long_exit, long_qty)
            short_score = score_trade(-1, short_entry, short_exit, short_qty)
            fd = feature_delta(now, base)
            rows.append(
                {
                    "panel": panel,
                    "trade_date": str(trade_date),
                    "symbol": str(symbol),
                    "signal_index": signal_idx,
                    "entry_index": entry_idx,
                    "exit_index": exit_idx,
                    "signal_ts_ms": float(now["exchange_timestamp_ms"]),
                    "entry_ts_ms": float(entry["exchange_timestamp_ms"]),
                    "exit_ts_ms": float(exit_row["exchange_timestamp_ms"]),
                    "actual_forward_ticks_after_entry": actual_forward,
                    "hold_ms": hold_ms,
                    "l1_imbalance": float(now["l1_imbalance"]),
                    "l2_l5_imbalance": float(now["l2_l5_imbalance"]),
                    "top5_imbalance": float(now["top5_imbalance"]),
                    "spread_bps_feature": float(now["spread_bps_feature"]),
                    "book_slope": float(now["book_slope"]),
                    "long_entry_price": long_entry,
                    "long_exit_price": long_exit,
                    "short_entry_price": short_entry,
                    "short_exit_price": short_exit,
                    "long_net_pnl_inr": float(long_score["net_pnl_inr"]),
                    "short_net_pnl_inr": float(short_score["net_pnl_inr"]),
                    "long_gross_pnl_inr": float(long_score["gross_pnl_inr"]),
                    "short_gross_pnl_inr": float(short_score["gross_pnl_inr"]),
                    "long_cost200_inr": float(long_score["cost200_inr"]),
                    "short_cost200_inr": float(short_score["cost200_inr"]),
                    **fd,
                }
            )
            kept += 1
    events = pd.DataFrame(rows)
    if events.empty:
        return events
    events["best_side_int"] = np.where(events["long_net_pnl_inr"].ge(events["short_net_pnl_inr"]), 1, -1)
    events["best_net_pnl_inr"] = np.maximum(events["long_net_pnl_inr"], events["short_net_pnl_inr"])
    events["signed_label_inr"] = events["long_net_pnl_inr"] - events["short_net_pnl_inr"]
    return events


def split_dates(events: pd.DataFrame) -> tuple[list[str], list[str]]:
    dates = sorted(events["trade_date"].astype(str).unique().tolist())
    cut = max(1, len(dates) // 2)
    if cut >= len(dates):
        cut = max(1, len(dates) - 1)
    return dates[:cut], dates[cut:]


def fit_linear_ranker(train: pd.DataFrame, feature_cols: list[str]) -> pd.DataFrame:
    rows = []
    y = train["signed_label_inr"].astype(float)
    y_std = float(y.std(ddof=0))
    for col in feature_cols:
        x = train[col].astype(float).replace([np.inf, -np.inf], 0.0).fillna(0.0)
        x_std = float(x.std(ddof=0))
        if x_std <= 0 or y_std <= 0:
            weight = 0.0
        else:
            weight = float(np.corrcoef(x, y)[0, 1])
            if not np.isfinite(weight):
                weight = 0.0
        rows.append({"feature": col, "weight": weight, "mean": float(x.mean()), "std": max(x_std, 1e-9)})
    return pd.DataFrame(rows)


def apply_ranker(events: pd.DataFrame, weights: pd.DataFrame, score_col: str) -> pd.DataFrame:
    out = events.copy()
    score = np.zeros(len(out), dtype=float)
    for row in weights.itertuples(index=False):
        x = out[str(row.feature)].astype(float).replace([np.inf, -np.inf], 0.0).fillna(0.0)
        score += float(row.weight) * ((x - float(row.mean)) / float(row.std))
    out[score_col] = score
    return out


def select_and_score(events: pd.DataFrame, *, score_col: str, scenario_id: str, side_multiplier: int = 1, shuffle_scores: bool = False) -> pd.DataFrame:
    if events.empty:
        return pd.DataFrame()
    ranked = events.copy()
    if shuffle_scores:
        ranked[score_col] = ranked.groupby("trade_date")[score_col].transform(lambda s: s.sample(frac=1.0, random_state=435).to_numpy())
    ranked["model_side_int"] = np.where(ranked[score_col].ge(0), 1, -1) * int(side_multiplier)
    ranked["abs_score"] = ranked[score_col].abs()
    picks = (
        ranked.sort_values(["trade_date", "symbol", "abs_score"], ascending=[True, True, False])
        .groupby(["trade_date", "symbol"], sort=False)
        .head(TOP_K_PER_SYMBOL_DATE)
        .copy()
    )
    picks["scenario_id"] = scenario_id
    picks["side"] = np.where(picks["model_side_int"].gt(0), "long", "short")
    picks["entry_price"] = np.where(picks["model_side_int"].gt(0), picks["long_entry_price"], picks["short_entry_price"])
    picks["exit_price"] = np.where(picks["model_side_int"].gt(0), picks["long_exit_price"], picks["short_exit_price"])
    picks["gross_pnl_inr"] = np.where(picks["model_side_int"].gt(0), picks["long_gross_pnl_inr"], picks["short_gross_pnl_inr"])
    picks["cost200_inr"] = np.where(picks["model_side_int"].gt(0), picks["long_cost200_inr"], picks["short_cost200_inr"])
    picks["net_pnl_inr"] = np.where(picks["model_side_int"].gt(0), picks["long_net_pnl_inr"], picks["short_net_pnl_inr"])
    return picks


def summarize_trades(trades: pd.DataFrame, *, panel: str, scenario_id: str) -> dict[str, Any]:
    if trades.empty:
        return {
            "panel": panel,
            "scenario_id": scenario_id,
            "completed_round_trips": 0,
            "trade_dates": 0,
            "symbols": 0,
            "positive_date_fraction": 0.0,
            "gross_pnl_inr": 0.0,
            "cost200_inr": 0.0,
            "net_pnl_inr": 0.0,
            "annualized_return_pct": 0.0,
        }
    date_pnl = trades.groupby("trade_date")["net_pnl_inr"].sum()
    dates = int(trades["trade_date"].nunique())
    net = float(trades["net_pnl_inr"].sum())
    return {
        "panel": panel,
        "scenario_id": scenario_id,
        "completed_round_trips": int(len(trades)),
        "trade_dates": dates,
        "symbols": int(trades["symbol"].nunique()),
        "positive_date_fraction": float((date_pnl > 0).mean()) if len(date_pnl) else 0.0,
        "gross_pnl_inr": float(trades["gross_pnl_inr"].sum()),
        "cost200_inr": float(trades["cost200_inr"].sum()),
        "net_pnl_inr": net,
        "annualized_return_pct": float((net / INITIAL_CAPITAL_INR) * (252.0 / max(1, dates)) * 100.0),
    }


def build_gates(summary: pd.DataFrame, weights: pd.DataFrame, real_summary: pd.DataFrame) -> pd.DataFrame:
    primary = summary[summary["scenario_id"].eq("P435_full_depth_ranker_validation")].iloc[0]
    l1 = summary[summary["scenario_id"].eq("P435_l1_only_ablation_validation")].iloc[0]
    side = summary[summary["scenario_id"].eq("P435_side_flip_control_validation")].iloc[0]
    shuffle = summary[summary["scenario_id"].eq("P435_time_shuffle_control_validation")].iloc[0]
    real = real_summary[real_summary["scenario_id"].eq("P435_full_depth_ranker_real_anchor")].iloc[0] if not real_summary.empty else pd.Series(dtype=object)
    full_depth_weight_abs = float(weights[weights["feature"].isin(FULL_DEPTH_FEATURES)]["weight"].abs().sum())
    l1_weight_abs = float(weights[weights["feature"].isin(L1_ONLY_FEATURES)]["weight"].abs().sum())
    gates = [
        ("P435_PHASE434_PRECOMMIT_USED", True, PHASE434_NEXT_ACTION, "phase434_next_action"),
        ("P435_TRAIN_VALIDATION_SPLIT_PRESENT", int(primary.get("trade_dates", 0)) > 0, primary.get("trade_dates", 0), ">0 validation dates"),
        ("P435_FULL_DEPTH_FEATURE_WEIGHTS_NONZERO", full_depth_weight_abs > 0, full_depth_weight_abs, ">0"),
        ("P435_L2_L5_MATERIALITY_OVER_L1", float(primary["annualized_return_pct"]) - float(l1["annualized_return_pct"]) >= 5.0, float(primary["annualized_return_pct"]) - float(l1["annualized_return_pct"]), ">=5 pct pts"),
        ("P435_SIDE_FLIP_CONTROL_NOT_DOMINANT", float(primary["annualized_return_pct"]) >= float(side["annualized_return_pct"]), side["annualized_return_pct"], "primary>=side_flip"),
        ("P435_TIME_SHUFFLE_CONTROL_NOT_DOMINANT", float(primary["annualized_return_pct"]) >= float(shuffle["annualized_return_pct"]), shuffle["annualized_return_pct"], "primary>=time_shuffle"),
        ("P435_COST200_FIXED_CAPITAL", True, f"cost={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR};notional={ORDER_NOTIONAL_INR}", "cost200_fixed_capital"),
        ("P435_EVENT_FLOOR", int(primary["completed_round_trips"]) >= MIN_COMPLETED_ROUND_TRIPS, primary["completed_round_trips"], f">={MIN_COMPLETED_ROUND_TRIPS}"),
        ("P435_DATE_BREADTH", int(primary["trade_dates"]) >= MIN_TRADE_DATES, primary["trade_dates"], f">={MIN_TRADE_DATES}"),
        ("P435_SYMBOL_BREADTH", int(primary["symbols"]) >= MIN_SYMBOLS, primary["symbols"], f">={MIN_SYMBOLS}"),
        ("P435_POSITIVE_DATE_FRACTION", float(primary["positive_date_fraction"]) >= MIN_POSITIVE_DATE_FRACTION, primary["positive_date_fraction"], f">={MIN_POSITIVE_DATE_FRACTION}"),
        ("P435_ANNUALIZED_FLOOR", float(primary["annualized_return_pct"]) >= ANNUALIZED_THRESHOLD_PCT, primary["annualized_return_pct"], f">={ANNUALIZED_THRESHOLD_PCT}"),
        ("P435_REAL_ANCHOR_CROSS_CHECK", (float(primary["annualized_return_pct"]) == 0 and float(real.get("annualized_return_pct", 0)) == 0) or float(primary["annualized_return_pct"]) * float(real.get("annualized_return_pct", 0)) >= 0, real.get("annualized_return_pct", 0), "same_sign"),
        ("P435_BOUNDARIES_CLOSED", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(events: pd.DataFrame, summary: pd.DataFrame, gates: pd.DataFrame, real_summary: pd.DataFrame) -> pd.DataFrame:
    primary = summary[summary["scenario_id"].eq("P435_full_depth_ranker_validation")].iloc[0]
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    survivors = int(hard_pass == hard_rows)
    return pd.DataFrame(
        [
            ("phase435_supervised_full_depth_event_ranker_complete", 1, "Phase435 execution completed"),
            ("phase435_thesis_id", THESIS_ID, "Execution thesis"),
            ("phase435_synthetic_event_rows", len(events), "Synthetic event-label rows"),
            ("phase435_best_scenario_id", primary["scenario_id"], "Primary validation scenario"),
            ("phase435_best_completed_round_trips", primary["completed_round_trips"], "Primary completed round trips"),
            ("phase435_best_trade_dates", primary["trade_dates"], "Primary validation trade dates"),
            ("phase435_best_symbols", primary["symbols"], "Primary validation symbols"),
            ("phase435_best_positive_date_fraction", primary["positive_date_fraction"], "Primary positive-date fraction"),
            ("phase435_best_gross_pnl_inr", primary["gross_pnl_inr"], "Primary gross P&L"),
            ("phase435_best_cost200_inr", primary["cost200_inr"], "Primary cost200 charges"),
            ("phase435_best_net_pnl_inr", primary["net_pnl_inr"], "Primary net P&L"),
            ("phase435_best_annualized_return_pct", primary["annualized_return_pct"], "Primary annualized return"),
            ("phase435_real_anchor_round_trips", real_summary["completed_round_trips"].iloc[0] if not real_summary.empty else 0, "Real-anchor selected trades"),
            ("phase435_cost200_acceptance_survivor_rows", survivors, "Accepted rows after all gates"),
            ("phase435_strategy_promotion_allowed", 0, "No promotion"),
            ("phase435_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase435_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase435_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase435_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase435_next_best_action", NEXT_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, summary: pd.DataFrame, real_summary: pd.DataFrame, weights: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase435 Supervised Full-Depth Event Ranker Execution",
        "",
        "Phase435 executes the Phase434 materially new source: a train-only supervised event ranker using L1-L5 book-state features and cost-aware forward labels.",
        "",
        "This is an execution result, not a promotion or paper/live decision.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Scenario Summary",
        "",
        _markdown_table(summary),
        "",
        "## Real-Anchor Summary",
        "",
        _markdown_table(real_summary),
        "",
        "## Learned Weights",
        "",
        _markdown_table(weights.sort_values("weight", key=lambda s: s.abs(), ascending=False)),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: no strategy promotion, paper/live acceptance or deployable profitability claim is opened by Phase435.",
    ]
    (output_dir / "phase435_supervised_full_depth_event_ranker_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(raw_root: Path = DEFAULT_RAW_ROOT, phase434_dir: Path = DEFAULT_PHASE434_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR, real_roots: list[Path] | None = None) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase434 = read_csv(phase434_dir / "phase434_acceptance_summary.csv")
    if str(metric_value(phase434, "phase434_next_best_action", "")) != PHASE434_NEXT_ACTION:
        raise ValueError("Phase435 requires Phase434 execution allowance.")
    synthetic_ticks = load_synthetic_ticks(raw_root)
    events = build_events(synthetic_ticks, panel="synthetic", max_hold_ticks=MAX_HOLD_TICKS_SYNTHETIC, stride=SYNTHETIC_SCAN_STRIDE)
    if events.empty:
        raise ValueError("Phase435 produced no synthetic event rows.")
    train_dates, validation_dates = split_dates(events)
    train = events[events["trade_date"].isin(train_dates)].copy()
    validation = events[events["trade_date"].isin(validation_dates)].copy()
    full_weights = fit_linear_ranker(train, ALL_FEATURES)
    l1_weights = fit_linear_ranker(train, L1_ONLY_FEATURES)
    scored_validation = apply_ranker(validation, full_weights, "full_depth_score")
    scored_validation = apply_ranker(scored_validation, l1_weights, "l1_only_score")
    primary_trades = select_and_score(scored_validation, score_col="full_depth_score", scenario_id="P435_full_depth_ranker_validation")
    l1_trades = select_and_score(scored_validation, score_col="l1_only_score", scenario_id="P435_l1_only_ablation_validation")
    side_flip_trades = select_and_score(scored_validation, score_col="full_depth_score", scenario_id="P435_side_flip_control_validation", side_multiplier=-1)
    shuffle_trades = select_and_score(scored_validation, score_col="full_depth_score", scenario_id="P435_time_shuffle_control_validation", shuffle_scores=True)
    summary = pd.DataFrame(
        [
            summarize_trades(primary_trades, panel="synthetic_validation", scenario_id="P435_full_depth_ranker_validation"),
            summarize_trades(l1_trades, panel="synthetic_validation", scenario_id="P435_l1_only_ablation_validation"),
            summarize_trades(side_flip_trades, panel="synthetic_validation", scenario_id="P435_side_flip_control_validation"),
            summarize_trades(shuffle_trades, panel="synthetic_validation", scenario_id="P435_time_shuffle_control_validation"),
        ]
    )
    real_ticks = load_real_anchor_ticks(real_roots or DEFAULT_REAL_ROOTS)
    real_events = build_events(real_ticks, panel="real_anchor", max_hold_ticks=MAX_HOLD_TICKS_REAL, stride=REAL_SCAN_STRIDE)
    if not real_events.empty:
        real_scored = apply_ranker(real_events, full_weights, "full_depth_score")
        real_trades = select_and_score(real_scored, score_col="full_depth_score", scenario_id="P435_full_depth_ranker_real_anchor")
    else:
        real_trades = pd.DataFrame()
    real_summary = pd.DataFrame([summarize_trades(real_trades, panel="real_anchor", scenario_id="P435_full_depth_ranker_real_anchor")])
    gates = build_gates(summary, full_weights, real_summary)
    acceptance = build_acceptance(events, summary, gates, real_summary)
    events.head(50_000).to_csv(output_dir / "phase435_synthetic_event_label_sample.csv", index=False)
    full_weights.to_csv(output_dir / "phase435_full_depth_ranker_weights.csv", index=False)
    l1_weights.to_csv(output_dir / "phase435_l1_only_ranker_weights.csv", index=False)
    summary.to_csv(output_dir / "phase435_scenario_summary.csv", index=False)
    primary_trades.head(25_000).to_csv(output_dir / "phase435_primary_trade_ledger_sample.csv", index=False)
    l1_trades.head(25_000).to_csv(output_dir / "phase435_l1_control_trade_ledger_sample.csv", index=False)
    side_flip_trades.head(25_000).to_csv(output_dir / "phase435_side_flip_trade_ledger_sample.csv", index=False)
    shuffle_trades.head(25_000).to_csv(output_dir / "phase435_time_shuffle_trade_ledger_sample.csv", index=False)
    real_summary.to_csv(output_dir / "phase435_real_anchor_summary.csv", index=False)
    real_trades.head(25_000).to_csv(output_dir / "phase435_real_anchor_trade_ledger_sample.csv", index=False)
    gates.to_csv(output_dir / "phase435_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase435_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, summary, real_summary, full_weights, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase435_supervised_full_depth_event_ranker",
        **reproducibility_fields(
            artifact_id="phase435_supervised_full_depth_event_ranker",
            generated_utc=generated_utc,
            inputs={"phase434_acceptance_summary": str(phase434_dir / "phase434_acceptance_summary.csv"), "raw_root": str(raw_root)},
            parameters={
                "thesis_id": THESIS_ID,
                "lookback_ticks": LOOKBACK_TICKS,
                "forward_ticks": FORWARD_TICKS,
                "min_hold_ms": MIN_HOLD_MS,
                "top_k_per_symbol_date": TOP_K_PER_SYMBOL_DATE,
                "train_dates": train_dates,
                "validation_dates": validation_dates,
            },
            outputs={"acceptance_summary": str(output_dir / "phase435_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase435_exact_tick_forward_label",
        ),
    }
    (output_dir / "phase435_supervised_full_depth_event_ranker_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase435 supervised full-depth event ranker.")
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--phase434-dir", type=Path, default=DEFAULT_PHASE434_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.raw_root, args.phase434_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
