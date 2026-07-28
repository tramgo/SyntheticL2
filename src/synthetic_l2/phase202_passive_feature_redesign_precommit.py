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
DEFAULT_PHASE201_DIR = Path("outputs/phase201")
DEFAULT_OUTPUT_DIR = Path("outputs/phase202")
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


def build_failure_decomposition(phase201: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "failure_id": "P202_ADVERSE_SELECTION_GATE_FAILED",
                "observed": metric_value(phase201, "phase201_dominant_failure_reason", ""),
                "phase201_pre_replay_candidate_rows": as_int(metric_value(phase201, "phase201_pre_replay_candidate_rows", 0)),
                "phase201_joined_label_candidate_rows": as_int(metric_value(phase201, "phase201_joined_label_candidate_rows", 0)),
                "redesign_response": "Add queue recovery persistence, adverse markout ceiling, and toxicity abstention filters before candidate construction.",
                "must_address_before_replay": 1,
            },
            {
                "failure_id": "P202_BREADTH_GATE_FAILED",
                "observed": metric_value(phase201, "phase201_dominant_failure_reason", ""),
                "phase201_max_candidate_symbols": as_int(metric_value(phase201, "phase201_max_candidate_symbols", 0)),
                "phase201_max_candidate_trade_dates": as_int(metric_value(phase201, "phase201_max_candidate_trade_dates", 0)),
                "redesign_response": "Require symbol/month stability at the feature-family level instead of single pocket survival.",
                "must_address_before_replay": 1,
            },
        ]
    )


def build_redesigned_feature_contract(base_contract: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {
            "redesign_feature_id": "P202_QUEUE_RECOVERY_PERSISTENCE",
            "source_family": "P118_QUEUE_RECOVERY_AFTER_ADVERSE_TOUCH",
            "hypothesis": "Passive fills are safer only when replenishment persists after a touch and the spread does not re-expand.",
            "required_inputs": "replenishment_bucket;spread_transition_bucket;depth_rebuild_rate;time_of_day_bucket;symbol_liquidity_tier",
            "failure_target": "adverse_selection_gate_failed",
            "label_only_materialization_required": 1,
        },
        {
            "redesign_feature_id": "P202_TOXICITY_ABSTENTION_FILTER",
            "source_family": "P118_REPLENISHMENT_STABILITY_FILTER",
            "hypothesis": "Abstain in buckets where historical passive adverse-selection rate or cost-clearing failure remains high.",
            "required_inputs": "adverse_selection_bucket;cost_clearing_rate_bucket;feed_imperfection_rate;spread_percentile",
            "failure_target": "adverse_selection_gate_failed",
            "label_only_materialization_required": 1,
        },
        {
            "redesign_feature_id": "P202_SYMBOL_MONTH_STABILITY_SCORE",
            "source_family": "P118_REPLENISHMENT_STABILITY_FILTER",
            "hypothesis": "Candidate families must be stable across symbols and months before any replay, avoiding one-symbol pockets.",
            "required_inputs": "symbol_liquidity_tier;trade_month;candidate_family_id;label_quality_score",
            "failure_target": "breadth_gate_failed",
            "label_only_materialization_required": 1,
        },
        {
            "redesign_feature_id": "P202_SPREAD_COMPRESSION_WITH_CANCEL_GUARD",
            "source_family": "P118_SPREAD_COMPRESSION_MAKER_ONLY",
            "hypothesis": "Maker spread capture is only eligible when spread compression is paired with stale-quote cancellation and non-toxic markout.",
            "required_inputs": "spread_transition_state;recent_spread_percentile;stale_quote_flag;adverse_markout_bucket",
            "failure_target": "adverse_selection_gate_failed",
            "label_only_materialization_required": 1,
        },
    ]
    out = pd.DataFrame(rows)
    out["base_contract_rows_available"] = int(len(base_contract))
    out["strategy_replay_allowed"] = 0
    out["test_replay_allowed_next"] = 0
    return out


def build_acceptance_contract(redesign: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {
            "contract_id": "P202_MIN_BREADTH_BEFORE_REPLAY",
            "requirement": "Any redesigned passive candidate must cover at least 4 trade dates and at least 8 symbols before bounded pilot replay can be precommitted.",
            "required_before_phase203": 1,
        },
        {
            "contract_id": "P202_ADVERSE_SELECTION_CEILING",
            "requirement": "Candidate family must lower passive adverse-selection toxicity versus Stage 01 and record a positive cost-clearing observation before replay.",
            "required_before_phase203": 1,
        },
        {
            "contract_id": "P202_NO_THRESHOLD_WIDENING",
            "requirement": "Do not rescue Phase201 failed buckets by widening thresholds after observing label outcomes; materialize redesigned features first.",
            "required_before_phase203": 1,
        },
        {
            "contract_id": "P202_LABEL_ONLY_NEXT",
            "requirement": "The next phase may materialize/audit redesigned labels only; strategy replay and test replay remain forbidden.",
            "required_before_phase203": 1,
        },
    ]
    out = pd.DataFrame(rows)
    out["redesigned_feature_rows"] = int(len(redesign))
    out["strategy_replay_allowed"] = 0
    out["test_replay_allowed_next"] = 0
    return out


def build_phase203_action_plan() -> pd.DataFrame:
    rows = [
        {
            "action_id": "P203_MATERIALIZE_QUEUE_RECOVERY_PERSISTENCE_LABELS",
            "priority": 1,
            "action": "Materialize redesigned queue recovery persistence labels over Stage 01 shards.",
            "allowed_scope": "label_only_no_replay",
            "strategy_replay_allowed": 0,
        },
        {
            "action_id": "P203_MATERIALIZE_TOXICITY_ABSTENTION_FILTERS",
            "priority": 2,
            "action": "Materialize toxicity abstention filters and compare against Phase201 adverse-selection failures.",
            "allowed_scope": "label_only_no_replay",
            "strategy_replay_allowed": 0,
        },
        {
            "action_id": "P203_AUDIT_SYMBOL_MONTH_STABILITY",
            "priority": 3,
            "action": "Audit symbol/month stability for redesigned passive feature families.",
            "allowed_scope": "label_only_no_replay",
            "strategy_replay_allowed": 0,
        },
    ]
    return pd.DataFrame(rows)


def build_gates(phase201: pd.DataFrame, failure: pd.DataFrame, redesign: pd.DataFrame, contract: pd.DataFrame, actions: pd.DataFrame) -> pd.DataFrame:
    phase201_complete = as_int(metric_value(phase201, "phase201_label_only_stage01_complete", 0))
    pre_replay = as_int(metric_value(phase201, "phase201_pre_replay_candidate_rows", 0))
    return pd.DataFrame(
        [
            {"gate_id": "P202_PHASE201_COMPLETE", "gate_pass": int(phase201_complete == 1), "evidence": f"phase201_complete={phase201_complete}", "severity": "hard"},
            {"gate_id": "P202_STAGE01_NO_REPLAY_CANDIDATE_ACKNOWLEDGED", "gate_pass": int(pre_replay == 0), "evidence": f"pre_replay_candidate_rows={pre_replay}", "severity": "hard"},
            {"gate_id": "P202_FAILURE_DECOMPOSITION_RECORDED", "gate_pass": int(len(failure) >= 2 and failure["must_address_before_replay"].astype(int).eq(1).all()), "evidence": f"failure_rows={len(failure)}", "severity": "hard"},
            {"gate_id": "P202_REDESIGNED_FEATURE_CONTRACT_RECORDED", "gate_pass": int(len(redesign) >= 4 and redesign["label_only_materialization_required"].astype(int).eq(1).all()), "evidence": f"redesign_rows={len(redesign)}", "severity": "hard"},
            {"gate_id": "P202_ACCEPTANCE_CONTRACT_RECORDED", "gate_pass": int(len(contract) >= 4 and contract["required_before_phase203"].astype(int).eq(1).all()), "evidence": f"contract_rows={len(contract)}", "severity": "hard"},
            {"gate_id": "P202_PHASE203_ACTION_PLAN_LABEL_ONLY", "gate_pass": int(len(actions) >= 3 and actions["strategy_replay_allowed"].astype(int).eq(0).all()), "evidence": f"action_rows={len(actions)}", "severity": "hard"},
            {"gate_id": "P202_NO_REPLAY_OR_PROMOTION", "gate_pass": 1, "evidence": "strategy_replay=0; test_replay=0; promotion=0; paper_live=0", "severity": "hard"},
        ]
    )


def build_acceptance(failure: pd.DataFrame, redesign: pd.DataFrame, contract: pd.DataFrame, actions: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates.loc[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(int).sum()) if not hard.empty else 0
    return pd.DataFrame(
        [
            ("phase202_failure_decomposition_rows", int(len(failure)), "Failure rows from Phase201"),
            ("phase202_redesigned_feature_rows", int(len(redesign)), "Redesigned passive feature rows"),
            ("phase202_acceptance_contract_rows", int(len(contract)), "Acceptance contract rows"),
            ("phase202_phase203_action_rows", int(len(actions)), "Next label-only action rows"),
            ("phase202_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase202_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase202_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase202_passive_feature_redesign_precommit_complete", int(len(hard) > 0 and hard_pass == len(hard)), "1 means Phase202 completed"),
            ("phase202_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase202_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase202_promotion_allowed", 0, "No promotion opened"),
            ("phase202_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase202_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase202_next_best_action", "run_phase203_redesigned_passive_label_materialization_no_replay", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase202 Passive Feature Redesign Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase202 precommits a redesigned passive feature path after Phase201 improved breadth but found no pre-replay candidate.",
        "It remains label-only: no replay, test, orders, fills, P&L, promotion or paper/live acceptance.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase202_passive_feature_redesign_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase202(phase118_dir: Path, phase201_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase201 = read_csv(phase201_dir / "phase201_stage01_acceptance_summary.csv")
    base_contract = read_csv(phase118_dir / "richer_passive_feature_contract.csv")
    failure = build_failure_decomposition(phase201)
    redesign = build_redesigned_feature_contract(base_contract)
    contract = build_acceptance_contract(redesign)
    actions = build_phase203_action_plan()
    gates = build_gates(phase201, failure, redesign, contract, actions)
    acceptance = build_acceptance(failure, redesign, contract, actions, gates)

    failure.to_csv(output_dir / "phase202_failure_decomposition.csv", index=False)
    redesign.to_csv(output_dir / "phase202_redesigned_passive_feature_contract.csv", index=False)
    contract.to_csv(output_dir / "phase202_acceptance_contract.csv", index=False)
    actions.to_csv(output_dir / "phase202_phase203_label_only_action_plan.csv", index=False)
    gates.to_csv(output_dir / "phase202_passive_feature_redesign_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase202_passive_feature_redesign_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Failure Decomposition": failure,
            "Redesigned Passive Feature Contract": redesign,
            "Acceptance Contract": contract,
            "Phase203 Action Plan": actions,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase202_passive_feature_redesign_precommit_no_replay",
        **reproducibility_fields(
            artifact_id="phase202_passive_feature_redesign_precommit",
            generated_utc=generated,
            inputs={
                "phase201_acceptance": str(phase201_dir / "phase201_stage01_acceptance_summary.csv"),
                "phase118_feature_contract": str(phase118_dir / "richer_passive_feature_contract.csv"),
            },
            parameters={
                "precommit_scope": "redesigned_passive_queue_features_label_only",
                "strategy_replay_allowed": "0",
                "test_replay_allowed_next": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "failure": str(output_dir / "phase202_failure_decomposition.csv"),
                "redesign": str(output_dir / "phase202_redesigned_passive_feature_contract.csv"),
                "contract": str(output_dir / "phase202_acceptance_contract.csv"),
                "actions": str(output_dir / "phase202_phase203_label_only_action_plan.csv"),
                "gates": str(output_dir / "phase202_passive_feature_redesign_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase202_passive_feature_redesign_acceptance_summary.csv"),
                "report": str(output_dir / "phase202_passive_feature_redesign_precommit_report.md"),
            },
            scenario_ids="phase202_passive_feature_redesign_precommit_no_replay",
            cost_model_version="phase66_phase120_passive_cost_toxicity_labels",
            latency_model_version="not_applicable_no_strategy_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase202_passive_feature_redesign_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase118-dir", type=Path, default=DEFAULT_PHASE118_DIR)
    parser.add_argument("--phase201-dir", type=Path, default=DEFAULT_PHASE201_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase202(args.phase118_dir, args.phase201_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
