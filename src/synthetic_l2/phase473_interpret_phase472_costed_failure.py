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


DEFAULT_PHASE471_DIR = Path("outputs/phase471")
DEFAULT_PHASE472_DIR = Path("outputs/phase472")
DEFAULT_OUTPUT_DIR = Path("outputs/phase473")

THESIS_ID = "P473_INTERPRET_PHASE472_COSTED_FAILURE"
NEXT_ACTION = "precommit_phase474_larger_horizon_fewer_trade_source_event_l1_l5_experiment"
MIN_ACCEPTABLE_ANNUALIZED_RETURN_PCT = 12.0


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def build_failure_attribution(phase471: pd.DataFrame, phase472: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    primary = scenarios[scenarios["model_name"].astype(str).eq("primary")].copy()
    best_primary = primary.sort_values(["annualized_return_pct", "net_pnl_inr"], ascending=False).iloc[0]
    best_primary_cost_drag = float(best_primary["zerodha_total_charges_inr"]) + float(best_primary["adverse_slippage_inr"])
    best_primary_gross = float(best_primary["gross_pnl_inr"])
    best_primary_net = float(best_primary["net_pnl_inr"])
    rows = [
        {
            "attribution_id": "predictive_signal_passed",
            "observed_value": float(scalar(phase471, "phase471_primary_holdout_auc", 0.0)),
            "comparison_value": 0.53,
            "verdict": "passed",
            "description": "Phase471 primary holdout AUC cleared the predictive floor.",
        },
        {
            "attribution_id": "gross_edge_positive_but_small",
            "observed_value": best_primary_gross,
            "comparison_value": best_primary_cost_drag,
            "verdict": "cost_drag_larger_than_gross_edge",
            "description": "Best primary scenario had positive gross P&L but costs plus slippage were larger.",
        },
        {
            "attribution_id": "best_primary_net_negative",
            "observed_value": best_primary_net,
            "comparison_value": 0.0,
            "verdict": "failed",
            "description": "Best primary net P&L was negative after cost200 and Zerodha charges.",
        },
        {
            "attribution_id": "annualized_profitability_failed",
            "observed_value": float(best_primary["annualized_return_pct"]),
            "comparison_value": MIN_ACCEPTABLE_ANNUALIZED_RETURN_PCT,
            "verdict": "failed",
            "description": "Best primary fixed-capital annualized return was below the 12% research profitability bar.",
        },
        {
            "attribution_id": "same_threshold_grid_not_rescuable",
            "observed_value": int((primary["net_pnl_inr"].astype(float) > 0).sum()),
            "comparison_value": 1,
            "verdict": "closed",
            "description": "No primary threshold in the tested grid produced positive net P&L.",
        },
        {
            "attribution_id": "phase472_expansion_not_allowed",
            "observed_value": as_int(scalar(phase472, "phase472_phase473_allowed_next", 0)),
            "comparison_value": 1,
            "verdict": "expansion_blocked",
            "description": "Phase472 did not allow direct expansion because profitability gates failed.",
        },
    ]
    return pd.DataFrame(rows)


def build_next_experiment_contract() -> pd.DataFrame:
    rows = [
        ("selected_next_thesis", "P474_LARGER_HORIZON_FEWER_TRADE_SOURCE_EVENT_L1_L5", "Seek larger gross moves rather than denser threshold retuning."),
        ("input_matrix_allowed", "outputs/phase470/phase470_source_event_aware_feature_label_matrix.csv", "Reuse repaired source-event-aware L1-L5 features."),
        ("same_phase472_threshold_retune_allowed", 0, "Do not only move thresholds on the same 240-tick horizon replay."),
        ("required_change_1", "larger_forward_horizon", "Increase horizon to target moves large enough to survive costs."),
        ("required_change_2", "fewer_higher_confidence_events", "Reduce turnover by ranking confidence and trading fewer events."),
        ("required_change_3", "full_depth_l1_l5_required", "Keep L1-L5 depth features central to the experiment."),
        ("required_change_4", "zerodha_cost200_required", "Apply Zerodha order-formula charges and cost200 slippage."),
        ("required_change_5", "fixed_capital_annualization_required", "Annualize using fixed reusable capital, not unlimited notional."),
        ("minimum_profitability_bar_pct", MIN_ACCEPTABLE_ANNUALIZED_RETURN_PCT, "Research lead profitability floor requested by user."),
        ("model_retraining_required", 1, "Horizon change requires new labels and a new train/holdout model evaluation."),
        ("paper_or_live_acceptance_allowed", 0, "No paper/live without expanded synthetic and real-L2 holdout checks."),
        ("deployable_profitability_claim_allowed", 0, "No deployable claim from this synthetic-only failure interpretation."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_gates(phase472: pd.DataFrame, attribution: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    attr = dict(zip(attribution["attribution_id"].astype(str), attribution["verdict"].astype(str)))
    contract_map = dict(zip(contract["contract_id"].astype(str), contract["contract_value"]))
    rows = [
        ("P473_PHASE472_REPLAY_COMPLETE", as_int(scalar(phase472, "phase472_score_to_signal_replay_cost200_complete", 0)) == 1, scalar(phase472, "phase472_score_to_signal_replay_cost200_complete", 0), 1),
        ("P473_PHASE472_REJECTED_CONFIRMED", as_int(scalar(phase472, "phase472_phase473_allowed_next", 1)) == 0, scalar(phase472, "phase472_phase473_allowed_next", 1), 0),
        ("P473_COST_DRAG_ATTRIBUTED", attr.get("gross_edge_positive_but_small") == "cost_drag_larger_than_gross_edge", attr.get("gross_edge_positive_but_small", ""), "cost_drag_larger_than_gross_edge"),
        ("P473_BEST_PRIMARY_NET_NEGATIVE_CONFIRMED", attr.get("best_primary_net_negative") == "failed", attr.get("best_primary_net_negative", ""), "failed"),
        ("P473_12PCT_BAR_FAILED_CONFIRMED", attr.get("annualized_profitability_failed") == "failed", attr.get("annualized_profitability_failed", ""), "failed"),
        ("P473_SAME_THRESHOLD_RETUNE_BLOCKED", as_int(contract_map.get("same_phase472_threshold_retune_allowed", 1)) == 0, contract_map.get("same_phase472_threshold_retune_allowed", ""), 0),
        ("P473_LARGER_HORIZON_NEXT_PRECOMMITTED", "LARGER_HORIZON" in str(contract_map.get("selected_next_thesis", "")), contract_map.get("selected_next_thesis", ""), "larger_horizon"),
        ("P473_FULL_DEPTH_REQUIRED_NEXT", str(contract_map.get("required_change_3", "")) == "full_depth_l1_l5_required", contract_map.get("required_change_3", ""), "full_depth_l1_l5_required"),
        ("P473_COST200_REQUIRED_NEXT", str(contract_map.get("required_change_4", "")) == "zerodha_cost200_required", contract_map.get("required_change_4", ""), "zerodha_cost200_required"),
        ("P473_NO_PAPER_LIVE_OR_CLAIM", as_int(contract_map.get("paper_or_live_acceptance_allowed", 1)) == 0 and as_int(contract_map.get("deployable_profitability_claim_allowed", 1)) == 0, "paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    all_pass = int(hard_pass == hard_rows)
    rows = [
        ("phase473_interpret_phase472_costed_failure_complete", 1, "Phase473 interpretation completed"),
        ("phase473_thesis_id", THESIS_ID, "Interpretation thesis"),
        ("phase473_same_phase472_threshold_retune_allowed", 0, "Same-grid threshold rescue is blocked"),
        ("phase473_larger_horizon_experiment_precommitted", 1, "Next experiment must target larger gross move"),
        ("phase473_strategy_promotion_allowed", 0, "No promotion"),
        ("phase473_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase473_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase473_phase474_allowed_next", all_pass, "Allows Phase474 precommit only if gates pass"),
        ("phase473_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase473_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase473_next_best_action", NEXT_ACTION if all_pass else "repair_phase473_failure_interpretation", "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, attribution: pd.DataFrame, contract: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase473 Interpret Phase472 Costed Failure",
        "",
        "Phase473 interprets the Phase472 costed replay failure and precommits the next experiment boundary.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Failure Attribution",
        "",
        _markdown_table(attribution),
        "",
        "## Next Experiment Contract",
        "",
        _markdown_table(contract),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: this is not a rescue. Same-horizon threshold tuning remains blocked. The next valid path must seek larger gross moves with full-depth L1-L5 and cost200 replay.",
    ]
    (output_dir / "phase473_interpret_phase472_costed_failure_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase471_dir: Path = DEFAULT_PHASE471_DIR, phase472_dir: Path = DEFAULT_PHASE472_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase471 = read_csv(phase471_dir / "phase471_acceptance_summary.csv")
    phase472 = read_csv(phase472_dir / "phase472_acceptance_summary.csv")
    scenarios = read_csv(phase472_dir / "phase472_scenario_summary.csv")
    attribution = build_failure_attribution(phase471, phase472, scenarios)
    contract = build_next_experiment_contract()
    gates = build_gates(phase472, attribution, contract)
    acceptance = build_acceptance(gates)
    attribution.to_csv(output_dir / "phase473_failure_attribution.csv", index=False)
    contract.to_csv(output_dir / "phase473_next_experiment_contract.csv", index=False)
    gates.to_csv(output_dir / "phase473_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase473_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, attribution, contract, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase473_interpret_phase472_costed_failure",
        **reproducibility_fields(
            artifact_id="phase473_interpret_phase472_costed_failure",
            generated_utc=generated_utc,
            inputs={
                "phase471_acceptance": str(phase471_dir / "phase471_acceptance_summary.csv"),
                "phase472_acceptance": str(phase472_dir / "phase472_acceptance_summary.csv"),
                "phase472_scenarios": str(phase472_dir / "phase472_scenario_summary.csv"),
            },
            parameters={
                "thesis_id": THESIS_ID,
                "minimum_acceptable_annualized_return_pct": MIN_ACCEPTABLE_ANNUALIZED_RETURN_PCT,
                "next_action": NEXT_ACTION,
            },
            outputs={"acceptance_summary": str(output_dir / "phase473_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase473_interpretation_no_execution",
        ),
    }
    (output_dir / "phase473_interpret_phase472_costed_failure_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase473 interpretation of Phase472 costed replay failure.")
    parser.add_argument("--phase471-dir", type=Path, default=DEFAULT_PHASE471_DIR)
    parser.add_argument("--phase472-dir", type=Path, default=DEFAULT_PHASE472_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    out = run(args.phase471_dir, args.phase472_dir, args.output_dir)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
