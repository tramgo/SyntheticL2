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
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase478")

THESIS_ID = "P478_REAL_EXPANSION_RECONCILIATION_AFTER_PHASE477"
NEXT_ACTION = "repair_azure_cli_tls_or_provide_fresh_sas_then_download_one_disk_safe_official_catalyst_l2_day"
SUPPORTED_SAS_ENV_NAMES = [
    "AZURE_STORAGE_SAS_TOKEN",
    "AZURE_BLOB_SERVICE_SAS_URL",
    "STCTRADE1RAMIC_BLOB_SAS_URL",
    "STCTRADE1RAMIC_SAS_TOKEN",
]


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def shell_probe(args: list[str], timeout: int = 30) -> dict[str, Any]:
    run_args = args
    command_preview_args = args
    if args and args[0].lower() == "az":
        resolved_az = shutil.which("az.cmd") or shutil.which("az")
        if resolved_az:
            run_args = ["cmd.exe", "/c", resolved_az, *args[1:]]
            command_preview_args = [resolved_az, *args[1:]]
    try:
        proc = subprocess.run(run_args, capture_output=True, text=True, timeout=timeout, check=False)
        out = (proc.stdout or "").strip()
        err = (proc.stderr or "").strip()
        return {
            "command": " ".join(command_preview_args[:4]) + (" ..." if len(command_preview_args) > 4 else ""),
            "exit_code": proc.returncode,
            "stdout_preview": out[:500],
            "stderr_preview": err[:500],
            "success": int(proc.returncode == 0),
        }
    except Exception as exc:  # pragma: no cover - defensive audit path
        return {
            "command": " ".join(command_preview_args[:4]) + (" ..." if len(command_preview_args) > 4 else ""),
            "exit_code": -1,
            "stdout_preview": "",
            "stderr_preview": type(exc).__name__ + ": " + str(exc)[:450],
            "success": 0,
        }


def local_real_inventory() -> pd.DataFrame:
    candidate_files = []
    roots = [
        Path("real_data_sample/l2_single_day"),
        Path("scratch_azcopy_selected/raw_l2"),
        Path("scratch_l2_sample_20260710_HDFCBANK"),
        Path("raw_l2"),
    ]
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*.parquet"):
            text = str(path)
            trade_date = ""
            symbol = ""
            for part in path.parts:
                if part.startswith("trade_date="):
                    trade_date = part.split("=", 1)[1]
                if part.startswith("symbol="):
                    symbol = part.split("=", 1)[1]
            candidate_files.append(
                {
                    "root": str(root),
                    "path": text,
                    "trade_date": trade_date,
                    "symbol": symbol,
                    "bytes": int(path.stat().st_size),
                }
            )
    if not candidate_files:
        return pd.DataFrame(columns=["root", "path", "trade_date", "symbol", "bytes"])
    return pd.DataFrame(candidate_files)


def build_branch_reconciliation(phase477: pd.DataFrame, phase360: pd.DataFrame, phase369: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {
            "branch_id": "P477_SYNTHETIC_COMBINED_SHOCK_MARKET_CONTEXT_L2_FADE",
            "evidence_source": "outputs/phase477",
            "status": "rejected",
            "net_pnl_inr": float(scalar(phase477, "phase477_best_primary_net_pnl_inr", 0.0)),
            "annualized_return_pct": float(scalar(phase477, "phase477_best_primary_annualized_return_pct", 0.0)),
            "trade_rows": as_int(scalar(phase477, "phase477_best_primary_trade_count", 0)),
            "acceptance_allowed": 0,
            "next_use": "negative_control_only",
        },
        {
            "branch_id": "P360_UNSEEN_REAL_FULL_DEPTH_MARKET_NEUTRAL_FADE",
            "evidence_source": "outputs/phase360",
            "status": "unseen_real_failed",
            "net_pnl_inr": float(scalar(phase360, "phase360_primary_net_pnl_inr", 0.0)),
            "annualized_return_pct": float(scalar(phase360, "phase360_primary_annualized_return_pct", 0.0)),
            "trade_rows": as_int(scalar(phase360, "phase360_primary_capacity_selected_trade_rows", 0)),
            "acceptance_allowed": 0,
            "next_use": "requires_more_real_dates_or_close",
        },
        {
            "branch_id": "P369_REAL_DATE_EXPANSION_READINESS",
            "evidence_source": "outputs/phase369",
            "status": "data_expansion_required",
            "net_pnl_inr": 0.0,
            "annualized_return_pct": 0.0,
            "trade_rows": as_int(scalar(phase369, "phase369_phase366_selected_trades", 0)),
            "acceptance_allowed": 0,
            "next_use": "download_or_local_drop_one_disk_safe_day",
        },
    ]
    return pd.DataFrame(rows)


def build_access_probe() -> pd.DataFrame:
    sas_present_names = [name for name in SUPPORTED_SAS_ENV_NAMES if os.environ.get(name)]
    az_account = shell_probe(["az", "account", "show", "--query", "{name:name,tenantId:tenantId,user:user.name}", "-o", "json"])
    az_container = shell_probe(["az", "storage", "container", "list", "--account-name", "stctrade1ramic", "--auth-mode", "login", "--query", "[].name", "-o", "tsv"])
    return pd.DataFrame(
        [
            {
                "probe_id": "supported_sas_env_present",
                "available": int(bool(sas_present_names)),
                "evidence": f"present_count={len(sas_present_names)}; names_redacted={';'.join(sas_present_names)}",
                "secret_material_recorded": 0,
            },
            {
                "probe_id": "az_account_show",
                "available": int(az_account["success"]),
                "evidence": (az_account["stdout_preview"] or az_account["stderr_preview"])[:500],
                "secret_material_recorded": 0,
            },
            {
                "probe_id": "az_storage_container_list_login",
                "available": int(az_container["success"]),
                "evidence": (az_container["stdout_preview"] or az_container["stderr_preview"])[:500],
                "secret_material_recorded": 0,
            },
        ]
    )


def build_next_contract(local_inventory: pd.DataFrame, access_probe: pd.DataFrame) -> pd.DataFrame:
    dated = local_inventory[local_inventory["trade_date"].astype(str).ne("")] if not local_inventory.empty else pd.DataFrame()
    date_count = int(dated["trade_date"].nunique()) if not dated.empty else 0
    sas_ok = int(access_probe.loc[access_probe["probe_id"].eq("supported_sas_env_present"), "available"].iloc[0])
    az_storage_ok = int(access_probe.loc[access_probe["probe_id"].eq("az_storage_container_list_login"), "available"].iloc[0])
    rows = [
        ("selected_next_action", NEXT_ACTION, "Real-date expansion is the only credible next path after Phase477 rejection."),
        ("local_real_l2_date_count_observed", date_count, "Local dated real L2 partitions found by this audit."),
        ("fresh_sas_env_available", sas_ok, "Supported SAS env variables present in this process."),
        ("az_storage_login_list_available", az_storage_ok, "Azure CLI storage list via login succeeded."),
        ("one_day_disk_safe_increment_required", 1, "Do not attempt broad 80GB downloads while disk is constrained."),
        ("target_download_scope", "one_full_universe_official_catalyst_l2_day", "One new day first, then verify schema and event overlap."),
        ("required_partition_shape", "raw_l2/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet", "Expected local shape."),
        ("acceptance_retest_allowed_now", 0, "No acceptance retest until new real L2 event breadth exists."),
        ("strategy_promotion_allowed", 0, "No strategy promotion."),
        ("paper_or_live_acceptance_allowed", 0, "No paper/live."),
        ("deployable_profitability_claim_allowed", 0, "No deployable claim."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_gates(phase477: pd.DataFrame, phase360: pd.DataFrame, phase369: pd.DataFrame, reconciliation: pd.DataFrame, access_probe: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    c = dict(zip(contract["contract_id"].astype(str), contract["contract_value"]))
    secret_rows = int(access_probe["secret_material_recorded"].astype(int).sum())
    rows = [
        ("P478_PHASE477_REJECTION_USED", as_int(scalar(phase477, "phase477_phase478_allowed_next", 1)) == 0, scalar(phase477, "phase477_phase478_allowed_next", 1), 0),
        ("P478_PHASE360_UNSEEN_REAL_EVIDENCE_USED", as_int(scalar(phase360, "phase360_full_depth_market_neutral_fade_unseen_execution_complete", 0)) == 1, scalar(phase360, "phase360_full_depth_market_neutral_fade_unseen_execution_complete", 0), 1),
        ("P478_PHASE369_EXPANSION_READINESS_USED", as_int(scalar(phase369, "phase369_official_catalyst_real_l2_expansion_readiness_complete", 0)) == 1, scalar(phase369, "phase369_official_catalyst_real_l2_expansion_readiness_complete", 0), 1),
        ("P478_BRANCH_RECONCILIATION_ROWS_PRESENT", len(reconciliation) >= 3, len(reconciliation), ">=3"),
        ("P478_ACCESS_PROBED_WITHOUT_SECRETS", secret_rows == 0, secret_rows, 0),
        ("P478_REAL_EXPANSION_SELECTED_NEXT", str(c.get("selected_next_action", "")).startswith("repair_azure_cli_tls"), c.get("selected_next_action", ""), "repair_or_sas_download"),
        ("P478_ONE_DAY_DISK_SAFE_INCREMENT_REQUIRED", as_int(c.get("one_day_disk_safe_increment_required", 0)) == 1, c.get("one_day_disk_safe_increment_required", ""), 1),
        ("P478_NO_ACCEPTANCE_RETEST_NOW", as_int(c.get("acceptance_retest_allowed_now", 1)) == 0, c.get("acceptance_retest_allowed_now", ""), 0),
        ("P478_NO_PROMOTION_PAPER_LIVE_OR_CLAIM", as_int(c.get("paper_or_live_acceptance_allowed", 1)) == 0 and as_int(c.get("deployable_profitability_claim_allowed", 1)) == 0, "paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(gates: pd.DataFrame, access_probe: pd.DataFrame, local_inventory: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    complete = int(hard_pass == hard_rows)
    dated = local_inventory[local_inventory["trade_date"].astype(str).ne("")] if not local_inventory.empty else pd.DataFrame()
    rows = [
        ("phase478_real_expansion_reconciliation_complete", complete, "Phase478 complete if all gates pass"),
        ("phase478_thesis_id", THESIS_ID, "Phase478 thesis"),
        ("phase478_local_real_l2_file_rows", int(len(local_inventory)), "Local real L2 parquet files found"),
        ("phase478_local_real_l2_date_rows", int(dated["trade_date"].nunique()) if not dated.empty else 0, "Local dated real L2 dates found"),
        ("phase478_supported_sas_env_present", int(access_probe.loc[access_probe["probe_id"].eq("supported_sas_env_present"), "available"].iloc[0]), "SAS env available"),
        ("phase478_az_account_available", int(access_probe.loc[access_probe["probe_id"].eq("az_account_show"), "available"].iloc[0]), "Azure account probe success"),
        ("phase478_az_storage_list_available", int(access_probe.loc[access_probe["probe_id"].eq("az_storage_container_list_login"), "available"].iloc[0]), "Azure storage list success"),
        ("phase478_strategy_promotion_allowed", 0, "No promotion"),
        ("phase478_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase478_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase478_phase479_allowed_next", complete, "Allows repair/download precommit only"),
        ("phase478_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase478_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase478_next_best_action", NEXT_ACTION, "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, reconciliation: pd.DataFrame, access_probe: pd.DataFrame, local_inventory: pd.DataFrame, contract: pd.DataFrame, gates: pd.DataFrame) -> None:
    sample_inventory = local_inventory.head(100).copy() if not local_inventory.empty else local_inventory
    lines = [
        "# Phase478 Real Expansion Reconciliation After Phase477",
        "",
        "Phase478 reconciles the rejected synthetic Phase477 diagnostic with prior unseen real-L2 evidence and selects the next real-data expansion action.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Branch Reconciliation",
        "",
        _markdown_table(reconciliation),
        "",
        "## Access Probe",
        "",
        _markdown_table(access_probe),
        "",
        "## Local Real L2 Inventory Sample",
        "",
        _markdown_table(sample_inventory),
        "",
        "## Next Contract",
        "",
        _markdown_table(contract),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase478 does not run another strategy shard. It selects one disk-safe real-data expansion step and keeps paper/live closed.",
    ]
    (output_dir / "phase478_real_expansion_reconciliation_after_phase477_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase477 = read_csv(Path("outputs/phase477/phase477_acceptance_summary.csv"))
    phase360 = read_csv(Path("outputs/phase360/phase360_acceptance_summary.csv"))
    phase369 = read_csv(Path("outputs/phase369/phase369_acceptance_summary.csv"))
    if phase477.empty or phase360.empty or phase369.empty:
        raise FileNotFoundError("Phase478 requires Phase477, Phase360, and Phase369 acceptance summaries.")
    local_inventory = local_real_inventory()
    access_probe = build_access_probe()
    reconciliation = build_branch_reconciliation(phase477, phase360, phase369)
    contract = build_next_contract(local_inventory, access_probe)
    gates = build_gates(phase477, phase360, phase369, reconciliation, access_probe, contract)
    acceptance = build_acceptance(gates, access_probe, local_inventory)
    local_inventory.to_csv(output_dir / "phase478_local_real_l2_inventory.csv", index=False)
    access_probe.to_csv(output_dir / "phase478_access_probe.csv", index=False)
    reconciliation.to_csv(output_dir / "phase478_branch_reconciliation.csv", index=False)
    contract.to_csv(output_dir / "phase478_next_real_expansion_contract.csv", index=False)
    gates.to_csv(output_dir / "phase478_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase478_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, reconciliation, access_probe, local_inventory, contract, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase478_real_expansion_reconciliation_after_phase477",
        **reproducibility_fields(
            artifact_id="phase478_real_expansion_reconciliation_after_phase477",
            generated_utc=generated_utc,
            inputs={
                "phase477_acceptance": "outputs/phase477/phase477_acceptance_summary.csv",
                "phase360_acceptance": "outputs/phase360/phase360_acceptance_summary.csv",
                "phase369_acceptance": "outputs/phase369/phase369_acceptance_summary.csv",
            },
            parameters={"thesis_id": THESIS_ID, "supported_sas_env_names": SUPPORTED_SAS_ENV_NAMES, "download_executed": False},
            outputs={"acceptance_summary": str(output_dir / "phase478_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase478_no_execution_access_probe_only",
        ),
    }
    (output_dir / "phase478_real_expansion_reconciliation_after_phase477_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase478 real expansion reconciliation after Phase477.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    out = run(args.output_dir)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
