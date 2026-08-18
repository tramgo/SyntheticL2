from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase469_source_event_aware_feature_repair_precommit import MIN_VARYING_FEATURES, THESIS_ID as PHASE469_THESIS_ID
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE467_DIR = Path("outputs/phase467")
DEFAULT_PHASE469_DIR = Path("outputs/phase469")
DEFAULT_OUTPUT_DIR = Path("outputs/phase470")

THESIS_ID = "P470_MATERIALIZE_SOURCE_EVENT_AWARE_L1_L5_FEATURE_MATRIX"
NEXT_ACTION_HAS_MATRIX = "precommit_phase471_train_holdout_source_event_aware_l1_l5_model_no_replay"
NEXT_ACTION_NO_MATRIX = "repair_phase470_source_event_aware_matrix_before_model_precommit"

BATCH_SIZE = 50_000
STARTS = [0, 5000, 10000, 20000, 50000]
PREHISTORY_ROWS = 512
SOURCE_EVENT_LOOKBACKS = [1, 3, 5]

RAW_COLUMNS = [
    "exchange_timestamp_ms",
    "trade_date",
    "exchange",
    "symbol",
    "source_annual_event_id",
    "last_price",
    "last_traded_quantity",
    "volume_traded",
    "total_buy_quantity",
    "total_sell_quantity",
]
for _level in range(1, 6):
    RAW_COLUMNS.extend(
        [
            f"buy_{_level}_price",
            f"buy_{_level}_quantity",
            f"buy_{_level}_orders",
            f"sell_{_level}_price",
            f"sell_{_level}_quantity",
            f"sell_{_level}_orders",
        ]
    )


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def cval(contract: pd.DataFrame, key: str, default: str = "") -> str:
    rows = contract.loc[contract["contract_id"].astype(str).eq(key), "contract_value"].astype(str).tolist()
    return rows[0] if rows else default


def ival(contract: pd.DataFrame, key: str, default: int) -> int:
    try:
        return int(float(cval(contract, key, str(default))))
    except ValueError:
        return default


def fval(contract: pd.DataFrame, key: str, default: float) -> float:
    try:
        return float(cval(contract, key, str(default)))
    except ValueError:
        return default


def sval(summary: pd.DataFrame, key: str, default: Any = 0) -> Any:
    rows = summary.loc[summary["metric"].eq(key), "value"].tolist()
    return rows[0] if rows else default


def safe_ratio(numerator: float, denominator: float) -> float:
    return float(numerator / denominator) if abs(denominator) > 1e-12 else 0.0


def slope(values: np.ndarray) -> float:
    if len(values) < 2:
        return 0.0
    x = np.arange(1, len(values) + 1, dtype=float)
    return float(np.polyfit(x, values.astype(float), 1)[0])


def mid(row: pd.Series) -> float:
    return (float(row["buy_1_price"]) + float(row["sell_1_price"])) / 2.0


def spread_bps(row: pd.Series) -> float:
    row_mid = mid(row)
    return safe_ratio(float(row["sell_1_price"]) - float(row["buy_1_price"]), row_mid) * 10_000.0


def l25_depth(row: pd.Series) -> float:
    return float(sum(float(row[f"buy_{level}_quantity"]) + float(row[f"sell_{level}_quantity"]) for level in range(2, 6)))


def read_candidate_windows(path: Path, month: str, starts: list[int], rows_per_window: int, prehistory_rows: int) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=RAW_COLUMNS + ["candidate_start_row", "window_local_row"])
    min_keep = min(starts) - prehistory_rows
    max_end = max(starts) + rows_per_window
    counts: dict[str, int] = {}
    parts = []
    pf = pq.ParquetFile(path)
    for batch in pf.iter_batches(batch_size=BATCH_SIZE, columns=RAW_COLUMNS):
        df = batch.to_pandas()
        if df.empty:
            continue
        df = df[df["trade_date"].astype(str).str.startswith(month)].copy()
        if df.empty:
            continue
        keep = []
        for trade_date, grp in df.groupby("trade_date", sort=False):
            key = str(trade_date)
            seen = counts.get(key, 0)
            n = len(grp)
            counts[key] = seen + n
            if seen >= max_end or seen + n <= min_keep:
                continue
            for start in starts:
                local_start = max(0, start - prehistory_rows - seen)
                local_end = min(n, start + rows_per_window - seen)
                if local_start < local_end:
                    window = grp.iloc[local_start:local_end].copy()
                    absolute_rows = range(seen + local_start, seen + local_end)
                    window["candidate_start_row"] = start
                    window["window_local_row"] = [row - start for row in absolute_rows]
                    keep.append(window)
        if keep:
            parts.append(pd.concat(keep, ignore_index=True))
    return pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=RAW_COLUMNS + ["candidate_start_row", "window_local_row"])


def source_event_rows(past: pd.DataFrame) -> pd.DataFrame:
    source = past.dropna(subset=["source_annual_event_id"]).copy()
    if source.empty:
        return past.tail(1).copy()
    source = source.sort_values(["source_annual_event_id", "window_local_row", "exchange_timestamp_ms"], kind="mergesort")
    source = source.drop_duplicates("source_annual_event_id", keep="last")
    return source.sort_values(["window_local_row", "exchange_timestamp_ms"], kind="mergesort").reset_index(drop=True)


def source_ref(source: pd.DataFrame, lookback: int) -> pd.Series:
    if source.empty:
        raise ValueError("source-event history is empty")
    index = max(0, len(source) - 1 - lookback)
    return source.iloc[index]


def compute_source_event_features(past: pd.DataFrame) -> dict[str, float]:
    source = source_event_rows(past)
    cur = source.iloc[-1]
    cur_mid = mid(cur)
    cur_l1_ofi_base = float(cur["buy_1_quantity"]) - float(cur["sell_1_quantity"])
    cur_l25_ofi_base = float(sum(float(cur[f"buy_{level}_quantity"]) - float(cur[f"sell_{level}_quantity"]) for level in range(2, 6)))
    features: dict[str, float] = {}
    for lookback in SOURCE_EVENT_LOOKBACKS:
        ref = source_ref(source, lookback)
        features[f"source_event_mid_return_{lookback}"] = safe_ratio(cur_mid - mid(ref), mid(ref)) * 10_000.0
    for lookback in [1, 3]:
        ref = source_ref(source, lookback)
        ref_l1_ofi_base = float(ref["buy_1_quantity"]) - float(ref["sell_1_quantity"])
        ref_l25_ofi_base = float(sum(float(ref[f"buy_{level}_quantity"]) - float(ref[f"sell_{level}_quantity"]) for level in range(2, 6)))
        features[f"source_event_l1_ofi_{lookback}"] = cur_l1_ofi_base - ref_l1_ofi_base
        features[f"source_event_l25_ofi_{lookback}"] = cur_l25_ofi_base - ref_l25_ofi_base
    recent = source.tail(6)
    l25_changes = np.diff(np.array([l25_depth(row) for _, row in recent.iterrows()], dtype=float))
    features["source_event_l25_replenishment_count_5"] = float((l25_changes > 0).sum())
    features["source_event_l25_withdrawal_count_5"] = float((l25_changes < 0).sum())
    spread_values = np.array([spread_bps(row) for _, row in source.tail(5).iterrows()], dtype=float)
    ref3 = source_ref(source, 3)
    features["source_event_spread_change_3_bps"] = spread_bps(cur) - spread_bps(ref3)
    features["source_event_spread_vol_5_bps"] = float(np.std(spread_values)) if len(spread_values) else 0.0
    features["source_event_distinct_history_rows"] = float(len(source))
    return features


def compute_record(g: pd.DataFrame, entry_index: int, horizon: int, min_abs_move_bps: float) -> dict[str, Any] | None:
    if g.empty:
        return None
    g = g.sort_values(["window_local_row", "exchange_timestamp_ms"], kind="mergesort").reset_index(drop=True)
    entry_matches = np.flatnonzero(g["window_local_row"].astype(int).to_numpy() == entry_index)
    exit_matches = np.flatnonzero(g["window_local_row"].astype(int).to_numpy() == entry_index + horizon)
    if len(entry_matches) == 0 or len(exit_matches) == 0:
        return None
    entry_pos = int(entry_matches[0])
    exit_pos = int(exit_matches[0])
    entry = g.iloc[entry_pos]
    exit_row = g.iloc[exit_pos]
    past = g.iloc[: entry_pos + 1].copy()
    dense_past = past.loc[past["window_local_row"].astype(int).ge(0)].copy()
    if dense_past.empty:
        dense_past = past.tail(1).copy()
    lookback_start = dense_past.iloc[0]
    bid_prices = np.array([float(entry[f"buy_{level}_price"]) for level in range(1, 6)], dtype=float)
    ask_prices = np.array([float(entry[f"sell_{level}_price"]) for level in range(1, 6)], dtype=float)
    bid_qty = np.array([float(entry[f"buy_{level}_quantity"]) for level in range(1, 6)], dtype=float)
    ask_qty = np.array([float(entry[f"sell_{level}_quantity"]) for level in range(1, 6)], dtype=float)
    bid_orders = np.array([float(entry[f"buy_{level}_orders"]) for level in range(1, 6)], dtype=float)
    ask_orders = np.array([float(entry[f"sell_{level}_orders"]) for level in range(1, 6)], dtype=float)
    entry_mid = mid(entry)
    exit_mid = mid(exit_row)
    if entry_mid <= 0:
        return None
    bid_l25 = float(bid_qty[1:].sum())
    ask_l25 = float(ask_qty[1:].sum())
    bid_l25_orders = float(bid_orders[1:].sum())
    ask_l25_orders = float(ask_orders[1:].sum())
    total_depth = float(bid_qty.sum() + ask_qty.sum())
    q_bid25 = dense_past[[f"buy_{level}_quantity" for level in range(2, 6)]].astype(float).sum(axis=1).to_numpy()
    q_ask25 = dense_past[[f"sell_{level}_quantity" for level in range(2, 6)]].astype(float).sum(axis=1).to_numpy()
    spread_series = (
        dense_past["sell_1_price"].astype(float).to_numpy()
        - dense_past["buy_1_price"].astype(float).to_numpy()
    ) / np.maximum(1e-9, (dense_past["sell_1_price"].astype(float).to_numpy() + dense_past["buy_1_price"].astype(float).to_numpy()) / 2.0) * 10_000.0
    trade_qty = dense_past["last_traded_quantity"].astype(float).to_numpy()
    half = max(1, len(trade_qty) // 2)
    l1_micro = safe_ratio(float(entry["sell_1_price"]) * float(entry["buy_1_quantity"]) + float(entry["buy_1_price"]) * float(entry["sell_1_quantity"]), float(entry["buy_1_quantity"]) + float(entry["sell_1_quantity"]))
    l25_micro = safe_ratio(float(np.dot(ask_prices[1:], bid_qty[1:]) + np.dot(bid_prices[1:], ask_qty[1:])), bid_l25 + ask_l25)
    forward = safe_ratio(exit_mid - entry_mid, entry_mid) * 10_000.0
    exchange_ts = int(entry["exchange_timestamp_ms"])
    rec: dict[str, Any] = {
        "trade_date": str(entry["trade_date"]),
        "exchange": str(entry["exchange"]),
        "symbol": str(entry["symbol"]),
        "candidate_start_row": int(entry["candidate_start_row"]),
        "entry_row": int(entry_index),
        "exit_row": int(entry_index + horizon),
        "entry_timestamp_ms": exchange_ts,
        "entry_price": entry_mid,
        "exit_price": exit_mid,
        "spread_bps": safe_ratio(float(entry["sell_1_price"]) - float(entry["buy_1_price"]), entry_mid) * 10_000.0,
        "l1_imbalance": safe_ratio(float(entry["buy_1_quantity"]) - float(entry["sell_1_quantity"]), float(entry["buy_1_quantity"]) + float(entry["sell_1_quantity"]) + 1.0),
        "l25_imbalance": safe_ratio(bid_l25 - ask_l25, bid_l25 + ask_l25 + 1.0),
        "volume_delta_lookback": float(entry["volume_traded"]) - float(lookback_start["volume_traded"]),
        "l1_l5_bid_depth_slope": slope(bid_qty),
        "l1_l5_ask_depth_slope": slope(ask_qty),
        "l1_l5_depth_concentration": safe_ratio(float(bid_qty[0] + ask_qty[0]), total_depth),
        "l25_order_imbalance": safe_ratio(bid_l25_orders - ask_l25_orders, bid_l25_orders + ask_l25_orders + 1.0),
        "microprice_l1_minus_mid_bps": safe_ratio(l1_micro - entry_mid, entry_mid) * 10_000.0,
        "microprice_l25_minus_mid_bps": safe_ratio(l25_micro - entry_mid, entry_mid) * 10_000.0,
        "spread_mean_lookback_bps": float(np.mean(spread_series)) if len(spread_series) else 0.0,
        "trade_qty_sum_lookback": float(np.sum(trade_qty)),
        "trade_qty_accel_lookback": float(np.sum(trade_qty[half:]) - np.sum(trade_qty[:half])),
        "minute_of_day": int((exchange_ts // 60_000) % (24 * 60)),
        "forward_return_bps": forward,
        "abs_forward_return_bps": abs(forward),
        "label_side": "long" if forward > 0 else ("short" if forward < 0 else "flat"),
        "move_candidate": int(abs(forward) >= min_abs_move_bps),
        "phase464_split": "train" if str(entry["trade_date"])[:7] in {"2026-01", "2026-02"} else ("holdout" if str(entry["trade_date"])[:7] == "2026-03" else "unused"),
    }
    rec.update(compute_source_event_features(past))
    return rec


def materialize_matrix(raw: pd.DataFrame, entry_index: int, horizon: int, min_abs_move_bps: float) -> pd.DataFrame:
    rows = []
    if raw.empty:
        return pd.DataFrame()
    raw = raw.sort_values(["trade_date", "symbol", "candidate_start_row", "window_local_row", "exchange_timestamp_ms"], kind="mergesort")
    for _, grp in raw.groupby(["trade_date", "symbol", "candidate_start_row"], sort=False):
        rec = compute_record(grp, entry_index, horizon, min_abs_move_bps)
        if rec is not None:
            rows.append(rec)
    return pd.DataFrame(rows)


def matrix_summary(matrix: pd.DataFrame, selected: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    if matrix.empty:
        values = {
            "selected_files": len(selected),
            "files_present": int(selected["exists"].sum()) if not selected.empty else 0,
            "matrix_rows": 0,
            "feature_count": len(features),
            "l2_l5_feature_count": int(features["uses_l2_l5_depth"].sum()) if not features.empty else 0,
            "move_candidate_rows": 0,
            "trade_dates": 0,
            "symbols": 0,
            "train_rows": 0,
            "holdout_rows": 0,
            "train_move_candidate_rows": 0,
            "holdout_move_candidate_rows": 0,
            "long_rows": 0,
            "short_rows": 0,
            "min_source_event_history_rows": 0,
            "median_source_event_history_rows": 0,
        }
    else:
        values = {
            "selected_files": len(selected),
            "files_present": int(selected["exists"].sum()) if not selected.empty else 0,
            "matrix_rows": len(matrix),
            "feature_count": len(features),
            "l2_l5_feature_count": int(features["uses_l2_l5_depth"].sum()),
            "move_candidate_rows": int(matrix["move_candidate"].sum()),
            "trade_dates": int(matrix["trade_date"].nunique()),
            "symbols": int(matrix["symbol"].nunique()),
            "train_rows": int(matrix["phase464_split"].eq("train").sum()),
            "holdout_rows": int(matrix["phase464_split"].eq("holdout").sum()),
            "train_move_candidate_rows": int(matrix.loc[matrix["phase464_split"].eq("train"), "move_candidate"].sum()),
            "holdout_move_candidate_rows": int(matrix.loc[matrix["phase464_split"].eq("holdout"), "move_candidate"].sum()),
            "long_rows": int(matrix["label_side"].eq("long").sum()),
            "short_rows": int(matrix["label_side"].eq("short").sum()),
            "min_source_event_history_rows": int(pd.to_numeric(matrix["source_event_distinct_history_rows"], errors="coerce").min()),
            "median_source_event_history_rows": float(pd.to_numeric(matrix["source_event_distinct_history_rows"], errors="coerce").median()),
        }
    return pd.DataFrame([{"metric": k, "value": v} for k, v in values.items()])


def feature_quality(matrix: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for feature in features["feature_name"].astype(str):
        if feature not in matrix.columns or matrix.empty:
            rows.append({"feature_name": feature, "present": int(feature in matrix.columns), "non_null_rows": 0, "unique_values": 0, "finite_rows": 0, "uses_l2_l5_depth": 0})
            continue
        series = pd.to_numeric(matrix[feature], errors="coerce")
        finite = np.isfinite(series.to_numpy(dtype=float))
        uses_l25 = int(features.loc[features["feature_name"].astype(str).eq(feature), "uses_l2_l5_depth"].astype(int).max())
        rows.append(
            {
                "feature_name": feature,
                "present": 1,
                "non_null_rows": int(series.notna().sum()),
                "unique_values": int(series.nunique(dropna=True)),
                "finite_rows": int(finite.sum()),
                "uses_l2_l5_depth": uses_l25,
            }
        )
    return pd.DataFrame(rows)


def build_gates(phase469: pd.DataFrame, summary: pd.DataFrame, quality: pd.DataFrame) -> pd.DataFrame:
    rows_count = as_int(sval(summary, "matrix_rows", 0))
    feature_count = as_int(sval(summary, "feature_count", 0))
    finite_ok = bool((quality["finite_rows"].astype(int) == rows_count).all()) if not quality.empty else False
    varying_features = int((quality["unique_values"].astype(int) > 1).sum()) if not quality.empty else 0
    varying_l25 = int(((quality["unique_values"].astype(int) > 1) & (quality["uses_l2_l5_depth"].astype(int) == 1)).sum()) if not quality.empty else 0
    gates = [
        ("P470_PHASE469_PRECOMMIT_USED", as_int(scalar(phase469, "phase469_phase470_allowed_next", 0)) == 1, scalar(phase469, "phase469_phase470_allowed_next", 0), 1),
        ("P470_MATRIX_ROWS_PRESENT", rows_count > 0, rows_count, ">0"),
        ("P470_FEATURE_COUNT_MATCHES_CONTRACT", feature_count == 25, feature_count, 25),
        ("P470_L2_L5_FEATURE_COUNT_MATCHES_CONTRACT", as_int(sval(summary, "l2_l5_feature_count", 0)) == 10, sval(summary, "l2_l5_feature_count", 0), 10),
        ("P470_ALL_FEATURES_FINITE", finite_ok, int(quality["finite_rows"].min()) if not quality.empty else 0, rows_count),
        ("P470_FEATURE_VARIATION_PRESENT", varying_features >= MIN_VARYING_FEATURES, varying_features, f">={MIN_VARYING_FEATURES}"),
        ("P470_L2_L5_FEATURE_VARIATION_PRESENT", varying_l25 >= 8, varying_l25, ">=8"),
        ("P470_MOVE_CANDIDATES_PRESENT", as_int(sval(summary, "move_candidate_rows", 0)) > 0, sval(summary, "move_candidate_rows", 0), ">0"),
        ("P470_TRAIN_AND_HOLDOUT_PRESENT", as_int(sval(summary, "train_rows", 0)) > 0 and as_int(sval(summary, "holdout_rows", 0)) > 0, f"train={sval(summary, 'train_rows', 0)};holdout={sval(summary, 'holdout_rows', 0)}", "both>0"),
        ("P470_BOTH_DIRECTIONS_PRESENT", as_int(sval(summary, "long_rows", 0)) > 0 and as_int(sval(summary, "short_rows", 0)) > 0, f"long={sval(summary, 'long_rows', 0)};short={sval(summary, 'short_rows', 0)}", "both>0"),
        ("P470_SOURCE_EVENT_HISTORY_PRESENT", as_int(sval(summary, "min_source_event_history_rows", 0)) >= 1, sval(summary, "min_source_event_history_rows", 0), ">=1"),
        ("P470_NO_MODEL_FIT", True, "matrix_only", "no_model_fit"),
        ("P470_NO_STRATEGY_PNL", True, "matrix_only", "no_pnl"),
        ("P470_NO_PAPER_LIVE_OR_CLAIM", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    all_pass = int(hard_pass == hard_rows)
    rows = [
        ("phase470_source_event_aware_l1_l5_feature_matrix_complete", 1, "Phase470 matrix materialization completed"),
        ("phase470_thesis_id", THESIS_ID, "Matrix thesis"),
        ("phase470_phase469_thesis_id", PHASE469_THESIS_ID, "Precommit source"),
        ("phase470_matrix_rows", sval(summary, "matrix_rows", 0), "Matrix rows"),
        ("phase470_feature_count", sval(summary, "feature_count", 0), "Feature count"),
        ("phase470_l2_l5_feature_count", sval(summary, "l2_l5_feature_count", 0), "L2-L5 feature count"),
        ("phase470_move_candidate_rows", sval(summary, "move_candidate_rows", 0), "Move candidates"),
        ("phase470_train_rows", sval(summary, "train_rows", 0), "Train rows"),
        ("phase470_holdout_rows", sval(summary, "holdout_rows", 0), "Holdout rows"),
        ("phase470_min_source_event_history_rows", sval(summary, "min_source_event_history_rows", 0), "Minimum distinct source-event history rows"),
        ("phase470_model_fit_generated", 0, "No model fit"),
        ("phase470_strategy_pnl_generated", 0, "No strategy P&L"),
        ("phase470_strategy_promotion_allowed", 0, "No promotion"),
        ("phase470_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase470_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase470_phase471_allowed_next", all_pass, "Allows model precommit only if all gates pass"),
        ("phase470_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase470_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase470_next_best_action", NEXT_ACTION_HAS_MATRIX if all_pass else NEXT_ACTION_NO_MATRIX, "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, summary: pd.DataFrame, quality: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase470 Source-Event-Aware L1-L5 Feature Matrix Materialization",
        "",
        "Phase470 materializes the Phase469 repaired feature contract using distinct `source_annual_event_id` history at or before entry.",
        "",
        "It does not fit a model and does not emit strategy P&L.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Matrix Summary",
        "",
        _markdown_table(summary),
        "",
        "## Feature Quality",
        "",
        _markdown_table(quality),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase470 is matrix materialization only. Phase471 must precommit model fitting before any training, and strategy replay remains closed.",
    ]
    (output_dir / "phase470_materialize_source_event_aware_l1_l5_feature_matrix_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase467_dir: Path = DEFAULT_PHASE467_DIR, phase469_dir: Path = DEFAULT_PHASE469_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase469 = read_csv(phase469_dir / "phase469_acceptance_summary.csv")
    contract = read_csv(phase467_dir / "phase467_frozen_phase468_contract.csv")
    selected = read_csv(phase467_dir / "phase467_selected_files.csv")
    features = read_csv(phase469_dir / "phase469_repaired_feature_contract.csv")
    if as_int(scalar(phase469, "phase469_phase470_allowed_next", 0)) != 1:
        raise ValueError("Phase470 requires Phase469 matrix materialization allowance.")
    entry_index = ival(contract, "entry_index", 20)
    horizon = ival(contract, "horizon_ticks", 240)
    min_abs_move = fval(contract, "min_abs_forward_move_bps", 2.0)
    rows_per_window = entry_index + horizon + 1
    raw_parts = [read_candidate_windows(Path(row["path"]), str(row["trade_month"]), STARTS, rows_per_window, PREHISTORY_ROWS) for row in selected.to_dict("records")]
    raw = pd.concat(raw_parts, ignore_index=True) if raw_parts else pd.DataFrame()
    matrix = materialize_matrix(raw, entry_index, horizon, min_abs_move)
    summary = matrix_summary(matrix, selected, features)
    quality = feature_quality(matrix, features)
    gates = build_gates(phase469, summary, quality)
    acceptance = build_acceptance(summary, gates)
    matrix.to_csv(output_dir / "phase470_source_event_aware_feature_label_matrix.csv", index=False)
    summary.to_csv(output_dir / "phase470_matrix_summary.csv", index=False)
    quality.to_csv(output_dir / "phase470_feature_quality.csv", index=False)
    gates.to_csv(output_dir / "phase470_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase470_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, summary, quality, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase470_materialize_source_event_aware_l1_l5_feature_matrix",
        **reproducibility_fields(
            artifact_id="phase470_materialize_source_event_aware_l1_l5_feature_matrix",
            generated_utc=generated_utc,
            inputs={
                "phase469_feature_contract": str(phase469_dir / "phase469_repaired_feature_contract.csv"),
                "phase467_selected_files": str(phase467_dir / "phase467_selected_files.csv"),
            },
            parameters={
                "thesis_id": THESIS_ID,
                "entry_index": entry_index,
                "horizon": horizon,
                "min_abs_move_bps": min_abs_move,
                "candidate_starts": STARTS,
                "prehistory_rows": PREHISTORY_ROWS,
                "source_event_lookbacks": SOURCE_EVENT_LOOKBACKS,
            },
            outputs={"acceptance_summary": str(output_dir / "phase470_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase470_matrix_materialization_no_model_no_pnl",
        ),
    }
    (output_dir / "phase470_materialize_source_event_aware_l1_l5_feature_matrix_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase470 source-event-aware L1-L5 matrix materialization.")
    parser.add_argument("--phase467-dir", type=Path, default=DEFAULT_PHASE467_DIR)
    parser.add_argument("--phase469-dir", type=Path, default=DEFAULT_PHASE469_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    out = run(args.phase467_dir, args.phase469_dir, args.output_dir)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
