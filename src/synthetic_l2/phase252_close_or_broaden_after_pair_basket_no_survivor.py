from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE251_DIR = Path("outputs/phase251")
DEFAULT_RAW_ROOTS = [Path("real_data_sample/l2_multiday_panel"), Path("real_data_sample/l2_unseen_validation"), Path("real_data_sample/l2_single_day")]
DEFAULT_OUTPUT_DIR = Path("outputs/phase252")


RAW_DEPTH_COLUMNS = [
    *(f"buy_{level}_{field}" for level in range(1, 6) for field in ("price", "quantity", "orders")),
    *(f"sell_{level}_{field}" for level in range(1, 6) for field in ("price", "quantity", "orders")),
]


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(path: Path, metric: str, default: Any = None) -> Any:
    frame = read_csv(path)
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def inspect_raw_roots(raw_roots: list[Path]) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    schema_rows: list[dict[str, Any]] = []
    sample_columns: set[str] = set()
    sampled_path = ""
    for root in raw_roots:
        date_dirs = sorted(root.glob("trade_date=*")) if root.exists() else []
        parquet_files: list[Path] = []
        if root.exists():
            for date_dir in date_dirs[:2]:
                parquet_files.extend(list(date_dir.rglob("*.parquet"))[:5])
            if not parquet_files:
                parquet_files = list(root.rglob("*.parquet"))[:5]
        if parquet_files and not sample_columns:
            sampled_path = str(parquet_files[0])
            sample_columns = set(pd.read_parquet(parquet_files[0]).columns)
        rows.append(
            {
                "raw_root": str(root),
                "exists": int(root.exists()),
                "trade_date_dir_rows": len(date_dirs),
                "sample_parquet_rows": len(parquet_files),
                "sampled_path": sampled_path if parquet_files else "",
            }
        )
    for column in RAW_DEPTH_COLUMNS:
        schema_rows.append(
            {
                "column": column,
                "required_for_richer_raw_depth": 1,
                "present_in_sample_schema": int(column in sample_columns),
            }
        )
    return pd.DataFrame(rows), pd.DataFrame(schema_rows)


def build_closure_ledger(phase251_dir: Path) -> pd.DataFrame:
    acceptance = phase251_dir / "phase251_acceptance_summary.csv"
    rows = [
        {
            "decision_id": "P252_CLOSE_AGGREGATE_PAIR_BASKET_RELATIVE_VALUE",
            "scope": "phase251_pair_basket_relative_value_on_phase235_aggregate_event_bars",
            "decision": "closed_for_current_evidence_set",
            "observed_value": as_int(metric_value(acceptance, "phase251_survivor_candidate_rows", 0)),
            "required_value": ">0 controlled survivors",
            "rationale": "Phase251 found no controlled survivor across market-neutral pair/basket variants.",
            "reuse_allowed_without_material_redesign": 0,
        },
        {
            "decision_id": "P252_BLOCK_THRESHOLD_RELAXATION_LOOP",
            "scope": "phase251_variant_thresholds",
            "decision": "blocked",
            "observed_value": as_int(metric_value(acceptance, "phase251_cost200_positive_variant_rows", 0)),
            "required_value": ">0 positive at 2x modeled costs",
            "rationale": "Relaxing thresholds after zero base-cost and zero 2x-cost positives would not address cost-floor dominance.",
            "reuse_allowed_without_material_redesign": 0,
        },
        {
            "decision_id": "P252_KEEP_NEW_DOWNLOADS_CLOSED",
            "scope": "fresh_real_l2_dates",
            "decision": "blocked_until_material_new_richer_depth_candidate",
            "observed_value": as_int(metric_value(acceptance, "phase251_future_holdout_precommit_allowed", 0)),
            "required_value": "future_holdout_precommit_allowed=1",
            "rationale": "No Phase251 survivor qualifies for fresh holdout data spend.",
            "reuse_allowed_without_material_redesign": 0,
        },
    ]
    return pd.DataFrame(rows)


def build_failure_attribution(phase251_dir: Path) -> pd.DataFrame:
    acceptance = phase251_dir / "phase251_acceptance_summary.csv"
    rows = [
        {
            "failure_mode": "aggregate_pair_basket_cost_floor_dominance",
            "observed_metric": "phase251_net_positive_variant_rows",
            "observed_value": as_int(metric_value(acceptance, "phase251_net_positive_variant_rows", 0)),
            "interpretation": "No tested pair/basket variant was positive even at base modeled costs.",
        },
        {
            "failure_mode": "no_2x_cost_positive_variants",
            "observed_metric": "phase251_cost200_positive_variant_rows",
            "observed_value": as_int(metric_value(acceptance, "phase251_cost200_positive_variant_rows", 0)),
            "interpretation": "The branch produced no cost-stress candidates for controls.",
        },
        {
            "failure_mode": "aggregate_depth_feature_limit",
            "observed_metric": "phase251_full_top_five_depth_variant_rows",
            "observed_value": as_int(metric_value(acceptance, "phase251_full_top_five_depth_variant_rows", 0)),
            "interpretation": "Phase251 used top-five aggregate and depth-beyond-L1 features, but not explicit per-level book-shape features from raw parquet.",
        },
        {
            "failure_mode": "best_failed_candidate_cost_drag",
            "observed_metric": "phase251_best_training_net_pnl_inr",
            "observed_value": metric_value(acceptance, "phase251_best_training_net_pnl_inr", ""),
            "interpretation": "The best failed candidate had positive gross P&L but modeled cost drag exceeded the edge.",
        },
    ]
    return pd.DataFrame(rows)


def build_broaden_queue() -> pd.DataFrame:
    rows = [
        {
            "priority": 1,
            "route_id": "P252_RICHER_RAW_TOP5_DEPTH_EVENT_BARS",
            "route": "rebuild_event_bars_from_raw_top5_depth_levels",
            "why_materially_different": "Moves from aggregate Phase235 depth features to explicit per-level buy/sell price, quantity and order-count shape features from raw parquet.",
            "allowed_sources": "existing downloaded raw parquet under real_data_sample; no new raw-date downloads",
            "precommit_next": "phase253_richer_raw_top5_depth_feature_materialization_precommit",
            "replay_allowed_now": 0,
        },
        {
            "priority": 2,
            "route_id": "P252_DEPTH_EVENT_SEQUENCE_MODEL",
            "route": "top5_depth_event_sequence_prediction",
            "why_materially_different": "Uses changes in per-level book shape, queue count and replenishment/withdrawal sequences rather than static aggregate imbalance.",
            "allowed_sources": "raw top-five market-by-price tick stream and receive-order deltas",
            "precommit_next": "phase253_depth_event_sequence_precommit",
            "replay_allowed_now": 0,
        },
        {
            "priority": 3,
            "route_id": "P252_LOW_TURNOVER_OPENING_DEPTH_SHOCK",
            "route": "opening_depth_shock_low_turnover_only",
            "why_materially_different": "Separates opening price-discovery/depth depletion from normal intraday microstructure and requires lower turnover.",
            "allowed_sources": "existing raw open-window L2 parquet plus cost model",
            "precommit_next": "phase253_opening_depth_shock_precommit",
            "replay_allowed_now": 0,
        },
    ]
    return pd.DataFrame(rows)


def build_guardrail_ledger() -> pd.DataFrame:
    rows = [
        ("P252_NO_PROFITABILITY_CLAIM", "No deployable profitability claim because Phase251 found zero positive variants and zero survivors.", 1),
        ("P252_NO_MORE_DATE_DOWNLOAD", "No fresh real L2 date downloads until a richer raw-depth candidate is frozen.", 1),
        ("P252_NO_THRESHOLD_RELAXATION_ONLY", "Do not continue by relaxing Phase251 thresholds; next route must change the feature source.", 1),
        ("P252_RAW_DEPTH_REQUIRED_NEXT", "The next primary route must use explicit raw buy/sell levels 1-5 price, quantity and order-count fields.", 1),
        ("P252_COSTS_AND_CONTROLS_REMAIN", "Zerodha modeled costs, spread/slippage, 2x-cost stress, side-flip and random-side controls remain mandatory.", 1),
        ("P252_NO_PAPER_LIVE", "Paper/live acceptance remains closed.", 1),
    ]
    return pd.DataFrame(rows, columns=["guardrail_id", "requirement", "active"])


def build_gate_evaluation(
    phase251_dir: Path,
    closure: pd.DataFrame,
    failures: pd.DataFrame,
    queue: pd.DataFrame,
    guardrails: pd.DataFrame,
    raw_schema: pd.DataFrame,
) -> pd.DataFrame:
    next_action = str(metric_value(phase251_dir / "phase251_acceptance_summary.csv", "phase251_next_best_action", ""))
    raw_depth_present = int(raw_schema["present_in_sample_schema"].astype(int).sum()) if not raw_schema.empty else 0
    rows = [
        ("P252_PHASE251_WORK_ORDER_PRESENT", "close_or_broaden_phase251" in next_action, next_action, "Phase251 next action asks close/broaden", "hard"),
        ("P252_CLOSURE_LEDGER_WRITTEN", len(closure) >= 3, len(closure), ">=3 closure rows", "hard"),
        ("P252_FAILURE_ATTRIBUTION_WRITTEN", len(failures) >= 4, len(failures), ">=4 failure rows", "hard"),
        ("P252_MATERIAL_BROADEN_QUEUE_WRITTEN", len(queue) >= 3, len(queue), ">=3 materially different routes", "hard"),
        ("P252_RAW_DEPTH_SCHEMA_AVAILABLE", raw_depth_present == len(RAW_DEPTH_COLUMNS), f"{raw_depth_present}/{len(RAW_DEPTH_COLUMNS)}", "all raw buy/sell levels 1-5 fields present in sample schema", "hard"),
        ("P252_GUARDRAILS_ACTIVE", bool((guardrails["active"].astype(int) == 1).all()), "all active", "all guardrails active", "hard"),
        ("P252_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase252 Close or Broaden After Pair/Basket No-survivor Search",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase252 closes the aggregate-feature pair/basket relative-value branch and opens a richer raw top-five depth materialization route.",
        "It does not download new data, run a replay, promote a strategy, open paper/live acceptance or claim profitability.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase251_dir: Path = DEFAULT_PHASE251_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR, raw_roots: list[Path] | None = None) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_inventory, raw_schema = inspect_raw_roots(raw_roots or DEFAULT_RAW_ROOTS)
    closure = build_closure_ledger(phase251_dir)
    failures = build_failure_attribution(phase251_dir)
    queue = build_broaden_queue()
    guardrails = build_guardrail_ledger()
    gates = build_gate_evaluation(phase251_dir, closure, failures, queue, guardrails, raw_schema)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    selected = queue.sort_values("priority").iloc[0].to_dict()
    next_action = "run_phase253_richer_raw_top5_depth_feature_materialization_precommit_no_new_downloads_no_paper_live"
    acceptance = pd.DataFrame(
        [
            ("phase252_close_or_broaden_complete", 1, "Phase252 close/broaden decision completed"),
            ("phase252_closed_scope", "aggregate_pair_basket_relative_value_on_phase235_event_bars", "Scope closed under current evidence"),
            ("phase252_phase251_variant_rows", as_int(metric_value(phase251_dir / "phase251_acceptance_summary.csv", "phase251_variant_rows", 0)), "Phase251 variants considered"),
            ("phase252_phase251_base_positive_rows", as_int(metric_value(phase251_dir / "phase251_acceptance_summary.csv", "phase251_net_positive_variant_rows", 0)), "Phase251 base-cost positive variants"),
            ("phase252_phase251_cost200_positive_rows", as_int(metric_value(phase251_dir / "phase251_acceptance_summary.csv", "phase251_cost200_positive_variant_rows", 0)), "Phase251 2x-cost positive variants"),
            ("phase252_phase251_survivor_rows", as_int(metric_value(phase251_dir / "phase251_acceptance_summary.csv", "phase251_survivor_candidate_rows", 0)), "Phase251 controlled survivors"),
            ("phase252_raw_root_rows", len(raw_inventory), "Raw roots inspected"),
            ("phase252_raw_depth_schema_present_rows", int(raw_schema["present_in_sample_schema"].astype(int).sum()) if not raw_schema.empty else 0, "Raw depth schema fields present"),
            ("phase252_raw_depth_schema_rows", len(raw_schema), "Raw depth schema fields required"),
            ("phase252_closure_rows", len(closure), "Closure ledger rows"),
            ("phase252_failure_attribution_rows", len(failures), "Failure attribution rows"),
            ("phase252_broaden_queue_rows", len(queue), "Materially different broaden routes"),
            ("phase252_selected_next_route", selected.get("route_id", ""), "Highest-priority next route"),
            ("phase252_threshold_relaxation_only_allowed", 0, "No threshold relaxation loop"),
            ("phase252_download_more_dates_now_allowed", 0, "No raw-date download in Phase252"),
            ("phase252_replay_execution_allowed_now", 0, "No replay execution in Phase252"),
            ("phase252_strategy_promotion_allowed", 0, "No strategy promotion from Phase252"),
            ("phase252_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase252"),
            ("phase252_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase252"),
            ("phase252_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase252_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase252_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    raw_inventory.to_csv(output_dir / "phase252_raw_depth_inventory.csv", index=False)
    raw_schema.to_csv(output_dir / "phase252_raw_depth_schema_contract.csv", index=False)
    closure.to_csv(output_dir / "phase252_closure_ledger.csv", index=False)
    failures.to_csv(output_dir / "phase252_failure_attribution.csv", index=False)
    queue.to_csv(output_dir / "phase252_material_broaden_queue.csv", index=False)
    guardrails.to_csv(output_dir / "phase252_guardrail_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase252_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase252_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase252_close_or_broaden_after_pair_basket_no_survivor_report.md",
        {
            "Acceptance Summary": acceptance,
            "Raw Depth Inventory": raw_inventory,
            "Raw Depth Schema Contract": raw_schema,
            "Closure Ledger": closure,
            "Failure Attribution": failures,
            "Material Broaden Queue": queue,
            "Guardrail Ledger": guardrails,
            "Gate Evaluation": gates,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase252_close_or_broaden_after_pair_basket_no_survivor",
        **reproducibility_fields(
            artifact_id="phase252",
            generated_utc=generated_utc,
            inputs={"phase251_dir": str(phase251_dir), "raw_roots": [str(path) for path in (raw_roots or DEFAULT_RAW_ROOTS)]},
            parameters={
                "threshold_relaxation_only_allowed": 0,
                "download_more_dates_now_allowed": 0,
                "replay_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "raw_depth_inventory": str(output_dir / "phase252_raw_depth_inventory.csv"),
                "raw_depth_schema_contract": str(output_dir / "phase252_raw_depth_schema_contract.csv"),
                "closure_ledger": str(output_dir / "phase252_closure_ledger.csv"),
                "failure_attribution": str(output_dir / "phase252_failure_attribution.csv"),
                "material_broaden_queue": str(output_dir / "phase252_material_broaden_queue.csv"),
                "guardrail_ledger": str(output_dir / "phase252_guardrail_ledger.csv"),
                "gate_evaluation": str(output_dir / "phase252_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase252_acceptance_summary.csv"),
                "report": str(output_dir / "phase252_close_or_broaden_after_pair_basket_no_survivor_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_decision_only",
        ),
    }
    (output_dir / "phase252_close_or_broaden_after_pair_basket_no_survivor_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase252 close/broaden decision after Phase251 no-survivor search.")
    parser.add_argument("--phase251-dir", type=Path, default=DEFAULT_PHASE251_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--raw-root", type=Path, action="append", dest="raw_roots")
    args = parser.parse_args()
    manifest = run(phase251_dir=args.phase251_dir, output_dir=args.output_dir, raw_roots=args.raw_roots)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
