from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE409_DIR = Path("outputs/phase409")
DEFAULT_PHASE423_DIR = Path("outputs/phase423")
DEFAULT_PHASE426_DIR = Path("outputs/phase426")
DEFAULT_PHASE433_DIR = Path("outputs/phase433")
DEFAULT_OUTPUT_DIR = Path("outputs/phase434")

THESIS_ID = "P434_SUPERVISED_FULL_DEPTH_EVENT_RANKER_SOURCE_PRECOMMIT"
SELECTED_SOURCE_ID = "supervised_full_depth_event_ranker"
NEXT_ACTION = "run_phase435_supervised_full_depth_event_ranker_no_paper_live"
REPAIR_ACTION = "repair_phase434_source_precommit_inputs"


def sha256_frame(frame: pd.DataFrame) -> str:
    return hashlib.sha256(frame.to_csv(index=False, lineterminator="\n").encode("utf-8")).hexdigest()


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def load_optional(path: Path) -> pd.DataFrame:
    return read_csv(path) if path.exists() else pd.DataFrame()


def build_prior_evidence(phase409: pd.DataFrame, phase423: pd.DataFrame, phase426: pd.DataFrame, phase433: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {
            "phase": "P409",
            "route": "retail_two_sided_market_maker_cancel_latency",
            "verdict_or_status": scalar(phase409, "phase409_selected_verdict", "P409_RETAIL_MARKET_MAKER_CANCEL_RACE_REJECTED_OR_UNAVAILABLE"),
            "reason_for_not_continuing": "attached cancel-included charter line already tested; do not reopen without new external execution source",
        },
        {
            "phase": "P423",
            "route": "pair_spread_convergence",
            "verdict_or_status": scalar(phase423, "phase423_selected_verdict", "P423_PAIR_SPREAD_REALISM_RETEST_REJECTED_OR_CLOSED"),
            "reason_for_not_continuing": "realism retest closed the route; do not repair with same-stack tuning",
        },
        {
            "phase": "P426",
            "route": "queue_depletion_continuation",
            "verdict_or_status": scalar(phase426, "phase426_selected_verdict", "P426_QUEUE_DEPLETION_CONTINUATION_REJECTED_OR_CLOSED"),
            "reason_for_not_continuing": "queue-depletion continuation failed acceptance; broader sweep was already attempted next",
        },
        {
            "phase": "P433",
            "route": "geometry_consistent_full_depth_threshold_family_sweep",
            "verdict_or_status": scalar(phase433, "phase433_selected_verdict", ""),
            "reason_for_not_continuing": "threshold-family sweep produced active but sparse negative cost200 trades; no same-threshold tuning",
        },
    ]
    return pd.DataFrame(rows)


def build_source_scorecard() -> pd.DataFrame:
    rows = [
        {
            "source_id": "supervised_full_depth_event_ranker",
            "material_new_axis": "learned event ranking from full-depth L1-L5 feature vectors and cost-aware forward labels",
            "uses_l2_l5_core": 1,
            "non_threshold_source": 1,
            "can_execute_next": 1,
            "why_selected": "moves away from hand-threshold sweeps; ranks only the best events per symbol/date under fixed cost-aware labels",
        },
        {
            "source_id": "more_same_threshold_sweep",
            "material_new_axis": "none",
            "uses_l2_l5_core": 1,
            "non_threshold_source": 0,
            "can_execute_next": 0,
            "why_selected": "rejected: Phase433 forbids same-threshold family tuning after negative sparse result",
        },
        {
            "source_id": "retail_market_maker_cancel_latency_rescue",
            "material_new_axis": "none_without_new_external_execution_source",
            "uses_l2_l5_core": 1,
            "non_threshold_source": 0,
            "can_execute_next": 0,
            "why_selected": "rejected: attached cancel-included route already ran through Phase407-409 and was falsified",
        },
        {
            "source_id": "fresh_real_l2_download_only",
            "material_new_axis": "data_breadth_without_new_signal_source",
            "uses_l2_l5_core": 1,
            "non_threshold_source": 1,
            "can_execute_next": 0,
            "why_selected": "not selected now: useful later, but low disk space and no frozen new candidate makes it a storage-first detour",
        },
    ]
    return pd.DataFrame(rows)


def build_contract(source_scorecard: pd.DataFrame) -> pd.DataFrame:
    selected_hash = sha256_frame(source_scorecard[source_scorecard["source_id"].eq(SELECTED_SOURCE_ID)])
    rows = [
        ("thesis_id", THESIS_ID, "Phase434 selected source precommit."),
        ("selected_source", SELECTED_SOURCE_ID, "Materially new non-threshold source for Phase435."),
        ("source_row_hash", selected_hash, "Hash of selected source row."),
        ("model_family", "train_only_regularized_event_ranker_logistic_or_tree_baseline", "Phase435 may compare simple rankers but must choose from train-only scoring."),
        ("primary_features", "L1_mid_spread_volume_plus_L2_to_L5_depth_shape_imbalance_slope_pressure_replenishment", "Full top-five book state remains core."),
        ("label_design", "forward_3_ticks_cost_aware_net_bps_and_tradeability_label", "Label must subtract pinned Zerodha cost model before ranking."),
        ("capital_policy", "fixed_initial_capital_1000000_inr_order_notional_100000_inr_cost200", "Annualized return denominator is fixed capital, not unlimited capital."),
        ("selection_policy", "train_only_top_k_event_budget_per_symbol_date_then_validation_execution", "No validation/test threshold tuning."),
        ("controls_required", "l1_only_feature_ablation_side_flip_time_shuffle_real_anchor_cross_check", "Controls must be emitted by Phase435."),
        ("acceptance_floor", "annualized_return_pct_ge_12_cost200_and_event_floor_ge_30_and_positive_date_fraction_ge_0p60", "Profitability threshold remains the user's >12% annualized bar with breadth."),
        ("forbidden", "same_threshold_family_tuning;market_maker_rescue_without_external_execution_source;promotion;paper_live;deployable_profitability_claim", "Closed boundaries."),
        ("execution_results_generated_now", "0", "Phase434 freezes the source only."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_gates(prior: pd.DataFrame, scorecard: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    selected = scorecard[scorecard["source_id"].eq(SELECTED_SOURCE_ID)]
    forbidden = ";".join(contract.loc[contract["contract_id"].eq("forbidden"), "contract_value"].astype(str).tolist())
    gates = [
        ("P434_PHASE433_AVAILABLE", prior["phase"].eq("P433").any(), "P433 evidence row present", "present"),
        ("P434_PHASE433_NEXT_ACTION_MATCHED", "same-threshold tuning" in prior.loc[prior["phase"].eq("P433"), "reason_for_not_continuing"].astype(str).str.cat(sep=" "), prior.loc[prior["phase"].eq("P433"), "reason_for_not_continuing"].astype(str).str.cat(sep=" "), "no same-threshold tuning"),
        ("P434_ATTACHED_CANCEL_CHARTER_RECONCILED", prior["phase"].eq("P409").any(), "P409 cancel-latency evidence row present", "present"),
        ("P434_SELECTED_SOURCE_PRESENT", len(selected) == 1, len(selected), 1),
        ("P434_SELECTED_SOURCE_USES_L2_L5", int(selected["uses_l2_l5_core"].iloc[0]) == 1 if len(selected) else False, int(selected["uses_l2_l5_core"].iloc[0]) if len(selected) else "", 1),
        ("P434_SELECTED_SOURCE_NON_THRESHOLD", int(selected["non_threshold_source"].iloc[0]) == 1 if len(selected) else False, int(selected["non_threshold_source"].iloc[0]) if len(selected) else "", 1),
        ("P434_PHASE435_EXECUTION_ALLOWED", int(selected["can_execute_next"].iloc[0]) == 1 if len(selected) else False, int(selected["can_execute_next"].iloc[0]) if len(selected) else "", 1),
        ("P434_COST200_FIXED_CAPITAL_PRECOMMITTED", contract["contract_value"].astype(str).str.contains("cost200", regex=False).any(), contract.loc[contract["contract_id"].eq("capital_policy"), "contract_value"].astype(str).str.cat(sep=" "), "cost200 fixed capital"),
        ("P434_CONTROLS_PRECOMMITTED", contract["contract_value"].astype(str).str.contains("l1_only_feature_ablation", regex=False).any(), contract.loc[contract["contract_id"].eq("controls_required"), "contract_value"].astype(str).str.cat(sep=" "), "l1/control set"),
        ("P434_RESULTS_NOT_GENERATED", contract.loc[contract["contract_id"].eq("execution_results_generated_now"), "contract_value"].astype(str).str.cat(sep=" ") == "0", contract.loc[contract["contract_id"].eq("execution_results_generated_now"), "contract_value"].astype(str).str.cat(sep=" "), 0),
        ("P434_BOUNDARIES_CLOSED", all(x in forbidden for x in ["promotion", "paper_live", "deployable_profitability_claim"]), forbidden, "closed"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(scorecard: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    selected = scorecard[scorecard["source_id"].eq(SELECTED_SOURCE_ID)]
    return pd.DataFrame(
        [
            ("phase434_strategy_decision_precommit_complete", 1, "Phase434 source decision completed"),
            ("phase434_thesis_id", THESIS_ID, "Frozen thesis/source precommit"),
            ("phase434_selected_source_id", SELECTED_SOURCE_ID, "Selected materially new source"),
            ("phase434_selected_source_uses_l2_l5", int(selected["uses_l2_l5_core"].iloc[0]) if len(selected) else 0, "Selected source uses full top-five depth"),
            ("phase434_selected_source_non_threshold", int(selected["non_threshold_source"].iloc[0]) if len(selected) else 0, "Selected source is not another threshold-family sweep"),
            ("phase434_execution_results_generated", 0, "Precommit only"),
            ("phase434_strategy_promotion_allowed", 0, "No promotion"),
            ("phase434_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase434_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase434_execution_allowed_next", int(hard_pass == hard_rows), "Whether Phase435 may execute"),
            ("phase434_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase434_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase434_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, prior: pd.DataFrame, scorecard: pd.DataFrame, contract: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase434 Strategy Decision and Non-Threshold Source Precommit",
        "",
        "Phase434 responds to Phase433 by choosing the execution path rather than continuing same-threshold full-depth sweeps.",
        "",
        f"Selected source: `{SELECTED_SOURCE_ID}`.",
        "",
        "This is not a profitability result. It is a frozen source decision that allows Phase435 to execute a materially different strategy test: a train-only supervised event ranker using L1-L5 book state and cost-aware forward labels.",
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
        "## Frozen Phase435 Contract",
        "",
        _markdown_table(contract),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase435 may execute the selected supervised full-depth event-ranker source, but may not rescue the same Phase427/431 threshold families or reopen the attached cancel-latency market-maker route without a new external execution source.",
    ]
    (output_dir / "phase434_strategy_decision_and_non_threshold_source_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    phase409_dir: Path = DEFAULT_PHASE409_DIR,
    phase423_dir: Path = DEFAULT_PHASE423_DIR,
    phase426_dir: Path = DEFAULT_PHASE426_DIR,
    phase433_dir: Path = DEFAULT_PHASE433_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase409 = load_optional(phase409_dir / "phase409_acceptance_summary.csv")
    phase423 = load_optional(phase423_dir / "phase423_acceptance_summary.csv")
    phase426 = load_optional(phase426_dir / "phase426_acceptance_summary.csv")
    phase433 = read_csv(phase433_dir / "phase433_acceptance_summary.csv")
    if phase433.empty:
        raise FileNotFoundError("Phase434 requires outputs/phase433/phase433_acceptance_summary.csv")
    prior = build_prior_evidence(phase409, phase423, phase426, phase433)
    scorecard = build_source_scorecard()
    contract = build_contract(scorecard)
    gates = build_gates(prior, scorecard, contract)
    acceptance = build_acceptance(scorecard, gates)
    prior.to_csv(output_dir / "phase434_prior_evidence_boundary.csv", index=False)
    scorecard.to_csv(output_dir / "phase434_source_scorecard.csv", index=False)
    contract.to_csv(output_dir / "phase434_frozen_phase435_contract.csv", index=False)
    gates.to_csv(output_dir / "phase434_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase434_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, prior, scorecard, contract, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase434_strategy_decision_and_non_threshold_source_precommit",
        **reproducibility_fields(
            artifact_id="phase434_strategy_decision_and_non_threshold_source_precommit",
            generated_utc=generated_utc,
            inputs={
                "phase433_acceptance_summary": str(phase433_dir / "phase433_acceptance_summary.csv"),
                "phase409_acceptance_summary": str(phase409_dir / "phase409_acceptance_summary.csv"),
                "phase423_acceptance_summary": str(phase423_dir / "phase423_acceptance_summary.csv"),
                "phase426_acceptance_summary": str(phase426_dir / "phase426_acceptance_summary.csv"),
            },
            parameters={"thesis_id": THESIS_ID, "selected_source_id": SELECTED_SOURCE_ID, "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase434_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase435_precommitted_exact_tick_forward_label",
        ),
    }
    (output_dir / "phase434_strategy_decision_and_non_threshold_source_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase434 strategy decision and non-threshold source precommit.")
    parser.add_argument("--phase409-dir", type=Path, default=DEFAULT_PHASE409_DIR)
    parser.add_argument("--phase423-dir", type=Path, default=DEFAULT_PHASE423_DIR)
    parser.add_argument("--phase426-dir", type=Path, default=DEFAULT_PHASE426_DIR)
    parser.add_argument("--phase433-dir", type=Path, default=DEFAULT_PHASE433_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase409_dir, args.phase423_dir, args.phase426_dir, args.phase433_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
