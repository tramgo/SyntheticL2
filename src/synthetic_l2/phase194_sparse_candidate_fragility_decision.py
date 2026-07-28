from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE193_DIR = Path("outputs/phase193")
DEFAULT_OUTPUT_DIR = Path("outputs/phase194")
FORBIDDEN_OUTPUTS = "test_result;test_replay_execution;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim"


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


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def build_fragility_decision(acceptance: pd.DataFrame, by_date: pd.DataFrame) -> pd.DataFrame:
    extension = by_date.loc[by_date["split_role"].astype(str).eq("unassigned")].copy()
    validation = by_date.loc[by_date["split_role"].astype(str).eq("validation")].copy()
    extension_dates = sorted(extension["trade_date"].astype(str).unique().tolist()) if not extension.empty else []
    profiles = sorted(by_date["latency_profile_id"].astype(str).unique().tolist()) if not by_date.empty else []
    extension_profile_date_rows = int(len(extension))
    negative_extension_rows = int((pd.to_numeric(extension["net_return_bps_after_cost_proxy_mean"], errors="coerce") <= 0).sum()) if not extension.empty else 0
    all_extension_profile_dates_negative = int(extension_profile_date_rows > 0 and negative_extension_rows == extension_profile_date_rows)
    original_validation_positive = int(
        not validation.empty
        and (pd.to_numeric(validation["net_return_bps_after_cost_proxy_mean"], errors="coerce") > 0).all()
    )
    date_positive_fraction = as_float(metric_value(acceptance, "phase193_min_profile_net_bps_proxy_mean", 0.0))
    phase193_verdict = str(metric_value(acceptance, "phase193_verdict", ""))
    decision = (
        "close_frozen_sparse_candidate_for_test_replay_redesign_required"
        if all_extension_profile_dates_negative
        else "keep_collecting_validation_before_test_replay"
    )
    return pd.DataFrame(
        [
            {
                "candidate_id": metric_value(acceptance, "phase193_candidate_id", ""),
                "candidate_contract_hash": metric_value(acceptance, "phase193_candidate_contract_hash", ""),
                "original_validation_dates": metric_value(acceptance, "phase193_original_validation_dates", ""),
                "extension_validation_dates": ";".join(extension_dates),
                "latency_profiles_evaluated": ";".join(profiles),
                "extension_profile_date_rows": extension_profile_date_rows,
                "negative_extension_profile_date_rows": negative_extension_rows,
                "all_extension_profile_dates_negative": all_extension_profile_dates_negative,
                "original_validation_positive_all_profiles": original_validation_positive,
                "phase193_min_profile_net_bps_proxy_mean": date_positive_fraction,
                "phase193_verdict": phase193_verdict,
                "phase194_decision": decision,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
            }
        ]
    )


def build_redesign_blueprint(decision: pd.DataFrame) -> pd.DataFrame:
    row = decision.iloc[0] if not decision.empty else {}
    candidate_id = row.get("candidate_id", "")
    return pd.DataFrame(
        [
            {
                "blueprint_id": "P194_REGIME_CONSISTENT_RECEIVE_FLOW",
                "closed_candidate_id": candidate_id,
                "design_change": "Require candidate to be net positive by date under both retail latency profiles before any test precommit.",
                "rationale": "The frozen sparse candidate was positive on the original validation date but negative on every added validation-extension profile/date row.",
                "required_gate": "date_positive_fraction_equals_1_before_test_precommit",
            },
            {
                "blueprint_id": "P194_SYMBOL_BREADTH_FILTER",
                "closed_candidate_id": candidate_id,
                "design_change": "Penalize or reject candidates with symbol-positive fraction below 25 percent, even when aggregate net is positive.",
                "rationale": "Phase193 symbol-positive fraction remained about 6.45 percent, indicating narrow symbol support.",
                "required_gate": "symbol_positive_fraction_ge_0p25",
            },
            {
                "blueprint_id": "P194_EXTENSION_FIRST_SELECTION_DISCIPLINE",
                "closed_candidate_id": candidate_id,
                "design_change": "Use train-only selection, validation for screening, validation-extension for rejection, and keep test untouched until all validation-extension gates pass.",
                "rationale": "Avoid letting one strong validation date dominate the decision and accidentally spend the only untouched test split.",
                "required_gate": "test_replay_allowed_next_equals_0_until_extension_pass",
            },
        ]
    )


def build_gates(decision: pd.DataFrame, blueprint: pd.DataFrame) -> pd.DataFrame:
    row = decision.iloc[0] if not decision.empty else {}
    return pd.DataFrame(
        [
            {"gate_id": "P194_PHASE193_EVIDENCE_PRESENT", "gate_pass": int(not decision.empty), "evidence": f"decision_rows={len(decision)}", "severity": "hard"},
            {"gate_id": "P194_EXTENSION_NEGATIVE_RECORDED", "gate_pass": int(int(row.get("all_extension_profile_dates_negative", 0)) == 1), "evidence": f"negative_extension_profile_date_rows={row.get('negative_extension_profile_date_rows', '')}; extension_profile_date_rows={row.get('extension_profile_date_rows', '')}", "severity": "hard"},
            {"gate_id": "P194_TEST_REPLAY_CLOSED", "gate_pass": int(int(row.get("test_replay_allowed_next", 1)) == 0), "evidence": "test_replay_allowed_next=0", "severity": "hard"},
            {"gate_id": "P194_PROMOTION_CLOSED", "gate_pass": int(int(row.get("promotion_allowed", 1)) == 0), "evidence": "promotion_allowed=0", "severity": "hard"},
            {"gate_id": "P194_PAPER_LIVE_CLOSED", "gate_pass": int(int(row.get("paper_or_live_acceptance_allowed", 1)) == 0), "evidence": "paper_or_live_acceptance_allowed=0", "severity": "hard"},
            {"gate_id": "P194_REDESIGN_BLUEPRINT_WRITTEN", "gate_pass": int(len(blueprint) >= 3), "evidence": f"blueprint_rows={len(blueprint)}", "severity": "hard"},
        ]
    )


def build_acceptance(decision: pd.DataFrame, blueprint: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates.loc[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(int).sum()) if not hard.empty else 0
    row = decision.iloc[0] if not decision.empty else {}
    return pd.DataFrame(
        [
            ("phase194_decision_rows", int(len(decision)), "Fragility decision rows"),
            ("phase194_blueprint_rows", int(len(blueprint)), "Redesign blueprint rows"),
            ("phase194_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase194_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase194_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase194_candidate_id", row.get("candidate_id", ""), "Candidate assessed"),
            ("phase194_extension_validation_dates", row.get("extension_validation_dates", ""), "Extension dates in decision"),
            ("phase194_all_extension_profile_dates_negative", row.get("all_extension_profile_dates_negative", ""), "1 means every extension profile/date row is net negative"),
            ("phase194_decision", row.get("phase194_decision", ""), "Decision"),
            ("phase194_fragility_decision_complete", int(len(hard) > 0 and hard_pass == len(hard)), "1 means Phase194 completed"),
            ("phase194_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase194_promotion_allowed", 0, "No promotion opened"),
            ("phase194_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase194_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase194_next_best_action", "redesign_receive_flow_candidate_with_date_and_symbol_breadth_gates_before_test", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase194 Sparse Candidate Fragility Decision",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase194 turns the Phase193 validation-extension evidence into a no-test research decision.",
        "It closes the frozen sparse candidate for test replay and writes redesign gates.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase194_sparse_candidate_fragility_decision_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase194(phase193_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    acceptance193 = read_csv(phase193_dir / "phase193_validation_breadth_extension_acceptance_summary.csv")
    by_date = read_csv(phase193_dir / "phase193_validation_extension_by_date.csv")
    decision = build_fragility_decision(acceptance193, by_date)
    blueprint = build_redesign_blueprint(decision)
    gates = build_gates(decision, blueprint)
    acceptance = build_acceptance(decision, blueprint, gates)

    decision.to_csv(output_dir / "phase194_sparse_candidate_fragility_decision.csv", index=False)
    blueprint.to_csv(output_dir / "phase194_receive_flow_redesign_blueprint.csv", index=False)
    gates.to_csv(output_dir / "phase194_sparse_candidate_fragility_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase194_sparse_candidate_fragility_acceptance_summary.csv", index=False)
    write_report(output_dir, {"Acceptance Summary": acceptance, "Fragility Decision": decision, "Redesign Blueprint": blueprint, "Gate Evaluation": gates})
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase194_sparse_candidate_fragility_decision_no_test",
        **reproducibility_fields(
            artifact_id="phase194_sparse_candidate_fragility_decision",
            generated_utc=generated,
            inputs={
                "phase193_acceptance": str(phase193_dir / "phase193_validation_breadth_extension_acceptance_summary.csv"),
                "phase193_by_date": str(phase193_dir / "phase193_validation_extension_by_date.csv"),
            },
            parameters={
                "decision_policy": "close_candidate_when_all_added_extension_profile_date_rows_are_negative",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "decision": str(output_dir / "phase194_sparse_candidate_fragility_decision.csv"),
                "blueprint": str(output_dir / "phase194_receive_flow_redesign_blueprint.csv"),
                "gate_evaluation": str(output_dir / "phase194_sparse_candidate_fragility_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase194_sparse_candidate_fragility_acceptance_summary.csv"),
                "report": str(output_dir / "phase194_sparse_candidate_fragility_decision_report.md"),
            },
            random_seed="none_deterministic_decision",
            scenario_ids="phase194_sparse_candidate_fragility_decision_no_test",
            cost_model_version="phase180_inherited_via_phase193",
            latency_model_version="phase180_inherited_via_phase193",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase194_sparse_candidate_fragility_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase193-dir", type=Path, default=DEFAULT_PHASE193_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase194(args.phase193_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
