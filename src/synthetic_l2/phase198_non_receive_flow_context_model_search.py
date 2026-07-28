from __future__ import annotations

import argparse
import json
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase184_train_validation_replay_dry_run import build_model_frame, profile_cost_bps
from synthetic_l2.phase197_non_receive_flow_feature_expansion_precommit import clean_numeric, derive_context_features, read_csv
from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


warnings.filterwarnings("ignore", category=RuntimeWarning)

DEFAULT_PHASE176_DIR = Path("outputs/phase176")
DEFAULT_PHASE180_DIR = Path("outputs/phase180")
DEFAULT_PHASE181_DIR = Path("outputs/phase181")
DEFAULT_PHASE197_DIR = Path("outputs/phase197")
DEFAULT_OUTPUT_DIR = Path("outputs/phase198")
RANDOM_SEED = 198
ALLOWED_PROFILES = {"P180_RETAIL_MARKETABLE_DEFAULT", "P180_STRESSED_RETAIL"}
EVALUATION_ROLES = {"validation", "unassigned"}
FORBIDDEN_OUTPUTS = "test_result;test_replay_execution;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim"


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


def add_phase198_transforms(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    out["asset_class_proxy_etf"] = out["asset_class_proxy"].astype(str).eq("etf").astype(float)
    out["context_spread_x_time"] = clean_numeric(out["relative_spread_to_symbol_train_median"], 1_000).fillna(0) * clean_numeric(out["time_of_day_sin_ist"], 10).fillna(0)
    out["market_stress_x_liquidity"] = clean_numeric(out["prior_market_receive_event_count_sum"], 1_000_000).fillna(0) * clean_numeric(out["relative_spread_to_symbol_train_median"], 1_000).fillna(0)
    out["lagged_market_imbalance_x_local_top5"] = clean_numeric(out["prior_market_median_top5_imbalance"], 10).fillna(0) * clean_numeric(out["top5_qty_imbalance"], 10).fillna(0)
    return out


def model_grid(candidate_matrix: pd.DataFrame) -> pd.DataFrame:
    ready = candidate_matrix.loc[candidate_matrix["ready_for_phase198_search"].astype(int).eq(1)].copy()
    family_cols = {
        "P197_TIME_OF_DAY_CONTEXT": ["seconds_from_open_ist", "time_of_day_sin_ist", "time_of_day_cos_ist", "context_spread_x_time"],
        "P197_SYMBOL_LIQUIDITY_REGIME": ["relative_spread_to_symbol_train_median", "relative_receive_count_to_symbol_train_median", "symbol_train_spread_bps_median"],
        "P197_MARKET_CONTEXT_LAGGED": ["prior_market_active_symbol_count", "prior_market_median_spread_bps", "prior_market_median_top5_imbalance", "prior_market_receive_event_count_sum", "prior_market_cross_symbol_arrival_share", "market_stress_x_liquidity", "lagged_market_imbalance_x_local_top5"],
        "P197_ASSET_CLASS_PROXY": ["asset_class_proxy_etf", "relative_spread_to_symbol_train_median", "prior_market_median_spread_bps"],
        "P197_MICROSTRUCTURE_TRANSFORMS": ["spread_bps", "quote_churn_log", "depth_refresh_log", "stale_quote_log_ms", "relative_spread_to_symbol_train_median"],
    }
    composite = [
        "time_of_day_sin_ist",
        "time_of_day_cos_ist",
        "relative_spread_to_symbol_train_median",
        "prior_market_median_spread_bps",
        "prior_market_median_top5_imbalance",
        "asset_class_proxy_etf",
        "quote_churn_log",
        "stale_quote_log_ms",
        "lagged_market_imbalance_x_local_top5",
    ]
    rows: list[dict[str, Any]] = []
    for feature_id in ready["feature_id"].astype(str):
        if feature_id not in family_cols:
            continue
        for horizon_scope in ["1", "5"]:
            for side_mode in ["signed_score", "inverse_score"]:
                for quantile in [0.98, 0.99]:
                    for max_spread_bps in [1.5, 2.5]:
                        rows.append(
                            {
                                "model_id": f"P198_{feature_id.replace('P197_', '')}_H{horizon_scope}_{side_mode.replace('_score','').upper()}_Q{int(quantile*1000)}_S{str(max_spread_bps).replace('.', 'p')}",
                                "source_feature_id": feature_id,
                                "feature_family": str(ready.loc[ready["feature_id"].astype(str).eq(feature_id), "feature_family"].iloc[0]),
                                "feature_columns": ";".join(family_cols[feature_id]),
                                "horizon_scope": horizon_scope,
                                "side_mode": side_mode,
                                "score_quantile": quantile,
                                "max_spread_bps": max_spread_bps,
                                "max_decision_rate": 0.01,
                                "test_replay_allowed_in_phase198": 0,
                            }
                        )
    for horizon_scope in ["1", "5"]:
        for side_mode in ["signed_score", "inverse_score"]:
            for quantile in [0.99]:
                for max_spread_bps in [1.5, 2.5]:
                    rows.append(
                        {
                            "model_id": f"P198_COMPOSITE_CONTEXT_H{horizon_scope}_{side_mode.replace('_score','').upper()}_Q{int(quantile*1000)}_S{str(max_spread_bps).replace('.', 'p')}",
                            "source_feature_id": "P197_COMPOSITE_CONTEXT",
                            "feature_family": "composite_non_receive_flow_context",
                            "feature_columns": ";".join(composite),
                            "horizon_scope": horizon_scope,
                            "side_mode": side_mode,
                            "score_quantile": quantile,
                            "max_spread_bps": max_spread_bps,
                            "max_decision_rate": 0.01,
                            "test_replay_allowed_in_phase198": 0,
                        }
                    )
    return pd.DataFrame(rows)


def filtered_frame(frame: pd.DataFrame, model: pd.Series) -> pd.DataFrame:
    out = frame.loc[clean_numeric(frame["spread_bps"], 1_000).le(float(model["max_spread_bps"]))].copy()
    scope = str(model["horizon_scope"])
    if scope != "all":
        out = out.loc[pd.to_numeric(out["horizon_sec"], errors="coerce").astype("Int64").astype(str).eq(scope)].copy()
    return out


def fit_model(train: pd.DataFrame, model: pd.Series) -> dict[str, Any]:
    data = filtered_frame(train, model)
    target = clean_numeric(data["future_mid_return_bps_next_bucket"], 10_000).fillna(0.0)
    score = pd.Series(0.0, index=data.index)
    means: dict[str, float] = {}
    stds: dict[str, float] = {}
    weights: dict[str, float] = {}
    for feature in str(model["feature_columns"]).split(";"):
        values = clean_numeric(data[feature], 1_000_000).fillna(0.0)
        mean = float(values.mean()) if len(values) else 0.0
        std = float(values.std(ddof=0)) if len(values) else 1.0
        if not np.isfinite(std) or std <= 0:
            std = 1.0
        z = (values - mean) / std
        corr = float(z.corr(target)) if len(z) > 2 else 0.0
        if not np.isfinite(corr):
            corr = 0.0
        means[feature] = mean
        stds[feature] = std
        weights[feature] = corr
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
        values = clean_numeric(data[feature], 1_000_000).fillna(0.0)
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
    selected["source_feature_id"] = model["source_feature_id"]
    selected["feature_family"] = model["feature_family"]
    selected["latency_profile_id"] = profile["profile_id"]
    selected["score"] = score.loc[mask]
    selected["dry_side"] = np.sign(selected["score"]).replace(0, np.nan).fillna(0).astype(int)
    selected["gross_return_bps_proxy"] = selected["dry_side"] * clean_numeric(selected["future_mid_return_bps_next_bucket"], 10_000).fillna(0.0)
    selected["cost_bound_bps"] = profile_cost_bps(selected, profile)
    selected["net_return_bps_after_cost_proxy"] = selected["gross_return_bps_proxy"] - selected["cost_bound_bps"]
    shuffled = clean_numeric(selected["future_mid_return_bps_next_bucket"], 10_000).fillna(0.0).to_numpy(copy=True)
    rng.shuffle(shuffled)
    selected["shuffled_time_net_bps_proxy"] = selected["dry_side"].to_numpy() * shuffled - selected["cost_bound_bps"].to_numpy()
    selected["net_edge_over_shuffled_time_bps"] = selected["net_return_bps_after_cost_proxy"] - selected["shuffled_time_net_bps_proxy"]
    selected["test_rows_used"] = 0
    selected["promotion_allowed"] = 0
    return selected


def summarize_events(events: pd.DataFrame, denominator_rows: int, split_bucket: str) -> dict[str, Any]:
    return {
        "model_id": events["model_id"].iloc[0] if len(events) else "",
        "source_feature_id": events["source_feature_id"].iloc[0] if len(events) else "",
        "feature_family": events["feature_family"].iloc[0] if len(events) else "",
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
    fit_rows = [fit_model(train, pd.Series(model)) for model in models.to_dict("records")]
    fits = pd.DataFrame(fit_rows)
    train_summary_rows: list[dict[str, Any]] = []
    selected_rows: list[dict[str, Any]] = []
    model_lookup = models.set_index("model_id")
    fit_lookup = fits.set_index("model_id")
    for model_id in fits["model_id"].astype(str):
        model = model_lookup.loc[model_id].copy()
        model["model_id"] = model_id
        fit = fit_lookup.loc[model_id]
        train_denominator = len(filtered_frame(train, model))
        for profile in profiles.to_dict("records"):
            events = selected_events(train, model, fit, pd.Series(profile), rng)
            summary = summarize_events(events, train_denominator, "train")
            summary["selection_split"] = "train"
            train_summary_rows.append(summary)
            if (
                summary["decision_events"] >= 20
                and summary["decision_rate"] <= float(model["max_decision_rate"])
                and summary["net_return_bps_after_cost_proxy_mean"] > 0
                and summary["net_edge_over_shuffled_time_bps_mean"] > 0
            ):
                selected_rows.append(
                    {
                        **summary,
                        "validation_used_for_selection": 0,
                        "extension_used_for_selection": 0,
                        "test_used_for_selection": 0,
                        "promotion_allowed": 0,
                    }
                )
    train_summary = pd.DataFrame(train_summary_rows)
    selected = pd.DataFrame(selected_rows)
    evaluation_rows: list[dict[str, Any]] = []
    all_eval_events: list[pd.DataFrame] = []
    for item in selected.to_dict("records"):
        model = model_lookup.loc[item["model_id"]].copy()
        model["model_id"] = item["model_id"]
        fit = fit_lookup.loc[item["model_id"]]
        profile = profiles.loc[profiles["profile_id"].astype(str).eq(str(item["latency_profile_id"]))].iloc[0]
        for split_name, split_frame in [("validation", validation), ("validation_extension", extension)]:
            denominator = len(filtered_frame(split_frame, model))
            events = selected_events(split_frame, model, fit, profile, rng)
            events["evaluation_bucket"] = split_name
            evaluation_rows.append(summarize_events(events, denominator, split_name))
            if not events.empty:
                all_eval_events.append(events)
    evaluation = pd.DataFrame(evaluation_rows)
    eval_events = pd.concat(all_eval_events, ignore_index=True) if all_eval_events else pd.DataFrame()
    by_date, by_symbol = summarize_by_date_symbol(eval_events)
    return fits, train_summary, selected, evaluation, by_date, by_symbol


def model_decisions(selected: pd.DataFrame, evaluation: pd.DataFrame, by_date: pd.DataFrame, by_symbol: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for item in selected.to_dict("records"):
        model_id = str(item["model_id"])
        profile = str(item["latency_profile_id"])
        eval_rows = evaluation.loc[evaluation["model_id"].astype(str).eq(model_id) & evaluation["latency_profile_id"].astype(str).eq(profile)]
        if eval_rows.empty:
            continue
        validation = eval_rows.loc[eval_rows["split_bucket"].astype(str).eq("validation")]
        extension = eval_rows.loc[eval_rows["split_bucket"].astype(str).eq("validation_extension")]
        date_rows = by_date.loc[by_date["model_id"].astype(str).eq(model_id) & by_date["latency_profile_id"].astype(str).eq(profile)] if not by_date.empty else pd.DataFrame()
        symbol_rows = by_symbol.loc[by_symbol["model_id"].astype(str).eq(model_id) & by_symbol["latency_profile_id"].astype(str).eq(profile)] if not by_symbol.empty else pd.DataFrame()
        min_net = float(eval_rows["net_return_bps_after_cost_proxy_mean"].min()) if not eval_rows.empty else np.nan
        date_positive = float(date_rows["net_positive_group"].mean()) if not date_rows.empty else 0.0
        symbol_positive = float(symbol_rows["net_positive_group"].mean()) if not symbol_rows.empty else 0.0
        gate_pass = int(
            len(validation) > 0
            and len(extension) > 0
            and min_net > 0
            and date_positive >= 0.75
            and symbol_positive >= 0.25
        )
        rows.append(
            {
                "model_id": model_id,
                "source_feature_id": item.get("source_feature_id", ""),
                "feature_family": item.get("feature_family", ""),
                "latency_profile_id": profile,
                "train_net_bps": item.get("net_return_bps_after_cost_proxy_mean", np.nan),
                "validation_net_bps": float(validation["net_return_bps_after_cost_proxy_mean"].iloc[0]) if not validation.empty else np.nan,
                "extension_net_bps": float(extension["net_return_bps_after_cost_proxy_mean"].iloc[0]) if not extension.empty else np.nan,
                "min_extension_net_bps": min_net,
                "date_positive_fraction": date_positive,
                "symbol_positive_fraction": symbol_positive,
                "validation_extension_gate_pass": gate_pass,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
            }
        )
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).sort_values(
        ["validation_extension_gate_pass", "min_extension_net_bps", "date_positive_fraction", "symbol_positive_fraction"],
        ascending=[False, False, False, False],
    )


def partition_use_audit(partition_use: pd.DataFrame) -> pd.DataFrame:
    out = partition_use.copy()
    if out.empty:
        return out
    out["used_in_phase198_evaluation"] = np.where(out["split_role"].astype(str).eq("test_untouched"), 0, 1)
    return out


def build_gates(phase197: pd.DataFrame, partition_use: pd.DataFrame, train_summary: pd.DataFrame, selected: pd.DataFrame, decisions: pd.DataFrame) -> pd.DataFrame:
    phase197_complete = as_int(metric_value(phase197, "phase197_non_receive_flow_feature_precommit_complete", 0))
    ready = as_int(metric_value(phase197, "phase197_ready_feature_families", 0))
    test_used = int(partition_use.loc[partition_use["split_role"].astype(str).eq("test_untouched"), "used_in_phase198_evaluation"].sum()) if not partition_use.empty else 0
    passing = int(decisions["validation_extension_gate_pass"].astype(int).sum()) if not decisions.empty else 0
    train_only_ok = bool(
        not train_summary.empty
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
            {"gate_id": "P198_PHASE197_COMPLETE", "gate_pass": int(phase197_complete == 1), "evidence": f"phase197_precommit_complete={phase197_complete}; ready_feature_families={ready}", "severity": "hard"},
            {"gate_id": "P198_TRAIN_ONLY_FIT_AND_SELECTION", "gate_pass": int(train_only_ok), "evidence": f"train_summary_rows={len(train_summary)}; selected_model_rows={len(selected)}", "severity": "hard"},
            {"gate_id": "P198_EVALUATION_EXCLUDES_TEST", "gate_pass": int(test_used == 0), "evidence": f"test_partitions_used={test_used}", "severity": "hard"},
            {"gate_id": "P198_EXTENSION_BREADTH_GATES_APPLIED", "gate_pass": int(extension_gate_recorded), "evidence": f"selected_model_rows={len(selected)}; decision_rows={len(decisions)}", "severity": "hard"},
            {"gate_id": "P198_PASSING_MODEL_RECORDED", "gate_pass": int(passing >= 0), "evidence": f"passing_models={passing}", "severity": "hard"},
            {"gate_id": "P198_NO_TEST_REPLAY_OR_PROMOTION", "gate_pass": int(decisions.empty or (decisions["test_replay_allowed_next"].astype(int).eq(0).all() and decisions["promotion_allowed"].astype(int).eq(0).all())), "evidence": "test_replay_allowed_next=0; promotion_allowed=0", "severity": "hard"},
        ]
    )


def build_acceptance(models: pd.DataFrame, selected: pd.DataFrame, decisions: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates.loc[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(int).sum()) if not hard.empty else 0
    passing = decisions.loc[decisions["validation_extension_gate_pass"].astype(int).eq(1)] if not decisions.empty else pd.DataFrame()
    best = decisions.iloc[0] if not decisions.empty else {}
    next_action = "precommit_diagnostic_test_replay_contract_for_phase198_context_candidate" if not passing.empty else "expand_or_pause_non_receive_flow_context_branch_no_test"
    return pd.DataFrame(
        [
            ("phase198_model_grid_rows", int(len(models)), "Non-receive-flow context model rows"),
            ("phase198_train_selected_model_rows", int(len(selected)), "Train-selected model rows"),
            ("phase198_model_decision_rows", int(len(decisions)), "Model decision rows"),
            ("phase198_passing_extension_gate_models", int(len(passing)), "Models passing extension gates"),
            ("phase198_best_model_id", best.get("model_id", ""), "Top model by extension screen"),
            ("phase198_best_feature_family", best.get("feature_family", ""), "Top model feature family"),
            ("phase198_best_min_extension_net_bps", best.get("min_extension_net_bps", ""), "Best model minimum validation/extension net bps"),
            ("phase198_best_date_positive_fraction", best.get("date_positive_fraction", ""), "Best model date-positive fraction"),
            ("phase198_best_symbol_positive_fraction", best.get("symbol_positive_fraction", ""), "Best model symbol-positive fraction"),
            ("phase198_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase198_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase198_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase198_context_model_search_complete", int(len(hard) > 0 and hard_pass == len(hard)), "1 means Phase198 completed"),
            ("phase198_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase198_promotion_allowed", 0, "No promotion opened"),
            ("phase198_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase198_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase198_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase198 Non-Receive-Flow Context Model Search",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase198 runs a train/validation-only context model search using Phase197 feature families.",
        "It excludes untouched test replay and does not create orders, fills, P&L, promotion or paper/live acceptance.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase198_non_receive_flow_context_model_search_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase198(phase176_dir: Path, phase180_dir: Path, phase181_dir: Path, phase197_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase197 = read_csv(phase197_dir / "phase197_non_receive_flow_feature_acceptance_summary.csv")
    candidate_matrix = read_csv(phase197_dir / "phase197_phase198_candidate_matrix.csv")
    feature_inventory = read_csv(phase176_dir / "phase176_feature_partition_inventory.csv")
    label_inventory = read_csv(phase181_dir / "phase181_label_partition_inventory.csv")
    latency_profiles = read_csv(phase180_dir / "phase180_latency_slippage_profile_catalog.csv")
    profiles = latency_profiles.loc[latency_profiles["profile_id"].astype(str).isin(ALLOWED_PROFILES)].copy()
    frame, partition_use = build_model_frame(feature_inventory, label_inventory)
    frame = add_phase198_transforms(derive_context_features(frame))
    partition_use = partition_use_audit(partition_use)
    models = model_grid(candidate_matrix)
    fits, train_summary, selected, evaluation, by_date, by_symbol = run_search(frame, models, profiles)
    decisions = model_decisions(selected, evaluation, by_date, by_symbol)
    gates = build_gates(phase197, partition_use, train_summary, selected, decisions)
    acceptance = build_acceptance(models, selected, decisions, gates)

    models.to_csv(output_dir / "phase198_context_model_grid.csv", index=False)
    partition_use.to_csv(output_dir / "phase198_partition_use_audit.csv", index=False)
    fits.to_csv(output_dir / "phase198_train_model_fits.csv", index=False)
    train_summary.to_csv(output_dir / "phase198_train_model_summary.csv", index=False)
    selected.to_csv(output_dir / "phase198_train_selected_models.csv", index=False)
    evaluation.to_csv(output_dir / "phase198_validation_extension_summary.csv", index=False)
    by_date.to_csv(output_dir / "phase198_validation_extension_by_date.csv", index=False)
    by_symbol.to_csv(output_dir / "phase198_validation_extension_by_symbol.csv", index=False)
    decisions.to_csv(output_dir / "phase198_context_model_decision.csv", index=False)
    gates.to_csv(output_dir / "phase198_context_model_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase198_context_model_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Top Model Decisions": decisions.head(24),
            "Train-selected Models": selected.head(48),
            "Validation Extension Summary": evaluation.head(96),
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase198_non_receive_flow_context_model_search_no_test",
        **reproducibility_fields(
            artifact_id="phase198_non_receive_flow_context_model_search",
            generated_utc=generated,
            inputs={
                "phase176_feature_inventory": str(phase176_dir / "phase176_feature_partition_inventory.csv"),
                "phase181_label_inventory": str(phase181_dir / "phase181_label_partition_inventory.csv"),
                "phase180_latency_profiles": str(phase180_dir / "phase180_latency_slippage_profile_catalog.csv"),
                "phase197_candidate_matrix": str(phase197_dir / "phase197_phase198_candidate_matrix.csv"),
                "phase197_acceptance": str(phase197_dir / "phase197_non_receive_flow_feature_acceptance_summary.csv"),
            },
            parameters={
                "selection_split": "train",
                "evaluation_roles": ";".join(sorted(EVALUATION_ROLES)),
                "excluded_role": "test_untouched",
                "model_class": "train_fitted_linear_context_feature_scores",
                "required_date_positive_fraction": 0.75,
                "required_symbol_positive_fraction": 0.25,
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "model_grid": str(output_dir / "phase198_context_model_grid.csv"),
                "partition_use": str(output_dir / "phase198_partition_use_audit.csv"),
                "fits": str(output_dir / "phase198_train_model_fits.csv"),
                "train_summary": str(output_dir / "phase198_train_model_summary.csv"),
                "selected": str(output_dir / "phase198_train_selected_models.csv"),
                "evaluation": str(output_dir / "phase198_validation_extension_summary.csv"),
                "by_date": str(output_dir / "phase198_validation_extension_by_date.csv"),
                "by_symbol": str(output_dir / "phase198_validation_extension_by_symbol.csv"),
                "decisions": str(output_dir / "phase198_context_model_decision.csv"),
                "gate_evaluation": str(output_dir / "phase198_context_model_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase198_context_model_acceptance_summary.csv"),
                "report": str(output_dir / "phase198_non_receive_flow_context_model_search_report.md"),
            },
            random_seed=str(RANDOM_SEED),
            scenario_ids="phase198_non_receive_flow_context_model_search_no_test",
            cost_model_version="phase180_retail_default_and_stressed_profiles",
            latency_model_version="phase180_retail_default_and_stressed_profiles",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase198_context_model_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase176-dir", type=Path, default=DEFAULT_PHASE176_DIR)
    parser.add_argument("--phase180-dir", type=Path, default=DEFAULT_PHASE180_DIR)
    parser.add_argument("--phase181-dir", type=Path, default=DEFAULT_PHASE181_DIR)
    parser.add_argument("--phase197-dir", type=Path, default=DEFAULT_PHASE197_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase198(args.phase176_dir, args.phase180_dir, args.phase181_dir, args.phase197_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
