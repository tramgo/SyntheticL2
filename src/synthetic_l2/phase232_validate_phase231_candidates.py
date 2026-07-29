from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE231_DIR = Path("outputs/phase231")
DEFAULT_OUTPUT_DIR = Path("outputs/phase232")
CONTROL_SEEDS = list(range(1, 101))
COST_STRESS_MULTIPLIERS = [1.25, 1.50]


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns or "value" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def deterministic_sign(candidate_id: str, row_key: str, seed: int) -> int:
    digest = hashlib.sha256(f"{candidate_id}|{row_key}|{seed}".encode("utf-8")).hexdigest()
    return 1 if int(digest[:12], 16) % 2 == 0 else -1


def split_stats(trades: pd.DataFrame, split: str) -> dict[str, Any]:
    group = trades[trades["split"].astype(str).eq(split)].copy()
    if group.empty:
        return {
            f"{split}_trades": 0,
            f"{split}_net_pnl_inr": 0.0,
            f"{split}_gross_pnl_inr": 0.0,
            f"{split}_cost_pnl_drag_inr": 0.0,
            f"{split}_positive_months": 0,
            f"{split}_months": 0,
            f"{split}_symbols": 0,
            f"{split}_days": 0,
            f"{split}_min_month_net_pnl_inr": 0.0,
            f"{split}_leave_one_month_min_net_pnl_inr": 0.0,
            f"{split}_max_month_contribution_abs": np.nan,
            f"{split}_max_symbol_contribution_abs": np.nan,
        }
    net = float(group["net_pnl_inr"].sum())
    month_net = group.groupby("trade_month", sort=True)["net_pnl_inr"].sum()
    symbol_net = group.groupby("symbol", sort=True)["net_pnl_inr"].sum()
    leave_one = [net - float(value) for value in month_net.to_list()]
    denom = abs(net) if abs(net) > 0 else np.nan
    return {
        f"{split}_trades": int(len(group)),
        f"{split}_net_pnl_inr": net,
        f"{split}_gross_pnl_inr": float(group["gross_pnl_inr"].sum()),
        f"{split}_cost_pnl_drag_inr": float(group["cost_pnl_drag_inr"].sum()),
        f"{split}_positive_months": int((month_net > 0).sum()),
        f"{split}_months": int(month_net.shape[0]),
        f"{split}_symbols": int(group["symbol"].nunique()),
        f"{split}_days": int(group["trade_date"].nunique()),
        f"{split}_min_month_net_pnl_inr": float(month_net.min()),
        f"{split}_leave_one_month_min_net_pnl_inr": float(min(leave_one)) if leave_one else 0.0,
        f"{split}_max_month_contribution_abs": float(month_net.abs().max() / denom) if denom and not np.isnan(denom) else np.nan,
        f"{split}_max_symbol_contribution_abs": float(symbol_net.abs().max() / denom) if denom and not np.isnan(denom) else np.nan,
    }


def cost_stress_rows(trades: pd.DataFrame, candidate_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split, group in trades.groupby("split", sort=True):
        for multiplier in COST_STRESS_MULTIPLIERS:
            gross = float(group["gross_pnl_inr"].sum())
            stressed_cost = float(group["cost_pnl_drag_inr"].sum() * multiplier)
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "split": split,
                    "cost_multiplier": multiplier,
                    "gross_pnl_inr": gross,
                    "stressed_cost_pnl_drag_inr": stressed_cost,
                    "stressed_net_pnl_inr": gross - stressed_cost,
                    "stress_pass": gross - stressed_cost > 0,
                }
            )
    return rows


def side_flip_rows(trades: pd.DataFrame, candidate_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split, group in trades.groupby("split", sort=True):
        flipped_net = float((-group["gross_pnl_inr"] - group["cost_pnl_drag_inr"]).sum())
        rows.append(
            {
                "candidate_id": candidate_id,
                "split": split,
                "side_flip_net_pnl_inr": flipped_net,
                "side_flip_negative_control_pass": flipped_net < 0,
            }
        )
    return rows


def random_side_control_rows(trades: pd.DataFrame, candidate_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    frame = trades.copy()
    frame["future_return"] = frame["gross_return"] / frame["side"].replace(0, np.nan)
    frame["row_key"] = (
        frame["trade_month"].astype(str)
        + "|"
        + frame["trade_date"].astype(str)
        + "|"
        + frame["feed_profile"].astype(str)
        + "|"
        + frame["symbol"].astype(str)
        + "|"
        + frame["source_event_bar_id"].astype(str)
    )
    actual_by_split = frame.groupby("split", sort=True)["net_pnl_inr"].sum().to_dict()
    for seed in CONTROL_SEEDS:
        signs = frame["row_key"].map(lambda key: deterministic_sign(candidate_id, str(key), seed)).astype(float)
        frame[f"random_net_{seed}"] = (signs * frame["future_return"] - frame["cost_return"]) * 100000.0
        for split, group in frame.groupby("split", sort=True):
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "split": split,
                    "control_seed": seed,
                    "actual_net_pnl_inr": float(actual_by_split.get(split, 0.0)),
                    "random_side_net_pnl_inr": float(group[f"random_net_{seed}"].sum()),
                    "actual_beats_random": float(actual_by_split.get(split, 0.0)) > float(group[f"random_net_{seed}"].sum()),
                }
            )
        frame = frame.drop(columns=[f"random_net_{seed}"])
    return rows


def evaluate_candidate(candidate: dict[str, Any], trades: pd.DataFrame) -> dict[str, Any]:
    candidate_id = str(candidate["candidate_id"])
    row = {
        "candidate_id": candidate_id,
        "family_id": candidate.get("family_id", ""),
        "horizon_event_bars": candidate.get("horizon_event_bars", ""),
        "threshold_quantile": candidate.get("threshold_quantile", ""),
        "phase231_train_net_pnl_inr": candidate.get("train_net_pnl_inr", 0.0),
        "phase231_test_net_pnl_inr": candidate.get("test_net_pnl_inr", 0.0),
    }
    row.update(split_stats(trades, "train"))
    row.update(split_stats(trades, "test"))
    stress = pd.DataFrame(cost_stress_rows(trades, candidate_id))
    flips = pd.DataFrame(side_flip_rows(trades, candidate_id))
    random_controls = pd.DataFrame(random_side_control_rows(trades, candidate_id))
    test_random = random_controls[random_controls["split"].astype(str).eq("test")].copy()
    train_random = random_controls[random_controls["split"].astype(str).eq("train")].copy()
    row["train_random_side_beat_fraction"] = float(train_random["actual_beats_random"].mean()) if not train_random.empty else 0.0
    row["test_random_side_beat_fraction"] = float(test_random["actual_beats_random"].mean()) if not test_random.empty else 0.0
    row["test_random_side_p95_net_pnl_inr"] = float(test_random["random_side_net_pnl_inr"].quantile(0.95)) if not test_random.empty else 0.0
    row["test_side_flip_net_pnl_inr"] = float(flips.loc[flips["split"].astype(str).eq("test"), "side_flip_net_pnl_inr"].iloc[0]) if not flips.empty and flips["split"].astype(str).eq("test").any() else 0.0
    row["train_cost_125_pass"] = bool(stress.loc[stress["split"].astype(str).eq("train") & stress["cost_multiplier"].eq(1.25), "stress_pass"].iloc[0]) if not stress.empty and (stress["split"].astype(str).eq("train") & stress["cost_multiplier"].eq(1.25)).any() else False
    row["test_cost_125_pass"] = bool(stress.loc[stress["split"].astype(str).eq("test") & stress["cost_multiplier"].eq(1.25), "stress_pass"].iloc[0]) if not stress.empty and (stress["split"].astype(str).eq("test") & stress["cost_multiplier"].eq(1.25)).any() else False
    row["test_cost_150_pass"] = bool(stress.loc[stress["split"].astype(str).eq("test") & stress["cost_multiplier"].eq(1.50), "stress_pass"].iloc[0]) if not stress.empty and (stress["split"].astype(str).eq("test") & stress["cost_multiplier"].eq(1.50)).any() else False
    row["negative_controls_pass"] = bool(row["test_side_flip_net_pnl_inr"] < 0 and row["test_random_side_beat_fraction"] >= 0.95 and row["test_net_pnl_inr"] > row["test_random_side_p95_net_pnl_inr"])
    row["cost_stress_pass"] = bool(row["train_cost_125_pass"] and row["test_cost_125_pass"] and row["test_cost_150_pass"])
    row["holdout_stability_pass"] = bool(
        row["test_net_pnl_inr"] > 0
        and row["test_positive_months"] >= 4
        and row["test_leave_one_month_min_net_pnl_inr"] > 0
        and row["test_max_month_contribution_abs"] <= 0.65
        and row["test_max_symbol_contribution_abs"] <= 0.65
    )
    row["phase232_validated_synthetic_candidate"] = bool(row["negative_controls_pass"] and row["cost_stress_pass"] and row["holdout_stability_pass"])
    return row


def run_validation(candidate_summary: pd.DataFrame, trade_ledger: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    candidates = candidate_summary[candidate_summary["phase231_synthetic_candidate"].astype(bool)].copy()
    validation_rows: list[dict[str, Any]] = []
    stress_rows: list[dict[str, Any]] = []
    flip_rows_list: list[dict[str, Any]] = []
    random_rows: list[dict[str, Any]] = []
    for candidate in candidates.to_dict("records"):
        candidate_id = str(candidate["candidate_id"])
        trades = trade_ledger[trade_ledger["candidate_id"].astype(str).eq(candidate_id)].copy()
        validation_rows.append(evaluate_candidate(candidate, trades))
        stress_rows.extend(cost_stress_rows(trades, candidate_id))
        flip_rows_list.extend(side_flip_rows(trades, candidate_id))
        random_rows.extend(random_side_control_rows(trades, candidate_id))
    validation = pd.DataFrame(validation_rows).sort_values(
        ["phase232_validated_synthetic_candidate", "test_net_pnl_inr"],
        ascending=[False, False],
        kind="mergesort",
    )
    return validation, pd.DataFrame(stress_rows), pd.DataFrame(flip_rows_list), pd.DataFrame(random_rows)


def build_gate_evaluation(validation: pd.DataFrame, phase231_acceptance: pd.DataFrame) -> pd.DataFrame:
    inherited = as_int(metric_value(phase231_acceptance, "phase231_synthetic_candidate_rows", 0))
    validated = int(validation["phase232_validated_synthetic_candidate"].sum()) if not validation.empty else 0
    negative_controls = int(validation["negative_controls_pass"].sum()) if not validation.empty else 0
    cost_stress = int(validation["cost_stress_pass"].sum()) if not validation.empty else 0
    holdout = int(validation["holdout_stability_pass"].sum()) if not validation.empty else 0
    return pd.DataFrame(
        [
            {
                "gate_id": "P232_PHASE231_CANDIDATES_AVAILABLE",
                "passed": inherited > 0,
                "observed_value": inherited,
                "required_value": ">0 Phase231 candidates",
                "interpretation": "Phase232 has Phase231 candidates to validate.",
            },
            {
                "gate_id": "P232_NEGATIVE_CONTROLS_PASS",
                "passed": negative_controls > 0,
                "observed_value": negative_controls,
                "required_value": ">0 candidates pass side-flip and random-side controls",
                "interpretation": "Candidate performance beats deterministic negative controls.",
            },
            {
                "gate_id": "P232_COST_STRESS_PASS",
                "passed": cost_stress > 0,
                "observed_value": cost_stress,
                "required_value": ">0 candidates pass cost stress",
                "interpretation": "Candidate remains positive under 1.25x train/test and 1.50x test cost stress.",
            },
            {
                "gate_id": "P232_HOLDOUT_STABILITY_PASS",
                "passed": holdout > 0,
                "observed_value": holdout,
                "required_value": ">0 candidates pass month/symbol stability",
                "interpretation": "Candidate is not solely one-month or one-symbol dominated under the configured thresholds.",
            },
            {
                "gate_id": "P232_VALIDATED_SYNTHETIC_CANDIDATE_FOUND",
                "passed": validated > 0,
                "observed_value": validated,
                "required_value": ">0 candidates pass all Phase232 validation gates",
                "interpretation": "Validated synthetic candidates may proceed to stricter fragility/realism validation, not promotion.",
            },
        ]
    )


def metric_frame(rows: list[tuple[str, Any, str]]) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase232 Phase231 Candidate Validation",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase232 validates only the Phase231 train+test synthetic candidates using stricter holdout/concentration checks,",
        "cost stress, side-flip negative controls and deterministic random-side controls.",
        "Passing this phase is still synthetic-only validation; it does not promote a strategy or authorize paper/live use.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase232_validate_phase231_candidates_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase232(phase231_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase231_acceptance = read_csv(phase231_dir / "phase231_acceptance_summary.csv")
    candidate_summary = read_csv(phase231_dir / "phase231_candidate_summary.csv")
    trade_ledger = read_csv(phase231_dir / "phase231_trade_ledger.csv")
    validation, stress, flips, random_controls = run_validation(candidate_summary, trade_ledger)
    gates = build_gate_evaluation(validation, phase231_acceptance)
    best = validation.head(1)
    validated = int(validation["phase232_validated_synthetic_candidate"].sum()) if not validation.empty else 0
    next_action = (
        "run_phase233_fragility_and_realism_validation_for_phase232_candidates_no_paper_live"
        if validated > 0
        else "run_phase233_redesign_or_tighten_phase231_candidates_no_paper_live"
    )
    acceptance = metric_frame(
        [
            ("phase232_validate_phase231_candidates_complete", 1, "Phase232 validation completed"),
            ("phase232_phase231_candidate_rows", int(len(validation)), "Phase231 train+test candidates validated"),
            ("phase232_negative_control_pass_rows", int(validation["negative_controls_pass"].sum()) if not validation.empty else 0, "Candidates passing negative controls"),
            ("phase232_cost_stress_pass_rows", int(validation["cost_stress_pass"].sum()) if not validation.empty else 0, "Candidates passing cost stress"),
            ("phase232_holdout_stability_pass_rows", int(validation["holdout_stability_pass"].sum()) if not validation.empty else 0, "Candidates passing holdout/concentration stability"),
            ("phase232_validated_synthetic_candidate_rows", validated, "Candidates passing all Phase232 gates"),
            ("phase232_best_candidate_id", best["candidate_id"].iloc[0] if not best.empty else "none", "Best validated or ranked candidate"),
            ("phase232_best_test_net_pnl_inr", float(best["test_net_pnl_inr"].iloc[0]) if not best.empty else 0.0, "Best candidate test net P&L"),
            ("phase232_best_test_random_side_beat_fraction", float(best["test_random_side_beat_fraction"].iloc[0]) if not best.empty else 0.0, "Best candidate test random-side beat fraction"),
            ("phase232_best_test_leave_one_month_min_net_pnl_inr", float(best["test_leave_one_month_min_net_pnl_inr"].iloc[0]) if not best.empty else 0.0, "Best candidate minimum leave-one-test-month net P&L"),
            ("phase232_strategy_promotion_allowed", 0, "No promotion from synthetic validation alone"),
            ("phase232_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from synthetic validation alone"),
            ("phase232_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from synthetic validation alone"),
            ("phase232_next_best_action", next_action, "Next validation milestone"),
        ]
    )

    validation.to_csv(output_dir / "phase232_candidate_validation_summary.csv", index=False)
    stress.to_csv(output_dir / "phase232_cost_stress_summary.csv", index=False)
    flips.to_csv(output_dir / "phase232_side_flip_control_summary.csv", index=False)
    random_controls.to_csv(output_dir / "phase232_random_side_control_summary.csv", index=False)
    gates.to_csv(output_dir / "phase232_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase232_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Candidate Validation Summary": validation,
            "Cost Stress Summary": stress,
            "Side Flip Controls": flips,
            "Random Side Control Sample": random_controls.head(30),
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase232_validate_phase231_candidates",
        **reproducibility_fields(
            artifact_id="phase232",
            generated_utc=generated_utc,
            inputs={
                "phase231_acceptance_summary": str(phase231_dir / "phase231_acceptance_summary.csv"),
                "phase231_candidate_summary": str(phase231_dir / "phase231_candidate_summary.csv"),
                "phase231_trade_ledger": str(phase231_dir / "phase231_trade_ledger.csv"),
            },
            parameters={
                "cost_stress_multipliers": COST_STRESS_MULTIPLIERS,
                "random_side_control_seeds": CONTROL_SEEDS,
                "test_random_side_required_beat_fraction": 0.95,
                "test_max_month_contribution_abs": 0.65,
                "test_max_symbol_contribution_abs": 0.65,
                "strategy_promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "candidate_validation_summary": str(output_dir / "phase232_candidate_validation_summary.csv"),
                "cost_stress_summary": str(output_dir / "phase232_cost_stress_summary.csv"),
                "side_flip_control_summary": str(output_dir / "phase232_side_flip_control_summary.csv"),
                "random_side_control_summary": str(output_dir / "phase232_random_side_control_summary.csv"),
                "gate_evaluation": str(output_dir / "phase232_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase232_acceptance_summary.csv"),
                "report": str(output_dir / "phase232_validate_phase231_candidates_report.md"),
                "manifest": str(output_dir / "phase232_validate_phase231_candidates_manifest.json"),
            },
            random_seed="deterministic_hash_random_side_controls_seeds_1_to_100",
            scenario_ids="phase231_synthetic_candidate_validation",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase231_event_bar_horizon_cost_floor_validation",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase232_validate_phase231_candidates_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Phase231 synthetic candidates with holdout and negative controls.")
    parser.add_argument("--phase231-dir", type=Path, default=DEFAULT_PHASE231_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase232(args.phase231_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
