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
            scenario_ids="current_workspace_phase14_phase15_phase16_phase17_phase20_phase20_m01_evidence",
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
    }
    run_dashboard(args.output_dir, paths)


if __name__ == "__main__":
    main()
