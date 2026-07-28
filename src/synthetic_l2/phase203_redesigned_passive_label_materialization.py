from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE119_DIR = Path("outputs/phase120/P120_LABEL_STAGE_01_MIN_BREADTH/phase119")
DEFAULT_PHASE202_DIR = Path("outputs/phase202")
DEFAULT_OUTPUT_DIR = Path("outputs/phase203")
FORBIDDEN_OUTPUTS = "strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim"


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


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def contains_text(value: Any, needle: str) -> bool:
    return needle.lower() in str(value).lower()


def materialize_redesigned_labels(candidates: pd.DataFrame) -> pd.DataFrame:
    if candidates.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for _, row in candidates.iterrows():
        candidate_id = str(row.get("candidate_id", ""))
        symbols = as_int(row.get("symbols", 0))
        trade_dates = as_int(row.get("trade_dates", 0))
        baseline_adverse = as_float(row.get("baseline_adverse_selection_rate", 1.0), 1.0)
        replenishment_adverse = as_float(row.get("replenishment_adverse_selection_rate", 1.0), 1.0)
        spread_adverse = as_float(row.get("spread_adverse_direction_rate", 1.0), 1.0)
        mean_replenishment = as_float(row.get("mean_replenishment_ratio", 0.0))
        mean_spread_change_bps = as_float(row.get("mean_spread_change_bps", 0.0))
        mean_abs_recent_return_bps = as_float(row.get("mean_abs_recent_return_bps", 999.0), 999.0)
        label_quality_score = as_float(row.get("label_quality_score", 0.0))
        spread_transition = str(row.get("spread_transition_type", ""))
        replenishment_bucket = str(row.get("replenishment_bucket", ""))
        failure_reason = str(row.get("failure_reason", ""))

        queue_recovery_persistence = int(
            mean_replenishment >= 1.0
            and contains_text(replenishment_bucket, "rebuilt")
            and contains_text(spread_transition, "compression")
            and mean_spread_change_bps <= 0.0
        )
        toxicity_abstention_pass = int(
            baseline_adverse <= 0.75
            and replenishment_adverse <= 0.75
            and spread_adverse <= 0.75
        )
        symbol_month_stability_pass = int(symbols >= 8 and trade_dates >= 4 and label_quality_score >= 1.0)
        spread_compression_cancel_guard = int(
            contains_text(spread_transition, "compression")
            and mean_spread_change_bps <= 0.0
            and mean_abs_recent_return_bps <= 10.0
            and spread_adverse <= 0.75
        )
        redesigned_candidate_pass = int(
            queue_recovery_persistence == 1
            and toxicity_abstention_pass == 1
            and symbol_month_stability_pass == 1
            and spread_compression_cancel_guard == 1
        )
        rows.append(
            {
                "candidate_id": candidate_id,
                "feature_family_id": row.get("feature_family_id", ""),
                "base_strategy_id": row.get("base_strategy_id", ""),
                "side": row.get("side", ""),
                "spread_bucket": row.get("spread_bucket", ""),
                "imbalance_bucket": row.get("imbalance_bucket", ""),
                "replenishment_bucket": replenishment_bucket,
                "spread_transition_type": spread_transition,
                "recent_return_bucket": row.get("recent_return_bucket", ""),
                "symbols": symbols,
                "trade_dates": trade_dates,
                "inferred_touches": as_int(row.get("inferred_touches", 0)),
                "signal_rows": as_int(row.get("signal_rows", 0)),
                "baseline_adverse_selection_rate": baseline_adverse,
                "replenishment_adverse_selection_rate": replenishment_adverse,
                "spread_adverse_direction_rate": spread_adverse,
                "mean_replenishment_ratio": mean_replenishment,
                "mean_spread_change_bps": mean_spread_change_bps,
                "mean_abs_recent_return_bps": mean_abs_recent_return_bps,
                "label_quality_score": label_quality_score,
                "phase201_failure_reason": failure_reason,
                "p203_queue_recovery_persistence_label": queue_recovery_persistence,
                "p203_toxicity_abstention_filter_label": toxicity_abstention_pass,
                "p203_symbol_month_stability_label": symbol_month_stability_pass,
                "p203_spread_compression_cancel_guard_label": spread_compression_cancel_guard,
                "p203_redesigned_candidate_pass": redesigned_candidate_pass,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            }
        )
    return pd.DataFrame(rows)


def build_feature_summary(labels: pd.DataFrame) -> pd.DataFrame:
    if labels.empty:
        return pd.DataFrame()
    feature_cols = [
        "p203_queue_recovery_persistence_label",
        "p203_toxicity_abstention_filter_label",
        "p203_symbol_month_stability_label",
        "p203_spread_compression_cancel_guard_label",
        "p203_redesigned_candidate_pass",
    ]
    rows: list[dict[str, Any]] = []
    for col in feature_cols:
        pass_rows = as_int(labels[col].sum())
        rows.append(
            {
                "label_id": col,
                "candidate_rows": len(labels),
                "pass_rows": pass_rows,
                "pass_fraction": pass_rows / len(labels) if len(labels) else 0.0,
                "max_symbols_among_pass": as_int(labels.loc[labels[col].eq(1), "symbols"].max(), 0) if pass_rows else 0,
                "max_trade_dates_among_pass": as_int(labels.loc[labels[col].eq(1), "trade_dates"].max(), 0) if pass_rows else 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            }
        )
    return pd.DataFrame(rows)


def build_symbol_breadth_audit(labels: pd.DataFrame) -> pd.DataFrame:
    if labels.empty:
        return pd.DataFrame()
    grouped = (
        labels.groupby(["feature_family_id", "base_strategy_id"], dropna=False)
        .agg(
            candidate_rows=("candidate_id", "count"),
            max_symbols=("symbols", "max"),
            max_trade_dates=("trade_dates", "max"),
            mean_label_quality_score=("label_quality_score", "mean"),
            redesigned_pass_rows=("p203_redesigned_candidate_pass", "sum"),
        )
        .reset_index()
    )
    grouped["symbol_month_stability_requirement_met"] = (
        grouped["max_symbols"].ge(8) & grouped["max_trade_dates"].ge(4)
    ).astype(int)
    grouped["strategy_replay_allowed"] = 0
    grouped["test_replay_allowed_next"] = 0
    return grouped


def build_adverse_selection_audit(labels: pd.DataFrame) -> pd.DataFrame:
    if labels.empty:
        return pd.DataFrame()
    return pd.DataFrame(
        [
            {
                "audit_id": "P203_ADVERSE_SELECTION_VS_STAGE01",
                "candidate_rows": len(labels),
                "phase201_adverse_failure_rows": int(labels["phase201_failure_reason"].astype(str).str.contains("adverse_selection_gate_failed", regex=False).sum()),
                "toxicity_abstention_pass_rows": as_int(labels["p203_toxicity_abstention_filter_label"].sum()),
                "min_baseline_adverse_selection_rate": as_float(labels["baseline_adverse_selection_rate"].min(), 0.0),
                "min_replenishment_adverse_selection_rate": as_float(labels["replenishment_adverse_selection_rate"].min(), 0.0),
                "min_spread_adverse_direction_rate": as_float(labels["spread_adverse_direction_rate"].min(), 0.0),
                "adverse_selection_ceiling": 0.75,
                "adverse_selection_ceiling_met": int(as_int(labels["p203_toxicity_abstention_filter_label"].sum()) > 0),
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            }
        ]
    )


def build_gate_evaluation(
    phase202: pd.DataFrame,
    action_plan: pd.DataFrame,
    labels: pd.DataFrame,
    feature_summary: pd.DataFrame,
    breadth_audit: pd.DataFrame,
    adverse_audit: pd.DataFrame,
) -> pd.DataFrame:
    complete202 = as_int(metric_value(phase202, "phase202_passive_feature_redesign_precommit_complete", 0))
    strategy_replay = as_int(labels["strategy_replay_allowed"].max(), 0) if not labels.empty else 0
    test_replay = as_int(labels["test_replay_allowed_next"].max(), 0) if not labels.empty else 0
    rows = [
        ("P203_PHASE202_COMPLETE", complete202 == 1, f"phase202_complete={complete202}", "hard"),
        ("P203_ACTION_PLAN_PRESENT", len(action_plan) == 3, f"action_rows={len(action_plan)}", "hard"),
        ("P203_JOINED_LABEL_CANDIDATES_PRESENT", len(labels) > 0, f"materialized_rows={len(labels)}", "hard"),
        ("P203_REDESIGNED_FEATURE_LABELS_MATERIALIZED", len(feature_summary) >= 5, f"feature_summary_rows={len(feature_summary)}", "hard"),
        ("P203_ADVERSE_SELECTION_AUDIT_RECORDED", not adverse_audit.empty, f"adverse_audit_rows={len(adverse_audit)}", "hard"),
        ("P203_SYMBOL_MONTH_STABILITY_AUDIT_RECORDED", not breadth_audit.empty, f"breadth_audit_rows={len(breadth_audit)}", "hard"),
        ("P203_NO_REPLAY_OR_PROMOTION", strategy_replay == 0 and test_replay == 0, f"strategy_replay={strategy_replay}; test_replay={test_replay}; promotion=0; paper_live=0", "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "gate_pass", "evidence", "severity"])


def build_acceptance_summary(
    labels: pd.DataFrame,
    feature_summary: pd.DataFrame,
    breadth_audit: pd.DataFrame,
    adverse_audit: pd.DataFrame,
    gates: pd.DataFrame,
) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    redesigned_pass_rows = as_int(labels["p203_redesigned_candidate_pass"].sum(), 0) if not labels.empty else 0
    max_symbols = as_int(labels["symbols"].max(), 0) if not labels.empty else 0
    max_dates = as_int(labels["trade_dates"].max(), 0) if not labels.empty else 0
    adverse_ceiling_met = as_int(adverse_audit["adverse_selection_ceiling_met"].iloc[0], 0) if not adverse_audit.empty else 0
    breadth_requirement_rows = as_int(breadth_audit["symbol_month_stability_requirement_met"].sum(), 0) if not breadth_audit.empty else 0
    candidate_gate_open = int(redesigned_pass_rows > 0 and adverse_ceiling_met == 1 and breadth_requirement_rows > 0)
    next_action = (
        "run_phase204_passive_candidate_precommit_no_execution"
        if candidate_gate_open
        else "redesign_passive_labels_or_expand_label_materialization_before_replay"
    )
    rows = [
        ("phase203_materialized_label_rows", len(labels), "Rows in redesigned passive label materialization"),
        ("phase203_feature_summary_rows", len(feature_summary), "Rows in redesigned feature summary"),
        ("phase203_symbol_breadth_audit_rows", len(breadth_audit), "Rows in symbol/month stability audit"),
        ("phase203_adverse_selection_audit_rows", len(adverse_audit), "Rows in adverse-selection audit"),
        ("phase203_redesigned_candidate_pass_rows", redesigned_pass_rows, "Rows passing all redesigned passive labels"),
        ("phase203_max_candidate_symbols", max_symbols, "Maximum candidate symbol breadth observed"),
        ("phase203_max_candidate_trade_dates", max_dates, "Maximum candidate trade-date breadth observed"),
        ("phase203_adverse_selection_ceiling_met", adverse_ceiling_met, "1 means any candidate met the toxicity ceiling"),
        ("phase203_symbol_month_stability_requirement_rows", breadth_requirement_rows, "Feature-family rows meeting symbol/month stability requirement"),
        ("phase203_candidate_gate_open", candidate_gate_open, "1 means Phase204 candidate precommit may be considered"),
        ("phase203_gate_rows", len(gates), "Gates evaluated"),
        ("phase203_hard_gate_rows", len(hard), "Hard gates evaluated"),
        ("phase203_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
        ("phase203_label_materialization_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase203 completed"),
        ("phase203_strategy_replay_allowed", 0, "No strategy replay opened"),
        ("phase203_test_replay_allowed_next", 0, "No test replay opened"),
        ("phase203_promotion_allowed", 0, "No promotion opened"),
        ("phase203_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
        ("phase203_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
        ("phase203_next_best_action", next_action, "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(
    path: Path,
    acceptance: pd.DataFrame,
    feature_summary: pd.DataFrame,
    adverse_audit: pd.DataFrame,
    breadth_audit: pd.DataFrame,
    gates: pd.DataFrame,
) -> None:
    lines = [
        "# Phase203 Redesigned Passive Label Materialization",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase203 materializes the Phase202 redesigned passive labels over existing Phase119 joined passive candidates.",
        "It remains label-only: no replay, test, orders, fills, P&L, promotion or paper/live acceptance.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Redesigned Feature Summary",
        "",
        _markdown_table(feature_summary),
        "",
        "## Adverse Selection Audit",
        "",
        _markdown_table(adverse_audit),
        "",
        "## Symbol/Month Stability Audit",
        "",
        _markdown_table(breadth_audit.head(20)),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def run_phase203(phase119_dir: Path, phase202_dir: Path, output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    candidates = read_csv(phase119_dir / "richer_passive_joined_label_candidates.csv")
    phase202 = read_csv(phase202_dir / "phase202_passive_feature_redesign_acceptance_summary.csv")
    action_plan = read_csv(phase202_dir / "phase202_phase203_label_only_action_plan.csv")

    labels = materialize_redesigned_labels(candidates)
    feature_summary = build_feature_summary(labels)
    breadth_audit = build_symbol_breadth_audit(labels)
    adverse_audit = build_adverse_selection_audit(labels)
    gates = build_gate_evaluation(phase202, action_plan, labels, feature_summary, breadth_audit, adverse_audit)
    acceptance = build_acceptance_summary(labels, feature_summary, breadth_audit, adverse_audit, gates)

    labels.to_csv(output_dir / "phase203_redesigned_passive_label_rows.csv", index=False)
    feature_summary.to_csv(output_dir / "phase203_redesigned_feature_summary.csv", index=False)
    breadth_audit.to_csv(output_dir / "phase203_symbol_month_stability_audit.csv", index=False)
    adverse_audit.to_csv(output_dir / "phase203_adverse_selection_audit.csv", index=False)
    gates.to_csv(output_dir / "phase203_redesigned_passive_label_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase203_redesigned_passive_label_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase203_redesigned_passive_label_materialization_report.md",
        acceptance,
        feature_summary,
        adverse_audit,
        breadth_audit,
        gates,
    )

    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "phase": 203,
        "generated_utc": generated,
        "phase119_dir": str(phase119_dir),
        "phase202_dir": str(phase202_dir),
        "output_dir": str(output_dir),
        "forbidden_outputs": FORBIDDEN_OUTPUTS,
        "outputs": [
            "phase203_redesigned_passive_label_rows.csv",
            "phase203_redesigned_feature_summary.csv",
            "phase203_symbol_month_stability_audit.csv",
            "phase203_adverse_selection_audit.csv",
            "phase203_redesigned_passive_label_gate_evaluation.csv",
            "phase203_redesigned_passive_label_acceptance_summary.csv",
            "phase203_redesigned_passive_label_materialization_report.md",
        ],
        **reproducibility_fields(
            artifact_id="phase203_redesigned_passive_label_materialization",
            generated_utc=generated,
            inputs={
                "phase119_candidates": str(phase119_dir / "richer_passive_joined_label_candidates.csv"),
                "phase202_acceptance": str(phase202_dir / "phase202_passive_feature_redesign_acceptance_summary.csv"),
                "phase202_action_plan": str(phase202_dir / "phase202_phase203_label_only_action_plan.csv"),
            },
            parameters={
                "materialization_scope": "redesigned_passive_labels_only",
                "adverse_selection_ceiling": "0.75",
                "minimum_symbols_before_replay": "8",
                "minimum_trade_dates_before_replay": "4",
                "strategy_replay_allowed": "0",
                "test_replay_allowed_next": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "labels": str(output_dir / "phase203_redesigned_passive_label_rows.csv"),
                "feature_summary": str(output_dir / "phase203_redesigned_feature_summary.csv"),
                "breadth_audit": str(output_dir / "phase203_symbol_month_stability_audit.csv"),
                "adverse_audit": str(output_dir / "phase203_adverse_selection_audit.csv"),
                "gates": str(output_dir / "phase203_redesigned_passive_label_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase203_redesigned_passive_label_acceptance_summary.csv"),
                "report": str(output_dir / "phase203_redesigned_passive_label_materialization_report.md"),
            },
            scenario_ids="phase203_redesigned_passive_label_materialization_no_replay",
        ),
    }
    (output_dir / "phase203_redesigned_passive_label_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize Phase203 redesigned passive labels without replay.")
    parser.add_argument("--phase119-dir", type=Path, default=DEFAULT_PHASE119_DIR)
    parser.add_argument("--phase202-dir", type=Path, default=DEFAULT_PHASE202_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    run_phase203(args.phase119_dir, args.phase202_dir, args.output_dir)


if __name__ == "__main__":
    main()
