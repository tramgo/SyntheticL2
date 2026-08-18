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
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE467_DIR = Path("outputs/phase467")
DEFAULT_OUTPUT_DIR = Path("outputs/phase468")

THESIS_ID = "P468_MATERIALIZE_RICHER_PAST_ONLY_L1_L5_FEATURE_MATRIX"
NEXT_ACTION_HAS_MATRIX = "precommit_phase469_train_holdout_richer_past_only_l1_l5_model_no_replay"
NEXT_ACTION_NO_MATRIX = "repair_phase468_richer_matrix_materialization_before_model_precommit"

BATCH_SIZE = 50_000
RAW_COLUMNS = [
    "exchange_timestamp_ms",
    "trade_date",
    "exchange",
    "symbol",
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


def slist(value: str) -> list[str]:
    return [x.strip() for x in str(value).split(";") if x.strip()]


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


def ilist(value: str) -> list[int]:
    return [int(float(x.strip())) for x in str(value).split(";") if x.strip()]


def read_candidate_windows(path: Path, month: str, starts: list[int], rows_per_window: int) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=RAW_COLUMNS + ["candidate_start_row", "window_local_row"])
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
            if seen >= max_end or seen + n <= min(starts):
                continue
            for start in starts:
                local_start = max(0, start - seen)
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


def slope(values: np.ndarray) -> float:
    if len(values) < 2:
        return 0.0
    x = np.arange(1, len(values) + 1, dtype=float)
    return float(np.polyfit(x, values.astype(float), 1)[0])


def safe_ratio(numerator: float, denominator: float) -> float:
    return float(numerator / denominator) if abs(denominator) > 1e-12 else 0.0


def compute_record(g: pd.DataFrame, entry_index: int, horizon: int, min_abs_move_bps: float) -> dict[str, Any] | None:
    if len(g) <= entry_index + horizon:
        return None
    g = g.sort_values(["window_local_row", "exchange_timestamp_ms"], kind="mergesort").reset_index(drop=True)
    entry = g.iloc[entry_index]
    exit_row = g.iloc[entry_index + horizon]
    past = g.iloc[: entry_index + 1].copy()
    lookback_start = past.iloc[0]
    bid_prices = np.array([float(entry[f"buy_{level}_price"]) for level in range(1, 6)], dtype=float)
    ask_prices = np.array([float(entry[f"sell_{level}_price"]) for level in range(1, 6)], dtype=float)
    bid_qty = np.array([float(entry[f"buy_{level}_quantity"]) for level in range(1, 6)], dtype=float)
    ask_qty = np.array([float(entry[f"sell_{level}_quantity"]) for level in range(1, 6)], dtype=float)
    bid_orders = np.array([float(entry[f"buy_{level}_orders"]) for level in range(1, 6)], dtype=float)
    ask_orders = np.array([float(entry[f"sell_{level}_orders"]) for level in range(1, 6)], dtype=float)
    entry_mid = (float(entry["buy_1_price"]) + float(entry["sell_1_price"])) / 2.0
    exit_mid = (float(exit_row["buy_1_price"]) + float(exit_row["sell_1_price"])) / 2.0
    prior_mid = (float(lookback_start["buy_1_price"]) + float(lookback_start["sell_1_price"])) / 2.0
    if entry_mid <= 0:
        return None
    spread = float(entry["sell_1_price"]) - float(entry["buy_1_price"])
    bid_l25 = float(bid_qty[1:].sum())
    ask_l25 = float(ask_qty[1:].sum())
    bid_l25_orders = float(bid_orders[1:].sum())
    ask_l25_orders = float(ask_orders[1:].sum())
    total_depth = float(bid_qty.sum() + ask_qty.sum())
    q_bid1 = past["buy_1_quantity"].astype(float).to_numpy()
    q_ask1 = past["sell_1_quantity"].astype(float).to_numpy()
    q_bid25 = past[[f"buy_{level}_quantity" for level in range(2, 6)]].astype(float).sum(axis=1).to_numpy()
    q_ask25 = past[[f"sell_{level}_quantity" for level in range(2, 6)]].astype(float).sum(axis=1).to_numpy()
    l25_total = q_bid25 + q_ask25
    l25_diff = np.diff(l25_total) if len(l25_total) > 1 else np.array([], dtype=float)
    spread_series = (
        past["sell_1_price"].astype(float).to_numpy()
        - past["buy_1_price"].astype(float).to_numpy()
    ) / np.maximum(1e-9, (past["sell_1_price"].astype(float).to_numpy() + past["buy_1_price"].astype(float).to_numpy()) / 2.0) * 10_000.0
    trade_qty = past["last_traded_quantity"].astype(float).to_numpy()
    half = max(1, len(trade_qty) // 2)
    l1_micro = safe_ratio(float(entry["sell_1_price"]) * float(entry["buy_1_quantity"]) + float(entry["buy_1_price"]) * float(entry["sell_1_quantity"]), float(entry["buy_1_quantity"]) + float(entry["sell_1_quantity"]))
    l25_micro = safe_ratio(float(np.dot(ask_prices[1:], bid_qty[1:]) + np.dot(bid_prices[1:], ask_qty[1:])), bid_l25 + ask_l25)
    forward = (exit_mid - entry_mid) / entry_mid * 10_000.0
    exchange_ts = int(entry["exchange_timestamp_ms"])
    return {
        "trade_date": str(entry["trade_date"]),
        "exchange": str(entry["exchange"]),
        "symbol": str(entry["symbol"]),
        "candidate_start_row": int(entry["candidate_start_row"]),
        "entry_row": int(entry_index),
        "exit_row": int(entry_index + horizon),
        "entry_timestamp_ms": exchange_ts,
        "entry_price": entry_mid,
        "exit_price": exit_mid,
        "recent_mid_return_bps": safe_ratio(entry_mid - prior_mid, prior_mid) * 10_000.0,
        "spread_bps": safe_ratio(spread, entry_mid) * 10_000.0,
        "l1_imbalance": safe_ratio(float(entry["buy_1_quantity"]) - float(entry["sell_1_quantity"]), float(entry["buy_1_quantity"]) + float(entry["sell_1_quantity"]) + 1.0),
        "l25_imbalance": safe_ratio(bid_l25 - ask_l25, bid_l25 + ask_l25 + 1.0),
        "volume_delta_lookback": float(entry["volume_traded"]) - float(lookback_start["volume_traded"]),
        "l1_l5_bid_depth_slope": slope(bid_qty),
        "l1_l5_ask_depth_slope": slope(ask_qty),
        "l1_l5_depth_concentration": safe_ratio(float(bid_qty[0] + ask_qty[0]), total_depth),
        "l25_order_imbalance": safe_ratio(bid_l25_orders - ask_l25_orders, bid_l25_orders + ask_l25_orders + 1.0),
        "ofi_l1_lookback": float((q_bid1[-1] - q_bid1[0]) - (q_ask1[-1] - q_ask1[0])),
        "ofi_l25_lookback": float((q_bid25[-1] - q_bid25[0]) - (q_ask25[-1] - q_ask25[0])),
        "l25_replenishment_events": int((l25_diff > 0).sum()),
        "l25_withdrawal_events": int((l25_diff < 0).sum()),
        "microprice_l1_minus_mid_bps": safe_ratio(l1_micro - entry_mid, entry_mid) * 10_000.0,
        "microprice_l25_minus_mid_bps": safe_ratio(l25_micro - entry_mid, entry_mid) * 10_000.0,
        "spread_change_lookback_bps": float(spread_series[-1] - spread_series[0]) if len(spread_series) else 0.0,
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
        }
    return pd.DataFrame([{"metric": k, "value": v} for k, v in values.items()])


def sval(summary: pd.DataFrame, key: str, default: Any = 0) -> Any:
    rows = summary.loc[summary["metric"].eq(key), "value"].tolist()
    return rows[0] if rows else default


def feature_quality(matrix: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for feature in features["feature_name"].astype(str):
        if feature not in matrix.columns or matrix.empty:
            rows.append({"feature_name": feature, "present": int(feature in matrix.columns), "non_null_rows": 0, "unique_values": 0, "finite_rows": 0})
            continue
        series = pd.to_numeric(matrix[feature], errors="coerce")
        finite = np.isfinite(series.to_numpy(dtype=float))
        rows.append(
            {
                "feature_name": feature,
                "present": 1,
                "non_null_rows": int(series.notna().sum()),
                "unique_values": int(series.nunique(dropna=True)),
                "finite_rows": int(finite.sum()),
            }
        )
    return pd.DataFrame(rows)


def build_gates(phase467: pd.DataFrame, summary: pd.DataFrame, quality: pd.DataFrame) -> pd.DataFrame:
    rows_count = as_int(sval(summary, "matrix_rows", 0))
    feature_count = as_int(sval(summary, "feature_count", 0))
    finite_ok = bool((quality["finite_rows"].astype(int) == rows_count).all()) if not quality.empty else False
    varying_features = int((quality["unique_values"].astype(int) > 1).sum()) if not quality.empty else 0
    gates = [
        ("P468_PHASE467_PRECOMMIT_USED", as_int(scalar(phase467, "phase467_phase468_allowed_next", 0)) == 1, scalar(phase467, "phase467_phase468_allowed_next", 0), 1),
        ("P468_MATRIX_ROWS_PRESENT", rows_count > 0, rows_count, ">0"),
        ("P468_FEATURE_COUNT_MATCHES_CONTRACT", feature_count == 20, feature_count, 20),
        ("P468_L2_L5_FEATURE_COUNT_MATCHES_CONTRACT", as_int(sval(summary, "l2_l5_feature_count", 0)) == 9, sval(summary, "l2_l5_feature_count", 0), 9),
        ("P468_ALL_FEATURES_FINITE", finite_ok, int(quality["finite_rows"].min()) if not quality.empty else 0, rows_count),
        ("P468_FEATURE_VARIATION_PRESENT", varying_features >= 15, varying_features, ">=15"),
        ("P468_MOVE_CANDIDATES_PRESENT", as_int(sval(summary, "move_candidate_rows", 0)) > 0, sval(summary, "move_candidate_rows", 0), ">0"),
        ("P468_TRAIN_AND_HOLDOUT_PRESENT", as_int(sval(summary, "train_rows", 0)) > 0 and as_int(sval(summary, "holdout_rows", 0)) > 0, f"train={sval(summary, 'train_rows', 0)};holdout={sval(summary, 'holdout_rows', 0)}", "both>0"),
        ("P468_BOTH_DIRECTIONS_PRESENT", as_int(sval(summary, "long_rows", 0)) > 0 and as_int(sval(summary, "short_rows", 0)) > 0, f"long={sval(summary, 'long_rows', 0)};short={sval(summary, 'short_rows', 0)}", "both>0"),
        ("P468_NO_MODEL_FIT", True, "matrix_only", "no_model_fit"),
        ("P468_NO_STRATEGY_PNL", True, "matrix_only", "no_pnl"),
        ("P468_NO_PAPER_LIVE_OR_CLAIM", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    all_pass = int(hard_pass == hard_rows)
    rows = [
        ("phase468_richer_past_only_l1_l5_feature_matrix_complete", 1, "Phase468 matrix materialization completed"),
        ("phase468_thesis_id", THESIS_ID, "Matrix thesis"),
        ("phase468_matrix_rows", sval(summary, "matrix_rows", 0), "Matrix rows"),
        ("phase468_feature_count", sval(summary, "feature_count", 0), "Feature count"),
        ("phase468_l2_l5_feature_count", sval(summary, "l2_l5_feature_count", 0), "L2-L5 feature count"),
        ("phase468_move_candidate_rows", sval(summary, "move_candidate_rows", 0), "Move candidates"),
        ("phase468_train_rows", sval(summary, "train_rows", 0), "Train rows"),
        ("phase468_holdout_rows", sval(summary, "holdout_rows", 0), "Holdout rows"),
        ("phase468_model_fit_generated", 0, "No model fit"),
        ("phase468_strategy_pnl_generated", 0, "No strategy P&L"),
        ("phase468_strategy_promotion_allowed", 0, "No promotion"),
        ("phase468_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase468_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase468_phase469_allowed_next", all_pass, "Allows model precommit only if all gates pass"),
        ("phase468_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase468_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase468_next_best_action", NEXT_ACTION_HAS_MATRIX if all_pass else NEXT_ACTION_NO_MATRIX, "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, summary: pd.DataFrame, quality: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase468 Richer Past-Only L1-L5 Feature Matrix Materialization",
        "",
        "Phase468 materializes the Phase467 richer past-only feature matrix. It does not fit a model and does not emit strategy P&L.",
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
        "Boundary: Phase468 is matrix materialization only. Phase469 must precommit model fitting before any training, and strategy replay remains closed.",
    ]
    (output_dir / "phase468_materialize_richer_past_only_l1_l5_feature_matrix_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase467_dir: Path = DEFAULT_PHASE467_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase467 = read_csv(phase467_dir / "phase467_acceptance_summary.csv")
    contract = read_csv(phase467_dir / "phase467_frozen_phase468_contract.csv")
    selected = read_csv(phase467_dir / "phase467_selected_files.csv")
    features = read_csv(phase467_dir / "phase467_feature_contract.csv")
    if as_int(scalar(phase467, "phase467_phase468_allowed_next", 0)) != 1:
        raise ValueError("Phase468 requires Phase467 matrix materialization allowance.")
    starts = ilist("0;5000;10000;20000;50000")
    entry_index = ival(contract, "entry_index", 20)
    horizon = ival(contract, "horizon_ticks", 240)
    min_abs_move = fval(contract, "min_abs_forward_move_bps", 2.0)
    rows_per_window = entry_index + horizon + 1
    raw_parts = [read_candidate_windows(Path(row["path"]), str(row["trade_month"]), starts, rows_per_window) for row in selected.to_dict("records")]
    raw = pd.concat(raw_parts, ignore_index=True) if raw_parts else pd.DataFrame()
    matrix = materialize_matrix(raw, entry_index, horizon, min_abs_move)
    summary = matrix_summary(matrix, selected, features)
    quality = feature_quality(matrix, features)
    gates = build_gates(phase467, summary, quality)
    acceptance = build_acceptance(summary, gates)
    matrix.to_csv(output_dir / "phase468_richer_feature_label_matrix.csv", index=False)
    summary.to_csv(output_dir / "phase468_matrix_summary.csv", index=False)
    quality.to_csv(output_dir / "phase468_feature_quality.csv", index=False)
    gates.to_csv(output_dir / "phase468_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase468_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, summary, quality, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase468_materialize_richer_past_only_l1_l5_feature_matrix",
        **reproducibility_fields(
            artifact_id="phase468_materialize_richer_past_only_l1_l5_feature_matrix",
            generated_utc=generated_utc,
            inputs={"phase467_contract": str(phase467_dir / "phase467_frozen_phase468_contract.csv")},
            parameters={"thesis_id": THESIS_ID, "entry_index": entry_index, "horizon": horizon, "min_abs_move_bps": min_abs_move},
            outputs={"acceptance_summary": str(output_dir / "phase468_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase468_matrix_materialization_no_model_no_pnl",
        ),
    }
    (output_dir / "phase468_materialize_richer_past_only_l1_l5_feature_matrix_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase468 richer past-only L1-L5 matrix materialization.")
    parser.add_argument("--phase467-dir", type=Path, default=DEFAULT_PHASE467_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    out = run(args.phase467_dir, args.output_dir)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
