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


DEFAULT_PHASE356_DIR = Path("outputs/phase356")
DEFAULT_PHASE357_DIR = Path("outputs/phase357")
DEFAULT_OUTPUT_DIR = Path("outputs/phase358")
PRIMARY_SCENARIO_ID = "P356_CONTROL_DEPTH_2_5_FADE_VARIANT"
GUARD_SCENARIO_ID = "P356_CONTROL_DEPTH_2_5_GUARD_TOP5_FADE"
TOP5_REFERENCE_ID = "P356_FROZEN_NIFTYBEES_LB900_MARKET_NEUTRAL_TOP5_FADE"
ROBUST_EVENT_FLOOR = 30
ANNUALIZED_THRESHOLD_PCT = 12.0


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def summarize_primary(scenarios: pd.DataFrame) -> dict[str, Any]:
    primary = scenarios.loc[scenarios["scenario_id"].astype(str).eq(PRIMARY_SCENARIO_ID)]
    if primary.empty:
        raise ValueError(f"Primary scenario missing: {PRIMARY_SCENARIO_ID}")
    return primary.iloc[0].to_dict()


def write_outputs(phase356_dir: Path, phase357_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    scenarios356 = read_csv(phase356_dir / "phase356_scenario_summary.csv")
    trades356 = read_csv(phase356_dir / "phase356_trade_ledger.csv")
    family357 = read_csv(phase357_dir / "phase357_family_contract.csv")
    if scenarios356.empty or trades356.empty or family357.empty:
        raise FileNotFoundError("Phase356/Phase357 evidence is incomplete")

    primary = summarize_primary(scenarios356)
    guard = scenarios356.loc[scenarios356["scenario_id"].astype(str).eq(GUARD_SCENARIO_ID)].iloc[0].to_dict()
    top5 = scenarios356.loc[scenarios356["scenario_id"].astype(str).eq(TOP5_REFERENCE_ID)].iloc[0].to_dict()
    controls = scenarios356.loc[~scenarios356["scenario_id"].astype(str).isin([PRIMARY_SCENARIO_ID, GUARD_SCENARIO_ID, TOP5_REFERENCE_ID])].copy()
    primary_trades = trades356.loc[trades356["scenario_id"].astype(str).eq(PRIMARY_SCENARIO_ID)].copy()
    primary_trades.insert(0, "phase358_role", "primary_full_depth_family")

    execution_summary = pd.DataFrame(
        [
            ("phase358_full_depth_market_neutral_fade_execution_complete", 1, "Phase358 execution completed"),
            ("phase358_phase357_precommit_present", 1, "Phase357 family contract present"),
            ("phase358_primary_scenario_id", PRIMARY_SCENARIO_ID, "Primary full-depth family row"),
            ("phase358_primary_trade_rows", primary["trade_rows"], "Primary trade rows"),
            ("phase358_primary_diagnostic_trade_dates", primary["diagnostic_trade_dates"], "Primary dates"),
            ("phase358_primary_symbols", primary["symbols"], "Primary symbols"),
            ("phase358_primary_positive_symbols", primary["positive_symbols"], "Primary positive symbols"),
            ("phase358_primary_positive_symbol_date_cells", primary["positive_symbol_date_cells"], "Primary positive symbol/date cells"),
            ("phase358_primary_net_pnl_inr", primary["net_pnl_inr"], "Primary net PnL"),
            ("phase358_primary_annualized_return_pct", primary["annualized_return_pct"], "Primary fixed-capital annualized return"),
            ("phase358_primary_above12", primary["above12"], "Primary above 12%"),
            ("phase358_primary_event_floor_met", primary["event_floor_met"], "Primary >=30 event floor"),
            ("phase358_primary_acceptance_candidate", primary["acceptance_candidate"], "Primary acceptance candidate"),
            ("phase358_guard_annualized_return_pct", guard["annualized_return_pct"], "Depth guard annualized return"),
            ("phase358_top5_reference_annualized_return_pct", top5["annualized_return_pct"], "Top-five reference annualized return"),
            ("phase358_control_rows", len(controls), "Control rows"),
            ("phase358_acceptance_candidate_rows", int(scenarios356["acceptance_candidate"].astype(int).sum()), "Acceptance candidates"),
            ("phase358_strategy_promotion_allowed", 0, "No promotion"),
            ("phase358_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase358_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase358_next_best_action", "restore_phase350_real_date_expansion_for_unseen_event_floor_no_paper_live", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )

    interpretation = pd.DataFrame(
        [
            {
                "interpretation_id": "primary_positive",
                "value": int(float(primary["annualized_return_pct"]) > ANNUALIZED_THRESHOLD_PCT),
                "evidence": f"annualized={primary['annualized_return_pct']}; net={primary['net_pnl_inr']}",
                "decision": "Full-depth family remains a positive sparse clue.",
            },
            {
                "interpretation_id": "event_floor_failed",
                "value": int(int(primary["trade_rows"]) < ROBUST_EVENT_FLOOR),
                "evidence": f"trade_rows={primary['trade_rows']}; required={ROBUST_EVENT_FLOOR}",
                "decision": "No acceptance until unseen real-date expansion increases event count.",
            },
            {
                "interpretation_id": "top5_reference_not_primary",
                "value": int(float(primary["annualized_return_pct"]) > float(top5["annualized_return_pct"])),
                "evidence": f"primary={primary['annualized_return_pct']}; top5={top5['annualized_return_pct']}",
                "decision": "Keep depth-levels-2-5 fade as primary family.",
            },
            {
                "interpretation_id": "paper_live_closed",
                "value": 1,
                "evidence": "promotion=0; paper_live=0; deployable_claim=0",
                "decision": "Research clue only.",
            },
        ]
    )

    gates = pd.DataFrame(
        [
            ("P358_PHASE357_PRECOMMIT_PRESENT", 1, "Phase357 family contract present"),
            ("P358_PRIMARY_FULL_DEPTH_EXECUTED", int(PRIMARY_SCENARIO_ID in set(scenarios356["scenario_id"].astype(str))), PRIMARY_SCENARIO_ID),
            ("P358_COST200_FIXED_CAPITAL", 1, "Inherited Phase356 cost200 fixed-capital scoring"),
            ("P358_EVENT_FLOOR_CHECKED", 1, f"event_floor_met={primary['event_floor_met']}"),
            ("P358_CONTROLS_AVAILABLE", int(len(controls) >= 4), f"control_rows={len(controls)}"),
            ("P358_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "closed"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )

    outputs = {
        "summary": output_dir / "phase358_acceptance_summary.csv",
        "scenario": output_dir / "phase358_scenario_summary.csv",
        "primary_trades": output_dir / "phase358_primary_trade_ledger.csv",
        "interpretation": output_dir / "phase358_interpretation_ledger.csv",
        "gates": output_dir / "phase358_gate_evaluation.csv",
        "report": output_dir / "phase358_full_depth_market_neutral_fade_execution_report.md",
        "manifest": output_dir / "phase358_full_depth_market_neutral_fade_execution_manifest.json",
    }
    execution_summary.to_csv(outputs["summary"], index=False)
    scenarios356.to_csv(outputs["scenario"], index=False)
    primary_trades.to_csv(outputs["primary_trades"], index=False)
    interpretation.to_csv(outputs["interpretation"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    report = "\n".join(
        [
            "# Phase358 Full-Depth Market-Neutral Fade Execution",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase358 executes the Phase357 precommitted full-depth family on the current local panel using Phase356 materialized scenario/trade evidence.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(execution_summary),
            "",
            "## Interpretation",
            "",
            _markdown_table(interpretation),
            "",
            "## Scenario summary",
            "",
            _markdown_table(scenarios356),
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
        "phase": 358,
        "generated_at_utc": generated_utc,
        "phase356_dir": str(phase356_dir),
        "phase357_dir": str(phase357_dir),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase358_full_depth_market_neutral_fade_execution",
            generated_utc=generated_utc,
            inputs={"phase356_dir": str(phase356_dir), "phase357_dir": str(phase357_dir)},
            parameters={"primary_scenario_id": PRIMARY_SCENARIO_ID, "event_floor": ROBUST_EVENT_FLOOR},
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase356_materialized_entry_exit_timestamps",
        ),
        "next_action": "restore_phase350_real_date_expansion_for_unseen_event_floor_no_paper_live",
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase356-dir", type=Path, default=DEFAULT_PHASE356_DIR)
    parser.add_argument("--phase357-dir", type=Path, default=DEFAULT_PHASE357_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase356_dir, args.phase357_dir, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
