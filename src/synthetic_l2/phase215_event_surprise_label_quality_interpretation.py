from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE214_DIR = Path("outputs/phase214")
DEFAULT_OUTPUT_DIR = Path("outputs/phase215")
FORBIDDEN_OUTPUTS = "model_fit;model_prediction;strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export"
NEXT_ACTION = "run_phase216_event_surprise_label_redesign_or_event_only_target_precommit_no_model_no_replay_no_test"


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


def build_quality_interpretation(balance: pd.DataFrame, quality: pd.DataFrame) -> pd.DataFrame:
    if balance.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    labels = [
        ("event_surprise_up_conditional_label", "mean_up_positive_rate"),
        ("event_surprise_down_conditional_label", "mean_down_positive_rate"),
        ("event_surprise_vol_expansion_conditional_label", "mean_vol_expansion_positive_rate"),
    ]
    sparse_by_split_horizon = {}
    if not quality.empty:
        q = quality.copy()
        q["sparse_event_surprise_partition"] = pd.to_numeric(q.get("sparse_event_surprise_partition", 0), errors="coerce").fillna(0).astype(int)
        for (split_role, horizon), part in q.groupby(["split_role", "horizon_sec"], sort=True):
            sparse_by_split_horizon[(str(split_role), as_int(horizon))] = int(part["sparse_event_surprise_partition"].sum())
    for record in balance.to_dict("records"):
        split_role = str(record.get("split_role", ""))
        horizon = as_int(record.get("horizon_sec", 0))
        total_rows = as_int(record.get("total_rows", 0))
        event_rows = as_int(record.get("event_surprise_rows", 0))
        event_share = (event_rows / total_rows) if total_rows else 0.0
        for label_name, rate_col in labels:
            positive_rate = float(record.get(rate_col, 0.0))
            balance_pass = 0.01 <= positive_rate <= 0.20
            event_density_pass = event_share >= 0.005
            train_validation_scope_pass = split_role in {"train", "validation"}
            sparse_partitions = sparse_by_split_horizon.get((split_role, horizon), 0)
            interpretation_pass = int(balance_pass and event_density_pass and train_validation_scope_pass)
            if interpretation_pass:
                verdict = "label_interpretable_for_event_only_precommit_not_model_fit"
            elif not balance_pass:
                verdict = "label_positive_rate_outside_event_surprise_interpretation_band"
            else:
                verdict = "event_surprise_density_too_sparse_for_model_fit_precommit"
            rows.append(
                {
                    "phase215_interpretation_id": f"P215_{split_role}_H{horizon}s_{label_name}",
                    "split_role": split_role,
                    "horizon_sec": horizon,
                    "label_name": label_name,
                    "total_rows": total_rows,
                    "event_surprise_rows": event_rows,
                    "event_surprise_share": event_share,
                    "positive_rate": positive_rate,
                    "sparse_event_surprise_partitions": sparse_partitions,
                    "event_density_pass": int(event_density_pass),
                    "positive_rate_interpretation_pass": int(balance_pass),
                    "train_validation_scope_pass": int(train_validation_scope_pass),
                    "interpretation_pass": interpretation_pass,
                    "verdict": verdict,
                    "model_fit_allowed_next": 0,
                    "strategy_replay_allowed": 0,
                    "test_replay_allowed_next": 0,
                    "profitability_claim_allowed": 0,
                }
            )
    return pd.DataFrame(rows)


def build_label_family_summary(interpretation: pd.DataFrame) -> pd.DataFrame:
    if interpretation.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for label_name, part in interpretation.groupby("label_name", sort=True):
        pass_rows = int(part["interpretation_pass"].astype(int).sum())
        min_event_share = float(pd.to_numeric(part["event_surprise_share"], errors="coerce").min())
        max_positive = float(pd.to_numeric(part["positive_rate"], errors="coerce").max())
        min_positive = float(pd.to_numeric(part["positive_rate"], errors="coerce").min())
        rows.append(
            {
                "phase215_label_family_summary_id": f"P215_FAMILY_{label_name}",
                "label_name": label_name,
                "interpreted_split_horizon_rows": len(part),
                "passing_interpretation_rows": pass_rows,
                "min_event_surprise_share": min_event_share,
                "min_positive_rate": min_positive,
                "max_positive_rate": max_positive,
                "family_verdict": "event_only_target_precommit_required_before_model_fit" if pass_rows > 0 else "label_redesign_required_before_model_fit",
                "model_fit_allowed_next": 0,
                "strategy_replay_allowed": 0,
            }
        )
    return pd.DataFrame(rows)


def build_decision_ledger(interpretation: pd.DataFrame, family: pd.DataFrame) -> pd.DataFrame:
    pass_rows = int(interpretation["interpretation_pass"].astype(int).sum()) if not interpretation.empty else 0
    family_pass = int(family["passing_interpretation_rows"].astype(int).gt(0).sum()) if not family.empty else 0
    return pd.DataFrame(
        [
            {
                "phase215_decision_id": "P215_EVENT_SURPRISE_LABEL_QUALITY_DECISION",
                "passing_interpretation_rows": pass_rows,
                "label_families_with_interpretable_rows": family_pass,
                "decision": "event_only_target_precommit_required_no_model_fit" if pass_rows > 0 else "label_redesign_required_no_model_fit",
                "rationale": "Phase214 labels are materialized, but positive rates are sparse and must be interpreted as event-only targets before any model-fit precommit.",
                "model_fit_allowed_next": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "profitability_claim_allowed": 0,
            }
        ]
    )


def build_phase216_work_order(decision: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "phase216_work_order_id": "P216_EVENT_ONLY_TARGET_OR_LABEL_REDESIGN_PRECOMMIT",
                "decision": decision["decision"].iloc[0] if not decision.empty else "label_redesign_required_no_model_fit",
                "required_action": "Precommit whether Phase214 labels should be narrowed to event-only rows or redesigned for better class balance before any model fit.",
                "allowed_next_scope": "precommit_only_no_model_no_replay_no_test",
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
                "emitted_in_phase215": 0,
                "allowed_in_phase215": 0,
                "rationale": "Phase215 interprets label quality only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact.",
            }
            for item in FORBIDDEN_OUTPUTS.split(";")
        ]
    )


def build_gates(phase214: pd.DataFrame, interpretation: pd.DataFrame, family: pd.DataFrame, decision: pd.DataFrame, work_order: pd.DataFrame, forbidden: pd.DataFrame) -> pd.DataFrame:
    phase214_complete = as_int(metric_value(phase214, "phase214_event_surprise_label_materialization_complete", 0))
    sealed_used = as_int(metric_value(phase214, "phase214_sealed_test_rows_used", 0))
    replay_flags = 0
    for frame in [interpretation, family, decision, work_order]:
        for col in ["model_fit_allowed_next", "strategy_replay_allowed", "test_replay_allowed_next", "promotion_allowed", "paper_or_live_acceptance_allowed", "profitability_claim_allowed"]:
            if not frame.empty and col in frame.columns:
                replay_flags += int(pd.to_numeric(frame[col], errors="coerce").fillna(0).sum())
    forbidden_emitted = int(forbidden["emitted_in_phase215"].astype(int).sum()) if not forbidden.empty else 1
    return pd.DataFrame(
        [
            ("P215_PHASE214_COMPLETE", phase214_complete == 1, f"phase214_complete={phase214_complete}", "hard"),
            ("P215_SEALED_TEST_STILL_UNUSED", sealed_used == 0, f"sealed_test_rows_used={sealed_used}", "hard"),
            ("P215_INTERPRETATION_ROWS_RECORDED", len(interpretation) == 24, f"interpretation_rows={len(interpretation)}", "hard"),
            ("P215_LABEL_FAMILY_SUMMARY_RECORDED", len(family) == 3, f"family_rows={len(family)}", "hard"),
            ("P215_DECISION_LEDGER_RECORDED", len(decision) == 1, f"decision_rows={len(decision)}", "hard"),
            ("P215_PHASE216_WORK_ORDER_RECORDED", len(work_order) == 1, f"work_order_rows={len(work_order)}", "hard"),
            ("P215_FORBIDDEN_OUTPUTS_CLEAN", forbidden_emitted == 0 and replay_flags == 0, f"forbidden_emitted={forbidden_emitted}; replay_flags={replay_flags}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(interpretation: pd.DataFrame, family: pd.DataFrame, decision: pd.DataFrame, work_order: pd.DataFrame, forbidden: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    pass_rows = int(interpretation["interpretation_pass"].astype(int).sum()) if not interpretation.empty else 0
    return pd.DataFrame(
        [
            ("phase215_interpretation_rows", len(interpretation), "Split/horizon/label interpretation rows"),
            ("phase215_passing_interpretation_rows", pass_rows, "Rows passing event-only interpretation screen"),
            ("phase215_label_family_summary_rows", len(family), "Label-family summary rows"),
            ("phase215_label_families_with_interpretable_rows", int(family["passing_interpretation_rows"].astype(int).gt(0).sum()) if not family.empty else 0, "Label families with at least one interpretable row"),
            ("phase215_decision_rows", len(decision), "Decision ledger rows"),
            ("phase215_phase216_work_order_rows", len(work_order), "Phase216 work-order rows"),
            ("phase215_forbidden_execution_rows", len(forbidden), "Forbidden execution rows"),
            ("phase215_gate_rows", len(gates), "Gates evaluated"),
            ("phase215_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase215_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase215_event_surprise_label_quality_interpretation_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase215 completed"),
            ("phase215_model_fit_allowed_next", 0, "No model fit opened"),
            ("phase215_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase215_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase215_promotion_allowed", 0, "No promotion opened"),
            ("phase215_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase215_profitability_claim_allowed", 0, "No profitability claim is allowed"),
            ("phase215_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase215_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase215 Event-surprise Label Quality Interpretation",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase215 interprets Phase214 event-surprise label balance and sparsity before any model-fit precommit.",
        "It keeps model fitting, replay, sealed test, promotion, paper/live acceptance, and profitability claims closed.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase215_event_surprise_label_quality_interpretation_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase215(phase214_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase214 = read_csv(phase214_dir / "phase214_event_surprise_label_acceptance_summary.csv")
    balance = read_csv(phase214_dir / "phase214_split_balance_summary.csv")
    quality = read_csv(phase214_dir / "phase214_label_partition_quality.csv")
    interpretation = build_quality_interpretation(balance, quality)
    family = build_label_family_summary(interpretation)
    decision = build_decision_ledger(interpretation, family)
    work_order = build_phase216_work_order(decision)
    forbidden = build_forbidden_execution_ledger()
    gates = build_gates(phase214, interpretation, family, decision, work_order, forbidden)
    acceptance = build_acceptance(interpretation, family, decision, work_order, forbidden, gates)

    interpretation.to_csv(output_dir / "phase215_label_quality_interpretation.csv", index=False)
    family.to_csv(output_dir / "phase215_label_family_summary.csv", index=False)
    decision.to_csv(output_dir / "phase215_decision_ledger.csv", index=False)
    work_order.to_csv(output_dir / "phase215_phase216_work_order.csv", index=False)
    forbidden.to_csv(output_dir / "phase215_execution_forbidden_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase215_label_quality_interpretation_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase215_label_quality_interpretation_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Label Quality Interpretation": interpretation,
            "Label Family Summary": family,
            "Decision Ledger": decision,
            "Phase216 Work Order": work_order,
            "Forbidden Execution Ledger": forbidden,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase215_event_surprise_label_quality_interpretation_no_model_no_replay_no_test",
        **reproducibility_fields(
            artifact_id="phase215_event_surprise_label_quality_interpretation",
            generated_utc=generated,
            inputs={
                "phase214_acceptance": str(phase214_dir / "phase214_event_surprise_label_acceptance_summary.csv"),
                "phase214_balance": str(phase214_dir / "phase214_split_balance_summary.csv"),
                "phase214_quality": str(phase214_dir / "phase214_label_partition_quality.csv"),
            },
            parameters={
                "event_surprise_share_minimum": "0.005",
                "event_only_positive_rate_band": "0.01_to_0.20",
                "model_fit_allowed": "0",
                "strategy_replay_allowed": "0",
                "test_replay_allowed_next": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "interpretation": str(output_dir / "phase215_label_quality_interpretation.csv"),
                "family": str(output_dir / "phase215_label_family_summary.csv"),
                "decision": str(output_dir / "phase215_decision_ledger.csv"),
                "work_order": str(output_dir / "phase215_phase216_work_order.csv"),
                "forbidden": str(output_dir / "phase215_execution_forbidden_ledger.csv"),
                "gates": str(output_dir / "phase215_label_quality_interpretation_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase215_label_quality_interpretation_acceptance_summary.csv"),
                "report": str(output_dir / "phase215_event_surprise_label_quality_interpretation_report.md"),
            },
            scenario_ids="phase215_event_surprise_label_quality_interpretation_no_model_no_replay_no_test",
            cost_model_version="not_applicable_no_replay",
            latency_model_version="not_applicable_no_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase215_label_quality_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase215 label-quality interpretation without model/replay/test.")
    parser.add_argument("--phase214-dir", type=Path, default=DEFAULT_PHASE214_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase215(args.phase214_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
