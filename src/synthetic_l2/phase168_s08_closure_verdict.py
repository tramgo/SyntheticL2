from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE167_DIR = Path("outputs/phase167")
DEFAULT_OUTPUT_DIR = Path("outputs/phase168")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = "missing") -> Any:
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"] if "metric" in frame.columns else pd.Series(dtype=object)
    if rows.empty:
        return default
    return rows.iloc[0]


def to_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def build_gate_evaluation(acceptance: pd.DataFrame, gates: pd.DataFrame, profile_summary: pd.DataFrame) -> pd.DataFrame:
    cache_ready = to_int(metric_value(acceptance, "phase167_source_cache_ready", 0))
    files_scanned = to_int(metric_value(acceptance, "phase167_cache_files_scanned", 0))
    trade_rows = to_int(metric_value(acceptance, "phase167_trade_rows", 0))
    positive_rows = to_int(metric_value(acceptance, "phase167_positive_after_cost_profile_rows", 0))
    candidate_rows = to_int(metric_value(acceptance, "phase167_candidate_profile_rows", 0))
    promotion_allowed = to_int(metric_value(acceptance, "phase167_strategy_promotion_allowed", 1))
    paper_allowed = to_int(metric_value(acceptance, "phase167_paper_or_live_acceptance_allowed", 1))
    deployable_allowed = to_int(metric_value(acceptance, "phase167_deployable_profitability_claim_allowed", 1))
    best_pnl = float(profile_summary["annual_net_pnl_inr"].max()) if not profile_summary.empty else 0.0
    all_gate_profiles_fail = bool((~gates["phase167_profile_pass"].astype(bool)).all()) if not gates.empty else False
    return pd.DataFrame(
        [
            {
                "gate_id": "P168_PHASE166_CACHE_READY",
                "passed": cache_ready == 1,
                "observed_value": cache_ready,
                "required_value": "1",
                "interpretation": "S08 closure is based on a ready full-year Phase166 cache.",
            },
            {
                "gate_id": "P168_FULL_YEAR_SCOPE",
                "passed": files_scanned >= 12,
                "observed_value": files_scanned,
                "required_value": ">=12 monthly cache files",
                "interpretation": "Phase167 used the full local Phase166 cache scope.",
            },
            {
                "gate_id": "P168_TRADE_LEDGER_PRESENT",
                "passed": trade_rows > 0,
                "observed_value": trade_rows,
                "required_value": ">0 trade rows",
                "interpretation": "The S08 closure is based on actual replay trades, not a dry verdict.",
            },
            {
                "gate_id": "P168_NO_POSITIVE_PROFILE_ROWS",
                "passed": positive_rows == 0,
                "observed_value": positive_rows,
                "required_value": "0",
                "interpretation": "No execution profile is positive after costs.",
            },
            {
                "gate_id": "P168_NO_CANDIDATE_PROFILE_ROWS",
                "passed": candidate_rows == 0,
                "observed_value": candidate_rows,
                "required_value": "0",
                "interpretation": "No profile passes the positive, coverage, stability and precision gates.",
            },
            {
                "gate_id": "P168_BEST_PROFILE_NEGATIVE",
                "passed": best_pnl < 0,
                "observed_value": best_pnl,
                "required_value": "<0 INR annual net P&L",
                "interpretation": "Even the best observed S08 profile is negative.",
            },
            {
                "gate_id": "P168_ALL_PROFILE_GATES_FAIL",
                "passed": all_gate_profiles_fail,
                "observed_value": int(all_gate_profiles_fail),
                "required_value": "1",
                "interpretation": "All Phase167 execution-profile gate rows fail.",
            },
            {
                "gate_id": "P168_PROMOTION_BOUNDARY_CLOSED",
                "passed": promotion_allowed == 0,
                "observed_value": promotion_allowed,
                "required_value": "0",
                "interpretation": "S08 closure must not promote a strategy.",
            },
            {
                "gate_id": "P168_BROKER_BOUNDARY_CLOSED",
                "passed": paper_allowed == 0,
                "observed_value": paper_allowed,
                "required_value": "0",
                "interpretation": "S08 closure must not claim broker/paper/live readiness.",
            },
            {
                "gate_id": "P168_DEPLOYABLE_CLAIM_CLOSED",
                "passed": deployable_allowed == 0,
                "observed_value": deployable_allowed,
                "required_value": "0",
                "interpretation": "S08 closure must not make a deployable profitability claim.",
            },
        ]
    )


def build_verdict(acceptance: pd.DataFrame, profile_summary: pd.DataFrame, gate_evaluation: pd.DataFrame) -> pd.DataFrame:
    all_closure_gates_pass = bool(gate_evaluation["passed"].astype(bool).all()) if not gate_evaluation.empty else False
    best = profile_summary.sort_values("annual_net_pnl_inr", ascending=False, kind="mergesort").head(1)
    best_profile = best["execution_profile"].iloc[0] if not best.empty else "none"
    best_pnl = float(best["annual_net_pnl_inr"].iloc[0]) if not best.empty else 0.0
    outcome = "A_S08_CURRENT_FORM_FALSIFIED" if all_closure_gates_pass else "REVIEW_REQUIRED"
    decision = "close_s08_current_cross_symbol_lead_lag_form" if all_closure_gates_pass else "review_phase167_evidence_before_closure"
    next_action = "design_new_precommitted_non_blocklisted_hypothesis_or_wait_for_real_l2_anchor" if all_closure_gates_pass else "repair_phase167_evidence_or_rerun_verdict"
    return pd.DataFrame(
        [
            {
                "verdict_id": "phase168_s08_closure_verdict",
                "outcome": outcome,
                "decision": decision,
                "phase167_strategy_id": metric_value(acceptance, "phase167_strategy_id", "missing"),
                "phase167_trade_rows": to_int(metric_value(acceptance, "phase167_trade_rows", 0)),
                "phase167_positive_after_cost_profile_rows": to_int(metric_value(acceptance, "phase167_positive_after_cost_profile_rows", 0)),
                "phase167_candidate_profile_rows": to_int(metric_value(acceptance, "phase167_candidate_profile_rows", 0)),
                "best_execution_profile": best_profile,
                "best_annual_net_pnl_inr": best_pnl,
                "strategy_promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
                "next_best_action": next_action,
            }
        ]
    )


def build_blocklist_candidate(verdict: pd.DataFrame, profile_summary: pd.DataFrame) -> pd.DataFrame:
    best_pnl = float(verdict["best_annual_net_pnl_inr"].iloc[0])
    return pd.DataFrame(
        [
            {
                "blocked_family_id": "PHASE167_S08_CROSS_SYMBOL_LEAD_LAG_CONTINUATION",
                "source_strategy_id": "S08",
                "phase167_strategy_id": verdict["phase167_strategy_id"].iloc[0],
                "blocked_form": "fixed_score_threshold_0_42_market_sector_etf_lagged_depth_pressure_continuation",
                "best_execution_profile": verdict["best_execution_profile"].iloc[0],
                "best_annual_net_pnl_inr": best_pnl,
                "profile_rows": int(len(profile_summary)),
                "positive_after_cost_profile_rows": int(verdict["phase167_positive_after_cost_profile_rows"].iloc[0]),
                "candidate_profile_rows": int(verdict["phase167_candidate_profile_rows"].iloc[0]),
                "recommended_status": "block_current_phase167_s08_form" if str(verdict["outcome"].iloc[0]) == "A_S08_CURRENT_FORM_FALSIFIED" else "review_required",
                "unlock_condition": "new precommitted feature form, different label/execution contract, or real-anchor evidence; do not rerun this same S08 form shard-after-shard hoping for profit",
            }
        ]
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase168 S08 Closure Verdict",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase168 converts the Phase167 S08 full-year replay into a closure/blocklist decision.",
        "It does not run a new strategy, does not promote a signal, and does not claim paper/live or deployable readiness.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase168_s08_closure_verdict_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase168(phase167_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    acceptance = read_csv(phase167_dir / "phase167_s08_replay_acceptance_summary.csv")
    profile_summary = read_csv(phase167_dir / "phase167_s08_strategy_profile_summary.csv")
    gates = read_csv(phase167_dir / "phase167_s08_gate_evaluation.csv")
    gate_evaluation = build_gate_evaluation(acceptance, gates, profile_summary)
    verdict = build_verdict(acceptance, profile_summary, gate_evaluation)
    blocklist = build_blocklist_candidate(verdict, profile_summary)
    acceptance_summary = pd.DataFrame(
        [
            ("phase168_outcome", verdict["outcome"].iloc[0], "Selected Phase168 outcome"),
            ("phase168_decision", verdict["decision"].iloc[0], "S08 current-form decision"),
            ("phase168_closure_gates_passed", int(gate_evaluation["passed"].astype(bool).sum()), "Closure gates passed"),
            ("phase168_closure_gates_total", int(len(gate_evaluation)), "Closure gates evaluated"),
            ("phase168_blocklist_rows", int(len(blocklist)), "Blocklist-candidate rows emitted"),
            ("phase168_best_annual_net_pnl_inr", verdict["best_annual_net_pnl_inr"].iloc[0], "Inherited best Phase167 annual net P&L"),
            ("phase168_strategy_promotion_allowed", 0, "Strategy promotion remains closed"),
            ("phase168_paper_or_live_acceptance_allowed", 0, "Paper/live broker acceptance remains closed"),
            ("phase168_deployable_profitability_claim_allowed", 0, "Deployable claim remains closed"),
            ("phase168_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Inherited Zerodha equity intraday NSE formula"),
            ("phase168_next_best_action", verdict["next_best_action"].iloc[0], "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    gate_evaluation.to_csv(output_dir / "phase168_s08_closure_gate_evaluation.csv", index=False)
    verdict.to_csv(output_dir / "phase168_s08_closure_verdict.csv", index=False)
    blocklist.to_csv(output_dir / "phase168_s08_blocklist_candidate_update.csv", index=False)
    acceptance_summary.to_csv(output_dir / "phase168_s08_closure_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance_summary,
            "Verdict": verdict,
            "Closure Gate Evaluation": gate_evaluation,
            "Blocklist Candidate Update": blocklist,
            "Phase167 Profile Summary": profile_summary,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase168_s08_closure_verdict",
        **reproducibility_fields(
            artifact_id="phase168_s08_closure_verdict",
            generated_utc=generated_utc,
            inputs={
                "phase167_acceptance_summary": str(phase167_dir / "phase167_s08_replay_acceptance_summary.csv"),
                "phase167_profile_summary": str(phase167_dir / "phase167_s08_strategy_profile_summary.csv"),
                "phase167_gate_evaluation": str(phase167_dir / "phase167_s08_gate_evaluation.csv"),
            },
            parameters={
                "closure_policy": "close_if_full_year_trade_evidence_present_no_positive_profiles_no_candidates_and_boundaries_closed",
                "strategy_promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "gate_evaluation": str(output_dir / "phase168_s08_closure_gate_evaluation.csv"),
                "verdict": str(output_dir / "phase168_s08_closure_verdict.csv"),
                "blocklist_candidate_update": str(output_dir / "phase168_s08_blocklist_candidate_update.csv"),
                "acceptance_summary": str(output_dir / "phase168_s08_closure_acceptance_summary.csv"),
                "report": str(output_dir / "phase168_s08_closure_verdict_report.md"),
                "manifest": str(output_dir / "phase168_s08_closure_manifest.json"),
            },
            random_seed="none_deterministic_phase168_verdict",
            scenario_ids="phase167_s08_cross_symbol_full_year_replay",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase12_execution_profiles_v1_reused_for_phase167_bucket_latency",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase168_s08_closure_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase167-dir", type=Path, default=DEFAULT_PHASE167_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase168(args.phase167_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
