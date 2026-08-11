from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase362")
THESIS_ID = "P362_LIQUIDITY_REPLENISHED_CATALYST_IMPULSE_CONTINUATION"
NEXT_ACTION = "run_phase363_liquidity_replenished_catalyst_impulse_diagnostic_no_paper_live"


def write_outputs(output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    thesis = pd.DataFrame(
        [
            {
                "thesis_id": THESIS_ID,
                "status": "precommit",
                "material_difference_from_closed_fade": "Uses post-catalyst price impulse continuation after liquidity replenishment; does not fade top-five or levels-2-5 imbalance.",
                "signal_timing": "wait 60s/120s after official catalyst diagnostic start before deciding",
                "side_rule": "continue the signed mid-price impulse from start to decision tick",
                "full_depth_rule": "levels 2-5 imbalance must support impulse direction and top-five imbalance must not contradict it",
                "liquidity_replenishment_rule": "top-five displayed quantity at decision must be at least as large as at start, with stressed variant requiring >=10% replenishment",
                "execution_rule": "marketable diagnostic entry/exit with Zerodha cost200 fixed-capital scoring",
                "lookahead_forbidden": 1,
                "paper_live_or_profit_claim_allowed": 0,
            }
        ]
    )
    scenario_grid = pd.DataFrame(
        [
            {
                "scenario_grid_id": f"P362_D{delay}_I{str(impulse).replace('.', 'p')}_D{str(deep).replace('.', 'p')}_R{str(repl).replace('.', 'p')}",
                "decision_delay_seconds": delay,
                "horizon_seconds": 900,
                "min_abs_impulse_bps": impulse,
                "min_abs_l2_l5_imbalance": deep,
                "min_replenishment_ratio": repl,
                "top5_noncontradiction_required": 1,
                "side_policy": "impulse_continuation",
                "control_side_policy": "impulse_reversal",
            }
            for delay in [60, 120]
            for impulse in [2.5, 5.0]
            for deep in [0.15, 0.25]
            for repl in [0.0, 0.10]
        ]
    )
    validation_contract = pd.DataFrame(
        [
            ("phase361_branch_closed", 1, "The prior full-depth fade branch must be closed for acceptance before this new thesis runs."),
            ("materially_new_thesis_required", 1, "This is continuation after catalyst absorption, not same-family fade rescue."),
            ("input_real_l2_roots", "real_data_sample/l2_multiday_panel;real_data_sample/l2_unseen_validation", "Use the current local official-catalyst real L2 panels."),
            ("input_work_orders", "outputs/phase341/phase341_phase342_execution_work_order.csv;outputs/phase359/phase359_phase360_execution_work_order.csv", "Use existing official-catalyst no-lookahead work orders."),
            ("full_top_five_depth_required", 1, "Use bid/ask price, quantity and order-count levels 1-5."),
            ("levels_2_to_5_materiality_required", 1, "Levels 2-5 determine the support filter; no L1-only variant is allowed."),
            ("liquidity_replenishment_required", 1, "Displayed top-five quantity must replenish after catalyst start."),
            ("cost200_fixed_capital_required", 1, "Zerodha cost200 and fixed INR 250000 capital denominator are required."),
            ("annualized_threshold_pct", 12.0, "Keep user profitability threshold."),
            ("robust_event_floor", 30, "Sparse fewer-than-30 trade outcomes are discovery only."),
            ("same_family_parameter_rescue_allowed", 0, "Do not reopen Phase357/358 fade via hidden filters."),
            ("paper_live_or_profit_claim_allowed", 0, "No paper/live acceptance or deployable profitability claim."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )
    gates = pd.DataFrame(
        [
            ("P362_MATERIAL_NEW_THESIS", 1, "continuation_after_liquidity_replenishment_not_fade"),
            ("P362_SCENARIO_GRID_PRESENT", int(len(scenario_grid) == 16), f"grid_rows={len(scenario_grid)}"),
            ("P362_FULL_DEPTH_REQUIRED", 1, "levels 1-5 with levels 2-5 materiality"),
            ("P362_COST200_FIXED_CAPITAL_REQUIRED", 1, ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION),
            ("P362_NO_SAME_FAMILY_RESCUE", 1, "fade branch remains closed"),
            ("P362_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "closed"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )
    summary = pd.DataFrame(
        [
            ("phase362_liquidity_replenished_catalyst_impulse_precommit_complete", 1, "Phase362 precommit completed"),
            ("phase362_thesis_id", THESIS_ID, "Precommitted thesis"),
            ("phase362_scenario_grid_rows", len(scenario_grid), "Scenario grid rows"),
            ("phase362_materially_new_thesis", 1, "Not same-family fade rescue"),
            ("phase362_same_family_parameter_rescue_allowed", 0, "No rescue of closed fade branch"),
            ("phase362_strategy_promotion_allowed", 0, "No promotion"),
            ("phase362_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase362_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase362_hard_gate_pass_rows", int(gates["passed"].astype(int).sum()), "Passed hard gates"),
            ("phase362_hard_gate_rows", len(gates), "Hard gates"),
            ("phase362_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    outputs = {
        "summary": output_dir / "phase362_acceptance_summary.csv",
        "thesis": output_dir / "phase362_thesis_contract.csv",
        "grid": output_dir / "phase362_scenario_grid.csv",
        "validation": output_dir / "phase362_validation_contract.csv",
        "gates": output_dir / "phase362_gate_evaluation.csv",
        "report": output_dir / "phase362_liquidity_replenished_catalyst_impulse_precommit_report.md",
        "manifest": output_dir / "phase362_liquidity_replenished_catalyst_impulse_precommit_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    thesis.to_csv(outputs["thesis"], index=False)
    scenario_grid.to_csv(outputs["grid"], index=False)
    validation_contract.to_csv(outputs["validation"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    report = "\n".join(
        [
            "# Phase362 Liquidity-Replenished Catalyst Impulse Precommit",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase362 precommits a materially new real-L2 thesis after Phase361 closed the full-depth fade branch for acceptance. This route tests post-catalyst impulse continuation only after displayed liquidity replenishes and levels 2-5 support the impulse direction.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Thesis contract",
            "",
            _markdown_table(thesis),
            "",
            "## Scenario grid",
            "",
            _markdown_table(scenario_grid),
            "",
            "## Validation contract",
            "",
            _markdown_table(validation_contract),
            "",
            "## Gate evaluation",
            "",
            _markdown_table(gates),
            "",
            "No promotion, paper/live acceptance, or deployable profitability claim is opened.",
        ]
    )
    outputs["report"].write_text(report + "\n", encoding="utf-8")
    manifest = {
        "phase": 362,
        "generated_at_utc": generated_utc,
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase362_liquidity_replenished_catalyst_impulse_precommit",
            generated_utc=generated_utc,
            inputs={"phase361_decision": "outputs/phase361/phase361_branch_decision_ledger.csv"},
            parameters={"thesis_id": THESIS_ID, "scenario_grid_rows": len(scenario_grid)},
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": NEXT_ACTION,
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
