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


MANIFEST_CANDIDATES = [
    ("stage_a1", "outputs/stage_a1/manifest_check.json"),
    ("phase1", "outputs/phase1/phase1_manifest.json"),
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
    ("phase12", "outputs/phase12/execution_manifest.json"),
    ("phase13", "outputs/phase13/experiment_design_manifest.json"),
    ("phase14", "outputs/phase14/quality_validation_manifest.json"),
    ("phase15", "outputs/phase15/acceptance_gates_manifest.json"),
    ("phase16", "outputs/phase16/metrics_reporting_manifest.json"),
    ("phase17", "outputs/phase17/work_packages_manifest.json"),
    ("phase18", "outputs/phase18/technology_stack_manifest.json"),
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


def write_report(output_dir: Path, summary: pd.DataFrame, gaps: pd.DataFrame, audit: pd.DataFrame) -> None:
    status_summary = audit.groupby("coverage_status", sort=True).size().reset_index(name="field_checks")
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
    ]
    (output_dir / "phase19_reproducibility_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase19(output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    catalog = required_field_catalog()
    audit = manifest_audit(base_dir)
    summary = artifact_summary(audit)
    gaps = gap_summary(audit)

    catalog.to_csv(output_dir / "reproducibility_required_fields.csv", index=False)
    audit.to_csv(output_dir / "manifest_field_audit.csv", index=False)
    summary.to_csv(output_dir / "artifact_reproducibility_summary.csv", index=False)
    gaps.to_csv(output_dir / "reproducibility_gap_summary.csv", index=False)
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "required_fields": int(len(catalog)),
        "audited_artifacts": int(summary["artifact_id"].nunique()),
        "field_checks": int(len(audit)),
        "exact_regeneration_ready_artifacts": int(summary["exact_regeneration_ready"].sum()),
        "artifacts_with_missing_fields": int((summary["missing_fields"] > 0).sum()),
        "manifest_missing_or_unreadable_artifacts": int((summary["manifest_missing_or_unreadable_fields"] > 0).sum()),
        "gap_rows": int(len(gaps)),
        "scope": "phase19_reproducibility_manifest_field_audit",
    }
    (output_dir / "reproducibility_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, summary, gaps, audit)


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
