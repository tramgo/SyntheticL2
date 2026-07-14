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

ROBUSTNESS_REQUIREMENT_PRIORITY = {
    "registered_for_alpha_parameter_proxy_grid": 1,
    "full_validation_seed_coverage": 2,
    "execution_profile_robustness": 3,
    "negative_control_rejection": 4,
    "parameter_neighborhood_smoothness": 5,
    "walk_forward_coverage": 6,
    "holdout_generator_strategy_rerun": 7,
    "real_data_rerun": 8,
}

ROBUSTNESS_ACTION_CLASS = {
    "registered_for_alpha_parameter_proxy_grid": "strategy_registry_support_closure",
    "full_validation_seed_coverage": "full_seed_execution",
    "execution_profile_robustness": "execution_profile_robustness_validation",
    "negative_control_rejection": "negative_control_validation",
    "parameter_neighborhood_smoothness": "parameter_smoothness_validation",
    "walk_forward_coverage": "walk_forward_execution",
    "holdout_generator_strategy_rerun": "holdout_generator_strategy_rerun",
    "real_data_rerun": "real_data_robustness_rerun",
}

ROBUSTNESS_DEPENDENCY_TYPE = {
    "registered_for_alpha_parameter_proxy_grid": "phase13_strategy_registry_and_parameter_grid",
    "full_validation_seed_coverage": "registered_full_validation_seed_plan",
    "execution_profile_robustness": "deployable_and_stressed_execution_profiles",
    "negative_control_rejection": "mandatory_negative_control_experiments",
    "parameter_neighborhood_smoothness": "parameter_neighborhood_grid_execution",
    "walk_forward_coverage": "walk_forward_fold_execution",
    "holdout_generator_strategy_rerun": "untouched_holdout_generator_outputs",
    "real_data_rerun": "multi_day_real_data_rerun",
}

REALISM_REQUIREMENT_PRIORITY = {
    "synthetic_quality_gate_clear": 1,
    "strategy_support_ready": 2,
    "holdout_generator_coverage": 3,
    "feed_imperfection_coverage": 4,
    "holdout_strategy_rerun": 5,
    "pessimistic_execution_realism": 6,
    "artifact_exploitation_rejection": 7,
    "real_multi_day_realism_validation": 8,
}

REALISM_ACTION_CLASS = {
    "synthetic_quality_gate_clear": "synthetic_quality_gate_validation",
    "strategy_support_ready": "strategy_support_closure",
    "holdout_generator_coverage": "holdout_generator_coverage_validation",
    "feed_imperfection_coverage": "feed_imperfection_coverage_validation",
    "holdout_strategy_rerun": "holdout_generator_strategy_rerun",
    "pessimistic_execution_realism": "pessimistic_execution_realism_rerun",
    "artifact_exploitation_rejection": "artifact_exploitation_control",
    "real_multi_day_realism_validation": "real_multiday_realism_validation",
}

REALISM_DEPENDENCY_TYPE = {
    "synthetic_quality_gate_clear": "phase14_quality_gates_and_warning_triage",
    "strategy_support_ready": "strategy_feature_product_or_module_support",
    "holdout_generator_coverage": "phase14_holdout_generator_profiles",
    "feed_imperfection_coverage": "phase8_feed_profiles_and_holdout_generator",
    "holdout_strategy_rerun": "untouched_holdout_generator_strategy_outputs",
    "pessimistic_execution_realism": "stressed_retail_latency_slippage_and_fill_controls",
    "artifact_exploitation_rejection": "artifact_control_and_negative_template_reruns",
    "real_multi_day_realism_validation": "multi_day_real_data_validation",
}

EXECUTION_MILESTONE_RANK = {
    "M01_broker_external_reconciliation": 1,
    "M02_strategy_support_and_registry_closure": 2,
    "M03_predictive_model_and_baseline_validation": 3,
    "M04_full_seed_walk_forward_and_robustness_execution": 4,
    "M05_full_lifecycle_risk_and_economic_replay": 5,
    "M06_holdout_generator_and_realism_reruns": 6,
    "M07_real_multiday_acceptance_validation": 7,
}

EXECUTION_MILESTONE_DESCRIPTION = {
    "M01_broker_external_reconciliation": "Broker/exchange fill provenance and contract-note/cost reconciliation prerequisites.",
    "M02_strategy_support_and_registry_closure": "Close unsupported or partial strategy feature, module and registry coverage before acceptance reruns.",
    "M03_predictive_model_and_baseline_validation": "Produce calibrated predictive outputs and baseline/holdout/falsification evidence.",
    "M04_full_seed_walk_forward_and_robustness_execution": "Run full seed, walk-forward, parameter-neighborhood, execution-profile and negative-control robustness tests.",
    "M05_full_lifecycle_risk_and_economic_replay": "Run full event/lifecycle risk, guardrail, slippage, tail-risk and risk-adjusted economic acceptance replays.",
    "M06_holdout_generator_and_realism_reruns": "Rerun strategies on holdout generator profiles, feed imperfections, pessimistic execution and artifact controls.",
    "M07_real_multiday_acceptance_validation": "Validate surviving candidates on diagnostically sound multi-day real data holdouts.",
}

ACTION_CLASS_WORK_PACKAGE = {
    "acceptance_run_coverage": "WP8",
    "artifact_exploitation_control": "WP10",
    "baseline_lift_validation": "WP9/WP10",
    "broker_contract_note_reconciliation": "WP8/WP10",
    "broker_or_exchange_fill_reconciliation": "WP8/WP10",
    "broker_or_exchange_reconciliation": "WP8/WP10",
    "calibrated_model_training": "WP9/WP10",
    "documented_cost_formula_validation": "WP8/WP10",
    "execution_profile_robustness_validation": "WP8/WP10",
    "feed_imperfection_coverage_validation": "WP6/WP10",
    "full_seed_execution": "WP9/WP10",
    "guardrail_validation": "WP8",
    "holdout_cell_validation": "WP10",
    "holdout_generator_coverage_validation": "WP10",
    "holdout_generator_strategy_rerun": "WP10",
    "holdout_or_real_multiday_economic_validation": "WP10",
    "latency_slippage_acceptance_run": "WP8/WP10",
    "model_feature_stability_validation": "WP9/WP10",
    "multi_seed_walk_forward_execution": "WP9/WP10",
    "negative_control_validation": "WP10",
    "net_profitability_validation": "WP8/WP10",
    "parameter_smoothness_validation": "WP9/WP10",
    "pessimistic_execution_realism_rerun": "WP8/WP10",
    "promotion_falsification_clearance": "WP10",
    "real_data_robustness_rerun": "WP10",
    "real_multiday_predictive_holdout": "WP10",
    "real_multiday_realism_validation": "WP10",
    "risk_adjusted_economic_validation": "WP8/WP10",
    "risk_state_persistence": "WP8",
    "strategy_feature_support_closure": "WP9",
    "strategy_registry_support_closure": "WP9/WP10",
    "strategy_support_closure": "WP9",
    "synthetic_quality_gate_validation": "WP10",
    "tail_risk_validation": "WP8",
    "untouched_test_validation": "WP10",
    "walk_forward_execution": "WP9/WP10",
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
        "robustness_acceptance_gap": pd.read_csv(paths["robustness_acceptance_gap"]),
        "robustness_dimension_summary": pd.read_csv(paths["robustness_dimension_summary"]),
        "experiment_profile_robustness_summary": pd.read_csv(paths["experiment_profile_robustness_summary"]),
        "experiment_run_summary": pd.read_csv(paths["experiment_run_summary"]),
        "experiment_registry": pd.read_csv(paths["experiment_registry"]),
        "realism_acceptance_gap": pd.read_csv(paths["realism_acceptance_gap"]),
        "quality_gate_summary": pd.read_csv(paths["quality_gate_summary"]),
        "quality_warning_triage": pd.read_csv(paths["quality_warning_triage"]),
        "holdout_generator_realism_summary": pd.read_csv(paths["holdout_generator_realism_summary"]),
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


def _robustness_strategy_summary(
    dimension: pd.DataFrame,
    profile: pd.DataFrame,
    run_summary: pd.DataFrame,
    registry: pd.DataFrame,
) -> pd.DataFrame:
    dimension_cols = [
        "strategy_id",
        "registered_for_phase13_proxy",
        "proxy_run_rows",
        "profile_robustness_rows",
        "initial_engineering_seeds_run",
        "required_full_validation_seeds",
        "quarter_profiles_run",
        "execution_profiles_evaluated",
        "all_execution_profiles_positive",
        "stressed_profile_positive",
        "negative_control_rows",
        "interpretable_negative_control_rows",
        "passed_negative_control_rows",
        "parameter_sets_planned",
        "parameter_sets_run",
        "walk_forward_windows_planned",
        "walk_forward_windows_run",
        "holdout_generator_profiles_available",
        "holdout_generator_profiles_present_in_proxy",
        "acceptance_eligible",
    ]
    summary = dimension[[column for column in dimension_cols if column in dimension.columns]].copy()
    profile_cols = [
        "strategy_id",
        "positive_base_profiles",
        "worst_profile_base_net_return",
        "best_profile_base_net_return",
        "profile_base_net_return_range",
    ]
    if not profile.empty:
        summary = summary.merge(profile[[column for column in profile_cols if column in profile.columns]], on="strategy_id", how="left")
    run_cols = [
        "strategy_id",
        "run_rows",
        "base_rows",
        "median_base_net_return",
        "worst_control_net_return",
    ]
    if not run_summary.empty:
        summary = summary.merge(run_summary[[column for column in run_cols if column in run_summary.columns]], on="strategy_id", how="left")
    if not registry.empty:
        registry_summary = (
            registry.groupby("strategy_id", sort=True)
            .agg(
                planned_registry_rows=("experiment_id", "count"),
                registry_seeds=("simulation_seed", "nunique"),
                registry_parameter_sets=("parameter_set_id", "nunique"),
                registry_controls=("control_id", "nunique"),
                registry_quarter_profiles=("quarter_profile", "nunique"),
            )
            .reset_index()
        )
        summary = summary.merge(registry_summary, on="strategy_id", how="left")
    return summary.fillna(0)


def build_robustness_hardening_plan(
    queue: pd.DataFrame,
    robustness_gap: pd.DataFrame,
    dimension: pd.DataFrame,
    profile: pd.DataFrame,
    run_summary: pd.DataFrame,
    registry: pd.DataFrame,
) -> pd.DataFrame:
    robustness_queue = queue[queue["gate_id"].astype(str) == "G03_robustness"][
        ["queue_rank", "priority_band", "strategy_id", "strategy_support_level", "strategy_role"]
    ].copy()
    robustness_summary = _robustness_strategy_summary(dimension, profile, run_summary, registry)
    rows = robustness_gap.merge(robustness_queue, on="strategy_id", how="left").merge(robustness_summary, on="strategy_id", how="left")
    rows = rows[rows["queue_rank"].notna()].copy()
    rows["requirement_priority"] = rows["robustness_requirement"].map(ROBUSTNESS_REQUIREMENT_PRIORITY).fillna(99).astype(int)
    rows["action_class"] = rows["robustness_requirement"].map(ROBUSTNESS_ACTION_CLASS).fillna("unmapped_robustness_action")
    rows["dependency_type"] = rows["robustness_requirement"].map(ROBUSTNESS_DEPENDENCY_TYPE).fillna("unmapped_dependency")
    rows["acceptance_requirement_met"] = rows["acceptance_requirement_met"].astype(bool)
    evidence_status = rows["current_evidence_status"].astype(str)
    rows["proxy_evidence_available"] = evidence_status.str.contains(
        "proxy|available|registered|design|present|multi_profile",
        case=False,
        regex=True,
    ) & ~evidence_status.str.contains("not_available|missing", case=False, regex=True)
    rows["proxy_evidence_available"] = rows["proxy_evidence_available"] | rows["acceptance_requirement_met"]
    rows["acceptance_ready_now"] = False
    rows["robustness_hardening_status"] = rows.apply(
        lambda row: "acceptance_met"
        if row["acceptance_requirement_met"]
        else "proxy_evidence_needs_acceptance_upgrade"
        if row["proxy_evidence_available"]
        else "missing_required_acceptance_evidence",
        axis=1,
    )
    numeric_summary_columns = [
        "proxy_run_rows",
        "profile_robustness_rows",
        "initial_engineering_seeds_run",
        "required_full_validation_seeds",
        "quarter_profiles_run",
        "execution_profiles_evaluated",
        "negative_control_rows",
        "interpretable_negative_control_rows",
        "passed_negative_control_rows",
        "parameter_sets_planned",
        "parameter_sets_run",
        "walk_forward_windows_planned",
        "walk_forward_windows_run",
        "holdout_generator_profiles_available",
        "holdout_generator_profiles_present_in_proxy",
        "positive_base_profiles",
        "planned_registry_rows",
        "registry_seeds",
        "registry_parameter_sets",
        "registry_controls",
        "registry_quarter_profiles",
    ]
    for column in numeric_summary_columns:
        if column in rows:
            rows[column] = rows[column].fillna(0)
    for column in [
        "registered_for_phase13_proxy",
        "all_execution_profiles_positive",
        "stressed_profile_positive",
        "acceptance_eligible",
    ]:
        if column in rows:
            rows[column] = rows[column].fillna(False).astype(bool)
    rows["robustness_evidence_summary"] = rows.apply(
        lambda row: (
            f"registered={bool(row.get('registered_for_phase13_proxy', False))}; "
            f"initial_seeds={int(row.get('initial_engineering_seeds_run', 0))}/"
            f"{int(row.get('required_full_validation_seeds', 0))}; "
            f"profiles_positive={bool(row.get('all_execution_profiles_positive', False))}; "
            f"negative_controls_passed={int(row.get('passed_negative_control_rows', 0))}/"
            f"{int(row.get('interpretable_negative_control_rows', 0))}; "
            f"walk_forward_run={int(row.get('walk_forward_windows_run', 0))}/"
            f"{int(row.get('walk_forward_windows_planned', 0))}; "
            f"parameter_sets_run={int(row.get('parameter_sets_run', 0))}/"
            f"{int(row.get('parameter_sets_planned', 0))}"
        ),
        axis=1,
    )
    output_columns = [
        "queue_rank",
        "priority_band",
        "strategy_id",
        "strategy_support_level",
        "strategy_role",
        "robustness_requirement",
        "requirement_priority",
        "action_class",
        "dependency_type",
        "required_threshold",
        "observed_value",
        "current_evidence_status",
        "proxy_evidence_available",
        "acceptance_requirement_met",
        "robustness_hardening_status",
        "blocking_gap",
        "required_next_evidence",
        "robustness_evidence_summary",
        "registered_for_phase13_proxy",
        "proxy_run_rows",
        "initial_engineering_seeds_run",
        "required_full_validation_seeds",
        "execution_profiles_evaluated",
        "all_execution_profiles_positive",
        "passed_negative_control_rows",
        "interpretable_negative_control_rows",
        "parameter_sets_run",
        "parameter_sets_planned",
        "walk_forward_windows_run",
        "walk_forward_windows_planned",
        "holdout_generator_profiles_present_in_proxy",
        "planned_registry_rows",
        "acceptance_ready_now",
        "evidence_source",
    ]
    for column in output_columns:
        if column not in rows:
            rows[column] = 0 if column.endswith("_rows") or column.endswith("_run") or column.endswith("_planned") else ""
    return rows[output_columns].sort_values(["queue_rank", "requirement_priority"], kind="mergesort")


def build_robustness_action_summary(robustness_plan: pd.DataFrame) -> pd.DataFrame:
    if robustness_plan.empty:
        return pd.DataFrame(
            columns=[
                "action_class",
                "dependency_type",
                "robustness_requirement_rows",
                "strategies",
                "proxy_evidence_rows",
                "acceptance_met_rows",
                "open_rows",
            ]
        )
    grouped = (
        robustness_plan.groupby(["action_class", "dependency_type"], sort=True)
        .agg(
            robustness_requirement_rows=("robustness_requirement", "count"),
            strategies=("strategy_id", "nunique"),
            proxy_evidence_rows=("proxy_evidence_available", lambda values: int(values.astype(bool).sum())),
            acceptance_met_rows=("acceptance_requirement_met", lambda values: int(values.astype(bool).sum())),
        )
        .reset_index()
    )
    grouped["open_rows"] = grouped["robustness_requirement_rows"] - grouped["acceptance_met_rows"]
    return grouped.sort_values(["open_rows", "action_class"], ascending=[False, True], kind="mergesort")


def _realism_global_summary(
    quality: pd.DataFrame,
    warning_triage: pd.DataFrame,
    holdout: pd.DataFrame,
) -> dict[str, object]:
    quality_status = quality["status"].astype(str) if "status" in quality else pd.Series(dtype=str)
    holdout_status = holdout["realism_status"].astype(str) if "realism_status" in holdout else pd.Series(dtype=str)
    feed_profiles = sorted(holdout["feed_profile"].dropna().astype(str).unique()) if "feed_profile" in holdout else []
    quarter_profiles = sorted(holdout["quarter_profile"].dropna().astype(str).unique()) if "quarter_profile" in holdout else []
    return {
        "quality_gate_rows": int(len(quality)),
        "quality_pass_rows": int((quality_status == "pass").sum()),
        "quality_warn_rows": int((quality_status == "warn").sum()),
        "quality_fail_rows": int((quality_status == "fail").sum()),
        "warning_triage_rows": int(len(warning_triage)),
        "holdout_generator_rows": int(len(holdout)),
        "holdout_proxy_available_rows": int((holdout_status == "holdout_proxy_available_not_acceptance").sum()),
        "holdout_structural_ready_rows": int(holdout["structural_ready_for_holdout_proxy"].astype(bool).sum())
        if "structural_ready_for_holdout_proxy" in holdout
        else 0,
        "feed_profiles": ";".join(feed_profiles),
        "quarter_profiles": ";".join(quarter_profiles),
        "feed_profile_count": int(len(feed_profiles)),
        "quarter_profile_count": int(len(quarter_profiles)),
    }


def build_realism_hardening_plan(
    queue: pd.DataFrame,
    realism_gap: pd.DataFrame,
    quality: pd.DataFrame,
    warning_triage: pd.DataFrame,
    holdout: pd.DataFrame,
) -> pd.DataFrame:
    realism_queue = queue[queue["gate_id"].astype(str) == "G05_realism"][
        ["queue_rank", "priority_band", "strategy_id", "strategy_support_level", "strategy_role"]
    ].copy()
    rows = realism_gap.merge(realism_queue, on="strategy_id", how="inner")
    summary = _realism_global_summary(quality, warning_triage, holdout)
    for key, value in summary.items():
        rows[key] = value
    rows["requirement_priority"] = rows["realism_requirement"].map(REALISM_REQUIREMENT_PRIORITY).fillna(99).astype(int)
    rows["action_class"] = rows["realism_requirement"].map(REALISM_ACTION_CLASS).fillna("unmapped_realism_action")
    rows["dependency_type"] = rows["realism_requirement"].map(REALISM_DEPENDENCY_TYPE).fillna("unmapped_dependency")
    rows["proxy_evidence_available"] = rows["proxy_evidence_available"].astype(bool)
    rows["acceptance_requirement_met"] = rows["acceptance_requirement_met"].astype(bool)
    rows["acceptance_ready_now"] = False
    rows["realism_hardening_status"] = rows.apply(
        lambda row: "acceptance_met"
        if row["acceptance_requirement_met"]
        else "proxy_evidence_needs_acceptance_upgrade"
        if row["proxy_evidence_available"]
        else "missing_required_acceptance_evidence",
        axis=1,
    )
    rows["realism_evidence_summary"] = rows.apply(
        lambda row: (
            f"quality_pass={int(row.get('quality_pass_rows', 0))}/{int(row.get('quality_gate_rows', 0))}; "
            f"warnings={int(row.get('quality_warn_rows', 0))}; "
            f"fails={int(row.get('quality_fail_rows', 0))}; "
            f"holdout_rows={int(row.get('holdout_generator_rows', 0))}; "
            f"holdout_proxy_rows={int(row.get('holdout_proxy_available_rows', 0))}; "
            f"feed_profiles={int(row.get('feed_profile_count', 0))}; "
            f"quarters={int(row.get('quarter_profile_count', 0))}"
        ),
        axis=1,
    )
    output_columns = [
        "queue_rank",
        "priority_band",
        "strategy_id",
        "strategy_support_level",
        "strategy_role",
        "realism_requirement",
        "requirement_priority",
        "action_class",
        "dependency_type",
        "required_threshold",
        "observed_value",
        "current_evidence_status",
        "proxy_evidence_available",
        "acceptance_requirement_met",
        "realism_hardening_status",
        "blocking_gap",
        "required_next_evidence",
        "realism_evidence_summary",
        "quality_gate_rows",
        "quality_pass_rows",
        "quality_warn_rows",
        "quality_fail_rows",
        "warning_triage_rows",
        "holdout_generator_rows",
        "holdout_proxy_available_rows",
        "holdout_structural_ready_rows",
        "feed_profile_count",
        "quarter_profile_count",
        "acceptance_ready_now",
        "evidence_source",
    ]
    for column in output_columns:
        if column not in rows:
            rows[column] = 0 if column.endswith("_rows") or column.endswith("_count") else ""
    return rows[output_columns].sort_values(["queue_rank", "requirement_priority"], kind="mergesort")


def build_realism_action_summary(realism_plan: pd.DataFrame) -> pd.DataFrame:
    if realism_plan.empty:
        return pd.DataFrame(
            columns=[
                "action_class",
                "dependency_type",
                "realism_requirement_rows",
                "strategies",
                "proxy_evidence_rows",
                "acceptance_met_rows",
                "open_rows",
            ]
        )
    grouped = (
        realism_plan.groupby(["action_class", "dependency_type"], sort=True)
        .agg(
            realism_requirement_rows=("realism_requirement", "count"),
            strategies=("strategy_id", "nunique"),
            proxy_evidence_rows=("proxy_evidence_available", lambda values: int(values.astype(bool).sum())),
            acceptance_met_rows=("acceptance_requirement_met", lambda values: int(values.astype(bool).sum())),
        )
        .reset_index()
    )
    grouped["open_rows"] = grouped["realism_requirement_rows"] - grouped["acceptance_met_rows"]
    return grouped.sort_values(["open_rows", "action_class"], ascending=[False, True], kind="mergesort")


def _execution_milestone_for(action_class: str, dependency_type: str) -> str:
    action = str(action_class)
    dependency = str(dependency_type)
    combined = f"{action} {dependency}"
    if "real_multiday" in action or "multi_day_real" in dependency or "real_data" in dependency:
        return "M07_real_multiday_acceptance_validation"
    if "broker" in combined or "contract_note" in combined or "external_" in dependency:
        return "M01_broker_external_reconciliation"
    if "strategy_feature_support" in action or "strategy_registry" in action or action == "strategy_support_closure":
        return "M02_strategy_support_and_registry_closure"
    if (
        "baseline" in action
        or "calibrated_model" in action
        or "feature_stability" in action
        or "holdout_cell" in action
        or "untouched_test" in action
        or "promotion_falsification" in action
    ):
        return "M03_predictive_model_and_baseline_validation"
    if (
        "seed" in action
        or "walk_forward" in action
        or "parameter" in action
        or "negative_control" in action
        or "execution_profile_robustness" in action
        or "real_data_robustness" in action
    ):
        return "M04_full_seed_walk_forward_and_robustness_execution"
    if (
        "risk" in action
        or "guardrail" in action
        or "tail" in action
        or "profitability" in action
        or "latency_slippage" in action
        or "acceptance_run_coverage" in action
    ):
        return "M05_full_lifecycle_risk_and_economic_replay"
    if (
        "holdout_generator" in action
        or "feed_imperfection" in action
        or "synthetic_quality" in action
        or "pessimistic_execution" in action
        or "artifact" in action
        or "holdout_generator" in dependency
    ):
        return "M06_holdout_generator_and_realism_reruns"
    return "M05_full_lifecycle_risk_and_economic_replay"


def _normalize_hardening_plan(
    plan: pd.DataFrame,
    *,
    gate_id: str,
    gate_name: str,
    requirement_column: str,
    status_column: str,
    evidence_column: str,
) -> pd.DataFrame:
    rows = plan.copy()
    rows["gate_id"] = gate_id
    rows["gate_name"] = gate_name
    rows["hardening_requirement"] = rows[requirement_column].astype(str)
    rows["hardening_status"] = rows[status_column].astype(str)
    rows["evidence_summary"] = rows[evidence_column].astype(str)
    rows["execution_milestone"] = [
        _execution_milestone_for(action_class, dependency_type)
        for action_class, dependency_type in zip(rows["action_class"], rows["dependency_type"])
    ]
    rows["execution_milestone_rank"] = rows["execution_milestone"].map(EXECUTION_MILESTONE_RANK).fillna(99).astype(int)
    rows["execution_milestone_description"] = rows["execution_milestone"].map(EXECUTION_MILESTONE_DESCRIPTION).fillna("")
    rows["gate_priority_rank"] = GATE_PRIORITY[gate_id]
    rows["work_package_focus"] = rows["action_class"].map(ACTION_CLASS_WORK_PACKAGE).fillna(GATE_WORK_PACKAGE[gate_id])
    rows["proxy_evidence_available"] = rows["proxy_evidence_available"].astype(bool)
    rows["acceptance_requirement_met"] = rows["acceptance_requirement_met"].astype(bool)
    rows["acceptance_ready_now"] = rows["acceptance_ready_now"].astype(bool)
    rows["dependency_status"] = rows.apply(
        lambda row: "acceptance_met"
        if row["acceptance_requirement_met"]
        else "proxy_to_upgrade"
        if row["proxy_evidence_available"]
        else "missing_required_evidence",
        axis=1,
    )
    columns = [
        "gate_id",
        "gate_name",
        "gate_priority_rank",
        "execution_milestone",
        "execution_milestone_rank",
        "execution_milestone_description",
        "queue_rank",
        "priority_band",
        "strategy_id",
        "strategy_support_level",
        "strategy_role",
        "work_package_focus",
        "hardening_requirement",
        "requirement_priority",
        "action_class",
        "dependency_type",
        "dependency_status",
        "required_threshold",
        "observed_value",
        "current_evidence_status",
        "proxy_evidence_available",
        "acceptance_requirement_met",
        "acceptance_ready_now",
        "hardening_status",
        "blocking_gap",
        "required_next_evidence",
        "evidence_summary",
        "evidence_source",
    ]
    return rows[columns]


def build_execution_roadmap(
    risk_plan: pd.DataFrame,
    economic_plan: pd.DataFrame,
    predictive_plan: pd.DataFrame,
    robustness_plan: pd.DataFrame,
    realism_plan: pd.DataFrame,
) -> pd.DataFrame:
    roadmap = pd.concat(
        [
            _normalize_hardening_plan(
                risk_plan,
                gate_id="G04_risk",
                gate_name="risk",
                requirement_column="risk_requirement",
                status_column="risk_hardening_status",
                evidence_column="risk_evidence_summary",
            ),
            _normalize_hardening_plan(
                economic_plan,
                gate_id="G02_economic",
                gate_name="economic",
                requirement_column="economic_requirement",
                status_column="economic_hardening_status",
                evidence_column="economic_evidence_summary",
            ),
            _normalize_hardening_plan(
                predictive_plan,
                gate_id="G01_predictive",
                gate_name="predictive",
                requirement_column="predictive_requirement",
                status_column="predictive_hardening_status",
                evidence_column="predictive_evidence_summary",
            ),
            _normalize_hardening_plan(
                robustness_plan,
                gate_id="G03_robustness",
                gate_name="robustness",
                requirement_column="robustness_requirement",
                status_column="robustness_hardening_status",
                evidence_column="robustness_evidence_summary",
            ),
            _normalize_hardening_plan(
                realism_plan,
                gate_id="G05_realism",
                gate_name="realism",
                requirement_column="realism_requirement",
                status_column="realism_hardening_status",
                evidence_column="realism_evidence_summary",
            ),
        ],
        ignore_index=True,
    )
    roadmap = roadmap.sort_values(
        ["execution_milestone_rank", "gate_priority_rank", "queue_rank", "requirement_priority", "strategy_id"],
        kind="mergesort",
    ).reset_index(drop=True)
    roadmap.insert(0, "execution_rank", range(1, len(roadmap) + 1))
    return roadmap


def build_execution_milestone_summary(execution_roadmap: pd.DataFrame) -> pd.DataFrame:
    if execution_roadmap.empty:
        return pd.DataFrame(
            columns=[
                "execution_milestone",
                "execution_milestone_rank",
                "execution_milestone_description",
                "roadmap_rows",
                "gates",
                "strategies",
                "action_classes",
                "work_packages",
                "proxy_evidence_rows",
                "missing_required_evidence_rows",
                "acceptance_met_rows",
                "acceptance_ready_rows",
                "first_execution_rank",
                "top_required_next_evidence",
            ]
        )
    grouped = (
        execution_roadmap.groupby(
            ["execution_milestone", "execution_milestone_rank", "execution_milestone_description"],
            sort=True,
        )
        .agg(
            roadmap_rows=("hardening_requirement", "size"),
            gates=("gate_id", "nunique"),
            strategies=("strategy_id", "nunique"),
            action_classes=("action_class", "nunique"),
            work_packages=("work_package_focus", "nunique"),
            proxy_evidence_rows=("proxy_evidence_available", "sum"),
            acceptance_met_rows=("acceptance_requirement_met", "sum"),
            acceptance_ready_rows=("acceptance_ready_now", "sum"),
            first_execution_rank=("execution_rank", "min"),
            top_required_next_evidence=("required_next_evidence", "first"),
        )
        .reset_index()
    )
    grouped["missing_required_evidence_rows"] = grouped["roadmap_rows"] - grouped["proxy_evidence_rows"]
    return grouped[
        [
            "execution_milestone",
            "execution_milestone_rank",
            "execution_milestone_description",
            "roadmap_rows",
            "gates",
            "strategies",
            "action_classes",
            "work_packages",
            "proxy_evidence_rows",
            "missing_required_evidence_rows",
            "acceptance_met_rows",
            "acceptance_ready_rows",
            "first_execution_rank",
            "top_required_next_evidence",
        ]
    ].sort_values(["execution_milestone_rank"], kind="mergesort")


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
    robustness_plan: pd.DataFrame,
    robustness_action_summary: pd.DataFrame,
    realism_plan: pd.DataFrame,
    realism_action_summary: pd.DataFrame,
    execution_roadmap: pd.DataFrame,
    execution_milestone_summary: pd.DataFrame,
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
        "## Execution Milestone Roadmap",
        "",
        _markdown_table(execution_milestone_summary),
        "",
        "## Top Execution Roadmap Rows",
        "",
        _markdown_table(
            execution_roadmap[
                [
                    "execution_rank",
                    "execution_milestone",
                    "gate_id",
                    "strategy_id",
                    "work_package_focus",
                    "hardening_requirement",
                    "action_class",
                    "dependency_status",
                    "hardening_status",
                    "required_next_evidence",
                ]
            ].head(60)
        ),
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
        "## Robustness Hardening Action Summary",
        "",
        _markdown_table(robustness_action_summary),
        "",
        "## Top Robustness Hardening Requirements",
        "",
        _markdown_table(
            robustness_plan[
                [
                    "queue_rank",
                    "strategy_id",
                    "robustness_requirement",
                    "action_class",
                    "robustness_hardening_status",
                    "robustness_evidence_summary",
                    "required_next_evidence",
                ]
            ].head(40)
        ),
        "",
        "## Realism Hardening Action Summary",
        "",
        _markdown_table(realism_action_summary),
        "",
        "## Top Realism Hardening Requirements",
        "",
        _markdown_table(
            realism_plan[
                [
                    "queue_rank",
                    "strategy_id",
                    "realism_requirement",
                    "action_class",
                    "realism_hardening_status",
                    "realism_evidence_summary",
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
    robustness_plan = build_robustness_hardening_plan(
        queue,
        inputs["robustness_acceptance_gap"],
        inputs["robustness_dimension_summary"],
        inputs["experiment_profile_robustness_summary"],
        inputs["experiment_run_summary"],
        inputs["experiment_registry"],
    )
    robustness_action_summary = build_robustness_action_summary(robustness_plan)
    realism_plan = build_realism_hardening_plan(
        queue,
        inputs["realism_acceptance_gap"],
        inputs["quality_gate_summary"],
        inputs["quality_warning_triage"],
        inputs["holdout_generator_realism_summary"],
    )
    realism_action_summary = build_realism_action_summary(realism_plan)
    execution_roadmap = build_execution_roadmap(
        risk_plan,
        economic_plan,
        predictive_plan,
        robustness_plan,
        realism_plan,
    )
    execution_milestone_summary = build_execution_milestone_summary(execution_roadmap)

    queue.to_csv(output_dir / "acceptance_hardening_queue.csv", index=False)
    gate_summary.to_csv(output_dir / "acceptance_hardening_gate_summary.csv", index=False)
    strategy_queue.to_csv(output_dir / "acceptance_hardening_strategy_summary.csv", index=False)
    execution_roadmap.to_csv(output_dir / "acceptance_execution_roadmap.csv", index=False)
    execution_milestone_summary.to_csv(output_dir / "acceptance_execution_milestones.csv", index=False)
    risk_plan.to_csv(output_dir / "risk_hardening_plan.csv", index=False)
    risk_action_summary.to_csv(output_dir / "risk_hardening_action_summary.csv", index=False)
    economic_plan.to_csv(output_dir / "economic_hardening_plan.csv", index=False)
    economic_action_summary.to_csv(output_dir / "economic_hardening_action_summary.csv", index=False)
    predictive_plan.to_csv(output_dir / "predictive_hardening_plan.csv", index=False)
    predictive_action_summary.to_csv(output_dir / "predictive_hardening_action_summary.csv", index=False)
    robustness_plan.to_csv(output_dir / "robustness_hardening_plan.csv", index=False)
    robustness_action_summary.to_csv(output_dir / "robustness_hardening_action_summary.csv", index=False)
    realism_plan.to_csv(output_dir / "realism_hardening_plan.csv", index=False)
    realism_action_summary.to_csv(output_dir / "realism_hardening_action_summary.csv", index=False)
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "queue_rows": int(len(queue)),
        "gate_summary_rows": int(len(gate_summary)),
        "strategy_summary_rows": int(len(strategy_queue)),
        "acceptance_execution_roadmap_rows": int(len(execution_roadmap)),
        "acceptance_execution_milestone_rows": int(len(execution_milestone_summary)),
        "acceptance_execution_roadmap_proxy_rows": int(execution_roadmap["proxy_evidence_available"].astype(bool).sum()),
        "acceptance_execution_roadmap_missing_rows": int((~execution_roadmap["proxy_evidence_available"].astype(bool)).sum()),
        "acceptance_execution_roadmap_met_rows": int(execution_roadmap["acceptance_requirement_met"].astype(bool).sum()),
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
        "robustness_hardening_plan_rows": int(len(robustness_plan)),
        "robustness_hardening_open_rows": int((~robustness_plan["acceptance_requirement_met"].astype(bool)).sum()),
        "robustness_hardening_proxy_rows": int(robustness_plan["proxy_evidence_available"].astype(bool).sum()),
        "robustness_hardening_action_summary_rows": int(len(robustness_action_summary)),
        "realism_hardening_plan_rows": int(len(realism_plan)),
        "realism_hardening_open_rows": int((~realism_plan["acceptance_requirement_met"].astype(bool)).sum()),
        "realism_hardening_proxy_rows": int(realism_plan["proxy_evidence_available"].astype(bool).sum()),
        "realism_hardening_action_summary_rows": int(len(realism_action_summary)),
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
                "acceptance_execution_roadmap": str(output_dir / "acceptance_execution_roadmap.csv"),
                "acceptance_execution_milestones": str(output_dir / "acceptance_execution_milestones.csv"),
                "risk_hardening_plan": str(output_dir / "risk_hardening_plan.csv"),
                "risk_hardening_action_summary": str(output_dir / "risk_hardening_action_summary.csv"),
                "economic_hardening_plan": str(output_dir / "economic_hardening_plan.csv"),
                "economic_hardening_action_summary": str(output_dir / "economic_hardening_action_summary.csv"),
                "predictive_hardening_plan": str(output_dir / "predictive_hardening_plan.csv"),
                "predictive_hardening_action_summary": str(output_dir / "predictive_hardening_action_summary.csv"),
                "robustness_hardening_plan": str(output_dir / "robustness_hardening_plan.csv"),
                "robustness_hardening_action_summary": str(output_dir / "robustness_hardening_action_summary.csv"),
                "realism_hardening_plan": str(output_dir / "realism_hardening_plan.csv"),
                "realism_hardening_action_summary": str(output_dir / "realism_hardening_action_summary.csv"),
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
        robustness_plan,
        robustness_action_summary,
        realism_plan,
        realism_action_summary,
        execution_roadmap,
        execution_milestone_summary,
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
    parser.add_argument("--robustness-acceptance-gap", type=Path, default=Path("outputs/phase13/robustness_acceptance_gap_ledger.csv"))
    parser.add_argument("--robustness-dimension-summary", type=Path, default=Path("outputs/phase13/robustness_dimension_summary.csv"))
    parser.add_argument("--experiment-profile-robustness-summary", type=Path, default=Path("outputs/phase13/experiment_profile_robustness_summary.csv"))
    parser.add_argument("--experiment-run-summary", type=Path, default=Path("outputs/phase13/experiment_run_summary.csv"))
    parser.add_argument("--experiment-registry", type=Path, default=Path("outputs/phase13/experiment_registry.csv"))
    parser.add_argument("--realism-acceptance-gap", type=Path, default=Path("outputs/phase14/realism_acceptance_gap_ledger.csv"))
    parser.add_argument("--quality-gate-summary", type=Path, default=Path("outputs/phase14/quality_gate_summary.csv"))
    parser.add_argument("--quality-warning-triage", type=Path, default=Path("outputs/phase14/quality_warning_triage.csv"))
    parser.add_argument("--holdout-generator-realism-summary", type=Path, default=Path("outputs/phase14/holdout_generator_realism_summary.csv"))
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
        "robustness_acceptance_gap": args.robustness_acceptance_gap,
        "robustness_dimension_summary": args.robustness_dimension_summary,
        "experiment_profile_robustness_summary": args.experiment_profile_robustness_summary,
        "experiment_run_summary": args.experiment_run_summary,
        "experiment_registry": args.experiment_registry,
        "realism_acceptance_gap": args.realism_acceptance_gap,
        "quality_gate_summary": args.quality_gate_summary,
        "quality_warning_triage": args.quality_warning_triage,
        "holdout_generator_realism_summary": args.holdout_generator_realism_summary,
    }
    run_phase20(paths, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
