from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase271_fixed_capital_concurrency_and_capacity_return_analysis import (
    COST_PROFILES,
    load_candidate_events,
    schedule_events_for_scenario,
)
from synthetic_l2.phase273_focused_capital_aware_candidate_followthrough_search import (
    ORDER_POLICIES,
    apply_order_policy,
)
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE268_DIR = Path("outputs/phase268")
DEFAULT_PHASE269_DIR = Path("outputs/phase269")
DEFAULT_PHASE274_DIR = Path("outputs/phase274")
DEFAULT_OUTPUT_DIR = Path("outputs/phase275")

SELECTED_ROUTE = "P275_FOCUSED_CAPITAL_MULTIDAY_SYNTHETIC_FOLLOWTHROUGH_SEARCH"
NEXT_ACTION = "run_phase276_multiday_synthetic_followthrough_interpretation_no_paper_live"
REPAIR_ACTION = "repair_phase275_focused_capital_multiday_synthetic_followthrough_search"

INITIAL_CAPITAL_GRID_INR = [100_000.0, 250_000.0]
FIXED_NOTIONAL_GRID_INR = [75_000.0, 100_000.0]
MAX_CONCURRENT_GRID = [1, 2, 3]
SYNTHETIC_DATE_ROWS = 8
SYNTHETIC_SEEDS = [101, 202, 303, 404]
SYNTHETIC_REGIMES = {
    "base_bootstrap": {"edge_multiplier": 1.00, "edge_shift_bps": 0.0, "noise_bps": 2.0, "spread_shift_bps": 0.0},
    "noisy_depth": {"edge_multiplier": 0.90, "edge_shift_bps": 0.0, "noise_bps": 5.0, "spread_shift_bps": 0.5},
    "adverse_trend": {"edge_multiplier": 0.65, "edge_shift_bps": -2.0, "noise_bps": 4.0, "spread_shift_bps": 0.5},
    "spread_stress": {"edge_multiplier": 0.85, "edge_shift_bps": -1.0, "noise_bps": 3.0, "spread_shift_bps": 1.5},
}
ANNUALIZED_THRESHOLD_PCT = 12.0
MIN_SYNTHETIC_DATES_FOR_MULTIDAY_DIAGNOSTIC = 5

FULL_DEPTH_REQUIRED_COLUMNS = [
    "avg_cum_top5_qty_imbalance",
    "avg_depth_beyond_l1_qty_imbalance",
    "avg_level_weighted_depth_imbalance",
    "depth_replenishment_pressure",
    "depth_withdrawal_pressure",
    "top5_churn_pressure",
]


def stable_unit_interval(value: str) -> float:
    raw = hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]
    return int(raw, 16) / float(16**12 - 1)


def cost_profile_lookup() -> dict[str, dict[str, Any]]:
    return {str(row["cost_profile"]): row for row in COST_PROFILES}


def load_scope_profiles(phase274_dir: Path) -> pd.DataFrame:
    route = read_csv(phase274_dir / "phase274_next_route_contract.csv")
    ranked = read_csv(phase274_dir / "phase274_ranked_followthrough_scope_profiles.csv")
    if route.empty:
        raise FileNotFoundError("Missing Phase274 next route contract.")
    if ranked.empty:
        raise FileNotFoundError("Missing Phase274 ranked follow-through profiles.")
    scope_text = str(route.loc[route["contract_id"].astype(str).eq("P275_SCOPE_PROFILES"), "contract_value"].iloc[0])
    requested = [item.strip() for item in scope_text.split(";") if item.strip()]
    rows: list[pd.Series] = []
    for item in requested:
        if ":" not in item:
            continue
        scope_id, cost_profile = item.split(":", 1)
        match = ranked[
            ranked["phase273_scope_id"].astype(str).eq(scope_id)
            & ranked["cost_profile"].astype(str).eq(cost_profile)
        ]
        if not match.empty:
            rows.append(match.iloc[0])
    if not rows:
        raise ValueError("Phase274 route contract did not resolve to any ranked scope profiles.")
    profiles = pd.DataFrame(rows).drop_duplicates(["phase273_scope_id", "phase273_scope_candidate_id", "cost_profile"]).reset_index(drop=True)
    profiles["phase275_scope_profile_id"] = profiles["phase273_scope_id"].astype(str) + ":" + profiles["cost_profile"].astype(str)
    return profiles


def synthetic_trade_dates(rows: int) -> list[str]:
    return [date.strftime("%Y-%m-%d") for date in pd.bdate_range("2026-07-14", periods=rows)]


def perturb_numeric_column(frame: pd.DataFrame, column: str, keys: pd.Series, scale: float, floor: float | None = None) -> None:
    if column not in frame.columns:
        return
    values = pd.to_numeric(frame[column], errors="coerce").fillna(0.0)
    noise = keys.map(lambda key: (stable_unit_interval(f"{key}|{column}") - 0.5) * scale)
    out = values * (1.0 + noise)
    if floor is not None:
        out = out.clip(lower=floor)
    frame[column] = out


def materialize_synthetic_events(base_events: pd.DataFrame, scope_id: str, seed: int, regime_id: str) -> pd.DataFrame:
    if base_events.empty:
        return pd.DataFrame()
    regime = SYNTHETIC_REGIMES[regime_id]
    dates = synthetic_trade_dates(SYNTHETIC_DATE_ROWS)
    frames: list[pd.DataFrame] = []
    base = base_events.sort_values(["trade_date", "exchange", "richer_event_bar_id", "candidate_rank", "candidate_id", "symbol"]).reset_index(drop=True)
    sample_size = max(1, len(base))
    for date_index, trade_date in enumerate(dates):
        sampled = base.sample(n=sample_size, replace=True, random_state=seed + date_index * 997 + len(scope_id)).copy()
        sampled = sampled.sort_values(["richer_event_bar_id", "candidate_rank", "candidate_id", "symbol"]).reset_index(drop=True)
        sampled["trade_date"] = trade_date
        sampled["synthetic_source_trade_date"] = base.loc[sampled.index % len(base), "trade_date"].astype(str).to_numpy()
        sampled["synthetic_date_index"] = date_index + 1
        sampled["synthetic_seed"] = seed
        sampled["synthetic_regime"] = regime_id
        sampled["richer_event_bar_id"] = range(1, len(sampled) + 1)
        keys = (
            sampled["candidate_id"].astype(str)
            + "|"
            + sampled["symbol"].astype(str)
            + "|"
            + sampled["richer_event_bar_id"].astype(str)
            + "|"
            + str(seed)
            + "|"
            + regime_id
            + "|"
            + trade_date
        )
        base_edge = pd.to_numeric(sampled["gross_edge_bps"], errors="coerce").fillna(0.0)
        edge_noise = keys.map(lambda key: (stable_unit_interval(f"{key}|edge") - 0.5) * float(regime["noise_bps"]))
        sampled["gross_edge_bps"] = base_edge * float(regime["edge_multiplier"]) + float(regime["edge_shift_bps"]) + edge_noise
        if "avg_spread_bps" in sampled.columns:
            sampled["avg_spread_bps"] = pd.to_numeric(sampled["avg_spread_bps"], errors="coerce").fillna(0.0) + float(regime["spread_shift_bps"])
        for col in FULL_DEPTH_REQUIRED_COLUMNS:
            perturb_numeric_column(sampled, col, keys, scale=0.18, floor=None if "imbalance" in col else 0.0)
        frames.append(sampled)
    return pd.concat(frames, ignore_index=True)


def daily_summary_from_ledger(ledger: pd.DataFrame, scenario: dict[str, Any]) -> pd.DataFrame:
    if ledger.empty:
        return pd.DataFrame()
    scheduled = ledger[ledger["decision"].astype(str).eq("scheduled")].copy()
    if scheduled.empty:
        dates = sorted(ledger["trade_date"].astype(str).unique())
        return pd.DataFrame(
            [
                {
                    "scenario_id": scenario["scenario_id"],
                    "trade_date": date,
                    "daily_net_pnl_inr": 0.0,
                    "daily_return_pct": 0.0,
                    "scheduled_event_rows": 0,
                    "scheduled_notional_inr": 0.0,
                    "synthetic_seed": scenario["synthetic_seed"],
                    "synthetic_regime": scenario["synthetic_regime"],
                    "phase275_scope_id": scenario["phase275_scope_id"],
                    "cost_profile": scenario["cost_profile"],
                }
                for date in dates
            ]
        )
    grouped = (
        scheduled.groupby("trade_date", dropna=False)
        .agg(
            daily_net_pnl_inr=("net_pnl_inr", "sum"),
            scheduled_event_rows=("decision", "size"),
            scheduled_notional_inr=("notional_inr", "sum"),
        )
        .reset_index()
    )
    grouped["scenario_id"] = scenario["scenario_id"]
    grouped["daily_return_pct"] = grouped["daily_net_pnl_inr"] / float(scenario["initial_capital_inr"]) * 100.0
    grouped["synthetic_seed"] = scenario["synthetic_seed"]
    grouped["synthetic_regime"] = scenario["synthetic_regime"]
    grouped["phase275_scope_id"] = scenario["phase275_scope_id"]
    grouped["cost_profile"] = scenario["cost_profile"]
    return grouped


def run_multiday_search(scope_profiles: pd.DataFrame, events: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    profiles = cost_profile_lookup()
    scenario_rows: list[dict[str, Any]] = []
    daily_frames: list[pd.DataFrame] = []
    sample_ledgers: list[pd.DataFrame] = []
    synthetic_cache: dict[tuple[str, str, int, str], pd.DataFrame] = {}

    for _, profile_row in scope_profiles.iterrows():
        scope_id = str(profile_row["phase273_scope_id"])
        scope_candidate_id = str(profile_row["phase273_scope_candidate_id"])
        cost_profile = str(profile_row["cost_profile"])
        if cost_profile not in profiles:
            continue
        candidate_ids = [item for item in scope_candidate_id.split(";") if item]
        base_scope_events = events[events["candidate_id"].astype(str).isin(candidate_ids)].copy()
        if base_scope_events.empty:
            continue
        cost = profiles[cost_profile]
        for regime_id in SYNTHETIC_REGIMES:
            for seed in SYNTHETIC_SEEDS:
                cache_key = (scope_id, scope_candidate_id, seed, regime_id)
                if cache_key not in synthetic_cache:
                    synthetic_cache[cache_key] = materialize_synthetic_events(base_scope_events, scope_id, seed, regime_id)
                synthetic_events = synthetic_cache[cache_key]
                for order_policy in ORDER_POLICIES:
                    ordered_events = apply_order_policy(synthetic_events, order_policy)
                    for initial_capital in INITIAL_CAPITAL_GRID_INR:
                        for fixed_notional in FIXED_NOTIONAL_GRID_INR:
                            for max_concurrent in MAX_CONCURRENT_GRID:
                                scenario, ledger = schedule_events_for_scenario(
                                    events=ordered_events,
                                    scope_id=f"P275_{scope_id}_{order_policy.upper()}_{regime_id.upper()}_SEED{seed}",
                                    scope_candidate_id=scope_candidate_id,
                                    initial_capital_inr=initial_capital,
                                    fixed_notional_inr=fixed_notional,
                                    max_concurrent_positions=max_concurrent,
                                    cost_profile=cost_profile,
                                    cost_multiplier=float(cost["cost_multiplier"]),
                                    extra_slippage_bps=float(cost["extra_slippage_bps"]),
                                )
                                scenario_id = str(scenario["scenario_id"])
                                scenario.update(
                                    {
                                        "scenario_id": scenario_id,
                                        "phase275_scope_id": scope_id,
                                        "phase275_scope_candidate_id": scope_candidate_id,
                                        "phase275_scope_profile_id": f"{scope_id}:{cost_profile}",
                                        "order_policy": order_policy,
                                        "synthetic_seed": seed,
                                        "synthetic_regime": regime_id,
                                        "synthetic_date_rows": SYNTHETIC_DATE_ROWS,
                                        "synthetic_multiday_diagnostic_allowed": int(scenario["observed_trade_dates"] >= MIN_SYNTHETIC_DATES_FOR_MULTIDAY_DIAGNOSTIC),
                                        "synthetic_multiday_above12_diagnostic": int(
                                            float(scenario["mechanical_one_date_annualized_portfolio_return_pct"]) > ANNUALIZED_THRESHOLD_PCT
                                            and int(scenario["observed_trade_dates"]) >= MIN_SYNTHETIC_DATES_FOR_MULTIDAY_DIAGNOSTIC
                                        ),
                                        "portfolio_claim_allowed": 0,
                                        "annualized_return_is_robust_portfolio_claim": 0,
                                        "strategy_replay_allowed": 0,
                                        "promotion_allowed": 0,
                                        "paper_or_live_acceptance_allowed": 0,
                                        "deployable_profitability_claim_allowed": 0,
                                    }
                                )
                                ledger = ledger.copy()
                                ledger["scenario_id"] = scenario_id
                                ledger["phase275_scope_id"] = scope_id
                                ledger["phase275_scope_profile_id"] = f"{scope_id}:{cost_profile}"
                                ledger["order_policy"] = order_policy
                                ledger["synthetic_seed"] = seed
                                ledger["synthetic_regime"] = regime_id
                                scenario_rows.append(scenario)
                                daily_frames.append(daily_summary_from_ledger(ledger, scenario))
                                if (
                                    cost_profile in {"cost100", "cost200"}
                                    and initial_capital == 100_000.0
                                    and fixed_notional == 100_000.0
                                    and max_concurrent == 1
                                    and order_policy in {"deterministic_shuffle", "time_rank"}
                                    and regime_id in {"base_bootstrap", "adverse_trend"}
                                    and len(sample_ledgers) < 16
                                ):
                                    sample_ledgers.append(ledger)
    scenarios = pd.DataFrame(scenario_rows)
    daily = pd.concat(daily_frames, ignore_index=True) if daily_frames else pd.DataFrame()
    sample_ledger = pd.concat(sample_ledgers, ignore_index=True) if sample_ledgers else pd.DataFrame()
    return scenarios, daily, sample_ledger


def build_stability_summary(scenarios: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame()
    frame = scenarios.copy()
    numeric_cols = [
        "mechanical_one_date_annualized_portfolio_return_pct",
        "realized_net_pnl_inr",
        "synthetic_multiday_above12_diagnostic",
        "scheduled_event_rows",
        "max_drawdown_inr",
    ]
    for col in numeric_cols:
        frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
    grouped = (
        frame.groupby(["phase275_scope_id", "phase275_scope_candidate_id", "cost_profile"], dropna=False)
        .agg(
            scenario_rows=("scenario_id", "nunique"),
            synthetic_above12_scenario_rows=("synthetic_multiday_above12_diagnostic", "sum"),
            min_annualized_pct=("mechanical_one_date_annualized_portfolio_return_pct", "min"),
            median_annualized_pct=("mechanical_one_date_annualized_portfolio_return_pct", "median"),
            max_annualized_pct=("mechanical_one_date_annualized_portfolio_return_pct", "max"),
            mean_net_pnl_inr=("realized_net_pnl_inr", "mean"),
            max_net_pnl_inr=("realized_net_pnl_inr", "max"),
            min_net_pnl_inr=("realized_net_pnl_inr", "min"),
            max_scheduled_event_rows=("scheduled_event_rows", "max"),
            worst_drawdown_inr=("max_drawdown_inr", "min"),
            order_policy_rows=("order_policy", "nunique"),
            synthetic_seed_rows=("synthetic_seed", "nunique"),
            synthetic_regime_rows=("synthetic_regime", "nunique"),
        )
        .reset_index()
    )
    grouped["above12_fraction"] = grouped["synthetic_above12_scenario_rows"] / grouped["scenario_rows"]
    grouped["median_above12"] = (grouped["median_annualized_pct"] > ANNUALIZED_THRESHOLD_PCT).astype(int)
    grouped["worst_case_above12"] = (grouped["min_annualized_pct"] > ANNUALIZED_THRESHOLD_PCT).astype(int)
    return grouped.sort_values(
        ["median_above12", "worst_case_above12", "synthetic_above12_scenario_rows", "median_annualized_pct"],
        ascending=[False, False, False, False],
    ).reset_index(drop=True)


def build_gate_evaluation(phase274_summary: pd.DataFrame, scope_profiles: pd.DataFrame, scenarios: pd.DataFrame, stability: pd.DataFrame, sample_ledger: pd.DataFrame) -> pd.DataFrame:
    phase274_next = str(metric_value(phase274_summary, "phase274_next_best_action", ""))
    phase274_complete = as_int(metric_value(phase274_summary, "phase274_interpretation_complete", 0))
    full_depth_present = bool(not sample_ledger.empty and all(col in sample_ledger.columns for col in FULL_DEPTH_REQUIRED_COLUMNS))
    full_depth_material = bool(
        full_depth_present
        and any(pd.to_numeric(sample_ledger[col], errors="coerce").fillna(0.0).abs().sum() > 0 for col in FULL_DEPTH_REQUIRED_COLUMNS)
    )
    rows = [
        ("P275_PHASE274_WORK_ORDER_PRESENT", "run_phase275_focused_capital_multiday_synthetic_followthrough_search" in phase274_next, phase274_next, "Phase274 next action targets Phase275", "hard"),
        ("P275_PHASE274_INTERPRETATION_COMPLETE", phase274_complete == 1, phase274_complete, "Phase274 complete", "hard"),
        ("P275_ROUTE_SCOPE_PROFILES_PRESENT", len(scope_profiles) > 0, len(scope_profiles), ">0 Phase274 route scope profiles", "hard"),
        ("P275_SYNTHETIC_MULTIDAY_ROWS_PRESENT", len(scenarios) > 0 and int(scenarios["observed_trade_dates"].min()) >= MIN_SYNTHETIC_DATES_FOR_MULTIDAY_DIAGNOSTIC, f"rows={len(scenarios)};min_dates={int(scenarios['observed_trade_dates'].min()) if not scenarios.empty else 0}", "scenarios cover multiple synthetic dates", "hard"),
        ("P275_ORDER_POLICY_STRESS_PRESENT", set(ORDER_POLICIES).issubset(set(scenarios["order_policy"].astype(str))) if not scenarios.empty else False, ";".join(sorted(scenarios["order_policy"].astype(str).unique())) if not scenarios.empty else "", "all Phase273 order policies retained", "hard"),
        ("P275_COST_STRESS_PRESENT", bool(not scenarios.empty and scenarios["cost_profile"].astype(str).eq("cost200").any()), ";".join(sorted(scenarios["cost_profile"].astype(str).unique())) if not scenarios.empty else "", "cost200 included", "hard"),
        ("P275_FULL_DEPTH_CONTRACT_PRESERVED", full_depth_material, "top5_rows_1_to_5_depth_columns_inherited_and_sample_ledger_persists_depth_materiality", "full top-five and levels 2-5 materiality required", "hard"),
        ("P275_BOUNDARIES_CLOSED", bool(not scenarios.empty and (scenarios["strategy_replay_allowed"].astype(int).eq(0).all()) and (scenarios["paper_or_live_acceptance_allowed"].astype(int).eq(0).all()) and (scenarios["deployable_profitability_claim_allowed"].astype(int).eq(0).all())), "replay=0;paper=0;deployable_claim=0", "no replay/paper/live/deployable claim", "hard"),
        ("P275_OUTCOME_CLASSIFIED", len(stability) > 0, len(stability), "scope/profile stability summary written whether positive or negative", "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def build_acceptance_summary(scenarios: pd.DataFrame, stability: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    best = scenarios.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0] if not scenarios.empty else pd.Series(dtype=object)
    cost100 = scenarios[scenarios["cost_profile"].astype(str).eq("cost100")] if not scenarios.empty else pd.DataFrame()
    cost200 = scenarios[scenarios["cost_profile"].astype(str).eq("cost200")] if not scenarios.empty else pd.DataFrame()
    cost200_stability = stability[stability["cost_profile"].astype(str).eq("cost200")] if not stability.empty else pd.DataFrame()
    next_action = NEXT_ACTION if hard_pass == len(hard) else REPAIR_ACTION
    rows = [
        ("phase275_multiday_synthetic_followthrough_search_complete", 1, "Phase275 multiday synthetic follow-through search completed"),
        ("phase275_selected_route", SELECTED_ROUTE, "Selected route"),
        ("phase275_scenario_rows", len(scenarios), "Synthetic multiday scenarios evaluated"),
        ("phase275_scope_profile_rows", int(scenarios["phase275_scope_profile_id"].astype(str).nunique()) if not scenarios.empty else 0, "Route scope/profile rows evaluated"),
        ("phase275_order_policy_rows", int(scenarios["order_policy"].astype(str).nunique()) if not scenarios.empty else 0, "Order policies evaluated"),
        ("phase275_synthetic_seed_rows", int(scenarios["synthetic_seed"].astype(str).nunique()) if not scenarios.empty else 0, "Synthetic seeds evaluated"),
        ("phase275_synthetic_regime_rows", int(scenarios["synthetic_regime"].astype(str).nunique()) if not scenarios.empty else 0, "Synthetic regimes evaluated"),
        ("phase275_synthetic_date_rows", int(scenarios["observed_trade_dates"].min()) if not scenarios.empty else 0, "Synthetic dates per scenario"),
        ("phase275_cost100_above12_scenario_rows", int(cost100["synthetic_multiday_above12_diagnostic"].astype(int).sum()) if not cost100.empty else 0, "Cost100 above-12 synthetic multiday diagnostic rows"),
        ("phase275_cost200_above12_scenario_rows", int(cost200["synthetic_multiday_above12_diagnostic"].astype(int).sum()) if not cost200.empty else 0, "Cost200 above-12 synthetic multiday diagnostic rows"),
        ("phase275_cost200_median_above12_scope_profile_rows", int(cost200_stability["median_above12"].astype(int).sum()) if not cost200_stability.empty else 0, "Cost200 scope/profile rows with median synthetic annualized return above 12%"),
        ("phase275_cost200_worst_case_above12_scope_profile_rows", int(cost200_stability["worst_case_above12"].astype(int).sum()) if not cost200_stability.empty else 0, "Cost200 scope/profile rows with worst synthetic annualized return above 12%"),
        ("phase275_best_scenario_id", best.get("scenario_id", ""), "Best synthetic multiday scenario"),
        ("phase275_best_scope_profile", best.get("phase275_scope_profile_id", ""), "Best synthetic multiday scope/profile"),
        ("phase275_best_order_policy", best.get("order_policy", ""), "Best order policy"),
        ("phase275_best_synthetic_regime", best.get("synthetic_regime", ""), "Best synthetic regime"),
        ("phase275_best_synthetic_seed", best.get("synthetic_seed", ""), "Best synthetic seed"),
        ("phase275_best_cost_profile", best.get("cost_profile", ""), "Best cost profile"),
        ("phase275_best_realized_net_pnl_inr", best.get("realized_net_pnl_inr", ""), "Best realized net P&L"),
        ("phase275_best_synthetic_multiday_annualized_portfolio_return_pct", best.get("mechanical_one_date_annualized_portfolio_return_pct", ""), "Best synthetic multiday annualized diagnostic"),
        ("phase275_best_scheduled_event_rows", best.get("scheduled_event_rows", ""), "Best scheduled event rows"),
        ("phase275_synthetic_multiday_diagnostic_allowed", int(len(scenarios) > 0 and int(scenarios["observed_trade_dates"].min()) >= MIN_SYNTHETIC_DATES_FOR_MULTIDAY_DIAGNOSTIC), "Synthetic multiday diagnostic is allowed"),
        ("phase275_portfolio_claim_allowed", 0, "Robust real portfolio claim remains closed"),
        ("phase275_strategy_replay_allowed", 0, "No strategy replay unlocked"),
        ("phase275_strategy_promotion_allowed", 0, "No strategy promotion unlocked"),
        ("phase275_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
        ("phase275_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        ("phase275_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase275_hard_gate_rows", len(hard), "Hard gates evaluated"),
        ("phase275_next_best_action", next_action, "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase275 Focused Capital Multiday Synthetic Follow-through Search",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase275 executes the Phase274-selected synthetic-only multiday follow-through.",
        "It bootstraps full-depth Phase268 event candidates into multiple synthetic sessions and evaluates the Phase273 capital-aware order-policy grid under cost and regime stress.",
        "",
        "This is deliberately not a real portfolio-return or deployable-profitability claim. It is a synthetic multiday diagnostic used to decide the next research move.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    phase268_dir: Path = DEFAULT_PHASE268_DIR,
    phase269_dir: Path = DEFAULT_PHASE269_DIR,
    phase274_dir: Path = DEFAULT_PHASE274_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase274_summary = read_csv(phase274_dir / "phase274_acceptance_summary.csv")
    if phase274_summary.empty:
        raise FileNotFoundError("Missing Phase274 acceptance summary.")
    scope_profiles = load_scope_profiles(phase274_dir)
    _, events, _ = load_candidate_events(phase268_dir, phase269_dir)
    scenarios, daily, sample_ledger = run_multiday_search(scope_profiles, events)
    stability = build_stability_summary(scenarios)
    gates = build_gate_evaluation(phase274_summary, scope_profiles, scenarios, stability, sample_ledger)
    acceptance = build_acceptance_summary(scenarios, stability, gates)

    scenarios.to_csv(output_dir / "phase275_multiday_synthetic_scenario_results.csv", index=False)
    daily.to_csv(output_dir / "phase275_daily_synthetic_scenario_results.csv", index=False)
    sample_ledger.to_csv(output_dir / "phase275_sample_synthetic_scheduled_event_ledger.csv", index=False)
    stability.to_csv(output_dir / "phase275_scope_profile_stability_summary.csv", index=False)
    gates.to_csv(output_dir / "phase275_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase275_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase275_focused_capital_multiday_synthetic_followthrough_search_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Scope/Profile Stability": stability,
            "Top Synthetic Scenarios": scenarios.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).head(20),
            "Daily Synthetic Scenario Sample": daily.head(20),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase275_focused_capital_multiday_synthetic_followthrough_search",
        **reproducibility_fields(
            artifact_id="phase275",
            generated_utc=generated_utc,
            inputs={
                "phase268_exploratory_event_ledger": str(phase268_dir / "phase268_exploratory_event_ledger.csv"),
                "phase269_ranked_annualized_research_leads": str(phase269_dir / "phase269_ranked_annualized_research_leads.csv"),
                "phase274_acceptance_summary": str(phase274_dir / "phase274_acceptance_summary.csv"),
                "phase274_next_route_contract": str(phase274_dir / "phase274_next_route_contract.csv"),
                "phase274_ranked_followthrough_scope_profiles": str(phase274_dir / "phase274_ranked_followthrough_scope_profiles.csv"),
            },
            parameters={
                "selected_route": SELECTED_ROUTE,
                "initial_capital_grid_inr": INITIAL_CAPITAL_GRID_INR,
                "fixed_notional_grid_inr": FIXED_NOTIONAL_GRID_INR,
                "max_concurrent_grid": MAX_CONCURRENT_GRID,
                "order_policies": ORDER_POLICIES,
                "synthetic_seed_rows": len(SYNTHETIC_SEEDS),
                "synthetic_date_rows": SYNTHETIC_DATE_ROWS,
                "synthetic_regimes": SYNTHETIC_REGIMES,
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "min_synthetic_dates_for_multiday_diagnostic": MIN_SYNTHETIC_DATES_FOR_MULTIDAY_DIAGNOSTIC,
                "full_depth_required_columns": FULL_DEPTH_REQUIRED_COLUMNS,
                "portfolio_claim_allowed": 0,
                "strategy_replay_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "multiday_synthetic_scenario_results": str(output_dir / "phase275_multiday_synthetic_scenario_results.csv"),
                "daily_synthetic_scenario_results": str(output_dir / "phase275_daily_synthetic_scenario_results.csv"),
                "sample_synthetic_scheduled_event_ledger": str(output_dir / "phase275_sample_synthetic_scheduled_event_ledger.csv"),
                "scope_profile_stability_summary": str(output_dir / "phase275_scope_profile_stability_summary.csv"),
                "gate_evaluation": str(output_dir / "phase275_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase275_acceptance_summary.csv"),
                "report": str(output_dir / "phase275_focused_capital_multiday_synthetic_followthrough_search_report.md"),
                "manifest": str(output_dir / "phase275_focused_capital_multiday_synthetic_followthrough_search_manifest.json"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase275_synthetic_multiday_no_new_live_latency",
        ),
    }
    (output_dir / "phase275_focused_capital_multiday_synthetic_followthrough_search_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase275 focused capital multiday synthetic follow-through search.")
    parser.add_argument("--phase268-dir", type=Path, default=DEFAULT_PHASE268_DIR)
    parser.add_argument("--phase269-dir", type=Path, default=DEFAULT_PHASE269_DIR)
    parser.add_argument("--phase274-dir", type=Path, default=DEFAULT_PHASE274_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase268_dir=args.phase268_dir, phase269_dir=args.phase269_dir, phase274_dir=args.phase274_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
