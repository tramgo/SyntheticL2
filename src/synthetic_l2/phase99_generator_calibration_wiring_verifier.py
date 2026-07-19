from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.generator_calibration_profiles import DEFAULT_PROFILE_ID, PROFILES, get_calibration_profile
from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase45_raw_tick_lake_materializer import build_raw_ticks
from synthetic_l2.phase49_dense_tick_rate_expansion import densify_frame
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE98_DIR = Path("outputs/phase98")
DEFAULT_OUTPUT_DIR = Path("outputs/phase99")


def metric_value(path: Path, metric: str, default: Any = None) -> Any:
    if not path.exists():
        return default
    frame = pd.read_csv(path)
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    value = rows.iloc[0]
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def fixture_events() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for idx in range(8):
        symbol = "HDFCBANK" if idx < 4 else "RELIANCE"
        rows.append(
            {
                "annual_event_id": idx + 1,
                "feed_profile": "normal_feed",
                "synthetic_year_day": 1,
                "synthetic_trade_date": "2026-01-01",
                "symbol": symbol,
                "receive_sequence": idx + 1,
                "collector_received_utc_ms": 1_800_000 + idx * 100,
                "source_sequence": idx + 1,
                "regime_code": "D01",
                "mid_price": 1000.0 + idx,
                "tick_size": 0.05,
                "spread_ticks": 2,
                "spread": 0.10,
                "event_intensity_proxy": 2.0 + idx,
                "is_market_shock_day": False,
                "is_symbol_shock": False,
                "is_duplicate": False,
                "is_disconnect_gap": False,
                "is_out_of_order_injected": False,
                "l1_imbalance": -0.20 + idx * 0.05,
                "l5_imbalance": -0.10 + idx * 0.03,
                "microprice_l1": 1000.0 + idx,
            }
        )
    return pd.DataFrame(rows)


def profile_catalog() -> pd.DataFrame:
    return pd.DataFrame([profile.to_manifest() for profile in PROFILES.values()]).sort_values("profile_id", kind="mergesort")


def verify_phase45_book_wiring(events: pd.DataFrame) -> pd.DataFrame:
    legacy = build_raw_ticks(events, calibration_profile=get_calibration_profile(DEFAULT_PROFILE_ID))
    base = build_raw_ticks(events, calibration_profile=get_calibration_profile("P98_FULL_BOOK_REBALANCE_BASE"))
    strong = build_raw_ticks(events, calibration_profile=get_calibration_profile("P98_FULL_BOOK_REBALANCE_STRONG"))
    rows = []
    for profile_id, frame in [
        (DEFAULT_PROFILE_ID, legacy),
        ("P98_FULL_BOOK_REBALANCE_BASE", base),
        ("P98_FULL_BOOK_REBALANCE_STRONG", strong),
    ]:
        rows.append(
            {
                "profile_id": profile_id,
                "rows": int(len(frame)),
                "median_l1_depth": float((frame["buy_1_quantity"] + frame["sell_1_quantity"]).median()),
                "median_l5_depth": float(
                    sum(frame[f"buy_{level}_quantity"] + frame[f"sell_{level}_quantity"] for level in range(1, 6)).median()
                ),
                "median_abs_l1_imbalance_proxy": float(
                    ((frame["buy_1_quantity"] - frame["sell_1_quantity"]) / (frame["buy_1_quantity"] + frame["sell_1_quantity"]).replace(0, np.nan)).abs().median()
                ),
                "schema_columns": int(frame.shape[1]),
            }
        )
    result = pd.DataFrame(rows)
    default_again = build_raw_ticks(events)
    result["default_matches_legacy_explicit"] = bool(legacy.equals(default_again))
    return result


def verify_phase49_dense_wiring(raw_ticks: pd.DataFrame) -> pd.DataFrame:
    source = raw_ticks.rename(
        columns={
            "callback_received_utc_ms": "callback_received_utc_ms",
            "exchange_timestamp_ms": "exchange_timestamp_ms",
            "last_trade_time_ms": "last_trade_time_ms",
        }
    ).copy()
    source["annual_event_id"] = np.arange(1, len(source) + 1)
    rows = []
    for profile_id in [DEFAULT_PROFILE_ID, "P98_TIMING_VOL_MODERATE", "P98_FULL_BOOK_REBALANCE_STRONG"]:
        dense = densify_frame(source, multiplier=4, calibration_profile=get_calibration_profile(profile_id))
        rows.append(
            {
                "profile_id": profile_id,
                "source_rows": int(len(source)),
                "dense_rows": int(len(dense)),
                "median_callback_gap_ms": float(dense["callback_received_utc_ms"].sort_values().diff().dropna().median()),
                "p90_callback_gap_ms": float(dense["callback_received_utc_ms"].sort_values().diff().dropna().quantile(0.90)),
                "last_price_std": float(dense["last_price"].astype(float).std(ddof=1)),
                "max_dense_subtick_id": int(dense["dense_subtick_id"].max()),
            }
        )
    return pd.DataFrame(rows)


def build_wiring_checks(book: pd.DataFrame, dense: pd.DataFrame, phase98_dir: Path) -> pd.DataFrame:
    phase98_ready = metric_value(phase98_dir / "generator_calibration_config_acceptance_summary.csv", "phase98_ready_for_generator_patch_wiring", 0)
    phase98_replay = metric_value(phase98_dir / "generator_calibration_config_acceptance_summary.csv", "phase98_strategy_replay_allowed", 1)
    legacy_book = book[book["profile_id"].eq(DEFAULT_PROFILE_ID)].iloc[0]
    base_book = book[book["profile_id"].eq("P98_FULL_BOOK_REBALANCE_BASE")].iloc[0]
    legacy_dense = dense[dense["profile_id"].eq(DEFAULT_PROFILE_ID)].iloc[0]
    strong_dense = dense[dense["profile_id"].eq("P98_FULL_BOOK_REBALANCE_STRONG")].iloc[0]
    return pd.DataFrame(
        [
            {
                "check_id": "P99_PHASE98_READY",
                "passed": bool(int(float(phase98_ready)) == 1),
                "detail": f"phase98_ready_for_generator_patch_wiring={phase98_ready}",
            },
            {
                "check_id": "P99_REPLAY_LOCK_PRESERVED",
                "passed": bool(int(float(phase98_replay)) == 0),
                "detail": f"phase98_strategy_replay_allowed={phase98_replay}",
            },
            {
                "check_id": "P99_DEFAULT_PROFILE_IDENTITY",
                "passed": bool(book["default_matches_legacy_explicit"].all()),
                "detail": "build_raw_ticks(events) equals explicit P98_LEGACY_DEFAULT output",
            },
            {
                "check_id": "P99_BOOK_PROFILE_HAS_EFFECT",
                "passed": bool(float(base_book["median_l5_depth"]) != float(legacy_book["median_l5_depth"])),
                "detail": "P98_FULL_BOOK_REBALANCE_BASE changes depth metrics on fixture",
            },
            {
                "check_id": "P99_DENSE_PROFILE_HAS_EFFECT",
                "passed": bool(float(strong_dense["p90_callback_gap_ms"]) != float(legacy_dense["p90_callback_gap_ms"])),
                "detail": "P98_FULL_BOOK_REBALANCE_STRONG changes dense timing metrics on fixture",
            },
        ]
    )


def summarize(checks: pd.DataFrame, catalog: pd.DataFrame) -> pd.DataFrame:
    passed = int(checks["passed"].astype(bool).sum())
    return pd.DataFrame(
        [
            ("phase99_profile_rows", int(len(catalog)), "Generator calibration profiles available in code"),
            ("phase99_wiring_check_rows", int(len(checks)), "Wiring checks executed"),
            ("phase99_wiring_checks_passed", passed, "Wiring checks passed"),
            ("phase99_wiring_pass", int(passed == len(checks)), "1 means calibration profiles are wired and replay lock is preserved"),
            ("phase99_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase99_recommend_next_action", "run_calibrated_generator_quality_smoke_no_strategy_replay", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase99 Generator Calibration Wiring Verifier",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase99 verifies that Phase98 calibration profiles are available in code and affect generator outputs when explicitly selected.",
        "It also checks that legacy default behavior is preserved and strategy replay remains locked.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase99_generator_calibration_wiring_verifier_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase99(phase98_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    events = fixture_events()
    catalog = profile_catalog()
    book = verify_phase45_book_wiring(events)
    raw_ticks = build_raw_ticks(events, calibration_profile=get_calibration_profile(DEFAULT_PROFILE_ID))
    dense = verify_phase49_dense_wiring(raw_ticks)
    checks = build_wiring_checks(book, dense, phase98_dir)
    acceptance = summarize(checks, catalog)

    catalog.to_csv(output_dir / "generator_calibration_profiles_in_code.csv", index=False)
    events.to_csv(output_dir / "phase99_fixture_events.csv", index=False)
    book.to_csv(output_dir / "phase45_book_profile_effects.csv", index=False)
    dense.to_csv(output_dir / "phase49_dense_profile_effects.csv", index=False)
    checks.to_csv(output_dir / "generator_calibration_wiring_checks.csv", index=False)
    acceptance.to_csv(output_dir / "generator_calibration_wiring_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Wiring Checks": checks,
            "Profiles In Code": catalog,
            "Phase45 Book Profile Effects": book,
            "Phase49 Dense Profile Effects": dense,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {"generated_utc": generated_utc, "scope": "phase99_generator_calibration_wiring_verifier"}
    manifest.update(
        reproducibility_fields(
            artifact_id="phase99",
            generated_utc=generated_utc,
            inputs={"phase98_acceptance": str(phase98_dir / "generator_calibration_config_acceptance_summary.csv")},
            parameters={
                "strategy_replay_policy": "closed",
                "fixture_rows": int(len(events)),
                "default_profile": DEFAULT_PROFILE_ID,
            },
            outputs={
                "profiles_in_code": str(output_dir / "generator_calibration_profiles_in_code.csv"),
                "fixture_events": str(output_dir / "phase99_fixture_events.csv"),
                "book_effects": str(output_dir / "phase45_book_profile_effects.csv"),
                "dense_effects": str(output_dir / "phase49_dense_profile_effects.csv"),
                "checks": str(output_dir / "generator_calibration_wiring_checks.csv"),
                "acceptance_summary": str(output_dir / "generator_calibration_wiring_acceptance_summary.csv"),
                "report": str(output_dir / "phase99_generator_calibration_wiring_verifier_report.md"),
                "manifest": str(output_dir / "phase99_generator_calibration_wiring_verifier_manifest.json"),
            },
            random_seed="none_deterministic_fixture",
            scenario_ids="phase99_generator_profile_fixture",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase98_generator_calibration_profile_wiring",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase99_generator_calibration_wiring_verifier_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify generator calibration profile wiring.")
    parser.add_argument("--phase98-dir", type=Path, default=DEFAULT_PHASE98_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase99(args.phase98_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
