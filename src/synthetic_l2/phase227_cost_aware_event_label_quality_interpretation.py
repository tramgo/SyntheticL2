from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE226_DIR = Path("outputs/phase226")
DEFAULT_OUTPUT_DIR = Path("outputs/phase227")
MIN_QUALITY_PASS_SPLITS_FOR_FIT_PRECOMMIT = 4
MIN_ACTIONABLE_ROWS_FOR_FIT_PRECOMMIT = 4_000
FORBIDDEN_OUTPUTS = "label_materialization;feature_materialization;model_fit;model_prediction;strategy_replay;broader_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export"
NEXT_ACTION = "run_phase228_cost_aware_label_redesign_closure_or_relaxation_precommit_no_fit_no_replay_no_test"


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


def build_quality_interpretation(split_summary: pd.DataFrame) -> pd.DataFrame:
    if split_summary.empty:
        return pd.DataFrame()
    frame = split_summary.copy()
    numeric_cols = [
        "horizon_sec",
        "partitions",
        "rows",
        "cost_aware_actionable_rows",
        "symbols",
        "trade_dates",
        "passes_min_event_count",
        "passes_min_symbol_count",
        "passes_min_trade_date_count",
        "quality_gate_pass",
        "test_rows_used",
    ]
    for col in numeric_cols:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0)
    frame["actionable_rate"] = frame["cost_aware_actionable_rows"] / frame["rows"].replace(0, pd.NA)
    frame["actionable_rate"] = pd.to_numeric(frame["actionable_rate"], errors="coerce").fillna(0.0)
    frame["fit_precommit_candidate"] = 0
    frame["model_fit_allowed_next"] = 0
    frame["strategy_replay_allowed"] = 0
    frame["test_replay_allowed_next"] = 0
    frame["promotion_allowed"] = 0
    frame["paper_or_live_acceptance_allowed"] = 0
    frame["profitability_claim_allowed"] = 0
    frame["failure_reason"] = frame.apply(
        lambda r: "minimum_actionable_event_count_failed"
        if int(r["passes_min_event_count"]) == 0
        else "minimum_symbol_or_date_coverage_failed"
        if int(r["passes_min_symbol_count"]) == 0 or int(r["passes_min_trade_date_count"]) == 0
        else "",
        axis=1,
    )
    frame["interpretation_verdict"] = frame.apply(
        lambda r: "insufficient_cost_aware_label_support_for_fit_precommit" if int(r["quality_gate_pass"]) == 0 else "label_quality_candidate_requires_new_precommit",
        axis=1,
    )
    return frame.sort_values(["quality_gate_pass", "cost_aware_actionable_rows"], ascending=[False, False]).reset_index(drop=True)


def build_horizon_interpretation(quality: pd.DataFrame, availability: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    available = availability.copy() if not availability.empty else pd.DataFrame()
    for horizon, part in quality.groupby("horizon_sec", sort=True) if not quality.empty else []:
        rows.append(
            {
                "horizon_sec": int(horizon),
                "materialization_available": 1,
                "split_rows": len(part),
                "quality_pass_rows": int(pd.to_numeric(part["quality_gate_pass"], errors="coerce").fillna(0).sum()),
                "total_rows": int(pd.to_numeric(part["rows"], errors="coerce").fillna(0).sum()),
                "cost_aware_actionable_rows": int(pd.to_numeric(part["cost_aware_actionable_rows"], errors="coerce").fillna(0).sum()),
                "max_actionable_rate": float(pd.to_numeric(part["actionable_rate"], errors="coerce").fillna(0.0).max()),
                "horizon_fit_precommit_allowed": 0,
                "horizon_verdict": "insufficient_split_quality_for_model_fit",
            }
        )
    if not available.empty:
        materialized = {int(r["horizon_sec"]) for r in rows}
        for record in available.to_dict("records"):
            horizon = as_int(record.get("horizon_sec", 0))
            if horizon in materialized:
                continue
            rows.append(
                {
                    "horizon_sec": horizon,
                    "materialization_available": as_int(record.get("materialization_available", 0)),
                    "split_rows": 0,
                    "quality_pass_rows": 0,
                    "total_rows": 0,
                    "cost_aware_actionable_rows": 0,
                    "max_actionable_rate": 0.0,
                    "horizon_fit_precommit_allowed": 0,
                    "horizon_verdict": "contracted_horizon_unavailable_in_current_inputs",
                }
            )
    return pd.DataFrame(rows).sort_values("horizon_sec").reset_index(drop=True) if rows else pd.DataFrame()


def build_failure_mode_ledger(acceptance: pd.DataFrame, quality: pd.DataFrame, availability: pd.DataFrame) -> pd.DataFrame:
    actionable = as_int(metric_value(acceptance, "phase226_cost_aware_actionable_rows", 0))
    quality_pass = as_int(metric_value(acceptance, "phase226_quality_pass_rows", 0))
    total = as_int(metric_value(acceptance, "phase226_total_label_rows", 0))
    blocked_horizons = as_int(metric_value(acceptance, "phase226_blocked_horizon_rows", 0))
    train_dates = 0
    validation_dates = 0
    if not quality.empty and "split_role" in quality.columns:
        train = quality[quality["split_role"].astype(str).eq("train")]
        validation = quality[quality["split_role"].astype(str).eq("validation")]
        train_dates = int(pd.to_numeric(train["trade_dates"], errors="coerce").fillna(0).max()) if not train.empty else 0
        validation_dates = int(pd.to_numeric(validation["trade_dates"], errors="coerce").fillna(0).max()) if not validation.empty else 0
    return pd.DataFrame(
        [
            {
                "phase227_failure_mode_id": "P227_ACTIONABLE_EVENT_COUNT_TOO_LOW",
                "failure_mode": "cost_aware_actionable_labels_are_too_sparse_for_fit_precommit",
                "affected_rows": len(quality),
                "evidence": f"actionable_rows={actionable}; required={MIN_ACTIONABLE_ROWS_FOR_FIT_PRECOMMIT}; quality_pass_rows={quality_pass}",
                "redesign_implication": "Relaxing thresholds post hoc is forbidden; next phase must precommit a materially different label/hurdle design or close this branch.",
                "model_fit_allowed_next": 0,
            },
            {
                "phase227_failure_mode_id": "P227_VALIDATION_DATE_BREADTH_TOO_LOW",
                "failure_mode": "validation_split_has_insufficient_trade_date_breadth_for_quality_gate",
                "affected_rows": int((quality["split_role"].astype(str).eq("validation")).sum()) if not quality.empty else 0,
                "evidence": f"train_max_dates={train_dates}; validation_max_dates={validation_dates}",
                "redesign_implication": "Broader validation-date materialization or new source coverage is required before fit/replay can be considered.",
                "model_fit_allowed_next": 0,
            },
            {
                "phase227_failure_mode_id": "P227_CONTRACTED_30S_HORIZON_UNAVAILABLE",
                "failure_mode": "phase225_contracted_30s_horizon_is_unavailable_in_current_phase181_phase214_inputs",
                "affected_rows": blocked_horizons,
                "evidence": "30s unavailable; 60s was not substituted",
                "redesign_implication": "Either precommit available horizons only or materialize a genuine 30s source before using 30s labels.",
                "model_fit_allowed_next": 0,
            },
            {
                "phase227_failure_mode_id": "P227_COST_HURDLE_WALL_TOO_STRICT_FOR_CURRENT_EVENT_SOURCE",
                "failure_mode": "zerodha_cost_hurdle_filters_most_event_surprise_rows_to_neutral",
                "affected_rows": total,
                "evidence": f"total_event_rows={total}; actionable_rows={actionable}",
                "redesign_implication": "Future source must either find larger expected moves ex ante or change execution premise with an explicit no-impossible-fills contract.",
                "model_fit_allowed_next": 0,
            },
        ]
    )


def build_phase228_work_order(failure: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "phase228_work_order_id": "P228_COST_AWARE_LABEL_REDESIGN_CLOSURE_OR_RELAXATION_PRECOMMIT",
                "work_order": "Decide whether to close the cost-aware event label branch or precommit a materially different relaxation/source expansion without post hoc threshold widening.",
                "failure_mode_rows": len(failure),
                "recommended_decision": "close_or_precommit_material_redesign_before_any_fit",
                "allowed_next_scope": "closure_or_material_redesign_precommit_only_no_fit_no_replay_no_test",
                "threshold_widening_allowed": 0,
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
                "emitted_in_phase227": 0,
                "allowed_in_phase227": 0,
                "rationale": "Phase227 interprets aggregate label quality only and emits no materialization, fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, threshold-widening, row-level export, or profitability artifact.",
            }
            for item in FORBIDDEN_OUTPUTS.split(";")
        ]
    )


def build_gates(phase226: pd.DataFrame, quality: pd.DataFrame, horizon: pd.DataFrame, failure: pd.DataFrame, work_order: pd.DataFrame, forbidden: pd.DataFrame) -> pd.DataFrame:
    phase226_complete = as_int(metric_value(phase226, "phase226_cost_aware_event_label_materialization_dry_run_complete", 0))
    actionable_rows = as_int(metric_value(phase226, "phase226_cost_aware_actionable_rows", 0))
    quality_pass_rows = as_int(metric_value(phase226, "phase226_quality_pass_rows", 0))
    test_rows_used = as_int(metric_value(phase226, "phase226_test_rows_used", 0))
    fit_candidates = int(pd.to_numeric(quality["fit_precommit_candidate"], errors="coerce").fillna(0).sum()) if not quality.empty else 0
    forbidden_emitted = int(pd.to_numeric(forbidden["emitted_in_phase227"], errors="coerce").fillna(0).sum()) if not forbidden.empty else 1
    forbidden_flags = 0
    for frame in [quality, horizon, failure, work_order]:
        for col in ["model_fit_allowed_next", "horizon_fit_precommit_allowed", "strategy_replay_allowed", "broader_replay_allowed_next", "test_replay_allowed_next", "promotion_allowed", "paper_or_live_acceptance_allowed", "profitability_claim_allowed", "threshold_widening_allowed"]:
            if not frame.empty and col in frame.columns:
                forbidden_flags += int(pd.to_numeric(frame[col], errors="coerce").fillna(0).sum())
    return pd.DataFrame(
        [
            ("P227_PHASE226_COMPLETE", phase226_complete == 1, f"phase226_complete={phase226_complete}", "hard"),
            ("P227_QUALITY_INTERPRETATION_RECORDED", len(quality) == 4, f"quality_rows={len(quality)}", "hard"),
            ("P227_SPARSE_LABEL_FAILURE_RECORDED", actionable_rows > 0 and quality_pass_rows == 0 and fit_candidates == 0, f"actionable_rows={actionable_rows}; quality_pass_rows={quality_pass_rows}; fit_candidates={fit_candidates}", "hard"),
            ("P227_HORIZON_INTERPRETATION_RECORDED", len(horizon) == 3, f"horizon_rows={len(horizon)}", "hard"),
            ("P227_PHASE228_WORK_ORDER_RECORDED", len(work_order) == 1, f"work_order_rows={len(work_order)}", "hard"),
            ("P227_TEST_ROWS_UNTOUCHED", test_rows_used == 0, f"test_rows_used={test_rows_used}", "hard"),
            ("P227_FORBIDDEN_OUTPUTS_CLEAN", forbidden_emitted == 0 and forbidden_flags == 0, f"forbidden_emitted={forbidden_emitted}; forbidden_flags={forbidden_flags}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(phase226: pd.DataFrame, quality: pd.DataFrame, horizon: pd.DataFrame, failure: pd.DataFrame, work_order: pd.DataFrame, forbidden: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("phase227_quality_interpretation_rows", len(quality), "Split-level quality interpretation rows"),
            ("phase227_horizon_interpretation_rows", len(horizon), "Horizon interpretation rows"),
            ("phase227_failure_mode_rows", len(failure), "Failure-mode rows"),
            ("phase227_phase228_work_order_rows", len(work_order), "Phase228 work-order rows"),
            ("phase227_actionable_rows", as_int(metric_value(phase226, "phase226_cost_aware_actionable_rows", 0)), "Phase226 actionable rows interpreted"),
            ("phase227_quality_pass_rows", as_int(metric_value(phase226, "phase226_quality_pass_rows", 0)), "Phase226 quality pass rows interpreted"),
            ("phase227_fit_precommit_candidate_rows", int(pd.to_numeric(quality["fit_precommit_candidate"], errors="coerce").fillna(0).sum()) if not quality.empty else 0, "Rows eligible for fit precommit"),
            ("phase227_model_fit_allowed_next", 0, "No model fit opened"),
            ("phase227_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase227_broader_replay_allowed_next", 0, "No broader replay opened"),
            ("phase227_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase227_test_rows_used", 0, "No sealed test rows used"),
            ("phase227_promotion_allowed", 0, "No promotion opened"),
            ("phase227_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase227_profitability_claim_allowed", 0, "No profitability claim is allowed"),
            ("phase227_forbidden_execution_rows", len(forbidden), "Forbidden execution rows"),
            ("phase227_gate_rows", len(gates), "Gates evaluated"),
            ("phase227_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase227_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase227_cost_aware_event_label_quality_interpretation_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase227 completed"),
            ("phase227_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase227_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase227 Cost-aware Event Label Quality Interpretation",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase227 interprets Phase226 cost-aware label quality and decides whether model-fit precommit remains closed.",
        "It emits no new labels, model fit, replay, sealed test, promotion, paper/live, or profitability artifact.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase227_cost_aware_event_label_quality_interpretation_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase227(phase226_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase226 = read_csv(phase226_dir / "phase226_label_materialization_acceptance_summary.csv")
    split_summary = read_csv(phase226_dir / "phase226_label_quality_split_summary.csv")
    availability = read_csv(phase226_dir / "phase226_horizon_availability_ledger.csv")
    quality = build_quality_interpretation(split_summary)
    horizon = build_horizon_interpretation(quality, availability)
    failure = build_failure_mode_ledger(phase226, quality, availability)
    work_order = build_phase228_work_order(failure)
    forbidden = build_forbidden_execution_ledger()
    gates = build_gates(phase226, quality, horizon, failure, work_order, forbidden)
    acceptance = build_acceptance(phase226, quality, horizon, failure, work_order, forbidden, gates)

    quality.to_csv(output_dir / "phase227_quality_interpretation.csv", index=False)
    horizon.to_csv(output_dir / "phase227_horizon_interpretation.csv", index=False)
    failure.to_csv(output_dir / "phase227_failure_mode_ledger.csv", index=False)
    work_order.to_csv(output_dir / "phase227_phase228_work_order.csv", index=False)
    forbidden.to_csv(output_dir / "phase227_execution_forbidden_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase227_quality_interpretation_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase227_quality_interpretation_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Quality Interpretation": quality,
            "Horizon Interpretation": horizon,
            "Failure Mode Ledger": failure,
            "Phase228 Work Order": work_order,
            "Forbidden Execution Ledger": forbidden,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase227_cost_aware_event_label_quality_interpretation_no_fit_no_replay_no_test",
        **reproducibility_fields(
            artifact_id="phase227_cost_aware_event_label_quality_interpretation",
            generated_utc=generated,
            inputs={
                "phase226_acceptance": str(phase226_dir / "phase226_label_materialization_acceptance_summary.csv"),
                "phase226_split_summary": str(phase226_dir / "phase226_label_quality_split_summary.csv"),
                "phase226_availability": str(phase226_dir / "phase226_horizon_availability_ledger.csv"),
            },
            parameters={
                "min_quality_pass_splits_for_fit_precommit": str(MIN_QUALITY_PASS_SPLITS_FOR_FIT_PRECOMMIT),
                "min_actionable_rows_for_fit_precommit": str(MIN_ACTIONABLE_ROWS_FOR_FIT_PRECOMMIT),
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "quality": str(output_dir / "phase227_quality_interpretation.csv"),
                "horizon": str(output_dir / "phase227_horizon_interpretation.csv"),
                "failure": str(output_dir / "phase227_failure_mode_ledger.csv"),
                "work_order": str(output_dir / "phase227_phase228_work_order.csv"),
                "forbidden": str(output_dir / "phase227_execution_forbidden_ledger.csv"),
                "gates": str(output_dir / "phase227_quality_interpretation_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase227_quality_interpretation_acceptance_summary.csv"),
                "report": str(output_dir / "phase227_cost_aware_event_label_quality_interpretation_report.md"),
            },
            scenario_ids="phase227_cost_aware_event_label_quality_interpretation_no_fit_no_replay_no_test",
            cost_model_version="phase180_zerodha_equity_cost_component_catalog_bound",
            latency_model_version="phase180_latency_slippage_profile_catalog_bound",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase227_quality_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Interpret Phase226 cost-aware label quality without fit, replay, or test.")
    parser.add_argument("--phase226-dir", type=Path, default=DEFAULT_PHASE226_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase227(args.phase226_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
