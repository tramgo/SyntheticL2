from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE317_DIR = Path("outputs/phase317")
DEFAULT_OUTPUT_DIR = Path("outputs/phase318")

NEXT_ACTION = "run_phase319_event_catalyst_multievent_feature_materialization_precommit_no_replay"
REPAIR_ACTION = "repair_phase318_event_catalyst_multievent_join_quality_audit"

DEPTH_COLUMNS = [
    f"{side}_{level}_{field}"
    for level in range(1, 6)
    for side in ("buy", "sell")
    for field in ("price", "quantity", "orders")
]


def parquet_path(phase317_dir: Path) -> Path:
    return phase317_dir / "phase317_joined_multievent_top5_depth.parquet"


def run_duckdb_quality(joined_path: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    con = duckdb.connect()
    path = str(joined_path).replace("\\", "/")
    summary = con.execute(
        f"""
        select
          count(*) as joined_rows,
          count(distinct event_id) as event_rows,
          count(distinct symbol) as symbol_rows,
          min(relative_second) as min_relative_second,
          max(relative_second) as max_relative_second,
          sum(case when buy_1_price >= sell_1_price then 1 else 0 end) as crossed_or_locked_l1_rows,
          sum(case when buy_1_quantity <= 0 or sell_1_quantity <= 0 then 1 else 0 end) as nonpositive_l1_quantity_rows,
          sum(case when buy_2_quantity <= 0 or buy_3_quantity <= 0 or buy_4_quantity <= 0 or buy_5_quantity <= 0
                    or sell_2_quantity <= 0 or sell_3_quantity <= 0 or sell_4_quantity <= 0 or sell_5_quantity <= 0
                   then 1 else 0 end) as nonpositive_depth_beyond_l1_quantity_rows,
          sum(case when not (buy_1_price >= buy_2_price and buy_2_price >= buy_3_price and buy_3_price >= buy_4_price and buy_4_price >= buy_5_price)
                   then 1 else 0 end) as bid_depth_sort_error_rows,
          sum(case when not (sell_1_price <= sell_2_price and sell_2_price <= sell_3_price and sell_3_price <= sell_4_price and sell_4_price <= sell_5_price)
                   then 1 else 0 end) as ask_depth_sort_error_rows,
          sum(case when buy_2_quantity + buy_3_quantity + buy_4_quantity + buy_5_quantity + sell_2_quantity + sell_3_quantity + sell_4_quantity + sell_5_quantity > 0
                   then 1 else 0 end) as depth_beyond_l1_material_rows
        from read_parquet('{path}', hive_partitioning=false)
        """
    ).fetchdf()
    by_event = con.execute(
        f"""
        select event_id, count(*) as joined_rows, count(distinct symbol) as symbols,
               min(relative_second) as min_relative_second, max(relative_second) as max_relative_second
        from read_parquet('{path}', hive_partitioning=false)
        group by 1
        order by 1
        """
    ).fetchdf()
    by_symbol = con.execute(
        f"""
        select symbol, count(*) as joined_rows, count(distinct event_id) as events,
               min(relative_second) as min_relative_second, max(relative_second) as max_relative_second
        from read_parquet('{path}', hive_partitioning=false)
        group by 1
        order by 1
        """
    ).fetchdf()
    return summary, by_event, by_symbol


def build_gate_evaluation(phase317: pd.DataFrame, joined_path: Path, summary: pd.DataFrame, by_event: pd.DataFrame, by_symbol: pd.DataFrame) -> pd.DataFrame:
    schema_names = set(pq.ParquetFile(joined_path).schema.names) if joined_path.exists() else set()
    row = summary.iloc[0] if not summary.empty else pd.Series(dtype=object)
    joined_rows = as_int(row.get("joined_rows", 0))
    event_rows = as_int(row.get("event_rows", 0))
    symbol_rows = as_int(row.get("symbol_rows", 0))
    min_event_symbols = int(by_event["symbols"].min()) if not by_event.empty else 0
    min_symbol_events = int(by_symbol["events"].min()) if not by_symbol.empty else 0
    depth_material = as_int(row.get("depth_beyond_l1_material_rows", 0))
    rows: list[tuple[str, bool, Any, Any]] = [
        ("P318_PHASE317_COMPLETE", as_int(metric_value(phase317, "phase317_multievent_top5_depth_join_materialization_complete", 0)) == 1, metric_value(phase317, "phase317_multievent_top5_depth_join_materialization_complete", ""), 1),
        ("P318_JOINED_PARQUET_EXISTS", joined_path.exists(), int(joined_path.exists()), 1),
        ("P318_FULL_DEPTH_SCHEMA_PRESENT", set(DEPTH_COLUMNS).issubset(schema_names), int(set(DEPTH_COLUMNS).issubset(schema_names)), 1),
        ("P318_JOINED_ROWS_MATCH_PHASE317", joined_rows == as_int(metric_value(phase317, "phase317_materialized_join_rows", 0)), joined_rows, metric_value(phase317, "phase317_materialized_join_rows", "")),
        ("P318_EVENT_COVERAGE_COMPLETE", event_rows >= 10 and min_event_symbols >= 32, f"events={event_rows};min_symbols={min_event_symbols}", ">=10_events_x_32_symbols"),
        ("P318_SYMBOL_COVERAGE_COMPLETE", symbol_rows >= 32 and min_symbol_events >= 10, f"symbols={symbol_rows};min_events={min_symbol_events}", ">=32_symbols_x_10_events"),
        ("P318_RELATIVE_WINDOW_BOUNDED", as_int(row.get("min_relative_second", 0)) >= -900 and as_int(row.get("max_relative_second", 0)) <= 1800, f"{row.get('min_relative_second', '')}..{row.get('max_relative_second', '')}", "-900..1800"),
        ("P318_NO_CROSSED_OR_LOCKED_L1", as_int(row.get("crossed_or_locked_l1_rows", 0)) == 0, row.get("crossed_or_locked_l1_rows", ""), 0),
        ("P318_DEPTH_SORT_OK", as_int(row.get("bid_depth_sort_error_rows", 0)) == 0 and as_int(row.get("ask_depth_sort_error_rows", 0)) == 0, f"bid={row.get('bid_depth_sort_error_rows', '')};ask={row.get('ask_depth_sort_error_rows', '')}", 0),
        ("P318_DEPTH_BEYOND_L1_MATERIAL", depth_material == joined_rows and joined_rows > 0, depth_material, joined_rows),
        ("P318_NO_STRATEGY_SEARCH_OPENED", True, "strategy_search_allowed_now=0", 0),
        ("P318_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(summary: pd.DataFrame, by_event: pd.DataFrame, by_symbol: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    row = summary.iloc[0] if not summary.empty else pd.Series(dtype=object)
    complete = int(hard_pass == hard_rows)
    return pd.DataFrame(
        [
            ("phase318_multievent_join_quality_audit_complete", complete, "Phase318 multi-event join quality audit completed"),
            ("phase318_joined_rows", as_int(row.get("joined_rows", 0)), "Joined rows audited"),
            ("phase318_event_rows", as_int(row.get("event_rows", 0)), "Distinct events audited"),
            ("phase318_symbol_rows", as_int(row.get("symbol_rows", 0)), "Distinct symbols audited"),
            ("phase318_min_event_symbol_coverage", int(by_event["symbols"].min()) if not by_event.empty else 0, "Minimum symbols per event"),
            ("phase318_min_symbol_event_coverage", int(by_symbol["events"].min()) if not by_symbol.empty else 0, "Minimum events per symbol"),
            ("phase318_relative_second_min", as_int(row.get("min_relative_second", 0)), "Minimum relative second"),
            ("phase318_relative_second_max", as_int(row.get("max_relative_second", 0)), "Maximum relative second"),
            ("phase318_crossed_or_locked_l1_rows", as_int(row.get("crossed_or_locked_l1_rows", 0)), "Crossed or locked top-of-book rows"),
            ("phase318_bid_depth_sort_error_rows", as_int(row.get("bid_depth_sort_error_rows", 0)), "Bid depth sort error rows"),
            ("phase318_ask_depth_sort_error_rows", as_int(row.get("ask_depth_sort_error_rows", 0)), "Ask depth sort error rows"),
            ("phase318_depth_beyond_l1_material_rows", as_int(row.get("depth_beyond_l1_material_rows", 0)), "Rows with depth levels 2-5 material"),
            ("phase318_strategy_search_allowed_now", 0, "No strategy search in Phase318"),
            ("phase318_strategy_replay_allowed", 0, "No replay"),
            ("phase318_strategy_promotion_allowed", 0, "No promotion"),
            ("phase318_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase318_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase318_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase318_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase318_next_best_action", NEXT_ACTION if complete else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, summary: pd.DataFrame, by_event: pd.DataFrame, by_symbol: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase318 Event-Catalyst Multi-Event Join Quality Audit",
        "",
        "Phase318 audits the Phase317 joined top-five market-by-price depth parquet. It does not run strategy search, replay, promotion, paper/live acceptance, or profitability claims.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Quality summary",
        "",
        _markdown_table(summary),
        "",
        "## Event coverage",
        "",
        _markdown_table(by_event),
        "",
        "## Symbol coverage",
        "",
        _markdown_table(by_symbol),
        "",
        "## Gates",
        "",
        _markdown_table(gates),
    ]
    (output_dir / "phase318_event_catalyst_multievent_join_quality_audit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase317_dir: Path = DEFAULT_PHASE317_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase317 = read_csv(phase317_dir / "phase317_acceptance_summary.csv")
    joined_path = parquet_path(phase317_dir)
    summary, by_event, by_symbol = run_duckdb_quality(joined_path)
    gates = build_gate_evaluation(phase317, joined_path, summary, by_event, by_symbol)
    acceptance = build_acceptance(summary, by_event, by_symbol, gates)

    summary.to_csv(output_dir / "phase318_join_quality_summary.csv", index=False)
    by_event.to_csv(output_dir / "phase318_join_event_coverage.csv", index=False)
    by_symbol.to_csv(output_dir / "phase318_join_symbol_coverage.csv", index=False)
    gates.to_csv(output_dir / "phase318_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase318_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, summary, by_event, by_symbol, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase318_event_catalyst_multievent_join_quality_audit",
        **reproducibility_fields(
            artifact_id="phase318",
            generated_utc=generated_utc,
            inputs={
                "phase317_acceptance": str(phase317_dir / "phase317_acceptance_summary.csv"),
                "phase317_joined_parquet": str(joined_path),
            },
            parameters={"duckdb_quality_audit": True, "depth_columns": DEPTH_COLUMNS},
            outputs={"acceptance_summary": str(output_dir / "phase318_acceptance_summary.csv")},
            cost_model_version="not_applicable_join_quality_audit_only",
            latency_model_version="not_applicable_join_quality_audit_only",
        ),
    }
    (output_dir / "phase318_event_catalyst_multievent_join_quality_audit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase318 multi-event joined top-five depth quality audit.")
    parser.add_argument("--phase317-dir", type=Path, default=DEFAULT_PHASE317_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase317_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
