from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase119")
DEFAULT_PHASE66_DIR = Path("outputs/phase66")
DEFAULT_PHASE68_DIR = Path("outputs/phase68")
DEFAULT_PHASE69_DIR = Path("outputs/phase69")
DEFAULT_PHASE118_DIR = Path("outputs/phase118")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def read_metric_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["metric", "value", "description"])
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    value = rows.iloc[0]
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    return int(round(as_float(value, float(default))))


def normalize_bool(frame: pd.DataFrame, column: str) -> pd.Series:
    if frame.empty or column not in frame.columns:
        return pd.Series(dtype=bool)
    return frame[column].astype(str).str.lower().isin(["true", "1", "yes"])


def build_joined_label_candidates(phase66: pd.DataFrame, phase68: pd.DataFrame, phase69: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "candidate_id",
        "feature_family_id",
        "base_strategy_id",
        "side",
        "spread_bucket",
        "imbalance_bucket",
        "replenishment_bucket",
        "spread_transition_type",
        "recent_return_bucket",
        "symbols",
        "trade_dates",
        "inferred_touches",
        "signal_rows",
        "baseline_adverse_selection_rate",
        "replenishment_adverse_selection_rate",
        "spread_adverse_direction_rate",
        "mean_replenishment_ratio",
        "mean_spread_change_bps",
        "mean_abs_recent_return_bps",
        "label_quality_score",
        "adverse_selection_gate",
        "replenishment_gate",
        "spread_confirmation_gate",
        "breadth_gate",
        "p118_pre_replay_candidate",
        "failure_reason",
    ]
    if phase66.empty or phase68.empty or phase69.empty:
        return pd.DataFrame(columns=columns)

    p66 = phase66.copy()
    p68 = phase68.copy()
    p69 = phase69.copy()
    for frame in [p66, p68, p69]:
        for column in ["side", "symbols", "trade_dates"]:
            if column in frame.columns:
                frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0)

    base = p68.merge(
        p66[
            [
                "side",
                "spread_bucket",
                "imbalance_bucket",
                "symbols",
                "trade_dates",
                "inferred_touches",
                "mean_adverse_selection_rate",
                "mean_abs_l1_imbalance",
                "touch_rate",
            ]
        ].rename(
            columns={
                "symbols": "baseline_symbols",
                "trade_dates": "baseline_trade_dates",
                "inferred_touches": "baseline_inferred_touches",
                "mean_adverse_selection_rate": "baseline_adverse_selection_rate",
            }
        ),
        on=["side", "spread_bucket", "imbalance_bucket"],
        how="left",
    )
    joined = base.merge(
        p69[
            [
                "side",
                "transition_type",
                "spread_bucket",
                "recent_return_bucket",
                "symbols",
                "trade_dates",
                "signal_rows",
                "mean_adverse_direction_rate",
                "mean_spread_change_bps",
                "mean_abs_recent_return_bps",
            ]
        ].rename(
            columns={
                "transition_type": "spread_transition_type",
                "symbols": "spread_symbols",
                "trade_dates": "spread_trade_dates",
                "mean_adverse_direction_rate": "spread_adverse_direction_rate",
            }
        ),
        on=["side", "spread_bucket"],
        how="left",
    )
    if joined.empty:
        return pd.DataFrame(columns=columns)

    joined["baseline_adverse_selection_rate"] = pd.to_numeric(
        joined["baseline_adverse_selection_rate"], errors="coerce"
    ).fillna(1.0)
    joined["replenishment_adverse_selection_rate"] = pd.to_numeric(
        joined["mean_adverse_selection_rate"], errors="coerce"
    ).fillna(1.0)
    joined["spread_adverse_direction_rate"] = pd.to_numeric(joined["spread_adverse_direction_rate"], errors="coerce").fillna(1.0)
    joined["mean_replenishment_ratio"] = pd.to_numeric(joined["mean_replenishment_ratio"], errors="coerce").fillna(0.0)
    joined["mean_spread_change_bps"] = pd.to_numeric(joined["mean_spread_change_bps"], errors="coerce").fillna(0.0)
    joined["mean_abs_recent_return_bps"] = pd.to_numeric(joined["mean_abs_recent_return_bps"], errors="coerce").fillna(0.0)
    joined["symbols"] = joined[["symbols", "baseline_symbols", "spread_symbols"]].apply(
        lambda row: int(pd.to_numeric(row, errors="coerce").fillna(0).min()), axis=1
    )
    joined["trade_dates"] = joined[["trade_dates", "baseline_trade_dates", "spread_trade_dates"]].apply(
        lambda row: int(pd.to_numeric(row, errors="coerce").fillna(0).min()), axis=1
    )
    joined["inferred_touches"] = pd.to_numeric(joined["inferred_touches"], errors="coerce").fillna(0).astype(int)
    joined["signal_rows"] = pd.to_numeric(joined["signal_rows"], errors="coerce").fillna(0).astype(int)
    joined["adverse_selection_gate"] = (
        (joined["baseline_adverse_selection_rate"] <= 0.45)
        & (joined["replenishment_adverse_selection_rate"] <= 0.45)
        & (joined["spread_adverse_direction_rate"] <= 0.45)
    )
    joined["replenishment_gate"] = joined["mean_replenishment_ratio"] >= 1.0
    joined["spread_confirmation_gate"] = (
        joined["spread_transition_type"].astype(str).eq("compression")
        & (joined["mean_spread_change_bps"] <= 0.0)
    )
    joined["breadth_gate"] = (joined["symbols"] >= 20) & (joined["trade_dates"] >= 4)
    joined["p118_pre_replay_candidate"] = (
        joined["adverse_selection_gate"]
        & joined["replenishment_gate"]
        & joined["spread_confirmation_gate"]
        & joined["breadth_gate"]
    )
    joined["feature_family_id"] = "P118_RICHER_PASSIVE_LABEL_COMPOSITE"
    joined["base_strategy_id"] = joined["strategy_id"]
    joined["candidate_id"] = (
        joined["feature_family_id"].astype(str)
        + "__"
        + joined["base_strategy_id"].astype(str)
        + "__S"
        + joined["side"].astype(int).astype(str)
        + "__"
        + joined["spread_bucket"].astype(str)
        + "__"
        + joined["imbalance_bucket"].astype(str)
        + "__"
        + joined["replenishment_bucket"].astype(str)
        + "__"
        + joined["spread_transition_type"].astype(str)
        + "__"
        + joined["recent_return_bucket"].astype(str)
    )
    joined["label_quality_score"] = (
        (1.0 - joined[["baseline_adverse_selection_rate", "replenishment_adverse_selection_rate", "spread_adverse_direction_rate"]].max(axis=1))
        + joined["mean_replenishment_ratio"].clip(upper=2.0) / 2.0
        + joined["spread_confirmation_gate"].astype(float)
        + joined["breadth_gate"].astype(float)
    )
    failure_parts = []
    for _, row in joined.iterrows():
        reasons: list[str] = []
        if not bool(row["adverse_selection_gate"]):
            reasons.append("adverse_selection_gate_failed")
        if not bool(row["replenishment_gate"]):
            reasons.append("replenishment_gate_failed")
        if not bool(row["spread_confirmation_gate"]):
            reasons.append("spread_confirmation_gate_failed")
        if not bool(row["breadth_gate"]):
            reasons.append("breadth_gate_failed")
        failure_parts.append("|".join(reasons) if reasons else "passes_pre_replay_label_gate")
    joined["failure_reason"] = failure_parts
    return joined[columns].sort_values(
        ["p118_pre_replay_candidate", "label_quality_score", "symbols", "inferred_touches"],
        ascending=[False, False, False, False],
        kind="mergesort",
    )


def build_family_summary(candidates: pd.DataFrame) -> pd.DataFrame:
    if candidates.empty:
        return pd.DataFrame(
            [
                {
                    "feature_family_id": "P118_RICHER_PASSIVE_LABEL_COMPOSITE",
                    "candidate_rows": 0,
                    "pre_replay_candidate_rows": 0,
                    "best_label_quality_score": 0.0,
                    "max_symbols": 0,
                    "max_trade_dates": 0,
                    "dominant_failure_reason": "no_joined_label_candidates",
                }
            ]
        )
    grouped = candidates.groupby("feature_family_id", sort=True)
    rows = []
    for family_id, group in grouped:
        failure_counts = group["failure_reason"].astype(str).value_counts()
        rows.append(
            {
                "feature_family_id": family_id,
                "candidate_rows": int(len(group)),
                "pre_replay_candidate_rows": int(group["p118_pre_replay_candidate"].astype(bool).sum()),
                "best_label_quality_score": float(pd.to_numeric(group["label_quality_score"], errors="coerce").fillna(0).max()),
                "max_symbols": int(pd.to_numeric(group["symbols"], errors="coerce").fillna(0).max()),
                "max_trade_dates": int(pd.to_numeric(group["trade_dates"], errors="coerce").fillna(0).max()),
                "dominant_failure_reason": str(failure_counts.index[0]) if not failure_counts.empty else "",
            }
        )
    return pd.DataFrame(rows)


def build_gate_evaluation(candidates: pd.DataFrame) -> pd.DataFrame:
    if candidates.empty:
        adverse = replenish = spread = breadth = all_pass = 0
    else:
        adverse = int(candidates["adverse_selection_gate"].astype(bool).sum())
        replenish = int(candidates["replenishment_gate"].astype(bool).sum())
        spread = int(candidates["spread_confirmation_gate"].astype(bool).sum())
        breadth = int(candidates["breadth_gate"].astype(bool).sum())
        all_pass = int(candidates["p118_pre_replay_candidate"].astype(bool).sum())
    return pd.DataFrame(
        [
            {
                "gate_id": "P119_ADVERSE_SELECTION_CEILING",
                "candidate_rows_passing": adverse,
                "gate_pass": int(adverse > 0),
                "requirement": "All joined label components must have adverse-selection/direction rate <= 0.45.",
            },
            {
                "gate_id": "P119_REPLENISHMENT_CONFIRMATION",
                "candidate_rows_passing": replenish,
                "gate_pass": int(replenish > 0),
                "requirement": "Mean same-side post-touch replenishment ratio must be >= 1.0.",
            },
            {
                "gate_id": "P119_SPREAD_CONFIRMATION",
                "candidate_rows_passing": spread,
                "gate_pass": int(spread > 0),
                "requirement": "Matched spread-transition context must be compression/non-expansion.",
            },
            {
                "gate_id": "P119_BREADTH_BEFORE_REPLAY",
                "candidate_rows_passing": breadth,
                "gate_pass": int(breadth > 0),
                "requirement": "Joined labels must span at least 20 symbols and 4 trade dates.",
            },
            {
                "gate_id": "P119_PRE_REPLAY_LABEL_GATE",
                "candidate_rows_passing": all_pass,
                "gate_pass": int(all_pass > 0),
                "requirement": "At least one candidate must pass all Phase118-derived pre-replay gates.",
            },
        ]
    )


def build_acceptance_summary(candidates: pd.DataFrame, family_summary: pd.DataFrame, gate_eval: pd.DataFrame, phase118: pd.DataFrame) -> pd.DataFrame:
    candidate_rows = int(len(candidates))
    pre_replay_rows = int(candidates["p118_pre_replay_candidate"].astype(bool).sum()) if not candidates.empty else 0
    max_symbols = int(family_summary["max_symbols"].max()) if not family_summary.empty else 0
    max_trade_dates = int(family_summary["max_trade_dates"].max()) if not family_summary.empty else 0
    phase118_pilot_allowed = as_int(metric_value(phase118, "phase118_bounded_pilot_replay_allowed"))
    return pd.DataFrame(
        [
            ("phase119_joined_label_candidate_rows", candidate_rows, "Richer passive joined label candidates constructed from Phase66/68/69 labels"),
            ("phase119_pre_replay_candidate_rows", pre_replay_rows, "Joined candidates passing all pre-replay label gates"),
            ("phase119_max_candidate_symbols", max_symbols, "Maximum symbols covered by a joined candidate"),
            ("phase119_max_candidate_trade_dates", max_trade_dates, "Maximum trade dates covered by a joined candidate"),
            ("phase119_gate_rows", int(len(gate_eval)), "Gate evaluations emitted"),
            ("phase119_all_gates_pass", int(gate_eval["gate_pass"].astype(bool).all()) if not gate_eval.empty else 0, "1 means every Phase119 gate has at least one passing row"),
            ("phase119_phase118_pilot_replay_allowed_input", phase118_pilot_allowed, "Inherited Phase118 bounded replay permission"),
            ("phase119_bounded_pilot_replay_allowed", 1 if pre_replay_rows > 0 and phase118_pilot_allowed else 0, "Bounded replay remains closed unless Phase118 and Phase119 both allow it"),
            ("phase119_full_year_replay_allowed", 0, "Full-year replay remains closed"),
            ("phase119_next_best_action", "collect_more_label_coverage_or_redesign_passive_features_no_replay", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase119 Richer Passive Label Builder",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase119 joins the prior passive adverse-selection, replenishment and spread-transition labels into richer passive label candidates.",
        "It remains pre-replay: candidates are filtered by label feasibility and breadth, not by replay P&L.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase119_richer_passive_label_builder_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase119(
    base_dir: Path,
    output_dir: Path,
    phase66_dir: Path,
    phase68_dir: Path,
    phase69_dir: Path,
    phase118_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase66 = read_csv(base_dir / phase66_dir / "passive_label_bucket_rollup.csv")
    phase68 = read_csv(base_dir / phase68_dir / "replenishment_bucket_rollup.csv")
    phase69 = read_csv(base_dir / phase69_dir / "spread_transition_bucket_rollup.csv")
    phase118 = read_metric_table(base_dir / phase118_dir / "phase118_richer_passive_precommit_acceptance_summary.csv")
    candidates = build_joined_label_candidates(phase66, phase68, phase69)
    family_summary = build_family_summary(candidates)
    gate_eval = build_gate_evaluation(candidates)
    acceptance = build_acceptance_summary(candidates, family_summary, gate_eval, phase118)

    candidates.to_csv(output_dir / "richer_passive_joined_label_candidates.csv", index=False)
    family_summary.to_csv(output_dir / "richer_passive_label_family_summary.csv", index=False)
    gate_eval.to_csv(output_dir / "richer_passive_pre_replay_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase119_richer_passive_label_builder_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Richer Passive Label Family Summary": family_summary,
            "Pre-Replay Gate Evaluation": gate_eval,
            "Joined Label Candidates": candidates.head(50),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase119_richer_passive_label_builder",
        "pre_replay_candidate_rows": int(
            acceptance.loc[acceptance["metric"].eq("phase119_pre_replay_candidate_rows"), "value"].iloc[0]
        ),
        "bounded_pilot_replay_allowed": int(
            acceptance.loc[acceptance["metric"].eq("phase119_bounded_pilot_replay_allowed"), "value"].iloc[0]
        ),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase119",
            generated_utc=generated_utc,
            inputs={
                "phase66_bucket_rollup": str(phase66_dir / "passive_label_bucket_rollup.csv"),
                "phase68_bucket_rollup": str(phase68_dir / "replenishment_bucket_rollup.csv"),
                "phase69_bucket_rollup": str(phase69_dir / "spread_transition_bucket_rollup.csv"),
                "phase118_acceptance": str(phase118_dir / "phase118_richer_passive_precommit_acceptance_summary.csv"),
            },
            parameters={
                "selection_policy": "label_feasibility_only_no_replay_pnl",
                "adverse_selection_rate_max": 0.45,
                "replenishment_ratio_min": 1.0,
                "symbols_min": 20,
                "trade_dates_min": 4,
            },
            outputs={
                "joined_label_candidates": str(output_dir / "richer_passive_joined_label_candidates.csv"),
                "family_summary": str(output_dir / "richer_passive_label_family_summary.csv"),
                "gate_evaluation": str(output_dir / "richer_passive_pre_replay_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase119_richer_passive_label_builder_acceptance_summary.csv"),
                "report": str(output_dir / "phase119_richer_passive_label_builder_report.md"),
                "manifest": str(output_dir / "phase119_richer_passive_label_builder_manifest.json"),
            },
            random_seed="none_deterministic_label_join",
            scenario_ids="phase119_richer_passive_pre_replay_label_builder",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_label_builder",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase119_richer_passive_label_builder_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase119 richer passive pre-replay label candidates.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--phase66-dir", type=Path, default=DEFAULT_PHASE66_DIR)
    parser.add_argument("--phase68-dir", type=Path, default=DEFAULT_PHASE68_DIR)
    parser.add_argument("--phase69-dir", type=Path, default=DEFAULT_PHASE69_DIR)
    parser.add_argument("--phase118-dir", type=Path, default=DEFAULT_PHASE118_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase119(
        base_dir=args.base_dir,
        output_dir=args.output_dir,
        phase66_dir=args.phase66_dir,
        phase68_dir=args.phase68_dir,
        phase69_dir=args.phase69_dir,
        phase118_dir=args.phase118_dir,
    )


if __name__ == "__main__":
    main()
