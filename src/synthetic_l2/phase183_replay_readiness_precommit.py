from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE176_DIR = Path("outputs/phase176")
DEFAULT_PHASE180_DIR = Path("outputs/phase180")
DEFAULT_PHASE181_DIR = Path("outputs/phase181")
DEFAULT_PHASE182_DIR = Path("outputs/phase182")
DEFAULT_PHASE179_DIR = Path("outputs/phase179")
DEFAULT_OUTPUT_DIR = Path("outputs/phase183")
FORBIDDEN_OUTPUTS = "order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance"


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


def build_replay_input_contract(
    families: pd.DataFrame,
    feature_inventory: pd.DataFrame,
    label_inventory: pd.DataFrame,
    latency_profiles: pd.DataFrame,
) -> pd.DataFrame:
    feature_partitions = int(len(feature_inventory))
    label_partitions = int(len(label_inventory))
    feature_rows = int(feature_inventory["rows"].sum()) if not feature_inventory.empty and "rows" in feature_inventory.columns else 0
    label_rows = int(label_inventory["rows"].sum()) if not label_inventory.empty and "rows" in label_inventory.columns else 0
    allowed_profiles = ";".join(latency_profiles.loc[latency_profiles["allowed_for_promotion"].astype(int).eq(1), "profile_id"].astype(str).tolist()) if not latency_profiles.empty else ""
    rows = []
    for item in families.to_dict("records"):
        rows.append(
            {
                "strategy_family_id": item["strategy_family_id"],
                "allowed_feature_ids": item["allowed_feature_ids"],
                "feature_partitions_required": feature_partitions,
                "label_partitions_required": label_partitions,
                "feature_rows_available": feature_rows,
                "label_rows_available": label_rows,
                "allowed_latency_profiles_for_future_replay": allowed_profiles,
                "diagnostic_only_profiles": "P180_ZERO_LATENCY_CONTROL_DIAGNOSTIC_ONLY",
                "cost_catalog_required": "phase180_zerodha_equity_cost_component_catalog",
                "label_leakage_audit_required": "phase182_label_quality_leakage_audit_pass",
                "replay_opened_by_phase183": 0,
            }
        )
    return pd.DataFrame(rows)


def build_replay_gate_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "gate_id": "P183_TRAIN_ONLY_FIT",
                "gate_definition": "All model fitting, baselines, feature transforms and threshold choices must fit on train dates only unless validation-use is explicitly declared.",
                "required_before_phase184": 1,
                "failure_action": "block_replay",
            },
            {
                "gate_id": "P183_VALIDATION_SELECTION_ONLY",
                "gate_definition": "Validation date may select among predeclared families/thresholds only; no test-date feedback allowed.",
                "required_before_phase184": 1,
                "failure_action": "block_replay",
            },
            {
                "gate_id": "P183_TEST_UNTOUCHED_UNTIL_FINAL",
                "gate_definition": "Test date remains untouched until the replay runner has produced train/validation-only readiness evidence.",
                "required_before_phase184": 1,
                "failure_action": "block_replay",
            },
            {
                "gate_id": "P183_COST_LATENCY_BOUND",
                "gate_definition": "Future replay must bind Phase180 Zerodha cost catalog and retail/stressed latency profiles before any net result.",
                "required_before_phase184": 1,
                "failure_action": "block_replay",
            },
            {
                "gate_id": "P183_BLOCKLIST_OVERLAP_SCAN",
                "gate_definition": "Future replay must scan candidate rules for overlap with Phase164, Phase167 and Phase131-136 blocked forms.",
                "required_before_phase184": 1,
                "failure_action": "block_replay",
            },
            {
                "gate_id": "P183_NEGATIVE_CONTROLS_REQUIRED",
                "gate_definition": "Future replay must include shuffled-time and shuffled-symbol negative controls before acceptance can be interpreted.",
                "required_before_phase184": 1,
                "failure_action": "block_acceptance",
            },
            {
                "gate_id": "P183_KILL_SWITCH_PREDECLARED",
                "gate_definition": "Future replay must abort promotion if only zero-latency/control rows are positive or if retail/stressed profiles are negative.",
                "required_before_phase184": 1,
                "failure_action": "block_promotion",
            },
        ]
    )


def build_kill_switch_catalog() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "kill_switch_id": "P183_ZERO_LATENCY_ONLY_EDGE",
                "condition": "positive_result_count_zero_latency > 0 and positive_result_count_retail_stressed == 0",
                "action": "reject_for_promotion_and_report_control_only_edge",
            },
            {
                "kill_switch_id": "P183_TEST_DATE_SELECTION_LEAK",
                "condition": "any_threshold_or_family_selection_uses_test_untouched_rows",
                "action": "invalidate_replay_and_return_to_phase182_or_phase183",
            },
            {
                "kill_switch_id": "P183_FORBIDDEN_FORM_OVERLAP",
                "condition": "candidate_rule_overlaps_phase164_phase167_or_phase131_136_blocklist",
                "action": "block_replay_before_execution",
            },
            {
                "kill_switch_id": "P183_COST_LATENCY_UNBOUND",
                "condition": "any_net_metric_computed_without_phase180_cost_and_latency_profile_binding",
                "action": "invalidate_result",
            },
        ]
    )


def build_gate_evaluation(
    phase176: pd.DataFrame,
    phase180: pd.DataFrame,
    phase181: pd.DataFrame,
    phase182: pd.DataFrame,
    replay_contract: pd.DataFrame,
    gate_contract: pd.DataFrame,
    kill_switches: pd.DataFrame,
) -> pd.DataFrame:
    features_materialized = as_int(metric_value(phase176, "phase176_features_materialized", 0))
    phase180_ready = as_int(metric_value(phase180, "phase180_precommit_ready", 0))
    labels_materialized = as_int(metric_value(phase181, "phase181_labels_materialized", 0))
    label_audit_pass = as_int(metric_value(phase182, "phase182_label_quality_leakage_audit_pass", 0))
    return pd.DataFrame(
        [
            {
                "gate_id": "P183_PHASE176_FEATURES_MATERIALIZED",
                "gate_pass": int(features_materialized == 1),
                "evidence": f"phase176_features_materialized={features_materialized}",
                "severity": "hard",
            },
            {
                "gate_id": "P183_PHASE180_COST_LATENCY_LABEL_PRECOMMIT_READY",
                "gate_pass": int(phase180_ready == 1),
                "evidence": f"phase180_precommit_ready={phase180_ready}",
                "severity": "hard",
            },
            {
                "gate_id": "P183_PHASE181_LABELS_MATERIALIZED",
                "gate_pass": int(labels_materialized == 1),
                "evidence": f"phase181_labels_materialized={labels_materialized}",
                "severity": "hard",
            },
            {
                "gate_id": "P183_PHASE182_LABEL_AUDIT_PASS",
                "gate_pass": int(label_audit_pass == 1),
                "evidence": f"phase182_label_quality_leakage_audit_pass={label_audit_pass}",
                "severity": "hard",
            },
            {
                "gate_id": "P183_REPLAY_INPUT_CONTRACT_DECLARED",
                "gate_pass": int(len(replay_contract) >= 3 and replay_contract["replay_opened_by_phase183"].astype(int).eq(0).all()),
                "evidence": f"replay_contract_rows={len(replay_contract)}",
                "severity": "hard",
            },
            {
                "gate_id": "P183_REPLAY_GATE_CONTRACT_DECLARED",
                "gate_pass": int(len(gate_contract) >= 7),
                "evidence": f"gate_contract_rows={len(gate_contract)}",
                "severity": "hard",
            },
            {
                "gate_id": "P183_KILL_SWITCHES_DECLARED",
                "gate_pass": int(len(kill_switches) >= 4),
                "evidence": f"kill_switch_rows={len(kill_switches)}",
                "severity": "hard",
            },
            {
                "gate_id": "P183_NO_PNL_OR_REPLAY_OUTPUTS",
                "gate_pass": 1,
                "evidence": "replay-readiness precommit only; forbidden_outputs=" + FORBIDDEN_OUTPUTS,
                "severity": "hard",
            },
        ]
    )


def build_acceptance_summary(
    replay_contract: pd.DataFrame,
    gate_contract: pd.DataFrame,
    kill_switches: pd.DataFrame,
    gates: pd.DataFrame,
) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0
    readiness_precommitted = int(not hard.empty and hard_pass == len(hard))
    return pd.DataFrame(
        [
            ("phase183_replay_input_contract_rows", int(len(replay_contract)), "Replay input contract rows"),
            ("phase183_replay_gate_contract_rows", int(len(gate_contract)), "Future replay gates precommitted"),
            ("phase183_kill_switch_rows", int(len(kill_switches)), "Kill-switch rows precommitted"),
            ("phase183_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase183_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase183_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase183_replay_readiness_precommitted", readiness_precommitted, "1 means replay design may be implemented next"),
            ("phase183_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase183_pnl_allowed", 0, "P&L remains closed"),
            ("phase183_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase183_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase183_next_best_action", "build_phase184_train_validation_replay_dry_run_no_test_no_promotion" if readiness_precommitted else "repair_phase183_replay_readiness_precommit", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase183 Replay-readiness Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase183 precommits the exact conditions under which a later replay implementation may be built.",
        "It does not run replay, emit orders/fills, calculate P&L, claim profitability, or open paper/live acceptance.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase183_replay_readiness_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase183(
    phase176_dir: Path,
    phase179_dir: Path,
    phase180_dir: Path,
    phase181_dir: Path,
    phase182_dir: Path,
    output_dir: Path,
    base_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase176 = read_csv(phase176_dir / "phase176_receive_flow_feature_materializer_acceptance_summary.csv")
    feature_inventory = read_csv(phase176_dir / "phase176_feature_partition_inventory.csv")
    families = read_csv(phase179_dir / "phase179_strategy_family_catalog.csv")
    phase180 = read_csv(phase180_dir / "phase180_cost_latency_label_precommit_acceptance_summary.csv")
    latency_profiles = read_csv(phase180_dir / "phase180_latency_slippage_profile_catalog.csv")
    phase181 = read_csv(phase181_dir / "phase181_label_materialization_acceptance_summary.csv")
    label_inventory = read_csv(phase181_dir / "phase181_label_partition_inventory.csv")
    phase182 = read_csv(phase182_dir / "phase182_label_quality_leakage_audit_acceptance_summary.csv")

    replay_contract = build_replay_input_contract(families, feature_inventory, label_inventory, latency_profiles)
    gate_contract = build_replay_gate_contract()
    kill_switches = build_kill_switch_catalog()
    gates = build_gate_evaluation(phase176, phase180, phase181, phase182, replay_contract, gate_contract, kill_switches)
    acceptance = build_acceptance_summary(replay_contract, gate_contract, kill_switches, gates)

    replay_contract.to_csv(output_dir / "phase183_replay_input_contract.csv", index=False)
    gate_contract.to_csv(output_dir / "phase183_future_replay_gate_contract.csv", index=False)
    kill_switches.to_csv(output_dir / "phase183_replay_kill_switch_catalog.csv", index=False)
    gates.to_csv(output_dir / "phase183_replay_readiness_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase183_replay_readiness_precommit_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Replay Input Contract": replay_contract,
            "Future Replay Gate Contract": gate_contract,
            "Replay Kill-switch Catalog": kill_switches,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase183_replay_readiness_precommit",
        **reproducibility_fields(
            artifact_id="phase183_replay_readiness_precommit",
            generated_utc=generated,
            inputs={
                "phase176_acceptance": str(phase176_dir / "phase176_receive_flow_feature_materializer_acceptance_summary.csv"),
                "phase176_feature_inventory": str(phase176_dir / "phase176_feature_partition_inventory.csv"),
                "phase179_strategy_family_catalog": str(phase179_dir / "phase179_strategy_family_catalog.csv"),
                "phase180_acceptance": str(phase180_dir / "phase180_cost_latency_label_precommit_acceptance_summary.csv"),
                "phase180_latency_profiles": str(phase180_dir / "phase180_latency_slippage_profile_catalog.csv"),
                "phase181_acceptance": str(phase181_dir / "phase181_label_materialization_acceptance_summary.csv"),
                "phase181_label_inventory": str(phase181_dir / "phase181_label_partition_inventory.csv"),
                "phase182_acceptance": str(phase182_dir / "phase182_label_quality_leakage_audit_acceptance_summary.csv"),
            },
            parameters={
                "precommit_policy": "replay_readiness_only_no_pnl",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
                "next_required_gate": "phase184_train_validation_replay_dry_run_no_test_no_promotion",
            },
            outputs={
                "replay_input_contract": str(output_dir / "phase183_replay_input_contract.csv"),
                "future_replay_gate_contract": str(output_dir / "phase183_future_replay_gate_contract.csv"),
                "kill_switch_catalog": str(output_dir / "phase183_replay_kill_switch_catalog.csv"),
                "gate_evaluation": str(output_dir / "phase183_replay_readiness_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase183_replay_readiness_precommit_acceptance_summary.csv"),
                "report": str(output_dir / "phase183_replay_readiness_precommit_report.md"),
            },
            random_seed="none_deterministic_replay_readiness_precommit",
            scenario_ids="phase183_replay_readiness_precommit",
            cost_model_version="phase180_pinned_required_for_future_replay",
            latency_model_version="phase180_profiles_required_for_future_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase183_replay_readiness_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase176-dir", type=Path, default=DEFAULT_PHASE176_DIR)
    parser.add_argument("--phase179-dir", type=Path, default=DEFAULT_PHASE179_DIR)
    parser.add_argument("--phase180-dir", type=Path, default=DEFAULT_PHASE180_DIR)
    parser.add_argument("--phase181-dir", type=Path, default=DEFAULT_PHASE181_DIR)
    parser.add_argument("--phase182-dir", type=Path, default=DEFAULT_PHASE182_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase183(args.phase176_dir, args.phase179_dir, args.phase180_dir, args.phase181_dir, args.phase182_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
