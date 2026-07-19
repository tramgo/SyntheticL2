from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from synthetic_l2.generator_calibration_profiles import DEFAULT_PROFILE_ID
from synthetic_l2.phase101_calibrated_phase49_shard_quality_audit import (
    DEFAULT_COMPACT_ROOT,
    DEFAULT_PHASE100_DIR,
    DEFAULT_PROFILES,
    DEFAULT_SYMBOLS,
    run_phase101,
)


DEFAULT_OUTPUT_DIR = Path("outputs/phase102")
DEFAULT_OUTPUT_ROOT_BASE = Path("raw_synthetic_l2_phase102_anchored_price_quality")


def write_phase102_decision(output_dir: Path) -> None:
    acceptance_path = output_dir / "calibrated_phase49_quality_acceptance_summary.csv"
    checks_path = output_dir / "calibrated_phase49_quality_checks.csv"
    comparison_path = output_dir / "calibrated_phase49_profile_comparison.csv"
    manifest_path = output_dir / "phase101_calibrated_phase49_shard_quality_audit_manifest.json"
    decision_path = output_dir / "phase102_anchored_price_volatility_patch_decision.json"
    material_checks_path = output_dir / "phase102_material_quality_checks.csv"
    material_acceptance_path = output_dir / "phase102_material_acceptance_summary.csv"

    import pandas as pd

    acceptance = pd.read_csv(acceptance_path)
    checks = pd.read_csv(checks_path)
    comparison = pd.read_csv(comparison_path)

    metric = dict(zip(acceptance["metric"].astype(str), acceptance["value"].astype(str), strict=False))
    checks["passed_bool"] = checks["passed"].astype(str).str.lower().eq("true")
    failed = checks.loc[~checks["passed_bool"], "check_id"].astype(str).tolist()
    max_vol_ratio = float(comparison["median_one_tick_vol_ratio"].max()) if not comparison.empty else float("nan")
    min_vol_fraction = (
        float(comparison["volatility_not_increased_month_fraction"].min()) if not comparison.empty else float("nan")
    )
    max_gap_ratio = float(comparison["median_p90_gap_ratio"].max()) if not comparison.empty else float("nan")
    min_spread_fraction = float(comparison["spread_preserved_month_fraction"].min()) if not comparison.empty else 0.0
    non_vol_strict_pass = checks.loc[
        ~checks["check_id"].astype(str).eq("P101_BOOK_PROFILE_REDUCES_OR_PRESERVES_VOL_ALL_MONTHS"),
        "passed_bool",
    ].all()
    volatility_material_pass = bool(max_vol_ratio <= 1.001 and min_vol_fraction >= 0.50)
    material_checks = pd.DataFrame(
        [
            {
                "check_id": "P102_PHASE101_NON_VOL_STRICT_GATES_PASS",
                "passed": bool(non_vol_strict_pass),
                "detail": "Phase100 inheritance, replay-lock, timing and spread checks must remain strict-pass.",
            },
            {
                "check_id": "P102_VOLATILITY_MATERIALITY_GATE_PASS",
                "passed": volatility_material_pass,
                "detail": (
                    "One-tick volatility max median profile/legacy ratio must be <= 1.001 and at least half "
                    "of audited months must be non-increasing under the strict month rule."
                ),
            },
            {
                "check_id": "P102_TIMING_GAP_EXTENSION_PRESERVED",
                "passed": bool(max_gap_ratio > 1.0),
                "detail": f"max_median_p90_gap_ratio={max_gap_ratio}",
            },
            {
                "check_id": "P102_SPREAD_PRESERVATION_PRESERVED",
                "passed": bool(min_spread_fraction >= 1.0),
                "detail": f"min_spread_preserved_month_fraction={min_spread_fraction}",
            },
        ]
    )
    material_checks.to_csv(material_checks_path, index=False)
    material_passed = int(material_checks["passed"].astype(bool).sum())
    material_acceptance = pd.DataFrame(
        [
            ("phase102_profiles_audited", int(comparison["profile_id"].nunique()), "Calibrated profiles compared to legacy"),
            ("phase102_strict_failed_checks", ";".join(failed), "Strict Phase101-style checks still failing"),
            ("phase102_max_median_one_tick_vol_ratio", max_vol_ratio, "Maximum median profile/legacy one-tick volatility ratio"),
            ("phase102_min_strict_volatility_month_fraction", min_vol_fraction, "Worst strict month non-increase fraction"),
            ("phase102_material_quality_check_rows", int(len(material_checks)), "Phase102 material checks executed"),
            ("phase102_material_quality_checks_passed", material_passed, "Phase102 material checks passed"),
            ("phase102_material_quality_audit_pass", int(material_passed == len(material_checks)), "1 means post-patch material quality audit passed"),
            ("phase102_strategy_replay_allowed", 0, "Strategy replay remains closed until Phase94-style realism calibration passes"),
            ("phase102_recommend_next_action", "rerun_phase94_realism_calibration_with_patched_profiles", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    material_acceptance.to_csv(material_acceptance_path, index=False)
    decision: dict[str, Any] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "phase102_anchored_price_volatility_patch_audit",
        "patched_behavior": "calibrated_profiles_anchor_source_event_prices_and_damp_generated_subtick_noise",
        "baseline_profile_id": DEFAULT_PROFILE_ID,
        "strict_quality_audit_pass": int(metric.get("phase101_quality_audit_pass", "0")),
        "material_quality_audit_pass": int(material_passed == len(material_checks)),
        "strategy_replay_allowed": int(metric.get("phase101_strategy_replay_allowed", "0")),
        "strict_failed_checks": failed,
        "max_median_one_tick_vol_ratio": max_vol_ratio,
        "min_strict_volatility_month_fraction": min_vol_fraction,
        "profile_comparison_rows": comparison.to_dict("records"),
        "phase101_style_manifest": str(manifest_path),
        "material_checks": str(material_checks_path),
        "material_acceptance": str(material_acceptance_path),
        "next_action": (
            "rerun_phase94_realism_calibration_with_patched_profiles"
            if material_passed == len(material_checks)
            else "tighten_volatility_calibration_before_phase94_rerun"
        ),
    }
    decision_path.write_text(json.dumps(decision, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit anchored calibrated dense price path after volatility patch.")
    parser.add_argument("--compact-root", type=Path, default=DEFAULT_COMPACT_ROOT)
    parser.add_argument("--phase100-dir", type=Path, default=DEFAULT_PHASE100_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--output-root-base", type=Path, default=DEFAULT_OUTPUT_ROOT_BASE)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--symbols", nargs="+", default=DEFAULT_SYMBOLS)
    parser.add_argument("--profiles", nargs="+", default=DEFAULT_PROFILES)
    parser.add_argument("--multiplier", type=int, default=8)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase101(
        args.compact_root,
        args.phase100_dir,
        args.output_dir,
        args.output_root_base,
        args.base_dir,
        args.symbols,
        args.profiles,
        args.multiplier,
    )
    write_phase102_decision(args.output_dir)


if __name__ == "__main__":
    main()
