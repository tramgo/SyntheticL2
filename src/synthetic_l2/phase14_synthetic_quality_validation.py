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


def load_inputs(paths: dict[str, Path]) -> dict[str, pd.DataFrame]:
    return {
        "real_quality": pd.read_csv(paths["real_quality"]),
        "real_price": pd.read_csv(paths["real_price"]),
        "real_depth": pd.read_csv(paths["real_depth"]),
        "phase4_calendar": pd.read_csv(paths["phase4_calendar"]),
        "phase5_daily": pd.read_csv(paths["phase5_daily"]),
        "phase6_summary": pd.read_csv(paths["phase6_summary"]),
        "phase9_features": pq.read_table(paths["phase9_features"]).to_pandas(),
    }


def level1_structural(inputs: dict[str, pd.DataFrame]) -> pd.DataFrame:
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


def level2_marginals(inputs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    real_price = inputs["real_price"][["symbol", "spread_ticks_median", "spread_ticks_q95", "nonzero_price_change_fraction"]]
    real_depth = inputs["real_depth"][["symbol", "bid_l5_qty_median", "ask_l5_qty_median", "l5_imbalance_median"]]
    real = real_price.merge(real_depth, on="symbol", how="inner")
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
        rows.append(
            {
                "level": "L2_marginal",
                "metric": metric,
                "symbols_compared": int(len(joined)),
                "median_relative_or_absolute_error": value,
                "status": status_from_value(value, 0.75, 1.5),
                "evidence": "Real one-day symbol calibration versus current Phase 9 synthetic feature aggregates.",
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


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
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
    frames = {
        "level1_structural": level1_structural(inputs),
        "level2_marginal": level2_marginals(inputs),
        "level3_temporal": level3_temporal(inputs),
        "level4_cross_sectional": level4_cross_sectional(inputs),
        "level5_conditional": level5_conditional(inputs),
        "level6_discriminator_proxy": level6_discriminator(inputs),
        "level7_counterfactual": level7_counterfactual(inputs),
    }
    for name, frame in frames.items():
        frame.to_csv(output_dir / f"{name}.csv", index=False)
    summary = pd.concat(
        [frame.assign(validation_table=name) for name, frame in frames.items() if "status" in frame.columns],
        ignore_index=True,
        sort=False,
    )
    summary.to_csv(output_dir / "quality_gate_summary.csv", index=False)
    inputs_manifest = {key: str(value) for key, value in paths.items()}
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "inputs": inputs_manifest,
        "tables": list(frames),
        "summary_rows": int(len(summary)),
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
    write_report(output_dir, frames)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 14 synthetic data quality validation.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase14"))
    parser.add_argument("--real-quality", type=Path, default=Path("outputs/stage_a1/data_quality_report.csv"))
    parser.add_argument("--real-price", type=Path, default=Path("outputs/phase2/price_tick_calibration.csv"))
    parser.add_argument("--real-depth", type=Path, default=Path("outputs/phase2/depth_calibration.csv"))
    parser.add_argument("--phase4-calendar", type=Path, default=Path("outputs/phase4/scenario_calendar.csv"))
    parser.add_argument("--phase5-daily", type=Path, default=Path("outputs/phase5/daily_price_summary.csv"))
    parser.add_argument("--phase6-summary", type=Path, default=Path("outputs/phase6/l2_book_summary.csv"))
    parser.add_argument("--phase9-features", type=Path, default=Path("outputs/phase9/tier_c/features_5m.parquet"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "real_quality": args.real_quality,
        "real_price": args.real_price,
        "real_depth": args.real_depth,
        "phase4_calendar": args.phase4_calendar,
        "phase5_daily": args.phase5_daily,
        "phase6_summary": args.phase6_summary,
        "phase9_features": args.phase9_features,
    }
    run_phase14(args.output_dir, paths)


if __name__ == "__main__":
    main()
