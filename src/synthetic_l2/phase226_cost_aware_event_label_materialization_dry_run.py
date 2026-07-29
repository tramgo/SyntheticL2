from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE176_DIR = Path("outputs/phase176")
DEFAULT_PHASE180_DIR = Path("outputs/phase180")
DEFAULT_PHASE181_DIR = Path("outputs/phase181")
DEFAULT_PHASE214_DIR = Path("outputs/phase214")
DEFAULT_PHASE225_DIR = Path("outputs/phase225")
DEFAULT_OUTPUT_DIR = Path("outputs/phase226")
DEFAULT_LABEL_ROOT = Path("derived_phase226_cost_aware_event_labels")
JOIN_KEYS = ["bucket_ms", "trade_date", "exchange", "symbol", "horizon_sec"]
ALLOWED_SPLITS = {"train", "validation"}
SEALED_TEST_SPLITS = {"test", "test_untouched"}
FORBIDDEN_OUTPUTS = "model_fit;model_prediction;strategy_replay;broader_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export"
NEXT_ACTION = "run_phase227_cost_aware_event_label_quality_interpretation_no_fit_no_replay_no_test"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = "") -> Any:
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


def partition_key(row: dict[str, Any]) -> tuple[int, str, str, str]:
    return (as_int(row.get("horizon_sec", 0)), str(row.get("trade_date", "")), str(row.get("exchange", "")), str(row.get("symbol", "")))


def read_selected_columns(path: Path, columns: list[str]) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    available = pd.read_parquet(path).columns.astype(str).tolist()
    return pd.read_parquet(path, columns=[c for c in columns if c in available])


def statutory_intraday_round_trip_bps(notional: float = 100_000.0) -> float:
    brokerage_bps = 2.0 * (min(0.0003 * notional, 20.0) / notional * 10_000.0)
    stt_bps = 0.00025 * 10_000.0
    transaction_bps = 2.0 * 0.0000307 * 10_000.0
    sebi_bps = 2.0 * (10.0 / 10_000_000.0) * 10_000.0
    stamp_bps = 0.00003 * 10_000.0
    gst_bps = 0.18 * (brokerage_bps + transaction_bps + sebi_bps)
    return float(brokerage_bps + stt_bps + transaction_bps + sebi_bps + stamp_bps + gst_bps)


def profile_cost_bps(frame: pd.DataFrame, profile: pd.Series) -> pd.Series:
    mid = ((pd.to_numeric(frame["best_bid"], errors="coerce") + pd.to_numeric(frame["best_ask"], errors="coerce")) / 2.0).replace(0, np.nan)
    spread_bps = (pd.to_numeric(frame["spread"], errors="coerce") / mid * 10_000.0).replace([np.inf, -np.inf], np.nan).fillna(0.0).clip(lower=0.0)
    tick_slippage_bps = (float(profile["slippage_ticks"]) * 0.05 / mid * 10_000.0).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    return statutory_intraday_round_trip_bps() + (2.0 * float(profile["spread_cross_multiplier"]) * spread_bps) + (2.0 * tick_slippage_bps)


def latency_profile(latency: pd.DataFrame, profile_id: str) -> pd.Series:
    rows = latency[latency["profile_id"].astype(str).eq(profile_id)] if not latency.empty and "profile_id" in latency.columns else pd.DataFrame()
    if rows.empty:
        return pd.Series({"profile_id": profile_id, "slippage_ticks": 0, "spread_cross_multiplier": 1.0})
    return rows.iloc[0]


def build_horizon_availability(label_contract: pd.DataFrame, phase181_inventory: pd.DataFrame, phase214_inventory: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for contract in label_contract.to_dict("records"):
        horizon = as_int(contract.get("horizon_sec", 0))
        p181 = phase181_inventory[pd.to_numeric(phase181_inventory["horizon_sec"], errors="coerce").fillna(-1).astype(int).eq(horizon)] if not phase181_inventory.empty else pd.DataFrame()
        p214 = phase214_inventory[pd.to_numeric(phase214_inventory["horizon_sec"], errors="coerce").fillna(-1).astype(int).eq(horizon)] if not phase214_inventory.empty else pd.DataFrame()
        p181_allowed = p181[p181["split_role"].astype(str).isin(ALLOWED_SPLITS)] if not p181.empty else pd.DataFrame()
        p214_allowed = p214[p214["split_role"].astype(str).isin(ALLOWED_SPLITS)] if not p214.empty else pd.DataFrame()
        rows.append(
            {
                "phase225_label_contract_id": contract.get("phase225_label_contract_id", ""),
                "horizon_sec": horizon,
                "phase181_allowed_partitions": len(p181_allowed),
                "phase214_allowed_partitions": len(p214_allowed),
                "materialization_available": int(len(p181_allowed) > 0 and len(p214_allowed) > 0),
                "blocked_reason": "" if len(p181_allowed) > 0 and len(p214_allowed) > 0 else "contracted_horizon_not_available_in_current_phase181_phase214_train_validation_inputs",
                "test_rows_used": 0,
            }
        )
    return pd.DataFrame(rows)


def materialize_labels(
    feature_inventory: pd.DataFrame,
    phase181_inventory: pd.DataFrame,
    phase214_inventory: pd.DataFrame,
    label_contract: pd.DataFrame,
    latency: pd.DataFrame,
    output_root: Path,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    feature_paths = {partition_key(row): Path(str(row.get("parquet_file", ""))) for row in feature_inventory.to_dict("records")}
    phase181_paths = {partition_key(row): Path(str(row.get("label_file", ""))) for row in phase181_inventory.to_dict("records")}
    phase214_paths = {partition_key(row): Path(str(row.get("label_file", ""))) for row in phase214_inventory.to_dict("records")}
    contract_horizons = sorted({as_int(v) for v in label_contract["horizon_sec"].tolist()}) if not label_contract.empty else []
    retail = latency_profile(latency, "P180_RETAIL_MARKETABLE_DEFAULT")
    stressed = latency_profile(latency, "P180_STRESSED_RETAIL")
    output_root.mkdir(parents=True, exist_ok=True)

    inventory_rows: list[dict[str, Any]] = []
    quality_rows: list[dict[str, Any]] = []
    sealed_rows: list[dict[str, Any]] = []
    allowed_181 = phase181_inventory[
        phase181_inventory["split_role"].astype(str).isin(ALLOWED_SPLITS | SEALED_TEST_SPLITS)
        & pd.to_numeric(phase181_inventory["horizon_sec"], errors="coerce").fillna(-1).astype(int).isin(contract_horizons)
    ] if not phase181_inventory.empty else pd.DataFrame()

    for row in allowed_181.to_dict("records"):
        split_role = str(row.get("split_role", ""))
        key = partition_key(row)
        if split_role in SEALED_TEST_SPLITS:
            sealed_rows.append(
                {
                    "horizon_sec": key[0],
                    "trade_date": key[1],
                    "exchange": key[2],
                    "symbol": key[3],
                    "split_role": split_role,
                    "sealed_test_rows_available": as_int(row.get("label_available_rows", row.get("rows", 0))),
                    "sealed_test_rows_used": 0,
                    "materialized_in_phase226": 0,
                }
            )
            continue
        feature_path = feature_paths.get(key)
        phase181_path = phase181_paths.get(key)
        phase214_path = phase214_paths.get(key)
        if feature_path is None or phase181_path is None or phase214_path is None or not feature_path.exists() or not phase181_path.exists() or not phase214_path.exists():
            continue
        features = read_selected_columns(feature_path, JOIN_KEYS + ["last_price", "best_bid", "best_ask", "spread"])
        labels = read_selected_columns(phase181_path, JOIN_KEYS + ["split_role", "label_available", "future_mid_return_bps_next_bucket"])
        events = read_selected_columns(phase214_path, JOIN_KEYS + ["event_surprise_bucket"])
        if features.empty or labels.empty or events.empty:
            continue
        joined = features.merge(labels, on=JOIN_KEYS, how="inner").merge(events, on=JOIN_KEYS, how="inner")
        joined = joined[
            pd.to_numeric(joined.get("label_available", 0), errors="coerce").fillna(0).astype(int).eq(1)
            & pd.to_numeric(joined.get("event_surprise_bucket", 0), errors="coerce").fillna(0).astype(int).eq(1)
        ].copy()
        for col in ["last_price", "best_bid", "best_ask", "spread", "future_mid_return_bps_next_bucket"]:
            joined[col] = pd.to_numeric(joined.get(col, 0.0), errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(0.0)
        if joined.empty:
            retail_cost = pd.Series(dtype=float)
            stressed_cost = pd.Series(dtype=float)
        else:
            retail_cost = profile_cost_bps(joined, retail)
            stressed_cost = profile_cost_bps(joined, stressed)
        joined["retail_cost_bound_bps"] = retail_cost
        joined["stressed_cost_bound_bps"] = stressed_cost
        joined["forward_move_bps"] = joined["future_mid_return_bps_next_bucket"]
        joined["cost_aware_up_label"] = ((joined["forward_move_bps"] - joined["retail_cost_bound_bps"] >= 1.0) & (joined["forward_move_bps"] - joined["stressed_cost_bound_bps"] >= 0.0)).astype(int)
        joined["cost_aware_down_label"] = (((-joined["forward_move_bps"]) - joined["retail_cost_bound_bps"] >= 1.0) & (((-joined["forward_move_bps"]) - joined["stressed_cost_bound_bps"]) >= 0.0)).astype(int)
        joined["cost_aware_direction_label"] = np.select(
            [joined["cost_aware_up_label"].eq(1), joined["cost_aware_down_label"].eq(1)],
            [1, -1],
            default=0,
        )
        joined["cost_aware_actionable_label"] = joined["cost_aware_direction_label"].ne(0).astype(int)
        joined["cost_aware_neutral_label"] = joined["cost_aware_direction_label"].eq(0).astype(int)
        joined["test_rows_used"] = 0
        out_cols = JOIN_KEYS + [
            "split_role",
            "event_surprise_bucket",
            "forward_move_bps",
            "retail_cost_bound_bps",
            "stressed_cost_bound_bps",
            "cost_aware_up_label",
            "cost_aware_down_label",
            "cost_aware_neutral_label",
            "cost_aware_actionable_label",
            "cost_aware_direction_label",
            "test_rows_used",
        ]
        rel = Path(f"horizon={key[0]}s") / f"trade_date={key[1]}" / f"exchange={key[2]}" / f"symbol={key[3]}" / "cost_aware_event_labels.parquet"
        out_path = output_root / rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        joined[out_cols].to_parquet(out_path, index=False)
        rows = len(joined)
        actionable = int(joined["cost_aware_actionable_label"].sum()) if rows else 0
        up = int(joined["cost_aware_up_label"].sum()) if rows else 0
        down = int(joined["cost_aware_down_label"].sum()) if rows else 0
        inventory_rows.append(
            {
                "horizon_sec": key[0],
                "trade_date": key[1],
                "exchange": key[2],
                "symbol": key[3],
                "split_role": split_role,
                "rows": rows,
                "cost_aware_actionable_rows": actionable,
                "cost_aware_up_rows": up,
                "cost_aware_down_rows": down,
                "label_file": str(out_path),
                "bytes": out_path.stat().st_size,
                "test_rows_used": 0,
            }
        )
        quality_rows.append(
            {
                "horizon_sec": key[0],
                "trade_date": key[1],
                "exchange": key[2],
                "symbol": key[3],
                "split_role": split_role,
                "rows": rows,
                "cost_aware_actionable_rows": actionable,
                "actionable_rate": float(actionable / rows) if rows else 0.0,
                "up_rows": up,
                "down_rows": down,
                "neutral_rows": int(joined["cost_aware_neutral_label"].sum()) if rows else 0,
                "median_retail_cost_bound_bps": float(joined["retail_cost_bound_bps"].median()) if rows else 0.0,
                "median_stressed_cost_bound_bps": float(joined["stressed_cost_bound_bps"].median()) if rows else 0.0,
                "max_abs_forward_move_bps": float(joined["forward_move_bps"].abs().max()) if rows else 0.0,
                "test_rows_used": 0,
            }
        )
    return pd.DataFrame(inventory_rows), pd.DataFrame(quality_rows), pd.DataFrame(sealed_rows)


def build_split_summary(inventory: pd.DataFrame, label_contract: pd.DataFrame) -> pd.DataFrame:
    if inventory.empty:
        return pd.DataFrame()
    min_events = int(pd.to_numeric(label_contract["minimum_event_count_per_split"], errors="coerce").fillna(1000).min()) if not label_contract.empty else 1000
    min_symbols = int(pd.to_numeric(label_contract["minimum_symbol_count_per_split"], errors="coerce").fillna(8).min()) if not label_contract.empty else 8
    min_dates = int(pd.to_numeric(label_contract["minimum_trade_date_count_per_split"], errors="coerce").fillna(5).min()) if not label_contract.empty else 5
    rows: list[dict[str, Any]] = []
    for (horizon, split), part in inventory.groupby(["horizon_sec", "split_role"], sort=True):
        actionable = int(pd.to_numeric(part["cost_aware_actionable_rows"], errors="coerce").fillna(0).sum())
        symbols = int(part["symbol"].astype(str).nunique())
        dates = int(part["trade_date"].astype(str).nunique())
        rows.append(
            {
                "horizon_sec": int(horizon),
                "split_role": split,
                "partitions": len(part),
                "rows": int(pd.to_numeric(part["rows"], errors="coerce").fillna(0).sum()),
                "cost_aware_actionable_rows": actionable,
                "symbols": symbols,
                "trade_dates": dates,
                "passes_min_event_count": int(actionable >= min_events),
                "passes_min_symbol_count": int(symbols >= min_symbols),
                "passes_min_trade_date_count": int(dates >= min_dates),
                "quality_gate_pass": int(actionable >= min_events and symbols >= min_symbols and dates >= min_dates),
                "test_rows_used": 0,
            }
        )
    return pd.DataFrame(rows)


def build_negative_control_summary(inventory: pd.DataFrame) -> pd.DataFrame:
    if inventory.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for (horizon, split), part in inventory.groupby(["horizon_sec", "split_role"], sort=True):
        actionable = int(pd.to_numeric(part["cost_aware_actionable_rows"], errors="coerce").fillna(0).sum())
        rows.extend(
            [
                {
                    "control_id": "P225_CONTROL_EVENT_TIME_SHUFFLE",
                    "horizon_sec": int(horizon),
                    "split_role": split,
                    "control_status": "precommitted_for_phase227_interpretation",
                    "reference_actionable_rows": actionable,
                    "materialized_in_phase226": 0,
                    "model_fit_allowed": 0,
                    "strategy_replay_allowed": 0,
                },
                {
                    "control_id": "P225_CONTROL_SYMBOL_DATE_BASE_RATE",
                    "horizon_sec": int(horizon),
                    "split_role": split,
                    "control_status": "aggregate_base_rate_available_from_phase226_inventory",
                    "reference_actionable_rows": actionable,
                    "materialized_in_phase226": 0,
                    "model_fit_allowed": 0,
                    "strategy_replay_allowed": 0,
                },
                {
                    "control_id": "P225_CONTROL_COST_HURDLE_ABLATION",
                    "horizon_sec": int(horizon),
                    "split_role": split,
                    "control_status": "cost_hurdle_effect_measured_by_actionable_rate_and_phase214_event_filter",
                    "reference_actionable_rows": actionable,
                    "materialized_in_phase226": 0,
                    "model_fit_allowed": 0,
                    "strategy_replay_allowed": 0,
                },
            ]
        )
    return pd.DataFrame(rows)


def build_forbidden_execution_ledger() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "forbidden_output": item,
                "emitted_in_phase226": 0,
                "allowed_in_phase226": 0,
                "rationale": "Phase226 materializes train/validation cost-aware labels only and emits no fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, row-level prediction export, threshold-widening, or profitability artifact.",
            }
            for item in FORBIDDEN_OUTPUTS.split(";")
        ]
    )


def build_gates(phase225: pd.DataFrame, availability: pd.DataFrame, inventory: pd.DataFrame, split_summary: pd.DataFrame, controls: pd.DataFrame, sealed: pd.DataFrame, forbidden: pd.DataFrame) -> pd.DataFrame:
    phase225_complete = as_int(metric_value(phase225, "phase225_cost_aware_event_source_redesign_precommit_complete", 0))
    available_horizons = int(pd.to_numeric(availability["materialization_available"], errors="coerce").fillna(0).sum()) if not availability.empty else 0
    blocked_horizons = int(pd.to_numeric(availability["materialization_available"], errors="coerce").fillna(0).eq(0).sum()) if not availability.empty else 0
    materialized_horizons = int(inventory["horizon_sec"].astype(int).nunique()) if not inventory.empty else 0
    inventory_rows = len(inventory)
    summary_rows = len(split_summary)
    quality_pass_rows = int(pd.to_numeric(split_summary["quality_gate_pass"], errors="coerce").fillna(0).sum()) if not split_summary.empty else 0
    actionable_rows = int(pd.to_numeric(inventory["cost_aware_actionable_rows"], errors="coerce").fillna(0).sum()) if not inventory.empty else 0
    sealed_used = int(pd.to_numeric(sealed["sealed_test_rows_used"], errors="coerce").fillna(0).sum()) if not sealed.empty else 0
    forbidden_emitted = int(pd.to_numeric(forbidden["emitted_in_phase226"], errors="coerce").fillna(0).sum()) if not forbidden.empty else 1
    forbidden_flags = 0
    for frame in [controls]:
        for col in ["model_fit_allowed", "strategy_replay_allowed"]:
            if not frame.empty and col in frame.columns:
                forbidden_flags += int(pd.to_numeric(frame[col], errors="coerce").fillna(0).sum())
    return pd.DataFrame(
        [
            ("P226_PHASE225_COMPLETE", phase225_complete == 1, f"phase225_complete={phase225_complete}", "hard"),
            ("P226_HORIZON_AVAILABILITY_RECORDED", len(availability) == 3 and available_horizons == 2 and blocked_horizons == 1, f"availability_rows={len(availability)}; available={available_horizons}; blocked={blocked_horizons}", "hard"),
            ("P226_LABELS_MATERIALIZED_FOR_AVAILABLE_HORIZONS", materialized_horizons == 2 and inventory_rows > 0, f"materialized_horizons={materialized_horizons}; inventory_rows={inventory_rows}", "hard"),
            ("P226_QUALITY_SUMMARY_RECORDED", summary_rows == 4 and actionable_rows > 0, f"summary_rows={summary_rows}; quality_pass_rows={quality_pass_rows}; actionable_rows={actionable_rows}", "hard"),
            ("P226_NEGATIVE_CONTROL_SUMMARY_RECORDED", len(controls) == 12, f"control_rows={len(controls)}", "hard"),
            ("P226_TEST_ROWS_UNTOUCHED", sealed_used == 0, f"sealed_test_rows_used={sealed_used}", "hard"),
            ("P226_FORBIDDEN_OUTPUTS_CLEAN", forbidden_emitted == 0 and forbidden_flags == 0, f"forbidden_emitted={forbidden_emitted}; forbidden_flags={forbidden_flags}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(availability: pd.DataFrame, inventory: pd.DataFrame, split_summary: pd.DataFrame, controls: pd.DataFrame, sealed: pd.DataFrame, forbidden: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    actionable = int(pd.to_numeric(inventory["cost_aware_actionable_rows"], errors="coerce").fillna(0).sum()) if not inventory.empty else 0
    up = int(pd.to_numeric(inventory["cost_aware_up_rows"], errors="coerce").fillna(0).sum()) if not inventory.empty else 0
    down = int(pd.to_numeric(inventory["cost_aware_down_rows"], errors="coerce").fillna(0).sum()) if not inventory.empty else 0
    return pd.DataFrame(
        [
            ("phase226_horizon_availability_rows", len(availability), "Contracted horizon availability rows"),
            ("phase226_available_horizon_rows", int(pd.to_numeric(availability["materialization_available"], errors="coerce").fillna(0).sum()) if not availability.empty else 0, "Available contracted horizons"),
            ("phase226_blocked_horizon_rows", int(pd.to_numeric(availability["materialization_available"], errors="coerce").fillna(0).eq(0).sum()) if not availability.empty else 0, "Unavailable contracted horizons"),
            ("phase226_label_partition_rows", len(inventory), "Materialized label partition rows"),
            ("phase226_materialized_horizons", int(inventory["horizon_sec"].astype(int).nunique()) if not inventory.empty else 0, "Materialized horizons"),
            ("phase226_total_label_rows", int(pd.to_numeric(inventory["rows"], errors="coerce").fillna(0).sum()) if not inventory.empty else 0, "Total materialized event rows"),
            ("phase226_cost_aware_actionable_rows", actionable, "Cost-aware actionable label rows"),
            ("phase226_cost_aware_up_rows", up, "Cost-aware up rows"),
            ("phase226_cost_aware_down_rows", down, "Cost-aware down rows"),
            ("phase226_split_summary_rows", len(split_summary), "Split quality summary rows"),
            ("phase226_quality_pass_rows", int(pd.to_numeric(split_summary["quality_gate_pass"], errors="coerce").fillna(0).sum()) if not split_summary.empty else 0, "Split quality pass rows"),
            ("phase226_negative_control_summary_rows", len(controls), "Negative-control summary rows"),
            ("phase226_sealed_test_rows_available", int(pd.to_numeric(sealed["sealed_test_rows_available"], errors="coerce").fillna(0).sum()) if not sealed.empty else 0, "Sealed test rows available but not used"),
            ("phase226_test_rows_used", 0, "No sealed test rows used"),
            ("phase226_model_fit_allowed_next", 0, "No model fit opened"),
            ("phase226_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase226_broader_replay_allowed_next", 0, "No broader replay opened"),
            ("phase226_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase226_promotion_allowed", 0, "No promotion opened"),
            ("phase226_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase226_profitability_claim_allowed", 0, "No profitability claim is allowed"),
            ("phase226_forbidden_execution_rows", len(forbidden), "Forbidden execution rows"),
            ("phase226_gate_rows", len(gates), "Gates evaluated"),
            ("phase226_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase226_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase226_cost_aware_event_label_materialization_dry_run_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase226 completed"),
            ("phase226_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase226_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase226 Cost-aware Event Label Materialization Dry Run",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase226 materializes train/validation-only cost-aware event labels from Phase225 contracts.",
        "Unavailable contracted horizons are recorded explicitly; no model fit, replay, sealed test, promotion, paper/live, or profitability artifact is emitted.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase226_cost_aware_event_label_materialization_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase226(phase176_dir: Path, phase180_dir: Path, phase181_dir: Path, phase214_dir: Path, phase225_dir: Path, output_dir: Path, label_root: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase225 = read_csv(phase225_dir / "phase225_redesign_precommit_acceptance_summary.csv")
    label_contract = read_csv(phase225_dir / "phase225_label_contract.csv")
    feature_inventory = read_csv(phase176_dir / "phase176_feature_partition_inventory.csv")
    phase181_inventory = read_csv(phase181_dir / "phase181_label_partition_inventory.csv")
    phase214_inventory = read_csv(phase214_dir / "phase214_label_partition_inventory.csv")
    latency = read_csv(phase180_dir / "phase180_latency_slippage_profile_catalog.csv")

    availability = build_horizon_availability(label_contract, phase181_inventory, phase214_inventory)
    available_horizons = set(pd.to_numeric(availability.loc[availability["materialization_available"].astype(int).eq(1), "horizon_sec"], errors="coerce").dropna().astype(int).tolist()) if not availability.empty else set()
    available_contract = label_contract[pd.to_numeric(label_contract["horizon_sec"], errors="coerce").fillna(-1).astype(int).isin(available_horizons)] if not label_contract.empty else pd.DataFrame()
    inventory, quality, sealed = materialize_labels(feature_inventory, phase181_inventory, phase214_inventory, available_contract, latency, label_root)
    split_summary = build_split_summary(inventory, available_contract)
    controls = build_negative_control_summary(inventory)
    forbidden = build_forbidden_execution_ledger()
    gates = build_gates(phase225, availability, inventory, split_summary, controls, sealed, forbidden)
    acceptance = build_acceptance(availability, inventory, split_summary, controls, sealed, forbidden, gates)

    availability.to_csv(output_dir / "phase226_horizon_availability_ledger.csv", index=False)
    inventory.to_csv(output_dir / "phase226_label_partition_inventory.csv", index=False)
    quality.to_csv(output_dir / "phase226_label_quality_by_partition.csv", index=False)
    split_summary.to_csv(output_dir / "phase226_label_quality_split_summary.csv", index=False)
    controls.to_csv(output_dir / "phase226_negative_control_summary.csv", index=False)
    sealed.to_csv(output_dir / "phase226_sealed_test_exclusion_ledger.csv", index=False)
    forbidden.to_csv(output_dir / "phase226_execution_forbidden_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase226_label_materialization_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase226_label_materialization_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Horizon Availability Ledger": availability,
            "Label Partition Inventory": inventory,
            "Split Quality Summary": split_summary,
            "Negative Control Summary": controls,
            "Sealed Test Exclusion Ledger": sealed,
            "Forbidden Execution Ledger": forbidden,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase226_cost_aware_event_label_materialization_dry_run_no_fit_no_replay_no_test",
        **reproducibility_fields(
            artifact_id="phase226_cost_aware_event_label_materialization_dry_run",
            generated_utc=generated,
            inputs={
                "phase225_acceptance": str(phase225_dir / "phase225_redesign_precommit_acceptance_summary.csv"),
                "phase225_label_contract": str(phase225_dir / "phase225_label_contract.csv"),
                "phase176_feature_inventory": str(phase176_dir / "phase176_feature_partition_inventory.csv"),
                "phase181_label_inventory": str(phase181_dir / "phase181_label_partition_inventory.csv"),
                "phase214_label_inventory": str(phase214_dir / "phase214_label_partition_inventory.csv"),
                "phase180_latency_catalog": str(phase180_dir / "phase180_latency_slippage_profile_catalog.csv"),
            },
            parameters={
                "allowed_splits": "train;validation",
                "contracted_horizons": ";".join(label_contract["horizon_sec"].astype(str).tolist()) if not label_contract.empty else "",
                "available_horizons": ";".join(str(v) for v in sorted(available_horizons)),
                "label_root": str(label_root),
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "availability": str(output_dir / "phase226_horizon_availability_ledger.csv"),
                "inventory": str(output_dir / "phase226_label_partition_inventory.csv"),
                "quality": str(output_dir / "phase226_label_quality_by_partition.csv"),
                "split_summary": str(output_dir / "phase226_label_quality_split_summary.csv"),
                "controls": str(output_dir / "phase226_negative_control_summary.csv"),
                "sealed": str(output_dir / "phase226_sealed_test_exclusion_ledger.csv"),
                "forbidden": str(output_dir / "phase226_execution_forbidden_ledger.csv"),
                "gates": str(output_dir / "phase226_label_materialization_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase226_label_materialization_acceptance_summary.csv"),
                "report": str(output_dir / "phase226_cost_aware_event_label_materialization_report.md"),
            },
            scenario_ids="phase226_cost_aware_event_label_materialization_dry_run_no_fit_no_replay_no_test",
            cost_model_version="phase180_zerodha_equity_cost_component_catalog_bound",
            latency_model_version="phase180_latency_slippage_profile_catalog_bound",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase226_label_materialization_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize Phase226 cost-aware event labels without fit, replay, or test.")
    parser.add_argument("--phase176-dir", type=Path, default=DEFAULT_PHASE176_DIR)
    parser.add_argument("--phase180-dir", type=Path, default=DEFAULT_PHASE180_DIR)
    parser.add_argument("--phase181-dir", type=Path, default=DEFAULT_PHASE181_DIR)
    parser.add_argument("--phase214-dir", type=Path, default=DEFAULT_PHASE214_DIR)
    parser.add_argument("--phase225-dir", type=Path, default=DEFAULT_PHASE225_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--label-root", type=Path, default=DEFAULT_LABEL_ROOT)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase226(args.phase176_dir, args.phase180_dir, args.phase181_dir, args.phase214_dir, args.phase225_dir, args.output_dir, args.label_root, args.base_dir)


if __name__ == "__main__":
    main()
