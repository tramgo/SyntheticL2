from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase332_event_catalyst_expanded_strategy_search_training_only import (
    passive_adjustments,
    signed_signal,
    vector_cost_inr,
    write_parquet,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE330_DIR = Path("outputs/phase330")
DEFAULT_PHASE334_DIR = Path("outputs/phase334")
DEFAULT_OUTPUT_DIR = Path("outputs/phase335")

NEXT_ACTION = "run_phase336_cost_stress_margin_redesign_interpretation_no_replay"
REPAIR_ACTION = "repair_phase335_cost_stress_margin_redesign_training_only"

ANNUALIZED_THRESHOLD_PCT = 12.0
ROBUST_EVENT_FLOOR = 30
PRESERVED_FAMILY = "P331_DEPTH_ACCEL_REVERSAL"


def stable_random_side(event_id: str, symbol: str, seed: int = 335) -> int:
    key = f"{seed}|{event_id}|{symbol}".encode("utf-8")
    digest = hashlib.sha256(key).digest()
    return 1 if digest[0] % 2 == 0 else -1


def add_live_features(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    out["signal"] = signed_signal(out, PRESERVED_FAMILY).fillna(0.0)
    out["abs_signal"] = out["signal"].abs()
    out["side"] = np.where(out["signal"] > 0, 1, -1)
    out["spread_bps"] = (
        pd.to_numeric(out["event_l1_spread"], errors="coerce")
        / pd.to_numeric(out["event_l1_mid"], errors="coerce").replace(0, np.nan)
        * 10_000.0
    ).replace([np.inf, -np.inf], np.nan).fillna(999.0)
    out["depth_share"] = pd.to_numeric(out["event_l2_l5_depth_share"], errors="coerce").fillna(0.0)
    out["order_imbalance_abs"] = pd.to_numeric(out["event_depth_l2_l5_order_imbalance"], errors="coerce").abs().fillna(0.0)
    out["random_side"] = [stable_random_side(str(e), str(s)) for e, s in zip(out["event_id"], out["symbol"])]
    return out


def build_variant_grid() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []

    def add_lane(lane_id: str, signal_qs: list[float], spread_qs: list[float], depth_qs: list[float], top_ns: list[int], horizons: list[int], side_policies: list[str]) -> None:
        for signal_q in signal_qs:
            for spread_q in spread_qs:
                for depth_q in depth_qs:
                    for top_n in top_ns:
                        for horizon in horizons:
                            for side_policy in side_policies:
                                rows.append(
                                    {
                                        "lane_id": lane_id,
                                        "signal_quantile": signal_q,
                                        "spread_max_quantile": spread_q,
                                        "depth_share_min_quantile": depth_q,
                                        "top_n_per_event": top_n,
                                        "horizon_seconds": horizon,
                                        "side_policy": side_policy,
                                    }
                                )

    add_lane(
        "P334_LANE_A_STRICTER_DEPTH_ACCEL_EDGE",
        signal_qs=[0.95, 0.975],
        spread_qs=[0.75, 1.00],
        depth_qs=[0.50, 0.75],
        top_ns=[2, 4],
        horizons=[300, 900],
        side_policies=["long_only"],
    )
    add_lane(
        "P334_LANE_B_TURNOVER_COMPRESSION",
        signal_qs=[0.50, 0.75, 0.90],
        spread_qs=[0.50, 0.75],
        depth_qs=[0.50],
        top_ns=[1, 2],
        horizons=[900, 1800],
        side_policies=["long_only"],
    )
    add_lane(
        "P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN",
        signal_qs=[0.50, 0.75],
        spread_qs=[0.35, 0.50, 0.75],
        depth_qs=[0.50, 0.75],
        top_ns=[3, 4],
        horizons=[900, 1800],
        side_policies=["long_only"],
    )
    add_lane(
        "P334_LANE_D_HORIZON_AND_EXIT_MARGIN",
        signal_qs=[0.75, 0.90, 0.975],
        spread_qs=[1.00],
        depth_qs=[0.50],
        top_ns=[1, 2, 4],
        horizons=[60, 300, 900, 1800],
        side_policies=["long_only"],
    )
    return pd.DataFrame(rows).drop_duplicates().reset_index(drop=True)


def scenario_id(row: pd.Series) -> str:
    return (
        f"P335_{row['lane_id']}_SQ{float(row['signal_quantile']):.3f}_SPQ{float(row['spread_max_quantile']):.3f}_"
        f"DSQ{float(row['depth_share_min_quantile']):.3f}_TOP{int(row['top_n_per_event'])}_"
        f"H{int(row['horizon_seconds'])}_{row['side_policy']}_{row['execution_policy']}_"
        f"CAP{int(row['initial_capital_inr'])}_NOT{int(row['fixed_notional_inr'])}_"
        f"CONC{int(row['max_concurrent_positions'])}_{row['cost_profile']}"
    ).replace(".", "p")


def annualized_from_returns(selected: pd.DataFrame, signed_returns: pd.Series, notional: float, capital: float, cost_profile: str, execution_policy: str) -> tuple[float, float, float, float, float, float]:
    if selected.empty:
        return 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    fill_probability, _, passive_penalty = passive_adjustments(selected, execution_policy, notional)
    gross_pnl = notional * signed_returns / 10_000.0 * fill_probability
    costs = vector_cost_inr(notional, signed_returns, cost_profile) * fill_probability
    gross_sum = float(gross_pnl.sum())
    cost_sum = float(costs.sum())
    passive_sum = float(passive_penalty.sum())
    net_pnl = gross_sum - cost_sum - passive_sum
    observed_dates = int(selected["event_time_ist"].astype(str).str.slice(0, 10).nunique())
    portfolio_return_pct = net_pnl / capital * 100.0 if capital else 0.0
    annualized = portfolio_return_pct * 252.0 / max(observed_dates, 1)
    avg_fill = float(fill_probability.mean()) if len(fill_probability) else 0.0
    return annualized, net_pnl, gross_sum, cost_sum, passive_sum, avg_fill


def run_search(features: pd.DataFrame, variants: pd.DataFrame) -> pd.DataFrame:
    frame = add_live_features(features)
    rows: list[dict[str, Any]] = []
    capitals = [100_000.0, 250_000.0]
    notionals = [50_000.0, 100_000.0]
    max_concurrencies = [1, 2, 4]
    cost_profiles = ["zerodha_base", "zerodha_2x_all_in_cost_proxy"]
    execution_policies = ["taker_entry_taker_exit", "passive_aware_directional_with_penalties"]

    for variant in variants.itertuples(index=False):
        target_col = f"target_post_{int(variant.horizon_seconds)}s_mid_return_bps"
        if target_col not in frame.columns:
            continue
        work = frame[
            frame["signal"].ne(0)
            & frame["abs_signal"].ge(frame["abs_signal"].quantile(float(variant.signal_quantile)))
            & frame["spread_bps"].le(frame["spread_bps"].quantile(float(variant.spread_max_quantile)))
            & frame["depth_share"].ge(frame["depth_share"].quantile(float(variant.depth_share_min_quantile)))
        ].copy()
        if str(variant.side_policy) == "long_only":
            work = work[work["side"].eq(1)].copy()
        work[target_col] = pd.to_numeric(work[target_col], errors="coerce")
        work = work.dropna(subset=[target_col]).sort_values(["event_id", "abs_signal", "symbol"], ascending=[True, False, True])
        selected_base = work.groupby("event_id", group_keys=False).head(int(variant.top_n_per_event)).copy() if not work.empty else pd.DataFrame()

        for notional in notionals:
            for capital in capitals:
                for max_concurrent in max_concurrencies:
                    slots = max(0, min(int(max_concurrent), int(capital // notional), int(variant.top_n_per_event)))
                    if selected_base.empty or slots <= 0:
                        selected = pd.DataFrame()
                    else:
                        selected = selected_base.groupby("event_id", group_keys=False).head(slots).copy()
                    event_rows = int(selected["event_id"].nunique()) if not selected.empty else 0
                    symbol_rows = int(selected["symbol"].nunique()) if not selected.empty else 0
                    observed_dates = int(selected["event_time_ist"].astype(str).str.slice(0, 10).nunique()) if not selected.empty else 0
                    trade_rows = int(len(selected))
                    base_returns = selected["side"] * pd.to_numeric(selected[target_col], errors="coerce") if not selected.empty else pd.Series(dtype=float)
                    side_flip_returns = -base_returns
                    random_returns = selected["random_side"] * pd.to_numeric(selected[target_col], errors="coerce") if not selected.empty else pd.Series(dtype=float)
                    for execution_policy in execution_policies:
                        for cost_profile in cost_profiles:
                            annualized, net_pnl, gross_pnl, cost_inr, passive_penalty, avg_fill = annualized_from_returns(
                                selected, base_returns.fillna(0.0), notional, capital, cost_profile, execution_policy
                            )
                            side_flip_annualized, side_flip_net, *_ = annualized_from_returns(
                                selected, side_flip_returns.fillna(0.0), notional, capital, cost_profile, execution_policy
                            )
                            random_annualized, random_net, *_ = annualized_from_returns(
                                selected, random_returns.fillna(0.0), notional, capital, cost_profile, execution_policy
                            )
                            control_pass = int(annualized > side_flip_annualized and annualized > random_annualized)
                            acceptance_grade = int(
                                cost_profile == "zerodha_2x_all_in_cost_proxy"
                                and annualized > ANNUALIZED_THRESHOLD_PCT
                                and event_rows >= ROBUST_EVENT_FLOOR
                                and symbol_rows >= 2
                                and observed_dates >= 2
                                and control_pass == 1
                            )
                            row = {
                                "lane_id": variant.lane_id,
                                "family_id": PRESERVED_FAMILY,
                                "signal_quantile": float(variant.signal_quantile),
                                "spread_max_quantile": float(variant.spread_max_quantile),
                                "depth_share_min_quantile": float(variant.depth_share_min_quantile),
                                "top_n_per_event": int(variant.top_n_per_event),
                                "horizon_seconds": int(variant.horizon_seconds),
                                "side_policy": variant.side_policy,
                                "execution_policy": execution_policy,
                                "cost_profile": cost_profile,
                                "initial_capital_inr": capital,
                                "fixed_notional_inr": notional,
                                "max_concurrent_positions": int(max_concurrent),
                                "scheduled_event_rows": event_rows,
                                "symbol_rows": symbol_rows,
                                "observed_trade_dates": observed_dates,
                                "trade_rows": trade_rows,
                                "avg_fill_probability": avg_fill,
                                "gross_pnl_inr": gross_pnl,
                                "cost_inr": cost_inr,
                                "passive_penalty_inr": passive_penalty,
                                "net_pnl_inr": net_pnl,
                                "portfolio_return_pct": net_pnl / capital * 100.0 if capital else 0.0,
                                "annualized_return_pct": annualized,
                                "side_flip_annualized_return_pct": side_flip_annualized,
                                "side_flip_net_pnl_inr": side_flip_net,
                                "random_side_annualized_return_pct": random_annualized,
                                "random_side_net_pnl_inr": random_net,
                                "control_pass": control_pass,
                                "above12_annualized": int(annualized > ANNUALIZED_THRESHOLD_PCT),
                                "robust_event_floor_met": int(event_rows >= ROBUST_EVENT_FLOOR),
                                "acceptance_grade_candidate": acceptance_grade,
                                "profitability_claim_allowed": 0,
                            }
                            row["scenario_id"] = scenario_id(pd.Series(row))
                            rows.append(row)
    return pd.DataFrame(rows)


def build_interpretation(scenarios: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame([("phase335_best_scenario_id", "", "No scenarios produced")], columns=["metric", "value", "description"])
    ranked = scenarios.sort_values(["annualized_return_pct", "net_pnl_inr"], ascending=[False, False])
    best = ranked.iloc[0]
    cost200 = scenarios[scenarios["cost_profile"].astype(str).eq("zerodha_2x_all_in_cost_proxy")]
    best_cost200 = cost200.sort_values(["annualized_return_pct", "net_pnl_inr"], ascending=[False, False]).head(1)
    accepted = cost200[cost200["acceptance_grade_candidate"].astype(int).eq(1)] if not cost200.empty else pd.DataFrame()
    best_accepted = accepted.sort_values(["annualized_return_pct", "net_pnl_inr"], ascending=[False, False]).head(1)
    rows = [
        ("phase335_best_scenario_id", best["scenario_id"], "Best scenario by annualized return"),
        ("phase335_best_lane_id", best["lane_id"], "Best scenario design lane"),
        ("phase335_best_annualized_return_pct", float(best["annualized_return_pct"]), "Best annualized fixed-capital return"),
        ("phase335_best_cost_profile", best["cost_profile"], "Best cost profile"),
        ("phase335_cost200_above12_scenario_rows", int((cost200["annualized_return_pct"] > ANNUALIZED_THRESHOLD_PCT).sum()) if not cost200.empty else 0, "2x-cost scenarios above 12%"),
        ("phase335_cost200_acceptance_grade_candidate_rows", int(cost200["acceptance_grade_candidate"].sum()) if not cost200.empty else 0, "2x-cost scenarios passing acceptance-grade diagnostics"),
        ("phase335_best_cost200_scenario_id", best_cost200.iloc[0]["scenario_id"] if not best_cost200.empty else "", "Best 2x-cost scenario id"),
        ("phase335_best_cost200_lane_id", best_cost200.iloc[0]["lane_id"] if not best_cost200.empty else "", "Best 2x-cost lane"),
        ("phase335_best_cost200_annualized_return_pct", float(best_cost200.iloc[0]["annualized_return_pct"]) if not best_cost200.empty else "", "Best 2x-cost annualized return"),
        ("phase335_best_cost200_scheduled_event_rows", int(best_cost200.iloc[0]["scheduled_event_rows"]) if not best_cost200.empty else 0, "Best 2x-cost scheduled events"),
        ("phase335_best_cost200_control_pass", int(best_cost200.iloc[0]["control_pass"]) if not best_cost200.empty else 0, "Best 2x-cost control pass"),
        ("phase335_best_acceptance_grade_cost200_scenario_id", best_accepted.iloc[0]["scenario_id"] if not best_accepted.empty else "", "Best acceptance-grade 2x-cost scenario"),
        ("phase335_best_acceptance_grade_cost200_lane_id", best_accepted.iloc[0]["lane_id"] if not best_accepted.empty else "", "Best acceptance-grade lane"),
        ("phase335_best_acceptance_grade_cost200_annualized_return_pct", float(best_accepted.iloc[0]["annualized_return_pct"]) if not best_accepted.empty else "", "Best acceptance-grade annualized return"),
        ("phase335_best_acceptance_grade_cost200_scheduled_event_rows", int(best_accepted.iloc[0]["scheduled_event_rows"]) if not best_accepted.empty else 0, "Best acceptance-grade scheduled events"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def build_lane_summary(scenarios: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame()
    return (
        scenarios.groupby(["lane_id", "cost_profile", "execution_policy"], dropna=False)
        .agg(
            scenario_rows=("scenario_id", "count"),
            above12_rows=("above12_annualized", "sum"),
            acceptance_grade_rows=("acceptance_grade_candidate", "sum"),
            control_pass_rows=("control_pass", "sum"),
            best_annualized_return_pct=("annualized_return_pct", "max"),
            best_net_pnl_inr=("net_pnl_inr", "max"),
            max_scheduled_event_rows=("scheduled_event_rows", "max"),
            max_symbol_rows=("symbol_rows", "max"),
        )
        .reset_index()
        .sort_values(["acceptance_grade_rows", "best_annualized_return_pct"], ascending=[False, False])
    )


def build_gate_evaluation(phase334: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    phase334_complete = as_int(metric_value(phase334, "phase334_cost_stress_margin_redesign_precommit_complete", 0))
    execution_allowed = as_int(metric_value(phase334, "phase334_strategy_search_execution_allowed_next", 0))
    design_lanes_required = as_int(metric_value(phase334, "phase334_design_lane_rows", 0))
    rows = [
        ("P335_PHASE334_COMPLETE", phase334_complete == 1, phase334_complete, 1),
        ("P335_PHASE334_EXECUTION_ALLOWED", execution_allowed == 1, execution_allowed, 1),
        ("P335_SCENARIOS_PRODUCED", len(scenarios) > 0, len(scenarios), ">0"),
        ("P335_DESIGN_LANES_COVERED", int(scenarios["lane_id"].nunique()) >= design_lanes_required if not scenarios.empty else False, int(scenarios["lane_id"].nunique()) if not scenarios.empty else 0, f">={design_lanes_required}"),
        ("P335_COST200_SCENARIOS_PRESENT", int(scenarios["cost_profile"].astype(str).eq("zerodha_2x_all_in_cost_proxy").sum()) > 0 if not scenarios.empty else False, int(scenarios["cost_profile"].astype(str).eq("zerodha_2x_all_in_cost_proxy").sum()) if not scenarios.empty else 0, ">0"),
        ("P335_PASSIVE_DIAGNOSTICS_PRESENT", int(scenarios["execution_policy"].astype(str).eq("passive_aware_directional_with_penalties").sum()) > 0 if not scenarios.empty else False, int(scenarios["execution_policy"].astype(str).eq("passive_aware_directional_with_penalties").sum()) if not scenarios.empty else 0, ">0"),
        ("P335_FIXED_CAPITAL_DENOMINATOR", bool((scenarios["initial_capital_inr"] > 0).all()) if not scenarios.empty else False, "all_positive", "all_positive"),
        ("P335_CONTROL_COLUMNS_PRESENT", all(col in scenarios.columns for col in ["side_flip_annualized_return_pct", "random_side_annualized_return_pct", "control_pass"]) if not scenarios.empty else False, "present", "present"),
        ("P335_NO_PROFITABILITY_CLAIM", bool((scenarios["profitability_claim_allowed"].astype(int) == 0).all()) if not scenarios.empty else False, "profitability_claim_allowed=0", 0),
        ("P335_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(scenarios: pd.DataFrame, interpretation: pd.DataFrame, gates: pd.DataFrame, scenario_parquet: Path) -> pd.DataFrame:
    im = {str(row.metric): row.value for row in interpretation.itertuples(index=False)}
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    complete = int(hard_pass == hard_rows)
    cost200_rows = int(scenarios["cost_profile"].astype(str).eq("zerodha_2x_all_in_cost_proxy").sum()) if not scenarios.empty else 0
    passive_rows = int(scenarios["execution_policy"].astype(str).eq("passive_aware_directional_with_penalties").sum()) if not scenarios.empty else 0
    rows = [
        ("phase335_cost_stress_margin_redesign_training_complete", complete, "Phase335 training-only redesign search completed"),
        ("phase335_scenario_rows", int(len(scenarios)), "Scenario rows evaluated"),
        ("phase335_design_lane_rows", int(scenarios["lane_id"].nunique()) if not scenarios.empty else 0, "Design lanes evaluated"),
        ("phase335_cost200_scenario_rows", cost200_rows, "2x cost-stress scenarios"),
        ("phase335_passive_aware_scenario_rows", passive_rows, "Passive-aware diagnostic scenarios"),
        ("phase335_above12_annualized_scenario_rows", int(scenarios["above12_annualized"].astype(int).sum()) if not scenarios.empty else 0, "Scenarios above 12%"),
        ("phase335_cost200_above12_scenario_rows", as_int(im.get("phase335_cost200_above12_scenario_rows", 0)), "2x-cost scenarios above 12%"),
        ("phase335_cost200_acceptance_grade_candidate_rows", as_int(im.get("phase335_cost200_acceptance_grade_candidate_rows", 0)), "2x-cost acceptance-grade candidates"),
        ("phase335_best_scenario_id", im.get("phase335_best_scenario_id", ""), "Best scenario id"),
        ("phase335_best_lane_id", im.get("phase335_best_lane_id", ""), "Best lane"),
        ("phase335_best_annualized_return_pct", im.get("phase335_best_annualized_return_pct", ""), "Best annualized return"),
        ("phase335_best_cost_profile", im.get("phase335_best_cost_profile", ""), "Best cost profile"),
        ("phase335_best_cost200_scenario_id", im.get("phase335_best_cost200_scenario_id", ""), "Best 2x-cost scenario id"),
        ("phase335_best_cost200_lane_id", im.get("phase335_best_cost200_lane_id", ""), "Best 2x-cost lane"),
        ("phase335_best_cost200_annualized_return_pct", im.get("phase335_best_cost200_annualized_return_pct", ""), "Best 2x-cost annualized return"),
        ("phase335_best_cost200_scheduled_event_rows", im.get("phase335_best_cost200_scheduled_event_rows", ""), "Best 2x-cost scheduled events"),
        ("phase335_best_cost200_control_pass", im.get("phase335_best_cost200_control_pass", ""), "Best 2x-cost control pass"),
        ("phase335_best_acceptance_grade_cost200_scenario_id", im.get("phase335_best_acceptance_grade_cost200_scenario_id", ""), "Best acceptance-grade 2x-cost scenario id"),
        ("phase335_best_acceptance_grade_cost200_lane_id", im.get("phase335_best_acceptance_grade_cost200_lane_id", ""), "Best acceptance-grade lane"),
        ("phase335_best_acceptance_grade_cost200_annualized_return_pct", im.get("phase335_best_acceptance_grade_cost200_annualized_return_pct", ""), "Best acceptance-grade annualized return"),
        ("phase335_best_acceptance_grade_cost200_scheduled_event_rows", im.get("phase335_best_acceptance_grade_cost200_scheduled_event_rows", ""), "Best acceptance-grade scheduled events"),
        ("phase335_scenario_parquet_written", int(scenario_parquet.exists()), "Scenario parquet written"),
        ("phase335_scenario_parquet_bytes", int(scenario_parquet.stat().st_size) if scenario_parquet.exists() else 0, "Scenario parquet bytes"),
        ("phase335_annualized_denominator", "fixed_initial_capital", "No unlimited capital denominator"),
        ("phase335_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha cost model version"),
        ("phase335_strategy_replay_allowed", 0, "No replay"),
        ("phase335_strategy_promotion_allowed", 0, "No promotion"),
        ("phase335_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase335_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        ("phase335_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase335_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase335_next_best_action", NEXT_ACTION if complete else REPAIR_ACTION, "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, interpretation: pd.DataFrame, lane_summary: pd.DataFrame, gates: pd.DataFrame, top: pd.DataFrame) -> None:
    lines = [
        "# Phase335 Cost-Stress Margin Redesign Training-Only",
        "",
        "Phase335 executes the Phase334-precommitted redesign around the preserved depth-acceleration reversal near miss.",
        "It is training-only. It does not replay, promote, open paper/live acceptance, or claim deployable profitability.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Interpretation metrics",
        "",
        _markdown_table(interpretation),
        "",
        "## Top scenarios",
        "",
        _markdown_table(top),
        "",
        "## Lane summary",
        "",
        _markdown_table(lane_summary.head(80) if not lane_summary.empty else lane_summary),
        "",
        "## Gates",
        "",
        _markdown_table(gates),
    ]
    (output_dir / "phase335_cost_stress_margin_redesign_training_only_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase330_dir: Path = DEFAULT_PHASE330_DIR, phase334_dir: Path = DEFAULT_PHASE334_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    feature_parquet = phase330_dir / "phase330_event_catalyst_expanded_feature_matrix.parquet"
    feature_csv = phase330_dir / "phase330_event_catalyst_expanded_feature_matrix.csv"
    features = pd.read_parquet(feature_parquet) if feature_parquet.exists() else read_csv(feature_csv)
    phase334 = read_csv(phase334_dir / "phase334_acceptance_summary.csv")
    variants = build_variant_grid()
    scenarios = run_search(features, variants)
    if not scenarios.empty:
        scenarios = scenarios.sort_values(["annualized_return_pct", "net_pnl_inr"], ascending=[False, False]).reset_index(drop=True)
    scenario_parquet = output_dir / "phase335_scenario_summary.parquet"
    if not scenarios.empty:
        write_parquet(scenarios, scenario_parquet)
    interpretation = build_interpretation(scenarios)
    lane_summary = build_lane_summary(scenarios)
    gates = build_gate_evaluation(phase334, scenarios)
    acceptance = build_acceptance(scenarios, interpretation, gates, scenario_parquet)
    top = scenarios.head(100) if not scenarios.empty else scenarios

    variants.to_csv(output_dir / "phase335_variant_grid.csv", index=False)
    top.to_csv(output_dir / "phase335_top_scenarios.csv", index=False)
    lane_summary.to_csv(output_dir / "phase335_lane_summary.csv", index=False)
    interpretation.to_csv(output_dir / "phase335_interpretation_metrics.csv", index=False)
    gates.to_csv(output_dir / "phase335_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase335_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, interpretation, lane_summary, gates, top)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase335_cost_stress_margin_redesign_training_only",
        **reproducibility_fields(
            artifact_id="phase335",
            generated_utc=generated_utc,
            inputs={
                "phase330_feature_matrix": str(feature_parquet if feature_parquet.exists() else feature_csv),
                "phase334_acceptance": str(phase334_dir / "phase334_acceptance_summary.csv"),
            },
            parameters={
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "robust_event_floor": ROBUST_EVENT_FLOOR,
                "preserved_family": PRESERVED_FAMILY,
                "variant_rows": int(len(variants)),
            },
            outputs={"acceptance_summary": str(output_dir / "phase335_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase334_training_only_existing_target_horizons",
        ),
    }
    (output_dir / "phase335_cost_stress_margin_redesign_training_only_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase335 cost-stress margin redesign training-only search.")
    parser.add_argument("--phase330-dir", type=Path, default=DEFAULT_PHASE330_DIR)
    parser.add_argument("--phase334-dir", type=Path, default=DEFAULT_PHASE334_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase330_dir, args.phase334_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
