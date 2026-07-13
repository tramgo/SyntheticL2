from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from synthetic_l2.phase11_strategy_validation_matrix import build_signals, load_features


PREDICTIVE_METRICS = [
    ("directional_accuracy", "computed_proxy", "phase11_signal_diagnostics.directional_accuracy_nonzero"),
    ("balanced_accuracy", "sample_proxy", "Computed from Phase 11 ternary proxy signal confusion by direction."),
    ("precision_recall_by_direction", "sample_proxy", "Computed from Phase 11 ternary proxy signal confusion by long/short direction."),
    ("roc_auc", "sample_proxy", "Rank-AUC proxy computed from ternary signal score; not a calibrated probabilistic ROC."),
    ("brier_score", "sample_proxy", "Computed from deterministic ternary-signal pseudo-probabilities; not a calibrated probability model."),
    ("calibration_curve", "sample_proxy", "Computed from deterministic ternary-signal probability buckets and realized up/down frequency."),
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
    ("turnover", "proxy_available", "Trade count is available; capital-normalized turnover is not."),
    ("cost_to_gross_profit_ratio", "sample_proxy", "Computed from sampled trade ledger."),
    ("fill_ratio", "sample_proxy", "Phase 12 order-lifecycle proxy provides submitted and filled quantities over the sampled trade ledger."),
    ("adverse_selection", "sample_proxy", "Computed from sampled post-fill markout windows over the Phase 12 trade ledger."),
    ("mae_mfe", "sample_proxy", "Computed from sampled 1/3/6-bar post-entry markout path over the Phase 12 trade ledger."),
    ("exposure_holding_time", "sample_proxy", "Phase 12 order-lifecycle proxy provides running position exposure; holding-time lifecycle remains approximate."),
]

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
    ("random_seed", "seed", "missing"),
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
    "regime_stability": "strategy_specific_missing_or_not_mapped",
    "regime_aware_vs_unaware_uplift": "strategy_specific_missing_or_not_mapped",
    "miss_rate": "fill_ratio",
    "trade_reduction": "turnover",
}


def load_inputs(paths: dict[str, Path]) -> dict[str, pd.DataFrame]:
    return {
        "signal_diagnostics": pd.read_csv(paths["signal_diagnostics"]),
        "metric_requirements": pd.read_csv(paths["metric_requirements"]),
        "execution_summary": pd.read_csv(paths["execution_summary"]),
        "trade_sample": pd.read_parquet(paths["trade_sample"]),
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
    importance: pd.DataFrame,
    trading: pd.DataFrame,
    breakdowns: pd.DataFrame,
) -> None:
    catalog_summary = catalog.groupby(["metric_category", "current_status"], sort=True).size().reset_index(name="metrics")
    breakdown_summary = breakdowns.groupby("current_status", sort=True).size().reset_index(name="breakdowns")
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
        "## Feature Importance Stability Proxy",
        "",
        _markdown_table(importance.head(12)),
        "",
        "## Top Trading Proxy Rows",
        "",
        _markdown_table(trading.sort_values("mean_net_return", ascending=False).head(10)),
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
    importance = feature_importance_stability(inputs)
    markouts = markout_analysis(inputs["trade_sample"])
    inputs["markout_analysis"] = markouts
    trading = trading_scoreboard(inputs)
    breakdowns = breakdown_coverage(inputs)
    requirement_coverage = metric_requirement_coverage(inputs, catalog)

    catalog.to_csv(output_dir / "metric_catalog.csv", index=False)
    predictive.to_csv(output_dir / "predictive_metric_scoreboard.csv", index=False)
    predictive_proxy.to_csv(output_dir / "predictive_proxy_diagnostics.csv", index=False)
    signal_buckets.to_csv(output_dir / "predictive_signal_bucket_returns.csv", index=False)
    brier.to_csv(output_dir / "predictive_brier_score_proxy.csv", index=False)
    calibration.to_csv(output_dir / "predictive_calibration_curve_proxy.csv", index=False)
    importance.to_csv(output_dir / "feature_importance_stability_proxy.csv", index=False)
    trading.to_csv(output_dir / "trading_metric_scoreboard.csv", index=False)
    markouts.to_csv(output_dir / "markout_mae_mfe_summary.csv", index=False)
    breakdowns.to_csv(output_dir / "breakdown_coverage.csv", index=False)
    requirement_coverage.to_csv(output_dir / "strategy_metric_requirement_coverage.csv", index=False)
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {key: str(value) for key, value in paths.items()},
        "metric_catalog_rows": int(len(catalog)),
        "predictive_scoreboard_rows": int(len(predictive)),
        "predictive_proxy_rows": int(len(predictive_proxy)),
        "predictive_signal_bucket_rows": int(len(signal_buckets)),
        "predictive_brier_score_rows": int(len(brier)),
        "predictive_calibration_curve_rows": int(len(calibration)),
        "feature_importance_stability_rows": int(len(importance)),
        "trading_scoreboard_rows": int(len(trading)),
        "markout_summary_rows": int(len(markouts)),
        "markout_horizons_bars": [1, 3, 6],
        "breakdown_rows": int(len(breakdowns)),
        "acceptance_grade_metrics": int(catalog["acceptance_eligible_now"].sum()),
        "scope": "metrics_reporting_catalog_and_proxy_scoreboards",
    }
    (output_dir / "metrics_reporting_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, catalog, predictive, predictive_proxy, signal_buckets, brier, calibration, importance, trading, breakdowns)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 16 metrics/reporting artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase16"))
    parser.add_argument("--signal-diagnostics", type=Path, default=Path("outputs/phase11/strategy_signal_diagnostics.csv"))
    parser.add_argument("--metric-requirements", type=Path, default=Path("outputs/phase11/strategy_metric_requirements.csv"))
    parser.add_argument("--execution-summary", type=Path, default=Path("outputs/phase12/execution_summary.csv"))
    parser.add_argument("--trade-sample", type=Path, default=Path("outputs/phase12/trade_ledger_sample.parquet"))
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
        "features": args.features,
        "acceptance_summary": args.acceptance_summary,
        "seed_plan": args.seed_plan,
    }
    run_phase16(args.output_dir, paths)


if __name__ == "__main__":
    main()
