from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE354_DIR = Path("outputs/phase354")
DEFAULT_OUTPUT_DIR = Path("outputs/phase355")


FROZEN_SCENARIO_ID = "P354_capacity_selected_events_NIFTYBEES_LB900_market_neutral_top5_fade"
ROBUST_EVENT_FLOOR = 30
ANNUALIZED_THRESHOLD_PCT = 12.0


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def write_outputs(phase354_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    summary354 = read_csv(phase354_dir / "phase354_acceptance_summary.csv")
    scenarios354 = read_csv(phase354_dir / "phase354_scenario_summary.csv")
    trades354 = read_csv(phase354_dir / "phase354_trade_ledger.csv")
    if summary354.empty or scenarios354.empty or trades354.empty:
        raise FileNotFoundError(f"Phase354 evidence incomplete under {phase354_dir}")

    frozen = scenarios354.loc[scenarios354["scenario_id"].astype(str).eq(FROZEN_SCENARIO_ID)].copy()
    if frozen.empty:
        raise ValueError(f"Frozen clue not found: {FROZEN_SCENARIO_ID}")
    frozen_row = frozen.iloc[0].to_dict()
    frozen_trades = trades354.loc[trades354["scenario_id"].astype(str).eq(FROZEN_SCENARIO_ID)].copy()
    above12_rows = int(scenarios354["above12"].astype(int).sum())
    acceptance_rows = int(scenarios354["acceptance_candidate"].astype(int).sum())

    frozen_contract = pd.DataFrame(
        [
            ("scenario_id", FROZEN_SCENARIO_ID, "Frozen Phase354 clue; no scenario substitution allowed"),
            ("scope", frozen_row["scope"], "Must remain capacity-selected events"),
            ("proxy_symbol", frozen_row["proxy_symbol"], "Must remain NIFTYBEES"),
            ("lookback_seconds", frozen_row["lookback_seconds"], "Must remain 900 seconds"),
            ("rule_id", frozen_row["rule_id"], "Must remain market-neutral top-five fade"),
            ("trade_rows", frozen_row["trade_rows"], "Observed Phase354 trade rows"),
            ("diagnostic_trade_dates", frozen_row["diagnostic_trade_dates"], "Observed diagnostic dates"),
            ("symbols", frozen_row["symbols"], "Observed symbols"),
            ("positive_symbols", frozen_row["positive_symbols"], "Observed positive symbols"),
            ("positive_symbol_date_cells", frozen_row["positive_symbol_date_cells"], "Observed positive symbol/date cells"),
            ("net_pnl_inr", frozen_row["net_pnl_inr"], "Observed net PnL"),
            ("annualized_return_pct", frozen_row["annualized_return_pct"], "Observed fixed-capital annualized return"),
            ("event_floor_met", frozen_row["event_floor_met"], "Must reach 30 events before acceptance"),
            ("acceptance_candidate", frozen_row["acceptance_candidate"], "Current clue is not acceptance-grade"),
        ],
        columns=["field", "frozen_value", "description"],
    )

    validation_contract = pd.DataFrame(
        [
            {
                "contract_id": "P355_NO_POST_HOC_THRESHOLD_CHANGE",
                "requirement": "Do not change scope, proxy, lookback, market-neutral threshold, top-five fade rule, costs, or fixed-capital denominator.",
                "acceptance_evidence": "Frozen contract reconciles exactly to Phase354.",
                "hard_gate": 1,
            },
            {
                "contract_id": "P355_EVENT_FLOOR_REQUIRED",
                "requirement": f"Validation requires at least {ROBUST_EVENT_FLOOR} trades/events.",
                "acceptance_evidence": "Expanded real-date or predeclared validation ledger event count.",
                "hard_gate": 1,
            },
            {
                "contract_id": "P355_ABOVE12_REQUIRED",
                "requirement": f"Fixed-capital annualized return must remain > {ANNUALIZED_THRESHOLD_PCT}%.",
                "acceptance_evidence": "Cost200 fixed-capital scenario summary.",
                "hard_gate": 1,
            },
            {
                "contract_id": "P355_BREADTH_REQUIRED",
                "requirement": "At least two positive symbols and two positive symbol/date cells; current clue already exceeds this but validation must preserve it.",
                "acceptance_evidence": "Positive-symbol and positive-symbol-date counts.",
                "hard_gate": 1,
            },
            {
                "contract_id": "P355_FULL_DEPTH_GUARDS_REQUIRED",
                "requirement": "Because the lead clue is top-five rather than depth-2-5 specific, validation must log depth-levels-2-5 diagnostics and run depth-2-5 guard/control variants.",
                "acceptance_evidence": "Validation ledger includes entry_l2_l5_qty_imbalance and depth guard/control rows.",
                "hard_gate": 1,
            },
            {
                "contract_id": "P355_CONTROLS_REQUIRED",
                "requirement": "Side-flip, random-side, proxy-swap BANKBEES, lookback-swap 300s, and depth-2-5 guard controls must not dominate the frozen clue.",
                "acceptance_evidence": "Control comparison ledger.",
                "hard_gate": 1,
            },
            {
                "contract_id": "P355_NO_PROMOTION_PAPER_LIVE",
                "requirement": "No promotion, paper/live acceptance, or deployable profitability claim from this precommit.",
                "acceptance_evidence": "Boundary ledger remains closed.",
                "hard_gate": 1,
            },
        ]
    )

    control_catalog = pd.DataFrame(
        [
            ("side_flip", "Flip every long/short side from the frozen clue.", "must_not_outperform_frozen"),
            ("random_side_deterministic", "Deterministic alternating/randomized side assignment with fixed seed.", "must_not_outperform_frozen"),
            ("proxy_swap_bankbees", "Replace NIFTYBEES with BANKBEES while keeping 900s lookback and market-neutral top-five fade.", "diagnostic_control"),
            ("lookback_swap_300s", "Replace 900s with 300s while keeping NIFTYBEES and market-neutral top-five fade.", "diagnostic_control"),
            ("depth_2_5_guard", "Require depth-levels-2-5 imbalance to be non-contradictory or report failure if it removes the clue.", "materiality_guard"),
            ("depth_2_5_fade_variant", "Test depth-levels-2-5 fade under the same market-neutral proxy context.", "full_depth_control"),
        ],
        columns=["control_id", "description", "required_interpretation"],
    )

    boundary = pd.DataFrame(
        [
            ("strategy_replay_allowed", 0, "No replay unlock"),
            ("strategy_promotion_allowed", 0, "No promotion"),
            ("paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("current_result_is_sparse_clue_only", 1, "Phase354 has >12 rows but <30 events"),
        ],
        columns=["boundary", "value", "description"],
    )

    summary = pd.DataFrame(
        [
            ("phase355_market_context_clue_validation_precommit_complete", 1, "Phase355 precommit completed"),
            ("phase355_phase354_complete", 1, "Phase354 evidence present"),
            ("phase355_phase354_above12_rows", above12_rows, "Phase354 above-12 rows"),
            ("phase355_phase354_acceptance_candidate_rows", acceptance_rows, "Phase354 acceptance rows"),
            ("phase355_frozen_scenario_id", FROZEN_SCENARIO_ID, "Frozen clue"),
            ("phase355_frozen_trade_rows", frozen_row["trade_rows"], "Frozen clue trade rows"),
            ("phase355_frozen_annualized_return_pct", frozen_row["annualized_return_pct"], "Frozen clue annualized return"),
            ("phase355_frozen_net_pnl_inr", frozen_row["net_pnl_inr"], "Frozen clue net PnL"),
            ("phase355_event_floor_required", ROBUST_EVENT_FLOOR, "Required event floor"),
            ("phase355_validation_execution_allowed_next", 1, "Phase356 execution allowed"),
            ("phase355_strategy_promotion_allowed", 0, "No promotion"),
            ("phase355_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase355_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase355_next_best_action", "run_phase356_market_context_clue_validation_execution_no_paper_live", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )

    gates = pd.DataFrame(
        [
            ("P355_PHASE354_COMPLETE", 1, "Phase354 evidence present"),
            ("P355_FROZEN_CLUE_PRESENT", int(len(frozen) == 1), FROZEN_SCENARIO_ID),
            ("P355_SPARSE_CLUE_RECOGNIZED", int(int(frozen_row["trade_rows"]) < ROBUST_EVENT_FLOOR), f"trade_rows={frozen_row['trade_rows']}"),
            ("P355_CONTRACT_PRESENT", int(len(validation_contract) >= 7), f"contract_rows={len(validation_contract)}"),
            ("P355_CONTROLS_PRESENT", int(len(control_catalog) >= 5), f"control_rows={len(control_catalog)}"),
            ("P355_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "closed"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )

    outputs = {
        "summary": output_dir / "phase355_acceptance_summary.csv",
        "frozen": output_dir / "phase355_frozen_clue_contract.csv",
        "validation": output_dir / "phase355_validation_contract.csv",
        "controls": output_dir / "phase355_control_catalog.csv",
        "boundary": output_dir / "phase355_boundary_ledger.csv",
        "frozen_trades": output_dir / "phase355_frozen_clue_trade_ledger.csv",
        "gates": output_dir / "phase355_gate_evaluation.csv",
        "report": output_dir / "phase355_market_context_clue_validation_precommit_report.md",
        "manifest": output_dir / "phase355_market_context_clue_validation_precommit_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    frozen_contract.to_csv(outputs["frozen"], index=False)
    validation_contract.to_csv(outputs["validation"], index=False)
    control_catalog.to_csv(outputs["controls"], index=False)
    boundary.to_csv(outputs["boundary"], index=False)
    frozen_trades.to_csv(outputs["frozen_trades"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    report = "\n".join(
        [
            "# Phase355 Market-Context Clue Validation Precommit",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase355 freezes the exact Phase354 sparse positive clue before any validation or expansion. It is a precommit only.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Frozen clue contract",
            "",
            _markdown_table(frozen_contract),
            "",
            "## Validation contract",
            "",
            _markdown_table(validation_contract),
            "",
            "## Control catalog",
            "",
            _markdown_table(control_catalog),
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
        "phase": 355,
        "generated_at_utc": generated_utc,
        "phase354_dir": str(phase354_dir),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase355_market_context_clue_validation_precommit",
            generated_utc=generated_utc,
            inputs={"phase354_dir": str(phase354_dir), "frozen_scenario_id": FROZEN_SCENARIO_ID},
            parameters={"robust_event_floor": ROBUST_EVENT_FLOOR, "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT},
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_precommit_only",
        ),
        "next_action": "run_phase356_market_context_clue_validation_execution_no_paper_live",
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase354-dir", type=Path, default=DEFAULT_PHASE354_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase354_dir, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
