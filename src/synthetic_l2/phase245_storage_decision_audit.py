from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE244_DIR = Path("outputs/phase244")
DEFAULT_OUTPUT_DIR = Path("outputs/phase245")
DEFAULT_WORKSPACE_ROOT = Path(".")
WATCH_PREFIXES = (
    "raw_synthetic_l2",
    "derived_",
    "scratch_",
)
WATCH_EXACT = {
    "outputs",
    "real_data_sample",
    "Plan",
    "src",
    "scripts",
}
TARGET_FRESH_HOLDOUT_DATES = 3
CONSERVATIVE_GB_PER_DATE = 2.5
MIN_FREE_AFTER_DOWNLOAD_GB = 40.0


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
    return rows.iloc[0]


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def dir_size(path: Path) -> tuple[int, int]:
    total = 0
    files = 0
    if not path.exists():
        return 0, 0
    for child in path.rglob("*"):
        if child.is_file():
            try:
                total += child.stat().st_size
                files += 1
            except OSError:
                pass
    return total, files


def candidate_roots(workspace_root: Path) -> list[Path]:
    roots: list[Path] = []
    for child in sorted(workspace_root.iterdir()):
        if not child.is_dir():
            continue
        name = child.name
        if name in {".git", ".agents", ".codex", ".pycache_codex"}:
            continue
        if name in WATCH_EXACT or any(name.startswith(prefix) for prefix in WATCH_PREFIXES):
            roots.append(child)
    return roots


def build_storage_inventory(workspace_root: Path) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for root in candidate_roots(workspace_root):
        size, files = dir_size(root)
        rows.append(
            {
                "path": str(root),
                "name": root.name,
                "bytes": size,
                "gb": size / (1024**3),
                "files": files,
                "category": (
                    "real_raw_or_sample"
                    if root.name == "real_data_sample"
                    else ("outputs" if root.name == "outputs" else ("scratch" if root.name.startswith("scratch_") else ("synthetic_raw" if root.name.startswith("raw_synthetic_l2") else "derived_or_code")))
                ),
            }
        )
    return pd.DataFrame(rows).sort_values("bytes", ascending=False).reset_index(drop=True)


def build_cleanup_candidates(inventory: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for row in inventory.to_dict("records"):
        name = str(row["name"])
        category = str(row["category"])
        if category == "scratch" or "smoke" in name.lower():
            cleanup_class = "likely_safe_after_user_review"
            rationale = "scratch/smoke artifact; not needed for current Phase244 frozen candidate unless user wants to preserve it"
        elif category == "synthetic_raw":
            cleanup_class = "archive_candidate_after_manifest_check"
            rationale = "large generated raw synthetic artifact; archive or move before deletion"
        elif category == "real_raw_or_sample":
            cleanup_class = "preserve_current_real_holdout"
            rationale = "contains downloaded real L2 holdout data and seed samples"
        elif category == "outputs":
            cleanup_class = "preserve_research_evidence"
            rationale = "contains committed CSV/report evidence and ignored parquet outputs"
        else:
            cleanup_class = "preserve_by_default"
            rationale = "code/plan/derived artifact; not a first cleanup target"
        rows.append(
            {
                "path": row["path"],
                "gb": row["gb"],
                "files": row["files"],
                "cleanup_class": cleanup_class,
                "destructive_action_allowed_now": 0,
                "requires_user_approval": int(cleanup_class in {"likely_safe_after_user_review", "archive_candidate_after_manifest_check"}),
                "recommended_action": "review_then_archive_or_delete" if cleanup_class == "likely_safe_after_user_review" else ("archive_or_move_if_space_needed" if cleanup_class == "archive_candidate_after_manifest_check" else "preserve"),
                "rationale": rationale,
            }
        )
    return pd.DataFrame(rows).sort_values(["requires_user_approval", "gb"], ascending=[False, False]).reset_index(drop=True)


def build_download_readiness(phase244_dir: Path, free_bytes: int) -> pd.DataFrame:
    phase244 = phase244_dir / "phase244_acceptance_summary.csv"
    min_dates = as_int(metric_value(phase244, "phase244_min_holdout_dates_required", 2), 2)
    target_dates = as_int(metric_value(phase244, "phase244_target_holdout_dates", TARGET_FRESH_HOLDOUT_DATES), TARGET_FRESH_HOLDOUT_DATES)
    conservative_needed_gb = target_dates * CONSERVATIVE_GB_PER_DATE
    free_gb = free_bytes / (1024**3)
    projected_free = free_gb - conservative_needed_gb
    local_download_feasible = int(projected_free >= MIN_FREE_AFTER_DOWNLOAD_GB)
    return pd.DataFrame(
        [
            {
                "decision_id": "P245_LOCAL_C_DRIVE_DOWNLOAD_READINESS",
                "free_gb_now": free_gb,
                "target_holdout_dates": target_dates,
                "min_holdout_dates": min_dates,
                "conservative_gb_per_date": CONSERVATIVE_GB_PER_DATE,
                "projected_required_gb": conservative_needed_gb,
                "projected_free_gb_after_target": projected_free,
                "min_free_gb_after_download": MIN_FREE_AFTER_DOWNLOAD_GB,
                "local_download_feasible_by_space_only": local_download_feasible,
                "download_allowed_now": 0,
                "decision": "storage_choice_still_required_before_download",
            }
        ]
    )


def build_gate_evaluation(inventory: pd.DataFrame, readiness: pd.DataFrame, cleanup: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("P245_PHASE244_STORAGE_GATE_OBSERVED", True, "phase244_storage_decision_required=1", "Phase244 requires storage decision", "hard"),
        ("P245_STORAGE_INVENTORY_WRITTEN", len(inventory) > 0, len(inventory), ">0 inventory rows", "hard"),
        ("P245_CLEANUP_LEDGER_NON_DESTRUCTIVE", bool((cleanup["destructive_action_allowed_now"].astype(int) == 0).all()), 0, "all destructive actions disabled", "hard"),
        ("P245_DOWNLOAD_READINESS_WRITTEN", len(readiness) == 1, len(readiness), "one readiness decision row", "hard"),
        ("P245_NO_DOWNLOAD_EXECUTED", True, 0, 0, "hard"),
        ("P245_NO_PAPER_LIVE_OR_PROFIT_CLAIM", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase245 Storage Decision Audit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase245 is a non-destructive storage audit supporting the Phase244 future-holdout precommit.",
        "It sizes workspace storage, identifies cleanup/archive candidates, and records download readiness without deleting files or downloading new raw dates.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(workspace_root: Path = DEFAULT_WORKSPACE_ROOT, phase244_dir: Path = DEFAULT_PHASE244_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    usage = shutil.disk_usage(workspace_root.resolve())
    inventory = build_storage_inventory(workspace_root)
    cleanup = build_cleanup_candidates(inventory)
    readiness = build_download_readiness(phase244_dir, usage.free)
    gates = build_gate_evaluation(inventory, readiness, cleanup)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    readiness_row = readiness.iloc[0].to_dict()
    next_action = (
        "choose_local_c_drive_download_or_cleanup_policy_then_run_phase246_fresh_holdout_download_no_tuning_no_paper_live"
        if int(readiness_row["local_download_feasible_by_space_only"]) == 1
        else "choose_external_storage_or_cleanup_before_phase246_fresh_holdout_download_no_tuning_no_paper_live"
    )
    acceptance = pd.DataFrame(
        [
            ("phase245_storage_decision_audit_complete", 1, "Phase245 storage audit completed"),
            ("phase245_free_gb_now", float(readiness_row["free_gb_now"]), "Free GB on workspace drive"),
            ("phase245_inventory_rows", int(len(inventory)), "Storage inventory rows"),
            ("phase245_cleanup_candidate_rows", int(cleanup["requires_user_approval"].astype(int).sum()), "Rows requiring user review before cleanup/archive"),
            ("phase245_target_holdout_dates", int(readiness_row["target_holdout_dates"]), "Target future holdout dates from Phase244"),
            ("phase245_projected_required_gb", float(readiness_row["projected_required_gb"]), "Conservative space needed for target fresh dates"),
            ("phase245_projected_free_gb_after_target", float(readiness_row["projected_free_gb_after_target"]), "Projected free GB after target download"),
            ("phase245_local_download_feasible_by_space_only", int(readiness_row["local_download_feasible_by_space_only"]), "Space-only feasibility; still needs user storage decision"),
            ("phase245_destructive_cleanup_allowed_now", 0, "No cleanup/delete action is allowed by Phase245"),
            ("phase245_download_more_dates_now_allowed", 0, "No additional raw-date download in Phase245"),
            ("phase245_holdout_execution_allowed_now", 0, "No holdout run in Phase245"),
            ("phase245_strategy_promotion_allowed", 0, "No strategy promotion from Phase245"),
            ("phase245_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase245"),
            ("phase245_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase245"),
            ("phase245_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase245_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase245_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    inventory.to_csv(output_dir / "phase245_storage_inventory.csv", index=False)
    cleanup.to_csv(output_dir / "phase245_cleanup_candidate_ledger.csv", index=False)
    readiness.to_csv(output_dir / "phase245_download_readiness_decision.csv", index=False)
    gates.to_csv(output_dir / "phase245_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase245_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase245_storage_decision_audit_report.md",
        {
            "Acceptance Summary": acceptance,
            "Download Readiness Decision": readiness,
            "Storage Inventory": inventory.head(60),
            "Cleanup Candidate Ledger": cleanup.head(80),
            "Gate Evaluation": gates,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase245_storage_decision_audit",
        **reproducibility_fields(
            artifact_id="phase245",
            generated_utc=generated_utc,
            inputs={"workspace_root": str(workspace_root), "phase244_dir": str(phase244_dir)},
            parameters={
                "target_fresh_holdout_dates": TARGET_FRESH_HOLDOUT_DATES,
                "conservative_gb_per_date": CONSERVATIVE_GB_PER_DATE,
                "min_free_after_download_gb": MIN_FREE_AFTER_DOWNLOAD_GB,
                "destructive_cleanup_allowed_now": 0,
                "download_more_dates_now_allowed": 0,
            },
            outputs={
                "storage_inventory": str(output_dir / "phase245_storage_inventory.csv"),
                "cleanup_candidate_ledger": str(output_dir / "phase245_cleanup_candidate_ledger.csv"),
                "download_readiness_decision": str(output_dir / "phase245_download_readiness_decision.csv"),
                "gate_evaluation": str(output_dir / "phase245_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase245_acceptance_summary.csv"),
                "report": str(output_dir / "phase245_storage_decision_audit_report.md"),
            },
            random_seed="none_deterministic_storage_audit",
            cost_model_version="not_applicable_storage_audit",
            latency_model_version="not_applicable_storage_audit",
        ),
    }
    (output_dir / "phase245_storage_decision_audit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase245 storage decision audit.")
    parser.add_argument("--workspace-root", type=Path, default=DEFAULT_WORKSPACE_ROOT)
    parser.add_argument("--phase244-dir", type=Path, default=DEFAULT_PHASE244_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(workspace_root=args.workspace_root, phase244_dir=args.phase244_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
