from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase363_liquidity_replenished_catalyst_impulse_diagnostic import (
    FIXED_NOTIONAL_INR,
    INITIAL_CAPITAL_INR,
    MAX_CONCURRENT_POSITIONS,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase481")
THESIS_ID = "P481_REAL_L2_CAPACITY_SENSITIVITY_PRECOMMIT"
PRIMARY_SCENARIO_ID = "P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL"
SIDE_FLIP_SCENARIO_ID = "P362_D120_I2p5_D0p25_R0p0_CONTINUATION"
NEXT_ACTION = "execute_phase482_real_l2_capacity_sensitivity_no_search_no_download_no_paper_live"
REPAIR_ACTION = "repair_phase481_real_l2_capacity_sensitivity_precommit"

PHASE480_SUMMARY = Path("outputs/phase480/phase480_acceptance_summary.csv")
PHASE480_DATES = Path("outputs/phase480/phase480_local_real_l2_date_summary.csv")
PHASE480_OVERLAP = Path("outputs/phase480/phase480_official_catalyst_overlap_by_date.csv")
PHASE400_WORK = Path("outputs/phase400/phase386_phase360_execution_work_order.csv")
PHASE401_TRADES = Path("outputs/phase401/phase387_trade_ledger.csv")
PHASE401_SCENARIOS = Path("outputs/phase401/phase387_scenario_summary.csv")
PHASE402_SUMMARY = Path("outputs/phase402/phase388_acceptance_summary.csv")


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def file_hash(path: Path) -> str:
    if not path.exists():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_capacity_policy_catalog() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "capacity_policy_id": "P481_BASELINE_MAX2_CONCURRENT",
                "policy_role": "baseline",
                "selection_rule": "reproduce Phase387 apply_capacity: sort by decision_ms, canonical_work_order_id; keep if active exits < 2",
                "max_concurrent_positions": MAX_CONCURRENT_POSITIONS,
                "per_symbol_date_cap": "",
                "per_trade_date_cap": "",
                "all_ready_events": 0,
                "acceptance_role": "primary",
            },
            {
                "capacity_policy_id": "P481_MAX3_CONCURRENT_DIAGNOSTIC",
                "policy_role": "looser_capacity_diagnostic",
                "selection_rule": "same active-exit overlap logic as baseline but max concurrent positions = 3; diagnostic because it can exceed pinned capital",
                "max_concurrent_positions": 3,
                "per_symbol_date_cap": "",
                "per_trade_date_cap": "",
                "all_ready_events": 0,
                "acceptance_role": "diagnostic_only",
            },
            {
                "capacity_policy_id": "P481_MAX5_CONCURRENT_DIAGNOSTIC",
                "policy_role": "looser_capacity_diagnostic",
                "selection_rule": "same active-exit overlap logic as baseline but max concurrent positions = 5; diagnostic because it can exceed pinned capital",
                "max_concurrent_positions": 5,
                "per_symbol_date_cap": "",
                "per_trade_date_cap": "",
                "all_ready_events": 0,
                "acceptance_role": "diagnostic_only",
            },
            {
                "capacity_policy_id": "P481_ONE_PER_SYMBOL_DATE",
                "policy_role": "breadth_first_diagnostic",
                "selection_rule": "after readiness and signal filters, keep earliest candidate per scenario, diagnostic_trade_date, symbol; diagnostic until overlap/capital feasibility is proven",
                "max_concurrent_positions": "",
                "per_symbol_date_cap": 1,
                "per_trade_date_cap": "",
                "all_ready_events": 0,
                "acceptance_role": "diagnostic_only",
            },
            {
                "capacity_policy_id": "P481_TWO_PER_TRADE_DATE",
                "policy_role": "date_balanced_diagnostic",
                "selection_rule": "after readiness and signal filters, keep earliest two candidates per scenario and diagnostic_trade_date; diagnostic until overlap/capital feasibility is proven",
                "max_concurrent_positions": "",
                "per_symbol_date_cap": "",
                "per_trade_date_cap": 2,
                "all_ready_events": 0,
                "acceptance_role": "diagnostic_only",
            },
            {
                "capacity_policy_id": "P481_ALL_READY_DIAGNOSTIC",
                "policy_role": "upper_bound_diagnostic",
                "selection_rule": "select every scheduled ready candidate; not sufficient alone for acceptance because it ignores capital overlap",
                "max_concurrent_positions": "",
                "per_symbol_date_cap": "",
                "per_trade_date_cap": "",
                "all_ready_events": 1,
                "acceptance_role": "diagnostic_only",
            },
        ]
    )


def build_execution_contract(work: pd.DataFrame, trades: pd.DataFrame) -> pd.DataFrame:
    scheduled_primary = int(
        trades.loc[trades["scenario_id"].astype(str).eq(PRIMARY_SCENARIO_ID), "canonical_work_order_id"].nunique()
    ) if not trades.empty and "scenario_id" in trades.columns else 0
    return pd.DataFrame(
        [
            ("contract_id", THESIS_ID, "Frozen Phase481 contract identifier."),
            ("input_work_order", str(PHASE400_WORK), "Use the latest 16-date adapted official-catalyst work order."),
            ("input_work_order_rows", len(work), "Expected rows in frozen work order."),
            ("input_trade_ledger", str(PHASE401_TRADES), "Reuse Phase401 event/trade features; do not rebuild signal after seeing capacity outcomes."),
            ("scheduled_primary_candidates", scheduled_primary, "Current primary scheduled candidate count before capacity policy."),
            ("primary_scenario_id", PRIMARY_SCENARIO_ID, "Frozen reversal-control scenario."),
            ("side_flip_control_scenario_id", SIDE_FLIP_SCENARIO_ID, "Frozen continuation side-flip control."),
            ("cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha cost model."),
            ("cost_multiplier", 2, "Cost200 remains required."),
            ("initial_capital_inr", INITIAL_CAPITAL_INR, "Pinned capital denominator from the executed real-L2 branch."),
            ("fixed_notional_per_trade_inr", FIXED_NOTIONAL_INR, "Pinned per-trade notional from the executed real-L2 branch."),
            ("max_acceptance_concurrent_positions", MAX_CONCURRENT_POSITIONS, "Only policies at or below this overlap cap are acceptance-feasible without increasing capital."),
            ("minimum_selected_trades", 30, "Event floor cannot be softened."),
            ("annualized_return_floor_pct", 12, "User research profitability bar retained."),
            ("full_depth_required", "L1 plus top-five market-by-price depth; levels 2-5 materiality retained", "Core project objective."),
            ("no_download_allowed", 1, "Use current local 16-date panel first."),
            ("parameter_search_allowed", 0, "No post-result tuning."),
            ("paper_live_or_profit_claim_allowed", 0, "Boundaries closed."),
        ],
        columns=["contract_key", "contract_value", "description"],
    )


def build_prior_evidence(phase480: pd.DataFrame, phase402: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    primary = scenarios.loc[scenarios["scenario_id"].astype(str).eq(PRIMARY_SCENARIO_ID)].copy() if not scenarios.empty else pd.DataFrame()
    p = primary.iloc[0].to_dict() if not primary.empty else {}
    return pd.DataFrame(
        [
            ("phase480_local_real_l2_dates", scalar(phase480, "phase480_local_real_l2_date_rows", ""), "Current local real-L2 dates."),
            ("phase480_full_32_symbol_days", scalar(phase480, "phase480_full_32_symbol_day_rows", ""), "Dates with all configured symbols present."),
            ("phase480_official_catalyst_overlap_dates", scalar(phase480, "phase480_official_catalyst_overlap_date_rows", ""), "Official-catalyst overlap dates."),
            ("phase387_scheduled_primary_candidates", p.get("scheduled_event_rows", ""), "Scheduled candidates before capacity selection."),
            ("phase387_primary_selected_trades", p.get("capacity_selected_trade_rows", ""), "Actual baseline capacity-selected trades."),
            ("phase387_primary_net_pnl_inr", p.get("net_pnl_inr", ""), "Actual baseline net PnL."),
            ("phase387_primary_annualized_return_pct", p.get("annualized_return_pct", ""), "Actual baseline annualized return."),
            ("phase388_capacity_selected_gap", scalar(phase402, "phase388_capacity_selected_gap", ""), "Remaining trade gap to 30 selected trades."),
            ("phase388_acceptance_candidate", scalar(phase402, "phase388_acceptance_candidate", ""), "Acceptance remains closed."),
        ],
        columns=["evidence_id", "value", "description"],
    )


def build_gates(phase480: pd.DataFrame, work: pd.DataFrame, trades: pd.DataFrame, catalog: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    local_dates = as_int(scalar(phase480, "phase480_local_real_l2_date_rows", 0))
    full_depth_flags_ok = (
        not work.empty
        and "full_depth_levels_1_to_5_required" in work.columns
        and "levels_2_to_5_materiality_required" in work.columns
        and work["full_depth_levels_1_to_5_required"].astype(int).eq(1).all()
        and work["levels_2_to_5_materiality_required"].astype(int).eq(1).all()
    )
    cost_ok = (
        not trades.empty
        and "cost_model_version" in trades.columns
        and trades["cost_model_version"].astype(str).eq(ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION).all()
        and "cost200_inr" in trades.columns
    )
    scheduled_primary = int(trades.loc[trades["scenario_id"].astype(str).eq(PRIMARY_SCENARIO_ID), "canonical_work_order_id"].nunique()) if not trades.empty else 0
    rows = [
        ("P481_PHASE480_COMPLETE", as_int(scalar(phase480, "phase480_comprehensive_local_real_l2_breadth_audit_complete", 0)) == 1, scalar(phase480, "phase480_comprehensive_local_real_l2_breadth_audit_complete", 0), 1),
        ("P481_CURRENT_16_DATE_PANEL_USED", local_dates >= 16, local_dates, ">=16"),
        ("P481_WORK_ORDER_PRESENT", len(work) >= 273, len(work), ">=273"),
        ("P481_PRIOR_TRADE_LEDGER_PRESENT", scheduled_primary > 0, scheduled_primary, ">0"),
        ("P481_CAPACITY_POLICY_GRID_FROZEN", len(catalog) == 6, len(catalog), 6),
        ("P481_FULL_DEPTH_L2_L5_RETAINED", full_depth_flags_ok, int(full_depth_flags_ok), 1),
        ("P481_COST200_RETAINED", cost_ok, int(cost_ok), 1),
        ("P481_NO_DOWNLOAD_OR_RETEST_NOW", contract.loc[contract["contract_key"].eq("no_download_allowed"), "contract_value"].astype(str).iloc[0] == "1", "download=0;retest=0", "both_zero"),
        ("P481_NO_PROMOTION_PAPER_LIVE_OR_CLAIM", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame(
        [{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows]
    )


def build_acceptance(gates: pd.DataFrame, work: pd.DataFrame, catalog: pd.DataFrame, phase480: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    gate_pass = int(gates["passed"].astype(bool).sum())
    gate_rows = int(len(gates))
    primary = scenarios.loc[scenarios["scenario_id"].astype(str).eq(PRIMARY_SCENARIO_ID)].copy() if not scenarios.empty else pd.DataFrame()
    p = primary.iloc[0].to_dict() if not primary.empty else {}
    return pd.DataFrame(
        [
            ("phase481_real_l2_capacity_sensitivity_precommit_complete", int(gate_pass == gate_rows), "Phase481 complete if all gates pass"),
            ("phase481_thesis_id", THESIS_ID, "Phase481 thesis"),
            ("phase481_local_real_l2_date_rows", scalar(phase480, "phase480_local_real_l2_date_rows", ""), "Local dates used"),
            ("phase481_input_work_order_rows", len(work), "Frozen work-order rows"),
            ("phase481_capacity_policy_rows", len(catalog), "Frozen capacity policies"),
            ("phase481_acceptance_feasible_policy_rows", int(catalog["acceptance_role"].astype(str).ne("diagnostic_only").sum()), "Capital-feasible acceptance policies"),
            ("phase481_prior_scheduled_primary_candidates", p.get("scheduled_event_rows", ""), "Prior scheduled primary candidates"),
            ("phase481_prior_capacity_selected_trades", p.get("capacity_selected_trade_rows", ""), "Prior baseline selected trades"),
            ("phase481_prior_net_pnl_inr", p.get("net_pnl_inr", ""), "Prior baseline net PnL"),
            ("phase481_prior_annualized_return_pct", p.get("annualized_return_pct", ""), "Prior baseline annualized return"),
            ("phase481_strategy_retest_executed_now", 0, "Precommit only"),
            ("phase481_download_executed_now", 0, "No download"),
            ("phase481_strategy_promotion_allowed", 0, "No promotion"),
            ("phase481_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase481_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase481_hard_gate_pass_rows", gate_pass, "Passed hard gates"),
            ("phase481_hard_gate_rows", gate_rows, "Hard gates"),
            ("phase481_next_best_action", NEXT_ACTION if gate_pass == gate_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, evidence: pd.DataFrame, catalog: pd.DataFrame, contract: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase481 Real-L2 Capacity Sensitivity Precommit",
        "",
        "Phase481 freezes a no-download capacity sensitivity retest for the current 16-date real-L2 official-catalyst panel. It does not execute the retest.",
        "",
        "The purpose is to determine whether the latest 25-trade result is caused by the capacity selector or by the signal economics themselves.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Prior Evidence",
        "",
        _markdown_table(evidence),
        "",
        "## Capacity Policy Catalog",
        "",
        _markdown_table(catalog),
        "",
        "## Execution Contract",
        "",
        _markdown_table(contract),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: no download, no retest in this phase, no strategy promotion, no paper/live, no deployable profitability claim.",
    ]
    (output_dir / "phase481_real_l2_capacity_sensitivity_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase480 = read_csv(PHASE480_SUMMARY)
    work = read_csv(PHASE400_WORK)
    trades = read_csv(PHASE401_TRADES)
    scenarios = read_csv(PHASE401_SCENARIOS)
    phase402 = read_csv(PHASE402_SUMMARY)
    if phase480.empty or work.empty or trades.empty or scenarios.empty or phase402.empty:
        raise FileNotFoundError("Phase481 requires Phase480 and latest Phase400-402 retest artifacts.")
    catalog = build_capacity_policy_catalog()
    contract = build_execution_contract(work, trades)
    evidence = build_prior_evidence(phase480, phase402, scenarios)
    gates = build_gates(phase480, work, trades, catalog, contract)
    acceptance = build_acceptance(gates, work, catalog, phase480, scenarios)
    catalog.to_csv(output_dir / "phase481_capacity_policy_catalog.csv", index=False)
    contract.to_csv(output_dir / "phase481_execution_contract.csv", index=False)
    evidence.to_csv(output_dir / "phase481_prior_evidence_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase481_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase481_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, evidence, catalog, contract, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase481_real_l2_capacity_sensitivity_precommit",
        **reproducibility_fields(
            artifact_id="phase481_real_l2_capacity_sensitivity_precommit",
            generated_utc=generated_utc,
            inputs={
                "phase480_summary": str(PHASE480_SUMMARY),
                "phase400_work_order": str(PHASE400_WORK),
                "phase401_trade_ledger": str(PHASE401_TRADES),
                "phase401_scenario_summary": str(PHASE401_SCENARIOS),
                "phase402_summary": str(PHASE402_SUMMARY),
            },
            parameters={
                "thesis_id": THESIS_ID,
                "primary_scenario_id": PRIMARY_SCENARIO_ID,
                "side_flip_scenario_id": SIDE_FLIP_SCENARIO_ID,
                "capacity_policy_count": len(catalog),
                "initial_capital_inr": INITIAL_CAPITAL_INR,
                "fixed_notional_inr": FIXED_NOTIONAL_INR,
                "max_acceptance_concurrent_positions": MAX_CONCURRENT_POSITIONS,
                "download_executed": False,
                "retest_executed": False,
                "phase400_work_order_sha256": file_hash(PHASE400_WORK),
                "phase401_trade_ledger_sha256": file_hash(PHASE401_TRADES),
            },
            outputs={"acceptance_summary": str(output_dir / "phase481_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase481_no_execution_precommit_only",
        ),
    }
    (output_dir / "phase481_real_l2_capacity_sensitivity_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase481 real-L2 capacity sensitivity precommit.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    out = run(args.output_dir)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
