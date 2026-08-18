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


DEFAULT_PHASE455_DIR = Path("outputs/phase455")
DEFAULT_OUTPUT_DIR = Path("outputs/phase456")

THESIS_ID = "P456_CROSS_ASSET_ETF_PRESSURE_INTERPRETATION"
SELECTED_VERDICT = "P456_FIRST_WINDOW_CROSS_ASSET_ETF_PRESSURE_REJECTED_ZERO_GROSS_EDGE"
NEXT_ACTION = "precommit_material_new_timing_or_label_source_not_first_window_cross_asset_pressure"


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def row(summary: pd.DataFrame, scenario_id: str) -> dict[str, Any]:
    rows = summary[summary["scenario_id"].astype(str).eq(scenario_id)]
    return rows.iloc[0].to_dict() if not rows.empty else {}


def build_decision(acceptance455: pd.DataFrame, scenarios: pd.DataFrame, gates455: pd.DataFrame) -> pd.DataFrame:
    failed = gates455[~gates455["passed"].astype(str).str.lower().isin(["true", "1"])]
    primary = row(scenarios, "P455_contiguous_cross_asset_etf_pressure_primary")
    shifted = row(scenarios, "P455_contiguous_cross_asset_etf_pressure_source_time_shift")
    side = row(scenarios, "P455_contiguous_cross_asset_etf_pressure_side_flip")
    etf_l1 = row(scenarios, "P455_contiguous_cross_asset_etf_l1_only")
    rows = [
        ("selected_verdict", SELECTED_VERDICT, "The repaired first-window cross-asset ETF pressure source is rejected.", "terminal_for_first_window_form"),
        ("acceptance_survivor", scalar(acceptance455, "phase455_acceptance_survivor", 0), "No accepted survivor.", 0),
        ("primary_completed_round_trips", primary.get("completed_round_trips", ""), "Breadth was sufficient for a real verdict.", ">=30"),
        ("primary_trade_dates", primary.get("trade_dates", ""), "Date breadth was sufficient.", ">=5"),
        ("primary_symbols", primary.get("symbols", ""), "Symbol breadth was sufficient.", ">=3"),
        ("primary_gross_pnl_inr", primary.get("gross_pnl_inr", ""), "Gross edge before costs.", "positive_required_for_any_costed_edge"),
        ("primary_net_pnl_inr", primary.get("net_pnl_inr", ""), "Net P&L after Zerodha cost200.", ">0_required"),
        ("primary_annualized_return_pct", primary.get("annualized_return_pct", ""), "Fixed-capital annualized return.", ">=12_required"),
        ("source_time_shift_net_pnl_inr", shifted.get("net_pnl_inr", ""), "Time-shift control.", "primary_should_dominate"),
        ("side_flip_net_pnl_inr", side.get("net_pnl_inr", ""), "Side-flip control.", "primary_should_dominate"),
        ("etf_l1_only_net_pnl_inr", etf_l1.get("net_pnl_inr", ""), "ETF L1-only control.", "primary_should_dominate"),
        ("failed_gate_ids", ";".join(failed["gate_id"].astype(str).tolist()), "Failed Phase455 gates.", "must_be_empty_for_acceptance"),
        ("same_first_window_cross_asset_rescue_allowed", 0, "Do not tune the same first-window source after this result.", 0),
        ("paper_live_or_profit_claim", 0, "No promotion, paper/live acceptance or deployable claim.", 0),
        ("next_action", NEXT_ACTION, "Next source must alter timing/label source materially, not tweak this failed form.", "material_new"),
    ]
    return pd.DataFrame(rows, columns=["decision_id", "decision_value", "description", "required_or_implication"])


def build_byproducts() -> pd.DataFrame:
    rows = [
        ("contiguous_window_reader", "reusable", "Reads first contiguous raw L1-L5 tick windows per symbol/date from monthly Parquet partitions."),
        ("cross_asset_signal_metrics", "reusable", "Daily proxy/target L1-L5 pressure metrics for ETF-to-constituent experiments."),
        ("low_turnover_control_harness", "reusable", "Source-shift, side-flip, target-only and ETF L1-only controls."),
        ("negative_evidence_first_window", "ledger", "First-window proxy pressure produced zero gross edge and only costs."),
    ]
    return pd.DataFrame(rows, columns=["byproduct_id", "status", "description"])


def build_gates(acceptance455: pd.DataFrame, decision: pd.DataFrame, gates455: pd.DataFrame) -> pd.DataFrame:
    failed = gates455[~gates455["passed"].astype(str).str.lower().isin(["true", "1"])]
    gates = [
        ("P456_PHASE455_COMPLETE", as_int(scalar(acceptance455, "phase455_contiguous_cross_asset_execution_complete", 0)) == 1, scalar(acceptance455, "phase455_contiguous_cross_asset_execution_complete", 0), 1),
        ("P456_PHASE455_REAL_TRADES_PRESENT", as_int(scalar(acceptance455, "phase455_best_completed_round_trips", 0)) > 0, scalar(acceptance455, "phase455_best_completed_round_trips", 0), ">0"),
        ("P456_NO_ACCEPTANCE_SURVIVOR", as_int(scalar(acceptance455, "phase455_acceptance_survivor", 1)) == 0, scalar(acceptance455, "phase455_acceptance_survivor", 1), 0),
        ("P456_FAILED_GATE_BASIS_PRESENT", len(failed) > 0, ";".join(failed["gate_id"].astype(str).tolist()), ">0"),
        ("P456_VERDICT_REJECTS_FIRST_WINDOW_FORM", "REJECTED" in str(decision.loc[decision["decision_id"].eq("selected_verdict"), "decision_value"].iloc[0]), decision.loc[decision["decision_id"].eq("selected_verdict"), "decision_value"].iloc[0], "REJECTED"),
        ("P456_SAME_FORM_RESCUE_CLOSED", str(decision.loc[decision["decision_id"].eq("same_first_window_cross_asset_rescue_allowed"), "decision_value"].iloc[0]) == "0", 0, 0),
        ("P456_BOUNDARIES_CLOSED", str(decision.loc[decision["decision_id"].eq("paper_live_or_profit_claim"), "decision_value"].iloc[0]) == "0", 0, 0),
        ("P456_NEXT_ACTION_MATERIAL_NEW", "material_new" in str(decision.loc[decision["decision_id"].eq("next_action"), "required_or_implication"].iloc[0]), decision.loc[decision["decision_id"].eq("next_action"), "decision_value"].iloc[0], "material_new"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase456_cross_asset_interpretation_complete", 1, "Phase456 interpretation completed"),
            ("phase456_thesis_id", THESIS_ID, "Interpretation thesis"),
            ("phase456_selected_verdict", SELECTED_VERDICT, "Selected verdict"),
            ("phase456_same_form_rescue_allowed", 0, "No same-form rescue"),
            ("phase456_strategy_promotion_allowed", 0, "No promotion"),
            ("phase456_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase456_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase456_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase456_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase456_next_best_action", NEXT_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, decision: pd.DataFrame, byproducts: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase456 Cross-Asset ETF Pressure Interpretation",
        "",
        "Phase456 formally interprets the repaired Phase455 cross-asset ETF pressure execution. The first-window form is rejected because it produced zero gross edge and failed control dominance.",
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
        "Boundary: do not tune the same first-window cross-asset pressure form. A new phase must precommit a materially different timing or label source.",
    ]
    (output_dir / "phase456_cross_asset_etf_pressure_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase455_dir: Path = DEFAULT_PHASE455_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    acceptance455 = read_csv(phase455_dir / "phase455_acceptance_summary.csv")
    scenarios = read_csv(phase455_dir / "phase455_scenario_summary.csv")
    gates455 = read_csv(phase455_dir / "phase455_gate_evaluation.csv")
    if acceptance455.empty or scenarios.empty or gates455.empty:
        raise FileNotFoundError("Phase456 requires Phase455 acceptance, scenario summary and gates.")
    decision = build_decision(acceptance455, scenarios, gates455)
    byproducts = build_byproducts()
    gates = build_gates(acceptance455, decision, gates455)
    acceptance = build_acceptance(gates)
    decision.to_csv(output_dir / "phase456_decision_ledger.csv", index=False)
    byproducts.to_csv(output_dir / "phase456_durable_byproduct_catalog.csv", index=False)
    gates.to_csv(output_dir / "phase456_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase456_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, decision, byproducts, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase456_cross_asset_etf_pressure_interpretation",
        **reproducibility_fields(
            artifact_id="phase456_cross_asset_etf_pressure_interpretation",
            generated_utc=generated_utc,
            inputs={"phase455_acceptance_summary": str(phase455_dir / "phase455_acceptance_summary.csv"), "phase455_scenario_summary": str(phase455_dir / "phase455_scenario_summary.csv"), "phase455_gate_evaluation": str(phase455_dir / "phase455_gate_evaluation.csv")},
            parameters={"thesis_id": THESIS_ID, "selected_verdict": SELECTED_VERDICT},
            outputs={"acceptance_summary": str(output_dir / "phase456_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase455_contiguous_tick_window",
        ),
    }
    (output_dir / "phase456_cross_asset_etf_pressure_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase456 cross-asset ETF pressure interpretation.")
    parser.add_argument("--phase455-dir", type=Path, default=DEFAULT_PHASE455_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase455_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
