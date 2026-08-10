from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE307_DIR = Path("outputs/phase307")
DEFAULT_PHASE309_DIR = Path("outputs/phase309")
DEFAULT_OUTPUT_DIR = Path("outputs/phase310")

NEXT_ACTION = "run_phase311_event_catalyst_strategy_search_precommit_no_execution"
REPAIR_ACTION = "repair_phase310_event_catalyst_feature_materialization"


def safe_div(num: pd.Series, den: pd.Series) -> pd.Series:
    return num / den.where(den.abs() > 1e-12)


def enrich_ticks(joined: pd.DataFrame) -> pd.DataFrame:
    frame = joined.copy()
    buy_qty_cols = [f"buy_{level}_quantity" for level in range(1, 6)]
    sell_qty_cols = [f"sell_{level}_quantity" for level in range(1, 6)]
    buy_order_cols = [f"buy_{level}_orders" for level in range(1, 6)]
    sell_order_cols = [f"sell_{level}_orders" for level in range(1, 6)]
    buy_l2_l5_qty_cols = [f"buy_{level}_quantity" for level in range(2, 6)]
    sell_l2_l5_qty_cols = [f"sell_{level}_quantity" for level in range(2, 6)]
    buy_l2_l5_order_cols = [f"buy_{level}_orders" for level in range(2, 6)]
    sell_l2_l5_order_cols = [f"sell_{level}_orders" for level in range(2, 6)]

    frame["l1_spread"] = frame["sell_1_price"] - frame["buy_1_price"]
    frame["l1_mid"] = (frame["sell_1_price"] + frame["buy_1_price"]) / 2.0
    frame["l1_microprice"] = safe_div(
        frame["sell_1_price"] * frame["buy_1_quantity"] + frame["buy_1_price"] * frame["sell_1_quantity"],
        frame["buy_1_quantity"] + frame["sell_1_quantity"],
    )
    frame["l1_queue_imbalance"] = safe_div(
        frame["buy_1_quantity"] - frame["sell_1_quantity"],
        frame["buy_1_quantity"] + frame["sell_1_quantity"],
    )
    frame["l1_l5_buy_qty"] = frame[buy_qty_cols].sum(axis=1)
    frame["l1_l5_sell_qty"] = frame[sell_qty_cols].sum(axis=1)
    frame["l2_l5_buy_qty"] = frame[buy_l2_l5_qty_cols].sum(axis=1)
    frame["l2_l5_sell_qty"] = frame[sell_l2_l5_qty_cols].sum(axis=1)
    frame["l1_l5_buy_orders"] = frame[buy_order_cols].sum(axis=1)
    frame["l1_l5_sell_orders"] = frame[sell_order_cols].sum(axis=1)
    frame["l2_l5_buy_orders"] = frame[buy_l2_l5_order_cols].sum(axis=1)
    frame["l2_l5_sell_orders"] = frame[sell_l2_l5_order_cols].sum(axis=1)
    frame["l1_l5_qty_imbalance"] = safe_div(frame["l1_l5_buy_qty"] - frame["l1_l5_sell_qty"], frame["l1_l5_buy_qty"] + frame["l1_l5_sell_qty"])
    frame["l2_l5_qty_imbalance"] = safe_div(frame["l2_l5_buy_qty"] - frame["l2_l5_sell_qty"], frame["l2_l5_buy_qty"] + frame["l2_l5_sell_qty"])
    frame["l1_l5_order_imbalance"] = safe_div(frame["l1_l5_buy_orders"] - frame["l1_l5_sell_orders"], frame["l1_l5_buy_orders"] + frame["l1_l5_sell_orders"])
    frame["l2_l5_order_imbalance"] = safe_div(frame["l2_l5_buy_orders"] - frame["l2_l5_sell_orders"], frame["l2_l5_buy_orders"] + frame["l2_l5_sell_orders"])
    frame["bid_depth_slope_l1_l5"] = frame["buy_1_price"] - frame["buy_5_price"]
    frame["ask_depth_slope_l1_l5"] = frame["sell_5_price"] - frame["sell_1_price"]
    frame["depth_pressure"] = safe_div(frame["l1_l5_qty_imbalance"], frame["l1_spread"])
    frame["l2_l5_pressure"] = safe_div(frame["l2_l5_qty_imbalance"], frame["l1_spread"])
    return frame


def nearest_value(group: pd.DataFrame, column: str, relative_second: int) -> float:
    idx = (group["relative_second"].astype(int) - relative_second).abs().idxmin()
    return float(group.loc[idx, column])


def materialize_features(joined: pd.DataFrame) -> pd.DataFrame:
    if joined.empty:
        return pd.DataFrame()
    ticks = enrich_ticks(joined)
    rows: list[dict[str, Any]] = []
    feature_cols = [
        "l1_spread",
        "l1_mid",
        "l1_microprice",
        "l1_queue_imbalance",
        "l1_l5_qty_imbalance",
        "l2_l5_qty_imbalance",
        "l1_l5_order_imbalance",
        "l2_l5_order_imbalance",
        "bid_depth_slope_l1_l5",
        "ask_depth_slope_l1_l5",
        "depth_pressure",
        "l2_l5_pressure",
    ]
    for (event_id, symbol), group in ticks.groupby(["event_id", "symbol"], dropna=False):
        group = group.sort_values("relative_second")
        pre = group[group["relative_second"].astype(int) < 0]
        row: dict[str, Any] = {
            "event_id": event_id,
            "event_time_ist": group["event_time_ist"].iloc[0],
            "event_type": group["event_type"].iloc[0],
            "symbol": symbol,
            "source_tick_rows": int(len(group)),
            "relative_second_min": int(group["relative_second"].min()),
            "relative_second_max": int(group["relative_second"].max()),
        }
        event_mid = nearest_value(group, "l1_mid", 0)
        row["event_mid"] = event_mid
        for col in feature_cols:
            row[f"event_{col}"] = nearest_value(group, col, 0)
            row[f"pre_mean_{col}"] = float(pre[col].mean()) if not pre.empty else float("nan")
        row["pre_mid_std"] = float(pre["l1_mid"].std()) if len(pre) > 1 else 0.0
        for horizon in (60, 300, 900, 1800):
            horizon_mid = nearest_value(group, "l1_mid", horizon)
            row[f"target_return_{horizon}s_bps"] = (horizon_mid / event_mid - 1.0) * 10000.0 if event_mid else float("nan")
        row["target_pressure_shift_300s"] = nearest_value(group, "depth_pressure", 300) - row["event_depth_pressure"]
        row["target_l2_l5_pressure_shift_300s"] = nearest_value(group, "l2_l5_pressure", 300) - row["event_l2_l5_pressure"]
        rows.append(row)
    return pd.DataFrame(rows)


def build_quality(features: pd.DataFrame) -> pd.DataFrame:
    if features.empty:
        return pd.DataFrame([{"quality_id": "empty_feature_matrix", "passed": False, "observed": 0, "required": ">0"}])
    feature_cols = [c for c in features.columns if c.startswith("event_") or c.startswith("pre_mean_") or c == "pre_mid_std"]
    target_cols = [c for c in features.columns if c.startswith("target_")]
    return pd.DataFrame(
        [
            {"quality_id": "feature_matrix_nonempty", "passed": len(features) > 0, "observed": int(len(features)), "required": ">0"},
            {"quality_id": "symbol_breadth_32", "passed": int(features["symbol"].nunique()) >= 32, "observed": int(features["symbol"].nunique()), "required": ">=32"},
            {"quality_id": "materialized_event_rows_nonzero", "passed": int(features["event_id"].nunique()) >= 1, "observed": int(features["event_id"].nunique()), "required": ">=1"},
            {"quality_id": "feature_columns_nonempty", "passed": len(feature_cols) > 0, "observed": len(feature_cols), "required": ">0"},
            {"quality_id": "target_columns_nonempty", "passed": len(target_cols) > 0, "observed": len(target_cols), "required": ">0"},
            {"quality_id": "no_required_feature_nulls", "passed": int(features[feature_cols].isna().sum().sum()) == 0, "observed": int(features[feature_cols].isna().sum().sum()), "required": 0},
            {"quality_id": "relative_window_complete", "passed": bool(((features["relative_second_min"].astype(int) <= -900) & (features["relative_second_max"].astype(int) >= 1800)).all()), "observed": int(((features["relative_second_min"].astype(int) <= -900) & (features["relative_second_max"].astype(int) >= 1800)).sum()), "required": int(len(features))},
        ]
    )


def build_gate_evaluation(phase309: pd.DataFrame, features: pd.DataFrame, quality: pd.DataFrame) -> pd.DataFrame:
    phase309_complete = as_int(metric_value(phase309, "phase309_event_feature_precommit_complete", 0))
    quality_pass = bool(not quality.empty and quality["passed"].astype(bool).all())
    gates = [
        ("P310_PHASE309_PRECOMMIT_COMPLETE", phase309_complete == 1, phase309_complete, 1),
        ("P310_FEATURE_MATRIX_NONEMPTY", len(features) > 0, len(features), ">0"),
        ("P310_FEATURE_QUALITY_PASS", quality_pass, int(quality_pass), 1),
        ("P310_FULL_DEPTH_FEATURES_MATERIALIZED", "event_l2_l5_qty_imbalance" in features.columns and "pre_mean_l2_l5_pressure" in features.columns, "l2_l5 columns present", "present"),
        ("P310_NO_STRATEGY_SEARCH_OPENED", True, "strategy_search_allowed_now=0", 0),
        ("P310_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(features: pd.DataFrame, quality: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    next_action = NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION
    return pd.DataFrame(
        [
            ("phase310_event_feature_materialization_complete", 1, "Phase310 event-catalyst feature materialization completed"),
            ("phase310_feature_matrix_rows", int(len(features)), "Feature matrix rows"),
            ("phase310_materialized_event_rows", int(features["event_id"].nunique()) if not features.empty else 0, "Distinct materialized events"),
            ("phase310_materialized_symbols", int(features["symbol"].nunique()) if not features.empty else 0, "Distinct materialized symbols"),
            ("phase310_quality_rows", int(len(quality)), "Quality rows"),
            ("phase310_quality_pass_rows", int(quality["passed"].astype(bool).sum()) if not quality.empty else 0, "Quality rows passed"),
            ("phase310_full_depth_features_materialized", int("event_l2_l5_qty_imbalance" in features.columns and "pre_mean_l2_l5_pressure" in features.columns), "Depth levels 2-5 feature columns present"),
            ("phase310_strategy_search_allowed_now", 0, "No strategy search in Phase310"),
            ("phase310_strategy_replay_allowed", 0, "No replay"),
            ("phase310_strategy_promotion_allowed", 0, "No promotion"),
            ("phase310_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase310_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase310_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase310_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase310_next_best_action", next_action, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, features: pd.DataFrame, quality: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase310 Event-Catalyst Feature Materialization",
        "",
        "Phase310 materializes compact event-symbol features and response diagnostics from the Phase307 joined full-depth artifact.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Quality",
        "",
        _markdown_table(quality),
        "",
        "## Feature matrix preview",
        "",
        _markdown_table(features.head(40)),
        "",
        "## Gates",
        "",
        _markdown_table(gates),
    ]
    (output_dir / "phase310_event_catalyst_feature_materialization_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase307_dir: Path = DEFAULT_PHASE307_DIR, phase309_dir: Path = DEFAULT_PHASE309_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase309 = read_csv(phase309_dir / "phase309_acceptance_summary.csv")
    joined = pd.read_parquet(phase307_dir / "phase307_joined_event_top5_depth.parquet")
    features = materialize_features(joined)
    quality = build_quality(features)
    gates = build_gate_evaluation(phase309, features, quality)
    acceptance = build_acceptance(features, quality, gates)

    features.to_csv(output_dir / "phase310_event_catalyst_feature_matrix.csv", index=False)
    quality.to_csv(output_dir / "phase310_feature_quality.csv", index=False)
    gates.to_csv(output_dir / "phase310_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase310_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, features, quality, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase310_event_catalyst_feature_materialization",
        **reproducibility_fields(
            artifact_id="phase310",
            generated_utc=generated_utc,
            inputs={
                "phase307_joined_parquet": str(phase307_dir / "phase307_joined_event_top5_depth.parquet"),
                "phase309_acceptance": str(phase309_dir / "phase309_acceptance_summary.csv"),
            },
            parameters={"feature_role_policy": "pre_event_and_event_features_only_targets_separate"},
            outputs={"acceptance_summary": str(output_dir / "phase310_acceptance_summary.csv")},
            cost_model_version="not_applicable_feature_materialization_only",
            latency_model_version="not_applicable_feature_materialization_only",
        ),
    }
    (output_dir / "phase310_event_catalyst_feature_materialization_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize Phase310 event-catalyst full-depth features.")
    parser.add_argument("--phase307-dir", type=Path, default=DEFAULT_PHASE307_DIR)
    parser.add_argument("--phase309-dir", type=Path, default=DEFAULT_PHASE309_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase307_dir, args.phase309_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
