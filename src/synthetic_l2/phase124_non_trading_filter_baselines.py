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


DEFAULT_OUTPUT_DIR = Path("outputs/phase124")
DEFAULT_PHASE123_DIR = Path("outputs/phase123")
LABELS = ["regime_realism_risk_label", "opportunity_abstention_label"]
FEATURES = [
    "feed_imperfection_rate",
    "median_spread_bps",
    "p90_spread_bps",
    "mean_l1_depth",
    "mean_l5_depth",
    "one_tick_return_std",
    "passive_min_adverse_rate",
]


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


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
        pc = clip_prob(p)
        total += -(float(y) * math.log(pc) + (1.0 - float(y)) * math.log(1.0 - pc))
    return float(total / len(y_true))


def accuracy(y_true: list[int], y_prob: list[float], threshold: float = 0.5) -> float:
    if not y_true:
        return 0.0
    hits = sum(int((p >= threshold) == bool(y)) for y, p in zip(y_true, y_prob))
    return float(hits / len(y_true))


def auc_score(y_true: list[int], y_score: list[float]) -> float | None:
    positives = [(score, idx) for idx, (y, score) in enumerate(zip(y_true, y_score)) if int(y) == 1]
    negatives = [(score, idx) for idx, (y, score) in enumerate(zip(y_true, y_score)) if int(y) == 0]
    if not positives or not negatives:
        return None
    wins = 0.0
    total = len(positives) * len(negatives)
    for ps, _ in positives:
        for ns, _ in negatives:
            if ps > ns:
                wins += 1.0
            elif ps == ns:
                wins += 0.5
    return float(wins / total)


def evaluate_predictions(label: str, model_id: str, train_y: list[int], holdout_y: list[int], holdout_prob: list[float], details: dict[str, Any]) -> dict[str, Any]:
    train_positive_rate = float(sum(train_y) / len(train_y)) if train_y else 0.0
    holdout_positive_rate = float(sum(holdout_y) / len(holdout_y)) if holdout_y else 0.0
    return {
        "label": label,
        "model_id": model_id,
        "train_rows": int(len(train_y)),
        "holdout_rows": int(len(holdout_y)),
        "train_positive_rate": train_positive_rate,
        "holdout_positive_rate": holdout_positive_rate,
        "holdout_brier": brier_score(holdout_y, holdout_prob),
        "holdout_log_loss": log_loss(holdout_y, holdout_prob),
        "holdout_accuracy": accuracy(holdout_y, holdout_prob),
        "holdout_auc": auc_score(holdout_y, holdout_prob),
        "strategy_replay_allowed": 0,
        **details,
    }


def train_prior_model(label: str, train: pd.DataFrame, holdout: pd.DataFrame) -> dict[str, Any]:
    train_y = train[label].astype(int).tolist()
    holdout_y = holdout[label].astype(int).tolist()
    prior = clip_prob(sum(train_y) / len(train_y)) if train_y else 0.5
    return evaluate_predictions(
        label,
        "train_prior_probability",
        train_y,
        holdout_y,
        [prior for _ in holdout_y],
        {"feature": "", "direction": "", "threshold": "", "train_prediction_rate": prior},
    )


def threshold_candidates(series: pd.Series) -> list[float]:
    values = pd.to_numeric(series, errors="coerce").dropna()
    if values.empty:
        return []
    return sorted({float(values.quantile(q)) for q in [0.25, 0.50, 0.75]})


def threshold_model(label: str, feature: str, train: pd.DataFrame, holdout: pd.DataFrame, direction: str, threshold: float) -> dict[str, Any]:
    train_y = train[label].astype(int).tolist()
    holdout_y = holdout[label].astype(int).tolist()
    if direction == "ge":
        train_pred = (pd.to_numeric(train[feature], errors="coerce").fillna(0.0) >= threshold).astype(int)
        holdout_pred = (pd.to_numeric(holdout[feature], errors="coerce").fillna(0.0) >= threshold).astype(int)
    else:
        train_pred = (pd.to_numeric(train[feature], errors="coerce").fillna(0.0) <= threshold).astype(int)
        holdout_pred = (pd.to_numeric(holdout[feature], errors="coerce").fillna(0.0) <= threshold).astype(int)
    # Deterministic smoothed probability: hard threshold models are kept intentionally simple.
    holdout_prob = [0.75 if int(item) else 0.25 for item in holdout_pred.tolist()]
    return evaluate_predictions(
        label,
        f"threshold_{feature}_{direction}_{threshold:.8g}",
        train_y,
        holdout_y,
        holdout_prob,
        {
            "feature": feature,
            "direction": direction,
            "threshold": threshold,
            "train_prediction_rate": float(train_pred.mean()) if len(train_pred) else 0.0,
        },
    )


def evaluate_models(matrix: pd.DataFrame) -> pd.DataFrame:
    if matrix.empty:
        return pd.DataFrame()
    train = matrix[matrix["train_split"].eq("train")].copy()
    holdout = matrix[matrix["train_split"].eq("holdout")].copy()
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
                    "feature": "",
                    "direction": "",
                    "threshold": "",
                    "train_prediction_rate": "",
                }
            )
            continue
        rows.append(train_prior_model(label, train, holdout))
        for feature in FEATURES:
            if feature not in matrix.columns:
                continue
            for threshold in threshold_candidates(train[feature]):
                for direction in ["ge", "le"]:
                    rows.append(threshold_model(label, feature, train, holdout, direction, threshold))
    results = pd.DataFrame(rows)
    if not results.empty and "holdout_brier" in results.columns:
        results["holdout_brier"] = pd.to_numeric(results["holdout_brier"], errors="coerce")
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
                    "holdout_auc": None,
                    "model_selected": False,
                    "selection_reason": "no_fit",
                }
            )
            continue
        prior_rows = group[group["model_id"].eq("train_prior_probability")]
        prior_brier = float(prior_rows["holdout_brier"].iloc[0]) if not prior_rows.empty else float(group["holdout_brier"].max())
        best = group.dropna(subset=["holdout_brier"]).iloc[0]
        best_brier = float(best["holdout_brier"])
        improvement = prior_brier - best_brier
        auc = best.get("holdout_auc")
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
                "holdout_auc": auc,
                "model_selected": selected,
                "selection_reason": "beats_prior_brier_by_minimum_margin" if selected else "no_material_brier_improvement_over_prior",
            }
        )
    return pd.DataFrame(rows)


def build_gate_evaluation(selection: pd.DataFrame) -> pd.DataFrame:
    selected = int(selection["model_selected"].astype(bool).sum()) if not selection.empty else 0
    return pd.DataFrame(
        [
            {
                "gate_id": "P124_NON_TRADING_ONLY",
                "gate_pass": 1,
                "evidence": "All model outputs are label probabilities/screeners; strategy_replay_allowed remains 0.",
            },
            {
                "gate_id": "P124_BASELINE_FIT_EXISTS",
                "gate_pass": int(not selection.empty),
                "evidence": f"selection_rows={len(selection)}",
            },
            {
                "gate_id": "P124_MATERIAL_CALIBRATION_IMPROVEMENT",
                "gate_pass": int(selected > 0),
                "evidence": f"selected_models={selected}",
            },
            {
                "gate_id": "P124_REPLAY_LOCK",
                "gate_pass": 1,
                "evidence": "No buy/sell signal or replay artifact emitted.",
            },
        ]
    )


def build_acceptance_summary(results: pd.DataFrame, selection: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    selected = int(selection["model_selected"].astype(bool).sum()) if not selection.empty else 0
    return pd.DataFrame(
        [
            ("phase124_model_result_rows", int(len(results)), "Baseline model rows evaluated"),
            ("phase124_label_selection_rows", int(len(selection)), "Labels with model selection rows"),
            ("phase124_selected_filter_models", selected, "Non-trading filter models materially improving over train-prior baseline"),
            ("phase124_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase124_all_gates_pass", int(gates["gate_pass"].astype(bool).all()) if not gates.empty else 0, "1 means all Phase124 gates pass"),
            ("phase124_filter_integration_allowed_next", selected, "1+ means selected non-trading filter(s) can be prepared for integration as abstention/diagnostic layers"),
            ("phase124_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase124_next_best_action", "prepare_phase125_filter_integration_contract_if_selected_models_exist", "Recommended next milestone"),
            ("phase124_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model retained for future filter validation"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase124 Non-Trading Filter Baselines",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase124 evaluates transparent non-trading baselines for Phase123 filter labels.",
        "The outputs are calibration diagnostics only; no buy/sell side, order model, P&L replay or strategy promotion is emitted.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase124_non_trading_filter_baselines_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase124(base_dir: Path, phase123_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    matrix = read_csv(base_dir / phase123_dir / "filter_label_matrix.csv")
    results = evaluate_models(matrix)
    selection = build_model_selection(results)
    gates = build_gate_evaluation(selection)
    acceptance = build_acceptance_summary(results, selection, gates)

    results.to_csv(output_dir / "filter_baseline_model_results.csv", index=False)
    selection.to_csv(output_dir / "filter_baseline_model_selection.csv", index=False)
    gates.to_csv(output_dir / "filter_baseline_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase124_filter_baseline_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Model Selection": selection,
            "Gate Evaluation": gates,
            "Top Model Results": results.head(30),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase124_non_trading_filter_baselines",
        "strategy_replay_allowed": 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase124",
            generated_utc=generated_utc,
            inputs={"phase123_filter_label_matrix": str(phase123_dir / "filter_label_matrix.csv")},
            parameters={
                "labels": "|".join(LABELS),
                "features": "|".join(FEATURES),
                "selection_rule": "holdout_brier_improvement_gt_0p005_vs_train_prior",
                "policy": "no_replay_no_trade_signal",
            },
            outputs={
                "model_results": str(output_dir / "filter_baseline_model_results.csv"),
                "model_selection": str(output_dir / "filter_baseline_model_selection.csv"),
                "gate_evaluation": str(output_dir / "filter_baseline_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase124_filter_baseline_acceptance_summary.csv"),
                "report": str(output_dir / "phase124_non_trading_filter_baselines_report.md"),
                "manifest": str(output_dir / "phase124_non_trading_filter_baselines_manifest.json"),
            },
            random_seed="none_deterministic_baselines",
            scenario_ids="phase124_non_trading_filter_baseline_evaluation",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_filter_baseline",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase124_non_trading_filter_baselines_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate Phase124 non-trading filter baselines.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--phase123-dir", type=Path, default=DEFAULT_PHASE123_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase124(base_dir=args.base_dir, phase123_dir=args.phase123_dir, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
