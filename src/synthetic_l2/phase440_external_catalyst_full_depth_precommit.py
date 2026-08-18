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


DEFAULT_PHASE387_DIR = Path("outputs/phase387")
DEFAULT_PHASE393_DIR = Path("outputs/phase393")
DEFAULT_PHASE439_DIR = Path("outputs/phase439")
DEFAULT_OUTPUT_DIR = Path("outputs/phase440")

THESIS_ID = "P440_EXTERNAL_CATALYST_FULL_DEPTH_CONFIRMATION_PRECOMMIT"
SELECTED_SOURCE_ID = "official_catalyst_reversal_with_full_depth_confirmation"
NEXT_ACTION = "run_phase441_external_catalyst_full_depth_confirmation_no_paper_live"
REPAIR_ACTION = "repair_phase440_precommit_inputs"

MIN_CANDIDATE_EVENTS_BEFORE_REPLAY = 30
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


def build_evidence(phase387: pd.DataFrame, phase393: pd.DataFrame, phase439: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("phase439_boundary", scalar(phase439, "phase439_next_best_action", ""), "Latest plan boundary requires external alpha source or pause."),
            ("phase387_primary_annualized_return_pct", scalar(phase387, "phase387_primary_annualized_return_pct", ""), "Prior official-catalyst real-L2 clue exceeded 12 percent but was sparse."),
            ("phase387_primary_selected_trade_rows", scalar(phase387, "phase387_primary_selected_trade_rows", ""), "Prior selected trades were below the event floor."),
            ("phase387_primary_diagnostic_dates", scalar(phase387, "phase387_primary_diagnostic_dates", ""), "Prior clue had useful date breadth."),
            ("phase387_primary_symbols", scalar(phase387, "phase387_primary_symbols", ""), "Prior clue had useful symbol breadth."),
            ("phase387_primary_acceptance_candidate", scalar(phase387, "phase387_primary_acceptance_candidate", ""), "Prior clue was not accepted."),
            ("phase393_full_universe_local_after", scalar(phase393, "phase393_local_full_universe_after", ""), "Local full-universe day available from prior Azure download milestone."),
            ("phase393_strategy_retest_executed_now", scalar(phase393, "phase393_strategy_retest_executed_now", ""), "Phase393 downloaded/verified data but did not retest."),
        ],
        columns=["evidence_id", "value", "description"],
    )


def build_contract() -> pd.DataFrame:
    rows = [
        ("thesis_id", THESIS_ID, "External-alpha precommit after L2-only routes failed."),
        ("selected_source", SELECTED_SOURCE_ID, "Official/external catalyst provides direction context; L1-L5 depth confirms tradability."),
        ("external_alpha_axis", "official_catalyst_calendar_and_context_from_local_phase387_phase393_artifacts", "Not another L2-only source."),
        ("l2_role", "confirmation_filter_and_slippage_context_not_primary_alpha", "Full-depth remains core but does not invent direction alone."),
        ("primary_candidate", "phase387_reversal_control_positive_sparse_clue", "Use as clue only, not accepted result."),
        ("event_floor_repair", f"require_candidate_events_before_replay_ge_{MIN_CANDIDATE_EVENTS_BEFORE_REPLAY}", "Do not replay a sparse event set as acceptance."),
        ("direction_policy", "pre_event_or_post_event_reversal_only_when_depth_confirms_exhaustion", "Frozen source family."),
        ("full_depth_features", "L1_spread_microprice_plus_L2_to_L5_imbalance_depth_slope_replenishment_vacuum", "Top-five depth confirmation required."),
        ("controls_required", "non_catalyst_date_control;side_flip;time_shifted_catalyst;L1_only_ablation;real_anchor_holdout", "External-alpha controls required."),
        ("capital_policy", f"fixed_initial_capital_{int(INITIAL_CAPITAL_INR)}_inr_order_notional_{int(ORDER_NOTIONAL_INR)}_inr_cost200", "Annualized denominator fixed."),
        ("acceptance_floor", f"round_trips_ge_{MIN_COMPLETED_ROUND_TRIPS};dates_ge_{MIN_TRADE_DATES};symbols_ge_{MIN_SYMBOLS};positive_date_fraction_ge_{MIN_POSITIVE_DATE_FRACTION};annualized_ge_{ANNUALIZED_THRESHOLD_PCT}", "User profitability floor with breadth."),
        ("forbidden", "same_l2_only_timing_variant;same_phase435_ranker_rescue;same_phase438_regime_rescue;promotion;paper_live;deployable_profitability_claim", "Closed boundaries."),
        ("execution_results_generated_now", "0", "Precommit only."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_phase441_grid() -> pd.DataFrame:
    rows = []
    for horizon_ticks in [600, 1200, 2400]:
        for depth_confirmation in ["exhaustion", "replenishment_after_exhaustion"]:
            for capacity_events_per_date in [3, 5]:
                rows.append(
                    {
                        "scenario_id": f"P441_catalyst_reversal_H{horizon_ticks}_{depth_confirmation}_C{capacity_events_per_date}",
                        "family_id": "official_catalyst_reversal",
                        "horizon_ticks": horizon_ticks,
                        "depth_confirmation": depth_confirmation,
                        "capacity_events_per_date": capacity_events_per_date,
                        "cost_multiplier": COST_MULTIPLIER,
                        "order_notional_inr": ORDER_NOTIONAL_INR,
                    }
                )
    return pd.DataFrame(rows)


def build_gates(evidence: pd.DataFrame, contract: pd.DataFrame, grid: pd.DataFrame) -> pd.DataFrame:
    values = dict(zip(evidence["evidence_id"], evidence["value"]))
    forbidden = ";".join(contract.loc[contract["contract_id"].eq("forbidden"), "contract_value"].astype(str).tolist())
    external_axis = contract.loc[contract["contract_id"].eq("external_alpha_axis"), "contract_value"].astype(str).str.cat(sep=" ")
    gates = [
        ("P440_PHASE439_AVAILABLE", "external_alpha_source" in str(values.get("phase439_boundary", "")), values.get("phase439_boundary", ""), "external_alpha_source"),
        ("P440_PRIOR_POSITIVE_SPARSE_CLUE_PRESENT", float(values.get("phase387_primary_annualized_return_pct", 0) or 0) >= ANNUALIZED_THRESHOLD_PCT, values.get("phase387_primary_annualized_return_pct", ""), f">={ANNUALIZED_THRESHOLD_PCT}"),
        ("P440_PRIOR_CLUE_NOT_ACCEPTED", as_int(values.get("phase387_primary_acceptance_candidate", 1)) == 0, values.get("phase387_primary_acceptance_candidate", ""), 0),
        ("P440_EVENT_FLOOR_REPAIR_REQUIRED", as_int(values.get("phase387_primary_selected_trade_rows", 0)) < MIN_COMPLETED_ROUND_TRIPS, values.get("phase387_primary_selected_trade_rows", ""), f"<{MIN_COMPLETED_ROUND_TRIPS}_prior_sparse"),
        ("P440_EXTERNAL_ALPHA_AXIS_PRESENT", "official_catalyst" in external_axis, external_axis, "official_catalyst"),
        ("P440_FULL_DEPTH_CONFIRMATION_REQUIRED", contract["contract_value"].astype(str).str.contains("L2_to_L5", regex=False).any(), contract.loc[contract["contract_id"].eq("full_depth_features"), "contract_value"].astype(str).str.cat(sep=" "), "L2-L5"),
        ("P440_GRID_FROZEN", len(grid) == 12, len(grid), 12),
        ("P440_COST200_FIXED_CAPITAL_PINNED", "cost200" in contract.loc[contract["contract_id"].eq("capital_policy"), "contract_value"].astype(str).str.cat(sep=" "), contract.loc[contract["contract_id"].eq("capital_policy"), "contract_value"].astype(str).str.cat(sep=" "), "cost200_fixed_capital"),
        ("P440_CONTROLS_PRECOMMITTED", "non_catalyst_date_control" in contract.loc[contract["contract_id"].eq("controls_required"), "contract_value"].astype(str).str.cat(sep=" "), contract.loc[contract["contract_id"].eq("controls_required"), "contract_value"].astype(str).str.cat(sep=" "), "external_controls"),
        ("P440_RESULTS_NOT_GENERATED", contract.loc[contract["contract_id"].eq("execution_results_generated_now"), "contract_value"].astype(str).str.cat(sep=" ") == "0", contract.loc[contract["contract_id"].eq("execution_results_generated_now"), "contract_value"].astype(str).str.cat(sep=" "), 0),
        ("P440_BOUNDARIES_CLOSED", all(x in forbidden for x in ["promotion", "paper_live", "deployable_profitability_claim"]), forbidden, "closed"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(grid: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase440_external_catalyst_precommit_complete", 1, "Phase440 precommit completed"),
            ("phase440_thesis_id", THESIS_ID, "Frozen thesis"),
            ("phase440_selected_source_id", SELECTED_SOURCE_ID, "Selected external-alpha source"),
            ("phase440_grid_rows", len(grid), "Frozen Phase441 scenario rows"),
            ("phase440_grid_hash", sha256_frame(grid), "Hash of frozen grid"),
            ("phase440_execution_results_generated", 0, "Precommit only"),
            ("phase440_strategy_promotion_allowed", 0, "No promotion"),
            ("phase440_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase440_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase440_execution_allowed_next", int(hard_pass == hard_rows), "Whether Phase441 may execute"),
            ("phase440_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase440_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase440_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, evidence: pd.DataFrame, contract: pd.DataFrame, grid: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase440 External Catalyst Full-Depth Confirmation Precommit",
        "",
        "Phase440 responds to Phase439 by selecting an external-alpha source instead of another L2-only timing or threshold variant.",
        "",
        "The source uses official/local catalyst evidence as the alpha axis and full L1-L5 depth as the confirmation and execution-quality layer.",
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
        "## Frozen Phase441 Grid",
        "",
        _markdown_table(grid),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase440 does not accept the prior sparse positive clue. Phase441 may execute only the frozen external-catalyst plus full-depth confirmation source, with controls and no paper/live path.",
    ]
    (output_dir / "phase440_external_catalyst_full_depth_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase387_dir: Path = DEFAULT_PHASE387_DIR, phase393_dir: Path = DEFAULT_PHASE393_DIR, phase439_dir: Path = DEFAULT_PHASE439_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase387 = read_csv(phase387_dir / "phase387_acceptance_summary.csv")
    phase393 = read_csv(phase393_dir / "phase393_acceptance_summary.csv")
    phase439 = read_csv(phase439_dir / "phase439_acceptance_summary.csv")
    if phase387.empty or phase439.empty:
        raise FileNotFoundError("Phase440 requires Phase387 clue evidence and Phase439 boundary evidence.")
    evidence = build_evidence(phase387, phase393, phase439)
    contract = build_contract()
    grid = build_phase441_grid()
    gates = build_gates(evidence, contract, grid)
    acceptance = build_acceptance(grid, gates)
    evidence.to_csv(output_dir / "phase440_evidence_registry.csv", index=False)
    contract.to_csv(output_dir / "phase440_frozen_phase441_contract.csv", index=False)
    grid.to_csv(output_dir / "phase440_external_catalyst_scenario_grid.csv", index=False)
    gates.to_csv(output_dir / "phase440_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase440_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, evidence, contract, grid, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase440_external_catalyst_full_depth_precommit",
        **reproducibility_fields(
            artifact_id="phase440_external_catalyst_full_depth_precommit",
            generated_utc=generated_utc,
            inputs={
                "phase387_acceptance_summary": str(phase387_dir / "phase387_acceptance_summary.csv"),
                "phase439_acceptance_summary": str(phase439_dir / "phase439_acceptance_summary.csv"),
            },
            parameters={"thesis_id": THESIS_ID, "selected_source": SELECTED_SOURCE_ID, "grid_hash": sha256_frame(grid)},
            outputs={"acceptance_summary": str(output_dir / "phase440_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase441_external_catalyst_fixed_horizon",
        ),
    }
    (output_dir / "phase440_external_catalyst_full_depth_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase440 external catalyst full-depth precommit.")
    parser.add_argument("--phase387-dir", type=Path, default=DEFAULT_PHASE387_DIR)
    parser.add_argument("--phase393-dir", type=Path, default=DEFAULT_PHASE393_DIR)
    parser.add_argument("--phase439-dir", type=Path, default=DEFAULT_PHASE439_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase387_dir, args.phase393_dir, args.phase439_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
