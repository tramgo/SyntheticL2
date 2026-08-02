from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase255_richer_raw_depth_feature_quality_interpretation import safe_float
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE277_DIR = Path("outputs/phase277")
DEFAULT_OUTPUT_DIR = Path("outputs/phase278")

SELECTED_NEXT_ROUTE = "P278_MATERIAL_NEW_TARGET_CONSTRUCTION_PRECOMMIT"
NEXT_ACTION = "run_phase279_material_new_target_construction_precommit_no_paper_live"
REPAIR_ACTION = "repair_phase278_cost_robust_redesign_interpretation"

ANNUALIZED_THRESHOLD_PCT = 12.0


def numeric(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = frame.copy()
    for col in columns:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0.0)
    return out


def build_ranked_interpretation(variant_summary: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    if variant_summary.empty:
        return pd.DataFrame()
    variants = numeric(
        variant_summary,
        [
            "cost200_above12_scenario_rows",
            "min_annualized_pct",
            "median_annualized_pct",
            "max_annualized_pct",
            "max_net_pnl_inr",
            "min_net_pnl_inr",
            "max_scheduled_event_rows",
            "above12_fraction",
            "median_above12",
            "worst_case_above12",
            "uses_top5",
            "uses_levels_2_to_5",
            "l1_only_variant",
        ],
    )
    rows: list[dict[str, Any]] = []
    for _, row in variants.iterrows():
        variant_id = str(row["phase277_variant_id"])
        scenario_rows = scenarios[scenarios["phase277_variant_id"].astype(str).eq(variant_id)] if not scenarios.empty else pd.DataFrame()
        best = scenario_rows.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0] if not scenario_rows.empty else pd.Series(dtype=object)
        max_ann = safe_float(row.get("max_annualized_pct", 0.0), 0.0)
        median_ann = safe_float(row.get("median_annualized_pct", 0.0), 0.0)
        rows.append(
            {
                "phase277_variant_id": variant_id,
                "redesign_family": row.get("redesign_family", ""),
                "feature_rule": row.get("feature_rule", ""),
                "scenario_rows": as_int(row.get("scenario_rows", 0)),
                "selected_event_rows": as_int(row.get("selected_event_rows", 0)),
                "cost200_above12_scenario_rows": as_int(row.get("cost200_above12_scenario_rows", 0)),
                "min_annualized_pct": safe_float(row.get("min_annualized_pct", 0.0), 0.0),
                "median_annualized_pct": median_ann,
                "max_annualized_pct": max_ann,
                "max_net_pnl_inr": safe_float(row.get("max_net_pnl_inr", 0.0), 0.0),
                "min_net_pnl_inr": safe_float(row.get("min_net_pnl_inr", 0.0), 0.0),
                "best_scenario_id": best.get("scenario_id", ""),
                "best_initial_capital_inr": best.get("initial_capital_inr", ""),
                "best_fixed_notional_inr": best.get("fixed_notional_inr", ""),
                "best_max_concurrent_positions": best.get("max_concurrent_positions", ""),
                "best_scheduled_event_rows": as_int(row.get("max_scheduled_event_rows", 0)),
                "uses_top5": as_int(row.get("uses_top5", 0)),
                "uses_levels_2_to_5": as_int(row.get("uses_levels_2_to_5", 0)),
                "l1_only_variant": as_int(row.get("l1_only_variant", 0)),
                "near_miss_under_12": int(0.0 < max_ann < ANNUALIZED_THRESHOLD_PCT),
                "material_clue": int(max_ann > 0.0 and as_int(row.get("l1_only_variant", 0)) == 0),
                "close_for_acceptance": int(as_int(row.get("cost200_above12_scenario_rows", 0)) == 0 and median_ann <= ANNUALIZED_THRESHOLD_PCT),
            }
        )
    ranked = pd.DataFrame(rows)
    return ranked.sort_values(
        ["material_clue", "cost200_above12_scenario_rows", "max_annualized_pct", "median_annualized_pct"],
        ascending=[False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_interpretation_ledger(summary: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    variants = as_int(metric_value(summary, "phase277_variant_rows", 0))
    scenarios = as_int(metric_value(summary, "phase277_scenario_rows", 0))
    above12 = as_int(metric_value(summary, "phase277_cost200_above12_scenario_rows", 0))
    best_ann = safe_float(metric_value(summary, "phase277_best_cost200_annualized_pct", 0.0), 0.0)
    l1_only = as_int(metric_value(summary, "phase277_l1_only_variant_rows", 0))
    material_clues = int(ranked["material_clue"].astype(int).sum()) if not ranked.empty else 0
    rows = [
        ("cost_robust_redesign_executed", f"variants={variants};scenarios={scenarios}", "evidence", int(variants > 0 and scenarios > 0), "Phase277 executed the intended redesign search."),
        ("cost200_acceptance_failed", f"cost200_above12={above12};best_ann={best_ann}", "hard_negative", int(above12 == 0 and best_ann < ANNUALIZED_THRESHOLD_PCT), "No cost200 redesign cleared the >12% diagnostic threshold."),
        ("best_filter_is_near_miss_not_survivor", f"best_ann={best_ann};threshold={ANNUALIZED_THRESHOLD_PCT}", "risk", int(0.0 < best_ann < ANNUALIZED_THRESHOLD_PCT), "The best replenishment/withdrawal clue is useful but below acceptance."),
        ("full_depth_boundary_preserved", f"l1_only={l1_only};material_clues={material_clues}", "constraint", int(l1_only == 0), "No L1-only fallback occurred; full-depth evidence remains central."),
        ("same_filter_family_should_close_for_acceptance", "cost200_median_above12=0;cost200_worst_case_above12=0", "decision", 1, "Do not keep iterating the same filter family for acceptance."),
        ("next_route_should_change_target_construction", SELECTED_NEXT_ROUTE, "next_action", 1, "Move to materially different target construction rather than relaxing cost stress."),
    ]
    return pd.DataFrame(rows, columns=["finding_id", "evidence", "severity", "finding_present", "interpretation"])


def build_decision_ledger(summary: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    top = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    above12 = as_int(metric_value(summary, "phase277_cost200_above12_scenario_rows", 0))
    best_ann = safe_float(metric_value(summary, "phase277_best_cost200_annualized_pct", 0.0), 0.0)
    return pd.DataFrame(
        [
            ("close_phase277_filter_redesign_for_acceptance", int(above12 == 0), f"cost200_above12={above12};best_ann={best_ann}", "Do not promote or continue this same filter route as accepted."),
            ("preserve_replenishment_withdrawal_clue", int(str(top.get("redesign_family", "")) == "depth_replenishment_withdrawal"), f"top_variant={top.get('phase277_variant_id', '')};max_ann={top.get('max_annualized_pct', '')}", "Keep the best full-depth clue for future feature construction."),
            ("do_not_relax_cost_threshold", 1, "cost200_required;threshold=12", "Do not downgrade acceptance to cost100 or below-12 cost200."),
            ("selected_next_route", SELECTED_NEXT_ROUTE, "filter redesign exhausted without cost200 survivor", "Precommit a materially new target construction."),
        ],
        columns=["decision_id", "decision_value", "evidence", "description"],
    )


def build_next_route_contract(ranked: pd.DataFrame) -> pd.DataFrame:
    top_clues = ranked[ranked["material_clue"].astype(int).eq(1)].head(5) if not ranked.empty else pd.DataFrame()
    clue_ids = ";".join(top_clues["phase277_variant_id"].astype(str).tolist()) if not top_clues.empty else ""
    return pd.DataFrame(
        [
            ("P279_INPUT", "outputs/phase277/phase277_cost_robust_redesign_variant_summary.csv;outputs/phase277/phase277_cost200_redesign_event_universe.csv", "Use Phase277 redesign evidence and event universe."),
            ("P279_PRESERVED_CLUES", clue_ids, "Preserve useful full-depth near-miss clues without accepting them."),
            ("P279_TARGET_CHANGE", "event_target_construction_not_filter_relaxation", "Change target construction rather than only tuning filters."),
            ("P279_REQUIRED_DIRECTIONS", "net_edge_distribution_shift;time_to_exit;adverse_selection_avoidance;depth_replenishment_confirmation;spread_cost_margin", "Explore materially different labels/targets around cost robustness."),
            ("P279_BOUNDARY", "no_paper_live;no_deployable_profitability_claim;full_depth_required;l1_only_forbidden", "Boundaries remain closed."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def decision_value(decisions: pd.DataFrame, decision_id: str) -> str:
    rows = decisions.loc[decisions["decision_id"].astype(str).eq(decision_id), "decision_value"] if not decisions.empty else pd.Series(dtype=str)
    return "" if rows.empty else str(rows.iloc[0])


def build_gate_evaluation(summary: pd.DataFrame, ranked: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame) -> pd.DataFrame:
    phase277_complete = as_int(metric_value(summary, "phase277_cost_robust_redesign_search_complete", 0))
    phase277_next = str(metric_value(summary, "phase277_next_best_action", ""))
    hard_pass = as_int(metric_value(summary, "phase277_hard_gate_pass_rows", 0))
    hard_rows = as_int(metric_value(summary, "phase277_hard_gate_rows", 0))
    replay_allowed = as_int(metric_value(summary, "phase277_strategy_replay_allowed", 1))
    paper_allowed = as_int(metric_value(summary, "phase277_paper_or_live_acceptance_allowed", 1))
    claim_allowed = as_int(metric_value(summary, "phase277_deployable_profitability_claim_allowed", 1))
    above12 = as_int(metric_value(summary, "phase277_cost200_above12_scenario_rows", 0))
    best_ann = safe_float(metric_value(summary, "phase277_best_cost200_annualized_pct", 0.0), 0.0)
    rows = [
        ("P278_PHASE277_WORK_ORDER_PRESENT", "run_phase278_cost_robust_redesign_interpretation" in phase277_next, phase277_next, "Phase277 next action targets Phase278", "hard"),
        ("P278_PHASE277_SEARCH_COMPLETE", phase277_complete == 1, phase277_complete, "Phase277 complete", "hard"),
        ("P278_PHASE277_HARD_GATES_PASS", hard_pass == hard_rows and hard_rows > 0, f"{hard_pass}/{hard_rows}", "Phase277 hard gates pass", "hard"),
        ("P278_RESULTS_PRESENT", len(ranked) > 0, len(ranked), "Phase277 variants interpreted", "hard"),
        ("P278_OUTCOME_CLASSIFIED_AS_NO_COST200_SURVIVOR", above12 == 0 and best_ann < ANNUALIZED_THRESHOLD_PCT, f"cost200_above12={above12};best_ann={best_ann}", "no accepted cost200 survivor", "hard"),
        ("P278_BOUNDARIES_CLOSED", replay_allowed == 0 and paper_allowed == 0 and claim_allowed == 0, f"replay={replay_allowed};paper={paper_allowed};claim={claim_allowed}", "no replay/paper/live/claim", "hard"),
        ("P278_NEXT_ROUTE_SELECTED", decision_value(decisions, "selected_next_route") == SELECTED_NEXT_ROUTE and int(route["contract_id"].astype(str).eq("P279_TARGET_CHANGE").sum()) == 1, SELECTED_NEXT_ROUTE, "Phase279 material target construction selected", "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def build_acceptance_summary(summary: pd.DataFrame, ranked: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    top = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    next_action = NEXT_ACTION if hard_pass == len(hard) else REPAIR_ACTION
    rows = [
        ("phase278_interpretation_complete", 1, "Phase278 cost-robust redesign interpretation completed"),
        ("phase278_selected_next_route", SELECTED_NEXT_ROUTE, "Selected next route"),
        ("phase278_phase277_variant_rows", as_int(metric_value(summary, "phase277_variant_rows", 0)), "Phase277 variants interpreted"),
        ("phase278_phase277_scenario_rows", as_int(metric_value(summary, "phase277_scenario_rows", 0)), "Phase277 scenarios interpreted"),
        ("phase278_phase277_cost200_above12_scenario_rows", as_int(metric_value(summary, "phase277_cost200_above12_scenario_rows", 0)), "Phase277 cost200 above-12 rows"),
        ("phase278_phase277_best_cost200_annualized_pct", metric_value(summary, "phase277_best_cost200_annualized_pct", ""), "Best Phase277 cost200 annualized diagnostic"),
        ("phase278_material_clue_variant_rows", int(ranked["material_clue"].astype(int).sum()) if not ranked.empty else 0, "Full-depth material clue rows"),
        ("phase278_close_filter_redesign_for_acceptance", 1, "Close Phase277 filter redesign for acceptance"),
        ("phase278_best_preserved_clue_variant", top.get("phase277_variant_id", ""), "Best preserved clue variant"),
        ("phase278_best_preserved_clue_family", top.get("redesign_family", ""), "Best preserved clue family"),
        ("phase278_do_not_relax_cost_threshold", 1, "Keep cost200 threshold"),
        ("phase278_strategy_replay_allowed", 0, "No strategy replay unlocked"),
        ("phase278_strategy_promotion_allowed", 0, "No strategy promotion unlocked"),
        ("phase278_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
        ("phase278_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        ("phase278_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase278_hard_gate_rows", len(hard), "Hard gates evaluated"),
        ("phase278_next_best_action", next_action, "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase278 Cost-robust Redesign Interpretation",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase278 interprets the Phase277 cost-robust full-depth redesign search.",
        "It closes the current filter-redesign route for acceptance and selects a materially new target-construction precommit.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase277_dir: Path = DEFAULT_PHASE277_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = read_csv(phase277_dir / "phase277_acceptance_summary.csv")
    variant_summary = read_csv(phase277_dir / "phase277_cost_robust_redesign_variant_summary.csv")
    scenarios = read_csv(phase277_dir / "phase277_cost_robust_redesign_scenario_results.csv")
    if summary.empty:
        raise FileNotFoundError("Missing Phase277 acceptance summary.")
    if variant_summary.empty:
        raise FileNotFoundError("Missing Phase277 variant summary.")
    ranked = build_ranked_interpretation(variant_summary, scenarios)
    interpretations = build_interpretation_ledger(summary, ranked)
    decisions = build_decision_ledger(summary, ranked)
    route = build_next_route_contract(ranked)
    gates = build_gate_evaluation(summary, ranked, decisions, route)
    acceptance = build_acceptance_summary(summary, ranked, gates)

    ranked.to_csv(output_dir / "phase278_ranked_cost_robust_redesign_interpretation.csv", index=False)
    interpretations.to_csv(output_dir / "phase278_interpretation_ledger.csv", index=False)
    decisions.to_csv(output_dir / "phase278_decision_ledger.csv", index=False)
    route.to_csv(output_dir / "phase278_next_route_contract.csv", index=False)
    gates.to_csv(output_dir / "phase278_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase278_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase278_cost_robust_redesign_interpretation_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Ranked Cost-robust Redesign Interpretation": ranked.head(20),
            "Interpretation Ledger": interpretations,
            "Decision Ledger": decisions,
            "Next Route Contract": route,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase278_cost_robust_redesign_interpretation",
        **reproducibility_fields(
            artifact_id="phase278",
            generated_utc=generated_utc,
            inputs={
                "phase277_acceptance_summary": str(phase277_dir / "phase277_acceptance_summary.csv"),
                "phase277_cost_robust_redesign_variant_summary": str(phase277_dir / "phase277_cost_robust_redesign_variant_summary.csv"),
                "phase277_cost_robust_redesign_scenario_results": str(phase277_dir / "phase277_cost_robust_redesign_scenario_results.csv"),
            },
            parameters={
                "selected_next_route": SELECTED_NEXT_ROUTE,
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "strategy_replay_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "ranked_cost_robust_redesign_interpretation": str(output_dir / "phase278_ranked_cost_robust_redesign_interpretation.csv"),
                "interpretation_ledger": str(output_dir / "phase278_interpretation_ledger.csv"),
                "decision_ledger": str(output_dir / "phase278_decision_ledger.csv"),
                "next_route_contract": str(output_dir / "phase278_next_route_contract.csv"),
                "gate_evaluation": str(output_dir / "phase278_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase278_acceptance_summary.csv"),
                "report": str(output_dir / "phase278_cost_robust_redesign_interpretation_report.md"),
                "manifest": str(output_dir / "phase278_cost_robust_redesign_interpretation_manifest.json"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase278_interpretation_only_no_new_replay",
        ),
    }
    (output_dir / "phase278_cost_robust_redesign_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase278 cost-robust redesign interpretation.")
    parser.add_argument("--phase277-dir", type=Path, default=DEFAULT_PHASE277_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase277_dir=args.phase277_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
