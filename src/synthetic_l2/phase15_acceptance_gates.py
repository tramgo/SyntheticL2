from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


GATES = [
    {
        "gate_id": "G01_predictive",
        "gate_name": "Predictive gate",
        "requirement": "Stable signal-response relationship, baseline improvement, multi-seed stability, no ticker/template dependence.",
    },
    {
        "gate_id": "G02_economic",
        "gate_name": "Economic gate",
        "requirement": "Positive after realistic costs, slippage stress, retail latency, adequate edge versus spread, acceptable turnover.",
    },
    {
        "gate_id": "G03_robustness",
        "gate_name": "Robustness gate",
        "requirement": "Works in intended regimes, deactivates in hostile regimes, adjacent parameters are smooth, not day-concentrated.",
    },
    {
        "gate_id": "G04_risk",
        "gate_name": "Risk gate",
        "requirement": "Controlled drawdown, bounded position size, tail loss understood, effective daily loss limit.",
    },
    {
        "gate_id": "G05_realism",
        "gate_name": "Realism gate",
        "requirement": "No generator-artifact exploitation; viable with holdout configs, feed imperfections and pessimistic execution.",
    },
]


def load_inputs(paths: dict[str, Path]) -> dict[str, pd.DataFrame]:
    inputs = {
        "strategy_matrix": pd.read_csv(paths["strategy_matrix"]),
        "signal_diagnostics": pd.read_csv(paths["signal_diagnostics"]),
        "execution_summary": pd.read_csv(paths["execution_summary"]),
        "cost_schedule": pd.read_csv(paths["cost_schedule"]),
        "experiment_registry": pd.read_csv(paths["experiment_registry"]),
        "quality_summary": pd.read_csv(paths["quality_summary"]),
    }
    run_summary_path = paths.get("experiment_run_summary")
    if run_summary_path is not None and run_summary_path.exists():
        inputs["experiment_run_summary"] = pd.read_csv(run_summary_path)
    else:
        inputs["experiment_run_summary"] = pd.DataFrame()
    return inputs


def gate_definitions() -> pd.DataFrame:
    return pd.DataFrame(GATES)


def _exec_row(execution: pd.DataFrame, strategy_id: str, profile: str) -> pd.Series | None:
    rows = execution[(execution["strategy_id"] == strategy_id) & (execution["execution_profile"] == profile)]
    return rows.iloc[0] if len(rows) else None


def evaluate_strategy(strategy: pd.Series, inputs: dict[str, pd.DataFrame]) -> list[dict]:
    sid = strategy["strategy_id"]
    signal = inputs["signal_diagnostics"][inputs["signal_diagnostics"]["strategy_id"] == sid]
    signal_row = signal.iloc[0] if len(signal) else None
    execution = inputs["execution_summary"]
    cost_schedule = inputs["cost_schedule"]
    registry = inputs["experiment_registry"]
    run_summary = inputs["experiment_run_summary"]
    quality = inputs["quality_summary"]
    quality_fail = int((quality["status"] == "fail").sum()) if "status" in quality else 0
    quality_warn = int((quality["status"] == "warn").sum()) if "status" in quality else 0
    planned_experiments = int((registry["strategy_id"] == sid).sum()) if "strategy_id" in registry else 0
    run_rows = 0
    robustness_evidence_source = "outputs/phase13/experiment_registry.csv"
    robustness_blocker = (
        "No Phase 13 proxy smoke row is registered for this strategy; no completed multi-seed, "
        "walk-forward, parameter-smoothness, holdout or real-data rerun evidence."
    )
    if not run_summary.empty and "strategy_id" in run_summary:
        strategy_run = run_summary[run_summary["strategy_id"] == sid]
        if len(strategy_run):
            run_rows = int(strategy_run.iloc[0].get("run_rows", 0))
            robustness_evidence_source = "outputs/phase13/experiment_registry.csv; outputs/phase13/experiment_run_summary.csv"
            robustness_blocker = (
                "Phase 13 has a deterministic proxy smoke ledger, but no acceptance-grade full multi-seed, "
                "walk-forward, parameter-smoothness, holdout or real-data rerun evidence."
            )
    runnable = strategy["support_level"] in {"runnable_proxy", "partial_missing_required_features"}
    retail = _exec_row(execution, sid, "retail_marketable_default")
    stressed = _exec_row(execution, sid, "stressed_retail")
    required_cost_components = {
        "profile_fee_bps",
        "impact_bps",
        "half_spread",
        "fixed_slippage_ticks",
        "partial_fill_opportunity_cost",
        "statutory_and_brokerage_charges",
    }
    present_cost_components = set(cost_schedule["cost_component"].astype(str)) if "cost_component" in cost_schedule else set()
    has_proxy_cost_basis = required_cost_components.issubset(present_cost_components)
    statutory_placeholder = (
        "formula_or_source" in cost_schedule
        and (
            cost_schedule.loc[
                cost_schedule["cost_component"].astype(str) == "statutory_and_brokerage_charges",
                "formula_or_source",
            ].astype(str)
            == "not_verified_v1"
        ).any()
    )

    rows: list[dict] = []

    predictive_pass = (
        runnable
        and signal_row is not None
        and pd.notna(signal_row.get("directional_accuracy_nonzero"))
        and float(signal_row["directional_accuracy_nonzero"]) >= 0.52
    )
    rows.append(
        {
            "strategy_id": sid,
            "gate_id": "G01_predictive",
            "gate_status": "pass" if predictive_pass else "blocked",
            "evidence_value": None if signal_row is None else signal_row.get("directional_accuracy_nonzero"),
            "blocker": "" if predictive_pass else "No acceptance-level predictive evidence; current diagnostics are proxy-only and/or directional accuracy below threshold.",
            "evidence_source": "outputs/phase11/strategy_signal_diagnostics.csv",
        }
    )

    economic_pass = (
        retail is not None
        and stressed is not None
        and float(retail["mean_net_return"]) > 0
        and float(stressed["mean_net_return"]) > 0
    )
    economic_blocker = []
    if retail is None or stressed is None:
        economic_blocker.append("missing retail/stressed execution profile")
    else:
        if float(retail["mean_net_return"]) <= 0:
            economic_blocker.append("retail profile mean_net_return not positive")
        if float(stressed["mean_net_return"]) <= 0:
            economic_blocker.append("stressed profile mean_net_return not positive")
    if has_proxy_cost_basis and statutory_placeholder:
        economic_blocker.append("statutory/brokerage charges are not verified; current cost schedule is placeholder only")
        economic_blocker.append("execution result is still a 5-minute proxy and not acceptance evidence")
    elif has_proxy_cost_basis:
        economic_blocker.append("execution result is still a 5-minute proxy and not acceptance evidence")
    else:
        economic_blocker.append("missing required proxy cost schedule components")
    rows.append(
        {
            "strategy_id": sid,
            "gate_id": "G02_economic",
            "gate_status": "blocked",
            "evidence_value": None if retail is None else retail.get("mean_net_return"),
            "blocker": "; ".join(economic_blocker),
            "evidence_source": "outputs/phase12/execution_summary.csv; outputs/phase12/cost_schedule.csv",
        }
    )

    robustness_pass = False
    rows.append(
        {
            "strategy_id": sid,
            "gate_id": "G03_robustness",
            "gate_status": "blocked",
            "evidence_value": f"planned={planned_experiments};smoke_run_rows={run_rows}",
            "blocker": robustness_blocker,
            "evidence_source": robustness_evidence_source,
        }
    )

    rows.append(
        {
            "strategy_id": sid,
            "gate_id": "G04_risk",
            "gate_status": "blocked",
            "evidence_value": None,
            "blocker": "Only sampled proxy risk-control evidence exists; no acceptance-grade full-run drawdown, position-limit, tail-loss or daily-loss-limit validation exists.",
            "evidence_source": "outputs/phase12/execution_summary.csv; outputs/phase12_order_lifecycle/risk_control_summary.csv",
        }
    )

    realism_pass = quality_fail == 0 and quality_warn == 0 and runnable and strategy["support_level"] == "runnable_proxy"
    rows.append(
        {
            "strategy_id": sid,
            "gate_id": "G05_realism",
            "gate_status": "pass" if realism_pass else "blocked",
            "evidence_value": f"fail={quality_fail};warn={quality_warn};support={strategy['support_level']}",
            "blocker": "" if realism_pass else "Synthetic quality has warnings and/or strategy only has proxy/partial support; no holdout generator evidence.",
            "evidence_source": "outputs/phase14/quality_gate_summary.csv; outputs/phase11/strategy_validation_matrix.csv",
        }
    )
    return rows


def evaluate(inputs: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    matrix = inputs["strategy_matrix"].copy()
    gate_rows: list[dict] = []
    for _, strategy in matrix.iterrows():
        gate_rows.extend(evaluate_strategy(strategy, inputs))
    gates = pd.DataFrame(gate_rows).merge(gate_definitions(), on="gate_id", how="left")
    summary_rows = []
    for sid, group in gates.groupby("strategy_id", sort=True):
        blocked = int((group["gate_status"] != "pass").sum())
        passed = int((group["gate_status"] == "pass").sum())
        summary_rows.append(
            {
                "strategy_id": sid,
                "passed_gates": passed,
                "blocked_gates": blocked,
                "total_gates": int(len(group)),
                "promotion_allowed": False,
                "acceptance_status": "blocked_not_promotable",
                "primary_blockers": " | ".join(group[group["gate_status"] != "pass"]["blocker"].head(5).tolist()),
            }
        )
    summary = pd.DataFrame(summary_rows).merge(
        matrix[["strategy_id", "name", "role", "support_level"]],
        on="strategy_id",
        how="left",
    )
    blockers = gates[gates["gate_status"] != "pass"][
        ["strategy_id", "gate_id", "gate_name", "blocker", "evidence_source"]
    ].reset_index(drop=True)
    return gates, summary, blockers


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    text = frame.copy()
    for column in text.columns:
        text[column] = text[column].map(lambda value: "" if pd.isna(value) else str(value))
    headers = [str(column) for column in text.columns]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in text.values.tolist())
    return "\n".join(lines)


def write_report(output_dir: Path, gates: pd.DataFrame, summary: pd.DataFrame, blockers: pd.DataFrame) -> None:
    status_summary = gates.groupby(["gate_id", "gate_name", "gate_status"], sort=True).size().reset_index(name="strategies")
    lines = [
        "# Phase 15 Strategy Acceptance Gates Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase evaluates whether each strategy may advance from synthetic screening.",
        "Current evidence is insufficient for promotion; all promotion_allowed flags are false.",
        "",
        "## Gate Status Summary",
        "",
        _markdown_table(status_summary),
        "",
        "## Strategy Summary",
        "",
        _markdown_table(summary[["strategy_id", "name", "support_level", "passed_gates", "blocked_gates", "promotion_allowed", "acceptance_status"]]),
        "",
        "## Top Blockers",
        "",
        _markdown_table(blockers.head(30)),
        "",
    ]
    (output_dir / "phase15_acceptance_gates_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase15(output_dir: Path, paths: dict[str, Path]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    inputs = load_inputs(paths)
    definitions = gate_definitions()
    gates, summary, blockers = evaluate(inputs)
    definitions.to_csv(output_dir / "gate_definitions.csv", index=False)
    gates.to_csv(output_dir / "strategy_gate_results.csv", index=False)
    summary.to_csv(output_dir / "strategy_acceptance_summary.csv", index=False)
    blockers.to_csv(output_dir / "acceptance_blockers.csv", index=False)
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {key: str(value) for key, value in paths.items()},
        "strategies": int(summary["strategy_id"].nunique()),
        "gate_rows": int(len(gates)),
        "promoted_strategies": int(summary["promotion_allowed"].sum()),
        "blocked_strategies": int((~summary["promotion_allowed"]).sum()),
        "not_promotion_result": True,
        "promotion_allowed_requires_all_gates_pass": True,
    }
    (output_dir / "acceptance_gates_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, gates, summary, blockers)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate Phase 15 strategy acceptance gates.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase15"))
    parser.add_argument("--strategy-matrix", type=Path, default=Path("outputs/phase11/strategy_validation_matrix.csv"))
    parser.add_argument("--signal-diagnostics", type=Path, default=Path("outputs/phase11/strategy_signal_diagnostics.csv"))
    parser.add_argument("--execution-summary", type=Path, default=Path("outputs/phase12/execution_summary.csv"))
    parser.add_argument("--cost-schedule", type=Path, default=Path("outputs/phase12/cost_schedule.csv"))
    parser.add_argument("--experiment-registry", type=Path, default=Path("outputs/phase13/experiment_registry.csv"))
    parser.add_argument("--experiment-run-summary", type=Path, default=Path("outputs/phase13/experiment_run_summary.csv"))
    parser.add_argument("--quality-summary", type=Path, default=Path("outputs/phase14/quality_gate_summary.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "strategy_matrix": args.strategy_matrix,
        "signal_diagnostics": args.signal_diagnostics,
        "execution_summary": args.execution_summary,
        "cost_schedule": args.cost_schedule,
        "experiment_registry": args.experiment_registry,
        "experiment_run_summary": args.experiment_run_summary,
        "quality_summary": args.quality_summary,
    }
    run_phase15(args.output_dir, paths)


if __name__ == "__main__":
    main()
