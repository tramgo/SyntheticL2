from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE343_DIR = Path("outputs/phase343")
DEFAULT_OUTPUT_DIR = Path("outputs/phase344")

NEXT_ACTION = "run_phase345_official_catalyst_native_full_depth_strategy_search_execution_no_paper_live"
REPAIR_ACTION = "repair_phase344_official_catalyst_native_full_depth_strategy_search_precommit"

ANNUALIZED_THRESHOLD_PCT = 12.0
ROBUST_EVENT_FLOOR = 30


def build_family_catalog(clues: pd.DataFrame) -> pd.DataFrame:
    positive_capacity = clues[
        clues["scope"].astype(str).eq("capacity_selected") & (clues["net_pnl_inr"].astype(float) > 0)
    ].copy()
    clue_categories = positive_capacity["description"].astype(str).tolist()
    rows = [
        {
            "family_id": "P344_CATALYST_CATEGORY_CONTINUATION",
            "material_new_reason": "Uses official catalyst category and real post-catalyst L2 response; not the failed synthetic survivor signal.",
            "allowed_catalyst_categories": ";".join(clue_categories) if clue_categories else "General Updates;Updates",
            "side_policy": "category_directional_continuation",
            "entry_timing_grid": "market_open_or_first_tick_after_announcement;delay_60s;delay_300s",
            "horizon_grid_seconds": "300;900;1800",
            "full_depth_features": "top5_qty_imbalance;l2_l5_qty_imbalance;top5_order_imbalance;spread;quote_churn",
            "control_required": "category_shuffle;side_flip;random_side",
        },
        {
            "family_id": "P344_FULL_DEPTH_CATALYST_REACTION_FILTER",
            "material_new_reason": "Conditions official catalyst rows on observed real full-depth pressure after event start.",
            "allowed_catalyst_categories": "all_official_categories",
            "side_policy": "depth_pressure_sign",
            "entry_timing_grid": "first_valid_tick;delay_60s;delay_300s",
            "horizon_grid_seconds": "300;900;1800",
            "full_depth_features": "l2_l5_qty_imbalance_delta;top5_order_imbalance_delta;spread_compression;depth_replenishment_proxy",
            "control_required": "depth_feature_shuffle;side_flip;random_side",
        },
        {
            "family_id": "P344_SBIN_AND_BANK_CATALYST_DIAGNOSTIC",
            "material_new_reason": "Separately tests official SBIN/bank catalysts requested by the user, without treating SBIN clues as accepted.",
            "allowed_catalyst_categories": "SBIN;AXISBANK;HDFCBANK;ICICIBANK;KOTAKBANK",
            "side_policy": "bank_catalyst_depth_confirmation",
            "entry_timing_grid": "market_open_or_first_tick_after_announcement;delay_300s",
            "horizon_grid_seconds": "900;1800",
            "full_depth_features": "top5_qty_imbalance;l2_l5_qty_imbalance;spread;receive_event_rate",
            "control_required": "bank_symbol_shuffle;side_flip;random_side",
        },
        {
            "family_id": "P344_NEGATIVE_CONTROL_FAILED_SURVIVOR_REPLAY",
            "material_new_reason": "Negative control only: confirms failed Phase338/339 survivor is not reopened as a tuned route.",
            "allowed_catalyst_categories": "all_official_categories",
            "side_policy": "failed_survivor_frozen_long_only",
            "entry_timing_grid": "phase342_exact",
            "horizon_grid_seconds": "900",
            "full_depth_features": "none_new_negative_control",
            "control_required": "must_remain_closed_for_acceptance",
        },
    ]
    return pd.DataFrame(rows)


def build_search_grid(families: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for family in families.to_dict("records"):
        timing_values = str(family["entry_timing_grid"]).split(";")
        horizon_values = [int(value) for value in str(family["horizon_grid_seconds"]).split(";") if value]
        quantiles = [0.0, 0.5, 0.75] if family["family_id"] != "P344_NEGATIVE_CONTROL_FAILED_SURVIVOR_REPLAY" else [0.0]
        for timing in timing_values:
            for horizon in horizon_values:
                for threshold_quantile in quantiles:
                    rows.append(
                        {
                            "family_id": family["family_id"],
                            "entry_timing_policy": timing,
                            "horizon_seconds": horizon,
                            "depth_threshold_quantile": threshold_quantile,
                            "cost_profile": "zerodha_2x_all_in_cost_proxy",
                            "fixed_capital_required": 1,
                            "full_depth_required": 1,
                            "levels_2_to_5_required": 1,
                            "l1_only_allowed": 0,
                            "no_lookahead_required": 1,
                            "acceptance_allowed_in_phase344": 0,
                        }
                    )
    return pd.DataFrame(rows)


def build_phase345_contract(families: pd.DataFrame, grid: pd.DataFrame, phase343: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("input_official_calendar", "outputs/phase340/phase340_official_catalyst_calendar.csv", "Official catalyst source only."),
        ("input_no_lookahead_eligibility", "outputs/phase341/phase341_no_lookahead_official_catalyst_eligibility_ledger.csv", "Use no-lookahead catalyst timing."),
        ("input_real_trade_diagnostic", "outputs/phase342/phase342_real_day_trade_diagnostic_ledger.csv", "Use as clue/control evidence, not as tuned labels."),
        ("phase343_failed_survivor_closed", metric_value(phase343, "phase343_current_survivor_route_closed", ""), "Failed synthetic survivor remains closed."),
        ("family_rows", len(families), "Search family count."),
        ("grid_rows", len(grid), "Phase345 scenario grid rows."),
        ("material_new_required", 1, "Official-catalyst-native, real-L2/full-depth search only."),
        ("negative_control_required", 1, "Include failed survivor replay as negative control only."),
        ("full_top_five_depth_required", 1, "Use top-five bid/ask price, quantity, and order-count fields."),
        ("levels_2_to_5_materiality_required", 1, "Depth beyond L1 must be material."),
        ("l1_only_allowed", 0, "No L1-only variants."),
        ("no_lookahead_required", 1, "No future catalyst or price information at signal time."),
        ("fixed_capital_denominator_required", 1, "No unlimited-capital annualization."),
        ("cost_profile_required", "zerodha_2x_all_in_cost_proxy", "Keep 2x Zerodha all-in cost stress."),
        ("cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned cost model."),
        ("annualized_threshold_pct", ANNUALIZED_THRESHOLD_PCT, "Keep user threshold."),
        ("robust_event_floor", ROBUST_EVENT_FLOOR, "Do not accept sparse pockets below 30 events."),
        ("controls_required", "side_flip;random_side;category_shuffle_or_feature_shuffle", "Controls must run in execution phase."),
        ("paper_or_live_allowed", 0, "No paper/live acceptance."),
        ("deployable_profitability_claim_allowed", 0, "No deployable profitability claim."),
        ("phase345_execution_allowed_next", 1, "Open Phase345 execution if gates pass."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_gate_evaluation(phase343: pd.DataFrame, families: pd.DataFrame, grid: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    phase343_complete = as_int(metric_value(phase343, "phase343_official_catalyst_real_day_diagnostic_interpretation_complete", 0))
    survivor_closed = as_int(metric_value(phase343, "phase343_current_survivor_route_closed", 0))
    negative_control_rows = int(families["family_id"].astype(str).eq("P344_NEGATIVE_CONTROL_FAILED_SURVIVOR_REPLAY").sum())
    rows = [
        ("P344_PHASE343_COMPLETE", phase343_complete == 1, phase343_complete, 1),
        ("P344_FAILED_SURVIVOR_CLOSED", survivor_closed == 1, survivor_closed, 1),
        ("P344_MATERIAL_NEW_FAMILIES_PRESENT", len(families) >= 3, len(families), ">=3"),
        ("P344_GRID_PRESENT", len(grid) > 0, len(grid), ">0"),
        ("P344_NEGATIVE_CONTROL_PRESENT", negative_control_rows == 1, negative_control_rows, 1),
        ("P344_FULL_DEPTH_NO_L1_ONLY_NO_LOOKAHEAD", bool(grid["full_depth_required"].eq(1).all() and grid["levels_2_to_5_required"].eq(1).all() and grid["l1_only_allowed"].eq(0).all() and grid["no_lookahead_required"].eq(1).all()), "preserved", "preserved"),
        ("P344_CONTRACT_PRESENT", len(contract) >= 18, len(contract), ">=18"),
        ("P344_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", True, "closed", "closed"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed", "required"])


def write_outputs(phase343_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase343 = read_csv(phase343_dir / "phase343_acceptance_summary.csv")
    clues = pd.read_csv(phase343_dir / "phase343_diagnostic_clue_ledger.csv")
    families = build_family_catalog(clues)
    grid = build_search_grid(families)
    contract = build_phase345_contract(families, grid, phase343)
    gates = build_gate_evaluation(phase343, families, grid, contract)
    passed = int(gates["passed"].astype(bool).sum())
    total = int(len(gates))
    summary = pd.DataFrame(
        [
            ("phase344_official_catalyst_native_full_depth_strategy_search_precommit_complete", 1, "Phase344 precommit completed"),
            ("phase344_phase343_complete", as_int(metric_value(phase343, "phase343_official_catalyst_real_day_diagnostic_interpretation_complete", 0)), "Phase343 complete"),
            ("phase344_failed_survivor_closed", as_int(metric_value(phase343, "phase343_current_survivor_route_closed", 0)), "Failed survivor remains closed"),
            ("phase344_family_rows", len(families), "Search family rows"),
            ("phase344_grid_rows", len(grid), "Search grid rows"),
            ("phase344_negative_control_rows", int(families["family_id"].astype(str).eq("P344_NEGATIVE_CONTROL_FAILED_SURVIVOR_REPLAY").sum()), "Negative control family rows"),
            ("phase344_material_new_required", 1, "Material-new route required"),
            ("phase344_full_depth_required", 1, "Full top-five depth required"),
            ("phase344_levels_2_to_5_required", 1, "Levels 2-5 materiality required"),
            ("phase344_l1_only_allowed", 0, "No L1-only variants"),
            ("phase344_no_lookahead_required", 1, "No lookahead"),
            ("phase344_phase345_execution_allowed_next", int(passed == total), "Phase345 execution allowed next"),
            ("phase344_strategy_promotion_allowed", 0, "No promotion"),
            ("phase344_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase344_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase344_hard_gate_pass_rows", passed, "Passed hard gates"),
            ("phase344_hard_gate_rows", total, "Hard gates"),
            ("phase344_next_best_action", NEXT_ACTION if passed == total else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )
    report = "\n".join(
        [
            "# Phase344 Official-Catalyst-Native Full-Depth Strategy Search Precommit",
            "",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
            "Phase344 precommits a materially new official-catalyst-native full-depth search. The failed Phase338/339 survivor remains closed.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Family catalog",
            "",
            _markdown_table(families),
            "",
            "## Gate evaluation",
            "",
            _markdown_table(gates),
            "",
            "No promotion, paper/live acceptance, or deployable profitability claim is opened by Phase344.",
        ]
    )
    outputs = {
        "summary": output_dir / "phase344_acceptance_summary.csv",
        "family_catalog": output_dir / "phase344_strategy_family_catalog.csv",
        "grid": output_dir / "phase344_phase345_search_grid.csv",
        "contract": output_dir / "phase344_phase345_execution_contract.csv",
        "gates": output_dir / "phase344_gate_evaluation.csv",
        "report": output_dir / "phase344_official_catalyst_native_full_depth_strategy_search_precommit_report.md",
        "manifest": output_dir / "phase344_official_catalyst_native_full_depth_strategy_search_precommit_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    families.to_csv(outputs["family_catalog"], index=False)
    grid.to_csv(outputs["grid"], index=False)
    contract.to_csv(outputs["contract"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    outputs["report"].write_text(report, encoding="utf-8")
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "phase": 344,
        "generated_at_utc": generated_utc,
        "phase343_dir": str(phase343_dir),
        "output_dir": str(output_dir),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase344",
            generated_utc=generated_utc,
            inputs={
                "phase343_acceptance": str(phase343_dir / "phase343_acceptance_summary.csv"),
                "phase343_clues": str(phase343_dir / "phase343_diagnostic_clue_ledger.csv"),
            },
            parameters={"annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT, "robust_event_floor": ROBUST_EVENT_FLOOR},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase343-dir", type=Path, default=DEFAULT_PHASE343_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase343_dir, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
