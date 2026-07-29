from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE227_DIR = Path("outputs/phase227")
DEFAULT_OUTPUT_DIR = Path("outputs/phase228")
SELECTED_ROUTE_ID = "P228_SOURCE_EXPANSION_AND_AVAILABLE_HORIZON_REPAIR"
FORBIDDEN_OUTPUTS = "label_materialization;feature_materialization;model_fit;model_prediction;strategy_replay;broader_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export"
NEXT_ACTION = "run_phase229_cost_aware_source_expansion_precommit_no_materialization_no_fit_no_replay_no_test"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = "") -> Any:
    if frame.empty or "metric" not in frame.columns or "value" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def build_closure_decision(phase227: pd.DataFrame, horizon: pd.DataFrame) -> pd.DataFrame:
    actionable_rows = as_int(metric_value(phase227, "phase227_actionable_rows", 0))
    quality_pass_rows = as_int(metric_value(phase227, "phase227_quality_pass_rows", 0))
    fit_candidates = as_int(metric_value(phase227, "phase227_fit_precommit_candidate_rows", 0))
    unavailable_horizons = 0
    if not horizon.empty and "materialization_available" in horizon.columns:
        unavailable_horizons = int(pd.to_numeric(horizon["materialization_available"], errors="coerce").fillna(0).eq(0).sum())
    return pd.DataFrame(
        [
            {
                "phase228_decision_id": "P228_CLOSE_CURRENT_COST_AWARE_LABEL_SET_FOR_FIT",
                "decision": "close_current_cost_aware_label_set_for_model_fit_and_replay",
                "phase227_actionable_rows": actionable_rows,
                "phase227_quality_pass_rows": quality_pass_rows,
                "phase227_fit_precommit_candidate_rows": fit_candidates,
                "unavailable_contract_horizon_rows": unavailable_horizons,
                "current_label_set_closed_for_fit": 1,
                "current_label_set_closed_for_replay": 1,
                "reuse_without_material_redesign_allowed": 0,
                "closure_reason": "cost_aware_label_quality_interpretation_has_zero_quality_pass_splits_and_zero_fit_precommit_candidates",
                "threshold_widening_allowed": 0,
                "model_fit_allowed_next": 0,
                "strategy_replay_allowed": 0,
                "broader_replay_allowed_next": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "profitability_claim_allowed": 0,
            }
        ]
    )


def build_redesign_catalog() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "phase228_redesign_route_id": "P228_SOURCE_EXPANSION_AND_AVAILABLE_HORIZON_REPAIR",
                "redesign_theme": "source_coverage_expansion",
                "precommit_action": "Expand train/validation source coverage and repair the contracted horizon set before rematerializing cost-aware labels.",
                "why_materially_different": "Addresses sparse labels by adding source coverage and using only genuinely available horizons, not by lowering the cost hurdle after seeing failure.",
                "required_before_materialization": "source_coverage_contract;available_horizon_contract;minimum_date_breadth_contract;no_threshold_widening_proof",
                "phase229_candidate": 1,
                "label_materialization_allowed_next": 0,
                "model_fit_allowed_next": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            },
            {
                "phase228_redesign_route_id": "P228_EXECUTION_PREMISE_SPLIT_PASSIVE_ONLY",
                "redesign_theme": "execution_premise_redesign",
                "precommit_action": "Define a separate passive-only cost-aware label route with nonfill penalties and no impossible fill assumptions.",
                "why_materially_different": "Changes execution mechanism rather than relaxing the retail marketable cost hurdle that caused sparsity.",
                "required_before_materialization": "passive_fill_feasibility_contract;nonfill_penalty_contract;queue_proxy_contract;separate_acceptance_path",
                "phase229_candidate": 1,
                "label_materialization_allowed_next": 0,
                "model_fit_allowed_next": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            },
            {
                "phase228_redesign_route_id": "P228_CLOSE_COST_AWARE_ROUTE",
                "redesign_theme": "branch_closure",
                "precommit_action": "Close the cost-aware event label branch if source expansion cannot provide adequate event count and date breadth.",
                "why_materially_different": "Prevents compute drift into underpowered labels and preserves sealed-test discipline.",
                "required_before_materialization": "closure_decision_only",
                "phase229_candidate": 1,
                "label_materialization_allowed_next": 0,
                "model_fit_allowed_next": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            },
        ]
    )


def build_guardrail_ledger() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "phase228_guardrail_id": "P228_NO_POST_HOC_THRESHOLD_WIDENING",
                "guardrail": "Do not lower cost hurdles, reduce minimum event count, or reinterpret failed quality gates inside Phase228.",
                "required_in_phase229": 1,
                "threshold_widening_allowed": 0,
                "model_fit_allowed_next": 0,
            },
            {
                "phase228_guardrail_id": "P228_AVAILABLE_HORIZONS_ONLY",
                "guardrail": "A horizon may be used only if genuine Phase181/Phase214 train/validation inputs exist for that horizon.",
                "required_in_phase229": 1,
                "threshold_widening_allowed": 0,
                "model_fit_allowed_next": 0,
            },
            {
                "phase228_guardrail_id": "P228_SOURCE_BREADTH_BEFORE_FIT",
                "guardrail": "Any rematerialization must improve date breadth and actionable count before model-fit precommit can be opened.",
                "required_in_phase229": 1,
                "threshold_widening_allowed": 0,
                "model_fit_allowed_next": 0,
            },
        ]
    )


def build_phase229_work_order(redesign: pd.DataFrame, guardrails: pd.DataFrame) -> pd.DataFrame:
    selected = redesign[redesign["phase228_redesign_route_id"].astype(str).eq(SELECTED_ROUTE_ID)] if not redesign.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            {
                "phase229_work_order_id": "P229_COST_AWARE_SOURCE_EXPANSION_PRECOMMIT",
                "work_order": "Precommit source expansion and available-horizon repair for cost-aware labels before any rematerialization, fit, replay, or sealed test.",
                "selected_route_id": SELECTED_ROUTE_ID,
                "selected_route_theme": selected["redesign_theme"].iloc[0] if not selected.empty else "source_coverage_expansion",
                "required_artifacts": selected["required_before_materialization"].iloc[0] if not selected.empty else "",
                "guardrail_rows": len(guardrails),
                "allowed_next_scope": "source_expansion_precommit_only_no_materialization_no_fit_no_replay_no_test",
                "label_materialization_allowed_next": 0,
                "model_fit_allowed_next": 0,
                "strategy_replay_allowed": 0,
                "broader_replay_allowed_next": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "profitability_claim_allowed": 0,
            }
        ]
    )


def build_forbidden_execution_ledger() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "forbidden_output": item,
                "emitted_in_phase228": 0,
                "allowed_in_phase228": 0,
                "rationale": "Phase228 is a closure/redesign precommit decision only and emits no labels, features, fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, threshold-widening, row-level export, or profitability artifact.",
            }
            for item in FORBIDDEN_OUTPUTS.split(";")
        ]
    )


def build_gates(phase227: pd.DataFrame, closure: pd.DataFrame, redesign: pd.DataFrame, guardrails: pd.DataFrame, work_order: pd.DataFrame, forbidden: pd.DataFrame) -> pd.DataFrame:
    phase227_complete = as_int(metric_value(phase227, "phase227_cost_aware_event_label_quality_interpretation_complete", 0))
    fit_candidates = as_int(metric_value(phase227, "phase227_fit_precommit_candidate_rows", 0))
    current_closed_fit = int(pd.to_numeric(closure["current_label_set_closed_for_fit"], errors="coerce").fillna(0).sum()) if not closure.empty else 0
    current_closed_replay = int(pd.to_numeric(closure["current_label_set_closed_for_replay"], errors="coerce").fillna(0).sum()) if not closure.empty else 0
    selected_rows = int(redesign["phase228_redesign_route_id"].astype(str).eq(SELECTED_ROUTE_ID).sum()) if not redesign.empty else 0
    forbidden_emitted = int(pd.to_numeric(forbidden["emitted_in_phase228"], errors="coerce").fillna(0).sum()) if not forbidden.empty else 1
    forbidden_flags = 0
    for frame in [closure, redesign, guardrails, work_order]:
        for col in ["label_materialization_allowed_next", "model_fit_allowed_next", "strategy_replay_allowed", "broader_replay_allowed_next", "test_replay_allowed_next", "promotion_allowed", "paper_or_live_acceptance_allowed", "profitability_claim_allowed", "threshold_widening_allowed"]:
            if not frame.empty and col in frame.columns:
                forbidden_flags += int(pd.to_numeric(frame[col], errors="coerce").fillna(0).sum())
    return pd.DataFrame(
        [
            ("P228_PHASE227_COMPLETE", phase227_complete == 1, f"phase227_complete={phase227_complete}", "hard"),
            ("P228_NO_FIT_CANDIDATES_CONFIRMED", fit_candidates == 0, f"fit_candidates={fit_candidates}", "hard"),
            ("P228_CURRENT_LABEL_SET_CLOSED", len(closure) == 1 and current_closed_fit == 1 and current_closed_replay == 1, f"closure_rows={len(closure)}; closed_fit={current_closed_fit}; closed_replay={current_closed_replay}", "hard"),
            ("P228_REDESIGN_CATALOG_RECORDED", len(redesign) == 3 and selected_rows == 1, f"redesign_rows={len(redesign)}; selected_rows={selected_rows}", "hard"),
            ("P228_GUARDRAILS_RECORDED", len(guardrails) == 3 and guardrails["required_in_phase229"].astype(int).eq(1).all(), f"guardrail_rows={len(guardrails)}", "hard"),
            ("P228_PHASE229_WORK_ORDER_RECORDED", len(work_order) == 1, f"work_order_rows={len(work_order)}", "hard"),
            ("P228_FORBIDDEN_OUTPUTS_CLEAN", forbidden_emitted == 0 and forbidden_flags == 0, f"forbidden_emitted={forbidden_emitted}; forbidden_flags={forbidden_flags}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(closure: pd.DataFrame, redesign: pd.DataFrame, guardrails: pd.DataFrame, work_order: pd.DataFrame, forbidden: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("phase228_closure_rows", len(closure), "Closure decision rows"),
            ("phase228_current_label_set_closed_for_fit", int(pd.to_numeric(closure["current_label_set_closed_for_fit"], errors="coerce").fillna(0).sum()) if not closure.empty else 0, "Current label set closed for fit"),
            ("phase228_current_label_set_closed_for_replay", int(pd.to_numeric(closure["current_label_set_closed_for_replay"], errors="coerce").fillna(0).sum()) if not closure.empty else 0, "Current label set closed for replay"),
            ("phase228_redesign_route_rows", len(redesign), "Redesign route rows"),
            ("phase228_guardrail_rows", len(guardrails), "Guardrail rows"),
            ("phase228_phase229_work_order_rows", len(work_order), "Phase229 work-order rows"),
            ("phase228_selected_route_id", SELECTED_ROUTE_ID, "Selected Phase229 route"),
            ("phase228_label_materialization_allowed_next", 0, "No label materialization opened"),
            ("phase228_model_fit_allowed_next", 0, "No model fit opened"),
            ("phase228_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase228_broader_replay_allowed_next", 0, "No broader replay opened"),
            ("phase228_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase228_test_rows_used", 0, "No sealed test rows used"),
            ("phase228_threshold_widening_allowed", 0, "No threshold widening opened"),
            ("phase228_promotion_allowed", 0, "No promotion opened"),
            ("phase228_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase228_profitability_claim_allowed", 0, "No profitability claim is allowed"),
            ("phase228_forbidden_execution_rows", len(forbidden), "Forbidden execution rows"),
            ("phase228_gate_rows", len(gates), "Gates evaluated"),
            ("phase228_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase228_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase228_cost_aware_label_redesign_closure_or_relaxation_precommit_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase228 completed"),
            ("phase228_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase228_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase228 Cost-aware Label Redesign Closure or Relaxation Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase228 closes the current sparse cost-aware label set for fit/replay and precommits a materially different source-expansion route.",
        "It does not materialize labels, fit models, run replay, widen thresholds, touch sealed test, or make profitability claims.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase228_cost_aware_label_redesign_closure_or_relaxation_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase228(phase227_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase227 = read_csv(phase227_dir / "phase227_quality_interpretation_acceptance_summary.csv")
    horizon = read_csv(phase227_dir / "phase227_horizon_interpretation.csv")
    closure = build_closure_decision(phase227, horizon)
    redesign = build_redesign_catalog()
    guardrails = build_guardrail_ledger()
    work_order = build_phase229_work_order(redesign, guardrails)
    forbidden = build_forbidden_execution_ledger()
    gates = build_gates(phase227, closure, redesign, guardrails, work_order, forbidden)
    acceptance = build_acceptance(closure, redesign, guardrails, work_order, forbidden, gates)

    closure.to_csv(output_dir / "phase228_closure_decision.csv", index=False)
    redesign.to_csv(output_dir / "phase228_redesign_route_catalog.csv", index=False)
    guardrails.to_csv(output_dir / "phase228_guardrail_ledger.csv", index=False)
    work_order.to_csv(output_dir / "phase228_phase229_work_order.csv", index=False)
    forbidden.to_csv(output_dir / "phase228_execution_forbidden_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase228_closure_or_relaxation_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase228_closure_or_relaxation_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Closure Decision": closure,
            "Redesign Route Catalog": redesign,
            "Guardrail Ledger": guardrails,
            "Phase229 Work Order": work_order,
            "Forbidden Execution Ledger": forbidden,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase228_cost_aware_label_redesign_closure_or_relaxation_precommit_no_fit_no_replay_no_test",
        **reproducibility_fields(
            artifact_id="phase228_cost_aware_label_redesign_closure_or_relaxation_precommit",
            generated_utc=generated,
            inputs={
                "phase227_acceptance": str(phase227_dir / "phase227_quality_interpretation_acceptance_summary.csv"),
                "phase227_horizon_interpretation": str(phase227_dir / "phase227_horizon_interpretation.csv"),
            },
            parameters={
                "selected_route_id": SELECTED_ROUTE_ID,
                "threshold_widening_allowed": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "closure": str(output_dir / "phase228_closure_decision.csv"),
                "redesign": str(output_dir / "phase228_redesign_route_catalog.csv"),
                "guardrails": str(output_dir / "phase228_guardrail_ledger.csv"),
                "work_order": str(output_dir / "phase228_phase229_work_order.csv"),
                "forbidden": str(output_dir / "phase228_execution_forbidden_ledger.csv"),
                "gates": str(output_dir / "phase228_closure_or_relaxation_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase228_closure_or_relaxation_acceptance_summary.csv"),
                "report": str(output_dir / "phase228_cost_aware_label_redesign_closure_or_relaxation_precommit_report.md"),
            },
            scenario_ids="phase228_cost_aware_label_redesign_closure_or_relaxation_precommit_no_fit_no_replay_no_test",
            cost_model_version="phase180_zerodha_equity_cost_component_catalog_bound",
            latency_model_version="phase180_latency_slippage_profile_catalog_bound",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase228_closure_or_relaxation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Precommit Phase228 cost-aware label closure or source expansion without materialization, fit, replay, or test.")
    parser.add_argument("--phase227-dir", type=Path, default=DEFAULT_PHASE227_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase228(args.phase227_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
