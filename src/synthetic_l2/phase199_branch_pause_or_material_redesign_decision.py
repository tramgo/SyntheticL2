from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE194_DIR = Path("outputs/phase194")
DEFAULT_PHASE195_DIR = Path("outputs/phase195")
DEFAULT_PHASE196_DIR = Path("outputs/phase196")
DEFAULT_PHASE197_DIR = Path("outputs/phase197")
DEFAULT_PHASE198_DIR = Path("outputs/phase198")
DEFAULT_OUTPUT_DIR = Path("outputs/phase199")
FORBIDDEN_OUTPUTS = "test_result;test_replay_execution;strategy_replay;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim"


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


def build_evidence_ledger(inputs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    p194 = inputs["phase194"]
    p195 = inputs["phase195"]
    p196 = inputs["phase196"]
    p197 = inputs["phase197"]
    p198 = inputs["phase198"]
    rows = [
        {
            "phase": 194,
            "milestone": "sparse_candidate_fragility_decision",
            "status": "closed_for_test_replay" if as_int(metric_value(p194, "phase194_fragility_decision_complete", 0)) else "missing",
            "key_evidence": f"all_extension_profile_dates_negative={metric_value(p194, 'phase194_all_extension_profile_dates_negative', '')}; test_replay_allowed_next={metric_value(p194, 'phase194_test_replay_allowed_next', '')}",
            "survivor_count": 0,
            "test_replay_allowed_next": as_int(metric_value(p194, "phase194_test_replay_allowed_next", 0)),
        },
        {
            "phase": 195,
            "milestone": "receive_flow_redesign_candidate_search",
            "status": "no_extension_gate_survivor" if as_int(metric_value(p195, "phase195_redesign_search_complete", 0)) else "missing",
            "key_evidence": f"grid_rows={metric_value(p195, 'phase195_redesigned_candidate_grid_rows', metric_value(p195, 'phase195_candidate_grid_rows', ''))}; train_selected={metric_value(p195, 'phase195_train_selected_candidate_rows', '')}; passing={metric_value(p195, 'phase195_passing_extension_gate_candidates', '')}",
            "survivor_count": as_int(metric_value(p195, "phase195_passing_extension_gate_candidates", 0)),
            "test_replay_allowed_next": as_int(metric_value(p195, "phase195_test_replay_allowed_next", 0)),
        },
        {
            "phase": 196,
            "milestone": "expanded_receive_flow_feature_model_search",
            "status": "no_train_survivor" if as_int(metric_value(p196, "phase196_expanded_model_search_complete", 0)) else "missing",
            "key_evidence": f"grid_rows={metric_value(p196, 'phase196_model_grid_rows', '')}; train_selected={metric_value(p196, 'phase196_train_selected_model_rows', '')}; passing={metric_value(p196, 'phase196_passing_extension_gate_models', '')}",
            "survivor_count": as_int(metric_value(p196, "phase196_passing_extension_gate_models", 0)),
            "test_replay_allowed_next": as_int(metric_value(p196, "phase196_test_replay_allowed_next", 0)),
        },
        {
            "phase": 197,
            "milestone": "non_receive_flow_feature_expansion_precommit",
            "status": "feature_expansion_ready" if as_int(metric_value(p197, "phase197_non_receive_flow_feature_precommit_complete", 0)) else "missing",
            "key_evidence": f"ready_feature_families={metric_value(p197, 'phase197_ready_feature_families', '')}; strategy_replay_allowed={metric_value(p197, 'phase197_strategy_replay_allowed', '')}",
            "survivor_count": as_int(metric_value(p197, "phase197_ready_feature_families", 0)),
            "test_replay_allowed_next": as_int(metric_value(p197, "phase197_test_replay_allowed_next", 0)),
        },
        {
            "phase": 198,
            "milestone": "non_receive_flow_context_model_search",
            "status": "no_train_survivor" if as_int(metric_value(p198, "phase198_context_model_search_complete", 0)) else "missing",
            "key_evidence": f"grid_rows={metric_value(p198, 'phase198_model_grid_rows', '')}; train_selected={metric_value(p198, 'phase198_train_selected_model_rows', '')}; passing={metric_value(p198, 'phase198_passing_extension_gate_models', '')}",
            "survivor_count": as_int(metric_value(p198, "phase198_passing_extension_gate_models", 0)),
            "test_replay_allowed_next": as_int(metric_value(p198, "phase198_test_replay_allowed_next", 0)),
        },
    ]
    return pd.DataFrame(rows)


def build_branch_decision(evidence: pd.DataFrame) -> pd.DataFrame:
    blocking = evidence.loc[evidence["phase"].isin([194, 195, 196, 198])].copy()
    no_survivor_or_closed = int((blocking["survivor_count"].astype(int).eq(0)).all())
    replay_closed = int(evidence["test_replay_allowed_next"].astype(int).eq(0).all())
    feature_expansion_ready = int(evidence.loc[evidence["phase"].eq(197), "survivor_count"].astype(int).max() if not evidence.loc[evidence["phase"].eq(197)].empty else 0)
    decision = "pause_current_receive_flow_context_branch_require_material_new_hypothesis"
    rationale = (
        "Phases194-198 close the current receive-flow/context line for untouched-test use: "
        "the sparse candidate was fragile, the redesigned threshold grid found no extension survivor, "
        "expanded receive-flow models found no train survivor, and broader context models also found no train survivor."
    )
    return pd.DataFrame(
        [
            {
                "decision_id": "P199_RECEIVE_FLOW_CONTEXT_BRANCH_DECISION",
                "branch": "real_receive_flow_source",
                "phase199_decision": decision,
                "no_survivor_or_closed_in_decision_phases": no_survivor_or_closed,
                "all_test_replay_gates_closed": replay_closed,
                "phase197_ready_feature_families": feature_expansion_ready,
                "current_branch_paused": int(no_survivor_or_closed == 1 and replay_closed == 1),
                "material_redesign_required": 1,
                "untouched_test_replay_precommit_allowed": 0,
                "test_replay_allowed_next": 0,
                "strategy_replay_allowed": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "rationale": rationale,
            }
        ]
    )


def build_material_redesign_contract() -> pd.DataFrame:
    rows = [
        {
            "contract_id": "P199_NEW_DATA_AXIS_REQUIRED",
            "requirement": "Any continuation must introduce a materially new data axis or target design, not another near-variant of receive cadence, imbalance, or first-pass context scoring.",
            "required_before_phase200_search": 1,
        },
        {
            "contract_id": "P199_TRAIN_ONLY_SELECTION_REQUIRED",
            "requirement": "Model/threshold selection must remain train-only; validation and validation-extension may reject candidates but may not fit or select them.",
            "required_before_phase200_search": 1,
        },
        {
            "contract_id": "P199_UNTOUCHED_TEST_STAYS_CLOSED",
            "requirement": "The untouched test split stays closed until a future precommit phase records a single frozen candidate and all branch-specific gates.",
            "required_before_phase200_search": 1,
        },
        {
            "contract_id": "P199_COST_LATENCY_BINDING_REQUIRED",
            "requirement": "Any future search must bind Phase180 cost and latency profiles before net metrics or acceptance interpretation.",
            "required_before_phase200_search": 1,
        },
        {
            "contract_id": "P199_NEGATIVE_CONTROLS_REQUIRED",
            "requirement": "Any future search must include shuffled-time or equivalent negative controls before interpreting edge.",
            "required_before_phase200_search": 1,
        },
        {
            "contract_id": "P199_DECISION_RATE_BUDGET_REQUIRED",
            "requirement": "Any future high-frequency strategy search must precommit a decision-rate budget and may not relax it after seeing validation results.",
            "required_before_phase200_search": 1,
        },
    ]
    return pd.DataFrame(rows)


def build_next_hypothesis_queue() -> pd.DataFrame:
    rows = [
        {
            "hypothesis_id": "P200_QUEUE_PASSIVE_QUEUE_POSITION_PROXY",
            "hypothesis_family": "passive_execution_microstructure",
            "material_difference": "Switch from marketable receive-flow/context signals to passive queue-position and adverse-selection survival labels.",
            "recommended_next_action": "precommit_passive_queue_position_label_contract_no_test",
            "priority": 1,
            "test_replay_allowed_next": 0,
        },
        {
            "hypothesis_id": "P200_QUEUE_EVENT_SHOCK_ABSORPTION",
            "hypothesis_family": "event_shock_resilience",
            "material_difference": "Model post-shock spread/depth recovery regimes rather than immediate receive-flow imbalance.",
            "recommended_next_action": "precommit_event_shock_absorption_feature_label_contract_no_test",
            "priority": 2,
            "test_replay_allowed_next": 0,
        },
        {
            "hypothesis_id": "P200_QUEUE_CROSS_SYMBOL_LEAD_LAG_CAUSAL",
            "hypothesis_family": "cross_symbol_lead_lag",
            "material_difference": "Use lagged cross-symbol causal ordering with target-symbol exclusion instead of contemporaneous cross-sectional context.",
            "recommended_next_action": "precommit_causal_lead_lag_feature_contract_no_test",
            "priority": 3,
            "test_replay_allowed_next": 0,
        },
    ]
    return pd.DataFrame(rows)


def build_gates(evidence: pd.DataFrame, decision: pd.DataFrame, contract: pd.DataFrame, queue: pd.DataFrame) -> pd.DataFrame:
    row = decision.iloc[0] if not decision.empty else {}
    return pd.DataFrame(
        [
            {"gate_id": "P199_DECISION_EVIDENCE_RECORDED", "gate_pass": int(len(evidence) == 5), "evidence": f"evidence_rows={len(evidence)}", "severity": "hard"},
            {"gate_id": "P199_PRIOR_SEARCHES_COMPLETE_OR_CLOSED", "gate_pass": int(as_int(row.get("no_survivor_or_closed_in_decision_phases", 0)) == 1), "evidence": f"no_survivor_or_closed={row.get('no_survivor_or_closed_in_decision_phases', '')}", "severity": "hard"},
            {"gate_id": "P199_TEST_REPLAY_CLOSED", "gate_pass": int(as_int(row.get("test_replay_allowed_next", 1)) == 0 and as_int(row.get("all_test_replay_gates_closed", 0)) == 1), "evidence": f"all_test_replay_gates_closed={row.get('all_test_replay_gates_closed', '')}", "severity": "hard"},
            {"gate_id": "P199_BRANCH_PAUSE_RECORDED", "gate_pass": int(as_int(row.get("current_branch_paused", 0)) == 1), "evidence": f"current_branch_paused={row.get('current_branch_paused', '')}", "severity": "hard"},
            {"gate_id": "P199_MATERIAL_REDESIGN_CONTRACT_RECORDED", "gate_pass": int(len(contract) >= 6 and contract["required_before_phase200_search"].astype(int).eq(1).all()), "evidence": f"contract_rows={len(contract)}", "severity": "hard"},
            {"gate_id": "P199_NEXT_HYPOTHESIS_QUEUE_RECORDED", "gate_pass": int(len(queue) >= 3 and queue["test_replay_allowed_next"].astype(int).eq(0).all()), "evidence": f"queue_rows={len(queue)}", "severity": "hard"},
            {"gate_id": "P199_PROMOTION_AND_PAPER_LIVE_CLOSED", "gate_pass": int(as_int(row.get("promotion_allowed", 1)) == 0 and as_int(row.get("paper_or_live_acceptance_allowed", 1)) == 0), "evidence": f"promotion_allowed={row.get('promotion_allowed', '')}; paper_live={row.get('paper_or_live_acceptance_allowed', '')}", "severity": "hard"},
        ]
    )


def build_acceptance(decision: pd.DataFrame, evidence: pd.DataFrame, contract: pd.DataFrame, queue: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates.loc[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(int).sum()) if not hard.empty else 0
    row = decision.iloc[0] if not decision.empty else {}
    return pd.DataFrame(
        [
            ("phase199_decision_rows", int(len(decision)), "Decision rows"),
            ("phase199_evidence_rows", int(len(evidence)), "Prior phase evidence rows"),
            ("phase199_material_redesign_contract_rows", int(len(contract)), "Material redesign contract rows"),
            ("phase199_next_hypothesis_queue_rows", int(len(queue)), "Next hypothesis queue rows"),
            ("phase199_decision", row.get("phase199_decision", ""), "Branch decision"),
            ("phase199_current_branch_paused", row.get("current_branch_paused", ""), "1 means current branch paused"),
            ("phase199_material_redesign_required", row.get("material_redesign_required", ""), "1 means materially new hypothesis required"),
            ("phase199_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase199_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase199_untouched_test_replay_precommit_allowed", 0, "No untouched test precommit opened"),
            ("phase199_promotion_allowed", 0, "No promotion opened"),
            ("phase199_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase199_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase199_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase199_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase199_branch_decision_complete", int(len(hard) > 0 and hard_pass == len(hard)), "1 means Phase199 completed"),
            ("phase199_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase199_next_best_action", "run_phase200_material_new_hypothesis_precommit_no_test", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase199 Branch Pause or Material Redesign Decision",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase199 converts the Phase198 `expand_or_pause` instruction into an explicit branch decision.",
        "The current receive-flow/context branch is paused for untouched-test purposes unless a materially different hypothesis is precommitted.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase199_branch_pause_or_material_redesign_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase199(
    phase194_dir: Path,
    phase195_dir: Path,
    phase196_dir: Path,
    phase197_dir: Path,
    phase198_dir: Path,
    output_dir: Path,
    base_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    inputs = {
        "phase194": read_csv(phase194_dir / "phase194_sparse_candidate_fragility_acceptance_summary.csv"),
        "phase195": read_csv(phase195_dir / "phase195_receive_flow_redesign_candidate_acceptance_summary.csv"),
        "phase196": read_csv(phase196_dir / "phase196_expanded_feature_model_acceptance_summary.csv"),
        "phase197": read_csv(phase197_dir / "phase197_non_receive_flow_feature_acceptance_summary.csv"),
        "phase198": read_csv(phase198_dir / "phase198_context_model_acceptance_summary.csv"),
    }
    evidence = build_evidence_ledger(inputs)
    decision = build_branch_decision(evidence)
    contract = build_material_redesign_contract()
    queue = build_next_hypothesis_queue()
    gates = build_gates(evidence, decision, contract, queue)
    acceptance = build_acceptance(decision, evidence, contract, queue, gates)

    evidence.to_csv(output_dir / "phase199_prior_phase_evidence_ledger.csv", index=False)
    decision.to_csv(output_dir / "phase199_branch_decision.csv", index=False)
    contract.to_csv(output_dir / "phase199_material_redesign_contract.csv", index=False)
    queue.to_csv(output_dir / "phase199_next_hypothesis_queue.csv", index=False)
    gates.to_csv(output_dir / "phase199_branch_decision_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase199_branch_decision_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Branch Decision": decision,
            "Prior Phase Evidence": evidence,
            "Material Redesign Contract": contract,
            "Next Hypothesis Queue": queue,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase199_branch_pause_or_material_redesign_decision_no_test",
        **reproducibility_fields(
            artifact_id="phase199_branch_pause_or_material_redesign_decision",
            generated_utc=generated,
            inputs={
                "phase194_acceptance": str(phase194_dir / "phase194_sparse_candidate_fragility_acceptance_summary.csv"),
                "phase195_acceptance": str(phase195_dir / "phase195_receive_flow_redesign_candidate_acceptance_summary.csv"),
                "phase196_acceptance": str(phase196_dir / "phase196_expanded_feature_model_acceptance_summary.csv"),
                "phase197_acceptance": str(phase197_dir / "phase197_non_receive_flow_feature_acceptance_summary.csv"),
                "phase198_acceptance": str(phase198_dir / "phase198_context_model_acceptance_summary.csv"),
            },
            parameters={
                "decision_scope": "pause_current_receive_flow_context_branch_or_require_material_redesign",
                "strategy_replay_allowed": "0",
                "test_replay_allowed_next": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "evidence": str(output_dir / "phase199_prior_phase_evidence_ledger.csv"),
                "decision": str(output_dir / "phase199_branch_decision.csv"),
                "contract": str(output_dir / "phase199_material_redesign_contract.csv"),
                "queue": str(output_dir / "phase199_next_hypothesis_queue.csv"),
                "gates": str(output_dir / "phase199_branch_decision_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase199_branch_decision_acceptance_summary.csv"),
                "report": str(output_dir / "phase199_branch_pause_or_material_redesign_report.md"),
            },
            scenario_ids="phase199_branch_pause_or_material_redesign_decision_no_test",
            cost_model_version="not_applicable_no_strategy_replay",
            latency_model_version="not_applicable_no_strategy_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase199_branch_decision_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase194-dir", type=Path, default=DEFAULT_PHASE194_DIR)
    parser.add_argument("--phase195-dir", type=Path, default=DEFAULT_PHASE195_DIR)
    parser.add_argument("--phase196-dir", type=Path, default=DEFAULT_PHASE196_DIR)
    parser.add_argument("--phase197-dir", type=Path, default=DEFAULT_PHASE197_DIR)
    parser.add_argument("--phase198-dir", type=Path, default=DEFAULT_PHASE198_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase199(args.phase194_dir, args.phase195_dir, args.phase196_dir, args.phase197_dir, args.phase198_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
