from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE211_DIR = Path("outputs/phase211")
DEFAULT_OUTPUT_DIR = Path("outputs/phase212")
FORBIDDEN_OUTPUTS = "model_fit;model_prediction;strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export"
NEXT_ACTION = "run_phase213_material_new_model_source_precommit_no_replay_no_test"


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


def build_family_closure_ledger(family_summary: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for record in family_summary.to_dict("records"):
        pass_rows = as_int(record.get("passing_interpretation_rows", 0))
        rows.append(
            {
                "phase212_closure_id": str(record.get("phase211_family_summary_id", "")).replace("P211_FAMILY_", "P212_CLOSE_"),
                "phase209_model_spec_id": record.get("phase209_model_spec_id", ""),
                "interpreted_horizon_rows": as_int(record.get("interpreted_horizon_rows", 0)),
                "passing_interpretation_rows": pass_rows,
                "best_mse_improvement_pct_vs_control": record.get("best_mse_improvement_pct_vs_control", ""),
                "best_abs_validation_correlation": record.get("best_abs_validation_correlation", ""),
                "best_binary_accuracy_lift_vs_control": record.get("best_binary_accuracy_lift_vs_control", ""),
                "current_family_closed_for_replay": int(pass_rows == 0),
                "current_family_reuse_without_redesign_allowed": 0,
                "closure_reason": "control_aware_validation_screen_failed_no_replay_candidate" if pass_rows == 0 else "diagnostic_survivor_requires_new_precommit_before_replay",
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "profitability_claim_allowed": 0,
            }
        )
    return pd.DataFrame(rows)


def build_failure_mode_ledger(interpretation: pd.DataFrame) -> pd.DataFrame:
    if interpretation.empty:
        return pd.DataFrame()
    failure = interpretation.copy()
    failure["mse_improvement_pct_vs_control"] = pd.to_numeric(failure["mse_improvement_pct_vs_control"], errors="coerce").fillna(0.0)
    failure["validation_correlation"] = pd.to_numeric(failure["validation_correlation"], errors="coerce").fillna(0.0)
    failure["binary_accuracy_lift_vs_control"] = pd.to_numeric(failure["binary_accuracy_lift_vs_control"], errors="coerce").fillna(0.0)
    rows = [
        {
            "phase212_failure_mode_id": "P212_CONTROL_LIKE_MSE",
            "failure_mode": "validation_mse_not_materially_better_than_shuffled_target_control",
            "affected_rows": int(failure["mse_improvement_pass"].astype(int).eq(0).sum()) if "mse_improvement_pass" in failure.columns else len(failure),
            "worst_or_best_evidence": f"best_mse_improvement_pct={failure['mse_improvement_pct_vs_control'].max()}",
            "redesign_implication": "Future source must create materially stronger out-of-sample target separation before model/replay precommit.",
            "strategy_replay_allowed": 0,
        },
        {
            "phase212_failure_mode_id": "P212_WEAK_VALIDATION_CORRELATION",
            "failure_mode": "absolute_validation_correlation_too_weak_or_not_jointly_supported",
            "affected_rows": int(failure["correlation_pass"].astype(int).eq(0).sum()) if "correlation_pass" in failure.columns else len(failure),
            "worst_or_best_evidence": f"best_abs_validation_correlation={failure['validation_correlation'].abs().max()}",
            "redesign_implication": "Future source should test regime/state segmentation or materially different labels before any new fit.",
            "strategy_replay_allowed": 0,
        },
        {
            "phase212_failure_mode_id": "P212_BASE_RATE_ACCURACY",
            "failure_mode": "binary_accuracy_base_rate_or_control_like",
            "affected_rows": int(failure["binary_accuracy_lift_pass"].astype(int).eq(0).sum()) if "binary_accuracy_lift_pass" in failure.columns else len(failure),
            "worst_or_best_evidence": f"best_binary_accuracy_lift={failure['binary_accuracy_lift_vs_control'].max()}",
            "redesign_implication": "Future binary classification must use balanced lift/control-aware metrics, not headline accuracy.",
            "strategy_replay_allowed": 0,
        },
    ]
    return pd.DataFrame(rows)


def build_redesign_precommit_catalog() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "phase212_redesign_id": "P212_EVENT_SURPRISE_CONDITIONAL_LABEL_SOURCE",
                "redesign_theme": "material_new_label_source",
                "precommit_action": "Define labels around receive-event surprise conditional on symbol/date liquidity regime, not raw next-bucket direction.",
                "why_materially_different": "Moves from broad base-rate labels to conditional event-surprise labels designed to defeat shuffled-target/base-rate controls.",
                "required_before_model_fit": "new_label_contract;balanced_control_metrics;train_validation_only_materialization",
                "phase213_candidate": 1,
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            },
            {
                "phase212_redesign_id": "P212_REGIME_STRATIFIED_FEATURE_SOURCE",
                "redesign_theme": "material_new_feature_source",
                "precommit_action": "Precommit regime-stratified receive-flow features split by spread, liquidity, churn, and opening/steady-state context.",
                "why_materially_different": "Tests whether weak global correlations hide local regime effects without selecting on sealed test outcomes.",
                "required_before_model_fit": "regime_partition_contract;minimum_rows_per_regime;negative_control_per_regime",
                "phase213_candidate": 1,
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            },
            {
                "phase212_redesign_id": "P212_CROSS_SECTIONAL_RELATIVE_FLOW_SOURCE",
                "redesign_theme": "material_new_cross_sectional_source",
                "precommit_action": "Define cross-sectional relative receive-flow ranks and market-wide shock residuals with target-symbol exclusion.",
                "why_materially_different": "Moves from absolute per-symbol flow to relative/residual context while preserving target-symbol leakage controls.",
                "required_before_model_fit": "target_symbol_exclusion_proof;market_shock_residual_contract;shuffled_symbol_control",
                "phase213_candidate": 1,
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            },
        ]
    )


def build_action_queue(redesign: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for idx, record in enumerate(redesign.to_dict("records"), start=1):
        rows.append(
            {
                "phase212_action_rank": idx,
                "phase212_redesign_id": record.get("phase212_redesign_id", ""),
                "next_phase": "Phase213",
                "required_action": record.get("precommit_action", ""),
                "acceptance_boundary": "precommit_only_no_model_fit_no_replay_no_test",
                "blocking_until_done": 1,
                "strategy_replay_allowed": 0,
                "promotion_allowed": 0,
            }
        )
    return pd.DataFrame(rows)


def build_forbidden_execution_ledger() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "forbidden_output": item,
                "emitted_in_phase212": 0,
                "allowed_in_phase212": 0,
                "rationale": "Phase212 closes/reprecommits research direction only; it emits no fit, replay, prediction, P&L, promotion, paper/live, or threshold-widening artifact.",
            }
            for item in FORBIDDEN_OUTPUTS.split(";")
        ]
    )


def build_gates(phase211: pd.DataFrame, closure: pd.DataFrame, failure: pd.DataFrame, redesign: pd.DataFrame, action: pd.DataFrame, forbidden: pd.DataFrame) -> pd.DataFrame:
    phase211_complete = as_int(metric_value(phase211, "phase211_model_fit_validation_interpretation_complete", 0))
    passing_rows = as_int(metric_value(phase211, "phase211_passing_interpretation_rows", 0))
    closed_rows = int(closure["current_family_closed_for_replay"].astype(int).sum()) if not closure.empty else 0
    reuse_allowed = int(closure["current_family_reuse_without_redesign_allowed"].astype(int).sum()) if not closure.empty else 1
    replay_flags = 0
    for frame in [closure, failure, redesign, action]:
        for col in ["strategy_replay_allowed", "test_replay_allowed_next", "promotion_allowed", "paper_or_live_acceptance_allowed", "profitability_claim_allowed", "model_fit_allowed_now"]:
            if not frame.empty and col in frame.columns:
                replay_flags += int(pd.to_numeric(frame[col], errors="coerce").fillna(0).sum())
    forbidden_emitted = int(forbidden["emitted_in_phase212"].astype(int).sum()) if not forbidden.empty else 1
    return pd.DataFrame(
        [
            ("P212_PHASE211_COMPLETE", phase211_complete == 1, f"phase211_complete={phase211_complete}", "hard"),
            ("P212_NO_PHASE211_PASSING_ROWS", passing_rows == 0, f"passing_rows={passing_rows}", "hard"),
            ("P212_CURRENT_FAMILIES_CLOSED_FOR_REPLAY", len(closure) == 3 and closed_rows == 3 and reuse_allowed == 0, f"closure_rows={len(closure)}; closed_rows={closed_rows}; reuse_allowed={reuse_allowed}", "hard"),
            ("P212_FAILURE_MODES_RECORDED", len(failure) == 3, f"failure_mode_rows={len(failure)}", "hard"),
            ("P212_MATERIAL_REDESIGN_QUEUE_RECORDED", len(redesign) == 3 and int(redesign['phase213_candidate'].astype(int).sum()) == 3, f"redesign_rows={len(redesign)}", "hard"),
            ("P212_ACTION_QUEUE_RECORDED", len(action) == 3 and action["blocking_until_done"].astype(int).eq(1).all(), f"action_rows={len(action)}", "hard"),
            ("P212_FORBIDDEN_OUTPUTS_CLEAN", forbidden_emitted == 0 and replay_flags == 0, f"forbidden_emitted={forbidden_emitted}; replay_flags={replay_flags}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(closure: pd.DataFrame, failure: pd.DataFrame, redesign: pd.DataFrame, action: pd.DataFrame, forbidden: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("phase212_family_closure_rows", len(closure), "Model-family closure rows"),
            ("phase212_families_closed_for_replay", int(closure["current_family_closed_for_replay"].astype(int).sum()) if not closure.empty else 0, "Families closed for replay"),
            ("phase212_reuse_without_redesign_allowed", int(closure["current_family_reuse_without_redesign_allowed"].astype(int).sum()) if not closure.empty else 0, "Reuse without redesign allowed rows"),
            ("phase212_failure_mode_rows", len(failure), "Failure-mode rows"),
            ("phase212_redesign_precommit_rows", len(redesign), "Material redesign precommit rows"),
            ("phase212_action_queue_rows", len(action), "Phase213 action queue rows"),
            ("phase212_forbidden_execution_rows", len(forbidden), "Forbidden execution rows"),
            ("phase212_gate_rows", len(gates), "Gates evaluated"),
            ("phase212_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase212_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase212_model_family_closure_or_redesign_precommit_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase212 completed"),
            ("phase212_candidate_opened_for_replay", 0, "No candidate opened for replay"),
            ("phase212_model_fit_allowed_next", 0, "No model fit opened by Phase212"),
            ("phase212_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase212_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase212_promotion_allowed", 0, "No promotion opened"),
            ("phase212_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase212_profitability_claim_allowed", 0, "No profitability claim is allowed"),
            ("phase212_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase212_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase212 Model-family Closure or Redesign Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase212 closes the current Phase209/210 model-family set for replay after Phase211 found no control-aware survivor.",
        "It records failure modes and a material redesign queue for Phase213 without fitting models, running replay, touching sealed test, or making profitability claims.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase212_model_family_closure_or_redesign_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase212(phase211_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase211 = read_csv(phase211_dir / "phase211_model_fit_validation_interpretation_acceptance_summary.csv")
    family_summary = read_csv(phase211_dir / "phase211_family_interpretation_summary.csv")
    interpretation = read_csv(phase211_dir / "phase211_validation_interpretation.csv")
    closure = build_family_closure_ledger(family_summary)
    failure = build_failure_mode_ledger(interpretation)
    redesign = build_redesign_precommit_catalog()
    action = build_action_queue(redesign)
    forbidden = build_forbidden_execution_ledger()
    gates = build_gates(phase211, closure, failure, redesign, action, forbidden)
    acceptance = build_acceptance(closure, failure, redesign, action, forbidden, gates)

    closure.to_csv(output_dir / "phase212_model_family_closure_ledger.csv", index=False)
    failure.to_csv(output_dir / "phase212_failure_mode_ledger.csv", index=False)
    redesign.to_csv(output_dir / "phase212_material_redesign_precommit_catalog.csv", index=False)
    action.to_csv(output_dir / "phase212_phase213_action_queue.csv", index=False)
    forbidden.to_csv(output_dir / "phase212_execution_forbidden_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase212_model_family_closure_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase212_model_family_closure_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Model-family Closure Ledger": closure,
            "Failure Mode Ledger": failure,
            "Material Redesign Precommit Catalog": redesign,
            "Phase213 Action Queue": action,
            "Forbidden Execution Ledger": forbidden,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase212_model_family_closure_or_redesign_precommit_no_replay_no_test",
        **reproducibility_fields(
            artifact_id="phase212_model_family_closure_or_redesign_precommit",
            generated_utc=generated,
            inputs={
                "phase211_acceptance": str(phase211_dir / "phase211_model_fit_validation_interpretation_acceptance_summary.csv"),
                "phase211_family_summary": str(phase211_dir / "phase211_family_interpretation_summary.csv"),
                "phase211_interpretation": str(phase211_dir / "phase211_validation_interpretation.csv"),
            },
            parameters={
                "closure_required_when_phase211_passing_rows": "0",
                "material_redesign_rows_required": "3",
                "model_fit_allowed": "0",
                "strategy_replay_allowed": "0",
                "test_replay_allowed_next": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "closure": str(output_dir / "phase212_model_family_closure_ledger.csv"),
                "failure": str(output_dir / "phase212_failure_mode_ledger.csv"),
                "redesign": str(output_dir / "phase212_material_redesign_precommit_catalog.csv"),
                "action_queue": str(output_dir / "phase212_phase213_action_queue.csv"),
                "forbidden": str(output_dir / "phase212_execution_forbidden_ledger.csv"),
                "gates": str(output_dir / "phase212_model_family_closure_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase212_model_family_closure_acceptance_summary.csv"),
                "report": str(output_dir / "phase212_model_family_closure_or_redesign_precommit_report.md"),
            },
            scenario_ids="phase212_model_family_closure_or_redesign_precommit_no_replay_no_test",
            cost_model_version="not_applicable_no_replay",
            latency_model_version="not_applicable_no_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase212_model_family_closure_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase212 model-family closure/redesign precommit without replay/test.")
    parser.add_argument("--phase211-dir", type=Path, default=DEFAULT_PHASE211_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase212(args.phase211_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
