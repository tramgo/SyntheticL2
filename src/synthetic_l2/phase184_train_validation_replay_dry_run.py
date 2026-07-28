from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE176_DIR = Path("outputs/phase176")
DEFAULT_PHASE180_DIR = Path("outputs/phase180")
DEFAULT_PHASE181_DIR = Path("outputs/phase181")
DEFAULT_PHASE183_DIR = Path("outputs/phase183")
DEFAULT_OUTPUT_DIR = Path("outputs/phase184")
DEFAULT_FEATURE_ROOT = Path("derived_real_l2_receive_flow_features_phase176")
DEFAULT_LABEL_ROOT = Path("derived_real_l2_receive_flow_labels_phase181")
RANDOM_SEED = 184
FORBIDDEN_OUTPUTS = "order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance;test_result;promotion"

FEATURE_ID_TO_COLUMN = {
    "P175_RECEIVE_EVENT_RATE_ZSCORE": "receive_event_rate_zscore",
    "P175_QUOTE_CHURN_RATE": "quote_churn_count",
    "P175_DEPTH_REFRESH_INTENSITY": "depth_refresh_count",
    "P175_STALE_QUOTE_DURATION": "stale_quote_duration_ms",
    "P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY": "cross_symbol_arrival_share",
    "P175_RECEIVE_FLOW_REGIME_STATE": "receive_event_count",
}


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


def load_joined_partition(feature_path: Path, label_path: Path) -> pd.DataFrame:
    features = pd.read_parquet(feature_path)
    labels = pd.read_parquet(label_path)
    keys = ["bucket_ms", "trade_date", "exchange", "symbol", "horizon_sec"]
    keep_label_columns = keys + [
        "split_role",
        "future_mid_return_bps_next_bucket",
        "short_horizon_direction_label",
        "label_available",
    ]
    return features.merge(labels[keep_label_columns], on=keys, how="inner")


def build_model_frame(feature_inventory: pd.DataFrame, label_inventory: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    label_lookup = label_inventory.set_index(["horizon_sec", "trade_date", "exchange", "symbol"])
    frames: list[pd.DataFrame] = []
    partition_rows: list[dict[str, Any]] = []
    for item in feature_inventory.to_dict("records"):
        key = (item["horizon_sec"], item["trade_date"], item["exchange"], item["symbol"])
        if key not in label_lookup.index:
            continue
        label_row = label_lookup.loc[key]
        split_role = str(label_row["split_role"])
        if split_role == "test_untouched":
            partition_rows.append({**{k: item[k] for k in ["horizon_sec", "trade_date", "exchange", "symbol"]}, "split_role": split_role, "rows_joined": 0, "used_in_phase184": 0})
            continue
        joined = load_joined_partition(Path(item["parquet_file"]), Path(label_row["label_file"]))
        joined = joined.loc[joined["label_available"].astype(int).eq(1)].copy()
        joined["split_role"] = split_role
        frames.append(joined)
        partition_rows.append(
            {
                **{k: item[k] for k in ["horizon_sec", "trade_date", "exchange", "symbol"]},
                "split_role": split_role,
                "rows_joined": int(len(joined)),
                "used_in_phase184": int(split_role in {"train", "validation"}),
            }
        )
    if not frames:
        return pd.DataFrame(), pd.DataFrame(partition_rows)
    return pd.concat(frames, ignore_index=True), pd.DataFrame(partition_rows)


def feature_columns_for_family(row: pd.Series) -> list[str]:
    ids = [x.strip() for x in str(row["allowed_feature_ids"]).split(";") if x.strip()]
    return [FEATURE_ID_TO_COLUMN[x] for x in ids if x in FEATURE_ID_TO_COLUMN]


def fit_family_parameters(frame: pd.DataFrame, replay_contract: pd.DataFrame) -> pd.DataFrame:
    train = frame.loc[frame["split_role"].astype(str).eq("train")].copy()
    target = pd.to_numeric(train["future_mid_return_bps_next_bucket"], errors="coerce")
    rows: list[dict[str, Any]] = []
    for family in replay_contract.to_dict("records"):
        family_id = family["strategy_family_id"]
        cols = feature_columns_for_family(pd.Series(family))
        params: dict[str, Any] = {
            "strategy_family_id": family_id,
            "feature_columns": ";".join(cols),
            "fit_split_role": "train",
            "validation_used_for_fit": 0,
            "test_used_for_fit": 0,
            "threshold_selection_split": "train",
        }
        score = pd.Series(0.0, index=train.index)
        weight_parts: list[str] = []
        for col in cols:
            values = pd.to_numeric(train[col], errors="coerce")
            mean = float(values.mean()) if values.notna().any() else 0.0
            std = float(values.std(ddof=0)) if values.notna().any() else 0.0
            if not np.isfinite(std) or std <= 0:
                std = 1.0
            z = ((values - mean) / std).replace([np.inf, -np.inf], np.nan).fillna(0.0)
            corr = float(z.corr(target)) if target.notna().sum() > 2 else 0.0
            if not np.isfinite(corr):
                corr = 0.0
            score = score + (corr * z)
            params[f"{col}_train_mean"] = mean
            params[f"{col}_train_std"] = std
            params[f"{col}_train_target_corr_weight"] = corr
            weight_parts.append(f"{col}:{corr:.8f}")
        params["train_weight_spec"] = ";".join(weight_parts)
        params["long_score_threshold_train_q90"] = float(score.quantile(0.90)) if len(score) else np.nan
        params["short_score_threshold_train_q10"] = float(score.quantile(0.10)) if len(score) else np.nan
        params["train_rows_used"] = int(len(train))
        rows.append(params)
    return pd.DataFrame(rows)


def apply_family_score(frame: pd.DataFrame, params: pd.Series) -> pd.Series:
    score = pd.Series(0.0, index=frame.index)
    for col in str(params["feature_columns"]).split(";"):
        if not col:
            continue
        values = pd.to_numeric(frame[col], errors="coerce")
        mean = float(params.get(f"{col}_train_mean", 0.0))
        std = float(params.get(f"{col}_train_std", 1.0))
        if not np.isfinite(std) or std <= 0:
            std = 1.0
        weight = float(params.get(f"{col}_train_target_corr_weight", 0.0))
        score = score + weight * ((values - mean) / std).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    return score


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
    slippage_ticks = float(profile["slippage_ticks"])
    spread_cross_multiplier = float(profile["spread_cross_multiplier"])
    tick_slippage_bps = (slippage_ticks * 0.05 / mid * 10_000.0).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    return statutory_intraday_round_trip_bps() + (2.0 * spread_cross_multiplier * spread_bps) + (2.0 * tick_slippage_bps)


def summarize_replay(frame: pd.DataFrame, fit_params: pd.DataFrame, latency_profiles: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(RANDOM_SEED)
    event_rows: list[dict[str, Any]] = []
    control_rows: list[dict[str, Any]] = []
    usable_profiles = latency_profiles.loc[latency_profiles["profile_id"].astype(str).isin(["P180_RETAIL_MARKETABLE_DEFAULT", "P180_STRESSED_RETAIL"])].copy()
    for params in fit_params.to_dict("records"):
        params_s = pd.Series(params)
        score = apply_family_score(frame, params_s)
        long_threshold = float(params_s["long_score_threshold_train_q90"])
        short_threshold = float(params_s["short_score_threshold_train_q10"])
        side = pd.Series(0, index=frame.index)
        side.loc[score >= long_threshold] = 1
        side.loc[score <= short_threshold] = -1
        selected = frame.loc[side.ne(0)].copy()
        selected_side = side.loc[side.ne(0)]
        if selected.empty:
            selected["gross_return_bps_proxy"] = pd.Series(dtype=float)
        else:
            selected["gross_return_bps_proxy"] = selected_side.to_numpy() * pd.to_numeric(selected["future_mid_return_bps_next_bucket"], errors="coerce").to_numpy()
        shuffled = selected["future_mid_return_bps_next_bucket"].to_numpy(copy=True)
        rng.shuffle(shuffled)
        selected["shuffled_time_return_bps_proxy"] = selected_side.to_numpy() * shuffled if len(selected) else []
        shuffled_symbol = frame["future_mid_return_bps_next_bucket"].sample(frac=1.0, random_state=RANDOM_SEED).reset_index(drop=True).to_numpy()
        symbol_control = pd.Series(shuffled_symbol[: len(selected)], index=selected.index) if len(selected) else pd.Series(dtype=float)
        selected["shuffled_symbol_return_bps_proxy"] = selected_side.to_numpy() * symbol_control.to_numpy() if len(selected) else []

        for profile in usable_profiles.to_dict("records"):
            profile_s = pd.Series(profile)
            if selected.empty:
                work = selected.copy()
                costs = pd.Series(dtype=float)
            else:
                work = selected.copy()
                costs = profile_cost_bps(work, profile_s)
            work["cost_bound_bps"] = costs
            for split_role in ["train", "validation"]:
                part = work.loc[work["split_role"].astype(str).eq(split_role)]
                for control_name, gross_col in [
                    ("actual_time_order", "gross_return_bps_proxy"),
                    ("shuffled_time_negative_control", "shuffled_time_return_bps_proxy"),
                    ("shuffled_symbol_negative_control", "shuffled_symbol_return_bps_proxy"),
                ]:
                    gross = pd.to_numeric(part[gross_col], errors="coerce") if not part.empty else pd.Series(dtype=float)
                    cost = pd.to_numeric(part["cost_bound_bps"], errors="coerce") if not part.empty else pd.Series(dtype=float)
                    net = gross - cost
                    row = {
                        "strategy_family_id": params["strategy_family_id"],
                        "latency_profile_id": profile["profile_id"],
                        "split_role": split_role,
                        "control_name": control_name,
                        "dry_decision_events": int(len(part)),
                        "gross_return_bps_proxy_mean": float(gross.mean()) if len(gross) else np.nan,
                        "cost_bound_bps_mean": float(cost.mean()) if len(cost) else np.nan,
                        "net_return_bps_after_cost_proxy_mean": float(net.mean()) if len(net) else np.nan,
                        "net_positive_event_fraction": float((net > 0).mean()) if len(net) else np.nan,
                        "promotion_allowed": 0,
                        "test_rows_used": 0,
                    }
                    event_rows.append(row)
                    if control_name != "actual_time_order":
                        control_rows.append(row)
    return pd.DataFrame(event_rows), pd.DataFrame(control_rows)


def build_selection_screen(summary: pd.DataFrame) -> pd.DataFrame:
    actual = summary.loc[summary["control_name"].astype(str).eq("actual_time_order") & summary["split_role"].astype(str).eq("validation")].copy()
    if actual.empty:
        return pd.DataFrame()
    actual["rank_validation_net_proxy"] = actual["net_return_bps_after_cost_proxy_mean"].rank(method="first", ascending=False).astype(int)
    actual["selected_for_future_test_replay"] = 0
    actual["promotion_allowed"] = 0
    actual["selection_interpretation"] = "validation screen only; no test rows used and no promotion opened"
    return actual.sort_values("rank_validation_net_proxy")


def build_gate_evaluation(
    phase183: pd.DataFrame,
    partition_use: pd.DataFrame,
    fit_params: pd.DataFrame,
    summary: pd.DataFrame,
    controls: pd.DataFrame,
) -> pd.DataFrame:
    readiness = as_int(metric_value(phase183, "phase183_replay_readiness_precommitted", 0))
    test_rows_used = int(partition_use.loc[partition_use["split_role"].astype(str).eq("test_untouched"), "used_in_phase184"].sum()) if not partition_use.empty else 0
    validation_rows = int(partition_use.loc[partition_use["split_role"].astype(str).eq("validation"), "rows_joined"].sum()) if not partition_use.empty else 0
    train_rows = int(partition_use.loc[partition_use["split_role"].astype(str).eq("train"), "rows_joined"].sum()) if not partition_use.empty else 0
    controls_present = int(set(controls["control_name"].astype(str).unique()) >= {"shuffled_time_negative_control", "shuffled_symbol_negative_control"}) if not controls.empty else 0
    return pd.DataFrame(
        [
            {"gate_id": "P184_PHASE183_REPLAY_READINESS_PRECOMMITTED", "gate_pass": int(readiness == 1), "evidence": f"phase183_replay_readiness_precommitted={readiness}", "severity": "hard"},
            {"gate_id": "P184_TRAIN_ROWS_PRESENT", "gate_pass": int(train_rows > 0), "evidence": f"train_rows={train_rows}", "severity": "hard"},
            {"gate_id": "P184_VALIDATION_ROWS_PRESENT", "gate_pass": int(validation_rows > 0), "evidence": f"validation_rows={validation_rows}", "severity": "hard"},
            {"gate_id": "P184_TEST_ROWS_UNTOUCHED", "gate_pass": int(test_rows_used == 0), "evidence": f"test_rows_used={test_rows_used}", "severity": "hard"},
            {"gate_id": "P184_TRAIN_ONLY_FIT_PARAMETERS", "gate_pass": int(not fit_params.empty and fit_params["validation_used_for_fit"].astype(int).eq(0).all() and fit_params["test_used_for_fit"].astype(int).eq(0).all()), "evidence": f"fit_parameter_rows={len(fit_params)}", "severity": "hard"},
            {"gate_id": "P184_COST_LATENCY_BOUND_SUMMARY", "gate_pass": int(not summary.empty and summary["latency_profile_id"].astype(str).isin(["P180_RETAIL_MARKETABLE_DEFAULT", "P180_STRESSED_RETAIL"]).all()), "evidence": f"summary_rows={len(summary)}", "severity": "hard"},
            {"gate_id": "P184_NEGATIVE_CONTROLS_PRESENT", "gate_pass": controls_present, "evidence": f"control_rows={len(controls)}", "severity": "hard"},
            {"gate_id": "P184_NO_PROMOTION_OR_PAPER_LIVE", "gate_pass": int(not summary.empty and summary["promotion_allowed"].astype(int).eq(0).all()), "evidence": "promotion_allowed=0; paper_live_acceptance_allowed=0", "severity": "hard"},
        ]
    )


def build_acceptance_summary(partition_use: pd.DataFrame, fit_params: pd.DataFrame, summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates.loc[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(int).sum()) if not hard.empty else 0
    dry_run_complete = int(len(hard) > 0 and hard_pass == len(hard))
    rows = [
        ("phase184_partition_rows_scanned", int(len(partition_use)), "Feature/label partitions scanned"),
        ("phase184_train_partitions_used", int(partition_use.loc[partition_use["split_role"].astype(str).eq("train"), "used_in_phase184"].sum()) if not partition_use.empty else 0, "Train partitions used"),
        ("phase184_validation_partitions_used", int(partition_use.loc[partition_use["split_role"].astype(str).eq("validation"), "used_in_phase184"].sum()) if not partition_use.empty else 0, "Validation partitions used"),
        ("phase184_test_partitions_used", int(partition_use.loc[partition_use["split_role"].astype(str).eq("test_untouched"), "used_in_phase184"].sum()) if not partition_use.empty else 0, "Test partitions used"),
        ("phase184_train_rows_used", int(partition_use.loc[partition_use["split_role"].astype(str).eq("train"), "rows_joined"].sum()) if not partition_use.empty else 0, "Train rows used"),
        ("phase184_validation_rows_used", int(partition_use.loc[partition_use["split_role"].astype(str).eq("validation"), "rows_joined"].sum()) if not partition_use.empty else 0, "Validation rows used"),
        ("phase184_fit_parameter_rows", int(len(fit_params)), "Train-fitted family parameter rows"),
        ("phase184_dry_run_summary_rows", int(len(summary)), "Dry-run summary rows"),
        ("phase184_gate_rows", int(len(gates)), "Gates evaluated"),
        ("phase184_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
        ("phase184_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase184_train_validation_dry_run_complete", dry_run_complete, "1 means Phase184 dry run completed"),
        ("phase184_strategy_replay_dry_run_performed", dry_run_complete, "Dry replay summary performed without orders/fills/P&L"),
        ("phase184_test_rows_used", 0, "Test rows remain untouched"),
        ("phase184_promotion_allowed", 0, "No promotion opened"),
        ("phase184_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
        ("phase184_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
        ("phase184_next_best_action", "build_phase185_validation_replay_interpretation_and_kill_switch_audit_no_test" if dry_run_complete else "repair_phase184_train_validation_dry_run", "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, selection: pd.DataFrame, gates: pd.DataFrame, summary: pd.DataFrame) -> None:
    lines = [
        "# Phase184 Train/Validation Replay Dry-run",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase184 runs a train/validation-only dry replay over the audited receive-flow feature and label stack.",
        "It binds Phase180 retail/stressed cost and latency profiles and includes shuffled negative controls.",
        "It does not use test rows, emit orders/fills, calculate contract-note P&L, claim profitability, open paper/live acceptance, or promote any candidate.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Validation Selection Screen",
        "",
        _markdown_table(selection),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "## Dry-run Summary Sample",
        "",
        _markdown_table(summary.head(24)),
        "",
    ]
    (output_dir / "phase184_train_validation_replay_dry_run_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase184(
    phase176_dir: Path,
    phase180_dir: Path,
    phase181_dir: Path,
    phase183_dir: Path,
    output_dir: Path,
    base_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase183 = read_csv(phase183_dir / "phase183_replay_readiness_precommit_acceptance_summary.csv")
    replay_contract = read_csv(phase183_dir / "phase183_replay_input_contract.csv")
    feature_inventory = read_csv(phase176_dir / "phase176_feature_partition_inventory.csv")
    label_inventory = read_csv(phase181_dir / "phase181_label_partition_inventory.csv")
    latency_profiles = read_csv(phase180_dir / "phase180_latency_slippage_profile_catalog.csv")

    frame, partition_use = build_model_frame(feature_inventory, label_inventory)
    fit_params = fit_family_parameters(frame, replay_contract) if not frame.empty else pd.DataFrame()
    summary, controls = summarize_replay(frame, fit_params, latency_profiles) if not fit_params.empty else (pd.DataFrame(), pd.DataFrame())
    selection = build_selection_screen(summary)
    gates = build_gate_evaluation(phase183, partition_use, fit_params, summary, controls)
    acceptance = build_acceptance_summary(partition_use, fit_params, summary, gates)

    partition_use.to_csv(output_dir / "phase184_partition_use_audit.csv", index=False)
    fit_params.to_csv(output_dir / "phase184_train_fit_parameters.csv", index=False)
    summary.to_csv(output_dir / "phase184_dry_run_summary.csv", index=False)
    controls.to_csv(output_dir / "phase184_negative_control_summary.csv", index=False)
    selection.to_csv(output_dir / "phase184_validation_selection_screen.csv", index=False)
    gates.to_csv(output_dir / "phase184_train_validation_replay_dry_run_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase184_train_validation_replay_dry_run_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, selection, gates, summary)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase184_train_validation_replay_dry_run_no_test_no_promotion",
        **reproducibility_fields(
            artifact_id="phase184_train_validation_replay_dry_run",
            generated_utc=generated_utc,
            inputs={
                "phase183_acceptance": str(phase183_dir / "phase183_replay_readiness_precommit_acceptance_summary.csv"),
                "phase183_replay_input_contract": str(phase183_dir / "phase183_replay_input_contract.csv"),
                "phase176_feature_inventory": str(phase176_dir / "phase176_feature_partition_inventory.csv"),
                "phase181_label_inventory": str(phase181_dir / "phase181_label_partition_inventory.csv"),
                "phase180_latency_profiles": str(phase180_dir / "phase180_latency_slippage_profile_catalog.csv"),
            },
            parameters={
                "random_seed": RANDOM_SEED,
                "fit_split": "train",
                "evaluation_splits": "train;validation",
                "test_rows_used": 0,
                "promotion_allowed": 0,
            },
            outputs={
                "partition_use_audit": str(output_dir / "phase184_partition_use_audit.csv"),
                "train_fit_parameters": str(output_dir / "phase184_train_fit_parameters.csv"),
                "dry_run_summary": str(output_dir / "phase184_dry_run_summary.csv"),
                "negative_control_summary": str(output_dir / "phase184_negative_control_summary.csv"),
                "validation_selection_screen": str(output_dir / "phase184_validation_selection_screen.csv"),
                "gate_evaluation": str(output_dir / "phase184_train_validation_replay_dry_run_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase184_train_validation_replay_dry_run_acceptance_summary.csv"),
                "report": str(output_dir / "phase184_train_validation_replay_dry_run_report.md"),
            },
            random_seed=RANDOM_SEED,
            scenario_ids="phase184_train_validation_replay_dry_run",
            cost_model_version="phase180_zerodha_equity_intraday_cost_bound_proxy",
            latency_model_version="phase180_retail_marketable_default_and_stressed_retail",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase184_train_validation_replay_dry_run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase176-dir", type=Path, default=DEFAULT_PHASE176_DIR)
    parser.add_argument("--phase180-dir", type=Path, default=DEFAULT_PHASE180_DIR)
    parser.add_argument("--phase181-dir", type=Path, default=DEFAULT_PHASE181_DIR)
    parser.add_argument("--phase183-dir", type=Path, default=DEFAULT_PHASE183_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase184(args.phase176_dir, args.phase180_dir, args.phase181_dir, args.phase183_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
