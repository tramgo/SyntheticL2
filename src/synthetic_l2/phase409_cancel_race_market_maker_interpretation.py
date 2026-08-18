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


DEFAULT_PHASE407_DIR = Path("outputs/phase407")
DEFAULT_PHASE408_DIR = Path("outputs/phase408")
DEFAULT_OUTPUT_DIR = Path("outputs/phase409")

SELECTED_VERDICT = "P409_CANCEL_RACE_MARKET_MAKER_FALSIFIED"
NEXT_ACTION = "stop_retail_two_sided_top5_l2_market_maker_route_or_require_new_external_execution_source"
REPAIR_ACTION = "repair_phase409_cancel_race_market_maker_interpretation"


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def build_terminal_verdict(summary408: pd.DataFrame, gates408: pd.DataFrame, synthetic_diag: pd.DataFrame, real_scenarios: pd.DataFrame) -> pd.DataFrame:
    failed = gates408.loc[gates408["passed"].astype(str).str.lower().isin(["false", "0"])]
    cancel_attempts = int(pd.to_numeric(synthetic_diag.get("cancel_attempted", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()) if not synthetic_diag.empty else 0
    cancel_succeeded = int(pd.to_numeric(synthetic_diag.get("cancel_succeeded", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()) if not synthetic_diag.empty else 0
    cancel_lost = int(pd.to_numeric(synthetic_diag.get("cancel_lost_race", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()) if not synthetic_diag.empty else 0
    real_best = real_scenarios.sort_values("annualized_return_pct", ascending=False, kind="mergesort").iloc[0] if not real_scenarios.empty else pd.Series(dtype=object)
    return pd.DataFrame(
        [
            ("selected_verdict", SELECTED_VERDICT, "No cost200 survivor and kill-switch fired.", "terminal_for_tested_route"),
            ("p263_closure_upgrade", "conservative_zero_cancel_to_cancel_race_falsified", "Phase408 added realistic cancel latency and still failed.", "upgrade"),
            ("phase408_best_annualized_return_pct", metric_value(summary408, "phase408_best_annualized_return_pct", ""), "Best synthetic scenario annualized return.", "failed_profitability"),
            ("phase408_best_completed_round_trips", metric_value(summary408, "phase408_best_completed_round_trips", ""), "Event floor was met.", "passed_event_floor"),
            ("phase408_best_trade_dates", metric_value(summary408, "phase408_best_trade_dates", ""), "Date breadth was met.", "passed_date_breadth"),
            ("phase408_best_symbols", metric_value(summary408, "phase408_best_symbols", ""), "Symbol breadth was met.", "passed_symbol_breadth"),
            ("phase408_positive_date_fraction", metric_value(summary408, "phase408_best_positive_date_fraction", ""), "Every synthetic date was net negative.", "failed_positive_date_fraction"),
            ("phase408_acceptance_survivors", metric_value(summary408, "phase408_cost200_acceptance_survivor_rows", ""), "Zero accepted scenarios.", "failed_acceptance"),
            ("phase408_failed_hard_gates", ";".join(failed["gate_id"].astype(str).tolist()), "Failed gates.", "kill_switch_basis"),
            ("synthetic_cancel_attempts", cancel_attempts, "Cancel attempts logged in per-tick loop.", "diagnostic"),
            ("synthetic_cancel_succeeded", cancel_succeeded, "No synthetic cancel succeeded before fill in this bounded run.", "diagnostic"),
            ("synthetic_cancel_lost_race", cancel_lost, "Cancel attempts that lost the race.", "diagnostic"),
            ("real_anchor_best_annualized_return_pct", real_best.get("annualized_return_pct", ""), "Reserved real-anchor replay also negative.", "cross_check"),
            ("same_family_tuning_allowed", 0, "Charter has no third tune-it outcome.", "forbidden"),
            ("paper_live_or_profit_claim", 0, "promotion=0;paper=0;claim=0", "closed"),
            ("next_action", NEXT_ACTION, "Only a new external execution source could reopen this retail maker route.", "next"),
        ],
        columns=["verdict_id", "verdict_value", "evidence", "status"],
    )


def build_byproducts() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("P409_PER_TICK_CANCEL_RACE_HARNESS", "reusable_infrastructure", "Reusable for future order-lifecycle realism tests.", "Not evidence of true exchange queue identity."),
            ("P409_LATENCY_GRID_AND_JITTER", "reusable_latency_model", "Pinned cancel-latency scenarios and deterministic jitter.", "Do not use sub-100ms retail fantasy latency."),
            ("P409_CANCEL_LOST_RACE_LEDGER", "negative_evidence", "Shows cancel attempts losing to fills in the tested windows.", "Do not treat as broker-confirmed fills."),
            ("P409_ZERODHA_COST200_APPLICATION", "reusable_cost_model", "Applies pinned Zerodha equity intraday cost model under 2x stress.", "Do not weaken costs to rescue maker economics."),
            ("P409_REAL_ANCHOR_REPLAY_PATH", "cross_check_infrastructure", "Reserved real-anchor replay path for local Zerodha L2 days.", "Not paper/live or contract-note reconciliation."),
        ],
        columns=["byproduct_id", "classification", "kept_for", "not_kept_for"],
    )


def build_gate_evaluation(summary408: pd.DataFrame, gates408: pd.DataFrame, verdict: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(summary408, "phase408_per_tick_cancel_race_market_maker_complete", 0))
    survivors = as_int(metric_value(summary408, "phase408_cost200_acceptance_survivor_rows", 0))
    kill = as_int(metric_value(summary408, "phase408_kill_switch_triggered", 0))
    failed = gates408.loc[gates408["passed"].astype(str).str.lower().isin(["false", "0"])]
    gates = [
        ("P409_PHASE408_COMPLETE", complete == 1, complete, 1),
        ("P409_CANCEL_RACE_GATES_EVALUATED", len(gates408) == 18, len(gates408), 18),
        ("P409_NO_COST200_SURVIVORS", survivors == 0, survivors, 0),
        ("P409_KILL_SWITCH_FIRED", kill == 1, kill, 1),
        ("P409_FAILED_GATE_BASIS_PRESENT", len(failed) > 0, ";".join(failed["gate_id"].astype(str).tolist()), ">0"),
        ("P409_TERMINAL_VERDICT_PRESENT", str(verdict.loc[verdict["verdict_id"].eq("selected_verdict"), "verdict_value"].iloc[0]) == SELECTED_VERDICT, SELECTED_VERDICT, SELECTED_VERDICT),
        ("P409_NO_TUNE_IT_OUTCOME", str(verdict.loc[verdict["verdict_id"].eq("same_family_tuning_allowed"), "verdict_value"].iloc[0]) == "0", 0, 0),
        ("P409_BOUNDARIES_CLOSED", str(verdict.loc[verdict["verdict_id"].eq("paper_live_or_profit_claim"), "verdict_value"].iloc[0]) == "0", "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(summary408: pd.DataFrame, gates408: pd.DataFrame, verdict: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase409_cancel_race_market_maker_interpretation_complete", 1, "Phase409 interpretation completed"),
            ("phase409_selected_verdict", SELECTED_VERDICT, "Selected verdict"),
            ("phase409_phase408_best_completed_round_trips", metric_value(summary408, "phase408_best_completed_round_trips", ""), "Best round trips"),
            ("phase409_phase408_best_trade_dates", metric_value(summary408, "phase408_best_trade_dates", ""), "Best trade dates"),
            ("phase409_phase408_best_symbols", metric_value(summary408, "phase408_best_symbols", ""), "Best symbols"),
            ("phase409_phase408_best_positive_date_fraction", metric_value(summary408, "phase408_best_positive_date_fraction", ""), "Positive date fraction"),
            ("phase409_phase408_best_net_pnl_inr", metric_value(summary408, "phase408_best_net_pnl_inr", ""), "Best net PnL"),
            ("phase409_phase408_best_annualized_return_pct", metric_value(summary408, "phase408_best_annualized_return_pct", ""), "Best annualized return"),
            ("phase409_phase408_cost200_acceptance_survivor_rows", metric_value(summary408, "phase408_cost200_acceptance_survivor_rows", ""), "Acceptance survivors"),
            ("phase409_phase408_failed_hard_gate_rows", len(gates408.loc[gates408["passed"].astype(str).str.lower().isin(["false", "0"])]), "Failed Phase408 hard gates"),
            ("phase409_p263_closure_upgraded_to_strong_falsification", 1, "P263 closure upgraded for tested cancel-race route"),
            ("phase409_same_family_tuning_allowed", 0, "No tune-it outcome"),
            ("phase409_strategy_promotion_allowed", 0, "No promotion"),
            ("phase409_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase409_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase409_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase409_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase409_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, verdict: pd.DataFrame, byproducts: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase409 Cancel-Race Market-Maker Interpretation",
        "",
        "Phase409 interprets the Phase408 per-tick cancel-race market-maker run required by the Phase407 charter.",
        "",
        "The tested retail two-sided top-five L2 quoting route is falsified under the honest cancel-race model: no cost200 survivor, kill-switch fired, no tune-it outcome.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Terminal Verdict Ledger",
        "",
        _markdown_table(verdict),
        "",
        "## Durable Byproducts",
        "",
        _markdown_table(byproducts),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: this is not paper/live evidence and does not claim broker-confirmed queue priority or fills.",
    ]
    (output_dir / "phase409_cancel_race_market_maker_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase407_dir: Path = DEFAULT_PHASE407_DIR, phase408_dir: Path = DEFAULT_PHASE408_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    summary408 = read_csv(phase408_dir / "phase408_acceptance_summary.csv")
    gates408 = read_csv(phase408_dir / "phase408_gate_evaluation.csv")
    synthetic_diag = read_csv(phase408_dir / "phase408_synthetic_cancel_race_diagnostics.csv")
    real_scenarios = read_csv(phase408_dir / "phase408_real_anchor_scenario_summary.csv")
    if summary408.empty or gates408.empty or synthetic_diag.empty or real_scenarios.empty:
        raise FileNotFoundError("Phase409 requires Phase408 summary, gates, diagnostics and real-anchor scenarios.")
    verdict = build_terminal_verdict(summary408, gates408, synthetic_diag, real_scenarios)
    byproducts = build_byproducts()
    gates = build_gate_evaluation(summary408, gates408, verdict)
    acceptance = build_acceptance(summary408, gates408, verdict, gates)
    verdict.to_csv(output_dir / "phase409_terminal_verdict_ledger.csv", index=False)
    byproducts.to_csv(output_dir / "phase409_durable_byproduct_catalog.csv", index=False)
    gates.to_csv(output_dir / "phase409_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase409_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, verdict, byproducts, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase409_cancel_race_market_maker_interpretation",
        **reproducibility_fields(
            artifact_id="phase409_cancel_race_market_maker_interpretation",
            generated_utc=generated_utc,
            inputs={
                "phase407_acceptance_summary": str(phase407_dir / "phase407_acceptance_summary.csv"),
                "phase408_acceptance_summary": str(phase408_dir / "phase408_acceptance_summary.csv"),
                "phase408_gate_evaluation": str(phase408_dir / "phase408_gate_evaluation.csv"),
                "phase408_synthetic_cancel_race_diagnostics": str(phase408_dir / "phase408_synthetic_cancel_race_diagnostics.csv"),
                "phase408_real_anchor_scenario_summary": str(phase408_dir / "phase408_real_anchor_scenario_summary.csv"),
            },
            parameters={"selected_verdict": SELECTED_VERDICT, "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase409_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase407_precommitted_cancel_latency_grid",
        ),
    }
    (output_dir / "phase409_cancel_race_market_maker_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase409 cancel-race market-maker interpretation.")
    parser.add_argument("--phase407-dir", type=Path, default=DEFAULT_PHASE407_DIR)
    parser.add_argument("--phase408-dir", type=Path, default=DEFAULT_PHASE408_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase407_dir, args.phase408_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
