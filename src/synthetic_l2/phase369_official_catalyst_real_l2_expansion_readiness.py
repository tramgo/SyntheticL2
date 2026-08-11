from __future__ import annotations

import argparse
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase369")
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


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def unique_nonempty(series: pd.Series) -> list[str]:
    if series.empty:
        return []
    return sorted({str(value) for value in series.dropna().tolist() if str(value).strip()})


def write_outputs(output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()

    phase341_summary = read_csv(Path("outputs/phase341/phase341_acceptance_summary.csv"))
    phase341_work = read_csv(Path("outputs/phase341/phase341_phase342_execution_work_order.csv"))
    phase359_summary = read_csv(Path("outputs/phase359/phase359_acceptance_summary.csv"))
    phase359_inventory = read_csv(Path("outputs/phase359/phase359_local_unseen_real_l2_inventory.csv"))
    phase359_elig = read_csv(Path("outputs/phase359/phase359_no_lookahead_official_catalyst_eligibility.csv"))
    phase350_summary = read_csv(Path("outputs/phase350/phase350_acceptance_summary.csv"))
    phase350_access = read_csv(Path("outputs/phase350/phase350_access_ledger.csv"))
    phase366_summary = read_csv(Path("outputs/phase366/phase366_acceptance_summary.csv"))
    phase368_summary = read_csv(Path("outputs/phase368/phase368_acceptance_summary.csv"))

    required_inputs = {
        "phase341_summary": phase341_summary,
        "phase341_work_order": phase341_work,
        "phase359_summary": phase359_summary,
        "phase359_inventory": phase359_inventory,
        "phase359_eligibility": phase359_elig,
        "phase350_summary": phase350_summary,
        "phase350_access": phase350_access,
        "phase366_summary": phase366_summary,
        "phase368_summary": phase368_summary,
    }
    missing = [name for name, frame in required_inputs.items() if frame.empty]
    if missing:
        raise FileNotFoundError("Phase369 requires non-empty artifacts: " + "; ".join(missing))

    phase341_events = as_int(metric_value(phase341_summary, "phase341_no_lookahead_eligible_event_rows"))
    phase341_symbol_dates = as_int(metric_value(phase341_summary, "phase341_no_lookahead_eligible_symbol_dates"))
    phase359_events = as_int(metric_value(phase359_summary, "phase359_no_lookahead_eligible_event_rows"))
    phase359_symbol_dates = as_int(metric_value(phase359_summary, "phase359_no_lookahead_eligible_symbol_dates"))
    phase359_unseen_dates = unique_nonempty(phase359_inventory["trade_date"]) if "trade_date" in phase359_inventory.columns else []
    phase359_symbols = as_int(metric_value(phase359_summary, "phase359_unseen_symbols"))
    phase359_bytes = int(pd.to_numeric(phase359_inventory.get("bytes", pd.Series(dtype=float)), errors="coerce").fillna(0).sum())
    phase359_days = len(phase359_unseen_dates)
    bytes_per_full_universe_day = int(phase359_bytes / phase359_days) if phase359_days else 0

    current_work_rows = phase341_events + phase359_events
    phase366_trades = as_int(metric_value(phase366_summary, "phase366_primary_trade_rows"))
    phase366_event_floor_met = as_int(metric_value(phase366_summary, "phase366_primary_event_floor_met"))
    phase366_acceptance = as_int(metric_value(phase366_summary, "phase366_acceptance_candidate_rows"))
    phase366_ann = as_float(metric_value(phase366_summary, "phase366_primary_annualized_return_pct"))
    additional_selected_trades_needed = max(0, 30 - phase366_trades)
    selected_trade_yield = phase366_trades / current_work_rows if current_work_rows else 0.0
    eligible_events_needed_at_current_yield = math.ceil(additional_selected_trades_needed / selected_trade_yield) if selected_trade_yield > 0 else 0
    eligible_events_per_unseen_day = phase359_events / phase359_days if phase359_days else 0.0
    estimated_full_universe_days_needed = math.ceil(eligible_events_needed_at_current_yield / eligible_events_per_unseen_day) if eligible_events_per_unseen_day > 0 else 0
    estimated_bytes_needed = estimated_full_universe_days_needed * bytes_per_full_universe_day

    sas_env_present_names = [name for name in SUPPORTED_SAS_ENV_NAMES if os.environ.get(name)]
    sas_env_present = int(bool(sas_env_present_names))
    phase350_route_available = as_int(metric_value(phase350_summary, "phase350_sas_env_present")) or sas_env_present
    phase350_new_dates = as_int(metric_value(phase350_summary, "phase350_new_real_l2_dates_added"))
    phase368_next = str(metric_value(phase368_summary, "phase368_next_best_action", ""))

    access_audit = pd.DataFrame(
        [
            {
                "access_route": "existing_local_phase341_phase359_panel",
                "available": 1,
                "evidence": f"phase341_events={phase341_events}; phase359_events={phase359_events}; phase359_dates={';'.join(phase359_unseen_dates)}",
                "secret_material_recorded": 0,
            },
            {
                "access_route": "phase350_sas_or_local_verify_route",
                "available": int(phase350_route_available),
                "evidence": f"phase350_sas_env_present={metric_value(phase350_summary, 'phase350_sas_env_present')}; current_supported_sas_env_names_present={len(sas_env_present_names)}; new_dates_added={phase350_new_dates}",
                "secret_material_recorded": 0,
            },
            {
                "access_route": "manual_local_dropzone",
                "available": 1,
                "evidence": "Can verify a locally dropped raw_l2/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL partition without persisting secrets.",
                "secret_material_recorded": 0,
            },
        ]
    )

    expansion_math = pd.DataFrame(
        [
            ("current_no_lookahead_work_rows", current_work_rows, "Phase341 + Phase359 eligible official-catalyst work rows"),
            ("current_phase366_selected_trades", phase366_trades, "Frozen reversal clue selected trades"),
            ("acceptance_event_floor", 30, "Minimum scheduled/selected event floor used by this branch"),
            ("additional_selected_trades_needed", additional_selected_trades_needed, "Selected trades needed before retest can meet event floor"),
            ("selected_trade_yield_per_work_row", selected_trade_yield, "Phase366 selected trades divided by current work rows"),
            ("eligible_events_needed_at_current_yield", eligible_events_needed_at_current_yield, "Estimated additional eligible events needed at observed yield"),
            ("phase359_eligible_events_per_unseen_day", eligible_events_per_unseen_day, "Observed eligible events per new full-universe local day"),
            ("estimated_full_universe_days_needed", estimated_full_universe_days_needed, "Estimated additional full-universe days needed"),
            ("bytes_per_full_universe_day", bytes_per_full_universe_day, "Observed Phase359 full-universe raw L2 bytes per day"),
            ("estimated_bytes_needed", estimated_bytes_needed, "Estimated disk needed at observed Phase359 size"),
        ],
        columns=["metric", "value", "description"],
    )

    target_contract = pd.DataFrame(
        [
            {
                "target_id": "P369_ONE_DAY_DISK_SAFE_INCREMENT",
                "priority": 1,
                "action": "Add or verify exactly one new full-universe official-catalyst real L2 trade_date partition first.",
                "why": "Disk-aware increment; proves the route and may add 10-20 eligible events without an 80GB pull.",
                "required_shape": "raw_l2/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet",
                "acceptance_retest_allowed_after": 0,
            },
            {
                "target_id": "P369_EVENT_FLOOR_INCREMENT",
                "priority": 2,
                "action": f"Target roughly {estimated_full_universe_days_needed} similar full-universe days before expecting event-floor retest eligibility.",
                "why": f"Observed selected-trade yield implies about {eligible_events_needed_at_current_yield} more eligible catalyst work rows are needed.",
                "required_shape": "same as above, with full top-five depth and official no-lookahead catalyst rows",
                "acceptance_retest_allowed_after": 0,
            },
            {
                "target_id": "P369_RETREAT_TO_REPORT_IF_NO_DATA",
                "priority": 3,
                "action": "If no fresh SAS/azcopy/local drop is available, do not run another acceptance-style strategy shard.",
                "why": "Phase368 already closed the current branch for acceptance; more strategy shards without more events would be theater, not science.",
                "required_shape": "none",
                "acceptance_retest_allowed_after": 0,
            },
        ]
    )

    blockers = pd.DataFrame(
        [
            {
                "blocker_id": "P369_EVENT_FLOOR_NOT_MET",
                "blocking": int(phase366_event_floor_met == 0),
                "evidence": f"phase366_trades={phase366_trades}; needed=30",
                "resolution": "Add/verify more official-catalyst real L2 events before retest.",
            },
            {
                "blocker_id": "P369_NO_CURRENT_DOWNLOAD_ROUTE",
                "blocking": int(not phase350_route_available),
                "evidence": f"phase350_sas_env_present={metric_value(phase350_summary, 'phase350_sas_env_present')}; current_supported_sas_env_names_present={len(sas_env_present_names)}",
                "resolution": "Provide fresh SAS env in-process, install/provide azcopy, or use local dropzone verification.",
            },
            {
                "blocker_id": "P369_ACCEPTANCE_BRANCH_CLOSED",
                "blocking": int(phase366_acceptance == 0),
                "evidence": f"phase366_acceptance={phase366_acceptance}; phase366_ann={phase366_ann}",
                "resolution": "Treat current clue as diagnostic-only until event floor and robustness controls pass.",
            },
        ]
    )

    gates = pd.DataFrame(
        [
            ("P369_PHASE368_TERMINAL_PRESENT", int(bool(phase368_next)), phase368_next),
            ("P369_LOCAL_REAL_EVENT_EVIDENCE_PRESENT", int(current_work_rows > 0), f"work_rows={current_work_rows}"),
            ("P369_EVENT_FLOOR_GAP_COMPUTED", int(additional_selected_trades_needed > 0), f"needed={additional_selected_trades_needed}"),
            ("P369_DISK_INCREMENT_ESTIMATED", int(bytes_per_full_universe_day > 0), f"bytes_per_day={bytes_per_full_universe_day}"),
            ("P369_ACCESS_ROUTE_AUDITED_WITHOUT_SECRETS", int(access_audit["secret_material_recorded"].astype(int).sum() == 0), "secret_rows=0"),
            ("P369_NO_RETEST_WITH_CURRENT_SPARSE_CLUE", int(phase366_event_floor_met == 0 and phase366_acceptance == 0), f"event_floor={phase366_event_floor_met}; acceptance={phase366_acceptance}"),
            ("P369_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "closed"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )

    summary = pd.DataFrame(
        [
            ("phase369_official_catalyst_real_l2_expansion_readiness_complete", int(gates["passed"].astype(int).all()), "Phase369 complete if all hard gates pass"),
            ("phase369_current_no_lookahead_work_rows", current_work_rows, "Phase341 + Phase359 work rows"),
            ("phase369_phase366_selected_trades", phase366_trades, "Current clue selected trades"),
            ("phase369_additional_selected_trades_needed", additional_selected_trades_needed, "Additional trades needed to reach 30"),
            ("phase369_estimated_additional_eligible_events_needed", eligible_events_needed_at_current_yield, "Additional eligible catalyst events estimated"),
            ("phase369_estimated_full_universe_days_needed", estimated_full_universe_days_needed, "Estimated additional full-universe days"),
            ("phase369_bytes_per_full_universe_day", bytes_per_full_universe_day, "Observed bytes per full-universe day"),
            ("phase369_estimated_bytes_needed", estimated_bytes_needed, "Estimated bytes for event-floor-sized increment"),
            ("phase369_current_download_route_available", int(phase350_route_available), "Fresh SAS/env or Phase350 route available now"),
            ("phase369_one_day_increment_recommended", 1, "Disk-safe next increment"),
            ("phase369_acceptance_retest_allowed_now", 0, "No retest until event floor evidence exists"),
            ("phase369_strategy_promotion_allowed", 0, "No promotion"),
            ("phase369_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase369_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase369_hard_gate_pass_rows", int(gates["passed"].astype(int).sum()), "Passed hard gates"),
            ("phase369_hard_gate_rows", len(gates), "Hard gates"),
            ("phase369_next_best_action", "provide_fresh_sas_or_local_drop_one_new_full_universe_official_catalyst_l2_day_then_verify_no_paper_live", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )

    outputs = {
        "summary": output_dir / "phase369_acceptance_summary.csv",
        "access": output_dir / "phase369_access_route_audit.csv",
        "math": output_dir / "phase369_event_floor_expansion_math.csv",
        "target": output_dir / "phase369_target_increment_contract.csv",
        "blockers": output_dir / "phase369_blocker_ledger.csv",
        "gates": output_dir / "phase369_gate_evaluation.csv",
        "report": output_dir / "phase369_official_catalyst_real_l2_expansion_readiness_report.md",
        "manifest": output_dir / "phase369_official_catalyst_real_l2_expansion_readiness_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    access_audit.to_csv(outputs["access"], index=False)
    expansion_math.to_csv(outputs["math"], index=False)
    target_contract.to_csv(outputs["target"], index=False)
    blockers.to_csv(outputs["blockers"], index=False)
    gates.to_csv(outputs["gates"], index=False)

    report = "\n".join(
        [
            "# Phase369 Official-Catalyst Real L2 Expansion Readiness",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase369 turns the Phase368 next action into a concrete data-expansion readiness ledger. It does not download data, does not run a strategy retest, and opens no promotion, paper/live acceptance, or deployable profitability claim.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Access route audit",
            "",
            _markdown_table(access_audit),
            "",
            "## Event-floor expansion math",
            "",
            _markdown_table(expansion_math),
            "",
            "## Target increment contract",
            "",
            _markdown_table(target_contract),
            "",
            "## Blocker ledger",
            "",
            _markdown_table(blockers),
            "",
            "## Gate evaluation",
            "",
            _markdown_table(gates),
            "",
            "Phase369 decision: one new full-universe official-catalyst real L2 day is the disk-safe next increment, but acceptance retesting is still blocked until the event-floor-sized evidence gap is closed.",
            "",
            "No promotion, paper/live acceptance, or deployable profitability claim is opened.",
        ]
    )
    outputs["report"].write_text(report + "\n", encoding="utf-8")

    manifest = {
        "phase": 369,
        "generated_at_utc": generated_utc,
        "supported_sas_env_names_checked": SUPPORTED_SAS_ENV_NAMES,
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase369_official_catalyst_real_l2_expansion_readiness",
            generated_utc=generated_utc,
            inputs={
                "phase341_summary": "outputs/phase341/phase341_acceptance_summary.csv",
                "phase359_summary": "outputs/phase359/phase359_acceptance_summary.csv",
                "phase350_summary": "outputs/phase350/phase350_acceptance_summary.csv",
                "phase366_summary": "outputs/phase366/phase366_acceptance_summary.csv",
                "phase368_summary": "outputs/phase368/phase368_acceptance_summary.csv",
            },
            parameters={
                "event_floor": 30,
                "secret_material_recorded": 0,
                "download_executed": False,
                "strategy_retest_executed": False,
            },
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": str(summary[summary["metric"].eq("phase369_next_best_action")]["value"].iloc[0]),
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))
