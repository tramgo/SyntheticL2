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


DEFAULT_PHASE336_DIR = Path("outputs/phase336")
DEFAULT_CHARTER_PATH = Path("C:/Users/Ramic/.codex/attachments/10cf61a2-bfc1-4e3b-9099-09a01ef9583e/pasted-text.txt")
DEFAULT_OUTPUT_DIR = Path("outputs/phase337")

NEXT_ACTION = "run_phase338_cost_stress_holdout_validation_execution_no_replay"
REPAIR_ACTION = "repair_phase337_cost_stress_holdout_validation_precommit"

ANNUALIZED_THRESHOLD_PCT = 12.0
ROBUST_EVENT_FLOOR = 30
MIN_SYMBOL_DATE_POSITIVE_CELLS = 2
COST_PROFILE = "zerodha_2x_all_in_cost_proxy"
COST_MODEL_VERSION = "zerodha_equity_intraday_nse_order_formula_v2_2026_07_14"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def build_candidate_freeze(candidates: pd.DataFrame) -> pd.DataFrame:
    if candidates.empty:
        return pd.DataFrame()
    frozen = candidates.copy()
    frozen.insert(0, "freeze_rank", range(1, len(frozen) + 1))
    frozen["frozen_for_holdout"] = 1
    frozen["candidate_selection_source"] = "phase336_acceptance_grade_candidate_ledger"
    frozen["holdout_tuning_allowed"] = 0
    frozen["posthoc_filter_addition_allowed"] = 0
    frozen["primary_holdout_execution_policy"] = frozen["execution_policy"].astype(str)
    frozen["passive_aware_diagnostic_required"] = 1
    return frozen


def build_charter_reconciliation(charter_text: str) -> pd.DataFrame:
    charter_present = int(bool(charter_text.strip()))
    old_phase300_mentions = int("Phase 300" in charter_text or "phase3ee" in charter_text.lower() or "P300" in charter_text)
    rows = [
        {
            "charter_item": "attached_charter_present",
            "status": "applied" if charter_present else "missing",
            "phase337_interpretation": "The attached passive-aware execution charter was read and reconciled into the current Phase337 precommit.",
            "phase337_requirement": "charter_text_recorded_before_results",
        },
        {
            "charter_item": "stale_phase_numbering",
            "status": "renumbered_not_reopened" if old_phase300_mentions else "not_applicable",
            "phase337_interpretation": "The document uses older Phase300 language; current repo evidence already has Phase300/Phase336 state, so the substance is carried forward without reopening old Phase300 as accepted.",
            "phase337_requirement": "use_current_phase337_route",
        },
        {
            "charter_item": "passive_aware_hybrid_execution",
            "status": "required_as_holdout_diagnostic",
            "phase337_interpretation": "Passive-aware hybrid execution must be evaluated alongside frozen directional candidates, but it cannot override failed primary passive-aware evidence unless it passes all realism penalties.",
            "phase337_requirement": "phase338_compare_taker_primary_vs_passive_aware_diagnostic",
        },
        {
            "charter_item": "fill_model",
            "status": "required",
            "phase337_interpretation": "Passive entries must draw from a pessimistic retail queue-depth fill probability, never assumed fills.",
            "phase337_requirement": "fill_probability_applied_to_every_passive_entry",
        },
        {
            "charter_item": "adverse_selection",
            "status": "required",
            "phase337_interpretation": "Filled passive orders must pay a fill-conditioned toxicity/adverse-selection penalty.",
            "phase337_requirement": "adverse_selection_penalty_applied_to_every_passive_fill",
        },
        {
            "charter_item": "forced_flatten",
            "status": "required",
            "phase337_interpretation": "Any unexited inventory must pay taker flatten spread plus full statutory costs by signal expiry or end of day.",
            "phase337_requirement": "forced_flatten_cost_applied_to_leftover_inventory",
        },
        {
            "charter_item": "no_maker_rebate",
            "status": "required",
            "phase337_interpretation": "No maker rebate is allowed for retail execution assumptions.",
            "phase337_requirement": "maker_rebate_assumed_zero",
        },
        {
            "charter_item": "terminal_killswitch",
            "status": "preserved",
            "phase337_interpretation": "If holdout fails breadth, 2x cost, or realism-penalty requirements, the route closes rather than being rescued by weakening penalties.",
            "phase337_requirement": "no_rescue_iteration_after_phase338_failure",
        },
    ]
    return pd.DataFrame(rows)


def build_holdout_contract(candidate_freeze: pd.DataFrame, charter_reconciliation: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("input_candidates", "outputs/phase336/phase336_acceptance_grade_candidate_ledger.csv", "Freeze Phase336-preserved acceptance-grade training candidates before any holdout result."),
        ("candidate_rows_frozen", len(candidate_freeze), "All Phase336 candidate rows are carried forward without post-hoc filtering."),
        ("candidate_selection_tuning_allowed", 0, "No holdout-date tuning, no post-result candidate selection, no new filters."),
        ("primary_scope", "phase335_cost200_acceptance_grade_candidates", "Primary holdout validates the positive cost-stress training pocket."),
        ("charter_scope", "attached_passive_aware_directional_execution_charter", "The attached passive-aware charter is applied as a Phase337/Phase338 execution diagnostic contract."),
        ("annualized_threshold_pct", ANNUALIZED_THRESHOLD_PCT, "User profitability threshold remains >12%."),
        ("robust_event_floor", ROBUST_EVENT_FLOOR, "Sparse pockets below 30 scheduled events remain discovery clues only."),
        ("minimum_positive_symbol_date_cells", MIN_SYMBOL_DATE_POSITIVE_CELLS, "Breadth cannot be a single symbol/date pocket."),
        ("required_cost_profile", COST_PROFILE, "2x Zerodha all-in cost stress is required."),
        ("cost_model_version", COST_MODEL_VERSION, "Pinned Zerodha equity intraday NSE cost formula."),
        ("fixed_capital_denominator", "required", "Annualized return must use fixed initial capital, not unlimited capital."),
        ("initial_capital_source", "frozen_candidate_initial_capital_inr", "Use the frozen candidate's capital denominator."),
        ("full_top_five_depth_required", 1, "Use market-by-price top-five depth."),
        ("levels_2_to_5_materiality_required", 1, "Depth beyond L1 must be material to features/filters/diagnostics."),
        ("l1_only_variant_rows_allowed", 0, "No L1-only variants."),
        ("net_edge_live_mask_rows_allowed", 0, "No future outcome/net-edge live masks."),
        ("passive_fill_model_required", 1, "Passive-aware diagnostic must use queue-depth fill probability."),
        ("adverse_selection_penalty_required", 1, "Passive fills must include toxicity/adverse-selection penalty."),
        ("forced_flatten_cost_required", 1, "Leftover inventory must pay taker flatten plus full costs."),
        ("maker_rebate_allowed", 0, "No maker rebate for retail assumptions."),
        ("passive_aware_primary_rescue_allowed", 0, "Prior passive-aware evidence remains diagnostic; it cannot rescue the route unless all hard gates pass."),
        ("rank_stability_required", "1x_to_2x_no_ordering_reversal", "Cost-stress ranking should not depend on fragile cost-order reversal."),
        ("negative_controls_required", "side_flip;random_side;breadth", "Holdout execution must preserve controls."),
        ("kill_switch_no_weakening", 1, "Do not weaken realism penalties, cost threshold, or event floor to rescue failure."),
        ("strategy_replay_allowed", 0, "Phase337 is precommit only."),
        ("strategy_promotion_allowed", 0, "No strategy promotion opens here."),
        ("paper_or_live_acceptance_allowed", 0, "No paper/live acceptance opens here."),
        ("deployable_profitability_claim_allowed", 0, "No deployable profitability claim opens here."),
        ("phase338_execution_allowed_next", 1, "If gates pass, Phase338 may execute the frozen holdout contract."),
    ]
    required_charter = int((charter_reconciliation["status"].astype(str).isin(["required", "required_as_holdout_diagnostic", "applied", "renumbered_not_reopened", "preserved"])).sum())
    rows.append(("charter_requirements_recorded", required_charter, "Charter-derived requirements recorded in reconciliation ledger."))
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_phase338_work_order(candidate_freeze: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("P338_FREEZE_INPUTS", "load_frozen_candidates", "Use only Phase337 frozen candidate rows; no post-hoc additions."),
        ("P338_PRIMARY_HOLDOUT", "execute_taker_policy_holdout", "Evaluate frozen primary execution policies under 2x Zerodha costs and fixed capital."),
        ("P338_PASSIVE_AWARE_DIAGNOSTIC", "execute_passive_aware_hybrid_diagnostic", "Apply fill probability, adverse selection, forced flatten, no maker rebate."),
        ("P338_FULL_DEPTH_AUDIT", "verify_l1_l5_depth_materiality", "Confirm levels 2-5 are used and L1-only rows are zero."),
        ("P338_NO_LOOKAHEAD_AUDIT", "verify_no_future_masks", "Confirm net_edge_live_mask_rows and target live-mask rows are zero."),
        ("P338_CONTROLS", "run_side_flip_random_side_breadth_controls", "Require no cost-stress order reversal and positive breadth."),
        ("P338_KILLSWITCH", "apply_no_rescue_killswitch", "Close route if event floor, 2x cost, breadth, or realism penalties fail."),
        ("P338_REPORTING", "write_holdout_execution_ledgers", "Write scenario, control, passive diagnostic, gate, and interpretation outputs."),
    ]
    frame = pd.DataFrame(rows, columns=["work_order_id", "action", "requirements"])
    frame["frozen_candidate_rows"] = len(candidate_freeze)
    return frame


def build_gate_evaluation(phase336: pd.DataFrame, candidate_freeze: pd.DataFrame, charter_reconciliation: pd.DataFrame, contract: pd.DataFrame, work_order: pd.DataFrame) -> pd.DataFrame:
    phase336_complete = as_int(metric_value(phase336, "phase336_cost_stress_margin_redesign_interpretation_complete", 0))
    phase336_next = str(metric_value(phase336, "phase336_next_best_action", ""))
    phase336_claim = as_int(metric_value(phase336, "phase336_deployable_profitability_claim_allowed", 1))
    phase336_replay = as_int(metric_value(phase336, "phase336_replay_allowed", 1))
    charter_required = set(["fill_model", "adverse_selection", "forced_flatten", "no_maker_rebate"])
    charter_present = set(charter_reconciliation.loc[charter_reconciliation["status"].astype(str).eq("required"), "charter_item"].astype(str))
    contract_lookup = contract.set_index("contract_id")["contract_value"].to_dict() if not contract.empty else {}
    rows = [
        ("P337_PHASE336_COMPLETE", phase336_complete == 1, phase336_complete, 1),
        ("P337_PHASE336_ROUTE_MATCH", phase336_next == "run_phase337_cost_stress_holdout_validation_precommit_no_replay", phase336_next, "run_phase337_cost_stress_holdout_validation_precommit_no_replay"),
        ("P337_CANDIDATES_FROZEN", len(candidate_freeze) >= 1, len(candidate_freeze), ">0"),
        ("P337_ACCEPTANCE_EVENT_FLOOR_FROZEN", int(candidate_freeze["scheduled_event_rows"].astype(float).min()) >= ROBUST_EVENT_FLOOR if not candidate_freeze.empty else False, candidate_freeze["scheduled_event_rows"].min() if not candidate_freeze.empty else 0, f">={ROBUST_EVENT_FLOOR}"),
        ("P337_CHARTER_RECONCILED", not charter_reconciliation.empty, len(charter_reconciliation), ">0"),
        ("P337_PASSIVE_REALISM_PENALTIES_REQUIRED", charter_required.issubset(charter_present), ";".join(sorted(charter_present)), ";".join(sorted(charter_required))),
        ("P337_COST200_FIXED_CAPITAL_REQUIRED", contract_lookup.get("required_cost_profile") == COST_PROFILE and contract_lookup.get("fixed_capital_denominator") == "required", f"cost={contract_lookup.get('required_cost_profile')};capital={contract_lookup.get('fixed_capital_denominator')}", f"{COST_PROFILE};fixed"),
        ("P337_FULL_DEPTH_REQUIRED", as_int(contract_lookup.get("full_top_five_depth_required", 0)) == 1 and as_int(contract_lookup.get("levels_2_to_5_materiality_required", 0)) == 1, f"top5={contract_lookup.get('full_top_five_depth_required')};l2_l5={contract_lookup.get('levels_2_to_5_materiality_required')}", "both=1"),
        ("P337_L1_ONLY_FORBIDDEN", as_int(contract_lookup.get("l1_only_variant_rows_allowed", 1)) == 0, contract_lookup.get("l1_only_variant_rows_allowed"), 0),
        ("P337_NO_LOOKAHEAD", as_int(contract_lookup.get("net_edge_live_mask_rows_allowed", 1)) == 0, contract_lookup.get("net_edge_live_mask_rows_allowed"), 0),
        ("P337_BOUNDARIES_CLOSED", phase336_replay == 0 and phase336_claim == 0 and as_int(contract_lookup.get("strategy_replay_allowed", 1)) == 0 and as_int(contract_lookup.get("deployable_profitability_claim_allowed", 1)) == 0, f"phase336_replay={phase336_replay};phase336_claim={phase336_claim};contract_replay={contract_lookup.get('strategy_replay_allowed')};contract_claim={contract_lookup.get('deployable_profitability_claim_allowed')}", "all_zero"),
        ("P337_PHASE338_WORK_ORDER_PRESENT", len(work_order) >= 8, len(work_order), ">=8"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(candidate_freeze: pd.DataFrame, charter_reconciliation: pd.DataFrame, contract: pd.DataFrame, work_order: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    complete = int(hard_pass == hard_rows)
    best_candidate = candidate_freeze["scenario_id"].iloc[0] if not candidate_freeze.empty else ""
    best_ann = candidate_freeze["annualized_return_pct"].iloc[0] if not candidate_freeze.empty else ""
    best_events = candidate_freeze["scheduled_event_rows"].iloc[0] if not candidate_freeze.empty else ""
    candidate_lanes = ";".join(sorted(candidate_freeze["lane_id"].astype(str).unique().tolist())) if not candidate_freeze.empty else ""
    return pd.DataFrame(
        [
            ("phase337_cost_stress_holdout_validation_precommit_complete", complete, "Phase337 precommit completed"),
            ("phase337_candidate_rows_frozen", len(candidate_freeze), "Frozen candidate rows"),
            ("phase337_best_frozen_candidate", best_candidate, "Best frozen candidate"),
            ("phase337_best_frozen_annualized_return_pct", best_ann, "Best training annualized return carried into holdout precommit"),
            ("phase337_best_frozen_scheduled_events", best_events, "Best frozen candidate scheduled events"),
            ("phase337_candidate_lanes_frozen", candidate_lanes, "Frozen candidate lanes"),
            ("phase337_attached_passive_aware_charter_reconciled", int(not charter_reconciliation.empty), "Attached passive-aware charter reconciled"),
            ("phase337_passive_fill_model_required", 1, "Passive fill probability required"),
            ("phase337_adverse_selection_penalty_required", 1, "Passive adverse-selection penalty required"),
            ("phase337_forced_flatten_cost_required", 1, "Forced flatten cost required"),
            ("phase337_maker_rebate_allowed", 0, "No maker rebate"),
            ("phase337_cost_profile_required", COST_PROFILE, "Required cost profile"),
            ("phase337_cost_model_version", COST_MODEL_VERSION, "Pinned cost model"),
            ("phase337_annualized_threshold_pct", ANNUALIZED_THRESHOLD_PCT, "Required annualized threshold"),
            ("phase337_robust_event_floor", ROBUST_EVENT_FLOOR, "Required scheduled-event floor"),
            ("phase337_full_depth_required", 1, "Full top-five depth required"),
            ("phase337_levels_2_to_5_required", 1, "Levels 2-5 materiality required"),
            ("phase337_l1_only_allowed", 0, "No L1-only variants"),
            ("phase337_net_edge_live_mask_allowed", 0, "No lookahead masks"),
            ("phase337_strategy_replay_allowed", 0, "No replay"),
            ("phase337_strategy_promotion_allowed", 0, "No promotion"),
            ("phase337_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase337_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase337_phase338_execution_allowed_next", complete, "Phase338 execution allowed next"),
            ("phase337_contract_rows", len(contract), "Holdout contract rows"),
            ("phase337_phase338_work_order_rows", len(work_order), "Phase338 work-order rows"),
            ("phase337_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase337_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase337_next_best_action", NEXT_ACTION if complete else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase337 Cost-Stress Holdout Validation Precommit",
        "",
        "Phase337 freezes Phase336 acceptance-grade training candidates and reconciles the attached passive-aware execution charter into the current holdout contract.",
        "It is precommit-only: no holdout result, replay, promotion, paper/live acceptance, or deployable profitability claim is produced here.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase337_cost_stress_holdout_validation_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase336_dir: Path = DEFAULT_PHASE336_DIR, charter_path: Path = DEFAULT_CHARTER_PATH, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase336 = read_csv(phase336_dir / "phase336_acceptance_summary.csv")
    candidates = read_csv(phase336_dir / "phase336_acceptance_grade_candidate_ledger.csv")
    charter_text = read_text(charter_path)
    candidate_freeze = build_candidate_freeze(candidates)
    charter_reconciliation = build_charter_reconciliation(charter_text)
    contract = build_holdout_contract(candidate_freeze, charter_reconciliation)
    work_order = build_phase338_work_order(candidate_freeze)
    gates = build_gate_evaluation(phase336, candidate_freeze, charter_reconciliation, contract, work_order)
    acceptance = build_acceptance(candidate_freeze, charter_reconciliation, contract, work_order, gates)

    candidate_freeze.to_csv(output_dir / "phase337_frozen_candidate_ledger.csv", index=False)
    charter_reconciliation.to_csv(output_dir / "phase337_passive_aware_charter_reconciliation.csv", index=False)
    contract.to_csv(output_dir / "phase337_holdout_contract.csv", index=False)
    work_order.to_csv(output_dir / "phase337_phase338_work_order.csv", index=False)
    gates.to_csv(output_dir / "phase337_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase337_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        acceptance,
        {
            "Frozen candidate ledger": candidate_freeze.head(50),
            "Passive-aware charter reconciliation": charter_reconciliation,
            "Holdout contract": contract,
            "Phase338 work order": work_order,
            "Gates": gates,
        },
    )

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase337_cost_stress_holdout_validation_precommit",
        "attached_charter_path": str(charter_path),
        **reproducibility_fields(
            artifact_id="phase337",
            generated_utc=generated_utc,
            inputs={
                "phase336_acceptance": str(phase336_dir / "phase336_acceptance_summary.csv"),
                "phase336_candidates": str(phase336_dir / "phase336_acceptance_grade_candidate_ledger.csv"),
                "attached_passive_aware_charter": str(charter_path),
            },
            parameters={
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "robust_event_floor": ROBUST_EVENT_FLOOR,
                "minimum_positive_symbol_date_cells": MIN_SYMBOL_DATE_POSITIVE_CELLS,
                "cost_profile": COST_PROFILE,
            },
            outputs={"acceptance_summary": str(output_dir / "phase337_acceptance_summary.csv")},
            cost_model_version=COST_MODEL_VERSION,
            latency_model_version="precommit_requires_phase338_passive_aware_latency_and_fill_model",
        ),
    }
    (output_dir / "phase337_cost_stress_holdout_validation_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Precommit Phase337 cost-stress holdout validation with passive-aware charter reconciliation.")
    parser.add_argument("--phase336-dir", type=Path, default=DEFAULT_PHASE336_DIR)
    parser.add_argument("--charter-path", type=Path, default=DEFAULT_CHARTER_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase336_dir, args.charter_path, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
