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


DEFAULT_PHASE248_DIR = Path("outputs/phase248")
DEFAULT_OUTPUT_DIR = Path("outputs/phase249")


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


def build_closure_ledger(phase248_dir: Path) -> pd.DataFrame:
    acceptance = phase248_dir / "phase248_acceptance_summary.csv"
    rows = [
        {
            "decision_id": "P249_CLOSE_SINGLE_NAME_BAR_RETURN_REVERSAL",
            "scope": "single_name_bar_return_reversal_with_top5_depth_filters",
            "decision": "closed_for_current_evidence_set",
            "observed_value": as_int(metric_value(acceptance, "phase248_survivor_candidate_rows", 0)),
            "required_value": ">0 controlled survivors",
            "rationale": "Phase248 found no controlled survivor after adding top-five imbalance, spread/liquidity, event-intensity and range/market guards.",
            "reuse_allowed_without_material_redesign": 0,
        },
        {
            "decision_id": "P249_BLOCK_THRESHOLD_RELAXATION_LOOP",
            "scope": "phase248_variant_thresholds",
            "decision": "blocked",
            "observed_value": as_int(metric_value(acceptance, "phase248_cost200_positive_variant_rows", 0)),
            "required_value": ">0 positive at 2x modeled costs",
            "rationale": "Relaxing thresholds after zero 2x-cost positives would optimize toward cost-fragile sparse artifacts.",
            "reuse_allowed_without_material_redesign": 0,
        },
        {
            "decision_id": "P249_NO_MORE_DOWNLOADS_FOR_CLOSED_BRANCH",
            "scope": "fresh_real_l2_dates",
            "decision": "blocked_for_closed_parent",
            "observed_value": as_int(metric_value(acceptance, "phase248_future_holdout_precommit_allowed", 0)),
            "required_value": "future_holdout_precommit_allowed=1",
            "rationale": "No candidate qualifies for fresh holdout, so more date downloads would spend disk without a testable frozen candidate.",
            "reuse_allowed_without_material_redesign": 0,
        },
    ]
    return pd.DataFrame(rows)


def build_failure_attribution(phase248_dir: Path) -> pd.DataFrame:
    acceptance = phase248_dir / "phase248_acceptance_summary.csv"
    gates = read_csv(phase248_dir / "phase248_gate_evaluation.csv")
    rows = [
        {
            "failure_mode": "cost_floor_dominates_l2_filtered_reversal",
            "observed_metric": "phase248_cost200_positive_variant_rows",
            "observed_value": as_int(metric_value(acceptance, "phase248_cost200_positive_variant_rows", 0)),
            "interpretation": "No combined-filter variant survived 2.0x modeled Zerodha costs.",
        },
        {
            "failure_mode": "sparse_positive_artifacts",
            "observed_metric": "phase248_best_trade_rows",
            "observed_value": as_int(metric_value(acceptance, "phase248_best_trade_rows", 0)),
            "interpretation": "Best apparent candidate had one trade, one date and one symbol, so it is not a strategy.",
        },
        {
            "failure_mode": "no_controlled_survivors",
            "observed_metric": "phase248_survivor_candidate_rows",
            "observed_value": as_int(metric_value(acceptance, "phase248_survivor_candidate_rows", 0)),
            "interpretation": "No candidate reached the control stage with sufficient cost-stress and breadth.",
        },
    ]
    for gate in gates.to_dict("records"):
        if str(gate.get("passed")).lower() != "true":
            rows.append(
                {
                    "failure_mode": f"gate_failed_{gate.get('gate_id')}",
                    "observed_metric": gate.get("gate_id", ""),
                    "observed_value": gate.get("observed_value", ""),
                    "interpretation": f"Gate failed against requirement {gate.get('required_value', '')}.",
                }
            )
    return pd.DataFrame(rows)


def build_broaden_queue() -> pd.DataFrame:
    rows = [
        {
            "priority": 1,
            "route_id": "P249_PAIR_OR_BASKET_RELATIVE_VALUE",
            "route": "pair_or_basket_relative_value",
            "why_materially_different": "Moves from single-name reversal to cross-sectional / market-neutral effects where common market shock is hedged.",
            "allowed_sources": "same existing real event bars plus symbol basket normalization; no new raw downloads",
            "precommit_next": "phase250_pair_basket_relative_value_precommit",
            "replay_allowed_now": 0,
        },
        {
            "priority": 2,
            "route_id": "P249_TOP5_DEPTH_PREDICTIVE_TARGET",
            "route": "top5_depth_as_predictive_target_or_source",
            "why_materially_different": "Uses L2 imbalance transitions as the signal source/target rather than only a filter around bar reversal.",
            "allowed_sources": "avg_top5_market_by_price_imbalance, avg_l1_imbalance, quote churn, depth refresh, future mid returns",
            "precommit_next": "phase250_top5_depth_predictive_target_precommit",
            "replay_allowed_now": 0,
        },
        {
            "priority": 3,
            "route_id": "P249_OPENING_SHOCK_SEPARATION",
            "route": "opening_shock_vs_normal_intraday_separation",
            "why_materially_different": "Separates open-auction shock/price-discovery behavior from normal intraday microstructure instead of mixing regimes.",
            "allowed_sources": "event-bar time buckets already available in Phase235/246 outputs",
            "precommit_next": "phase250_opening_shock_separation_precommit",
            "replay_allowed_now": 0,
        },
        {
            "priority": 4,
            "route_id": "P249_CONSERVATIVE_PASSIVE_FILL_MODEL",
            "route": "passive_limit_order_queue_model_only_if_fill_probability_conservative",
            "why_materially_different": "Tests whether maker-style execution can overcome taker cost drag, but only with pessimistic fill probability and adverse-selection controls.",
            "allowed_sources": "top-five market-by-price depth, spread, quote churn, depth refresh, stale quote duration",
            "precommit_next": "phase250_passive_fill_model_precommit",
            "replay_allowed_now": 0,
        },
    ]
    return pd.DataFrame(rows)


def build_guardrail_ledger() -> pd.DataFrame:
    rows = [
        ("P249_NO_PROFITABILITY_CLAIM", "No deployable profitability claim because Phase248 found zero survivors.", 1),
        ("P249_NO_MORE_DATE_DOWNLOAD", "No more fresh real L2 date downloads until a materially new frozen candidate exists.", 1),
        ("P249_NO_HOLDOUT_TUNING", "2026-07-17 and 2026-07-20 remain forbidden tuning dates for descendants.", 1),
        ("P249_NO_THRESHOLD_RELAXATION_ONLY", "Threshold relaxation alone is blocked; next route must be materially different.", 1),
        ("P249_COST_STRESS_FIRST_REMAINS", "2.0x modeled Zerodha cost positivity remains a first-class search objective.", 1),
        ("P249_RANDOM_SIDE_SIDE_FLIP_REMAIN", "Random-side and side-flip controls remain mandatory before holdout.", 1),
    ]
    return pd.DataFrame(rows, columns=["guardrail_id", "requirement", "active"])


def build_gate_evaluation(closure: pd.DataFrame, failures: pd.DataFrame, queue: pd.DataFrame, guardrails: pd.DataFrame, phase248_dir: Path) -> pd.DataFrame:
    next_action = str(metric_value(phase248_dir / "phase248_acceptance_summary.csv", "phase248_next_best_action", ""))
    rows = [
        ("P249_PHASE248_WORK_ORDER_PRESENT", "close_or_broaden_phase248" in next_action, next_action, "Phase248 next action asks close/broaden", "hard"),
        ("P249_CLOSURE_LEDGER_WRITTEN", len(closure) >= 3, len(closure), ">=3 closure rows", "hard"),
        ("P249_FAILURE_ATTRIBUTION_WRITTEN", len(failures) >= 3, len(failures), ">=3 failure attribution rows", "hard"),
        ("P249_MATERIAL_BROADEN_QUEUE_WRITTEN", len(queue) >= 3, len(queue), ">=3 materially different routes", "hard"),
        ("P249_GUARDRAILS_ACTIVE", bool((guardrails["active"].astype(int) == 1).all()), "all active", "all guardrails active", "hard"),
        ("P249_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase249 Close or Broaden After L2-filtered No-survivor Search",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase249 closes the current single-name bar-return reversal branch under the present evidence and opens only materially different research routes.",
        "It does not download data, rerun holdout dates, relax thresholds, promote a strategy, or open paper/live acceptance.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase248_dir: Path = DEFAULT_PHASE248_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    closure = build_closure_ledger(phase248_dir)
    failures = build_failure_attribution(phase248_dir)
    queue = build_broaden_queue()
    guardrails = build_guardrail_ledger()
    gates = build_gate_evaluation(closure, failures, queue, guardrails, phase248_dir)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    selected = queue.sort_values("priority").iloc[0].to_dict()
    next_action = "run_phase250_pair_basket_relative_value_precommit_no_downloads_no_2026_07_17_or_2026_07_20_tuning_no_paper_live"
    acceptance = pd.DataFrame(
        [
            ("phase249_close_or_broaden_complete", 1, "Phase249 close/broaden decision completed"),
            ("phase249_closed_scope", "single_name_bar_return_reversal_with_top5_depth_filters", "Scope closed under current evidence"),
            ("phase249_phase248_variant_rows", as_int(metric_value(phase248_dir / "phase248_acceptance_summary.csv", "phase248_variant_rows", 0)), "Phase248 variants considered"),
            ("phase249_phase248_cost200_positive_rows", as_int(metric_value(phase248_dir / "phase248_acceptance_summary.csv", "phase248_cost200_positive_variant_rows", 0)), "Phase248 2x-cost positive variants"),
            ("phase249_phase248_survivor_rows", as_int(metric_value(phase248_dir / "phase248_acceptance_summary.csv", "phase248_survivor_candidate_rows", 0)), "Phase248 controlled survivors"),
            ("phase249_closure_rows", len(closure), "Closure ledger rows"),
            ("phase249_failure_attribution_rows", len(failures), "Failure attribution rows"),
            ("phase249_broaden_queue_rows", len(queue), "Materially different broaden routes"),
            ("phase249_selected_next_route", selected.get("route_id", ""), "Highest-priority next route"),
            ("phase249_threshold_relaxation_only_allowed", 0, "No threshold relaxation loop"),
            ("phase249_download_more_dates_now_allowed", 0, "No raw-date download in Phase249"),
            ("phase249_replay_execution_allowed_now", 0, "No replay execution in Phase249"),
            ("phase249_strategy_promotion_allowed", 0, "No strategy promotion from Phase249"),
            ("phase249_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase249"),
            ("phase249_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase249"),
            ("phase249_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase249_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase249_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    closure.to_csv(output_dir / "phase249_closure_ledger.csv", index=False)
    failures.to_csv(output_dir / "phase249_failure_attribution.csv", index=False)
    queue.to_csv(output_dir / "phase249_material_broaden_queue.csv", index=False)
    guardrails.to_csv(output_dir / "phase249_guardrail_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase249_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase249_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase249_close_or_broaden_after_l2_filtered_no_survivor_report.md",
        {
            "Acceptance Summary": acceptance,
            "Closure Ledger": closure,
            "Failure Attribution": failures,
            "Material Broaden Queue": queue,
            "Guardrail Ledger": guardrails,
            "Gate Evaluation": gates,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase249_close_or_broaden_after_l2_filtered_no_survivor",
        **reproducibility_fields(
            artifact_id="phase249",
            generated_utc=generated_utc,
            inputs={"phase248_dir": str(phase248_dir)},
            parameters={
                "threshold_relaxation_only_allowed": 0,
                "download_more_dates_now_allowed": 0,
                "replay_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "closure_ledger": str(output_dir / "phase249_closure_ledger.csv"),
                "failure_attribution": str(output_dir / "phase249_failure_attribution.csv"),
                "material_broaden_queue": str(output_dir / "phase249_material_broaden_queue.csv"),
                "guardrail_ledger": str(output_dir / "phase249_guardrail_ledger.csv"),
                "gate_evaluation": str(output_dir / "phase249_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase249_acceptance_summary.csv"),
                "report": str(output_dir / "phase249_close_or_broaden_after_l2_filtered_no_survivor_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_decision_only",
        ),
    }
    (output_dir / "phase249_close_or_broaden_after_l2_filtered_no_survivor_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase249 close-or-broaden decision after Phase248 no-survivor search.")
    parser.add_argument("--phase248-dir", type=Path, default=DEFAULT_PHASE248_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase248_dir=args.phase248_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
