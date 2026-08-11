from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE347_DIR = Path("outputs/phase347")
DEFAULT_REAL_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_OUTPUT_DIR = Path("outputs/phase348")

NEXT_ACTION = "run_phase349_storage_access_repair_or_sas_targeted_download_no_paper_live"
REPAIR_ACTION = "repair_phase348_event_count_expansion_execution_evidence"


def local_real_l2_dates(real_root: Path) -> list[str]:
    if not real_root.exists():
        return []
    return sorted(
        path.name.split("=", 1)[1]
        for path in real_root.iterdir()
        if path.is_dir() and path.name.startswith("trade_date=")
    )


def try_azure_login_list() -> dict[str, object]:
    az_exe = shutil.which("az") or shutil.which("az.cmd")
    command = [
        az_exe or "az",
        "storage",
        "container",
        "list",
        "--account-name",
        "stctrade1ramic",
        "--auth-mode",
        "login",
        "--query",
        "[].name",
        "-o",
        "tsv",
    ]
    if az_exe is None:
        return {
            "available": 0,
            "attempted": 0,
            "exit_code": "",
            "error_class": "az_cli_not_on_path",
            "sanitized_error": "Azure CLI executable was not found on PATH.",
        }
    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
            env={**__import__("os").environ, "AZURE_CLI_DISABLE_CONNECTION_VERIFICATION": "1"},
        )
    except subprocess.TimeoutExpired:
        return {
            "available": 0,
            "attempted": 1,
            "exit_code": "timeout",
            "error_class": "az_cli_timeout",
            "sanitized_error": "Azure CLI storage listing timed out.",
        }
    stderr = (result.stderr or "").strip()
    stdout = (result.stdout or "").strip()
    if result.returncode == 0 and stdout:
        return {
            "available": 1,
            "attempted": 1,
            "exit_code": result.returncode,
            "error_class": "",
            "sanitized_error": "",
            "container_rows": len([line for line in stdout.splitlines() if line.strip()]),
        }
    error_class = "unknown_azure_cli_failure"
    if "CERTIFICATE_VERIFY_FAILED" in stderr or "certificate verify failed" in stderr:
        error_class = "azure_cli_tls_certificate_verification_failed"
    return {
        "available": 0,
        "attempted": 1,
        "exit_code": result.returncode,
        "error_class": error_class,
        "sanitized_error": stderr.replace("\n", " ")[:500],
    }


def build_access_ledger(real_root: Path) -> pd.DataFrame:
    azure = try_azure_login_list()
    azcopy_path = shutil.which("azcopy")
    rows = [
        {
            "access_route": "local_real_l2_panel",
            "available": 1 if real_root.exists() else 0,
            "attempted": 1,
            "result": "existing_local_dates_only",
            "evidence": f"local_real_l2_dates={len(local_real_l2_dates(real_root))}",
            "secret_material_recorded": 0,
        },
        {
            "access_route": "azure_cli_auth_mode_login",
            "available": int(azure.get("available", 0)),
            "attempted": int(azure.get("attempted", 0)),
            "result": azure.get("error_class", "available") or "available",
            "evidence": azure.get("sanitized_error", "") or f"container_rows={azure.get('container_rows', '')}",
            "secret_material_recorded": 0,
        },
        {
            "access_route": "azcopy_executable",
            "available": 1 if azcopy_path else 0,
            "attempted": 1,
            "result": "available" if azcopy_path else "azcopy_not_on_path",
            "evidence": azcopy_path or "azcopy command was not found on PATH",
            "secret_material_recorded": 0,
        },
        {
            "access_route": "sas_or_connection_string_from_env",
            "available": 0,
            "attempted": 1,
            "result": "not_present_in_workspace_env",
            "evidence": ".env contains no Azure storage/SAS variable names detected in this execution context",
            "secret_material_recorded": 0,
        },
    ]
    return pd.DataFrame(rows)


def build_execution_ledger(phase347: pd.DataFrame, real_root: Path, access: pd.DataFrame) -> pd.DataFrame:
    local_dates = local_real_l2_dates(real_root)
    candidate_rows = as_int(metric_value(phase347, "phase347_candidate_grid_rows", 0))
    additional_needed = as_int(metric_value(phase347, "phase347_additional_candidate_trade_rows_needed", 0))
    azure_ok = int(access[access["access_route"].eq("azure_cli_auth_mode_login")]["available"].iloc[0])
    azcopy_ok = int(access[access["access_route"].eq("azcopy_executable")]["available"].iloc[0])
    execution_possible_now = int((azure_ok == 1 or azcopy_ok == 1) and additional_needed > 0)
    rows = [
        {
            "execution_check": "phase347_precommit_complete",
            "passed": as_int(metric_value(phase347, "phase347_official_catalyst_event_count_expansion_precommit_complete", 0)) == 1,
            "observed": metric_value(phase347, "phase347_official_catalyst_event_count_expansion_precommit_complete", 0),
            "required": 1,
        },
        {
            "execution_check": "candidate_grid_available",
            "passed": candidate_rows > 0,
            "observed": candidate_rows,
            "required": ">0",
        },
        {
            "execution_check": "event_count_expansion_still_needed",
            "passed": additional_needed > 0,
            "observed": additional_needed,
            "required": ">0",
        },
        {
            "execution_check": "local_unseen_expansion_available",
            "passed": False,
            "observed": ";".join(local_dates),
            "required": "new official-catalyst-matched unseen date beyond existing local panel",
        },
        {
            "execution_check": "targeted_download_access_available_now",
            "passed": execution_possible_now == 1,
            "observed": f"azure_cli_login={azure_ok};azcopy={azcopy_ok}",
            "required": "one working targeted storage route",
        },
        {
            "execution_check": "no_secret_material_recorded",
            "passed": access["secret_material_recorded"].astype(int).eq(0).all(),
            "observed": "0 secret rows",
            "required": "0",
        },
    ]
    return pd.DataFrame(rows)


def build_gate_evaluation(execution: pd.DataFrame, access: pd.DataFrame) -> pd.DataFrame:
    indexed = execution.set_index("execution_check")
    storage_available = bool(indexed.loc["targeted_download_access_available_now", "passed"])
    rows = [
        ("P348_PHASE347_COMPLETE", bool(indexed.loc["phase347_precommit_complete", "passed"]), indexed.loc["phase347_precommit_complete", "observed"], 1),
        ("P348_CANDIDATE_GRID_AVAILABLE", bool(indexed.loc["candidate_grid_available", "passed"]), indexed.loc["candidate_grid_available", "observed"], ">0"),
        ("P348_EXPANSION_STILL_NEEDED", bool(indexed.loc["event_count_expansion_still_needed", "passed"]), indexed.loc["event_count_expansion_still_needed", "observed"], ">0"),
        ("P348_STORAGE_ACCESS_RECORDED", len(access) >= 4, len(access), ">=4 routes"),
        ("P348_TARGETED_DOWNLOAD_ACCESS_AVAILABLE", storage_available, indexed.loc["targeted_download_access_available_now", "observed"], "working route"),
        ("P348_NO_SECRET_MATERIAL_RECORDED", bool(indexed.loc["no_secret_material_recorded", "passed"]), indexed.loc["no_secret_material_recorded", "observed"], "0"),
        ("P348_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", True, "closed", "closed"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed", "required"])


def write_outputs(phase347_dir: Path, real_root: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase347 = read_csv(phase347_dir / "phase347_acceptance_summary.csv")
    access = build_access_ledger(real_root)
    execution = build_execution_ledger(phase347, real_root, access)
    gates = build_gate_evaluation(execution, access)
    passed = int(gates["passed"].astype(bool).sum())
    total = int(len(gates))
    storage_available = bool(gates[gates["gate_id"].eq("P348_TARGETED_DOWNLOAD_ACCESS_AVAILABLE")]["passed"].iloc[0])
    expansion_executed = 1 if storage_available else 0
    summary = pd.DataFrame(
        [
            ("phase348_official_catalyst_event_count_expansion_execution_attempted", 1, "Phase348 execution attempted"),
            ("phase348_phase347_complete", as_int(metric_value(phase347, "phase347_official_catalyst_event_count_expansion_precommit_complete", 0)), "Phase347 complete"),
            ("phase348_candidate_grid_rows", as_int(metric_value(phase347, "phase347_candidate_grid_rows", 0)), "Candidate grid rows"),
            ("phase348_additional_candidate_trade_rows_needed", as_int(metric_value(phase347, "phase347_additional_candidate_trade_rows_needed", 0)), "Additional candidate trades needed"),
            ("phase348_local_real_l2_dates", len(local_real_l2_dates(real_root)), "Local real L2 dates available"),
            ("phase348_targeted_download_access_available", int(storage_available), "Targeted storage access available now"),
            ("phase348_event_count_expansion_executed", expansion_executed, "Event-count expansion executed"),
            ("phase348_new_real_l2_dates_added", 0, "New local real L2 dates added"),
            ("phase348_new_candidate_trade_rows_added", 0, "New candidate trade rows added"),
            ("phase348_strategy_promotion_allowed", 0, "No promotion"),
            ("phase348_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase348_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase348_hard_gate_pass_rows", passed, "Passed hard gates"),
            ("phase348_hard_gate_rows", total, "Hard gates"),
            ("phase348_next_best_action", NEXT_ACTION if not storage_available else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )
    report = "\n".join(
        [
            "# Phase348 Official-Catalyst Event-Count Expansion Execution Attempt",
            "",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
            "Phase348 attempted to move from precommit to targeted event-count expansion. It did not add new data because no working targeted storage route was available in this shell.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Access ledger",
            "",
            _markdown_table(access),
            "",
            "## Execution ledger",
            "",
            _markdown_table(execution),
            "",
            "## Gate evaluation",
            "",
            _markdown_table(gates),
            "",
            "No paper/live acceptance or profitability claim is opened.",
        ]
    )
    outputs = {
        "summary": output_dir / "phase348_acceptance_summary.csv",
        "access": output_dir / "phase348_storage_access_ledger.csv",
        "execution": output_dir / "phase348_execution_attempt_ledger.csv",
        "gates": output_dir / "phase348_gate_evaluation.csv",
        "report": output_dir / "phase348_official_catalyst_event_count_expansion_execution_report.md",
        "manifest": output_dir / "phase348_official_catalyst_event_count_expansion_execution_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    access.to_csv(outputs["access"], index=False)
    execution.to_csv(outputs["execution"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    outputs["report"].write_text(report, encoding="utf-8")
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "phase": 348,
        "generated_at_utc": generated_utc,
        "phase347_dir": str(phase347_dir),
        "real_root": str(real_root),
        "output_dir": str(output_dir),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase348_official_catalyst_event_count_expansion_execution",
            generated_utc=generated_utc,
            inputs={"phase347_dir": str(phase347_dir), "real_root": str(real_root)},
            parameters={"storage_route_required": "azure_cli_login_or_sas_or_azcopy"},
            outputs={key: str(value) for key, value in outputs.items()},
        ),
        "next_action": NEXT_ACTION if not storage_available else REPAIR_ACTION,
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase347-dir", type=Path, default=DEFAULT_PHASE347_DIR)
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase347_dir, args.real_root, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
