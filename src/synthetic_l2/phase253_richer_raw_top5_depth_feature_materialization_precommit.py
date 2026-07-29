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


DEFAULT_PHASE252_DIR = Path("outputs/phase252")
DEFAULT_OUTPUT_DIR = Path("outputs/phase253")
DEFAULT_RAW_ROOTS = [
    Path("real_data_sample/l2_multiday_panel"),
    Path("real_data_sample/l2_unseen_validation"),
    Path("real_data_sample/l2_single_day"),
]
RAW_DEPTH_COLUMNS = [
    *(f"buy_{level}_{field}" for level in range(1, 6) for field in ("price", "quantity", "orders")),
    *(f"sell_{level}_{field}" for level in range(1, 6) for field in ("price", "quantity", "orders")),
]
CORE_COLUMNS = [
    "collector_received_utc",
    "collector_received_utc_ms",
    "trade_date",
    "exchange",
    "tradingsymbol",
    "last_price",
    "last_traded_quantity",
    "volume_traded",
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


def inspect_raw_roots(raw_roots: list[Path]) -> tuple[pd.DataFrame, set[str]]:
    rows: list[dict[str, Any]] = []
    sample_columns: set[str] = set()
    for root in raw_roots:
        date_dirs = sorted(root.glob("trade_date=*")) if root.exists() else []
        sample_files = list(root.rglob("*.parquet"))[:3] if root.exists() else []
        sample_path = str(sample_files[0]) if sample_files else ""
        if sample_files and not sample_columns:
            sample_columns = set(pd.read_parquet(sample_files[0]).columns)
        rows.append(
            {
                "raw_root": str(root),
                "exists": int(root.exists()),
                "trade_date_dir_rows": len(date_dirs),
                "sample_parquet_rows": len(sample_files),
                "sample_path": sample_path,
                "usable_without_new_download": int(root.exists() and len(sample_files) > 0),
            }
        )
    return pd.DataFrame(rows), sample_columns


def build_schema_contract(sample_columns: set[str]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for column in CORE_COLUMNS + RAW_DEPTH_COLUMNS:
        rows.append(
            {
                "column": column,
                "column_group": "raw_depth_l1_to_l5" if column in RAW_DEPTH_COLUMNS else "core_tick",
                "required_for_phase254": 1,
                "present_in_sample_schema": int(column in sample_columns),
            }
        )
    return pd.DataFrame(rows)


def build_feature_catalog() -> pd.DataFrame:
    rows = [
        ("l1_mid_price", "level_1_price", "mean of buy_1_price and sell_1_price", "top-of-book price anchor"),
        ("l1_spread", "level_1_price", "sell_1_price minus buy_1_price", "spread and tradability guard"),
        ("level_n_spread_1_to_5", "per_level_price", "sell_n_price minus buy_n_price for n=1..5", "per-level book-width shape"),
        ("buy_quantity_1_to_5", "per_level_quantity", "buy_n_quantity for n=1..5", "visible bid-side depth by level"),
        ("sell_quantity_1_to_5", "per_level_quantity", "sell_n_quantity for n=1..5", "visible ask-side depth by level"),
        ("buy_orders_1_to_5", "per_level_order_count", "buy_n_orders for n=1..5", "visible bid queue-count shape"),
        ("sell_orders_1_to_5", "per_level_order_count", "sell_n_orders for n=1..5", "visible ask queue-count shape"),
        ("cum_buy_qty_l1_l5", "cumulative_depth", "sum buy_1_quantity..buy_5_quantity", "full visible bid depth"),
        ("cum_sell_qty_l1_l5", "cumulative_depth", "sum sell_1_quantity..sell_5_quantity", "full visible ask depth"),
        ("cum_top5_qty_imbalance", "cumulative_depth", "(cum_buy_qty_l1_l5 - cum_sell_qty_l1_l5)/(cum_buy_qty_l1_l5 + cum_sell_qty_l1_l5)", "full visible depth imbalance"),
        ("depth_beyond_l1_qty_imbalance", "depth_beyond_l1", "levels 2..5 bid/ask imbalance", "separate deeper book pressure from top-of-book"),
        ("level_weighted_depth_imbalance", "weighted_depth", "near-level weighted bid/ask imbalance across levels 1..5", "book pressure emphasizing executable levels"),
        ("depth_slope_bid", "depth_shape", "slope of bid quantities across levels 1..5", "bid-side depth shape"),
        ("depth_slope_ask", "depth_shape", "slope of ask quantities across levels 1..5", "ask-side depth shape"),
        ("depth_convexity_bid", "depth_shape", "curvature of bid quantities across levels 1..5", "bid-side replenishment shape"),
        ("depth_convexity_ask", "depth_shape", "curvature of ask quantities across levels 1..5", "ask-side replenishment shape"),
        ("order_count_imbalance_l1_l5", "order_count_shape", "buy order-count total versus sell order-count total", "visible queue crowding"),
        ("avg_qty_per_order_bid_l1_l5", "order_size_shape", "cum buy quantity divided by cum buy orders", "visible bid order-size proxy"),
        ("avg_qty_per_order_ask_l1_l5", "order_size_shape", "cum sell quantity divided by cum sell orders", "visible ask order-size proxy"),
        ("delta_per_level_qty_1_to_5", "event_sequence", "receive-order change in each buy/sell level quantity", "add/cancel/consume proxy"),
        ("delta_per_level_orders_1_to_5", "event_sequence", "receive-order change in each buy/sell level order count", "queue-count transition proxy"),
        ("price_shift_level_1_to_5", "event_sequence", "receive-order change in per-level bid/ask prices", "book move and queue-roll proxy"),
        ("depth_replenishment_pressure", "event_sequence", "positive depth deltas after adverse price move", "replenishment proxy"),
        ("depth_withdrawal_pressure", "event_sequence", "negative depth deltas before/with price move", "withdrawal proxy"),
        ("top5_book_churn", "event_sequence", "sum absolute per-level quantity/order changes", "book activity independent of trade volume"),
        ("event_bar_future_mid_return", "label", "future close-mid return over configured event-bar horizons", "training target for Phase254+ searches"),
    ]
    return pd.DataFrame(rows, columns=["feature_name", "feature_group", "definition", "purpose"])


def build_materialization_contract() -> pd.DataFrame:
    rows = [
        ("P253_EXISTING_RAW_ONLY", "Phase254 must use existing local raw parquet roots only; no new Azure/raw downloads.", "hard"),
        ("P253_EXPLICIT_LEVELS_1_TO_5", "Phase254 must read buy/sell levels 1..5 price, quantity and order-count columns directly.", "hard"),
        ("P253_RECEIVE_ORDER_SORT", "Ticks must be sorted by trade_date, exchange, symbol, collector_received_utc_ms and monotonic timestamp when present.", "hard"),
        ("P253_EVENT_BAR_CLOCK_DECLARED", "Event bars must use a declared receive-event clock and retain source tick counts per bar.", "hard"),
        ("P253_NO_FORBIDDEN_TUNING", "2026-07-17 and 2026-07-20 remain excluded from downstream parameter selection.", "hard"),
        ("P253_LEVEL_SHAPE_FEATURES_REQUIRED", "Outputs must include per-level, cumulative, weighted, slope/convexity and order-count features.", "hard"),
        ("P253_DELTA_SEQUENCE_FEATURES_REQUIRED", "Outputs must include receive-order deltas for per-level quantity, price and order-count changes.", "hard"),
        ("P253_SCHEMA_QUALITY_GATES", "Outputs must check crossed/locked books, nonpositive quantities, missing levels and invalid sorting.", "hard"),
        ("P253_COST_MODEL_CARRIED", "Downstream outputs must carry Zerodha modeled cost/spread floor fields before replay.", "hard"),
        ("P253_NO_REPLAY_PAPER_LIVE", "Phase253 is precommit only; no replay, promotion, paper/live or profitability claim.", "hard"),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "requirement", "severity"])


def build_gate_evaluation(phase252_dir: Path, schema: pd.DataFrame, features: pd.DataFrame, contract: pd.DataFrame, inventory: pd.DataFrame) -> pd.DataFrame:
    next_action = str(metric_value(phase252_dir / "phase252_acceptance_summary.csv", "phase252_next_best_action", ""))
    schema_present = int(schema["present_in_sample_schema"].astype(int).sum()) if not schema.empty else 0
    usable_roots = int(inventory["usable_without_new_download"].astype(int).sum()) if not inventory.empty else 0
    rows = [
        ("P253_PHASE252_WORK_ORDER_PRESENT", "run_phase253_richer_raw_top5_depth_feature_materialization_precommit" in next_action, next_action, "Phase252 next action targets Phase253", "hard"),
        ("P253_LOCAL_RAW_ROOT_AVAILABLE", usable_roots > 0, usable_roots, ">0 usable local raw roots", "hard"),
        ("P253_RAW_SCHEMA_PRESENT", schema_present == len(schema) and len(schema) > 0, f"{schema_present}/{len(schema)}", "all core/depth fields present in sample schema", "hard"),
        ("P253_FEATURE_CATALOG_WRITTEN", len(features) >= 20, len(features), ">=20 richer raw-depth features", "hard"),
        ("P253_CONTRACT_WRITTEN", len(contract) >= 10, len(contract), ">=10 materialization contract rows", "hard"),
        ("P253_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase253 Richer Raw Top-five Depth Feature-materialization Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase253 precommits the next executable materializer for raw Zerodha top-five market-by-price depth.",
        "It is a precommit only: no new downloads, no replay, no strategy promotion, no paper/live acceptance and no profitability claim.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase252_dir: Path = DEFAULT_PHASE252_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR, raw_roots: list[Path] | None = None) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    inventory, sample_columns = inspect_raw_roots(raw_roots or DEFAULT_RAW_ROOTS)
    schema = build_schema_contract(sample_columns)
    features = build_feature_catalog()
    contract = build_materialization_contract()
    gates = build_gate_evaluation(phase252_dir, schema, features, contract, inventory)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    next_action = "run_phase254_materialize_richer_raw_top5_depth_event_bars_existing_raw_only_no_paper_live"
    acceptance = pd.DataFrame(
        [
            ("phase253_richer_raw_depth_precommit_complete", 1, "Phase253 richer raw-depth materialization precommit completed"),
            ("phase253_raw_root_rows", len(inventory), "Raw roots inspected"),
            ("phase253_usable_raw_root_rows", int(inventory["usable_without_new_download"].astype(int).sum()) if not inventory.empty else 0, "Local raw roots usable without new download"),
            ("phase253_schema_present_rows", int(schema["present_in_sample_schema"].astype(int).sum()) if not schema.empty else 0, "Core/raw depth fields present"),
            ("phase253_schema_rows", len(schema), "Core/raw depth fields required"),
            ("phase253_raw_depth_level_columns", len(RAW_DEPTH_COLUMNS), "Explicit buy/sell level 1-5 price/quantity/order columns"),
            ("phase253_feature_catalog_rows", len(features), "Feature catalog rows"),
            ("phase253_materialization_contract_rows", len(contract), "Materialization contract rows"),
            ("phase253_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase253_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase253_phase254_materialization_allowed_next", int(hard_pass == len(hard)), "Whether Phase254 materialization is allowed next"),
            ("phase253_download_more_dates_now_allowed", 0, "No raw-date download in Phase253"),
            ("phase253_replay_execution_allowed_now", 0, "No replay execution in Phase253"),
            ("phase253_strategy_promotion_allowed", 0, "No strategy promotion from Phase253"),
            ("phase253_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase253"),
            ("phase253_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase253"),
            ("phase253_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    inventory.to_csv(output_dir / "phase253_raw_root_inventory.csv", index=False)
    schema.to_csv(output_dir / "phase253_raw_schema_contract.csv", index=False)
    features.to_csv(output_dir / "phase253_richer_depth_feature_catalog.csv", index=False)
    contract.to_csv(output_dir / "phase253_materialization_contract.csv", index=False)
    gates.to_csv(output_dir / "phase253_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase253_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase253_richer_raw_top5_depth_feature_materialization_precommit_report.md",
        {
            "Acceptance Summary": acceptance,
            "Raw Root Inventory": inventory,
            "Raw Schema Contract": schema,
            "Richer Depth Feature Catalog": features,
            "Materialization Contract": contract,
            "Gate Evaluation": gates,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase253_richer_raw_top5_depth_feature_materialization_precommit",
        **reproducibility_fields(
            artifact_id="phase253",
            generated_utc=generated_utc,
            inputs={"phase252_dir": str(phase252_dir), "raw_roots": [str(path) for path in (raw_roots or DEFAULT_RAW_ROOTS)]},
            parameters={
                "raw_depth_columns": RAW_DEPTH_COLUMNS,
                "download_more_dates_now_allowed": 0,
                "replay_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "raw_root_inventory": str(output_dir / "phase253_raw_root_inventory.csv"),
                "raw_schema_contract": str(output_dir / "phase253_raw_schema_contract.csv"),
                "richer_depth_feature_catalog": str(output_dir / "phase253_richer_depth_feature_catalog.csv"),
                "materialization_contract": str(output_dir / "phase253_materialization_contract.csv"),
                "gate_evaluation": str(output_dir / "phase253_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase253_acceptance_summary.csv"),
                "report": str(output_dir / "phase253_richer_raw_top5_depth_feature_materialization_precommit_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_precommit_only",
        ),
    }
    (output_dir / "phase253_richer_raw_top5_depth_feature_materialization_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase253 richer raw top-five depth materialization precommit.")
    parser.add_argument("--phase252-dir", type=Path, default=DEFAULT_PHASE252_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--raw-root", type=Path, action="append", dest="raw_roots")
    args = parser.parse_args()
    manifest = run(phase252_dir=args.phase252_dir, output_dir=args.output_dir, raw_roots=args.raw_roots)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
