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


DEFAULT_PHASE325_DIR = Path("outputs/phase325")
DEFAULT_OUTPUT_DIR = Path("outputs/phase326")

PRE_EVENT_SECONDS = 900
POST_EVENT_SECONDS = 1800
MIN_EVENT_ROWS = 40
TARGET_EVENT_ROWS = 50
MIN_SYMBOLS_PER_EVENT = 32
NEXT_ACTION = "run_phase327_event_catalyst_expanded_top5_depth_join_materialization_no_strategy_search"
REPAIR_ACTION = "repair_phase326_event_catalyst_expanded_top5_depth_join_precommit"

DEPTH_COLUMNS = [
    f"{side}_{level}_{field}"
    for level in range(1, 6)
    for side in ("buy", "sell")
    for field in ("price", "quantity", "orders")
]


def build_join_contract(events: pd.DataFrame, work_order: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("P326_INPUT_EVENTS", str(len(events)), "Use the expanded Phase325 synthetic catalyst event ledger."),
            ("P326_INPUT_EVENT_SYMBOL_ROWS", str(len(work_order)), "Use the Phase325 event-symbol dense join work order."),
            ("P326_JOIN_WINDOW_SECONDS", f"pre={PRE_EVENT_SECONDS};post={POST_EVENT_SECONDS}", "Preserve Phase317/320 event-window comparability."),
            ("P326_JOIN_CLOCK", "event_time_ist", "Center each join window on the generated catalyst timestamp."),
            ("P326_FULL_DEPTH_REQUIRED", "depth_levels_1_to_5", "Materialization must retain all visible top-five market-by-price depth columns."),
            ("P326_DEPTH_BEYOND_L1_REQUIRED", "depth_levels_2_to_5_material", "Downstream features/search must not collapse to top-of-book only."),
            ("P326_OUTPUT_JOINED_PARQUET", "outputs/phase327/phase327_joined_expanded_event_top5_depth.parquet", "Phase327 expanded joined top-five depth target."),
            ("P326_OUTPUT_COVERAGE_AUDIT", "outputs/phase327/phase327_event_symbol_timestamp_coverage.csv", "Phase327 coverage audit target."),
            ("P326_TARGET_EVENT_ROWS", str(TARGET_EVENT_ROWS), "Preferred expanded breadth target inherited from Phase324/325."),
            ("P326_MIN_EVENT_ROWS", str(MIN_EVENT_ROWS), "Minimum expanded breadth target inherited from Phase324/325."),
            ("P326_NO_DIRECTIONAL_LABEL", "required", "Event rows provide timing only, not true bullish/bearish labels."),
            ("P326_NO_STRATEGY_SEARCH", "required", "Expanded join materialization precedes feature/search phases."),
            ("P326_BOUNDARIES", "replay=0;promotion=0;paper=0;claim=0", "No strategy acceptance boundaries change in this phase."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def build_materialization_work_order(work_order: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "event_id",
        "event_time_ist",
        "event_type",
        "symbol",
        "dense_file_path",
        "pre_event_seconds",
        "post_event_seconds",
        "window_start_epoch",
        "window_end_epoch",
        "timestamp_overlap",
    ]
    frame = work_order.copy()
    for col in columns:
        if col not in frame.columns:
            frame[col] = ""
    frame = frame[columns].copy()
    frame["phase327_action"] = "read_overlapping_row_groups_and_filter_window"
    frame["required_depth_columns"] = ";".join(DEPTH_COLUMNS)
    return frame


def build_gate_evaluation(phase325: pd.DataFrame, events: pd.DataFrame, work_order: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    event_rows = int(len(events))
    distinct_dates = int(events["event_date_ist"].nunique()) if "event_date_ist" in events.columns and not events.empty else 0
    min_symbols = int(work_order.groupby("event_id")["symbol"].nunique().min()) if not work_order.empty else 0
    bad_windows = 0
    if not work_order.empty:
        bad_windows = int(
            (
                (pd.to_numeric(work_order.get("pre_event_seconds"), errors="coerce").fillna(0).astype(int) != PRE_EVENT_SECONDS)
                | (pd.to_numeric(work_order.get("post_event_seconds"), errors="coerce").fillna(0).astype(int) != POST_EVENT_SECONDS)
            ).sum()
        )
    rows: list[tuple[str, bool, Any, Any]] = [
        ("P326_PHASE325_MATERIALIZATION_COMPLETE", as_int(metric_value(phase325, "phase325_breadth_expansion_materialization_complete", 0)) == 1, metric_value(phase325, "phase325_breadth_expansion_materialization_complete", ""), 1),
        ("P326_TARGET_EVENT_ROWS_PRESENT", event_rows >= TARGET_EVENT_ROWS, event_rows, f">={TARGET_EVENT_ROWS}"),
        ("P326_MIN_EVENT_ROWS_PRESENT", event_rows >= MIN_EVENT_ROWS, event_rows, f">={MIN_EVENT_ROWS}"),
        ("P326_DISTINCT_EVENT_DATES_PRESENT", distinct_dates >= TARGET_EVENT_ROWS, distinct_dates, f">={TARGET_EVENT_ROWS}"),
        ("P326_32_SYMBOL_COVERAGE_PRESENT", min_symbols >= MIN_SYMBOLS_PER_EVENT, min_symbols, f">={MIN_SYMBOLS_PER_EVENT}"),
        ("P326_EVENT_SYMBOL_WORK_ORDER_COMPLETE", len(work_order) >= event_rows * MIN_SYMBOLS_PER_EVENT and work_order["event_id"].nunique() == event_rows, f"events={work_order['event_id'].nunique() if not work_order.empty else 0};rows={len(work_order)}", "all_events_x_32_symbols"),
        ("P326_JOIN_WINDOWS_FIXED", bad_windows == 0, bad_windows, 0),
        ("P326_FULL_DEPTH_CONTRACT_PRESENT", "P326_FULL_DEPTH_REQUIRED" in set(contract["contract_id"].astype(str)), "contract", "present"),
        ("P326_DEPTH_BEYOND_L1_CONTRACT_PRESENT", "P326_DEPTH_BEYOND_L1_REQUIRED" in set(contract["contract_id"].astype(str)), "contract", "present"),
        ("P326_NO_STRATEGY_SEARCH_OPENED", True, "strategy_search_allowed_now=0", 0),
        ("P326_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(events: pd.DataFrame, work_order: pd.DataFrame, contract: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    complete = int(hard_pass == hard_rows)
    return pd.DataFrame(
        [
            ("phase326_expanded_top5_depth_join_precommit_complete", complete, "Phase326 expanded top-five depth join precommit completed"),
            ("phase326_generated_event_rows", int(len(events)), "Phase325 expanded synthetic event rows inherited"),
            ("phase326_event_symbol_work_order_rows", int(len(work_order)), "Phase325 event-symbol work-order rows inherited"),
            ("phase326_min_symbols_per_event", int(work_order.groupby("event_id")["symbol"].nunique().min()) if not work_order.empty else 0, "Minimum symbols per generated event"),
            ("phase326_join_contract_rows", int(len(contract)), "Join contract rows"),
            ("phase326_target_event_rows", TARGET_EVENT_ROWS, "Target event rows"),
            ("phase326_minimum_event_rows", MIN_EVENT_ROWS, "Minimum event rows"),
            ("phase326_full_depth_required", 1, "Phase327 must retain depth levels 1-5"),
            ("phase326_depth_beyond_l1_required", 1, "Phase327/328 must preserve depth levels 2-5 materiality"),
            ("phase326_strategy_search_allowed_now", 0, "No strategy search in Phase326"),
            ("phase326_strategy_replay_allowed", 0, "No replay"),
            ("phase326_strategy_promotion_allowed", 0, "No promotion"),
            ("phase326_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase326_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase326_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase326_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase326_next_best_action", NEXT_ACTION if complete else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, contract: pd.DataFrame, materialization_work_order: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase326 Event-Catalyst Expanded Top-Five Depth Join Precommit",
        "",
        "Phase326 precommits the expanded 50-event top-five market-by-price depth join from the Phase325 event ledger.",
        "It does not materialize joined rows, run strategy search, replay, promote, or claim profitability.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Join contract",
        "",
        _markdown_table(contract),
        "",
        "## Phase327 materialization work-order preview",
        "",
        _markdown_table(materialization_work_order.head(80)),
        "",
        "## Gates",
        "",
        _markdown_table(gates),
    ]
    (output_dir / "phase326_event_catalyst_expanded_top5_depth_join_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase325_dir: Path = DEFAULT_PHASE325_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase325 = read_csv(phase325_dir / "phase325_acceptance_summary.csv")
    events = read_csv(phase325_dir / "phase325_expanded_synthetic_event_ledger.csv")
    work_order = read_csv(phase325_dir / "phase325_event_symbol_join_work_order.csv")
    contract = build_join_contract(events, work_order)
    materialization_work_order = build_materialization_work_order(work_order)
    gates = build_gate_evaluation(phase325, events, work_order, contract)
    acceptance = build_acceptance(events, work_order, contract, gates)

    contract.to_csv(output_dir / "phase326_expanded_top5_depth_join_contract.csv", index=False)
    materialization_work_order.to_csv(output_dir / "phase326_phase327_materialization_work_order.csv", index=False)
    gates.to_csv(output_dir / "phase326_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase326_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, contract, materialization_work_order, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase326_event_catalyst_expanded_top5_depth_join_precommit",
        **reproducibility_fields(
            artifact_id="phase326",
            generated_utc=generated_utc,
            inputs={
                "phase325_acceptance": str(phase325_dir / "phase325_acceptance_summary.csv"),
                "phase325_events": str(phase325_dir / "phase325_expanded_synthetic_event_ledger.csv"),
                "phase325_work_order": str(phase325_dir / "phase325_event_symbol_join_work_order.csv"),
            },
            parameters={"pre_event_seconds": PRE_EVENT_SECONDS, "post_event_seconds": POST_EVENT_SECONDS, "depth_columns": DEPTH_COLUMNS},
            outputs={"acceptance_summary": str(output_dir / "phase326_acceptance_summary.csv")},
            cost_model_version="not_applicable_join_precommit_only",
            latency_model_version="not_applicable_join_precommit_only",
        ),
    }
    (output_dir / "phase326_event_catalyst_expanded_top5_depth_join_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Precommit Phase326 expanded top-five depth join.")
    parser.add_argument("--phase325-dir", type=Path, default=DEFAULT_PHASE325_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase325_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
