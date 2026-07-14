from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


RECALIBRATION_DOMAINS = [
    ("intraday_curves", "Intraday curves", "Re-estimate open/midday/close activity, spread, depth and volatility curves."),
    ("spread_depth_distributions", "Spread/depth distributions", "Re-estimate queue depth, spread and visible-liquidity distributions by symbol/regime."),
    ("regime_frequencies", "Regime frequencies", "Update normal, volatile, thin-book and shock regime probabilities."),
    ("price_impact_functions", "Price-impact functions", "Re-estimate impact and recovery curves from trade/quote interactions."),
    ("trade_quote_interaction", "Trade/quote interaction", "Refresh event ordering, quote response and signed-trade proxy relationships."),
    ("cross_ticker_correlation", "Cross-ticker correlation", "Re-estimate same-sector, ETF/basket and market-wide co-movement structure."),
    ("shocks_and_recovery", "Shocks and recovery", "Refresh shock templates, depth evaporation and recovery profiles."),
    ("retail_feed_latency", "Retail feed latency", "Re-estimate websocket delivery delay, batching, stale gaps and reconnect behaviour."),
    ("missing_data_patterns", "Missing-data patterns", "Track missing levels, stale books, disconnect windows and symbol-specific capture gaps."),
]


MILESTONES = [
    ("M22_01_one_day_schema_pipeline", "1 day", 1, 1, "schema, scale and pipeline"),
    ("M22_02_five_to_ten_days_intraday", "5-10 days", 5, 10, "normal intraday variation"),
    ("M22_03_twenty_to_thirty_days_regime", "20-30 days", 20, 30, "basic regime calibration"),
    ("M22_04_sixty_days_oos", "60 days", 60, 60, "preliminary out-of-sample comparison"),
    ("M22_05_three_to_six_months_screening", "3-6 months", 63, 126, "meaningful strategy screening"),
    ("M22_06_twelve_months_robustness", "12+ months", 252, 252, "stronger regime and robustness assessment"),
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


def _first_int(frame: pd.DataFrame, column: str, default: int = 0) -> int:
    if column not in frame.columns or frame.empty:
        return default
    return int(pd.to_numeric(frame[column], errors="coerce").fillna(default).iloc[0])


def current_real_data_state(paths: dict[str, Path]) -> dict[str, int | str | bool]:
    stage_a2 = pd.read_csv(paths["stage_a2_readiness_summary"])
    stage_e = pd.read_csv(paths["stage_e_prerequisite_ledger"])
    m07_gap_summary = pd.read_csv(paths["real_multiday_gap_summary"])
    phase21_summary = pd.read_csv(paths["phase21_decision_summary"])

    sample_days = _first_int(stage_a2, "current_sample_days_available")
    open_contract_rows = _first_int(stage_a2, "open_contract_rows")
    acceptance_met_rows = _first_int(stage_a2, "acceptance_met_rows")
    symbols_evaluated = _first_int(stage_a2, "symbols_evaluated")
    current_rows = _first_int(stage_a2, "current_rows")
    stage_a2_status = str(stage_a2.get("stage_a2_status", pd.Series(["unknown"])).iloc[0])
    extension_allowed = bool(
        stage_e.loc[stage_e["prerequisite_id"].eq("full_year_extension_allowed"), "passes"].astype(bool).any()
    )
    real_multiday_acceptance_met_rows = int(pd.to_numeric(m07_gap_summary["acceptance_met_rows"], errors="coerce").fillna(0).sum())
    current_decision = str(
        phase21_summary.loc[phase21_summary["metric"].eq("current_decision"), "value"].iloc[0]
    )

    # Phase 22 milestones explicitly refer to complete Class B event-grade days.
    # The current workspace has a one-day sample, but Stage A2 still has open
    # capture-contract rows, so it must not be counted as Class B event-grade.
    class_b_event_grade_days = sample_days if open_contract_rows == 0 and acceptance_met_rows > 0 else 0

    return {
        "sample_days_available": sample_days,
        "class_b_event_grade_days": class_b_event_grade_days,
        "symbols_evaluated": symbols_evaluated,
        "current_rows": current_rows,
        "stage_a2_open_contract_rows": open_contract_rows,
        "stage_a2_acceptance_met_rows": acceptance_met_rows,
        "stage_a2_status": stage_a2_status,
        "real_multiday_acceptance_met_rows": real_multiday_acceptance_met_rows,
        "full_year_extension_allowed": extension_allowed,
        "phase21_current_decision": current_decision,
    }


def build_milestone_catalog(state: dict[str, int | str | bool]) -> pd.DataFrame:
    class_b_days = int(state["class_b_event_grade_days"])
    sample_days = int(state["sample_days_available"])
    rows = []
    for milestone_id, availability, min_days, target_days, use in MILESTONES:
        reached = class_b_days >= min_days
        sample_smoke = milestone_id == "M22_01_one_day_schema_pipeline" and sample_days >= 1 and not reached
        days_needed_min = max(min_days - class_b_days, 0)
        days_needed_target = max(target_days - class_b_days, 0)
        if reached:
            status = "class_b_milestone_reached"
        elif sample_smoke:
            status = "sample_day_smoke_available_not_class_b"
        else:
            status = "blocked_until_more_class_b_event_grade_days"
        rows.append(
            {
                "milestone_id": milestone_id,
                "real_data_availability": availability,
                "class_b_min_days": min_days,
                "class_b_target_days": target_days,
                "current_class_b_event_grade_days": class_b_days,
                "current_sample_days_available": sample_days,
                "days_needed_for_min": days_needed_min,
                "days_needed_for_target": days_needed_target,
                "recalibration_use": use,
                "current_status": status,
                "acceptance_permission": bool(reached and state["full_year_extension_allowed"]),
            }
        )
    return pd.DataFrame(rows)


def build_recalibration_task_ledger(milestones: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for milestone in milestones.to_dict("records"):
        for domain_id, domain_name, description in RECALIBRATION_DOMAINS:
            if milestone["current_status"] == "class_b_milestone_reached":
                task_status = "ready_for_recalibration"
                next_action = "Run recalibration and compare against prior synthetic assumptions."
            elif milestone["milestone_id"] == "M22_01_one_day_schema_pipeline" and milestone["current_sample_days_available"] >= 1:
                task_status = "schema_smoke_only_not_event_flow_recalibration"
                next_action = "Use current sample for schema/scale checks only; collect Class B event-grade days before recalibration."
            else:
                task_status = "blocked_waiting_for_class_b_days"
                next_action = f"Collect at least {milestone['days_needed_for_min']} more Class B event-grade day(s) before this task."
            rows.append(
                {
                    "milestone_id": milestone["milestone_id"],
                    "domain_id": domain_id,
                    "domain_name": domain_name,
                    "domain_description": description,
                    "current_status": task_status,
                    "recalibration_use": milestone["recalibration_use"],
                    "minimum_class_b_days_required": milestone["class_b_min_days"],
                    "current_class_b_event_grade_days": milestone["current_class_b_event_grade_days"],
                    "next_action": next_action,
                }
            )
    return pd.DataFrame(rows)


def build_capture_expansion_plan(state: dict[str, int | str | bool], milestone_catalog: pd.DataFrame) -> pd.DataFrame:
    next_unreached = milestone_catalog[milestone_catalog["current_status"].ne("class_b_milestone_reached")].iloc[0]
    return pd.DataFrame(
        [
            {
                "priority_rank": 1,
                "workstream": "class_b_event_grade_capture",
                "current_state": f"sample_days={state['sample_days_available']}; class_b_event_grade_days={state['class_b_event_grade_days']}",
                "target_state": f"{next_unreached['class_b_min_days']} Class B event-grade day(s) for {next_unreached['real_data_availability']} milestone",
                "blocking_gap": "Current one-day sample is not accepted as complete Class B event-grade evidence.",
                "required_next_action": "Collect/import diagnostically complete multi-day websocket L2 data and rerun Stage A2 capture diagnostics.",
            },
            {
                "priority_rank": 2,
                "workstream": "capture_contract_closure",
                "current_state": f"stage_a2_open_contract_rows={state['stage_a2_open_contract_rows']}; stage_a2_acceptance_met_rows={state['stage_a2_acceptance_met_rows']}",
                "target_state": "0 open Stage A2 capture-contract rows and nonzero acceptance-met rows",
                "blocking_gap": str(state["stage_a2_status"]),
                "required_next_action": "Close timestamp semantics, sequencing, dropped-message, compaction and stale-gap diagnostics before counting days as Class B.",
            },
            {
                "priority_rank": 3,
                "workstream": "real_multiday_acceptance_inputs",
                "current_state": f"phase20_m07_acceptance_met_rows={state['real_multiday_acceptance_met_rows']}",
                "target_state": "Real multi-day predictive, economic and robustness validation rows become acceptance-grade.",
                "blocking_gap": "Phase 20 M07 real multi-day acceptance contract has 0 acceptance-met rows.",
                "required_next_action": "After Class B capture exists, run strategy real-holdout, real economic and real robustness validations.",
            },
            {
                "priority_rank": 4,
                "workstream": "phase21_decision_guardrail",
                "current_state": str(state["phase21_current_decision"]),
                "target_state": "Decision framework permits extension/paper testing only after evidence gates pass.",
                "blocking_gap": "Current Phase 21 decision blocks extension/paper testing.",
                "required_next_action": "Do not tune generator to create profit; use new real days to reduce assumptions and retest blockers.",
            },
        ]
    )


def build_readiness_summary(
    state: dict[str, int | str | bool],
    milestone_catalog: pd.DataFrame,
    task_ledger: pd.DataFrame,
) -> pd.DataFrame:
    first_ready = milestone_catalog[milestone_catalog["current_status"].eq("class_b_milestone_reached")]
    next_blocked = milestone_catalog[milestone_catalog["current_status"].ne("class_b_milestone_reached")].iloc[0]
    return pd.DataFrame(
        [
            {"metric": "sample_days_available", "value": int(state["sample_days_available"]), "description": "Current real sample trading days available"},
            {"metric": "class_b_event_grade_days", "value": int(state["class_b_event_grade_days"]), "description": "Complete Class B event-grade real days counted for Phase 22 milestones"},
            {"metric": "milestones_reached", "value": int(len(first_ready)), "description": "Phase 22 Class B milestones reached"},
            {"metric": "next_milestone_min_days", "value": int(next_blocked["class_b_min_days"]), "description": str(next_blocked["milestone_id"])},
            {"metric": "recalibration_tasks", "value": int(len(task_ledger)), "description": "Milestone/domain recalibration task rows"},
            {
                "metric": "schema_smoke_tasks_only",
                "value": int((task_ledger["current_status"].astype(str) == "schema_smoke_only_not_event_flow_recalibration").sum()),
                "description": "Tasks supported only for schema/scale smoke checks by the current sample",
            },
            {
                "metric": "ready_recalibration_tasks",
                "value": int((task_ledger["current_status"].astype(str) == "ready_for_recalibration").sum()),
                "description": "Tasks ready for event-flow recalibration",
            },
            {
                "metric": "phase22_extension_or_paper_ready",
                "value": 0,
                "description": "Phase 22 does not permit extension or paper testing under current evidence",
            },
        ]
    )


def write_report(
    output_dir: Path,
    summary: pd.DataFrame,
    milestone_catalog: pd.DataFrame,
    task_ledger: pd.DataFrame,
    expansion_plan: pd.DataFrame,
) -> None:
    lines = [
        "# Phase 22 Real Data Integration Roadmap",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This roadmap converts the plan's real-data availability milestones into a current-state ledger.",
        "It distinguishes current one-day sample/schema evidence from complete Class B event-grade days.",
        "It is not strategy-promotion evidence.",
        "",
        "## Readiness Summary",
        "",
        _markdown_table(summary),
        "",
        "## Real-Data Milestone Catalog",
        "",
        _markdown_table(milestone_catalog),
        "",
        "## Recalibration Task Ledger",
        "",
        _markdown_table(task_ledger),
        "",
        "## Capture Expansion Plan",
        "",
        _markdown_table(expansion_plan),
        "",
    ]
    (output_dir / "phase22_real_data_integration_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase22(paths: dict[str, Path], output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    state = current_real_data_state(paths)
    milestone_catalog = build_milestone_catalog(state)
    task_ledger = build_recalibration_task_ledger(milestone_catalog)
    expansion_plan = build_capture_expansion_plan(state, milestone_catalog)
    summary = build_readiness_summary(state, milestone_catalog, task_ledger)

    milestone_catalog.to_csv(output_dir / "real_data_milestone_catalog.csv", index=False)
    task_ledger.to_csv(output_dir / "recalibration_task_ledger.csv", index=False)
    expansion_plan.to_csv(output_dir / "capture_expansion_plan.csv", index=False)
    summary.to_csv(output_dir / "real_data_integration_summary.csv", index=False)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "sample_days_available": int(state["sample_days_available"]),
        "class_b_event_grade_days": int(state["class_b_event_grade_days"]),
        "milestone_rows": int(len(milestone_catalog)),
        "recalibration_task_rows": int(len(task_ledger)),
        "scope": "phase22_real_data_integration_roadmap_not_promotion_evidence",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase22",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={"milestones": MILESTONES, "recalibration_domains": RECALIBRATION_DOMAINS},
            outputs={
                "milestone_catalog": str(output_dir / "real_data_milestone_catalog.csv"),
                "recalibration_task_ledger": str(output_dir / "recalibration_task_ledger.csv"),
                "capture_expansion_plan": str(output_dir / "capture_expansion_plan.csv"),
                "summary": str(output_dir / "real_data_integration_summary.csv"),
                "report": str(output_dir / "phase22_real_data_integration_report.md"),
                "manifest": str(output_dir / "phase22_real_data_integration_manifest.json"),
            },
            random_seed="not_applicable_real_data_roadmap",
            scenario_ids="phase22_real_data_availability_milestones_current_workspace",
            cost_model_version="phase20_m07_real_multiday_economic_contract_not_acceptance",
            latency_model_version="stage_a2_capture_diagnostics_and_phase8_feed_profiles",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase22_real_data_integration_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, summary, milestone_catalog, task_ledger, expansion_plan)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 22 real-data integration roadmap artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase22"))
    parser.add_argument("--stage-a2-readiness-summary", type=Path, default=Path("outputs/stage_a2/stage_a2_readiness_summary.csv"))
    parser.add_argument("--stage-e-prerequisite-ledger", type=Path, default=Path("outputs/stage_e/stage_e_prerequisite_ledger.csv"))
    parser.add_argument("--real-multiday-gap-summary", type=Path, default=Path("outputs/phase20_m07/real_multiday_gap_summary.csv"))
    parser.add_argument("--phase21-decision-summary", type=Path, default=Path("outputs/phase21/decision_summary.csv"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "stage_a2_readiness_summary": args.stage_a2_readiness_summary,
        "stage_e_prerequisite_ledger": args.stage_e_prerequisite_ledger,
        "real_multiday_gap_summary": args.real_multiday_gap_summary,
        "phase21_decision_summary": args.phase21_decision_summary,
    }
    run_phase22(paths, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
