from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, metric_value, read_csv
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE269_DIR = Path("outputs/phase269")
DEFAULT_OUTPUT_DIR = Path("outputs/phase270")
SELECTED_ROUTE = "P270_FIXED_CAPITAL_CONCURRENCY_AND_CAPACITY_RETURN_MODEL"
NEXT_ACTION = "run_phase271_fixed_capital_concurrency_and_capacity_return_analysis_no_paper_live"


def build_capital_model_contract() -> pd.DataFrame:
    rows = [
        ("initial_capital_inr", "100000;250000;500000;1000000", "Evaluate fixed starting capital scenarios instead of unlimited capital."),
        ("per_trade_notional_policy", "min(fixed_notional, available_cash / open_slot_count)", "Each event consumes capital; no order may exceed available capital."),
        ("fixed_notional_grid_inr", "25000;50000;100000", "Stress the Phase268 fixed-notional proxy under smaller and equal notionals."),
        ("max_concurrent_positions", "1;2;4;8", "Cap simultaneous exposure; overlapping events must compete for capital."),
        ("capital_reuse_rule", "capital_released_after_horizon_exit", "Capital is not reusable until the event horizon exits."),
        ("cash_drag_rule", "idle_cash_return_zero_intraday", "Unused cash earns zero intraday return."),
        ("portfolio_return_formula", "realized_net_pnl_inr / initial_capital_inr", "Only this capital-accounted formula may be called portfolio return."),
        ("annualized_portfolio_return_formula", "portfolio_return_over_observed_dates * 252 / observed_trade_dates", "Annualize only after fixed-capital event scheduling is materialized."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_concurrency_capacity_contract() -> pd.DataFrame:
    rows = [
        ("event_time_key", "trade_date;exchange;symbol;richer_event_bar_id;horizon", "Event scheduling key for capital locks."),
        ("position_exit_key", "richer_event_bar_id + horizon", "Capital is released after the modeled holding horizon."),
        ("same_symbol_overlap_policy", "keep_highest_ranked_event_when_capital_or_overlap_conflict", "Avoid stacking contradictory events in the same symbol/window."),
        ("cross_symbol_concurrency_policy", "rank_by_research_lead_score_then_allocate_until_cash_or_slot_limit", "Allocate limited capital to ranked research leads."),
        ("capacity_proxy", "event_count;symbol_count;notional_turnover;cost_stress;depth_quantity_context", "Small-event leads must pass capacity diagnostics."),
        ("turnover_limit_diagnostic", "daily_notional_turnover / initial_capital", "Record turnover pressure before acceptance."),
        ("slippage_sensitivity", "base_cost;1p5x_cost;2x_cost;additional_1bp;additional_2bp", "Capacity analysis must include extra slippage stress."),
        ("minimum_observed_dates_for_claim", ">=1_current_data_for_mechanics;>=5_future_for_portfolio_claim", "One-date current data can test mechanics, not robust annual portfolio claims."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_candidate_input_contract() -> pd.DataFrame:
    rows = [
        ("ranked_research_leads", "outputs/phase269/phase269_ranked_annualized_research_leads.csv", "Use the 17 fixed-notional annualized research leads."),
        ("variant_results", "outputs/phase268/phase268_two_lane_variant_results.csv", "Use all Phase268 variants for controls and fallback ranking."),
        ("exploratory_event_ledger", "outputs/phase268/phase268_exploratory_event_ledger.csv", "Use event-level rows for scheduling and capital locks."),
        ("acceptance_event_ledger", "outputs/phase268/phase268_acceptance_event_ledger.csv", "Expected empty until acceptance-grade candidates appear."),
        ("full_depth_source_surface", "outputs/phase254/phase254_richer_raw_top5_depth_event_bars.parquet", "Full top-five event-bar source remains the underlying signal surface."),
    ]
    return pd.DataFrame(rows, columns=["input_id", "path", "description"])


def build_return_output_contract() -> pd.DataFrame:
    rows = [
        ("capital_scenario_results", "phase271_capital_scenario_results.csv", "Portfolio return, drawdown, turnover and utilization by capital/concurrency scenario."),
        ("scheduled_event_ledger", "phase271_scheduled_event_ledger.csv", "Event-level capital allocation and rejection reasons."),
        ("candidate_capacity_diagnostics", "phase271_candidate_capacity_diagnostics.csv", "Capacity, turnover and slippage diagnostics by candidate family."),
        ("annualized_proxy_reconciliation", "phase271_annualized_proxy_reconciliation.csv", "Compare fixed-notional proxy vs capital-accounted return."),
        ("acceptance_summary", "phase271_acceptance_summary.csv", "No replay/promotion unless capital model passes gates."),
    ]
    return pd.DataFrame(rows, columns=["output_id", "planned_path", "description"])


def build_control_contract() -> pd.DataFrame:
    rows = [
        ("full_top_five_depth_required", "required", "Rows 1-5 remain mandatory for every included signal."),
        ("levels_2_to_5_materiality_required", "required", "L2-L5 materiality remains mandatory."),
        ("l1_only_candidate_allowed", "forbidden", "No L1-only candidate or capital analysis is allowed."),
        ("unlimited_capital_assumption", "forbidden", "Capital-aware return cannot assume unlimited simultaneous capital."),
        ("portfolio_return_claim_without_scheduler", "forbidden", "No portfolio return claim without event scheduling and capital locks."),
        ("fixed_notional_proxy_as_portfolio_return", "forbidden", "Phase268 annualized proxy cannot be relabeled as portfolio return."),
        ("paper_live_or_deployable_profitability_claim", "forbidden", "No paper/live or deployable profitability claim in Phase270/271."),
        ("replay_execution_now", "forbidden", "Phase270 is a precommit only."),
    ]
    return pd.DataFrame(rows, columns=["control_id", "control_status", "description"])


def build_gate_evaluation(
    phase269_dir: Path,
    capital: pd.DataFrame,
    capacity: pd.DataFrame,
    inputs: pd.DataFrame,
    outputs: pd.DataFrame,
    controls: pd.DataFrame,
) -> pd.DataFrame:
    summary = phase269_dir / "phase269_acceptance_summary.csv"
    next_route = read_csv(phase269_dir / "phase269_next_route_contract.csv")
    next_action = str(metric_value(summary, "phase269_next_best_action", ""))
    route_selected = str(metric_value(summary, "phase269_selected_next_route", ""))
    do_not_claim_portfolio = as_int(metric_value(summary, "phase269_do_not_claim_portfolio_annual_return", 0))
    do_not_replay = as_int(metric_value(summary, "phase269_do_not_promote_or_replay_phase268", 0))
    full_depth = as_int(metric_value(summary, "phase269_phase268_full_depth_variant_rows", 0))
    variants = as_int(metric_value(summary, "phase269_phase268_variant_rows", 0))
    l2_l5 = as_int(metric_value(summary, "phase269_phase268_l2_l5_variant_rows", 0))
    l1_only = as_int(metric_value(summary, "phase269_phase268_l1_only_variant_rows", 1))
    capital_contract_present = int(next_route["contract_id"].astype(str).eq("P270_CAPITAL_ACCOUNTING").sum()) if not next_route.empty else 0
    capacity_contract_present = int(next_route["contract_id"].astype(str).eq("P270_CAPACITY_ACCOUNTING").sum()) if not next_route.empty else 0
    rows = [
        ("P270_PHASE269_WORK_ORDER_PRESENT", "run_phase270_fixed_capital_concurrency_and_capacity_return_precommit" in next_action, next_action, "Phase269 next action targets Phase270", "hard"),
        ("P270_PHASE269_ROUTE_SELECTED", "P269_FIXED_CAPITAL_CONCURRENCY_AND_CAPACITY_RETURN_PRECOMMIT" in route_selected, route_selected, "Phase269 selected fixed-capital route", "hard"),
        ("P270_PHASE269_FORBIDS_PORTFOLIO_CLAIM", do_not_claim_portfolio == 1, do_not_claim_portfolio, "Phase269 forbids portfolio-return claim", "hard"),
        ("P270_PHASE269_FORBIDS_REPLAY", do_not_replay == 1, do_not_replay, "Phase269 forbids replay/promotion", "hard"),
        ("P270_PHASE269_FULL_DEPTH_RECOGNIZED", full_depth == variants and l2_l5 == variants and l1_only == 0 and variants > 0, f"full_depth={full_depth};l2_l5={l2_l5};l1_only={l1_only};variants={variants}", "Full-depth Phase268 evidence recognized", "hard"),
        ("P270_PHASE269_CAPITAL_CONTRACT_PRESENT", capital_contract_present >= 1, capital_contract_present, "Phase269 next route contains capital accounting", "hard"),
        ("P270_PHASE269_CAPACITY_CONTRACT_PRESENT", capacity_contract_present >= 1, capacity_contract_present, "Phase269 next route contains capacity accounting", "hard"),
        ("P270_CAPITAL_MODEL_CONTRACT_WRITTEN", len(capital) >= 8, len(capital), "Capital model contract rows written", "hard"),
        ("P270_CONCURRENCY_CAPACITY_CONTRACT_WRITTEN", len(capacity) >= 8, len(capacity), "Concurrency/capacity rows written", "hard"),
        ("P270_INPUT_CONTRACT_WRITTEN", len(inputs) >= 5, len(inputs), "Input contract rows written", "hard"),
        ("P270_OUTPUT_CONTRACT_WRITTEN", len(outputs) >= 5, len(outputs), "Phase271 output contract rows written", "hard"),
        ("P270_CONTROLS_WRITTEN", int(controls["control_status"].astype(str).eq("forbidden").sum()) >= 5 and int(controls["control_status"].astype(str).eq("required").sum()) >= 2, len(controls), "Required and forbidden controls written", "hard"),
        ("P270_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase270 Fixed-capital Concurrency and Capacity Return Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase270 precommits the capital-aware return model required after Phase269 preserved fixed-notional annualized research leads.",
        "The purpose is to prevent fixed-notional annualized proxies from being mistaken for portfolio annual return.",
        "Full Zerodha top-five market-by-price rows 1-5 and levels 2-5 remain mandatory; L1-only candidates remain forbidden.",
        "This is not replay execution, strategy promotion, paper/live acceptance, or a deployable profitability claim.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase269_dir: Path = DEFAULT_PHASE269_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    capital = build_capital_model_contract()
    capacity = build_concurrency_capacity_contract()
    inputs = build_candidate_input_contract()
    outputs = build_return_output_contract()
    controls = build_control_contract()
    gates = build_gate_evaluation(phase269_dir, capital, capacity, inputs, outputs, controls)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    next_action = NEXT_ACTION if hard_pass == len(hard) else "repair_phase270_fixed_capital_precommit"
    acceptance = pd.DataFrame(
        [
            ("phase270_fixed_capital_precommit_complete", 1, "Phase270 fixed-capital/concurrency/capacity precommit completed"),
            ("phase270_selected_route", SELECTED_ROUTE, "Selected route"),
            ("phase270_phase269_interpretation_complete", as_int(metric_value(phase269_dir / "phase269_acceptance_summary.csv", "phase269_interpretation_complete", 0)), "Phase269 interpretation complete"),
            ("phase270_phase269_research_leads_preserved", as_int(metric_value(phase269_dir / "phase269_acceptance_summary.csv", "phase269_preserve_research_leads", 0)), "Phase269 preserved research leads"),
            ("phase270_phase269_do_not_claim_portfolio_annual_return", as_int(metric_value(phase269_dir / "phase269_acceptance_summary.csv", "phase269_do_not_claim_portfolio_annual_return", 0)), "Portfolio annual return claim forbidden"),
            ("phase270_phase269_do_not_promote_or_replay", as_int(metric_value(phase269_dir / "phase269_acceptance_summary.csv", "phase269_do_not_promote_or_replay_phase268", 0)), "Replay/promotion forbidden"),
            ("phase270_capital_model_contract_rows", len(capital), "Capital model contract rows"),
            ("phase270_concurrency_capacity_contract_rows", len(capacity), "Concurrency/capacity contract rows"),
            ("phase270_candidate_input_contract_rows", len(inputs), "Candidate input contract rows"),
            ("phase270_return_output_contract_rows", len(outputs), "Return output contract rows"),
            ("phase270_control_contract_rows", len(controls), "Control contract rows"),
            ("phase270_full_top_five_depth_required", 1, "Zerodha rows 1-5 required"),
            ("phase270_levels_2_to_5_materiality_required", 1, "Levels 2-5 materiality required"),
            ("phase270_l1_only_candidate_allowed", 0, "L1-only candidates forbidden"),
            ("phase270_unlimited_capital_assumption_allowed", 0, "Unlimited capital assumption forbidden"),
            ("phase270_portfolio_return_claim_without_scheduler_allowed", 0, "Portfolio return claim without scheduler forbidden"),
            ("phase270_fixed_notional_proxy_as_portfolio_return_allowed", 0, "Fixed-notional proxy cannot be relabeled portfolio return"),
            ("phase270_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase270_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase270_download_more_dates_now_allowed", 0, "No new download in Phase270"),
            ("phase270_replay_execution_allowed_now", 0, "No replay execution in Phase270"),
            ("phase270_strategy_promotion_allowed", 0, "No strategy promotion from Phase270"),
            ("phase270_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase270"),
            ("phase270_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase270"),
            ("phase270_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    capital.to_csv(output_dir / "phase270_capital_model_contract.csv", index=False)
    capacity.to_csv(output_dir / "phase270_concurrency_capacity_contract.csv", index=False)
    inputs.to_csv(output_dir / "phase270_candidate_input_contract.csv", index=False)
    outputs.to_csv(output_dir / "phase270_return_output_contract.csv", index=False)
    controls.to_csv(output_dir / "phase270_control_contract.csv", index=False)
    gates.to_csv(output_dir / "phase270_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase270_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase270_fixed_capital_concurrency_and_capacity_return_precommit_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Capital Model Contract": capital,
            "Concurrency and Capacity Contract": capacity,
            "Candidate Input Contract": inputs,
            "Return Output Contract": outputs,
            "Control Contract": controls,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase270_fixed_capital_concurrency_and_capacity_return_precommit",
        **reproducibility_fields(
            artifact_id="phase270",
            generated_utc=generated_utc,
            inputs={"phase269_dir": str(phase269_dir)},
            parameters={
                "selected_route": SELECTED_ROUTE,
                "full_top_five_depth_required": 1,
                "levels_2_to_5_materiality_required": 1,
                "l1_only_candidate_allowed": 0,
                "unlimited_capital_assumption_allowed": 0,
                "portfolio_return_claim_without_scheduler_allowed": 0,
                "fixed_notional_proxy_as_portfolio_return_allowed": 0,
                "download_more_dates_now_allowed": 0,
                "replay_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "capital_model_contract": str(output_dir / "phase270_capital_model_contract.csv"),
                "concurrency_capacity_contract": str(output_dir / "phase270_concurrency_capacity_contract.csv"),
                "candidate_input_contract": str(output_dir / "phase270_candidate_input_contract.csv"),
                "return_output_contract": str(output_dir / "phase270_return_output_contract.csv"),
                "control_contract": str(output_dir / "phase270_control_contract.csv"),
                "gate_evaluation": str(output_dir / "phase270_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase270_acceptance_summary.csv"),
                "report": str(output_dir / "phase270_fixed_capital_concurrency_and_capacity_return_precommit_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase270_no_replay_capital_contract",
        ),
    }
    (output_dir / "phase270_fixed_capital_concurrency_and_capacity_return_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase270 fixed-capital/concurrency/capacity return precommit.")
    parser.add_argument("--phase269-dir", type=Path, default=DEFAULT_PHASE269_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase269_dir=args.phase269_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
