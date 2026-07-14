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


STRATEGY_IDS = ["S01", "S02", "S05", "S07", "S09"]
THRESHOLD_QUANTILES = [0.50, 0.70, 0.85, 0.95]
SPREAD_LIMIT_QUANTILES = [0.50, 0.80, 1.00]
LIQUIDITY_FILTERS = ["none", "above_median"]
MIN_TRADES_FOR_CANDIDATE = 50


def _abs_threshold(features: pd.DataFrame, column: str, quantile: float) -> float:
    values = features[column].astype(float).abs().replace([np.inf, -np.inf], np.nan).dropna()
    if values.empty:
        return 0.0
    return float(values.quantile(quantile))


def _base_signal(features: pd.DataFrame, strategy_id: str, threshold_quantile: float) -> pd.Series:
    nontrend = ~features["regime_code"].astype(str).isin(["D03", "D04", "D05", "D06"])
    if strategy_id == "S01":
        threshold = _abs_threshold(features, "momentum_3_event", threshold_quantile)
        signal = np.sign(features["momentum_3_event"]).where(
            (features["momentum_3_event"].abs() >= threshold)
            & (np.sign(features["momentum_3_event"]) == np.sign(features["mlofi_qty_event"])),
            0,
        )
    elif strategy_id == "S02":
        threshold = _abs_threshold(features, "mlofi_qty_event", threshold_quantile)
        signal = np.sign(features["mlofi_qty_event"]).where(features["mlofi_qty_event"].abs() >= threshold, 0)
    elif strategy_id == "S05":
        threshold = _abs_threshold(features, "microprice_dev", threshold_quantile)
        signal = np.sign(features["microprice_dev"]).where(features["microprice_dev"].abs() >= threshold, 0)
    elif strategy_id == "S07":
        threshold = _abs_threshold(features, "l5_imbalance", threshold_quantile)
        signal = -np.sign(features["l5_imbalance"]).where(nontrend & (features["l5_imbalance"].abs() >= threshold), 0)
    elif strategy_id == "S09":
        threshold = _abs_threshold(features, "l1_imbalance", threshold_quantile)
        signal = np.sign(features["l1_imbalance"]).where(features["l1_imbalance"].abs() >= threshold, 0)
    else:
        raise ValueError(f"Unsupported strategy_id: {strategy_id}")
    return pd.Series(signal, index=features.index).fillna(0).astype("int8")


def build_variant_catalog(features: pd.DataFrame) -> pd.DataFrame:
    rows = []
    median_liquidity = float(features["liquidity_score"].median())
    for strategy_id in STRATEGY_IDS:
        for threshold_quantile in THRESHOLD_QUANTILES:
            for spread_limit_quantile in SPREAD_LIMIT_QUANTILES:
                spread_limit = float(features["spread_ticks"].quantile(spread_limit_quantile))
                for liquidity_filter in LIQUIDITY_FILTERS:
                    min_liquidity = 0.0 if liquidity_filter == "none" else median_liquidity
                    variant_id = (
                        f"{strategy_id}_q{int(threshold_quantile * 100):02d}"
                        f"_sp{int(spread_limit_quantile * 100):03d}"
                        f"_liq{'med' if liquidity_filter == 'above_median' else 'all'}"
                    )
                    rows.append(
                        {
                            "variant_id": variant_id,
                            "parent_strategy_id": strategy_id,
                            "threshold_quantile": threshold_quantile,
                            "spread_limit_quantile": spread_limit_quantile,
                            "spread_tick_limit": spread_limit,
                            "liquidity_filter": liquidity_filter,
                            "min_liquidity_score": min_liquidity,
                            "variant_scope": "phase26_parameter_salvage_scan_not_acceptance",
                        }
                    )
    return pd.DataFrame(rows)


def build_variant_signal(features: pd.DataFrame, variant: dict) -> pd.Series:
    signal = _base_signal(features, str(variant["parent_strategy_id"]), float(variant["threshold_quantile"]))
    tradable = features["spread_ticks"].astype(float) <= float(variant["spread_tick_limit"])
    tradable &= features["liquidity_score"].astype(float) >= float(variant["min_liquidity_score"])
    tradable &= ~features["is_disconnect_gap"].astype(bool)
    tradable &= ~features["is_duplicate"].astype(bool)
    tradable &= ~features["is_out_of_order_injected"].astype(bool)
    return signal.where(tradable, 0).fillna(0).astype("int8")


def compare_to_baselines(summary: pd.DataFrame, baseline_summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for row in summary.to_dict("records"):
        comp = baseline_summary[baseline_summary["execution_profile"].eq(row["execution_profile"])]
        best_baseline = float(comp["mean_net_return"].max()) if len(comp) else np.nan
        rows.append(
            {
                "variant_id": row["model_id"],
                "parent_strategy_id": row["parent_strategy_id"],
                "execution_profile": row["execution_profile"],
                "trades": int(row["trades"]),
                "mean_gross_return": float(row["mean_gross_return"]),
                "mean_cost_return": float(row["mean_cost_return"]),
                "mean_net_return": float(row["mean_net_return"]),
                "total_net_pnl_inr": float(row["total_net_pnl_inr"]),
                "best_baseline_mean_net_return": best_baseline,
                "net_return_lift_vs_best_baseline": float(row["mean_net_return"] - best_baseline) if pd.notna(best_baseline) else np.nan,
                "positive_after_costs": bool(row["mean_net_return"] > 0.0),
                "beats_best_baseline_proxy": bool(row["mean_net_return"] > best_baseline) if pd.notna(best_baseline) else False,
                "enough_trades_for_candidate": bool(row["trades"] >= MIN_TRADES_FOR_CANDIDATE),
            }
        )
    return pd.DataFrame(rows)


def candidate_summary(comparison: pd.DataFrame, risk: pd.DataFrame) -> pd.DataFrame:
    if comparison.empty:
        return pd.DataFrame()
    merged = comparison.merge(
        risk[["model_id", "execution_profile", "risk_status"]],
        left_on=["variant_id", "execution_profile"],
        right_on=["model_id", "execution_profile"],
        how="left",
    ).drop(columns=["model_id"])
    merged["risk_not_breached_proxy"] = merged["risk_status"].astype(str).eq("risk_not_breached_proxy")
    merged["realistic_charged_profile"] = ~merged["execution_profile"].astype(str).eq("zero_latency_spread_only_control")
    merged["salvage_candidate_proxy"] = (
        merged["realistic_charged_profile"]
        & merged["positive_after_costs"]
        & merged["beats_best_baseline_proxy"]
        & merged["enough_trades_for_candidate"]
        & merged["risk_not_breached_proxy"]
    )
    merged["zero_latency_positive_control"] = (
        ~merged["realistic_charged_profile"]
        & merged["positive_after_costs"]
        & merged["beats_best_baseline_proxy"]
        & merged["enough_trades_for_candidate"]
        & merged["risk_not_breached_proxy"]
    )
    return merged.sort_values(
        ["salvage_candidate_proxy", "mean_net_return", "net_return_lift_vs_best_baseline"],
        ascending=[False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def rejection_ledger(candidates: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for row in candidates.to_dict("records"):
        reasons = []
        if not row["positive_after_costs"]:
            reasons.append("net_return_not_positive_after_costs")
        if not row["realistic_charged_profile"]:
            reasons.append("zero_latency_control_not_retail_survivor")
        if not row["beats_best_baseline_proxy"]:
            reasons.append("does_not_beat_best_baseline_proxy")
        if not row["enough_trades_for_candidate"]:
            reasons.append("insufficient_trade_count")
        if not row["risk_not_breached_proxy"]:
            reasons.append("proxy_risk_breached_or_missing")
        if not reasons:
            reasons.append("candidate_for_deeper_event_replay_not_acceptance")
        rows.append(
            {
                "variant_id": row["variant_id"],
                "parent_strategy_id": row["parent_strategy_id"],
                "execution_profile": row["execution_profile"],
                "rejection_reasons": ";".join(reasons),
                "salvage_candidate_proxy": bool(row["salvage_candidate_proxy"]),
                "phase26_scope": "parameter_salvage_scan_not_acceptance",
            }
        )
    return pd.DataFrame(rows)


def overall_summary(catalog: pd.DataFrame, summary: pd.DataFrame, candidates: pd.DataFrame, rejection: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"metric": "phase26_variants_registered", "value": int(len(catalog)), "description": "Strategy parameter/filter variants registered"},
            {"metric": "phase26_variant_profile_rows", "value": int(len(summary)), "description": "Variant/profile replay summary rows"},
            {"metric": "phase26_total_replay_trades", "value": int(summary["trades"].sum()) if len(summary) else 0, "description": "Total trades across all variant/profile replays"},
            {"metric": "phase26_positive_after_cost_rows", "value": int(candidates["positive_after_costs"].sum()) if len(candidates) else 0, "description": "Variant/profile rows with positive mean net return after costs"},
            {"metric": "phase26_realistic_positive_after_cost_rows", "value": int((candidates["realistic_charged_profile"] & candidates["positive_after_costs"]).sum()) if len(candidates) else 0, "description": "Retail/stressed rows with positive mean net return after Zerodha-style costs"},
            {"metric": "phase26_zero_latency_positive_control_rows", "value": int(candidates["zero_latency_positive_control"].sum()) if len(candidates) else 0, "description": "Frictionless control rows that are positive but not retail survivors"},
            {"metric": "phase26_beats_best_baseline_rows", "value": int(candidates["beats_best_baseline_proxy"].sum()) if len(candidates) else 0, "description": "Variant/profile rows beating best baseline proxy"},
            {"metric": "phase26_salvage_candidate_rows", "value": int(candidates["salvage_candidate_proxy"].sum()) if len(candidates) else 0, "description": "Rows passing positive net, baseline, trade-count and proxy-risk filters"},
            {"metric": "phase26_rejected_rows", "value": int((~rejection["salvage_candidate_proxy"]).sum()) if len(rejection) else 0, "description": "Variant/profile rows rejected by at least one diagnostic"},
            {"metric": "phase26_acceptance_ready", "value": 0, "description": "Parameter scan is execution diagnostic evidence, not acceptance evidence"},
        ]
    )


def write_report(
    output_dir: Path,
    overall: pd.DataFrame,
    catalog: pd.DataFrame,
    summary: pd.DataFrame,
    candidates: pd.DataFrame,
    rejection: pd.DataFrame,
) -> None:
    lines = [
        "# Phase 26 Strategy Salvage Scan",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This milestone answers the immediate post-Phase-25 question: do simple threshold, spread and liquidity filters salvage any event-order strategy after realistic costs?",
        "It is an execution diagnostic and rejection/salvage screen, not a promotion or acceptance result.",
        "",
        "## Overall Summary",
        "",
        _markdown_table(overall),
        "",
        "## Top Candidate Rows",
        "",
        _markdown_table(candidates.head(25)),
        "",
        "## Rejection Ledger",
        "",
        _markdown_table(rejection.head(50)),
        "",
        "## Variant Catalog",
        "",
        _markdown_table(catalog.head(50)),
        "",
        "## Replay Summary",
        "",
        _markdown_table(summary.head(50)),
        "",
    ]
    (output_dir / "phase26_strategy_salvage_scan_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase26(event_features_path: Path, phase25_summary_path: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    features = load_event_features(event_features_path)
    catalog = build_variant_catalog(features)
    baseline_summary = pd.read_csv(phase25_summary_path)
    baseline_summary = baseline_summary[baseline_summary["model_type"].eq("baseline")].copy()

    trade_frames = []
    for variant in catalog.to_dict("records"):
        signal = build_variant_signal(features, variant)
        for profile in EXECUTION_PROFILES:
            trades = simulate_signal(features, signal, str(variant["variant_id"]), "strategy_variant", profile)
            trades["parent_strategy_id"] = variant["parent_strategy_id"]
            trades["threshold_quantile"] = variant["threshold_quantile"]
            trades["spread_limit_quantile"] = variant["spread_limit_quantile"]
            trades["spread_tick_limit"] = variant["spread_tick_limit"]
            trades["liquidity_filter"] = variant["liquidity_filter"]
            trades["phase26_scope"] = "strategy_salvage_scan_not_acceptance"
            if not trades.empty:
                trade_frames.append(trades)
    trades = pd.concat(trade_frames, ignore_index=True) if trade_frames else pd.DataFrame()
    summary = summarize_trades(trades)
    if len(summary):
        parent_lookup = catalog.set_index("variant_id")["parent_strategy_id"].to_dict()
        summary["parent_strategy_id"] = summary["model_id"].map(parent_lookup)
        summary = summary.sort_values(["mean_net_return", "trades"], ascending=[False, False], kind="mergesort").reset_index(drop=True)
    risk = risk_summary(trades)
    comparison = compare_to_baselines(summary, baseline_summary)
    candidates = candidate_summary(comparison, risk)
    rejection = rejection_ledger(candidates)
    overall = overall_summary(catalog, summary, candidates, rejection)

    pq.write_table(pa.Table.from_pandas(trades, preserve_index=False), output_dir / "strategy_salvage_trade_ledger.parquet", compression="zstd")
    catalog.to_csv(output_dir / "strategy_salvage_variant_catalog.csv", index=False)
    summary.to_csv(output_dir / "strategy_salvage_summary.csv", index=False)
    risk.to_csv(output_dir / "strategy_salvage_risk_summary.csv", index=False)
    comparison.to_csv(output_dir / "strategy_salvage_baseline_comparison.csv", index=False)
    candidates.to_csv(output_dir / "strategy_salvage_candidate_summary.csv", index=False)
    rejection.to_csv(output_dir / "strategy_salvage_rejection_ledger.csv", index=False)
    overall.to_csv(output_dir / "strategy_salvage_overall_summary.csv", index=False)
    write_report(output_dir, overall, catalog, summary, candidates, rejection)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "event_feature_rows": int(len(features)),
        "variant_rows": int(len(catalog)),
        "variant_profile_rows": int(len(summary)),
        "trade_rows": int(len(trades)),
        "salvage_candidate_rows": int(candidates["salvage_candidate_proxy"].sum()) if len(candidates) else 0,
        "scope": "phase26_strategy_salvage_scan_not_acceptance_evidence",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase26",
            generated_utc=generated_utc,
            inputs={
                "event_features": str(event_features_path),
                "phase25_baseline_summary": str(phase25_summary_path),
                "execution_profiles": "src.synthetic_l2.phase12_execution_simulator.EXECUTION_PROFILES",
            },
            parameters={
                "strategy_ids": STRATEGY_IDS,
                "threshold_quantiles": THRESHOLD_QUANTILES,
                "spread_limit_quantiles": SPREAD_LIMIT_QUANTILES,
                "liquidity_filters": LIQUIDITY_FILTERS,
                "min_trades_for_candidate": MIN_TRADES_FOR_CANDIDATE,
            },
            outputs={
                "trade_ledger": str(output_dir / "strategy_salvage_trade_ledger.parquet"),
                "variant_catalog": str(output_dir / "strategy_salvage_variant_catalog.csv"),
                "summary": str(output_dir / "strategy_salvage_summary.csv"),
                "risk_summary": str(output_dir / "strategy_salvage_risk_summary.csv"),
                "baseline_comparison": str(output_dir / "strategy_salvage_baseline_comparison.csv"),
                "candidate_summary": str(output_dir / "strategy_salvage_candidate_summary.csv"),
                "rejection_ledger": str(output_dir / "strategy_salvage_rejection_ledger.csv"),
                "overall_summary": str(output_dir / "strategy_salvage_overall_summary.csv"),
                "report": str(output_dir / "phase26_strategy_salvage_scan_report.md"),
                "manifest": str(output_dir / "phase26_strategy_salvage_scan_manifest.json"),
            },
            random_seed="none_deterministic_parameter_grid",
            scenario_ids="stage_b2_event_ordered_development_subset",
            cost_model_version="zerodha_equity_intraday_nse_order_formula_v2_2026_07_14",
            latency_model_version="phase12_execution_profiles_event_latency_counts",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase26_strategy_salvage_scan_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 26 strategy parameter salvage scan over Stage B2 event features.")
    parser.add_argument("--event-features", type=Path, default=Path("outputs/stage_b2/stage_b2_event_feature_panel.parquet"))
    parser.add_argument("--phase25-summary", type=Path, default=Path("outputs/phase25/event_replay_summary.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase26"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase26(args.event_features, args.phase25_summary, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
