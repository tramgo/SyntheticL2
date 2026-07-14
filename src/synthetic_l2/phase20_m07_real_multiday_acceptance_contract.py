from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


REAL_MULTIDAY_ACCEPTANCE_CRITERIA = [
    ("real_multiday_data_coverage", "Multiple diagnostically sound real trading days are collected for each candidate strategy universe.", "multi-day real L2 coverage with documented gaps and symbol coverage"),
    ("real_multiday_predictive_holdout", "Predictive results are rerun and stable on real multi-day holdout data.", "real multi-day predictive baseline, calibration and stability pass"),
    ("real_multiday_economic_validation", "Economic P&L is validated on real multi-day or untouched holdout data with reconciled costs.", "retail/stress economics remain positive after broker/fill/cost reconciliation"),
    ("real_multiday_robustness_rerun", "Robustness checks are rerun on multiple real days and compared to synthetic scenarios.", "real multi-day strategy behavior is stable and not synthetic-specific"),
    ("real_multiday_realism_validation", "Synthetic/holdout realism is checked against real multi-day strategy behavior.", "real behavior matches accepted synthetic/holdout envelopes without artifact dependence"),
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
            for criterion_id, description, threshold in REAL_MULTIDAY_ACCEPTANCE_CRITERIA
        ]
    )


def _status(row: pd.Series) -> str:
    support = str(row.get("strategy_support_level", ""))
    gate = str(row.get("gate_id", ""))
    if support == "not_supported_by_current_product":
        return "blocked_by_unsupported_strategy_scope"
    if support == "partial_missing_required_features":
        return "blocked_by_partial_strategy_support"
    if gate == "G02_economic":
        return "real_multiday_economic_validation_missing"
    if gate == "G01_predictive":
        return "real_multiday_predictive_holdout_missing"
    if gate == "G03_robustness":
        return "real_multiday_robustness_rerun_missing"
    if gate == "G05_realism":
        return "real_multiday_realism_validation_missing"
    return "real_multiday_acceptance_requirement_open"


def _observed_metric(row: pd.Series) -> str:
    gate = str(row.get("gate_id", ""))
    if gate == "G02_economic":
        return (
            f"economic_acceptance_ready_now={row.get('economic_acceptance_ready_now', '')}; "
            f"broker_contract_note_reconciliation_ready={row.get('broker_contract_note_reconciliation_ready', '')}; "
            f"real_multiday_rows=0"
        )
    if gate == "G01_predictive":
        return (
            f"predictive_promotion_candidate_proxy={row.get('predictive_promotion_candidate_proxy', '')}; "
            f"falsification_status={row.get('falsification_status', '')}; real_multiday_rows=0"
        )
    if gate == "G03_robustness":
        return (
            f"real_data_rerun_status={row.get('real_data_rerun_status', '')}; "
            f"dimension_status={row.get('dimension_status', '')}; real_multiday_rows=0"
        )
    if gate == "G05_realism":
        return (
            f"holdout_profiles={row.get('holdout_profiles', '')}; "
            f"holdout_acceptance_eligible_profiles={row.get('holdout_acceptance_eligible_profiles', '')}; "
            f"real_multiday_rows=0"
        )
    return str(row.get("observed_value", ""))


def build_real_multiday_ledger(
    execution_roadmap: pd.DataFrame,
    stage_quality: pd.DataFrame,
    horizon_summary: pd.DataFrame,
    economic: pd.DataFrame,
    predictive: pd.DataFrame,
    robustness: pd.DataFrame,
    holdout: pd.DataFrame,
    support: pd.DataFrame,
) -> pd.DataFrame:
    m07 = execution_roadmap[
        execution_roadmap["execution_milestone"].astype(str) == "M07_real_multiday_acceptance_validation"
    ].copy()
    real_sample_summary = {
        "real_sample_days_available": 1,
        "real_sample_symbols": int(stage_quality["symbol"].nunique()),
        "real_sample_rows": int(stage_quality["row_count"].sum()),
        "symbols_with_15s_gaps": int((stage_quality["stale_gap_gt_15s_count"] > 0).sum()),
        "dense_1s_full_session_symbols": int(
            horizon_summary[
                (horizon_summary["scope"].astype(str) == "full_session")
                & (horizon_summary["horizon_ms"].astype(int) == 1000)
            ]["dense_regular_panel_symbols"].max()
        )
        if not horizon_summary.empty
        else 0,
    }
    holdout_summary = {
        "holdout_profiles": int(len(holdout)),
        "holdout_acceptance_eligible_profiles": int(holdout["acceptance_eligible_now"].astype(bool).sum()),
    }
    rows = (
        m07.merge(economic, on="strategy_id", how="left")
        .merge(predictive, on="strategy_id", how="left", suffixes=("", "_predictive"))
        .merge(robustness[["strategy_id", "real_data_rerun_status", "dimension_status", "acceptance_eligible"]], on="strategy_id", how="left")
        .merge(support[["strategy_id", "strategy_support_closure_status", "required_support_action"]], on="strategy_id", how="left")
    )
    for column, value in real_sample_summary.items():
        rows[column] = value
    for column, value in holdout_summary.items():
        rows[column] = value
    rows["real_multiday_acceptance_status"] = rows.apply(_status, axis=1)
    rows["observed_real_multiday_metric"] = rows.apply(_observed_metric, axis=1)
    rows["real_multiday_data_required"] = True
    rows["economic_real_validation_required"] = rows["gate_id"].astype(str).eq("G02_economic")
    rows["predictive_real_holdout_required"] = rows["gate_id"].astype(str).eq("G01_predictive")
    rows["robustness_real_rerun_required"] = rows["gate_id"].astype(str).eq("G03_robustness")
    rows["realism_real_validation_required"] = rows["gate_id"].astype(str).eq("G05_realism")
    rows["acceptance_requirement_met_after_contract"] = False
    rows["blocking_gap_after_contract"] = rows.apply(
        lambda row: (
            f"Support closure required first: {row.get('required_support_action', '')}"
            if str(row.get("strategy_support_closure_status", "")).startswith("requires_")
            else "Real multi-day acceptance evidence is missing; current evidence is one-day/proxy/synthetic only."
        ),
        axis=1,
    )
    rows["required_real_multiday_action"] = rows.apply(
        lambda row: (
            "Collect/run multi-day real economic validation with reconciled fills, costs and P&L."
            if row["economic_real_validation_required"]
            else "Collect/run multi-day real predictive holdout validation with frozen model and baseline checks."
            if row["predictive_real_holdout_required"]
            else "Collect/run multi-day real robustness reruns and compare against synthetic scenario behavior."
            if row["robustness_real_rerun_required"]
            else "Collect/run multi-day real realism validation and compare against synthetic/holdout envelopes."
        ),
        axis=1,
    )
    columns = [
        "execution_rank",
        "gate_id",
        "strategy_id",
        "strategy_support_level",
        "strategy_role",
        "hardening_requirement",
        "action_class",
        "dependency_status",
        "strategy_support_closure_status",
        "real_multiday_acceptance_status",
        "observed_real_multiday_metric",
        "real_sample_days_available",
        "real_sample_symbols",
        "real_sample_rows",
        "symbols_with_15s_gaps",
        "dense_1s_full_session_symbols",
        "holdout_profiles",
        "holdout_acceptance_eligible_profiles",
        "real_multiday_data_required",
        "economic_real_validation_required",
        "predictive_real_holdout_required",
        "robustness_real_rerun_required",
        "realism_real_validation_required",
        "acceptance_requirement_met_after_contract",
        "blocking_gap_after_contract",
        "required_real_multiday_action",
        "required_next_evidence",
    ]
    for column in columns:
        if column not in rows:
            rows[column] = False if column.endswith("_required") else ""
    return rows[columns].sort_values("execution_rank", kind="mergesort")


def build_gap_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    return (
        ledger.groupby("real_multiday_acceptance_status", sort=True)
        .agg(rows=("hardening_requirement", "size"), strategies=("strategy_id", "nunique"), acceptance_met_rows=("acceptance_requirement_met_after_contract", "sum"))
        .reset_index()
        .sort_values(["rows", "real_multiday_acceptance_status"], ascending=[False, True], kind="mergesort")
    )


def build_strategy_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    grouped = ledger.groupby(["strategy_id", "strategy_support_level", "strategy_role"], sort=True).agg(
        m07_rows=("hardening_requirement", "size"),
        economic_real_validation_rows=("economic_real_validation_required", "sum"),
        predictive_real_holdout_rows=("predictive_real_holdout_required", "sum"),
        robustness_real_rerun_rows=("robustness_real_rerun_required", "sum"),
        realism_real_validation_rows=("realism_real_validation_required", "sum"),
        acceptance_met_rows=("acceptance_requirement_met_after_contract", "sum"),
        first_required_action=("required_real_multiday_action", "first"),
    ).reset_index()
    grouped["real_multiday_contract_status"] = "real_multiday_evidence_missing_not_acceptance"
    return grouped


def write_report(output_dir: Path, criteria: pd.DataFrame, ledger: pd.DataFrame, gap_summary: pd.DataFrame, strategy_summary: pd.DataFrame) -> None:
    lines = [
        "# Phase 20 M07 Real Multi-Day Acceptance Validation Contract",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase converts the seventh Phase 20 execution milestone into a real multi-day acceptance validation contract.",
        "It records that current evidence is one-day/proxy/synthetic and keeps every row non-acceptance-ready until multi-day real validation is collected and run.",
        "",
        "## Acceptance Criteria Contract",
        "",
        _markdown_table(criteria),
        "",
        "## Real Multi-Day Gap Summary",
        "",
        _markdown_table(gap_summary),
        "",
        "## Strategy Summary",
        "",
        _markdown_table(strategy_summary),
        "",
        "## M07 Real Multi-Day Acceptance Ledger",
        "",
        _markdown_table(ledger),
        "",
    ]
    (output_dir / "phase20_m07_real_multiday_acceptance_contract_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase20_m07(paths: dict[str, Path], output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    criteria = build_acceptance_criteria()
    ledger = build_real_multiday_ledger(
        pd.read_csv(paths["execution_roadmap"]),
        pd.read_csv(paths["stage_quality"]),
        pd.read_csv(paths["horizon_readiness_summary"]),
        pd.read_csv(paths["economic_reconciliation_strategy_summary"]),
        pd.read_csv(paths["predictive_promotion_falsification"]),
        pd.read_csv(paths["robustness_dimension_summary"]),
        pd.read_csv(paths["holdout_generator_realism_summary"]),
        pd.read_csv(paths["strategy_support_decision_summary"]),
    )
    gap_summary = build_gap_summary(ledger)
    strategy_summary = build_strategy_summary(ledger)
    criteria.to_csv(output_dir / "real_multiday_acceptance_criteria.csv", index=False)
    ledger.to_csv(output_dir / "real_multiday_acceptance_ledger.csv", index=False)
    gap_summary.to_csv(output_dir / "real_multiday_gap_summary.csv", index=False)
    strategy_summary.to_csv(output_dir / "real_multiday_strategy_summary.csv", index=False)
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "real_multiday_acceptance_criteria_rows": int(len(criteria)),
        "real_multiday_acceptance_rows": int(len(ledger)),
        "real_multiday_gap_summary_rows": int(len(gap_summary)),
        "real_multiday_strategy_rows": int(len(strategy_summary)),
        "economic_real_validation_required_rows": int(ledger["economic_real_validation_required"].astype(bool).sum()),
        "predictive_real_holdout_required_rows": int(ledger["predictive_real_holdout_required"].astype(bool).sum()),
        "robustness_real_rerun_required_rows": int(ledger["robustness_real_rerun_required"].astype(bool).sum()),
        "realism_real_validation_required_rows": int(ledger["realism_real_validation_required"].astype(bool).sum()),
        "acceptance_met_after_contract_rows": int(ledger["acceptance_requirement_met_after_contract"].astype(bool).sum()),
        "scope": "phase20_m07_real_multiday_acceptance_contract_not_acceptance",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase20_m07",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={"real_multiday_acceptance_criteria": REAL_MULTIDAY_ACCEPTANCE_CRITERIA},
            outputs={
                "real_multiday_acceptance_criteria": str(output_dir / "real_multiday_acceptance_criteria.csv"),
                "real_multiday_acceptance_ledger": str(output_dir / "real_multiday_acceptance_ledger.csv"),
                "real_multiday_gap_summary": str(output_dir / "real_multiday_gap_summary.csv"),
                "real_multiday_strategy_summary": str(output_dir / "real_multiday_strategy_summary.csv"),
                "report": str(output_dir / "phase20_m07_real_multiday_acceptance_contract_report.md"),
                "manifest": str(output_dir / "real_multiday_acceptance_contract_manifest.json"),
            },
            random_seed="not_applicable_deterministic_real_multiday_acceptance_contract",
            scenario_ids="phase20_M07_real_multiday_acceptance_validation_rows",
            cost_model_version="phase12_zerodha_order_formula_proxy_contract_note_missing",
            latency_model_version="stage_a1_one_day_zerodha_websocket_sample",
            base_dir=base_dir,
        )
    )
    (output_dir / "real_multiday_acceptance_contract_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, criteria, ledger, gap_summary, strategy_summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 20 M07 real multi-day acceptance validation contract artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase20_m07"))
    parser.add_argument("--execution-roadmap", type=Path, default=Path("outputs/phase20/acceptance_execution_roadmap.csv"))
    parser.add_argument("--stage-quality", type=Path, default=Path("outputs/stage_a1/data_quality_report.csv"))
    parser.add_argument("--horizon-readiness-summary", type=Path, default=Path("outputs/horizon_readiness/horizon_readiness_summary.csv"))
    parser.add_argument("--economic-reconciliation-strategy-summary", type=Path, default=Path("outputs/phase16/economic_reconciliation_strategy_summary.csv"))
    parser.add_argument("--predictive-promotion-falsification", type=Path, default=Path("outputs/phase16/predictive_promotion_falsification.csv"))
    parser.add_argument("--robustness-dimension-summary", type=Path, default=Path("outputs/phase13/robustness_dimension_summary.csv"))
    parser.add_argument("--holdout-generator-realism-summary", type=Path, default=Path("outputs/phase14/holdout_generator_realism_summary.csv"))
    parser.add_argument("--strategy-support-decision-summary", type=Path, default=Path("outputs/phase20_m02/strategy_support_decision_summary.csv"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "execution_roadmap": args.execution_roadmap,
        "stage_quality": args.stage_quality,
        "horizon_readiness_summary": args.horizon_readiness_summary,
        "economic_reconciliation_strategy_summary": args.economic_reconciliation_strategy_summary,
        "predictive_promotion_falsification": args.predictive_promotion_falsification,
        "robustness_dimension_summary": args.robustness_dimension_summary,
        "holdout_generator_realism_summary": args.holdout_generator_realism_summary,
        "strategy_support_decision_summary": args.strategy_support_decision_summary,
    }
    run_phase20_m07(paths, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
