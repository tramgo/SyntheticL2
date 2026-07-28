from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE200_DIR = Path("outputs/phase200")
DEFAULT_PHASE201_DIR = Path("outputs/phase201")
DEFAULT_PHASE202_DIR = Path("outputs/phase202")
DEFAULT_PHASE203_DIR = Path("outputs/phase203")
DEFAULT_OUTPUT_DIR = Path("outputs/phase204")
FORBIDDEN_OUTPUTS = "strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening"


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


def build_evidence_ledger(inputs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    p200 = inputs["phase200"]
    p201 = inputs["phase201"]
    p202 = inputs["phase202"]
    p203 = inputs["phase203"]
    return pd.DataFrame(
        [
            {
                "phase": 200,
                "milestone": "passive_queue_position_hypothesis_precommit",
                "status": "complete" if as_int(metric_value(p200, "phase200_material_new_hypothesis_precommit_complete", 0)) else "missing",
                "key_evidence": f"selected_hypothesis={metric_value(p200, 'phase200_selected_hypothesis_id', '')}; label_contract_rows={metric_value(p200, 'phase200_label_contract_rows', '')}",
                "candidate_gate_open": 0,
                "strategy_replay_allowed": as_int(metric_value(p200, "phase200_strategy_replay_allowed", 0)),
                "test_replay_allowed_next": as_int(metric_value(p200, "phase200_test_replay_allowed_next", 0)),
            },
            {
                "phase": 201,
                "milestone": "passive_queue_stage01_label_expansion",
                "status": "complete_no_pre_replay_candidate" if as_int(metric_value(p201, "phase201_label_only_stage01_complete", 0)) else "missing",
                "key_evidence": f"joined_rows={metric_value(p201, 'phase201_joined_label_candidate_rows', '')}; pre_replay_candidates={metric_value(p201, 'phase201_pre_replay_candidate_rows', '')}; dominant_failure={metric_value(p201, 'phase201_dominant_failure_reason', '')}",
                "candidate_gate_open": as_int(metric_value(p201, "phase201_pre_replay_candidate_rows", 0)) > 0,
                "strategy_replay_allowed": as_int(metric_value(p201, "phase201_strategy_replay_allowed", 0)),
                "test_replay_allowed_next": as_int(metric_value(p201, "phase201_test_replay_allowed_next", 0)),
            },
            {
                "phase": 202,
                "milestone": "passive_feature_redesign_precommit",
                "status": "complete" if as_int(metric_value(p202, "phase202_passive_feature_redesign_precommit_complete", 0)) else "missing",
                "key_evidence": f"redesigned_features={metric_value(p202, 'phase202_redesigned_feature_rows', '')}; acceptance_contract_rows={metric_value(p202, 'phase202_acceptance_contract_rows', '')}",
                "candidate_gate_open": 0,
                "strategy_replay_allowed": as_int(metric_value(p202, "phase202_strategy_replay_allowed", 0)),
                "test_replay_allowed_next": as_int(metric_value(p202, "phase202_test_replay_allowed_next", 0)),
            },
            {
                "phase": 203,
                "milestone": "redesigned_passive_label_materialization",
                "status": "complete_candidate_gate_closed" if as_int(metric_value(p203, "phase203_label_materialization_complete", 0)) and as_int(metric_value(p203, "phase203_candidate_gate_open", 0)) == 0 else "complete_candidate_gate_open" if as_int(metric_value(p203, "phase203_label_materialization_complete", 0)) else "missing",
                "key_evidence": f"materialized_rows={metric_value(p203, 'phase203_materialized_label_rows', '')}; redesigned_pass_rows={metric_value(p203, 'phase203_redesigned_candidate_pass_rows', '')}; adverse_ceiling_met={metric_value(p203, 'phase203_adverse_selection_ceiling_met', '')}; max_symbols={metric_value(p203, 'phase203_max_candidate_symbols', '')}; max_dates={metric_value(p203, 'phase203_max_candidate_trade_dates', '')}",
                "candidate_gate_open": as_int(metric_value(p203, "phase203_candidate_gate_open", 0)),
                "strategy_replay_allowed": as_int(metric_value(p203, "phase203_strategy_replay_allowed", 0)),
                "test_replay_allowed_next": as_int(metric_value(p203, "phase203_test_replay_allowed_next", 0)),
            },
        ]
    )


def build_closure_decision(evidence: pd.DataFrame, phase203: pd.DataFrame) -> pd.DataFrame:
    all_replay_closed = int(
        evidence["strategy_replay_allowed"].astype(int).eq(0).all()
        and evidence["test_replay_allowed_next"].astype(int).eq(0).all()
    )
    candidate_gate_open = as_int(metric_value(phase203, "phase203_candidate_gate_open", 0))
    adverse_ceiling_met = as_int(metric_value(phase203, "phase203_adverse_selection_ceiling_met", 0))
    stability_rows = as_int(metric_value(phase203, "phase203_symbol_month_stability_requirement_rows", 0))
    decision = "close_current_passive_queue_redesign_for_replay_require_material_new_source_or_broader_labels"
    return pd.DataFrame(
        [
            {
                "decision_id": "P204_PASSIVE_QUEUE_REDESIGN_CLOSURE_DECISION",
                "branch": "real_receive_flow_source",
                "phase204_decision": decision,
                "phase203_candidate_gate_open": candidate_gate_open,
                "phase203_adverse_selection_ceiling_met": adverse_ceiling_met,
                "phase203_symbol_month_stability_requirement_rows": stability_rows,
                "all_replay_gates_closed": all_replay_closed,
                "current_passive_redesign_closed_for_replay": int(candidate_gate_open == 0 and all_replay_closed == 1),
                "threshold_widening_allowed": 0,
                "material_new_source_required": 1,
                "broader_label_materialization_allowed": 1,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "rationale": (
                    "Phase203 materialized the redesigned labels over 696 Stage01 candidates but found zero redesigned "
                    "candidate pass rows. Toxicity abstention, symbol/month stability and cancel-guard labels all failed, "
                    "so the passive queue redesign cannot proceed to replay without a materially new source or broader "
                    "label-only evidence."
                ),
            }
        ]
    )


def build_next_research_queue() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "queue_rank": 1,
                "next_item": "precommit_non_passive_external_orderflow_or_context_source",
                "recommended_phase": "Phase205",
                "why": "The passive queue branch failed toxicity and breadth after redesign; the next synthetic-only route must use a materially different source.",
                "allowed_scope": "precommit_only_no_replay",
                "strategy_replay_allowed": 0,
            },
            {
                "queue_rank": 2,
                "next_item": "expand_redesigned_passive_label_materialization_breadth",
                "recommended_phase": "Phase205_alt",
                "why": "Only label-only expansion is allowed if we stay with passive labels; it must target adverse-selection ceiling and at least 8 symbols before replay precommit.",
                "allowed_scope": "label_only_no_replay",
                "strategy_replay_allowed": 0,
            },
            {
                "queue_rank": 3,
                "next_item": "return_to_real_anchor_microstructure_calibration",
                "recommended_phase": "real_anchor",
                "why": "Real L2 remains the strongest source for realistic cadence/depth calibration and should be downloaded first, then analyzed locally.",
                "allowed_scope": "local_data_audit_no_strategy_replay",
                "strategy_replay_allowed": 0,
            },
        ]
    )


def build_guardrail_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "contract_id": "P204_NO_PASSIVE_REPLAY_FROM_ZERO_CANDIDATE_GATE",
                "requirement": "Do not run passive strategy replay while Phase203 candidate_gate_open is 0.",
                "required_next": 1,
            },
            {
                "contract_id": "P204_NO_THRESHOLD_WIDENING",
                "requirement": "Do not rescue Phase203 by relaxing toxicity, breadth or cancel-guard thresholds after observing label outcomes.",
                "required_next": 1,
            },
            {
                "contract_id": "P204_MATERIAL_NEW_SOURCE_OR_BREADTH_REQUIRED",
                "requirement": "Any continuation must either precommit a materially new non-passive source or expand labels before replay.",
                "required_next": 1,
            },
            {
                "contract_id": "P204_COST_LATENCY_REBIND_REQUIRED",
                "requirement": "Any future candidate must rebind Zerodha-style costs and latency before P&L or acceptance interpretation.",
                "required_next": 1,
            },
        ]
    )


def build_gates(evidence: pd.DataFrame, decision: pd.DataFrame, queue: pd.DataFrame, guardrails: pd.DataFrame) -> pd.DataFrame:
    row = decision.iloc[0] if not decision.empty else {}
    return pd.DataFrame(
        [
            ("P204_PHASE200_203_EVIDENCE_RECORDED", len(evidence) == 4, f"evidence_rows={len(evidence)}", "hard"),
            ("P204_PHASE203_GATE_CLOSED_ACKNOWLEDGED", as_int(row.get("phase203_candidate_gate_open", 1)) == 0, f"candidate_gate_open={row.get('phase203_candidate_gate_open', '')}", "hard"),
            ("P204_PASSIVE_REDESIGN_CLOSED_FOR_REPLAY", as_int(row.get("current_passive_redesign_closed_for_replay", 0)) == 1, f"closed_for_replay={row.get('current_passive_redesign_closed_for_replay', '')}", "hard"),
            ("P204_NEXT_QUEUE_RECORDED", len(queue) >= 3 and queue["strategy_replay_allowed"].astype(int).eq(0).all(), f"queue_rows={len(queue)}", "hard"),
            ("P204_GUARDRAIL_CONTRACT_RECORDED", len(guardrails) >= 4 and guardrails["required_next"].astype(int).eq(1).all(), f"guardrail_rows={len(guardrails)}", "hard"),
            ("P204_NO_REPLAY_OR_PROMOTION", as_int(row.get("strategy_replay_allowed", 1)) == 0 and as_int(row.get("test_replay_allowed_next", 1)) == 0 and as_int(row.get("promotion_allowed", 1)) == 0 and as_int(row.get("paper_or_live_acceptance_allowed", 1)) == 0, "strategy_replay=0; test_replay=0; promotion=0; paper_live=0", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(decision: pd.DataFrame, evidence: pd.DataFrame, queue: pd.DataFrame, guardrails: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    row = decision.iloc[0] if not decision.empty else {}
    return pd.DataFrame(
        [
            ("phase204_evidence_rows", len(evidence), "Phase200-203 evidence rows"),
            ("phase204_decision_rows", len(decision), "Decision rows"),
            ("phase204_next_queue_rows", len(queue), "Next research queue rows"),
            ("phase204_guardrail_rows", len(guardrails), "Guardrail contract rows"),
            ("phase204_decision", row.get("phase204_decision", ""), "Branch decision"),
            ("phase204_current_passive_redesign_closed_for_replay", row.get("current_passive_redesign_closed_for_replay", ""), "1 means current passive redesign closed for replay"),
            ("phase204_material_new_source_required", row.get("material_new_source_required", ""), "1 means next source must be materially new unless label breadth expands first"),
            ("phase204_broader_label_materialization_allowed", row.get("broader_label_materialization_allowed", ""), "1 means label-only breadth expansion remains allowed"),
            ("phase204_threshold_widening_allowed", row.get("threshold_widening_allowed", ""), "0 means threshold widening is forbidden"),
            ("phase204_gate_rows", len(gates), "Gates evaluated"),
            ("phase204_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase204_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase204_closure_decision_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase204 completed"),
            ("phase204_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase204_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase204_promotion_allowed", 0, "No promotion opened"),
            ("phase204_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase204_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase204_next_best_action", "run_phase205_material_new_source_precommit_or_label_breadth_plan_no_replay", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase204 Passive Redesign Closure Decision",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase204 records the post-Phase203 decision: the current passive queue redesign is closed for replay.",
        "It emits a guarded next queue and does not run replay, tests, orders, fills, P&L, promotion, or paper/live acceptance.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase204_passive_redesign_closure_decision_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase204(
    phase200_dir: Path,
    phase201_dir: Path,
    phase202_dir: Path,
    phase203_dir: Path,
    output_dir: Path,
    base_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    inputs = {
        "phase200": read_csv(phase200_dir / "phase200_material_new_hypothesis_acceptance_summary.csv"),
        "phase201": read_csv(phase201_dir / "phase201_stage01_acceptance_summary.csv"),
        "phase202": read_csv(phase202_dir / "phase202_passive_feature_redesign_acceptance_summary.csv"),
        "phase203": read_csv(phase203_dir / "phase203_redesigned_passive_label_acceptance_summary.csv"),
    }
    evidence = build_evidence_ledger(inputs)
    decision = build_closure_decision(evidence, inputs["phase203"])
    queue = build_next_research_queue()
    guardrails = build_guardrail_contract()
    gates = build_gates(evidence, decision, queue, guardrails)
    acceptance = build_acceptance(decision, evidence, queue, guardrails, gates)

    evidence.to_csv(output_dir / "phase204_passive_redesign_evidence_ledger.csv", index=False)
    decision.to_csv(output_dir / "phase204_passive_redesign_closure_decision.csv", index=False)
    queue.to_csv(output_dir / "phase204_next_research_queue.csv", index=False)
    guardrails.to_csv(output_dir / "phase204_guardrail_contract.csv", index=False)
    gates.to_csv(output_dir / "phase204_passive_redesign_closure_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase204_passive_redesign_closure_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Evidence Ledger": evidence,
            "Closure Decision": decision,
            "Next Research Queue": queue,
            "Guardrail Contract": guardrails,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase204_passive_redesign_closure_decision_no_replay",
        **reproducibility_fields(
            artifact_id="phase204_passive_redesign_closure_decision",
            generated_utc=generated,
            inputs={
                "phase200_acceptance": str(phase200_dir / "phase200_material_new_hypothesis_acceptance_summary.csv"),
                "phase201_acceptance": str(phase201_dir / "phase201_stage01_acceptance_summary.csv"),
                "phase202_acceptance": str(phase202_dir / "phase202_passive_feature_redesign_acceptance_summary.csv"),
                "phase203_acceptance": str(phase203_dir / "phase203_redesigned_passive_label_acceptance_summary.csv"),
            },
            parameters={
                "decision_scope": "close_current_passive_queue_redesign_for_replay",
                "threshold_widening_allowed": "0",
                "strategy_replay_allowed": "0",
                "test_replay_allowed_next": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "evidence": str(output_dir / "phase204_passive_redesign_evidence_ledger.csv"),
                "decision": str(output_dir / "phase204_passive_redesign_closure_decision.csv"),
                "queue": str(output_dir / "phase204_next_research_queue.csv"),
                "guardrails": str(output_dir / "phase204_guardrail_contract.csv"),
                "gates": str(output_dir / "phase204_passive_redesign_closure_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase204_passive_redesign_closure_acceptance_summary.csv"),
                "report": str(output_dir / "phase204_passive_redesign_closure_decision_report.md"),
            },
            scenario_ids="phase204_passive_redesign_closure_decision_no_replay",
            cost_model_version="not_applicable_no_strategy_replay",
            latency_model_version="not_applicable_no_strategy_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase204_passive_redesign_closure_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Record Phase204 passive redesign closure decision without replay.")
    parser.add_argument("--phase200-dir", type=Path, default=DEFAULT_PHASE200_DIR)
    parser.add_argument("--phase201-dir", type=Path, default=DEFAULT_PHASE201_DIR)
    parser.add_argument("--phase202-dir", type=Path, default=DEFAULT_PHASE202_DIR)
    parser.add_argument("--phase203-dir", type=Path, default=DEFAULT_PHASE203_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase204(args.phase200_dir, args.phase201_dir, args.phase202_dir, args.phase203_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
