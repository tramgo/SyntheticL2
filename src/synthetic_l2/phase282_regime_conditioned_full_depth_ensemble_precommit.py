from __future__ import annotations

import argparse
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


DEFAULT_PHASE281_DIR = Path("outputs/phase281")
DEFAULT_OUTPUT_DIR = Path("outputs/phase282")

SELECTED_ROUTE = "P282_REGIME_CONDITIONED_FULL_DEPTH_ENSEMBLE_PRECOMMIT"
NEXT_ACTION = "run_phase283_regime_conditioned_full_depth_ensemble_search_no_paper_live"
REPAIR_ACTION = "repair_phase282_regime_conditioned_full_depth_ensemble_precommit"

ANNUALIZED_THRESHOLD_PCT = 12.0
TARGET_COST_PROFILE = "cost200"
MIN_EVENTS_FOR_ROBUST_PORTFOLIO_CLAIM = 30
MIN_EVENTS_FOR_SEARCH_DIAGNOSTIC = 8

ENSEMBLE_FAMILIES: list[dict[str, Any]] = [
    {
        "ensemble_family_id": "P282_SPREAD_REPLENISH_ADVERSE_ENSEMBLE",
        "ensemble_family": "spread_replenish_adverse_ensemble",
        "included_target_families": "spread_cost_margin;depth_replenishment_confirmation;adverse_selection_avoidance",
        "ensemble_rule": "combine low-spread, replenishment-confirmed, low-withdrawal/low-churn full-depth clues",
    },
    {
        "ensemble_family_id": "P282_TIME_GATED_REPLENISH_ENSEMBLE",
        "ensemble_family": "time_gated_replenish_ensemble",
        "included_target_families": "time_to_exit;depth_replenishment_confirmation;spread_cost_margin",
        "ensemble_rule": "condition short-exit clues by time-of-day and spread state before fixed-capital scoring",
    },
    {
        "ensemble_family_id": "P282_ADVERSE_AVOID_NET_LABEL_ENSEMBLE",
        "ensemble_family": "adverse_avoid_net_label_ensemble",
        "included_target_families": "adverse_selection_avoidance;net_edge_distribution_shift;spread_cost_margin",
        "ensemble_rule": "use net-edge labels only offline while live masks remain observable full-depth features",
    },
    {
        "ensemble_family_id": "P282_FAMILY_VOTE_ENSEMBLE",
        "ensemble_family": "family_vote_ensemble",
        "included_target_families": "spread_cost_margin;time_to_exit;adverse_selection_avoidance;depth_replenishment_confirmation;net_edge_distribution_shift",
        "ensemble_rule": "require two or more positive full-depth family votes with regime-specific thresholds",
    },
]

REGIME_BUCKETS: list[dict[str, Any]] = [
    {
        "bucket_id": "P282_TIME_OPEN_BUCKET",
        "bucket_type": "time_of_day",
        "bucket_rule": "early/open bucket derived from richer_event_bar_id lower quantiles or available event timestamps",
        "purpose": "test whether near-miss edge is concentrated near the open without assuming a universal all-day effect",
    },
    {
        "bucket_id": "P282_TIME_LATER_BUCKET",
        "bucket_type": "time_of_day",
        "bucket_rule": "later bucket derived from richer_event_bar_id upper quantiles or available event timestamps",
        "purpose": "control for open-only overfitting and identify later-session pockets",
    },
    {
        "bucket_id": "P282_SPREAD_COMPRESSED_BUCKET",
        "bucket_type": "spread_state",
        "bucket_rule": "avg_spread_bps at or below configurable lower/middle quantiles",
        "purpose": "reduce cost hurdle and slippage pressure without lowering the Zerodha cost model",
    },
    {
        "bucket_id": "P282_DEPTH_STABLE_BUCKET",
        "bucket_type": "depth_state",
        "bucket_rule": "low top5 churn and low withdrawal pressure with positive levels 2-5 imbalance",
        "purpose": "distinguish stable liquidity from noisy one-bar depth flickers",
    },
]


def parse_contract_value(route: pd.DataFrame, contract_id: str) -> str:
    if route.empty:
        return ""
    rows = route.loc[route["contract_id"].astype(str).eq(contract_id), "contract_value"]
    return "" if rows.empty else str(rows.iloc[0])


def split_contract_values(value: str) -> list[str]:
    return [item.strip() for item in str(value).split(";") if item.strip()]


def load_inputs(phase281_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    summary = read_csv(phase281_dir / "phase281_acceptance_summary.csv")
    ranked = read_csv(phase281_dir / "phase281_ranked_material_target_interpretation.csv")
    route = read_csv(phase281_dir / "phase281_next_route_contract.csv")
    decisions = read_csv(phase281_dir / "phase281_decision_ledger.csv")
    if summary.empty:
        raise FileNotFoundError("Missing Phase281 acceptance summary.")
    if ranked.empty:
        raise FileNotFoundError("Missing Phase281 ranked interpretation.")
    if route.empty:
        raise FileNotFoundError("Missing Phase281 next route contract.")
    if decisions.empty:
        raise FileNotFoundError("Missing Phase281 decision ledger.")
    return summary, ranked, route, decisions


def build_preserved_clue_catalog(ranked: pd.DataFrame, route: pd.DataFrame) -> pd.DataFrame:
    preserved = set(split_contract_values(parse_contract_value(route, "P282_PRESERVED_CLUES")))
    frame = ranked[ranked["phase280_variant_id"].astype(str).isin(preserved)].copy()
    if frame.empty:
        frame = ranked.head(8).copy()
    numeric_cols = [
        "max_annualized_pct",
        "median_annualized_pct",
        "min_annualized_pct",
        "max_scheduled_event_rows",
        "selected_event_rows",
        "material_full_depth_clue",
        "near_miss_under_12",
        "l1_only_variant",
        "uses_net_edge_as_live_mask",
        "uses_levels_2_to_5",
        "uses_top5",
    ]
    for col in numeric_cols:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
    frame["preserve_as_ensemble_seed_not_acceptance"] = 1
    frame["eligible_for_phase283_search_seed"] = (
        frame["material_full_depth_clue"].astype(int).eq(1)
        & frame["l1_only_variant"].astype(int).eq(0)
        & frame["uses_net_edge_as_live_mask"].astype(int).eq(0)
        & frame["uses_levels_2_to_5"].astype(int).eq(1)
    ).astype(int)
    cols = [
        "phase280_variant_id",
        "target_family_id",
        "target_family",
        "target_rule",
        "max_annualized_pct",
        "median_annualized_pct",
        "max_scheduled_event_rows",
        "selected_event_rows",
        "material_full_depth_clue",
        "near_miss_under_12",
        "uses_top5",
        "uses_levels_2_to_5",
        "l1_only_variant",
        "uses_net_edge_as_offline_label",
        "uses_net_edge_as_live_mask",
        "preserve_as_ensemble_seed_not_acceptance",
        "eligible_for_phase283_search_seed",
    ]
    return frame[[col for col in cols if col in frame.columns]].reset_index(drop=True)


def build_ensemble_family_catalog(clues: pd.DataFrame) -> pd.DataFrame:
    available_families = set(clues["target_family"].astype(str).tolist()) if not clues.empty else set()
    rows: list[dict[str, Any]] = []
    for family in ENSEMBLE_FAMILIES:
        required = split_contract_values(family["included_target_families"])
        matched = [item for item in required if item in available_families]
        rows.append(
            {
                **family,
                "matched_target_family_rows": len(matched),
                "matched_target_families": ";".join(matched),
                "cost_profile_required": TARGET_COST_PROFILE,
                "fixed_capital_required": 1,
                "full_depth_required": 1,
                "levels_2_to_5_required": 1,
                "l1_only_allowed": 0,
                "net_edge_live_mask_allowed": 0,
                "phase283_search_allowed": int(len(matched) >= 2),
            }
        )
    return pd.DataFrame(rows)


def build_regime_bucket_contract() -> pd.DataFrame:
    rows = []
    for bucket in REGIME_BUCKETS:
        rows.append(
            {
                **bucket,
                "full_depth_required": 1,
                "cost_profile_required": TARGET_COST_PROFILE,
                "phase283_search_allowed": 1,
            }
        )
    return pd.DataFrame(rows)


def build_scoring_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("P282_FIXED_CAPITAL_DENOMINATOR", "annualized_return = realized_net_pnl / initial_capital * 100 * 252 / observed_trade_dates", "hard"),
            ("P282_COST200_REQUIRED", "all Phase283 scenarios must use Zerodha cost200 or stronger stress", "hard"),
            ("P282_MIN_EVENT_FLOOR_DIAGNOSTIC", str(MIN_EVENTS_FOR_SEARCH_DIAGNOSTIC), "hard"),
            ("P282_ROBUST_PORTFOLIO_CLAIM_FLOOR", str(MIN_EVENTS_FOR_ROBUST_PORTFOLIO_CLAIM), "hard"),
            ("P282_NO_LABEL_LEAKAGE", "net/gross edge may only define offline diagnostics, never live selection masks", "hard"),
            ("P282_FULL_DEPTH_REQUIRED", "top-five rows 1-5 and levels 2-5/beyond-L1 materiality required", "hard"),
            ("P282_NO_PROMOTION", "no strategy replay, promotion, paper/live acceptance, or deployable profitability claim", "hard"),
        ],
        columns=["scoring_control_id", "scoring_control_value", "severity"],
    )


def build_next_route_contract(clues: pd.DataFrame, ensembles: pd.DataFrame, buckets: pd.DataFrame) -> pd.DataFrame:
    clue_ids = ";".join(clues.loc[clues["eligible_for_phase283_search_seed"].astype(int).eq(1), "phase280_variant_id"].astype(str).tolist()) if not clues.empty else ""
    ensemble_ids = ";".join(ensembles.loc[ensembles["phase283_search_allowed"].astype(int).eq(1), "ensemble_family_id"].astype(str).tolist()) if not ensembles.empty else ""
    bucket_ids = ";".join(buckets["bucket_id"].astype(str).tolist()) if not buckets.empty else ""
    return pd.DataFrame(
        [
            ("P283_INPUTS", "outputs/phase280/phase280_material_target_scenario_results.csv;outputs/phase280/phase280_sample_material_target_scheduled_event_ledger.csv;outputs/phase282/phase282_ensemble_family_catalog.csv;outputs/phase282/phase282_regime_bucket_contract.csv", "Use Phase280 evidence and Phase282 ensemble/regime contracts."),
            ("P283_SEARCH_SEEDS", clue_ids, "Use preserved Phase280 full-depth clues as seeds, not accepted strategies."),
            ("P283_ENSEMBLE_FAMILIES", ensemble_ids, "Execute allowed ensemble families."),
            ("P283_REGIME_BUCKETS", bucket_ids, "Evaluate regime/time/spread/depth buckets."),
            ("P283_SEARCH_TYPE", "regime_conditioned_full_depth_ensemble_search", "Execute the next search milestone."),
            ("P283_BOUNDARY", "no_paper_live;no_deployable_profitability_claim;cost200_required;fixed_capital_required;full_depth_required;l1_only_forbidden;net_edge_live_mask_forbidden", "Boundaries remain closed."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def build_gate_evaluation(summary: pd.DataFrame, route: pd.DataFrame, clues: pd.DataFrame, ensembles: pd.DataFrame, buckets: pd.DataFrame, scoring: pd.DataFrame, next_route: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(summary, "phase281_interpretation_complete", 0))
    next_action = str(metric_value(summary, "phase281_next_best_action", ""))
    close_phase280 = as_int(metric_value(summary, "phase281_close_phase280_for_acceptance", 0))
    do_not_relax = as_int(metric_value(summary, "phase281_do_not_relax_cost_threshold", 0))
    do_not_claim = as_int(metric_value(summary, "phase281_do_not_claim_portfolio_return", 0))
    replay_allowed = as_int(metric_value(summary, "phase281_strategy_replay_allowed", 1))
    paper_allowed = as_int(metric_value(summary, "phase281_paper_or_live_acceptance_allowed", 1))
    claim_allowed = as_int(metric_value(summary, "phase281_deployable_profitability_claim_allowed", 1))
    clue_seeds = int(clues["eligible_for_phase283_search_seed"].astype(int).sum()) if not clues.empty else 0
    ensemble_allowed = int(ensembles["phase283_search_allowed"].astype(int).sum()) if not ensembles.empty else 0
    bucket_allowed = int(buckets["phase283_search_allowed"].astype(int).sum()) if not buckets.empty else 0
    l1_allowed = int(ensembles["l1_only_allowed"].astype(int).sum()) if not ensembles.empty else 1
    live_mask_allowed = int(ensembles["net_edge_live_mask_allowed"].astype(int).sum()) if not ensembles.empty else 1
    rows = [
        ("P282_PHASE281_WORK_ORDER_PRESENT", "run_phase282_regime_conditioned_full_depth_ensemble_precommit" in next_action, next_action, "Phase281 next action targets Phase282", "hard"),
        ("P282_PHASE281_INTERPRETATION_COMPLETE", complete == 1, complete, "Phase281 complete", "hard"),
        ("P282_PHASE280_CLOSED_AND_COST_PRESERVED", close_phase280 == 1 and do_not_relax == 1 and do_not_claim == 1, f"close={close_phase280};do_not_relax={do_not_relax};do_not_claim={do_not_claim}", "Phase280 closed, cost threshold preserved, portfolio claim blocked", "hard"),
        ("P282_ROUTE_CONTRACT_PRESENT", int(route["contract_id"].astype(str).eq("P282_SEARCH_TYPE").sum()) == 1, len(route), "Phase281 route contract present", "hard"),
        ("P282_CLUE_SEEDS_PRESENT", clue_seeds > 0, clue_seeds, ">0 eligible full-depth search seeds", "hard"),
        ("P282_ENSEMBLES_PRESENT", len(ensembles) >= 4 and ensemble_allowed >= 3, f"ensembles={len(ensembles)};allowed={ensemble_allowed}", ">=4 ensembles and >=3 allowed", "hard"),
        ("P282_REGIME_BUCKETS_PRESENT", len(buckets) >= 4 and bucket_allowed >= 4, f"buckets={len(buckets)};allowed={bucket_allowed}", ">=4 regime buckets allowed", "hard"),
        ("P282_SCORING_CONTROLS_PRESENT", len(scoring) >= 7, len(scoring), "scoring controls present", "hard"),
        ("P282_FULL_DEPTH_AND_LEAKAGE_BOUNDARY", l1_allowed == 0 and live_mask_allowed == 0, f"l1_allowed_sum={l1_allowed};live_mask_allowed_sum={live_mask_allowed}", "L1-only and live label masks forbidden", "hard"),
        ("P282_BOUNDARIES_CLOSED", replay_allowed == 0 and paper_allowed == 0 and claim_allowed == 0, f"replay={replay_allowed};paper={paper_allowed};claim={claim_allowed}", "no replay/paper/live/claim", "hard"),
        ("P282_NEXT_ROUTE_SELECTED", int(next_route["contract_id"].astype(str).eq("P283_SEARCH_TYPE").sum()) == 1, "P283 ensemble search", "Phase283 search route selected", "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def build_acceptance_summary(clues: pd.DataFrame, ensembles: pd.DataFrame, buckets: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    next_action = NEXT_ACTION if hard_pass == len(hard) else REPAIR_ACTION
    rows = [
        ("phase282_regime_conditioned_ensemble_precommit_complete", 1, "Phase282 regime-conditioned full-depth ensemble precommit completed"),
        ("phase282_selected_route", SELECTED_ROUTE, "Selected route"),
        ("phase282_preserved_clue_rows", len(clues), "Preserved Phase281 clue rows"),
        ("phase282_phase283_search_seed_rows", int(clues["eligible_for_phase283_search_seed"].astype(int).sum()) if not clues.empty else 0, "Eligible Phase283 search seeds"),
        ("phase282_ensemble_family_rows", len(ensembles), "Ensemble families defined"),
        ("phase282_phase283_allowed_ensemble_rows", int(ensembles["phase283_search_allowed"].astype(int).sum()) if not ensembles.empty else 0, "Ensemble families allowed for Phase283"),
        ("phase282_regime_bucket_rows", len(buckets), "Regime/time/spread/depth buckets defined"),
        ("phase282_min_event_floor_diagnostic", MIN_EVENTS_FOR_SEARCH_DIAGNOSTIC, "Minimum scheduled-event floor for sparse diagnostic ranking"),
        ("phase282_min_events_for_robust_portfolio_claim", MIN_EVENTS_FOR_ROBUST_PORTFOLIO_CLAIM, "Minimum scheduled-event floor for robust portfolio-return claim"),
        ("phase282_cost200_required", 1, "Cost200 required"),
        ("phase282_fixed_capital_required", 1, "Fixed-capital denominator required"),
        ("phase282_full_depth_required", 1, "Full top-five and levels 2-5 required"),
        ("phase282_l1_only_allowed", 0, "L1-only ensembles forbidden"),
        ("phase282_net_edge_live_mask_allowed", 0, "Net/gross edge live masks forbidden"),
        ("phase282_strategy_replay_allowed", 0, "No strategy replay unlocked"),
        ("phase282_strategy_promotion_allowed", 0, "No strategy promotion unlocked"),
        ("phase282_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
        ("phase282_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        ("phase282_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase282_hard_gate_rows", len(hard), "Hard gates evaluated"),
        ("phase282_next_best_action", next_action, "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase282 Regime-conditioned Full-depth Ensemble Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase282 precommits a broader regime-conditioned full-depth ensemble search after Phase281 closed Phase280 for acceptance.",
        "The next executable search must keep cost200, fixed-capital annualization, full-depth L2, event floors, and no paper/live boundaries.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase281_dir: Path = DEFAULT_PHASE281_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary, ranked, route, decisions = load_inputs(phase281_dir)
    clues = build_preserved_clue_catalog(ranked, route)
    ensembles = build_ensemble_family_catalog(clues)
    buckets = build_regime_bucket_contract()
    scoring = build_scoring_contract()
    next_route = build_next_route_contract(clues, ensembles, buckets)
    gates = build_gate_evaluation(summary, route, clues, ensembles, buckets, scoring, next_route)
    acceptance = build_acceptance_summary(clues, ensembles, buckets, gates)

    clues.to_csv(output_dir / "phase282_preserved_clue_catalog.csv", index=False)
    ensembles.to_csv(output_dir / "phase282_ensemble_family_catalog.csv", index=False)
    buckets.to_csv(output_dir / "phase282_regime_bucket_contract.csv", index=False)
    scoring.to_csv(output_dir / "phase282_scoring_control_contract.csv", index=False)
    next_route.to_csv(output_dir / "phase282_next_route_contract.csv", index=False)
    gates.to_csv(output_dir / "phase282_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase282_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase282_regime_conditioned_full_depth_ensemble_precommit_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Preserved Clue Catalog": clues,
            "Ensemble Family Catalog": ensembles,
            "Regime Bucket Contract": buckets,
            "Scoring Control Contract": scoring,
            "Next Route Contract": next_route,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase282_regime_conditioned_full_depth_ensemble_precommit",
        **reproducibility_fields(
            artifact_id="phase282",
            generated_utc=generated_utc,
            inputs={
                "phase281_acceptance_summary": str(phase281_dir / "phase281_acceptance_summary.csv"),
                "phase281_ranked_material_target_interpretation": str(phase281_dir / "phase281_ranked_material_target_interpretation.csv"),
                "phase281_next_route_contract": str(phase281_dir / "phase281_next_route_contract.csv"),
                "phase281_decision_ledger": str(phase281_dir / "phase281_decision_ledger.csv"),
            },
            parameters={
                "selected_route": SELECTED_ROUTE,
                "target_cost_profile": TARGET_COST_PROFILE,
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "min_events_for_search_diagnostic": MIN_EVENTS_FOR_SEARCH_DIAGNOSTIC,
                "min_events_for_robust_portfolio_claim": MIN_EVENTS_FOR_ROBUST_PORTFOLIO_CLAIM,
                "ensemble_families": ENSEMBLE_FAMILIES,
                "regime_buckets": REGIME_BUCKETS,
                "strategy_replay_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "preserved_clue_catalog": str(output_dir / "phase282_preserved_clue_catalog.csv"),
                "ensemble_family_catalog": str(output_dir / "phase282_ensemble_family_catalog.csv"),
                "regime_bucket_contract": str(output_dir / "phase282_regime_bucket_contract.csv"),
                "scoring_control_contract": str(output_dir / "phase282_scoring_control_contract.csv"),
                "next_route_contract": str(output_dir / "phase282_next_route_contract.csv"),
                "gate_evaluation": str(output_dir / "phase282_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase282_acceptance_summary.csv"),
                "report": str(output_dir / "phase282_regime_conditioned_full_depth_ensemble_precommit_report.md"),
                "manifest": str(output_dir / "phase282_regime_conditioned_full_depth_ensemble_precommit_manifest.json"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase282_precommit_only_no_new_replay",
        ),
    }
    (output_dir / "phase282_regime_conditioned_full_depth_ensemble_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase282 regime-conditioned full-depth ensemble precommit.")
    parser.add_argument("--phase281-dir", type=Path, default=DEFAULT_PHASE281_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase281_dir=args.phase281_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
