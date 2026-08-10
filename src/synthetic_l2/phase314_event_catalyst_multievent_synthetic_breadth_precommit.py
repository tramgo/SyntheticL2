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


DEFAULT_PHASE313_DIR = Path("outputs/phase313")
DEFAULT_OUTPUT_DIR = Path("outputs/phase314")

NEXT_ACTION = "run_phase315_event_catalyst_multievent_synthetic_breadth_materialization_no_replay"
REPAIR_ACTION = "repair_phase314_event_catalyst_multievent_synthetic_breadth_precommit"


def build_breadth_contract() -> pd.DataFrame:
    rows = [
        ("P314_MIN_SYNTHETIC_EVENT_DATES", ">=10", "Generate at least 10 synthetic event dates before rerunning event-catalyst search."),
        ("P314_MIN_SYMBOLS_PER_EVENT", "32", "Each synthetic event should cover the 32-symbol universe when dense rows exist."),
        ("P314_SOURCE_CLOCK_POLICY", "discover_from_dense_row_level_or_row_group_coverage", "Do not assume NSE-clock-normal rows; choose timestamps from actual dense coverage."),
        ("P314_EVENT_WINDOW_SECONDS", "pre=900;post=1800", "Preserve Phase306/307 event window for comparability."),
        ("P314_EVENT_TYPE_POLICY", "synthetic_calendar_rbi_policy_like", "Synthetic-calendar events are catalyst timestamps only, not real RBI dates."),
        ("P314_TRAINING_ONLY_POLICY", "no_replay_no_promotion_no_paper_live", "Breadth expansion is still synthetic-only training research."),
        ("P314_FULL_DEPTH_POLICY", "levels_1_to_5_required", "Every generated event must retain full top-five market-by-price depth."),
        ("P314_L2_L5_MATERIALITY_POLICY", "required", "The next search must preserve depth-beyond-L1 features."),
        ("P314_ACCEPTANCE_FLOOR_FOR_FUTURE", ">=10_events_now;>=30_trades_for_candidate_interpretation", "Increase breadth before interpreting annualized leads."),
        ("P314_NEXT", NEXT_ACTION, "Materialize the multi-event synthetic event ledger and rerun join/features/search pipeline."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_generation_work_order() -> pd.DataFrame:
    rows = [
        ("event_timestamp_discovery", "raw_synthetic_l2_dense_full_year", "Discover candidate timestamps from dense parquet metadata and row-level samples."),
        ("cross_symbol_overlap", "32_symbol_universe", "Keep event timestamps that have broad symbol coverage for the same event window."),
        ("event_spacing", "prefer_distinct_synthetic_dates_and_nonoverlapping_windows", "Avoid near-duplicate adjacent windows."),
        ("calendar_labeling", "synthetic_calendar_event_id", "Label generated rows as synthetic-calendar events, not real-world events."),
        ("phase315_outputs", "event_sources/event_catalysts/generated/phase315_multievent_synthetic_calendar.csv", "Write generated event ledger separately from verified external event sources."),
        ("phase316_join", "rerun_event_catalyst_join_for_multievent_ledger", "Join multi-event ledger to top-five depth before feature/search rerun."),
    ]
    return pd.DataFrame(rows, columns=["work_order_id", "scope", "description"])


def build_controls() -> pd.DataFrame:
    rows = [
        ("real_event_date_claim", "forbidden", "Synthetic-calendar rows must not be described as real-world RBI/news dates."),
        ("directional_event_label", "forbidden", "Event rows provide timing only; no bullish/bearish truth label."),
        ("l1_only_candidate", "forbidden", "Full-depth branch cannot collapse to L1-only."),
        ("unlimited_capital_return", "forbidden", "Future annualized return must retain fixed-capital denominator."),
        ("paper_live_acceptance", "forbidden", "No paper/live claim from synthetic breadth expansion."),
        ("deployable_profitability_claim", "forbidden", "No deployable claim until independent breadth and acceptance gates exist."),
        ("zerodha_cost_stress", "required", "Future search keeps Zerodha cost model and stress profiles."),
        ("sparse_annualized_label", "required", "Annualized >12% remains a sparse research lead until breadth gates pass."),
    ]
    return pd.DataFrame(rows, columns=["control_id", "control_status", "description"])


def build_gate_evaluation(phase313: pd.DataFrame, contract: pd.DataFrame, work_order: pd.DataFrame, controls: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(phase313, "phase313_interpretation_complete", 0))
    selected = str(metric_value(phase313, "phase313_selected_next_route", ""))
    rows = [
        ("P314_PHASE313_COMPLETE", complete == 1, complete, 1),
        ("P314_PHASE313_ROUTE_SELECTED", "P314_EVENT_CATALYST_MULTIEVENT_SYNTHETIC_BREADTH_PRECOMMIT" in selected, selected, "P314 selected"),
        ("P314_CONTRACT_ROWS_PRESENT", len(contract) >= 10, len(contract), ">=10"),
        ("P314_WORK_ORDER_ROWS_PRESENT", len(work_order) >= 6, len(work_order), ">=6"),
        ("P314_CONTROLS_PRESENT", len(controls) >= 8, len(controls), ">=8"),
        ("P314_NO_REPLAY_PROMOTION_OR_PAPER_LIVE", True, "replay=0;promotion=0;paper=0", "all_zero"),
        ("P314_PROFITABILITY_CLAIM_CLOSED", True, 0, 0),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in rows])


def build_acceptance(contract: pd.DataFrame, work_order: pd.DataFrame, controls: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase314_multievent_breadth_precommit_complete", 1, "Phase314 multi-event synthetic breadth precommit completed"),
            ("phase314_breadth_contract_rows", int(len(contract)), "Breadth contract rows"),
            ("phase314_generation_work_order_rows", int(len(work_order)), "Generation work-order rows"),
            ("phase314_control_rows", int(len(controls)), "Control rows"),
            ("phase314_min_synthetic_event_dates", 10, "Minimum synthetic event dates for next materialization"),
            ("phase314_min_symbols_per_event", 32, "Minimum symbol universe target per event"),
            ("phase314_full_depth_required", 1, "Full top-five market-by-price depth required"),
            ("phase314_depth_beyond_l1_required", 1, "Levels 2-5 materiality required"),
            ("phase314_replay_allowed", 0, "No replay"),
            ("phase314_strategy_promotion_allowed", 0, "No promotion"),
            ("phase314_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase314_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase314_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase314_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase314_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase314 Event-Catalyst Multi-Event Synthetic Breadth Precommit",
        "",
        "Phase314 precommits the synthetic multi-event breadth expansion selected by Phase313.",
        "It does not generate events, run joins, replay strategies, promote strategies, or claim deployable profitability.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase314_event_catalyst_multievent_synthetic_breadth_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run(phase313_dir: Path = DEFAULT_PHASE313_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase313 = read_csv(phase313_dir / "phase313_acceptance_summary.csv")
    contract = build_breadth_contract()
    work_order = build_generation_work_order()
    controls = build_controls()
    gates = build_gate_evaluation(phase313, contract, work_order, controls)
    acceptance = build_acceptance(contract, work_order, controls, gates)

    contract.to_csv(output_dir / "phase314_multievent_breadth_contract.csv", index=False)
    work_order.to_csv(output_dir / "phase314_generation_work_order.csv", index=False)
    controls.to_csv(output_dir / "phase314_control_contract.csv", index=False)
    gates.to_csv(output_dir / "phase314_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase314_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, {"Breadth contract": contract, "Generation work order": work_order, "Controls": controls, "Gates": gates})

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase314_event_catalyst_multievent_synthetic_breadth_precommit",
        **reproducibility_fields(
            artifact_id="phase314",
            generated_utc=generated_utc,
            inputs={"phase313_acceptance": str(phase313_dir / "phase313_acceptance_summary.csv")},
            parameters={"min_synthetic_event_dates": 10, "min_symbols_per_event": 32},
            outputs={"acceptance_summary": str(output_dir / "phase314_acceptance_summary.csv")},
            cost_model_version="not_applicable_precommit_only",
            latency_model_version="not_applicable_precommit_only",
        ),
    }
    (output_dir / "phase314_event_catalyst_multievent_synthetic_breadth_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Precommit Phase314 multi-event synthetic breadth expansion.")
    parser.add_argument("--phase313-dir", type=Path, default=DEFAULT_PHASE313_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase313_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
