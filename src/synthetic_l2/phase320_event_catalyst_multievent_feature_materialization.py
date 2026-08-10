from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_JOINED_PATH = Path("outputs/phase317/phase317_joined_multievent_top5_depth.parquet")
DEFAULT_PHASE319_DIR = Path("outputs/phase319")
DEFAULT_OUTPUT_DIR = Path("outputs/phase320")

NEXT_ACTION = "run_phase321_event_catalyst_multievent_strategy_search_precommit_no_replay"
REPAIR_ACTION = "repair_phase320_event_catalyst_multievent_feature_materialization"


IDENTITY_COLUMNS = ["event_id", "event_time_ist", "event_type", "symbol"]
TARGET_COLUMNS = [
    "target_post_60s_mid_return_bps",
    "target_post_300s_mid_return_bps",
    "target_post_900s_mid_return_bps",
    "target_post_1800s_mid_return_bps",
    "target_post_300s_depth_pressure_shift",
]


def parquet_sql_path(path: Path) -> str:
    return path.as_posix().replace("'", "''")


def feature_matrix_sql(joined_path: Path) -> str:
    source = parquet_sql_path(joined_path)
    qty_l1_l5_bid = "COALESCE(buy_1_quantity,0)+COALESCE(buy_2_quantity,0)+COALESCE(buy_3_quantity,0)+COALESCE(buy_4_quantity,0)+COALESCE(buy_5_quantity,0)"
    qty_l1_l5_ask = "COALESCE(sell_1_quantity,0)+COALESCE(sell_2_quantity,0)+COALESCE(sell_3_quantity,0)+COALESCE(sell_4_quantity,0)+COALESCE(sell_5_quantity,0)"
    qty_l2_l5_bid = "COALESCE(buy_2_quantity,0)+COALESCE(buy_3_quantity,0)+COALESCE(buy_4_quantity,0)+COALESCE(buy_5_quantity,0)"
    qty_l2_l5_ask = "COALESCE(sell_2_quantity,0)+COALESCE(sell_3_quantity,0)+COALESCE(sell_4_quantity,0)+COALESCE(sell_5_quantity,0)"
    ord_l1_l5_bid = "COALESCE(buy_1_orders,0)+COALESCE(buy_2_orders,0)+COALESCE(buy_3_orders,0)+COALESCE(buy_4_orders,0)+COALESCE(buy_5_orders,0)"
    ord_l1_l5_ask = "COALESCE(sell_1_orders,0)+COALESCE(sell_2_orders,0)+COALESCE(sell_3_orders,0)+COALESCE(sell_4_orders,0)+COALESCE(sell_5_orders,0)"
    ord_l2_l5_bid = "COALESCE(buy_2_orders,0)+COALESCE(buy_3_orders,0)+COALESCE(buy_4_orders,0)+COALESCE(buy_5_orders,0)"
    ord_l2_l5_ask = "COALESCE(sell_2_orders,0)+COALESCE(sell_3_orders,0)+COALESCE(sell_4_orders,0)+COALESCE(sell_5_orders,0)"
    return f"""
WITH raw AS (
    SELECT * FROM read_parquet('{source}')
),
ticks AS (
    SELECT
        event_id,
        event_time_ist,
        event_type,
        symbol,
        relative_second,
        last_price,
        volume_traded,
        sell_1_price - buy_1_price AS l1_spread,
        (sell_1_price + buy_1_price) / 2.0 AS l1_mid,
        ((sell_1_price * buy_1_quantity) + (buy_1_price * sell_1_quantity)) / NULLIF(buy_1_quantity + sell_1_quantity, 0) AS l1_microprice,
        (buy_1_quantity - sell_1_quantity) / NULLIF(buy_1_quantity + sell_1_quantity, 0) AS l1_queue_imbalance,
        ({qty_l1_l5_bid} - {qty_l1_l5_ask}) / NULLIF({qty_l1_l5_bid} + {qty_l1_l5_ask}, 0) AS depth_l1_l5_qty_imbalance,
        ({qty_l2_l5_bid} - {qty_l2_l5_ask}) / NULLIF({qty_l2_l5_bid} + {qty_l2_l5_ask}, 0) AS depth_l2_l5_qty_imbalance,
        ({ord_l1_l5_bid} - {ord_l1_l5_ask}) / NULLIF({ord_l1_l5_bid} + {ord_l1_l5_ask}, 0) AS depth_l1_l5_order_imbalance,
        ({ord_l2_l5_bid} - {ord_l2_l5_ask}) / NULLIF({ord_l2_l5_bid} + {ord_l2_l5_ask}, 0) AS depth_l2_l5_order_imbalance,
        (buy_1_price - buy_5_price) / 4.0 AS bid_depth_slope_l1_l5,
        (sell_5_price - sell_1_price) / 4.0 AS ask_depth_slope_l1_l5,
        ({qty_l2_l5_bid} + {qty_l2_l5_ask}) / NULLIF({qty_l1_l5_bid} + {qty_l1_l5_ask}, 0) AS l2_l5_depth_share,
        (({qty_l1_l5_bid} - {qty_l1_l5_ask}) / NULLIF({qty_l1_l5_bid} + {qty_l1_l5_ask}, 0)) / GREATEST(sell_1_price - buy_1_price, 0.01) AS depth_pressure,
        (({qty_l2_l5_bid} - {qty_l2_l5_ask}) / NULLIF({qty_l2_l5_bid} + {qty_l2_l5_ask}, 0)) / GREATEST(sell_1_price - buy_1_price, 0.01) AS depth_l2_l5_pressure
    FROM raw
),
base AS (
    SELECT
        event_id,
        ANY_VALUE(event_time_ist) AS event_time_ist,
        ANY_VALUE(event_type) AS event_type,
        symbol,
        COUNT(*) AS source_tick_rows,
        MIN(relative_second) AS relative_second_min,
        MAX(relative_second) AS relative_second_max,
        MIN(last_price) AS min_last_price,
        MAX(last_price) AS max_last_price
    FROM ticks
    GROUP BY event_id, symbol
),
pre900 AS (
    SELECT
        event_id,
        symbol,
        AVG(l1_spread) AS pre900_l1_spread_avg,
        AVG(l1_microprice - l1_mid) AS pre900_microprice_minus_mid_avg,
        AVG(l1_queue_imbalance) AS pre900_l1_queue_imbalance_avg,
        AVG(depth_l1_l5_qty_imbalance) AS pre900_depth_l1_l5_qty_imbalance_avg,
        AVG(depth_l2_l5_qty_imbalance) AS pre900_depth_l2_l5_qty_imbalance_avg,
        AVG(depth_l1_l5_order_imbalance) AS pre900_depth_l1_l5_order_imbalance_avg,
        AVG(depth_l2_l5_order_imbalance) AS pre900_depth_l2_l5_order_imbalance_avg,
        AVG(bid_depth_slope_l1_l5) AS pre900_bid_depth_slope_l1_l5_avg,
        AVG(ask_depth_slope_l1_l5) AS pre900_ask_depth_slope_l1_l5_avg,
        AVG(l2_l5_depth_share) AS pre900_l2_l5_depth_share_avg,
        AVG(depth_pressure) AS pre900_depth_pressure_avg,
        AVG(depth_l2_l5_pressure) AS pre900_depth_l2_l5_pressure_avg
    FROM ticks
    WHERE relative_second < 0
    GROUP BY event_id, symbol
),
pre300 AS (
    SELECT
        event_id,
        symbol,
        AVG(l1_spread) AS pre300_l1_spread_avg,
        AVG(l1_microprice - l1_mid) AS pre300_microprice_minus_mid_avg,
        AVG(l1_queue_imbalance) AS pre300_l1_queue_imbalance_avg,
        AVG(depth_l1_l5_qty_imbalance) AS pre300_depth_l1_l5_qty_imbalance_avg,
        AVG(depth_l2_l5_qty_imbalance) AS pre300_depth_l2_l5_qty_imbalance_avg,
        AVG(depth_l1_l5_order_imbalance) AS pre300_depth_l1_l5_order_imbalance_avg,
        AVG(depth_l2_l5_order_imbalance) AS pre300_depth_l2_l5_order_imbalance_avg,
        AVG(l2_l5_depth_share) AS pre300_l2_l5_depth_share_avg,
        AVG(depth_pressure) AS pre300_depth_pressure_avg,
        AVG(depth_l2_l5_pressure) AS pre300_depth_l2_l5_pressure_avg
    FROM ticks
    WHERE relative_second BETWEEN -300 AND -1
    GROUP BY event_id, symbol
),
snap AS (
    SELECT
        event_id,
        symbol,
        ARG_MIN(l1_mid, ABS(relative_second)) AS event_l1_mid,
        ARG_MIN(l1_spread, ABS(relative_second)) AS event_l1_spread,
        ARG_MIN(l1_microprice, ABS(relative_second)) AS event_l1_microprice,
        ARG_MIN(l1_queue_imbalance, ABS(relative_second)) AS event_l1_queue_imbalance,
        ARG_MIN(depth_l1_l5_qty_imbalance, ABS(relative_second)) AS event_depth_l1_l5_qty_imbalance,
        ARG_MIN(depth_l2_l5_qty_imbalance, ABS(relative_second)) AS event_depth_l2_l5_qty_imbalance,
        ARG_MIN(depth_l1_l5_order_imbalance, ABS(relative_second)) AS event_depth_l1_l5_order_imbalance,
        ARG_MIN(depth_l2_l5_order_imbalance, ABS(relative_second)) AS event_depth_l2_l5_order_imbalance,
        ARG_MIN(l2_l5_depth_share, ABS(relative_second)) AS event_l2_l5_depth_share,
        ARG_MIN(depth_pressure, ABS(relative_second)) AS event_depth_pressure,
        ARG_MIN(depth_l2_l5_pressure, ABS(relative_second)) AS event_depth_l2_l5_pressure
    FROM ticks
    GROUP BY event_id, symbol
),
post AS (
    SELECT
        event_id,
        symbol,
        ARG_MIN(l1_mid, ABS(relative_second - 60)) FILTER (WHERE relative_second >= 0) AS post60_mid,
        ARG_MIN(l1_mid, ABS(relative_second - 300)) FILTER (WHERE relative_second >= 0) AS post300_mid,
        ARG_MIN(l1_mid, ABS(relative_second - 900)) FILTER (WHERE relative_second >= 0) AS post900_mid,
        ARG_MIN(l1_mid, ABS(relative_second - 1800)) FILTER (WHERE relative_second >= 0) AS post1800_mid,
        AVG(depth_pressure) FILTER (WHERE relative_second BETWEEN 0 AND 300) AS post300_depth_pressure_avg
    FROM ticks
    GROUP BY event_id, symbol
)
SELECT
    b.*,
    p900.* EXCLUDE (event_id, symbol),
    p300.* EXCLUDE (event_id, symbol),
    s.* EXCLUDE (event_id, symbol),
    10000.0 * (p.post60_mid - s.event_l1_mid) / NULLIF(s.event_l1_mid, 0) AS target_post_60s_mid_return_bps,
    10000.0 * (p.post300_mid - s.event_l1_mid) / NULLIF(s.event_l1_mid, 0) AS target_post_300s_mid_return_bps,
    10000.0 * (p.post900_mid - s.event_l1_mid) / NULLIF(s.event_l1_mid, 0) AS target_post_900s_mid_return_bps,
    10000.0 * (p.post1800_mid - s.event_l1_mid) / NULLIF(s.event_l1_mid, 0) AS target_post_1800s_mid_return_bps,
    p.post300_depth_pressure_avg - p300.pre300_depth_pressure_avg AS target_post_300s_depth_pressure_shift
FROM base b
LEFT JOIN pre900 p900 USING (event_id, symbol)
LEFT JOIN pre300 p300 USING (event_id, symbol)
LEFT JOIN snap s USING (event_id, symbol)
LEFT JOIN post p USING (event_id, symbol)
ORDER BY event_id, symbol
"""


def materialize_feature_matrix(joined_path: Path) -> pd.DataFrame:
    con = duckdb.connect()
    try:
        con.execute("PRAGMA threads=4")
        return con.execute(feature_matrix_sql(joined_path)).fetchdf()
    finally:
        con.close()


def build_feature_quality(matrix: pd.DataFrame, joined_rows: int) -> pd.DataFrame:
    feature_columns = [column for column in matrix.columns if column not in IDENTITY_COLUMNS and not column.startswith("target_")]
    depth_columns = [column for column in feature_columns if "depth" in column or "l2_l5" in column]
    target_columns = [column for column in matrix.columns if column.startswith("target_")]
    rows = [
        ("feature_matrix_rows", int(len(matrix)), "Expected compact event-symbol rows."),
        ("event_rows", int(matrix["event_id"].nunique()) if not matrix.empty else 0, "Distinct events."),
        ("symbol_rows", int(matrix["symbol"].nunique()) if not matrix.empty else 0, "Distinct symbols."),
        ("source_tick_rows", int(matrix["source_tick_rows"].sum()) if not matrix.empty else 0, "Joined ticks represented by the compact matrix."),
        ("min_source_tick_rows_per_event_symbol", int(matrix["source_tick_rows"].min()) if not matrix.empty else 0, "Minimum raw tick support per event-symbol row."),
        ("live_feature_columns", int(len(feature_columns)), "Columns available to live signal modeling."),
        ("depth_feature_columns", int(len(depth_columns)), "Live feature columns using depth levels 1-5 or 2-5."),
        ("target_columns", int(len(target_columns)), "Separated target/response columns."),
        ("live_feature_null_cells", int(matrix[feature_columns].isna().sum().sum()) if feature_columns else 0, "Null cells across live feature columns."),
        ("target_null_cells", int(matrix[target_columns].isna().sum().sum()) if target_columns else 0, "Null cells across target columns."),
        ("joined_rows_expected", int(joined_rows), "Phase318 accepted joined rows."),
        ("joined_rows_represented", int(matrix["source_tick_rows"].sum()) if not matrix.empty else 0, "Source rows represented in matrix."),
        ("target_columns_used_as_live_features", int(sum(column in feature_columns for column in target_columns)), "Must remain zero."),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def build_gate_evaluation(phase319: pd.DataFrame, quality: pd.DataFrame) -> pd.DataFrame:
    q = {str(row.metric): row.value for row in quality.itertuples(index=False)}
    phase319_complete = as_int(metric_value(phase319, "phase319_multievent_feature_materialization_precommit_complete", 0))
    rows: list[tuple[str, bool, Any, Any]] = [
        ("P320_PHASE319_COMPLETE", phase319_complete == 1, phase319_complete, 1),
        ("P320_FEATURE_MATRIX_ROWS", as_int(q.get("feature_matrix_rows", 0)) == 320, q.get("feature_matrix_rows", 0), 320),
        ("P320_EVENT_BREADTH", as_int(q.get("event_rows", 0)) >= 10, q.get("event_rows", 0), ">=10"),
        ("P320_SYMBOL_BREADTH", as_int(q.get("symbol_rows", 0)) >= 32, q.get("symbol_rows", 0), ">=32"),
        ("P320_JOIN_ROWS_REPRESENTED", as_int(q.get("joined_rows_represented", 0)) == as_int(q.get("joined_rows_expected", -1)), f"{q.get('joined_rows_represented', 0)}/{q.get('joined_rows_expected', -1)}", "equal"),
        ("P320_MIN_RAW_TICKS_PRESENT", as_int(q.get("min_source_tick_rows_per_event_symbol", 0)) > 0, q.get("min_source_tick_rows_per_event_symbol", 0), ">0"),
        ("P320_LIVE_FEATURE_COLUMNS_PRESENT", as_int(q.get("live_feature_columns", 0)) >= 35, q.get("live_feature_columns", 0), ">=35"),
        ("P320_DEPTH_FEATURE_COLUMNS_PRESENT", as_int(q.get("depth_feature_columns", 0)) >= 20, q.get("depth_feature_columns", 0), ">=20"),
        ("P320_TARGET_COLUMNS_SEPARATED", as_int(q.get("target_columns", 0)) == 5 and as_int(q.get("target_columns_used_as_live_features", 1)) == 0, f"targets={q.get('target_columns', 0)};live_target_cols={q.get('target_columns_used_as_live_features', 1)}", "5_targets_and_0_live_targets"),
        ("P320_NO_STRATEGY_SEARCH_OPENED", True, "strategy_search_allowed_now=0", 0),
        ("P320_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(matrix: pd.DataFrame, quality: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    q = {str(row.metric): row.value for row in quality.itertuples(index=False)}
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    complete = int(hard_pass == hard_rows)
    rows = [
        ("phase320_multievent_feature_materialization_complete", complete, "Phase320 multi-event feature materialization completed"),
        ("phase320_feature_matrix_rows", int(len(matrix)), "Compact event-symbol feature matrix rows"),
        ("phase320_event_rows", as_int(q.get("event_rows", 0)), "Distinct events"),
        ("phase320_symbol_rows", as_int(q.get("symbol_rows", 0)), "Distinct symbols"),
        ("phase320_source_tick_rows", as_int(q.get("source_tick_rows", 0)), "Joined ticks represented"),
        ("phase320_min_source_tick_rows_per_event_symbol", as_int(q.get("min_source_tick_rows_per_event_symbol", 0)), "Minimum raw tick support per event-symbol row"),
        ("phase320_live_feature_columns", as_int(q.get("live_feature_columns", 0)), "Live feature columns"),
        ("phase320_depth_feature_columns", as_int(q.get("depth_feature_columns", 0)), "Depth-aware live feature columns"),
        ("phase320_target_columns", as_int(q.get("target_columns", 0)), "Separated target columns"),
        ("phase320_live_feature_null_cells", as_int(q.get("live_feature_null_cells", 0)), "Live feature null cells"),
        ("phase320_target_null_cells", as_int(q.get("target_null_cells", 0)), "Target null cells"),
        ("phase320_target_columns_used_as_live_features", as_int(q.get("target_columns_used_as_live_features", 0)), "Target columns used as live features"),
        ("phase320_full_depth_required", 1, "Depth levels 1-5 required"),
        ("phase320_depth_beyond_l1_required", 1, "Depth levels 2-5 materiality required"),
        ("phase320_l1_only_variant_rows_allowed", 0, "No L1-only variants allowed"),
        ("phase320_net_edge_live_mask_rows_allowed", 0, "No net-edge live lookahead mask allowed"),
        ("phase320_strategy_search_allowed_now", 0, "No strategy search in Phase320"),
        ("phase320_strategy_replay_allowed", 0, "No replay"),
        ("phase320_strategy_promotion_allowed", 0, "No promotion"),
        ("phase320_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase320_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        ("phase320_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase320_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase320_next_best_action", NEXT_ACTION if complete else REPAIR_ACTION, "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, quality: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase320 Event-Catalyst Multi-Event Feature Materialization",
        "",
        "Phase320 materializes a compact event-symbol feature matrix from the accepted Phase317/318 top-five market-by-price depth join.",
        "It keeps target response columns separated from live signal columns and does not run strategy search, replay, promotion, paper/live acceptance, or profitability claims.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Feature quality",
        "",
        _markdown_table(quality),
        "",
        "## Gates",
        "",
        _markdown_table(gates),
    ]
    (output_dir / "phase320_event_catalyst_multievent_feature_materialization_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(joined_path: Path = DEFAULT_JOINED_PATH, phase319_dir: Path = DEFAULT_PHASE319_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase319 = read_csv(phase319_dir / "phase319_acceptance_summary.csv")
    joined_rows = 0
    if joined_path.exists():
        con = duckdb.connect()
        try:
            joined_rows = int(con.execute(f"SELECT COUNT(*) FROM read_parquet('{parquet_sql_path(joined_path)}')").fetchone()[0])
        finally:
            con.close()

    matrix = materialize_feature_matrix(joined_path) if joined_path.exists() else pd.DataFrame()
    quality = build_feature_quality(matrix, joined_rows)
    gates = build_gate_evaluation(phase319, quality)
    acceptance = build_acceptance(matrix, quality, gates)

    matrix.to_csv(output_dir / "phase320_event_catalyst_multievent_feature_matrix.csv", index=False)
    quality.to_csv(output_dir / "phase320_feature_quality.csv", index=False)
    gates.to_csv(output_dir / "phase320_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase320_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, quality, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase320_event_catalyst_multievent_feature_materialization",
        **reproducibility_fields(
            artifact_id="phase320",
            generated_utc=generated_utc,
            inputs={
                "joined_parquet": str(joined_path),
                "phase319_acceptance": str(phase319_dir / "phase319_acceptance_summary.csv"),
            },
            parameters={"no_strategy_search": 1, "full_depth_required": 1, "target_separation_required": 1},
            outputs={"feature_matrix": str(output_dir / "phase320_event_catalyst_multievent_feature_matrix.csv")},
            cost_model_version="not_applicable_feature_materialization_only",
            latency_model_version="not_applicable_feature_materialization_only",
        ),
    }
    (output_dir / "phase320_event_catalyst_multievent_feature_materialization_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize Phase320 multi-event feature matrix.")
    parser.add_argument("--joined-path", type=Path, default=DEFAULT_JOINED_PATH)
    parser.add_argument("--phase319-dir", type=Path, default=DEFAULT_PHASE319_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.joined_path, args.phase319_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
