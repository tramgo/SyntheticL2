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


DEFAULT_PHASE265_DIR = Path("outputs/phase265")
DEFAULT_OUTPUT_DIR = Path("outputs/phase266")
SELECTED_NEXT_ROUTE = "P266_FULL_DEPTH_LIQUIDITY_SHOCK_BREADTH_AND_SHUFFLE_ROBUSTNESS_REPAIR_PRECOMMIT"
MIN_EVENT_ROWS = 30
MIN_SYMBOLS = 8
MIN_DATES = 1
MIN_SHUFFLE_EDGE_INR = 100.0
MIN_COST200_AVG_NET_PER_EVENT_INR = 25.0


def metric_value_from_frame(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    return default if rows.empty else rows.iloc[0]


def best_variant(variants: pd.DataFrame) -> dict[str, Any]:
    if variants.empty:
        return {}
    ordered = variants.sort_values(
        ["survivor_candidate", "has_events", "cost200_net_pnl_inr", "cost150_net_pnl_inr", "cost100_net_pnl_inr"],
        ascending=[False, False, False, False, False],
        kind="mergesort",
    )
    return ordered.iloc[0].to_dict()


def build_failure_mode_ledger(summary: pd.DataFrame, variants: pd.DataFrame) -> pd.DataFrame:
    variant_rows = as_int(metric_value_from_frame(summary, "phase265_variant_rows", 0))
    full_depth = as_int(metric_value_from_frame(summary, "phase265_full_top_five_depth_variant_rows", 0))
    l2_l5 = as_int(metric_value_from_frame(summary, "phase265_depth_beyond_l1_variant_rows", 0))
    l1_only = as_int(metric_value_from_frame(summary, "phase265_l1_only_variant_rows", 0))
    positive_1x = as_int(metric_value_from_frame(summary, "phase265_cost100_positive_variant_rows", 0))
    positive_15x = as_int(metric_value_from_frame(summary, "phase265_cost150_positive_variant_rows", 0))
    positive_2x = as_int(metric_value_from_frame(summary, "phase265_cost200_positive_variant_rows", 0))
    survivors = as_int(metric_value_from_frame(summary, "phase265_survivor_candidate_rows", 0))
    best = best_variant(variants)
    best_cost100 = safe_float(best.get("cost100_net_pnl_inr", 0.0), 0.0)
    best_cost200 = safe_float(best.get("cost200_net_pnl_inr", 0.0), 0.0)
    best_cost200_avg = safe_float(best.get("cost200_avg_net_per_event", 0.0), 0.0)
    best_rows = as_int(best.get("cost100_event_rows", 0), 0)
    best_symbols = as_int(best.get("symbols", 0), 0)
    best_dates = as_int(best.get("trade_dates", 0), 0)
    shuffle_net = safe_float(best.get("shuffle_label_net_pnl_inr", 0.0), 0.0)
    shuffle_margin = best_cost100 - shuffle_net
    cost200_positive_rows = int(variants["cost200_net_pnl_inr"].gt(0).sum()) if not variants.empty else 0
    cost200_breadth_rows = int(
        (
            variants["cost200_net_pnl_inr"].gt(0)
            & variants["cost100_event_rows"].ge(MIN_EVENT_ROWS)
            & variants["symbols"].ge(MIN_SYMBOLS)
            & variants["trade_dates"].ge(MIN_DATES)
        ).sum()
    ) if not variants.empty else 0
    rows = [
        (
            "no_survivor_after_full_control_stack",
            f"survivors={survivors}",
            "hard",
            int(survivors == 0),
            "No Phase265 candidate can be promoted or replayed.",
        ),
        (
            "positive_2x_edge_exists_but_is_tiny_and_sparse",
            f"positive_1x={positive_1x}; positive_1p5={positive_15x}; positive_2x={positive_2x}; best_cost100={best_cost100}; best_cost200={best_cost200}; best_cost200_avg={best_cost200_avg}",
            "hard",
            int(positive_2x > 0 and best_cost200 > 0 and best_cost200_avg < MIN_COST200_AVG_NET_PER_EVENT_INR),
            "The best result is positive under 2x costs, but the remaining edge per event is too small to treat as robust.",
        ),
        (
            "best_candidate_breadth_fragile",
            f"best_events={best_rows}; best_symbols={best_symbols}; best_dates={best_dates}; required_events={MIN_EVENT_ROWS}; required_symbols={MIN_SYMBOLS}; required_dates={MIN_DATES}",
            "hard",
            int(best_rows < MIN_EVENT_ROWS or best_symbols < MIN_SYMBOLS or best_dates < MIN_DATES),
            "The lead pocket is too narrow for acceptance.",
        ),
        (
            "positive_2x_breadth_rows_absent",
            f"cost200_positive_rows={cost200_positive_rows}; cost200_positive_breadth_rows={cost200_breadth_rows}",
            "hard",
            int(cost200_positive_rows > 0 and cost200_breadth_rows == 0),
            "2x-positive rows do not survive breadth requirements.",
        ),
        (
            "shuffle_label_margin_not_economic",
            f"best_cost100={best_cost100}; shuffle_label_net={shuffle_net}; shuffle_margin={shuffle_margin}; required_margin={MIN_SHUFFLE_EDGE_INR}",
            "hard",
            int(shuffle_margin < MIN_SHUFFLE_EDGE_INR),
            "The lead row's shuffled-label separation is effectively not robust enough for acceptance.",
        ),
        (
            "full_depth_surface_preserved_not_invalidated",
            f"full_depth={full_depth}; l2_l5={l2_l5}; l1_only={l1_only}; variants={variant_rows}",
            "important_context",
            int(full_depth == variant_rows and l2_l5 == variant_rows and l1_only == 0 and variant_rows > 0),
            "Full top-five and levels 2-5 depth remain mandatory and were respected.",
        ),
    ]
    return pd.DataFrame(rows, columns=["failure_mode", "evidence", "severity", "closed_or_requires_repair", "interpretation"])


def build_decision_ledger(summary: pd.DataFrame, variants: pd.DataFrame) -> pd.DataFrame:
    variant_rows = as_int(metric_value_from_frame(summary, "phase265_variant_rows", 0))
    full_depth = as_int(metric_value_from_frame(summary, "phase265_full_top_five_depth_variant_rows", 0))
    l2_l5 = as_int(metric_value_from_frame(summary, "phase265_depth_beyond_l1_variant_rows", 0))
    l1_only = as_int(metric_value_from_frame(summary, "phase265_l1_only_variant_rows", 0))
    survivors = as_int(metric_value_from_frame(summary, "phase265_survivor_candidate_rows", 0))
    positive_2x = as_int(metric_value_from_frame(summary, "phase265_cost200_positive_variant_rows", 0))
    best = best_variant(variants)
    best_rows = as_int(best.get("cost100_event_rows", 0), 0)
    best_symbols = as_int(best.get("symbols", 0), 0)
    best_dates = as_int(best.get("trade_dates", 0), 0)
    full_depth_preserved = int(full_depth == variant_rows and l2_l5 == variant_rows and l1_only == 0 and variant_rows > 0)
    breadth_fragile = int(best_rows < MIN_EVENT_ROWS or best_symbols < MIN_SYMBOLS or best_dates < MIN_DATES)
    return pd.DataFrame(
        [
            ("close_phase265_for_promotion", int(survivors == 0), f"survivors={survivors}", "Do not promote Phase265 candidates."),
            ("close_phase265_for_replay", int(survivors == 0), f"survivors={survivors}", "Do not execute strategy replay from Phase265."),
            ("recognize_promising_but_unaccepted_2x_pocket", int(positive_2x > 0), f"positive_2x={positive_2x}; best={best.get('candidate_id', '')}", "Keep the mechanism alive as a research lead, not as an accepted strategy."),
            ("close_current_narrow_liquidity_shock_candidate", int(breadth_fragile == 1), f"best_events={best_rows}; best_symbols={best_symbols}; best_dates={best_dates}", "The current narrow pocket is closed for acceptance."),
            ("preserve_full_top_five_depth_surface", full_depth_preserved, f"full_depth={full_depth}; l2_l5={l2_l5}; l1_only={l1_only}; variants={variant_rows}", "Full top-five L2 depth remains the core project surface."),
            ("threshold_relaxation_only_allowed", 0, "positive pocket is sparse and shuffle-fragile", "Do not continue by merely loosening thresholds."),
            ("material_breadth_and_shuffle_robustness_repair_required", 1, "best candidate is 2x-positive but too sparse and economically weak versus shuffled-label control", "Next work must repair breadth and label/control robustness."),
            ("selected_next_route", SELECTED_NEXT_ROUTE, "full-depth breadth + shuffle-robustness repair precommit", "Next materially different action."),
        ],
        columns=["decision_id", "decision_value", "evidence", "description"],
    )


def build_next_route_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("P267_INPUT", "outputs/phase265/phase265_liquidity_shock_variant_results.csv plus outputs/phase254/phase254_richer_raw_top5_depth_event_bars.parquet", "Reuse current full-depth event-bar surface; no new download in the precommit."),
            ("P267_DEPTH_REQUIREMENT", "levels_1_to_5_required_l2_l5_required", "Every candidate must use top-five market-by-price rows 1-5 and material levels 2-5 evidence."),
            ("P267_FORBIDDEN", "l1_only;threshold_relaxation_only;paper_live_or_deployable_profitability_claim", "No L1-only route, no naked threshold loosening, and no paper/live/profitability acceptance."),
            ("P267_REPAIR_TARGET", "breadth_and_shuffle_robustness", "Repair the Phase265 failure by requiring broader events and economically material shuffled-label separation."),
            ("P267_EVENT_GENERALIZATION", "bid_absorption;ask_absorption;spread_compression_absorption;withdrawal_reversal;market_regime_confirmed_absorption", "Generalize the mechanism across full-depth families, not by only reusing the top row."),
            ("P267_ACCEPTANCE_FLOORS", "events>=30;symbols>=8;dates>=1;cost200_net>0;cost200_avg_net_per_event>=25;shuffle_margin>=100", "Training candidate floors before any future replay discussion."),
            ("P267_CONTROLS", "side_flip;random_side;shuffled_label_margin;cost_stress_1p5_2x;breadth;no_l1_only", "All controls must be explicit in the candidate ledger."),
            ("P267_NEXT_IF_FAILS", "close_liquidity_shock_absorption_route_or_require_more_unseen_real_dates", "If breadth/robustness repair fails, stop this route or use fresh unseen real dates rather than overfitting current date."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def decision_value(frame: pd.DataFrame, decision_id: str) -> str:
    rows = frame.loc[frame["decision_id"].astype(str).eq(decision_id), "decision_value"] if not frame.empty else pd.Series(dtype=str)
    return "" if rows.empty else str(rows.iloc[0])


def build_gate_evaluation(phase265_dir: Path, summary: pd.DataFrame, variants: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame) -> pd.DataFrame:
    next_action = str(metric_value(phase265_dir / "phase265_acceptance_summary.csv", "phase265_next_best_action", ""))
    variant_rows = as_int(metric_value_from_frame(summary, "phase265_variant_rows", 0))
    full_depth = as_int(metric_value_from_frame(summary, "phase265_full_top_five_depth_variant_rows", 0))
    l2_l5 = as_int(metric_value_from_frame(summary, "phase265_depth_beyond_l1_variant_rows", 0))
    l1_only = as_int(metric_value_from_frame(summary, "phase265_l1_only_variant_rows", 0))
    survivors = as_int(metric_value_from_frame(summary, "phase265_survivor_candidate_rows", 0))
    positive_2x = as_int(metric_value_from_frame(summary, "phase265_cost200_positive_variant_rows", 0))
    best = best_variant(variants)
    best_rows = as_int(best.get("cost100_event_rows", 0), 0)
    best_symbols = as_int(best.get("symbols", 0), 0)
    shuffle_margin = safe_float(best.get("cost100_net_pnl_inr", 0.0), 0.0) - safe_float(best.get("shuffle_label_net_pnl_inr", 0.0), 0.0)
    rows = [
        ("P266_PHASE265_WORK_ORDER_PRESENT", "run_phase266_full_depth_liquidity_shock_absorption_event_interpretation" in next_action, next_action, "Phase265 next action targets Phase266", "hard"),
        ("P266_PHASE265_SEARCH_EXECUTED", variant_rows > 0 and len(variants) == variant_rows, f"summary={variant_rows};rows={len(variants)}", "Phase265 variants present", "hard"),
        ("P266_FULL_DEPTH_RECOGNIZED", full_depth == variant_rows and l2_l5 == variant_rows and l1_only == 0 and variant_rows > 0, f"full_depth={full_depth};l2_l5={l2_l5};l1_only={l1_only};variants={variant_rows}", "all variants full-depth and no L1-only", "hard"),
        ("P266_NO_SURVIVOR_RECOGNIZED", survivors == 0, survivors, "0 Phase265 survivors", "hard"),
        ("P266_2X_POSITIVE_BUT_BREADTH_FRAGILE_RECOGNIZED", positive_2x > 0 and (best_rows < MIN_EVENT_ROWS or best_symbols < MIN_SYMBOLS), f"positive_2x={positive_2x};best_events={best_rows};best_symbols={best_symbols}", "2x-positive pocket must be treated as fragile", "hard"),
        ("P266_SHUFFLE_MARGIN_FRAGILITY_RECOGNIZED", shuffle_margin < MIN_SHUFFLE_EDGE_INR, shuffle_margin, f"shuffled-label separation too small: <{MIN_SHUFFLE_EDGE_INR}", "hard"),
        ("P266_NEXT_ROUTE_SELECTED", int(route["contract_id"].astype(str).eq("P267_REPAIR_TARGET").sum()) == 1 and decision_value(decisions, "selected_next_route") == SELECTED_NEXT_ROUTE, SELECTED_NEXT_ROUTE, "Phase267 repair route contract written", "hard"),
        ("P266_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase266 Full-depth Liquidity-shock Absorption Event Interpretation",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase266 interprets the Phase265 full-depth liquidity-shock/absorption training search.",
        "It keeps the core Zerodha top-five depth objective intact: rows 1-5 are required, levels 2-5 must be material, and L1-only variants remain forbidden.",
        "The Phase265 lead is treated as a promising but unaccepted research pocket because it is 2x-cost positive but breadth-fragile and economically weak versus shuffled-label control.",
        "This is not replay execution, strategy promotion, paper/live acceptance, or a deployable profitability claim.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase265_dir: Path = DEFAULT_PHASE265_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = read_csv(phase265_dir / "phase265_acceptance_summary.csv")
    variants = read_csv(phase265_dir / "phase265_liquidity_shock_variant_results.csv")
    if summary.empty:
        raise FileNotFoundError("Missing Phase265 acceptance summary.")
    if variants.empty:
        raise FileNotFoundError("Missing Phase265 variant results.")
    failures = build_failure_mode_ledger(summary, variants)
    decisions = build_decision_ledger(summary, variants)
    route = build_next_route_contract()
    gates = build_gate_evaluation(phase265_dir, summary, variants, decisions, route)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    best = best_variant(variants)
    next_action = (
        "run_phase267_full_depth_liquidity_shock_breadth_shuffle_robustness_repair_precommit_no_paper_live"
        if hard_pass == len(hard)
        else "repair_phase266_liquidity_shock_interpretation_before_next_route"
    )
    shuffle_margin = safe_float(best.get("cost100_net_pnl_inr", 0.0), 0.0) - safe_float(best.get("shuffle_label_net_pnl_inr", 0.0), 0.0)
    acceptance = pd.DataFrame(
        [
            ("phase266_interpretation_complete", 1, "Phase266 liquidity-shock interpretation completed"),
            ("phase266_phase265_variant_rows", as_int(metric_value_from_frame(summary, "phase265_variant_rows", 0)), "Phase265 variants interpreted"),
            ("phase266_phase265_full_depth_variant_rows", as_int(metric_value_from_frame(summary, "phase265_full_top_five_depth_variant_rows", 0)), "Full-depth variants interpreted"),
            ("phase266_phase265_l2_l5_variant_rows", as_int(metric_value_from_frame(summary, "phase265_depth_beyond_l1_variant_rows", 0)), "Levels 2-5 variants interpreted"),
            ("phase266_phase265_l1_only_variant_rows", as_int(metric_value_from_frame(summary, "phase265_l1_only_variant_rows", 0)), "L1-only variants interpreted"),
            ("phase266_phase265_cost100_positive_variant_rows", as_int(metric_value_from_frame(summary, "phase265_cost100_positive_variant_rows", 0)), "Phase265 variants positive at 1x charges"),
            ("phase266_phase265_cost150_positive_variant_rows", as_int(metric_value_from_frame(summary, "phase265_cost150_positive_variant_rows", 0)), "Phase265 variants positive at 1.5x charges"),
            ("phase266_phase265_cost200_positive_variant_rows", as_int(metric_value_from_frame(summary, "phase265_cost200_positive_variant_rows", 0)), "Phase265 variants positive at 2x charges"),
            ("phase266_phase265_survivor_candidate_rows", as_int(metric_value_from_frame(summary, "phase265_survivor_candidate_rows", 0)), "Phase265 survivors"),
            ("phase266_best_candidate_id", best.get("candidate_id", ""), "Best Phase265 candidate"),
            ("phase266_best_family_id", best.get("family_id", ""), "Best Phase265 family"),
            ("phase266_best_cost100_net_pnl_inr", best.get("cost100_net_pnl_inr", 0.0), "Best 1x-charge net P&L"),
            ("phase266_best_cost200_net_pnl_inr", best.get("cost200_net_pnl_inr", 0.0), "Best 2x-charge net P&L"),
            ("phase266_best_cost200_avg_net_per_event_inr", best.get("cost200_avg_net_per_event", 0.0), "Best 2x average net per event"),
            ("phase266_best_event_rows", best.get("cost100_event_rows", 0), "Best event rows"),
            ("phase266_best_symbols", best.get("symbols", 0), "Best symbol breadth"),
            ("phase266_best_trade_dates", best.get("trade_dates", 0), "Best date breadth"),
            ("phase266_best_shuffle_label_net_pnl_inr", best.get("shuffle_label_net_pnl_inr", 0.0), "Best shuffled-label net P&L"),
            ("phase266_best_shuffle_label_margin_inr", shuffle_margin, "Best 1x P&L minus shuffled-label P&L"),
            ("phase266_close_phase265_for_promotion", as_int(decision_value(decisions, "close_phase265_for_promotion"), 0), "Close Phase265 for promotion"),
            ("phase266_close_phase265_for_replay", as_int(decision_value(decisions, "close_phase265_for_replay"), 0), "Close Phase265 for replay"),
            ("phase266_recognize_promising_but_unaccepted_2x_pocket", as_int(decision_value(decisions, "recognize_promising_but_unaccepted_2x_pocket"), 0), "Recognize 2x-positive pocket as research lead only"),
            ("phase266_close_current_narrow_liquidity_shock_candidate", as_int(decision_value(decisions, "close_current_narrow_liquidity_shock_candidate"), 0), "Close narrow candidate for acceptance"),
            ("phase266_full_top_five_depth_preserved", as_int(decision_value(decisions, "preserve_full_top_five_depth_surface"), 0), "Preserve full top-five depth"),
            ("phase266_threshold_relaxation_only_allowed", as_int(decision_value(decisions, "threshold_relaxation_only_allowed"), 1), "Threshold relaxation only remains forbidden"),
            ("phase266_selected_next_route", SELECTED_NEXT_ROUTE, "Selected next route"),
            ("phase266_next_route_contract_rows", len(route), "Next route contract rows"),
            ("phase266_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase266_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase266_download_more_dates_now_allowed", 0, "No new download in Phase266"),
            ("phase266_replay_execution_allowed_now", 0, "No replay execution in Phase266"),
            ("phase266_strategy_promotion_allowed", 0, "No strategy promotion from Phase266"),
            ("phase266_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase266"),
            ("phase266_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase266"),
            ("phase266_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    failures.to_csv(output_dir / "phase266_failure_mode_ledger.csv", index=False)
    decisions.to_csv(output_dir / "phase266_decision_ledger.csv", index=False)
    route.to_csv(output_dir / "phase266_next_route_contract.csv", index=False)
    gates.to_csv(output_dir / "phase266_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase266_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase266_full_depth_liquidity_shock_absorption_event_interpretation_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Failure Mode Ledger": failures,
            "Decision Ledger": decisions,
            "Next Route Contract": route,
            "Top Phase265 Variants": variants.head(20),
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase266_full_depth_liquidity_shock_absorption_event_interpretation",
        **reproducibility_fields(
            artifact_id="phase266",
            generated_utc=generated_utc,
            inputs={"phase265_dir": str(phase265_dir)},
            parameters={
                "selected_next_route": SELECTED_NEXT_ROUTE,
                "min_event_rows": MIN_EVENT_ROWS,
                "min_symbols": MIN_SYMBOLS,
                "min_dates": MIN_DATES,
                "min_shuffle_edge_inr": MIN_SHUFFLE_EDGE_INR,
                "min_cost200_avg_net_per_event_inr": MIN_COST200_AVG_NET_PER_EVENT_INR,
                "full_top_five_depth_required": 1,
                "levels_2_to_5_materiality_required": 1,
                "l1_only_candidate_allowed": 0,
                "threshold_relaxation_only_allowed": 0,
                "download_more_dates_now_allowed": 0,
                "replay_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "failure_mode_ledger": str(output_dir / "phase266_failure_mode_ledger.csv"),
                "decision_ledger": str(output_dir / "phase266_decision_ledger.csv"),
                "next_route_contract": str(output_dir / "phase266_next_route_contract.csv"),
                "gate_evaluation": str(output_dir / "phase266_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase266_acceptance_summary.csv"),
                "report": str(output_dir / "phase266_full_depth_liquidity_shock_absorption_event_interpretation_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase266_no_replay_decision_interpretation",
        ),
    }
    (output_dir / "phase266_full_depth_liquidity_shock_absorption_event_interpretation_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase266 full-depth liquidity-shock/absorption interpretation.")
    parser.add_argument("--phase265-dir", type=Path, default=DEFAULT_PHASE265_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase265_dir=args.phase265_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
