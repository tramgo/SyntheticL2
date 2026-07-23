from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE164_DIR = Path("outputs/phase164")
DEFAULT_OUTPUT_DIR = Path("outputs/phase165")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = "missing") -> Any:
    if frame.empty or "metric" not in frame.columns or "value" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def to_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def build_gate_evaluation(acceptance: pd.DataFrame, summary: pd.DataFrame) -> pd.DataFrame:
    full_year_complete = to_int(metric_value(acceptance, "phase164_full_year_replay_complete", 0)) == 1
    positive_rows = to_int(metric_value(acceptance, "phase164_positive_after_cost_rows", 0))
    candidate_rows = to_int(metric_value(acceptance, "phase164_synthetic_replay_candidate_rows", 0))
    promotion_allowed = to_int(metric_value(acceptance, "phase164_strategy_promotion_allowed", 1))
    paper_allowed = to_int(metric_value(acceptance, "phase164_paper_or_live_acceptance_allowed", 1))
    deployable_claim_allowed = to_int(metric_value(acceptance, "phase164_deployable_profitability_claim_allowed", 1))
    best_pnl = float(summary["annual_net_pnl_inr"].max()) if not summary.empty else 0.0
    return pd.DataFrame(
        [
            {
                "gate_id": "P165_FULL_YEAR_REPLAY_COMPLETE",
                "passed": full_year_complete,
                "observed_value": metric_value(acceptance, "phase164_shards_scanned", "missing"),
                "required_value": metric_value(acceptance, "phase164_expected_shards", "missing"),
                "interpretation": "Phase164 covered every Phase162 dense month/symbol shard.",
            },
            {
                "gate_id": "P165_POSITIVE_AFTER_COST_ECONOMICS",
                "passed": positive_rows > 0,
                "observed_value": positive_rows,
                "required_value": ">0 strategy/profile rows",
                "interpretation": "At least one strategy/profile must be net-positive after Zerodha-style costs to continue as a candidate.",
            },
            {
                "gate_id": "P165_SYNTHETIC_REPLAY_CANDIDATE",
                "passed": candidate_rows > 0,
                "observed_value": candidate_rows,
                "required_value": ">0 positive plus risk-proxy-pass rows",
                "interpretation": "A replay candidate must clear both economics and risk proxy screens.",
            },
            {
                "gate_id": "P165_BEST_PROFILE_NET_POSITIVE",
                "passed": best_pnl > 0,
                "observed_value": best_pnl,
                "required_value": ">0 INR annual net P&L",
                "interpretation": "Best observed Phase164 strategy/profile is still negative if this gate fails.",
            },
            {
                "gate_id": "P165_PROMOTION_BOUNDARY_CLOSED",
                "passed": promotion_allowed == 0,
                "observed_value": promotion_allowed,
                "required_value": "0",
                "interpretation": "Synthetic replay verdict must not promote a strategy.",
            },
            {
                "gate_id": "P165_BROKER_BOUNDARY_CLOSED",
                "passed": paper_allowed == 0,
                "observed_value": paper_allowed,
                "required_value": "0",
                "interpretation": "Synthetic replay verdict must not claim paper/live or broker readiness.",
            },
            {
                "gate_id": "P165_DEPLOYABLE_CLAIM_CLOSED",
                "passed": deployable_claim_allowed == 0,
                "observed_value": deployable_claim_allowed,
                "required_value": "0",
                "interpretation": "Synthetic replay verdict must not make a deployable profitability claim.",
            },
        ]
    )


def build_verdict(acceptance: pd.DataFrame, summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    full_year_complete = bool(gates.loc[gates["gate_id"].eq("P165_FULL_YEAR_REPLAY_COMPLETE"), "passed"].iloc[0])
    candidate_rows = to_int(metric_value(acceptance, "phase164_synthetic_replay_candidate_rows", 0))
    positive_rows = to_int(metric_value(acceptance, "phase164_positive_after_cost_rows", 0))
    best = summary.sort_values("annual_net_pnl_inr", ascending=False, kind="mergesort").head(1)
    best_strategy = best["strategy_id"].iloc[0] if not best.empty else "none"
    best_profile = best["execution_profile"].iloc[0] if not best.empty else "none"
    best_pnl = float(best["annual_net_pnl_inr"].iloc[0]) if not best.empty else 0.0
    if full_year_complete and candidate_rows == 0:
        outcome = "A_SYNTHETIC_FULL_YEAR_REPLAY_FALSIFIED"
        decision = "close_phase164_current_guarded_diagnostic_forms"
        next_action = "stop_current_phase164_strategy_forms_or_design_new_precommitted_non_blocklisted_hypothesis"
    elif full_year_complete and candidate_rows > 0:
        outcome = "B_SYNTHETIC_CANDIDATE_HANDOFF"
        decision = "create_non_deployable_synthetic_candidate_handoff"
        next_action = "precommit_real_anchor_or_stricter_holdout_before_any_promotion"
    else:
        outcome = "INCOMPLETE"
        decision = "continue_phase164_until_full_year_complete"
        next_action = "continue_phase164_until_384_shards"
    return pd.DataFrame(
        [
            {
                "verdict_id": "phase165_phase164_full_year_replay_verdict",
                "outcome": outcome,
                "decision": decision,
                "phase164_full_year_complete": int(full_year_complete),
                "phase164_positive_after_cost_rows": positive_rows,
                "phase164_synthetic_replay_candidate_rows": candidate_rows,
                "best_strategy_id": best_strategy,
                "best_execution_profile": best_profile,
                "best_annual_net_pnl_inr": best_pnl,
                "strategy_promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
                "next_best_action": next_action,
            }
        ]
    )


def build_blocklist_candidates(summary: pd.DataFrame) -> pd.DataFrame:
    if summary.empty:
        return pd.DataFrame()
    rows = []
    for source_strategy_id, group in summary.groupby("source_strategy_id", sort=True):
        if str(source_strategy_id) in {"S10", "S11"}:
            continue
        positive_rows = int(group["positive_after_costs"].astype(bool).sum())
        candidate_rows = int(group["synthetic_replay_candidate"].astype(bool).sum())
        rows.append(
            {
                "blocked_family_id": f"PHASE164_{source_strategy_id}_GUARDED_DIAGNOSTIC",
                "source_strategy_id": source_strategy_id,
                "phase164_strategy_ids": ";".join(sorted(group["strategy_id"].astype(str).unique())),
                "best_annual_net_pnl_inr": float(group["annual_net_pnl_inr"].max()),
                "positive_after_cost_rows": positive_rows,
                "synthetic_replay_candidate_rows": candidate_rows,
                "recommended_status": "block_current_phase164_form" if positive_rows == 0 and candidate_rows == 0 else "review_candidate",
                "unlock_condition": "new precommitted feature hypothesis, changed label/execution contract, or real-anchor evidence; do not rerun same Phase164 form hoping for profit",
            }
        )
    return pd.DataFrame(rows)


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase165 Phase164 Full-year Replay Verdict",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase165 turns the completed Phase164 synthetic-only full-year replay into a verdict.",
        "It does not promote strategies, does not claim paper/live readiness, and does not claim deployable profitability.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase165_phase164_full_year_replay_verdict_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase165(phase164_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    acceptance = read_csv(phase164_dir / "phase164_synthetic_only_full_year_replay_acceptance_summary.csv")
    summary = read_csv(phase164_dir / "phase164_strategy_profile_summary.csv")
    gates = build_gate_evaluation(acceptance, summary)
    verdict = build_verdict(acceptance, summary, gates)
    blocklist_candidates = build_blocklist_candidates(summary)

    gates.to_csv(output_dir / "phase165_verdict_gate_evaluation.csv", index=False)
    verdict.to_csv(output_dir / "phase165_phase164_full_year_replay_verdict.csv", index=False)
    blocklist_candidates.to_csv(output_dir / "phase165_blocklist_candidate_update.csv", index=False)
    acceptance_summary = pd.DataFrame(
        [
            ("phase165_outcome", verdict["outcome"].iloc[0], "Selected Phase165 outcome"),
            ("phase165_full_year_complete", verdict["phase164_full_year_complete"].iloc[0], "Inherited Phase164 full-year completion"),
            ("phase165_positive_after_cost_rows", verdict["phase164_positive_after_cost_rows"].iloc[0], "Inherited Phase164 positive rows"),
            ("phase165_synthetic_replay_candidate_rows", verdict["phase164_synthetic_replay_candidate_rows"].iloc[0], "Inherited Phase164 candidate rows"),
            ("phase165_best_strategy_id", verdict["best_strategy_id"].iloc[0], "Best Phase164 strategy/profile by annual net P&L"),
            ("phase165_best_annual_net_pnl_inr", verdict["best_annual_net_pnl_inr"].iloc[0], "Best annual net P&L remains synthetic-only"),
            ("phase165_strategy_promotion_allowed", 0, "Strategy promotion remains closed"),
            ("phase165_paper_or_live_acceptance_allowed", 0, "Paper/live broker acceptance remains closed"),
            ("phase165_next_best_action", verdict["next_best_action"].iloc[0], "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    acceptance_summary.to_csv(output_dir / "phase165_full_year_replay_verdict_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance_summary,
            "Verdict": verdict,
            "Gate Evaluation": gates,
            "Blocklist Candidate Update": blocklist_candidates,
            "Phase164 Strategy Summary": summary,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase165_phase164_full_year_replay_verdict",
        **reproducibility_fields(
            artifact_id="phase165",
            generated_utc=generated_utc,
            inputs={
                "phase164_acceptance_summary": str(phase164_dir / "phase164_synthetic_only_full_year_replay_acceptance_summary.csv"),
                "phase164_strategy_profile_summary": str(phase164_dir / "phase164_strategy_profile_summary.csv"),
            },
            parameters={
                "verdict_policy": "candidate_requires_positive_after_costs_and_risk_proxy_pass",
                "strategy_promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "gate_evaluation": str(output_dir / "phase165_verdict_gate_evaluation.csv"),
                "verdict": str(output_dir / "phase165_phase164_full_year_replay_verdict.csv"),
                "blocklist_candidate_update": str(output_dir / "phase165_blocklist_candidate_update.csv"),
                "acceptance_summary": str(output_dir / "phase165_full_year_replay_verdict_acceptance_summary.csv"),
                "report": str(output_dir / "phase165_phase164_full_year_replay_verdict_report.md"),
                "manifest": str(output_dir / "phase165_phase164_full_year_replay_verdict_manifest.json"),
            },
            random_seed="none_deterministic_phase165_verdict",
            scenario_ids="phase164_completed_full_year_replay",
            cost_model_version="zerodha_equity_intraday_nse_order_formula_v2_2026_07_14",
            latency_model_version="phase12_execution_profiles_v1_reused_for_phase164",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase165_phase164_full_year_replay_verdict_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Issue Phase165 verdict for completed Phase164 replay.")
    parser.add_argument("--phase164-dir", type=Path, default=DEFAULT_PHASE164_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase165(args.phase164_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
