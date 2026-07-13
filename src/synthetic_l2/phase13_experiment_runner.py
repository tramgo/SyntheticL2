from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


CONTROL_TRANSFORMS = {
    "BASE": {
        "net_multiplier": 1.0,
        "predictive_multiplier": 1.0,
        "signal_fraction_multiplier": 1.0,
        "description": "Registered base experiment using current proxy evidence.",
    },
    "NC01": {
        "net_multiplier": 0.05,
        "predictive_multiplier": 0.02,
        "signal_fraction_multiplier": 1.0,
        "description": "Shuffle-within-time-bucket proxy: preserves turnover but removes most predictive coupling.",
    },
    "NC02": {
        "net_multiplier": 0.35,
        "predictive_multiplier": 0.35,
        "signal_fraction_multiplier": 0.9,
        "description": "Delayed-signal proxy: degrades signal edge and modestly reduces executable turnover.",
    },
    "NC03": {
        "net_multiplier": -1.0,
        "predictive_multiplier": -1.0,
        "signal_fraction_multiplier": 1.0,
        "description": "Inverted-signal proxy: reverses directional edge while preserving turnover.",
    },
}


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def _pick_execution_profile(execution: pd.DataFrame, profile: str) -> pd.DataFrame:
    if "execution_profile" not in execution:
        raise ValueError("execution summary is missing execution_profile")
    selected = execution[execution["execution_profile"].astype(str) == profile].copy()
    if selected.empty:
        raise ValueError(f"execution profile not found: {profile}")
    return selected


def build_experiment_run_ledger(
    registry: pd.DataFrame,
    signal_diagnostics: pd.DataFrame,
    execution_summary: pd.DataFrame,
    execution_profile: str,
) -> pd.DataFrame:
    selected_execution = _pick_execution_profile(execution_summary, execution_profile)

    signal_cols = [
        "strategy_id",
        "support_level",
        "rows_evaluated",
        "signal_rows",
        "signal_fraction",
        "mean_future_return_when_signaled",
        "signed_mean_future_return",
        "directional_accuracy_nonzero",
    ]
    execution_cols = [
        "strategy_id",
        "trades",
        "mean_gross_return",
        "mean_cost_return",
        "mean_net_return",
        "win_rate_net",
        "total_net_pnl_units",
        "status",
    ]
    signal = signal_diagnostics[[column for column in signal_cols if column in signal_diagnostics]].copy()
    execution = selected_execution[[column for column in execution_cols if column in selected_execution]].copy()
    execution = execution.rename(columns={"status": "phase12_status"})

    merged = registry.merge(signal, on="strategy_id", how="left").merge(execution, on="strategy_id", how="left")
    rows = []
    for row in merged.to_dict("records"):
        control_id = str(row["control_id"])
        transform = CONTROL_TRANSFORMS.get(control_id, CONTROL_TRANSFORMS["BASE"])
        base_net = float(row.get("mean_net_return", 0.0) or 0.0)
        base_pnl = float(row.get("total_net_pnl_units", 0.0) or 0.0)
        base_signal_fraction = float(row.get("signal_fraction", 0.0) or 0.0)
        base_signed_return = float(row.get("signed_mean_future_return", 0.0) or 0.0)
        base_directional_accuracy = float(row.get("directional_accuracy_nonzero", 0.5) or 0.5)
        proxy_net = base_net * transform["net_multiplier"]
        proxy_pnl = base_pnl * transform["net_multiplier"]
        proxy_signed_return = base_signed_return * transform["predictive_multiplier"]
        proxy_signal_fraction = base_signal_fraction * transform["signal_fraction_multiplier"]
        proxy_directional_accuracy = 0.5 + (base_directional_accuracy - 0.5) * abs(transform["predictive_multiplier"])
        if control_id == "NC03":
            proxy_directional_accuracy = 1.0 - base_directional_accuracy

        negative_control_interpretable = control_id != "BASE" and base_net > 0
        if control_id == "BASE":
            negative_control_result = "base_case"
        elif not negative_control_interpretable:
            negative_control_result = "not_interpretable_base_not_positive"
        elif proxy_net <= max(0.0, base_net * 0.25):
            negative_control_result = "pass_proxy"
        else:
            negative_control_result = "fail_proxy"

        out = dict(row)
        out.update(
            {
                "execution_profile": execution_profile,
                "run_status": "executed_proxy_smoke_not_acceptance",
                "proxy_control_description": transform["description"],
                "proxy_signal_fraction": proxy_signal_fraction,
                "proxy_signed_mean_future_return": proxy_signed_return,
                "proxy_directional_accuracy_nonzero": proxy_directional_accuracy,
                "proxy_mean_net_return": proxy_net,
                "proxy_total_net_pnl_units": proxy_pnl,
                "negative_control_interpretable": negative_control_interpretable,
                "negative_control_result": negative_control_result,
                "parameter_smoothness_status": "not_evaluated_single_parameter_set",
                "walk_forward_status": "not_evaluated_static_proxy_inputs",
                "holdout_status": "not_evaluated_calibration_validation_scope_only",
                "acceptance_eligible": False,
            }
        )
        rows.append(out)
    return pd.DataFrame(rows)


def build_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for strategy_id, group in ledger.groupby("strategy_id", sort=True):
        bases = group[group["control_id"].astype(str) == "BASE"]
        controls = group[group["control_id"].astype(str) != "BASE"]
        interpretable = controls[controls["negative_control_interpretable"].astype(bool)]
        passed = interpretable[interpretable["negative_control_result"].astype(str) == "pass_proxy"]
        rows.append(
            {
                "strategy_id": strategy_id,
                "run_rows": int(len(group)),
                "base_rows": int(len(bases)),
                "negative_control_rows": int(len(controls)),
                "interpretable_negative_control_rows": int(len(interpretable)),
                "passed_negative_control_rows": int(len(passed)),
                "positive_base_rows": int((bases["proxy_mean_net_return"] > 0).sum()),
                "median_base_net_return": float(bases["proxy_mean_net_return"].median()) if not bases.empty else 0.0,
                "worst_control_net_return": float(controls["proxy_mean_net_return"].min()) if not controls.empty else 0.0,
                "robustness_smoke_status": "executed_proxy_smoke_not_acceptance",
                "acceptance_eligible": False,
                "blocker": "Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing.",
            }
        )
    return pd.DataFrame(rows)


def build_control_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    return (
        ledger.groupby("control_id", sort=True)
        .agg(
            run_rows=("experiment_id", "count"),
            strategies=("strategy_id", "nunique"),
            mean_proxy_net_return=("proxy_mean_net_return", "mean"),
            mean_proxy_signal_fraction=("proxy_signal_fraction", "mean"),
            interpretable_rows=("negative_control_interpretable", "sum"),
        )
        .reset_index()
    )


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


def write_report(output_dir: Path, manifest: dict, summary: pd.DataFrame, control_summary: pd.DataFrame) -> None:
    lines = [
        "# Phase 13 Experiment Run Smoke Report",
        "",
        f"Generated UTC: {manifest['generated_utc']}",
        "",
        "## Scope",
        "",
        "This is a deterministic engineering smoke ledger over the pre-registered Phase 13 initial experiment rows.",
        "It uses existing Phase 11 signal diagnostics and Phase 12 execution summaries; it is not a full experiment execution, parameter search, walk-forward result or promotion result.",
        "",
        "## Manifest Summary",
        "",
        f"- Registered rows evaluated: {manifest['registered_rows_evaluated']}",
        f"- Strategies: {manifest['strategies']}",
        f"- Controls: {manifest['controls']}",
        f"- Execution profile: {manifest['execution_profile']}",
        f"- Acceptance eligible: {manifest['acceptance_eligible']}",
        "",
        "## Strategy Robustness Smoke Summary",
        "",
        _markdown_table(summary),
        "",
        "## Control Summary",
        "",
        _markdown_table(control_summary),
        "",
        "## Caveat",
        "",
        "The output closes the bookkeeping gap between a planned registry and an auditable proxy run ledger, but it does not close the acceptance-grade robustness gate.",
        "",
    ]
    (output_dir / "experiment_run_smoke_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase13_experiment_smoke(
    registry_path: Path,
    signal_diagnostics_path: Path,
    execution_summary_path: Path,
    output_dir: Path,
    execution_profile: str,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    registry = _read_csv(registry_path)
    signal_diagnostics = _read_csv(signal_diagnostics_path)
    execution_summary = _read_csv(execution_summary_path)

    ledger = build_experiment_run_ledger(registry, signal_diagnostics, execution_summary, execution_profile)
    summary = build_summary(ledger)
    control_summary = build_control_summary(ledger)

    ledger.to_csv(output_dir / "experiment_run_ledger.csv", index=False)
    summary.to_csv(output_dir / "experiment_run_summary.csv", index=False)
    control_summary.to_csv(output_dir / "negative_control_run_summary.csv", index=False)

    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "registry_path": str(registry_path),
        "signal_diagnostics_path": str(signal_diagnostics_path),
        "execution_summary_path": str(execution_summary_path),
        "execution_profile": execution_profile,
        "registered_rows_evaluated": int(len(ledger)),
        "strategies": int(ledger["strategy_id"].nunique()),
        "controls": int(ledger["control_id"].nunique()),
        "base_rows": int((ledger["control_id"].astype(str) == "BASE").sum()),
        "negative_control_rows": int((ledger["control_id"].astype(str) != "BASE").sum()),
        "acceptance_eligible": False,
        "run_scope": "deterministic_proxy_smoke_not_full_experiment",
    }
    (output_dir / "experiment_run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, manifest, summary, control_summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 13 deterministic experiment smoke ledger.")
    parser.add_argument("--registry", type=Path, default=Path("outputs/phase13/experiment_registry.csv"))
    parser.add_argument("--signal-diagnostics", type=Path, default=Path("outputs/phase11/strategy_signal_diagnostics.csv"))
    parser.add_argument("--execution-summary", type=Path, default=Path("outputs/phase12/execution_summary.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase13"))
    parser.add_argument("--execution-profile", default="retail_marketable_default")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase13_experiment_smoke(
        registry_path=args.registry,
        signal_diagnostics_path=args.signal_diagnostics,
        execution_summary_path=args.execution_summary,
        output_dir=args.output_dir,
        execution_profile=args.execution_profile,
    )


if __name__ == "__main__":
    main()
