from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE464_DIR = Path("outputs/phase464")
DEFAULT_OUTPUT_DIR = Path("outputs/phase465")

THESIS_ID = "P465_TRAIN_HOLDOUT_PAST_ONLY_L1_L5_LABEL_MODEL"
NEXT_ACTION_PASS = "precommit_phase466_signal_replay_from_past_only_l1_l5_model_scores_with_cost200_no_live"
NEXT_ACTION_FAIL = "interpret_phase465_predictive_model_failure_or_expand_past_only_features_before_replay"

MIN_HOLDOUT_AUC = 0.53
MIN_AUC_LIFT_VS_SHUFFLED = 0.02
MIN_BALANCED_ACCURACY = 0.52
LEARNING_RATE = 0.08
L2_PENALTY = 0.04
EPOCHS = 2500
SEED = 46520260818


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def cval(contract: pd.DataFrame, key: str, default: str = "") -> str:
    rows = contract.loc[contract["contract_id"].astype(str).eq(key), "contract_value"].astype(str).tolist()
    return rows[0] if rows else default


def slist(value: str) -> list[str]:
    return [x.strip() for x in str(value).split(";") if x.strip()]


def sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(z, -40.0, 40.0)))


def standardize(train_x: np.ndarray, holdout_x: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    mean = train_x.mean(axis=0)
    std = train_x.std(axis=0)
    std = np.where(std < 1e-9, 1.0, std)
    return (train_x - mean) / std, (holdout_x - mean) / std, mean, std


def class_weights(y: np.ndarray) -> np.ndarray:
    pos = max(1, int(y.sum()))
    neg = max(1, int(len(y) - y.sum()))
    w_pos = len(y) / (2.0 * pos)
    w_neg = len(y) / (2.0 * neg)
    return np.where(y == 1, w_pos, w_neg)


def fit_logistic(x: np.ndarray, y: np.ndarray, seed: int = SEED) -> tuple[np.ndarray, list[float]]:
    rng = np.random.default_rng(seed)
    xb = np.column_stack([np.ones(len(x)), x])
    beta = rng.normal(0.0, 0.01, xb.shape[1])
    weights = class_weights(y)
    losses: list[float] = []
    for epoch in range(EPOCHS):
        p = sigmoid(xb @ beta)
        grad = (xb.T @ ((p - y) * weights)) / len(y)
        grad[1:] += L2_PENALTY * beta[1:]
        beta -= LEARNING_RATE * grad
        if epoch in {0, 99, 499, 999, EPOCHS - 1}:
            losses.append(log_loss(y, p, weights))
    return beta, losses


def predict(beta: np.ndarray, x: np.ndarray) -> np.ndarray:
    xb = np.column_stack([np.ones(len(x)), x])
    return sigmoid(xb @ beta)


def log_loss(y: np.ndarray, p: np.ndarray, weights: np.ndarray | None = None) -> float:
    p = np.clip(p, 1e-9, 1.0 - 1e-9)
    loss = -(y * np.log(p) + (1 - y) * np.log(1 - p))
    if weights is not None:
        loss = loss * weights
    return float(loss.mean())


def auc_score(y: np.ndarray, score: np.ndarray) -> float:
    pos = score[y == 1]
    neg = score[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return 0.5
    order = np.argsort(score, kind="mergesort")
    ranks = np.empty(len(score), dtype=float)
    ranks[order] = np.arange(1, len(score) + 1)
    pos_rank_sum = ranks[y == 1].sum()
    return float((pos_rank_sum - len(pos) * (len(pos) + 1) / 2.0) / (len(pos) * len(neg)))


def metrics(y: np.ndarray, p: np.ndarray, threshold: float = 0.5) -> dict[str, float]:
    pred = (p >= threshold).astype(int)
    tp = int(((pred == 1) & (y == 1)).sum())
    tn = int(((pred == 0) & (y == 0)).sum())
    fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum())
    tpr = tp / max(1, tp + fn)
    tnr = tn / max(1, tn + fp)
    return {
        "rows": float(len(y)),
        "positive_rate": float(y.mean()) if len(y) else 0.0,
        "auc": auc_score(y, p),
        "accuracy": float((pred == y).mean()) if len(y) else 0.0,
        "balanced_accuracy": float((tpr + tnr) / 2.0),
        "log_loss": log_loss(y, p),
        "tp": float(tp),
        "tn": float(tn),
        "fp": float(fp),
        "fn": float(fn),
    }


def threshold_scores(train: pd.DataFrame, holdout: pd.DataFrame, feature: str) -> tuple[np.ndarray, float, str]:
    best_auc = -1.0
    best_direction = "positive"
    for direction in ["positive", "negative"]:
        score = train[feature].astype(float).to_numpy()
        if direction == "negative":
            score = -score
        auc = auc_score(train["target_long"].to_numpy(), score)
        if auc > best_auc:
            best_auc = auc
            best_direction = direction
    holdout_score = holdout[feature].astype(float).to_numpy()
    if best_direction == "negative":
        holdout_score = -holdout_score
    ranks = pd.Series(holdout_score).rank(pct=True).to_numpy()
    return ranks, best_auc, best_direction


def prepare_data(matrix: pd.DataFrame, features: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    data = matrix[matrix["move_candidate"].astype(int).eq(1)].copy()
    data = data[data["label_side"].astype(str).isin(["long", "short"])].copy()
    data["target_long"] = data["label_side"].astype(str).eq("long").astype(int)
    for feature in features:
        data[feature] = pd.to_numeric(data[feature], errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(0.0)
    train = data[data["phase464_split"].astype(str).eq("train")].copy()
    holdout = data[data["phase464_split"].astype(str).eq("holdout")].copy()
    return train, holdout


def model_rows(train_y: np.ndarray, holdout_y: np.ndarray, holdout_p: np.ndarray, shuffled_p: np.ndarray, threshold_p: np.ndarray) -> pd.DataFrame:
    rows = []
    for model_id, p in [
        ("P465_PRIMARY_CLASS_WEIGHTED_LOGISTIC_L1_L5", holdout_p),
        ("P465_SHUFFLED_LABEL_CONTROL", shuffled_p),
        ("P465_L25_THRESHOLD_CONTROL", threshold_p),
    ]:
        m = metrics(holdout_y, p)
        m.update({"model_id": model_id, "train_rows": float(len(train_y)), "holdout_rows": float(len(holdout_y))})
        rows.append(m)
    return pd.DataFrame(rows)


def coefficient_table(features: list[str], beta: np.ndarray, mean: np.ndarray, std: np.ndarray) -> pd.DataFrame:
    rows = [{"term": "intercept", "coefficient": float(beta[0]), "train_mean": 0.0, "train_std": 1.0}]
    for i, feature in enumerate(features):
        rows.append({"term": feature, "coefficient": float(beta[i + 1]), "train_mean": float(mean[i]), "train_std": float(std[i])})
    return pd.DataFrame(rows)


def build_gates(phase464: pd.DataFrame, model_summary: pd.DataFrame, train: pd.DataFrame, holdout: pd.DataFrame, allowed_features: list[str], forbidden: list[str]) -> pd.DataFrame:
    primary = model_summary[model_summary["model_id"].eq("P465_PRIMARY_CLASS_WEIGHTED_LOGISTIC_L1_L5")].iloc[0]
    shuffled = model_summary[model_summary["model_id"].eq("P465_SHUFFLED_LABEL_CONTROL")].iloc[0]
    threshold = model_summary[model_summary["model_id"].eq("P465_L25_THRESHOLD_CONTROL")].iloc[0]
    auc_lift = float(primary["auc"] - shuffled["auc"])
    gates = [
        ("P465_PHASE464_PRECOMMIT_USED", as_int(scalar(phase464, "phase464_phase465_allowed_next", 0)) == 1, scalar(phase464, "phase464_phase465_allowed_next", 0), 1),
        ("P465_TRAIN_ROWS_PRESENT", len(train) > 0, len(train), ">0"),
        ("P465_HOLDOUT_ROWS_PRESENT", len(holdout) > 0, len(holdout), ">0"),
        ("P465_BOTH_CLASSES_TRAIN", train["target_long"].nunique() == 2, int(train["target_long"].nunique()), 2),
        ("P465_BOTH_CLASSES_HOLDOUT", holdout["target_long"].nunique() == 2, int(holdout["target_long"].nunique()), 2),
        ("P465_FULL_DEPTH_FEATURE_USED", "l25_imbalance" in allowed_features, "l25_imbalance" if "l25_imbalance" in allowed_features else "", "l25_imbalance"),
        ("P465_FORBIDDEN_FEATURES_EXCLUDED", set(allowed_features).isdisjoint(set(forbidden)), ";".join(sorted(set(allowed_features) & set(forbidden))), "empty"),
        ("P465_HOLDOUT_AUC_GE_053", float(primary["auc"]) >= MIN_HOLDOUT_AUC, float(primary["auc"]), f">={MIN_HOLDOUT_AUC}"),
        ("P465_AUC_LIFT_VS_SHUFFLED_GE_002", auc_lift >= MIN_AUC_LIFT_VS_SHUFFLED, auc_lift, f">={MIN_AUC_LIFT_VS_SHUFFLED}"),
        ("P465_BALANCED_ACCURACY_GE_052", float(primary["balanced_accuracy"]) >= MIN_BALANCED_ACCURACY, float(primary["balanced_accuracy"]), f">={MIN_BALANCED_ACCURACY}"),
        ("P465_PRIMARY_NOT_WORSE_THAN_L25_THRESHOLD", float(primary["auc"]) >= float(threshold["auc"]), f"primary={float(primary['auc'])};threshold={float(threshold['auc'])}", "primary>=threshold"),
        ("P465_NO_STRATEGY_PNL", True, "model_fit_only", "no_pnl"),
        ("P465_NO_PAPER_LIVE_OR_CLAIM", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(gates: pd.DataFrame, model_summary: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    passed = int(hard_pass == hard_rows)
    primary = model_summary[model_summary["model_id"].eq("P465_PRIMARY_CLASS_WEIGHTED_LOGISTIC_L1_L5")].iloc[0]
    shuffled = model_summary[model_summary["model_id"].eq("P465_SHUFFLED_LABEL_CONTROL")].iloc[0]
    rows = [
        ("phase465_train_holdout_past_only_l1_l5_label_model_complete", 1, "Phase465 model fit/evaluation completed"),
        ("phase465_thesis_id", THESIS_ID, "Model fit thesis"),
        ("phase465_primary_holdout_auc", float(primary["auc"]), "Primary holdout AUC"),
        ("phase465_shuffled_holdout_auc", float(shuffled["auc"]), "Shuffled-label control AUC"),
        ("phase465_auc_lift_vs_shuffled", float(primary["auc"] - shuffled["auc"]), "AUC lift versus shuffled-label control"),
        ("phase465_primary_holdout_balanced_accuracy", float(primary["balanced_accuracy"]), "Primary holdout balanced accuracy"),
        ("phase465_strategy_pnl_generated", 0, "No strategy P&L"),
        ("phase465_strategy_promotion_allowed", 0, "No promotion"),
        ("phase465_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase465_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase465_phase466_allowed_next", passed, "Allows precommitted score-to-signal replay only if all gates pass"),
        ("phase465_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase465_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase465_next_best_action", NEXT_ACTION_PASS if passed else NEXT_ACTION_FAIL, "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, model_summary: pd.DataFrame, coefficients: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase465 Train/Holdout Past-Only L1-L5 Label Model",
        "",
        "Phase465 trains and evaluates the Phase464 frozen past-only model contract. It does not create strategy P&L or acceptance.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Model Summary",
        "",
        _markdown_table(model_summary),
        "",
        "## Primary Coefficients",
        "",
        _markdown_table(coefficients),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: a predictive label model is not a strategy. Any score-to-order replay must be separately precommitted with costs, latency, slippage and risk.",
    ]
    (output_dir / "phase465_train_holdout_past_only_l1_l5_label_model_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase464_dir: Path = DEFAULT_PHASE464_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase464 = read_csv(phase464_dir / "phase464_acceptance_summary.csv")
    contract = read_csv(phase464_dir / "phase464_frozen_phase465_model_contract.csv")
    matrix = read_csv(phase464_dir / "phase464_split_label_matrix_preview.csv")
    if as_int(scalar(phase464, "phase464_phase465_allowed_next", 0)) != 1:
        raise ValueError("Phase465 requires Phase464 allowance.")
    features = slist(cval(contract, "allowed_features"))
    forbidden = slist(cval(contract, "forbidden_feature_columns"))
    train, holdout = prepare_data(matrix, features)
    train_x = train[features].astype(float).to_numpy()
    holdout_x = holdout[features].astype(float).to_numpy()
    train_y = train["target_long"].to_numpy(dtype=int)
    holdout_y = holdout["target_long"].to_numpy(dtype=int)
    x_train, x_holdout, mean, std = standardize(train_x, holdout_x)
    beta, losses = fit_logistic(x_train, train_y)
    holdout_p = predict(beta, x_holdout)
    rng = np.random.default_rng(SEED)
    shuffled_y = rng.permutation(train_y)
    shuffled_beta, shuffled_losses = fit_logistic(x_train, shuffled_y, seed=SEED + 1)
    shuffled_p = predict(shuffled_beta, x_holdout)
    threshold_p, threshold_train_auc, threshold_direction = threshold_scores(train, holdout, "l25_imbalance")
    model_summary = model_rows(train_y, holdout_y, holdout_p, shuffled_p, threshold_p)
    model_summary["primary_training_loss_path"] = ";".join(f"{x:.6f}" for x in losses)
    model_summary["shuffled_training_loss_path"] = ";".join(f"{x:.6f}" for x in shuffled_losses)
    model_summary["l25_threshold_train_auc"] = float(threshold_train_auc)
    model_summary["l25_threshold_direction"] = threshold_direction
    coefficients = coefficient_table(features, beta, mean, std)
    scored = holdout[["trade_date", "symbol", "candidate_start_row", "label_side", "forward_return_bps", "abs_forward_return_bps"]].copy()
    scored["primary_long_probability"] = holdout_p
    scored["shuffled_long_probability"] = shuffled_p
    scored["l25_threshold_score"] = threshold_p
    gates = build_gates(phase464, model_summary, train, holdout, features, forbidden)
    acc = build_acceptance(gates, model_summary)
    model_summary.to_csv(output_dir / "phase465_model_summary.csv", index=False)
    coefficients.to_csv(output_dir / "phase465_primary_coefficients.csv", index=False)
    scored.to_csv(output_dir / "phase465_holdout_scores.csv", index=False)
    gates.to_csv(output_dir / "phase465_gate_evaluation.csv", index=False)
    acc.to_csv(output_dir / "phase465_acceptance_summary.csv", index=False)
    write_report(output_dir, acc, model_summary, coefficients, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase465_train_holdout_past_only_l1_l5_label_model",
        **reproducibility_fields(
            artifact_id="phase465_train_holdout_past_only_l1_l5_label_model",
            generated_utc=generated_utc,
            inputs={"phase464_model_contract": str(phase464_dir / "phase464_frozen_phase465_model_contract.csv")},
            parameters={
                "thesis_id": THESIS_ID,
                "features": features,
                "learning_rate": LEARNING_RATE,
                "l2_penalty": L2_PENALTY,
                "epochs": EPOCHS,
                "seed": SEED,
                "min_holdout_auc": MIN_HOLDOUT_AUC,
                "min_auc_lift_vs_shuffled": MIN_AUC_LIFT_VS_SHUFFLED,
            },
            outputs={"acceptance_summary": str(output_dir / "phase465_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase465_model_fit_no_strategy_pnl",
        ),
    }
    (output_dir / "phase465_train_holdout_past_only_l1_l5_label_model_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acc


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase465 train/holdout past-only L1-L5 label model.")
    parser.add_argument("--phase464-dir", type=Path, default=DEFAULT_PHASE464_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    out = run(args.phase464_dir, args.output_dir)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
