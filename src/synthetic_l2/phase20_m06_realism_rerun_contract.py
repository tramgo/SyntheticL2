from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


REALISM_RERUN_ACCEPTANCE_CRITERIA = [
    ("synthetic_quality_gate_clear", "Synthetic quality gates remain green on the accepted generator version.", "no fail rows and no unresolved warning rows"),
    ("holdout_generator_coverage", "Predeclared holdout generator profiles are structurally available.", "holdout profiles cover required quarter/feed scenarios"),
    ("feed_imperfection_coverage", "Disconnect/stressed feed imperfections are present and used in reruns.", "feed-imperfection profiles are rerun through full lifecycle execution"),
    ("holdout_strategy_rerun", "Candidate strategies are rerun on holdout-generator profiles.", "strategy P&L/signal/risk reruns exist on Q-B/Q-C holdout profiles"),
    ("pessimistic_execution_realism", "Holdout reruns include stressed retail, partial-fill and pessimistic execution assumptions.", "pessimistic execution rerun passes or blocks promotion"),
    ("artifact_exploitation_rejection", "Artifact/control reruns reject generator-specific edge.", "negative controls show edge does not depend on synthetic artifacts"),
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
            for criterion_id, description, threshold in REALISM_RERUN_ACCEPTANCE_CRITERIA
        ]
    )


def _status(row: pd.Series) -> str:
    support = str(row.get("strategy_support_level", ""))
    requirement = str(row.get("hardening_requirement", ""))
    if support == "not_supported_by_current_product":
        return "blocked_by_unsupported_strategy_scope"
    if support == "partial_missing_required_features":
        return "blocked_by_partial_strategy_support"
    if requirement in {"holdout_generator_strategy_rerun", "holdout_strategy_rerun"}:
        return "holdout_strategy_rerun_missing_acceptance_evidence"
    if requirement == "synthetic_quality_gate_clear":
        return "quality_gates_proxy_clear_not_strategy_rerun"
    if requirement == "holdout_generator_coverage":
        return "holdout_generator_proxy_available_not_acceptance_rerun"
    if requirement == "feed_imperfection_coverage":
        return "feed_imperfection_proxy_available_not_acceptance_rerun"
    if requirement == "pessimistic_execution_realism":
        return "pessimistic_execution_realism_rerun_missing"
    if requirement == "artifact_exploitation_rejection":
        return "artifact_exploitation_control_missing"
    return "realism_rerun_requirement_open"


def _observed_metric(row: pd.Series) -> str:
    requirement = str(row.get("hardening_requirement", ""))
    if requirement == "synthetic_quality_gate_clear":
        return f"quality_pass_rows={row.get('quality_pass_rows', '')}; quality_warn_rows={row.get('quality_warn_rows', '')}; quality_fail_rows={row.get('quality_fail_rows', '')}; warning_triage_rows={row.get('warning_triage_rows', '')}"
    if requirement in {"holdout_generator_coverage", "holdout_generator_strategy_rerun", "holdout_strategy_rerun"}:
        return f"holdout_profiles={row.get('holdout_profiles', '')}; structural_ready_profiles={row.get('structural_ready_profiles', '')}; holdout_status={row.get('holdout_status', '')}; acceptance_eligible_profiles={row.get('holdout_acceptance_eligible_profiles', '')}"
    if requirement == "feed_imperfection_coverage":
        return f"feed_profiles={row.get('feed_profiles', '')}; disconnect_profiles={row.get('disconnect_profiles', '')}; stressed_profile_positive={row.get('stressed_profile_positive', '')}"
    if requirement == "pessimistic_execution_realism":
        return f"stressed_profile_positive={row.get('stressed_profile_positive', '')}; all_profiles_positive={row.get('all_profiles_positive', '')}; profile_robustness_status={row.get('profile_robustness_status', '')}"
    if requirement == "artifact_exploitation_rejection":
        return f"interpretable_negative_control_rows={row.get('interpretable_negative_control_rows', '')}; passed_negative_control_rows={row.get('passed_negative_control_rows', '')}"
    return str(row.get("observed_value", ""))


def build_realism_rerun_ledger(
    execution_roadmap: pd.DataFrame,
    quality: pd.DataFrame,
    warning_triage: pd.DataFrame,
    holdout: pd.DataFrame,
    matrix: pd.DataFrame,
    robustness: pd.DataFrame,
    profile_robustness: pd.DataFrame,
    support: pd.DataFrame,
) -> pd.DataFrame:
    m06 = execution_roadmap[
        execution_roadmap["execution_milestone"].astype(str) == "M06_holdout_generator_and_realism_reruns"
    ].copy()

    quality_summary = pd.DataFrame(
        [
            {
                "quality_pass_rows": int((quality["status"].astype(str) == "pass").sum()),
                "quality_warn_rows": int((quality["status"].astype(str) == "warn").sum()),
                "quality_fail_rows": int((quality["status"].astype(str) == "fail").sum()),
                "warning_triage_rows": int(len(warning_triage)),
            }
        ]
    )
    holdout_summary = pd.DataFrame(
        [
            {
                "holdout_profiles": int(len(holdout)),
                "structural_ready_profiles": int(holdout["structural_ready_for_holdout_proxy"].astype(bool).sum()),
                "holdout_acceptance_eligible_profiles": int(holdout["acceptance_eligible_now"].astype(bool).sum()),
                "feed_profiles": int(holdout["feed_profile"].nunique()),
                "disconnect_profiles": int(holdout["feed_profile"].astype(str).str.contains("disconnect|stress", case=False, regex=True).sum()),
            }
        ]
    )
    matrix_cols = ["strategy_id", "name", "support_level", "missing_features", "required_scenarios", "caveat"]
    robust_cols = [
        "strategy_id",
        "holdout_generator_profiles_available",
        "holdout_generator_profiles_present_in_proxy",
        "holdout_status",
        "real_data_rerun_status",
        "dimension_status",
    ]
    profile_cols = [
        "strategy_id",
        "all_profiles_positive",
        "stressed_profile_positive",
        "interpretable_negative_control_rows",
        "passed_negative_control_rows",
        "profile_robustness_status",
    ]
    rows = (
        m06.merge(matrix[[c for c in matrix_cols if c in matrix]], on="strategy_id", how="left")
        .merge(robustness[[c for c in robust_cols if c in robustness]], on="strategy_id", how="left")
        .merge(profile_robustness[[c for c in profile_cols if c in profile_robustness]], on="strategy_id", how="left")
        .merge(support[["strategy_id", "strategy_support_closure_status", "required_support_action"]], on="strategy_id", how="left")
    )
    for column, value in quality_summary.iloc[0].to_dict().items():
        rows[column] = value
    for column, value in holdout_summary.iloc[0].to_dict().items():
        rows[column] = value
    rows["realism_rerun_status"] = rows.apply(_status, axis=1)
    rows["observed_realism_metric"] = rows.apply(_observed_metric, axis=1)
    rows["holdout_rerun_required"] = rows["hardening_requirement"].astype(str).isin(
        {"holdout_generator_strategy_rerun", "holdout_strategy_rerun"}
    )
    rows["quality_gate_required"] = rows["hardening_requirement"].astype(str).eq("synthetic_quality_gate_clear")
    rows["feed_imperfection_required"] = rows["hardening_requirement"].astype(str).eq("feed_imperfection_coverage")
    rows["pessimistic_execution_required"] = rows["hardening_requirement"].astype(str).eq("pessimistic_execution_realism")
    rows["artifact_control_required"] = rows["hardening_requirement"].astype(str).eq("artifact_exploitation_rejection")
    rows["acceptance_requirement_met_after_contract"] = False
    rows["blocking_gap_after_contract"] = rows.apply(
        lambda row: (
            f"Support closure required first: {row.get('required_support_action', '')}"
            if str(row.get("strategy_support_closure_status", "")).startswith("requires_")
            else "Holdout/realism evidence remains structural or proxy-only; strategy reruns with full lifecycle execution are still required."
        ),
        axis=1,
    )
    rows["required_realism_action"] = rows.apply(
        lambda row: (
            "Run strategy on holdout-generator profiles and compare against development/calibration results with leakage checks."
            if row["holdout_rerun_required"]
            else "Keep synthetic quality gates green on the accepted generator and rerun strategy realism checks."
            if row["quality_gate_required"]
            else "Rerun strategies on feed-imperfection profiles with full lifecycle execution."
            if row["feed_imperfection_required"]
            else "Evaluate holdout strategies under stressed retail, partial-fill and pessimistic execution assumptions."
            if row["pessimistic_execution_required"]
            else "Run artifact/control templates and reject generator-artifact dependent edge."
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
        "realism_rerun_status",
        "observed_realism_metric",
        "quality_pass_rows",
        "quality_warn_rows",
        "quality_fail_rows",
        "holdout_profiles",
        "structural_ready_profiles",
        "holdout_acceptance_eligible_profiles",
        "feed_profiles",
        "disconnect_profiles",
        "holdout_generator_profiles_available",
        "holdout_generator_profiles_present_in_proxy",
        "holdout_status",
        "stressed_profile_positive",
        "all_profiles_positive",
        "interpretable_negative_control_rows",
        "passed_negative_control_rows",
        "holdout_rerun_required",
        "quality_gate_required",
        "feed_imperfection_required",
        "pessimistic_execution_required",
        "artifact_control_required",
        "acceptance_requirement_met_after_contract",
        "blocking_gap_after_contract",
        "required_realism_action",
        "required_next_evidence",
    ]
    for column in columns:
        if column not in rows:
            rows[column] = False if column.endswith("_required") else ""
    return rows[columns].sort_values("execution_rank", kind="mergesort")


def build_gap_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    return (
        ledger.groupby("realism_rerun_status", sort=True)
        .agg(rows=("hardening_requirement", "size"), strategies=("strategy_id", "nunique"), acceptance_met_rows=("acceptance_requirement_met_after_contract", "sum"))
        .reset_index()
        .sort_values(["rows", "realism_rerun_status"], ascending=[False, True], kind="mergesort")
    )


def build_strategy_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    grouped = ledger.groupby(["strategy_id", "strategy_support_level", "strategy_role"], sort=True).agg(
        m06_rows=("hardening_requirement", "size"),
        holdout_rerun_rows=("holdout_rerun_required", "sum"),
        quality_gate_rows=("quality_gate_required", "sum"),
        feed_imperfection_rows=("feed_imperfection_required", "sum"),
        pessimistic_execution_rows=("pessimistic_execution_required", "sum"),
        artifact_control_rows=("artifact_control_required", "sum"),
        acceptance_met_rows=("acceptance_requirement_met_after_contract", "sum"),
        first_required_action=("required_realism_action", "first"),
    ).reset_index()
    grouped["realism_rerun_contract_status"] = "proxy_or_support_blocked_not_acceptance"
    return grouped


def write_report(output_dir: Path, criteria: pd.DataFrame, ledger: pd.DataFrame, gap_summary: pd.DataFrame, strategy_summary: pd.DataFrame) -> None:
    lines = [
        "# Phase 20 M06 Holdout Generator and Realism Rerun Contract",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase converts the sixth Phase 20 execution milestone into a holdout-generator and realism rerun contract.",
        "It joins current Phase 14 quality/holdout realism diagnostics and Phase 13 robustness proxy evidence to the M06 roadmap while keeping every row non-acceptance-ready until strategy reruns exist.",
        "",
        "## Acceptance Criteria Contract",
        "",
        _markdown_table(criteria),
        "",
        "## Realism Rerun Gap Summary",
        "",
        _markdown_table(gap_summary),
        "",
        "## Strategy Summary",
        "",
        _markdown_table(strategy_summary),
        "",
        "## M06 Realism Rerun Ledger",
        "",
        _markdown_table(ledger),
        "",
    ]
    (output_dir / "phase20_m06_realism_rerun_contract_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase20_m06(paths: dict[str, Path], output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    criteria = build_acceptance_criteria()
    ledger = build_realism_rerun_ledger(
        pd.read_csv(paths["execution_roadmap"]),
        pd.read_csv(paths["quality_gate_summary"]),
        pd.read_csv(paths["quality_warning_triage"]),
        pd.read_csv(paths["holdout_generator_realism_summary"]),
        pd.read_csv(paths["strategy_validation_matrix"]),
        pd.read_csv(paths["robustness_dimension_summary"]),
        pd.read_csv(paths["experiment_profile_robustness_summary"]),
        pd.read_csv(paths["strategy_support_decision_summary"]),
    )
    gap_summary = build_gap_summary(ledger)
    strategy_summary = build_strategy_summary(ledger)
    criteria.to_csv(output_dir / "realism_rerun_acceptance_criteria.csv", index=False)
    ledger.to_csv(output_dir / "realism_rerun_ledger.csv", index=False)
    gap_summary.to_csv(output_dir / "realism_rerun_gap_summary.csv", index=False)
    strategy_summary.to_csv(output_dir / "realism_rerun_strategy_summary.csv", index=False)
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "realism_rerun_acceptance_criteria_rows": int(len(criteria)),
        "realism_rerun_rows": int(len(ledger)),
        "realism_rerun_gap_summary_rows": int(len(gap_summary)),
        "realism_rerun_strategy_rows": int(len(strategy_summary)),
        "holdout_rerun_required_rows": int(ledger["holdout_rerun_required"].astype(bool).sum()),
        "quality_gate_required_rows": int(ledger["quality_gate_required"].astype(bool).sum()),
        "feed_imperfection_required_rows": int(ledger["feed_imperfection_required"].astype(bool).sum()),
        "pessimistic_execution_required_rows": int(ledger["pessimistic_execution_required"].astype(bool).sum()),
        "artifact_control_required_rows": int(ledger["artifact_control_required"].astype(bool).sum()),
        "acceptance_met_after_contract_rows": int(ledger["acceptance_requirement_met_after_contract"].astype(bool).sum()),
        "scope": "phase20_m06_realism_rerun_contract_not_acceptance",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase20_m06",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={"realism_rerun_acceptance_criteria": REALISM_RERUN_ACCEPTANCE_CRITERIA},
            outputs={
                "realism_rerun_acceptance_criteria": str(output_dir / "realism_rerun_acceptance_criteria.csv"),
                "realism_rerun_ledger": str(output_dir / "realism_rerun_ledger.csv"),
                "realism_rerun_gap_summary": str(output_dir / "realism_rerun_gap_summary.csv"),
                "realism_rerun_strategy_summary": str(output_dir / "realism_rerun_strategy_summary.csv"),
                "report": str(output_dir / "phase20_m06_realism_rerun_contract_report.md"),
                "manifest": str(output_dir / "realism_rerun_contract_manifest.json"),
            },
            random_seed="not_applicable_deterministic_realism_rerun_contract",
            scenario_ids="phase20_M06_holdout_generator_and_realism_reruns_rows",
            cost_model_version="not_applicable_no_new_execution_costs",
            latency_model_version="phase14_feed_profiles_proxy_not_acceptance_rerun",
            base_dir=base_dir,
        )
    )
    (output_dir / "realism_rerun_contract_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, criteria, ledger, gap_summary, strategy_summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 20 M06 holdout-generator and realism rerun contract artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase20_m06"))
    parser.add_argument("--execution-roadmap", type=Path, default=Path("outputs/phase20/acceptance_execution_roadmap.csv"))
    parser.add_argument("--quality-gate-summary", type=Path, default=Path("outputs/phase14/quality_gate_summary.csv"))
    parser.add_argument("--quality-warning-triage", type=Path, default=Path("outputs/phase14/quality_warning_triage.csv"))
    parser.add_argument("--holdout-generator-realism-summary", type=Path, default=Path("outputs/phase14/holdout_generator_realism_summary.csv"))
    parser.add_argument("--strategy-validation-matrix", type=Path, default=Path("outputs/phase11/strategy_validation_matrix.csv"))
    parser.add_argument("--robustness-dimension-summary", type=Path, default=Path("outputs/phase13/robustness_dimension_summary.csv"))
    parser.add_argument("--experiment-profile-robustness-summary", type=Path, default=Path("outputs/phase13/experiment_profile_robustness_summary.csv"))
    parser.add_argument("--strategy-support-decision-summary", type=Path, default=Path("outputs/phase20_m02/strategy_support_decision_summary.csv"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "execution_roadmap": args.execution_roadmap,
        "quality_gate_summary": args.quality_gate_summary,
        "quality_warning_triage": args.quality_warning_triage,
        "holdout_generator_realism_summary": args.holdout_generator_realism_summary,
        "strategy_validation_matrix": args.strategy_validation_matrix,
        "robustness_dimension_summary": args.robustness_dimension_summary,
        "experiment_profile_robustness_summary": args.experiment_profile_robustness_summary,
        "strategy_support_decision_summary": args.strategy_support_decision_summary,
    }
    run_phase20_m06(paths, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
