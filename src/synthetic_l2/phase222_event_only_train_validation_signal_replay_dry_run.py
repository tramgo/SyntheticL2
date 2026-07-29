from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase219_event_only_train_validation_model_fit_dry_run import (
    fit_ridge,
    transform_features,
)
from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE176_DIR = Path("outputs/phase176")
DEFAULT_PHASE180_DIR = Path("outputs/phase180")
DEFAULT_PHASE214_DIR = Path("outputs/phase214")
DEFAULT_PHASE218_DIR = Path("outputs/phase218")
DEFAULT_PHASE221_DIR = Path("outputs/phase221")
DEFAULT_OUTPUT_DIR = Path("outputs/phase222")
JOIN_KEYS = ["bucket_ms", "trade_date", "exchange", "symbol", "horizon_sec"]
RNG_SEED = 222
FORBIDDEN_OUTPUTS = "test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export"
NEXT_ACTION = "run_phase223_event_only_signal_replay_validation_interpretation_no_test"


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


def split_columns(value: Any) -> list[str]:
    return [c.strip() for c in str(value).split(";") if c.strip()]


def partition_key(row: dict[str, Any]) -> tuple[int, str, str, str]:
    return (as_int(row.get("horizon_sec", 0)), str(row.get("trade_date", "")), str(row.get("exchange", "")), str(row.get("symbol", "")))


def feature_columns_by_horizon(feature_contract: pd.DataFrame) -> dict[int, list[str]]:
    mapping: dict[int, set[str]] = {}
    if feature_contract.empty:
        return {}
    allowed = feature_contract[pd.to_numeric(feature_contract["eligible_for_phase219_fit_dry_run"], errors="coerce").fillna(0).astype(int).eq(1)] if "eligible_for_phase219_fit_dry_run" in feature_contract.columns else feature_contract
    for row in allowed.to_dict("records"):
        horizon = as_int(row.get("horizon_sec", 0))
        mapping.setdefault(horizon, set()).update(split_columns(row.get("required_columns", "")))
    return {horizon: sorted(cols) for horizon, cols in mapping.items()}


def load_event_only_matrices(feature_inventory: pd.DataFrame, label_inventory: pd.DataFrame, candidates: pd.DataFrame, feature_map: dict[int, list[str]]) -> tuple[dict[int, dict[str, pd.DataFrame]], pd.DataFrame]:
    horizons = sorted({as_int(v) for v in candidates["horizon_sec"].dropna().tolist()}) if not candidates.empty else []
    target_columns = sorted(set(candidates["target_label"].dropna().astype(str).tolist())) if not candidates.empty else []
    feature_paths = {partition_key(row): Path(str(row.get("parquet_file", ""))) for row in feature_inventory.to_dict("records")}
    usable_labels = label_inventory[
        label_inventory["split_role"].astype(str).isin(["train", "validation"])
        & pd.to_numeric(label_inventory["horizon_sec"], errors="coerce").fillna(-1).astype(int).isin(horizons)
    ] if not label_inventory.empty else pd.DataFrame()
    matrices: dict[int, dict[str, list[pd.DataFrame]]] = {}
    inventory_rows: list[dict[str, Any]] = []
    column_cache: dict[Path, list[str]] = {}
    market_cols = ["best_bid", "best_ask", "spread", "last_price"]
    for row in usable_labels.to_dict("records"):
        key = partition_key(row)
        horizon = key[0]
        split_role = str(row.get("split_role", ""))
        feature_path = feature_paths.get(key)
        label_path = Path(str(row.get("label_file", "")))
        feature_cols = feature_map.get(horizon, [])
        if feature_path is None or not feature_path.exists() or not label_path.exists() or not feature_cols:
            inventory_rows.append({**{"horizon_sec": horizon, "trade_date": key[1], "exchange": key[2], "symbol": key[3], "split_role": split_role}, "event_only_joined_rows": 0, "test_rows_used": 0})
            continue
        if feature_path not in column_cache:
            column_cache[feature_path] = pd.read_parquet(feature_path).columns.astype(str).tolist()
        if label_path not in column_cache:
            column_cache[label_path] = pd.read_parquet(label_path).columns.astype(str).tolist()
        feature_read_cols = [c for c in JOIN_KEYS + market_cols + feature_cols if c in column_cache[feature_path]]
        label_read_cols = [c for c in JOIN_KEYS + ["split_role", "event_surprise_bucket"] + target_columns if c in column_cache[label_path]]
        features = pd.read_parquet(feature_path, columns=feature_read_cols)
        labels = pd.read_parquet(label_path, columns=label_read_cols)
        labels = labels[pd.to_numeric(labels["event_surprise_bucket"], errors="coerce").fillna(0).astype(int).eq(1)]
        joined = features.merge(labels, on=JOIN_KEYS, how="inner")
        for col in feature_cols + market_cols:
            if col not in joined.columns:
                joined[col] = 0.0
        joined[feature_cols + market_cols] = joined[feature_cols + market_cols].apply(pd.to_numeric, errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(0.0)
        for col in target_columns:
            if col in joined.columns:
                joined[col] = pd.to_numeric(joined[col], errors="coerce").fillna(0).astype(int)
        keep = JOIN_KEYS + ["split_role"] + market_cols + feature_cols + [c for c in target_columns if c in joined.columns]
        joined = joined[keep]
        matrices.setdefault(horizon, {}).setdefault(split_role, []).append(joined)
        inventory_rows.append({**{"horizon_sec": horizon, "trade_date": key[1], "exchange": key[2], "symbol": key[3], "split_role": split_role}, "event_only_joined_rows": len(joined), "test_rows_used": 0})
    out: dict[int, dict[str, pd.DataFrame]] = {}
    for horizon, split_map in matrices.items():
        out[horizon] = {split_role: pd.concat(frames, ignore_index=True) for split_role, frames in split_map.items() if frames}
    return out, pd.DataFrame(inventory_rows)


def statutory_intraday_round_trip_bps(notional: float = 100_000.0) -> float:
    brokerage_bps = 2.0 * (min(0.0003 * notional, 20.0) / notional * 10_000.0)
    stt_bps = 0.00025 * 10_000.0
    transaction_bps = 2.0 * 0.0000307 * 10_000.0
    sebi_bps = 2.0 * (10.0 / 10_000_000.0) * 10_000.0
    stamp_bps = 0.00003 * 10_000.0
    gst_bps = 0.18 * (brokerage_bps + transaction_bps + sebi_bps)
    return float(brokerage_bps + stt_bps + transaction_bps + sebi_bps + stamp_bps + gst_bps)


def profile_cost_bps(frame: pd.DataFrame, profile: pd.Series) -> pd.Series:
    mid = ((pd.to_numeric(frame["best_bid"], errors="coerce") + pd.to_numeric(frame["best_ask"], errors="coerce")) / 2.0).replace(0, np.nan)
    spread_bps = (pd.to_numeric(frame["spread"], errors="coerce") / mid * 10_000.0).replace([np.inf, -np.inf], np.nan).fillna(0.0).clip(lower=0.0)
    tick_slippage_bps = (float(profile["slippage_ticks"]) * 0.05 / mid * 10_000.0).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    return statutory_intraday_round_trip_bps() + (2.0 * float(profile["spread_cross_multiplier"]) * spread_bps) + (2.0 * tick_slippage_bps)


def candidate_thresholds(rule: pd.Series) -> list[float]:
    values = split_columns(rule.get("max_threshold_grid_values", ""))
    return [float(v) for v in values] if values else [0.55, 0.60, 0.65, 0.70]


def score_frame(model: dict[str, Any], frame: pd.DataFrame) -> np.ndarray:
    x_raw = transform_features(frame, model["feature_columns"], str(model["model_family"])).to_numpy(dtype=float)
    x = (x_raw - model["means"]) / model["stds"] if len(x_raw) else np.zeros((0, len(model["feature_columns"])))
    design = np.column_stack([np.ones(len(x)), x]) if len(x) else np.zeros((0, len(model["feature_columns"]) + 1))
    return np.clip(design @ model["beta"], 0.0, 1.0) if len(design) else np.array([])


def payoff_unit_bps(horizon: int, target_label: str) -> float:
    if "vol_expansion" in target_label:
        return 1.0 if horizon <= 1 else 1.5
    return 1.0 if horizon <= 1 else 2.0


def summarize_replay(matrices: dict[int, dict[str, pd.DataFrame]], candidates: pd.DataFrame, signal_rules: pd.DataFrame, feature_map: dict[int, list[str]], latency: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(RNG_SEED)
    summary_rows: list[dict[str, Any]] = []
    control_rows: list[dict[str, Any]] = []
    threshold_rows: list[dict[str, Any]] = []
    profiles = latency[latency["profile_id"].astype(str).isin(["P180_ZERO_LATENCY_CONTROL_DIAGNOSTIC_ONLY", "P180_RETAIL_MARKETABLE_DEFAULT", "P180_STRESSED_RETAIL"])].copy()
    rules = signal_rules.set_index("phase219_model_fit_id") if not signal_rules.empty else pd.DataFrame()
    for candidate in candidates.to_dict("records"):
        model_id = str(candidate.get("phase219_model_fit_id", ""))
        horizon = as_int(candidate.get("horizon_sec", 0))
        target = str(candidate.get("target_label", ""))
        family = str(candidate.get("model_family", ""))
        feature_columns = feature_map.get(horizon, [])
        train = matrices.get(horizon, {}).get("train", pd.DataFrame())
        validation = matrices.get(horizon, {}).get("validation", pd.DataFrame())
        if train.empty or validation.empty or target not in train.columns or target not in validation.columns or not feature_columns:
            continue
        model = fit_ridge(train, feature_columns, target, family, shuffle=False)
        rule = rules.loc[model_id] if not rules.empty and model_id in rules.index else pd.Series(dtype=object)
        thresholds = candidate_thresholds(rule)
        for split_role, frame in [("train", train), ("validation", validation)]:
            scores = score_frame(model, frame)
            labels = pd.to_numeric(frame[target], errors="coerce").fillna(0).to_numpy(dtype=float)
            shuffled_labels = labels.copy()
            rng.shuffle(shuffled_labels)
            for threshold in thresholds:
                selected_mask = scores >= threshold
                selected = frame.loc[selected_mask].copy()
                selected_labels = labels[selected_mask]
                selected_shuffled = shuffled_labels[selected_mask]
                unit = payoff_unit_bps(horizon, target)
                gross = np.where(selected_labels >= 0.5, unit, -unit)
                shuffled_gross = np.where(selected_shuffled >= 0.5, unit, -unit)
                for profile in profiles.to_dict("records"):
                    profile_s = pd.Series(profile)
                    cost = profile_cost_bps(selected, profile_s).to_numpy(dtype=float) if len(selected) else np.array([])
                    for control_name, gross_values in [("actual_label_order", gross), ("shuffled_event_label_control", shuffled_gross)]:
                        net = gross_values - cost if len(gross_values) else np.array([])
                        row = {
                            "phase221_candidate_id": candidate.get("phase221_candidate_id", ""),
                            "phase219_model_fit_id": model_id,
                            "model_family": family,
                            "target_label": target,
                            "horizon_sec": horizon,
                            "split_role": split_role,
                            "threshold": threshold,
                            "latency_profile_id": profile.get("profile_id", ""),
                            "control_name": control_name,
                            "decision_events": int(len(gross_values)),
                            "hit_rate": float((gross_values > 0).mean()) if len(gross_values) else np.nan,
                            "gross_label_payoff_bps_proxy_mean": float(np.mean(gross_values)) if len(gross_values) else np.nan,
                            "cost_bound_bps_mean": float(np.mean(cost)) if len(cost) else np.nan,
                            "net_after_cost_bps_proxy_mean": float(np.mean(net)) if len(net) else np.nan,
                            "net_positive_event_fraction": float((net > 0).mean()) if len(net) else np.nan,
                            "test_rows_used": 0,
                            "promotion_allowed": 0,
                            "paper_or_live_acceptance_allowed": 0,
                            "profitability_claim_allowed": 0,
                        }
                        summary_rows.append(row)
                        if control_name != "actual_label_order":
                            control_rows.append(row)
                threshold_rows.append(
                    {
                        "phase219_model_fit_id": model_id,
                        "target_label": target,
                        "horizon_sec": horizon,
                        "split_role": split_role,
                        "threshold": threshold,
                        "candidate_score_rows": int(len(scores)),
                        "decision_events": int(selected_mask.sum()),
                        "activation_rate": float(selected_mask.mean()) if len(selected_mask) else np.nan,
                        "row_level_prediction_export_allowed": 0,
                        "test_rows_used": 0,
                    }
                )
    return pd.DataFrame(summary_rows), pd.DataFrame(control_rows), pd.DataFrame(threshold_rows)


def build_validation_screen(summary: pd.DataFrame) -> pd.DataFrame:
    if summary.empty:
        return pd.DataFrame()
    actual = summary[
        summary["split_role"].astype(str).eq("validation")
        & summary["control_name"].astype(str).eq("actual_label_order")
        & summary["latency_profile_id"].astype(str).isin(["P180_RETAIL_MARKETABLE_DEFAULT", "P180_STRESSED_RETAIL"])
    ].copy()
    if actual.empty:
        return actual
    net_proxy = pd.to_numeric(actual["net_after_cost_bps_proxy_mean"], errors="coerce")
    actual["rank_validation_net_proxy"] = net_proxy.rank(method="first", ascending=False, na_option="bottom").astype("Int64")
    actual["selected_for_phase223_interpretation"] = 1
    actual["test_replay_allowed_next"] = 0
    actual["promotion_allowed"] = 0
    return actual.sort_values("rank_validation_net_proxy")


def build_forbidden_execution_ledger() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "forbidden_output": item,
                "emitted_in_phase222": 0,
                "allowed_in_phase222": 0,
                "rationale": "Phase222 runs train/validation diagnostic signal replay only and emits no test, order/fill, P&L, promotion, paper/live, row-level prediction, or profitability artifact.",
            }
            for item in FORBIDDEN_OUTPUTS.split(";")
        ]
    )


def build_gates(phase221: pd.DataFrame, inventory: pd.DataFrame, summary: pd.DataFrame, controls: pd.DataFrame, thresholds: pd.DataFrame, forbidden: pd.DataFrame) -> pd.DataFrame:
    phase221_complete = as_int(metric_value(phase221, "phase221_event_only_signal_replay_precommit_or_stop_complete", 0))
    replay_precommitted = as_int(metric_value(phase221, "phase221_phase222_replay_dry_run_precommitted", 0))
    validation_events = int(pd.to_numeric(summary.loc[summary["split_role"].astype(str).eq("validation"), "decision_events"], errors="coerce").fillna(0).sum()) if not summary.empty else 0
    test_rows_used = 0
    for frame in [inventory, summary, controls, thresholds]:
        if not frame.empty and "test_rows_used" in frame.columns:
            test_rows_used += int(pd.to_numeric(frame["test_rows_used"], errors="coerce").fillna(0).sum())
    forbidden_emitted = int(pd.to_numeric(forbidden["emitted_in_phase222"], errors="coerce").fillna(0).sum()) if not forbidden.empty else 1
    forbidden_flags = 0
    for frame in [summary, controls]:
        for col in ["promotion_allowed", "paper_or_live_acceptance_allowed", "profitability_claim_allowed"]:
            if not frame.empty and col in frame.columns:
                forbidden_flags += int(pd.to_numeric(frame[col], errors="coerce").fillna(0).sum())
    return pd.DataFrame(
        [
            ("P222_PHASE221_COMPLETE_AND_REPLAY_PRECOMMITTED", phase221_complete == 1 and replay_precommitted == 1, f"phase221_complete={phase221_complete}; replay_precommitted={replay_precommitted}", "hard"),
            ("P222_EVENT_ONLY_MATRICES_JOINED", int(inventory["event_only_joined_rows"].sum()) > 0 if not inventory.empty else False, f"event_only_joined_rows={int(inventory['event_only_joined_rows'].sum()) if not inventory.empty else 0}", "hard"),
            ("P222_REPLAY_SUMMARY_RECORDED", len(summary) > 0 and validation_events > 0, f"summary_rows={len(summary)}; validation_decision_events={validation_events}", "hard"),
            ("P222_NEGATIVE_CONTROLS_RECORDED", len(controls) > 0, f"control_rows={len(controls)}", "hard"),
            ("P222_THRESHOLD_ACTIVATION_RECORDED", len(thresholds) > 0, f"threshold_rows={len(thresholds)}", "hard"),
            ("P222_TEST_ROWS_UNTOUCHED", test_rows_used == 0, f"test_rows_used={test_rows_used}", "hard"),
            ("P222_FORBIDDEN_OUTPUTS_CLEAN", forbidden_emitted == 0 and forbidden_flags == 0, f"forbidden_emitted={forbidden_emitted}; forbidden_flags={forbidden_flags}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(inventory: pd.DataFrame, summary: pd.DataFrame, controls: pd.DataFrame, thresholds: pd.DataFrame, screen: pd.DataFrame, forbidden: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    validation = summary[summary["split_role"].astype(str).eq("validation") & summary["control_name"].astype(str).eq("actual_label_order")] if not summary.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("phase222_event_only_partition_rows", len(inventory), "Train/validation event-only partition rows"),
            ("phase222_event_only_joined_rows", int(inventory["event_only_joined_rows"].sum()) if not inventory.empty else 0, "Joined event-only rows"),
            ("phase222_threshold_activation_rows", len(thresholds), "Threshold activation rows"),
            ("phase222_replay_summary_rows", len(summary), "Replay summary rows"),
            ("phase222_control_rows", len(controls), "Negative-control rows"),
            ("phase222_validation_screen_rows", len(screen), "Validation screen rows"),
            ("phase222_validation_decision_events", int(pd.to_numeric(validation["decision_events"], errors="coerce").fillna(0).sum()) if not validation.empty else 0, "Validation decision events"),
            ("phase222_best_validation_net_after_cost_bps_proxy", float(pd.to_numeric(validation["net_after_cost_bps_proxy_mean"], errors="coerce").max()) if not validation.empty else 0.0, "Best validation net-after-cost proxy"),
            ("phase222_worst_validation_net_after_cost_bps_proxy", float(pd.to_numeric(validation["net_after_cost_bps_proxy_mean"], errors="coerce").min()) if not validation.empty else 0.0, "Worst validation net-after-cost proxy"),
            ("phase222_forbidden_execution_rows", len(forbidden), "Forbidden execution rows"),
            ("phase222_gate_rows", len(gates), "Gates evaluated"),
            ("phase222_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase222_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase222_event_only_train_validation_signal_replay_dry_run_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase222 completed"),
            ("phase222_strategy_replay_execution", 1, "Train/validation signal replay dry run executed"),
            ("phase222_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase222_test_rows_used", 0, "No sealed test rows used"),
            ("phase222_promotion_allowed", 0, "No promotion opened"),
            ("phase222_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase222_profitability_claim_allowed", 0, "No profitability claim is allowed"),
            ("phase222_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase222_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase222 Event-only Train/Validation Signal Replay Dry Run",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase222 executes the Phase221-precommitted train/validation-only event-only signal replay dry run.",
        "It binds Phase180 Zerodha costs and latency/slippage profiles, records aggregate diagnostic replay summaries, and keeps sealed test, promotion, paper/live, row-level prediction export, and profitability claims closed.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase222_event_only_train_validation_signal_replay_dry_run_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase222(phase176_dir: Path, phase180_dir: Path, phase214_dir: Path, phase218_dir: Path, phase221_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase221 = read_csv(phase221_dir / "phase221_signal_replay_precommit_acceptance_summary.csv")
    candidates = read_csv(phase221_dir / "phase221_frozen_candidate_contract.csv")
    signal_rules = read_csv(phase221_dir / "phase221_signal_rule_contract.csv")
    feature_contract = read_csv(phase218_dir / "phase218_event_only_feature_contract.csv")
    feature_inventory = read_csv(phase176_dir / "phase176_feature_partition_inventory.csv")
    label_inventory = read_csv(phase214_dir / "phase214_label_partition_inventory.csv")
    latency = read_csv(phase180_dir / "phase180_latency_slippage_profile_catalog.csv")
    feature_map = feature_columns_by_horizon(feature_contract)
    matrices, inventory = load_event_only_matrices(feature_inventory, label_inventory, candidates, feature_map)
    summary, controls, thresholds = summarize_replay(matrices, candidates, signal_rules, feature_map, latency)
    screen = build_validation_screen(summary)
    forbidden = build_forbidden_execution_ledger()
    gates = build_gates(phase221, inventory, summary, controls, thresholds, forbidden)
    acceptance = build_acceptance(inventory, summary, controls, thresholds, screen, forbidden, gates)

    inventory.to_csv(output_dir / "phase222_event_only_partition_inventory.csv", index=False)
    thresholds.to_csv(output_dir / "phase222_threshold_activation_summary.csv", index=False)
    summary.to_csv(output_dir / "phase222_signal_replay_summary.csv", index=False)
    controls.to_csv(output_dir / "phase222_negative_control_summary.csv", index=False)
    screen.to_csv(output_dir / "phase222_validation_screen.csv", index=False)
    forbidden.to_csv(output_dir / "phase222_execution_forbidden_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase222_signal_replay_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase222_signal_replay_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Event-only Partition Inventory": inventory,
            "Threshold Activation Summary": thresholds,
            "Signal Replay Summary": summary,
            "Negative Control Summary": controls,
            "Validation Screen": screen,
            "Forbidden Execution Ledger": forbidden,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase222_event_only_train_validation_signal_replay_dry_run_no_test",
        **reproducibility_fields(
            artifact_id="phase222_event_only_train_validation_signal_replay_dry_run",
            generated_utc=generated,
            inputs={
                "phase221_acceptance": str(phase221_dir / "phase221_signal_replay_precommit_acceptance_summary.csv"),
                "phase221_candidates": str(phase221_dir / "phase221_frozen_candidate_contract.csv"),
                "phase221_signal_rules": str(phase221_dir / "phase221_signal_rule_contract.csv"),
                "phase180_latency": str(phase180_dir / "phase180_latency_slippage_profile_catalog.csv"),
                "phase176_feature_inventory": str(phase176_dir / "phase176_feature_partition_inventory.csv"),
                "phase214_label_inventory": str(phase214_dir / "phase214_label_partition_inventory.csv"),
                "phase218_feature_contract": str(phase218_dir / "phase218_event_only_feature_contract.csv"),
            },
            parameters={
                "rng_seed": str(RNG_SEED),
                "threshold_grid": "0.55;0.60;0.65;0.70",
                "event_only_filter": "event_surprise_bucket == 1",
                "payoff_proxy": "label_correctness_bps_proxy_not_pnl",
                "cost_model": "phase180_zerodha_intraday_round_trip_cost_bound",
                "allowed_splits": "train;validation",
                "test_rows_used": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "inventory": str(output_dir / "phase222_event_only_partition_inventory.csv"),
                "thresholds": str(output_dir / "phase222_threshold_activation_summary.csv"),
                "summary": str(output_dir / "phase222_signal_replay_summary.csv"),
                "controls": str(output_dir / "phase222_negative_control_summary.csv"),
                "screen": str(output_dir / "phase222_validation_screen.csv"),
                "forbidden": str(output_dir / "phase222_execution_forbidden_ledger.csv"),
                "gates": str(output_dir / "phase222_signal_replay_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase222_signal_replay_acceptance_summary.csv"),
                "report": str(output_dir / "phase222_event_only_train_validation_signal_replay_dry_run_report.md"),
            },
            scenario_ids="phase222_event_only_train_validation_signal_replay_dry_run_no_test",
            cost_model_version="phase180_zerodha_equity_cost_component_catalog_bound",
            latency_model_version="phase180_latency_slippage_profile_catalog_bound",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase222_signal_replay_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase222 event-only train/validation signal replay dry run without test.")
    parser.add_argument("--phase176-dir", type=Path, default=DEFAULT_PHASE176_DIR)
    parser.add_argument("--phase180-dir", type=Path, default=DEFAULT_PHASE180_DIR)
    parser.add_argument("--phase214-dir", type=Path, default=DEFAULT_PHASE214_DIR)
    parser.add_argument("--phase218-dir", type=Path, default=DEFAULT_PHASE218_DIR)
    parser.add_argument("--phase221-dir", type=Path, default=DEFAULT_PHASE221_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase222(args.phase176_dir, args.phase180_dir, args.phase214_dir, args.phase218_dir, args.phase221_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
