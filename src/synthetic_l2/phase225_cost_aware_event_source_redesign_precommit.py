from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE180_DIR = Path("outputs/phase180")
DEFAULT_PHASE224_DIR = Path("outputs/phase224")
DEFAULT_OUTPUT_DIR = Path("outputs/phase225")
SELECTED_ROUTE_ID = "P224_COST_AWARE_ACTIONABLE_EVENT_LABELS"
FORBIDDEN_OUTPUTS = "label_materialization;feature_materialization;model_fit;model_prediction;strategy_replay;broader_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export"
NEXT_ACTION = "run_phase226_cost_aware_event_label_materialization_dry_run_no_fit_no_replay_no_test"


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


def build_cost_hurdle_catalog(cost_catalog: pd.DataFrame, latency_catalog: pd.DataFrame) -> pd.DataFrame:
    profiles = ["P180_RETAIL_MARKETABLE_DEFAULT", "P180_STRESSED_RETAIL"]
    statutory_rows = len(cost_catalog) if not cost_catalog.empty else 0
    latency_id_col = "latency_profile_id" if "latency_profile_id" in latency_catalog.columns else "profile_id" if "profile_id" in latency_catalog.columns else ""
    latency_rows = latency_catalog[latency_catalog[latency_id_col].astype(str).isin(profiles)].copy() if not latency_catalog.empty and latency_id_col else pd.DataFrame()
    return pd.DataFrame(
        [
            {
                "phase225_cost_hurdle_id": "P225_COST_HURDLE_RETAIL_MARKETABLE",
                "latency_profile_id": "P180_RETAIL_MARKETABLE_DEFAULT",
                "hurdle_role": "primary_train_validation_acceptance_hurdle",
                "minimum_forward_edge_bps_rule": "gross_forward_move_bps_must_exceed_phase180_statutory_cost_plus_spread_latency_slippage_bound",
                "statutory_cost_catalog_rows_bound": statutory_rows,
                "latency_profile_rows_bound": int(len(latency_rows[latency_rows[latency_id_col].astype(str).eq("P180_RETAIL_MARKETABLE_DEFAULT")])) if not latency_rows.empty and latency_id_col else 0,
                "target_net_after_cost_floor_bps": 0.0,
                "safety_margin_bps": 1.0,
                "label_positive_condition": "forward_signed_move_bps - estimated_cost_bound_bps >= 1.0",
                "label_negative_condition": "forward_signed_move_bps + estimated_cost_bound_bps <= -1.0",
                "neutral_condition": "otherwise_no_action_label",
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            },
            {
                "phase225_cost_hurdle_id": "P225_COST_HURDLE_STRESSED_RETAIL",
                "latency_profile_id": "P180_STRESSED_RETAIL",
                "hurdle_role": "stress_acceptance_hurdle",
                "minimum_forward_edge_bps_rule": "candidate_must_remain_nonnegative_under_stressed_retail_bound_before_replay_precommit",
                "statutory_cost_catalog_rows_bound": statutory_rows,
                "latency_profile_rows_bound": int(len(latency_rows[latency_rows[latency_id_col].astype(str).eq("P180_STRESSED_RETAIL")])) if not latency_rows.empty and latency_id_col else 0,
                "target_net_after_cost_floor_bps": 0.0,
                "safety_margin_bps": 0.0,
                "label_positive_condition": "forward_signed_move_bps - stressed_estimated_cost_bound_bps >= 0.0",
                "label_negative_condition": "forward_signed_move_bps + stressed_estimated_cost_bound_bps <= 0.0",
                "neutral_condition": "otherwise_no_action_label",
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            },
        ]
    )


def build_label_contract() -> pd.DataFrame:
    horizons = [5, 15, 30]
    rows: list[dict[str, Any]] = []
    for horizon in horizons:
        rows.append(
            {
                "phase225_label_contract_id": f"P225_COST_AWARE_EVENT_MOVE_H{horizon}s",
                "label_family": "cost_aware_actionable_event_move",
                "horizon_sec": horizon,
                "source_event_filter": "event_surprise_bucket == 1",
                "price_reference": "last_price_at_event_to_future_mid_or_last_price_proxy",
                "directional_labels": "cost_aware_up;cost_aware_down;neutral_no_action",
                "positive_label_rule": "future_up_move_bps_exceeds_retail_cost_hurdle_and_stress_nonnegative",
                "negative_label_rule": "future_down_move_bps_exceeds_retail_cost_hurdle_and_stress_nonnegative",
                "neutral_label_rule": "forward_move_does_not_clear_cost_hurdle",
                "minimum_event_count_per_split": 1000,
                "minimum_symbol_count_per_split": 8,
                "minimum_trade_date_count_per_split": 5,
                "allowed_splits": "train;validation",
                "sealed_test_rows_used": 0,
                "threshold_widening_allowed": 0,
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            }
        )
    return pd.DataFrame(rows)


def build_negative_control_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "phase225_control_id": "P225_CONTROL_EVENT_TIME_SHUFFLE",
                "control_type": "event_time_shuffle_within_symbol_date_split",
                "purpose": "Reject labels whose apparent signal survives only because of event timing leakage or base-rate structure.",
                "required_before_fit": 1,
                "pass_condition": "model_or_screen_must_beat_shuffled_control_on_validation_before_replay_precommit",
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
            },
            {
                "phase225_control_id": "P225_CONTROL_SYMBOL_DATE_BASE_RATE",
                "control_type": "symbol_date_base_rate",
                "purpose": "Reject labels explained by symbol/date unconditional actionability rates.",
                "required_before_fit": 1,
                "pass_condition": "validation lift must exceed symbol-date base-rate control",
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
            },
            {
                "phase225_control_id": "P225_CONTROL_COST_HURDLE_ABLATION",
                "control_type": "cost_hurdle_ablation",
                "purpose": "Quantify whether cost-aware labels materially reduce churn versus pre-cost event-only labels.",
                "required_before_fit": 1,
                "pass_condition": "activation budget and positive-label rate must remain above minimum counts after cost hurdle",
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
            },
        ]
    )


def build_materialization_contract(labels: pd.DataFrame, controls: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "phase226_work_order_id": "P226_COST_AWARE_EVENT_LABEL_MATERIALIZATION_DRY_RUN",
                "work_order": "Materialize train/validation-only cost-aware actionable event labels using Phase225 frozen label and control contracts.",
                "label_contract_rows": len(labels),
                "negative_control_rows": len(controls),
                "required_inputs": "phase176_features;phase214_event_surprise_labels;phase180_cost_latency_catalogs",
                "required_outputs": "label_partition_inventory;quality_summary;control_summary;acceptance_summary",
                "allowed_next_scope": "label_materialization_dry_run_only_no_fit_no_replay_no_test",
                "label_materialization_allowed_next": 1,
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
                "emitted_in_phase225": 0,
                "allowed_in_phase225": 0,
                "rationale": "Phase225 precommits source/label/control contracts only and emits no materialized labels, fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, threshold-widening, or profitability artifact.",
            }
            for item in FORBIDDEN_OUTPUTS.split(";")
        ]
    )


def build_gates(phase224: pd.DataFrame, work_order_224: pd.DataFrame, cost_hurdle: pd.DataFrame, labels: pd.DataFrame, controls: pd.DataFrame, materialization: pd.DataFrame, forbidden: pd.DataFrame) -> pd.DataFrame:
    phase224_complete = as_int(metric_value(phase224, "phase224_event_only_signal_replay_closure_or_redesign_precommit_complete", 0))
    selected_route = str(metric_value(phase224, "phase224_selected_redesign_route", ""))
    work_selected = str(work_order_224["selected_route_id"].iloc[0]) if not work_order_224.empty and "selected_route_id" in work_order_224.columns else ""
    cost_bound_rows = int(pd.to_numeric(cost_hurdle["statutory_cost_catalog_rows_bound"], errors="coerce").fillna(0).min()) if not cost_hurdle.empty else 0
    latency_bound_rows = int(pd.to_numeric(cost_hurdle["latency_profile_rows_bound"], errors="coerce").fillna(0).sum()) if not cost_hurdle.empty else 0
    label_materialization_next = int(pd.to_numeric(materialization["label_materialization_allowed_next"], errors="coerce").fillna(0).sum()) if not materialization.empty else 0
    forbidden_emitted = int(pd.to_numeric(forbidden["emitted_in_phase225"], errors="coerce").fillna(0).sum()) if not forbidden.empty else 1
    forbidden_flags = 0
    for frame in [cost_hurdle, labels, controls, materialization]:
        for col in ["model_fit_allowed_now", "model_fit_allowed_next", "strategy_replay_allowed", "broader_replay_allowed_next", "test_replay_allowed_next", "promotion_allowed", "paper_or_live_acceptance_allowed", "profitability_claim_allowed", "threshold_widening_allowed"]:
            if not frame.empty and col in frame.columns:
                forbidden_flags += int(pd.to_numeric(frame[col], errors="coerce").fillna(0).sum())
    return pd.DataFrame(
        [
            ("P225_PHASE224_COMPLETE", phase224_complete == 1, f"phase224_complete={phase224_complete}", "hard"),
            ("P225_SELECTED_ROUTE_BOUND", selected_route == SELECTED_ROUTE_ID and work_selected == SELECTED_ROUTE_ID, f"phase224_selected={selected_route}; work_selected={work_selected}", "hard"),
            ("P225_COST_HURDLES_BOUND", len(cost_hurdle) == 2 and cost_bound_rows > 0 and latency_bound_rows == 2, f"cost_hurdle_rows={len(cost_hurdle)}; cost_rows={cost_bound_rows}; latency_rows={latency_bound_rows}", "hard"),
            ("P225_LABEL_CONTRACT_RECORDED", len(labels) == 3 and labels["sealed_test_rows_used"].astype(int).eq(0).all(), f"label_rows={len(labels)}", "hard"),
            ("P225_NEGATIVE_CONTROLS_RECORDED", len(controls) == 3 and controls["required_before_fit"].astype(int).eq(1).all(), f"control_rows={len(controls)}", "hard"),
            ("P225_PHASE226_MATERIALIZATION_WORK_ORDER_RECORDED", len(materialization) == 1 and label_materialization_next == 1, f"work_order_rows={len(materialization)}; materialization_next={label_materialization_next}", "hard"),
            ("P225_FORBIDDEN_OUTPUTS_CLEAN", forbidden_emitted == 0 and forbidden_flags == 0, f"forbidden_emitted={forbidden_emitted}; forbidden_flags={forbidden_flags}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(cost_hurdle: pd.DataFrame, labels: pd.DataFrame, controls: pd.DataFrame, materialization: pd.DataFrame, forbidden: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("phase225_cost_hurdle_rows", len(cost_hurdle), "Cost hurdle contract rows"),
            ("phase225_label_contract_rows", len(labels), "Cost-aware label contract rows"),
            ("phase225_negative_control_rows", len(controls), "Negative-control contract rows"),
            ("phase225_phase226_work_order_rows", len(materialization), "Phase226 work-order rows"),
            ("phase225_selected_route_id", SELECTED_ROUTE_ID, "Selected redesign route"),
            ("phase225_label_materialization_allowed_next", int(pd.to_numeric(materialization["label_materialization_allowed_next"], errors="coerce").fillna(0).sum()) if not materialization.empty else 0, "Label materialization allowed next"),
            ("phase225_model_fit_allowed_next", 0, "No model fit opened"),
            ("phase225_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase225_broader_replay_allowed_next", 0, "No broader replay opened"),
            ("phase225_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase225_test_rows_used", 0, "No sealed test rows used"),
            ("phase225_promotion_allowed", 0, "No promotion opened"),
            ("phase225_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase225_profitability_claim_allowed", 0, "No profitability claim is allowed"),
            ("phase225_forbidden_execution_rows", len(forbidden), "Forbidden execution rows"),
            ("phase225_gate_rows", len(gates), "Gates evaluated"),
            ("phase225_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase225_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase225_cost_aware_event_source_redesign_precommit_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase225 completed"),
            ("phase225_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase225_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase225 Cost-aware Event Source Redesign Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase225 freezes a cost-aware actionable event label/source redesign before any label materialization, model fit, replay, broader replay, or sealed test.",
        "The key move is economic: labels must clear the Zerodha cost/latency hurdle before they are allowed to become candidates.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase225_cost_aware_event_source_redesign_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase225(phase180_dir: Path, phase224_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase224 = read_csv(phase224_dir / "phase224_closure_or_redesign_acceptance_summary.csv")
    work_order_224 = read_csv(phase224_dir / "phase224_phase225_work_order.csv")
    cost_catalog = read_csv(phase180_dir / "phase180_zerodha_equity_cost_component_catalog.csv")
    latency_catalog = read_csv(phase180_dir / "phase180_latency_slippage_profile_catalog.csv")

    cost_hurdle = build_cost_hurdle_catalog(cost_catalog, latency_catalog)
    labels = build_label_contract()
    controls = build_negative_control_contract()
    materialization = build_materialization_contract(labels, controls)
    forbidden = build_forbidden_execution_ledger()
    gates = build_gates(phase224, work_order_224, cost_hurdle, labels, controls, materialization, forbidden)
    acceptance = build_acceptance(cost_hurdle, labels, controls, materialization, forbidden, gates)

    cost_hurdle.to_csv(output_dir / "phase225_cost_hurdle_contract.csv", index=False)
    labels.to_csv(output_dir / "phase225_label_contract.csv", index=False)
    controls.to_csv(output_dir / "phase225_negative_control_contract.csv", index=False)
    materialization.to_csv(output_dir / "phase225_phase226_work_order.csv", index=False)
    forbidden.to_csv(output_dir / "phase225_execution_forbidden_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase225_redesign_precommit_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase225_redesign_precommit_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Cost Hurdle Contract": cost_hurdle,
            "Label Contract": labels,
            "Negative Control Contract": controls,
            "Phase226 Work Order": materialization,
            "Forbidden Execution Ledger": forbidden,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase225_cost_aware_event_source_redesign_precommit_no_fit_no_replay_no_test",
        **reproducibility_fields(
            artifact_id="phase225_cost_aware_event_source_redesign_precommit",
            generated_utc=generated,
            inputs={
                "phase224_acceptance": str(phase224_dir / "phase224_closure_or_redesign_acceptance_summary.csv"),
                "phase224_work_order": str(phase224_dir / "phase224_phase225_work_order.csv"),
                "phase180_cost_catalog": str(phase180_dir / "phase180_zerodha_equity_cost_component_catalog.csv"),
                "phase180_latency_catalog": str(phase180_dir / "phase180_latency_slippage_profile_catalog.csv"),
            },
            parameters={
                "selected_route_id": SELECTED_ROUTE_ID,
                "label_horizons_sec": "5;15;30",
                "primary_net_floor_bps": "0",
                "primary_safety_margin_bps": "1",
                "allowed_splits": "train;validation",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "cost_hurdle": str(output_dir / "phase225_cost_hurdle_contract.csv"),
                "labels": str(output_dir / "phase225_label_contract.csv"),
                "controls": str(output_dir / "phase225_negative_control_contract.csv"),
                "work_order": str(output_dir / "phase225_phase226_work_order.csv"),
                "forbidden": str(output_dir / "phase225_execution_forbidden_ledger.csv"),
                "gates": str(output_dir / "phase225_redesign_precommit_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase225_redesign_precommit_acceptance_summary.csv"),
                "report": str(output_dir / "phase225_cost_aware_event_source_redesign_precommit_report.md"),
            },
            scenario_ids="phase225_cost_aware_event_source_redesign_precommit_no_fit_no_replay_no_test",
            cost_model_version="phase180_zerodha_equity_cost_component_catalog_bound",
            latency_model_version="phase180_latency_slippage_profile_catalog_bound",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase225_redesign_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Precommit a cost-aware event source redesign without materialization, fit, replay, or test.")
    parser.add_argument("--phase180-dir", type=Path, default=DEFAULT_PHASE180_DIR)
    parser.add_argument("--phase224-dir", type=Path, default=DEFAULT_PHASE224_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase225(args.phase180_dir, args.phase224_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
