from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase184_train_validation_replay_dry_run import build_model_frame
from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE176_DIR = Path("outputs/phase176")
DEFAULT_PHASE181_DIR = Path("outputs/phase181")
DEFAULT_PHASE196_DIR = Path("outputs/phase196")
DEFAULT_OUTPUT_DIR = Path("outputs/phase197")
FORBIDDEN_OUTPUTS = "test_result;test_replay_execution;strategy_replay;order_arrival;fill_model;pnl_replay;profitability_claim;promotion;paper_live_acceptance"


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


def clean_numeric(series: pd.Series, clip_abs: float = 1_000_000.0) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).clip(-clip_abs, clip_abs)


def derive_context_features(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    seconds_ist = ((pd.to_numeric(out["bucket_ms"], errors="coerce") // 1000 + 19_800) % 86_400).astype("float64")
    out["seconds_from_open_ist"] = seconds_ist - ((9 * 60 + 15) * 60)
    out["time_of_day_sin_ist"] = np.sin(2.0 * np.pi * seconds_ist / 86_400.0)
    out["time_of_day_cos_ist"] = np.cos(2.0 * np.pi * seconds_ist / 86_400.0)
    mid = ((clean_numeric(out["best_bid"]) + clean_numeric(out["best_ask"])) / 2.0).replace(0, np.nan)
    out["spread_bps"] = (clean_numeric(out["spread"]) / mid * 10_000.0).replace([np.inf, -np.inf], np.nan)
    out["quote_churn_log"] = np.log1p(clean_numeric(out["quote_churn_count"]).fillna(0).clip(lower=0))
    out["depth_refresh_log"] = np.log1p(clean_numeric(out["depth_refresh_count"]).fillna(0).clip(lower=0))
    out["stale_quote_log_ms"] = np.log1p(clean_numeric(out["stale_quote_duration_ms"], 60_000).fillna(0).clip(lower=0))
    out["asset_class_proxy"] = np.where(out["symbol"].astype(str).str.endswith("BEES"), "etf", "equity")

    train = out.loc[out["split_role"].astype(str).eq("train")].copy()
    if train.empty:
        out["symbol_train_spread_bps_median"] = np.nan
        out["symbol_train_receive_event_count_median"] = np.nan
    else:
        symbol_baseline = (
            train.groupby("symbol", as_index=False)
            .agg(
                symbol_train_spread_bps_median=("spread_bps", "median"),
                symbol_train_receive_event_count_median=("receive_event_count", "median"),
            )
        )
        out = out.merge(symbol_baseline, on="symbol", how="left")
    out["relative_spread_to_symbol_train_median"] = out["spread_bps"] / out["symbol_train_spread_bps_median"].replace(0, np.nan)
    out["relative_receive_count_to_symbol_train_median"] = clean_numeric(out["receive_event_count"]) / out["symbol_train_receive_event_count_median"].replace(0, np.nan)

    xsec = (
        out.groupby(["trade_date", "bucket_ms"], as_index=False)
        .agg(
            market_active_symbol_count=("symbol", "nunique"),
            market_median_spread_bps=("spread_bps", "median"),
            market_median_top5_imbalance=("top5_qty_imbalance", "median"),
            market_receive_event_count_sum=("receive_event_count", "sum"),
            market_cross_symbol_arrival_share=("cross_symbol_arrival_share", "mean"),
        )
        .sort_values(["trade_date", "bucket_ms"])
    )
    for col in [
        "market_active_symbol_count",
        "market_median_spread_bps",
        "market_median_top5_imbalance",
        "market_receive_event_count_sum",
        "market_cross_symbol_arrival_share",
    ]:
        xsec[f"prior_{col}"] = xsec.groupby("trade_date")[col].shift(1)
    prior_cols = ["trade_date", "bucket_ms"] + [c for c in xsec.columns if c.startswith("prior_")]
    out = out.merge(xsec[prior_cols], on=["trade_date", "bucket_ms"], how="left")
    return out


def feature_contract() -> pd.DataFrame:
    rows = [
        {
            "feature_id": "P197_TIME_OF_DAY_CONTEXT",
            "feature_family": "intraday_time_context",
            "candidate_columns": "seconds_from_open_ist;time_of_day_sin_ist;time_of_day_cos_ist",
            "derivation": "bucket timestamp transformed to IST session-relative features",
            "non_receive_flow_dimension": "session_clock",
            "leakage_boundary": "uses timestamp only; no target or future data",
        },
        {
            "feature_id": "P197_SYMBOL_LIQUIDITY_REGIME",
            "feature_family": "symbol_liquidity_regime",
            "candidate_columns": "symbol_train_spread_bps_median;symbol_train_receive_event_count_median;relative_spread_to_symbol_train_median;relative_receive_count_to_symbol_train_median",
            "derivation": "symbol baselines fitted on train split only and applied to non-test rows",
            "non_receive_flow_dimension": "symbol_baseline_liquidity",
            "leakage_boundary": "train-only baselines; validation/unassigned not used for fitting",
        },
        {
            "feature_id": "P197_MARKET_CONTEXT_LAGGED",
            "feature_family": "lagged_market_context",
            "candidate_columns": "prior_market_active_symbol_count;prior_market_median_spread_bps;prior_market_median_top5_imbalance;prior_market_receive_event_count_sum;prior_market_cross_symbol_arrival_share",
            "derivation": "cross-sectional market context lagged by one receive bucket",
            "non_receive_flow_dimension": "market_regime_context",
            "leakage_boundary": "prior bucket only; no same-bucket target return and no future data",
        },
        {
            "feature_id": "P197_ASSET_CLASS_PROXY",
            "feature_family": "instrument_context",
            "candidate_columns": "asset_class_proxy",
            "derivation": "static symbol-name proxy for equity versus ETF-like BEES instruments",
            "non_receive_flow_dimension": "instrument_type",
            "leakage_boundary": "static symbol metadata proxy; no target data",
        },
        {
            "feature_id": "P197_MICROSTRUCTURE_TRANSFORMS",
            "feature_family": "nonlinear_microstructure_context",
            "candidate_columns": "spread_bps;quote_churn_log;depth_refresh_log;stale_quote_log_ms",
            "derivation": "current observable L1/top-five state transformed into stable nonlinear context fields",
            "non_receive_flow_dimension": "liquidity_and_staleness_context",
            "leakage_boundary": "computed from current-or-prior observed book state only",
        },
    ]
    contract = pd.DataFrame(rows)
    contract["precommit_status"] = "candidate_for_phase198_search_only"
    contract["strategy_replay_allowed"] = 0
    contract["test_replay_allowed_next"] = 0
    contract["promotion_allowed"] = 0
    contract["paper_or_live_acceptance_allowed"] = 0
    return contract


def availability_audit(frame: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for item in contract.to_dict("records"):
        columns = [c for c in str(item["candidate_columns"]).split(";") if c]
        for split_role, part in frame.groupby("split_role"):
            present = [c for c in columns if c in part.columns]
            numeric_columns = [c for c in present if c != "asset_class_proxy"]
            usable_counts = []
            for col in numeric_columns:
                usable_counts.append(int(clean_numeric(part[col]).notna().sum()))
            categorical_ok = int("asset_class_proxy" in present and part["asset_class_proxy"].astype(str).ne("").any())
            min_usable = min(usable_counts) if usable_counts else (int(len(part)) if categorical_ok else 0)
            rows.append(
                {
                    "feature_id": item["feature_id"],
                    "feature_family": item["feature_family"],
                    "split_role": split_role,
                    "rows_scanned": int(len(part)),
                    "candidate_columns": ";".join(columns),
                    "present_column_count": int(len(present)),
                    "required_column_count": int(len(columns)),
                    "min_usable_rows_any_column": int(min_usable),
                    "feature_available_for_future_search": int(len(present) == len(columns) and min_usable > 0),
                    "test_rows_used": 0,
                }
            )
    return pd.DataFrame(rows)


def split_use_audit(partition_use: pd.DataFrame) -> pd.DataFrame:
    out = partition_use.copy()
    if out.empty:
        return out
    out["used_in_phase197_feature_precommit"] = np.where(out["split_role"].astype(str).eq("test_untouched"), 0, 1)
    return out


def candidate_matrix(contract: pd.DataFrame, audit: pd.DataFrame) -> pd.DataFrame:
    if audit.empty:
        out = contract.copy()
        out["train_available"] = 0
        out["validation_available"] = 0
        out["unassigned_available"] = 0
        out["ready_for_phase198_search"] = 0
        return out
    pivot = (
        audit.pivot_table(
            index="feature_id",
            columns="split_role",
            values="feature_available_for_future_search",
            aggfunc="min",
            fill_value=0,
        )
        .reset_index()
        .rename(columns={"train": "train_available", "validation": "validation_available", "unassigned": "unassigned_available"})
    )
    out = contract.merge(pivot, on="feature_id", how="left").fillna(0)
    for col in ["train_available", "validation_available", "unassigned_available"]:
        if col not in out.columns:
            out[col] = 0
        out[col] = out[col].astype(int)
    out["ready_for_phase198_search"] = ((out["train_available"] == 1) & (out["validation_available"] == 1)).astype(int)
    out["phase198_allowed_use"] = np.where(out["ready_for_phase198_search"].eq(1), "train_selection_and_validation_extension_screen_no_test", "blocked_until_available")
    return out


def build_gates(phase196: pd.DataFrame, split_use: pd.DataFrame, contract: pd.DataFrame, audit: pd.DataFrame, matrix: pd.DataFrame) -> pd.DataFrame:
    phase196_complete = as_int(metric_value(phase196, "phase196_expanded_model_search_complete", 0))
    test_partitions_used = int(split_use.loc[split_use["split_role"].astype(str).eq("test_untouched"), "used_in_phase197_feature_precommit"].sum()) if not split_use.empty else 0
    ready = int(matrix["ready_for_phase198_search"].astype(int).sum()) if not matrix.empty else 0
    leakage_boundaries = int(contract["leakage_boundary"].astype(str).ne("").all()) if not contract.empty else 0
    return pd.DataFrame(
        [
            {"gate_id": "P197_PHASE196_COMPLETE", "gate_pass": int(phase196_complete == 1), "evidence": f"phase196_expanded_model_search_complete={phase196_complete}", "severity": "hard"},
            {"gate_id": "P197_FEATURE_CONTRACT_RECORDED", "gate_pass": int(len(contract) >= 5), "evidence": f"feature_contract_rows={len(contract)}", "severity": "hard"},
            {"gate_id": "P197_AVAILABILITY_AUDIT_RECORDED", "gate_pass": int(not audit.empty), "evidence": f"availability_rows={len(audit)}", "severity": "hard"},
            {"gate_id": "P197_TEST_SPLIT_NOT_USED", "gate_pass": int(test_partitions_used == 0), "evidence": f"test_partitions_used={test_partitions_used}", "severity": "hard"},
            {"gate_id": "P197_LEAKAGE_BOUNDARIES_RECORDED", "gate_pass": leakage_boundaries, "evidence": f"leakage_boundary_rows={int(contract['leakage_boundary'].astype(str).ne('').sum()) if not contract.empty else 0}", "severity": "hard"},
            {"gate_id": "P197_PHASE198_READY_FEATURES_RECORDED", "gate_pass": int(ready >= 1), "evidence": f"ready_feature_families={ready}", "severity": "hard"},
            {"gate_id": "P197_NO_REPLAY_OR_PROMOTION", "gate_pass": 1, "evidence": "strategy_replay=0; test_replay=0; promotion=0; paper_live=0", "severity": "hard"},
        ]
    )


def build_acceptance(contract: pd.DataFrame, audit: pd.DataFrame, matrix: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates.loc[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(int).sum()) if not hard.empty else 0
    ready = int(matrix["ready_for_phase198_search"].astype(int).sum()) if not matrix.empty else 0
    return pd.DataFrame(
        [
            ("phase197_feature_contract_rows", int(len(contract)), "Non-receive-flow feature family rows precommitted"),
            ("phase197_availability_audit_rows", int(len(audit)), "Feature/split availability rows"),
            ("phase197_ready_feature_families", ready, "Feature families ready for future train/validation search"),
            ("phase197_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase197_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase197_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase197_non_receive_flow_feature_precommit_complete", int(len(hard) > 0 and hard_pass == len(hard)), "1 means Phase197 completed"),
            ("phase197_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase197_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase197_promotion_allowed", 0, "No promotion opened"),
            ("phase197_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase197_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase197_next_best_action", "run_phase198_non_receive_flow_context_model_search_no_test", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase197 Non-Receive-Flow Feature Expansion Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase197 responds to the Phase196 no-survivor result by precommitting broader context features.",
        "It is not a strategy replay and it does not use the untouched test split.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase197_non_receive_flow_feature_expansion_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase197(phase176_dir: Path, phase181_dir: Path, phase196_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase196 = read_csv(phase196_dir / "phase196_expanded_feature_model_acceptance_summary.csv")
    feature_inventory = read_csv(phase176_dir / "phase176_feature_partition_inventory.csv")
    label_inventory = read_csv(phase181_dir / "phase181_label_partition_inventory.csv")
    frame, partition_use = build_model_frame(feature_inventory, label_inventory)
    frame = derive_context_features(frame)
    split_use = split_use_audit(partition_use)
    contract = feature_contract()
    audit = availability_audit(frame, contract)
    matrix = candidate_matrix(contract, audit)
    gates = build_gates(phase196, split_use, contract, audit, matrix)
    acceptance = build_acceptance(contract, audit, matrix, gates)

    contract.to_csv(output_dir / "phase197_non_receive_flow_feature_contract.csv", index=False)
    audit.to_csv(output_dir / "phase197_feature_availability_audit.csv", index=False)
    matrix.to_csv(output_dir / "phase197_phase198_candidate_matrix.csv", index=False)
    split_use.to_csv(output_dir / "phase197_partition_use_audit.csv", index=False)
    gates.to_csv(output_dir / "phase197_non_receive_flow_feature_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase197_non_receive_flow_feature_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Phase198 Candidate Matrix": matrix,
            "Feature Availability Audit": audit,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase197_non_receive_flow_feature_expansion_precommit_no_test",
        **reproducibility_fields(
            artifact_id="phase197_non_receive_flow_feature_expansion_precommit",
            generated_utc=generated,
            inputs={
                "phase176_feature_inventory": str(phase176_dir / "phase176_feature_partition_inventory.csv"),
                "phase181_label_inventory": str(phase181_dir / "phase181_label_partition_inventory.csv"),
                "phase196_acceptance": str(phase196_dir / "phase196_expanded_feature_model_acceptance_summary.csv"),
            },
            parameters={
                "precommit_scope": "non_receive_flow_context_feature_families",
                "excluded_role": "test_untouched",
                "strategy_replay_allowed": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "feature_contract": str(output_dir / "phase197_non_receive_flow_feature_contract.csv"),
                "availability_audit": str(output_dir / "phase197_feature_availability_audit.csv"),
                "candidate_matrix": str(output_dir / "phase197_phase198_candidate_matrix.csv"),
                "partition_use": str(output_dir / "phase197_partition_use_audit.csv"),
                "gate_evaluation": str(output_dir / "phase197_non_receive_flow_feature_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase197_non_receive_flow_feature_acceptance_summary.csv"),
                "report": str(output_dir / "phase197_non_receive_flow_feature_expansion_precommit_report.md"),
            },
            scenario_ids="phase197_non_receive_flow_feature_expansion_precommit_no_test",
            cost_model_version="not_applicable_no_strategy_replay",
            latency_model_version="not_applicable_no_strategy_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase197_non_receive_flow_feature_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase176-dir", type=Path, default=DEFAULT_PHASE176_DIR)
    parser.add_argument("--phase181-dir", type=Path, default=DEFAULT_PHASE181_DIR)
    parser.add_argument("--phase196-dir", type=Path, default=DEFAULT_PHASE196_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase197(args.phase176_dir, args.phase181_dir, args.phase196_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
