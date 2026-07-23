from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase95_real_anchor_panel_contract import EXPECTED_SYMBOLS
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase137")
DEFAULT_PHASE132_DIR = Path("outputs/phase132")
DEFAULT_PHASE117_DIR = Path("outputs/phase117")
DEFAULT_PHASE116_DIR = Path("outputs/phase116")
DEFAULT_PHASE115_DIR = Path("outputs/phase115")
MIN_READY_REAL_DAYS = 5
TARGET_READY_REAL_DAYS = 10


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


def build_closed_branch_ledger(phase132_acceptance: pd.DataFrame, phase116_blocklist: pd.DataFrame) -> pd.DataFrame:
    kill = as_int(metric_value(phase132_acceptance, "phase132_kill_switch_fired"), 1)
    survivors = as_int(metric_value(phase132_acceptance, "phase132_surviving_feature_rows"), 0)
    labels_cleared = as_int(metric_value(phase132_acceptance, "phase132_labels_cleared_brier_lift"), 0)
    blocklisted = int(
        not phase116_blocklist.empty
        and phase116_blocklist["blocked_family_id"].astype(str).eq("DEEP_BOOK_LABEL_LIFT").any()
    )
    return pd.DataFrame(
        [
            {
                "closed_branch_id": "PHASE131_132_TOP_FIVE_DEPTH_LABEL_LIFT",
                "phase132_kill_switch_fired": kill,
                "phase132_surviving_feature_rows": survivors,
                "phase132_labels_cleared_brier_lift": labels_cleared,
                "phase116_blocklist_entry_present": blocklisted,
                "phase133_136_allowed": 0,
                "synthetic_strategy_branch_allowed": 0,
                "strategy_replay_allowed": 0,
                "closure_verdict": "falsified" if kill and blocklisted else "closure_incomplete",
                "why": "Phase132 found no top-five-depth diagnostic lift over Phase130 baselines; continuation plan says skip Phase133-136.",
            }
        ]
    )


def build_real_anchor_requirements(phase117_acceptance: pd.DataFrame) -> pd.DataFrame:
    ready = as_int(metric_value(phase117_acceptance, "phase117_current_ready_real_anchor_days"), 0)
    min_missing = max(0, MIN_READY_REAL_DAYS - ready)
    target_missing = max(0, TARGET_READY_REAL_DAYS - ready)
    rows: list[dict[str, Any]] = []
    for slot in range(1, target_missing + 1):
        rows.append(
            {
                "slot_id": f"POST_P132_REAL_L2_DAY_{ready + slot:02d}",
                "required_for": "minimum_replay_unlock_review" if slot <= min_missing else "preferred_real_anchor_target",
                "current_ready_real_anchor_days": ready,
                "trade_date": "TBD_real_nse_trading_day",
                "exchange": "NSE",
                "symbols_required": len(EXPECTED_SYMBOLS),
                "minimum_expected_symbol_fraction": 0.95,
                "required_layout": "real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet",
                "required_content": "raw Zerodha Level-2/top-five market-by-price WebSocket updates with depth_level_1 through depth_level_5 bid/ask price, quantity and order-count fields",
                "acceptance_command_after_drop": "python scripts/run_phase115_real_panel_refresh_orchestrator.py --source-root real_data_sample/l2_multiday_panel --execute-import",
                "unlock_note": "Replay remains closed until Phase115/Phase110 prove enough ready real-anchor days and downstream realism gates are refreshed.",
            }
        )
    if not rows:
        rows.append(
            {
                "slot_id": "POST_P132_REAL_L2_TARGET_ALREADY_MET",
                "required_for": "none",
                "current_ready_real_anchor_days": ready,
                "trade_date": "",
                "exchange": "NSE",
                "symbols_required": len(EXPECTED_SYMBOLS),
                "minimum_expected_symbol_fraction": 0.95,
                "required_layout": "already_satisfied",
                "required_content": "already_satisfied",
                "acceptance_command_after_drop": "python scripts/run_phase115_real_panel_refresh_orchestrator.py --execute-import",
                "unlock_note": "Rerun Phase115/Phase110 before opening replay.",
            }
        )
    return pd.DataFrame(rows)


def build_operational_runbook(phase117_acceptance: pd.DataFrame) -> pd.DataFrame:
    ready = as_int(metric_value(phase117_acceptance, "phase117_current_ready_real_anchor_days"), 0)
    min_missing = max(0, MIN_READY_REAL_DAYS - ready)
    return pd.DataFrame(
        [
            {
                "step": 1,
                "action": "stop_synthetic_strategy_branching",
                "command": "No command. Do not run Phase133-136 for the closed Phase131-132 branch.",
                "runs_now": False,
                "expected_evidence": "outputs/phase132/kill_switch_summary.csv has kill_switch_fired=1 and outputs/phase116/strategy_replay_blocklist.csv contains DEEP_BOOK_LABEL_LIFT.",
            },
            {
                "step": 2,
                "action": "collect_or_sync_real_l2_days",
                "command": f"Add at least {min_missing} new real NSE trading days under real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet",
                "runs_now": False,
                "expected_evidence": "Each new day covers at least 95 percent of the current 32-symbol universe and includes top-five market-by-price depth fields.",
            },
            {
                "step": 3,
                "action": "dry_run_refresh",
                "command": "python scripts/run_phase115_real_panel_refresh_orchestrator.py --source-root real_data_sample/l2_multiday_panel",
                "runs_now": False,
                "expected_evidence": "Phase115 discovers candidate days without copying files; use this if newly dropped data needs layout validation first.",
            },
            {
                "step": 4,
                "action": "execute_import_refresh",
                "command": "python scripts/run_phase115_real_panel_refresh_orchestrator.py --source-root real_data_sample/l2_multiday_panel --execute-import",
                "runs_now": False,
                "expected_evidence": "Phase113 copies files, Phase114 integrity passes, Phase96/Phase110 ready day counts update.",
            },
            {
                "step": 5,
                "action": "review_replay_unlock_gate",
                "command": "Import-Csv outputs/phase115/phase115_real_panel_refresh_acceptance_summary.csv",
                "runs_now": False,
                "expected_evidence": "Replay remains closed unless Phase110/115 explicitly prove unlock conditions.",
            },
        ]
    )


def build_gate_evaluation(
    closed_branch: pd.DataFrame,
    requirements: pd.DataFrame,
    phase117_acceptance: pd.DataFrame,
    phase115_acceptance: pd.DataFrame,
) -> pd.DataFrame:
    ready = as_int(metric_value(phase117_acceptance, "phase117_current_ready_real_anchor_days"), 0)
    days_needed = max(0, MIN_READY_REAL_DAYS - ready)
    replay_allowed_115 = as_int(metric_value(phase115_acceptance, "phase115_strategy_replay_allowed"), 0)
    return pd.DataFrame(
        [
            {
                "gate_id": "P137_PHASE132_BRANCH_CLOSED",
                "gate_pass": int(not closed_branch.empty and closed_branch["closure_verdict"].astype(str).eq("falsified").all()),
                "evidence": f"closure_verdict={closed_branch['closure_verdict'].iloc[0] if not closed_branch.empty else 'missing'}",
            },
            {
                "gate_id": "P137_PHASE133_136_SKIPPED",
                "gate_pass": int(not closed_branch.empty and closed_branch["phase133_136_allowed"].astype(int).sum() == 0),
                "evidence": "phase133_136_allowed=0",
            },
            {
                "gate_id": "P137_REAL_ANCHOR_DEFICIT_DECLARED",
                "gate_pass": int(days_needed > 0 and not requirements.empty),
                "evidence": f"ready_real_anchor_days={ready}; days_needed_for_min={days_needed}",
            },
            {
                "gate_id": "P137_OPERATIONAL_RUNBOOK_DECLARED",
                "gate_pass": 1,
                "evidence": "post-Phase132 real-anchor acquisition runbook emitted",
            },
            {
                "gate_id": "P137_REPLAY_REMAINS_CLOSED",
                "gate_pass": int(replay_allowed_115 == 0 and closed_branch["strategy_replay_allowed"].astype(int).sum() == 0),
                "evidence": f"phase115_strategy_replay_allowed={replay_allowed_115}",
            },
        ]
    )


def build_acceptance_summary(
    closed_branch: pd.DataFrame,
    requirements: pd.DataFrame,
    gates: pd.DataFrame,
    phase117_acceptance: pd.DataFrame,
    phase115_acceptance: pd.DataFrame,
) -> pd.DataFrame:
    ready = as_int(metric_value(phase117_acceptance, "phase117_current_ready_real_anchor_days"), 0)
    min_missing = max(0, MIN_READY_REAL_DAYS - ready)
    target_missing = max(0, TARGET_READY_REAL_DAYS - ready)
    replay_allowed_115 = as_int(metric_value(phase115_acceptance, "phase115_strategy_replay_allowed"), 0)
    return pd.DataFrame(
        [
            ("phase137_closed_branch_rows", int(len(closed_branch)), "Closed synthetic top-five-depth branch ledger rows"),
            ("phase137_phase132_kill_switch_fired", int(closed_branch["phase132_kill_switch_fired"].iloc[0]) if not closed_branch.empty else 0, "Phase132 kill-switch flag carried forward"),
            ("phase137_phase116_deep_book_blocklist_present", int(closed_branch["phase116_blocklist_entry_present"].iloc[0]) if not closed_branch.empty else 0, "Phase116 DEEP_BOOK_LABEL_LIFT row present"),
            ("phase137_current_ready_real_anchor_days", ready, "Ready real-anchor days currently proven"),
            ("phase137_additional_days_needed_for_min", min_missing, "Additional ready real days needed for minimum replay-unlock review"),
            ("phase137_additional_days_needed_for_target", target_missing, "Additional ready real days needed for preferred 10-day target"),
            ("phase137_real_anchor_requirement_rows", int(len(requirements)), "Real-anchor acquisition requirement rows emitted"),
            ("phase137_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase137_all_gates_pass", int(gates["gate_pass"].astype(bool).all()) if not gates.empty else 0, "1 means Phase137 restart work order is self-consistent"),
            ("phase137_strategy_replay_allowed", replay_allowed_115, "Replay flag remains inherited from Phase115"),
            ("phase137_next_best_action", f"drop_or_sync_{min_missing}_more_real_l2_days_then_run_phase115_execute_import" if min_missing else "run_phase115_execute_import_and_review_unlock", "Recommended next milestone"),
            ("phase137_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned cost model retained for audit continuity"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase137 Post-Phase132 Real-Anchor Restart",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase137 converts the Phase132 clean falsification into the next operational path: real Zerodha L2 anchor acquisition.",
        "It does not reopen synthetic strategy work, run Phase133-136, emit order simulations, or change replay permissions.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase137_post_phase132_real_anchor_restart_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase137(base_dir: Path, output_dir: Path, phase132_dir: Path, phase117_dir: Path, phase116_dir: Path, phase115_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase132_acceptance = read_csv(base_dir / phase132_dir / "phase132_deep_book_feature_diagnostics_acceptance_summary.csv")
    phase117_acceptance = read_csv(base_dir / phase117_dir / "phase117_real_anchor_acquisition_acceptance_summary.csv")
    phase116_blocklist = read_csv(base_dir / phase116_dir / "strategy_replay_blocklist.csv")
    phase115_acceptance = read_csv(base_dir / phase115_dir / "phase115_real_panel_refresh_acceptance_summary.csv")

    closed_branch = build_closed_branch_ledger(phase132_acceptance, phase116_blocklist)
    requirements = build_real_anchor_requirements(phase117_acceptance)
    runbook = build_operational_runbook(phase117_acceptance)
    gates = build_gate_evaluation(closed_branch, requirements, phase117_acceptance, phase115_acceptance)
    acceptance = build_acceptance_summary(closed_branch, requirements, gates, phase117_acceptance, phase115_acceptance)

    closed_branch.to_csv(output_dir / "closed_synthetic_branch_ledger.csv", index=False)
    requirements.to_csv(output_dir / "real_anchor_acquisition_requirements.csv", index=False)
    runbook.to_csv(output_dir / "real_anchor_operational_runbook.csv", index=False)
    gates.to_csv(output_dir / "phase137_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase137_post_phase132_real_anchor_restart_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Closed Synthetic Branch Ledger": closed_branch,
            "Real Anchor Acquisition Requirements": requirements,
            "Operational Runbook": runbook,
            "Gate Evaluation": gates,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase137_post_phase132_real_anchor_restart",
        "strategy_replay_allowed": 0,
        "synthetic_strategy_branch_allowed": 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase137",
            generated_utc=generated_utc,
            inputs={
                "phase132_acceptance": str(phase132_dir / "phase132_deep_book_feature_diagnostics_acceptance_summary.csv"),
                "phase117_acceptance": str(phase117_dir / "phase117_real_anchor_acquisition_acceptance_summary.csv"),
                "phase116_blocklist": str(phase116_dir / "strategy_replay_blocklist.csv"),
                "phase115_acceptance": str(phase115_dir / "phase115_real_panel_refresh_acceptance_summary.csv"),
            },
            parameters={
                "post_phase132_policy": "synthetic_top_five_depth_branch_closed",
                "next_path": "real_zerodha_l2_anchor_acquisition",
                "minimum_ready_real_days": MIN_READY_REAL_DAYS,
                "target_ready_real_days": TARGET_READY_REAL_DAYS,
                "replay_policy": "closed_until_phase115_phase110_unlock",
            },
            outputs={
                "closed_branch": str(output_dir / "closed_synthetic_branch_ledger.csv"),
                "requirements": str(output_dir / "real_anchor_acquisition_requirements.csv"),
                "runbook": str(output_dir / "real_anchor_operational_runbook.csv"),
                "gates": str(output_dir / "phase137_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase137_post_phase132_real_anchor_restart_acceptance_summary.csv"),
                "report": str(output_dir / "phase137_post_phase132_real_anchor_restart_report.md"),
                "manifest": str(output_dir / "phase137_post_phase132_real_anchor_restart_manifest.json"),
            },
            random_seed="none_deterministic_restart_work_order",
            scenario_ids="phase137_real_anchor_restart_after_phase132_falsification",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_restart_work_order",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase137_post_phase132_real_anchor_restart_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase137 post-Phase132 real-anchor restart work order.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--phase132-dir", type=Path, default=DEFAULT_PHASE132_DIR)
    parser.add_argument("--phase117-dir", type=Path, default=DEFAULT_PHASE117_DIR)
    parser.add_argument("--phase116-dir", type=Path, default=DEFAULT_PHASE116_DIR)
    parser.add_argument("--phase115-dir", type=Path, default=DEFAULT_PHASE115_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase137(
        base_dir=args.base_dir,
        output_dir=args.output_dir,
        phase132_dir=args.phase132_dir,
        phase117_dir=args.phase117_dir,
        phase116_dir=args.phase116_dir,
        phase115_dir=args.phase115_dir,
    )


if __name__ == "__main__":
    main()
