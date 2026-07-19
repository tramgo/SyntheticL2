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


DEFAULT_OUTPUT_DIR = Path("outputs/phase123")
DEFAULT_PHASE79_DIR = Path("outputs/phase79")
DEFAULT_PHASE109_DIR = Path("outputs/phase109")
DEFAULT_STAGE02_DIR = Path("outputs/phase120/P120_LABEL_STAGE_02_TRAIN_HALF")
DEFAULT_PHASE122_DIR = Path("outputs/phase122")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def read_metric_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["metric", "value", "description"])
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


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    return int(round(as_float(value, float(default))))


def build_passive_symbol_toxicity(stage02_dir: Path) -> pd.DataFrame:
    p66 = read_csv(stage02_dir / "phase66/passive_label_symbol_rollup.csv")
    p68 = read_csv(stage02_dir / "phase68/replenishment_symbol_rollup.csv")
    p69 = read_csv(stage02_dir / "phase69/spread_transition_symbol_rollup.csv")
    rows: list[pd.DataFrame] = []
    if not p66.empty:
        rows.append(
            p66.groupby("symbol", sort=True)
            .agg(
                p66_rows=("symbol", "count"),
                p66_inferred_touches=("inferred_touches", "sum"),
                p66_mean_after_cost_bps=("mean_after_cost_bps_if_touched", "mean"),
                p66_min_adverse_selection_rate=("mean_adverse_selection_rate", "min"),
                p66_max_cost_clearing_rate=("mean_cost_clearing_rate", "max"),
            )
            .reset_index()
        )
    if not p68.empty:
        rows.append(
            p68.groupby("symbol", sort=True)
            .agg(
                p68_rows=("symbol", "count"),
                p68_inferred_touches=("inferred_touches", "sum"),
                p68_mean_after_cost_bps=("mean_after_cost_bps_if_touched", "mean"),
                p68_min_adverse_selection_rate=("mean_adverse_selection_rate", "min"),
                p68_max_cost_clearing_rate=("mean_cost_clearing_rate", "max"),
                p68_mean_replenishment_ratio=("mean_replenishment_ratio", "mean"),
            )
            .reset_index()
        )
    if not p69.empty:
        rows.append(
            p69.groupby("symbol", sort=True)
            .agg(
                p69_rows=("symbol", "count"),
                p69_signal_rows=("signal_rows", "sum"),
                p69_mean_after_cost_bps=("mean_after_cost_bps", "mean"),
                p69_max_cost_clearing_rate=("mean_cost_clearing_rate", "max"),
                p69_min_adverse_direction_rate=("mean_adverse_direction_rate", "min"),
            )
            .reset_index()
        )
    if not rows:
        return pd.DataFrame(columns=["symbol"])
    out = rows[0]
    for frame in rows[1:]:
        out = out.merge(frame, on="symbol", how="outer")
    for column in out.columns:
        if column != "symbol":
            out[column] = pd.to_numeric(out[column], errors="coerce").fillna(0.0)
    out["passive_min_adverse_rate"] = out[
        [
            col
            for col in ["p66_min_adverse_selection_rate", "p68_min_adverse_selection_rate", "p69_min_adverse_direction_rate"]
            if col in out.columns
        ]
    ].min(axis=1)
    out["passive_max_cost_clearing_rate"] = out[
        [col for col in ["p66_max_cost_clearing_rate", "p68_max_cost_clearing_rate", "p69_max_cost_clearing_rate"] if col in out.columns]
    ].max(axis=1)
    return out


def build_label_matrix(base_dir: Path, phase79_dir: Path, phase109_dir: Path, stage02_dir: Path) -> pd.DataFrame:
    profile = read_csv(base_dir / phase79_dir / "partition_scenario_profile.csv")
    if profile.empty:
        return pd.DataFrame()
    toxicity = build_passive_symbol_toxicity(base_dir / stage02_dir)
    frame = profile.merge(toxicity, on="symbol", how="left")
    numeric_cols = [
        "duplicate_rate",
        "disconnect_gap_rate",
        "out_of_order_rate",
        "mean_spread_bps",
        "median_spread_bps",
        "p90_spread_bps",
        "mean_l1_depth",
        "mean_l5_depth",
        "one_tick_return_std",
        "passive_min_adverse_rate",
        "passive_max_cost_clearing_rate",
        "p66_mean_after_cost_bps",
        "p68_mean_after_cost_bps",
        "p69_mean_after_cost_bps",
    ]
    for column in numeric_cols:
        if column not in frame.columns:
            frame[column] = 0.0
        frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0.0)

    q_spread = float(frame["median_spread_bps"].quantile(0.75))
    q_imperfection = float((frame["duplicate_rate"] + frame["disconnect_gap_rate"] + frame["out_of_order_rate"]).quantile(0.75))
    q_low_depth = float(frame["mean_l1_depth"].quantile(0.25))
    q_low_vol = float(frame["one_tick_return_std"].quantile(0.25))
    q_high_vol = float(frame["one_tick_return_std"].quantile(0.90))
    gaps = read_csv(base_dir / phase109_dir / "calibrated_gap_summary.csv")
    residual_gap_fraction = float(pd.to_numeric(gaps.get("gap_fraction", pd.Series(dtype=float)), errors="coerce").fillna(0.0).max()) if not gaps.empty else 0.0

    frame["feed_imperfection_rate"] = frame["duplicate_rate"] + frame["disconnect_gap_rate"] + frame["out_of_order_rate"]
    frame["cost_toxicity_label"] = (
        (frame["passive_min_adverse_rate"] >= 0.90)
        | (frame["passive_max_cost_clearing_rate"] <= 0.0)
        | (frame["median_spread_bps"] >= q_spread)
    ).astype(int)
    frame["regime_realism_risk_label"] = (
        (frame["feed_imperfection_rate"] >= q_imperfection)
        | (frame["market_shock_rows"].astype(float) > 0)
        | (frame["symbol_shock_rows"].astype(float) > 0)
        | (residual_gap_fraction > 0.0)
    ).astype(int)
    frame["opportunity_abstention_label"] = (
        (frame["mean_l1_depth"] <= q_low_depth)
        | (frame["one_tick_return_std"] <= q_low_vol)
        | (frame["median_spread_bps"] >= q_spread)
        | (frame["one_tick_return_std"] >= q_high_vol)
    ).astype(int)
    frame["train_split"] = frame["trade_month"].astype(str).isin(["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"]).map(
        {True: "train", False: "holdout"}
    )
    frame["label_source"] = "phase79_partition_profile_plus_phase120_stage02_passive_toxicity"
    frame["strategy_replay_allowed"] = 0
    output_cols = [
        "trade_month",
        "trade_date",
        "symbol",
        "train_split",
        "rows_scanned",
        "regime_count",
        "feed_profile_count",
        "market_shock_rows",
        "symbol_shock_rows",
        "duplicate_rate",
        "disconnect_gap_rate",
        "out_of_order_rate",
        "feed_imperfection_rate",
        "median_spread_bps",
        "p90_spread_bps",
        "mean_l1_depth",
        "mean_l5_depth",
        "one_tick_return_std",
        "passive_min_adverse_rate",
        "passive_max_cost_clearing_rate",
        "cost_toxicity_label",
        "regime_realism_risk_label",
        "opportunity_abstention_label",
        "label_source",
        "strategy_replay_allowed",
    ]
    return frame[[col for col in output_cols if col in frame.columns]].sort_values(["trade_month", "symbol"], kind="mergesort")


def label_diagnostics(matrix: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for label in ["cost_toxicity_label", "regime_realism_risk_label", "opportunity_abstention_label"]:
        if matrix.empty or label not in matrix.columns:
            rows.append({"label": label, "rows": 0, "positive_rows": 0, "positive_rate": 0.0, "symbols": 0, "months": 0, "has_class_variation": False})
            continue
        positives = int(matrix[label].astype(int).sum())
        rows.append(
            {
                "label": label,
                "rows": int(len(matrix)),
                "positive_rows": positives,
                "positive_rate": positives / len(matrix) if len(matrix) else 0.0,
                "symbols": int(matrix["symbol"].nunique()),
                "months": int(matrix["trade_month"].nunique()),
                "train_rows": int(matrix["train_split"].eq("train").sum()),
                "holdout_rows": int(matrix["train_split"].eq("holdout").sum()),
                "has_class_variation": bool(0 < positives < len(matrix)),
            }
        )
    return pd.DataFrame(rows)


def build_baseline_diagnostics(matrix: pd.DataFrame) -> pd.DataFrame:
    if matrix.empty:
        return pd.DataFrame()
    rows = []
    for label in ["cost_toxicity_label", "regime_realism_risk_label", "opportunity_abstention_label"]:
        train = matrix[matrix["train_split"].eq("train")]
        holdout = matrix[matrix["train_split"].eq("holdout")]
        train_rate = float(train[label].mean()) if not train.empty else 0.0
        holdout_rate = float(holdout[label].mean()) if not holdout.empty else 0.0
        rows.append(
            {
                "label": label,
                "train_positive_rate": train_rate,
                "holdout_positive_rate": holdout_rate,
                "absolute_train_holdout_rate_gap": abs(train_rate - holdout_rate),
                "baseline_model": "train_prior_probability",
                "model_fit_allowed_next": bool(0.0 < train_rate < 1.0 and 0.0 < holdout_rate < 1.0),
            }
        )
    return pd.DataFrame(rows)


def build_gate_evaluation(matrix: pd.DataFrame, diagnostics: pd.DataFrame, phase122: pd.DataFrame) -> pd.DataFrame:
    strategy_replay = as_int(metric_value(phase122, "phase122_strategy_replay_allowed"))
    rows = int(len(matrix))
    symbols = int(matrix["symbol"].nunique()) if not matrix.empty else 0
    months = int(matrix["trade_month"].nunique()) if not matrix.empty else 0
    varied_labels = int(diagnostics["has_class_variation"].astype(bool).sum()) if not diagnostics.empty else 0
    return pd.DataFrame(
        [
            {
                "gate_id": "P123_LABEL_MATRIX_EXISTS",
                "gate_pass": int(rows > 0),
                "evidence": f"rows={rows}",
            },
            {
                "gate_id": "P123_BREADTH",
                "gate_pass": int(symbols >= 20 and months >= 4),
                "evidence": f"symbols={symbols}; months={months}",
            },
            {
                "gate_id": "P123_LABEL_VARIATION",
                "gate_pass": int(varied_labels >= 2),
                "evidence": f"labels_with_class_variation={varied_labels}",
            },
            {
                "gate_id": "P123_NO_REPLAY",
                "gate_pass": int(strategy_replay == 0 and (matrix['strategy_replay_allowed'].sum() == 0 if not matrix.empty else True)),
                "evidence": f"phase122_strategy_replay_allowed={strategy_replay}",
            },
        ]
    )


def build_acceptance_summary(matrix: pd.DataFrame, diagnostics: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    model_fit_allowed = int(gates["gate_pass"].astype(bool).all() and diagnostics["has_class_variation"].astype(bool).any())
    return pd.DataFrame(
        [
            ("phase123_filter_label_rows", int(len(matrix)), "Filter label matrix rows"),
            ("phase123_filter_label_symbols", int(matrix["symbol"].nunique()) if not matrix.empty else 0, "Symbols covered by label matrix"),
            ("phase123_filter_label_months", int(matrix["trade_month"].nunique()) if not matrix.empty else 0, "Months covered by label matrix"),
            ("phase123_label_diagnostic_rows", int(len(diagnostics)), "Filter labels diagnosed"),
            ("phase123_labels_with_class_variation", int(diagnostics["has_class_variation"].astype(bool).sum()) if not diagnostics.empty else 0, "Labels suitable for future classifier fitting"),
            ("phase123_gate_rows", int(len(gates)), "Label matrix gates evaluated"),
            ("phase123_all_gates_pass", int(gates["gate_pass"].astype(bool).all()) if not gates.empty else 0, "1 means label matrix passes all no-replay readiness gates"),
            ("phase123_filter_model_fit_allowed_next", model_fit_allowed, "1 means a future non-trading filter model fit may be attempted"),
            ("phase123_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase123_next_best_action", "fit_phase124_non_trading_filter_baselines_if_class_variation_present", "Recommended next milestone"),
            ("phase123_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model retained for future filter validation"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase123 Filter Label Matrix Builder",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase123 builds the first no-replay label matrix for the Phase122 non-trading filters.",
        "Rows are symbol/month partitions. Labels describe cost toxicity, synthetic realism risk and abstention opportunity, not trade direction.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase123_filter_label_matrix_builder_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase123(
    base_dir: Path,
    output_dir: Path,
    phase79_dir: Path,
    phase109_dir: Path,
    stage02_dir: Path,
    phase122_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    matrix = build_label_matrix(base_dir, phase79_dir, phase109_dir, stage02_dir)
    diagnostics = label_diagnostics(matrix)
    baselines = build_baseline_diagnostics(matrix)
    phase122 = read_metric_table(base_dir / phase122_dir / "phase122_non_trading_filter_acceptance_summary.csv")
    gates = build_gate_evaluation(matrix, diagnostics, phase122)
    acceptance = build_acceptance_summary(matrix, diagnostics, gates)

    matrix.to_csv(output_dir / "filter_label_matrix.csv", index=False)
    diagnostics.to_csv(output_dir / "filter_label_diagnostics.csv", index=False)
    baselines.to_csv(output_dir / "filter_baseline_diagnostics.csv", index=False)
    gates.to_csv(output_dir / "filter_label_matrix_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase123_filter_label_matrix_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Filter Label Diagnostics": diagnostics,
            "Baseline Diagnostics": baselines,
            "Gate Evaluation": gates,
            "Filter Label Matrix Sample": matrix.head(40),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase123_filter_label_matrix_builder",
        "strategy_replay_allowed": 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase123",
            generated_utc=generated_utc,
            inputs={
                "phase79_partition_scenario_profile": str(phase79_dir / "partition_scenario_profile.csv"),
                "phase109_calibrated_gap_summary": str(phase109_dir / "calibrated_gap_summary.csv"),
                "stage02_phase66_symbol_rollup": str(stage02_dir / "phase66/passive_label_symbol_rollup.csv"),
                "stage02_phase68_symbol_rollup": str(stage02_dir / "phase68/replenishment_symbol_rollup.csv"),
                "stage02_phase69_symbol_rollup": str(stage02_dir / "phase69/spread_transition_symbol_rollup.csv"),
                "phase122_acceptance": str(phase122_dir / "phase122_non_trading_filter_acceptance_summary.csv"),
            },
            parameters={
                "matrix_grain": "trade_month_symbol",
                "policy": "no_replay_no_buy_sell_signals",
                "train_months": "2026-01..2026-06",
                "holdout_months": "2026-07..2026-12",
            },
            outputs={
                "label_matrix": str(output_dir / "filter_label_matrix.csv"),
                "label_diagnostics": str(output_dir / "filter_label_diagnostics.csv"),
                "baseline_diagnostics": str(output_dir / "filter_baseline_diagnostics.csv"),
                "gate_evaluation": str(output_dir / "filter_label_matrix_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase123_filter_label_matrix_acceptance_summary.csv"),
                "report": str(output_dir / "phase123_filter_label_matrix_builder_report.md"),
                "manifest": str(output_dir / "phase123_filter_label_matrix_builder_manifest.json"),
            },
            random_seed="none_deterministic_label_matrix",
            scenario_ids="phase123_non_trading_filter_label_matrix",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_label_matrix",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase123_filter_label_matrix_builder_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase123 no-replay filter label matrix.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--phase79-dir", type=Path, default=DEFAULT_PHASE79_DIR)
    parser.add_argument("--phase109-dir", type=Path, default=DEFAULT_PHASE109_DIR)
    parser.add_argument("--stage02-dir", type=Path, default=DEFAULT_STAGE02_DIR)
    parser.add_argument("--phase122-dir", type=Path, default=DEFAULT_PHASE122_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase123(
        base_dir=args.base_dir,
        output_dir=args.output_dir,
        phase79_dir=args.phase79_dir,
        phase109_dir=args.phase109_dir,
        stage02_dir=args.stage02_dir,
        phase122_dir=args.phase122_dir,
    )


if __name__ == "__main__":
    main()
