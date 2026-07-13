from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


GATE_PRIORITY = {
    "G04_risk": 1,
    "G02_economic": 2,
    "G01_predictive": 3,
    "G03_robustness": 4,
    "G05_realism": 5,
}

GATE_WORK_PACKAGE = {
    "G01_predictive": "WP9/WP10",
    "G02_economic": "WP8/WP10",
    "G03_robustness": "WP9/WP10",
    "G04_risk": "WP8",
    "G05_realism": "WP10",
}

ACCEPTANCE_MILESTONE = {
    "G01_predictive": "multi_seed_predictive_validation",
    "G02_economic": "broker_reconciled_full_run_economic_validation",
    "G03_robustness": "full_registry_robustness_execution",
    "G04_risk": "full_lifecycle_acceptance_risk_run",
    "G05_realism": "holdout_generator_strategy_rerun",
}

DEPENDENCY_NOTE = {
    "G01_predictive": "Requires calibrated model outputs, baseline comparisons, multi-seed synthetic runs and later multi-day real holdout.",
    "G02_economic": "Requires full event/tick execution P&L, Zerodha rupee cost formulas, slippage stress and broker contract-note reconciliation where available.",
    "G03_robustness": "Requires full required-seed execution, walk-forward folds, parameter-neighborhood smoothness, holdout-generator reruns and real-data reruns.",
    "G04_risk": "Requires full lifecycle risk state over generated trades, daily equity curves, position exposure, halt behavior and tail-loss summaries.",
    "G05_realism": "Requires strategy reruns on holdout generator configurations with feed imperfections and pessimistic execution controls.",
}


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    text = frame.copy()
    for column in text.columns:
        text[column] = text[column].map(lambda value: "" if pd.isna(value) else str(value))
    headers = [str(column) for column in text.columns]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in text.values.tolist())
    return "\n".join(lines)


def load_inputs(paths: dict[str, Path]) -> dict[str, pd.DataFrame]:
    return {
        "acceptance_blockers": pd.read_csv(paths["acceptance_blockers"]),
        "strategy_acceptance_summary": pd.read_csv(paths["strategy_acceptance_summary"]),
        "implementation_gap_backlog": pd.read_csv(paths["implementation_gap_backlog"]),
        "deliverable_traceability": pd.read_csv(paths["deliverable_traceability"]),
    }


def build_gate_summary(blockers: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for gate_id, group in blockers.groupby("gate_id", sort=True):
        rows.append(
            {
                "gate_id": gate_id,
                "gate_name": group["gate_name"].iloc[0],
                "blocked_strategies": int(group["strategy_id"].nunique()),
                "blocker_rows": int(len(group)),
                "blocker_categories": "; ".join(sorted(group["blocker_category"].dropna().astype(str).unique())),
                "evidence_sources_present": int((group["evidence_source_status"] == "present").sum()),
                "evidence_sources_missing": int((group["evidence_source_status"] != "present").sum()),
                "priority_rank": GATE_PRIORITY.get(gate_id, 99),
                "work_package_focus": GATE_WORK_PACKAGE.get(gate_id, "unmapped"),
                "acceptance_milestone": ACCEPTANCE_MILESTONE.get(gate_id, "unmapped"),
                "dependency_note": DEPENDENCY_NOTE.get(gate_id, "No dependency note mapped."),
            }
        )
    return pd.DataFrame(rows).sort_values(["priority_rank", "gate_id"], kind="mergesort")


def build_hardening_queue(
    blockers: pd.DataFrame,
    strategy_summary: pd.DataFrame,
    backlog: pd.DataFrame,
    deliverables: pd.DataFrame,
) -> pd.DataFrame:
    support_map = dict(zip(strategy_summary["strategy_id"], strategy_summary["support_level"]))
    role_map = dict(zip(strategy_summary["strategy_id"], strategy_summary["role"]))
    backlog_focus = (
        backlog.groupby("work_package_id", sort=True)
        .agg(
            backlog_items=("deliverable", "count"),
            backlog_deliverables=("deliverable", lambda values: "; ".join(sorted(map(str, values))[:8])),
        )
        .reset_index()
    )
    backlog_map = backlog_focus.set_index("work_package_id").to_dict("index")
    acceptance_grade_by_wp = (
        deliverables.groupby("work_package_id", sort=True)["acceptance_grade"]
        .agg(lambda values: int(values.sum()))
        .to_dict()
    )

    rows = []
    for row in blockers.itertuples(index=False):
        gate_id = str(row.gate_id)
        wp_focus = GATE_WORK_PACKAGE.get(gate_id, "unmapped")
        primary_wp = wp_focus.split("/")[0]
        backlog_info = backlog_map.get(primary_wp, {"backlog_items": 0, "backlog_deliverables": ""})
        evidence_paths = [part.strip() for part in str(row.evidence_source).split(";") if part.strip()]
        support_level = support_map.get(row.strategy_id, "unknown")
        support_penalty = 1 if support_level == "runnable_proxy" else 2 if support_level == "partial_missing_required_features" else 3
        priority_rank = GATE_PRIORITY.get(gate_id, 99)
        rows.append(
            {
                "queue_rank": 0,
                "priority_band": f"P{priority_rank}",
                "gate_id": gate_id,
                "gate_name": row.gate_name,
                "strategy_id": row.strategy_id,
                "strategy_support_level": support_level,
                "strategy_role": role_map.get(row.strategy_id, "unknown"),
                "work_package_focus": wp_focus,
                "primary_work_package": primary_wp,
                "acceptance_milestone": ACCEPTANCE_MILESTONE.get(gate_id, "unmapped"),
                "blocker_category": row.blocker_category,
                "missing_requirement": row.missing_requirement,
                "next_required_evidence": row.next_required_evidence,
                "current_evidence_sources": row.evidence_source,
                "current_evidence_source_count": len(evidence_paths),
                "current_evidence_source_status": row.evidence_source_status,
                "primary_wp_backlog_items": int(backlog_info["backlog_items"]),
                "primary_wp_proxy_deliverables": backlog_info["backlog_deliverables"],
                "primary_wp_acceptance_grade_deliverables": int(acceptance_grade_by_wp.get(primary_wp, 0)),
                "dependency_note": DEPENDENCY_NOTE.get(gate_id, "No dependency note mapped."),
                "acceptance_ready_now": False,
                "priority_sort_key": priority_rank * 100 + support_penalty,
            }
        )
    frame = pd.DataFrame(rows).sort_values(
        ["priority_sort_key", "gate_id", "strategy_id"],
        kind="mergesort",
    )
    frame["queue_rank"] = range(1, len(frame) + 1)
    return frame.drop(columns=["priority_sort_key"])


def build_strategy_queue_summary(queue: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        queue.groupby("strategy_id", sort=True)
        .agg(
            queue_items=("queue_rank", "count"),
            top_queue_rank=("queue_rank", "min"),
            blocked_gates=("gate_id", lambda values: "; ".join(sorted(set(map(str, values))))),
            first_priority_band=("priority_band", "first"),
            support_level=("strategy_support_level", "first"),
            acceptance_milestones=("acceptance_milestone", lambda values: "; ".join(sorted(set(map(str, values))))),
        )
        .reset_index()
    )
    return grouped.sort_values(["top_queue_rank", "strategy_id"], kind="mergesort")


def write_report(output_dir: Path, queue: pd.DataFrame, gate_summary: pd.DataFrame, strategy_summary: pd.DataFrame) -> None:
    priority_summary = queue.groupby(["priority_band", "gate_id", "acceptance_milestone"], sort=True).size().reset_index(name="queue_items")
    lines = [
        "# Phase 20 Acceptance Hardening Queue",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This queue converts the current Phase 15 blockers and Phase 17 proxy backlog into executable acceptance-hardening work items.",
        "It is not a promotion result. Every row remains non-acceptance-ready until the required evidence is produced and Phase 15 gates pass.",
        "",
        "## Priority Summary",
        "",
        _markdown_table(priority_summary),
        "",
        "## Gate Summary",
        "",
        _markdown_table(gate_summary),
        "",
        "## Strategy Queue Summary",
        "",
        _markdown_table(strategy_summary),
        "",
        "## Top Queue Items",
        "",
        _markdown_table(queue.head(25)),
        "",
    ]
    (output_dir / "phase20_acceptance_hardening_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase20(paths: dict[str, Path], output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    inputs = load_inputs(paths)
    gate_summary = build_gate_summary(inputs["acceptance_blockers"])
    queue = build_hardening_queue(
        inputs["acceptance_blockers"],
        inputs["strategy_acceptance_summary"],
        inputs["implementation_gap_backlog"],
        inputs["deliverable_traceability"],
    )
    strategy_queue = build_strategy_queue_summary(queue)

    queue.to_csv(output_dir / "acceptance_hardening_queue.csv", index=False)
    gate_summary.to_csv(output_dir / "acceptance_hardening_gate_summary.csv", index=False)
    strategy_queue.to_csv(output_dir / "acceptance_hardening_strategy_summary.csv", index=False)
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "queue_rows": int(len(queue)),
        "gate_summary_rows": int(len(gate_summary)),
        "strategy_summary_rows": int(len(strategy_queue)),
        "acceptance_ready_queue_rows": int(queue["acceptance_ready_now"].sum()),
        "top_priority_gate": gate_summary.iloc[0]["gate_id"] if len(gate_summary) else "",
        "scope": "phase20_acceptance_hardening_queue",
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase20",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={
                "gate_priority": GATE_PRIORITY,
                "gate_work_package": GATE_WORK_PACKAGE,
                "acceptance_milestones": ACCEPTANCE_MILESTONE,
            },
            outputs={
                "acceptance_hardening_queue": str(output_dir / "acceptance_hardening_queue.csv"),
                "acceptance_hardening_gate_summary": str(output_dir / "acceptance_hardening_gate_summary.csv"),
                "acceptance_hardening_strategy_summary": str(output_dir / "acceptance_hardening_strategy_summary.csv"),
                "report": str(output_dir / "phase20_acceptance_hardening_report.md"),
            },
            random_seed="not_applicable_deterministic_blocker_queue",
            scenario_ids="phase15_blockers_by_strategy_gate",
            cost_model_version="outputs/phase12/cost_schedule.csv_and_zerodha_order_formula_v2_or_not_applicable",
            latency_model_version="outputs/phase12/execution_profiles.csv_or_not_applicable",
            base_dir=base_dir,
        )
    )
    (output_dir / "acceptance_hardening_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, queue, gate_summary, strategy_queue)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 20 acceptance-hardening queue artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase20"))
    parser.add_argument("--acceptance-blockers", type=Path, default=Path("outputs/phase15/acceptance_blockers.csv"))
    parser.add_argument("--strategy-acceptance-summary", type=Path, default=Path("outputs/phase15/strategy_acceptance_summary.csv"))
    parser.add_argument("--implementation-gap-backlog", type=Path, default=Path("outputs/phase17/implementation_gap_backlog.csv"))
    parser.add_argument("--deliverable-traceability", type=Path, default=Path("outputs/phase17/deliverable_traceability.csv"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "acceptance_blockers": args.acceptance_blockers,
        "strategy_acceptance_summary": args.strategy_acceptance_summary,
        "implementation_gap_backlog": args.implementation_gap_backlog,
        "deliverable_traceability": args.deliverable_traceability,
    }
    run_phase20(paths, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
