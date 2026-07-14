from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


ROBUSTNESS_EXECUTION_ACCEPTANCE_CRITERIA = [
    (
        "full_validation_seed_coverage",
        "Every candidate strategy is executed across the full registered Phase 13 validation seed plan.",
        "executed_seed_count equals required_full_validation_seeds and no seed is reused for threshold tuning",
    ),
    (
        "walk_forward_execution",
        "All predeclared train/test walk-forward windows are executed with leakage checks preserved.",
        "walk_forward_windows_run equals walk_forward_windows_planned and train/test boundaries are unchanged",
    ),
    (
        "parameter_neighborhood_smoothness",
        "The predeclared parameter neighborhood is run and summarized without selecting on final-test results.",
        "parameter_sets_run equals parameter_sets_planned and neighborhood performance is not single-point fragile",
    ),
    (
        "execution_profile_robustness",
        "Candidate strategies remain positive across deployable and stressed execution profiles using acceptance-grade fills and costs.",
        "all deployable/stressed execution profiles pass after broker/cost reconciliation prerequisites are met",
    ),
    (
        "negative_control_rejection",
        "Mandatory negative controls degrade or fail under the same full execution harness.",
        "all interpretable mandatory negative controls reject/degrade versus BASE",
    ),
]


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    text = frame.copy()
    for column in text.columns:
        text[column] = text[column].map(lambda value: "" if pd.isna(value) else str(value))
    headers = [str(column) for column in text.columns]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |" for row in text.values.tolist())
    return "\n".join(lines)


def build_acceptance_criteria() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "criterion_id": criterion_id,
                "criterion_description": description,
                "acceptance_threshold": threshold,
                "current_status": "contract_defined_not_acceptance_evidence",
            }
            for criterion_id, description, threshold in ROBUSTNESS_EXECUTION_ACCEPTANCE_CRITERIA
        ]
    )


def _robustness_status(row: pd.Series) -> str:
    support = str(row.get("strategy_support_level", ""))
    requirement = str(row.get("hardening_requirement", ""))
    if support == "not_supported_by_current_product":
        return "blocked_by_unsupported_strategy_scope"
    if support == "partial_missing_required_features":
        return "blocked_by_partial_strategy_support"
    if requirement == "full_validation_seed_coverage":
        return "proxy_initial_seed_only_full_seed_execution_missing"
    if requirement == "walk_forward_coverage":
        return "walk_forward_design_available_not_executed"
    if requirement == "parameter_neighborhood_smoothness":
        return "single_parameter_proxy_parameter_grid_missing"
    if requirement == "execution_profile_robustness":
        return "execution_profile_proxy_not_acceptance_grade"
    if requirement == "negative_control_rejection":
        return "negative_control_proxy_incomplete_or_not_acceptance_grade"
    if requirement == "multi_seed_walk_forward_validation":
        return "predictive_multiseed_walk_forward_required_before_robustness_acceptance"
    return "robustness_execution_requirement_open"


def _observed_metric_for(row: pd.Series) -> str:
    requirement = str(row.get("hardening_requirement", ""))
    if requirement == "full_validation_seed_coverage":
        return (
            f"initial_engineering_seeds_run={row.get('initial_engineering_seeds_run', '')}; "
            f"required_full_validation_seeds={row.get('required_full_validation_seeds', '')}; "
            f"seed_scope_status={row.get('seed_scope_status', '')}"
        )
    if requirement == "walk_forward_coverage":
        return (
            f"walk_forward_windows_run={row.get('walk_forward_windows_run', '')}; "
            f"walk_forward_windows_planned={row.get('walk_forward_windows_planned', '')}; "
            f"walk_forward_status={row.get('walk_forward_status', '')}"
        )
    if requirement == "parameter_neighborhood_smoothness":
        return (
            f"parameter_sets_run={row.get('parameter_sets_run', '')}; "
            f"parameter_sets_planned={row.get('parameter_sets_planned', '')}; "
            f"parameter_smoothness_status={row.get('parameter_smoothness_status', '')}"
        )
    if requirement == "execution_profile_robustness":
        return (
            f"execution_profiles_evaluated={row.get('execution_profiles_evaluated', '')}; "
            f"all_profiles_positive={row.get('all_profiles_positive', row.get('all_execution_profiles_positive', ''))}; "
            f"stressed_profile_positive={row.get('stressed_profile_positive', '')}; "
            f"worst_profile_base_net_return={row.get('worst_profile_base_net_return', '')}"
        )
    if requirement == "negative_control_rejection":
        return (
            f"interpretable_negative_control_rows={row.get('interpretable_negative_control_rows', '')}; "
            f"passed_negative_control_rows={row.get('passed_negative_control_rows', '')}; "
            f"negative_control_rows={row.get('negative_control_rows', '')}"
        )
    if requirement == "multi_seed_walk_forward_validation":
        return "predictive M04 row requires full registered multi-seed walk-forward model execution; current evidence is proxy-only"
    return str(row.get("observed_value", ""))


def build_robustness_execution_ledger(
    execution_roadmap: pd.DataFrame,
    robustness_dimension: pd.DataFrame,
    profile_robustness: pd.DataFrame,
    run_summary: pd.DataFrame,
    support_decisions: pd.DataFrame,
) -> pd.DataFrame:
    m04 = execution_roadmap[
        execution_roadmap["execution_milestone"].astype(str) == "M04_full_seed_walk_forward_and_robustness_execution"
    ].copy()
    support_cols = [
        "strategy_id",
        "strategy_support_closure_status",
        "required_support_action",
    ]
    rows = (
        m04.merge(robustness_dimension, on="strategy_id", how="left", suffixes=("", "_dimension"))
        .merge(profile_robustness, on="strategy_id", how="left", suffixes=("", "_profile"))
        .merge(run_summary, on="strategy_id", how="left", suffixes=("", "_smoke"))
        .merge(support_decisions[[c for c in support_cols if c in support_decisions]], on="strategy_id", how="left")
    )
    rows["robustness_execution_status"] = rows.apply(_robustness_status, axis=1)
    rows["observed_robustness_metric"] = rows.apply(_observed_metric_for, axis=1)
    rows["full_seed_execution_required"] = rows["hardening_requirement"].astype(str).isin(
        {"full_validation_seed_coverage", "multi_seed_walk_forward_validation"}
    )
    rows["walk_forward_execution_required"] = rows["hardening_requirement"].astype(str).isin(
        {"walk_forward_coverage", "multi_seed_walk_forward_validation"}
    )
    rows["parameter_smoothness_required"] = rows["hardening_requirement"].astype(str).eq("parameter_neighborhood_smoothness")
    rows["execution_profile_required"] = rows["hardening_requirement"].astype(str).eq("execution_profile_robustness")
    rows["negative_control_required"] = rows["hardening_requirement"].astype(str).eq("negative_control_rejection")
    rows["acceptance_requirement_met_after_contract"] = False
    rows["blocking_gap_after_contract"] = rows.apply(
        lambda row: (
            f"Support closure required first: {row.get('required_support_action', '')}"
            if str(row.get("strategy_support_closure_status", "")).startswith("requires_")
            else "Robustness evidence remains proxy-only, incomplete or execution-profile failing; full registered acceptance execution is still required."
        ),
        axis=1,
    )
    rows["required_robustness_action"] = rows.apply(
        lambda row: (
            "Execute the full Phase 13 required seed plan and preserve seed-level result lineage."
            if row["full_seed_execution_required"] and not row["walk_forward_execution_required"]
            else "Execute the registered multi-seed walk-forward windows without train/test leakage or threshold reuse."
            if row["walk_forward_execution_required"]
            else "Run the full predeclared parameter grid and report neighborhood smoothness."
            if row["parameter_smoothness_required"]
            else "Rerun all deployable and stressed execution profiles with acceptance-grade fill/cost evidence."
            if row["execution_profile_required"]
            else "Run mandatory negative controls under the same acceptance harness and require rejection/degradation."
        ),
        axis=1,
    )
    columns = [
        "execution_rank",
        "gate_id",
        "strategy_id",
        "strategy_support_level",
        "strategy_role",
        "hardening_requirement",
        "action_class",
        "dependency_status",
        "strategy_support_closure_status",
        "robustness_execution_status",
        "observed_robustness_metric",
        "registered_for_phase13_proxy",
        "initial_engineering_seeds_run",
        "required_full_validation_seeds",
        "walk_forward_windows_run",
        "walk_forward_windows_planned",
        "parameter_sets_run",
        "parameter_sets_planned",
        "execution_profiles_evaluated",
        "all_execution_profiles_positive",
        "stressed_profile_positive",
        "interpretable_negative_control_rows",
        "passed_negative_control_rows",
        "full_seed_execution_required",
        "walk_forward_execution_required",
        "parameter_smoothness_required",
        "execution_profile_required",
        "negative_control_required",
        "acceptance_requirement_met_after_contract",
        "blocking_gap_after_contract",
        "required_robustness_action",
        "required_next_evidence",
    ]
    for column in columns:
        if column not in rows:
            rows[column] = False if column.endswith("_required") or column.startswith("all_") or column.startswith("stressed_") else ""
    return rows[columns].sort_values(["execution_rank"], kind="mergesort")


def build_gap_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    if ledger.empty:
        return pd.DataFrame()
    return (
        ledger.groupby(["robustness_execution_status"], sort=True)
        .agg(
            rows=("hardening_requirement", "size"),
            strategies=("strategy_id", "nunique"),
            acceptance_met_rows=("acceptance_requirement_met_after_contract", "sum"),
        )
        .reset_index()
        .sort_values(["rows", "robustness_execution_status"], ascending=[False, True], kind="mergesort")
    )


def build_strategy_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    if ledger.empty:
        return pd.DataFrame()
    grouped = (
        ledger.groupby(["strategy_id", "strategy_support_level", "strategy_role"], sort=True)
        .agg(
            m04_rows=("hardening_requirement", "size"),
            distinct_statuses=("robustness_execution_status", "nunique"),
            acceptance_met_rows=("acceptance_requirement_met_after_contract", "sum"),
            seed_rows_requiring_execution=("full_seed_execution_required", "sum"),
            walk_forward_rows_requiring_execution=("walk_forward_execution_required", "sum"),
            parameter_rows_requiring_smoothness=("parameter_smoothness_required", "sum"),
            profile_rows_requiring_execution=("execution_profile_required", "sum"),
            negative_control_rows_requiring_execution=("negative_control_required", "sum"),
            first_required_action=("required_robustness_action", "first"),
        )
        .reset_index()
    )
    grouped["robustness_execution_contract_status"] = "proxy_or_support_blocked_not_acceptance"
    return grouped.sort_values(["robustness_execution_contract_status", "strategy_id"], kind="mergesort")


def write_report(
    output_dir: Path,
    criteria: pd.DataFrame,
    ledger: pd.DataFrame,
    gap_summary: pd.DataFrame,
    strategy_summary: pd.DataFrame,
) -> None:
    lines = [
        "# Phase 20 M04 Robustness Execution Contract",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase converts the fourth Phase 20 execution milestone into a full seed, walk-forward, parameter-neighborhood, execution-profile and negative-control robustness execution contract.",
        "It joins current Phase 13 proxy robustness artifacts to the M04 roadmap and keeps every row non-acceptance-ready until the full registered execution harness is run.",
        "",
        "## Acceptance Criteria Contract",
        "",
        _markdown_table(criteria),
        "",
        "## Robustness Execution Gap Summary",
        "",
        _markdown_table(gap_summary),
        "",
        "## Strategy Summary",
        "",
        _markdown_table(strategy_summary),
        "",
        "## M04 Robustness Execution Ledger",
        "",
        _markdown_table(ledger),
        "",
    ]
    (output_dir / "phase20_m04_robustness_execution_contract_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase20_m04(paths: dict[str, Path], output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    execution_roadmap = pd.read_csv(paths["execution_roadmap"])
    robustness_dimension = pd.read_csv(paths["robustness_dimension_summary"])
    profile_robustness = pd.read_csv(paths["experiment_profile_robustness_summary"])
    run_summary = pd.read_csv(paths["experiment_run_summary"])
    support_decisions = pd.read_csv(paths["strategy_support_decision_summary"])

    criteria = build_acceptance_criteria()
    ledger = build_robustness_execution_ledger(
        execution_roadmap,
        robustness_dimension,
        profile_robustness,
        run_summary,
        support_decisions,
    )
    gap_summary = build_gap_summary(ledger)
    strategy_summary = build_strategy_summary(ledger)

    criteria.to_csv(output_dir / "robustness_execution_acceptance_criteria.csv", index=False)
    ledger.to_csv(output_dir / "robustness_execution_ledger.csv", index=False)
    gap_summary.to_csv(output_dir / "robustness_execution_gap_summary.csv", index=False)
    strategy_summary.to_csv(output_dir / "robustness_execution_strategy_summary.csv", index=False)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "robustness_execution_acceptance_criteria_rows": int(len(criteria)),
        "robustness_execution_rows": int(len(ledger)),
        "robustness_execution_gap_summary_rows": int(len(gap_summary)),
        "robustness_execution_strategy_rows": int(len(strategy_summary)),
        "full_seed_execution_required_rows": int(ledger["full_seed_execution_required"].astype(bool).sum()),
        "walk_forward_execution_required_rows": int(ledger["walk_forward_execution_required"].astype(bool).sum()),
        "parameter_smoothness_required_rows": int(ledger["parameter_smoothness_required"].astype(bool).sum()),
        "execution_profile_required_rows": int(ledger["execution_profile_required"].astype(bool).sum()),
        "negative_control_required_rows": int(ledger["negative_control_required"].astype(bool).sum()),
        "acceptance_met_after_contract_rows": int(ledger["acceptance_requirement_met_after_contract"].astype(bool).sum()),
        "scope": "phase20_m04_robustness_execution_contract_not_acceptance",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase20_m04",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={"robustness_execution_acceptance_criteria": ROBUSTNESS_EXECUTION_ACCEPTANCE_CRITERIA},
            outputs={
                "robustness_execution_acceptance_criteria": str(output_dir / "robustness_execution_acceptance_criteria.csv"),
                "robustness_execution_ledger": str(output_dir / "robustness_execution_ledger.csv"),
                "robustness_execution_gap_summary": str(output_dir / "robustness_execution_gap_summary.csv"),
                "robustness_execution_strategy_summary": str(output_dir / "robustness_execution_strategy_summary.csv"),
                "report": str(output_dir / "phase20_m04_robustness_execution_contract_report.md"),
                "manifest": str(output_dir / "robustness_execution_contract_manifest.json"),
            },
            random_seed="phase13_seed_plan_required_not_executed_for_acceptance",
            scenario_ids="phase20_M04_full_seed_walk_forward_and_robustness_execution_rows",
            cost_model_version="phase12_execution_profiles_proxy_not_acceptance_grade",
            latency_model_version="phase12_execution_profiles_proxy_not_acceptance_grade",
            base_dir=base_dir,
        )
    )
    (output_dir / "robustness_execution_contract_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, criteria, ledger, gap_summary, strategy_summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 20 M04 robustness execution contract artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase20_m04"))
    parser.add_argument("--execution-roadmap", type=Path, default=Path("outputs/phase20/acceptance_execution_roadmap.csv"))
    parser.add_argument("--robustness-dimension-summary", type=Path, default=Path("outputs/phase13/robustness_dimension_summary.csv"))
    parser.add_argument("--experiment-profile-robustness-summary", type=Path, default=Path("outputs/phase13/experiment_profile_robustness_summary.csv"))
    parser.add_argument("--experiment-run-summary", type=Path, default=Path("outputs/phase13/experiment_run_summary.csv"))
    parser.add_argument("--strategy-support-decision-summary", type=Path, default=Path("outputs/phase20_m02/strategy_support_decision_summary.csv"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "execution_roadmap": args.execution_roadmap,
        "robustness_dimension_summary": args.robustness_dimension_summary,
        "experiment_profile_robustness_summary": args.experiment_profile_robustness_summary,
        "experiment_run_summary": args.experiment_run_summary,
        "strategy_support_decision_summary": args.strategy_support_decision_summary,
    }
    run_phase20_m04(paths, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
