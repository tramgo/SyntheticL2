from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from synthetic_l2.phase12_execution_simulator import EXECUTION_PROFILES
from synthetic_l2.phase25_event_replay_expansion import (
    _markdown_table,
    load_event_features,
    risk_summary,
    simulate_signal,
    summarize_trades,
)
from synthetic_l2.reproducibility import reproducibility_fields


FEATURE_SPECS = [
    {"feature_id": "F01_momentum_3_event", "column": "momentum_3_event", "polarity": 1, "feature_family": "short_horizon_momentum"},
    {"feature_id": "F02_mlofi_qty_event", "column": "mlofi_qty_event", "polarity": 1, "feature_family": "order_flow_imbalance"},
    {"feature_id": "F03_l1_imbalance", "column": "l1_imbalance", "polarity": 1, "feature_family": "top_of_book_imbalance"},
    {"feature_id": "F04_l5_imbalance", "column": "l5_imbalance", "polarity": 1, "feature_family": "depth_imbalance"},
    {"feature_id": "F05_microprice_dev", "column": "microprice_dev", "polarity": 1, "feature_family": "microprice_pressure"},
    {"feature_id": "F06_l5_mean_reversion", "column": "l5_imbalance", "polarity": -1, "feature_family": "depth_mean_reversion"},
    {"feature_id": "F07_l1_mean_reversion", "column": "l1_imbalance", "polarity": -1, "feature_family": "top_of_book_mean_reversion"},
]
HORIZON_EVENTS = [1, 2, 3, 5]
THRESHOLD_QUANTILES = [0.50, 0.70, 0.85, 0.95]
MIN_TRADES_FOR_EDGE = 50


def _group_cols() -> list[str]:
    return ["feed_profile", "trade_date", "stage_b2_bucket", "scenario_day", "symbol"]


def add_horizon_mid(features: pd.DataFrame, horizon_events: int) -> pd.DataFrame:
    frame = features.copy()
    grouped = frame.groupby(_group_cols(), sort=False)
    frame["next_mid_price"] = grouped["mid_price"].shift(-horizon_events)
    frame["edge_horizon_events"] = horizon_events
    return frame


def _feature_threshold(features: pd.DataFrame, column: str, threshold_quantile: float) -> float:
    values = features[column].astype(float).abs().replace([np.inf, -np.inf], np.nan).dropna()
    if values.empty:
        return 0.0
    return float(values.quantile(threshold_quantile))


def build_candidate_catalog(features: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for spec in FEATURE_SPECS:
        for horizon_events in HORIZON_EVENTS:
            for threshold_quantile in THRESHOLD_QUANTILES:
                threshold_value = _feature_threshold(features, spec["column"], threshold_quantile)
                candidate_id = f"{spec['feature_id']}_h{horizon_events}_q{int(threshold_quantile * 100):02d}"
                rows.append(
                    {
                        "candidate_id": candidate_id,
                        "feature_id": spec["feature_id"],
                        "feature_family": spec["feature_family"],
                        "feature_column": spec["column"],
                        "polarity": int(spec["polarity"]),
                        "horizon_events": int(horizon_events),
                        "threshold_quantile": float(threshold_quantile),
                        "threshold_value": threshold_value,
                        "candidate_scope": "phase27_feature_edge_cost_hurdle_scan_not_acceptance",
                    }
                )
    return pd.DataFrame(rows)


def build_candidate_signal(features: pd.DataFrame, candidate: dict) -> pd.Series:
    values = features[str(candidate["feature_column"])].astype(float)
    signal = np.sign(values) * int(candidate["polarity"])
    signal = pd.Series(signal, index=features.index).where(values.abs() >= float(candidate["threshold_value"]), 0)
    tradable = features["next_mid_price"].notna()
    tradable &= ~features["is_disconnect_gap"].astype(bool)
    tradable &= ~features["is_duplicate"].astype(bool)
    tradable &= ~features["is_out_of_order_injected"].astype(bool)
    tradable &= features["spread_ticks"].astype(float).ge(1)
    return signal.where(tradable, 0).fillna(0).astype("int8")


def baseline_comparison(summary: pd.DataFrame, phase25_summary: pd.DataFrame) -> pd.DataFrame:
    baseline_summary = phase25_summary[phase25_summary["model_type"].eq("baseline")].copy()
    rows = []
    for row in summary.to_dict("records"):
        comp = baseline_summary[baseline_summary["execution_profile"].eq(row["execution_profile"])]
        best_baseline = float(comp["mean_net_return"].max()) if len(comp) else np.nan
        rows.append(
            {
                "candidate_id": row["model_id"],
                "feature_id": row["feature_id"],
                "feature_family": row["feature_family"],
                "execution_profile": row["execution_profile"],
                "horizon_events": int(row["horizon_events"]),
                "threshold_quantile": float(row["threshold_quantile"]),
                "trades": int(row["trades"]),
                "mean_gross_return": float(row["mean_gross_return"]),
                "mean_cost_return": float(row["mean_cost_return"]),
                "mean_net_return": float(row["mean_net_return"]),
                "best_baseline_mean_net_return": best_baseline,
                "net_return_lift_vs_best_baseline": float(row["mean_net_return"] - best_baseline) if pd.notna(best_baseline) else np.nan,
                "positive_after_costs": bool(row["mean_net_return"] > 0.0),
                "beats_best_baseline_proxy": bool(row["mean_net_return"] > best_baseline) if pd.notna(best_baseline) else False,
                "enough_trades_for_edge": bool(row["trades"] >= MIN_TRADES_FOR_EDGE),
            }
        )
    return pd.DataFrame(rows)


def edge_candidate_summary(comparison: pd.DataFrame, risk: pd.DataFrame) -> pd.DataFrame:
    if comparison.empty:
        return pd.DataFrame()
    merged = comparison.merge(
        risk[["model_id", "execution_profile", "risk_status"]],
        left_on=["candidate_id", "execution_profile"],
        right_on=["model_id", "execution_profile"],
        how="left",
    ).drop(columns=["model_id"])
    merged["realistic_charged_profile"] = ~merged["execution_profile"].astype(str).eq("zero_latency_spread_only_control")
    merged["risk_not_breached_proxy"] = merged["risk_status"].astype(str).eq("risk_not_breached_proxy")
    merged["cost_hurdle_ratio"] = np.where(
        merged["mean_cost_return"].abs() > 0,
        merged["mean_gross_return"] / merged["mean_cost_return"].abs(),
        np.nan,
    )
    merged["realistic_cost_clearing_edge"] = (
        merged["realistic_charged_profile"]
        & merged["positive_after_costs"]
        & merged["beats_best_baseline_proxy"]
        & merged["enough_trades_for_edge"]
        & merged["risk_not_breached_proxy"]
    )
    merged["zero_latency_edge_control"] = (
        ~merged["realistic_charged_profile"]
        & merged["positive_after_costs"]
        & merged["beats_best_baseline_proxy"]
        & merged["enough_trades_for_edge"]
        & merged["risk_not_breached_proxy"]
    )
    return merged.sort_values(
        ["realistic_cost_clearing_edge", "mean_net_return", "cost_hurdle_ratio"],
        ascending=[False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def feature_family_summary(candidates: pd.DataFrame) -> pd.DataFrame:
    if candidates.empty:
        return pd.DataFrame()
    grouped = candidates.groupby(["feature_family", "execution_profile"], sort=True)
    return grouped.agg(
        candidate_rows=("candidate_id", "size"),
        positive_after_cost_rows=("positive_after_costs", "sum"),
        realistic_cost_clearing_rows=("realistic_cost_clearing_edge", "sum"),
        zero_latency_edge_control_rows=("zero_latency_edge_control", "sum"),
        max_mean_net_return=("mean_net_return", "max"),
        max_cost_hurdle_ratio=("cost_hurdle_ratio", "max"),
        median_trades=("trades", "median"),
    ).reset_index()


def rejection_ledger(candidates: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for row in candidates.to_dict("records"):
        reasons = []
        if not row["realistic_charged_profile"]:
            reasons.append("zero_latency_control_not_retail_edge")
        if not row["positive_after_costs"]:
            reasons.append("net_return_not_positive_after_costs")
        if not row["beats_best_baseline_proxy"]:
            reasons.append("does_not_beat_best_baseline_proxy")
        if not row["enough_trades_for_edge"]:
            reasons.append("insufficient_trade_count")
        if not row["risk_not_breached_proxy"]:
            reasons.append("proxy_risk_breached_or_missing")
        if not reasons:
            reasons.append("cost_clearing_feature_edge_for_deeper_strategy_design")
        rows.append(
            {
                "candidate_id": row["candidate_id"],
                "feature_id": row["feature_id"],
                "feature_family": row["feature_family"],
                "execution_profile": row["execution_profile"],
                "horizon_events": int(row["horizon_events"]),
                "rejection_reasons": ";".join(reasons),
                "realistic_cost_clearing_edge": bool(row["realistic_cost_clearing_edge"]),
                "phase27_scope": "feature_edge_cost_hurdle_scan_not_acceptance",
            }
        )
    return pd.DataFrame(rows)


def overall_summary(catalog: pd.DataFrame, summary: pd.DataFrame, candidates: pd.DataFrame, rejection: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"metric": "phase27_feature_candidates_registered", "value": int(len(catalog)), "description": "Feature/horizon/threshold candidates registered"},
            {"metric": "phase27_candidate_profile_rows", "value": int(len(summary)), "description": "Candidate/profile replay summary rows"},
            {"metric": "phase27_total_replay_trades", "value": int(summary["trades"].sum()) if len(summary) else 0, "description": "Total trades across feature-edge replays"},
            {"metric": "phase27_positive_after_cost_rows", "value": int(candidates["positive_after_costs"].sum()) if len(candidates) else 0, "description": "Rows with positive mean net return after costs"},
            {"metric": "phase27_realistic_cost_clearing_rows", "value": int(candidates["realistic_cost_clearing_edge"].sum()) if len(candidates) else 0, "description": "Retail/stressed rows passing net, baseline, trade-count and risk filters"},
            {"metric": "phase27_zero_latency_edge_control_rows", "value": int(candidates["zero_latency_edge_control"].sum()) if len(candidates) else 0, "description": "Frictionless positive feature-edge controls"},
            {"metric": "phase27_rejected_candidate_rows", "value": int((~rejection["realistic_cost_clearing_edge"]).sum()) if len(rejection) else 0, "description": "Candidate/profile rows rejected by at least one diagnostic"},
            {"metric": "phase27_acceptance_ready", "value": 0, "description": "Feature-edge scan is diagnostic evidence, not acceptance evidence"},
        ]
    )


def write_report(
    output_dir: Path,
    overall: pd.DataFrame,
    family: pd.DataFrame,
    candidates: pd.DataFrame,
    rejection: pd.DataFrame,
    catalog: pd.DataFrame,
) -> None:
    lines = [
        "# Phase 27 Feature Edge Cost-Hurdle Scan",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This milestone checks whether raw event-level features contain enough directional edge to clear execution costs.",
        "It is a diagnostic for signal redesign, not a strategy promotion result.",
        "",
        "## Overall Summary",
        "",
        _markdown_table(overall),
        "",
        "## Feature Family Summary",
        "",
        _markdown_table(family),
        "",
        "## Top Candidate Diagnostics",
        "",
        _markdown_table(candidates.head(40)),
        "",
        "## Rejection Ledger",
        "",
        _markdown_table(rejection.head(60)),
        "",
        "## Candidate Catalog",
        "",
        _markdown_table(catalog.head(60)),
        "",
    ]
    (output_dir / "phase27_feature_edge_scan_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase27(event_features_path: Path, phase25_summary_path: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    base_features = load_event_features(event_features_path)
    catalog = build_candidate_catalog(base_features)
    phase25_summary = pd.read_csv(phase25_summary_path)
    trade_frames = []

    for horizon_events in HORIZON_EVENTS:
        features = add_horizon_mid(base_features, horizon_events)
        for candidate in catalog[catalog["horizon_events"].eq(horizon_events)].to_dict("records"):
            signal = build_candidate_signal(features, candidate)
            for profile in EXECUTION_PROFILES:
                trades = simulate_signal(features, signal, str(candidate["candidate_id"]), "feature_edge_candidate", profile)
                if trades.empty:
                    continue
                trades["feature_id"] = candidate["feature_id"]
                trades["feature_family"] = candidate["feature_family"]
                trades["feature_column"] = candidate["feature_column"]
                trades["horizon_events"] = int(candidate["horizon_events"])
                trades["threshold_quantile"] = float(candidate["threshold_quantile"])
                trades["threshold_value"] = float(candidate["threshold_value"])
                trades["polarity"] = int(candidate["polarity"])
                trades["phase27_scope"] = "feature_edge_cost_hurdle_scan_not_acceptance"
                trade_frames.append(trades)

    trades = pd.concat(trade_frames, ignore_index=True) if trade_frames else pd.DataFrame()
    summary = summarize_trades(trades)
    if len(summary):
        lookup = catalog.set_index("candidate_id").to_dict("index")
        summary["feature_id"] = summary["model_id"].map(lambda value: lookup[value]["feature_id"])
        summary["feature_family"] = summary["model_id"].map(lambda value: lookup[value]["feature_family"])
        summary["horizon_events"] = summary["model_id"].map(lambda value: lookup[value]["horizon_events"])
        summary["threshold_quantile"] = summary["model_id"].map(lambda value: lookup[value]["threshold_quantile"])
        summary = summary.sort_values(["mean_net_return", "trades"], ascending=[False, False], kind="mergesort").reset_index(drop=True)
    risk = risk_summary(trades)
    comparison = baseline_comparison(summary, phase25_summary)
    candidates = edge_candidate_summary(comparison, risk)
    family = feature_family_summary(candidates)
    rejection = rejection_ledger(candidates)
    overall = overall_summary(catalog, summary, candidates, rejection)

    pq.write_table(pa.Table.from_pandas(trades, preserve_index=False), output_dir / "feature_edge_trade_ledger.parquet", compression="zstd")
    catalog.to_csv(output_dir / "feature_edge_candidate_catalog.csv", index=False)
    summary.to_csv(output_dir / "feature_edge_summary.csv", index=False)
    risk.to_csv(output_dir / "feature_edge_risk_summary.csv", index=False)
    comparison.to_csv(output_dir / "feature_edge_baseline_comparison.csv", index=False)
    candidates.to_csv(output_dir / "feature_edge_candidate_summary.csv", index=False)
    family.to_csv(output_dir / "feature_edge_family_summary.csv", index=False)
    rejection.to_csv(output_dir / "feature_edge_rejection_ledger.csv", index=False)
    overall.to_csv(output_dir / "feature_edge_overall_summary.csv", index=False)
    write_report(output_dir, overall, family, candidates, rejection, catalog)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "event_feature_rows": int(len(base_features)),
        "candidate_rows": int(len(catalog)),
        "candidate_profile_rows": int(len(summary)),
        "trade_rows": int(len(trades)),
        "realistic_cost_clearing_rows": int(candidates["realistic_cost_clearing_edge"].sum()) if len(candidates) else 0,
        "scope": "phase27_feature_edge_cost_hurdle_scan_not_acceptance_evidence",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase27",
            generated_utc=generated_utc,
            inputs={
                "event_features": str(event_features_path),
                "phase25_baseline_summary": str(phase25_summary_path),
                "execution_profiles": "src.synthetic_l2.phase12_execution_simulator.EXECUTION_PROFILES",
            },
            parameters={
                "feature_specs": FEATURE_SPECS,
                "horizon_events": HORIZON_EVENTS,
                "threshold_quantiles": THRESHOLD_QUANTILES,
                "min_trades_for_edge": MIN_TRADES_FOR_EDGE,
            },
            outputs={
                "trade_ledger": str(output_dir / "feature_edge_trade_ledger.parquet"),
                "candidate_catalog": str(output_dir / "feature_edge_candidate_catalog.csv"),
                "summary": str(output_dir / "feature_edge_summary.csv"),
                "risk_summary": str(output_dir / "feature_edge_risk_summary.csv"),
                "baseline_comparison": str(output_dir / "feature_edge_baseline_comparison.csv"),
                "candidate_summary": str(output_dir / "feature_edge_candidate_summary.csv"),
                "family_summary": str(output_dir / "feature_edge_family_summary.csv"),
                "rejection_ledger": str(output_dir / "feature_edge_rejection_ledger.csv"),
                "overall_summary": str(output_dir / "feature_edge_overall_summary.csv"),
                "report": str(output_dir / "phase27_feature_edge_scan_report.md"),
                "manifest": str(output_dir / "phase27_feature_edge_scan_manifest.json"),
            },
            random_seed="none_deterministic_feature_grid",
            scenario_ids="stage_b2_event_ordered_development_subset",
            cost_model_version="zerodha_equity_intraday_nse_order_formula_v2_2026_07_14",
            latency_model_version="phase12_execution_profiles_event_latency_counts",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase27_feature_edge_scan_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 27 event-feature edge cost-hurdle scan.")
    parser.add_argument("--event-features", type=Path, default=Path("outputs/stage_b2/stage_b2_event_feature_panel.parquet"))
    parser.add_argument("--phase25-summary", type=Path, default=Path("outputs/phase25/event_replay_summary.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase27"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase27(args.event_features, args.phase25_summary, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
