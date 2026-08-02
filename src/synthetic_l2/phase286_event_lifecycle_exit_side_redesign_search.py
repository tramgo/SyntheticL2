from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase255_richer_raw_depth_feature_quality_interpretation import safe_float
from synthetic_l2.phase271_fixed_capital_concurrency_and_capacity_return_analysis import schedule_events_for_scenario
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE277_DIR = Path("outputs/phase277")
DEFAULT_PHASE285_DIR = Path("outputs/phase285")
DEFAULT_OUTPUT_DIR = Path("outputs/phase286")

SELECTED_ROUTE = "P286_EVENT_LIFECYCLE_EXIT_SIDE_REDESIGN_SEARCH"
NEXT_ACTION = "run_phase287_event_lifecycle_exit_side_redesign_interpretation_no_paper_live"
REPAIR_ACTION = "repair_phase286_event_lifecycle_exit_side_redesign_search"

ANNUALIZED_THRESHOLD_PCT = 12.0
SPARSE_DIAGNOSTIC_EVENT_FLOOR = 8
ROBUST_PORTFOLIO_EVENT_FLOOR = 30
INITIAL_CAPITAL_INR = 100_000.0
COST_MULTIPLIER = 2.0
EXTRA_SLIPPAGE_BPS = 0.0


def q(frame: pd.DataFrame, col: str, quantile: float) -> float:
    return float(pd.to_numeric(frame[col], errors="coerce").fillna(0.0).quantile(quantile))


def normalize(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce").fillna(0.0)
    lo = float(values.min())
    hi = float(values.max())
    if hi <= lo:
        return pd.Series(0.0, index=series.index)
    return (values - lo) / (hi - lo)


def load_inputs(phase277_dir: Path, phase285_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    phase285_summary = read_csv(phase285_dir / "phase285_acceptance_summary.csv")
    lifecycle_families = read_csv(phase285_dir / "phase285_lifecycle_family_catalog.csv")
    grid = read_csv(phase285_dir / "phase285_entry_exit_grid_contract.csv")
    capital = read_csv(phase285_dir / "phase285_capital_cost_contract.csv")
    events = read_csv(phase277_dir / "phase277_cost200_redesign_event_universe.csv")
    if phase285_summary.empty:
        raise FileNotFoundError("Missing Phase285 acceptance summary.")
    if lifecycle_families.empty:
        raise FileNotFoundError("Missing Phase285 lifecycle family catalog.")
    if grid.empty:
        raise FileNotFoundError("Missing Phase285 entry/exit grid contract.")
    if capital.empty:
        raise FileNotFoundError("Missing Phase285 capital/cost contract.")
    if events.empty:
        raise FileNotFoundError("Missing Phase277 event universe.")
    return phase285_summary, lifecycle_families, grid, capital, events


def prepare_events(events: pd.DataFrame) -> pd.DataFrame:
    frame = events.copy()
    numeric_cols = [
        "richer_event_bar_id",
        "candidate_rank",
        "side",
        "horizon",
        "gross_edge_bps",
        "zerodha_round_trip_charge_bps",
        "avg_spread_bps",
        "avg_cum_top5_qty_imbalance",
        "avg_depth_beyond_l1_qty_imbalance",
        "avg_level_weighted_depth_imbalance",
        "depth_replenishment_pressure",
        "depth_withdrawal_pressure",
        "top5_churn_pressure",
        "depth_replenish_withdraw_ratio",
        "depth_consensus_imbalance",
        "event_sparsity_pressure",
    ]
    for col in numeric_cols:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
    frame = frame.sort_values(["trade_date", "exchange", "richer_event_bar_id", "candidate_rank", "candidate_id", "symbol"]).reset_index(drop=True)
    frame["base_horizon_ticks"] = frame["horizon"].astype(int)
    frame["uses_top5"] = 1
    frame["uses_levels_2_to_5"] = 1
    frame["l1_only_variant"] = 0
    frame["uses_net_edge_as_live_mask"] = 0
    return frame


def family_mask(events: pd.DataFrame, family_id: str) -> tuple[pd.Series, str]:
    spread_q50 = q(events, "avg_spread_bps", 0.50)
    spread_q75 = q(events, "avg_spread_bps", 0.75)
    churn_q50 = q(events, "top5_churn_pressure", 0.50)
    churn_q75 = q(events, "top5_churn_pressure", 0.75)
    withdrawal_q50 = q(events, "depth_withdrawal_pressure", 0.50)
    replenish_q50 = q(events, "depth_replenish_withdraw_ratio", 0.50)
    consensus_q50 = q(events, "depth_consensus_imbalance", 0.50)
    beyond_q50 = q(events, "avg_depth_beyond_l1_qty_imbalance", 0.50)
    if family_id == "P285_SIDE_FLIP_REVERSAL_TEST":
        mask = events["avg_depth_beyond_l1_qty_imbalance"].ge(beyond_q50)
        return mask, f"beyond_l1_imbalance>=q50({beyond_q50:.6f})"
    if family_id == "P285_ENTRY_DELAY_TEST":
        mask = events["top5_churn_pressure"].le(churn_q75) & events["avg_spread_bps"].le(spread_q75)
        return mask, f"churn<=q75({churn_q75:.6f}) and spread<=q75({spread_q75:.6f})"
    if family_id == "P285_SHORT_HORIZON_EXIT_TEST":
        mask = events["avg_spread_bps"].le(spread_q50) & events["depth_consensus_imbalance"].ge(consensus_q50)
        return mask, f"spread<=q50({spread_q50:.6f}) and consensus>=q50({consensus_q50:.6f})"
    if family_id == "P285_TAKE_PROFIT_STOP_TIMEOUT_TEST":
        mask = events["depth_replenish_withdraw_ratio"].ge(replenish_q50) & events["depth_withdrawal_pressure"].le(withdrawal_q50)
        return mask, f"replenish_withdraw>=q50({replenish_q50:.6f}) and withdrawal<=q50({withdrawal_q50:.6f})"
    if family_id == "P285_QUEUE_ADVERSITY_ORDER_TIMING_TEST":
        mask = (
            events["top5_churn_pressure"].le(churn_q50)
            & events["depth_withdrawal_pressure"].le(withdrawal_q50)
            & events["avg_depth_beyond_l1_qty_imbalance"].ge(beyond_q50)
        )
        return mask, f"churn<=q50({churn_q50:.6f}) and withdrawal<=q50({withdrawal_q50:.6f}) and beyond_l1>=q50({beyond_q50:.6f})"
    return pd.Series(False, index=events.index), "unknown family"


def adjusted_gross_edge(events: pd.DataFrame, grid_row: pd.Series) -> pd.Series:
    side_multiplier = safe_float(grid_row.get("side_multiplier", 1), 1.0)
    entry_delay = safe_float(grid_row.get("entry_delay_ticks", 0), 0.0)
    exit_horizon = max(1.0, safe_float(grid_row.get("exit_horizon_ticks", 10), 10.0))
    take_profit = grid_row.get("take_profit_bps", "")
    stop_loss = grid_row.get("stop_loss_bps", "")
    latency_bucket = str(grid_row.get("latency_bucket", "base"))

    horizon_factor = (exit_horizon / 10.0) ** 0.5
    churn_adversity = normalize(events["top5_churn_pressure"]) if "top5_churn_pressure" in events.columns else pd.Series(0.0, index=events.index)
    withdrawal_adversity = normalize(events["depth_withdrawal_pressure"]) if "depth_withdrawal_pressure" in events.columns else pd.Series(0.0, index=events.index)
    spread = pd.to_numeric(events["avg_spread_bps"], errors="coerce").fillna(0.0)
    delay_penalty = entry_delay * (0.20 * spread + 0.50 * churn_adversity + 0.35 * withdrawal_adversity)
    latency_penalty = (0.35 * spread + 0.50 * churn_adversity + 0.50 * withdrawal_adversity) if latency_bucket == "slow" else 0.0
    adjusted = side_multiplier * pd.to_numeric(events["gross_edge_bps"], errors="coerce").fillna(0.0) * horizon_factor - delay_penalty - latency_penalty
    if str(take_profit).strip() not in {"", "nan"}:
        adjusted = adjusted.clip(upper=safe_float(take_profit, 0.0))
    if str(stop_loss).strip() not in {"", "nan"}:
        adjusted = adjusted.clip(lower=-safe_float(stop_loss, 0.0))
    return adjusted


def build_variant_catalog(families: pd.DataFrame, grid: pd.DataFrame, events: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    rows: list[dict[str, Any]] = []
    variant_events: dict[str, pd.DataFrame] = {}
    for _, family in families.iterrows():
        if as_int(family.get("phase286_search_allowed", 0)) != 1:
            continue
        mask, rule = family_mask(events, str(family["lifecycle_family_id"]))
        family_events = events[mask].copy()
        for _, grid_row in grid.iterrows():
            if as_int(grid_row.get("phase286_search_allowed", 0)) != 1:
                continue
            variant_id = f"P286_{family['lifecycle_family_id']}_{grid_row['grid_id']}"
            frame = family_events.copy()
            if frame.empty:
                selected_rows = 0
            else:
                adjusted = adjusted_gross_edge(frame, grid_row)
                frame["candidate_id"] = variant_id
                frame["candidate_rank"] = 1
                frame["family_id"] = str(family["lifecycle_family_id"])
                frame["side"] = int(safe_float(grid_row.get("side_multiplier", 1), 1.0))
                frame["horizon"] = int(safe_float(grid_row.get("exit_horizon_ticks", 10), 10.0))
                frame["exit_bar_id"] = frame["richer_event_bar_id"].astype(int) + frame["horizon"].astype(int)
                frame["gross_edge_bps"] = adjusted
                frame["phase286_variant_id"] = variant_id
                frame["lifecycle_family_id"] = str(family["lifecycle_family_id"])
                frame["lifecycle_family"] = str(family["lifecycle_family"])
                frame["grid_id"] = str(grid_row["grid_id"])
                frame["entry_delay_ticks"] = int(safe_float(grid_row.get("entry_delay_ticks", 0), 0.0))
                frame["exit_horizon_ticks"] = int(safe_float(grid_row.get("exit_horizon_ticks", 10), 10.0))
                frame["side_multiplier"] = int(safe_float(grid_row.get("side_multiplier", 1), 1.0))
                frame["take_profit_bps"] = grid_row.get("take_profit_bps", "")
                frame["stop_loss_bps"] = grid_row.get("stop_loss_bps", "")
                frame["latency_bucket"] = str(grid_row.get("latency_bucket", "base"))
                frame["lifecycle_proxy_model"] = "phase286_horizon10_edge_transform_v1"
                selected_rows = len(frame)
            rows.append(
                {
                    "phase286_variant_id": variant_id,
                    "lifecycle_family_id": family["lifecycle_family_id"],
                    "lifecycle_family": family["lifecycle_family"],
                    "grid_id": grid_row["grid_id"],
                    "selection_rule": rule,
                    "selected_event_rows": selected_rows,
                    "side_multiplier": grid_row.get("side_multiplier", ""),
                    "entry_delay_ticks": grid_row.get("entry_delay_ticks", ""),
                    "exit_horizon_ticks": grid_row.get("exit_horizon_ticks", ""),
                    "take_profit_bps": grid_row.get("take_profit_bps", ""),
                    "stop_loss_bps": grid_row.get("stop_loss_bps", ""),
                    "latency_bucket": grid_row.get("latency_bucket", ""),
                    "uses_top5": 1,
                    "uses_levels_2_to_5": 1,
                    "l1_only_variant": 0,
                    "uses_net_edge_as_live_mask": 0,
                    "phase286_search_allowed": int(selected_rows > 0),
                }
            )
            if not frame.empty:
                variant_events[variant_id] = frame
    return pd.DataFrame(rows), variant_events


def parse_contract_grid(capital: pd.DataFrame, contract_id: str, default: list[float]) -> list[float]:
    if capital.empty:
        return default
    rows = capital.loc[capital["contract_id"].astype(str).eq(contract_id), "contract_value"]
    if rows.empty:
        return default
    values = []
    for item in str(rows.iloc[0]).split(";"):
        item = item.strip()
        if not item:
            continue
        values.append(float(item))
    return values or default


def build_scenarios(variant_catalog: pd.DataFrame, variant_events: dict[str, pd.DataFrame], capital: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    fixed_notionals = parse_contract_grid(capital, "P285_FIXED_NOTIONAL_GRID_INR", [25_000.0, 50_000.0, 75_000.0, 100_000.0])
    max_concurrency = [int(x) for x in parse_contract_grid(capital, "P285_MAX_CONCURRENT_GRID", [1, 2, 4])]
    scenarios: list[dict[str, Any]] = []
    ledgers: list[pd.DataFrame] = []
    meta = variant_catalog.set_index("phase286_variant_id").to_dict(orient="index") if not variant_catalog.empty else {}
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
                info = meta.get(variant_id, {})
                scenario.update(
                    {
                        "phase286_variant_id": variant_id,
                        "lifecycle_family_id": info.get("lifecycle_family_id", ""),
                        "lifecycle_family": info.get("lifecycle_family", ""),
                        "grid_id": info.get("grid_id", ""),
                        "selected_event_rows": info.get("selected_event_rows", 0),
                        "side_multiplier": info.get("side_multiplier", ""),
                        "entry_delay_ticks": info.get("entry_delay_ticks", ""),
                        "exit_horizon_ticks": info.get("exit_horizon_ticks", ""),
                        "take_profit_bps": info.get("take_profit_bps", ""),
                        "stop_loss_bps": info.get("stop_loss_bps", ""),
                        "latency_bucket": info.get("latency_bucket", ""),
                        "uses_top5": 1,
                        "uses_levels_2_to_5": 1,
                        "l1_only_variant": 0,
                        "uses_net_edge_as_live_mask": 0,
                        "lifecycle_proxy_model": "phase286_horizon10_edge_transform_v1",
                    }
                )
                scenario["sparse_diagnostic_event_floor_met"] = int(int(scenario["scheduled_event_rows"]) >= SPARSE_DIAGNOSTIC_EVENT_FLOOR)
                scenario["robust_portfolio_event_floor_met"] = int(int(scenario["scheduled_event_rows"]) >= ROBUST_PORTFOLIO_EVENT_FLOOR)
                scenario["cost200_above12_sparse_diagnostic"] = int(
                    float(scenario["mechanical_one_date_annualized_portfolio_return_pct"]) > ANNUALIZED_THRESHOLD_PCT
                    and int(scenario["scheduled_event_rows"]) >= SPARSE_DIAGNOSTIC_EVENT_FLOOR
                )
                scenario["robust_portfolio_floor_above12"] = int(
                    float(scenario["mechanical_one_date_annualized_portfolio_return_pct"]) > ANNUALIZED_THRESHOLD_PCT
                    and int(scenario["scheduled_event_rows"]) >= ROBUST_PORTFOLIO_EVENT_FLOOR
                )
                scenarios.append(scenario)
                if not ledger.empty:
                    ledger = ledger.copy()
                    ledger["phase286_variant_id"] = variant_id
                    ledger["lifecycle_family"] = info.get("lifecycle_family", "")
                    ledger["grid_id"] = info.get("grid_id", "")
                    ledgers.append(ledger)
    return pd.DataFrame(scenarios), pd.concat(ledgers, ignore_index=True) if ledgers else pd.DataFrame()


def summarize_variants(scenarios: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame()
    frame = scenarios.copy()
    numeric_cols = [
        "mechanical_one_date_annualized_portfolio_return_pct",
        "realized_net_pnl_inr",
        "scheduled_event_rows",
        "selected_event_rows",
        "cost200_above12_sparse_diagnostic",
        "robust_portfolio_floor_above12",
        "sparse_diagnostic_event_floor_met",
        "robust_portfolio_event_floor_met",
    ]
    for col in numeric_cols:
        frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
    grouped = frame.groupby(["phase286_variant_id", "lifecycle_family", "grid_id"], dropna=False).agg(
        scenario_rows=("scenario_id", "count"),
        selected_event_rows=("selected_event_rows", "max"),
        max_scheduled_event_rows=("scheduled_event_rows", "max"),
        cost200_above12_sparse_diagnostic_rows=("cost200_above12_sparse_diagnostic", "sum"),
        robust_portfolio_floor_above12_rows=("robust_portfolio_floor_above12", "sum"),
        sparse_floor_met_rows=("sparse_diagnostic_event_floor_met", "sum"),
        robust_portfolio_floor_met_rows=("robust_portfolio_event_floor_met", "sum"),
        min_annualized_pct=("mechanical_one_date_annualized_portfolio_return_pct", "min"),
        median_annualized_pct=("mechanical_one_date_annualized_portfolio_return_pct", "median"),
        max_annualized_pct=("mechanical_one_date_annualized_portfolio_return_pct", "max"),
        max_net_pnl_inr=("realized_net_pnl_inr", "max"),
    ).reset_index()
    return grouped.sort_values(
        ["robust_portfolio_floor_above12_rows", "cost200_above12_sparse_diagnostic_rows", "max_annualized_pct", "max_scheduled_event_rows"],
        ascending=[False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_gate_evaluation(phase285_summary: pd.DataFrame, variant_catalog: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(phase285_summary, "phase285_lifecycle_redesign_precommit_complete", 0))
    next_action = str(metric_value(phase285_summary, "phase285_next_best_action", ""))
    cost_required = as_int(metric_value(phase285_summary, "phase285_cost200_required", 0))
    fixed_required = as_int(metric_value(phase285_summary, "phase285_fixed_capital_required", 0))
    full_depth = as_int(metric_value(phase285_summary, "phase285_full_depth_required", 0))
    replay_allowed = as_int(metric_value(phase285_summary, "phase285_strategy_replay_allowed", 1))
    paper_allowed = as_int(metric_value(phase285_summary, "phase285_paper_or_live_acceptance_allowed", 1))
    claim_allowed = as_int(metric_value(phase285_summary, "phase285_deployable_profitability_claim_allowed", 1))
    l1_only = int(pd.to_numeric(variant_catalog.get("l1_only_variant", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not variant_catalog.empty else 1
    live_mask = int(pd.to_numeric(variant_catalog.get("uses_net_edge_as_live_mask", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not variant_catalog.empty else 1
    scenario_l1 = int(pd.to_numeric(scenarios.get("l1_only_variant", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not scenarios.empty else 1
    scenario_live_mask = int(pd.to_numeric(scenarios.get("uses_net_edge_as_live_mask", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not scenarios.empty else 1
    rows = [
        ("P286_PHASE285_WORK_ORDER_PRESENT", "run_phase286_event_lifecycle_exit_side_redesign_search" in next_action, next_action, "Phase285 next action targets Phase286", "hard"),
        ("P286_PHASE285_PRECOMMIT_COMPLETE", complete == 1, complete, "Phase285 complete", "hard"),
        ("P286_VARIANTS_PRESENT", len(variant_catalog) >= 60, len(variant_catalog), ">=60 lifecycle variants", "hard"),
        ("P286_SCENARIOS_PRESENT", len(scenarios) >= 700, len(scenarios), ">=700 cost200 fixed-capital scenarios", "hard"),
        ("P286_COST_AND_FIXED_CAPITAL_REQUIRED", cost_required == 1 and fixed_required == 1, f"cost200={cost_required};fixed_capital={fixed_required}", "cost200 fixed-capital scoring", "hard"),
        ("P286_FULL_DEPTH_REQUIRED", full_depth == 1 and l1_only == 0 and scenario_l1 == 0, f"full_depth={full_depth};catalog_l1={l1_only};scenario_l1={scenario_l1}", "full-depth with L1-only forbidden", "hard"),
        ("P286_NO_LIVE_NET_EDGE_MASKS", live_mask == 0 and scenario_live_mask == 0, f"catalog_live_mask={live_mask};scenario_live_mask={scenario_live_mask}", "net/gross edge not used as live masks", "hard"),
        ("P286_BOUNDARIES_CLOSED", replay_allowed == 0 and paper_allowed == 0 and claim_allowed == 0, f"replay={replay_allowed};paper={paper_allowed};claim={claim_allowed}", "no replay/paper/live/claim", "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def build_acceptance_summary(variant_catalog: pd.DataFrame, scenarios: pd.DataFrame, variant_summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    best = scenarios.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0] if not scenarios.empty else pd.Series(dtype=object)
    sparse = int(pd.to_numeric(scenarios.get("cost200_above12_sparse_diagnostic", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not scenarios.empty else 0
    robust_above12 = int(pd.to_numeric(scenarios.get("robust_portfolio_floor_above12", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not scenarios.empty else 0
    robust_floor = int(pd.to_numeric(scenarios.get("robust_portfolio_event_floor_met", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not scenarios.empty else 0
    next_action = NEXT_ACTION if hard_pass == len(hard) else REPAIR_ACTION
    rows = [
        ("phase286_lifecycle_redesign_search_complete", 1, "Phase286 lifecycle/side/exit redesign search completed"),
        ("phase286_selected_route", SELECTED_ROUTE, "Selected route"),
        ("phase286_variant_rows", len(variant_catalog), "Lifecycle variants evaluated"),
        ("phase286_scenario_rows", len(scenarios), "Cost200 fixed-capital scenarios evaluated"),
        ("phase286_sparse_above12_scenario_rows", sparse, "Cost200 above-12 sparse diagnostic rows with event floor met"),
        ("phase286_robust_portfolio_floor_scenario_rows", robust_floor, "Scenarios meeting robust portfolio event floor"),
        ("phase286_robust_portfolio_above12_scenario_rows", robust_above12, "Robust floor scenarios above 12 percent"),
        ("phase286_best_variant_id", best.get("phase286_variant_id", ""), "Best Phase286 variant"),
        ("phase286_best_lifecycle_family", best.get("lifecycle_family", ""), "Best lifecycle family"),
        ("phase286_best_grid_id", best.get("grid_id", ""), "Best lifecycle grid"),
        ("phase286_best_cost200_annualized_pct", best.get("mechanical_one_date_annualized_portfolio_return_pct", ""), "Best cost200 annualized diagnostic"),
        ("phase286_best_realized_net_pnl_inr", best.get("realized_net_pnl_inr", ""), "Best realized net P&L"),
        ("phase286_best_scheduled_event_rows", best.get("scheduled_event_rows", ""), "Best scheduled event rows"),
        ("phase286_l1_only_variant_rows", int(pd.to_numeric(variant_catalog.get("l1_only_variant", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not variant_catalog.empty else 0, "L1-only variants"),
        ("phase286_net_edge_live_mask_rows", int(pd.to_numeric(variant_catalog.get("uses_net_edge_as_live_mask", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not variant_catalog.empty else 0, "Live masks using net/gross edge"),
        ("phase286_strategy_replay_allowed", 0, "No strategy replay unlocked"),
        ("phase286_strategy_promotion_allowed", 0, "No strategy promotion unlocked"),
        ("phase286_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
        ("phase286_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        ("phase286_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase286_hard_gate_rows", len(hard), "Hard gates evaluated"),
        ("phase286_next_best_action", next_action, "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase286 Event Lifecycle / Side / Exit Redesign Search",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase286 executes the Phase285 lifecycle/side/exit search contract using observable full-depth L2 masks and a fixed-capital cost200 scheduler.",
        "The edge transform is a lifecycle proxy derived from the available horizon-10 synthetic gross-edge field; this is not a raw tick-path replay.",
        "Full top-five depth and beyond-L1 materiality remain mandatory, and no replay/paper/live/profitability claim is unlocked by this phase.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase277_dir: Path = DEFAULT_PHASE277_DIR, phase285_dir: Path = DEFAULT_PHASE285_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase285_summary, families, grid, capital, raw_events = load_inputs(phase277_dir, phase285_dir)
    events = prepare_events(raw_events)
    variant_catalog, variant_events = build_variant_catalog(families, grid, events)
    scenarios, ledger = build_scenarios(variant_catalog, variant_events, capital)
    variant_summary = summarize_variants(scenarios)
    gates = build_gate_evaluation(phase285_summary, variant_catalog, scenarios)
    acceptance = build_acceptance_summary(variant_catalog, scenarios, variant_summary, gates)

    variant_catalog.to_csv(output_dir / "phase286_lifecycle_variant_catalog.csv", index=False)
    scenarios.to_csv(output_dir / "phase286_lifecycle_scenario_results.csv", index=False)
    variant_summary.to_csv(output_dir / "phase286_lifecycle_variant_summary.csv", index=False)
    ledger.head(5000).to_csv(output_dir / "phase286_sample_lifecycle_scheduled_event_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase286_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase286_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase286_event_lifecycle_exit_side_redesign_search_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Top Scenarios": scenarios.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).head(25),
            "Variant Summary": variant_summary.head(25),
            "Variant Catalog": variant_catalog.head(25),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase286_event_lifecycle_exit_side_redesign_search",
        **reproducibility_fields(
            artifact_id="phase286",
            generated_utc=generated_utc,
            inputs={
                "phase285_acceptance_summary": str(phase285_dir / "phase285_acceptance_summary.csv"),
                "phase285_lifecycle_family_catalog": str(phase285_dir / "phase285_lifecycle_family_catalog.csv"),
                "phase285_entry_exit_grid_contract": str(phase285_dir / "phase285_entry_exit_grid_contract.csv"),
                "phase285_capital_cost_contract": str(phase285_dir / "phase285_capital_cost_contract.csv"),
                "phase277_event_universe": str(phase277_dir / "phase277_cost200_redesign_event_universe.csv"),
            },
            parameters={
                "selected_route": SELECTED_ROUTE,
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "sparse_diagnostic_event_floor": SPARSE_DIAGNOSTIC_EVENT_FLOOR,
                "robust_portfolio_event_floor": ROBUST_PORTFOLIO_EVENT_FLOOR,
                "initial_capital_inr": INITIAL_CAPITAL_INR,
                "cost_multiplier": COST_MULTIPLIER,
                "extra_slippage_bps": EXTRA_SLIPPAGE_BPS,
                "lifecycle_proxy_model": "phase286_horizon10_edge_transform_v1",
                "strategy_replay_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "variant_catalog": str(output_dir / "phase286_lifecycle_variant_catalog.csv"),
                "scenario_results": str(output_dir / "phase286_lifecycle_scenario_results.csv"),
                "variant_summary": str(output_dir / "phase286_lifecycle_variant_summary.csv"),
                "sample_scheduled_event_ledger": str(output_dir / "phase286_sample_lifecycle_scheduled_event_ledger.csv"),
                "gate_evaluation": str(output_dir / "phase286_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase286_acceptance_summary.csv"),
                "report": str(output_dir / "phase286_event_lifecycle_exit_side_redesign_search_report.md"),
                "manifest": str(output_dir / "phase286_event_lifecycle_exit_side_redesign_search_manifest.json"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase286_lifecycle_proxy_latency_bucket_v1",
        ),
    }
    (output_dir / "phase286_event_lifecycle_exit_side_redesign_search_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase286 event lifecycle / side / exit redesign search.")
    parser.add_argument("--phase277-dir", type=Path, default=DEFAULT_PHASE277_DIR)
    parser.add_argument("--phase285-dir", type=Path, default=DEFAULT_PHASE285_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase277_dir=args.phase277_dir, phase285_dir=args.phase285_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
