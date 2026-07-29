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
from synthetic_l2.phase176_receive_flow_feature_materializer import (
    add_cross_symbol_synchrony,
    add_prior_date_receive_rate_zscore,
    aggregate_horizon,
    build_1s_features_for_symbol,
    discover_symbol_dirs,
)
from synthetic_l2.phase235_real_anchor_microprice_replay import materialize_event_bars
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_RAW_ROOT = Path("real_data_sample/l2_unseen_validation")
DEFAULT_PHASE238_DIR = Path("outputs/phase238")
DEFAULT_OUTPUT_DIR = Path("outputs/phase241")
TRADE_DATE = "2026-07-17"
SOURCE_HORIZON_SEC = 15
RANDOM_CONTROL_RUNS = 1000
RANDOM_SEED = 241


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def load_frozen_candidate(phase238_dir: Path) -> dict[str, Any]:
    spec = read_csv(phase238_dir / "phase238_frozen_candidate_spec.csv")
    if spec.empty:
        raise FileNotFoundError(phase238_dir / "phase238_frozen_candidate_spec.csv")
    row = spec.iloc[0].to_dict()
    if as_int(row.get("parameter_tuning_allowed_in_phase238", 1), 1) != 0:
        raise ValueError("Frozen candidate spec does not explicitly forbid parameter tuning")
    return row


def materialize_one_date_features(raw_root: Path, trade_date: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    symbol_dirs = [
        path
        for path in discover_symbol_dirs(raw_root)
        if f"trade_date={trade_date}" in path.parts
    ]
    frames: list[pd.DataFrame] = []
    rows: list[dict[str, Any]] = []
    for symbol_dir in symbol_dirs:
        frame = build_1s_features_for_symbol(symbol_dir)
        if frame.empty:
            continue
        frames.append(frame)
        rows.append(
            {
                "trade_date": trade_date,
                "exchange": frame["exchange"].iloc[0],
                "symbol": frame["symbol"].iloc[0],
                "source_1s_rows": int(len(frame)),
                "raw_parquet_files": int(len(list(symbol_dir.glob("*.parquet")))),
            }
        )
    if not frames:
        return pd.DataFrame(), pd.DataFrame(rows)
    features_1s = pd.concat(frames, ignore_index=True)
    features_1s = add_cross_symbol_synchrony(features_1s)
    features_1s = add_prior_date_receive_rate_zscore(features_1s)
    features_15s = aggregate_horizon(features_1s, SOURCE_HORIZON_SEC)
    return features_15s.sort_values(["trade_date", "symbol", "bucket_ms"], kind="mergesort").reset_index(drop=True), pd.DataFrame(rows)


def replay_frozen_candidate(bars: pd.DataFrame, candidate: dict[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame]:
    horizon = as_int(candidate.get("horizon_event_bars", 6), 6)
    event_threshold = as_float(candidate.get("event_window_score_threshold", 0.0), 0.0)
    signal_source = str(candidate.get("signal_source", "bar_return"))
    signal_threshold = as_float(candidate.get("signal_abs_threshold", 0.0), 0.0)
    direction = str(candidate.get("direction", "reversal"))
    if signal_source not in bars.columns:
        raise ValueError(f"Frozen signal_source={signal_source!r} missing from materialized bars")
    frame = bars.copy()
    future_col = f"future_return_h{horizon}"
    frame[future_col] = (
        frame.groupby(["trade_date", "symbol"], sort=False)["close_mid_price"].shift(-horizon)
        / frame["close_mid_price"]
        - 1.0
    )
    selected = frame[
        frame[future_col].notna()
        & frame["event_window_score"].ge(event_threshold)
        & frame[signal_source].abs().ge(signal_threshold)
    ].copy()
    side = np.sign(selected[signal_source].astype(float))
    if direction == "reversal":
        side = -side
    selected["side"] = side
    selected = selected[selected["side"].ne(0)].copy()
    selected["candidate_id"] = str(candidate.get("candidate_id", ""))
    selected["horizon_event_bars"] = horizon
    selected["event_window_score_threshold"] = event_threshold
    selected["signal_source"] = signal_source
    selected["signal_abs_threshold"] = signal_threshold
    selected["gross_return"] = selected["side"] * selected[future_col].astype(float)
    selected["cost_return"] = selected["taker_round_trip_cost_floor_bps"].astype(float) / 10000.0
    selected["net_return"] = selected["gross_return"] - selected["cost_return"]
    selected["gross_pnl_inr"] = selected["gross_return"] * DEFAULT_ORDER_NOTIONAL_INR
    selected["cost_pnl_drag_inr"] = selected["cost_return"] * DEFAULT_ORDER_NOTIONAL_INR
    selected["net_pnl_inr"] = selected["net_return"] * DEFAULT_ORDER_NOTIONAL_INR
    keep = [
        "candidate_id",
        "trade_date",
        "exchange",
        "symbol",
        "source_event_bar_id",
        "horizon_event_bars",
        "side",
        "event_window_score",
        "event_window_score_threshold",
        "signal_source",
        signal_source,
        "signal_abs_threshold",
        "close_mid_price",
        "taker_round_trip_cost_floor_bps",
        future_col,
        "gross_pnl_inr",
        "cost_pnl_drag_inr",
        "net_pnl_inr",
    ]
    return selected[keep], frame


def summarize_diagnostic(trades: pd.DataFrame, bars: pd.DataFrame, symbol_inventory: pd.DataFrame, candidate: dict[str, Any]) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame(
            [
                {
                    "candidate_id": candidate.get("candidate_id", ""),
                    "diagnostic_trade_rows": 0,
                    "diagnostic_net_pnl_inr": 0.0,
                    "diagnostic_gross_pnl_inr": 0.0,
                    "diagnostic_cost_pnl_drag_inr": 0.0,
                    "diagnostic_dates": 0,
                    "diagnostic_symbols": 0,
                    "diagnostic_positive_symbols": 0,
                    "diagnostic_precision_cost_clear": 0.0,
                    "diagnostic_max_symbol_contribution_abs": np.nan,
                    "materialized_event_bars": int(len(bars)),
                    "materialized_symbols": int(bars["symbol"].nunique()) if not bars.empty else 0,
                    "raw_symbols": int(symbol_inventory["symbol"].nunique()) if not symbol_inventory.empty else 0,
                    "raw_parquet_files": int(symbol_inventory["raw_parquet_files"].sum()) if not symbol_inventory.empty else 0,
                }
            ]
        )
    net = float(trades["net_pnl_inr"].sum())
    symbol_net = trades.groupby("symbol", sort=True)["net_pnl_inr"].sum()
    denom = abs(net) if abs(net) > 0 else np.nan
    return pd.DataFrame(
        [
            {
                "candidate_id": trades["candidate_id"].iloc[0],
                "diagnostic_trade_rows": int(len(trades)),
                "diagnostic_net_pnl_inr": net,
                "diagnostic_gross_pnl_inr": float(trades["gross_pnl_inr"].sum()),
                "diagnostic_cost_pnl_drag_inr": float(trades["cost_pnl_drag_inr"].sum()),
                "diagnostic_dates": int(trades["trade_date"].nunique()),
                "diagnostic_symbols": int(trades["symbol"].nunique()),
                "diagnostic_positive_symbols": int((symbol_net > 0).sum()),
                "diagnostic_precision_cost_clear": float((trades["net_pnl_inr"] > 0).mean()),
                "diagnostic_max_symbol_contribution_abs": float(symbol_net.abs().max() / denom) if denom and not np.isnan(denom) else np.nan,
                "materialized_event_bars": int(len(bars)),
                "materialized_symbols": int(bars["symbol"].nunique()) if not bars.empty else 0,
                "raw_symbols": int(symbol_inventory["symbol"].nunique()) if not symbol_inventory.empty else 0,
                "raw_parquet_files": int(symbol_inventory["raw_parquet_files"].sum()) if not symbol_inventory.empty else 0,
            }
        ]
    )


def build_controls(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame(
            [
                {"control_id": "SIDE_FLIP", "net_pnl_inr": 0.0, "passed": False},
                {"control_id": "RANDOM_SIDE_1000_RUNS", "net_pnl_inr": 0.0, "random_p95_net_pnl_inr": 0.0, "random_beat_fraction": 0.0, "passed": False},
                {"control_id": "COST_150", "net_pnl_inr": 0.0, "passed": False},
                {"control_id": "COST_200", "net_pnl_inr": 0.0, "passed": False},
            ]
        )
    gross = trades["gross_pnl_inr"].to_numpy(dtype=float)
    cost = trades["cost_pnl_drag_inr"].to_numpy(dtype=float)
    net = float(trades["net_pnl_inr"].sum())
    future_abs = np.abs(gross + cost)
    rng = np.random.default_rng(RANDOM_SEED)
    random_nets = np.asarray(
        [float((rng.choice([-1.0, 1.0], size=len(trades)) * future_abs - cost).sum()) for _ in range(RANDOM_CONTROL_RUNS)]
    )
    return pd.DataFrame(
        [
            {"control_id": "SIDE_FLIP", "net_pnl_inr": float((-gross - cost).sum()), "passed": bool((-gross - cost).sum() < 0)},
            {
                "control_id": "RANDOM_SIDE_1000_RUNS",
                "net_pnl_inr": net,
                "random_p95_net_pnl_inr": float(np.quantile(random_nets, 0.95)),
                "random_beat_fraction": float((net > random_nets).mean()),
                "passed": bool((net > random_nets).mean() >= 0.95),
            },
            {"control_id": "COST_150", "net_pnl_inr": float((gross - 1.5 * cost).sum()), "passed": bool((gross - 1.5 * cost).sum() > 0)},
            {"control_id": "COST_200", "net_pnl_inr": float((gross - 2.0 * cost).sum()), "passed": bool((gross - 2.0 * cost).sum() > 0)},
        ]
    )


def build_gate_evaluation(summary: pd.DataFrame, controls: pd.DataFrame) -> pd.DataFrame:
    row = summary.iloc[0].to_dict() if not summary.empty else {}
    trades = as_int(row.get("diagnostic_trade_rows", 0), 0)
    net = as_float(row.get("diagnostic_net_pnl_inr", 0.0), 0.0)
    symbols = as_int(row.get("diagnostic_symbols", 0), 0)
    control_pass = int(controls["passed"].astype(bool).sum()) if not controls.empty else 0
    rows = [
        ("P241_ONE_DATE_RAW_L2_PRESENT", as_int(row.get("raw_parquet_files", 0), 0) > 0, row.get("raw_parquet_files", 0), ">0 raw parquet files", "hard"),
        ("P241_EVENT_BARS_MATERIALIZED", as_int(row.get("materialized_event_bars", 0), 0) > 0, row.get("materialized_event_bars", 0), ">0 event bars", "hard"),
        ("P241_FROZEN_CANDIDATE_REPLAYED", trades >= 1, trades, ">=1 frozen-candidate trade", "hard"),
        ("P241_DIAGNOSTIC_NET_POSITIVE", net > 0, net, ">0 one-date net P&L after costs", "diagnostic"),
        ("P241_DIAGNOSTIC_SYMBOL_BREADTH", symbols >= 5, symbols, ">=5 symbols on one-date diagnostic", "diagnostic"),
        ("P241_DIAGNOSTIC_CONTROLS", control_pass >= 3, control_pass, ">=3 / 4 controls pass", "diagnostic"),
        ("P241_FULL_ACCEPTANCE_CLOSED_ONE_DATE_ONLY", True, 1, 1, "hard"),
        ("P241_NO_PAPER_LIVE_OR_PROMOTION_UNLOCK", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase241 One-date Unseen Real L2 Diagnostic",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase241 materializes the downloaded 2026-07-17 raw Zerodha-websocket-like top-five market-by-price L2 data into Phase235-compatible event bars.",
        "It replays only the frozen Phase237 candidate with frozen thresholds and no parameter tuning.",
        "Because disk pressure limits validation to one new real date, this is an early-falsification diagnostic only, not full five-date acceptance.",
        "",
    ]
    for title, table in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(table), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(raw_root: Path = DEFAULT_RAW_ROOT, phase238_dir: Path = DEFAULT_PHASE238_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR, trade_date: str = TRADE_DATE) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    candidate = load_frozen_candidate(phase238_dir)
    features_15s, symbol_inventory = materialize_one_date_features(raw_root, trade_date)
    bars = materialize_event_bars(features_15s) if not features_15s.empty else pd.DataFrame()
    trades, labeled_bars = replay_frozen_candidate(bars, candidate) if not bars.empty else (pd.DataFrame(), bars)
    summary = summarize_diagnostic(trades, bars, symbol_inventory, candidate)
    controls = build_controls(trades)
    gates = build_gate_evaluation(summary, controls)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    diagnostic = gates[gates["severity"].astype(str).eq("diagnostic")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    diagnostic_pass = int(diagnostic["passed"].astype(bool).sum()) if not diagnostic.empty else 0
    diagnostic_candidate_survived = int(diagnostic_pass == len(diagnostic) and not diagnostic.empty)
    next_action = (
        "free_disk_or_attach_storage_then_download_second_unseen_date_before_any_acceptance_claim"
        if diagnostic_candidate_survived
        else "close_or_redesign_phase237_candidate_after_one_date_unseen_real_l2_diagnostic_failure_no_paper_live"
    )
    acceptance = pd.DataFrame(
        [
            ("phase241_one_date_unseen_diagnostic_complete", 1, "Phase241 one-date diagnostic completed"),
            ("phase241_trade_date", trade_date, "Unseen real date used"),
            ("phase241_candidate_id", candidate.get("candidate_id", ""), "Frozen Phase237 candidate"),
            ("phase241_parameter_tuning_used", 0, "No Phase241 parameter tuning"),
            ("phase241_source_feature_rows_15s", int(len(features_15s)), "15-second source feature rows materialized"),
            ("phase241_real_event_bar_rows", int(len(bars)), "Phase235-compatible event bars materialized"),
            ("phase241_raw_symbols", as_int(summary["raw_symbols"].iloc[0], 0), "Raw symbols represented"),
            ("phase241_raw_parquet_files", as_int(summary["raw_parquet_files"].iloc[0], 0), "Raw parquet files represented"),
            ("phase241_trade_rows", as_int(summary["diagnostic_trade_rows"].iloc[0], 0), "Frozen candidate trades selected"),
            ("phase241_net_pnl_inr", as_float(summary["diagnostic_net_pnl_inr"].iloc[0], 0.0), "One-date diagnostic net P&L after costs"),
            ("phase241_symbols", as_int(summary["diagnostic_symbols"].iloc[0], 0), "Symbols represented in selected trades"),
            ("phase241_control_pass_rows", int(controls["passed"].astype(bool).sum()) if not controls.empty else 0, "Controls passed"),
            ("phase241_control_rows", int(len(controls)), "Controls evaluated"),
            ("phase241_diagnostic_gate_pass_rows", diagnostic_pass, "Diagnostic gates passed"),
            ("phase241_diagnostic_gate_rows", int(len(diagnostic)), "Diagnostic gates evaluated"),
            ("phase241_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase241_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase241_one_date_diagnostic_candidate_survived", diagnostic_candidate_survived, "One-date diagnostic survived; still not acceptance"),
            ("phase241_full_five_date_acceptance_allowed", 0, "One-date diagnostic cannot satisfy full acceptance"),
            ("phase241_strategy_promotion_allowed", 0, "No strategy promotion from Phase241"),
            ("phase241_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase241"),
            ("phase241_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase241"),
            ("phase241_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    features_15s.to_parquet(output_dir / "phase241_source_features_15s.parquet", index=False)
    bars.to_parquet(output_dir / "phase241_real_event_bars.parquet", index=False)
    labeled_bars.to_parquet(output_dir / "phase241_labeled_real_event_bars.parquet", index=False)
    trades.to_csv(output_dir / "phase241_trade_ledger.csv", index=False)
    summary.to_csv(output_dir / "phase241_diagnostic_summary.csv", index=False)
    symbol_inventory.to_csv(output_dir / "phase241_symbol_inventory.csv", index=False)
    controls.to_csv(output_dir / "phase241_control_summary.csv", index=False)
    gates.to_csv(output_dir / "phase241_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase241_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase241_one_date_unseen_real_l2_diagnostic_report.md",
        {
            "Acceptance Summary": acceptance,
            "Diagnostic Summary": summary,
            "Controls": controls,
            "Gate Evaluation": gates,
            "Symbol Inventory": symbol_inventory,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase241_one_date_unseen_real_l2_diagnostic",
        **reproducibility_fields(
            artifact_id="phase241",
            generated_utc=generated_utc,
            inputs={
                "raw_root": str(raw_root),
                "phase238_frozen_candidate_spec": str(phase238_dir / "phase238_frozen_candidate_spec.csv"),
            },
            parameters={
                "trade_date": trade_date,
                "source_horizon_sec": SOURCE_HORIZON_SEC,
                "random_control_runs": RANDOM_CONTROL_RUNS,
                "random_seed": RANDOM_SEED,
                "parameter_tuning_used": 0,
                "one_date_only_low_disk_policy": 1,
                "full_five_date_acceptance_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "source_features_15s": str(output_dir / "phase241_source_features_15s.parquet"),
                "real_event_bars": str(output_dir / "phase241_real_event_bars.parquet"),
                "labeled_real_event_bars": str(output_dir / "phase241_labeled_real_event_bars.parquet"),
                "trade_ledger": str(output_dir / "phase241_trade_ledger.csv"),
                "diagnostic_summary": str(output_dir / "phase241_diagnostic_summary.csv"),
                "symbol_inventory": str(output_dir / "phase241_symbol_inventory.csv"),
                "control_summary": str(output_dir / "phase241_control_summary.csv"),
                "gate_evaluation": str(output_dir / "phase241_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase241_acceptance_summary.csv"),
                "report": str(output_dir / "phase241_one_date_unseen_real_l2_diagnostic_report.md"),
            },
            random_seed=RANDOM_SEED,
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase235_real_anchor_event_bar_adapter_one_date_unseen",
        ),
    }
    (output_dir / "phase241_one_date_unseen_real_l2_diagnostic_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase241 one-date unseen real L2 diagnostic.")
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--phase238-dir", type=Path, default=DEFAULT_PHASE238_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--trade-date", default=TRADE_DATE)
    args = parser.parse_args()
    manifest = run(raw_root=args.raw_root, phase238_dir=args.phase238_dir, output_dir=args.output_dir, trade_date=args.trade_date)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
