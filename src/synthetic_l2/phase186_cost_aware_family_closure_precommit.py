from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE179_DIR = Path("outputs/phase179")
DEFAULT_PHASE180_DIR = Path("outputs/phase180")
DEFAULT_PHASE185_DIR = Path("outputs/phase185")
DEFAULT_OUTPUT_DIR = Path("outputs/phase186")
FORBIDDEN_OUTPUTS = "test_replay;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim"


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


def build_family_closure(family_decision: pd.DataFrame, phase179_catalog: pd.DataFrame) -> pd.DataFrame:
    if family_decision.empty:
        return pd.DataFrame()
    family_rollup = (
        family_decision.groupby("strategy_family_id", as_index=False)
        .agg(
            best_validation_net_bps_proxy_mean=("validation_net_bps_proxy_mean", "max"),
            best_gross_edge_over_control_bps=("gross_edge_over_best_control_bps", "max"),
            profile_rows=("latency_profile_id", "count"),
            promoted_rows=("promotion_allowed", "sum"),
            test_replay_allowed_rows=("test_replay_allowed_next", "sum"),
        )
    )
    family_rollup = family_rollup.merge(
        phase179_catalog[["strategy_family_id", "family_type", "hypothesis", "allowed_feature_ids"]],
        on="strategy_family_id",
        how="left",
    )
    family_rollup["closure_decision"] = "closed_cost_dominated_validation"
    family_rollup["closure_reason"] = (
        "Phase185 found every retail/default and stressed-retail validation profile net-negative after Phase180 cost/latency bounds; no test replay opened."
    )
    family_rollup["test_replay_allowed_after_phase186"] = 0
    family_rollup["promotion_allowed_after_phase186"] = 0
    family_rollup["reuse_without_redesign_allowed"] = 0
    return family_rollup[
        [
            "strategy_family_id",
            "family_type",
            "hypothesis",
            "allowed_feature_ids",
            "best_validation_net_bps_proxy_mean",
            "best_gross_edge_over_control_bps",
            "profile_rows",
            "closure_decision",
            "closure_reason",
            "test_replay_allowed_after_phase186",
            "promotion_allowed_after_phase186",
            "reuse_without_redesign_allowed",
        ]
    ]


def build_redesign_contract(latency_profiles: pd.DataFrame) -> pd.DataFrame:
    allowed_profiles = ";".join(
        latency_profiles.loc[latency_profiles["allowed_for_promotion"].astype(int).eq(1), "profile_id"].astype(str).tolist()
    ) if not latency_profiles.empty else "P180_RETAIL_MARKETABLE_DEFAULT;P180_STRESSED_RETAIL"
    rows = [
        {
            "redesign_contract_id": "P186_COST_AWARE_THRESHOLDING",
            "requirement": "Candidate thresholds must be fitted against net return-bps proxies after Phase180 cost/latency bounds, not gross label direction alone.",
            "required_before_new_replay": 1,
            "evidence_required": "train_fitted_cost_aware_threshold_catalog",
        },
        {
            "redesign_contract_id": "P186_MIN_VALIDATION_NET_EDGE",
            "requirement": "A redesigned family must predeclare a minimum validation net edge that exceeds both retail/default and stressed-retail cost bounds.",
            "required_before_new_replay": 1,
            "evidence_required": "validation_net_edge_margin_bps_by_profile",
        },
        {
            "redesign_contract_id": "P186_EVENT_SELECTIVITY_BOUND",
            "requirement": "A redesigned family must cap decision frequency or explicitly prove that high event count does not make costs dominate.",
            "required_before_new_replay": 1,
            "evidence_required": "train_validation_decision_rate_and_turnover_bound",
        },
        {
            "redesign_contract_id": "P186_NEGATIVE_CONTROL_MARGIN",
            "requirement": "Actual-time validation net edge must beat shuffled-time and shuffled-symbol controls by a predeclared positive margin.",
            "required_before_new_replay": 1,
            "evidence_required": "negative_control_net_edge_margin",
        },
        {
            "redesign_contract_id": "P186_NO_TEST_UNTIL_REDESIGN_PASSES",
            "requirement": "Untouched test replay remains blocked until a redesigned family passes train/validation cost-aware gates.",
            "required_before_new_replay": 1,
            "evidence_required": "test_rows_used_equals_0_and_test_replay_allowed_next_equals_0",
        },
        {
            "redesign_contract_id": "P186_ALLOWED_LATENCY_PROFILES",
            "requirement": f"Only promotion-eligible latency profiles may support acceptance: {allowed_profiles}. Zero-latency remains diagnostic-only.",
            "required_before_new_replay": 1,
            "evidence_required": "phase180_latency_profile_binding",
        },
    ]
    return pd.DataFrame(rows)


def build_next_family_blueprint() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "candidate_family_id": "P186_NET_EDGE_SPARSE_RECEIVE_FLOW",
                "family_goal": "Reduce event count and require expected move to exceed estimated spread, slippage and statutory costs before any dry decision.",
                "allowed_feature_inputs": "receive_event_rate_zscore;quote_churn_count;depth_refresh_count;stale_quote_duration_ms;cross_symbol_arrival_share;spread;l1_qty_imbalance;top5_qty_imbalance",
                "required_label_inputs": "future_mid_return_bps_next_bucket;future_spread_change_bps_next_bucket;execution_risk_spread_widen_next_bucket",
                "entry_rule_shape": "cost_buffered_sparse_threshold; no passive queue/fill claim",
                "predeclared_abort_condition": "validation_net_mean_bps <= 0 under any promotion-eligible Phase180 latency profile",
                "test_replay_allowed_in_phase186": 0,
            },
            {
                "candidate_family_id": "P186_EXECUTION_RISK_AVOIDANCE_FILTER",
                "family_goal": "Use receive-flow and book-state churn to avoid costly regimes rather than predict every short-horizon move.",
                "allowed_feature_inputs": "quote_churn_count;depth_refresh_count;stale_quote_duration_ms;cross_symbol_arrival_share;spread;top5_qty_imbalance",
                "required_label_inputs": "execution_risk_spread_widen_next_bucket;future_abs_return_bps_next_bucket",
                "entry_rule_shape": "filter_or_abstain_layer_only; no standalone buy/sell signal until cost-aware candidate exists",
                "predeclared_abort_condition": "filter does not improve validation net bps versus unfiltered baseline after costs",
                "test_replay_allowed_in_phase186": 0,
            },
        ]
    )


def build_gate_evaluation(phase185: pd.DataFrame, closure: pd.DataFrame, redesign: pd.DataFrame, blueprint: pd.DataFrame) -> pd.DataFrame:
    interpretation_complete = as_int(metric_value(phase185, "phase185_validation_interpretation_complete", 0))
    cost_dominated = as_int(metric_value(phase185, "phase185_cost_dominates_validation_edge", 0))
    test_replay_allowed = as_int(metric_value(phase185, "phase185_test_replay_allowed_next", 0))
    promotion_allowed = as_int(metric_value(phase185, "phase185_promotion_allowed", 0))
    return pd.DataFrame(
        [
            {
                "gate_id": "P186_PHASE185_INTERPRETATION_COMPLETE",
                "gate_pass": int(interpretation_complete == 1),
                "evidence": f"phase185_validation_interpretation_complete={interpretation_complete}",
                "severity": "hard",
            },
            {
                "gate_id": "P186_COST_DOMINATED_RESULT_ACKNOWLEDGED",
                "gate_pass": int(cost_dominated == 1),
                "evidence": f"phase185_cost_dominates_validation_edge={cost_dominated}",
                "severity": "hard",
            },
            {
                "gate_id": "P186_CURRENT_FAMILIES_CLOSED",
                "gate_pass": int(not closure.empty and closure["reuse_without_redesign_allowed"].astype(int).eq(0).all()),
                "evidence": f"closed_family_rows={len(closure)}",
                "severity": "hard",
            },
            {
                "gate_id": "P186_TEST_REPLAY_REMAINS_CLOSED",
                "gate_pass": int(test_replay_allowed == 0 and not closure.empty and closure["test_replay_allowed_after_phase186"].astype(int).eq(0).all()),
                "evidence": f"phase185_test_replay_allowed_next={test_replay_allowed}",
                "severity": "hard",
            },
            {
                "gate_id": "P186_PROMOTION_REMAINS_CLOSED",
                "gate_pass": int(promotion_allowed == 0 and not closure.empty and closure["promotion_allowed_after_phase186"].astype(int).eq(0).all()),
                "evidence": f"phase185_promotion_allowed={promotion_allowed}",
                "severity": "hard",
            },
            {
                "gate_id": "P186_REDESIGN_CONTRACT_PRECOMMITTED",
                "gate_pass": int(len(redesign) >= 6 and redesign["required_before_new_replay"].astype(int).eq(1).all()),
                "evidence": f"redesign_contract_rows={len(redesign)}",
                "severity": "hard",
            },
            {
                "gate_id": "P186_NEXT_BLUEPRINT_DECLARED_NO_REPLAY",
                "gate_pass": int(len(blueprint) >= 2 and blueprint["test_replay_allowed_in_phase186"].astype(int).eq(0).all()),
                "evidence": f"blueprint_rows={len(blueprint)}",
                "severity": "hard",
            },
        ]
    )


def build_acceptance_summary(closure: pd.DataFrame, redesign: pd.DataFrame, blueprint: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates.loc[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(int).sum()) if not hard.empty else 0
    closure_complete = int(len(hard) > 0 and hard_pass == len(hard))
    best_net = float(closure["best_validation_net_bps_proxy_mean"].max()) if not closure.empty else ""
    rows = [
        ("phase186_closed_family_rows", int(len(closure)), "Current family rows closed"),
        ("phase186_redesign_contract_rows", int(len(redesign)), "Redesign contract rows"),
        ("phase186_next_family_blueprint_rows", int(len(blueprint)), "Next family blueprint rows"),
        ("phase186_best_closed_family_validation_net_bps_proxy_mean", best_net, "Best validation net bps among closed families"),
        ("phase186_gate_rows", int(len(gates)), "Gates evaluated"),
        ("phase186_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
        ("phase186_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase186_current_family_set_closed", closure_complete, "1 means current Phase179 family set is closed unless redesigned"),
        ("phase186_reuse_without_redesign_allowed", 0, "Closed family set cannot be reused unchanged"),
        ("phase186_test_replay_allowed_next", 0, "No test replay opened by Phase186"),
        ("phase186_promotion_allowed", 0, "No promotion opened"),
        ("phase186_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
        ("phase186_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
        ("phase186_next_best_action", "build_phase187_cost_aware_sparse_receive_flow_candidate_no_test", "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, closure: pd.DataFrame, redesign: pd.DataFrame, blueprint: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase186 Cost-aware Family Closure and Redesign Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase186 closes the current Phase179 receive-flow family set after Phase185 found validation results cost-dominated.",
        "It does not run a new replay, touch test rows, open promotion, or claim profitability.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Closed Family Set",
        "",
        _markdown_table(closure),
        "",
        "## Redesign Contract",
        "",
        _markdown_table(redesign),
        "",
        "## Next Family Blueprint",
        "",
        _markdown_table(blueprint),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
    ]
    (output_dir / "phase186_cost_aware_family_closure_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase186(phase179_dir: Path, phase180_dir: Path, phase185_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase179_catalog = read_csv(phase179_dir / "phase179_strategy_family_catalog.csv")
    latency_profiles = read_csv(phase180_dir / "phase180_latency_slippage_profile_catalog.csv")
    phase185 = read_csv(phase185_dir / "phase185_validation_replay_interpretation_acceptance_summary.csv")
    family_decision = read_csv(phase185_dir / "phase185_family_decision.csv")

    closure = build_family_closure(family_decision, phase179_catalog)
    redesign = build_redesign_contract(latency_profiles)
    blueprint = build_next_family_blueprint()
    gates = build_gate_evaluation(phase185, closure, redesign, blueprint)
    acceptance = build_acceptance_summary(closure, redesign, blueprint, gates)

    closure.to_csv(output_dir / "phase186_closed_family_set.csv", index=False)
    redesign.to_csv(output_dir / "phase186_cost_aware_redesign_contract.csv", index=False)
    blueprint.to_csv(output_dir / "phase186_next_family_blueprint.csv", index=False)
    gates.to_csv(output_dir / "phase186_cost_aware_family_closure_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase186_cost_aware_family_closure_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, closure, redesign, blueprint, gates)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase186_cost_aware_family_closure_precommit",
        **reproducibility_fields(
            artifact_id="phase186_cost_aware_family_closure_precommit",
            generated_utc=generated_utc,
            inputs={
                "phase179_strategy_family_catalog": str(phase179_dir / "phase179_strategy_family_catalog.csv"),
                "phase180_latency_profiles": str(phase180_dir / "phase180_latency_slippage_profile_catalog.csv"),
                "phase185_acceptance": str(phase185_dir / "phase185_validation_replay_interpretation_acceptance_summary.csv"),
                "phase185_family_decision": str(phase185_dir / "phase185_family_decision.csv"),
            },
            parameters={
                "close_current_family_set": 1,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "new_replay_executed": 0,
            },
            outputs={
                "closed_family_set": str(output_dir / "phase186_closed_family_set.csv"),
                "redesign_contract": str(output_dir / "phase186_cost_aware_redesign_contract.csv"),
                "next_family_blueprint": str(output_dir / "phase186_next_family_blueprint.csv"),
                "gate_evaluation": str(output_dir / "phase186_cost_aware_family_closure_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase186_cost_aware_family_closure_acceptance_summary.csv"),
                "report": str(output_dir / "phase186_cost_aware_family_closure_precommit_report.md"),
            },
            scenario_ids="phase186_cost_aware_family_closure_precommit",
            cost_model_version="phase180_zerodha_equity_intraday_cost_bound_proxy",
            latency_model_version="phase180_retail_marketable_default_and_stressed_retail",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase186_cost_aware_family_closure_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase179-dir", type=Path, default=DEFAULT_PHASE179_DIR)
    parser.add_argument("--phase180-dir", type=Path, default=DEFAULT_PHASE180_DIR)
    parser.add_argument("--phase185-dir", type=Path, default=DEFAULT_PHASE185_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase186(args.phase179_dir, args.phase180_dir, args.phase185_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
