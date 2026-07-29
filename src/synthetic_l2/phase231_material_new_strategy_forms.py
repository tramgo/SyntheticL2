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
DEFAULT_PHASE230_DIR = Path("outputs/phase230")
DEFAULT_OUTPUT_DIR = Path("outputs/phase231")
ORDER_NOTIONAL_INR = 100000.0
TRAIN_MONTHS = {f"2026-{month:02d}" for month in range(1, 7)}
TEST_MONTHS = {f"2026-{month:02d}" for month in range(7, 13)}
HORIZONS = [3, 6, 12]
THRESHOLD_QUANTILES = [0.90, 0.95, 0.975, 0.99]
FAMILIES = [
    {
        "family_id": "P231_EVENT_CONTINUATION",
        "signal_source": "bar_return",
        "direction": "continuation",
        "feature_filter": "event_window_score_and_abs_bar_return",
    },
    {
        "family_id": "P231_EVENT_REVERSAL",
        "signal_source": "bar_return",
        "direction": "reversal",
        "feature_filter": "event_window_score_and_abs_bar_return",
    },
    {
        "family_id": "P231_L5_IMBALANCE_CONTINUATION",
        "signal_source": "avg_l5_imbalance",
        "direction": "continuation",
        "feature_filter": "event_window_score_and_abs_l5_imbalance",
    },
    {
        "family_id": "P231_L5_IMBALANCE_REVERSAL",
        "signal_source": "avg_l5_imbalance",
        "direction": "reversal",
        "feature_filter": "event_window_score_and_abs_l5_imbalance",
    },
    {
        "family_id": "P231_MICROPRICE_CONTINUATION",
        "signal_source": "avg_microprice_dev",
        "direction": "continuation",
        "feature_filter": "event_window_score_and_abs_microprice_dev",
    },
    {
        "family_id": "P231_MICROPRICE_REVERSAL",
        "signal_source": "avg_microprice_dev",
        "direction": "reversal",
        "feature_filter": "event_window_score_and_abs_microprice_dev",
    },
]


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
        ]
    ].copy()
    frame = features.merge(
        bars,
        on=["trade_month", "trade_date", "feed_profile", "source_event_bar_id", "symbol"],
        how="left",
        validate="one_to_one",
    )
    frame = frame.sort_values(["feed_profile", "symbol", "trade_date", "source_event_bar_id"], kind="mergesort").reset_index(drop=True)
    for horizon in HORIZONS:
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


def train_thresholds(frame: pd.DataFrame) -> dict[float, dict[str, float]]:
    train = frame[frame["split"].eq("train")]
    thresholds: dict[float, dict[str, float]] = {}
    for q in THRESHOLD_QUANTILES:
        thresholds[q] = {
            "event_window_score_threshold": float(train["event_window_score"].quantile(q)),
            "abs_bar_return_bps_threshold": float(train["abs_bar_return_bps"].quantile(q)),
            "abs_l5_imbalance_threshold": float(train["avg_l5_imbalance"].abs().quantile(q)),
            "abs_microprice_dev_threshold": float(train["avg_microprice_dev"].abs().quantile(q)),
        }
    return thresholds


def build_candidate_catalog(thresholds: dict[float, dict[str, float]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for family in FAMILIES:
        for horizon in HORIZONS:
            for q in THRESHOLD_QUANTILES:
                threshold = thresholds[q]
                rows.append(
                    {
                        "candidate_id": f"{family['family_id']}_H{horizon}_Q{str(q).replace('.', '_')}",
                        "family_id": family["family_id"],
                        "signal_source": family["signal_source"],
                        "direction": family["direction"],
                        "feature_filter": family["feature_filter"],
                        "horizon_event_bars": horizon,
                        "threshold_quantile": q,
                        **threshold,
                        "train_months": "|".join(sorted(TRAIN_MONTHS)),
                        "test_months": "|".join(sorted(TEST_MONTHS)),
                    }
                )
    return pd.DataFrame(rows)


def select_trades(frame: pd.DataFrame, spec: dict[str, Any]) -> pd.DataFrame:
    horizon = int(spec["horizon_event_bars"])
    selected = frame[frame[f"future_return_h{horizon}"].notna() & frame["event_window_score"].ge(float(spec["event_window_score_threshold"]))].copy()
    source = str(spec["signal_source"])
    if source == "bar_return":
        selected = selected[selected["abs_bar_return_bps"].ge(float(spec["abs_bar_return_bps_threshold"]))].copy()
        raw_side = np.sign(selected["bar_return"].astype(float))
    elif source == "avg_l5_imbalance":
        selected = selected[selected["avg_l5_imbalance"].abs().ge(float(spec["abs_l5_imbalance_threshold"]))].copy()
        raw_side = np.sign(selected["avg_l5_imbalance"].astype(float))
    elif source == "avg_microprice_dev":
        selected = selected[selected["avg_microprice_dev"].abs().ge(float(spec["abs_microprice_dev_threshold"]))].copy()
        raw_side = np.sign(selected["avg_microprice_dev"].astype(float))
    else:
        raise ValueError(f"Unsupported signal_source: {source}")
    side = raw_side if str(spec["direction"]) == "continuation" else -raw_side
    selected["side"] = side
    selected = selected[selected["side"].ne(0)].copy()
    selected["candidate_id"] = str(spec["candidate_id"])
    selected["family_id"] = str(spec["family_id"])
    selected["horizon_event_bars"] = horizon
    selected["gross_return"] = selected["side"].astype(float) * selected[f"future_return_h{horizon}"].astype(float)
    selected["cost_return"] = selected["taker_round_trip_cost_floor_bps"].astype(float) / 10000.0
    selected["net_return"] = selected["gross_return"] - selected["cost_return"]
    selected["gross_pnl_inr"] = selected["gross_return"] * ORDER_NOTIONAL_INR
    selected["cost_pnl_drag_inr"] = selected["cost_return"] * ORDER_NOTIONAL_INR
    selected["net_pnl_inr"] = selected["net_return"] * ORDER_NOTIONAL_INR
    return selected


def contribution(group: pd.DataFrame, by: str, total_net: float) -> float:
    if group.empty or abs(total_net) <= 0:
        return np.nan
    values = group.groupby(by, sort=True)["net_pnl_inr"].sum()
    return float(values.abs().max() / abs(total_net))


def split_metrics(trades: pd.DataFrame, split: str) -> dict[str, Any]:
    group = trades[trades["split"].eq(split)].copy() if not trades.empty else pd.DataFrame()
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
            f"{split}_gross_to_cost_ratio": np.nan,
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
        f"{split}_gross_to_cost_ratio": abs(gross) / cost if cost > 0 else np.nan,
    }


def evaluate_candidate(spec: dict[str, Any], trades: pd.DataFrame) -> dict[str, Any]:
    row = dict(spec)
    row.update(split_metrics(trades, "train"))
    row.update(split_metrics(trades, "test"))
    row["train_pass"] = bool(
        row["train_net_pnl_inr"] > 0
        and 20 <= row["train_trades"] <= 5000
        and row["train_symbols"] >= 3
        and row["train_days"] >= 4
        and row["train_precision_cost_clear"] >= 0.53
        and pd.notna(row["train_gross_to_cost_ratio"])
        and row["train_gross_to_cost_ratio"] >= 1.10
    )
    row["test_pass"] = bool(
        row["test_net_pnl_inr"] > 0
        and 20 <= row["test_trades"] <= 5000
        and row["test_symbols"] >= 3
        and row["test_days"] >= 4
        and row["test_precision_cost_clear"] >= 0.53
        and row["test_positive_months"] >= 2
        and pd.notna(row["test_gross_to_cost_ratio"])
        and row["test_gross_to_cost_ratio"] >= 1.10
        and pd.notna(row["test_max_day_trade_fraction"])
        and row["test_max_day_trade_fraction"] <= 0.25
    )
    row["phase231_synthetic_candidate"] = bool(row["train_pass"] and row["test_pass"])
    return row


def run_candidate_replay(frame: pd.DataFrame, catalog: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    trade_frames: list[pd.DataFrame] = []
    for spec in catalog.to_dict("records"):
        trades = select_trades(frame, spec)
        rows.append(evaluate_candidate(spec, trades))
        if not trades.empty:
            keep_cols = [
                "candidate_id",
                "family_id",
                "trade_month",
                "trade_date",
                "feed_profile",
                "source_event_bar_id",
                "symbol",
                "split",
                "horizon_event_bars",
                "side",
                "gross_return",
                "cost_return",
                "net_return",
                "gross_pnl_inr",
                "cost_pnl_drag_inr",
                "net_pnl_inr",
            ]
            trade_frames.append(trades[keep_cols].copy())
    summary = pd.DataFrame(rows).sort_values(
        ["phase231_synthetic_candidate", "test_net_pnl_inr", "train_net_pnl_inr"],
        ascending=[False, False, False],
        kind="mergesort",
    )
    trade_ledger = pd.concat(trade_frames, ignore_index=True) if trade_frames else pd.DataFrame()
    return summary, trade_ledger


def build_family_summary(summary: pd.DataFrame) -> pd.DataFrame:
    if summary.empty:
        return pd.DataFrame()
    return (
        summary.groupby("family_id", sort=True)
        .agg(
            candidate_rows=("candidate_id", "count"),
            train_pass_rows=("train_pass", "sum"),
            test_pass_rows=("test_pass", "sum"),
            synthetic_candidate_rows=("phase231_synthetic_candidate", "sum"),
            best_train_net_pnl_inr=("train_net_pnl_inr", "max"),
            best_test_net_pnl_inr=("test_net_pnl_inr", "max"),
            best_test_precision_cost_clear=("test_precision_cost_clear", "max"),
        )
        .reset_index()
        .sort_values(["synthetic_candidate_rows", "best_test_net_pnl_inr"], ascending=[False, False], kind="mergesort")
    )


def build_gate_evaluation(summary: pd.DataFrame, phase230_acceptance: pd.DataFrame) -> pd.DataFrame:
    candidate_rows = int(len(summary))
    train_pass = int(summary["train_pass"].sum()) if not summary.empty else 0
    test_pass = int(summary["test_pass"].sum()) if not summary.empty else 0
    synthetic_candidates = int(summary["phase231_synthetic_candidate"].sum()) if not summary.empty else 0
    inherited_positive = as_int(metric_value(phase230_acceptance, "phase230_positive_expanded_group_rows", 0))
    return pd.DataFrame(
        [
            {
                "gate_id": "P231_PHASE230_HANDOFF_CONFIRMED",
                "passed": inherited_positive == 0,
                "observed_value": inherited_positive,
                "required_value": "0 positive Phase230 expanded groups",
                "interpretation": "Phase231 is justified by Phase230 failure of old signal variants.",
            },
            {
                "gate_id": "P231_MATERIAL_NEW_CANDIDATES_REPLAYED",
                "passed": candidate_rows >= len(FAMILIES) * len(HORIZONS),
                "observed_value": candidate_rows,
                "required_value": ">=18 candidates",
                "interpretation": "Materially new event-bar strategy forms were replayed.",
            },
            {
                "gate_id": "P231_TRAIN_PASS_CANDIDATES_FOUND",
                "passed": train_pass > 0,
                "observed_value": train_pass,
                "required_value": ">0 train-pass candidates",
                "interpretation": "At least one new candidate clears train economics and breadth gates.",
            },
            {
                "gate_id": "P231_TEST_PASS_CANDIDATES_FOUND",
                "passed": test_pass > 0,
                "observed_value": test_pass,
                "required_value": ">0 test-pass candidates",
                "interpretation": "At least one new candidate clears test economics and breadth gates.",
            },
            {
                "gate_id": "P231_SYNTHETIC_CANDIDATES_FOUND",
                "passed": synthetic_candidates > 0,
                "observed_value": synthetic_candidates,
                "required_value": ">0 train+test pass candidates",
                "interpretation": "Positive synthetic candidates exist, subject to stricter holdout and realism checks before any promotion.",
            },
        ]
    )


def metric_frame(rows: list[tuple[str, Any, str]]) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase231 Material New Strategy Forms",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase231 executes materially new longer-horizon event-bar strategy forms after Phase230 showed that",
        "filtering or inverting the old Phase164 signals could not clear realistic modeled costs.",
        "This is still synthetic-only candidate evidence, not strategy promotion, paper/live acceptance, or a deployable profitability claim.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase231_material_new_strategy_forms_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase231(features_path: Path, bars_path: Path, phase230_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase230_acceptance = read_csv(phase230_dir / "phase230_strategy_search_acceptance_summary.csv")
    frame = load_event_bar_frame(features_path, bars_path)
    thresholds = train_thresholds(frame)
    catalog = build_candidate_catalog(thresholds)
    summary, trade_ledger = run_candidate_replay(frame, catalog)
    family_summary = build_family_summary(summary)
    gates = build_gate_evaluation(summary, phase230_acceptance)
    best = summary.head(1)
    synthetic_candidates = int(summary["phase231_synthetic_candidate"].sum()) if not summary.empty else 0
    next_action = (
        "run_phase232_validate_phase231_candidates_on_stricter_holdout_and_negative_controls_no_paper_live"
        if synthetic_candidates > 0
        else "run_phase232_design_new_edge_source_or_stop_strategy_search"
    )
    acceptance = metric_frame(
        [
            ("phase231_material_new_strategy_forms_complete", 1, "Phase231 replay completed"),
            ("phase231_event_bar_rows", int(len(frame)), "Event-bar rows scanned"),
            ("phase231_candidate_rows", int(len(summary)), "Candidate strategy forms replayed"),
            ("phase231_trade_ledger_rows", int(len(trade_ledger)), "Selected candidate trade rows"),
            ("phase231_train_pass_candidates", int(summary["train_pass"].sum()) if not summary.empty else 0, "Candidates passing train gates"),
            ("phase231_test_pass_candidates", int(summary["test_pass"].sum()) if not summary.empty else 0, "Candidates passing test gates"),
            ("phase231_synthetic_candidate_rows", synthetic_candidates, "Candidates passing both train and test gates"),
            ("phase231_best_candidate_id", best["candidate_id"].iloc[0] if not best.empty else "none", "Best candidate by pass status and test P&L"),
            ("phase231_best_family_id", best["family_id"].iloc[0] if not best.empty else "none", "Best candidate family"),
            ("phase231_best_train_net_pnl_inr", float(best["train_net_pnl_inr"].iloc[0]) if not best.empty else 0.0, "Best candidate train net P&L"),
            ("phase231_best_test_net_pnl_inr", float(best["test_net_pnl_inr"].iloc[0]) if not best.empty else 0.0, "Best candidate test net P&L"),
            ("phase231_best_test_precision_cost_clear", float(best["test_precision_cost_clear"].iloc[0]) if not best.empty else 0.0, "Best candidate test precision cost-clear fraction"),
            ("phase231_strategy_promotion_allowed", 0, "No promotion from synthetic candidate search alone"),
            ("phase231_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from synthetic candidate search alone"),
            ("phase231_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from synthetic candidate search alone"),
            ("phase231_next_best_action", next_action, "Next validation milestone"),
        ]
    )

    catalog.to_csv(output_dir / "phase231_candidate_catalog.csv", index=False)
    summary.to_csv(output_dir / "phase231_candidate_summary.csv", index=False)
    family_summary.to_csv(output_dir / "phase231_family_summary.csv", index=False)
    trade_ledger.to_csv(output_dir / "phase231_trade_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase231_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase231_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Top Candidate Summary": summary.head(15),
            "Family Summary": family_summary,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase231_material_new_strategy_forms",
        **reproducibility_fields(
            artifact_id="phase231",
            generated_utc=generated_utc,
            inputs={
                "phase92_event_window_features": str(features_path),
                "phase83_stratified_source_event_bars": str(bars_path),
                "phase230_acceptance_summary": str(phase230_dir / "phase230_strategy_search_acceptance_summary.csv"),
            },
            parameters={
                "train_months": sorted(TRAIN_MONTHS),
                "test_months": sorted(TEST_MONTHS),
                "horizon_event_bars": HORIZONS,
                "threshold_quantiles": THRESHOLD_QUANTILES,
                "families": [family["family_id"] for family in FAMILIES],
                "order_notional_inr": ORDER_NOTIONAL_INR,
                "strategy_promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "candidate_catalog": str(output_dir / "phase231_candidate_catalog.csv"),
                "candidate_summary": str(output_dir / "phase231_candidate_summary.csv"),
                "family_summary": str(output_dir / "phase231_family_summary.csv"),
                "trade_ledger": str(output_dir / "phase231_trade_ledger.csv"),
                "gate_evaluation": str(output_dir / "phase231_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase231_acceptance_summary.csv"),
                "report": str(output_dir / "phase231_material_new_strategy_forms_report.md"),
                "manifest": str(output_dir / "phase231_material_new_strategy_forms_manifest.json"),
            },
            random_seed="none_deterministic_phase231_event_bar_replay",
            scenario_ids="phase83_phase92_event_bar_full_year_train_test",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="event_bar_horizon_replay_cost_floor_no_broker_promotion",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase231_material_new_strategy_forms_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replay materially new longer-horizon event-bar strategy forms.")
    parser.add_argument("--features-path", type=Path, default=DEFAULT_PHASE92_FEATURES)
    parser.add_argument("--bars-path", type=Path, default=DEFAULT_PHASE83_BARS)
    parser.add_argument("--phase230-dir", type=Path, default=DEFAULT_PHASE230_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase231(
        features_path=args.features_path,
        bars_path=args.bars_path,
        phase230_dir=args.phase230_dir,
        output_dir=args.output_dir,
        base_dir=args.base_dir,
    )


if __name__ == "__main__":
    main()
