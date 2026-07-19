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
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE83_DIR = Path("outputs/phase83")
DEFAULT_PHASE92_DIR = Path("outputs/phase92")
DEFAULT_OUTPUT_DIR = Path("outputs/phase93")
TRAIN_MONTHS = {"2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"}
TEST_MONTHS = {"2026-07", "2026-08", "2026-09", "2026-10", "2026-11", "2026-12"}


def load_inputs(phase83_dir: Path, phase92_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    features_path = phase92_dir / "low_turnover_event_window_features.parquet"
    specs_path = phase92_dir / "precommitted_event_window_candidate_specs.csv"
    gates_path = phase92_dir / "precommitted_event_window_validation_gates.csv"
    bars_path = phase83_dir / "stratified_source_event_bars.parquet"
    for path in [features_path, specs_path, gates_path, bars_path]:
        if not path.exists():
            raise FileNotFoundError(path)
    features = pd.read_parquet(features_path)
    bars = pd.read_parquet(bars_path)[
        [
            "trade_month",
            "trade_date",
            "feed_profile",
            "source_event_bar_id",
            "symbol",
            "next_bar_return",
        ]
    ].copy()
    replay = features.merge(
        bars,
        on=["trade_month", "trade_date", "feed_profile", "source_event_bar_id", "symbol"],
        how="left",
        validate="one_to_one",
    )
    return replay, pd.read_csv(specs_path), pd.read_csv(gates_path)


def candidate_trades(replay: pd.DataFrame, spec: dict[str, Any]) -> pd.DataFrame:
    selected = replay[
        replay["next_bar_return"].notna()
        & replay["event_window_score"].ge(float(spec["event_window_score_threshold"]))
        & replay["abs_bar_return_bps"].ge(float(spec["abs_bar_return_bps_threshold"]))
        & replay["taker_round_trip_cost_floor_bps"].le(float(spec["max_taker_round_trip_cost_floor_bps"]))
    ].copy()
    if str(spec["requires_shock_bar"]).lower() == "true":
        selected = selected[selected["shock_bar"].astype(bool)].copy()
    if float(spec["book_dislocation_score_threshold"]) > 0:
        selected = selected[selected["book_dislocation_score"].ge(float(spec["book_dislocation_score_threshold"]))].copy()
    if selected.empty:
        return selected
    if str(spec["direction_rule"]).strip().startswith("side = -sign"):
        selected["side"] = -np.sign(selected["bar_return"].astype(float))
    else:
        selected["side"] = np.sign(selected["bar_return"].astype(float))
    selected = selected[selected["side"].ne(0)].copy()
    selected["gross_return"] = selected["side"].astype(float) * selected["next_bar_return"].astype(float)
    selected["cost_return"] = selected["taker_round_trip_cost_floor_bps"].astype(float) / 10000.0
    selected["net_return"] = selected["gross_return"] - selected["cost_return"]
    selected["gross_pnl_inr"] = selected["gross_return"] * DEFAULT_ORDER_NOTIONAL_INR
    selected["cost_pnl_drag_inr"] = selected["cost_return"] * DEFAULT_ORDER_NOTIONAL_INR
    selected["net_pnl_inr"] = selected["net_return"] * DEFAULT_ORDER_NOTIONAL_INR
    selected["candidate_id"] = str(spec["candidate_id"])
    selected["family_id"] = str(spec["family_id"])
    selected["split"] = np.where(
        selected["trade_month"].isin(TRAIN_MONTHS),
        "train",
        np.where(selected["trade_month"].isin(TEST_MONTHS), "test", "excluded"),
    )
    return selected[selected["split"].isin(["train", "test"])].copy()


def contribution(group: pd.DataFrame, by: str, total_net: float) -> float:
    if group.empty or abs(total_net) <= 0:
        return np.nan
    values = group.groupby(by, sort=True)["net_pnl_inr"].sum()
    return float(values.abs().max() / abs(total_net))


def split_metrics(trades: pd.DataFrame, split: str) -> dict[str, Any]:
    if trades.empty or "split" not in trades.columns:
        group = pd.DataFrame()
    else:
        group = trades[trades["split"].eq(split)].copy()
    if group.empty:
        return {
            f"{split}_trades": 0,
            f"{split}_symbols": 0,
            f"{split}_days": 0,
            f"{split}_months": 0,
            f"{split}_net_pnl_inr": 0.0,
            f"{split}_gross_pnl_inr": 0.0,
            f"{split}_cost_pnl_drag_inr": 0.0,
            f"{split}_precision_cost_clear": 0.0,
            f"{split}_positive_months": 0,
            f"{split}_max_day_trade_fraction": np.nan,
            f"{split}_max_month_contribution_abs": np.nan,
            f"{split}_max_symbol_contribution_abs": np.nan,
            f"{split}_abs_gross_to_cost_drag_ratio": np.nan,
        }
    total_net = float(group["net_pnl_inr"].sum())
    gross = float(group["gross_pnl_inr"].sum())
    cost = float(group["cost_pnl_drag_inr"].sum())
    month_net = group.groupby("trade_month", sort=True)["net_pnl_inr"].sum()
    day_counts = group.groupby("trade_date", sort=True).size()
    return {
        f"{split}_trades": int(len(group)),
        f"{split}_symbols": int(group["symbol"].nunique()),
        f"{split}_days": int(group["trade_date"].nunique()),
        f"{split}_months": int(month_net.shape[0]),
        f"{split}_net_pnl_inr": total_net,
        f"{split}_gross_pnl_inr": gross,
        f"{split}_cost_pnl_drag_inr": cost,
        f"{split}_precision_cost_clear": float((group["gross_return"] > group["cost_return"]).mean()),
        f"{split}_positive_months": int((month_net > 0).sum()),
        f"{split}_max_day_trade_fraction": float(day_counts.max() / len(group)) if len(group) else np.nan,
        f"{split}_max_month_contribution_abs": contribution(group, "trade_month", total_net),
        f"{split}_max_symbol_contribution_abs": contribution(group, "symbol", total_net),
        f"{split}_abs_gross_to_cost_drag_ratio": abs(gross) / cost if cost > 0 else np.nan,
    }


def evaluate_candidate(spec: dict[str, Any], trades: pd.DataFrame) -> dict[str, Any]:
    row = dict(spec)
    row.update(split_metrics(trades, "train"))
    row.update(split_metrics(trades, "test"))
    row["train_pass"] = bool(
        row["train_net_pnl_inr"] > 0
        and 50 <= row["train_trades"] <= 1500
        and row["train_symbols"] >= 10
        and row["train_precision_cost_clear"] >= 0.56
        and pd.notna(row["train_max_day_trade_fraction"])
        and row["train_max_day_trade_fraction"] <= 0.10
    )
    row["test_pass"] = bool(
        row["test_net_pnl_inr"] > 0
        and 50 <= row["test_trades"] <= 1500
        and row["test_symbols"] >= 10
        and row["test_precision_cost_clear"] >= 0.56
        and row["test_positive_months"] >= 4
        and pd.notna(row["test_max_day_trade_fraction"])
        and row["test_max_day_trade_fraction"] <= 0.10
        and pd.notna(row["test_abs_gross_to_cost_drag_ratio"])
        and row["test_abs_gross_to_cost_drag_ratio"] >= 1.5
        and pd.notna(row["test_max_month_contribution_abs"])
        and row["test_max_month_contribution_abs"] <= 0.40
        and pd.notna(row["test_max_symbol_contribution_abs"])
        and row["test_max_symbol_contribution_abs"] <= 0.40
    )
    row["phase93_candidate_pass"] = bool(row["train_pass"] and row["test_pass"])
    return row


def run_replay(replay: pd.DataFrame, specs: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    result_rows: list[dict[str, Any]] = []
    trade_frames: list[pd.DataFrame] = []
    monthly_rows: list[pd.DataFrame] = []
    symbol_rows: list[pd.DataFrame] = []
    for spec in specs.to_dict("records"):
        trades = candidate_trades(replay, spec)
        result_rows.append(evaluate_candidate(spec, trades))
        if not trades.empty:
            trade_frames.append(trades)
            monthly_rows.append(
                trades.groupby(["candidate_id", "family_id", "split", "trade_month"], sort=True)
                .agg(
                    trades=("symbol", "count"),
                    symbols=("symbol", "nunique"),
                    net_pnl_inr=("net_pnl_inr", "sum"),
                    gross_pnl_inr=("gross_pnl_inr", "sum"),
                    cost_pnl_drag_inr=("cost_pnl_drag_inr", "sum"),
                    precision_cost_clear=("gross_return", lambda s: float((s > trades.loc[s.index, "cost_return"]).mean())),
                )
                .reset_index()
            )
            symbol_rows.append(
                trades.groupby(["candidate_id", "family_id", "split", "symbol"], sort=True)
                .agg(
                    trades=("trade_month", "count"),
                    months=("trade_month", "nunique"),
                    net_pnl_inr=("net_pnl_inr", "sum"),
                    gross_pnl_inr=("gross_pnl_inr", "sum"),
                    cost_pnl_drag_inr=("cost_pnl_drag_inr", "sum"),
                    precision_cost_clear=("gross_return", lambda s: float((s > trades.loc[s.index, "cost_return"]).mean())),
                )
                .reset_index()
            )
    results = pd.DataFrame(result_rows).sort_values(
        ["phase93_candidate_pass", "test_net_pnl_inr"], ascending=[False, False], kind="mergesort"
    )
    monthly = pd.concat(monthly_rows, ignore_index=True) if monthly_rows else pd.DataFrame()
    symbol = pd.concat(symbol_rows, ignore_index=True) if symbol_rows else pd.DataFrame()
    trades_all = pd.concat(trade_frames, ignore_index=True) if trade_frames else pd.DataFrame()
    return results, monthly, symbol, trades_all


def summarize(results: pd.DataFrame, specs: pd.DataFrame) -> pd.DataFrame:
    passed = int(results["phase93_candidate_pass"].sum()) if not results.empty else 0
    train_pass = int(results["train_pass"].sum()) if not results.empty else 0
    test_pass = int(results["test_pass"].sum()) if not results.empty else 0
    best_test = float(results["test_net_pnl_inr"].max()) if not results.empty else 0.0
    best_train = float(results["train_net_pnl_inr"].max()) if not results.empty else 0.0
    return pd.DataFrame(
        [
            ("phase93_precommitted_candidate_rows", int(len(specs)), "Phase92 candidate specs replayed without threshold changes"),
            ("phase93_train_pass_candidates", train_pass, "Candidates passing train gates"),
            ("phase93_test_pass_candidates", test_pass, "Candidates passing test gates"),
            ("phase93_full_pass_candidates", passed, "Candidates passing both train and test gates"),
            ("phase93_best_train_net_pnl_inr", best_train, "Best train after-cost net P&L"),
            ("phase93_best_test_net_pnl_inr", best_test, "Best test after-cost net P&L"),
            ("phase93_low_turnover_event_replay_pass", int(passed > 0), "1 means at least one low-turnover event-window candidate survives"),
            (
                "phase93_recommend_next_action",
                "expand_surviving_low_turnover_event_window_with_risk_controls"
                if passed > 0
                else "stop_strategy_mining_return_to_generator_realism_calibration_audit",
                "Recommended next milestone",
            ),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase93 Low-Turnover Event-Window Replay",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase93 mechanically replays only the Phase92-precommitted low-turnover event-window candidates.",
        "No thresholds are widened. If this phase fails, the predeclared next action is to stop strategy mining and return to generator realism/calibration audit.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase93_low_turnover_event_window_replay_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase93(phase83_dir: Path, phase92_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    replay, specs, gates = load_inputs(phase83_dir, phase92_dir)
    results, monthly, symbol, trades = run_replay(replay, specs)
    acceptance = summarize(results, specs)

    specs.to_csv(output_dir / "replayed_event_window_candidate_specs.csv", index=False)
    gates.to_csv(output_dir / "locked_event_window_validation_gates.csv", index=False)
    results.to_csv(output_dir / "event_window_candidate_results.csv", index=False)
    monthly.to_csv(output_dir / "event_window_candidate_monthly.csv", index=False)
    symbol.to_csv(output_dir / "event_window_candidate_symbol.csv", index=False)
    trades.to_csv(output_dir / "event_window_candidate_trades.csv", index=False)
    acceptance.to_csv(output_dir / "event_window_replay_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Candidate Results": results,
            "Monthly Summary": monthly.head(60),
            "Symbol Summary": symbol.head(60),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {"generated_utc": generated_utc, "scope": "phase93_low_turnover_event_window_replay"}
    manifest.update(
        reproducibility_fields(
            artifact_id="phase93",
            generated_utc=generated_utc,
            inputs={
                "phase83_cached_bars": str(phase83_dir / "stratified_source_event_bars.parquet"),
                "phase92_features": str(phase92_dir / "low_turnover_event_window_features.parquet"),
                "phase92_candidate_specs": str(phase92_dir / "precommitted_event_window_candidate_specs.csv"),
                "phase92_validation_gates": str(phase92_dir / "precommitted_event_window_validation_gates.csv"),
            },
            parameters={
                "train_months": sorted(TRAIN_MONTHS),
                "test_months": sorted(TEST_MONTHS),
                "no_threshold_changes_from_phase92": True,
                "low_turnover_gate": "50_to_1500_trades_per_split",
                "stop_if_no_survivor": "return_to_generator_realism_calibration_audit",
            },
            outputs={
                "candidate_results": str(output_dir / "event_window_candidate_results.csv"),
                "monthly": str(output_dir / "event_window_candidate_monthly.csv"),
                "symbol": str(output_dir / "event_window_candidate_symbol.csv"),
                "trades": str(output_dir / "event_window_candidate_trades.csv"),
                "acceptance_summary": str(output_dir / "event_window_replay_acceptance_summary.csv"),
                "report": str(output_dir / "phase93_low_turnover_event_window_replay_report.md"),
                "manifest": str(output_dir / "phase93_low_turnover_event_window_replay_manifest.json"),
            },
            random_seed="none_deterministic_low_turnover_event_replay",
            scenario_ids="phase93_phase92_locked_low_turnover_event_candidates",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase83_source_event_ordinal_alignment",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase93_low_turnover_event_window_replay_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replay Phase92 precommitted low-turnover event-window candidates.")
    parser.add_argument("--phase83-dir", type=Path, default=DEFAULT_PHASE83_DIR)
    parser.add_argument("--phase92-dir", type=Path, default=DEFAULT_PHASE92_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase93(args.phase83_dir, args.phase92_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
