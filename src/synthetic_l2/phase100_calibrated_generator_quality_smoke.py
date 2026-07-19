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
from synthetic_l2.phase99_generator_calibration_wiring_verifier import fixture_events
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE97_DIR = Path("outputs/phase97")
DEFAULT_PHASE99_DIR = Path("outputs/phase99")
DEFAULT_OUTPUT_DIR = Path("outputs/phase100")


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


def build_profile_outputs(multiplier: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    events = fixture_events()
    raw_rows: list[dict[str, Any]] = []
    dense_rows: list[dict[str, Any]] = []
    for profile_id in sorted(PROFILES):
        profile = get_calibration_profile(profile_id)
        raw = build_raw_ticks(events, calibration_profile=profile)
        raw_rows.append(
            {
                "profile_id": profile_id,
                "raw_rows": int(len(raw)),
                "median_l1_depth": float((raw["buy_1_quantity"] + raw["sell_1_quantity"]).median()),
                "median_l5_depth": float(
                    sum(raw[f"buy_{level}_quantity"] + raw[f"sell_{level}_quantity"] for level in range(1, 6)).median()
                ),
                "median_abs_l1_imbalance_proxy": float(
                    (
                        (raw["buy_1_quantity"] - raw["sell_1_quantity"])
                        / (raw["buy_1_quantity"] + raw["sell_1_quantity"]).replace(0, np.nan)
                    )
                    .abs()
                    .median()
                ),
                "median_spread_bps_proxy": float(
                    ((raw["sell_1_price"] - raw["buy_1_price"]) / ((raw["sell_1_price"] + raw["buy_1_price"]) / 2.0) * 10000.0).median()
                ),
            }
        )
        dense_source = raw.copy()
        dense_source["annual_event_id"] = np.arange(1, len(dense_source) + 1)
        dense = densify_frame(dense_source, multiplier=multiplier, calibration_profile=profile)
        gaps = dense["callback_received_utc_ms"].sort_values().diff().dropna()
        dense_rows.append(
            {
                "profile_id": profile_id,
                "source_rows": int(len(dense_source)),
                "dense_rows": int(len(dense)),
                "dense_multiplier": int(multiplier),
                "median_callback_gap_ms": float(gaps.median()),
                "p90_callback_gap_ms": float(gaps.quantile(0.90)),
                "last_price_std": float(dense["last_price"].astype(float).std(ddof=1)),
                "spread_preservation_proxy": float(
                    ((dense["sell_1_price"] - dense["buy_1_price"]) / ((dense["sell_1_price"] + dense["buy_1_price"]) / 2.0) * 10000.0).median()
                ),
            }
        )
    return pd.DataFrame(raw_rows), pd.DataFrame(dense_rows)


def compare_to_legacy(raw: pd.DataFrame, dense: pd.DataFrame) -> pd.DataFrame:
    legacy_raw = raw[raw["profile_id"].eq(DEFAULT_PROFILE_ID)].iloc[0]
    legacy_dense = dense[dense["profile_id"].eq(DEFAULT_PROFILE_ID)].iloc[0]
    rows: list[dict[str, Any]] = []
    for profile_id in sorted(set(raw["profile_id"]) - {DEFAULT_PROFILE_ID}):
        r = raw[raw["profile_id"].eq(profile_id)].iloc[0]
        d = dense[dense["profile_id"].eq(profile_id)].iloc[0]
        rows.append(
            {
                "profile_id": profile_id,
                "p90_gap_ms_ratio_vs_legacy": float(d["p90_callback_gap_ms"] / legacy_dense["p90_callback_gap_ms"]),
                "last_price_std_ratio_vs_legacy": float(d["last_price_std"] / legacy_dense["last_price_std"]),
                "median_abs_l1_imbalance_ratio_vs_legacy": float(
                    r["median_abs_l1_imbalance_proxy"] / legacy_raw["median_abs_l1_imbalance_proxy"]
                ),
                "median_l5_depth_ratio_vs_legacy": float(r["median_l5_depth"] / legacy_raw["median_l5_depth"]),
                "spread_bps_ratio_vs_legacy": float(r["median_spread_bps_proxy"] / legacy_raw["median_spread_bps_proxy"]),
                "tail_gap_improves": bool(d["p90_callback_gap_ms"] > legacy_dense["p90_callback_gap_ms"]),
                "volatility_not_increased": bool(d["last_price_std"] <= legacy_dense["last_price_std"]),
                "l1_imbalance_increases": bool(r["median_abs_l1_imbalance_proxy"] >= legacy_raw["median_abs_l1_imbalance_proxy"]),
                "spread_preserved": bool(abs((r["median_spread_bps_proxy"] / legacy_raw["median_spread_bps_proxy"]) - 1.0) <= 0.05),
            }
        )
    return pd.DataFrame(rows)


def build_quality_checks(profile_comparison: pd.DataFrame, phase97_dir: Path, phase99_dir: Path) -> pd.DataFrame:
    phase99_pass = metric_value(phase99_dir / "generator_calibration_wiring_acceptance_summary.csv", "phase99_wiring_pass", 0)
    phase99_replay = metric_value(phase99_dir / "generator_calibration_wiring_acceptance_summary.csv", "phase99_strategy_replay_allowed", 1)
    base = profile_comparison[profile_comparison["profile_id"].eq("P98_FULL_BOOK_REBALANCE_BASE")]
    strong = profile_comparison[profile_comparison["profile_id"].eq("P98_FULL_BOOK_REBALANCE_STRONG")]
    timing = profile_comparison[profile_comparison["profile_id"].eq("P98_TIMING_VOL_MODERATE")]
    severe_rows = metric_value(phase97_dir / "generator_recalibration_patch_acceptance_summary.csv", "phase97_severe_patch_rows", 0)
    return pd.DataFrame(
        [
            {
                "check_id": "P100_PHASE99_WIRING_PASS",
                "passed": bool(int(float(phase99_pass)) == 1),
                "detail": f"phase99_wiring_pass={phase99_pass}",
            },
            {
                "check_id": "P100_REPLAY_LOCK_PRESERVED",
                "passed": bool(int(float(phase99_replay)) == 0),
                "detail": f"phase99_strategy_replay_allowed={phase99_replay}",
            },
            {
                "check_id": "P100_SEVERE_GAPS_PRESENT_FOR_SMOKE",
                "passed": bool(int(float(severe_rows)) >= 2),
                "detail": f"phase97_severe_patch_rows={severe_rows}",
            },
            {
                "check_id": "P100_TIMING_PROFILE_MOVES_TAIL_GAP",
                "passed": bool(not timing.empty and bool(timing.iloc[0]["tail_gap_improves"])),
                "detail": "P98_TIMING_VOL_MODERATE should increase p90 callback gap vs legacy on fixture.",
            },
            {
                "check_id": "P100_FULL_PROFILE_REDUCES_OR_PRESERVES_VOL",
                "passed": bool(not base.empty and bool(base.iloc[0]["volatility_not_increased"])),
                "detail": "P98_FULL_BOOK_REBALANCE_BASE should not increase last-price fixture volatility vs legacy.",
            },
            {
                "check_id": "P100_FULL_PROFILE_INCREASES_L1_IMBALANCE",
                "passed": bool(not base.empty and bool(base.iloc[0]["l1_imbalance_increases"])),
                "detail": "P98_FULL_BOOK_REBALANCE_BASE should increase L1 imbalance dispersion vs legacy.",
            },
            {
                "check_id": "P100_SPREAD_ANCHOR_PRESERVED",
                "passed": bool(not strong.empty and profile_comparison["spread_preserved"].astype(bool).all()),
                "detail": "All calibrated profiles should preserve median spread proxy within 5%.",
            },
        ]
    )


def summarize(raw: pd.DataFrame, dense: pd.DataFrame, comparison: pd.DataFrame, checks: pd.DataFrame) -> pd.DataFrame:
    passed = int(checks["passed"].astype(bool).sum())
    return pd.DataFrame(
        [
            ("phase100_profiles_smoked", int(raw["profile_id"].nunique()), "Profiles evaluated in generator quality smoke"),
            ("phase100_dense_multiplier", int(dense["dense_multiplier"].iloc[0]) if not dense.empty else 0, "Dense multiplier used for fixture smoke"),
            ("phase100_profile_comparison_rows", int(len(comparison)), "Non-legacy profiles compared with legacy"),
            ("phase100_quality_check_rows", int(len(checks)), "Quality smoke checks executed"),
            ("phase100_quality_checks_passed", passed, "Quality smoke checks passed"),
            ("phase100_quality_smoke_pass", int(passed == len(checks)), "1 means calibrated generator quality smoke passed"),
            ("phase100_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase100_recommend_next_action", "run_small_calibrated_phase49_shard_quality_audit_no_strategy_replay", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase100 Calibrated Generator Quality Smoke",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase100 runs a fixture-level generator quality smoke for the Phase98/99 calibration profiles.",
        "It checks that profiles move failed calibration anchors in the intended direction while preserving spread and keeping strategy replay locked.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase100_calibrated_generator_quality_smoke_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase100(phase97_dir: Path, phase99_dir: Path, output_dir: Path, base_dir: Path, multiplier: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    raw, dense = build_profile_outputs(multiplier=multiplier)
    comparison = compare_to_legacy(raw, dense)
    checks = build_quality_checks(comparison, phase97_dir, phase99_dir)
    acceptance = summarize(raw, dense, comparison, checks)

    raw.to_csv(output_dir / "raw_book_profile_quality_smoke.csv", index=False)
    dense.to_csv(output_dir / "dense_timing_profile_quality_smoke.csv", index=False)
    comparison.to_csv(output_dir / "profile_quality_comparison_vs_legacy.csv", index=False)
    checks.to_csv(output_dir / "calibrated_generator_quality_checks.csv", index=False)
    acceptance.to_csv(output_dir / "calibrated_generator_quality_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Quality Checks": checks,
            "Profile Comparison vs Legacy": comparison,
            "Raw Book Profile Smoke": raw,
            "Dense Timing Profile Smoke": dense,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {"generated_utc": generated_utc, "scope": "phase100_calibrated_generator_quality_smoke"}
    manifest.update(
        reproducibility_fields(
            artifact_id="phase100",
            generated_utc=generated_utc,
            inputs={
                "phase97_acceptance": str(phase97_dir / "generator_recalibration_patch_acceptance_summary.csv"),
                "phase99_acceptance": str(phase99_dir / "generator_calibration_wiring_acceptance_summary.csv"),
            },
            parameters={
                "strategy_replay_policy": "closed",
                "dense_multiplier": multiplier,
                "fixture_source": "phase99_fixture_events",
                "quality_scope": "fixture_smoke_not_full_calibration_acceptance",
            },
            outputs={
                "raw_book_smoke": str(output_dir / "raw_book_profile_quality_smoke.csv"),
                "dense_timing_smoke": str(output_dir / "dense_timing_profile_quality_smoke.csv"),
                "profile_comparison": str(output_dir / "profile_quality_comparison_vs_legacy.csv"),
                "checks": str(output_dir / "calibrated_generator_quality_checks.csv"),
                "acceptance_summary": str(output_dir / "calibrated_generator_quality_acceptance_summary.csv"),
                "report": str(output_dir / "phase100_calibrated_generator_quality_smoke_report.md"),
                "manifest": str(output_dir / "phase100_calibrated_generator_quality_smoke_manifest.json"),
            },
            random_seed="none_deterministic_fixture_smoke",
            scenario_ids="phase100_generator_profile_fixture_quality_smoke",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase98_phase99_generator_profile_wiring",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase100_calibrated_generator_quality_smoke_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run calibrated generator quality smoke without strategy replay.")
    parser.add_argument("--phase97-dir", type=Path, default=DEFAULT_PHASE97_DIR)
    parser.add_argument("--phase99-dir", type=Path, default=DEFAULT_PHASE99_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--multiplier", type=int, default=8)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase100(args.phase97_dir, args.phase99_dir, args.output_dir, args.base_dir, args.multiplier)


if __name__ == "__main__":
    main()
