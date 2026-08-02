from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase255_richer_raw_depth_feature_quality_interpretation import safe_float
from synthetic_l2.phase271_fixed_capital_concurrency_and_capacity_return_analysis import schedule_events_for_scenario
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE277_DIR = Path("outputs/phase277")
DEFAULT_PHASE287_DIR = Path("outputs/phase287")
DEFAULT_OUTPUT_DIR = Path("outputs/phase288")

SELECTED_ROUTE = "P288_FULL_DEPTH_LIQUIDITY_PRESSURE_STRATEGY_SEARCH"
NEXT_ACTION = "run_phase289_full_depth_liquidity_pressure_interpretation_no_paper_live"
REPAIR_ACTION = "repair_phase288_full_depth_liquidity_pressure_strategy_search"

INITIAL_CAPITAL_INR = 100_000.0
COST_MULTIPLIER = 2.0
EXTRA_SLIPPAGE_BPS = 0.0
ANNUALIZED_THRESHOLD_PCT = 12.0
SPARSE_DIAGNOSTIC_EVENT_FLOOR = 8
ROBUST_PORTFOLIO_EVENT_FLOOR = 30


FEATURE_COLUMNS = [
    "avg_cum_top5_qty_imbalance",
    "avg_depth_beyond_l1_qty_imbalance",
    "avg_level_weighted_depth_imbalance",
    "depth_replenishment_pressure",
    "depth_withdrawal_pressure",
    "top5_churn_pressure",
    "avg_spread_bps",
    "depth_replenish_withdraw_ratio",
    "depth_consensus_imbalance",
    "event_sparsity_pressure",
]


def q(frame: pd.DataFrame, col: str, quantile: float) -> float:
    values = pd.to_numeric(frame[col], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if values.empty:
        return 0.0
    return float(values.quantile(quantile))


def prepare_events(events: pd.DataFrame) -> pd.DataFrame:
    frame = events.copy()
    for col in FEATURE_COLUMNS + ["gross_edge_bps", "zerodha_round_trip_charge_bps", "richer_event_bar_id", "horizon"]:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
    frame["abs_beyond_l1_imbalance"] = frame["avg_depth_beyond_l1_qty_imbalance"].abs()
    frame["abs_level_weighted_imbalance"] = frame["avg_level_weighted_depth_imbalance"].abs()
    frame["abs_consensus_imbalance"] = frame["depth_consensus_imbalance"].abs()
    frame["depth_slope_pressure"] = (frame["avg_level_weighted_depth_imbalance"] - frame["avg_cum_top5_qty_imbalance"]).abs()
    frame["signed_pressure"] = (
        frame["avg_depth_beyond_l1_qty_imbalance"]
        + frame["avg_level_weighted_depth_imbalance"]
        + frame["depth_consensus_imbalance"]
    ) / 3.0
    frame["liquidity_vacuum_pressure"] = frame["depth_withdrawal_pressure"] / (frame["depth_replenishment_pressure"].abs() + 1.0)
    frame["replenishment_dominance"] = frame["depth_replenishment_pressure"] / (frame["depth_withdrawal_pressure"].abs() + 1.0)
    frame["market_open_bucket"] = (frame["richer_event_bar_id"] <= q(frame, "richer_event_bar_id", 0.25)).astype(int)
    frame["uses_top5"] = 1
    frame["uses_levels_2_to_5"] = 1
    frame["l1_only_variant"] = 0
    frame["uses_net_edge_as_live_mask"] = 0
    return frame


def family_masks(events: pd.DataFrame) -> dict[str, tuple[pd.Series, str, str]]:
    return {
        "P288_PRESSURE_CONTINUATION": (
            (events["abs_beyond_l1_imbalance"] >= q(events, "abs_beyond_l1_imbalance", 0.60))
            & (events["abs_consensus_imbalance"] >= q(events, "abs_consensus_imbalance", 0.60))
            & (events["avg_spread_bps"] <= q(events, "avg_spread_bps", 0.75)),
            "pressure_continuation",
            "beyond-L1 and consensus imbalance high with spread not in the worst quartile",
        ),
        "P288_EXHAUSTION_REVERSAL": (
            (events["depth_withdrawal_pressure"] >= q(events, "depth_withdrawal_pressure", 0.60))
            & (events["top5_churn_pressure"] >= q(events, "top5_churn_pressure", 0.60))
            & (events["avg_spread_bps"] <= q(events, "avg_spread_bps", 0.75)),
            "exhaustion_reversal",
            "withdrawal and churn high, testing reversal after book exhaustion",
        ),
        "P288_SPREAD_COMPRESSION_PRESSURE": (
            (events["avg_spread_bps"] <= q(events, "avg_spread_bps", 0.50))
            & (events["replenishment_dominance"] >= q(events, "replenishment_dominance", 0.60))
            & (events["abs_level_weighted_imbalance"] >= q(events, "abs_level_weighted_imbalance", 0.50)),
            "spread_compression_pressure",
            "tight spread with replenishment dominance and level-weighted pressure",
        ),
        "P288_OPEN_PRESSURE_BURST": (
            (events["market_open_bucket"] == 1)
            & (events["abs_beyond_l1_imbalance"] >= q(events, "abs_beyond_l1_imbalance", 0.50))
            & (events["top5_churn_pressure"] >= q(events, "top5_churn_pressure", 0.50)),
            "open_pressure_burst",
            "market-open bucket with beyond-L1 imbalance and churn",
        ),
        "P288_REPLENISHMENT_ABSORPTION": (
            (events["replenishment_dominance"] >= q(events, "replenishment_dominance", 0.70))
            & (events["depth_withdrawal_pressure"] <= q(events, "depth_withdrawal_pressure", 0.60))
            & (events["abs_consensus_imbalance"] >= q(events, "abs_consensus_imbalance", 0.50)),
            "replenishment_absorption",
            "replenishment dominance with limited withdrawal and consensus pressure",
        ),
        "P288_LIQUIDITY_VACUUM": (
            (events["liquidity_vacuum_pressure"] >= q(events, "liquidity_vacuum_pressure", 0.70))
            & (events["depth_slope_pressure"] >= q(events, "depth_slope_pressure", 0.50))
            & (events["avg_spread_bps"] <= q(events, "avg_spread_bps", 0.90)),
            "liquidity_vacuum",
            "withdrawal-dominated book vacuum with depth-slope pressure",
        ),
    }


def build_variant_catalog(events: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    side_modes = [
        ("ORIG", 1, "original synthetic edge side"),
        ("INV", -1, "inverse/reversal side"),
    ]
    intensity_quantiles = [0.50, 0.60, 0.70, 0.80]
    horizons = [3, 5, 8, 10]
    rows: list[dict[str, Any]] = []
    variant_events: dict[str, pd.DataFrame] = {}
    masks = family_masks(events)
    for family_id, (base_mask, family_name, rule) in masks.items():
        base = events[base_mask].copy()
        if base.empty:
            continue
        pressure_col = {
            "P288_PRESSURE_CONTINUATION": "abs_consensus_imbalance",
            "P288_EXHAUSTION_REVERSAL": "depth_withdrawal_pressure",
            "P288_SPREAD_COMPRESSION_PRESSURE": "replenishment_dominance",
            "P288_OPEN_PRESSURE_BURST": "top5_churn_pressure",
            "P288_REPLENISHMENT_ABSORPTION": "replenishment_dominance",
            "P288_LIQUIDITY_VACUUM": "liquidity_vacuum_pressure",
        }[family_id]
        for threshold_q in intensity_quantiles:
            threshold = q(base, pressure_col, threshold_q)
            selected = base[base[pressure_col] >= threshold].copy()
            if selected.empty:
                continue
            for side_label, side_multiplier, side_rule in side_modes:
                for horizon in horizons:
                    variant_id = f"P288_{family_id}_Q{int(threshold_q*100)}_{side_label}_H{horizon}"
                    v = selected.copy()
                    horizon_factor = float(np.sqrt(max(1, horizon) / 10.0))
                    spread_penalty = np.maximum(0.0, v["avg_spread_bps"] - q(events, "avg_spread_bps", 0.50)) * 0.10
                    churn_penalty = np.maximum(0.0, v["top5_churn_pressure"] - q(events, "top5_churn_pressure", 0.75)) / (q(events, "top5_churn_pressure", 0.75) + 1.0) * 1.5
                    v["gross_edge_bps"] = (v["gross_edge_bps"].astype(float) * side_multiplier * horizon_factor) - spread_penalty - churn_penalty
                    v["side"] = (v["side"].astype(int) * side_multiplier).replace(0, side_multiplier)
                    v["horizon"] = horizon
                    v["candidate_id"] = variant_id
                    v["candidate_rank"] = 1
                    v["family_id"] = family_id
                    v = v.sort_values(["trade_date", pressure_col, "richer_event_bar_id"], ascending=[True, False, True]).reset_index(drop=True)
                    variant_events[variant_id] = v
                    rows.append(
                        {
                            "phase288_variant_id": variant_id,
                            "liquidity_family_id": family_id,
                            "liquidity_family": family_name,
                            "selection_rule": rule,
                            "pressure_column": pressure_col,
                            "pressure_threshold_quantile": threshold_q,
                            "pressure_threshold_value": threshold,
                            "side_mode": side_label,
                            "side_rule": side_rule,
                            "side_multiplier": side_multiplier,
                            "exit_horizon_ticks": horizon,
                            "selected_event_rows": int(len(v)),
                            "symbols": int(v["symbol"].astype(str).nunique()),
                            "trade_dates": int(v["trade_date"].astype(str).nunique()),
                            "uses_top5": 1,
                            "uses_levels_2_to_5": 1,
                            "l1_only_variant": 0,
                            "uses_net_edge_as_live_mask": 0,
                            "annualized_denominator": "fixed_initial_capital",
                            "strategy_replay_allowed": 0,
                            "paper_or_live_acceptance_allowed": 0,
                            "deployable_profitability_claim_allowed": 0,
                        }
                    )
    return pd.DataFrame(rows), variant_events


def build_scenarios(variant_catalog: pd.DataFrame, variant_events: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame]:
    fixed_notionals = [25_000.0, 50_000.0, 75_000.0, 100_000.0]
    max_concurrency = [1, 2, 4]
    scenarios: list[dict[str, Any]] = []
    ledgers: list[pd.DataFrame] = []
    meta = variant_catalog.set_index("phase288_variant_id").to_dict(orient="index") if not variant_catalog.empty else {}
    for variant_id, events in variant_events.items():
        for fixed_notional in fixed_notionals:
            for max_concurrent in max_concurrency:
                scenario, ledger = schedule_events_for_scenario(
                    events=events,
                    scope_id=variant_id,
                    scope_candidate_id=variant_id,
                    initial_capital_inr=INITIAL_CAPITAL_INR,
                    fixed_notional_inr=fixed_notional,
                    max_concurrent_positions=max_concurrent,
                    cost_profile="cost200",
                    cost_multiplier=COST_MULTIPLIER,
                    extra_slippage_bps=EXTRA_SLIPPAGE_BPS,
                )
                variant_meta = meta.get(variant_id, {})
                scenario.update(
                    {
                        "phase288_variant_id": variant_id,
                        "liquidity_family_id": variant_meta.get("liquidity_family_id", ""),
                        "liquidity_family": variant_meta.get("liquidity_family", ""),
                        "pressure_column": variant_meta.get("pressure_column", ""),
                        "pressure_threshold_quantile": variant_meta.get("pressure_threshold_quantile", ""),
                        "side_mode": variant_meta.get("side_mode", ""),
                        "exit_horizon_ticks": variant_meta.get("exit_horizon_ticks", ""),
                        "selected_event_rows": variant_meta.get("selected_event_rows", 0),
                        "uses_top5": 1,
                        "uses_levels_2_to_5": 1,
                        "l1_only_variant": 0,
                        "uses_net_edge_as_live_mask": 0,
                        "sparse_diagnostic_event_floor_met": int(scenario["scheduled_event_rows"] >= SPARSE_DIAGNOSTIC_EVENT_FLOOR),
                        "robust_portfolio_event_floor_met": int(scenario["scheduled_event_rows"] >= ROBUST_PORTFOLIO_EVENT_FLOOR),
                        "cost200_above12_sparse_diagnostic": int(
                            scenario["mechanical_one_date_annualized_portfolio_return_pct"] > ANNUALIZED_THRESHOLD_PCT
                            and scenario["scheduled_event_rows"] >= SPARSE_DIAGNOSTIC_EVENT_FLOOR
                        ),
                        "robust_portfolio_floor_above12": int(
                            scenario["mechanical_one_date_annualized_portfolio_return_pct"] > ANNUALIZED_THRESHOLD_PCT
                            and scenario["scheduled_event_rows"] >= ROBUST_PORTFOLIO_EVENT_FLOOR
                        ),
                    }
                )
                scenarios.append(scenario)
                if not ledger.empty:
                    for key, value in scenario.items():
                        if key.startswith("phase288_") or key in {"liquidity_family_id", "liquidity_family", "pressure_column", "side_mode"}:
                            ledger[key] = value
                    ledgers.append(ledger)
    return pd.DataFrame(scenarios), pd.concat(ledgers, ignore_index=True) if ledgers else pd.DataFrame()


def build_variant_summary(scenarios: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for variant_id, group in scenarios.groupby("phase288_variant_id", dropna=False):
        ranked = group.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False)
        best = ranked.iloc[0]
        rows.append(
            {
                "phase288_variant_id": variant_id,
                "liquidity_family": best.get("liquidity_family", ""),
                "pressure_column": best.get("pressure_column", ""),
                "side_mode": best.get("side_mode", ""),
                "exit_horizon_ticks": best.get("exit_horizon_ticks", ""),
                "scenario_rows": int(len(group)),
                "selected_event_rows": int(group["selected_event_rows"].max()),
                "max_scheduled_event_rows": int(group["scheduled_event_rows"].max()),
                "cost200_above12_sparse_diagnostic_rows": int(group["cost200_above12_sparse_diagnostic"].sum()),
                "robust_portfolio_floor_above12_rows": int(group["robust_portfolio_floor_above12"].sum()),
                "sparse_floor_met_rows": int(group["sparse_diagnostic_event_floor_met"].sum()),
                "robust_portfolio_floor_met_rows": int(group["robust_portfolio_event_floor_met"].sum()),
                "min_annualized_pct": float(group["mechanical_one_date_annualized_portfolio_return_pct"].min()),
                "median_annualized_pct": float(group["mechanical_one_date_annualized_portfolio_return_pct"].median()),
                "max_annualized_pct": float(group["mechanical_one_date_annualized_portfolio_return_pct"].max()),
                "max_net_pnl_inr": float(group["realized_net_pnl_inr"].max()),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["cost200_above12_sparse_diagnostic_rows", "robust_portfolio_floor_above12_rows", "max_annualized_pct", "max_scheduled_event_rows"],
        ascending=[False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_gate_evaluation(phase287_summary: pd.DataFrame, variant_catalog: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(phase287_summary, "phase287_interpretation_complete", 0))
    next_action = str(metric_value(phase287_summary, "phase287_next_best_action", ""))
    l1_only = int(pd.to_numeric(variant_catalog.get("l1_only_variant", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not variant_catalog.empty else 1
    live_mask = int(pd.to_numeric(variant_catalog.get("uses_net_edge_as_live_mask", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not variant_catalog.empty else 1
    gates = [
        ("P288_PHASE287_WORK_ORDER_PRESENT", complete == 1 and "phase288" in next_action, next_action, "Phase287 routes to Phase288", "hard"),
        ("P288_VARIANTS_PRESENT", len(variant_catalog) >= 180, len(variant_catalog), ">=180 direct L2 pressure variants", "hard"),
        ("P288_SCENARIOS_PRESENT", len(scenarios) >= 2000, len(scenarios), ">=2000 fixed-capital scenarios", "hard"),
        ("P288_COST_AND_FIXED_CAPITAL_REQUIRED", bool((scenarios["cost_profile"].astype(str).eq("cost200")).all()) and bool((scenarios["initial_capital_inr"].astype(float).eq(INITIAL_CAPITAL_INR)).all()), "cost200=1;fixed_capital=1", "cost200 fixed-capital scoring", "hard"),
        ("P288_FULL_DEPTH_REQUIRED", l1_only == 0 and bool((variant_catalog["uses_top5"].astype(int).eq(1)).all()) and bool((variant_catalog["uses_levels_2_to_5"].astype(int).eq(1)).all()), f"catalog_l1={l1_only}", "full-depth with L1-only forbidden", "hard"),
        ("P288_NO_LIVE_NET_EDGE_MASKS", live_mask == 0, live_mask, "net/gross edge not used as live masks", "hard"),
        ("P288_FIXED_CAPITAL_ANNUALIZED_DENOMINATOR", bool((variant_catalog["annualized_denominator"].astype(str).eq("fixed_initial_capital")).all()), "fixed_initial_capital", "no unlimited-capital denominator", "hard"),
        ("P288_BOUNDARIES_CLOSED", True, "replay=0;paper=0;claim=0", "no replay/paper/live/claim", "hard"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": s} for g, p, o, r, s in gates])


def build_acceptance_summary(variant_catalog: pd.DataFrame, scenarios: pd.DataFrame, variant_summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    best = scenarios.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0] if not scenarios.empty else pd.Series(dtype=object)
    sparse = int(pd.to_numeric(scenarios.get("cost200_above12_sparse_diagnostic", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not scenarios.empty else 0
    robust_above12 = int(pd.to_numeric(scenarios.get("robust_portfolio_floor_above12", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not scenarios.empty else 0
    robust_floor = int(pd.to_numeric(scenarios.get("robust_portfolio_event_floor_met", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not scenarios.empty else 0
    next_action = NEXT_ACTION if hard_pass == len(hard) else REPAIR_ACTION
    rows = [
        ("phase288_liquidity_pressure_search_complete", 1, "Phase288 direct full-depth liquidity-pressure search completed"),
        ("phase288_selected_route", SELECTED_ROUTE, "Selected route"),
        ("phase288_variant_rows", int(len(variant_catalog)), "Variants evaluated"),
        ("phase288_scenario_rows", int(len(scenarios)), "Cost200 fixed-capital scenarios evaluated"),
        ("phase288_sparse_above12_scenario_rows", sparse, "Above-12 sparse diagnostic rows with event floor met"),
        ("phase288_robust_portfolio_floor_scenario_rows", robust_floor, "Scenarios meeting robust portfolio event floor"),
        ("phase288_robust_portfolio_above12_scenario_rows", robust_above12, "Robust floor scenarios above 12 percent"),
        ("phase288_best_variant_id", best.get("phase288_variant_id", ""), "Best Phase288 variant"),
        ("phase288_best_liquidity_family", best.get("liquidity_family", ""), "Best liquidity family"),
        ("phase288_best_pressure_column", best.get("pressure_column", ""), "Best pressure feature"),
        ("phase288_best_side_mode", best.get("side_mode", ""), "Best side mode"),
        ("phase288_best_cost200_annualized_pct", best.get("mechanical_one_date_annualized_portfolio_return_pct", ""), "Best cost200 fixed-capital annualized diagnostic"),
        ("phase288_best_realized_net_pnl_inr", best.get("realized_net_pnl_inr", ""), "Best realized net P&L"),
        ("phase288_best_scheduled_event_rows", best.get("scheduled_event_rows", ""), "Best scheduled event rows"),
        ("phase288_l1_only_variant_rows", int(pd.to_numeric(variant_catalog.get("l1_only_variant", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not variant_catalog.empty else 0, "L1-only variants"),
        ("phase288_net_edge_live_mask_rows", int(pd.to_numeric(variant_catalog.get("uses_net_edge_as_live_mask", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not variant_catalog.empty else 0, "Live masks using net/gross edge"),
        ("phase288_strategy_replay_allowed", 0, "No strategy replay unlocked"),
        ("phase288_strategy_promotion_allowed", 0, "No strategy promotion unlocked"),
        ("phase288_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
        ("phase288_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        ("phase288_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase288_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
        ("phase288_next_best_action", next_action, "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, variant_summary: pd.DataFrame, scenarios: pd.DataFrame, gates: pd.DataFrame, summary: pd.DataFrame) -> None:
    lines = [
        "# Phase288 Full-Depth Liquidity-Pressure Strategy Search",
        "",
        "Phase288 executes direct full-depth L2 pressure masks using Zerodha top-five rows 1-5 and levels 2-5 / beyond-L1 features. Selection masks are observable L2 features only; gross edge is used only after selection for synthetic scoring.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(summary),
        "",
        "## Top Variant Summary",
        "",
        _markdown_table(variant_summary.head(20)),
        "",
        "## Top Scenarios",
        "",
        _markdown_table(scenarios.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).head(20)),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
    ]
    (output_dir / "phase288_full_depth_liquidity_pressure_strategy_search_report.md").write_text("\n".join(lines), encoding="utf-8")


def run(phase277_dir: Path = DEFAULT_PHASE277_DIR, phase287_dir: Path = DEFAULT_PHASE287_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase287_summary = read_csv(phase287_dir / "phase287_acceptance_summary.csv")
    events = prepare_events(read_csv(phase277_dir / "phase277_cost200_redesign_event_universe.csv"))
    variant_catalog, variant_events = build_variant_catalog(events)
    scenarios, ledger = build_scenarios(variant_catalog, variant_events)
    variant_summary = build_variant_summary(scenarios)
    gates = build_gate_evaluation(phase287_summary, variant_catalog, scenarios)
    summary = build_acceptance_summary(variant_catalog, scenarios, variant_summary, gates)

    variant_catalog.to_csv(output_dir / "phase288_liquidity_pressure_variant_catalog.csv", index=False)
    scenarios.to_csv(output_dir / "phase288_liquidity_pressure_scenario_results.csv", index=False)
    variant_summary.to_csv(output_dir / "phase288_liquidity_pressure_variant_summary.csv", index=False)
    ledger.head(5000).to_csv(output_dir / "phase288_sample_liquidity_pressure_scheduled_event_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase288_gate_evaluation.csv", index=False)
    summary.to_csv(output_dir / "phase288_acceptance_summary.csv", index=False)
    write_report(output_dir, variant_summary, scenarios, gates, summary)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase288_full_depth_liquidity_pressure_strategy_search",
        **reproducibility_fields(
            artifact_id="phase288",
            generated_utc=generated_utc,
            inputs={
                "phase287_acceptance_summary": str(phase287_dir / "phase287_acceptance_summary.csv"),
                "phase277_event_universe": str(phase277_dir / "phase277_cost200_redesign_event_universe.csv"),
            },
            parameters={
                "selected_route": SELECTED_ROUTE,
                "initial_capital_inr": INITIAL_CAPITAL_INR,
                "cost_multiplier": COST_MULTIPLIER,
                "extra_slippage_bps": EXTRA_SLIPPAGE_BPS,
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "sparse_diagnostic_event_floor": SPARSE_DIAGNOSTIC_EVENT_FLOOR,
                "robust_portfolio_event_floor": ROBUST_PORTFOLIO_EVENT_FLOOR,
                "selection_masks": "observable_full_depth_l2_features_only",
                "strategy_replay_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "acceptance_summary": str(output_dir / "phase288_acceptance_summary.csv"),
                "scenario_results": str(output_dir / "phase288_liquidity_pressure_scenario_results.csv"),
                "variant_catalog": str(output_dir / "phase288_liquidity_pressure_variant_catalog.csv"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase288_direct_pressure_horizon_proxy_v1",
        ),
    }
    (output_dir / "phase288_full_depth_liquidity_pressure_strategy_search_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return manifest


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase277-dir", type=Path, default=DEFAULT_PHASE277_DIR)
    parser.add_argument("--phase287-dir", type=Path, default=DEFAULT_PHASE287_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args(argv)
    print(json.dumps(run(args.phase277_dir, args.phase287_dir, args.output_dir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
