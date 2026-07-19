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
DEFAULT_PHASE91_DIR = Path("outputs/phase91")
DEFAULT_OUTPUT_DIR = Path("outputs/phase92")
TRAIN_MONTHS = {"2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"}
TEST_MONTHS = {"2026-07", "2026-08", "2026-09", "2026-10", "2026-11", "2026-12"}


def metric_value(path: Path, metric: str, default: Any = None) -> Any:
    if not path.exists():
        return default
    frame = pd.read_csv(path)
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    value = rows.iloc[0]
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def load_bars(phase83_dir: Path) -> pd.DataFrame:
    path = phase83_dir / "stratified_source_event_bars.parquet"
    if not path.exists():
        raise FileNotFoundError(path)
    bars = pd.read_parquet(path)
    required = {
        "trade_month",
        "trade_date",
        "feed_profile",
        "symbol",
        "regime_code",
        "source_event_bar_id",
        "close_mid_price",
        "avg_spread",
        "avg_l1_imbalance",
        "avg_l5_imbalance",
        "avg_microprice_dev",
        "avg_event_intensity_proxy",
        "is_market_shock_bar",
        "is_symbol_shock_bar",
        "bar_return",
    }
    missing = sorted(required.difference(bars.columns))
    if missing:
        raise ValueError(f"Phase83 bars are missing required columns: {missing}")
    return bars.copy()


def add_event_design_features(bars: pd.DataFrame) -> pd.DataFrame:
    charges = calculate_equity_intraday_nse_charges(
        buy_value_inr=DEFAULT_ORDER_NOTIONAL_INR,
        sell_value_inr=DEFAULT_ORDER_NOTIONAL_INR,
        buy_quantity=1.0,
        sell_quantity=1.0,
        buy_orders=1,
        sell_orders=1,
    )
    frame = bars.copy()
    frame["zerodha_round_trip_charge_bps"] = float(charges.breakeven_bps_on_buy_value)
    frame["spread_bps"] = frame["avg_spread"].astype(float) / frame["close_mid_price"].replace(0, np.nan).astype(float) * 10000.0
    frame["taker_round_trip_cost_floor_bps"] = frame["spread_bps"] + frame["zerodha_round_trip_charge_bps"]
    frame["abs_bar_return_bps"] = frame["bar_return"].abs().astype(float) * 10000.0
    frame["shock_bar"] = frame["is_market_shock_bar"].astype(bool) | frame["is_symbol_shock_bar"].astype(bool)
    frame["book_dislocation_score"] = (
        frame["avg_l1_imbalance"].abs().astype(float)
        + frame["avg_l5_imbalance"].abs().astype(float)
        + frame["avg_microprice_dev"].abs().astype(float) * 10000.0
    )
    frame["event_window_score"] = (
        frame["abs_bar_return_bps"].astype(float)
        * np.log1p(frame["avg_event_intensity_proxy"].clip(lower=0).astype(float))
        / frame["taker_round_trip_cost_floor_bps"].replace(0, np.nan).astype(float)
    )
    return frame


def train_quantile(frame: pd.DataFrame, column: str, quantile: float) -> float:
    train = frame[frame["trade_month"].isin(TRAIN_MONTHS)]
    values = train[column].replace([np.inf, -np.inf], np.nan).dropna()
    if values.empty:
        return 0.0
    return float(values.quantile(quantile))


def build_event_families() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "family_id": "P92_SHOCK_EXHAUSTION_REVERSAL",
                "hypothesis": "Large shock/event-window bars may overextend and reverse after immediate liquidity exhaustion.",
                "direction_rule": "side = -sign(bar_return)",
                "required_filters": "shock_bar AND abs_bar_return_bps threshold AND event_window_score threshold AND cost_floor threshold",
                "target_holding_period": "next_source_event_bar",
                "turnover_intent": "low_turnover_event_only",
                "why_not_posthoc": "Shock exhaustion is precommitted after Phase91 failure and before Phase93 replay.",
            },
            {
                "family_id": "P92_SHOCK_CONTINUATION",
                "hypothesis": "Some high-intensity shock bars may continue when the event-window score is extreme enough to clear retail costs.",
                "direction_rule": "side = sign(bar_return)",
                "required_filters": "shock_bar AND abs_bar_return_bps threshold AND event_window_score threshold AND cost_floor threshold",
                "target_holding_period": "next_source_event_bar",
                "turnover_intent": "low_turnover_event_only",
                "why_not_posthoc": "Continuation is locked as the competing hypothesis, not chosen after inspecting replay P&L.",
            },
            {
                "family_id": "P92_BOOK_DISLOCATION_REVERSAL",
                "hypothesis": "Extreme book dislocation with large current move may revert when displayed L1/L5 pressure is stretched.",
                "direction_rule": "side = -sign(bar_return)",
                "required_filters": "book_dislocation_score threshold AND abs_bar_return_bps threshold AND event_window_score threshold AND cost_floor threshold",
                "target_holding_period": "next_source_event_bar",
                "turnover_intent": "low_turnover_event_only",
                "why_not_posthoc": "Book-dislocation threshold is feature-only and train-period calibrated before replay.",
            },
        ]
    )


def build_candidate_specs(features: pd.DataFrame, families: pd.DataFrame) -> pd.DataFrame:
    train = features[features["trade_month"].isin(TRAIN_MONTHS)]
    cost_p50 = float(train["taker_round_trip_cost_floor_bps"].quantile(0.50))
    rows: list[dict[str, Any]] = []
    for family in families.to_dict("records"):
        for event_q in [0.95, 0.975]:
            for move_q in [0.95, 0.975]:
                dislocation_q = 0.95 if family["family_id"] == "P92_BOOK_DISLOCATION_REVERSAL" else 0.0
                rows.append(
                    {
                        "candidate_id": (
                            f"{family['family_id']}_E{str(event_q).replace('.', '_')}_M{str(move_q).replace('.', '_')}"
                        ),
                        "family_id": family["family_id"],
                        "direction_rule": family["direction_rule"],
                        "requires_shock_bar": family["family_id"] in {"P92_SHOCK_EXHAUSTION_REVERSAL", "P92_SHOCK_CONTINUATION"},
                        "event_window_score_quantile": event_q,
                        "event_window_score_threshold": train_quantile(features, "event_window_score", event_q),
                        "abs_bar_return_bps_quantile": move_q,
                        "abs_bar_return_bps_threshold": train_quantile(features, "abs_bar_return_bps", move_q),
                        "book_dislocation_score_quantile": dislocation_q,
                        "book_dislocation_score_threshold": train_quantile(features, "book_dislocation_score", dislocation_q)
                        if dislocation_q
                        else 0.0,
                        "max_taker_round_trip_cost_floor_bps": cost_p50,
                        "train_months": "|".join(sorted(TRAIN_MONTHS)),
                        "test_months": "|".join(sorted(TEST_MONTHS)),
                    }
                )
    return pd.DataFrame(rows)


def build_validation_gates() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "gate_id": "P92_NO_LABEL_INSPECTION",
                "requirement": "Phase92 may compute event-window features and train thresholds only; no directional P&L or next_bar_return replay is evaluated.",
                "pass_threshold": "No candidate selected using replay P&L.",
            },
            {
                "gate_id": "P92_LOW_TURNOVER",
                "requirement": "Replay must be low turnover: 50 to 1500 trades per split, at least 10 symbols, and no daily burst over 10% of split trades.",
                "pass_threshold": "50<=trades<=1500; symbols>=10; max_day_trade_fraction<=0.10",
            },
            {
                "gate_id": "P92_COST_FLOOR",
                "requirement": "Only rows below the train p50 taker round-trip cost floor may trade, and gross edge must clear at least 1.5x realized cost drag on test.",
                "pass_threshold": "cost_floor_filter=1; test_abs_gross_to_cost_drag_ratio>=1.5",
            },
            {
                "gate_id": "P92_AFTER_COST_SURVIVAL",
                "requirement": "After-cost net P&L must be positive in train and test with precision_cost_clear >= 0.56.",
                "pass_threshold": "train_net>0; test_net>0; train_precision>=0.56; test_precision>=0.56",
            },
            {
                "gate_id": "P92_MONTH_AND_SYMBOL_BREADTH",
                "requirement": "At least 4 test months positive; no single month or symbol may contribute more than 40% of absolute test net P&L.",
                "pass_threshold": "test_positive_months>=4; max_month_contribution_abs<=0.40; max_symbol_contribution_abs<=0.40",
            },
            {
                "gate_id": "P92_RETIREMENT",
                "requirement": "If no low-turnover event-window candidate passes, stop strategy mining and return to generator realism/calibration audit.",
                "pass_threshold": "No threshold widening in Phase93.",
            },
        ]
    )


def build_feature_diagnostics(features: pd.DataFrame) -> pd.DataFrame:
    train = features[features["trade_month"].isin(TRAIN_MONTHS)]
    rows = []
    for column in ["event_window_score", "abs_bar_return_bps", "book_dislocation_score", "taker_round_trip_cost_floor_bps"]:
        values = train[column].replace([np.inf, -np.inf], np.nan).dropna()
        rows.append(
            {
                "feature": column,
                "train_rows": int(values.shape[0]),
                "train_p50": float(values.quantile(0.50)) if not values.empty else 0.0,
                "train_p90": float(values.quantile(0.90)) if not values.empty else 0.0,
                "train_p95": float(values.quantile(0.95)) if not values.empty else 0.0,
                "train_p975": float(values.quantile(0.975)) if not values.empty else 0.0,
            }
        )
    return pd.DataFrame(rows)


def summarize(features: pd.DataFrame, families: pd.DataFrame, specs: pd.DataFrame, gates: pd.DataFrame, phase91_dir: Path) -> pd.DataFrame:
    phase91_pass = metric_value(phase91_dir / "cross_symbol_replay_acceptance_summary.csv", "phase91_cross_symbol_replay_pass", 1)
    ready = int(len(features) > 0 and len(families) == 3 and len(specs) == 12 and len(gates) >= 6 and float(phase91_pass) == 0)
    return pd.DataFrame(
        [
            ("phase92_event_feature_rows", int(len(features)), "Event-window design rows built from Phase83 cached bars"),
            ("phase92_train_rows", int(features["trade_month"].isin(TRAIN_MONTHS).sum()), "Train rows used for feature thresholds"),
            ("phase92_test_rows", int(features["trade_month"].isin(TEST_MONTHS).sum()), "Locked test rows reserved for Phase93 replay"),
            ("phase92_signal_family_rows", int(len(families)), "Low-turnover event-window families precommitted"),
            ("phase92_candidate_spec_rows", int(len(specs)), "Candidate specs precommitted"),
            ("phase92_validation_gate_rows", int(len(gates)), "Validation gates locked"),
            ("phase92_phase91_cross_symbol_pass", int(float(phase91_pass)), "Phase91 pass flag used only as pivot context"),
            ("phase92_ready_for_replay", ready, "1 means Phase93 low-turnover event replay may run"),
            ("phase92_recommend_next_action", "run_precommitted_low_turnover_event_window_replay", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase92 Low-Turnover Event-Window Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase92 precommits a lower-turnover event-window feature class after Phase91 falsified simple cross-symbol imbalance.",
        "It computes feature-only thresholds from train months and locks replay gates before Phase93 inspects next-bar outcomes.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase92_low_turnover_event_window_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase92(phase83_dir: Path, phase91_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    features = add_event_design_features(load_bars(phase83_dir))
    families = build_event_families()
    specs = build_candidate_specs(features, families)
    gates = build_validation_gates()
    diagnostics = build_feature_diagnostics(features)
    acceptance = summarize(features, families, specs, gates, phase91_dir)

    feature_columns = [
        "trade_month",
        "trade_date",
        "feed_profile",
        "source_event_bar_id",
        "symbol",
        "regime_code",
        "close_mid_price",
        "spread_bps",
        "taker_round_trip_cost_floor_bps",
        "avg_event_intensity_proxy",
        "shock_bar",
        "bar_return",
        "abs_bar_return_bps",
        "book_dislocation_score",
        "event_window_score",
    ]
    features[feature_columns].to_parquet(output_dir / "low_turnover_event_window_features.parquet", index=False)
    diagnostics.to_csv(output_dir / "event_window_feature_diagnostics.csv", index=False)
    families.to_csv(output_dir / "precommitted_event_window_signal_families.csv", index=False)
    specs.to_csv(output_dir / "precommitted_event_window_candidate_specs.csv", index=False)
    gates.to_csv(output_dir / "precommitted_event_window_validation_gates.csv", index=False)
    acceptance.to_csv(output_dir / "event_window_precommit_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Feature Diagnostics": diagnostics,
            "Precommitted Signal Families": families,
            "Candidate Specs": specs,
            "Validation Gates": gates,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {"generated_utc": generated_utc, "scope": "phase92_low_turnover_event_window_precommit"}
    manifest.update(
        reproducibility_fields(
            artifact_id="phase92",
            generated_utc=generated_utc,
            inputs={
                "phase83_cached_bars": str(phase83_dir / "stratified_source_event_bars.parquet"),
                "phase91_cross_symbol_summary": str(phase91_dir / "cross_symbol_replay_acceptance_summary.csv"),
            },
            parameters={
                "train_months": sorted(TRAIN_MONTHS),
                "test_months": sorted(TEST_MONTHS),
                "candidate_quantiles": {"event_window_score": [0.95, 0.975], "abs_bar_return_bps": [0.95, 0.975]},
                "no_label_inspection": True,
                "low_turnover_policy": "50_to_1500_trades_per_split_in_phase93",
            },
            outputs={
                "features": str(output_dir / "low_turnover_event_window_features.parquet"),
                "diagnostics": str(output_dir / "event_window_feature_diagnostics.csv"),
                "families": str(output_dir / "precommitted_event_window_signal_families.csv"),
                "candidate_specs": str(output_dir / "precommitted_event_window_candidate_specs.csv"),
                "validation_gates": str(output_dir / "precommitted_event_window_validation_gates.csv"),
                "acceptance_summary": str(output_dir / "event_window_precommit_acceptance_summary.csv"),
                "report": str(output_dir / "phase92_low_turnover_event_window_precommit_report.md"),
                "manifest": str(output_dir / "phase92_low_turnover_event_window_precommit_manifest.json"),
            },
            random_seed="none_deterministic_event_window_precommit",
            scenario_ids="phase92_post_phase91_low_turnover_event_window",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase83_source_event_ordinal_alignment",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase92_low_turnover_event_window_precommit_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Precommit low-turnover event-window replay.")
    parser.add_argument("--phase83-dir", type=Path, default=DEFAULT_PHASE83_DIR)
    parser.add_argument("--phase91-dir", type=Path, default=DEFAULT_PHASE91_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase92(args.phase83_dir, args.phase91_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
