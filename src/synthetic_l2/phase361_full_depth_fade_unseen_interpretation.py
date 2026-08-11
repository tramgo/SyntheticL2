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
DEFAULT_PHASE358_DIR = Path("outputs/phase358")
DEFAULT_PHASE359_DIR = Path("outputs/phase359")
DEFAULT_PHASE360_DIR = Path("outputs/phase360")
DEFAULT_OUTPUT_DIR = Path("outputs/phase361")

PHASE356_PRIMARY_ID = "P356_CONTROL_DEPTH_2_5_FADE_VARIANT"
PHASE360_PRIMARY_ID = "P360_UNSEEN_P357_FULL_DEPTH_MARKET_NEUTRAL_DEPTH_2_5_FADE"
INITIAL_CAPITAL_INR = 250_000.0
TRADING_DAYS_PER_YEAR = 252.0
ANNUALIZED_THRESHOLD_PCT = 12.0
ROBUST_EVENT_FLOOR = 30


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(float(value))
    except Exception:
        return default


def build_combined_readthrough(phase356_scenarios: pd.DataFrame, phase360_scenarios: pd.DataFrame) -> pd.DataFrame:
    p356 = phase356_scenarios.loc[phase356_scenarios["scenario_id"].astype(str).eq(PHASE356_PRIMARY_ID)]
    p360 = phase360_scenarios.loc[phase360_scenarios["scenario_id"].astype(str).eq(PHASE360_PRIMARY_ID)]
    if p356.empty or p360.empty:
        return pd.DataFrame()
    p356_row = p356.iloc[0]
    p360_row = p360.iloc[0]
    p356_trades = as_int(p356_row.get("trade_rows"))
    p356_dates = as_int(p356_row.get("diagnostic_trade_dates"))
    p356_net = as_float(p356_row.get("net_pnl_inr"))
    p360_trades = as_int(p360_row.get("capacity_selected_trade_rows"))
    p360_dates = as_int(p360_row.get("diagnostic_trade_dates"))
    p360_net = as_float(p360_row.get("net_pnl_inr"))
    combined_trades = p356_trades + p360_trades
    combined_dates = p356_dates + p360_dates
    combined_net = p356_net + p360_net
    combined_ann = (combined_net / INITIAL_CAPITAL_INR) * (TRADING_DAYS_PER_YEAR / max(1, combined_dates)) * 100.0
    return pd.DataFrame(
        [
            {
                "readthrough_id": "phase356_training_plus_phase360_unseen",
                "phase356_primary_trades": p356_trades,
                "phase356_primary_dates": p356_dates,
                "phase356_primary_net_pnl_inr": p356_net,
                "phase356_primary_annualized_return_pct": as_float(p356_row.get("annualized_return_pct")),
                "phase360_unseen_trades": p360_trades,
                "phase360_unseen_dates": p360_dates,
                "phase360_unseen_net_pnl_inr": p360_net,
                "phase360_unseen_annualized_return_pct": as_float(p360_row.get("annualized_return_pct")),
                "combined_trades": combined_trades,
                "combined_dates": combined_dates,
                "combined_net_pnl_inr": combined_net,
                "combined_annualized_return_pct": combined_ann,
                "combined_above12": int(combined_ann > ANNUALIZED_THRESHOLD_PCT),
                "combined_event_floor_met": int(combined_trades >= ROBUST_EVENT_FLOOR),
                "combined_acceptance_candidate": int(combined_ann > ANNUALIZED_THRESHOLD_PCT and combined_trades >= ROBUST_EVENT_FLOOR),
            }
        ]
    )


def write_outputs(phase356_dir: Path, phase358_dir: Path, phase359_dir: Path, phase360_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase358_summary = read_csv(phase358_dir / "phase358_acceptance_summary.csv")
    phase359_summary = read_csv(phase359_dir / "phase359_acceptance_summary.csv")
    phase360_summary = read_csv(phase360_dir / "phase360_acceptance_summary.csv")
    phase356_scenarios = read_csv(phase356_dir / "phase356_scenario_summary.csv")
    phase360_scenarios = read_csv(phase360_dir / "phase360_scenario_summary.csv")
    combined = build_combined_readthrough(phase356_scenarios, phase360_scenarios)

    p360_primary = phase360_scenarios.loc[phase360_scenarios["scenario_id"].astype(str).eq(PHASE360_PRIMARY_ID)]
    if p360_primary.empty or combined.empty:
        raise FileNotFoundError("Required Phase356/Phase360 primary evidence is missing")
    p360 = p360_primary.iloc[0]
    c = combined.iloc[0]
    unseen_negative = int(as_float(p360["annualized_return_pct"]) <= 0.0 and as_float(p360["net_pnl_inr"]) < 0.0)
    combined_below12 = int(as_int(c["combined_above12"]) == 0)
    combined_below_floor = int(as_int(c["combined_event_floor_met"]) == 0)
    acceptance_rows = as_int(metric_value(phase360_summary, "phase360_acceptance_candidate_rows", 0))

    decision = pd.DataFrame(
        [
            {
                "decision_id": "P361_CLOSE_FULL_DEPTH_MARKET_NEUTRAL_FADE_FOR_ACCEPTANCE",
                "decision": "close_for_acceptance_under_current_real_l2_evidence",
                "reason": "The sparse Phase358 positive clue failed on unseen real L2 and the combined read-through is below the 12% threshold and below the 30-event floor.",
                "parameter_rescue_allowed": 0,
                "additional_same_family_filter_rescue_allowed": 0,
                "additional_real_date_falsification_allowed": 1,
                "materially_new_thesis_allowed": 1,
                "paper_live_or_profit_claim_allowed": 0,
            }
        ]
    )
    interpretation = pd.DataFrame(
        [
            {
                "interpretation_id": "unseen_failure",
                "value": unseen_negative,
                "evidence": f"net={p360['net_pnl_inr']}; annualized={p360['annualized_return_pct']}",
                "decision": "Phase358 positive clue did not survive first unseen local real-L2 expansion.",
            },
            {
                "interpretation_id": "combined_below_threshold",
                "value": combined_below12,
                "evidence": f"combined_annualized={c['combined_annualized_return_pct']}; threshold={ANNUALIZED_THRESHOLD_PCT}",
                "decision": "Combined read-through is not profitable by the user's 12% annualized bar.",
            },
            {
                "interpretation_id": "combined_event_floor_failed",
                "value": combined_below_floor,
                "evidence": f"combined_trades={c['combined_trades']}; required={ROBUST_EVENT_FLOOR}",
                "decision": "Even after unseen expansion, event count is below acceptance floor.",
            },
            {
                "interpretation_id": "no_acceptance_survivor",
                "value": int(acceptance_rows == 0),
                "evidence": f"phase360_acceptance_candidate_rows={acceptance_rows}",
                "decision": "No replay, paper/live, promotion or deployable profitability claim is allowed.",
            },
        ]
    )
    gates = pd.DataFrame(
        [
            ("P361_PHASE358_PRESENT", int(as_int(metric_value(phase358_summary, "phase358_full_depth_market_neutral_fade_execution_complete", 0)) == 1), "Phase358 summary present"),
            ("P361_PHASE359_PRESENT", int(as_int(metric_value(phase359_summary, "phase359_local_unseen_real_l2_catalyst_expansion_complete", 0)) == 1), "Phase359 summary present"),
            ("P361_PHASE360_PRESENT", int(as_int(metric_value(phase360_summary, "phase360_full_depth_market_neutral_fade_unseen_execution_complete", 0)) == 1), "Phase360 summary present"),
            ("P361_UNSEEN_FAILURE_RECORDED", unseen_negative, f"phase360_ann={p360['annualized_return_pct']}"),
            ("P361_COMBINED_READTHROUGH_BELOW12_RECORDED", combined_below12, f"combined_ann={c['combined_annualized_return_pct']}"),
            ("P361_EVENT_FLOOR_RECHECKED", 1, f"combined_trades={c['combined_trades']}"),
            ("P361_PARAMETER_RESCUE_FORBIDDEN", 1, "same-family parameter/filter rescue closed"),
            ("P361_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "closed"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )
    passed = int(gates["passed"].astype(int).sum())
    summary = pd.DataFrame(
        [
            ("phase361_full_depth_fade_unseen_interpretation_complete", 1, "Phase361 interpretation completed"),
            ("phase361_phase360_unseen_net_pnl_inr", p360["net_pnl_inr"], "Phase360 primary unseen net PnL"),
            ("phase361_phase360_unseen_annualized_return_pct", p360["annualized_return_pct"], "Phase360 primary unseen annualized return"),
            ("phase361_combined_trade_rows", c["combined_trades"], "Phase356 + Phase360 trades"),
            ("phase361_combined_diagnostic_dates", c["combined_dates"], "Phase356 + Phase360 dates"),
            ("phase361_combined_net_pnl_inr", c["combined_net_pnl_inr"], "Combined net PnL"),
            ("phase361_combined_annualized_return_pct", c["combined_annualized_return_pct"], "Combined annualized return"),
            ("phase361_combined_above12", c["combined_above12"], "Combined above 12%"),
            ("phase361_combined_event_floor_met", c["combined_event_floor_met"], "Combined event floor met"),
            ("phase361_acceptance_candidate_rows", c["combined_acceptance_candidate"], "Combined acceptance candidates"),
            ("phase361_branch_closed_for_acceptance", 1, "Full-depth market-neutral fade closed for acceptance under current evidence"),
            ("phase361_parameter_rescue_allowed", 0, "No same-family parameter rescue"),
            ("phase361_additional_real_date_falsification_allowed", 1, "More real dates may be used for falsification evidence"),
            ("phase361_materially_new_thesis_allowed", 1, "A materially different thesis may be precommitted"),
            ("phase361_strategy_promotion_allowed", 0, "No promotion"),
            ("phase361_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase361_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase361_hard_gate_pass_rows", passed, "Passed hard gates"),
            ("phase361_hard_gate_rows", len(gates), "Hard gates"),
            ("phase361_next_best_action", "precommit_materially_new_real_l2_thesis_or_expand_real_dates_for_falsification_no_paper_live", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    outputs = {
        "summary": output_dir / "phase361_acceptance_summary.csv",
        "combined": output_dir / "phase361_combined_readthrough.csv",
        "interpretation": output_dir / "phase361_interpretation_ledger.csv",
        "decision": output_dir / "phase361_branch_decision_ledger.csv",
        "gates": output_dir / "phase361_gate_evaluation.csv",
        "report": output_dir / "phase361_full_depth_fade_unseen_interpretation_report.md",
        "manifest": output_dir / "phase361_full_depth_fade_unseen_interpretation_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    combined.to_csv(outputs["combined"], index=False)
    interpretation.to_csv(outputs["interpretation"], index=False)
    decision.to_csv(outputs["decision"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    report = "\n".join(
        [
            "# Phase361 Full-Depth Fade Unseen Interpretation",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase361 interprets the Phase360 unseen real-L2 result for the Phase357/358 full-depth market-neutral fade family. It is a branch decision, not a new search.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Combined read-through",
            "",
            _markdown_table(combined),
            "",
            "## Interpretation",
            "",
            _markdown_table(interpretation),
            "",
            "## Branch decision",
            "",
            _markdown_table(decision),
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
        "phase": 361,
        "generated_at_utc": generated_utc,
        "phase356_dir": str(phase356_dir),
        "phase358_dir": str(phase358_dir),
        "phase359_dir": str(phase359_dir),
        "phase360_dir": str(phase360_dir),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase361_full_depth_fade_unseen_interpretation",
            generated_utc=generated_utc,
            inputs={
                "phase356_scenarios": str(phase356_dir / "phase356_scenario_summary.csv"),
                "phase358_summary": str(phase358_dir / "phase358_acceptance_summary.csv"),
                "phase359_summary": str(phase359_dir / "phase359_acceptance_summary.csv"),
                "phase360_scenarios": str(phase360_dir / "phase360_scenario_summary.csv"),
            },
            parameters={"annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT, "event_floor": ROBUST_EVENT_FLOOR},
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": str(summary[summary["metric"].eq("phase361_next_best_action")]["value"].iloc[0]),
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase356-dir", type=Path, default=DEFAULT_PHASE356_DIR)
    parser.add_argument("--phase358-dir", type=Path, default=DEFAULT_PHASE358_DIR)
    parser.add_argument("--phase359-dir", type=Path, default=DEFAULT_PHASE359_DIR)
    parser.add_argument("--phase360-dir", type=Path, default=DEFAULT_PHASE360_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase356_dir, args.phase358_dir, args.phase359_dir, args.phase360_dir, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
