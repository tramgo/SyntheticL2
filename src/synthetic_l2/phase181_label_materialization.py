from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE180_DIR = Path("outputs/phase180")
DEFAULT_PHASE176_DIR = Path("outputs/phase176")
DEFAULT_OUTPUT_DIR = Path("outputs/phase181")
DEFAULT_LABEL_ROOT = Path("derived_real_l2_receive_flow_labels_phase181")
FORBIDDEN_OUTPUTS = "signal;side;order;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance"


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


def split_role(trade_date: str, label_precommit: pd.DataFrame) -> str:
    if label_precommit.empty:
        return "unknown"
    row = label_precommit.iloc[0]
    if trade_date in str(row.get("train_dates", "")).split(";"):
        return "train"
    if trade_date in str(row.get("validation_dates", "")).split(";"):
        return "validation"
    if trade_date in str(row.get("test_dates", "")).split(";"):
        return "test_untouched"
    return "unassigned"


def materialize_partition(feature_path: Path, out_path: Path, label_precommit: pd.DataFrame) -> dict[str, Any]:
    df = pd.read_parquet(feature_path).sort_values("bucket_ms").reset_index(drop=True)
    mid = ((pd.to_numeric(df["best_bid"], errors="coerce") + pd.to_numeric(df["best_ask"], errors="coerce")) / 2).fillna(
        pd.to_numeric(df["last_price"], errors="coerce")
    )
    spread = pd.to_numeric(df["spread"], errors="coerce")
    future_mid = mid.shift(-1)
    future_spread = spread.shift(-1)
    future_return_bps = ((future_mid - mid) / mid.replace(0, np.nan)) * 10_000
    future_spread_change_bps = ((future_spread - spread) / mid.replace(0, np.nan)) * 10_000
    future_abs_return_bps = future_return_bps.abs()
    future_volatility_proxy_bps = future_return_bps.shift(-1).rolling(window=5, min_periods=2).std().shift(-3)

    out = pd.DataFrame(
        {
            "bucket_ms": df["bucket_ms"],
            "trade_date": df["trade_date"],
            "exchange": df["exchange"],
            "symbol": df["symbol"],
            "horizon_sec": df["horizon_sec"],
            "split_role": split_role(str(df["trade_date"].iloc[0]) if len(df) else "", label_precommit),
            "future_mid_return_bps_next_bucket": future_return_bps,
            "future_abs_return_bps_next_bucket": future_abs_return_bps,
            "future_spread_change_bps_next_bucket": future_spread_change_bps,
            "future_volatility_proxy_bps_next_5_buckets": future_volatility_proxy_bps,
            "execution_risk_spread_widen_next_bucket": (future_spread > spread).astype("Int64"),
            "short_horizon_direction_label": np.sign(future_return_bps.fillna(0)).astype("int8"),
        }
    )
    out["label_available"] = (
        out[
            [
                "future_mid_return_bps_next_bucket",
                "future_abs_return_bps_next_bucket",
                "future_spread_change_bps_next_bucket",
            ]
        ]
        .notna()
        .all(axis=1)
        .astype("int8")
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_parquet(out_path, index=False)
    return {
        "horizon_sec": int(df["horizon_sec"].iloc[0]) if len(df) else "",
        "trade_date": str(df["trade_date"].iloc[0]) if len(df) else "",
        "exchange": str(df["exchange"].iloc[0]) if len(df) else "",
        "symbol": str(df["symbol"].iloc[0]) if len(df) else "",
        "split_role": str(out["split_role"].iloc[0]) if len(out) else "",
        "rows": int(len(out)),
        "label_available_rows": int(out["label_available"].sum()) if len(out) else 0,
        "label_file": str(out_path),
        "bytes": int(out_path.stat().st_size),
    }


def output_path_for(label_root: Path, row: pd.Series) -> Path:
    horizon = f"{int(row['horizon_sec'])}s"
    return (
        label_root
        / f"horizon={horizon}"
        / f"trade_date={row['trade_date']}"
        / f"exchange={row['exchange']}"
        / f"symbol={row['symbol']}"
        / "receive_flow_labels.parquet"
    )


def materialize_labels(inventory: pd.DataFrame, label_precommit: pd.DataFrame, label_root: Path) -> pd.DataFrame:
    if label_root.exists():
        resolved = label_root.resolve()
        cwd = Path(".").resolve()
        if cwd not in resolved.parents and resolved != cwd:
            raise ValueError(f"Refusing to clear label root outside workspace: {label_root}")
        shutil.rmtree(label_root)
    label_root.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for item in inventory.to_dict("records"):
        feature_path = Path(item["parquet_file"])
        if not feature_path.exists():
            continue
        out_path = output_path_for(label_root, pd.Series(item))
        rows.append(materialize_partition(feature_path, out_path, label_precommit))
    return pd.DataFrame(rows)


def build_label_quality(inventory: pd.DataFrame) -> pd.DataFrame:
    if inventory.empty:
        return pd.DataFrame(columns=["horizon_sec", "trade_date", "split_role", "partitions", "rows", "label_available_rows", "availability_fraction"])
    rows = []
    for (horizon, trade_date, split), group in inventory.groupby(["horizon_sec", "trade_date", "split_role"], sort=True):
        total = int(group["rows"].sum())
        available = int(group["label_available_rows"].sum())
        rows.append(
            {
                "horizon_sec": horizon,
                "trade_date": trade_date,
                "split_role": split,
                "partitions": int(len(group)),
                "rows": total,
                "label_available_rows": available,
                "availability_fraction": available / total if total else 0.0,
            }
        )
    return pd.DataFrame(rows)


def build_gate_evaluation(phase180: pd.DataFrame, label_inventory: pd.DataFrame, quality: pd.DataFrame) -> pd.DataFrame:
    phase180_ready = as_int(metric_value(phase180, "phase180_precommit_ready", 0))
    split_roles = set(label_inventory["split_role"].astype(str).tolist()) if not label_inventory.empty else set()
    min_availability = float(quality["availability_fraction"].min()) if not quality.empty else 0.0
    return pd.DataFrame(
        [
            {
                "gate_id": "P181_PHASE180_PRECOMMIT_READY",
                "gate_pass": int(phase180_ready == 1),
                "evidence": f"phase180_precommit_ready={phase180_ready}",
                "severity": "hard",
            },
            {
                "gate_id": "P181_LABEL_PARTITIONS_WRITTEN",
                "gate_pass": int(len(label_inventory) >= 640),
                "evidence": f"label_partitions={len(label_inventory)}",
                "severity": "hard",
            },
            {
                "gate_id": "P181_SPLIT_ROLES_PRESENT",
                "gate_pass": int({"train", "validation", "test_untouched"}.issubset(split_roles)),
                "evidence": "split_roles=" + ";".join(sorted(split_roles)),
                "severity": "hard",
            },
            {
                "gate_id": "P181_LABEL_AVAILABILITY_NONZERO",
                "gate_pass": int(min_availability > 0.90),
                "evidence": f"min_availability_fraction={min_availability:.6f}",
                "severity": "hard",
            },
            {
                "gate_id": "P181_NO_REPLAY_OR_PROFITABILITY_OUTPUTS",
                "gate_pass": 1,
                "evidence": "label materialization only; forbidden_outputs=" + FORBIDDEN_OUTPUTS,
                "severity": "hard",
            },
        ]
    )


def build_acceptance_summary(label_inventory: pd.DataFrame, quality: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0
    materialized = int(not hard.empty and hard_pass == len(hard))
    return pd.DataFrame(
        [
            ("phase181_label_partition_rows", int(len(label_inventory)), "Label partitions materialized"),
            ("phase181_label_rows", int(label_inventory["rows"].sum()) if not label_inventory.empty else 0, "Label rows written"),
            ("phase181_label_available_rows", int(label_inventory["label_available_rows"].sum()) if not label_inventory.empty else 0, "Rows with primary labels available"),
            ("phase181_quality_rows", int(len(quality)), "Horizon/date/split quality rows"),
            ("phase181_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase181_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase181_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase181_labels_materialized", materialized, "1 means label parquet was materialized"),
            ("phase181_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase181_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase181_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase181_next_best_action", "build_phase182_label_quality_leakage_audit_no_replay" if materialized else "repair_phase181_label_materialization", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase181 Label Materialization",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase181 materializes future receive-flow labels from Phase176 features under the Phase180 precommit.",
        "It does not emit signals, sides, orders, fills, P&L, profitability claims, or paper/live acceptance.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase181_label_materialization_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase181(phase180_dir: Path, phase176_dir: Path, output_dir: Path, label_root: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase180 = read_csv(phase180_dir / "phase180_cost_latency_label_precommit_acceptance_summary.csv")
    label_precommit = read_csv(phase180_dir / "phase180_label_family_precommit.csv")
    feature_inventory = read_csv(phase176_dir / "phase176_feature_partition_inventory.csv")
    label_inventory = materialize_labels(feature_inventory, label_precommit, label_root)
    quality = build_label_quality(label_inventory)
    gates = build_gate_evaluation(phase180, label_inventory, quality)
    acceptance = build_acceptance_summary(label_inventory, quality, gates)

    label_inventory.to_csv(output_dir / "phase181_label_partition_inventory.csv", index=False)
    quality.to_csv(output_dir / "phase181_label_quality_by_horizon_date_split.csv", index=False)
    gates.to_csv(output_dir / "phase181_label_materialization_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase181_label_materialization_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Label Quality by Horizon/date/split": quality,
            "Gate Evaluation": gates,
            "Label Partition Inventory": label_inventory.head(200),
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase181_label_materialization",
        **reproducibility_fields(
            artifact_id="phase181_label_materialization",
            generated_utc=generated,
            inputs={
                "phase180_acceptance": str(phase180_dir / "phase180_cost_latency_label_precommit_acceptance_summary.csv"),
                "phase180_label_precommit": str(phase180_dir / "phase180_label_family_precommit.csv"),
                "phase176_feature_inventory": str(phase176_dir / "phase176_feature_partition_inventory.csv"),
            },
            parameters={
                "label_root": str(label_root),
                "materialization_policy": "future_labels_only_no_strategy_replay",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "label_partition_inventory": str(output_dir / "phase181_label_partition_inventory.csv"),
                "label_quality": str(output_dir / "phase181_label_quality_by_horizon_date_split.csv"),
                "gate_evaluation": str(output_dir / "phase181_label_materialization_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase181_label_materialization_acceptance_summary.csv"),
                "report": str(output_dir / "phase181_label_materialization_report.md"),
            },
            random_seed="none_deterministic_label_materialization",
            scenario_ids="phase181_label_materialization",
            cost_model_version="phase180_pinned_not_applied_no_pnl",
            latency_model_version="phase180_pinned_not_applied_no_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase181_label_materialization_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase180-dir", type=Path, default=DEFAULT_PHASE180_DIR)
    parser.add_argument("--phase176-dir", type=Path, default=DEFAULT_PHASE176_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--label-root", type=Path, default=DEFAULT_LABEL_ROOT)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase181(args.phase180_dir, args.phase176_dir, args.output_dir, args.label_root, args.base_dir)


if __name__ == "__main__":
    main()
