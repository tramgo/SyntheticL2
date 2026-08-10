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
from synthetic_l2.phase315_event_catalyst_multievent_synthetic_breadth_materialization import (
    DEFAULT_DENSE_ROOT,
    MIN_SYMBOLS_PER_EVENT,
    POST_EVENT_SECONDS,
    PRE_EVENT_SECONDS,
    REFERENCE_SYMBOL,
    dense_reference_date_candidates,
    discover_bounds,
    row_group_candidates,
    select_events,
)
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE324_DIR = Path("outputs/phase324")
DEFAULT_GENERATED_DIR = Path("event_sources/event_catalysts/generated")
DEFAULT_OUTPUT_DIR = Path("outputs/phase325")

TARGET_EVENT_ROWS = 50
MIN_EVENT_ROWS = 40
NEXT_ACTION = "run_phase326_event_catalyst_expanded_top5_depth_join_precommit_no_replay"
REPAIR_ACTION = "repair_phase325_event_catalyst_breadth_expansion_materialization"


def rewrite_phase325_events(events: pd.DataFrame, work_order: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if events.empty:
        return events, work_order
    events = events.copy().sort_values("event_epoch_seconds").reset_index(drop=True)
    id_map: dict[str, str] = {}
    for idx, row in events.iterrows():
        old = str(row["event_id"])
        event_date = str(row["event_date_ist"]).replace("-", "")
        new = f"P325_SYNTH_EVENT_{idx + 1:03d}_{event_date}"
        id_map[old] = new
        events.loc[idx, "event_id"] = new
        events.loc[idx, "source_url_or_file"] = "outputs/phase324/phase324_phase325_work_order.csv"
        events.loc[idx, "event_title"] = f"Phase325 expanded synthetic catalyst breadth timestamp {idx + 1:03d}"
        events.loc[idx, "source_provider"] = "SyntheticL2 Phase325 dense-coverage timestamp generator"
        events.loc[idx, "notes"] = "Expanded synthetic-calendar catalyst timestamp generated from dense parquet timestamp coverage; not a real-world RBI/news event."
    if not work_order.empty:
        work_order = work_order.copy()
        work_order["event_id"] = work_order["event_id"].astype(str).map(id_map).fillna(work_order["event_id"].astype(str))
    return events, work_order


def build_gate_evaluation(phase324: pd.DataFrame, events: pd.DataFrame, work_order: pd.DataFrame, inventory: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(phase324, "phase324_breadth_expansion_precommit_complete", 0))
    event_rows = int(len(events))
    distinct_dates = int(events["event_date_ist"].nunique()) if not events.empty else 0
    min_symbols = int(events["covered_symbols"].min()) if not events.empty else 0
    work_order_events = int(work_order["event_id"].nunique()) if not work_order.empty else 0
    rows: list[tuple[str, bool, Any, Any]] = [
        ("P325_PHASE324_COMPLETE", complete == 1, complete, 1),
        ("P325_DENSE_FILE_INVENTORY_PRESENT", len(inventory) > 0, len(inventory), ">0"),
        ("P325_MIN_EVENT_ROWS", event_rows >= MIN_EVENT_ROWS, event_rows, f">={MIN_EVENT_ROWS}"),
        ("P325_TARGET_EVENT_ROWS", event_rows >= TARGET_EVENT_ROWS, event_rows, f">={TARGET_EVENT_ROWS}"),
        ("P325_DISTINCT_EVENT_DATES", distinct_dates == event_rows and distinct_dates >= MIN_EVENT_ROWS, distinct_dates, "one_date_per_event_and_min_met"),
        ("P325_SYMBOL_COVERAGE_TARGET_MET", min_symbols >= MIN_SYMBOLS_PER_EVENT, min_symbols, f">={MIN_SYMBOLS_PER_EVENT}"),
        ("P325_EVENT_SYMBOL_WORK_ORDER_COMPLETE", work_order_events == event_rows and len(work_order) >= event_rows * MIN_SYMBOLS_PER_EVENT, f"events={work_order_events};rows={len(work_order)}", "all_events_x_32_symbols"),
        ("P325_FULL_DEPTH_POLICY_PRESERVED", as_int(metric_value(phase324, "phase324_full_depth_required", 0)) == 1, metric_value(phase324, "phase324_full_depth_required", ""), 1),
        ("P325_DEPTH_BEYOND_L1_POLICY_PRESERVED", as_int(metric_value(phase324, "phase324_depth_beyond_l1_required", 0)) == 1, metric_value(phase324, "phase324_depth_beyond_l1_required", ""), 1),
        ("P325_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(events: pd.DataFrame, work_order: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    complete = int(hard_pass == hard_rows)
    return pd.DataFrame(
        [
            ("phase325_breadth_expansion_materialization_complete", complete, "Phase325 event-catalyst breadth expansion materialization completed"),
            ("phase325_generated_event_rows", int(len(events)), "Expanded generated synthetic catalyst event rows"),
            ("phase325_distinct_event_dates", int(events["event_date_ist"].nunique()) if not events.empty else 0, "Distinct generated synthetic event dates"),
            ("phase325_min_symbols_per_event", int(events["covered_symbols"].min()) if not events.empty else 0, "Minimum symbol coverage across generated events"),
            ("phase325_event_symbol_work_order_rows", int(len(work_order)), "Event-symbol dense join work-order rows"),
            ("phase325_target_event_rows", TARGET_EVENT_ROWS, "Target event rows"),
            ("phase325_minimum_event_rows", MIN_EVENT_ROWS, "Minimum event rows"),
            ("phase325_full_depth_required", 1, "Future join/search must use top-five market-by-price depth levels 1-5"),
            ("phase325_depth_beyond_l1_required", 1, "Future features/search must preserve depth levels 2-5 materiality"),
            ("phase325_strategy_replay_allowed", 0, "No replay"),
            ("phase325_strategy_promotion_allowed", 0, "No promotion"),
            ("phase325_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase325_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase325_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase325_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase325_next_best_action", NEXT_ACTION if complete else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, events: pd.DataFrame, work_order: pd.DataFrame, inventory: pd.DataFrame, candidates: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase325 Event-Catalyst Breadth Expansion Materialization",
        "",
        "Phase325 materializes an expanded synthetic catalyst event ledger and event-symbol work order from actual dense parquet timestamp coverage.",
        "It does not join depth rows, run strategy search, replay, promote, or claim profitability.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Expanded generated synthetic events",
        "",
        _markdown_table(events),
        "",
        "## Event-symbol work order preview",
        "",
        _markdown_table(work_order.head(80)),
        "",
        "## Dense inventory summary",
        "",
        _markdown_table(
            pd.DataFrame(
                [
                    {
                        "dense_files": int(len(inventory)),
                        "symbols": int(inventory["symbol"].nunique()) if not inventory.empty else 0,
                        "trade_month_partitions": int(inventory["trade_month_partition"].nunique()) if not inventory.empty else 0,
                        "total_source_rows": int(inventory["source_rows"].sum()) if not inventory.empty else 0,
                    }
                ]
            )
        ),
        "",
        "## Candidate discovery preview",
        "",
        _markdown_table(candidates.head(40)),
        "",
        "## Gates",
        "",
        _markdown_table(gates),
    ]
    (output_dir / "phase325_event_catalyst_breadth_expansion_materialization_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    phase324_dir: Path = DEFAULT_PHASE324_DIR,
    dense_root: Path = DEFAULT_DENSE_ROOT,
    generated_dir: Path = DEFAULT_GENERATED_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    reference_symbol: str = REFERENCE_SYMBOL,
) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase324 = read_csv(phase324_dir / "phase324_acceptance_summary.csv")
    inventory, by_symbol = discover_bounds(dense_root)
    candidates = dense_reference_date_candidates(dense_root, reference_symbol, TARGET_EVENT_ROWS)
    if candidates.empty:
        candidate_rows: list[dict[str, Any]] = []
        for path in sorted(dense_root.glob(f"trade_month=*/symbol={reference_symbol}/part-*.parquet")):
            candidate_rows.extend(row_group_candidates(path))
        candidates = pd.DataFrame(candidate_rows)
    events, work_order = select_events(candidates, by_symbol, TARGET_EVENT_ROWS, MIN_SYMBOLS_PER_EVENT)
    events, work_order = rewrite_phase325_events(events, work_order)
    gates = build_gate_evaluation(phase324, events, work_order, inventory)
    acceptance = build_acceptance(events, work_order, gates)

    calendar_columns = [
        "event_time_ist",
        "event_type",
        "symbol_scope",
        "index_scope",
        "source_url_or_file",
        "confidence",
        "embargo_safe_flag",
        "event_title",
        "expected_impact_side",
        "source_provider",
        "source_published_time_ist",
        "notes",
    ]
    events.to_csv(output_dir / "phase325_expanded_synthetic_event_ledger.csv", index=False)
    if not events.empty:
        events[calendar_columns].to_csv(generated_dir / "phase325_expanded_synthetic_calendar.csv", index=False)
    work_order.to_csv(output_dir / "phase325_event_symbol_join_work_order.csv", index=False)
    inventory.to_csv(output_dir / "phase325_dense_file_inventory.csv", index=False)
    candidates.to_csv(output_dir / "phase325_reference_row_level_candidates.csv", index=False)
    gates.to_csv(output_dir / "phase325_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase325_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, events, work_order, inventory, candidates, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase325_event_catalyst_breadth_expansion_materialization",
        **reproducibility_fields(
            artifact_id="phase325",
            generated_utc=generated_utc,
            inputs={"phase324_acceptance": str(phase324_dir / "phase324_acceptance_summary.csv"), "dense_root": str(dense_root)},
            parameters={"reference_symbol": reference_symbol, "target_event_rows": TARGET_EVENT_ROWS, "minimum_event_rows": MIN_EVENT_ROWS},
            outputs={
                "acceptance_summary": str(output_dir / "phase325_acceptance_summary.csv"),
                "expanded_calendar": str(generated_dir / "phase325_expanded_synthetic_calendar.csv"),
                "event_symbol_work_order": str(output_dir / "phase325_event_symbol_join_work_order.csv"),
            },
            cost_model_version="not_applicable_event_materialization_only",
            latency_model_version="not_applicable_event_materialization_only",
        ),
    }
    (output_dir / "phase325_event_catalyst_breadth_expansion_materialization_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize Phase325 expanded synthetic event-catalyst breadth ledger.")
    parser.add_argument("--phase324-dir", type=Path, default=DEFAULT_PHASE324_DIR)
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--generated-dir", type=Path, default=DEFAULT_GENERATED_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--reference-symbol", default=REFERENCE_SYMBOL)
    args = parser.parse_args()
    acceptance = run(args.phase324_dir, args.dense_root, args.generated_dir, args.output_dir, args.reference_symbol)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
