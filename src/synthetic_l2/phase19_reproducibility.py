from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


REQUIRED_FIELDS = [
    ("generator_version", "Exact code/generator version for the artifact."),
    ("configuration_hash", "Hash of effective configuration used to generate the artifact."),
    ("random_seed", "Seed or seed plan for stochastic generation."),
    ("calibration_dataset_id", "Identifier for real-data calibration input."),
    ("ticker_metadata_version", "Version of ticker universe and metadata."),
    ("regime_calendar_version", "Version of regime/scenario calendar."),
    ("scenario_ids", "Scenario profile/day IDs represented in the artifact."),
    ("cost_model_version", "Version of execution/cost assumptions."),
    ("latency_model_version", "Version of feed/latency assumptions."),
    ("creation_timestamp", "Creation timestamp for the artifact."),
]


FIELD_VALUE_GUIDANCE = {
    "generator_version": "Use git commit SHA or package version for the code that generated the artifact.",
    "configuration_hash": "Hash the effective runtime configuration, inputs and materially relevant defaults.",
    "random_seed": "Record integer seed, seed-plan artifact, or explicit not_applicable_deterministic.",
    "calibration_dataset_id": "Record real-data source ID/date range or synthetic upstream artifact ID.",
    "ticker_metadata_version": "Record ticker universe version and exchange metadata source/date.",
    "regime_calendar_version": "Record scenario/regime calendar artifact and generator version.",
    "scenario_ids": "Record scenario profile/day IDs or explicit not_applicable_observed_real_sample.",
    "cost_model_version": "Record cost schedule artifact/version or explicit not_applicable_no_execution_costs.",
    "latency_model_version": "Record feed/execution latency model artifact/version or explicit not_applicable_no_latency_model.",
    "creation_timestamp": "Record generated_utc in UTC ISO-8601 format.",
}


MANIFEST_CANDIDATES = [
    ("stage_a1", "outputs/stage_a1/manifest_check.json"),
    ("phase1", "outputs/phase1/phase1_manifest.json"),
    ("phase1_event_reconstruction", "outputs/phase1/event_reconstruction/event_reconstruction_manifest.json"),
    ("stage_a2", "outputs/stage_a2/stage_a2_capture_diagnostics_contract_manifest.json"),
    ("stage_b1", "outputs/stage_b1/stage_b1_structural_synthetic_proof_manifest.json"),
    ("stage_b2", "outputs/stage_b2/stage_b2_event_driven_synthetic_proof_manifest.json"),
    ("stage_c", "outputs/stage_c/stage_c_medium_pilot_manifest.json"),
    ("stage_d", "outputs/stage_d/stage_d_three_month_study_manifest.json"),
    ("stage_e", "outputs/stage_e/stage_e_full_year_readiness_manifest.json"),
    ("phase21", "outputs/phase21/phase21_decision_framework_manifest.json"),
    ("phase22", "outputs/phase22/phase22_real_data_integration_manifest.json"),
    ("phase23", "outputs/phase23/phase23_key_risk_register_manifest.json"),
    ("phase25", "outputs/phase25/phase25_event_replay_manifest.json"),
    ("phase26", "outputs/phase26/phase26_strategy_salvage_scan_manifest.json"),
    ("phase27", "outputs/phase27/phase27_feature_edge_scan_manifest.json"),
    ("phase28", "outputs/phase28/phase28_richer_event_label_support_manifest.json"),
    ("phase29", "outputs/phase29/phase29_partial_strategy_proxy_replay_manifest.json"),
    ("phase30", "outputs/phase30/phase30_strategy_decision_triage_manifest.json"),
    ("phase31", "outputs/phase31/phase31_redesign_evidence_contract_manifest.json"),
    ("phase32", "outputs/phase32/phase32_contract_evidence_scanner_manifest.json"),
    ("phase33", "outputs/phase33/phase33_broker_evidence_intake_manifest.json"),
    ("phase34", "outputs/phase34/phase34_real_data_multiday_readiness_manifest.json"),
    ("phase35", "outputs/phase35/phase35_stage_a2_computable_diagnostics_manifest.json"),
    ("phase2", "outputs/phase2/calibration_manifest.json"),
    ("phase3", "outputs/phase3/regime_manifest.json"),
    ("phase4", "outputs/phase4/scenario_manifest.json"),
    ("phase5", "outputs/phase5/price_process_manifest.json"),
    ("phase6", "outputs/phase6/l2_book_manifest.json"),
    ("phase7", "outputs/phase7/shock_library_manifest.json"),
    ("phase8", "outputs/phase8/retail_feed_manifest.json"),
    ("phase9", "outputs/phase9/data_product_manifest.json"),
    ("phase10", "outputs/phase10/storage_manifest.json"),
    ("phase11", "outputs/phase11/strategy_validation_manifest.json"),
    ("phase11_strategy_modules", "outputs/phase11/strategy_module_registry_manifest.json"),
    ("phase12", "outputs/phase12/execution_manifest.json"),
    ("phase12_event_backtest", "outputs/phase12/event_backtest_manifest.json"),
    ("phase13", "outputs/phase13/experiment_design_manifest.json"),
    ("phase13_smoke_run", "outputs/phase13/experiment_run_manifest.json"),
    ("phase14", "outputs/phase14/quality_validation_manifest.json"),
    ("phase15", "outputs/phase15/acceptance_gates_manifest.json"),
    ("phase16", "outputs/phase16/metrics_reporting_manifest.json"),
    ("phase17", "outputs/phase17/work_packages_manifest.json"),
    ("phase18", "outputs/phase18/technology_stack_manifest.json"),
    ("phase20", "outputs/phase20/acceptance_hardening_manifest.json"),
    ("phase20_m01", "outputs/phase20_m01/broker_evidence_contract_manifest.json"),
    ("phase20_m02", "outputs/phase20_m02/strategy_support_contract_manifest.json"),
    ("phase20_m03", "outputs/phase20_m03/predictive_validation_contract_manifest.json"),
    ("phase20_m04", "outputs/phase20_m04/robustness_execution_contract_manifest.json"),
    ("phase20_m05", "outputs/phase20_m05/lifecycle_economic_replay_contract_manifest.json"),
    ("phase20_m06", "outputs/phase20_m06/realism_rerun_contract_manifest.json"),
    ("phase20_m07", "outputs/phase20_m07/real_multiday_acceptance_contract_manifest.json"),
    ("horizon_readiness", "outputs/horizon_readiness/horizon_readiness_manifest.json"),
    ("dashboard", "outputs/dashboard/validation_dashboard_manifest.json"),
    ("duckdb", "outputs/duckdb/duckdb_workspace_manifest.json"),
]


FIELD_ALIASES = {
    "creation_timestamp": ["generated_utc", "created_utc", "creation_timestamp"],
    "random_seed": ["random_seed", "seed", "seed_plan", "seeds"],
    "scenario_ids": ["scenario_ids", "scenario_day", "scenario_profiles", "quarter_profile"],
    "calibration_dataset_id": ["calibration_dataset_id", "real_data_sample", "source_dataset", "features_path"],
    "cost_model_version": ["cost_model_version", "cost_schedule", "execution_profiles"],
    "latency_model_version": ["latency_model_version", "feed_profiles", "execution_profiles"],
    "regime_calendar_version": ["regime_calendar_version", "scenario_calendar", "phase4_calendar"],
    "ticker_metadata_version": ["ticker_metadata_version", "symbols", "target_symbols"],
    "configuration_hash": ["configuration_hash", "config_hash"],
    "generator_version": ["generator_version", "code_version"],
}


def _flatten_keys(value: Any, prefix: str = "") -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            full = f"{prefix}.{key_text}" if prefix else key_text
            keys.add(full)
            keys.add(key_text)
            keys.update(_flatten_keys(child, full))
    elif isinstance(value, list):
        for idx, child in enumerate(value[:20]):
            keys.update(_flatten_keys(child, f"{prefix}[{idx}]"))
    return keys


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def required_field_catalog() -> pd.DataFrame:
    return pd.DataFrame(REQUIRED_FIELDS, columns=["required_field", "definition"])


def manifest_schema_template() -> dict[str, Any]:
    return {
        "schema_name": "synthetic_l2_reproducibility_manifest_v1",
        "schema_purpose": "Minimum metadata required to evaluate whether a generated artifact can be exactly regenerated.",
        "required_fields": [
            {
                "field": field,
                "definition": definition,
                "value_guidance": FIELD_VALUE_GUIDANCE[field],
                "allowed_missing_policy": "Do not omit. Use an explicit not_applicable_* value only when the concept truly does not apply.",
            }
            for field, definition in REQUIRED_FIELDS
        ],
        "recommended_additional_fields": [
            "inputs",
            "outputs",
            "generator_command",
            "environment",
            "dependency_versions",
            "artifact_row_counts",
            "validation_checks",
        ],
    }


def manifest_audit(base_dir: Path) -> pd.DataFrame:
    rows = []
    for artifact_id, rel_path in MANIFEST_CANDIDATES:
        path = base_dir / rel_path
        manifest = _load_json(path)
        keys = _flatten_keys(manifest) if manifest is not None else set()
        for field, _definition in REQUIRED_FIELDS:
            aliases = FIELD_ALIASES[field]
            exact = field in keys
            alias_hits = sorted(alias for alias in aliases if alias in keys)
            if manifest is None:
                status = "manifest_missing_or_unreadable"
            elif exact:
                status = "present_exact"
            elif alias_hits:
                status = "present_alias_or_inferred"
            else:
                status = "missing"
            rows.append(
                {
                    "artifact_id": artifact_id,
                    "manifest_path": rel_path,
                    "manifest_exists": path.exists(),
                    "required_field": field,
                    "coverage_status": status,
                    "matched_aliases": ";".join(alias_hits),
                }
            )
    return pd.DataFrame(rows)


def artifact_summary(audit: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for artifact_id, group in audit.groupby("artifact_id", sort=True):
        exact = int((group["coverage_status"] == "present_exact").sum())
        inferred = int((group["coverage_status"] == "present_alias_or_inferred").sum())
        missing = int((group["coverage_status"] == "missing").sum())
        unreadable = int((group["coverage_status"] == "manifest_missing_or_unreadable").sum())
        exact_regeneration_ready = missing == 0 and unreadable == 0 and exact + inferred == len(group)
        rows.append(
            {
                "artifact_id": artifact_id,
                "manifest_path": group["manifest_path"].iloc[0],
                "required_fields": int(len(group)),
                "present_exact": exact,
                "present_alias_or_inferred": inferred,
                "missing_fields": missing,
                "manifest_missing_or_unreadable_fields": unreadable,
                "exact_regeneration_ready": exact_regeneration_ready,
            }
        )
    return pd.DataFrame(rows)


def gap_summary(audit: pd.DataFrame) -> pd.DataFrame:
    gaps = audit[audit["coverage_status"].isin(["missing", "manifest_missing_or_unreadable"])].copy()
    if gaps.empty:
        return pd.DataFrame(columns=["required_field", "affected_artifacts", "coverage_status", "recommended_action"])
    grouped = gaps.groupby(["required_field", "coverage_status"], sort=True).agg(
        affected_artifacts=("artifact_id", lambda values: ";".join(sorted(values))),
        artifact_count=("artifact_id", "nunique"),
    ).reset_index()
    grouped["recommended_action"] = grouped["required_field"].map(_recommended_action)
    return grouped[
        ["required_field", "coverage_status", "artifact_count", "affected_artifacts", "recommended_action"]
    ].sort_values(["coverage_status", "required_field"], kind="mergesort")


def remediation_plan(audit: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for row in audit.to_dict("records"):
        status = row["coverage_status"]
        field = row["required_field"]
        if status == "present_exact":
            remediation_status = "complete_exact"
            action = "No remediation required."
            value_source = field
        elif status == "present_alias_or_inferred":
            remediation_status = "normalize_alias_to_exact_field"
            action = f"Copy or rename matched alias into exact field `{field}` in the next generated manifest."
            value_source = row.get("matched_aliases") or "alias"
        elif status == "manifest_missing_or_unreadable":
            remediation_status = "recover_or_rerun_manifest"
            action = "Recover the manifest or rerun the generating phase with the normalized manifest schema."
            value_source = "manifest_missing_or_unreadable"
        else:
            remediation_status = "add_field_in_generator"
            action = _recommended_action(field)
            value_source = FIELD_VALUE_GUIDANCE[field]
        rows.append(
            {
                "artifact_id": row["artifact_id"],
                "manifest_path": row["manifest_path"],
                "required_field": field,
                "current_coverage_status": status,
                "matched_aliases": row.get("matched_aliases", ""),
                "remediation_status": remediation_status,
                "recommended_value_source": value_source,
                "recommended_action": action,
            }
        )
    frame = pd.DataFrame(rows)
    status_rank = {
        "recover_or_rerun_manifest": 0,
        "add_field_in_generator": 1,
        "normalize_alias_to_exact_field": 2,
        "complete_exact": 3,
    }
    frame["remediation_rank"] = frame["remediation_status"].map(status_rank)
    return frame.sort_values(["remediation_rank", "artifact_id", "required_field"], kind="mergesort").drop(columns=["remediation_rank"])


def remediation_summary(plan: pd.DataFrame) -> pd.DataFrame:
    return (
        plan.groupby("remediation_status", sort=True)
        .agg(
            field_checks=("required_field", "count"),
            artifacts=("artifact_id", "nunique"),
        )
        .reset_index()
        .sort_values("remediation_status", kind="mergesort")
    )


def _recommended_action(field: str) -> str:
    actions = {
        "generator_version": "Add generator_version or code hash to every phase manifest.",
        "configuration_hash": "Serialize effective config and store a stable hash per artifact.",
        "random_seed": "Record seed or seed-plan reference for every stochastic artifact.",
        "calibration_dataset_id": "Record real-data calibration dataset identifier and date range.",
        "ticker_metadata_version": "Version ticker universe and metadata source.",
        "regime_calendar_version": "Record scenario/regime calendar version for generated artifacts.",
        "scenario_ids": "Record scenario IDs/profiles represented by each generated artifact.",
        "cost_model_version": "Version execution/cost assumptions and cost schedule.",
        "latency_model_version": "Version feed latency/drop/duplication assumptions.",
        "creation_timestamp": "Store generated_utc or creation_timestamp in every manifest.",
    }
    return actions[field]


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


def write_report(output_dir: Path, summary: pd.DataFrame, gaps: pd.DataFrame, audit: pd.DataFrame, remediation: pd.DataFrame, remediation_status: pd.DataFrame) -> None:
    status_summary = audit.groupby("coverage_status", sort=True).size().reset_index(name="field_checks")
    normalized_summary_path = output_dir / "normalized_manifest_overlay_summary.csv"
    normalized_field_path = output_dir / "normalized_manifest_field_sources.csv"
    normalized_lines = []
    if normalized_summary_path.exists() and normalized_field_path.exists():
        normalized_summary = pd.read_csv(normalized_summary_path)
        normalized_fields = pd.read_csv(normalized_field_path)
        overlay_totals = pd.DataFrame(
            [
                {
                    "overlay_metric": "normalized_overlay_artifacts",
                    "value": int(len(normalized_summary)),
                },
                {
                    "overlay_metric": "exact_field_overlay_ready_artifacts",
                    "value": int(normalized_summary["exact_field_overlay_ready"].sum()),
                },
                {
                    "overlay_metric": "normalizer_default_fields",
                    "value": int(normalized_summary["normalizer_default_fields"].sum()),
                },
                {
                    "overlay_metric": "source_manifest_exact_or_alias_fields",
                    "value": int(normalized_summary["source_manifest_exact_or_alias_fields"].sum()),
                },
                {
                    "overlay_metric": "normalized_field_rows",
                    "value": int(len(normalized_fields)),
                },
            ]
        )
        normalized_lines = [
            "## Normalized Manifest Overlay",
            "",
            "The overlay provides exact required-field manifests for current audit artifacts without rewriting historical source manifests.",
            "It is a reproducibility bridge, not proof that every original phase generator already emits normalized manifests.",
            "",
            _markdown_table(overlay_totals),
            "",
            _markdown_table(normalized_summary),
            "",
        ]
    lines = [
        "# Phase 19 Reproducibility Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase audits whether current manifests contain the metadata needed for exact regeneration.",
        "It treats aliases and inferred references as useful but not as strong as exact versioned fields.",
        "",
        "## Coverage Status Summary",
        "",
        _markdown_table(status_summary),
        "",
        "## Artifact Summary",
        "",
        _markdown_table(summary),
        "",
        "## Reproducibility Gaps",
        "",
        _markdown_table(gaps),
        "",
        "## Remediation Status",
        "",
        _markdown_table(remediation_status),
        "",
        *normalized_lines,
        "## Highest Priority Remediation Rows",
        "",
        _markdown_table(remediation.head(40)),
        "",
    ]
    (output_dir / "phase19_reproducibility_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase19(output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    catalog = required_field_catalog()
    audit = manifest_audit(base_dir)
    summary = artifact_summary(audit)
    gaps = gap_summary(audit)
    remediation = remediation_plan(audit)
    remediation_status = remediation_summary(remediation)

    catalog.to_csv(output_dir / "reproducibility_required_fields.csv", index=False)
    audit.to_csv(output_dir / "manifest_field_audit.csv", index=False)
    summary.to_csv(output_dir / "artifact_reproducibility_summary.csv", index=False)
    gaps.to_csv(output_dir / "reproducibility_gap_summary.csv", index=False)
    remediation.to_csv(output_dir / "reproducibility_remediation_plan.csv", index=False)
    remediation_status.to_csv(output_dir / "reproducibility_remediation_summary.csv", index=False)
    (output_dir / "manifest_schema_template.json").write_text(json.dumps(manifest_schema_template(), indent=2), encoding="utf-8")
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "required_fields": int(len(catalog)),
        "audited_artifacts": int(summary["artifact_id"].nunique()),
        "field_checks": int(len(audit)),
        "exact_regeneration_ready_artifacts": int(summary["exact_regeneration_ready"].sum()),
        "artifacts_with_missing_fields": int((summary["missing_fields"] > 0).sum()),
        "manifest_missing_or_unreadable_artifacts": int((summary["manifest_missing_or_unreadable_fields"] > 0).sum()),
        "gap_rows": int(len(gaps)),
        "remediation_rows": int(len(remediation)),
        "remediation_summary_rows": int(len(remediation_status)),
        "schema_template": str(output_dir / "manifest_schema_template.json"),
        "scope": "phase19_reproducibility_manifest_field_audit",
    }
    (output_dir / "reproducibility_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, summary, gaps, audit, remediation, remediation_status)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit reproducibility metadata coverage across phase manifests.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase19"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase19(args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
