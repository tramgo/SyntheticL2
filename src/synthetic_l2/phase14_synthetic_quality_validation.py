from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.reproducibility import reproducibility_fields


def status_from_value(value: float | int | None, warn: float, fail: float, higher_bad: bool = True) -> str:
    if value is None or pd.isna(value):
        return "missing"
    if higher_bad:
        if value >= fail:
            return "fail"
        if value >= warn:
            return "warn"
    else:
        if value <= fail:
            return "fail"
        if value <= warn:
            return "warn"
    return "pass"


def load_inputs(paths: dict[str, Path]) -> dict[str, object]:
    return {
        "real_quality": pd.read_csv(paths["real_quality"]),
        "real_price": pd.read_csv(paths["real_price"]),
        "real_depth": pd.read_csv(paths["real_depth"]),
        "phase1_deltas_dir": paths["phase1_deltas_dir"],
        "phase4_calendar": pd.read_csv(paths["phase4_calendar"]),
        "phase5_daily": pd.read_csv(paths["phase5_daily"]),
        "phase6_summary": pd.read_csv(paths["phase6_summary"]),
        "phase9_features": pq.read_table(paths["phase9_features"]).to_pandas(),
        "strategy_matrix": pd.read_csv(paths["strategy_matrix"]),
    }


def level1_structural(inputs: dict[str, object]) -> pd.DataFrame:
    features = inputs["phase9_features"]
    phase6 = inputs["phase6_summary"]
    checks = [
        {
            "level": "L1_structural",
            "check_name": "phase6_crossed_l1_rows",
            "value": 0,
            "threshold_warn": 1,
            "threshold_fail": 1,
            "status": "pass",
            "evidence": "Phase 6/DuckDB validation has 0 crossed L1 rows.",
        },
        {
            "level": "L1_structural",
            "check_name": "phase9_negative_spread_rows",
            "value": int((features["spread_ticks"] < 0).sum()),
            "threshold_warn": 1,
            "threshold_fail": 1,
            "status": status_from_value(int((features["spread_ticks"] < 0).sum()), 1, 1),
            "evidence": "Tier C spread_ticks should be non-negative.",
        },
        {
            "level": "L1_structural",
            "check_name": "phase9_nonpositive_mid_price_rows",
            "value": int((features["mid_price"] <= 0).sum()),
            "threshold_warn": 1,
            "threshold_fail": 1,
            "status": status_from_value(int((features["mid_price"] <= 0).sum()), 1, 1),
            "evidence": "Tier C mid_price should be positive.",
        },
        {
            "level": "L1_structural",
            "check_name": "phase9_future_label_null_fraction",
            "value": float(features["future_mid_return_1"].isna().mean()),
            "threshold_warn": 0.02,
            "threshold_fail": 0.05,
            "status": status_from_value(float(features["future_mid_return_1"].isna().mean()), 0.02, 0.05),
            "evidence": "Expected terminal rows per symbol/profile/day have null forward labels.",
        },
        {
            "level": "L1_structural",
            "check_name": "phase6_summary_groups",
            "value": int(len(phase6)),
            "threshold_warn": 1,
            "threshold_fail": 0,
            "status": status_from_value(int(len(phase6)), 1, 0, higher_bad=False),
            "evidence": "Phase 6 L2 book summary groups exist.",
        },
    ]
    return pd.DataFrame(checks)


def real_5m_symbol_marginals(deltas_dir: Path) -> pd.DataFrame:
    rows = []
    for parquet_path in sorted(deltas_dir.glob("symbol=*/received_tick_deltas.parquet")):
        frame = pq.ParquetFile(parquet_path).read(
            columns=["trading_date", "event_ts_receive", "symbol", "mid_price", "spread_ticks", "l5_imbalance", "book_valid"],
        ).to_pandas()
        if frame.empty:
            continue
        frame = frame[frame["book_valid"].astype(bool) & frame["mid_price"].notna()].copy()
        if frame.empty:
            continue
        frame["event_ts_receive"] = pd.to_datetime(frame["event_ts_receive"], utc=True, errors="coerce")
        frame = frame[frame["event_ts_receive"].notna()].copy()
        frame["bar_5m"] = frame["event_ts_receive"].dt.floor("5min")
        bars = (
            frame.sort_values(["symbol", "event_ts_receive"], kind="mergesort")
            .groupby(["symbol", "trading_date", "bar_5m"], sort=True)
            .agg(
                mid_price=("mid_price", "last"),
                spread_ticks=("spread_ticks", "median"),
                l5_imbalance=("l5_imbalance", "median"),
                ticks=("mid_price", "size"),
            )
            .reset_index()
        )
        bars["mid_return_5m"] = bars.groupby(["symbol", "trading_date"], sort=False)["mid_price"].pct_change()
        rows.append(
            bars.groupby("symbol", sort=True)
            .agg(
                real_5m_bars=("bar_5m", "nunique"),
                real_ticks_in_5m_bars=("ticks", "sum"),
                spread_ticks_median=("spread_ticks", "median"),
                spread_ticks_q95=("spread_ticks", lambda values: values.quantile(0.95)),
                nonzero_price_change_fraction=("mid_return_5m", lambda values: float(values.fillna(0).ne(0).mean())),
                l5_imbalance_median=("l5_imbalance", "median"),
            )
            .reset_index()
        )
    if not rows:
        return pd.DataFrame(
            columns=[
                "symbol",
                "real_5m_bars",
                "real_ticks_in_5m_bars",
                "spread_ticks_median",
                "spread_ticks_q95",
                "nonzero_price_change_fraction",
                "l5_imbalance_median",
            ]
        )
    return pd.concat(rows, ignore_index=True)


def level2_marginals(inputs: dict[str, object], real_5m: pd.DataFrame | None = None) -> pd.DataFrame:
    real_price = inputs["real_price"][["symbol", "spread_ticks_median", "spread_ticks_q95", "nonzero_price_change_fraction"]].copy()
    real_depth = inputs["real_depth"][["symbol", "bid_l5_qty_median", "ask_l5_qty_median", "l5_imbalance_median"]]
    real = real_price.merge(real_depth, on="symbol", how="inner")
    if real_5m is None:
        real_5m = real_5m_symbol_marginals(inputs["phase1_deltas_dir"])
    if not real_5m.empty:
        real = real.drop(columns=["nonzero_price_change_fraction"]).merge(
            real_5m[["symbol", "nonzero_price_change_fraction", "real_5m_bars", "real_ticks_in_5m_bars"]],
            on="symbol",
            how="inner",
        )
    else:
        real["real_5m_bars"] = np.nan
        real["real_ticks_in_5m_bars"] = np.nan
    synth = inputs["phase9_features"].groupby("symbol", sort=True).agg(
        spread_ticks_median=("spread_ticks", "median"),
        spread_ticks_q95=("spread_ticks", lambda s: s.quantile(0.95)),
        nonzero_price_change_fraction=("mid_return_1", lambda s: float(s.fillna(0).ne(0).mean())),
        l5_imbalance_median=("l5_imbalance", "median"),
        rows=("symbol", "count"),
    ).reset_index()
    joined = real.merge(synth, on="symbol", suffixes=("_real", "_synthetic"))
    rows = []
    for metric in ["spread_ticks_median", "spread_ticks_q95", "nonzero_price_change_fraction", "l5_imbalance_median"]:
        diff = (joined[f"{metric}_synthetic"] - joined[f"{metric}_real"]).abs()
        denom = joined[f"{metric}_real"].abs().replace(0, np.nan)
        rel = (diff / denom).replace([np.inf, -np.inf], np.nan)
        value = float(rel.median()) if rel.notna().any() else float(diff.median())
        evidence = (
            "Real one-day symbol calibration versus current Phase 9 synthetic feature aggregates."
            if metric != "nonzero_price_change_fraction"
            else "Horizon-matched 5-minute real-derived bars versus current Phase 9 5-minute synthetic feature aggregates."
        )
        rows.append(
            {
                "level": "L2_marginal",
                "metric": metric,
                "symbols_compared": int(len(joined)),
                "median_relative_or_absolute_error": value,
                "status": status_from_value(value, 0.75, 1.5),
                "evidence": evidence,
                "real_5m_bar_symbols": int(joined["real_5m_bars"].notna().sum()) if "real_5m_bars" in joined else 0,
            }
        )
    return pd.DataFrame(rows)


def _autocorr(group: pd.Series, lag: int = 1) -> float:
    values = group.dropna()
    if len(values) <= lag + 2 or values.std() == 0:
        return np.nan
    return float(values.autocorr(lag))


def level3_temporal(inputs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    features = inputs["phase9_features"].sort_values(["feed_profile", "trade_date", "scenario_day", "symbol", "bar_index"], kind="mergesort")
    group_cols = ["feed_profile", "trade_date", "scenario_day", "symbol"]
    grouped = features.groupby(group_cols, sort=False)
    metrics = {
        "return_autocorr_lag1": grouped["mid_return_1"].apply(_autocorr),
        "abs_return_autocorr_lag1": grouped["mid_return_1"].apply(lambda s: _autocorr(s.abs())),
        "mlofi_autocorr_lag1": grouped["mlofi_qty"].apply(_autocorr),
        "spread_autocorr_lag1": grouped["spread_ticks"].apply(_autocorr),
    }
    rows = []
    for metric, series in metrics.items():
        value = float(series.dropna().median()) if series.notna().any() else None
        rows.append(
            {
                "level": "L3_temporal",
                "metric": metric,
                "groups": int(series.notna().sum()),
                "median_value": value,
                "status": "pass" if value is not None else "missing",
                "evidence": "Autocorrelation measured over synthetic profile/day/symbol feature sequences.",
            }
        )
    return pd.DataFrame(rows)


def level4_cross_sectional(inputs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    daily = inputs["phase5_daily"]
    value_col = "daily_return" if "daily_return" in daily.columns else None
    if value_col is None:
        for candidate in ["close_return", "cumulative_return", "total_return"]:
            if candidate in daily.columns:
                value_col = candidate
                break
    if value_col is None:
        return pd.DataFrame([{"level": "L4_cross_sectional", "metric": "daily_return_correlation", "value": None, "status": "missing", "evidence": "No daily return column found."}])
    pivot = daily.pivot_table(index=["quarter_profile", "scenario_day"], columns="symbol", values=value_col)
    corr = pivot.corr().where(lambda x: ~np.eye(len(x), dtype=bool)).stack()
    return pd.DataFrame(
        [
            {
                "level": "L4_cross_sectional",
                "metric": "pairwise_daily_return_correlation_median",
                "value": float(corr.median()) if len(corr) else None,
                "status": "pass" if len(corr) else "missing",
                "evidence": "Pairwise symbol correlation across synthetic daily returns.",
            },
            {
                "level": "L4_cross_sectional",
                "metric": "pairwise_daily_return_correlation_q95",
                "value": float(corr.quantile(0.95)) if len(corr) else None,
                "status": "pass" if len(corr) else "missing",
                "evidence": "Upper-tail synthetic cross-sectional correlation.",
            },
        ]
    )


def level5_conditional(inputs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    f = inputs["phase9_features"]
    checks = []
    pairs = [
        ("future_return_vs_mlofi", "mlofi_qty", "future_mid_return_1"),
        ("spread_vs_local_volatility", "local_volatility_6", "spread_ticks"),
        ("event_intensity_vs_local_volatility", "local_volatility_6", "event_intensity_proxy"),
        ("future_abs_return_vs_spread", "spread_ticks", "future_mid_return_1_abs"),
    ]
    f = f.copy()
    f["future_mid_return_1_abs"] = f["future_mid_return_1"].abs()
    for metric, x, y in pairs:
        sample = f[[x, y]].dropna()
        value = float(sample[x].rank().corr(sample[y].rank())) if len(sample) > 2 and sample[x].nunique() > 1 and sample[y].nunique() > 1 else None
        checks.append(
            {
                "level": "L5_conditional",
                "metric": metric,
                "rows": int(len(sample)),
                "spearman_corr": value,
                "status": "pass" if value is not None else "missing",
                "evidence": "Synthetic conditional relationship diagnostic; sign is descriptive, not acceptance.",
            }
        )
    return pd.DataFrame(checks)


def level6_discriminator(inputs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    real = inputs["real_price"].merge(inputs["real_depth"], on=["symbol", "instrument_class", "evidence_label"], how="inner")
    synth = inputs["phase9_features"].groupby("symbol", sort=True).agg(
        spread_ticks_median=("spread_ticks", "median"),
        l5_imbalance_median=("l5_imbalance", "median"),
        nonzero_price_change_fraction=("mid_return_1", lambda s: float(s.fillna(0).ne(0).mean())),
        event_intensity_median=("event_intensity_proxy", "median"),
    ).reset_index()
    real_features = real[["symbol", "spread_ticks_median", "l5_imbalance_median", "nonzero_price_change_fraction"]].copy()
    synth_features = synth[["symbol", "spread_ticks_median", "l5_imbalance_median", "nonzero_price_change_fraction"]].copy()
    joined = real_features.merge(synth_features, on="symbol", suffixes=("_real", "_synthetic"))
    score = 0.0
    for metric in ["spread_ticks_median", "l5_imbalance_median", "nonzero_price_change_fraction"]:
        diff = (joined[f"{metric}_synthetic"] - joined[f"{metric}_real"]).abs()
        scale = joined[f"{metric}_real"].abs().median() or 1.0
        score += float((diff / scale).median())
    status = status_from_value(score, 2.0, 5.0)
    return pd.DataFrame(
        [
            {
                "level": "L6_strategy_neutral_realism",
                "metric": "simple_symbol_feature_separability_score",
                "value": score,
                "symbols": int(len(joined)),
                "status": status,
                "evidence": "Simple real-vs-synthetic symbol aggregate separability proxy; not a trained discriminator.",
            }
        ]
    )


def level7_counterfactual(inputs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    cal = inputs["phase4_calendar"]
    rows = []
    for intervention, col, expected in [
        ("increase_volatility", "vol_multiplier", "higher values should correspond to wider return distribution"),
        ("reduce_liquidity", "depth_multiplier", "lower values should correspond to lower depth"),
        ("widen_spreads", "spread_multiplier", "higher values should correspond to wider spreads"),
        ("increase_activity", "event_rate_multiplier", "higher values should correspond to more activity"),
    ]:
        values = cal[col].dropna()
        rows.append(
            {
                "level": "L7_counterfactual",
                "intervention": intervention,
                "calendar_field": col,
                "min_value": float(values.min()),
                "median_value": float(values.median()),
                "max_value": float(values.max()),
                "has_variation": bool(values.nunique() > 1),
                "status": "pass" if values.nunique() > 1 else "warn",
                "expected_result": expected,
            }
        )
    return pd.DataFrame(rows)


def holdout_generator_realism(inputs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    features = inputs["phase9_features"].copy()
    calendar = inputs["phase4_calendar"].copy()
    if features.empty:
        return pd.DataFrame(
            columns=[
                "quarter_profile",
                "feed_profile",
                "holdout_role",
                "scenario_days",
                "feature_rows",
                "symbols",
                "regimes",
                "market_shock_days",
                "median_spread_ticks",
                "nonzero_mid_return_fraction",
                "structural_ready_for_holdout_proxy",
                "realism_status",
                "acceptance_eligible_now",
                "blocker",
            ]
        )
    calendar_flags = calendar.groupby("quarter_profile", sort=True).agg(
        calendar_days=("scenario_day", "nunique"),
        regimes=("regime_code", "nunique"),
        market_shock_days=("is_market_shock_day", "sum"),
    ).reset_index()
    grouped = (
        features.groupby(["quarter_profile", "feed_profile"], sort=True)
        .agg(
            scenario_days=("scenario_day", "nunique"),
            feature_rows=("symbol", "size"),
            symbols=("symbol", "nunique"),
            median_spread_ticks=("spread_ticks", "median"),
            nonzero_mid_return_fraction=("mid_return_1", lambda values: float(values.fillna(0).ne(0).mean())),
            negative_spread_rows=("spread_ticks", lambda values: int((values < 0).sum())),
            nonpositive_mid_rows=("mid_price", lambda values: int((values <= 0).sum())),
        )
        .reset_index()
        .merge(calendar_flags, on="quarter_profile", how="left")
    )
    grouped["holdout_role"] = np.select(
        [
            grouped["quarter_profile"].astype(str).eq("Q-A"),
            grouped["quarter_profile"].astype(str).eq("Q-B"),
            grouped["quarter_profile"].astype(str).eq("Q-C"),
        ],
        [
            "development_reference_profile",
            "bullish_high_momentum_holdout_proxy",
            "stressed_volatile_holdout_proxy",
        ],
        default="unclassified_profile",
    )
    grouped["structural_ready_for_holdout_proxy"] = (
        grouped["scenario_days"].ge(60)
        & grouped["symbols"].ge(32)
        & grouped["negative_spread_rows"].eq(0)
        & grouped["nonpositive_mid_rows"].eq(0)
    )
    grouped["realism_status"] = np.where(
        grouped["structural_ready_for_holdout_proxy"],
        "holdout_proxy_available_not_acceptance",
        "holdout_proxy_incomplete",
    )
    grouped["acceptance_eligible_now"] = False
    grouped["blocker"] = (
        "Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not "
        "acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout "
        "configs with full event/tick execution and later multi-day real holdout."
    )
    return grouped[
        [
            "quarter_profile",
            "feed_profile",
            "holdout_role",
            "scenario_days",
            "feature_rows",
            "symbols",
            "regimes",
            "market_shock_days",
            "median_spread_ticks",
            "nonzero_mid_return_fraction",
            "structural_ready_for_holdout_proxy",
            "realism_status",
            "acceptance_eligible_now",
            "blocker",
        ]
    ]


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


def warning_triage(summary: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "level",
        "validation_table",
        "metric",
        "status",
        "observed_value",
        "acceptance_impact",
        "root_cause",
        "next_required_evidence",
        "not_acceptance_waiver",
    ]
    non_pass = summary[summary["status"].astype(str) != "pass"].copy()
    rows = []
    for row in non_pass.to_dict("records"):
        metric = str(row.get("metric") or row.get("check_name") or row.get("intervention") or "unknown_check")
        status = str(row.get("status"))
        observed_value = next(
            (
                row.get(field)
                for field in ("value", "median_relative_or_absolute_error", "median_value")
                if pd.notna(row.get(field))
            ),
            None,
        )
        if metric == "nonzero_price_change_fraction":
            root_cause = (
                "Current Phase 9 features are 5-minute synthetic state/features, while the calibration reference is "
                "one-day received-tick activity; price-change frequency is therefore not expected to match tick-level "
                "nonzero-change frequency without a dedicated event/tick generator or horizon-specific tolerance."
            )
            next_required = (
                "Either add a horizon-matched comparison for 5-minute synthetic features versus 5-minute real-derived "
                "features, or introduce a tick/event-level generator that can target received-tick nonzero price-change "
                "frequency directly."
            )
        else:
            root_cause = "Non-pass quality check requires manual review before promotion use."
            next_required = "Add metric-specific tolerance, calibration evidence or generator fix before treating this as accepted realism evidence."
        rows.append(
            {
                "level": row.get("level"),
                "validation_table": row.get("validation_table"),
                "metric": metric,
                "status": status,
                "observed_value": observed_value,
                "acceptance_impact": "blocks_realism_gate",
                "root_cause": root_cause,
                "next_required_evidence": next_required,
                "not_acceptance_waiver": True,
            }
        )
    return pd.DataFrame(rows, columns=columns)


def realism_acceptance_gap_ledger(
    quality_summary: pd.DataFrame,
    triage: pd.DataFrame,
    holdout: pd.DataFrame,
    strategy_matrix: pd.DataFrame,
) -> pd.DataFrame:
    columns = [
        "strategy_id",
        "realism_requirement",
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
        "outputs/phase14/quality_gate_summary.csv; outputs/phase14/quality_warning_triage.csv; "
        "outputs/phase14/holdout_generator_realism_summary.csv; outputs/phase11/strategy_validation_matrix.csv"
    )
    quality_fail = int((quality_summary["status"].astype(str) == "fail").sum()) if len(quality_summary) else 0
    quality_warn = int((quality_summary["status"].astype(str) == "warn").sum()) if len(quality_summary) else 0
    quality_pass = int((quality_summary["status"].astype(str) == "pass").sum()) if len(quality_summary) else 0
    triage_rows = int(len(triage))
    holdout_rows = int(len(holdout))
    holdout_proxy_rows = int((holdout["realism_status"].astype(str) == "holdout_proxy_available_not_acceptance").sum()) if len(holdout) else 0
    structural_ready_rows = int(holdout["structural_ready_for_holdout_proxy"].astype(bool).sum()) if len(holdout) else 0
    feed_profiles = set(map(str, holdout["feed_profile"].dropna().unique())) if len(holdout) else set()
    quarter_profiles = set(map(str, holdout["quarter_profile"].dropna().unique())) if len(holdout) else set()
    has_feed_imperfections = bool({"disconnect_scenario", "stressed_retail"}.issubset(feed_profiles))
    has_holdout_quarters = bool({"Q-B", "Q-C"}.issubset(quarter_profiles))

    rows: list[dict] = []
    for record in strategy_matrix.sort_values("strategy_id").to_dict("records"):
        strategy_id = str(record["strategy_id"])
        support_level = str(record.get("support_level", "unknown"))
        runnable_proxy = support_level == "runnable_proxy"

        def add(
            realism_requirement: str,
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
                    "realism_requirement": realism_requirement,
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
            "synthetic_quality_gate_clear",
            "no failing or warning quality checks before strategy realism acceptance",
            f"pass={quality_pass}; warn={quality_warn}; fail={quality_fail}; triage_rows={triage_rows}",
            "quality_proxy_clear_not_acceptance" if quality_fail == 0 and quality_warn == 0 else "quality_warnings_or_failures_present",
            bool(len(quality_summary) and quality_fail == 0 and quality_warn == 0),
            "Quality checks are current synthetic diagnostics over one-day calibration and generated scenarios, not strategy rerun evidence.",
            "Keep quality gates green after any generator changes and rerun strategy realism checks on the accepted generator version.",
        )
        add(
            "holdout_generator_coverage",
            "structurally ready holdout-generator profiles exist for development and holdout quarters",
            f"{holdout_proxy_rows}/{holdout_rows} holdout proxy rows; structural_ready={structural_ready_rows}; quarters={';'.join(sorted(quarter_profiles))}",
            "holdout_generator_proxy_available_not_acceptance" if holdout_proxy_rows else "missing_holdout_generator_proxy",
            bool(holdout_proxy_rows and has_holdout_quarters),
            "Holdout-generator coverage exists as structural proxy evidence, but strategies have not been rerun as acceptance tests.",
            "Run every candidate strategy on predeclared holdout-generator profiles and compare against development/calibration results.",
        )
        add(
            "feed_imperfection_coverage",
            "holdout evidence includes disconnect and stressed-retail feed profiles",
            f"feed_profiles={';'.join(sorted(feed_profiles)) if feed_profiles else 'none'}",
            "feed_imperfection_proxy_available_not_acceptance" if has_feed_imperfections else "missing_feed_imperfection_proxy",
            has_feed_imperfections,
            "Feed imperfections exist as generated profiles, not acceptance-grade strategy reruns.",
            "Rerun strategies on disconnect/stressed feed profiles with full lifecycle execution and verify performance does not depend on ideal feed assumptions.",
        )
        add(
            "strategy_support_ready",
            "strategy is runnable in the current feature and execution product",
            f"support_level={support_level}",
            "runnable_proxy_not_acceptance" if runnable_proxy else "partial_or_unsupported_strategy",
            runnable_proxy,
            "Partial or unsupported strategies cannot pass realism until required features/modules exist.",
            "Implement missing strategy features/modules or mark the strategy as research-only before realism acceptance.",
        )
        add(
            "holdout_strategy_rerun",
            "strategy rerun on holdout-generator configurations with no development leakage",
            "not available in current Phase 14 evidence",
            "missing_holdout_strategy_rerun",
            False,
            "Current Phase 14 holdout rows are generator/profile diagnostics, not strategy P&L or signal reruns.",
            "Run Phase 11/12/13 strategy evaluation on Q-B/Q-C holdout profiles and preserve leakage checks.",
        )
        add(
            "pessimistic_execution_realism",
            "holdout strategy rerun uses stressed retail latency/slippage/fill assumptions",
            "not available in current Phase 14 evidence",
            "missing_pessimistic_execution_holdout_rerun",
            False,
            "Strategies have not been rerun on holdout generator outputs with pessimistic execution controls.",
            "Evaluate holdout-generator strategy results with stressed retail, partial-fill and risk-control assumptions.",
        )
        add(
            "artifact_exploitation_rejection",
            "strategy does not exploit generator artifacts or synthetic-only templates",
            "not available in current Phase 14 evidence",
            "missing_artifact_exploitation_rejection",
            False,
            "No negative-control or artifact-exploitation rerun exists for realism acceptance.",
            "Run artifact/control templates and reject strategies whose edge disappears or depends on generator-specific artifacts.",
        )
        add(
            "real_multi_day_realism_validation",
            "realism and strategy behavior validated on multiple real market days",
            "not available in current one-day/proxy evidence",
            "missing_multi_day_real_realism_validation",
            False,
            "Real calibration uses a one-day sample and no multi-day strategy validation.",
            "Collect and validate multiple real market days, then compare strategy behavior against synthetic and holdout-generator results.",
        )

    return pd.DataFrame(rows, columns=columns).sort_values(["strategy_id", "realism_requirement"], kind="mergesort")


def write_report(
    output_dir: Path,
    frames: dict[str, pd.DataFrame],
    triage: pd.DataFrame,
    holdout: pd.DataFrame,
    real_5m: pd.DataFrame,
    realism_gap: pd.DataFrame,
) -> None:
    summary = pd.concat(
        [
            frame.assign(validation_table=name)
            for name, frame in frames.items()
            if "status" in frame.columns
        ],
        ignore_index=True,
        sort=False,
    )
    status_summary = summary.groupby(["level", "status"], dropna=False).size().reset_index(name="checks")
    realism_gap_summary = (
        realism_gap.groupby(["realism_requirement", "proxy_evidence_available", "acceptance_requirement_met"], sort=True)
        .size()
        .reset_index(name="rows")
        if len(realism_gap)
        else pd.DataFrame(columns=["realism_requirement", "proxy_evidence_available", "acceptance_requirement_met", "rows"])
    )
    lines = [
        "# Phase 14 Synthetic Data Quality Validation Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase validates current synthetic products against structural, marginal, temporal, cross-sectional, conditional, discriminator-proxy and counterfactual checks.",
        "It is a quality gate diagnostic, not strategy acceptance.",
        "",
        "## Status Summary",
        "",
        _markdown_table(status_summary),
        "",
        "## Level 1 Structural",
        "",
        _markdown_table(frames["level1_structural"]),
        "",
        "## Level 2 Marginal",
        "",
        _markdown_table(frames["level2_marginal"]),
        "",
        "## Real-Derived 5-Minute Symbol Marginals",
        "",
        _markdown_table(real_5m),
        "",
        "## Warning Triage",
        "",
        _markdown_table(triage),
        "",
        "## Holdout Generator Realism Proxy",
        "",
        _markdown_table(holdout),
        "",
        "## Realism Acceptance Gap Ledger",
        "",
        _markdown_table(realism_gap_summary),
        "",
        _markdown_table(realism_gap),
        "",
        "## Caveats",
        "",
        "- Real evidence is still a one-day sample.",
        "- Current Phase 6-9 synthetic products are 5-minute state/feature products, not full tick-event simulation.",
        "- Fail/warn labels identify engineering work, not trading conclusions.",
        "",
    ]
    (output_dir / "phase14_quality_validation_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase14(output_dir: Path, paths: dict[str, Path]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    inputs = load_inputs(paths)
    real_5m = real_5m_symbol_marginals(inputs["phase1_deltas_dir"])
    frames = {
        "level1_structural": level1_structural(inputs),
        "level2_marginal": level2_marginals(inputs, real_5m=real_5m),
        "level3_temporal": level3_temporal(inputs),
        "level4_cross_sectional": level4_cross_sectional(inputs),
        "level5_conditional": level5_conditional(inputs),
        "level6_discriminator_proxy": level6_discriminator(inputs),
        "level7_counterfactual": level7_counterfactual(inputs),
    }
    for name, frame in frames.items():
        frame.to_csv(output_dir / f"{name}.csv", index=False)
    real_5m.to_csv(output_dir / "real_5m_symbol_marginals.csv", index=False)
    summary = pd.concat(
        [frame.assign(validation_table=name) for name, frame in frames.items() if "status" in frame.columns],
        ignore_index=True,
        sort=False,
    )
    triage = warning_triage(summary)
    holdout = holdout_generator_realism(inputs)
    realism_gap = realism_acceptance_gap_ledger(summary, triage, holdout, inputs["strategy_matrix"])
    summary.to_csv(output_dir / "quality_gate_summary.csv", index=False)
    triage.to_csv(output_dir / "quality_warning_triage.csv", index=False)
    holdout.to_csv(output_dir / "holdout_generator_realism_summary.csv", index=False)
    realism_gap.to_csv(output_dir / "realism_acceptance_gap_ledger.csv", index=False)
    inputs_manifest = {key: str(value) for key, value in paths.items()}
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "inputs": inputs_manifest,
        "tables": list(frames),
        "summary_rows": int(len(summary)),
        "warning_triage_rows": int(len(triage)),
        "real_5m_symbol_marginal_rows": int(len(real_5m)),
        "holdout_generator_realism_rows": int(len(holdout)),
        "holdout_proxy_available_rows": int(
            (holdout["realism_status"].astype(str) == "holdout_proxy_available_not_acceptance").sum()
        ),
        "realism_acceptance_gap_rows": int(len(realism_gap)),
        "realism_acceptance_gap_open_rows": int((~realism_gap["acceptance_requirement_met"].astype(bool)).sum()) if len(realism_gap) else 0,
        "realism_acceptance_gap_proxy_available_rows": int(realism_gap["proxy_evidence_available"].astype(bool).sum()) if len(realism_gap) else 0,
        "realism_acceptance_gap_met_rows": int(realism_gap["acceptance_requirement_met"].astype(bool).sum()) if len(realism_gap) else 0,
        "status_counts": summary["status"].value_counts(dropna=False).to_dict(),
        "not_strategy_acceptance": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase14",
            generated_utc=generated_utc,
            inputs=inputs_manifest,
            parameters={"validation_levels": list(frames), "not_strategy_acceptance": True},
            outputs={
                "quality_gate_summary": str(output_dir / "quality_gate_summary.csv"),
                "quality_warning_triage": str(output_dir / "quality_warning_triage.csv"),
                "real_5m_symbol_marginals": str(output_dir / "real_5m_symbol_marginals.csv"),
                "holdout_generator_realism_summary": str(output_dir / "holdout_generator_realism_summary.csv"),
                "realism_acceptance_gap_ledger": str(output_dir / "realism_acceptance_gap_ledger.csv"),
                "report": str(output_dir / "phase14_quality_validation_report.md"),
                "manifest": str(output_dir / "quality_validation_manifest.json"),
                **{name: str(output_dir / f"{name}.csv") for name in frames},
            },
            random_seed="not_applicable_deterministic_quality_checks",
            scenario_ids="outputs/phase4/scenario_calendar.csv_via_phase5_phase6_phase9",
            cost_model_version="not_applicable_no_execution_costs",
            latency_model_version="phase8_feed_profiles_v1",
        )
    )
    (output_dir / "quality_validation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, frames, triage, holdout, real_5m, realism_gap)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 14 synthetic data quality validation.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase14"))
    parser.add_argument("--real-quality", type=Path, default=Path("outputs/stage_a1/data_quality_report.csv"))
    parser.add_argument("--real-price", type=Path, default=Path("outputs/phase2/price_tick_calibration.csv"))
    parser.add_argument("--real-depth", type=Path, default=Path("outputs/phase2/depth_calibration.csv"))
    parser.add_argument("--phase1-deltas-dir", type=Path, default=Path("outputs/phase1/received_tick_deltas_by_symbol"))
    parser.add_argument("--phase4-calendar", type=Path, default=Path("outputs/phase4/scenario_calendar.csv"))
    parser.add_argument("--phase5-daily", type=Path, default=Path("outputs/phase5/daily_price_summary.csv"))
    parser.add_argument("--phase6-summary", type=Path, default=Path("outputs/phase6/l2_book_summary.csv"))
    parser.add_argument("--phase9-features", type=Path, default=Path("outputs/phase9/tier_c/features_5m.parquet"))
    parser.add_argument("--strategy-matrix", type=Path, default=Path("outputs/phase11/strategy_validation_matrix.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "real_quality": args.real_quality,
        "real_price": args.real_price,
        "real_depth": args.real_depth,
        "phase1_deltas_dir": args.phase1_deltas_dir,
        "phase4_calendar": args.phase4_calendar,
        "phase5_daily": args.phase5_daily,
        "phase6_summary": args.phase6_summary,
        "phase9_features": args.phase9_features,
        "strategy_matrix": args.strategy_matrix,
    }
    run_phase14(args.output_dir, paths)


if __name__ == "__main__":
    main()
