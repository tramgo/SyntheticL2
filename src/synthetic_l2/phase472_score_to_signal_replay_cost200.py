from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import (
    ZERODHA_CHARGES_SOURCE_URL,
    ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
    calculate_equity_intraday_nse_charges,
)


DEFAULT_PHASE471_DIR = Path("outputs/phase471")
DEFAULT_OUTPUT_DIR = Path("outputs/phase472")

THESIS_ID = "P472_SCORE_TO_SIGNAL_REPLAY_COST200"
NEXT_ACTION_PASS = "expand_phase472_replay_to_more_dates_symbols_or_real_l2_holdout_before_any_paper_live"
NEXT_ACTION_FAIL = "interpret_phase472_costed_replay_failure_before_tuning"

FIXED_CAPITAL_INR = 100_000.0
ADVERSE_SLIPPAGE_ROUND_TRIP_BPS = 2.0
MIN_ANNUALIZED_RETURN_PCT = 12.0
MIN_TRADE_COUNT = 10
THRESHOLDS = [0.50, 0.52, 0.54, 0.56, 0.58, 0.60]


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def side_from_probability(prob: float, threshold: float) -> int:
    if prob >= threshold:
        return 1
    if prob <= 1.0 - threshold:
        return -1
    return 0


def replay_trades(scores: pd.DataFrame, model_score_column: str, threshold: float) -> pd.DataFrame:
    rows = []
    for row in scores.to_dict("records"):
        prob = float(row[model_score_column])
        side = side_from_probability(prob, threshold)
        if side == 0:
            continue
        entry_price = float(row["entry_price"])
        exit_price = float(row["exit_price"])
        quantity = max(1, int(FIXED_CAPITAL_INR // max(entry_price, 1e-9)))
        entry_value = quantity * entry_price
        exit_value = quantity * exit_price
        if side == 1:
            buy_value = entry_value
            sell_value = exit_value
            gross_pnl = exit_value - entry_value
        else:
            buy_value = exit_value
            sell_value = entry_value
            gross_pnl = entry_value - exit_value
        charges = calculate_equity_intraday_nse_charges(
            buy_value_inr=buy_value,
            sell_value_inr=sell_value,
            buy_quantity=quantity,
            sell_quantity=quantity,
            buy_orders=1,
            sell_orders=1,
        )
        slippage_inr = (ADVERSE_SLIPPAGE_ROUND_TRIP_BPS / 10_000.0) * entry_value
        net_pnl = gross_pnl - charges.total_charges - slippage_inr
        rows.append(
            {
                "trade_date": row["trade_date"],
                "symbol": row["symbol"],
                "candidate_start_row": int(row["candidate_start_row"]),
                "model_score_column": model_score_column,
                "threshold": threshold,
                "signal_side": "long" if side == 1 else "short",
                "probability": prob,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "quantity": quantity,
                "gross_pnl_inr": gross_pnl,
                "zerodha_total_charges_inr": charges.total_charges,
                "adverse_slippage_inr": slippage_inr,
                "net_pnl_inr": net_pnl,
                "forward_return_bps": float(row["forward_return_bps"]),
                "abs_forward_return_bps": float(row["abs_forward_return_bps"]),
                "label_side": row["label_side"],
                **{f"charge_{key}": value for key, value in asdict(charges).items() if key in {"brokerage", "stt", "transaction_charge", "sebi_charge", "stamp_duty", "gst"}},
            }
        )
    return pd.DataFrame(rows)


def summarize_trades(trades: pd.DataFrame, scenario_id: str, holdout_days: int) -> dict[str, Any]:
    if trades.empty:
        return {
            "scenario_id": scenario_id,
            "trade_count": 0,
            "unique_trade_dates": holdout_days,
            "gross_pnl_inr": 0.0,
            "zerodha_total_charges_inr": 0.0,
            "adverse_slippage_inr": 0.0,
            "net_pnl_inr": 0.0,
            "win_rate": 0.0,
            "avg_net_per_trade_inr": 0.0,
            "annualized_return_pct": 0.0,
            "max_daily_drawdown_inr": 0.0,
        }
    daily = trades.groupby("trade_date", sort=True)["net_pnl_inr"].sum().reset_index()
    equity = daily["net_pnl_inr"].cumsum()
    drawdown = equity - equity.cummax()
    net = float(trades["net_pnl_inr"].sum())
    annualized = (net / FIXED_CAPITAL_INR) * (252.0 / max(1, holdout_days)) * 100.0
    return {
        "scenario_id": scenario_id,
        "trade_count": int(len(trades)),
        "unique_trade_dates": holdout_days,
        "gross_pnl_inr": float(trades["gross_pnl_inr"].sum()),
        "zerodha_total_charges_inr": float(trades["zerodha_total_charges_inr"].sum()),
        "adverse_slippage_inr": float(trades["adverse_slippage_inr"].sum()),
        "net_pnl_inr": net,
        "win_rate": float((trades["net_pnl_inr"] > 0).mean()),
        "avg_net_per_trade_inr": float(trades["net_pnl_inr"].mean()),
        "annualized_return_pct": annualized,
        "max_daily_drawdown_inr": float(drawdown.min()) if len(drawdown) else 0.0,
    }


def run_scenarios(scores: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    holdout_days = int(scores["trade_date"].nunique())
    summaries = []
    trade_parts = []
    for model_name, column in [("primary", "primary_long_probability"), ("shuffled", "shuffled_long_probability"), ("l25_threshold", "l25_threshold_score")]:
        for threshold in THRESHOLDS:
            scenario_id = f"{model_name}_threshold_{threshold:.2f}_cost200"
            trades = replay_trades(scores, column, threshold)
            if not trades.empty:
                trades["scenario_id"] = scenario_id
                trade_parts.append(trades)
            summary = summarize_trades(trades, scenario_id, holdout_days)
            summary["model_name"] = model_name
            summary["threshold"] = threshold
            summary["fixed_capital_inr"] = FIXED_CAPITAL_INR
            summary["adverse_slippage_round_trip_bps"] = ADVERSE_SLIPPAGE_ROUND_TRIP_BPS
            summaries.append(summary)
    return pd.DataFrame(summaries), (pd.concat(trade_parts, ignore_index=True) if trade_parts else pd.DataFrame())


def build_gates(phase471: pd.DataFrame, scenario_summary: pd.DataFrame) -> pd.DataFrame:
    primary = scenario_summary[scenario_summary["model_name"].eq("primary")].copy()
    shuffled = scenario_summary[scenario_summary["model_name"].eq("shuffled")].copy()
    best_primary = primary.sort_values(["annualized_return_pct", "net_pnl_inr"], ascending=False).iloc[0]
    best_shuffled = shuffled.sort_values(["annualized_return_pct", "net_pnl_inr"], ascending=False).iloc[0]
    positive_primary = int((primary["net_pnl_inr"].astype(float) > 0).sum())
    above12_primary = int((primary["annualized_return_pct"].astype(float) >= MIN_ANNUALIZED_RETURN_PCT).sum())
    rows = [
        ("P472_PHASE471_MODEL_USED", as_int(scalar(phase471, "phase471_phase472_allowed_next", 0)) == 1, scalar(phase471, "phase471_phase472_allowed_next", 0), 1),
        ("P472_SCENARIOS_PRESENT", len(scenario_summary) == len(THRESHOLDS) * 3, len(scenario_summary), len(THRESHOLDS) * 3),
        ("P472_FIXED_CAPITAL_USED", FIXED_CAPITAL_INR == 100_000.0, FIXED_CAPITAL_INR, 100_000.0),
        ("P472_ZERODHA_COSTS_INCLUDED", True, ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "zerodha_cost_model"),
        ("P472_COST200_SLIPPAGE_INCLUDED", ADVERSE_SLIPPAGE_ROUND_TRIP_BPS == 2.0, ADVERSE_SLIPPAGE_ROUND_TRIP_BPS, 2.0),
        ("P472_PRIMARY_POSITIVE_SCENARIO_EXISTS", positive_primary > 0, positive_primary, ">0"),
        ("P472_PRIMARY_ABOVE_12PCT_ANNUALIZED_EXISTS", above12_primary > 0, above12_primary, ">0"),
        ("P472_BEST_PRIMARY_TRADE_COUNT_GE_10", int(best_primary["trade_count"]) >= MIN_TRADE_COUNT, int(best_primary["trade_count"]), f">={MIN_TRADE_COUNT}"),
        ("P472_BEST_PRIMARY_BEATS_BEST_SHUFFLED", float(best_primary["annualized_return_pct"]) > float(best_shuffled["annualized_return_pct"]), f"primary={float(best_primary['annualized_return_pct'])};shuffled={float(best_shuffled['annualized_return_pct'])}", "primary>shuffled"),
        ("P472_NO_PAPER_LIVE_OR_CLAIM", True, "replay_only;paper=0;live=0", "no_paper_live"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in rows])


def build_acceptance(gates: pd.DataFrame, scenario_summary: pd.DataFrame) -> pd.DataFrame:
    primary = scenario_summary[scenario_summary["model_name"].eq("primary")].copy()
    best_primary = primary.sort_values(["annualized_return_pct", "net_pnl_inr"], ascending=False).iloc[0]
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    passed = int(hard_pass == hard_rows)
    rows = [
        ("phase472_score_to_signal_replay_cost200_complete", 1, "Phase472 replay completed"),
        ("phase472_thesis_id", THESIS_ID, "Replay thesis"),
        ("phase472_best_primary_scenario_id", best_primary["scenario_id"], "Best primary scenario"),
        ("phase472_best_primary_trade_count", int(best_primary["trade_count"]), "Trade count"),
        ("phase472_best_primary_net_pnl_inr", float(best_primary["net_pnl_inr"]), "Best primary net P&L"),
        ("phase472_best_primary_annualized_return_pct", float(best_primary["annualized_return_pct"]), "Fixed-capital annualized return"),
        ("phase472_best_primary_avg_net_per_trade_inr", float(best_primary["avg_net_per_trade_inr"]), "Average net per trade"),
        ("phase472_primary_above12_scenario_rows", int((primary["annualized_return_pct"].astype(float) >= MIN_ANNUALIZED_RETURN_PCT).sum()), "Primary scenarios above 12% annualized"),
        ("phase472_fixed_capital_inr", FIXED_CAPITAL_INR, "Reusable capital denominator"),
        ("phase472_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model version"),
        ("phase472_zerodha_cost_source_url", ZERODHA_CHARGES_SOURCE_URL, "Cost source"),
        ("phase472_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase472_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase472_phase473_allowed_next", passed, "Allows expanded validation if all gates pass"),
        ("phase472_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase472_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase472_next_best_action", NEXT_ACTION_PASS if passed else NEXT_ACTION_FAIL, "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, scenario_summary: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase472 Score-to-Signal Replay Cost200",
        "",
        "Phase472 replays Phase471 holdout scores with fixed reusable capital, Zerodha equity intraday NSE charges, and adverse round-trip slippage.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Scenario Summary",
        "",
        _markdown_table(scenario_summary),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase472 is synthetic holdout replay evidence only. It is not paper/live acceptance and not a deployable profitability claim.",
    ]
    (output_dir / "phase472_score_to_signal_replay_cost200_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase471_dir: Path = DEFAULT_PHASE471_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase471 = read_csv(phase471_dir / "phase471_acceptance_summary.csv")
    scores = read_csv(phase471_dir / "phase471_holdout_scores.csv")
    if as_int(scalar(phase471, "phase471_phase472_allowed_next", 0)) != 1:
        raise ValueError("Phase472 requires Phase471 allowance.")
    matrix = read_csv(Path("outputs/phase470/phase470_source_event_aware_feature_label_matrix.csv"))
    scores = scores.merge(
        matrix[["trade_date", "symbol", "candidate_start_row", "entry_price", "exit_price"]],
        on=["trade_date", "symbol", "candidate_start_row"],
        how="left",
    )
    scenario_summary, trades = run_scenarios(scores)
    gates = build_gates(phase471, scenario_summary)
    acceptance = build_acceptance(gates, scenario_summary)
    scenario_summary.to_csv(output_dir / "phase472_scenario_summary.csv", index=False)
    trades.to_csv(output_dir / "phase472_trade_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase472_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase472_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, scenario_summary, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase472_score_to_signal_replay_cost200",
        **reproducibility_fields(
            artifact_id="phase472_score_to_signal_replay_cost200",
            generated_utc=generated_utc,
            inputs={"phase471_holdout_scores": str(phase471_dir / "phase471_holdout_scores.csv")},
            parameters={
                "thesis_id": THESIS_ID,
                "fixed_capital_inr": FIXED_CAPITAL_INR,
                "thresholds": THRESHOLDS,
                "adverse_slippage_round_trip_bps": ADVERSE_SLIPPAGE_ROUND_TRIP_BPS,
                "min_annualized_return_pct": MIN_ANNUALIZED_RETURN_PCT,
            },
            outputs={"acceptance_summary": str(output_dir / "phase472_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase472_cost200_adverse_slippage_proxy",
        ),
    }
    (output_dir / "phase472_score_to_signal_replay_cost200_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase472 score-to-signal replay with cost200.")
    parser.add_argument("--phase471-dir", type=Path, default=DEFAULT_PHASE471_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    out = run(args.phase471_dir, args.output_dir)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
