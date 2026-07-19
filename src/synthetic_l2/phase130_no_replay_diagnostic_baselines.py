from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase130")
DEFAULT_PHASE129_DIR = Path("outputs/phase129")
DEFAULT_PHASE117_DIR = Path("outputs/phase117")

LABELS = [
    "p129_regime_stability_label",
    "p129_liquidity_opportunity_label",
    "p129_cost_toxicity_refinement_label",
]
FEATURES = [
    "feed_imperfection_rate",
    "median_spread_bps",
    "p90_spread_bps",
    "mean_l1_depth",
    "mean_l5_depth",
    "one_tick_return_std",
    "passive_min_adverse_rate",
    "regime_realism_risk_label",
    "realism_review_flag",
    "opportunity_abstention_label",
]
FORBIDDEN_SIGNALS = "buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim"


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


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


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


def add_chronological_split(matrix: pd.DataFrame, holdout_months: int = 2) -> pd.DataFrame:
    if matrix.empty:
        return pd.DataFrame()
    frame = matrix.copy()
    months = sorted(frame["trade_month"].astype(str).unique())
    holdout = set(months[-holdout_months:]) if len(months) > holdout_months else set(months[-1:])
    frame["phase130_split"] = frame["trade_month"].astype(str).map(lambda month: "holdout" if month in holdout else "train")
    return frame


def threshold_candidates(series: pd.Series) -> list[float]:
    values = pd.to_numeric(series, errors="coerce").dropna()
    if values.empty:
        return []
    return sorted({float(values.quantile(q)) for q in [0.10, 0.25, 0.50, 0.75, 0.90]})


def evaluate_predictions(
    label: str,
    model_id: str,
    train_y: list[int],
    holdout_y: list[int],
    holdout_prob: list[float],
    details: dict[str, Any],
) -> dict[str, Any]:
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
        "forbidden_outputs": FORBIDDEN_SIGNALS,
        **details,
    }


def prior_model(label: str, train: pd.DataFrame, holdout: pd.DataFrame) -> dict[str, Any]:
    train_y = train[label].astype(int).tolist()
    holdout_y = holdout[label].astype(int).tolist()
    prior = clip_prob(sum(train_y) / len(train_y)) if train_y else 0.5
    return evaluate_predictions(
        label=label,
        model_id="train_prior_probability",
        train_y=train_y,
        holdout_y=holdout_y,
        holdout_prob=[prior for _ in holdout_y],
        details={"feature": "", "direction": "", "threshold": "", "train_prediction_rate": prior, "baseline_type": "prior"},
    )


def threshold_model(label: str, feature: str, train: pd.DataFrame, holdout: pd.DataFrame, direction: str, threshold: float) -> dict[str, Any]:
    train_y = train[label].astype(int).tolist()
    holdout_y = holdout[label].astype(int).tolist()
    train_values = pd.to_numeric(train[feature], errors="coerce").fillna(0.0)
    holdout_values = pd.to_numeric(holdout[feature], errors="coerce").fillna(0.0)
    if direction == "ge":
        train_pred = train_values.ge(threshold).astype(int)
        holdout_pred = holdout_values.ge(threshold).astype(int)
    else:
        train_pred = train_values.le(threshold).astype(int)
        holdout_pred = holdout_values.le(threshold).astype(int)
    holdout_prob = [0.80 if int(value) else 0.20 for value in holdout_pred.tolist()]
    return evaluate_predictions(
        label=label,
        model_id=f"threshold_{feature}_{direction}_{threshold:.8g}",
        train_y=train_y,
        holdout_y=holdout_y,
        holdout_prob=holdout_prob,
        details={
            "feature": feature,
            "direction": direction,
            "threshold": threshold,
            "train_prediction_rate": float(train_pred.mean()) if len(train_pred) else 0.0,
            "baseline_type": "single_feature_threshold",
        },
    )


def evaluate_baselines(matrix: pd.DataFrame) -> pd.DataFrame:
    if matrix.empty:
        return pd.DataFrame()
    train = matrix[matrix["phase130_split"].eq("train")].copy()
    holdout = matrix[matrix["phase130_split"].eq("holdout")].copy()
    rows: list[dict[str, Any]] = []
    for label in LABELS:
        if label not in matrix.columns:
            continue
        if train[label].nunique() < 2 or holdout[label].nunique() < 2:
            rows.append(
                {
                    "label": label,
                    "model_id": "not_fit_no_class_variation",
                    "train_rows": int(len(train)),
                    "holdout_rows": int(len(holdout)),
                    "train_positive_rate": float(train[label].mean()) if not train.empty else 0.0,
                    "holdout_positive_rate": float(holdout[label].mean()) if not holdout.empty else 0.0,
                    "holdout_brier": None,
                    "holdout_log_loss": None,
                    "holdout_accuracy": None,
                    "holdout_auc": None,
                    "strategy_replay_allowed": 0,
                    "forbidden_outputs": FORBIDDEN_SIGNALS,
                    "feature": "",
                    "direction": "",
                    "threshold": "",
                    "train_prediction_rate": "",
                    "baseline_type": "not_fit",
                }
            )
            continue
        rows.append(prior_model(label, train, holdout))
        for feature in FEATURES:
            if feature not in matrix.columns:
                continue
            for threshold in threshold_candidates(train[feature]):
                for direction in ["ge", "le"]:
                    rows.append(threshold_model(label, feature, train, holdout, direction, threshold))
    results = pd.DataFrame(rows)
    if not results.empty:
        results["holdout_brier"] = pd.to_numeric(results["holdout_brier"], errors="coerce")
        results["holdout_log_loss"] = pd.to_numeric(results["holdout_log_loss"], errors="coerce")
        results = results.sort_values(["label", "holdout_brier", "holdout_log_loss"], ascending=[True, True, True], kind="mergesort")
    return results


def build_model_selection(results: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for label in LABELS:
        group = results[results["label"].eq(label)].copy() if not results.empty else pd.DataFrame()
        if group.empty or group["holdout_brier"].dropna().empty:
            rows.append(
                {
                    "label": label,
                    "selected_model_id": "",
                    "prior_brier": None,
                    "best_brier": None,
                    "brier_improvement": None,
                    "holdout_log_loss": None,
                    "holdout_accuracy": None,
                    "holdout_auc": None,
                    "model_selected": False,
                    "selection_reason": "no_fit",
                    "strategy_replay_allowed": 0,
                }
            )
            continue
        prior_rows = group[group["model_id"].eq("train_prior_probability")]
        prior_brier = float(prior_rows["holdout_brier"].iloc[0]) if not prior_rows.empty else float(group["holdout_brier"].max())
        best = group.dropna(subset=["holdout_brier"]).iloc[0]
        best_brier = float(best["holdout_brier"])
        improvement = prior_brier - best_brier
        selected = bool(improvement > 0.005 and str(best["model_id"]) != "train_prior_probability")
        rows.append(
            {
                "label": label,
                "selected_model_id": str(best["model_id"]),
                "prior_brier": prior_brier,
                "best_brier": best_brier,
                "brier_improvement": improvement,
                "holdout_log_loss": best.get("holdout_log_loss"),
                "holdout_accuracy": best.get("holdout_accuracy"),
                "holdout_auc": best.get("holdout_auc"),
                "model_selected": selected,
                "selection_reason": "beats_prior_brier_by_minimum_margin" if selected else "no_material_brier_improvement_over_prior",
                "strategy_replay_allowed": 0,
            }
        )
    return pd.DataFrame(rows)


def build_split_summary(matrix: pd.DataFrame) -> pd.DataFrame:
    if matrix.empty:
        return pd.DataFrame()
    rows = []
    for split, group in matrix.groupby("phase130_split", sort=True):
        row: dict[str, Any] = {
            "phase130_split": split,
            "rows": int(len(group)),
            "symbols": int(group["symbol"].nunique()),
            "months": int(group["trade_month"].nunique()),
            "trade_months": ";".join(sorted(group["trade_month"].astype(str).unique())),
            "strategy_replay_allowed": 0,
        }
        for label in LABELS:
            row[f"{label}_positive_rate"] = float(group[label].mean()) if label in group.columns else None
        rows.append(row)
    return pd.DataFrame(rows)


def build_guardrails() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "guardrail_id": "P130_NO_REPLAY",
                "requirement": "Phase130 fits diagnostic label baselines only and cannot emit strategy replay artifacts.",
                "enforcement": "strategy_replay_allowed=0 and forbidden_outputs carried through every model row.",
            },
            {
                "guardrail_id": "P130_CHRONOLOGICAL_HOLDOUT",
                "requirement": "Model diagnostics must be evaluated on later months than the fit set.",
                "enforcement": "phase130_split assigns the final two trade months to holdout.",
            },
            {
                "guardrail_id": "P130_BASELINES_NOT_TRADING_RULES",
                "requirement": "Selected models are screeners for label quality, not buy/sell rules.",
                "enforcement": f"Forbidden outputs remain {FORBIDDEN_SIGNALS}.",
            },
            {
                "guardrail_id": "P130_REAL_ANCHOR_REMAINS_PRIMARY",
                "requirement": "More real Zerodha L2 days remain the primary path to future replay unlock.",
                "enforcement": "Phase117 real-anchor blocker is carried into the acceptance summary.",
            },
        ]
    )


def build_gate_evaluation(matrix: pd.DataFrame, split_summary: pd.DataFrame, results: pd.DataFrame, selection: pd.DataFrame, phase117: pd.DataFrame) -> pd.DataFrame:
    ready_days = as_int(metric_value(phase117, "phase117_current_ready_real_anchor_days"))
    days_needed = as_int(metric_value(phase117, "phase117_additional_days_needed_for_min"))
    selected = int(selection["model_selected"].astype(bool).sum()) if not selection.empty else 0
    holdout_rows = int(split_summary.loc[split_summary["phase130_split"].eq("holdout"), "rows"].iloc[0]) if not split_summary.empty and split_summary["phase130_split"].eq("holdout").any() else 0
    return pd.DataFrame(
        [
            {"gate_id": "P130_SPLIT_EXISTS", "gate_pass": int(not split_summary.empty and set(split_summary["phase130_split"]) == {"holdout", "train"}), "evidence": f"split_rows={len(split_summary)}; holdout_rows={holdout_rows}"},
            {"gate_id": "P130_BASELINE_RESULTS_EXIST", "gate_pass": int(not results.empty), "evidence": f"baseline_result_rows={len(results)}"},
            {"gate_id": "P130_SELECTION_ROWS_EXIST", "gate_pass": int(len(selection) == len(LABELS)), "evidence": f"selection_rows={len(selection)}"},
            {"gate_id": "P130_MATERIAL_DIAGNOSTIC_SIGNAL", "gate_pass": int(selected > 0), "evidence": f"selected_models={selected}"},
            {"gate_id": "P130_NO_REPLAY", "gate_pass": int(not matrix.empty and matrix["strategy_replay_allowed"].sum() == 0 and (results.empty or results["strategy_replay_allowed"].sum() == 0)), "evidence": "strategy_replay_allowed remains 0"},
            {"gate_id": "P130_REAL_ANCHOR_STILL_PRIMARY", "gate_pass": int(ready_days < 5 and days_needed > 0), "evidence": f"ready_real_anchor_days={ready_days}; days_needed={days_needed}"},
        ]
    )


def build_acceptance_summary(matrix: pd.DataFrame, results: pd.DataFrame, selection: pd.DataFrame, gates: pd.DataFrame, phase117: pd.DataFrame) -> pd.DataFrame:
    ready_days = as_int(metric_value(phase117, "phase117_current_ready_real_anchor_days"))
    days_needed = as_int(metric_value(phase117, "phase117_additional_days_needed_for_min"))
    selected = int(selection["model_selected"].astype(bool).sum()) if not selection.empty else 0
    return pd.DataFrame(
        [
            ("phase130_label_matrix_rows", int(len(matrix)), "Phase129 rows split for no-replay diagnostic baselines"),
            ("phase130_baseline_result_rows", int(len(results)), "Prior and threshold baseline evaluations emitted"),
            ("phase130_selection_rows", int(len(selection)), "Label-level model selection rows emitted"),
            ("phase130_selected_diagnostic_models", selected, "Labels with material holdout Brier improvement over prior"),
            ("phase130_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase130_all_gates_pass", int(gates["gate_pass"].astype(bool).all()) if not gates.empty else 0, "1 means Phase130 obeys no-replay guardrails"),
            ("phase130_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase130_current_ready_real_anchor_days", ready_days, "Real anchor days currently ready from Phase117"),
            ("phase130_additional_real_anchor_days_needed", days_needed, "Additional real anchor days needed before replay unlock"),
            ("phase130_next_best_action", "promote_selected_diagnostics_to_phase131_permission_update_or_continue_real_anchor_acquisition", "Recommended next milestone"),
            ("phase130_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model retained for audit continuity"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase130 No-Replay Diagnostic Baselines",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase130 fits deterministic baseline screeners for Phase129 diagnostic labels using a chronological holdout.",
        "These are label diagnostics only. They do not authorize strategy replay, order simulation, or profitability claims.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase130_no_replay_diagnostic_baselines_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase130(base_dir: Path, output_dir: Path, phase129_dir: Path, phase117_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_matrix = read_csv(base_dir / phase129_dir / "allowed_context_label_matrix.csv")
    phase117 = read_metric_table(base_dir / phase117_dir / "phase117_real_anchor_acquisition_acceptance_summary.csv")
    matrix = add_chronological_split(raw_matrix)
    split_summary = build_split_summary(matrix)
    results = evaluate_baselines(matrix)
    selection = build_model_selection(results)
    guardrails = build_guardrails()
    gates = build_gate_evaluation(matrix, split_summary, results, selection, phase117)
    acceptance = build_acceptance_summary(matrix, results, selection, gates, phase117)

    matrix.to_csv(output_dir / "phase130_split_label_matrix.csv", index=False)
    split_summary.to_csv(output_dir / "chronological_split_summary.csv", index=False)
    results.to_csv(output_dir / "diagnostic_baseline_results.csv", index=False)
    selection.to_csv(output_dir / "diagnostic_model_selection.csv", index=False)
    guardrails.to_csv(output_dir / "diagnostic_baseline_guardrails.csv", index=False)
    gates.to_csv(output_dir / "diagnostic_baseline_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase130_no_replay_diagnostic_baselines_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Chronological Split Summary": split_summary,
            "Diagnostic Model Selection": selection,
            "Best Baseline Results": results.groupby("label", sort=True).head(5) if not results.empty else results,
            "Guardrails": guardrails,
            "Gate Evaluation": gates,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase130_no_replay_diagnostic_baselines",
        "strategy_replay_allowed": 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase130",
            generated_utc=generated_utc,
            inputs={
                "phase129_label_matrix": str(phase129_dir / "allowed_context_label_matrix.csv"),
                "phase117_acceptance": str(phase117_dir / "phase117_real_anchor_acquisition_acceptance_summary.csv"),
            },
            parameters={
                "split_policy": "chronological_final_two_trade_months_holdout",
                "model_family": "prior_and_single_feature_threshold_diagnostics",
                "selection_rule": "best_holdout_brier_beats_prior_by_more_than_0.005",
                "replay_policy": "closed",
                "forbidden_outputs": FORBIDDEN_SIGNALS,
            },
            outputs={
                "split_matrix": str(output_dir / "phase130_split_label_matrix.csv"),
                "split_summary": str(output_dir / "chronological_split_summary.csv"),
                "baseline_results": str(output_dir / "diagnostic_baseline_results.csv"),
                "model_selection": str(output_dir / "diagnostic_model_selection.csv"),
                "guardrails": str(output_dir / "diagnostic_baseline_guardrails.csv"),
                "gates": str(output_dir / "diagnostic_baseline_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase130_no_replay_diagnostic_baselines_acceptance_summary.csv"),
                "report": str(output_dir / "phase130_no_replay_diagnostic_baselines_report.md"),
                "manifest": str(output_dir / "phase130_no_replay_diagnostic_baselines_manifest.json"),
            },
            random_seed="none_deterministic_diagnostic_baselines",
            scenario_ids="phase130_allowed_context_no_replay_diagnostic_baselines",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_diagnostic_baselines",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase130_no_replay_diagnostic_baselines_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fit Phase130 no-replay diagnostic baselines for Phase129 labels.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--phase129-dir", type=Path, default=DEFAULT_PHASE129_DIR)
    parser.add_argument("--phase117-dir", type=Path, default=DEFAULT_PHASE117_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase130(base_dir=args.base_dir, output_dir=args.output_dir, phase129_dir=args.phase129_dir, phase117_dir=args.phase117_dir)


if __name__ == "__main__":
    main()
