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


DEFAULT_PHASE323_DIR = Path("outputs/phase323")
DEFAULT_PHASE315_DIR = Path("outputs/phase315")
DEFAULT_OUTPUT_DIR = Path("outputs/phase324")

NEXT_ACTION = "run_phase325_event_catalyst_breadth_expansion_materialization_no_replay"
REPAIR_ACTION = "repair_phase324_event_catalyst_breadth_expansion_precommit"

TARGET_EVENT_ROWS = 50
MIN_EVENT_ROWS = 40
ROBUST_EVENT_FLOOR = 30
MIN_SYMBOLS_PER_EVENT = 32
PRE_EVENT_SECONDS = 900
POST_EVENT_SECONDS = 1800


def build_expansion_contract(phase323: pd.DataFrame) -> pd.DataFrame:
    preserved_family = metric_value(phase323, "phase323_best_family_preserved_for_breadth_expansion", "P321_DEPTH_ACCEL_REVERSAL")
    rows = [
        ("selected_route", "P324_EVENT_CATALYST_BREADTH_EXPANSION_PRECOMMIT", "Expand the event-catalyst universe before further acceptance decisions."),
        ("preserved_strategy_family", preserved_family, "Carry forward the Phase323 best full-depth clue."),
        ("target_event_rows", TARGET_EVENT_ROWS, "Preferred total synthetic catalyst events for Phase325."),
        ("minimum_event_rows", MIN_EVENT_ROWS, "Minimum total synthetic catalyst events before Phase326 join/materialization."),
        ("robust_event_floor", ROBUST_EVENT_FLOOR, "Acceptance floor that Phase322 could not satisfy."),
        ("minimum_symbols_per_event", MIN_SYMBOLS_PER_EVENT, "Preserve full 32-symbol universe per event."),
        ("window_seconds", f"pre={PRE_EVENT_SECONDS};post={POST_EVENT_SECONDS}", "Use the same event-relative window as Phase317/320."),
        ("source_root", "raw_synthetic_l2_dense_full_year", "Use the existing full-year dense top-five book-state source."),
        ("candidate_selection", "row_level_dense_buckets_distinct_dates", "Avoid row-group midpoint false positives; use dense row-level buckets."),
        ("full_depth_required", "depth_levels_1_to_5", "Preserve top-five market-by-price depth."),
        ("depth_beyond_l1_required", "depth_levels_2_to_5_material", "No L1-only candidate path."),
        ("cost_model_preserved", "zerodha_equity_intraday_nse_order_formula_v2_2026_07_14", "Future search must keep documented Zerodha costs."),
        ("fixed_capital_required", "required", "No unlimited-capital annualized return."),
        ("cost200_required", "required", "Keep 2x cost-stress scoring."),
        ("target_live_separation", "required", "target_ fields stay outcomes, not live signals."),
        ("net_edge_live_mask", "forbidden", "No lookahead live mask."),
        ("phase324_execution_now", "precommit_only", "Do not materialize new joins in Phase324."),
        ("boundaries", "replay=0;promotion=0;paper=0;claim=0", "No boundary change."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_phase325_work_order() -> pd.DataFrame:
    rows = [
        ("discover_dense_source_inventory", "raw_synthetic_l2_dense_full_year/trade_month=*/symbol=*/part-*.parquet", "Inventory available synthetic top-five depth files."),
        ("select_row_level_dense_buckets", "reference_symbol=HDFCBANK; distinct_event_dates; target=50; minimum=40", "Select actual dense row-level windows, not only file metadata."),
        ("validate_symbol_coverage", f"symbols_per_event>={MIN_SYMBOLS_PER_EVENT}", "Reject events missing full symbol breadth."),
        ("write_expanded_event_ledger", "event_sources/event_catalysts/generated/phase325_expanded_synthetic_events.csv", "Materialize expanded event ledger."),
        ("write_expanded_work_order", "outputs/phase325/phase325_event_symbol_work_order.csv", "Create event-symbol join work order."),
        ("preserve_phase323_family_seed", "P321_DEPTH_ACCEL_REVERSAL", "Carry preserved strategy clue into later search, without optimizing on future labels."),
        ("run_quality_gates", "event_rows>=40;symbols=32;depth=top5;no_replay", "Gate Phase325 before any join/search."),
        ("next_join_precommit", "run_phase326_event_catalyst_expanded_top5_depth_join_precommit_no_replay", "Prepare expanded top-five-depth join after breadth is materialized."),
    ]
    return pd.DataFrame(rows, columns=["work_order_id", "scope", "description"])


def build_gate_evaluation(phase323: pd.DataFrame, phase315: pd.DataFrame, contract: pd.DataFrame, work_order: pd.DataFrame) -> pd.DataFrame:
    phase323_complete = as_int(metric_value(phase323, "phase323_multievent_strategy_search_interpretation_complete", 0))
    current_events = as_int(metric_value(phase315, "phase315_generated_event_rows", 0))
    research_leads = as_int(metric_value(phase323, "phase323_fixed_capital_profitable_research_leads_exist", 0))
    acceptance_candidates = as_int(metric_value(phase323, "phase323_acceptance_grade_candidates_exist", 0))
    rows = [
        ("P324_PHASE323_COMPLETE", phase323_complete == 1, phase323_complete, 1),
        ("P324_RESEARCH_LEAD_PRESENT", research_leads == 1, research_leads, 1),
        ("P324_ACCEPTANCE_NOT_ALREADY_OPEN", acceptance_candidates == 0, acceptance_candidates, 0),
        ("P324_CURRENT_BREADTH_BELOW_FLOOR", current_events < ROBUST_EVENT_FLOOR, current_events, f"<{ROBUST_EVENT_FLOOR}"),
        ("P324_EXPANDED_BREADTH_TARGET_EXCEEDS_FLOOR", MIN_EVENT_ROWS >= ROBUST_EVENT_FLOOR, MIN_EVENT_ROWS, f">={ROBUST_EVENT_FLOOR}"),
        ("P324_CONTRACT_ROWS_PRESENT", len(contract) >= 18, len(contract), ">=18"),
        ("P324_WORK_ORDER_ROWS_PRESENT", len(work_order) >= 8, len(work_order), ">=8"),
        ("P324_DEPTH_AND_COST_BOUNDARIES_PRESENT", {"full_depth_required", "depth_beyond_l1_required", "cost_model_preserved", "fixed_capital_required", "cost200_required"}.issubset(set(contract["contract_id"].astype(str))), "present", "present"),
        ("P324_NO_REPLAY_PROMOTION_OR_PAPER_LIVE", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(contract: pd.DataFrame, work_order: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    complete = int(hard_pass == hard_rows)
    return pd.DataFrame(
        [
            ("phase324_breadth_expansion_precommit_complete", complete, "Phase324 event-catalyst breadth expansion precommit completed"),
            ("phase324_target_event_rows", TARGET_EVENT_ROWS, "Preferred total event rows for Phase325"),
            ("phase324_minimum_event_rows", MIN_EVENT_ROWS, "Minimum total event rows for Phase325"),
            ("phase324_robust_event_floor", ROBUST_EVENT_FLOOR, "Robustness floor from Phase323 interpretation"),
            ("phase324_min_symbols_per_event", MIN_SYMBOLS_PER_EVENT, "Minimum symbols per event"),
            ("phase324_contract_rows", int(len(contract)), "Expansion contract rows"),
            ("phase324_work_order_rows", int(len(work_order)), "Phase325 work-order rows"),
            ("phase324_full_depth_required", 1, "Depth levels 1-5 required"),
            ("phase324_depth_beyond_l1_required", 1, "Depth levels 2-5 materiality required"),
            ("phase324_l1_only_candidate_allowed", 0, "No L1-only candidate path"),
            ("phase324_fixed_capital_required", 1, "Fixed capital denominator required"),
            ("phase324_cost200_required", 1, "2x cost stress required"),
            ("phase324_strategy_replay_allowed", 0, "No replay"),
            ("phase324_strategy_promotion_allowed", 0, "No promotion"),
            ("phase324_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase324_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase324_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase324_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase324_next_best_action", NEXT_ACTION if complete else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase324 Event-Catalyst Breadth Expansion Precommit",
        "",
        "Phase324 precommits the event-breadth expansion needed after Phase323 found profitable but sparse fixed-capital research leads.",
        "It does not materialize rows, join depth, run strategy search, replay, promote, or claim profitability.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase324_event_catalyst_breadth_expansion_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase323_dir: Path = DEFAULT_PHASE323_DIR, phase315_dir: Path = DEFAULT_PHASE315_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase323 = read_csv(phase323_dir / "phase323_acceptance_summary.csv")
    phase315 = read_csv(phase315_dir / "phase315_acceptance_summary.csv")
    contract = build_expansion_contract(phase323)
    work_order = build_phase325_work_order()
    gates = build_gate_evaluation(phase323, phase315, contract, work_order)
    acceptance = build_acceptance(contract, work_order, gates)

    contract.to_csv(output_dir / "phase324_breadth_expansion_contract.csv", index=False)
    work_order.to_csv(output_dir / "phase324_phase325_work_order.csv", index=False)
    gates.to_csv(output_dir / "phase324_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase324_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, {"Breadth expansion contract": contract, "Phase325 work order": work_order, "Gates": gates})

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase324_event_catalyst_breadth_expansion_precommit",
        **reproducibility_fields(
            artifact_id="phase324",
            generated_utc=generated_utc,
            inputs={
                "phase323_acceptance": str(phase323_dir / "phase323_acceptance_summary.csv"),
                "phase315_acceptance": str(phase315_dir / "phase315_acceptance_summary.csv"),
            },
            parameters={"target_event_rows": TARGET_EVENT_ROWS, "minimum_event_rows": MIN_EVENT_ROWS, "robust_event_floor": ROBUST_EVENT_FLOOR},
            outputs={"acceptance_summary": str(output_dir / "phase324_acceptance_summary.csv")},
            cost_model_version="inherits_phase322",
            latency_model_version="not_applicable_precommit_only",
        ),
    }
    (output_dir / "phase324_event_catalyst_breadth_expansion_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Precommit Phase324 event-catalyst breadth expansion.")
    parser.add_argument("--phase323-dir", type=Path, default=DEFAULT_PHASE323_DIR)
    parser.add_argument("--phase315-dir", type=Path, default=DEFAULT_PHASE315_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase323_dir, args.phase315_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
