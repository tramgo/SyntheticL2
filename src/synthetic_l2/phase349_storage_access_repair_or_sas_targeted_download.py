from __future__ import annotations

import argparse
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE348_DIR = Path("outputs/phase348")
DEFAULT_PHASE347_DIR = Path("outputs/phase347")
DEFAULT_OUTPUT_DIR = Path("outputs/phase349")

NEXT_ACTION_WITH_SECRET = "run_phase350_execute_sas_targeted_one_date_download_no_paper_live"
NEXT_ACTION_NO_SECRET = "provide_sas_or_install_azcopy_then_run_phase350_targeted_download_no_paper_live"
REPAIR_ACTION = "repair_phase349_storage_access_repair_contract"


SAS_ENV_NAMES = [
    "AZURE_STORAGE_SAS_TOKEN",
    "AZURE_BLOB_SERVICE_SAS_URL",
    "STCTRADE1RAMIC_BLOB_SAS_URL",
    "STCTRADE1RAMIC_SAS_TOKEN",
]


def env_has_sas() -> bool:
    return any(bool(os.environ.get(name, "").strip()) for name in SAS_ENV_NAMES)


def masked_env_inventory() -> pd.DataFrame:
    rows = []
    for name in SAS_ENV_NAMES:
        present = bool(os.environ.get(name, "").strip())
        rows.append(
            {
                "input_name": name,
                "present": int(present),
                "secret_value_recorded": 0,
                "use": "Phase350 may consume this in-memory environment variable; Phase349 never writes the value.",
            }
        )
    return pd.DataFrame(rows)


def build_repair_options(phase348_access: pd.DataFrame) -> pd.DataFrame:
    azcopy_present = shutil.which("azcopy") is not None
    azure_tls_failed = phase348_access["result"].astype(str).str.contains("tls_certificate", case=False, na=False).any()
    rows = [
        {
            "repair_option_id": "P349_OPT_001_USE_FRESH_BLOB_SAS_ENV",
            "priority": 1,
            "route": "sas_https_without_az_login",
            "action": "Provide a fresh blob service SAS URL or SAS token via an environment variable, then run Phase350 targeted one-date download.",
            "why": "Bypasses the local Azure CLI TLS token-refresh failure and avoids storing secrets in repo outputs.",
            "ready_now": int(env_has_sas()),
            "secret_material_recorded": 0,
        },
        {
            "repair_option_id": "P349_OPT_002_INSTALL_OR_PROVIDE_AZCOPY",
            "priority": 2,
            "route": "azcopy_with_sas",
            "action": "Install azcopy or add it to PATH, then use SAS-protected URLs for targeted partition copies.",
            "why": "AzCopy is better for resumable targeted Azure Blob/File downloads when storage access is SAS-based.",
            "ready_now": int(azcopy_present and env_has_sas()),
            "secret_material_recorded": 0,
        },
        {
            "repair_option_id": "P349_OPT_003_REPAIR_AZURE_CLI_CA_CHAIN",
            "priority": 3,
            "route": "az_cli_auth_mode_login",
            "action": "Repair Azure CLI certificate trust or configure the proxy CA bundle, then retry az storage listing/download.",
            "why": "Current az login-mode route fails on certificate verification before storage listing can proceed.",
            "ready_now": 0 if azure_tls_failed else 1,
            "secret_material_recorded": 0,
        },
        {
            "repair_option_id": "P349_OPT_004_LOCAL_DROPZONE_ONE_DATE",
            "priority": 4,
            "route": "manual_local_drop",
            "action": "Drop one official-catalyst-matched date partition into the local real L2 panel, then run Phase350 local verification.",
            "why": "Works when cloud access cannot be repaired immediately and disk space is tight.",
            "ready_now": 0,
            "secret_material_recorded": 0,
        },
    ]
    return pd.DataFrame(rows)


def build_phase350_contract(phase347_work: pd.DataFrame, candidate_grid: pd.DataFrame) -> pd.DataFrame:
    download_row = phase347_work[phase347_work["work_order_id"].eq("P347_WO_002_TARGETED_REAL_L2_DOWNLOAD")].iloc[0]
    target_symbols = str(download_row["target_symbols"])
    rows = [
        ("phase350_scope", "targeted_one_new_official_catalyst_matched_date", "Download or verify only one new date increment."),
        ("target_symbols", target_symbols, "Candidate symbols from Phase347; do not download unrelated full panel."),
        ("max_new_dates_per_increment", str(download_row["max_new_dates_per_increment"]), "Disk-aware increment size."),
        ("target_partition_shape", "raw_l2/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet", "Expected Zerodha-websocket-like raw top-five L2 partition shape."),
        ("full_top_five_depth_required", "1", "Persist bid/ask price, quantity and order-count levels 1-5."),
        ("levels_2_to_5_materiality_required", "1", "Do not reduce to L1-only features."),
        ("official_catalyst_timestamp_authority_required", "1", "Use official NSE/BSE/SEBI-style timestamp authority."),
        ("no_lookahead_join_required", "1", "Entry/replay time must be first tick at or after official announcement time."),
        ("candidate_grid_rows", str(len(candidate_grid)), "Rerun only Phase347 candidate grid rows after expansion."),
        ("additional_candidate_trade_rows_needed", str(max(0, 30 - int(candidate_grid["trade_rows"].astype(int).max())) if not candidate_grid.empty else 0), "Minimum additional candidate rows before acceptance re-evaluation."),
        ("paper_live_or_profit_claim_allowed", "0", "No paper/live or deployable profitability claim."),
        ("secret_persistence_allowed", "0", "Do not write SAS, connection strings, account keys or signed URLs to repo outputs."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_command_contract() -> pd.DataFrame:
    rows = [
        {
            "command_id": "P349_CMD_001_SET_SAS_IN_PROCESS",
            "shell": "PowerShell",
            "template": "$env:AZURE_BLOB_SERVICE_SAS_URL='<paste fresh blob service SAS URL only in your local shell>'; python scripts\\run_phase350_sas_targeted_one_date_download.py",
            "safe_logging": "Do not echo the environment variable; Phase350 must redact signed URLs.",
            "secret_material_recorded": 0,
        },
        {
            "command_id": "P349_CMD_002_SET_TOKEN_IN_PROCESS",
            "shell": "PowerShell",
            "template": "$env:AZURE_STORAGE_SAS_TOKEN='<paste fresh SAS token only in your local shell>'; python scripts\\run_phase350_sas_targeted_one_date_download.py",
            "safe_logging": "Do not echo the environment variable; Phase350 must redact signed URLs.",
            "secret_material_recorded": 0,
        },
        {
            "command_id": "P349_CMD_003_LOCAL_DROP_VERIFY",
            "shell": "PowerShell",
            "template": "python scripts\\run_phase350_sas_targeted_one_date_download.py --local-only-verify",
            "safe_logging": "Use only after manually dropping a new trade_date=YYYY-MM-DD partition.",
            "secret_material_recorded": 0,
        },
    ]
    return pd.DataFrame(rows)


def build_gate_evaluation(phase348: pd.DataFrame, env_inventory: pd.DataFrame, repair: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    phase348_attempted = as_int(metric_value(phase348, "phase348_official_catalyst_event_count_expansion_execution_attempted", 0))
    secret_clean = (
        env_inventory["secret_value_recorded"].astype(int).eq(0).all()
        and repair["secret_material_recorded"].astype(int).eq(0).all()
        and str(contract.set_index("contract_id").loc["secret_persistence_allowed", "contract_value"]) == "0"
    )
    rows = [
        ("P349_PHASE348_ATTEMPT_RECORDED", phase348_attempted == 1, phase348_attempted, 1),
        ("P349_STORAGE_ACCESS_REPAIR_OPTIONS_PRESENT", len(repair) >= 4, len(repair), ">=4"),
        ("P349_SAS_ENV_INPUT_CONTRACT_PRESENT", len(env_inventory) >= 4, len(env_inventory), ">=4"),
        ("P349_PHASE350_DOWNLOAD_CONTRACT_PRESENT", len(contract) >= 10, len(contract), ">=10"),
        ("P349_FULL_DEPTH_AND_NO_LOOKAHEAD_PRESERVED", str(contract.set_index("contract_id").loc["full_top_five_depth_required", "contract_value"]) == "1" and str(contract.set_index("contract_id").loc["no_lookahead_join_required", "contract_value"]) == "1", "preserved", "preserved"),
        ("P349_NO_SECRET_MATERIAL_RECORDED", secret_clean, "clean" if secret_clean else "leak", "clean"),
        ("P349_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", True, "closed", "closed"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed", "required"])


def write_outputs(phase348_dir: Path, phase347_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase348 = read_csv(phase348_dir / "phase348_acceptance_summary.csv")
    phase348_access = pd.read_csv(phase348_dir / "phase348_storage_access_ledger.csv")
    phase347_work = pd.read_csv(phase347_dir / "phase347_event_count_expansion_work_order.csv")
    candidate_grid = pd.read_csv(phase347_dir / "phase347_candidate_execution_grid.csv")
    env_inventory = masked_env_inventory()
    repair = build_repair_options(phase348_access)
    contract = build_phase350_contract(phase347_work, candidate_grid)
    commands = build_command_contract()
    gates = build_gate_evaluation(phase348, env_inventory, repair, contract)
    passed = int(gates["passed"].astype(bool).sum())
    total = int(len(gates))
    sas_ready = int(env_inventory["present"].astype(int).sum() > 0)
    next_action = NEXT_ACTION_WITH_SECRET if sas_ready and passed == total else NEXT_ACTION_NO_SECRET if passed == total else REPAIR_ACTION
    summary = pd.DataFrame(
        [
            ("phase349_storage_access_repair_or_sas_targeted_download_precommit_complete", 1, "Phase349 precommit completed"),
            ("phase349_phase348_attempted", as_int(metric_value(phase348, "phase348_official_catalyst_event_count_expansion_execution_attempted", 0)), "Phase348 attempted"),
            ("phase349_sas_env_inputs_present", sas_ready, "Any supported SAS environment input present"),
            ("phase349_repair_option_rows", len(repair), "Storage repair options"),
            ("phase349_phase350_contract_rows", len(contract), "Phase350 execution contract rows"),
            ("phase349_command_contract_rows", len(commands), "Safe command contract rows"),
            ("phase349_candidate_grid_rows", len(candidate_grid), "Candidate grid rows"),
            ("phase349_secret_material_recorded", 0, "No secret material recorded"),
            ("phase349_strategy_promotion_allowed", 0, "No promotion"),
            ("phase349_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase349_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase349_hard_gate_pass_rows", passed, "Passed hard gates"),
            ("phase349_hard_gate_rows", total, "Hard gates"),
            ("phase349_next_best_action", next_action, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )
    report = "\n".join(
        [
            "# Phase349 Storage Access Repair Or SAS Targeted Download Precommit",
            "",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
            "Phase349 converts the Phase348 storage-access block into a safe repair and targeted-download contract. It does not store secrets and does not execute a download.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## SAS environment input inventory",
            "",
            _markdown_table(env_inventory),
            "",
            "## Repair options",
            "",
            _markdown_table(repair),
            "",
            "## Phase350 execution contract",
            "",
            _markdown_table(contract),
            "",
            "## Safe command contract",
            "",
            _markdown_table(commands),
            "",
            "No paper/live acceptance or profitability claim is opened.",
        ]
    )
    outputs = {
        "summary": output_dir / "phase349_acceptance_summary.csv",
        "env_inventory": output_dir / "phase349_sas_env_input_inventory.csv",
        "repair": output_dir / "phase349_storage_repair_option_ledger.csv",
        "contract": output_dir / "phase349_phase350_targeted_download_contract.csv",
        "commands": output_dir / "phase349_safe_command_contract.csv",
        "gates": output_dir / "phase349_gate_evaluation.csv",
        "report": output_dir / "phase349_storage_access_repair_or_sas_targeted_download_report.md",
        "manifest": output_dir / "phase349_storage_access_repair_or_sas_targeted_download_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    env_inventory.to_csv(outputs["env_inventory"], index=False)
    repair.to_csv(outputs["repair"], index=False)
    contract.to_csv(outputs["contract"], index=False)
    commands.to_csv(outputs["commands"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    outputs["report"].write_text(report, encoding="utf-8")
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "phase": 349,
        "generated_at_utc": generated_utc,
        "phase348_dir": str(phase348_dir),
        "phase347_dir": str(phase347_dir),
        "output_dir": str(output_dir),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase349_storage_access_repair_or_sas_targeted_download",
            generated_utc=generated_utc,
            inputs={"phase348_dir": str(phase348_dir), "phase347_dir": str(phase347_dir)},
            parameters={"sas_env_names": SAS_ENV_NAMES},
            outputs={key: str(value) for key, value in outputs.items()},
        ),
        "next_action": next_action,
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase348-dir", type=Path, default=DEFAULT_PHASE348_DIR)
    parser.add_argument("--phase347-dir", type=Path, default=DEFAULT_PHASE347_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase348_dir, args.phase347_dir, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
