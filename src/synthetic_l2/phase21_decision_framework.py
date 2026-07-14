from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


DECISION_RULES = [
    (
        "D21_01_no_strategy_survives_costs_latency",
        "No strategy survives costs and latency",
        "Improve or reject strategies; do not tune generator to create profit",
    ),
    (
        "D21_02_only_price_baselines_work",
        "Only price baselines work",
        "L2 adds insufficient value under tested assumptions",
    ),
    (
        "D21_03_l2_improves_modestly_robustly",
        "L2 improves baseline modestly and robustly",
        "Continue collecting real data and extend synthetic testing",
    ),
    (
        "D21_04_strategy_works_one_regime",
        "Strategy works only in one regime",
        "Build explicit regime gate and test false-classification risk",
    ),
    (
        "D21_05_zero_latency_only",
        "Strategy works only with zero latency",
        "Reject for retail deployment",
    ),
    (
        "D21_06_optimistic_passive_only",
        "Strategy works only with optimistic passive fills",
        "Reject or redesign execution",
    ),
    (
        "D21_07_across_generators_seeds",
        "Strategy works across generators/seeds",
        "Candidate for real-data paper testing",
    ),
    (
        "D21_08_synthetic_not_real",
        "Strategy works synthetically but not on accumulating real days",
        "Treat as generator artifact and investigate",
    ),
    (
        "D21_09_wild_seed_variation",
        "Results vary wildly by seed",
        "Insufficient robustness or unstable scenario design",
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


def build_decision_rules() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "decision_rule_id": rule_id,
                "outcome_condition": condition,
                "plan_decision": decision,
                "rule_scope": "phase21_post_three_month_decision_framework",
            }
            for rule_id, condition, decision in DECISION_RULES
        ]
    )


def build_decision_ledger(paths: dict[str, Path]) -> pd.DataFrame:
    stage_d = pd.read_csv(paths["stage_d_strategy_summary"])
    stage_e = pd.read_csv(paths["stage_e_prerequisite_ledger"])
    acceptance = pd.read_csv(paths["strategy_acceptance_summary"])
    economic = pd.read_csv(paths["economic_viability_frontier"])
    risk_adjusted = pd.read_csv(paths["risk_adjusted_economic_frontier"])
    predictive = pd.read_csv(paths["predictive_promotion_falsification"])
    execution = pd.read_csv(paths["execution_summary"])

    promoted = int(acceptance["promotion_allowed"].astype(bool).sum())
    extension_allowed = bool(stage_e.loc[stage_e["prerequisite_id"].eq("full_year_extension_allowed"), "passes"].astype(bool).iloc[0])
    blocking_prereqs = int((~stage_e["passes"].astype(bool)).sum())
    stage_d_positive_strategies = int(
        stage_d.loc[
            (~stage_d["control_or_risk_module"].astype(bool))
            & (stage_d["mean_gross_return_proxy"].astype(float) > 0),
            "strategy_id",
        ].nunique()
    )
    retail_stress_positive = int(
        economic.loc[
            economic["retail_or_stress_profile"].astype(bool)
            & economic["net_positive_proxy"].astype(bool),
            "strategy_id",
        ].nunique()
    )
    risk_joint_pass = int(risk_adjusted["net_positive_and_risk_pass_proxy"].astype(bool).sum())
    predictive_candidates = int(predictive["predictive_promotion_candidate_proxy"].astype(bool).sum())
    baseline_pass = int(predictive["baseline_pass_proxy"].astype(bool).sum())
    all_holdout_pass = int(predictive["holdout_all_cell_pass_proxy"].astype(bool).sum())
    zero_latency_positive = int(
        execution.loc[
            execution["execution_profile"].astype(str).eq("zero_latency_spread_only_control")
            & (execution["mean_net_return"].astype(float) > 0),
            "strategy_id",
        ].nunique()
    )
    retail_positive = int(
        execution.loc[
            execution["execution_profile"].astype(str).isin(["retail_marketable_default", "stressed_retail"])
            & (execution["mean_net_return"].astype(float) > 0),
            "strategy_id",
        ].nunique()
    )
    seed_variation_rows = (
        stage_d.groupby("strategy_id")["mean_gross_return_proxy"]
        .agg(["min", "max"])
        .assign(range_proxy=lambda frame: frame["max"] - frame["min"])
    )
    wild_seed_variation_rows = int((seed_variation_rows["range_proxy"].abs() > 0.001).sum())

    rows = [
        {
            "decision_rule_id": "D21_01_no_strategy_survives_costs_latency",
            "current_condition_met": bool(promoted == 0 and risk_joint_pass == 0),
            "observed_value": f"promoted={promoted}; risk_adjusted_joint_pass_rows={risk_joint_pass}; retail_stress_positive_strategies={retail_stress_positive}",
            "current_decision": "Improve or reject strategies; do not tune generator to create profit",
            "evidence_source": f"{paths['strategy_acceptance_summary']}; {paths['risk_adjusted_economic_frontier']}; {paths['economic_viability_frontier']}",
            "next_action": "Clear acceptance blockers or reject/redesign strategies before any full-year extension.",
            "decision_status": "active_current_decision",
        },
        {
            "decision_rule_id": "D21_02_only_price_baselines_work",
            "current_condition_met": False,
            "observed_value": "Stage C baseline proxies exist, but current evidence does not prove price-only baselines are the only working models.",
            "current_decision": "L2 adds insufficient value under tested assumptions",
            "evidence_source": str(paths["stage_c_baseline_summary"]),
            "next_action": "Compare acceptance-grade L2 and price-only baselines after full execution/holdout evidence exists.",
            "decision_status": "not_proven_currently",
        },
        {
            "decision_rule_id": "D21_03_l2_improves_modestly_robustly",
            "current_condition_met": bool(predictive_candidates > 0 and all_holdout_pass > 0 and extension_allowed),
            "observed_value": f"predictive_candidates={predictive_candidates}; holdout_all_cell_pass={all_holdout_pass}; extension_allowed={extension_allowed}",
            "current_decision": "Continue collecting real data and extend synthetic testing",
            "evidence_source": f"{paths['predictive_promotion_falsification']}; {paths['stage_e_prerequisite_ledger']}",
            "next_action": "Do not advance; predictive/holdout/full-year readiness criteria are not met.",
            "decision_status": "blocked_not_current_decision",
        },
        {
            "decision_rule_id": "D21_04_strategy_works_one_regime",
            "current_condition_met": False,
            "observed_value": "No acceptance-grade per-regime winner exists; Stage D is proxy-only.",
            "current_decision": "Build explicit regime gate and test false-classification risk",
            "evidence_source": str(paths["stage_d_strategy_summary"]),
            "next_action": "Create regime-gated acceptance diagnostics only after candidate strategy exists.",
            "decision_status": "not_proven_currently",
        },
        {
            "decision_rule_id": "D21_05_zero_latency_only",
            "current_condition_met": bool(zero_latency_positive > 0 and retail_positive == 0),
            "observed_value": f"zero_latency_positive_strategies={zero_latency_positive}; retail_or_stress_positive_strategies={retail_positive}",
            "current_decision": "Reject for retail deployment",
            "evidence_source": str(paths["execution_summary"]),
            "next_action": "Keep retail/stressed execution profiles as required; do not promote zero-latency-only behavior.",
            "decision_status": "not_current_primary_decision",
        },
        {
            "decision_rule_id": "D21_06_optimistic_passive_only",
            "current_condition_met": False,
            "observed_value": "Current acceptance state does not contain an optimistic-passive-only promoted candidate.",
            "current_decision": "Reject or redesign execution",
            "evidence_source": str(paths["risk_adjusted_economic_frontier"]),
            "next_action": "Require pessimistic/retail execution controls before promotion.",
            "decision_status": "not_proven_currently",
        },
        {
            "decision_rule_id": "D21_07_across_generators_seeds",
            "current_condition_met": bool(stage_d_positive_strategies > 0 and predictive_candidates > 0 and blocking_prereqs == 0),
            "observed_value": f"stage_d_positive_noncontrol_strategies={stage_d_positive_strategies}; predictive_candidates={predictive_candidates}; stage_e_blocking_prereqs={blocking_prereqs}",
            "current_decision": "Candidate for real-data paper testing",
            "evidence_source": f"{paths['stage_d_strategy_summary']}; {paths['predictive_promotion_falsification']}; {paths['stage_e_prerequisite_ledger']}",
            "next_action": "Do not paper-test yet; full readiness blockers remain.",
            "decision_status": "blocked_not_current_decision",
        },
        {
            "decision_rule_id": "D21_08_synthetic_not_real",
            "current_condition_met": False,
            "observed_value": "Real multi-day strategy comparison does not exist yet.",
            "current_decision": "Treat as generator artifact and investigate",
            "evidence_source": str(paths["stage_e_prerequisite_ledger"]),
            "next_action": "Collect/import multi-day real holdout before classifying synthetic-vs-real divergence.",
            "decision_status": "not_testable_currently",
        },
        {
            "decision_rule_id": "D21_09_wild_seed_variation",
            "current_condition_met": bool(wild_seed_variation_rows > 0),
            "observed_value": f"wild_seed_variation_rows={wild_seed_variation_rows}; note=Stage D current seed summaries are proxy/static by seed",
            "current_decision": "Insufficient robustness or unstable scenario design",
            "evidence_source": str(paths["stage_d_strategy_summary"]),
            "next_action": "Run true full-seed stochastic execution before using seed variation as an acceptance decision.",
            "decision_status": "not_proven_currently",
        },
    ]
    return pd.DataFrame(rows)


def build_decision_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    active = ledger[ledger["decision_status"].astype(str).eq("active_current_decision")]
    current_decision = active["current_decision"].iloc[0] if len(active) else "No active decision"
    return pd.DataFrame(
        [
            {"metric": "decision_rules", "value": int(len(ledger)), "description": "Phase 21 decision rules evaluated"},
            {"metric": "active_current_decisions", "value": int(len(active)), "description": "Rules currently determining the decision"},
            {"metric": "extension_or_paper_ready", "value": 0, "description": "No current row permits full-year extension or real-data paper testing"},
            {"metric": "current_decision", "value": current_decision, "description": "Current Phase 21 decision"},
        ]
    )


def write_report(output_dir: Path, rules: pd.DataFrame, ledger: pd.DataFrame, summary: pd.DataFrame) -> None:
    lines = [
        "# Phase 21 Decision Framework",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This framework evaluates the plan's post-three-month decision table against current Stage D, Stage E, Phase 15 and Phase 16 evidence.",
        "It is a decision ledger, not strategy-promotion evidence.",
        "",
        "## Decision Summary",
        "",
        _markdown_table(summary),
        "",
        "## Decision Rules",
        "",
        _markdown_table(rules),
        "",
        "## Current Decision Ledger",
        "",
        _markdown_table(ledger),
        "",
    ]
    (output_dir / "phase21_decision_framework_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase21(paths: dict[str, Path], output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    rules = build_decision_rules()
    ledger = build_decision_ledger(paths)
    summary = build_decision_summary(ledger)
    rules.to_csv(output_dir / "decision_rules.csv", index=False)
    ledger.to_csv(output_dir / "decision_ledger.csv", index=False)
    summary.to_csv(output_dir / "decision_summary.csv", index=False)
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "decision_rule_rows": int(len(rules)),
        "decision_ledger_rows": int(len(ledger)),
        "active_current_decisions": int((ledger["decision_status"].astype(str) == "active_current_decision").sum()),
        "scope": "phase21_decision_framework_not_promotion_evidence",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase21",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={"decision_rules": DECISION_RULES},
            outputs={
                "decision_rules": str(output_dir / "decision_rules.csv"),
                "decision_ledger": str(output_dir / "decision_ledger.csv"),
                "decision_summary": str(output_dir / "decision_summary.csv"),
                "report": str(output_dir / "phase21_decision_framework_report.md"),
                "manifest": str(output_dir / "phase21_decision_framework_manifest.json"),
            },
            random_seed="not_applicable_decision_framework",
            scenario_ids="phase21_post_stage_d_stage_e_current_evidence",
            cost_model_version="phase12_phase16_proxy_cost_evidence_not_acceptance",
            latency_model_version="phase12_phase16_proxy_latency_evidence_not_acceptance",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase21_decision_framework_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, rules, ledger, summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 21 decision framework artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase21"))
    parser.add_argument("--stage-d-strategy-summary", type=Path, default=Path("outputs/stage_d/stage_d_strategy_proxy_summary.csv"))
    parser.add_argument("--stage-e-prerequisite-ledger", type=Path, default=Path("outputs/stage_e/stage_e_prerequisite_ledger.csv"))
    parser.add_argument("--strategy-acceptance-summary", type=Path, default=Path("outputs/phase15/strategy_acceptance_summary.csv"))
    parser.add_argument("--economic-viability-frontier", type=Path, default=Path("outputs/phase16/economic_viability_frontier.csv"))
    parser.add_argument("--risk-adjusted-economic-frontier", type=Path, default=Path("outputs/phase16/risk_adjusted_economic_frontier.csv"))
    parser.add_argument("--predictive-promotion-falsification", type=Path, default=Path("outputs/phase16/predictive_promotion_falsification.csv"))
    parser.add_argument("--execution-summary", type=Path, default=Path("outputs/phase12/execution_summary.csv"))
    parser.add_argument("--stage-c-baseline-summary", type=Path, default=Path("outputs/stage_c/stage_c_baseline_proxy_run_summary.csv"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "stage_d_strategy_summary": args.stage_d_strategy_summary,
        "stage_e_prerequisite_ledger": args.stage_e_prerequisite_ledger,
        "strategy_acceptance_summary": args.strategy_acceptance_summary,
        "economic_viability_frontier": args.economic_viability_frontier,
        "risk_adjusted_economic_frontier": args.risk_adjusted_economic_frontier,
        "predictive_promotion_falsification": args.predictive_promotion_falsification,
        "execution_summary": args.execution_summary,
        "stage_c_baseline_summary": args.stage_c_baseline_summary,
    }
    run_phase21(paths, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
