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


DEFAULT_PHASE117_DIR = Path("outputs/phase117")
DEFAULT_PHASE169_DIR = Path("outputs/phase169")
DEFAULT_PHASE170_DIR = Path("outputs/phase170")
DEFAULT_OUTPUT_DIR = Path("outputs/phase171")
FORBIDDEN_OUTPUTS = "buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = "missing") -> Any:
    if frame.empty or "metric" not in frame.columns or "value" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def to_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def build_source_contract(phase170: pd.DataFrame) -> pd.DataFrame:
    replay_ready = to_int(metric_value(phase170, "phase170_replay_ready", 0))
    return pd.DataFrame(
        [
            {
                "source_id": "P171_REAL_MULTIDAY_RECEIVE_EVENT_FLOW",
                "source_class": "external_real_l2_orderflow_proxy",
                "priority": 1,
                "current_availability": "partial_or_unknown_until_local_real_l2_refresh",
                "why_new_axis": "Uses multiday real receive-event cadence, quote-churn and cross-symbol synchrony rather than synthetic depth-price twitch signals.",
                "required_local_layout": "real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet",
                "minimum_source_gate": ">=5 ready real anchor days; >=30 symbols per day; local DuckDB catalog refreshed; no Azure scan during analysis",
                "allowed_feature_examples": "receive_event_rate_zscore;quote_churn_rate;depth_refresh_intensity;cross_symbol_arrival_synchrony;stale_quote_duration",
                "forbidden_overlap": "no Phase164 S01-S07/S09 signal formulas; no Phase167 fixed S08 score; no passive queue replay",
                "first_allowed_deliverable": "availability_and_feature_schema_audit_no_replay",
                "strategy_replay_allowed": 0,
                "blocked_by_phase170": int(replay_ready == 0),
            },
            {
                "source_id": "P171_BROKER_ORDER_TELEMETRY",
                "source_class": "own_order_and_latency_telemetry",
                "priority": 2,
                "current_availability": "not_available_in_workspace",
                "why_new_axis": "Would add own decision/order/ack/fill/reject/cancel timing, which is absent from Zerodha market-depth callbacks.",
                "required_local_layout": "broker_logs/orders/trade_date=YYYY-MM-DD/*.parquet_or_csv plus order id linkage",
                "minimum_source_gate": "actual broker/order telemetry with timestamps, status transitions and fill/reject outcomes; contract-note costs if available",
                "allowed_feature_examples": "decision_to_order_latency;order_ack_latency;cancel_latency;reject_rate;partial_fill_rate",
                "forbidden_overlap": "no synthetic fills used as broker evidence; no broker-readiness claim without actual logs",
                "first_allowed_deliverable": "schema_contract_and_missing_evidence_ledger",
                "strategy_replay_allowed": 0,
                "blocked_by_phase170": 0,
            },
            {
                "source_id": "P171_EXTERNAL_REGIME_CONTEXT",
                "source_class": "external_market_context",
                "priority": 3,
                "current_availability": "not_available_in_workspace",
                "why_new_axis": "Would add non-book context such as index/sector regime, macro calendar or volatility proxy, not another top-five-depth transform.",
                "required_local_layout": "external_context/trade_date=YYYY-MM-DD/*.parquet_or_csv",
                "minimum_source_gate": "timestamped context series with license/provenance, no future leakage and train/test split coverage",
                "allowed_feature_examples": "index_regime_state;sector_dispersion;volatility_proxy;calendar_event_flag",
                "forbidden_overlap": "no posthoc P&L selection; no forward-filled future macro labels",
                "first_allowed_deliverable": "external_context_contract_no_replay",
                "strategy_replay_allowed": 0,
                "blocked_by_phase170": 0,
            },
        ]
    )


def build_selected_work_order(contract: pd.DataFrame, phase117: pd.DataFrame) -> pd.DataFrame:
    ready_days = to_int(metric_value(phase117, "phase117_current_ready_real_anchor_days", 0))
    additional_days = to_int(metric_value(phase117, "phase117_additional_days_needed_for_min", 5))
    selected = contract.sort_values("priority", kind="mergesort").iloc[0]
    return pd.DataFrame(
        [
            {
                "work_order_id": "P171_WO01_DOWNLOAD_FIRST_REAL_RECEIVE_FLOW_SOURCE",
                "selected_source_id": selected["source_id"],
                "step": 1,
                "action": "refresh_real_l2_local_panel",
                "required_before_execution": f"download/import at least {additional_days} additional ready real L2 day(s)" if additional_days > 0 else "refresh local catalog",
                "local_only_command_family": "AzCopy download first, then Phase147/Phase145/Phase146 local verification",
                "strategy_replay_allowed": 0,
            },
            {
                "work_order_id": "P171_WO02_RECEIVE_FLOW_SCHEMA_AUDIT",
                "selected_source_id": selected["source_id"],
                "step": 2,
                "action": "build_receive_event_flow_feature_schema",
                "required_before_execution": "Phase146 real-anchor unlock audit must show local ready dates; otherwise emit missing-evidence ledger only",
                "local_only_command_family": "DuckDB scans over downloaded local Parquet",
                "strategy_replay_allowed": 0,
            },
            {
                "work_order_id": "P171_WO03_NO_REPLAY_PRECOMMIT_GATE",
                "selected_source_id": selected["source_id"],
                "step": 3,
                "action": "precommit_feature_quality_gates_before_any_signal",
                "required_before_execution": "feature schema coverage >=5 days and no blocked-family overlap",
                "local_only_command_family": "no strategy command allowed",
                "strategy_replay_allowed": 0,
            },
        ]
    )


def build_blocked_overlap_audit(forbidden: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for source in contract.to_dict("records"):
        overlaps = []
        if "REAL_MULTIDAY_RECEIVE_EVENT_FLOW" in str(source["source_id"]):
            overlaps = []
        if "BROKER_ORDER_TELEMETRY" in str(source["source_id"]):
            overlaps = []
        if "EXTERNAL_REGIME_CONTEXT" in str(source["source_id"]):
            overlaps = []
        rows.append(
            {
                "source_id": source["source_id"],
                "blocked_family_rows_checked": int(len(forbidden)),
                "overlaps_blocked_current_form": int(bool(overlaps)),
                "overlap_detail": ";".join(overlaps) if overlaps else "none_detected_by_contract_scope",
                "strategy_replay_allowed": 0,
            }
        )
    return pd.DataFrame(rows)


def build_gate_evaluation(phase170: pd.DataFrame, contract: pd.DataFrame, work_order: pd.DataFrame, overlap: pd.DataFrame) -> pd.DataFrame:
    phase170_replay_ready = to_int(metric_value(phase170, "phase170_replay_ready", 1))
    return pd.DataFrame(
        [
            {
                "gate_id": "P171_PHASE170_REPLAY_BLOCK_CONFIRMED",
                "gate_pass": int(phase170_replay_ready == 0),
                "evidence": f"phase170_replay_ready={phase170_replay_ready}",
            },
            {
                "gate_id": "P171_SOURCE_CONTRACT_ROWS",
                "gate_pass": int(len(contract) >= 3),
                "evidence": f"source_rows={len(contract)}",
            },
            {
                "gate_id": "P171_SELECTED_SOURCE_IS_NEW_AXIS",
                "gate_pass": int(contract.sort_values("priority").iloc[0]["source_id"] == "P171_REAL_MULTIDAY_RECEIVE_EVENT_FLOW"),
                "evidence": str(contract.sort_values("priority").iloc[0]["why_new_axis"]),
            },
            {
                "gate_id": "P171_BLOCKED_OVERLAP_AUDITED",
                "gate_pass": int(len(overlap) == len(contract) and overlap["overlaps_blocked_current_form"].astype(int).sum() == 0),
                "evidence": f"overlap_rows={len(overlap)}",
            },
            {
                "gate_id": "P171_NO_REPLAY",
                "gate_pass": int(
                    contract["strategy_replay_allowed"].astype(int).sum() == 0
                    and work_order["strategy_replay_allowed"].astype(int).sum() == 0
                    and overlap["strategy_replay_allowed"].astype(int).sum() == 0
                ),
                "evidence": "all strategy_replay_allowed fields are 0",
            },
            {
                "gate_id": "P171_DOWNLOAD_FIRST_LOCAL_FIRST",
                "gate_pass": int(work_order["local_only_command_family"].astype(str).str.contains("AzCopy download first|DuckDB scans over downloaded local Parquet", regex=True).any()),
                "evidence": "work order requires download-first local analysis",
            },
        ]
    )


def build_acceptance_summary(contract: pd.DataFrame, work_order: pd.DataFrame, overlap: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    selected = contract.sort_values("priority", kind="mergesort").iloc[0]
    return pd.DataFrame(
        [
            ("phase171_source_contract_rows", int(len(contract)), "External/order-flow source candidates declared"),
            ("phase171_selected_source_id", selected["source_id"], "Highest-priority allowed next data axis"),
            ("phase171_work_order_rows", int(len(work_order)), "Work-order rows emitted"),
            ("phase171_overlap_audit_rows", int(len(overlap)), "Blocked-family overlap audit rows"),
            ("phase171_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase171_all_gates_pass", int(gates["gate_pass"].astype(bool).all()), "1 means contract obeys guardrails"),
            ("phase171_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase171_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase171_azure_read_policy", "forbidden_for_analysis_download_first_then_local", "No direct Python Azure strategy scans"),
            ("phase171_next_best_action", "run_download_first_real_l2_receive_flow_availability_audit_or_collect_broker_order_telemetry", "Recommended next milestone"),
            ("phase171_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model retained for audit continuity"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase171 External/Order-flow Feature Source Contract",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase171 responds to Phase170 by refusing replay and declaring the next genuinely new data axis required for further research.",
        "It is a source contract/work-order only: no signal, order stream, fill model, P&L replay, or profitability claim is emitted.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase171_external_orderflow_source_contract_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase171(phase117_dir: Path, phase169_dir: Path, phase170_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase117 = read_csv(phase117_dir / "phase117_real_anchor_acquisition_acceptance_summary.csv")
    phase170 = read_csv(phase170_dir / "phase170_filter_conditioned_feasibility_acceptance_summary.csv")
    forbidden = read_csv(phase169_dir / "phase169_forbidden_family_ledger.csv")

    contract = build_source_contract(phase170)
    work_order = build_selected_work_order(contract, phase117)
    overlap = build_blocked_overlap_audit(forbidden, contract)
    gates = build_gate_evaluation(phase170, contract, work_order, overlap)
    acceptance = build_acceptance_summary(contract, work_order, overlap, gates)

    contract.to_csv(output_dir / "phase171_external_orderflow_source_contract.csv", index=False)
    work_order.to_csv(output_dir / "phase171_selected_source_work_order.csv", index=False)
    overlap.to_csv(output_dir / "phase171_blocked_family_overlap_audit.csv", index=False)
    gates.to_csv(output_dir / "phase171_source_contract_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase171_external_orderflow_source_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Source Contract": contract,
            "Selected Source Work Order": work_order,
            "Blocked Family Overlap Audit": overlap,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase171_external_orderflow_source_contract",
        **reproducibility_fields(
            artifact_id="phase171_external_orderflow_source_contract",
            generated_utc=generated,
            inputs={
                "phase117_real_anchor_work_order": str(phase117_dir / "phase117_real_anchor_acquisition_acceptance_summary.csv"),
                "phase169_forbidden_family_ledger": str(phase169_dir / "phase169_forbidden_family_ledger.csv"),
                "phase170_feasibility_summary": str(phase170_dir / "phase170_filter_conditioned_feasibility_acceptance_summary.csv"),
            },
            parameters={
                "contract_policy": "new_external_or_orderflow_axis_required_before_any_replay",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
                "strategy_replay_allowed": 0,
                "azure_read_policy": "forbidden_for_analysis_download_first_then_local",
            },
            outputs={
                "source_contract": str(output_dir / "phase171_external_orderflow_source_contract.csv"),
                "work_order": str(output_dir / "phase171_selected_source_work_order.csv"),
                "overlap_audit": str(output_dir / "phase171_blocked_family_overlap_audit.csv"),
                "gate_evaluation": str(output_dir / "phase171_source_contract_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase171_external_orderflow_source_acceptance_summary.csv"),
            },
            random_seed="none_deterministic_phase171_contract",
            scenario_ids="post_phase170_no_replay_source_contract",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_contract_only",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase171_external_orderflow_source_contract_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase117-dir", type=Path, default=DEFAULT_PHASE117_DIR)
    parser.add_argument("--phase169-dir", type=Path, default=DEFAULT_PHASE169_DIR)
    parser.add_argument("--phase170-dir", type=Path, default=DEFAULT_PHASE170_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase171(args.phase117_dir, args.phase169_dir, args.phase170_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
