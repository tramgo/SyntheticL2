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


DEFAULT_PHASE442_DIR = Path("outputs/phase442")
DEFAULT_PHASE441_DIR = Path("outputs/phase441")
DEFAULT_OUTPUT_DIR = Path("outputs/phase443")

THESIS_ID = "P443_EXTERNAL_CATALYST_CONTINUATION_FULL_DEPTH_PRECOMMIT"
SELECTED_SOURCE_ID = "official_catalyst_continuation_with_full_depth_exhaustion_confirmation"
NEXT_ACTION = "run_phase444_external_catalyst_continuation_full_depth_no_paper_live"
REPAIR_ACTION = "repair_phase443_precommit_inputs"

MIN_COMPLETED_ROUND_TRIPS = 30
MIN_TRADE_DATES = 5
MIN_SYMBOLS = 5
MIN_POSITIVE_DATE_FRACTION = 0.60
ANNUALIZED_THRESHOLD_PCT = 12.0
INITIAL_CAPITAL_INR = 1_000_000.0
ORDER_NOTIONAL_INR = 100_000.0
COST_MULTIPLIER = 2.0


def sha256_frame(frame: pd.DataFrame) -> str:
    return hashlib.sha256(frame.to_csv(index=False, lineterminator="\n").encode("utf-8")).hexdigest()


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def build_grid() -> pd.DataFrame:
    rows = []
    for horizon_ticks in [600, 1200, 2400]:
        for depth_confirmation in ["exhaustion", "replenishment_after_exhaustion"]:
            for capacity_events_per_date in [3, 5]:
                rows.append(
                    {
                        "scenario_id": f"P444_catalyst_continuation_H{horizon_ticks}_{depth_confirmation}_C{capacity_events_per_date}",
                        "family_id": "official_catalyst_continuation",
                        "horizon_ticks": horizon_ticks,
                        "depth_confirmation": depth_confirmation,
                        "capacity_events_per_date": capacity_events_per_date,
                        "cost_multiplier": COST_MULTIPLIER,
                        "order_notional_inr": ORDER_NOTIONAL_INR,
                    }
                )
    return pd.DataFrame(rows)


def build_evidence(phase442: pd.DataFrame, controls441: pd.DataFrame) -> pd.DataFrame:
    side = controls441[controls441["control"].astype(str).eq("side_flip")].iloc[0] if not controls441.empty else pd.Series(dtype=object)
    primary = scalar(phase442, "phase442_phase441_best_annualized_return_pct", "")
    return pd.DataFrame(
        [
            ("phase442_next_action", scalar(phase442, "phase442_next_best_action", ""), "Phase442 allowed catalyst continuation/side-flip as a new source."),
            ("phase442_side_flip_new_precommit_allowed", scalar(phase442, "phase442_side_flip_new_precommit_allowed", ""), "Must be one."),
            ("phase441_primary_reversal_annualized_pct", primary, "Rejected reversal baseline."),
            ("phase441_side_flip_annualized_pct", side.get("annualized_return_pct", ""), "Side-flip clue to test as continuation."),
            ("phase441_side_flip_net_pnl_inr", side.get("net_pnl_inr", ""), "Side-flip net P&L clue."),
            ("phase441_side_flip_positive_date_fraction", side.get("positive_date_fraction", ""), "Side-flip positive-date clue."),
        ],
        columns=["evidence_id", "value", "description"],
    )


def build_contract() -> pd.DataFrame:
    rows = [
        ("thesis_id", THESIS_ID, "Catalyst continuation precommit after Phase442 side-flip clue."),
        ("selected_source", SELECTED_SOURCE_ID, "External catalyst continuation with L2-L5 confirmation."),
        ("relationship_to_phase442", "material_new_direction_source_not_reversal_rescue", "Continuation is a new precommitted source, not a same-run rescue."),
        ("direction_policy", "follow_impulse_side_when_full_depth_confirms_exhaustion_or_replenishment_after_exhaustion", "Primary direction is continuation."),
        ("reversal_role", "control_only", "Reversal remains a control, not the primary."),
        ("full_depth_features", "L1_spread_microprice_plus_L2_to_L5_imbalance_depth_slope_replenishment_vacuum", "Top-five depth confirmation required."),
        ("controls_required", "reversal_control;L1_only_ablation;time_shifted_catalyst;capacity_robustness", "Controls must be emitted by Phase444."),
        ("capital_policy", f"fixed_initial_capital_{int(INITIAL_CAPITAL_INR)}_inr_order_notional_{int(ORDER_NOTIONAL_INR)}_inr_cost200", "Annualized denominator fixed."),
        ("acceptance_floor", f"round_trips_ge_{MIN_COMPLETED_ROUND_TRIPS};dates_ge_{MIN_TRADE_DATES};symbols_ge_{MIN_SYMBOLS};positive_date_fraction_ge_{MIN_POSITIVE_DATE_FRACTION};annualized_ge_{ANNUALIZED_THRESHOLD_PCT}", "User profitability floor with breadth."),
        ("forbidden", "same_reversal_rescue;post_result_direction_flip_without_precommit;promotion;paper_live;deployable_profitability_claim", "Closed boundaries."),
        ("execution_results_generated_now", "0", "Precommit only."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_gates(evidence: pd.DataFrame, contract: pd.DataFrame, grid: pd.DataFrame) -> pd.DataFrame:
    values = dict(zip(evidence["evidence_id"], evidence["value"]))
    forbidden = ";".join(contract.loc[contract["contract_id"].eq("forbidden"), "contract_value"].astype(str).tolist())
    gates = [
        ("P443_PHASE442_AVAILABLE", "continuation" in str(values.get("phase442_next_action", "")), values.get("phase442_next_action", ""), "continuation"),
        ("P443_SIDE_FLIP_ALLOWED_BY_PHASE442", as_int(values.get("phase442_side_flip_new_precommit_allowed", 0)) == 1, values.get("phase442_side_flip_new_precommit_allowed", ""), 1),
        ("P443_SIDE_FLIP_CLUE_BETTER_THAN_REVERSAL", float(values.get("phase441_side_flip_annualized_pct", -999) or -999) > float(values.get("phase441_primary_reversal_annualized_pct", 999) or 999), f"side={values.get('phase441_side_flip_annualized_pct','')};primary={values.get('phase441_primary_reversal_annualized_pct','')}", "side>primary"),
        ("P443_MATERIAL_NEW_DIRECTION_SOURCE", True, SELECTED_SOURCE_ID, "continuation_not_reversal_rescue"),
        ("P443_FULL_DEPTH_CONFIRMATION_REQUIRED", contract["contract_value"].astype(str).str.contains("L2_to_L5", regex=False).any(), contract.loc[contract["contract_id"].eq("full_depth_features"), "contract_value"].astype(str).str.cat(sep=" "), "L2-L5"),
        ("P443_GRID_FROZEN", len(grid) == 12, len(grid), 12),
        ("P443_COST200_FIXED_CAPITAL_PINNED", "cost200" in contract.loc[contract["contract_id"].eq("capital_policy"), "contract_value"].astype(str).str.cat(sep=" "), contract.loc[contract["contract_id"].eq("capital_policy"), "contract_value"].astype(str).str.cat(sep=" "), "cost200_fixed_capital"),
        ("P443_CONTROLS_PRECOMMITTED", "reversal_control" in contract.loc[contract["contract_id"].eq("controls_required"), "contract_value"].astype(str).str.cat(sep=" "), contract.loc[contract["contract_id"].eq("controls_required"), "contract_value"].astype(str).str.cat(sep=" "), "controls_present"),
        ("P443_RESULTS_NOT_GENERATED", contract.loc[contract["contract_id"].eq("execution_results_generated_now"), "contract_value"].astype(str).str.cat(sep=" ") == "0", contract.loc[contract["contract_id"].eq("execution_results_generated_now"), "contract_value"].astype(str).str.cat(sep=" "), 0),
        ("P443_BOUNDARIES_CLOSED", all(x in forbidden for x in ["promotion", "paper_live", "deployable_profitability_claim"]), forbidden, "closed"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(grid: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase443_catalyst_continuation_precommit_complete", 1, "Phase443 precommit completed"),
            ("phase443_thesis_id", THESIS_ID, "Frozen thesis"),
            ("phase443_selected_source_id", SELECTED_SOURCE_ID, "Selected continuation source"),
            ("phase443_grid_rows", len(grid), "Frozen Phase444 grid rows"),
            ("phase443_grid_hash", sha256_frame(grid), "Frozen grid hash"),
            ("phase443_execution_results_generated", 0, "Precommit only"),
            ("phase443_strategy_promotion_allowed", 0, "No promotion"),
            ("phase443_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase443_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase443_execution_allowed_next", int(hard_pass == hard_rows), "Whether Phase444 may execute"),
            ("phase443_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase443_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase443_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, evidence: pd.DataFrame, contract: pd.DataFrame, grid: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase443 External Catalyst Continuation Precommit",
        "",
        "Phase443 freezes catalyst continuation/side-flip as a new precommitted source after Phase442 closed the catalyst-reversal form.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Evidence Registry",
        "",
        _markdown_table(evidence),
        "",
        "## Frozen Contract",
        "",
        _markdown_table(contract),
        "",
        "## Frozen Phase444 Grid",
        "",
        _markdown_table(grid),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase444 may execute continuation only as the frozen primary source. Reversal is a control.",
    ]
    (output_dir / "phase443_external_catalyst_continuation_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase442_dir: Path = DEFAULT_PHASE442_DIR, phase441_dir: Path = DEFAULT_PHASE441_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase442 = read_csv(phase442_dir / "phase442_acceptance_summary.csv")
    controls441 = read_csv(phase441_dir / "phase441_best_scenario_controls.csv")
    if phase442.empty or controls441.empty:
        raise FileNotFoundError("Phase443 requires Phase442 acceptance and Phase441 control evidence.")
    evidence = build_evidence(phase442, controls441)
    contract = build_contract()
    grid = build_grid()
    gates = build_gates(evidence, contract, grid)
    acceptance = build_acceptance(grid, gates)
    evidence.to_csv(output_dir / "phase443_evidence_registry.csv", index=False)
    contract.to_csv(output_dir / "phase443_frozen_phase444_contract.csv", index=False)
    grid.to_csv(output_dir / "phase443_catalyst_continuation_scenario_grid.csv", index=False)
    gates.to_csv(output_dir / "phase443_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase443_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, evidence, contract, grid, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase443_external_catalyst_continuation_precommit",
        **reproducibility_fields(
            artifact_id="phase443_external_catalyst_continuation_precommit",
            generated_utc=generated_utc,
            inputs={"phase442_acceptance_summary": str(phase442_dir / "phase442_acceptance_summary.csv")},
            parameters={"thesis_id": THESIS_ID, "selected_source": SELECTED_SOURCE_ID, "grid_hash": sha256_frame(grid)},
            outputs={"acceptance_summary": str(output_dir / "phase443_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase444_external_catalyst_fixed_horizon",
        ),
    }
    (output_dir / "phase443_external_catalyst_continuation_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase443 external catalyst continuation precommit.")
    parser.add_argument("--phase442-dir", type=Path, default=DEFAULT_PHASE442_DIR)
    parser.add_argument("--phase441-dir", type=Path, default=DEFAULT_PHASE441_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase442_dir, args.phase441_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
