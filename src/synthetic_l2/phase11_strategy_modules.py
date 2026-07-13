from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def build_module_registry(paths: dict[str, Path]) -> pd.DataFrame:
    matrix = _read_csv(paths["strategy_matrix"])
    diagnostics = _read_csv(paths["signal_diagnostics"])
    availability = _read_csv(paths["feature_availability"])
    metric_req = _read_csv(paths["metric_requirements"])
    scenario_req = _read_csv(paths["scenario_requirements"])
    event_manifest = json.loads(paths["event_backtest_manifest"].read_text(encoding="utf-8"))

    diag_map = diagnostics.set_index("strategy_id").to_dict("index")
    avail_map = availability.set_index("strategy_id").to_dict("index")
    metric_counts = metric_req.groupby("strategy_id", sort=True).size().to_dict()
    scenario_counts = scenario_req.groupby("strategy_id", sort=True).size().to_dict()

    rows = []
    for record in matrix.to_dict("records"):
        sid = record["strategy_id"]
        diag = diag_map.get(sid, {})
        avail = avail_map.get(sid, {})
        if sid == "S10":
            module_type = "execution_risk_module_proxy"
            implementation_status = "implemented_proxy_non_alpha"
            evidence_path = "outputs/phase12/event_backtest_order_summary.csv"
            execution_integration = "phase12_event_backtester"
            signal_status = "not_alpha_signal"
            caveat = "Passive market-making module is execution/risk plumbing only; true queue fills are not observed."
            module_rows = int(event_manifest.get("passive_limit_orders", 0))
        elif sid == "S11":
            module_type = "risk_filter_module_proxy"
            implementation_status = "implemented_proxy_non_manipulation_label"
            evidence_path = "outputs/phase11/strategy_scenario_requirements.csv"
            execution_integration = "risk_filter_requirements_only"
            signal_status = "not_alpha_signal"
            caveat = "Spoof-like wall module is a risk-filter specification only; it does not classify manipulation or participants."
            module_rows = int(scenario_counts.get(sid, 0))
        elif record["support_level"] == "runnable_proxy":
            module_type = "signal_module_proxy"
            implementation_status = "implemented_proxy_signal_diagnostic"
            evidence_path = "outputs/phase11/strategy_signal_diagnostics.csv"
            execution_integration = "phase12_execution_summary"
            signal_status = "signal_proxy_available"
            caveat = record["caveat"]
            module_rows = int(diag.get("signal_rows", 0) or 0)
        else:
            module_type = "partial_signal_module_proxy"
            implementation_status = "implemented_proxy_with_missing_acceptance_features"
            evidence_path = "outputs/phase11/strategy_feature_availability.csv"
            execution_integration = "phase12_execution_summary"
            signal_status = "partial_signal_proxy_available"
            caveat = record["caveat"]
            module_rows = int(diag.get("signal_rows", 0) or 0)
        rows.append(
            {
                "strategy_id": sid,
                "name": record["name"],
                "role": record["role"],
                "module_type": module_type,
                "implementation_status": implementation_status,
                "support_level": record["support_level"],
                "signal_status": signal_status,
                "module_rows_or_requirements": module_rows,
                "proxy_features_present": int(avail.get("proxy_features_present", 0) or 0),
                "proxy_features_absent": int(avail.get("proxy_features_absent", 0) or 0),
                "metric_requirements": int(metric_counts.get(sid, 0)),
                "scenario_requirements": int(scenario_counts.get(sid, 0)),
                "evidence_path": evidence_path,
                "execution_integration": execution_integration,
                "acceptance_grade": False,
                "promotion_ready": False,
                "limitation": caveat,
            }
        )
    return pd.DataFrame(rows)


def build_module_coverage(registry: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {
            "coverage_check": "s01_s11_module_rows",
            "value": int(len(registry)),
            "target": 11,
            "passed": int(len(registry)) == 11,
            "evidence": "strategy_module_registry.csv",
        },
        {
            "coverage_check": "implemented_proxy_modules",
            "value": int(registry["implementation_status"].astype(str).str.startswith("implemented_proxy").sum()),
            "target": 11,
            "passed": int(registry["implementation_status"].astype(str).str.startswith("implemented_proxy").sum()) == 11,
            "evidence": "strategy_module_registry.csv",
        },
        {
            "coverage_check": "acceptance_grade_modules",
            "value": int(registry["acceptance_grade"].astype(bool).sum()),
            "target": 0,
            "passed": int(registry["acceptance_grade"].astype(bool).sum()) == 0,
            "evidence": "strategy_module_registry.csv",
        },
        {
            "coverage_check": "promotion_ready_modules",
            "value": int(registry["promotion_ready"].astype(bool).sum()),
            "target": 0,
            "passed": int(registry["promotion_ready"].astype(bool).sum()) == 0,
            "evidence": "strategy_module_registry.csv",
        },
        {
            "coverage_check": "non_alpha_or_risk_modules",
            "value": int(registry["module_type"].isin(["execution_risk_module_proxy", "risk_filter_module_proxy"]).sum()),
            "target": 2,
            "passed": int(registry["module_type"].isin(["execution_risk_module_proxy", "risk_filter_module_proxy"]).sum()) == 2,
            "evidence": "S10/S11 module_type rows",
        },
    ]
    return pd.DataFrame(rows)


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


def write_report(output_dir: Path, registry: pd.DataFrame, coverage: pd.DataFrame) -> None:
    status_summary = registry.groupby(["module_type", "implementation_status"], sort=True).size().reset_index(name="modules")
    lines = [
        "# Phase 11 Strategy Module Registry Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This artifact converts S01-S11 from strategy concepts into explicit module registry rows.",
        "It does not promote or accept any strategy. S10 is an execution/risk module proxy, and S11 is a risk-filter specification that must not be interpreted as manipulation detection.",
        "",
        "## Coverage",
        "",
        _markdown_table(coverage),
        "",
        "## Status Summary",
        "",
        _markdown_table(status_summary),
        "",
        "## Module Registry",
        "",
        _markdown_table(registry),
        "",
    ]
    (output_dir / "strategy_module_registry_report.md").write_text("\n".join(lines), encoding="utf-8")


def run(output_dir: Path, paths: dict[str, Path]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    registry = build_module_registry(paths)
    coverage = build_module_coverage(registry)
    registry_path = output_dir / "strategy_module_registry.csv"
    coverage_path = output_dir / "strategy_module_coverage.csv"
    report_path = output_dir / "strategy_module_registry_report.md"
    registry.to_csv(registry_path, index=False)
    coverage.to_csv(coverage_path, index=False)
    inputs = {key: str(value) for key, value in paths.items()}
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "inputs": inputs,
        "modules": int(len(registry)),
        "implemented_proxy_modules": int(registry["implementation_status"].astype(str).str.startswith("implemented_proxy").sum()),
        "acceptance_grade_modules": int(registry["acceptance_grade"].astype(bool).sum()),
        "promotion_ready_modules": int(registry["promotion_ready"].astype(bool).sum()),
        "non_alpha_or_risk_modules": int(registry["module_type"].isin(["execution_risk_module_proxy", "risk_filter_module_proxy"]).sum()),
        "scope": "s01_s11_strategy_module_registry_not_promotion_evidence",
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase11_strategy_modules",
            generated_utc=generated_utc,
            inputs=inputs,
            parameters={"registry_scope": manifest["scope"]},
            outputs={
                "registry": str(registry_path),
                "coverage": str(coverage_path),
                "report": str(report_path),
            },
            scenario_ids="outputs/phase11/strategy_scenario_requirements.csv",
            cost_model_version="phase12_event_backtest_cost_model_if_execution_module_else_not_applicable",
            latency_model_version="phase12_event_backtest_latency_model_if_execution_module_else_not_applicable",
        )
    )
    (output_dir / "strategy_module_registry_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, registry, coverage)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 11 S01-S11 strategy module registry artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase11"))
    parser.add_argument("--strategy-matrix", type=Path, default=Path("outputs/phase11/strategy_validation_matrix.csv"))
    parser.add_argument("--signal-diagnostics", type=Path, default=Path("outputs/phase11/strategy_signal_diagnostics.csv"))
    parser.add_argument("--feature-availability", type=Path, default=Path("outputs/phase11/strategy_feature_availability.csv"))
    parser.add_argument("--metric-requirements", type=Path, default=Path("outputs/phase11/strategy_metric_requirements.csv"))
    parser.add_argument("--scenario-requirements", type=Path, default=Path("outputs/phase11/strategy_scenario_requirements.csv"))
    parser.add_argument("--event-backtest-manifest", type=Path, default=Path("outputs/phase12/event_backtest_manifest.json"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "strategy_matrix": args.strategy_matrix,
        "signal_diagnostics": args.signal_diagnostics,
        "feature_availability": args.feature_availability,
        "metric_requirements": args.metric_requirements,
        "scenario_requirements": args.scenario_requirements,
        "event_backtest_manifest": args.event_backtest_manifest,
    }
    run(args.output_dir, paths)


if __name__ == "__main__":
    main()
