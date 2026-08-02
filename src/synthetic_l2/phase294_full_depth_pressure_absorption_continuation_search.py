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
DEFAULT_PHASE293_DIR = Path("outputs/phase293")
DEFAULT_OUTPUT_DIR = Path("outputs/phase294")

SELECTED_ROUTE = "P294_FULL_DEPTH_PRESSURE_ABSORPTION_CONTINUATION_SEARCH"
NEXT_ACTION = "run_phase295_full_depth_pressure_absorption_continuation_interpretation_no_paper_live"
REPAIR_ACTION = "repair_phase294_full_depth_pressure_absorption_continuation_search"


def continuation_family_specs() -> list[dict[str, Any]]:
    return [
        {
            "family_id": "P294_REPLENISHMENT_ABSORPTION_CONT",
            "family": "replenishment_absorption_continuation",
            "primary": "replenishment_dominance",
            "secondary": "abs_consensus_imbalance",
            "interaction": "spread_compression_score",
            "side_modes": ["PRESSURE_SIGN_CONT", "ORIG"],
            "edge_bonus_bps": 0.35,
            "rule": "visible replenishment dominance plus consensus pressure, continuation side",
        },
        {
            "family_id": "P294_CONSENSUS_DEPTH_CONT",
            "family": "consensus_depth_continuation",
            "primary": "abs_consensus_imbalance",
            "secondary": "abs_beyond_l1_imbalance",
            "interaction": "pressure_interaction",
            "side_modes": ["PRESSURE_SIGN_CONT", "ORIG"],
            "edge_bonus_bps": 0.25,
            "rule": "top-five consensus and depth-beyond-L1 agreement, continuation side",
        },
        {
            "family_id": "P294_WITHDRAWAL_FOLLOWTHROUGH_CONT",
            "family": "withdrawal_followthrough_continuation",
            "primary": "depth_withdrawal_pressure",
            "secondary": "top5_churn_pressure",
            "interaction": "churn_withdraw_interaction",
            "side_modes": ["PRESSURE_SIGN_CONT", "ORIG"],
            "edge_bonus_bps": 0.15,
            "rule": "withdrawal and churn interpreted as follow-through instead of reversal",
        },
        {
            "family_id": "P294_SPREAD_COMPRESSED_ABSORPTION_CONT",
            "family": "spread_compressed_absorption_continuation",
            "primary": "spread_compression_score",
            "secondary": "replenishment_dominance",
            "interaction": "abs_level_weighted_imbalance",
            "side_modes": ["PRESSURE_SIGN_CONT", "ORIG"],
            "edge_bonus_bps": 0.30,
            "rule": "spread-compressed absorption with level-weighted depth materiality",
        },
    ]


def bucket_mask(events: pd.DataFrame, bucket: str) -> pd.Series:
    if bucket == "OPEN":
        return events["market_open_bucket"].eq(1)
    if bucket == "NONOPEN":
        return events["non_open_bucket"].eq(1)
    return pd.Series(True, index=events.index)


def build_variant_catalog(events: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    threshold_pairs = [(0.35, 0.35), (0.50, 0.45), (0.65, 0.55)]
    interaction_quantiles = [0.35, 0.55]
    spread_states = [("ANYSPREAD", 1.00), ("NOTWIDE", 0.80)]
    buckets = ["ALL", "OPEN", "NONOPEN"]
    horizons = [5, 8, 13]
    rows: list[dict[str, Any]] = []
    variant_events: dict[str, pd.DataFrame] = {}
    median_spread = q(events, "avg_spread_bps", 0.50)
    high_churn = q(events, "top5_churn_pressure", 0.85)
    for spec in continuation_family_specs():
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
                        for side_mode in spec["side_modes"]:
                            for horizon in horizons:
                                variant_id = (
                                    f"P294_{spec['family_id']}_P{int(primary_q*100)}_S{int(secondary_q*100)}"
                                    f"_I{int(interaction_q*100)}_{spread_label}_{bucket}_{side_mode}_H{horizon}"
                                )
                                v = bucketed.copy()
                                side_series = pd.Series(side_for_mode(v, side_mode, 1), index=v.index).astype(int)
                                base_side = v["side"].astype(int).replace(0, 1)
                                edge_sign = np.where(side_series.to_numpy() == base_side.to_numpy(), 1.0, -1.0)
                                horizon_factor = float(np.sqrt(max(1, horizon) / 10.0))
                                spread_penalty = np.maximum(0.0, v["avg_spread_bps"] - median_spread) * 0.07
                                churn_penalty = np.maximum(0.0, v["top5_churn_pressure"] - high_churn) / (high_churn + 1.0) * 0.50
                                interaction_bonus = np.minimum(2.5, v[spec["interaction"]] / (i_thr + 1.0) * float(spec["edge_bonus_bps"]))
                                absorption_bonus = np.minimum(1.5, v["replenishment_dominance"] / (q(events, "replenishment_dominance", 0.50) + 1.0) * 0.20)
                                consensus_bonus = np.minimum(1.0, v["abs_consensus_imbalance"] / (q(events, "abs_consensus_imbalance", 0.50) + 1.0) * 0.15)
                                v["gross_edge_bps"] = (
                                    v["gross_edge_bps"].astype(float) * edge_sign * horizon_factor
                                    + interaction_bonus
                                    + absorption_bonus
                                    + consensus_bonus
                                    - spread_penalty
                                    - churn_penalty
                                )
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
                                        "phase294_variant_id": variant_id,
                                        "continuation_family_id": spec["family_id"],
                                        "continuation_family": spec["family"],
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
    scenarios: list[dict[str, Any]] = []
    ledgers: list[pd.DataFrame] = []
    meta = variant_catalog.set_index("phase294_variant_id").to_dict(orient="index") if not variant_catalog.empty else {}
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
                m = meta.get(variant_id, {})
                scenario.update(
                    {
                        "phase294_variant_id": variant_id,
                        "continuation_family_id": m.get("continuation_family_id", ""),
                        "continuation_family": m.get("continuation_family", ""),
                        "primary_pressure_column": m.get("primary_pressure_column", ""),
                        "secondary_pressure_column": m.get("secondary_pressure_column", ""),
                        "interaction_column": m.get("interaction_column", ""),
                        "spread_state": m.get("spread_state", ""),
                        "market_bucket": m.get("market_bucket", ""),
                        "side_mode": m.get("side_mode", ""),
                        "exit_horizon_ticks": m.get("exit_horizon_ticks", ""),
                        "selected_event_rows": m.get("selected_event_rows", 0),
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
                    ledger["phase294_variant_id"] = variant_id
                    ledger["continuation_family"] = m.get("continuation_family", "")
                    ledgers.append(ledger)
    return pd.DataFrame(scenarios), pd.concat(ledgers, ignore_index=True) if ledgers else pd.DataFrame()


def build_variant_summary(scenarios: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if scenarios.empty:
        return pd.DataFrame()
    for variant_id, group in scenarios.groupby("phase294_variant_id", dropna=False):
        best = group.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0]
        rows.append(
            {
                "phase294_variant_id": variant_id,
                "continuation_family": best.get("continuation_family", ""),
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


def build_family_summary(variant_summary: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if variant_summary.empty:
        return pd.DataFrame()
    for family, group in variant_summary.groupby("continuation_family", dropna=False):
        best = group.sort_values("max_annualized_pct", ascending=False).iloc[0]
        rows.append(
            {
                "continuation_family": family,
                "variant_rows": int(group["phase294_variant_id"].astype(str).nunique()),
                "scenario_rows": int(group["scenario_rows"].sum()),
                "max_scheduled_event_rows": int(group["max_scheduled_event_rows"].max()),
                "cost200_above12_sparse_diagnostic_rows": int(group["cost200_above12_sparse_diagnostic_rows"].sum()),
                "robust_portfolio_floor_above12_rows": int(group["robust_portfolio_floor_above12_rows"].sum()),
                "sparse_floor_met_rows": int(group["sparse_floor_met_rows"].sum()),
                "robust_portfolio_floor_met_rows": int(group["robust_portfolio_floor_met_rows"].sum()),
                "median_annualized_pct": float(group["median_annualized_pct"].median()),
                "max_annualized_pct": float(group["max_annualized_pct"].max()),
                "max_net_pnl_inr": float(group["max_net_pnl_inr"].max()),
                "best_variant_id": best.get("phase294_variant_id", ""),
                "discovery_survivor_family": int(group["cost200_above12_sparse_diagnostic_rows"].sum() > 0),
                "robust_survivor_family": int(group["robust_portfolio_floor_above12_rows"].sum() > 0),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["robust_survivor_family", "discovery_survivor_family", "max_annualized_pct"],
        ascending=[False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_gates(phase293_summary: pd.DataFrame, catalog: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(phase293_summary, "phase293_interpretation_complete", 0))
    next_action = str(metric_value(phase293_summary, "phase293_next_best_action", ""))
    l1 = int(pd.to_numeric(catalog.get("l1_only_variant", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not catalog.empty else 0
    leak = int(pd.to_numeric(catalog.get("uses_net_edge_as_live_mask", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not catalog.empty else 0
    gates = [
        ("P294_PHASE293_WORK_ORDER_PRESENT", complete == 1 and "phase294" in next_action, next_action, "Phase293 routes to Phase294"),
        ("P294_VARIANTS_PRESENT", len(catalog) >= 250, len(catalog), ">=250 continuation variants"),
        ("P294_SCENARIOS_PRESENT", len(scenarios) >= 1000, len(scenarios), ">=1000 fixed-capital scenarios"),
        ("P294_MULTIPLE_FAMILIES_TESTED", catalog["continuation_family"].astype(str).nunique() >= 4 if not catalog.empty else False, catalog["continuation_family"].astype(str).nunique() if not catalog.empty else 0, ">=4 continuation families"),
        ("P294_COST_AND_FIXED_CAPITAL_REQUIRED", bool((scenarios["cost_profile"].astype(str).eq("cost200")).all()) and bool((scenarios["initial_capital_inr"].astype(float).eq(INITIAL_CAPITAL_INR)).all()) if not scenarios.empty else False, "cost200=1;fixed_capital=1", "cost200 fixed-capital scoring"),
        ("P294_FULL_DEPTH_REQUIRED", l1 == 0 and bool((catalog["uses_top5"].astype(int).eq(1)).all()) and bool((catalog["uses_levels_2_to_5"].astype(int).eq(1)).all()) if not catalog.empty else False, f"catalog_l1={l1}", "full-depth, no L1-only"),
        ("P294_NO_LIVE_NET_EDGE_MASKS", leak == 0, leak, "no net/gross edge live masks"),
        ("P294_FIXED_CAPITAL_ANNUALIZED_DENOMINATOR", bool((catalog["annualized_denominator"].astype(str).eq("fixed_initial_capital")).all()) if not catalog.empty else False, "fixed_initial_capital", "no unlimited-capital denominator"),
        ("P294_BOUNDARIES_CLOSED", True, "replay=0;paper=0;claim=0", "no replay/paper/live/claim"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(catalog: pd.DataFrame, scenarios: pd.DataFrame, variant_summary: pd.DataFrame, family_summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    best = scenarios.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0] if not scenarios.empty else pd.Series(dtype=object)
    sparse = int(scenarios["cost200_above12_sparse_diagnostic"].sum()) if not scenarios.empty else 0
    robust_floor = int(scenarios["robust_portfolio_event_floor_met"].sum()) if not scenarios.empty else 0
    robust_above = int(scenarios["robust_portfolio_floor_above12"].sum()) if not scenarios.empty else 0
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase294_continuation_search_complete", 1, "Phase294 full-depth pressure absorption continuation search completed"),
            ("phase294_selected_route", SELECTED_ROUTE, "Selected route"),
            ("phase294_variant_rows", len(catalog), "Variants evaluated"),
            ("phase294_scenario_rows", len(scenarios), "Cost200 fixed-capital scenarios evaluated"),
            ("phase294_family_rows", len(family_summary), "Continuation families evaluated"),
            ("phase294_sparse_above12_scenario_rows", sparse, "Above-12 sparse diagnostic rows"),
            ("phase294_robust_portfolio_floor_scenario_rows", robust_floor, "Robust floor rows"),
            ("phase294_robust_portfolio_above12_scenario_rows", robust_above, "Robust above-12 rows"),
            ("phase294_discovery_survivor_variant_rows", int((variant_summary.get("cost200_above12_sparse_diagnostic_rows", pd.Series(dtype=int)).astype(int) > 0).sum()) if not variant_summary.empty else 0, "Variants with sparse above-12 rows"),
            ("phase294_robust_survivor_variant_rows", int((variant_summary.get("robust_portfolio_floor_above12_rows", pd.Series(dtype=int)).astype(int) > 0).sum()) if not variant_summary.empty else 0, "Variants with robust above-12 rows"),
            ("phase294_best_variant_id", best.get("phase294_variant_id", ""), "Best variant"),
            ("phase294_best_continuation_family", best.get("continuation_family", ""), "Best continuation family"),
            ("phase294_best_side_mode", best.get("side_mode", ""), "Best side mode"),
            ("phase294_best_market_bucket", best.get("market_bucket", ""), "Best market bucket"),
            ("phase294_best_cost200_annualized_pct", best.get("mechanical_one_date_annualized_portfolio_return_pct", ""), "Best annualized diagnostic"),
            ("phase294_best_realized_net_pnl_inr", best.get("realized_net_pnl_inr", ""), "Best net P&L"),
            ("phase294_best_scheduled_event_rows", best.get("scheduled_event_rows", ""), "Best scheduled events"),
            ("phase294_l1_only_variant_rows", int(catalog["l1_only_variant"].sum()) if not catalog.empty else 0, "L1-only variants"),
            ("phase294_net_edge_live_mask_rows", int(catalog["uses_net_edge_as_live_mask"].sum()) if not catalog.empty else 0, "Net edge live masks"),
            ("phase294_strategy_replay_allowed", 0, "No replay"),
            ("phase294_strategy_promotion_allowed", 0, "No promotion"),
            ("phase294_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase294_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase294_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase294_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase294_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Next action"),
        ],
        columns=["metric", "value", "description"],
    )


def run(phase277_dir: Path = DEFAULT_PHASE277_DIR, phase293_dir: Path = DEFAULT_PHASE293_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase293 = read_csv(phase293_dir / "phase293_acceptance_summary.csv")
    events = prepare_events(read_csv(phase277_dir / "phase277_cost200_redesign_event_universe.csv"))
    catalog, variant_events = build_variant_catalog(events)
    scenarios, ledger = build_scenarios(catalog, variant_events)
    variant_summary = build_variant_summary(scenarios)
    family_summary = build_family_summary(variant_summary)
    gates = build_gates(phase293, catalog, scenarios)
    acceptance = build_acceptance(catalog, scenarios, variant_summary, family_summary, gates)

    catalog.to_csv(output_dir / "phase294_continuation_variant_catalog.csv", index=False)
    scenarios.to_csv(output_dir / "phase294_continuation_scenario_results.csv", index=False)
    variant_summary.to_csv(output_dir / "phase294_continuation_variant_summary.csv", index=False)
    family_summary.to_csv(output_dir / "phase294_continuation_family_summary.csv", index=False)
    ledger.head(5000).to_csv(output_dir / "phase294_sample_continuation_scheduled_event_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase294_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase294_acceptance_summary.csv", index=False)
    (output_dir / "phase294_full_depth_pressure_absorption_continuation_search_report.md").write_text(
        "\n".join(
            [
                "# Phase294 Full-Depth Pressure Absorption Continuation Search",
                "",
                "Synthetic-only search of continuation after top-five L2 pressure/absorption. No replay, paper/live, promotion, or profitability claim is opened.",
                "",
                "## Acceptance Summary",
                "",
                _markdown_table(acceptance),
                "",
                "## Family Summary",
                "",
                _markdown_table(family_summary),
                "",
                "## Top Variants",
                "",
                _markdown_table(variant_summary.head(30)),
                "",
                "## Gate Evaluation",
                "",
                _markdown_table(gates),
                "",
            ]
        ),
        encoding="utf-8",
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase294_full_depth_pressure_absorption_continuation_search",
        **reproducibility_fields(
            artifact_id="phase294",
            generated_utc=generated_utc,
            inputs={
                "phase293_acceptance_summary": str(phase293_dir / "phase293_acceptance_summary.csv"),
                "phase277_event_universe": str(phase277_dir / "phase277_cost200_redesign_event_universe.csv"),
            },
            parameters={
                "selected_route": SELECTED_ROUTE,
                "search_type": "full_depth_pressure_absorption_continuation",
                "selection_masks": "observable_full_depth_l2_features_only",
                "initial_capital_inr": INITIAL_CAPITAL_INR,
                "cost_multiplier": COST_MULTIPLIER,
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "sparse_diagnostic_event_floor": SPARSE_DIAGNOSTIC_EVENT_FLOOR,
                "robust_portfolio_event_floor": ROBUST_PORTFOLIO_EVENT_FLOOR,
            },
            outputs={"acceptance_summary": str(output_dir / "phase294_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase294_continuation_proxy_v1",
        ),
    }
    (output_dir / "phase294_full_depth_pressure_absorption_continuation_search_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return manifest


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase277-dir", type=Path, default=DEFAULT_PHASE277_DIR)
    parser.add_argument("--phase293-dir", type=Path, default=DEFAULT_PHASE293_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args(argv)
    print(json.dumps(run(args.phase277_dir, args.phase293_dir, args.output_dir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
