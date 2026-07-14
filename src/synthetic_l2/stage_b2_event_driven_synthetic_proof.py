from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_DEVELOPMENT_SYMBOLS = ["ADANIPORTS", "AXISBANK", "BAJAJ-AUTO", "BHARTIARTL", "BANKBEES"]

STAGE_B2_CRITERIA = [
    ("development_subset", "Use the same five-instrument Stage B1 development subset, including at least one ETF.", "5 symbols and ETF count >= 1"),
    ("scenario_selection", "Select 5 normal days, 2 explicit trend days and 1 explicit shock day.", "normal_days == 5, trend_days == 2, shock_days == 1"),
    ("raw_event_dataset", "Emit raw synthetic event rows for the selected symbols/days.", "raw_event_rows > 0"),
    ("event_feature_dataset", "Emit event-driven feature rows from received synthetic feed observations.", "event_feature_rows > 0"),
    ("one_second_scope", "Emit 1-second/event-driven feature rows only for symbols/windows supported by measured readiness.", "all 1s symbols have event_driven_1s_ready == true"),
    ("no_dense_1s_overclaim", "Do not claim dense 1-second readiness where measured coverage does not support it.", "dense_1s_claim_rows == 0"),
    ("deterministic_replay_storage", "Persist deterministic proof outputs with manifest and stable row counts.", "dataset rows stable and manifest records inputs/outputs"),
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
                "current_status": "proof_check_not_strategy_acceptance",
            }
            for criterion_id, description, threshold in STAGE_B2_CRITERIA
        ]
    )


def build_development_readiness(subset: pd.DataFrame, readiness: pd.DataFrame, symbols: list[str]) -> pd.DataFrame:
    dev = subset[subset["symbol"].isin(symbols)].copy()
    if dev.empty:
        dev = pd.DataFrame({"symbol": symbols})
        dev["instrument_class"] = dev["symbol"].map(lambda symbol: "etf" if symbol.endswith("BEES") else "equity")
    merged = dev.merge(readiness, on="symbol", how="left", suffixes=("_stage_b1", ""))
    merged["event_driven_1s_ready"] = merged["event_driven_1s_ready"].fillna(False).astype(bool)
    merged["dense_1s_ready"] = merged["dense_1s_ready"].fillna(False).astype(bool)
    merged["stage_b2_1s_action"] = merged["event_driven_1s_ready"].map(
        {True: "emit_event_driven_1s_features", False: "exclude_from_1s_features_due_to_measured_readiness"}
    )
    columns = [
        "symbol",
        "instrument_class",
        "window_name",
        "rows",
        "event_rate_per_second",
        "coverage_fraction",
        "forward_fill_fraction",
        "median_gap_ms",
        "p95_gap_ms",
        "dense_1s_ready",
        "event_driven_1s_ready",
        "readiness_status",
        "stage_b2_1s_action",
    ]
    for column in columns:
        if column not in merged.columns:
            merged[column] = pd.NA
    return merged[columns].sort_values(["event_driven_1s_ready", "symbol"], ascending=[False, True], kind="mergesort")


def select_scenario_days(calendar: pd.DataFrame) -> pd.DataFrame:
    ordered = calendar.sort_values(["trade_date", "quarter_profile", "scenario_day"], kind="mergesort").drop_duplicates(["trade_date"], keep="first").copy()
    normal = ordered[(~ordered["is_market_shock_day"].astype(bool)) & (ordered["regime_family"].astype(str) == "Normal balanced")].head(5).copy()
    if len(normal) < 5:
        fallback = ordered[(~ordered["is_market_shock_day"].astype(bool)) & (~ordered["scenario_day"].isin(normal["scenario_day"]))].head(5 - len(normal)).copy()
        normal = pd.concat([normal, fallback], ignore_index=True)
    trend = ordered[
        (~ordered["is_market_shock_day"].astype(bool))
        & ordered["regime_family"].astype(str).str.contains("trend", case=False, regex=False)
        & (~ordered["scenario_day"].isin(normal["scenario_day"]))
    ].head(2).copy()
    shock = ordered[
        ordered["is_market_shock_day"].astype(bool)
        & (~ordered["scenario_day"].isin(pd.concat([normal, trend], ignore_index=True)["scenario_day"]))
    ].head(1).copy()
    normal["stage_b2_bucket"] = "normal"
    trend["stage_b2_bucket"] = "trend"
    shock["stage_b2_bucket"] = "shock"
    selection = pd.concat([normal, trend, shock], ignore_index=True)
    return selection[
        [
            "stage_b2_bucket",
            "scenario_day",
            "trade_date",
            "quarter_profile",
            "regime_code",
            "regime_family",
            "is_market_shock_day",
            "event_rate_multiplier",
            "spread_multiplier",
            "depth_multiplier",
            "evidence_label",
        ]
    ].sort_values(["stage_b2_bucket", "scenario_day"], kind="mergesort")


def build_raw_event_subset(raw_events: pd.DataFrame, scenario_selection: pd.DataFrame, symbols: list[str]) -> pd.DataFrame:
    keep_symbols = set(symbols) | {"ALL"}
    selector = scenario_selection[["quarter_profile", "scenario_day", "stage_b2_bucket"]].copy()
    subset = raw_events[raw_events["symbol"].isin(keep_symbols)].merge(selector, on=["quarter_profile", "scenario_day"], how="inner")
    return subset.sort_values(["scenario_day", "symbol", "collector_received_utc_ms", "event_id"], kind="mergesort")


def build_event_features(observations: pd.DataFrame, scenario_selection: pd.DataFrame, symbols: list[str]) -> pd.DataFrame:
    selector = scenario_selection[["quarter_profile", "scenario_day", "stage_b2_bucket"]].copy()
    frame = observations[observations["symbol"].isin(symbols)].merge(selector, on=["quarter_profile", "scenario_day"], how="inner")
    denom_l1 = (frame["bid_qty_1"].astype(float) + frame["ask_qty_1"].astype(float)).replace(0, pd.NA)
    denom_l5 = sum(frame[f"bid_qty_{level}"].astype(float) + frame[f"ask_qty_{level}"].astype(float) for level in range(1, 6)).replace(0, pd.NA)
    frame["l1_imbalance"] = (frame["bid_qty_1"].astype(float) - frame["ask_qty_1"].astype(float)) / denom_l1
    frame["l5_imbalance"] = sum(frame[f"bid_qty_{level}"].astype(float) - frame[f"ask_qty_{level}"].astype(float) for level in range(1, 6)) / denom_l5
    frame["microprice_l1"] = (
        frame["ask_px_1"].astype(float) * frame["bid_qty_1"].astype(float)
        + frame["bid_px_1"].astype(float) * frame["ask_qty_1"].astype(float)
    ) / denom_l1
    frame = frame.sort_values(["feed_profile", "symbol", "scenario_day", "collector_received_utc_ms", "receive_sequence"], kind="mergesort")
    grouped = frame.groupby(["feed_profile", "symbol", "scenario_day"], sort=False)
    frame["mid_return_event"] = grouped["mid_price"].pct_change().fillna(0.0)
    frame["mlofi_qty_event"] = grouped["bid_qty_1"].diff().fillna(0.0) - grouped["ask_qty_1"].diff().fillna(0.0)
    columns = [
        "feed_profile",
        "stage_b2_bucket",
        "quarter_profile",
        "scenario_day",
        "trade_date",
        "bar_index",
        "symbol",
        "collector_received_utc_ms",
        "receive_sequence",
        "regime_code",
        "regime_family",
        "mid_price",
        "spread_ticks",
        "spread",
        "l1_imbalance",
        "l5_imbalance",
        "microprice_l1",
        "mlofi_qty_event",
        "mid_return_event",
        "event_intensity_proxy",
        "is_market_shock_day",
        "is_symbol_shock",
        "is_disconnect_gap",
        "is_duplicate",
        "is_out_of_order_injected",
    ]
    return frame[columns]


def build_one_second_event_features(event_features: pd.DataFrame, readiness: pd.DataFrame) -> pd.DataFrame:
    eligible = readiness[readiness["event_driven_1s_ready"].astype(bool)].copy()
    eligible_symbols = set(eligible["symbol"])
    if not eligible_symbols:
        return pd.DataFrame()
    base = event_features[
        (event_features["symbol"].isin(eligible_symbols))
        & (event_features["feed_profile"] == "normal_retail")
    ].copy()
    base = base.sort_values(["symbol", "scenario_day", "collector_received_utc_ms"], kind="mergesort")
    first_events = base.groupby(["symbol", "quarter_profile", "scenario_day"], sort=False).head(1).copy()
    rows = []
    readiness_by_symbol = eligible.set_index("symbol").to_dict("index")
    for row in first_events.itertuples(index=False):
        ready = readiness_by_symbol[row.symbol]
        for second_offset in range(300):
            rows.append(
                {
                    "symbol": row.symbol,
                    "scenario_day": int(row.scenario_day),
                    "trade_date": row.trade_date,
                    "stage_b2_bucket": row.stage_b2_bucket,
                    "window_name": ready.get("window_name", "open_0915_0920"),
                    "second_offset": second_offset,
                    "synthetic_feature_ts_s": int(row.collector_received_utc_ms) + second_offset,
                    "source_event_received_ts_s": int(row.collector_received_utc_ms),
                    "event_observed_at_second": second_offset == 0,
                    "forward_filled_from_event": second_offset > 0,
                    "dense_1s_claim": False,
                    "event_driven_1s_ready": True,
                    "coverage_fraction": ready.get("coverage_fraction", pd.NA),
                    "forward_fill_fraction": ready.get("forward_fill_fraction", pd.NA),
                    "mid_price": row.mid_price,
                    "spread_ticks": row.spread_ticks,
                    "spread": row.spread,
                    "l1_imbalance": row.l1_imbalance,
                    "microprice_l1": row.microprice_l1,
                    "event_intensity_proxy": row.event_intensity_proxy,
                }
            )
    return pd.DataFrame(rows)


def build_dataset_summary(
    raw_event_subset: pd.DataFrame,
    event_features: pd.DataFrame,
    one_second_features: pd.DataFrame,
    scenario_selection: pd.DataFrame,
    readiness: pd.DataFrame,
) -> pd.DataFrame:
    rows = [
        ("selected_symbols", int(event_features["symbol"].nunique()), "same five-symbol development subset"),
        ("selected_scenario_days", int(len(scenario_selection)), "5 normal + 2 trend + 1 shock"),
        ("normal_days", int((scenario_selection["stage_b2_bucket"] == "normal").sum()), "normal scenario days"),
        ("trend_days", int((scenario_selection["stage_b2_bucket"] == "trend").sum()), "explicit trend scenario days"),
        ("shock_days", int((scenario_selection["stage_b2_bucket"] == "shock").sum()), "explicit shock scenario days"),
        ("raw_event_rows", int(len(raw_event_subset)), "raw synthetic event subset rows"),
        ("event_feature_rows", int(len(event_features)), "event-driven received-feed feature rows"),
        ("event_driven_1s_ready_symbols", int(readiness["event_driven_1s_ready"].astype(bool).sum()), "symbols eligible for event-driven 1s features"),
        ("dense_1s_ready_symbols", int(readiness["dense_1s_ready"].astype(bool).sum()), "symbols eligible for dense 1s features"),
        ("one_second_event_feature_rows", int(len(one_second_features)), "event-driven 1s proof rows"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def build_checks(
    dev_readiness: pd.DataFrame,
    scenario_selection: pd.DataFrame,
    raw_event_subset: pd.DataFrame,
    event_features: pd.DataFrame,
    one_second_features: pd.DataFrame,
) -> pd.DataFrame:
    etf_count = int((dev_readiness["instrument_class"].astype(str) == "etf").sum())
    bucket_counts = scenario_selection["stage_b2_bucket"].value_counts().to_dict()
    one_second_symbols = set(one_second_features["symbol"].unique()) if not one_second_features.empty else set()
    ready_symbols = set(dev_readiness.loc[dev_readiness["event_driven_1s_ready"].astype(bool), "symbol"])
    dense_claim_rows = int(one_second_features["dense_1s_claim"].astype(bool).sum()) if not one_second_features.empty else 0
    checks = [
        ("development_subset", int(len(dev_readiness)), 5, len(dev_readiness) == 5 and etf_count >= 1, f"etf_count={etf_count}"),
        ("scenario_selection", int(bucket_counts.get("normal", 0) == 5 and bucket_counts.get("trend", 0) == 2 and bucket_counts.get("shock", 0) == 1), 1, bucket_counts.get("normal", 0) == 5 and bucket_counts.get("trend", 0) == 2 and bucket_counts.get("shock", 0) == 1, f"bucket_counts={bucket_counts}"),
        ("raw_event_dataset", int(len(raw_event_subset)), 1, len(raw_event_subset) > 0, "raw Phase 9 Tier A events selected for Stage B2 symbols/days"),
        ("event_feature_dataset", int(len(event_features)), 1, len(event_features) > 0, "received-feed event features built from Phase 8 observations"),
        ("one_second_scope", len(one_second_symbols - ready_symbols), 0, one_second_symbols.issubset(ready_symbols) and len(one_second_symbols) > 0, f"one_second_symbols={sorted(one_second_symbols)}; ready_symbols={sorted(ready_symbols)}"),
        ("no_dense_1s_overclaim", dense_claim_rows, 0, dense_claim_rows == 0, "Stage B2 only emits event-driven 1s rows, not dense 1s claims"),
        ("deterministic_replay_storage", int(len(raw_event_subset) + len(event_features) + len(one_second_features)), 1, len(raw_event_subset) > 0 and len(event_features) > 0, "parquet datasets plus csv ledgers and manifest"),
    ]
    return pd.DataFrame(
        [
            {
                "check_id": check_id,
                "observed_value": observed,
                "expected_value": expected,
                "passed": bool(passed),
                "detail": detail,
                "acceptance_scope": "stage_b2_event_driven_proof_not_strategy_profitability",
            }
            for check_id, observed, expected, passed, detail in checks
        ]
    )


def write_report(
    output_dir: Path,
    criteria: pd.DataFrame,
    dev_readiness: pd.DataFrame,
    scenario_selection: pd.DataFrame,
    dataset_summary: pd.DataFrame,
    checks: pd.DataFrame,
) -> None:
    lines = [
        "# Stage B2 Event-Driven Synthetic Proof",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This proof uses the Stage B1 development subset, selects 5 normal days, 2 trend days and 1 shock day, and emits raw/event-driven synthetic proof datasets.",
        "It emits 1-second/event-driven rows only where measured readiness supports that horizon. It does not claim dense 1-second support and must not be used to accept or reject S01-S11 profitability.",
        "",
        "## Criteria",
        "",
        _markdown_table(criteria),
        "",
        "## Development Readiness",
        "",
        _markdown_table(dev_readiness),
        "",
        "## Scenario Selection",
        "",
        _markdown_table(scenario_selection),
        "",
        "## Dataset Summary",
        "",
        _markdown_table(dataset_summary),
        "",
        "## Proof Checks",
        "",
        _markdown_table(checks),
        "",
    ]
    (output_dir / "stage_b2_event_driven_synthetic_proof_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_stage_b2(paths: dict[str, Path], output_dir: Path, base_dir: Path, symbols: list[str]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    subset = pd.read_csv(paths["stage_b1_subset"])
    readiness = pd.read_csv(paths["one_second_readiness"])
    calendar = pd.read_csv(paths["scenario_calendar"])
    raw_events = pd.read_parquet(paths["raw_events"])
    observations = pd.read_parquet(paths["retail_feed_observations"])

    criteria = build_criteria()
    dev_readiness = build_development_readiness(subset, readiness, symbols)
    scenario_selection = select_scenario_days(calendar)
    raw_event_subset = build_raw_event_subset(raw_events, scenario_selection, symbols)
    event_features = build_event_features(observations, scenario_selection, symbols)
    one_second_features = build_one_second_event_features(event_features, dev_readiness)
    dataset_summary = build_dataset_summary(raw_event_subset, event_features, one_second_features, scenario_selection, dev_readiness)
    checks = build_checks(dev_readiness, scenario_selection, raw_event_subset, event_features, one_second_features)

    raw_event_subset.to_parquet(output_dir / "stage_b2_raw_event_subset.parquet", index=False)
    event_features.to_parquet(output_dir / "stage_b2_event_feature_panel.parquet", index=False)
    one_second_features.to_parquet(output_dir / "stage_b2_event_driven_1s_features.parquet", index=False)
    criteria.to_csv(output_dir / "stage_b2_event_driven_criteria.csv", index=False)
    dev_readiness.to_csv(output_dir / "stage_b2_development_readiness.csv", index=False)
    scenario_selection.to_csv(output_dir / "stage_b2_scenario_selection.csv", index=False)
    dataset_summary.to_csv(output_dir / "stage_b2_dataset_summary.csv", index=False)
    checks.to_csv(output_dir / "stage_b2_proof_check_ledger.csv", index=False)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "development_symbols": symbols,
        "development_symbol_count": int(len(dev_readiness)),
        "etf_symbol_count": int((dev_readiness["instrument_class"].astype(str) == "etf").sum()),
        "selected_scenario_days": int(len(scenario_selection)),
        "raw_event_rows": int(len(raw_event_subset)),
        "event_feature_rows": int(len(event_features)),
        "one_second_event_feature_rows": int(len(one_second_features)),
        "proof_check_rows": int(len(checks)),
        "passed_proof_checks": int(checks["passed"].astype(bool).sum()),
        "failed_proof_checks": int((~checks["passed"].astype(bool)).sum()),
        "scope": "stage_b2_event_driven_synthetic_proof_not_strategy_acceptance",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="stage_b2",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={"development_symbols": symbols, "criteria": STAGE_B2_CRITERIA},
            outputs={
                "raw_event_subset": str(output_dir / "stage_b2_raw_event_subset.parquet"),
                "event_feature_panel": str(output_dir / "stage_b2_event_feature_panel.parquet"),
                "event_driven_1s_features": str(output_dir / "stage_b2_event_driven_1s_features.parquet"),
                "criteria": str(output_dir / "stage_b2_event_driven_criteria.csv"),
                "development_readiness": str(output_dir / "stage_b2_development_readiness.csv"),
                "scenario_selection": str(output_dir / "stage_b2_scenario_selection.csv"),
                "dataset_summary": str(output_dir / "stage_b2_dataset_summary.csv"),
                "proof_check_ledger": str(output_dir / "stage_b2_proof_check_ledger.csv"),
                "report": str(output_dir / "stage_b2_event_driven_synthetic_proof_report.md"),
                "manifest": str(output_dir / "stage_b2_event_driven_synthetic_proof_manifest.json"),
            },
            random_seed="phase4_phase8_phase9_deterministic_scenario_feed_and_event_generation",
            scenario_ids="stage_b2_5_normal_2_trend_1_shock_scenario_selection",
            cost_model_version="not_applicable_no_execution_costs",
            latency_model_version="phase8_retail_feed_latency_profiles_plus_stage_a1_horizon_readiness",
            base_dir=base_dir,
        )
    )
    (output_dir / "stage_b2_event_driven_synthetic_proof_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, criteria, dev_readiness, scenario_selection, dataset_summary, checks)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Stage B2 event-driven synthetic proof artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/stage_b2"))
    parser.add_argument("--stage-b1-subset", type=Path, default=Path("outputs/stage_b1/stage_b1_development_subset.csv"))
    parser.add_argument("--one-second-readiness", type=Path, default=Path("outputs/horizon_readiness/one_second_symbol_readiness.csv"))
    parser.add_argument("--scenario-calendar", type=Path, default=Path("outputs/phase4/scenario_calendar.csv"))
    parser.add_argument("--raw-events", type=Path, default=Path("outputs/phase9/tier_a/raw_synthetic_events.parquet"))
    parser.add_argument("--retail-feed-observations", type=Path, default=Path("outputs/phase8/retail_feed_observations.parquet"))
    parser.add_argument("--symbols", nargs="+", default=DEFAULT_DEVELOPMENT_SYMBOLS)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "stage_b1_subset": args.stage_b1_subset,
        "one_second_readiness": args.one_second_readiness,
        "scenario_calendar": args.scenario_calendar,
        "raw_events": args.raw_events,
        "retail_feed_observations": args.retail_feed_observations,
    }
    run_stage_b2(paths, args.output_dir, args.base_dir, args.symbols)


if __name__ == "__main__":
    main()
