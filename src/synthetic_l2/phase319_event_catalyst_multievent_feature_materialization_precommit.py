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


DEFAULT_PHASE318_DIR = Path("outputs/phase318")
DEFAULT_OUTPUT_DIR = Path("outputs/phase319")

NEXT_ACTION = "run_phase320_event_catalyst_multievent_feature_materialization_no_strategy_search"
REPAIR_ACTION = "repair_phase319_event_catalyst_multievent_feature_materialization_precommit"


def build_feature_catalog() -> pd.DataFrame:
    rows = [
        ("event_clock_relative_second", "relative_second", "event_clock", "Event-relative second from -900 through +1800.", "context", 1, 0, 0),
        ("l1_spread", "sell_1_price - buy_1_price", "top_of_book", "Best bid/ask spread.", "signal", 1, 0, 0),
        ("l1_mid", "(sell_1_price + buy_1_price) / 2", "top_of_book", "Best bid/ask midpoint.", "signal", 1, 0, 0),
        ("l1_microprice", "weighted best quote by opposite-side quantity", "top_of_book", "Best-level microprice.", "signal", 1, 0, 0),
        ("l1_queue_imbalance", "(buy_1_quantity - sell_1_quantity) / total_l1_qty", "top_of_book", "Best-level quantity imbalance.", "signal", 1, 0, 0),
        ("depth_l1_l5_qty_imbalance", "sum_qty_bid_l1_l5 vs sum_qty_ask_l1_l5", "full_depth", "Quantity imbalance across depth levels 1-5.", "signal", 1, 1, 0),
        ("depth_l2_l5_qty_imbalance", "sum_qty_bid_l2_l5 vs sum_qty_ask_l2_l5", "depth_beyond_l1", "Quantity imbalance across depth levels 2-5.", "signal", 1, 1, 0),
        ("depth_l1_l5_order_imbalance", "sum_orders_bid_l1_l5 vs sum_orders_ask_l1_l5", "full_depth", "Order-count imbalance across depth levels 1-5.", "signal", 1, 1, 0),
        ("depth_l2_l5_order_imbalance", "sum_orders_bid_l2_l5 vs sum_orders_ask_l2_l5", "depth_beyond_l1", "Order-count imbalance across depth levels 2-5.", "signal", 1, 1, 0),
        ("bid_depth_slope_l1_l5", "buy_1_price - buy_5_price", "full_depth", "Bid-side price ladder slope across depth levels 1-5.", "signal", 1, 1, 0),
        ("ask_depth_slope_l1_l5", "sell_5_price - sell_1_price", "full_depth", "Ask-side price ladder slope across depth levels 1-5.", "signal", 1, 1, 0),
        ("l2_l5_depth_share", "depth_l2_l5_qty / depth_l1_l5_qty", "depth_beyond_l1", "Share of displayed quantity beyond top of book.", "signal", 1, 1, 0),
        ("depth_pressure", "depth_l1_l5_qty_imbalance / max(l1_spread,tick)", "full_depth", "Full-depth imbalance normalized by spread.", "signal", 1, 1, 0),
        ("depth_l2_l5_pressure", "depth_l2_l5_qty_imbalance / max(l1_spread,tick)", "depth_beyond_l1", "Depth-beyond-L1 imbalance normalized by spread.", "signal", 1, 1, 0),
        ("pre_900s_mean_features", "mean(signal features where relative_second < 0)", "pre_event_context", "Pre-event feature means over the full 900s lead-in.", "signal", 1, 1, 0),
        ("pre_300s_mean_features", "mean(signal features where -300 <= relative_second < 0)", "pre_event_context", "Near-event feature means over the last 300s before the event.", "signal", 1, 1, 0),
        ("event_nearest_features", "nearest row to relative_second=0", "event_context", "At-event feature snapshot.", "signal", 1, 1, 0),
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
            "phase320_materialization_required",
            "uses_depth_beyond_l1",
            "lookahead_target_only",
        ],
    )


def build_materialization_contract() -> pd.DataFrame:
    rows = [
        ("P319_INPUT_JOIN", "outputs/phase317/phase317_joined_multievent_top5_depth.parquet", "Use the accepted local Phase317 joined parquet."),
        ("P319_INPUT_QUALITY", "outputs/phase318/phase318_acceptance_summary.csv", "Require Phase318 quality audit before feature materialization."),
        ("P319_MIN_JOIN_ROWS", "28350310", "Preserve Phase318 audited joined-row count unless Phase317 is rerun."),
        ("P319_EVENT_SYMBOL_SCOPE", "10_events_x_32_symbols", "Feature matrix should produce one compact row per event and symbol."),
        ("P319_WINDOW", "relative_second=-900..1800", "Use only the audited event-relative window."),
        ("P319_FULL_DEPTH_REQUIRED", "depth_levels_1_to_5", "Retain full Zerodha top-five market-by-price depth."),
        ("P319_DEPTH_BEYOND_L1_REQUIRED", "depth_levels_2_to_5_material", "Feature matrix must include material depth-beyond-L1 features."),
        ("P319_NO_L1_ONLY_VARIANTS", "l1_only_variant_rows=0", "No downstream strategy family may use only top-of-book fields."),
        ("P319_TARGET_SEPARATION", "target_columns_not_live_signal_features", "Post-event returns and pressure shifts must be targets/diagnostics, not live signal inputs."),
        ("P319_NO_NET_EDGE_LIVE_MASK", "net_edge_live_mask_rows=0", "No future outcome mask may be used to select live rows."),
        ("P319_NO_STRATEGY_SEARCH", "strategy_search_allowed_now=0", "Precommit only; no P&L, replay or optimization."),
        ("P319_BOUNDARIES", "replay=0;promotion=0;paper=0;claim=0", "No acceptance boundary changes."),
        ("P319_NEXT", NEXT_ACTION, "Materialize compact multi-event feature matrix next."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_processing_work_order() -> pd.DataFrame:
    rows = [
        ("load_joined_parquet", "DuckDB scan over outputs/phase317/phase317_joined_multievent_top5_depth.parquet", "Avoid loading all 28.35M rows into pandas at once."),
        ("derive_tick_features", "SQL expressions for spread, mid, microprice, depth imbalances, depth slopes and pressures", "Use depth levels 1-5 and depth levels 2-5."),
        ("aggregate_signal_features", "group by event_id,event_time_ist,event_type,symbol", "Produce compact event-symbol feature rows."),
        ("separate_targets", "post_60s/post_300s/post_900s/post_1800s response columns", "Keep target columns explicitly outside live feature set."),
        ("write_outputs", "outputs/phase320/phase320_event_catalyst_multievent_feature_matrix.csv", "Feature materialization target."),
        ("quality_audit", "outputs/phase320/phase320_feature_quality.csv", "Validate full-depth features, target separation and 10x32 coverage."),
    ]
    return pd.DataFrame(rows, columns=["work_order_id", "scope", "description"])


def build_gate_evaluation(phase318: pd.DataFrame, features: pd.DataFrame, contract: pd.DataFrame, work_order: pd.DataFrame) -> pd.DataFrame:
    phase318_complete = as_int(metric_value(phase318, "phase318_multievent_join_quality_audit_complete", 0))
    feature_depth_rows = int(features["uses_depth_beyond_l1"].astype(int).sum()) if not features.empty else 0
    target_rows = int(features["lookahead_target_only"].astype(int).sum()) if not features.empty else 0
    rows: list[tuple[str, bool, Any, Any]] = [
        ("P319_PHASE318_COMPLETE", phase318_complete == 1, phase318_complete, 1),
        ("P319_PHASE318_JOIN_BREADTH_OK", as_int(metric_value(phase318, "phase318_event_rows", 0)) >= 10 and as_int(metric_value(phase318, "phase318_symbol_rows", 0)) >= 32, f"events={metric_value(phase318, 'phase318_event_rows', '')};symbols={metric_value(phase318, 'phase318_symbol_rows', '')}", ">=10_events_x_32_symbols"),
        ("P319_PHASE318_DEPTH_OK", as_int(metric_value(phase318, "phase318_depth_beyond_l1_material_rows", 0)) == as_int(metric_value(phase318, "phase318_joined_rows", -1)), metric_value(phase318, "phase318_depth_beyond_l1_material_rows", ""), "all_joined_rows"),
        ("P319_FEATURE_CATALOG_NONEMPTY", len(features) > 0, len(features), ">0"),
        ("P319_DEPTH_BEYOND_L1_FEATURES_PRESENT", feature_depth_rows >= 8, feature_depth_rows, ">=8"),
        ("P319_TARGET_COLUMNS_SEPARATED", target_rows >= 5, target_rows, ">=5"),
        ("P319_CONTRACT_ROWS_PRESENT", len(contract) >= 13, len(contract), ">=13"),
        ("P319_WORK_ORDER_ROWS_PRESENT", len(work_order) >= 6, len(work_order), ">=6"),
        ("P319_NO_STRATEGY_SEARCH_OPENED", True, "strategy_search_allowed_now=0", 0),
        ("P319_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(features: pd.DataFrame, contract: pd.DataFrame, work_order: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    complete = int(hard_pass == hard_rows)
    return pd.DataFrame(
        [
            ("phase319_multievent_feature_materialization_precommit_complete", complete, "Phase319 multi-event feature materialization precommit completed"),
            ("phase319_feature_catalog_rows", int(len(features)), "Feature catalog rows"),
            ("phase319_depth_beyond_l1_feature_rows", int(features["uses_depth_beyond_l1"].astype(int).sum()) if not features.empty else 0, "Feature rows using depth levels 2-5"),
            ("phase319_lookahead_target_only_rows", int(features["lookahead_target_only"].astype(int).sum()) if not features.empty else 0, "Target-only lookahead columns explicitly separated"),
            ("phase319_materialization_contract_rows", int(len(contract)), "Materialization contract rows"),
            ("phase319_processing_work_order_rows", int(len(work_order)), "Processing work-order rows"),
            ("phase319_full_depth_required", 1, "Depth levels 1-5 required"),
            ("phase319_depth_beyond_l1_required", 1, "Depth levels 2-5 materiality required"),
            ("phase319_l1_only_variant_rows_allowed", 0, "No L1-only variants allowed"),
            ("phase319_net_edge_live_mask_rows_allowed", 0, "No net-edge live lookahead mask allowed"),
            ("phase319_strategy_search_allowed_now", 0, "No strategy search in Phase319"),
            ("phase319_strategy_replay_allowed", 0, "No replay"),
            ("phase319_strategy_promotion_allowed", 0, "No promotion"),
            ("phase319_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase319_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase319_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase319_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase319_next_best_action", NEXT_ACTION if complete else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, features: pd.DataFrame, contract: pd.DataFrame, work_order: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase319 Event-Catalyst Multi-Event Feature Materialization Precommit",
        "",
        "Phase319 precommits compact event-symbol feature materialization from the accepted Phase317/318 multi-event top-five depth join.",
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
    (output_dir / "phase319_event_catalyst_multievent_feature_materialization_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase318_dir: Path = DEFAULT_PHASE318_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase318 = read_csv(phase318_dir / "phase318_acceptance_summary.csv")
    features = build_feature_catalog()
    contract = build_materialization_contract()
    work_order = build_processing_work_order()
    gates = build_gate_evaluation(phase318, features, contract, work_order)
    acceptance = build_acceptance(features, contract, work_order, gates)

    features.to_csv(output_dir / "phase319_multievent_feature_catalog.csv", index=False)
    contract.to_csv(output_dir / "phase319_feature_materialization_contract.csv", index=False)
    work_order.to_csv(output_dir / "phase319_processing_work_order.csv", index=False)
    gates.to_csv(output_dir / "phase319_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase319_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, features, contract, work_order, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase319_event_catalyst_multievent_feature_materialization_precommit",
        **reproducibility_fields(
            artifact_id="phase319",
            generated_utc=generated_utc,
            inputs={"phase318_acceptance": str(phase318_dir / "phase318_acceptance_summary.csv")},
            parameters={"no_strategy_search": 1, "full_depth_required": 1, "target_separation_required": 1},
            outputs={"acceptance_summary": str(output_dir / "phase319_acceptance_summary.csv")},
            cost_model_version="not_applicable_feature_precommit_only",
            latency_model_version="not_applicable_feature_precommit_only",
        ),
    }
    (output_dir / "phase319_event_catalyst_multievent_feature_materialization_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Precommit Phase319 multi-event feature materialization.")
    parser.add_argument("--phase318-dir", type=Path, default=DEFAULT_PHASE318_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase318_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
