from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


STAGE_E_CRITERIA = [
    ("synthetic_quality_gates_pass", "Synthetic quality gates pass without warning/failure.", "phase14_fail_rows == 0 and phase14_warn_rows == 0"),
    ("backtest_controls_pass", "Backtest controls and promotion gates pass for at least one candidate.", "promoted_strategies > 0 and acceptance_blockers == 0"),
    ("storage_is_acceptable", "Full-year storage estimate is within current research workstation/cloud budget.", "full_year_conservative_total_gb <= 150"),
    ("strategy_code_is_stable", "Strategy modules are acceptance-grade and promotion-ready where applicable.", "promotion_ready_modules > 0 and acceptance_grade_modules > 0"),
    ("results_not_generator_artifacts", "Results survive anti-artifact checks, holdout reruns and real-data validation.", "predictive_candidates > 0 and real_or_holdout_gaps_open == 0"),
    ("full_year_extension_allowed", "Full-year extension can start only after every prerequisite passes.", "all prerequisites pass"),
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


def build_criteria() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "criterion_id": criterion_id,
                "criterion_description": description,
                "acceptance_threshold": threshold,
                "current_status": "stage_e_readiness_gate_not_extension_run",
            }
            for criterion_id, description, threshold in STAGE_E_CRITERIA
        ]
    )


def _full_year_storage_row(size_estimates: pd.DataFrame) -> pd.Series:
    candidates = size_estimates[size_estimates["profile"].astype(str).str.lower().eq("full")]
    if candidates.empty:
        candidates = size_estimates[size_estimates["trading_days"].astype(int) >= 252]
    if candidates.empty:
        raise ValueError("No full-year storage estimate row found.")
    return candidates.iloc[0]


def build_prerequisite_ledger(paths: dict[str, Path]) -> pd.DataFrame:
    quality = pd.read_csv(paths["quality_gate_summary"])
    acceptance = pd.read_csv(paths["strategy_acceptance_summary"])
    blockers = pd.read_csv(paths["acceptance_blockers"])
    size_estimates = pd.read_csv(paths["size_estimates"])
    modules = pd.read_csv(paths["strategy_module_registry"])
    predictive = pd.read_csv(paths["predictive_promotion_falsification"])
    economic_gap = pd.read_csv(paths["economic_acceptance_gap"])
    robustness_gap = pd.read_csv(paths["robustness_acceptance_gap"])
    stage_d = pd.read_csv(paths["stage_d_check_ledger"])

    full = _full_year_storage_row(size_estimates)
    quality_fail = int((quality["status"].astype(str) == "fail").sum())
    quality_warn = int((quality["status"].astype(str) == "warn").sum())
    promoted = int(acceptance["promotion_allowed"].astype(bool).sum())
    blocker_rows = int(len(blockers))
    conservative_gb = float(full["conservative_total_gb"])
    promotion_ready_modules = int(modules["promotion_ready"].astype(bool).sum())
    acceptance_grade_modules = int(modules["acceptance_grade"].astype(bool).sum())
    predictive_candidates = int(predictive["predictive_promotion_candidate_proxy"].astype(bool).sum())
    economic_open = int((~economic_gap["acceptance_requirement_met"].astype(bool)).sum())
    robustness_open = int((~robustness_gap["acceptance_requirement_met"].astype(bool)).sum())
    stage_d_passed = bool(stage_d["passed"].astype(bool).all())

    rows = [
        {
            "prerequisite_id": "synthetic_quality_gates_pass",
            "observed_value": f"fail_rows={quality_fail}; warn_rows={quality_warn}",
            "passes": bool(quality_fail == 0 and quality_warn == 0),
            "evidence_source": str(paths["quality_gate_summary"]),
            "blocking_gap": "" if quality_fail == 0 and quality_warn == 0 else "Synthetic quality warnings/failures remain.",
            "required_next_action": "Keep quality gate green while later extension inputs change.",
        },
        {
            "prerequisite_id": "backtest_controls_pass",
            "observed_value": f"promoted_strategies={promoted}; acceptance_blockers={blocker_rows}",
            "passes": bool(promoted > 0 and blocker_rows == 0),
            "evidence_source": f"{paths['strategy_acceptance_summary']}; {paths['acceptance_blockers']}",
            "blocking_gap": "No strategy is promoted and acceptance blockers remain.",
            "required_next_action": "Clear predictive, economic, robustness, risk and realism acceptance blockers before full-year run.",
        },
        {
            "prerequisite_id": "storage_is_acceptable",
            "observed_value": f"full_year_conservative_total_gb={conservative_gb:.3f}",
            "passes": bool(conservative_gb <= 150.0),
            "evidence_source": str(paths["size_estimates"]),
            "blocking_gap": "" if conservative_gb <= 150.0 else "Full-year conservative storage estimate exceeds threshold.",
            "required_next_action": "Reconfirm storage budget before materializing full-year raw/compact/features.",
        },
        {
            "prerequisite_id": "strategy_code_is_stable",
            "observed_value": f"promotion_ready_modules={promotion_ready_modules}; acceptance_grade_modules={acceptance_grade_modules}",
            "passes": bool(promotion_ready_modules > 0 and acceptance_grade_modules > 0),
            "evidence_source": str(paths["strategy_module_registry"]),
            "blocking_gap": "No strategy module is promotion-ready or acceptance-grade.",
            "required_next_action": "Upgrade strategy modules from proxy diagnostics to acceptance-grade implementations.",
        },
        {
            "prerequisite_id": "results_not_generator_artifacts",
            "observed_value": f"predictive_candidates={predictive_candidates}; economic_open={economic_open}; robustness_open={robustness_open}",
            "passes": bool(predictive_candidates > 0 and economic_open == 0 and robustness_open == 0),
            "evidence_source": f"{paths['predictive_promotion_falsification']}; {paths['economic_acceptance_gap']}; {paths['robustness_acceptance_gap']}",
            "blocking_gap": "No predictive promotion candidates exist and economic/robustness acceptance gaps remain open.",
            "required_next_action": "Run holdout-generator, walk-forward, full-seed and real-data reruns before treating results as non-artifact.",
        },
        {
            "prerequisite_id": "stage_d_three_month_proxy_available",
            "observed_value": f"stage_d_all_checks_pass={stage_d_passed}",
            "passes": stage_d_passed,
            "evidence_source": str(paths["stage_d_check_ledger"]),
            "blocking_gap": "" if stage_d_passed else "Stage D proxy checks are not all passing.",
            "required_next_action": "Use Stage D as proxy input only; do not treat it as acceptance evidence.",
        },
    ]
    ledger = pd.DataFrame(rows)
    extension_allowed = bool(ledger.loc[ledger["prerequisite_id"].ne("stage_d_three_month_proxy_available"), "passes"].all())
    ledger = pd.concat(
        [
            ledger,
            pd.DataFrame(
                [
                    {
                        "prerequisite_id": "full_year_extension_allowed",
                        "observed_value": f"extension_allowed={extension_allowed}",
                        "passes": extension_allowed,
                        "evidence_source": "stage_e_prerequisite_ledger",
                        "blocking_gap": "" if extension_allowed else "One or more mandatory Stage E prerequisites are not satisfied.",
                        "required_next_action": "Do not run full-year extension until all mandatory prerequisites pass.",
                    }
                ]
            ),
        ],
        ignore_index=True,
    )
    return ledger


def build_gap_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    return (
        ledger.groupby(["passes"], sort=True)
        .size()
        .reset_index(name="rows")
        .assign(scope="stage_e_full_year_readiness")
    )


def build_action_plan(ledger: pd.DataFrame) -> pd.DataFrame:
    open_rows = ledger[~ledger["passes"].astype(bool)].copy()
    open_rows["priority_rank"] = range(1, len(open_rows) + 1)
    return open_rows[["priority_rank", "prerequisite_id", "blocking_gap", "required_next_action", "evidence_source"]]


def write_report(output_dir: Path, criteria: pd.DataFrame, ledger: pd.DataFrame, gap_summary: pd.DataFrame, action_plan: pd.DataFrame) -> None:
    lines = [
        "# Stage E Full-Year Extension Readiness",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This gate checks whether the plan permits a full-year extension. It does not run the full-year extension.",
        "Current evidence must pass quality, backtest/control, storage, strategy-code-stability and anti-generator-artifact prerequisites before Stage E can start.",
        "",
        "## Criteria",
        "",
        _markdown_table(criteria),
        "",
        "## Prerequisite Ledger",
        "",
        _markdown_table(ledger),
        "",
        "## Gap Summary",
        "",
        _markdown_table(gap_summary),
        "",
        "## Required Action Plan",
        "",
        _markdown_table(action_plan),
        "",
    ]
    (output_dir / "stage_e_full_year_readiness_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_stage_e(paths: dict[str, Path], output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    criteria = build_criteria()
    ledger = build_prerequisite_ledger(paths)
    gap_summary = build_gap_summary(ledger)
    action_plan = build_action_plan(ledger)
    criteria.to_csv(output_dir / "stage_e_readiness_criteria.csv", index=False)
    ledger.to_csv(output_dir / "stage_e_prerequisite_ledger.csv", index=False)
    gap_summary.to_csv(output_dir / "stage_e_gap_summary.csv", index=False)
    action_plan.to_csv(output_dir / "stage_e_required_action_plan.csv", index=False)
    generated_utc = datetime.now(timezone.utc).isoformat()
    extension_allowed = bool(ledger.loc[ledger["prerequisite_id"].eq("full_year_extension_allowed"), "passes"].iloc[0])
    manifest = {
        "generated_utc": generated_utc,
        "extension_allowed": extension_allowed,
        "prerequisite_rows": int(len(ledger)),
        "passing_prerequisite_rows": int(ledger["passes"].astype(bool).sum()),
        "blocking_prerequisite_rows": int((~ledger["passes"].astype(bool)).sum()),
        "scope": "stage_e_full_year_extension_readiness_not_extension_run",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="stage_e",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={"stage_e_storage_threshold_conservative_gb": 150.0},
            outputs={
                "criteria": str(output_dir / "stage_e_readiness_criteria.csv"),
                "prerequisite_ledger": str(output_dir / "stage_e_prerequisite_ledger.csv"),
                "gap_summary": str(output_dir / "stage_e_gap_summary.csv"),
                "required_action_plan": str(output_dir / "stage_e_required_action_plan.csv"),
                "report": str(output_dir / "stage_e_full_year_readiness_report.md"),
                "manifest": str(output_dir / "stage_e_full_year_readiness_manifest.json"),
            },
            random_seed="not_applicable_readiness_gate",
            scenario_ids="not_applicable_no_scenario_generation",
            cost_model_version="phase12_phase16_proxy_cost_evidence_not_acceptance",
            latency_model_version="phase12_phase16_proxy_latency_evidence_not_acceptance",
            base_dir=base_dir,
        )
    )
    (output_dir / "stage_e_full_year_readiness_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, criteria, ledger, gap_summary, action_plan)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Stage E full-year extension readiness artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/stage_e"))
    parser.add_argument("--quality-gate-summary", type=Path, default=Path("outputs/phase14/quality_gate_summary.csv"))
    parser.add_argument("--strategy-acceptance-summary", type=Path, default=Path("outputs/phase15/strategy_acceptance_summary.csv"))
    parser.add_argument("--acceptance-blockers", type=Path, default=Path("outputs/phase15/acceptance_blockers.csv"))
    parser.add_argument("--size-estimates", type=Path, default=Path("outputs/phase10/size_estimates.csv"))
    parser.add_argument("--strategy-module-registry", type=Path, default=Path("outputs/phase11/strategy_module_registry.csv"))
    parser.add_argument("--predictive-promotion-falsification", type=Path, default=Path("outputs/phase16/predictive_promotion_falsification.csv"))
    parser.add_argument("--economic-acceptance-gap", type=Path, default=Path("outputs/phase16/economic_acceptance_gap_ledger.csv"))
    parser.add_argument("--robustness-acceptance-gap", type=Path, default=Path("outputs/phase13/robustness_acceptance_gap_ledger.csv"))
    parser.add_argument("--stage-d-check-ledger", type=Path, default=Path("outputs/stage_d/stage_d_check_ledger.csv"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "quality_gate_summary": args.quality_gate_summary,
        "strategy_acceptance_summary": args.strategy_acceptance_summary,
        "acceptance_blockers": args.acceptance_blockers,
        "size_estimates": args.size_estimates,
        "strategy_module_registry": args.strategy_module_registry,
        "predictive_promotion_falsification": args.predictive_promotion_falsification,
        "economic_acceptance_gap": args.economic_acceptance_gap,
        "robustness_acceptance_gap": args.robustness_acceptance_gap,
        "stage_d_check_ledger": args.stage_d_check_ledger,
    }
    run_stage_e(paths, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
