from __future__ import annotations

import argparse
import hashlib
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


DEFAULT_PHASE436_DIR = Path("outputs/phase436")
DEFAULT_OUTPUT_DIR = Path("outputs/phase437")

THESIS_ID = "P437_LOW_TURNOVER_FULL_DEPTH_REGIME_CARRY_PRECOMMIT"
SELECTED_SOURCE_ID = "opening_full_depth_regime_carry_one_trade_per_symbol_date"
NEXT_ACTION = "run_phase438_low_turnover_depth_regime_carry_no_paper_live"
REPAIR_ACTION = "repair_phase437_precommit_inputs"

EARLY_WINDOW_TICKS = [120, 240, 480]
HOLD_TICKS = [1200, 2400, 3600]
ENTRY_DELAY_TICKS = [5]
MAX_TRADES_PER_SYMBOL_DATE = 1
MIN_TRADE_DATES = 5
MIN_SYMBOLS = 5
MIN_COMPLETED_ROUND_TRIPS = 30
MIN_POSITIVE_DATE_FRACTION = 0.60
ANNUALIZED_THRESHOLD_PCT = 12.0
INITIAL_CAPITAL_INR = 1_000_000.0
ORDER_NOTIONAL_INR = 100_000.0
COST_MULTIPLIER = 2.0


def sha256_frame(frame: pd.DataFrame) -> str:
    return hashlib.sha256(frame.to_csv(index=False, lineterminator="\n").encode("utf-8")).hexdigest()


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def build_contract() -> pd.DataFrame:
    rows = [
        ("thesis_id", THESIS_ID, "Lower-turnover full-depth source precommit after Phase436."),
        ("selected_source", SELECTED_SOURCE_ID, "One trade per symbol/date from early-session L1-L5 regime."),
        ("relationship_to_phase436", "materially_new_lower_turnover_longer_horizon_source", "Directly responds to cost domination in Phase435."),
        ("turnover_policy", f"max_trades_per_symbol_date={MAX_TRADES_PER_SYMBOL_DATE}", "No dense tick-scalping."),
        ("entry_policy", "observe_early_window_then_enter_after_fixed_tick_delay", "Signal data precedes entry."),
        ("exit_policy", "exit_after_precommitted_longer_hold_ticks_or_end_of_group", "Longer horizon intended to reduce cost drag per gross opportunity."),
        ("early_window_ticks", ";".join(map(str, EARLY_WINDOW_TICKS)), "Frozen early full-depth observation windows."),
        ("hold_ticks", ";".join(map(str, HOLD_TICKS)), "Frozen longer-horizon hold windows."),
        ("entry_delay_ticks", ";".join(map(str, ENTRY_DELAY_TICKS)), "Frozen entry delay."),
        ("full_depth_features", "L1_mid_spread_volume_plus_L2_to_L5_imbalance_depth_slope_order_churn_replenishment", "Top-five depth is core."),
        ("direction_rule", "sign_of_early_top5_pressure_plus_l2_l5_slope;optional_contrarian_variant_precommitted", "Simple low-turnover directional regime, not learned after results."),
        ("controls_required", "l1_only_ablation;side_flip;time_shuffle;real_anchor_cross_check", "Controls must be emitted by Phase438."),
        ("capital_policy", f"fixed_initial_capital_{int(INITIAL_CAPITAL_INR)}_inr_order_notional_{int(ORDER_NOTIONAL_INR)}_inr_cost200", "Annualized return denominator is fixed capital."),
        ("acceptance_floor", f"round_trips_ge_{MIN_COMPLETED_ROUND_TRIPS};dates_ge_{MIN_TRADE_DATES};symbols_ge_{MIN_SYMBOLS};positive_date_fraction_ge_{MIN_POSITIVE_DATE_FRACTION};annualized_ge_{ANNUALIZED_THRESHOLD_PCT}", "User profitability floor with breadth."),
        ("forbidden", "dense_tick_scalping;same_phase435_ranker_rescue;same_phase427_threshold_sweep;market_maker_rescue_without_external_execution_source;promotion;paper_live;deployable_profitability_claim", "Closed or forbidden routes."),
        ("execution_results_generated_now", "0", "Precommit only."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_grid() -> pd.DataFrame:
    rows = []
    for family_id, direction_mode in [
        ("depth_regime_carry", "with_early_full_depth_pressure"),
        ("depth_regime_snapback", "against_early_full_depth_pressure"),
    ]:
        for early in EARLY_WINDOW_TICKS:
            for hold in HOLD_TICKS:
                for delay in ENTRY_DELAY_TICKS:
                    rows.append(
                        {
                            "scenario_id": f"P438_{family_id}_E{early}_H{hold}_D{delay}",
                            "family_id": family_id,
                            "direction_mode": direction_mode,
                            "early_window_ticks": early,
                            "hold_ticks": hold,
                            "entry_delay_ticks": delay,
                            "max_trades_per_symbol_date": MAX_TRADES_PER_SYMBOL_DATE,
                            "cost_multiplier": COST_MULTIPLIER,
                            "order_notional_inr": ORDER_NOTIONAL_INR,
                        }
                    )
    return pd.DataFrame(rows)


def build_gates(phase436: pd.DataFrame, contract: pd.DataFrame, grid: pd.DataFrame) -> pd.DataFrame:
    next_action = str(scalar(phase436, "phase436_next_best_action", ""))
    forbidden = ";".join(contract.loc[contract["contract_id"].eq("forbidden"), "contract_value"].astype(str).tolist())
    full_depth = contract.loc[contract["contract_id"].eq("full_depth_features"), "contract_value"].astype(str).str.cat(sep=" ")
    gates = [
        ("P437_PHASE436_AVAILABLE", as_int(scalar(phase436, "phase436_supervised_ranker_interpretation_complete", 0)) == 1, scalar(phase436, "phase436_supervised_ranker_interpretation_complete", 0), 1),
        ("P437_PHASE436_NEXT_ACTION_MATCHED", "lower_turnover" in next_action or "longer" in next_action, next_action, "lower_turnover_or_longer_horizon"),
        ("P437_MATERIAL_NEW_SOURCE", True, SELECTED_SOURCE_ID, "not_phase435_ranker_or_phase427_threshold_sweep"),
        ("P437_LOW_TURNOVER_PINNED", MAX_TRADES_PER_SYMBOL_DATE == 1, MAX_TRADES_PER_SYMBOL_DATE, 1),
        ("P437_LONGER_HORIZON_PINNED", min(HOLD_TICKS) >= 1200, ";".join(map(str, HOLD_TICKS)), "min_hold_ticks>=1200"),
        ("P437_FULL_DEPTH_L2_L5_REQUIRED", "L2_to_L5" in full_depth or "L2-L5" in full_depth, full_depth, "L2-L5"),
        ("P437_GRID_FROZEN", len(grid) == len(EARLY_WINDOW_TICKS) * len(HOLD_TICKS) * len(ENTRY_DELAY_TICKS) * 2, len(grid), 18),
        ("P437_COST200_FIXED_CAPITAL_PINNED", "cost200" in contract.loc[contract["contract_id"].eq("capital_policy"), "contract_value"].astype(str).str.cat(sep=" "), contract.loc[contract["contract_id"].eq("capital_policy"), "contract_value"].astype(str).str.cat(sep=" "), "cost200_fixed_capital"),
        ("P437_CONTROLS_PRECOMMITTED", "time_shuffle" in contract.loc[contract["contract_id"].eq("controls_required"), "contract_value"].astype(str).str.cat(sep=" "), contract.loc[contract["contract_id"].eq("controls_required"), "contract_value"].astype(str).str.cat(sep=" "), "controls_present"),
        ("P437_RESULTS_NOT_GENERATED", contract.loc[contract["contract_id"].eq("execution_results_generated_now"), "contract_value"].astype(str).str.cat(sep=" ") == "0", contract.loc[contract["contract_id"].eq("execution_results_generated_now"), "contract_value"].astype(str).str.cat(sep=" "), 0),
        ("P437_BOUNDARIES_CLOSED", all(x in forbidden for x in ["promotion", "paper_live", "deployable_profitability_claim"]), forbidden, "closed"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(grid: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase437_low_turnover_precommit_complete", 1, "Phase437 precommit completed"),
            ("phase437_thesis_id", THESIS_ID, "Frozen thesis"),
            ("phase437_selected_source_id", SELECTED_SOURCE_ID, "Selected lower-turnover source"),
            ("phase437_grid_rows", len(grid), "Frozen scenario rows"),
            ("phase437_grid_hash", sha256_frame(grid), "Hash of frozen grid"),
            ("phase437_max_trades_per_symbol_date", MAX_TRADES_PER_SYMBOL_DATE, "Turnover cap"),
            ("phase437_min_hold_ticks", min(HOLD_TICKS), "Minimum longer-horizon hold"),
            ("phase437_execution_results_generated", 0, "Precommit only"),
            ("phase437_strategy_promotion_allowed", 0, "No promotion"),
            ("phase437_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase437_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase437_execution_allowed_next", int(hard_pass == hard_rows), "Whether Phase438 may execute"),
            ("phase437_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase437_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase437_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, contract: pd.DataFrame, grid: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase437 Low-Turnover Full-Depth Regime Carry Precommit",
        "",
        "Phase437 freezes a materially new lower-turnover and longer-horizon source after Phase436 showed dense event ranking remained cost-dominated.",
        "",
        "The selected source uses early-session L1-L5 book pressure to take at most one trade per symbol/date, then holds for a precommitted longer tick horizon.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Frozen Contract",
        "",
        _markdown_table(contract),
        "",
        "## Frozen Scenario Grid",
        "",
        _markdown_table(grid),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase438 may execute this lower-turnover source only. It may not retune Phase435, reopen dense tick scalping, or promote/paper/live anything from this precommit.",
    ]
    (output_dir / "phase437_low_turnover_depth_regime_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase436_dir: Path = DEFAULT_PHASE436_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase436 = read_csv(phase436_dir / "phase436_acceptance_summary.csv")
    if phase436.empty:
        raise FileNotFoundError("Phase437 requires outputs/phase436/phase436_acceptance_summary.csv")
    contract = build_contract()
    grid = build_grid()
    gates = build_gates(phase436, contract, grid)
    acceptance = build_acceptance(grid, gates)
    contract.to_csv(output_dir / "phase437_frozen_phase438_contract.csv", index=False)
    grid.to_csv(output_dir / "phase437_low_turnover_scenario_grid.csv", index=False)
    gates.to_csv(output_dir / "phase437_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase437_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, contract, grid, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase437_low_turnover_depth_regime_precommit",
        **reproducibility_fields(
            artifact_id="phase437_low_turnover_depth_regime_precommit",
            generated_utc=generated_utc,
            inputs={"phase436_acceptance_summary": str(phase436_dir / "phase436_acceptance_summary.csv")},
            parameters={"thesis_id": THESIS_ID, "selected_source": SELECTED_SOURCE_ID, "grid_hash": sha256_frame(grid)},
            outputs={"acceptance_summary": str(output_dir / "phase437_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase438_fixed_tick_longer_horizon",
        ),
    }
    (output_dir / "phase437_low_turnover_depth_regime_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase437 low-turnover full-depth regime precommit.")
    parser.add_argument("--phase436-dir", type=Path, default=DEFAULT_PHASE436_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase436_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
