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


DEFAULT_PHASE237_DIR = Path("outputs/phase237")
DEFAULT_PHASE235_BARS = Path("outputs/phase235/phase235_real_event_bars.parquet")
DEFAULT_OUTPUT_DIR = Path("outputs/phase238")
MIN_UNSEEN_VALIDATION_DATES = 5
MIN_VALIDATION_SYMBOLS = 20
MIN_VALIDATION_TRADES = 50


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


def load_best_candidate(phase237_dir: Path) -> dict[str, Any]:
    acceptance = read_csv(phase237_dir / "phase237_acceptance_summary.csv")
    candidates = read_csv(phase237_dir / "phase237_breadth_positive_candidates.csv")
    best_id = str(metric_value(acceptance, "phase237_best_candidate_id", ""))
    best = candidates[candidates["candidate_id"].astype(str).eq(best_id)].head(1)
    if best.empty:
        expanded = read_csv(phase237_dir / "phase237_expanded_candidate_summary.csv")
        best = expanded[expanded["candidate_id"].astype(str).eq(best_id)].head(1) if not expanded.empty else pd.DataFrame()
    if best.empty:
        raise FileNotFoundError("Phase237 best candidate row not found")
    row = best.iloc[0].to_dict()
    row["phase237_candidate_opened_for_phase238"] = as_int(metric_value(acceptance, "phase237_candidate_opened_for_phase238", 0))
    row["phase237_best_control_pass_rows"] = as_int(metric_value(acceptance, "phase237_best_control_pass_rows", 0))
    row["phase237_best_control_rows"] = as_int(metric_value(acceptance, "phase237_best_control_rows", 0))
    return row


def build_candidate_freeze(best: dict[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "candidate_id": best.get("candidate_id", ""),
                "family_id": best.get("family_id", ""),
                "signal_source": best.get("signal_source", ""),
                "direction": best.get("direction", ""),
                "horizon_event_bars": as_int(best.get("horizon_event_bars", 0)),
                "event_quantile": as_float(best.get("event_quantile", 0.0)),
                "signal_quantile": as_float(best.get("signal_quantile", 0.0)),
                "event_window_score_threshold": as_float(best.get("event_window_score_threshold", 0.0)),
                "signal_abs_threshold": as_float(best.get("signal_abs_threshold", 0.0)),
                "source_event_bar_adapter": "phase235_real_anchor_event_bar_adapter",
                "cost_model_version": ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
                "phase237_net_pnl_inr": as_float(best.get("real_anchor_net_pnl_inr", 0.0)),
                "phase237_trades": as_int(best.get("real_anchor_trades", 0)),
                "phase237_dates": as_int(best.get("real_anchor_dates", 0)),
                "phase237_symbols": as_int(best.get("real_anchor_symbols", 0)),
                "frozen_for_phase238": 1,
                "parameter_tuning_allowed_in_phase238": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            }
        ]
    )


def build_availability(
    bars_path: Path,
    phase237_dir: Path,
    candidate_freeze: pd.DataFrame,
) -> pd.DataFrame:
    bars = pd.read_parquet(bars_path, columns=["trade_date", "symbol"]) if bars_path.exists() else pd.DataFrame()
    ledger = read_csv(phase237_dir / "phase237_best_candidate_trade_ledger.csv")
    all_dates = sorted(bars["trade_date"].astype(str).unique().tolist()) if not bars.empty else []
    discovery_dates = sorted(ledger["trade_date"].astype(str).unique().tolist()) if not ledger.empty else []
    # Phase237 thresholds were computed on all Phase235 bars, so every current Phase235 date is discovery-contaminated.
    local_unseen_dates = []
    rows = [
        {
            "availability_check": "P238_PHASE235_REAL_EVENT_BARS_AVAILABLE",
            "passed": bool(len(all_dates) > 0),
            "observed_value": len(all_dates),
            "required_value": ">0 local real event-bar dates",
            "interpretation": "Local real event bars are available for diagnostics and split accounting.",
        },
        {
            "availability_check": "P238_PHASE237_CANDIDATE_FROZEN",
            "passed": bool(not candidate_freeze.empty and int(candidate_freeze["frozen_for_phase238"].iloc[0]) == 1),
            "observed_value": candidate_freeze["candidate_id"].iloc[0] if not candidate_freeze.empty else "",
            "required_value": "frozen candidate id",
            "interpretation": "Phase238 may not tune thresholds or candidate selection.",
        },
        {
            "availability_check": "P238_CURRENT_LOCAL_DATES_DISCOVERY_CONTAMINATED",
            "passed": True,
            "observed_value": ";".join(all_dates),
            "required_value": "all Phase235 dates treated as Phase237 discovery data",
            "interpretation": "Because real quantile thresholds were selected on Phase235 bars, current dates cannot prove unseen acceptance.",
        },
        {
            "availability_check": "P238_TRULY_UNSEEN_LOCAL_DATES_AVAILABLE",
            "passed": bool(len(local_unseen_dates) >= MIN_UNSEEN_VALIDATION_DATES),
            "observed_value": len(local_unseen_dates),
            "required_value": f">={MIN_UNSEEN_VALIDATION_DATES} dates not used by Phase237 discovery",
            "interpretation": "No currently materialized local Phase235 dates qualify as truly unseen validation dates.",
        },
        {
            "availability_check": "P238_PHASE237_DISCOVERY_TRADE_DATES",
            "passed": bool(len(discovery_dates) > 0),
            "observed_value": ";".join(discovery_dates),
            "required_value": "best candidate trade dates recorded",
            "interpretation": "Trade-date breadth is known for the discovery result.",
        },
    ]
    return pd.DataFrame(rows)


def build_validation_contract(best: dict[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "contract_id": "P238_UNSEEN_REAL_ANCHOR_PRIMARY",
                "validation_type": "acceptance_candidate_validation",
                "input_data": "future downloaded real Zerodha-websocket-like L2 dates not used by Phase237",
                "candidate_id": best.get("candidate_id", ""),
                "parameter_tuning_allowed": 0,
                "minimum_dates": MIN_UNSEEN_VALIDATION_DATES,
                "minimum_symbols": MIN_VALIDATION_SYMBOLS,
                "minimum_trades": MIN_VALIDATION_TRADES,
                "required_controls": "side_flip;random_side_1000;cost_150;cost_200;date_symbol_concentration",
                "acceptance_rule": "net_pnl_after_costs_positive AND >=3/4 controls pass AND date/symbol/trade breadth met",
                "result_claim_allowed": "validation_candidate_only_no_paper_live",
            },
            {
                "contract_id": "P238_WALK_FORWARD_DIAGNOSTIC_FALLBACK",
                "validation_type": "non_acceptance_diagnostic",
                "input_data": "existing Phase235 real event bars split by date order",
                "candidate_id": best.get("candidate_id", ""),
                "parameter_tuning_allowed": 0,
                "minimum_dates": as_int(best.get("real_anchor_dates", 0)),
                "minimum_symbols": as_int(best.get("real_anchor_symbols", 0)),
                "minimum_trades": as_int(best.get("real_anchor_trades", 0)),
                "required_controls": "rolling_prefix_date_freeze;leave_one_date;cost_stress",
                "acceptance_rule": "diagnostic_only_not_promotional_even_if_positive",
                "result_claim_allowed": "diagnostic_only",
            },
        ]
    )


def build_phase239_work_order(best: dict[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "step_order": 1,
                "phase239_task": "acquire_or_materialize_unseen_real_l2_dates",
                "candidate_id": best.get("candidate_id", ""),
                "detail": f"Download/materialize at least {MIN_UNSEEN_VALIDATION_DATES} real L2 dates not present in Phase235/Phase237 discovery outputs.",
                "evidence": "date inventory proving new dates are outside Phase237 discovery sample",
            },
            {
                "step_order": 2,
                "phase239_task": "rebuild_phase235_event_bar_adapter_for_unseen_dates",
                "candidate_id": best.get("candidate_id", ""),
                "detail": "Use identical Phase235 event-bar adapter; no threshold recalibration on validation dates.",
                "evidence": "unseen real event-bar coverage summary",
            },
            {
                "step_order": 3,
                "phase239_task": "replay_frozen_phase237_candidate",
                "candidate_id": best.get("candidate_id", ""),
                "detail": "Apply frozen Phase237 event threshold, signal threshold, horizon, side rule and Zerodha cost model.",
                "evidence": "unseen validation trade ledger and summary",
            },
            {
                "step_order": 4,
                "phase239_task": "controls_and_decision",
                "candidate_id": best.get("candidate_id", ""),
                "detail": "Run side-flip, random-side, cost stress and concentration controls; decide validate, redesign or close.",
                "evidence": "Phase239 gate evaluation and no paper/live promotion boundary",
            },
        ]
    )


def build_gate_evaluation(availability: pd.DataFrame, contract: pd.DataFrame, candidate_freeze: pd.DataFrame) -> pd.DataFrame:
    frozen = bool(not candidate_freeze.empty and int(candidate_freeze["frozen_for_phase238"].iloc[0]) == 1)
    primary = contract[contract["contract_id"].astype(str).eq("P238_UNSEEN_REAL_ANCHOR_PRIMARY")]
    fallback = contract[contract["contract_id"].astype(str).eq("P238_WALK_FORWARD_DIAGNOSTIC_FALLBACK")]
    unseen_row = availability[availability["availability_check"].astype(str).eq("P238_TRULY_UNSEEN_LOCAL_DATES_AVAILABLE")]
    unseen_available = bool(not unseen_row.empty and bool(unseen_row["passed"].iloc[0]))
    rows = [
        ("P238_PHASE237_CANDIDATE_OPENED", frozen, candidate_freeze["candidate_id"].iloc[0] if frozen else "", "frozen Phase237 candidate", "hard"),
        ("P238_PRIMARY_UNSEEN_CONTRACT_WRITTEN", not primary.empty, int(not primary.empty), 1, "hard"),
        ("P238_DIAGNOSTIC_FALLBACK_CONTRACT_WRITTEN", not fallback.empty, int(not fallback.empty), 1, "hard"),
        ("P238_LOCAL_UNSEEN_ACCEPTANCE_DATA_AVAILABLE_NOW", unseen_available, int(unseen_available), 1, "soft"),
        ("P238_PHASE239_WORK_ORDER_REQUIRED", not unseen_available, int(not unseen_available), 1, "hard"),
        ("P238_NO_PAPER_LIVE_OR_PROMOTION_UNLOCK", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase238 Validation Precommit Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase238 freezes the Phase237 candidate and precommits validation rules.",
        "It does not validate on the same real-anchor sample used for Phase237 threshold-transfer discovery.",
        "The primary validation route requires unseen real L2 dates; the current local sample supports only diagnostic walk-forward checks.",
        "",
    ]
    for title, table in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(table), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    phase237_dir: Path = DEFAULT_PHASE237_DIR,
    bars_path: Path = DEFAULT_PHASE235_BARS,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    best = load_best_candidate(phase237_dir)
    candidate_freeze = build_candidate_freeze(best)
    availability = build_availability(bars_path, phase237_dir, candidate_freeze)
    contract = build_validation_contract(best)
    work_order = build_phase239_work_order(best)
    gates = build_gate_evaluation(availability, contract, candidate_freeze)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    hard_rows = int(len(hard))
    unseen_available = bool(
        availability.loc[
            availability["availability_check"].astype(str).eq("P238_TRULY_UNSEEN_LOCAL_DATES_AVAILABLE"),
            "passed",
        ].iloc[0]
    )
    acceptance = pd.DataFrame(
        [
            ("phase238_validation_precommit_complete", 1, "Phase238 validation precommit completed"),
            ("phase238_candidate_id", candidate_freeze["candidate_id"].iloc[0], "Frozen Phase237 candidate"),
            ("phase238_phase237_net_pnl_inr", candidate_freeze["phase237_net_pnl_inr"].iloc[0], "Phase237 discovery net P&L"),
            ("phase238_phase237_trade_rows", candidate_freeze["phase237_trades"].iloc[0], "Phase237 discovery trade count"),
            ("phase238_phase237_dates", candidate_freeze["phase237_dates"].iloc[0], "Phase237 discovery date count"),
            ("phase238_phase237_symbols", candidate_freeze["phase237_symbols"].iloc[0], "Phase237 discovery symbol count"),
            ("phase238_primary_validation_contract_rows", int(contract["contract_id"].astype(str).eq("P238_UNSEEN_REAL_ANCHOR_PRIMARY").sum()), "Primary unseen-validation contracts"),
            ("phase238_walk_forward_diagnostic_contract_rows", int(contract["contract_id"].astype(str).eq("P238_WALK_FORWARD_DIAGNOSTIC_FALLBACK").sum()), "Diagnostic fallback contracts"),
            ("phase238_local_unseen_validation_dates_available", int(unseen_available), "Whether enough local unseen validation dates exist now"),
            ("phase238_min_unseen_validation_dates_required", MIN_UNSEEN_VALIDATION_DATES, "Minimum unseen dates required"),
            ("phase238_phase239_work_order_rows", int(len(work_order)), "Phase239 work-order rows"),
            ("phase238_hard_gate_pass_rows", hard_pass, "Hard Phase238 gates passed"),
            ("phase238_hard_gate_rows", hard_rows, "Hard Phase238 gates evaluated"),
            ("phase238_strategy_promotion_allowed", 0, "No strategy promotion from Phase238"),
            ("phase238_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase238"),
            ("phase238_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase238"),
            ("phase238_next_best_action", "run_phase239_acquire_or_materialize_unseen_real_anchor_validation_dates_no_paper_live", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    candidate_freeze.to_csv(output_dir / "phase238_frozen_candidate_spec.csv", index=False)
    availability.to_csv(output_dir / "phase238_validation_data_availability.csv", index=False)
    contract.to_csv(output_dir / "phase238_validation_contract.csv", index=False)
    work_order.to_csv(output_dir / "phase238_phase239_work_order.csv", index=False)
    gates.to_csv(output_dir / "phase238_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase238_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase238_validation_precommit_report.md",
        {
            "Acceptance Summary": acceptance,
            "Frozen Candidate": candidate_freeze,
            "Validation Data Availability": availability,
            "Validation Contract": contract,
            "Phase239 Work Order": work_order,
            "Gate Evaluation": gates,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase238_validation_precommit",
        **reproducibility_fields(
            artifact_id="phase238",
            generated_utc=generated_utc,
            inputs={
                "phase237_dir": str(phase237_dir),
                "phase235_real_event_bars": str(bars_path),
            },
            parameters={
                "min_unseen_validation_dates": MIN_UNSEEN_VALIDATION_DATES,
                "min_validation_symbols": MIN_VALIDATION_SYMBOLS,
                "min_validation_trades": MIN_VALIDATION_TRADES,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "frozen_candidate_spec": str(output_dir / "phase238_frozen_candidate_spec.csv"),
                "validation_data_availability": str(output_dir / "phase238_validation_data_availability.csv"),
                "validation_contract": str(output_dir / "phase238_validation_contract.csv"),
                "phase239_work_order": str(output_dir / "phase238_phase239_work_order.csv"),
                "gate_evaluation": str(output_dir / "phase238_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase238_acceptance_summary.csv"),
                "report": str(output_dir / "phase238_validation_precommit_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase235_real_anchor_event_bar_adapter",
        ),
    }
    (output_dir / "phase238_validation_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Precommit Phase238 validation for the Phase237 candidate.")
    parser.add_argument("--phase237-dir", type=Path, default=DEFAULT_PHASE237_DIR)
    parser.add_argument("--bars-path", type=Path, default=DEFAULT_PHASE235_BARS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase237_dir=args.phase237_dir, bars_path=args.bars_path, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
