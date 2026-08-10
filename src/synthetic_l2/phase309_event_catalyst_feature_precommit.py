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


DEFAULT_PHASE308_DIR = Path("outputs/phase308")
DEFAULT_OUTPUT_DIR = Path("outputs/phase309")

NEXT_ACTION = "run_phase310_event_catalyst_feature_materialization_no_strategy_search"
REPAIR_ACTION = "repair_phase309_event_catalyst_feature_precommit"


def build_feature_catalog() -> pd.DataFrame:
    rows = [
        ("event_clock", "relative_second", "event_time_alignment", "Event-relative second from -900 to +1800.", 1, 0),
        ("l1_spread", "sell_1_price - buy_1_price", "top_of_book", "Quoted spread at best bid/ask.", 1, 0),
        ("l1_mid", "(sell_1_price + buy_1_price) / 2", "top_of_book", "Best bid/ask midpoint.", 1, 0),
        ("l1_microprice", "weighted best quote by opposite-side quantity", "top_of_book", "Microprice using L1 bid/ask prices and quantities.", 1, 0),
        ("l1_queue_imbalance", "(buy_1_quantity - sell_1_quantity) / total_l1_qty", "top_of_book", "Best-level queue imbalance.", 1, 0),
        ("l1_l5_qty_imbalance", "sum_buy_qty_l1_l5 vs sum_sell_qty_l1_l5", "full_depth", "Aggregate quantity imbalance across levels 1-5.", 1, 1),
        ("l2_l5_qty_imbalance", "sum_buy_qty_l2_l5 vs sum_sell_qty_l2_l5", "depth_beyond_l1", "Depth-beyond-L1 quantity imbalance.", 1, 1),
        ("l1_l5_order_imbalance", "sum_buy_orders_l1_l5 vs sum_sell_orders_l1_l5", "full_depth", "Aggregate order-count imbalance across levels 1-5.", 1, 1),
        ("l2_l5_order_imbalance", "sum_buy_orders_l2_l5 vs sum_sell_orders_l2_l5", "depth_beyond_l1", "Depth-beyond-L1 order-count imbalance.", 1, 1),
        ("bid_depth_slope_l1_l5", "buy_1_price - buy_5_price", "full_depth", "Bid-side depth price slope across levels 1-5.", 1, 1),
        ("ask_depth_slope_l1_l5", "sell_5_price - sell_1_price", "full_depth", "Ask-side depth price slope across levels 1-5.", 1, 1),
        ("depth_pressure", "l1_l5_qty_imbalance / spread", "full_depth", "Liquidity pressure normalized by spread.", 1, 1),
        ("l2_l5_pressure", "l2_l5_qty_imbalance / spread", "depth_beyond_l1", "Beyond-L1 pressure normalized by spread.", 1, 1),
        ("event_pre_mean_mid", "mean mid where relative_second < 0", "event_context", "Pre-event reference midpoint.", 1, 0),
        ("event_post_return_60s", "mid at +60s vs event mid", "event_response", "Short post-event midpoint response.", 1, 0),
        ("event_post_return_300s", "mid at +300s vs event mid", "event_response", "Five-minute post-event midpoint response.", 1, 0),
        ("event_post_return_900s", "mid at +900s vs event mid", "event_response", "Fifteen-minute post-event midpoint response.", 1, 0),
        ("event_post_depth_pressure_shift", "post pressure minus pre pressure", "full_depth_response", "Full-depth pressure change around event.", 1, 1),
    ]
    return pd.DataFrame(
        rows,
        columns=["feature_id", "formula", "feature_family", "description", "phase310_materialization_required", "uses_depth_beyond_l1"],
    )


def build_contract() -> pd.DataFrame:
    rows = [
        ("P309_INPUT", "outputs/phase307/phase307_joined_event_top5_depth.parquet", "Use Phase307 joined event/depth artifact."),
        ("P309_QUALITY_GATE", "phase308_hard_issue_rows == 0", "Only materialize if Phase308 quality audit passes."),
        ("P309_DEPTH_REQUIREMENT", "levels_1_to_5_required", "Feature set must preserve top-five market-by-price depth."),
        ("P309_L2_L5_MATERIALITY", "depth_beyond_l1_required", "At least one material feature family must use levels 2-5."),
        ("P309_NO_L1_ONLY_SEARCH", "l1_only_candidate_allowed=0", "Do not open L1-only strategies from this branch."),
        ("P309_EVENT_BOUNDARY", "event rows are catalysts only", "No directional labels from event source."),
        ("P309_NO_STRATEGY_SEARCH", "strategy_search_allowed_now=0", "Precommit only; no P&L or optimization."),
        ("P309_NEXT", "run_phase310_event_catalyst_feature_materialization_no_strategy_search", "Materialize features before searching strategies."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_gate_evaluation(phase308: pd.DataFrame, features: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    phase308_complete = as_int(metric_value(phase308, "phase308_join_quality_audit_complete", 0))
    phase308_issues = as_int(metric_value(phase308, "phase308_hard_issue_rows", 999))
    depth_features = int(features["uses_depth_beyond_l1"].astype(int).sum()) if not features.empty else 0
    gates = [
        ("P309_PHASE308_COMPLETE", phase308_complete == 1, phase308_complete, 1),
        ("P309_PHASE308_NO_HARD_ISSUES", phase308_issues == 0, phase308_issues, 0),
        ("P309_FEATURE_CATALOG_NONEMPTY", len(features) > 0, len(features), ">0"),
        ("P309_DEPTH_BEYOND_L1_FEATURES_PRESENT", depth_features > 0, depth_features, ">0"),
        ("P309_CONTRACT_ROWS_PRESENT", len(contract) >= 8, len(contract), ">=8"),
        ("P309_NO_STRATEGY_SEARCH_OPENED", True, "strategy_search_allowed_now=0", 0),
        ("P309_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(features: pd.DataFrame, contract: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    next_action = NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION
    return pd.DataFrame(
        [
            ("phase309_event_feature_precommit_complete", 1, "Phase309 event-catalyst feature precommit completed"),
            ("phase309_feature_catalog_rows", int(len(features)), "Feature catalog rows"),
            ("phase309_depth_beyond_l1_feature_rows", int(features["uses_depth_beyond_l1"].astype(int).sum()) if not features.empty else 0, "Features using depth levels 2-5"),
            ("phase309_materialization_contract_rows", int(len(contract)), "Materialization contract rows"),
            ("phase309_full_depth_required", 1, "Top-five market-by-price depth required"),
            ("phase309_l1_only_candidate_allowed", 0, "L1-only candidate path closed"),
            ("phase309_strategy_search_allowed_now", 0, "No strategy search in Phase309"),
            ("phase309_strategy_replay_allowed", 0, "No replay"),
            ("phase309_strategy_promotion_allowed", 0, "No promotion"),
            ("phase309_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase309_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase309_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase309_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase309_next_best_action", next_action, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, features: pd.DataFrame, contract: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase309 Event-Catalyst Feature Precommit",
        "",
        "Phase309 precommits full-depth event-catalyst feature construction before any strategy search.",
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
        "## Gates",
        "",
        _markdown_table(gates),
    ]
    (output_dir / "phase309_event_catalyst_feature_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase308_dir: Path = DEFAULT_PHASE308_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase308 = read_csv(phase308_dir / "phase308_acceptance_summary.csv")
    features = build_feature_catalog()
    contract = build_contract()
    gates = build_gate_evaluation(phase308, features, contract)
    acceptance = build_acceptance(features, contract, gates)

    features.to_csv(output_dir / "phase309_event_catalyst_feature_catalog.csv", index=False)
    contract.to_csv(output_dir / "phase309_event_catalyst_feature_materialization_contract.csv", index=False)
    gates.to_csv(output_dir / "phase309_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase309_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, features, contract, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase309_event_catalyst_feature_precommit",
        **reproducibility_fields(
            artifact_id="phase309",
            generated_utc=generated_utc,
            inputs={"phase308_acceptance": str(phase308_dir / "phase308_acceptance_summary.csv")},
            parameters={"no_strategy_search": 1, "full_depth_required": 1},
            outputs={"acceptance_summary": str(output_dir / "phase309_acceptance_summary.csv")},
            cost_model_version="not_applicable_feature_precommit_only",
            latency_model_version="not_applicable_feature_precommit_only",
        ),
    }
    (output_dir / "phase309_event_catalyst_feature_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Precommit Phase309 event-catalyst full-depth feature construction.")
    parser.add_argument("--phase308-dir", type=Path, default=DEFAULT_PHASE308_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase308_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
