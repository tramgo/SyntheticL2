from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


GATE_PRIORITY = {
    "G04_risk": 1,
    "G02_economic": 2,
    "G01_predictive": 3,
    "G03_robustness": 4,
    "G05_realism": 5,
}

GATE_WORK_PACKAGE = {
    "G01_predictive": "WP9/WP10",
    "G02_economic": "WP8/WP10",
    "G03_robustness": "WP9/WP10",
    "G04_risk": "WP8",
    "G05_realism": "WP10",
}

ACCEPTANCE_MILESTONE = {
    "G01_predictive": "multi_seed_predictive_validation",
    "G02_economic": "broker_reconciled_full_run_economic_validation",
    "G03_robustness": "full_registry_robustness_execution",
    "G04_risk": "full_lifecycle_acceptance_risk_run",
    "G05_realism": "holdout_generator_strategy_rerun",
}

DEPENDENCY_NOTE = {
    "G01_predictive": "Requires calibrated model outputs, baseline comparisons, multi-seed synthetic runs and later multi-day real holdout.",
    "G02_economic": "Requires full event/tick execution P&L, Zerodha rupee cost formulas, slippage stress and broker contract-note reconciliation where available.",
    "G03_robustness": "Requires full required-seed execution, walk-forward folds, parameter-neighborhood smoothness, holdout-generator reruns and real-data reruns.",
    "G04_risk": "Requires full lifecycle risk state over generated trades, daily equity curves, position exposure, halt behavior and tail-loss summaries.",
    "G05_realism": "Requires strategy reruns on holdout generator configurations with feed imperfections and pessimistic execution controls.",
}

RISK_REQUIREMENT_PRIORITY = {
    "broker_exchange_fill_provenance": 1,
    "contract_note_and_cost_reconciliation": 2,
    "strategy_full_run_coverage": 3,
    "daily_equity_curve_and_halt_coverage": 4,
    "daily_loss_limit_validation": 5,
    "drawdown_breach_validation": 6,
    "position_limit_validation": 7,
    "tail_loss_validation": 8,
}

RISK_ACTION_CLASS = {
    "broker_exchange_fill_provenance": "broker_or_exchange_reconciliation",
    "contract_note_and_cost_reconciliation": "broker_contract_note_reconciliation",
    "strategy_full_run_coverage": "acceptance_run_coverage",
    "daily_equity_curve_and_halt_coverage": "risk_state_persistence",
    "daily_loss_limit_validation": "guardrail_validation",
    "drawdown_breach_validation": "guardrail_validation",
    "position_limit_validation": "guardrail_validation",
    "tail_loss_validation": "tail_risk_validation",
}

RISK_DEPENDENCY_TYPE = {
    "broker_exchange_fill_provenance": "external_broker_or_exchange_records",
    "contract_note_and_cost_reconciliation": "external_broker_contract_notes_or_documented_synthetic_substitute",
    "strategy_full_run_coverage": "internal_full_run_event_lifecycle_engine",
    "daily_equity_curve_and_halt_coverage": "internal_full_run_event_lifecycle_engine",
    "daily_loss_limit_validation": "internal_guardrail_replay_plus_acceptance_thresholds",
    "drawdown_breach_validation": "internal_guardrail_replay_plus_acceptance_thresholds",
    "position_limit_validation": "internal_guardrail_replay_plus_acceptance_thresholds",
    "tail_loss_validation": "internal_tail_risk_replay_plus_acceptance_thresholds",
}

ECONOMIC_REQUIREMENT_PRIORITY = {
    "broker_exchange_fill_provenance": 1,
    "contract_note_reconciliation": 2,
    "zerodha_order_formula_ready": 3,
    "latency_slippage_stress_confirmation": 4,
    "retail_and_stress_net_positive": 5,
    "stressed_profile_net_positive": 6,
    "risk_adjusted_economic_joint_pass": 7,
    "multi_day_real_or_holdout_economic_validation": 8,
}

ECONOMIC_ACTION_CLASS = {
    "broker_exchange_fill_provenance": "broker_or_exchange_fill_reconciliation",
    "contract_note_reconciliation": "broker_contract_note_reconciliation",
    "zerodha_order_formula_ready": "documented_cost_formula_validation",
    "latency_slippage_stress_confirmation": "latency_slippage_acceptance_run",
    "retail_and_stress_net_positive": "net_profitability_validation",
    "stressed_profile_net_positive": "net_profitability_validation",
    "risk_adjusted_economic_joint_pass": "risk_adjusted_economic_validation",
    "multi_day_real_or_holdout_economic_validation": "holdout_or_real_multiday_economic_validation",
}

ECONOMIC_DEPENDENCY_TYPE = {
    "broker_exchange_fill_provenance": "external_broker_or_exchange_records",
    "contract_note_reconciliation": "external_broker_contract_notes_or_documented_synthetic_substitute",
    "zerodha_order_formula_ready": "documented_zerodha_charge_formula_and_cost_catalog",
    "latency_slippage_stress_confirmation": "internal_event_lifecycle_latency_slippage_replay",
    "retail_and_stress_net_positive": "internal_full_run_economic_replay_plus_acceptance_thresholds",
    "stressed_profile_net_positive": "internal_stress_profile_economic_replay",
    "risk_adjusted_economic_joint_pass": "internal_joined_economic_and_risk_acceptance_evidence",
    "multi_day_real_or_holdout_economic_validation": "multi_day_real_data_or_untouched_holdout_generator",
}

PREDICTIVE_REQUIREMENT_PRIORITY = {
    "strategy_support_ready": 1,
    "baseline_outperformance": 2,
    "holdout_cell_stability": 3,
    "untouched_test_stability": 4,
    "feature_stability": 5,
    "multi_seed_walk_forward_validation": 6,
    "calibrated_model_output": 7,
    "real_multi_day_holdout": 8,
    "promotion_falsification_clear": 9,
}

PREDICTIVE_ACTION_CLASS = {
    "strategy_support_ready": "strategy_feature_support_closure",
    "baseline_outperformance": "baseline_lift_validation",
    "holdout_cell_stability": "holdout_cell_validation",
    "untouched_test_stability": "untouched_test_validation",
    "feature_stability": "model_feature_stability_validation",
    "multi_seed_walk_forward_validation": "multi_seed_walk_forward_execution",
    "calibrated_model_output": "calibrated_model_training",
    "real_multi_day_holdout": "real_multiday_predictive_holdout",
    "promotion_falsification_clear": "promotion_falsification_clearance",
}

PREDICTIVE_DEPENDENCY_TYPE = {
    "strategy_support_ready": "strategy_feature_product_or_module_support",
    "baseline_outperformance": "calibrated_or_proxy_predictions_with_baselines",
    "holdout_cell_stability": "quarter_feed_segment_holdout_cells",
    "untouched_test_stability": "untouched_test_segments",
    "feature_stability": "multi_seed_model_importance_or_attribution",
    "multi_seed_walk_forward_validation": "registered_seeds_and_walk_forward_folds",
    "calibrated_model_output": "trained_frozen_calibrated_probability_models",
    "real_multi_day_holdout": "multi_day_real_data_holdout",
    "promotion_falsification_clear": "joined_baseline_holdout_feature_and_real_holdout_evidence",
}


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    text = frame.copy()
    for column in text.columns:
        text[column] = text[column].map(lambda value: "" if pd.isna(value) else str(value))
    headers = [str(column) for column in text.columns]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in text.values.tolist())
    return "\n".join(lines)


def load_inputs(paths: dict[str, Path]) -> dict[str, pd.DataFrame]:
    return {
        "acceptance_blockers": pd.read_csv(paths["acceptance_blockers"]),
        "strategy_acceptance_summary": pd.read_csv(paths["strategy_acceptance_summary"]),
        "implementation_gap_backlog": pd.read_csv(paths["implementation_gap_backlog"]),
        "deliverable_traceability": pd.read_csv(paths["deliverable_traceability"]),
        "risk_acceptance_readiness": pd.read_csv(paths["risk_acceptance_readiness"]),
        "risk_breach_severity": pd.read_csv(paths["risk_breach_severity"]),
        "risk_limit_sensitivity": pd.read_csv(paths["risk_limit_sensitivity"]),
        "economic_acceptance_gap": pd.read_csv(paths["economic_acceptance_gap"]),
        "economic_viability_frontier": pd.read_csv(paths["economic_viability_frontier"]),
        "risk_adjusted_economic_frontier": pd.read_csv(paths["risk_adjusted_economic_frontier"]),
        "broker_reconciliation_readiness": pd.read_csv(paths["broker_reconciliation_readiness"]),
        "economic_reconciliation_strategy_summary": pd.read_csv(paths["economic_reconciliation_strategy_summary"]),
        "predictive_acceptance_gap": pd.read_csv(paths["predictive_acceptance_gap"]),
        "predictive_baseline_comparison": pd.read_csv(paths["predictive_baseline_comparison"]),
        "predictive_holdout_stability_summary": pd.read_csv(paths["predictive_holdout_stability_summary"]),
        "predictive_promotion_falsification": pd.read_csv(paths["predictive_promotion_falsification"]),
        "feature_importance_stability": pd.read_csv(paths["feature_importance_stability"]),
    }


def build_gate_summary(blockers: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for gate_id, group in blockers.groupby("gate_id", sort=True):
        rows.append(
            {
                "gate_id": gate_id,
                "gate_name": group["gate_name"].iloc[0],
                "blocked_strategies": int(group["strategy_id"].nunique()),
                "blocker_rows": int(len(group)),
                "blocker_categories": "; ".join(sorted(group["blocker_category"].dropna().astype(str).unique())),
                "evidence_sources_present": int((group["evidence_source_status"] == "present").sum()),
                "evidence_sources_missing": int((group["evidence_source_status"] != "present").sum()),
                "priority_rank": GATE_PRIORITY.get(gate_id, 99),
                "work_package_focus": GATE_WORK_PACKAGE.get(gate_id, "unmapped"),
                "acceptance_milestone": ACCEPTANCE_MILESTONE.get(gate_id, "unmapped"),
                "dependency_note": DEPENDENCY_NOTE.get(gate_id, "No dependency note mapped."),
            }
        )
    return pd.DataFrame(rows).sort_values(["priority_rank", "gate_id"], kind="mergesort")


def build_hardening_queue(
    blockers: pd.DataFrame,
    strategy_summary: pd.DataFrame,
    backlog: pd.DataFrame,
    deliverables: pd.DataFrame,
) -> pd.DataFrame:
    support_map = dict(zip(strategy_summary["strategy_id"], strategy_summary["support_level"]))
    role_map = dict(zip(strategy_summary["strategy_id"], strategy_summary["role"]))
    backlog_focus = (
        backlog.groupby("work_package_id", sort=True)
        .agg(
            backlog_items=("deliverable", "count"),
            backlog_deliverables=("deliverable", lambda values: "; ".join(sorted(map(str, values))[:8])),
        )
        .reset_index()
    )
    backlog_map = backlog_focus.set_index("work_package_id").to_dict("index")
    acceptance_grade_by_wp = (
        deliverables.groupby("work_package_id", sort=True)["acceptance_grade"]
        .agg(lambda values: int(values.sum()))
        .to_dict()
    )

    rows = []
    for row in blockers.itertuples(index=False):
        gate_id = str(row.gate_id)
        wp_focus = GATE_WORK_PACKAGE.get(gate_id, "unmapped")
        primary_wp = wp_focus.split("/")[0]
        backlog_info = backlog_map.get(primary_wp, {"backlog_items": 0, "backlog_deliverables": ""})
        evidence_paths = [part.strip() for part in str(row.evidence_source).split(";") if part.strip()]
        support_level = support_map.get(row.strategy_id, "unknown")
        support_penalty = 1 if support_level == "runnable_proxy" else 2 if support_level == "partial_missing_required_features" else 3
        priority_rank = GATE_PRIORITY.get(gate_id, 99)
        rows.append(
            {
                "queue_rank": 0,
                "priority_band": f"P{priority_rank}",
                "gate_id": gate_id,
                "gate_name": row.gate_name,
                "strategy_id": row.strategy_id,
                "strategy_support_level": support_level,
                "strategy_role": role_map.get(row.strategy_id, "unknown"),
                "work_package_focus": wp_focus,
                "primary_work_package": primary_wp,
                "acceptance_milestone": ACCEPTANCE_MILESTONE.get(gate_id, "unmapped"),
                "blocker_category": row.blocker_category,
                "missing_requirement": row.missing_requirement,
                "next_required_evidence": row.next_required_evidence,
                "current_evidence_sources": row.evidence_source,
                "current_evidence_source_count": len(evidence_paths),
                "current_evidence_source_status": row.evidence_source_status,
                "primary_wp_backlog_items": int(backlog_info["backlog_items"]),
                "primary_wp_proxy_deliverables": backlog_info["backlog_deliverables"],
                "primary_wp_acceptance_grade_deliverables": int(acceptance_grade_by_wp.get(primary_wp, 0)),
                "dependency_note": DEPENDENCY_NOTE.get(gate_id, "No dependency note mapped."),
                "acceptance_ready_now": False,
                "priority_sort_key": priority_rank * 100 + support_penalty,
            }
        )
    frame = pd.DataFrame(rows).sort_values(
        ["priority_sort_key", "gate_id", "strategy_id"],
        kind="mergesort",
    )
    frame["queue_rank"] = range(1, len(frame) + 1)
    return frame.drop(columns=["priority_sort_key"])


def build_strategy_queue_summary(queue: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        queue.groupby("strategy_id", sort=True)
        .agg(
            queue_items=("queue_rank", "count"),
            top_queue_rank=("queue_rank", "min"),
            blocked_gates=("gate_id", lambda values: "; ".join(sorted(set(map(str, values))))),
            first_priority_band=("priority_band", "first"),
            support_level=("strategy_support_level", "first"),
            acceptance_milestones=("acceptance_milestone", lambda values: "; ".join(sorted(set(map(str, values))))),
        )
        .reset_index()
    )
    return grouped.sort_values(["top_queue_rank", "strategy_id"], kind="mergesort")


def _risk_strategy_summary(breach: pd.DataFrame, limits: pd.DataFrame) -> pd.DataFrame:
    if breach.empty:
        breach_summary = pd.DataFrame(columns=["strategy_id"])
    else:
        breach_summary = (
            breach.groupby("strategy_id", sort=True)
            .agg(
                risk_breach_rows=("strategy_id", "count"),
                high_proxy_breach_rows=(
                    "risk_severity_band",
                    lambda values: int((values.astype(str) == "high_proxy_breach_severity").sum()),
                ),
                proxy_risk_pass_candidate_rows=("risk_pass_candidate_proxy", lambda values: int(values.astype(bool).sum())),
                worst_daily_risk_adjusted_net_pnl_inr=("worst_daily_risk_adjusted_net_pnl_inr", "min"),
                worst_tail_loss_1pct_filled_pnl_inr=("tail_loss_1pct_filled_pnl_inr", "min"),
                worst_intraday_drawdown_inr=("max_intraday_drawdown_inr", "min"),
                max_abs_position_units=("max_abs_position_units", "max"),
                max_breach_day_fraction=("breach_day_fraction", "max"),
                max_risk_severity_score=("risk_severity_score", "max"),
            )
            .reset_index()
        )
    if limits.empty:
        limit_summary = pd.DataFrame(columns=["strategy_id"])
    else:
        limit_summary = (
            limits.groupby("strategy_id", sort=True)
            .agg(
                risk_limit_rows=("strategy_id", "count"),
                current_proxy_limit_pass_rows=(
                    "risk_pass_candidate_under_limit_profile",
                    lambda values: 0,
                ),
                any_limit_pass_rows=("risk_pass_candidate_under_limit_profile", lambda values: int(values.astype(bool).sum())),
                high_risk_limit_rows=(
                    "risk_limit_status",
                    lambda values: int((values.astype(str) == "high_proxy_breach_under_limit_profile").sum()),
                ),
                max_risk_limit_severity_score=("risk_limit_severity_score", "max"),
            )
            .reset_index()
        )
        current_limit = limits[limits["risk_limit_profile"].astype(str) == "current_proxy_limits"]
        if not current_limit.empty:
            current_pass = (
                current_limit.groupby("strategy_id", sort=True)["risk_pass_candidate_under_limit_profile"]
                .agg(lambda values: int(values.astype(bool).sum()))
                .reset_index(name="current_proxy_limit_pass_rows")
            )
            limit_summary = limit_summary.drop(columns=["current_proxy_limit_pass_rows"]).merge(
                current_pass,
                on="strategy_id",
                how="left",
            )
    return breach_summary.merge(limit_summary, on="strategy_id", how="outer").fillna(0)


def build_risk_hardening_plan(
    queue: pd.DataFrame,
    readiness: pd.DataFrame,
    breach: pd.DataFrame,
    limits: pd.DataFrame,
) -> pd.DataFrame:
    risk_queue = queue[queue["gate_id"].astype(str) == "G04_risk"][
        ["queue_rank", "priority_band", "strategy_id", "strategy_support_level", "strategy_role"]
    ].copy()
    risk_summary = _risk_strategy_summary(breach, limits)
    rows = readiness.merge(risk_queue, on="strategy_id", how="left").merge(risk_summary, on="strategy_id", how="left")
    rows = rows[rows["queue_rank"].notna()].copy()
    rows["requirement_priority"] = rows["risk_requirement"].map(RISK_REQUIREMENT_PRIORITY).fillna(99).astype(int)
    rows["action_class"] = rows["risk_requirement"].map(RISK_ACTION_CLASS).fillna("unmapped_risk_action")
    rows["dependency_type"] = rows["risk_requirement"].map(RISK_DEPENDENCY_TYPE).fillna("unmapped_dependency")
    rows["proxy_evidence_available"] = rows["proxy_evidence_available"].astype(bool)
    rows["acceptance_requirement_met"] = rows["acceptance_requirement_met"].astype(bool)
    rows["acceptance_ready_now"] = False
    rows["risk_hardening_status"] = rows.apply(
        lambda row: "acceptance_met"
        if row["acceptance_requirement_met"]
        else "proxy_evidence_needs_acceptance_upgrade"
        if row["proxy_evidence_available"]
        else "missing_required_acceptance_evidence",
        axis=1,
    )
    numeric_summary_columns = [
        "risk_breach_rows",
        "high_proxy_breach_rows",
        "proxy_risk_pass_candidate_rows",
        "current_proxy_limit_pass_rows",
        "any_limit_pass_rows",
        "high_risk_limit_rows",
        "max_breach_day_fraction",
        "max_risk_severity_score",
        "max_risk_limit_severity_score",
    ]
    for column in numeric_summary_columns:
        if column in rows:
            rows[column] = rows[column].fillna(0)
    rows["risk_evidence_summary"] = rows.apply(
        lambda row: (
            f"breach_rows={int(row.get('risk_breach_rows', 0))}; "
            f"high_breach_rows={int(row.get('high_proxy_breach_rows', 0))}; "
            f"proxy_pass_rows={int(row.get('proxy_risk_pass_candidate_rows', 0))}; "
            f"current_limit_pass_rows={int(row.get('current_proxy_limit_pass_rows', 0))}; "
            f"any_limit_pass_rows={int(row.get('any_limit_pass_rows', 0))}"
        ),
        axis=1,
    )
    output_columns = [
        "queue_rank",
        "priority_band",
        "strategy_id",
        "strategy_support_level",
        "strategy_role",
        "risk_requirement",
        "requirement_priority",
        "action_class",
        "dependency_type",
        "required_threshold",
        "observed_value",
        "current_evidence_status",
        "proxy_evidence_available",
        "acceptance_requirement_met",
        "risk_hardening_status",
        "blocking_gap",
        "required_next_evidence",
        "risk_evidence_summary",
        "risk_breach_rows",
        "high_proxy_breach_rows",
        "proxy_risk_pass_candidate_rows",
        "current_proxy_limit_pass_rows",
        "any_limit_pass_rows",
        "high_risk_limit_rows",
        "max_breach_day_fraction",
        "max_risk_severity_score",
        "max_risk_limit_severity_score",
        "acceptance_ready_now",
        "evidence_source",
    ]
    for column in output_columns:
        if column not in rows:
            rows[column] = 0 if column.endswith("_rows") or column.startswith("max_") else ""
    return rows[output_columns].sort_values(["queue_rank", "requirement_priority"], kind="mergesort")


def build_risk_action_summary(risk_plan: pd.DataFrame) -> pd.DataFrame:
    if risk_plan.empty:
        return pd.DataFrame(
            columns=[
                "action_class",
                "dependency_type",
                "risk_requirement_rows",
                "strategies",
                "proxy_evidence_rows",
                "acceptance_met_rows",
                "open_rows",
            ]
        )
    grouped = (
        risk_plan.groupby(["action_class", "dependency_type"], sort=True)
        .agg(
            risk_requirement_rows=("risk_requirement", "count"),
            strategies=("strategy_id", "nunique"),
            proxy_evidence_rows=("proxy_evidence_available", lambda values: int(values.astype(bool).sum())),
            acceptance_met_rows=("acceptance_requirement_met", lambda values: int(values.astype(bool).sum())),
        )
        .reset_index()
    )
    grouped["open_rows"] = grouped["risk_requirement_rows"] - grouped["acceptance_met_rows"]
    return grouped.sort_values(["open_rows", "action_class"], ascending=[False, True], kind="mergesort")


def _economic_strategy_summary(
    economic: pd.DataFrame,
    risk_adjusted: pd.DataFrame,
    reconciliation: pd.DataFrame,
) -> pd.DataFrame:
    if economic.empty:
        economic_summary = pd.DataFrame(columns=["strategy_id"])
    else:
        stressed = economic[economic["execution_profile"].astype(str) == "stressed_retail"]
        economic_summary = (
            economic.groupby("strategy_id", sort=True)
            .agg(
                economic_frontier_rows=("strategy_id", "count"),
                net_positive_proxy_rows=("net_positive_proxy", lambda values: int(values.astype(bool).sum())),
                retail_stress_rows=("retail_or_stress_profile", lambda values: int(values.astype(bool).sum())),
                retail_stress_net_positive_rows=(
                    "net_positive_proxy",
                    lambda values: 0,
                ),
                best_net_edge_bps=("net_edge_bps", "max"),
                worst_net_edge_bps=("net_edge_bps", "min"),
                max_additional_gross_edge_needed_bps=("additional_gross_edge_needed_bps", "max"),
                max_cost_reduction_needed_bps=("cost_reduction_needed_bps", "max"),
            )
            .reset_index()
        )
        retail_stress_positive = (
            economic[economic["retail_or_stress_profile"].astype(bool)]
            .groupby("strategy_id", sort=True)["net_positive_proxy"]
            .agg(lambda values: int(values.astype(bool).sum()))
            .reset_index(name="retail_stress_net_positive_rows")
        )
        stressed_positive = (
            stressed.groupby("strategy_id", sort=True)["net_positive_proxy"]
            .agg(lambda values: int(values.astype(bool).sum()))
            .reset_index(name="stressed_net_positive_rows")
        )
        economic_summary = economic_summary.drop(columns=["retail_stress_net_positive_rows"]).merge(
            retail_stress_positive,
            on="strategy_id",
            how="left",
        ).merge(stressed_positive, on="strategy_id", how="left")
    if risk_adjusted.empty:
        risk_adjusted_summary = pd.DataFrame(columns=["strategy_id"])
    else:
        risk_adjusted_summary = (
            risk_adjusted.groupby("strategy_id", sort=True)
            .agg(
                risk_adjusted_rows=("strategy_id", "count"),
                risk_adjusted_joint_pass_rows=("net_positive_and_risk_pass_proxy", lambda values: int(values.astype(bool).sum())),
                retail_stress_joint_pass_rows=(
                    "retail_stress_net_positive_and_risk_pass_proxy",
                    lambda values: int(values.astype(bool).sum()),
                ),
                economic_positive_but_risk_blocked_rows=(
                    "risk_adjusted_frontier_status",
                    lambda values: int((values.astype(str) == "economic_positive_but_risk_blocked_proxy").sum()),
                ),
                best_risk_adjusted_net_edge_bps=("risk_adjusted_net_edge_bps", "max"),
                worst_risk_adjusted_net_edge_bps=("risk_adjusted_net_edge_bps", "min"),
            )
            .reset_index()
        )
    if reconciliation.empty:
        reconciliation_summary = pd.DataFrame(columns=["strategy_id"])
    else:
        reconciliation_summary = reconciliation[
            [
                "strategy_id",
                "documented_zerodha_formula_ready",
                "broker_contract_note_reconciliation_ready",
                "missing_reconciliation_items",
                "economic_acceptance_ready_now",
            ]
        ].copy()
    return (
        economic_summary.merge(risk_adjusted_summary, on="strategy_id", how="outer")
        .merge(reconciliation_summary, on="strategy_id", how="outer")
        .fillna(0)
    )


def build_economic_hardening_plan(
    queue: pd.DataFrame,
    economic_gap: pd.DataFrame,
    economic: pd.DataFrame,
    risk_adjusted: pd.DataFrame,
    broker_reconciliation: pd.DataFrame,
    reconciliation: pd.DataFrame,
) -> pd.DataFrame:
    economic_queue = queue[queue["gate_id"].astype(str) == "G02_economic"][
        ["queue_rank", "priority_band", "strategy_id", "strategy_support_level", "strategy_role"]
    ].copy()
    economic_summary = _economic_strategy_summary(economic, risk_adjusted, reconciliation)
    broker_reconciliation_summary = {
        "broker_reconciliation_items": int(len(broker_reconciliation)),
        "proxy_formula_ready_items": int(broker_reconciliation["proxy_formula_available_now"].astype(bool).sum())
        if "proxy_formula_available_now" in broker_reconciliation
        else 0,
        "contract_note_ready_items": int(broker_reconciliation["broker_contract_note_available_now"].astype(bool).sum())
        if "broker_contract_note_available_now" in broker_reconciliation
        else 0,
        "actual_fill_ready_items": int(broker_reconciliation["actual_fill_available_now"].astype(bool).sum())
        if "actual_fill_available_now" in broker_reconciliation
        else 0,
    }
    rows = economic_gap.merge(economic_queue, on="strategy_id", how="left").merge(economic_summary, on="strategy_id", how="left")
    rows = rows[rows["queue_rank"].notna()].copy()
    for key, value in broker_reconciliation_summary.items():
        rows[key] = value
    rows["requirement_priority"] = rows["economic_requirement"].map(ECONOMIC_REQUIREMENT_PRIORITY).fillna(99).astype(int)
    rows["action_class"] = rows["economic_requirement"].map(ECONOMIC_ACTION_CLASS).fillna("unmapped_economic_action")
    rows["dependency_type"] = rows["economic_requirement"].map(ECONOMIC_DEPENDENCY_TYPE).fillna("unmapped_dependency")
    rows["proxy_evidence_available"] = rows["proxy_evidence_available"].astype(bool)
    rows["acceptance_requirement_met"] = rows["acceptance_requirement_met"].astype(bool)
    rows["acceptance_ready_now"] = False
    rows["economic_hardening_status"] = rows.apply(
        lambda row: "acceptance_met"
        if row["acceptance_requirement_met"]
        else "proxy_evidence_needs_acceptance_upgrade"
        if row["proxy_evidence_available"]
        else "missing_required_acceptance_evidence",
        axis=1,
    )
    numeric_summary_columns = [
        "economic_frontier_rows",
        "net_positive_proxy_rows",
        "retail_stress_rows",
        "retail_stress_net_positive_rows",
        "stressed_net_positive_rows",
        "risk_adjusted_rows",
        "risk_adjusted_joint_pass_rows",
        "retail_stress_joint_pass_rows",
        "economic_positive_but_risk_blocked_rows",
        "missing_reconciliation_items",
        "broker_reconciliation_items",
        "proxy_formula_ready_items",
        "contract_note_ready_items",
        "actual_fill_ready_items",
        "best_net_edge_bps",
        "worst_net_edge_bps",
        "best_risk_adjusted_net_edge_bps",
        "worst_risk_adjusted_net_edge_bps",
        "max_additional_gross_edge_needed_bps",
        "max_cost_reduction_needed_bps",
    ]
    for column in numeric_summary_columns:
        if column in rows:
            rows[column] = rows[column].fillna(0)
    rows["economic_evidence_summary"] = rows.apply(
        lambda row: (
            f"net_positive_rows={int(row.get('net_positive_proxy_rows', 0))}; "
            f"retail_stress_positive_rows={int(row.get('retail_stress_net_positive_rows', 0))}; "
            f"stressed_positive_rows={int(row.get('stressed_net_positive_rows', 0))}; "
            f"risk_adjusted_joint_pass_rows={int(row.get('risk_adjusted_joint_pass_rows', 0))}; "
            f"missing_reconciliation_items={int(row.get('missing_reconciliation_items', 0))}"
        ),
        axis=1,
    )
    output_columns = [
        "queue_rank",
        "priority_band",
        "strategy_id",
        "strategy_support_level",
        "strategy_role",
        "economic_requirement",
        "requirement_priority",
        "action_class",
        "dependency_type",
        "required_threshold",
        "observed_value",
        "current_evidence_status",
        "proxy_evidence_available",
        "acceptance_requirement_met",
        "economic_hardening_status",
        "blocking_gap",
        "required_next_evidence",
        "economic_evidence_summary",
        "economic_frontier_rows",
        "net_positive_proxy_rows",
        "retail_stress_net_positive_rows",
        "stressed_net_positive_rows",
        "risk_adjusted_joint_pass_rows",
        "retail_stress_joint_pass_rows",
        "economic_positive_but_risk_blocked_rows",
        "best_net_edge_bps",
        "best_risk_adjusted_net_edge_bps",
        "broker_reconciliation_items",
        "proxy_formula_ready_items",
        "contract_note_ready_items",
        "actual_fill_ready_items",
        "missing_reconciliation_items",
        "acceptance_ready_now",
        "evidence_source",
    ]
    for column in output_columns:
        if column not in rows:
            rows[column] = 0 if column.endswith("_rows") or column.endswith("_items") or column.endswith("_bps") else ""
    return rows[output_columns].sort_values(["queue_rank", "requirement_priority"], kind="mergesort")


def build_economic_action_summary(economic_plan: pd.DataFrame) -> pd.DataFrame:
    if economic_plan.empty:
        return pd.DataFrame(
            columns=[
                "action_class",
                "dependency_type",
                "economic_requirement_rows",
                "strategies",
                "proxy_evidence_rows",
                "acceptance_met_rows",
                "open_rows",
            ]
        )
    grouped = (
        economic_plan.groupby(["action_class", "dependency_type"], sort=True)
        .agg(
            economic_requirement_rows=("economic_requirement", "count"),
            strategies=("strategy_id", "nunique"),
            proxy_evidence_rows=("proxy_evidence_available", lambda values: int(values.astype(bool).sum())),
            acceptance_met_rows=("acceptance_requirement_met", lambda values: int(values.astype(bool).sum())),
        )
        .reset_index()
    )
    grouped["open_rows"] = grouped["economic_requirement_rows"] - grouped["acceptance_met_rows"]
    return grouped.sort_values(["open_rows", "action_class"], ascending=[False, True], kind="mergesort")


def _predictive_strategy_summary(
    baseline: pd.DataFrame,
    holdout: pd.DataFrame,
    falsification: pd.DataFrame,
    feature_stability: pd.DataFrame,
) -> pd.DataFrame:
    baseline_cols = [
        "strategy_id",
        "directional_eval_rows",
        "directional_accuracy_excess_vs_no_skill",
        "directional_accuracy_excess_vs_majority",
        "brier_skill_score_proxy",
        "beats_no_skill_accuracy_proxy",
        "beats_majority_accuracy_proxy",
        "beats_brier_baseline_proxy",
        "predictive_baseline_status",
    ]
    baseline_summary = baseline[[column for column in baseline_cols if column in baseline.columns]].copy()
    holdout_cols = [
        "strategy_id",
        "stability_cells",
        "cells_with_minimum_rows",
        "cells_beating_local_majority",
        "cell_beat_fraction",
        "untouched_test_cells",
        "untouched_test_cells_beating_local_majority",
        "min_accuracy_excess_vs_majority",
        "median_accuracy_excess_vs_majority",
        "worst_segment_status",
    ]
    holdout_summary = holdout[[column for column in holdout_cols if column in holdout.columns]].copy()
    falsification_cols = [
        "strategy_id",
        "baseline_pass_proxy",
        "holdout_all_cell_pass_proxy",
        "untouched_test_pass_proxy",
        "feature_stability_proxy_available",
        "stable_feature_count_proxy",
        "max_feature_top3_frequency_proxy",
        "median_feature_importance_cv_proxy",
        "predictive_promotion_candidate_proxy",
        "falsification_status",
    ]
    falsification_summary = falsification[[column for column in falsification_cols if column in falsification.columns]].copy()
    stable_feature_count = int((feature_stability["top3_frequency"] >= 0.5).sum()) if "top3_frequency" in feature_stability else 0
    max_top3_frequency = float(feature_stability["top3_frequency"].max()) if "top3_frequency" in feature_stability and len(feature_stability) else 0.0
    median_feature_cv = float(feature_stability["coefficient_of_variation"].median()) if "coefficient_of_variation" in feature_stability and len(feature_stability) else 0.0
    summary = baseline_summary.merge(holdout_summary, on="strategy_id", how="outer").merge(falsification_summary, on="strategy_id", how="outer")
    summary["global_stable_feature_count"] = stable_feature_count
    summary["global_max_feature_top3_frequency"] = max_top3_frequency
    summary["global_median_feature_importance_cv"] = median_feature_cv
    return summary.fillna(0)


def build_predictive_hardening_plan(
    queue: pd.DataFrame,
    predictive_gap: pd.DataFrame,
    baseline: pd.DataFrame,
    holdout: pd.DataFrame,
    falsification: pd.DataFrame,
    feature_stability: pd.DataFrame,
) -> pd.DataFrame:
    predictive_queue = queue[queue["gate_id"].astype(str) == "G01_predictive"][
        ["queue_rank", "priority_band", "strategy_id", "strategy_support_level", "strategy_role"]
    ].copy()
    predictive_summary = _predictive_strategy_summary(baseline, holdout, falsification, feature_stability)
    rows = predictive_gap.merge(predictive_queue, on="strategy_id", how="left").merge(predictive_summary, on="strategy_id", how="left")
    rows = rows[rows["queue_rank"].notna()].copy()
    rows["requirement_priority"] = rows["predictive_requirement"].map(PREDICTIVE_REQUIREMENT_PRIORITY).fillna(99).astype(int)
    rows["action_class"] = rows["predictive_requirement"].map(PREDICTIVE_ACTION_CLASS).fillna("unmapped_predictive_action")
    rows["dependency_type"] = rows["predictive_requirement"].map(PREDICTIVE_DEPENDENCY_TYPE).fillna("unmapped_dependency")
    rows["proxy_evidence_available"] = rows["proxy_evidence_available"].astype(bool)
    rows["acceptance_requirement_met"] = rows["acceptance_requirement_met"].astype(bool)
    rows["acceptance_ready_now"] = False
    rows["predictive_hardening_status"] = rows.apply(
        lambda row: "acceptance_met"
        if row["acceptance_requirement_met"]
        else "proxy_evidence_needs_acceptance_upgrade"
        if row["proxy_evidence_available"]
        else "missing_required_acceptance_evidence",
        axis=1,
    )
    numeric_summary_columns = [
        "directional_eval_rows",
        "directional_accuracy_excess_vs_no_skill",
        "directional_accuracy_excess_vs_majority",
        "brier_skill_score_proxy",
        "stability_cells",
        "cells_with_minimum_rows",
        "cells_beating_local_majority",
        "cell_beat_fraction",
        "untouched_test_cells",
        "untouched_test_cells_beating_local_majority",
        "min_accuracy_excess_vs_majority",
        "median_accuracy_excess_vs_majority",
        "stable_feature_count_proxy",
        "max_feature_top3_frequency_proxy",
        "median_feature_importance_cv_proxy",
        "global_stable_feature_count",
        "global_max_feature_top3_frequency",
        "global_median_feature_importance_cv",
    ]
    for column in numeric_summary_columns:
        if column in rows:
            rows[column] = rows[column].fillna(0)
    for column in [
        "baseline_pass_proxy",
        "holdout_all_cell_pass_proxy",
        "untouched_test_pass_proxy",
        "feature_stability_proxy_available",
        "predictive_promotion_candidate_proxy",
    ]:
        if column in rows:
            rows[column] = rows[column].fillna(False).astype(bool)
    rows["predictive_evidence_summary"] = rows.apply(
        lambda row: (
            f"baseline_pass={bool(row.get('baseline_pass_proxy', False))}; "
            f"holdout_all_cell_pass={bool(row.get('holdout_all_cell_pass_proxy', False))}; "
            f"untouched_test_pass={bool(row.get('untouched_test_pass_proxy', False))}; "
            f"cell_beat_fraction={float(row.get('cell_beat_fraction', 0)):.3f}; "
            f"stable_feature_count={int(row.get('stable_feature_count_proxy', row.get('global_stable_feature_count', 0)))}; "
            f"promotion_candidate={bool(row.get('predictive_promotion_candidate_proxy', False))}"
        ),
        axis=1,
    )
    output_columns = [
        "queue_rank",
        "priority_band",
        "strategy_id",
        "strategy_support_level",
        "strategy_role",
        "predictive_requirement",
        "requirement_priority",
        "action_class",
        "dependency_type",
        "required_threshold",
        "observed_value",
        "current_evidence_status",
        "proxy_evidence_available",
        "acceptance_requirement_met",
        "predictive_hardening_status",
        "blocking_gap",
        "required_next_evidence",
        "predictive_evidence_summary",
        "directional_eval_rows",
        "directional_accuracy_excess_vs_no_skill",
        "directional_accuracy_excess_vs_majority",
        "brier_skill_score_proxy",
        "baseline_pass_proxy",
        "cell_beat_fraction",
        "untouched_test_cells_beating_local_majority",
        "holdout_all_cell_pass_proxy",
        "untouched_test_pass_proxy",
        "feature_stability_proxy_available",
        "stable_feature_count_proxy",
        "predictive_promotion_candidate_proxy",
        "falsification_status",
        "acceptance_ready_now",
        "evidence_source",
    ]
    for column in output_columns:
        if column not in rows:
            rows[column] = 0 if column.endswith("_rows") or column.endswith("_proxy") or column.endswith("_fraction") else ""
    return rows[output_columns].sort_values(["queue_rank", "requirement_priority"], kind="mergesort")


def build_predictive_action_summary(predictive_plan: pd.DataFrame) -> pd.DataFrame:
    if predictive_plan.empty:
        return pd.DataFrame(
            columns=[
                "action_class",
                "dependency_type",
                "predictive_requirement_rows",
                "strategies",
                "proxy_evidence_rows",
                "acceptance_met_rows",
                "open_rows",
            ]
        )
    grouped = (
        predictive_plan.groupby(["action_class", "dependency_type"], sort=True)
        .agg(
            predictive_requirement_rows=("predictive_requirement", "count"),
            strategies=("strategy_id", "nunique"),
            proxy_evidence_rows=("proxy_evidence_available", lambda values: int(values.astype(bool).sum())),
            acceptance_met_rows=("acceptance_requirement_met", lambda values: int(values.astype(bool).sum())),
        )
        .reset_index()
    )
    grouped["open_rows"] = grouped["predictive_requirement_rows"] - grouped["acceptance_met_rows"]
    return grouped.sort_values(["open_rows", "action_class"], ascending=[False, True], kind="mergesort")


def write_report(
    output_dir: Path,
    queue: pd.DataFrame,
    gate_summary: pd.DataFrame,
    strategy_summary: pd.DataFrame,
    risk_plan: pd.DataFrame,
    risk_action_summary: pd.DataFrame,
    economic_plan: pd.DataFrame,
    economic_action_summary: pd.DataFrame,
    predictive_plan: pd.DataFrame,
    predictive_action_summary: pd.DataFrame,
) -> None:
    priority_summary = queue.groupby(["priority_band", "gate_id", "acceptance_milestone"], sort=True).size().reset_index(name="queue_items")
    lines = [
        "# Phase 20 Acceptance Hardening Queue",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This queue converts the current Phase 15 blockers and Phase 17 proxy backlog into executable acceptance-hardening work items.",
        "It is not a promotion result. Every row remains non-acceptance-ready until the required evidence is produced and Phase 15 gates pass.",
        "",
        "## Priority Summary",
        "",
        _markdown_table(priority_summary),
        "",
        "## Gate Summary",
        "",
        _markdown_table(gate_summary),
        "",
        "## Strategy Queue Summary",
        "",
        _markdown_table(strategy_summary),
        "",
        "## Top Queue Items",
        "",
        _markdown_table(queue.head(25)),
        "",
        "## Risk Hardening Action Summary",
        "",
        _markdown_table(risk_action_summary),
        "",
        "## Top Risk Hardening Requirements",
        "",
        _markdown_table(
            risk_plan[
                [
                    "queue_rank",
                    "strategy_id",
                    "risk_requirement",
                    "action_class",
                    "risk_hardening_status",
                    "risk_evidence_summary",
                    "required_next_evidence",
                ]
            ].head(40)
        ),
        "",
        "## Economic Hardening Action Summary",
        "",
        _markdown_table(economic_action_summary),
        "",
        "## Top Economic Hardening Requirements",
        "",
        _markdown_table(
            economic_plan[
                [
                    "queue_rank",
                    "strategy_id",
                    "economic_requirement",
                    "action_class",
                    "economic_hardening_status",
                    "economic_evidence_summary",
                    "required_next_evidence",
                ]
            ].head(40)
        ),
        "",
        "## Predictive Hardening Action Summary",
        "",
        _markdown_table(predictive_action_summary),
        "",
        "## Top Predictive Hardening Requirements",
        "",
        _markdown_table(
            predictive_plan[
                [
                    "queue_rank",
                    "strategy_id",
                    "predictive_requirement",
                    "action_class",
                    "predictive_hardening_status",
                    "predictive_evidence_summary",
                    "required_next_evidence",
                ]
            ].head(40)
        ),
        "",
    ]
    (output_dir / "phase20_acceptance_hardening_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase20(paths: dict[str, Path], output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    inputs = load_inputs(paths)
    gate_summary = build_gate_summary(inputs["acceptance_blockers"])
    queue = build_hardening_queue(
        inputs["acceptance_blockers"],
        inputs["strategy_acceptance_summary"],
        inputs["implementation_gap_backlog"],
        inputs["deliverable_traceability"],
    )
    strategy_queue = build_strategy_queue_summary(queue)
    risk_plan = build_risk_hardening_plan(
        queue,
        inputs["risk_acceptance_readiness"],
        inputs["risk_breach_severity"],
        inputs["risk_limit_sensitivity"],
    )
    risk_action_summary = build_risk_action_summary(risk_plan)
    economic_plan = build_economic_hardening_plan(
        queue,
        inputs["economic_acceptance_gap"],
        inputs["economic_viability_frontier"],
        inputs["risk_adjusted_economic_frontier"],
        inputs["broker_reconciliation_readiness"],
        inputs["economic_reconciliation_strategy_summary"],
    )
    economic_action_summary = build_economic_action_summary(economic_plan)
    predictive_plan = build_predictive_hardening_plan(
        queue,
        inputs["predictive_acceptance_gap"],
        inputs["predictive_baseline_comparison"],
        inputs["predictive_holdout_stability_summary"],
        inputs["predictive_promotion_falsification"],
        inputs["feature_importance_stability"],
    )
    predictive_action_summary = build_predictive_action_summary(predictive_plan)

    queue.to_csv(output_dir / "acceptance_hardening_queue.csv", index=False)
    gate_summary.to_csv(output_dir / "acceptance_hardening_gate_summary.csv", index=False)
    strategy_queue.to_csv(output_dir / "acceptance_hardening_strategy_summary.csv", index=False)
    risk_plan.to_csv(output_dir / "risk_hardening_plan.csv", index=False)
    risk_action_summary.to_csv(output_dir / "risk_hardening_action_summary.csv", index=False)
    economic_plan.to_csv(output_dir / "economic_hardening_plan.csv", index=False)
    economic_action_summary.to_csv(output_dir / "economic_hardening_action_summary.csv", index=False)
    predictive_plan.to_csv(output_dir / "predictive_hardening_plan.csv", index=False)
    predictive_action_summary.to_csv(output_dir / "predictive_hardening_action_summary.csv", index=False)
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "queue_rows": int(len(queue)),
        "gate_summary_rows": int(len(gate_summary)),
        "strategy_summary_rows": int(len(strategy_queue)),
        "risk_hardening_plan_rows": int(len(risk_plan)),
        "risk_hardening_open_rows": int((~risk_plan["acceptance_requirement_met"].astype(bool)).sum()),
        "risk_hardening_proxy_rows": int(risk_plan["proxy_evidence_available"].astype(bool).sum()),
        "risk_hardening_action_summary_rows": int(len(risk_action_summary)),
        "economic_hardening_plan_rows": int(len(economic_plan)),
        "economic_hardening_open_rows": int((~economic_plan["acceptance_requirement_met"].astype(bool)).sum()),
        "economic_hardening_proxy_rows": int(economic_plan["proxy_evidence_available"].astype(bool).sum()),
        "economic_hardening_action_summary_rows": int(len(economic_action_summary)),
        "predictive_hardening_plan_rows": int(len(predictive_plan)),
        "predictive_hardening_open_rows": int((~predictive_plan["acceptance_requirement_met"].astype(bool)).sum()),
        "predictive_hardening_proxy_rows": int(predictive_plan["proxy_evidence_available"].astype(bool).sum()),
        "predictive_hardening_action_summary_rows": int(len(predictive_action_summary)),
        "acceptance_ready_queue_rows": int(queue["acceptance_ready_now"].sum()),
        "top_priority_gate": gate_summary.iloc[0]["gate_id"] if len(gate_summary) else "",
        "scope": "phase20_acceptance_hardening_queue",
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase20",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={
                "gate_priority": GATE_PRIORITY,
                "gate_work_package": GATE_WORK_PACKAGE,
                "acceptance_milestones": ACCEPTANCE_MILESTONE,
            },
            outputs={
                "acceptance_hardening_queue": str(output_dir / "acceptance_hardening_queue.csv"),
                "acceptance_hardening_gate_summary": str(output_dir / "acceptance_hardening_gate_summary.csv"),
                "acceptance_hardening_strategy_summary": str(output_dir / "acceptance_hardening_strategy_summary.csv"),
                "risk_hardening_plan": str(output_dir / "risk_hardening_plan.csv"),
                "risk_hardening_action_summary": str(output_dir / "risk_hardening_action_summary.csv"),
                "economic_hardening_plan": str(output_dir / "economic_hardening_plan.csv"),
                "economic_hardening_action_summary": str(output_dir / "economic_hardening_action_summary.csv"),
                "predictive_hardening_plan": str(output_dir / "predictive_hardening_plan.csv"),
                "predictive_hardening_action_summary": str(output_dir / "predictive_hardening_action_summary.csv"),
                "report": str(output_dir / "phase20_acceptance_hardening_report.md"),
            },
            random_seed="not_applicable_deterministic_blocker_queue",
            scenario_ids="phase15_blockers_by_strategy_gate",
            cost_model_version="outputs/phase12/cost_schedule.csv_and_zerodha_order_formula_v2_or_not_applicable",
            latency_model_version="outputs/phase12/execution_profiles.csv_or_not_applicable",
            base_dir=base_dir,
        )
    )
    (output_dir / "acceptance_hardening_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(
        output_dir,
        queue,
        gate_summary,
        strategy_queue,
        risk_plan,
        risk_action_summary,
        economic_plan,
        economic_action_summary,
        predictive_plan,
        predictive_action_summary,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 20 acceptance-hardening queue artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase20"))
    parser.add_argument("--acceptance-blockers", type=Path, default=Path("outputs/phase15/acceptance_blockers.csv"))
    parser.add_argument("--strategy-acceptance-summary", type=Path, default=Path("outputs/phase15/strategy_acceptance_summary.csv"))
    parser.add_argument("--implementation-gap-backlog", type=Path, default=Path("outputs/phase17/implementation_gap_backlog.csv"))
    parser.add_argument("--deliverable-traceability", type=Path, default=Path("outputs/phase17/deliverable_traceability.csv"))
    parser.add_argument("--risk-acceptance-readiness", type=Path, default=Path("outputs/phase12/full_run_risk_acceptance_readiness.csv"))
    parser.add_argument("--risk-breach-severity", type=Path, default=Path("outputs/phase12/full_run_lifecycle_risk_breach_severity.csv"))
    parser.add_argument("--risk-limit-sensitivity", type=Path, default=Path("outputs/phase12/full_run_lifecycle_risk_limit_sensitivity.csv"))
    parser.add_argument("--economic-acceptance-gap", type=Path, default=Path("outputs/phase16/economic_acceptance_gap_ledger.csv"))
    parser.add_argument("--economic-viability-frontier", type=Path, default=Path("outputs/phase16/economic_viability_frontier.csv"))
    parser.add_argument("--risk-adjusted-economic-frontier", type=Path, default=Path("outputs/phase16/risk_adjusted_economic_frontier.csv"))
    parser.add_argument("--broker-reconciliation-readiness", type=Path, default=Path("outputs/phase16/broker_reconciliation_readiness.csv"))
    parser.add_argument("--economic-reconciliation-strategy-summary", type=Path, default=Path("outputs/phase16/economic_reconciliation_strategy_summary.csv"))
    parser.add_argument("--predictive-acceptance-gap", type=Path, default=Path("outputs/phase16/predictive_acceptance_gap_ledger.csv"))
    parser.add_argument("--predictive-baseline-comparison", type=Path, default=Path("outputs/phase16/predictive_baseline_comparison.csv"))
    parser.add_argument("--predictive-holdout-stability-summary", type=Path, default=Path("outputs/phase16/predictive_holdout_stability_summary.csv"))
    parser.add_argument("--predictive-promotion-falsification", type=Path, default=Path("outputs/phase16/predictive_promotion_falsification.csv"))
    parser.add_argument("--feature-importance-stability", type=Path, default=Path("outputs/phase16/feature_importance_stability_proxy.csv"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "acceptance_blockers": args.acceptance_blockers,
        "strategy_acceptance_summary": args.strategy_acceptance_summary,
        "implementation_gap_backlog": args.implementation_gap_backlog,
        "deliverable_traceability": args.deliverable_traceability,
        "risk_acceptance_readiness": args.risk_acceptance_readiness,
        "risk_breach_severity": args.risk_breach_severity,
        "risk_limit_sensitivity": args.risk_limit_sensitivity,
        "economic_acceptance_gap": args.economic_acceptance_gap,
        "economic_viability_frontier": args.economic_viability_frontier,
        "risk_adjusted_economic_frontier": args.risk_adjusted_economic_frontier,
        "broker_reconciliation_readiness": args.broker_reconciliation_readiness,
        "economic_reconciliation_strategy_summary": args.economic_reconciliation_strategy_summary,
        "predictive_acceptance_gap": args.predictive_acceptance_gap,
        "predictive_baseline_comparison": args.predictive_baseline_comparison,
        "predictive_holdout_stability_summary": args.predictive_holdout_stability_summary,
        "predictive_promotion_falsification": args.predictive_promotion_falsification,
        "feature_importance_stability": args.feature_importance_stability,
    }
    run_phase20(paths, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
