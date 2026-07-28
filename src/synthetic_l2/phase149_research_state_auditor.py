from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_OUTPUT_DIR = Path("outputs/phase149")
DEFAULT_OUTPUTS_ROOT = Path("outputs")
DEFAULT_SCRIPTS_ROOT = Path("scripts")
DEFAULT_PLAN_PATH = Path("Plan/zerodha_l2_synthetic_data_strategy_validation_plan.md")


PHASE_RE = re.compile(r"phase(\d+)", re.IGNORECASE)


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(path: Path, metric: str, default: Any = None) -> Any:
    frame = read_csv(path)
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    value = rows.iloc[0]
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def discover_script_phases(scripts_root: Path) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for path in sorted(scripts_root.glob("run_phase*.*")):
        match = PHASE_RE.search(path.name)
        if not match:
            continue
        rows.append(
            {
                "phase": int(match.group(1)),
                "runner": str(path),
                "runner_exists": True,
                "runner_suffix": path.suffix.lower(),
            }
        )
    return pd.DataFrame(rows)


def discover_output_phases(outputs_root: Path) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if not outputs_root.exists():
        return pd.DataFrame(columns=["phase", "output_dir", "output_exists", "file_count", "acceptance_files", "manifest_files"])
    for directory in sorted(path for path in outputs_root.iterdir() if path.is_dir()):
        match = PHASE_RE.search(directory.name)
        if not match:
            continue
        files = sorted(path for path in directory.rglob("*") if path.is_file())
        acceptance = [path for path in files if "acceptance_summary" in path.name]
        manifests = [path for path in files if path.name.endswith("_manifest.json") or path.name.endswith("manifest.json")]
        rows.append(
            {
                "phase": int(match.group(1)),
                "output_dir": str(directory),
                "output_exists": True,
                "file_count": int(len(files)),
                "acceptance_files": "|".join(str(path) for path in acceptance),
                "manifest_files": "|".join(str(path) for path in manifests),
                "is_smoke_or_partial": bool("smoke" in directory.name.lower() or "partial" in directory.name.lower()),
            }
        )
    return pd.DataFrame(rows)


def phase_status_from_metrics(phase: int) -> dict[str, Any]:
    paths = {
        52: Path("outputs/phase52/dense_replay_acceptance_summary_partial.csv"),
        96: Path("outputs/phase115/subruns/phase96/real_anchor_panel_builder_acceptance_summary.csv"),
        110: Path("outputs/phase115/subruns/phase110/phase110_multiday_replay_unlock_acceptance_summary.csv"),
        115: Path("outputs/phase115/phase115_real_panel_refresh_acceptance_summary.csv"),
        132: Path("outputs/phase132/phase132_deep_book_feature_diagnostics_acceptance_summary.csv"),
        133: Path("outputs/phase133/phase133_passive_execution_model_upgrade_acceptance_summary.csv"),
        136: Path("outputs/phase136/phase136_deep_book_verdict_acceptance_summary.csv"),
        142: Path("outputs/phase142/phase142_local_real_l2_download_verifier_acceptance_summary.csv"),
        143: Path("outputs/phase143/phase143_real_l2_two_date_preflight_acceptance_summary.csv"),
        145: Path("outputs/phase145/phase145_real_l2_post_download_refresh_acceptance_summary.csv"),
        146: Path("outputs/phase146/phase146_real_anchor_minimum_unlock_audit_acceptance_summary.csv"),
        147: Path("outputs/phase147/phase147_azcopy_download_intake_audit_acceptance_summary.csv"),
        148: Path("outputs/phase148/phase148_real_l2_download_refresh_workflow_acceptance_summary.csv"),
        171: Path("outputs/phase171/phase171_external_orderflow_source_acceptance_summary.csv"),
        172: Path("outputs/phase172/phase172_real_l2_receive_flow_availability_acceptance_summary.csv"),
        173: Path("outputs/phase173/phase173_real_l2_download_credential_preflight_acceptance_summary.csv"),
        174: Path("outputs/phase174/phase174_secure_real_l2_download_orchestrator_acceptance_summary.csv"),
        175: Path("outputs/phase175/phase175_receive_flow_feature_schema_precommit_acceptance_summary.csv"),
        176: Path("outputs/phase176/phase176_receive_flow_feature_materializer_acceptance_summary.csv"),
        177: Path("outputs/phase177/phase177_receive_flow_feature_quality_audit_acceptance_summary.csv"),
        178: Path("outputs/phase178/phase178_receive_flow_feature_handoff_precommit_acceptance_summary.csv"),
        179: Path("outputs/phase179/phase179_strategy_family_precommit_acceptance_summary.csv"),
        180: Path("outputs/phase180/phase180_cost_latency_label_precommit_acceptance_summary.csv"),
        181: Path("outputs/phase181/phase181_label_materialization_acceptance_summary.csv"),
        182: Path("outputs/phase182/phase182_label_quality_leakage_audit_acceptance_summary.csv"),
        183: Path("outputs/phase183/phase183_replay_readiness_precommit_acceptance_summary.csv"),
        184: Path("outputs/phase184/phase184_train_validation_replay_dry_run_acceptance_summary.csv"),
        185: Path("outputs/phase185/phase185_validation_replay_interpretation_acceptance_summary.csv"),
        186: Path("outputs/phase186/phase186_cost_aware_family_closure_acceptance_summary.csv"),
        187: Path("outputs/phase187/phase187_cost_aware_sparse_candidate_acceptance_summary.csv"),
        188: Path("outputs/phase188/phase188_sparse_candidate_interpretation_acceptance_summary.csv"),
        189: Path("outputs/phase189/phase189_test_replay_precommit_decision_acceptance_summary.csv"),
        190: Path("outputs/phase190/phase190_validation_breadth_or_diagnostic_test_spec_acceptance_summary.csv"),
        191: Path("outputs/phase191/phase191_diagnostic_test_replay_precommit_acceptance_summary.csv"),
        192: Path("outputs/phase192/phase192_real_validation_date_download_acceptance_summary.csv"),
        193: Path("outputs/phase193/phase193_validation_breadth_extension_acceptance_summary.csv"),
        194: Path("outputs/phase194/phase194_sparse_candidate_fragility_acceptance_summary.csv"),
        195: Path("outputs/phase195/phase195_receive_flow_redesign_candidate_acceptance_summary.csv"),
        196: Path("outputs/phase196/phase196_expanded_feature_model_acceptance_summary.csv"),
        197: Path("outputs/phase197/phase197_non_receive_flow_feature_acceptance_summary.csv"),
        198: Path("outputs/phase198/phase198_context_model_acceptance_summary.csv"),
        199: Path("outputs/phase199/phase199_branch_decision_acceptance_summary.csv"),
        200: Path("outputs/phase200/phase200_material_new_hypothesis_acceptance_summary.csv"),
        201: Path("outputs/phase201/phase201_stage01_acceptance_summary.csv"),
        202: Path("outputs/phase202/phase202_passive_feature_redesign_acceptance_summary.csv"),
        203: Path("outputs/phase203/phase203_redesigned_passive_label_acceptance_summary.csv"),
        204: Path("outputs/phase204/phase204_passive_redesign_closure_acceptance_summary.csv"),
        205: Path("outputs/phase205/phase205_material_new_source_acceptance_summary.csv"),
        206: Path("outputs/phase206/phase206_nonoverlap_feature_acceptance_summary.csv"),
        207: Path("outputs/phase207/phase207_feature_matrix_acceptance_summary.csv"),
    }
    path = paths.get(phase)
    if path is None or not path.exists():
        return {}
    if phase == 52:
        return {
            "branch": "dense_synthetic_replay",
            "state": "partial_or_smoke_artifacts_present",
            "strategy_replay_allowed": 0,
            "next_action": "do_not_promote_partial_dense_replay_without_acceptance_gate",
        }
    if phase == 132:
        return {
            "branch": "top_five_depth_passive",
            "state": "closed_kill_switch",
            "kill_switch_fired": as_int(metric_value(path, "phase132_kill_switch_fired", 0)),
            "surviving_feature_rows": as_int(metric_value(path, "phase132_surviving_feature_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase132_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase132_next_best_action", ""),
        }
    if phase == 133:
        return {
            "branch": "top_five_depth_passive",
            "state": "execution_contract_pinned_phase134_closed",
            "hard_gate_pass_rows": as_int(metric_value(path, "phase133_hard_gate_pass_rows", 0)),
            "phase134_open_allowed": as_int(metric_value(path, "phase133_phase134_open_allowed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase133_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase133_next_best_action", ""),
        }
    if phase == 136:
        return {
            "branch": "top_five_depth_passive",
            "state": "closed_clean_falsification",
            "outcome": metric_value(path, "phase136_outcome", ""),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase136_hard_gate_pass_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase136_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase136_next_best_action", ""),
        }
    if phase in {96, 110, 115, 142, 143, 145, 146, 147, 148}:
        ready_days = (
            metric_value(path, f"phase{phase}_ready_real_anchor_days", None)
            or metric_value(path, f"phase{phase}_phase115_ready_real_anchor_days", None)
            or metric_value(path, f"phase{phase}_phase110_ready_real_anchor_days", None)
            or metric_value(path, "phase110_ready_real_anchor_days", None)
            or metric_value(path, "phase96_ready_anchor_days", None)
        )
        days_needed = (
            metric_value(path, f"phase{phase}_days_needed_for_min", None)
            or metric_value(path, f"phase{phase}_phase146_days_needed_for_min", None)
            or metric_value(path, "phase110_days_needed_for_min", None)
        )
        strategy_allowed = (
            metric_value(path, f"phase{phase}_strategy_replay_allowed", None)
            or metric_value(path, f"phase{phase}_replay_unlock_allowed", None)
            or metric_value(path, "phase110_strategy_replay_allowed", None)
            or 0
        )
        return {
            "branch": "real_l2_anchor_gate",
            "state": "gated_waiting_for_more_real_anchor_days",
            "ready_real_anchor_days": as_int(ready_days, -1) if ready_days is not None else "",
            "days_needed_for_min": as_int(days_needed, -1) if days_needed is not None else "",
            "strategy_replay_allowed": as_int(strategy_allowed, 0),
            "next_action": metric_value(path, f"phase{phase}_next_best_action", ""),
        }
    if phase == 171:
        return {
            "branch": "real_receive_flow_source",
            "state": "source_contract_declared_no_replay",
            "selected_source_id": metric_value(path, "phase171_selected_source_id", ""),
            "source_contract_rows": as_int(metric_value(path, "phase171_source_contract_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase171_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase171_next_best_action", ""),
        }
    if phase == 172:
        return {
            "branch": "real_receive_flow_source",
            "state": "local_receive_flow_structural_ready_but_day_count_gated",
            "ready_receive_flow_dates": as_int(metric_value(path, "phase172_ready_receive_flow_dates", 0)),
            "additional_dates_needed": as_int(metric_value(path, "phase172_additional_dates_needed", 0)),
            "hard_gate_pass_rows": as_int(metric_value(path, "phase172_hard_gate_pass_rows", 0)),
            "unlock_gate_pass_rows": as_int(metric_value(path, "phase172_unlock_gate_pass_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase172_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase172_next_best_action", ""),
        }
    if phase == 173:
        download_ready = as_int(metric_value(path, "phase173_download_ready_now", 0))
        return {
            "branch": "real_receive_flow_download_gate",
            "state": "download_preflight_ready" if download_ready else "download_preflight_waiting_for_sas_or_key_or_tls_fix",
            "download_ready_now": download_ready,
            "additional_dates_needed": as_int(metric_value(path, "phase173_additional_dates_needed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase173_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase173_next_best_action", ""),
        }
    if phase == 174:
        download_ran = as_int(metric_value(path, "phase174_download_ran", 0))
        return {
            "branch": "real_receive_flow_download_gate",
            "state": "secure_download_executed" if download_ran else "secure_download_skipped_no_credential",
            "download_ran": download_ran,
            "additional_dates_needed": as_int(metric_value(path, "phase174_phase172_additional_dates_needed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase174_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase174_next_best_action", ""),
        }
    if phase == 175:
        activation_ready = as_int(metric_value(path, "phase175_activation_ready", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "receive_flow_feature_schema_activation_ready" if activation_ready else "receive_flow_feature_schema_precommitted_gated",
            "feature_schema_rows": as_int(metric_value(path, "phase175_feature_schema_rows", 0)),
            "activation_ready": activation_ready,
            "additional_dates_needed": as_int(metric_value(path, "phase175_additional_dates_needed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase175_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase175_next_best_action", ""),
        }
    if phase == 176:
        features_materialized = as_int(metric_value(path, "phase176_features_materialized", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "receive_flow_feature_materializer_ready_gated" if features_materialized == 0 else "receive_flow_features_materialized_no_replay",
            "features_materialized": features_materialized,
            "activation_ready": as_int(metric_value(path, "phase176_activation_ready", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase176_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase176_next_best_action", ""),
        }
    if phase == 177:
        audit_ran = as_int(metric_value(path, "phase177_feature_quality_audit_ran", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "receive_flow_feature_quality_audit_scaffold_gated" if audit_ran == 0 else "receive_flow_feature_quality_audited_no_replay",
            "feature_quality_audit_ran": audit_ran,
            "quality_check_rows": as_int(metric_value(path, "phase177_quality_check_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase177_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase177_next_best_action", ""),
        }
    if phase == 178:
        handoff_ready = as_int(metric_value(path, "phase178_handoff_ready", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "receive_flow_feature_handoff_precommitted_no_replay" if handoff_ready else "receive_flow_feature_handoff_gated",
            "handoff_ready": handoff_ready,
            "handoff_feature_rows": as_int(metric_value(path, "phase178_handoff_feature_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase178_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase178_next_best_action", ""),
        }
    if phase == 179:
        precommit_ready = as_int(metric_value(path, "phase179_precommit_ready", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "strategy_family_precommitted_no_replay" if precommit_ready else "strategy_family_precommit_gated",
            "precommit_ready": precommit_ready,
            "strategy_family_rows": as_int(metric_value(path, "phase179_strategy_family_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase179_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase179_next_best_action", ""),
        }
    if phase == 180:
        precommit_ready = as_int(metric_value(path, "phase180_precommit_ready", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "cost_latency_label_precommitted_no_replay" if precommit_ready else "cost_latency_label_precommit_gated",
            "precommit_ready": precommit_ready,
            "label_family_rows": as_int(metric_value(path, "phase180_label_family_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase180_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase180_next_best_action", ""),
        }
    if phase == 181:
        labels_materialized = as_int(metric_value(path, "phase181_labels_materialized", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "labels_materialized_no_replay" if labels_materialized else "label_materialization_gated",
            "labels_materialized": labels_materialized,
            "label_rows": as_int(metric_value(path, "phase181_label_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase181_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase181_next_best_action", ""),
        }
    if phase == 182:
        audit_pass = as_int(metric_value(path, "phase182_label_quality_leakage_audit_pass", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "label_quality_leakage_audited_no_replay" if audit_pass else "label_quality_leakage_audit_gated",
            "label_quality_leakage_audit_pass": audit_pass,
            "partition_audit_rows": as_int(metric_value(path, "phase182_partition_audit_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase182_strategy_replay_allowed", 0)),
            "next_action": metric_value(path, "phase182_next_best_action", ""),
        }
    if phase == 183:
        readiness = as_int(metric_value(path, "phase183_replay_readiness_precommitted", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "replay_readiness_precommitted_no_pnl" if readiness else "replay_readiness_precommit_gated",
            "replay_readiness_precommitted": readiness,
            "strategy_replay_allowed": as_int(metric_value(path, "phase183_strategy_replay_allowed", 0)),
            "pnl_allowed": as_int(metric_value(path, "phase183_pnl_allowed", 0)),
            "next_action": metric_value(path, "phase183_next_best_action", ""),
        }
    if phase == 184:
        dry_run_complete = as_int(metric_value(path, "phase184_train_validation_dry_run_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "train_validation_replay_dry_run_complete_no_test_no_promotion" if dry_run_complete else "train_validation_replay_dry_run_gated",
            "train_validation_dry_run_complete": dry_run_complete,
            "strategy_replay_dry_run_performed": as_int(metric_value(path, "phase184_strategy_replay_dry_run_performed", 0)),
            "test_rows_used": as_int(metric_value(path, "phase184_test_rows_used", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase184_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase184_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase184_next_best_action", ""),
        }
    if phase == 185:
        interpretation_complete = as_int(metric_value(path, "phase185_validation_interpretation_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "validation_interpretation_cost_dominated_no_test_no_promotion" if interpretation_complete else "validation_interpretation_gated",
            "validation_interpretation_complete": interpretation_complete,
            "cost_dominates_validation_edge": as_int(metric_value(path, "phase185_cost_dominates_validation_edge", 0)),
            "test_rows_used": as_int(metric_value(path, "phase185_test_rows_used", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase185_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase185_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase185_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase185_next_best_action", ""),
        }
    if phase == 186:
        family_set_closed = as_int(metric_value(path, "phase186_current_family_set_closed", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "current_family_set_closed_cost_aware_redesign_pending" if family_set_closed else "family_closure_gated",
            "current_family_set_closed": family_set_closed,
            "reuse_without_redesign_allowed": as_int(metric_value(path, "phase186_reuse_without_redesign_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase186_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase186_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase186_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase186_next_best_action", ""),
        }
    if phase == 187:
        candidate_complete = as_int(metric_value(path, "phase187_cost_aware_sparse_candidate_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "cost_aware_sparse_candidate_validation_interpretation_pending" if candidate_complete else "cost_aware_sparse_candidate_gated",
            "cost_aware_sparse_candidate_complete": candidate_complete,
            "validation_positive_all_profiles": as_int(metric_value(path, "phase187_validation_positive_all_profiles", 0)),
            "test_rows_used": as_int(metric_value(path, "phase187_test_rows_used", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase187_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase187_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase187_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase187_next_best_action", ""),
        }
    if phase == 188:
        interpretation_complete = as_int(metric_value(path, "phase188_interpretation_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "sparse_candidate_interpreted_phase189_decision_pending" if interpretation_complete else "sparse_candidate_interpretation_gated",
            "sparse_candidate_interpretation_complete": interpretation_complete,
            "breadth_warning": as_int(metric_value(path, "phase188_breadth_warning", 0)),
            "date_count_warning": as_int(metric_value(path, "phase188_date_count_warning", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase188_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase188_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase188_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase188_next_best_action", ""),
        }
    if phase == 189:
        decision_complete = as_int(metric_value(path, "phase189_decision_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "test_replay_deferred_validation_breadth_pending" if decision_complete else "test_replay_precommit_decision_gated",
            "test_precommit_decision_complete": decision_complete,
            "untouched_test_replay_precommit_allowed": as_int(metric_value(path, "phase189_untouched_test_replay_precommit_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase189_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase189_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase189_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase189_next_best_action", ""),
        }
    if phase == 190:
        decision_complete = as_int(metric_value(path, "phase190_decision_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "diagnostic_test_spec_written_validation_breadth_pending" if decision_complete else "validation_breadth_or_diagnostic_spec_gated",
            "phase190_decision_complete": decision_complete,
            "additional_validation_breadth_available_now": as_int(metric_value(path, "phase190_additional_validation_breadth_available_now", 0)),
            "may_relabel_test_as_validation": as_int(metric_value(path, "phase190_may_relabel_test_as_validation", 0)),
            "test_replay_execution": as_int(metric_value(path, "phase190_test_replay_execution", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase190_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase190_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase190_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase190_next_best_action", ""),
        }
    if phase == 191:
        precommit_complete = as_int(metric_value(path, "phase191_diagnostic_test_precommit_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "diagnostic_test_replay_precommitted_no_execution" if precommit_complete else "diagnostic_test_replay_precommit_gated",
            "diagnostic_test_precommit_complete": precommit_complete,
            "test_replay_execution": as_int(metric_value(path, "phase191_test_replay_execution", 0)),
            "test_result_allowed": as_int(metric_value(path, "phase191_test_result_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase191_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase191_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase191_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase191_next_best_action", ""),
        }
    if phase == 192:
        failed = as_int(metric_value(path, "phase192_failed_files_or_dates", 0))
        downloaded = as_int(metric_value(path, "phase192_downloaded_files", 0))
        skipped = as_int(metric_value(path, "phase192_skipped_existing_files", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "real_validation_date_downloaded_no_test" if failed == 0 and (downloaded + skipped) > 0 else "real_validation_date_download_gated",
            "real_validation_download_complete": int(failed == 0 and (downloaded + skipped) > 0),
            "test_replay_execution": as_int(metric_value(path, "phase192_test_replay_execution", 0)),
            "test_result_allowed": as_int(metric_value(path, "phase192_test_result_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase192_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase192_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase192_next_best_action", ""),
        }
    if phase == 193:
        complete = as_int(metric_value(path, "phase193_validation_breadth_extension_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "validation_breadth_extended_mixed_negative_by_date_no_test" if complete else "validation_breadth_extension_gated",
            "validation_breadth_extension_complete": complete,
            "extension_validation_dates": metric_value(path, "phase193_extension_validation_dates", ""),
            "min_profile_net_bps_proxy_mean": metric_value(path, "phase193_min_profile_net_bps_proxy_mean", ""),
            "breadth_warning": as_int(metric_value(path, "phase193_breadth_warning", 0)),
            "date_count_warning": as_int(metric_value(path, "phase193_date_count_warning", 0)),
            "test_replay_execution": as_int(metric_value(path, "phase193_test_replay_execution", 0)),
            "test_result_allowed": as_int(metric_value(path, "phase193_test_result_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase193_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase193_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase193_next_best_action", ""),
        }
    if phase == 194:
        complete = as_int(metric_value(path, "phase194_fragility_decision_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "frozen_sparse_candidate_closed_for_test_replay_redesign_required" if complete else "sparse_candidate_fragility_decision_gated",
            "fragility_decision_complete": complete,
            "extension_validation_dates": metric_value(path, "phase194_extension_validation_dates", ""),
            "all_extension_profile_dates_negative": as_int(metric_value(path, "phase194_all_extension_profile_dates_negative", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase194_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase194_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase194_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase194_next_best_action", ""),
        }
    if phase == 195:
        complete = as_int(metric_value(path, "phase195_redesign_search_complete", 0))
        passing = as_int(metric_value(path, "phase195_passing_extension_gate_candidates", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "redesign_search_no_extension_gate_survivor_no_test" if complete and passing == 0 else "redesign_search_candidate_precommit_pending" if complete else "redesign_search_gated",
            "redesign_search_complete": complete,
            "passing_extension_gate_candidates": passing,
            "best_candidate_id": metric_value(path, "phase195_best_candidate_id", ""),
            "best_min_extension_net_bps": metric_value(path, "phase195_best_min_extension_net_bps", ""),
            "best_date_positive_fraction": metric_value(path, "phase195_best_date_positive_fraction", ""),
            "best_symbol_positive_fraction": metric_value(path, "phase195_best_symbol_positive_fraction", ""),
            "test_replay_allowed_next": as_int(metric_value(path, "phase195_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase195_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase195_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase195_next_best_action", ""),
        }
    if phase == 196:
        complete = as_int(metric_value(path, "phase196_expanded_model_search_complete", 0))
        passing = as_int(metric_value(path, "phase196_passing_extension_gate_models", 0))
        selected = as_int(metric_value(path, "phase196_train_selected_model_rows", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "expanded_feature_model_search_no_train_survivor_no_test" if complete and selected == 0 else "expanded_feature_model_search_no_extension_survivor_no_test" if complete and passing == 0 else "expanded_feature_model_contract_pending" if complete else "expanded_feature_model_search_gated",
            "expanded_model_search_complete": complete,
            "train_selected_model_rows": selected,
            "passing_extension_gate_models": passing,
            "best_model_id": metric_value(path, "phase196_best_model_id", ""),
            "best_min_extension_net_bps": metric_value(path, "phase196_best_min_extension_net_bps", ""),
            "test_replay_allowed_next": as_int(metric_value(path, "phase196_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase196_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase196_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase196_next_best_action", ""),
        }
    if phase == 197:
        complete = as_int(metric_value(path, "phase197_non_receive_flow_feature_precommit_complete", 0))
        ready = as_int(metric_value(path, "phase197_ready_feature_families", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "non_receive_flow_feature_expansion_precommitted_phase198_ready_no_test" if complete and ready > 0 else "non_receive_flow_feature_expansion_precommitted_no_ready_features_no_test" if complete else "non_receive_flow_feature_expansion_gated",
            "non_receive_flow_feature_precommit_complete": complete,
            "ready_feature_families": ready,
            "strategy_replay_allowed": as_int(metric_value(path, "phase197_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase197_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase197_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase197_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase197_next_best_action", ""),
        }
    if phase == 198:
        complete = as_int(metric_value(path, "phase198_context_model_search_complete", 0))
        selected = as_int(metric_value(path, "phase198_train_selected_model_rows", 0))
        passing = as_int(metric_value(path, "phase198_passing_extension_gate_models", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "non_receive_flow_context_model_search_no_train_survivor_no_test" if complete and selected == 0 else "non_receive_flow_context_model_search_no_extension_survivor_no_test" if complete and passing == 0 else "non_receive_flow_context_model_contract_pending" if complete else "non_receive_flow_context_model_search_gated",
            "context_model_search_complete": complete,
            "train_selected_model_rows": selected,
            "passing_extension_gate_models": passing,
            "best_model_id": metric_value(path, "phase198_best_model_id", ""),
            "best_feature_family": metric_value(path, "phase198_best_feature_family", ""),
            "best_min_extension_net_bps": metric_value(path, "phase198_best_min_extension_net_bps", ""),
            "test_replay_allowed_next": as_int(metric_value(path, "phase198_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase198_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase198_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase198_next_best_action", ""),
        }
    if phase == 199:
        complete = as_int(metric_value(path, "phase199_branch_decision_complete", 0))
        paused = as_int(metric_value(path, "phase199_current_branch_paused", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "current_receive_flow_context_branch_paused_material_redesign_required_no_test" if complete and paused == 1 else "branch_decision_recorded_no_pause_no_test" if complete else "branch_decision_gated",
            "branch_decision_complete": complete,
            "current_branch_paused": paused,
            "material_redesign_required": as_int(metric_value(path, "phase199_material_redesign_required", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase199_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase199_test_replay_allowed_next", 0)),
            "untouched_test_replay_precommit_allowed": as_int(metric_value(path, "phase199_untouched_test_replay_precommit_allowed", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase199_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase199_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase199_next_best_action", ""),
        }
    if phase == 200:
        complete = as_int(metric_value(path, "phase200_material_new_hypothesis_precommit_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "material_new_passive_queue_hypothesis_precommitted_label_expansion_pending_no_test" if complete else "material_new_hypothesis_precommit_gated",
            "material_new_hypothesis_precommit_complete": complete,
            "selected_hypothesis_id": metric_value(path, "phase200_selected_hypothesis_id", ""),
            "label_contract_rows": as_int(metric_value(path, "phase200_label_contract_rows", 0)),
            "stage_action_rows": as_int(metric_value(path, "phase200_stage_action_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase200_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase200_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase200_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase200_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase200_next_best_action", ""),
        }
    if phase == 201:
        complete = as_int(metric_value(path, "phase201_label_only_stage01_complete", 0))
        pre_replay = as_int(metric_value(path, "phase201_pre_replay_candidate_rows", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "passive_queue_stage01_label_expansion_complete_no_replay_candidate_redesign_pending" if complete and pre_replay == 0 else "passive_queue_stage01_label_expansion_complete_candidate_precommit_pending" if complete else "passive_queue_stage01_label_expansion_gated",
            "label_only_stage01_complete": complete,
            "pre_replay_candidate_rows": pre_replay,
            "joined_label_candidate_rows": as_int(metric_value(path, "phase201_joined_label_candidate_rows", 0)),
            "max_candidate_symbols": as_int(metric_value(path, "phase201_max_candidate_symbols", 0)),
            "max_candidate_trade_dates": as_int(metric_value(path, "phase201_max_candidate_trade_dates", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase201_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase201_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase201_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase201_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase201_next_best_action", ""),
        }
    if phase == 202:
        complete = as_int(metric_value(path, "phase202_passive_feature_redesign_precommit_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "passive_feature_redesign_precommitted_label_materialization_pending_no_replay" if complete else "passive_feature_redesign_precommit_gated",
            "passive_feature_redesign_precommit_complete": complete,
            "redesigned_feature_rows": as_int(metric_value(path, "phase202_redesigned_feature_rows", 0)),
            "acceptance_contract_rows": as_int(metric_value(path, "phase202_acceptance_contract_rows", 0)),
            "phase203_action_rows": as_int(metric_value(path, "phase202_phase203_action_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase202_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase202_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase202_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase202_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase202_next_best_action", ""),
        }
    if phase == 203:
        complete = as_int(metric_value(path, "phase203_label_materialization_complete", 0))
        candidate_gate = as_int(metric_value(path, "phase203_candidate_gate_open", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "redesigned_passive_labels_materialized_candidate_gate_closed_no_replay" if complete and candidate_gate == 0 else "redesigned_passive_labels_materialized_candidate_precommit_pending" if complete else "redesigned_passive_label_materialization_gated",
            "label_materialization_complete": complete,
            "materialized_label_rows": as_int(metric_value(path, "phase203_materialized_label_rows", 0)),
            "redesigned_candidate_pass_rows": as_int(metric_value(path, "phase203_redesigned_candidate_pass_rows", 0)),
            "max_candidate_symbols": as_int(metric_value(path, "phase203_max_candidate_symbols", 0)),
            "max_candidate_trade_dates": as_int(metric_value(path, "phase203_max_candidate_trade_dates", 0)),
            "adverse_selection_ceiling_met": as_int(metric_value(path, "phase203_adverse_selection_ceiling_met", 0)),
            "candidate_gate_open": candidate_gate,
            "strategy_replay_allowed": as_int(metric_value(path, "phase203_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase203_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase203_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase203_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase203_next_best_action", ""),
        }
    if phase == 204:
        complete = as_int(metric_value(path, "phase204_closure_decision_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "passive_redesign_closed_for_replay_material_new_source_or_label_breadth_pending_no_replay" if complete else "passive_redesign_closure_decision_gated",
            "closure_decision_complete": complete,
            "current_passive_redesign_closed_for_replay": as_int(metric_value(path, "phase204_current_passive_redesign_closed_for_replay", 0)),
            "material_new_source_required": as_int(metric_value(path, "phase204_material_new_source_required", 0)),
            "broader_label_materialization_allowed": as_int(metric_value(path, "phase204_broader_label_materialization_allowed", 0)),
            "threshold_widening_allowed": as_int(metric_value(path, "phase204_threshold_widening_allowed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase204_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase204_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase204_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase204_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase204_next_best_action", ""),
        }
    if phase == 205:
        complete = as_int(metric_value(path, "phase205_material_new_source_precommit_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "material_new_source_precommitted_phase206_contract_pending_no_replay" if complete else "material_new_source_precommit_gated",
            "material_new_source_precommit_complete": complete,
            "selected_route_id": metric_value(path, "phase205_selected_route_id", ""),
            "route_scorecard_rows": as_int(metric_value(path, "phase205_route_scorecard_rows", 0)),
            "phase206_work_order_rows": as_int(metric_value(path, "phase205_phase206_work_order_rows", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase205_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase205_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase205_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase205_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase205_next_best_action", ""),
        }
    if phase == 206:
        complete = as_int(metric_value(path, "phase206_nonoverlap_feature_contract_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "selected_source_nonoverlap_feature_contract_complete_phase207_matrix_pending_no_replay" if complete else "selected_source_nonoverlap_feature_contract_gated",
            "nonoverlap_feature_contract_complete": complete,
            "feature_catalog_rows": as_int(metric_value(path, "phase206_feature_catalog_rows", 0)),
            "blocked_reference_rows": as_int(metric_value(path, "phase206_blocked_reference_rows", 0)),
            "nonoverlap_pass_rows": as_int(metric_value(path, "phase206_nonoverlap_pass_rows", 0)),
            "phase207_work_order_rows": as_int(metric_value(path, "phase206_phase207_work_order_rows", 0)),
            "model_fit_allowed": as_int(metric_value(path, "phase206_model_fit_allowed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase206_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase206_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase206_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase206_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase206_next_best_action", ""),
        }
    if phase == 207:
        complete = as_int(metric_value(path, "phase207_feature_matrix_precommit_complete", 0))
        return {
            "branch": "real_receive_flow_source",
            "state": "allowed_feature_matrix_precommitted_phase208_quality_gate_pending_no_model_no_replay" if complete else "allowed_feature_matrix_precommit_gated",
            "feature_matrix_precommit_complete": complete,
            "feature_matrix_rows": as_int(metric_value(path, "phase207_feature_matrix_rows", 0)),
            "feature_available_rows": as_int(metric_value(path, "phase207_feature_available_rows", 0)),
            "trade_dates_max": as_int(metric_value(path, "phase207_trade_dates_max", 0)),
            "symbols_max": as_int(metric_value(path, "phase207_symbols_max", 0)),
            "model_fit_allowed": as_int(metric_value(path, "phase207_model_fit_allowed", 0)),
            "strategy_replay_allowed": as_int(metric_value(path, "phase207_strategy_replay_allowed", 0)),
            "test_replay_allowed_next": as_int(metric_value(path, "phase207_test_replay_allowed_next", 0)),
            "promotion_allowed": as_int(metric_value(path, "phase207_promotion_allowed", 0)),
            "paper_or_live_acceptance_allowed": as_int(metric_value(path, "phase207_paper_or_live_acceptance_allowed", 0)),
            "next_action": metric_value(path, "phase207_next_best_action", ""),
        }
    return {}


def build_phase_ledger(scripts: pd.DataFrame, outputs: pd.DataFrame) -> pd.DataFrame:
    phases = sorted(set(scripts["phase"].astype(int).tolist() if not scripts.empty else []).union(outputs["phase"].astype(int).tolist() if not outputs.empty else []))
    rows: list[dict[str, Any]] = []
    for phase in phases:
        script_rows = scripts[scripts["phase"].astype(int).eq(phase)] if not scripts.empty else pd.DataFrame()
        output_rows = outputs[outputs["phase"].astype(int).eq(phase)] if not outputs.empty else pd.DataFrame()
        metric_status = phase_status_from_metrics(phase)
        has_runner = not script_rows.empty
        has_outputs = not output_rows.empty
        has_acceptance = bool(not output_rows.empty and output_rows["acceptance_files"].astype(str).ne("").any())
        smoke_or_partial = bool(not output_rows.empty and output_rows["is_smoke_or_partial"].astype(bool).any())
        status = "script_only"
        if has_outputs and has_acceptance and not smoke_or_partial:
            status = "evidence_present"
        elif has_outputs and smoke_or_partial:
            status = "smoke_or_partial"
        if metric_status.get("state"):
            status = str(metric_status["state"])
        rows.append(
            {
                "phase": phase,
                "runner_count": int(len(script_rows)),
                "output_rows": int(len(output_rows)),
                "has_runner": has_runner,
                "has_outputs": has_outputs,
                "has_acceptance_summary": has_acceptance,
                "status": status,
                "branch": metric_status.get("branch", ""),
                "strategy_replay_allowed": metric_status.get("strategy_replay_allowed", ""),
                "pnl_allowed": metric_status.get("pnl_allowed", ""),
                "test_rows_used": metric_status.get("test_rows_used", ""),
                "test_replay_execution": metric_status.get("test_replay_execution", ""),
                "test_result_allowed": metric_status.get("test_result_allowed", ""),
                "test_replay_allowed_next": metric_status.get("test_replay_allowed_next", ""),
                "untouched_test_replay_precommit_allowed": metric_status.get("untouched_test_replay_precommit_allowed", ""),
                "reuse_without_redesign_allowed": metric_status.get("reuse_without_redesign_allowed", ""),
                "additional_validation_breadth_available_now": metric_status.get("additional_validation_breadth_available_now", ""),
                "may_relabel_test_as_validation": metric_status.get("may_relabel_test_as_validation", ""),
                "breadth_warning": metric_status.get("breadth_warning", ""),
                "date_count_warning": metric_status.get("date_count_warning", ""),
                "promotion_allowed": metric_status.get("promotion_allowed", ""),
                "paper_or_live_acceptance_allowed": metric_status.get("paper_or_live_acceptance_allowed", ""),
                "next_action": metric_status.get("next_action", ""),
                "runner": "|".join(script_rows["runner"].astype(str).tolist()) if has_runner else "",
                "output_dir": "|".join(output_rows["output_dir"].astype(str).tolist()) if has_outputs else "",
            }
        )
    return pd.DataFrame(rows)


def build_branch_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    phase174 = phase_status_from_metrics(174)
    phase175 = phase_status_from_metrics(175)
    phase176 = phase_status_from_metrics(176)
    phase177 = phase_status_from_metrics(177)
    phase178 = phase_status_from_metrics(178)
    phase179 = phase_status_from_metrics(179)
    phase180 = phase_status_from_metrics(180)
    phase181 = phase_status_from_metrics(181)
    phase182 = phase_status_from_metrics(182)
    phase183 = phase_status_from_metrics(183)
    phase184 = phase_status_from_metrics(184)
    phase185 = phase_status_from_metrics(185)
    phase186 = phase_status_from_metrics(186)
    phase187 = phase_status_from_metrics(187)
    phase188 = phase_status_from_metrics(188)
    phase189 = phase_status_from_metrics(189)
    phase190 = phase_status_from_metrics(190)
    phase191 = phase_status_from_metrics(191)
    phase192 = phase_status_from_metrics(192)
    phase193 = phase_status_from_metrics(193)
    phase194 = phase_status_from_metrics(194)
    phase195 = phase_status_from_metrics(195)
    phase196 = phase_status_from_metrics(196)
    phase197 = phase_status_from_metrics(197)
    phase198 = phase_status_from_metrics(198)
    phase199 = phase_status_from_metrics(199)
    phase200 = phase_status_from_metrics(200)
    phase201 = phase_status_from_metrics(201)
    phase202 = phase_status_from_metrics(202)
    phase203 = phase_status_from_metrics(203)
    phase204 = phase_status_from_metrics(204)
    phase205 = phase_status_from_metrics(205)
    phase206 = phase_status_from_metrics(206)
    phase207 = phase_status_from_metrics(207)
    phase172 = phase_status_from_metrics(172)
    real_receive_next = phase207.get("next_action") or phase206.get("next_action") or phase205.get("next_action") or phase204.get("next_action") or phase203.get("next_action") or phase202.get("next_action") or phase201.get("next_action") or phase200.get("next_action") or phase199.get("next_action") or phase198.get("next_action") or phase197.get("next_action") or phase196.get("next_action") or phase195.get("next_action") or phase194.get("next_action") or phase193.get("next_action") or phase192.get("next_action") or phase191.get("next_action") or phase190.get("next_action") or phase189.get("next_action") or phase188.get("next_action") or phase187.get("next_action") or phase186.get("next_action") or phase185.get("next_action") or phase184.get("next_action") or phase183.get("next_action") or phase182.get("next_action") or phase181.get("next_action") or phase180.get("next_action") or phase179.get("next_action") or phase178.get("next_action") or phase177.get("next_action") or phase176.get("next_action") or phase175.get("next_action") or phase174.get("next_action") or phase172.get("next_action") or "run_phase174_or_phase172_according_to_latest_gate"
    ready_dates = as_int(phase172.get("ready_receive_flow_dates", 0))
    additional_dates_needed = as_int(phase172.get("additional_dates_needed", 0))
    features_materialized = as_int(phase176.get("features_materialized", 0))
    quality_audit_ran = as_int(phase177.get("feature_quality_audit_ran", 0))
    handoff_ready = as_int(phase178.get("handoff_ready", 0))
    precommit_ready = as_int(phase179.get("precommit_ready", 0))
    cost_label_ready = as_int(phase180.get("precommit_ready", 0))
    labels_materialized = as_int(phase181.get("labels_materialized", 0))
    label_audit_pass = as_int(phase182.get("label_quality_leakage_audit_pass", 0))
    replay_readiness = as_int(phase183.get("replay_readiness_precommitted", 0))
    dry_run_complete = as_int(phase184.get("train_validation_dry_run_complete", 0))
    interpretation_complete = as_int(phase185.get("validation_interpretation_complete", 0))
    family_set_closed = as_int(phase186.get("current_family_set_closed", 0))
    sparse_candidate_complete = as_int(phase187.get("cost_aware_sparse_candidate_complete", 0))
    sparse_interpretation_complete = as_int(phase188.get("sparse_candidate_interpretation_complete", 0))
    test_precommit_decision_complete = as_int(phase189.get("test_precommit_decision_complete", 0))
    phase190_complete = as_int(phase190.get("phase190_decision_complete", 0))
    phase191_complete = as_int(phase191.get("diagnostic_test_precommit_complete", 0))
    phase192_complete = as_int(phase192.get("real_validation_download_complete", 0))
    phase193_complete = as_int(phase193.get("validation_breadth_extension_complete", 0))
    phase194_complete = as_int(phase194.get("fragility_decision_complete", 0))
    phase195_complete = as_int(phase195.get("redesign_search_complete", 0))
    phase196_complete = as_int(phase196.get("expanded_model_search_complete", 0))
    phase197_complete = as_int(phase197.get("non_receive_flow_feature_precommit_complete", 0))
    phase198_complete = as_int(phase198.get("context_model_search_complete", 0))
    phase199_complete = as_int(phase199.get("branch_decision_complete", 0))
    phase200_complete = as_int(phase200.get("material_new_hypothesis_precommit_complete", 0))
    phase201_complete = as_int(phase201.get("label_only_stage01_complete", 0))
    phase202_complete = as_int(phase202.get("passive_feature_redesign_precommit_complete", 0))
    phase203_complete = as_int(phase203.get("label_materialization_complete", 0))
    phase204_complete = as_int(phase204.get("closure_decision_complete", 0))
    phase205_complete = as_int(phase205.get("material_new_source_precommit_complete", 0))
    phase206_complete = as_int(phase206.get("nonoverlap_feature_contract_complete", 0))
    phase207_complete = as_int(phase207.get("feature_matrix_precommit_complete", 0))
    if ready_dates >= 5 and additional_dates_needed == 0:
        real_receive_status = "source_gate_open_feature_materialization_pending" if features_materialized == 0 else "feature_quality_pending"
        if quality_audit_ran == 1:
            real_receive_status = "quality_audited_handoff_pending"
        if handoff_ready == 1:
            real_receive_status = "handoff_precommitted_strategy_family_pending"
        if precommit_ready == 1:
            real_receive_status = "strategy_family_precommitted_cost_latency_label_pending"
        if cost_label_ready == 1:
            real_receive_status = "cost_latency_label_precommitted_label_materialization_pending"
        if labels_materialized == 1:
            real_receive_status = "labels_materialized_quality_leakage_pending"
        if label_audit_pass == 1:
            real_receive_status = "label_quality_leakage_audited_replay_readiness_pending"
        if replay_readiness == 1:
            real_receive_status = "replay_readiness_precommitted_train_validation_dry_run_pending"
        if dry_run_complete == 1:
            real_receive_status = "train_validation_replay_dry_run_complete_interpretation_pending"
        if interpretation_complete == 1:
            real_receive_status = "validation_interpretation_cost_dominated_redesign_or_close_pending"
        if family_set_closed == 1:
            real_receive_status = "current_family_set_closed_cost_aware_redesign_pending"
        if sparse_candidate_complete == 1:
            real_receive_status = "cost_aware_sparse_candidate_validation_interpretation_pending"
        if sparse_interpretation_complete == 1:
            real_receive_status = "sparse_candidate_interpreted_phase189_decision_pending"
        if test_precommit_decision_complete == 1:
            real_receive_status = "test_replay_deferred_validation_breadth_pending"
        if phase190_complete == 1:
            real_receive_status = "diagnostic_test_spec_written_validation_breadth_pending"
        if phase191_complete == 1:
            real_receive_status = "diagnostic_test_replay_precommitted_no_execution"
        if phase192_complete == 1:
            real_receive_status = "real_validation_date_downloaded_feature_label_refresh_pending"
        if phase193_complete == 1:
            real_receive_status = "validation_breadth_extended_mixed_negative_by_date_no_test"
        if phase194_complete == 1:
            real_receive_status = "frozen_sparse_candidate_closed_for_test_replay_redesign_required"
        if phase195_complete == 1:
            real_receive_status = str(phase195.get("state", "redesign_search_complete_no_test"))
        if phase196_complete == 1:
            real_receive_status = str(phase196.get("state", "expanded_feature_model_search_complete_no_test"))
        if phase197_complete == 1:
            real_receive_status = str(phase197.get("state", "non_receive_flow_feature_expansion_precommitted_no_test"))
        if phase198_complete == 1:
            real_receive_status = str(phase198.get("state", "non_receive_flow_context_model_search_complete_no_test"))
        if phase199_complete == 1:
            real_receive_status = str(phase199.get("state", "branch_decision_complete_no_test"))
        if phase200_complete == 1:
            real_receive_status = str(phase200.get("state", "material_new_hypothesis_precommit_complete_no_test"))
        if phase201_complete == 1:
            real_receive_status = str(phase201.get("state", "passive_queue_stage01_complete_no_test"))
        if phase202_complete == 1:
            real_receive_status = str(phase202.get("state", "passive_feature_redesign_precommitted_no_test"))
        if phase203_complete == 1:
            real_receive_status = str(phase203.get("state", "redesigned_passive_labels_materialized_no_test"))
        if phase204_complete == 1:
            real_receive_status = str(phase204.get("state", "passive_redesign_closure_decision_complete_no_test"))
        if phase205_complete == 1:
            real_receive_status = str(phase205.get("state", "material_new_source_precommit_complete_no_test"))
        if phase206_complete == 1:
            real_receive_status = str(phase206.get("state", "selected_source_nonoverlap_feature_contract_complete_no_test"))
        if phase207_complete == 1:
            real_receive_status = str(phase207.get("state", "allowed_feature_matrix_precommit_complete_no_test"))
    else:
        real_receive_status = "gated_waiting_for_two_more_real_l2_dates"
    real_receive_evidence = (
        f"Phase172 ready_dates={phase172.get('ready_receive_flow_dates', '')}, additional_dates_needed={phase172.get('additional_dates_needed', '')}; "
        f"Phase174 download_ran={phase174.get('download_ran', '')}; "
        f"Phase175 activation_ready={phase175.get('activation_ready', '')}; "
        f"Phase176 features_materialized={phase176.get('features_materialized', '')}; "
        f"Phase177 quality_audit_ran={phase177.get('feature_quality_audit_ran', '')}; "
        f"Phase178 handoff_ready={phase178.get('handoff_ready', '')}; "
        f"Phase179 precommit_ready={phase179.get('precommit_ready', '')}; "
        f"Phase180 precommit_ready={phase180.get('precommit_ready', '')}; "
        f"Phase181 labels_materialized={phase181.get('labels_materialized', '')}; "
        f"Phase182 label_audit_pass={phase182.get('label_quality_leakage_audit_pass', '')}; "
        f"Phase183 replay_readiness={phase183.get('replay_readiness_precommitted', '')}; "
        f"Phase184 dry_run_complete={phase184.get('train_validation_dry_run_complete', '')}, test_rows_used={phase184.get('test_rows_used', '')}, promotion_allowed={phase184.get('promotion_allowed', '')}; "
        f"Phase185 interpretation_complete={phase185.get('validation_interpretation_complete', '')}, cost_dominates={phase185.get('cost_dominates_validation_edge', '')}, test_replay_allowed_next={phase185.get('test_replay_allowed_next', '')}; "
        f"Phase186 family_set_closed={phase186.get('current_family_set_closed', '')}, reuse_without_redesign_allowed={phase186.get('reuse_without_redesign_allowed', '')}, test_replay_allowed_next={phase186.get('test_replay_allowed_next', '')}; "
        f"Phase187 candidate_complete={phase187.get('cost_aware_sparse_candidate_complete', '')}, validation_positive_all_profiles={phase187.get('validation_positive_all_profiles', '')}, test_replay_allowed_next={phase187.get('test_replay_allowed_next', '')}; "
        f"Phase188 interpretation_complete={phase188.get('sparse_candidate_interpretation_complete', '')}, breadth_warning={phase188.get('breadth_warning', '')}, date_count_warning={phase188.get('date_count_warning', '')}, test_replay_allowed_next={phase188.get('test_replay_allowed_next', '')}; "
        f"Phase189 decision_complete={phase189.get('test_precommit_decision_complete', '')}, test_precommit_allowed={phase189.get('untouched_test_replay_precommit_allowed', '')}, test_replay_allowed_next={phase189.get('test_replay_allowed_next', '')}; "
        f"Phase190 decision_complete={phase190.get('phase190_decision_complete', '')}, additional_validation_breadth_available_now={phase190.get('additional_validation_breadth_available_now', '')}, test_replay_execution={phase190.get('test_replay_execution', '')}; "
        f"Phase191 precommit_complete={phase191.get('diagnostic_test_precommit_complete', '')}, test_replay_execution={phase191.get('test_replay_execution', '')}, test_result_allowed={phase191.get('test_result_allowed', '')}; "
        f"Phase192 download_complete={phase192.get('real_validation_download_complete', '')}, test_replay_execution={phase192.get('test_replay_execution', '')}; "
        f"Phase193 extension_complete={phase193.get('validation_breadth_extension_complete', '')}, extension_dates={phase193.get('extension_validation_dates', '')}, min_profile_net={phase193.get('min_profile_net_bps_proxy_mean', '')}, breadth_warning={phase193.get('breadth_warning', '')}, test_replay_execution={phase193.get('test_replay_execution', '')}; "
        f"Phase194 fragility_decision_complete={phase194.get('fragility_decision_complete', '')}, all_extension_profile_dates_negative={phase194.get('all_extension_profile_dates_negative', '')}, test_replay_allowed_next={phase194.get('test_replay_allowed_next', '')}; "
        f"Phase195 redesign_search_complete={phase195.get('redesign_search_complete', '')}, passing_extension_gate_candidates={phase195.get('passing_extension_gate_candidates', '')}, best_candidate={phase195.get('best_candidate_id', '')}, best_min_extension_net={phase195.get('best_min_extension_net_bps', '')}, test_replay_allowed_next={phase195.get('test_replay_allowed_next', '')}; "
        f"Phase196 expanded_model_search_complete={phase196.get('expanded_model_search_complete', '')}, train_selected_model_rows={phase196.get('train_selected_model_rows', '')}, passing_extension_gate_models={phase196.get('passing_extension_gate_models', '')}, best_model={phase196.get('best_model_id', '')}, test_replay_allowed_next={phase196.get('test_replay_allowed_next', '')}; "
        f"Phase197 feature_precommit_complete={phase197.get('non_receive_flow_feature_precommit_complete', '')}, ready_feature_families={phase197.get('ready_feature_families', '')}, strategy_replay_allowed={phase197.get('strategy_replay_allowed', '')}, test_replay_allowed_next={phase197.get('test_replay_allowed_next', '')}; "
        f"Phase198 context_model_search_complete={phase198.get('context_model_search_complete', '')}, train_selected_model_rows={phase198.get('train_selected_model_rows', '')}, passing_extension_gate_models={phase198.get('passing_extension_gate_models', '')}, best_model={phase198.get('best_model_id', '')}, best_family={phase198.get('best_feature_family', '')}, test_replay_allowed_next={phase198.get('test_replay_allowed_next', '')}; "
        f"Phase199 branch_decision_complete={phase199.get('branch_decision_complete', '')}, current_branch_paused={phase199.get('current_branch_paused', '')}, material_redesign_required={phase199.get('material_redesign_required', '')}, test_replay_allowed_next={phase199.get('test_replay_allowed_next', '')}; "
        f"Phase200 precommit_complete={phase200.get('material_new_hypothesis_precommit_complete', '')}, selected_hypothesis={phase200.get('selected_hypothesis_id', '')}, label_contract_rows={phase200.get('label_contract_rows', '')}, stage_action_rows={phase200.get('stage_action_rows', '')}, test_replay_allowed_next={phase200.get('test_replay_allowed_next', '')}; "
        f"Phase201 stage01_complete={phase201.get('label_only_stage01_complete', '')}, joined_rows={phase201.get('joined_label_candidate_rows', '')}, pre_replay_candidates={phase201.get('pre_replay_candidate_rows', '')}, max_symbols={phase201.get('max_candidate_symbols', '')}, max_dates={phase201.get('max_candidate_trade_dates', '')}, test_replay_allowed_next={phase201.get('test_replay_allowed_next', '')}; "
        f"Phase202 redesign_precommit_complete={phase202.get('passive_feature_redesign_precommit_complete', '')}, redesigned_feature_rows={phase202.get('redesigned_feature_rows', '')}, acceptance_contract_rows={phase202.get('acceptance_contract_rows', '')}, phase203_action_rows={phase202.get('phase203_action_rows', '')}, test_replay_allowed_next={phase202.get('test_replay_allowed_next', '')}; "
        f"Phase203 label_materialization_complete={phase203.get('label_materialization_complete', '')}, materialized_label_rows={phase203.get('materialized_label_rows', '')}, redesigned_candidate_pass_rows={phase203.get('redesigned_candidate_pass_rows', '')}, max_symbols={phase203.get('max_candidate_symbols', '')}, max_dates={phase203.get('max_candidate_trade_dates', '')}, adverse_selection_ceiling_met={phase203.get('adverse_selection_ceiling_met', '')}, candidate_gate_open={phase203.get('candidate_gate_open', '')}, test_replay_allowed_next={phase203.get('test_replay_allowed_next', '')}; "
        f"Phase204 closure_decision_complete={phase204.get('closure_decision_complete', '')}, passive_redesign_closed_for_replay={phase204.get('current_passive_redesign_closed_for_replay', '')}, material_new_source_required={phase204.get('material_new_source_required', '')}, threshold_widening_allowed={phase204.get('threshold_widening_allowed', '')}, test_replay_allowed_next={phase204.get('test_replay_allowed_next', '')}; "
        f"Phase205 material_new_source_precommit_complete={phase205.get('material_new_source_precommit_complete', '')}, selected_route={phase205.get('selected_route_id', '')}, phase206_work_order_rows={phase205.get('phase206_work_order_rows', '')}, test_replay_allowed_next={phase205.get('test_replay_allowed_next', '')}; "
        f"Phase206 nonoverlap_feature_contract_complete={phase206.get('nonoverlap_feature_contract_complete', '')}, feature_catalog_rows={phase206.get('feature_catalog_rows', '')}, blocked_reference_rows={phase206.get('blocked_reference_rows', '')}, nonoverlap_pass_rows={phase206.get('nonoverlap_pass_rows', '')}, model_fit_allowed={phase206.get('model_fit_allowed', '')}, test_replay_allowed_next={phase206.get('test_replay_allowed_next', '')}; "
        f"Phase207 feature_matrix_precommit_complete={phase207.get('feature_matrix_precommit_complete', '')}, matrix_rows={phase207.get('feature_matrix_rows', '')}, available_rows={phase207.get('feature_available_rows', '')}, trade_dates={phase207.get('trade_dates_max', '')}, symbols={phase207.get('symbols_max', '')}, model_fit_allowed={phase207.get('model_fit_allowed', '')}, test_replay_allowed_next={phase207.get('test_replay_allowed_next', '')}."
    )
    branches = [
        {
            "branch": "real_l2_anchor_gate",
            "status": "gated",
            "evidence": "Phase146/148 keep strategy replay closed until at least five ready real-anchor days are proven.",
            "current_next_action": "use_phase174_secure_download_orchestrator_for_required_real_l2_dates",
        },
        {
            "branch": "real_receive_flow_source",
            "status": real_receive_status,
            "evidence": real_receive_evidence,
            "current_next_action": real_receive_next,
        },
        {
            "branch": "top_five_depth_passive",
            "status": "closed_clean_falsification",
            "evidence": "Phase136 Outcome A closes the branch after Phase132 kill-switch and Phase116 blocklist verification.",
            "current_next_action": "do_not_open_phase134_or_phase135_for_this_branch",
        },
        {
            "branch": "dense_synthetic_replay",
            "status": "not_promoted",
            "evidence": "Partial/smoke dense replay artifacts remain non-promotional and do not override replay gates.",
            "current_next_action": "only_continue_if_precommitted_and_not_blocklisted",
        },
    ]
    return pd.DataFrame(branches)


def build_global_gates(phase_ledger: pd.DataFrame) -> pd.DataFrame:
    phase136 = phase_ledger[phase_ledger["phase"].astype(int).eq(136)] if not phase_ledger.empty else pd.DataFrame()
    phase148 = phase_ledger[phase_ledger["phase"].astype(int).eq(148)] if not phase_ledger.empty else pd.DataFrame()
    phase172 = phase_ledger[phase_ledger["phase"].astype(int).eq(172)] if not phase_ledger.empty else pd.DataFrame()
    phase174 = phase_ledger[phase_ledger["phase"].astype(int).eq(174)] if not phase_ledger.empty else pd.DataFrame()
    phase175 = phase_ledger[phase_ledger["phase"].astype(int).eq(175)] if not phase_ledger.empty else pd.DataFrame()
    phase176 = phase_ledger[phase_ledger["phase"].astype(int).eq(176)] if not phase_ledger.empty else pd.DataFrame()
    phase177 = phase_ledger[phase_ledger["phase"].astype(int).eq(177)] if not phase_ledger.empty else pd.DataFrame()
    phase178 = phase_ledger[phase_ledger["phase"].astype(int).eq(178)] if not phase_ledger.empty else pd.DataFrame()
    phase179 = phase_ledger[phase_ledger["phase"].astype(int).eq(179)] if not phase_ledger.empty else pd.DataFrame()
    phase180 = phase_ledger[phase_ledger["phase"].astype(int).eq(180)] if not phase_ledger.empty else pd.DataFrame()
    phase181 = phase_ledger[phase_ledger["phase"].astype(int).eq(181)] if not phase_ledger.empty else pd.DataFrame()
    phase182 = phase_ledger[phase_ledger["phase"].astype(int).eq(182)] if not phase_ledger.empty else pd.DataFrame()
    phase183 = phase_ledger[phase_ledger["phase"].astype(int).eq(183)] if not phase_ledger.empty else pd.DataFrame()
    phase184 = phase_ledger[phase_ledger["phase"].astype(int).eq(184)] if not phase_ledger.empty else pd.DataFrame()
    phase185 = phase_ledger[phase_ledger["phase"].astype(int).eq(185)] if not phase_ledger.empty else pd.DataFrame()
    phase186 = phase_ledger[phase_ledger["phase"].astype(int).eq(186)] if not phase_ledger.empty else pd.DataFrame()
    phase187 = phase_ledger[phase_ledger["phase"].astype(int).eq(187)] if not phase_ledger.empty else pd.DataFrame()
    phase188 = phase_ledger[phase_ledger["phase"].astype(int).eq(188)] if not phase_ledger.empty else pd.DataFrame()
    phase189 = phase_ledger[phase_ledger["phase"].astype(int).eq(189)] if not phase_ledger.empty else pd.DataFrame()
    phase190 = phase_ledger[phase_ledger["phase"].astype(int).eq(190)] if not phase_ledger.empty else pd.DataFrame()
    phase191 = phase_ledger[phase_ledger["phase"].astype(int).eq(191)] if not phase_ledger.empty else pd.DataFrame()
    phase192 = phase_ledger[phase_ledger["phase"].astype(int).eq(192)] if not phase_ledger.empty else pd.DataFrame()
    phase193 = phase_ledger[phase_ledger["phase"].astype(int).eq(193)] if not phase_ledger.empty else pd.DataFrame()
    phase194 = phase_ledger[phase_ledger["phase"].astype(int).eq(194)] if not phase_ledger.empty else pd.DataFrame()
    phase195 = phase_ledger[phase_ledger["phase"].astype(int).eq(195)] if not phase_ledger.empty else pd.DataFrame()
    phase196 = phase_ledger[phase_ledger["phase"].astype(int).eq(196)] if not phase_ledger.empty else pd.DataFrame()
    phase197 = phase_ledger[phase_ledger["phase"].astype(int).eq(197)] if not phase_ledger.empty else pd.DataFrame()
    phase198 = phase_ledger[phase_ledger["phase"].astype(int).eq(198)] if not phase_ledger.empty else pd.DataFrame()
    phase199 = phase_ledger[phase_ledger["phase"].astype(int).eq(199)] if not phase_ledger.empty else pd.DataFrame()
    phase200 = phase_ledger[phase_ledger["phase"].astype(int).eq(200)] if not phase_ledger.empty else pd.DataFrame()
    phase201 = phase_ledger[phase_ledger["phase"].astype(int).eq(201)] if not phase_ledger.empty else pd.DataFrame()
    phase202 = phase_ledger[phase_ledger["phase"].astype(int).eq(202)] if not phase_ledger.empty else pd.DataFrame()
    phase203 = phase_ledger[phase_ledger["phase"].astype(int).eq(203)] if not phase_ledger.empty else pd.DataFrame()
    phase204 = phase_ledger[phase_ledger["phase"].astype(int).eq(204)] if not phase_ledger.empty else pd.DataFrame()
    phase205 = phase_ledger[phase_ledger["phase"].astype(int).eq(205)] if not phase_ledger.empty else pd.DataFrame()
    phase206 = phase_ledger[phase_ledger["phase"].astype(int).eq(206)] if not phase_ledger.empty else pd.DataFrame()
    phase207 = phase_ledger[phase_ledger["phase"].astype(int).eq(207)] if not phase_ledger.empty else pd.DataFrame()
    phase206_metrics = phase_status_from_metrics(206)
    real_replay_allowed = int(phase148["strategy_replay_allowed"].iloc[0]) if not phase148.empty and str(phase148["strategy_replay_allowed"].iloc[0]) != "" else 0
    receive_replay_allowed = int(phase172["strategy_replay_allowed"].iloc[0]) if not phase172.empty and str(phase172["strategy_replay_allowed"].iloc[0]) != "" else 0
    secure_replay_allowed = int(phase174["strategy_replay_allowed"].iloc[0]) if not phase174.empty and str(phase174["strategy_replay_allowed"].iloc[0]) != "" else 0
    schema_replay_allowed = int(phase175["strategy_replay_allowed"].iloc[0]) if not phase175.empty and str(phase175["strategy_replay_allowed"].iloc[0]) != "" else 0
    materializer_replay_allowed = int(phase176["strategy_replay_allowed"].iloc[0]) if not phase176.empty and str(phase176["strategy_replay_allowed"].iloc[0]) != "" else 0
    quality_replay_allowed = int(phase177["strategy_replay_allowed"].iloc[0]) if not phase177.empty and str(phase177["strategy_replay_allowed"].iloc[0]) != "" else 0
    handoff_replay_allowed = int(phase178["strategy_replay_allowed"].iloc[0]) if not phase178.empty and str(phase178["strategy_replay_allowed"].iloc[0]) != "" else 0
    precommit_replay_allowed = int(phase179["strategy_replay_allowed"].iloc[0]) if not phase179.empty and str(phase179["strategy_replay_allowed"].iloc[0]) != "" else 0
    cost_label_replay_allowed = int(phase180["strategy_replay_allowed"].iloc[0]) if not phase180.empty and str(phase180["strategy_replay_allowed"].iloc[0]) != "" else 0
    label_materialization_replay_allowed = int(phase181["strategy_replay_allowed"].iloc[0]) if not phase181.empty and str(phase181["strategy_replay_allowed"].iloc[0]) != "" else 0
    label_audit_replay_allowed = int(phase182["strategy_replay_allowed"].iloc[0]) if not phase182.empty and str(phase182["strategy_replay_allowed"].iloc[0]) != "" else 0
    replay_readiness_replay_allowed = int(phase183["strategy_replay_allowed"].iloc[0]) if not phase183.empty and str(phase183["strategy_replay_allowed"].iloc[0]) != "" else 0
    replay_readiness_pnl_allowed = int(phase183["pnl_allowed"].iloc[0]) if not phase183.empty and str(phase183["pnl_allowed"].iloc[0]) != "" else 0
    dry_run_test_rows_used = int(phase184["test_rows_used"].iloc[0]) if not phase184.empty and str(phase184["test_rows_used"].iloc[0]) != "" else 0
    dry_run_promotion_allowed = int(phase184["promotion_allowed"].iloc[0]) if not phase184.empty and str(phase184["promotion_allowed"].iloc[0]) != "" else 0
    dry_run_paper_live_allowed = int(phase184["paper_or_live_acceptance_allowed"].iloc[0]) if not phase184.empty and str(phase184["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    interpretation_test_rows_used = int(phase185["test_rows_used"].iloc[0]) if not phase185.empty and str(phase185["test_rows_used"].iloc[0]) != "" else 0
    interpretation_test_replay_allowed = int(phase185["test_replay_allowed_next"].iloc[0]) if not phase185.empty and str(phase185["test_replay_allowed_next"].iloc[0]) != "" else 0
    interpretation_promotion_allowed = int(phase185["promotion_allowed"].iloc[0]) if not phase185.empty and str(phase185["promotion_allowed"].iloc[0]) != "" else 0
    interpretation_paper_live_allowed = int(phase185["paper_or_live_acceptance_allowed"].iloc[0]) if not phase185.empty and str(phase185["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    closure_reuse_allowed = int(phase186["reuse_without_redesign_allowed"].iloc[0]) if not phase186.empty and str(phase186["reuse_without_redesign_allowed"].iloc[0]) != "" else 0
    closure_test_replay_allowed = int(phase186["test_replay_allowed_next"].iloc[0]) if not phase186.empty and str(phase186["test_replay_allowed_next"].iloc[0]) != "" else 0
    closure_promotion_allowed = int(phase186["promotion_allowed"].iloc[0]) if not phase186.empty and str(phase186["promotion_allowed"].iloc[0]) != "" else 0
    closure_paper_live_allowed = int(phase186["paper_or_live_acceptance_allowed"].iloc[0]) if not phase186.empty and str(phase186["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    sparse_test_rows_used = int(phase187["test_rows_used"].iloc[0]) if not phase187.empty and str(phase187["test_rows_used"].iloc[0]) != "" else 0
    sparse_test_replay_allowed = int(phase187["test_replay_allowed_next"].iloc[0]) if not phase187.empty and str(phase187["test_replay_allowed_next"].iloc[0]) != "" else 0
    sparse_promotion_allowed = int(phase187["promotion_allowed"].iloc[0]) if not phase187.empty and str(phase187["promotion_allowed"].iloc[0]) != "" else 0
    sparse_paper_live_allowed = int(phase187["paper_or_live_acceptance_allowed"].iloc[0]) if not phase187.empty and str(phase187["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    interp188_test_replay_allowed = int(phase188["test_replay_allowed_next"].iloc[0]) if not phase188.empty and str(phase188["test_replay_allowed_next"].iloc[0]) != "" else 0
    interp188_promotion_allowed = int(phase188["promotion_allowed"].iloc[0]) if not phase188.empty and str(phase188["promotion_allowed"].iloc[0]) != "" else 0
    interp188_paper_live_allowed = int(phase188["paper_or_live_acceptance_allowed"].iloc[0]) if not phase188.empty and str(phase188["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    decision189_test_precommit_allowed = int(phase189["untouched_test_replay_precommit_allowed"].iloc[0]) if not phase189.empty and str(phase189["untouched_test_replay_precommit_allowed"].iloc[0]) != "" else 0
    decision189_test_replay_allowed = int(phase189["test_replay_allowed_next"].iloc[0]) if not phase189.empty and str(phase189["test_replay_allowed_next"].iloc[0]) != "" else 0
    decision189_promotion_allowed = int(phase189["promotion_allowed"].iloc[0]) if not phase189.empty and str(phase189["promotion_allowed"].iloc[0]) != "" else 0
    decision189_paper_live_allowed = int(phase189["paper_or_live_acceptance_allowed"].iloc[0]) if not phase189.empty and str(phase189["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase190_test_replay_execution = int(phase190["test_replay_execution"].iloc[0]) if not phase190.empty and str(phase190["test_replay_execution"].iloc[0]) != "" else 0
    phase190_test_replay_allowed = int(phase190["test_replay_allowed_next"].iloc[0]) if not phase190.empty and str(phase190["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase190_promotion_allowed = int(phase190["promotion_allowed"].iloc[0]) if not phase190.empty and str(phase190["promotion_allowed"].iloc[0]) != "" else 0
    phase190_paper_live_allowed = int(phase190["paper_or_live_acceptance_allowed"].iloc[0]) if not phase190.empty and str(phase190["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase191_test_replay_execution = int(phase191["test_replay_execution"].iloc[0]) if not phase191.empty and str(phase191["test_replay_execution"].iloc[0]) != "" else 0
    phase191_test_result_allowed = int(phase191["test_result_allowed"].iloc[0]) if not phase191.empty and str(phase191["test_result_allowed"].iloc[0]) != "" else 0
    phase191_test_replay_allowed = int(phase191["test_replay_allowed_next"].iloc[0]) if not phase191.empty and str(phase191["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase191_promotion_allowed = int(phase191["promotion_allowed"].iloc[0]) if not phase191.empty and str(phase191["promotion_allowed"].iloc[0]) != "" else 0
    phase191_paper_live_allowed = int(phase191["paper_or_live_acceptance_allowed"].iloc[0]) if not phase191.empty and str(phase191["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase192_test_replay_execution = int(phase192["test_replay_execution"].iloc[0]) if not phase192.empty and str(phase192["test_replay_execution"].iloc[0]) != "" else 0
    phase192_test_result_allowed = int(phase192["test_result_allowed"].iloc[0]) if not phase192.empty and str(phase192["test_result_allowed"].iloc[0]) != "" else 0
    phase192_promotion_allowed = int(phase192["promotion_allowed"].iloc[0]) if not phase192.empty and str(phase192["promotion_allowed"].iloc[0]) != "" else 0
    phase192_paper_live_allowed = int(phase192["paper_or_live_acceptance_allowed"].iloc[0]) if not phase192.empty and str(phase192["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase193_test_replay_execution = int(phase193["test_replay_execution"].iloc[0]) if not phase193.empty and str(phase193["test_replay_execution"].iloc[0]) != "" else 0
    phase193_test_result_allowed = int(phase193["test_result_allowed"].iloc[0]) if not phase193.empty and str(phase193["test_result_allowed"].iloc[0]) != "" else 0
    phase193_promotion_allowed = int(phase193["promotion_allowed"].iloc[0]) if not phase193.empty and str(phase193["promotion_allowed"].iloc[0]) != "" else 0
    phase193_paper_live_allowed = int(phase193["paper_or_live_acceptance_allowed"].iloc[0]) if not phase193.empty and str(phase193["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase194_test_replay_allowed = int(phase194["test_replay_allowed_next"].iloc[0]) if not phase194.empty and str(phase194["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase194_promotion_allowed = int(phase194["promotion_allowed"].iloc[0]) if not phase194.empty and str(phase194["promotion_allowed"].iloc[0]) != "" else 0
    phase194_paper_live_allowed = int(phase194["paper_or_live_acceptance_allowed"].iloc[0]) if not phase194.empty and str(phase194["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase195_test_replay_allowed = int(phase195["test_replay_allowed_next"].iloc[0]) if not phase195.empty and str(phase195["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase195_promotion_allowed = int(phase195["promotion_allowed"].iloc[0]) if not phase195.empty and str(phase195["promotion_allowed"].iloc[0]) != "" else 0
    phase195_paper_live_allowed = int(phase195["paper_or_live_acceptance_allowed"].iloc[0]) if not phase195.empty and str(phase195["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase196_test_replay_allowed = int(phase196["test_replay_allowed_next"].iloc[0]) if not phase196.empty and str(phase196["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase196_promotion_allowed = int(phase196["promotion_allowed"].iloc[0]) if not phase196.empty and str(phase196["promotion_allowed"].iloc[0]) != "" else 0
    phase196_paper_live_allowed = int(phase196["paper_or_live_acceptance_allowed"].iloc[0]) if not phase196.empty and str(phase196["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase197_strategy_replay_allowed = int(phase197["strategy_replay_allowed"].iloc[0]) if not phase197.empty and str(phase197["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase197_test_replay_allowed = int(phase197["test_replay_allowed_next"].iloc[0]) if not phase197.empty and str(phase197["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase197_promotion_allowed = int(phase197["promotion_allowed"].iloc[0]) if not phase197.empty and str(phase197["promotion_allowed"].iloc[0]) != "" else 0
    phase197_paper_live_allowed = int(phase197["paper_or_live_acceptance_allowed"].iloc[0]) if not phase197.empty and str(phase197["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase198_test_replay_allowed = int(phase198["test_replay_allowed_next"].iloc[0]) if not phase198.empty and str(phase198["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase198_promotion_allowed = int(phase198["promotion_allowed"].iloc[0]) if not phase198.empty and str(phase198["promotion_allowed"].iloc[0]) != "" else 0
    phase198_paper_live_allowed = int(phase198["paper_or_live_acceptance_allowed"].iloc[0]) if not phase198.empty and str(phase198["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase199_strategy_replay_allowed = int(phase199["strategy_replay_allowed"].iloc[0]) if not phase199.empty and str(phase199["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase199_test_replay_allowed = int(phase199["test_replay_allowed_next"].iloc[0]) if not phase199.empty and str(phase199["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase199_precommit_allowed = int(phase199["untouched_test_replay_precommit_allowed"].iloc[0]) if not phase199.empty and str(phase199["untouched_test_replay_precommit_allowed"].iloc[0]) != "" else 0
    phase199_promotion_allowed = int(phase199["promotion_allowed"].iloc[0]) if not phase199.empty and str(phase199["promotion_allowed"].iloc[0]) != "" else 0
    phase199_paper_live_allowed = int(phase199["paper_or_live_acceptance_allowed"].iloc[0]) if not phase199.empty and str(phase199["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase200_strategy_replay_allowed = int(phase200["strategy_replay_allowed"].iloc[0]) if not phase200.empty and str(phase200["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase200_test_replay_allowed = int(phase200["test_replay_allowed_next"].iloc[0]) if not phase200.empty and str(phase200["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase200_promotion_allowed = int(phase200["promotion_allowed"].iloc[0]) if not phase200.empty and str(phase200["promotion_allowed"].iloc[0]) != "" else 0
    phase200_paper_live_allowed = int(phase200["paper_or_live_acceptance_allowed"].iloc[0]) if not phase200.empty and str(phase200["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase201_strategy_replay_allowed = int(phase201["strategy_replay_allowed"].iloc[0]) if not phase201.empty and str(phase201["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase201_test_replay_allowed = int(phase201["test_replay_allowed_next"].iloc[0]) if not phase201.empty and str(phase201["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase201_promotion_allowed = int(phase201["promotion_allowed"].iloc[0]) if not phase201.empty and str(phase201["promotion_allowed"].iloc[0]) != "" else 0
    phase201_paper_live_allowed = int(phase201["paper_or_live_acceptance_allowed"].iloc[0]) if not phase201.empty and str(phase201["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase202_strategy_replay_allowed = int(phase202["strategy_replay_allowed"].iloc[0]) if not phase202.empty and str(phase202["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase202_test_replay_allowed = int(phase202["test_replay_allowed_next"].iloc[0]) if not phase202.empty and str(phase202["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase202_promotion_allowed = int(phase202["promotion_allowed"].iloc[0]) if not phase202.empty and str(phase202["promotion_allowed"].iloc[0]) != "" else 0
    phase202_paper_live_allowed = int(phase202["paper_or_live_acceptance_allowed"].iloc[0]) if not phase202.empty and str(phase202["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase203_strategy_replay_allowed = int(phase203["strategy_replay_allowed"].iloc[0]) if not phase203.empty and str(phase203["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase203_test_replay_allowed = int(phase203["test_replay_allowed_next"].iloc[0]) if not phase203.empty and str(phase203["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase203_promotion_allowed = int(phase203["promotion_allowed"].iloc[0]) if not phase203.empty and str(phase203["promotion_allowed"].iloc[0]) != "" else 0
    phase203_paper_live_allowed = int(phase203["paper_or_live_acceptance_allowed"].iloc[0]) if not phase203.empty and str(phase203["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase204_strategy_replay_allowed = int(phase204["strategy_replay_allowed"].iloc[0]) if not phase204.empty and str(phase204["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase204_test_replay_allowed = int(phase204["test_replay_allowed_next"].iloc[0]) if not phase204.empty and str(phase204["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase204_promotion_allowed = int(phase204["promotion_allowed"].iloc[0]) if not phase204.empty and str(phase204["promotion_allowed"].iloc[0]) != "" else 0
    phase204_paper_live_allowed = int(phase204["paper_or_live_acceptance_allowed"].iloc[0]) if not phase204.empty and str(phase204["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase205_strategy_replay_allowed = int(phase205["strategy_replay_allowed"].iloc[0]) if not phase205.empty and str(phase205["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase205_test_replay_allowed = int(phase205["test_replay_allowed_next"].iloc[0]) if not phase205.empty and str(phase205["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase205_promotion_allowed = int(phase205["promotion_allowed"].iloc[0]) if not phase205.empty and str(phase205["promotion_allowed"].iloc[0]) != "" else 0
    phase205_paper_live_allowed = int(phase205["paper_or_live_acceptance_allowed"].iloc[0]) if not phase205.empty and str(phase205["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase206_model_fit_allowed = as_int(phase206_metrics.get("model_fit_allowed", 0))
    phase206_strategy_replay_allowed = int(phase206["strategy_replay_allowed"].iloc[0]) if not phase206.empty and str(phase206["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase206_test_replay_allowed = int(phase206["test_replay_allowed_next"].iloc[0]) if not phase206.empty and str(phase206["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase206_promotion_allowed = int(phase206["promotion_allowed"].iloc[0]) if not phase206.empty and str(phase206["promotion_allowed"].iloc[0]) != "" else 0
    phase206_paper_live_allowed = int(phase206["paper_or_live_acceptance_allowed"].iloc[0]) if not phase206.empty and str(phase206["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    phase207_metrics = phase_status_from_metrics(207)
    phase207_model_fit_allowed = as_int(phase207_metrics.get("model_fit_allowed", 0))
    phase207_strategy_replay_allowed = int(phase207["strategy_replay_allowed"].iloc[0]) if not phase207.empty and str(phase207["strategy_replay_allowed"].iloc[0]) != "" else 0
    phase207_test_replay_allowed = int(phase207["test_replay_allowed_next"].iloc[0]) if not phase207.empty and str(phase207["test_replay_allowed_next"].iloc[0]) != "" else 0
    phase207_promotion_allowed = int(phase207["promotion_allowed"].iloc[0]) if not phase207.empty and str(phase207["promotion_allowed"].iloc[0]) != "" else 0
    phase207_paper_live_allowed = int(phase207["paper_or_live_acceptance_allowed"].iloc[0]) if not phase207.empty and str(phase207["paper_or_live_acceptance_allowed"].iloc[0]) != "" else 0
    secure_download_recorded = bool(not phase174.empty and "secure_download" in str(phase174["status"].iloc[0]))
    feature_schema_recorded = bool(not phase175.empty and "feature_schema" in str(phase175["status"].iloc[0]))
    phase176_status = str(phase176["status"].iloc[0]) if not phase176.empty else ""
    materializer_recorded = bool(not phase176.empty and ("materializer" in phase176_status or "receive_flow_features_materialized" in phase176_status))
    quality_audit_recorded = bool(not phase177.empty and "quality_audit" in str(phase177["status"].iloc[0]))
    handoff_recorded = bool(not phase178.empty and "handoff" in str(phase178["status"].iloc[0]))
    strategy_precommit_recorded = bool(not phase179.empty and "strategy_family_precommitted" in str(phase179["status"].iloc[0]))
    cost_label_precommit_recorded = bool(not phase180.empty and "cost_latency_label_precommitted" in str(phase180["status"].iloc[0]))
    label_materialization_recorded = bool(not phase181.empty and "labels_materialized" in str(phase181["status"].iloc[0]))
    label_audit_recorded = bool(not phase182.empty and "label_quality_leakage_audited" in str(phase182["status"].iloc[0]))
    replay_readiness_recorded = bool(not phase183.empty and "replay_readiness_precommitted" in str(phase183["status"].iloc[0]))
    dry_run_recorded = bool(not phase184.empty and "train_validation_replay_dry_run_complete" in str(phase184["status"].iloc[0]))
    interpretation_recorded = bool(not phase185.empty and "validation_interpretation_cost_dominated" in str(phase185["status"].iloc[0]))
    closure_recorded = bool(not phase186.empty and "current_family_set_closed" in str(phase186["status"].iloc[0]))
    sparse_candidate_recorded = bool(not phase187.empty and "cost_aware_sparse_candidate" in str(phase187["status"].iloc[0]))
    sparse_interpretation_recorded = bool(not phase188.empty and "sparse_candidate_interpreted" in str(phase188["status"].iloc[0]))
    decision189_recorded = bool(not phase189.empty and "test_replay_deferred" in str(phase189["status"].iloc[0]))
    phase190_recorded = bool(not phase190.empty and "diagnostic_test_spec_written" in str(phase190["status"].iloc[0]))
    phase191_recorded = bool(not phase191.empty and "diagnostic_test_replay_precommitted" in str(phase191["status"].iloc[0]))
    phase192_recorded = bool(not phase192.empty and "real_validation_date_downloaded" in str(phase192["status"].iloc[0]))
    phase193_recorded = bool(not phase193.empty and "validation_breadth_extended" in str(phase193["status"].iloc[0]))
    phase194_recorded = bool(not phase194.empty and "frozen_sparse_candidate_closed" in str(phase194["status"].iloc[0]))
    phase195_recorded = bool(not phase195.empty and "redesign_search" in str(phase195["status"].iloc[0]))
    phase196_recorded = bool(not phase196.empty and "expanded_feature_model_search" in str(phase196["status"].iloc[0]))
    phase197_recorded = bool(not phase197.empty and "non_receive_flow_feature_expansion" in str(phase197["status"].iloc[0]))
    phase198_recorded = bool(not phase198.empty and "non_receive_flow_context_model_search" in str(phase198["status"].iloc[0]))
    phase199_recorded = bool(not phase199.empty and "branch_paused_material_redesign" in str(phase199["status"].iloc[0]))
    phase200_recorded = bool(not phase200.empty and "material_new_passive_queue_hypothesis" in str(phase200["status"].iloc[0]))
    phase201_recorded = bool(not phase201.empty and "passive_queue_stage01_label_expansion" in str(phase201["status"].iloc[0]))
    phase202_recorded = bool(not phase202.empty and "passive_feature_redesign" in str(phase202["status"].iloc[0]))
    phase203_recorded = bool(not phase203.empty and "redesigned_passive_labels_materialized" in str(phase203["status"].iloc[0]))
    phase204_recorded = bool(not phase204.empty and "passive_redesign_closed_for_replay" in str(phase204["status"].iloc[0]))
    phase205_recorded = bool(not phase205.empty and "material_new_source_precommitted" in str(phase205["status"].iloc[0]))
    phase206_recorded = bool(not phase206.empty and "selected_source_nonoverlap_feature_contract" in str(phase206["status"].iloc[0]))
    phase207_recorded = bool(not phase207.empty and "allowed_feature_matrix" in str(phase207["status"].iloc[0]))
    branch_closed = bool(not phase136.empty and "closed_clean_falsification" in str(phase136["status"].iloc[0]))
    rows = [
        ("phase149_real_l2_replay_gate_closed", bool(real_replay_allowed == 0), real_replay_allowed, 0, "hard"),
        ("phase149_real_receive_flow_source_gate_open_or_explicitly_blocked", bool(receive_replay_allowed in (0, 1)), receive_replay_allowed, "0_or_1_tracked_by_phase172", "hard"),
        ("phase149_secure_download_gate_recorded", secure_download_recorded, int(secure_download_recorded), 1, "hard"),
        ("phase149_secure_orchestrator_replay_gate_closed", bool(secure_replay_allowed == 0), secure_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_feature_schema_recorded", feature_schema_recorded, int(feature_schema_recorded), 1, "hard"),
        ("phase149_receive_flow_feature_schema_replay_gate_closed", bool(schema_replay_allowed == 0), schema_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_materializer_recorded", materializer_recorded, int(materializer_recorded), 1, "hard"),
        ("phase149_receive_flow_materializer_replay_gate_closed", bool(materializer_replay_allowed == 0), materializer_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_quality_audit_recorded", quality_audit_recorded, int(quality_audit_recorded), 1, "hard"),
        ("phase149_receive_flow_quality_audit_replay_gate_closed", bool(quality_replay_allowed == 0), quality_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_handoff_precommit_recorded", handoff_recorded, int(handoff_recorded), 1, "hard"),
        ("phase149_receive_flow_handoff_replay_gate_closed", bool(handoff_replay_allowed == 0), handoff_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_strategy_family_precommit_recorded", strategy_precommit_recorded, int(strategy_precommit_recorded), 1, "hard"),
        ("phase149_receive_flow_strategy_family_replay_gate_closed", bool(precommit_replay_allowed == 0), precommit_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_cost_latency_label_precommit_recorded", cost_label_precommit_recorded, int(cost_label_precommit_recorded), 1, "hard"),
        ("phase149_receive_flow_cost_latency_label_replay_gate_closed", bool(cost_label_replay_allowed == 0), cost_label_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_label_materialization_recorded", label_materialization_recorded, int(label_materialization_recorded), 1, "hard"),
        ("phase149_receive_flow_label_materialization_replay_gate_closed", bool(label_materialization_replay_allowed == 0), label_materialization_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_label_quality_leakage_audit_recorded", label_audit_recorded, int(label_audit_recorded), 1, "hard"),
        ("phase149_receive_flow_label_quality_leakage_replay_gate_closed", bool(label_audit_replay_allowed == 0), label_audit_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_replay_readiness_precommit_recorded", replay_readiness_recorded, int(replay_readiness_recorded), 1, "hard"),
        ("phase149_receive_flow_replay_readiness_replay_gate_closed", bool(replay_readiness_replay_allowed == 0), replay_readiness_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_replay_readiness_pnl_gate_closed", bool(replay_readiness_pnl_allowed == 0), replay_readiness_pnl_allowed, 0, "hard"),
        ("phase149_receive_flow_train_validation_dry_run_recorded", dry_run_recorded, int(dry_run_recorded), 1, "hard"),
        ("phase149_receive_flow_train_validation_dry_run_test_gate_closed", bool(dry_run_test_rows_used == 0), dry_run_test_rows_used, 0, "hard"),
        ("phase149_receive_flow_train_validation_dry_run_promotion_gate_closed", bool(dry_run_promotion_allowed == 0), dry_run_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_train_validation_dry_run_paper_live_gate_closed", bool(dry_run_paper_live_allowed == 0), dry_run_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_validation_interpretation_recorded", interpretation_recorded, int(interpretation_recorded), 1, "hard"),
        ("phase149_receive_flow_validation_interpretation_test_rows_closed", bool(interpretation_test_rows_used == 0), interpretation_test_rows_used, 0, "hard"),
        ("phase149_receive_flow_validation_interpretation_test_replay_closed", bool(interpretation_test_replay_allowed == 0), interpretation_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_validation_interpretation_promotion_closed", bool(interpretation_promotion_allowed == 0), interpretation_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_validation_interpretation_paper_live_closed", bool(interpretation_paper_live_allowed == 0), interpretation_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_current_family_closure_recorded", closure_recorded, int(closure_recorded), 1, "hard"),
        ("phase149_receive_flow_current_family_reuse_without_redesign_closed", bool(closure_reuse_allowed == 0), closure_reuse_allowed, 0, "hard"),
        ("phase149_receive_flow_current_family_closure_test_replay_closed", bool(closure_test_replay_allowed == 0), closure_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_current_family_closure_promotion_closed", bool(closure_promotion_allowed == 0), closure_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_current_family_closure_paper_live_closed", bool(closure_paper_live_allowed == 0), closure_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_cost_aware_sparse_candidate_recorded", sparse_candidate_recorded, int(sparse_candidate_recorded), 1, "hard"),
        ("phase149_receive_flow_cost_aware_sparse_candidate_test_rows_closed", bool(sparse_test_rows_used == 0), sparse_test_rows_used, 0, "hard"),
        ("phase149_receive_flow_cost_aware_sparse_candidate_test_replay_closed", bool(sparse_test_replay_allowed == 0), sparse_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_cost_aware_sparse_candidate_promotion_closed", bool(sparse_promotion_allowed == 0), sparse_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_cost_aware_sparse_candidate_paper_live_closed", bool(sparse_paper_live_allowed == 0), sparse_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_sparse_candidate_interpretation_recorded", sparse_interpretation_recorded, int(sparse_interpretation_recorded), 1, "hard"),
        ("phase149_receive_flow_sparse_candidate_interpretation_test_replay_closed", bool(interp188_test_replay_allowed == 0), interp188_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_sparse_candidate_interpretation_promotion_closed", bool(interp188_promotion_allowed == 0), interp188_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_sparse_candidate_interpretation_paper_live_closed", bool(interp188_paper_live_allowed == 0), interp188_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_test_precommit_decision_recorded", decision189_recorded, int(decision189_recorded), 1, "hard"),
        ("phase149_receive_flow_test_precommit_allowed_closed", bool(decision189_test_precommit_allowed == 0), decision189_test_precommit_allowed, 0, "hard"),
        ("phase149_receive_flow_test_replay_still_closed", bool(decision189_test_replay_allowed == 0), decision189_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_test_precommit_decision_promotion_closed", bool(decision189_promotion_allowed == 0), decision189_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_test_precommit_decision_paper_live_closed", bool(decision189_paper_live_allowed == 0), decision189_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase190_diagnostic_spec_recorded", phase190_recorded, int(phase190_recorded), 1, "hard"),
        ("phase149_receive_flow_phase190_test_replay_not_executed", bool(phase190_test_replay_execution == 0), phase190_test_replay_execution, 0, "hard"),
        ("phase149_receive_flow_phase190_test_replay_closed", bool(phase190_test_replay_allowed == 0), phase190_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase190_promotion_closed", bool(phase190_promotion_allowed == 0), phase190_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase190_paper_live_closed", bool(phase190_paper_live_allowed == 0), phase190_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase191_diagnostic_precommit_recorded", phase191_recorded, int(phase191_recorded), 1, "hard"),
        ("phase149_receive_flow_phase191_test_replay_not_executed", bool(phase191_test_replay_execution == 0), phase191_test_replay_execution, 0, "hard"),
        ("phase149_receive_flow_phase191_test_result_closed", bool(phase191_test_result_allowed == 0), phase191_test_result_allowed, 0, "hard"),
        ("phase149_receive_flow_phase191_test_replay_closed", bool(phase191_test_replay_allowed == 0), phase191_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase191_promotion_closed", bool(phase191_promotion_allowed == 0), phase191_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase191_paper_live_closed", bool(phase191_paper_live_allowed == 0), phase191_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase192_real_validation_download_recorded", phase192_recorded, int(phase192_recorded), 1, "hard"),
        ("phase149_receive_flow_phase192_test_replay_not_executed", bool(phase192_test_replay_execution == 0), phase192_test_replay_execution, 0, "hard"),
        ("phase149_receive_flow_phase192_test_result_closed", bool(phase192_test_result_allowed == 0), phase192_test_result_allowed, 0, "hard"),
        ("phase149_receive_flow_phase192_promotion_closed", bool(phase192_promotion_allowed == 0), phase192_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase192_paper_live_closed", bool(phase192_paper_live_allowed == 0), phase192_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase193_validation_extension_recorded", phase193_recorded, int(phase193_recorded), 1, "hard"),
        ("phase149_receive_flow_phase193_test_replay_not_executed", bool(phase193_test_replay_execution == 0), phase193_test_replay_execution, 0, "hard"),
        ("phase149_receive_flow_phase193_test_result_closed", bool(phase193_test_result_allowed == 0), phase193_test_result_allowed, 0, "hard"),
        ("phase149_receive_flow_phase193_promotion_closed", bool(phase193_promotion_allowed == 0), phase193_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase193_paper_live_closed", bool(phase193_paper_live_allowed == 0), phase193_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase194_fragility_decision_recorded", phase194_recorded, int(phase194_recorded), 1, "hard"),
        ("phase149_receive_flow_phase194_test_replay_closed", bool(phase194_test_replay_allowed == 0), phase194_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase194_promotion_closed", bool(phase194_promotion_allowed == 0), phase194_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase194_paper_live_closed", bool(phase194_paper_live_allowed == 0), phase194_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase195_redesign_search_recorded", phase195_recorded, int(phase195_recorded), 1, "hard"),
        ("phase149_receive_flow_phase195_test_replay_closed", bool(phase195_test_replay_allowed == 0), phase195_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase195_promotion_closed", bool(phase195_promotion_allowed == 0), phase195_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase195_paper_live_closed", bool(phase195_paper_live_allowed == 0), phase195_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase196_expanded_model_search_recorded", phase196_recorded, int(phase196_recorded), 1, "hard"),
        ("phase149_receive_flow_phase196_test_replay_closed", bool(phase196_test_replay_allowed == 0), phase196_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase196_promotion_closed", bool(phase196_promotion_allowed == 0), phase196_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase196_paper_live_closed", bool(phase196_paper_live_allowed == 0), phase196_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase197_non_receive_flow_feature_precommit_recorded", phase197_recorded, int(phase197_recorded), 1, "hard"),
        ("phase149_receive_flow_phase197_strategy_replay_closed", bool(phase197_strategy_replay_allowed == 0), phase197_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase197_test_replay_closed", bool(phase197_test_replay_allowed == 0), phase197_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase197_promotion_closed", bool(phase197_promotion_allowed == 0), phase197_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase197_paper_live_closed", bool(phase197_paper_live_allowed == 0), phase197_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase198_context_model_search_recorded", phase198_recorded, int(phase198_recorded), 1, "hard"),
        ("phase149_receive_flow_phase198_test_replay_closed", bool(phase198_test_replay_allowed == 0), phase198_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase198_promotion_closed", bool(phase198_promotion_allowed == 0), phase198_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase198_paper_live_closed", bool(phase198_paper_live_allowed == 0), phase198_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase199_branch_decision_recorded", phase199_recorded, int(phase199_recorded), 1, "hard"),
        ("phase149_receive_flow_phase199_strategy_replay_closed", bool(phase199_strategy_replay_allowed == 0), phase199_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase199_test_precommit_closed", bool(phase199_precommit_allowed == 0), phase199_precommit_allowed, 0, "hard"),
        ("phase149_receive_flow_phase199_test_replay_closed", bool(phase199_test_replay_allowed == 0), phase199_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase199_promotion_closed", bool(phase199_promotion_allowed == 0), phase199_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase199_paper_live_closed", bool(phase199_paper_live_allowed == 0), phase199_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase200_material_hypothesis_precommit_recorded", phase200_recorded, int(phase200_recorded), 1, "hard"),
        ("phase149_receive_flow_phase200_strategy_replay_closed", bool(phase200_strategy_replay_allowed == 0), phase200_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase200_test_replay_closed", bool(phase200_test_replay_allowed == 0), phase200_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase200_promotion_closed", bool(phase200_promotion_allowed == 0), phase200_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase200_paper_live_closed", bool(phase200_paper_live_allowed == 0), phase200_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase201_stage01_label_expansion_recorded", phase201_recorded, int(phase201_recorded), 1, "hard"),
        ("phase149_receive_flow_phase201_strategy_replay_closed", bool(phase201_strategy_replay_allowed == 0), phase201_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase201_test_replay_closed", bool(phase201_test_replay_allowed == 0), phase201_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase201_promotion_closed", bool(phase201_promotion_allowed == 0), phase201_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase201_paper_live_closed", bool(phase201_paper_live_allowed == 0), phase201_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase202_passive_feature_redesign_recorded", phase202_recorded, int(phase202_recorded), 1, "hard"),
        ("phase149_receive_flow_phase202_strategy_replay_closed", bool(phase202_strategy_replay_allowed == 0), phase202_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase202_test_replay_closed", bool(phase202_test_replay_allowed == 0), phase202_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase202_promotion_closed", bool(phase202_promotion_allowed == 0), phase202_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase202_paper_live_closed", bool(phase202_paper_live_allowed == 0), phase202_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase203_redesigned_label_materialization_recorded", phase203_recorded, int(phase203_recorded), 1, "hard"),
        ("phase149_receive_flow_phase203_strategy_replay_closed", bool(phase203_strategy_replay_allowed == 0), phase203_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase203_test_replay_closed", bool(phase203_test_replay_allowed == 0), phase203_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase203_promotion_closed", bool(phase203_promotion_allowed == 0), phase203_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase203_paper_live_closed", bool(phase203_paper_live_allowed == 0), phase203_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase204_passive_redesign_closure_recorded", phase204_recorded, int(phase204_recorded), 1, "hard"),
        ("phase149_receive_flow_phase204_strategy_replay_closed", bool(phase204_strategy_replay_allowed == 0), phase204_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase204_test_replay_closed", bool(phase204_test_replay_allowed == 0), phase204_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase204_promotion_closed", bool(phase204_promotion_allowed == 0), phase204_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase204_paper_live_closed", bool(phase204_paper_live_allowed == 0), phase204_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase205_material_new_source_precommit_recorded", phase205_recorded, int(phase205_recorded), 1, "hard"),
        ("phase149_receive_flow_phase205_strategy_replay_closed", bool(phase205_strategy_replay_allowed == 0), phase205_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase205_test_replay_closed", bool(phase205_test_replay_allowed == 0), phase205_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase205_promotion_closed", bool(phase205_promotion_allowed == 0), phase205_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase205_paper_live_closed", bool(phase205_paper_live_allowed == 0), phase205_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase206_nonoverlap_feature_contract_recorded", phase206_recorded, int(phase206_recorded), 1, "hard"),
        ("phase149_receive_flow_phase206_model_fit_closed", bool(phase206_model_fit_allowed == 0), phase206_model_fit_allowed, 0, "hard"),
        ("phase149_receive_flow_phase206_strategy_replay_closed", bool(phase206_strategy_replay_allowed == 0), phase206_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase206_test_replay_closed", bool(phase206_test_replay_allowed == 0), phase206_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase206_promotion_closed", bool(phase206_promotion_allowed == 0), phase206_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase206_paper_live_closed", bool(phase206_paper_live_allowed == 0), phase206_paper_live_allowed, 0, "hard"),
        ("phase149_receive_flow_phase207_allowed_feature_matrix_recorded", phase207_recorded, int(phase207_recorded), 1, "hard"),
        ("phase149_receive_flow_phase207_model_fit_closed", bool(phase207_model_fit_allowed == 0), phase207_model_fit_allowed, 0, "hard"),
        ("phase149_receive_flow_phase207_strategy_replay_closed", bool(phase207_strategy_replay_allowed == 0), phase207_strategy_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase207_test_replay_closed", bool(phase207_test_replay_allowed == 0), phase207_test_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_phase207_promotion_closed", bool(phase207_promotion_allowed == 0), phase207_promotion_allowed, 0, "hard"),
        ("phase149_receive_flow_phase207_paper_live_closed", bool(phase207_paper_live_allowed == 0), phase207_paper_live_allowed, 0, "hard"),
        ("phase149_deep_book_branch_closed", branch_closed, int(branch_closed), 1, "hard"),
        ("phase149_no_promoted_strategy_replay", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate", "pass", "observed", "required", "severity"])


def summarize(phase_ledger: pd.DataFrame, branch_summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    outputs_with_acceptance = int(phase_ledger["has_acceptance_summary"].astype(bool).sum()) if not phase_ledger.empty else 0
    script_phases = int(phase_ledger["has_runner"].astype(bool).sum()) if not phase_ledger.empty else 0
    receive_rows = branch_summary.loc[branch_summary["branch"].astype(str).eq("real_receive_flow_source"), "current_next_action"] if not branch_summary.empty else pd.Series(dtype=str)
    next_action = receive_rows.iloc[0] if not receive_rows.empty else "inspect_phase149_branch_status_summary"
    return pd.DataFrame(
        [
            ("phase149_phase_rows", int(len(phase_ledger)), "Phase rows discovered from scripts and outputs"),
            ("phase149_runner_phase_rows", script_phases, "Phase rows with at least one runner"),
            ("phase149_acceptance_phase_rows", outputs_with_acceptance, "Phase rows with acceptance summaries"),
            ("phase149_branch_rows", int(len(branch_summary)), "Current research branches summarized"),
            ("phase149_hard_gate_rows", int(len(hard)), "Hard global-state gates evaluated"),
            ("phase149_hard_gate_pass_rows", int(hard["pass"].astype(bool).sum()) if not hard.empty else 0, "Hard global-state gates passed"),
            ("phase149_strategy_replay_allowed", 0, "Phase149 never unlocks strategy replay"),
            ("phase149_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase149 Research State Auditor",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase149 reconciles current phase scripts, output evidence, branch states, and replay gates.",
        "It does not run strategies, contact Azure, import data, or unlock replay.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase149_research_state_auditor_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase149(output_dir: Path, base_dir: Path, scripts_root: Path, outputs_root: Path, plan_path: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    scripts = discover_script_phases(scripts_root)
    outputs = discover_output_phases(outputs_root)
    phase_ledger = build_phase_ledger(scripts, outputs)
    branch_summary = build_branch_summary(phase_ledger)
    gates = build_global_gates(phase_ledger)
    acceptance = summarize(phase_ledger, branch_summary, gates)

    scripts.to_csv(output_dir / "phase149_script_phase_inventory.csv", index=False)
    outputs.to_csv(output_dir / "phase149_output_phase_inventory.csv", index=False)
    phase_ledger.to_csv(output_dir / "phase149_phase_status_ledger.csv", index=False)
    branch_summary.to_csv(output_dir / "phase149_branch_status_summary.csv", index=False)
    gates.to_csv(output_dir / "phase149_global_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase149_research_state_auditor_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Branch Status Summary": branch_summary,
            "Global Gate Evaluation": gates,
            "Phase Status Ledger": phase_ledger.tail(80),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase149_research_state_auditor",
        **reproducibility_fields(
            artifact_id="phase149",
            generated_utc=generated_utc,
            inputs={
                "scripts_root": str(scripts_root),
                "outputs_root": str(outputs_root),
                "plan_path": str(plan_path),
            },
            parameters={
                "policy": "read_only_research_state_reconciliation",
                "strategy_replay_policy": "closed",
            },
            outputs={
                "script_phase_inventory": str(output_dir / "phase149_script_phase_inventory.csv"),
                "output_phase_inventory": str(output_dir / "phase149_output_phase_inventory.csv"),
                "phase_status_ledger": str(output_dir / "phase149_phase_status_ledger.csv"),
                "branch_status_summary": str(output_dir / "phase149_branch_status_summary.csv"),
                "global_gate_evaluation": str(output_dir / "phase149_global_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase149_research_state_auditor_acceptance_summary.csv"),
                "report": str(output_dir / "phase149_research_state_auditor_report.md"),
                "manifest": str(output_dir / "phase149_research_state_auditor_manifest.json"),
            },
            random_seed="none_deterministic_state_audit",
            scenario_ids="phase149_research_state_auditor",
            cost_model_version="not_applicable",
            latency_model_version="not_applicable",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase149_research_state_auditor_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit current research phase state and gates.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--scripts-root", type=Path, default=DEFAULT_SCRIPTS_ROOT)
    parser.add_argument("--outputs-root", type=Path, default=DEFAULT_OUTPUTS_ROOT)
    parser.add_argument("--plan-path", type=Path, default=DEFAULT_PLAN_PATH)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase149(args.output_dir, args.base_dir, args.scripts_root, args.outputs_root, args.plan_path)


if __name__ == "__main__":
    main()
