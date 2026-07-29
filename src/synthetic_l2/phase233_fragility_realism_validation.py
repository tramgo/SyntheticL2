from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE83_BARS = Path("outputs/phase83/stratified_source_event_bars.parquet")
DEFAULT_PHASE92_FEATURES = Path("outputs/phase92/low_turnover_event_window_features.parquet")
DEFAULT_PHASE232_DIR = Path("outputs/phase232")
DEFAULT_OUTPUT_DIR = Path("outputs/phase233")
ORDER_NOTIONAL_INR = 100000.0
TRAIN_MONTHS = {f"2026-{month:02d}" for month in range(1, 7)}
TEST_MONTHS = {f"2026-{month:02d}" for month in range(7, 13)}
NEIGHBOR_HORIZONS = [2, 3, 4, 5]
NEIGHBOR_QUANTILES = [0.875, 0.900, 0.925]
REALISM_COST_MULTIPLIERS = [1.0, 1.25, 1.50, 2.0]


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


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def load_event_bar_frame(features_path: Path, bars_path: Path) -> pd.DataFrame:
    features = pd.read_parquet(features_path)
    bars = pd.read_parquet(bars_path)[
        [
            "trade_month",
            "trade_date",
            "feed_profile",
            "source_event_bar_id",
            "symbol",
            "avg_l1_imbalance",
            "avg_l5_imbalance",
            "avg_microprice_dev",
            "is_market_shock_bar",
            "is_symbol_shock_bar",
        ]
    ].copy()
    frame = features.merge(
        bars,
        on=["trade_month", "trade_date", "feed_profile", "source_event_bar_id", "symbol"],
        how="left",
        validate="one_to_one",
    )
    frame = frame.sort_values(["feed_profile", "symbol", "trade_date", "source_event_bar_id"], kind="mergesort").reset_index(drop=True)
    for horizon in NEIGHBOR_HORIZONS:
        frame[f"future_return_h{horizon}"] = (
            frame.groupby(["feed_profile", "symbol", "trade_date"], sort=False)["close_mid_price"].shift(-horizon)
            / frame["close_mid_price"]
            - 1.0
        )
    frame["split"] = np.where(
        frame["trade_month"].isin(TRAIN_MONTHS),
        "train",
        np.where(frame["trade_month"].isin(TEST_MONTHS), "test", "excluded"),
    )
    return frame[frame["split"].isin(["train", "test"])].copy()


def build_neighbor_catalog(frame: pd.DataFrame, survivor: pd.Series) -> pd.DataFrame:
    train = frame[frame["split"].eq("train")]
    rows: list[dict[str, Any]] = []
    for horizon in NEIGHBOR_HORIZONS:
        for q in NEIGHBOR_QUANTILES:
            rows.append(
                {
                    "candidate_id": f"P233_MICROPRICE_REVERSAL_H{horizon}_Q{str(q).replace('.', '_')}",
                    "parent_candidate_id": survivor["candidate_id"],
                    "family_id": "P231_MICROPRICE_REVERSAL",
                    "signal_source": "avg_microprice_dev",
                    "direction": "reversal",
                    "horizon_event_bars": horizon,
                    "threshold_quantile": q,
                    "event_window_score_threshold": float(train["event_window_score"].quantile(q)),
                    "abs_microprice_dev_threshold": float(train["avg_microprice_dev"].abs().quantile(q)),
                    "parent_horizon_event_bars": survivor["horizon_event_bars"],
                    "parent_threshold_quantile": survivor["threshold_quantile"],
                }
            )
    return pd.DataFrame(rows)


def select_neighbor_trades(frame: pd.DataFrame, spec: dict[str, Any]) -> pd.DataFrame:
    horizon = int(spec["horizon_event_bars"])
    selected = frame[
        frame[f"future_return_h{horizon}"].notna()
        & frame["event_window_score"].ge(float(spec["event_window_score_threshold"]))
        & frame["avg_microprice_dev"].abs().ge(float(spec["abs_microprice_dev_threshold"]))
    ].copy()
    selected["side"] = -np.sign(selected["avg_microprice_dev"].astype(float))
    selected = selected[selected["side"].ne(0)].copy()
    selected["candidate_id"] = str(spec["candidate_id"])
    selected["parent_candidate_id"] = str(spec["parent_candidate_id"])
    selected["family_id"] = str(spec["family_id"])
    selected["horizon_event_bars"] = horizon
    selected["gross_return"] = selected["side"].astype(float) * selected[f"future_return_h{horizon}"].astype(float)
    selected["cost_return"] = selected["taker_round_trip_cost_floor_bps"].astype(float) / 10000.0
    selected["net_return"] = selected["gross_return"] - selected["cost_return"]
    selected["gross_pnl_inr"] = selected["gross_return"] * ORDER_NOTIONAL_INR
    selected["cost_pnl_drag_inr"] = selected["cost_return"] * ORDER_NOTIONAL_INR
    selected["net_pnl_inr"] = selected["net_return"] * ORDER_NOTIONAL_INR
    return selected


def split_metrics(group: pd.DataFrame, split: str, cost_multiplier: float = 1.0) -> dict[str, Any]:
    data = group[group["split"].astype(str).eq(split)].copy()
    if data.empty:
        return {
            f"{split}_trades": 0,
            f"{split}_net_pnl_inr": 0.0,
            f"{split}_gross_pnl_inr": 0.0,
            f"{split}_cost_pnl_drag_inr": 0.0,
            f"{split}_positive_months": 0,
            f"{split}_months": 0,
            f"{split}_symbols": 0,
            f"{split}_days": 0,
            f"{split}_min_month_net_pnl_inr": 0.0,
            f"{split}_leave_one_month_min_net_pnl_inr": 0.0,
            f"{split}_max_month_contribution_abs": np.nan,
            f"{split}_max_symbol_contribution_abs": np.nan,
            f"{split}_gross_to_cost_ratio": np.nan,
        }
    data["stress_net_pnl_inr"] = data["gross_pnl_inr"] - data["cost_pnl_drag_inr"] * cost_multiplier
    net = float(data["stress_net_pnl_inr"].sum())
    month_net = data.groupby("trade_month", sort=True)["stress_net_pnl_inr"].sum()
    symbol_net = data.groupby("symbol", sort=True)["stress_net_pnl_inr"].sum()
    leave_one = [net - float(value) for value in month_net.to_list()]
    denom = abs(net) if abs(net) > 0 else np.nan
    return {
        f"{split}_trades": int(len(data)),
        f"{split}_net_pnl_inr": net,
        f"{split}_gross_pnl_inr": float(data["gross_pnl_inr"].sum()),
        f"{split}_cost_pnl_drag_inr": float(data["cost_pnl_drag_inr"].sum() * cost_multiplier),
        f"{split}_positive_months": int((month_net > 0).sum()),
        f"{split}_months": int(month_net.shape[0]),
        f"{split}_symbols": int(data["symbol"].nunique()),
        f"{split}_days": int(data["trade_date"].nunique()),
        f"{split}_min_month_net_pnl_inr": float(month_net.min()),
        f"{split}_leave_one_month_min_net_pnl_inr": float(min(leave_one)) if leave_one else 0.0,
        f"{split}_max_month_contribution_abs": float(month_net.abs().max() / denom) if denom and not np.isnan(denom) else np.nan,
        f"{split}_max_symbol_contribution_abs": float(symbol_net.abs().max() / denom) if denom and not np.isnan(denom) else np.nan,
        f"{split}_gross_to_cost_ratio": abs(float(data["gross_pnl_inr"].sum())) / float(data["cost_pnl_drag_inr"].sum() * cost_multiplier)
        if float(data["cost_pnl_drag_inr"].sum() * cost_multiplier) > 0
        else np.nan,
    }


def summarize_candidate(spec: dict[str, Any], trades: pd.DataFrame) -> dict[str, Any]:
    row = dict(spec)
    row.update(split_metrics(trades, "train"))
    row.update(split_metrics(trades, "test"))
    row["train_positive"] = bool(row["train_net_pnl_inr"] > 0)
    row["test_positive"] = bool(row["test_net_pnl_inr"] > 0)
    row["test_stable"] = bool(
        row["test_net_pnl_inr"] > 0
        and row["test_positive_months"] >= 4
        and row["test_leave_one_month_min_net_pnl_inr"] > 0
        and row["test_max_month_contribution_abs"] <= 0.65
        and row["test_max_symbol_contribution_abs"] <= 0.65
    )
    row["fragility_neighbor_pass"] = bool(row["train_positive"] and row["test_stable"])
    return row


def build_neighbor_results(frame: pd.DataFrame, catalog: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    trade_frames: list[pd.DataFrame] = []
    for spec in catalog.to_dict("records"):
        trades = select_neighbor_trades(frame, spec)
        rows.append(summarize_candidate(spec, trades))
        if not trades.empty:
            keep = [
                "candidate_id",
                "parent_candidate_id",
                "family_id",
                "trade_month",
                "trade_date",
                "feed_profile",
                "source_event_bar_id",
                "symbol",
                "regime_code",
                "split",
                "horizon_event_bars",
                "side",
                "gross_return",
                "cost_return",
                "net_return",
                "gross_pnl_inr",
                "cost_pnl_drag_inr",
                "net_pnl_inr",
                "shock_bar",
                "is_market_shock_bar",
                "is_symbol_shock_bar",
            ]
            trade_frames.append(trades[keep])
    summary = pd.DataFrame(rows).sort_values(["fragility_neighbor_pass", "test_net_pnl_inr"], ascending=[False, False], kind="mergesort")
    ledger = pd.concat(trade_frames, ignore_index=True) if trade_frames else pd.DataFrame()
    return summary, ledger


def build_cost_multiplier_summary(parent_trades: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for split in ["train", "test"]:
        group = parent_trades[parent_trades["split"].astype(str).eq(split)].copy()
        for multiplier in REALISM_COST_MULTIPLIERS:
            metrics = split_metrics(group, split, cost_multiplier=multiplier)
            rows.append(
                {
                    "split": split,
                    "cost_multiplier": multiplier,
                    "net_pnl_inr": metrics[f"{split}_net_pnl_inr"],
                    "positive_months": metrics[f"{split}_positive_months"],
                    "leave_one_month_min_net_pnl_inr": metrics[f"{split}_leave_one_month_min_net_pnl_inr"],
                    "gross_to_cost_ratio": metrics[f"{split}_gross_to_cost_ratio"],
                    "cost_multiplier_pass": metrics[f"{split}_net_pnl_inr"] > 0,
                }
            )
    return pd.DataFrame(rows)


def build_realism_slice_summary(parent_trades: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    slice_defs = {
        "feed_profile": "feed_profile",
        "regime_code": "regime_code",
        "shock_bar": "shock_bar",
        "market_shock_bar": "is_market_shock_bar",
        "symbol_shock_bar": "is_symbol_shock_bar",
    }
    for split in ["train", "test"]:
        split_frame = parent_trades[parent_trades["split"].astype(str).eq(split)].copy()
        for slice_name, column in slice_defs.items():
            if column not in split_frame.columns:
                continue
            for value, group in split_frame.groupby(column, sort=True):
                net = float(group["net_pnl_inr"].sum())
                rows.append(
                    {
                        "split": split,
                        "slice_name": slice_name,
                        "slice_value": str(value),
                        "trades": int(len(group)),
                        "symbols": int(group["symbol"].nunique()),
                        "days": int(group["trade_date"].nunique()),
                        "net_pnl_inr": net,
                        "gross_pnl_inr": float(group["gross_pnl_inr"].sum()),
                        "cost_pnl_drag_inr": float(group["cost_pnl_drag_inr"].sum()),
                        "positive_slice": net > 0,
                    }
                )
    return pd.DataFrame(rows)


def build_gate_evaluation(neighbor_summary: pd.DataFrame, cost_summary: pd.DataFrame, slice_summary: pd.DataFrame, phase232_acceptance: pd.DataFrame) -> pd.DataFrame:
    inherited = as_int(metric_value(phase232_acceptance, "phase232_validated_synthetic_candidate_rows", 0))
    neighbor_pass = int(neighbor_summary["fragility_neighbor_pass"].sum()) if not neighbor_summary.empty else 0
    parent_neighbor = neighbor_summary[
        neighbor_summary["horizon_event_bars"].astype(int).eq(3)
        & np.isclose(neighbor_summary["threshold_quantile"].astype(float), 0.9)
    ]
    parent_still_pass = bool(parent_neighbor["fragility_neighbor_pass"].iloc[0]) if not parent_neighbor.empty else False
    test_cost_2x = cost_summary[cost_summary["split"].astype(str).eq("test") & cost_summary["cost_multiplier"].eq(2.0)]
    cost_2x_pass = bool(test_cost_2x["cost_multiplier_pass"].iloc[0]) if not test_cost_2x.empty else False
    test_slices = slice_summary[slice_summary["split"].astype(str).eq("test")].copy()
    feed_positive = int(test_slices[test_slices["slice_name"].eq("feed_profile")]["positive_slice"].sum()) if not test_slices.empty else 0
    regime_positive = int(test_slices[test_slices["slice_name"].eq("regime_code")]["positive_slice"].sum()) if not test_slices.empty else 0
    return pd.DataFrame(
        [
            {
                "gate_id": "P233_PHASE232_SURVIVOR_AVAILABLE",
                "passed": inherited > 0,
                "observed_value": inherited,
                "required_value": ">0 Phase232 validated candidates",
                "interpretation": "Phase233 has a validated synthetic candidate to stress.",
            },
            {
                "gate_id": "P233_PARENT_REPLAY_STILL_PASSES",
                "passed": parent_still_pass,
                "observed_value": int(parent_still_pass),
                "required_value": "1",
                "interpretation": "Parent candidate still passes under the Phase233 recomputation path.",
            },
            {
                "gate_id": "P233_PARAMETER_NEIGHBORHOOD_HAS_SURVIVORS",
                "passed": neighbor_pass >= 2,
                "observed_value": neighbor_pass,
                "required_value": ">=2 passing neighbor cells",
                "interpretation": "Candidate should not be a single-cell threshold/horizon accident.",
            },
            {
                "gate_id": "P233_TEST_2X_COST_STRESS_PASS",
                "passed": cost_2x_pass,
                "observed_value": int(cost_2x_pass),
                "required_value": "1",
                "interpretation": "Parent test split remains positive under 2x cost drag.",
            },
            {
                "gate_id": "P233_TEST_FEED_AND_REGIME_BREADTH_PASS",
                "passed": feed_positive >= 1 and regime_positive >= 2,
                "observed_value": f"feed_positive={feed_positive};regime_positive={regime_positive}",
                "required_value": ">=1 feed profile and >=2 regime slices positive",
                "interpretation": "Candidate should not depend on exactly one synthetic regime slice.",
            },
        ]
    )


def metric_frame(rows: list[tuple[str, Any, str]]) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase233 Fragility and Realism Validation",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase233 stresses the single Phase232 survivor across nearby horizons/thresholds, cost multipliers, feed/regime slices and shock slices.",
        "It remains synthetic-only validation and does not promote a strategy or permit paper/live use.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase233_fragility_realism_validation_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase233(features_path: Path, bars_path: Path, phase232_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase232_acceptance = read_csv(phase232_dir / "phase232_acceptance_summary.csv")
    phase232_validation = read_csv(phase232_dir / "phase232_candidate_validation_summary.csv")
    survivors = phase232_validation[phase232_validation["phase232_validated_synthetic_candidate"].astype(bool)].copy()
    if survivors.empty:
        survivor = pd.Series({"candidate_id": "none", "horizon_event_bars": 0, "threshold_quantile": 0.0})
    else:
        survivor = survivors.sort_values("test_net_pnl_inr", ascending=False, kind="mergesort").iloc[0]
    frame = load_event_bar_frame(features_path, bars_path)
    catalog = build_neighbor_catalog(frame, survivor)
    neighbor_summary, neighbor_ledger = build_neighbor_results(frame, catalog)
    parent_id = f"P233_MICROPRICE_REVERSAL_H3_Q0_9"
    parent_trades = neighbor_ledger[neighbor_ledger["candidate_id"].astype(str).eq(parent_id)].copy()
    cost_summary = build_cost_multiplier_summary(parent_trades)
    slice_summary = build_realism_slice_summary(parent_trades)
    gates = build_gate_evaluation(neighbor_summary, cost_summary, slice_summary, phase232_acceptance)
    passing_neighbors = int(neighbor_summary["fragility_neighbor_pass"].sum()) if not neighbor_summary.empty else 0
    test_2x = cost_summary[cost_summary["split"].astype(str).eq("test") & cost_summary["cost_multiplier"].eq(2.0)]
    test_2x_net = float(test_2x["net_pnl_inr"].iloc[0]) if not test_2x.empty else 0.0
    all_gates_pass = bool(gates["passed"].astype(bool).all()) if not gates.empty else False
    next_action = (
        "run_phase234_prepare_real_anchor_or_sealed_generator_holdout_for_phase233_candidate_no_paper_live"
        if all_gates_pass
        else "run_phase234_redesign_or_tighten_phase233_candidate_before_real_anchor"
    )
    acceptance = metric_frame(
        [
            ("phase233_fragility_realism_validation_complete", 1, "Phase233 validation completed"),
            ("phase233_phase232_survivor_rows", int(len(survivors)), "Phase232 validated candidates available"),
            ("phase233_parent_candidate_id", str(survivor.get("candidate_id", "none")), "Parent Phase232 candidate stressed"),
            ("phase233_neighbor_candidate_rows", int(len(neighbor_summary)), "Parameter-neighborhood candidates replayed"),
            ("phase233_neighbor_pass_rows", passing_neighbors, "Neighbor cells passing train/test stability"),
            ("phase233_parent_test_2x_cost_net_pnl_inr", test_2x_net, "Parent test net P&L under 2x cost drag"),
            ("phase233_gate_pass_rows", int(gates["passed"].astype(bool).sum()) if not gates.empty else 0, "Phase233 gates passed"),
            ("phase233_gate_rows", int(len(gates)), "Phase233 gates evaluated"),
            ("phase233_fragility_realism_pass", int(all_gates_pass), "1 means Phase233 candidate passes this synthetic fragility/realism layer"),
            ("phase233_strategy_promotion_allowed", 0, "No promotion from synthetic validation alone"),
            ("phase233_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from synthetic validation alone"),
            ("phase233_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from synthetic validation alone"),
            ("phase233_next_best_action", next_action, "Next validation milestone"),
        ]
    )

    catalog.to_csv(output_dir / "phase233_neighbor_candidate_catalog.csv", index=False)
    neighbor_summary.to_csv(output_dir / "phase233_neighbor_candidate_summary.csv", index=False)
    neighbor_ledger.to_csv(output_dir / "phase233_neighbor_trade_ledger.csv", index=False)
    cost_summary.to_csv(output_dir / "phase233_cost_multiplier_summary.csv", index=False)
    slice_summary.to_csv(output_dir / "phase233_realism_slice_summary.csv", index=False)
    gates.to_csv(output_dir / "phase233_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase233_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Neighbor Candidate Summary": neighbor_summary,
            "Cost Multiplier Summary": cost_summary,
            "Realism Slice Summary": slice_summary,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase233_fragility_realism_validation",
        **reproducibility_fields(
            artifact_id="phase233",
            generated_utc=generated_utc,
            inputs={
                "phase92_event_window_features": str(features_path),
                "phase83_stratified_source_event_bars": str(bars_path),
                "phase232_acceptance_summary": str(phase232_dir / "phase232_acceptance_summary.csv"),
                "phase232_candidate_validation_summary": str(phase232_dir / "phase232_candidate_validation_summary.csv"),
            },
            parameters={
                "neighbor_horizons": NEIGHBOR_HORIZONS,
                "neighbor_quantiles": NEIGHBOR_QUANTILES,
                "cost_multipliers": REALISM_COST_MULTIPLIERS,
                "parent_candidate_family": "P231_MICROPRICE_REVERSAL",
                "strategy_promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "neighbor_candidate_catalog": str(output_dir / "phase233_neighbor_candidate_catalog.csv"),
                "neighbor_candidate_summary": str(output_dir / "phase233_neighbor_candidate_summary.csv"),
                "neighbor_trade_ledger": str(output_dir / "phase233_neighbor_trade_ledger.csv"),
                "cost_multiplier_summary": str(output_dir / "phase233_cost_multiplier_summary.csv"),
                "realism_slice_summary": str(output_dir / "phase233_realism_slice_summary.csv"),
                "gate_evaluation": str(output_dir / "phase233_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase233_acceptance_summary.csv"),
                "report": str(output_dir / "phase233_fragility_realism_validation_report.md"),
                "manifest": str(output_dir / "phase233_fragility_realism_validation_manifest.json"),
            },
            random_seed="none_deterministic_phase233_fragility_grid",
            scenario_ids="phase232_survivor_microprice_reversal_fragility_grid",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase231_event_bar_horizon_cost_floor_realism_stress",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase233_fragility_realism_validation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase233 fragility and realism validation for Phase232 survivor.")
    parser.add_argument("--features-path", type=Path, default=DEFAULT_PHASE92_FEATURES)
    parser.add_argument("--bars-path", type=Path, default=DEFAULT_PHASE83_BARS)
    parser.add_argument("--phase232-dir", type=Path, default=DEFAULT_PHASE232_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase233(args.features_path, args.bars_path, args.phase232_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
