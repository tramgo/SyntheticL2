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


DEFAULT_PHASE238_DIR = Path("outputs/phase238")
DEFAULT_RAW_ROOTS = [
    Path("real_data_sample/l2_multiday_panel"),
    Path("scratch_azcopy_selected/raw_l2"),
]
DEFAULT_DERIVED_ROOT = Path("derived_real_l2_receive_flow_features_phase176")
DEFAULT_OUTPUT_DIR = Path("outputs/phase239")
MIN_UNSEEN_VALIDATION_DATES = 5
TARGET_UNSEEN_DATES = ["2026-07-17", "2026-07-20", "2026-07-21", "2026-07-22", "2026-07-23"]
STORAGE_ACCOUNT = "stctrade1ramic"
FILE_SHARE = "ctrade1-l2-data"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns or "value" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def discover_dates_under(root: Path) -> list[str]:
    if not root.exists():
        return []
    dates: set[str] = set()
    for part in root.rglob("trade_date=*"):
        if part.is_dir() and part.name.startswith("trade_date="):
            dates.add(part.name.split("=", 1)[1])
    return sorted(dates)


def build_local_inventory(phase238_dir: Path, raw_roots: list[Path], derived_root: Path) -> tuple[pd.DataFrame, list[str]]:
    availability = read_csv(phase238_dir / "phase238_validation_data_availability.csv")
    discovery_dates: set[str] = set()
    rows = availability[
        availability.get("availability_check", pd.Series(dtype=str)).astype(str).eq(
            "P238_CURRENT_LOCAL_DATES_DISCOVERY_CONTAMINATED"
        )
    ]
    if not rows.empty:
        discovery_dates.update(str(rows["observed_value"].iloc[0]).split(";"))
    inventory: list[dict[str, Any]] = []
    all_dates: set[str] = set()
    for root in raw_roots:
        dates = discover_dates_under(root)
        all_dates.update(dates)
        for d in dates:
            inventory.append(
                {
                    "root": str(root),
                    "data_kind": "raw_l2_parquet",
                    "trade_date": d,
                    "is_phase237_discovery_date": d in discovery_dates,
                    "is_unseen_candidate_date": d not in discovery_dates,
                }
            )
    derived_dates = discover_dates_under(derived_root)
    all_dates.update(derived_dates)
    for d in derived_dates:
        inventory.append(
            {
                "root": str(derived_root),
                "data_kind": "derived_receive_flow_features",
                "trade_date": d,
                "is_phase237_discovery_date": d in discovery_dates,
                "is_unseen_candidate_date": d not in discovery_dates,
            }
        )
    return pd.DataFrame(inventory), sorted(d for d in all_dates if d and d not in discovery_dates)


def run_command(args: list[str], timeout: int = 30) -> tuple[int, str]:
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        output = (proc.stdout or "") + (proc.stderr or "")
        return int(proc.returncode), output.strip()[:2000]
    except Exception as exc:
        return -1, repr(exc)


def build_azure_preflight() -> pd.DataFrame:
    az_path = shutil.which("az")
    azcopy_path = shutil.which("azcopy")
    env_sas = os.environ.get("AZURE_STORAGE_SAS_TOKEN") or os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    rows: list[dict[str, Any]] = [
        {
            "check_id": "P239_AZ_CLI_AVAILABLE",
            "passed": bool(az_path),
            "observed_value": az_path or "",
            "required_value": "az on PATH or SDK credential alternative",
            "interpretation": "Azure CLI is available for a possible download path." if az_path else "Azure CLI is not available.",
        },
        {
            "check_id": "P239_AZCOPY_AVAILABLE",
            "passed": bool(azcopy_path),
            "observed_value": azcopy_path or "",
            "required_value": "azcopy optional",
            "interpretation": "AzCopy is available." if azcopy_path else "AzCopy is not on PATH; use Azure CLI or Python SDK download path.",
        },
        {
            "check_id": "P239_CURRENT_PROCESS_STORAGE_SECRET_AVAILABLE",
            "passed": bool(env_sas),
            "observed_value": "present" if env_sas else "absent",
            "required_value": "fresh SAS/connection string or working az login",
            "interpretation": "A current-process storage secret exists." if env_sas else "No storage SAS/connection string is available in this process.",
        },
    ]
    if az_path:
        code, output = run_command(
            [
                "az",
                "storage",
                "container",
                "list",
                "--account-name",
                STORAGE_ACCOUNT,
                "--auth-mode",
                "login",
                "--query",
                "[].name",
                "-o",
                "tsv",
            ],
            timeout=30,
        )
        rows.append(
            {
                "check_id": "P239_AZ_LOGIN_STORAGE_LIST_READABLE",
                "passed": code == 0,
                "observed_value": "success" if code == 0 else output.replace("\n", " ")[:500],
                "required_value": "readable storage container listing",
                "interpretation": "Azure login can list containers." if code == 0 else "Azure CLI storage listing failed before data download.",
            }
        )
    else:
        rows.append(
            {
                "check_id": "P239_AZ_LOGIN_STORAGE_LIST_READABLE",
                "passed": False,
                "observed_value": "az missing",
                "required_value": "readable storage container listing",
                "interpretation": "Cannot list storage containers without Azure CLI or SDK credentials.",
            }
        )
    if os.environ.get("AZURE_STORAGE_SAS_TOKEN"):
        try:
            import truststore
            from azure.storage.fileshare import ShareServiceClient

            truststore.inject_into_ssl()
            svc = ShareServiceClient(
                account_url=f"https://{STORAGE_ACCOUNT}.file.core.windows.net",
                credential=os.environ["AZURE_STORAGE_SAS_TOKEN"],
            )
            shares = [item["name"] for item in svc.list_shares()]
            share_ready = FILE_SHARE in shares
            rows.append(
                {
                    "check_id": "P239_FILE_SERVICE_SAS_SHARE_READABLE",
                    "passed": share_ready,
                    "observed_value": FILE_SHARE if share_ready else ";".join(shares),
                    "required_value": FILE_SHARE,
                    "interpretation": "SAS can read the Azure Files L2 share." if share_ready else "SAS could list shares but the expected L2 share was not found.",
                }
            )
            if share_ready:
                share = svc.get_share_client(FILE_SHARE)
                raw = share.get_directory_client("raw_l2")
                dates = sorted(
                    item["name"].split("=", 1)[1]
                    for item in raw.list_directories_and_files()
                    if str(item["name"]).startswith("trade_date=")
                )
                rows.append(
                    {
                        "check_id": "P239_FILE_SERVICE_RAW_L2_DATES_READABLE",
                        "passed": bool(dates),
                        "observed_value": ";".join(dates),
                        "required_value": "raw_l2/trade_date=*",
                        "interpretation": "SAS can list raw_l2 trade-date directories.",
                    }
                )
                target_available = [d for d in TARGET_UNSEEN_DATES if d in dates]
                rows.append(
                    {
                        "check_id": "P239_FILE_SERVICE_TARGET_UNSEEN_DATES_AVAILABLE",
                        "passed": len(target_available) >= MIN_UNSEEN_VALIDATION_DATES,
                        "observed_value": ";".join(target_available),
                        "required_value": ";".join(TARGET_UNSEEN_DATES),
                        "interpretation": "All target unseen dates are visible in Azure Files raw_l2."
                        if len(target_available) >= MIN_UNSEEN_VALIDATION_DATES
                        else "Not enough target unseen dates are visible in Azure Files raw_l2.",
                    }
                )
        except Exception as exc:
            rows.append(
                {
                    "check_id": "P239_FILE_SERVICE_SAS_SHARE_READABLE",
                    "passed": False,
                    "observed_value": repr(exc)[:500],
                    "required_value": FILE_SHARE,
                    "interpretation": "Azure Files SAS preflight failed before download.",
                }
            )
    else:
        rows.append(
            {
                "check_id": "P239_FILE_SERVICE_SAS_SHARE_READABLE",
                "passed": False,
                "observed_value": "no AZURE_STORAGE_SAS_TOKEN in process",
                "required_value": FILE_SHARE,
                "interpretation": "Provide a fresh SAS token in the process environment to use the Azure Files SDK path.",
            }
        )
    return pd.DataFrame(rows)


def build_target_date_plan(local_unseen_dates: list[str]) -> pd.DataFrame:
    rows = []
    for d in TARGET_UNSEEN_DATES:
        rows.append(
            {
                "target_trade_date": d,
                "already_materialized_locally": d in local_unseen_dates,
                "required_for_phase238_primary_validation": True,
                "expected_source_prefix": f"raw_l2/trade_date={d}/exchange=NSE/",
                "target_raw_root": f"real_data_sample/l2_unseen_validation/trade_date={d}/exchange=NSE/",
                "target_feature_root": f"derived_real_l2_receive_flow_features_phase239/trade_date={d}/exchange=NSE/",
                "holiday_calendar_check_required": True,
            }
        )
    return pd.DataFrame(rows)


def build_download_plan(azure_preflight: pd.DataFrame, target_dates: pd.DataFrame) -> pd.DataFrame:
    az_ok = bool(
        not azure_preflight.empty
        and azure_preflight.loc[
            azure_preflight["check_id"].astype(str).eq("P239_AZ_LOGIN_STORAGE_LIST_READABLE"), "passed"
        ].astype(bool).any()
    )
    file_sas_ok = bool(
        not azure_preflight.empty
        and azure_preflight.loc[
            azure_preflight["check_id"].astype(str).eq("P239_FILE_SERVICE_TARGET_UNSEEN_DATES_AVAILABLE"), "passed"
        ].astype(bool).any()
    )
    rows = []
    for d in target_dates["target_trade_date"].astype(str).tolist():
        rows.append(
            {
                "step_order": len(rows) + 1,
                "download_task": "download_raw_l2_date",
                "trade_date": d,
                "preferred_method": "azure_files_python_sdk" if file_sas_ok else "azure_cli_or_python_sdk",
                "ready_to_execute_now": int(az_ok or file_sas_ok),
                "source": f"{STORAGE_ACCOUNT}/{FILE_SHARE}:raw_l2/trade_date={d}/exchange=NSE/",
                "destination": f"real_data_sample/l2_unseen_validation/trade_date={d}/exchange=NSE/",
                "notes": "Execute only with fresh SAS/working az login and TLS trust fixed; do not print secrets.",
            }
        )
    rows.append(
        {
            "step_order": len(rows) + 1,
            "download_task": "materialize_phase235_adapter_features",
            "trade_date": ";".join(target_dates["target_trade_date"].astype(str).tolist()),
            "preferred_method": "reuse_phase176_materializer_contract",
            "ready_to_execute_now": 0,
            "source": "real_data_sample/l2_unseen_validation/",
            "destination": "derived_real_l2_receive_flow_features_phase239/",
            "notes": "Run after raw unseen dates are downloaded and schema/date/symbol coverage is verified.",
        }
    )
    rows.append(
        {
            "step_order": len(rows) + 1,
            "download_task": "run_frozen_phase237_validation",
            "trade_date": ";".join(target_dates["target_trade_date"].astype(str).tolist()),
            "preferred_method": "phase240_or_phase239_validation_runner",
            "ready_to_execute_now": 0,
            "source": "derived_real_l2_receive_flow_features_phase239/",
            "destination": "outputs/phase240/",
            "notes": "Apply frozen Phase238 candidate only; no threshold tuning on unseen validation dates.",
        }
    )
    return pd.DataFrame(rows)


def build_gate_evaluation(local_inventory: pd.DataFrame, azure_preflight: pd.DataFrame, download_plan: pd.DataFrame) -> pd.DataFrame:
    unseen_local_dates = (
        local_inventory[local_inventory["is_unseen_candidate_date"].astype(bool)]["trade_date"].nunique()
        if not local_inventory.empty
        else 0
    )
    az_readable = bool(
        not azure_preflight.empty
        and azure_preflight.loc[
            azure_preflight["check_id"].astype(str).eq("P239_AZ_LOGIN_STORAGE_LIST_READABLE"), "passed"
        ].astype(bool).any()
    )
    file_sas_readable = bool(
        not azure_preflight.empty
        and azure_preflight.loc[
            azure_preflight["check_id"].astype(str).eq("P239_FILE_SERVICE_TARGET_UNSEEN_DATES_AVAILABLE"), "passed"
        ].astype(bool).any()
    )
    rows = [
        ("P239_LOCAL_UNSEEN_DATES_AVAILABLE", unseen_local_dates >= MIN_UNSEEN_VALIDATION_DATES, unseen_local_dates, f">={MIN_UNSEEN_VALIDATION_DATES}", "hard"),
        ("P239_AZURE_DOWNLOAD_READY_NOW", az_readable or file_sas_readable, int(az_readable or file_sas_readable), 1, "soft"),
        ("P239_TARGET_UNSEEN_DATE_PLAN_WRITTEN", True, len(TARGET_UNSEEN_DATES), MIN_UNSEEN_VALIDATION_DATES, "hard"),
        ("P239_DOWNLOAD_AND_MATERIALIZATION_PLAN_WRITTEN", not download_plan.empty, len(download_plan), ">0 rows", "hard"),
        ("P239_NO_VALIDATION_OR_PROMOTION_UNLOCK", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase239 Unseen-date Acquisition / Materialization Audit Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase239 audits whether the Phase238 unseen-date validation requirement can be executed now.",
        "It does not validate the strategy, tune thresholds, print secrets, or unlock paper/live trading.",
        "",
    ]
    for title, table in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(table), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    phase238_dir: Path = DEFAULT_PHASE238_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    local_inventory, local_unseen_dates = build_local_inventory(phase238_dir, DEFAULT_RAW_ROOTS, DEFAULT_DERIVED_ROOT)
    azure_preflight = build_azure_preflight()
    target_dates = build_target_date_plan(local_unseen_dates)
    download_plan = build_download_plan(azure_preflight, target_dates)
    gates = build_gate_evaluation(local_inventory, azure_preflight, download_plan)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    hard_rows = int(len(hard))
    local_unseen_count = len(set(local_unseen_dates))
    az_ready = int(
        (
            azure_preflight.loc[
                azure_preflight["check_id"].astype(str).isin(
                    ["P239_AZ_LOGIN_STORAGE_LIST_READABLE", "P239_FILE_SERVICE_TARGET_UNSEEN_DATES_AVAILABLE"]
                ),
                "passed",
            ].astype(bool).any()
            if not azure_preflight.empty
            else False
        )
    )
    next_action = (
        "run_phase240_execute_unseen_real_l2_download_and_materialization_no_paper_live"
        if az_ready
        else "fix_azure_cli_tls_or_provide_fresh_sas_then_run_phase240_unseen_real_l2_download_no_paper_live"
    )
    acceptance = pd.DataFrame(
        [
            ("phase239_unseen_date_acquisition_audit_complete", 1, "Phase239 acquisition/materialization audit completed"),
            ("phase239_local_unseen_candidate_dates", local_unseen_count, "Local dates not in Phase237 discovery sample"),
            ("phase239_min_unseen_validation_dates_required", MIN_UNSEEN_VALIDATION_DATES, "Minimum unseen dates required by Phase238"),
            ("phase239_target_unseen_date_rows", int(len(target_dates)), "Target unseen date rows planned"),
            ("phase239_az_cli_available", int(azure_preflight.loc[azure_preflight["check_id"].astype(str).eq("P239_AZ_CLI_AVAILABLE"), "passed"].astype(bool).any()), "Azure CLI availability"),
            ("phase239_azcopy_available", int(azure_preflight.loc[azure_preflight["check_id"].astype(str).eq("P239_AZCOPY_AVAILABLE"), "passed"].astype(bool).any()), "AzCopy availability"),
            ("phase239_azure_storage_listing_ready", az_ready, "Whether Azure storage listing is readable now"),
            ("phase239_download_plan_rows", int(len(download_plan)), "Download/materialization plan rows"),
            ("phase239_hard_gate_pass_rows", hard_pass, "Hard Phase239 gates passed"),
            ("phase239_hard_gate_rows", hard_rows, "Hard Phase239 gates evaluated"),
            ("phase239_validation_execution_allowed_now", 0, "Phase239 does not execute validation"),
            ("phase239_strategy_promotion_allowed", 0, "No strategy promotion from Phase239"),
            ("phase239_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase239"),
            ("phase239_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase239"),
            ("phase239_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    local_inventory.to_csv(output_dir / "phase239_local_real_l2_inventory.csv", index=False)
    azure_preflight.to_csv(output_dir / "phase239_azure_access_preflight.csv", index=False)
    target_dates.to_csv(output_dir / "phase239_target_unseen_dates.csv", index=False)
    download_plan.to_csv(output_dir / "phase239_download_materialization_plan.csv", index=False)
    gates.to_csv(output_dir / "phase239_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase239_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase239_unseen_date_acquisition_report.md",
        {
            "Acceptance Summary": acceptance,
            "Local Real L2 Inventory": local_inventory,
            "Azure Access Preflight": azure_preflight,
            "Target Unseen Dates": target_dates,
            "Download and Materialization Plan": download_plan,
            "Gate Evaluation": gates,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase239_unseen_date_acquisition_materialization_audit",
        **reproducibility_fields(
            artifact_id="phase239",
            generated_utc=generated_utc,
            inputs={
                "phase238_dir": str(phase238_dir),
                "raw_roots": [str(p) for p in DEFAULT_RAW_ROOTS],
                "derived_root": str(DEFAULT_DERIVED_ROOT),
            },
            parameters={
                "target_unseen_dates": TARGET_UNSEEN_DATES,
                "min_unseen_validation_dates": MIN_UNSEEN_VALIDATION_DATES,
                "storage_account": STORAGE_ACCOUNT,
                "validation_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "local_inventory": str(output_dir / "phase239_local_real_l2_inventory.csv"),
                "azure_access_preflight": str(output_dir / "phase239_azure_access_preflight.csv"),
                "target_unseen_dates": str(output_dir / "phase239_target_unseen_dates.csv"),
                "download_materialization_plan": str(output_dir / "phase239_download_materialization_plan.csv"),
                "gate_evaluation": str(output_dir / "phase239_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase239_acceptance_summary.csv"),
                "report": str(output_dir / "phase239_unseen_date_acquisition_report.md"),
            },
            cost_model_version="not_applicable_no_strategy_replay",
            latency_model_version="not_applicable_no_strategy_replay",
        ),
    }
    (output_dir / "phase239_unseen_date_acquisition_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit unseen real-anchor date acquisition/materialization readiness.")
    parser.add_argument("--phase238-dir", type=Path, default=DEFAULT_PHASE238_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase238_dir=args.phase238_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
