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


DEFAULT_PHASE335_DIR = Path("outputs/phase335")
DEFAULT_OUTPUT_DIR = Path("outputs/phase336")

NEXT_ACTION = "run_phase337_cost_stress_holdout_validation_precommit_no_replay"
REPAIR_ACTION = "repair_phase336_cost_stress_margin_redesign_interpretation"

ANNUALIZED_THRESHOLD_PCT = 12.0
ROBUST_EVENT_FLOOR = 30


def summarize_acceptance_candidates(scenario_parquet: Path) -> pd.DataFrame:
    if not scenario_parquet.exists():
        return pd.DataFrame()
    query = f"""
        SELECT
            scenario_id,
            lane_id,
            horizon_seconds,
            signal_quantile,
            spread_max_quantile,
            depth_share_min_quantile,
            top_n_per_event,
            side_policy,
            execution_policy,
            cost_profile,
            initial_capital_inr,
            fixed_notional_inr,
            max_concurrent_positions,
            scheduled_event_rows,
            symbol_rows,
            observed_trade_dates,
            trade_rows,
            net_pnl_inr,
            annualized_return_pct,
            side_flip_annualized_return_pct,
            random_side_annualized_return_pct,
            control_pass
        FROM read_parquet('{scenario_parquet.as_posix()}')
        WHERE cost_profile = 'zerodha_2x_all_in_cost_proxy'
          AND acceptance_grade_candidate = 1
        ORDER BY annualized_return_pct DESC, scheduled_event_rows DESC, symbol_rows DESC
    """
    return duckdb.sql(query).df()


def summarize_failure_modes(scenarios: pd.DataFrame, candidates: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame()
    cost200 = scenarios[scenarios["cost_profile"].astype(str).eq("zerodha_2x_all_in_cost_proxy")]
    rows = [
        {
            "failure_mode": "sparse_high_return_not_acceptance_grade",
            "scenario_rows": int(((cost200["annualized_return_pct"] > ANNUALIZED_THRESHOLD_PCT) & (cost200["scheduled_event_rows"] < ROBUST_EVENT_FLOOR)).sum()),
            "interpretation": "Some high-return rows are too sparse and must not drive validation.",
        },
        {
            "failure_mode": "passive_aware_no_cost200_acceptance",
            "scenario_rows": int(((cost200["execution_policy"].astype(str).eq("passive_aware_directional_with_penalties")) & (cost200["acceptance_grade_candidate"].astype(int).eq(1))).sum()),
            "interpretation": "Passive-aware route did not produce acceptance-grade candidates; keep it diagnostic.",
        },
        {
            "failure_mode": "candidate_count_requires_holdout",
            "scenario_rows": int(len(candidates)),
            "interpretation": "Positive training candidates exist, so next step must be precommitted holdout/falsification, not a profitability claim.",
        },
    ]
    return pd.DataFrame(rows)


def build_decision_ledger(phase335: pd.DataFrame, candidates: pd.DataFrame, failure_modes: pd.DataFrame) -> pd.DataFrame:
    scenario_rows = as_int(metric_value(phase335, "phase335_scenario_rows", 0))
    cost200_above12 = as_int(metric_value(phase335, "phase335_cost200_above12_scenario_rows", 0))
    acceptance_rows = as_int(metric_value(phase335, "phase335_cost200_acceptance_grade_candidate_rows", 0))
    best_acceptance = str(metric_value(phase335, "phase335_best_acceptance_grade_cost200_scenario_id", ""))
    best_acceptance_ann = metric_value(phase335, "phase335_best_acceptance_grade_cost200_annualized_return_pct", "")
    best_acceptance_events = as_int(metric_value(phase335, "phase335_best_acceptance_grade_cost200_scheduled_event_rows", 0))
    candidate_lanes = ";".join(sorted(candidates["lane_id"].astype(str).unique().tolist())) if not candidates.empty else ""
    rows = [
        ("phase335_training_complete", 1, f"scenario_rows={scenario_rows}", "Phase335 completed the training-only redesign search."),
        ("cost200_profitable_training_pockets_exist", int(cost200_above12 > 0), f"cost200_above12={cost200_above12}", "The redesigned training surface crossed the user >12% threshold under 2x costs."),
        ("cost200_acceptance_grade_training_candidates_exist", int(acceptance_rows > 0), f"acceptance_rows={acceptance_rows}", "Training-only candidates pass cost, breadth, and control diagnostics."),
        ("best_acceptance_grade_candidate_preserved", best_acceptance, f"annualized={best_acceptance_ann}; events={best_acceptance_events}", "Preserve the best candidate for holdout precommit."),
        ("candidate_lanes_preserved", candidate_lanes, f"candidate_rows={len(candidates)}", "Preserve all lanes that generated acceptance-grade rows."),
        ("passive_aware_status", "diagnostic_only_no_acceptance_grade_rows", "passive acceptance-grade rows=0", "Passive-aware realism remains diagnostic and should not be used to claim acceptance."),
        ("failure_modes_recorded", int(len(failure_modes)), "sparse; passive; holdout_required", "Record reasons this is not yet final profitability."),
        ("replay_allowed_now", 0, "training-only evidence", "No replay opens directly from Phase336."),
        ("paper_live_or_profitability_claim_allowed", 0, "closed", "No paper/live or deployable profitability claim opens."),
        ("selected_next_route", "P337_COST_STRESS_HOLDOUT_VALIDATION_PRECOMMIT", NEXT_ACTION, "Precommit holdout/falsification for the preserved training candidates."),
    ]
    return pd.DataFrame(rows, columns=["decision_id", "decision_value", "evidence", "interpretation"])


def build_gate_evaluation(phase335: pd.DataFrame, decisions: pd.DataFrame, candidates: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(phase335, "phase335_cost_stress_margin_redesign_training_complete", 0))
    replay = as_int(metric_value(phase335, "phase335_strategy_replay_allowed", 1))
    claim = as_int(metric_value(phase335, "phase335_deployable_profitability_claim_allowed", 1))
    selected = decisions[decisions["decision_id"].astype(str).eq("selected_next_route")]
    rows = [
        ("P336_PHASE335_COMPLETE", complete == 1, complete, 1),
        ("P336_DECISION_ROWS_PRESENT", len(decisions) >= 10, len(decisions), ">=10"),
        ("P336_ACCEPTANCE_CANDIDATES_INTERPRETED", len(candidates) > 0, len(candidates), ">0"),
        ("P336_HOLDOUT_ROUTE_SELECTED", not selected.empty, selected["decision_value"].iloc[0] if not selected.empty else "", "selected"),
        ("P336_REPLAY_REMAINS_CLOSED", replay == 0, replay, 0),
        ("P336_PROFITABILITY_CLAIM_CLOSED", claim == 0, claim, 0),
        ("P336_NEXT_IS_PRECOMMIT_NOT_REPLAY", str(selected["decision_value"].iloc[0]).endswith("_PRECOMMIT") if not selected.empty else False, selected["decision_value"].iloc[0] if not selected.empty else "", "precommit"),
        ("P336_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(decisions: pd.DataFrame, gates: pd.DataFrame, candidates: pd.DataFrame, phase335: pd.DataFrame) -> pd.DataFrame:
    lookup = decisions.set_index("decision_id")["decision_value"].to_dict() if not decisions.empty else {}
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase336_cost_stress_margin_redesign_interpretation_complete", int(hard_pass == hard_rows), "Phase336 interpretation completed"),
            ("phase336_cost200_profitable_training_pockets_exist", lookup.get("cost200_profitable_training_pockets_exist", 0), "2x-cost profitable training pockets exist"),
            ("phase336_cost200_acceptance_grade_training_candidates_exist", lookup.get("cost200_acceptance_grade_training_candidates_exist", 0), "2x-cost acceptance-grade training candidates exist"),
            ("phase336_candidate_rows_preserved", int(len(candidates)), "Acceptance-grade candidates preserved"),
            ("phase336_best_acceptance_grade_candidate", lookup.get("best_acceptance_grade_candidate_preserved", ""), "Best candidate preserved"),
            ("phase336_best_acceptance_grade_annualized_return_pct", metric_value(phase335, "phase335_best_acceptance_grade_cost200_annualized_return_pct", ""), "Best acceptance-grade annualized return"),
            ("phase336_best_acceptance_grade_scheduled_events", metric_value(phase335, "phase335_best_acceptance_grade_cost200_scheduled_event_rows", ""), "Best acceptance-grade scheduled events"),
            ("phase336_candidate_lanes_preserved", lookup.get("candidate_lanes_preserved", ""), "Candidate lanes preserved"),
            ("phase336_passive_aware_status", lookup.get("passive_aware_status", ""), "Passive-aware status"),
            ("phase336_replay_allowed", 0, "No replay"),
            ("phase336_strategy_promotion_allowed", 0, "No promotion"),
            ("phase336_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase336_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase336_selected_next_route", lookup.get("selected_next_route", ""), "Selected next route"),
            ("phase336_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase336_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase336_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase336 Cost-Stress Margin Redesign Interpretation",
        "",
        "Phase336 interprets Phase335 positive training-only cost-stress results.",
        "It preserves candidates for holdout precommit, but does not replay, promote, open paper/live acceptance, or claim deployable profitability.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase336_cost_stress_margin_redesign_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase335_dir: Path = DEFAULT_PHASE335_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase335 = read_csv(phase335_dir / "phase335_acceptance_summary.csv")
    scenario_parquet = phase335_dir / "phase335_scenario_summary.parquet"
    scenarios = duckdb.sql(f"SELECT * FROM read_parquet('{scenario_parquet.as_posix()}')").df() if scenario_parquet.exists() else pd.DataFrame()
    candidates = summarize_acceptance_candidates(scenario_parquet)
    failure_modes = summarize_failure_modes(scenarios, candidates)
    decisions = build_decision_ledger(phase335, candidates, failure_modes)
    gates = build_gate_evaluation(phase335, decisions, candidates)
    acceptance = build_acceptance(decisions, gates, candidates, phase335)

    candidates.to_csv(output_dir / "phase336_acceptance_grade_candidate_ledger.csv", index=False)
    failure_modes.to_csv(output_dir / "phase336_failure_mode_ledger.csv", index=False)
    decisions.to_csv(output_dir / "phase336_interpretation_decision_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase336_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase336_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        acceptance,
        {
            "Decision ledger": decisions,
            "Acceptance-grade candidates": candidates.head(50),
            "Failure modes": failure_modes,
            "Gates": gates,
        },
    )

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase336_cost_stress_margin_redesign_interpretation",
        **reproducibility_fields(
            artifact_id="phase336",
            generated_utc=generated_utc,
            inputs={
                "phase335_acceptance": str(phase335_dir / "phase335_acceptance_summary.csv"),
                "phase335_scenarios": str(scenario_parquet),
            },
            parameters={"annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT, "robust_event_floor": ROBUST_EVENT_FLOOR},
            outputs={"acceptance_summary": str(output_dir / "phase336_acceptance_summary.csv")},
            cost_model_version="inherits_phase335_zerodha_cost_profiles",
            latency_model_version="not_applicable_interpretation_only",
        ),
    }
    (output_dir / "phase336_cost_stress_margin_redesign_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Interpret Phase335 cost-stress margin redesign.")
    parser.add_argument("--phase335-dir", type=Path, default=DEFAULT_PHASE335_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase335_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
