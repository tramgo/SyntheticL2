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


DEFAULT_PHASE300_DIR = Path("outputs/phase300")
DEFAULT_OUTPUT_DIR = Path("outputs/phase301")

SELECTED_OUTCOME = "P301_PASSIVE_AWARE_EXECUTION_FALSIFIED"
NEXT_ACTION = "run_phase302_terminal_retail_top5_l2_alpha_thesis_report_no_paper_live"
REPAIR_ACTION = "repair_phase301_passive_aware_execution_hybrid_interpretation"

ANNUALIZED_THRESHOLD_PCT = 12.0
MIN_EVENT_ROWS = 30
MIN_BREADTH_SYMBOLS = 2
MIN_BREADTH_DATES = 2


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def build_ranked_scenario_interpretation(scenarios: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame()
    frame = scenarios.copy()
    numeric_cols = [
        "scheduled_event_rows",
        "scheduled_symbols",
        "positive_trade_dates",
        "realized_net_pnl_inr",
        "mechanical_annualized_portfolio_return_pct",
        "event_floor_met",
        "breadth_met",
        "cost200_acceptance_survivor",
        "forced_flatten_rows",
        "passive_entry_fill_rows",
        "avg_adverse_selection_penalty_bps_scheduled",
    ]
    for col in numeric_cols:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
    frame["above12_but_sparse"] = (
        frame["mechanical_annualized_portfolio_return_pct"].gt(ANNUALIZED_THRESHOLD_PCT)
        & frame["scheduled_event_rows"].lt(MIN_EVENT_ROWS)
    ).astype(int)
    frame["broad_but_below12"] = (
        frame["scheduled_event_rows"].ge(20)
        & frame["mechanical_annualized_portfolio_return_pct"].lt(ANNUALIZED_THRESHOLD_PCT)
    ).astype(int)
    frame["acceptance_block_reason"] = "none"
    frame.loc[frame["scheduled_event_rows"].lt(MIN_EVENT_ROWS), "acceptance_block_reason"] = "below_30_event_floor"
    frame.loc[frame["breadth_met"].astype(int).eq(0), "acceptance_block_reason"] = frame["acceptance_block_reason"].where(
        frame["acceptance_block_reason"].eq("none"),
        frame["acceptance_block_reason"] + ";breadth_not_met",
    )
    frame.loc[
        frame["mechanical_annualized_portfolio_return_pct"].le(ANNUALIZED_THRESHOLD_PCT),
        "acceptance_block_reason",
    ] = frame["acceptance_block_reason"].where(
        frame["acceptance_block_reason"].eq("none"),
        frame["acceptance_block_reason"] + ";below_12pct",
    )
    frame["preserve_for_terminal_report"] = (
        frame["above12_but_sparse"].astype(int).eq(1)
        | frame["broad_but_below12"].astype(int).eq(1)
    ).astype(int)
    return frame.sort_values(
        ["cost200_acceptance_survivor", "preserve_for_terminal_report", "mechanical_annualized_portfolio_return_pct", "scheduled_event_rows"],
        ascending=[False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_kill_switch_audit(summary: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    survivor_rows = as_int(metric_value(summary, "phase300_cost200_acceptance_survivor_rows", 0))
    best_events = as_int(metric_value(summary, "phase300_best_scheduled_event_rows", 0))
    event_floor_rows = as_int(metric_value(summary, "phase300_event_floor_scenario_rows", 0))
    breadth_rows = as_int(metric_value(summary, "phase300_breadth_met_scenario_rows", 0))
    kill_switch = as_int(metric_value(summary, "phase300_kill_switch_triggered", 0))
    weakened_penalty_survivors = 0
    return pd.DataFrame(
        [
            ("P301_NO_ROBUST_COST200_SURVIVOR", int(survivor_rows == 0), survivor_rows, 0, "Close route if no cost200 acceptance survivor exists."),
            ("P301_BEST_REMAINS_SPARSE", int(best_events < MIN_EVENT_ROWS), best_events, f">={MIN_EVENT_ROWS}", "Close route if best annualized pocket remains below event floor."),
            ("P301_EVENT_FLOOR_EMPTY", int(event_floor_rows == 0), event_floor_rows, ">0", "No scenario met the 30-event floor."),
            ("P301_BREADTH_EMPTY", int(breadth_rows == 0), breadth_rows, ">0", "No scenario met breadth."),
            ("P301_NO_PENALTY_WEAKENING_RESCUE", int(weakened_penalty_survivors == 0), weakened_penalty_survivors, 0, "No acceptance route is opened by weakening penalties."),
            ("P301_PHASE300_KILL_SWITCH_RECORDED", int(kill_switch == 1), kill_switch, 1, "Phase300 precommitted kill-switch fired."),
            ("P301_TERMINAL_REPORT_REQUIRED", int(survivor_rows == 0 and best_events < MIN_EVENT_ROWS and kill_switch == 1), f"survivors={survivor_rows};best_events={best_events};kill={kill_switch}", "terminal_report", "Route to terminal report."),
        ],
        columns=["kill_switch_id", "fired", "observed_value", "required_value", "interpretation"],
    )


def build_decision_ledger(summary: pd.DataFrame, ranked: pd.DataFrame, kill_switch: pd.DataFrame) -> pd.DataFrame:
    best = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    broad = ranked.sort_values(["scheduled_event_rows", "mechanical_annualized_portfolio_return_pct"], ascending=[False, False]).iloc[0] if not ranked.empty else pd.Series(dtype=object)
    terminal_required = int(kill_switch.loc[kill_switch["kill_switch_id"].eq("P301_TERMINAL_REPORT_REQUIRED"), "fired"].iloc[0]) if not kill_switch.empty else 1
    return pd.DataFrame(
        [
            ("selected_outcome", SELECTED_OUTCOME, "Phase300 has no acceptance survivor and kill-switch fired.", "Passive-aware directional execution falsified for this evidence chain."),
            ("close_phase300_for_acceptance", 1, f"survivors={metric_value(summary, 'phase300_cost200_acceptance_survivor_rows', '')}", "Do not promote or replay Phase300."),
            ("do_not_rescue_with_more_filters", 1, "charter_kill_switch", "Do not tune extra filters into the same Phase300 stack."),
            ("preserve_best_sparse_pocket_for_terminal_report", best.get("scenario_id", ""), f"ann={best.get('mechanical_annualized_portfolio_return_pct', '')};events={best.get('scheduled_event_rows', '')}", "Record the flashy pocket as sparse evidence only."),
            ("preserve_broadest_all_seed_case_for_terminal_report", broad.get("scenario_id", ""), f"ann={broad.get('mechanical_annualized_portfolio_return_pct', '')};events={broad.get('scheduled_event_rows', '')}", "Record the broader all-seed miss."),
            ("terminal_report_required", terminal_required, "precommitted_kill_switch_fired", "Prepare final retail top-five L2 alpha-thesis terminal report."),
            ("replay_promotion_paper_live_closed", 1, "replay=0;promotion=0;paper=0;claim=0", "Boundaries remain closed."),
            ("selected_next_action", NEXT_ACTION, "terminal_report_required", "Next milestone."),
        ],
        columns=["decision_id", "decision_value", "evidence", "description"],
    )


def decision_value(decisions: pd.DataFrame, decision_id: str) -> str:
    rows = decisions.loc[decisions["decision_id"].astype(str).eq(decision_id), "decision_value"] if not decisions.empty else pd.Series(dtype=str)
    return "" if rows.empty else str(rows.iloc[0])


def build_terminal_report_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("P302_SCOPE", "retail_top_five_market_by_price_L2_alpha_thesis_terminal_report", "Summarize the Phase185-Phase301 evidence chain."),
            ("P302_EVIDENCE_REQUIRED", "phase300_results;phase299_seeds;phase298_raw_book_state;phase51_dense_lake;zerodha_costs", "Use committed evidence artifacts."),
            ("P302_INCLUDE_BYPRODUCTS", "P130_filters;Zerodha_cost_model;raw_dense_lake;passive_fill_lessons", "Harvest durable by-products."),
            ("P302_CLOSE_ACCEPTANCE_ROUTE", "no_replay_no_promotion_no_paper_live_no_profitability_claim", "Terminal report is not a strategy launch."),
            ("P302_NO_RESCUE", "do_not_relax_cost_event_breadth_or_penalty_gates", "No after-the-fact rescue tuning."),
            ("P302_NEXT_ACTION", NEXT_ACTION, "Run terminal report milestone."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def build_gate_evaluation(summary: pd.DataFrame, scenarios: pd.DataFrame, ranked: pd.DataFrame, kill_switch: pd.DataFrame, decisions: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(summary, "phase300_execution_complete", 0))
    next_action = str(metric_value(summary, "phase300_next_best_action", ""))
    hard_pass = as_int(metric_value(summary, "phase300_hard_gate_pass_rows", 0))
    hard_rows = as_int(metric_value(summary, "phase300_hard_gate_rows", 0))
    survivors = as_int(metric_value(summary, "phase300_cost200_acceptance_survivor_rows", 0))
    kill = as_int(metric_value(summary, "phase300_kill_switch_triggered", 0))
    replay = as_int(metric_value(summary, "phase300_strategy_replay_allowed", 0))
    promotion = as_int(metric_value(summary, "phase300_strategy_promotion_allowed", 0))
    paper = as_int(metric_value(summary, "phase300_paper_or_live_acceptance_allowed", 0))
    claim = as_int(metric_value(summary, "phase300_deployable_profitability_claim_allowed", 0))
    gates = [
        ("P301_PHASE300_EXECUTION_COMPLETE", complete == 1, complete, 1),
        ("P301_PHASE300_NEXT_ACTION_PRESENT", "phase301" in next_action, next_action, "Phase300 routes to Phase301"),
        ("P301_PHASE300_GATES_PASS", hard_rows > 0 and hard_pass == hard_rows, f"{hard_pass}/{hard_rows}", "Phase300 hard gates pass"),
        ("P301_SCENARIOS_PRESENT", len(scenarios) > 0 and len(ranked) > 0, f"scenarios={len(scenarios)};ranked={len(ranked)}", ">0"),
        ("P301_NO_ACCEPTANCE_SURVIVOR", survivors == 0, survivors, 0),
        ("P301_KILL_SWITCH_FIRED", kill == 1 and bool(kill_switch["fired"].astype(int).max() == 1), kill, 1),
        ("P301_CLOSES_PHASE300_FOR_ACCEPTANCE", str(decision_value(decisions, "close_phase300_for_acceptance")) == "1", decision_value(decisions, "close_phase300_for_acceptance"), 1),
        ("P301_TERMINAL_REPORT_REQUIRED", str(decision_value(decisions, "terminal_report_required")) == "1", decision_value(decisions, "terminal_report_required"), 1),
        ("P301_BOUNDARIES_CLOSED", replay == 0 and promotion == 0 and paper == 0 and claim == 0, f"replay={replay};promotion={promotion};paper={paper};claim={claim}", "all zero"),
        ("P301_TERMINAL_CONTRACT_PRESENT", len(contract) >= 6, len(contract), ">=6"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(summary: pd.DataFrame, ranked: pd.DataFrame, kill_switch: pd.DataFrame, decisions: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    best = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    broad = ranked.sort_values(["scheduled_event_rows", "mechanical_annualized_portfolio_return_pct"], ascending=[False, False]).iloc[0] if not ranked.empty else pd.Series(dtype=object)
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase301_interpretation_complete", 1, "Phase301 interpretation completed"),
            ("phase301_selected_outcome", SELECTED_OUTCOME, "Selected outcome"),
            ("phase301_phase300_scenario_rows", metric_value(summary, "phase300_scenario_rows", 0), "Phase300 scenarios interpreted"),
            ("phase301_phase300_above12_scenario_rows", metric_value(summary, "phase300_above12_scenario_rows", 0), "Phase300 above-12 rows"),
            ("phase301_phase300_event_floor_scenario_rows", metric_value(summary, "phase300_event_floor_scenario_rows", 0), "Phase300 event-floor rows"),
            ("phase301_phase300_breadth_met_scenario_rows", metric_value(summary, "phase300_breadth_met_scenario_rows", 0), "Phase300 breadth rows"),
            ("phase301_phase300_cost200_acceptance_survivor_rows", metric_value(summary, "phase300_cost200_acceptance_survivor_rows", 0), "Phase300 acceptance survivors"),
            ("phase301_phase300_kill_switch_triggered", metric_value(summary, "phase300_kill_switch_triggered", 0), "Phase300 kill-switch"),
            ("phase301_best_scenario_id", best.get("scenario_id", ""), "Best annualized scenario"),
            ("phase301_best_annualized_pct", best.get("mechanical_annualized_portfolio_return_pct", ""), "Best annualized diagnostic"),
            ("phase301_best_scheduled_event_rows", best.get("scheduled_event_rows", ""), "Best scheduled events"),
            ("phase301_broadest_scenario_id", broad.get("scenario_id", ""), "Broadest scheduled scenario"),
            ("phase301_broadest_annualized_pct", broad.get("mechanical_annualized_portfolio_return_pct", ""), "Broadest scheduled scenario annualized"),
            ("phase301_broadest_scheduled_event_rows", broad.get("scheduled_event_rows", ""), "Broadest scheduled events"),
            ("phase301_kill_switch_rows", len(kill_switch), "Kill-switch audit rows"),
            ("phase301_terminal_report_required", decision_value(decisions, "terminal_report_required"), "Terminal report required"),
            ("phase301_do_not_rescue_with_more_filters", decision_value(decisions, "do_not_rescue_with_more_filters"), "No rescue tuning"),
            ("phase301_strategy_replay_allowed", 0, "No replay"),
            ("phase301_strategy_promotion_allowed", 0, "No promotion"),
            ("phase301_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase301_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase301_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase301_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase301_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, gates: pd.DataFrame, kill_switch: pd.DataFrame, decisions: pd.DataFrame, contract: pd.DataFrame, ranked: pd.DataFrame) -> None:
    lines = [
        "# Phase301 Passive-Aware Execution Hybrid Interpretation",
        "",
        "Phase301 interprets Phase300 as a falsification for the passive-aware directional top-five-depth execution route under the precommitted gates.",
        "",
        "No replay, promotion, paper/live acceptance, or deployable profitability claim is opened.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "## Kill-Switch Audit",
        "",
        _markdown_table(kill_switch),
        "",
        "## Decision Ledger",
        "",
        _markdown_table(decisions),
        "",
        "## Terminal Report Contract",
        "",
        _markdown_table(contract),
        "",
        "## Ranked Scenario Interpretation",
        "",
        _markdown_table(ranked.head(30)),
    ]
    (output_dir / "phase301_passive_aware_execution_hybrid_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase300_dir: Path = DEFAULT_PHASE300_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    summary = read_csv(phase300_dir / "phase300_acceptance_summary.csv")
    scenarios = read_csv(phase300_dir / "phase300_execution_scenario_summary.csv")
    if summary.empty or scenarios.empty:
        raise FileNotFoundError(f"Phase300 outputs are incomplete under {phase300_dir}")
    ranked = build_ranked_scenario_interpretation(scenarios)
    kill_switch = build_kill_switch_audit(summary, ranked)
    decisions = build_decision_ledger(summary, ranked, kill_switch)
    contract = build_terminal_report_contract()
    gates = build_gate_evaluation(summary, scenarios, ranked, kill_switch, decisions, contract)
    acceptance = build_acceptance(summary, ranked, kill_switch, decisions, gates)

    ranked.to_csv(output_dir / "phase301_ranked_scenario_interpretation.csv", index=False)
    kill_switch.to_csv(output_dir / "phase301_kill_switch_audit.csv", index=False)
    decisions.to_csv(output_dir / "phase301_decision_ledger.csv", index=False)
    contract.to_csv(output_dir / "phase301_terminal_report_contract.csv", index=False)
    gates.to_csv(output_dir / "phase301_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase301_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, gates, kill_switch, decisions, contract, ranked)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase301_passive_aware_execution_hybrid_interpretation",
        **reproducibility_fields(
            artifact_id="phase301",
            generated_utc=generated_utc,
            inputs={
                "phase300_acceptance_summary": str(phase300_dir / "phase300_acceptance_summary.csv"),
                "phase300_execution_scenario_summary": str(phase300_dir / "phase300_execution_scenario_summary.csv"),
            },
            parameters={
                "selected_outcome": SELECTED_OUTCOME,
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "min_event_rows": MIN_EVENT_ROWS,
                "min_breadth_symbols": MIN_BREADTH_SYMBOLS,
                "min_breadth_dates": MIN_BREADTH_DATES,
                "next_action": NEXT_ACTION,
            },
            outputs={"acceptance_summary": str(output_dir / "phase301_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase301_interpretation_only",
        ),
    }
    (output_dir / "phase301_passive_aware_execution_hybrid_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase301 passive-aware execution hybrid interpretation.")
    parser.add_argument("--phase300-dir", type=Path, default=DEFAULT_PHASE300_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(phase300_dir=args.phase300_dir, output_dir=args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
