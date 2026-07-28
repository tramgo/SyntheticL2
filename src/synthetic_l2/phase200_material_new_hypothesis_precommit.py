from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE118_DIR = Path("outputs/phase118")
DEFAULT_PHASE120_DIR = Path("outputs/phase120")
DEFAULT_PHASE199_DIR = Path("outputs/phase199")
DEFAULT_OUTPUT_DIR = Path("outputs/phase200")
FORBIDDEN_OUTPUTS = "strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim"


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


def select_priority_hypothesis(queue: pd.DataFrame) -> pd.DataFrame:
    if queue.empty:
        return pd.DataFrame()
    selected = queue.sort_values("priority").head(1).copy()
    selected["phase200_selected_for_precommit"] = 1
    selected["phase200_precommit_scope"] = "label_contract_only_no_strategy_replay"
    selected["strategy_replay_allowed"] = 0
    selected["test_replay_allowed_next"] = 0
    selected["promotion_allowed"] = 0
    selected["paper_or_live_acceptance_allowed"] = 0
    return selected


def build_label_contract(selected: pd.DataFrame, feature_contract: pd.DataFrame) -> pd.DataFrame:
    selected_id = str(selected["hypothesis_id"].iloc[0]) if not selected.empty else "P200_QUEUE_PASSIVE_QUEUE_POSITION_PROXY"
    rows = [
        {
            "contract_id": "P200_PASSIVE_SURVIVAL_LABEL",
            "hypothesis_id": selected_id,
            "label_name": "passive_queue_survival_without_adverse_markout",
            "definition": "A hypothetical maker order is acceptable only if inferred touch/fill survival is followed by adverse-selection below the Phase200 ceiling and no spread-widening penalty breach.",
            "source_evidence": "phase66_adverse_selection;phase68_replenishment;phase69_spread_transition;phase118_feature_contract",
            "required_before_search": 1,
        },
        {
            "contract_id": "P200_QUEUE_RECOVERY_FEATURES",
            "hypothesis_id": selected_id,
            "label_name": "queue_recovery_feature_set",
            "definition": "Use pre-touch imbalance, replenishment bucket, spread transition bucket, event intensity, time-of-day and symbol-liquidity tier; forbid future returns or post-entry unavailable features.",
            "source_evidence": "outputs/phase118/richer_passive_feature_contract.csv",
            "required_before_search": 1,
        },
        {
            "contract_id": "P200_LABEL_ONLY_EXPANSION_FIRST",
            "hypothesis_id": selected_id,
            "label_name": "stage01_label_coverage_expansion",
            "definition": "Run Phase120 Stage 01 label-only expansion before any candidate replay, then rebuild richer passive joined labels.",
            "source_evidence": "outputs/phase120/passive_label_expansion_stage_plan.csv",
            "required_before_search": 1,
        },
        {
            "contract_id": "P200_BREADTH_REQUIREMENT",
            "hypothesis_id": selected_id,
            "label_name": "minimum_breadth_gate",
            "definition": "Require multi-month and multi-symbol label stability before any bounded pilot replay; one-month pockets are not enough.",
            "source_evidence": "phase119_max_candidate_trade_dates;phase120_current_label_months",
            "required_before_search": 1,
        },
        {
            "contract_id": "P200_COST_TOXICITY_BOUND",
            "hypothesis_id": selected_id,
            "label_name": "cost_toxicity_bound",
            "definition": "Reject candidate buckets whose passive adverse-selection rate or cost-clearing rate remains toxic after label expansion.",
            "source_evidence": "phase66_best_cost_clearing_rate;phase123_cost_toxicity_label",
            "required_before_search": 1,
        },
        {
            "contract_id": "P200_NO_TEST_OR_REPLAY",
            "hypothesis_id": selected_id,
            "label_name": "no_test_no_replay_guard",
            "definition": "Phase200 cannot run strategy replay, test replay, order arrival, fill model, P&L replay, promotion or paper/live acceptance.",
            "source_evidence": "phase199_material_redesign_contract",
            "required_before_search": 1,
        },
    ]
    out = pd.DataFrame(rows)
    out["feature_contract_rows_available"] = int(len(feature_contract))
    out["strategy_replay_allowed"] = 0
    out["test_replay_allowed_next"] = 0
    return out


def build_stage_action_plan(stage_plan: pd.DataFrame) -> pd.DataFrame:
    if stage_plan.empty:
        return pd.DataFrame(
            [
                {
                    "action_id": "P200_STAGE01_LABEL_EXPANSION_MISSING",
                    "priority": 1,
                    "action": "Phase120 stage plan is missing; rebuild label expansion plan before Phase201.",
                    "command": "",
                    "required_next": 1,
                    "strategy_replay_allowed": 0,
                }
            ]
        )
    stage1 = stage_plan.sort_values("limit_shards").head(1).copy()
    rows: list[dict[str, Any]] = []
    for col, action_name in [
        ("phase66_command", "run_passive_adverse_selection_labels"),
        ("phase68_command", "run_replenishment_after_touch_labels"),
        ("phase69_command", "run_spread_transition_labels"),
        ("phase119_command_after_labels", "rerun_richer_passive_joined_labels"),
    ]:
        rows.append(
            {
                "action_id": f"P200_{action_name.upper()}",
                "stage_id": stage1["stage_id"].iloc[0],
                "priority": len(rows) + 1,
                "action": action_name,
                "command": stage1[col].iloc[0],
                "required_next": 1,
                "strategy_replay_allowed": 0,
            }
        )
    return pd.DataFrame(rows)


def build_prior_evidence_summary(
    phase120_acceptance: pd.DataFrame,
    feature_contract: pd.DataFrame,
    stage_plan: pd.DataFrame,
    coverage: pd.DataFrame,
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "evidence_id": "P200_PHASE120_LABEL_EXPANSION_ALLOWED",
                "observed": metric_value(phase120_acceptance, "phase120_label_expansion_allowed", ""),
                "interpretation": "Label-only expansion is allowed without replay.",
            },
            {
                "evidence_id": "P200_PHASE120_REPLAY_CLOSED",
                "observed": metric_value(phase120_acceptance, "phase120_replay_allowed", ""),
                "interpretation": "Passive replay remains closed.",
            },
            {
                "evidence_id": "P200_FEATURE_CONTRACT_AVAILABLE",
                "observed": len(feature_contract),
                "interpretation": "Phase118 passive feature contracts available.",
            },
            {
                "evidence_id": "P200_STAGE_PLAN_AVAILABLE",
                "observed": len(stage_plan),
                "interpretation": "Phase120 staged label expansion commands available.",
            },
            {
                "evidence_id": "P200_CURRENT_COVERAGE_ROWS",
                "observed": len(coverage),
                "interpretation": "Current passive label coverage rows available for stage planning.",
            },
        ]
    )


def build_gates(
    phase199: pd.DataFrame,
    selected: pd.DataFrame,
    label_contract: pd.DataFrame,
    actions: pd.DataFrame,
    phase120_acceptance: pd.DataFrame,
) -> pd.DataFrame:
    phase199_complete = as_int(metric_value(phase199, "phase199_branch_decision_complete", 0))
    material_required = as_int(metric_value(phase199, "phase199_material_redesign_required", 0))
    label_expansion_allowed = as_int(metric_value(phase120_acceptance, "phase120_label_expansion_allowed", 0))
    replay_allowed = as_int(metric_value(phase120_acceptance, "phase120_replay_allowed", 0))
    selected_ok = int(not selected.empty and str(selected["hypothesis_id"].iloc[0]) == "P200_QUEUE_PASSIVE_QUEUE_POSITION_PROXY")
    return pd.DataFrame(
        [
            {"gate_id": "P200_PHASE199_BRANCH_DECISION_COMPLETE", "gate_pass": int(phase199_complete == 1 and material_required == 1), "evidence": f"phase199_complete={phase199_complete}; material_required={material_required}", "severity": "hard"},
            {"gate_id": "P200_PRIORITY_HYPOTHESIS_SELECTED", "gate_pass": selected_ok, "evidence": f"selected_rows={len(selected)}", "severity": "hard"},
            {"gate_id": "P200_MATERIAL_DIFFERENCE_RECORDED", "gate_pass": int(not selected.empty and selected["material_difference"].astype(str).ne("").all()), "evidence": "passive queue-position differs from receive-flow/context marketable search", "severity": "hard"},
            {"gate_id": "P200_LABEL_CONTRACT_RECORDED", "gate_pass": int(len(label_contract) >= 6 and label_contract["required_before_search"].astype(int).eq(1).all()), "evidence": f"contract_rows={len(label_contract)}", "severity": "hard"},
            {"gate_id": "P200_LABEL_ONLY_EXPANSION_ACTIONS_RECORDED", "gate_pass": int(len(actions) >= 4 and actions["strategy_replay_allowed"].astype(int).eq(0).all()), "evidence": f"action_rows={len(actions)}", "severity": "hard"},
            {"gate_id": "P200_PHASE120_LABEL_EXPANSION_ALLOWED_REPLAY_CLOSED", "gate_pass": int(label_expansion_allowed == 1 and replay_allowed == 0), "evidence": f"label_expansion_allowed={label_expansion_allowed}; replay_allowed={replay_allowed}", "severity": "hard"},
            {"gate_id": "P200_NO_TEST_REPLAY_OR_PROMOTION", "gate_pass": 1, "evidence": "test_replay=0; strategy_replay=0; promotion=0; paper_live=0", "severity": "hard"},
        ]
    )


def build_acceptance(selected: pd.DataFrame, label_contract: pd.DataFrame, actions: pd.DataFrame, evidence: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates.loc[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(int).sum()) if not hard.empty else 0
    selected_id = selected["hypothesis_id"].iloc[0] if not selected.empty else ""
    return pd.DataFrame(
        [
            ("phase200_selected_hypothesis_id", selected_id, "Selected material new hypothesis"),
            ("phase200_selected_hypothesis_rows", int(len(selected)), "Selected hypothesis rows"),
            ("phase200_label_contract_rows", int(len(label_contract)), "Passive queue label contract rows"),
            ("phase200_stage_action_rows", int(len(actions)), "Next stage action rows"),
            ("phase200_prior_evidence_rows", int(len(evidence)), "Prior evidence rows"),
            ("phase200_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase200_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase200_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase200_material_new_hypothesis_precommit_complete", int(len(hard) > 0 and hard_pass == len(hard)), "1 means Phase200 completed"),
            ("phase200_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase200_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase200_promotion_allowed", 0, "No promotion opened"),
            ("phase200_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase200_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase200_next_best_action", "run_phase201_passive_queue_label_only_stage01_expansion_no_replay", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase200 Material New Hypothesis Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase200 selects the highest-priority materially new hypothesis from Phase199: passive queue-position/adverse-selection survival.",
        "It is a label-contract and label-expansion precommit only; no strategy replay, test replay, orders, fills, P&L, promotion or paper/live acceptance is opened.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase200_material_new_hypothesis_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase200(phase118_dir: Path, phase120_dir: Path, phase199_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase199 = read_csv(phase199_dir / "phase199_branch_decision_acceptance_summary.csv")
    queue = read_csv(phase199_dir / "phase199_next_hypothesis_queue.csv")
    feature_contract = read_csv(phase118_dir / "richer_passive_feature_contract.csv")
    phase120_acceptance = read_csv(phase120_dir / "phase120_passive_label_coverage_acceptance_summary.csv")
    stage_plan = read_csv(phase120_dir / "passive_label_expansion_stage_plan.csv")
    coverage = read_csv(phase120_dir / "current_passive_label_coverage.csv")

    selected = select_priority_hypothesis(queue)
    label_contract = build_label_contract(selected, feature_contract)
    actions = build_stage_action_plan(stage_plan)
    evidence = build_prior_evidence_summary(phase120_acceptance, feature_contract, stage_plan, coverage)
    gates = build_gates(phase199, selected, label_contract, actions, phase120_acceptance)
    acceptance = build_acceptance(selected, label_contract, actions, evidence, gates)

    selected.to_csv(output_dir / "phase200_selected_material_hypothesis.csv", index=False)
    label_contract.to_csv(output_dir / "phase200_passive_queue_label_contract.csv", index=False)
    actions.to_csv(output_dir / "phase200_label_only_stage_action_plan.csv", index=False)
    evidence.to_csv(output_dir / "phase200_prior_passive_evidence_summary.csv", index=False)
    gates.to_csv(output_dir / "phase200_material_new_hypothesis_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase200_material_new_hypothesis_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Selected Hypothesis": selected,
            "Passive Queue Label Contract": label_contract,
            "Label-only Stage Action Plan": actions,
            "Prior Passive Evidence": evidence,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase200_material_new_hypothesis_precommit_no_test",
        **reproducibility_fields(
            artifact_id="phase200_material_new_hypothesis_precommit",
            generated_utc=generated,
            inputs={
                "phase199_acceptance": str(phase199_dir / "phase199_branch_decision_acceptance_summary.csv"),
                "phase199_queue": str(phase199_dir / "phase199_next_hypothesis_queue.csv"),
                "phase118_feature_contract": str(phase118_dir / "richer_passive_feature_contract.csv"),
                "phase120_acceptance": str(phase120_dir / "phase120_passive_label_coverage_acceptance_summary.csv"),
                "phase120_stage_plan": str(phase120_dir / "passive_label_expansion_stage_plan.csv"),
            },
            parameters={
                "selected_hypothesis": "P200_QUEUE_PASSIVE_QUEUE_POSITION_PROXY",
                "precommit_scope": "passive_queue_label_contract_and_stage01_label_expansion_plan",
                "strategy_replay_allowed": "0",
                "test_replay_allowed_next": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "selected": str(output_dir / "phase200_selected_material_hypothesis.csv"),
                "label_contract": str(output_dir / "phase200_passive_queue_label_contract.csv"),
                "actions": str(output_dir / "phase200_label_only_stage_action_plan.csv"),
                "evidence": str(output_dir / "phase200_prior_passive_evidence_summary.csv"),
                "gates": str(output_dir / "phase200_material_new_hypothesis_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase200_material_new_hypothesis_acceptance_summary.csv"),
                "report": str(output_dir / "phase200_material_new_hypothesis_precommit_report.md"),
            },
            scenario_ids="phase200_material_new_hypothesis_precommit_no_test",
            cost_model_version="phase66_phase120_passive_cost_toxicity_labels",
            latency_model_version="not_applicable_no_strategy_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase200_material_new_hypothesis_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase118-dir", type=Path, default=DEFAULT_PHASE118_DIR)
    parser.add_argument("--phase120-dir", type=Path, default=DEFAULT_PHASE120_DIR)
    parser.add_argument("--phase199-dir", type=Path, default=DEFAULT_PHASE199_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase200(args.phase118_dir, args.phase120_dir, args.phase199_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
