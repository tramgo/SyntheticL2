from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_OUTPUT_DIR = Path("outputs/phase146")
DEFAULT_PHASE95_SUMMARY = Path("outputs/phase95/real_anchor_panel_acceptance_summary.csv")
DEFAULT_PHASE96_SUMMARY = Path("outputs/phase115/subruns/phase96/real_anchor_panel_builder_acceptance_summary.csv")
DEFAULT_PHASE96_MANIFEST = Path("outputs/phase115/subruns/phase96/real_anchor_panel_manifest.csv")
DEFAULT_PHASE110_SUMMARY = Path("outputs/phase115/subruns/phase110/phase110_multiday_replay_unlock_acceptance_summary.csv")
DEFAULT_PHASE115_SUMMARY = Path("outputs/phase115/phase115_real_panel_refresh_acceptance_summary.csv")
DEFAULT_PHASE142_SUMMARY = Path("outputs/phase142/phase142_local_real_l2_download_verifier_acceptance_summary.csv")
DEFAULT_PHASE143_SUMMARY = Path("outputs/phase143/phase143_real_l2_two_date_preflight_acceptance_summary.csv")
DEFAULT_PHASE145_SUMMARY = Path("outputs/phase145/phase145_real_l2_post_download_refresh_acceptance_summary.csv")
DEFAULT_MIN_READY_REAL_DAYS = 5


def read_metric_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["metric", "value", "description"])
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


def snapshot_row(phase: str, path: Path, frame: pd.DataFrame, metrics: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for metric in metrics:
        rows.append(
            {
                "phase": phase,
                "source_path": str(path),
                "source_exists": path.exists(),
                "metric": metric,
                "value": metric_value(frame, metric, ""),
            }
        )
    return rows


def evaluate_gates(
    phase96: pd.DataFrame,
    phase110: pd.DataFrame,
    phase115: pd.DataFrame,
    phase143: pd.DataFrame,
    phase145: pd.DataFrame,
    min_ready_real_days: int,
) -> pd.DataFrame:
    phase96_ready = as_int(metric_value(phase96, "phase96_max_ready_dates_in_panel", metric_value(phase96, "phase96_ready_anchor_days", 0)))
    phase96_unlocked = as_int(metric_value(phase96, "phase96_strategy_replay_unlocked", 0))
    phase110_ready = as_int(metric_value(phase110, "phase110_ready_real_anchor_days", 0))
    phase110_required = as_int(metric_value(phase110, "phase110_required_ready_real_days_min", min_ready_real_days), min_ready_real_days)
    phase110_unlocked = as_int(metric_value(phase110, "phase110_replay_unlock_allowed", 0))
    phase115_ready = as_int(metric_value(phase115, "phase115_phase110_ready_real_anchor_days", 0))
    phase115_days_needed = as_int(metric_value(phase115, "phase115_phase110_days_needed_for_min", min_ready_real_days), min_ready_real_days)
    phase115_unlocked = as_int(metric_value(phase115, "phase115_replay_unlock_allowed", 0))
    required_rows = as_int(metric_value(phase143, "phase143_required_date_rows", 0))
    required_satisfied = as_int(metric_value(phase143, "phase143_required_dates_satisfied", 0))
    phase145_failed = as_int(metric_value(phase145, "phase145_failed_steps", 1), 1)
    phase145_import_executed = as_int(metric_value(phase145, "phase145_phase115_import_executed", 0))

    canonical_ready_days = min(phase96_ready, phase110_ready, phase115_ready)
    ready_consistent = bool(phase96_ready == phase110_ready == phase115_ready)
    min_days_pass = bool(canonical_ready_days >= min_ready_real_days)
    days_needed_pass = bool(phase115_days_needed == max(0, phase110_required - phase115_ready))
    unlock_consistent = bool(phase96_unlocked == phase110_unlocked == phase115_unlocked)
    replay_can_open = bool(min_days_pass and ready_consistent and days_needed_pass and unlock_consistent and phase115_unlocked == 1)

    rows = [
        {
            "gate": "phase96_phase110_phase115_ready_day_consistency",
            "pass": ready_consistent,
            "observed": f"phase96={phase96_ready};phase110={phase110_ready};phase115={phase115_ready}",
            "required": "all_ready_day_counts_equal",
            "severity": "hard",
        },
        {
            "gate": "minimum_ready_real_anchor_days",
            "pass": min_days_pass,
            "observed": canonical_ready_days,
            "required": min_ready_real_days,
            "severity": "hard",
        },
        {
            "gate": "phase115_days_needed_arithmetic",
            "pass": days_needed_pass,
            "observed": phase115_days_needed,
            "required": max(0, phase110_required - phase115_ready),
            "severity": "hard",
        },
        {
            "gate": "replay_unlock_flag_consistency",
            "pass": unlock_consistent,
            "observed": f"phase96={phase96_unlocked};phase110={phase110_unlocked};phase115={phase115_unlocked}",
            "required": "all_unlock_flags_equal",
            "severity": "hard",
        },
        {
            "gate": "phase145_post_download_refresh_clean",
            "pass": bool(phase145_failed == 0),
            "observed": phase145_failed,
            "required": 0,
            "severity": "hard",
        },
        {
            "gate": "configured_required_dates_satisfied",
            "pass": bool(required_rows > 0 and required_satisfied == required_rows),
            "observed": f"{required_satisfied}/{required_rows}",
            "required": "all_required_dates_ready_in_scratch_or_target",
            "severity": "diagnostic_until_minimum_days_pass",
        },
        {
            "gate": "phase115_import_ran_after_download",
            "pass": bool(phase145_import_executed == 1),
            "observed": phase145_import_executed,
            "required": 1,
            "severity": "diagnostic_until_required_dates_satisfied",
        },
        {
            "gate": "phase146_strategy_replay_can_open",
            "pass": replay_can_open,
            "observed": int(replay_can_open),
            "required": 1,
            "severity": "hard",
        },
    ]
    return pd.DataFrame(rows)


def summarize(gates: pd.DataFrame, phase96: pd.DataFrame, phase110: pd.DataFrame, phase115: pd.DataFrame, phase143: pd.DataFrame, phase145: pd.DataFrame, min_ready_real_days: int) -> pd.DataFrame:
    hard_gates = gates.loc[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard_gates["pass"].astype(bool).sum()) if not hard_gates.empty else 0
    hard_total = int(len(hard_gates))
    ready_days = as_int(metric_value(phase115, "phase115_phase110_ready_real_anchor_days", 0))
    days_needed = as_int(metric_value(phase115, "phase115_phase110_days_needed_for_min", min_ready_real_days), min_ready_real_days)
    required_rows = as_int(metric_value(phase143, "phase143_required_date_rows", 0))
    required_satisfied = as_int(metric_value(phase143, "phase143_required_dates_satisfied", 0))
    phase145_import = as_int(metric_value(phase145, "phase145_phase115_import_executed", 0))
    replay_can_open = bool(gates.loc[gates["gate"].eq("phase146_strategy_replay_can_open"), "pass"].astype(bool).any())
    next_action = (
        "run_synthetic_only_strategy_replay_with_real_anchor_gate_recorded"
        if replay_can_open
        else "download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase145_phase146"
    )
    return pd.DataFrame(
        [
            ("phase146_hard_gate_rows", hard_total, "Hard unlock-audit gates evaluated"),
            ("phase146_hard_gate_pass_rows", hard_pass, "Hard unlock-audit gates passed"),
            ("phase146_minimum_ready_real_days", min_ready_real_days, "Minimum ready real-anchor days required before replay unlock"),
            ("phase146_phase115_ready_real_anchor_days", ready_days, "Ready real-anchor days reported by Phase115/110"),
            ("phase146_days_needed_for_min", days_needed, "Additional ready real-anchor days still needed"),
            ("phase146_required_date_rows", required_rows, "Required download/import dates checked by Phase143"),
            ("phase146_required_dates_satisfied", required_satisfied, "Required dates ready in scratch or target"),
            ("phase146_phase145_import_executed", phase145_import, "Whether Phase145 ran Phase115 import on this pass"),
            ("phase146_minimum_unlock_audit_pass", int(hard_pass == hard_total and hard_total > 0), "1 means all hard audit gates passed"),
            ("phase146_strategy_replay_allowed", int(replay_can_open), "1 means downstream strategy replay can open under this audit"),
            ("phase146_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase146 Real-anchor Minimum Unlock Audit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase146 is a read-only audit gate. It reconciles Phase96, Phase110, Phase115, Phase143, and Phase145 evidence before strategy replay is allowed to proceed.",
        "It does not contact Azure, does not import data, and does not infer readiness from partial downloads.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase146_real_anchor_minimum_unlock_audit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase146(
    output_dir: Path,
    base_dir: Path,
    phase95_summary: Path,
    phase96_summary: Path,
    phase96_manifest: Path,
    phase110_summary: Path,
    phase115_summary: Path,
    phase142_summary: Path,
    phase143_summary: Path,
    phase145_summary: Path,
    min_ready_real_days: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase95 = read_metric_table(phase95_summary)
    phase96 = read_metric_table(phase96_summary)
    phase110 = read_metric_table(phase110_summary)
    phase115 = read_metric_table(phase115_summary)
    phase142 = read_metric_table(phase142_summary)
    phase143 = read_metric_table(phase143_summary)
    phase145 = read_metric_table(phase145_summary)

    evidence_rows: list[dict[str, Any]] = []
    evidence_rows.extend(snapshot_row("phase95", phase95_summary, phase95, ["phase95_ready_anchor_days", "phase95_strategy_replay_unlocked"]))
    evidence_rows.extend(snapshot_row("phase96", phase96_summary, phase96, ["phase96_ready_anchor_days", "phase96_max_ready_dates_in_panel", "phase96_strategy_replay_unlocked"]))
    evidence_rows.extend(snapshot_row("phase110", phase110_summary, phase110, ["phase110_ready_real_anchor_days", "phase110_required_ready_real_days_min", "phase110_days_needed_for_min", "phase110_replay_unlock_allowed"]))
    evidence_rows.extend(snapshot_row("phase115", phase115_summary, phase115, ["phase115_phase96_ready_anchor_days", "phase115_phase110_ready_real_anchor_days", "phase115_phase110_days_needed_for_min", "phase115_replay_unlock_allowed"]))
    evidence_rows.extend(snapshot_row("phase142", phase142_summary, phase142, ["phase142_ready_date_rows", "phase142_canonical_symbol_partition_rows", "phase142_nested_trade_date_symbol_partition_rows"]))
    evidence_rows.extend(snapshot_row("phase143", phase143_summary, phase143, ["phase143_required_date_rows", "phase143_required_dates_satisfied", "phase143_can_run_phase115_import_now"]))
    evidence_rows.extend(snapshot_row("phase145", phase145_summary, phase145, ["phase145_failed_steps", "phase145_phase115_import_executed", "phase145_ready_real_anchor_days", "phase145_days_needed_for_min"]))
    evidence = pd.DataFrame(evidence_rows)
    evidence = pd.concat(
        [
            evidence,
            pd.DataFrame(
                [
                    {
                        "phase": "phase96",
                        "source_path": str(phase96_manifest),
                        "source_exists": phase96_manifest.exists(),
                        "metric": "phase96_manifest_exists",
                        "value": int(phase96_manifest.exists()),
                    }
                ]
            ),
        ],
        ignore_index=True,
    )

    gates = evaluate_gates(phase96, phase110, phase115, phase143, phase145, min_ready_real_days)
    acceptance = summarize(gates, phase96, phase110, phase115, phase143, phase145, min_ready_real_days)

    acceptance.to_csv(output_dir / "phase146_real_anchor_minimum_unlock_audit_acceptance_summary.csv", index=False)
    gates.to_csv(output_dir / "phase146_gate_evaluation.csv", index=False)
    evidence.to_csv(output_dir / "phase146_evidence_snapshot.csv", index=False)
    write_report(output_dir, {"Acceptance Summary": acceptance, "Gate Evaluation": gates, "Evidence Snapshot": evidence})

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase146_real_anchor_minimum_unlock_audit",
        **reproducibility_fields(
            artifact_id="phase146",
            generated_utc=generated_utc,
            inputs={
                "phase95_summary": str(phase95_summary),
                "phase96_summary": str(phase96_summary),
                "phase96_manifest": str(phase96_manifest),
                "phase110_summary": str(phase110_summary),
                "phase115_summary": str(phase115_summary),
                "phase142_summary": str(phase142_summary),
                "phase143_summary": str(phase143_summary),
                "phase145_summary": str(phase145_summary),
            },
            parameters={
                "minimum_ready_real_days": min_ready_real_days,
                "strategy_replay_policy": "closed_until_phase96_phase110_phase115_hard_gates_all_pass_and_unlock_flags_are_consistent",
            },
            outputs={
                "acceptance_summary": str(output_dir / "phase146_real_anchor_minimum_unlock_audit_acceptance_summary.csv"),
                "gate_evaluation": str(output_dir / "phase146_gate_evaluation.csv"),
                "evidence_snapshot": str(output_dir / "phase146_evidence_snapshot.csv"),
                "report": str(output_dir / "phase146_real_anchor_minimum_unlock_audit_report.md"),
                "manifest": str(output_dir / "phase146_real_anchor_minimum_unlock_audit_manifest.json"),
            },
            random_seed="none_read_only_audit",
            scenario_ids="phase146_real_anchor_minimum_unlock_audit",
            cost_model_version="not_applicable",
            latency_model_version="phase96_phase110_phase115_unlock_gate",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase146_real_anchor_minimum_unlock_audit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit real-anchor minimum unlock evidence before strategy replay.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--phase95-summary", type=Path, default=DEFAULT_PHASE95_SUMMARY)
    parser.add_argument("--phase96-summary", type=Path, default=DEFAULT_PHASE96_SUMMARY)
    parser.add_argument("--phase96-manifest", type=Path, default=DEFAULT_PHASE96_MANIFEST)
    parser.add_argument("--phase110-summary", type=Path, default=DEFAULT_PHASE110_SUMMARY)
    parser.add_argument("--phase115-summary", type=Path, default=DEFAULT_PHASE115_SUMMARY)
    parser.add_argument("--phase142-summary", type=Path, default=DEFAULT_PHASE142_SUMMARY)
    parser.add_argument("--phase143-summary", type=Path, default=DEFAULT_PHASE143_SUMMARY)
    parser.add_argument("--phase145-summary", type=Path, default=DEFAULT_PHASE145_SUMMARY)
    parser.add_argument("--min-ready-real-days", type=int, default=DEFAULT_MIN_READY_REAL_DAYS)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase146(
        output_dir=args.output_dir,
        base_dir=args.base_dir,
        phase95_summary=args.phase95_summary,
        phase96_summary=args.phase96_summary,
        phase96_manifest=args.phase96_manifest,
        phase110_summary=args.phase110_summary,
        phase115_summary=args.phase115_summary,
        phase142_summary=args.phase142_summary,
        phase143_summary=args.phase143_summary,
        phase145_summary=args.phase145_summary,
        min_ready_real_days=args.min_ready_real_days,
    )


if __name__ == "__main__":
    main()
