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


DEFAULT_OUTPUT_DIR = Path("outputs/phase122")
INPUTS = {
    "phase70": Path("outputs/phase70/lead_lag_acceptance_summary.csv"),
    "phase71": Path("outputs/phase71/shock_acceptance_summary.csv"),
    "phase72": Path("outputs/phase72/research_audit_acceptance_summary.csv"),
    "phase74": Path("outputs/phase74/remediation_acceptance_summary.csv"),
    "phase116": Path("outputs/phase116/phase116_profitability_verdict_acceptance_summary.csv"),
    "phase117": Path("outputs/phase117/phase117_real_anchor_acquisition_acceptance_summary.csv"),
    "phase121": Path("outputs/phase121/phase121_passive_branch_retirement_acceptance_summary.csv"),
}


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


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    return int(round(as_float(value, float(default))))


def build_prior_evidence(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "evidence_id": "P70_CROSS_SYMBOL_LEAD_LAG",
                "scope": "cross-symbol lead-lag labels",
                "rows_reviewed": as_int(metric_value(tables["phase70"], "phase70_rule_rows")),
                "candidate_rows": as_int(metric_value(tables["phase70"], "phase70_label_candidate_rows")),
                "best_net_pnl_inr": as_float(metric_value(tables["phase70"], "phase70_best_net_pnl_inr")),
                "survives_gate": as_int(metric_value(tables["phase70"], "phase70_survives_cross_symbol_gate")),
                "decision_use": "feature_context_only_not_replay",
            },
            {
                "evidence_id": "P71_SHOCK_RESILIENCE",
                "scope": "shock/control event-bar labels",
                "rows_reviewed": as_int(metric_value(tables["phase71"], "phase71_rule_rows")),
                "candidate_rows": as_int(metric_value(tables["phase71"], "phase71_label_candidate_rows")),
                "best_net_pnl_inr": as_float(metric_value(tables["phase71"], "phase71_best_net_pnl_inr")),
                "survives_gate": as_int(metric_value(tables["phase71"], "phase71_survives_shock_resilience_gate")),
                "decision_use": "regime_risk_context_only_not_replay",
            },
            {
                "evidence_id": "P72_RESEARCH_AUDIT",
                "scope": "strategy family audit across Phase52-71",
                "rows_reviewed": as_int(metric_value(tables["phase72"], "phase72_families_reviewed")),
                "candidate_rows": as_int(metric_value(tables["phase72"], "phase72_scale_ready_family_count")),
                "best_net_pnl_inr": None,
                "survives_gate": as_int(metric_value(tables["phase72"], "phase72_allow_more_full_year_strategy_replay_now")),
                "decision_use": "blocks_more_strategy_replay",
            },
            {
                "evidence_id": "P116_PROFITABILITY_VERDICT",
                "scope": "latest strategy profitability verdict",
                "rows_reviewed": as_int(metric_value(tables["phase116"], "phase116_profitability_evidence_rows")),
                "candidate_rows": as_int(metric_value(tables["phase116"], "phase116_accepted_strategy_rows")),
                "best_net_pnl_inr": None,
                "survives_gate": 0,
                "decision_use": "current_families_not_profitable",
            },
            {
                "evidence_id": "P121_PASSIVE_RETIREMENT",
                "scope": "passive branch train-half retirement gate",
                "rows_reviewed": as_int(metric_value(tables["phase121"], "phase121_train_half_candidate_orders")),
                "candidate_rows": as_int(metric_value(tables["phase121"], "phase121_train_half_pre_replay_candidates")),
                "best_net_pnl_inr": None,
                "survives_gate": as_int(metric_value(tables["phase121"], "phase121_passive_replay_allowed")),
                "decision_use": "passive_branch_replay_closed",
            },
            {
                "evidence_id": "P117_REAL_ANCHOR_GATE",
                "scope": "real-anchor acquisition status",
                "rows_reviewed": as_int(metric_value(tables["phase117"], "phase117_current_ready_real_anchor_days")),
                "candidate_rows": as_int(metric_value(tables["phase117"], "phase117_strategy_replay_allowed")),
                "best_net_pnl_inr": None,
                "survives_gate": as_int(metric_value(tables["phase117"], "phase117_strategy_replay_allowed")),
                "decision_use": "real_replay_locked_until_more_days",
            },
        ]
    )


def build_forecast_feature_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "feature_source_id": "P122_COST_TOXICITY_FORECAST_FILTER",
                "purpose": "Predict when spread, costs and adverse-selection risk are too high, so future strategies can abstain rather than trade.",
                "not_a_strategy": True,
                "allowed_inputs": "spread bucket, depth bucket, event intensity, shock flags, passive toxicity labels, cross-symbol context",
                "forbidden_inputs": "future P&L, realized trade outcome, test-period threshold tuning",
                "candidate_output": "probability_of_cost_clearing_failure",
                "minimum_value_claim": "reduces false-positive strategy candidates and improves abstention calibration",
            },
            {
                "feature_source_id": "P122_REGIME_REALISM_FILTER",
                "purpose": "Classify synthetic regimes where generator assumptions are unreliable before using them for strategy evidence.",
                "not_a_strategy": True,
                "allowed_inputs": "shock flags, spread/depth/cadence diagnostics, Phase94/109 realism gaps, cross-symbol synchronization features",
                "forbidden_inputs": "strategy net P&L as a regime label",
                "candidate_output": "realism_risk_score",
                "minimum_value_claim": "separates calibration-quality screening from alpha mining",
            },
            {
                "feature_source_id": "P122_OPPORTUNITY_ABSTENTION_FILTER",
                "purpose": "Predict low-opportunity periods where any future strategy family should be disabled before execution modeling.",
                "not_a_strategy": True,
                "allowed_inputs": "event rate, spread, depth, volatility, shock state, cross-symbol dispersion",
                "forbidden_inputs": "directional side labels or threshold selection from replay P&L",
                "candidate_output": "trade_disable_flag",
                "minimum_value_claim": "reduces compute spent on structurally untradeable event windows",
            },
        ]
    )


def build_validation_gates() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "gate_id": "P122_NO_DIRECT_TRADING",
                "stage": "pre_model",
                "requirement": "Phase122 feature sources must not emit buy/sell signals or open replay.",
                "pass_threshold": "strategy_replay_allowed == 0 and outputs are filters/scores only",
            },
            {
                "gate_id": "P122_NO_PNL_SELECTION",
                "stage": "pre_model",
                "requirement": "Feature filters cannot be selected or tuned using strategy P&L.",
                "pass_threshold": "threshold policy uses train-only labels and calibration metrics, not replay P&L",
            },
            {
                "gate_id": "P122_CALIBRATION_VALUE",
                "stage": "model_gate",
                "requirement": "A future model must improve calibration of cost/toxicity/realism labels over naive baselines.",
                "pass_threshold": "holdout Brier/log-loss improvement and monotonic risk buckets",
            },
            {
                "gate_id": "P122_BREADTH",
                "stage": "model_gate",
                "requirement": "A future filter must be valid across symbols and months, not a pocket.",
                "pass_threshold": ">=20 symbols and >=4 train months before pilot integration",
            },
            {
                "gate_id": "P122_INTEGRATION_ONLY_AFTER_FILTER_PASS",
                "stage": "integration_gate",
                "requirement": "Only after filter validation may future strategy candidates use it as a risk/abstention layer.",
                "pass_threshold": "filter_validation_pass == 1; still no profitability claim without downstream gates",
            },
        ]
    )


def build_candidate_model_queue(contract: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for idx, item in enumerate(contract.to_dict("records"), start=1):
        rows.append(
            {
                "priority": idx,
                "model_work_item": item["feature_source_id"],
                "first_deliverable": "label_matrix_and_baseline_diagnostics",
                "model_type_allowed": "calibrated_logistic_or_tree_model_only_after_label_matrix",
                "pilot_replay_allowed": False,
                "full_year_replay_allowed": False,
                "why": item["purpose"],
            }
        )
    return pd.DataFrame(rows)


def build_permission_gate(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    real_days = as_int(metric_value(tables["phase117"], "phase117_current_ready_real_anchor_days"))
    days_needed = as_int(metric_value(tables["phase117"], "phase117_additional_days_needed_for_min"))
    accepted_strategies = as_int(metric_value(tables["phase116"], "phase116_accepted_strategy_rows"))
    passive_allowed = as_int(metric_value(tables["phase121"], "phase121_passive_replay_allowed"))
    return pd.DataFrame(
        [
            {
                "permission_id": "P122_FILTER_DESIGN",
                "permission": "allowed",
                "evidence": "Designing non-trading filters is allowed because it does not reopen replay.",
            },
            {
                "permission_id": "P122_FILTER_MODEL_FIT",
                "permission": "closed_until_label_matrix_exists",
                "evidence": "No Phase122 label matrix has been built yet.",
            },
            {
                "permission_id": "P122_STRATEGY_REPLAY",
                "permission": "closed",
                "evidence": f"accepted_strategies={accepted_strategies}; passive_replay_allowed={passive_allowed}",
            },
            {
                "permission_id": "P122_REAL_ANCHOR_REPLAY",
                "permission": "closed",
                "evidence": f"ready_real_anchor_days={real_days}; additional_days_needed_for_min={days_needed}",
            },
        ]
    )


def build_acceptance_summary(
    prior: pd.DataFrame,
    contract: pd.DataFrame,
    gates: pd.DataFrame,
    queue: pd.DataFrame,
    permission: pd.DataFrame,
) -> pd.DataFrame:
    surviving_prior = int(pd.to_numeric(prior["survives_gate"], errors="coerce").fillna(0).sum())
    replay_open = int(permission.loc[permission["permission_id"].eq("P122_STRATEGY_REPLAY"), "permission"].astype(str).eq("allowed").sum())
    return pd.DataFrame(
        [
            ("phase122_prior_evidence_rows", int(len(prior)), "Prior evidence rows reviewed"),
            ("phase122_prior_surviving_replay_rows", surviving_prior, "Prior rows currently allowing replay"),
            ("phase122_feature_source_rows", int(len(contract)), "Non-trading feature sources precommitted"),
            ("phase122_validation_gate_rows", int(len(gates)), "Validation gates locked"),
            ("phase122_model_queue_rows", int(len(queue)), "Future model work items queued"),
            ("phase122_filter_design_allowed", 1, "1 means filter design may continue"),
            ("phase122_strategy_replay_allowed", replay_open, "1 means strategy replay may run"),
            ("phase122_next_best_action", "build_phase123_filter_label_matrix_no_replay", "Recommended next milestone"),
            ("phase122_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model retained for future cost/toxicity filters"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase122 Non-Trading Forecast Filter Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase122 opens a new admissible branch after taker and passive replay paths failed: non-trading forecast filters.",
        "These filters are not buy/sell strategies. They may only predict cost toxicity, realism risk, or abstention regimes until their own calibration gates pass.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase122_non_trading_forecast_filter_precommit_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def run_phase122(base_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    tables = {name: read_metric_table(base_dir / path) for name, path in INPUTS.items()}
    prior = build_prior_evidence(tables)
    contract = build_forecast_feature_contract()
    gates = build_validation_gates()
    queue = build_candidate_model_queue(contract)
    permission = build_permission_gate(tables)
    acceptance = build_acceptance_summary(prior, contract, gates, queue, permission)

    prior.to_csv(output_dir / "prior_replay_blocker_evidence.csv", index=False)
    contract.to_csv(output_dir / "non_trading_filter_feature_contract.csv", index=False)
    gates.to_csv(output_dir / "non_trading_filter_validation_gates.csv", index=False)
    queue.to_csv(output_dir / "filter_model_work_queue.csv", index=False)
    permission.to_csv(output_dir / "filter_permission_gate.csv", index=False)
    acceptance.to_csv(output_dir / "phase122_non_trading_filter_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Prior Replay Blocker Evidence": prior,
            "Non-Trading Filter Feature Contract": contract,
            "Validation Gates": gates,
            "Filter Model Work Queue": queue,
            "Permission Gate": permission,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase122_non_trading_forecast_filter_precommit",
        "strategy_replay_allowed": int(
            acceptance.loc[acceptance["metric"].eq("phase122_strategy_replay_allowed"), "value"].iloc[0]
        ),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase122",
            generated_utc=generated_utc,
            inputs={name: str(path) for name, path in INPUTS.items()},
            parameters={
                "branch_policy": "non_trading_filter_precommit_only",
                "replay_policy": "closed",
                "next_phase": "phase123_filter_label_matrix_no_replay",
            },
            outputs={
                "prior_evidence": str(output_dir / "prior_replay_blocker_evidence.csv"),
                "feature_contract": str(output_dir / "non_trading_filter_feature_contract.csv"),
                "validation_gates": str(output_dir / "non_trading_filter_validation_gates.csv"),
                "model_queue": str(output_dir / "filter_model_work_queue.csv"),
                "permission_gate": str(output_dir / "filter_permission_gate.csv"),
                "acceptance_summary": str(output_dir / "phase122_non_trading_filter_acceptance_summary.csv"),
                "report": str(output_dir / "phase122_non_trading_forecast_filter_precommit_report.md"),
                "manifest": str(output_dir / "phase122_non_trading_forecast_filter_precommit_manifest.json"),
            },
            random_seed="none_deterministic_precommit",
            scenario_ids="phase122_new_non_trading_filter_branch_after_replay_retirements",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_filter_precommit",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase122_non_trading_forecast_filter_precommit_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase122 non-trading forecast-filter precommit.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase122(args.base_dir, args.output_dir)


if __name__ == "__main__":
    main()
