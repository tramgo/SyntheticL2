from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE241_DIR = Path("outputs/phase241")
DEFAULT_OUTPUT_DIR = Path("outputs/phase242")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(path: Path, metric: str, default: Any = None) -> Any:
    frame = read_csv(path)
    if frame.empty or "metric" not in frame.columns:
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


def build_closure_decision(phase241_dir: Path) -> pd.DataFrame:
    acceptance = phase241_dir / "phase241_acceptance_summary.csv"
    candidate_id = metric_value(acceptance, "phase241_candidate_id", "")
    net_pnl = as_float(metric_value(acceptance, "phase241_net_pnl_inr", 0.0), 0.0)
    control_pass = as_int(metric_value(acceptance, "phase241_control_pass_rows", 0), 0)
    control_rows = as_int(metric_value(acceptance, "phase241_control_rows", 0), 0)
    survived = as_int(metric_value(acceptance, "phase241_one_date_diagnostic_candidate_survived", 0), 0)
    return pd.DataFrame(
        [
            {
                "candidate_id": candidate_id,
                "decision": "close_exact_phase237_candidate",
                "decision_reason": "positive one-date net P&L did not survive robustness controls",
                "one_date_net_pnl_inr": net_pnl,
                "control_pass_rows": control_pass,
                "control_rows": control_rows,
                "candidate_survived_one_date_diagnostic": survived,
                "download_more_dates_for_this_candidate": 0,
                "reuse_2026_07_17_for_parameter_tuning": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            }
        ]
    )


def build_failure_attribution(phase241_dir: Path) -> pd.DataFrame:
    controls = read_csv(phase241_dir / "phase241_control_summary.csv")
    rows: list[dict[str, Any]] = []
    for row in controls.to_dict("records"):
        control_id = str(row.get("control_id", ""))
        passed = str(row.get("passed", "")).lower() == "true"
        if passed:
            reason = "control_passed"
            action = "retain_as_supporting_evidence_only"
        elif control_id == "RANDOM_SIDE_1000_RUNS":
            reason = "edge_not_strong_enough_against_randomized_direction_control"
            action = "require stronger directional mechanism before any new holdout use"
        elif control_id in {"COST_150", "COST_200"}:
            reason = "edge_not_robust_to_transaction_cost_stress"
            action = "redesign for wider expected move or materially lower turnover"
        elif control_id == "SIDE_FLIP":
            reason = "side_flip_not_rejected"
            action = "do_not_use_directional_signal_without sign validation"
        else:
            reason = "control_failed"
            action = "inspect_before_reuse"
        rows.append(
            {
                "control_id": control_id,
                "passed": int(passed),
                "net_pnl_inr": row.get("net_pnl_inr", ""),
                "random_beat_fraction": row.get("random_beat_fraction", ""),
                "failure_reason": reason,
                "required_redesign_action": action,
            }
        )
    return pd.DataFrame(rows)


def build_redesign_queue(candidate_id: str) -> pd.DataFrame:
    rows = [
        {
            "priority": 1,
            "redesign_track": "cost_stress_first_signal_search",
            "allowed_data": "pre_existing_synthetic_and_discovery_real_anchor_only_not_2026_07_17_tuning",
            "required_change": "optimize for pass under 1.5x and 2.0x modeled Zerodha cost before any future holdout",
            "blocked_action": "do_not_download_more_dates_for_closed_candidate",
        },
        {
            "priority": 2,
            "redesign_track": "random_side_discriminator_strength",
            "allowed_data": "training_discovery_sets_only",
            "required_change": "require random-side beat fraction >=0.95 before reopening a holdout candidate",
            "blocked_action": "do_not_adjust_phase237_thresholds_using_2026_07_17",
        },
        {
            "priority": 3,
            "redesign_track": "lower_turnover_wider_move_hypotheses",
            "allowed_data": "synthetic_only_or_existing_discovery_real_anchor",
            "required_change": "prefer fewer trades with larger expected move and lower cost drag ratio",
            "blocked_action": "do_not_claim_profitability_from_positive_one_date_net_pnl",
        },
    ]
    frame = pd.DataFrame(rows)
    frame["closed_candidate_id"] = candidate_id
    frame["paper_or_live_acceptance_allowed"] = 0
    frame["deployable_profitability_claim_allowed"] = 0
    return frame


def write_report(path: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase242 Closure / Redesign Decision After One-date Diagnostic",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase242 closes the exact Phase237 frozen candidate after the Phase241 one-date unseen diagnostic failed robustness controls.",
        "It opens redesign work that must not tune on the 2026-07-17 holdout and must not consume more disk by downloading dates for the closed candidate.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase241_dir: Path = DEFAULT_PHASE241_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    closure = build_closure_decision(phase241_dir)
    candidate_id = str(closure["candidate_id"].iloc[0]) if not closure.empty else ""
    attribution = build_failure_attribution(phase241_dir)
    redesign = build_redesign_queue(candidate_id)
    hard_rows = [
        ("P242_PHASE241_RESULT_PRESENT", int(not closure.empty), "closure decision row exists"),
        ("P242_CANDIDATE_CLOSED", int(str(closure["decision"].iloc[0]) == "close_exact_phase237_candidate"), "exact candidate closed"),
        ("P242_HOLDOUT_TUNING_BLOCKED", 1, "2026-07-17 cannot be used for parameter tuning"),
        ("P242_MORE_DOWNLOADS_FOR_CLOSED_CANDIDATE_BLOCKED", 1, "no additional raw dates for this closed candidate under low disk"),
        ("P242_NO_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "promotion/paper/live/profitability claims closed"),
    ]
    gates = pd.DataFrame(hard_rows, columns=["gate_id", "passed", "required"])
    next_action = "run_phase243_cost_stress_first_redesign_search_without_2026_07_17_holdout_tuning_no_paper_live"
    acceptance = pd.DataFrame(
        [
            ("phase242_closure_or_redesign_complete", 1, "Phase242 closure/redesign decision completed"),
            ("phase242_closed_candidate_id", candidate_id, "Exact candidate closed"),
            ("phase242_one_date_net_pnl_inr", closure["one_date_net_pnl_inr"].iloc[0], "Phase241 net P&L"),
            ("phase242_control_pass_rows", closure["control_pass_rows"].iloc[0], "Phase241 control passes"),
            ("phase242_control_rows", closure["control_rows"].iloc[0], "Phase241 controls"),
            ("phase242_redesign_queue_rows", int(len(redesign)), "Redesign queue rows opened"),
            ("phase242_download_more_dates_for_closed_candidate_allowed", 0, "Do not spend disk on this closed candidate"),
            ("phase242_holdout_parameter_tuning_allowed", 0, "Do not tune on 2026-07-17"),
            ("phase242_strategy_promotion_allowed", 0, "No strategy promotion from Phase242"),
            ("phase242_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase242"),
            ("phase242_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase242"),
            ("phase242_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    closure.to_csv(output_dir / "phase242_closure_decision.csv", index=False)
    attribution.to_csv(output_dir / "phase242_failure_attribution.csv", index=False)
    redesign.to_csv(output_dir / "phase242_redesign_queue.csv", index=False)
    gates.to_csv(output_dir / "phase242_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase242_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase242_closure_or_redesign_report.md",
        {
            "Acceptance Summary": acceptance,
            "Closure Decision": closure,
            "Failure Attribution": attribution,
            "Redesign Queue": redesign,
            "Gate Evaluation": gates,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase242_close_or_redesign_after_one_date_diagnostic",
        **reproducibility_fields(
            artifact_id="phase242",
            generated_utc=generated_utc,
            inputs={"phase241_dir": str(phase241_dir)},
            parameters={
                "low_disk_policy": "no_more_raw_date_downloads_for_closed_candidate",
                "holdout_tuning_policy": "2026_07_17_not_allowed_for_parameter_tuning",
            },
            outputs={
                "closure_decision": str(output_dir / "phase242_closure_decision.csv"),
                "failure_attribution": str(output_dir / "phase242_failure_attribution.csv"),
                "redesign_queue": str(output_dir / "phase242_redesign_queue.csv"),
                "gate_evaluation": str(output_dir / "phase242_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase242_acceptance_summary.csv"),
                "report": str(output_dir / "phase242_closure_or_redesign_report.md"),
            },
            random_seed="none_deterministic_decision",
            cost_model_version="phase241_zerodha_cost_model",
            latency_model_version="not_applicable_decision_only",
        ),
    }
    (output_dir / "phase242_closure_or_redesign_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase242 close/redesign decision after one-date diagnostic.")
    parser.add_argument("--phase241-dir", type=Path, default=DEFAULT_PHASE241_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase241_dir=args.phase241_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
