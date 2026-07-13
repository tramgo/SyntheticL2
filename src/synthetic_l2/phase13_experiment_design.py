from __future__ import annotations

import argparse
import itertools
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


SPLITS = [
    ("calibration_development", 1, 30, "feature construction and rough thresholds"),
    ("validation", 31, 45, "model/threshold selection"),
    ("untouched_test", 46, 63, "final quarter evaluation"),
]


NEGATIVE_CONTROLS = [
    ("NC01", "shuffle_signal_time_bucket", "Shuffle signal within same time-of-day bucket; preserves intraday seasonality."),
    ("NC02", "delayed_signal", "Delay signal by one or more decision horizons."),
    ("NC03", "inverted_signal", "Invert signal direction while preserving turnover."),
    ("NC04", "random_matched_turnover", "Random direction with matched strategy turnover and holding horizon."),
    ("NC05", "no_predictive_coupling_data", "Run on synthetic data generated without predictive coupling."),
    ("NC06", "zero_cost_vs_realistic_cost", "Compare zero-cost control against configured cost schedule."),
    ("NC07", "zero_latency_vs_realistic_latency", "Compare zero latency against retail/stressed profiles."),
    ("NC08", "hide_regime_labels", "Suppress regime labels for regime-aware strategies."),
    ("NC09", "cross_ticker_timestamp_shift", "Shift cross-ticker timestamps to detect lead-lag leakage."),
]


STRATEGY_GRIDS = {
    "S01": {"lookback": [1, 3, 5], "mlofi_quantile": [0.7, 0.8, 0.9], "spread_max_ticks": [2, 5]},
    "S02": {"ofi_quantile": [0.6, 0.8, 0.9], "horizon": ["next_event", "5m"]},
    "S03": {"withdrawal_proxy_quantile": [0.75, 0.85, 0.95], "intensity_quantile": [0.75, 0.9]},
    "S04": {"mlofi_quantile": [0.6, 0.8], "intensity_quantile": [0.7, 0.9]},
    "S05": {"microprice_deviation_quantile": [0.7, 0.8, 0.9]},
    "S06": {"intensity_quantile": [0.8, 0.9], "price_progress_max_quantile": [0.1, 0.2]},
    "S07": {"imbalance_quantile": [0.8, 0.9], "regime_gate": ["strict", "loose"]},
    "S08": {"market_factor_quantile": [0.7, 0.8, 0.9], "lag_events": [1, 2, 3]},
    "S09": {"l1_imbalance_quantile": [0.6, 0.8, 0.9], "latency_profile": ["zero", "retail", "stressed"]},
}


def load_calendar(path: Path) -> pd.DataFrame:
    return pd.read_csv(path).sort_values(["quarter_profile", "scenario_day"], kind="mergesort").reset_index(drop=True)


def build_data_splits(calendar: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for row in calendar.to_dict("records"):
        segment = next(name for name, start, end, _ in SPLITS if start <= int(row["scenario_day"]) <= end)
        purpose = next(purpose for name, _, _, purpose in SPLITS if name == segment)
        out = dict(row)
        out["experiment_segment"] = segment
        out["segment_purpose"] = purpose
        out["shuffle_allowed"] = False
        rows.append(out)
    return pd.DataFrame(rows)


def build_seed_plan(profiles: list[str], initial_seeds: int = 3, full_seeds: int = 10) -> pd.DataFrame:
    rows = []
    for profile_index, profile in enumerate(sorted(profiles), start=1):
        for seed_ordinal in range(1, full_seeds + 1):
            rows.append(
                {
                    "quarter_profile": profile,
                    "seed_ordinal": seed_ordinal,
                    "simulation_seed": 900_000 + profile_index * 10_000 + seed_ordinal,
                    "initial_engineering_seed": seed_ordinal <= initial_seeds,
                    "required_for_full_validation": True,
                }
            )
    return pd.DataFrame(rows)


def build_walk_forward_windows(calendar: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for profile in sorted(calendar["quarter_profile"].unique()):
        for mode in ["fixed_20_train_5_test", "expanding_train_5_test"]:
            start = 1
            while True:
                if mode == "fixed_20_train_5_test":
                    train_start, train_end = start, start + 19
                else:
                    train_start, train_end = 1, start + 19
                test_start, test_end = train_end + 1, train_end + 5
                if test_end > 63:
                    break
                rows.append(
                    {
                        "quarter_profile": profile,
                        "window_mode": mode,
                        "train_start_day": train_start,
                        "train_end_day": train_end,
                        "test_start_day": test_start,
                        "test_end_day": test_end,
                        "roll_step_days": 5,
                    }
                )
                start += 5
    return pd.DataFrame(rows)


def build_parameter_grid() -> pd.DataFrame:
    rows = []
    for strategy_id, params in STRATEGY_GRIDS.items():
        names = list(params)
        values = [params[name] for name in names]
        for combo_id, combo in enumerate(itertools.product(*values), start=1):
            rows.append(
                {
                    "strategy_id": strategy_id,
                    "parameter_set_id": f"{strategy_id}_P{combo_id:03d}",
                    "parameters_json": json.dumps(dict(zip(names, combo)), sort_keys=True),
                    "predeclared": True,
                    "max_tuning_segment": "validation",
                    "final_test_reuse_allowed": False,
                }
            )
    return pd.DataFrame(rows)


def build_negative_controls() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "negative_control_id": control_id,
                "control_name": name,
                "implementation_requirement": requirement,
                "mandatory": True,
                "promotion_blocks_if_failed": True,
            }
            for control_id, name, requirement in NEGATIVE_CONTROLS
        ]
    )


def build_experiment_registry(
    seed_plan: pd.DataFrame,
    parameter_grid: pd.DataFrame,
    negative_controls: pd.DataFrame,
) -> pd.DataFrame:
    engineering_seeds = seed_plan[seed_plan["initial_engineering_seed"]].copy()
    strategies = sorted(parameter_grid["strategy_id"].unique())
    rows = []
    experiment_id = 1
    for _, seed in engineering_seeds.iterrows():
        for strategy_id in strategies:
            first_param = parameter_grid[parameter_grid["strategy_id"] == strategy_id].iloc[0]
            for control_id in ["BASE", *negative_controls["negative_control_id"].head(3).tolist()]:
                rows.append(
                    {
                        "experiment_id": f"EXP13_{experiment_id:06d}",
                        "quarter_profile": seed["quarter_profile"],
                        "simulation_seed": int(seed["simulation_seed"]),
                        "strategy_id": strategy_id,
                        "parameter_set_id": first_param["parameter_set_id"],
                        "control_id": control_id,
                        "segment_scope": "calibration_development_and_validation_only",
                        "status": "planned_not_run",
                        "retain_failed_run": True,
                    }
                )
                experiment_id += 1
    return pd.DataFrame(rows)


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


def write_report(output_dir: Path, splits: pd.DataFrame, seeds: pd.DataFrame, windows: pd.DataFrame, grid: pd.DataFrame, controls: pd.DataFrame, registry: pd.DataFrame) -> None:
    segment_summary = splits.groupby(["quarter_profile", "experiment_segment"], sort=True).agg(days=("scenario_day", "count")).reset_index()
    grid_summary = grid.groupby("strategy_id", sort=True).agg(parameter_sets=("parameter_set_id", "count")).reset_index()
    lines = [
        "# Phase 13 Experiment Design Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase defines experiment splits, seed plans, walk-forward windows, predeclared parameter grids and negative controls.",
        "It does not run or promote strategy results.",
        "",
        "## Segment Summary",
        "",
        _markdown_table(segment_summary),
        "",
        "## Seed Plan",
        "",
        f"- Quarter profiles: {seeds['quarter_profile'].nunique()}",
        f"- Full validation seeds: {len(seeds)}",
        f"- Initial engineering seeds: {int(seeds['initial_engineering_seed'].sum())}",
        "",
        "## Walk-Forward Windows",
        "",
        f"- Windows: {len(windows)}",
        "",
        "## Parameter Sets",
        "",
        _markdown_table(grid_summary),
        "",
        "## Negative Controls",
        "",
        _markdown_table(controls[["negative_control_id", "control_name", "mandatory"]]),
        "",
        "## Registry Skeleton",
        "",
        f"- Planned initial experiments: {len(registry)}",
        "",
    ]
    (output_dir / "phase13_experiment_design_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase13(calendar_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    calendar = load_calendar(calendar_path)
    splits = build_data_splits(calendar)
    seeds = build_seed_plan(calendar["quarter_profile"].unique().tolist())
    windows = build_walk_forward_windows(calendar)
    grid = build_parameter_grid()
    controls = build_negative_controls()
    registry = build_experiment_registry(seeds, grid, controls)

    splits.to_csv(output_dir / "data_splits.csv", index=False)
    seeds.to_csv(output_dir / "seed_plan.csv", index=False)
    windows.to_csv(output_dir / "walk_forward_windows.csv", index=False)
    grid.to_csv(output_dir / "parameter_grid.csv", index=False)
    controls.to_csv(output_dir / "negative_controls.csv", index=False)
    registry.to_csv(output_dir / "experiment_registry.csv", index=False)
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "calendar_path": str(calendar_path),
        "split_days": {name: end - start + 1 for name, start, end, _ in SPLITS},
        "quarter_profiles": int(calendar["quarter_profile"].nunique()),
        "calendar_rows": int(len(calendar)),
        "seed_rows": int(len(seeds)),
        "walk_forward_windows": int(len(windows)),
        "parameter_sets": int(len(grid)),
        "negative_controls": int(len(controls)),
        "planned_initial_experiments": int(len(registry)),
        "not_strategy_results": True,
    }
    (output_dir / "experiment_design_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, splits, seeds, windows, grid, controls, registry)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 13 experiment design artifacts.")
    parser.add_argument("--calendar-path", type=Path, default=Path("outputs/phase4/scenario_calendar.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase13"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase13(args.calendar_path, args.output_dir)


if __name__ == "__main__":
    main()
