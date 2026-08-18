from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase474_larger_horizon_fewer_trade_experiment import HORIZONS
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import (
    ZERODHA_CHARGES_SOURCE_URL,
    ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
    calculate_equity_intraday_nse_charges,
)


DEFAULT_PHASE467_DIR = Path("outputs/phase467")
DEFAULT_PHASE474_DIR = Path("outputs/phase474")
DEFAULT_OUTPUT_DIR = Path("outputs/phase475")

THESIS_ID = "P475_CATALYST_LIQUIDITY_CONDITIONED_REPLAY"
NEXT_ACTION_PASS = "precommit_phase476_expand_conditioned_candidate_with_real_catalyst_l2_holdout"
NEXT_ACTION_FAIL = "interpret_phase475_conditioned_replay_failure_or_return_to_real_date_expansion"

FIXED_CAPITAL_INR = 100_000.0
ADVERSE_SLIPPAGE_ROUND_TRIP_BPS = 2.0
MIN_ANNUALIZED_RETURN_PCT = 12.0
MIN_TRADE_COUNT = 10
TOP_FRACTIONS = [0.05, 0.10, 0.20]
FILTER_IDS = [
    "shock_only",
    "liquidity_vacuum",
    "shock_and_liquidity_vacuum",
    "shock_and_l25_pressure",
]


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def load_shock_calendar(selected: pd.DataFrame) -> pd.DataFrame:
    rows = []
    columns = ["trade_date", "symbol", "is_market_shock_day", "is_symbol_shock", "regime_code"]
    for path in selected["path"].astype(str):
        p = Path(path)
        if not p.exists():
            continue
        parts = [batch.to_pandas() for batch in pq.ParquetFile(p).iter_batches(batch_size=100_000, columns=columns)]
        df = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=columns)
        if df.empty:
            continue
        grouped = (
            df.groupby(["trade_date", "symbol"], sort=False)
            .agg(
                is_market_shock_day=("is_market_shock_day", "max"),
                is_symbol_shock=("is_symbol_shock", "max"),
                regime_code=("regime_code", lambda x: ";".join(sorted(set(map(str, x.dropna()))))[:120]),
            )
            .reset_index()
        )
        rows.append(grouped)
    if not rows:
        return pd.DataFrame(columns=columns)
    out = pd.concat(rows, ignore_index=True).drop_duplicates(["trade_date", "symbol"], keep="last")
    out["is_market_shock_day"] = out["is_market_shock_day"].astype(bool).astype(int)
    out["is_symbol_shock"] = out["is_symbol_shock"].astype(bool).astype(int)
    return out


def quantile_thresholds(train: pd.DataFrame) -> dict[str, float]:
    return {
        "spread_q75": float(pd.to_numeric(train["spread_bps"], errors="coerce").quantile(0.75)),
        "spread_vol_q75": float(pd.to_numeric(train["source_event_spread_vol_5_bps"], errors="coerce").quantile(0.75)),
        "l25_abs_imbalance_q75": float(pd.to_numeric(train["l25_imbalance"], errors="coerce").abs().quantile(0.75)),
        "l25_ofi_abs_q75": float(pd.to_numeric(train["source_event_l25_ofi_1"], errors="coerce").abs().quantile(0.75)),
    }


def apply_filter(df: pd.DataFrame, filter_id: str, thresholds: dict[str, float]) -> pd.Series:
    shock = df["is_market_shock_day"].astype(int).eq(1) | df["is_symbol_shock"].astype(int).eq(1)
    liquidity_vacuum = (
        pd.to_numeric(df["spread_bps"], errors="coerce").ge(thresholds["spread_q75"])
        & pd.to_numeric(df["source_event_spread_vol_5_bps"], errors="coerce").ge(thresholds["spread_vol_q75"])
    )
    l25_pressure = (
        pd.to_numeric(df["l25_imbalance"], errors="coerce").abs().ge(thresholds["l25_abs_imbalance_q75"])
        | pd.to_numeric(df["source_event_l25_ofi_1"], errors="coerce").abs().ge(thresholds["l25_ofi_abs_q75"])
    )
    if filter_id == "shock_only":
        return shock
    if filter_id == "liquidity_vacuum":
        return liquidity_vacuum
    if filter_id == "shock_and_liquidity_vacuum":
        return shock & liquidity_vacuum
    if filter_id == "shock_and_l25_pressure":
        return shock & l25_pressure
    raise ValueError(f"Unknown filter_id {filter_id}")


def replay_selected(rows: pd.DataFrame, horizon: int, filter_id: str, top_fraction: float, candidate_rows: int) -> pd.DataFrame:
    if rows.empty:
        return pd.DataFrame()
    target_count = max(MIN_TRADE_COUNT, int(round(candidate_rows * top_fraction)))
    target_count = min(target_count, len(rows))
    selected = rows.sort_values(["confidence", "abs_forward_return_bps"], ascending=False).head(target_count)
    out = []
    for row in selected.to_dict("records"):
        prob = float(row["primary_long_probability"])
        side = 1 if prob >= 0.5 else -1
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
        out.append(
            {
                "trade_date": row["trade_date"],
                "symbol": row["symbol"],
                "candidate_start_row": int(row["candidate_start_row"]),
                "horizon_ticks": horizon,
                "filter_id": filter_id,
                "top_fraction": top_fraction,
                "signal_side": "long" if side == 1 else "short",
                "probability": prob,
                "confidence": float(row["confidence"]),
                "is_market_shock_day": int(row["is_market_shock_day"]),
                "is_symbol_shock": int(row["is_symbol_shock"]),
                "entry_price": entry_price,
                "exit_price": exit_price,
                "quantity": quantity,
                "gross_pnl_inr": gross_pnl,
                "zerodha_total_charges_inr": charges.total_charges,
                "adverse_slippage_inr": slippage_inr,
                "net_pnl_inr": net_pnl,
                "forward_return_bps": float(row["forward_return_bps"]),
                "label_side": row["label_side"],
                **{f"charge_{key}": value for key, value in asdict(charges).items() if key in {"brokerage", "stt", "transaction_charge", "sebi_charge", "stamp_duty", "gst"}},
            }
        )
    return pd.DataFrame(out)


def summarize(trades: pd.DataFrame, scenario_id: str, horizon: int, filter_id: str, top_fraction: float, candidate_rows: int, holdout_days: int) -> dict[str, Any]:
    if trades.empty:
        return {
            "scenario_id": scenario_id,
            "horizon_ticks": horizon,
            "filter_id": filter_id,
            "top_fraction": top_fraction,
            "candidate_rows_after_filter": candidate_rows,
            "trade_count": 0,
            "holdout_days": holdout_days,
            "gross_pnl_inr": 0.0,
            "zerodha_total_charges_inr": 0.0,
            "adverse_slippage_inr": 0.0,
            "net_pnl_inr": 0.0,
            "annualized_return_pct": 0.0,
            "win_rate": 0.0,
            "avg_net_per_trade_inr": 0.0,
            "max_daily_drawdown_inr": 0.0,
        }
    daily = trades.groupby("trade_date", sort=True)["net_pnl_inr"].sum().reset_index()
    equity = daily["net_pnl_inr"].cumsum()
    drawdown = equity - equity.cummax()
    net = float(trades["net_pnl_inr"].sum())
    return {
        "scenario_id": scenario_id,
        "horizon_ticks": horizon,
        "filter_id": filter_id,
        "top_fraction": top_fraction,
        "candidate_rows_after_filter": candidate_rows,
        "trade_count": int(len(trades)),
        "holdout_days": holdout_days,
        "gross_pnl_inr": float(trades["gross_pnl_inr"].sum()),
        "zerodha_total_charges_inr": float(trades["zerodha_total_charges_inr"].sum()),
        "adverse_slippage_inr": float(trades["adverse_slippage_inr"].sum()),
        "net_pnl_inr": net,
        "annualized_return_pct": (net / FIXED_CAPITAL_INR) * (252.0 / max(1, holdout_days)) * 100.0,
        "win_rate": float((trades["net_pnl_inr"] > 0).mean()),
        "avg_net_per_trade_inr": float(trades["net_pnl_inr"].mean()),
        "max_daily_drawdown_inr": float(drawdown.min()) if len(drawdown) else 0.0,
    }


def build_conditioned_replay(phase467_dir: Path, phase474_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    selected_files = read_csv(phase467_dir / "phase467_selected_files.csv")
    shock_calendar = load_shock_calendar(selected_files)
    score_base = read_csv(phase474_dir / "phase474_holdout_scores.csv")
    scenario_rows = []
    trade_parts = []
    threshold_rows = []
    for horizon in HORIZONS:
        matrix = read_csv(phase474_dir / f"phase474_feature_label_matrix_horizon_{horizon}.csv")
        scores = score_base[score_base["horizon_ticks"].astype(int).eq(horizon)].copy()
        keep_cols = ["trade_date", "symbol", "candidate_start_row", "spread_bps", "l25_imbalance", "source_event_l25_ofi_1", "source_event_spread_vol_5_bps"]
        enriched = scores.merge(matrix[keep_cols], on=["trade_date", "symbol", "candidate_start_row"], how="left")
        enriched = enriched.merge(shock_calendar, on=["trade_date", "symbol"], how="left")
        enriched[["is_market_shock_day", "is_symbol_shock"]] = enriched[["is_market_shock_day", "is_symbol_shock"]].fillna(0).astype(int)
        enriched["confidence"] = (pd.to_numeric(enriched["primary_long_probability"], errors="coerce") - 0.5).abs()
        train = matrix[matrix["phase464_split"].astype(str).eq("train")].copy()
        thresholds = quantile_thresholds(train)
        threshold_rows.append({"horizon_ticks": horizon, **thresholds})
        holdout_days = int(enriched["trade_date"].nunique())
        for filter_id in FILTER_IDS:
            mask = apply_filter(enriched, filter_id, thresholds)
            filtered = enriched[mask].copy()
            candidate_rows = int(len(filtered))
            for top_fraction in TOP_FRACTIONS:
                scenario_id = f"horizon_{horizon}_{filter_id}_top_{top_fraction:.2f}_cost200"
                trades = replay_selected(filtered, horizon, filter_id, top_fraction, candidate_rows)
                if not trades.empty:
                    trades["scenario_id"] = scenario_id
                    trade_parts.append(trades)
                scenario_rows.append(summarize(trades, scenario_id, horizon, filter_id, top_fraction, candidate_rows, holdout_days))
    return pd.DataFrame(scenario_rows), (pd.concat(trade_parts, ignore_index=True) if trade_parts else pd.DataFrame()), pd.DataFrame(threshold_rows)


def build_gates(phase474: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    best = scenarios.sort_values(["annualized_return_pct", "net_pnl_inr"], ascending=False).iloc[0]
    positive = int((scenarios["net_pnl_inr"].astype(float) > 0).sum())
    above12 = int((scenarios["annualized_return_pct"].astype(float) >= MIN_ANNUALIZED_RETURN_PCT).sum())
    rows = [
        ("P475_PHASE474_COMPLETE_USED", as_int(scalar(phase474, "phase474_larger_horizon_fewer_trade_experiment_complete", 0)) == 1, scalar(phase474, "phase474_larger_horizon_fewer_trade_experiment_complete", 0), 1),
        ("P475_PHASE474_REJECTION_USED", as_int(scalar(phase474, "phase474_phase475_allowed_next", 1)) == 0, scalar(phase474, "phase474_phase475_allowed_next", 1), 0),
        ("P475_FILTER_GRID_PRESENT", len(scenarios) == len(HORIZONS) * len(FILTER_IDS) * len(TOP_FRACTIONS), len(scenarios), len(HORIZONS) * len(FILTER_IDS) * len(TOP_FRACTIONS)),
        ("P475_CATALYST_FILTERS_USED", bool(scenarios["filter_id"].astype(str).str.contains("shock").any()), ";".join(sorted(scenarios["filter_id"].astype(str).unique())), "shock_filter_present"),
        ("P475_LIQUIDITY_FILTERS_USED", bool(scenarios["filter_id"].astype(str).str.contains("liquidity|l25", regex=True).any()), ";".join(sorted(scenarios["filter_id"].astype(str).unique())), "liquidity_or_l25_filter_present"),
        ("P475_COST200_INCLUDED", ADVERSE_SLIPPAGE_ROUND_TRIP_BPS == 2.0, ADVERSE_SLIPPAGE_ROUND_TRIP_BPS, 2.0),
        ("P475_FIXED_CAPITAL_USED", FIXED_CAPITAL_INR == 100_000.0, FIXED_CAPITAL_INR, 100_000.0),
        ("P475_POSITIVE_NET_SCENARIO_EXISTS", positive > 0, positive, ">0"),
        ("P475_ABOVE_12PCT_ANNUALIZED_SCENARIO_EXISTS", above12 > 0, above12, ">0"),
        ("P475_BEST_TRADE_COUNT_GE_10", int(best["trade_count"]) >= MIN_TRADE_COUNT, int(best["trade_count"]), f">={MIN_TRADE_COUNT}"),
        ("P475_NO_PAPER_LIVE_OR_CLAIM", True, "synthetic_conditioned_replay_only;paper=0;live=0", "no_paper_live"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(gates: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    best = scenarios.sort_values(["annualized_return_pct", "net_pnl_inr"], ascending=False).iloc[0]
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    all_pass = int(hard_pass == hard_rows)
    rows = [
        ("phase475_catalyst_liquidity_conditioned_replay_complete", 1, "Phase475 conditioned replay completed"),
        ("phase475_thesis_id", THESIS_ID, "Conditioned replay thesis"),
        ("phase475_best_scenario_id", best["scenario_id"], "Best scenario"),
        ("phase475_best_trade_count", int(best["trade_count"]), "Best trade count"),
        ("phase475_best_net_pnl_inr", float(best["net_pnl_inr"]), "Best net P&L"),
        ("phase475_best_annualized_return_pct", float(best["annualized_return_pct"]), "Best fixed-capital annualized return"),
        ("phase475_positive_net_scenario_rows", int((scenarios["net_pnl_inr"].astype(float) > 0).sum()), "Positive net scenarios"),
        ("phase475_above12_annualized_scenario_rows", int((scenarios["annualized_return_pct"].astype(float) >= MIN_ANNUALIZED_RETURN_PCT).sum()), "Scenarios above 12% annualized"),
        ("phase475_fixed_capital_inr", FIXED_CAPITAL_INR, "Reusable capital denominator"),
        ("phase475_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model version"),
        ("phase475_zerodha_cost_source_url", ZERODHA_CHARGES_SOURCE_URL, "Cost source"),
        ("phase475_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase475_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase475_phase476_allowed_next", all_pass, "Allows expansion only if all gates pass"),
        ("phase475_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase475_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase475_next_best_action", NEXT_ACTION_PASS if all_pass else NEXT_ACTION_FAIL, "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, thresholds: pd.DataFrame, scenarios: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase475 Catalyst/Liquidity-Conditioned Replay",
        "",
        "Phase475 conditions the Phase474 synthetic branch on catalyst/shock flags and entry-time L1-L5 liquidity-vacuum features, then replays top-confidence holdout trades with Zerodha cost200.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Train-Only Filter Thresholds",
        "",
        _markdown_table(thresholds),
        "",
        "## Scenario Summary",
        "",
        _markdown_table(scenarios),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase475 is synthetic-conditioned replay evidence only. It is not paper/live acceptance and not a deployable profitability claim.",
    ]
    (output_dir / "phase475_catalyst_liquidity_conditioned_replay_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase467_dir: Path = DEFAULT_PHASE467_DIR, phase474_dir: Path = DEFAULT_PHASE474_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase474 = read_csv(phase474_dir / "phase474_acceptance_summary.csv")
    scenarios, trades, thresholds = build_conditioned_replay(phase467_dir, phase474_dir)
    gates = build_gates(phase474, scenarios)
    acceptance = build_acceptance(gates, scenarios)
    thresholds.to_csv(output_dir / "phase475_train_filter_thresholds.csv", index=False)
    scenarios.to_csv(output_dir / "phase475_scenario_summary.csv", index=False)
    trades.to_csv(output_dir / "phase475_trade_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase475_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase475_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, thresholds, scenarios, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase475_catalyst_liquidity_conditioned_replay",
        **reproducibility_fields(
            artifact_id="phase475_catalyst_liquidity_conditioned_replay",
            generated_utc=generated_utc,
            inputs={
                "phase474_holdout_scores": str(phase474_dir / "phase474_holdout_scores.csv"),
                "phase474_matrices": str(phase474_dir),
                "phase467_selected_files": str(phase467_dir / "phase467_selected_files.csv"),
            },
            parameters={
                "thesis_id": THESIS_ID,
                "filters": FILTER_IDS,
                "top_fractions": TOP_FRACTIONS,
                "fixed_capital_inr": FIXED_CAPITAL_INR,
                "adverse_slippage_round_trip_bps": ADVERSE_SLIPPAGE_ROUND_TRIP_BPS,
                "min_annualized_return_pct": MIN_ANNUALIZED_RETURN_PCT,
            },
            outputs={"acceptance_summary": str(output_dir / "phase475_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase475_cost200_adverse_slippage_proxy",
        ),
    }
    (output_dir / "phase475_catalyst_liquidity_conditioned_replay_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase475 catalyst/liquidity-conditioned replay.")
    parser.add_argument("--phase467-dir", type=Path, default=DEFAULT_PHASE467_DIR)
    parser.add_argument("--phase474-dir", type=Path, default=DEFAULT_PHASE474_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    out = run(args.phase467_dir, args.phase474_dir, args.output_dir)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
