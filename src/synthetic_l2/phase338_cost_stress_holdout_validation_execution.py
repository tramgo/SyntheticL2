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
from synthetic_l2.phase335_cost_stress_margin_redesign_training_only import add_live_features, annualized_from_returns
from synthetic_l2.phase332_event_catalyst_expanded_strategy_search_training_only import write_parquet
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE330_DIR = Path("outputs/phase330")
DEFAULT_PHASE337_DIR = Path("outputs/phase337")
DEFAULT_OUTPUT_DIR = Path("outputs/phase338")

NEXT_ACTION = "run_phase339_cost_stress_holdout_validation_interpretation_no_replay"
REPAIR_ACTION = "repair_phase338_cost_stress_holdout_validation_execution"

ANNUALIZED_THRESHOLD_PCT = 12.0
ROBUST_EVENT_FLOOR = 30
MIN_SYMBOL_DATE_POSITIVE_CELLS = 2
HOLDOUT_HASH_SEED = 338
HOLDOUT_BUCKET_CUTOFF = 50
COST200 = "zerodha_2x_all_in_cost_proxy"


def stable_bucket(event_id: str, seed: int = HOLDOUT_HASH_SEED) -> int:
    digest = hashlib.sha256(f"{seed}|{event_id}".encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big") % 100


def load_feature_matrix(phase330_dir: Path) -> pd.DataFrame:
    parquet = phase330_dir / "phase330_event_catalyst_expanded_feature_matrix.parquet"
    csv = phase330_dir / "phase330_event_catalyst_expanded_feature_matrix.csv"
    return pd.read_parquet(parquet) if parquet.exists() else read_csv(csv)


def prepare_holdout_features(features: pd.DataFrame) -> pd.DataFrame:
    frame = add_live_features(features)
    frame["holdout_bucket"] = [stable_bucket(str(event_id)) for event_id in frame["event_id"].astype(str)]
    frame["holdout_partition"] = np.where(frame["holdout_bucket"].lt(HOLDOUT_BUCKET_CUTOFF), "phase338_hash_holdout", "phase338_hash_reference")
    return frame


def select_candidate_trades(frame: pd.DataFrame, candidate: pd.Series) -> pd.DataFrame:
    target_col = f"target_post_{int(float(candidate['horizon_seconds']))}s_mid_return_bps"
    if target_col not in frame.columns:
        return pd.DataFrame()
    holdout = frame[frame["holdout_partition"].astype(str).eq("phase338_hash_holdout")].copy()
    work = holdout[
        holdout["signal"].ne(0)
        & holdout["abs_signal"].ge(holdout["abs_signal"].quantile(float(candidate["signal_quantile"])))
        & holdout["spread_bps"].le(holdout["spread_bps"].quantile(float(candidate["spread_max_quantile"])))
        & holdout["depth_share"].ge(holdout["depth_share"].quantile(float(candidate["depth_share_min_quantile"])))
    ].copy()
    if str(candidate["side_policy"]) == "long_only":
        work = work[work["side"].eq(1)].copy()
    work[target_col] = pd.to_numeric(work[target_col], errors="coerce")
    work = work.dropna(subset=[target_col]).sort_values(["event_id", "abs_signal", "symbol"], ascending=[True, False, True])
    if work.empty:
        return pd.DataFrame()
    top_n = int(float(candidate["top_n_per_event"]))
    selected = work.groupby("event_id", group_keys=False).head(top_n).copy()
    capital = float(candidate["initial_capital_inr"])
    notional = float(candidate["fixed_notional_inr"])
    slots = max(0, min(int(float(candidate["max_concurrent_positions"])), int(capital // notional), top_n))
    if slots <= 0:
        return pd.DataFrame()
    selected = selected.groupby("event_id", group_keys=False).head(slots).copy()
    selected["target_return_bps"] = pd.to_numeric(selected[target_col], errors="coerce")
    selected["signed_return_bps"] = selected["side"] * selected["target_return_bps"]
    selected["side_flip_signed_return_bps"] = -selected["signed_return_bps"]
    selected["random_side_signed_return_bps"] = selected["random_side"] * selected["target_return_bps"]
    selected["scenario_id"] = str(candidate["scenario_id"])
    selected["freeze_rank"] = int(float(candidate["freeze_rank"]))
    return selected


def positive_symbol_date_cells(selected: pd.DataFrame, notional: float, cost_profile: str, execution_policy: str) -> int:
    if selected.empty:
        return 0
    fill_probability, _, passive_penalty = annualized_fill_penalty(selected, execution_policy, notional)
    gross = notional * selected["signed_return_bps"].fillna(0.0) / 10_000.0 * fill_probability
    from synthetic_l2.phase332_event_catalyst_expanded_strategy_search_training_only import vector_cost_inr

    cost = vector_cost_inr(notional, selected["signed_return_bps"].fillna(0.0), cost_profile) * fill_probability
    net = gross - cost - passive_penalty
    cells = pd.DataFrame(
        {
            "trade_date": selected["event_time_ist"].astype(str).str.slice(0, 10),
            "symbol": selected["symbol"].astype(str),
            "net": net,
        }
    )
    return int((cells.groupby(["trade_date", "symbol"])["net"].sum() > 0).sum())


def annualized_fill_penalty(selected: pd.DataFrame, execution_policy: str, notional: float) -> tuple[pd.Series, pd.Series, pd.Series]:
    from synthetic_l2.phase332_event_catalyst_expanded_strategy_search_training_only import passive_adjustments

    return passive_adjustments(selected, execution_policy, notional)


def score_candidate(selected: pd.DataFrame, candidate: pd.Series, cost_profile: str, execution_policy: str) -> dict[str, Any]:
    capital = float(candidate["initial_capital_inr"])
    notional = float(candidate["fixed_notional_inr"])
    annualized, net_pnl, gross_pnl, cost_inr, passive_penalty, avg_fill = annualized_from_returns(
        selected, selected["signed_return_bps"].fillna(0.0) if not selected.empty else pd.Series(dtype=float), notional, capital, cost_profile, execution_policy
    )
    side_flip_ann, side_flip_net, *_ = annualized_from_returns(
        selected, selected["side_flip_signed_return_bps"].fillna(0.0) if not selected.empty else pd.Series(dtype=float), notional, capital, cost_profile, execution_policy
    )
    random_ann, random_net, *_ = annualized_from_returns(
        selected, selected["random_side_signed_return_bps"].fillna(0.0) if not selected.empty else pd.Series(dtype=float), notional, capital, cost_profile, execution_policy
    )
    fill_probability, adverse_bps, penalty = annualized_fill_penalty(selected, execution_policy, notional) if not selected.empty else (pd.Series(dtype=float), pd.Series(dtype=float), pd.Series(dtype=float))
    scheduled_events = int(selected["event_id"].nunique()) if not selected.empty else 0
    symbol_rows = int(selected["symbol"].nunique()) if not selected.empty else 0
    observed_dates = int(selected["event_time_ist"].astype(str).str.slice(0, 10).nunique()) if not selected.empty else 0
    positive_cells = positive_symbol_date_cells(selected, notional, cost_profile, execution_policy)
    control_pass = int(annualized > side_flip_ann and annualized > random_ann)
    acceptance = int(
        cost_profile == COST200
        and execution_policy == str(candidate["primary_holdout_execution_policy"])
        and annualized > ANNUALIZED_THRESHOLD_PCT
        and scheduled_events >= ROBUST_EVENT_FLOOR
        and positive_cells >= MIN_SYMBOL_DATE_POSITIVE_CELLS
        and symbol_rows >= 2
        and control_pass == 1
    )
    return {
        "source_scenario_id": str(candidate["scenario_id"]),
        "freeze_rank": int(float(candidate["freeze_rank"])),
        "lane_id": str(candidate["lane_id"]),
        "horizon_seconds": int(float(candidate["horizon_seconds"])),
        "signal_quantile": float(candidate["signal_quantile"]),
        "spread_max_quantile": float(candidate["spread_max_quantile"]),
        "depth_share_min_quantile": float(candidate["depth_share_min_quantile"]),
        "top_n_per_event": int(float(candidate["top_n_per_event"])),
        "side_policy": str(candidate["side_policy"]),
        "execution_policy": execution_policy,
        "cost_profile": cost_profile,
        "initial_capital_inr": capital,
        "fixed_notional_inr": notional,
        "max_concurrent_positions": int(float(candidate["max_concurrent_positions"])),
        "scheduled_event_rows": scheduled_events,
        "symbol_rows": symbol_rows,
        "observed_trade_dates": observed_dates,
        "trade_rows": int(len(selected)),
        "positive_symbol_date_cells": positive_cells,
        "avg_fill_probability": avg_fill,
        "avg_adverse_selection_bps": float(adverse_bps.mean()) if len(adverse_bps) else 0.0,
        "passive_penalty_inr": passive_penalty,
        "gross_pnl_inr": gross_pnl,
        "cost_inr": cost_inr,
        "net_pnl_inr": net_pnl,
        "portfolio_return_pct": net_pnl / capital * 100.0 if capital else 0.0,
        "annualized_return_pct": annualized,
        "side_flip_annualized_return_pct": side_flip_ann,
        "side_flip_net_pnl_inr": side_flip_net,
        "random_side_annualized_return_pct": random_ann,
        "random_side_net_pnl_inr": random_net,
        "control_pass": control_pass,
        "above12_annualized": int(annualized > ANNUALIZED_THRESHOLD_PCT),
        "robust_event_floor_met": int(scheduled_events >= ROBUST_EVENT_FLOOR),
        "holdout_acceptance_candidate": acceptance,
        "profitability_claim_allowed": 0,
    }


def execute_holdout(features: pd.DataFrame, frozen: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    trade_rows: list[pd.DataFrame] = []
    for _, candidate in frozen.iterrows():
        selected = select_candidate_trades(features, candidate)
        if not selected.empty:
            trade_rows.append(selected)
        policies = [str(candidate["primary_holdout_execution_policy"]), "passive_aware_directional_with_penalties"]
        for execution_policy in sorted(set(policies)):
            for cost_profile in ["zerodha_base", COST200]:
                rows.append(score_candidate(selected, candidate, cost_profile, execution_policy))
    scenarios = pd.DataFrame(rows)
    if not scenarios.empty:
        scenarios["holdout_scenario_id"] = (
            "P338_"
            + scenarios["source_scenario_id"].astype(str)
            + "_"
            + scenarios["execution_policy"].astype(str)
            + "_"
            + scenarios["cost_profile"].astype(str)
        )
        scenarios = scenarios.sort_values(["annualized_return_pct", "net_pnl_inr"], ascending=[False, False]).reset_index(drop=True)
    trades = pd.concat(trade_rows, ignore_index=True) if trade_rows else pd.DataFrame()
    return scenarios, trades


def build_partition_ledger(features: pd.DataFrame) -> pd.DataFrame:
    grouped = features.groupby("holdout_partition", dropna=False).agg(event_rows=("event_id", "nunique"), row_count=("event_id", "count"), symbol_rows=("symbol", "nunique")).reset_index()
    grouped["hash_seed"] = HOLDOUT_HASH_SEED
    grouped["holdout_bucket_cutoff"] = HOLDOUT_BUCKET_CUTOFF
    grouped["partition_note"] = "deterministic event-hash synthetic holdout partition; not paper/live acceptance"
    return grouped


def build_control_ledger(scenarios: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame()
    primary = scenarios[scenarios["execution_policy"].astype(str).eq("taker_entry_taker_exit")]
    base = primary[primary["cost_profile"].astype(str).eq("zerodha_base")].sort_values("annualized_return_pct", ascending=False)
    cost200 = primary[primary["cost_profile"].astype(str).eq(COST200)].sort_values("annualized_return_pct", ascending=False)
    base_top = str(base.iloc[0]["source_scenario_id"]) if not base.empty else ""
    cost200_top = str(cost200.iloc[0]["source_scenario_id"]) if not cost200.empty else ""
    structural_cols = ["lane_id", "horizon_seconds", "signal_quantile", "spread_max_quantile", "depth_share_min_quantile", "top_n_per_event", "side_policy", "execution_policy"]
    base_shape = "|".join(str(base.iloc[0][col]) for col in structural_cols) if not base.empty else ""
    cost200_shape = "|".join(str(cost200.iloc[0][col]) for col in structural_cols) if not cost200.empty else ""
    return pd.DataFrame(
        [
            ("base_top_scenario", base_top, "Top primary taker scenario under base Zerodha costs"),
            ("cost200_top_scenario", cost200_top, "Top primary taker scenario under 2x Zerodha costs"),
            ("base_top_strategy_shape", base_shape, "Top primary taker structural strategy shape under base Zerodha costs"),
            ("cost200_top_strategy_shape", cost200_shape, "Top primary taker structural strategy shape under 2x Zerodha costs"),
            ("cost_rank_top_stable", int(base_shape == cost200_shape and bool(base_shape)), "Top structural strategy shape stable from base to 2x cost"),
            ("cost200_control_pass_rows", int(cost200["control_pass"].astype(int).sum()) if not cost200.empty else 0, "2x-cost primary rows beating side-flip and random-side controls"),
            ("cost200_above12_rows", int(cost200["above12_annualized"].astype(int).sum()) if not cost200.empty else 0, "2x-cost primary rows above 12%"),
            ("cost200_holdout_acceptance_rows", int(cost200["holdout_acceptance_candidate"].astype(int).sum()) if not cost200.empty else 0, "2x-cost primary holdout acceptance rows"),
        ],
        columns=["control_id", "value", "description"],
    )


def build_passive_diagnostic(scenarios: pd.DataFrame) -> pd.DataFrame:
    passive = scenarios[scenarios["execution_policy"].astype(str).eq("passive_aware_directional_with_penalties")] if not scenarios.empty else pd.DataFrame()
    cost200 = passive[passive["cost_profile"].astype(str).eq(COST200)] if not passive.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("passive_aware_rows", int(len(passive)), "Passive-aware diagnostic rows"),
            ("passive_aware_cost200_rows", int(len(cost200)), "Passive-aware 2x-cost diagnostic rows"),
            ("passive_aware_cost200_above12_rows", int(cost200["above12_annualized"].astype(int).sum()) if not cost200.empty else 0, "Passive-aware 2x-cost rows above 12%"),
            ("passive_aware_cost200_acceptance_rows", int(cost200["holdout_acceptance_candidate"].astype(int).sum()) if not cost200.empty else 0, "Passive-aware rows are diagnostic and not primary acceptance"),
            ("passive_aware_avg_fill_probability", float(cost200["avg_fill_probability"].mean()) if not cost200.empty else 0.0, "Average modeled passive fill probability"),
            ("passive_aware_avg_adverse_selection_bps", float(cost200["avg_adverse_selection_bps"].mean()) if not cost200.empty else 0.0, "Average modeled adverse selection penalty"),
            ("maker_rebate_assumed", 0, "No maker rebate assumed"),
        ],
        columns=["diagnostic_id", "value", "description"],
    )


def build_gate_evaluation(phase337: pd.DataFrame, features: pd.DataFrame, scenarios: pd.DataFrame, controls: pd.DataFrame, passive: pd.DataFrame) -> pd.DataFrame:
    phase337_complete = as_int(metric_value(phase337, "phase337_cost_stress_holdout_validation_precommit_complete", 0))
    phase338_allowed = as_int(metric_value(phase337, "phase337_phase338_execution_allowed_next", 0))
    full_depth = as_int(metric_value(phase337, "phase337_full_depth_required", 0))
    l2_l5 = as_int(metric_value(phase337, "phase337_levels_2_to_5_required", 0))
    l1_only = as_int(metric_value(phase337, "phase337_l1_only_allowed", 1))
    lookahead = as_int(metric_value(phase337, "phase337_net_edge_live_mask_allowed", 1))
    cost200 = scenarios[scenarios["cost_profile"].astype(str).eq(COST200)] if not scenarios.empty else pd.DataFrame()
    primary_cost200 = cost200[cost200["execution_policy"].astype(str).eq("taker_entry_taker_exit")] if not cost200.empty else pd.DataFrame()
    control_lookup = controls.set_index("control_id")["value"].to_dict() if not controls.empty else {}
    passive_lookup = passive.set_index("diagnostic_id")["value"].to_dict() if not passive.empty else {}
    required_columns = [
        "event_depth_l2_l5_qty_imbalance",
        "event_depth_l2_l5_order_imbalance",
        "event_l2_l5_depth_share",
        "event_depth_l2_l5_pressure",
    ]
    rows = [
        ("P338_PHASE337_COMPLETE", phase337_complete == 1, phase337_complete, 1),
        ("P338_EXECUTION_ALLOWED", phase338_allowed == 1, phase338_allowed, 1),
        ("P338_HOLDOUT_PARTITION_PRESENT", int(features["holdout_partition"].astype(str).eq("phase338_hash_holdout").sum()) > 0, int(features["holdout_partition"].astype(str).eq("phase338_hash_holdout").sum()), ">0"),
        ("P338_SCENARIOS_PRODUCED", len(scenarios) > 0, len(scenarios), ">0"),
        ("P338_COST200_PRIMARY_ROWS_PRESENT", len(primary_cost200) > 0, len(primary_cost200), ">0"),
        ("P338_ACCEPTANCE_ROWS_EXIST", int(primary_cost200["holdout_acceptance_candidate"].astype(int).sum()) > 0 if not primary_cost200.empty else False, int(primary_cost200["holdout_acceptance_candidate"].astype(int).sum()) if not primary_cost200.empty else 0, ">0"),
        ("P338_FULL_DEPTH_COLUMNS_PRESENT", all(col in features.columns for col in required_columns) and full_depth == 1 and l2_l5 == 1, ";".join([col for col in required_columns if col in features.columns]), "all_required_l2_l5_columns"),
        ("P338_L1_ONLY_FORBIDDEN", l1_only == 0, l1_only, 0),
        ("P338_NO_LOOKAHEAD", lookahead == 0, lookahead, 0),
        ("P338_RANK_STABILITY", as_int(control_lookup.get("cost_rank_top_stable", 0)) == 1, control_lookup.get("cost_rank_top_stable", 0), 1),
        ("P338_PASSIVE_REALISM_APPLIED", as_int(passive_lookup.get("passive_aware_cost200_rows", 0)) > 0 and float(passive_lookup.get("passive_aware_avg_fill_probability", 0) or 0) < 1.0 and as_int(passive_lookup.get("maker_rebate_assumed", 1)) == 0, f"rows={passive_lookup.get('passive_aware_cost200_rows', 0)};fill={passive_lookup.get('passive_aware_avg_fill_probability', 0)};rebate={passive_lookup.get('maker_rebate_assumed', 1)}", "passive_rows_and_no_rebate"),
        ("P338_BOUNDARIES_CLOSED", bool((scenarios["profitability_claim_allowed"].astype(int) == 0).all()) if not scenarios.empty else False, "profitability_claim_allowed=0", 0),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(scenarios: pd.DataFrame, partition: pd.DataFrame, controls: pd.DataFrame, passive: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    primary_cost200 = scenarios[(scenarios["cost_profile"].astype(str).eq(COST200)) & (scenarios["execution_policy"].astype(str).eq("taker_entry_taker_exit"))] if not scenarios.empty else pd.DataFrame()
    accepted = primary_cost200[primary_cost200["holdout_acceptance_candidate"].astype(int).eq(1)] if not primary_cost200.empty else pd.DataFrame()
    best = primary_cost200.sort_values(["annualized_return_pct", "net_pnl_inr"], ascending=[False, False]).head(1) if not primary_cost200.empty else pd.DataFrame()
    holdout_events = int(partition.loc[partition["holdout_partition"].astype(str).eq("phase338_hash_holdout"), "event_rows"].iloc[0]) if not partition.empty and partition["holdout_partition"].astype(str).eq("phase338_hash_holdout").any() else 0
    passive_lookup = passive.set_index("diagnostic_id")["value"].to_dict() if not passive.empty else {}
    return pd.DataFrame(
        [
            ("phase338_cost_stress_holdout_validation_execution_complete", int(hard_pass == hard_rows), "Phase338 execution completed"),
            ("phase338_holdout_partition_method", f"event_hash_seed_{HOLDOUT_HASH_SEED}_bucket_lt_{HOLDOUT_BUCKET_CUTOFF}", "Synthetic deterministic holdout partition"),
            ("phase338_holdout_event_rows", holdout_events, "Holdout event rows"),
            ("phase338_scenario_rows", int(len(scenarios)), "Scenario rows evaluated"),
            ("phase338_primary_cost200_rows", int(len(primary_cost200)), "Primary 2x-cost rows"),
            ("phase338_holdout_acceptance_candidate_rows", int(len(accepted)), "Primary 2x-cost holdout acceptance rows"),
            ("phase338_best_holdout_candidate", best.iloc[0]["source_scenario_id"] if not best.empty else "", "Best primary 2x-cost holdout candidate"),
            ("phase338_best_holdout_annualized_return_pct", float(best.iloc[0]["annualized_return_pct"]) if not best.empty else "", "Best primary 2x-cost annualized return"),
            ("phase338_best_holdout_scheduled_events", int(best.iloc[0]["scheduled_event_rows"]) if not best.empty else 0, "Best primary 2x-cost scheduled events"),
            ("phase338_best_holdout_positive_symbol_date_cells", int(best.iloc[0]["positive_symbol_date_cells"]) if not best.empty else 0, "Best positive symbol-date cells"),
            ("phase338_best_holdout_control_pass", int(best.iloc[0]["control_pass"]) if not best.empty else 0, "Best primary 2x-cost control pass"),
            ("phase338_passive_aware_cost200_above12_rows", passive_lookup.get("passive_aware_cost200_above12_rows", 0), "Passive-aware 2x-cost rows above 12%"),
            ("phase338_passive_aware_cost200_acceptance_rows", passive_lookup.get("passive_aware_cost200_acceptance_rows", 0), "Passive-aware diagnostic acceptance rows"),
            ("phase338_passive_aware_avg_fill_probability", passive_lookup.get("passive_aware_avg_fill_probability", 0), "Average passive fill probability"),
            ("phase338_maker_rebate_assumed", 0, "No maker rebate"),
            ("phase338_full_depth_required", 1, "Full top-five depth required"),
            ("phase338_levels_2_to_5_required", 1, "Levels 2-5 materiality required"),
            ("phase338_l1_only_allowed", 0, "No L1-only variants"),
            ("phase338_net_edge_live_mask_allowed", 0, "No lookahead masks"),
            ("phase338_strategy_replay_allowed", 0, "No replay"),
            ("phase338_strategy_promotion_allowed", 0, "No promotion"),
            ("phase338_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase338_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase338_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase338_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase338_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase338 Cost-Stress Holdout Validation Execution",
        "",
        "Phase338 executes the Phase337 frozen candidate contract on a deterministic synthetic event-hash holdout partition.",
        "It evaluates primary taker execution plus passive-aware diagnostics with fill probability, adverse-selection, forced-flatten penalties and no maker rebate.",
        "This is still not paper/live acceptance or a deployable profitability claim.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase338_cost_stress_holdout_validation_execution_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase330_dir: Path = DEFAULT_PHASE330_DIR, phase337_dir: Path = DEFAULT_PHASE337_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase337 = read_csv(phase337_dir / "phase337_acceptance_summary.csv")
    frozen = read_csv(phase337_dir / "phase337_frozen_candidate_ledger.csv")
    features = prepare_holdout_features(load_feature_matrix(phase330_dir))
    scenarios, trades = execute_holdout(features, frozen)
    partition = build_partition_ledger(features)
    controls = build_control_ledger(scenarios)
    passive = build_passive_diagnostic(scenarios)
    gates = build_gate_evaluation(phase337, features, scenarios, controls, passive)
    acceptance = build_acceptance(scenarios, partition, controls, passive, gates)

    scenario_parquet = output_dir / "phase338_holdout_scenario_summary.parquet"
    if not scenarios.empty:
        write_parquet(scenarios, scenario_parquet)
    scenarios.head(100).to_csv(output_dir / "phase338_top_holdout_scenarios.csv", index=False)
    trades.to_csv(output_dir / "phase338_holdout_trade_ledger.csv", index=False)
    partition.to_csv(output_dir / "phase338_partition_ledger.csv", index=False)
    controls.to_csv(output_dir / "phase338_control_ledger.csv", index=False)
    passive.to_csv(output_dir / "phase338_passive_aware_diagnostic_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase338_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase338_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        acceptance,
        {
            "Partition ledger": partition,
            "Top holdout scenarios": scenarios.head(50),
            "Control ledger": controls,
            "Passive-aware diagnostics": passive,
            "Gates": gates,
        },
    )

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase338_cost_stress_holdout_validation_execution",
        **reproducibility_fields(
            artifact_id="phase338",
            generated_utc=generated_utc,
            inputs={
                "phase330_feature_matrix": str(phase330_dir / "phase330_event_catalyst_expanded_feature_matrix.parquet"),
                "phase337_acceptance": str(phase337_dir / "phase337_acceptance_summary.csv"),
                "phase337_frozen_candidates": str(phase337_dir / "phase337_frozen_candidate_ledger.csv"),
            },
            parameters={
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "robust_event_floor": ROBUST_EVENT_FLOOR,
                "holdout_hash_seed": HOLDOUT_HASH_SEED,
                "holdout_bucket_cutoff": HOLDOUT_BUCKET_CUTOFF,
                "cost_profile": COST200,
            },
            outputs={"acceptance_summary": str(output_dir / "phase338_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase338_passive_aware_fill_adverse_forced_flatten_diagnostic",
        ),
    }
    (output_dir / "phase338_cost_stress_holdout_validation_execution_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Execute Phase338 cost-stress holdout validation.")
    parser.add_argument("--phase330-dir", type=Path, default=DEFAULT_PHASE330_DIR)
    parser.add_argument("--phase337-dir", type=Path, default=DEFAULT_PHASE337_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase330_dir, args.phase337_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
