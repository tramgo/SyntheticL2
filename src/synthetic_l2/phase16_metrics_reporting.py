from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from synthetic_l2.phase11_strategy_validation_matrix import build_signals, load_features
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


PREDICTIVE_METRICS = [
    ("directional_accuracy", "computed_proxy", "phase11_signal_diagnostics.directional_accuracy_nonzero"),
    ("balanced_accuracy", "sample_proxy", "Computed from Phase 11 ternary proxy signal confusion by direction."),
    ("precision_recall_by_direction", "sample_proxy", "Computed from Phase 11 ternary proxy signal confusion by long/short direction."),
    ("roc_auc", "sample_proxy", "Rank-AUC proxy computed from ternary signal score; not a calibrated probabilistic ROC."),
    ("brier_score", "sample_proxy", "Computed from deterministic ternary-signal pseudo-probabilities; not a calibrated probability model."),
    ("calibration_curve", "sample_proxy", "Computed from deterministic ternary-signal probability buckets and realized up/down frequency."),
    ("baseline_improvement", "sample_proxy", "Compares current proxy signals against no-skill, majority-direction and Brier baselines."),
    ("holdout_segment_stability", "sample_proxy", "Compares current proxy signals against local majority-direction baselines by quarter, feed profile and scenario segment."),
    ("information_coefficient", "proxy_available", "Proxy signed_mean_future_return is available; rank IC is not computed yet."),
    ("future_return_by_signal_decile", "sample_proxy", "Computed as ternary signal-score buckets because current signals are not continuous decile scores."),
    ("incremental_r2", "sample_proxy", "Computed as simple signal-vs-intercept R2 over future returns; not a model-vs-rich-baseline result."),
    ("feature_importance_stability", "sample_proxy", "Computed from deterministic seed-sampled feature/target association stability; not model importance."),
]

TRADING_METRICS = [
    ("gross_pnl", "computed_proxy", "phase12_execution_summary.total gross proxy can be inferred from mean_gross_return * trades."),
    ("net_pnl", "computed_proxy", "phase12_execution_summary.total_net_pnl_units."),
    ("return_on_allocated_capital", "proxy_available", "Phase 12 order-lifecycle proxy carries submitted/filled notional; accepted capital allocation is still missing."),
    ("sharpe", "sample_proxy", "Computed from Phase 12 sampled trade ledger, not full daily equity curves."),
    ("sortino", "sample_proxy", "Computed from Phase 12 sampled trade ledger, not full daily equity curves."),
    ("maximum_drawdown", "sample_proxy", "Computed on sampled trade sequence, not accepted daily equity curve."),
    ("calmar_ratio", "sample_proxy", "Drawdown proxy exists in Phase 12 order-lifecycle sample; accepted annualized return horizon is still missing."),
    ("profit_factor", "sample_proxy", "Computed from sampled trade ledger."),
    ("win_rate", "computed_proxy", "phase12_execution_summary.win_rate_net."),
    ("average_win_loss", "sample_proxy", "Computed from sampled trade ledger."),
    ("expectancy_per_trade", "computed_proxy", "phase12_execution_summary.mean_net_return."),
    ("risk_adjusted_net_edge", "sample_proxy", "Joins economic frontier rows to Phase 12 full-run lifecycle breach severity; not acceptance-grade broker risk evidence."),
    ("turnover", "proxy_available", "Trade count is available; capital-normalized turnover is not."),
    ("cost_to_gross_profit_ratio", "sample_proxy", "Computed from sampled trade ledger."),
    ("fill_ratio", "sample_proxy", "Phase 12 order-lifecycle proxy provides submitted and filled quantities over the sampled trade ledger."),
    ("adverse_selection", "sample_proxy", "Computed from sampled post-fill markout windows over the Phase 12 trade ledger."),
    ("mae_mfe", "sample_proxy", "Computed from sampled 1/3/6-bar post-entry markout path over the Phase 12 trade ledger."),
    ("exposure_holding_time", "sample_proxy", "Phase 12 order-lifecycle proxy provides running position exposure; holding-time lifecycle remains approximate."),
]

METRIC_EVIDENCE_PATHS = {
    "directional_accuracy": "outputs/phase16/predictive_metric_scoreboard.csv; outputs/phase11/strategy_signal_diagnostics.csv",
    "balanced_accuracy": "outputs/phase16/predictive_proxy_diagnostics.csv",
    "precision_recall_by_direction": "outputs/phase16/predictive_proxy_diagnostics.csv",
    "roc_auc": "outputs/phase16/predictive_proxy_diagnostics.csv",
    "brier_score": "outputs/phase16/predictive_brier_score_proxy.csv",
    "calibration_curve": "outputs/phase16/predictive_calibration_curve_proxy.csv",
    "baseline_improvement": "outputs/phase16/predictive_baseline_comparison.csv",
    "holdout_segment_stability": "outputs/phase16/predictive_holdout_stability_summary.csv; outputs/phase16/predictive_holdout_stability.csv",
    "information_coefficient": "outputs/phase16/predictive_metric_scoreboard.csv; outputs/phase11/strategy_signal_diagnostics.csv",
    "future_return_by_signal_decile": "outputs/phase16/predictive_signal_bucket_returns.csv",
    "incremental_r2": "outputs/phase16/predictive_proxy_diagnostics.csv",
    "feature_importance_stability": "outputs/phase16/feature_importance_stability_proxy.csv",
    "gross_pnl": "outputs/phase16/trading_metric_scoreboard.csv; outputs/phase12/execution_summary.csv",
    "net_pnl": "outputs/phase16/trading_metric_scoreboard.csv; outputs/phase12/execution_summary.csv",
    "return_on_allocated_capital": "outputs/phase16/trading_metric_scoreboard.csv; outputs/phase12_order_lifecycle/risk_control_summary.csv",
    "sharpe": "outputs/phase16/trading_metric_scoreboard.csv; outputs/phase12/trade_ledger_sample.parquet",
    "sortino": "outputs/phase16/trading_metric_scoreboard.csv; outputs/phase12/trade_ledger_sample.parquet",
    "maximum_drawdown": "outputs/phase16/trading_metric_scoreboard.csv; outputs/phase12_order_lifecycle/risk_control_summary.csv",
    "calmar_ratio": "outputs/phase16/trading_metric_scoreboard.csv; outputs/phase12_order_lifecycle/risk_control_summary.csv",
    "profit_factor": "outputs/phase16/trading_metric_scoreboard.csv; outputs/phase12/trade_ledger_sample.parquet",
    "win_rate": "outputs/phase16/trading_metric_scoreboard.csv; outputs/phase12/execution_summary.csv",
    "average_win_loss": "outputs/phase16/trading_metric_scoreboard.csv; outputs/phase12/trade_ledger_sample.parquet",
    "expectancy_per_trade": "outputs/phase16/trading_metric_scoreboard.csv; outputs/phase12/execution_summary.csv",
    "risk_adjusted_net_edge": "outputs/phase16/risk_adjusted_economic_frontier.csv; outputs/phase12/full_run_lifecycle_risk_breach_severity.csv",
    "turnover": "outputs/phase16/trading_metric_scoreboard.csv; outputs/phase12/execution_summary.csv",
    "cost_to_gross_profit_ratio": "outputs/phase16/trading_metric_scoreboard.csv; outputs/phase12/cost_schedule.csv",
    "fill_ratio": "outputs/phase16/trading_metric_scoreboard.csv; outputs/phase12_order_lifecycle/partial_fill_summary.csv",
    "adverse_selection": "outputs/phase16/markout_mae_mfe_summary.csv",
    "mae_mfe": "outputs/phase16/markout_mae_mfe_summary.csv",
    "exposure_holding_time": "outputs/phase16/trading_metric_scoreboard.csv; outputs/phase12_order_lifecycle/risk_control_summary.csv",
}

METRIC_ACCEPTANCE_BLOCKERS = {
    "computed_proxy": "Computed from current one-day-derived synthetic/proxy products; not acceptance-grade without multi-day real holdout, full execution validation and promotion-gate clearance.",
    "sample_proxy": "Computed from sampled/proxy evidence; not acceptance-grade without full-run coverage, multi-seed/walk-forward/holdout evidence and broker/exchange fill validation where applicable.",
    "proxy_available": "Supporting proxy evidence exists, but the accepted production metric definition or capital/fill normalization remains incomplete.",
}

BREAKDOWNS = [
    ("ticker", "symbol", "available"),
    ("day", "trade_date", "available"),
    ("regime", "regime_code", "available"),
    ("time_of_day", "bar_index", "proxy_available"),
    ("volatility_bucket", "volatility_bucket", "proxy_available"),
    ("spread_bucket", "spread_ticks", "proxy_available"),
    ("liquidity_bucket", "liquidity_bucket", "proxy_available"),
    ("long_short", "side", "available"),
    ("latency_profile", "execution_profile", "available"),
    ("cost_profile", "execution_profile", "proxy_available"),
    ("random_seed", "seed", "proxy_available"),
    ("event_vs_non_event_day", "is_market_shock_day", "available"),
]


METRIC_ALIASES = {
    "signal_deciles": "future_return_by_signal_decile",
    "classification_accuracy": "directional_accuracy",
    "next_quote_accuracy": "directional_accuracy",
    "continuation_probability": "directional_accuracy",
    "false_positive_rate": "precision_recall_by_direction",
    "false_detection_rate": "precision_recall_by_direction",
    "false_breakout_reduction": "precision_recall_by_direction",
    "false_reversion_rate": "precision_recall_by_direction",
    "false_absorption_rate": "precision_recall_by_direction",
    "risk_filter_precision": "precision_recall_by_direction",
    "control_rejection_rate": "precision_recall_by_direction",
    "incremental_l2_l5_value": "incremental_r2",
    "incremental_predictive_value": "incremental_r2",
    "feature_stability": "feature_importance_stability",
    "label_stability": "feature_importance_stability",
    "shock_template_stability": "feature_importance_stability",
    "lead_lag_stability": "feature_importance_stability",
    "calibration": "calibration_curve",
    "net_expectancy": "expectancy_per_trade",
    "net_expectancy_by_state": "expectancy_per_trade",
    "state_conditional_return": "expectancy_per_trade",
    "net_edge_after_costs": "expectancy_per_trade",
    "net_edge_after_spread": "expectancy_per_trade",
    "net_performance_uplift_over_parent": "expectancy_per_trade",
    "pessimistic_model_pnl": "net_pnl",
    "mae": "mae_mfe",
    "mfe": "mae_mfe",
    "post_entry_adverse_movement": "mae_mfe",
    "adverse_selection_loss": "adverse_selection",
    "drawdown": "maximum_drawdown",
    "inventory_drawdown": "maximum_drawdown",
    "parent_strategy_drawdown_reduction": "maximum_drawdown",
    "cost_sensitivity": "cost_to_gross_profit_ratio",
    "slippage_sensitivity": "cost_to_gross_profit_ratio",
    "entry_slippage": "cost_to_gross_profit_ratio",
    "liquidation_cost": "cost_to_gross_profit_ratio",
    "expected_move_vs_spread": "cost_to_gross_profit_ratio",
    "latency_tolerance": "exposure_holding_time",
    "latency_decay": "exposure_holding_time",
    "fill_uncertainty": "fill_ratio",
    "spread_capture": "gross_pnl",
    "reversal_probability": "directional_accuracy",
    "regime_stability": "holdout_segment_stability",
    "regime_aware_vs_unaware_uplift": "holdout_segment_stability",
    "miss_rate": "fill_ratio",
    "trade_reduction": "turnover",
}


def load_inputs(paths: dict[str, Path]) -> dict[str, pd.DataFrame]:
    return {
        "signal_diagnostics": pd.read_csv(paths["signal_diagnostics"]),
        "metric_requirements": pd.read_csv(paths["metric_requirements"]),
        "execution_summary": pd.read_csv(paths["execution_summary"]),
        "trade_sample": pd.read_parquet(paths["trade_sample"]),
        "risk_breach_severity": pd.read_csv(paths["risk_breach_severity"]),
        "cost_schedule": pd.read_csv(paths["cost_schedule"]),
        "charge_component_catalog": pd.read_csv(paths["charge_component_catalog"]),
        "representative_charge_scenarios": pd.read_csv(paths["representative_charge_scenarios"]),
        "features": load_features(paths["features"]),
        "acceptance_summary": pd.read_csv(paths["acceptance_summary"]),
        "seed_plan": pd.read_csv(paths["seed_plan"]),
    }


def metric_catalog() -> pd.DataFrame:
    rows = []
    for category, metrics in [("predictive", PREDICTIVE_METRICS), ("trading", TRADING_METRICS)]:
        for metric_name, current_status, evidence_note in metrics:
            rows.append(
                {
                    "metric_category": category,
                    "metric_name": metric_name,
                    "current_status": current_status,
                    "evidence_note": evidence_note,
                    "evidence_path": METRIC_EVIDENCE_PATHS.get(metric_name, ""),
                    "blocker": "" if current_status == "computed_acceptance" else METRIC_ACCEPTANCE_BLOCKERS.get(current_status, "Not acceptance-grade in the current one-day/proxy evidence set."),
                    "acceptance_eligible_now": current_status == "computed_acceptance",
                }
            )
    return pd.DataFrame(rows)


def predictive_scoreboard(inputs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    diag = inputs["signal_diagnostics"].copy()
    acceptance = inputs["acceptance_summary"][["strategy_id", "promotion_allowed", "acceptance_status"]]
    out = diag.merge(acceptance, on="strategy_id", how="left")
    out["directional_accuracy_status"] = np.where(
        out["directional_accuracy_nonzero"].fillna(0) >= 0.52,
        "proxy_threshold_met_not_acceptance",
        "proxy_threshold_not_met",
    )
    out["information_coefficient_proxy"] = out["signed_mean_future_return"]
    out["metric_scope"] = "phase11_5m_proxy_diagnostic"
    return out[
        [
            "strategy_id",
            "name",
            "support_level",
            "rows_evaluated",
            "signal_rows",
            "signal_fraction",
            "directional_accuracy_nonzero",
            "directional_accuracy_status",
            "mean_future_return_when_signaled",
            "signed_mean_future_return",
            "information_coefficient_proxy",
            "promotion_allowed",
            "acceptance_status",
            "metric_scope",
        ]
    ]


def _safe_metric(num: float, den: float) -> float | None:
    if den == 0 or pd.isna(den):
        return None
    return float(num / den)


def _auc_from_scores(labels: pd.Series, scores: pd.Series) -> float | None:
    valid = labels.notna() & scores.notna()
    y = labels[valid].astype(int)
    s = scores[valid].astype(float)
    positives = int((y == 1).sum())
    negatives = int((y == 0).sum())
    if positives == 0 or negatives == 0:
        return None
    ranks = s.rank(method="average")
    positive_rank_sum = float(ranks[y == 1].sum())
    return float((positive_rank_sum - positives * (positives + 1) / 2.0) / (positives * negatives))


def _r2_against_intercept(y: pd.Series, x: pd.Series) -> float | None:
    valid = y.notna() & x.notna()
    yv = y[valid].astype(float)
    xv = x[valid].astype(float)
    if len(yv) < 2 or float(xv.var()) == 0.0:
        return None
    slope = float(np.cov(xv, yv, ddof=0)[0, 1] / xv.var(ddof=0))
    intercept = float(yv.mean() - slope * xv.mean())
    pred = intercept + slope * xv
    sse = float(((yv - pred) ** 2).sum())
    sst = float(((yv - yv.mean()) ** 2).sum())
    return _safe_metric(sst - sse, sst)


def predictive_proxy_diagnostics(inputs: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame]:
    features = inputs["features"].copy()
    future = features["future_mid_return_1"].astype(float)
    actual_direction = np.sign(future)
    binary_up = (future > 0).astype(int)
    signals = build_signals(features)

    summary_rows = []
    bucket_rows = []
    for strategy_id, signal in signals.items():
        signal = signal.astype(float)
        valid_direction = signal.ne(0) & future.notna() & future.ne(0)
        pred_long = valid_direction & (signal > 0)
        pred_short = valid_direction & (signal < 0)
        actual_up = valid_direction & (actual_direction > 0)
        actual_down = valid_direction & (actual_direction < 0)
        true_long = pred_long & actual_up
        true_short = pred_short & actual_down
        precision_long = _safe_metric(float(true_long.sum()), float(pred_long.sum()))
        recall_long = _safe_metric(float(true_long.sum()), float(actual_up.sum()))
        precision_short = _safe_metric(float(true_short.sum()), float(pred_short.sum()))
        recall_short = _safe_metric(float(true_short.sum()), float(actual_down.sum()))
        recall_values = [value for value in [recall_long, recall_short] if value is not None]
        balanced_accuracy = float(np.mean(recall_values)) if recall_values else None
        auc_proxy = _auc_from_scores(binary_up[future.notna()], signal[future.notna()])
        signed_score = signal * future
        incremental_r2 = _r2_against_intercept(future, signal)
        summary_rows.append(
            {
                "strategy_id": strategy_id,
                "rows_evaluated": int(len(features)),
                "nonzero_signal_rows": int(signal.ne(0).sum()),
                "directional_eval_rows": int(valid_direction.sum()),
                "true_long_rows": int(true_long.sum()),
                "false_long_rows": int((pred_long & actual_down).sum()),
                "true_short_rows": int(true_short.sum()),
                "false_short_rows": int((pred_short & actual_up).sum()),
                "precision_long_proxy": precision_long,
                "recall_long_proxy": recall_long,
                "precision_short_proxy": precision_short,
                "recall_short_proxy": recall_short,
                "balanced_accuracy_proxy": balanced_accuracy,
                "rank_auc_proxy": auc_proxy,
                "incremental_r2_proxy": incremental_r2,
                "mean_signed_future_return_proxy": float(signed_score[signal.ne(0) & future.notna()].mean()) if int((signal.ne(0) & future.notna()).sum()) else None,
                "metric_scope": "phase11_ternary_signal_predictive_proxy_not_acceptance",
            }
        )
        bucket_frame = pd.DataFrame(
            {
                "strategy_id": strategy_id,
                "signal_score_bucket": np.select([signal < 0, signal > 0], ["short_signal", "long_signal"], default="flat_signal"),
                "future_mid_return_1": future,
                "signed_future_return": signal * future,
            }
        )
        grouped = (
            bucket_frame.groupby(["strategy_id", "signal_score_bucket"], sort=True)
            .agg(
                rows=("future_mid_return_1", "count"),
                mean_future_return=("future_mid_return_1", "mean"),
                mean_signed_future_return=("signed_future_return", "mean"),
                positive_future_fraction=("future_mid_return_1", lambda values: float((values > 0).mean())),
            )
            .reset_index()
        )
        grouped["metric_scope"] = "ternary_signal_bucket_not_true_decile"
        bucket_rows.append(grouped)

    return pd.DataFrame(summary_rows), pd.concat(bucket_rows, ignore_index=True)


def predictive_calibration_proxies(inputs: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame]:
    features = inputs["features"].copy()
    future = features["future_mid_return_1"].astype(float)
    valid = future.notna()
    binary_up = (future > 0).astype(int)
    signals = build_signals(features)
    brier_rows = []
    curve_rows = []
    bins = [-0.001, 0.2, 0.4, 0.6, 0.8, 1.001]
    labels = ["0.0_0.2", "0.2_0.4", "0.4_0.6", "0.6_0.8", "0.8_1.0"]
    for strategy_id, signal in signals.items():
        signal = signal.astype(float)
        p_up = (0.5 + 0.2 * signal).clip(0.05, 0.95)
        eval_mask = valid & p_up.notna()
        if int(eval_mask.sum()) == 0:
            brier_rows.append(
                {
                    "strategy_id": strategy_id,
                    "rows_evaluated": 0,
                    "brier_score_proxy": None,
                    "baseline_brier_score_proxy": None,
                    "brier_skill_score_proxy": None,
                    "mean_predicted_up_probability": None,
                    "observed_up_fraction": None,
                    "metric_scope": "ternary_signal_probability_proxy_not_calibrated_model",
                }
            )
            continue
        y = binary_up[eval_mask].astype(float)
        p = p_up[eval_mask].astype(float)
        baseline = float(y.mean())
        brier = float(((p - y) ** 2).mean())
        baseline_brier = float(((baseline - y) ** 2).mean())
        brier_rows.append(
            {
                "strategy_id": strategy_id,
                "rows_evaluated": int(eval_mask.sum()),
                "brier_score_proxy": brier,
                "baseline_brier_score_proxy": baseline_brier,
                "brier_skill_score_proxy": _safe_metric(baseline_brier - brier, baseline_brier),
                "mean_predicted_up_probability": float(p.mean()),
                "observed_up_fraction": float(y.mean()),
                "metric_scope": "ternary_signal_probability_proxy_not_calibrated_model",
            }
        )
        frame = pd.DataFrame(
            {
                "strategy_id": strategy_id,
                "probability_bucket": pd.cut(p, bins=bins, labels=labels, include_lowest=True),
                "predicted_up_probability": p,
                "actual_up": y,
            }
        )
        grouped = (
            frame.groupby(["strategy_id", "probability_bucket"], observed=False, sort=True)
            .agg(
                rows=("actual_up", "count"),
                mean_predicted_up_probability=("predicted_up_probability", "mean"),
                observed_up_fraction=("actual_up", "mean"),
            )
            .reset_index()
        )
        grouped["calibration_error_abs"] = (
            grouped["mean_predicted_up_probability"] - grouped["observed_up_fraction"]
        ).abs()
        grouped["metric_scope"] = "ternary_signal_probability_bucket_proxy_not_acceptance"
        curve_rows.append(grouped)
    return pd.DataFrame(brier_rows), pd.concat(curve_rows, ignore_index=True)


def predictive_baseline_comparison(
    predictive: pd.DataFrame,
    predictive_proxy: pd.DataFrame,
    brier: pd.DataFrame,
) -> pd.DataFrame:
    rows = predictive.merge(
        predictive_proxy[
            [
                "strategy_id",
                "directional_eval_rows",
                "balanced_accuracy_proxy",
                "rank_auc_proxy",
                "incremental_r2_proxy",
            ]
        ],
        on="strategy_id",
        how="left",
    ).merge(
        brier[
            [
                "strategy_id",
                "brier_score_proxy",
                "baseline_brier_score_proxy",
                "brier_skill_score_proxy",
                "observed_up_fraction",
            ]
        ],
        on="strategy_id",
        how="left",
    )
    rows["no_skill_directional_accuracy_baseline"] = 0.5
    rows["majority_direction_accuracy_baseline"] = rows["observed_up_fraction"].map(
        lambda value: max(float(value), 1.0 - float(value)) if pd.notna(value) else np.nan
    )
    rows["directional_accuracy_excess_vs_no_skill"] = (
        rows["directional_accuracy_nonzero"] - rows["no_skill_directional_accuracy_baseline"]
    )
    rows["directional_accuracy_excess_vs_majority"] = (
        rows["directional_accuracy_nonzero"] - rows["majority_direction_accuracy_baseline"]
    )
    rows["beats_no_skill_accuracy_proxy"] = rows["directional_accuracy_excess_vs_no_skill"] > 0
    rows["beats_majority_accuracy_proxy"] = rows["directional_accuracy_excess_vs_majority"] > 0
    rows["beats_brier_baseline_proxy"] = rows["brier_skill_score_proxy"] > 0
    rows["has_minimum_directional_rows_proxy"] = rows["directional_eval_rows"].fillna(0) >= 1_000
    rows["support_level_blocks_acceptance"] = rows["support_level"].astype(str).ne("runnable_proxy")
    rows["predictive_baseline_status"] = np.select(
        [
            rows["support_level_blocks_acceptance"],
            rows["directional_eval_rows"].fillna(0).eq(0),
            rows["beats_no_skill_accuracy_proxy"]
            & rows["beats_majority_accuracy_proxy"]
            & rows["beats_brier_baseline_proxy"]
            & rows["has_minimum_directional_rows_proxy"],
        ],
        [
            "unsupported_or_partial_strategy_proxy",
            "no_directional_evaluation_rows",
            "beats_proxy_baselines_not_acceptance",
        ],
        default="does_not_beat_required_proxy_baselines",
    )
    rows["acceptance_eligible_now"] = False
    rows["metric_scope"] = "phase16_predictive_baseline_proxy_not_acceptance"
    return rows[
        [
            "strategy_id",
            "name",
            "support_level",
            "directional_eval_rows",
            "directional_accuracy_nonzero",
            "balanced_accuracy_proxy",
            "rank_auc_proxy",
            "incremental_r2_proxy",
            "observed_up_fraction",
            "no_skill_directional_accuracy_baseline",
            "majority_direction_accuracy_baseline",
            "directional_accuracy_excess_vs_no_skill",
            "directional_accuracy_excess_vs_majority",
            "brier_score_proxy",
            "baseline_brier_score_proxy",
            "brier_skill_score_proxy",
            "beats_no_skill_accuracy_proxy",
            "beats_majority_accuracy_proxy",
            "beats_brier_baseline_proxy",
            "has_minimum_directional_rows_proxy",
            "predictive_baseline_status",
            "promotion_allowed",
            "acceptance_status",
            "acceptance_eligible_now",
            "metric_scope",
        ]
    ]


def _scenario_segment(day: object) -> str:
    try:
        value = int(day)
    except (TypeError, ValueError):
        return "unknown"
    if value <= 30:
        return "calibration_development"
    if value <= 45:
        return "validation"
    return "untouched_test"


def predictive_holdout_stability(inputs: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame]:
    features = inputs["features"].copy()
    matrix = inputs["signal_diagnostics"][["strategy_id", "name", "support_level"]].drop_duplicates()
    features["scenario_segment"] = features["scenario_day"].map(_scenario_segment)
    future = features["future_mid_return_1"].astype(float)
    future_sign = np.sign(future)
    signals = build_signals(features)
    group_cols = ["quarter_profile", "feed_profile", "scenario_segment"]
    detail_rows = []

    for _, spec in matrix.sort_values("strategy_id").iterrows():
        strategy_id = str(spec["strategy_id"])
        signal = signals.get(strategy_id)
        if signal is None:
            detail_rows.append(
                {
                    "strategy_id": strategy_id,
                    "name": spec.get("name"),
                    "support_level": spec.get("support_level"),
                    "quarter_profile": "not_supported",
                    "feed_profile": "not_supported",
                    "scenario_segment": "not_supported",
                    "rows_evaluated": int(len(features)),
                    "directional_eval_rows": 0,
                    "signal_rows": 0,
                    "directional_accuracy_proxy": None,
                    "majority_direction_baseline": None,
                    "accuracy_excess_vs_majority": None,
                    "mean_signed_future_return": None,
                    "stability_cell_status": "not_supported_by_current_product",
                    "metric_scope": "phase16_predictive_holdout_stability_proxy_not_acceptance",
                }
            )
            continue
        signal = signal.astype(float)
        frame = features[group_cols].copy()
        frame["signal"] = signal
        frame["future"] = future
        frame["future_sign"] = future_sign
        frame["signed_future_return"] = signal * future
        frame["eval_mask"] = signal.ne(0) & future.notna() & future.ne(0)
        for keys, group in frame.groupby(group_cols, sort=True):
            eval_group = group[group["eval_mask"]].copy()
            directional_rows = int(len(eval_group))
            if directional_rows:
                accuracy = float((np.sign(eval_group["signal"]) == eval_group["future_sign"]).mean())
                up_fraction = float((eval_group["future"] > 0).mean())
                majority = max(up_fraction, 1.0 - up_fraction)
                excess = accuracy - majority
                signed_mean = float(eval_group["signed_future_return"].mean())
                status = "beats_local_majority_proxy" if excess > 0 and directional_rows >= 1_000 else "does_not_beat_local_majority_proxy"
            else:
                accuracy = None
                majority = None
                excess = None
                signed_mean = None
                status = "no_directional_rows"
            detail_rows.append(
                {
                    "strategy_id": strategy_id,
                    "name": spec.get("name"),
                    "support_level": spec.get("support_level"),
                    "quarter_profile": keys[0],
                    "feed_profile": keys[1],
                    "scenario_segment": keys[2],
                    "rows_evaluated": int(len(group)),
                    "directional_eval_rows": directional_rows,
                    "signal_rows": int(group["signal"].ne(0).sum()),
                    "directional_accuracy_proxy": accuracy,
                    "majority_direction_baseline": majority,
                    "accuracy_excess_vs_majority": excess,
                    "mean_signed_future_return": signed_mean,
                    "stability_cell_status": status,
                    "metric_scope": "phase16_predictive_holdout_stability_proxy_not_acceptance",
                }
            )

    detail = pd.DataFrame(detail_rows)
    summary_rows = []
    for strategy_id, group in detail.groupby("strategy_id", sort=True):
        supported = group["stability_cell_status"].astype(str).ne("not_supported_by_current_product")
        eval_group = group[supported & group["directional_eval_rows"].fillna(0).gt(0)].copy()
        beat_group = eval_group[eval_group["stability_cell_status"].astype(str).eq("beats_local_majority_proxy")]
        test_group = eval_group[eval_group["scenario_segment"].astype(str).eq("untouched_test")]
        summary_rows.append(
            {
                "strategy_id": strategy_id,
                "name": group["name"].dropna().iloc[0] if group["name"].notna().any() else None,
                "support_level": group["support_level"].dropna().iloc[0] if group["support_level"].notna().any() else None,
                "stability_cells": int(len(eval_group)),
                "cells_with_minimum_rows": int((eval_group["directional_eval_rows"] >= 1_000).sum()) if len(eval_group) else 0,
                "cells_beating_local_majority": int(len(beat_group)),
                "cell_beat_fraction": float(len(beat_group) / len(eval_group)) if len(eval_group) else 0.0,
                "untouched_test_cells": int(len(test_group)),
                "untouched_test_cells_beating_local_majority": int(
                    (test_group["stability_cell_status"].astype(str) == "beats_local_majority_proxy").sum()
                ) if len(test_group) else 0,
                "min_accuracy_excess_vs_majority": float(eval_group["accuracy_excess_vs_majority"].min()) if len(eval_group) else None,
                "median_accuracy_excess_vs_majority": float(eval_group["accuracy_excess_vs_majority"].median()) if len(eval_group) else None,
                "worst_segment_status": (
                    "not_supported_by_current_product"
                    if not len(eval_group)
                    else ("all_cells_beat_local_majority_proxy" if len(beat_group) == len(eval_group) else "fails_some_holdout_stability_cells")
                ),
                "acceptance_eligible_now": False,
                "blocker": (
                    "Proxy holdout stability cells do not consistently beat local majority baselines; acceptance requires multi-seed, walk-forward and later real holdout predictive validation."
                    if len(eval_group)
                    else "Strategy is not supported by the current feature product for predictive holdout stability validation."
                ),
                "metric_scope": "phase16_predictive_holdout_stability_summary_proxy_not_acceptance",
            }
        )
    return detail, pd.DataFrame(summary_rows)


def feature_importance_stability(inputs: dict[str, pd.DataFrame], sample_rows: int = 100_000, max_seeds: int = 12) -> pd.DataFrame:
    features = inputs["features"]
    seed_plan = inputs["seed_plan"].copy()
    seed_column = next((column for column in ["seed", "simulation_seed", "random_seed"] if column in seed_plan.columns), None)
    seeds = seed_plan[seed_column].dropna().astype(int).drop_duplicates().head(max_seeds).tolist() if seed_column else []
    if not seeds:
        seeds = [20260714]
    candidate_features = [
        "mlofi_qty",
        "momentum_3",
        "book_slope_l5",
        "event_intensity_proxy",
        "l5_imbalance",
        "l1_imbalance",
        "local_volatility_6",
        "spread_ticks",
        "book_convexity_l5",
    ]
    available_features = [column for column in candidate_features if column in features.columns]
    base_cols = [*available_features, "future_mid_return_1"]
    base = features[base_cols].dropna()
    if base.empty or not available_features:
        return pd.DataFrame(
            columns=[
                "feature_name",
                "seed_runs",
                "mean_abs_correlation_importance",
                "std_abs_correlation_importance",
                "coefficient_of_variation",
                "mean_rank",
                "rank_std",
                "top3_frequency",
                "metric_scope",
            ]
        )
    rows = []
    replace = len(base) < sample_rows
    n = min(sample_rows, len(base)) if not replace else sample_rows
    for seed in seeds:
        sample = base.sample(n=n, replace=replace, random_state=seed)
        target = sample["future_mid_return_1"].astype(float)
        importances = {}
        for feature_name in available_features:
            value = sample[feature_name].astype(float)
            corr = value.corr(target)
            importances[feature_name] = 0.0 if pd.isna(corr) else abs(float(corr))
        ranked = pd.Series(importances).rank(method="average", ascending=False)
        for feature_name, importance in importances.items():
            rows.append(
                {
                    "seed": seed,
                    "feature_name": feature_name,
                    "abs_correlation_importance": importance,
                    "rank": float(ranked[feature_name]),
                    "in_top3": bool(ranked[feature_name] <= 3),
                }
            )
    frame = pd.DataFrame(rows)
    out = (
        frame.groupby("feature_name", sort=True)
        .agg(
            seed_runs=("seed", "nunique"),
            mean_abs_correlation_importance=("abs_correlation_importance", "mean"),
            std_abs_correlation_importance=("abs_correlation_importance", "std"),
            mean_rank=("rank", "mean"),
            rank_std=("rank", "std"),
            top3_frequency=("in_top3", "mean"),
        )
        .reset_index()
    )
    out["coefficient_of_variation"] = out.apply(
        lambda row: _safe_metric(float(row["std_abs_correlation_importance"]), float(row["mean_abs_correlation_importance"])),
        axis=1,
    )
    out["metric_scope"] = "seed_sampled_feature_target_association_proxy_not_model_importance"
    return out.sort_values(["top3_frequency", "mean_abs_correlation_importance"], ascending=[False, False], kind="mergesort")


def predictive_promotion_falsification(
    baseline_comparison: pd.DataFrame,
    holdout_stability_summary: pd.DataFrame,
    importance: pd.DataFrame,
    acceptance_summary: pd.DataFrame,
) -> pd.DataFrame:
    acceptance = acceptance_summary[["strategy_id", "acceptance_status"]].copy()
    baseline_cols = [
        "strategy_id",
        "support_level",
        "directional_eval_rows",
        "directional_accuracy_excess_vs_no_skill",
        "directional_accuracy_excess_vs_majority",
        "brier_skill_score_proxy",
        "beats_no_skill_accuracy_proxy",
        "beats_majority_accuracy_proxy",
        "beats_brier_baseline_proxy",
        "has_minimum_directional_rows_proxy",
        "predictive_baseline_status",
    ]
    holdout_cols = [
        "strategy_id",
        "stability_cells",
        "cells_with_minimum_rows",
        "cells_beating_local_majority",
        "cell_beat_fraction",
        "untouched_test_cells",
        "untouched_test_cells_beating_local_majority",
        "min_accuracy_excess_vs_majority",
        "worst_segment_status",
    ]
    rows = acceptance.merge(baseline_comparison[baseline_cols], on="strategy_id", how="left").merge(
        holdout_stability_summary[holdout_cols],
        on="strategy_id",
        how="left",
    )

    stable_features = importance.copy()
    if len(stable_features):
        stable_features["feature_stable_proxy"] = (
            stable_features["top3_frequency"].astype(float).fillna(0.0) >= 0.5
        ) & (
            stable_features["coefficient_of_variation"].astype(float).replace([np.inf, -np.inf], np.nan).fillna(999.0) <= 1.5
        )
        feature_stability_ready = bool(stable_features["feature_stable_proxy"].any())
        stable_feature_count = int(stable_features["feature_stable_proxy"].sum())
        max_top3_frequency = float(stable_features["top3_frequency"].max())
        median_feature_cv = float(stable_features["coefficient_of_variation"].replace([np.inf, -np.inf], np.nan).median())
    else:
        feature_stability_ready = False
        stable_feature_count = 0
        max_top3_frequency = 0.0
        median_feature_cv = np.nan

    for column in [
        "beats_no_skill_accuracy_proxy",
        "beats_majority_accuracy_proxy",
        "beats_brier_baseline_proxy",
        "has_minimum_directional_rows_proxy",
    ]:
        rows[column] = rows[column].fillna(False).astype(bool)
    numeric_defaults = {
        "directional_eval_rows": 0,
        "stability_cells": 0,
        "cells_with_minimum_rows": 0,
        "cells_beating_local_majority": 0,
        "cell_beat_fraction": 0.0,
        "untouched_test_cells": 0,
        "untouched_test_cells_beating_local_majority": 0,
    }
    for column, default in numeric_defaults.items():
        rows[column] = rows[column].fillna(default)
    rows["support_level"] = rows["support_level"].fillna("not_supported_by_current_product")
    rows["predictive_baseline_status"] = rows["predictive_baseline_status"].fillna("no_predictive_baseline_evidence")
    rows["worst_segment_status"] = rows["worst_segment_status"].fillna("no_holdout_stability_evidence")
    rows["baseline_pass_proxy"] = (
        rows["beats_no_skill_accuracy_proxy"]
        & rows["beats_majority_accuracy_proxy"]
        & rows["beats_brier_baseline_proxy"]
        & rows["has_minimum_directional_rows_proxy"]
        & rows["support_level"].astype(str).eq("runnable_proxy")
    )
    rows["holdout_all_cell_pass_proxy"] = rows["worst_segment_status"].astype(str).eq("all_cells_beat_local_majority_proxy")
    rows["untouched_test_pass_proxy"] = (
        rows["untouched_test_cells"].astype(float) > 0
    ) & (
        rows["untouched_test_cells_beating_local_majority"].astype(float) == rows["untouched_test_cells"].astype(float)
    )
    rows["feature_stability_proxy_available"] = feature_stability_ready
    rows["stable_feature_count_proxy"] = stable_feature_count
    rows["max_feature_top3_frequency_proxy"] = max_top3_frequency
    rows["median_feature_importance_cv_proxy"] = median_feature_cv
    rows["predictive_promotion_candidate_proxy"] = (
        rows["baseline_pass_proxy"]
        & rows["holdout_all_cell_pass_proxy"]
        & rows["untouched_test_pass_proxy"]
        & rows["feature_stability_proxy_available"]
        & rows["support_level"].astype(str).eq("runnable_proxy")
    )

    def _reason(row: pd.Series) -> str:
        reasons: list[str] = []
        if str(row["support_level"]) != "runnable_proxy":
            reasons.append("strategy support is partial or unsupported")
        if not bool(row["baseline_pass_proxy"]):
            reasons.append("does not clear required no-skill, majority and Brier proxy baselines")
        if not bool(row["holdout_all_cell_pass_proxy"]):
            reasons.append("does not beat local-majority baseline in every holdout stability cell")
        if not bool(row["untouched_test_pass_proxy"]):
            reasons.append("untouched-test segment stability is incomplete or failing")
        if not bool(row["feature_stability_proxy_available"]):
            reasons.append("feature-importance stability proxy has no stable top feature")
        reasons.append("requires multi-seed/walk-forward rerun and later real multi-day holdout before acceptance")
        return "; ".join(reasons)

    rows["falsification_status"] = np.where(
        rows["predictive_promotion_candidate_proxy"],
        "proxy_candidate_not_acceptance",
        "falsified_for_predictive_promotion_under_current_proxy_evidence",
    )
    rows["acceptance_eligible_now"] = False
    rows["blocker"] = rows.apply(_reason, axis=1)
    rows["metric_scope"] = "phase16_predictive_promotion_falsification_proxy_not_acceptance"
    return rows[
        [
            "strategy_id",
            "support_level",
            "acceptance_status",
            "directional_eval_rows",
            "directional_accuracy_excess_vs_no_skill",
            "directional_accuracy_excess_vs_majority",
            "brier_skill_score_proxy",
            "baseline_pass_proxy",
            "predictive_baseline_status",
            "stability_cells",
            "cells_with_minimum_rows",
            "cells_beating_local_majority",
            "cell_beat_fraction",
            "untouched_test_cells",
            "untouched_test_cells_beating_local_majority",
            "min_accuracy_excess_vs_majority",
            "holdout_all_cell_pass_proxy",
            "untouched_test_pass_proxy",
            "worst_segment_status",
            "feature_stability_proxy_available",
            "stable_feature_count_proxy",
            "max_feature_top3_frequency_proxy",
            "median_feature_importance_cv_proxy",
            "predictive_promotion_candidate_proxy",
            "falsification_status",
            "acceptance_eligible_now",
            "blocker",
            "metric_scope",
        ]
    ].sort_values(["predictive_promotion_candidate_proxy", "strategy_id"], ascending=[False, True], kind="mergesort")


def predictive_acceptance_gap_ledger(
    baseline_comparison: pd.DataFrame,
    holdout_stability_summary: pd.DataFrame,
    importance: pd.DataFrame,
    predictive_falsification: pd.DataFrame,
    acceptance_summary: pd.DataFrame,
) -> pd.DataFrame:
    columns = [
        "strategy_id",
        "predictive_requirement",
        "required_threshold",
        "observed_value",
        "current_evidence_status",
        "proxy_evidence_available",
        "acceptance_requirement_met",
        "blocking_gap",
        "evidence_source",
        "required_next_evidence",
        "acceptance_eligible_now",
    ]
    evidence_source = (
        "outputs/phase11/strategy_signal_diagnostics.csv; "
        "outputs/phase16/predictive_baseline_comparison.csv; "
        "outputs/phase16/predictive_holdout_stability_summary.csv; "
        "outputs/phase16/feature_importance_stability_proxy.csv; "
        "outputs/phase16/predictive_promotion_falsification.csv"
    )
    rows: list[dict] = []
    feature_proxy_available = bool(len(importance))
    stable_feature_count = 0
    if len(importance):
        stable_feature_count = int(
            (
                (importance["top3_frequency"].astype(float).fillna(0.0) >= 0.5)
                & (
                    importance["coefficient_of_variation"]
                    .astype(float)
                    .replace([np.inf, -np.inf], np.nan)
                    .fillna(999.0)
                    <= 1.5
                )
            ).sum()
        )

    for record in acceptance_summary.sort_values("strategy_id").to_dict("records"):
        strategy_id = str(record["strategy_id"])
        baseline = baseline_comparison[baseline_comparison["strategy_id"].astype(str) == strategy_id]
        holdout = holdout_stability_summary[holdout_stability_summary["strategy_id"].astype(str) == strategy_id]
        falsification = predictive_falsification[predictive_falsification["strategy_id"].astype(str) == strategy_id]
        baseline_row = baseline.iloc[0] if len(baseline) else pd.Series(dtype="object")
        holdout_row = holdout.iloc[0] if len(holdout) else pd.Series(dtype="object")
        falsification_row = falsification.iloc[0] if len(falsification) else pd.Series(dtype="object")
        support_level = str(baseline_row.get("support_level", record.get("support_level", "not_available")))
        baseline_pass = bool(falsification_row.get("baseline_pass_proxy", False))
        holdout_pass = bool(falsification_row.get("holdout_all_cell_pass_proxy", False))
        untouched_pass = bool(falsification_row.get("untouched_test_pass_proxy", False))
        feature_pass = bool(falsification_row.get("feature_stability_proxy_available", feature_proxy_available))
        candidate_proxy = bool(falsification_row.get("predictive_promotion_candidate_proxy", False))
        def as_int(value: object) -> int:
            if pd.isna(value):
                return 0
            return int(float(value))

        directional_rows = as_int(baseline_row.get("directional_eval_rows", 0)) if len(baseline) else 0
        stability_cells = as_int(holdout_row.get("stability_cells", 0)) if len(holdout) else 0
        cells_beating = as_int(holdout_row.get("cells_beating_local_majority", 0)) if len(holdout) else 0
        untouched_cells = as_int(holdout_row.get("untouched_test_cells", 0)) if len(holdout) else 0
        untouched_beating = as_int(holdout_row.get("untouched_test_cells_beating_local_majority", 0)) if len(holdout) else 0

        def add(
            predictive_requirement: str,
            required_threshold: str,
            observed_value: str,
            current_evidence_status: str,
            proxy_evidence_available: bool,
            blocking_gap: str,
            required_next_evidence: str,
        ) -> None:
            rows.append(
                {
                    "strategy_id": strategy_id,
                    "predictive_requirement": predictive_requirement,
                    "required_threshold": required_threshold,
                    "observed_value": observed_value,
                    "current_evidence_status": current_evidence_status,
                    "proxy_evidence_available": bool(proxy_evidence_available),
                    "acceptance_requirement_met": False,
                    "blocking_gap": blocking_gap,
                    "evidence_source": evidence_source,
                    "required_next_evidence": required_next_evidence,
                    "acceptance_eligible_now": False,
                }
            )

        add(
            "strategy_support_ready",
            "strategy is runnable in the current feature product",
            f"support_level={support_level}",
            "runnable_proxy_not_acceptance" if support_level == "runnable_proxy" else "partial_or_unsupported_strategy",
            support_level == "runnable_proxy",
            "Runnable proxy support is necessary but not sufficient for predictive acceptance.",
            "Implement missing required features/modules or explicitly classify the strategy as research-only before predictive promotion.",
        )
        add(
            "baseline_outperformance",
            "beats no-skill, local majority and Brier proxy baselines with enough rows",
            (
                f"rows={directional_rows}; baseline_pass_proxy={baseline_pass}; "
                f"accuracy_excess_vs_majority={baseline_row.get('directional_accuracy_excess_vs_majority', 'NA')}; "
                f"brier_skill={baseline_row.get('brier_skill_score_proxy', 'NA')}"
            ),
            "baseline_proxy_available_not_acceptance" if len(baseline) else "missing_baseline_proxy",
            bool(len(baseline)),
            "Current baseline comparison is proxy-only and does not clear all required baseline checks.",
            "Run calibrated predictive validation and require positive accuracy/Brier skill versus no-skill and local-majority baselines.",
        )
        add(
            "holdout_cell_stability",
            "beats local-majority baseline in every quarter/feed/segment holdout cell",
            f"{cells_beating}/{stability_cells} cells beating local majority; all_cell_pass={holdout_pass}",
            "holdout_stability_proxy_available_not_acceptance" if len(holdout) else "missing_holdout_stability_proxy",
            bool(len(holdout)),
            "Current proxy holdout cells do not consistently beat local-majority baselines.",
            "Run predeclared holdout-cell validation over multi-seed synthetic and untouched holdout-generator outputs.",
        )
        add(
            "untouched_test_stability",
            "all untouched-test cells beat local-majority baseline",
            f"{untouched_beating}/{untouched_cells} untouched cells beating local majority; untouched_pass={untouched_pass}",
            "untouched_test_proxy_available_not_acceptance" if len(holdout) else "missing_untouched_test_proxy",
            bool(len(holdout) and untouched_cells > 0),
            "Untouched-test stability is incomplete or failing in current proxy evidence.",
            "Reserve untouched cells and require all to beat local-majority baselines without feature or threshold reuse.",
        )
        add(
            "feature_stability",
            "stable predictive feature importance across seed samples",
            f"feature_proxy_available={feature_proxy_available}; stable_feature_count={stable_feature_count}; feature_pass={feature_pass}",
            "feature_stability_proxy_available_not_acceptance" if feature_proxy_available else "missing_feature_stability_proxy",
            feature_proxy_available,
            "Feature stability is a seed-sampled association proxy, not calibrated model importance stability.",
            "Train calibrated predictive models across registered seeds and require stable feature importance / attribution.",
        )
        add(
            "multi_seed_walk_forward_validation",
            "registered multi-seed and walk-forward predictive validation complete",
            "not available in current proxy evidence",
            "missing_multi_seed_walk_forward_predictive_validation",
            False,
            "Current predictive evidence is single current proxy diagnostics, not full registered multi-seed/walk-forward validation.",
            "Execute the Phase 13 seed plan and walk-forward windows for predictive models without test reuse.",
        )
        add(
            "calibrated_model_output",
            "calibrated probability or score model with acceptance-grade calibration diagnostics",
            "ternary pseudo-probability proxy only",
            "missing_calibrated_model_output",
            False,
            "Current Brier/calibration rows are deterministic ternary-signal pseudo-probabilities, not calibrated model outputs.",
            "Train and freeze calibrated probability models, then evaluate Brier, calibration curve and baseline lift out of sample.",
        )
        add(
            "real_multi_day_holdout",
            "predictive edge survives multi-day real market holdout",
            "not available in current one-day/proxy evidence",
            "missing_real_multi_day_predictive_holdout",
            False,
            "Current predictive evidence has no multi-day real holdout validation.",
            "Collect/run multiple real market days and compare predictive stability against synthetic and holdout-generator results.",
        )
        add(
            "promotion_falsification_clear",
            "not falsified by baseline, holdout, untouched-test, feature-stability or support checks",
            f"predictive_promotion_candidate_proxy={candidate_proxy}; status={falsification_row.get('falsification_status', 'missing')}",
            "promotion_falsification_proxy_available_not_acceptance" if len(falsification) else "missing_promotion_falsification",
            bool(len(falsification)),
            "Current predictive promotion-falsification ledger marks no strategy as acceptance-ready.",
            "Clear the full predictive promotion-falsification checklist after calibrated, multi-seed and real/holdout validation.",
        )

    return pd.DataFrame(rows, columns=columns).sort_values(["strategy_id", "predictive_requirement"], kind="mergesort")


def _safe_div(num: float, den: float) -> float | None:
    if den == 0 or pd.isna(den):
        return None
    return float(num / den)


def _sample_trade_metrics(sample: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (strategy_id, execution_profile), group in sample.groupby(["strategy_id", "execution_profile"], sort=True):
        net = group["net_return"].astype(float)
        gross = group["gross_return"].astype(float)
        costs = group["cost_return"].astype(float)
        wins = net[net > 0]
        losses = net[net < 0]
        cumulative = net.cumsum()
        running_max = cumulative.cummax()
        drawdown = cumulative - running_max
        downside = net[net < 0]
        rows.append(
            {
                "strategy_id": strategy_id,
                "execution_profile": execution_profile,
                "sample_trades": int(len(group)),
                "sample_mean_net_return": float(net.mean()) if len(group) else None,
                "sample_sharpe_per_trade": _safe_div(float(net.mean()), float(net.std(ddof=1))) if len(net) > 1 else None,
                "sample_sortino_per_trade": _safe_div(float(net.mean()), float(downside.std(ddof=1))) if len(downside) > 1 else None,
                "sample_max_drawdown_units": float(drawdown.min()) if len(drawdown) else None,
                "sample_profit_factor": _safe_div(float(wins.sum()), abs(float(losses.sum()))) if len(losses) else None,
                "sample_average_win": float(wins.mean()) if len(wins) else None,
                "sample_average_loss": float(losses.mean()) if len(losses) else None,
                "sample_cost_to_gross_profit_ratio": _safe_div(float(costs.sum()), float(gross[gross > 0].sum())),
            }
        )
    return pd.DataFrame(rows)


def markout_analysis(sample: pd.DataFrame, horizons: tuple[int, ...] = (1, 3, 6)) -> pd.DataFrame:
    required = {"quarter_profile", "trade_date", "symbol", "bar_index", "strategy_id", "execution_profile", "side", "mid_price"}
    missing = required.difference(sample.columns)
    if missing:
        raise ValueError(f"trade sample is missing required markout columns: {sorted(missing)}")
    base = sample.copy()
    group_cols = ["quarter_profile", "trade_date", "symbol"]
    base = base.sort_values(group_cols + ["bar_index"], kind="mergesort").reset_index(drop=True)
    for horizon in horizons:
        future_mid = base.groupby(group_cols, sort=False)["mid_price"].shift(-horizon)
        base[f"signed_markout_{horizon}bar"] = base["side"].astype(float) * (future_mid.astype(float) - base["mid_price"].astype(float)) / base["mid_price"].astype(float)

    markout_cols = [f"signed_markout_{horizon}bar" for horizon in horizons]
    base["valid_markout_windows"] = base[markout_cols].notna().sum(axis=1)
    base["mae_proxy"] = base[markout_cols].min(axis=1, skipna=True)
    base["mfe_proxy"] = base[markout_cols].max(axis=1, skipna=True)
    base["adverse_selection_proxy"] = base[markout_cols[-1]] < 0
    valid = base[base["valid_markout_windows"] > 0].copy()
    if valid.empty:
        return pd.DataFrame(
            columns=[
                "strategy_id",
                "execution_profile",
                "markout_sample_trades",
                "adverse_selection_rate_6bar_proxy",
                "mean_markout_1bar",
                "mean_markout_3bar",
                "mean_markout_6bar",
                "mean_mae_proxy",
                "mean_mfe_proxy",
                "worst_mae_proxy",
                "best_mfe_proxy",
                "metric_scope",
            ]
        )
    rows = []
    for (strategy_id, execution_profile), group in valid.groupby(["strategy_id", "execution_profile"], sort=True):
        rows.append(
            {
                "strategy_id": strategy_id,
                "execution_profile": execution_profile,
                "markout_sample_trades": int(len(group)),
                "adverse_selection_rate_6bar_proxy": float(group["adverse_selection_proxy"].mean()),
                "mean_markout_1bar": float(group["signed_markout_1bar"].mean()),
                "mean_markout_3bar": float(group["signed_markout_3bar"].mean()),
                "mean_markout_6bar": float(group["signed_markout_6bar"].mean()),
                "mean_mae_proxy": float(group["mae_proxy"].mean()),
                "mean_mfe_proxy": float(group["mfe_proxy"].mean()),
                "worst_mae_proxy": float(group["mae_proxy"].min()),
                "best_mfe_proxy": float(group["mfe_proxy"].max()),
                "metric_scope": "phase12_sampled_trade_markout_not_acceptance",
            }
        )
    return pd.DataFrame(rows)


def trading_scoreboard(inputs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    summary = inputs["execution_summary"].copy()
    sample_metrics = _sample_trade_metrics(inputs["trade_sample"])
    markouts = inputs.get("markout_analysis", pd.DataFrame())
    out = summary.merge(sample_metrics, on=["strategy_id", "execution_profile"], how="left")
    if not markouts.empty:
        out = out.merge(markouts.drop(columns=["metric_scope"], errors="ignore"), on=["strategy_id", "execution_profile"], how="left")
    out["gross_pnl_units_proxy"] = out["mean_gross_return"] * out["trades"]
    out["net_pnl_units_proxy"] = out["total_net_pnl_units"]
    out["expectancy_per_trade_proxy"] = out["mean_net_return"]
    out["turnover_trade_count_proxy"] = out["trades"]
    out["metric_scope"] = "phase12_5m_marketable_proxy_not_acceptance"
    return out[
        [
            "strategy_id",
            "name",
            "execution_profile",
            "trades",
            "gross_pnl_units_proxy",
            "net_pnl_units_proxy",
            "mean_gross_return",
            "mean_cost_return",
            "mean_net_return",
            "expectancy_per_trade_proxy",
            "win_rate_net",
            "turnover_trade_count_proxy",
            "sample_trades",
            "sample_sharpe_per_trade",
            "sample_sortino_per_trade",
            "sample_max_drawdown_units",
            "sample_profit_factor",
            "sample_average_win",
            "sample_average_loss",
            "sample_cost_to_gross_profit_ratio",
            "markout_sample_trades",
            "adverse_selection_rate_6bar_proxy",
            "mean_markout_1bar",
            "mean_markout_3bar",
            "mean_markout_6bar",
            "mean_mae_proxy",
            "mean_mfe_proxy",
            "worst_mae_proxy",
            "best_mfe_proxy",
            "metric_scope",
            "status",
        ]
    ]


def economic_viability_frontier(inputs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    summary = inputs["execution_summary"].copy()
    acceptance_columns = ["strategy_id", "promotion_allowed", "acceptance_status"]
    if "support_level" not in summary.columns and "support_level" in inputs["acceptance_summary"].columns:
        acceptance_columns.append("support_level")
    acceptance = inputs["acceptance_summary"][acceptance_columns].copy()
    out = summary.merge(acceptance, on="strategy_id", how="left")
    if "support_level" not in out.columns:
        out["support_level"] = ""
    out["gross_edge_bps"] = out["mean_gross_return"].astype(float) * 10_000.0
    out["cost_drag_bps"] = out["mean_cost_return"].astype(float) * 10_000.0
    out["net_edge_bps"] = out["mean_net_return"].astype(float) * 10_000.0
    out["zerodha_charge_bps"] = out.get("mean_zerodha_charge_bps", pd.Series(0.0, index=out.index)).fillna(0.0).astype(float)
    out["non_zerodha_cost_bps"] = out["cost_drag_bps"] - out["zerodha_charge_bps"]
    out["break_even_cost_bps"] = out["gross_edge_bps"]
    out["cost_surplus_bps"] = out["gross_edge_bps"] - out["cost_drag_bps"]
    out["additional_gross_edge_needed_bps"] = (-out["net_edge_bps"]).clip(lower=0.0)
    out["cost_reduction_needed_bps"] = (-out["cost_surplus_bps"]).clip(lower=0.0)
    out["gross_edge_covers_cost"] = out["gross_edge_bps"] > out["cost_drag_bps"]
    out["net_positive_proxy"] = out["net_edge_bps"] > 0
    out["retail_or_stress_profile"] = out["execution_profile"].astype(str).isin(["retail_marketable_default", "stressed_retail"])
    out["economic_frontier_status"] = np.select(
        [
            out["net_positive_proxy"] & out["retail_or_stress_profile"],
            ~out["retail_or_stress_profile"],
        ],
        [
            "net_positive_proxy_not_acceptance",
            "control_profile_not_deployable",
        ],
        default="below_break_even_after_costs",
    )
    out["acceptance_eligible_now"] = False
    out["blocker"] = np.where(
        out["net_positive_proxy"] & out["retail_or_stress_profile"],
        "Proxy net edge is positive for this profile, but acceptance still requires broker/exchange fills, multi-day holdout and stress-profile confirmation.",
        "Proxy net edge is not positive after the current cost/slippage/latency assumptions; improve gross edge, lower turnover/cost exposure, or reject the strategy before promotion.",
    )
    return out[
        [
            "strategy_id",
            "name",
            "support_level",
            "execution_profile",
            "trades",
            "gross_edge_bps",
            "cost_drag_bps",
            "zerodha_charge_bps",
            "non_zerodha_cost_bps",
            "net_edge_bps",
            "break_even_cost_bps",
            "cost_surplus_bps",
            "additional_gross_edge_needed_bps",
            "cost_reduction_needed_bps",
            "gross_edge_covers_cost",
            "net_positive_proxy",
            "retail_or_stress_profile",
            "economic_frontier_status",
            "promotion_allowed",
            "acceptance_status",
            "acceptance_eligible_now",
            "blocker",
        ]
    ]


def risk_adjusted_economic_frontier(economic_frontier: pd.DataFrame, inputs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    severity = inputs["risk_breach_severity"].copy()
    severity_cols = [
        "strategy_id",
        "execution_profile",
        "fill_model",
        "queue_position_bucket",
        "breach_days",
        "daily_loss_breach_days",
        "position_limit_breach_days",
        "drawdown_breach_days",
        "daily_halt_days",
        "breach_day_fraction",
        "daily_halt_day_fraction",
        "risk_severity_score",
        "risk_severity_band",
        "risk_pass_candidate_proxy",
    ]
    out = economic_frontier.merge(severity[severity_cols], on=["strategy_id", "execution_profile"], how="left")
    out["fill_model"] = out["fill_model"].fillna("not_available")
    out["risk_severity_band"] = out["risk_severity_band"].fillna("risk_severity_missing")
    out["risk_pass_candidate_proxy"] = out["risk_pass_candidate_proxy"].fillna(False).astype(bool)
    out["risk_severity_score"] = out["risk_severity_score"].fillna(np.inf).astype(float)
    out["breach_day_fraction"] = out["breach_day_fraction"].fillna(1.0).astype(float)
    out["daily_halt_day_fraction"] = out["daily_halt_day_fraction"].fillna(1.0).astype(float)
    out["risk_penalty_bps"] = out["risk_severity_score"].replace(np.inf, 10_000.0).clip(lower=0.0)
    out["risk_adjusted_net_edge_bps"] = out["net_edge_bps"].astype(float) - out["risk_penalty_bps"]
    out["net_positive_and_risk_pass_proxy"] = out["net_positive_proxy"].astype(bool) & out["risk_pass_candidate_proxy"]
    out["retail_stress_net_positive_and_risk_pass_proxy"] = (
        out["retail_or_stress_profile"].astype(bool)
        & out["net_positive_and_risk_pass_proxy"]
    )
    out["risk_adjusted_frontier_status"] = np.select(
        [
            out["net_positive_and_risk_pass_proxy"] & out["retail_or_stress_profile"].astype(bool),
            out["net_positive_proxy"].astype(bool) & ~out["risk_pass_candidate_proxy"],
            out["risk_pass_candidate_proxy"] & ~out["net_positive_proxy"].astype(bool),
            ~out["retail_or_stress_profile"].astype(bool),
        ],
        [
            "net_positive_and_risk_pass_proxy_not_acceptance",
            "economic_positive_but_risk_blocked_proxy",
            "risk_pass_but_economic_negative_proxy",
            "control_profile_not_deployable",
        ],
        default="economic_and_risk_blocked_proxy",
    )
    out["acceptance_eligible_now"] = False
    out["blocker"] = np.where(
        out["net_positive_and_risk_pass_proxy"],
        "Proxy economics and proxy risk pass candidate align, but acceptance still requires broker/exchange fills, contract-note reconciliation and multi-day holdout.",
        "Current row does not jointly clear proxy net-edge and proxy lifecycle risk-pass checks; do not promote.",
    )
    return out[
        [
            "strategy_id",
            "name",
            "support_level",
            "execution_profile",
            "fill_model",
            "queue_position_bucket",
            "gross_edge_bps",
            "cost_drag_bps",
            "net_edge_bps",
            "risk_penalty_bps",
            "risk_adjusted_net_edge_bps",
            "net_positive_proxy",
            "risk_pass_candidate_proxy",
            "net_positive_and_risk_pass_proxy",
            "retail_or_stress_profile",
            "retail_stress_net_positive_and_risk_pass_proxy",
            "breach_days",
            "daily_loss_breach_days",
            "position_limit_breach_days",
            "drawdown_breach_days",
            "daily_halt_days",
            "breach_day_fraction",
            "daily_halt_day_fraction",
            "risk_severity_score",
            "risk_severity_band",
            "risk_adjusted_frontier_status",
            "promotion_allowed",
            "acceptance_status",
            "acceptance_eligible_now",
            "blocker",
        ]
    ].sort_values(["risk_adjusted_net_edge_bps", "strategy_id", "execution_profile", "fill_model"], ascending=[False, True, True, True], kind="mergesort")


def broker_reconciliation_readiness_ledger(inputs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    cost_schedule = inputs["cost_schedule"].copy()
    component_catalog = inputs["charge_component_catalog"].copy()
    scenario_count = int(len(inputs["representative_charge_scenarios"]))
    modeled_components = set(component_catalog["component"].astype(str)) if "component" in component_catalog else set()
    cost_components = set(cost_schedule["cost_component"].astype(str)) if "cost_component" in cost_schedule else set()

    rows: list[dict] = []
    formula_items = [
        ("brokerage", "zerodha_brokerage_inr", "brokerage", "contract_note_brokerage"),
        ("stt", "zerodha_stt_inr", "stt", "contract_note_stt"),
        ("nse_transaction_charge", "zerodha_transaction_charge_inr", "nse_transaction_charge", "contract_note_exchange_transaction_charges"),
        ("sebi_charge", "zerodha_sebi_charge_inr", "sebi_charge", "contract_note_sebi_turnover_fees"),
        ("stamp_duty", "zerodha_stamp_duty_inr", "stamp_duty", "contract_note_stamp_duty"),
        ("gst", "zerodha_gst_inr", "gst", "contract_note_gst"),
        ("total_charges", "zerodha_total_charges_inr", "statutory_and_brokerage_charges", "contract_note_total_charges"),
    ]
    for item, proxy_field, evidence_key, broker_field in formula_items:
        component_row = component_catalog[component_catalog.get("component", pd.Series(dtype=str)).astype(str) == evidence_key]
        source_url = component_row["source_url"].iloc[0] if len(component_row) and "source_url" in component_row else ""
        formula = component_row["formula"].iloc[0] if len(component_row) and "formula" in component_row else ""
        proxy_available = evidence_key in modeled_components or evidence_key in cost_components
        rows.append(
            {
                "reconciliation_domain": "charges",
                "reconciliation_item": item,
                "proxy_field_or_artifact": proxy_field,
                "proxy_evidence": "outputs/phase12/cost_schedule.csv; outputs/phase12/charge_component_catalog.csv; outputs/phase12/representative_charge_scenarios.csv",
                "zerodha_model_version": ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
                "documented_formula_or_proxy_basis": formula or "Phase 12 cost schedule component",
                "documented_source_url": source_url,
                "representative_scenarios_available": scenario_count,
                "broker_contract_note_field_required": broker_field,
                "broker_contract_note_available_now": False,
                "proxy_formula_available_now": bool(proxy_available),
                "actual_fill_available_now": False,
                "reconciliation_status": "proxy_formula_ready_broker_contract_note_missing" if proxy_available else "proxy_formula_missing_broker_contract_note_missing",
                "acceptance_eligible_now": False,
                "blocker": "Broker contract-note row and broker/exchange fill identifiers are required before economic acceptance.",
            }
        )

    fill_items = [
        ("exchange_order_id", "not_available_in_proxy", "contract_note_or_orderbook_exchange_order_id"),
        ("exchange_trade_id", "not_available_in_proxy", "contract_note_trade_id"),
        ("executed_quantity", "simulated_trade_quantity_proxy", "broker_fill_quantity"),
        ("executed_price", "simulated_entry_exit_mid_price_proxy", "broker_fill_price"),
        ("contract_note_number", "not_available_in_proxy", "contract_note_number"),
        ("settlement_obligation", "simulated_net_pnl_after_formula_charges", "contract_note_net_obligation"),
    ]
    for item, proxy_field, broker_field in fill_items:
        rows.append(
            {
                "reconciliation_domain": "fills_and_contract_note",
                "reconciliation_item": item,
                "proxy_field_or_artifact": proxy_field,
                "proxy_evidence": "outputs/phase12/execution_summary.csv; outputs/phase12/trade_ledger_sample.parquet",
                "zerodha_model_version": ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
                "documented_formula_or_proxy_basis": "Simulated marketable-order proxy field; broker-confirmed source is not present.",
                "documented_source_url": "",
                "representative_scenarios_available": scenario_count,
                "broker_contract_note_field_required": broker_field,
                "broker_contract_note_available_now": False,
                "proxy_formula_available_now": item in {"executed_quantity", "executed_price", "settlement_obligation"},
                "actual_fill_available_now": False,
                "reconciliation_status": "broker_fill_or_contract_note_missing",
                "acceptance_eligible_now": False,
                "blocker": "Actual broker/exchange fills and contract-note identifiers are required before economic acceptance.",
            }
        )
    return pd.DataFrame(rows).sort_values(["reconciliation_domain", "reconciliation_item"], kind="mergesort")


def economic_reconciliation_strategy_summary(
    economic_frontier: pd.DataFrame,
    risk_adjusted_frontier: pd.DataFrame,
    readiness_ledger: pd.DataFrame,
    acceptance_summary: pd.DataFrame,
) -> pd.DataFrame:
    broker_ready = bool(readiness_ledger["broker_contract_note_available_now"].all()) if len(readiness_ledger) else False
    charge_rows = readiness_ledger[readiness_ledger["reconciliation_domain"].astype(str) == "charges"]
    formula_ready = bool(charge_rows["proxy_formula_available_now"].all()) if len(charge_rows) else False
    missing_items = int((~readiness_ledger["broker_contract_note_available_now"].astype(bool)).sum()) if len(readiness_ledger) else 0
    rows = []
    for record in acceptance_summary.sort_values("strategy_id").to_dict("records"):
        strategy_id = record["strategy_id"]
        group = economic_frontier[economic_frontier["strategy_id"].astype(str) == str(strategy_id)]
        risk_group = risk_adjusted_frontier[risk_adjusted_frontier["strategy_id"].astype(str) == str(strategy_id)]
        retail_stress = group[group["retail_or_stress_profile"].astype(bool)]
        rows.append(
            {
                "strategy_id": strategy_id,
                "acceptance_status": record.get("acceptance_status", ""),
                "economic_frontier_rows": int(len(group)),
                "retail_stress_rows": int(len(retail_stress)),
                "net_positive_proxy_rows": int(group["net_positive_proxy"].astype(bool).sum()),
                "retail_stress_net_positive_proxy_rows": int(retail_stress["net_positive_proxy"].astype(bool).sum()) if len(retail_stress) else 0,
                "risk_adjusted_joint_pass_rows": int(risk_group["net_positive_and_risk_pass_proxy"].astype(bool).sum()) if len(risk_group) else 0,
                "documented_zerodha_formula_ready": formula_ready,
                "broker_contract_note_reconciliation_ready": broker_ready,
                "missing_reconciliation_items": missing_items,
                "economic_acceptance_ready_now": False,
                "readiness_status": "blocked_broker_contract_note_and_actual_fill_reconciliation_missing",
                "required_next_evidence": "Broker contract-note rows and broker/exchange fill records reconciled to Phase 12 order-formula charge components and net P&L.",
            }
        )
    return pd.DataFrame(rows)


def economic_acceptance_gap_ledger(
    economic_frontier: pd.DataFrame,
    risk_adjusted_frontier: pd.DataFrame,
    broker_readiness: pd.DataFrame,
    economic_reconciliation: pd.DataFrame,
    acceptance_summary: pd.DataFrame,
) -> pd.DataFrame:
    columns = [
        "strategy_id",
        "economic_requirement",
        "required_threshold",
        "observed_value",
        "current_evidence_status",
        "proxy_evidence_available",
        "acceptance_requirement_met",
        "blocking_gap",
        "evidence_source",
        "required_next_evidence",
        "acceptance_eligible_now",
    ]
    evidence_source = (
        "outputs/phase12/execution_summary.csv; outputs/phase12/cost_schedule.csv; "
        "outputs/phase16/economic_viability_frontier.csv; outputs/phase16/risk_adjusted_economic_frontier.csv; "
        "outputs/phase16/broker_reconciliation_readiness.csv; outputs/phase16/economic_reconciliation_strategy_summary.csv"
    )
    rows: list[dict] = []
    charge_rows = broker_readiness[broker_readiness["reconciliation_domain"].astype(str) == "charges"]
    formula_ready = bool(charge_rows["proxy_formula_available_now"].astype(bool).all()) if len(charge_rows) else False
    broker_contract_ready = bool(broker_readiness["broker_contract_note_available_now"].astype(bool).all()) if len(broker_readiness) else False
    actual_fill_ready = bool(broker_readiness["actual_fill_available_now"].astype(bool).all()) if len(broker_readiness) else False
    missing_reconciliation_items = int((~broker_readiness["broker_contract_note_available_now"].astype(bool)).sum()) if len(broker_readiness) else 0

    for record in acceptance_summary.sort_values("strategy_id").to_dict("records"):
        strategy_id = str(record["strategy_id"])
        frontier = economic_frontier[economic_frontier["strategy_id"].astype(str) == strategy_id]
        risk_frontier = risk_adjusted_frontier[risk_adjusted_frontier["strategy_id"].astype(str) == strategy_id]
        reconciliation = economic_reconciliation[economic_reconciliation["strategy_id"].astype(str) == strategy_id]
        retail_stress = frontier[frontier["retail_or_stress_profile"].astype(bool)] if len(frontier) else pd.DataFrame()
        stressed = frontier[frontier["execution_profile"].astype(str) == "stressed_retail"] if len(frontier) else pd.DataFrame()
        retail_stress_positive = int(retail_stress["net_positive_proxy"].astype(bool).sum()) if len(retail_stress) else 0
        stressed_positive = int(stressed["net_positive_proxy"].astype(bool).sum()) if len(stressed) else 0
        joint_pass = int(risk_frontier["net_positive_and_risk_pass_proxy"].astype(bool).sum()) if len(risk_frontier) else 0
        retail_stress_joint_pass = (
            int(risk_frontier["retail_stress_net_positive_and_risk_pass_proxy"].astype(bool).sum())
            if len(risk_frontier)
            else 0
        )
        profiles_present = sorted(set(map(str, frontier["execution_profile"].dropna().unique()))) if len(frontier) else []
        reconciliation_ready = (
            bool(reconciliation["economic_acceptance_ready_now"].astype(bool).all())
            if len(reconciliation)
            else False
        )

        def add(
            economic_requirement: str,
            required_threshold: str,
            observed_value: str,
            current_evidence_status: str,
            proxy_evidence_available: bool,
            blocking_gap: str,
            required_next_evidence: str,
        ) -> None:
            rows.append(
                {
                    "strategy_id": strategy_id,
                    "economic_requirement": economic_requirement,
                    "required_threshold": required_threshold,
                    "observed_value": observed_value,
                    "current_evidence_status": current_evidence_status,
                    "proxy_evidence_available": bool(proxy_evidence_available),
                    "acceptance_requirement_met": False,
                    "blocking_gap": blocking_gap,
                    "evidence_source": evidence_source,
                    "required_next_evidence": required_next_evidence,
                    "acceptance_eligible_now": False,
                }
            )

        add(
            "retail_and_stress_net_positive",
            "net-positive after costs in retail and stressed deployable profiles",
            f"{retail_stress_positive}/2 retail/stress profile rows net-positive",
            "proxy_frontier_available_not_acceptance" if len(retail_stress) else "missing_retail_stress_proxy_rows",
            bool(len(retail_stress) == 2),
            "Current proxy does not prove persistent positive economics after realistic costs, slippage and latency.",
            "Run acceptance-grade event/tick P&L with deployable retail and stressed profiles, then require positive net results.",
        )
        add(
            "stressed_profile_net_positive",
            "stressed retail profile net-positive after all costs",
            f"{stressed_positive}/1 stressed profile rows net-positive",
            "proxy_stress_row_available_not_acceptance" if len(stressed) else "missing_stressed_profile_proxy_row",
            bool(len(stressed)),
            "Stressed-profile economics are proxy-only and may be nonpositive.",
            "Require stressed-profile net profitability under acceptance fills, costs and latency.",
        )
        add(
            "risk_adjusted_economic_joint_pass",
            "net-positive economics jointly clears lifecycle risk-pass criteria",
            f"{joint_pass} all-profile joint-pass rows; {retail_stress_joint_pass} retail/stress joint-pass rows",
            "risk_adjusted_proxy_available_not_acceptance" if len(risk_frontier) else "missing_risk_adjusted_frontier",
            bool(len(risk_frontier)),
            "Risk-adjusted frontier is proxy-only and currently has no retail/stress joint pass.",
            "Join acceptance-grade economic P&L to acceptance-grade risk state and require joint pass.",
        )
        add(
            "zerodha_order_formula_ready",
            "documented Zerodha equity-intraday charge formulas applied to P&L proxy",
            f"formula_ready={formula_ready}",
            "zerodha_formula_proxy_ready_not_acceptance" if formula_ready else "zerodha_formula_missing",
            formula_ready,
            "Documented formulas exist, but formula evidence alone is not broker reconciliation.",
            "Retain Zerodha formula evidence and reconcile charges against broker contract notes where available.",
        )
        add(
            "broker_exchange_fill_provenance",
            "actual broker/exchange order and fill identifiers available and reconciled",
            f"actual_fill_ready={actual_fill_ready}",
            "missing_actual_fill_provenance",
            False,
            "No actual broker/exchange fill identifiers, prices or quantities are present in current proxy evidence.",
            "Capture/import broker order/fill records and map them to strategy decisions and lifecycle state.",
        )
        add(
            "contract_note_reconciliation",
            "broker contract-note charges and net obligation reconcile to strategy P&L",
            f"broker_contract_ready={broker_contract_ready}; missing_items={missing_reconciliation_items}; strategy_ready={reconciliation_ready}",
            "proxy_formula_ready_contract_note_missing" if formula_ready else "contract_note_and_formula_missing",
            formula_ready,
            "Contract-note fields are missing, so realized cost/P&L reconciliation is not acceptance-grade.",
            "Reconcile brokerage, STT, exchange transaction charge, SEBI charge, stamp duty, GST and net obligation to broker notes.",
        )
        add(
            "latency_slippage_stress_confirmation",
            "retail and stressed latency/slippage profiles evaluated and economically viable",
            f"profiles_present={';'.join(profiles_present) if profiles_present else 'none'}; retail_stress_positive={retail_stress_positive}/2",
            "latency_slippage_proxy_profiles_available_not_acceptance" if len(frontier) else "missing_latency_slippage_profiles",
            bool({"retail_marketable_default", "stressed_retail"}.issubset(set(profiles_present))),
            "Latency and slippage stress exists as Phase 12 proxy settings, not acceptance-grade execution evidence.",
            "Run tick/event lifecycle execution with calibrated retail latency, slippage stress and cancel/reject behavior.",
        )
        add(
            "multi_day_real_or_holdout_economic_validation",
            "positive economics survive multi-day real-data or untouched holdout-generator reruns",
            "not available in current one-day/proxy evidence",
            "missing_multi_day_real_or_holdout_economic_validation",
            False,
            "Current economic evidence is synthetic/proxy and does not include multi-day real or untouched economic holdout validation.",
            "Run economic validation on multi-day real data and/or untouched holdout-generator configurations before promotion.",
        )

    return pd.DataFrame(rows, columns=columns).sort_values(["strategy_id", "economic_requirement"], kind="mergesort")


def breakdown_coverage(inputs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    sample_cols = set(inputs["trade_sample"].columns)
    rows = []
    for breakdown_name, source_column, status in BREAKDOWNS:
        rows.append(
            {
                "breakdown_name": breakdown_name,
                "source_column": source_column,
                "current_status": status if source_column in sample_cols else "missing",
                "available_in_trade_sample": source_column in sample_cols,
                "distinct_values_in_sample": int(inputs["trade_sample"][source_column].nunique()) if source_column in sample_cols else 0,
            }
        )
    return pd.DataFrame(rows)


def metric_requirement_coverage(inputs: dict[str, pd.DataFrame], catalog: pd.DataFrame) -> pd.DataFrame:
    req = inputs["metric_requirements"].copy()
    status_map = dict(zip(catalog["metric_name"], catalog["current_status"]))
    req["phase16_mapped_metric_name"] = req["primary_metric"].map(lambda value: METRIC_ALIASES.get(str(value), str(value)))
    req["phase16_current_status"] = req["phase16_mapped_metric_name"].map(status_map).fillna("strategy_specific_missing_or_not_mapped")
    req["phase16_acceptance_ready"] = False
    return req


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


def write_report(
    output_dir: Path,
    catalog: pd.DataFrame,
    predictive: pd.DataFrame,
    predictive_proxy: pd.DataFrame,
    signal_buckets: pd.DataFrame,
    brier: pd.DataFrame,
    calibration: pd.DataFrame,
    baseline_comparison: pd.DataFrame,
    holdout_stability_summary: pd.DataFrame,
    importance: pd.DataFrame,
    predictive_falsification: pd.DataFrame,
    predictive_gap: pd.DataFrame,
    trading: pd.DataFrame,
    economic_frontier: pd.DataFrame,
    risk_adjusted_frontier: pd.DataFrame,
    broker_reconciliation: pd.DataFrame,
    economic_reconciliation: pd.DataFrame,
    economic_gap: pd.DataFrame,
    breakdowns: pd.DataFrame,
) -> None:
    catalog_summary = catalog.groupby(["metric_category", "current_status"], sort=True).size().reset_index(name="metrics")
    breakdown_summary = breakdowns.groupby("current_status", sort=True).size().reset_index(name="breakdowns")
    predictive_gap_summary = (
        predictive_gap.groupby(["predictive_requirement", "proxy_evidence_available", "acceptance_requirement_met"], sort=True)
        .size()
        .reset_index(name="rows")
        if len(predictive_gap)
        else pd.DataFrame(columns=["predictive_requirement", "proxy_evidence_available", "acceptance_requirement_met", "rows"])
    )
    economic_gap_summary = (
        economic_gap.groupby(["economic_requirement", "proxy_evidence_available", "acceptance_requirement_met"], sort=True)
        .size()
        .reset_index(name="rows")
        if len(economic_gap)
        else pd.DataFrame(columns=["economic_requirement", "proxy_evidence_available", "acceptance_requirement_met", "rows"])
    )
    lines = [
        "# Phase 16 Metrics and Reporting Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase creates a metrics catalog and current-evidence scoreboards for Phase 11 predictive diagnostics and Phase 12 trading proxies.",
        "No metric is acceptance-grade yet; current values are proxy/reporting evidence only.",
        "",
        "## Metric Catalog Summary",
        "",
        _markdown_table(catalog_summary),
        "",
        "## Top Predictive Proxy Rows",
        "",
        _markdown_table(predictive.sort_values("directional_accuracy_nonzero", ascending=False).head(10)),
        "",
        "## Predictive Confusion / Rank Proxy Rows",
        "",
        _markdown_table(predictive_proxy.sort_values("balanced_accuracy_proxy", ascending=False).head(10)),
        "",
        "## Signal Bucket Future Returns",
        "",
        _markdown_table(signal_buckets.head(30)),
        "",
        "## Brier Score Proxy",
        "",
        _markdown_table(brier.sort_values("brier_score_proxy", ascending=True).head(12)),
        "",
        "## Calibration Curve Proxy",
        "",
        _markdown_table(calibration.head(30)),
        "",
        "## Predictive Baseline Comparison",
        "",
        _markdown_table(baseline_comparison.sort_values("directional_accuracy_excess_vs_majority", ascending=False).head(12)),
        "",
        "## Predictive Holdout Stability Summary",
        "",
        _markdown_table(holdout_stability_summary.sort_values("cell_beat_fraction", ascending=False).head(12)),
        "",
        "## Feature Importance Stability Proxy",
        "",
        _markdown_table(importance.head(12)),
        "",
        "## Predictive Promotion Falsification",
        "",
        _markdown_table(predictive_falsification),
        "",
        "## Predictive Acceptance Gap Ledger",
        "",
        _markdown_table(predictive_gap_summary),
        "",
        _markdown_table(predictive_gap),
        "",
        "## Top Trading Proxy Rows",
        "",
        _markdown_table(trading.sort_values("mean_net_return", ascending=False).head(10)),
        "",
        "## Economic Viability Frontier",
        "",
        _markdown_table(economic_frontier.sort_values("net_edge_bps", ascending=False).head(18)),
        "",
        "## Risk-Adjusted Economic Frontier",
        "",
        _markdown_table(risk_adjusted_frontier.sort_values("risk_adjusted_net_edge_bps", ascending=False).head(18)),
        "",
        "## Broker Contract-Note Reconciliation Readiness",
        "",
        _markdown_table(broker_reconciliation),
        "",
        "## Economic Reconciliation Strategy Readiness",
        "",
        _markdown_table(economic_reconciliation),
        "",
        "## Economic Acceptance Gap Ledger",
        "",
        _markdown_table(economic_gap_summary),
        "",
        _markdown_table(economic_gap),
        "",
        "## Required Breakdown Coverage",
        "",
        _markdown_table(breakdown_summary),
        "",
        _markdown_table(breakdowns),
        "",
    ]
    (output_dir / "phase16_metrics_reporting_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase16(output_dir: Path, paths: dict[str, Path]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    inputs = load_inputs(paths)
    catalog = metric_catalog()
    predictive = predictive_scoreboard(inputs)
    predictive_proxy, signal_buckets = predictive_proxy_diagnostics(inputs)
    brier, calibration = predictive_calibration_proxies(inputs)
    baseline_comparison = predictive_baseline_comparison(predictive, predictive_proxy, brier)
    holdout_stability, holdout_stability_summary = predictive_holdout_stability(inputs)
    importance = feature_importance_stability(inputs)
    predictive_falsification = predictive_promotion_falsification(
        baseline_comparison,
        holdout_stability_summary,
        importance,
        inputs["acceptance_summary"],
    )
    predictive_gap = predictive_acceptance_gap_ledger(
        baseline_comparison,
        holdout_stability_summary,
        importance,
        predictive_falsification,
        inputs["acceptance_summary"],
    )
    markouts = markout_analysis(inputs["trade_sample"])
    inputs["markout_analysis"] = markouts
    trading = trading_scoreboard(inputs)
    economic_frontier = economic_viability_frontier(inputs)
    risk_adjusted_frontier = risk_adjusted_economic_frontier(economic_frontier, inputs)
    broker_reconciliation = broker_reconciliation_readiness_ledger(inputs)
    economic_reconciliation = economic_reconciliation_strategy_summary(
        economic_frontier,
        risk_adjusted_frontier,
        broker_reconciliation,
        inputs["acceptance_summary"],
    )
    economic_gap = economic_acceptance_gap_ledger(
        economic_frontier,
        risk_adjusted_frontier,
        broker_reconciliation,
        economic_reconciliation,
        inputs["acceptance_summary"],
    )
    breakdowns = breakdown_coverage(inputs)
    requirement_coverage = metric_requirement_coverage(inputs, catalog)

    catalog.to_csv(output_dir / "metric_catalog.csv", index=False)
    predictive.to_csv(output_dir / "predictive_metric_scoreboard.csv", index=False)
    predictive_proxy.to_csv(output_dir / "predictive_proxy_diagnostics.csv", index=False)
    signal_buckets.to_csv(output_dir / "predictive_signal_bucket_returns.csv", index=False)
    brier.to_csv(output_dir / "predictive_brier_score_proxy.csv", index=False)
    calibration.to_csv(output_dir / "predictive_calibration_curve_proxy.csv", index=False)
    baseline_comparison.to_csv(output_dir / "predictive_baseline_comparison.csv", index=False)
    holdout_stability.to_csv(output_dir / "predictive_holdout_stability.csv", index=False)
    holdout_stability_summary.to_csv(output_dir / "predictive_holdout_stability_summary.csv", index=False)
    importance.to_csv(output_dir / "feature_importance_stability_proxy.csv", index=False)
    predictive_falsification.to_csv(output_dir / "predictive_promotion_falsification.csv", index=False)
    predictive_gap.to_csv(output_dir / "predictive_acceptance_gap_ledger.csv", index=False)
    trading.to_csv(output_dir / "trading_metric_scoreboard.csv", index=False)
    economic_frontier.to_csv(output_dir / "economic_viability_frontier.csv", index=False)
    risk_adjusted_frontier.to_csv(output_dir / "risk_adjusted_economic_frontier.csv", index=False)
    broker_reconciliation.to_csv(output_dir / "broker_reconciliation_readiness.csv", index=False)
    economic_reconciliation.to_csv(output_dir / "economic_reconciliation_strategy_summary.csv", index=False)
    economic_gap.to_csv(output_dir / "economic_acceptance_gap_ledger.csv", index=False)
    markouts.to_csv(output_dir / "markout_mae_mfe_summary.csv", index=False)
    breakdowns.to_csv(output_dir / "breakdown_coverage.csv", index=False)
    requirement_coverage.to_csv(output_dir / "strategy_metric_requirement_coverage.csv", index=False)
    generated_utc = datetime.now(timezone.utc).isoformat()
    inputs_manifest = {key: str(value) for key, value in paths.items()}
    manifest = {
        "generated_utc": generated_utc,
        "inputs": inputs_manifest,
        "metric_catalog_rows": int(len(catalog)),
        "predictive_scoreboard_rows": int(len(predictive)),
        "predictive_proxy_rows": int(len(predictive_proxy)),
        "predictive_signal_bucket_rows": int(len(signal_buckets)),
        "predictive_brier_score_rows": int(len(brier)),
        "predictive_calibration_curve_rows": int(len(calibration)),
        "predictive_baseline_comparison_rows": int(len(baseline_comparison)),
        "predictive_holdout_stability_rows": int(len(holdout_stability)),
        "predictive_holdout_stability_summary_rows": int(len(holdout_stability_summary)),
        "predictive_holdout_stability_all_cell_pass_rows": int(
            (holdout_stability_summary["worst_segment_status"].astype(str) == "all_cells_beat_local_majority_proxy").sum()
        ) if len(holdout_stability_summary) else 0,
        "predictive_baseline_beating_rows": int(
            (
                baseline_comparison["predictive_baseline_status"].astype(str)
                == "beats_proxy_baselines_not_acceptance"
            ).sum()
        ),
        "feature_importance_stability_rows": int(len(importance)),
        "predictive_promotion_falsification_rows": int(len(predictive_falsification)),
        "predictive_promotion_candidate_proxy_rows": int(predictive_falsification["predictive_promotion_candidate_proxy"].astype(bool).sum()) if len(predictive_falsification) else 0,
        "predictive_promotion_falsified_rows": int((predictive_falsification["falsification_status"].astype(str) == "falsified_for_predictive_promotion_under_current_proxy_evidence").sum()) if len(predictive_falsification) else 0,
        "predictive_acceptance_gap_rows": int(len(predictive_gap)),
        "predictive_acceptance_gap_open_rows": int((~predictive_gap["acceptance_requirement_met"].astype(bool)).sum()) if len(predictive_gap) else 0,
        "predictive_acceptance_gap_proxy_available_rows": int(predictive_gap["proxy_evidence_available"].astype(bool).sum()) if len(predictive_gap) else 0,
        "predictive_acceptance_gap_met_rows": int(predictive_gap["acceptance_requirement_met"].astype(bool).sum()) if len(predictive_gap) else 0,
        "trading_scoreboard_rows": int(len(trading)),
        "economic_viability_frontier_rows": int(len(economic_frontier)),
        "economic_viability_net_positive_rows": int(economic_frontier["net_positive_proxy"].sum()) if len(economic_frontier) else 0,
        "economic_viability_retail_stress_net_positive_rows": int(
            (economic_frontier["net_positive_proxy"] & economic_frontier["retail_or_stress_profile"]).sum()
        ) if "retail_or_stress_profile" in economic_frontier else 0,
        "risk_adjusted_economic_frontier_rows": int(len(risk_adjusted_frontier)),
        "risk_adjusted_economic_joint_pass_rows": int(risk_adjusted_frontier["net_positive_and_risk_pass_proxy"].sum()) if len(risk_adjusted_frontier) else 0,
        "risk_adjusted_economic_retail_stress_joint_pass_rows": int(risk_adjusted_frontier["retail_stress_net_positive_and_risk_pass_proxy"].sum()) if len(risk_adjusted_frontier) else 0,
        "risk_adjusted_economic_risk_blocked_positive_rows": int((risk_adjusted_frontier["risk_adjusted_frontier_status"].astype(str) == "economic_positive_but_risk_blocked_proxy").sum()) if len(risk_adjusted_frontier) else 0,
        "broker_reconciliation_readiness_rows": int(len(broker_reconciliation)),
        "broker_reconciliation_proxy_formula_ready_rows": int(broker_reconciliation["proxy_formula_available_now"].astype(bool).sum()) if len(broker_reconciliation) else 0,
        "broker_reconciliation_contract_note_ready_rows": int(broker_reconciliation["broker_contract_note_available_now"].astype(bool).sum()) if len(broker_reconciliation) else 0,
        "economic_reconciliation_strategy_rows": int(len(economic_reconciliation)),
        "economic_reconciliation_ready_strategies": int(economic_reconciliation["economic_acceptance_ready_now"].astype(bool).sum()) if len(economic_reconciliation) else 0,
        "economic_acceptance_gap_rows": int(len(economic_gap)),
        "economic_acceptance_gap_open_rows": int((~economic_gap["acceptance_requirement_met"].astype(bool)).sum()) if len(economic_gap) else 0,
        "economic_acceptance_gap_proxy_available_rows": int(economic_gap["proxy_evidence_available"].astype(bool).sum()) if len(economic_gap) else 0,
        "economic_acceptance_gap_met_rows": int(economic_gap["acceptance_requirement_met"].astype(bool).sum()) if len(economic_gap) else 0,
        "markout_summary_rows": int(len(markouts)),
        "markout_horizons_bars": [1, 3, 6],
        "breakdown_rows": int(len(breakdowns)),
        "acceptance_grade_metrics": int(catalog["acceptance_eligible_now"].sum()),
        "scope": "metrics_reporting_catalog_and_proxy_scoreboards",
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase16",
            generated_utc=generated_utc,
            inputs=inputs_manifest,
            parameters={
                "predictive_metric_count": len(PREDICTIVE_METRICS),
                "trading_metric_count": len(TRADING_METRICS),
                "breakdown_count": len(BREAKDOWNS),
                "markout_horizons_bars": [1, 3, 6],
            },
            outputs={
                "metric_catalog": str(output_dir / "metric_catalog.csv"),
                "predictive_metric_scoreboard": str(output_dir / "predictive_metric_scoreboard.csv"),
                "predictive_baseline_comparison": str(output_dir / "predictive_baseline_comparison.csv"),
                "predictive_holdout_stability": str(output_dir / "predictive_holdout_stability.csv"),
                "predictive_holdout_stability_summary": str(output_dir / "predictive_holdout_stability_summary.csv"),
                "predictive_promotion_falsification": str(output_dir / "predictive_promotion_falsification.csv"),
                "predictive_acceptance_gap_ledger": str(output_dir / "predictive_acceptance_gap_ledger.csv"),
                "trading_metric_scoreboard": str(output_dir / "trading_metric_scoreboard.csv"),
                "economic_viability_frontier": str(output_dir / "economic_viability_frontier.csv"),
                "risk_adjusted_economic_frontier": str(output_dir / "risk_adjusted_economic_frontier.csv"),
                "broker_reconciliation_readiness": str(output_dir / "broker_reconciliation_readiness.csv"),
                "economic_reconciliation_strategy_summary": str(output_dir / "economic_reconciliation_strategy_summary.csv"),
                "economic_acceptance_gap_ledger": str(output_dir / "economic_acceptance_gap_ledger.csv"),
                "breakdown_coverage": str(output_dir / "breakdown_coverage.csv"),
                "strategy_metric_requirement_coverage": str(output_dir / "strategy_metric_requirement_coverage.csv"),
                "report": str(output_dir / "phase16_metrics_reporting_report.md"),
            },
            random_seed="outputs/phase13/seed_plan.csv",
            scenario_ids="phase11_strategy_metric_requirements_and_phase12_seeded_trade_sample",
            cost_model_version="outputs/phase12/cost_schedule.csv_and_zerodha_order_formula_v2",
            latency_model_version="outputs/phase12/execution_profiles.csv",
        )
    )
    (output_dir / "metrics_reporting_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(
        output_dir,
        catalog,
        predictive,
        predictive_proxy,
        signal_buckets,
        brier,
        calibration,
        baseline_comparison,
        holdout_stability_summary,
        importance,
        predictive_falsification,
        predictive_gap,
        trading,
        economic_frontier,
        risk_adjusted_frontier,
        broker_reconciliation,
        economic_reconciliation,
        economic_gap,
        breakdowns,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 16 metrics/reporting artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase16"))
    parser.add_argument("--signal-diagnostics", type=Path, default=Path("outputs/phase11/strategy_signal_diagnostics.csv"))
    parser.add_argument("--metric-requirements", type=Path, default=Path("outputs/phase11/strategy_metric_requirements.csv"))
    parser.add_argument("--execution-summary", type=Path, default=Path("outputs/phase12/execution_summary.csv"))
    parser.add_argument("--trade-sample", type=Path, default=Path("outputs/phase12/trade_ledger_sample.parquet"))
    parser.add_argument("--risk-breach-severity", type=Path, default=Path("outputs/phase12/full_run_lifecycle_risk_breach_severity.csv"))
    parser.add_argument("--cost-schedule", type=Path, default=Path("outputs/phase12/cost_schedule.csv"))
    parser.add_argument("--charge-component-catalog", type=Path, default=Path("outputs/phase12/charge_component_catalog.csv"))
    parser.add_argument("--representative-charge-scenarios", type=Path, default=Path("outputs/phase12/representative_charge_scenarios.csv"))
    parser.add_argument("--features", type=Path, default=Path("outputs/phase9/tier_c/features_5m.parquet"))
    parser.add_argument("--acceptance-summary", type=Path, default=Path("outputs/phase15/strategy_acceptance_summary.csv"))
    parser.add_argument("--seed-plan", type=Path, default=Path("outputs/phase13/seed_plan.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "signal_diagnostics": args.signal_diagnostics,
        "metric_requirements": args.metric_requirements,
        "execution_summary": args.execution_summary,
        "trade_sample": args.trade_sample,
        "risk_breach_severity": args.risk_breach_severity,
        "cost_schedule": args.cost_schedule,
        "charge_component_catalog": args.charge_component_catalog,
        "representative_charge_scenarios": args.representative_charge_scenarios,
        "features": args.features,
        "acceptance_summary": args.acceptance_summary,
        "seed_plan": args.seed_plan,
    }
    run_phase16(args.output_dir, paths)


if __name__ == "__main__":
    main()
