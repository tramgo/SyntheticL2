from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE178_DIR = Path("outputs/phase178")
DEFAULT_PHASE177_DIR = Path("outputs/phase177")
DEFAULT_OUTPUT_DIR = Path("outputs/phase179")
FORBIDDEN_OUTPUTS = "order;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance"


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


def build_strategy_family_catalog(handoff: pd.DataFrame) -> pd.DataFrame:
    feature_ids = set(handoff["feature_id"].astype(str).tolist()) if not handoff.empty and "feature_id" in handoff.columns else set()
    rows = [
        {
            "strategy_family_id": "P179_SOURCE_QUALITY_REGIME_FILTER",
            "family_type": "context_filter",
            "allowed_feature_ids": "P175_RECEIVE_FLOW_REGIME_STATE;P175_STALE_QUOTE_DURATION;P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY",
            "hypothesis": "Avoid or down-weight later candidate decisions during feed-stale or cross-symbol burst regimes.",
            "decision_output_allowed_in_phase179": 0,
            "replay_allowed_in_phase179": 0,
            "required_later_label_family": "future_mid_or_spread_adjusted_return_label_precommitted_after_phase179",
            "required_cost_latency_binding": "zerodha_equity_cost_catalog_plus_receive_to_order_latency_catalog_before_replay",
            "blocked_overlap_check": "must_not_recreate_phase164_or_phase167_blocked_signal_logic",
        },
        {
            "strategy_family_id": "P179_LIQUIDITY_CHURN_CONTEXT",
            "family_type": "liquidity_context",
            "allowed_feature_ids": "P175_QUOTE_CHURN_RATE;P175_DEPTH_REFRESH_INTENSITY;P175_STALE_QUOTE_DURATION",
            "hypothesis": "Use churn/depth refresh as context for later execution-risk filters, not as standalone passive-fill proof.",
            "decision_output_allowed_in_phase179": 0,
            "replay_allowed_in_phase179": 0,
            "required_later_label_family": "execution_risk_or_spread_transition_label_precommitted_after_phase179",
            "required_cost_latency_binding": "zerodha_equity_cost_catalog_plus_slippage_latency_stress_before_replay",
            "blocked_overlap_check": "must_not_reopen_phase131_to_136_passive_queue_or_fill_claims",
        },
        {
            "strategy_family_id": "P179_RECEIVE_CADENCE_SHOCK_CONTEXT",
            "family_type": "event_cadence_context",
            "allowed_feature_ids": "P175_RECEIVE_EVENT_RATE_ZSCORE;P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY;P175_QUOTE_CHURN_RATE",
            "hypothesis": "Detect receive-cadence shocks that may condition later short-horizon models under strict train/validation/test separation.",
            "decision_output_allowed_in_phase179": 0,
            "replay_allowed_in_phase179": 0,
            "required_later_label_family": "short_horizon_direction_or_volatility_label_precommitted_after_phase179",
            "required_cost_latency_binding": "zerodha_equity_cost_catalog_plus_latency_queue_before_replay",
            "blocked_overlap_check": "must_not_reuse_phase167_fixed_cross_symbol_lead_lag_score",
        },
    ]
    catalog = pd.DataFrame(rows)
    catalog["referenced_feature_count"] = catalog["allowed_feature_ids"].str.split(";").map(len)
    catalog["all_features_in_phase178_handoff"] = catalog["allowed_feature_ids"].map(
        lambda text: int(set(str(text).split(";")).issubset(feature_ids))
    )
    return catalog


def build_precommit_rules(split_policy: pd.DataFrame) -> pd.DataFrame:
    split = split_policy.to_dict("records")[0] if not split_policy.empty else {}
    return pd.DataFrame(
        [
            {
                "rule_id": "P179_NO_REPLAY_NO_PNL",
                "rule": "Phase179 may declare strategy families only; it must not emit orders, fills, P&L or profitability claims.",
                "required_value": "true",
            },
            {
                "rule_id": "P179_CHRONOLOGICAL_SPLIT_REQUIRED",
                "rule": f"Use Phase178 split: train={split.get('train_dates', '')}; validation={split.get('validation_dates', '')}; test={split.get('test_dates', '')}.",
                "required_value": "true",
            },
            {
                "rule_id": "P179_TEST_DATE_UNTOUCHED",
                "rule": "No model/threshold/feature-family choice may use the test date before a replay precommit explicitly opens it.",
                "required_value": "true",
            },
            {
                "rule_id": "P179_COST_LATENCY_BINDING_REQUIRED",
                "rule": "Any later replay must bind Zerodha brokerage/STT/exchange/GST/SEBI/stamp-cost catalog plus latency/slippage assumptions before computing P&L.",
                "required_value": "true",
            },
            {
                "rule_id": "P179_BLOCKLIST_OVERLAP_AUDIT_REQUIRED",
                "rule": "Any later replay must audit overlap against Phase164, Phase167 and Phase131-136 blocked forms before running.",
                "required_value": "true",
            },
        ]
    )


def build_gate_evaluation(phase178: pd.DataFrame, phase177: pd.DataFrame, catalog: pd.DataFrame, rules: pd.DataFrame) -> pd.DataFrame:
    handoff_ready = as_int(metric_value(phase178, "phase178_handoff_ready", 0))
    quality_ran = as_int(metric_value(phase177, "phase177_feature_quality_audit_ran", 0))
    feature_refs_ok = int(not catalog.empty and catalog["all_features_in_phase178_handoff"].astype(bool).all())
    no_decisions = int(not catalog.empty and catalog["decision_output_allowed_in_phase179"].astype(int).eq(0).all())
    no_replay = int(not catalog.empty and catalog["replay_allowed_in_phase179"].astype(int).eq(0).all())
    return pd.DataFrame(
        [
            {
                "gate_id": "P179_PHASE178_HANDOFF_READY",
                "gate_pass": int(handoff_ready == 1),
                "evidence": f"phase178_handoff_ready={handoff_ready}",
                "severity": "hard",
            },
            {
                "gate_id": "P179_PHASE177_QUALITY_AUDIT_RAN",
                "gate_pass": int(quality_ran == 1),
                "evidence": f"phase177_feature_quality_audit_ran={quality_ran}",
                "severity": "hard",
            },
            {
                "gate_id": "P179_FEATURE_REFERENCES_IN_HANDOFF",
                "gate_pass": feature_refs_ok,
                "evidence": f"families={len(catalog)};all_features_in_phase178_handoff={feature_refs_ok}",
                "severity": "hard",
            },
            {
                "gate_id": "P179_NO_DECISION_OUTPUTS",
                "gate_pass": no_decisions,
                "evidence": f"decision_output_allowed_sum={int(catalog['decision_output_allowed_in_phase179'].astype(int).sum()) if not catalog.empty else -1}",
                "severity": "hard",
            },
            {
                "gate_id": "P179_NO_REPLAY_OUTPUTS",
                "gate_pass": no_replay,
                "evidence": f"replay_allowed_sum={int(catalog['replay_allowed_in_phase179'].astype(int).sum()) if not catalog.empty else -1}",
                "severity": "hard",
            },
            {
                "gate_id": "P179_PRECOMMIT_RULES_DECLARED",
                "gate_pass": int(len(rules) >= 5),
                "evidence": f"rules={len(rules)}",
                "severity": "hard",
            },
        ]
    )


def build_acceptance_summary(catalog: pd.DataFrame, rules: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0
    precommit_ready = int(not hard.empty and hard_pass == len(hard))
    next_action = "build_phase180_cost_latency_bound_label_precommit_no_replay" if precommit_ready else "repair_phase179_strategy_family_precommit"
    return pd.DataFrame(
        [
            ("phase179_strategy_family_rows", int(len(catalog)), "Candidate strategy families precommitted"),
            ("phase179_precommit_rule_rows", int(len(rules)), "Rules required before any later replay"),
            ("phase179_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase179_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase179_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase179_precommit_ready", precommit_ready, "1 means next no-replay label/cost precommit may be built"),
            ("phase179_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase179_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase179_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase179_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase179 Strategy-family Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase179 declares candidate strategy families that may later consume the audited receive-flow feature lake.",
        "It does not run replay, emit orders, compute fills, calculate P&L, claim profitability, or open paper/live acceptance.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase179_strategy_family_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase179(phase178_dir: Path, phase177_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase178 = read_csv(phase178_dir / "phase178_receive_flow_feature_handoff_precommit_acceptance_summary.csv")
    handoff = read_csv(phase178_dir / "phase178_allowed_feature_handoff.csv")
    split_policy = read_csv(phase178_dir / "phase178_train_test_split_policy.csv")
    phase177 = read_csv(phase177_dir / "phase177_receive_flow_feature_quality_audit_acceptance_summary.csv")

    catalog = build_strategy_family_catalog(handoff)
    rules = build_precommit_rules(split_policy)
    gates = build_gate_evaluation(phase178, phase177, catalog, rules)
    acceptance = build_acceptance_summary(catalog, rules, gates)

    catalog.to_csv(output_dir / "phase179_strategy_family_catalog.csv", index=False)
    rules.to_csv(output_dir / "phase179_precommit_rules.csv", index=False)
    gates.to_csv(output_dir / "phase179_strategy_family_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase179_strategy_family_precommit_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Strategy Family Catalog": catalog,
            "Precommit Rules": rules,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase179_strategy_family_precommit",
        **reproducibility_fields(
            artifact_id="phase179_strategy_family_precommit",
            generated_utc=generated,
            inputs={
                "phase178_acceptance": str(phase178_dir / "phase178_receive_flow_feature_handoff_precommit_acceptance_summary.csv"),
                "phase178_allowed_feature_handoff": str(phase178_dir / "phase178_allowed_feature_handoff.csv"),
                "phase178_train_test_split_policy": str(phase178_dir / "phase178_train_test_split_policy.csv"),
                "phase177_acceptance": str(phase177_dir / "phase177_receive_flow_feature_quality_audit_acceptance_summary.csv"),
            },
            parameters={
                "precommit_policy": "strategy_family_catalog_only_no_replay",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
                "next_required_gate": "phase180_cost_latency_bound_label_precommit_no_replay",
            },
            outputs={
                "strategy_family_catalog": str(output_dir / "phase179_strategy_family_catalog.csv"),
                "precommit_rules": str(output_dir / "phase179_precommit_rules.csv"),
                "gate_evaluation": str(output_dir / "phase179_strategy_family_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase179_strategy_family_precommit_acceptance_summary.csv"),
                "report": str(output_dir / "phase179_strategy_family_precommit_report.md"),
            },
            random_seed="none_deterministic_strategy_family_precommit",
            scenario_ids="phase179_strategy_family_precommit",
            cost_model_version="not_bound_until_phase180",
            latency_model_version="not_bound_until_phase180",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase179_strategy_family_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase178-dir", type=Path, default=DEFAULT_PHASE178_DIR)
    parser.add_argument("--phase177-dir", type=Path, default=DEFAULT_PHASE177_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase179(args.phase178_dir, args.phase177_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
