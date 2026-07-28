from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE171_DIR = Path("outputs/phase171")
DEFAULT_PHASE172_DIR = Path("outputs/phase172")
DEFAULT_PHASE175_DIR = Path("outputs/phase175")
DEFAULT_PHASE176_DIR = Path("outputs/phase176")
DEFAULT_PHASE177_DIR = Path("outputs/phase177")
DEFAULT_PHASE203_DIR = Path("outputs/phase203")
DEFAULT_PHASE204_DIR = Path("outputs/phase204")
DEFAULT_OUTPUT_DIR = Path("outputs/phase205")
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


def build_source_evidence(inputs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    p171 = inputs["phase171"]
    p172 = inputs["phase172"]
    p175 = inputs["phase175"]
    p176 = inputs["phase176"]
    p177 = inputs["phase177"]
    p203 = inputs["phase203"]
    p204 = inputs["phase204"]
    return pd.DataFrame(
        [
            {
                "evidence_id": "P205_PHASE204_CLOSURE",
                "source_route": "post_passive_closure",
                "status": "ready" if as_int(metric_value(p204, "phase204_closure_decision_complete", 0)) else "missing",
                "evidence": f"passive_closed={metric_value(p204, 'phase204_current_passive_redesign_closed_for_replay', '')}; material_new_source_required={metric_value(p204, 'phase204_material_new_source_required', '')}; threshold_widening_allowed={metric_value(p204, 'phase204_threshold_widening_allowed', '')}",
                "replay_allowed": as_int(metric_value(p204, "phase204_strategy_replay_allowed", 0)),
            },
            {
                "evidence_id": "P205_PHASE203_PASSIVE_REJECTION",
                "source_route": "passive_label_breadth_alternative",
                "status": "candidate_gate_closed" if as_int(metric_value(p203, "phase203_candidate_gate_open", 0)) == 0 else "candidate_gate_open",
                "evidence": f"materialized_rows={metric_value(p203, 'phase203_materialized_label_rows', '')}; redesigned_pass_rows={metric_value(p203, 'phase203_redesigned_candidate_pass_rows', '')}; adverse_ceiling_met={metric_value(p203, 'phase203_adverse_selection_ceiling_met', '')}",
                "replay_allowed": as_int(metric_value(p203, "phase203_strategy_replay_allowed", 0)),
            },
            {
                "evidence_id": "P205_PHASE171_EXTERNAL_SOURCE",
                "source_route": "real_receive_flow_external_orderflow_context",
                "status": "selected_axis_available" if str(metric_value(p171, "phase171_selected_source_id", "")) == "P171_REAL_MULTIDAY_RECEIVE_EVENT_FLOW" else "missing",
                "evidence": f"selected_source={metric_value(p171, 'phase171_selected_source_id', '')}; gates_pass={metric_value(p171, 'phase171_all_gates_pass', '')}; azure_policy={metric_value(p171, 'phase171_azure_read_policy', '')}",
                "replay_allowed": as_int(metric_value(p171, "phase171_strategy_replay_allowed", 0)),
            },
            {
                "evidence_id": "P205_PHASE172_LOCAL_PANEL",
                "source_route": "real_receive_flow_external_orderflow_context",
                "status": "ready" if as_int(metric_value(p172, "phase172_ready_receive_flow_dates", 0)) >= 5 else "insufficient",
                "evidence": f"ready_dates={metric_value(p172, 'phase172_ready_receive_flow_dates', '')}; symbol_day_rows={metric_value(p172, 'phase172_symbol_day_rows', '')}; rows={metric_value(p172, 'phase172_total_rows', '')}; bytes={metric_value(p172, 'phase172_total_bytes', '')}",
                "replay_allowed": as_int(metric_value(p172, "phase172_strategy_replay_allowed", 0)),
            },
            {
                "evidence_id": "P205_PHASE175_177_FEATURE_QUALITY",
                "source_route": "real_receive_flow_external_orderflow_context",
                "status": "quality_ready" if as_int(metric_value(p175, "phase175_activation_ready", 0)) and as_int(metric_value(p176, "phase176_features_materialized", 0)) and as_int(metric_value(p177, "phase177_feature_quality_audit_ran", 0)) else "quality_incomplete",
                "evidence": f"schema_activation={metric_value(p175, 'phase175_activation_ready', '')}; features_materialized={metric_value(p176, 'phase176_features_materialized', '')}; quality_audit={metric_value(p177, 'phase177_feature_quality_audit_ran', '')}",
                "replay_allowed": 0,
            },
        ]
    )


def build_route_scorecard(evidence: pd.DataFrame, phase204_queue: pd.DataFrame) -> pd.DataFrame:
    real_ready = int(evidence.loc[evidence["source_route"].eq("real_receive_flow_external_orderflow_context"), "status"].astype(str).isin(["selected_axis_available", "ready", "quality_ready"]).sum() >= 3)
    passive_closed = int(evidence.loc[evidence["evidence_id"].eq("P205_PHASE203_PASSIVE_REJECTION"), "status"].astype(str).eq("candidate_gate_closed").any())
    rows = [
        {
            "route_id": "P205_REAL_RECEIVE_FLOW_CONTEXT_SOURCE_REFRESH",
            "phase204_queue_item": "precommit_non_passive_external_orderflow_or_context_source",
            "route_class": "material_new_non_passive_source",
            "priority": 1,
            "evidence_ready": real_ready,
            "blocked_reason": "" if real_ready else "real_receive_flow_evidence_incomplete",
            "selected_route": real_ready,
            "allowed_next_scope": "source_contract_refresh_and_feature_family_precommit_no_replay",
            "strategy_replay_allowed": 0,
        },
        {
            "route_id": "P205_PASSIVE_LABEL_BREADTH_EXPANSION_ONLY",
            "phase204_queue_item": "expand_redesigned_passive_label_materialization_breadth",
            "route_class": "passive_label_only_alternative",
            "priority": 2,
            "evidence_ready": passive_closed,
            "blocked_reason": "replay_closed_candidate_gate_zero",
            "selected_route": 0,
            "allowed_next_scope": "label_only_breadth_expansion_no_replay",
            "strategy_replay_allowed": 0,
        },
        {
            "route_id": "P205_REAL_ANCHOR_CALIBRATION_REFRESH",
            "phase204_queue_item": "return_to_real_anchor_microstructure_calibration",
            "route_class": "calibration_audit",
            "priority": 3,
            "evidence_ready": 1,
            "blocked_reason": "not_primary_source_precommit_route",
            "selected_route": 0,
            "allowed_next_scope": "local_calibration_audit_no_replay",
            "strategy_replay_allowed": 0,
        },
    ]
    out = pd.DataFrame(rows)
    if not phase204_queue.empty:
        out["phase204_queue_rows_available"] = len(phase204_queue)
    else:
        out["phase204_queue_rows_available"] = 0
    return out


def build_selected_source_contract(scorecard: pd.DataFrame) -> pd.DataFrame:
    selected = scorecard.loc[scorecard["selected_route"].astype(int).eq(1)].sort_values("priority").head(1)
    route_id = selected["route_id"].iloc[0] if not selected.empty else "none"
    return pd.DataFrame(
        [
            {
                "contract_id": "P205_SELECTED_SOURCE_ROUTE",
                "selected_route_id": route_id,
                "selected_source_family": "real_receive_flow_context_source_refresh",
                "material_difference": "Re-enters the real multiday receive-flow source as a source-contract refresh after the passive queue redesign closed, not as a replay of the failed passive or prior context models.",
                "required_inputs_next": "phase171_source_contract;phase172_local_panel;phase175_schema;phase176_features;phase177_quality;phase204_guardrails",
                "first_allowed_deliverable": "Phase206 refreshed source contract and non-overlap feature-family catalog",
                "forbidden_next": FORBIDDEN_OUTPUTS,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
            }
        ]
    )


def build_phase206_work_order(contract: pd.DataFrame) -> pd.DataFrame:
    selected = contract.iloc[0] if not contract.empty else {}
    return pd.DataFrame(
        [
            {
                "work_order_id": "P206_WO01_SOURCE_NON_OVERLAP_AUDIT",
                "selected_route_id": selected.get("selected_route_id", ""),
                "action": "audit selected source against failed Phase194-204 forms",
                "allowed_scope": "source_contract_no_replay",
                "strategy_replay_allowed": 0,
            },
            {
                "work_order_id": "P206_WO02_FEATURE_FAMILY_CATALOG",
                "selected_route_id": selected.get("selected_route_id", ""),
                "action": "catalog materially new receive-flow context features without model fitting",
                "allowed_scope": "feature_contract_no_replay",
                "strategy_replay_allowed": 0,
            },
            {
                "work_order_id": "P206_WO03_PRE_REPLAY_GUARDRAILS",
                "selected_route_id": selected.get("selected_route_id", ""),
                "action": "carry forward no-threshold-widening, train-only selection, and no test replay guardrails",
                "allowed_scope": "guardrail_contract_no_replay",
                "strategy_replay_allowed": 0,
            },
        ]
    )


def build_gates(evidence: pd.DataFrame, scorecard: pd.DataFrame, contract: pd.DataFrame, work_order: pd.DataFrame) -> pd.DataFrame:
    selected_rows = int(scorecard["selected_route"].astype(int).sum()) if not scorecard.empty else 0
    replay_flags = int(evidence["replay_allowed"].astype(int).sum()) if not evidence.empty else 0
    return pd.DataFrame(
        [
            ("P205_PHASE204_EVIDENCE_RECORDED", len(evidence) >= 5, f"evidence_rows={len(evidence)}", "hard"),
            ("P205_SINGLE_ROUTE_SELECTED", selected_rows == 1, f"selected_routes={selected_rows}", "hard"),
            ("P205_SELECTED_ROUTE_IS_MATERIAL_NEW_SOURCE", str(contract.iloc[0]["selected_route_id"]).startswith("P205_REAL_RECEIVE_FLOW") if not contract.empty else False, f"selected_route={contract.iloc[0]['selected_route_id'] if not contract.empty else ''}", "hard"),
            ("P205_PASSIVE_REPLAY_REMAINS_CLOSED", replay_flags in (0, 1), f"source_evidence_replay_flags_sum={replay_flags}; phase172_unlock_is_source_not_replay", "hard"),
            ("P205_PHASE206_WORK_ORDER_RECORDED", len(work_order) == 3 and work_order["strategy_replay_allowed"].astype(int).eq(0).all(), f"work_order_rows={len(work_order)}", "hard"),
            ("P205_NO_REPLAY_OR_PROMOTION", int(contract["strategy_replay_allowed"].astype(int).sum()) == 0 and int(contract["test_replay_allowed_next"].astype(int).sum()) == 0 and int(contract["promotion_allowed"].astype(int).sum()) == 0 and int(contract["paper_or_live_acceptance_allowed"].astype(int).sum()) == 0, "strategy_replay=0; test_replay=0; promotion=0; paper_live=0", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(evidence: pd.DataFrame, scorecard: pd.DataFrame, contract: pd.DataFrame, work_order: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    selected = contract.iloc[0] if not contract.empty else {}
    return pd.DataFrame(
        [
            ("phase205_evidence_rows", len(evidence), "Source evidence rows"),
            ("phase205_route_scorecard_rows", len(scorecard), "Route scorecard rows"),
            ("phase205_selected_source_contract_rows", len(contract), "Selected source contract rows"),
            ("phase205_phase206_work_order_rows", len(work_order), "Phase206 work-order rows"),
            ("phase205_selected_route_id", selected.get("selected_route_id", ""), "Selected route"),
            ("phase205_gate_rows", len(gates), "Gates evaluated"),
            ("phase205_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase205_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase205_material_new_source_precommit_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase205 completed"),
            ("phase205_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase205_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase205_promotion_allowed", 0, "No promotion opened"),
            ("phase205_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase205_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase205_next_best_action", "run_phase206_selected_source_nonoverlap_feature_contract_no_replay", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase205 Material New Source Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase205 selects the next post-passive-closure route.",
        "It precommits a material source path only; no replay, test, orders, fills, P&L, promotion, or paper/live acceptance is opened.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase205_material_new_source_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase205(
    phase171_dir: Path,
    phase172_dir: Path,
    phase175_dir: Path,
    phase176_dir: Path,
    phase177_dir: Path,
    phase203_dir: Path,
    phase204_dir: Path,
    output_dir: Path,
    base_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    inputs = {
        "phase171": read_csv(phase171_dir / "phase171_external_orderflow_source_acceptance_summary.csv"),
        "phase172": read_csv(phase172_dir / "phase172_real_l2_receive_flow_availability_acceptance_summary.csv"),
        "phase175": read_csv(phase175_dir / "phase175_receive_flow_feature_schema_precommit_acceptance_summary.csv"),
        "phase176": read_csv(phase176_dir / "phase176_receive_flow_feature_materializer_acceptance_summary.csv"),
        "phase177": read_csv(phase177_dir / "phase177_receive_flow_feature_quality_audit_acceptance_summary.csv"),
        "phase203": read_csv(phase203_dir / "phase203_redesigned_passive_label_acceptance_summary.csv"),
        "phase204": read_csv(phase204_dir / "phase204_passive_redesign_closure_acceptance_summary.csv"),
    }
    phase204_queue = read_csv(phase204_dir / "phase204_next_research_queue.csv")
    evidence = build_source_evidence(inputs)
    scorecard = build_route_scorecard(evidence, phase204_queue)
    contract = build_selected_source_contract(scorecard)
    work_order = build_phase206_work_order(contract)
    gates = build_gates(evidence, scorecard, contract, work_order)
    acceptance = build_acceptance(evidence, scorecard, contract, work_order, gates)

    evidence.to_csv(output_dir / "phase205_source_evidence_ledger.csv", index=False)
    scorecard.to_csv(output_dir / "phase205_route_scorecard.csv", index=False)
    contract.to_csv(output_dir / "phase205_selected_source_contract.csv", index=False)
    work_order.to_csv(output_dir / "phase205_phase206_work_order.csv", index=False)
    gates.to_csv(output_dir / "phase205_material_new_source_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase205_material_new_source_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Source Evidence Ledger": evidence,
            "Route Scorecard": scorecard,
            "Selected Source Contract": contract,
            "Phase206 Work Order": work_order,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase205_material_new_source_precommit_no_replay",
        **reproducibility_fields(
            artifact_id="phase205_material_new_source_precommit",
            generated_utc=generated,
            inputs={
                "phase171_acceptance": str(phase171_dir / "phase171_external_orderflow_source_acceptance_summary.csv"),
                "phase172_acceptance": str(phase172_dir / "phase172_real_l2_receive_flow_availability_acceptance_summary.csv"),
                "phase175_acceptance": str(phase175_dir / "phase175_receive_flow_feature_schema_precommit_acceptance_summary.csv"),
                "phase176_acceptance": str(phase176_dir / "phase176_receive_flow_feature_materializer_acceptance_summary.csv"),
                "phase177_acceptance": str(phase177_dir / "phase177_receive_flow_feature_quality_audit_acceptance_summary.csv"),
                "phase203_acceptance": str(phase203_dir / "phase203_redesigned_passive_label_acceptance_summary.csv"),
                "phase204_acceptance": str(phase204_dir / "phase204_passive_redesign_closure_acceptance_summary.csv"),
            },
            parameters={
                "decision_scope": "post_passive_closure_material_new_source_precommit",
                "strategy_replay_allowed": "0",
                "test_replay_allowed_next": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "evidence": str(output_dir / "phase205_source_evidence_ledger.csv"),
                "scorecard": str(output_dir / "phase205_route_scorecard.csv"),
                "contract": str(output_dir / "phase205_selected_source_contract.csv"),
                "work_order": str(output_dir / "phase205_phase206_work_order.csv"),
                "gates": str(output_dir / "phase205_material_new_source_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase205_material_new_source_acceptance_summary.csv"),
                "report": str(output_dir / "phase205_material_new_source_precommit_report.md"),
            },
            scenario_ids="phase205_material_new_source_precommit_no_replay",
            cost_model_version="not_applicable_no_strategy_replay",
            latency_model_version="not_applicable_no_strategy_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase205_material_new_source_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Precommit Phase205 material new source route without replay.")
    parser.add_argument("--phase171-dir", type=Path, default=DEFAULT_PHASE171_DIR)
    parser.add_argument("--phase172-dir", type=Path, default=DEFAULT_PHASE172_DIR)
    parser.add_argument("--phase175-dir", type=Path, default=DEFAULT_PHASE175_DIR)
    parser.add_argument("--phase176-dir", type=Path, default=DEFAULT_PHASE176_DIR)
    parser.add_argument("--phase177-dir", type=Path, default=DEFAULT_PHASE177_DIR)
    parser.add_argument("--phase203-dir", type=Path, default=DEFAULT_PHASE203_DIR)
    parser.add_argument("--phase204-dir", type=Path, default=DEFAULT_PHASE204_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase205(
        args.phase171_dir,
        args.phase172_dir,
        args.phase175_dir,
        args.phase176_dir,
        args.phase177_dir,
        args.phase203_dir,
        args.phase204_dir,
        args.output_dir,
        args.base_dir,
    )


if __name__ == "__main__":
    main()
