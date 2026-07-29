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


DEFAULT_PHASE256_DIR = Path("outputs/phase256")
DEFAULT_OUTPUT_DIR = Path("outputs/phase257")
SELECTED_NEXT_ROUTE = "P257_PASSIVE_QUEUE_AWARE_SPREAD_CAPTURE_PRECOMMIT"


def classify_failure_modes(variants: pd.DataFrame, phase256_summary: pd.DataFrame) -> pd.DataFrame:
    best_cost100 = safe_float(metric_value_from_frame(phase256_summary, "phase256_best_cost100_net_pnl_inr", 0.0), 0.0)
    best_cost200 = safe_float(metric_value_from_frame(phase256_summary, "phase256_best_cost200_net_pnl_inr", 0.0), 0.0)
    survivor_rows = as_int(metric_value_from_frame(phase256_summary, "phase256_survivor_candidate_rows", 0))
    cost100_positive = as_int(metric_value_from_frame(phase256_summary, "phase256_cost100_positive_variant_rows", 0))
    rows = [
        {
            "failure_mode": "taker_cost_floor_dominates_gross_edge",
            "evidence": f"best_cost100_net={best_cost100}; best_cost200_net={best_cost200}; cost100_positive={cost100_positive}",
            "severity": "hard",
            "closed_by_phase257": int(best_cost100 <= 0 and cost100_positive == 0),
        },
        {
            "failure_mode": "no_cost_stress_survivor",
            "evidence": f"survivor_candidate_rows={survivor_rows}",
            "severity": "hard",
            "closed_by_phase257": int(survivor_rows == 0),
        },
        {
            "failure_mode": "best_candidate_too_sparse_for_breadth",
            "evidence": (
                f"best_trade_rows={metric_value_from_frame(phase256_summary, 'phase256_best_trade_rows', '')}; "
                f"best_symbols={metric_value_from_frame(phase256_summary, 'phase256_best_symbols', '')}"
            ),
            "severity": "medium",
            "closed_by_phase257": int(
                as_int(metric_value_from_frame(phase256_summary, "phase256_best_trade_rows", 0)) < 30
                or as_int(metric_value_from_frame(phase256_summary, "phase256_best_symbols", 0)) < 8
            ),
        },
        {
            "failure_mode": "full_depth_signal_not_invalidated",
            "evidence": "Phase255 found healthy_full_depth_features=11/11 and max_abs_full_depth_ic=0.1475390528147801",
            "severity": "important_context",
            "closed_by_phase257": 0,
        },
    ]
    if not variants.empty:
        gross_positive = int(variants["cost100_gross_pnl_inr"].gt(0).sum()) if "cost100_gross_pnl_inr" in variants else 0
        rows.append(
            {
                "failure_mode": "gross_edge_exists_but_is_insufficient",
                "evidence": f"gross_positive_variants={gross_positive}; net_positive_variants={cost100_positive}",
                "severity": "important_context",
                "closed_by_phase257": int(gross_positive > 0 and cost100_positive == 0),
            }
        )
    return pd.DataFrame(rows)


def metric_value_from_frame(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def build_decision_ledger(phase256_summary: pd.DataFrame, variants: pd.DataFrame) -> pd.DataFrame:
    variant_rows = as_int(metric_value_from_frame(phase256_summary, "phase256_variant_rows", 0))
    full_depth_rows = as_int(metric_value_from_frame(phase256_summary, "phase256_full_top_five_depth_variant_rows", 0))
    survivor_rows = as_int(metric_value_from_frame(phase256_summary, "phase256_survivor_candidate_rows", 0))
    cost100_positive = as_int(metric_value_from_frame(phase256_summary, "phase256_cost100_positive_variant_rows", 0))
    max_gross = safe_float(variants["cost100_gross_pnl_inr"].max(), 0.0) if not variants.empty and "cost100_gross_pnl_inr" in variants else 0.0
    max_cost = safe_float(variants["cost100_cost_inr"].max(), 0.0) if not variants.empty and "cost100_cost_inr" in variants else 0.0
    median_cost = safe_float(variants["cost100_cost_inr"].median(), 0.0) if not variants.empty and "cost100_cost_inr" in variants else 0.0
    return pd.DataFrame(
        [
            ("close_phase256_taker_threshold_search", int(variant_rows > 0 and survivor_rows == 0), f"variants={variant_rows}; survivors={survivor_rows}", "Close current taker-threshold search family"),
            ("preserve_full_top_five_depth_surface", int(full_depth_rows == variant_rows and variant_rows > 0), f"full_depth_rows={full_depth_rows}; variants={variant_rows}", "Keep levels 1-5 depth as core input"),
            ("do_not_repeat_threshold_relaxation_only", int(cost100_positive == 0), f"cost100_positive={cost100_positive}", "Avoid simply relaxing thresholds on same taker model"),
            ("cost_dominance_confirmed", int(max_gross < max_cost and median_cost > 0), f"max_gross={max_gross}; max_cost={max_cost}; median_cost={median_cost}", "Costs dominate the searched gross edge"),
            ("selected_next_route", SELECTED_NEXT_ROUTE, "passive/queue-aware route", "Next materially different route"),
        ],
        columns=["decision_id", "decision_value", "evidence", "description"],
    )


def build_next_route_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("P258_INPUT", "outputs/phase254/phase254_richer_raw_top5_depth_event_bars.parquet", "Use existing compact raw top-five depth event bars; no new download required"),
            ("P258_DEPTH_REQUIREMENT", "levels_1_to_5_required", "Use full Zerodha top-five market-by-price book; no L1-only candidate is allowed"),
            ("P258_ORDER_MODEL", "passive_queue_aware_limit_order_proxy", "Model quote placement, queue adversity, cancel/replace pressure and non-fill risk"),
            ("P258_EDGE_SOURCE", "spread_capture_minus_adverse_selection", "Shift from taker edge to passive spread capture and adverse-selection controls"),
            ("P258_COST_MODEL", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Carry modeled Zerodha charges; passive fill still pays statutory/brokerage cost stack"),
            ("P258_CONTROLS", "random_side;side_flip;cost_stress;queue_adversity", "Controls must remain active before any promotion"),
            ("P258_FORBIDDEN", "paper_live_or_deployable_profitability_claim", "No paper/live acceptance or deployable profitability claim from Phase257/P258 precommit"),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def build_gate_evaluation(phase256_dir: Path, summary: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame) -> pd.DataFrame:
    phase256_next = str(metric_value(phase256_dir / "phase256_acceptance_summary.csv", "phase256_next_best_action", ""))
    variant_rows = as_int(metric_value_from_frame(summary, "phase256_variant_rows", 0))
    survivor_rows = as_int(metric_value_from_frame(summary, "phase256_survivor_candidate_rows", 0))
    full_depth_rows = as_int(metric_value_from_frame(summary, "phase256_full_top_five_depth_variant_rows", 0))
    selected_rows = int(route["contract_id"].astype(str).eq("P258_ORDER_MODEL").sum()) if not route.empty else 0
    rows = [
        ("P257_PHASE256_WORK_ORDER_PRESENT", "run_phase257_richer_raw_top5_depth_strategy_search_interpretation" in phase256_next, phase256_next, "Phase256 next action targets Phase257", "hard"),
        ("P257_PHASE256_SEARCH_EXECUTED", variant_rows > 0, variant_rows, ">0 Phase256 variants available for interpretation", "hard"),
        ("P257_NO_SURVIVOR_RECOGNIZED", survivor_rows == 0, survivor_rows, "0 Phase256 survivors", "hard"),
        ("P257_FULL_DEPTH_PRESERVED", full_depth_rows == variant_rows and variant_rows > 0, f"{full_depth_rows}/{variant_rows}", "all interpreted variants used full top-five depth", "hard"),
        ("P257_TAKER_BRANCH_CLOSED", decision_value(decisions, "close_phase256_taker_threshold_search") == "1", decision_value(decisions, "close_phase256_taker_threshold_search"), "close taker threshold route", "hard"),
        ("P257_NEXT_ROUTE_SELECTED", selected_rows == 1, selected_rows, "passive/queue-aware route contract written", "hard"),
        ("P257_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def decision_value(frame: pd.DataFrame, decision_id: str) -> str:
    if frame.empty:
        return ""
    rows = frame.loc[frame["decision_id"].astype(str).eq(decision_id), "decision_value"]
    return "" if rows.empty else str(rows.iloc[0])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase257 Richer Raw Top-five Depth Strategy-search Interpretation",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase257 interprets the Phase256 full-depth cost-aware taker strategy search.",
        "It closes the current taker-threshold family after no survivor was found, while preserving the full Zerodha top-five depth surface as the core project input.",
        "It selects a passive/queue-aware spread-capture precommit as the next materially different route.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase256_dir: Path = DEFAULT_PHASE256_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = read_csv(phase256_dir / "phase256_acceptance_summary.csv")
    variants = read_csv(phase256_dir / "phase256_strategy_variant_results.csv")
    if summary.empty:
        raise FileNotFoundError("Missing Phase256 acceptance summary.")
    decisions = build_decision_ledger(summary, variants)
    failures = classify_failure_modes(variants, summary)
    route = build_next_route_contract()
    gates = build_gate_evaluation(phase256_dir, summary, decisions, route)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    next_action = (
        "run_phase258_passive_queue_aware_spread_capture_precommit_full_top5_depth_no_paper_live"
        if hard_pass == len(hard)
        else "repair_phase257_interpretation_before_next_route"
    )
    acceptance = pd.DataFrame(
        [
            ("phase257_interpretation_complete", 1, "Phase257 strategy-search interpretation completed"),
            ("phase257_phase256_variant_rows", as_int(metric_value_from_frame(summary, "phase256_variant_rows", 0)), "Phase256 variants interpreted"),
            ("phase257_phase256_full_depth_variant_rows", as_int(metric_value_from_frame(summary, "phase256_full_top_five_depth_variant_rows", 0)), "Full top-five depth variants interpreted"),
            ("phase257_phase256_survivor_candidate_rows", as_int(metric_value_from_frame(summary, "phase256_survivor_candidate_rows", 0)), "Phase256 survivor candidates"),
            ("phase257_phase256_cost100_positive_variant_rows", as_int(metric_value_from_frame(summary, "phase256_cost100_positive_variant_rows", 0)), "Phase256 variants positive at 1x cost"),
            ("phase257_closed_taker_threshold_route", as_int(decision_value(decisions, "close_phase256_taker_threshold_search"), 0), "Close current taker-threshold route"),
            ("phase257_full_top_five_depth_preserved", as_int(decision_value(decisions, "preserve_full_top_five_depth_surface"), 0), "Preserve full top-five depth as core surface"),
            ("phase257_threshold_relaxation_only_allowed", 0, "Do not continue by simple threshold relaxation"),
            ("phase257_selected_next_route", SELECTED_NEXT_ROUTE, "Selected materially different route"),
            ("phase257_next_route_contract_rows", len(route), "Next route contract rows"),
            ("phase257_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase257_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase257_download_more_dates_now_allowed", 0, "No new download in Phase257"),
            ("phase257_replay_execution_allowed_now", 0, "No replay execution in Phase257"),
            ("phase257_strategy_promotion_allowed", 0, "No strategy promotion from Phase257"),
            ("phase257_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase257"),
            ("phase257_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase257"),
            ("phase257_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    failures.to_csv(output_dir / "phase257_failure_mode_ledger.csv", index=False)
    decisions.to_csv(output_dir / "phase257_decision_ledger.csv", index=False)
    route.to_csv(output_dir / "phase257_next_route_contract.csv", index=False)
    gates.to_csv(output_dir / "phase257_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase257_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase257_richer_raw_top5_depth_strategy_search_interpretation_report.md",
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
        "scope": "phase257_richer_raw_top5_depth_strategy_search_interpretation",
        **reproducibility_fields(
            artifact_id="phase257",
            generated_utc=generated_utc,
            inputs={"phase256_dir": str(phase256_dir)},
            parameters={
                "selected_next_route": SELECTED_NEXT_ROUTE,
                "download_more_dates_now_allowed": 0,
                "replay_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "failure_mode_ledger": str(output_dir / "phase257_failure_mode_ledger.csv"),
                "decision_ledger": str(output_dir / "phase257_decision_ledger.csv"),
                "next_route_contract": str(output_dir / "phase257_next_route_contract.csv"),
                "gate_evaluation": str(output_dir / "phase257_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase257_acceptance_summary.csv"),
                "report": str(output_dir / "phase257_richer_raw_top5_depth_strategy_search_interpretation_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase257_no_replay_decision_interpretation",
        ),
    }
    (output_dir / "phase257_richer_raw_top5_depth_strategy_search_interpretation_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase257 richer raw top-five depth strategy-search interpretation.")
    parser.add_argument("--phase256-dir", type=Path, default=DEFAULT_PHASE256_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase256_dir=args.phase256_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
