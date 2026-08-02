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


DEFAULT_PHASE280_DIR = Path("outputs/phase280")
DEFAULT_OUTPUT_DIR = Path("outputs/phase281")

SELECTED_NEXT_ROUTE = "P281_REGIME_CONDITIONED_FULL_DEPTH_ENSEMBLE_PRECOMMIT"
NEXT_ACTION = "run_phase282_regime_conditioned_full_depth_ensemble_precommit_no_paper_live"
REPAIR_ACTION = "repair_phase281_material_target_construction_interpretation"

ANNUALIZED_THRESHOLD_PCT = 12.0
MIN_EVENTS_FOR_ROBUST_PORTFOLIO_CLAIM = 30


def numeric(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = frame.copy()
    for col in columns:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0.0)
    return out


def build_ranked_variant_interpretation(scenarios: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame()
    frame = numeric(
        scenarios,
        [
            "mechanical_one_date_annualized_portfolio_return_pct",
            "realized_net_pnl_inr",
            "scheduled_event_rows",
            "selected_event_rows",
            "cost200_above12_diagnostic",
            "l1_only_variant",
            "uses_net_edge_as_live_mask",
            "uses_net_edge_as_offline_label",
            "initial_capital_inr",
            "fixed_notional_inr",
            "max_concurrent_positions",
        ],
    )
    rows: list[dict[str, Any]] = []
    for variant_id, group in frame.groupby("phase280_variant_id", dropna=False):
        ranked = group.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False)
        best = ranked.iloc[0]
        max_ann = safe_float(best.get("mechanical_one_date_annualized_portfolio_return_pct", 0.0), 0.0)
        max_events = int(group["scheduled_event_rows"].max())
        rows.append(
            {
                "phase280_variant_id": str(variant_id),
                "target_family_id": best.get("target_family_id", ""),
                "target_family": best.get("target_family", ""),
                "target_rule": best.get("target_rule", ""),
                "scenario_rows": int(len(group)),
                "selected_event_rows": int(group["selected_event_rows"].max()),
                "max_scheduled_event_rows": max_events,
                "cost200_above12_scenario_rows": int(group["cost200_above12_diagnostic"].sum()),
                "max_annualized_pct": max_ann,
                "median_annualized_pct": float(group["mechanical_one_date_annualized_portfolio_return_pct"].median()),
                "min_annualized_pct": float(group["mechanical_one_date_annualized_portfolio_return_pct"].min()),
                "max_net_pnl_inr": float(group["realized_net_pnl_inr"].max()),
                "best_scenario_id": best.get("scenario_id", ""),
                "best_initial_capital_inr": best.get("initial_capital_inr", ""),
                "best_fixed_notional_inr": best.get("fixed_notional_inr", ""),
                "best_max_concurrent_positions": best.get("max_concurrent_positions", ""),
                "uses_top5": as_int(best.get("uses_top5", 0)),
                "uses_levels_2_to_5": as_int(best.get("uses_levels_2_to_5", 0)),
                "l1_only_variant": as_int(best.get("l1_only_variant", 0)),
                "uses_net_edge_as_offline_label": as_int(best.get("uses_net_edge_as_offline_label", 0)),
                "uses_net_edge_as_live_mask": as_int(best.get("uses_net_edge_as_live_mask", 0)),
                "near_miss_under_12": int(0.0 < max_ann < ANNUALIZED_THRESHOLD_PCT),
                "too_sparse_for_portfolio_claim": int(max_events < MIN_EVENTS_FOR_ROBUST_PORTFOLIO_CLAIM),
                "material_full_depth_clue": int(max_ann > 0.0 and as_int(best.get("l1_only_variant", 0)) == 0 and as_int(best.get("uses_levels_2_to_5", 0)) == 1),
            }
        )
    ranked = pd.DataFrame(rows)
    return ranked.sort_values(
        ["material_full_depth_clue", "cost200_above12_scenario_rows", "max_annualized_pct", "max_scheduled_event_rows"],
        ascending=[False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_family_interpretation(family_summary: pd.DataFrame, ranked_variants: pd.DataFrame) -> pd.DataFrame:
    if family_summary.empty:
        return pd.DataFrame()
    fam = numeric(
        family_summary,
        [
            "scenario_rows",
            "variant_rows",
            "cost200_above12_scenario_rows",
            "min_annualized_pct",
            "median_annualized_pct",
            "max_annualized_pct",
            "max_net_pnl_inr",
            "max_scheduled_event_rows",
            "l1_only_variant_rows",
            "net_edge_live_mask_rows",
            "median_above12",
        ],
    )
    rows: list[dict[str, Any]] = []
    for _, row in fam.iterrows():
        family = str(row.get("target_family", ""))
        family_variants = ranked_variants[ranked_variants["target_family"].astype(str).eq(family)] if not ranked_variants.empty else pd.DataFrame()
        rows.append(
            {
                "target_family_id": row.get("target_family_id", ""),
                "target_family": family,
                "variant_rows": as_int(row.get("variant_rows", 0)),
                "scenario_rows": as_int(row.get("scenario_rows", 0)),
                "cost200_above12_scenario_rows": as_int(row.get("cost200_above12_scenario_rows", 0)),
                "min_annualized_pct": safe_float(row.get("min_annualized_pct", 0.0), 0.0),
                "median_annualized_pct": safe_float(row.get("median_annualized_pct", 0.0), 0.0),
                "max_annualized_pct": safe_float(row.get("max_annualized_pct", 0.0), 0.0),
                "max_net_pnl_inr": safe_float(row.get("max_net_pnl_inr", 0.0), 0.0),
                "max_scheduled_event_rows": as_int(row.get("max_scheduled_event_rows", 0)),
                "material_clue_variants": int(family_variants["material_full_depth_clue"].astype(int).sum()) if not family_variants.empty else 0,
                "near_miss_variants": int(family_variants["near_miss_under_12"].astype(int).sum()) if not family_variants.empty else 0,
                "close_family_for_acceptance": int(as_int(row.get("cost200_above12_scenario_rows", 0)) == 0),
                "preserve_for_ensemble_search": int(safe_float(row.get("max_annualized_pct", 0.0), 0.0) > 0.0),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["preserve_for_ensemble_search", "max_annualized_pct", "max_scheduled_event_rows"],
        ascending=[False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_interpretation_ledger(summary: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    scenario_rows = as_int(metric_value(summary, "phase280_scenario_rows", 0))
    above12 = as_int(metric_value(summary, "phase280_cost200_above12_scenario_rows", 0))
    best_ann = safe_float(metric_value(summary, "phase280_best_cost200_annualized_pct", 0.0), 0.0)
    best_events = as_int(metric_value(summary, "phase280_best_scheduled_event_rows", 0))
    l1_only = as_int(metric_value(summary, "phase280_l1_only_variant_rows", 0))
    leakage = as_int(metric_value(summary, "phase280_net_edge_live_mask_rows", 0))
    material_clues = int(ranked["material_full_depth_clue"].astype(int).sum()) if not ranked.empty else 0
    return pd.DataFrame(
        [
            ("phase280_executed", f"scenario_rows={scenario_rows}", "evidence", int(scenario_rows > 0), "Phase280 executed the target-construction search."),
            ("cost200_acceptance_failed", f"cost200_above12={above12};best_ann={best_ann}", "hard_negative", int(above12 == 0 and best_ann < ANNUALIZED_THRESHOLD_PCT), "No Phase280 target crossed the >12% cost200 diagnostic threshold."),
            ("near_miss_is_too_sparse", f"best_ann={best_ann};best_scheduled_events={best_events}", "risk", int(0.0 < best_ann < ANNUALIZED_THRESHOLD_PCT and best_events < MIN_EVENTS_FOR_ROBUST_PORTFOLIO_CLAIM), "The top clue is close but too sparse for a robust portfolio-return claim."),
            ("full_depth_boundary_preserved", f"l1_only={l1_only};live_label_leakage={leakage}", "constraint", int(l1_only == 0 and leakage == 0), "Full-depth and no-live-leakage constraints held."),
            ("material_clues_exist", f"material_clue_variants={material_clues}", "evidence", int(material_clues > 0), "Preserve useful L2 clues for a broader ensemble search."),
            ("same_target_construction_should_close_for_acceptance", "all_families_cost200_above12=0", "decision", 1, "Do not keep iterating the same Phase280 target masks for acceptance."),
            ("next_route_broadens_search_not_thresholds", SELECTED_NEXT_ROUTE, "next_action", 1, "Move to regime-conditioned full-depth ensembles instead of relaxing cost stress."),
        ],
        columns=["finding_id", "evidence", "severity", "finding_present", "interpretation"],
    )


def build_decision_ledger(summary: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    top = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    above12 = as_int(metric_value(summary, "phase280_cost200_above12_scenario_rows", 0))
    best_ann = safe_float(metric_value(summary, "phase280_best_cost200_annualized_pct", 0.0), 0.0)
    best_events = as_int(metric_value(summary, "phase280_best_scheduled_event_rows", 0))
    return pd.DataFrame(
        [
            ("close_phase280_target_construction_for_acceptance", int(above12 == 0), f"cost200_above12={above12};best_ann={best_ann}", "Do not accept or promote Phase280 target construction."),
            ("preserve_best_near_miss_full_depth_clue", top.get("phase280_variant_id", ""), f"family={top.get('target_family', '')};best_ann={top.get('max_annualized_pct', '')};scheduled_events={best_events}", "Keep the top full-depth clue as an ensemble seed."),
            ("do_not_relax_cost_threshold", 1, "cost200_required;threshold=12", "Do not downgrade acceptance to cost100 or below-12 cost200."),
            ("do_not_claim_portfolio_return", 1, f"best_scheduled_events={best_events};min_required={MIN_EVENTS_FOR_ROBUST_PORTFOLIO_CLAIM}", "Sparse diagnostic is not a robust annual portfolio claim."),
            ("selected_next_route", SELECTED_NEXT_ROUTE, "target construction near-miss without survivor", "Precommit a regime-conditioned full-depth ensemble search."),
        ],
        columns=["decision_id", "decision_value", "evidence", "description"],
    )


def build_next_route_contract(ranked: pd.DataFrame, families: pd.DataFrame) -> pd.DataFrame:
    top_clues = ranked[ranked["material_full_depth_clue"].astype(int).eq(1)].head(8) if not ranked.empty else pd.DataFrame()
    clue_ids = ";".join(top_clues["phase280_variant_id"].astype(str).tolist()) if not top_clues.empty else ""
    family_ids = ";".join(families[families["preserve_for_ensemble_search"].astype(int).eq(1)]["target_family_id"].astype(str).tolist()) if not families.empty else ""
    return pd.DataFrame(
        [
            ("P282_INPUTS", "outputs/phase280/phase280_material_target_scenario_results.csv;outputs/phase280/phase280_sample_material_target_scheduled_event_ledger.csv", "Use Phase280 scenarios and scheduled-event evidence."),
            ("P282_PRESERVED_CLUES", clue_ids, "Seed ensemble search with positive full-depth near-miss clues only as clues."),
            ("P282_PRESERVED_FAMILIES", family_ids, "Carry forward families with positive max annualized diagnostics."),
            ("P282_SEARCH_TYPE", "regime_conditioned_full_depth_ensemble", "Combine multiple full-depth L2 targets under regime/time/spread buckets."),
            ("P282_REQUIRED_DIRECTIONS", "regime_conditioning;family_ensemble;time_of_day_filter;spread_state_filter;event_count_floor;fixed_capital_cost200", "Broaden the search axis rather than relaxing cost stress."),
            ("P282_BOUNDARY", "no_paper_live;no_deployable_profitability_claim;full_depth_required;l1_only_forbidden;net_edge_live_mask_forbidden", "Boundaries remain closed."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def decision_value(decisions: pd.DataFrame, decision_id: str) -> str:
    rows = decisions.loc[decisions["decision_id"].astype(str).eq(decision_id), "decision_value"] if not decisions.empty else pd.Series(dtype=str)
    return "" if rows.empty else str(rows.iloc[0])


def build_gate_evaluation(summary: pd.DataFrame, ranked: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(summary, "phase280_material_new_target_construction_search_complete", 0))
    next_action = str(metric_value(summary, "phase280_next_best_action", ""))
    hard_pass = as_int(metric_value(summary, "phase280_hard_gate_pass_rows", 0))
    hard_rows = as_int(metric_value(summary, "phase280_hard_gate_rows", 0))
    replay_allowed = as_int(metric_value(summary, "phase280_strategy_replay_allowed", 1))
    paper_allowed = as_int(metric_value(summary, "phase280_paper_or_live_acceptance_allowed", 1))
    claim_allowed = as_int(metric_value(summary, "phase280_deployable_profitability_claim_allowed", 1))
    above12 = as_int(metric_value(summary, "phase280_cost200_above12_scenario_rows", 0))
    best_ann = safe_float(metric_value(summary, "phase280_best_cost200_annualized_pct", 0.0), 0.0)
    l1_only = as_int(metric_value(summary, "phase280_l1_only_variant_rows", 0))
    live_leakage = as_int(metric_value(summary, "phase280_net_edge_live_mask_rows", 0))
    rows = [
        ("P281_PHASE280_WORK_ORDER_PRESENT", "run_phase281_material_new_target_construction_interpretation" in next_action, next_action, "Phase280 next action targets Phase281", "hard"),
        ("P281_PHASE280_SEARCH_COMPLETE", complete == 1, complete, "Phase280 complete", "hard"),
        ("P281_PHASE280_HARD_GATES_PASS", hard_pass == hard_rows and hard_rows > 0, f"{hard_pass}/{hard_rows}", "Phase280 hard gates pass", "hard"),
        ("P281_RESULTS_PRESENT", len(ranked) > 0, len(ranked), "Phase280 variants interpreted", "hard"),
        ("P281_OUTCOME_CLASSIFIED_AS_NO_COST200_SURVIVOR", above12 == 0 and best_ann < ANNUALIZED_THRESHOLD_PCT, f"cost200_above12={above12};best_ann={best_ann}", "no accepted cost200 survivor", "hard"),
        ("P281_FULL_DEPTH_BOUNDARY_PRESERVED", l1_only == 0 and live_leakage == 0, f"l1_only={l1_only};live_leakage={live_leakage}", "full-depth/no-leakage preserved", "hard"),
        ("P281_BOUNDARIES_CLOSED", replay_allowed == 0 and paper_allowed == 0 and claim_allowed == 0, f"replay={replay_allowed};paper={paper_allowed};claim={claim_allowed}", "no replay/paper/live/claim", "hard"),
        ("P281_NEXT_ROUTE_SELECTED", decision_value(decisions, "selected_next_route") == SELECTED_NEXT_ROUTE and int(route["contract_id"].astype(str).eq("P282_SEARCH_TYPE").sum()) == 1, SELECTED_NEXT_ROUTE, "Phase282 ensemble precommit selected", "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def build_acceptance_summary(summary: pd.DataFrame, ranked: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    top = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    next_action = NEXT_ACTION if hard_pass == len(hard) else REPAIR_ACTION
    rows = [
        ("phase281_interpretation_complete", 1, "Phase281 material target-construction interpretation completed"),
        ("phase281_selected_next_route", SELECTED_NEXT_ROUTE, "Selected next route"),
        ("phase281_phase280_target_family_rows", as_int(metric_value(summary, "phase280_target_family_rows", 0)), "Phase280 target families interpreted"),
        ("phase281_phase280_variant_rows", as_int(metric_value(summary, "phase280_variant_rows", 0)), "Phase280 variants interpreted"),
        ("phase281_phase280_scenario_rows", as_int(metric_value(summary, "phase280_scenario_rows", 0)), "Phase280 scenarios interpreted"),
        ("phase281_phase280_cost200_above12_scenario_rows", as_int(metric_value(summary, "phase280_cost200_above12_scenario_rows", 0)), "Phase280 cost200 above-12 rows"),
        ("phase281_phase280_best_cost200_annualized_pct", metric_value(summary, "phase280_best_cost200_annualized_pct", ""), "Best Phase280 cost200 annualized diagnostic"),
        ("phase281_phase280_best_scheduled_event_rows", metric_value(summary, "phase280_best_scheduled_event_rows", ""), "Best Phase280 scheduled events"),
        ("phase281_material_clue_variant_rows", int(ranked["material_full_depth_clue"].astype(int).sum()) if not ranked.empty else 0, "Full-depth material clue rows"),
        ("phase281_near_miss_variant_rows", int(ranked["near_miss_under_12"].astype(int).sum()) if not ranked.empty else 0, "Near-miss variants below 12%"),
        ("phase281_close_phase280_for_acceptance", 1, "Close Phase280 target construction for acceptance"),
        ("phase281_best_preserved_clue_variant", top.get("phase280_variant_id", ""), "Best preserved clue variant"),
        ("phase281_best_preserved_clue_family", top.get("target_family", ""), "Best preserved clue family"),
        ("phase281_do_not_relax_cost_threshold", 1, "Keep cost200 threshold"),
        ("phase281_do_not_claim_portfolio_return", 1, "Sparse diagnostic is not a robust annual portfolio claim"),
        ("phase281_strategy_replay_allowed", 0, "No strategy replay unlocked"),
        ("phase281_strategy_promotion_allowed", 0, "No strategy promotion unlocked"),
        ("phase281_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
        ("phase281_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        ("phase281_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase281_hard_gate_rows", len(hard), "Hard gates evaluated"),
        ("phase281_next_best_action", next_action, "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase281 Material Target-construction Interpretation",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase281 interprets the Phase280 material target-construction search.",
        "It preserves the full-depth near-miss clue, closes the route for acceptance, and selects a broader regime-conditioned ensemble precommit.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase280_dir: Path = DEFAULT_PHASE280_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = read_csv(phase280_dir / "phase280_acceptance_summary.csv")
    family_summary = read_csv(phase280_dir / "phase280_material_target_family_summary.csv")
    scenarios = read_csv(phase280_dir / "phase280_material_target_scenario_results.csv")
    if summary.empty:
        raise FileNotFoundError("Missing Phase280 acceptance summary.")
    if family_summary.empty:
        raise FileNotFoundError("Missing Phase280 family summary.")
    if scenarios.empty:
        raise FileNotFoundError("Missing Phase280 scenario results.")
    ranked = build_ranked_variant_interpretation(scenarios)
    families = build_family_interpretation(family_summary, ranked)
    interpretations = build_interpretation_ledger(summary, ranked)
    decisions = build_decision_ledger(summary, ranked)
    route = build_next_route_contract(ranked, families)
    gates = build_gate_evaluation(summary, ranked, decisions, route)
    acceptance = build_acceptance_summary(summary, ranked, gates)

    ranked.to_csv(output_dir / "phase281_ranked_material_target_interpretation.csv", index=False)
    families.to_csv(output_dir / "phase281_family_interpretation.csv", index=False)
    interpretations.to_csv(output_dir / "phase281_interpretation_ledger.csv", index=False)
    decisions.to_csv(output_dir / "phase281_decision_ledger.csv", index=False)
    route.to_csv(output_dir / "phase281_next_route_contract.csv", index=False)
    gates.to_csv(output_dir / "phase281_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase281_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase281_material_target_construction_interpretation_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Ranked Variant Interpretation": ranked.head(20),
            "Family Interpretation": families,
            "Interpretation Ledger": interpretations,
            "Decision Ledger": decisions,
            "Next Route Contract": route,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase281_material_target_construction_interpretation",
        **reproducibility_fields(
            artifact_id="phase281",
            generated_utc=generated_utc,
            inputs={
                "phase280_acceptance_summary": str(phase280_dir / "phase280_acceptance_summary.csv"),
                "phase280_material_target_family_summary": str(phase280_dir / "phase280_material_target_family_summary.csv"),
                "phase280_material_target_scenario_results": str(phase280_dir / "phase280_material_target_scenario_results.csv"),
            },
            parameters={
                "selected_next_route": SELECTED_NEXT_ROUTE,
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "min_events_for_robust_portfolio_claim": MIN_EVENTS_FOR_ROBUST_PORTFOLIO_CLAIM,
                "strategy_replay_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "ranked_material_target_interpretation": str(output_dir / "phase281_ranked_material_target_interpretation.csv"),
                "family_interpretation": str(output_dir / "phase281_family_interpretation.csv"),
                "interpretation_ledger": str(output_dir / "phase281_interpretation_ledger.csv"),
                "decision_ledger": str(output_dir / "phase281_decision_ledger.csv"),
                "next_route_contract": str(output_dir / "phase281_next_route_contract.csv"),
                "gate_evaluation": str(output_dir / "phase281_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase281_acceptance_summary.csv"),
                "report": str(output_dir / "phase281_material_target_construction_interpretation_report.md"),
                "manifest": str(output_dir / "phase281_material_target_construction_interpretation_manifest.json"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase281_interpretation_only_no_new_replay",
        ),
    }
    (output_dir / "phase281_material_target_construction_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase281 material target-construction interpretation.")
    parser.add_argument("--phase280-dir", type=Path, default=DEFAULT_PHASE280_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase280_dir=args.phase280_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
