from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase184_train_validation_replay_dry_run import build_model_frame, profile_cost_bps
from synthetic_l2.phase187_cost_aware_sparse_candidate import add_derived_fields
from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE176_DIR = Path("outputs/phase176")
DEFAULT_PHASE180_DIR = Path("outputs/phase180")
DEFAULT_PHASE181_DIR = Path("outputs/phase181")
DEFAULT_PHASE195_DIR = Path("outputs/phase195")
DEFAULT_OUTPUT_DIR = Path("outputs/phase196")
RANDOM_SEED = 196
ALLOWED_PROFILES = {"P180_RETAIL_MARKETABLE_DEFAULT", "P180_STRESSED_RETAIL"}
EVALUATION_ROLES = {"validation", "unassigned"}
FORBIDDEN_OUTPUTS = "test_result;test_replay_execution;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim"


BASE_FEATURES = [
    "top5_qty_imbalance",
    "l1_qty_imbalance",
    "receive_event_rate_zscore",
    "quote_churn_count",
    "depth_refresh_count",
    "stale_quote_duration_ms",
    "cross_symbol_arrival_share",
    "spread_bps",
]


def clean_numeric(series: pd.Series, clip_abs: float = 1_000_000.0) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(0.0).clip(-clip_abs, clip_abs)


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = "") -> Any:
    if frame.empty or "metric" not in frame.columns or "value" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def enrich_features(frame: pd.DataFrame) -> pd.DataFrame:
    out = add_derived_fields(frame)
    top5 = clean_numeric(out["top5_qty_imbalance"], 10.0)
    l1 = clean_numeric(out["l1_qty_imbalance"], 10.0)
    event_z = clean_numeric(out["receive_event_rate_zscore"], 25.0)
    churn_log = np.log1p(clean_numeric(out["quote_churn_count"], 1_000.0).clip(lower=0))
    out["top5_x_event_z"] = top5 * event_z
    out["l1_x_event_z"] = l1 * event_z
    out["top5_x_churn"] = top5 * churn_log
    out["l1_x_churn"] = l1 * churn_log
    out["depth_refresh_log"] = np.log1p(clean_numeric(out["depth_refresh_count"], 1_000.0).clip(lower=0))
    out["quote_churn_log"] = churn_log
    out["stale_quote_log_ms"] = np.log1p(clean_numeric(out["stale_quote_duration_ms"], 60_000.0).clip(lower=0))
    out["liquidity_tightness"] = -clean_numeric(out["spread_bps"], 1_000.0)
    return out


def model_grid() -> pd.DataFrame:
    families = {
        "imbalance_event": ["top5_qty_imbalance", "l1_qty_imbalance", "receive_event_rate_zscore", "top5_x_event_z", "l1_x_event_z"],
        "liquidity_churn": ["top5_qty_imbalance", "quote_churn_log", "depth_refresh_log", "top5_x_churn", "liquidity_tightness"],
        "stale_synchrony": ["top5_qty_imbalance", "stale_quote_log_ms", "cross_symbol_arrival_share", "receive_event_rate_zscore", "liquidity_tightness"],
        "full_micro": ["top5_qty_imbalance", "l1_qty_imbalance", "receive_event_rate_zscore", "top5_x_event_z", "quote_churn_log", "depth_refresh_log", "stale_quote_log_ms", "cross_symbol_arrival_share", "liquidity_tightness"],
    }
    rows: list[dict[str, Any]] = []
    for horizon_scope in ["1", "5"]:
        for family, features in families.items():
            for side_mode in ["signed_score", "inverse_score"]:
                for quantile in [0.975, 0.99]:
                    for max_spread_bps in [1.5, 2.5]:
                        rows.append(
                            {
                                "model_id": f"P196_{family.upper()}_H{horizon_scope}_{side_mode.replace('_score','').upper()}_Q{int(quantile*1000)}_S{str(max_spread_bps).replace('.', 'p')}",
                                "family": family,
                                "feature_columns": ";".join(features),
                                "horizon_scope": horizon_scope,
                                "side_mode": side_mode,
                                "score_quantile": quantile,
                                "max_spread_bps": max_spread_bps,
                                "max_decision_rate": 0.01,
                                "test_replay_allowed_in_phase196": 0,
                            }
                        )
    return pd.DataFrame(rows)


def filtered_frame(frame: pd.DataFrame, model: pd.Series) -> pd.DataFrame:
    out = frame.loc[pd.to_numeric(frame["spread_bps"], errors="coerce").le(float(model["max_spread_bps"]))].copy()
    scope = str(model["horizon_scope"])
    if scope != "all":
        out = out.loc[pd.to_numeric(out["horizon_sec"], errors="coerce").astype("Int64").astype(str).eq(scope)].copy()
    return out


def fit_model(train: pd.DataFrame, model: pd.Series) -> dict[str, Any]:
    data = filtered_frame(train, model)
    target = clean_numeric(data["future_mid_return_bps_next_bucket"], 10_000.0)
    weights: dict[str, float] = {}
    means: dict[str, float] = {}
    stds: dict[str, float] = {}
    score = pd.Series(0.0, index=data.index)
    for feature in str(model["feature_columns"]).split(";"):
        values = clean_numeric(data[feature])
        mean = float(values.mean()) if len(values) else 0.0
        std = float(values.std(ddof=0)) if len(values) else 1.0
        if not np.isfinite(std) or std <= 0:
            std = 1.0
        z = (values - mean) / std
        corr = float(z.corr(target)) if len(z) > 2 else 0.0
        if not np.isfinite(corr):
            corr = 0.0
        weights[feature] = corr
        means[feature] = mean
        stds[feature] = std
        score = score + corr * z
    if str(model["side_mode"]) == "inverse_score":
        score = -score
    abs_score = score.abs()
    threshold = float(abs_score.quantile(float(model["score_quantile"]))) if len(abs_score) else np.inf
    return {
        "model_id": model["model_id"],
        "train_rows": int(len(data)),
        "feature_weights": ";".join(f"{k}:{v:.8f}" for k, v in weights.items()),
        "feature_means": json.dumps(means, sort_keys=True),
        "feature_stds": json.dumps(stds, sort_keys=True),
        "score_threshold": threshold,
        "selection_split": "train",
        "validation_used_for_fit": 0,
        "extension_used_for_fit": 0,
        "test_used_for_fit": 0,
    }


def score_frame(frame: pd.DataFrame, model: pd.Series, fit: pd.Series) -> pd.Series:
    data = filtered_frame(frame, model)
    means = json.loads(str(fit["feature_means"]))
    stds = json.loads(str(fit["feature_stds"]))
    weights = {
        part.split(":", 1)[0]: float(part.split(":", 1)[1])
        for part in str(fit["feature_weights"]).split(";")
        if ":" in part
    }
    score = pd.Series(0.0, index=data.index)
    for feature, weight in weights.items():
        values = clean_numeric(data[feature])
        std = float(stds.get(feature, 1.0))
        if not np.isfinite(std) or std <= 0:
            std = 1.0
        score = score + weight * ((values - float(means.get(feature, 0.0))) / std)
    if str(model["side_mode"]) == "inverse_score":
        score = -score
    return score


def selected_events(frame: pd.DataFrame, model: pd.Series, fit: pd.Series, profile: pd.Series, rng: np.random.Generator) -> pd.DataFrame:
    data = filtered_frame(frame, model)
    score = score_frame(frame, model, fit)
    mask = score.abs().ge(float(fit["score_threshold"]))
    selected = data.loc[mask].copy()
    selected["model_id"] = model["model_id"]
    selected["latency_profile_id"] = profile["profile_id"]
    selected["score"] = score.loc[mask]
    selected["dry_side"] = np.sign(selected["score"]).replace(0, np.nan).fillna(0).astype(int)
    selected["gross_return_bps_proxy"] = selected["dry_side"] * clean_numeric(selected["future_mid_return_bps_next_bucket"], 10_000.0)
    selected["cost_bound_bps"] = profile_cost_bps(selected, profile)
    selected["net_return_bps_after_cost_proxy"] = selected["gross_return_bps_proxy"] - selected["cost_bound_bps"]
    shuffled = pd.to_numeric(selected["future_mid_return_bps_next_bucket"], errors="coerce").to_numpy(copy=True)
    rng.shuffle(shuffled)
    selected["shuffled_time_net_bps_proxy"] = selected["dry_side"].to_numpy() * shuffled - selected["cost_bound_bps"].to_numpy()
    selected["net_edge_over_shuffled_time_bps"] = selected["net_return_bps_after_cost_proxy"] - selected["shuffled_time_net_bps_proxy"]
    selected["test_rows_used"] = 0
    selected["promotion_allowed"] = 0
    return selected


def summarize_events(events: pd.DataFrame, denominator_rows: int, split_bucket: str) -> dict[str, Any]:
    return {
        "model_id": events["model_id"].iloc[0] if len(events) else "",
        "latency_profile_id": events["latency_profile_id"].iloc[0] if len(events) else "",
        "split_bucket": split_bucket,
        "decision_events": int(len(events)),
        "decision_rate": float(len(events) / denominator_rows) if denominator_rows else 0.0,
        "dates_with_events": int(events["trade_date"].nunique()) if len(events) else 0,
        "symbols_with_events": int(events["symbol"].nunique()) if len(events) else 0,
        "net_return_bps_after_cost_proxy_mean": float(events["net_return_bps_after_cost_proxy"].mean()) if len(events) else np.nan,
        "net_edge_over_shuffled_time_bps_mean": float(events["net_edge_over_shuffled_time_bps"].mean()) if len(events) else np.nan,
        "net_positive_event_fraction": float((events["net_return_bps_after_cost_proxy"] > 0).mean()) if len(events) else np.nan,
        "test_rows_used": 0,
        "promotion_allowed": 0,
    }


def summarize_by_date_symbol(events: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if events.empty:
        return pd.DataFrame(), pd.DataFrame()
    by_date = (
        events.groupby(["model_id", "latency_profile_id", "split_role", "trade_date"], as_index=False)
        .agg(
            decision_events=("bucket_ms", "count"),
            symbols=("symbol", "nunique"),
            net_return_bps_after_cost_proxy_mean=("net_return_bps_after_cost_proxy", "mean"),
            net_edge_over_shuffled_time_bps_mean=("net_edge_over_shuffled_time_bps", "mean"),
        )
    )
    by_date["net_positive_group"] = (by_date["net_return_bps_after_cost_proxy_mean"] > 0).astype(int)
    by_date["beats_shuffled_time_group"] = (by_date["net_edge_over_shuffled_time_bps_mean"] > 0).astype(int)
    by_symbol = (
        events.groupby(["model_id", "latency_profile_id", "symbol"], as_index=False)
        .agg(
            decision_events=("bucket_ms", "count"),
            dates=("trade_date", "nunique"),
            net_return_bps_after_cost_proxy_mean=("net_return_bps_after_cost_proxy", "mean"),
            net_edge_over_shuffled_time_bps_mean=("net_edge_over_shuffled_time_bps", "mean"),
        )
    )
    by_symbol["net_positive_group"] = (by_symbol["net_return_bps_after_cost_proxy_mean"] > 0).astype(int)
    return by_date, by_symbol


def run_search(frame: pd.DataFrame, models: pd.DataFrame, profiles: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(RANDOM_SEED)
    train = frame.loc[frame["split_role"].astype(str).eq("train")].copy()
    validation = frame.loc[frame["split_role"].astype(str).eq("validation")].copy()
    extension = frame.loc[frame["split_role"].astype(str).eq("unassigned")].copy()
    evaluation = frame.loc[frame["split_role"].astype(str).isin(EVALUATION_ROLES)].copy()
    fit_rows = [fit_model(train, pd.Series(model)) for model in models.to_dict("records")]
    fits = pd.DataFrame(fit_rows)
    train_summary_rows: list[dict[str, Any]] = []
    selected_rows: list[dict[str, Any]] = []
    model_lookup = models.set_index("model_id")
    fit_lookup = fits.set_index("model_id")
    for model_id in fits["model_id"].astype(str).tolist():
        model = model_lookup.loc[model_id].copy()
        model["model_id"] = model_id
        fit = fit_lookup.loc[model_id]
        prof_summaries: list[dict[str, Any]] = []
        for profile in profiles.to_dict("records"):
            train_filtered = filtered_frame(train, model)
            events = selected_events(train, model, fit, pd.Series(profile), rng)
            summary = summarize_events(events, len(train_filtered), "train")
            summary["model_id"] = model_id
            summary["latency_profile_id"] = profile["profile_id"]
            train_summary_rows.append(summary)
            prof_summaries.append(summary)
        prof_frame = pd.DataFrame(prof_summaries)
        if (
            not prof_frame.empty
            and prof_frame["decision_events"].min() >= 100
            and prof_frame["decision_rate"].max() <= float(model["max_decision_rate"])
            and prof_frame["net_return_bps_after_cost_proxy_mean"].min() > 0
            and prof_frame["net_edge_over_shuffled_time_bps_mean"].min() > 0
        ):
            selected_rows.append(
                {
                    "model_id": model_id,
                    "min_train_net_bps": float(prof_frame["net_return_bps_after_cost_proxy_mean"].min()),
                    "min_train_edge_bps": float(prof_frame["net_edge_over_shuffled_time_bps_mean"].min()),
                    "max_train_decision_rate": float(prof_frame["decision_rate"].max()),
                    "selected_by_phase196_train_only": 1,
                    "validation_used_for_selection": 0,
                    "extension_used_for_selection": 0,
                    "test_used_for_selection": 0,
                }
            )
    train_summary = pd.DataFrame(train_summary_rows)
    selected = pd.DataFrame(selected_rows).sort_values(["min_train_net_bps", "min_train_edge_bps"], ascending=False).head(24) if selected_rows else pd.DataFrame()
    if not selected.empty:
        selected = selected.merge(models, on="model_id", how="left").merge(fits, on="model_id", how="left")
    eval_rows: list[dict[str, Any]] = []
    eval_event_frames: list[pd.DataFrame] = []
    for row in selected.to_dict("records"):
        model = pd.Series(row)
        fit = pd.Series(row)
        for profile in profiles.to_dict("records"):
            profile_s = pd.Series(profile)
            val_filtered = filtered_frame(validation, model)
            ext_filtered = filtered_frame(extension, model)
            val_events = selected_events(validation, model, fit, profile_s, rng)
            ext_events = selected_events(extension, model, fit, profile_s, rng)
            vs = summarize_events(val_events, len(val_filtered), "validation")
            es = summarize_events(ext_events, len(ext_filtered), "validation_extension")
            vs["model_id"] = row["model_id"]
            es["model_id"] = row["model_id"]
            vs["latency_profile_id"] = profile["profile_id"]
            es["latency_profile_id"] = profile["profile_id"]
            eval_rows.extend([vs, es])
            eval_event_frames.extend([val_events, ext_events])
    evaluation_summary = pd.DataFrame(eval_rows)
    event_audit = pd.concat(eval_event_frames, ignore_index=True) if eval_event_frames else pd.DataFrame()
    by_date, by_symbol = summarize_by_date_symbol(event_audit)
    return fits, train_summary, selected, evaluation_summary, by_date, by_symbol


def model_decisions(selected: pd.DataFrame, evaluation: pd.DataFrame, by_date: pd.DataFrame, by_symbol: pd.DataFrame) -> pd.DataFrame:
    if selected.empty or evaluation.empty or by_date.empty or by_symbol.empty:
        return pd.DataFrame()
    selected_lookup = selected.set_index("model_id")
    rows: list[dict[str, Any]] = []
    for model_id in selected["model_id"].astype(str).tolist():
        eval_rows = evaluation.loc[evaluation["model_id"].astype(str).eq(model_id)]
        date_rows = by_date.loc[by_date["model_id"].astype(str).eq(model_id)]
        symbol_rows = by_symbol.loc[by_symbol["model_id"].astype(str).eq(model_id)]
        min_validation_net = float(eval_rows.loc[eval_rows["split_bucket"].eq("validation"), "net_return_bps_after_cost_proxy_mean"].min())
        min_extension_net = float(eval_rows.loc[eval_rows["split_bucket"].eq("validation_extension"), "net_return_bps_after_cost_proxy_mean"].min())
        date_positive_fraction = float(date_rows["net_positive_group"].mean()) if not date_rows.empty else 0.0
        date_control_fraction = float(date_rows["beats_shuffled_time_group"].mean()) if not date_rows.empty else 0.0
        symbol_positive_fraction = float(symbol_rows["net_positive_group"].mean()) if not symbol_rows.empty else 0.0
        gate_pass = int(min_validation_net > 0 and min_extension_net > 0 and date_positive_fraction >= 1.0 and date_control_fraction >= 1.0 and symbol_positive_fraction >= 0.25)
        row = selected_lookup.loc[model_id].to_dict()
        rows.append(
            {
                "model_id": model_id,
                "family": row.get("family", ""),
                "horizon_scope": row.get("horizon_scope", ""),
                "side_mode": row.get("side_mode", ""),
                "min_train_net_bps": row.get("min_train_net_bps", np.nan),
                "min_validation_net_bps": min_validation_net,
                "min_extension_net_bps": min_extension_net,
                "date_positive_fraction": date_positive_fraction,
                "date_control_positive_fraction": date_control_fraction,
                "symbol_positive_fraction": symbol_positive_fraction,
                "validation_extension_gate_pass": gate_pass,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["validation_extension_gate_pass", "min_extension_net_bps", "date_positive_fraction", "symbol_positive_fraction"],
        ascending=False,
    )


def partition_use_audit(partition_use: pd.DataFrame) -> pd.DataFrame:
    out = partition_use.copy()
    out["used_in_phase196_train_fit"] = out["split_role"].astype(str).eq("train").astype(int)
    out["used_in_phase196_evaluation"] = out["split_role"].astype(str).isin(EVALUATION_ROLES).astype(int)
    out.loc[out["split_role"].astype(str).eq("test_untouched"), ["used_in_phase196_train_fit", "used_in_phase196_evaluation"]] = 0
    return out


def build_gates(phase195: pd.DataFrame, partition_use: pd.DataFrame, train_summary: pd.DataFrame, selected: pd.DataFrame, decisions: pd.DataFrame) -> pd.DataFrame:
    phase195_complete = as_int(metric_value(phase195, "phase195_redesign_search_complete", 0))
    test_used = int(partition_use.loc[partition_use["split_role"].astype(str).eq("test_untouched"), "used_in_phase196_evaluation"].sum()) if not partition_use.empty else 0
    passing = int(decisions["validation_extension_gate_pass"].astype(int).sum()) if not decisions.empty else 0
    train_fit_recorded = not train_summary.empty and "model_id" in train_summary.columns
    train_only_ok = bool(
        train_fit_recorded
        and (
            selected.empty
            or (
                selected["validation_used_for_selection"].astype(int).eq(0).all()
                and selected["extension_used_for_selection"].astype(int).eq(0).all()
                and selected["test_used_for_selection"].astype(int).eq(0).all()
            )
        )
    )
    extension_gate_recorded = bool(
        selected.empty
        or (
            not decisions.empty
            and {"date_positive_fraction", "symbol_positive_fraction", "validation_extension_gate_pass"}.issubset(decisions.columns)
        )
    )
    return pd.DataFrame(
        [
            {"gate_id": "P196_PHASE195_COMPLETE", "gate_pass": int(phase195_complete == 1), "evidence": f"phase195_redesign_search_complete={phase195_complete}", "severity": "hard"},
            {"gate_id": "P196_TRAIN_ONLY_FIT", "gate_pass": int(train_only_ok), "evidence": f"train_summary_rows={len(train_summary)}; selected_model_rows={len(selected)}", "severity": "hard"},
            {"gate_id": "P196_EVALUATION_EXCLUDES_TEST", "gate_pass": int(test_used == 0), "evidence": f"test_partitions_used={test_used}", "severity": "hard"},
            {"gate_id": "P196_EXTENSION_BREADTH_GATES_APPLIED", "gate_pass": int(extension_gate_recorded), "evidence": f"selected_model_rows={len(selected)}; decision_rows={len(decisions)}", "severity": "hard"},
            {"gate_id": "P196_PASSING_MODEL_RECORDED", "gate_pass": int(passing >= 0), "evidence": f"passing_models={passing}", "severity": "hard"},
            {"gate_id": "P196_NO_TEST_REPLAY_OR_PROMOTION", "gate_pass": int(decisions.empty or (decisions["test_replay_allowed_next"].astype(int).eq(0).all() and decisions["promotion_allowed"].astype(int).eq(0).all())), "evidence": "test_replay_allowed_next=0; promotion_allowed=0", "severity": "hard"},
        ]
    )


def build_acceptance(models: pd.DataFrame, selected: pd.DataFrame, decisions: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates.loc[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(int).sum()) if not hard.empty else 0
    passing = decisions.loc[decisions["validation_extension_gate_pass"].astype(int).eq(1)] if not decisions.empty else pd.DataFrame()
    best = decisions.iloc[0] if not decisions.empty else {}
    next_action = "precommit_phase197_expanded_model_contract_no_test" if not passing.empty else "expand_non_receive_flow_features_or_pause_this_branch_no_test"
    return pd.DataFrame(
        [
            ("phase196_model_grid_rows", int(len(models)), "Expanded feature/model rows"),
            ("phase196_train_selected_model_rows", int(len(selected)), "Train-selected model rows"),
            ("phase196_model_decision_rows", int(len(decisions)), "Model decision rows"),
            ("phase196_passing_extension_gate_models", int(len(passing)), "Models passing extension gates"),
            ("phase196_best_model_id", best.get("model_id", ""), "Top model by extension screen"),
            ("phase196_best_min_extension_net_bps", best.get("min_extension_net_bps", ""), "Best model minimum extension net bps"),
            ("phase196_best_date_positive_fraction", best.get("date_positive_fraction", ""), "Best model date-positive fraction"),
            ("phase196_best_symbol_positive_fraction", best.get("symbol_positive_fraction", ""), "Best model symbol-positive fraction"),
            ("phase196_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase196_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase196_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase196_expanded_model_search_complete", int(len(hard) > 0 and hard_pass == len(hard)), "1 means Phase196 completed"),
            ("phase196_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase196_promotion_allowed", 0, "No promotion opened"),
            ("phase196_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase196_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase196_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase196 Expanded Feature Model Search",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase196 expands from threshold grids to train-fitted linear feature families.",
        "It preserves the Phase195 discipline: train-only fitting, validation-extension rejection, no untouched test replay, no promotion, and no paper/live acceptance.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase196_expanded_feature_model_search_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase196(phase176_dir: Path, phase180_dir: Path, phase181_dir: Path, phase195_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase195 = read_csv(phase195_dir / "phase195_receive_flow_redesign_candidate_acceptance_summary.csv")
    feature_inventory = read_csv(phase176_dir / "phase176_feature_partition_inventory.csv")
    label_inventory = read_csv(phase181_dir / "phase181_label_partition_inventory.csv")
    latency_profiles = read_csv(phase180_dir / "phase180_latency_slippage_profile_catalog.csv")
    profiles = latency_profiles.loc[latency_profiles["profile_id"].astype(str).isin(ALLOWED_PROFILES)].copy()
    frame, partition_use = build_model_frame(feature_inventory, label_inventory)
    frame = enrich_features(frame)
    partition_use = partition_use_audit(partition_use)
    models = model_grid()
    fits, train_summary, selected, evaluation, by_date, by_symbol = run_search(frame, models, profiles)
    decisions = model_decisions(selected, evaluation, by_date, by_symbol)
    gates = build_gates(phase195, partition_use, train_summary, selected, decisions)
    acceptance = build_acceptance(models, selected, decisions, gates)

    models.to_csv(output_dir / "phase196_expanded_model_grid.csv", index=False)
    partition_use.to_csv(output_dir / "phase196_partition_use_audit.csv", index=False)
    fits.to_csv(output_dir / "phase196_train_model_fits.csv", index=False)
    train_summary.to_csv(output_dir / "phase196_train_model_summary.csv", index=False)
    selected.to_csv(output_dir / "phase196_train_selected_models.csv", index=False)
    evaluation.to_csv(output_dir / "phase196_validation_extension_summary.csv", index=False)
    by_date.to_csv(output_dir / "phase196_validation_extension_by_date.csv", index=False)
    by_symbol.to_csv(output_dir / "phase196_validation_extension_by_symbol.csv", index=False)
    decisions.to_csv(output_dir / "phase196_expanded_model_decision.csv", index=False)
    gates.to_csv(output_dir / "phase196_expanded_feature_model_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase196_expanded_feature_model_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Top Model Decisions": decisions.head(24),
            "Train-selected Models": selected,
            "Validation Extension Summary": evaluation.head(96),
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase196_expanded_feature_model_search_no_test",
        **reproducibility_fields(
            artifact_id="phase196_expanded_feature_model_search",
            generated_utc=generated,
            inputs={
                "phase176_feature_inventory": str(phase176_dir / "phase176_feature_partition_inventory.csv"),
                "phase181_label_inventory": str(phase181_dir / "phase181_label_partition_inventory.csv"),
                "phase180_latency_profiles": str(phase180_dir / "phase180_latency_slippage_profile_catalog.csv"),
                "phase195_acceptance": str(phase195_dir / "phase195_receive_flow_redesign_candidate_acceptance_summary.csv"),
            },
            parameters={
                "selection_split": "train",
                "evaluation_roles": ";".join(sorted(EVALUATION_ROLES)),
                "excluded_role": "test_untouched",
                "model_class": "train_fitted_linear_feature_family_scores",
                "required_date_positive_fraction": 1.0,
                "required_symbol_positive_fraction": 0.25,
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "model_grid": str(output_dir / "phase196_expanded_model_grid.csv"),
                "partition_use": str(output_dir / "phase196_partition_use_audit.csv"),
                "fits": str(output_dir / "phase196_train_model_fits.csv"),
                "train_summary": str(output_dir / "phase196_train_model_summary.csv"),
                "selected": str(output_dir / "phase196_train_selected_models.csv"),
                "evaluation": str(output_dir / "phase196_validation_extension_summary.csv"),
                "by_date": str(output_dir / "phase196_validation_extension_by_date.csv"),
                "by_symbol": str(output_dir / "phase196_validation_extension_by_symbol.csv"),
                "decisions": str(output_dir / "phase196_expanded_model_decision.csv"),
                "gate_evaluation": str(output_dir / "phase196_expanded_feature_model_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase196_expanded_feature_model_acceptance_summary.csv"),
                "report": str(output_dir / "phase196_expanded_feature_model_search_report.md"),
            },
            random_seed=str(RANDOM_SEED),
            scenario_ids="phase196_expanded_feature_model_search_no_test",
            cost_model_version="phase180_retail_default_and_stressed_profiles",
            latency_model_version="phase180_retail_default_and_stressed_profiles",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase196_expanded_feature_model_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase176-dir", type=Path, default=DEFAULT_PHASE176_DIR)
    parser.add_argument("--phase180-dir", type=Path, default=DEFAULT_PHASE180_DIR)
    parser.add_argument("--phase181-dir", type=Path, default=DEFAULT_PHASE181_DIR)
    parser.add_argument("--phase195-dir", type=Path, default=DEFAULT_PHASE195_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase196(args.phase176_dir, args.phase180_dir, args.phase181_dir, args.phase195_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
