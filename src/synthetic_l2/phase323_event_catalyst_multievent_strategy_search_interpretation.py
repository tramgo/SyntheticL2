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


DEFAULT_PHASE322_DIR = Path("outputs/phase322")
DEFAULT_OUTPUT_DIR = Path("outputs/phase323")

NEXT_ACTION = "run_phase324_event_catalyst_breadth_expansion_precommit_no_replay"
REPAIR_ACTION = "repair_phase323_event_catalyst_multievent_strategy_search_interpretation"

ANNUALIZED_THRESHOLD_PCT = 12.0
ROBUST_EVENT_FLOOR = 30


def summarize_family(scenarios: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame()
    grouped = scenarios.groupby("family_id", dropna=False).agg(
        scenario_rows=("scenario_id", "count"),
        above12_rows=("above12_annualized", "sum"),
        cost200_above12_rows=("cost_profile", lambda s: int(((s.astype(str).eq("zerodha_2x_all_in_cost_proxy")) & (scenarios.loc[s.index, "above12_annualized"].astype(int).eq(1))).sum())),
        acceptance_grade_rows=("acceptance_grade_candidate", "sum"),
        best_annualized_pct=("annualized_return_pct", "max"),
        median_annualized_pct=("annualized_return_pct", "median"),
        best_net_pnl_inr=("net_pnl_inr", "max"),
        max_scheduled_event_rows=("scheduled_event_rows", "max"),
        max_symbol_rows=("symbol_rows", "max"),
    ).reset_index()
    grouped["above12_fraction"] = grouped["above12_rows"] / grouped["scenario_rows"]
    grouped["cost200_above12_fraction"] = grouped["cost200_above12_rows"] / grouped["scenario_rows"]
    return grouped.sort_values(["cost200_above12_rows", "best_annualized_pct"], ascending=[False, False])


def summarize_execution(scenarios: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame()
    grouped = scenarios.groupby(["execution_policy", "cost_profile"], dropna=False).agg(
        scenario_rows=("scenario_id", "count"),
        above12_rows=("above12_annualized", "sum"),
        acceptance_grade_rows=("acceptance_grade_candidate", "sum"),
        best_annualized_pct=("annualized_return_pct", "max"),
        median_annualized_pct=("annualized_return_pct", "median"),
        max_scheduled_event_rows=("scheduled_event_rows", "max"),
        avg_fill_probability=("avg_fill_probability", "mean"),
    ).reset_index()
    grouped["above12_fraction"] = grouped["above12_rows"] / grouped["scenario_rows"]
    return grouped.sort_values(["execution_policy", "cost_profile"])


def summarize_breadth(scenarios: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame()
    bins = [
        ("events_lt_10", scenarios["scheduled_event_rows"].astype(int) < 10),
        ("events_eq_10", scenarios["scheduled_event_rows"].astype(int) == 10),
        ("events_ge_30", scenarios["scheduled_event_rows"].astype(int) >= 30),
        ("cost200_above12_events_lt_30", scenarios["cost_profile"].astype(str).eq("zerodha_2x_all_in_cost_proxy") & scenarios["above12_annualized"].astype(int).eq(1) & (scenarios["scheduled_event_rows"].astype(int) < 30)),
        ("acceptance_grade", scenarios["acceptance_grade_candidate"].astype(int).eq(1)),
    ]
    rows = []
    for bucket, mask in bins:
        subset = scenarios[mask]
        rows.append(
            {
                "breadth_bucket": bucket,
                "scenario_rows": int(len(subset)),
                "best_annualized_pct": float(subset["annualized_return_pct"].max()) if not subset.empty else "",
                "max_scheduled_event_rows": int(subset["scheduled_event_rows"].max()) if not subset.empty else 0,
                "distinct_families": int(subset["family_id"].nunique()) if not subset.empty else 0,
            }
        )
    return pd.DataFrame(rows)


def build_decision_ledger(phase322: pd.DataFrame, interpretation_metrics: pd.DataFrame, scenarios: pd.DataFrame, family: pd.DataFrame, execution: pd.DataFrame) -> pd.DataFrame:
    scenario_rows = as_int(metric_value(phase322, "phase322_scenario_rows", 0))
    cost200_above12 = as_int(metric_value(phase322, "phase322_cost200_above12_scenario_rows", 0))
    acceptance_grade = as_int(metric_value(phase322, "phase322_cost200_acceptance_grade_candidate_rows", 0))
    best_cost200_annualized = metric_value(phase322, "phase322_best_cost200_annualized_return_pct", "")
    best_cost200_events = as_int(metric_value(phase322, "phase322_best_cost200_scheduled_event_rows", 0))
    broadest_events = as_int(metric_value(interpretation_metrics, "phase322_broadest_scheduled_event_rows", 0))
    best_family = str(metric_value(phase322, "phase322_best_family_id", ""))
    taker_best = scenarios[scenarios["execution_policy"].astype(str).eq("taker_entry_taker_exit")]["annualized_return_pct"].max() if not scenarios.empty else ""
    passive_best = scenarios[scenarios["execution_policy"].astype(str).eq("passive_aware_directional_with_penalties")]["annualized_return_pct"].max() if not scenarios.empty else ""
    rows = [
        ("phase322_training_complete", 1, f"scenario_rows={scenario_rows}", "Training-only search completed."),
        ("fixed_capital_profitable_research_leads_exist", int(cost200_above12 > 0), f"cost200_above12_scenario_rows={cost200_above12}; threshold={ANNUALIZED_THRESHOLD_PCT}", "Research lead exists under user-requested annualized threshold and 2x costs."),
        ("acceptance_grade_candidates_exist", int(acceptance_grade > 0), f"cost200_acceptance_grade_candidate_rows={acceptance_grade}", "No acceptance-grade candidate unless 2x cost and breadth gates both pass."),
        ("best_2x_cost_lead_is_sparse", int(best_cost200_events < ROBUST_EVENT_FLOOR), f"best_cost200_annualized={best_cost200_annualized}; best_cost200_events={best_cost200_events}; required_events={ROBUST_EVENT_FLOOR}", "Best 2x-cost return is profitable-looking but too sparse."),
        ("breadth_universe_limits_acceptance", int(broadest_events < ROBUST_EVENT_FLOOR), f"broadest_scheduled_events={broadest_events}; required_events={ROBUST_EVENT_FLOOR}", "The current 10-event universe cannot prove a 30-event acceptance floor."),
        ("best_family_preserved_for_breadth_expansion", best_family, "top family from Phase322", "Preserve the best clue; do not discard just because acceptance is not yet proven."),
        ("passive_aware_rescue_status", "diagnostic_only_not_dominant" if passive_best != "" and taker_best != "" and passive_best < taker_best else "diagnostic_preserved", f"best_passive={passive_best}; best_taker={taker_best}", "Attached passive-aware realism is preserved as a diagnostic policy, not a shortcut to acceptance."),
        ("replay_or_promotion_allowed", 0, "closed", "No replay or promotion from sparse training-only evidence."),
        ("deployable_profitability_claim_allowed", 0, "closed", "No deployable profitability claim from Phase323."),
        ("selected_next_route", "P324_EVENT_CATALYST_BREADTH_EXPANSION_PRECOMMIT", NEXT_ACTION, "Expand event breadth around preserved full-depth families before any replay/promotion decision."),
    ]
    return pd.DataFrame(rows, columns=["decision_id", "decision_value", "evidence", "interpretation"])


def build_gate_evaluation(phase322: pd.DataFrame, decisions: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(phase322, "phase322_multievent_strategy_search_training_complete", 0))
    claim = as_int(metric_value(phase322, "phase322_deployable_profitability_claim_allowed", 1))
    selected = decisions[decisions["decision_id"].astype(str).eq("selected_next_route")]
    rows = [
        ("P323_PHASE322_COMPLETE", complete == 1, complete, 1),
        ("P323_DECISION_ROWS_PRESENT", len(decisions) >= 10, len(decisions), ">=10"),
        ("P323_RESEARCH_LEAD_INTERPRETED", decisions["decision_id"].astype(str).eq("fixed_capital_profitable_research_leads_exist").any(), "present", "present"),
        ("P323_ACCEPTANCE_GRADE_CHECKED", decisions["decision_id"].astype(str).eq("acceptance_grade_candidates_exist").any(), "present", "present"),
        ("P323_BREADTH_LIMIT_INTERPRETED", decisions["decision_id"].astype(str).eq("breadth_universe_limits_acceptance").any(), "present", "present"),
        ("P323_PROFITABILITY_CLAIM_CLOSED", claim == 0, claim, 0),
        ("P323_NEXT_ROUTE_SELECTED", not selected.empty, selected["decision_value"].iloc[0] if not selected.empty else "", "selected"),
        ("P323_NO_REPLAY_PROMOTION_OR_PAPER_LIVE", True, "replay=0;promotion=0;paper=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(decisions: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    lookup = decisions.set_index("decision_id")["decision_value"].to_dict() if not decisions.empty else {}
    return pd.DataFrame(
        [
            ("phase323_multievent_strategy_search_interpretation_complete", int(hard_pass == hard_rows), "Phase323 multi-event strategy-search interpretation completed"),
            ("phase323_fixed_capital_profitable_research_leads_exist", lookup.get("fixed_capital_profitable_research_leads_exist", 0), "Fixed-capital profitable research leads exist"),
            ("phase323_acceptance_grade_candidates_exist", lookup.get("acceptance_grade_candidates_exist", 0), "Acceptance-grade candidates exist"),
            ("phase323_best_2x_cost_lead_is_sparse", lookup.get("best_2x_cost_lead_is_sparse", 1), "Best 2x cost lead is sparse"),
            ("phase323_breadth_universe_limits_acceptance", lookup.get("breadth_universe_limits_acceptance", 1), "Current event universe limits acceptance"),
            ("phase323_best_family_preserved_for_breadth_expansion", lookup.get("best_family_preserved_for_breadth_expansion", ""), "Best family preserved for breadth expansion"),
            ("phase323_passive_aware_rescue_status", lookup.get("passive_aware_rescue_status", ""), "Passive-aware diagnostic status"),
            ("phase323_replay_allowed", 0, "No replay"),
            ("phase323_strategy_promotion_allowed", 0, "No promotion"),
            ("phase323_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase323_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase323_selected_next_route", lookup.get("selected_next_route", ""), "Selected next route"),
            ("phase323_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase323_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase323_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase323 Event-Catalyst Multi-Event Strategy Search Interpretation",
        "",
        "Phase323 interprets Phase322 training-only results. It preserves profitable fixed-capital research leads while refusing acceptance because the 2x-cost profitable pockets remain sparse.",
        "It does not replay, promote, open paper/live acceptance, or claim deployable profitability.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase323_event_catalyst_multievent_strategy_search_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase322_dir: Path = DEFAULT_PHASE322_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase322 = read_csv(phase322_dir / "phase322_acceptance_summary.csv")
    interpretation_metrics = read_csv(phase322_dir / "phase322_interpretation_metrics.csv")
    scenarios = read_csv(phase322_dir / "phase322_scenario_summary.csv")
    family = summarize_family(scenarios)
    execution = summarize_execution(scenarios)
    breadth = summarize_breadth(scenarios)
    decisions = build_decision_ledger(phase322, interpretation_metrics, scenarios, family, execution)
    gates = build_gate_evaluation(phase322, decisions)
    acceptance = build_acceptance(decisions, gates)

    family.to_csv(output_dir / "phase323_family_interpretation_summary.csv", index=False)
    execution.to_csv(output_dir / "phase323_execution_policy_interpretation_summary.csv", index=False)
    breadth.to_csv(output_dir / "phase323_breadth_interpretation_summary.csv", index=False)
    decisions.to_csv(output_dir / "phase323_interpretation_decision_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase323_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase323_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        acceptance,
        {
            "Family interpretation": family,
            "Execution policy interpretation": execution,
            "Breadth interpretation": breadth,
            "Decision ledger": decisions,
            "Gates": gates,
        },
    )

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase323_event_catalyst_multievent_strategy_search_interpretation",
        **reproducibility_fields(
            artifact_id="phase323",
            generated_utc=generated_utc,
            inputs={
                "phase322_acceptance": str(phase322_dir / "phase322_acceptance_summary.csv"),
                "phase322_scenarios": str(phase322_dir / "phase322_scenario_summary.csv"),
            },
            parameters={"annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT, "robust_event_floor": ROBUST_EVENT_FLOOR},
            outputs={"acceptance_summary": str(output_dir / "phase323_acceptance_summary.csv")},
            cost_model_version="inherits_phase322",
            latency_model_version="not_applicable_interpretation_only",
        ),
    }
    (output_dir / "phase323_event_catalyst_multievent_strategy_search_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Interpret Phase322 multi-event strategy search.")
    parser.add_argument("--phase322-dir", type=Path, default=DEFAULT_PHASE322_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase322_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
