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


DEFAULT_PHASE83_DIR = Path("outputs/phase83")
DEFAULT_OUTPUT_DIR = Path("outputs/phase89")
OBSERVATION_SAMPLE_ROWS = 50_000
TRAIN_MONTHS = {"2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"}
TEST_MONTHS = {"2026-07", "2026-08", "2026-09", "2026-10", "2026-11", "2026-12"}


FILL_ASSUMPTIONS = [
    {
        "fill_assumption": "pessimistic_queue",
        "base_fill_prob": 0.12,
        "adverse_multiplier": 2.50,
        "favorable_multiplier": 0.25,
        "shock_multiplier": 0.65,
        "max_fill_prob": 0.35,
    },
    {
        "fill_assumption": "base_queue",
        "base_fill_prob": 0.25,
        "adverse_multiplier": 1.75,
        "favorable_multiplier": 0.50,
        "shock_multiplier": 0.80,
        "max_fill_prob": 0.60,
    },
    {
        "fill_assumption": "optimistic_queue",
        "base_fill_prob": 0.45,
        "adverse_multiplier": 1.25,
        "favorable_multiplier": 0.75,
        "shock_multiplier": 1.00,
        "max_fill_prob": 0.85,
    },
]


def load_bars(phase83_dir: Path) -> pd.DataFrame:
    path = phase83_dir / "stratified_source_event_bars.parquet"
    if not path.exists():
        raise FileNotFoundError(path)
    bars = pd.read_parquet(path)
    required = {
        "trade_month",
        "trade_date",
        "symbol",
        "regime_code",
        "avg_spread",
        "close_mid_price",
        "avg_l1_imbalance",
        "avg_l5_imbalance",
        "avg_microprice_dev",
        "avg_event_intensity_proxy",
        "is_market_shock_bar",
        "is_symbol_shock_bar",
        "next_bar_return",
    }
    missing = sorted(required.difference(bars.columns))
    if missing:
        raise ValueError(f"Phase83 bars are missing required columns: {missing}")
    return bars[bars["next_bar_return"].notna()].copy()


def add_cost_floor_columns(bars: pd.DataFrame) -> pd.DataFrame:
    frame = bars.copy()
    charges = calculate_equity_intraday_nse_charges(
        buy_value_inr=DEFAULT_ORDER_NOTIONAL_INR,
        sell_value_inr=DEFAULT_ORDER_NOTIONAL_INR,
        buy_quantity=1.0,
        sell_quantity=1.0,
        buy_orders=1,
        sell_orders=1,
    )
    frame["zerodha_round_trip_charge_bps"] = float(charges.breakeven_bps_on_buy_value)
    frame["half_spread_bps"] = (
        frame["avg_spread"].astype(float) / frame["close_mid_price"].replace(0, np.nan).astype(float) * 10000.0 / 2.0
    )
    frame["passive_round_trip_cost_floor_bps"] = frame["zerodha_round_trip_charge_bps"]
    frame["taker_round_trip_spread_penalty_bps"] = frame["half_spread_bps"] * 2.0
    return frame


def build_candidate_specs(bars: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    feature_defs = [
        ("l1_imbalance", "avg_l1_imbalance", "side = sign(avg_l1_imbalance)"),
        ("l5_imbalance", "avg_l5_imbalance", "side = sign(avg_l5_imbalance)"),
        ("microprice_dev", "avg_microprice_dev", "side = sign(avg_microprice_dev)"),
    ]
    intensity_thresholds = bars["avg_event_intensity_proxy"].quantile([0.50, 0.75]).to_dict()
    feature_thresholds: dict[str, dict[float, float]] = {}
    for _, col, _ in feature_defs:
        feature_thresholds[col] = bars[col].abs().quantile([0.50, 0.75, 0.90]).to_dict()
    for feature_name, col, direction_rule in feature_defs:
        for feature_q, feature_threshold in feature_thresholds[col].items():
            for intensity_q, intensity_threshold in intensity_thresholds.items():
                rows.append(
                    {
                        "candidate_id": f"P89_{feature_name.upper()}_Q{str(feature_q).replace('.', '_')}_I{str(intensity_q).replace('.', '_')}",
                        "feature_name": feature_name,
                        "feature_column": col,
                        "direction_rule": direction_rule,
                        "feature_abs_quantile": float(feature_q),
                        "feature_abs_threshold": float(feature_threshold),
                        "event_intensity_quantile": float(intensity_q),
                        "event_intensity_threshold": float(intensity_threshold),
                    }
                )
    return pd.DataFrame(rows)


def candidate_observations(bars: pd.DataFrame, spec: dict[str, Any]) -> pd.DataFrame:
    col = str(spec["feature_column"])
    selected = bars[
        (bars[col].abs().astype(float) >= float(spec["feature_abs_threshold"]))
        & (bars["avg_event_intensity_proxy"].astype(float) >= float(spec["event_intensity_threshold"]))
    ].copy()
    if selected.empty:
        return selected
    selected["side"] = np.sign(selected[col].astype(float))
    selected = selected[selected["side"].ne(0)].copy()
    if selected.empty:
        return selected
    selected["candidate_id"] = spec["candidate_id"]
    selected["feature_name"] = spec["feature_name"]
    selected["adverse_selection"] = (selected["side"].astype(float) * selected["next_bar_return"].astype(float)) < 0.0
    selected["favorable_selection"] = (selected["side"].astype(float) * selected["next_bar_return"].astype(float)) > 0.0
    selected["shock_bar"] = selected["is_market_shock_bar"].astype(bool) | selected["is_symbol_shock_bar"].astype(bool)
    selected["gross_passive_capture_return"] = (
        selected["side"].astype(float) * selected["next_bar_return"].astype(float)
        + (selected["half_spread_bps"].astype(float) / 10000.0)
    )
    selected["charge_return"] = selected["passive_round_trip_cost_floor_bps"].astype(float) / 10000.0
    selected["net_if_filled_return"] = selected["gross_passive_capture_return"] - selected["charge_return"]
    selected["gross_if_filled_pnl_inr"] = selected["gross_passive_capture_return"] * DEFAULT_ORDER_NOTIONAL_INR
    selected["cost_if_filled_pnl_inr"] = selected["charge_return"] * DEFAULT_ORDER_NOTIONAL_INR
    selected["net_if_filled_pnl_inr"] = selected["net_if_filled_return"] * DEFAULT_ORDER_NOTIONAL_INR
    selected["split"] = np.where(
        selected["trade_month"].isin(TRAIN_MONTHS),
        "train",
        np.where(selected["trade_month"].isin(TEST_MONTHS), "test", "excluded"),
    )
    return selected[selected["split"].isin(["train", "test"])].copy()


def apply_fill_assumption(observations: pd.DataFrame, assumption: dict[str, Any]) -> pd.DataFrame:
    if observations.empty:
        return observations
    frame = observations.copy()
    fill_prob = np.full(len(frame), float(assumption["base_fill_prob"]), dtype=float)
    fill_prob = np.where(frame["adverse_selection"].astype(bool), fill_prob * float(assumption["adverse_multiplier"]), fill_prob)
    fill_prob = np.where(frame["favorable_selection"].astype(bool), fill_prob * float(assumption["favorable_multiplier"]), fill_prob)
    fill_prob = np.where(frame["shock_bar"].astype(bool), fill_prob * float(assumption["shock_multiplier"]), fill_prob)
    frame["fill_assumption"] = str(assumption["fill_assumption"])
    frame["fill_probability"] = np.clip(fill_prob, 0.0, float(assumption["max_fill_prob"]))
    frame["expected_net_pnl_inr"] = frame["fill_probability"] * frame["net_if_filled_pnl_inr"]
    frame["expected_gross_pnl_inr"] = frame["fill_probability"] * frame["gross_if_filled_pnl_inr"]
    frame["expected_cost_pnl_inr"] = frame["fill_probability"] * frame["cost_if_filled_pnl_inr"]
    return frame


def split_metrics(trades: pd.DataFrame, split: str) -> dict[str, Any]:
    group = trades[trades["split"].eq(split)]
    if group.empty:
        return {
            f"{split}_observations": 0,
            f"{split}_expected_fills": 0.0,
            f"{split}_symbols": 0,
            f"{split}_months": 0,
            f"{split}_expected_net_pnl_inr": 0.0,
            f"{split}_adverse_selection_rate": 0.0,
            f"{split}_positive_months": 0,
            f"{split}_max_month_contribution_abs": np.nan,
        }
    month_net = group.groupby("trade_month", sort=True)["expected_net_pnl_inr"].sum()
    total_net = float(group["expected_net_pnl_inr"].sum())
    max_contrib = float(month_net.abs().max() / abs(total_net)) if abs(total_net) > 0 else np.nan
    return {
        f"{split}_observations": int(len(group)),
        f"{split}_expected_fills": float(group["fill_probability"].sum()),
        f"{split}_symbols": int(group["symbol"].nunique()),
        f"{split}_months": int(month_net.shape[0]),
        f"{split}_expected_net_pnl_inr": total_net,
        f"{split}_adverse_selection_rate": float(group["adverse_selection"].mean()),
        f"{split}_positive_months": int((month_net > 0).sum()),
        f"{split}_max_month_contribution_abs": max_contrib,
    }


def evaluate_candidate_assumption(spec: dict[str, Any], assumption: dict[str, Any], trades: pd.DataFrame) -> dict[str, Any]:
    row = dict(spec)
    row.update({k: v for k, v in assumption.items() if k != "fill_assumption"})
    row["fill_assumption"] = assumption["fill_assumption"]
    row.update(split_metrics(trades, "train"))
    row.update(split_metrics(trades, "test"))
    row["train_pass"] = bool(
        row["train_expected_net_pnl_inr"] > 0
        and row["train_expected_fills"] >= 500
        and row["train_symbols"] >= 20
        and row["train_adverse_selection_rate"] <= 0.58
    )
    row["test_pass"] = bool(
        row["test_expected_net_pnl_inr"] > 0
        and row["test_expected_fills"] >= 500
        and row["test_symbols"] >= 20
        and row["test_positive_months"] >= 4
        and row["test_adverse_selection_rate"] <= 0.58
        and (pd.notna(row["test_max_month_contribution_abs"]) and row["test_max_month_contribution_abs"] <= 0.50)
    )
    row["assumption_pass"] = bool(row["train_pass"] and row["test_pass"])
    return row


def run_replay(bars: pd.DataFrame, specs: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    result_rows: list[dict[str, Any]] = []
    trade_frames: list[pd.DataFrame] = []
    monthly_rows: list[pd.DataFrame] = []
    for spec in specs.to_dict("records"):
        observations = candidate_observations(bars, spec)
        for assumption in FILL_ASSUMPTIONS:
            trades = apply_fill_assumption(observations, assumption)
            result_rows.append(evaluate_candidate_assumption(spec, assumption, trades))
            if not trades.empty:
                trade_frames.append(trades)
                monthly_rows.append(
                    trades.groupby(["candidate_id", "feature_name", "fill_assumption", "split", "trade_month"], sort=True)
                    .agg(
                        observations=("symbol", "count"),
                        expected_fills=("fill_probability", "sum"),
                        symbols=("symbol", "nunique"),
                        expected_net_pnl_inr=("expected_net_pnl_inr", "sum"),
                        expected_gross_pnl_inr=("expected_gross_pnl_inr", "sum"),
                        expected_cost_pnl_inr=("expected_cost_pnl_inr", "sum"),
                        adverse_selection_rate=("adverse_selection", "mean"),
                    )
                    .reset_index()
                )
    results = pd.DataFrame(result_rows).sort_values(
        ["assumption_pass", "test_expected_net_pnl_inr"], ascending=[False, False], kind="mergesort"
    )
    trades_all = pd.concat(trade_frames, ignore_index=True) if trade_frames else pd.DataFrame()
    monthly_all = pd.concat(monthly_rows, ignore_index=True) if monthly_rows else pd.DataFrame()
    return results, monthly_all, trades_all


def build_candidate_survival(results: pd.DataFrame) -> pd.DataFrame:
    if results.empty:
        return pd.DataFrame()
    grouped = results.groupby("candidate_id", sort=True)
    rows = []
    for candidate_id, group in grouped:
        passed_assumptions = set(group.loc[group["assumption_pass"].astype(bool), "fill_assumption"].astype(str))
        all_pass = all(item["fill_assumption"] in passed_assumptions for item in FILL_ASSUMPTIONS)
        rows.append(
            {
                "candidate_id": candidate_id,
                "feature_name": group["feature_name"].iloc[0],
                "assumptions_passed": "|".join(sorted(passed_assumptions)),
                "all_fill_assumptions_pass": bool(all_pass),
                "best_test_expected_net_pnl_inr": float(group["test_expected_net_pnl_inr"].max()),
                "worst_test_expected_net_pnl_inr": float(group["test_expected_net_pnl_inr"].min()),
                "max_test_adverse_selection_rate": float(group["test_adverse_selection_rate"].max()),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["all_fill_assumptions_pass", "worst_test_expected_net_pnl_inr"], ascending=[False, False], kind="mergesort"
    )


def summarize(results: pd.DataFrame, survival: pd.DataFrame, specs: pd.DataFrame) -> pd.DataFrame:
    assumption_pass_rows = int(results["assumption_pass"].sum()) if not results.empty else 0
    robust_candidates = int(survival["all_fill_assumptions_pass"].sum()) if not survival.empty else 0
    best_test = float(results["test_expected_net_pnl_inr"].max()) if not results.empty else 0.0
    worst_best = float(survival["worst_test_expected_net_pnl_inr"].max()) if not survival.empty else 0.0
    return pd.DataFrame(
        [
            ("phase89_candidate_specs", int(len(specs)), "Passive feature candidates evaluated"),
            ("phase89_fill_assumption_rows", int(len(results)), "Candidate/fill-assumption rows evaluated"),
            ("phase89_assumption_pass_rows", assumption_pass_rows, "Candidate/fill rows passing train and test gates"),
            ("phase89_all_assumption_survivor_candidates", robust_candidates, "Candidates passing pessimistic, base and optimistic fill assumptions"),
            ("phase89_best_test_expected_net_pnl_inr", best_test, "Best test expected net P&L under any fill assumption"),
            ("phase89_best_worst_case_test_expected_net_pnl_inr", worst_best, "Best candidate worst-case test expected net P&L across assumptions"),
            ("phase89_passive_queue_cost_floor_pass", int(robust_candidates > 0), "1 means a passive candidate clears the cost floor under all fill assumptions"),
            (
                "phase89_recommend_next_action",
                "precommit_passive_queue_replay_with_risk_controls"
                if robust_candidates > 0
                else "retire_simple_passive_imbalance_or_design_richer_passive_features",
                "Recommended next milestone",
            ),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase89 Passive Queue-Capture Cost-Floor Experiment",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase89 starts the post-pivot feature class from Phase88.",
        "It evaluates hypothetical passive L1 queue-capture candidates with pessimistic, base and optimistic fill assumptions.",
        "Entry selection uses only current-bar features; next-bar movement is used only for markout/adverse-selection evaluation.",
        "Optimistic-only profitability is not accepted as a survivor.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase89_passive_queue_capture_cost_floor_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase89(phase83_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    bars = add_cost_floor_columns(load_bars(phase83_dir))
    specs = build_candidate_specs(bars)
    results, monthly, trades = run_replay(bars, specs)
    survival = build_candidate_survival(results)
    acceptance = summarize(results, survival, specs)

    specs.to_csv(output_dir / "passive_candidate_specs.csv", index=False)
    results.to_csv(output_dir / "passive_candidate_fill_assumption_results.csv", index=False)
    survival.to_csv(output_dir / "passive_candidate_survival_summary.csv", index=False)
    monthly.to_csv(output_dir / "passive_candidate_monthly.csv", index=False)
    observation_sample = trades.head(OBSERVATION_SAMPLE_ROWS).copy() if not trades.empty else trades
    observation_sample.to_csv(output_dir / "passive_candidate_observation_sample.csv", index=False)
    acceptance.to_csv(output_dir / "passive_queue_cost_floor_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Candidate Survival Summary": survival.head(20),
            "Fill Assumption Results": results.head(30),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {"generated_utc": generated_utc, "scope": "phase89_passive_queue_capture_cost_floor"}
    manifest.update(
        reproducibility_fields(
            artifact_id="phase89",
            generated_utc=generated_utc,
            inputs={"phase83_cached_bars": str(phase83_dir / "stratified_source_event_bars.parquet")},
            parameters={
                "train_months": sorted(TRAIN_MONTHS),
                "test_months": sorted(TEST_MONTHS),
                "fill_assumptions": FILL_ASSUMPTIONS,
                "passive_cost_floor": "Zerodha round-trip statutory/brokerage charges; no taker spread crossing",
                "survival_policy": "candidate must pass pessimistic, base and optimistic fill assumptions",
            },
            outputs={
                "candidate_specs": str(output_dir / "passive_candidate_specs.csv"),
                "fill_assumption_results": str(output_dir / "passive_candidate_fill_assumption_results.csv"),
                "survival_summary": str(output_dir / "passive_candidate_survival_summary.csv"),
                "monthly": str(output_dir / "passive_candidate_monthly.csv"),
                "observation_sample": str(output_dir / "passive_candidate_observation_sample.csv"),
                "acceptance_summary": str(output_dir / "passive_queue_cost_floor_acceptance_summary.csv"),
                "report": str(output_dir / "phase89_passive_queue_capture_cost_floor_report.md"),
                "manifest": str(output_dir / "phase89_passive_queue_capture_cost_floor_manifest.json"),
            },
            random_seed="none_deterministic_passive_cost_floor",
            scenario_ids="phase89_post_phase88_passive_queue_capture",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_event_bar_passive_assumption_catalog",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase89_passive_queue_capture_cost_floor_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase89 passive queue-capture cost-floor experiment.")
    parser.add_argument("--phase83-dir", type=Path, default=DEFAULT_PHASE83_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase89(args.phase83_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
