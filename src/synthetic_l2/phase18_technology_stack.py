from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


STACK_DECISIONS = [
    ("Language", "Python", "adopted", "Current pipeline is Python scripts/modules."),
    ("DataFrame engine", "Pandas", "adopted_now", "Used for summaries and moderate-size CSV/Parquet operations."),
    ("DataFrame engine", "PyArrow", "adopted_now", "Used for Parquet IO and schema handling."),
    ("DataFrame engine", "Polars", "optional_later", "Useful for larger scans; not required by current pipeline."),
    ("Storage", "Parquet + Zstandard", "adopted", "Durable data products are Parquet with compression."),
    ("Query", "DuckDB", "adopted", "Local analytical layer over Parquet/CSV outputs."),
    ("Numerical work", "NumPy", "adopted", "Used by generation and simulation phases."),
    ("Numerical work", "SciPy", "optional_later", "Useful for richer distribution fitting; not required by current scripts."),
    ("Statistical models", "statsmodels", "optional_later", "Needed only for formal statistical modeling phases."),
    ("Statistical models", "scikit-learn", "optional_later", "Needed for discriminator/model validation beyond current proxies."),
    ("Tree models", "LightGBM/XGBoost", "defer", "Do not add until acceptance experiments require tree models."),
    ("Configuration", "JSON/YAML + Pydantic optional", "partial_current", "Current outputs use JSON manifests; schema validation can be added later."),
    ("Experiment tracking", "Structured local metadata", "adopted_now", "Current manifests and registries are local structured metadata."),
    ("Experiment tracking", "MLflow", "defer", "Avoid until experiment volume requires a tracking server or richer UI."),
    ("Parallel generation", "multiprocessing", "optional_later", "Use only after single-machine bottlenecks are measured."),
    ("Parallel generation", "Ray/Dask", "defer", "Avoid distributed infrastructure before local limits are measured."),
    ("Testing", "pytest", "recommended_next", "Add formal tests around phase invariants and generators."),
    ("Testing", "hypothesis", "optional_later", "Property-based tests are useful for book/price invariants."),
    ("Visualization", "Matplotlib", "optional_later", "Useful for static reports."),
    ("Visualization", "Plotly", "optional_later", "Useful for interactive dashboard once Phase 17 WP10 dashboard starts."),
    ("Versioning", "Git + data manifests + generator hashes", "partial_current", "Data manifests exist; this folder is not currently a Git repo."),
]


DEPENDENCIES = [
    ("python", "executable", "required_now"),
    ("pandas", "python_module", "required_now"),
    ("numpy", "python_module", "required_now"),
    ("pyarrow", "python_module", "required_now"),
    ("duckdb", "python_module", "required_now"),
    ("scipy", "python_module", "optional_later"),
    ("sklearn", "python_module", "optional_later"),
    ("statsmodels", "python_module", "optional_later"),
    ("polars", "python_module", "optional_later"),
    ("pydantic", "python_module", "optional_later"),
    ("pytest", "python_module", "recommended_next"),
    ("hypothesis", "python_module", "optional_later"),
    ("matplotlib", "python_module", "optional_later"),
    ("plotly", "python_module", "optional_later"),
    ("git", "executable", "recommended_next"),
]


def stack_decisions() -> pd.DataFrame:
    return pd.DataFrame(
        STACK_DECISIONS,
        columns=["component", "selected_option", "decision_status", "rationale"],
    )


def dependency_availability() -> pd.DataFrame:
    rows = []
    for name, dependency_type, requirement_status in DEPENDENCIES:
        if dependency_type == "python_module":
            available = importlib.util.find_spec(name) is not None
            evidence = "importlib.find_spec"
        else:
            available = shutil.which(name) is not None
            evidence = "shutil.which"
        rows.append(
            {
                "dependency": name,
                "dependency_type": dependency_type,
                "requirement_status": requirement_status,
                "available_now": available,
                "evidence_method": evidence,
                "action": _dependency_action(name, requirement_status, available),
            }
        )
    return pd.DataFrame(rows)


def _dependency_action(name: str, requirement_status: str, available: bool) -> str:
    if available:
        return "no_action"
    if requirement_status == "required_now":
        return f"install_or_fix_required_dependency:{name}"
    if requirement_status == "recommended_next":
        return f"install_when_adding_tests_or_versioning:{name}"
    return "defer_until_needed"


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


def write_report(output_dir: Path, decisions: pd.DataFrame, availability: pd.DataFrame) -> None:
    decision_summary = decisions.groupby("decision_status", sort=True).size().reset_index(name="items")
    availability_summary = availability.groupby(["requirement_status", "available_now"], sort=True).size().reset_index(name="dependencies")
    missing_now = availability[(availability["requirement_status"] == "required_now") & (~availability["available_now"])]
    lines = [
        "# Phase 18 Technology Stack Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase records the working technology-stack decision and checks local availability of required/optional dependencies.",
        "The current direction remains single-machine Python, Parquet/Zstandard and DuckDB. Distributed tools are deferred until measured local limits require them.",
        "",
        "## Decision Summary",
        "",
        _markdown_table(decision_summary),
        "",
        "## Dependency Availability Summary",
        "",
        _markdown_table(availability_summary),
        "",
        "## Missing Required Dependencies",
        "",
        _markdown_table(missing_now),
        "",
        "## Stack Decisions",
        "",
        _markdown_table(decisions),
        "",
    ]
    (output_dir / "phase18_technology_stack_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase18(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    decisions = stack_decisions()
    availability = dependency_availability()
    decisions.to_csv(output_dir / "stack_decisions.csv", index=False)
    availability.to_csv(output_dir / "dependency_availability.csv", index=False)
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "stack_decision_rows": int(len(decisions)),
        "dependency_rows": int(len(availability)),
        "required_now_dependencies": int((availability["requirement_status"] == "required_now").sum()),
        "missing_required_now_dependencies": int(((availability["requirement_status"] == "required_now") & (~availability["available_now"])).sum()),
        "deferred_or_optional_items": int(decisions["decision_status"].isin(["optional_later", "defer"]).sum()),
        "scope": "phase18_technology_stack_decisions_and_local_availability",
    }
    (output_dir / "technology_stack_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, decisions, availability)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 18 technology stack decision artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase18"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase18(args.output_dir)


if __name__ == "__main__":
    main()
