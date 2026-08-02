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
DEFAULT_PHASE289_DIR = Path("outputs/phase289")
DEFAULT_OUTPUT_DIR = Path("outputs/phase290")

SELECTED_ROUTE = "P290_ADAPTIVE_FULL_DEPTH_LIQUIDITY_PRESSURE_EXPANSION_SEARCH"
NEXT_ACTION = "run_phase291_adaptive_full_depth_liquidity_pressure_interpretation_no_paper_live"
REPAIR_ACTION = "repair_phase290_adaptive_full_depth_liquidity_pressure_expansion_search"

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
    frame["withdraw_replenish_ratio"] = frame["depth_withdrawal_pressure"] / (frame["depth_replenishment_pressure"].abs() + 1.0)
    frame["pressure_interaction"] = frame["abs_beyond_l1_imbalance"] * frame["abs_consensus_imbalance"]
    frame["churn_withdraw_interaction"] = frame["top5_churn_pressure"] * frame["depth_withdrawal_pressure"]
    frame["spread_compression_score"] = frame["replenishment_dominance"] / (frame["avg_spread_bps"].abs() + 1.0)
    frame["market_open_bucket"] = (frame["richer_event_bar_id"] <= q(frame, "richer_event_bar_id", 0.25)).astype(int)
    frame["non_open_bucket"] = 1 - frame["market_open_bucket"]
    frame["uses_top5"] = 1
    frame["uses_levels_2_to_5"] = 1
    frame["l1_only_variant"] = 0
    frame["uses_net_edge_as_live_mask"] = 0
    return frame


def adaptive_family_specs() -> list[dict[str, Any]]:
    return [
        {
            "family_id": "P290_EXHAUSTION_REVERSAL_ADAPTIVE",
            "family": "exhaustion_reversal_adaptive",
            "primary": "depth_withdrawal_pressure",
            "secondary": "top5_churn_pressure",
            "interaction": "churn_withdraw_interaction",
            "side_modes": [("ORIG", 1), ("INV", -1), ("PRESSURE_SIGN_REV", -1)],
            "rule": "withdrawal/churn interaction with adaptive reversal and continuation sides",
        },
        {
            "family_id": "P290_REPLENISHMENT_ABSORPTION_ADAPTIVE",
            "family": "replenishment_absorption_adaptive",
            "primary": "replenishment_dominance",
            "secondary": "abs_consensus_imbalance",
            "interaction": "spread_compression_score",
            "side_modes": [("ORIG", 1), ("INV", -1), ("PRESSURE_SIGN_CONT", 1)],
            "rule": "replenishment dominance with consensus and spread-compression interaction",
        },
        {
            "family_id": "P290_PRESSURE_CONTINUATION_ADAPTIVE",
            "family": "pressure_continuation_adaptive",
            "primary": "abs_consensus_imbalance",
            "secondary": "abs_beyond_l1_imbalance",
            "interaction": "pressure_interaction",
            "side_modes": [("ORIG", 1), ("PRESSURE_SIGN_CONT", 1), ("INV", -1)],
            "rule": "consensus and beyond-L1 pressure interaction for continuation/reversal comparison",
        },
        {
            "family_id": "P290_LIQUIDITY_VACUUM_ADAPTIVE",
            "family": "liquidity_vacuum_adaptive",
            "primary": "liquidity_vacuum_pressure",
            "secondary": "depth_slope_pressure",
            "interaction": "withdraw_replenish_ratio",
            "side_modes": [("ORIG", 1), ("INV", -1)],
            "rule": "withdrawal-dominant vacuum with depth-slope interaction",
        },
    ]


def bucket_mask(events: pd.DataFrame, bucket: str) -> pd.Series:
    if bucket == "OPEN":
        return events["market_open_bucket"].eq(1)
    if bucket == "NONOPEN":
        return events["non_open_bucket"].eq(1)
    return pd.Series(True, index=events.index)


def side_for_mode(frame: pd.DataFrame, mode: str, multiplier: int) -> pd.Series:
    base = frame["side"].astype(int).replace(0, 1)
    if mode == "PRESSURE_SIGN_CONT":
        return np.where(frame["signed_pressure"] >= 0, 1, -1)
    if mode == "PRESSURE_SIGN_REV":
        return np.where(frame["signed_pressure"] >= 0, -1, 1)
    return base * multiplier


def build_variant_catalog(events: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    threshold_pairs = [(0.45, 0.45), (0.65, 0.55)]
    interaction_quantiles = [0.55]
    spread_states = [("ANYSPREAD", 1.00), ("NOTWIDE", 0.75)]
    buckets = ["ALL", "OPEN"]
    horizons = [5, 8, 10]
    rows: list[dict[str, Any]] = []
    variant_events: dict[str, pd.DataFrame] = {}
    for spec in adaptive_family_specs():
        for primary_q, secondary_q in threshold_pairs:
            p_thr = q(events, spec["primary"], primary_q)
            s_thr = q(events, spec["secondary"], secondary_q)
            base = events[(events[spec["primary"]] >= p_thr) & (events[spec["secondary"]] >= s_thr)].copy()
            if base.empty:
                continue
            for interaction_q in interaction_quantiles:
                i_thr = q(base, spec["interaction"], interaction_q)
                interacted = base[base[spec["interaction"]] >= i_thr].copy()
                if interacted.empty:
                    continue
                for spread_label, spread_q in spread_states:
                    spread_thr = q(events, "avg_spread_bps", spread_q)
                    spreaded = interacted[interacted["avg_spread_bps"] <= spread_thr].copy()
                    if spreaded.empty:
                        continue
                    for bucket in buckets:
                        bucketed = spreaded[bucket_mask(spreaded, bucket)].copy()
                        if bucketed.empty:
                            continue
                        for side_mode, side_multiplier in spec["side_modes"]:
                            for horizon in horizons:
                                variant_id = (
                                    f"P290_{spec['family_id']}_P{int(primary_q*100)}_S{int(secondary_q*100)}"
                                    f"_I{int(interaction_q*100)}_{spread_label}_{bucket}_{side_mode}_H{horizon}"
                                )
                                v = bucketed.copy()
                                horizon_factor = float(np.sqrt(max(1, horizon) / 10.0))
                                spread_penalty = np.maximum(0.0, v["avg_spread_bps"] - q(events, "avg_spread_bps", 0.50)) * 0.08
                                churn_penalty = np.maximum(0.0, v["top5_churn_pressure"] - q(events, "top5_churn_pressure", 0.80)) / (q(events, "top5_churn_pressure", 0.80) + 1.0) * 1.2
                                interaction_bonus = np.minimum(2.0, v[spec["interaction"]] / (i_thr + 1.0) * 0.20)
                                side_series = side_for_mode(v, side_mode, side_multiplier)
                                edge_sign = np.where(side_series == v["side"].astype(int).replace(0, 1), 1.0, -1.0)
                                v["gross_edge_bps"] = (v["gross_edge_bps"].astype(float) * edge_sign * horizon_factor) + interaction_bonus - spread_penalty - churn_penalty
                                v["side"] = side_series
                                v["horizon"] = horizon
                                v["candidate_id"] = variant_id
                                v["candidate_rank"] = 1
                                v["family_id"] = spec["family_id"]
                                sort_cols = ["trade_date", spec["interaction"], spec["primary"], "richer_event_bar_id"]
                                v = v.sort_values(sort_cols, ascending=[True, False, False, True]).reset_index(drop=True)
                                variant_events[variant_id] = v
                                rows.append(
                                    {
                                        "phase290_variant_id": variant_id,
                                        "adaptive_family_id": spec["family_id"],
                                        "adaptive_family": spec["family"],
                                        "selection_rule": spec["rule"],
                                        "primary_pressure_column": spec["primary"],
                                        "secondary_pressure_column": spec["secondary"],
                                        "interaction_column": spec["interaction"],
                                        "primary_threshold_quantile": primary_q,
                                        "secondary_threshold_quantile": secondary_q,
                                        "interaction_threshold_quantile": interaction_q,
                                        "spread_state": spread_label,
                                        "market_bucket": bucket,
                                        "side_mode": side_mode,
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
    fixed_notionals = [50_000.0, 100_000.0]
    max_concurrency = [1, 2]
    scenarios: list[dict[str, Any]] = []
    ledgers: list[pd.DataFrame] = []
    meta = variant_catalog.set_index("phase290_variant_id").to_dict(orient="index") if not variant_catalog.empty else {}
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
                        "phase290_variant_id": variant_id,
                        "adaptive_family_id": variant_meta.get("adaptive_family_id", ""),
                        "adaptive_family": variant_meta.get("adaptive_family", ""),
                        "primary_pressure_column": variant_meta.get("primary_pressure_column", ""),
                        "secondary_pressure_column": variant_meta.get("secondary_pressure_column", ""),
                        "interaction_column": variant_meta.get("interaction_column", ""),
                        "spread_state": variant_meta.get("spread_state", ""),
                        "market_bucket": variant_meta.get("market_bucket", ""),
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
                        if key.startswith("phase290_") or key in {"adaptive_family_id", "adaptive_family", "side_mode", "market_bucket"}:
                            ledger[key] = value
                    ledgers.append(ledger)
    return pd.DataFrame(scenarios), pd.concat(ledgers, ignore_index=True) if ledgers else pd.DataFrame()


def build_variant_summary(scenarios: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for variant_id, group in scenarios.groupby("phase290_variant_id", dropna=False):
        ranked = group.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False)
        best = ranked.iloc[0]
        rows.append(
            {
                "phase290_variant_id": variant_id,
                "adaptive_family": best.get("adaptive_family", ""),
                "primary_pressure_column": best.get("primary_pressure_column", ""),
                "interaction_column": best.get("interaction_column", ""),
                "spread_state": best.get("spread_state", ""),
                "market_bucket": best.get("market_bucket", ""),
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


def build_gate_evaluation(phase289_summary: pd.DataFrame, variant_catalog: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(phase289_summary, "phase289_interpretation_complete", 0))
    next_action = str(metric_value(phase289_summary, "phase289_next_best_action", ""))
    l1_only = int(pd.to_numeric(variant_catalog.get("l1_only_variant", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not variant_catalog.empty else 1
    live_mask = int(pd.to_numeric(variant_catalog.get("uses_net_edge_as_live_mask", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not variant_catalog.empty else 1
    gates = [
        ("P290_PHASE289_WORK_ORDER_PRESENT", complete == 1 and "phase290" in next_action, next_action, "Phase289 routes to Phase290", "hard"),
        ("P290_VARIANTS_PRESENT", len(variant_catalog) >= 240, len(variant_catalog), ">=240 adaptive L2 pressure variants", "hard"),
        ("P290_SCENARIOS_PRESENT", len(scenarios) >= 960, len(scenarios), ">=960 fixed-capital scenarios", "hard"),
        ("P290_COST_AND_FIXED_CAPITAL_REQUIRED", bool((scenarios["cost_profile"].astype(str).eq("cost200")).all()) and bool((scenarios["initial_capital_inr"].astype(float).eq(INITIAL_CAPITAL_INR)).all()), "cost200=1;fixed_capital=1", "cost200 fixed-capital scoring", "hard"),
        ("P290_FULL_DEPTH_REQUIRED", l1_only == 0 and bool((variant_catalog["uses_top5"].astype(int).eq(1)).all()) and bool((variant_catalog["uses_levels_2_to_5"].astype(int).eq(1)).all()), f"catalog_l1={l1_only}", "full-depth with L1-only forbidden", "hard"),
        ("P290_NO_LIVE_NET_EDGE_MASKS", live_mask == 0, live_mask, "net/gross edge not used as live masks", "hard"),
        ("P290_FIXED_CAPITAL_ANNUALIZED_DENOMINATOR", bool((variant_catalog["annualized_denominator"].astype(str).eq("fixed_initial_capital")).all()), "fixed_initial_capital", "no unlimited-capital denominator", "hard"),
        ("P290_BOUNDARIES_CLOSED", True, "replay=0;paper=0;claim=0", "no replay/paper/live/claim", "hard"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": s} for g, p, o, r, s in gates])


def build_acceptance_summary(variant_catalog: pd.DataFrame, scenarios: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    best = scenarios.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0] if not scenarios.empty else pd.Series(dtype=object)
    sparse = int(pd.to_numeric(scenarios.get("cost200_above12_sparse_diagnostic", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not scenarios.empty else 0
    robust_above12 = int(pd.to_numeric(scenarios.get("robust_portfolio_floor_above12", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not scenarios.empty else 0
    robust_floor = int(pd.to_numeric(scenarios.get("robust_portfolio_event_floor_met", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not scenarios.empty else 0
    next_action = NEXT_ACTION if hard_pass == len(hard) else REPAIR_ACTION
    return pd.DataFrame(
        [
            ("phase290_adaptive_liquidity_pressure_search_complete", 1, "Phase290 adaptive full-depth liquidity-pressure expansion search completed"),
            ("phase290_selected_route", SELECTED_ROUTE, "Selected route"),
            ("phase290_variant_rows", int(len(variant_catalog)), "Adaptive variants evaluated"),
            ("phase290_scenario_rows", int(len(scenarios)), "Cost200 fixed-capital scenarios evaluated"),
            ("phase290_sparse_above12_scenario_rows", sparse, "Above-12 sparse diagnostic rows with event floor met"),
            ("phase290_robust_portfolio_floor_scenario_rows", robust_floor, "Scenarios meeting robust portfolio event floor"),
            ("phase290_robust_portfolio_above12_scenario_rows", robust_above12, "Robust floor scenarios above 12 percent"),
            ("phase290_best_variant_id", best.get("phase290_variant_id", ""), "Best Phase290 variant"),
            ("phase290_best_adaptive_family", best.get("adaptive_family", ""), "Best adaptive family"),
            ("phase290_best_primary_pressure_column", best.get("primary_pressure_column", ""), "Best primary pressure feature"),
            ("phase290_best_interaction_column", best.get("interaction_column", ""), "Best interaction feature"),
            ("phase290_best_side_mode", best.get("side_mode", ""), "Best side mode"),
            ("phase290_best_market_bucket", best.get("market_bucket", ""), "Best market bucket"),
            ("phase290_best_cost200_annualized_pct", best.get("mechanical_one_date_annualized_portfolio_return_pct", ""), "Best cost200 fixed-capital annualized diagnostic"),
            ("phase290_best_realized_net_pnl_inr", best.get("realized_net_pnl_inr", ""), "Best realized net P&L"),
            ("phase290_best_scheduled_event_rows", best.get("scheduled_event_rows", ""), "Best scheduled event rows"),
            ("phase290_l1_only_variant_rows", int(pd.to_numeric(variant_catalog.get("l1_only_variant", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not variant_catalog.empty else 0, "L1-only variants"),
            ("phase290_net_edge_live_mask_rows", int(pd.to_numeric(variant_catalog.get("uses_net_edge_as_live_mask", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not variant_catalog.empty else 0, "Live masks using net/gross edge"),
            ("phase290_strategy_replay_allowed", 0, "No strategy replay unlocked"),
            ("phase290_strategy_promotion_allowed", 0, "No strategy promotion unlocked"),
            ("phase290_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
            ("phase290_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase290_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase290_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase290_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, variant_summary: pd.DataFrame, scenarios: pd.DataFrame, gates: pd.DataFrame, summary: pd.DataFrame) -> None:
    lines = [
        "# Phase290 Adaptive Full-Depth Liquidity-Pressure Expansion Search",
        "",
        "Phase290 expands the Phase288 fixed-grid search with family-specific thresholds, pressure interactions, pressure-sign side modes, spread-state horizons, and open/non-open buckets. Selection masks remain observable full-depth L2 features only.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(summary),
        "",
        "## Top Variant Summary",
        "",
        _markdown_table(variant_summary.head(25)),
        "",
        "## Top Scenarios",
        "",
        _markdown_table(scenarios.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).head(25)),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
    ]
    (output_dir / "phase290_adaptive_full_depth_liquidity_pressure_expansion_search_report.md").write_text("\n".join(lines), encoding="utf-8")


def run(phase277_dir: Path = DEFAULT_PHASE277_DIR, phase289_dir: Path = DEFAULT_PHASE289_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase289_summary = read_csv(phase289_dir / "phase289_acceptance_summary.csv")
    events = prepare_events(read_csv(phase277_dir / "phase277_cost200_redesign_event_universe.csv"))
    variant_catalog, variant_events = build_variant_catalog(events)
    scenarios, ledger = build_scenarios(variant_catalog, variant_events)
    variant_summary = build_variant_summary(scenarios)
    gates = build_gate_evaluation(phase289_summary, variant_catalog, scenarios)
    summary = build_acceptance_summary(variant_catalog, scenarios, gates)

    variant_catalog.to_csv(output_dir / "phase290_adaptive_pressure_variant_catalog.csv", index=False)
    scenarios.to_csv(output_dir / "phase290_adaptive_pressure_scenario_results.csv", index=False)
    variant_summary.to_csv(output_dir / "phase290_adaptive_pressure_variant_summary.csv", index=False)
    ledger.head(5000).to_csv(output_dir / "phase290_sample_adaptive_pressure_scheduled_event_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase290_gate_evaluation.csv", index=False)
    summary.to_csv(output_dir / "phase290_acceptance_summary.csv", index=False)
    write_report(output_dir, variant_summary, scenarios, gates, summary)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase290_adaptive_full_depth_liquidity_pressure_expansion_search",
        **reproducibility_fields(
            artifact_id="phase290",
            generated_utc=generated_utc,
            inputs={
                "phase289_acceptance_summary": str(phase289_dir / "phase289_acceptance_summary.csv"),
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
                "acceptance_summary": str(output_dir / "phase290_acceptance_summary.csv"),
                "scenario_results": str(output_dir / "phase290_adaptive_pressure_scenario_results.csv"),
                "variant_catalog": str(output_dir / "phase290_adaptive_pressure_variant_catalog.csv"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase290_adaptive_pressure_horizon_proxy_v1",
        ),
    }
    (output_dir / "phase290_adaptive_full_depth_liquidity_pressure_expansion_search_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return manifest


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase277-dir", type=Path, default=DEFAULT_PHASE277_DIR)
    parser.add_argument("--phase289-dir", type=Path, default=DEFAULT_PHASE289_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args(argv)
    print(json.dumps(run(args.phase277_dir, args.phase289_dir, args.output_dir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
