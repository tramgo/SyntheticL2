from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE277_DIR = Path("outputs/phase277")
DEFAULT_PHASE283_DIR = Path("outputs/phase283")
DEFAULT_PHASE284_DIR = Path("outputs/phase284")
DEFAULT_OUTPUT_DIR = Path("outputs/phase285")

SELECTED_ROUTE = "P285_EVENT_LIFECYCLE_EXIT_SIDE_REDESIGN_PRECOMMIT"
NEXT_ACTION = "run_phase286_event_lifecycle_exit_side_redesign_search_no_paper_live"
REPAIR_ACTION = "repair_phase285_event_lifecycle_exit_side_redesign_precommit"

ANNUALIZED_THRESHOLD_PCT = 12.0
TARGET_COST_PROFILE = "cost200"
SPARSE_DIAGNOSTIC_EVENT_FLOOR = 8
ROBUST_PORTFOLIO_EVENT_FLOOR = 30
INITIAL_CAPITAL_INR = 100_000.0
FIXED_NOTIONAL_GRID_INR = [25_000.0, 50_000.0, 75_000.0, 100_000.0]
MAX_CONCURRENT_GRID = [1, 2, 4]


LIFECYCLE_FAMILIES: list[dict[str, Any]] = [
    {
        "lifecycle_family_id": "P285_SIDE_FLIP_REVERSAL_TEST",
        "lifecycle_family": "side_flip_reversal_test",
        "primary_change": "test whether the sparse follow-through clue is actually a reversal edge after entry costs",
        "side_policy": "original;inverse",
        "entry_policy": "same_event",
        "exit_policy": "fixed_horizon",
    },
    {
        "lifecycle_family_id": "P285_ENTRY_DELAY_TEST",
        "lifecycle_family": "entry_delay_test",
        "primary_change": "delay entry by one or more ticks/bars to avoid immediate adverse selection after the L2 signal",
        "side_policy": "original;inverse",
        "entry_policy": "delay_1;delay_2;delay_3",
        "exit_policy": "fixed_horizon",
    },
    {
        "lifecycle_family_id": "P285_SHORT_HORIZON_EXIT_TEST",
        "lifecycle_family": "short_horizon_exit_test",
        "primary_change": "test whether edge exists before the current horizon leaks away",
        "side_policy": "original;inverse",
        "entry_policy": "same_event;delay_1",
        "exit_policy": "horizon_3;horizon_5;horizon_8",
    },
    {
        "lifecycle_family_id": "P285_TAKE_PROFIT_STOP_TIMEOUT_TEST",
        "lifecycle_family": "take_profit_stop_timeout_test",
        "primary_change": "bound tail losses and harvest early positive excursions instead of waiting for a fixed exit only",
        "side_policy": "original;inverse",
        "entry_policy": "same_event;delay_1",
        "exit_policy": "take_profit_4_8_bps;stop_loss_4_8_bps;timeout_horizon_5_10",
    },
    {
        "lifecycle_family_id": "P285_QUEUE_ADVERSITY_ORDER_TIMING_TEST",
        "lifecycle_family": "queue_adversity_order_timing_test",
        "primary_change": "stress order arrival timing and queue adversity rather than assuming the signal can trade instantly",
        "side_policy": "original;inverse",
        "entry_policy": "latency_bucket_fast;latency_bucket_slow",
        "exit_policy": "fixed_horizon;timeout_horizon_5_10",
    },
]


ENTRY_EXIT_GRID: list[dict[str, Any]] = [
    {"grid_id": "P285_GRID_ORIG_E0_H3", "side_multiplier": 1, "entry_delay_ticks": 0, "exit_horizon_ticks": 3, "take_profit_bps": "", "stop_loss_bps": "", "latency_bucket": "base"},
    {"grid_id": "P285_GRID_ORIG_E0_H5", "side_multiplier": 1, "entry_delay_ticks": 0, "exit_horizon_ticks": 5, "take_profit_bps": "", "stop_loss_bps": "", "latency_bucket": "base"},
    {"grid_id": "P285_GRID_ORIG_E1_H5", "side_multiplier": 1, "entry_delay_ticks": 1, "exit_horizon_ticks": 5, "take_profit_bps": "", "stop_loss_bps": "", "latency_bucket": "base"},
    {"grid_id": "P285_GRID_ORIG_E2_H8", "side_multiplier": 1, "entry_delay_ticks": 2, "exit_horizon_ticks": 8, "take_profit_bps": "", "stop_loss_bps": "", "latency_bucket": "slow"},
    {"grid_id": "P285_GRID_INV_E0_H3", "side_multiplier": -1, "entry_delay_ticks": 0, "exit_horizon_ticks": 3, "take_profit_bps": "", "stop_loss_bps": "", "latency_bucket": "base"},
    {"grid_id": "P285_GRID_INV_E0_H5", "side_multiplier": -1, "entry_delay_ticks": 0, "exit_horizon_ticks": 5, "take_profit_bps": "", "stop_loss_bps": "", "latency_bucket": "base"},
    {"grid_id": "P285_GRID_INV_E1_H5", "side_multiplier": -1, "entry_delay_ticks": 1, "exit_horizon_ticks": 5, "take_profit_bps": "", "stop_loss_bps": "", "latency_bucket": "base"},
    {"grid_id": "P285_GRID_INV_E2_H8", "side_multiplier": -1, "entry_delay_ticks": 2, "exit_horizon_ticks": 8, "take_profit_bps": "", "stop_loss_bps": "", "latency_bucket": "slow"},
    {"grid_id": "P285_GRID_ORIG_TP4_SL4_H5", "side_multiplier": 1, "entry_delay_ticks": 0, "exit_horizon_ticks": 5, "take_profit_bps": 4, "stop_loss_bps": 4, "latency_bucket": "base"},
    {"grid_id": "P285_GRID_ORIG_TP8_SL4_H10", "side_multiplier": 1, "entry_delay_ticks": 1, "exit_horizon_ticks": 10, "take_profit_bps": 8, "stop_loss_bps": 4, "latency_bucket": "slow"},
    {"grid_id": "P285_GRID_INV_TP4_SL4_H5", "side_multiplier": -1, "entry_delay_ticks": 0, "exit_horizon_ticks": 5, "take_profit_bps": 4, "stop_loss_bps": 4, "latency_bucket": "base"},
    {"grid_id": "P285_GRID_INV_TP8_SL4_H10", "side_multiplier": -1, "entry_delay_ticks": 1, "exit_horizon_ticks": 10, "take_profit_bps": 8, "stop_loss_bps": 4, "latency_bucket": "slow"},
]


def parse_contract_value(route: pd.DataFrame, contract_id: str) -> str:
    if route.empty:
        return ""
    rows = route.loc[route["contract_id"].astype(str).eq(contract_id), "contract_value"]
    return "" if rows.empty else str(rows.iloc[0])


def split_contract_values(value: str) -> list[str]:
    return [item.strip() for item in str(value).split(";") if item.strip()]


def load_inputs(
    phase277_dir: Path,
    phase283_dir: Path,
    phase284_dir: Path,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    phase284_summary = read_csv(phase284_dir / "phase284_acceptance_summary.csv")
    phase284_route = read_csv(phase284_dir / "phase284_next_route_contract.csv")
    ranked_ensembles = read_csv(phase284_dir / "phase284_ranked_ensemble_interpretation.csv")
    event_universe = read_csv(phase277_dir / "phase277_cost200_redesign_event_universe.csv")
    scheduled_ledger = read_csv(phase283_dir / "phase283_sample_regime_conditioned_scheduled_event_ledger.csv")
    if phase284_summary.empty:
        raise FileNotFoundError("Missing Phase284 acceptance summary.")
    if phase284_route.empty:
        raise FileNotFoundError("Missing Phase284 next route contract.")
    if ranked_ensembles.empty:
        raise FileNotFoundError("Missing Phase284 ranked ensemble interpretation.")
    if event_universe.empty:
        raise FileNotFoundError("Missing Phase277 event universe.")
    if scheduled_ledger.empty:
        raise FileNotFoundError("Missing Phase283 scheduled event ledger.")
    return phase284_summary, phase284_route, ranked_ensembles, event_universe, scheduled_ledger


def build_preserved_clue_catalog(route: pd.DataFrame, ranked_ensembles: pd.DataFrame) -> pd.DataFrame:
    preserved = set(split_contract_values(parse_contract_value(route, "P285_PRESERVED_PHASE283_CLUES")))
    frame = ranked_ensembles[ranked_ensembles["phase283_variant_id"].astype(str).isin(preserved)].copy()
    if frame.empty:
        frame = ranked_ensembles.head(10).copy()
    numeric_cols = [
        "max_annualized_pct",
        "median_annualized_pct",
        "min_annualized_pct",
        "max_scheduled_event_rows",
        "selected_event_rows",
        "cost200_above12_sparse_diagnostic_rows",
        "sparse_floor_met_rows",
        "robust_portfolio_floor_met_rows",
        "full_depth_positive_clue",
        "near_miss_under_12",
        "too_sparse_for_portfolio_claim",
        "uses_top5",
        "uses_levels_2_to_5",
        "l1_only_variant",
        "uses_net_edge_as_live_mask",
    ]
    for col in numeric_cols:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
    frame["preserve_as_lifecycle_seed_not_acceptance"] = 1
    frame["eligible_for_phase286_lifecycle_seed"] = (
        frame["full_depth_positive_clue"].astype(int).eq(1)
        & frame["l1_only_variant"].astype(int).eq(0)
        & frame["uses_net_edge_as_live_mask"].astype(int).eq(0)
        & frame["uses_levels_2_to_5"].astype(int).eq(1)
    ).astype(int)
    cols = [
        "phase283_variant_id",
        "ensemble_family_id",
        "ensemble_family",
        "bucket_id",
        "vote_threshold",
        "seed_ids",
        "included_target_families",
        "max_annualized_pct",
        "median_annualized_pct",
        "max_scheduled_event_rows",
        "selected_event_rows",
        "cost200_above12_sparse_diagnostic_rows",
        "sparse_floor_met_rows",
        "robust_portfolio_floor_met_rows",
        "full_depth_positive_clue",
        "near_miss_under_12",
        "too_sparse_for_portfolio_claim",
        "uses_top5",
        "uses_levels_2_to_5",
        "l1_only_variant",
        "uses_net_edge_as_live_mask",
        "preserve_as_lifecycle_seed_not_acceptance",
        "eligible_for_phase286_lifecycle_seed",
    ]
    return frame[[col for col in cols if col in frame.columns]].reset_index(drop=True)


def build_event_universe_diagnostics(event_universe: pd.DataFrame, scheduled_ledger: pd.DataFrame) -> pd.DataFrame:
    universe = event_universe.copy()
    ledger = scheduled_ledger.copy()
    for frame in (universe, ledger):
        for col in ["net_edge_bps", "gross_edge_bps", "avg_spread_bps", "richer_event_bar_id", "horizon"]:
            if col in frame.columns:
                frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
    scheduled = ledger[ledger.get("decision", "").astype(str).eq("scheduled")] if "decision" in ledger.columns else ledger
    rejected = ledger[ledger.get("decision", "").astype(str).eq("rejected")] if "decision" in ledger.columns else pd.DataFrame()
    rejection_counts = rejected["rejection_reason"].astype(str).value_counts().to_dict() if not rejected.empty and "rejection_reason" in rejected.columns else {}
    rows = [
        ("event_universe_rows", len(universe), "Phase277 full-depth event universe rows"),
        ("event_universe_dates", int(universe["trade_date"].astype(str).nunique()) if "trade_date" in universe.columns else 0, "Distinct event-universe dates"),
        ("event_universe_symbols", int(universe["symbol"].astype(str).nunique()) if "symbol" in universe.columns else 0, "Distinct event-universe symbols"),
        ("event_universe_median_spread_bps", float(universe["avg_spread_bps"].median()) if "avg_spread_bps" in universe.columns else "", "Median event-universe spread"),
        ("event_universe_positive_net_edge_rows", int((universe["net_edge_bps"] > 0.0).sum()) if "net_edge_bps" in universe.columns else 0, "Rows with positive inherited net edge"),
        ("phase283_ledger_rows", len(ledger), "Phase283 scheduled/rejected ledger rows sampled"),
        ("phase283_scheduled_rows", len(scheduled), "Phase283 scheduled rows in ledger"),
        ("phase283_rejected_rows", len(rejected), "Phase283 rejected rows in ledger"),
        ("phase283_rejected_same_symbol_overlap_rows", int(rejection_counts.get("same_symbol_overlap", 0)), "Rejected same-symbol overlap rows"),
        ("phase283_rejected_max_concurrent_rows", int(rejection_counts.get("max_concurrent_positions", 0)), "Rejected max-concurrent rows"),
        ("phase283_scheduled_median_net_edge_bps", float(scheduled["net_edge_bps"].median()) if not scheduled.empty and "net_edge_bps" in scheduled.columns else "", "Median scheduled net edge in Phase283 ledger"),
    ]
    return pd.DataFrame(rows, columns=["diagnostic_id", "diagnostic_value", "description"])


def build_lifecycle_family_catalog(clues: pd.DataFrame, diagnostics: pd.DataFrame) -> pd.DataFrame:
    eligible_seed_rows = int(clues["eligible_for_phase286_lifecycle_seed"].astype(int).sum()) if not clues.empty else 0
    rows: list[dict[str, Any]] = []
    for family in LIFECYCLE_FAMILIES:
        rows.append(
            {
                **family,
                "eligible_seed_rows": eligible_seed_rows,
                "cost_profile_required": TARGET_COST_PROFILE,
                "fixed_capital_required": 1,
                "full_depth_required": 1,
                "levels_2_to_5_required": 1,
                "beyond_l1_features_required": 1,
                "l1_only_allowed": 0,
                "net_edge_live_mask_allowed": 0,
                "phase286_search_allowed": int(eligible_seed_rows > 0 and len(diagnostics) > 0),
            }
        )
    return pd.DataFrame(rows)


def build_entry_exit_grid_contract() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for item in ENTRY_EXIT_GRID:
        rows.append(
            {
                **item,
                "cost_profile_required": TARGET_COST_PROFILE,
                "fixed_capital_initial_capital_inr": INITIAL_CAPITAL_INR,
                "full_depth_required": 1,
                "phase286_search_allowed": 1,
            }
        )
    return pd.DataFrame(rows)


def build_capital_cost_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("P285_INITIAL_CAPITAL_INR", str(INITIAL_CAPITAL_INR), "Fixed capital denominator for Phase286 diagnostics", "hard"),
            ("P285_FIXED_NOTIONAL_GRID_INR", ";".join(str(int(x)) for x in FIXED_NOTIONAL_GRID_INR), "Fixed notional grid for lifecycle search", "hard"),
            ("P285_MAX_CONCURRENT_GRID", ";".join(str(x) for x in MAX_CONCURRENT_GRID), "Concurrency grid to reduce two-trade bottleneck diagnostics", "hard"),
            ("P285_COST200_REQUIRED", "Zerodha cost200 required for all acceptance diagnostics", "hard"),
            ("P285_ANNUALIZED_FORMULA", "realized_net_pnl / initial_capital * 100 * 252 / observed_trade_dates", "Fixed-capital annualized diagnostic formula", "hard"),
            ("P285_SPARSE_DIAGNOSTIC_EVENT_FLOOR", str(SPARSE_DIAGNOSTIC_EVENT_FLOOR), "Minimum scheduled events for sparse >12 diagnostic", "hard"),
            ("P285_ROBUST_PORTFOLIO_EVENT_FLOOR", str(ROBUST_PORTFOLIO_EVENT_FLOOR), "Minimum scheduled events for robust portfolio-return claim", "hard"),
            ("P285_NO_PROMOTION", "no replay, promotion, paper/live, or deployable profitability claim", "Boundaries remain closed", "hard"),
        ],
        columns=["contract_id", "contract_value", "description", "severity"],
    )


def build_next_route_contract(clues: pd.DataFrame, families: pd.DataFrame, grid: pd.DataFrame) -> pd.DataFrame:
    clue_ids = ";".join(clues.loc[clues["eligible_for_phase286_lifecycle_seed"].astype(int).eq(1), "phase283_variant_id"].astype(str).tolist()) if not clues.empty else ""
    family_ids = ";".join(families.loc[families["phase286_search_allowed"].astype(int).eq(1), "lifecycle_family_id"].astype(str).tolist()) if not families.empty else ""
    grid_ids = ";".join(grid.loc[grid["phase286_search_allowed"].astype(int).eq(1), "grid_id"].astype(str).tolist()) if not grid.empty else ""
    return pd.DataFrame(
        [
            ("P286_INPUTS", "outputs/phase277/phase277_cost200_redesign_event_universe.csv;outputs/phase285/phase285_preserved_phase283_clue_catalog.csv;outputs/phase285/phase285_lifecycle_family_catalog.csv;outputs/phase285/phase285_entry_exit_grid_contract.csv", "Use full-depth event universe plus Phase285 lifecycle contract."),
            ("P286_LIFECYCLE_SEEDS", clue_ids, "Use preserved Phase283 full-depth near-misses only as search seeds."),
            ("P286_LIFECYCLE_FAMILIES", family_ids, "Execute allowed lifecycle families."),
            ("P286_ENTRY_EXIT_GRIDS", grid_ids, "Execute side/entry/exit/take-profit/stop/latency grid."),
            ("P286_SEARCH_TYPE", "event_lifecycle_exit_side_redesign_search", "Execute lifecycle search next."),
            ("P286_ACCEPTANCE_DIAGNOSTICS", f"cost200_annualized_pct_gt_{ANNUALIZED_THRESHOLD_PCT};scheduled_event_rows_ge_{SPARSE_DIAGNOSTIC_EVENT_FLOOR}_for_sparse_diagnostic;scheduled_event_rows_ge_{ROBUST_PORTFOLIO_EVENT_FLOOR}_for_portfolio_claim", "Sparse >12 is a discovery clue; robust portfolio claim needs the larger event floor."),
            ("P286_BOUNDARY", "no_paper_live;no_strategy_replay;no_deployable_profitability_claim;fixed_capital_required;full_depth_required;l1_only_forbidden;net_edge_live_mask_forbidden", "Boundaries remain closed."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def build_gate_evaluation(
    phase284_summary: pd.DataFrame,
    route: pd.DataFrame,
    clues: pd.DataFrame,
    diagnostics: pd.DataFrame,
    families: pd.DataFrame,
    grid: pd.DataFrame,
    capital_cost: pd.DataFrame,
    next_route: pd.DataFrame,
) -> pd.DataFrame:
    phase284_complete = as_int(metric_value(phase284_summary, "phase284_interpretation_complete", 0))
    phase284_next = str(metric_value(phase284_summary, "phase284_next_best_action", ""))
    close_phase283 = as_int(metric_value(phase284_summary, "phase284_close_phase283_for_acceptance", 0))
    do_not_relax = as_int(metric_value(phase284_summary, "phase284_do_not_relax_cost_threshold", 0))
    do_not_claim = as_int(metric_value(phase284_summary, "phase284_do_not_claim_portfolio_return", 0))
    replay_allowed = as_int(metric_value(phase284_summary, "phase284_strategy_replay_allowed", 1))
    paper_allowed = as_int(metric_value(phase284_summary, "phase284_paper_or_live_acceptance_allowed", 1))
    claim_allowed = as_int(metric_value(phase284_summary, "phase284_deployable_profitability_claim_allowed", 1))
    eligible_seeds = int(clues["eligible_for_phase286_lifecycle_seed"].astype(int).sum()) if not clues.empty else 0
    family_allowed = int(families["phase286_search_allowed"].astype(int).sum()) if not families.empty else 0
    grid_allowed = int(grid["phase286_search_allowed"].astype(int).sum()) if not grid.empty else 0
    l1_allowed = int(families["l1_only_allowed"].astype(int).sum()) if not families.empty else 1
    live_mask_allowed = int(families["net_edge_live_mask_allowed"].astype(int).sum()) if not families.empty else 1
    rows = [
        ("P285_PHASE284_WORK_ORDER_PRESENT", "run_phase285_event_lifecycle_exit_side_redesign_precommit" in phase284_next, phase284_next, "Phase284 next action targets Phase285", "hard"),
        ("P285_PHASE284_INTERPRETATION_COMPLETE", phase284_complete == 1, phase284_complete, "Phase284 complete", "hard"),
        ("P285_PHASE283_CLOSED_AND_COST_PRESERVED", close_phase283 == 1 and do_not_relax == 1 and do_not_claim == 1, f"close={close_phase283};do_not_relax={do_not_relax};do_not_claim={do_not_claim}", "Phase283 closed, cost threshold preserved, portfolio claim blocked", "hard"),
        ("P285_ROUTE_CONTRACT_PRESENT", int(route["contract_id"].astype(str).eq("P285_SEARCH_TYPE").sum()) == 1, len(route), "Phase284 route contract present", "hard"),
        ("P285_LIFECYCLE_SEEDS_PRESENT", eligible_seeds > 0, eligible_seeds, ">0 eligible full-depth lifecycle seeds", "hard"),
        ("P285_EVENT_UNIVERSE_DIAGNOSTICS_PRESENT", int(diagnostics["diagnostic_id"].astype(str).eq("event_universe_rows").sum()) == 1, len(diagnostics), "event-universe diagnostics present", "hard"),
        ("P285_LIFECYCLE_FAMILIES_PRESENT", len(families) >= 5 and family_allowed >= 5, f"families={len(families)};allowed={family_allowed}", ">=5 lifecycle families allowed", "hard"),
        ("P285_ENTRY_EXIT_GRID_PRESENT", len(grid) >= 12 and grid_allowed >= 12, f"grid={len(grid)};allowed={grid_allowed}", ">=12 lifecycle grid rows allowed", "hard"),
        ("P285_CAPITAL_COST_CONTROLS_PRESENT", len(capital_cost) >= 8, len(capital_cost), "capital/cost controls present", "hard"),
        ("P285_FULL_DEPTH_AND_LEAKAGE_BOUNDARY", l1_allowed == 0 and live_mask_allowed == 0, f"l1_allowed_sum={l1_allowed};live_mask_allowed_sum={live_mask_allowed}", "L1-only and live label masks forbidden", "hard"),
        ("P285_BOUNDARIES_CLOSED", replay_allowed == 0 and paper_allowed == 0 and claim_allowed == 0, f"replay={replay_allowed};paper={paper_allowed};claim={claim_allowed}", "no replay/paper/live/claim", "hard"),
        ("P285_NEXT_ROUTE_SELECTED", int(next_route["contract_id"].astype(str).eq("P286_SEARCH_TYPE").sum()) == 1, "P286 lifecycle search", "Phase286 search route selected", "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def build_acceptance_summary(clues: pd.DataFrame, diagnostics: pd.DataFrame, families: pd.DataFrame, grid: pd.DataFrame, capital_cost: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    diag_map = dict(zip(diagnostics["diagnostic_id"].astype(str), diagnostics["diagnostic_value"])) if not diagnostics.empty else {}
    next_action = NEXT_ACTION if hard_pass == len(hard) else REPAIR_ACTION
    rows = [
        ("phase285_lifecycle_redesign_precommit_complete", 1, "Phase285 event lifecycle/side/exit redesign precommit completed"),
        ("phase285_selected_route", SELECTED_ROUTE, "Selected route"),
        ("phase285_preserved_phase283_clue_rows", len(clues), "Preserved Phase283 clue rows"),
        ("phase285_phase286_lifecycle_seed_rows", int(clues["eligible_for_phase286_lifecycle_seed"].astype(int).sum()) if not clues.empty else 0, "Eligible Phase286 lifecycle seeds"),
        ("phase285_event_universe_rows", diag_map.get("event_universe_rows", ""), "Full-depth event universe rows"),
        ("phase285_event_universe_dates", diag_map.get("event_universe_dates", ""), "Event-universe dates"),
        ("phase285_event_universe_symbols", diag_map.get("event_universe_symbols", ""), "Event-universe symbols"),
        ("phase285_phase283_scheduled_rows", diag_map.get("phase283_scheduled_rows", ""), "Phase283 scheduled rows sampled"),
        ("phase285_phase283_rejected_same_symbol_overlap_rows", diag_map.get("phase283_rejected_same_symbol_overlap_rows", ""), "Same-symbol overlap bottleneck rows"),
        ("phase285_phase283_rejected_max_concurrent_rows", diag_map.get("phase283_rejected_max_concurrent_rows", ""), "Max-concurrency bottleneck rows"),
        ("phase285_lifecycle_family_rows", len(families), "Lifecycle families defined"),
        ("phase285_phase286_allowed_lifecycle_family_rows", int(families["phase286_search_allowed"].astype(int).sum()) if not families.empty else 0, "Lifecycle families allowed for Phase286"),
        ("phase285_entry_exit_grid_rows", len(grid), "Entry/exit grid rows"),
        ("phase285_capital_cost_contract_rows", len(capital_cost), "Capital/cost contract rows"),
        ("phase285_cost200_required", 1, "Cost200 required"),
        ("phase285_fixed_capital_required", 1, "Fixed-capital denominator required"),
        ("phase285_sparse_diagnostic_event_floor", SPARSE_DIAGNOSTIC_EVENT_FLOOR, "Sparse diagnostic event floor"),
        ("phase285_robust_portfolio_event_floor", ROBUST_PORTFOLIO_EVENT_FLOOR, "Robust portfolio event floor"),
        ("phase285_full_depth_required", 1, "Full top-five and levels 2-5 required"),
        ("phase285_beyond_l1_features_required", 1, "Beyond-L1 features required"),
        ("phase285_l1_only_allowed", 0, "L1-only variants forbidden"),
        ("phase285_net_edge_live_mask_allowed", 0, "Net/gross edge live masks forbidden"),
        ("phase285_strategy_replay_allowed", 0, "No strategy replay unlocked"),
        ("phase285_strategy_promotion_allowed", 0, "No strategy promotion unlocked"),
        ("phase285_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
        ("phase285_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        ("phase285_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase285_hard_gate_rows", len(hard), "Hard gates evaluated"),
        ("phase285_next_best_action", next_action, "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase285 Event Lifecycle / Side / Exit Redesign Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase285 converts the Phase284 decision into an executable Phase286 search contract.",
        "The selected pivot is not another static filter layer: Phase286 must test trade side, entry delay, exit horizon, take-profit/stop/timeout behavior, latency bucket, queue adversity, and fixed-capital cost200 capacity.",
        "Full Zerodha top-five rows 1-5 and levels 2-5 / beyond-L1 materiality remain mandatory; L1-only variants and net-edge live masks remain forbidden.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    phase277_dir: Path = DEFAULT_PHASE277_DIR,
    phase283_dir: Path = DEFAULT_PHASE283_DIR,
    phase284_dir: Path = DEFAULT_PHASE284_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase284_summary, phase284_route, ranked_ensembles, event_universe, scheduled_ledger = load_inputs(phase277_dir, phase283_dir, phase284_dir)
    clues = build_preserved_clue_catalog(phase284_route, ranked_ensembles)
    diagnostics = build_event_universe_diagnostics(event_universe, scheduled_ledger)
    families = build_lifecycle_family_catalog(clues, diagnostics)
    grid = build_entry_exit_grid_contract()
    capital_cost = build_capital_cost_contract()
    next_route = build_next_route_contract(clues, families, grid)
    gates = build_gate_evaluation(phase284_summary, phase284_route, clues, diagnostics, families, grid, capital_cost, next_route)
    acceptance = build_acceptance_summary(clues, diagnostics, families, grid, capital_cost, gates)

    clues.to_csv(output_dir / "phase285_preserved_phase283_clue_catalog.csv", index=False)
    diagnostics.to_csv(output_dir / "phase285_event_universe_diagnostics.csv", index=False)
    families.to_csv(output_dir / "phase285_lifecycle_family_catalog.csv", index=False)
    grid.to_csv(output_dir / "phase285_entry_exit_grid_contract.csv", index=False)
    capital_cost.to_csv(output_dir / "phase285_capital_cost_contract.csv", index=False)
    next_route.to_csv(output_dir / "phase285_next_route_contract.csv", index=False)
    gates.to_csv(output_dir / "phase285_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase285_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase285_event_lifecycle_exit_side_redesign_precommit_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Preserved Phase283 Clues": clues,
            "Event Universe Diagnostics": diagnostics,
            "Lifecycle Family Catalog": families,
            "Entry Exit Grid Contract": grid,
            "Capital Cost Contract": capital_cost,
            "Next Route Contract": next_route,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase285_event_lifecycle_exit_side_redesign_precommit",
        **reproducibility_fields(
            artifact_id="phase285",
            generated_utc=generated_utc,
            inputs={
                "phase284_acceptance_summary": str(phase284_dir / "phase284_acceptance_summary.csv"),
                "phase284_next_route_contract": str(phase284_dir / "phase284_next_route_contract.csv"),
                "phase284_ranked_ensemble_interpretation": str(phase284_dir / "phase284_ranked_ensemble_interpretation.csv"),
                "phase277_event_universe": str(phase277_dir / "phase277_cost200_redesign_event_universe.csv"),
                "phase283_scheduled_ledger": str(phase283_dir / "phase283_sample_regime_conditioned_scheduled_event_ledger.csv"),
            },
            parameters={
                "selected_route": SELECTED_ROUTE,
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "target_cost_profile": TARGET_COST_PROFILE,
                "sparse_diagnostic_event_floor": SPARSE_DIAGNOSTIC_EVENT_FLOOR,
                "robust_portfolio_event_floor": ROBUST_PORTFOLIO_EVENT_FLOOR,
                "initial_capital_inr": INITIAL_CAPITAL_INR,
                "fixed_notional_grid_inr": FIXED_NOTIONAL_GRID_INR,
                "max_concurrent_grid": MAX_CONCURRENT_GRID,
                "strategy_replay_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "preserved_phase283_clue_catalog": str(output_dir / "phase285_preserved_phase283_clue_catalog.csv"),
                "event_universe_diagnostics": str(output_dir / "phase285_event_universe_diagnostics.csv"),
                "lifecycle_family_catalog": str(output_dir / "phase285_lifecycle_family_catalog.csv"),
                "entry_exit_grid_contract": str(output_dir / "phase285_entry_exit_grid_contract.csv"),
                "capital_cost_contract": str(output_dir / "phase285_capital_cost_contract.csv"),
                "next_route_contract": str(output_dir / "phase285_next_route_contract.csv"),
                "gate_evaluation": str(output_dir / "phase285_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase285_acceptance_summary.csv"),
                "report": str(output_dir / "phase285_event_lifecycle_exit_side_redesign_precommit_report.md"),
                "manifest": str(output_dir / "phase285_event_lifecycle_exit_side_redesign_precommit_manifest.json"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase285_precommit_latency_buckets_for_phase286",
        ),
    }
    (output_dir / "phase285_event_lifecycle_exit_side_redesign_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase285 event lifecycle / side / exit redesign precommit.")
    parser.add_argument("--phase277-dir", type=Path, default=DEFAULT_PHASE277_DIR)
    parser.add_argument("--phase283-dir", type=Path, default=DEFAULT_PHASE283_DIR)
    parser.add_argument("--phase284-dir", type=Path, default=DEFAULT_PHASE284_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase277_dir=args.phase277_dir, phase283_dir=args.phase283_dir, phase284_dir=args.phase284_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
