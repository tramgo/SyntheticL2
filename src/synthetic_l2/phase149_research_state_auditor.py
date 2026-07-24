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
    phase172 = phase_status_from_metrics(172)
    real_receive_next = phase177.get("next_action") or phase176.get("next_action") or phase175.get("next_action") or phase174.get("next_action") or phase172.get("next_action") or "run_phase174_or_phase172_according_to_latest_gate"
    real_receive_evidence = (
        f"Phase172 ready_dates={phase172.get('ready_receive_flow_dates', '')}, additional_dates_needed={phase172.get('additional_dates_needed', '')}; "
        f"Phase174 download_ran={phase174.get('download_ran', '')}; "
        f"Phase175 activation_ready={phase175.get('activation_ready', '')}; "
        f"Phase176 features_materialized={phase176.get('features_materialized', '')}; "
        f"Phase177 quality_audit_ran={phase177.get('feature_quality_audit_ran', '')}."
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
            "status": "gated_waiting_for_two_more_real_l2_dates",
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
    real_replay_allowed = int(phase148["strategy_replay_allowed"].iloc[0]) if not phase148.empty and str(phase148["strategy_replay_allowed"].iloc[0]) != "" else 0
    receive_replay_allowed = int(phase172["strategy_replay_allowed"].iloc[0]) if not phase172.empty and str(phase172["strategy_replay_allowed"].iloc[0]) != "" else 0
    secure_replay_allowed = int(phase174["strategy_replay_allowed"].iloc[0]) if not phase174.empty and str(phase174["strategy_replay_allowed"].iloc[0]) != "" else 0
    schema_replay_allowed = int(phase175["strategy_replay_allowed"].iloc[0]) if not phase175.empty and str(phase175["strategy_replay_allowed"].iloc[0]) != "" else 0
    materializer_replay_allowed = int(phase176["strategy_replay_allowed"].iloc[0]) if not phase176.empty and str(phase176["strategy_replay_allowed"].iloc[0]) != "" else 0
    quality_replay_allowed = int(phase177["strategy_replay_allowed"].iloc[0]) if not phase177.empty and str(phase177["strategy_replay_allowed"].iloc[0]) != "" else 0
    secure_download_recorded = bool(not phase174.empty and "secure_download" in str(phase174["status"].iloc[0]))
    feature_schema_recorded = bool(not phase175.empty and "feature_schema" in str(phase175["status"].iloc[0]))
    materializer_recorded = bool(not phase176.empty and "materializer" in str(phase176["status"].iloc[0]))
    quality_audit_recorded = bool(not phase177.empty and "quality_audit" in str(phase177["status"].iloc[0]))
    branch_closed = bool(not phase136.empty and "closed_clean_falsification" in str(phase136["status"].iloc[0]))
    rows = [
        ("phase149_real_l2_replay_gate_closed", bool(real_replay_allowed == 0), real_replay_allowed, 0, "hard"),
        ("phase149_real_receive_flow_replay_gate_closed", bool(receive_replay_allowed == 0), receive_replay_allowed, 0, "hard"),
        ("phase149_secure_download_gate_recorded", secure_download_recorded, int(secure_download_recorded), 1, "hard"),
        ("phase149_secure_orchestrator_replay_gate_closed", bool(secure_replay_allowed == 0), secure_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_feature_schema_recorded", feature_schema_recorded, int(feature_schema_recorded), 1, "hard"),
        ("phase149_receive_flow_feature_schema_replay_gate_closed", bool(schema_replay_allowed == 0), schema_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_materializer_recorded", materializer_recorded, int(materializer_recorded), 1, "hard"),
        ("phase149_receive_flow_materializer_replay_gate_closed", bool(materializer_replay_allowed == 0), materializer_replay_allowed, 0, "hard"),
        ("phase149_receive_flow_quality_audit_recorded", quality_audit_recorded, int(quality_audit_recorded), 1, "hard"),
        ("phase149_receive_flow_quality_audit_replay_gate_closed", bool(quality_replay_allowed == 0), quality_replay_allowed, 0, "hard"),
        ("phase149_deep_book_branch_closed", branch_closed, int(branch_closed), 1, "hard"),
        ("phase149_no_promoted_strategy_replay", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate", "pass", "observed", "required", "severity"])


def summarize(phase_ledger: pd.DataFrame, branch_summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    outputs_with_acceptance = int(phase_ledger["has_acceptance_summary"].astype(bool).sum()) if not phase_ledger.empty else 0
    script_phases = int(phase_ledger["has_runner"].astype(bool).sum()) if not phase_ledger.empty else 0
    return pd.DataFrame(
        [
            ("phase149_phase_rows", int(len(phase_ledger)), "Phase rows discovered from scripts and outputs"),
            ("phase149_runner_phase_rows", script_phases, "Phase rows with at least one runner"),
            ("phase149_acceptance_phase_rows", outputs_with_acceptance, "Phase rows with acceptance summaries"),
            ("phase149_branch_rows", int(len(branch_summary)), "Current research branches summarized"),
            ("phase149_hard_gate_rows", int(len(hard)), "Hard global-state gates evaluated"),
            ("phase149_hard_gate_pass_rows", int(hard["pass"].astype(bool).sum()) if not hard.empty else 0, "Hard global-state gates passed"),
            ("phase149_strategy_replay_allowed", 0, "Phase149 never unlocks strategy replay"),
            ("phase149_next_best_action", "add_AZURE_STORAGE_SAS_TOKEN_or_AZURE_STORAGE_KEY_then_rerun_phase174", "Recommended next milestone"),
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
