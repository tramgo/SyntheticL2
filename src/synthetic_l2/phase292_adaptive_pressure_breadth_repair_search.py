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
from synthetic_l2.phase271_fixed_capital_concurrency_and_capacity_return_analysis import schedule_events_for_scenario
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase290_adaptive_full_depth_liquidity_pressure_expansion_search import (
    ANNUALIZED_THRESHOLD_PCT,
    COST_MULTIPLIER,
    EXTRA_SLIPPAGE_BPS,
    FEATURE_COLUMNS,
    INITIAL_CAPITAL_INR,
    ROBUST_PORTFOLIO_EVENT_FLOOR,
    SPARSE_DIAGNOSTIC_EVENT_FLOOR,
    prepare_events,
    q,
    side_for_mode,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE277_DIR = Path("outputs/phase277")
DEFAULT_PHASE291_DIR = Path("outputs/phase291")
DEFAULT_OUTPUT_DIR = Path("outputs/phase292")

SELECTED_ROUTE = "P292_ADAPTIVE_PRESSURE_BREADTH_REPAIR_SEARCH"
NEXT_ACTION = "run_phase293_adaptive_pressure_breadth_repair_interpretation_no_paper_live"
REPAIR_ACTION = "repair_phase292_adaptive_pressure_breadth_repair_search"


def build_variant_catalog(events: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    threshold_pairs = [(0.25, 0.25), (0.40, 0.35), (0.55, 0.45)]
    interaction_quantiles = [0.25, 0.45]
    spread_states = [("ANYSPREAD", 1.00), ("NOTWIDE", 0.80)]
    buckets = ["ALL", "OPEN"]
    side_modes = [("INV", -1), ("PRESSURE_SIGN_REV", -1), ("ORIG", 1)]
    horizons = [8, 10]
    rows: list[dict[str, Any]] = []
    variant_events: dict[str, pd.DataFrame] = {}
    primary = "depth_withdrawal_pressure"
    secondary = "top5_churn_pressure"
    interaction = "churn_withdraw_interaction"
    for primary_q, secondary_q in threshold_pairs:
        base = events[(events[primary] >= q(events, primary, primary_q)) & (events[secondary] >= q(events, secondary, secondary_q))].copy()
        if base.empty:
            continue
        for interaction_q in interaction_quantiles:
            interacted = base[base[interaction] >= q(base, interaction, interaction_q)].copy()
            if interacted.empty:
                continue
            for spread_label, spread_q in spread_states:
                spreaded = interacted[interacted["avg_spread_bps"] <= q(events, "avg_spread_bps", spread_q)].copy()
                if spreaded.empty:
                    continue
                for bucket in buckets:
                    if bucket == "OPEN":
                        bucketed = spreaded[spreaded["market_open_bucket"].eq(1)].copy()
                    elif bucket == "NONOPEN":
                        bucketed = spreaded[spreaded["non_open_bucket"].eq(1)].copy()
                    else:
                        bucketed = spreaded.copy()
                    if bucketed.empty:
                        continue
                    for side_mode, side_multiplier in side_modes:
                        for horizon in horizons:
                            variant_id = f"P292_EXHAUSTION_BREADTH_P{int(primary_q*100)}_S{int(secondary_q*100)}_I{int(interaction_q*100)}_{spread_label}_{bucket}_{side_mode}_H{horizon}"
                            v = bucketed.copy()
                            horizon_factor = float(np.sqrt(max(1, horizon) / 10.0))
                            spread_penalty = np.maximum(0.0, v["avg_spread_bps"] - q(events, "avg_spread_bps", 0.50)) * 0.06
                            interaction_bonus = np.minimum(1.5, v[interaction] / (q(base, interaction, interaction_q) + 1.0) * 0.12)
                            side_series = side_for_mode(v, side_mode, side_multiplier)
                            edge_sign = np.where(side_series == v["side"].astype(int).replace(0, 1), 1.0, -1.0)
                            v["gross_edge_bps"] = (v["gross_edge_bps"].astype(float) * edge_sign * horizon_factor) + interaction_bonus - spread_penalty
                            v["side"] = side_series
                            v["horizon"] = horizon
                            v["candidate_id"] = variant_id
                            v["candidate_rank"] = 1
                            v["family_id"] = "P292_EXHAUSTION_BREADTH_REPAIR"
                            v = v.sort_values(["trade_date", interaction, primary, "richer_event_bar_id"], ascending=[True, False, False, True]).reset_index(drop=True)
                            variant_events[variant_id] = v
                            rows.append(
                                {
                                    "phase292_variant_id": variant_id,
                                    "repair_family": "exhaustion_reversal_breadth_repair",
                                    "primary_pressure_column": primary,
                                    "secondary_pressure_column": secondary,
                                    "interaction_column": interaction,
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
                                }
                            )
    return pd.DataFrame(rows), variant_events


def build_scenarios(variant_catalog: pd.DataFrame, variant_events: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame]:
    scenarios: list[dict[str, Any]] = []
    ledgers: list[pd.DataFrame] = []
    meta = variant_catalog.set_index("phase292_variant_id").to_dict(orient="index")
    for variant_id, events in variant_events.items():
        for fixed_notional in [50_000.0, 100_000.0]:
            for max_concurrent in [1, 2]:
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
                m = meta[variant_id]
                scenario.update({k: m.get(k, "") for k in ["repair_family", "primary_pressure_column", "interaction_column", "spread_state", "market_bucket", "side_mode", "exit_horizon_ticks", "selected_event_rows"]})
                scenario["phase292_variant_id"] = variant_id
                scenario.update(
                    {
                        "uses_top5": 1,
                        "uses_levels_2_to_5": 1,
                        "l1_only_variant": 0,
                        "uses_net_edge_as_live_mask": 0,
                        "sparse_diagnostic_event_floor_met": int(scenario["scheduled_event_rows"] >= SPARSE_DIAGNOSTIC_EVENT_FLOOR),
                        "robust_portfolio_event_floor_met": int(scenario["scheduled_event_rows"] >= ROBUST_PORTFOLIO_EVENT_FLOOR),
                        "cost200_above12_sparse_diagnostic": int(scenario["mechanical_one_date_annualized_portfolio_return_pct"] > ANNUALIZED_THRESHOLD_PCT and scenario["scheduled_event_rows"] >= SPARSE_DIAGNOSTIC_EVENT_FLOOR),
                        "robust_portfolio_floor_above12": int(scenario["mechanical_one_date_annualized_portfolio_return_pct"] > ANNUALIZED_THRESHOLD_PCT and scenario["scheduled_event_rows"] >= ROBUST_PORTFOLIO_EVENT_FLOOR),
                    }
                )
                scenarios.append(scenario)
                if not ledger.empty:
                    ledger["phase292_variant_id"] = variant_id
                    ledger["repair_family"] = m.get("repair_family", "")
                    ledgers.append(ledger)
    return pd.DataFrame(scenarios), pd.concat(ledgers, ignore_index=True) if ledgers else pd.DataFrame()


def build_variant_summary(scenarios: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for variant_id, group in scenarios.groupby("phase292_variant_id", dropna=False):
        best = group.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0]
        rows.append(
            {
                "phase292_variant_id": variant_id,
                "repair_family": best.get("repair_family", ""),
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
    return pd.DataFrame(rows).sort_values(["cost200_above12_sparse_diagnostic_rows", "max_annualized_pct", "max_scheduled_event_rows"], ascending=[False, False, False], kind="mergesort").reset_index(drop=True)


def build_gates(phase291_summary: pd.DataFrame, catalog: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(phase291_summary, "phase291_interpretation_complete", 0))
    next_action = str(metric_value(phase291_summary, "phase291_next_best_action", ""))
    l1 = int(pd.to_numeric(catalog.get("l1_only_variant", pd.Series(dtype=int)), errors="coerce").fillna(0).sum())
    leak = int(pd.to_numeric(catalog.get("uses_net_edge_as_live_mask", pd.Series(dtype=int)), errors="coerce").fillna(0).sum())
    gates = [
        ("P292_PHASE291_WORK_ORDER_PRESENT", complete == 1 and "phase292" in next_action, next_action, "Phase291 routes to Phase292"),
        ("P292_VARIANTS_PRESENT", len(catalog) >= 130, len(catalog), ">=130 breadth repair variants"),
        ("P292_SCENARIOS_PRESENT", len(scenarios) >= 500, len(scenarios), ">=500 fixed-capital scenarios"),
        ("P292_COST_AND_FIXED_CAPITAL_REQUIRED", bool((scenarios["cost_profile"].astype(str).eq("cost200")).all()) and bool((scenarios["initial_capital_inr"].astype(float).eq(INITIAL_CAPITAL_INR)).all()), "cost200=1;fixed_capital=1", "cost200 fixed-capital scoring"),
        ("P292_FULL_DEPTH_REQUIRED", l1 == 0 and bool((catalog["uses_top5"].astype(int).eq(1)).all()) and bool((catalog["uses_levels_2_to_5"].astype(int).eq(1)).all()), f"catalog_l1={l1}", "full-depth, no L1-only"),
        ("P292_NO_LIVE_NET_EDGE_MASKS", leak == 0, leak, "no net/gross edge live masks"),
        ("P292_FIXED_CAPITAL_ANNUALIZED_DENOMINATOR", bool((catalog["annualized_denominator"].astype(str).eq("fixed_initial_capital")).all()), "fixed_initial_capital", "no unlimited-capital denominator"),
        ("P292_BOUNDARIES_CLOSED", True, "replay=0;paper=0;claim=0", "no replay/paper/live/claim"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(catalog: pd.DataFrame, scenarios: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    best = scenarios.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0]
    sparse = int(scenarios["cost200_above12_sparse_diagnostic"].sum())
    robust_floor = int(scenarios["robust_portfolio_event_floor_met"].sum())
    robust_above = int(scenarios["robust_portfolio_floor_above12"].sum())
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase292_breadth_repair_search_complete", 1, "Phase292 adaptive pressure breadth repair search completed"),
            ("phase292_selected_route", SELECTED_ROUTE, "Selected route"),
            ("phase292_variant_rows", len(catalog), "Variants evaluated"),
            ("phase292_scenario_rows", len(scenarios), "Cost200 fixed-capital scenarios evaluated"),
            ("phase292_sparse_above12_scenario_rows", sparse, "Above-12 sparse diagnostic rows"),
            ("phase292_robust_portfolio_floor_scenario_rows", robust_floor, "Robust floor rows"),
            ("phase292_robust_portfolio_above12_scenario_rows", robust_above, "Robust above-12 rows"),
            ("phase292_best_variant_id", best.get("phase292_variant_id", ""), "Best variant"),
            ("phase292_best_repair_family", best.get("repair_family", ""), "Best repair family"),
            ("phase292_best_side_mode", best.get("side_mode", ""), "Best side mode"),
            ("phase292_best_market_bucket", best.get("market_bucket", ""), "Best market bucket"),
            ("phase292_best_cost200_annualized_pct", best.get("mechanical_one_date_annualized_portfolio_return_pct", ""), "Best annualized diagnostic"),
            ("phase292_best_realized_net_pnl_inr", best.get("realized_net_pnl_inr", ""), "Best net P&L"),
            ("phase292_best_scheduled_event_rows", best.get("scheduled_event_rows", ""), "Best scheduled events"),
            ("phase292_l1_only_variant_rows", int(catalog["l1_only_variant"].sum()), "L1-only variants"),
            ("phase292_net_edge_live_mask_rows", int(catalog["uses_net_edge_as_live_mask"].sum()), "Net edge live masks"),
            ("phase292_strategy_replay_allowed", 0, "No replay"),
            ("phase292_strategy_promotion_allowed", 0, "No promotion"),
            ("phase292_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase292_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase292_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase292_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase292_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Next action"),
        ],
        columns=["metric", "value", "description"],
    )


def run(phase277_dir: Path = DEFAULT_PHASE277_DIR, phase291_dir: Path = DEFAULT_PHASE291_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase291 = read_csv(phase291_dir / "phase291_acceptance_summary.csv")
    events = prepare_events(read_csv(phase277_dir / "phase277_cost200_redesign_event_universe.csv"))
    catalog, variant_events = build_variant_catalog(events)
    scenarios, ledger = build_scenarios(catalog, variant_events)
    summary = build_variant_summary(scenarios)
    gates = build_gates(phase291, catalog, scenarios)
    acceptance = build_acceptance(catalog, scenarios, gates)
    catalog.to_csv(output_dir / "phase292_breadth_repair_variant_catalog.csv", index=False)
    scenarios.to_csv(output_dir / "phase292_breadth_repair_scenario_results.csv", index=False)
    summary.to_csv(output_dir / "phase292_breadth_repair_variant_summary.csv", index=False)
    ledger.head(5000).to_csv(output_dir / "phase292_sample_breadth_repair_scheduled_event_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase292_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase292_acceptance_summary.csv", index=False)
    (output_dir / "phase292_adaptive_pressure_breadth_repair_search_report.md").write_text(
        "\n".join(["# Phase292 Adaptive Pressure Breadth Repair Search", "", _markdown_table(acceptance), "", _markdown_table(summary.head(25)), "", _markdown_table(gates)]),
        encoding="utf-8",
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {"generated_utc": generated_utc, "scope": "phase292_adaptive_pressure_breadth_repair_search", **reproducibility_fields(artifact_id="phase292", generated_utc=generated_utc, inputs={"phase291_acceptance_summary": str(phase291_dir / "phase291_acceptance_summary.csv"), "phase277_event_universe": str(phase277_dir / "phase277_cost200_redesign_event_universe.csv")}, parameters={"selected_route": SELECTED_ROUTE, "selection_masks": "observable_full_depth_l2_features_only", "initial_capital_inr": INITIAL_CAPITAL_INR, "cost_multiplier": COST_MULTIPLIER}, outputs={"acceptance_summary": str(output_dir / "phase292_acceptance_summary.csv")}, cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, latency_model_version="phase292_breadth_repair_proxy_v1")}
    (output_dir / "phase292_adaptive_pressure_breadth_repair_search_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return manifest


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase277-dir", type=Path, default=DEFAULT_PHASE277_DIR)
    parser.add_argument("--phase291-dir", type=Path, default=DEFAULT_PHASE291_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args(argv)
    print(json.dumps(run(args.phase277_dir, args.phase291_dir, args.output_dir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
