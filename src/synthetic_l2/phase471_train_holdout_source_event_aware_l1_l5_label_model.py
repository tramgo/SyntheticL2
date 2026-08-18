from __future__ import annotations

import argparse
import json
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


DEFAULT_PHASE469_DIR = Path("outputs/phase469")
DEFAULT_PHASE470_DIR = Path("outputs/phase470")
DEFAULT_OUTPUT_DIR = Path("outputs/phase471")

THESIS_ID = "P471_TRAIN_HOLDOUT_SOURCE_EVENT_AWARE_L1_L5_LABEL_MODEL"
NEXT_ACTION_PASS = "precommit_phase472_score_to_signal_replay_with_cost200_no_live"
NEXT_ACTION_FAIL = "interpret_phase471_predictive_model_failure_before_any_replay"

MIN_HOLDOUT_AUC = 0.53
MIN_AUC_LIFT_VS_SHUFFLED = 0.02
MIN_BALANCED_ACCURACY = 0.52
LEARNING_RATE = 0.08
L2_PENALTY = 0.04
EPOCHS = 2500
SEED = 47120260818
PRIMARY_MODEL_ID = "P471_PRIMARY_CLASS_WEIGHTED_LOGISTIC_SOURCE_EVENT_L1_L5"
SHUFFLED_MODEL_ID = "P471_SHUFFLED_LABEL_CONTROL"
L25_THRESHOLD_MODEL_ID = "P471_L25_THRESHOLD_CONTROL"


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


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


def log_loss(y: np.ndarray, p: np.ndarray, weights: np.ndarray | None = None) -> float:
    p = np.clip(p, 1e-9, 1.0 - 1e-9)
    loss = -(y * np.log(p) + (1 - y) * np.log(1 - p))
    if weights is not None:
        loss = loss * weights
    return float(loss.mean())


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
    return sigmoid(np.column_stack([np.ones(len(x)), x]) @ beta)


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
    return pd.Series(holdout_score).rank(pct=True).to_numpy(), best_auc, best_direction


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
        (PRIMARY_MODEL_ID, holdout_p),
        (SHUFFLED_MODEL_ID, shuffled_p),
        (L25_THRESHOLD_MODEL_ID, threshold_p),
    ]:
        row = metrics(holdout_y, p)
        row.update({"model_id": model_id, "train_rows": float(len(train_y)), "holdout_rows": float(len(holdout_y))})
        rows.append(row)
    return pd.DataFrame(rows)


def coefficient_table(features: list[str], beta: np.ndarray, mean: np.ndarray, std: np.ndarray, feature_contract: pd.DataFrame) -> pd.DataFrame:
    rows = [{"term": "intercept", "coefficient": float(beta[0]), "train_mean": 0.0, "train_std": 1.0, "uses_l2_l5_depth": 0}]
    uses = dict(zip(feature_contract["feature_name"].astype(str), feature_contract["uses_l2_l5_depth"].astype(int)))
    for i, feature in enumerate(features):
        rows.append({"term": feature, "coefficient": float(beta[i + 1]), "train_mean": float(mean[i]), "train_std": float(std[i]), "uses_l2_l5_depth": int(uses.get(feature, 0))})
    return pd.DataFrame(rows)


def build_gates(phase470: pd.DataFrame, model_summary: pd.DataFrame, train: pd.DataFrame, holdout: pd.DataFrame, features: list[str], feature_contract: pd.DataFrame) -> pd.DataFrame:
    primary = model_summary[model_summary["model_id"].eq(PRIMARY_MODEL_ID)].iloc[0]
    shuffled = model_summary[model_summary["model_id"].eq(SHUFFLED_MODEL_ID)].iloc[0]
    threshold = model_summary[model_summary["model_id"].eq(L25_THRESHOLD_MODEL_ID)].iloc[0]
    auc_lift = float(primary["auc"] - shuffled["auc"])
    l25_features = int(feature_contract["uses_l2_l5_depth"].astype(int).sum())
    source_event_features = int(sum(1 for f in features if f.startswith("source_event_")))
    gates = [
        ("P471_PHASE470_MATRIX_USED", as_int(scalar(phase470, "phase470_phase471_allowed_next", 0)) == 1, scalar(phase470, "phase470_phase471_allowed_next", 0), 1),
        ("P471_TRAIN_ROWS_PRESENT", len(train) > 0, len(train), ">0"),
        ("P471_HOLDOUT_ROWS_PRESENT", len(holdout) > 0, len(holdout), ">0"),
        ("P471_BOTH_CLASSES_TRAIN", train["target_long"].nunique() == 2, int(train["target_long"].nunique()), 2),
        ("P471_BOTH_CLASSES_HOLDOUT", holdout["target_long"].nunique() == 2, int(holdout["target_long"].nunique()), 2),
        ("P471_FULL_DEPTH_FEATURES_USED", l25_features >= 10, l25_features, ">=10"),
        ("P471_SOURCE_EVENT_FEATURES_USED", source_event_features >= 11, source_event_features, ">=11"),
        ("P471_HOLDOUT_AUC_GE_053", float(primary["auc"]) >= MIN_HOLDOUT_AUC, float(primary["auc"]), f">={MIN_HOLDOUT_AUC}"),
        ("P471_AUC_LIFT_VS_SHUFFLED_GE_002", auc_lift >= MIN_AUC_LIFT_VS_SHUFFLED, auc_lift, f">={MIN_AUC_LIFT_VS_SHUFFLED}"),
        ("P471_BALANCED_ACCURACY_GE_052", float(primary["balanced_accuracy"]) >= MIN_BALANCED_ACCURACY, float(primary["balanced_accuracy"]), f">={MIN_BALANCED_ACCURACY}"),
        ("P471_PRIMARY_NOT_WORSE_THAN_L25_THRESHOLD", float(primary["auc"]) >= float(threshold["auc"]), f"primary={float(primary['auc'])};threshold={float(threshold['auc'])}", "primary>=threshold"),
        ("P471_NO_STRATEGY_PNL", True, "model_fit_only", "no_pnl"),
        ("P471_NO_PAPER_LIVE_OR_CLAIM", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(gates: pd.DataFrame, model_summary: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    passed = int(hard_pass == hard_rows)
    primary = model_summary[model_summary["model_id"].eq(PRIMARY_MODEL_ID)].iloc[0]
    shuffled = model_summary[model_summary["model_id"].eq(SHUFFLED_MODEL_ID)].iloc[0]
    rows = [
        ("phase471_train_holdout_source_event_aware_l1_l5_label_model_complete", 1, "Phase471 model fit/evaluation completed"),
        ("phase471_thesis_id", THESIS_ID, "Model fit thesis"),
        ("phase471_primary_holdout_auc", float(primary["auc"]), "Primary holdout AUC"),
        ("phase471_shuffled_holdout_auc", float(shuffled["auc"]), "Shuffled-label control AUC"),
        ("phase471_auc_lift_vs_shuffled", float(primary["auc"] - shuffled["auc"]), "AUC lift versus shuffled-label control"),
        ("phase471_primary_holdout_balanced_accuracy", float(primary["balanced_accuracy"]), "Primary holdout balanced accuracy"),
        ("phase471_strategy_pnl_generated", 0, "No strategy P&L"),
        ("phase471_strategy_promotion_allowed", 0, "No promotion"),
        ("phase471_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase471_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase471_phase472_allowed_next", passed, "Allows score-to-signal replay only if all gates pass"),
        ("phase471_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase471_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase471_next_best_action", NEXT_ACTION_PASS if passed else NEXT_ACTION_FAIL, "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, model_summary: pd.DataFrame, coefficients: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase471 Train/Holdout Source-Event-Aware L1-L5 Label Model",
        "",
        "Phase471 trains and evaluates a class-weighted logistic model on the Phase470 source-event-aware feature-label matrix.",
        "",
        "It does not create strategy P&L or acceptance.",
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
    (output_dir / "phase471_train_holdout_source_event_aware_l1_l5_label_model_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase469_dir: Path = DEFAULT_PHASE469_DIR, phase470_dir: Path = DEFAULT_PHASE470_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase470 = read_csv(phase470_dir / "phase470_acceptance_summary.csv")
    feature_contract = read_csv(phase469_dir / "phase469_repaired_feature_contract.csv")
    matrix = read_csv(phase470_dir / "phase470_source_event_aware_feature_label_matrix.csv")
    if as_int(scalar(phase470, "phase470_phase471_allowed_next", 0)) != 1:
        raise ValueError("Phase471 requires Phase470 allowance.")
    features = feature_contract["feature_name"].astype(str).tolist()
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
    coefficients = coefficient_table(features, beta, mean, std, feature_contract)
    scored = holdout[["trade_date", "symbol", "candidate_start_row", "label_side", "forward_return_bps", "abs_forward_return_bps"]].copy()
    scored["primary_long_probability"] = holdout_p
    scored["shuffled_long_probability"] = shuffled_p
    scored["l25_threshold_score"] = threshold_p
    gates = build_gates(phase470, model_summary, train, holdout, features, feature_contract)
    acceptance = build_acceptance(gates, model_summary)
    model_summary.to_csv(output_dir / "phase471_model_summary.csv", index=False)
    coefficients.to_csv(output_dir / "phase471_primary_coefficients.csv", index=False)
    scored.to_csv(output_dir / "phase471_holdout_scores.csv", index=False)
    gates.to_csv(output_dir / "phase471_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase471_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, model_summary, coefficients, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase471_train_holdout_source_event_aware_l1_l5_label_model",
        **reproducibility_fields(
            artifact_id="phase471_train_holdout_source_event_aware_l1_l5_label_model",
            generated_utc=generated_utc,
            inputs={
                "phase469_feature_contract": str(phase469_dir / "phase469_repaired_feature_contract.csv"),
                "phase470_matrix": str(phase470_dir / "phase470_source_event_aware_feature_label_matrix.csv"),
            },
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
            outputs={"acceptance_summary": str(output_dir / "phase471_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase471_model_fit_no_strategy_pnl",
        ),
    }
    (output_dir / "phase471_train_holdout_source_event_aware_l1_l5_label_model_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase471 train/holdout source-event-aware L1-L5 label model.")
    parser.add_argument("--phase469-dir", type=Path, default=DEFAULT_PHASE469_DIR)
    parser.add_argument("--phase470-dir", type=Path, default=DEFAULT_PHASE470_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    out = run(args.phase469_dir, args.phase470_dir, args.output_dir)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
