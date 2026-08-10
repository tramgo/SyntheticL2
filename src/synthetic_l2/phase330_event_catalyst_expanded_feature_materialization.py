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


DEFAULT_JOINED_PATH = Path("outputs/phase327/phase327_joined_expanded_event_top5_depth.parquet")
DEFAULT_PHASE329_DIR = Path("outputs/phase329")
DEFAULT_OUTPUT_DIR = Path("outputs/phase330")

NEXT_ACTION = "run_phase331_event_catalyst_expanded_strategy_search_precommit_no_replay"
REPAIR_ACTION = "repair_phase330_event_catalyst_expanded_feature_materialization"

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
    l1_spread = "sell_1_price - buy_1_price"
    l1_mid = "(sell_1_price + buy_1_price) / 2.0"
    l1_microprice = "((sell_1_price * buy_1_quantity) + (buy_1_price * sell_1_quantity)) / NULLIF(buy_1_quantity + sell_1_quantity, 0)"
    l1_queue_imbalance = "(buy_1_quantity - sell_1_quantity) / NULLIF(buy_1_quantity + sell_1_quantity, 0)"
    depth_l1_l5_qty_imbalance = f"({qty_l1_l5_bid} - {qty_l1_l5_ask}) / NULLIF({qty_l1_l5_bid} + {qty_l1_l5_ask}, 0)"
    depth_l2_l5_qty_imbalance = f"({qty_l2_l5_bid} - {qty_l2_l5_ask}) / NULLIF({qty_l2_l5_bid} + {qty_l2_l5_ask}, 0)"
    depth_l1_l5_order_imbalance = f"({ord_l1_l5_bid} - {ord_l1_l5_ask}) / NULLIF({ord_l1_l5_bid} + {ord_l1_l5_ask}, 0)"
    depth_l2_l5_order_imbalance = f"({ord_l2_l5_bid} - {ord_l2_l5_ask}) / NULLIF({ord_l2_l5_bid} + {ord_l2_l5_ask}, 0)"
    bid_depth_slope_l1_l5 = "(buy_1_price - buy_5_price) / 4.0"
    ask_depth_slope_l1_l5 = "(sell_5_price - sell_1_price) / 4.0"
    l2_l5_depth_share = f"({qty_l2_l5_bid} + {qty_l2_l5_ask}) / NULLIF({qty_l1_l5_bid} + {qty_l1_l5_ask}, 0)"
    depth_pressure = f"(({qty_l1_l5_bid} - {qty_l1_l5_ask}) / NULLIF({qty_l1_l5_bid} + {qty_l1_l5_ask}, 0)) / GREATEST(sell_1_price - buy_1_price, 0.01)"
    depth_l2_l5_pressure = f"(({qty_l2_l5_bid} - {qty_l2_l5_ask}) / NULLIF({qty_l2_l5_bid} + {qty_l2_l5_ask}, 0)) / GREATEST(sell_1_price - buy_1_price, 0.01)"
    return f"""
WITH features AS (
    SELECT
        event_id,
        ANY_VALUE(event_time_ist) AS event_time_ist,
        ANY_VALUE(event_type) AS event_type,
        symbol,
        COUNT(*) AS source_tick_rows,
        MIN(relative_second) AS relative_second_min,
        MAX(relative_second) AS relative_second_max,
        MIN(last_price) AS min_last_price,
        MAX(last_price) AS max_last_price,
        AVG({l1_spread}) FILTER (WHERE relative_second < 0) AS pre900_l1_spread_avg,
        AVG({l1_microprice} - {l1_mid}) FILTER (WHERE relative_second < 0) AS pre900_microprice_minus_mid_avg,
        AVG({l1_queue_imbalance}) FILTER (WHERE relative_second < 0) AS pre900_l1_queue_imbalance_avg,
        AVG({depth_l1_l5_qty_imbalance}) FILTER (WHERE relative_second < 0) AS pre900_depth_l1_l5_qty_imbalance_avg,
        AVG({depth_l2_l5_qty_imbalance}) FILTER (WHERE relative_second < 0) AS pre900_depth_l2_l5_qty_imbalance_avg,
        AVG({depth_l1_l5_order_imbalance}) FILTER (WHERE relative_second < 0) AS pre900_depth_l1_l5_order_imbalance_avg,
        AVG({depth_l2_l5_order_imbalance}) FILTER (WHERE relative_second < 0) AS pre900_depth_l2_l5_order_imbalance_avg,
        AVG({bid_depth_slope_l1_l5}) FILTER (WHERE relative_second < 0) AS pre900_bid_depth_slope_l1_l5_avg,
        AVG({ask_depth_slope_l1_l5}) FILTER (WHERE relative_second < 0) AS pre900_ask_depth_slope_l1_l5_avg,
        AVG({l2_l5_depth_share}) FILTER (WHERE relative_second < 0) AS pre900_l2_l5_depth_share_avg,
        AVG({depth_pressure}) FILTER (WHERE relative_second < 0) AS pre900_depth_pressure_avg,
        AVG({depth_l2_l5_pressure}) FILTER (WHERE relative_second < 0) AS pre900_depth_l2_l5_pressure_avg,
        AVG({l1_spread}) FILTER (WHERE relative_second BETWEEN -300 AND -1) AS pre300_l1_spread_avg,
        AVG({l1_microprice} - {l1_mid}) FILTER (WHERE relative_second BETWEEN -300 AND -1) AS pre300_microprice_minus_mid_avg,
        AVG({l1_queue_imbalance}) FILTER (WHERE relative_second BETWEEN -300 AND -1) AS pre300_l1_queue_imbalance_avg,
        AVG({depth_l1_l5_qty_imbalance}) FILTER (WHERE relative_second BETWEEN -300 AND -1) AS pre300_depth_l1_l5_qty_imbalance_avg,
        AVG({depth_l2_l5_qty_imbalance}) FILTER (WHERE relative_second BETWEEN -300 AND -1) AS pre300_depth_l2_l5_qty_imbalance_avg,
        AVG({depth_l1_l5_order_imbalance}) FILTER (WHERE relative_second BETWEEN -300 AND -1) AS pre300_depth_l1_l5_order_imbalance_avg,
        AVG({depth_l2_l5_order_imbalance}) FILTER (WHERE relative_second BETWEEN -300 AND -1) AS pre300_depth_l2_l5_order_imbalance_avg,
        AVG({l2_l5_depth_share}) FILTER (WHERE relative_second BETWEEN -300 AND -1) AS pre300_l2_l5_depth_share_avg,
        AVG({depth_pressure}) FILTER (WHERE relative_second BETWEEN -300 AND -1) AS pre300_depth_pressure_avg,
        AVG({depth_l2_l5_pressure}) FILTER (WHERE relative_second BETWEEN -300 AND -1) AS pre300_depth_l2_l5_pressure_avg,
        ARG_MIN({l1_mid}, ABS(relative_second)) AS event_l1_mid,
        ARG_MIN({l1_spread}, ABS(relative_second)) AS event_l1_spread,
        ARG_MIN({l1_microprice}, ABS(relative_second)) AS event_l1_microprice,
        ARG_MIN({l1_queue_imbalance}, ABS(relative_second)) AS event_l1_queue_imbalance,
        ARG_MIN({depth_l1_l5_qty_imbalance}, ABS(relative_second)) AS event_depth_l1_l5_qty_imbalance,
        ARG_MIN({depth_l2_l5_qty_imbalance}, ABS(relative_second)) AS event_depth_l2_l5_qty_imbalance,
        ARG_MIN({depth_l1_l5_order_imbalance}, ABS(relative_second)) AS event_depth_l1_l5_order_imbalance,
        ARG_MIN({depth_l2_l5_order_imbalance}, ABS(relative_second)) AS event_depth_l2_l5_order_imbalance,
        ARG_MIN({l2_l5_depth_share}, ABS(relative_second)) AS event_l2_l5_depth_share,
        ARG_MIN({depth_pressure}, ABS(relative_second)) AS event_depth_pressure,
        ARG_MIN({depth_l2_l5_pressure}, ABS(relative_second)) AS event_depth_l2_l5_pressure,
        ARG_MIN({l1_mid}, ABS(relative_second - 60)) FILTER (WHERE relative_second >= 0) AS post60_mid,
        ARG_MIN({l1_mid}, ABS(relative_second - 300)) FILTER (WHERE relative_second >= 0) AS post300_mid,
        ARG_MIN({l1_mid}, ABS(relative_second - 900)) FILTER (WHERE relative_second >= 0) AS post900_mid,
        ARG_MIN({l1_mid}, ABS(relative_second - 1800)) FILTER (WHERE relative_second >= 0) AS post1800_mid,
        AVG({depth_pressure}) FILTER (WHERE relative_second BETWEEN 0 AND 300) AS post300_depth_pressure_avg
    FROM read_parquet('{source}')
    GROUP BY event_id, symbol
)
SELECT
    * EXCLUDE (post60_mid, post300_mid, post900_mid, post1800_mid, post300_depth_pressure_avg),
    10000.0 * (post60_mid - event_l1_mid) / NULLIF(event_l1_mid, 0) AS target_post_60s_mid_return_bps,
    10000.0 * (post300_mid - event_l1_mid) / NULLIF(event_l1_mid, 0) AS target_post_300s_mid_return_bps,
    10000.0 * (post900_mid - event_l1_mid) / NULLIF(event_l1_mid, 0) AS target_post_900s_mid_return_bps,
    10000.0 * (post1800_mid - event_l1_mid) / NULLIF(event_l1_mid, 0) AS target_post_1800s_mid_return_bps,
    post300_depth_pressure_avg - pre300_depth_pressure_avg AS target_post_300s_depth_pressure_shift
FROM features
ORDER BY event_id, symbol
"""


def materialize_feature_matrix(joined_path: Path) -> pd.DataFrame:
    con = duckdb.connect()
    try:
        con.execute("PRAGMA threads=4")
        return con.execute(feature_matrix_sql(joined_path)).fetchdf()
    finally:
        con.close()


def write_matrix_parquet(matrix: pd.DataFrame, output_path: Path) -> None:
    con = duckdb.connect()
    try:
        con.register("phase330_matrix", matrix)
        con.execute(f"COPY phase330_matrix TO '{parquet_sql_path(output_path)}' (FORMAT PARQUET)")
    finally:
        con.close()


def build_feature_quality(matrix: pd.DataFrame, joined_rows: int, parquet_path: Path) -> pd.DataFrame:
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
        ("joined_rows_expected", int(joined_rows), "Phase328 accepted joined rows."),
        ("joined_rows_represented", int(matrix["source_tick_rows"].sum()) if not matrix.empty else 0, "Source rows represented in matrix."),
        ("target_columns_used_as_live_features", int(sum(column in feature_columns for column in target_columns)), "Must remain zero."),
        ("matrix_parquet_written", int(parquet_path.exists()), "Feature matrix parquet was written."),
        ("matrix_parquet_bytes", int(parquet_path.stat().st_size) if parquet_path.exists() else 0, "Feature matrix parquet size in bytes."),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def build_gate_evaluation(phase329: pd.DataFrame, quality: pd.DataFrame) -> pd.DataFrame:
    q = {str(row.metric): row.value for row in quality.itertuples(index=False)}
    phase329_complete = as_int(metric_value(phase329, "phase329_expanded_feature_materialization_precommit_complete", 0))
    rows: list[tuple[str, bool, Any, Any]] = [
        ("P330_PHASE329_COMPLETE", phase329_complete == 1, phase329_complete, 1),
        ("P330_FEATURE_MATRIX_ROWS", as_int(q.get("feature_matrix_rows", 0)) == 1600, q.get("feature_matrix_rows", 0), 1600),
        ("P330_EVENT_BREADTH", as_int(q.get("event_rows", 0)) >= 50, q.get("event_rows", 0), ">=50"),
        ("P330_SYMBOL_BREADTH", as_int(q.get("symbol_rows", 0)) >= 32, q.get("symbol_rows", 0), ">=32"),
        ("P330_JOIN_ROWS_REPRESENTED", as_int(q.get("joined_rows_represented", 0)) == as_int(q.get("joined_rows_expected", -1)), f"{q.get('joined_rows_represented', 0)}/{q.get('joined_rows_expected', -1)}", "equal"),
        ("P330_MIN_RAW_TICKS_PRESENT", as_int(q.get("min_source_tick_rows_per_event_symbol", 0)) > 0, q.get("min_source_tick_rows_per_event_symbol", 0), ">0"),
        ("P330_LIVE_FEATURE_COLUMNS_PRESENT", as_int(q.get("live_feature_columns", 0)) >= 35, q.get("live_feature_columns", 0), ">=35"),
        ("P330_DEPTH_FEATURE_COLUMNS_PRESENT", as_int(q.get("depth_feature_columns", 0)) >= 20, q.get("depth_feature_columns", 0), ">=20"),
        ("P330_TARGET_COLUMNS_SEPARATED", as_int(q.get("target_columns", 0)) == 5 and as_int(q.get("target_columns_used_as_live_features", 1)) == 0, f"targets={q.get('target_columns', 0)};live_target_cols={q.get('target_columns_used_as_live_features', 1)}", "5_targets_and_0_live_targets"),
        ("P330_MATRIX_PARQUET_WRITTEN", as_int(q.get("matrix_parquet_written", 0)) == 1 and as_int(q.get("matrix_parquet_bytes", 0)) > 0, f"written={q.get('matrix_parquet_written', 0)};bytes={q.get('matrix_parquet_bytes', 0)}", "written_and_nonempty"),
        ("P330_NO_STRATEGY_SEARCH_OPENED", True, "strategy_search_allowed_now=0", 0),
        ("P330_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(matrix: pd.DataFrame, quality: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    q = {str(row.metric): row.value for row in quality.itertuples(index=False)}
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    complete = int(hard_pass == hard_rows)
    rows = [
        ("phase330_expanded_feature_materialization_complete", complete, "Phase330 expanded feature materialization completed"),
        ("phase330_feature_matrix_rows", int(len(matrix)), "Compact event-symbol feature matrix rows"),
        ("phase330_event_rows", as_int(q.get("event_rows", 0)), "Distinct events"),
        ("phase330_symbol_rows", as_int(q.get("symbol_rows", 0)), "Distinct symbols"),
        ("phase330_source_tick_rows", as_int(q.get("source_tick_rows", 0)), "Joined ticks represented"),
        ("phase330_min_source_tick_rows_per_event_symbol", as_int(q.get("min_source_tick_rows_per_event_symbol", 0)), "Minimum raw tick support per event-symbol row"),
        ("phase330_live_feature_columns", as_int(q.get("live_feature_columns", 0)), "Live feature columns"),
        ("phase330_depth_feature_columns", as_int(q.get("depth_feature_columns", 0)), "Depth-aware live feature columns"),
        ("phase330_target_columns", as_int(q.get("target_columns", 0)), "Separated target columns"),
        ("phase330_live_feature_null_cells", as_int(q.get("live_feature_null_cells", 0)), "Live feature null cells"),
        ("phase330_target_null_cells", as_int(q.get("target_null_cells", 0)), "Target null cells"),
        ("phase330_target_columns_used_as_live_features", as_int(q.get("target_columns_used_as_live_features", 0)), "Target columns used as live features"),
        ("phase330_matrix_parquet_written", as_int(q.get("matrix_parquet_written", 0)), "Feature matrix parquet written"),
        ("phase330_matrix_parquet_bytes", as_int(q.get("matrix_parquet_bytes", 0)), "Feature matrix parquet bytes"),
        ("phase330_full_depth_required", 1, "Depth levels 1-5 required"),
        ("phase330_depth_beyond_l1_required", 1, "Depth levels 2-5 materiality required"),
        ("phase330_l1_only_variant_rows_allowed", 0, "No L1-only variants allowed"),
        ("phase330_net_edge_live_mask_rows_allowed", 0, "No net-edge live lookahead mask allowed"),
        ("phase330_strategy_search_allowed_now", 0, "No strategy search in Phase330"),
        ("phase330_strategy_replay_allowed", 0, "No replay"),
        ("phase330_strategy_promotion_allowed", 0, "No promotion"),
        ("phase330_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase330_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        ("phase330_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase330_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase330_next_best_action", NEXT_ACTION if complete else REPAIR_ACTION, "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, quality: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase330 Event-Catalyst Expanded Feature Materialization",
        "",
        "Phase330 materializes a compact event-symbol feature matrix from the repaired Phase327 and accepted Phase328 top-five market-by-price depth join.",
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
    (output_dir / "phase330_event_catalyst_expanded_feature_materialization_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(joined_path: Path = DEFAULT_JOINED_PATH, phase329_dir: Path = DEFAULT_PHASE329_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase329 = read_csv(phase329_dir / "phase329_acceptance_summary.csv")
    joined_rows = 0
    if joined_path.exists():
        con = duckdb.connect()
        try:
            joined_rows = int(con.execute(f"SELECT COUNT(*) FROM read_parquet('{parquet_sql_path(joined_path)}')").fetchone()[0])
        finally:
            con.close()

    matrix = materialize_feature_matrix(joined_path) if joined_path.exists() else pd.DataFrame()
    parquet_path = output_dir / "phase330_event_catalyst_expanded_feature_matrix.parquet"
    if not matrix.empty:
        write_matrix_parquet(matrix, parquet_path)
    quality = build_feature_quality(matrix, joined_rows, parquet_path)
    gates = build_gate_evaluation(phase329, quality)
    acceptance = build_acceptance(matrix, quality, gates)

    matrix.to_csv(output_dir / "phase330_event_catalyst_expanded_feature_matrix.csv", index=False)
    quality.to_csv(output_dir / "phase330_feature_quality.csv", index=False)
    gates.to_csv(output_dir / "phase330_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase330_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, quality, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase330_event_catalyst_expanded_feature_materialization",
        **reproducibility_fields(
            artifact_id="phase330",
            generated_utc=generated_utc,
            inputs={
                "joined_parquet": str(joined_path),
                "phase329_acceptance": str(phase329_dir / "phase329_acceptance_summary.csv"),
            },
            parameters={"no_strategy_search": 1, "full_depth_required": 1, "target_separation_required": 1, "expected_feature_rows": 1600},
            outputs={
                "feature_matrix_parquet": str(parquet_path),
                "feature_matrix_csv": str(output_dir / "phase330_event_catalyst_expanded_feature_matrix.csv"),
            },
            cost_model_version="not_applicable_feature_materialization_only",
            latency_model_version="not_applicable_feature_materialization_only",
        ),
    }
    (output_dir / "phase330_event_catalyst_expanded_feature_materialization_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize Phase330 expanded event-catalyst feature matrix.")
    parser.add_argument("--joined-path", type=Path, default=DEFAULT_JOINED_PATH)
    parser.add_argument("--phase329-dir", type=Path, default=DEFAULT_PHASE329_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.joined_path, args.phase329_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
