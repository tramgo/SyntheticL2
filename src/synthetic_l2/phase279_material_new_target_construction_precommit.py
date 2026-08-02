from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase255_richer_raw_depth_feature_quality_interpretation import safe_float
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE277_DIR = Path("outputs/phase277")
DEFAULT_PHASE278_DIR = Path("outputs/phase278")
DEFAULT_OUTPUT_DIR = Path("outputs/phase279")

SELECTED_ROUTE = "P279_MATERIAL_NEW_TARGET_CONSTRUCTION_PRECOMMIT"
NEXT_ACTION = "run_phase280_material_new_target_construction_search_no_paper_live"
REPAIR_ACTION = "repair_phase279_material_new_target_construction_precommit"

ANNUALIZED_THRESHOLD_PCT = 12.0
TARGET_COST_PROFILE = "cost200"

REQUIRED_TARGET_FAMILIES = [
    {
        "target_family_id": "P279_SPREAD_COST_MARGIN_TARGET",
        "target_family": "spread_cost_margin",
        "target_definition": "classify events where observable spread and full-depth pressure imply enough gross edge margin to survive cost200",
        "primary_features": "avg_spread_bps;avg_cum_top5_qty_imbalance;avg_depth_beyond_l1_qty_imbalance;avg_level_weighted_depth_imbalance",
        "preserved_clue_dependency": "P277_SPREAD_LE_Q80;P277_REPLENISH_WITHDRAW_GE_Q90",
    },
    {
        "target_family_id": "P279_ADVERSE_SELECTION_AVOIDANCE_TARGET",
        "target_family": "adverse_selection_avoidance",
        "target_definition": "filter events likely to avoid immediate adverse selection after entry using churn and depth withdrawal pressure",
        "primary_features": "top5_churn_pressure;depth_withdrawal_pressure;depth_replenishment_pressure;avg_depth_beyond_l1_qty_imbalance",
        "preserved_clue_dependency": "P277_CHURN_LE_Q60;P277_CHURN_LE_Q80",
    },
    {
        "target_family_id": "P279_REPLENISHMENT_CONFIRMATION_TARGET",
        "target_family": "depth_replenishment_confirmation",
        "target_definition": "require replenishment dominance to persist as confirmation rather than a one-bar filter",
        "primary_features": "depth_replenish_withdraw_ratio;depth_replenishment_pressure;avg_level_weighted_depth_imbalance",
        "preserved_clue_dependency": "P277_REPLENISH_WITHDRAW_GE_Q90;P277_REPLENISH_CHURN_Q70",
    },
    {
        "target_family_id": "P279_TIME_TO_EXIT_TARGET",
        "target_family": "time_to_exit",
        "target_definition": "vary event exit target and holding horizon to test if the edge exists at a different exit time rather than only at the current horizon",
        "primary_features": "horizon;richer_event_bar_id;avg_spread_bps;depth_replenish_withdraw_ratio",
        "preserved_clue_dependency": "P277_REPLENISH_WITHDRAW_GE_Q90",
    },
    {
        "target_family_id": "P279_NET_EDGE_DISTRIBUTION_SHIFT_TARGET",
        "target_family": "net_edge_distribution_shift",
        "target_definition": "evaluate target construction that improves the distribution tail of net edge under cost200 without using net edge as a live selection feature",
        "primary_features": "full_depth_features_for_selection;net_edge_bps_for_offline_label_only",
        "preserved_clue_dependency": "P277_REPLENISH_WITHDRAW_GE_Q90;P277_SPREAD_LE_Q80;P277_REPLENISH_CHURN_Q70",
    },
]


def parse_contract_value(route: pd.DataFrame, contract_id: str) -> str:
    if route.empty:
        return ""
    rows = route.loc[route["contract_id"].astype(str).eq(contract_id), "contract_value"]
    return "" if rows.empty else str(rows.iloc[0])


def load_inputs(phase277_dir: Path, phase278_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    phase278_summary = read_csv(phase278_dir / "phase278_acceptance_summary.csv")
    phase278_route = read_csv(phase278_dir / "phase278_next_route_contract.csv")
    variant_summary = read_csv(phase277_dir / "phase277_cost_robust_redesign_variant_summary.csv")
    event_universe = read_csv(phase277_dir / "phase277_cost200_redesign_event_universe.csv")
    if phase278_summary.empty:
        raise FileNotFoundError("Missing Phase278 acceptance summary.")
    if phase278_route.empty:
        raise FileNotFoundError("Missing Phase278 next route contract.")
    if variant_summary.empty:
        raise FileNotFoundError("Missing Phase277 variant summary.")
    if event_universe.empty:
        raise FileNotFoundError("Missing Phase277 cost200 redesign event universe.")
    return phase278_summary, phase278_route, variant_summary, event_universe


def build_preserved_clue_catalog(route: pd.DataFrame, variant_summary: pd.DataFrame) -> pd.DataFrame:
    clue_ids = [item.strip() for item in parse_contract_value(route, "P279_PRESERVED_CLUES").split(";") if item.strip()]
    frame = variant_summary[variant_summary["phase277_variant_id"].astype(str).isin(clue_ids)].copy()
    if frame.empty:
        frame = variant_summary.head(5).copy()
    numeric_cols = ["max_annualized_pct", "median_annualized_pct", "cost200_above12_scenario_rows", "uses_top5", "uses_levels_2_to_5", "l1_only_variant"]
    for col in numeric_cols:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
    frame["preserve_as_clue_not_acceptance"] = 1
    frame["eligible_for_phase280_anchor"] = (
        frame["l1_only_variant"].astype(int).eq(0)
        & (frame["max_annualized_pct"] > 0.0)
    ).astype(int)
    cols = [
        "phase277_variant_id",
        "redesign_family",
        "feature_rule",
        "max_annualized_pct",
        "median_annualized_pct",
        "cost200_above12_scenario_rows",
        "uses_top5",
        "uses_levels_2_to_5",
        "l1_only_variant",
        "preserve_as_clue_not_acceptance",
        "eligible_for_phase280_anchor",
    ]
    return frame[[col for col in cols if col in frame.columns]].reset_index(drop=True)


def build_target_family_catalog(clues: pd.DataFrame, event_universe: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    clue_ids = set(clues["phase277_variant_id"].astype(str)) if not clues.empty else set()
    for row in REQUIRED_TARGET_FAMILIES:
        deps = [item for item in row["preserved_clue_dependency"].split(";") if item]
        matched = [item for item in deps if item in clue_ids]
        rows.append(
            {
                **row,
                "matched_preserved_clue_rows": len(matched),
                "matched_preserved_clues": ";".join(matched),
                "cost_profile_required": TARGET_COST_PROFILE,
                "full_depth_required": 1,
                "levels_2_to_5_required": 1,
                "l1_only_allowed": 0,
                "event_universe_rows": len(event_universe),
                "phase280_search_allowed": int(len(event_universe) > 0 and (len(matched) > 0 or row["target_family"] == "time_to_exit")),
            }
        )
    return pd.DataFrame(rows)


def build_control_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("P279_NO_LABEL_LEAKAGE", "net_edge_bps and gross_edge_bps may define offline labels only, not live selection masks", "hard"),
            ("P279_COST200_REQUIRED", "all Phase280 scoring must include cost200 or stronger stress", "hard"),
            ("P279_FULL_DEPTH_REQUIRED", "top-five rows 1-5 and levels 2-5 materiality required", "hard"),
            ("P279_L1_ONLY_FORBIDDEN", "L1-only target families and variants forbidden", "hard"),
            ("P279_NO_PROMOTION", "no strategy replay, promotion, paper/live, or deployable profitability claim", "hard"),
            ("P279_ACCEPTANCE_THRESHOLD", "diagnostic acceptance remains annualized > 12 percent under cost200 with stability evidence", "hard"),
        ],
        columns=["control_id", "control_value", "severity"],
    )


def build_next_route_contract(targets: pd.DataFrame, clues: pd.DataFrame) -> pd.DataFrame:
    allowed_targets = targets[targets["phase280_search_allowed"].astype(int).eq(1)]
    target_ids = ";".join(allowed_targets["target_family_id"].astype(str).tolist())
    clue_ids = ";".join(clues.loc[clues["eligible_for_phase280_anchor"].astype(int).eq(1), "phase277_variant_id"].astype(str).tolist()) if not clues.empty else ""
    return pd.DataFrame(
        [
            ("P280_INPUT", "outputs/phase277/phase277_cost200_redesign_event_universe.csv;outputs/phase279/phase279_target_family_catalog.csv", "Use cost200 event universe and Phase279 target contract."),
            ("P280_TARGET_FAMILIES", target_ids, "Execute materially new target-construction families."),
            ("P280_ANCHOR_CLUES", clue_ids, "Use preserved full-depth clues as anchors, not accepted strategies."),
            ("P280_SEARCH_TYPE", "material_new_target_construction_search", "Execute target-construction search next."),
            ("P280_BOUNDARY", "no_paper_live;no_deployable_profitability_claim;cost200_required;full_depth_required;l1_only_forbidden", "Boundaries remain closed."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def build_gate_evaluation(phase278_summary: pd.DataFrame, route: pd.DataFrame, clues: pd.DataFrame, targets: pd.DataFrame, controls: pd.DataFrame, next_route: pd.DataFrame) -> pd.DataFrame:
    phase278_complete = as_int(metric_value(phase278_summary, "phase278_interpretation_complete", 0))
    phase278_next = str(metric_value(phase278_summary, "phase278_next_best_action", ""))
    close_filter = as_int(metric_value(phase278_summary, "phase278_close_filter_redesign_for_acceptance", 0))
    do_not_relax = as_int(metric_value(phase278_summary, "phase278_do_not_relax_cost_threshold", 0))
    full_depth_targets = bool(not targets.empty and targets["full_depth_required"].astype(int).eq(1).all() and targets["levels_2_to_5_required"].astype(int).eq(1).all())
    l1_forbidden = bool(not targets.empty and targets["l1_only_allowed"].astype(int).eq(0).all())
    rows = [
        ("P279_PHASE278_WORK_ORDER_PRESENT", "run_phase279_material_new_target_construction_precommit" in phase278_next, phase278_next, "Phase278 next action targets Phase279", "hard"),
        ("P279_PHASE278_INTERPRETATION_COMPLETE", phase278_complete == 1, phase278_complete, "Phase278 complete", "hard"),
        ("P279_FILTER_ROUTE_CLOSED", close_filter == 1 and do_not_relax == 1, f"close_filter={close_filter};do_not_relax={do_not_relax}", "filter route closed and cost threshold preserved", "hard"),
        ("P279_ROUTE_CONTRACT_PRESENT", int(route["contract_id"].astype(str).eq("P279_TARGET_CHANGE").sum()) == 1, len(route), "Phase279 route contract present", "hard"),
        ("P279_TARGET_FAMILIES_PRESENT", len(targets) >= 5 and int(targets["phase280_search_allowed"].astype(int).sum()) >= 4, f"targets={len(targets)};allowed={int(targets['phase280_search_allowed'].astype(int).sum())}", ">=5 target families and >=4 allowed", "hard"),
        ("P279_PRESERVED_CLUES_PRESENT", len(clues) > 0 and int(clues["eligible_for_phase280_anchor"].astype(int).sum()) > 0, len(clues), ">0 preserved full-depth clues", "hard"),
        ("P279_FULL_DEPTH_AND_L1_BOUNDARY", full_depth_targets and l1_forbidden, f"full_depth={full_depth_targets};l1_forbidden={l1_forbidden}", "full-depth required and L1-only forbidden", "hard"),
        ("P279_CONTROLS_PRESENT", len(controls) >= 6, len(controls), "control contract present", "hard"),
        ("P279_NEXT_ROUTE_SELECTED", int(next_route["contract_id"].astype(str).eq("P280_SEARCH_TYPE").sum()) == 1, "P280 material target search", "Phase280 route selected", "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def build_acceptance_summary(clues: pd.DataFrame, targets: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    next_action = NEXT_ACTION if hard_pass == len(hard) else REPAIR_ACTION
    rows = [
        ("phase279_target_construction_precommit_complete", 1, "Phase279 material new target-construction precommit completed"),
        ("phase279_selected_route", SELECTED_ROUTE, "Selected route"),
        ("phase279_target_family_rows", len(targets), "Target families defined"),
        ("phase279_phase280_allowed_target_family_rows", int(targets["phase280_search_allowed"].astype(int).sum()) if not targets.empty else 0, "Target families allowed for Phase280 search"),
        ("phase279_preserved_clue_rows", len(clues), "Preserved Phase277 clue rows"),
        ("phase279_phase280_anchor_clue_rows", int(clues["eligible_for_phase280_anchor"].astype(int).sum()) if not clues.empty else 0, "Clues eligible as Phase280 anchors"),
        ("phase279_cost200_required", 1, "Cost200 required"),
        ("phase279_full_depth_required", 1, "Full top-five and levels 2-5 required"),
        ("phase279_l1_only_allowed", 0, "L1-only targets forbidden"),
        ("phase279_strategy_replay_allowed", 0, "No strategy replay unlocked"),
        ("phase279_strategy_promotion_allowed", 0, "No strategy promotion unlocked"),
        ("phase279_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
        ("phase279_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        ("phase279_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase279_hard_gate_rows", len(hard), "Hard gates evaluated"),
        ("phase279_next_best_action", next_action, "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase279 Material New Target-construction Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase279 precommits materially different target construction after Phase278 closed the filter-redesign route for acceptance.",
        "The next executable search must retain cost200, full-depth L2, and no paper/live boundaries.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    phase277_dir: Path = DEFAULT_PHASE277_DIR,
    phase278_dir: Path = DEFAULT_PHASE278_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase278_summary, phase278_route, variant_summary, event_universe = load_inputs(phase277_dir, phase278_dir)
    clues = build_preserved_clue_catalog(phase278_route, variant_summary)
    targets = build_target_family_catalog(clues, event_universe)
    controls = build_control_contract()
    next_route = build_next_route_contract(targets, clues)
    gates = build_gate_evaluation(phase278_summary, phase278_route, clues, targets, controls, next_route)
    acceptance = build_acceptance_summary(clues, targets, gates)

    clues.to_csv(output_dir / "phase279_preserved_clue_catalog.csv", index=False)
    targets.to_csv(output_dir / "phase279_target_family_catalog.csv", index=False)
    controls.to_csv(output_dir / "phase279_control_contract.csv", index=False)
    next_route.to_csv(output_dir / "phase279_next_route_contract.csv", index=False)
    gates.to_csv(output_dir / "phase279_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase279_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase279_material_new_target_construction_precommit_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Preserved Clue Catalog": clues,
            "Target Family Catalog": targets,
            "Control Contract": controls,
            "Next Route Contract": next_route,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase279_material_new_target_construction_precommit",
        **reproducibility_fields(
            artifact_id="phase279",
            generated_utc=generated_utc,
            inputs={
                "phase278_acceptance_summary": str(phase278_dir / "phase278_acceptance_summary.csv"),
                "phase278_next_route_contract": str(phase278_dir / "phase278_next_route_contract.csv"),
                "phase277_cost_robust_redesign_variant_summary": str(phase277_dir / "phase277_cost_robust_redesign_variant_summary.csv"),
                "phase277_cost200_redesign_event_universe": str(phase277_dir / "phase277_cost200_redesign_event_universe.csv"),
            },
            parameters={
                "selected_route": SELECTED_ROUTE,
                "target_cost_profile": TARGET_COST_PROFILE,
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "required_target_families": REQUIRED_TARGET_FAMILIES,
                "strategy_replay_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "preserved_clue_catalog": str(output_dir / "phase279_preserved_clue_catalog.csv"),
                "target_family_catalog": str(output_dir / "phase279_target_family_catalog.csv"),
                "control_contract": str(output_dir / "phase279_control_contract.csv"),
                "next_route_contract": str(output_dir / "phase279_next_route_contract.csv"),
                "gate_evaluation": str(output_dir / "phase279_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase279_acceptance_summary.csv"),
                "report": str(output_dir / "phase279_material_new_target_construction_precommit_report.md"),
                "manifest": str(output_dir / "phase279_material_new_target_construction_precommit_manifest.json"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase279_precommit_only_no_new_replay",
        ),
    }
    (output_dir / "phase279_material_new_target_construction_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase279 material new target-construction precommit.")
    parser.add_argument("--phase277-dir", type=Path, default=DEFAULT_PHASE277_DIR)
    parser.add_argument("--phase278-dir", type=Path, default=DEFAULT_PHASE278_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase277_dir=args.phase277_dir, phase278_dir=args.phase278_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
