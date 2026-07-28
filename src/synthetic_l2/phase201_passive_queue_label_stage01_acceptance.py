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
DEFAULT_STAGE01_DIR = Path("outputs/phase120/P120_LABEL_STAGE_01_MIN_BREADTH")
DEFAULT_OUTPUT_DIR = Path("outputs/phase201")
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


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def build_stage_inventory(stage_dir: Path) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for phase, rel in [
        ("phase66", "phase66/passive_label_acceptance_summary.csv"),
        ("phase68", "phase68/phase68_replenishment_after_touch_labels_manifest.json"),
        ("phase69", "phase69/phase69_spread_transition_labels_manifest.json"),
        ("phase119", "phase119/phase119_richer_passive_label_builder_acceptance_summary.csv"),
    ]:
        path = stage_dir / rel
        rows.append(
            {
                "stage_id": "P120_LABEL_STAGE_01_MIN_BREADTH",
                "phase": phase,
                "artifact_path": str(path),
                "artifact_exists": int(path.exists()),
                "strategy_replay_allowed": 0,
            }
        )
    return pd.DataFrame(rows)


def build_label_outcome_summary(phase66: pd.DataFrame, phase119: pd.DataFrame, family_summary: pd.DataFrame) -> pd.DataFrame:
    family = family_summary.iloc[0].to_dict() if not family_summary.empty else {}
    return pd.DataFrame(
        [
            {
                "summary_id": "P201_STAGE01_PASSIVE_LABEL_OUTCOME",
                "phase66_shards_scanned": as_int(metric_value(phase66, "phase66_shards_scanned", 0)),
                "phase66_inferred_touches": as_int(metric_value(phase66, "phase66_inferred_touches", 0)),
                "phase66_label_candidate_rows": as_int(metric_value(phase66, "phase66_label_candidate_rows", 0)),
                "phase66_best_mean_after_cost_bps_if_touched": as_float(metric_value(phase66, "phase66_best_mean_after_cost_bps_if_touched", 0.0)),
                "phase119_joined_label_candidate_rows": as_int(metric_value(phase119, "phase119_joined_label_candidate_rows", 0)),
                "phase119_pre_replay_candidate_rows": as_int(metric_value(phase119, "phase119_pre_replay_candidate_rows", 0)),
                "phase119_max_candidate_symbols": as_int(metric_value(phase119, "phase119_max_candidate_symbols", 0)),
                "phase119_max_candidate_trade_dates": as_int(metric_value(phase119, "phase119_max_candidate_trade_dates", 0)),
                "phase119_bounded_pilot_replay_allowed": as_int(metric_value(phase119, "phase119_bounded_pilot_replay_allowed", 0)),
                "family_dominant_failure_reason": family.get("dominant_failure_reason", ""),
                "stage01_label_expansion_complete": 1,
                "stage01_replay_candidate_survived": as_int(metric_value(phase119, "phase119_pre_replay_candidate_rows", 0)) > 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
            }
        ]
    )


def build_next_decision(outcome: pd.DataFrame) -> pd.DataFrame:
    row = outcome.iloc[0] if not outcome.empty else {}
    pre_replay = as_int(row.get("phase119_pre_replay_candidate_rows", 0))
    max_dates = as_int(row.get("phase119_max_candidate_trade_dates", 0))
    max_symbols = as_int(row.get("phase119_max_candidate_symbols", 0))
    if pre_replay > 0:
        decision = "precommit_bounded_passive_pilot_replay_contract_no_execution"
        next_action = "build_phase202_bounded_passive_pilot_precommit_no_execution"
    elif max_dates >= 4 and max_symbols >= 4:
        decision = "stage01_breadth_improved_but_gates_failed_redesign_passive_features_before_stage02"
        next_action = "run_phase202_passive_feature_redesign_precommit_no_replay"
    else:
        decision = "stage01_insufficient_breadth_continue_label_only_stage02"
        next_action = "run_phase202_passive_label_only_stage02_train_half_no_replay"
    return pd.DataFrame(
        [
            {
                "decision_id": "P201_STAGE01_PASSIVE_QUEUE_DECISION",
                "phase201_decision": decision,
                "next_best_action": next_action,
                "pre_replay_candidate_rows": pre_replay,
                "max_candidate_trade_dates": max_dates,
                "max_candidate_symbols": max_symbols,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
            }
        ]
    )


def build_gates(phase200: pd.DataFrame, inventory: pd.DataFrame, outcome: pd.DataFrame, decision: pd.DataFrame) -> pd.DataFrame:
    phase200_complete = as_int(metric_value(phase200, "phase200_material_new_hypothesis_precommit_complete", 0))
    row = outcome.iloc[0] if not outcome.empty else {}
    drow = decision.iloc[0] if not decision.empty else {}
    return pd.DataFrame(
        [
            {"gate_id": "P201_PHASE200_PRECOMMIT_COMPLETE", "gate_pass": int(phase200_complete == 1), "evidence": f"phase200_complete={phase200_complete}", "severity": "hard"},
            {"gate_id": "P201_STAGE01_ARTIFACTS_PRESENT", "gate_pass": int(not inventory.empty and inventory["artifact_exists"].astype(int).eq(1).all()), "evidence": f"artifact_rows={len(inventory)}; present={int(inventory['artifact_exists'].astype(int).sum()) if not inventory.empty else 0}", "severity": "hard"},
            {"gate_id": "P201_LABEL_ONLY_EXPANSION_RECORDED", "gate_pass": int(as_int(row.get("stage01_label_expansion_complete", 0)) == 1 and as_int(row.get("phase66_shards_scanned", 0)) >= 128), "evidence": f"phase66_shards={row.get('phase66_shards_scanned', '')}", "severity": "hard"},
            {"gate_id": "P201_PHASE119_OUTCOME_RECORDED", "gate_pass": int(as_int(row.get("phase119_joined_label_candidate_rows", 0)) > 0), "evidence": f"joined_rows={row.get('phase119_joined_label_candidate_rows', '')}; pre_replay={row.get('phase119_pre_replay_candidate_rows', '')}", "severity": "hard"},
            {"gate_id": "P201_REPLAY_REMAINS_CLOSED", "gate_pass": int(as_int(drow.get("strategy_replay_allowed", 1)) == 0 and as_int(drow.get("test_replay_allowed_next", 1)) == 0), "evidence": "strategy_replay=0; test_replay=0", "severity": "hard"},
            {"gate_id": "P201_PROMOTION_AND_PAPER_LIVE_CLOSED", "gate_pass": int(as_int(drow.get("promotion_allowed", 1)) == 0 and as_int(drow.get("paper_or_live_acceptance_allowed", 1)) == 0), "evidence": "promotion=0; paper_live=0", "severity": "hard"},
        ]
    )


def build_acceptance(outcome: pd.DataFrame, decision: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates.loc[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(int).sum()) if not hard.empty else 0
    row = outcome.iloc[0] if not outcome.empty else {}
    drow = decision.iloc[0] if not decision.empty else {}
    return pd.DataFrame(
        [
            ("phase201_stage01_shards_scanned", row.get("phase66_shards_scanned", ""), "Stage 01 dense shards scanned"),
            ("phase201_inferred_touches", row.get("phase66_inferred_touches", ""), "Passive inferred touches"),
            ("phase201_joined_label_candidate_rows", row.get("phase119_joined_label_candidate_rows", ""), "Joined richer passive candidates"),
            ("phase201_pre_replay_candidate_rows", row.get("phase119_pre_replay_candidate_rows", ""), "Candidates passing pre-replay gates"),
            ("phase201_max_candidate_symbols", row.get("phase119_max_candidate_symbols", ""), "Max candidate symbol breadth"),
            ("phase201_max_candidate_trade_dates", row.get("phase119_max_candidate_trade_dates", ""), "Max candidate date breadth"),
            ("phase201_dominant_failure_reason", row.get("family_dominant_failure_reason", ""), "Dominant failure reason"),
            ("phase201_decision", drow.get("phase201_decision", ""), "Stage 01 decision"),
            ("phase201_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase201_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase201_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase201_label_only_stage01_complete", int(len(hard) > 0 and hard_pass == len(hard)), "1 means Phase201 completed"),
            ("phase201_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase201_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase201_promotion_allowed", 0, "No promotion opened"),
            ("phase201_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase201_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase201_next_best_action", drow.get("next_best_action", ""), "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase201 Passive Queue Label-only Stage 01 Acceptance",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase201 records the Phase120 Stage 01 label-only passive expansion for the Phase200 passive queue hypothesis.",
        "It does not open strategy replay, test replay, orders, fills, P&L, promotion or paper/live acceptance.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase201_passive_queue_label_stage01_acceptance_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase201(phase200_dir: Path, stage01_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase200 = read_csv(phase200_dir / "phase200_material_new_hypothesis_acceptance_summary.csv")
    phase66 = read_csv(stage01_dir / "phase66/passive_label_acceptance_summary.csv")
    phase119 = read_csv(stage01_dir / "phase119/phase119_richer_passive_label_builder_acceptance_summary.csv")
    family_summary = read_csv(stage01_dir / "phase119/richer_passive_label_family_summary.csv")
    inventory = build_stage_inventory(stage01_dir)
    outcome = build_label_outcome_summary(phase66, phase119, family_summary)
    decision = build_next_decision(outcome)
    gates = build_gates(phase200, inventory, outcome, decision)
    acceptance = build_acceptance(outcome, decision, gates)

    inventory.to_csv(output_dir / "phase201_stage01_artifact_inventory.csv", index=False)
    outcome.to_csv(output_dir / "phase201_stage01_label_outcome_summary.csv", index=False)
    decision.to_csv(output_dir / "phase201_stage01_passive_queue_decision.csv", index=False)
    gates.to_csv(output_dir / "phase201_stage01_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase201_stage01_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Stage 01 Label Outcome": outcome,
            "Decision": decision,
            "Artifact Inventory": inventory,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase201_passive_queue_label_only_stage01_acceptance_no_replay",
        **reproducibility_fields(
            artifact_id="phase201_passive_queue_label_stage01_acceptance",
            generated_utc=generated,
            inputs={
                "phase200_acceptance": str(phase200_dir / "phase200_material_new_hypothesis_acceptance_summary.csv"),
                "stage01_phase66": str(stage01_dir / "phase66/passive_label_acceptance_summary.csv"),
                "stage01_phase119": str(stage01_dir / "phase119/phase119_richer_passive_label_builder_acceptance_summary.csv"),
                "stage01_family_summary": str(stage01_dir / "phase119/richer_passive_label_family_summary.csv"),
            },
            parameters={
                "stage_id": "P120_LABEL_STAGE_01_MIN_BREADTH",
                "strategy_replay_allowed": "0",
                "test_replay_allowed_next": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "inventory": str(output_dir / "phase201_stage01_artifact_inventory.csv"),
                "outcome": str(output_dir / "phase201_stage01_label_outcome_summary.csv"),
                "decision": str(output_dir / "phase201_stage01_passive_queue_decision.csv"),
                "gates": str(output_dir / "phase201_stage01_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase201_stage01_acceptance_summary.csv"),
                "report": str(output_dir / "phase201_passive_queue_label_stage01_acceptance_report.md"),
            },
            scenario_ids="phase201_passive_queue_label_stage01_acceptance_no_replay",
            cost_model_version="phase66_phase120_passive_cost_toxicity_labels",
            latency_model_version="not_applicable_no_strategy_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase201_stage01_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase200-dir", type=Path, default=DEFAULT_PHASE200_DIR)
    parser.add_argument("--stage01-dir", type=Path, default=DEFAULT_STAGE01_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase201(args.phase200_dir, args.stage01_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
