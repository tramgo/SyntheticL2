from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE106_DIR = Path("outputs/phase106")
DEFAULT_OUTPUT_DIR = Path("outputs/phase107")


def _metric_value(path: Path, metric: str, default: Any = None) -> Any:
    if not path.exists():
        return default
    frame = pd.read_csv(path)
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def build_gap_matrix(comparison: pd.DataFrame) -> pd.DataFrame:
    matrix = comparison.copy()
    matrix["calibration_gap"] = matrix["calibration_gap"].astype(str).str.lower().eq("true")
    matrix["synthetic_to_real_ratio"] = matrix["synthetic_to_real_ratio"].astype(float)
    matrix["gap_direction"] = np.where(
        matrix["synthetic_to_real_ratio"] < matrix["lower_ratio_gate"].astype(float),
        "synthetic_too_low",
        np.where(matrix["synthetic_to_real_ratio"] > matrix["upper_ratio_gate"].astype(float), "synthetic_too_high", "inside_gate"),
    )
    matrix["severity_ratio_to_nearest_gate"] = np.where(
        matrix["gap_direction"].eq("synthetic_too_low"),
        matrix["lower_ratio_gate"].astype(float) / matrix["synthetic_to_real_ratio"].replace(0, np.nan),
        np.where(
            matrix["gap_direction"].eq("synthetic_too_high"),
            matrix["synthetic_to_real_ratio"] / matrix["upper_ratio_gate"].astype(float),
            1.0,
        ),
    )
    return matrix.sort_values(["calibration_gap", "metric", "symbol"], ascending=[False, True, True], kind="mergesort")


def action_for_gap(row: dict[str, Any]) -> tuple[str, str, float]:
    metric = str(row["metric"])
    ratio = float(row["synthetic_to_real_ratio"])
    real_value = float(row["real_value"])
    synthetic_value = float(row["synthetic_value"])
    direction = str(row["gap_direction"])
    if metric == "p90_gap_ms" and direction == "synthetic_too_low":
        needed_multiplier = real_value / synthetic_value if synthetic_value > 0 else np.nan
        return (
            "add_symbol_tail_idle_cadence_model",
            "Median cadence is mostly inside gate, so p90 gaps need symbol-specific idle/tail spacing rather than one global multiplier.",
            needed_multiplier,
        )
    if metric in {"median_l1_depth", "median_l5_depth"}:
        target_scale = real_value / synthetic_value if synthetic_value > 0 else np.nan
        return (
            "add_symbol_depth_scale_override",
            "Displayed book depth differs by symbol/instrument class; apply symbol-level quantity scale before dense audit.",
            target_scale,
        )
    if metric == "median_abs_l1_imbalance":
        target_scale = real_value / synthetic_value if synthetic_value > 0 else np.nan
        if not np.isfinite(target_scale):
            target_scale = 4.0
        return (
            "add_symbol_l1_imbalance_skew_override",
            "L1 imbalance is too damped for this symbol; amplify side imbalance while preserving positive quantities.",
            min(float(target_scale), 4.0),
        )
    return ("review_metric_specific_override", "No automatic override rule is registered for this metric.", np.nan)


def build_override_proposal(gap_matrix: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for row in gap_matrix[gap_matrix["calibration_gap"]].to_dict("records"):
        action, rationale, raw_value = action_for_gap(row)
        rows.append(
            {
                "symbol": row["symbol"],
                "metric": row["metric"],
                "gap_direction": row["gap_direction"],
                "real_value": row["real_value"],
                "synthetic_value": row["synthetic_value"],
                "synthetic_to_real_ratio": row["synthetic_to_real_ratio"],
                "proposed_action": action,
                "proposed_raw_multiplier": raw_value,
                "implementation_rationale": rationale,
            }
        )
    return pd.DataFrame(rows)


def build_patch_contract(overrides: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if overrides.empty:
        return pd.DataFrame(columns=["priority", "patch_item", "symbols_affected", "acceptance_gate"])
    grouped = overrides.groupby("proposed_action", sort=True)
    priority = 1
    for action, group in grouped:
        rows.append(
            {
                "priority": priority,
                "patch_item": action,
                "symbols_affected": int(group["symbol"].nunique()),
                "failed_metric_rows": int(len(group)),
                "representative_symbols": ";".join(sorted(group["symbol"].astype(str).unique())[:8]),
                "acceptance_gate": (
                    "Rerun Phase106-style 32-symbol calibrated realism audit; target <=25% total gaps, "
                    "no severe metric gap, and strategy replay still locked."
                ),
            }
        )
        priority += 1
    return pd.DataFrame(rows)


def summarize(gap_matrix: pd.DataFrame, overrides: pd.DataFrame, contract: pd.DataFrame, phase106_dir: Path) -> pd.DataFrame:
    gap_rows = int(gap_matrix["calibration_gap"].sum())
    all_gaps_have_actions = bool(gap_rows == len(overrides))
    return pd.DataFrame(
        [
            ("phase107_phase106_gap_rows", gap_rows, "Phase106 failed symbol-metric anchors triaged"),
            ("phase107_override_rows", int(len(overrides)), "Concrete symbol/metric override proposals emitted"),
            ("phase107_patch_items", int(len(contract)), "Distinct implementation patch items required"),
            ("phase107_all_gaps_have_actions", int(all_gaps_have_actions), "1 means every Phase106 gap has a proposed action"),
            (
                "phase107_phase106_gap_fraction",
                _metric_value(phase106_dir / "phase106_full_symbol_calibrated_realism_acceptance_summary.csv", "phase106_calibration_gap_fraction", "missing"),
                "Inherited Phase106 full-symbol gap fraction",
            ),
            (
                "phase107_phase106_severe_metric_gap_count",
                _metric_value(phase106_dir / "phase106_full_symbol_calibrated_realism_acceptance_summary.csv", "phase106_severe_metric_gap_count", "missing"),
                "Inherited Phase106 severe metric count",
            ),
            ("phase107_ready_for_symbol_aware_generator_patch", int(all_gaps_have_actions and gap_rows > 0), "1 means Phase108 can implement overrides"),
            ("phase107_strategy_replay_allowed", 0, "Strategy replay remains closed"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase107 Symbol-Aware Calibration Contract",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase107 converts the Phase106 full-symbol realism gaps into executable calibration patch items.",
        "It does not reopen strategy replay.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase107_symbol_aware_calibration_contract_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase107(phase106_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    comparison = pd.read_csv(phase106_dir / "real_vs_calibrated_synthetic_comparison.csv")
    gap_matrix = build_gap_matrix(comparison)
    overrides = build_override_proposal(gap_matrix)
    contract = build_patch_contract(overrides)
    acceptance = summarize(gap_matrix, overrides, contract, phase106_dir)

    gap_matrix.to_csv(output_dir / "phase107_symbol_gap_matrix.csv", index=False)
    overrides.to_csv(output_dir / "phase107_symbol_override_proposal.csv", index=False)
    contract.to_csv(output_dir / "phase107_patch_contract.csv", index=False)
    acceptance.to_csv(output_dir / "phase107_symbol_aware_calibration_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Patch Contract": contract,
            "Override Proposal": overrides,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase107_symbol_aware_calibration_contract",
        **reproducibility_fields(
            artifact_id="phase107",
            generated_utc=generated_utc,
            inputs={
                "phase106_comparison": str(phase106_dir / "real_vs_calibrated_synthetic_comparison.csv"),
                "phase106_acceptance": str(phase106_dir / "phase106_full_symbol_calibrated_realism_acceptance_summary.csv"),
            },
            parameters={
                "strategy_replay_policy": "closed",
                "contract_policy": "all_phase106_gaps_must_have_patch_action",
            },
            outputs={
                "gap_matrix": str(output_dir / "phase107_symbol_gap_matrix.csv"),
                "override_proposal": str(output_dir / "phase107_symbol_override_proposal.csv"),
                "patch_contract": str(output_dir / "phase107_patch_contract.csv"),
                "acceptance_summary": str(output_dir / "phase107_symbol_aware_calibration_acceptance_summary.csv"),
                "report": str(output_dir / "phase107_symbol_aware_calibration_contract_report.md"),
                "manifest": str(output_dir / "phase107_symbol_aware_calibration_contract_manifest.json"),
            },
            random_seed="none_deterministic_phase107_contract",
            scenario_ids="phase107_from_phase106_full_symbol_gaps",
            cost_model_version="not_applicable",
            latency_model_version="phase106_full_symbol_calibrated_realism",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase107_symbol_aware_calibration_contract_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build symbol-aware calibration contract from Phase106 gaps.")
    parser.add_argument("--phase106-dir", type=Path, default=DEFAULT_PHASE106_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase107(args.phase106_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
