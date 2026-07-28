from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE175_DIR = Path("outputs/phase175")
DEFAULT_PHASE176_DIR = Path("outputs/phase176")
DEFAULT_PHASE177_DIR = Path("outputs/phase177")
DEFAULT_OUTPUT_DIR = Path("outputs/phase178")
FORBIDDEN_OUTPUTS = "buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance"


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


def build_allowed_feature_handoff(schema: pd.DataFrame, inventory: pd.DataFrame) -> pd.DataFrame:
    if schema.empty:
        return pd.DataFrame()
    horizons = ";".join(str(item) for item in sorted(inventory["horizon_sec"].dropna().astype(int).unique())) if not inventory.empty and "horizon_sec" in inventory.columns else ""
    dates = ";".join(str(item) for item in sorted(inventory["trade_date"].dropna().astype(str).unique())) if not inventory.empty and "trade_date" in inventory.columns else ""
    symbols = int(inventory["symbol"].nunique()) if not inventory.empty and "symbol" in inventory.columns else 0
    rows = []
    for item in schema.to_dict("records"):
        rows.append(
            {
                "feature_id": item["feature_id"],
                "feature_family": item["feature_family"],
                "handoff_status": "allowed_for_phase179_precommit_only",
                "allowed_horizons_materialized_seconds": horizons,
                "available_trade_dates": dates,
                "available_symbol_count": symbols,
                "allowed_downstream_use": "feature_candidate_for_future_strategy_precommit_only",
                "required_before_replay": "phase179_strategy_family_precommit;train_test_split;leakage_audit;blocklist_overlap_audit;cost_latency_catalog_binding",
                "forbidden_direct_use": FORBIDDEN_OUTPUTS,
                "leakage_boundary": item.get("leakage_control", ""),
            }
        )
    return pd.DataFrame(rows)


def build_train_test_policy(inventory: pd.DataFrame) -> pd.DataFrame:
    dates = sorted(inventory["trade_date"].dropna().astype(str).unique()) if not inventory.empty and "trade_date" in inventory.columns else []
    train_dates = dates[:3]
    validation_dates = dates[3:4]
    test_dates = dates[4:]
    return pd.DataFrame(
        [
            {
                "split_id": "P178_CHRONOLOGICAL_3_1_1",
                "train_dates": ";".join(train_dates),
                "validation_dates": ";".join(validation_dates),
                "test_dates": ";".join(test_dates),
                "fit_policy": "fit baselines/transforms/model choices on train_dates only",
                "selection_policy": "validation_dates may select predeclared thresholds only after Phase179",
                "final_test_policy": "test_dates are untouched until the replay phase precommit passes",
                "minimum_dates_required": 5,
                "split_pass": int(len(train_dates) >= 3 and len(validation_dates) >= 1 and len(test_dates) >= 1),
            }
        ]
    )


def build_blocklist_policy() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "blocked_source": "PHASE164_S01_TO_S07_S09_SYNTHETIC_FORMS",
                "handoff_rule": "feature may not recreate blocked synthetic signal formulas or thresholds",
                "overlap_allowed": 0,
            },
            {
                "blocked_source": "PHASE167_S08_FIXED_CROSS_SYMBOL_LEAD_LAG_FORM",
                "handoff_rule": "cross-symbol arrival synchrony is context only; fixed S08 lead-lag score remains forbidden",
                "overlap_allowed": 0,
            },
            {
                "blocked_source": "PHASE131_TO_136_TOP_FIVE_DEPTH_PASSIVE_BRANCH",
                "handoff_rule": "depth refresh/churn may describe feed/book context only; passive queue/fill claims remain closed",
                "overlap_allowed": 0,
            },
        ]
    )


def build_gate_evaluation(
    phase176: pd.DataFrame,
    phase177: pd.DataFrame,
    handoff: pd.DataFrame,
    split_policy: pd.DataFrame,
    coverage: pd.DataFrame,
    partition_quality: pd.DataFrame,
) -> pd.DataFrame:
    features_materialized = as_int(metric_value(phase176, "phase176_features_materialized", 0))
    quality_ran = as_int(metric_value(phase177, "phase177_feature_quality_audit_ran", 0))
    coverage_rows = as_int(metric_value(phase177, "phase177_coverage_rows", 0))
    coverage_pass = as_int(metric_value(phase177, "phase177_coverage_pass_rows", 0))
    missing_required = as_int(metric_value(phase177, "phase177_missing_required_column_partitions", 0))
    duplicate_buckets = as_int(metric_value(phase177, "phase177_duplicate_bucket_rows", 0))
    monotonic_violations = as_int(metric_value(phase177, "phase177_bucket_monotonic_violations", 0))
    return pd.DataFrame(
        [
            {
                "gate_id": "P178_PHASE176_FEATURES_MATERIALIZED",
                "gate_pass": int(features_materialized == 1),
                "evidence": f"phase176_features_materialized={features_materialized}",
                "severity": "hard",
            },
            {
                "gate_id": "P178_PHASE177_QUALITY_AUDIT_RAN",
                "gate_pass": int(quality_ran == 1),
                "evidence": f"phase177_feature_quality_audit_ran={quality_ran}",
                "severity": "hard",
            },
            {
                "gate_id": "P178_COVERAGE_COMPLETE",
                "gate_pass": int(coverage_rows > 0 and coverage_rows == coverage_pass and len(coverage) == coverage_rows),
                "evidence": f"coverage_pass_rows={coverage_pass}/{coverage_rows}",
                "severity": "hard",
            },
            {
                "gate_id": "P178_PARTITION_QUALITY_CLEAN",
                "gate_pass": int(missing_required == 0 and duplicate_buckets == 0 and monotonic_violations == 0 and len(partition_quality) > 0),
                "evidence": f"missing_required={missing_required};duplicate_buckets={duplicate_buckets};monotonic_violations={monotonic_violations};partitions={len(partition_quality)}",
                "severity": "hard",
            },
            {
                "gate_id": "P178_HANDOFF_FEATURES_DECLARED",
                "gate_pass": int(len(handoff) >= 6),
                "evidence": f"handoff_feature_rows={len(handoff)}",
                "severity": "hard",
            },
            {
                "gate_id": "P178_CHRONOLOGICAL_SPLIT_DECLARED",
                "gate_pass": int(not split_policy.empty and split_policy["split_pass"].astype(bool).all()),
                "evidence": split_policy.to_dict("records")[0] if not split_policy.empty else "missing_split_policy",
                "severity": "hard",
            },
            {
                "gate_id": "P178_NO_REPLAY_OR_PROFITABILITY_OUTPUTS",
                "gate_pass": 1,
                "evidence": "handoff precommit only; forbidden_outputs=" + FORBIDDEN_OUTPUTS,
                "severity": "hard",
            },
        ]
    )


def build_acceptance_summary(handoff: pd.DataFrame, split_policy: pd.DataFrame, blocklist: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0
    handoff_ready = int(not hard.empty and hard_pass == len(hard))
    next_action = "build_phase179_strategy_family_precommit_no_replay" if handoff_ready else "repair_phase176_phase177_feature_quality_before_phase178_handoff"
    return pd.DataFrame(
        [
            ("phase178_handoff_feature_rows", int(len(handoff)), "Feature families handed off for future precommit only"),
            ("phase178_train_test_policy_rows", int(len(split_policy)), "Chronological train/validation/test split policies"),
            ("phase178_blocklist_policy_rows", int(len(blocklist)), "Blocked-family policies carried forward"),
            ("phase178_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase178_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase178_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase178_handoff_ready", handoff_ready, "1 means Phase179 precommit may be built"),
            ("phase178_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase178_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase178_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase178_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase178 Receive-flow Feature Handoff Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase178 defines how audited receive-flow features may be handed to a later strategy precommit phase.",
        "It does not emit signals, orders, fills, P&L, profitability claims, or paper/live acceptance.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase178_receive_flow_feature_handoff_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase178(
    phase175_dir: Path,
    phase176_dir: Path,
    phase177_dir: Path,
    output_dir: Path,
    base_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    schema = read_csv(phase175_dir / "phase175_receive_flow_feature_schema.csv")
    phase176 = read_csv(phase176_dir / "phase176_receive_flow_feature_materializer_acceptance_summary.csv")
    inventory = read_csv(phase176_dir / "phase176_feature_partition_inventory.csv")
    phase177 = read_csv(phase177_dir / "phase177_receive_flow_feature_quality_audit_acceptance_summary.csv")
    coverage = read_csv(phase177_dir / "phase177_horizon_date_coverage_metrics.csv")
    partition_quality = read_csv(phase177_dir / "phase177_partition_quality_metrics.csv")

    handoff = build_allowed_feature_handoff(schema, inventory)
    split_policy = build_train_test_policy(inventory)
    blocklist = build_blocklist_policy()
    gates = build_gate_evaluation(phase176, phase177, handoff, split_policy, coverage, partition_quality)
    acceptance = build_acceptance_summary(handoff, split_policy, blocklist, gates)

    handoff.to_csv(output_dir / "phase178_allowed_feature_handoff.csv", index=False)
    split_policy.to_csv(output_dir / "phase178_train_test_split_policy.csv", index=False)
    blocklist.to_csv(output_dir / "phase178_blocklist_carry_forward_policy.csv", index=False)
    gates.to_csv(output_dir / "phase178_handoff_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase178_receive_flow_feature_handoff_precommit_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Allowed Feature Handoff": handoff,
            "Train/Test Split Policy": split_policy,
            "Blocklist Carry-forward Policy": blocklist,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase178_receive_flow_feature_handoff_precommit",
        **reproducibility_fields(
            artifact_id="phase178_receive_flow_feature_handoff_precommit",
            generated_utc=generated,
            inputs={
                "phase175_schema": str(phase175_dir / "phase175_receive_flow_feature_schema.csv"),
                "phase176_acceptance": str(phase176_dir / "phase176_receive_flow_feature_materializer_acceptance_summary.csv"),
                "phase176_inventory": str(phase176_dir / "phase176_feature_partition_inventory.csv"),
                "phase177_acceptance": str(phase177_dir / "phase177_receive_flow_feature_quality_audit_acceptance_summary.csv"),
                "phase177_coverage": str(phase177_dir / "phase177_horizon_date_coverage_metrics.csv"),
                "phase177_partition_quality": str(phase177_dir / "phase177_partition_quality_metrics.csv"),
            },
            parameters={
                "handoff_policy": "precommit_only_no_strategy_replay",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
                "split_policy": "chronological_3_train_1_validation_1_test_from_available_5_dates",
            },
            outputs={
                "allowed_feature_handoff": str(output_dir / "phase178_allowed_feature_handoff.csv"),
                "train_test_split_policy": str(output_dir / "phase178_train_test_split_policy.csv"),
                "blocklist_policy": str(output_dir / "phase178_blocklist_carry_forward_policy.csv"),
                "gate_evaluation": str(output_dir / "phase178_handoff_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase178_receive_flow_feature_handoff_precommit_acceptance_summary.csv"),
                "report": str(output_dir / "phase178_receive_flow_feature_handoff_precommit_report.md"),
            },
            random_seed="none_deterministic_handoff_precommit",
            scenario_ids="phase178_receive_flow_feature_handoff_precommit",
            cost_model_version="not_applicable_no_replay",
            latency_model_version="not_applicable_no_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase178_receive_flow_feature_handoff_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase175-dir", type=Path, default=DEFAULT_PHASE175_DIR)
    parser.add_argument("--phase176-dir", type=Path, default=DEFAULT_PHASE176_DIR)
    parser.add_argument("--phase177-dir", type=Path, default=DEFAULT_PHASE177_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase178(args.phase175_dir, args.phase176_dir, args.phase177_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
