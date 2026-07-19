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
DEFAULT_PHASE88_DIR = Path("outputs/phase88")
DEFAULT_PHASE89_DIR = Path("outputs/phase89")
DEFAULT_OUTPUT_DIR = Path("outputs/phase90")
TRAIN_MONTHS = {"2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"}
TEST_MONTHS = {"2026-07", "2026-08", "2026-09", "2026-10", "2026-11", "2026-12"}


SYMBOL_SECTOR = {
    "ADANIPORTS": "infrastructure",
    "AXISBANK": "private_bank",
    "BAJAJ-AUTO": "auto",
    "BANKBEES": "bank_etf",
    "BHARTIARTL": "telecom",
    "BPCL": "energy",
    "BRITANNIA": "fmcg",
    "CIPLA": "pharma",
    "DRREDDY": "pharma",
    "GOLDBEES": "gold_etf",
    "HCLTECH": "it",
    "HDFCBANK": "private_bank",
    "HINDUNILVR": "fmcg",
    "ICICIBANK": "private_bank",
    "INFY": "it",
    "ITBEES": "it_etf",
    "ITC": "fmcg",
    "JUNIORBEES": "broad_etf",
    "KOTAKBANK": "private_bank",
    "LT": "infrastructure",
    "M&M": "auto",
    "MARUTI": "auto",
    "NESTLEIND": "fmcg",
    "NIFTYBEES": "broad_etf",
    "ONGC": "energy",
    "RELIANCE": "energy",
    "SBIN": "public_bank",
    "SUNPHARMA": "pharma",
    "TCS": "it",
    "TECHM": "it",
    "ULTRACEMCO": "materials",
    "WIPRO": "it",
}

ETF_SYMBOLS = {"BANKBEES", "GOLDBEES", "ITBEES", "JUNIORBEES", "NIFTYBEES"}


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
        "source_event_bar_id",
        "regime_code",
        "close_mid_price",
        "avg_spread",
        "avg_l1_imbalance",
        "avg_l5_imbalance",
        "avg_microprice_dev",
        "avg_event_intensity_proxy",
        "bar_return",
        "next_bar_return",
    }
    missing = sorted(required.difference(bars.columns))
    if missing:
        raise ValueError(f"Phase83 bars are missing required columns: {missing}")
    frame = bars.copy()
    frame["sector"] = frame["symbol"].map(SYMBOL_SECTOR).fillna("unknown")
    frame["is_etf"] = frame["symbol"].isin(ETF_SYMBOLS)
    return frame


def add_cost_floor(frame: pd.DataFrame) -> pd.DataFrame:
    charges = calculate_equity_intraday_nse_charges(
        buy_value_inr=DEFAULT_ORDER_NOTIONAL_INR,
        sell_value_inr=DEFAULT_ORDER_NOTIONAL_INR,
        buy_quantity=1.0,
        sell_quantity=1.0,
        buy_orders=1,
        sell_orders=1,
    )
    out = frame.copy()
    out["zerodha_round_trip_charge_bps"] = float(charges.breakeven_bps_on_buy_value)
    out["spread_bps"] = out["avg_spread"].astype(float) / out["close_mid_price"].replace(0, np.nan).astype(float) * 10000.0
    out["taker_round_trip_cost_floor_bps"] = out["spread_bps"] + out["zerodha_round_trip_charge_bps"]
    return out


def build_cross_symbol_features(bars: pd.DataFrame) -> pd.DataFrame:
    keys = ["trade_month", "trade_date", "feed_profile", "source_event_bar_id"]
    frame = add_cost_floor(bars)
    frame["signed_l1_pressure"] = frame["avg_l1_imbalance"].astype(float)
    frame["signed_l5_pressure"] = frame["avg_l5_imbalance"].astype(float)
    frame["signed_microprice_pressure"] = frame["avg_microprice_dev"].astype(float)

    market = (
        frame.groupby(keys, sort=False)
        .agg(
            market_l1_pressure_sum=("signed_l1_pressure", "sum"),
            market_l5_pressure_sum=("signed_l5_pressure", "sum"),
            market_microprice_pressure_sum=("signed_microprice_pressure", "sum"),
            market_symbol_count=("symbol", "nunique"),
            market_event_intensity=("avg_event_intensity_proxy", "mean"),
        )
        .reset_index()
    )
    sector = (
        frame.groupby(keys + ["sector"], sort=False)
        .agg(
            sector_l1_pressure_sum=("signed_l1_pressure", "sum"),
            sector_l5_pressure_sum=("signed_l5_pressure", "sum"),
            sector_microprice_pressure_sum=("signed_microprice_pressure", "sum"),
            sector_symbol_count=("symbol", "nunique"),
            sector_event_intensity=("avg_event_intensity_proxy", "mean"),
        )
        .reset_index()
    )
    out = frame.merge(market, on=keys, how="left").merge(sector, on=keys + ["sector"], how="left")
    market_den = (out["market_symbol_count"].astype(float) - 1.0).replace(0, np.nan)
    sector_den = (out["sector_symbol_count"].astype(float) - 1.0).replace(0, np.nan)
    out["x_market_l1_ex_target"] = (out["market_l1_pressure_sum"] - out["signed_l1_pressure"]) / market_den
    out["x_market_l5_ex_target"] = (out["market_l5_pressure_sum"] - out["signed_l5_pressure"]) / market_den
    out["x_market_microprice_ex_target"] = (out["market_microprice_pressure_sum"] - out["signed_microprice_pressure"]) / market_den
    out["x_sector_l1_ex_target"] = (out["sector_l1_pressure_sum"] - out["signed_l1_pressure"]) / sector_den
    out["x_sector_l5_ex_target"] = (out["sector_l5_pressure_sum"] - out["signed_l5_pressure"]) / sector_den
    out["x_sector_microprice_ex_target"] = (out["sector_microprice_pressure_sum"] - out["signed_microprice_pressure"]) / sector_den
    out["x_symbol_vs_sector_l1"] = out["signed_l1_pressure"] - out["x_sector_l1_ex_target"]
    out["x_symbol_vs_sector_l5"] = out["signed_l5_pressure"] - out["x_sector_l5_ex_target"]
    out["x_market_regime_intensity"] = out["market_event_intensity"] * out["x_market_l5_ex_target"].abs()
    out["x_sector_regime_intensity"] = out["sector_event_intensity"] * out["x_sector_l5_ex_target"].abs()
    return out


def train_quantile(frame: pd.DataFrame, column: str, quantile: float) -> float:
    train = frame[frame["trade_month"].isin(TRAIN_MONTHS)]
    values = train[column].replace([np.inf, -np.inf], np.nan).dropna().abs()
    if values.empty:
        return 0.0
    return float(values.quantile(quantile))


def build_signal_families(features: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "family_id": "P90_MARKET_IMBALANCE_CONTINUATION",
                "hypothesis": "When broad same-bar ex-target market L5 imbalance is extreme and event intensity is high, target symbols may continue in the same direction over the next event bar.",
                "feature_column": "x_market_l5_ex_target",
                "direction_rule": "side = sign(x_market_l5_ex_target)",
                "target_universe": "equities_only",
                "required_filters": "abs(x_market_l5_ex_target) threshold AND x_market_regime_intensity threshold AND taker_round_trip_cost_floor_bps <= train_p60_cost_floor_bps",
                "turnover_policy": "max 1 signal per symbol per trade_date/feed_profile/source_event_bar_id; candidate replay must cap test trades by predeclared gate",
                "why_not_posthoc": "Family is defined after Phase89 failure and before any Phase90 directional P&L replay.",
            },
            {
                "family_id": "P90_SECTOR_IMBALANCE_CONTINUATION",
                "hypothesis": "When ex-target sector L5 imbalance is extreme, lower-turnover sector-context signals may transfer to target symbols.",
                "feature_column": "x_sector_l5_ex_target",
                "direction_rule": "side = sign(x_sector_l5_ex_target)",
                "target_universe": "equities_only_with_sector_symbol_count_ge_3",
                "required_filters": "abs(x_sector_l5_ex_target) threshold AND x_sector_regime_intensity threshold AND taker_round_trip_cost_floor_bps <= train_p60_cost_floor_bps",
                "turnover_policy": "max 1 signal per symbol per trade_date/feed_profile/source_event_bar_id; no symbol may exceed concentration gate",
                "why_not_posthoc": "Uses sector map and train feature thresholds only; no next_bar_return inspection.",
            },
            {
                "family_id": "P90_SYMBOL_SECTOR_DIVERGENCE_REVERSION",
                "hypothesis": "When a symbol's own L1 pressure diverges from its sector ex-target pressure, the symbol may mean-revert toward sector pressure over the next event bar.",
                "feature_column": "x_symbol_vs_sector_l1",
                "direction_rule": "side = -sign(x_symbol_vs_sector_l1)",
                "target_universe": "equities_only_with_sector_symbol_count_ge_3",
                "required_filters": "abs(x_symbol_vs_sector_l1) threshold AND sector_event_intensity threshold AND taker_round_trip_cost_floor_bps <= train_p60_cost_floor_bps",
                "turnover_policy": "max 1 signal per symbol per trade_date/feed_profile/source_event_bar_id; require broad symbol/month survival",
                "why_not_posthoc": "Divergence/reversion hypothesis is locked before replay and competes with continuation families.",
            },
        ]
    )


def build_candidate_specs(features: pd.DataFrame, families: pd.DataFrame) -> pd.DataFrame:
    train = features[features["trade_month"].isin(TRAIN_MONTHS)].copy()
    cost_floor = float(train["taker_round_trip_cost_floor_bps"].quantile(0.60))
    rows: list[dict[str, Any]] = []
    for family in families.to_dict("records"):
        feature_col = str(family["feature_column"])
        intensity_col = (
            "x_market_regime_intensity"
            if "MARKET" in str(family["family_id"])
            else "x_sector_regime_intensity"
            if "SECTOR_IMBALANCE" in str(family["family_id"])
            else "sector_event_intensity"
        )
        for feature_q in [0.90, 0.95]:
            for intensity_q in [0.75, 0.90]:
                rows.append(
                    {
                        "candidate_id": (
                            f"{family['family_id']}_F{str(feature_q).replace('.', '_')}_I{str(intensity_q).replace('.', '_')}"
                        ),
                        "family_id": family["family_id"],
                        "feature_column": feature_col,
                        "direction_rule": family["direction_rule"],
                        "target_universe": family["target_universe"],
                        "feature_abs_quantile": feature_q,
                        "feature_abs_threshold": train_quantile(features, feature_col, feature_q),
                        "intensity_column": intensity_col,
                        "intensity_abs_quantile": intensity_q,
                        "intensity_abs_threshold": train_quantile(features, intensity_col, intensity_q),
                        "max_taker_round_trip_cost_floor_bps": cost_floor,
                        "train_months": "|".join(sorted(TRAIN_MONTHS)),
                        "test_months": "|".join(sorted(TEST_MONTHS)),
                    }
                )
    return pd.DataFrame(rows)


def build_validation_gates() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "gate_id": "P90_NO_LABEL_INSPECTION",
                "requirement": "Phase90 may compute cross-symbol features and train-period feature thresholds only; directional P&L and next_bar_return labels are reserved for replay.",
                "pass_threshold": "No candidate is selected or edited using replay P&L.",
            },
            {
                "gate_id": "P90_SPLIT_LOCK",
                "requirement": "Train months are 2026-01 through 2026-06; test months are 2026-07 through 2026-12.",
                "pass_threshold": "Splits appear in every candidate spec and cannot be changed in replay.",
            },
            {
                "gate_id": "P90_COST_BUDGET",
                "requirement": "Replay may only trade rows at or below the train-period p60 taker round-trip cost floor for the relevant cached bars.",
                "pass_threshold": "taker_round_trip_cost_floor_bps <= max_taker_round_trip_cost_floor_bps",
            },
            {
                "gate_id": "P90_TURNOVER_BREADTH",
                "requirement": "Replay candidate must have 500 to 8000 trades per split and at least 20 target symbols in both train and test.",
                "pass_threshold": "500<=train_trades<=8000; 500<=test_trades<=8000; train_symbols>=20; test_symbols>=20",
            },
            {
                "gate_id": "P90_AFTER_COST_SURVIVAL",
                "requirement": "Replay must produce positive after-cost net P&L in both train and test with precision_cost_clear >= 0.55.",
                "pass_threshold": "train_net_pnl_inr>0; test_net_pnl_inr>0; train_precision>=0.55; test_precision>=0.55",
            },
            {
                "gate_id": "P90_CONCENTRATION",
                "requirement": "No single symbol or month may contribute more than 35% of absolute positive test net P&L.",
                "pass_threshold": "max_symbol_contribution_abs<=0.35; max_month_contribution_abs<=0.35",
            },
            {
                "gate_id": "P90_RETIREMENT",
                "requirement": "If no precommitted candidate passes, do not widen thresholds in the same family; move to P91 event-window low-turnover design.",
                "pass_threshold": "No post-hoc threshold widening.",
            },
        ]
    )


def build_feature_diagnostics(features: pd.DataFrame) -> pd.DataFrame:
    train = features[features["trade_month"].isin(TRAIN_MONTHS)].copy()
    rows = []
    for column in [
        "x_market_l5_ex_target",
        "x_sector_l5_ex_target",
        "x_symbol_vs_sector_l1",
        "x_market_regime_intensity",
        "x_sector_regime_intensity",
        "taker_round_trip_cost_floor_bps",
    ]:
        values = train[column].replace([np.inf, -np.inf], np.nan).dropna()
        rows.append(
            {
                "feature": column,
                "train_rows": int(values.shape[0]),
                "train_abs_p75": float(values.abs().quantile(0.75)) if not values.empty else 0.0,
                "train_abs_p90": float(values.abs().quantile(0.90)) if not values.empty else 0.0,
                "train_abs_p95": float(values.abs().quantile(0.95)) if not values.empty else 0.0,
                "train_mean": float(values.mean()) if not values.empty else 0.0,
            }
        )
    return pd.DataFrame(rows)


def summarize(
    features: pd.DataFrame,
    families: pd.DataFrame,
    specs: pd.DataFrame,
    gates: pd.DataFrame,
    phase88_dir: Path,
    phase89_dir: Path,
) -> pd.DataFrame:
    p88_same_shards = metric_value(phase88_dir / "strategy_pivot_acceptance_summary.csv", "phase88_more_same_family_shards_allowed", 1)
    p89_passive_pass = metric_value(phase89_dir / "passive_queue_cost_floor_acceptance_summary.csv", "phase89_passive_queue_cost_floor_pass", 1)
    ready = int(len(features) > 0 and len(families) == 3 and len(specs) == 12 and len(gates) >= 7 and float(p88_same_shards) == 0)
    return pd.DataFrame(
        [
            ("phase90_feature_rows", int(len(features)), "Cross-symbol feature rows materialized from Phase83 cached bars"),
            ("phase90_train_feature_rows", int(features["trade_month"].isin(TRAIN_MONTHS).sum()), "Train rows available for feature-threshold calibration"),
            ("phase90_test_feature_rows", int(features["trade_month"].isin(TEST_MONTHS).sum()), "Test rows locked for replay evaluation"),
            ("phase90_signal_family_rows", int(len(families)), "Cross-symbol/regime signal families precommitted"),
            ("phase90_candidate_spec_rows", int(len(specs)), "Candidate threshold specs precommitted"),
            ("phase90_validation_gate_rows", int(len(gates)), "Replay validation gates locked"),
            ("phase90_phase88_same_family_shards_allowed", int(float(p88_same_shards)), "Must be 0 before pivoting to a new family"),
            ("phase90_phase89_passive_queue_pass", int(float(p89_passive_pass)), "Phase89 simple passive result used only as pivot context"),
            ("phase90_ready_for_replay", ready, "1 means Phase91 cross-symbol replay may run without changing thresholds"),
            ("phase90_recommend_next_action", "run_precommitted_cross_symbol_regime_imbalance_replay", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase90 Cross-Symbol Regime-Imbalance Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase90 locks a new cross-symbol feature class before directional replay.",
        "It follows Phase88's pivot contract and Phase89's simple passive falsification by moving to lower-turnover market/sector-context imbalance features.",
        "Feature thresholds are computed from train-month feature distributions only; replay P&L is not inspected here.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase90_cross_symbol_regime_imbalance_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase90(phase83_dir: Path, phase88_dir: Path, phase89_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    bars = load_bars(phase83_dir)
    features = build_cross_symbol_features(bars)
    families = build_signal_families(features)
    specs = build_candidate_specs(features, families)
    gates = build_validation_gates()
    diagnostics = build_feature_diagnostics(features)
    acceptance = summarize(features, families, specs, gates, phase88_dir, phase89_dir)

    feature_columns = [
        "trade_month",
        "trade_date",
        "feed_profile",
        "source_event_bar_id",
        "symbol",
        "sector",
        "regime_code",
        "is_etf",
        "close_mid_price",
        "spread_bps",
        "taker_round_trip_cost_floor_bps",
        "avg_event_intensity_proxy",
        "sector_event_intensity",
        "market_event_intensity",
        "x_market_l1_ex_target",
        "x_market_l5_ex_target",
        "x_sector_l1_ex_target",
        "x_sector_l5_ex_target",
        "x_symbol_vs_sector_l1",
        "x_symbol_vs_sector_l5",
        "x_market_regime_intensity",
        "x_sector_regime_intensity",
    ]
    features[feature_columns].to_parquet(output_dir / "cross_symbol_regime_features.parquet", index=False)
    diagnostics.to_csv(output_dir / "cross_symbol_feature_diagnostics.csv", index=False)
    families.to_csv(output_dir / "precommitted_cross_symbol_signal_families.csv", index=False)
    specs.to_csv(output_dir / "precommitted_cross_symbol_candidate_specs.csv", index=False)
    gates.to_csv(output_dir / "precommitted_cross_symbol_validation_gates.csv", index=False)
    acceptance.to_csv(output_dir / "cross_symbol_precommit_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Feature Diagnostics": diagnostics,
            "Precommitted Signal Families": families,
            "Precommitted Candidate Specs": specs,
            "Validation Gates": gates,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {"generated_utc": generated_utc, "scope": "phase90_cross_symbol_regime_imbalance_precommit"}
    manifest.update(
        reproducibility_fields(
            artifact_id="phase90",
            generated_utc=generated_utc,
            inputs={
                "phase83_cached_bars": str(phase83_dir / "stratified_source_event_bars.parquet"),
                "phase88_pivot_summary": str(phase88_dir / "strategy_pivot_acceptance_summary.csv"),
                "phase89_passive_summary": str(phase89_dir / "passive_queue_cost_floor_acceptance_summary.csv"),
            },
            parameters={
                "train_months": sorted(TRAIN_MONTHS),
                "test_months": sorted(TEST_MONTHS),
                "symbol_sector_map": SYMBOL_SECTOR,
                "etf_symbols": sorted(ETF_SYMBOLS),
                "no_label_inspection": True,
                "candidate_quantiles": {"feature_abs": [0.90, 0.95], "intensity_abs": [0.75, 0.90]},
            },
            outputs={
                "features": str(output_dir / "cross_symbol_regime_features.parquet"),
                "diagnostics": str(output_dir / "cross_symbol_feature_diagnostics.csv"),
                "families": str(output_dir / "precommitted_cross_symbol_signal_families.csv"),
                "candidate_specs": str(output_dir / "precommitted_cross_symbol_candidate_specs.csv"),
                "validation_gates": str(output_dir / "precommitted_cross_symbol_validation_gates.csv"),
                "acceptance_summary": str(output_dir / "cross_symbol_precommit_acceptance_summary.csv"),
                "report": str(output_dir / "phase90_cross_symbol_regime_imbalance_precommit_report.md"),
                "manifest": str(output_dir / "phase90_cross_symbol_regime_imbalance_precommit_manifest.json"),
            },
            random_seed="none_deterministic_cross_symbol_precommit",
            scenario_ids="phase90_post_phase88_phase89_cross_symbol_pivot",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase83_source_event_ordinal_alignment",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase90_cross_symbol_regime_imbalance_precommit_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Precommit cross-symbol regime-imbalance replay.")
    parser.add_argument("--phase83-dir", type=Path, default=DEFAULT_PHASE83_DIR)
    parser.add_argument("--phase88-dir", type=Path, default=DEFAULT_PHASE88_DIR)
    parser.add_argument("--phase89-dir", type=Path, default=DEFAULT_PHASE89_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase90(args.phase83_dir, args.phase88_dir, args.phase89_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
