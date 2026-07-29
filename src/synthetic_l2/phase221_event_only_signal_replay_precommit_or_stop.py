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
DEFAULT_PHASE220_DIR = Path("outputs/phase220")
DEFAULT_OUTPUT_DIR = Path("outputs/phase221")
FORBIDDEN_OUTPUTS = "strategy_replay_execution;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export"
NEXT_ACTION = "run_phase222_event_only_train_validation_signal_replay_dry_run_no_test"


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


def build_precommit_decision(phase220: pd.DataFrame, interpretation: pd.DataFrame, family_summary: pd.DataFrame) -> pd.DataFrame:
    phase220_complete = as_int(metric_value(phase220, "phase220_event_only_model_fit_validation_interpretation_complete", 0))
    passing_rows = as_int(metric_value(phase220, "phase220_passing_candidate_rows", 0))
    candidate_families = as_int(metric_value(phase220, "phase220_candidate_family_rows", 0))
    best_base = as_float(metric_value(phase220, "phase220_best_mse_improvement_vs_base", 0.0))
    best_shuffle = as_float(metric_value(phase220, "phase220_best_improvement_vs_shuffle", 0.0))
    best_corr = as_float(metric_value(phase220, "phase220_best_validation_correlation", 0.0))
    replay_precommit_allowed = int(phase220_complete == 1 and passing_rows >= 3 and candidate_families >= 1 and best_base > 0 and best_shuffle > 0 and best_corr >= 0.10)
    family = ""
    if not family_summary.empty:
        candidates = family_summary[pd.to_numeric(family_summary["candidate_family_for_phase221"], errors="coerce").fillna(0).astype(int).eq(1)]
        family = ";".join(candidates["model_family"].astype(str).tolist())
    return pd.DataFrame(
        [
            {
                "phase221_decision_id": "P221_PRECOMMIT_EVENT_ONLY_TRAIN_VALIDATION_REPLAY_DRY_RUN",
                "decision": "precommit_phase222_event_only_train_validation_signal_replay_dry_run" if replay_precommit_allowed else "stop_or_redesign_before_replay_precommit",
                "phase220_complete": phase220_complete,
                "passing_candidate_rows": passing_rows,
                "candidate_model_families": family,
                "candidate_family_rows": candidate_families,
                "best_mse_improvement_vs_base": best_base,
                "best_improvement_vs_shuffle": best_shuffle,
                "best_validation_correlation": best_corr,
                "phase222_replay_dry_run_precommitted": replay_precommit_allowed,
                "strategy_replay_execution_allowed_phase221": 0,
                "strategy_replay_allowed_next": replay_precommit_allowed,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "profitability_claim_allowed": 0,
            }
        ]
    )


def build_candidate_freeze(interpretation: pd.DataFrame) -> pd.DataFrame:
    passing = interpretation[pd.to_numeric(interpretation["interpretation_pass"], errors="coerce").fillna(0).astype(int).eq(1)].copy() if not interpretation.empty else pd.DataFrame()
    if passing.empty:
        return pd.DataFrame()
    keep = [
        "phase219_model_fit_id",
        "model_family",
        "target_label",
        "horizon_sec",
        "rows",
        "positive_rate",
        "mse_improvement_vs_base",
        "improvement_vs_shuffle",
        "correlation",
        "binary_accuracy",
    ]
    cols = [c for c in keep if c in passing.columns]
    out = passing[cols].copy()
    out.insert(0, "phase221_candidate_id", [f"P221_CANDIDATE_{i+1:02d}" for i in range(len(out))])
    out["candidate_frozen_for_phase222"] = 1
    out["threshold_widening_allowed"] = 0
    out["strategy_replay_execution_allowed_phase221"] = 0
    out["test_replay_allowed_next"] = 0
    return out


def build_signal_rule_contract(candidates: pd.DataFrame) -> pd.DataFrame:
    if candidates.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for row in candidates.to_dict("records"):
        rows.append(
            {
                "phase221_signal_rule_id": str(row.get("phase221_candidate_id", "")).replace("CANDIDATE", "SIGNAL_RULE"),
                "phase221_candidate_id": row.get("phase221_candidate_id", ""),
                "phase219_model_fit_id": row.get("phase219_model_fit_id", ""),
                "target_label": row.get("target_label", ""),
                "horizon_sec": as_int(row.get("horizon_sec", 0)),
                "signal_direction_policy": "event_only_probability_score_ranked_direction_for_target_label",
                "entry_filter": "event_surprise_bucket == 1 and validation_precommitted_candidate_only",
                "threshold_policy": "phase222_train_validation_diagnostic_threshold_grid_predeclared_no_test",
                "max_threshold_grid_values": "0.55;0.60;0.65;0.70",
                "position_sizing_policy": "unit_notional_diagnostic_only",
                "row_level_prediction_export_allowed": 0,
                "strategy_replay_execution_allowed_phase221": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
            }
        )
    return pd.DataFrame(rows)


def build_replay_contract(decision: pd.DataFrame, candidates: pd.DataFrame, costs: pd.DataFrame, latency: pd.DataFrame) -> pd.DataFrame:
    dry_run_precommit = as_int(decision["phase222_replay_dry_run_precommitted"].iloc[0]) if not decision.empty else 0
    cost_rows = len(costs)
    latency_rows = len(latency)
    return pd.DataFrame(
        [
            {
                "phase221_replay_contract_id": "P221_EVENT_ONLY_TRAIN_VALIDATION_REPLAY_CONTRACT",
                "contract": "Phase222 may run only train/validation diagnostic signal replay for frozen Phase221 candidates, with Phase180 Zerodha cost components and latency/slippage profiles bound before any net metric.",
                "candidate_rows": len(candidates),
                "cost_component_rows_required": cost_rows,
                "latency_profile_rows_required": latency_rows,
                "allowed_splits": "train;validation",
                "sealed_test_rows_used": 0,
                "strategy_replay_execution_allowed_phase221": 0,
                "strategy_replay_execution_allowed_phase222": dry_run_precommit,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "profitability_claim_allowed": 0,
            }
        ]
    )


def build_phase222_work_order(decision: pd.DataFrame, candidates: pd.DataFrame, signal_rules: pd.DataFrame, replay_contract: pd.DataFrame) -> pd.DataFrame:
    allowed = as_int(decision["phase222_replay_dry_run_precommitted"].iloc[0]) if not decision.empty else 0
    return pd.DataFrame(
        [
            {
                "phase222_work_order_id": "P222_EVENT_ONLY_TRAIN_VALIDATION_SIGNAL_REPLAY_DRY_RUN",
                "work_order": "Run train/validation-only event-only signal replay for frozen Phase221 candidates with Phase180 costs/latency; no sealed test, no promotion, no paper/live, no profitability claim.",
                "phase222_replay_dry_run_precommitted": allowed,
                "candidate_rows": len(candidates),
                "signal_rule_rows": len(signal_rules),
                "replay_contract_rows": len(replay_contract),
                "allowed_next_scope": "train_validation_signal_replay_dry_run_no_test",
                "strategy_replay_execution_allowed_phase222": allowed,
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
                "emitted_in_phase221": 0,
                "allowed_in_phase221": 0,
                "rationale": "Phase221 precommits a future replay contract only and emits no replay, test, promotion, P&L, prediction export, paper/live, or profitability artifact.",
            }
            for item in FORBIDDEN_OUTPUTS.split(";")
        ]
    )


def build_gates(
    phase220: pd.DataFrame,
    decision: pd.DataFrame,
    candidates: pd.DataFrame,
    signal_rules: pd.DataFrame,
    replay_contract: pd.DataFrame,
    work_order: pd.DataFrame,
    forbidden: pd.DataFrame,
) -> pd.DataFrame:
    phase220_complete = as_int(metric_value(phase220, "phase220_event_only_model_fit_validation_interpretation_complete", 0))
    precommitted = as_int(decision["phase222_replay_dry_run_precommitted"].iloc[0]) if not decision.empty else 0
    phase221_replay_exec = as_int(decision["strategy_replay_execution_allowed_phase221"].iloc[0]) if not decision.empty else 1
    forbidden_emitted = int(pd.to_numeric(forbidden["emitted_in_phase221"], errors="coerce").fillna(0).sum()) if not forbidden.empty else 1
    replay_flags = 0
    for frame in [decision, candidates, signal_rules, replay_contract, work_order]:
        for col in ["strategy_replay_execution_allowed_phase221", "test_replay_allowed_next", "promotion_allowed", "paper_or_live_acceptance_allowed", "profitability_claim_allowed", "threshold_widening_allowed", "row_level_prediction_export_allowed"]:
            if not frame.empty and col in frame.columns:
                replay_flags += int(pd.to_numeric(frame[col], errors="coerce").fillna(0).sum())
    return pd.DataFrame(
        [
            ("P221_PHASE220_COMPLETE", phase220_complete == 1, f"phase220_complete={phase220_complete}", "hard"),
            ("P221_DECISION_RECORDED", len(decision) == 1 and precommitted == 1, f"decision_rows={len(decision)}; phase222_precommitted={precommitted}", "hard"),
            ("P221_CANDIDATES_FROZEN", len(candidates) == 5 and int(pd.to_numeric(candidates["candidate_frozen_for_phase222"], errors="coerce").fillna(0).sum()) == 5, f"candidate_rows={len(candidates)}", "hard"),
            ("P221_SIGNAL_RULE_CONTRACT_RECORDED", len(signal_rules) == len(candidates), f"signal_rule_rows={len(signal_rules)}; candidate_rows={len(candidates)}", "hard"),
            ("P221_REPLAY_COST_LATENCY_CONTRACT_RECORDED", len(replay_contract) == 1 and as_int(replay_contract["cost_component_rows_required"].iloc[0]) >= 1 and as_int(replay_contract["latency_profile_rows_required"].iloc[0]) >= 1, f"replay_contract_rows={len(replay_contract)}", "hard"),
            ("P221_PHASE222_WORK_ORDER_RECORDED", len(work_order) == 1 and as_int(work_order["strategy_replay_execution_allowed_phase222"].iloc[0]) == 1, f"work_order_rows={len(work_order)}", "hard"),
            ("P221_PHASE221_REPLAY_EXECUTION_CLOSED", phase221_replay_exec == 0, f"phase221_replay_execution={phase221_replay_exec}", "hard"),
            ("P221_FORBIDDEN_OUTPUTS_CLEAN", forbidden_emitted == 0 and replay_flags == 0, f"forbidden_emitted={forbidden_emitted}; replay_flags={replay_flags}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(decision: pd.DataFrame, candidates: pd.DataFrame, signal_rules: pd.DataFrame, replay_contract: pd.DataFrame, work_order: pd.DataFrame, forbidden: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("phase221_decision_rows", len(decision), "Decision rows"),
            ("phase221_candidate_rows", len(candidates), "Frozen candidate rows"),
            ("phase221_signal_rule_rows", len(signal_rules), "Signal rule contract rows"),
            ("phase221_replay_contract_rows", len(replay_contract), "Replay precommit contract rows"),
            ("phase221_phase222_work_order_rows", len(work_order), "Phase222 work-order rows"),
            ("phase221_forbidden_execution_rows", len(forbidden), "Forbidden execution rows"),
            ("phase221_gate_rows", len(gates), "Gates evaluated"),
            ("phase221_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase221_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase221_event_only_signal_replay_precommit_or_stop_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase221 completed"),
            ("phase221_phase222_replay_dry_run_precommitted", as_int(decision["phase222_replay_dry_run_precommitted"].iloc[0]) if not decision.empty else 0, "1 means Phase222 may execute train/validation replay dry run"),
            ("phase221_strategy_replay_execution_allowed", 0, "No strategy replay execution in Phase221"),
            ("phase221_strategy_replay_allowed_next", as_int(decision["strategy_replay_allowed_next"].iloc[0]) if not decision.empty else 0, "1 means next phase may execute gated train/validation replay"),
            ("phase221_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase221_promotion_allowed", 0, "No promotion opened"),
            ("phase221_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase221_profitability_claim_allowed", 0, "No profitability claim is allowed"),
            ("phase221_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase221_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase221 Event-only Signal Replay Precommit-or-stop",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase221 freezes Phase220 passing candidates and precommits a train/validation-only signal replay dry-run contract for Phase222.",
        "It does not execute replay, use sealed test, emit predictions, compute P&L, promote anything, open paper/live acceptance, or make profitability claims.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase221_event_only_signal_replay_precommit_or_stop_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase221(phase180_dir: Path, phase220_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase220 = read_csv(phase220_dir / "phase220_validation_interpretation_acceptance_summary.csv")
    interpretation = read_csv(phase220_dir / "phase220_validation_interpretation.csv")
    family_summary = read_csv(phase220_dir / "phase220_model_family_summary.csv")
    costs = read_csv(phase180_dir / "phase180_zerodha_equity_cost_component_catalog.csv")
    latency = read_csv(phase180_dir / "phase180_latency_slippage_profile_catalog.csv")
    decision = build_precommit_decision(phase220, interpretation, family_summary)
    candidates = build_candidate_freeze(interpretation)
    signal_rules = build_signal_rule_contract(candidates)
    replay_contract = build_replay_contract(decision, candidates, costs, latency)
    work_order = build_phase222_work_order(decision, candidates, signal_rules, replay_contract)
    forbidden = build_forbidden_execution_ledger()
    gates = build_gates(phase220, decision, candidates, signal_rules, replay_contract, work_order, forbidden)
    acceptance = build_acceptance(decision, candidates, signal_rules, replay_contract, work_order, forbidden, gates)

    decision.to_csv(output_dir / "phase221_signal_replay_precommit_decision.csv", index=False)
    candidates.to_csv(output_dir / "phase221_frozen_candidate_contract.csv", index=False)
    signal_rules.to_csv(output_dir / "phase221_signal_rule_contract.csv", index=False)
    replay_contract.to_csv(output_dir / "phase221_replay_cost_latency_contract.csv", index=False)
    work_order.to_csv(output_dir / "phase221_phase222_work_order.csv", index=False)
    forbidden.to_csv(output_dir / "phase221_execution_forbidden_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase221_signal_replay_precommit_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase221_signal_replay_precommit_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Decision": decision,
            "Frozen Candidate Contract": candidates,
            "Signal Rule Contract": signal_rules,
            "Replay Cost Latency Contract": replay_contract,
            "Phase222 Work Order": work_order,
            "Forbidden Execution Ledger": forbidden,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase221_event_only_signal_replay_precommit_or_stop_no_replay_no_test",
        **reproducibility_fields(
            artifact_id="phase221_event_only_signal_replay_precommit_or_stop",
            generated_utc=generated,
            inputs={
                "phase220_acceptance": str(phase220_dir / "phase220_validation_interpretation_acceptance_summary.csv"),
                "phase220_interpretation": str(phase220_dir / "phase220_validation_interpretation.csv"),
                "phase220_family_summary": str(phase220_dir / "phase220_model_family_summary.csv"),
                "phase180_cost_catalog": str(phase180_dir / "phase180_zerodha_equity_cost_component_catalog.csv"),
                "phase180_latency_catalog": str(phase180_dir / "phase180_latency_slippage_profile_catalog.csv"),
            },
            parameters={
                "minimum_passing_candidates": "3",
                "allowed_splits_next": "train;validation",
                "strategy_replay_execution_allowed_phase221": "0",
                "strategy_replay_execution_allowed_phase222": "1",
                "test_replay_allowed_next": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "decision": str(output_dir / "phase221_signal_replay_precommit_decision.csv"),
                "candidates": str(output_dir / "phase221_frozen_candidate_contract.csv"),
                "signal_rules": str(output_dir / "phase221_signal_rule_contract.csv"),
                "replay_contract": str(output_dir / "phase221_replay_cost_latency_contract.csv"),
                "work_order": str(output_dir / "phase221_phase222_work_order.csv"),
                "forbidden": str(output_dir / "phase221_execution_forbidden_ledger.csv"),
                "gates": str(output_dir / "phase221_signal_replay_precommit_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase221_signal_replay_precommit_acceptance_summary.csv"),
                "report": str(output_dir / "phase221_event_only_signal_replay_precommit_or_stop_report.md"),
            },
            scenario_ids="phase221_event_only_signal_replay_precommit_or_stop_no_replay_no_test",
            cost_model_version="phase180_zerodha_equity_cost_component_catalog_bound_for_phase222",
            latency_model_version="phase180_latency_slippage_profile_catalog_bound_for_phase222",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase221_signal_replay_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase221 event-only signal replay precommit-or-stop without replay/test.")
    parser.add_argument("--phase180-dir", type=Path, default=DEFAULT_PHASE180_DIR)
    parser.add_argument("--phase220-dir", type=Path, default=DEFAULT_PHASE220_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase221(args.phase180_dir, args.phase220_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
