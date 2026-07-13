from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq


@dataclass(frozen=True)
class StrategySpec:
    strategy_id: str
    name: str
    priority: str
    role: str
    hypothesis: str
    required_features: tuple[str, ...]
    current_proxy_features: tuple[str, ...]
    missing_features: tuple[str, ...]
    required_scenarios: tuple[str, ...]
    primary_metrics: tuple[str, ...]
    support_level: str
    caveat: str


STRATEGIES = [
    StrategySpec(
        "S01",
        "Momentum/breakout filtered by MLOFI",
        "1",
        "priority",
        "Breakouts confirmed by persistent five-level OFI should continue better than price-only breakouts.",
        ("momentum", "mlofi", "spread", "future_return", "time_of_day_regime"),
        ("momentum_3", "mlofi_qty", "spread_ticks", "future_mid_return_1", "regime_code"),
        ("trade_flow_confirmation", "true_1s_lookbacks", "market_or_sector_alignment"),
        ("gradual trend", "strong rally", "sell-off", "false breakout", "sideways", "shock continuation", "shock reversal"),
        ("false_breakout_reduction", "net_expectancy", "mae_mfe", "cost_sensitivity", "latency_tolerance", "regime_stability"),
        "runnable_proxy",
        "Current proxy uses 5-minute synthetic features, not true 1/5/15/30 second MLOFI lookbacks.",
    ),
    StrategySpec(
        "S02",
        "Pure multi-level OFI directional model",
        "2",
        "priority",
        "Five-level OFI should predict future mid-price movement beyond static imbalance.",
        ("l1_imbalance", "l5_imbalance", "mlofi", "future_return"),
        ("l1_imbalance", "l5_imbalance", "mlofi_qty", "future_mid_return_1"),
        ("true_l1_ofi", "next_quote_move_label", "multi_horizon_second_labels"),
        ("normal", "trend", "shock", "high-volatility sideways"),
        ("information_coefficient", "directional_accuracy", "signal_deciles", "incremental_value_l2_l5", "regime_stability"),
        "runnable_proxy",
        "Current proxy can compare static imbalance and mlofi_qty at 5-minute event spacing only.",
    ),
    StrategySpec(
        "S03",
        "Liquidity-vacuum breakout",
        "3",
        "priority",
        "One-sided depth withdrawal plus aggressive flow should precede a short-horizon move.",
        ("depth_withdrawal", "trade_confirmation", "price_breakout", "spread_constraint", "future_return"),
        ("book_slope_l5", "spread_ticks", "momentum_3", "future_mid_return_1"),
        ("explicit_depth_withdrawal_rate", "aggressive_trade_flow", "multi_level_sweep_labels"),
        ("genuine continuation", "fake withdrawal", "spread blowout", "market shock", "isolated vacuum", "rapid recovery", "multi-level sweep"),
        ("profit_after_latency", "slippage_sensitivity", "template_dependence", "ticker_concentration"),
        "partial_missing_required_features",
        "Only a weak proxy exists because Phase 9 Tier C does not yet carry explicit withdrawal/replenishment rates.",
    ),
    StrategySpec(
        "S04",
        "Trade-flow plus depth confirmation",
        "4",
        "priority",
        "Trade imbalance and depth flow jointly classify continuation, absorption, exhaustion and false breakout.",
        ("mlofi", "trade_imbalance", "future_return", "regime"),
        ("mlofi_qty", "event_intensity_proxy", "future_mid_return_1", "regime_code"),
        ("aggressive_trade_imbalance", "absorption_label", "exhaustion_label"),
        ("continuation", "absorption", "exhaustion", "false breakout"),
        ("state_conditional_return", "classification_separation", "regime_stability"),
        "partial_missing_required_features",
        "Event intensity is not a substitute for signed aggressive trade imbalance.",
    ),
    StrategySpec(
        "S05",
        "Microprice entry/exit filter",
        "5",
        "filter",
        "Microprice should improve next-move estimates and entry/exit timing.",
        ("microprice", "mid_price", "future_return", "spread"),
        ("microprice_l1", "mid_price", "future_mid_return_1", "spread_ticks"),
        ("next_tick_direction", "entry_slippage", "parent_strategy_linkage"),
        ("normal", "trend", "shock"),
        ("brier_score", "directional_accuracy", "trade_reduction", "net_uplift_over_parent"),
        "runnable_proxy",
        "Standalone microprice results are diagnostic only; plan says not to promote it as a standalone annual-return strategy.",
    ),
    StrategySpec(
        "S06",
        "Absorption and exhaustion reversal",
        "6",
        "priority",
        "Large aggressive flow with limited price progress followed by reversal should predict short-term reversal.",
        ("aggressive_flow", "limited_price_progress", "flow_reversal", "future_return"),
        ("event_intensity_proxy", "momentum_3", "future_mid_return_1", "regime_code"),
        ("signed_aggressive_flow", "flow_reversal", "replenishment_rate"),
        ("true absorption", "pause before continuation", "hidden-liquidity-like replenishment", "post-shock stabilization", "deceptive replenishment"),
        ("reversal_return", "false_reversal_rate", "regime_stability"),
        "partial_missing_required_features",
        "Can only label absorption-like proxies; top-five market-by-price cannot prove iceberg/participant identity.",
    ),
    StrategySpec(
        "S07",
        "Mean reversion after imbalance",
        "7",
        "priority",
        "Extreme imbalance followed by replenishment and lower intensity should predict reversion in non-trend regimes.",
        ("l5_imbalance", "replenishment", "event_intensity", "regime", "future_return"),
        ("l5_imbalance", "event_intensity_proxy", "regime_code", "future_mid_return_1"),
        ("explicit_replenishment_rate", "trend_suppression_gate"),
        ("sideways", "high-volatility sideways", "post-shock recovery", "sustained trend", "panic", "rally"),
        ("regime_aware_vs_unaware", "net_expectancy", "false_reversion_rate"),
        "runnable_proxy",
        "Proxy uses imbalance/intensity and regime_code; explicit replenishment is still missing.",
    ),
    StrategySpec(
        "S08",
        "Cross-ticker/index lead-lag OFI",
        "8",
        "research",
        "Market, sector or leader OFI should improve follower prediction while avoiding simultaneous-shock false positives.",
        ("leader_mlofi", "follower_return", "timestamp_skew_controls", "market_factor"),
        ("mlofi_qty", "future_mid_return_1", "symbol", "bar_index", "trade_date"),
        ("sector_mapping", "leader_labels", "timestamp_skew_simulations", "explicit_lead_lag_scenarios"),
        ("true lead-lag", "simultaneous shock", "timestamp skew", "spurious correlation", "changing leader", "no lead-lag"),
        ("incremental_ic", "false_detection_controls", "leader_stability"),
        "partial_missing_required_features",
        "Can compute market-level proxy factors, but causal lead-lag validation requires dedicated synthetic controls.",
    ),
    StrategySpec(
        "S09",
        "Pure queue-imbalance scalping",
        "9",
        "benchmark",
        "Queue imbalance may predict next quote direction but must survive latency and costs.",
        ("l1_imbalance", "future_return", "latency_cost_model", "spread"),
        ("l1_imbalance", "future_mid_return_1", "spread_ticks"),
        ("queue_position", "50_100_250_500ms_labels", "cost_model"),
        ("normal", "latency stress", "spread stress"),
        ("directional_accuracy", "edge_after_spread_cost", "latency_survival"),
        "runnable_proxy",
        "Benchmark only. Accuracy above 50% is not sufficient without spread/cost survival.",
    ),
    StrategySpec(
        "S10",
        "Passive market making",
        "10",
        "research_only",
        "Synthetic testing can develop inventory/risk logic but cannot validate real queue fills from shallow MBP data.",
        ("queue_position", "partial_fills", "cancellation_latency", "inventory", "adverse_selection", "liquidation_cost"),
        tuple(),
        ("queue_position", "fill_model", "inventory_model", "cancellation_latency", "order_simulator"),
        ("optimistic fills", "neutral fills", "pessimistic fills"),
        ("pnl_under_pessimistic_model", "inventory_risk", "adverse_selection"),
        "not_supported_by_current_product",
        "Requires Phase 12 execution simulator and pessimistic queue-fill assumptions.",
    ),
    StrategySpec(
        "S11",
        "Spoof-like wall filter",
        "11",
        "risk_filter_only",
        "Wall appearance/cancellation patterns can be used only as a risk feature, not participant classification.",
        ("wall_appearance", "wall_movement", "cancellation_before_touch", "non_execution", "temporary_imbalance_distortion"),
        tuple(),
        ("order_lifetime_proxy", "wall_tracking", "touch/non_touch_events", "cancellation_labels"),
        ("temporary wall", "genuine liquidity", "shock liquidity", "no wall"),
        ("risk_filter_precision", "false_positive_rate", "strategy_uplift_as_filter"),
        "not_supported_by_current_product",
        "Current top-five snapshots do not support spoof/manipulation assertions.",
    ),
]


BASELINES = [
    ("B01", "Random direction with matched trade frequency", "must match signal count and holding horizon"),
    ("B02", "Buy-and-hold intraday control", "price-only benchmark"),
    ("B03", "Simple short-term momentum", "price-only benchmark"),
    ("B04", "Opening-range breakout", "price-only benchmark"),
    ("B05", "VWAP continuation", "requires VWAP/trade-volume feature before runnable"),
    ("B06", "Short-term mean reversion", "price-only benchmark"),
    ("B07", "Volatility breakout", "price-only benchmark"),
]


def load_features(path: Path) -> pd.DataFrame:
    cols = [
        "feed_profile",
        "quarter_profile",
        "scenario_day",
        "trade_date",
        "bar_index",
        "symbol",
        "regime_code",
        "mid_price",
        "spread_ticks",
        "l1_imbalance",
        "l5_imbalance",
        "microprice_l1",
        "mlofi_qty",
        "momentum_3",
        "local_volatility_6",
        "book_slope_l5",
        "book_convexity_l5",
        "event_intensity_proxy",
        "is_market_shock_day",
        "is_symbol_shock",
        "is_duplicate",
        "is_disconnect_gap",
        "is_out_of_order_injected",
        "future_mid_return_1",
    ]
    return pq.read_table(path, columns=cols).to_pandas()


def strategy_matrix() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "strategy_id": spec.strategy_id,
                "name": spec.name,
                "priority": spec.priority,
                "role": spec.role,
                "hypothesis": spec.hypothesis,
                "required_features": "; ".join(spec.required_features),
                "current_proxy_features": "; ".join(spec.current_proxy_features),
                "missing_features": "; ".join(spec.missing_features),
                "required_scenarios": "; ".join(spec.required_scenarios),
                "primary_metrics": "; ".join(spec.primary_metrics),
                "support_level": spec.support_level,
                "caveat": spec.caveat,
            }
            for spec in STRATEGIES
        ]
    )


def baseline_matrix() -> pd.DataFrame:
    return pd.DataFrame(
        [{"baseline_id": baseline_id, "name": name, "requirement": requirement} for baseline_id, name, requirement in BASELINES]
    )


def sign_accuracy(signal: pd.Series, future: pd.Series) -> float | None:
    mask = signal.ne(0) & future.notna() & future.ne(0)
    if int(mask.sum()) == 0:
        return None
    return float((np.sign(signal[mask]) == np.sign(future[mask])).mean())


def safe_mean(series: pd.Series) -> float | None:
    values = series.dropna()
    return float(values.mean()) if len(values) else None


def build_signals(features: pd.DataFrame) -> dict[str, pd.Series]:
    q = features[
        [
            "mlofi_qty",
            "momentum_3",
            "book_slope_l5",
            "event_intensity_proxy",
            "l5_imbalance",
            "l1_imbalance",
            "local_volatility_6",
        ]
    ].quantile([0.1, 0.2, 0.8, 0.9]).to_dict()
    micro_dev = (features["microprice_l1"] - features["mid_price"]) / features["mid_price"].replace(0, np.nan)
    market_mlofi = features.groupby(["feed_profile", "trade_date", "scenario_day", "bar_index"])["mlofi_qty"].transform("mean")

    s01 = np.sign(features["momentum_3"]).where(
        (features["momentum_3"].abs() >= max(abs(q["momentum_3"][0.1]), abs(q["momentum_3"][0.9])))
        & (np.sign(features["momentum_3"]) == np.sign(features["mlofi_qty"]))
        & (features["spread_ticks"] <= features["spread_ticks"].quantile(0.8)),
        0,
    )
    s02 = np.sign(features["mlofi_qty"]).where(features["mlofi_qty"].abs() >= max(abs(q["mlofi_qty"][0.2]), abs(q["mlofi_qty"][0.8])), 0)
    s03 = np.sign(features["momentum_3"]).where(
        (features["book_slope_l5"] >= q["book_slope_l5"][0.8])
        & (features["event_intensity_proxy"] >= q["event_intensity_proxy"][0.8])
        & (features["momentum_3"].abs() > 0),
        0,
    )
    s04 = np.sign(features["mlofi_qty"]).where(
        (features["event_intensity_proxy"] >= q["event_intensity_proxy"][0.8]) & (features["mlofi_qty"].abs() > 0),
        0,
    )
    s05 = np.sign(micro_dev).where(micro_dev.abs() >= micro_dev.abs().quantile(0.8), 0)
    s06 = -np.sign(features["momentum_3"]).where(
        (features["event_intensity_proxy"] >= q["event_intensity_proxy"][0.8])
        & (features["momentum_3"].abs() <= features["momentum_3"].abs().quantile(0.2)),
        0,
    )
    nontrend = ~features["regime_code"].astype(str).isin(["D03", "D04", "D05", "D06"])
    s07 = -np.sign(features["l5_imbalance"]).where(
        nontrend & (features["l5_imbalance"].abs() >= max(abs(q["l5_imbalance"][0.1]), abs(q["l5_imbalance"][0.9]))),
        0,
    )
    s08 = np.sign(market_mlofi).where(market_mlofi.abs() >= market_mlofi.abs().quantile(0.8), 0)
    s09 = np.sign(features["l1_imbalance"]).where(features["l1_imbalance"].abs() >= max(abs(q["l1_imbalance"][0.2]), abs(q["l1_imbalance"][0.8])), 0)
    return {
        "S01": pd.Series(s01, index=features.index).fillna(0),
        "S02": pd.Series(s02, index=features.index).fillna(0),
        "S03": pd.Series(s03, index=features.index).fillna(0),
        "S04": pd.Series(s04, index=features.index).fillna(0),
        "S05": pd.Series(s05, index=features.index).fillna(0),
        "S06": pd.Series(s06, index=features.index).fillna(0),
        "S07": pd.Series(s07, index=features.index).fillna(0),
        "S08": pd.Series(s08, index=features.index).fillna(0),
        "S09": pd.Series(s09, index=features.index).fillna(0),
    }


def signal_diagnostics(features: pd.DataFrame, matrix: pd.DataFrame) -> pd.DataFrame:
    future = features["future_mid_return_1"]
    signals = build_signals(features)
    rows: list[dict] = []
    for spec in STRATEGIES:
        signal = signals.get(spec.strategy_id)
        if signal is None:
            rows.append(
                {
                    "strategy_id": spec.strategy_id,
                    "support_level": spec.support_level,
                    "rows_evaluated": int(len(features)),
                    "signal_rows": 0,
                    "signal_fraction": 0.0,
                    "mean_future_return_when_signaled": None,
                    "signed_mean_future_return": None,
                    "directional_accuracy_nonzero": None,
                    "profiles": int(features["feed_profile"].nunique()),
                    "symbols": int(features["symbol"].nunique()),
                    "status": "not_evaluated_missing_product_support",
                }
            )
            continue
        mask = signal.ne(0) & future.notna()
        signed = signal[mask] * future[mask]
        rows.append(
            {
                "strategy_id": spec.strategy_id,
                "support_level": spec.support_level,
                "rows_evaluated": int(len(features)),
                "signal_rows": int(mask.sum()),
                "signal_fraction": float(mask.mean()),
                "mean_future_return_when_signaled": safe_mean(future[mask]),
                "signed_mean_future_return": safe_mean(signed),
                "directional_accuracy_nonzero": sign_accuracy(signal, future),
                "profiles": int(features.loc[mask, "feed_profile"].nunique()) if int(mask.sum()) else 0,
                "symbols": int(features.loc[mask, "symbol"].nunique()) if int(mask.sum()) else 0,
                "status": "diagnostic_only_not_acceptance_test",
            }
        )
    return pd.DataFrame(rows).merge(matrix[["strategy_id", "name", "role", "caveat"]], on="strategy_id", how="left")


def feature_availability(features: pd.DataFrame, matrix: pd.DataFrame) -> pd.DataFrame:
    columns = set(features.columns)
    rows = []
    for spec in STRATEGIES:
        proxies = list(spec.current_proxy_features)
        present = [col for col in proxies if col in columns]
        absent = [col for col in proxies if col and col not in columns]
        rows.append(
            {
                "strategy_id": spec.strategy_id,
                "support_level": spec.support_level,
                "proxy_feature_count": len(proxies),
                "proxy_features_present": len(present),
                "proxy_features_absent": len(absent),
                "present_proxy_features": "; ".join(present),
                "absent_proxy_features": "; ".join(absent),
                "plan_missing_features": spec.missing_features and "; ".join(spec.missing_features) or "",
            }
        )
    return pd.DataFrame(rows).merge(matrix[["strategy_id", "name"]], on="strategy_id", how="left")


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    text = frame.copy()
    for column in text.columns:
        text[column] = text[column].map(lambda value: "" if pd.isna(value) else (f"{value:.6g}" if isinstance(value, float) else str(value)))
    headers = [str(column) for column in text.columns]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in text.values.tolist())
    return "\n".join(lines)


def write_report(output_dir: Path, matrix: pd.DataFrame, diagnostics: pd.DataFrame, availability: pd.DataFrame) -> None:
    support = matrix["support_level"].value_counts().rename_axis("support_level").reset_index(name="strategies")
    diag_cols = [
        "strategy_id",
        "signal_rows",
        "signal_fraction",
        "signed_mean_future_return",
        "directional_accuracy_nonzero",
        "status",
    ]
    lines = [
        "# Phase 11 Strategy Validation Matrix Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase defines strategy experiments and runs preliminary signal diagnostics against current Phase 9 Tier C features.",
        "These diagnostics are not strategy acceptance results. The current feature product is 5-minute synthetic data derived from a one-day real sample.",
        "",
        "## Support Levels",
        "",
        _markdown_table(support),
        "",
        "## Preliminary Signal Diagnostics",
        "",
        _markdown_table(diagnostics[diag_cols]),
        "",
        "## Feature Availability",
        "",
        _markdown_table(availability[["strategy_id", "support_level", "proxy_features_present", "proxy_features_absent", "plan_missing_features"]]),
        "",
        "## Outputs",
        "",
        "- `strategy_validation_matrix.csv`",
        "- `baseline_strategy_matrix.csv`",
        "- `strategy_feature_availability.csv`",
        "- `strategy_signal_diagnostics.csv`",
        "- `strategy_validation_manifest.json`",
        "",
    ]
    (output_dir / "phase11_strategy_validation_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase11(features_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    features = load_features(features_path)
    matrix = strategy_matrix()
    baselines = baseline_matrix()
    availability = feature_availability(features, matrix)
    diagnostics = signal_diagnostics(features, matrix)

    matrix.to_csv(output_dir / "strategy_validation_matrix.csv", index=False)
    baselines.to_csv(output_dir / "baseline_strategy_matrix.csv", index=False)
    availability.to_csv(output_dir / "strategy_feature_availability.csv", index=False)
    diagnostics.to_csv(output_dir / "strategy_signal_diagnostics.csv", index=False)
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "features_path": str(features_path),
        "rows_evaluated": int(len(features)),
        "strategies": int(len(matrix)),
        "baselines": int(len(baselines)),
        "support_levels": matrix["support_level"].value_counts().to_dict(),
        "diagnostic_scope": "preliminary_feature_and_signal_diagnostics_only",
        "not_acceptance_result": True,
    }
    (output_dir / "strategy_validation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, matrix, diagnostics, availability)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 11 strategy validation matrix and preliminary signal diagnostics.")
    parser.add_argument("--features-path", type=Path, default=Path("outputs/phase9/tier_c/features_5m.parquet"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase11"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase11(args.features_path, args.output_dir)


if __name__ == "__main__":
    main()
