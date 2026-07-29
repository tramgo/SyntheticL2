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


DEFAULT_PHASE259_DIR = Path("outputs/phase259")
DEFAULT_OUTPUT_DIR = Path("outputs/phase260")
SELECTED_NEXT_ROUTE = "P260_PASSIVE_OPPORTUNITY_BREADTH_AND_FILL_MODEL_REPAIR_PRECOMMIT"


def metric_value_from_frame(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    return default if rows.empty else rows.iloc[0]


def build_failure_mode_ledger(summary: pd.DataFrame, variants: pd.DataFrame) -> pd.DataFrame:
    positive_1x = as_int(metric_value_from_frame(summary, "phase259_cost100_positive_variant_rows", 0))
    positive_15x = as_int(metric_value_from_frame(summary, "phase259_cost150_positive_variant_rows", 0))
    positive_2x = as_int(metric_value_from_frame(summary, "phase259_cost200_positive_variant_rows", 0))
    survivors = as_int(metric_value_from_frame(summary, "phase259_survivor_candidate_rows", 0))
    best_rows = as_int(metric_value_from_frame(summary, "phase259_best_opportunity_rows", 0))
    best_symbols = as_int(metric_value_from_frame(summary, "phase259_best_symbols", 0))
    best_1x = safe_float(metric_value_from_frame(summary, "phase259_best_cost100_expected_net_pnl_inr", 0.0), 0.0)
    best_2x = safe_float(metric_value_from_frame(summary, "phase259_best_cost200_expected_net_pnl_inr", 0.0), 0.0)
    nonzero_variants = int(variants["cost100_opportunity_rows"].gt(0).sum()) if not variants.empty and "cost100_opportunity_rows" in variants else 0
    rows = [
        ("base_charge_edge_sparse", f"positive_1x={positive_1x}; best_1x={best_1x}; best_opportunities={best_rows}; best_symbols={best_symbols}", "hard", int(positive_1x > 0 and (best_rows < 30 or best_symbols < 8))),
        ("cost_stress_failure", f"positive_1p5={positive_15x}; positive_2x={positive_2x}; best_2x={best_2x}", "hard", int(positive_15x == 0 and positive_2x == 0)),
        ("no_survivor_after_controls", f"survivors={survivors}", "hard", int(survivors == 0)),
        ("opportunity_surface_too_sparse", f"nonzero_variant_rows={nonzero_variants}; total_variants={len(variants)}", "medium", int(nonzero_variants > 0 and nonzero_variants < len(variants) * 0.25)),
        ("full_depth_route_not_invalidated", "all Phase259 variants used full top-five depth and levels 2-5", "important_context", 0),
    ]
    return pd.DataFrame(rows, columns=["failure_mode", "evidence", "severity", "closed_or_requires_repair"])


def build_decision_ledger(summary: pd.DataFrame) -> pd.DataFrame:
    variants = as_int(metric_value_from_frame(summary, "phase259_variant_rows", 0))
    full_depth = as_int(metric_value_from_frame(summary, "phase259_full_top_five_depth_variant_rows", 0))
    positive_1x = as_int(metric_value_from_frame(summary, "phase259_cost100_positive_variant_rows", 0))
    positive_2x = as_int(metric_value_from_frame(summary, "phase259_cost200_positive_variant_rows", 0))
    survivors = as_int(metric_value_from_frame(summary, "phase259_survivor_candidate_rows", 0))
    return pd.DataFrame(
        [
            ("close_first_passive_search_for_promotion", int(survivors == 0), f"survivors={survivors}", "Do not promote Phase259 candidates"),
            ("do_not_close_full_passive_route_yet", int(positive_1x > 0 and positive_2x == 0), f"positive_1x={positive_1x}; positive_2x={positive_2x}", "Sparse base edge justifies one repair/broaden pass"),
            ("preserve_full_top_five_depth_surface", int(full_depth == variants and variants > 0), f"full_depth={full_depth}; variants={variants}", "Full top-five depth remains mandatory"),
            ("repair_opportunity_breadth_required", 1, "best opportunity and symbol breadth are too small", "Broaden passive opportunity surface before next search"),
            ("repair_fill_model_required", 1, "fill-equivalent rows are too sparse", "Separate opportunity generation from fill-probability model"),
            ("selected_next_route", SELECTED_NEXT_ROUTE, "passive repair/broaden route", "Next materially different action"),
        ],
        columns=["decision_id", "decision_value", "evidence", "description"],
    )


def build_next_route_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("P261_INPUT", "outputs/phase254/phase254_richer_raw_top5_depth_event_bars.parquet", "Use existing compact raw top-five depth event bars; no new download required"),
            ("P261_DEPTH_REQUIREMENT", "levels_1_to_5_required", "Use full Zerodha top-five market-by-price book; L1-only candidates remain forbidden"),
            ("P261_REPAIR_1", "separate_opportunity_filter_from_fill_probability", "Avoid filtering away most passive opportunities before fill model scores them"),
            ("P261_REPAIR_2", "calibrate_fill_probability_grid", "Search conservative fill haircuts and non-fill rates rather than one fixed formula"),
            ("P261_REPAIR_3", "broaden_spread_and_replenishment_thresholds", "Broaden opportunity count while retaining queue-adversity controls"),
            ("P261_CONTROLS", "random_side;side_flip;cost_stress;queue_adversity;nonfill_stress", "Controls required before any candidate can survive"),
            ("P261_FORBIDDEN", "paper_live_or_deployable_profitability_claim", "No paper/live acceptance or deployable profitability claim"),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def decision_value(frame: pd.DataFrame, decision_id: str) -> str:
    rows = frame.loc[frame["decision_id"].astype(str).eq(decision_id), "decision_value"] if not frame.empty else pd.Series(dtype=str)
    return "" if rows.empty else str(rows.iloc[0])


def build_gate_evaluation(phase259_dir: Path, summary: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame) -> pd.DataFrame:
    next_action = str(metric_value(phase259_dir / "phase259_acceptance_summary.csv", "phase259_next_best_action", ""))
    variants = as_int(metric_value_from_frame(summary, "phase259_variant_rows", 0))
    survivors = as_int(metric_value_from_frame(summary, "phase259_survivor_candidate_rows", 0))
    full_depth = as_int(metric_value_from_frame(summary, "phase259_full_top_five_depth_variant_rows", 0))
    rows = [
        ("P260_PHASE259_WORK_ORDER_PRESENT", "run_phase260_passive_queue_aware_spread_capture_interpretation" in next_action, next_action, "Phase259 next action targets Phase260", "hard"),
        ("P260_PHASE259_SEARCH_EXECUTED", variants > 0, variants, ">0 Phase259 variants", "hard"),
        ("P260_NO_SURVIVOR_RECOGNIZED", survivors == 0, survivors, "0 Phase259 survivors", "hard"),
        ("P260_FULL_DEPTH_PRESERVED", full_depth == variants and variants > 0, f"{full_depth}/{variants}", "all interpreted variants used full top-five depth", "hard"),
        ("P260_PROMOTION_CLOSED", decision_value(decisions, "close_first_passive_search_for_promotion") == "1", decision_value(decisions, "close_first_passive_search_for_promotion"), "no promotion from Phase259", "hard"),
        ("P260_NEXT_ROUTE_SELECTED", int(route["contract_id"].astype(str).eq("P261_REPAIR_1").sum()) == 1, SELECTED_NEXT_ROUTE, "repair/broaden contract written", "hard"),
        ("P260_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase260 Passive Queue-aware Spread-capture Interpretation",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase260 interprets the Phase259 passive/queue-aware training search.",
        "It closes Phase259 candidates for promotion because there are no survivors, but keeps the full-depth passive route open for one repair/broaden precommit because sparse base-charge edge exists.",
        "It does not download data, run replay execution, promote a strategy, open paper/live acceptance or claim deployable profitability.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase259_dir: Path = DEFAULT_PHASE259_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = read_csv(phase259_dir / "phase259_acceptance_summary.csv")
    variants = read_csv(phase259_dir / "phase259_passive_strategy_variant_results.csv")
    if summary.empty:
        raise FileNotFoundError("Missing Phase259 acceptance summary.")
    failures = build_failure_mode_ledger(summary, variants)
    decisions = build_decision_ledger(summary)
    route = build_next_route_contract()
    gates = build_gate_evaluation(phase259_dir, summary, decisions, route)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    next_action = (
        "run_phase261_passive_opportunity_breadth_fill_model_repair_precommit_full_top5_depth_no_paper_live"
        if hard_pass == len(hard)
        else "repair_phase260_interpretation_before_next_route"
    )
    acceptance = pd.DataFrame(
        [
            ("phase260_interpretation_complete", 1, "Phase260 passive search interpretation completed"),
            ("phase260_phase259_variant_rows", as_int(metric_value_from_frame(summary, "phase259_variant_rows", 0)), "Phase259 variants interpreted"),
            ("phase260_phase259_full_depth_variant_rows", as_int(metric_value_from_frame(summary, "phase259_full_top_five_depth_variant_rows", 0)), "Full-depth variants interpreted"),
            ("phase260_phase259_cost100_positive_variant_rows", as_int(metric_value_from_frame(summary, "phase259_cost100_positive_variant_rows", 0)), "Phase259 variants positive at base charges"),
            ("phase260_phase259_cost200_positive_variant_rows", as_int(metric_value_from_frame(summary, "phase259_cost200_positive_variant_rows", 0)), "Phase259 variants positive at 2x charges"),
            ("phase260_phase259_survivor_candidate_rows", as_int(metric_value_from_frame(summary, "phase259_survivor_candidate_rows", 0)), "Phase259 survivors"),
            ("phase260_phase259_best_opportunity_rows", as_int(metric_value_from_frame(summary, "phase259_best_opportunity_rows", 0)), "Best Phase259 opportunity rows"),
            ("phase260_close_phase259_for_promotion", as_int(decision_value(decisions, "close_first_passive_search_for_promotion"), 0), "Close Phase259 candidates for promotion"),
            ("phase260_full_passive_route_closed", 0, "Do not fully close passive route yet"),
            ("phase260_full_top_five_depth_preserved", as_int(decision_value(decisions, "preserve_full_top_five_depth_surface"), 0), "Preserve full top-five depth"),
            ("phase260_selected_next_route", SELECTED_NEXT_ROUTE, "Selected next route"),
            ("phase260_next_route_contract_rows", len(route), "Next route contract rows"),
            ("phase260_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase260_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase260_download_more_dates_now_allowed", 0, "No new download in Phase260"),
            ("phase260_replay_execution_allowed_now", 0, "No replay execution in Phase260"),
            ("phase260_strategy_promotion_allowed", 0, "No strategy promotion from Phase260"),
            ("phase260_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase260"),
            ("phase260_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase260"),
            ("phase260_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    failures.to_csv(output_dir / "phase260_failure_mode_ledger.csv", index=False)
    decisions.to_csv(output_dir / "phase260_decision_ledger.csv", index=False)
    route.to_csv(output_dir / "phase260_next_route_contract.csv", index=False)
    gates.to_csv(output_dir / "phase260_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase260_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase260_passive_queue_aware_spread_capture_interpretation_report.md",
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
        "scope": "phase260_passive_queue_aware_spread_capture_interpretation",
        **reproducibility_fields(
            artifact_id="phase260",
            generated_utc=generated_utc,
            inputs={"phase259_dir": str(phase259_dir)},
            parameters={
                "selected_next_route": SELECTED_NEXT_ROUTE,
                "download_more_dates_now_allowed": 0,
                "replay_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "failure_mode_ledger": str(output_dir / "phase260_failure_mode_ledger.csv"),
                "decision_ledger": str(output_dir / "phase260_decision_ledger.csv"),
                "next_route_contract": str(output_dir / "phase260_next_route_contract.csv"),
                "gate_evaluation": str(output_dir / "phase260_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase260_acceptance_summary.csv"),
                "report": str(output_dir / "phase260_passive_queue_aware_spread_capture_interpretation_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase260_no_replay_decision_interpretation",
        ),
    }
    (output_dir / "phase260_passive_queue_aware_spread_capture_interpretation_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase260 passive queue-aware spread-capture interpretation.")
    parser.add_argument("--phase259-dir", type=Path, default=DEFAULT_PHASE259_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase259_dir=args.phase259_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
