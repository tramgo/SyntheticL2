from __future__ import annotations

import argparse
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_OUTPUT_DIR = Path("outputs/phase173")
DEFAULT_PHASE172_SUMMARY = Path("outputs/phase172/phase172_real_l2_receive_flow_availability_acceptance_summary.csv")
DEFAULT_PHASE148_SUMMARY = Path("outputs/phase148/phase148_real_l2_download_refresh_workflow_acceptance_summary.csv")
DEFAULT_PHASE147_SUMMARY = Path("outputs/phase147/phase147_azcopy_download_intake_audit_acceptance_summary.csv")
DEFAULT_PHASE146_SUMMARY = Path("outputs/phase146/phase146_real_anchor_minimum_unlock_audit_acceptance_summary.csv")
DEFAULT_DATES = ["2026-07-10", "2026-07-14"]
DEFAULT_STORAGE_ACCOUNT = "stctrade1ramic"
DEFAULT_SHARE_NAME = "ctrade1-l2-data"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["metric", "value", "description"])
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = "") -> Any:
    if frame.empty or "metric" not in frame.columns or "value" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def find_azcopy() -> str:
    found = shutil.which("azcopy.exe") or shutil.which("azcopy")
    if found:
        return found
    temp = os.environ.get("TEMP")
    if not temp:
        return ""
    root = Path(temp)
    if not root.exists():
        return ""
    candidates = sorted(root.rglob("azcopy.exe"), key=lambda path: path.stat().st_mtime, reverse=True)
    return str(candidates[0]) if candidates else ""


def build_preflight(
    phase172: pd.DataFrame,
    phase148: pd.DataFrame,
    phase147: pd.DataFrame,
    phase146: pd.DataFrame,
    dates: list[str],
    storage_account: str,
    share_name: str,
    azure_cli_probe_status: str,
    azure_cli_probe_evidence: str,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    sas_present = bool(os.environ.get("AZURE_STORAGE_SAS_TOKEN", "").strip())
    key_present = bool(os.environ.get("AZURE_STORAGE_KEY", "").strip())
    azcopy_path = find_azcopy()
    phase172_ready = as_int(metric_value(phase172, "phase172_ready_receive_flow_dates", 0))
    phase172_needed = as_int(metric_value(phase172, "phase172_additional_dates_needed", 2), 2)
    phase148_download_ran = as_int(metric_value(phase148, "phase148_download_ran", 0))
    phase147_satisfied = as_int(metric_value(phase147, "phase147_required_dates_satisfied", 0))
    phase146_replay = as_int(metric_value(phase146, "phase146_strategy_replay_allowed", 0))
    phase146_needed = as_int(metric_value(phase146, "phase146_days_needed_for_min", phase172_needed), phase172_needed)
    credential_ready = bool(sas_present or key_present)
    azure_cli_usable = azure_cli_probe_status == "ok"
    download_ready = bool(azcopy_path and credential_ready)
    if download_ready:
        next_action = "run_phase148_with_download_for_required_dates_then_rerun_phase172"
    elif azure_cli_usable:
        next_action = "generate_read_list_sas_or_account_key_then_run_phase148_download"
    else:
        next_action = "provide_share_sas_or_storage_key_or_repair_azure_cli_tls_then_run_phase148_download"

    evidence = pd.DataFrame(
        [
            ("phase173_storage_account", storage_account, "Configured Azure Files storage account"),
            ("phase173_share_name", share_name, "Configured Azure Files share"),
            ("phase173_required_dates", ",".join(dates), "Real L2 dates needed to satisfy Phase172 minimum"),
            ("phase173_azcopy_path", azcopy_path, "Resolved AzCopy executable path, if present"),
            ("phase173_azcopy_available", int(bool(azcopy_path)), "1 means AzCopy can be launched"),
            ("phase173_sas_token_available_in_env", int(sas_present), "1 means AZURE_STORAGE_SAS_TOKEN is set; value is never recorded"),
            ("phase173_account_key_available_in_env", int(key_present), "1 means AZURE_STORAGE_KEY is set; value is never recorded"),
            ("phase173_azure_cli_probe_status", azure_cli_probe_status, "Current Azure CLI metadata/auth probe result"),
            ("phase173_azure_cli_probe_evidence", azure_cli_probe_evidence, "Redacted CLI evidence captured outside secret values"),
            ("phase173_phase172_ready_receive_flow_dates", phase172_ready, "Ready local receive-flow dates from Phase172"),
            ("phase173_phase172_additional_dates_needed", phase172_needed, "Additional complete local real L2 dates needed"),
            ("phase173_phase148_download_ran", phase148_download_ran, "Latest Phase148 download flag"),
            ("phase173_phase147_required_dates_satisfied", phase147_satisfied, "Latest local intake satisfied date count"),
            ("phase173_phase146_days_needed_for_min", phase146_needed, "Latest real-anchor gate days still needed"),
            ("phase173_phase146_strategy_replay_allowed", phase146_replay, "Latest real-anchor replay gate"),
        ],
        columns=["metric", "value", "description"],
    )
    gates = pd.DataFrame(
        [
            {
                "gate_id": "P173_AZCOPY_AVAILABLE",
                "gate_pass": int(bool(azcopy_path)),
                "evidence": "azcopy resolved" if azcopy_path else "azcopy not found",
                "severity": "hard_for_download",
            },
            {
                "gate_id": "P173_DOWNLOAD_CREDENTIAL_AVAILABLE",
                "gate_pass": int(credential_ready),
                "evidence": f"sas_env={int(sas_present)};account_key_env={int(key_present)}",
                "severity": "hard_for_download",
            },
            {
                "gate_id": "P173_AZURE_CLI_USABLE_FOR_SAS",
                "gate_pass": int(azure_cli_usable),
                "evidence": azure_cli_probe_evidence,
                "severity": "alternative_path",
            },
            {
                "gate_id": "P173_TWO_DATES_STILL_REQUIRED",
                "gate_pass": int(phase172_needed >= 2 and phase146_needed >= 2),
                "evidence": f"phase172_needed={phase172_needed};phase146_needed={phase146_needed}",
                "severity": "status",
            },
            {
                "gate_id": "P173_REPLAY_REMAINS_CLOSED",
                "gate_pass": int(phase146_replay == 0),
                "evidence": f"phase146_strategy_replay_allowed={phase146_replay}",
                "severity": "safety",
            },
        ]
    )
    summary = pd.DataFrame(
        [
            ("phase173_required_date_rows", len(dates), "Dates required for next acquisition attempt"),
            ("phase173_azcopy_available", int(bool(azcopy_path)), "AzCopy availability"),
            ("phase173_download_credential_available", int(credential_ready), "SAS or account key available in environment"),
            ("phase173_azure_cli_usable_for_sas", int(azure_cli_usable), "Azure CLI can be used to generate or locate download credentials"),
            ("phase173_download_ready_now", int(download_ready), "1 means Phase148 can run download immediately"),
            ("phase173_additional_dates_needed", max(phase172_needed, phase146_needed), "Additional complete local real L2 dates still needed"),
            ("phase173_strategy_replay_allowed", 0, "Credential preflight never opens replay"),
            ("phase173_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase173_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    return evidence, gates, summary


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase173 Real L2 Download Credential Preflight",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase173 records whether the next two-date real L2 download can be executed now.",
        "It never records SAS signatures, account keys, passwords, or broker credentials.",
        "It does not contact Azure, run AzCopy, import data, unlock replay, or run strategy P&L.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase173_real_l2_download_credential_preflight_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase173(
    output_dir: Path,
    base_dir: Path,
    phase172_summary: Path,
    phase148_summary: Path,
    phase147_summary: Path,
    phase146_summary: Path,
    dates: list[str],
    storage_account: str,
    share_name: str,
    azure_cli_probe_status: str,
    azure_cli_probe_evidence: str,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase172 = read_csv(phase172_summary)
    phase148 = read_csv(phase148_summary)
    phase147 = read_csv(phase147_summary)
    phase146 = read_csv(phase146_summary)
    evidence, gates, summary = build_preflight(
        phase172,
        phase148,
        phase147,
        phase146,
        dates,
        storage_account,
        share_name,
        azure_cli_probe_status,
        azure_cli_probe_evidence,
    )
    evidence.to_csv(output_dir / "phase173_download_preflight_evidence.csv", index=False)
    gates.to_csv(output_dir / "phase173_download_preflight_gate_evaluation.csv", index=False)
    summary.to_csv(output_dir / "phase173_real_l2_download_credential_preflight_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": summary,
            "Preflight Evidence": evidence,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase173_real_l2_download_credential_preflight",
        **reproducibility_fields(
            artifact_id="phase173_real_l2_download_credential_preflight",
            generated_utc=generated,
            inputs={
                "phase172_summary": str(phase172_summary),
                "phase148_summary": str(phase148_summary),
                "phase147_summary": str(phase147_summary),
                "phase146_summary": str(phase146_summary),
            },
            parameters={
                "required_dates": dates,
                "storage_account": storage_account,
                "share_name": share_name,
                "secrets_recorded": "none",
                "azure_contact_policy": "none_in_phase173",
                "strategy_replay_policy": "closed",
            },
            outputs={
                "evidence": str(output_dir / "phase173_download_preflight_evidence.csv"),
                "gate_evaluation": str(output_dir / "phase173_download_preflight_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase173_real_l2_download_credential_preflight_acceptance_summary.csv"),
                "report": str(output_dir / "phase173_real_l2_download_credential_preflight_report.md"),
            },
            random_seed="none_deterministic_preflight",
            scenario_ids="phase172_requires_two_more_real_l2_dates",
            cost_model_version="not_applicable_no_replay",
            latency_model_version="not_applicable_no_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase173_real_l2_download_credential_preflight_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--phase172-summary", type=Path, default=DEFAULT_PHASE172_SUMMARY)
    parser.add_argument("--phase148-summary", type=Path, default=DEFAULT_PHASE148_SUMMARY)
    parser.add_argument("--phase147-summary", type=Path, default=DEFAULT_PHASE147_SUMMARY)
    parser.add_argument("--phase146-summary", type=Path, default=DEFAULT_PHASE146_SUMMARY)
    parser.add_argument("--dates", nargs="+", default=DEFAULT_DATES)
    parser.add_argument("--storage-account", default=DEFAULT_STORAGE_ACCOUNT)
    parser.add_argument("--share-name", default=DEFAULT_SHARE_NAME)
    parser.add_argument("--azure-cli-probe-status", default="not_run")
    parser.add_argument("--azure-cli-probe-evidence", default="not_run")
    args = parser.parse_args()
    dates: list[str] = []
    for item in args.dates:
        dates.extend(part.strip() for part in str(item).split(",") if part.strip())
    run_phase173(
        args.output_dir,
        args.base_dir,
        args.phase172_summary,
        args.phase148_summary,
        args.phase147_summary,
        args.phase146_summary,
        dates,
        args.storage_account,
        args.share_name,
        args.azure_cli_probe_status,
        args.azure_cli_probe_evidence,
    )


if __name__ == "__main__":
    main()
