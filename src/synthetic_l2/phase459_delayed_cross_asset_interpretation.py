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


DEFAULT_PHASE458_DIR = Path("outputs/phase458")
DEFAULT_OUTPUT_DIR = Path("outputs/phase459")

THESIS_ID = "P459_DELAYED_CROSS_ASSET_DISPLACEMENT_INTERPRETATION"
SELECTED_VERDICT = "P459_DELAYED_CROSS_ASSET_DISPLACEMENT_REJECTED_ZERO_GROSS_EDGE"
NEXT_ACTION = "precommit_actual_move_candidate_label_source_or_pause_synthetic_fixed_window_routes"


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def row(summary: pd.DataFrame, scenario_id: str) -> dict[str, Any]:
    rows = summary[summary["scenario_id"].astype(str).eq(scenario_id)]
    return rows.iloc[0].to_dict() if not rows.empty else {}


def build_decision(acceptance458: pd.DataFrame, scenarios: pd.DataFrame, gates458: pd.DataFrame) -> pd.DataFrame:
    primary = row(scenarios, "P458_delayed_cross_asset_displacement_primary")
    failed = gates458[~gates458["passed"].astype(str).str.lower().isin(["true", "1"])]
    rows = [
        ("selected_verdict", SELECTED_VERDICT, "The delayed fixed-window cross-asset source is rejected.", "terminal_for_this_fixed_window_form"),
        ("acceptance_survivor", scalar(acceptance458, "phase458_acceptance_survivor", 0), "No accepted survivor.", 0),
        ("primary_completed_round_trips", primary.get("completed_round_trips", ""), "Breadth was sufficient.", ">=30"),
        ("primary_trade_dates", primary.get("trade_dates", ""), "Date breadth was sufficient.", ">=5"),
        ("primary_symbols", primary.get("symbols", ""), "Symbol breadth was sufficient.", ">=3"),
        ("primary_gross_pnl_inr", primary.get("gross_pnl_inr", ""), "Gross edge before costs.", "must_be_positive_to_continue"),
        ("primary_net_pnl_inr", primary.get("net_pnl_inr", ""), "Net P&L after cost200.", ">0_required"),
        ("primary_annualized_return_pct", primary.get("annualized_return_pct", ""), "Fixed-capital annualized return.", ">=12_required"),
        ("failed_gate_ids", ";".join(failed["gate_id"].astype(str).tolist()), "Failed Phase458 gates.", "basis"),
        ("same_delayed_fixed_window_rescue_allowed", 0, "Do not tune row offset or thresholds after seeing this result.", 0),
        ("paper_live_or_profit_claim", 0, "No promotion, paper/live acceptance or deployable claim.", 0),
        ("next_action", NEXT_ACTION, "Next route should use actual move-candidate labels rather than fixed row windows.", "material_new_label_source"),
    ]
    return pd.DataFrame(rows, columns=["decision_id", "decision_value", "description", "required_or_implication"])


def build_byproducts() -> pd.DataFrame:
    rows = [
        ("delayed_window_reader", "reusable", "Can extract contiguous L1-L5 windows from later intraday row offsets."),
        ("fixed_window_negative_evidence", "ledger", "Both first-window and delayed row-5000 windows produced zero gross edge under the current synthetic dense generator."),
        ("next_source_hint", "research_queue", "Use actual move-candidate labels or volatility-active windows before applying cross-asset pressure."),
    ]
    return pd.DataFrame(rows, columns=["byproduct_id", "status", "description"])


def build_gates(acceptance458: pd.DataFrame, decision: pd.DataFrame, gates458: pd.DataFrame) -> pd.DataFrame:
    failed = gates458[~gates458["passed"].astype(str).str.lower().isin(["true", "1"])]
    gates = [
        ("P459_PHASE458_COMPLETE", as_int(scalar(acceptance458, "phase458_delayed_cross_asset_execution_complete", 0)) == 1, scalar(acceptance458, "phase458_delayed_cross_asset_execution_complete", 0), 1),
        ("P459_PHASE458_REAL_TRADES_PRESENT", as_int(scalar(acceptance458, "phase458_best_completed_round_trips", 0)) > 0, scalar(acceptance458, "phase458_best_completed_round_trips", 0), ">0"),
        ("P459_NO_ACCEPTANCE_SURVIVOR", as_int(scalar(acceptance458, "phase458_acceptance_survivor", 1)) == 0, scalar(acceptance458, "phase458_acceptance_survivor", 1), 0),
        ("P459_FAILED_GATE_BASIS_PRESENT", len(failed) > 0, ";".join(failed["gate_id"].astype(str).tolist()), ">0"),
        ("P459_VERDICT_REJECTS_ROUTE", "REJECTED" in str(decision.loc[decision["decision_id"].eq("selected_verdict"), "decision_value"].iloc[0]), decision.loc[decision["decision_id"].eq("selected_verdict"), "decision_value"].iloc[0], "REJECTED"),
        ("P459_SAME_ROUTE_RESCUE_CLOSED", str(decision.loc[decision["decision_id"].eq("same_delayed_fixed_window_rescue_allowed"), "decision_value"].iloc[0]) == "0", 0, 0),
        ("P459_BOUNDARIES_CLOSED", str(decision.loc[decision["decision_id"].eq("paper_live_or_profit_claim"), "decision_value"].iloc[0]) == "0", 0, 0),
        ("P459_NEXT_ACTION_LABEL_SOURCE", "label_source" in str(decision.loc[decision["decision_id"].eq("next_action"), "required_or_implication"].iloc[0]), decision.loc[decision["decision_id"].eq("next_action"), "decision_value"].iloc[0], "material_new_label_source"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase459_delayed_cross_asset_interpretation_complete", 1, "Phase459 interpretation completed"),
            ("phase459_thesis_id", THESIS_ID, "Interpretation thesis"),
            ("phase459_selected_verdict", SELECTED_VERDICT, "Selected verdict"),
            ("phase459_same_route_rescue_allowed", 0, "No same-route rescue"),
            ("phase459_strategy_promotion_allowed", 0, "No promotion"),
            ("phase459_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase459_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase459_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase459_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase459_next_best_action", NEXT_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, decision: pd.DataFrame, byproducts: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase459 Delayed Cross-Asset Displacement Interpretation",
        "",
        "Phase459 formally interprets Phase458 and closes the delayed fixed-window cross-asset displacement form.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Decision Ledger",
        "",
        _markdown_table(decision),
        "",
        "## Durable Byproducts",
        "",
        _markdown_table(byproducts),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: do not tune the same fixed-window cross-asset route. Next work should precommit actual move-candidate labels or pause synthetic fixed-window routes.",
    ]
    (output_dir / "phase459_delayed_cross_asset_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase458_dir: Path = DEFAULT_PHASE458_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    acceptance458 = read_csv(phase458_dir / "phase458_acceptance_summary.csv")
    scenarios = read_csv(phase458_dir / "phase458_scenario_summary.csv")
    gates458 = read_csv(phase458_dir / "phase458_gate_evaluation.csv")
    if acceptance458.empty or scenarios.empty or gates458.empty:
        raise FileNotFoundError("Phase459 requires Phase458 acceptance, scenarios and gates.")
    decision = build_decision(acceptance458, scenarios, gates458)
    byproducts = build_byproducts()
    gates = build_gates(acceptance458, decision, gates458)
    acceptance = build_acceptance(gates)
    decision.to_csv(output_dir / "phase459_decision_ledger.csv", index=False)
    byproducts.to_csv(output_dir / "phase459_durable_byproduct_catalog.csv", index=False)
    gates.to_csv(output_dir / "phase459_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase459_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, decision, byproducts, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase459_delayed_cross_asset_interpretation",
        **reproducibility_fields(
            artifact_id="phase459_delayed_cross_asset_interpretation",
            generated_utc=generated_utc,
            inputs={"phase458_acceptance_summary": str(phase458_dir / "phase458_acceptance_summary.csv"), "phase458_scenario_summary": str(phase458_dir / "phase458_scenario_summary.csv"), "phase458_gate_evaluation": str(phase458_dir / "phase458_gate_evaluation.csv")},
            parameters={"thesis_id": THESIS_ID, "selected_verdict": SELECTED_VERDICT},
            outputs={"acceptance_summary": str(output_dir / "phase459_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase458_delayed_contiguous_tick_window",
        ),
    }
    (output_dir / "phase459_delayed_cross_asset_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase459 delayed cross-asset interpretation.")
    parser.add_argument("--phase458-dir", type=Path, default=DEFAULT_PHASE458_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase458_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
