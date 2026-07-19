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
DEFAULT_PHASE90_DIR = Path("outputs/phase90")
DEFAULT_OUTPUT_DIR = Path("outputs/phase91")
TRAIN_MONTHS = {"2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"}
TEST_MONTHS = {"2026-07", "2026-08", "2026-09", "2026-10", "2026-11", "2026-12"}
ETF_SYMBOLS = {"BANKBEES", "GOLDBEES", "ITBEES", "JUNIORBEES", "NIFTYBEES"}


def load_inputs(phase83_dir: Path, phase90_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    features_path = phase90_dir / "cross_symbol_regime_features.parquet"
    specs_path = phase90_dir / "precommitted_cross_symbol_candidate_specs.csv"
    gates_path = phase90_dir / "precommitted_cross_symbol_validation_gates.csv"
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
            "bar_return",
        ]
    ].copy()
    replay = features.merge(
        bars,
        on=["trade_month", "trade_date", "feed_profile", "source_event_bar_id", "symbol"],
        how="left",
        validate="one_to_one",
    )
    return replay, pd.read_csv(specs_path), pd.read_csv(gates_path)


def apply_target_universe(frame: pd.DataFrame, target_universe: str) -> pd.DataFrame:
    out = frame[~frame["symbol"].isin(ETF_SYMBOLS)].copy()
    if "sector_symbol_count_ge_3" in str(target_universe):
        out = out[out["sector_symbol_count"].fillna(0).astype(float) >= 3.0].copy() if "sector_symbol_count" in out.columns else out
        # The compact Phase90 feature parquet does not persist sector_symbol_count.
        # Use the sector universe counts implied by available rows when the column is absent.
        if "sector_symbol_count" not in frame.columns:
            counts = out.groupby(["trade_month", "trade_date", "feed_profile", "source_event_bar_id", "sector"])["symbol"].transform("nunique")
            out = out[counts >= 3].copy()
    return out


def candidate_trades(replay: pd.DataFrame, spec: dict[str, Any]) -> pd.DataFrame:
    feature_col = str(spec["feature_column"])
    intensity_col = str(spec["intensity_column"])
    selected = apply_target_universe(replay, str(spec["target_universe"]))
    selected = selected[
        selected["next_bar_return"].notna()
        & selected[feature_col].abs().ge(float(spec["feature_abs_threshold"]))
        & selected[intensity_col].abs().ge(float(spec["intensity_abs_threshold"]))
        & selected["taker_round_trip_cost_floor_bps"].le(float(spec["max_taker_round_trip_cost_floor_bps"]))
    ].copy()
    if selected.empty:
        return selected
    if str(spec["direction_rule"]).strip().startswith("side = -sign"):
        selected["side"] = -np.sign(selected[feature_col].astype(float))
    else:
        selected["side"] = np.sign(selected[feature_col].astype(float))
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


def concentration(group: pd.DataFrame, by: str, total_net: float) -> float:
    if group.empty or abs(total_net) <= 0:
        return np.nan
    component = group.groupby(by, sort=True)["net_pnl_inr"].sum()
    return float(component.abs().max() / abs(total_net))


def split_metrics(trades: pd.DataFrame, split: str) -> dict[str, Any]:
    if trades.empty or "split" not in trades.columns:
        group = pd.DataFrame()
    else:
        group = trades[trades["split"].eq(split)].copy()
    if group.empty:
        return {
            f"{split}_trades": 0,
            f"{split}_symbols": 0,
            f"{split}_months": 0,
            f"{split}_net_pnl_inr": 0.0,
            f"{split}_gross_pnl_inr": 0.0,
            f"{split}_cost_pnl_drag_inr": 0.0,
            f"{split}_precision_cost_clear": 0.0,
            f"{split}_positive_months": 0,
            f"{split}_max_month_contribution_abs": np.nan,
            f"{split}_max_symbol_contribution_abs": np.nan,
            f"{split}_cost_drag_to_abs_gross_ratio": np.nan,
        }
    total_net = float(group["net_pnl_inr"].sum())
    gross = float(group["gross_pnl_inr"].sum())
    cost = float(group["cost_pnl_drag_inr"].sum())
    month_net = group.groupby("trade_month", sort=True)["net_pnl_inr"].sum()
    return {
        f"{split}_trades": int(len(group)),
        f"{split}_symbols": int(group["symbol"].nunique()),
        f"{split}_months": int(month_net.shape[0]),
        f"{split}_net_pnl_inr": total_net,
        f"{split}_gross_pnl_inr": gross,
        f"{split}_cost_pnl_drag_inr": cost,
        f"{split}_precision_cost_clear": float((group["gross_return"] > group["cost_return"]).mean()),
        f"{split}_positive_months": int((month_net > 0).sum()),
        f"{split}_max_month_contribution_abs": concentration(group, "trade_month", total_net),
        f"{split}_max_symbol_contribution_abs": concentration(group, "symbol", total_net),
        f"{split}_cost_drag_to_abs_gross_ratio": cost / abs(gross) if abs(gross) > 0 else np.nan,
    }


def evaluate_candidate(spec: dict[str, Any], trades: pd.DataFrame) -> dict[str, Any]:
    row = dict(spec)
    row.update(split_metrics(trades, "train"))
    row.update(split_metrics(trades, "test"))
    row["train_pass"] = bool(
        row["train_net_pnl_inr"] > 0
        and 500 <= row["train_trades"] <= 8000
        and row["train_symbols"] >= 20
        and row["train_precision_cost_clear"] >= 0.55
    )
    row["test_pass"] = bool(
        row["test_net_pnl_inr"] > 0
        and 500 <= row["test_trades"] <= 8000
        and row["test_symbols"] >= 20
        and row["test_precision_cost_clear"] >= 0.55
        and row["test_positive_months"] >= 4
        and pd.notna(row["test_max_month_contribution_abs"])
        and row["test_max_month_contribution_abs"] <= 0.35
        and pd.notna(row["test_max_symbol_contribution_abs"])
        and row["test_max_symbol_contribution_abs"] <= 0.35
    )
    row["phase91_candidate_pass"] = bool(row["train_pass"] and row["test_pass"])
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
        ["phase91_candidate_pass", "test_net_pnl_inr"], ascending=[False, False], kind="mergesort"
    )
    trades_all = pd.concat(trade_frames, ignore_index=True) if trade_frames else pd.DataFrame()
    monthly_all = pd.concat(monthly_rows, ignore_index=True) if monthly_rows else pd.DataFrame()
    symbol_all = pd.concat(symbol_rows, ignore_index=True) if symbol_rows else pd.DataFrame()
    return results, monthly_all, symbol_all, trades_all


def summarize(results: pd.DataFrame, specs: pd.DataFrame) -> pd.DataFrame:
    passed = int(results["phase91_candidate_pass"].sum()) if not results.empty else 0
    train_pass = int(results["train_pass"].sum()) if not results.empty else 0
    test_pass = int(results["test_pass"].sum()) if not results.empty else 0
    best_test = float(results["test_net_pnl_inr"].max()) if not results.empty else 0.0
    best_train = float(results["train_net_pnl_inr"].max()) if not results.empty else 0.0
    return pd.DataFrame(
        [
            ("phase91_precommitted_candidate_rows", int(len(specs)), "Phase90 candidate specs replayed without threshold changes"),
            ("phase91_train_pass_candidates", train_pass, "Candidates passing train gates"),
            ("phase91_test_pass_candidates", test_pass, "Candidates passing test gates"),
            ("phase91_full_pass_candidates", passed, "Candidates passing both train and test gates"),
            ("phase91_best_train_net_pnl_inr", best_train, "Best train after-cost net P&L"),
            ("phase91_best_test_net_pnl_inr", best_test, "Best test after-cost net P&L"),
            ("phase91_cross_symbol_replay_pass", int(passed > 0), "1 means at least one cross-symbol candidate survives"),
            (
                "phase91_recommend_next_action",
                "expand_surviving_cross_symbol_family_with_risk_controls"
                if passed > 0
                else "retire_cross_symbol_imbalance_or_move_to_low_turnover_event_window_design",
                "Recommended next milestone",
            ),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase91 Cross-Symbol Regime-Imbalance Replay",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase91 mechanically replays only the Phase90-precommitted cross-symbol/regime imbalance candidates.",
        "No thresholds are widened in this phase. Train/test, turnover, cost, breadth and concentration gates are applied exactly as locked.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase91_cross_symbol_regime_imbalance_replay_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase91(phase83_dir: Path, phase90_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    replay, specs, gates = load_inputs(phase83_dir, phase90_dir)
    results, monthly, symbol, trades = run_replay(replay, specs)
    acceptance = summarize(results, specs)

    specs.to_csv(output_dir / "replayed_cross_symbol_candidate_specs.csv", index=False)
    gates.to_csv(output_dir / "locked_cross_symbol_validation_gates.csv", index=False)
    results.to_csv(output_dir / "cross_symbol_candidate_results.csv", index=False)
    monthly.to_csv(output_dir / "cross_symbol_candidate_monthly.csv", index=False)
    symbol.to_csv(output_dir / "cross_symbol_candidate_symbol.csv", index=False)
    trades.to_csv(output_dir / "cross_symbol_candidate_trades.csv", index=False)
    acceptance.to_csv(output_dir / "cross_symbol_replay_acceptance_summary.csv", index=False)
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
    manifest: dict[str, Any] = {"generated_utc": generated_utc, "scope": "phase91_cross_symbol_regime_imbalance_replay"}
    manifest.update(
        reproducibility_fields(
            artifact_id="phase91",
            generated_utc=generated_utc,
            inputs={
                "phase83_cached_bars": str(phase83_dir / "stratified_source_event_bars.parquet"),
                "phase90_features": str(phase90_dir / "cross_symbol_regime_features.parquet"),
                "phase90_candidate_specs": str(phase90_dir / "precommitted_cross_symbol_candidate_specs.csv"),
                "phase90_validation_gates": str(phase90_dir / "precommitted_cross_symbol_validation_gates.csv"),
            },
            parameters={
                "train_months": sorted(TRAIN_MONTHS),
                "test_months": sorted(TEST_MONTHS),
                "no_threshold_changes_from_phase90": True,
                "turnover_gate": "500_to_8000_trades_per_split",
                "concentration_gate": "max_symbol_and_month_contribution_abs_le_0_35",
            },
            outputs={
                "candidate_results": str(output_dir / "cross_symbol_candidate_results.csv"),
                "monthly": str(output_dir / "cross_symbol_candidate_monthly.csv"),
                "symbol": str(output_dir / "cross_symbol_candidate_symbol.csv"),
                "trades": str(output_dir / "cross_symbol_candidate_trades.csv"),
                "acceptance_summary": str(output_dir / "cross_symbol_replay_acceptance_summary.csv"),
                "report": str(output_dir / "phase91_cross_symbol_regime_imbalance_replay_report.md"),
                "manifest": str(output_dir / "phase91_cross_symbol_regime_imbalance_replay_manifest.json"),
            },
            random_seed="none_deterministic_cross_symbol_replay",
            scenario_ids="phase91_phase90_locked_cross_symbol_candidates",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase83_source_event_ordinal_alignment",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase91_cross_symbol_regime_imbalance_replay_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replay Phase90 precommitted cross-symbol regime-imbalance candidates.")
    parser.add_argument("--phase83-dir", type=Path, default=DEFAULT_PHASE83_DIR)
    parser.add_argument("--phase90-dir", type=Path, default=DEFAULT_PHASE90_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase91(args.phase83_dir, args.phase90_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
