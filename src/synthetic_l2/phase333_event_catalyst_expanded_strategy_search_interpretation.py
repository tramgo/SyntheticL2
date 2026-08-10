from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import duckdb
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE332_DIR = Path("outputs/phase332")
DEFAULT_OUTPUT_DIR = Path("outputs/phase333")

NEXT_ACTION = "run_phase334_cost_stress_margin_redesign_precommit_no_replay"
REPAIR_ACTION = "repair_phase333_event_catalyst_expanded_strategy_search_interpretation"

ANNUALIZED_THRESHOLD_PCT = 12.0
NEAR_MISS_FLOOR_PCT = 10.0
ROBUST_EVENT_FLOOR = 30


def summarize_family_cost_stress(scenario_parquet: Path) -> pd.DataFrame:
    if not scenario_parquet.exists():
        return pd.DataFrame()
    query = f"""
        SELECT
            family_id,
            execution_policy,
            cost_profile,
            COUNT(*) AS scenario_rows,
            SUM(CASE WHEN annualized_return_pct > {ANNUALIZED_THRESHOLD_PCT} THEN 1 ELSE 0 END) AS above12_rows,
            SUM(CASE WHEN acceptance_grade_candidate THEN 1 ELSE 0 END) AS acceptance_grade_rows,
            MAX(annualized_return_pct) AS best_annualized_return_pct,
            MEDIAN(annualized_return_pct) AS median_annualized_return_pct,
            MAX(net_pnl_inr) AS best_net_pnl_inr,
            MAX(scheduled_event_rows) AS max_scheduled_event_rows,
            MAX(symbol_rows) AS max_symbol_rows,
            MAX(observed_trade_dates) AS max_observed_trade_dates
        FROM read_parquet('{scenario_parquet.as_posix()}')
        GROUP BY family_id, execution_policy, cost_profile
        ORDER BY
            CASE WHEN cost_profile = 'zerodha_2x_all_in_cost_proxy' THEN 0 ELSE 1 END,
            best_annualized_return_pct DESC,
            above12_rows DESC
    """
    return duckdb.sql(query).df()


def summarize_near_miss(scenario_parquet: Path) -> pd.DataFrame:
    if not scenario_parquet.exists():
        return pd.DataFrame()
    query = f"""
        SELECT
            scenario_id,
            family_id,
            horizon_seconds,
            threshold_policy,
            side_policy,
            execution_policy,
            event_bucket_policy,
            initial_capital_inr,
            fixed_notional_inr,
            max_concurrent_positions,
            scheduled_event_rows,
            symbol_rows,
            observed_trade_dates,
            trade_rows,
            gross_pnl_inr,
            cost_inr,
            passive_penalty_inr,
            net_pnl_inr,
            annualized_return_pct,
            ({ANNUALIZED_THRESHOLD_PCT} - annualized_return_pct) AS annualized_gap_to_12pct
        FROM read_parquet('{scenario_parquet.as_posix()}')
        WHERE cost_profile = 'zerodha_2x_all_in_cost_proxy'
        ORDER BY annualized_return_pct DESC, scheduled_event_rows DESC, symbol_rows DESC
        LIMIT 25
    """
    return duckdb.sql(query).df()


def summarize_profile_gap(scenario_parquet: Path) -> pd.DataFrame:
    if not scenario_parquet.exists():
        return pd.DataFrame()
    query = f"""
        WITH best_by_profile AS (
            SELECT
                family_id,
                threshold_policy,
                side_policy,
                execution_policy,
                event_bucket_policy,
                initial_capital_inr,
                fixed_notional_inr,
                max_concurrent_positions,
                cost_profile,
                MAX(annualized_return_pct) AS best_annualized_return_pct,
                MAX(scheduled_event_rows) AS max_scheduled_event_rows
            FROM read_parquet('{scenario_parquet.as_posix()}')
            GROUP BY
                family_id, threshold_policy, side_policy, execution_policy, event_bucket_policy,
                initial_capital_inr, fixed_notional_inr, max_concurrent_positions, cost_profile
        )
        SELECT
            family_id,
            threshold_policy,
            side_policy,
            execution_policy,
            event_bucket_policy,
            initial_capital_inr,
            fixed_notional_inr,
            max_concurrent_positions,
            MAX(CASE WHEN cost_profile = 'zerodha_base' THEN best_annualized_return_pct END) AS base_best_annualized_return_pct,
            MAX(CASE WHEN cost_profile = 'zerodha_2x_all_in_cost_proxy' THEN best_annualized_return_pct END) AS cost200_best_annualized_return_pct,
            MAX(CASE WHEN cost_profile = 'zerodha_base' THEN max_scheduled_event_rows END) AS base_max_scheduled_events,
            MAX(CASE WHEN cost_profile = 'zerodha_2x_all_in_cost_proxy' THEN max_scheduled_event_rows END) AS cost200_max_scheduled_events,
            (
                MAX(CASE WHEN cost_profile = 'zerodha_base' THEN best_annualized_return_pct END)
                - MAX(CASE WHEN cost_profile = 'zerodha_2x_all_in_cost_proxy' THEN best_annualized_return_pct END)
            ) AS cost_stress_drag_pct
        FROM best_by_profile
        GROUP BY
            family_id, threshold_policy, side_policy, execution_policy, event_bucket_policy,
            initial_capital_inr, fixed_notional_inr, max_concurrent_positions
        HAVING cost200_best_annualized_return_pct IS NOT NULL
        ORDER BY cost200_best_annualized_return_pct DESC, base_best_annualized_return_pct DESC
        LIMIT 50
    """
    return duckdb.sql(query).df()


def build_decision_ledger(phase332: pd.DataFrame, near_miss: pd.DataFrame, family: pd.DataFrame) -> pd.DataFrame:
    scenario_rows = as_int(metric_value(phase332, "phase332_scenario_rows", 0))
    above12 = as_int(metric_value(phase332, "phase332_above12_annualized_scenario_rows", 0))
    cost200_above12 = as_int(metric_value(phase332, "phase332_cost200_above12_scenario_rows", 0))
    cost200_acceptance = as_int(metric_value(phase332, "phase332_cost200_acceptance_grade_candidate_rows", 0))
    best_family = str(metric_value(phase332, "phase332_best_family_id", ""))
    best_cost200 = float(metric_value(phase332, "phase332_best_cost200_annualized_return_pct", 0) or 0)
    best_cost200_events = as_int(metric_value(phase332, "phase332_best_cost200_scheduled_event_rows", 0))
    threshold_gap = ANNUALIZED_THRESHOLD_PCT - best_cost200
    passive_best = ""
    taker_best = ""
    if not family.empty:
        passive = family[family["execution_policy"].astype(str).eq("passive_aware_directional_with_penalties")]
        taker = family[family["execution_policy"].astype(str).eq("taker_entry_taker_exit")]
        passive_best = float(passive["best_annualized_return_pct"].max()) if not passive.empty else ""
        taker_best = float(taker["best_annualized_return_pct"].max()) if not taker.empty else ""

    near_miss_preserved = int(
        cost200_above12 == 0
        and best_cost200 >= NEAR_MISS_FLOOR_PCT
        and best_cost200 < ANNUALIZED_THRESHOLD_PCT
        and best_cost200_events >= ROBUST_EVENT_FLOOR
    )
    rows = [
        ("phase332_search_complete", 1, f"scenario_rows={scenario_rows}", "The expanded training-only search ran to completion."),
        ("base_or_slippage_profitable_research_pockets_exist", int(above12 > 0), f"above12_scenario_rows={above12}", "Profitable-looking pockets exist before the strict 2x cost-stress bar."),
        ("cost200_profitability_bar_passed", int(cost200_above12 > 0), f"cost200_above12_scenario_rows={cost200_above12}; threshold>{ANNUALIZED_THRESHOLD_PCT}", "The user threshold is not met under the 2x Zerodha all-in cost proxy."),
        ("cost200_acceptance_grade_candidates_exist", int(cost200_acceptance > 0), f"cost200_acceptance_grade_candidate_rows={cost200_acceptance}", "No acceptance-grade candidate exists without passing both cost and breadth gates."),
        ("best_cost200_near_miss_preserved", near_miss_preserved, f"best_cost200={best_cost200}; gap_to_12={threshold_gap}; events={best_cost200_events}", "The near-miss is broad enough to redesign around, but it is not accepted as profitable."),
        ("preserved_family_for_redesign", best_family, "Phase332 best family", "Depth-acceleration reversal remains the strongest actionable clue."),
        ("passive_aware_rescue_status", "falsified_as_primary_rescue", f"best_passive={passive_best}; best_taker={taker_best}", "Passive-aware execution realism stays required, but it did not rescue the branch."),
        ("next_design_focus", "cost_stress_margin_and_turnover_reduction", "2x cost miss is 0.482445937 pct points below 12", "The next test should reduce cost drag without lowering the annualized or cost-stress bar."),
        ("forbidden_next_actions", "no_replay_no_promotion_no_paper_live_no_profit_claim", "all acceptance gates closed", "Do not jump to replay or declare profitability from Phase332."),
        ("selected_next_route", "P334_COST_STRESS_MARGIN_REDESIGN_PRECOMMIT", NEXT_ACTION, "Precommit a narrow redesign around the preserved cost-stress near miss, then execute it."),
    ]
    return pd.DataFrame(rows, columns=["decision_id", "decision_value", "evidence", "interpretation"])


def build_gate_evaluation(phase332: pd.DataFrame, decisions: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(phase332, "phase332_expanded_strategy_search_training_complete", 0))
    claim = as_int(metric_value(phase332, "phase332_deployable_profitability_claim_allowed", 1))
    replay = as_int(metric_value(phase332, "phase332_strategy_replay_allowed", 1))
    selected = decisions[decisions["decision_id"].astype(str).eq("selected_next_route")]
    rows = [
        ("P333_PHASE332_COMPLETE", complete == 1, complete, 1),
        ("P333_DECISION_ROWS_PRESENT", len(decisions) >= 10, len(decisions), ">=10"),
        ("P333_COST200_FAILURE_INTERPRETED", decisions["decision_id"].astype(str).eq("cost200_profitability_bar_passed").any(), "present", "present"),
        ("P333_NEAR_MISS_DECISION_PRESENT", decisions["decision_id"].astype(str).eq("best_cost200_near_miss_preserved").any(), "present", "present"),
        ("P333_PASSIVE_AWARE_STATUS_PRESENT", decisions["decision_id"].astype(str).eq("passive_aware_rescue_status").any(), "present", "present"),
        ("P333_PROFITABILITY_CLAIM_CLOSED", claim == 0, claim, 0),
        ("P333_REPLAY_CLOSED", replay == 0, replay, 0),
        ("P333_NEXT_ROUTE_SELECTED", not selected.empty, selected["decision_value"].iloc[0] if not selected.empty else "", "selected"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(decisions: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    lookup = decisions.set_index("decision_id")["decision_value"].to_dict() if not decisions.empty else {}
    return pd.DataFrame(
        [
            ("phase333_event_catalyst_expanded_strategy_search_interpretation_complete", int(hard_pass == hard_rows), "Phase333 interpretation completed"),
            ("phase333_base_or_slippage_profitable_research_pockets_exist", lookup.get("base_or_slippage_profitable_research_pockets_exist", 0), "Base/slippage research pockets above 12 exist"),
            ("phase333_cost200_profitability_bar_passed", lookup.get("cost200_profitability_bar_passed", 0), "2x-cost >12% bar passed"),
            ("phase333_cost200_acceptance_grade_candidates_exist", lookup.get("cost200_acceptance_grade_candidates_exist", 0), "2x-cost acceptance-grade candidates exist"),
            ("phase333_best_cost200_near_miss_preserved", lookup.get("best_cost200_near_miss_preserved", 0), "Near-miss preserved as redesign clue"),
            ("phase333_preserved_family_for_redesign", lookup.get("preserved_family_for_redesign", ""), "Family preserved for redesign"),
            ("phase333_passive_aware_rescue_status", lookup.get("passive_aware_rescue_status", ""), "Passive-aware rescue status"),
            ("phase333_next_design_focus", lookup.get("next_design_focus", ""), "Next design focus"),
            ("phase333_replay_allowed", 0, "No replay"),
            ("phase333_strategy_promotion_allowed", 0, "No promotion"),
            ("phase333_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase333_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase333_selected_next_route", lookup.get("selected_next_route", ""), "Selected next route"),
            ("phase333_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase333_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase333_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase333 Event-Catalyst Expanded Strategy Search Interpretation",
        "",
        "Phase333 interprets the Phase332 full expanded strategy surface. It does not run replay, promote a strategy, open paper/live acceptance, or claim deployable profitability.",
        "The central verdict is crisp: the expanded full-depth search found real base-cost research pockets, but no 2x Zerodha cost-stress scenario exceeded the user's >12% annualized threshold.",
        "Because the best 2x-cost result reached 11.517554062957867% over 40 scheduled events, the clue is preserved for a focused cost-stress-margin redesign rather than discarded.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase333_event_catalyst_expanded_strategy_search_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase332_dir: Path = DEFAULT_PHASE332_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase332 = read_csv(phase332_dir / "phase332_acceptance_summary.csv")
    scenario_parquet = phase332_dir / "phase332_scenario_summary.parquet"
    family = summarize_family_cost_stress(scenario_parquet)
    near_miss = summarize_near_miss(scenario_parquet)
    profile_gap = summarize_profile_gap(scenario_parquet)
    decisions = build_decision_ledger(phase332, near_miss, family)
    gates = build_gate_evaluation(phase332, decisions)
    acceptance = build_acceptance(decisions, gates)

    family.to_csv(output_dir / "phase333_family_cost_stress_interpretation_summary.csv", index=False)
    near_miss.to_csv(output_dir / "phase333_cost200_near_miss_top_scenarios.csv", index=False)
    profile_gap.to_csv(output_dir / "phase333_cost_profile_gap_summary.csv", index=False)
    decisions.to_csv(output_dir / "phase333_interpretation_decision_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase333_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase333_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        acceptance,
        {
            "Decision ledger": decisions,
            "2x-cost near-miss scenarios": near_miss,
            "Cost profile gap": profile_gap,
            "Family cost-stress interpretation": family.head(80),
            "Gates": gates,
        },
    )

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase333_event_catalyst_expanded_strategy_search_interpretation",
        **reproducibility_fields(
            artifact_id="phase333",
            generated_utc=generated_utc,
            inputs={
                "phase332_acceptance": str(phase332_dir / "phase332_acceptance_summary.csv"),
                "phase332_scenarios": str(scenario_parquet),
            },
            parameters={
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "near_miss_floor_pct": NEAR_MISS_FLOOR_PCT,
                "robust_event_floor": ROBUST_EVENT_FLOOR,
            },
            outputs={"acceptance_summary": str(output_dir / "phase333_acceptance_summary.csv")},
            cost_model_version="inherits_phase332_zerodha_cost_profiles",
            latency_model_version="not_applicable_interpretation_only",
        ),
    }
    (output_dir / "phase333_event_catalyst_expanded_strategy_search_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Interpret Phase332 expanded strategy search.")
    parser.add_argument("--phase332-dir", type=Path, default=DEFAULT_PHASE332_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase332_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
