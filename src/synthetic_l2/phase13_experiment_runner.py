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


def build_robustness_dimension_summary(
    ledger: pd.DataFrame,
    profile_ledger: pd.DataFrame,
    profile_summary: pd.DataFrame,
    signal_diagnostics: pd.DataFrame,
    seed_plan: pd.DataFrame,
    walk_forward_windows: pd.DataFrame,
    parameter_grid: pd.DataFrame,
    holdout_realism: pd.DataFrame,
) -> pd.DataFrame:
    strategy_ids = sorted(signal_diagnostics["strategy_id"].astype(str).unique().tolist())
    holdout_available_profiles = set()
    if not holdout_realism.empty and {"quarter_profile", "holdout_role", "structural_ready_for_holdout_proxy"}.issubset(holdout_realism.columns):
        holdout_available_profiles = set(
            holdout_realism[
                holdout_realism["structural_ready_for_holdout_proxy"].astype(bool)
                & holdout_realism["holdout_role"].astype(str).str.contains("holdout", case=False, na=False)
            ]["quarter_profile"].astype(str)
        )

    rows = []
    for strategy_id in strategy_ids:
        strategy_ledger = ledger[ledger["strategy_id"].astype(str) == strategy_id].copy()
        strategy_profile_ledger = profile_ledger[profile_ledger["strategy_id"].astype(str) == strategy_id].copy()
        strategy_profile_summary = profile_summary[profile_summary["strategy_id"].astype(str) == strategy_id].copy()
        strategy_grid = parameter_grid[parameter_grid["strategy_id"].astype(str) == strategy_id].copy()
        registered = not strategy_ledger.empty
        base = strategy_ledger[strategy_ledger["control_id"].astype(str) == "BASE"] if registered else pd.DataFrame()
        controls = strategy_ledger[strategy_ledger["control_id"].astype(str) != "BASE"] if registered else pd.DataFrame()
        profile_base = (
            strategy_profile_ledger[strategy_profile_ledger["control_id"].astype(str) == "BASE"]
            if not strategy_profile_ledger.empty
            else pd.DataFrame()
        )
        profile_quarters = set(profile_base["quarter_profile"].astype(str).unique().tolist()) if not profile_base.empty else set()
        holdout_profiles_present = profile_quarters.intersection(holdout_available_profiles)
        execution_profiles = (
            int(strategy_profile_ledger["execution_profile"].astype(str).nunique())
            if "execution_profile" in strategy_profile_ledger
            else 0
        )
        seeds_run = int(strategy_ledger["simulation_seed"].nunique()) if registered and "simulation_seed" in strategy_ledger else 0
        required_seeds = int(seed_plan["simulation_seed"].nunique()) if "simulation_seed" in seed_plan else 0
        initial_seed_rows = int(seed_plan["initial_engineering_seed"].sum()) if "initial_engineering_seed" in seed_plan else 0
        parameter_sets_planned = int(strategy_grid["parameter_set_id"].nunique()) if "parameter_set_id" in strategy_grid else 0
        parameter_sets_run = int(strategy_ledger["parameter_set_id"].nunique()) if registered and "parameter_set_id" in strategy_ledger else 0
        walk_forward_windows_planned = int(len(walk_forward_windows))
        negative_control_rows = int(len(controls))
        interpretable_controls = (
            int(controls["negative_control_interpretable"].astype(bool).sum())
            if not controls.empty and "negative_control_interpretable" in controls
            else 0
        )
        passed_controls = (
            int((controls["negative_control_result"].astype(str) == "pass_proxy").sum())
            if not controls.empty and "negative_control_result" in controls
            else 0
        )
        all_profiles_positive = (
            bool(strategy_profile_summary["all_profiles_positive"].astype(bool).any())
            if not strategy_profile_summary.empty and "all_profiles_positive" in strategy_profile_summary
            else False
        )
        stressed_profile_positive = (
            bool(strategy_profile_summary["stressed_profile_positive"].astype(bool).any())
            if not strategy_profile_summary.empty and "stressed_profile_positive" in strategy_profile_summary
            else False
        )
        dimension_status = (
            "robustness_proxy_dimensions_available_not_acceptance"
            if registered
            else "not_registered_for_phase13_proxy_run"
        )
        rows.append(
            {
                "strategy_id": strategy_id,
                "registered_for_phase13_proxy": bool(registered),
                "proxy_run_rows": int(len(strategy_ledger)),
                "profile_robustness_rows": int(len(strategy_profile_ledger)),
                "initial_engineering_seeds_run": seeds_run,
                "required_full_validation_seeds": required_seeds,
                "seed_scope_status": "initial_engineering_seed_proxy_only" if seeds_run else "not_run",
                "quarter_profiles_run": int(strategy_ledger["quarter_profile"].nunique()) if registered else 0,
                "execution_profiles_evaluated": execution_profiles,
                "all_execution_profiles_positive": all_profiles_positive,
                "stressed_profile_positive": stressed_profile_positive,
                "negative_control_rows": negative_control_rows,
                "interpretable_negative_control_rows": interpretable_controls,
                "passed_negative_control_rows": passed_controls,
                "parameter_sets_planned": parameter_sets_planned,
                "parameter_sets_run": parameter_sets_run,
                "parameter_smoothness_status": (
                    "design_available_single_parameter_proxy_run"
                    if parameter_sets_planned > parameter_sets_run > 0
                    else "not_registered_or_not_run"
                ),
                "walk_forward_windows_planned": walk_forward_windows_planned,
                "walk_forward_windows_run": 0,
                "walk_forward_status": "design_available_not_run",
                "holdout_generator_profiles_available": int(len(holdout_available_profiles)),
                "holdout_generator_profiles_present_in_proxy": int(len(holdout_profiles_present)),
                "holdout_status": (
                    "holdout_profiles_present_as_proxy_not_rerun_acceptance"
                    if len(holdout_profiles_present) > 0
                    else "holdout_proxy_not_present_for_strategy"
                ),
                "real_data_rerun_status": "not_available_one_day_seed_only",
                "dimension_status": dimension_status,
                "acceptance_eligible": False,
                "blocker": (
                    "Robustness proxy dimensions are now summarized, but acceptance still requires full required-seed "
                    "execution, walk-forward runs, parameter-neighborhood smoothness, holdout-generator strategy reruns "
                    "and later multi-day real-data reruns."
                    if registered
                    else "Strategy is not registered in the current Phase 13 alpha-parameter proxy grid; robustness acceptance evidence is missing."
                ),
            }
        )
    return pd.DataFrame(rows)


def build_robustness_acceptance_gap_ledger(dimension_summary: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "strategy_id",
        "robustness_requirement",
        "required_threshold",
        "observed_value",
        "current_evidence_status",
        "acceptance_requirement_met",
        "blocking_gap",
        "evidence_source",
        "required_next_evidence",
        "acceptance_eligible_now",
    ]
    if dimension_summary.empty:
        return pd.DataFrame(columns=columns)

    rows: list[dict] = []
    for row in dimension_summary.sort_values("strategy_id").to_dict("records"):
        strategy_id = row["strategy_id"]
        registered = bool(row.get("registered_for_phase13_proxy", False))
        required_seeds = int(row.get("required_full_validation_seeds", 0) or 0)
        observed_seeds = int(row.get("initial_engineering_seeds_run", 0) or 0)
        planned_parameters = int(row.get("parameter_sets_planned", 0) or 0)
        run_parameters = int(row.get("parameter_sets_run", 0) or 0)
        planned_walk_forward = int(row.get("walk_forward_windows_planned", 0) or 0)
        run_walk_forward = int(row.get("walk_forward_windows_run", 0) or 0)
        execution_profiles = int(row.get("execution_profiles_evaluated", 0) or 0)
        all_profiles_positive = bool(row.get("all_execution_profiles_positive", False))
        holdout_profiles_present = int(row.get("holdout_generator_profiles_present_in_proxy", 0) or 0)
        real_data_status = str(row.get("real_data_rerun_status", "not_available"))
        negative_controls = int(row.get("negative_control_rows", 0) or 0)
        passed_controls = int(row.get("passed_negative_control_rows", 0) or 0)

        requirements = [
            {
                "robustness_requirement": "registered_for_alpha_parameter_proxy_grid",
                "required_threshold": "strategy registered in Phase 13 proxy experiment grid",
                "observed_value": str(registered),
                "current_evidence_status": "registered_proxy" if registered else "not_registered",
                "acceptance_requirement_met": registered,
                "blocking_gap": "" if registered else "Strategy is not registered for the current alpha-parameter robustness proxy grid.",
                "required_next_evidence": "Register strategy in the applicable alpha-parameter experiment grid or classify it as non-alpha/risk-only before robustness acceptance.",
            },
            {
                "robustness_requirement": "full_validation_seed_coverage",
                "required_threshold": f"{required_seeds} required full-validation seeds",
                "observed_value": f"{observed_seeds} initial-engineering proxy seeds",
                "current_evidence_status": str(row.get("seed_scope_status", "")),
                "acceptance_requirement_met": registered and observed_seeds >= required_seeds and required_seeds > 0,
                "blocking_gap": "" if registered and observed_seeds >= required_seeds and required_seeds > 0 else "Only initial-engineering seed proxy coverage is complete; full required-seed execution is missing.",
                "required_next_evidence": "Execute all required full-validation seeds from outputs/phase13/seed_plan.csv.",
            },
            {
                "robustness_requirement": "execution_profile_robustness",
                "required_threshold": "all deployable/stress execution profiles positive and evaluated",
                "observed_value": f"{execution_profiles} profiles; all_profiles_positive={all_profiles_positive}",
                "current_evidence_status": "multi_profile_proxy_not_acceptance" if execution_profiles else "not_run",
                "acceptance_requirement_met": registered and execution_profiles >= 3 and all_profiles_positive,
                "blocking_gap": "" if registered and execution_profiles >= 3 and all_profiles_positive else "Current multi-profile proxy does not show positive results across all execution profiles.",
                "required_next_evidence": "Run full strategy registry across deployable and stressed execution profiles with acceptance-grade fills/costs.",
            },
            {
                "robustness_requirement": "parameter_neighborhood_smoothness",
                "required_threshold": f"{planned_parameters} predeclared parameter sets evaluated smoothly",
                "observed_value": f"{run_parameters} parameter set(s) run",
                "current_evidence_status": str(row.get("parameter_smoothness_status", "")),
                "acceptance_requirement_met": registered and planned_parameters > 0 and run_parameters >= planned_parameters,
                "blocking_gap": "" if registered and planned_parameters > 0 and run_parameters >= planned_parameters else "Only one/sparse parameter-set proxy evidence exists; parameter-neighborhood smoothness is missing.",
                "required_next_evidence": "Execute the full predeclared parameter grid and summarize neighborhood smoothness without final-test reuse.",
            },
            {
                "robustness_requirement": "walk_forward_coverage",
                "required_threshold": f"{planned_walk_forward} walk-forward windows run",
                "observed_value": f"{run_walk_forward} walk-forward windows run",
                "current_evidence_status": str(row.get("walk_forward_status", "")),
                "acceptance_requirement_met": registered and planned_walk_forward > 0 and run_walk_forward >= planned_walk_forward,
                "blocking_gap": "" if registered and planned_walk_forward > 0 and run_walk_forward >= planned_walk_forward else "Walk-forward design exists but no walk-forward windows have been executed.",
                "required_next_evidence": "Execute registered walk-forward windows and preserve train/test leakage checks.",
            },
            {
                "robustness_requirement": "holdout_generator_strategy_rerun",
                "required_threshold": "holdout-generator profiles rerun as strategy evidence",
                "observed_value": f"{holdout_profiles_present} holdout profiles present as proxy",
                "current_evidence_status": str(row.get("holdout_status", "")),
                "acceptance_requirement_met": False,
                "blocking_gap": "Holdout-generator profiles exist as realism/proxy evidence but strategy reruns are not acceptance-grade.",
                "required_next_evidence": "Run strategies on holdout-generator outputs and compare against calibration/development results.",
            },
            {
                "robustness_requirement": "negative_control_rejection",
                "required_threshold": "all interpretable negative controls rejected or degraded",
                "observed_value": f"{passed_controls}/{negative_controls} negative-control rows passed proxy criterion",
                "current_evidence_status": "proxy_negative_controls_available" if negative_controls else "not_available",
                "acceptance_requirement_met": registered and negative_controls > 0 and passed_controls == negative_controls,
                "blocking_gap": "" if registered and negative_controls > 0 and passed_controls == negative_controls else "Negative-control evidence is proxy-only or incomplete.",
                "required_next_evidence": "Run mandatory negative controls under full experiment execution and require rejection/degradation before promotion.",
            },
            {
                "robustness_requirement": "real_data_rerun",
                "required_threshold": "multi-day real-data rerun evidence available",
                "observed_value": real_data_status,
                "current_evidence_status": real_data_status,
                "acceptance_requirement_met": real_data_status == "multi_day_real_rerun_available",
                "blocking_gap": "Current evidence is one-day seed/synthetic only; multi-day real rerun is missing.",
                "required_next_evidence": "Collect and run multiple real market days, then compare stability against synthetic scenarios.",
            },
        ]
        for item in requirements:
            out = {
                "strategy_id": strategy_id,
                "evidence_source": (
                    "outputs/phase13/experiment_registry.csv; outputs/phase13/experiment_run_summary.csv; "
                    "outputs/phase13/experiment_profile_robustness_summary.csv; outputs/phase13/robustness_dimension_summary.csv"
                ),
                "acceptance_eligible_now": False,
            }
            out.update(item)
            rows.append(out)

    result = pd.DataFrame(rows)
    return result[columns].sort_values(["strategy_id", "robustness_requirement"], kind="mergesort")


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
    dimension_summary: pd.DataFrame,
    acceptance_gap_ledger: pd.DataFrame,
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
        "## Robustness Dimension Coverage Summary",
        "",
        _markdown_table(dimension_summary),
        "",
        "## Robustness Acceptance Gap Ledger",
        "",
        _markdown_table(acceptance_gap_ledger),
        "",
        "## Caveat",
        "",
        "The output closes the bookkeeping gap between a planned registry and auditable proxy run ledgers, including execution-profile sensitivity and dimension coverage, but it does not close the acceptance-grade robustness gate.",
        "",
    ]
    (output_dir / "experiment_run_smoke_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase13_experiment_smoke(
    registry_path: Path,
    signal_diagnostics_path: Path,
    execution_summary_path: Path,
    seed_plan_path: Path,
    walk_forward_windows_path: Path,
    parameter_grid_path: Path,
    holdout_realism_path: Path,
    output_dir: Path,
    execution_profile: str,
    robustness_profiles: list[str] | None = None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    registry = _read_csv(registry_path)
    signal_diagnostics = _read_csv(signal_diagnostics_path)
    execution_summary = _read_csv(execution_summary_path)
    seed_plan = _read_csv(seed_plan_path)
    walk_forward_windows = _read_csv(walk_forward_windows_path)
    parameter_grid = _read_csv(parameter_grid_path)
    holdout_realism = _read_csv(holdout_realism_path) if holdout_realism_path.exists() else pd.DataFrame()

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
    dimension_summary = build_robustness_dimension_summary(
        ledger=ledger,
        profile_ledger=profile_ledger,
        profile_summary=profile_summary,
        signal_diagnostics=signal_diagnostics,
        seed_plan=seed_plan,
        walk_forward_windows=walk_forward_windows,
        parameter_grid=parameter_grid,
        holdout_realism=holdout_realism,
    )
    acceptance_gap_ledger = build_robustness_acceptance_gap_ledger(dimension_summary)

    ledger.to_csv(output_dir / "experiment_run_ledger.csv", index=False)
    summary.to_csv(output_dir / "experiment_run_summary.csv", index=False)
    control_summary.to_csv(output_dir / "negative_control_run_summary.csv", index=False)
    profile_ledger.to_csv(output_dir / "experiment_profile_robustness_ledger.csv", index=False)
    profile_summary.to_csv(output_dir / "experiment_profile_robustness_summary.csv", index=False)
    dimension_summary.to_csv(output_dir / "robustness_dimension_summary.csv", index=False)
    acceptance_gap_ledger.to_csv(output_dir / "robustness_acceptance_gap_ledger.csv", index=False)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "registry_path": str(registry_path),
        "signal_diagnostics_path": str(signal_diagnostics_path),
        "execution_summary_path": str(execution_summary_path),
        "seed_plan_path": str(seed_plan_path),
        "walk_forward_windows_path": str(walk_forward_windows_path),
        "parameter_grid_path": str(parameter_grid_path),
        "holdout_realism_path": str(holdout_realism_path),
        "execution_profile": execution_profile,
        "registered_rows_evaluated": int(len(ledger)),
        "strategies": int(ledger["strategy_id"].nunique()),
        "controls": int(ledger["control_id"].nunique()),
        "robustness_execution_profiles": robustness_profiles,
        "profile_robustness_rows": int(len(profile_ledger)),
        "profile_robustness_summary_rows": int(len(profile_summary)),
        "robustness_dimension_summary_rows": int(len(dimension_summary)),
        "robustness_acceptance_gap_rows": int(len(acceptance_gap_ledger)),
        "robustness_acceptance_gap_open_rows": int((~acceptance_gap_ledger["acceptance_requirement_met"].astype(bool)).sum()) if len(acceptance_gap_ledger) else 0,
        "robustness_acceptance_ready_rows": int(acceptance_gap_ledger["acceptance_requirement_met"].astype(bool).sum()) if len(acceptance_gap_ledger) else 0,
        "robustness_dimension_registered_rows": int(dimension_summary["registered_for_phase13_proxy"].sum()) if len(dimension_summary) else 0,
        "robustness_dimension_holdout_proxy_rows": int(
            (dimension_summary["holdout_generator_profiles_present_in_proxy"] > 0).sum()
        ) if len(dimension_summary) else 0,
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
                "seed_plan_path": str(seed_plan_path),
                "walk_forward_windows_path": str(walk_forward_windows_path),
                "parameter_grid_path": str(parameter_grid_path),
                "holdout_realism_path": str(holdout_realism_path),
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
                "robustness_dimension_summary": str(output_dir / "robustness_dimension_summary.csv"),
                "robustness_acceptance_gap_ledger": str(output_dir / "robustness_acceptance_gap_ledger.csv"),
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
    write_report(output_dir, manifest, summary, control_summary, profile_summary, dimension_summary, acceptance_gap_ledger)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 13 deterministic experiment smoke ledger.")
    parser.add_argument("--registry", type=Path, default=Path("outputs/phase13/experiment_registry.csv"))
    parser.add_argument("--signal-diagnostics", type=Path, default=Path("outputs/phase11/strategy_signal_diagnostics.csv"))
    parser.add_argument("--execution-summary", type=Path, default=Path("outputs/phase12/execution_summary.csv"))
    parser.add_argument("--seed-plan", type=Path, default=Path("outputs/phase13/seed_plan.csv"))
    parser.add_argument("--walk-forward-windows", type=Path, default=Path("outputs/phase13/walk_forward_windows.csv"))
    parser.add_argument("--parameter-grid", type=Path, default=Path("outputs/phase13/parameter_grid.csv"))
    parser.add_argument("--holdout-realism", type=Path, default=Path("outputs/phase14/holdout_generator_realism_summary.csv"))
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
        seed_plan_path=args.seed_plan,
        walk_forward_windows_path=args.walk_forward_windows,
        parameter_grid_path=args.parameter_grid,
        holdout_realism_path=args.holdout_realism,
        output_dir=args.output_dir,
        execution_profile=args.execution_profile,
        robustness_profiles=args.robustness_profiles,
    )


if __name__ == "__main__":
    main()
