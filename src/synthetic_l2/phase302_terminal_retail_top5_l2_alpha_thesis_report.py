from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE298_DIR = Path("outputs/phase298")
DEFAULT_PHASE299_DIR = Path("outputs/phase299")
DEFAULT_PHASE300_DIR = Path("outputs/phase300")
DEFAULT_PHASE301_DIR = Path("outputs/phase301")
DEFAULT_OUTPUT_DIR = Path("outputs/phase302")

SELECTED_VERDICT = "P302_RETAIL_TOP5_L2_ALPHA_THESIS_CLOSED_FOR_ACCEPTANCE"
NEXT_ACTION = "do_not_continue_retail_top5_l2_alpha_rescue_without_material_new_source_or_thesis"
REPAIR_ACTION = "repair_phase302_terminal_retail_top5_l2_alpha_thesis_report"


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def top_row(frame: pd.DataFrame, sort_cols: list[str], ascending: list[bool]) -> pd.Series:
    if frame.empty:
        return pd.Series(dtype=object)
    sortable = frame.copy()
    for col in sort_cols:
        if col in sortable.columns:
            sortable[col] = pd.to_numeric(sortable[col], errors="coerce").fillna(0.0)
    return sortable.sort_values(sort_cols, ascending=ascending, kind="mergesort").iloc[0]


def build_evidence_chain(
    phase298: pd.DataFrame,
    phase299: pd.DataFrame,
    phase300: pd.DataFrame,
    phase301: pd.DataFrame,
    phase301_kill: pd.DataFrame,
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "phase": 298,
                "evidence_role": "raw_top_five_market_by_price_depth_strategy_sweep",
                "key_observation": (
                    f"raw_events={metric_value(phase298, 'phase298_raw_event_rows', '')}; "
                    f"variants={metric_value(phase298, 'phase298_variant_rows', '')}; "
                    f"scenarios={metric_value(phase298, 'phase298_scenario_rows', '')}; "
                    f"best_annualized={metric_value(phase298, 'phase298_best_cost200_annualized_pct', '')}; "
                    f"best_events={metric_value(phase298, 'phase298_best_scheduled_event_rows', '')}"
                ),
                "acceptance_read": "Sparse directional clues preserved; direct acceptance closed.",
            },
            {
                "phase": 299,
                "evidence_role": "raw_dense_sweep_interpretation_and_passive_route_selection",
                "key_observation": (
                    f"directional_signal_seeds={metric_value(phase299, 'phase299_directional_signal_seed_rows', '')}; "
                    f"above12_below_30_events={metric_value(phase299, 'phase299_above12_below_30_event_variant_rows', '')}; "
                    f"passive_fill_required={metric_value(phase299, 'phase299_require_passive_fill_model', '')}; "
                    f"profitability_claim_allowed={metric_value(phase299, 'phase299_deployable_profitability_claim_allowed', '')}"
                ),
                "acceptance_read": "Only seed-level continuation allowed; no profitability claim.",
            },
            {
                "phase": 300,
                "evidence_role": "passive_aware_execution_hybrid_with_cost200_and_fixed_capital",
                "key_observation": (
                    f"scenarios={metric_value(phase300, 'phase300_scenario_rows', '')}; "
                    f"above12={metric_value(phase300, 'phase300_above12_scenario_rows', '')}; "
                    f"event_floor={metric_value(phase300, 'phase300_event_floor_scenario_rows', '')}; "
                    f"breadth={metric_value(phase300, 'phase300_breadth_met_scenario_rows', '')}; "
                    f"survivors={metric_value(phase300, 'phase300_cost200_acceptance_survivor_rows', '')}; "
                    f"kill_switch={metric_value(phase300, 'phase300_kill_switch_triggered', '')}"
                ),
                "acceptance_read": "Passive-aware rescue failed acceptance; sparse pockets remain diagnostic only.",
            },
            {
                "phase": 301,
                "evidence_role": "interpretation_and_kill_switch_audit",
                "key_observation": (
                    f"selected_outcome={metric_value(phase301, 'phase301_selected_outcome', '')}; "
                    f"terminal_report_required={metric_value(phase301, 'phase301_terminal_report_required', '')}; "
                    f"kill_switch_rows={len(phase301_kill)}; "
                    f"do_not_rescue={metric_value(phase301, 'phase301_do_not_rescue_with_more_filters', '')}"
                ),
                "acceptance_read": "Route is closed and must be reported as terminal for acceptance.",
            },
        ]
    )


def build_byproduct_catalog() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "byproduct_id": "P302_RAW_DENSE_TOP5_BOOK_STATE_LAKE",
                "classification": "reusable_infrastructure",
                "kept_for": "future material-new thesis work requiring tick-level top-five market-by-price depth",
                "not_kept_for": "rescuing the closed retail directional route",
            },
            {
                "byproduct_id": "P302_ZERODHA_COST200_MODEL",
                "classification": "reusable_cost_model",
                "kept_for": f"all future India NSE intraday tests using {ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION}",
                "not_kept_for": "weakening costs to create a survivor",
            },
            {
                "byproduct_id": "P302_PASSIVE_BACK_OF_QUEUE_FILL_HARNESS",
                "classification": "reusable_execution_model",
                "kept_for": "future limit-order experiments where passive fills are explicitly modeled",
                "not_kept_for": "assuming all passive orders fill at touch",
            },
            {
                "byproduct_id": "P302_ADVERSE_SELECTION_AND_FORCED_FLATTEN_AUDIT",
                "classification": "reusable_realism_guard",
                "kept_for": "detecting fragile maker-like edge that disappears after fill realism",
                "not_kept_for": "adding guardrails after results to hide losses",
            },
            {
                "byproduct_id": "P302_NEGATIVE_EVIDENCE_LEDGER",
                "classification": "research_memory",
                "kept_for": "preventing repeated shard-by-shard searches of the same falsified route",
                "not_kept_for": "claiming full-depth L2 can never contain alpha",
            },
        ]
    )


def build_closure_decision(phase300: pd.DataFrame, phase301: pd.DataFrame, best: pd.Series, broad: pd.Series) -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("selected_terminal_verdict", SELECTED_VERDICT, "Phase300/301 evidence has no acceptance survivor.", "close_tested_route"),
            ("closed_scope", "retail_directional_top_five_market_by_price_depth_alpha_with_passive_aware_rescue", "Scope is narrower than all possible L2 research.", "scope_boundary"),
            ("close_for_acceptance", 1, f"survivors={metric_value(phase300, 'phase300_cost200_acceptance_survivor_rows', '')}", "closed"),
            ("close_for_replay_or_promotion", 1, "replay=0;promotion=0;paper_live=0;profitability_claim=0", "closed"),
            ("do_not_continue_with_more_filters", 1, f"phase301_do_not_rescue={metric_value(phase301, 'phase301_do_not_rescue_with_more_filters', '')}", "closed"),
            ("best_sparse_pocket_preserved", best.get("scenario_id", ""), f"ann={best.get('mechanical_annualized_portfolio_return_pct', '')};events={best.get('scheduled_event_rows', '')}", "diagnostic_only"),
            ("broadest_case_preserved", broad.get("scenario_id", ""), f"ann={broad.get('mechanical_annualized_portfolio_return_pct', '')};events={broad.get('scheduled_event_rows', '')}", "diagnostic_only"),
            ("material_new_source_or_thesis_required", 1, "same-route rescue is closed", "required"),
            ("next_best_action", NEXT_ACTION, "terminal report complete", "next"),
        ],
        columns=["decision_id", "decision_value", "evidence", "decision_status"],
    )


def build_gate_evaluation(
    phase300: pd.DataFrame,
    phase301: pd.DataFrame,
    scenarios: pd.DataFrame,
    decisions: pd.DataFrame,
    evidence: pd.DataFrame,
    byproducts: pd.DataFrame,
) -> pd.DataFrame:
    replay = as_int(metric_value(phase301, "phase301_strategy_replay_allowed", 0))
    promotion = as_int(metric_value(phase301, "phase301_strategy_promotion_allowed", 0))
    paper = as_int(metric_value(phase301, "phase301_paper_or_live_acceptance_allowed", 0))
    claim = as_int(metric_value(phase301, "phase301_deployable_profitability_claim_allowed", 0))
    gates = [
        ("P302_PHASE301_TERMINAL_REQUIRED", as_int(metric_value(phase301, "phase301_terminal_report_required", 0)) == 1, metric_value(phase301, "phase301_terminal_report_required", ""), 1),
        ("P302_PHASE300_NO_ACCEPTANCE_SURVIVOR", as_int(metric_value(phase300, "phase300_cost200_acceptance_survivor_rows", 0)) == 0, metric_value(phase300, "phase300_cost200_acceptance_survivor_rows", ""), 0),
        ("P302_PHASE300_KILL_SWITCH_FIRED", as_int(metric_value(phase300, "phase300_kill_switch_triggered", 0)) == 1, metric_value(phase300, "phase300_kill_switch_triggered", ""), 1),
        ("P302_SCENARIOS_AUDITED", len(scenarios) > 0, len(scenarios), ">0"),
        ("P302_EVIDENCE_CHAIN_PRESENT", len(evidence) == 4, len(evidence), 4),
        ("P302_BYPRODUCTS_CATALOGED", len(byproducts) >= 5, len(byproducts), ">=5"),
        ("P302_BOUNDARIES_CLOSED", replay == 0 and promotion == 0 and paper == 0 and claim == 0, f"replay={replay};promotion={promotion};paper={paper};claim={claim}", "all_zero"),
        ("P302_TERMINAL_DECISION_PRESENT", str(decisions.loc[decisions["decision_id"].eq("selected_terminal_verdict"), "decision_value"].iloc[0]) == SELECTED_VERDICT, SELECTED_VERDICT, SELECTED_VERDICT),
        ("P302_MATERIAL_NEW_REQUIREMENT_PRESENT", str(decisions.loc[decisions["decision_id"].eq("material_new_source_or_thesis_required"), "decision_value"].iloc[0]) == "1", 1, 1),
        ("P302_NEXT_ACTION_PRESENT", str(decisions.loc[decisions["decision_id"].eq("next_best_action"), "decision_value"].iloc[0]) == NEXT_ACTION, NEXT_ACTION, NEXT_ACTION),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(
    phase300: pd.DataFrame,
    phase301: pd.DataFrame,
    scenarios: pd.DataFrame,
    decisions: pd.DataFrame,
    gates: pd.DataFrame,
    byproducts: pd.DataFrame,
    best: pd.Series,
    broad: pd.Series,
) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase302_terminal_report_complete", 1, "Phase302 terminal report completed"),
            ("phase302_selected_verdict", SELECTED_VERDICT, "Selected terminal verdict"),
            ("phase302_closed_scope", "retail_directional_top_five_market_by_price_depth_alpha_with_passive_aware_rescue", "Closed scope"),
            ("phase302_phase300_scenario_rows", metric_value(phase300, "phase300_scenario_rows", 0), "Phase300 scenarios summarized"),
            ("phase302_phase300_above12_scenario_rows", metric_value(phase300, "phase300_above12_scenario_rows", 0), "Above-12 diagnostic scenarios"),
            ("phase302_phase300_event_floor_scenario_rows", metric_value(phase300, "phase300_event_floor_scenario_rows", 0), "Event-floor scenarios"),
            ("phase302_phase300_breadth_met_scenario_rows", metric_value(phase300, "phase300_breadth_met_scenario_rows", 0), "Breadth scenarios"),
            ("phase302_phase300_cost200_acceptance_survivor_rows", metric_value(phase300, "phase300_cost200_acceptance_survivor_rows", 0), "Cost200 acceptance survivors"),
            ("phase302_phase300_kill_switch_triggered", metric_value(phase300, "phase300_kill_switch_triggered", 0), "Phase300 kill switch"),
            ("phase302_phase301_selected_outcome", metric_value(phase301, "phase301_selected_outcome", ""), "Phase301 outcome"),
            ("phase302_best_sparse_scenario_id", best.get("scenario_id", ""), "Best sparse diagnostic scenario"),
            ("phase302_best_sparse_annualized_pct", best.get("mechanical_annualized_portfolio_return_pct", ""), "Best sparse annualized diagnostic"),
            ("phase302_best_sparse_scheduled_event_rows", best.get("scheduled_event_rows", ""), "Best sparse events"),
            ("phase302_broadest_scenario_id", broad.get("scenario_id", ""), "Broadest scheduled scenario"),
            ("phase302_broadest_annualized_pct", broad.get("mechanical_annualized_portfolio_return_pct", ""), "Broadest annualized diagnostic"),
            ("phase302_broadest_scheduled_event_rows", broad.get("scheduled_event_rows", ""), "Broadest scheduled events"),
            ("phase302_byproduct_rows", len(byproducts), "Reusable by-products cataloged"),
            ("phase302_strategy_replay_allowed", 0, "No replay"),
            ("phase302_strategy_promotion_allowed", 0, "No promotion"),
            ("phase302_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase302_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase302_material_new_source_or_thesis_required", 1, "Required before continuing"),
            ("phase302_do_not_continue_same_route", 1, "Same-route rescue closed"),
            ("phase302_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase302_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase302_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(
    output_dir: Path,
    acceptance: pd.DataFrame,
    evidence: pd.DataFrame,
    byproducts: pd.DataFrame,
    decisions: pd.DataFrame,
    gates: pd.DataFrame,
) -> None:
    lines = [
        "# Phase302 Terminal Retail Top-Five Depth Alpha Thesis Report",
        "",
        "Phase302 closes the tested retail directional top-five market-by-price depth alpha route for acceptance.",
        "",
        "This is a scope-specific closure, not a claim that all top-five depth data is useless. The closed scope is the Phase298-Phase301 route: directional signals derived from raw tick-level top-five market-by-price book state, then rescued with passive-aware execution, Zerodha-style cost200 stress, fixed initial capital, queue/adverse-selection penalties, and forced flattening.",
        "",
        "## Verdict",
        "",
        _markdown_table(acceptance.loc[acceptance["metric"].isin([
            "phase302_selected_verdict",
            "phase302_closed_scope",
            "phase302_phase300_cost200_acceptance_survivor_rows",
            "phase302_phase300_kill_switch_triggered",
            "phase302_material_new_source_or_thesis_required",
            "phase302_next_best_action",
        ])]),
        "",
        "## Evidence chain",
        "",
        _markdown_table(evidence),
        "",
        "## Durable by-products",
        "",
        _markdown_table(byproducts),
        "",
        "## Closure decisions",
        "",
        _markdown_table(decisions),
        "",
        "## Gates",
        "",
        _markdown_table(gates),
        "",
        "## Boundary",
        "",
        "No replay, promotion, paper/live acceptance, or deployable profitability claim is opened by this report. Sparse annualized pockets are preserved as diagnostic clues only.",
    ]
    (output_dir / "phase302_terminal_retail_top5_l2_alpha_thesis_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    phase298_dir: Path = DEFAULT_PHASE298_DIR,
    phase299_dir: Path = DEFAULT_PHASE299_DIR,
    phase300_dir: Path = DEFAULT_PHASE300_DIR,
    phase301_dir: Path = DEFAULT_PHASE301_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase298 = read_csv(phase298_dir / "phase298_acceptance_summary.csv")
    phase299 = read_csv(phase299_dir / "phase299_acceptance_summary.csv")
    phase300 = read_csv(phase300_dir / "phase300_acceptance_summary.csv")
    scenarios = read_csv(phase300_dir / "phase300_execution_scenario_summary.csv")
    phase301 = read_csv(phase301_dir / "phase301_acceptance_summary.csv")
    phase301_kill = read_csv(phase301_dir / "phase301_kill_switch_audit.csv")

    best = top_row(scenarios, ["mechanical_annualized_portfolio_return_pct", "scheduled_event_rows"], [False, False])
    broad = top_row(scenarios, ["scheduled_event_rows", "mechanical_annualized_portfolio_return_pct"], [False, False])
    evidence = build_evidence_chain(phase298, phase299, phase300, phase301, phase301_kill)
    byproducts = build_byproduct_catalog()
    decisions = build_closure_decision(phase300, phase301, best, broad)
    gates = build_gate_evaluation(phase300, phase301, scenarios, decisions, evidence, byproducts)
    acceptance = build_acceptance(phase300, phase301, scenarios, decisions, gates, byproducts, best, broad)

    evidence.to_csv(output_dir / "phase302_evidence_chain.csv", index=False)
    byproducts.to_csv(output_dir / "phase302_byproduct_catalog.csv", index=False)
    decisions.to_csv(output_dir / "phase302_closure_decision.csv", index=False)
    decisions.to_csv(output_dir / "phase302_terminal_verdict_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase302_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase302_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, evidence, byproducts, decisions, gates)

    manifest = {
        "phase": 302,
        "generated_utc": generated_utc,
        "scope": "phase302_terminal_retail_top5_l2_alpha_thesis_report",
        "inputs": {
            "phase298_acceptance": str(phase298_dir / "phase298_acceptance_summary.csv"),
            "phase299_acceptance": str(phase299_dir / "phase299_acceptance_summary.csv"),
            "phase300_acceptance": str(phase300_dir / "phase300_acceptance_summary.csv"),
            "phase300_scenarios": str(phase300_dir / "phase300_execution_scenario_summary.csv"),
            "phase301_acceptance": str(phase301_dir / "phase301_acceptance_summary.csv"),
            "phase301_kill_switch": str(phase301_dir / "phase301_kill_switch_audit.csv"),
        },
        "outputs": {
            "acceptance": str(output_dir / "phase302_acceptance_summary.csv"),
            "report": str(output_dir / "phase302_terminal_retail_top5_l2_alpha_thesis_report.md"),
            "evidence_chain": str(output_dir / "phase302_evidence_chain.csv"),
            "byproducts": str(output_dir / "phase302_byproduct_catalog.csv"),
            "closure_decision": str(output_dir / "phase302_closure_decision.csv"),
            "gates": str(output_dir / "phase302_gate_evaluation.csv"),
        },
        **reproducibility_fields(
            artifact_id="phase302",
            generated_utc=generated_utc,
            inputs={
                "phase298_acceptance": str(phase298_dir / "phase298_acceptance_summary.csv"),
                "phase299_acceptance": str(phase299_dir / "phase299_acceptance_summary.csv"),
                "phase300_acceptance": str(phase300_dir / "phase300_acceptance_summary.csv"),
                "phase300_scenarios": str(phase300_dir / "phase300_execution_scenario_summary.csv"),
                "phase301_acceptance": str(phase301_dir / "phase301_acceptance_summary.csv"),
                "phase301_kill_switch": str(phase301_dir / "phase301_kill_switch_audit.csv"),
            },
            parameters={
                "selected_verdict": SELECTED_VERDICT,
                "next_action": NEXT_ACTION,
                "closed_scope": "retail_directional_top_five_market_by_price_depth_alpha_with_passive_aware_rescue",
            },
            outputs={"acceptance_summary": str(output_dir / "phase302_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase302_terminal_report_only",
        ),
    }
    (output_dir / "phase302_terminal_retail_top5_l2_alpha_thesis_report_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Phase302 terminal retail top-five L2 alpha thesis report.")
    parser.add_argument("--phase298-dir", type=Path, default=DEFAULT_PHASE298_DIR)
    parser.add_argument("--phase299-dir", type=Path, default=DEFAULT_PHASE299_DIR)
    parser.add_argument("--phase300-dir", type=Path, default=DEFAULT_PHASE300_DIR)
    parser.add_argument("--phase301-dir", type=Path, default=DEFAULT_PHASE301_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase298_dir, args.phase299_dir, args.phase300_dir, args.phase301_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
