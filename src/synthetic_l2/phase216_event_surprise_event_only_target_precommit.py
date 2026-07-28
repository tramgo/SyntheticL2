from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE215_DIR = Path("outputs/phase215")
DEFAULT_OUTPUT_DIR = Path("outputs/phase216")
FORBIDDEN_OUTPUTS = "model_fit;model_prediction;strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export"
NEXT_ACTION = "run_phase217_event_only_design_matrix_precommit_no_model_no_replay_no_test"


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


def build_target_allowlist(interpretation: pd.DataFrame) -> pd.DataFrame:
    if interpretation.empty:
        return pd.DataFrame()
    passing = interpretation[pd.to_numeric(interpretation["interpretation_pass"], errors="coerce").fillna(0).astype(int).eq(1)].copy()
    passing = passing.sort_values(["horizon_sec", "label_name", "split_role"])
    rows: list[dict[str, Any]] = []
    for (horizon, label_name), part in passing.groupby(["horizon_sec", "label_name"], sort=True):
        split_roles = sorted(part["split_role"].astype(str).unique().tolist())
        train_ok = "train" in split_roles
        validation_ok = "validation" in split_roles
        rows.append(
            {
                "phase216_target_id": f"P216_EVENT_ONLY_H{as_int(horizon)}s_{label_name}",
                "label_name": label_name,
                "horizon_sec": as_int(horizon),
                "allowed_split_roles": ";".join(split_roles),
                "train_interpretable": int(train_ok),
                "validation_interpretable": int(validation_ok),
                "event_only_filter": "event_surprise_bucket == 1",
                "positive_rate_min": float(pd.to_numeric(part["positive_rate"], errors="coerce").min()),
                "positive_rate_max": float(pd.to_numeric(part["positive_rate"], errors="coerce").max()),
                "event_surprise_share_min": float(pd.to_numeric(part["event_surprise_share"], errors="coerce").min()),
                "allowed_for_phase217_design_matrix": int(train_ok and validation_ok),
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            }
        )
    return pd.DataFrame(rows)


def build_exclusion_ledger(interpretation: pd.DataFrame) -> pd.DataFrame:
    if interpretation.empty:
        return pd.DataFrame()
    rejected = interpretation[pd.to_numeric(interpretation["interpretation_pass"], errors="coerce").fillna(0).astype(int).eq(0)].copy()
    rows: list[dict[str, Any]] = []
    for record in rejected.to_dict("records"):
        rows.append(
            {
                "phase216_exclusion_id": f"P216_EXCLUDE_{record.get('split_role')}_H{as_int(record.get('horizon_sec', 0))}s_{record.get('label_name')}",
                "split_role": record.get("split_role", ""),
                "horizon_sec": as_int(record.get("horizon_sec", 0)),
                "label_name": record.get("label_name", ""),
                "positive_rate": record.get("positive_rate", ""),
                "event_surprise_share": record.get("event_surprise_share", ""),
                "exclusion_reason": record.get("verdict", "failed_phase215_event_only_interpretation"),
                "excluded_from_phase217_design_matrix": 1,
                "threshold_widening_allowed": 0,
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            }
        )
    return pd.DataFrame(rows)


def build_event_only_contract(allowlist: pd.DataFrame, exclusions: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "phase216_contract_id": "P216_EVENT_ONLY_TARGET_CONTRACT",
                "contract": "Use Phase214 event-surprise labels only on rows where event_surprise_bucket == 1; do not train all-row predictors on sparse conditional labels.",
                "allowed_target_rows": len(allowlist),
                "allowed_full_train_validation_target_rows": int(allowlist["allowed_for_phase217_design_matrix"].astype(int).sum()) if not allowlist.empty else 0,
                "excluded_split_horizon_label_rows": len(exclusions),
                "sealed_test_policy": "record_inventory_only_zero_rows_used",
                "threshold_widening_allowed": 0,
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
                "profitability_claim_allowed": 0,
            }
        ]
    )


def build_control_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "phase216_control_id": "P216_EVENT_ONLY_BASE_RATE_CONTROL",
                "control_type": "base_rate",
                "requirement": "Phase217 must compute event-only base-rate controls for each allowed label/horizon before any future fit.",
                "required_for_phase217": 1,
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
            },
            {
                "phase216_control_id": "P216_EVENT_TIME_SHUFFLE_CONTROL",
                "control_type": "time_shuffle",
                "requirement": "Phase217 must preserve a shuffled event-time control to test whether event timing matters beyond label base rates.",
                "required_for_phase217": 1,
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
            },
            {
                "phase216_control_id": "P216_SEALED_TEST_ZERO_USE_CONTROL",
                "control_type": "sealed_test",
                "requirement": "Phase217 may inventory sealed test rows but must use zero sealed test rows.",
                "required_for_phase217": 1,
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
            },
        ]
    )


def build_phase217_work_order(allowlist: pd.DataFrame, controls: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "phase217_work_order_id": "P217_EVENT_ONLY_DESIGN_MATRIX_PRECOMMIT",
                "work_order": "Precommit an event-only design matrix using only allowed Phase216 label/horizon rows and event_surprise_bucket == 1 filter.",
                "allowed_target_rows": len(allowlist),
                "full_train_validation_target_rows": int(allowlist["allowed_for_phase217_design_matrix"].astype(int).sum()) if not allowlist.empty else 0,
                "required_control_rows": len(controls),
                "allowed_next_scope": "design_matrix_contract_only_no_model_no_replay_no_test",
                "model_fit_allowed_next": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            }
        ]
    )


def build_forbidden_execution_ledger() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "forbidden_output": item,
                "emitted_in_phase216": 0,
                "allowed_in_phase216": 0,
                "rationale": "Phase216 is an event-only target precommit and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact.",
            }
            for item in FORBIDDEN_OUTPUTS.split(";")
        ]
    )


def build_gates(phase215: pd.DataFrame, allowlist: pd.DataFrame, exclusions: pd.DataFrame, contract: pd.DataFrame, controls: pd.DataFrame, work_order: pd.DataFrame, forbidden: pd.DataFrame) -> pd.DataFrame:
    phase215_complete = as_int(metric_value(phase215, "phase215_event_surprise_label_quality_interpretation_complete", 0))
    passing_rows = as_int(metric_value(phase215, "phase215_passing_interpretation_rows", 0))
    allowed_full = int(allowlist["allowed_for_phase217_design_matrix"].astype(int).sum()) if not allowlist.empty else 0
    replay_flags = 0
    for frame in [allowlist, exclusions, contract, controls, work_order]:
        for col in ["model_fit_allowed_now", "model_fit_allowed_next", "strategy_replay_allowed", "test_replay_allowed_next", "promotion_allowed", "profitability_claim_allowed", "threshold_widening_allowed"]:
            if not frame.empty and col in frame.columns:
                replay_flags += int(pd.to_numeric(frame[col], errors="coerce").fillna(0).sum())
    forbidden_emitted = int(forbidden["emitted_in_phase216"].astype(int).sum()) if not forbidden.empty else 1
    return pd.DataFrame(
        [
            ("P216_PHASE215_COMPLETE", phase215_complete == 1, f"phase215_complete={phase215_complete}", "hard"),
            ("P216_PHASE215_PASSING_ROWS_POSITIVE", passing_rows > 0, f"passing_rows={passing_rows}", "hard"),
            ("P216_ALLOWLIST_RECORDED", len(allowlist) >= 3 and allowed_full >= 3, f"allowlist_rows={len(allowlist)}; full_train_validation_rows={allowed_full}", "hard"),
            ("P216_EXCLUSION_LEDGER_RECORDED", len(exclusions) > 0, f"exclusion_rows={len(exclusions)}", "hard"),
            ("P216_EVENT_ONLY_CONTRACT_RECORDED", len(contract) == 1, f"contract_rows={len(contract)}", "hard"),
            ("P216_CONTROLS_AND_WORK_ORDER_RECORDED", len(controls) == 3 and len(work_order) == 1, f"controls={len(controls)}; work_order={len(work_order)}", "hard"),
            ("P216_FORBIDDEN_OUTPUTS_CLEAN", forbidden_emitted == 0 and replay_flags == 0, f"forbidden_emitted={forbidden_emitted}; replay_flags={replay_flags}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(allowlist: pd.DataFrame, exclusions: pd.DataFrame, contract: pd.DataFrame, controls: pd.DataFrame, work_order: pd.DataFrame, forbidden: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("phase216_event_only_target_rows", len(allowlist), "Allowed event-only target rows"),
            ("phase216_full_train_validation_target_rows", int(allowlist["allowed_for_phase217_design_matrix"].astype(int).sum()) if not allowlist.empty else 0, "Allowed targets with both train and validation interpretable"),
            ("phase216_excluded_target_rows", len(exclusions), "Excluded split/horizon/label rows"),
            ("phase216_event_only_contract_rows", len(contract), "Event-only target contract rows"),
            ("phase216_control_contract_rows", len(controls), "Control contract rows"),
            ("phase216_phase217_work_order_rows", len(work_order), "Phase217 work-order rows"),
            ("phase216_forbidden_execution_rows", len(forbidden), "Forbidden execution rows"),
            ("phase216_gate_rows", len(gates), "Gates evaluated"),
            ("phase216_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase216_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase216_event_surprise_event_only_target_precommit_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase216 completed"),
            ("phase216_model_fit_allowed_next", 0, "No model fit opened"),
            ("phase216_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase216_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase216_promotion_allowed", 0, "No promotion opened"),
            ("phase216_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase216_profitability_claim_allowed", 0, "No profitability claim is allowed"),
            ("phase216_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase216_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase216 Event-surprise Event-only Target Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase216 converts Phase215's sparse-label interpretation into an event-only target contract.",
        "It permits only event_surprise_bucket == 1 targets for future design-matrix precommit and keeps model fitting, replay, sealed test, promotion, paper/live acceptance, and profitability claims closed.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase216_event_surprise_event_only_target_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase216(phase215_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase215 = read_csv(phase215_dir / "phase215_label_quality_interpretation_acceptance_summary.csv")
    interpretation = read_csv(phase215_dir / "phase215_label_quality_interpretation.csv")
    allowlist = build_target_allowlist(interpretation)
    exclusions = build_exclusion_ledger(interpretation)
    contract = build_event_only_contract(allowlist, exclusions)
    controls = build_control_contract()
    work_order = build_phase217_work_order(allowlist, controls)
    forbidden = build_forbidden_execution_ledger()
    gates = build_gates(phase215, allowlist, exclusions, contract, controls, work_order, forbidden)
    acceptance = build_acceptance(allowlist, exclusions, contract, controls, work_order, forbidden, gates)

    allowlist.to_csv(output_dir / "phase216_event_only_target_allowlist.csv", index=False)
    exclusions.to_csv(output_dir / "phase216_excluded_target_ledger.csv", index=False)
    contract.to_csv(output_dir / "phase216_event_only_target_contract.csv", index=False)
    controls.to_csv(output_dir / "phase216_control_contract.csv", index=False)
    work_order.to_csv(output_dir / "phase216_phase217_work_order.csv", index=False)
    forbidden.to_csv(output_dir / "phase216_execution_forbidden_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase216_event_only_target_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase216_event_only_target_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Event-only Target Allowlist": allowlist,
            "Excluded Target Ledger": exclusions,
            "Event-only Target Contract": contract,
            "Control Contract": controls,
            "Phase217 Work Order": work_order,
            "Forbidden Execution Ledger": forbidden,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase216_event_surprise_label_redesign_or_event_only_target_precommit_no_model_no_replay_no_test",
        **reproducibility_fields(
            artifact_id="phase216_event_surprise_event_only_target_precommit",
            generated_utc=generated,
            inputs={
                "phase215_acceptance": str(phase215_dir / "phase215_label_quality_interpretation_acceptance_summary.csv"),
                "phase215_interpretation": str(phase215_dir / "phase215_label_quality_interpretation.csv"),
            },
            parameters={
                "event_only_filter": "event_surprise_bucket == 1",
                "model_fit_allowed": "0",
                "strategy_replay_allowed": "0",
                "test_replay_allowed_next": "0",
                "threshold_widening_allowed": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "allowlist": str(output_dir / "phase216_event_only_target_allowlist.csv"),
                "exclusions": str(output_dir / "phase216_excluded_target_ledger.csv"),
                "contract": str(output_dir / "phase216_event_only_target_contract.csv"),
                "controls": str(output_dir / "phase216_control_contract.csv"),
                "work_order": str(output_dir / "phase216_phase217_work_order.csv"),
                "forbidden": str(output_dir / "phase216_execution_forbidden_ledger.csv"),
                "gates": str(output_dir / "phase216_event_only_target_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase216_event_only_target_acceptance_summary.csv"),
                "report": str(output_dir / "phase216_event_surprise_event_only_target_precommit_report.md"),
            },
            scenario_ids="phase216_event_surprise_event_only_target_precommit_no_model_no_replay_no_test",
            cost_model_version="not_applicable_no_replay",
            latency_model_version="not_applicable_no_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase216_event_only_target_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase216 event-only target precommit without model/replay/test.")
    parser.add_argument("--phase215-dir", type=Path, default=DEFAULT_PHASE215_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase216(args.phase215_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
