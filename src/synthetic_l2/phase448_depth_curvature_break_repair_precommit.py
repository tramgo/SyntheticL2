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


DEFAULT_PHASE447_DIR = Path("outputs/phase447")
DEFAULT_PHASE409_DIR = Path("outputs/phase409")
DEFAULT_PHASE435_DIR = Path("outputs/phase435")
DEFAULT_PHASE439_DIR = Path("outputs/phase439")
DEFAULT_PHASE298_DIR = Path("outputs/phase298")
DEFAULT_DENSE_ROOT = Path("raw_synthetic_l2_dense_full_year")
DEFAULT_OUTPUT_DIR = Path("outputs/phase448")

THESIS_ID = "P448_DEPTH_CURVATURE_BREAK_REPAIR_PRECOMMIT"
SELECTED_SOURCE_ID = "depth_curvature_break_repair"
NEXT_ACTION = "run_phase449_depth_curvature_break_repair_no_paper_live"
REPAIR_ACTION = "repair_phase448_precommit_inputs"

INITIAL_CAPITAL_INR = 1_000_000.0
ORDER_NOTIONAL_INR = 100_000.0
COST_MULTIPLIER = 2.0


def sha256_frame(frame: pd.DataFrame) -> str:
    return hashlib.sha256(frame.to_csv(index=False, lineterminator="\n").encode("utf-8")).hexdigest()


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def optional_summary(directory: Path, filename: str) -> pd.DataFrame:
    path = directory / filename
    return read_csv(path) if path.exists() else pd.DataFrame()


def build_prior_boundary(phase447: pd.DataFrame, phase409: pd.DataFrame, phase435: pd.DataFrame, phase439: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("P409", "retail_two_sided_market_maker_cancel_latency", scalar(phase409, "phase409_selected_verdict", ""), "closed: cancel-included attachment already executed; no same-family maker rescue"),
        ("P435", "supervised_full_depth_event_ranker", scalar(phase435, "phase435_best_net_pnl_inr", ""), "closed for current evidence: learned ranker had negative validation net P&L and failed breadth/profit gates"),
        ("P439", "low_turnover_full_depth_regime_carry", scalar(phase439, "phase439_selected_verdict", ""), "closed: no gross edge under low-turnover carry"),
        ("P447", "external_catalyst_continuation_stability", scalar(phase447, "phase447_next_best_action", ""), "closed for same-route continuation: frozen chronological holdout failed"),
    ]
    return pd.DataFrame(rows, columns=["phase", "route", "verdict_or_status", "reason_for_not_continuing"])


def build_source_scorecard() -> pd.DataFrame:
    rows = [
        {
            "source_id": SELECTED_SOURCE_ID,
            "material_new_axis": "shape_change_in_depth_levels_2_to_5_curvature_before_short_horizon_break_or_repair",
            "uses_l2_l5_core": 1,
            "non_closed_family": 1,
            "can_execute_next": 1,
            "why_selected": "uses the geometry of liquidity across levels 2-5, not catalyst labels, passive making, supervised ranker selection, low-turnover carry or same threshold rescue",
        },
        {
            "source_id": "rerun_catalyst_continuation_with_new_dates",
            "material_new_axis": "none_without_new_source",
            "uses_l2_l5_core": 1,
            "non_closed_family": 0,
            "can_execute_next": 0,
            "why_selected": "rejected: Phase447 failed the frozen stability holdout",
        },
        {
            "source_id": "market_maker_cancel_latency_again",
            "material_new_axis": "none_without_external_execution_source",
            "uses_l2_l5_core": 1,
            "non_closed_family": 0,
            "can_execute_next": 0,
            "why_selected": "rejected: Phase407-409 already falsified the attached cancel-included charter",
        },
        {
            "source_id": "another_supervised_ranker",
            "material_new_axis": "weak",
            "uses_l2_l5_core": 1,
            "non_closed_family": 0,
            "can_execute_next": 0,
            "why_selected": "rejected: Phase435 ranker failed; a new ranker alone is too close without a different label/source",
        },
    ]
    return pd.DataFrame(rows)


def build_contract(scorecard: pd.DataFrame) -> pd.DataFrame:
    selected_hash = sha256_frame(scorecard[scorecard["source_id"].eq(SELECTED_SOURCE_ID)])
    rows = [
        ("thesis_id", THESIS_ID, "Phase448 selected source precommit."),
        ("selected_source", SELECTED_SOURCE_ID, "Materially new full-depth source for Phase449."),
        ("source_row_hash", selected_hash, "Hash of selected source scorecard row."),
        ("market_hypothesis", "levels_2_to_5_depth_curvature_break_or_repair_precedes_short_horizon_mid_move", "Curvature across deeper visible book can reveal hidden pressure before L1 fully reflects it."),
        ("feature_family", "L2_to_L5_convexity_slope_curvature_asymmetry_repair_rate_and_break_rate", "Full top-five market-by-price depth remains core."),
        ("entry_logic", "taker_entry_after_past_only_curvature_break_or_repair_confirmation", "No passive fill, no maker rebate and no future label access."),
        ("side_rule", "long_when_bid_depth_curvature_repairs_and_ask_curvature_breaks_short_when_opposite", "Side is determined by L2-L5 shape change, not catalyst text or fitted rank."),
        ("sample_policy", "bounded_month_symbol_stride_then_breadth_first_execution", "Execution may start bounded but must report breadth and no acceptance if floors are not met."),
        ("horizon_ticks", "60", "Fixed exit horizon if stop/target not hit."),
        ("stop_bps", "10.0", "Fixed stop."),
        ("take_profit_bps", "16.0", "Fixed target."),
        ("min_event_spacing_ticks", "120", "Avoid overlapping events in the same symbol stream."),
        ("full_depth_required", "L1_to_L5_book_state_with_levels_2_to_5_materiality", "L1-only variants are controls, not the primary."),
        ("controls_required", "l1_only_ablation;side_flip;time_reverse_or_shift;curvature_static_snapshot_without_repair", "Controls must be emitted by Phase449."),
        ("cost_model", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha equity intraday NSE formula."),
        ("capital_policy", f"fixed_initial_capital_{int(INITIAL_CAPITAL_INR)}_inr_order_notional_{int(ORDER_NOTIONAL_INR)}_inr_cost200", "Annualized denominator is fixed capital."),
        ("acceptance_floor", "round_trips_ge_30;dates_ge_5;symbols_ge_3;positive_date_fraction_ge_0p60;annualized_ge_12_cost200", "User profitability bar with breadth."),
        ("forbidden", "catalyst_continuation_rescue;market_maker_rescue;supervised_ranker_retry;low_turnover_carry_retry;promotion;paper_live;deployable_profitability_claim", "Closed boundaries."),
        ("execution_results_generated_now", "0", "Precommit only."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_input_registry(phase298: pd.DataFrame, dense_root: Path) -> pd.DataFrame:
    parquet_count = sum(1 for _ in dense_root.rglob("*.parquet")) if dense_root.exists() else 0
    rows = [
        ("phase298_available", as_int(scalar(phase298, "phase298_raw_dense_sweep_complete", 0)), "Prior raw dense L1-L5 sweep available."),
        ("phase298_dense_root", scalar(phase298, "phase298_dense_root", ""), "Dense lake root recorded by Phase298."),
        ("dense_root_exists", int(dense_root.exists()), "Current dense root exists."),
        ("dense_parquet_file_count", parquet_count, "Current dense Parquet file count."),
        ("levels_2_to_5_required", 1, "Phase448 requires depth beyond L1."),
        ("cost_multiplier", COST_MULTIPLIER, "Cost200 scoring is pinned."),
        ("initial_capital_inr", INITIAL_CAPITAL_INR, "Fixed capital denominator."),
        ("order_notional_inr", ORDER_NOTIONAL_INR, "Fixed notional per order."),
    ]
    return pd.DataFrame(rows, columns=["input_id", "value", "description"])


def input_value(inputs: pd.DataFrame, key: str, default: Any = "") -> Any:
    vals = inputs.loc[inputs["input_id"].eq(key), "value"].tolist()
    return vals[0] if vals else default


def build_gates(prior: pd.DataFrame, scorecard: pd.DataFrame, contract: pd.DataFrame, inputs: pd.DataFrame) -> pd.DataFrame:
    selected = scorecard[scorecard["source_id"].eq(SELECTED_SOURCE_ID)]
    forbidden = contract.loc[contract["contract_id"].eq("forbidden"), "contract_value"].astype(str).str.cat(sep=" ")
    gates = [
        ("P448_PHASE447_AVAILABLE", prior["phase"].eq("P447").any(), "P447 boundary row present", "present"),
        ("P448_PHASE447_REJECTED_OR_NEW_SOURCE_REQUIRED", "precommit_new_source_edge" in prior.loc[prior["phase"].eq("P447"), "verdict_or_status"].astype(str).str.cat(sep=" "), prior.loc[prior["phase"].eq("P447"), "verdict_or_status"].astype(str).str.cat(sep=" "), "new source required"),
        ("P448_SELECTED_SOURCE_PRESENT", len(selected) == 1, len(selected), 1),
        ("P448_SELECTED_SOURCE_USES_L2_L5", int(selected["uses_l2_l5_core"].iloc[0]) == 1 if len(selected) else False, int(selected["uses_l2_l5_core"].iloc[0]) if len(selected) else "", 1),
        ("P448_SELECTED_SOURCE_NOT_CLOSED_FAMILY", int(selected["non_closed_family"].iloc[0]) == 1 if len(selected) else False, int(selected["non_closed_family"].iloc[0]) if len(selected) else "", 1),
        ("P448_PHASE449_EXECUTION_ALLOWED", int(selected["can_execute_next"].iloc[0]) == 1 if len(selected) else False, int(selected["can_execute_next"].iloc[0]) if len(selected) else "", 1),
        ("P448_RAW_DENSE_LAKE_PRESENT", as_int(input_value(inputs, "dense_root_exists", 0)) == 1 and as_int(input_value(inputs, "dense_parquet_file_count", 0)) > 0, f"exists={input_value(inputs, 'dense_root_exists', 0)};files={input_value(inputs, 'dense_parquet_file_count', 0)}", "exists_and_files_gt_0"),
        ("P448_PHASE298_FULL_DEPTH_SOURCE_PRESENT", as_int(input_value(inputs, "phase298_available", 0)) == 1, input_value(inputs, "phase298_available", 0), 1),
        ("P448_COST200_FIXED_CAPITAL_PRECOMMITTED", "cost200" in contract.loc[contract["contract_id"].eq("capital_policy"), "contract_value"].astype(str).str.cat(sep=" "), contract.loc[contract["contract_id"].eq("capital_policy"), "contract_value"].astype(str).str.cat(sep=" "), "cost200_fixed_capital"),
        ("P448_CONTROLS_PRECOMMITTED", "l1_only_ablation" in contract.loc[contract["contract_id"].eq("controls_required"), "contract_value"].astype(str).str.cat(sep=" "), contract.loc[contract["contract_id"].eq("controls_required"), "contract_value"].astype(str).str.cat(sep=" "), "controls"),
        ("P448_RESULTS_NOT_GENERATED", contract.loc[contract["contract_id"].eq("execution_results_generated_now"), "contract_value"].astype(str).str.cat(sep=" ") == "0", contract.loc[contract["contract_id"].eq("execution_results_generated_now"), "contract_value"].astype(str).str.cat(sep=" "), 0),
        ("P448_BOUNDARIES_CLOSED", all(x in forbidden for x in ["promotion", "paper_live", "deployable_profitability_claim"]), forbidden, "closed"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase448_depth_curvature_precommit_complete", 1, "Phase448 source precommit completed"),
            ("phase448_thesis_id", THESIS_ID, "Frozen thesis/source precommit"),
            ("phase448_selected_source_id", SELECTED_SOURCE_ID, "Selected materially new source"),
            ("phase448_execution_results_generated", 0, "Precommit only"),
            ("phase448_strategy_promotion_allowed", 0, "No promotion"),
            ("phase448_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase448_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase448_execution_allowed_next", int(hard_pass == hard_rows), "Whether Phase449 may execute"),
            ("phase448_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase448_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase448_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, prior: pd.DataFrame, scorecard: pd.DataFrame, inputs: pd.DataFrame, contract: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase448 Depth-Curvature Break/Repair Source Precommit",
        "",
        "Phase448 responds to the Phase447 holdout rejection by freezing a genuinely new full-depth L2 source edge before any new result generation.",
        "",
        f"Selected source: `{SELECTED_SOURCE_ID}`.",
        "",
        "The source uses levels 2-5 as the primary information: curvature, slope, asymmetry, break rate and repair rate of visible liquidity beyond the touch.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Prior Evidence Boundary",
        "",
        _markdown_table(prior),
        "",
        "## Source Scorecard",
        "",
        _markdown_table(scorecard),
        "",
        "## Input Registry",
        "",
        _markdown_table(inputs),
        "",
        "## Frozen Phase449 Contract",
        "",
        _markdown_table(contract),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase449 may execute this depth-curvature source only. It may not rescue catalyst continuation, market making, supervised ranker, or low-turnover carry routes.",
    ]
    (output_dir / "phase448_depth_curvature_break_repair_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    phase447_dir: Path = DEFAULT_PHASE447_DIR,
    phase409_dir: Path = DEFAULT_PHASE409_DIR,
    phase435_dir: Path = DEFAULT_PHASE435_DIR,
    phase439_dir: Path = DEFAULT_PHASE439_DIR,
    phase298_dir: Path = DEFAULT_PHASE298_DIR,
    dense_root: Path = DEFAULT_DENSE_ROOT,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase447 = read_csv(phase447_dir / "phase447_acceptance_summary.csv")
    phase409 = optional_summary(phase409_dir, "phase409_acceptance_summary.csv")
    phase435 = optional_summary(phase435_dir, "phase435_acceptance_summary.csv")
    phase439 = optional_summary(phase439_dir, "phase439_acceptance_summary.csv")
    phase298 = read_csv(phase298_dir / "phase298_acceptance_summary.csv")
    if phase447.empty or phase298.empty:
        raise FileNotFoundError("Phase448 requires Phase447 acceptance summary and Phase298 dense source summary.")
    prior = build_prior_boundary(phase447, phase409, phase435, phase439)
    scorecard = build_source_scorecard()
    inputs = build_input_registry(phase298, dense_root)
    contract = build_contract(scorecard)
    gates = build_gates(prior, scorecard, contract, inputs)
    acceptance = build_acceptance(gates)

    prior.to_csv(output_dir / "phase448_prior_evidence_boundary.csv", index=False)
    scorecard.to_csv(output_dir / "phase448_source_scorecard.csv", index=False)
    inputs.to_csv(output_dir / "phase448_input_registry.csv", index=False)
    contract.to_csv(output_dir / "phase448_frozen_phase449_contract.csv", index=False)
    gates.to_csv(output_dir / "phase448_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase448_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, prior, scorecard, inputs, contract, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase448_depth_curvature_break_repair_precommit",
        **reproducibility_fields(
            artifact_id="phase448_depth_curvature_break_repair_precommit",
            generated_utc=generated_utc,
            inputs={
                "phase447_acceptance_summary": str(phase447_dir / "phase447_acceptance_summary.csv"),
                "phase298_acceptance_summary": str(phase298_dir / "phase298_acceptance_summary.csv"),
                "dense_root": str(dense_root),
            },
            parameters={
                "thesis_id": THESIS_ID,
                "selected_source_id": SELECTED_SOURCE_ID,
                "contract_hash": sha256_frame(contract),
            },
            outputs={"acceptance_summary": str(output_dir / "phase448_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase449_fixed_tick_horizon",
        ),
    }
    (output_dir / "phase448_depth_curvature_break_repair_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase448 depth-curvature break/repair precommit.")
    parser.add_argument("--phase447-dir", type=Path, default=DEFAULT_PHASE447_DIR)
    parser.add_argument("--phase409-dir", type=Path, default=DEFAULT_PHASE409_DIR)
    parser.add_argument("--phase435-dir", type=Path, default=DEFAULT_PHASE435_DIR)
    parser.add_argument("--phase439-dir", type=Path, default=DEFAULT_PHASE439_DIR)
    parser.add_argument("--phase298-dir", type=Path, default=DEFAULT_PHASE298_DIR)
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase447_dir, args.phase409_dir, args.phase435_dir, args.phase439_dir, args.phase298_dir, args.dense_root, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
