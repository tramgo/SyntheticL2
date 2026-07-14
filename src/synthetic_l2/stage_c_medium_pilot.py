from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


STAGE_C_STRATEGIES = ["S01", "S02", "S03", "S04", "S05"]
STAGE_C_CRITERIA = [
    ("all_32_instruments", "Pilot covers all 32 current instruments.", "symbol_count == 32"),
    ("twenty_trading_days", "Pilot covers 20 selected trading days.", "selected_trading_days == 20"),
    ("three_initial_seeds", "Pilot uses 3 initial engineering seeds.", "seed_count == 3"),
    ("multiple_regimes", "Pilot contains multiple regime families including trend and shock exposure.", "regime_family_count >= 3 and shock_days >= 1"),
    ("strategy_proxy_runs", "Pilot runs S01-S05 proxy strategy summaries.", "strategy_run_rows == 15"),
    ("baseline_proxy_runs", "Pilot runs all registered baseline proxy summaries.", "baseline_run_rows == 21"),
    ("non_acceptance_scope", "Pilot is labelled as proxy medium-pilot evidence, not promotion evidence.", "acceptance_ready_rows == 0"),
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


def _hash_direction(seed: int, *parts: object) -> int:
    text = "|".join([str(seed), *(str(part) for part in parts)])
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return 1 if int(digest[:8], 16) % 2 == 0 else -1


def _signed_summary(frame: pd.DataFrame, signal: pd.Series, *, model_id: str, model_name: str, model_type: str, seed: int, caveat: str) -> dict[str, object]:
    valid = signal.fillna(0).astype(int).ne(0) & frame["future_mid_return_1"].notna()
    signed_return = signal.fillna(0).astype(float) * frame["future_mid_return_1"].fillna(0.0).astype(float)
    trade_returns = signed_return[valid]
    trades = int(valid.sum())
    mean_gross_return = float(trade_returns.mean()) if trades else 0.0
    win_rate = float((trade_returns > 0).mean()) if trades else 0.0
    return {
        "model_id": model_id,
        "model_name": model_name,
        "model_type": model_type,
        "simulation_seed": int(seed),
        "rows_evaluated": int(len(frame)),
        "trades": trades,
        "signal_fraction": float(trades / len(frame)) if len(frame) else 0.0,
        "mean_gross_return_proxy": mean_gross_return,
        "win_rate_proxy": win_rate,
        "total_gross_pnl_units_proxy": float(trade_returns.sum()) if trades else 0.0,
        "acceptance_ready": False,
        "pilot_status": "medium_pilot_proxy_not_acceptance",
        "caveat": caveat,
    }


def select_trading_days(calendar: pd.DataFrame, quarter_profile: str, days: int) -> pd.DataFrame:
    selected = calendar[calendar["quarter_profile"].astype(str) == quarter_profile].sort_values("scenario_day", kind="mergesort").head(days).copy()
    return selected[
        [
            "quarter_profile",
            "scenario_day",
            "trade_date",
            "regime_code",
            "regime_family",
            "is_market_shock_day",
            "vol_multiplier",
            "event_rate_multiplier",
            "spread_multiplier",
            "depth_multiplier",
        ]
    ]


def select_seeds(seed_plan: pd.DataFrame, quarter_profile: str, count: int) -> pd.DataFrame:
    seeds = seed_plan[
        (seed_plan["quarter_profile"].astype(str) == quarter_profile)
        & seed_plan["initial_engineering_seed"].astype(bool)
    ].sort_values("seed_ordinal", kind="mergesort").head(count).copy()
    return seeds


def strategy_signal(frame: pd.DataFrame, strategy_id: str) -> pd.Series:
    zero = pd.Series(0, index=frame.index, dtype="int64")
    momentum = frame["momentum_3"].fillna(0.0).astype(float)
    mlofi = frame["mlofi_qty"].fillna(0.0).astype(float)
    spread = frame["spread_ticks"].fillna(frame["spread_ticks"].median()).astype(float)
    median_spread = float(spread.median())
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
        intensity = frame["event_intensity_proxy"].fillna(0.0).astype(float)
        signal = mlofi.apply(lambda value: 1 if value > 0 else (-1 if value < 0 else 0))
        return signal.where(intensity >= float(intensity.quantile(0.60)), 0).astype(int)
    if strategy_id == "S05":
        micro_edge = frame["microprice_l1"].fillna(frame["mid_price"]).astype(float) - frame["mid_price"].astype(float)
        return micro_edge.apply(lambda value: 1 if value > 0 else (-1 if value < 0 else 0)).astype(int)
    return zero


def baseline_signal(frame: pd.DataFrame, baseline_id: str, seed: int) -> pd.Series:
    if baseline_id == "B01":
        return pd.Series(
            [_hash_direction(seed, row.symbol, row.scenario_day, row.bar_index, row.feed_profile) for row in frame.itertuples(index=False)],
            index=frame.index,
            dtype="int64",
        )
    if baseline_id == "B02":
        return pd.Series(1, index=frame.index, dtype="int64")
    if baseline_id == "B03":
        return frame["momentum_3"].fillna(0.0).apply(lambda value: 1 if value > 0 else (-1 if value < 0 else 0)).astype(int)
    if baseline_id == "B04":
        first_mid = frame.groupby(["feed_profile", "symbol", "scenario_day"], sort=False)["mid_price"].transform("first")
        diff = frame["mid_price"].astype(float) - first_mid.astype(float)
        return diff.apply(lambda value: 1 if value > 0 else (-1 if value < 0 else 0)).astype(int)
    if baseline_id == "B05":
        rolling_mid = frame.groupby(["feed_profile", "symbol", "scenario_day"], sort=False)["mid_price"].transform(lambda s: s.rolling(6, min_periods=1).mean())
        diff = frame["mid_price"].astype(float) - rolling_mid.astype(float)
        return diff.apply(lambda value: 1 if value > 0 else (-1 if value < 0 else 0)).astype(int)
    if baseline_id == "B06":
        return -frame["momentum_3"].fillna(0.0).apply(lambda value: 1 if value > 0 else (-1 if value < 0 else 0)).astype(int)
    if baseline_id == "B07":
        momentum = frame["momentum_3"].fillna(0.0).astype(float)
        threshold = frame["local_volatility_6"].fillna(frame["local_volatility_6"].median()).astype(float)
        signal = momentum.apply(lambda value: 1 if value > 0 else (-1 if value < 0 else 0))
        return signal.where(momentum.abs() >= threshold, 0).astype(int)
    return pd.Series(0, index=frame.index, dtype="int64")


def build_strategy_runs(feature_panel: pd.DataFrame, strategies: pd.DataFrame, seeds: pd.DataFrame) -> pd.DataFrame:
    rows = []
    strategy_meta = strategies.set_index("strategy_id").to_dict("index")
    for seed in seeds["simulation_seed"].astype(int):
        for strategy_id in STAGE_C_STRATEGIES:
            meta = strategy_meta[strategy_id]
            rows.append(
                _signed_summary(
                    feature_panel,
                    strategy_signal(feature_panel, strategy_id),
                    model_id=strategy_id,
                    model_name=str(meta["name"]),
                    model_type="strategy",
                    seed=int(seed),
                    caveat=f"{meta['support_level']} medium-pilot proxy over 5-minute features; not acceptance-grade.",
                )
            )
    return pd.DataFrame(rows)


def build_baseline_runs(feature_panel: pd.DataFrame, baselines: pd.DataFrame, seeds: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for seed in seeds["simulation_seed"].astype(int):
        for row in baselines.itertuples(index=False):
            caveat = "Medium-pilot baseline proxy; B05 uses rolling-mid proxy because trade-volume/VWAP is not yet acceptance-grade." if row.baseline_id == "B05" else "Medium-pilot baseline proxy; not acceptance-grade."
            rows.append(
                _signed_summary(
                    feature_panel,
                    baseline_signal(feature_panel, row.baseline_id, int(seed)),
                    model_id=row.baseline_id,
                    model_name=row.name,
                    model_type="baseline",
                    seed=int(seed),
                    caveat=caveat,
                )
            )
    return pd.DataFrame(rows)


def build_dataset_summary(feature_panel: pd.DataFrame, days: pd.DataFrame, seeds: pd.DataFrame, strategy_runs: pd.DataFrame, baseline_runs: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("symbols", int(feature_panel["symbol"].nunique()), "instrument count in pilot feature subset"),
        ("selected_trading_days", int(days["trade_date"].nunique()), "selected Q-A pilot trading days"),
        ("selected_seed_rows", int(len(seeds)), "initial engineering seed rows"),
        ("regime_families", int(days["regime_family"].nunique()), "regime families in selected days"),
        ("shock_days", int(days["is_market_shock_day"].astype(bool).sum()), "selected market shock days"),
        ("feature_rows", int(len(feature_panel)), "Phase 9 Tier C rows in pilot feature subset"),
        ("feed_profiles", int(feature_panel["feed_profile"].nunique()), "feed profiles represented"),
        ("strategy_run_rows", int(len(strategy_runs)), "S01-S05 strategy/seed proxy run summaries"),
        ("baseline_run_rows", int(len(baseline_runs)), "baseline/seed proxy run summaries"),
        ("acceptance_ready_rows", int(strategy_runs["acceptance_ready"].astype(bool).sum() + baseline_runs["acceptance_ready"].astype(bool).sum()), "promotion-ready rows"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def build_checks(summary: pd.DataFrame) -> pd.DataFrame:
    metrics = summary.set_index("metric")["value"].to_dict()
    checks = [
        ("all_32_instruments", metrics["symbols"], 32, metrics["symbols"] == 32, "all current Stage A1 symbols represented"),
        ("twenty_trading_days", metrics["selected_trading_days"], 20, metrics["selected_trading_days"] == 20, "Q-A first 20 scenario days selected"),
        ("three_initial_seeds", metrics["selected_seed_rows"], 3, metrics["selected_seed_rows"] == 3, "Q-A initial engineering seeds selected"),
        ("multiple_regimes", metrics["regime_families"], 3, metrics["regime_families"] >= 3 and metrics["shock_days"] >= 1, f"shock_days={metrics['shock_days']}"),
        ("strategy_proxy_runs", metrics["strategy_run_rows"], 15, metrics["strategy_run_rows"] == 15, "S01-S05 x 3 seeds"),
        ("baseline_proxy_runs", metrics["baseline_run_rows"], 21, metrics["baseline_run_rows"] == 21, "B01-B07 x 3 seeds"),
        ("non_acceptance_scope", metrics["acceptance_ready_rows"], 0, metrics["acceptance_ready_rows"] == 0, "medium pilot is not strategy promotion evidence"),
    ]
    return pd.DataFrame(
        [
            {
                "check_id": check_id,
                "observed_value": observed,
                "expected_value": expected,
                "passed": bool(passed),
                "detail": detail,
                "acceptance_scope": "stage_c_medium_pilot_proxy_not_strategy_promotion",
            }
            for check_id, observed, expected, passed, detail in checks
        ]
    )


def write_report(output_dir: Path, days: pd.DataFrame, seeds: pd.DataFrame, summary: pd.DataFrame, checks: pd.DataFrame, strategy_runs: pd.DataFrame, baseline_runs: pd.DataFrame) -> None:
    lines = [
        "# Stage C Medium Pilot",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This medium pilot covers all 32 instruments, 20 selected Q-A trading days, 3 initial engineering seeds, S01-S05 proxy strategies and all 7 registered baselines.",
        "It is medium-pilot proxy evidence only. It is not acceptance-grade promotion evidence.",
        "",
        "## Selected Days",
        "",
        _markdown_table(days),
        "",
        "## Selected Seeds",
        "",
        _markdown_table(seeds),
        "",
        "## Dataset Summary",
        "",
        _markdown_table(summary),
        "",
        "## Checks",
        "",
        _markdown_table(checks),
        "",
        "## Strategy Proxy Runs",
        "",
        _markdown_table(strategy_runs),
        "",
        "## Baseline Proxy Runs",
        "",
        _markdown_table(baseline_runs),
        "",
    ]
    (output_dir / "stage_c_medium_pilot_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_stage_c(paths: dict[str, Path], output_dir: Path, base_dir: Path, quarter_profile: str, day_count: int, seed_count: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    calendar = pd.read_csv(paths["scenario_calendar"])
    quality = pd.read_csv(paths["stage_quality"])
    seed_plan = pd.read_csv(paths["seed_plan"])
    strategies = pd.read_csv(paths["strategy_matrix"])
    baselines = pd.read_csv(paths["baseline_matrix"])
    features = pd.read_parquet(paths["features_5m"])

    days = select_trading_days(calendar, quarter_profile, day_count)
    seeds = select_seeds(seed_plan, quarter_profile, seed_count)
    symbols = sorted(quality["symbol"].unique())
    feature_panel = features[
        (features["quarter_profile"].astype(str) == quarter_profile)
        & (features["scenario_day"].isin(days["scenario_day"]))
        & (features["symbol"].isin(symbols))
    ].copy()
    feature_panel = feature_panel.sort_values(["feed_profile", "symbol", "scenario_day", "bar_index"], kind="mergesort")
    strategy_runs = build_strategy_runs(feature_panel, strategies, seeds)
    baseline_runs = build_baseline_runs(feature_panel, baselines, seeds)
    summary = build_dataset_summary(feature_panel, days, seeds, strategy_runs, baseline_runs)
    checks = build_checks(summary)

    feature_panel.to_parquet(output_dir / "stage_c_medium_pilot_feature_subset.parquet", index=False)
    days.to_csv(output_dir / "stage_c_selected_trading_days.csv", index=False)
    seeds.to_csv(output_dir / "stage_c_selected_seeds.csv", index=False)
    summary.to_csv(output_dir / "stage_c_dataset_summary.csv", index=False)
    checks.to_csv(output_dir / "stage_c_check_ledger.csv", index=False)
    strategy_runs.to_csv(output_dir / "stage_c_strategy_proxy_run_summary.csv", index=False)
    baseline_runs.to_csv(output_dir / "stage_c_baseline_proxy_run_summary.csv", index=False)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "quarter_profile": quarter_profile,
        "selected_trading_days": int(days["trade_date"].nunique()),
        "symbol_count": int(feature_panel["symbol"].nunique()),
        "seed_count": int(len(seeds)),
        "strategy_run_rows": int(len(strategy_runs)),
        "baseline_run_rows": int(len(baseline_runs)),
        "passed_checks": int(checks["passed"].astype(bool).sum()),
        "failed_checks": int((~checks["passed"].astype(bool)).sum()),
        "scope": "stage_c_medium_pilot_proxy_not_acceptance",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="stage_c",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={"quarter_profile": quarter_profile, "day_count": day_count, "seed_count": seed_count, "strategies": STAGE_C_STRATEGIES},
            outputs={
                "feature_subset": str(output_dir / "stage_c_medium_pilot_feature_subset.parquet"),
                "selected_trading_days": str(output_dir / "stage_c_selected_trading_days.csv"),
                "selected_seeds": str(output_dir / "stage_c_selected_seeds.csv"),
                "dataset_summary": str(output_dir / "stage_c_dataset_summary.csv"),
                "check_ledger": str(output_dir / "stage_c_check_ledger.csv"),
                "strategy_proxy_run_summary": str(output_dir / "stage_c_strategy_proxy_run_summary.csv"),
                "baseline_proxy_run_summary": str(output_dir / "stage_c_baseline_proxy_run_summary.csv"),
                "report": str(output_dir / "stage_c_medium_pilot_report.md"),
                "manifest": str(output_dir / "stage_c_medium_pilot_manifest.json"),
            },
            random_seed="stage_c_selected_phase13_initial_engineering_seeds",
            scenario_ids=f"{quarter_profile}_first_{day_count}_scenario_days",
            cost_model_version="not_applicable_stage_c_gross_proxy_no_execution_costs",
            latency_model_version="phase9_tier_c_feed_profiles_no_order_latency",
            base_dir=base_dir,
        )
    )
    (output_dir / "stage_c_medium_pilot_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, days, seeds, summary, checks, strategy_runs, baseline_runs)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Stage C medium pilot proxy artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/stage_c"))
    parser.add_argument("--scenario-calendar", type=Path, default=Path("outputs/phase4/scenario_calendar.csv"))
    parser.add_argument("--stage-quality", type=Path, default=Path("outputs/stage_a1/data_quality_report.csv"))
    parser.add_argument("--seed-plan", type=Path, default=Path("outputs/phase13/seed_plan.csv"))
    parser.add_argument("--strategy-matrix", type=Path, default=Path("outputs/phase11/strategy_validation_matrix.csv"))
    parser.add_argument("--baseline-matrix", type=Path, default=Path("outputs/phase11/baseline_strategy_matrix.csv"))
    parser.add_argument("--features-5m", type=Path, default=Path("outputs/phase9/tier_c/features_5m.parquet"))
    parser.add_argument("--quarter-profile", default="Q-A")
    parser.add_argument("--day-count", type=int, default=20)
    parser.add_argument("--seed-count", type=int, default=3)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "scenario_calendar": args.scenario_calendar,
        "stage_quality": args.stage_quality,
        "seed_plan": args.seed_plan,
        "strategy_matrix": args.strategy_matrix,
        "baseline_matrix": args.baseline_matrix,
        "features_5m": args.features_5m,
    }
    run_stage_c(paths, args.output_dir, args.base_dir, args.quarter_profile, args.day_count, args.seed_count)


if __name__ == "__main__":
    main()
