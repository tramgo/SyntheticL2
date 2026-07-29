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


DEFAULT_PHASE232_DIR = Path("outputs/phase232")
DEFAULT_PHASE233_DIR = Path("outputs/phase233")
DEFAULT_PHASE150_DIR = Path("outputs/phase150")
DEFAULT_PHASE172_DIR = Path("outputs/phase172")
DEFAULT_PHASE142_DIR = Path("outputs/phase142")
DEFAULT_OUTPUT_DIR = Path("outputs/phase234")

NEXT_REAL_ACTION = "run_phase235_build_real_anchor_event_bar_microprice_reversal_adapter_no_paper_live"
NEXT_SEALED_ACTION = "run_phase235_build_sealed_generator_holdout_for_phase233_candidate_no_paper_live"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns or "value" not in frame.columns:
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


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def build_candidate_handoff(phase232_dir: Path, phase233_dir: Path) -> pd.DataFrame:
    validation = read_csv(phase232_dir / "phase232_candidate_validation_summary.csv")
    acceptance = read_csv(phase233_dir / "phase233_acceptance_summary.csv")
    catalog = read_csv(phase233_dir / "phase233_neighbor_candidate_catalog.csv")
    costs = read_csv(phase233_dir / "phase233_cost_multiplier_summary.csv")

    parent_id = str(metric_value(acceptance, "phase233_parent_candidate_id", "P231_MICROPRICE_REVERSAL_H3_Q0_9"))
    row = validation[validation["candidate_id"].astype(str).eq(parent_id)].head(1) if not validation.empty else pd.DataFrame()
    parent = row.iloc[0].to_dict() if not row.empty else {}

    parent_spec = catalog[catalog["candidate_id"].astype(str).eq("P233_MICROPRICE_REVERSAL_H3_Q0_9")].head(1)
    spec = parent_spec.iloc[0].to_dict() if not parent_spec.empty else {}
    test_2x = costs[(costs["split"].astype(str).eq("test")) & (costs["cost_multiplier"].astype(float).eq(2.0))]
    return pd.DataFrame(
        [
            {
                "candidate_id": parent_id,
                "phase233_fragility_realism_pass": as_int(metric_value(acceptance, "phase233_fragility_realism_pass", 0)),
                "family_id": parent.get("family_id", "P231_MICROPRICE_REVERSAL"),
                "signal_rule": "reversal: go opposite the event-bar average microprice deviation",
                "signal_source": spec.get("signal_source", "avg_microprice_dev"),
                "horizon_event_bars": as_int(parent.get("horizon_event_bars", spec.get("horizon_event_bars", 3)), 3),
                "threshold_quantile": as_float(parent.get("threshold_quantile", spec.get("threshold_quantile", 0.9)), 0.9),
                "event_window_score_threshold": as_float(spec.get("event_window_score_threshold", 0.0), 0.0),
                "abs_microprice_dev_threshold": as_float(spec.get("abs_microprice_dev_threshold", 0.0), 0.0),
                "synthetic_train_net_pnl_inr": as_float(parent.get("train_net_pnl_inr", 0.0), 0.0),
                "synthetic_test_net_pnl_inr": as_float(parent.get("test_net_pnl_inr", 0.0), 0.0),
                "synthetic_test_2x_cost_net_pnl_inr": as_float(test_2x["net_pnl_inr"].iloc[0], 0.0) if not test_2x.empty else as_float(metric_value(acceptance, "phase233_parent_test_2x_cost_net_pnl_inr", 0.0), 0.0),
                "zerodha_cost_model_version": ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            }
        ]
    )


def build_schema_mapping(schema: pd.DataFrame) -> pd.DataFrame:
    available = set(schema["column_name"].astype(str)) if not schema.empty and "column_name" in schema.columns else set()
    rows = [
        ("receive_order", "collector_received_utc_ms", "Required to replay websocket receive order and event-bar chronology."),
        ("monotonic_tiebreak", "collector_received_monotonic_ns", "Required when multiple ticks share the same receive millisecond."),
        ("trade_date", "trade_date", "Required for day partitioning and holdout split."),
        ("symbol", "tradingsymbol", "Required for symbol-level event bars."),
        ("last_price", "last_price", "Required for event-bar close price and return labels."),
        ("volume", "volume_traded", "Required for volume deltas and event-window intensity."),
        ("level1_bid_price", "buy_1_price", "Required for mid price and microprice."),
        ("level1_bid_quantity", "buy_1_quantity", "Required for microprice."),
        ("level1_ask_price", "sell_1_price", "Required for mid price and microprice."),
        ("level1_ask_quantity", "sell_1_quantity", "Required for microprice."),
        ("top_five_market_by_price_depth", "buy_1_price..buy_5_orders/sell_1_price..sell_5_orders", "Required for top-five market-by-price context and book-valid filtering."),
    ]
    out = []
    for feature, columns, purpose in rows:
        if ".." in columns:
            required = [
                f"{side}_{level}_{field}"
                for side in ("buy", "sell")
                for level in range(1, 6)
                for field in ("price", "quantity", "orders")
            ]
            present = all(col in available for col in required)
            missing = [col for col in required if col not in available]
        else:
            present = columns in available
            missing = [] if present else [columns]
        out.append(
            {
                "required_feature": feature,
                "source_column_or_family": columns,
                "present_in_real_l2_schema": bool(present),
                "missing_columns": ";".join(missing),
                "purpose": purpose,
            }
        )
    return pd.DataFrame(out)


def build_readiness_matrix(phase150_dir: Path, phase172_dir: Path, phase142_dir: Path, schema_mapping: pd.DataFrame) -> pd.DataFrame:
    phase150 = read_csv(phase150_dir / "phase150_real_l2_duckdb_catalog_acceptance_summary.csv")
    phase172 = read_csv(phase172_dir / "phase172_real_l2_receive_flow_availability_acceptance_summary.csv")
    phase142 = read_csv(phase142_dir / "local_real_l2_date_readiness.csv")

    ready_phase142_days = 0
    if not phase142.empty and "ready_for_phase115_import" in phase142.columns:
        ready = phase142[phase142["ready_for_phase115_import"].astype(str).str.lower().isin(["true", "1"])]
        ready_phase142_days = int(ready["trade_date"].nunique()) if "trade_date" in ready.columns else int(len(ready))

    rows = [
        {
            "check_id": "P234_PHASE233_SYNTHETIC_CANDIDATE_SURVIVED",
            "passed": False,
            "observed_value": "",
            "required_value": "Phase233 pass=1",
            "interpretation": "Filled after candidate handoff is built.",
        },
        {
            "check_id": "P234_LOCAL_REAL_PARQUET_CATALOG_EXISTS",
            "passed": as_int(metric_value(phase150, "phase150_parquet_files_cataloged", 0)) > 0,
            "observed_value": as_int(metric_value(phase150, "phase150_parquet_files_cataloged", 0)),
            "required_value": ">0 local Parquet files",
            "interpretation": "Download-first real L2 storage is available locally.",
        },
        {
            "check_id": "P234_MIN_REAL_RECEIVE_FLOW_DAYS",
            "passed": as_int(metric_value(phase172, "phase172_ready_receive_flow_dates", ready_phase142_days)) >= 5,
            "observed_value": as_int(metric_value(phase172, "phase172_ready_receive_flow_dates", ready_phase142_days)),
            "required_value": ">=5 ready receive-flow dates",
            "interpretation": "Enough real days exist for a small real-anchor adapter trial.",
        },
        {
            "check_id": "P234_SCHEMA_SUPPORTS_MICROPRICE_REVERSAL",
            "passed": bool(not schema_mapping.empty and schema_mapping["present_in_real_l2_schema"].astype(bool).all()),
            "observed_value": int(schema_mapping["present_in_real_l2_schema"].astype(bool).sum()) if not schema_mapping.empty else 0,
            "required_value": f"{len(schema_mapping)} / {len(schema_mapping)} required schema rows present",
            "interpretation": "Raw real ticks contain the fields needed to compute event bars and microprice reversal inputs.",
        },
        {
            "check_id": "P234_EVENT_BAR_ADAPTER_ALREADY_EXISTS",
            "passed": False,
            "observed_value": 0,
            "required_value": "Phase235 adapter not yet built",
            "interpretation": "Phase234 does not pretend strategy replay already exists on real L2; it creates the next executable adapter work order.",
        },
    ]
    return pd.DataFrame(rows)


def decide_route(candidate: pd.DataFrame, readiness: pd.DataFrame) -> pd.DataFrame:
    candidate_pass = bool(not candidate.empty and int(candidate["phase233_fragility_realism_pass"].iloc[0]) == 1)
    readiness = readiness.copy()
    readiness.loc[readiness["check_id"].eq("P234_PHASE233_SYNTHETIC_CANDIDATE_SURVIVED"), ["passed", "observed_value"]] = [candidate_pass, int(candidate_pass)]
    catalog_ready = bool(readiness.loc[readiness["check_id"].eq("P234_LOCAL_REAL_PARQUET_CATALOG_EXISTS"), "passed"].iloc[0])
    days_ready = bool(readiness.loc[readiness["check_id"].eq("P234_MIN_REAL_RECEIVE_FLOW_DAYS"), "passed"].iloc[0])
    schema_ready = bool(readiness.loc[readiness["check_id"].eq("P234_SCHEMA_SUPPORTS_MICROPRICE_REVERSAL"), "passed"].iloc[0])
    route_ready = candidate_pass and catalog_ready and days_ready and schema_ready
    selected_route = "P234_REAL_ANCHOR_EVENT_BAR_ADAPTER_PREP" if route_ready else "P234_SEALED_GENERATOR_HOLDOUT_PREP"
    next_action = NEXT_REAL_ACTION if route_ready else NEXT_SEALED_ACTION
    route = pd.DataFrame(
        [
            {
                "selected_route_id": selected_route,
                "route_ready": int(route_ready),
                "candidate_id": candidate["candidate_id"].iloc[0] if not candidate.empty else "",
                "real_anchor_adapter_preferred": int(route_ready),
                "sealed_generator_holdout_preferred": int(not route_ready),
                "strategy_replay_execution_allowed_now": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
                "next_best_action": next_action,
                "decision": "Build the real L2 event-bar adapter next; do not run paper/live or claim deployable profitability."
                if route_ready
                else "Use sealed synthetic generator holdout next because real-anchor prerequisites are incomplete.",
            }
        ]
    )
    return readiness, route


def build_work_order(candidate: pd.DataFrame, route: pd.DataFrame) -> pd.DataFrame:
    cid = candidate["candidate_id"].iloc[0] if not candidate.empty else ""
    return pd.DataFrame(
        [
            {
                "step_order": 1,
                "phase235_task": "materialize_real_event_bars",
                "candidate_id": cid,
                "implementation_detail": "Read local real L2 Parquet partitions; sort by collector_received_utc_ms and collector_received_monotonic_ns; build per-symbol/day event bars.",
                "acceptance_evidence": "Real event-bar row counts by date/symbol with no paper/live execution.",
            },
            {
                "step_order": 2,
                "phase235_task": "compute_microprice_reversal_features",
                "candidate_id": cid,
                "implementation_detail": "Compute mid price, L1 microprice, avg_microprice_dev, event_window_score, and forward 3-event-bar close-mid return labels.",
                "acceptance_evidence": "Feature quality ledger including missingness, stale-book filtering, gap segmentation and top-five market-by-price schema coverage.",
            },
            {
                "step_order": 3,
                "phase235_task": "dry_run_real_anchor_candidate",
                "candidate_id": cid,
                "implementation_detail": "Replay the frozen Phase233 thresholds and Zerodha equity intraday NSE cost model on local real-anchor event bars only.",
                "acceptance_evidence": "Train-free real-anchor summary; no parameter tuning on real data and no promotion claim.",
            },
            {
                "step_order": 4,
                "phase235_task": "controls_and_decision",
                "candidate_id": cid,
                "implementation_detail": "Run side-flip, random-side, cost stress, date/symbol concentration and stale-feed exclusion controls before deciding continuation.",
                "acceptance_evidence": "Phase235 gates decide whether to continue, redesign, or close the candidate.",
            },
        ]
    )


def build_gate_evaluation(readiness: pd.DataFrame, route: pd.DataFrame) -> pd.DataFrame:
    gate_rows = readiness.copy()
    gate_rows = gate_rows.rename(columns={"check_id": "gate_id", "passed": "passed"})
    gate_rows["severity"] = ["hard", "hard", "hard", "hard", "info"][: len(gate_rows)]
    route_ready = int(route["route_ready"].iloc[0]) if not route.empty else 0
    gate_rows = pd.concat(
        [
            gate_rows,
            pd.DataFrame(
                [
                    {
                        "gate_id": "P234_REAL_ANCHOR_OR_SEALED_HOLDOUT_ROUTE_SELECTED",
                        "passed": True,
                        "observed_value": route["selected_route_id"].iloc[0] if not route.empty else "",
                        "required_value": "explicit route decision",
                        "interpretation": "Phase234 always exits with a concrete next experiment.",
                        "severity": "hard",
                    },
                    {
                        "gate_id": "P234_NO_PAPER_LIVE_OR_PROMOTION_UNLOCK",
                        "passed": True,
                        "observed_value": 0,
                        "required_value": 0,
                        "interpretation": "Phase234 prepares the next experiment without changing paper/live boundaries.",
                        "severity": "hard",
                    },
                    {
                        "gate_id": "P234_REAL_ANCHOR_ADAPTER_ROUTE_READY",
                        "passed": bool(route_ready),
                        "observed_value": route_ready,
                        "required_value": 1,
                        "interpretation": "Whether the next best experiment can use local real L2 immediately.",
                        "severity": "soft",
                    },
                ]
            ),
        ],
        ignore_index=True,
    )
    return gate_rows


def write_report(path: Path, tables: dict[str, pd.DataFrame], route: pd.DataFrame) -> None:
    lines = [
        "# Phase234 Real-anchor or Sealed-holdout Preparation Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase234 responds to the profitable Phase231/232/233 synthetic microprice-reversal result by selecting the next executable holdout path.",
        "It does not tune the strategy, run paper/live trading, or unlock a deployable profitability claim.",
        "",
        f"Selected route: `{route['selected_route_id'].iloc[0] if not route.empty else ''}`.",
        f"Next action: `{route['next_best_action'].iloc[0] if not route.empty else ''}`.",
        "",
    ]
    for title, table in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(table), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    phase232_dir: Path = DEFAULT_PHASE232_DIR,
    phase233_dir: Path = DEFAULT_PHASE233_DIR,
    phase150_dir: Path = DEFAULT_PHASE150_DIR,
    phase172_dir: Path = DEFAULT_PHASE172_DIR,
    phase142_dir: Path = DEFAULT_PHASE142_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    candidate = build_candidate_handoff(phase232_dir, phase233_dir)
    schema = read_csv(phase150_dir / "phase150_real_l2_schema_columns.csv")
    schema_mapping = build_schema_mapping(schema)
    readiness = build_readiness_matrix(phase150_dir, phase172_dir, phase142_dir, schema_mapping)
    readiness, route = decide_route(candidate, readiness)
    work_order = build_work_order(candidate, route)
    gates = build_gate_evaluation(readiness, route)

    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    hard_rows = int(len(hard))
    route_ready = int(route["route_ready"].iloc[0]) if not route.empty else 0
    acceptance = pd.DataFrame(
        [
            ("phase234_holdout_preparation_complete", 1, "Phase234 route preparation completed"),
            ("phase234_parent_candidate_id", candidate["candidate_id"].iloc[0] if not candidate.empty else "", "Candidate carried forward from Phase233"),
            ("phase234_phase233_fragility_realism_pass", int(candidate["phase233_fragility_realism_pass"].iloc[0]) if not candidate.empty else 0, "Phase233 survivor pass flag"),
            ("phase234_required_schema_rows", int(len(schema_mapping)), "Required schema mapping rows evaluated"),
            ("phase234_required_schema_present_rows", int(schema_mapping["present_in_real_l2_schema"].astype(bool).sum()) if not schema_mapping.empty else 0, "Required schema rows present in local real L2 sample"),
            ("phase234_real_anchor_route_ready", route_ready, "Whether the next best action can use local real L2 adapter preparation"),
            ("phase234_selected_route_id", route["selected_route_id"].iloc[0] if not route.empty else "", "Selected holdout route"),
            ("phase234_phase235_work_order_rows", int(len(work_order)), "Concrete work-order rows for Phase235"),
            ("phase234_hard_gate_pass_rows", hard_pass, "Hard Phase234 gates passed"),
            ("phase234_hard_gate_rows", hard_rows, "Hard Phase234 gates evaluated"),
            ("phase234_strategy_replay_execution_allowed_now", 0, "Phase234 does not execute strategy replay"),
            ("phase234_strategy_promotion_allowed", 0, "No strategy promotion from Phase234"),
            ("phase234_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase234"),
            ("phase234_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase234"),
            ("phase234_next_best_action", route["next_best_action"].iloc[0] if not route.empty else NEXT_SEALED_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )

    candidate.to_csv(output_dir / "phase234_candidate_handoff.csv", index=False)
    schema_mapping.to_csv(output_dir / "phase234_required_schema_mapping.csv", index=False)
    readiness.to_csv(output_dir / "phase234_real_anchor_readiness_matrix.csv", index=False)
    route.to_csv(output_dir / "phase234_holdout_route_decision.csv", index=False)
    work_order.to_csv(output_dir / "phase234_phase235_work_order.csv", index=False)
    gates.to_csv(output_dir / "phase234_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase234_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase234_holdout_preparation_report.md",
        {
            "Acceptance Summary": acceptance,
            "Candidate Handoff": candidate,
            "Real-anchor Readiness": readiness,
            "Schema Mapping": schema_mapping,
            "Phase235 Work Order": work_order,
            "Gate Evaluation": gates,
        },
        route,
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase234_real_anchor_or_sealed_holdout_preparation",
        **reproducibility_fields(
            artifact_id="phase234",
            generated_utc=generated_utc,
            inputs={
                "phase232_candidate_validation_summary": str(phase232_dir / "phase232_candidate_validation_summary.csv"),
                "phase233_acceptance_summary": str(phase233_dir / "phase233_acceptance_summary.csv"),
                "phase150_schema_columns": str(phase150_dir / "phase150_real_l2_schema_columns.csv"),
                "phase172_receive_flow_availability": str(phase172_dir / "phase172_real_l2_receive_flow_availability_acceptance_summary.csv"),
                "phase142_local_real_l2_readiness": str(phase142_dir / "local_real_l2_date_readiness.csv"),
            },
            parameters={
                "selected_candidate_family": "P231_MICROPRICE_REVERSAL",
                "preferred_holdout_route_when_ready": "real_anchor_event_bar_adapter",
                "fallback_holdout_route": "sealed_generator_holdout",
                "strategy_replay_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "candidate_handoff": str(output_dir / "phase234_candidate_handoff.csv"),
                "schema_mapping": str(output_dir / "phase234_required_schema_mapping.csv"),
                "readiness_matrix": str(output_dir / "phase234_real_anchor_readiness_matrix.csv"),
                "route_decision": str(output_dir / "phase234_holdout_route_decision.csv"),
                "work_order": str(output_dir / "phase234_phase235_work_order.csv"),
                "gate_evaluation": str(output_dir / "phase234_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase234_acceptance_summary.csv"),
                "report": str(output_dir / "phase234_holdout_preparation_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
    }
    (output_dir / "phase234_holdout_preparation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare the Phase233 profitable synthetic candidate for real-anchor or sealed holdout.")
    parser.add_argument("--phase232-dir", type=Path, default=DEFAULT_PHASE232_DIR)
    parser.add_argument("--phase233-dir", type=Path, default=DEFAULT_PHASE233_DIR)
    parser.add_argument("--phase150-dir", type=Path, default=DEFAULT_PHASE150_DIR)
    parser.add_argument("--phase172-dir", type=Path, default=DEFAULT_PHASE172_DIR)
    parser.add_argument("--phase142-dir", type=Path, default=DEFAULT_PHASE142_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(
        phase232_dir=args.phase232_dir,
        phase233_dir=args.phase233_dir,
        phase150_dir=args.phase150_dir,
        phase172_dir=args.phase172_dir,
        phase142_dir=args.phase142_dir,
        output_dir=args.output_dir,
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
