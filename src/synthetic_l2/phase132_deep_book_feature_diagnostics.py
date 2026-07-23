from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase132")
DEFAULT_PHASE129_DIR = Path("outputs/phase129")
DEFAULT_PHASE130_DIR = Path("outputs/phase130")
DEFAULT_PHASE131_DIR = Path("outputs/phase131")
DEFAULT_PHASE116_DIR = Path("outputs/phase116")
DEFAULT_COMPACT_RAW_LAKE_DIR = Path("raw_synthetic_l2_full_year_compact_monthly")
LABELS = [
    "p129_regime_stability_label",
    "p129_liquidity_opportunity_label",
    "p129_cost_toxicity_refinement_label",
]
FORBIDDEN_OUTPUTS = "strategy_code;buy_sell_signal;order_arrival_stream;live_tagged_fill_model;pnl_replay;profitability_claim"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    value = rows.iloc[0]
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def clip_prob(value: float) -> float:
    return min(max(float(value), 1e-6), 1.0 - 1e-6)


def brier_score(y_true: list[int], y_prob: list[float]) -> float:
    if not y_true:
        return 0.0
    return float(sum((float(y) - float(p)) ** 2 for y, p in zip(y_true, y_prob)) / len(y_true))


def log_loss(y_true: list[int], y_prob: list[float]) -> float:
    if not y_true:
        return 0.0
    total = 0.0
    for y, p in zip(y_true, y_prob):
        pc = clip_prob(float(p))
        total += -(float(y) * math.log(pc) + (1.0 - float(y)) * math.log(1.0 - pc))
    return float(total / len(y_true))


def accuracy(y_true: list[int], y_prob: list[float], threshold: float = 0.5) -> float:
    if not y_true:
        return 0.0
    return float(sum(int((p >= threshold) == bool(y)) for y, p in zip(y_true, y_prob)) / len(y_true))


def auc_score(y_true: list[int], y_score: list[float]) -> float | None:
    positives = [score for y, score in zip(y_true, y_score) if int(y) == 1]
    negatives = [score for y, score in zip(y_true, y_score) if int(y) == 0]
    if not positives or not negatives:
        return None
    wins = 0.0
    total = len(positives) * len(negatives)
    for ps in positives:
        for ns in negatives:
            if ps > ns:
                wins += 1.0
            elif ps == ns:
                wins += 0.5
    return float(wins / total)


def parquet_files_for_months(raw_lake_dir: Path, months: set[str]) -> list[Path]:
    files: list[Path] = []
    for month in sorted(months):
        month_dir = raw_lake_dir / f"trade_month={month}"
        files.extend(sorted(month_dir.glob("*.parquet")))
    return files


def load_raw_depth_rows(raw_lake_dir: Path, allowed: pd.DataFrame) -> pd.DataFrame:
    months = set(allowed["trade_month"].astype(str).unique())
    symbols = set(allowed["symbol"].astype(str).unique())
    files = parquet_files_for_months(raw_lake_dir, months)
    if not files:
        return pd.DataFrame()
    columns = [
        "trade_date",
        "symbol",
        "feed_profile",
        "annual_event_id",
        "callback_received_utc_ms",
    ]
    for level in range(1, 6):
        columns.extend(
            [
                f"buy_{level}_price",
                f"buy_{level}_quantity",
                f"sell_{level}_price",
                f"sell_{level}_quantity",
            ]
        )
    tables = [pq.ParquetFile(path).read(columns=columns) for path in files]
    raw = pa.concat_tables(tables, promote_options="default").to_pandas()
    raw["trade_month"] = raw["trade_date"].astype(str).str.slice(0, 7)
    raw = raw[raw["symbol"].astype(str).isin(symbols) & raw["trade_month"].astype(str).isin(months)].copy()
    raw = raw.sort_values(["feed_profile", "trade_date", "symbol", "annual_event_id"], kind="mergesort").reset_index(drop=True)
    return raw


def row_depth_features(raw: pd.DataFrame) -> pd.DataFrame:
    frame = raw.copy()
    buy_qty = [f"buy_{level}_quantity" for level in range(1, 6)]
    sell_qty = [f"sell_{level}_quantity" for level in range(1, 6)]
    buy_price = [f"buy_{level}_price" for level in range(1, 6)]
    sell_price = [f"sell_{level}_price" for level in range(1, 6)]
    for column in buy_qty + sell_qty + buy_price + sell_price:
        frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0.0)

    bid_depth_2_5 = frame[[f"buy_{level}_quantity" for level in range(2, 6)]].sum(axis=1).replace(0.0, np.nan)
    ask_depth_2_5 = frame[[f"sell_{level}_quantity" for level in range(2, 6)]].sum(axis=1).replace(0.0, np.nan)
    frame["p131_depth_levels_2_5_ratio_bid"] = frame["buy_2_quantity"] / bid_depth_2_5
    frame["p131_depth_levels_2_5_ratio_ask"] = frame["sell_2_quantity"] / ask_depth_2_5

    bid_notional = sum(frame[f"buy_{level}_price"] * frame[f"buy_{level}_quantity"] for level in range(1, 6))
    ask_notional = sum(frame[f"sell_{level}_price"] * frame[f"sell_{level}_quantity"] for level in range(1, 6))
    frame["p131_cumulative_notional_imbalance_top5"] = (bid_notional - ask_notional) / (bid_notional + ask_notional).replace(0.0, np.nan)

    frame["sum_top5_depth"] = frame[buy_qty + sell_qty].sum(axis=1)
    group_cols = ["feed_profile", "trade_date", "symbol"]
    grouped = frame.groupby(group_cols, sort=False)
    rolling_median = grouped["sum_top5_depth"].transform(lambda values: values.rolling(5, min_periods=3).median())
    frame["p131_book_thinning_event_rate_1s"] = frame["sum_top5_depth"].lt(0.75 * rolling_median).fillna(False).astype(float)
    frame["p131_level_crossing_hazard_bid"] = frame["buy_1_price"].le(grouped["buy_2_price"].shift(1)).fillna(False).astype(float)
    frame["p131_level_crossing_hazard_ask"] = frame["sell_1_price"].ge(grouped["sell_2_price"].shift(1)).fillna(False).astype(float)

    levels = np.array([1, 2, 3, 4, 5], dtype=float)
    level_centered = levels - levels.mean()
    denom = float((level_centered**2).sum())
    bid_q = frame[buy_qty].to_numpy(dtype=float)
    ask_q = frame[sell_qty].to_numpy(dtype=float)
    frame["p131_depth_slope_top5_bid"] = (bid_q @ level_centered) / denom / np.maximum(bid_q.mean(axis=1), 1.0)
    frame["p131_depth_slope_top5_ask"] = (ask_q @ level_centered) / denom / np.maximum(ask_q.mean(axis=1), 1.0)

    cancel_parts = []
    for level in range(2, 6):
        for side in ["buy", "sell"]:
            price_col = f"{side}_{level}_price"
            qty_col = f"{side}_{level}_quantity"
            prev_price = grouped[price_col].shift(1)
            prev_qty = grouped[qty_col].shift(1)
            cancel_parts.append((prev_price.eq(frame[price_col]) & prev_qty.gt(frame[qty_col])).astype(float) * (prev_qty - frame[qty_col]).clip(lower=0.0))
    frame["p131_mean_cancel_intensity_depth_levels_2_5"] = sum(cancel_parts) / 8.0
    frame["p131_deep_book_pressure_signed"] = (
        frame["p131_cumulative_notional_imbalance_top5"]
        + 0.25 * frame["p131_depth_slope_top5_bid"]
        - 0.25 * frame["p131_depth_slope_top5_ask"]
    )
    return frame


PHASE131_FEATURES = [
    "p131_depth_levels_2_5_ratio_bid",
    "p131_depth_levels_2_5_ratio_ask",
    "p131_cumulative_notional_imbalance_top5",
    "p131_book_thinning_event_rate_1s",
    "p131_level_crossing_hazard_bid",
    "p131_level_crossing_hazard_ask",
    "p131_depth_slope_top5_bid",
    "p131_depth_slope_top5_ask",
    "p131_mean_cancel_intensity_depth_levels_2_5",
    "p131_deep_book_pressure_signed",
]


def aggregate_feature_matrix(raw_features: pd.DataFrame, phase130_matrix: pd.DataFrame) -> pd.DataFrame:
    if raw_features.empty:
        return pd.DataFrame()
    agg_spec: dict[str, tuple[str, str]] = {}
    for feature in PHASE131_FEATURES:
        agg_spec[feature] = (feature, "mean")
    agg_spec["raw_rows"] = ("symbol", "count")
    agg_spec["trade_dates"] = ("trade_date", "nunique")
    agg_spec["feed_profiles"] = ("feed_profile", "nunique")
    grouped = raw_features.groupby(["trade_month", "symbol"], sort=True).agg(**agg_spec).reset_index()
    grouped[PHASE131_FEATURES] = grouped[PHASE131_FEATURES].replace([np.inf, -np.inf], np.nan).fillna(0.0)
    matrix = phase130_matrix.merge(grouped, on=["trade_month", "symbol"], how="left", validate="one_to_one")
    matrix[PHASE131_FEATURES] = matrix[PHASE131_FEATURES].fillna(0.0)
    matrix["raw_rows"] = pd.to_numeric(matrix["raw_rows"], errors="coerce").fillna(0).astype(int)
    matrix["trade_dates"] = pd.to_numeric(matrix["trade_dates"], errors="coerce").fillna(0).astype(int)
    matrix["feed_profiles"] = pd.to_numeric(matrix["feed_profiles"], errors="coerce").fillna(0).astype(int)
    matrix["phase132_scope"] = "top_five_depth_label_diagnostics_only"
    matrix["strategy_replay_allowed"] = 0
    matrix["forbidden_outputs"] = FORBIDDEN_OUTPUTS
    return matrix


def threshold_candidates(series: pd.Series) -> list[float]:
    values = pd.to_numeric(series, errors="coerce").dropna()
    if values.empty:
        return []
    return sorted({float(values.quantile(q)) for q in [0.25, 0.50, 0.75]})


def evaluate_predictions(label: str, model_id: str, train_y: list[int], holdout_y: list[int], holdout_prob: list[float], details: dict[str, Any]) -> dict[str, Any]:
    return {
        "label": label,
        "model_id": model_id,
        "train_rows": int(len(train_y)),
        "holdout_rows": int(len(holdout_y)),
        "train_positive_rate": float(sum(train_y) / len(train_y)) if train_y else 0.0,
        "holdout_positive_rate": float(sum(holdout_y) / len(holdout_y)) if holdout_y else 0.0,
        "holdout_brier": brier_score(holdout_y, holdout_prob),
        "holdout_log_loss": log_loss(holdout_y, holdout_prob),
        "holdout_accuracy": accuracy(holdout_y, holdout_prob),
        "holdout_auc": auc_score(holdout_y, holdout_prob),
        "strategy_replay_allowed": 0,
        "forbidden_outputs": FORBIDDEN_OUTPUTS,
        **details,
    }


def prior_model(label: str, train: pd.DataFrame, holdout: pd.DataFrame) -> dict[str, Any]:
    train_y = train[label].astype(int).tolist()
    holdout_y = holdout[label].astype(int).tolist()
    prior = clip_prob(sum(train_y) / len(train_y)) if train_y else 0.5
    return evaluate_predictions(
        label,
        "phase132_train_prior_probability",
        train_y,
        holdout_y,
        [prior for _ in holdout_y],
        {"model_family": "prior", "feature_1": "", "direction_1": "", "threshold_1": "", "feature_2": "", "direction_2": "", "threshold_2": ""},
    )


def threshold_signal(values: pd.Series, direction: str, threshold: float) -> pd.Series:
    numeric = pd.to_numeric(values, errors="coerce").fillna(0.0)
    if direction == "ge":
        return numeric.ge(threshold)
    return numeric.le(threshold)


def single_feature_model(label: str, feature: str, train: pd.DataFrame, holdout: pd.DataFrame, direction: str, threshold: float) -> dict[str, Any]:
    train_pred = threshold_signal(train[feature], direction, threshold)
    holdout_pred = threshold_signal(holdout[feature], direction, threshold)
    holdout_prob = [0.80 if bool(value) else 0.20 for value in holdout_pred.tolist()]
    return evaluate_predictions(
        label,
        f"p132_single_{feature}_{direction}_{threshold:.8g}",
        train[label].astype(int).tolist(),
        holdout[label].astype(int).tolist(),
        holdout_prob,
        {
            "model_family": "single_feature_threshold",
            "feature_1": feature,
            "direction_1": direction,
            "threshold_1": threshold,
            "feature_2": "",
            "direction_2": "",
            "threshold_2": "",
            "train_prediction_rate": float(train_pred.mean()) if len(train_pred) else 0.0,
        },
    )


def combo_model(
    label: str,
    feature_1: str,
    feature_2: str,
    train: pd.DataFrame,
    holdout: pd.DataFrame,
    direction_1: str,
    direction_2: str,
    threshold_1: float,
    threshold_2: float,
) -> dict[str, Any]:
    train_pred = threshold_signal(train[feature_1], direction_1, threshold_1) & threshold_signal(train[feature_2], direction_2, threshold_2)
    holdout_pred = threshold_signal(holdout[feature_1], direction_1, threshold_1) & threshold_signal(holdout[feature_2], direction_2, threshold_2)
    holdout_prob = [0.80 if bool(value) else 0.20 for value in holdout_pred.tolist()]
    return evaluate_predictions(
        label,
        f"p132_combo_{feature_1}_{direction_1}_{threshold_1:.8g}__{feature_2}_{direction_2}_{threshold_2:.8g}",
        train[label].astype(int).tolist(),
        holdout[label].astype(int).tolist(),
        holdout_prob,
        {
            "model_family": "two_feature_threshold_combo",
            "feature_1": feature_1,
            "direction_1": direction_1,
            "threshold_1": threshold_1,
            "feature_2": feature_2,
            "direction_2": direction_2,
            "threshold_2": threshold_2,
            "train_prediction_rate": float(train_pred.mean()) if len(train_pred) else 0.0,
        },
    )


def evaluate_feature_diagnostics(matrix: pd.DataFrame) -> pd.DataFrame:
    train = matrix[matrix["phase130_split"].eq("train")].copy()
    holdout = matrix[matrix["phase130_split"].eq("holdout")].copy()
    rows: list[dict[str, Any]] = []
    medians = {feature: float(pd.to_numeric(train[feature], errors="coerce").median()) for feature in PHASE131_FEATURES}
    for label in LABELS:
        if train[label].nunique() < 2 or holdout[label].nunique() < 2:
            rows.append(
                {
                    "label": label,
                    "model_id": "not_fit_no_class_variation",
                    "model_family": "not_fit",
                    "train_rows": int(len(train)),
                    "holdout_rows": int(len(holdout)),
                    "holdout_brier": None,
                    "holdout_log_loss": None,
                    "holdout_accuracy": None,
                    "holdout_auc": None,
                    "strategy_replay_allowed": 0,
                    "forbidden_outputs": FORBIDDEN_OUTPUTS,
                }
            )
            continue
        rows.append(prior_model(label, train, holdout))
        for feature in PHASE131_FEATURES:
            for threshold in threshold_candidates(train[feature]):
                for direction in ["ge", "le"]:
                    rows.append(single_feature_model(label, feature, train, holdout, direction, threshold))
        for feature_1, feature_2 in combinations(PHASE131_FEATURES, 2):
            for direction_1 in ["ge", "le"]:
                for direction_2 in ["ge", "le"]:
                    rows.append(combo_model(label, feature_1, feature_2, train, holdout, direction_1, direction_2, medians[feature_1], medians[feature_2]))
    results = pd.DataFrame(rows)
    if not results.empty:
        results["holdout_brier"] = pd.to_numeric(results["holdout_brier"], errors="coerce")
        results["holdout_log_loss"] = pd.to_numeric(results["holdout_log_loss"], errors="coerce")
        results = results.sort_values(["label", "holdout_brier", "holdout_log_loss"], ascending=[True, True, True], kind="mergesort")
    return results


def build_model_selection(results: pd.DataFrame, baseline_reference: pd.DataFrame, margin: float) -> pd.DataFrame:
    rows = []
    for label in LABELS:
        group = results[results["label"].eq(label)].copy() if not results.empty else pd.DataFrame()
        ref = baseline_reference[baseline_reference["label"].eq(label)].copy() if not baseline_reference.empty else pd.DataFrame()
        phase130_brier = float(ref["best_brier"].iloc[0]) if not ref.empty else math.nan
        if group.empty or group["holdout_brier"].dropna().empty:
            rows.append(
                {
                    "label": label,
                    "phase132_selected_model_id": "",
                    "phase132_model_family": "",
                    "phase130_reference_brier": phase130_brier,
                    "phase132_best_brier": None,
                    "brier_lift_vs_phase130": None,
                    "brier_margin_required": margin,
                    "clears_phase132_lift_gate": 0,
                    "holdout_auc": None,
                    "feature_1": "",
                    "feature_2": "",
                    "strategy_replay_allowed": 0,
                }
            )
            continue
        best = group.dropna(subset=["holdout_brier"]).iloc[0]
        best_brier = float(best["holdout_brier"])
        lift = phase130_brier - best_brier if not math.isnan(phase130_brier) else math.nan
        clears = int(not math.isnan(lift) and lift > margin and str(best["model_family"]) != "prior")
        rows.append(
            {
                "label": label,
                "phase132_selected_model_id": str(best["model_id"]),
                "phase132_model_family": str(best["model_family"]),
                "phase130_reference_brier": phase130_brier,
                "phase132_best_brier": best_brier,
                "brier_lift_vs_phase130": lift,
                "brier_margin_required": margin,
                "clears_phase132_lift_gate": clears,
                "holdout_log_loss": best.get("holdout_log_loss"),
                "holdout_accuracy": best.get("holdout_accuracy"),
                "holdout_auc": best.get("holdout_auc"),
                "feature_1": best.get("feature_1", ""),
                "feature_2": best.get("feature_2", ""),
                "strategy_replay_allowed": 0,
            }
        )
    return pd.DataFrame(rows)


def build_surviving_features(selection: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in selection[selection["clears_phase132_lift_gate"].astype(int).eq(1)].iterrows():
        for feature_col in ["feature_1", "feature_2"]:
            feature = str(row.get(feature_col, "") or "")
            if feature and feature in PHASE131_FEATURES:
                rows.append(
                    {
                        "feature_id": feature,
                        "label": row["label"],
                        "selected_model_id": row["phase132_selected_model_id"],
                        "brier_lift_vs_phase130": row["brier_lift_vs_phase130"],
                        "holdout_auc": row.get("holdout_auc"),
                        "promoted_to_phase133": 1,
                        "strategy_replay_allowed": 0,
                    }
                )
    if not rows:
        return pd.DataFrame(columns=["feature_id", "label", "selected_model_id", "brier_lift_vs_phase130", "holdout_auc", "promoted_to_phase133", "strategy_replay_allowed"])
    return pd.DataFrame(rows).drop_duplicates(["feature_id", "label", "selected_model_id"]).sort_values(["label", "feature_id"], kind="mergesort")


def build_kill_switch(selection: pd.DataFrame, surviving: pd.DataFrame) -> pd.DataFrame:
    kill = int(surviving.empty)
    return pd.DataFrame(
        [
            {
                "branch_id": "PHASE132_TOP_FIVE_DEPTH_LABEL_LIFT",
                "kill_switch_fired": kill,
                "surviving_feature_rows": int(len(surviving)),
                "labels_cleared": int(selection["clears_phase132_lift_gate"].astype(int).sum()) if not selection.empty else 0,
                "blocklist_entry_required": "DEEP_BOOK_LABEL_LIFT = falsified" if kill else "",
                "next_phase_allowed": "phase133" if not kill else "none_skip_phase133_136",
                "strategy_replay_allowed": 0,
                "why": "no top-five-depth feature beat Phase130 baseline by the precommitted Brier margin" if kill else "at least one top-five-depth feature beat Phase130 baseline by the precommitted Brier margin",
            }
        ]
    )


def update_phase116_blocklist_if_needed(phase116_dir: Path, output_dir: Path, kill_switch: pd.DataFrame) -> pd.DataFrame:
    kill = int(kill_switch["kill_switch_fired"].iloc[0]) if not kill_switch.empty else 1
    blocklist_path = phase116_dir / "strategy_replay_blocklist.csv"
    existing = read_csv(blocklist_path)
    entry = {
        "blocked_family_id": "DEEP_BOOK_LABEL_LIFT",
        "blocked_strategy_ids": "phase131_phase132_top_five_depth_feature_diagnostics",
        "block_reason": "Phase132 top-five-depth feature diagnostics found zero labels where Phase131 features beat the Phase130 top-of-book/context baseline by the precommitted Brier margin.",
        "same_shard_continuation_allowed": False,
        "unlock_condition": "real Zerodha L2 anchor data through Phase113-115, or an externally precommitted research plan outside the synthetic-only top-five-depth passive branch",
    }
    before_rows = int(len(existing))
    already_present = bool(not existing.empty and existing["blocked_family_id"].astype(str).eq(entry["blocked_family_id"]).any())
    updated = existing.copy()
    update_applied = 0
    if kill and not already_present:
        updated = pd.concat([updated, pd.DataFrame([entry])], ignore_index=True)
        phase116_dir.mkdir(parents=True, exist_ok=True)
        updated.to_csv(blocklist_path, index=False)
        update_applied = 1
    elif kill and already_present:
        update_applied = 1
    after_rows = int(len(updated))
    verification = pd.DataFrame(
        [
            {
                "verification_id": "P132_PHASE116_BLOCKLIST_UPDATE",
                "kill_switch_fired": kill,
                "phase116_blocklist_path": str(blocklist_path),
                "before_rows": before_rows,
                "after_rows": after_rows,
                "blocklist_entry_present": int(kill and (already_present or update_applied == 1)),
                "blocklist_entry_added_this_run": int(kill and not already_present and update_applied == 1),
                "blocked_family_id": entry["blocked_family_id"] if kill else "",
                "strategy_replay_allowed": 0,
            }
        ]
    )
    verification.to_csv(output_dir / "phase116_blocklist_update_verification.csv", index=False)
    return verification


def build_guardrails() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"guardrail_id": "P132_PHASE131_FEATURES_ONLY", "requirement": "Only Phase131 precommitted top-five-depth features may be evaluated.", "enforcement": "Feature list is fixed in source from phase131_feature_catalog.csv."},
            {"guardrail_id": "P132_PHASE130_SPLIT_REUSED", "requirement": "Use the Phase130 chronological train/holdout split.", "enforcement": "phase130_split is carried from outputs/phase130/phase130_split_label_matrix.csv."},
            {"guardrail_id": "P132_SIMPLE_MODELS_ONLY", "requirement": "Fit only single-feature thresholds and simple two-feature threshold combinations.", "enforcement": "No model family outside prior/single_feature_threshold/two_feature_threshold_combo is emitted."},
            {"guardrail_id": "P132_KILL_SWITCH", "requirement": "Close branch if no feature beats Phase130 baseline by the Phase131 Brier margin.", "enforcement": "kill_switch_summary.csv records the branch outcome."},
            {"guardrail_id": "P132_NO_REPLAY", "requirement": "No strategy code, order simulation, P&L replay or profitability claim.", "enforcement": f"forbidden_outputs={FORBIDDEN_OUTPUTS}; strategy_replay_allowed=0."},
        ]
    )


def build_gate_evaluation(matrix: pd.DataFrame, results: pd.DataFrame, selection: pd.DataFrame, kill_switch: pd.DataFrame, blocklist_verification: pd.DataFrame) -> pd.DataFrame:
    model_families = set(results["model_family"].dropna().astype(str).unique()) if not results.empty and "model_family" in results.columns else set()
    allowed_families = {"prior", "single_feature_threshold", "two_feature_threshold_combo"}
    return pd.DataFrame(
        [
            {"gate_id": "P132_FEATURE_MATRIX_EXISTS", "gate_pass": int(not matrix.empty and len(matrix) == 228), "evidence": f"feature_matrix_rows={len(matrix)}"},
            {"gate_id": "P132_RAW_DEPTH_COVERAGE", "gate_pass": int(not matrix.empty and matrix["raw_rows"].gt(0).all()), "evidence": f"contexts_with_raw_rows={int(matrix['raw_rows'].gt(0).sum()) if not matrix.empty else 0}"},
            {"gate_id": "P132_PHASE130_SPLIT_PRESENT", "gate_pass": int(not matrix.empty and set(matrix["phase130_split"].astype(str).unique()) == {"train", "holdout"}), "evidence": f"splits={';'.join(sorted(matrix['phase130_split'].astype(str).unique())) if not matrix.empty else ''}"},
            {"gate_id": "P132_RESULTS_EXIST", "gate_pass": int(not results.empty), "evidence": f"diagnostic_result_rows={len(results)}"},
            {"gate_id": "P132_MODEL_FAMILIES_ALLOWED", "gate_pass": int(bool(model_families) and model_families.issubset(allowed_families)), "evidence": f"model_families={';'.join(sorted(model_families))}"},
            {"gate_id": "P132_SELECTION_ROWS_EXIST", "gate_pass": int(len(selection) == len(LABELS)), "evidence": f"selection_rows={len(selection)}"},
            {"gate_id": "P132_BRANCH_OUTCOME_DECLARED", "gate_pass": int(not kill_switch.empty), "evidence": f"kill_switch_fired={int(kill_switch['kill_switch_fired'].iloc[0]) if not kill_switch.empty else 'unknown'}"},
            {
                "gate_id": "P132_PHASE116_BLOCKLIST_UPDATED_IF_KILLED",
                "gate_pass": int(
                    not blocklist_verification.empty
                    and (
                        int(blocklist_verification["kill_switch_fired"].iloc[0]) == 0
                        or int(blocklist_verification["blocklist_entry_present"].iloc[0]) == 1
                    )
                ),
                "evidence": f"blocklist_entry_present={int(blocklist_verification['blocklist_entry_present'].iloc[0]) if not blocklist_verification.empty else 'unknown'}",
            },
            {"gate_id": "P132_NO_REPLAY", "gate_pass": int(not matrix.empty and matrix["strategy_replay_allowed"].sum() == 0 and (results.empty or results["strategy_replay_allowed"].sum() == 0)), "evidence": "strategy_replay_allowed remains 0"},
        ]
    )


def build_acceptance_summary(matrix: pd.DataFrame, results: pd.DataFrame, selection: pd.DataFrame, surviving: pd.DataFrame, kill_switch: pd.DataFrame, blocklist_verification: pd.DataFrame, gates: pd.DataFrame, margin: float) -> pd.DataFrame:
    kill = int(kill_switch["kill_switch_fired"].iloc[0]) if not kill_switch.empty else 1
    blocklist_present = int(blocklist_verification["blocklist_entry_present"].iloc[0]) if not blocklist_verification.empty else 0
    return pd.DataFrame(
        [
            ("phase132_feature_matrix_rows", int(len(matrix)), "Allowed Phase129 contexts with top-five-depth feature aggregates"),
            ("phase132_diagnostic_result_rows", int(len(results)), "Prior/single-feature/two-feature diagnostic evaluations"),
            ("phase132_selection_rows", int(len(selection)), "Label-level model selection rows"),
            ("phase132_surviving_feature_rows", int(len(surviving)), "Feature/label rows promoted to Phase133 if kill-switch is false"),
            ("phase132_labels_cleared_brier_lift", int(selection["clears_phase132_lift_gate"].astype(int).sum()) if not selection.empty else 0, "Labels where Phase131 feature diagnostics beat Phase130 baseline by margin"),
            ("phase132_brier_lift_margin", margin, "Precommitted Brier lift margin from Phase131"),
            ("phase132_kill_switch_fired", kill, "1 means close branch at Phase132 and skip Phase133-136"),
            ("phase132_phase116_blocklist_entry_present", blocklist_present, "1 means Phase116 blocklist contains the Phase132 deep-book label-lift falsification row"),
            ("phase132_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase132_all_gates_pass", int(gates["gate_pass"].astype(bool).all()) if not gates.empty else 0, "1 means Phase132 diagnostics are self-consistent"),
            ("phase132_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase132_next_best_action", "stop_update_phase116_blocklist" if kill else "run_phase133_passive_execution_model_upgrade", "Recommended next milestone"),
            ("phase132_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned cost model retained for audit continuity"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase132 Top-Five-Depth Feature Diagnostics",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase132 evaluates Phase131 precommitted Zerodha Level-2/top-five market-by-price depth features as label diagnostics only.",
        "It reuses the Phase130 chronological split and applies the Phase131 kill-switch. It does not emit strategy code, order simulation, P&L replay or profitability claims.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase132_deep_book_feature_diagnostics_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase132(base_dir: Path, output_dir: Path, phase129_dir: Path, phase130_dir: Path, phase131_dir: Path, phase116_dir: Path, raw_lake_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase130_matrix = read_csv(base_dir / phase130_dir / "phase130_split_label_matrix.csv")
    baseline_reference = read_csv(base_dir / phase131_dir / "phase131_phase130_baseline_reference.csv")
    phase131_acceptance = read_csv(base_dir / phase131_dir / "phase131_deep_book_feature_precommit_acceptance_summary.csv")
    margin = float(metric_value(phase131_acceptance, "phase131_brier_lift_margin", 0.005))
    allowed = read_csv(base_dir / phase129_dir / "allowed_context_label_matrix.csv")[["trade_month", "symbol"]].drop_duplicates()
    raw = load_raw_depth_rows(base_dir / raw_lake_dir, allowed)
    raw_features = row_depth_features(raw)
    matrix = aggregate_feature_matrix(raw_features, phase130_matrix)
    results = evaluate_feature_diagnostics(matrix)
    selection = build_model_selection(results, baseline_reference, margin)
    surviving = build_surviving_features(selection)
    kill_switch = build_kill_switch(selection, surviving)
    blocklist_verification = update_phase116_blocklist_if_needed(base_dir / phase116_dir, output_dir, kill_switch)
    guardrails = build_guardrails()
    gates = build_gate_evaluation(matrix, results, selection, kill_switch, blocklist_verification)
    acceptance = build_acceptance_summary(matrix, results, selection, surviving, kill_switch, blocklist_verification, gates, margin)

    matrix.to_csv(output_dir / "top_five_depth_feature_matrix.csv", index=False)
    results.to_csv(output_dir / "feature_diagnostic_results.csv", index=False)
    selection.to_csv(output_dir / "feature_model_selection.csv", index=False)
    surviving.to_csv(output_dir / "surviving_features.csv", index=False)
    kill_switch.to_csv(output_dir / "kill_switch_summary.csv", index=False)
    guardrails.to_csv(output_dir / "phase132_guardrails.csv", index=False)
    gates.to_csv(output_dir / "phase132_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase132_deep_book_feature_diagnostics_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Kill Switch Summary": kill_switch,
            "Feature Model Selection": selection,
            "Surviving Features": surviving,
            "Phase116 Blocklist Verification": blocklist_verification,
            "Feature Matrix Sample": matrix.head(50),
            "Best Diagnostic Results": results.groupby("label", sort=True).head(8) if not results.empty else results,
            "Guardrails": guardrails,
            "Gate Evaluation": gates,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase132_top_five_depth_feature_diagnostics",
        "strategy_replay_allowed": 0,
        "kill_switch_fired": int(kill_switch["kill_switch_fired"].iloc[0]) if not kill_switch.empty else 1,
        "forbidden_outputs": FORBIDDEN_OUTPUTS,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase132",
            generated_utc=generated_utc,
            inputs={
                "phase129_label_matrix": str(phase129_dir / "allowed_context_label_matrix.csv"),
                "phase130_split_matrix": str(phase130_dir / "phase130_split_label_matrix.csv"),
                "phase131_feature_catalog": str(phase131_dir / "phase131_feature_catalog.csv"),
                "phase131_baseline_reference": str(phase131_dir / "phase131_phase130_baseline_reference.csv"),
                "phase116_strategy_replay_blocklist": str(phase116_dir / "strategy_replay_blocklist.csv"),
                "compact_raw_lake": str(raw_lake_dir),
            },
            parameters={
                "feature_scope": "zerodha_level2_top_five_market_by_price_depth",
                "split_policy": "reuse_phase130_chronological_split",
                "model_family": "prior_single_feature_threshold_two_feature_threshold_combo",
                "kill_switch": f"requires_brier_lift_greater_than_{margin}_vs_phase130_baseline",
                "replay_policy": "closed",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "feature_matrix": str(output_dir / "top_five_depth_feature_matrix.csv"),
                "diagnostic_results": str(output_dir / "feature_diagnostic_results.csv"),
                "model_selection": str(output_dir / "feature_model_selection.csv"),
                "surviving_features": str(output_dir / "surviving_features.csv"),
                "kill_switch": str(output_dir / "kill_switch_summary.csv"),
                "phase116_blocklist_verification": str(output_dir / "phase116_blocklist_update_verification.csv"),
                "guardrails": str(output_dir / "phase132_guardrails.csv"),
                "gates": str(output_dir / "phase132_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase132_deep_book_feature_diagnostics_acceptance_summary.csv"),
                "report": str(output_dir / "phase132_deep_book_feature_diagnostics_report.md"),
                "manifest": str(output_dir / "phase132_deep_book_feature_diagnostics_manifest.json"),
            },
            random_seed="none_deterministic_threshold_diagnostics",
            scenario_ids="phase132_top_five_depth_label_diagnostics",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_label_diagnostics",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase132_deep_book_feature_diagnostics_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase132 top-five-depth feature diagnostics.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--phase129-dir", type=Path, default=DEFAULT_PHASE129_DIR)
    parser.add_argument("--phase130-dir", type=Path, default=DEFAULT_PHASE130_DIR)
    parser.add_argument("--phase131-dir", type=Path, default=DEFAULT_PHASE131_DIR)
    parser.add_argument("--phase116-dir", type=Path, default=DEFAULT_PHASE116_DIR)
    parser.add_argument("--raw-lake-dir", type=Path, default=DEFAULT_COMPACT_RAW_LAKE_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase132(
        base_dir=args.base_dir,
        output_dir=args.output_dir,
        phase129_dir=args.phase129_dir,
        phase130_dir=args.phase130_dir,
        phase131_dir=args.phase131_dir,
        phase116_dir=args.phase116_dir,
        raw_lake_dir=args.raw_lake_dir,
    )


if __name__ == "__main__":
    main()
