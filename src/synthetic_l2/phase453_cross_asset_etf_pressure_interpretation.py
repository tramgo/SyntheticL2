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


DEFAULT_PHASE452_DIR = Path("outputs/phase452")
DEFAULT_OUTPUT_DIR = Path("outputs/phase453")

THESIS_ID = "P453_CROSS_ASSET_ETF_PRESSURE_INTERPRETATION"
SELECTED_VERDICT = "P453_CROSS_ASSET_ETF_PRESSURE_EXECUTION_ACCESS_REPAIR_REQUIRED"
NEXT_ACTION = "precommit_phase454_contiguous_tick_window_cross_asset_etf_pressure_no_results"


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def build_decision(acceptance452: pd.DataFrame, gates452: pd.DataFrame) -> pd.DataFrame:
    failed = gates452[~gates452["passed"].astype(str).str.lower().isin(["true", "1"])]
    rows = [
        ("selected_verdict", SELECTED_VERDICT, "Phase452 did not produce executable trades because sparse stride conflicted with fixed tick horizon.", "repair_execution_access"),
        ("phase452_completed_round_trips", scalar(acceptance452, "phase452_best_completed_round_trips", ""), "Observed Phase452 trades.", "zero_is_not_strategy_edge_evidence"),
        ("phase452_acceptance_survivor", scalar(acceptance452, "phase452_acceptance_survivor", ""), "No survivor.", 0),
        ("failed_gate_ids", ";".join(failed["gate_id"].astype(str).tolist()), "Failed hard gates.", "basis"),
        ("cross_asset_source_closed", 0, "Source is not closed by zero-trade execution-access failure.", 0),
        ("phase451_stride_contract_closed", 1, "The sparse-stride plus 240-tick-horizon access contract is closed.", 1),
        ("profitability_claim_allowed", 0, "Zero-trade execution does not imply profitability.", 0),
        ("paper_live_or_promotion_allowed", 0, "No paper/live or promotion.", 0),
        ("next_action", NEXT_ACTION, "Repair with contiguous raw tick windows before execution.", "precommit_repair_first"),
    ]
    return pd.DataFrame(rows, columns=["decision_id", "decision_value", "description", "required_or_implication"])


def build_repair_contract() -> pd.DataFrame:
    rows = [
        ("repair_source", "same_cross_asset_etf_pressure_source", "Not a new alpha result; repairs data-access mechanics."),
        ("required_change", "contiguous_raw_tick_windows_per_symbol_date", "Retain at least EVENT_INDEX + horizon + guard rows per date."),
        ("forbidden_change", "no_threshold_relaxation_or_side_rule_change", "No signal rescue after seeing Phase452."),
        ("horizon_ticks", "240", "Keep Phase451 frozen horizon."),
        ("entry_index", "20", "Keep Phase452 event index."),
        ("max_events_per_target_date", "1", "Keep low-turnover cap."),
        ("cost_model", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Keep cost model."),
        ("cost_multiplier", "2.0", "Keep cost200."),
        ("capital_policy", "fixed_initial_capital_1000000_inr_order_notional_100000_inr_cost200", "Keep fixed capital/notional."),
        ("execution_results_generated_now", "0", "Phase453 interpretation only."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_gates(decision: pd.DataFrame, acceptance452: pd.DataFrame, repair: pd.DataFrame) -> pd.DataFrame:
    gates = [
        ("P453_PHASE452_COMPLETE", as_int(scalar(acceptance452, "phase452_cross_asset_execution_complete", 0)) == 1, scalar(acceptance452, "phase452_cross_asset_execution_complete", 0), 1),
        ("P453_ZERO_TRADE_BASIS_RECORDED", as_int(scalar(acceptance452, "phase452_best_completed_round_trips", -1)) == 0, scalar(acceptance452, "phase452_best_completed_round_trips", -1), 0),
        ("P453_SOURCE_NOT_FALSELY_CLOSED", str(decision.loc[decision["decision_id"].eq("cross_asset_source_closed"), "decision_value"].iloc[0]) == "0", 0, 0),
        ("P453_STRIDE_CONTRACT_CLOSED", str(decision.loc[decision["decision_id"].eq("phase451_stride_contract_closed"), "decision_value"].iloc[0]) == "1", 1, 1),
        ("P453_REPAIR_CONTRACT_PRESENT", len(repair) >= 8, len(repair), ">=8"),
        ("P453_NO_RESULTS_GENERATED", repair.loc[repair["contract_id"].eq("execution_results_generated_now"), "contract_value"].astype(str).str.cat(sep=" ") == "0", repair.loc[repair["contract_id"].eq("execution_results_generated_now"), "contract_value"].astype(str).str.cat(sep=" "), 0),
        ("P453_BOUNDARIES_CLOSED", str(decision.loc[decision["decision_id"].eq("paper_live_or_promotion_allowed"), "decision_value"].iloc[0]) == "0" and str(decision.loc[decision["decision_id"].eq("profitability_claim_allowed"), "decision_value"].iloc[0]) == "0", "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    rows = [
        ("phase453_cross_asset_interpretation_complete", 1, "Phase453 interpretation completed"),
        ("phase453_thesis_id", THESIS_ID, "Interpretation thesis"),
        ("phase453_selected_verdict", SELECTED_VERDICT, "Selected verdict"),
        ("phase453_cross_asset_source_closed", 0, "Source remains eligible only under repaired access contract"),
        ("phase453_stride_contract_closed", 1, "Sparse stride/horizon contract closed"),
        ("phase453_execution_results_generated", 0, "Interpretation only"),
        ("phase453_strategy_promotion_allowed", 0, "No promotion"),
        ("phase453_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase453_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase453_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase453_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase453_next_best_action", NEXT_ACTION, "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, decision: pd.DataFrame, repair: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase453 Cross-Asset ETF Pressure Interpretation",
        "",
        "Phase453 interprets Phase452 as an execution-access failure: sparse stride sampling was incompatible with a fixed 240-tick horizon after month filtering.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Decision Ledger",
        "",
        _markdown_table(decision),
        "",
        "## Required Repair Contract",
        "",
        _markdown_table(repair),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: the cross-asset source may be retested only after a new precommit that repairs contiguous raw tick-window access without changing signal thresholds or side rules.",
    ]
    (output_dir / "phase453_cross_asset_etf_pressure_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase452_dir: Path = DEFAULT_PHASE452_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    acceptance452 = read_csv(phase452_dir / "phase452_acceptance_summary.csv")
    gates452 = read_csv(phase452_dir / "phase452_gate_evaluation.csv")
    if acceptance452.empty or gates452.empty:
        raise FileNotFoundError("Phase453 requires Phase452 acceptance and gate evaluation.")
    decision = build_decision(acceptance452, gates452)
    repair = build_repair_contract()
    gates = build_gates(decision, acceptance452, repair)
    acceptance = build_acceptance(gates)
    decision.to_csv(output_dir / "phase453_decision_ledger.csv", index=False)
    repair.to_csv(output_dir / "phase453_required_repair_contract.csv", index=False)
    gates.to_csv(output_dir / "phase453_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase453_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, decision, repair, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase453_cross_asset_etf_pressure_interpretation",
        **reproducibility_fields(
            artifact_id="phase453_cross_asset_etf_pressure_interpretation",
            generated_utc=generated_utc,
            inputs={"phase452_acceptance_summary": str(phase452_dir / "phase452_acceptance_summary.csv"), "phase452_gate_evaluation": str(phase452_dir / "phase452_gate_evaluation.csv")},
            parameters={"thesis_id": THESIS_ID, "selected_verdict": SELECTED_VERDICT},
            outputs={"acceptance_summary": str(output_dir / "phase453_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase452_cross_asset_fixed_tick_horizon",
        ),
    }
    (output_dir / "phase453_cross_asset_etf_pressure_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase453 cross-asset ETF pressure interpretation.")
    parser.add_argument("--phase452-dir", type=Path, default=DEFAULT_PHASE452_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase452_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
