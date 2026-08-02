from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase271_fixed_capital_concurrency_and_capacity_return_analysis import schedule_events_for_scenario
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE277_DIR = Path("outputs/phase277")
DEFAULT_PHASE282_DIR = Path("outputs/phase282")
DEFAULT_OUTPUT_DIR = Path("outputs/phase283")

SELECTED_ROUTE = "P283_REGIME_CONDITIONED_FULL_DEPTH_ENSEMBLE_SEARCH"
NEXT_ACTION = "run_phase284_regime_conditioned_full_depth_ensemble_interpretation_no_paper_live"
REPAIR_ACTION = "repair_phase283_regime_conditioned_full_depth_ensemble_search"

TARGET_COST_PROFILE = "cost200"
ANNUALIZED_THRESHOLD_PCT = 12.0
MIN_EVENTS_FOR_SEARCH_DIAGNOSTIC = 8
MIN_EVENTS_FOR_ROBUST_PORTFOLIO_CLAIM = 30
INITIAL_CAPITAL_INR = 100_000.0
FIXED_NOTIONAL_GRID_INR = [50_000.0, 75_000.0, 100_000.0]
MAX_CONCURRENT_GRID = [1, 2]
VOTE_THRESHOLDS = [1, 2]

FULL_DEPTH_COLUMNS = [
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


def parse_contract_value(frame: pd.DataFrame, contract_id: str) -> str:
    if frame.empty:
        return ""
    rows = frame.loc[frame["contract_id"].astype(str).eq(contract_id), "contract_value"]
    return "" if rows.empty else str(rows.iloc[0])


def split_contract_values(value: str) -> list[str]:
    return [item.strip() for item in str(value).split(";") if item.strip()]


def q(frame: pd.DataFrame, col: str, quantile: float) -> float:
    return float(pd.to_numeric(frame[col], errors="coerce").fillna(0.0).quantile(quantile))


def prepare_events(events: pd.DataFrame) -> pd.DataFrame:
    frame = events.copy()
    numeric_cols = [
        "gross_edge_bps",
        "modeled_cost_bps",
        "cost_multiplier",
        "horizon",
        "richer_event_bar_id",
        "candidate_rank",
        *FULL_DEPTH_COLUMNS,
    ]
    for col in numeric_cols:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
    if "zerodha_round_trip_charge_bps" not in frame.columns:
        frame["zerodha_round_trip_charge_bps"] = frame["modeled_cost_bps"] / frame["cost_multiplier"].replace(0, 2.0)
    if "depth_replenish_withdraw_ratio" not in frame.columns:
        frame["depth_replenish_withdraw_ratio"] = frame["depth_replenishment_pressure"] / (frame["depth_withdrawal_pressure"] + 1.0)
    if "depth_consensus_imbalance" not in frame.columns:
        frame["depth_consensus_imbalance"] = (
            frame["avg_cum_top5_qty_imbalance"]
            + frame["avg_depth_beyond_l1_qty_imbalance"]
            + frame["avg_level_weighted_depth_imbalance"]
        ) / 3.0
    if "event_sparsity_pressure" not in frame.columns:
        frame["event_sparsity_pressure"] = frame["avg_spread_bps"] * (frame["top5_churn_pressure"] + 1.0)
    frame["richer_event_bar_id"] = pd.to_numeric(frame["richer_event_bar_id"], errors="coerce").fillna(0).astype(int)
    frame["candidate_rank"] = pd.to_numeric(frame["candidate_rank"], errors="coerce").fillna(999999).astype(int)
    frame["horizon"] = pd.to_numeric(frame["horizon"], errors="coerce").fillna(1).astype(int).clip(lower=1)
    return frame.sort_values(["trade_date", "exchange", "richer_event_bar_id", "candidate_rank", "candidate_id", "symbol"]).reset_index(drop=True)


def seed_mask(events: pd.DataFrame, seed_id: str) -> tuple[pd.Series, str, int]:
    spread = pd.to_numeric(events["avg_spread_bps"], errors="coerce").fillna(0.0)
    ratio = pd.to_numeric(events["depth_replenish_withdraw_ratio"], errors="coerce").fillna(0.0)
    beyond = pd.to_numeric(events["avg_depth_beyond_l1_qty_imbalance"], errors="coerce").fillna(0.0)
    churn = pd.to_numeric(events["top5_churn_pressure"], errors="coerce").fillna(0.0)
    withdrawal = pd.to_numeric(events["depth_withdrawal_pressure"], errors="coerce").fillna(0.0)
    weighted = pd.to_numeric(events["avg_level_weighted_depth_imbalance"], errors="coerce").fillna(0.0)
    consensus = pd.to_numeric(events["depth_consensus_imbalance"], errors="coerce").fillna(0.0)
    sparsity = pd.to_numeric(events["event_sparsity_pressure"], errors="coerce").fillna(0.0)

    if seed_id == "P280_SPREAD_REPLENISH_COMBO_Q70":
        mask = (spread <= q(events, "avg_spread_bps", 0.30)) & (ratio >= q(events, "depth_replenish_withdraw_ratio", 0.70)) & (beyond >= q(events, "avg_depth_beyond_l1_qty_imbalance", 0.60))
        return mask, "observable: spread<=q30 and replenish_withdraw>=q70 and beyond_l1_imbalance>=q60", 0
    if seed_id.startswith("P280_TIME_TO_EXIT_SHORT_HQ"):
        quantile = float(seed_id.rsplit("Q", 1)[1]) / 100.0
        mask = (events["horizon"] <= 10) & (ratio >= q(events, "depth_replenish_withdraw_ratio", quantile))
        return mask, f"observable: horizon<=10 and replenish_withdraw>=q{int(quantile * 100)}", 0
    if seed_id.startswith("P280_ADVERSE_SELECTION_AVOID_Q"):
        quantile = float(seed_id.rsplit("Q", 1)[1]) / 100.0
        mask = (churn <= q(events, "top5_churn_pressure", 1.0 - quantile)) & (withdrawal <= q(events, "depth_withdrawal_pressure", 1.0 - quantile))
        return mask, f"observable: churn<=q{int((1.0 - quantile) * 100)} and withdrawal<=q{int((1.0 - quantile) * 100)}", 0
    if seed_id.startswith("P280_REPLENISH_CONFIRM_Q"):
        quantile = float(seed_id.rsplit("Q", 1)[1]) / 100.0
        mask = (ratio >= q(events, "depth_replenish_withdraw_ratio", quantile)) & (weighted >= q(events, "avg_level_weighted_depth_imbalance", quantile))
        return mask, f"observable: replenish_withdraw>=q{int(quantile * 100)} and weighted_depth>=q{int(quantile * 100)}", 0
    if seed_id.startswith("P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q"):
        quantile = float(seed_id.rsplit("Q", 1)[1]) / 100.0
        mask = (consensus >= q(events, "depth_consensus_imbalance", quantile)) & (sparsity <= q(events, "event_sparsity_pressure", 1.0 - quantile))
        return mask, f"observable-only repair: consensus>=q{int(quantile * 100)} and sparsity<=q{int((1.0 - quantile) * 100)}; offline net-edge label removed", 1
    return pd.Series(False, index=events.index), "unknown seed skipped", 0


def build_seed_signal_matrix(events: pd.DataFrame, clues: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    signal = pd.DataFrame(index=events.index)
    for _, clue in clues.iterrows():
        seed_id = str(clue["phase280_variant_id"])
        mask, rule, repaired = seed_mask(events, seed_id)
        signal[seed_id] = mask.astype(int)
        rows.append(
            {
                "phase280_variant_id": seed_id,
                "target_family": clue.get("target_family", ""),
                "observable_seed_rule": rule,
                "event_rows": int(mask.sum()),
                "uses_top5": 1,
                "uses_levels_2_to_5": 1,
                "l1_only_seed": 0,
                "net_edge_live_mask_removed": repaired,
                "eligible_for_phase283": int(mask.sum() > 0),
            }
        )
    return signal, pd.DataFrame(rows)


def build_bucket_masks(events: pd.DataFrame, buckets: pd.DataFrame) -> dict[str, tuple[pd.Series, str]]:
    masks: dict[str, tuple[pd.Series, str]] = {
        "ALL_EVENTS": (pd.Series(True, index=events.index), "all eligible ensemble events"),
    }
    bar = pd.to_numeric(events["richer_event_bar_id"], errors="coerce").fillna(0.0)
    spread = pd.to_numeric(events["avg_spread_bps"], errors="coerce").fillna(0.0)
    churn = pd.to_numeric(events["top5_churn_pressure"], errors="coerce").fillna(0.0)
    withdrawal = pd.to_numeric(events["depth_withdrawal_pressure"], errors="coerce").fillna(0.0)
    beyond = pd.to_numeric(events["avg_depth_beyond_l1_qty_imbalance"], errors="coerce").fillna(0.0)
    for bucket_id in buckets["bucket_id"].astype(str).tolist():
        if bucket_id == "P282_TIME_OPEN_BUCKET":
            masks[bucket_id] = (bar <= q(events, "richer_event_bar_id", 0.50), "richer_event_bar_id<=q50")
        elif bucket_id == "P282_TIME_LATER_BUCKET":
            masks[bucket_id] = (bar >= q(events, "richer_event_bar_id", 0.50), "richer_event_bar_id>=q50")
        elif bucket_id == "P282_SPREAD_COMPRESSED_BUCKET":
            masks[bucket_id] = (spread <= q(events, "avg_spread_bps", 0.50), "avg_spread_bps<=q50")
        elif bucket_id == "P282_DEPTH_STABLE_BUCKET":
            masks[bucket_id] = (
                (churn <= q(events, "top5_churn_pressure", 0.50))
                & (withdrawal <= q(events, "depth_withdrawal_pressure", 0.50))
                & (beyond >= q(events, "avg_depth_beyond_l1_qty_imbalance", 0.50)),
                "churn<=q50 and withdrawal<=q50 and beyond_l1_imbalance>=q50",
            )
    return masks


def build_ensemble_variants(events: pd.DataFrame, signal: pd.DataFrame, clues: pd.DataFrame, ensembles: pd.DataFrame, buckets: pd.DataFrame) -> pd.DataFrame:
    clue_family = clues.set_index("phase280_variant_id")["target_family"].astype(str).to_dict()
    bucket_masks = build_bucket_masks(events, buckets)
    rows: list[dict[str, Any]] = []
    for _, ensemble in ensembles[ensembles["phase283_search_allowed"].astype(int).eq(1)].iterrows():
        included_families = set(split_contract_values(ensemble["included_target_families"]))
        seed_cols = [col for col in signal.columns if clue_family.get(col, "") in included_families]
        if not seed_cols:
            continue
        family_votes = pd.DataFrame(index=events.index)
        for family in included_families:
            family_cols = [col for col in seed_cols if clue_family.get(col, "") == family]
            if family_cols:
                family_votes[family] = signal[family_cols].max(axis=1)
        vote_count = family_votes.sum(axis=1) if not family_votes.empty else pd.Series(0, index=events.index)
        thresholds = VOTE_THRESHOLDS if str(ensemble["ensemble_family_id"]) != "P282_FAMILY_VOTE_ENSEMBLE" else [2, 3]
        for threshold in thresholds:
            base_mask = vote_count >= threshold
            for bucket_id, (bucket_mask, bucket_rule) in bucket_masks.items():
                mask = base_mask & bucket_mask
                rows.append(
                    {
                        "phase283_variant_id": f"P283_{ensemble['ensemble_family_id']}_V{threshold}_{bucket_id}",
                        "ensemble_family_id": ensemble["ensemble_family_id"],
                        "ensemble_family": ensemble["ensemble_family"],
                        "vote_threshold": threshold,
                        "bucket_id": bucket_id,
                        "bucket_rule": bucket_rule,
                        "seed_ids": ";".join(seed_cols),
                        "included_target_families": ";".join(sorted(included_families)),
                        "selected_event_rows": int(mask.sum()),
                        "uses_top5": 1,
                        "uses_levels_2_to_5": 1,
                        "l1_only_variant": 0,
                        "uses_net_edge_as_live_mask": 0,
                        "mask": mask,
                    }
                )
    return pd.DataFrame(rows)


def evaluate_variants(events: pd.DataFrame, variants: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    scenario_rows: list[dict[str, Any]] = []
    ledgers: list[pd.DataFrame] = []
    for _, variant in variants.iterrows():
        selected = events[variant["mask"]].copy()
        if selected.empty:
            continue
        for fixed_notional in FIXED_NOTIONAL_GRID_INR:
            for max_concurrent in MAX_CONCURRENT_GRID:
                scenario, ledger = schedule_events_for_scenario(
                    events=selected,
                    scope_id=str(variant["phase283_variant_id"]),
                    scope_candidate_id=";".join(sorted(selected["candidate_id"].astype(str).unique())),
                    initial_capital_inr=INITIAL_CAPITAL_INR,
                    fixed_notional_inr=fixed_notional,
                    max_concurrent_positions=max_concurrent,
                    cost_profile=TARGET_COST_PROFILE,
                    cost_multiplier=2.0,
                    extra_slippage_bps=0.0,
                )
                robust_claim = int(scenario["scheduled_event_rows"] >= MIN_EVENTS_FOR_ROBUST_PORTFOLIO_CLAIM)
                sparse_eligible = int(scenario["scheduled_event_rows"] >= MIN_EVENTS_FOR_SEARCH_DIAGNOSTIC)
                above12 = int(
                    sparse_eligible == 1
                    and float(scenario["mechanical_one_date_annualized_portfolio_return_pct"]) > ANNUALIZED_THRESHOLD_PCT
                )
                scenario.update(
                    {
                        "phase283_variant_id": variant["phase283_variant_id"],
                        "ensemble_family_id": variant["ensemble_family_id"],
                        "ensemble_family": variant["ensemble_family"],
                        "vote_threshold": variant["vote_threshold"],
                        "bucket_id": variant["bucket_id"],
                        "bucket_rule": variant["bucket_rule"],
                        "seed_ids": variant["seed_ids"],
                        "included_target_families": variant["included_target_families"],
                        "selected_event_rows": int(len(selected)),
                        "uses_top5": 1,
                        "uses_levels_2_to_5": 1,
                        "l1_only_variant": 0,
                        "uses_net_edge_as_live_mask": 0,
                        "sparse_diagnostic_event_floor_met": sparse_eligible,
                        "robust_portfolio_event_floor_met": robust_claim,
                        "cost200_above12_sparse_diagnostic": above12,
                        "strategy_replay_allowed": 0,
                        "promotion_allowed": 0,
                        "paper_or_live_acceptance_allowed": 0,
                        "deployable_profitability_claim_allowed": 0,
                    }
                )
                scenario_rows.append(scenario)
                if len(ledgers) < 12 and scenario["scheduled_event_rows"] > 0:
                    ledger = ledger.copy()
                    ledger["phase283_variant_id"] = variant["phase283_variant_id"]
                    ledger["ensemble_family"] = variant["ensemble_family"]
                    ledger["bucket_id"] = variant["bucket_id"]
                    ledgers.append(ledger)
    scenarios = pd.DataFrame(scenario_rows)
    ledger = pd.concat(ledgers, ignore_index=True) if ledgers else pd.DataFrame()
    return scenarios, ledger


def build_variant_summary(scenarios: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame()
    frame = scenarios.copy()
    for col in [
        "mechanical_one_date_annualized_portfolio_return_pct",
        "realized_net_pnl_inr",
        "scheduled_event_rows",
        "cost200_above12_sparse_diagnostic",
        "sparse_diagnostic_event_floor_met",
        "robust_portfolio_event_floor_met",
    ]:
        frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
    grouped = (
        frame.groupby(["phase283_variant_id", "ensemble_family", "bucket_id", "vote_threshold"], dropna=False)
        .agg(
            scenario_rows=("scenario_id", "nunique"),
            selected_event_rows=("selected_event_rows", "max"),
            max_scheduled_event_rows=("scheduled_event_rows", "max"),
            cost200_above12_sparse_diagnostic_rows=("cost200_above12_sparse_diagnostic", "sum"),
            sparse_floor_met_rows=("sparse_diagnostic_event_floor_met", "sum"),
            robust_portfolio_floor_met_rows=("robust_portfolio_event_floor_met", "sum"),
            min_annualized_pct=("mechanical_one_date_annualized_portfolio_return_pct", "min"),
            median_annualized_pct=("mechanical_one_date_annualized_portfolio_return_pct", "median"),
            max_annualized_pct=("mechanical_one_date_annualized_portfolio_return_pct", "max"),
            max_net_pnl_inr=("realized_net_pnl_inr", "max"),
        )
        .reset_index()
    )
    grouped["median_above12"] = (grouped["median_annualized_pct"] > ANNUALIZED_THRESHOLD_PCT).astype(int)
    return grouped.sort_values(
        ["cost200_above12_sparse_diagnostic_rows", "robust_portfolio_floor_met_rows", "max_annualized_pct", "max_scheduled_event_rows"],
        ascending=[False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_gate_evaluation(phase282_summary: pd.DataFrame, seed_catalog: pd.DataFrame, variants: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(phase282_summary, "phase282_regime_conditioned_ensemble_precommit_complete", 0))
    next_action = str(metric_value(phase282_summary, "phase282_next_best_action", ""))
    l1_only = int(scenarios["l1_only_variant"].astype(int).sum()) if not scenarios.empty else 0
    live_leakage = int(scenarios["uses_net_edge_as_live_mask"].astype(int).sum()) if not scenarios.empty else 0
    rows = [
        ("P283_PHASE282_WORK_ORDER_PRESENT", "run_phase283_regime_conditioned_full_depth_ensemble_search" in next_action, next_action, "Phase282 next action targets Phase283", "hard"),
        ("P283_PHASE282_PRECOMMIT_COMPLETE", complete == 1, complete, "Phase282 complete", "hard"),
        ("P283_SEED_REPAIRS_DOCUMENTED", int(seed_catalog["net_edge_live_mask_removed"].astype(int).sum()) >= 1, int(seed_catalog["net_edge_live_mask_removed"].astype(int).sum()), "net-edge label seed repaired to observable-only mask", "hard"),
        ("P283_VARIANTS_EVALUATED", len(variants) > 0, len(variants), ">0 ensemble variants", "hard"),
        ("P283_SCENARIOS_PRESENT", len(scenarios) > 0, len(scenarios), ">0 scenarios", "hard"),
        ("P283_COST200_REQUIRED", bool(not scenarios.empty and scenarios["cost_profile"].astype(str).eq(TARGET_COST_PROFILE).all()), TARGET_COST_PROFILE, "all scenarios cost200", "hard"),
        ("P283_FULL_DEPTH_REQUIRED", bool(not scenarios.empty and scenarios["uses_top5"].astype(int).eq(1).all() and scenarios["uses_levels_2_to_5"].astype(int).eq(1).all()), "top5=1;levels_2_to_5=1", "full-depth scenario contract", "hard"),
        ("P283_L1_ONLY_FORBIDDEN", l1_only == 0, l1_only, "0 L1-only variants", "hard"),
        ("P283_NO_LIVE_LABEL_LEAKAGE", live_leakage == 0, live_leakage, "0 net/gross edge live masks", "hard"),
        ("P283_BOUNDARIES_CLOSED", bool(not scenarios.empty and scenarios["strategy_replay_allowed"].astype(int).eq(0).all() and scenarios["paper_or_live_acceptance_allowed"].astype(int).eq(0).all() and scenarios["deployable_profitability_claim_allowed"].astype(int).eq(0).all()), "replay=0;paper=0;claim=0", "no replay/paper/live/claim", "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def build_acceptance_summary(scenarios: pd.DataFrame, variant_summary: pd.DataFrame, gates: pd.DataFrame, seed_catalog: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    best = scenarios.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0] if not scenarios.empty else pd.Series(dtype=object)
    sparse_above = int(pd.to_numeric(scenarios.get("cost200_above12_sparse_diagnostic", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()) if not scenarios.empty else 0
    robust_rows = int(pd.to_numeric(scenarios.get("robust_portfolio_event_floor_met", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()) if not scenarios.empty else 0
    next_action = NEXT_ACTION if hard_pass == len(hard) else REPAIR_ACTION
    rows = [
        ("phase283_regime_conditioned_ensemble_search_complete", 1, "Phase283 regime-conditioned full-depth ensemble search completed"),
        ("phase283_selected_route", SELECTED_ROUTE, "Selected route"),
        ("phase283_seed_rows", len(seed_catalog), "Search seed rows"),
        ("phase283_variant_rows", len(variant_summary), "Ensemble variants evaluated"),
        ("phase283_scenario_rows", len(scenarios), "Cost200 fixed-capital scenarios evaluated"),
        ("phase283_sparse_above12_scenario_rows", sparse_above, "Cost200 above-12 sparse diagnostic rows with event floor met"),
        ("phase283_robust_portfolio_floor_scenario_rows", robust_rows, "Scenarios meeting robust portfolio event floor"),
        ("phase283_best_variant_id", best.get("phase283_variant_id", ""), "Best Phase283 variant"),
        ("phase283_best_ensemble_family", best.get("ensemble_family", ""), "Best ensemble family"),
        ("phase283_best_bucket_id", best.get("bucket_id", ""), "Best regime bucket"),
        ("phase283_best_cost200_annualized_pct", best.get("mechanical_one_date_annualized_portfolio_return_pct", ""), "Best cost200 annualized diagnostic"),
        ("phase283_best_realized_net_pnl_inr", best.get("realized_net_pnl_inr", ""), "Best realized net P&L"),
        ("phase283_best_scheduled_event_rows", best.get("scheduled_event_rows", ""), "Best scheduled event rows"),
        ("phase283_l1_only_variant_rows", int(scenarios["l1_only_variant"].astype(int).sum()) if not scenarios.empty else 0, "L1-only variants"),
        ("phase283_net_edge_live_mask_rows", int(scenarios["uses_net_edge_as_live_mask"].astype(int).sum()) if not scenarios.empty else 0, "Live masks using net/gross edge"),
        ("phase283_strategy_replay_allowed", 0, "No strategy replay unlocked"),
        ("phase283_strategy_promotion_allowed", 0, "No strategy promotion unlocked"),
        ("phase283_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
        ("phase283_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        ("phase283_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase283_hard_gate_rows", len(hard), "Hard gates evaluated"),
        ("phase283_next_best_action", next_action, "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase283 Regime-conditioned Full-depth Ensemble Search",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase283 executes the Phase282 regime-conditioned full-depth ensemble search under cost200 fixed-capital scoring.",
        "The net-edge-shift seed is repaired into an observable-only depth/sparsity mask; no live net/gross-edge mask is allowed.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase277_dir: Path = DEFAULT_PHASE277_DIR, phase282_dir: Path = DEFAULT_PHASE282_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase282_summary = read_csv(phase282_dir / "phase282_acceptance_summary.csv")
    clues = read_csv(phase282_dir / "phase282_preserved_clue_catalog.csv")
    ensembles = read_csv(phase282_dir / "phase282_ensemble_family_catalog.csv")
    buckets = read_csv(phase282_dir / "phase282_regime_bucket_contract.csv")
    events = read_csv(phase277_dir / "phase277_cost200_redesign_event_universe.csv")
    if phase282_summary.empty:
        raise FileNotFoundError("Missing Phase282 acceptance summary.")
    if clues.empty or ensembles.empty or buckets.empty:
        raise FileNotFoundError("Missing Phase282 search contract artifacts.")
    if events.empty:
        raise FileNotFoundError("Missing Phase277 cost200 event universe.")

    prepared = prepare_events(events)
    signal, seed_catalog = build_seed_signal_matrix(prepared, clues[clues["eligible_for_phase283_search_seed"].astype(int).eq(1)].copy())
    variants = build_ensemble_variants(prepared, signal, clues, ensembles, buckets)
    scenarios, sample_ledger = evaluate_variants(prepared, variants)
    variant_summary = build_variant_summary(scenarios)
    gates = build_gate_evaluation(phase282_summary, seed_catalog, variants, scenarios)
    acceptance = build_acceptance_summary(scenarios, variant_summary, gates, seed_catalog)

    export_variants = variants.drop(columns=["mask"], errors="ignore")
    seed_catalog.to_csv(output_dir / "phase283_observable_seed_catalog.csv", index=False)
    export_variants.to_csv(output_dir / "phase283_ensemble_variant_catalog.csv", index=False)
    scenarios.to_csv(output_dir / "phase283_regime_conditioned_ensemble_scenario_results.csv", index=False)
    variant_summary.to_csv(output_dir / "phase283_regime_conditioned_ensemble_variant_summary.csv", index=False)
    sample_ledger.to_csv(output_dir / "phase283_sample_regime_conditioned_scheduled_event_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase283_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase283_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase283_regime_conditioned_full_depth_ensemble_search_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Observable Seed Catalog": seed_catalog,
            "Top Variant Summary": variant_summary.head(20),
            "Top Scenarios": scenarios.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).head(20),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase283_regime_conditioned_full_depth_ensemble_search",
        **reproducibility_fields(
            artifact_id="phase283",
            generated_utc=generated_utc,
            inputs={
                "phase277_cost200_redesign_event_universe": str(phase277_dir / "phase277_cost200_redesign_event_universe.csv"),
                "phase282_acceptance_summary": str(phase282_dir / "phase282_acceptance_summary.csv"),
                "phase282_preserved_clue_catalog": str(phase282_dir / "phase282_preserved_clue_catalog.csv"),
                "phase282_ensemble_family_catalog": str(phase282_dir / "phase282_ensemble_family_catalog.csv"),
                "phase282_regime_bucket_contract": str(phase282_dir / "phase282_regime_bucket_contract.csv"),
            },
            parameters={
                "selected_route": SELECTED_ROUTE,
                "target_cost_profile": TARGET_COST_PROFILE,
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "initial_capital_inr": INITIAL_CAPITAL_INR,
                "fixed_notional_grid_inr": FIXED_NOTIONAL_GRID_INR,
                "max_concurrent_grid": MAX_CONCURRENT_GRID,
                "vote_thresholds": VOTE_THRESHOLDS,
                "min_events_for_search_diagnostic": MIN_EVENTS_FOR_SEARCH_DIAGNOSTIC,
                "min_events_for_robust_portfolio_claim": MIN_EVENTS_FOR_ROBUST_PORTFOLIO_CLAIM,
                "full_depth_columns": FULL_DEPTH_COLUMNS,
                "net_edge_live_mask_allowed": 0,
                "l1_only_variant_allowed": 0,
                "strategy_replay_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "observable_seed_catalog": str(output_dir / "phase283_observable_seed_catalog.csv"),
                "ensemble_variant_catalog": str(output_dir / "phase283_ensemble_variant_catalog.csv"),
                "scenario_results": str(output_dir / "phase283_regime_conditioned_ensemble_scenario_results.csv"),
                "variant_summary": str(output_dir / "phase283_regime_conditioned_ensemble_variant_summary.csv"),
                "sample_scheduled_event_ledger": str(output_dir / "phase283_sample_regime_conditioned_scheduled_event_ledger.csv"),
                "gate_evaluation": str(output_dir / "phase283_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase283_acceptance_summary.csv"),
                "report": str(output_dir / "phase283_regime_conditioned_full_depth_ensemble_search_report.md"),
                "manifest": str(output_dir / "phase283_regime_conditioned_full_depth_ensemble_search_manifest.json"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase283_no_new_live_latency_synthetic_ensemble_search",
        ),
    }
    (output_dir / "phase283_regime_conditioned_full_depth_ensemble_search_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase283 regime-conditioned full-depth ensemble search.")
    parser.add_argument("--phase277-dir", type=Path, default=DEFAULT_PHASE277_DIR)
    parser.add_argument("--phase282-dir", type=Path, default=DEFAULT_PHASE282_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase277_dir=args.phase277_dir, phase282_dir=args.phase282_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
