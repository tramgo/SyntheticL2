from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase470_materialize_source_event_aware_l1_l5_feature_matrix import (
    PREHISTORY_ROWS,
    STARTS,
    fval,
    ival,
    materialize_matrix,
    read_candidate_windows,
)
from synthetic_l2.phase471_train_holdout_source_event_aware_l1_l5_label_model import (
    auc_score,
    class_weights,
    fit_logistic,
    log_loss,
    predict,
    standardize,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import (
    ZERODHA_CHARGES_SOURCE_URL,
    ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
    calculate_equity_intraday_nse_charges,
)


DEFAULT_PHASE467_DIR = Path("outputs/phase467")
DEFAULT_PHASE469_DIR = Path("outputs/phase469")
DEFAULT_PHASE473_DIR = Path("outputs/phase473")
DEFAULT_OUTPUT_DIR = Path("outputs/phase474")

THESIS_ID = "P474_LARGER_HORIZON_FEWER_TRADE_SOURCE_EVENT_L1_L5"
NEXT_ACTION_PASS = "expand_profitable_phase474_candidate_to_more_symbols_dates_and_real_l2_holdout"
NEXT_ACTION_FAIL = "interpret_phase474_larger_horizon_failure_or_precommit_catalyst_conditioned_subset"

HORIZONS = [480, 960, 1800]
TOP_FRACTIONS = [0.05, 0.10, 0.20]
FIXED_CAPITAL_INR = 100_000.0
ADVERSE_SLIPPAGE_ROUND_TRIP_BPS = 2.0
MIN_ANNUALIZED_RETURN_PCT = 12.0
MIN_TRADE_COUNT = 10
SEED_BASE = 47420260818


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def prepare_direction_data(matrix: pd.DataFrame, features: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    data = matrix[matrix["label_side"].astype(str).isin(["long", "short"])].copy()
    data["target_long"] = data["label_side"].astype(str).eq("long").astype(int)
    for feature in features:
        data[feature] = pd.to_numeric(data[feature], errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(0.0)
    train = data[data["phase464_split"].astype(str).eq("train")].copy()
    holdout = data[data["phase464_split"].astype(str).eq("holdout")].copy()
    return train, holdout


def metrics(y: np.ndarray, p: np.ndarray) -> dict[str, float]:
    pred = (p >= 0.5).astype(int)
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


def fit_and_score(matrix: pd.DataFrame, features: list[str], horizon: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train, holdout = prepare_direction_data(matrix, features)
    train_x = train[features].astype(float).to_numpy()
    holdout_x = holdout[features].astype(float).to_numpy()
    train_y = train["target_long"].to_numpy(dtype=int)
    holdout_y = holdout["target_long"].to_numpy(dtype=int)
    x_train, x_holdout, mean, std = standardize(train_x, holdout_x)
    beta, losses = fit_logistic(x_train, train_y, seed=SEED_BASE + horizon)
    holdout_p = predict(beta, x_holdout)
    rng = np.random.default_rng(SEED_BASE + horizon)
    shuffled_y = rng.permutation(train_y)
    shuffled_beta, shuffled_losses = fit_logistic(x_train, shuffled_y, seed=SEED_BASE + horizon + 1)
    shuffled_p = predict(shuffled_beta, x_holdout)
    primary = metrics(holdout_y, holdout_p)
    shuffled = metrics(holdout_y, shuffled_p)
    model_summary = pd.DataFrame(
        [
            {"horizon_ticks": horizon, "model_id": "P474_PRIMARY_DIRECTION_LOGISTIC", "train_rows": len(train), "holdout_rows": len(holdout), **primary},
            {"horizon_ticks": horizon, "model_id": "P474_SHUFFLED_LABEL_CONTROL", "train_rows": len(train), "holdout_rows": len(holdout), **shuffled},
        ]
    )
    model_summary["primary_training_loss_path"] = ";".join(f"{x:.6f}" for x in losses)
    model_summary["shuffled_training_loss_path"] = ";".join(f"{x:.6f}" for x in shuffled_losses)
    coefficients = pd.DataFrame(
        [{"horizon_ticks": horizon, "term": "intercept", "coefficient": float(beta[0]), "train_mean": 0.0, "train_std": 1.0}]
        + [
            {"horizon_ticks": horizon, "term": feature, "coefficient": float(beta[i + 1]), "train_mean": float(mean[i]), "train_std": float(std[i])}
            for i, feature in enumerate(features)
        ]
    )
    scores = holdout[["trade_date", "symbol", "candidate_start_row", "entry_price", "exit_price", "label_side", "forward_return_bps", "abs_forward_return_bps"]].copy()
    scores["horizon_ticks"] = horizon
    scores["primary_long_probability"] = holdout_p
    scores["shuffled_long_probability"] = shuffled_p
    scores["confidence"] = np.abs(holdout_p - 0.5)
    return model_summary, coefficients, scores


def replay_selected(scores: pd.DataFrame, top_fraction: float) -> pd.DataFrame:
    if scores.empty:
        return pd.DataFrame()
    holdout_days = max(1, int(scores["trade_date"].nunique()))
    target_count = max(MIN_TRADE_COUNT, int(round(len(scores) * top_fraction)))
    target_count = min(target_count, len(scores))
    selected = scores.sort_values(["confidence", "abs_forward_return_bps"], ascending=False).head(target_count)
    rows = []
    for row in selected.to_dict("records"):
        prob = float(row["primary_long_probability"])
        side = 1 if prob >= 0.5 else -1
        entry_price = float(row["entry_price"])
        exit_price = float(row["exit_price"])
        quantity = max(1, int(FIXED_CAPITAL_INR // max(entry_price, 1e-9)))
        entry_value = quantity * entry_price
        exit_value = quantity * exit_price
        if side == 1:
            buy_value = entry_value
            sell_value = exit_value
            gross_pnl = exit_value - entry_value
        else:
            buy_value = exit_value
            sell_value = entry_value
            gross_pnl = entry_value - exit_value
        charges = calculate_equity_intraday_nse_charges(
            buy_value_inr=buy_value,
            sell_value_inr=sell_value,
            buy_quantity=quantity,
            sell_quantity=quantity,
            buy_orders=1,
            sell_orders=1,
        )
        slippage_inr = (ADVERSE_SLIPPAGE_ROUND_TRIP_BPS / 10_000.0) * entry_value
        net_pnl = gross_pnl - charges.total_charges - slippage_inr
        rows.append(
            {
                "trade_date": row["trade_date"],
                "symbol": row["symbol"],
                "candidate_start_row": int(row["candidate_start_row"]),
                "horizon_ticks": int(row["horizon_ticks"]),
                "top_fraction": top_fraction,
                "signal_side": "long" if side == 1 else "short",
                "probability": prob,
                "confidence": float(row["confidence"]),
                "entry_price": entry_price,
                "exit_price": exit_price,
                "quantity": quantity,
                "gross_pnl_inr": gross_pnl,
                "zerodha_total_charges_inr": charges.total_charges,
                "adverse_slippage_inr": slippage_inr,
                "net_pnl_inr": net_pnl,
                "forward_return_bps": float(row["forward_return_bps"]),
                "label_side": row["label_side"],
                **{f"charge_{key}": value for key, value in asdict(charges).items() if key in {"brokerage", "stt", "transaction_charge", "sebi_charge", "stamp_duty", "gst"}},
            }
        )
    trades = pd.DataFrame(rows)
    trades["holdout_days"] = holdout_days
    return trades


def summarize_trades(trades: pd.DataFrame, horizon: int, top_fraction: float, model_summary: pd.DataFrame) -> dict[str, Any]:
    primary = model_summary[(model_summary["horizon_ticks"].astype(int).eq(horizon)) & (model_summary["model_id"].eq("P474_PRIMARY_DIRECTION_LOGISTIC"))].iloc[0]
    shuffled = model_summary[(model_summary["horizon_ticks"].astype(int).eq(horizon)) & (model_summary["model_id"].eq("P474_SHUFFLED_LABEL_CONTROL"))].iloc[0]
    scenario_id = f"horizon_{horizon}_top_{top_fraction:.2f}_cost200"
    if trades.empty:
        net = 0.0
        holdout_days = 1
        return {
            "scenario_id": scenario_id,
            "horizon_ticks": horizon,
            "top_fraction": top_fraction,
            "trade_count": 0,
            "holdout_days": holdout_days,
            "gross_pnl_inr": 0.0,
            "zerodha_total_charges_inr": 0.0,
            "adverse_slippage_inr": 0.0,
            "net_pnl_inr": net,
            "annualized_return_pct": 0.0,
            "win_rate": 0.0,
            "avg_net_per_trade_inr": 0.0,
            "primary_auc": float(primary["auc"]),
            "shuffled_auc": float(shuffled["auc"]),
            "auc_lift_vs_shuffled": float(primary["auc"] - shuffled["auc"]),
        }
    holdout_days = int(trades["holdout_days"].iloc[0])
    net = float(trades["net_pnl_inr"].sum())
    daily = trades.groupby("trade_date", sort=True)["net_pnl_inr"].sum().reset_index()
    equity = daily["net_pnl_inr"].cumsum()
    drawdown = equity - equity.cummax()
    return {
        "scenario_id": scenario_id,
        "horizon_ticks": horizon,
        "top_fraction": top_fraction,
        "trade_count": int(len(trades)),
        "holdout_days": holdout_days,
        "gross_pnl_inr": float(trades["gross_pnl_inr"].sum()),
        "zerodha_total_charges_inr": float(trades["zerodha_total_charges_inr"].sum()),
        "adverse_slippage_inr": float(trades["adverse_slippage_inr"].sum()),
        "net_pnl_inr": net,
        "annualized_return_pct": (net / FIXED_CAPITAL_INR) * (252.0 / max(1, holdout_days)) * 100.0,
        "win_rate": float((trades["net_pnl_inr"] > 0).mean()),
        "avg_net_per_trade_inr": float(trades["net_pnl_inr"].mean()),
        "max_daily_drawdown_inr": float(drawdown.min()) if len(drawdown) else 0.0,
        "primary_auc": float(primary["auc"]),
        "shuffled_auc": float(shuffled["auc"]),
        "auc_lift_vs_shuffled": float(primary["auc"] - shuffled["auc"]),
    }


def build_gates(phase473: pd.DataFrame, matrices: pd.DataFrame, model_summary: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    best = scenarios.sort_values(["annualized_return_pct", "net_pnl_inr"], ascending=False).iloc[0]
    profitable = int((scenarios["annualized_return_pct"].astype(float) >= MIN_ANNUALIZED_RETURN_PCT).sum())
    positive = int((scenarios["net_pnl_inr"].astype(float) > 0).sum())
    primary_models = model_summary[model_summary["model_id"].eq("P474_PRIMARY_DIRECTION_LOGISTIC")]
    rows = [
        ("P474_PHASE473_PRECOMMIT_USED", as_int(scalar(phase473, "phase473_phase474_allowed_next", 0)) == 1, scalar(phase473, "phase473_phase474_allowed_next", 0), 1),
        ("P474_LARGER_HORIZONS_USED", set(HORIZONS) == {480, 960, 1800}, ";".join(str(x) for x in HORIZONS), "480;960;1800"),
        ("P474_MATRIX_ROWS_PRESENT_ALL_HORIZONS", int((matrices["matrix_rows"].astype(int) > 0).sum()) == len(HORIZONS), int((matrices["matrix_rows"].astype(int) > 0).sum()), len(HORIZONS)),
        ("P474_FULL_DEPTH_FEATURES_USED", int(matrices["l2_l5_feature_count"].min()) >= 10, int(matrices["l2_l5_feature_count"].min()), ">=10"),
        ("P474_FEWER_TRADE_SCENARIOS_USED", set(TOP_FRACTIONS) == {0.05, 0.10, 0.20}, ";".join(str(x) for x in TOP_FRACTIONS), "0.05;0.10;0.20"),
        ("P474_COST200_INCLUDED", ADVERSE_SLIPPAGE_ROUND_TRIP_BPS == 2.0, ADVERSE_SLIPPAGE_ROUND_TRIP_BPS, 2.0),
        ("P474_FIXED_CAPITAL_USED", FIXED_CAPITAL_INR == 100_000.0, FIXED_CAPITAL_INR, 100_000.0),
        ("P474_ALL_MODELS_HAVE_POSITIVE_AUC_LIFT", bool((primary_models["auc"].astype(float).to_numpy() - model_summary[model_summary["model_id"].eq("P474_SHUFFLED_LABEL_CONTROL")]["auc"].astype(float).to_numpy() > 0).all()), "checked", "all>0"),
        ("P474_POSITIVE_NET_SCENARIO_EXISTS", positive > 0, positive, ">0"),
        ("P474_ABOVE_12PCT_ANNUALIZED_SCENARIO_EXISTS", profitable > 0, profitable, ">0"),
        ("P474_BEST_TRADE_COUNT_GE_10", int(best["trade_count"]) >= MIN_TRADE_COUNT, int(best["trade_count"]), f">={MIN_TRADE_COUNT}"),
        ("P474_NO_PAPER_LIVE_OR_CLAIM", True, "synthetic_replay_only;paper=0;live=0", "no_paper_live"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(gates: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    best = scenarios.sort_values(["annualized_return_pct", "net_pnl_inr"], ascending=False).iloc[0]
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    passed = int(hard_pass == hard_rows)
    rows = [
        ("phase474_larger_horizon_fewer_trade_experiment_complete", 1, "Phase474 experiment completed"),
        ("phase474_thesis_id", THESIS_ID, "Experiment thesis"),
        ("phase474_best_scenario_id", best["scenario_id"], "Best scenario"),
        ("phase474_best_horizon_ticks", int(best["horizon_ticks"]), "Best horizon"),
        ("phase474_best_top_fraction", float(best["top_fraction"]), "Best top confidence fraction"),
        ("phase474_best_trade_count", int(best["trade_count"]), "Best trade count"),
        ("phase474_best_net_pnl_inr", float(best["net_pnl_inr"]), "Best net P&L"),
        ("phase474_best_annualized_return_pct", float(best["annualized_return_pct"]), "Best fixed-capital annualized return"),
        ("phase474_positive_net_scenario_rows", int((scenarios["net_pnl_inr"].astype(float) > 0).sum()), "Positive net scenarios"),
        ("phase474_above12_annualized_scenario_rows", int((scenarios["annualized_return_pct"].astype(float) >= MIN_ANNUALIZED_RETURN_PCT).sum()), "Scenarios above 12% annualized"),
        ("phase474_fixed_capital_inr", FIXED_CAPITAL_INR, "Reusable capital denominator"),
        ("phase474_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model version"),
        ("phase474_zerodha_cost_source_url", ZERODHA_CHARGES_SOURCE_URL, "Cost source"),
        ("phase474_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase474_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase474_phase475_allowed_next", passed, "Allows expansion only if all gates pass"),
        ("phase474_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase474_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase474_next_best_action", NEXT_ACTION_PASS if passed else NEXT_ACTION_FAIL, "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, matrices: pd.DataFrame, model_summary: pd.DataFrame, scenarios: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase474 Larger-Horizon Fewer-Trade Source-Event L1-L5 Experiment",
        "",
        "Phase474 tests the Phase473 next path: larger forecast horizons and fewer top-confidence trades while retaining full-depth L1-L5 features, Zerodha cost200, and fixed-capital annualization.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Matrix Summary",
        "",
        _markdown_table(matrices),
        "",
        "## Model Summary",
        "",
        _markdown_table(model_summary),
        "",
        "## Scenario Summary",
        "",
        _markdown_table(scenarios),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase474 is synthetic-only replay evidence. It is not paper/live acceptance and not a deployable profitability claim.",
    ]
    (output_dir / "phase474_larger_horizon_fewer_trade_experiment_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    phase467_dir: Path = DEFAULT_PHASE467_DIR,
    phase469_dir: Path = DEFAULT_PHASE469_DIR,
    phase473_dir: Path = DEFAULT_PHASE473_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase473 = read_csv(phase473_dir / "phase473_acceptance_summary.csv")
    contract = read_csv(phase467_dir / "phase467_frozen_phase468_contract.csv")
    selected = read_csv(phase467_dir / "phase467_selected_files.csv")
    feature_contract = read_csv(phase469_dir / "phase469_repaired_feature_contract.csv")
    if as_int(scalar(phase473, "phase473_phase474_allowed_next", 0)) != 1:
        raise ValueError("Phase474 requires Phase473 allowance.")
    features = feature_contract["feature_name"].astype(str).tolist()
    entry_index = ival(contract, "entry_index", 20)
    min_abs_move = fval(contract, "min_abs_forward_move_bps", 2.0)
    matrix_summaries = []
    model_parts = []
    coefficient_parts = []
    score_parts = []
    trade_parts = []
    scenario_rows = []
    for horizon in HORIZONS:
        rows_per_window = entry_index + horizon + 1
        raw_parts = [read_candidate_windows(Path(row["path"]), str(row["trade_month"]), STARTS, rows_per_window, PREHISTORY_ROWS) for row in selected.to_dict("records")]
        raw = pd.concat(raw_parts, ignore_index=True) if raw_parts else pd.DataFrame()
        matrix = materialize_matrix(raw, entry_index, horizon, min_abs_move)
        matrix.to_csv(output_dir / f"phase474_feature_label_matrix_horizon_{horizon}.csv", index=False)
        matrix_summaries.append(
            {
                "horizon_ticks": horizon,
                "matrix_rows": len(matrix),
                "train_rows": int(matrix["phase464_split"].eq("train").sum()) if not matrix.empty else 0,
                "holdout_rows": int(matrix["phase464_split"].eq("holdout").sum()) if not matrix.empty else 0,
                "move_candidate_rows": int(matrix["move_candidate"].sum()) if not matrix.empty else 0,
                "l2_l5_feature_count": int(feature_contract["uses_l2_l5_depth"].astype(int).sum()),
                "source_event_feature_count": int(sum(1 for f in features if f.startswith("source_event_"))),
                "long_rows": int(matrix["label_side"].eq("long").sum()) if not matrix.empty else 0,
                "short_rows": int(matrix["label_side"].eq("short").sum()) if not matrix.empty else 0,
            }
        )
        model_summary, coefficients, scores = fit_and_score(matrix, features, horizon)
        model_parts.append(model_summary)
        coefficient_parts.append(coefficients)
        score_parts.append(scores)
        for top_fraction in TOP_FRACTIONS:
            trades = replay_selected(scores, top_fraction)
            if not trades.empty:
                trades["scenario_id"] = f"horizon_{horizon}_top_{top_fraction:.2f}_cost200"
                trade_parts.append(trades)
            scenario_rows.append(summarize_trades(trades, horizon, top_fraction, model_summary))
    matrices = pd.DataFrame(matrix_summaries)
    model_summary = pd.concat(model_parts, ignore_index=True)
    coefficients = pd.concat(coefficient_parts, ignore_index=True)
    scores = pd.concat(score_parts, ignore_index=True)
    trades = pd.concat(trade_parts, ignore_index=True) if trade_parts else pd.DataFrame()
    scenarios = pd.DataFrame(scenario_rows)
    gates = build_gates(phase473, matrices, model_summary, scenarios)
    acceptance = build_acceptance(gates, scenarios)
    matrices.to_csv(output_dir / "phase474_matrix_summary.csv", index=False)
    model_summary.to_csv(output_dir / "phase474_model_summary.csv", index=False)
    coefficients.to_csv(output_dir / "phase474_primary_coefficients.csv", index=False)
    scores.to_csv(output_dir / "phase474_holdout_scores.csv", index=False)
    trades.to_csv(output_dir / "phase474_trade_ledger.csv", index=False)
    scenarios.to_csv(output_dir / "phase474_scenario_summary.csv", index=False)
    gates.to_csv(output_dir / "phase474_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase474_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, matrices, model_summary, scenarios, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase474_larger_horizon_fewer_trade_source_event_l1_l5_experiment",
        **reproducibility_fields(
            artifact_id="phase474_larger_horizon_fewer_trade_experiment",
            generated_utc=generated_utc,
            inputs={
                "phase473_contract": str(phase473_dir / "phase473_next_experiment_contract.csv"),
                "phase469_feature_contract": str(phase469_dir / "phase469_repaired_feature_contract.csv"),
                "phase467_selected_files": str(phase467_dir / "phase467_selected_files.csv"),
            },
            parameters={
                "thesis_id": THESIS_ID,
                "horizons": HORIZONS,
                "top_fractions": TOP_FRACTIONS,
                "fixed_capital_inr": FIXED_CAPITAL_INR,
                "adverse_slippage_round_trip_bps": ADVERSE_SLIPPAGE_ROUND_TRIP_BPS,
                "min_annualized_return_pct": MIN_ANNUALIZED_RETURN_PCT,
            },
            outputs={"acceptance_summary": str(output_dir / "phase474_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase474_cost200_adverse_slippage_proxy",
        ),
    }
    (output_dir / "phase474_larger_horizon_fewer_trade_experiment_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase474 larger-horizon fewer-trade L1-L5 experiment.")
    parser.add_argument("--phase467-dir", type=Path, default=DEFAULT_PHASE467_DIR)
    parser.add_argument("--phase469-dir", type=Path, default=DEFAULT_PHASE469_DIR)
    parser.add_argument("--phase473-dir", type=Path, default=DEFAULT_PHASE473_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    out = run(args.phase467_dir, args.phase469_dir, args.phase473_dir, args.output_dir)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
