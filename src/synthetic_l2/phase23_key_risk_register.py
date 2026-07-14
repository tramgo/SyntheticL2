from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


RISK_DEFINITIONS = [
    {
        "risk_id": "R23_01_synthetic_alpha",
        "risk_title": "Synthetic alpha",
        "risk_description": "The generator may accidentally encode a predictable relationship that strategies exploit.",
        "risk_category": "model_artifact",
        "plan_mitigations": [
            "negative-control generators",
            "multiple model families",
            "hidden holdout generator",
            "parameter perturbation",
            "real-data paper testing",
            "generator-blind strategy development",
        ],
    },
    {
        "risk_id": "R23_02_one_day_overfitting",
        "risk_title": "One-day overfitting",
        "risk_description": "The sample day may be unusual.",
        "risk_category": "data_coverage",
        "plan_mitigations": [
            "pooled shrinkage",
            "broad stress ranges",
            "explicit uncertainty bands",
            "multiple synthetic normal-day configurations",
            "immediate recalibration with new real days",
        ],
    },
    {
        "risk_id": "R23_03_unrealistic_fills",
        "risk_title": "Unrealistic fills",
        "risk_description": "Execution assumptions may overstate attainable fills and understate adverse selection.",
        "risk_category": "execution_model",
        "plan_mitigations": [
            "pessimistic execution",
            "marketable-order focus initially",
            "latency simulation",
            "partial fills",
            "depth walk",
            "adverse-selection modelling",
        ],
    },
    {
        "risk_id": "R23_04_excessive_data_volume",
        "risk_title": "Excessive data volume",
        "risk_description": "Raw and synthetic L2 data volume may make repeated experiments slow or costly.",
        "risk_category": "storage_compute",
        "plan_mitigations": [
            "event-driven generation",
            "integer encoding",
            "Parquet/Zstandard",
            "delta-state representation",
            "separate raw and feature tiers",
            "selected dense tickers",
            "feature-only datasets for repeated experiments",
        ],
    },
    {
        "risk_id": "R23_05_false_confidence_three_months",
        "risk_title": "False confidence from three months",
        "risk_description": "Three synthetic months are a screening laboratory, not a profitability proof.",
        "risk_category": "governance",
        "plan_mitigations": [
            "synthetic engineering test",
            "synthetic multi-regime stress test",
            "real-data historical test",
            "live paper trading",
            "shadow execution",
            "very small capital",
            "gradual scale-up",
        ],
    },
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


def _summary_value(summary: pd.DataFrame, metric: str, default: int = 0) -> int:
    row = summary.loc[summary["metric"].eq(metric), "value"]
    if row.empty:
        return default
    return int(pd.to_numeric(row, errors="coerce").fillna(default).iloc[0])


def load_evidence(paths: dict[str, Path]) -> dict[str, int | str]:
    robustness_gap = pd.read_csv(paths["robustness_gap"])
    realism_gap = pd.read_csv(paths["realism_gap"])
    predictive_gap = pd.read_csv(paths["predictive_gap"])
    economic_gap = pd.read_csv(paths["economic_gap"])
    risk_readiness = pd.read_csv(paths["risk_acceptance_readiness"])
    execution_milestones = pd.read_csv(paths["execution_milestones"])
    phase21_summary = pd.read_csv(paths["phase21_decision_summary"])
    phase22_summary = pd.read_csv(paths["phase22_summary"])
    duckdb_report = Path(paths["duckdb_report"])
    phase10_size = pd.read_csv(paths["phase10_size_estimates"])

    return {
        "negative_control_open_rows": int(
            len(robustness_gap.loc[robustness_gap["robustness_requirement"].astype(str).eq("negative_control_rejection")])
        ),
        "holdout_strategy_open_rows": int(
            len(realism_gap.loc[realism_gap["realism_requirement"].astype(str).isin(["holdout_strategy_rerun", "artifact_exploitation_rejection"])])
        ),
        "predictive_open_rows": int((~predictive_gap["acceptance_requirement_met"].astype(bool)).sum()),
        "economic_open_rows": int((~economic_gap["acceptance_requirement_met"].astype(bool)).sum()),
        "risk_open_rows": int((~risk_readiness["acceptance_requirement_met"].astype(bool)).sum()),
        "phase20_acceptance_ready_rows": int(execution_milestones["acceptance_ready_rows"].sum()),
        "phase21_extension_or_paper_ready": _summary_value(phase21_summary, "extension_or_paper_ready"),
        "phase22_class_b_event_grade_days": _summary_value(phase22_summary, "class_b_event_grade_days"),
        "phase22_ready_recalibration_tasks": _summary_value(phase22_summary, "ready_recalibration_tasks"),
        "duckdb_report_present": str(duckdb_report.exists()),
        "full_year_conservative_total_gb": float(
            pd.to_numeric(
                phase10_size.loc[
                    phase10_size["profile"].astype(str).str.lower().eq("full"),
                    "conservative_total_gb",
                ],
                errors="coerce",
            )
            .fillna(0.0)
            .iloc[0]
        ),
    }


def build_risk_register(evidence: dict[str, int | str]) -> pd.DataFrame:
    rows = []
    for risk in RISK_DEFINITIONS:
        risk_id = risk["risk_id"]
        if risk_id == "R23_01_synthetic_alpha":
            current_status = "open_controls_proxy_only"
            severity = "high"
            observed = (
                f"negative_control_open_rows={evidence['negative_control_open_rows']}; "
                f"holdout_or_artifact_open_rows={evidence['holdout_strategy_open_rows']}; "
                f"phase21_extension_or_paper_ready={evidence['phase21_extension_or_paper_ready']}"
            )
            next_action = "Run acceptance-grade negative controls, holdout-generator strategy reruns and real-data paper tests before promotion."
        elif risk_id == "R23_02_one_day_overfitting":
            current_status = "open_until_multiday_class_b_capture"
            severity = "high"
            observed = (
                f"class_b_event_grade_days={evidence['phase22_class_b_event_grade_days']}; "
                f"ready_recalibration_tasks={evidence['phase22_ready_recalibration_tasks']}"
            )
            next_action = "Collect Class B event-grade multi-day data and rerun Phase 22 recalibration tasks."
        elif risk_id == "R23_03_unrealistic_fills":
            current_status = "open_until_broker_reconciled_lifecycle"
            severity = "high"
            observed = (
                f"risk_open_rows={evidence['risk_open_rows']}; "
                f"economic_open_rows={evidence['economic_open_rows']}"
            )
            next_action = "Run broker/exchange fill provenance, contract-note reconciliation and full lifecycle execution replay."
        elif risk_id == "R23_04_excessive_data_volume":
            current_status = "mitigated_by_current_storage_design_monitor"
            severity = "medium"
            observed = (
                f"duckdb_report_present={evidence['duckdb_report_present']}; "
                f"full_year_conservative_total_gb={evidence['full_year_conservative_total_gb']:.3f}"
            )
            next_action = "Keep Parquet/Zstandard durable storage and DuckDB query layer; re-estimate before materializing larger horizons."
        else:
            current_status = "open_governance_gate"
            severity = "high"
            observed = (
                f"phase20_acceptance_ready_rows={evidence['phase20_acceptance_ready_rows']}; "
                f"phase21_extension_or_paper_ready={evidence['phase21_extension_or_paper_ready']}"
            )
            next_action = "Preserve staged promotion path; do not skip from synthetic screening to capital deployment."
        rows.append(
            {
                "risk_id": risk_id,
                "risk_title": risk["risk_title"],
                "risk_category": risk["risk_category"],
                "risk_description": risk["risk_description"],
                "severity": severity,
                "current_status": current_status,
                "observed_value": observed,
                "plan_mitigations": "; ".join(risk["plan_mitigations"]),
                "required_next_action": next_action,
                "acceptance_blocking": True,
            }
        )
    return pd.DataFrame(rows)


def build_mitigation_ledger(risk_register: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for risk in RISK_DEFINITIONS:
        status = str(risk_register.loc[risk_register["risk_id"].eq(risk["risk_id"]), "current_status"].iloc[0])
        for rank, mitigation in enumerate(risk["plan_mitigations"], start=1):
            if "monitor" in status and risk["risk_id"] == "R23_04_excessive_data_volume":
                mitigation_status = "implemented_or_monitored_currently"
            else:
                mitigation_status = "required_before_acceptance"
            rows.append(
                {
                    "risk_id": risk["risk_id"],
                    "mitigation_rank": rank,
                    "mitigation": mitigation,
                    "mitigation_status": mitigation_status,
                    "current_evidence_status": status,
                }
            )
    return pd.DataFrame(rows)


def build_promotion_path() -> pd.DataFrame:
    steps = [
        ("P23_01", 1, "Synthetic engineering test", "current_proxy_running"),
        ("P23_02", 2, "Synthetic multi-regime stress test", "proxy_partial_not_acceptance"),
        ("P23_03", 3, "Real-data historical test", "blocked_missing_class_b_multiday"),
        ("P23_04", 4, "Live paper trading", "blocked_until_historical_acceptance"),
        ("P23_05", 5, "Shadow execution", "blocked_until_paper_trading"),
        ("P23_06", 6, "Very small capital", "blocked_until_shadow_execution"),
        ("P23_07", 7, "Gradual scale-up", "blocked_until_small_capital_risk_limits"),
    ]
    return pd.DataFrame(
        [
            {
                "promotion_step_id": step_id,
                "promotion_order": order,
                "promotion_step": step,
                "current_status": status,
                "skip_allowed": False,
            }
            for step_id, order, step, status in steps
        ]
    )


def build_summary(risk_register: pd.DataFrame, mitigation_ledger: pd.DataFrame, promotion_path: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"metric": "phase23_risks", "value": int(len(risk_register)), "description": "Key risk rows from the plan"},
            {
                "metric": "phase23_high_risks",
                "value": int((risk_register["severity"].astype(str) == "high").sum()),
                "description": "High-severity risk rows",
            },
            {
                "metric": "phase23_open_acceptance_blocking_risks",
                "value": int(risk_register["acceptance_blocking"].astype(bool).sum()),
                "description": "Risks still blocking acceptance or promotion",
            },
            {"metric": "phase23_mitigation_rows", "value": int(len(mitigation_ledger)), "description": "Mitigation ledger rows"},
            {"metric": "phase23_promotion_steps", "value": int(len(promotion_path)), "description": "Governed promotion path steps"},
            {"metric": "phase23_promotion_ready", "value": 0, "description": "No strategy is ready to advance beyond synthetic screening"},
        ]
    )


def write_report(output_dir: Path, summary: pd.DataFrame, risk_register: pd.DataFrame, mitigation_ledger: pd.DataFrame, promotion_path: pd.DataFrame) -> None:
    lines = [
        "# Phase 23 Key Risk Register",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This register converts the plan's key-risk section into auditable current-state controls.",
        "It is a governance artifact, not strategy-promotion evidence.",
        "",
        "## Summary",
        "",
        _markdown_table(summary),
        "",
        "## Risk Register",
        "",
        _markdown_table(risk_register),
        "",
        "## Mitigation Ledger",
        "",
        _markdown_table(mitigation_ledger),
        "",
        "## Promotion Path Guardrail",
        "",
        _markdown_table(promotion_path),
        "",
    ]
    (output_dir / "phase23_key_risk_register_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase23(paths: dict[str, Path], output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    evidence = load_evidence(paths)
    risk_register = build_risk_register(evidence)
    mitigation_ledger = build_mitigation_ledger(risk_register)
    promotion_path = build_promotion_path()
    summary = build_summary(risk_register, mitigation_ledger, promotion_path)

    risk_register.to_csv(output_dir / "key_risk_register.csv", index=False)
    mitigation_ledger.to_csv(output_dir / "risk_mitigation_ledger.csv", index=False)
    promotion_path.to_csv(output_dir / "promotion_path_guardrail.csv", index=False)
    summary.to_csv(output_dir / "key_risk_summary.csv", index=False)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "risk_rows": int(len(risk_register)),
        "mitigation_rows": int(len(mitigation_ledger)),
        "promotion_steps": int(len(promotion_path)),
        "scope": "phase23_key_risk_register_not_promotion_evidence",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase23",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={"risk_definitions": RISK_DEFINITIONS},
            outputs={
                "risk_register": str(output_dir / "key_risk_register.csv"),
                "mitigation_ledger": str(output_dir / "risk_mitigation_ledger.csv"),
                "promotion_path": str(output_dir / "promotion_path_guardrail.csv"),
                "summary": str(output_dir / "key_risk_summary.csv"),
                "report": str(output_dir / "phase23_key_risk_register_report.md"),
                "manifest": str(output_dir / "phase23_key_risk_register_manifest.json"),
            },
            random_seed="not_applicable_risk_register",
            scenario_ids="phase23_key_risk_governance_current_workspace",
            cost_model_version="phase12_phase16_phase20_m05_cost_and_economic_risk_evidence",
            latency_model_version="phase8_phase12_phase20_m05_latency_and_execution_risk_evidence",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase23_key_risk_register_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, summary, risk_register, mitigation_ledger, promotion_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 23 key risk register artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase23"))
    parser.add_argument("--robustness-gap", type=Path, default=Path("outputs/phase13/robustness_acceptance_gap_ledger.csv"))
    parser.add_argument("--realism-gap", type=Path, default=Path("outputs/phase14/realism_acceptance_gap_ledger.csv"))
    parser.add_argument("--predictive-gap", type=Path, default=Path("outputs/phase16/predictive_acceptance_gap_ledger.csv"))
    parser.add_argument("--economic-gap", type=Path, default=Path("outputs/phase16/economic_acceptance_gap_ledger.csv"))
    parser.add_argument("--risk-acceptance-readiness", type=Path, default=Path("outputs/phase12/full_run_risk_acceptance_readiness.csv"))
    parser.add_argument("--execution-milestones", type=Path, default=Path("outputs/phase20/acceptance_execution_milestones.csv"))
    parser.add_argument("--phase21-decision-summary", type=Path, default=Path("outputs/phase21/decision_summary.csv"))
    parser.add_argument("--phase22-summary", type=Path, default=Path("outputs/phase22/real_data_integration_summary.csv"))
    parser.add_argument("--duckdb-report", type=Path, default=Path("outputs/duckdb/duckdb_workspace_report.md"))
    parser.add_argument("--phase10-size-estimates", type=Path, default=Path("outputs/phase10/size_estimates.csv"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "robustness_gap": args.robustness_gap,
        "realism_gap": args.realism_gap,
        "predictive_gap": args.predictive_gap,
        "economic_gap": args.economic_gap,
        "risk_acceptance_readiness": args.risk_acceptance_readiness,
        "execution_milestones": args.execution_milestones,
        "phase21_decision_summary": args.phase21_decision_summary,
        "phase22_summary": args.phase22_summary,
        "duckdb_report": args.duckdb_report,
        "phase10_size_estimates": args.phase10_size_estimates,
    }
    run_phase23(paths, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
