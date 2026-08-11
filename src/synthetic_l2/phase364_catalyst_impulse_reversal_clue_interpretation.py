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


DEFAULT_PHASE363_DIR = Path("outputs/phase363")
DEFAULT_OUTPUT_DIR = Path("outputs/phase364")
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


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(float(value))
    except Exception:
        return default


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def write_outputs(phase363_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    summary363 = read_csv(phase363_dir / "phase363_acceptance_summary.csv")
    scenarios = read_csv(phase363_dir / "phase363_scenario_summary.csv")
    if summary363.empty or scenarios.empty:
        raise FileNotFoundError("Phase363 summary/scenario evidence is missing")

    continuation = scenarios[scenarios["scenario_role"].astype(str).eq("impulse_continuation")].copy()
    reversal = scenarios[scenarios["scenario_role"].astype(str).eq("impulse_reversal_control")].copy()
    above12_reversal = reversal[reversal["above12"].astype(int).eq(1)].copy()
    above12_continuation = continuation[continuation["above12"].astype(int).eq(1)].copy()
    best_reversal = reversal.sort_values(["annualized_return_pct", "capacity_selected_trade_rows"], ascending=[False, False]).iloc[0]
    best_continuation = continuation.sort_values(["annualized_return_pct", "capacity_selected_trade_rows"], ascending=[False, False]).iloc[0]
    best_reversal_sparse = as_int(best_reversal["capacity_selected_trade_rows"]) < ROBUST_EVENT_FLOOR
    decision = pd.DataFrame(
        [
            {
                "decision_id": "P364_REJECT_PHASE362_CONTINUATION_PRIMARY",
                "decision": "reject_primary_continuation_thesis_for_acceptance",
                "reason": "All impulse-continuation variants were below the 12% annualized threshold.",
                "evidence": f"continuation_above12_rows={len(above12_continuation)}; best_continuation_ann={best_continuation['annualized_return_pct']}",
                "paper_live_or_profit_claim_allowed": 0,
            },
            {
                "decision_id": "P364_FREEZE_REVERSAL_AFTER_REPLENISHMENT_CLUE",
                "decision": "freeze_as_new_precommit_candidate_not_acceptance",
                "reason": "All above-12 rows came from impulse-reversal controls, not the precommitted continuation thesis, and the best clue is below the 30-event floor.",
                "evidence": f"reversal_above12_rows={len(above12_reversal)}; best_reversal={best_reversal['scenario_id']}; trades={best_reversal['capacity_selected_trade_rows']}; ann={best_reversal['annualized_return_pct']}",
                "paper_live_or_profit_claim_allowed": 0,
            },
        ]
    )
    clue_contract = pd.DataFrame(
        [
            {
                "clue_id": "P364_POST_CATALYST_IMPULSE_REVERSAL_AFTER_REPLENISHMENT",
                "source_phase": "Phase363",
                "source_scenario_id": best_reversal["scenario_id"],
                "decision_delay_seconds": 120,
                "min_abs_impulse_bps": 2.5,
                "min_abs_l2_l5_imbalance": 0.25,
                "min_replenishment_ratio": 0.0,
                "side_rule": "reverse the signed post-catalyst impulse after displayed liquidity replenishment and levels 2-5 support the original impulse",
                "best_capacity_selected_trade_rows": best_reversal["capacity_selected_trade_rows"],
                "best_diagnostic_trade_dates": best_reversal["diagnostic_trade_dates"],
                "best_symbols": best_reversal["symbols"],
                "best_net_pnl_inr": best_reversal["net_pnl_inr"],
                "best_annualized_return_pct": best_reversal["annualized_return_pct"],
                "event_floor_met": best_reversal["event_floor_met"],
                "acceptance_candidate": best_reversal["acceptance_candidate"],
                "status": "sparse_clue_requires_precommit",
            }
        ]
    )
    interpretation = pd.DataFrame(
        [
            {
                "interpretation_id": "continuation_failed",
                "value": int(len(above12_continuation) == 0),
                "evidence": f"continuation_above12_rows={len(above12_continuation)}; best_continuation_ann={best_continuation['annualized_return_pct']}",
                "decision": "Do not continue the Phase362 primary continuation thesis for acceptance.",
            },
            {
                "interpretation_id": "reversal_control_positive_sparse",
                "value": int(len(above12_reversal) > 0 and best_reversal_sparse),
                "evidence": f"reversal_above12_rows={len(above12_reversal)}; best_trades={best_reversal['capacity_selected_trade_rows']}; required={ROBUST_EVENT_FLOOR}",
                "decision": "Treat reversal-after-replenishment as a new sparse clue only.",
            },
            {
                "interpretation_id": "acceptance_still_closed",
                "value": int(as_int(metric_value(summary363, "phase363_acceptance_candidate_rows", 0)) == 0),
                "evidence": f"phase363_acceptance_candidate_rows={metric_value(summary363, 'phase363_acceptance_candidate_rows', 0)}",
                "decision": "No replay, promotion, paper/live acceptance or deployable profitability claim.",
            },
        ]
    )
    gates = pd.DataFrame(
        [
            ("P364_PHASE363_PRESENT", 1, "Phase363 summary and scenarios present"),
            ("P364_CONTINUATION_FAILURE_RECORDED", int(len(above12_continuation) == 0), f"continuation_above12={len(above12_continuation)}"),
            ("P364_REVERSAL_CLUE_RECORDED", int(len(above12_reversal) > 0), f"reversal_above12={len(above12_reversal)}"),
            ("P364_EVENT_FLOOR_BLOCKER_RECORDED", int(best_reversal_sparse), f"best_trades={best_reversal['capacity_selected_trade_rows']}"),
            ("P364_NO_ACCEPTANCE_CANDIDATES", int(as_int(metric_value(summary363, "phase363_acceptance_candidate_rows", 0)) == 0), f"acceptance_rows={metric_value(summary363, 'phase363_acceptance_candidate_rows', 0)}"),
            ("P364_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "closed"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )
    summary = pd.DataFrame(
        [
            ("phase364_catalyst_impulse_reversal_clue_interpretation_complete", 1, "Phase364 interpretation completed"),
            ("phase364_phase363_above12_rows", metric_value(summary363, "phase363_above12_rows", 0), "Phase363 above-12 rows"),
            ("phase364_continuation_above12_rows", len(above12_continuation), "Continuation above-12 rows"),
            ("phase364_reversal_control_above12_rows", len(above12_reversal), "Reversal-control above-12 rows"),
            ("phase364_best_reversal_scenario_id", best_reversal["scenario_id"], "Best reversal clue"),
            ("phase364_best_reversal_trade_rows", best_reversal["capacity_selected_trade_rows"], "Best reversal selected trades"),
            ("phase364_best_reversal_dates", best_reversal["diagnostic_trade_dates"], "Best reversal dates"),
            ("phase364_best_reversal_symbols", best_reversal["symbols"], "Best reversal symbols"),
            ("phase364_best_reversal_net_pnl_inr", best_reversal["net_pnl_inr"], "Best reversal net PnL"),
            ("phase364_best_reversal_annualized_return_pct", best_reversal["annualized_return_pct"], "Best reversal annualized return"),
            ("phase364_best_reversal_event_floor_met", best_reversal["event_floor_met"], "Best reversal event floor"),
            ("phase364_acceptance_candidate_rows", 0, "No acceptance candidates"),
            ("phase364_strategy_promotion_allowed", 0, "No promotion"),
            ("phase364_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase364_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase364_hard_gate_pass_rows", int(gates["passed"].astype(int).sum()), "Passed hard gates"),
            ("phase364_hard_gate_rows", len(gates), "Hard gates"),
            ("phase364_next_best_action", "precommit_phase365_post_catalyst_impulse_reversal_after_replenishment_no_paper_live", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    outputs = {
        "summary": output_dir / "phase364_acceptance_summary.csv",
        "interpretation": output_dir / "phase364_interpretation_ledger.csv",
        "decision": output_dir / "phase364_branch_decision_ledger.csv",
        "clue": output_dir / "phase364_reversal_clue_contract.csv",
        "gates": output_dir / "phase364_gate_evaluation.csv",
        "report": output_dir / "phase364_catalyst_impulse_reversal_clue_interpretation_report.md",
        "manifest": output_dir / "phase364_catalyst_impulse_reversal_clue_interpretation_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    interpretation.to_csv(outputs["interpretation"], index=False)
    decision.to_csv(outputs["decision"], index=False)
    clue_contract.to_csv(outputs["clue"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    report = "\n".join(
        [
            "# Phase364 Catalyst Impulse Reversal Clue Interpretation",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase364 interprets Phase363. It rejects the precommitted impulse-continuation thesis for acceptance and freezes the impulse-reversal-after-replenishment control as a new sparse clue requiring its own precommit.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Interpretation",
            "",
            _markdown_table(interpretation),
            "",
            "## Branch decisions",
            "",
            _markdown_table(decision),
            "",
            "## Reversal clue contract",
            "",
            _markdown_table(clue_contract),
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
        "phase": 364,
        "generated_at_utc": generated_utc,
        "phase363_dir": str(phase363_dir),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase364_catalyst_impulse_reversal_clue_interpretation",
            generated_utc=generated_utc,
            inputs={"phase363_summary": str(phase363_dir / "phase363_acceptance_summary.csv"), "phase363_scenarios": str(phase363_dir / "phase363_scenario_summary.csv")},
            parameters={"annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT, "event_floor": ROBUST_EVENT_FLOOR},
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": str(summary[summary["metric"].eq("phase364_next_best_action")]["value"].iloc[0]),
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase363-dir", type=Path, default=DEFAULT_PHASE363_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase363_dir, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
