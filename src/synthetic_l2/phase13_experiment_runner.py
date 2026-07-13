from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


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


def build_profile_robustness_ledger(
    registry: pd.DataFrame,
    signal_diagnostics: pd.DataFrame,
    execution_summary: pd.DataFrame,
    execution_profiles: list[str],
) -> pd.DataFrame:
    ledgers = []
    for profile in execution_profiles:
        profile_ledger = build_experiment_run_ledger(
            registry=registry,
            signal_diagnostics=signal_diagnostics,
            execution_summary=execution_summary,
            execution_profile=profile,
        )
        profile_ledger["robustness_axis"] = "execution_profile"
        ledgers.append(profile_ledger)
    return pd.concat(ledgers, ignore_index=True) if ledgers else pd.DataFrame()


def build_profile_robustness_summary(profile_ledger: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if profile_ledger.empty:
        return pd.DataFrame(
            columns=[
                "strategy_id",
                "execution_profiles_evaluated",
                "base_profile_rows",
                "positive_base_profiles",
                "all_profiles_positive",
                "retail_profile_positive",
                "stressed_profile_positive",
                "worst_profile_base_net_return",
                "best_profile_base_net_return",
                "profile_base_net_return_range",
                "interpretable_negative_control_rows",
                "passed_negative_control_rows",
                "profile_robustness_status",
                "acceptance_eligible",
                "blocker",
            ]
        )

    for strategy_id, group in profile_ledger.groupby("strategy_id", sort=True):
        bases = group[group["control_id"].astype(str) == "BASE"].copy()
        profile_base = (
            bases.groupby("execution_profile", sort=True)
            .agg(median_base_net_return=("proxy_mean_net_return", "median"))
            .reset_index()
        )
        controls = group[group["control_id"].astype(str) != "BASE"]
        interpretable = controls[controls["negative_control_interpretable"].astype(bool)]
        passed = interpretable[interpretable["negative_control_result"].astype(str) == "pass_proxy"]
        positive_profiles = profile_base[profile_base["median_base_net_return"] > 0]
        profile_values = profile_base["median_base_net_return"].astype(float)
        rows.append(
            {
                "strategy_id": strategy_id,
                "execution_profiles_evaluated": int(profile_base["execution_profile"].nunique()),
                "base_profile_rows": int(len(profile_base)),
                "positive_base_profiles": int(len(positive_profiles)),
                "all_profiles_positive": bool(len(profile_base) > 0 and len(positive_profiles) == len(profile_base)),
                "retail_profile_positive": bool(
                    (
                        profile_base[
                            profile_base["execution_profile"].astype(str) == "retail_marketable_default"
                        ]["median_base_net_return"]
                        > 0
                    ).any()
                ),
                "stressed_profile_positive": bool(
                    (
                        profile_base[profile_base["execution_profile"].astype(str) == "stressed_retail"][
                            "median_base_net_return"
                        ]
                        > 0
                    ).any()
                ),
                "worst_profile_base_net_return": float(profile_values.min()) if len(profile_values) else 0.0,
                "best_profile_base_net_return": float(profile_values.max()) if len(profile_values) else 0.0,
                "profile_base_net_return_range": float(profile_values.max() - profile_values.min()) if len(profile_values) else 0.0,
                "interpretable_negative_control_rows": int(len(interpretable)),
                "passed_negative_control_rows": int(len(passed)),
                "profile_robustness_status": "multi_profile_proxy_not_acceptance",
                "acceptance_eligible": False,
                "blocker": (
                    "Multi-profile proxy robustness evidence exists, but full multi-seed, walk-forward, "
                    "parameter-smoothness, holdout-generator and real-data rerun evidence is still missing."
                ),
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


def write_report(
    output_dir: Path,
    manifest: dict,
    summary: pd.DataFrame,
    control_summary: pd.DataFrame,
    profile_summary: pd.DataFrame,
) -> None:
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
        f"- Robustness execution profiles: {manifest['robustness_execution_profiles']}",
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
        "## Multi-Profile Robustness Proxy Summary",
        "",
        _markdown_table(profile_summary),
        "",
        "## Caveat",
        "",
        "The output closes the bookkeeping gap between a planned registry and auditable proxy run ledgers, including execution-profile sensitivity, but it does not close the acceptance-grade robustness gate.",
        "",
    ]
    (output_dir / "experiment_run_smoke_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase13_experiment_smoke(
    registry_path: Path,
    signal_diagnostics_path: Path,
    execution_summary_path: Path,
    output_dir: Path,
    execution_profile: str,
    robustness_profiles: list[str] | None = None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    registry = _read_csv(registry_path)
    signal_diagnostics = _read_csv(signal_diagnostics_path)
    execution_summary = _read_csv(execution_summary_path)

    ledger = build_experiment_run_ledger(registry, signal_diagnostics, execution_summary, execution_profile)
    summary = build_summary(ledger)
    control_summary = build_control_summary(ledger)
    if robustness_profiles is None:
        robustness_profiles = sorted(execution_summary["execution_profile"].astype(str).unique().tolist())
    profile_ledger = build_profile_robustness_ledger(
        registry=registry,
        signal_diagnostics=signal_diagnostics,
        execution_summary=execution_summary,
        execution_profiles=robustness_profiles,
    )
    profile_summary = build_profile_robustness_summary(profile_ledger)

    ledger.to_csv(output_dir / "experiment_run_ledger.csv", index=False)
    summary.to_csv(output_dir / "experiment_run_summary.csv", index=False)
    control_summary.to_csv(output_dir / "negative_control_run_summary.csv", index=False)
    profile_ledger.to_csv(output_dir / "experiment_profile_robustness_ledger.csv", index=False)
    profile_summary.to_csv(output_dir / "experiment_profile_robustness_summary.csv", index=False)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "registry_path": str(registry_path),
        "signal_diagnostics_path": str(signal_diagnostics_path),
        "execution_summary_path": str(execution_summary_path),
        "execution_profile": execution_profile,
        "registered_rows_evaluated": int(len(ledger)),
        "strategies": int(ledger["strategy_id"].nunique()),
        "controls": int(ledger["control_id"].nunique()),
        "robustness_execution_profiles": robustness_profiles,
        "profile_robustness_rows": int(len(profile_ledger)),
        "profile_robustness_summary_rows": int(len(profile_summary)),
        "base_rows": int((ledger["control_id"].astype(str) == "BASE").sum()),
        "negative_control_rows": int((ledger["control_id"].astype(str) != "BASE").sum()),
        "acceptance_eligible": False,
        "run_scope": "deterministic_proxy_smoke_and_profile_robustness_not_full_experiment",
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase13_smoke_run",
            generated_utc=generated_utc,
            inputs={
                "registry_path": str(registry_path),
                "signal_diagnostics_path": str(signal_diagnostics_path),
                "execution_summary_path": str(execution_summary_path),
            },
            parameters={
                "execution_profile": execution_profile,
                "robustness_execution_profiles": robustness_profiles,
                "run_scope": manifest["run_scope"],
                "control_transforms": CONTROL_TRANSFORMS,
            },
            outputs={
                "experiment_run_ledger": str(output_dir / "experiment_run_ledger.csv"),
                "experiment_run_summary": str(output_dir / "experiment_run_summary.csv"),
                "negative_control_run_summary": str(output_dir / "negative_control_run_summary.csv"),
                "experiment_profile_robustness_ledger": str(output_dir / "experiment_profile_robustness_ledger.csv"),
                "experiment_profile_robustness_summary": str(output_dir / "experiment_profile_robustness_summary.csv"),
                "report": str(output_dir / "experiment_run_smoke_report.md"),
                "manifest": str(output_dir / "experiment_run_manifest.json"),
            },
            random_seed="outputs/phase13/seed_plan.csv_via_experiment_registry",
            scenario_ids="outputs/phase13/experiment_registry.csv",
            cost_model_version="outputs/phase12/cost_schedule.csv_and_zerodha_order_formula_v2",
            latency_model_version="outputs/phase12/execution_profiles.csv",
        )
    )
    (output_dir / "experiment_run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, manifest, summary, control_summary, profile_summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 13 deterministic experiment smoke ledger.")
    parser.add_argument("--registry", type=Path, default=Path("outputs/phase13/experiment_registry.csv"))
    parser.add_argument("--signal-diagnostics", type=Path, default=Path("outputs/phase11/strategy_signal_diagnostics.csv"))
    parser.add_argument("--execution-summary", type=Path, default=Path("outputs/phase12/execution_summary.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase13"))
    parser.add_argument("--execution-profile", default="retail_marketable_default")
    parser.add_argument(
        "--robustness-profiles",
        nargs="*",
        default=None,
        help="Execution profiles to include in the multi-profile robustness proxy. Defaults to all profiles in Phase 12 execution_summary.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase13_experiment_smoke(
        registry_path=args.registry,
        signal_diagnostics_path=args.signal_diagnostics,
        execution_summary_path=args.execution_summary,
        output_dir=args.output_dir,
        execution_profile=args.execution_profile,
        robustness_profiles=args.robustness_profiles,
    )


if __name__ == "__main__":
    main()
