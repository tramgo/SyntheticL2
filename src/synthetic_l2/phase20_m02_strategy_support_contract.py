from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


SUPPORT_DECISION_POLICY = {
    "runnable_proxy": "proxy_support_available_acceptance_upgrade_required",
    "partial_missing_required_features": "feature_engineering_required_before_acceptance",
    "not_supported_by_current_product": "explicit_research_or_risk_only_classification_required",
}

SUPPORT_ACCEPTANCE_CRITERIA = [
    (
        "feature_product_coverage",
        "Every required strategy feature is present in the acceptance feature product at the intended horizon.",
        "all required features present; no proxy-only substitute for required acceptance feature",
    ),
    (
        "module_registry_decision",
        "Every S01-S11 module has an explicit acceptance path or explicit research/risk-only exclusion.",
        "no strategy has ambiguous support status",
    ),
    (
        "alpha_registry_scope",
        "Only alpha strategies enter predictive/robustness promotion grids; non-alpha/risk filters are excluded from alpha promotion.",
        "S10/S11 excluded or separately registered as execution/risk controls",
    ),
    (
        "support_evidence_lineage",
        "Feature/module support decisions cite current artifacts and missing-feature lists.",
        "every M02 row has evidence_source and required_next_evidence",
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
            for criterion_id, description, threshold in SUPPORT_ACCEPTANCE_CRITERIA
        ]
    )


def build_support_closure_ledger(
    execution_roadmap: pd.DataFrame,
    feature_availability: pd.DataFrame,
    module_registry: pd.DataFrame,
    robustness_dimension: pd.DataFrame,
) -> pd.DataFrame:
    m02 = execution_roadmap[
        execution_roadmap["execution_milestone"].astype(str) == "M02_strategy_support_and_registry_closure"
    ].copy()
    feature_cols = [
        "strategy_id",
        "name",
        "support_level",
        "proxy_feature_count",
        "proxy_features_present",
        "proxy_features_absent",
        "present_proxy_features",
        "absent_proxy_features",
        "plan_missing_features",
    ]
    module_cols = [
        "strategy_id",
        "module_type",
        "implementation_status",
        "signal_status",
        "acceptance_grade",
        "promotion_ready",
        "limitation",
    ]
    robustness_cols = [
        "strategy_id",
        "registered_for_phase13_proxy",
        "planned_registry_rows",
        "initial_engineering_seeds_run",
        "required_full_validation_seeds",
        "walk_forward_windows_run",
        "walk_forward_windows_planned",
    ]
    rows = (
        m02.merge(feature_availability[[c for c in feature_cols if c in feature_availability]], on="strategy_id", how="left", suffixes=("", "_feature"))
        .merge(module_registry[[c for c in module_cols if c in module_registry]], on="strategy_id", how="left")
        .merge(robustness_dimension[[c for c in robustness_cols if c in robustness_dimension]], on="strategy_id", how="left")
    )
    rows["support_decision_policy"] = rows["strategy_support_level"].map(SUPPORT_DECISION_POLICY).fillna("unknown_support_policy")
    rows["classification_required"] = rows["strategy_support_level"].astype(str).eq("not_supported_by_current_product")
    rows["feature_engineering_required"] = rows["strategy_support_level"].astype(str).eq("partial_missing_required_features")
    rows["acceptance_upgrade_required"] = rows["strategy_support_level"].astype(str).eq("runnable_proxy")
    rows["alpha_promotion_scope"] = rows.apply(
        lambda row: "exclude_from_alpha_promotion_or_register_as_control"
        if row["classification_required"]
        else "eligible_for_future_alpha_support_upgrade"
        if row["strategy_role"] != "risk_filter_only"
        else "risk_filter_only_not_alpha_promotion",
        axis=1,
    )
    rows["support_contract_status"] = rows.apply(
        lambda row: "proxy_supported_acceptance_upgrade_required"
        if row["acceptance_upgrade_required"]
        else "partial_support_feature_engineering_required"
        if row["feature_engineering_required"]
        else "unsupported_requires_explicit_non_alpha_classification",
        axis=1,
    )
    rows["acceptance_requirement_met_after_contract"] = False
    rows["blocking_gap_after_contract"] = rows.apply(
        lambda row: (
            "Runnable proxy exists, but acceptance feature horizon/module evidence and full validation reruns are still required."
            if row["acceptance_upgrade_required"]
            else "Partial proxy exists, but required plan features are still missing from the current acceptance feature product."
            if row["feature_engineering_required"]
            else "Strategy is not supported by the current alpha feature product and must be explicitly excluded or separately registered as non-alpha control."
        ),
        axis=1,
    )
    rows["required_support_action"] = rows.apply(
        lambda row: (
            f"Upgrade proxy module to acceptance-grade feature horizon and rerun validation for {row['strategy_id']}."
            if row["acceptance_upgrade_required"]
            else f"Implement missing plan features for {row['strategy_id']}: {row.get('plan_missing_features', '')}."
            if row["feature_engineering_required"]
            else f"Classify {row['strategy_id']} as research-only/risk-filter-only or build a separate non-alpha registry path."
        ),
        axis=1,
    )
    columns = [
        "execution_rank",
        "gate_id",
        "strategy_id",
        "name",
        "strategy_support_level",
        "strategy_role",
        "hardening_requirement",
        "action_class",
        "dependency_status",
        "support_decision_policy",
        "support_contract_status",
        "alpha_promotion_scope",
        "classification_required",
        "feature_engineering_required",
        "acceptance_upgrade_required",
        "proxy_feature_count",
        "proxy_features_present",
        "proxy_features_absent",
        "present_proxy_features",
        "plan_missing_features",
        "module_type",
        "implementation_status",
        "signal_status",
        "registered_for_phase13_proxy",
        "planned_registry_rows",
        "initial_engineering_seeds_run",
        "required_full_validation_seeds",
        "walk_forward_windows_run",
        "walk_forward_windows_planned",
        "acceptance_requirement_met_after_contract",
        "blocking_gap_after_contract",
        "required_support_action",
        "required_next_evidence",
    ]
    for column in columns:
        if column not in rows:
            rows[column] = False if column.endswith("_required") or column.endswith("_contract") else ""
    return rows[columns].sort_values(["execution_rank"], kind="mergesort")


def build_support_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    if ledger.empty:
        return pd.DataFrame(columns=["support_contract_status", "gate_id", "rows", "strategies", "acceptance_met_rows"])
    grouped = (
        ledger.groupby(["support_contract_status", "gate_id"], sort=True)
        .agg(
            rows=("hardening_requirement", "size"),
            strategies=("strategy_id", "nunique"),
            acceptance_met_rows=("acceptance_requirement_met_after_contract", "sum"),
        )
        .reset_index()
    )
    return grouped.sort_values(["support_contract_status", "gate_id"], kind="mergesort")


def build_strategy_decision_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    if ledger.empty:
        return pd.DataFrame()
    grouped = (
        ledger.groupby(["strategy_id", "name", "strategy_support_level", "strategy_role"], sort=True)
        .agg(
            m02_rows=("hardening_requirement", "size"),
            gates=("gate_id", "nunique"),
            feature_engineering_required=("feature_engineering_required", "max"),
            classification_required=("classification_required", "max"),
            acceptance_upgrade_required=("acceptance_upgrade_required", "max"),
            acceptance_met_rows=("acceptance_requirement_met_after_contract", "sum"),
            required_support_action=("required_support_action", "first"),
        )
        .reset_index()
    )
    grouped["strategy_support_closure_status"] = grouped.apply(
        lambda row: "requires_explicit_non_alpha_classification"
        if bool(row["classification_required"])
        else "requires_feature_engineering"
        if bool(row["feature_engineering_required"])
        else "proxy_supported_requires_acceptance_upgrade",
        axis=1,
    )
    return grouped.sort_values(["strategy_support_closure_status", "strategy_id"], kind="mergesort")


def write_report(
    output_dir: Path,
    criteria: pd.DataFrame,
    ledger: pd.DataFrame,
    support_summary: pd.DataFrame,
    strategy_summary: pd.DataFrame,
) -> None:
    lines = [
        "# Phase 20 M02 Strategy Support Contract",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase converts the second Phase 20 execution milestone into a strategy support and registry closure contract.",
        "It does not make any strategy acceptance-ready. It identifies which strategies need feature engineering, proxy-to-acceptance upgrades, or explicit research/risk-only classification before acceptance reruns.",
        "",
        "## Acceptance Criteria Contract",
        "",
        _markdown_table(criteria),
        "",
        "## Support Summary",
        "",
        _markdown_table(support_summary),
        "",
        "## Strategy Decision Summary",
        "",
        _markdown_table(strategy_summary),
        "",
        "## M02 Support Closure Ledger",
        "",
        _markdown_table(ledger),
        "",
    ]
    (output_dir / "phase20_m02_strategy_support_contract_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase20_m02(paths: dict[str, Path], output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    execution_roadmap = pd.read_csv(paths["execution_roadmap"])
    feature_availability = pd.read_csv(paths["strategy_feature_availability"])
    module_registry = pd.read_csv(paths["strategy_module_registry"])
    robustness_dimension = pd.read_csv(paths["robustness_dimension_summary"])
    criteria = build_acceptance_criteria()
    ledger = build_support_closure_ledger(execution_roadmap, feature_availability, module_registry, robustness_dimension)
    support_summary = build_support_summary(ledger)
    strategy_summary = build_strategy_decision_summary(ledger)

    criteria.to_csv(output_dir / "strategy_support_acceptance_criteria.csv", index=False)
    ledger.to_csv(output_dir / "strategy_support_closure_ledger.csv", index=False)
    support_summary.to_csv(output_dir / "strategy_support_gap_summary.csv", index=False)
    strategy_summary.to_csv(output_dir / "strategy_support_decision_summary.csv", index=False)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "strategy_support_acceptance_criteria_rows": int(len(criteria)),
        "strategy_support_closure_rows": int(len(ledger)),
        "strategy_support_gap_summary_rows": int(len(support_summary)),
        "strategy_support_decision_rows": int(len(strategy_summary)),
        "feature_engineering_required_rows": int(ledger["feature_engineering_required"].astype(bool).sum()),
        "classification_required_rows": int(ledger["classification_required"].astype(bool).sum()),
        "acceptance_upgrade_required_rows": int(ledger["acceptance_upgrade_required"].astype(bool).sum()),
        "acceptance_met_after_contract_rows": int(ledger["acceptance_requirement_met_after_contract"].astype(bool).sum()),
        "scope": "phase20_m02_strategy_support_and_registry_contract_not_acceptance",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase20_m02",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={
                "support_decision_policy": SUPPORT_DECISION_POLICY,
                "support_acceptance_criteria": SUPPORT_ACCEPTANCE_CRITERIA,
            },
            outputs={
                "strategy_support_acceptance_criteria": str(output_dir / "strategy_support_acceptance_criteria.csv"),
                "strategy_support_closure_ledger": str(output_dir / "strategy_support_closure_ledger.csv"),
                "strategy_support_gap_summary": str(output_dir / "strategy_support_gap_summary.csv"),
                "strategy_support_decision_summary": str(output_dir / "strategy_support_decision_summary.csv"),
                "report": str(output_dir / "phase20_m02_strategy_support_contract_report.md"),
                "manifest": str(output_dir / "strategy_support_contract_manifest.json"),
            },
            random_seed="not_applicable_deterministic_strategy_support_contract",
            scenario_ids="phase20_M02_strategy_support_and_registry_closure_rows",
            cost_model_version="not_applicable_no_execution_costs",
            latency_model_version="not_applicable_no_latency_model",
            base_dir=base_dir,
        )
    )
    (output_dir / "strategy_support_contract_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, criteria, ledger, support_summary, strategy_summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 20 M02 strategy support and registry closure artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase20_m02"))
    parser.add_argument("--execution-roadmap", type=Path, default=Path("outputs/phase20/acceptance_execution_roadmap.csv"))
    parser.add_argument("--strategy-feature-availability", type=Path, default=Path("outputs/phase11/strategy_feature_availability.csv"))
    parser.add_argument("--strategy-module-registry", type=Path, default=Path("outputs/phase11/strategy_module_registry.csv"))
    parser.add_argument("--robustness-dimension-summary", type=Path, default=Path("outputs/phase13/robustness_dimension_summary.csv"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "execution_roadmap": args.execution_roadmap,
        "strategy_feature_availability": args.strategy_feature_availability,
        "strategy_module_registry": args.strategy_module_registry,
        "robustness_dimension_summary": args.robustness_dimension_summary,
    }
    run_phase20_m02(paths, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
