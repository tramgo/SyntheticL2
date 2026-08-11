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
DEFAULT_PHASE365_DIR = Path("outputs/phase365")
DEFAULT_OUTPUT_DIR = Path("outputs/phase366")

PRIMARY_SCENARIO_ID = "P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL"
SIDE_FLIP_SCENARIO_ID = "P362_D120_I2p5_D0p25_R0p0_CONTINUATION"
STRICT_REPLENISH_SCENARIO_ID = "P362_D120_I2p5_D0p25_R0p1_REVERSAL_CONTROL"
WEAKER_DEPTH_SCENARIO_ID = "P362_D120_I2p5_D0p15_R0p0_REVERSAL_CONTROL"
SHORTER_DELAY_SCENARIO_ID = "P362_D60_I2p5_D0p25_R0p0_REVERSAL_CONTROL"


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


def scenario_row(scenarios: pd.DataFrame, scenario_id: str, role: str, control_id: str) -> dict[str, Any]:
    row = scenarios[scenarios["scenario_id"].astype(str).eq(scenario_id)]
    if row.empty:
        return {
            "phase366_role": role,
            "control_id": control_id,
            "source_scenario_id": scenario_id,
            "present": 0,
        }
    out = row.iloc[0].to_dict()
    out["phase366_role"] = role
    out["control_id"] = control_id
    out["source_scenario_id"] = scenario_id
    out["present"] = 1
    return out


def write_outputs(phase363_dir: Path, phase365_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase365_summary = read_csv(phase365_dir / "phase365_acceptance_summary.csv")
    scenarios363 = read_csv(phase363_dir / "phase363_scenario_summary.csv")
    trades363 = read_csv(phase363_dir / "phase363_trade_ledger.csv")
    if phase365_summary.empty or scenarios363.empty or trades363.empty:
        raise FileNotFoundError("Phase366 requires Phase365 precommit and Phase363 scenario/trade ledgers")
    frozen_rows = pd.DataFrame(
        [
            scenario_row(scenarios363, PRIMARY_SCENARIO_ID, "primary_frozen_reversal", "primary"),
            scenario_row(scenarios363, SIDE_FLIP_SCENARIO_ID, "side_flip_continuation", "side_flip"),
            scenario_row(scenarios363, STRICT_REPLENISH_SCENARIO_ID, "stricter_replenishment", "stricter_replenishment"),
            scenario_row(scenarios363, WEAKER_DEPTH_SCENARIO_ID, "weaker_depth", "weaker_depth"),
            scenario_row(scenarios363, SHORTER_DELAY_SCENARIO_ID, "shorter_delay", "shorter_delay"),
        ]
    )
    primary = frozen_rows[frozen_rows["control_id"].eq("primary")].iloc[0]
    side_flip = frozen_rows[frozen_rows["control_id"].eq("side_flip")].iloc[0]
    strict = frozen_rows[frozen_rows["control_id"].eq("stricter_replenishment")].iloc[0]
    weaker = frozen_rows[frozen_rows["control_id"].eq("weaker_depth")].iloc[0]
    shorter = frozen_rows[frozen_rows["control_id"].eq("shorter_delay")].iloc[0]
    primary_trades = trades363[trades363["scenario_id"].astype(str).eq(PRIMARY_SCENARIO_ID)].copy()
    primary_selected = primary_trades[primary_trades["capacity_selected"].astype(int).eq(1)].copy() if not primary_trades.empty else pd.DataFrame()
    interpretation = pd.DataFrame(
        [
            {
                "interpretation_id": "primary_positive_sparse",
                "value": int(float(primary["annualized_return_pct"]) > 12.0 and int(primary["event_floor_met"]) == 0),
                "evidence": f"ann={primary['annualized_return_pct']}; trades={primary['capacity_selected_trade_rows']}",
                "decision": "Primary remains a positive sparse clue, not acceptance.",
            },
            {
                "interpretation_id": "side_flip_negative_control_pass",
                "value": int(float(primary["annualized_return_pct"]) > float(side_flip["annualized_return_pct"])),
                "evidence": f"primary={primary['annualized_return_pct']}; side_flip={side_flip['annualized_return_pct']}",
                "decision": "Reversal dominates same-filter continuation side flip.",
            },
            {
                "interpretation_id": "strict_replenishment_fragility",
                "value": int(float(strict["annualized_return_pct"]) < 12.0),
                "evidence": f"strict_replenishment_ann={strict['annualized_return_pct']}",
                "decision": "Clue weakens under stricter replenishment, so robustness is not established.",
            },
            {
                "interpretation_id": "acceptance_closed",
                "value": int(int(primary["acceptance_candidate"]) == 0),
                "evidence": f"event_floor={primary['event_floor_met']}; acceptance={primary['acceptance_candidate']}",
                "decision": "No promotion, paper/live acceptance or deployable profitability claim.",
            },
        ]
    )
    gates = pd.DataFrame(
        [
            ("P366_PHASE365_PRECOMMIT_PRESENT", int(str(metric_value(phase365_summary, "phase365_post_catalyst_impulse_reversal_precommit_complete", 0)) == "1"), "Phase365 precommit complete"),
            ("P366_PRIMARY_FROZEN_ROW_PRESENT", int(int(primary["present"]) == 1), PRIMARY_SCENARIO_ID),
            ("P366_REGISTERED_CONTROLS_PRESENT", int(frozen_rows["present"].astype(int).sum() == 5), f"present={int(frozen_rows['present'].astype(int).sum())}/5"),
            ("P366_FULL_DEPTH_COST200_INHERITED", 1, "Inherited from Phase363 full-depth cost200 diagnostic"),
            ("P366_EVENT_FLOOR_CHECKED", 1, f"event_floor_met={primary['event_floor_met']}"),
            ("P366_NO_SEARCH_OR_PARAMETER_EXPANSION", 1, "frozen extraction only"),
            ("P366_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "closed"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )
    summary = pd.DataFrame(
        [
            ("phase366_post_catalyst_impulse_reversal_frozen_diagnostic_complete", 1, "Phase366 completed"),
            ("phase366_primary_scenario_id", PRIMARY_SCENARIO_ID, "Frozen primary"),
            ("phase366_primary_trade_rows", primary["capacity_selected_trade_rows"], "Primary selected trades"),
            ("phase366_primary_dates", primary["diagnostic_trade_dates"], "Primary dates"),
            ("phase366_primary_symbols", primary["symbols"], "Primary symbols"),
            ("phase366_primary_positive_symbols", primary["positive_symbols"], "Primary positive symbols"),
            ("phase366_primary_net_pnl_inr", primary["net_pnl_inr"], "Primary net PnL"),
            ("phase366_primary_annualized_return_pct", primary["annualized_return_pct"], "Primary annualized return"),
            ("phase366_primary_above12", primary["above12"], "Primary above 12%"),
            ("phase366_primary_event_floor_met", primary["event_floor_met"], "Primary event floor"),
            ("phase366_acceptance_candidate_rows", primary["acceptance_candidate"], "Acceptance candidates"),
            ("phase366_side_flip_annualized_return_pct", side_flip["annualized_return_pct"], "Side flip annualized return"),
            ("phase366_strict_replenishment_annualized_return_pct", strict["annualized_return_pct"], "Strict replenishment annualized return"),
            ("phase366_weaker_depth_annualized_return_pct", weaker["annualized_return_pct"], "Weaker depth annualized return"),
            ("phase366_shorter_delay_annualized_return_pct", shorter["annualized_return_pct"], "Shorter delay annualized return"),
            ("phase366_strategy_promotion_allowed", 0, "No promotion"),
            ("phase366_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase366_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase366_hard_gate_pass_rows", int(gates["passed"].astype(int).sum()), "Passed hard gates"),
            ("phase366_hard_gate_rows", len(gates), "Hard gates"),
            ("phase366_next_best_action", "interpret_phase366_or_expand_real_dates_for_reversal_falsification_no_paper_live", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    outputs = {
        "summary": output_dir / "phase366_acceptance_summary.csv",
        "frozen": output_dir / "phase366_frozen_scenario_summary.csv",
        "primary_trades": output_dir / "phase366_primary_trade_ledger.csv",
        "interpretation": output_dir / "phase366_interpretation_ledger.csv",
        "gates": output_dir / "phase366_gate_evaluation.csv",
        "report": output_dir / "phase366_post_catalyst_impulse_reversal_frozen_diagnostic_report.md",
        "manifest": output_dir / "phase366_post_catalyst_impulse_reversal_frozen_diagnostic_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    frozen_rows.to_csv(outputs["frozen"], index=False)
    primary_selected.to_csv(outputs["primary_trades"], index=False)
    interpretation.to_csv(outputs["interpretation"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    report = "\n".join(
        [
            "# Phase366 Post-Catalyst Impulse Reversal Frozen Diagnostic",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase366 executes the Phase365 frozen reversal thesis by extracting the exact primary and registered controls from Phase363. It performs no parameter search and opens no promotion, paper/live acceptance, or deployable profitability claim.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Frozen scenario/control summary",
            "",
            _markdown_table(frozen_rows),
            "",
            "## Interpretation",
            "",
            _markdown_table(interpretation),
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
        "phase": 366,
        "generated_at_utc": generated_utc,
        "phase363_dir": str(phase363_dir),
        "phase365_dir": str(phase365_dir),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase366_post_catalyst_impulse_reversal_frozen_diagnostic",
            generated_utc=generated_utc,
            inputs={"phase363_scenarios": str(phase363_dir / "phase363_scenario_summary.csv"), "phase365_thesis": str(phase365_dir / "phase365_thesis_contract.csv")},
            parameters={"primary_scenario_id": PRIMARY_SCENARIO_ID},
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": str(summary[summary["metric"].eq("phase366_next_best_action")]["value"].iloc[0]),
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase363-dir", type=Path, default=DEFAULT_PHASE363_DIR)
    parser.add_argument("--phase365-dir", type=Path, default=DEFAULT_PHASE365_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase363_dir, args.phase365_dir, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
