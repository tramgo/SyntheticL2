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


DEFAULT_PHASE302_DIR = Path("outputs/phase302")
DEFAULT_OUTPUT_DIR = Path("outputs/phase303")

SELECTED_ROUTE = "P303_EXTERNAL_EVENT_CATALYST_PLUS_L2_RESPONSE_SOURCE_ACQUISITION"
NEXT_ACTION = "acquire_or_build_material_new_event_catalyst_source_before_any_new_l2_strategy_search"
REPAIR_ACTION = "repair_phase303_material_new_thesis_source_selector"


def build_candidate_catalog() -> pd.DataFrame:
    rows = [
        {
            "candidate_id": "P303_SAME_DIRECTIONAL_TOP5_RESCUE",
            "candidate_type": "rejected_same_route",
            "material_new_source": 0,
            "material_new_thesis": 0,
            "uses_top_five_depth_levels_1_to_5": 1,
            "requires_external_data": 0,
            "reason": "Only changes filters/execution around the Phase298-302 closed route.",
            "decision": "reject",
        },
        {
            "candidate_id": "P303_TWO_SIDED_RETAIL_MARKET_MAKING",
            "candidate_type": "rejected_scope",
            "material_new_source": 0,
            "material_new_thesis": 1,
            "uses_top_five_depth_levels_1_to_5": 1,
            "requires_external_data": 0,
            "reason": "Retail has no maker rebate, weak queue priority and slow cancels; prior charter excludes live market-making.",
            "decision": "reject_for_live_acceptance",
        },
        {
            "candidate_id": "P303_EXTERNAL_EVENT_CATALYST_PLUS_L2_RESPONSE",
            "candidate_type": "material_new_source_and_thesis",
            "material_new_source": 1,
            "material_new_thesis": 1,
            "uses_top_five_depth_levels_1_to_5": 1,
            "requires_external_data": 1,
            "reason": "Adds exogenous event/news/calendar state before interpreting L2 response; not a same-signal rescue.",
            "decision": "select",
        },
        {
            "candidate_id": "P303_BROKER_FILL_CONTRACT_NOTE_RECONCILIATION",
            "candidate_type": "material_new_execution_source",
            "material_new_source": 1,
            "material_new_thesis": 0,
            "uses_top_five_depth_levels_1_to_5": 0,
            "requires_external_data": 1,
            "reason": "Would validate execution economics, but user stated Zerodha fills/contract notes are unavailable.",
            "decision": "defer_until_available",
        },
        {
            "candidate_id": "P303_DERIVATIVES_OR_INDEX_FUTURES_LEAD_SOURCE",
            "candidate_type": "material_new_cross_market_source",
            "material_new_source": 1,
            "material_new_thesis": 1,
            "uses_top_five_depth_levels_1_to_5": 1,
            "requires_external_data": 1,
            "reason": "Adds a cross-market lead source; useful if futures/options/index feed can be acquired.",
            "decision": "candidate_after_event_catalyst",
        },
    ]
    return pd.DataFrame(rows)


def build_work_order(candidates: pd.DataFrame) -> pd.DataFrame:
    selected = candidates[candidates["decision"].eq("select")].iloc[0]
    return pd.DataFrame(
        [
            ("P303_WO_01", "define_event_source_schema", selected["candidate_id"], "event_time_ist,event_type,symbol_scope,index_scope,source_url_or_file,confidence,embargo_safe_flag"),
            ("P303_WO_02", "create_or_import_event_calendar", selected["candidate_id"], "No strategy search until at least one event source file exists."),
            ("P303_WO_03", "join_events_to_top5_depth_response", selected["candidate_id"], "Use tick-level top-five market-by-price levels 1-5 before/after event time."),
            ("P303_WO_04", "precommit_acceptance_gates", selected["candidate_id"], "Fixed capital, Zerodha cost200, event/breadth floors, no paper/live/profitability claim."),
            ("P303_WO_05", "run_only_after_source_exists", selected["candidate_id"], "Do not mine Phase302-closed same-route filters while waiting for source."),
        ],
        columns=["work_order_id", "action", "selected_candidate_id", "deliverable"],
    )


def build_gate_evaluation(phase302: pd.DataFrame, candidates: pd.DataFrame, work_order: pd.DataFrame) -> pd.DataFrame:
    selected = candidates[candidates["decision"].eq("select")]
    same_route_rejected = candidates.loc[candidates["candidate_id"].eq("P303_SAME_DIRECTIONAL_TOP5_RESCUE"), "decision"].astype(str).eq("reject").any()
    selected_new = bool(
        not selected.empty
        and as_int(selected["material_new_source"].iloc[0]) == 1
        and as_int(selected["material_new_thesis"].iloc[0]) == 1
    )
    gates = [
        ("P303_PHASE302_TERMINAL_COMPLETE", as_int(metric_value(phase302, "phase302_terminal_report_complete", 0)) == 1, metric_value(phase302, "phase302_terminal_report_complete", ""), 1),
        ("P303_PHASE302_MATERIAL_NEW_REQUIRED", as_int(metric_value(phase302, "phase302_material_new_source_or_thesis_required", 0)) == 1, metric_value(phase302, "phase302_material_new_source_or_thesis_required", ""), 1),
        ("P303_SAME_ROUTE_REJECTED", same_route_rejected, int(same_route_rejected), 1),
        ("P303_SELECTED_ROUTE_IS_MATERIAL_NEW", selected_new, int(selected_new), 1),
        ("P303_FULL_DEPTH_RETAINED", as_int(selected["uses_top_five_depth_levels_1_to_5"].iloc[0]) == 1 if not selected.empty else False, selected["uses_top_five_depth_levels_1_to_5"].iloc[0] if not selected.empty else "", 1),
        ("P303_EXTERNAL_SOURCE_REQUIREMENT_EXPLICIT", as_int(selected["requires_external_data"].iloc[0]) == 1 if not selected.empty else False, selected["requires_external_data"].iloc[0] if not selected.empty else "", 1),
        ("P303_WORK_ORDER_PRESENT", len(work_order) >= 5, len(work_order), ">=5"),
        ("P303_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(candidates: pd.DataFrame, work_order: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase303_material_new_selector_complete", 1, "Phase303 material-new thesis/source selector completed"),
            ("phase303_selected_route", SELECTED_ROUTE, "Selected route"),
            ("phase303_candidate_rows", len(candidates), "Candidate routes evaluated"),
            ("phase303_rejected_same_route_rows", int(candidates["candidate_type"].astype(str).eq("rejected_same_route").sum()), "Same-route candidates rejected"),
            ("phase303_selected_requires_external_source", 1, "Selected route requires new external source"),
            ("phase303_selected_uses_top_five_depth_levels_1_to_5", 1, "Selected route keeps top-five market-by-price levels 1-5"),
            ("phase303_work_order_rows", len(work_order), "Work-order rows emitted"),
            ("phase303_strategy_search_allowed_now", 0, "No strategy search until the new source exists"),
            ("phase303_strategy_replay_allowed", 0, "No replay"),
            ("phase303_strategy_promotion_allowed", 0, "No promotion"),
            ("phase303_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase303_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase303_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase303_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase303_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, candidates: pd.DataFrame, work_order: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase303 Material-New Thesis and Source Selector",
        "",
        "Phase303 responds to Phase302's terminal closure by selecting only a genuinely material-new path. It does not reopen the closed retail directional top-five depth rescue route.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Candidate catalog",
        "",
        _markdown_table(candidates),
        "",
        "## Work order",
        "",
        _markdown_table(work_order),
        "",
        "## Gates",
        "",
        _markdown_table(gates),
        "",
        "Boundary: no strategy search, replay, promotion, paper/live acceptance or profitability claim is opened until the new event-catalyst source exists and is joined to tick-level top-five market-by-price depth levels 1-5.",
    ]
    (output_dir / "phase303_material_new_thesis_source_selector_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase302_dir: Path = DEFAULT_PHASE302_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase302 = read_csv(phase302_dir / "phase302_acceptance_summary.csv")
    candidates = build_candidate_catalog()
    work_order = build_work_order(candidates)
    gates = build_gate_evaluation(phase302, candidates, work_order)
    acceptance = build_acceptance(candidates, work_order, gates)

    candidates.to_csv(output_dir / "phase303_material_new_candidate_catalog.csv", index=False)
    work_order.to_csv(output_dir / "phase303_material_new_source_work_order.csv", index=False)
    gates.to_csv(output_dir / "phase303_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase303_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, candidates, work_order, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase303_material_new_thesis_source_selector",
        **reproducibility_fields(
            artifact_id="phase303",
            generated_utc=generated_utc,
            inputs={"phase302_acceptance": str(phase302_dir / "phase302_acceptance_summary.csv")},
            parameters={"selected_route": SELECTED_ROUTE, "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase303_acceptance_summary.csv")},
            cost_model_version="not_applicable_decision_only",
            latency_model_version="not_applicable_decision_only",
        ),
    }
    (output_dir / "phase303_material_new_thesis_source_selector_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Phase303 material-new thesis/source selector.")
    parser.add_argument("--phase302-dir", type=Path, default=DEFAULT_PHASE302_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase302_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
