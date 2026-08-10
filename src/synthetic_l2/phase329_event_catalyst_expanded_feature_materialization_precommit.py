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


DEFAULT_PHASE328_DIR = Path("outputs/phase328")
DEFAULT_OUTPUT_DIR = Path("outputs/phase329")

NEXT_ACTION = "run_phase330_event_catalyst_expanded_feature_materialization_no_strategy_search"
REPAIR_ACTION = "repair_phase329_event_catalyst_expanded_feature_materialization_precommit"


def build_feature_catalog() -> pd.DataFrame:
    rows = [
        ("event_clock_relative_second", "relative_second", "event_clock", "Event-relative second from -900 through +1800.", "context", 1, 0, 0),
        ("l1_spread", "sell_1_price - buy_1_price", "top_of_book_l1", "Best bid/ask spread.", "signal", 1, 0, 0),
        ("l1_mid", "(sell_1_price + buy_1_price) / 2", "top_of_book_l1", "Best bid/ask midpoint.", "signal", 1, 0, 0),
        ("l1_microprice", "weighted best quote by opposite-side quantity", "top_of_book_l1", "Best-level microprice.", "signal", 1, 0, 0),
        ("l1_queue_imbalance", "(buy_1_quantity - sell_1_quantity) / total_l1_qty", "top_of_book_l1", "Best-level quantity imbalance.", "signal", 1, 0, 0),
        ("depth_l1_l5_qty_imbalance", "sum_qty_bid_l1_l5 vs sum_qty_ask_l1_l5", "top_five_depth", "Quantity imbalance across Zerodha visible market-by-price levels 1-5.", "signal", 1, 1, 0),
        ("depth_l2_l5_qty_imbalance", "sum_qty_bid_l2_l5 vs sum_qty_ask_l2_l5", "top_five_depth_beyond_l1", "Quantity imbalance across visible depth levels 2-5.", "signal", 1, 1, 0),
        ("depth_l1_l5_order_imbalance", "sum_orders_bid_l1_l5 vs sum_orders_ask_l1_l5", "top_five_depth", "Order-count imbalance across Zerodha visible market-by-price levels 1-5.", "signal", 1, 1, 0),
        ("depth_l2_l5_order_imbalance", "sum_orders_bid_l2_l5 vs sum_orders_ask_l2_l5", "top_five_depth_beyond_l1", "Order-count imbalance across visible depth levels 2-5.", "signal", 1, 1, 0),
        ("bid_depth_slope_l1_l5", "buy_1_price - buy_5_price", "top_five_depth", "Bid-side price ladder slope across levels 1-5.", "signal", 1, 1, 0),
        ("ask_depth_slope_l1_l5", "sell_5_price - sell_1_price", "top_five_depth", "Ask-side price ladder slope across levels 1-5.", "signal", 1, 1, 0),
        ("l2_l5_depth_share", "depth_l2_l5_qty / depth_l1_l5_qty", "top_five_depth_beyond_l1", "Share of displayed quantity beyond best bid/ask.", "signal", 1, 1, 0),
        ("depth_pressure", "depth_l1_l5_qty_imbalance / max(l1_spread,tick)", "top_five_depth", "Full visible-depth imbalance normalized by spread.", "signal", 1, 1, 0),
        ("depth_l2_l5_pressure", "depth_l2_l5_qty_imbalance / max(l1_spread,tick)", "top_five_depth_beyond_l1", "Levels 2-5 imbalance normalized by spread.", "signal", 1, 1, 0),
        ("pre_900s_mean_features", "mean(signal features where relative_second < 0)", "pre_event_context", "Pre-event feature means over the full 900s lead-in.", "signal", 1, 1, 0),
        ("pre_300s_mean_features", "mean(signal features where -300 <= relative_second < 0)", "pre_event_context", "Near-event feature means over the last 300s before the event.", "signal", 1, 1, 0),
        ("event_nearest_features", "nearest row to relative_second=0", "event_context", "At-event feature snapshot.", "signal", 1, 1, 0),
        ("pre_post_pressure_delta_diagnostic", "post depth_pressure minus pre depth_pressure", "diagnostic", "Pressure shift diagnostic separated from live entry features unless explicitly treated as a target.", "diagnostic", 1, 1, 1),
        ("post_60s_response", "midpoint return at +60s from event_mid", "target_response", "Short response target, excluded from live signal features.", "target", 1, 0, 1),
        ("post_300s_response", "midpoint return at +300s from event_mid", "target_response", "Five-minute response target, excluded from live signal features.", "target", 1, 0, 1),
        ("post_900s_response", "midpoint return at +900s from event_mid", "target_response", "Fifteen-minute response target, excluded from live signal features.", "target", 1, 0, 1),
        ("post_1800s_response", "midpoint return at +1800s from event_mid", "target_response", "Thirty-minute response target, excluded from live signal features.", "target", 1, 0, 1),
        ("post_depth_pressure_shift", "post depth_pressure minus pre depth_pressure", "target_response", "Liquidity-pressure response target, excluded from live signal features.", "target", 1, 1, 1),
    ]
    return pd.DataFrame(
        rows,
        columns=[
            "feature_id",
            "formula",
            "feature_family",
            "description",
            "feature_role",
            "phase330_materialization_required",
            "uses_depth_beyond_l1",
            "lookahead_target_only",
        ],
    )


def build_materialization_contract(phase328: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("P329_INPUT_JOIN", "outputs/phase327/phase327_joined_expanded_event_top5_depth.parquet", "Use the repaired and Phase328-audited expanded joined parquet."),
        ("P329_INPUT_QUALITY", "outputs/phase328/phase328_acceptance_summary.csv", "Require Phase328 quality audit before feature materialization."),
        ("P329_MIN_JOIN_ROWS", str(metric_value(phase328, "phase328_joined_rows", "")), "Preserve Phase328 audited joined-row count unless Phase327 is rerun."),
        ("P329_EVENT_SYMBOL_SCOPE", "50_events_x_32_symbols", "Feature matrix should produce one compact row per event and symbol."),
        ("P329_EXPECTED_FEATURE_ROWS", "1600", "One compact feature row per event-symbol pair."),
        ("P329_WINDOW", "relative_second=-900..1800", "Use only the audited event-relative window."),
        ("P329_FULL_DEPTH_REQUIRED", "zerodha_visible_depth_levels_1_to_5", "Retain full Zerodha top-five market-by-price depth."),
        ("P329_DEPTH_BEYOND_L1_REQUIRED", "visible_depth_levels_2_to_5_material", "Feature matrix must include material depth-beyond-L1 features."),
        ("P329_NO_L1_ONLY_VARIANTS", "l1_only_variant_rows=0", "No downstream strategy family may use only top-of-book fields."),
        ("P329_TARGET_SEPARATION", "target_columns_not_live_signal_features", "Post-event returns and pressure shifts must be targets/diagnostics, not live signal inputs."),
        ("P329_NO_NET_EDGE_LIVE_MASK", "net_edge_live_mask_rows=0", "No future outcome mask may be used to select live rows."),
        ("P329_NO_STRATEGY_SEARCH", "strategy_search_allowed_now=0", "Precommit only; no P&L, replay or optimization."),
        ("P329_BOUNDARIES", "replay=0;promotion=0;paper=0;claim=0", "No acceptance boundary changes."),
        ("P329_NEXT", NEXT_ACTION, "Materialize compact expanded feature matrix next."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_processing_work_order() -> pd.DataFrame:
    rows = [
        ("load_joined_parquet", "DuckDB scan over outputs/phase327/phase327_joined_expanded_event_top5_depth.parquet", "Avoid loading all 141.7M joined rows into pandas at once."),
        ("derive_tick_features", "SQL expressions for spread, mid, microprice, depth imbalances, depth slopes and pressure", "Use Zerodha visible levels 1-5 and depth-beyond-L1 levels 2-5."),
        ("aggregate_signal_features", "group by event_id,event_time_ist,event_type,symbol", "Produce compact event-symbol feature rows."),
        ("preserve_event_symbol_breadth", "expect 50 events x 32 symbols = 1600 rows", "Reject partial event-symbol feature coverage."),
        ("separate_targets", "post_60s/post_300s/post_900s/post_1800s response columns", "Keep target columns explicitly outside live feature set."),
        ("write_outputs", "outputs/phase330/phase330_event_catalyst_expanded_feature_matrix.parquet", "Feature materialization target."),
        ("quality_audit", "outputs/phase330/phase330_feature_quality.csv", "Validate full-depth features, target separation and 50x32 coverage."),
    ]
    return pd.DataFrame(rows, columns=["work_order_id", "scope", "description"])


def build_gate_evaluation(phase328: pd.DataFrame, features: pd.DataFrame, contract: pd.DataFrame, work_order: pd.DataFrame) -> pd.DataFrame:
    phase328_complete = as_int(metric_value(phase328, "phase328_expanded_join_quality_audit_complete", 0))
    feature_depth_rows = int(features["uses_depth_beyond_l1"].astype(int).sum()) if not features.empty else 0
    target_rows = int(features["lookahead_target_only"].astype(int).sum()) if not features.empty else 0
    rows: list[tuple[str, bool, Any, Any]] = [
        ("P329_PHASE328_COMPLETE", phase328_complete == 1, phase328_complete, 1),
        ("P329_PHASE328_JOIN_BREADTH_OK", as_int(metric_value(phase328, "phase328_event_rows", 0)) >= 50 and as_int(metric_value(phase328, "phase328_symbol_rows", 0)) >= 32 and as_int(metric_value(phase328, "phase328_min_event_symbol_coverage", 0)) >= 32 and as_int(metric_value(phase328, "phase328_min_symbol_event_coverage", 0)) >= 50, f"events={metric_value(phase328, 'phase328_event_rows', '')};symbols={metric_value(phase328, 'phase328_symbol_rows', '')};min_event_symbols={metric_value(phase328, 'phase328_min_event_symbol_coverage', '')};min_symbol_events={metric_value(phase328, 'phase328_min_symbol_event_coverage', '')}", "50_events_x_32_symbols"),
        ("P329_PHASE328_DEPTH_OK", as_int(metric_value(phase328, "phase328_depth_beyond_l1_material_rows", 0)) == as_int(metric_value(phase328, "phase328_joined_rows", -1)), metric_value(phase328, "phase328_depth_beyond_l1_material_rows", ""), "all_joined_rows"),
        ("P329_PHASE328_BOOK_QUALITY_OK", as_int(metric_value(phase328, "phase328_crossed_or_locked_l1_rows", 1)) == 0 and as_int(metric_value(phase328, "phase328_bid_depth_sort_error_rows", 1)) == 0 and as_int(metric_value(phase328, "phase328_ask_depth_sort_error_rows", 1)) == 0, f"crossed={metric_value(phase328, 'phase328_crossed_or_locked_l1_rows', '')};bid_sort={metric_value(phase328, 'phase328_bid_depth_sort_error_rows', '')};ask_sort={metric_value(phase328, 'phase328_ask_depth_sort_error_rows', '')}", 0),
        ("P329_FEATURE_CATALOG_NONEMPTY", len(features) > 0, len(features), ">0"),
        ("P329_DEPTH_BEYOND_L1_FEATURES_PRESENT", feature_depth_rows >= 9, feature_depth_rows, ">=9"),
        ("P329_TARGET_COLUMNS_SEPARATED", target_rows >= 6, target_rows, ">=6"),
        ("P329_CONTRACT_ROWS_PRESENT", len(contract) >= 14, len(contract), ">=14"),
        ("P329_WORK_ORDER_ROWS_PRESENT", len(work_order) >= 7, len(work_order), ">=7"),
        ("P329_NO_STRATEGY_SEARCH_OPENED", True, "strategy_search_allowed_now=0", 0),
        ("P329_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(features: pd.DataFrame, contract: pd.DataFrame, work_order: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    complete = int(hard_pass == hard_rows)
    return pd.DataFrame(
        [
            ("phase329_expanded_feature_materialization_precommit_complete", complete, "Phase329 expanded feature materialization precommit completed"),
            ("phase329_feature_catalog_rows", int(len(features)), "Feature catalog rows"),
            ("phase329_depth_beyond_l1_feature_rows", int(features["uses_depth_beyond_l1"].astype(int).sum()) if not features.empty else 0, "Feature rows using visible depth levels 2-5"),
            ("phase329_lookahead_target_only_rows", int(features["lookahead_target_only"].astype(int).sum()) if not features.empty else 0, "Target-only lookahead columns explicitly separated"),
            ("phase329_materialization_contract_rows", int(len(contract)), "Materialization contract rows"),
            ("phase329_processing_work_order_rows", int(len(work_order)), "Processing work-order rows"),
            ("phase329_expected_feature_rows", 1600, "Expected event-symbol feature rows for Phase330"),
            ("phase329_full_depth_required", 1, "Zerodha visible levels 1-5 required"),
            ("phase329_depth_beyond_l1_required", 1, "Visible levels 2-5 materiality required"),
            ("phase329_l1_only_variant_rows_allowed", 0, "No L1-only variants allowed"),
            ("phase329_net_edge_live_mask_rows_allowed", 0, "No net-edge live lookahead mask allowed"),
            ("phase329_strategy_search_allowed_now", 0, "No strategy search in Phase329"),
            ("phase329_strategy_replay_allowed", 0, "No replay"),
            ("phase329_strategy_promotion_allowed", 0, "No promotion"),
            ("phase329_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase329_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase329_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase329_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase329_next_best_action", NEXT_ACTION if complete else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, features: pd.DataFrame, contract: pd.DataFrame, work_order: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase329 Event-Catalyst Expanded Feature Materialization Precommit",
        "",
        "Phase329 precommits compact event-symbol feature materialization from the repaired Phase327 and accepted Phase328 expanded top-five-depth join.",
        "It does not materialize features, run strategy search, replay, promote, or claim profitability.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Feature catalog",
        "",
        _markdown_table(features),
        "",
        "## Materialization contract",
        "",
        _markdown_table(contract),
        "",
        "## Processing work order",
        "",
        _markdown_table(work_order),
        "",
        "## Gates",
        "",
        _markdown_table(gates),
    ]
    (output_dir / "phase329_event_catalyst_expanded_feature_materialization_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase328_dir: Path = DEFAULT_PHASE328_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase328 = read_csv(phase328_dir / "phase328_acceptance_summary.csv")
    features = build_feature_catalog()
    contract = build_materialization_contract(phase328)
    work_order = build_processing_work_order()
    gates = build_gate_evaluation(phase328, features, contract, work_order)
    acceptance = build_acceptance(features, contract, work_order, gates)

    features.to_csv(output_dir / "phase329_expanded_feature_catalog.csv", index=False)
    contract.to_csv(output_dir / "phase329_feature_materialization_contract.csv", index=False)
    work_order.to_csv(output_dir / "phase329_processing_work_order.csv", index=False)
    gates.to_csv(output_dir / "phase329_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase329_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, features, contract, work_order, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase329_event_catalyst_expanded_feature_materialization_precommit",
        **reproducibility_fields(
            artifact_id="phase329",
            generated_utc=generated_utc,
            inputs={"phase328_acceptance": str(phase328_dir / "phase328_acceptance_summary.csv")},
            parameters={"no_strategy_search": 1, "full_depth_required": 1, "target_separation_required": 1, "expected_feature_rows": 1600},
            outputs={"acceptance_summary": str(output_dir / "phase329_acceptance_summary.csv")},
            cost_model_version="not_applicable_feature_precommit_only",
            latency_model_version="not_applicable_feature_precommit_only",
        ),
    }
    (output_dir / "phase329_event_catalyst_expanded_feature_materialization_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Precommit Phase329 expanded feature materialization.")
    parser.add_argument("--phase328-dir", type=Path, default=DEFAULT_PHASE328_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase328_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
