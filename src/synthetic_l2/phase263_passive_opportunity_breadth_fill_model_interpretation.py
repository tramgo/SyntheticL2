from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, metric_value, read_csv
from synthetic_l2.phase255_richer_raw_depth_feature_quality_interpretation import safe_float
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE262_DIR = Path("outputs/phase262")
DEFAULT_OUTPUT_DIR = Path("outputs/phase263")
SELECTED_NEXT_ROUTE = "P263_FULL_DEPTH_LIQUIDITY_SHOCK_ABSORPTION_EVENT_PRECOMMIT"


def metric_value_from_frame(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    return default if rows.empty else rows.iloc[0]


def build_failure_mode_ledger(summary: pd.DataFrame, variants: pd.DataFrame) -> pd.DataFrame:
    variant_rows = as_int(metric_value_from_frame(summary, "phase262_variant_rows", 0))
    full_depth = as_int(metric_value_from_frame(summary, "phase262_full_top_five_depth_variant_rows", 0))
    l2_l5 = as_int(metric_value_from_frame(summary, "phase262_depth_beyond_l1_variant_rows", 0))
    l1_only = as_int(metric_value_from_frame(summary, "phase262_l1_only_variant_rows", 0))
    positive_1x = as_int(metric_value_from_frame(summary, "phase262_cost100_positive_variant_rows", 0))
    positive_15x = as_int(metric_value_from_frame(summary, "phase262_cost150_positive_variant_rows", 0))
    positive_2x = as_int(metric_value_from_frame(summary, "phase262_cost200_positive_variant_rows", 0))
    survivors = as_int(metric_value_from_frame(summary, "phase262_survivor_candidate_rows", 0))
    best_rows = as_int(metric_value_from_frame(summary, "phase262_best_opportunity_rows", 0))
    best_symbols = as_int(metric_value_from_frame(summary, "phase262_best_symbols", 0))
    best_fill_rows = safe_float(metric_value_from_frame(summary, "phase262_best_realized_fill_equivalent_rows", 0.0), 0.0)
    best_1x = safe_float(metric_value_from_frame(summary, "phase262_best_cost100_expected_net_pnl_inr", 0.0), 0.0)
    best_2x = safe_float(metric_value_from_frame(summary, "phase262_best_cost200_expected_net_pnl_inr", 0.0), 0.0)
    nonzero_variants = int(variants["cost100_opportunity_rows"].astype(float).gt(0).sum()) if not variants.empty and "cost100_opportunity_rows" in variants else 0
    queue_survivors = int(variants["queue_adversity_survives"].astype(int).sum()) if not variants.empty and "queue_adversity_survives" in variants else 0
    nonfill_survivors = int(variants["nonfill_stress_survives"].astype(int).sum()) if not variants.empty and "nonfill_stress_survives" in variants else 0
    rows = [
        ("cost_stress_failure", f"positive_1x={positive_1x}; positive_1p5={positive_15x}; positive_2x={positive_2x}; best_2x={best_2x}", "hard", int(positive_15x == 0 and positive_2x == 0)),
        ("no_survivor_after_full_control_stack", f"survivors={survivors}", "hard", int(survivors == 0)),
        ("best_ranked_candidate_negative_even_at_base_cost", f"best_1x={best_1x}; best_2x={best_2x}", "hard", int(best_1x <= 0 and best_2x <= 0)),
        ("opportunity_and_fill_breadth_too_sparse", f"best_opportunities={best_rows}; best_symbols={best_symbols}; best_fill_equivalent={best_fill_rows}", "hard", int(best_rows < 30 or best_symbols < 8 or best_fill_rows < 5)),
        ("queue_and_nonfill_stress_not_survived", f"queue_surviving_variants={queue_survivors}; nonfill_surviving_variants={nonfill_survivors}", "hard", int(queue_survivors == 0 or nonfill_survivors == 0)),
        ("positive_base_edge_not_robust", f"positive_1x={positive_1x}; nonzero_variants={nonzero_variants}; total_variants={variant_rows}", "medium", int(positive_1x > 0 and positive_2x == 0)),
        ("full_depth_surface_preserved_not_invalidated", f"full_depth={full_depth}; l2_l5={l2_l5}; l1_only={l1_only}; variants={variant_rows}", "important_context", int(full_depth == variant_rows and l2_l5 == variant_rows and l1_only == 0 and variant_rows > 0)),
    ]
    return pd.DataFrame(rows, columns=["failure_mode", "evidence", "severity", "closed_or_requires_repair"])


def build_decision_ledger(summary: pd.DataFrame) -> pd.DataFrame:
    variant_rows = as_int(metric_value_from_frame(summary, "phase262_variant_rows", 0))
    full_depth = as_int(metric_value_from_frame(summary, "phase262_full_top_five_depth_variant_rows", 0))
    l2_l5 = as_int(metric_value_from_frame(summary, "phase262_depth_beyond_l1_variant_rows", 0))
    l1_only = as_int(metric_value_from_frame(summary, "phase262_l1_only_variant_rows", 0))
    positive_1x = as_int(metric_value_from_frame(summary, "phase262_cost100_positive_variant_rows", 0))
    positive_2x = as_int(metric_value_from_frame(summary, "phase262_cost200_positive_variant_rows", 0))
    survivors = as_int(metric_value_from_frame(summary, "phase262_survivor_candidate_rows", 0))
    return pd.DataFrame(
        [
            ("close_phase262_for_promotion", int(survivors == 0), f"survivors={survivors}", "Do not promote Phase262 candidates"),
            ("close_passive_spread_capture_fill_model_route", int(survivors == 0 and positive_2x == 0), f"positive_1x={positive_1x}; positive_2x={positive_2x}; survivors={survivors}", "The repaired passive spread-capture/fill-model route is closed for now"),
            ("preserve_full_top_five_depth_surface", int(full_depth == variant_rows and l2_l5 == variant_rows and l1_only == 0 and variant_rows > 0), f"full_depth={full_depth}; l2_l5={l2_l5}; l1_only={l1_only}; variants={variant_rows}", "Full top-five L2 depth remains mandatory"),
            ("threshold_relaxation_only_allowed", 0, "two consecutive passive searches failed survivor/cost-stress gates", "Do not continue by merely relaxing passive thresholds"),
            ("materially_different_route_required", 1, "passive route failed after repair; full-depth signal surface still useful", "Open a different mechanism rather than another passive spread-capture tweak"),
            ("selected_next_route", SELECTED_NEXT_ROUTE, "full-depth liquidity shock / absorption event source", "Next materially different action"),
        ],
        columns=["decision_id", "decision_value", "evidence", "description"],
    )


def build_next_route_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("P264_INPUT", "outputs/phase254/phase254_richer_raw_top5_depth_event_bars.parquet", "Use existing richer raw Zerodha top-five event bars; no new download required"),
            ("P264_DEPTH_REQUIREMENT", "levels_1_to_5_required_l2_l5_required", "Use full top-five market-by-price rows 1-5 with explicit levels 2-5 features; L1-only variants forbidden"),
            ("P264_ROUTE", "full_depth_liquidity_shock_absorption_event_model", "Move from passive spread capture to directional liquidity-shock/absorption events"),
            ("P264_EVENT_FEATURES", "replenishment;withdrawal;top5_churn;order_churn;l2_l5_imbalance;spread_compression_expansion;level_weighted_imbalance", "Use depth dynamics rather than only static imbalance or bar return"),
            ("P264_LABELS", "future_mid_return_h3_h6_h10_cost_hurdled", "Evaluate directional continuation/reversal labels after realistic Zerodha cost floors"),
            ("P264_CONTROLS", "random_side;side_flip;cost_stress;shuffle_label;event_breadth;no_l1_only", "Controls required before any candidate can survive"),
            ("P264_FORBIDDEN", "paper_live_or_deployable_profitability_claim;threshold_relaxation_only", "No paper/live acceptance, deployable profitability claim, or mere passive-threshold relaxation"),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def decision_value(frame: pd.DataFrame, decision_id: str) -> str:
    rows = frame.loc[frame["decision_id"].astype(str).eq(decision_id), "decision_value"] if not frame.empty else pd.Series(dtype=str)
    return "" if rows.empty else str(rows.iloc[0])


def build_gate_evaluation(phase262_dir: Path, summary: pd.DataFrame, variants: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame) -> pd.DataFrame:
    next_action = str(metric_value(phase262_dir / "phase262_acceptance_summary.csv", "phase262_next_best_action", ""))
    variant_rows = as_int(metric_value_from_frame(summary, "phase262_variant_rows", 0))
    full_depth = as_int(metric_value_from_frame(summary, "phase262_full_top_five_depth_variant_rows", 0))
    l2_l5 = as_int(metric_value_from_frame(summary, "phase262_depth_beyond_l1_variant_rows", 0))
    l1_only = as_int(metric_value_from_frame(summary, "phase262_l1_only_variant_rows", 0))
    survivors = as_int(metric_value_from_frame(summary, "phase262_survivor_candidate_rows", 0))
    positive_2x = as_int(metric_value_from_frame(summary, "phase262_cost200_positive_variant_rows", 0))
    rows = [
        ("P263_PHASE262_WORK_ORDER_PRESENT", "run_phase263_passive_opportunity_breadth_fill_model_interpretation" in next_action, next_action, "Phase262 next action targets Phase263", "hard"),
        ("P263_PHASE262_SEARCH_EXECUTED", variant_rows > 0 and len(variants) == variant_rows, f"summary={variant_rows};rows={len(variants)}", "Phase262 variants present", "hard"),
        ("P263_NO_SURVIVOR_RECOGNIZED", survivors == 0, survivors, "0 Phase262 survivors", "hard"),
        ("P263_NO_2X_COST_POSITIVE_RECOGNIZED", positive_2x == 0, positive_2x, "0 variants positive at 2x costs", "hard"),
        ("P263_FULL_DEPTH_PRESERVED", full_depth == variant_rows and l2_l5 == variant_rows and l1_only == 0 and variant_rows > 0, f"full_depth={full_depth};l2_l5={l2_l5};l1_only={l1_only};variants={variant_rows}", "all variants full-depth and no L1-only", "hard"),
        ("P263_PASSIVE_ROUTE_CLOSED", decision_value(decisions, "close_passive_spread_capture_fill_model_route") == "1", decision_value(decisions, "close_passive_spread_capture_fill_model_route"), "passive route closed for now", "hard"),
        ("P263_NEXT_ROUTE_SELECTED", int(route["contract_id"].astype(str).eq("P264_ROUTE").sum()) == 1, SELECTED_NEXT_ROUTE, "Phase264 next route contract written", "hard"),
        ("P263_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase263 Passive Opportunity Breadth and Fill-model Interpretation",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase263 interprets the Phase262 broadened passive opportunity/fill-model training search.",
        "It closes the repaired passive spread-capture/fill-model route for promotion because no variants survived breadth, cost-stress and control gates.",
        "It preserves the core Zerodha top-five depth objective and selects a materially different full-depth liquidity-shock/absorption event route for Phase264.",
        "This is not replay execution, strategy promotion, paper/live acceptance or a deployable profitability claim.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase262_dir: Path = DEFAULT_PHASE262_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = read_csv(phase262_dir / "phase262_acceptance_summary.csv")
    variants = read_csv(phase262_dir / "phase262_passive_opportunity_variant_results.csv")
    if summary.empty:
        raise FileNotFoundError("Missing Phase262 acceptance summary.")
    failures = build_failure_mode_ledger(summary, variants)
    decisions = build_decision_ledger(summary)
    route = build_next_route_contract()
    gates = build_gate_evaluation(phase262_dir, summary, variants, decisions, route)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    next_action = (
        "run_phase264_full_depth_liquidity_shock_absorption_event_precommit_no_paper_live"
        if hard_pass == len(hard)
        else "repair_phase263_interpretation_before_next_route"
    )
    acceptance = pd.DataFrame(
        [
            ("phase263_interpretation_complete", 1, "Phase263 passive opportunity/fill-model interpretation completed"),
            ("phase263_phase262_variant_rows", as_int(metric_value_from_frame(summary, "phase262_variant_rows", 0)), "Phase262 variants interpreted"),
            ("phase263_phase262_full_depth_variant_rows", as_int(metric_value_from_frame(summary, "phase262_full_top_five_depth_variant_rows", 0)), "Full-depth variants interpreted"),
            ("phase263_phase262_l2_l5_variant_rows", as_int(metric_value_from_frame(summary, "phase262_depth_beyond_l1_variant_rows", 0)), "Levels 2-5 variants interpreted"),
            ("phase263_phase262_l1_only_variant_rows", as_int(metric_value_from_frame(summary, "phase262_l1_only_variant_rows", 0)), "L1-only variants interpreted"),
            ("phase263_phase262_cost100_positive_variant_rows", as_int(metric_value_from_frame(summary, "phase262_cost100_positive_variant_rows", 0)), "Phase262 variants positive at base charges"),
            ("phase263_phase262_cost200_positive_variant_rows", as_int(metric_value_from_frame(summary, "phase262_cost200_positive_variant_rows", 0)), "Phase262 variants positive at 2x charges"),
            ("phase263_phase262_survivor_candidate_rows", as_int(metric_value_from_frame(summary, "phase262_survivor_candidate_rows", 0)), "Phase262 survivors"),
            ("phase263_phase262_best_cost100_expected_net_pnl_inr", metric_value_from_frame(summary, "phase262_best_cost100_expected_net_pnl_inr", 0.0), "Best Phase262 1x expected net P&L"),
            ("phase263_phase262_best_cost200_expected_net_pnl_inr", metric_value_from_frame(summary, "phase262_best_cost200_expected_net_pnl_inr", 0.0), "Best Phase262 2x expected net P&L"),
            ("phase263_close_phase262_for_promotion", as_int(decision_value(decisions, "close_phase262_for_promotion"), 0), "Close Phase262 candidates for promotion"),
            ("phase263_close_passive_spread_capture_fill_model_route", as_int(decision_value(decisions, "close_passive_spread_capture_fill_model_route"), 0), "Close repaired passive route for now"),
            ("phase263_full_top_five_depth_preserved", as_int(decision_value(decisions, "preserve_full_top_five_depth_surface"), 0), "Preserve full top-five depth"),
            ("phase263_threshold_relaxation_only_allowed", as_int(decision_value(decisions, "threshold_relaxation_only_allowed"), 1), "Threshold relaxation only remains forbidden"),
            ("phase263_selected_next_route", SELECTED_NEXT_ROUTE, "Selected next route"),
            ("phase263_next_route_contract_rows", len(route), "Next route contract rows"),
            ("phase263_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase263_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase263_download_more_dates_now_allowed", 0, "No new download in Phase263"),
            ("phase263_replay_execution_allowed_now", 0, "No replay execution in Phase263"),
            ("phase263_strategy_promotion_allowed", 0, "No strategy promotion from Phase263"),
            ("phase263_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase263"),
            ("phase263_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase263"),
            ("phase263_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    failures.to_csv(output_dir / "phase263_failure_mode_ledger.csv", index=False)
    decisions.to_csv(output_dir / "phase263_decision_ledger.csv", index=False)
    route.to_csv(output_dir / "phase263_next_route_contract.csv", index=False)
    gates.to_csv(output_dir / "phase263_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase263_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase263_passive_opportunity_breadth_fill_model_interpretation_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Failure Mode Ledger": failures,
            "Decision Ledger": decisions,
            "Next Route Contract": route,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase263_passive_opportunity_breadth_fill_model_interpretation",
        **reproducibility_fields(
            artifact_id="phase263",
            generated_utc=generated_utc,
            inputs={"phase262_dir": str(phase262_dir)},
            parameters={
                "selected_next_route": SELECTED_NEXT_ROUTE,
                "close_passive_spread_capture_fill_model_route": 1,
                "full_top_five_depth_required": 1,
                "levels_2_to_5_materiality_required": 1,
                "l1_only_candidate_allowed": 0,
                "download_more_dates_now_allowed": 0,
                "replay_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "failure_mode_ledger": str(output_dir / "phase263_failure_mode_ledger.csv"),
                "decision_ledger": str(output_dir / "phase263_decision_ledger.csv"),
                "next_route_contract": str(output_dir / "phase263_next_route_contract.csv"),
                "gate_evaluation": str(output_dir / "phase263_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase263_acceptance_summary.csv"),
                "report": str(output_dir / "phase263_passive_opportunity_breadth_fill_model_interpretation_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase263_no_replay_decision_interpretation",
        ),
    }
    (output_dir / "phase263_passive_opportunity_breadth_fill_model_interpretation_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase263 passive opportunity breadth/fill-model interpretation.")
    parser.add_argument("--phase262-dir", type=Path, default=DEFAULT_PHASE262_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase262_dir=args.phase262_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
