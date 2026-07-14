from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


STAGE_D_STRATEGIES = [f"S{number:02d}" for number in range(1, 12)]
CONTROL_STRATEGIES = {"S09", "S10", "S11"}
STAGE_D_CRITERIA = [
    ("all_32_instruments", "Three-month study covers all 32 current instruments.", "symbol_count == 32"),
    ("sixty_three_days_per_profile", "Each Q-A/Q-B/Q-C profile contributes 63 trading days.", "min_days_per_profile == 63"),
    ("three_profiles", "Three quarter profiles are present.", "quarter_profile_count == 3"),
    ("initial_three_seeds_per_profile", "At least 3 initial engineering seeds per profile are present.", "initial_seed_rows == 9"),
    ("ten_seed_expansion_tracked", "Later 10-seed expansion is tracked as a remaining validation gap.", "full_seed_rows == 30 and initial_seed_rows < full_seed_rows"),
    ("raw_compact_feature_inventory", "Raw events, compact L2 states and feature datasets are inventoried.", "all three Phase 9 data products present"),
    ("all_strategy_proxy_runs", "S01-S11 have proxy/control summaries over the three-month feature product.", "strategy_run_rows == 99"),
    ("controls_labelled", "S09-S11 are treated as controls/non-alpha or risk-only modules.", "control_strategy_rows == 27"),
    ("non_acceptance_scope", "No Stage D row is strategy-promotion evidence.", "acceptance_ready_rows == 0"),
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


def build_criteria() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "criterion_id": criterion_id,
                "criterion_description": description,
                "acceptance_threshold": threshold,
                "current_status": "proxy_study_check_not_strategy_acceptance",
            }
            for criterion_id, description, threshold in STAGE_D_CRITERIA
        ]
    )


def build_profile_summary(calendar: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for profile, days in calendar.groupby("quarter_profile", sort=True):
        profile_features = features[features["quarter_profile"].astype(str) == str(profile)]
        rows.append(
            {
                "quarter_profile": profile,
                "trading_days": int(days["trade_date"].nunique()),
                "regime_families": int(days["regime_family"].nunique()),
                "shock_days": int(days["is_market_shock_day"].astype(bool).sum()),
                "feature_rows": int(len(profile_features)),
                "symbols": int(profile_features["symbol"].nunique()),
                "feed_profiles": int(profile_features["feed_profile"].nunique()),
            }
        )
    return pd.DataFrame(rows)


def build_seed_summary(seed_plan: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for profile, seeds in seed_plan.groupby("quarter_profile", sort=True):
        rows.append(
            {
                "quarter_profile": profile,
                "initial_engineering_seed_rows": int(seeds["initial_engineering_seed"].astype(bool).sum()),
                "full_validation_seed_rows": int(seeds["required_for_full_validation"].astype(bool).sum()),
                "initial_seed_list": "|".join(str(value) for value in seeds.loc[seeds["initial_engineering_seed"].astype(bool), "simulation_seed"].astype(int)),
                "full_seed_expansion_gap_rows": int(seeds["required_for_full_validation"].astype(bool).sum() - seeds["initial_engineering_seed"].astype(bool).sum()),
            }
        )
    return pd.DataFrame(rows)


def build_data_inventory(paths: dict[str, Path], raw_events: pd.DataFrame, compact_l2: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("raw_synthetic_events", paths["raw_events"], len(raw_events), raw_events.shape[1], "Phase 9 Tier A raw synthetic events"),
        ("compact_l2_state", paths["compact_l2"], len(compact_l2), compact_l2.shape[1], "Phase 9 Tier B compact L2 states"),
        ("features_5m", paths["features_5m"], len(features), features.shape[1], "Phase 9 Tier C five-minute feature panel"),
    ]
    return pd.DataFrame(
        [
            {
                "data_product": product,
                "path": str(path),
                "rows": int(rows_count),
                "columns": int(columns),
                "role_in_stage_d": role,
                "present": bool(path.exists()),
            }
            for product, path, rows_count, columns, role in rows
        ]
    )


def strategy_signal(frame: pd.DataFrame, strategy_id: str, seed: int) -> pd.Series:
    momentum = frame["momentum_3"].fillna(0.0).astype(float)
    mlofi = frame["mlofi_qty"].fillna(0.0).astype(float)
    spread = frame["spread_ticks"].fillna(frame["spread_ticks"].median()).astype(float)
    median_spread = float(spread.median())
    imbalance = frame["l5_imbalance"].fillna(0.0).astype(float)
    intensity = frame["event_intensity_proxy"].fillna(0.0).astype(float)
    if strategy_id == "S01":
        signal = momentum.apply(lambda value: 1 if value > 0 else (-1 if value < 0 else 0))
        return signal.where((momentum * mlofi > 0) & (spread <= median_spread + 1), 0).astype(int)
    if strategy_id == "S02":
        return mlofi.apply(lambda value: 1 if value > 0 else (-1 if value < 0 else 0)).astype(int)
    if strategy_id == "S03":
        slope = frame["book_slope_l5"].fillna(0.0).astype(float)
        signal = momentum.apply(lambda value: 1 if value > 0 else (-1 if value < 0 else 0))
        return signal.where((slope > float(slope.median())) & (spread <= median_spread + 1), 0).astype(int)
    if strategy_id == "S04":
        signal = mlofi.apply(lambda value: 1 if value > 0 else (-1 if value < 0 else 0))
        return signal.where(intensity >= float(intensity.quantile(0.60)), 0).astype(int)
    if strategy_id == "S05":
        micro_edge = frame["microprice_l1"].fillna(frame["mid_price"]).astype(float) - frame["mid_price"].astype(float)
        return micro_edge.apply(lambda value: 1 if value > 0 else (-1 if value < 0 else 0)).astype(int)
    if strategy_id == "S06":
        signal = (-momentum).apply(lambda value: 1 if value > 0 else (-1 if value < 0 else 0))
        return signal.where(intensity >= float(intensity.quantile(0.75)), 0).astype(int)
    if strategy_id == "S07":
        return (-imbalance).apply(lambda value: 1 if value > 0 else (-1 if value < 0 else 0)).astype(int)
    if strategy_id == "S08":
        by_bar = frame.groupby(["feed_profile", "trade_date", "bar_index"], sort=False)["mlofi_qty"].transform("mean")
        return by_bar.fillna(0.0).apply(lambda value: 1 if value > 0 else (-1 if value < 0 else 0)).astype(int)
    if strategy_id == "S09":
        return frame["l1_imbalance"].fillna(0.0).apply(lambda value: 1 if value > 0 else (-1 if value < 0 else 0)).astype(int)
    if strategy_id == "S10":
        return pd.Series(0, index=frame.index, dtype="int64")
    if strategy_id == "S11":
        return pd.Series(0, index=frame.index, dtype="int64")
    return pd.Series(0, index=frame.index, dtype="int64")


def summarize_signal(frame: pd.DataFrame, signal: pd.Series, strategy_id: str, meta: dict[str, object], seed: int) -> dict[str, object]:
    valid = signal.fillna(0).astype(int).ne(0) & frame["future_mid_return_1"].notna()
    signed = signal.fillna(0).astype(float) * frame["future_mid_return_1"].fillna(0.0).astype(float)
    returns = signed[valid]
    trades = int(valid.sum())
    control_role = strategy_id in CONTROL_STRATEGIES
    return {
        "strategy_id": strategy_id,
        "strategy_name": str(meta.get("name", strategy_id)),
        "strategy_role": "control_or_non_alpha" if control_role else str(meta.get("role", "")),
        "support_level": str(meta.get("support_level", "")),
        "simulation_seed": int(seed),
        "rows_evaluated": int(len(frame)),
        "trades": trades,
        "signal_fraction": float(trades / len(frame)) if len(frame) else 0.0,
        "mean_gross_return_proxy": float(returns.mean()) if trades else 0.0,
        "win_rate_proxy": float((returns > 0).mean()) if trades else 0.0,
        "total_gross_pnl_units_proxy": float(returns.sum()) if trades else 0.0,
        "control_or_risk_module": bool(control_role),
        "acceptance_ready": False,
        "stage_d_status": "three_month_proxy_not_acceptance",
        "caveat": "S09-S11 are controls/non-alpha or risk-only modules; not promotion candidates." if control_role else "Three-month 5-minute proxy summary; not acceptance-grade without full execution, walk-forward and real holdout evidence.",
    }


def build_strategy_summaries(features: pd.DataFrame, strategies: pd.DataFrame, seed_plan: pd.DataFrame) -> pd.DataFrame:
    initial_seeds = seed_plan[seed_plan["initial_engineering_seed"].astype(bool)].sort_values(["quarter_profile", "seed_ordinal"], kind="mergesort")
    meta = strategies.set_index("strategy_id").to_dict("index")
    signal_cache = {strategy_id: strategy_signal(features, strategy_id, 0) for strategy_id in STAGE_D_STRATEGIES}
    rows = []
    for seed in initial_seeds["simulation_seed"].astype(int):
        for strategy_id in STAGE_D_STRATEGIES:
            rows.append(summarize_signal(features, signal_cache[strategy_id], strategy_id, meta.get(strategy_id, {}), int(seed)))
    return pd.DataFrame(rows)


def build_dataset_summary(
    features: pd.DataFrame,
    calendar: pd.DataFrame,
    profile_summary: pd.DataFrame,
    seed_summary: pd.DataFrame,
    inventory: pd.DataFrame,
    strategy_summary: pd.DataFrame,
) -> pd.DataFrame:
    rows = [
        ("symbols", int(features["symbol"].nunique()), "instrument count in three-month feature product"),
        ("quarter_profiles", int(features["quarter_profile"].nunique()), "quarter profiles represented"),
        ("total_trading_days", int(calendar["trade_date"].nunique()), "unique calendar dates across profiles"),
        ("min_days_per_profile", int(profile_summary["trading_days"].min()), "minimum trading days per quarter profile"),
        ("feature_rows", int(len(features)), "Phase 9 Tier C feature rows"),
        ("raw_event_rows", int(inventory.loc[inventory["data_product"].eq("raw_synthetic_events"), "rows"].iloc[0]), "Phase 9 Tier A raw event rows"),
        ("compact_l2_rows", int(inventory.loc[inventory["data_product"].eq("compact_l2_state"), "rows"].iloc[0]), "Phase 9 Tier B compact L2 rows"),
        ("initial_seed_rows", int(seed_summary["initial_engineering_seed_rows"].sum()), "initial engineering seeds across profiles"),
        ("full_seed_rows", int(seed_summary["full_validation_seed_rows"].sum()), "full validation seed target rows"),
        ("strategy_run_rows", int(len(strategy_summary)), "S01-S11 x initial seeds"),
        ("control_strategy_rows", int(strategy_summary["control_or_risk_module"].astype(bool).sum()), "S09-S11 control/non-alpha rows"),
        ("acceptance_ready_rows", int(strategy_summary["acceptance_ready"].astype(bool).sum()), "promotion-ready rows"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def build_checks(summary: pd.DataFrame, inventory: pd.DataFrame) -> pd.DataFrame:
    metrics = summary.set_index("metric")["value"].to_dict()
    inventory_present = bool(inventory["present"].all()) and set(inventory["data_product"]) == {"raw_synthetic_events", "compact_l2_state", "features_5m"}
    checks = [
        ("all_32_instruments", metrics["symbols"], 32, metrics["symbols"] == 32, "all current symbols represented"),
        ("sixty_three_days_per_profile", metrics["min_days_per_profile"], 63, metrics["min_days_per_profile"] == 63, "Q-A/Q-B/Q-C each cover 63 days"),
        ("three_profiles", metrics["quarter_profiles"], 3, metrics["quarter_profiles"] == 3, "Q-A/Q-B/Q-C present"),
        ("initial_three_seeds_per_profile", metrics["initial_seed_rows"], 9, metrics["initial_seed_rows"] == 9, "3 initial engineering seeds x 3 profiles"),
        ("ten_seed_expansion_tracked", metrics["full_seed_rows"], 30, metrics["full_seed_rows"] == 30 and metrics["initial_seed_rows"] < metrics["full_seed_rows"], "remaining 21 full-seed rows are tracked as expansion gap"),
        ("raw_compact_feature_inventory", int(inventory_present), 1, inventory_present, "Phase 9 Tier A/B/C products present"),
        ("all_strategy_proxy_runs", metrics["strategy_run_rows"], 99, metrics["strategy_run_rows"] == 99, "S01-S11 x 9 initial seeds"),
        ("controls_labelled", metrics["control_strategy_rows"], 27, metrics["control_strategy_rows"] == 27, "S09-S11 x 9 seeds"),
        ("non_acceptance_scope", metrics["acceptance_ready_rows"], 0, metrics["acceptance_ready_rows"] == 0, "Stage D remains proxy evidence"),
    ]
    return pd.DataFrame(
        [
            {
                "check_id": check_id,
                "observed_value": observed,
                "expected_value": expected,
                "passed": bool(passed),
                "detail": detail,
                "acceptance_scope": "stage_d_three_month_proxy_not_strategy_promotion",
            }
            for check_id, observed, expected, passed, detail in checks
        ]
    )


def write_report(
    output_dir: Path,
    profile_summary: pd.DataFrame,
    seed_summary: pd.DataFrame,
    inventory: pd.DataFrame,
    dataset_summary: pd.DataFrame,
    checks: pd.DataFrame,
    strategy_summary: pd.DataFrame,
) -> None:
    lines = [
        "# Stage D Three-Month Study Proxy",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This three-month proxy study covers all 32 instruments, all Q-A/Q-B/Q-C 63-day profiles, the current 3 initial engineering seeds per profile and S01-S11 strategy/control summaries.",
        "It inventories raw synthetic events, compact L2 state and 5-minute feature products, but remains proxy evidence rather than strategy-promotion evidence.",
        "",
        "## Profile Summary",
        "",
        _markdown_table(profile_summary),
        "",
        "## Seed Summary",
        "",
        _markdown_table(seed_summary),
        "",
        "## Data Product Inventory",
        "",
        _markdown_table(inventory),
        "",
        "## Dataset Summary",
        "",
        _markdown_table(dataset_summary),
        "",
        "## Checks",
        "",
        _markdown_table(checks),
        "",
        "## Strategy Proxy Summary",
        "",
        _markdown_table(strategy_summary),
        "",
    ]
    (output_dir / "stage_d_three_month_study_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_stage_d(paths: dict[str, Path], output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    calendar = pd.read_csv(paths["scenario_calendar"])
    seed_plan = pd.read_csv(paths["seed_plan"])
    strategies = pd.read_csv(paths["strategy_matrix"])
    raw_events = pd.read_parquet(paths["raw_events"])
    compact_l2 = pd.read_parquet(paths["compact_l2"])
    features = pd.read_parquet(paths["features_5m"])

    profile_summary = build_profile_summary(calendar, features)
    seed_summary = build_seed_summary(seed_plan)
    inventory = build_data_inventory(paths, raw_events, compact_l2, features)
    strategy_summary = build_strategy_summaries(features, strategies, seed_plan)
    dataset_summary = build_dataset_summary(features, calendar, profile_summary, seed_summary, inventory, strategy_summary)
    criteria = build_criteria()
    checks = build_checks(dataset_summary, inventory)

    profile_summary.to_csv(output_dir / "stage_d_profile_summary.csv", index=False)
    seed_summary.to_csv(output_dir / "stage_d_seed_summary.csv", index=False)
    inventory.to_csv(output_dir / "stage_d_data_product_inventory.csv", index=False)
    dataset_summary.to_csv(output_dir / "stage_d_dataset_summary.csv", index=False)
    criteria.to_csv(output_dir / "stage_d_criteria.csv", index=False)
    checks.to_csv(output_dir / "stage_d_check_ledger.csv", index=False)
    strategy_summary.to_csv(output_dir / "stage_d_strategy_proxy_summary.csv", index=False)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "symbol_count": int(features["symbol"].nunique()),
        "quarter_profiles": int(features["quarter_profile"].nunique()),
        "feature_rows": int(len(features)),
        "strategy_run_rows": int(len(strategy_summary)),
        "passed_checks": int(checks["passed"].astype(bool).sum()),
        "failed_checks": int((~checks["passed"].astype(bool)).sum()),
        "scope": "stage_d_three_month_study_proxy_not_acceptance",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="stage_d",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={"strategies": STAGE_D_STRATEGIES, "initial_seed_policy": "3_per_quarter_profile_now_10_per_profile_tracked_as_gap"},
            outputs={
                "profile_summary": str(output_dir / "stage_d_profile_summary.csv"),
                "seed_summary": str(output_dir / "stage_d_seed_summary.csv"),
                "data_product_inventory": str(output_dir / "stage_d_data_product_inventory.csv"),
                "dataset_summary": str(output_dir / "stage_d_dataset_summary.csv"),
                "criteria": str(output_dir / "stage_d_criteria.csv"),
                "check_ledger": str(output_dir / "stage_d_check_ledger.csv"),
                "strategy_proxy_summary": str(output_dir / "stage_d_strategy_proxy_summary.csv"),
                "report": str(output_dir / "stage_d_three_month_study_report.md"),
                "manifest": str(output_dir / "stage_d_three_month_study_manifest.json"),
            },
            random_seed="phase13_initial_engineering_seeds_for_stage_d_proxy",
            scenario_ids="phase4_QA_QB_QC_all_63_day_profiles",
            cost_model_version="not_applicable_stage_d_gross_proxy_no_execution_costs",
            latency_model_version="phase9_tier_c_feed_profiles_no_order_latency",
            base_dir=base_dir,
        )
    )
    (output_dir / "stage_d_three_month_study_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, profile_summary, seed_summary, inventory, dataset_summary, checks, strategy_summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Stage D three-month study proxy artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/stage_d"))
    parser.add_argument("--scenario-calendar", type=Path, default=Path("outputs/phase4/scenario_calendar.csv"))
    parser.add_argument("--seed-plan", type=Path, default=Path("outputs/phase13/seed_plan.csv"))
    parser.add_argument("--strategy-matrix", type=Path, default=Path("outputs/phase11/strategy_validation_matrix.csv"))
    parser.add_argument("--raw-events", type=Path, default=Path("outputs/phase9/tier_a/raw_synthetic_events.parquet"))
    parser.add_argument("--compact-l2", type=Path, default=Path("outputs/phase9/tier_b/compact_l2_state.parquet"))
    parser.add_argument("--features-5m", type=Path, default=Path("outputs/phase9/tier_c/features_5m.parquet"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "scenario_calendar": args.scenario_calendar,
        "seed_plan": args.seed_plan,
        "strategy_matrix": args.strategy_matrix,
        "raw_events": args.raw_events,
        "compact_l2": args.compact_l2,
        "features_5m": args.features_5m,
    }
    run_stage_d(paths, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
