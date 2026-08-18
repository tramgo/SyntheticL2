from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE415_DIR = Path("outputs/phase415")
DEFAULT_OUTPUT_DIR = Path("outputs/phase416")

VERDICT = "P416_DEEP_BOOK_DIVERGENCE_SNAPBACK_REJECTED_NON_SPARSE_NEGATIVE"
NEXT_ACTION = "stop_deep_book_divergence_snapback_route_or_precommit_material_new_non_directional_full_depth_source"
REPAIR_ACTION = "repair_phase416_interpretation"


def failed_gates(gates: pd.DataFrame) -> str:
    if gates.empty:
        return ""
    failed = gates.loc[gates["passed"].astype(str).str.lower().isin(["false", "0"])]
    return ";".join(failed["gate_id"].astype(str).tolist())


def build_decision(summary: pd.DataFrame, gates415: pd.DataFrame, scenario_summary: pd.DataFrame) -> pd.DataFrame:
    primary = scenario_summary[scenario_summary["scenario_id"].eq("P415_PRIMARY_DEEP_BOOK_DIVERGENCE_SNAPBACK")]
    p = primary.iloc[0] if not primary.empty else pd.Series(dtype=object)
    return pd.DataFrame(
        [
            ("selected_verdict", VERDICT, "Enough events/breadth, but negative cost200 result.", "terminal_for_this_route"),
            ("primary_completed_round_trips", p.get("completed_round_trips", metric_value(summary, "phase415_primary_completed_round_trips", 0)), "Event floor passed.", "non_sparse"),
            ("primary_trade_dates", p.get("trade_dates", metric_value(summary, "phase415_primary_trade_dates", 0)), "Date breadth passed.", "non_sparse"),
            ("primary_symbols", p.get("symbols", metric_value(summary, "phase415_primary_symbols", 0)), "Symbol breadth passed.", "non_sparse"),
            ("primary_positive_date_fraction", p.get("positive_date_fraction", metric_value(summary, "phase415_primary_positive_date_fraction", 0)), "Failed positive-date fraction.", "failure"),
            ("primary_net_pnl_inr", p.get("net_pnl_inr", metric_value(summary, "phase415_primary_net_pnl_inr", 0)), "Net P&L after cost200.", "failure"),
            ("primary_annualized_return_pct", p.get("annualized_return_pct", metric_value(summary, "phase415_primary_annualized_return_pct", 0)), "Failed annualized floor.", "failure"),
            ("cost200_acceptance_survivor_rows", metric_value(summary, "phase415_cost200_acceptance_survivor_rows", 0), "No accepted scenario.", "failure"),
            ("phase415_failed_hard_gates", failed_gates(gates415), "Explicit failed gate basis.", "basis"),
            ("same_family_tuning_allowed", 0, "Do not tune this route after broad negative evidence.", "closed"),
            ("strategy_promotion_allowed", 0, "No accepted survivor.", "closed"),
            ("paper_or_live_acceptance_allowed", 0, "No paper/live acceptance.", "closed"),
            ("deployable_profitability_claim_allowed", 0, "No deployable claim.", "closed"),
            ("next_action", NEXT_ACTION, "Move away from this directional snapback route.", "next"),
        ],
        columns=["decision_id", "decision_value", "evidence", "status"],
    )


def build_gate_evaluation(summary: pd.DataFrame, gates415: pd.DataFrame, decision: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(summary, "phase415_deep_book_divergence_snapback_execution_complete", 0))
    trips = as_int(metric_value(summary, "phase415_primary_completed_round_trips", 0))
    dates = as_int(metric_value(summary, "phase415_primary_trade_dates", 0))
    symbols = as_int(metric_value(summary, "phase415_primary_symbols", 0))
    survivors = as_int(metric_value(summary, "phase415_cost200_acceptance_survivor_rows", 0))
    annualized = float(metric_value(summary, "phase415_primary_annualized_return_pct", 0))
    gates = [
        ("P416_PHASE415_COMPLETE", complete == 1, complete, 1),
        ("P416_PHASE415_GATES_EVALUATED", len(gates415) == 21, len(gates415), 21),
        ("P416_NON_SPARSE_EVENT_EVIDENCE", trips >= 30 and dates >= 5 and symbols >= 3, f"trips={trips};dates={dates};symbols={symbols}", "event_date_symbol_breadth"),
        ("P416_NEGATIVE_COST200_CONFIRMED", annualized < 0, annualized, "<0"),
        ("P416_NO_COST200_SURVIVORS", survivors == 0, survivors, 0),
        ("P416_VERDICT_PRESENT", str(decision.loc[decision["decision_id"].eq("selected_verdict"), "decision_value"].iloc[0]) == VERDICT, VERDICT, VERDICT),
        ("P416_NO_SAME_FAMILY_TUNING", str(decision.loc[decision["decision_id"].eq("same_family_tuning_allowed"), "decision_value"].iloc[0]) == "0", 0, 0),
        ("P416_BOUNDARIES_CLOSED", str(decision.loc[decision["decision_id"].eq("paper_or_live_acceptance_allowed"), "decision_value"].iloc[0]) == "0", "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase416_deep_book_divergence_snapback_interpretation_complete", 1, "Phase416 interpretation completed"),
            ("phase416_selected_verdict", VERDICT, "Selected verdict"),
            ("phase416_phase415_primary_completed_round_trips", metric_value(summary, "phase415_primary_completed_round_trips", 0), "Primary round trips"),
            ("phase416_phase415_primary_positive_date_fraction", metric_value(summary, "phase415_primary_positive_date_fraction", 0), "Primary positive date fraction"),
            ("phase416_phase415_primary_net_pnl_inr", metric_value(summary, "phase415_primary_net_pnl_inr", 0), "Primary net P&L"),
            ("phase416_phase415_primary_annualized_return_pct", metric_value(summary, "phase415_primary_annualized_return_pct", 0), "Primary annualized return"),
            ("phase416_cost200_acceptance_survivor_rows", metric_value(summary, "phase415_cost200_acceptance_survivor_rows", 0), "Acceptance survivors"),
            ("phase416_same_family_tuning_allowed", 0, "No same-family tuning"),
            ("phase416_strategy_promotion_allowed", 0, "No promotion"),
            ("phase416_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase416_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase416_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase416_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase416_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, decision: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase416 Deep-Book Divergence Snapback Interpretation",
        "",
        "Phase416 formally interprets the non-sparse but negative Phase415 result.",
        "",
        "The route is rejected for acceptance: it generated enough trades and breadth, but every date was non-positive and annualized return was deeply negative after cost200.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Decision Ledger",
        "",
        _markdown_table(decision),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: do not tune the same deep-book divergence snapback route after this negative result.",
    ]
    (output_dir / "phase416_deep_book_divergence_snapback_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase415_dir: Path = DEFAULT_PHASE415_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    summary = read_csv(phase415_dir / "phase415_acceptance_summary.csv")
    gates415 = read_csv(phase415_dir / "phase415_gate_evaluation.csv")
    scenario_summary = read_csv(phase415_dir / "phase415_synthetic_scenario_summary.csv")
    if summary.empty or gates415.empty or scenario_summary.empty:
        raise FileNotFoundError("Phase416 requires Phase415 summary, gates and scenario summary.")
    decision = build_decision(summary, gates415, scenario_summary)
    gates = build_gate_evaluation(summary, gates415, decision)
    acceptance = build_acceptance(summary, gates)
    decision.to_csv(output_dir / "phase416_decision_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase416_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase416_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, decision, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase416_deep_book_divergence_snapback_interpretation",
        **reproducibility_fields(
            artifact_id="phase416_deep_book_divergence_snapback_interpretation",
            generated_utc=generated_utc,
            inputs={
                "phase415_acceptance_summary": str(phase415_dir / "phase415_acceptance_summary.csv"),
                "phase415_gate_evaluation": str(phase415_dir / "phase415_gate_evaluation.csv"),
                "phase415_synthetic_scenario_summary": str(phase415_dir / "phase415_synthetic_scenario_summary.csv"),
            },
            parameters={"selected_verdict": VERDICT, "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase416_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase415_taker_next_tick_order_arrival",
        ),
    }
    (output_dir / "phase416_deep_book_divergence_snapback_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase416 deep-book divergence snapback interpretation.")
    parser.add_argument("--phase415-dir", type=Path, default=DEFAULT_PHASE415_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase415_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
