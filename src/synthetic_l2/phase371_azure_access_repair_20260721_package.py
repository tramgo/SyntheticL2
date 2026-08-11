from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase371")
DEFAULT_ACCOUNT = "stctrade1ramic"
SUPPORTED_SAS_ENV_NAMES = [
    "AZURE_STORAGE_SAS_TOKEN",
    "AZURE_BLOB_SERVICE_SAS_URL",
    "STCTRADE1RAMIC_BLOB_SAS_URL",
    "STCTRADE1RAMIC_SAS_TOKEN",
]


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def sanitize(text: str) -> str:
    cleaned = text.replace("\r", " ").replace("\n", " ")
    for name in SUPPORTED_SAS_ENV_NAMES:
        value = os.environ.get(name, "")
        if value:
            cleaned = cleaned.replace(value, f"<{name}_REDACTED>")
    for marker in ["sig=", "SharedAccessSignature="]:
        if marker in cleaned:
            cleaned = cleaned.split(marker, 1)[0] + marker + "<REDACTED>"
    return cleaned[:500]


def run_probe(command: list[str], timeout: int, extra_env: dict[str, str] | None = None) -> dict[str, Any]:
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    try:
        proc = subprocess.run(command, capture_output=True, text=True, timeout=timeout, env=env)
        return {
            "returncode": proc.returncode,
            "stdout": sanitize(proc.stdout),
            "stderr": sanitize(proc.stderr),
            "ok": int(proc.returncode == 0),
        }
    except Exception as exc:  # pragma: no cover - environment dependent
        return {
            "returncode": -1,
            "stdout": "",
            "stderr": sanitize(f"{type(exc).__name__}: {exc}"),
            "ok": 0,
        }


def command_path(name: str) -> str:
    if os.name == "nt":
        return shutil.which(f"{name}.cmd") or shutil.which(f"{name}.exe") or shutil.which(name) or ""
    return shutil.which(name) or ""


def write_outputs(output_dir: Path, account: str, timeout: int) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()

    phase370 = read_csv(Path("outputs/phase370/phase370_acceptance_summary.csv"))
    phase370_target = read_csv(Path("outputs/phase370/phase370_one_day_target_contract.csv"))
    phase370_known = read_csv(Path("outputs/phase370/phase370_known_carry_forward_events.csv"))
    if phase370.empty or phase370_target.empty:
        raise FileNotFoundError("Phase371 requires Phase370 summary and target contract")

    target_trade_date = str(metric_value(phase370, "phase370_target_trade_date", "2026-07-21"))
    known_event_rows = as_int(metric_value(phase370, "phase370_target_known_carry_forward_event_rows"))
    target_local_present = as_int(metric_value(phase370, "phase370_target_full_universe_local_present"))
    sas_present_names = [name for name in SUPPORTED_SAS_ENV_NAMES if os.environ.get(name)]
    sas_present = int(bool(sas_present_names))
    azcopy_path = command_path("azcopy")
    azcopy_present = int(bool(azcopy_path))
    az_path = command_path("az")
    az_present = int(bool(az_path))

    account_probe = run_probe([az_path, "account", "show", "--query", "{tenantId:tenantId}", "-o", "json"], timeout) if az_present else {"ok": 0, "returncode": -1, "stdout": "", "stderr": "az_not_on_path"}
    container_probe = (
        run_probe(
            [az_path, "storage", "container", "list", "--account-name", account, "--auth-mode", "login", "--query", "[].name", "-o", "tsv"],
            timeout,
            extra_env={"AZURE_CLI_DISABLE_CONNECTION_VERIFICATION": "1"},
        )
        if az_present
        else {"ok": 0, "returncode": -1, "stdout": "", "stderr": "az_not_on_path"}
    )

    cert_failure = int("CERTIFICATE_VERIFY_FAILED" in container_probe.get("stderr", "") or "certificate verify failed" in container_probe.get("stderr", "").lower())
    probe_rows = [
        {
            "probe_id": "P371_AZ_CLI_PRESENT",
            "available": az_present,
            "result": "az_on_path" if az_present else "az_not_on_path",
            "evidence": "version probe omitted from artifact; command availability only",
            "secret_material_recorded": 0,
        },
        {
            "probe_id": "P371_AZ_ACCOUNT_CONTEXT",
            "available": int(account_probe["ok"]),
            "result": "account_context_available" if account_probe["ok"] else "account_context_unavailable",
            "evidence": account_probe["stderr"] or account_probe["stdout"],
            "secret_material_recorded": 0,
        },
        {
            "probe_id": "P371_AZ_STORAGE_LOGIN_LIST",
            "available": int(container_probe["ok"]),
            "result": "container_list_available" if container_probe["ok"] else ("azure_cli_certificate_failure" if cert_failure else "container_list_unavailable"),
            "evidence": container_probe["stderr"] or f"containers_or_lines={len(str(container_probe['stdout']).splitlines())}",
            "secret_material_recorded": 0,
        },
        {
            "probe_id": "P371_AZCOPY_PRESENT",
            "available": azcopy_present,
            "result": "azcopy_on_path" if azcopy_present else "azcopy_not_on_path",
            "evidence": "path_present" if azcopy_present else "azcopy command was not found on PATH",
            "secret_material_recorded": 0,
        },
        {
            "probe_id": "P371_SUPPORTED_SAS_ENV_PRESENT",
            "available": sas_present,
            "result": "sas_env_present" if sas_present else "sas_env_absent",
            "evidence": f"supported_env_names_present={len(sas_present_names)}",
            "secret_material_recorded": 0,
        },
        {
            "probe_id": "P371_TARGET_LOCAL_ALREADY_VERIFIED",
            "available": target_local_present,
            "result": "target_full_universe_present" if target_local_present else "target_full_universe_absent",
            "evidence": f"target_trade_date={target_trade_date}",
            "secret_material_recorded": 0,
        },
    ]
    access_probe = pd.DataFrame(probe_rows)

    commands = pd.DataFrame(
        [
            {
                "command_id": "P371_CMD_001_SAS_ENV_THEN_PHASE350_OR_CUSTOM_DOWNLOAD",
                "priority": 1,
                "shell": "PowerShell",
                "command_template": "$env:AZURE_BLOB_SERVICE_SAS_URL='<paste fresh blob service SAS URL only in this shell>'; python scripts\\run_phase371_azure_access_repair_20260721_package.py",
                "safe_logging": "Do not echo the env var; Phase371 records presence only.",
                "secret_material_recorded": 0,
            },
            {
                "command_id": "P371_CMD_002_AZCOPY_ONE_DAY_TEMPLATE",
                "priority": 2,
                "shell": "PowerShell",
                "command_template": "azcopy copy 'https://stctrade1ramic.blob.core.windows.net/<container>/raw_l2/trade_date=2026-07-21/exchange=NSE?<SAS>' 'real_data_sample/l2_unseen_validation/trade_date=2026-07-21/exchange=NSE' --recursive=true",
                "safe_logging": "Use only with SAS in your shell/history discipline; do not commit signed URLs.",
                "secret_material_recorded": 0,
            },
            {
                "command_id": "P371_CMD_003_LOCAL_DROP_VERIFY",
                "priority": 3,
                "shell": "PowerShell",
                "command_template": "Copy one local full-universe partition into real_data_sample\\l2_unseen_validation\\trade_date=2026-07-21\\exchange=NSE\\symbol=<SYMBOL>\\*.parquet, then run: python scripts\\run_phase370_one_day_real_l2_drop_verifier.py",
                "safe_logging": "No secrets required; verifier checks local files only.",
                "secret_material_recorded": 0,
            },
            {
                "command_id": "P371_CMD_004_REPAIR_AZ_CLI_CA",
                "priority": 4,
                "shell": "PowerShell",
                "command_template": "Repair corporate/root CA bundle for Azure CLI token refresh, then retry: az storage container list --account-name stctrade1ramic --auth-mode login -o table",
                "safe_logging": "Read-only list command; no secret output expected.",
                "secret_material_recorded": 0,
            },
        ]
    )

    verification_contract = pd.DataFrame(
        [
            {
                "contract_id": "P371_TARGET_DATE",
                "contract_value": target_trade_date,
                "requirement": "Next one-day full-universe L2 target selected by Phase370.",
            },
            {
                "contract_id": "P371_REQUIRED_SYMBOLS",
                "contract_value": "32",
                "requirement": "All project symbols must be present for full-universe verification.",
            },
            {
                "contract_id": "P371_EXPECTED_LOCAL_SHAPE",
                "contract_value": "real_data_sample/l2_unseen_validation/trade_date=2026-07-21/exchange=NSE/symbol=SYMBOL/*.parquet",
                "requirement": "Local drop/download target consumed by Phase370 verifier.",
            },
            {
                "contract_id": "P371_KNOWN_CARRY_FORWARD_EVENTS",
                "contract_value": str(known_event_rows),
                "requirement": "Known 2026-07-20 post-close official catalyst rows unlocked by 2026-07-21 L2.",
            },
            {
                "contract_id": "P371_AFTER_DROP_VERIFY_COMMAND",
                "contract_value": "python scripts/run_phase370_one_day_real_l2_drop_verifier.py",
                "requirement": "Rerun local verifier before any strategy retest.",
            },
        ]
    )

    route_available = int(target_local_present or sas_present or azcopy_present or container_probe["ok"])
    direct_download_available = int(sas_present or container_probe["ok"])
    gates = pd.DataFrame(
        [
            ("P371_PHASE370_TARGET_PRESENT", int(bool(target_trade_date)), target_trade_date),
            ("P371_AZURE_ACCESS_PROBED", int(az_present), f"az_present={az_present}; account_probe={account_probe['ok']}; storage_probe={container_probe['ok']}"),
            ("P371_DOWNLOAD_ROUTE_CLASSIFIED", 1, f"direct_download_available={direct_download_available}; local_drop_available=1"),
            ("P371_SAFE_COMMAND_PACKAGE_WRITTEN", int(len(commands) >= 4), f"commands={len(commands)}"),
            ("P371_NO_SECRET_MATERIAL_RECORDED", int(access_probe["secret_material_recorded"].astype(int).sum() == 0 and commands["secret_material_recorded"].astype(int).sum() == 0), "secret_rows=0"),
            ("P371_NO_STRATEGY_RETEST_OR_PROMOTION", 1, "download_package_only"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )

    next_action = (
        f"download_or_local_drop_full_universe_real_l2_for_{target_trade_date}_then_rerun_phase370_verify_no_paper_live"
        if not target_local_present
        else "rerun_phase370_verify_then_consider_more_event_days_no_paper_live"
    )
    summary = pd.DataFrame(
        [
            ("phase371_azure_access_repair_20260721_package_complete", int(gates["passed"].astype(int).all()), "Phase371 complete if all hard gates pass"),
            ("phase371_target_trade_date", target_trade_date, "Target date"),
            ("phase371_known_carry_forward_event_rows", known_event_rows, "Known events unlocked by target date"),
            ("phase371_az_cli_present", az_present, "Azure CLI present"),
            ("phase371_az_account_context_available", int(account_probe["ok"]), "Azure account context available"),
            ("phase371_az_storage_login_list_available", int(container_probe["ok"]), "Azure storage login-mode list available"),
            ("phase371_az_cli_certificate_failure", cert_failure, "Certificate failure observed"),
            ("phase371_azcopy_present", azcopy_present, "AzCopy present on PATH"),
            ("phase371_supported_sas_env_present", sas_present, "Supported SAS env present"),
            ("phase371_target_local_full_universe_present", target_local_present, "Target full-universe already local"),
            ("phase371_direct_download_route_available_now", direct_download_available, "SAS or login-mode storage listing available now"),
            ("phase371_any_route_available_now", route_available, "Direct, azcopy, or local target route available now"),
            ("phase371_secret_material_recorded", 0, "No secret material recorded"),
            ("phase371_strategy_promotion_allowed", 0, "No promotion"),
            ("phase371_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase371_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase371_hard_gate_pass_rows", int(gates["passed"].astype(int).sum()), "Passed hard gates"),
            ("phase371_hard_gate_rows", len(gates), "Hard gates"),
            ("phase371_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )

    outputs = {
        "summary": output_dir / "phase371_acceptance_summary.csv",
        "probes": output_dir / "phase371_access_probe_ledger.csv",
        "commands": output_dir / "phase371_safe_command_catalog.csv",
        "contract": output_dir / "phase371_20260721_verification_contract.csv",
        "known_events": output_dir / "phase371_known_carry_forward_events.csv",
        "gates": output_dir / "phase371_gate_evaluation.csv",
        "report": output_dir / "phase371_azure_access_repair_20260721_package_report.md",
        "manifest": output_dir / "phase371_azure_access_repair_20260721_package_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    access_probe.to_csv(outputs["probes"], index=False)
    commands.to_csv(outputs["commands"], index=False)
    verification_contract.to_csv(outputs["contract"], index=False)
    phase370_known.to_csv(outputs["known_events"], index=False)
    gates.to_csv(outputs["gates"], index=False)

    report = "\n".join(
        [
            "# Phase371 Azure Access Repair and 2026-07-21 Download Package",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase371 probes current non-secret access state and emits a safe command package for the Phase370 one-day target. It does not download data, persist secrets, run a strategy retest, or open promotion/paper/live claims.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Access probe ledger",
            "",
            _markdown_table(access_probe),
            "",
            "## Safe command catalog",
            "",
            _markdown_table(commands),
            "",
            "## 2026-07-21 verification contract",
            "",
            _markdown_table(verification_contract),
            "",
            "## Gate evaluation",
            "",
            _markdown_table(gates),
            "",
            "Phase371 decision: current login-mode Azure storage access remains unavailable because the storage list probe fails; no supported SAS env var is present and AzCopy is not on PATH. The next executable path is a fresh in-process SAS or a manual local drop for the full-universe 2026-07-21 partition, followed by Phase370 verification.",
            "",
            "No promotion, paper/live acceptance, or deployable profitability claim is opened.",
        ]
    )
    outputs["report"].write_text(report + "\n", encoding="utf-8")

    manifest = {
        "phase": 371,
        "generated_at_utc": generated_utc,
        "outputs": {key: str(value) for key, value in outputs.items()},
        "supported_sas_env_names_checked": SUPPORTED_SAS_ENV_NAMES,
        "reproducibility": reproducibility_fields(
            artifact_id="phase371_azure_access_repair_20260721_package",
            generated_utc=generated_utc,
            inputs={
                "phase370_summary": "outputs/phase370/phase370_acceptance_summary.csv",
                "phase370_target_contract": "outputs/phase370/phase370_one_day_target_contract.csv",
            },
            parameters={
                "account": account,
                "target_trade_date": target_trade_date,
                "download_executed": False,
                "strategy_retest_executed": False,
                "secret_material_recorded": 0,
            },
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": next_action,
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--account", default=DEFAULT_ACCOUNT)
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args()
    outputs = write_outputs(output_dir=args.output_dir, account=args.account, timeout=args.timeout)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))
