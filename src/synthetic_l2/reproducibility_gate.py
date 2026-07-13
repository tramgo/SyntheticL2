from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class GateResult:
    name: str
    passed: bool
    observed: Any
    expected: Any
    detail: str


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _int(row: dict[str, str], column: str) -> int:
    value = row.get(column, "")
    return int(float(value)) if value not in ("", None) else 0


def run_gate(phase19_dir: Path) -> dict[str, Any]:
    summary_path = phase19_dir / "artifact_reproducibility_summary.csv"
    overlay_path = phase19_dir / "normalized_manifest_overlay_summary.csv"
    remediation_path = phase19_dir / "reproducibility_remediation_summary.csv"
    audit_path = phase19_dir / "manifest_field_audit.csv"

    summary = _read_csv(summary_path)
    overlay = _read_csv(overlay_path)
    remediation = _read_csv(remediation_path)
    audit = _read_csv(audit_path)

    exact_ready = [row for row in summary if row.get("exact_regeneration_ready") == "True"]
    missing_field_artifacts = [row["artifact_id"] for row in summary if _int(row, "missing_fields") > 0]
    unreadable_artifacts = [row["artifact_id"] for row in summary if _int(row, "manifest_missing_or_unreadable_fields") > 0]
    not_ready = [row["artifact_id"] for row in summary if row.get("exact_regeneration_ready") != "True"]
    overlay_not_ready = [row["artifact_id"] for row in overlay if row.get("exact_field_overlay_ready") != "True"]
    overlay_defaults = sum(_int(row, "normalizer_default_fields") for row in overlay)
    remediation_statuses = {row.get("remediation_status"): _int(row, "field_checks") for row in remediation}

    results = [
        GateResult(
            name="all_audited_artifacts_native_exact_ready",
            passed=len(exact_ready) == len(summary) and not not_ready,
            observed=f"{len(exact_ready)}/{len(summary)}",
            expected=f"{len(summary)}/{len(summary)}",
            detail="Artifacts not exact-ready: " + (", ".join(not_ready) if not_ready else "none"),
        ),
        GateResult(
            name="no_missing_source_manifest_fields",
            passed=not missing_field_artifacts,
            observed=len(missing_field_artifacts),
            expected=0,
            detail="Artifacts with missing fields: " + (", ".join(missing_field_artifacts) if missing_field_artifacts else "none"),
        ),
        GateResult(
            name="no_missing_or_unreadable_manifests",
            passed=not unreadable_artifacts,
            observed=len(unreadable_artifacts),
            expected=0,
            detail="Artifacts with missing/unreadable manifests: " + (", ".join(unreadable_artifacts) if unreadable_artifacts else "none"),
        ),
        GateResult(
            name="all_normalized_overlays_ready",
            passed=len(overlay_not_ready) == 0 and len(overlay) == len(summary),
            observed=f"{len(overlay) - len(overlay_not_ready)}/{len(overlay)}",
            expected=f"{len(summary)}/{len(summary)}",
            detail="Overlay artifacts not ready: " + (", ".join(overlay_not_ready) if overlay_not_ready else "none"),
        ),
        GateResult(
            name="no_normalizer_default_fields",
            passed=overlay_defaults == 0,
            observed=overlay_defaults,
            expected=0,
            detail="All normalized overlay values should be sourced from exact or alias fields in source manifests.",
        ),
        GateResult(
            name="remediation_is_complete_exact_only",
            passed=remediation_statuses == {"complete_exact": len(audit)},
            observed=remediation_statuses,
            expected={"complete_exact": len(audit)},
            detail="Remediation rows should not require add-field, alias-normalization or manifest recovery actions.",
        ),
    ]

    payload = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "phase19_dir": str(phase19_dir),
        "artifact_count": len(summary),
        "field_check_count": len(audit),
        "passed": all(result.passed for result in results),
        "results": [result.__dict__ for result in results],
    }
    return payload


def write_reports(payload: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "reproducibility_gate_result.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lines = [
        "# Phase 19 Reproducibility Gate Result",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Passed: {payload['passed']}",
        f"Audited artifacts: {payload['artifact_count']}",
        f"Field checks: {payload['field_check_count']}",
        "",
        "| gate | passed | observed | expected | detail |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in payload["results"]:
        detail = str(row["detail"]).replace("|", "\\|")
        lines.append(f"| {row['name']} | {row['passed']} | {row['observed']} | {row['expected']} | {detail} |")
    lines.append("")
    (output_dir / "reproducibility_gate_report.md").write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fail if Phase 19 native reproducibility coverage regresses.")
    parser.add_argument("--phase19-dir", type=Path, default=Path("outputs/phase19"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase19"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = run_gate(args.phase19_dir)
    write_reports(payload, args.output_dir)
    if not payload["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
