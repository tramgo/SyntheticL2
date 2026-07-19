from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase129")
DEFAULT_PHASE128_DIR = Path("outputs/phase128")
DEFAULT_PHASE117_DIR = Path("outputs/phase117")
FORBIDDEN_SIGNALS = "buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def read_metric_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["metric", "value", "description"])
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    value = rows.iloc[0]
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def numeric(frame: pd.DataFrame, column: str, default: float = 0.0) -> pd.Series:
    if column not in frame.columns:
        return pd.Series([default for _ in range(len(frame))], index=frame.index, dtype="float64")
    return pd.to_numeric(frame[column], errors="coerce").fillna(default)


def q(frame: pd.DataFrame, column: str, quantile: float, default: float = 0.0) -> float:
    series = numeric(frame, column).dropna()
    if series.empty:
        return default
    return float(series.quantile(quantile))


def build_thresholds(snapshot: pd.DataFrame) -> dict[str, float]:
    return {
        "feed_imperfection_median": q(snapshot, "feed_imperfection_rate", 0.50),
        "p90_spread_median": q(snapshot, "p90_spread_bps", 0.50),
        "p90_spread_q75": q(snapshot, "p90_spread_bps", 0.75),
        "l1_depth_median": q(snapshot, "mean_l1_depth", 0.50),
        "l5_depth_median": q(snapshot, "mean_l5_depth", 0.50),
        "one_tick_return_std_median": q(snapshot, "one_tick_return_std", 0.50),
        "passive_min_adverse_rate_median": q(snapshot, "passive_min_adverse_rate", 0.50),
        "passive_min_adverse_rate_q75": q(snapshot, "passive_min_adverse_rate", 0.75),
    }


def build_label_matrix(snapshot: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if snapshot.empty:
        return pd.DataFrame(), pd.DataFrame()
    frame = snapshot.copy()
    for column in [
        "candidate_generation_allowed",
        "strategy_replay_allowed",
        "realism_review_flag",
        "regime_realism_risk_label",
        "opportunity_abstention_label",
        "cost_toxicity_label",
    ]:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0).astype(int)

    thresholds = build_thresholds(frame)
    stable_mask = (
        numeric(frame, "feed_imperfection_rate").le(thresholds["feed_imperfection_median"])
        & numeric(frame, "p90_spread_bps").le(thresholds["p90_spread_q75"])
        & frame["regime_realism_risk_label"].eq(0)
        & frame["realism_review_flag"].eq(0)
    )
    liquidity_mask = (
        numeric(frame, "mean_l1_depth").ge(thresholds["l1_depth_median"])
        & numeric(frame, "mean_l5_depth").ge(thresholds["l5_depth_median"])
        & numeric(frame, "one_tick_return_std").ge(thresholds["one_tick_return_std_median"])
        & numeric(frame, "p90_spread_bps").ge(thresholds["p90_spread_median"])
    )
    adverse = numeric(frame, "passive_min_adverse_rate")
    spread = numeric(frame, "p90_spread_bps")
    cost_bucket = pd.Series("broad_cost_toxic_no_adverse_touch", index=frame.index, dtype="object")
    cost_bucket = cost_bucket.mask(adverse.gt(thresholds["passive_min_adverse_rate_median"]), "adverse_touch_cost_toxic")
    cost_bucket = cost_bucket.mask(
        adverse.ge(thresholds["passive_min_adverse_rate_q75"]) & spread.ge(thresholds["p90_spread_median"]),
        "high_adverse_wide_spread_cost_toxic",
    )

    frame["p129_regime_stability_label"] = stable_mask.astype(int)
    frame["p129_liquidity_opportunity_label"] = liquidity_mask.astype(int)
    frame["p129_cost_toxicity_refinement_bucket"] = cost_bucket
    frame["p129_cost_toxicity_refinement_label"] = cost_bucket.ne("broad_cost_toxic_no_adverse_touch").astype(int)
    frame["phase129_scope"] = "allowed_context_no_replay_label_matrix"
    frame["strategy_replay_allowed"] = 0
    frame["forbidden_outputs"] = FORBIDDEN_SIGNALS
    frame["label_source"] = frame.get("label_source", "").astype(str) + ";phase128_design_specs"

    threshold_rows = [{"threshold_name": name, "value": value} for name, value in thresholds.items()]
    threshold_rows.extend(
        [
            {
                "threshold_name": "regime_stability_rule",
                "value": "feed_imperfection<=median and p90_spread<=q75 and regime_realism_risk_label=0 and realism_review_flag=0",
            },
            {
                "threshold_name": "liquidity_opportunity_rule",
                "value": "l1_depth>=median and l5_depth>=median and one_tick_return_std>=median and p90_spread>=median",
            },
            {
                "threshold_name": "cost_toxicity_refinement_rule",
                "value": "bucket broad universal cost-toxicity using passive_min_adverse_rate and p90_spread",
            },
        ]
    )
    thresholds_frame = pd.DataFrame(threshold_rows)

    keep = [
        "trade_month",
        "symbol",
        "priority_bucket",
        "realism_review_flag",
        "candidate_generation_allowed",
        "rows_scanned",
        "feed_imperfection_rate",
        "median_spread_bps",
        "p90_spread_bps",
        "mean_l1_depth",
        "mean_l5_depth",
        "one_tick_return_std",
        "passive_min_adverse_rate",
        "passive_max_cost_clearing_rate",
        "cost_toxicity_label",
        "regime_realism_risk_label",
        "opportunity_abstention_label",
        "p129_regime_stability_label",
        "p129_liquidity_opportunity_label",
        "p129_cost_toxicity_refinement_label",
        "p129_cost_toxicity_refinement_bucket",
        "phase129_scope",
        "strategy_replay_allowed",
        "forbidden_outputs",
        "label_source",
    ]
    return frame[[column for column in keep if column in frame.columns]].sort_values(["trade_month", "symbol"], kind="mergesort"), thresholds_frame


def build_label_summary(matrix: pd.DataFrame) -> pd.DataFrame:
    if matrix.empty:
        return pd.DataFrame()
    rows = []
    for label in [
        "p129_regime_stability_label",
        "p129_liquidity_opportunity_label",
        "p129_cost_toxicity_refinement_label",
    ]:
        counts = matrix[label].value_counts(dropna=False).to_dict()
        rows.append(
            {
                "label_id": label,
                "rows": int(len(matrix)),
                "positive_rows": int(matrix[label].sum()),
                "negative_rows": int(len(matrix) - matrix[label].sum()),
                "positive_rate": float(matrix[label].mean()),
                "has_class_variation": int(matrix[label].nunique(dropna=False) > 1),
                "strategy_replay_allowed": 0,
                "value_counts": json.dumps({str(key): int(value) for key, value in counts.items()}, sort_keys=True),
            }
        )
    bucket_counts = matrix["p129_cost_toxicity_refinement_bucket"].value_counts(dropna=False).to_dict()
    rows.append(
        {
            "label_id": "p129_cost_toxicity_refinement_bucket",
            "rows": int(len(matrix)),
            "positive_rows": "",
            "negative_rows": "",
            "positive_rate": "",
            "has_class_variation": int(len(bucket_counts) > 1),
            "strategy_replay_allowed": 0,
            "value_counts": json.dumps({str(key): int(value) for key, value in bucket_counts.items()}, sort_keys=True),
        }
    )
    return pd.DataFrame(rows)


def build_blocked_audit(blocked: pd.DataFrame, matrix: pd.DataFrame) -> pd.DataFrame:
    if blocked.empty:
        return pd.DataFrame()
    blocked_keys = set(zip(blocked["trade_month"].astype(str), blocked["symbol"].astype(str)))
    matrix_keys = set(zip(matrix["trade_month"].astype(str), matrix["symbol"].astype(str))) if not matrix.empty else set()
    overlap = sorted(blocked_keys & matrix_keys)
    return pd.DataFrame(
        [
            {
                "audit_id": "P129_BLOCKED_CONTEXT_OVERLAP",
                "blocked_rows": int(len(blocked)),
                "label_matrix_rows": int(len(matrix)),
                "overlap_rows": int(len(overlap)),
                "overlap_sample": ";".join([f"{month}:{symbol}" for month, symbol in overlap[:10]]),
                "gate_pass": int(len(overlap) == 0),
            }
        ]
    )


def build_guardrails() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "guardrail_id": "P129_ALLOWED_CONTEXTS_ONLY",
                "requirement": "The label matrix may contain only rows from the Phase128 allowed feature snapshot.",
                "enforcement": "Rows inherit candidate_generation_allowed=1 and are audited against the blocked exclusion ledger.",
            },
            {
                "guardrail_id": "P129_LABELS_NOT_SIGNALS",
                "requirement": "Labels describe context diagnostics, not orders, sides, fills, or P&L.",
                "enforcement": f"forbidden_outputs={FORBIDDEN_SIGNALS}",
            },
            {
                "guardrail_id": "P129_CLASS_VARIATION_REQUIRED",
                "requirement": "Every binary Phase129 diagnostic label should have class variation before future baseline modeling.",
                "enforcement": "label_summary records has_class_variation for all emitted labels.",
            },
            {
                "guardrail_id": "P129_NO_REPLAY",
                "requirement": "Strategy replay remains closed.",
                "enforcement": "strategy_replay_allowed=0 across label matrix and summaries.",
            },
        ]
    )


def build_gate_evaluation(matrix: pd.DataFrame, label_summary: pd.DataFrame, blocked_audit: pd.DataFrame, phase117: pd.DataFrame) -> pd.DataFrame:
    ready_days = as_int(metric_value(phase117, "phase117_current_ready_real_anchor_days"))
    days_needed = as_int(metric_value(phase117, "phase117_additional_days_needed_for_min"))
    binary = label_summary[label_summary["label_id"].astype(str).str.endswith("_label")] if not label_summary.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            {"gate_id": "P129_LABEL_MATRIX_EXISTS", "gate_pass": int(not matrix.empty), "evidence": f"label_matrix_rows={len(matrix)}"},
            {
                "gate_id": "P129_ALL_ROWS_ALLOWED",
                "gate_pass": int(not matrix.empty and matrix["candidate_generation_allowed"].eq(1).all()),
                "evidence": "candidate_generation_allowed=1 for every matrix row",
            },
            {
                "gate_id": "P129_BLOCKED_CONTEXTS_EXCLUDED",
                "gate_pass": int(not blocked_audit.empty and blocked_audit["gate_pass"].astype(int).all()),
                "evidence": f"overlap_rows={int(blocked_audit['overlap_rows'].iloc[0]) if not blocked_audit.empty else 'unknown'}",
            },
            {
                "gate_id": "P129_BINARY_LABEL_CLASS_VARIATION",
                "gate_pass": int(not binary.empty and binary["has_class_variation"].astype(int).all()),
                "evidence": f"binary_labels_checked={len(binary)}",
            },
            {
                "gate_id": "P129_NO_REPLAY",
                "gate_pass": int(not matrix.empty and matrix["strategy_replay_allowed"].sum() == 0),
                "evidence": "strategy_replay_allowed remains 0",
            },
            {
                "gate_id": "P129_REAL_ANCHOR_STILL_PRIMARY",
                "gate_pass": int(ready_days < 5 and days_needed > 0),
                "evidence": f"ready_real_anchor_days={ready_days}; days_needed={days_needed}",
            },
        ]
    )


def build_acceptance_summary(matrix: pd.DataFrame, label_summary: pd.DataFrame, gates: pd.DataFrame, phase117: pd.DataFrame) -> pd.DataFrame:
    ready_days = as_int(metric_value(phase117, "phase117_current_ready_real_anchor_days"))
    days_needed = as_int(metric_value(phase117, "phase117_additional_days_needed_for_min"))
    return pd.DataFrame(
        [
            ("phase129_label_matrix_rows", int(len(matrix)), "Allowed-context no-replay label matrix rows"),
            ("phase129_symbols", int(matrix["symbol"].nunique()) if not matrix.empty else 0, "Symbols represented in Phase129"),
            ("phase129_months", int(matrix["trade_month"].nunique()) if not matrix.empty else 0, "Months represented in Phase129"),
            ("phase129_label_summary_rows", int(len(label_summary)), "Label summary rows emitted"),
            ("phase129_binary_labels_with_variation", int(label_summary[label_summary["label_id"].astype(str).str.endswith("_label")]["has_class_variation"].astype(int).sum()) if not label_summary.empty else 0, "Binary diagnostic labels with both classes"),
            ("phase129_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase129_all_gates_pass", int(gates["gate_pass"].astype(bool).all()) if not gates.empty else 0, "1 means Phase129 obeys no-replay guardrails"),
            ("phase129_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase129_current_ready_real_anchor_days", ready_days, "Real anchor days currently ready from Phase117"),
            ("phase129_additional_real_anchor_days_needed", days_needed, "Additional real anchor days needed before replay unlock"),
            ("phase129_next_best_action", "fit_phase130_no_replay_diagnostic_baselines_or_continue_real_anchor_acquisition", "Recommended next milestone"),
            ("phase129_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model retained for audit continuity"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase129 Allowed-Context Label Matrix",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase129 materializes the Phase128 no-replay label designs into a diagnostic label matrix.",
        "The labels are context labels only: no buy/sell side, no order/fill simulation, no P&L replay, and no profitability claim.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase129_allowed_context_label_matrix_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase129(base_dir: Path, output_dir: Path, phase128_dir: Path, phase117_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    snapshot = read_csv(base_dir / phase128_dir / "allowed_context_feature_snapshot.csv")
    blocked = read_csv(base_dir / phase128_dir / "blocked_context_exclusion_ledger.csv")
    phase117 = read_metric_table(base_dir / phase117_dir / "phase117_real_anchor_acquisition_acceptance_summary.csv")

    matrix, thresholds = build_label_matrix(snapshot)
    label_summary = build_label_summary(matrix)
    blocked_audit = build_blocked_audit(blocked, matrix)
    guardrails = build_guardrails()
    gates = build_gate_evaluation(matrix, label_summary, blocked_audit, phase117)
    acceptance = build_acceptance_summary(matrix, label_summary, gates, phase117)

    matrix.to_csv(output_dir / "allowed_context_label_matrix.csv", index=False)
    thresholds.to_csv(output_dir / "label_thresholds_and_rules.csv", index=False)
    label_summary.to_csv(output_dir / "label_summary.csv", index=False)
    blocked_audit.to_csv(output_dir / "blocked_context_overlap_audit.csv", index=False)
    guardrails.to_csv(output_dir / "label_matrix_guardrails.csv", index=False)
    gates.to_csv(output_dir / "label_matrix_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase129_allowed_context_label_matrix_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Label Summary": label_summary,
            "Thresholds and Rules": thresholds,
            "Label Matrix Sample": matrix.head(50),
            "Blocked Context Audit": blocked_audit,
            "Guardrails": guardrails,
            "Gate Evaluation": gates,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase129_allowed_context_label_matrix",
        "strategy_replay_allowed": 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase129",
            generated_utc=generated_utc,
            inputs={
                "phase128_allowed_feature_snapshot": str(phase128_dir / "allowed_context_feature_snapshot.csv"),
                "phase128_blocked_exclusion": str(phase128_dir / "blocked_context_exclusion_ledger.csv"),
                "phase117_acceptance": str(phase117_dir / "phase117_real_anchor_acquisition_acceptance_summary.csv"),
            },
            parameters={
                "matrix_scope": "allowed_context_no_replay_labels",
                "blocked_policy": "zero_overlap_required",
                "replay_policy": "closed",
                "forbidden_outputs": FORBIDDEN_SIGNALS,
            },
            outputs={
                "label_matrix": str(output_dir / "allowed_context_label_matrix.csv"),
                "thresholds": str(output_dir / "label_thresholds_and_rules.csv"),
                "label_summary": str(output_dir / "label_summary.csv"),
                "blocked_audit": str(output_dir / "blocked_context_overlap_audit.csv"),
                "guardrails": str(output_dir / "label_matrix_guardrails.csv"),
                "gates": str(output_dir / "label_matrix_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase129_allowed_context_label_matrix_acceptance_summary.csv"),
                "report": str(output_dir / "phase129_allowed_context_label_matrix_report.md"),
                "manifest": str(output_dir / "phase129_allowed_context_label_matrix_manifest.json"),
            },
            random_seed="none_deterministic_label_matrix",
            scenario_ids="phase129_allowed_context_no_replay_label_matrix",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_label_matrix",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase129_allowed_context_label_matrix_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase129 allowed-context no-replay label matrix.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--phase128-dir", type=Path, default=DEFAULT_PHASE128_DIR)
    parser.add_argument("--phase117-dir", type=Path, default=DEFAULT_PHASE117_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase129(base_dir=args.base_dir, output_dir=args.output_dir, phase128_dir=args.phase128_dir, phase117_dir=args.phase117_dir)


if __name__ == "__main__":
    main()
