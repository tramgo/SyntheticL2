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


DEFAULT_PHASE449_DIR = Path("outputs/phase449")
DEFAULT_OUTPUT_DIR = Path("outputs/phase450")

THESIS_ID = "P450_DEPTH_CURVATURE_BREAK_REPAIR_INTERPRETATION"
SELECTED_VERDICT = "P450_DEPTH_CURVATURE_DYNAMIC_ROUTE_REJECTED_COST_AND_CONTROLS"
NEXT_ACTION = "precommit_new_low_turnover_external_or_cross_asset_source_edge"


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def scenario_row(summary: pd.DataFrame, scenario_id: str) -> dict[str, Any]:
    rows = summary[summary["scenario_id"].astype(str).eq(scenario_id)]
    return rows.iloc[0].to_dict() if not rows.empty else {}


def build_decision_ledger(acceptance: pd.DataFrame, scenarios: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    primary = scenario_row(scenarios, "P449_depth_curvature_repair_primary")
    l1 = scenario_row(scenarios, "P449_depth_curvature_repair_l1_only_ablation")
    static = scenario_row(scenarios, "P449_depth_curvature_static_snapshot_control")
    shifted = scenario_row(scenarios, "P449_depth_curvature_time_shift_control")
    failed = gates[~gates["passed"].astype(str).str.lower().isin(["true", "1"])]
    rows = [
        ("selected_verdict", SELECTED_VERDICT, "Phase449 is rejected as a stable/profitable strategy route.", "terminal_for_this_dynamic_curvature_form"),
        ("acceptance_survivor", scalar(acceptance, "phase449_acceptance_survivor", 0), "No accepted survivor.", 0),
        ("primary_net_pnl_inr", primary.get("net_pnl_inr", ""), "Primary net P&L after cost200.", ">0_required_else_reject"),
        ("primary_annualized_return_pct", primary.get("annualized_return_pct", ""), "Fixed-capital annualized return.", ">=12_required"),
        ("primary_positive_date_fraction", primary.get("positive_date_fraction", ""), "Positive-date fraction.", ">=0.60_required"),
        ("l1_only_net_pnl_inr", l1.get("net_pnl_inr", ""), "L1-only control net P&L.", "primary_should_dominate"),
        ("static_curvature_net_pnl_inr", static.get("net_pnl_inr", ""), "Static curvature control net P&L.", "primary_should_dominate"),
        ("time_shift_net_pnl_inr", shifted.get("net_pnl_inr", ""), "Time-shift control net P&L.", "primary_should_dominate"),
        ("failed_gate_ids", ";".join(failed["gate_id"].astype(str).tolist()), "Failed hard gates.", "must_be_empty_for_acceptance"),
        ("same_source_rescue_allowed", 0, "Do not tune this dynamic curvature source after failure.", 0),
        ("paper_live_or_profit_claim", 0, "No promotion, paper/live acceptance or deployable profitability claim.", 0),
        ("next_action", NEXT_ACTION, "Next work must be a new source edge, preferably lower-turnover/external/cross-asset.", "new_source"),
    ]
    return pd.DataFrame(rows, columns=["decision_id", "decision_value", "description", "required_or_implication"])


def build_byproducts() -> pd.DataFrame:
    rows = [
        ("phase449_strided_parquet_scanner", "reusable", "Efficiently scans raw dense Parquet batches without loading full 80GB-style lake into memory."),
        ("phase449_l2_l5_curvature_features", "diagnostic", "Reusable feature engineering for depth curvature, asymmetry and repair/break rate."),
        ("phase449_control_harness", "reusable", "L1-only, side-flip, static-snapshot and time-shift controls can be reused for future L2 source tests."),
        ("negative_evidence_cost200", "ledger", "High event count with negative net P&L shows turnover/cost mismatch."),
    ]
    return pd.DataFrame(rows, columns=["byproduct_id", "status", "description"])


def build_gates(decision: pd.DataFrame, acceptance: pd.DataFrame, gates449: pd.DataFrame) -> pd.DataFrame:
    failed = gates449[~gates449["passed"].astype(str).str.lower().isin(["true", "1"])]
    verdict = decision.loc[decision["decision_id"].eq("selected_verdict"), "decision_value"].astype(str).str.cat(sep=" ")
    gates = [
        ("P450_PHASE449_COMPLETE", as_int(scalar(acceptance, "phase449_depth_curvature_execution_complete", 0)) == 1, scalar(acceptance, "phase449_depth_curvature_execution_complete", 0), 1),
        ("P450_NO_ACCEPTANCE_SURVIVOR", as_int(scalar(acceptance, "phase449_acceptance_survivor", 1)) == 0, scalar(acceptance, "phase449_acceptance_survivor", 1), 0),
        ("P450_FAILED_GATE_BASIS_PRESENT", len(failed) > 0, ";".join(failed["gate_id"].astype(str).tolist()), ">0"),
        ("P450_VERDICT_REJECTS_ROUTE", "REJECTED" in verdict, verdict, "REJECTED"),
        ("P450_SAME_SOURCE_RESCUE_CLOSED", str(decision.loc[decision["decision_id"].eq("same_source_rescue_allowed"), "decision_value"].iloc[0]) == "0", 0, 0),
        ("P450_BOUNDARIES_CLOSED", str(decision.loc[decision["decision_id"].eq("paper_live_or_profit_claim"), "decision_value"].iloc[0]) == "0", 0, 0),
        ("P450_NEXT_ACTION_NEW_SOURCE", "new_source" in str(decision.loc[decision["decision_id"].eq("next_action"), "required_or_implication"].iloc[0]), decision.loc[decision["decision_id"].eq("next_action"), "decision_value"].iloc[0], "new_source"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(decision: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase450_depth_curvature_interpretation_complete", 1, "Phase450 interpretation completed"),
            ("phase450_thesis_id", THESIS_ID, "Interpretation thesis"),
            ("phase450_selected_verdict", SELECTED_VERDICT, "Selected verdict"),
            ("phase450_phase449_acceptance_survivor", 0, "Phase449 survivor status"),
            ("phase450_same_source_rescue_allowed", 0, "No same-source rescue"),
            ("phase450_strategy_promotion_allowed", 0, "No promotion"),
            ("phase450_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase450_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase450_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase450_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase450_next_best_action", NEXT_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, decision: pd.DataFrame, byproducts: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase450 Depth-Curvature Break/Repair Interpretation",
        "",
        "Phase450 formally interprets Phase449. It records the depth-curvature dynamic route as rejected under cost200 and control dominance evidence.",
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
        "Boundary: do not tune this same dynamic curvature source. The next executable route must be precommitted as a new source edge.",
    ]
    (output_dir / "phase450_depth_curvature_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase449_dir: Path = DEFAULT_PHASE449_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    acceptance449 = read_csv(phase449_dir / "phase449_acceptance_summary.csv")
    scenarios449 = read_csv(phase449_dir / "phase449_scenario_summary.csv")
    gates449 = read_csv(phase449_dir / "phase449_gate_evaluation.csv")
    if acceptance449.empty or scenarios449.empty or gates449.empty:
        raise FileNotFoundError("Phase450 requires Phase449 acceptance, scenario summary and gate evaluation.")
    decision = build_decision_ledger(acceptance449, scenarios449, gates449)
    byproducts = build_byproducts()
    gates = build_gates(decision, acceptance449, gates449)
    acceptance = build_acceptance(decision, gates)
    decision.to_csv(output_dir / "phase450_decision_ledger.csv", index=False)
    byproducts.to_csv(output_dir / "phase450_durable_byproduct_catalog.csv", index=False)
    gates.to_csv(output_dir / "phase450_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase450_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, decision, byproducts, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase450_depth_curvature_interpretation",
        **reproducibility_fields(
            artifact_id="phase450_depth_curvature_interpretation",
            generated_utc=generated_utc,
            inputs={
                "phase449_acceptance_summary": str(phase449_dir / "phase449_acceptance_summary.csv"),
                "phase449_scenario_summary": str(phase449_dir / "phase449_scenario_summary.csv"),
                "phase449_gate_evaluation": str(phase449_dir / "phase449_gate_evaluation.csv"),
            },
            parameters={"thesis_id": THESIS_ID, "selected_verdict": SELECTED_VERDICT},
            outputs={"acceptance_summary": str(output_dir / "phase450_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase449_fixed_tick_horizon",
        ),
    }
    (output_dir / "phase450_depth_curvature_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase450 depth-curvature interpretation.")
    parser.add_argument("--phase449-dir", type=Path, default=DEFAULT_PHASE449_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase449_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
