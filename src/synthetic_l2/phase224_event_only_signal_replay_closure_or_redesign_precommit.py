from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE223_DIR = Path("outputs/phase223")
DEFAULT_OUTPUT_DIR = Path("outputs/phase224")
FORBIDDEN_OUTPUTS = "model_fit;model_prediction;strategy_replay;broader_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export"
NEXT_ACTION = "run_phase225_cost_aware_event_source_redesign_precommit_no_fit_no_replay_no_test"


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


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def build_candidate_set_closure(phase223: pd.DataFrame, interpretation: pd.DataFrame) -> pd.DataFrame:
    positive_rows = as_int(metric_value(phase223, "phase223_positive_net_validation_rows", 0))
    passing_rows = as_int(metric_value(phase223, "phase223_passing_interpretation_rows", 0))
    best_net = as_float(metric_value(phase223, "phase223_best_validation_net_after_cost_bps_proxy", 0.0))
    best_shuffle_edge = as_float(metric_value(phase223, "phase223_best_actual_vs_shuffle_net_edge_bps", 0.0))
    interpreted_candidates = int(interpretation["phase221_candidate_id"].astype(str).nunique()) if not interpretation.empty and "phase221_candidate_id" in interpretation.columns else 0
    interpreted_targets = int((interpretation["target_label"].astype(str) + "_H" + interpretation["horizon_sec"].astype(str)).nunique()) if not interpretation.empty and {"target_label", "horizon_sec"}.issubset(interpretation.columns) else 0
    return pd.DataFrame(
        [
            {
                "phase224_closure_id": "P224_CLOSE_PHASE221_EVENT_ONLY_SIGNAL_REPLAY_CANDIDATE_SET",
                "closed_candidate_set": "phase221_frozen_event_only_signal_replay_candidates",
                "interpreted_candidate_rows": interpreted_candidates,
                "interpreted_target_horizon_rows": interpreted_targets,
                "phase223_positive_net_validation_rows": positive_rows,
                "phase223_passing_interpretation_rows": passing_rows,
                "best_validation_net_after_cost_bps_proxy": best_net,
                "best_actual_vs_shuffle_net_edge_bps": best_shuffle_edge,
                "closed_for_broader_replay": 1,
                "closed_for_test_replay": 1,
                "reuse_without_material_redesign_allowed": 0,
                "closure_reason": "zerodha_cost_bound_validation_interpretation_has_zero_positive_net_rows_and_zero_passing_rows",
                "strategy_replay_allowed": 0,
                "broader_replay_allowed_next": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "profitability_claim_allowed": 0,
            }
        ]
    )


def build_failure_mode_ledger(phase223: pd.DataFrame, interpretation: pd.DataFrame) -> pd.DataFrame:
    best_net = as_float(metric_value(phase223, "phase223_best_validation_net_after_cost_bps_proxy", 0.0))
    worst_net = as_float(metric_value(phase223, "phase223_worst_validation_net_after_cost_bps_proxy", 0.0))
    best_shuffle_edge = as_float(metric_value(phase223, "phase223_best_actual_vs_shuffle_net_edge_bps", 0.0))
    positive_rows = as_int(metric_value(phase223, "phase223_positive_net_validation_rows", 0))
    passing_rows = as_int(metric_value(phase223, "phase223_passing_interpretation_rows", 0))
    decision_events = as_int(metric_value(phase223, "phase223_validation_decision_events", 0))
    cost_dominates_rows = as_int(metric_value(phase223, "phase223_cost_dominates_rows", 0))
    sparse_rows = 0
    if not interpretation.empty and "decision_events" in interpretation.columns:
        sparse_rows = int(pd.to_numeric(interpretation["decision_events"], errors="coerce").fillna(0).eq(0).sum())
    return pd.DataFrame(
        [
            {
                "phase224_failure_mode_id": "P224_COST_NEGATIVE_AFTER_ZERODHA_BOUNDS",
                "failure_mode": "validation_replay_edge_is_not_positive_after_zerodha_cost_and_latency_bounds",
                "affected_rows": len(interpretation),
                "evidence": f"best_net_bps={best_net}; worst_net_bps={worst_net}; positive_rows={positive_rows}; passing_rows={passing_rows}",
                "redesign_implication": "Future source must estimate actionable edge large enough to exceed statutory costs, spread, latency, and slippage before any replay precommit.",
                "strategy_replay_allowed": 0,
            },
            {
                "phase224_failure_mode_id": "P224_SIGNAL_CONTROL_EDGE_NOT_ACTIONABLE",
                "failure_mode": "actual_vs_shuffled_label_edge_exists_but_is_not_actionable_after_cost",
                "affected_rows": len(interpretation),
                "evidence": f"best_actual_vs_shuffle_net_edge_bps={best_shuffle_edge}; best_net_bps={best_net}",
                "redesign_implication": "Do not treat statistical edge as trading edge unless the net-after-cost hurdle is positive under retail and stressed profiles.",
                "strategy_replay_allowed": 0,
            },
            {
                "phase224_failure_mode_id": "P224_THRESHOLD_ACTIVITY_UNBALANCED",
                "failure_mode": "fixed_threshold_grid_activity_is_sparse_or_concentrated_in_non_directional_targets",
                "affected_rows": sparse_rows,
                "evidence": f"validation_decision_events={decision_events}; zero_decision_interpretation_rows={sparse_rows}",
                "redesign_implication": "Future labels/signals should include an ex-ante actionability hurdle and minimum effective sample size rather than widening thresholds post hoc.",
                "strategy_replay_allowed": 0,
            },
            {
                "phase224_failure_mode_id": "P224_COST_DOMINATES_GROSS_PROXY",
                "failure_mode": "cost_bound_dominates_gross_proxy_edge_for_material_rows",
                "affected_rows": cost_dominates_rows,
                "evidence": f"cost_dominates_rows={cost_dominates_rows}",
                "redesign_implication": "Future candidate generation must be cost-aware at label construction time, not just at replay interpretation time.",
                "strategy_replay_allowed": 0,
            },
        ]
    )


def build_redesign_route_catalog() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "phase224_redesign_route_id": "P224_COST_AWARE_ACTIONABLE_EVENT_LABELS",
                "redesign_theme": "cost_aware_label_source",
                "precommit_action": "Define event labels only when forward move potential exceeds a frozen Zerodha cost-plus-slippage hurdle before model fitting.",
                "why_materially_different": "Moves cost from post-replay interpretation into the target definition so candidates must be economically actionable before selection.",
                "required_before_fit_or_replay": "cost_hurdle_label_contract;train_validation_only_materialization;negative_control_labels;minimum_event_count_gate",
                "phase225_candidate": 1,
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            },
            {
                "phase224_redesign_route_id": "P224_SELECTIVITY_AND_COOLDOWN_SIGNAL_SOURCE",
                "redesign_theme": "turnover_suppression_source",
                "precommit_action": "Precommit signal features/labels with cooldown, persistence, and liquidity filters to reduce event churn before replay.",
                "why_materially_different": "Targets fewer higher-conviction decisions rather than dense activations that are eaten by spread and statutory costs.",
                "required_before_fit_or_replay": "cooldown_contract;persistence_contract;liquidity_gate_contract;train_validation_activation_budget",
                "phase225_candidate": 1,
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            },
            {
                "phase224_redesign_route_id": "P224_EXECUTION_AWARE_PASSIVE_OR_MIDPOINT_PROXY",
                "redesign_theme": "execution_mechanism_source",
                "precommit_action": "Evaluate whether passive queue-aware or midpoint-improvement proxy labels can overcome the retail marketable cost wall without assuming impossible fills.",
                "why_materially_different": "Changes the execution premise rather than trying to force marketable event signals through a negative cost surface.",
                "required_before_fit_or_replay": "fill_feasibility_contract;queue_position_proxy;nonfill_penalty;no_contract_note_acceptance_boundary",
                "phase225_candidate": 1,
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            },
        ]
    )


def build_phase225_work_order(redesign: pd.DataFrame) -> pd.DataFrame:
    selected_route = "P224_COST_AWARE_ACTIONABLE_EVENT_LABELS"
    selected = redesign[redesign["phase224_redesign_route_id"].astype(str).eq(selected_route)] if not redesign.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            {
                "phase225_work_order_id": "P225_COST_AWARE_EVENT_SOURCE_REDESIGN_PRECOMMIT",
                "work_order": "Precommit a cost-aware event source redesign before any model fit, replay, broader replay, or sealed test.",
                "selected_route_id": selected_route,
                "selected_route_theme": selected["redesign_theme"].iloc[0] if not selected.empty else "cost_aware_label_source",
                "required_artifacts": selected["required_before_fit_or_replay"].iloc[0] if not selected.empty else "cost_hurdle_label_contract;negative_controls;minimum_event_count_gate",
                "allowed_next_scope": "source_redesign_precommit_only_no_fit_no_replay_no_test",
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
                "emitted_in_phase224": 0,
                "allowed_in_phase224": 0,
                "rationale": "Phase224 closes or redesign-precommits only; it emits no model fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, row-level prediction, threshold-widening, or profitability artifact.",
            }
            for item in FORBIDDEN_OUTPUTS.split(";")
        ]
    )


def build_gates(phase223: pd.DataFrame, closure: pd.DataFrame, failure: pd.DataFrame, redesign: pd.DataFrame, work_order: pd.DataFrame, forbidden: pd.DataFrame) -> pd.DataFrame:
    phase223_complete = as_int(metric_value(phase223, "phase223_event_only_signal_replay_validation_interpretation_complete", 0))
    positive_rows = as_int(metric_value(phase223, "phase223_positive_net_validation_rows", 0))
    passing_rows = as_int(metric_value(phase223, "phase223_passing_interpretation_rows", 0))
    closed_for_broader = int(pd.to_numeric(closure["closed_for_broader_replay"], errors="coerce").fillna(0).sum()) if not closure.empty else 0
    closed_for_test = int(pd.to_numeric(closure["closed_for_test_replay"], errors="coerce").fillna(0).sum()) if not closure.empty else 0
    reuse_allowed = int(pd.to_numeric(closure["reuse_without_material_redesign_allowed"], errors="coerce").fillna(0).sum()) if not closure.empty else 1
    redesign_candidates = int(pd.to_numeric(redesign["phase225_candidate"], errors="coerce").fillna(0).sum()) if not redesign.empty else 0
    forbidden_emitted = int(pd.to_numeric(forbidden["emitted_in_phase224"], errors="coerce").fillna(0).sum()) if not forbidden.empty else 1
    forbidden_flags = 0
    for frame in [closure, failure, redesign, work_order]:
        for col in [
            "model_fit_allowed_now",
            "model_fit_allowed_next",
            "strategy_replay_allowed",
            "broader_replay_allowed_next",
            "test_replay_allowed_next",
            "promotion_allowed",
            "paper_or_live_acceptance_allowed",
            "profitability_claim_allowed",
        ]:
            if not frame.empty and col in frame.columns:
                forbidden_flags += int(pd.to_numeric(frame[col], errors="coerce").fillna(0).sum())
    return pd.DataFrame(
        [
            ("P224_PHASE223_COMPLETE", phase223_complete == 1, f"phase223_complete={phase223_complete}", "hard"),
            ("P224_PHASE223_NO_COST_POSITIVE_ROWS", positive_rows == 0 and passing_rows == 0, f"positive_rows={positive_rows}; passing_rows={passing_rows}", "hard"),
            ("P224_CURRENT_CANDIDATE_SET_CLOSED", len(closure) == 1 and closed_for_broader == 1 and closed_for_test == 1 and reuse_allowed == 0, f"closure_rows={len(closure)}; closed_for_broader={closed_for_broader}; closed_for_test={closed_for_test}; reuse_allowed={reuse_allowed}", "hard"),
            ("P224_FAILURE_MODES_RECORDED", len(failure) == 4, f"failure_rows={len(failure)}", "hard"),
            ("P224_MATERIAL_REDESIGN_ROUTES_RECORDED", len(redesign) == 3 and redesign_candidates == 3, f"redesign_rows={len(redesign)}; candidates={redesign_candidates}", "hard"),
            ("P224_PHASE225_WORK_ORDER_RECORDED", len(work_order) == 1, f"work_order_rows={len(work_order)}", "hard"),
            ("P224_FORBIDDEN_OUTPUTS_CLEAN", forbidden_emitted == 0 and forbidden_flags == 0, f"forbidden_emitted={forbidden_emitted}; forbidden_flags={forbidden_flags}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(phase223: pd.DataFrame, closure: pd.DataFrame, failure: pd.DataFrame, redesign: pd.DataFrame, work_order: pd.DataFrame, forbidden: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("phase224_closure_rows", len(closure), "Candidate-set closure rows"),
            ("phase224_current_candidate_set_closed_for_broader_replay", int(pd.to_numeric(closure["closed_for_broader_replay"], errors="coerce").fillna(0).sum()) if not closure.empty else 0, "Current candidate set closed for broader replay"),
            ("phase224_current_candidate_set_closed_for_test", int(pd.to_numeric(closure["closed_for_test_replay"], errors="coerce").fillna(0).sum()) if not closure.empty else 0, "Current candidate set closed for sealed test replay"),
            ("phase224_reuse_without_material_redesign_allowed", int(pd.to_numeric(closure["reuse_without_material_redesign_allowed"], errors="coerce").fillna(0).sum()) if not closure.empty else 0, "Reuse without material redesign allowed"),
            ("phase224_failure_mode_rows", len(failure), "Failure-mode rows"),
            ("phase224_redesign_route_rows", len(redesign), "Material redesign route rows"),
            ("phase224_phase225_work_order_rows", len(work_order), "Phase225 work-order rows"),
            ("phase224_selected_redesign_route", work_order["selected_route_id"].iloc[0] if not work_order.empty else "", "Selected Phase225 redesign route"),
            ("phase224_phase223_positive_net_validation_rows", as_int(metric_value(phase223, "phase223_positive_net_validation_rows", 0)), "Phase223 positive net validation rows"),
            ("phase224_phase223_passing_interpretation_rows", as_int(metric_value(phase223, "phase223_passing_interpretation_rows", 0)), "Phase223 passing interpretation rows"),
            ("phase224_forbidden_execution_rows", len(forbidden), "Forbidden execution rows"),
            ("phase224_gate_rows", len(gates), "Gates evaluated"),
            ("phase224_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase224_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase224_event_only_signal_replay_closure_or_redesign_precommit_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase224 completed"),
            ("phase224_model_fit_allowed_next", 0, "No model fit opened"),
            ("phase224_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase224_broader_replay_allowed_next", 0, "No broader replay opened"),
            ("phase224_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase224_promotion_allowed", 0, "No promotion opened"),
            ("phase224_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase224_profitability_claim_allowed", 0, "No profitability claim is allowed"),
            ("phase224_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase224_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase224 Event-only Signal Replay Closure or Redesign Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase224 closes the current Phase221/222/223 event-only signal replay candidate set for broader replay and sealed test.",
        "It records failure modes and a Phase225 material redesign work order without fitting models, running replay, widening thresholds, or making profitability claims.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase224_event_only_signal_replay_closure_or_redesign_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase224(phase223_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase223 = read_csv(phase223_dir / "phase223_validation_interpretation_acceptance_summary.csv")
    interpretation = read_csv(phase223_dir / "phase223_validation_interpretation.csv")
    work_order_223 = read_csv(phase223_dir / "phase223_phase224_work_order.csv")

    closure = build_candidate_set_closure(phase223, interpretation)
    failure = build_failure_mode_ledger(phase223, interpretation)
    redesign = build_redesign_route_catalog()
    work_order = build_phase225_work_order(redesign)
    forbidden = build_forbidden_execution_ledger()
    gates = build_gates(phase223, closure, failure, redesign, work_order, forbidden)
    acceptance = build_acceptance(phase223, closure, failure, redesign, work_order, forbidden, gates)

    closure.to_csv(output_dir / "phase224_candidate_set_closure_ledger.csv", index=False)
    failure.to_csv(output_dir / "phase224_failure_mode_ledger.csv", index=False)
    redesign.to_csv(output_dir / "phase224_redesign_route_catalog.csv", index=False)
    work_order.to_csv(output_dir / "phase224_phase225_work_order.csv", index=False)
    forbidden.to_csv(output_dir / "phase224_execution_forbidden_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase224_closure_or_redesign_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase224_closure_or_redesign_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Candidate-set Closure Ledger": closure,
            "Failure Mode Ledger": failure,
            "Redesign Route Catalog": redesign,
            "Phase225 Work Order": work_order,
            "Phase223 Work Order Input": work_order_223,
            "Forbidden Execution Ledger": forbidden,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase224_event_only_signal_replay_closure_or_redesign_precommit_no_test",
        **reproducibility_fields(
            artifact_id="phase224_event_only_signal_replay_closure_or_redesign_precommit",
            generated_utc=generated,
            inputs={
                "phase223_acceptance": str(phase223_dir / "phase223_validation_interpretation_acceptance_summary.csv"),
                "phase223_interpretation": str(phase223_dir / "phase223_validation_interpretation.csv"),
                "phase223_work_order": str(phase223_dir / "phase223_phase224_work_order.csv"),
            },
            parameters={
                "selected_phase225_route": "P224_COST_AWARE_ACTIONABLE_EVENT_LABELS",
                "broader_replay_allowed_next": "0",
                "test_replay_allowed_next": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "closure": str(output_dir / "phase224_candidate_set_closure_ledger.csv"),
                "failure": str(output_dir / "phase224_failure_mode_ledger.csv"),
                "redesign": str(output_dir / "phase224_redesign_route_catalog.csv"),
                "work_order": str(output_dir / "phase224_phase225_work_order.csv"),
                "forbidden": str(output_dir / "phase224_execution_forbidden_ledger.csv"),
                "gates": str(output_dir / "phase224_closure_or_redesign_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase224_closure_or_redesign_acceptance_summary.csv"),
                "report": str(output_dir / "phase224_event_only_signal_replay_closure_or_redesign_precommit_report.md"),
            },
            scenario_ids="phase224_event_only_signal_replay_closure_or_redesign_precommit_no_test",
            cost_model_version="phase180_zerodha_equity_cost_component_catalog_bound",
            latency_model_version="phase180_latency_slippage_profile_catalog_bound",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase224_closure_or_redesign_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Close Phase223 event-only signal replay candidate set or precommit redesign without replay/test.")
    parser.add_argument("--phase223-dir", type=Path, default=DEFAULT_PHASE223_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase224(args.phase223_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
