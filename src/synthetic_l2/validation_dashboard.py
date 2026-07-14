from __future__ import annotations

import argparse
import html
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def _status_class(value: object) -> str:
    text = str(value).lower()
    if text in {"pass", "available", "computed_proxy", "sample_proxy", "proxy_available", "implemented", "implemented_proxy"}:
        return "ok"
    if text in {"warn", "partial_current", "partial_proxy"}:
        return "warn"
    if text in {"fail", "blocked", "missing", "not_supported_by_current_product"}:
        return "bad"
    return "neutral"


def _table(frame: pd.DataFrame, columns: list[str] | None = None, max_rows: int = 20) -> str:
    if frame.empty:
        return "<p class='muted'>No rows.</p>"
    data = frame.copy()
    if columns is not None:
        data = data[[column for column in columns if column in data.columns]]
    data = data.head(max_rows)
    header = "".join(f"<th>{html.escape(str(column))}</th>" for column in data.columns)
    rows = []
    for record in data.to_dict("records"):
        cells = []
        for column in data.columns:
            value = record[column]
            text = "" if pd.isna(value) else str(value)
            cls = _status_class(value) if column in {"status", "current_status", "gate_status", "implementation_status", "priority", "acceptance_status"} else ""
            cells.append(f"<td class='{cls}'>{html.escape(text)}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return "<table><thead><tr>" + header + "</tr></thead><tbody>" + "".join(rows) + "</tbody></table>"


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    text = frame.copy()
    for column in text.columns:
        text[column] = text[column].map(lambda value: "" if pd.isna(value) else str(value))
    headers = [str(column) for column in text.columns]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |" for row in text.values.tolist())
    return "\n".join(lines)


def _metric_card(label: str, value: object, note: str = "") -> str:
    return (
        "<div class='card'>"
        f"<div class='card-label'>{html.escape(label)}</div>"
        f"<div class='card-value'>{html.escape(str(value))}</div>"
        f"<div class='card-note'>{html.escape(note)}</div>"
        "</div>"
    )


def _bar_rows(frame: pd.DataFrame, label_col: str, value_col: str) -> str:
    if frame.empty:
        return "<p class='muted'>No rows.</p>"
    max_value = max(float(frame[value_col].max()), 1.0)
    rows = []
    for record in frame.to_dict("records"):
        label = str(record[label_col])
        value = float(record[value_col])
        width = max(2.0, 100.0 * value / max_value)
        rows.append(
            "<div class='bar-row'>"
            f"<div class='bar-label'>{html.escape(label)}</div>"
            f"<div class='bar-track'><div class='bar-fill' style='width:{width:.2f}%'></div></div>"
            f"<div class='bar-value'>{value:.0f}</div>"
            "</div>"
        )
    return "".join(rows)


def build_dashboard(paths: dict[str, Path]) -> tuple[str, str, pd.DataFrame, dict]:
    quality = _read_csv(paths["quality"])
    holdout = _read_csv(paths["holdout"])
    realism_gap = _read_csv(paths["realism_gap"])
    lifecycle_risk = _read_csv(paths["lifecycle_risk"])
    lifecycle_risk_severity = _read_csv(paths["lifecycle_risk_severity"])
    lifecycle_risk_limit_sensitivity = _read_csv(paths["lifecycle_risk_limit_sensitivity"])
    risk_acceptance_readiness = _read_csv(paths["risk_acceptance_readiness"])
    robustness_dimension = _read_csv(paths["robustness_dimension"])
    robustness_gap = _read_csv(paths["robustness_gap"])
    acceptance = _read_csv(paths["acceptance"])
    blockers = _read_csv(paths["blockers"])
    metric_catalog = _read_csv(paths["metric_catalog"])
    predictive = _read_csv(paths["predictive"])
    predictive_holdout = _read_csv(paths["predictive_holdout"])
    predictive_falsification = _read_csv(paths["predictive_falsification"])
    predictive_gap = _read_csv(paths["predictive_gap"])
    trading = _read_csv(paths["trading"])
    economic = _read_csv(paths["economic"])
    risk_adjusted_economic = _read_csv(paths["risk_adjusted_economic"])
    broker_reconciliation = _read_csv(paths["broker_reconciliation"])
    economic_reconciliation = _read_csv(paths["economic_reconciliation"])
    economic_gap = _read_csv(paths["economic_gap"])
    markout = _read_csv(paths["markout"])
    gaps = _read_csv(paths["gaps"])
    hardening_queue = _read_csv(paths["hardening_queue"])
    hardening_gate_summary = _read_csv(paths["hardening_gate_summary"])
    execution_roadmap = _read_csv(paths["execution_roadmap"])
    execution_milestones = _read_csv(paths["execution_milestones"])
    risk_hardening_plan = _read_csv(paths["risk_hardening_plan"])
    risk_hardening_action_summary = _read_csv(paths["risk_hardening_action_summary"])
    economic_hardening_plan = _read_csv(paths["economic_hardening_plan"])
    economic_hardening_action_summary = _read_csv(paths["economic_hardening_action_summary"])
    predictive_hardening_plan = _read_csv(paths["predictive_hardening_plan"])
    predictive_hardening_action_summary = _read_csv(paths["predictive_hardening_action_summary"])
    robustness_hardening_plan = _read_csv(paths["robustness_hardening_plan"])
    robustness_hardening_action_summary = _read_csv(paths["robustness_hardening_action_summary"])
    realism_hardening_plan = _read_csv(paths["realism_hardening_plan"])
    realism_hardening_action_summary = _read_csv(paths["realism_hardening_action_summary"])
    broker_import_checklist = _read_csv(paths["broker_import_checklist"])
    broker_evidence_schema = _read_csv(paths["broker_evidence_schema"])
    broker_external_gap_ledger = _read_csv(paths["broker_external_gap_ledger"])
    broker_external_gap_summary = _read_csv(paths["broker_external_gap_summary"])
    broker_reconciliation_test_catalog = _read_csv(paths["broker_reconciliation_test_catalog"])
    strategy_support_criteria = _read_csv(paths["strategy_support_criteria"])
    strategy_support_ledger = _read_csv(paths["strategy_support_ledger"])
    strategy_support_gap_summary = _read_csv(paths["strategy_support_gap_summary"])
    strategy_support_decision_summary = _read_csv(paths["strategy_support_decision_summary"])
    predictive_validation_criteria = _read_csv(paths["predictive_validation_criteria"])
    predictive_validation_ledger = _read_csv(paths["predictive_validation_ledger"])
    predictive_validation_gap_summary = _read_csv(paths["predictive_validation_gap_summary"])
    predictive_validation_strategy_summary = _read_csv(paths["predictive_validation_strategy_summary"])
    robustness_execution_criteria = _read_csv(paths["robustness_execution_criteria"])
    robustness_execution_ledger = _read_csv(paths["robustness_execution_ledger"])
    robustness_execution_gap_summary = _read_csv(paths["robustness_execution_gap_summary"])
    robustness_execution_strategy_summary = _read_csv(paths["robustness_execution_strategy_summary"])
    lifecycle_economic_criteria = _read_csv(paths["lifecycle_economic_criteria"])
    lifecycle_economic_ledger = _read_csv(paths["lifecycle_economic_ledger"])
    lifecycle_economic_gap_summary = _read_csv(paths["lifecycle_economic_gap_summary"])
    lifecycle_economic_strategy_summary = _read_csv(paths["lifecycle_economic_strategy_summary"])
    realism_rerun_criteria = _read_csv(paths["realism_rerun_criteria"])
    realism_rerun_ledger = _read_csv(paths["realism_rerun_ledger"])
    realism_rerun_gap_summary = _read_csv(paths["realism_rerun_gap_summary"])
    realism_rerun_strategy_summary = _read_csv(paths["realism_rerun_strategy_summary"])
    real_multiday_criteria = _read_csv(paths["real_multiday_criteria"])
    real_multiday_ledger = _read_csv(paths["real_multiday_ledger"])
    real_multiday_gap_summary = _read_csv(paths["real_multiday_gap_summary"])
    real_multiday_strategy_summary = _read_csv(paths["real_multiday_strategy_summary"])
    stage_a2_criteria = _read_csv(paths["stage_a2_criteria"])
    stage_a2_schema = _read_csv(paths["stage_a2_schema"])
    stage_a2_ledger = _read_csv(paths["stage_a2_ledger"])
    stage_a2_gap_summary = _read_csv(paths["stage_a2_gap_summary"])
    stage_a2_readiness_summary = _read_csv(paths["stage_a2_readiness_summary"])
    stage_b1_subset = _read_csv(paths["stage_b1_subset"])
    stage_b1_criteria = _read_csv(paths["stage_b1_criteria"])
    stage_b1_scenario_summary = _read_csv(paths["stage_b1_scenario_summary"])
    stage_b1_check_ledger = _read_csv(paths["stage_b1_check_ledger"])
    stage_b2_readiness = _read_csv(paths["stage_b2_readiness"])
    stage_b2_criteria = _read_csv(paths["stage_b2_criteria"])
    stage_b2_scenario_selection = _read_csv(paths["stage_b2_scenario_selection"])
    stage_b2_dataset_summary = _read_csv(paths["stage_b2_dataset_summary"])
    stage_b2_check_ledger = _read_csv(paths["stage_b2_check_ledger"])
    stage_c_selected_days = _read_csv(paths["stage_c_selected_days"])
    stage_c_selected_seeds = _read_csv(paths["stage_c_selected_seeds"])
    stage_c_dataset_summary = _read_csv(paths["stage_c_dataset_summary"])
    stage_c_check_ledger = _read_csv(paths["stage_c_check_ledger"])
    stage_c_strategy_runs = _read_csv(paths["stage_c_strategy_runs"])
    stage_c_baseline_runs = _read_csv(paths["stage_c_baseline_runs"])
    stage_d_profile_summary = _read_csv(paths["stage_d_profile_summary"])
    stage_d_seed_summary = _read_csv(paths["stage_d_seed_summary"])
    stage_d_data_inventory = _read_csv(paths["stage_d_data_inventory"])
    stage_d_dataset_summary = _read_csv(paths["stage_d_dataset_summary"])
    stage_d_check_ledger = _read_csv(paths["stage_d_check_ledger"])
    stage_d_strategy_summary = _read_csv(paths["stage_d_strategy_summary"])
    stage_e_criteria = _read_csv(paths["stage_e_criteria"])
    stage_e_prerequisite_ledger = _read_csv(paths["stage_e_prerequisite_ledger"])
    stage_e_gap_summary = _read_csv(paths["stage_e_gap_summary"])
    stage_e_action_plan = _read_csv(paths["stage_e_action_plan"])
    phase21_decision_rules = _read_csv(paths["phase21_decision_rules"])
    phase21_decision_ledger = _read_csv(paths["phase21_decision_ledger"])
    phase21_decision_summary = _read_csv(paths["phase21_decision_summary"])
    phase22_milestone_catalog = _read_csv(paths["phase22_milestone_catalog"])
    phase22_recalibration_task_ledger = _read_csv(paths["phase22_recalibration_task_ledger"])
    phase22_capture_expansion_plan = _read_csv(paths["phase22_capture_expansion_plan"])
    phase22_summary = _read_csv(paths["phase22_summary"])
    phase23_risk_register = _read_csv(paths["phase23_risk_register"])
    phase23_mitigation_ledger = _read_csv(paths["phase23_mitigation_ledger"])
    phase23_promotion_path = _read_csv(paths["phase23_promotion_path"])
    phase23_summary = _read_csv(paths["phase23_summary"])
    phase25_replay_summary = _read_csv(paths["phase25_replay_summary"])
    phase25_risk_summary = _read_csv(paths["phase25_risk_summary"])
    phase25_baseline_comparison = _read_csv(paths["phase25_baseline_comparison"])
    phase25_overall_summary = _read_csv(paths["phase25_overall_summary"])
    phase26_variant_catalog = _read_csv(paths["phase26_variant_catalog"])
    phase26_summary = _read_csv(paths["phase26_summary"])
    phase26_candidate_summary = _read_csv(paths["phase26_candidate_summary"])
    phase26_rejection_ledger = _read_csv(paths["phase26_rejection_ledger"])
    phase26_overall_summary = _read_csv(paths["phase26_overall_summary"])
    phase27_candidate_catalog = _read_csv(paths["phase27_candidate_catalog"])
    phase27_candidate_summary = _read_csv(paths["phase27_candidate_summary"])
    phase27_family_summary = _read_csv(paths["phase27_family_summary"])
    phase27_rejection_ledger = _read_csv(paths["phase27_rejection_ledger"])
    phase27_overall_summary = _read_csv(paths["phase27_overall_summary"])
    phase28_feature_label_catalog = _read_csv(paths["phase28_feature_label_catalog"])
    phase28_event_label_summary = _read_csv(paths["phase28_event_label_summary"])
    phase28_lead_lag_summary = _read_csv(paths["phase28_lead_lag_summary"])
    phase28_strategy_support_summary = _read_csv(paths["phase28_strategy_support_summary"])
    phase28_overall_summary = _read_csv(paths["phase28_overall_summary"])
    phase29_summary = _read_csv(paths["phase29_summary"])
    phase29_risk_summary = _read_csv(paths["phase29_risk_summary"])
    phase29_candidate_summary = _read_csv(paths["phase29_candidate_summary"])
    phase29_overall_summary = _read_csv(paths["phase29_overall_summary"])
    phase30_decision_ledger = _read_csv(paths["phase30_decision_ledger"])
    phase30_execution_evidence = _read_csv(paths["phase30_execution_evidence"])
    phase30_redesign_queue = _read_csv(paths["phase30_redesign_queue"])
    phase30_overall_summary = _read_csv(paths["phase30_overall_summary"])
    phase31_spec_catalog = _read_csv(paths["phase31_spec_catalog"])
    phase31_contract_ledger = _read_csv(paths["phase31_contract_ledger"])
    phase31_replay_gate = _read_csv(paths["phase31_replay_gate"])
    phase31_overall_summary = _read_csv(paths["phase31_overall_summary"])
    phase32_scan_ledger = _read_csv(paths["phase32_scan_ledger"])
    phase32_availability_summary = _read_csv(paths["phase32_availability_summary"])
    phase32_acquisition_queue = _read_csv(paths["phase32_acquisition_queue"])
    phase32_strategy_summary = _read_csv(paths["phase32_strategy_summary"])
    phase32_overall_summary = _read_csv(paths["phase32_overall_summary"])
    phase33_template_inventory = _read_csv(paths["phase33_template_inventory"])
    phase33_file_validation = _read_csv(paths["phase33_file_validation"])
    phase33_test_readiness = _read_csv(paths["phase33_test_readiness"])
    phase33_overall_summary = _read_csv(paths["phase33_overall_summary"])
    phase34_symbol_day_coverage = _read_csv(paths["phase34_symbol_day_coverage"])
    phase34_day_inventory = _read_csv(paths["phase34_day_inventory"])
    phase34_readiness_summary = _read_csv(paths["phase34_readiness_summary"])
    phase34_acquisition_plan = _read_csv(paths["phase34_acquisition_plan"])

    quality_status = quality["status"].value_counts().rename_axis("status").reset_index(name="checks")
    realism_gap_status = (
        realism_gap.groupby(["proxy_evidence_available", "acceptance_requirement_met"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    gate_blockers = blockers["gate_id"].value_counts().rename_axis("gate_id").reset_index(name="blockers").sort_values("gate_id")
    metric_status = metric_catalog.groupby(["metric_category", "current_status"], sort=True).size().reset_index(name="metrics")
    gap_priority = gaps["priority"].value_counts().rename_axis("priority").reset_index(name="gaps").sort_values("priority")
    top_predictive = predictive.sort_values("balanced_accuracy_proxy", ascending=False)
    top_predictive_holdout = predictive_holdout.sort_values("cell_beat_fraction", ascending=False)
    top_predictive_falsification = predictive_falsification.sort_values("predictive_promotion_candidate_proxy", ascending=False)
    predictive_gap_status = (
        predictive_gap.groupby(["proxy_evidence_available", "acceptance_requirement_met"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    top_trading = trading.sort_values("mean_net_return", ascending=False)
    top_economic = economic.sort_values("net_edge_bps", ascending=False)
    top_risk_adjusted_economic = risk_adjusted_economic.sort_values("risk_adjusted_net_edge_bps", ascending=False)
    economic_gap_status = (
        economic_gap.groupby(["proxy_evidence_available", "acceptance_requirement_met"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    top_markout = markout.sort_values("adverse_selection_rate_6bar_proxy", ascending=True)
    lifecycle_overview = (
        lifecycle_risk.groupby("fill_model", sort=True)
        .agg(
            strategy_profiles=("strategy_id", "size"),
            orders=("orders", "sum"),
            mean_fill_ratio=("mean_fill_ratio", "mean"),
            risk_adjusted_net_pnl_inr=("risk_adjusted_net_pnl_inr", "sum"),
            daily_halt_rows=("daily_halt_rows", "sum"),
            position_limit_breach_rows=("position_limit_breach_rows", "sum"),
        )
        .reset_index()
    )
    robustness_status = robustness_dimension["dimension_status"].value_counts().rename_axis("dimension_status").reset_index(name="strategies")
    robustness_gap_status = robustness_gap["acceptance_requirement_met"].value_counts().rename_axis("acceptance_requirement_met").reset_index(name="rows")
    risk_acceptance_status = (
        risk_acceptance_readiness.groupby(["proxy_evidence_available", "acceptance_requirement_met"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    hardening_priority = hardening_queue["priority_band"].value_counts().rename_axis("priority_band").reset_index(name="queue_items").sort_values("priority_band")
    execution_milestone_status = (
        execution_roadmap.groupby(["execution_milestone", "dependency_status"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    risk_hardening_status = (
        risk_hardening_plan.groupby(["risk_hardening_status", "proxy_evidence_available", "acceptance_requirement_met"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    economic_hardening_status = (
        economic_hardening_plan.groupby(["economic_hardening_status", "proxy_evidence_available", "acceptance_requirement_met"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    predictive_hardening_status = (
        predictive_hardening_plan.groupby(["predictive_hardening_status", "proxy_evidence_available", "acceptance_requirement_met"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    robustness_hardening_status = (
        robustness_hardening_plan.groupby(["robustness_hardening_status", "proxy_evidence_available", "acceptance_requirement_met"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    realism_hardening_status = (
        realism_hardening_plan.groupby(["realism_hardening_status", "proxy_evidence_available", "acceptance_requirement_met"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    broker_external_status = (
        broker_external_gap_ledger.groupby(["broker_evidence_status", "gate_id"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    strategy_support_status = (
        strategy_support_ledger.groupby(["support_contract_status", "gate_id"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    predictive_validation_status = (
        predictive_validation_ledger.groupby(["predictive_contract_status"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    robustness_execution_status = (
        robustness_execution_ledger.groupby(["robustness_execution_status"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    lifecycle_economic_status = (
        lifecycle_economic_ledger.groupby(["lifecycle_economic_status"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    realism_rerun_status = (
        realism_rerun_ledger.groupby(["realism_rerun_status"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    real_multiday_status = (
        real_multiday_ledger.groupby(["real_multiday_acceptance_status"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    stage_a2_status = (
        stage_a2_ledger.groupby(["capture_contract_status"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    stage_b1_check_status = (
        stage_b1_check_ledger.groupby(["passed"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    stage_b2_check_status = (
        stage_b2_check_ledger.groupby(["passed"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    stage_c_check_status = (
        stage_c_check_ledger.groupby(["passed"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    stage_d_check_status = (
        stage_d_check_ledger.groupby(["passed"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    stage_e_status = (
        stage_e_prerequisite_ledger.groupby(["passes"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase21_decision_status = (
        phase21_decision_ledger.groupby(["decision_status"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase22_milestone_status = (
        phase22_milestone_catalog.groupby(["current_status"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase22_task_status = (
        phase22_recalibration_task_ledger.groupby(["current_status"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase23_risk_status = (
        phase23_risk_register.groupby(["severity", "current_status"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase23_mitigation_status = (
        phase23_mitigation_ledger.groupby(["mitigation_status"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase25_profile_status = (
        phase25_replay_summary.groupby(["model_type", "execution_profile"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase25_risk_status = (
        phase25_risk_summary.groupby(["risk_status"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase26_profile_status = (
        phase26_candidate_summary.groupby(["execution_profile", "positive_after_costs", "salvage_candidate_proxy"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase26_rejection_status = (
        phase26_rejection_ledger.groupby(["salvage_candidate_proxy"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase27_profile_status = (
        phase27_candidate_summary.groupby(["execution_profile", "positive_after_costs", "realistic_cost_clearing_edge"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase27_rejection_status = (
        phase27_rejection_ledger.groupby(["realistic_cost_clearing_edge"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase28_support_status = (
        phase28_strategy_support_summary.groupby(["support_upgrade_status", "acceptance_ready"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase29_profile_status = (
        phase29_candidate_summary.groupby(["execution_profile", "positive_after_costs", "partial_proxy_candidate"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase29_risk_status = (
        phase29_risk_summary.groupby(["risk_status"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase30_decision_status = (
        phase30_decision_ledger.groupby(["current_decision", "promotion_ready", "acceptance_ready"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase30_redesign_priority = (
        phase30_redesign_queue.groupby(["redesign_priority"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase31_contract_status = (
        phase31_replay_gate.groupby(["redesign_contract_status", "replay_expansion_allowed"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase31_evidence_domain_status = (
        phase31_contract_ledger.groupby(["evidence_domain", "current_evidence_status", "acceptance_requirement_met"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase32_scanner_status = (
        phase32_scan_ledger.groupby(["scanner_evidence_status", "scanner_acceptance_requirement_met"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase33_file_status = (
        phase33_file_validation.groupby(["schema_validation_status", "acceptance_import_ready"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase33_test_status = (
        phase33_test_readiness.groupby(["current_status", "test_import_ready"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase34_day_status = (
        phase34_day_inventory.groupby(["day_status", "class_b_event_grade_day"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    phase34_symbol_status = (
        phase34_symbol_day_coverage.groupby(["raw_file_coverage_status", "phase1_delta_available", "class_b_event_grade_now"], sort=True)
        .size()
        .reset_index(name="rows")
    )
    top_risk_severity = lifecycle_risk_severity.sort_values("risk_severity_score", ascending=False)
    top_risk_limit_sensitivity = lifecycle_risk_limit_sensitivity.sort_values("risk_limit_severity_score", ascending=False)

    summary_rows = [
        ("quality_checks", int(len(quality)), "Phase 14 quality rows"),
        ("quality_warn_checks", int((quality["status"].astype(str) == "warn").sum()), "Current quality warnings"),
        ("quality_fail_checks", int((quality["status"].astype(str) == "fail").sum()), "Current quality failures"),
        ("holdout_proxy_rows", int(len(holdout)), "Phase 14 holdout generator proxy rows"),
        ("holdout_proxy_available_rows", int((holdout["realism_status"].astype(str) == "holdout_proxy_available_not_acceptance").sum()), "Holdout proxy rows structurally available"),
        ("realism_acceptance_gap_rows", int(len(realism_gap)), "Phase 14 realism acceptance gap rows"),
        ("realism_acceptance_gap_open_rows", int((~realism_gap["acceptance_requirement_met"].astype(bool)).sum()), "Phase 14 open realism acceptance gaps"),
        ("realism_acceptance_gap_proxy_rows", int(realism_gap["proxy_evidence_available"].astype(bool).sum()), "Phase 14 realism gaps with proxy evidence"),
        ("realism_acceptance_gap_met_rows", int(realism_gap["acceptance_requirement_met"].astype(bool).sum()), "Phase 14 met realism acceptance requirements"),
        ("full_run_lifecycle_risk_rows", int(len(lifecycle_risk)), "Phase 12 full-run fill-adjusted risk rows"),
        ("full_run_lifecycle_fill_models", int(lifecycle_risk["fill_model"].nunique()), "Phase 12 full-run fill models"),
        ("full_run_lifecycle_daily_halt_rows", int(lifecycle_risk["daily_halt_rows"].sum()), "Phase 12 full-run lifecycle halt rows"),
        ("full_run_lifecycle_breach_severity_rows", int(len(lifecycle_risk_severity)), "Phase 12 full-run lifecycle breach-severity rows"),
        ("full_run_lifecycle_risk_pass_candidate_rows", int(lifecycle_risk_severity["risk_pass_candidate_proxy"].astype(bool).sum()), "Phase 12 proxy risk-pass candidate rows"),
        ("full_run_lifecycle_high_severity_rows", int((lifecycle_risk_severity["risk_severity_band"].astype(str) == "high_proxy_breach_severity").sum()), "Phase 12 high-severity proxy risk rows"),
        ("full_run_lifecycle_risk_limit_sensitivity_rows", int(len(lifecycle_risk_limit_sensitivity)), "Phase 12 risk-limit sensitivity rows"),
        ("full_run_lifecycle_risk_limit_profiles", int(lifecycle_risk_limit_sensitivity["risk_limit_profile"].nunique()), "Phase 12 risk-limit sensitivity profiles"),
        ("full_run_lifecycle_risk_limit_pass_rows", int(lifecycle_risk_limit_sensitivity["risk_pass_candidate_under_limit_profile"].astype(bool).sum()), "Phase 12 proxy pass rows under sensitivity profiles"),
        ("full_run_lifecycle_risk_limit_high_rows", int((lifecycle_risk_limit_sensitivity["risk_limit_status"].astype(str) == "high_proxy_breach_under_limit_profile").sum()), "Phase 12 high-severity risk-limit rows"),
        ("full_run_risk_acceptance_readiness_rows", int(len(risk_acceptance_readiness)), "Phase 12 risk acceptance readiness rows"),
        ("full_run_risk_acceptance_readiness_open_rows", int((~risk_acceptance_readiness["acceptance_requirement_met"].astype(bool)).sum()), "Phase 12 open risk acceptance requirements"),
        ("full_run_risk_acceptance_readiness_proxy_rows", int(risk_acceptance_readiness["proxy_evidence_available"].astype(bool).sum()), "Phase 12 risk readiness rows with proxy evidence"),
        ("full_run_risk_acceptance_readiness_met_rows", int(risk_acceptance_readiness["acceptance_requirement_met"].astype(bool).sum()), "Phase 12 met risk acceptance requirements"),
        ("robustness_dimension_rows", int(len(robustness_dimension)), "Phase 13 robustness dimension rows"),
        ("robustness_dimension_registered_rows", int(robustness_dimension["registered_for_phase13_proxy"].astype(bool).sum()), "Phase 13 registered robustness proxy rows"),
        ("robustness_acceptance_gap_rows", int(len(robustness_gap)), "Phase 13 robustness acceptance gap rows"),
        ("robustness_acceptance_gap_open_rows", int((~robustness_gap["acceptance_requirement_met"].astype(bool)).sum()), "Phase 13 open robustness acceptance gaps"),
        ("robustness_acceptance_gap_met_rows", int(robustness_gap["acceptance_requirement_met"].astype(bool).sum()), "Phase 13 met robustness proxy requirements"),
        ("strategies", int(acceptance["strategy_id"].nunique()), "Phase 15 strategies"),
        ("promoted_strategies", int(acceptance["promotion_allowed"].astype(bool).sum()), "Promotion allowed count"),
        ("acceptance_blockers", int(len(blockers)), "Phase 15 blocker rows"),
        ("metric_catalog_rows", int(len(metric_catalog)), "Phase 16 metric catalog rows"),
        ("predictive_holdout_summary_rows", int(len(predictive_holdout)), "Phase 16 predictive holdout stability summary rows"),
        ("predictive_holdout_all_cell_pass_rows", int((predictive_holdout["worst_segment_status"].astype(str) == "all_cells_beat_local_majority_proxy").sum()), "Predictive holdout all-cell pass rows"),
        ("predictive_promotion_falsification_rows", int(len(predictive_falsification)), "Phase 16 predictive promotion falsification rows"),
        ("predictive_promotion_candidate_proxy_rows", int(predictive_falsification["predictive_promotion_candidate_proxy"].astype(bool).sum()), "Predictive proxy promotion candidates"),
        ("predictive_promotion_falsified_rows", int((predictive_falsification["falsification_status"].astype(str) == "falsified_for_predictive_promotion_under_current_proxy_evidence").sum()), "Predictive rows falsified for proxy promotion"),
        ("predictive_acceptance_gap_rows", int(len(predictive_gap)), "Phase 16 predictive acceptance gap rows"),
        ("predictive_acceptance_gap_open_rows", int((~predictive_gap["acceptance_requirement_met"].astype(bool)).sum()), "Phase 16 open predictive acceptance gaps"),
        ("predictive_acceptance_gap_proxy_rows", int(predictive_gap["proxy_evidence_available"].astype(bool).sum()), "Phase 16 predictive gaps with proxy evidence"),
        ("predictive_acceptance_gap_met_rows", int(predictive_gap["acceptance_requirement_met"].astype(bool).sum()), "Phase 16 met predictive acceptance requirements"),
        ("economic_viability_rows", int(len(economic)), "Phase 16 economic viability frontier rows"),
        ("economic_viability_net_positive_rows", int(economic["net_positive_proxy"].astype(bool).sum()), "Phase 16 net-positive proxy rows"),
        ("economic_viability_retail_stress_positive_rows", int((economic["net_positive_proxy"].astype(bool) & economic["retail_or_stress_profile"].astype(bool)).sum()), "Retail/stress net-positive proxy rows"),
        ("risk_adjusted_economic_rows", int(len(risk_adjusted_economic)), "Phase 16 risk-adjusted economic frontier rows"),
        ("risk_adjusted_economic_joint_pass_rows", int(risk_adjusted_economic["net_positive_and_risk_pass_proxy"].astype(bool).sum()), "Proxy rows with net-positive economics and risk-pass candidate"),
        ("risk_adjusted_economic_retail_stress_joint_pass_rows", int(risk_adjusted_economic["retail_stress_net_positive_and_risk_pass_proxy"].astype(bool).sum()), "Retail/stress proxy rows with net-positive economics and risk-pass candidate"),
        ("broker_reconciliation_readiness_rows", int(len(broker_reconciliation)), "Broker reconciliation readiness rows"),
        ("broker_reconciliation_proxy_formula_ready_rows", int(broker_reconciliation["proxy_formula_available_now"].astype(bool).sum()), "Readiness rows with documented/proxy formula evidence"),
        ("broker_reconciliation_contract_note_ready_rows", int(broker_reconciliation["broker_contract_note_available_now"].astype(bool).sum()), "Readiness rows with broker contract-note evidence"),
        ("economic_reconciliation_ready_strategies", int(economic_reconciliation["economic_acceptance_ready_now"].astype(bool).sum()), "Strategies economically ready after broker reconciliation"),
        ("economic_acceptance_gap_rows", int(len(economic_gap)), "Phase 16 economic acceptance gap rows"),
        ("economic_acceptance_gap_open_rows", int((~economic_gap["acceptance_requirement_met"].astype(bool)).sum()), "Phase 16 open economic acceptance gaps"),
        ("economic_acceptance_gap_proxy_rows", int(economic_gap["proxy_evidence_available"].astype(bool).sum()), "Phase 16 economic gaps with proxy evidence"),
        ("economic_acceptance_gap_met_rows", int(economic_gap["acceptance_requirement_met"].astype(bool).sum()), "Phase 16 met economic acceptance requirements"),
        ("acceptance_grade_metrics", int(metric_catalog["acceptance_eligible_now"].astype(bool).sum()), "Acceptance-grade metrics"),
        ("missing_metrics", int((metric_catalog["current_status"].astype(str) == "missing").sum()), "Missing metric rows"),
        ("p1_gaps", int((gaps["priority"].astype(str) == "P1").sum()), "Phase 17 P1 backlog rows"),
        ("phase20_hardening_queue_rows", int(len(hardening_queue)), "Phase 20 acceptance hardening queue rows"),
        ("phase20_hardening_gate_rows", int(len(hardening_gate_summary)), "Phase 20 gate hardening summary rows"),
        ("phase20_execution_roadmap_rows", int(len(execution_roadmap)), "Phase 20 cross-gate execution roadmap rows"),
        ("phase20_execution_milestone_rows", int(len(execution_milestones)), "Phase 20 execution milestone rows"),
        ("phase20_execution_roadmap_proxy_rows", int(execution_roadmap["proxy_evidence_available"].astype(bool).sum()), "Phase 20 roadmap rows with proxy evidence"),
        ("phase20_execution_roadmap_missing_rows", int((~execution_roadmap["proxy_evidence_available"].astype(bool)).sum()), "Phase 20 roadmap rows missing required evidence"),
        ("phase20_execution_roadmap_met_rows", int(execution_roadmap["acceptance_requirement_met"].astype(bool).sum()), "Phase 20 roadmap rows with met acceptance requirements"),
        ("phase20_risk_hardening_plan_rows", int(len(risk_hardening_plan)), "Phase 20 risk hardening requirement rows"),
        ("phase20_risk_hardening_proxy_rows", int(risk_hardening_plan["proxy_evidence_available"].astype(bool).sum()), "Phase 20 risk hardening rows with proxy evidence"),
        ("phase20_risk_hardening_missing_rows", int((~risk_hardening_plan["proxy_evidence_available"].astype(bool)).sum()), "Phase 20 risk hardening rows missing required evidence"),
        ("phase20_risk_hardening_met_rows", int(risk_hardening_plan["acceptance_requirement_met"].astype(bool).sum()), "Phase 20 met risk hardening requirements"),
        ("phase20_economic_hardening_plan_rows", int(len(economic_hardening_plan)), "Phase 20 economic hardening requirement rows"),
        ("phase20_economic_hardening_proxy_rows", int(economic_hardening_plan["proxy_evidence_available"].astype(bool).sum()), "Phase 20 economic hardening rows with proxy evidence"),
        ("phase20_economic_hardening_missing_rows", int((~economic_hardening_plan["proxy_evidence_available"].astype(bool)).sum()), "Phase 20 economic hardening rows missing required evidence"),
        ("phase20_economic_hardening_met_rows", int(economic_hardening_plan["acceptance_requirement_met"].astype(bool).sum()), "Phase 20 met economic hardening requirements"),
        ("phase20_predictive_hardening_plan_rows", int(len(predictive_hardening_plan)), "Phase 20 predictive hardening requirement rows"),
        ("phase20_predictive_hardening_proxy_rows", int(predictive_hardening_plan["proxy_evidence_available"].astype(bool).sum()), "Phase 20 predictive hardening rows with proxy evidence"),
        ("phase20_predictive_hardening_missing_rows", int((~predictive_hardening_plan["proxy_evidence_available"].astype(bool)).sum()), "Phase 20 predictive hardening rows missing required evidence"),
        ("phase20_predictive_hardening_met_rows", int(predictive_hardening_plan["acceptance_requirement_met"].astype(bool).sum()), "Phase 20 met predictive hardening requirements"),
        ("phase20_robustness_hardening_plan_rows", int(len(robustness_hardening_plan)), "Phase 20 robustness hardening requirement rows"),
        ("phase20_robustness_hardening_proxy_rows", int(robustness_hardening_plan["proxy_evidence_available"].astype(bool).sum()), "Phase 20 robustness hardening rows with proxy evidence"),
        ("phase20_robustness_hardening_missing_rows", int((~robustness_hardening_plan["proxy_evidence_available"].astype(bool)).sum()), "Phase 20 robustness hardening rows missing required evidence"),
        ("phase20_robustness_hardening_met_rows", int(robustness_hardening_plan["acceptance_requirement_met"].astype(bool).sum()), "Phase 20 met robustness hardening requirements"),
        ("phase20_realism_hardening_plan_rows", int(len(realism_hardening_plan)), "Phase 20 realism hardening requirement rows"),
        ("phase20_realism_hardening_proxy_rows", int(realism_hardening_plan["proxy_evidence_available"].astype(bool).sum()), "Phase 20 realism hardening rows with proxy evidence"),
        ("phase20_realism_hardening_missing_rows", int((~realism_hardening_plan["proxy_evidence_available"].astype(bool)).sum()), "Phase 20 realism hardening rows missing required evidence"),
        ("phase20_realism_hardening_met_rows", int(realism_hardening_plan["acceptance_requirement_met"].astype(bool).sum()), "Phase 20 met realism hardening requirements"),
        ("phase20_acceptance_ready_rows", int(hardening_queue["acceptance_ready_now"].astype(bool).sum()), "Phase 20 acceptance-ready queue rows"),
        ("phase20_m01_broker_required_external_files", int(len(broker_import_checklist)), "Phase 20 M01 required broker/external evidence files"),
        ("phase20_m01_broker_available_external_files", int(broker_import_checklist["file_exists_now"].astype(bool).sum()), "Phase 20 M01 broker/external files currently available"),
        ("phase20_m01_broker_schema_rows", int(len(broker_evidence_schema)), "Phase 20 M01 broker evidence schema rows"),
        ("phase20_m01_broker_external_gap_rows", int(len(broker_external_gap_ledger)), "Phase 20 M01 broker/external gap rows"),
        ("phase20_m01_broker_external_gap_acceptance_met_rows", int(broker_external_gap_ledger["acceptance_requirement_met_after_contract"].astype(bool).sum()), "Phase 20 M01 broker/external gap rows that meet acceptance after contract"),
        ("phase20_m02_strategy_support_closure_rows", int(len(strategy_support_ledger)), "Phase 20 M02 strategy support closure rows"),
        ("phase20_m02_strategy_support_feature_engineering_rows", int(strategy_support_ledger["feature_engineering_required"].astype(bool).sum()), "Phase 20 M02 rows requiring feature engineering"),
        ("phase20_m02_strategy_support_classification_rows", int(strategy_support_ledger["classification_required"].astype(bool).sum()), "Phase 20 M02 rows requiring explicit non-alpha classification"),
        ("phase20_m02_strategy_support_acceptance_upgrade_rows", int(strategy_support_ledger["acceptance_upgrade_required"].astype(bool).sum()), "Phase 20 M02 rows requiring proxy-to-acceptance upgrade"),
        ("phase20_m02_strategy_support_acceptance_met_rows", int(strategy_support_ledger["acceptance_requirement_met_after_contract"].astype(bool).sum()), "Phase 20 M02 rows that meet acceptance after contract"),
        ("phase20_m03_predictive_validation_rows", int(len(predictive_validation_ledger)), "Phase 20 M03 predictive validation rows"),
        ("phase20_m03_predictive_calibrated_model_required_rows", int(predictive_validation_ledger["calibrated_model_required"].astype(bool).sum()), "Phase 20 M03 rows requiring calibrated model output"),
        ("phase20_m03_predictive_baseline_lift_required_rows", int(predictive_validation_ledger["baseline_lift_required"].astype(bool).sum()), "Phase 20 M03 rows requiring baseline lift"),
        ("phase20_m03_predictive_holdout_or_untouched_required_rows", int(predictive_validation_ledger["holdout_or_untouched_required"].astype(bool).sum()), "Phase 20 M03 rows requiring holdout or untouched-test evidence"),
        ("phase20_m03_predictive_promotion_falsification_required_rows", int(predictive_validation_ledger["promotion_falsification_required"].astype(bool).sum()), "Phase 20 M03 rows requiring promotion-falsification clearance"),
        ("phase20_m03_predictive_acceptance_met_rows", int(predictive_validation_ledger["acceptance_requirement_met_after_contract"].astype(bool).sum()), "Phase 20 M03 rows that meet acceptance after contract"),
        ("phase20_m04_robustness_execution_rows", int(len(robustness_execution_ledger)), "Phase 20 M04 robustness execution rows"),
        ("phase20_m04_full_seed_required_rows", int(robustness_execution_ledger["full_seed_execution_required"].astype(bool).sum()), "Phase 20 M04 rows requiring full seed execution"),
        ("phase20_m04_walk_forward_required_rows", int(robustness_execution_ledger["walk_forward_execution_required"].astype(bool).sum()), "Phase 20 M04 rows requiring walk-forward execution"),
        ("phase20_m04_parameter_smoothness_required_rows", int(robustness_execution_ledger["parameter_smoothness_required"].astype(bool).sum()), "Phase 20 M04 rows requiring parameter-neighborhood smoothness"),
        ("phase20_m04_execution_profile_required_rows", int(robustness_execution_ledger["execution_profile_required"].astype(bool).sum()), "Phase 20 M04 rows requiring execution-profile robustness"),
        ("phase20_m04_negative_control_required_rows", int(robustness_execution_ledger["negative_control_required"].astype(bool).sum()), "Phase 20 M04 rows requiring negative-control rejection"),
        ("phase20_m04_robustness_acceptance_met_rows", int(robustness_execution_ledger["acceptance_requirement_met_after_contract"].astype(bool).sum()), "Phase 20 M04 rows that meet acceptance after contract"),
        ("phase20_m05_lifecycle_economic_rows", int(len(lifecycle_economic_ledger)), "Phase 20 M05 lifecycle/economic replay rows"),
        ("phase20_m05_risk_replay_required_rows", int(lifecycle_economic_ledger["risk_replay_required"].astype(bool).sum()), "Phase 20 M05 rows requiring lifecycle risk replay"),
        ("phase20_m05_economic_replay_required_rows", int(lifecycle_economic_ledger["economic_replay_required"].astype(bool).sum()), "Phase 20 M05 rows requiring economic replay"),
        ("phase20_m05_broker_reconciliation_required_rows", int(lifecycle_economic_ledger["broker_reconciliation_required"].astype(bool).sum()), "Phase 20 M05 rows requiring broker/contract-note reconciliation"),
        ("phase20_m05_guardrail_validation_required_rows", int(lifecycle_economic_ledger["guardrail_validation_required"].astype(bool).sum()), "Phase 20 M05 rows requiring guardrail validation"),
        ("phase20_m05_lifecycle_economic_acceptance_met_rows", int(lifecycle_economic_ledger["acceptance_requirement_met_after_contract"].astype(bool).sum()), "Phase 20 M05 rows that meet acceptance after contract"),
        ("phase20_m06_realism_rerun_rows", int(len(realism_rerun_ledger)), "Phase 20 M06 holdout/realism rerun rows"),
        ("phase20_m06_holdout_rerun_required_rows", int(realism_rerun_ledger["holdout_rerun_required"].astype(bool).sum()), "Phase 20 M06 rows requiring holdout strategy reruns"),
        ("phase20_m06_quality_gate_required_rows", int(realism_rerun_ledger["quality_gate_required"].astype(bool).sum()), "Phase 20 M06 rows requiring quality-gate clearance"),
        ("phase20_m06_feed_imperfection_required_rows", int(realism_rerun_ledger["feed_imperfection_required"].astype(bool).sum()), "Phase 20 M06 rows requiring feed-imperfection reruns"),
        ("phase20_m06_pessimistic_execution_required_rows", int(realism_rerun_ledger["pessimistic_execution_required"].astype(bool).sum()), "Phase 20 M06 rows requiring pessimistic execution realism"),
        ("phase20_m06_artifact_control_required_rows", int(realism_rerun_ledger["artifact_control_required"].astype(bool).sum()), "Phase 20 M06 rows requiring artifact-exploitation controls"),
        ("phase20_m06_realism_acceptance_met_rows", int(realism_rerun_ledger["acceptance_requirement_met_after_contract"].astype(bool).sum()), "Phase 20 M06 rows that meet acceptance after contract"),
        ("phase20_m07_real_multiday_rows", int(len(real_multiday_ledger)), "Phase 20 M07 real multi-day acceptance rows"),
        ("phase20_m07_economic_real_validation_required_rows", int(real_multiday_ledger["economic_real_validation_required"].astype(bool).sum()), "Phase 20 M07 rows requiring real economic validation"),
        ("phase20_m07_predictive_real_holdout_required_rows", int(real_multiday_ledger["predictive_real_holdout_required"].astype(bool).sum()), "Phase 20 M07 rows requiring real predictive holdout"),
        ("phase20_m07_robustness_real_rerun_required_rows", int(real_multiday_ledger["robustness_real_rerun_required"].astype(bool).sum()), "Phase 20 M07 rows requiring real robustness rerun"),
        ("phase20_m07_realism_real_validation_required_rows", int(real_multiday_ledger["realism_real_validation_required"].astype(bool).sum()), "Phase 20 M07 rows requiring real realism validation"),
        ("phase20_m07_real_multiday_acceptance_met_rows", int(real_multiday_ledger["acceptance_requirement_met_after_contract"].astype(bool).sum()), "Phase 20 M07 rows that meet acceptance after contract"),
        ("stage_a2_capture_diagnostics_rows", int(len(stage_a2_ledger)), "Stage A2 capture diagnostics contract rows"),
        ("stage_a2_required_capture_schema_rows", int(len(stage_a2_schema)), "Stage A2 required capture schema rows"),
        ("stage_a2_symbols_evaluated", int(stage_a2_ledger["symbol"].nunique()), "Stage A2 symbols evaluated from current one-day sample"),
        ("stage_a2_current_sample_days_available", int(stage_a2_readiness_summary["current_sample_days_available"].iloc[0]), "Stage A2 current real sample days available"),
        ("stage_a2_open_contract_rows", int((~stage_a2_ledger["acceptance_requirement_met_after_contract"].astype(bool)).sum()), "Stage A2 open capture contract rows"),
        ("stage_a2_acceptance_met_rows", int(stage_a2_ledger["acceptance_requirement_met_after_contract"].astype(bool).sum()), "Stage A2 capture contract rows that meet acceptance"),
        ("stage_b1_development_symbols", int(len(stage_b1_subset)), "Stage B1 development subset symbols"),
        ("stage_b1_etf_symbols", int((stage_b1_subset["instrument_class"].astype(str) == "etf").sum()), "Stage B1 ETF symbols in development subset"),
        ("stage_b1_scenario_coverage_rows", int(len(stage_b1_scenario_summary)), "Stage B1 scenario coverage rows"),
        ("stage_b1_structural_check_rows", int(len(stage_b1_check_ledger)), "Stage B1 structural check rows"),
        ("stage_b1_structural_checks_passed", int(stage_b1_check_ledger["passed"].astype(bool).sum()), "Stage B1 passed structural checks"),
        ("stage_b1_structural_checks_failed", int((~stage_b1_check_ledger["passed"].astype(bool)).sum()), "Stage B1 failed structural checks"),
        ("stage_b2_development_symbols", int(len(stage_b2_readiness)), "Stage B2 development subset symbols"),
        ("stage_b2_event_driven_1s_ready_symbols", int(stage_b2_readiness["event_driven_1s_ready"].astype(bool).sum()), "Stage B2 event-driven 1s-ready development symbols"),
        ("stage_b2_selected_scenario_days", int(stage_b2_dataset_summary.loc[stage_b2_dataset_summary["metric"].eq("selected_scenario_days"), "value"].iloc[0]), "Stage B2 selected scenario days"),
        ("stage_b2_raw_event_rows", int(stage_b2_dataset_summary.loc[stage_b2_dataset_summary["metric"].eq("raw_event_rows"), "value"].iloc[0]), "Stage B2 raw event rows"),
        ("stage_b2_event_feature_rows", int(stage_b2_dataset_summary.loc[stage_b2_dataset_summary["metric"].eq("event_feature_rows"), "value"].iloc[0]), "Stage B2 event-driven feature rows"),
        ("stage_b2_one_second_event_feature_rows", int(stage_b2_dataset_summary.loc[stage_b2_dataset_summary["metric"].eq("one_second_event_feature_rows"), "value"].iloc[0]), "Stage B2 event-driven 1s proof rows"),
        ("stage_b2_proof_check_rows", int(len(stage_b2_check_ledger)), "Stage B2 proof check rows"),
        ("stage_b2_proof_checks_passed", int(stage_b2_check_ledger["passed"].astype(bool).sum()), "Stage B2 passed proof checks"),
        ("stage_b2_proof_checks_failed", int((~stage_b2_check_ledger["passed"].astype(bool)).sum()), "Stage B2 failed proof checks"),
        ("stage_c_symbols", int(stage_c_dataset_summary.loc[stage_c_dataset_summary["metric"].eq("symbols"), "value"].iloc[0]), "Stage C pilot symbols"),
        ("stage_c_selected_trading_days", int(stage_c_dataset_summary.loc[stage_c_dataset_summary["metric"].eq("selected_trading_days"), "value"].iloc[0]), "Stage C selected trading days"),
        ("stage_c_selected_seed_rows", int(stage_c_dataset_summary.loc[stage_c_dataset_summary["metric"].eq("selected_seed_rows"), "value"].iloc[0]), "Stage C selected seed rows"),
        ("stage_c_feature_rows", int(stage_c_dataset_summary.loc[stage_c_dataset_summary["metric"].eq("feature_rows"), "value"].iloc[0]), "Stage C pilot feature rows"),
        ("stage_c_strategy_run_rows", int(len(stage_c_strategy_runs)), "Stage C S01-S05 strategy proxy run rows"),
        ("stage_c_baseline_run_rows", int(len(stage_c_baseline_runs)), "Stage C baseline proxy run rows"),
        ("stage_c_check_rows", int(len(stage_c_check_ledger)), "Stage C check rows"),
        ("stage_c_checks_passed", int(stage_c_check_ledger["passed"].astype(bool).sum()), "Stage C passed checks"),
        ("stage_c_checks_failed", int((~stage_c_check_ledger["passed"].astype(bool)).sum()), "Stage C failed checks"),
        ("stage_d_symbols", int(stage_d_dataset_summary.loc[stage_d_dataset_summary["metric"].eq("symbols"), "value"].iloc[0]), "Stage D symbols"),
        ("stage_d_quarter_profiles", int(stage_d_dataset_summary.loc[stage_d_dataset_summary["metric"].eq("quarter_profiles"), "value"].iloc[0]), "Stage D quarter profiles"),
        ("stage_d_min_days_per_profile", int(stage_d_dataset_summary.loc[stage_d_dataset_summary["metric"].eq("min_days_per_profile"), "value"].iloc[0]), "Stage D minimum days per profile"),
        ("stage_d_feature_rows", int(stage_d_dataset_summary.loc[stage_d_dataset_summary["metric"].eq("feature_rows"), "value"].iloc[0]), "Stage D feature rows"),
        ("stage_d_strategy_run_rows", int(len(stage_d_strategy_summary)), "Stage D S01-S11 strategy/control proxy rows"),
        ("stage_d_control_strategy_rows", int(stage_d_strategy_summary["control_or_risk_module"].astype(bool).sum()), "Stage D S09-S11 control/risk rows"),
        ("stage_d_check_rows", int(len(stage_d_check_ledger)), "Stage D check rows"),
        ("stage_d_checks_passed", int(stage_d_check_ledger["passed"].astype(bool).sum()), "Stage D passed checks"),
        ("stage_d_checks_failed", int((~stage_d_check_ledger["passed"].astype(bool)).sum()), "Stage D failed checks"),
        ("stage_e_prerequisite_rows", int(len(stage_e_prerequisite_ledger)), "Stage E prerequisite rows"),
        ("stage_e_passing_prerequisites", int(stage_e_prerequisite_ledger["passes"].astype(bool).sum()), "Stage E passing prerequisites"),
        ("stage_e_blocking_prerequisites", int((~stage_e_prerequisite_ledger["passes"].astype(bool)).sum()), "Stage E blocking prerequisites"),
        ("stage_e_extension_allowed_rows", int(stage_e_prerequisite_ledger.loc[stage_e_prerequisite_ledger["prerequisite_id"].eq("full_year_extension_allowed"), "passes"].astype(bool).sum()), "Stage E extension allowed rows"),
        ("phase21_decision_rules", int(len(phase21_decision_rules)), "Phase 21 decision rules"),
        ("phase21_active_current_decisions", int((phase21_decision_ledger["decision_status"].astype(str) == "active_current_decision").sum()), "Phase 21 active current decisions"),
        ("phase21_extension_or_paper_ready", int(phase21_decision_summary.loc[phase21_decision_summary["metric"].eq("extension_or_paper_ready"), "value"].iloc[0]), "Phase 21 extension/paper-ready rows"),
        ("phase22_class_b_event_grade_days", int(phase22_summary.loc[phase22_summary["metric"].eq("class_b_event_grade_days"), "value"].iloc[0]), "Phase 22 complete Class B event-grade days"),
        ("phase22_recalibration_tasks", int(len(phase22_recalibration_task_ledger)), "Phase 22 milestone/domain recalibration tasks"),
        ("phase22_ready_recalibration_tasks", int(phase22_summary.loc[phase22_summary["metric"].eq("ready_recalibration_tasks"), "value"].iloc[0]), "Phase 22 tasks ready for event-flow recalibration"),
        ("phase22_extension_or_paper_ready", int(phase22_summary.loc[phase22_summary["metric"].eq("phase22_extension_or_paper_ready"), "value"].iloc[0]), "Phase 22 extension/paper-ready rows"),
        ("phase23_key_risks", int(len(phase23_risk_register)), "Phase 23 key risk rows"),
        ("phase23_open_acceptance_blocking_risks", int(phase23_summary.loc[phase23_summary["metric"].eq("phase23_open_acceptance_blocking_risks"), "value"].iloc[0]), "Phase 23 open acceptance-blocking risks"),
        ("phase23_mitigation_rows", int(len(phase23_mitigation_ledger)), "Phase 23 mitigation rows"),
        ("phase23_promotion_ready", int(phase23_summary.loc[phase23_summary["metric"].eq("phase23_promotion_ready"), "value"].iloc[0]), "Phase 23 promotion-ready rows"),
        ("phase25_models_replayed", int(phase25_overall_summary.loc[phase25_overall_summary["metric"].eq("phase25_models_replayed"), "value"].iloc[0]), "Phase 25 strategies/baselines replayed"),
        ("phase25_total_trades", int(phase25_overall_summary.loc[phase25_overall_summary["metric"].eq("phase25_total_trades"), "value"].iloc[0]), "Phase 25 event-order replay trades"),
        ("phase25_positive_strategy_profile_rows", int(phase25_overall_summary.loc[phase25_overall_summary["metric"].eq("phase25_positive_strategy_profile_rows"), "value"].iloc[0]), "Phase 25 positive strategy/profile rows"),
        ("phase25_beats_best_baseline_rows", int(phase25_overall_summary.loc[phase25_overall_summary["metric"].eq("phase25_beats_best_baseline_rows"), "value"].iloc[0]), "Phase 25 strategy/profile rows beating best baseline"),
        ("phase25_acceptance_ready", int(phase25_overall_summary.loc[phase25_overall_summary["metric"].eq("phase25_acceptance_ready"), "value"].iloc[0]), "Phase 25 acceptance-ready rows"),
        ("phase26_variants_registered", int(phase26_overall_summary.loc[phase26_overall_summary["metric"].eq("phase26_variants_registered"), "value"].iloc[0]), "Phase 26 parameter/filter variants registered"),
        ("phase26_total_replay_trades", int(phase26_overall_summary.loc[phase26_overall_summary["metric"].eq("phase26_total_replay_trades"), "value"].iloc[0]), "Phase 26 strategy-salvage replay trades"),
        ("phase26_realistic_positive_after_cost_rows", int(phase26_overall_summary.loc[phase26_overall_summary["metric"].eq("phase26_realistic_positive_after_cost_rows"), "value"].iloc[0]), "Phase 26 retail/stressed positive rows after costs"),
        ("phase26_zero_latency_positive_control_rows", int(phase26_overall_summary.loc[phase26_overall_summary["metric"].eq("phase26_zero_latency_positive_control_rows"), "value"].iloc[0]), "Phase 26 frictionless positive control rows"),
        ("phase26_salvage_candidate_rows", int(phase26_overall_summary.loc[phase26_overall_summary["metric"].eq("phase26_salvage_candidate_rows"), "value"].iloc[0]), "Phase 26 realistic salvage candidate rows"),
        ("phase26_acceptance_ready", int(phase26_overall_summary.loc[phase26_overall_summary["metric"].eq("phase26_acceptance_ready"), "value"].iloc[0]), "Phase 26 acceptance-ready rows"),
        ("phase27_feature_candidates_registered", int(phase27_overall_summary.loc[phase27_overall_summary["metric"].eq("phase27_feature_candidates_registered"), "value"].iloc[0]), "Phase 27 feature/horizon/threshold candidates"),
        ("phase27_total_replay_trades", int(phase27_overall_summary.loc[phase27_overall_summary["metric"].eq("phase27_total_replay_trades"), "value"].iloc[0]), "Phase 27 feature-edge replay trades"),
        ("phase27_positive_after_cost_rows", int(phase27_overall_summary.loc[phase27_overall_summary["metric"].eq("phase27_positive_after_cost_rows"), "value"].iloc[0]), "Phase 27 positive rows after costs"),
        ("phase27_realistic_cost_clearing_rows", int(phase27_overall_summary.loc[phase27_overall_summary["metric"].eq("phase27_realistic_cost_clearing_rows"), "value"].iloc[0]), "Phase 27 realistic cost-clearing feature rows"),
        ("phase27_zero_latency_edge_control_rows", int(phase27_overall_summary.loc[phase27_overall_summary["metric"].eq("phase27_zero_latency_edge_control_rows"), "value"].iloc[0]), "Phase 27 zero-latency positive feature controls"),
        ("phase27_acceptance_ready", int(phase27_overall_summary.loc[phase27_overall_summary["metric"].eq("phase27_acceptance_ready"), "value"].iloc[0]), "Phase 27 acceptance-ready rows"),
        ("phase28_received_delta_rows", int(phase28_overall_summary.loc[phase28_overall_summary["metric"].eq("phase28_received_delta_rows"), "value"].iloc[0]), "Phase 28 received tick-delta rows scanned"),
        ("phase28_symbols_evaluated", int(phase28_overall_summary.loc[phase28_overall_summary["metric"].eq("phase28_symbols_evaluated"), "value"].iloc[0]), "Phase 28 symbols evaluated"),
        ("phase28_proxy_feature_engineered_families", int(phase28_overall_summary.loc[phase28_overall_summary["metric"].eq("phase28_proxy_feature_engineered_families"), "value"].iloc[0]), "Phase 28 partial families with proxy labels"),
        ("phase28_total_proxy_label_rows", int(phase28_overall_summary.loc[phase28_overall_summary["metric"].eq("phase28_total_proxy_label_rows"), "value"].iloc[0]), "Phase 28 proxy label rows/buckets"),
        ("phase28_acceptance_ready", int(phase28_overall_summary.loc[phase28_overall_summary["metric"].eq("phase28_acceptance_ready"), "value"].iloc[0]), "Phase 28 acceptance-ready rows"),
        ("phase29_partial_strategies_replayed", int(phase29_overall_summary.loc[phase29_overall_summary["metric"].eq("phase29_partial_strategies_replayed"), "value"].iloc[0]), "Phase 29 partial strategies replayed"),
        ("phase29_total_replay_trades", int(phase29_overall_summary.loc[phase29_overall_summary["metric"].eq("phase29_total_replay_trades"), "value"].iloc[0]), "Phase 29 partial-strategy replay trades"),
        ("phase29_positive_after_cost_rows", int(phase29_overall_summary.loc[phase29_overall_summary["metric"].eq("phase29_positive_after_cost_rows"), "value"].iloc[0]), "Phase 29 positive rows after costs"),
        ("phase29_realistic_positive_rows", int(phase29_overall_summary.loc[phase29_overall_summary["metric"].eq("phase29_realistic_positive_rows"), "value"].iloc[0]), "Phase 29 retail/stressed positive rows"),
        ("phase29_proxy_candidate_rows", int(phase29_overall_summary.loc[phase29_overall_summary["metric"].eq("phase29_proxy_candidate_rows"), "value"].iloc[0]), "Phase 29 proxy candidate rows"),
        ("phase29_acceptance_ready", int(phase29_overall_summary.loc[phase29_overall_summary["metric"].eq("phase29_acceptance_ready"), "value"].iloc[0]), "Phase 29 acceptance-ready rows"),
        ("phase30_strategy_families_triaged", int(phase30_overall_summary.loc[phase30_overall_summary["metric"].eq("phase30_strategy_families_triaged"), "value"].iloc[0]), "Phase 30 strategy/control families triaged"),
        ("phase30_alpha_families_triaged", int(phase30_overall_summary.loc[phase30_overall_summary["metric"].eq("phase30_alpha_families_triaged"), "value"].iloc[0]), "Phase 30 alpha strategy families triaged"),
        ("phase30_reject_or_redesign_rows", int(phase30_overall_summary.loc[phase30_overall_summary["metric"].eq("phase30_reject_or_redesign_rows"), "value"].iloc[0]), "Phase 30 reject/redesign rows"),
        ("phase30_non_alpha_control_rows", int(phase30_overall_summary.loc[phase30_overall_summary["metric"].eq("phase30_non_alpha_control_rows"), "value"].iloc[0]), "Phase 30 non-alpha control rows"),
        ("phase30_promotion_ready_rows", int(phase30_overall_summary.loc[phase30_overall_summary["metric"].eq("phase30_promotion_ready_rows"), "value"].iloc[0]), "Phase 30 promotion-ready rows"),
        ("phase30_acceptance_ready_rows", int(phase30_overall_summary.loc[phase30_overall_summary["metric"].eq("phase30_acceptance_ready_rows"), "value"].iloc[0]), "Phase 30 acceptance-ready rows"),
        ("phase30_realistic_positive_execution_rows", int(phase30_overall_summary.loc[phase30_overall_summary["metric"].eq("phase30_realistic_positive_execution_rows"), "value"].iloc[0]), "Phase 30 realistic positive execution rows"),
        ("phase30_candidate_rows", int(phase30_overall_summary.loc[phase30_overall_summary["metric"].eq("phase30_candidate_rows"), "value"].iloc[0]), "Phase 30 candidate rows"),
        ("phase31_strategy_redesign_specs", int(phase31_overall_summary.loc[phase31_overall_summary["metric"].eq("phase31_strategy_redesign_specs"), "value"].iloc[0]), "Phase 31 strategy redesign specs"),
        ("phase31_contract_requirement_rows", int(phase31_overall_summary.loc[phase31_overall_summary["metric"].eq("phase31_contract_requirement_rows"), "value"].iloc[0]), "Phase 31 contract requirement rows"),
        ("phase31_open_contract_requirements", int(phase31_overall_summary.loc[phase31_overall_summary["metric"].eq("phase31_open_contract_requirements"), "value"].iloc[0]), "Phase 31 open contract requirements"),
        ("phase31_replay_allowed_rows", int(phase31_overall_summary.loc[phase31_overall_summary["metric"].eq("phase31_replay_allowed_rows"), "value"].iloc[0]), "Phase 31 replay-allowed rows"),
        ("phase31_replay_blocked_rows", int(phase31_overall_summary.loc[phase31_overall_summary["metric"].eq("phase31_replay_blocked_rows"), "value"].iloc[0]), "Phase 31 replay-blocked rows"),
        ("phase31_acceptance_ready_rows", int(phase31_overall_summary.loc[phase31_overall_summary["metric"].eq("phase31_acceptance_ready_rows"), "value"].iloc[0]), "Phase 31 acceptance-ready rows"),
        ("phase32_contract_rows_scanned", int(phase32_overall_summary.loc[phase32_overall_summary["metric"].eq("phase32_contract_rows_scanned"), "value"].iloc[0]), "Phase 32 contract rows scanned"),
        ("phase32_proxy_or_partial_available_rows", int(phase32_overall_summary.loc[phase32_overall_summary["metric"].eq("phase32_proxy_or_partial_available_rows"), "value"].iloc[0]), "Phase 32 proxy/partial available rows"),
        ("phase32_external_or_new_artifact_missing_rows", int(phase32_overall_summary.loc[phase32_overall_summary["metric"].eq("phase32_external_or_new_artifact_missing_rows"), "value"].iloc[0]), "Phase 32 external/new-artifact missing rows"),
        ("phase32_acceptance_met_rows", int(phase32_overall_summary.loc[phase32_overall_summary["metric"].eq("phase32_acceptance_met_rows"), "value"].iloc[0]), "Phase 32 acceptance-met rows"),
        ("phase32_replay_allowed_rows", int(phase32_overall_summary.loc[phase32_overall_summary["metric"].eq("phase32_replay_allowed_rows"), "value"].iloc[0]), "Phase 32 replay-allowed rows"),
        ("phase32_acquisition_queue_rows", int(phase32_overall_summary.loc[phase32_overall_summary["metric"].eq("phase32_acquisition_queue_rows"), "value"].iloc[0]), "Phase 32 evidence acquisition queue rows"),
        ("phase33_templates_generated", int(phase33_overall_summary.loc[phase33_overall_summary["metric"].eq("phase33_templates_generated"), "value"].iloc[0]), "Phase 33 broker evidence templates generated"),
        ("phase33_expected_external_files", int(phase33_overall_summary.loc[phase33_overall_summary["metric"].eq("phase33_expected_external_files"), "value"].iloc[0]), "Phase 33 expected external files"),
        ("phase33_external_files_present", int(phase33_overall_summary.loc[phase33_overall_summary["metric"].eq("phase33_external_files_present"), "value"].iloc[0]), "Phase 33 external files present"),
        ("phase33_acceptance_import_ready_files", int(phase33_overall_summary.loc[phase33_overall_summary["metric"].eq("phase33_acceptance_import_ready_files"), "value"].iloc[0]), "Phase 33 acceptance import-ready files"),
        ("phase33_missing_external_files", int(phase33_overall_summary.loc[phase33_overall_summary["metric"].eq("phase33_missing_external_files"), "value"].iloc[0]), "Phase 33 missing external files"),
        ("phase33_reconciliation_tests_ready", int(phase33_overall_summary.loc[phase33_overall_summary["metric"].eq("phase33_reconciliation_tests_ready"), "value"].iloc[0]), "Phase 33 reconciliation tests ready"),
        ("phase34_raw_trade_days_available", int(phase34_readiness_summary.loc[phase34_readiness_summary["metric"].eq("phase34_raw_trade_days_available"), "value"].iloc[0]), "Phase 34 raw trade days available"),
        ("phase34_full_universe_raw_days", int(phase34_readiness_summary.loc[phase34_readiness_summary["metric"].eq("phase34_full_universe_raw_days"), "value"].iloc[0]), "Phase 34 full-universe raw days"),
        ("phase34_class_b_event_grade_days", int(phase34_readiness_summary.loc[phase34_readiness_summary["metric"].eq("phase34_class_b_event_grade_days"), "value"].iloc[0]), "Phase 34 Class B event-grade days"),
        ("phase34_days_needed_for_min", int(phase34_readiness_summary.loc[phase34_readiness_summary["metric"].eq("phase34_days_needed_for_min"), "value"].iloc[0]), "Phase 34 additional Class B days needed for minimum"),
        ("phase34_days_needed_for_target", int(phase34_readiness_summary.loc[phase34_readiness_summary["metric"].eq("phase34_days_needed_for_target"), "value"].iloc[0]), "Phase 34 additional Class B days needed for target"),
        ("phase34_stage_a2_open_contract_rows", int(phase34_readiness_summary.loc[phase34_readiness_summary["metric"].eq("phase34_stage_a2_open_contract_rows"), "value"].iloc[0]), "Phase 34 Stage A2 open contract rows"),
        ("phase34_replay_allowed_rows", int(phase34_readiness_summary.loc[phase34_readiness_summary["metric"].eq("phase34_replay_allowed_rows"), "value"].iloc[0]), "Phase 34 replay-allowed rows"),
    ]
    summary = pd.DataFrame(summary_rows, columns=["metric", "value", "note"])
    inputs_manifest = {key: str(value) for key, value in paths.items()}
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "inputs": inputs_manifest,
        "summary": {row["metric"]: int(row["value"]) for row in summary.to_dict("records")},
        "scope": "static_validation_dashboard_not_promotion_evidence",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="dashboard",
            generated_utc=generated_utc,
            inputs=inputs_manifest,
            parameters={"scope": manifest["scope"], "summary_metrics": list(summary["metric"])},
            outputs={
                "html": "outputs/dashboard/synthetic_l2_validation_dashboard.html",
                "markdown": "outputs/dashboard/synthetic_l2_validation_dashboard.md",
                "summary": "outputs/dashboard/validation_dashboard_summary.csv",
                "manifest": "outputs/dashboard/validation_dashboard_manifest.json",
            },
            random_seed="not_applicable_deterministic_static_dashboard",
            scenario_ids="current_workspace_phase14_phase15_phase16_phase17_phase20_phase20_m01_stage_a_to_e_phase21_phase22_phase23_phase25_phase26_phase27_phase28_phase29_phase30_phase31_phase32_phase33_phase34_evidence",
            cost_model_version="outputs/phase12/cost_schedule.csv_and_zerodha_order_formula_v2_or_not_applicable",
            latency_model_version="outputs/phase12/execution_profiles.csv_or_phase8_feed_profiles_v1_or_not_applicable",
        )
    )

    cards = "".join(_metric_card(row["metric"], row["value"], row["note"]) for row in summary.to_dict("records"))
    css = """
    body { font-family: Inter, Segoe UI, Arial, sans-serif; margin: 24px; color: #172033; background: #f7f8fb; }
    h1, h2 { color: #111827; }
    .muted { color: #6b7280; }
    .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 12px; margin: 18px 0; }
    .card { background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 14px; box-shadow: 0 1px 2px rgba(0,0,0,0.04); }
    .card-label { color: #6b7280; font-size: 12px; text-transform: uppercase; letter-spacing: .04em; }
    .card-value { color: #111827; font-size: 28px; font-weight: 700; margin-top: 4px; }
    .card-note { color: #6b7280; font-size: 12px; margin-top: 4px; }
    section { background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; margin: 16px 0; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    th, td { border-bottom: 1px solid #edf0f4; padding: 8px; text-align: left; vertical-align: top; }
    th { color: #374151; background: #f9fafb; }
    .ok { color: #047857; font-weight: 600; }
    .warn { color: #b45309; font-weight: 600; }
    .bad { color: #b91c1c; font-weight: 600; }
    .bar-row { display: grid; grid-template-columns: 150px 1fr 50px; gap: 10px; align-items: center; margin: 7px 0; }
    .bar-track { background: #eef2ff; height: 14px; border-radius: 999px; overflow: hidden; }
    .bar-fill { background: #4f46e5; height: 100%; border-radius: 999px; }
    .bar-label, .bar-value { font-size: 13px; color: #374151; }
    """
    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>SyntheticL2 Validation Dashboard</title>
  <style>{css}</style>
</head>
<body>
  <h1>SyntheticL2 Validation Dashboard</h1>
  <p class="muted">Generated UTC: {html.escape(manifest['generated_utc'])}. Static dashboard for research traceability only; not promotion evidence.</p>
  <div class="cards">{cards}</div>
  <section><h2>Phase 14 Quality Status</h2>{_bar_rows(quality_status, 'status', 'checks')}{_table(quality, ['level', 'check_name', 'value', 'status', 'evidence'], 24)}</section>
  <section><h2>Phase 14 Holdout Generator Realism Proxy</h2>{_table(holdout, ['quarter_profile', 'feed_profile', 'holdout_role', 'scenario_days', 'symbols', 'regimes', 'realism_status', 'acceptance_eligible_now'], 20)}</section>
  <section><h2>Phase 14 Realism Acceptance Gap Ledger</h2>{_table(realism_gap_status, None, 10)}{_table(realism_gap, ['strategy_id', 'realism_requirement', 'observed_value', 'current_evidence_status', 'proxy_evidence_available', 'acceptance_requirement_met', 'blocking_gap'], 50)}</section>
  <section><h2>Phase 13 Robustness Dimension Proxy</h2>{_table(robustness_status, None, 10)}{_table(robustness_dimension, ['strategy_id', 'registered_for_phase13_proxy', 'initial_engineering_seeds_run', 'required_full_validation_seeds', 'execution_profiles_evaluated', 'parameter_sets_run', 'parameter_sets_planned', 'walk_forward_status', 'holdout_status', 'dimension_status'], 14)}</section>
  <section><h2>Phase 13 Robustness Acceptance Gap Ledger</h2>{_table(robustness_gap_status, None, 10)}{_table(robustness_gap, ['strategy_id', 'robustness_requirement', 'required_threshold', 'observed_value', 'current_evidence_status', 'acceptance_requirement_met', 'blocking_gap'], 40)}</section>
  <section><h2>Phase 12 Full-Run Lifecycle Risk Proxy</h2>{_table(lifecycle_overview, ['fill_model', 'strategy_profiles', 'orders', 'mean_fill_ratio', 'risk_adjusted_net_pnl_inr', 'daily_halt_rows', 'position_limit_breach_rows'], 10)}{_table(lifecycle_risk, ['strategy_id', 'execution_profile', 'fill_model', 'orders', 'mean_fill_ratio', 'risk_adjusted_net_pnl_inr', 'max_intraday_drawdown_inr', 'daily_halt_rows'], 18)}</section>
  <section><h2>Phase 12 Risk Breach Severity Proxy</h2>{_table(top_risk_severity, ['strategy_id', 'execution_profile', 'fill_model', 'breach_days', 'daily_loss_breach_days', 'position_limit_breach_days', 'drawdown_breach_days', 'daily_halt_days', 'risk_severity_score', 'risk_severity_band', 'risk_pass_candidate_proxy'], 25)}</section>
  <section><h2>Phase 12 Risk Limit Sensitivity Proxy</h2>{_table(top_risk_limit_sensitivity, ['strategy_id', 'execution_profile', 'fill_model', 'risk_limit_profile', 'breach_days', 'daily_loss_breach_days', 'drawdown_breach_days', 'position_limit_breach_days', 'tail_trade_loss_breach', 'risk_limit_severity_score', 'risk_limit_status', 'risk_pass_candidate_under_limit_profile'], 25)}</section>
  <section><h2>Phase 12 Risk Acceptance Readiness Ledger</h2>{_table(risk_acceptance_status, None, 10)}{_table(risk_acceptance_readiness, ['strategy_id', 'risk_requirement', 'observed_value', 'current_evidence_status', 'proxy_evidence_available', 'acceptance_requirement_met', 'blocking_gap'], 50)}</section>
  <section><h2>Phase 20 Execution Roadmap</h2>{_table(execution_milestones, ['execution_milestone', 'roadmap_rows', 'gates', 'strategies', 'action_classes', 'proxy_evidence_rows', 'missing_required_evidence_rows', 'acceptance_met_rows', 'acceptance_ready_rows', 'top_required_next_evidence'], 10)}{_table(execution_milestone_status, None, 30)}{_table(execution_roadmap, ['execution_rank', 'execution_milestone', 'gate_id', 'strategy_id', 'work_package_focus', 'hardening_requirement', 'action_class', 'dependency_status', 'required_next_evidence'], 60)}</section>
  <section><h2>Phase 20 Risk Hardening Plan</h2>{_table(risk_hardening_status, None, 10)}{_table(risk_hardening_action_summary, ['action_class', 'dependency_type', 'risk_requirement_rows', 'strategies', 'proxy_evidence_rows', 'acceptance_met_rows', 'open_rows'], 20)}{_table(risk_hardening_plan, ['queue_rank', 'strategy_id', 'risk_requirement', 'action_class', 'dependency_type', 'risk_hardening_status', 'risk_evidence_summary', 'required_next_evidence'], 50)}</section>
  <section><h2>Phase 20 Economic Hardening Plan</h2>{_table(economic_hardening_status, None, 10)}{_table(economic_hardening_action_summary, ['action_class', 'dependency_type', 'economic_requirement_rows', 'strategies', 'proxy_evidence_rows', 'acceptance_met_rows', 'open_rows'], 20)}{_table(economic_hardening_plan, ['queue_rank', 'strategy_id', 'economic_requirement', 'action_class', 'dependency_type', 'economic_hardening_status', 'economic_evidence_summary', 'required_next_evidence'], 50)}</section>
  <section><h2>Phase 20 Predictive Hardening Plan</h2>{_table(predictive_hardening_status, None, 10)}{_table(predictive_hardening_action_summary, ['action_class', 'dependency_type', 'predictive_requirement_rows', 'strategies', 'proxy_evidence_rows', 'acceptance_met_rows', 'open_rows'], 20)}{_table(predictive_hardening_plan, ['queue_rank', 'strategy_id', 'predictive_requirement', 'action_class', 'dependency_type', 'predictive_hardening_status', 'predictive_evidence_summary', 'required_next_evidence'], 50)}</section>
  <section><h2>Phase 20 Robustness Hardening Plan</h2>{_table(robustness_hardening_status, None, 10)}{_table(robustness_hardening_action_summary, ['action_class', 'dependency_type', 'robustness_requirement_rows', 'strategies', 'proxy_evidence_rows', 'acceptance_met_rows', 'open_rows'], 20)}{_table(robustness_hardening_plan, ['queue_rank', 'strategy_id', 'robustness_requirement', 'action_class', 'dependency_type', 'robustness_hardening_status', 'robustness_evidence_summary', 'required_next_evidence'], 50)}</section>
  <section><h2>Phase 20 Realism Hardening Plan</h2>{_table(realism_hardening_status, None, 10)}{_table(realism_hardening_action_summary, ['action_class', 'dependency_type', 'realism_requirement_rows', 'strategies', 'proxy_evidence_rows', 'acceptance_met_rows', 'open_rows'], 20)}{_table(realism_hardening_plan, ['queue_rank', 'strategy_id', 'realism_requirement', 'action_class', 'dependency_type', 'realism_hardening_status', 'realism_evidence_summary', 'required_next_evidence'], 50)}</section>
  <section><h2>Phase 20 M01 Broker Evidence Contract</h2>{_table(broker_import_checklist, ['evidence_file_id', 'expected_path', 'evidence_domain', 'file_exists_now', 'current_status', 'next_action'], 10)}{_table(broker_external_gap_summary, None, 10)}{_table(broker_external_status, None, 10)}{_table(broker_reconciliation_test_catalog, ['test_id', 'acceptance_threshold', 'current_status'], 10)}{_table(broker_external_gap_ledger, ['execution_rank', 'gate_id', 'strategy_id', 'hardening_requirement', 'required_external_files', 'broker_evidence_status', 'acceptance_requirement_met_after_contract', 'blocking_gap_after_contract'], 60)}</section>
  <section><h2>Phase 20 M02 Strategy Support Contract</h2>{_table(strategy_support_gap_summary, None, 10)}{_table(strategy_support_status, None, 20)}{_table(strategy_support_decision_summary, ['strategy_id', 'strategy_support_closure_status', 'm02_rows', 'required_support_action'], 15)}{_table(strategy_support_criteria, ['criterion_id', 'acceptance_threshold', 'current_status'], 10)}{_table(strategy_support_ledger, ['execution_rank', 'gate_id', 'strategy_id', 'strategy_support_level', 'hardening_requirement', 'support_contract_status', 'alpha_promotion_scope', 'acceptance_requirement_met_after_contract', 'required_support_action'], 60)}</section>
  <section><h2>Phase 20 M03 Predictive Validation Contract</h2>{_table(predictive_validation_gap_summary, None, 12)}{_table(predictive_validation_status, None, 12)}{_table(predictive_validation_strategy_summary, ['strategy_id', 'strategy_support_level', 'm03_rows', 'baseline_pass_proxy', 'predictive_promotion_candidate_proxy', 'predictive_validation_status'], 15)}{_table(predictive_validation_criteria, ['criterion_id', 'acceptance_threshold', 'current_status'], 10)}{_table(predictive_validation_ledger, ['execution_rank', 'strategy_id', 'hardening_requirement', 'predictive_contract_status', 'observed_predictive_metric', 'acceptance_requirement_met_after_contract', 'required_predictive_action'], 70)}</section>
  <section><h2>Phase 20 M04 Robustness Execution Contract</h2>{_table(robustness_execution_gap_summary, None, 12)}{_table(robustness_execution_status, None, 12)}{_table(robustness_execution_strategy_summary, ['strategy_id', 'strategy_support_level', 'm04_rows', 'seed_rows_requiring_execution', 'walk_forward_rows_requiring_execution', 'robustness_execution_contract_status'], 15)}{_table(robustness_execution_criteria, ['criterion_id', 'acceptance_threshold', 'current_status'], 10)}{_table(robustness_execution_ledger, ['execution_rank', 'strategy_id', 'hardening_requirement', 'robustness_execution_status', 'observed_robustness_metric', 'acceptance_requirement_met_after_contract', 'required_robustness_action'], 70)}</section>
  <section><h2>Phase 20 M05 Lifecycle/Economic Replay Contract</h2>{_table(lifecycle_economic_gap_summary, None, 12)}{_table(lifecycle_economic_status, None, 12)}{_table(lifecycle_economic_strategy_summary, ['strategy_id', 'strategy_support_level', 'm05_rows', 'risk_replay_rows', 'economic_replay_rows', 'lifecycle_economic_contract_status'], 15)}{_table(lifecycle_economic_criteria, ['criterion_id', 'acceptance_threshold', 'current_status'], 10)}{_table(lifecycle_economic_ledger, ['execution_rank', 'gate_id', 'strategy_id', 'hardening_requirement', 'lifecycle_economic_status', 'observed_lifecycle_economic_metric', 'acceptance_requirement_met_after_contract', 'required_lifecycle_economic_action'], 90)}</section>
  <section><h2>Phase 20 M06 Holdout/Realism Rerun Contract</h2>{_table(realism_rerun_gap_summary, None, 12)}{_table(realism_rerun_status, None, 12)}{_table(realism_rerun_strategy_summary, ['strategy_id', 'strategy_support_level', 'm06_rows', 'holdout_rerun_rows', 'feed_imperfection_rows', 'realism_rerun_contract_status'], 15)}{_table(realism_rerun_criteria, ['criterion_id', 'acceptance_threshold', 'current_status'], 10)}{_table(realism_rerun_ledger, ['execution_rank', 'gate_id', 'strategy_id', 'hardening_requirement', 'realism_rerun_status', 'observed_realism_metric', 'acceptance_requirement_met_after_contract', 'required_realism_action'], 70)}</section>
  <section><h2>Phase 20 M07 Real Multi-Day Acceptance Contract</h2>{_table(real_multiday_gap_summary, None, 12)}{_table(real_multiday_status, None, 12)}{_table(real_multiday_strategy_summary, ['strategy_id', 'strategy_support_level', 'm07_rows', 'economic_real_validation_rows', 'predictive_real_holdout_rows', 'real_multiday_contract_status'], 15)}{_table(real_multiday_criteria, ['criterion_id', 'acceptance_threshold', 'current_status'], 10)}{_table(real_multiday_ledger, ['execution_rank', 'gate_id', 'strategy_id', 'hardening_requirement', 'real_multiday_acceptance_status', 'observed_real_multiday_metric', 'acceptance_requirement_met_after_contract', 'required_real_multiday_action'], 70)}</section>
  <section><h2>Stage A2 Capture Diagnostics Contract</h2>{_table(stage_a2_readiness_summary, None, 5)}{_table(stage_a2_gap_summary, None, 10)}{_table(stage_a2_status, None, 10)}{_table(stage_a2_criteria, ['criterion_id', 'acceptance_threshold', 'current_status'], 10)}{_table(stage_a2_schema, ['artifact_name', 'field_name', 'field_type', 'required_status'], 25)}{_table(stage_a2_ledger, ['symbol', 'criterion_id', 'capture_contract_status', 'current_sample_days_available', 'current_stale_gap_gt_15s_count', 'acceptance_requirement_met_after_contract', 'required_capture_action'], 70)}</section>
  <section><h2>Stage B1 Structural Synthetic Proof</h2>{_table(stage_b1_check_status, None, 5)}{_table(stage_b1_subset, ['symbol', 'instrument_class', 'row_count', 'event_rate_per_second', 'selection_reason'], 10)}{_table(stage_b1_scenario_summary, None, 10)}{_table(stage_b1_criteria, ['criterion_id', 'acceptance_threshold', 'current_status'], 10)}{_table(stage_b1_check_ledger, ['check_id', 'observed_value', 'expected_value', 'passed', 'detail'], 10)}</section>
  <section><h2>Stage B2 Event-Driven Synthetic Proof</h2>{_table(stage_b2_check_status, None, 5)}{_table(stage_b2_dataset_summary, None, 12)}{_table(stage_b2_readiness, ['symbol', 'instrument_class', 'window_name', 'event_rate_per_second', 'coverage_fraction', 'dense_1s_ready', 'event_driven_1s_ready', 'stage_b2_1s_action'], 10)}{_table(stage_b2_scenario_selection, ['stage_b2_bucket', 'scenario_day', 'trade_date', 'quarter_profile', 'regime_family', 'is_market_shock_day'], 10)}{_table(stage_b2_criteria, ['criterion_id', 'acceptance_threshold', 'current_status'], 10)}{_table(stage_b2_check_ledger, ['check_id', 'observed_value', 'expected_value', 'passed', 'detail'], 10)}</section>
  <section><h2>Stage C Medium Pilot</h2>{_table(stage_c_check_status, None, 5)}{_table(stage_c_dataset_summary, None, 12)}{_table(stage_c_selected_days, ['quarter_profile', 'scenario_day', 'trade_date', 'regime_family', 'is_market_shock_day'], 25)}{_table(stage_c_selected_seeds, None, 5)}{_table(stage_c_strategy_runs, ['model_id', 'model_name', 'simulation_seed', 'trades', 'signal_fraction', 'mean_gross_return_proxy', 'win_rate_proxy', 'pilot_status'], 20)}{_table(stage_c_baseline_runs, ['model_id', 'model_name', 'simulation_seed', 'trades', 'signal_fraction', 'mean_gross_return_proxy', 'win_rate_proxy', 'pilot_status'], 25)}{_table(stage_c_check_ledger, ['check_id', 'observed_value', 'expected_value', 'passed', 'detail'], 10)}</section>
  <section><h2>Stage D Three-Month Study Proxy</h2>{_table(stage_d_check_status, None, 5)}{_table(stage_d_dataset_summary, None, 15)}{_table(stage_d_profile_summary, None, 5)}{_table(stage_d_seed_summary, None, 5)}{_table(stage_d_data_inventory, ['data_product', 'path', 'rows', 'columns', 'present'], 5)}{_table(stage_d_strategy_summary, ['strategy_id', 'strategy_name', 'strategy_role', 'support_level', 'simulation_seed', 'trades', 'signal_fraction', 'mean_gross_return_proxy', 'control_or_risk_module', 'stage_d_status'], 35)}{_table(stage_d_check_ledger, ['check_id', 'observed_value', 'expected_value', 'passed', 'detail'], 12)}</section>
  <section><h2>Stage E Full-Year Extension Readiness</h2>{_table(stage_e_status, None, 5)}{_table(stage_e_gap_summary, None, 5)}{_table(stage_e_criteria, ['criterion_id', 'acceptance_threshold', 'current_status'], 10)}{_table(stage_e_prerequisite_ledger, ['prerequisite_id', 'observed_value', 'passes', 'blocking_gap', 'required_next_action'], 12)}{_table(stage_e_action_plan, ['priority_rank', 'prerequisite_id', 'blocking_gap', 'required_next_action'], 10)}</section>
  <section><h2>Phase 21 Decision Framework</h2>{_table(phase21_decision_status, None, 10)}{_table(phase21_decision_summary, None, 10)}{_table(phase21_decision_rules, ['decision_rule_id', 'outcome_condition', 'plan_decision'], 12)}{_table(phase21_decision_ledger, ['decision_rule_id', 'current_condition_met', 'observed_value', 'current_decision', 'decision_status', 'next_action'], 12)}</section>
  <section><h2>Phase 22 Real Data Integration Roadmap</h2>{_table(phase22_milestone_status, None, 10)}{_table(phase22_task_status, None, 10)}{_table(phase22_summary, None, 10)}{_table(phase22_milestone_catalog, ['milestone_id', 'real_data_availability', 'current_class_b_event_grade_days', 'current_sample_days_available', 'days_needed_for_min', 'recalibration_use', 'current_status'], 10)}{_table(phase22_capture_expansion_plan, ['priority_rank', 'workstream', 'current_state', 'target_state', 'blocking_gap', 'required_next_action'], 10)}</section>
  <section><h2>Phase 23 Key Risk Register</h2>{_table(phase23_risk_status, None, 10)}{_table(phase23_mitigation_status, None, 10)}{_table(phase23_summary, None, 10)}{_table(phase23_risk_register, ['risk_id', 'risk_title', 'severity', 'current_status', 'observed_value', 'required_next_action'], 10)}{_table(phase23_promotion_path, ['promotion_order', 'promotion_step', 'current_status', 'skip_allowed'], 10)}</section>
  <section><h2>Phase 25 Event Replay Expansion</h2>{_table(phase25_profile_status, None, 10)}{_table(phase25_risk_status, None, 10)}{_table(phase25_overall_summary, None, 10)}{_table(phase25_replay_summary, ['model_id', 'model_type', 'execution_profile', 'trades', 'mean_net_return', 'total_net_pnl_inr', 'replay_status'], 30)}{_table(phase25_baseline_comparison, ['model_id', 'execution_profile', 'strategy_mean_net_return', 'best_baseline_mean_net_return', 'net_return_lift_vs_best_baseline', 'beats_best_baseline_proxy'], 20)}</section>
  <section><h2>Phase 26 Strategy Salvage Scan</h2>{_table(phase26_profile_status, None, 15)}{_table(phase26_rejection_status, None, 10)}{_table(phase26_overall_summary, None, 12)}{_table(phase26_candidate_summary, ['variant_id', 'parent_strategy_id', 'execution_profile', 'trades', 'mean_net_return', 'best_baseline_mean_net_return', 'positive_after_costs', 'realistic_charged_profile', 'salvage_candidate_proxy', 'zero_latency_positive_control'], 30)}{_table(phase26_rejection_ledger, ['variant_id', 'parent_strategy_id', 'execution_profile', 'rejection_reasons', 'salvage_candidate_proxy'], 30)}{_table(phase26_variant_catalog, ['variant_id', 'parent_strategy_id', 'threshold_quantile', 'spread_limit_quantile', 'liquidity_filter'], 20)}</section>
  <section><h2>Phase 27 Feature Edge Cost-Hurdle Scan</h2>{_table(phase27_profile_status, None, 15)}{_table(phase27_rejection_status, None, 10)}{_table(phase27_overall_summary, None, 12)}{_table(phase27_family_summary, ['feature_family', 'execution_profile', 'candidate_rows', 'positive_after_cost_rows', 'realistic_cost_clearing_rows', 'zero_latency_edge_control_rows', 'max_mean_net_return', 'max_cost_hurdle_ratio'], 30)}{_table(phase27_candidate_summary, ['candidate_id', 'feature_id', 'execution_profile', 'horizon_events', 'trades', 'mean_net_return', 'mean_cost_return', 'positive_after_costs', 'realistic_cost_clearing_edge', 'zero_latency_edge_control'], 30)}{_table(phase27_rejection_ledger, ['candidate_id', 'feature_family', 'execution_profile', 'horizon_events', 'rejection_reasons', 'realistic_cost_clearing_edge'], 30)}{_table(phase27_candidate_catalog, ['candidate_id', 'feature_family', 'feature_column', 'polarity', 'horizon_events', 'threshold_quantile'], 20)}</section>
  <section><h2>Phase 28 Richer Event Label Support</h2>{_table(phase28_support_status, None, 10)}{_table(phase28_overall_summary, None, 10)}{_table(phase28_strategy_support_summary, ['strategy_id', 'feature_label_family', 'proxy_rows', 'symbols_with_proxy', 'support_upgrade_status', 'acceptance_ready', 'required_next_evidence'], 10)}{_table(phase28_feature_label_catalog, ['strategy_id', 'feature_label', 'current_support', 'acceptance_blocker'], 10)}{_table(phase28_event_label_summary, ['symbol', 'usable_short_horizon_rows', 's03_liquidity_vacuum_proxy_rows', 's04_trade_flow_depth_confirm_rows', 's06_absorption_like_proxy_rows', 's08_lead_lag_bucket_rows'], 40)}{_table(phase28_lead_lag_summary, ['symbol', 'lead_lag_bucket_rows', 'lead_lag_abs_corr_proxy', 's08_proxy_available', 'limitation'], 40)}</section>
  <section><h2>Phase 29 Partial Strategy Proxy Replay</h2>{_table(phase29_profile_status, None, 15)}{_table(phase29_risk_status, None, 10)}{_table(phase29_overall_summary, None, 10)}{_table(phase29_summary, ['model_id', 'execution_profile', 'trades', 'mean_gross_return', 'mean_cost_return', 'mean_net_return', 'win_rate_net', 'total_net_pnl_inr'], 20)}{_table(phase29_candidate_summary, ['model_id', 'execution_profile', 'trades', 'mean_net_return', 'positive_after_costs', 'realistic_charged_profile', 'risk_status', 'partial_proxy_candidate'], 20)}</section>
  <section><h2>Phase 30 Strategy Decision Triage</h2>{_table(phase30_decision_status, None, 10)}{_table(phase30_redesign_priority, None, 10)}{_table(phase30_overall_summary, None, 12)}{_table(phase30_decision_ledger, ['strategy_id', 'strategy_name', 'current_decision', 'promotion_ready', 'acceptance_ready', 'realistic_positive_execution_rows', 'candidate_rows', 'blocking_reason'], 20)}{_table(phase30_execution_evidence, ['strategy_id', 'evidence_scope', 'realistic_positive_execution_rows', 'candidate_rows', 'phase28_proxy_rows', 'phase29_trades', 'evidence_note'], 20)}{_table(phase30_redesign_queue, ['strategy_id', 'strategy_name', 'redesign_priority', 'redesign_theme', 'required_evidence_before_next_execution_expansion'], 20)}</section>
  <section><h2>Phase 31 Redesign Evidence Contract</h2>{_table(phase31_contract_status, None, 10)}{_table(phase31_evidence_domain_status, None, 20)}{_table(phase31_overall_summary, None, 12)}{_table(phase31_replay_gate, ['strategy_id', 'strategy_name', 'redesign_priority', 'contract_requirements', 'open_requirements', 'replay_expansion_allowed', 'redesign_contract_status', 'next_action'], 20)}{_table(phase31_spec_catalog, ['strategy_id', 'strategy_name', 'redesign_priority', 'contract_requirements', 'evidence_domains', 'open_requirements', 'replay_expansion_allowed'], 20)}{_table(phase31_contract_ledger, ['strategy_id', 'contract_requirement_id', 'evidence_domain', 'required_artifact_or_test', 'current_evidence_status', 'acceptance_requirement_met', 'replay_expansion_allowed'], 60)}</section>
  <section><h2>Phase 32 Contract Evidence Scanner</h2>{_table(phase32_scanner_status, None, 12)}{_table(phase32_overall_summary, None, 12)}{_table(phase32_availability_summary, None, 20)}{_table(phase32_strategy_summary, ['strategy_id', 'strategy_name', 'requirement_rows', 'proxy_or_partial_available_rows', 'external_missing_rows', 'acceptance_met_rows', 'replay_allowed_rows', 'evidence_scan_status'], 20)}{_table(phase32_acquisition_queue, ['scanner_evidence_status', 'evidence_domain', 'requirement_rows', 'strategies', 'next_action'], 20)}{_table(phase32_scan_ledger, ['strategy_id', 'contract_requirement_id', 'evidence_domain', 'scanner_evidence_status', 'available_evidence_source', 'scanner_acceptance_requirement_met', 'scanner_replay_expansion_allowed'], 70)}</section>
  <section><h2>Phase 33 Broker Evidence Intake</h2>{_table(phase33_file_status, None, 10)}{_table(phase33_test_status, None, 10)}{_table(phase33_overall_summary, None, 12)}{_table(phase33_template_inventory, ['evidence_file_id', 'template_path', 'expected_external_path', 'required_fields', 'total_fields', 'template_status'], 10)}{_table(phase33_file_validation, ['evidence_file_id', 'expected_external_path', 'file_exists_now', 'row_count', 'required_columns_present', 'schema_validation_status', 'acceptance_import_ready', 'next_action'], 10)}{_table(phase33_test_readiness, ['test_id', 'required_evidence_files', 'missing_or_not_ready_files', 'test_import_ready', 'current_status'], 10)}</section>
  <section><h2>Phase 34 Real Data Multi-Day Readiness</h2>{_table(phase34_day_status, None, 10)}{_table(phase34_symbol_status, None, 10)}{_table(phase34_readiness_summary, None, 12)}{_table(phase34_day_inventory, ['trade_date', 'exchange', 'symbols', 'parquet_files', 'phase1_delta_rows', 'full_universe_raw_day', 'class_b_event_grade_day', 'day_status'], 10)}{_table(phase34_acquisition_plan, ['priority', 'action_id', 'action', 'current_blocker', 'acceptance_effect'], 10)}{_table(phase34_symbol_day_coverage, ['trade_date', 'exchange', 'symbol', 'parquet_files', 'phase1_delta_rows', 'book_valid_fraction', 'stale_gap_gt_15s_count', 'class_b_event_grade_now'], 40)}</section>
  <section><h2>Phase 15 Acceptance Blockers</h2>{_bar_rows(gate_blockers, 'gate_id', 'blockers')}{_table(acceptance, ['strategy_id', 'passed_gates', 'blocked_gates', 'promotion_allowed', 'acceptance_status', 'support_level'], 20)}</section>
  <section><h2>Phase 16 Metric Coverage</h2>{_table(metric_status, None, 20)}{_table(metric_catalog, ['metric_category', 'metric_name', 'current_status', 'acceptance_eligible_now', 'evidence_note'], 40)}</section>
  <section><h2>Top Predictive Proxy Diagnostics</h2>{_table(top_predictive, ['strategy_id', 'balanced_accuracy_proxy', 'precision_long_proxy', 'precision_short_proxy', 'rank_auc_proxy', 'incremental_r2_proxy'], 12)}</section>
  <section><h2>Phase 16 Predictive Holdout Stability</h2>{_table(top_predictive_holdout, ['strategy_id', 'support_level', 'stability_cells', 'cells_beating_local_majority', 'cell_beat_fraction', 'untouched_test_cells_beating_local_majority', 'min_accuracy_excess_vs_majority', 'worst_segment_status'], 14)}</section>
  <section><h2>Phase 16 Predictive Promotion Falsification</h2>{_table(top_predictive_falsification, ['strategy_id', 'support_level', 'baseline_pass_proxy', 'holdout_all_cell_pass_proxy', 'untouched_test_pass_proxy', 'feature_stability_proxy_available', 'predictive_promotion_candidate_proxy', 'falsification_status', 'blocker'], 14)}</section>
  <section><h2>Phase 16 Predictive Acceptance Gap Ledger</h2>{_table(predictive_gap_status, None, 10)}{_table(predictive_gap, ['strategy_id', 'predictive_requirement', 'observed_value', 'current_evidence_status', 'proxy_evidence_available', 'acceptance_requirement_met', 'blocking_gap'], 50)}</section>
  <section><h2>Phase 16 Economic Viability Frontier</h2>{_table(top_economic, ['strategy_id', 'execution_profile', 'gross_edge_bps', 'cost_drag_bps', 'net_edge_bps', 'additional_gross_edge_needed_bps', 'cost_reduction_needed_bps', 'economic_frontier_status'], 18)}</section>
  <section><h2>Phase 16 Risk-Adjusted Economic Frontier</h2>{_table(top_risk_adjusted_economic, ['strategy_id', 'execution_profile', 'fill_model', 'net_edge_bps', 'risk_penalty_bps', 'risk_adjusted_net_edge_bps', 'net_positive_proxy', 'risk_pass_candidate_proxy', 'net_positive_and_risk_pass_proxy', 'risk_severity_band', 'risk_adjusted_frontier_status'], 25)}</section>
  <section><h2>Phase 16 Broker Reconciliation Readiness</h2>{_table(broker_reconciliation, ['reconciliation_domain', 'reconciliation_item', 'proxy_formula_available_now', 'broker_contract_note_available_now', 'actual_fill_available_now', 'reconciliation_status', 'blocker'], 25)}{_table(economic_reconciliation, ['strategy_id', 'net_positive_proxy_rows', 'retail_stress_net_positive_proxy_rows', 'risk_adjusted_joint_pass_rows', 'documented_zerodha_formula_ready', 'broker_contract_note_reconciliation_ready', 'economic_acceptance_ready_now', 'readiness_status'], 15)}</section>
  <section><h2>Phase 16 Economic Acceptance Gap Ledger</h2>{_table(economic_gap_status, None, 10)}{_table(economic_gap, ['strategy_id', 'economic_requirement', 'observed_value', 'current_evidence_status', 'proxy_evidence_available', 'acceptance_requirement_met', 'blocking_gap'], 50)}</section>
  <section><h2>Top Trading Proxy Rows</h2>{_table(top_trading, ['strategy_id', 'execution_profile', 'trades', 'mean_net_return', 'win_rate_net', 'sample_max_drawdown_units', 'sample_profit_factor'], 15)}</section>
  <section><h2>Best Lower-Adverse-Selection Markout Rows</h2>{_table(top_markout, ['strategy_id', 'execution_profile', 'markout_sample_trades', 'adverse_selection_rate_6bar_proxy', 'mean_mae_proxy', 'mean_mfe_proxy'], 15)}</section>
  <section><h2>Phase 20 Acceptance Hardening Queue</h2>{_bar_rows(hardening_priority, 'priority_band', 'queue_items')}{_table(hardening_gate_summary, ['priority_rank', 'gate_id', 'gate_name', 'blocked_strategies', 'work_package_focus', 'acceptance_milestone'], 10)}{_table(hardening_queue, ['queue_rank', 'priority_band', 'gate_id', 'strategy_id', 'strategy_support_level', 'work_package_focus', 'acceptance_milestone', 'next_required_evidence'], 25)}</section>
  <section><h2>Phase 17 Gap Backlog</h2>{_bar_rows(gap_priority, 'priority', 'gaps')}{_table(gaps, ['priority', 'work_package_id', 'deliverable', 'implementation_status', 'evidence_status', 'recommended_next_action'], 40)}</section>
</body>
</html>"""

    md_lines = [
        "# SyntheticL2 Validation Dashboard Summary",
        "",
        f"Generated UTC: {manifest['generated_utc']}",
        "",
        "This dashboard is static research traceability output, not strategy promotion evidence.",
        "",
        "## Summary Metrics",
        "",
        _markdown_table(summary),
        "",
        "## Quality Status",
        "",
        _markdown_table(quality_status),
        "",
        "## Holdout Generator Realism Proxy",
        "",
        _markdown_table(holdout),
        "",
        "## Realism Acceptance Gap Ledger",
        "",
        _markdown_table(realism_gap_status),
        "",
        _markdown_table(realism_gap),
        "",
        "## Phase 12 Full-Run Lifecycle Risk Proxy",
        "",
        _markdown_table(lifecycle_overview),
        "",
        "## Phase 12 Risk Breach Severity Proxy",
        "",
        _markdown_table(top_risk_severity.head(25)),
        "",
        "## Phase 12 Risk Limit Sensitivity Proxy",
        "",
        _markdown_table(top_risk_limit_sensitivity.head(25)),
        "",
        "## Phase 12 Risk Acceptance Readiness Ledger",
        "",
        _markdown_table(risk_acceptance_status),
        "",
        _markdown_table(risk_acceptance_readiness),
        "",
        "## Phase 13 Robustness Dimension Proxy",
        "",
        _markdown_table(robustness_status),
        "",
        "## Phase 13 Robustness Acceptance Gap Ledger",
        "",
        _markdown_table(robustness_gap_status),
        "",
        _markdown_table(robustness_gap),
        "",
        "## Economic Viability Frontier",
        "",
        _markdown_table(top_economic.head(18)),
        "",
        "## Risk-Adjusted Economic Frontier",
        "",
        _markdown_table(top_risk_adjusted_economic.head(25)),
        "",
        "## Broker Reconciliation Readiness",
        "",
        _markdown_table(broker_reconciliation),
        "",
        "## Economic Reconciliation Strategy Readiness",
        "",
        _markdown_table(economic_reconciliation),
        "",
        "## Economic Acceptance Gap Ledger",
        "",
        _markdown_table(economic_gap_status),
        "",
        _markdown_table(economic_gap),
        "",
        "## Predictive Holdout Stability",
        "",
        _markdown_table(top_predictive_holdout),
        "",
        "## Predictive Promotion Falsification",
        "",
        _markdown_table(top_predictive_falsification),
        "",
        "## Predictive Acceptance Gap Ledger",
        "",
        _markdown_table(predictive_gap_status),
        "",
        _markdown_table(predictive_gap),
        "",
        "## Acceptance Blockers by Gate",
        "",
        _markdown_table(gate_blockers),
        "",
        "## Phase 20 Acceptance Hardening Queue",
        "",
        _markdown_table(hardening_gate_summary),
        "",
        _markdown_table(hardening_queue.head(25)),
        "",
        "## Phase 20 Execution Roadmap",
        "",
        _markdown_table(execution_milestones),
        "",
        _markdown_table(execution_milestone_status),
        "",
        _markdown_table(execution_roadmap.head(60)),
        "",
        "## Phase 20 Risk Hardening Plan",
        "",
        _markdown_table(risk_hardening_status),
        "",
        _markdown_table(risk_hardening_action_summary),
        "",
        _markdown_table(risk_hardening_plan.head(50)),
        "",
        "## Phase 20 Economic Hardening Plan",
        "",
        _markdown_table(economic_hardening_status),
        "",
        _markdown_table(economic_hardening_action_summary),
        "",
        _markdown_table(economic_hardening_plan.head(50)),
        "",
        "## Phase 20 Predictive Hardening Plan",
        "",
        _markdown_table(predictive_hardening_status),
        "",
        _markdown_table(predictive_hardening_action_summary),
        "",
        _markdown_table(predictive_hardening_plan.head(50)),
        "",
        "## Phase 20 Robustness Hardening Plan",
        "",
        _markdown_table(robustness_hardening_status),
        "",
        _markdown_table(robustness_hardening_action_summary),
        "",
        _markdown_table(robustness_hardening_plan.head(50)),
        "",
        "## Phase 20 Realism Hardening Plan",
        "",
        _markdown_table(realism_hardening_status),
        "",
        _markdown_table(realism_hardening_action_summary),
        "",
        _markdown_table(realism_hardening_plan.head(50)),
        "",
        "## Phase 20 M01 Broker Evidence Contract",
        "",
        _markdown_table(broker_import_checklist),
        "",
        _markdown_table(broker_external_gap_summary),
        "",
        _markdown_table(broker_external_status),
        "",
        _markdown_table(broker_reconciliation_test_catalog),
        "",
        _markdown_table(broker_external_gap_ledger.head(60)),
        "",
        "## Phase 20 M02 Strategy Support Contract",
        "",
        _markdown_table(strategy_support_gap_summary),
        "",
        _markdown_table(strategy_support_status),
        "",
        _markdown_table(strategy_support_decision_summary),
        "",
        _markdown_table(strategy_support_criteria),
        "",
        _markdown_table(strategy_support_ledger.head(60)),
        "",
        "## Phase 20 M03 Predictive Validation Contract",
        "",
        _markdown_table(predictive_validation_gap_summary),
        "",
        _markdown_table(predictive_validation_status),
        "",
        _markdown_table(predictive_validation_strategy_summary),
        "",
        _markdown_table(predictive_validation_criteria),
        "",
        _markdown_table(predictive_validation_ledger.head(70)),
        "",
        "## Phase 20 M04 Robustness Execution Contract",
        "",
        _markdown_table(robustness_execution_gap_summary),
        "",
        _markdown_table(robustness_execution_status),
        "",
        _markdown_table(robustness_execution_strategy_summary),
        "",
        _markdown_table(robustness_execution_criteria),
        "",
        _markdown_table(robustness_execution_ledger.head(70)),
        "",
        "## Phase 20 M05 Lifecycle/Economic Replay Contract",
        "",
        _markdown_table(lifecycle_economic_gap_summary),
        "",
        _markdown_table(lifecycle_economic_status),
        "",
        _markdown_table(lifecycle_economic_strategy_summary),
        "",
        _markdown_table(lifecycle_economic_criteria),
        "",
        _markdown_table(lifecycle_economic_ledger.head(90)),
        "",
        "## Phase 20 M06 Holdout/Realism Rerun Contract",
        "",
        _markdown_table(realism_rerun_gap_summary),
        "",
        _markdown_table(realism_rerun_status),
        "",
        _markdown_table(realism_rerun_strategy_summary),
        "",
        _markdown_table(realism_rerun_criteria),
        "",
        _markdown_table(realism_rerun_ledger.head(70)),
        "",
        "## Phase 20 M07 Real Multi-Day Acceptance Contract",
        "",
        _markdown_table(real_multiday_gap_summary),
        "",
        _markdown_table(real_multiday_status),
        "",
        _markdown_table(real_multiday_strategy_summary),
        "",
        _markdown_table(real_multiday_criteria),
        "",
        _markdown_table(real_multiday_ledger.head(70)),
        "",
        "## Stage A2 Capture Diagnostics Contract",
        "",
        _markdown_table(stage_a2_readiness_summary),
        "",
        _markdown_table(stage_a2_gap_summary),
        "",
        _markdown_table(stage_a2_status),
        "",
        _markdown_table(stage_a2_criteria),
        "",
        _markdown_table(stage_a2_schema),
        "",
        _markdown_table(stage_a2_ledger.head(70)),
        "",
        "## Stage B1 Structural Synthetic Proof",
        "",
        _markdown_table(stage_b1_check_status),
        "",
        _markdown_table(stage_b1_subset),
        "",
        _markdown_table(stage_b1_scenario_summary),
        "",
        _markdown_table(stage_b1_criteria),
        "",
        _markdown_table(stage_b1_check_ledger),
        "",
        "## Stage B2 Event-Driven Synthetic Proof",
        "",
        _markdown_table(stage_b2_check_status),
        "",
        _markdown_table(stage_b2_dataset_summary),
        "",
        _markdown_table(stage_b2_readiness),
        "",
        _markdown_table(stage_b2_scenario_selection),
        "",
        _markdown_table(stage_b2_criteria),
        "",
        _markdown_table(stage_b2_check_ledger),
        "",
        "## Stage C Medium Pilot",
        "",
        _markdown_table(stage_c_check_status),
        "",
        _markdown_table(stage_c_dataset_summary),
        "",
        _markdown_table(stage_c_selected_days),
        "",
        _markdown_table(stage_c_selected_seeds),
        "",
        _markdown_table(stage_c_strategy_runs),
        "",
        _markdown_table(stage_c_baseline_runs),
        "",
        _markdown_table(stage_c_check_ledger),
        "",
        "## Stage D Three-Month Study Proxy",
        "",
        _markdown_table(stage_d_check_status),
        "",
        _markdown_table(stage_d_dataset_summary),
        "",
        _markdown_table(stage_d_profile_summary),
        "",
        _markdown_table(stage_d_seed_summary),
        "",
        _markdown_table(stage_d_data_inventory),
        "",
        _markdown_table(stage_d_strategy_summary),
        "",
        _markdown_table(stage_d_check_ledger),
        "",
        "## Stage E Full-Year Extension Readiness",
        "",
        _markdown_table(stage_e_status),
        "",
        _markdown_table(stage_e_gap_summary),
        "",
        _markdown_table(stage_e_criteria),
        "",
        _markdown_table(stage_e_prerequisite_ledger),
        "",
        _markdown_table(stage_e_action_plan),
        "",
        "## Phase 21 Decision Framework",
        "",
        _markdown_table(phase21_decision_status),
        "",
        _markdown_table(phase21_decision_summary),
        "",
        _markdown_table(phase21_decision_rules),
        "",
        _markdown_table(phase21_decision_ledger),
        "",
        "## Phase 22 Real Data Integration Roadmap",
        "",
        _markdown_table(phase22_milestone_status),
        "",
        _markdown_table(phase22_task_status),
        "",
        _markdown_table(phase22_summary),
        "",
        _markdown_table(phase22_milestone_catalog),
        "",
        _markdown_table(phase22_capture_expansion_plan),
        "",
        "## Phase 23 Key Risk Register",
        "",
        _markdown_table(phase23_risk_status),
        "",
        _markdown_table(phase23_mitigation_status),
        "",
        _markdown_table(phase23_summary),
        "",
        _markdown_table(phase23_risk_register),
        "",
        _markdown_table(phase23_promotion_path),
        "",
        "## Phase 25 Event Replay Expansion",
        "",
        _markdown_table(phase25_profile_status),
        "",
        _markdown_table(phase25_risk_status),
        "",
        _markdown_table(phase25_overall_summary),
        "",
        _markdown_table(phase25_replay_summary),
        "",
        _markdown_table(phase25_baseline_comparison),
        "",
        "## Phase 26 Strategy Salvage Scan",
        "",
        _markdown_table(phase26_profile_status),
        "",
        _markdown_table(phase26_rejection_status),
        "",
        _markdown_table(phase26_overall_summary),
        "",
        _markdown_table(phase26_candidate_summary),
        "",
        _markdown_table(phase26_rejection_ledger),
        "",
        "## Phase 27 Feature Edge Cost-Hurdle Scan",
        "",
        _markdown_table(phase27_profile_status),
        "",
        _markdown_table(phase27_rejection_status),
        "",
        _markdown_table(phase27_overall_summary),
        "",
        _markdown_table(phase27_family_summary),
        "",
        _markdown_table(phase27_candidate_summary),
        "",
        _markdown_table(phase27_rejection_ledger),
        "",
        "## Phase 28 Richer Event Label Support",
        "",
        _markdown_table(phase28_support_status),
        "",
        _markdown_table(phase28_overall_summary),
        "",
        _markdown_table(phase28_strategy_support_summary),
        "",
        _markdown_table(phase28_feature_label_catalog),
        "",
        _markdown_table(phase28_event_label_summary),
        "",
        _markdown_table(phase28_lead_lag_summary),
        "",
        "## Phase 29 Partial Strategy Proxy Replay",
        "",
        _markdown_table(phase29_profile_status),
        "",
        _markdown_table(phase29_risk_status),
        "",
        _markdown_table(phase29_overall_summary),
        "",
        _markdown_table(phase29_summary),
        "",
        _markdown_table(phase29_candidate_summary),
        "",
        "## Phase 30 Strategy Decision Triage",
        "",
        _markdown_table(phase30_decision_status),
        "",
        _markdown_table(phase30_redesign_priority),
        "",
        _markdown_table(phase30_overall_summary),
        "",
        _markdown_table(phase30_decision_ledger),
        "",
        _markdown_table(phase30_execution_evidence),
        "",
        _markdown_table(phase30_redesign_queue),
        "",
        "## Phase 31 Redesign Evidence Contract",
        "",
        _markdown_table(phase31_contract_status),
        "",
        _markdown_table(phase31_evidence_domain_status),
        "",
        _markdown_table(phase31_overall_summary),
        "",
        _markdown_table(phase31_replay_gate),
        "",
        _markdown_table(phase31_spec_catalog),
        "",
        _markdown_table(phase31_contract_ledger),
        "",
        "## Phase 32 Contract Evidence Scanner",
        "",
        _markdown_table(phase32_scanner_status),
        "",
        _markdown_table(phase32_overall_summary),
        "",
        _markdown_table(phase32_availability_summary),
        "",
        _markdown_table(phase32_strategy_summary),
        "",
        _markdown_table(phase32_acquisition_queue),
        "",
        _markdown_table(phase32_scan_ledger),
        "",
        "## Phase 33 Broker Evidence Intake",
        "",
        _markdown_table(phase33_file_status),
        "",
        _markdown_table(phase33_test_status),
        "",
        _markdown_table(phase33_overall_summary),
        "",
        _markdown_table(phase33_template_inventory),
        "",
        _markdown_table(phase33_file_validation),
        "",
        _markdown_table(phase33_test_readiness),
        "",
        "## Phase 34 Real Data Multi-Day Readiness",
        "",
        _markdown_table(phase34_day_status),
        "",
        _markdown_table(phase34_symbol_status),
        "",
        _markdown_table(phase34_readiness_summary),
        "",
        _markdown_table(phase34_day_inventory),
        "",
        _markdown_table(phase34_acquisition_plan),
        "",
        _markdown_table(phase34_symbol_day_coverage.head(40)),
        "",
        "## Metric Status",
        "",
        _markdown_table(metric_status),
        "",
        "## Gap Priority",
        "",
        _markdown_table(gap_priority),
        "",
    ]
    return html_doc, "\n".join(md_lines), summary, manifest


def run_dashboard(output_dir: Path, paths: dict[str, Path]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    html_doc, markdown_doc, summary, manifest = build_dashboard(paths)
    (output_dir / "synthetic_l2_validation_dashboard.html").write_text(html_doc, encoding="utf-8")
    (output_dir / "synthetic_l2_validation_dashboard.md").write_text(markdown_doc, encoding="utf-8")
    summary.to_csv(output_dir / "validation_dashboard_summary.csv", index=False)
    (output_dir / "validation_dashboard_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a static SyntheticL2 validation dashboard from Phase 14-17 outputs.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/dashboard"))
    parser.add_argument("--quality", type=Path, default=Path("outputs/phase14/quality_gate_summary.csv"))
    parser.add_argument("--holdout", type=Path, default=Path("outputs/phase14/holdout_generator_realism_summary.csv"))
    parser.add_argument("--realism-gap", type=Path, default=Path("outputs/phase14/realism_acceptance_gap_ledger.csv"))
    parser.add_argument("--lifecycle-risk", type=Path, default=Path("outputs/phase12/full_run_lifecycle_risk_summary.csv"))
    parser.add_argument("--lifecycle-risk-severity", type=Path, default=Path("outputs/phase12/full_run_lifecycle_risk_breach_severity.csv"))
    parser.add_argument("--lifecycle-risk-limit-sensitivity", type=Path, default=Path("outputs/phase12/full_run_lifecycle_risk_limit_sensitivity.csv"))
    parser.add_argument("--risk-acceptance-readiness", type=Path, default=Path("outputs/phase12/full_run_risk_acceptance_readiness.csv"))
    parser.add_argument("--robustness-dimension", type=Path, default=Path("outputs/phase13/robustness_dimension_summary.csv"))
    parser.add_argument("--robustness-gap", type=Path, default=Path("outputs/phase13/robustness_acceptance_gap_ledger.csv"))
    parser.add_argument("--acceptance", type=Path, default=Path("outputs/phase15/strategy_acceptance_summary.csv"))
    parser.add_argument("--blockers", type=Path, default=Path("outputs/phase15/acceptance_blockers.csv"))
    parser.add_argument("--metric-catalog", type=Path, default=Path("outputs/phase16/metric_catalog.csv"))
    parser.add_argument("--predictive", type=Path, default=Path("outputs/phase16/predictive_proxy_diagnostics.csv"))
    parser.add_argument("--predictive-holdout", type=Path, default=Path("outputs/phase16/predictive_holdout_stability_summary.csv"))
    parser.add_argument("--predictive-falsification", type=Path, default=Path("outputs/phase16/predictive_promotion_falsification.csv"))
    parser.add_argument("--predictive-gap", type=Path, default=Path("outputs/phase16/predictive_acceptance_gap_ledger.csv"))
    parser.add_argument("--trading", type=Path, default=Path("outputs/phase16/trading_metric_scoreboard.csv"))
    parser.add_argument("--economic", type=Path, default=Path("outputs/phase16/economic_viability_frontier.csv"))
    parser.add_argument("--risk-adjusted-economic", type=Path, default=Path("outputs/phase16/risk_adjusted_economic_frontier.csv"))
    parser.add_argument("--broker-reconciliation", type=Path, default=Path("outputs/phase16/broker_reconciliation_readiness.csv"))
    parser.add_argument("--economic-reconciliation", type=Path, default=Path("outputs/phase16/economic_reconciliation_strategy_summary.csv"))
    parser.add_argument("--economic-gap", type=Path, default=Path("outputs/phase16/economic_acceptance_gap_ledger.csv"))
    parser.add_argument("--markout", type=Path, default=Path("outputs/phase16/markout_mae_mfe_summary.csv"))
    parser.add_argument("--gaps", type=Path, default=Path("outputs/phase17/implementation_gap_backlog.csv"))
    parser.add_argument("--hardening-queue", type=Path, default=Path("outputs/phase20/acceptance_hardening_queue.csv"))
    parser.add_argument("--hardening-gate-summary", type=Path, default=Path("outputs/phase20/acceptance_hardening_gate_summary.csv"))
    parser.add_argument("--execution-roadmap", type=Path, default=Path("outputs/phase20/acceptance_execution_roadmap.csv"))
    parser.add_argument("--execution-milestones", type=Path, default=Path("outputs/phase20/acceptance_execution_milestones.csv"))
    parser.add_argument("--risk-hardening-plan", type=Path, default=Path("outputs/phase20/risk_hardening_plan.csv"))
    parser.add_argument("--risk-hardening-action-summary", type=Path, default=Path("outputs/phase20/risk_hardening_action_summary.csv"))
    parser.add_argument("--economic-hardening-plan", type=Path, default=Path("outputs/phase20/economic_hardening_plan.csv"))
    parser.add_argument("--economic-hardening-action-summary", type=Path, default=Path("outputs/phase20/economic_hardening_action_summary.csv"))
    parser.add_argument("--predictive-hardening-plan", type=Path, default=Path("outputs/phase20/predictive_hardening_plan.csv"))
    parser.add_argument("--predictive-hardening-action-summary", type=Path, default=Path("outputs/phase20/predictive_hardening_action_summary.csv"))
    parser.add_argument("--robustness-hardening-plan", type=Path, default=Path("outputs/phase20/robustness_hardening_plan.csv"))
    parser.add_argument("--robustness-hardening-action-summary", type=Path, default=Path("outputs/phase20/robustness_hardening_action_summary.csv"))
    parser.add_argument("--realism-hardening-plan", type=Path, default=Path("outputs/phase20/realism_hardening_plan.csv"))
    parser.add_argument("--realism-hardening-action-summary", type=Path, default=Path("outputs/phase20/realism_hardening_action_summary.csv"))
    parser.add_argument("--broker-import-checklist", type=Path, default=Path("outputs/phase20_m01/broker_evidence_import_checklist.csv"))
    parser.add_argument("--broker-evidence-schema", type=Path, default=Path("outputs/phase20_m01/broker_evidence_schema.csv"))
    parser.add_argument("--broker-external-gap-ledger", type=Path, default=Path("outputs/phase20_m01/broker_external_gap_ledger.csv"))
    parser.add_argument("--broker-external-gap-summary", type=Path, default=Path("outputs/phase20_m01/broker_external_gap_summary.csv"))
    parser.add_argument("--broker-reconciliation-test-catalog", type=Path, default=Path("outputs/phase20_m01/broker_reconciliation_test_catalog.csv"))
    parser.add_argument("--strategy-support-criteria", type=Path, default=Path("outputs/phase20_m02/strategy_support_acceptance_criteria.csv"))
    parser.add_argument("--strategy-support-ledger", type=Path, default=Path("outputs/phase20_m02/strategy_support_closure_ledger.csv"))
    parser.add_argument("--strategy-support-gap-summary", type=Path, default=Path("outputs/phase20_m02/strategy_support_gap_summary.csv"))
    parser.add_argument("--strategy-support-decision-summary", type=Path, default=Path("outputs/phase20_m02/strategy_support_decision_summary.csv"))
    parser.add_argument("--predictive-validation-criteria", type=Path, default=Path("outputs/phase20_m03/predictive_validation_acceptance_criteria.csv"))
    parser.add_argument("--predictive-validation-ledger", type=Path, default=Path("outputs/phase20_m03/predictive_validation_ledger.csv"))
    parser.add_argument("--predictive-validation-gap-summary", type=Path, default=Path("outputs/phase20_m03/predictive_validation_gap_summary.csv"))
    parser.add_argument("--predictive-validation-strategy-summary", type=Path, default=Path("outputs/phase20_m03/predictive_validation_strategy_summary.csv"))
    parser.add_argument("--robustness-execution-criteria", type=Path, default=Path("outputs/phase20_m04/robustness_execution_acceptance_criteria.csv"))
    parser.add_argument("--robustness-execution-ledger", type=Path, default=Path("outputs/phase20_m04/robustness_execution_ledger.csv"))
    parser.add_argument("--robustness-execution-gap-summary", type=Path, default=Path("outputs/phase20_m04/robustness_execution_gap_summary.csv"))
    parser.add_argument("--robustness-execution-strategy-summary", type=Path, default=Path("outputs/phase20_m04/robustness_execution_strategy_summary.csv"))
    parser.add_argument("--lifecycle-economic-criteria", type=Path, default=Path("outputs/phase20_m05/lifecycle_economic_acceptance_criteria.csv"))
    parser.add_argument("--lifecycle-economic-ledger", type=Path, default=Path("outputs/phase20_m05/lifecycle_economic_replay_ledger.csv"))
    parser.add_argument("--lifecycle-economic-gap-summary", type=Path, default=Path("outputs/phase20_m05/lifecycle_economic_gap_summary.csv"))
    parser.add_argument("--lifecycle-economic-strategy-summary", type=Path, default=Path("outputs/phase20_m05/lifecycle_economic_strategy_summary.csv"))
    parser.add_argument("--realism-rerun-criteria", type=Path, default=Path("outputs/phase20_m06/realism_rerun_acceptance_criteria.csv"))
    parser.add_argument("--realism-rerun-ledger", type=Path, default=Path("outputs/phase20_m06/realism_rerun_ledger.csv"))
    parser.add_argument("--realism-rerun-gap-summary", type=Path, default=Path("outputs/phase20_m06/realism_rerun_gap_summary.csv"))
    parser.add_argument("--realism-rerun-strategy-summary", type=Path, default=Path("outputs/phase20_m06/realism_rerun_strategy_summary.csv"))
    parser.add_argument("--real-multiday-criteria", type=Path, default=Path("outputs/phase20_m07/real_multiday_acceptance_criteria.csv"))
    parser.add_argument("--real-multiday-ledger", type=Path, default=Path("outputs/phase20_m07/real_multiday_acceptance_ledger.csv"))
    parser.add_argument("--real-multiday-gap-summary", type=Path, default=Path("outputs/phase20_m07/real_multiday_gap_summary.csv"))
    parser.add_argument("--real-multiday-strategy-summary", type=Path, default=Path("outputs/phase20_m07/real_multiday_strategy_summary.csv"))
    parser.add_argument("--stage-a2-criteria", type=Path, default=Path("outputs/stage_a2/capture_diagnostics_acceptance_criteria.csv"))
    parser.add_argument("--stage-a2-schema", type=Path, default=Path("outputs/stage_a2/required_capture_schema.csv"))
    parser.add_argument("--stage-a2-ledger", type=Path, default=Path("outputs/stage_a2/capture_diagnostics_gap_ledger.csv"))
    parser.add_argument("--stage-a2-gap-summary", type=Path, default=Path("outputs/stage_a2/capture_diagnostics_gap_summary.csv"))
    parser.add_argument("--stage-a2-readiness-summary", type=Path, default=Path("outputs/stage_a2/stage_a2_readiness_summary.csv"))
    parser.add_argument("--stage-b1-subset", type=Path, default=Path("outputs/stage_b1/stage_b1_development_subset.csv"))
    parser.add_argument("--stage-b1-criteria", type=Path, default=Path("outputs/stage_b1/stage_b1_structural_criteria.csv"))
    parser.add_argument("--stage-b1-scenario-summary", type=Path, default=Path("outputs/stage_b1/stage_b1_scenario_coverage_summary.csv"))
    parser.add_argument("--stage-b1-check-ledger", type=Path, default=Path("outputs/stage_b1/stage_b1_structural_check_ledger.csv"))
    parser.add_argument("--stage-b2-readiness", type=Path, default=Path("outputs/stage_b2/stage_b2_development_readiness.csv"))
    parser.add_argument("--stage-b2-criteria", type=Path, default=Path("outputs/stage_b2/stage_b2_event_driven_criteria.csv"))
    parser.add_argument("--stage-b2-scenario-selection", type=Path, default=Path("outputs/stage_b2/stage_b2_scenario_selection.csv"))
    parser.add_argument("--stage-b2-dataset-summary", type=Path, default=Path("outputs/stage_b2/stage_b2_dataset_summary.csv"))
    parser.add_argument("--stage-b2-check-ledger", type=Path, default=Path("outputs/stage_b2/stage_b2_proof_check_ledger.csv"))
    parser.add_argument("--stage-c-selected-days", type=Path, default=Path("outputs/stage_c/stage_c_selected_trading_days.csv"))
    parser.add_argument("--stage-c-selected-seeds", type=Path, default=Path("outputs/stage_c/stage_c_selected_seeds.csv"))
    parser.add_argument("--stage-c-dataset-summary", type=Path, default=Path("outputs/stage_c/stage_c_dataset_summary.csv"))
    parser.add_argument("--stage-c-check-ledger", type=Path, default=Path("outputs/stage_c/stage_c_check_ledger.csv"))
    parser.add_argument("--stage-c-strategy-runs", type=Path, default=Path("outputs/stage_c/stage_c_strategy_proxy_run_summary.csv"))
    parser.add_argument("--stage-c-baseline-runs", type=Path, default=Path("outputs/stage_c/stage_c_baseline_proxy_run_summary.csv"))
    parser.add_argument("--stage-d-profile-summary", type=Path, default=Path("outputs/stage_d/stage_d_profile_summary.csv"))
    parser.add_argument("--stage-d-seed-summary", type=Path, default=Path("outputs/stage_d/stage_d_seed_summary.csv"))
    parser.add_argument("--stage-d-data-inventory", type=Path, default=Path("outputs/stage_d/stage_d_data_product_inventory.csv"))
    parser.add_argument("--stage-d-dataset-summary", type=Path, default=Path("outputs/stage_d/stage_d_dataset_summary.csv"))
    parser.add_argument("--stage-d-check-ledger", type=Path, default=Path("outputs/stage_d/stage_d_check_ledger.csv"))
    parser.add_argument("--stage-d-strategy-summary", type=Path, default=Path("outputs/stage_d/stage_d_strategy_proxy_summary.csv"))
    parser.add_argument("--stage-e-criteria", type=Path, default=Path("outputs/stage_e/stage_e_readiness_criteria.csv"))
    parser.add_argument("--stage-e-prerequisite-ledger", type=Path, default=Path("outputs/stage_e/stage_e_prerequisite_ledger.csv"))
    parser.add_argument("--stage-e-gap-summary", type=Path, default=Path("outputs/stage_e/stage_e_gap_summary.csv"))
    parser.add_argument("--stage-e-action-plan", type=Path, default=Path("outputs/stage_e/stage_e_required_action_plan.csv"))
    parser.add_argument("--phase21-decision-rules", type=Path, default=Path("outputs/phase21/decision_rules.csv"))
    parser.add_argument("--phase21-decision-ledger", type=Path, default=Path("outputs/phase21/decision_ledger.csv"))
    parser.add_argument("--phase21-decision-summary", type=Path, default=Path("outputs/phase21/decision_summary.csv"))
    parser.add_argument("--phase22-milestone-catalog", type=Path, default=Path("outputs/phase22/real_data_milestone_catalog.csv"))
    parser.add_argument("--phase22-recalibration-task-ledger", type=Path, default=Path("outputs/phase22/recalibration_task_ledger.csv"))
    parser.add_argument("--phase22-capture-expansion-plan", type=Path, default=Path("outputs/phase22/capture_expansion_plan.csv"))
    parser.add_argument("--phase22-summary", type=Path, default=Path("outputs/phase22/real_data_integration_summary.csv"))
    parser.add_argument("--phase23-risk-register", type=Path, default=Path("outputs/phase23/key_risk_register.csv"))
    parser.add_argument("--phase23-mitigation-ledger", type=Path, default=Path("outputs/phase23/risk_mitigation_ledger.csv"))
    parser.add_argument("--phase23-promotion-path", type=Path, default=Path("outputs/phase23/promotion_path_guardrail.csv"))
    parser.add_argument("--phase23-summary", type=Path, default=Path("outputs/phase23/key_risk_summary.csv"))
    parser.add_argument("--phase25-replay-summary", type=Path, default=Path("outputs/phase25/event_replay_summary.csv"))
    parser.add_argument("--phase25-risk-summary", type=Path, default=Path("outputs/phase25/event_replay_risk_summary.csv"))
    parser.add_argument("--phase25-baseline-comparison", type=Path, default=Path("outputs/phase25/event_replay_baseline_comparison.csv"))
    parser.add_argument("--phase25-overall-summary", type=Path, default=Path("outputs/phase25/event_replay_overall_summary.csv"))
    parser.add_argument("--phase26-variant-catalog", type=Path, default=Path("outputs/phase26/strategy_salvage_variant_catalog.csv"))
    parser.add_argument("--phase26-summary", type=Path, default=Path("outputs/phase26/strategy_salvage_summary.csv"))
    parser.add_argument("--phase26-candidate-summary", type=Path, default=Path("outputs/phase26/strategy_salvage_candidate_summary.csv"))
    parser.add_argument("--phase26-rejection-ledger", type=Path, default=Path("outputs/phase26/strategy_salvage_rejection_ledger.csv"))
    parser.add_argument("--phase26-overall-summary", type=Path, default=Path("outputs/phase26/strategy_salvage_overall_summary.csv"))
    parser.add_argument("--phase27-candidate-catalog", type=Path, default=Path("outputs/phase27/feature_edge_candidate_catalog.csv"))
    parser.add_argument("--phase27-candidate-summary", type=Path, default=Path("outputs/phase27/feature_edge_candidate_summary.csv"))
    parser.add_argument("--phase27-family-summary", type=Path, default=Path("outputs/phase27/feature_edge_family_summary.csv"))
    parser.add_argument("--phase27-rejection-ledger", type=Path, default=Path("outputs/phase27/feature_edge_rejection_ledger.csv"))
    parser.add_argument("--phase27-overall-summary", type=Path, default=Path("outputs/phase27/feature_edge_overall_summary.csv"))
    parser.add_argument("--phase28-feature-label-catalog", type=Path, default=Path("outputs/phase28/feature_label_catalog.csv"))
    parser.add_argument("--phase28-event-label-summary", type=Path, default=Path("outputs/phase28/event_label_summary.csv"))
    parser.add_argument("--phase28-lead-lag-summary", type=Path, default=Path("outputs/phase28/lead_lag_proxy_summary.csv"))
    parser.add_argument("--phase28-strategy-support-summary", type=Path, default=Path("outputs/phase28/strategy_support_upgrade_summary.csv"))
    parser.add_argument("--phase28-overall-summary", type=Path, default=Path("outputs/phase28/richer_event_label_overall_summary.csv"))
    parser.add_argument("--phase29-summary", type=Path, default=Path("outputs/phase29/partial_strategy_proxy_summary.csv"))
    parser.add_argument("--phase29-risk-summary", type=Path, default=Path("outputs/phase29/partial_strategy_proxy_risk_summary.csv"))
    parser.add_argument("--phase29-candidate-summary", type=Path, default=Path("outputs/phase29/partial_strategy_proxy_candidate_summary.csv"))
    parser.add_argument("--phase29-overall-summary", type=Path, default=Path("outputs/phase29/partial_strategy_proxy_overall_summary.csv"))
    parser.add_argument("--phase30-decision-ledger", type=Path, default=Path("outputs/phase30/strategy_family_decision_ledger.csv"))
    parser.add_argument("--phase30-execution-evidence", type=Path, default=Path("outputs/phase30/strategy_family_execution_evidence_summary.csv"))
    parser.add_argument("--phase30-redesign-queue", type=Path, default=Path("outputs/phase30/strategy_redesign_queue.csv"))
    parser.add_argument("--phase30-overall-summary", type=Path, default=Path("outputs/phase30/strategy_rejection_or_redesign_overall_summary.csv"))
    parser.add_argument("--phase31-spec-catalog", type=Path, default=Path("outputs/phase31/strategy_redesign_spec_catalog.csv"))
    parser.add_argument("--phase31-contract-ledger", type=Path, default=Path("outputs/phase31/redesign_evidence_contract_ledger.csv"))
    parser.add_argument("--phase31-replay-gate", type=Path, default=Path("outputs/phase31/replay_expansion_gate.csv"))
    parser.add_argument("--phase31-overall-summary", type=Path, default=Path("outputs/phase31/redesign_evidence_contract_overall_summary.csv"))
    parser.add_argument("--phase32-scan-ledger", type=Path, default=Path("outputs/phase32/contract_evidence_scan_ledger.csv"))
    parser.add_argument("--phase32-availability-summary", type=Path, default=Path("outputs/phase32/evidence_availability_summary.csv"))
    parser.add_argument("--phase32-acquisition-queue", type=Path, default=Path("outputs/phase32/evidence_acquisition_queue.csv"))
    parser.add_argument("--phase32-strategy-summary", type=Path, default=Path("outputs/phase32/strategy_evidence_scan_summary.csv"))
    parser.add_argument("--phase32-overall-summary", type=Path, default=Path("outputs/phase32/contract_evidence_scan_overall_summary.csv"))
    parser.add_argument("--phase33-template-inventory", type=Path, default=Path("outputs/phase33/broker_evidence_template_inventory.csv"))
    parser.add_argument("--phase33-file-validation", type=Path, default=Path("outputs/phase33/broker_evidence_file_validation.csv"))
    parser.add_argument("--phase33-test-readiness", type=Path, default=Path("outputs/phase33/broker_reconciliation_test_readiness.csv"))
    parser.add_argument("--phase33-overall-summary", type=Path, default=Path("outputs/phase33/broker_evidence_intake_overall_summary.csv"))
    parser.add_argument("--phase34-symbol-day-coverage", type=Path, default=Path("outputs/phase34/symbol_day_real_data_coverage.csv"))
    parser.add_argument("--phase34-day-inventory", type=Path, default=Path("outputs/phase34/real_data_day_inventory.csv"))
    parser.add_argument("--phase34-readiness-summary", type=Path, default=Path("outputs/phase34/multiday_real_data_readiness_summary.csv"))
    parser.add_argument("--phase34-acquisition-plan", type=Path, default=Path("outputs/phase34/multiday_real_data_acquisition_plan.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "quality": args.quality,
        "holdout": args.holdout,
        "realism_gap": args.realism_gap,
        "lifecycle_risk": args.lifecycle_risk,
        "lifecycle_risk_severity": args.lifecycle_risk_severity,
        "lifecycle_risk_limit_sensitivity": args.lifecycle_risk_limit_sensitivity,
        "risk_acceptance_readiness": args.risk_acceptance_readiness,
        "robustness_dimension": args.robustness_dimension,
        "robustness_gap": args.robustness_gap,
        "acceptance": args.acceptance,
        "blockers": args.blockers,
        "metric_catalog": args.metric_catalog,
        "predictive": args.predictive,
        "predictive_holdout": args.predictive_holdout,
        "predictive_falsification": args.predictive_falsification,
        "predictive_gap": args.predictive_gap,
        "trading": args.trading,
        "economic": args.economic,
        "risk_adjusted_economic": args.risk_adjusted_economic,
        "broker_reconciliation": args.broker_reconciliation,
        "economic_reconciliation": args.economic_reconciliation,
        "economic_gap": args.economic_gap,
        "markout": args.markout,
        "gaps": args.gaps,
        "hardening_queue": args.hardening_queue,
        "hardening_gate_summary": args.hardening_gate_summary,
        "execution_roadmap": args.execution_roadmap,
        "execution_milestones": args.execution_milestones,
        "risk_hardening_plan": args.risk_hardening_plan,
        "risk_hardening_action_summary": args.risk_hardening_action_summary,
        "economic_hardening_plan": args.economic_hardening_plan,
        "economic_hardening_action_summary": args.economic_hardening_action_summary,
        "predictive_hardening_plan": args.predictive_hardening_plan,
        "predictive_hardening_action_summary": args.predictive_hardening_action_summary,
        "robustness_hardening_plan": args.robustness_hardening_plan,
        "robustness_hardening_action_summary": args.robustness_hardening_action_summary,
        "realism_hardening_plan": args.realism_hardening_plan,
        "realism_hardening_action_summary": args.realism_hardening_action_summary,
        "broker_import_checklist": args.broker_import_checklist,
        "broker_evidence_schema": args.broker_evidence_schema,
        "broker_external_gap_ledger": args.broker_external_gap_ledger,
        "broker_external_gap_summary": args.broker_external_gap_summary,
        "broker_reconciliation_test_catalog": args.broker_reconciliation_test_catalog,
        "strategy_support_criteria": args.strategy_support_criteria,
        "strategy_support_ledger": args.strategy_support_ledger,
        "strategy_support_gap_summary": args.strategy_support_gap_summary,
        "strategy_support_decision_summary": args.strategy_support_decision_summary,
        "predictive_validation_criteria": args.predictive_validation_criteria,
        "predictive_validation_ledger": args.predictive_validation_ledger,
        "predictive_validation_gap_summary": args.predictive_validation_gap_summary,
        "predictive_validation_strategy_summary": args.predictive_validation_strategy_summary,
        "robustness_execution_criteria": args.robustness_execution_criteria,
        "robustness_execution_ledger": args.robustness_execution_ledger,
        "robustness_execution_gap_summary": args.robustness_execution_gap_summary,
        "robustness_execution_strategy_summary": args.robustness_execution_strategy_summary,
        "lifecycle_economic_criteria": args.lifecycle_economic_criteria,
        "lifecycle_economic_ledger": args.lifecycle_economic_ledger,
        "lifecycle_economic_gap_summary": args.lifecycle_economic_gap_summary,
        "lifecycle_economic_strategy_summary": args.lifecycle_economic_strategy_summary,
        "realism_rerun_criteria": args.realism_rerun_criteria,
        "realism_rerun_ledger": args.realism_rerun_ledger,
        "realism_rerun_gap_summary": args.realism_rerun_gap_summary,
        "realism_rerun_strategy_summary": args.realism_rerun_strategy_summary,
        "real_multiday_criteria": args.real_multiday_criteria,
        "real_multiday_ledger": args.real_multiday_ledger,
        "real_multiday_gap_summary": args.real_multiday_gap_summary,
        "real_multiday_strategy_summary": args.real_multiday_strategy_summary,
        "stage_a2_criteria": args.stage_a2_criteria,
        "stage_a2_schema": args.stage_a2_schema,
        "stage_a2_ledger": args.stage_a2_ledger,
        "stage_a2_gap_summary": args.stage_a2_gap_summary,
        "stage_a2_readiness_summary": args.stage_a2_readiness_summary,
        "stage_b1_subset": args.stage_b1_subset,
        "stage_b1_criteria": args.stage_b1_criteria,
        "stage_b1_scenario_summary": args.stage_b1_scenario_summary,
        "stage_b1_check_ledger": args.stage_b1_check_ledger,
        "stage_b2_readiness": args.stage_b2_readiness,
        "stage_b2_criteria": args.stage_b2_criteria,
        "stage_b2_scenario_selection": args.stage_b2_scenario_selection,
        "stage_b2_dataset_summary": args.stage_b2_dataset_summary,
        "stage_b2_check_ledger": args.stage_b2_check_ledger,
        "stage_c_selected_days": args.stage_c_selected_days,
        "stage_c_selected_seeds": args.stage_c_selected_seeds,
        "stage_c_dataset_summary": args.stage_c_dataset_summary,
        "stage_c_check_ledger": args.stage_c_check_ledger,
        "stage_c_strategy_runs": args.stage_c_strategy_runs,
        "stage_c_baseline_runs": args.stage_c_baseline_runs,
        "stage_d_profile_summary": args.stage_d_profile_summary,
        "stage_d_seed_summary": args.stage_d_seed_summary,
        "stage_d_data_inventory": args.stage_d_data_inventory,
        "stage_d_dataset_summary": args.stage_d_dataset_summary,
        "stage_d_check_ledger": args.stage_d_check_ledger,
        "stage_d_strategy_summary": args.stage_d_strategy_summary,
        "stage_e_criteria": args.stage_e_criteria,
        "stage_e_prerequisite_ledger": args.stage_e_prerequisite_ledger,
        "stage_e_gap_summary": args.stage_e_gap_summary,
        "stage_e_action_plan": args.stage_e_action_plan,
        "phase21_decision_rules": args.phase21_decision_rules,
        "phase21_decision_ledger": args.phase21_decision_ledger,
        "phase21_decision_summary": args.phase21_decision_summary,
        "phase22_milestone_catalog": args.phase22_milestone_catalog,
        "phase22_recalibration_task_ledger": args.phase22_recalibration_task_ledger,
        "phase22_capture_expansion_plan": args.phase22_capture_expansion_plan,
        "phase22_summary": args.phase22_summary,
        "phase23_risk_register": args.phase23_risk_register,
        "phase23_mitigation_ledger": args.phase23_mitigation_ledger,
        "phase23_promotion_path": args.phase23_promotion_path,
        "phase23_summary": args.phase23_summary,
        "phase25_replay_summary": args.phase25_replay_summary,
        "phase25_risk_summary": args.phase25_risk_summary,
        "phase25_baseline_comparison": args.phase25_baseline_comparison,
        "phase25_overall_summary": args.phase25_overall_summary,
        "phase26_variant_catalog": args.phase26_variant_catalog,
        "phase26_summary": args.phase26_summary,
        "phase26_candidate_summary": args.phase26_candidate_summary,
        "phase26_rejection_ledger": args.phase26_rejection_ledger,
        "phase26_overall_summary": args.phase26_overall_summary,
        "phase27_candidate_catalog": args.phase27_candidate_catalog,
        "phase27_candidate_summary": args.phase27_candidate_summary,
        "phase27_family_summary": args.phase27_family_summary,
        "phase27_rejection_ledger": args.phase27_rejection_ledger,
        "phase27_overall_summary": args.phase27_overall_summary,
        "phase28_feature_label_catalog": args.phase28_feature_label_catalog,
        "phase28_event_label_summary": args.phase28_event_label_summary,
        "phase28_lead_lag_summary": args.phase28_lead_lag_summary,
        "phase28_strategy_support_summary": args.phase28_strategy_support_summary,
        "phase28_overall_summary": args.phase28_overall_summary,
        "phase29_summary": args.phase29_summary,
        "phase29_risk_summary": args.phase29_risk_summary,
        "phase29_candidate_summary": args.phase29_candidate_summary,
        "phase29_overall_summary": args.phase29_overall_summary,
        "phase30_decision_ledger": args.phase30_decision_ledger,
        "phase30_execution_evidence": args.phase30_execution_evidence,
        "phase30_redesign_queue": args.phase30_redesign_queue,
        "phase30_overall_summary": args.phase30_overall_summary,
        "phase31_spec_catalog": args.phase31_spec_catalog,
        "phase31_contract_ledger": args.phase31_contract_ledger,
        "phase31_replay_gate": args.phase31_replay_gate,
        "phase31_overall_summary": args.phase31_overall_summary,
        "phase32_scan_ledger": args.phase32_scan_ledger,
        "phase32_availability_summary": args.phase32_availability_summary,
        "phase32_acquisition_queue": args.phase32_acquisition_queue,
        "phase32_strategy_summary": args.phase32_strategy_summary,
        "phase32_overall_summary": args.phase32_overall_summary,
        "phase33_template_inventory": args.phase33_template_inventory,
        "phase33_file_validation": args.phase33_file_validation,
        "phase33_test_readiness": args.phase33_test_readiness,
        "phase33_overall_summary": args.phase33_overall_summary,
        "phase34_symbol_day_coverage": args.phase34_symbol_day_coverage,
        "phase34_day_inventory": args.phase34_day_inventory,
        "phase34_readiness_summary": args.phase34_readiness_summary,
        "phase34_acquisition_plan": args.phase34_acquisition_plan,
    }
    run_dashboard(args.output_dir, paths)


if __name__ == "__main__":
    main()
