from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


LIFECYCLE_ECONOMIC_ACCEPTANCE_CRITERIA = [
    ("strategy_full_run_coverage", "Full event/tick lifecycle replay covers every supported strategy/profile/fill model.", "all supported strategies have preserved order/fill lineage"),
    ("daily_equity_curve_and_halt_coverage", "Daily equity, halt, resume and blocked-trading state is persisted from the replay engine.", "daily risk state is complete and reconciled to lifecycle fills"),
    ("guardrail_validation", "Daily loss, drawdown and position guardrails are enforced and validated on replay state.", "no unresolved deployable guardrail breach before promotion"),
    ("tail_loss_validation", "Tail-loss distribution is computed from replay fills under current and strict profiles.", "tail loss remains within approved capital limits"),
    ("documented_cost_formula_validation", "Documented Zerodha formula evidence is retained and reconciled to broker notes where available.", "documented formula plus broker contract-note reconciliation clears"),
    ("latency_slippage_acceptance_run", "Latency/slippage stress is replayed through the event lifecycle engine.", "retail and stressed profiles pass under calibrated latency/slippage"),
    ("net_profitability_validation", "Retail and stressed profiles remain net-positive after realistic costs.", "retail/stress and stressed-only net profitability pass"),
    ("risk_adjusted_economic_validation", "Economic P&L and lifecycle risk state jointly pass.", "risk-adjusted economic joint pass clears for deployable profiles"),
]


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    text = frame.copy()
    for column in text.columns:
        text[column] = text[column].map(lambda value: "" if pd.isna(value) else str(value))
    headers = [str(column) for column in text.columns]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |" for row in text.values.tolist())
    return "\n".join(lines)


def build_acceptance_criteria() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "criterion_id": criterion_id,
                "criterion_description": description,
                "acceptance_threshold": threshold,
                "current_status": "contract_defined_not_acceptance_evidence",
            }
            for criterion_id, description, threshold in LIFECYCLE_ECONOMIC_ACCEPTANCE_CRITERIA
        ]
    )


def _strategy_agg(frame: pd.DataFrame, strategy_col: str = "strategy_id") -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame({strategy_col: []})
    return frame.groupby(strategy_col, sort=True).first().reset_index()


def _status(row: pd.Series) -> str:
    support = str(row.get("strategy_support_level", ""))
    requirement = str(row.get("hardening_requirement", ""))
    if support == "not_supported_by_current_product":
        return "blocked_by_unsupported_strategy_scope"
    if support == "partial_missing_required_features":
        return "blocked_by_partial_strategy_support"
    if requirement in {
        "strategy_full_run_coverage",
        "daily_equity_curve_and_halt_coverage",
        "daily_loss_limit_validation",
        "drawdown_breach_validation",
        "position_limit_validation",
        "tail_loss_validation",
    }:
        return "lifecycle_risk_proxy_not_acceptance_grade"
    if requirement == "zerodha_order_formula_ready":
        return "zerodha_formula_proxy_contract_note_missing"
    if requirement == "latency_slippage_stress_confirmation":
        return "latency_slippage_proxy_not_acceptance_replay"
    if requirement in {"retail_and_stress_net_positive", "stressed_profile_net_positive"}:
        return "net_profitability_proxy_not_acceptance_grade"
    if requirement == "risk_adjusted_economic_joint_pass":
        return "risk_adjusted_joint_pass_proxy_failed_or_missing"
    return "lifecycle_economic_requirement_open"


def _observed_metric(row: pd.Series) -> str:
    requirement = str(row.get("hardening_requirement", ""))
    if requirement == "strategy_full_run_coverage":
        return f"lifecycle_orders={row.get('orders', '')}; lifecycle_rows={row.get('lifecycle_rows', '')}; risk_evidence_scope={row.get('risk_evidence_scope', '')}; not_acceptance_grade={row.get('not_acceptance_grade', '')}"
    if requirement == "daily_equity_curve_and_halt_coverage":
        return f"daily_risk_rows={row.get('daily_risk_rows', '')}; daily_halt_rows={row.get('daily_halt_rows', '')}; trade_dates={row.get('trade_dates', '')}"
    if requirement == "daily_loss_limit_validation":
        return f"daily_loss_breach_days={row.get('daily_loss_breach_days', '')}; breach_days={row.get('breach_days', '')}; risk_severity_band={row.get('risk_severity_band', '')}"
    if requirement == "drawdown_breach_validation":
        return f"drawdown_breach_days={row.get('drawdown_breach_days', '')}; max_intraday_drawdown_inr={row.get('max_intraday_drawdown_inr', '')}"
    if requirement == "position_limit_validation":
        return f"position_limit_breach_days={row.get('position_limit_breach_days', '')}; max_abs_position_units={row.get('max_abs_position_units', '')}"
    if requirement == "tail_loss_validation":
        return f"tail_loss_1pct_filled_pnl_inr={row.get('tail_loss_1pct_filled_pnl_inr', '')}; current_limit_pass_rows={row.get('current_limit_pass_rows', '')}"
    if requirement == "zerodha_order_formula_ready":
        return f"documented_zerodha_formula_ready={row.get('documented_zerodha_formula_ready', '')}; broker_contract_note_reconciliation_ready={row.get('broker_contract_note_reconciliation_ready', '')}; missing_reconciliation_items={row.get('missing_reconciliation_items', '')}"
    if requirement == "latency_slippage_stress_confirmation":
        return f"retail_stress_rows={row.get('retail_stress_rows', '')}; stressed_profile_rows={row.get('stressed_profile_rows', '')}; status={row.get('economic_frontier_status', '')}"
    if requirement == "retail_and_stress_net_positive":
        return f"retail_stress_net_positive_proxy_rows={row.get('retail_stress_net_positive_proxy_rows', '')}; retail_stress_rows={row.get('retail_stress_rows', '')}"
    if requirement == "stressed_profile_net_positive":
        return f"stressed_net_positive_proxy_rows={row.get('stressed_net_positive_proxy_rows', '')}; stressed_profile_rows={row.get('stressed_profile_rows', '')}"
    if requirement == "risk_adjusted_economic_joint_pass":
        return f"risk_adjusted_joint_pass_rows={row.get('risk_adjusted_joint_pass_rows', '')}; retail_stress_joint_pass_rows={row.get('retail_stress_net_positive_and_risk_pass_proxy_rows', '')}"
    return str(row.get("observed_value", ""))


def build_lifecycle_economic_ledger(
    execution_roadmap: pd.DataFrame,
    lifecycle: pd.DataFrame,
    daily: pd.DataFrame,
    severity: pd.DataFrame,
    limit_sensitivity: pd.DataFrame,
    economic: pd.DataFrame,
    risk_adjusted: pd.DataFrame,
    reconciliation: pd.DataFrame,
    support: pd.DataFrame,
) -> pd.DataFrame:
    m05 = execution_roadmap[
        execution_roadmap["execution_milestone"].astype(str) == "M05_full_lifecycle_risk_and_economic_replay"
    ].copy()

    lifecycle_agg = lifecycle.groupby("strategy_id", sort=True).agg(
        lifecycle_rows=("strategy_id", "size"),
        orders=("orders", "sum"),
        trade_dates=("trade_dates", "max"),
        mean_fill_ratio=("mean_fill_ratio", "mean"),
        risk_adjusted_net_pnl_inr=("risk_adjusted_net_pnl_inr", "sum"),
        daily_halt_rows=("daily_halt_rows", "sum"),
        position_limit_breach_rows=("position_limit_breach_rows", "sum"),
        risk_evidence_scope=("risk_evidence_scope", "first"),
        not_acceptance_grade=("not_acceptance_grade", "max"),
    ).reset_index()
    daily_agg = daily.groupby("strategy_id", sort=True).agg(
        daily_risk_rows=("strategy_id", "size"),
        daily_loss_limit_breach_rows=("daily_loss_limit_breach_rows", "sum"),
        daily_halt_rows_daily=("daily_halt_rows", "sum"),
    ).reset_index()
    severity_agg = severity.groupby("strategy_id", sort=True).agg(
        breach_days=("breach_days", "max"),
        daily_loss_breach_days=("daily_loss_breach_days", "max"),
        position_limit_breach_days=("position_limit_breach_days", "max"),
        drawdown_breach_days=("drawdown_breach_days", "max"),
        tail_loss_1pct_filled_pnl_inr=("tail_loss_1pct_filled_pnl_inr", "min"),
        max_intraday_drawdown_inr=("max_intraday_drawdown_inr", "min"),
        max_abs_position_units=("max_abs_position_units", "max"),
        risk_severity_band=("risk_severity_band", "first"),
        risk_pass_candidate_proxy=("risk_pass_candidate_proxy", "max"),
    ).reset_index()
    current_limits = limit_sensitivity[limit_sensitivity["risk_limit_profile"].astype(str).eq("current_proxy_limits")]
    limit_agg = current_limits.groupby("strategy_id", sort=True).agg(
        current_limit_pass_rows=("risk_pass_candidate_under_limit_profile", "sum"),
        current_limit_rows=("strategy_id", "size"),
    ).reset_index()
    econ_agg = economic.groupby("strategy_id", sort=True).agg(
        economic_frontier_rows=("strategy_id", "size"),
        retail_stress_rows=("retail_or_stress_profile", "sum"),
        net_positive_proxy_rows=("net_positive_proxy", "sum"),
        retail_stress_net_positive_proxy_rows=("net_positive_proxy", lambda s: int((s & economic.loc[s.index, "retail_or_stress_profile"]).sum())),
        stressed_profile_rows=("execution_profile", lambda s: int((s.astype(str) == "stressed_retail").sum())),
        stressed_net_positive_proxy_rows=("net_positive_proxy", lambda s: int((s & (economic.loc[s.index, "execution_profile"].astype(str) == "stressed_retail")).sum())),
        economic_frontier_status=("economic_frontier_status", "first"),
    ).reset_index()
    risk_econ_agg = risk_adjusted.groupby("strategy_id", sort=True).agg(
        risk_adjusted_joint_pass_rows=("net_positive_and_risk_pass_proxy", "sum"),
        retail_stress_net_positive_and_risk_pass_proxy_rows=("retail_stress_net_positive_and_risk_pass_proxy", "sum"),
    ).reset_index()

    rows = (
        m05.merge(lifecycle_agg, on="strategy_id", how="left")
        .merge(daily_agg, on="strategy_id", how="left")
        .merge(severity_agg, on="strategy_id", how="left")
        .merge(limit_agg, on="strategy_id", how="left")
        .merge(econ_agg, on="strategy_id", how="left")
        .merge(risk_econ_agg, on="strategy_id", how="left")
        .merge(reconciliation, on="strategy_id", how="left")
        .merge(support[["strategy_id", "strategy_support_closure_status", "required_support_action"]], on="strategy_id", how="left")
    )
    rows = rows.fillna("")
    rows["lifecycle_economic_status"] = rows.apply(_status, axis=1)
    rows["observed_lifecycle_economic_metric"] = rows.apply(_observed_metric, axis=1)
    rows["risk_replay_required"] = rows["gate_id"].astype(str).eq("G04_risk")
    rows["economic_replay_required"] = rows["gate_id"].astype(str).eq("G02_economic")
    rows["broker_reconciliation_required"] = rows["hardening_requirement"].astype(str).eq("zerodha_order_formula_ready")
    rows["guardrail_validation_required"] = rows["hardening_requirement"].astype(str).isin(
        {"daily_loss_limit_validation", "drawdown_breach_validation", "position_limit_validation"}
    )
    rows["acceptance_requirement_met_after_contract"] = False
    rows["blocking_gap_after_contract"] = rows.apply(
        lambda row: (
            f"Support closure required first: {row.get('required_support_action', '')}"
            if str(row.get("strategy_support_closure_status", "")).startswith("requires_")
            else "Lifecycle/risk/economic evidence remains proxy-only or blocked by missing broker fill and contract-note reconciliation."
        ),
        axis=1,
    )
    rows["required_lifecycle_economic_action"] = rows.apply(
        lambda row: (
            "Run acceptance-grade lifecycle risk replay with preserved order/fill/equity-state lineage."
            if row["risk_replay_required"]
            else "Run acceptance-grade economic replay with broker/fill/cost reconciliation and retail/stressed profile checks."
        ),
        axis=1,
    )
    columns = [
        "execution_rank", "gate_id", "strategy_id", "strategy_support_level", "strategy_role",
        "hardening_requirement", "action_class", "dependency_status", "strategy_support_closure_status",
        "lifecycle_economic_status", "observed_lifecycle_economic_metric", "lifecycle_rows", "orders",
        "daily_risk_rows", "breach_days", "risk_severity_band", "risk_pass_candidate_proxy",
        "current_limit_pass_rows", "economic_frontier_rows", "retail_stress_net_positive_proxy_rows",
        "stressed_net_positive_proxy_rows", "risk_adjusted_joint_pass_rows",
        "documented_zerodha_formula_ready", "broker_contract_note_reconciliation_ready",
        "missing_reconciliation_items", "risk_replay_required", "economic_replay_required",
        "broker_reconciliation_required", "guardrail_validation_required",
        "acceptance_requirement_met_after_contract", "blocking_gap_after_contract",
        "required_lifecycle_economic_action", "required_next_evidence",
    ]
    for column in columns:
        if column not in rows:
            rows[column] = False if column.endswith("_required") else ""
    return rows[columns].sort_values("execution_rank", kind="mergesort")


def build_gap_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    return ledger.groupby("lifecycle_economic_status", sort=True).agg(
        rows=("hardening_requirement", "size"),
        strategies=("strategy_id", "nunique"),
        acceptance_met_rows=("acceptance_requirement_met_after_contract", "sum"),
    ).reset_index().sort_values(["rows", "lifecycle_economic_status"], ascending=[False, True], kind="mergesort")


def build_strategy_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    grouped = ledger.groupby(["strategy_id", "strategy_support_level", "strategy_role"], sort=True).agg(
        m05_rows=("hardening_requirement", "size"),
        risk_replay_rows=("risk_replay_required", "sum"),
        economic_replay_rows=("economic_replay_required", "sum"),
        broker_reconciliation_rows=("broker_reconciliation_required", "sum"),
        guardrail_validation_rows=("guardrail_validation_required", "sum"),
        acceptance_met_rows=("acceptance_requirement_met_after_contract", "sum"),
        first_required_action=("required_lifecycle_economic_action", "first"),
    ).reset_index()
    grouped["lifecycle_economic_contract_status"] = "proxy_or_support_blocked_not_acceptance"
    return grouped


def write_report(output_dir: Path, criteria: pd.DataFrame, ledger: pd.DataFrame, gap_summary: pd.DataFrame, strategy_summary: pd.DataFrame) -> None:
    lines = [
        "# Phase 20 M05 Lifecycle Risk and Economic Replay Contract",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase converts the fifth Phase 20 execution milestone into a lifecycle risk and economic replay contract.",
        "It joins current Phase 12 lifecycle risk/economic proxy artifacts and Phase 16 reconciliation ledgers to the M05 roadmap while keeping every row non-acceptance-ready until broker/fill/contract-note reconciliation and acceptance-grade replay exist.",
        "",
        "## Acceptance Criteria Contract",
        "",
        _markdown_table(criteria),
        "",
        "## Lifecycle/Economic Gap Summary",
        "",
        _markdown_table(gap_summary),
        "",
        "## Strategy Summary",
        "",
        _markdown_table(strategy_summary),
        "",
        "## M05 Lifecycle/Economic Replay Ledger",
        "",
        _markdown_table(ledger),
        "",
    ]
    (output_dir / "phase20_m05_lifecycle_economic_replay_contract_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase20_m05(paths: dict[str, Path], output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    criteria = build_acceptance_criteria()
    ledger = build_lifecycle_economic_ledger(
        pd.read_csv(paths["execution_roadmap"]),
        pd.read_csv(paths["full_run_lifecycle_risk_summary"]),
        pd.read_csv(paths["full_run_lifecycle_daily_risk_summary"]),
        pd.read_csv(paths["full_run_lifecycle_risk_breach_severity"]),
        pd.read_csv(paths["full_run_lifecycle_risk_limit_sensitivity"]),
        pd.read_csv(paths["economic_viability_frontier"]),
        pd.read_csv(paths["risk_adjusted_economic_frontier"]),
        pd.read_csv(paths["economic_reconciliation_strategy_summary"]),
        pd.read_csv(paths["strategy_support_decision_summary"]),
    )
    gap_summary = build_gap_summary(ledger)
    strategy_summary = build_strategy_summary(ledger)
    criteria.to_csv(output_dir / "lifecycle_economic_acceptance_criteria.csv", index=False)
    ledger.to_csv(output_dir / "lifecycle_economic_replay_ledger.csv", index=False)
    gap_summary.to_csv(output_dir / "lifecycle_economic_gap_summary.csv", index=False)
    strategy_summary.to_csv(output_dir / "lifecycle_economic_strategy_summary.csv", index=False)
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "lifecycle_economic_acceptance_criteria_rows": int(len(criteria)),
        "lifecycle_economic_replay_rows": int(len(ledger)),
        "lifecycle_economic_gap_summary_rows": int(len(gap_summary)),
        "lifecycle_economic_strategy_rows": int(len(strategy_summary)),
        "risk_replay_required_rows": int(ledger["risk_replay_required"].astype(bool).sum()),
        "economic_replay_required_rows": int(ledger["economic_replay_required"].astype(bool).sum()),
        "broker_reconciliation_required_rows": int(ledger["broker_reconciliation_required"].astype(bool).sum()),
        "guardrail_validation_required_rows": int(ledger["guardrail_validation_required"].astype(bool).sum()),
        "acceptance_met_after_contract_rows": int(ledger["acceptance_requirement_met_after_contract"].astype(bool).sum()),
        "scope": "phase20_m05_lifecycle_economic_replay_contract_not_acceptance",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase20_m05",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={"lifecycle_economic_acceptance_criteria": LIFECYCLE_ECONOMIC_ACCEPTANCE_CRITERIA},
            outputs={
                "lifecycle_economic_acceptance_criteria": str(output_dir / "lifecycle_economic_acceptance_criteria.csv"),
                "lifecycle_economic_replay_ledger": str(output_dir / "lifecycle_economic_replay_ledger.csv"),
                "lifecycle_economic_gap_summary": str(output_dir / "lifecycle_economic_gap_summary.csv"),
                "lifecycle_economic_strategy_summary": str(output_dir / "lifecycle_economic_strategy_summary.csv"),
                "report": str(output_dir / "phase20_m05_lifecycle_economic_replay_contract_report.md"),
                "manifest": str(output_dir / "lifecycle_economic_replay_contract_manifest.json"),
            },
            random_seed="not_applicable_deterministic_lifecycle_economic_contract",
            scenario_ids="phase20_M05_full_lifecycle_risk_and_economic_replay_rows",
            cost_model_version="phase12_zerodha_order_formula_proxy_contract_note_missing",
            latency_model_version="phase12_execution_profiles_proxy_not_acceptance_grade",
            base_dir=base_dir,
        )
    )
    (output_dir / "lifecycle_economic_replay_contract_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, criteria, ledger, gap_summary, strategy_summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 20 M05 lifecycle risk and economic replay contract artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase20_m05"))
    parser.add_argument("--execution-roadmap", type=Path, default=Path("outputs/phase20/acceptance_execution_roadmap.csv"))
    parser.add_argument("--full-run-lifecycle-risk-summary", type=Path, default=Path("outputs/phase12/full_run_lifecycle_risk_summary.csv"))
    parser.add_argument("--full-run-lifecycle-daily-risk-summary", type=Path, default=Path("outputs/phase12/full_run_lifecycle_daily_risk_summary.csv"))
    parser.add_argument("--full-run-lifecycle-risk-breach-severity", type=Path, default=Path("outputs/phase12/full_run_lifecycle_risk_breach_severity.csv"))
    parser.add_argument("--full-run-lifecycle-risk-limit-sensitivity", type=Path, default=Path("outputs/phase12/full_run_lifecycle_risk_limit_sensitivity.csv"))
    parser.add_argument("--economic-viability-frontier", type=Path, default=Path("outputs/phase16/economic_viability_frontier.csv"))
    parser.add_argument("--risk-adjusted-economic-frontier", type=Path, default=Path("outputs/phase16/risk_adjusted_economic_frontier.csv"))
    parser.add_argument("--economic-reconciliation-strategy-summary", type=Path, default=Path("outputs/phase16/economic_reconciliation_strategy_summary.csv"))
    parser.add_argument("--strategy-support-decision-summary", type=Path, default=Path("outputs/phase20_m02/strategy_support_decision_summary.csv"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "execution_roadmap": args.execution_roadmap,
        "full_run_lifecycle_risk_summary": args.full_run_lifecycle_risk_summary,
        "full_run_lifecycle_daily_risk_summary": args.full_run_lifecycle_daily_risk_summary,
        "full_run_lifecycle_risk_breach_severity": args.full_run_lifecycle_risk_breach_severity,
        "full_run_lifecycle_risk_limit_sensitivity": args.full_run_lifecycle_risk_limit_sensitivity,
        "economic_viability_frontier": args.economic_viability_frontier,
        "risk_adjusted_economic_frontier": args.risk_adjusted_economic_frontier,
        "economic_reconciliation_strategy_summary": args.economic_reconciliation_strategy_summary,
        "strategy_support_decision_summary": args.strategy_support_decision_summary,
    }
    run_phase20_m05(paths, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
