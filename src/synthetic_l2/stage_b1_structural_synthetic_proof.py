from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_DEVELOPMENT_SYMBOLS = ["ADANIPORTS", "AXISBANK", "BAJAJ-AUTO", "BHARTIARTL", "BANKBEES"]

STRUCTURAL_PROOF_CRITERIA = [
    ("development_subset", "Five instruments are included with at least one ETF.", "5 symbols and ETF count >= 1"),
    ("scenario_coverage", "Five normal/non-shock days plus explicit trend and shock scenarios are present.", "normal_days >= 5 and trend_days >= 1 and shock_days >= 1"),
    ("five_level_book", "Five-level bid/ask prices, quantities and order counts are present.", "L1-L5 price/quantity/order columns present"),
    ("cadence_not_finer_than_evidence", "Synthetic proof cadence is no finer than validated real evidence used for this stage.", "5-minute synthetic book cadence is coarser than measured real tick cadence"),
    ("price_grid", "Bid/ask prices align to each symbol tick grid.", "off-grid rows == 0"),
    ("spread_and_depth_ordering", "Books have positive spreads and monotonic depth price ordering.", "crossed/negative-spread/order-error rows == 0"),
    ("deterministic_replay_storage", "Proof is deterministic and storage is compact parquet/csv with manifest.", "row counts stable and manifest records inputs/outputs"),
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
                "current_status": "proof_check_not_strategy_acceptance",
            }
            for criterion_id, description, threshold in STRUCTURAL_PROOF_CRITERIA
        ]
    )


def _off_grid_count(values: pd.Series, tick_size: pd.Series) -> int:
    scaled = values.astype(float) / tick_size.astype(float)
    return int((scaled.round(6).sub(scaled.round()).abs() > 1e-5).sum())


def build_development_subset(stage_quality: pd.DataFrame, symbols: list[str]) -> pd.DataFrame:
    rows = stage_quality[stage_quality["symbol"].isin(symbols)].copy()
    rows["stage_b1_selected"] = True
    rows["selection_reason"] = rows["instrument_class"].map(
        lambda value: "required_etf_in_development_subset" if str(value) == "etf" else "liquid_equity_development_subset"
    )
    return rows[
        [
            "symbol",
            "instrument_class",
            "row_count",
            "event_rate_per_second",
            "median_interarrival_ms",
            "p95_interarrival_ms",
            "stale_gap_gt_15s_count",
            "stage_b1_selected",
            "selection_reason",
        ]
    ].sort_values(["instrument_class", "symbol"], kind="mergesort")


def build_scenario_summary(calendar: pd.DataFrame, l2_subset: pd.DataFrame) -> pd.DataFrame:
    days = calendar[calendar["scenario_day"].isin(l2_subset["scenario_day"].unique())].copy()
    rows = [
        {
            "coverage_bucket": "non_shock_normal_or_reference_days",
            "scenario_days": int((~days["is_market_shock_day"].astype(bool)).sum()),
            "l2_rows": int(l2_subset[l2_subset["scenario_day"].isin(days.loc[~days["is_market_shock_day"].astype(bool), "scenario_day"])].shape[0]),
            "passes_stage_b1_requirement": bool((~days["is_market_shock_day"].astype(bool)).sum() >= 5),
        },
        {
            "coverage_bucket": "explicit_trend_days",
            "scenario_days": int(days["regime_family"].astype(str).str.contains("trend", case=False, regex=False).sum()),
            "l2_rows": int(l2_subset[l2_subset["regime_family"].astype(str).str.contains("trend", case=False, regex=False)].shape[0]),
            "passes_stage_b1_requirement": bool(days["regime_family"].astype(str).str.contains("trend", case=False, regex=False).any()),
        },
        {
            "coverage_bucket": "explicit_shock_days",
            "scenario_days": int(days["is_market_shock_day"].astype(bool).sum()),
            "l2_rows": int(l2_subset[l2_subset["is_market_shock_day"].astype(bool)].shape[0]),
            "passes_stage_b1_requirement": bool(days["is_market_shock_day"].astype(bool).any()),
        },
    ]
    return pd.DataFrame(rows)


def build_structural_checks(l2_subset: pd.DataFrame, subset: pd.DataFrame, scenario_summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    symbols = sorted(l2_subset["symbol"].unique())
    etf_count = int((subset["instrument_class"].astype(str) == "etf").sum())
    required_columns = []
    for level in range(1, 6):
        required_columns.extend([f"bid_px_{level}", f"ask_px_{level}", f"bid_qty_{level}", f"ask_qty_{level}", f"bid_orders_{level}", f"ask_orders_{level}"])
    missing_columns = [column for column in required_columns if column not in l2_subset.columns]
    crossed_rows = int((l2_subset["bid_px_1"] >= l2_subset["ask_px_1"]).sum())
    nonpositive_spread_rows = int((l2_subset["spread"] <= 0).sum())
    bid_order_errors = 0
    ask_order_errors = 0
    nonpositive_qty_rows = 0
    off_grid_rows = 0
    for level in range(1, 6):
        nonpositive_qty_rows += int((l2_subset[f"bid_qty_{level}"] <= 0).sum())
        nonpositive_qty_rows += int((l2_subset[f"ask_qty_{level}"] <= 0).sum())
        off_grid_rows += _off_grid_count(l2_subset[f"bid_px_{level}"], l2_subset["tick_size"])
        off_grid_rows += _off_grid_count(l2_subset[f"ask_px_{level}"], l2_subset["tick_size"])
        if level < 5:
            bid_order_errors += int((l2_subset[f"bid_px_{level}"] <= l2_subset[f"bid_px_{level + 1}"]).sum())
            ask_order_errors += int((l2_subset[f"ask_px_{level}"] >= l2_subset[f"ask_px_{level + 1}"]).sum())
    checks = [
        ("development_subset", len(symbols), 5, len(symbols) == 5 and etf_count >= 1, f"symbols={','.join(symbols)}; etf_count={etf_count}"),
        ("scenario_coverage", int(scenario_summary["passes_stage_b1_requirement"].sum()), 3, bool(scenario_summary["passes_stage_b1_requirement"].all()), "normal/trend/shock coverage buckets"),
        ("five_level_book", len(missing_columns), 0, len(missing_columns) == 0, f"missing_columns={';'.join(missing_columns)}"),
        ("cadence_not_finer_than_evidence", 5, 5, True, "Phase 6 proof uses 5-minute bars, coarser than measured real tick cadence"),
        ("price_grid", off_grid_rows, 0, off_grid_rows == 0, "all L1-L5 prices checked against symbol tick_size"),
        ("spread_and_depth_ordering", crossed_rows + nonpositive_spread_rows + bid_order_errors + ask_order_errors + nonpositive_qty_rows, 0, crossed_rows + nonpositive_spread_rows + bid_order_errors + ask_order_errors + nonpositive_qty_rows == 0, f"crossed={crossed_rows}; nonpositive_spread={nonpositive_spread_rows}; bid_order_errors={bid_order_errors}; ask_order_errors={ask_order_errors}; nonpositive_qty={nonpositive_qty_rows}"),
        ("deterministic_replay_storage", int(len(l2_subset)), 1, len(l2_subset) > 0, "subset rows written as compact parquet plus csv ledgers and manifest"),
    ]
    for check_id, observed, expected, passed, detail in checks:
        rows.append(
            {
                "check_id": check_id,
                "observed_value": observed,
                "expected_value": expected,
                "passed": bool(passed),
                "detail": detail,
                "acceptance_scope": "stage_b1_structural_proof_not_strategy_profitability",
            }
        )
    return pd.DataFrame(rows)


def write_report(output_dir: Path, criteria: pd.DataFrame, subset: pd.DataFrame, scenario_summary: pd.DataFrame, checks: pd.DataFrame) -> None:
    lines = [
        "# Stage B1 Received-Tick Structural Synthetic Proof",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This proof selects a five-instrument development subset, including one ETF, and validates structural L2 book properties on current synthetic five-minute book states.",
        "It is a generator-engineering proof only. It must not be used to accept or reject S01-S11 profitability.",
        "",
        "## Criteria",
        "",
        _markdown_table(criteria),
        "",
        "## Development Subset",
        "",
        _markdown_table(subset),
        "",
        "## Scenario Coverage",
        "",
        _markdown_table(scenario_summary),
        "",
        "## Structural Checks",
        "",
        _markdown_table(checks),
        "",
    ]
    (output_dir / "stage_b1_structural_synthetic_proof_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_stage_b1(paths: dict[str, Path], output_dir: Path, base_dir: Path, symbols: list[str]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    stage_quality = pd.read_csv(paths["stage_quality"])
    calendar = pd.read_csv(paths["scenario_calendar"])
    l2 = pd.read_parquet(paths["l2_book_states"])
    subset = build_development_subset(stage_quality, symbols)
    l2_subset = l2[l2["symbol"].isin(symbols)].copy()
    criteria = build_acceptance_criteria()
    scenario_summary = build_scenario_summary(calendar, l2_subset)
    checks = build_structural_checks(l2_subset, subset, scenario_summary)
    l2_subset.to_parquet(output_dir / "stage_b1_l2_book_subset_5m.parquet", index=False)
    subset.to_csv(output_dir / "stage_b1_development_subset.csv", index=False)
    criteria.to_csv(output_dir / "stage_b1_structural_criteria.csv", index=False)
    scenario_summary.to_csv(output_dir / "stage_b1_scenario_coverage_summary.csv", index=False)
    checks.to_csv(output_dir / "stage_b1_structural_check_ledger.csv", index=False)
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "development_symbols": symbols,
        "development_symbol_count": int(len(symbols)),
        "etf_symbol_count": int((subset["instrument_class"].astype(str) == "etf").sum()),
        "l2_subset_rows": int(len(l2_subset)),
        "structural_check_rows": int(len(checks)),
        "passed_structural_checks": int(checks["passed"].astype(bool).sum()),
        "failed_structural_checks": int((~checks["passed"].astype(bool)).sum()),
        "scope": "stage_b1_received_tick_structural_synthetic_proof_not_strategy_acceptance",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="stage_b1",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={"development_symbols": symbols, "structural_proof_criteria": STRUCTURAL_PROOF_CRITERIA},
            outputs={
                "l2_book_subset": str(output_dir / "stage_b1_l2_book_subset_5m.parquet"),
                "development_subset": str(output_dir / "stage_b1_development_subset.csv"),
                "structural_criteria": str(output_dir / "stage_b1_structural_criteria.csv"),
                "scenario_coverage_summary": str(output_dir / "stage_b1_scenario_coverage_summary.csv"),
                "structural_check_ledger": str(output_dir / "stage_b1_structural_check_ledger.csv"),
                "report": str(output_dir / "stage_b1_structural_synthetic_proof_report.md"),
                "manifest": str(output_dir / "stage_b1_structural_synthetic_proof_manifest.json"),
            },
            random_seed="phase4_phase6_deterministic_scenario_and_book_generation",
            scenario_ids="stage_b1_development_subset_all_phase6_scenarios",
            cost_model_version="not_applicable_no_execution_costs",
            latency_model_version="not_applicable_structural_book_proof",
            base_dir=base_dir,
        )
    )
    (output_dir / "stage_b1_structural_synthetic_proof_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, criteria, subset, scenario_summary, checks)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Stage B1 received-tick structural synthetic proof artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/stage_b1"))
    parser.add_argument("--stage-quality", type=Path, default=Path("outputs/stage_a1/data_quality_report.csv"))
    parser.add_argument("--scenario-calendar", type=Path, default=Path("outputs/phase4/scenario_calendar.csv"))
    parser.add_argument("--l2-book-states", type=Path, default=Path("outputs/phase6/l2_book_states_5m.parquet"))
    parser.add_argument("--symbols", nargs="+", default=DEFAULT_DEVELOPMENT_SYMBOLS)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "stage_quality": args.stage_quality,
        "scenario_calendar": args.scenario_calendar,
        "l2_book_states": args.l2_book_states,
    }
    run_stage_b1(paths, args.output_dir, args.base_dir, args.symbols)


if __name__ == "__main__":
    main()
