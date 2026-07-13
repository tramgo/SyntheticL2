from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase19_reproducibility import FIELD_ALIASES, MANIFEST_CANDIDATES, REQUIRED_FIELDS, _load_json
from synthetic_l2.reproducibility import reproducibility_fields


def _git_sha(base_dir: Path) -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=base_dir, text=True).strip()
    except Exception:
        return "git_sha_unavailable"


def _first_alias_value(manifest: dict[str, Any] | None, field: str) -> Any:
    if manifest is None:
        return None
    aliases = FIELD_ALIASES[field]
    for alias in [field, *aliases]:
        if alias in manifest and manifest[alias] not in (None, ""):
            return manifest[alias]
    for value in manifest.values():
        if isinstance(value, dict):
            child = _first_alias_value(value, field)
            if child not in (None, ""):
                return child
    return None


def _stable_config_hash(artifact_id: str, rel_path: str, manifest: dict[str, Any] | None) -> str:
    payload = {
        "artifact_id": artifact_id,
        "manifest_path": rel_path,
        "source_manifest": manifest or {},
    }
    raw = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _default_value(field: str, artifact_id: str, rel_path: str, git_sha: str, manifest: dict[str, Any] | None) -> str:
    if field == "generator_version":
        return git_sha
    if field == "configuration_hash":
        return _stable_config_hash(artifact_id, rel_path, manifest)
    if field == "random_seed":
        return "not_applicable_or_seed_plan_not_recorded"
    if field == "calibration_dataset_id":
        return "zerodha_l2_single_day_seed_and_current_synthetic_outputs"
    if field == "ticker_metadata_version":
        return "nse_32_symbol_universe_current_plan"
    if field == "regime_calendar_version":
        return "outputs/phase4/scenario_calendar.csv_or_not_applicable"
    if field == "scenario_ids":
        return "current_phase_outputs_all_available_scenarios_or_not_applicable"
    if field == "cost_model_version":
        return "zerodha_equity_intraday_nse_round_trip_bps_v1_or_not_applicable"
    if field == "latency_model_version":
        return "phase8_retail_feed_profiles_and_phase12_execution_profiles_or_not_applicable"
    if field == "creation_timestamp":
        value = _first_alias_value(manifest, field)
        return str(value) if value not in (None, "") else datetime.now(timezone.utc).isoformat()
    raise KeyError(field)


def normalize_manifest(artifact_id: str, rel_path: str, manifest: dict[str, Any] | None, git_sha: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    required_values: dict[str, Any] = {}
    field_rows = []
    for field, _definition in REQUIRED_FIELDS:
        source_value = _first_alias_value(manifest, field)
        if source_value not in (None, ""):
            value = source_value
            source = "source_manifest_exact_or_alias"
        else:
            value = _default_value(field, artifact_id, rel_path, git_sha, manifest)
            source = "normalizer_default"
        required_values[field] = value
        field_rows.append(
            {
                "artifact_id": artifact_id,
                "required_field": field,
                "value_source": source,
                "normalized_value_present": value not in (None, ""),
            }
        )
    normalized = {
        "schema_name": "synthetic_l2_reproducibility_manifest_v1",
        "artifact_id": artifact_id,
        "source_manifest_path": rel_path,
        "source_manifest_exists": manifest is not None,
        **required_values,
        "normalization_timestamp": datetime.now(timezone.utc).isoformat(),
        "normalization_scope": "exact_field_overlay_for_reproducibility_audit_not_source_manifest_rewrite",
    }
    return normalized, field_rows


def run(output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir = output_dir / "normalized_manifests"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    git_sha = _git_sha(base_dir)
    field_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    for artifact_id, rel_path in MANIFEST_CANDIDATES:
        manifest = _load_json(base_dir / rel_path)
        normalized, rows = normalize_manifest(artifact_id, rel_path, manifest, git_sha)
        out_path = manifest_dir / f"{artifact_id}.normalized_manifest.json"
        out_path.write_text(json.dumps(normalized, indent=2, default=str), encoding="utf-8")
        field_rows.extend(rows)
        summary_rows.append(
            {
                "artifact_id": artifact_id,
                "source_manifest_path": rel_path,
                "normalized_manifest_path": str(out_path),
                "source_manifest_exists": manifest is not None,
                "required_fields": len(REQUIRED_FIELDS),
                "normalized_fields_present": sum(1 for row in rows if row["normalized_value_present"]),
                "normalizer_default_fields": sum(1 for row in rows if row["value_source"] == "normalizer_default"),
                "source_manifest_exact_or_alias_fields": sum(1 for row in rows if row["value_source"] == "source_manifest_exact_or_alias"),
                "exact_field_overlay_ready": all(row["normalized_value_present"] for row in rows),
            }
        )
    summary = pd.DataFrame(summary_rows)
    fields = pd.DataFrame(field_rows)
    summary.to_csv(output_dir / "normalized_manifest_overlay_summary.csv", index=False)
    fields.to_csv(output_dir / "normalized_manifest_field_sources.csv", index=False)
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "git_sha_used": git_sha,
        "artifacts_normalized": int(len(summary)),
        "field_rows": int(len(fields)),
        "exact_field_overlay_ready_artifacts": int(summary["exact_field_overlay_ready"].sum()),
        "normalizer_default_fields": int(summary["normalizer_default_fields"].sum()),
        "source_manifest_exact_or_alias_fields": int(summary["source_manifest_exact_or_alias_fields"].sum()),
        "scope": "phase19_normalized_manifest_overlay_not_source_manifest_rewrite",
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase19_normalized_manifest_overlay",
            generated_utc=generated_utc,
            inputs={"manifest_candidates": MANIFEST_CANDIDATES},
            parameters={"required_fields": [field for field, _definition in REQUIRED_FIELDS]},
            outputs={
                "overlay_summary": str(output_dir / "normalized_manifest_overlay_summary.csv"),
                "field_sources": str(output_dir / "normalized_manifest_field_sources.csv"),
                "normalized_manifest_dir": str(manifest_dir),
            },
            cost_model_version="not_applicable_no_execution_costs",
            latency_model_version="not_applicable_no_latency_model",
            base_dir=base_dir,
        )
    )
    (output_dir / "normalized_manifest_overlay_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create normalized exact-field manifest overlays for Phase 19 audited artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase19"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run(args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
