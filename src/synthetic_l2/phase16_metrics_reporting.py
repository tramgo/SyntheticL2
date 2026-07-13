from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


PREDICTIVE_METRICS = [
    ("directional_accuracy", "computed_proxy", "phase11_signal_diagnostics.directional_accuracy_nonzero"),
    ("balanced_accuracy", "missing", "Requires class-confusion counts by direction."),
    ("precision_recall_by_direction", "missing", "Requires true/false positives by long/short direction."),
    ("roc_auc", "missing", "Requires probabilistic scores or ranked continuous predictions."),
    ("brier_score", "missing", "Requires calibrated probability forecasts."),
    ("calibration_curve", "missing", "Requires probability bins and realized frequencies."),
    ("information_coefficient", "proxy_available", "Proxy signed_mean_future_return is available; rank IC is not computed yet."),
    ("future_return_by_signal_decile", "missing", "Requires continuous signal scores and decile bucketing."),
    ("incremental_r2", "missing", "Requires model-vs-baseline regression outputs."),
    ("feature_importance_stability", "missing", "Requires multi-seed/model feature importance runs."),
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
    ("volatility_bucket", "volatility_bucket", "missing"),
    ("spread_bucket", "spread_ticks", "proxy_available"),
    ("liquidity_bucket", "liquidity_bucket", "missing"),
    ("long_short", "side", "available"),
    ("latency_profile", "execution_profile", "available"),
    ("cost_profile", "execution_profile", "proxy_available"),
    ("random_seed", "seed", "missing"),
    ("event_vs_non_event_day", "is_market_shock_day", "available"),
]


def load_inputs(paths: dict[str, Path]) -> dict[str, pd.DataFrame]:
    return {
        "signal_diagnostics": pd.read_csv(paths["signal_diagnostics"]),
        "metric_requirements": pd.read_csv(paths["metric_requirements"]),
        "execution_summary": pd.read_csv(paths["execution_summary"]),
        "trade_sample": pd.read_parquet(paths["trade_sample"]),
        "acceptance_summary": pd.read_csv(paths["acceptance_summary"]),
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
    req["phase16_current_status"] = req["primary_metric"].map(status_map).fillna("strategy_specific_missing_or_not_mapped")
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


def write_report(output_dir: Path, catalog: pd.DataFrame, predictive: pd.DataFrame, trading: pd.DataFrame, breakdowns: pd.DataFrame) -> None:
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
    markouts = markout_analysis(inputs["trade_sample"])
    inputs["markout_analysis"] = markouts
    trading = trading_scoreboard(inputs)
    breakdowns = breakdown_coverage(inputs)
    requirement_coverage = metric_requirement_coverage(inputs, catalog)

    catalog.to_csv(output_dir / "metric_catalog.csv", index=False)
    predictive.to_csv(output_dir / "predictive_metric_scoreboard.csv", index=False)
    trading.to_csv(output_dir / "trading_metric_scoreboard.csv", index=False)
    markouts.to_csv(output_dir / "markout_mae_mfe_summary.csv", index=False)
    breakdowns.to_csv(output_dir / "breakdown_coverage.csv", index=False)
    requirement_coverage.to_csv(output_dir / "strategy_metric_requirement_coverage.csv", index=False)
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {key: str(value) for key, value in paths.items()},
        "metric_catalog_rows": int(len(catalog)),
        "predictive_scoreboard_rows": int(len(predictive)),
        "trading_scoreboard_rows": int(len(trading)),
        "markout_summary_rows": int(len(markouts)),
        "markout_horizons_bars": [1, 3, 6],
        "breakdown_rows": int(len(breakdowns)),
        "acceptance_grade_metrics": int(catalog["acceptance_eligible_now"].sum()),
        "scope": "metrics_reporting_catalog_and_proxy_scoreboards",
    }
    (output_dir / "metrics_reporting_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, catalog, predictive, trading, breakdowns)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 16 metrics/reporting artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase16"))
    parser.add_argument("--signal-diagnostics", type=Path, default=Path("outputs/phase11/strategy_signal_diagnostics.csv"))
    parser.add_argument("--metric-requirements", type=Path, default=Path("outputs/phase11/strategy_metric_requirements.csv"))
    parser.add_argument("--execution-summary", type=Path, default=Path("outputs/phase12/execution_summary.csv"))
    parser.add_argument("--trade-sample", type=Path, default=Path("outputs/phase12/trade_ledger_sample.parquet"))
    parser.add_argument("--acceptance-summary", type=Path, default=Path("outputs/phase15/strategy_acceptance_summary.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "signal_diagnostics": args.signal_diagnostics,
        "metric_requirements": args.metric_requirements,
        "execution_summary": args.execution_summary,
        "trade_sample": args.trade_sample,
        "acceptance_summary": args.acceptance_summary,
    }
    run_phase16(args.output_dir, paths)


if __name__ == "__main__":
    main()
