from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


PREDICTIVE_ACCEPTANCE_CRITERIA = [
    (
        "calibrated_model_output",
        "Frozen calibrated probability models exist for each candidate strategy and are evaluated out of sample.",
        "model artifact/version present; Brier score and calibration curve computed out of sample",
    ),
    (
        "baseline_lift",
        "Directional and probabilistic metrics beat no-skill, majority-direction and Brier baselines.",
        "positive accuracy excess versus no-skill and majority baselines plus positive Brier skill",
    ),
    (
        "holdout_cell_stability",
        "Predeclared holdout cells beat local-majority baselines without threshold reuse.",
        "all minimum-row holdout cells pass",
    ),
    (
        "untouched_test_stability",
        "Untouched-test cells pass after development is frozen.",
        "all untouched-test cells beat local-majority baselines",
    ),
    (
        "feature_stability",
        "Feature importance or attribution is stable across registered seeds/folds.",
        "stable feature set and bounded importance volatility across seeds",
    ),
    (
        "promotion_falsification_clearance",
        "Joined predictive promotion-falsification checklist clears all blockers.",
        "predictive_promotion_candidate is true and falsification status is clear",
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
            for criterion_id, description, threshold in PREDICTIVE_ACCEPTANCE_CRITERIA
        ]
    )


def _requirement_status(row: pd.Series) -> str:
    requirement = str(row["hardening_requirement"])
    support = str(row.get("strategy_support_level", ""))
    if support == "not_supported_by_current_product":
        return "blocked_by_unsupported_strategy_scope"
    if support == "partial_missing_required_features":
        return "blocked_by_partial_strategy_support"
    if requirement == "calibrated_model_output":
        return "missing_calibrated_model_artifact"
    if requirement == "baseline_outperformance":
        return "proxy_baseline_failed"
    if requirement == "holdout_cell_stability":
        return "proxy_holdout_cells_failed"
    if requirement == "untouched_test_stability":
        return "untouched_test_proxy_failed_or_missing"
    if requirement == "feature_stability":
        return "proxy_feature_stability_available_not_model_importance"
    if requirement == "promotion_falsification_clear":
        return "predictive_promotion_falsified"
    return "predictive_requirement_open"


def _observed_metric_for(row: pd.Series) -> str:
    requirement = str(row["hardening_requirement"])
    if requirement == "baseline_outperformance":
        return (
            f"accuracy_excess_no_skill={row.get('directional_accuracy_excess_vs_no_skill', '')}; "
            f"accuracy_excess_majority={row.get('directional_accuracy_excess_vs_majority', '')}; "
            f"brier_skill={row.get('brier_skill_score_proxy', '')}; "
            f"baseline_pass={row.get('baseline_pass_proxy', '')}"
        )
    if requirement == "holdout_cell_stability":
        return (
            f"cell_beat_fraction={row.get('cell_beat_fraction', '')}; "
            f"cells_beating_local_majority={row.get('cells_beating_local_majority', '')}/{row.get('stability_cells', '')}; "
            f"worst_segment_status={row.get('worst_segment_status', '')}"
        )
    if requirement == "untouched_test_stability":
        return (
            f"untouched_cells_beating={row.get('untouched_test_cells_beating_local_majority', '')}/"
            f"{row.get('untouched_test_cells', '')}; untouched_pass={row.get('untouched_test_pass_proxy', '')}"
        )
    if requirement == "feature_stability":
        return (
            f"feature_stability_available={row.get('feature_stability_proxy_available', '')}; "
            f"stable_feature_count={row.get('stable_feature_count_proxy', '')}; "
            f"max_top3_frequency={row.get('max_feature_top3_frequency_proxy', '')}; "
            f"median_importance_cv={row.get('median_feature_importance_cv_proxy', '')}"
        )
    if requirement == "calibrated_model_output":
        return "no frozen calibrated probability model artifact is registered for this strategy"
    if requirement == "promotion_falsification_clear":
        return (
            f"promotion_candidate={row.get('predictive_promotion_candidate_proxy', '')}; "
            f"falsification_status={row.get('falsification_status', '')}"
        )
    return str(row.get("observed_value", ""))


def build_predictive_validation_ledger(
    execution_roadmap: pd.DataFrame,
    baseline: pd.DataFrame,
    holdout: pd.DataFrame,
    falsification: pd.DataFrame,
    support_decisions: pd.DataFrame,
) -> pd.DataFrame:
    m03 = execution_roadmap[
        execution_roadmap["execution_milestone"].astype(str) == "M03_predictive_model_and_baseline_validation"
    ].copy()
    rows = (
        m03.merge(baseline, on="strategy_id", how="left", suffixes=("", "_baseline"))
        .merge(holdout, on="strategy_id", how="left", suffixes=("", "_holdout"))
        .merge(falsification, on="strategy_id", how="left", suffixes=("", "_falsification"))
        .merge(
            support_decisions[
                [
                    "strategy_id",
                    "strategy_support_closure_status",
                    "required_support_action",
                ]
            ],
            on="strategy_id",
            how="left",
        )
    )
    rows["predictive_contract_status"] = rows.apply(_requirement_status, axis=1)
    rows["observed_predictive_metric"] = rows.apply(_observed_metric_for, axis=1)
    rows["calibrated_model_required"] = rows["hardening_requirement"].astype(str).eq("calibrated_model_output")
    rows["baseline_lift_required"] = rows["hardening_requirement"].astype(str).eq("baseline_outperformance")
    rows["holdout_or_untouched_required"] = rows["hardening_requirement"].astype(str).isin(
        {"holdout_cell_stability", "untouched_test_stability"}
    )
    rows["promotion_falsification_required"] = rows["hardening_requirement"].astype(str).eq("promotion_falsification_clear")
    rows["acceptance_requirement_met_after_contract"] = False
    rows["blocking_gap_after_contract"] = rows.apply(
        lambda row: (
            f"Support closure required first: {row.get('required_support_action', '')}"
            if str(row.get("strategy_support_closure_status", "")).startswith("requires_")
            else "Predictive evidence remains proxy-only or failing; calibrated out-of-sample model evidence is still required."
        ),
        axis=1,
    )
    rows["required_predictive_action"] = rows.apply(
        lambda row: (
            "Train and freeze calibrated probability model, then run out-of-sample Brier/calibration/baseline evaluation."
            if row["calibrated_model_required"]
            else "Rerun predictive validation and require positive lift over no-skill, local-majority and Brier baselines."
            if row["baseline_lift_required"]
            else "Run predeclared multi-seed holdout and untouched-test stability cells without reusing test thresholds."
            if row["holdout_or_untouched_required"]
            else "Replace proxy feature-target association with model attribution stability across registered seeds/folds."
            if str(row["hardening_requirement"]) == "feature_stability"
            else "Clear the joined promotion-falsification checklist only after support, baseline, holdout, feature-stability and real-holdout evidence pass."
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
        "predictive_contract_status",
        "observed_predictive_metric",
        "directional_eval_rows",
        "baseline_pass_proxy",
        "cell_beat_fraction",
        "untouched_test_pass_proxy",
        "feature_stability_proxy_available",
        "predictive_promotion_candidate_proxy",
        "falsification_status",
        "calibrated_model_required",
        "baseline_lift_required",
        "holdout_or_untouched_required",
        "promotion_falsification_required",
        "acceptance_requirement_met_after_contract",
        "blocking_gap_after_contract",
        "required_predictive_action",
        "required_next_evidence",
    ]
    for column in columns:
        if column not in rows:
            rows[column] = False if column.endswith("_required") or column.endswith("_proxy") else ""
    return rows[columns].sort_values(["execution_rank"], kind="mergesort")


def build_predictive_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    if ledger.empty:
        return pd.DataFrame()
    grouped = (
        ledger.groupby(["predictive_contract_status"], sort=True)
        .agg(
            rows=("hardening_requirement", "size"),
            strategies=("strategy_id", "nunique"),
            acceptance_met_rows=("acceptance_requirement_met_after_contract", "sum"),
        )
        .reset_index()
    )
    return grouped.sort_values(["rows", "predictive_contract_status"], ascending=[False, True], kind="mergesort")


def build_strategy_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    if ledger.empty:
        return pd.DataFrame()
    grouped = (
        ledger.groupby(["strategy_id", "strategy_support_level", "strategy_role"], sort=True)
        .agg(
            m03_rows=("hardening_requirement", "size"),
            distinct_statuses=("predictive_contract_status", "nunique"),
            acceptance_met_rows=("acceptance_requirement_met_after_contract", "sum"),
            baseline_pass_proxy=("baseline_pass_proxy", "max"),
            predictive_promotion_candidate_proxy=("predictive_promotion_candidate_proxy", "max"),
            first_required_action=("required_predictive_action", "first"),
        )
        .reset_index()
    )
    grouped["predictive_validation_status"] = grouped.apply(
        lambda row: "proxy_or_support_blocked_not_acceptance"
        if int(row["acceptance_met_rows"]) == 0
        else "partially_met_not_promotion_ready",
        axis=1,
    )
    return grouped.sort_values(["predictive_validation_status", "strategy_id"], kind="mergesort")


def write_report(
    output_dir: Path,
    criteria: pd.DataFrame,
    ledger: pd.DataFrame,
    predictive_summary: pd.DataFrame,
    strategy_summary: pd.DataFrame,
) -> None:
    lines = [
        "# Phase 20 M03 Predictive Validation Contract",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase converts the third Phase 20 execution milestone into a predictive validation contract.",
        "It consolidates current baseline, holdout, feature-stability and promotion-falsification proxy diagnostics and keeps every row non-acceptance-ready until calibrated, frozen, out-of-sample predictive evidence exists.",
        "",
        "## Acceptance Criteria Contract",
        "",
        _markdown_table(criteria),
        "",
        "## Predictive Requirement Summary",
        "",
        _markdown_table(predictive_summary),
        "",
        "## Strategy Summary",
        "",
        _markdown_table(strategy_summary),
        "",
        "## M03 Predictive Validation Ledger",
        "",
        _markdown_table(ledger),
        "",
    ]
    (output_dir / "phase20_m03_predictive_validation_contract_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase20_m03(paths: dict[str, Path], output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    execution_roadmap = pd.read_csv(paths["execution_roadmap"])
    baseline = pd.read_csv(paths["predictive_baseline_comparison"])
    holdout = pd.read_csv(paths["predictive_holdout_stability_summary"])
    falsification = pd.read_csv(paths["predictive_promotion_falsification"])
    support_decisions = pd.read_csv(paths["strategy_support_decision_summary"])
    criteria = build_acceptance_criteria()
    ledger = build_predictive_validation_ledger(execution_roadmap, baseline, holdout, falsification, support_decisions)
    predictive_summary = build_predictive_summary(ledger)
    strategy_summary = build_strategy_summary(ledger)

    criteria.to_csv(output_dir / "predictive_validation_acceptance_criteria.csv", index=False)
    ledger.to_csv(output_dir / "predictive_validation_ledger.csv", index=False)
    predictive_summary.to_csv(output_dir / "predictive_validation_gap_summary.csv", index=False)
    strategy_summary.to_csv(output_dir / "predictive_validation_strategy_summary.csv", index=False)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "predictive_validation_acceptance_criteria_rows": int(len(criteria)),
        "predictive_validation_rows": int(len(ledger)),
        "predictive_validation_gap_summary_rows": int(len(predictive_summary)),
        "predictive_validation_strategy_rows": int(len(strategy_summary)),
        "calibrated_model_required_rows": int(ledger["calibrated_model_required"].astype(bool).sum()),
        "baseline_lift_required_rows": int(ledger["baseline_lift_required"].astype(bool).sum()),
        "holdout_or_untouched_required_rows": int(ledger["holdout_or_untouched_required"].astype(bool).sum()),
        "promotion_falsification_required_rows": int(ledger["promotion_falsification_required"].astype(bool).sum()),
        "acceptance_met_after_contract_rows": int(ledger["acceptance_requirement_met_after_contract"].astype(bool).sum()),
        "scope": "phase20_m03_predictive_validation_contract_not_acceptance",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase20_m03",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={"predictive_acceptance_criteria": PREDICTIVE_ACCEPTANCE_CRITERIA},
            outputs={
                "predictive_validation_acceptance_criteria": str(output_dir / "predictive_validation_acceptance_criteria.csv"),
                "predictive_validation_ledger": str(output_dir / "predictive_validation_ledger.csv"),
                "predictive_validation_gap_summary": str(output_dir / "predictive_validation_gap_summary.csv"),
                "predictive_validation_strategy_summary": str(output_dir / "predictive_validation_strategy_summary.csv"),
                "report": str(output_dir / "phase20_m03_predictive_validation_contract_report.md"),
                "manifest": str(output_dir / "predictive_validation_contract_manifest.json"),
            },
            random_seed="not_applicable_deterministic_predictive_validation_contract",
            scenario_ids="phase20_M03_predictive_model_and_baseline_validation_rows",
            cost_model_version="not_applicable_no_execution_costs",
            latency_model_version="not_applicable_no_latency_model",
            base_dir=base_dir,
        )
    )
    (output_dir / "predictive_validation_contract_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, criteria, ledger, predictive_summary, strategy_summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 20 M03 predictive validation contract artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase20_m03"))
    parser.add_argument("--execution-roadmap", type=Path, default=Path("outputs/phase20/acceptance_execution_roadmap.csv"))
    parser.add_argument("--predictive-baseline-comparison", type=Path, default=Path("outputs/phase16/predictive_baseline_comparison.csv"))
    parser.add_argument("--predictive-holdout-stability-summary", type=Path, default=Path("outputs/phase16/predictive_holdout_stability_summary.csv"))
    parser.add_argument("--predictive-promotion-falsification", type=Path, default=Path("outputs/phase16/predictive_promotion_falsification.csv"))
    parser.add_argument("--strategy-support-decision-summary", type=Path, default=Path("outputs/phase20_m02/strategy_support_decision_summary.csv"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "execution_roadmap": args.execution_roadmap,
        "predictive_baseline_comparison": args.predictive_baseline_comparison,
        "predictive_holdout_stability_summary": args.predictive_holdout_stability_summary,
        "predictive_promotion_falsification": args.predictive_promotion_falsification,
        "strategy_support_decision_summary": args.strategy_support_decision_summary,
    }
    run_phase20_m03(paths, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
