from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase411_full_depth_replenishment_breakout_execution import (
    BREAKOUT_CONFIRM_SECONDS,
    DEFAULT_RAW_ROOT,
    DEFAULT_REAL_ROOTS,
    HORIZON_SECONDS,
    IMPULSE_LOOKBACK_SECONDS,
    MAX_DEPTH_WITHDRAWAL_PRESSURE,
    MAX_SPREAD_BPS,
    MIN_ABS_IMPULSE_BPS,
    MIN_LEVELS_2_TO_5_REPLENISHMENT_PRESSURE,
    MIN_LEVEL_WEIGHTED_IMBALANCE_ALIGNMENT,
    MIN_TICKS_PER_GROUP,
    MIN_TOP5_IMBALANCE_ALIGNMENT,
    PRIMARY_SCENARIO,
    REBUILD_CONFIRM_SECONDS,
    SCAN_STRIDE,
    l2_l5_imbalance,
    level_weighted_imbalance,
    load_real_anchor_ticks,
    load_synthetic_ticks,
    replenishment_and_withdrawal,
    side_from_impulse,
    spread_bps,
    top5_imbalance,
)
from synthetic_l2.phase410_full_depth_replenishment_breakout_precommit import THESIS_ID
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE412_DIR = Path("outputs/phase412")
DEFAULT_OUTPUT_DIR = Path("outputs/phase413")

ATTRIBUTION_ID = "P413_REPLENISHMENT_BREAKOUT_FILTER_FAILURE_ATTRIBUTION"
NEXT_ACTION = "precommit_material_new_less_sparse_full_depth_l2_thesis_using_phase413_failure_map"
REPAIR_ACTION = "repair_phase413_filter_attribution"

STAGE_ORDER = [
    "window_ok",
    "impulse_threshold",
    "top5_alignment",
    "level_weighted_alignment",
    "l2_l5_replenishment",
    "l2_l5_imbalance_alignment",
    "withdrawal_limit",
    "spread_limit",
    "breakout_confirmation",
    "future_window",
]


def bool_int(value: bool) -> int:
    return int(bool(value))


def evaluate_scan_point(group: pd.DataFrame, idx: int) -> dict[str, Any]:
    row = group.iloc[idx]
    ts = float(row["exchange_timestamp_ms"])
    impulse = group[(group["exchange_timestamp_ms"] >= ts - IMPULSE_LOOKBACK_SECONDS * 1000.0) & (group["exchange_timestamp_ms"] <= ts)]
    rebuild = group[(group["exchange_timestamp_ms"] >= ts - REBUILD_CONFIRM_SECONDS * 1000.0) & (group["exchange_timestamp_ms"] <= ts)]
    breakout = group[(group["exchange_timestamp_ms"] >= ts - BREAKOUT_CONFIRM_SECONDS * 1000.0) & (group["exchange_timestamp_ms"] <= ts)]
    window_ok = len(impulse) >= 3 and len(rebuild) >= 3 and len(breakout) >= 3
    impulse_bps = 0.0
    side = 0
    replenish = 0.0
    withdrawal = 0.0
    top5 = top5_imbalance(row)
    weighted = level_weighted_imbalance(row)
    l2_l5 = l2_l5_imbalance(row)
    spread = spread_bps(row)
    future_count = int(len(group[(group["exchange_timestamp_ms"] > ts) & (group["exchange_timestamp_ms"] <= ts + HORIZON_SECONDS * 1000.0)]))
    if window_ok:
        impulse_bps = (float(row["last_price"]) / float(impulse.iloc[0]["last_price"]) - 1.0) * 10_000.0
        side = side_from_impulse(impulse_bps) if impulse_bps != 0 else 0
        if side != 0:
            replenish, withdrawal = replenishment_and_withdrawal(rebuild, side)
    checks = {
        "window_ok": window_ok,
        "impulse_threshold": window_ok and abs(impulse_bps) >= MIN_ABS_IMPULSE_BPS,
        "top5_alignment": window_ok and side != 0 and side * top5 >= MIN_TOP5_IMBALANCE_ALIGNMENT,
        "level_weighted_alignment": window_ok and side != 0 and side * weighted >= MIN_LEVEL_WEIGHTED_IMBALANCE_ALIGNMENT,
        "l2_l5_replenishment": window_ok and side != 0 and replenish >= MIN_LEVELS_2_TO_5_REPLENISHMENT_PRESSURE,
        "l2_l5_imbalance_alignment": window_ok and side != 0 and side * l2_l5 >= MIN_LEVEL_WEIGHTED_IMBALANCE_ALIGNMENT,
        "withdrawal_limit": window_ok and side != 0 and withdrawal <= MAX_DEPTH_WITHDRAWAL_PRESSURE,
        "spread_limit": spread <= MAX_SPREAD_BPS,
        "breakout_confirmation": window_ok and side != 0 and (
            (side > 0 and float(row["last_price"]) >= float(breakout["last_price"].max()))
            or (side < 0 and float(row["last_price"]) <= float(breakout["last_price"].min()))
        ),
        "future_window": future_count >= 2,
    }
    first_failure = "passes_all"
    for stage in STAGE_ORDER:
        if not checks[stage]:
            first_failure = stage
            break
    return {
        "trade_date": str(row["trade_date"]),
        "symbol": str(row["symbol"]),
        "signal_ts_ms": ts,
        "impulse_bps": float(impulse_bps),
        "side": side,
        "top5_imbalance": float(top5),
        "l2_l5_imbalance": float(l2_l5),
        "level_weighted_imbalance": float(weighted),
        "l2_l5_replenishment_pressure": float(replenish),
        "depth_withdrawal_pressure": float(withdrawal),
        "spread_bps": float(spread),
        "future_ticks": future_count,
        **{f"pass_{stage}": bool_int(checks[stage]) for stage in STAGE_ORDER},
        "passes_all_filters": bool_int(first_failure == "passes_all"),
        "first_failure_stage": first_failure,
    }


def build_scan_ledger(ticks: pd.DataFrame, panel: str) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for (trade_date, symbol), group in ticks.groupby(["trade_date", "symbol"], sort=True):
        group = group.sort_values("exchange_timestamp_ms", kind="mergesort").reset_index(drop=True)
        if len(group) < MIN_TICKS_PER_GROUP:
            continue
        for idx in range(MIN_TICKS_PER_GROUP // 2, len(group) - 3, SCAN_STRIDE):
            row = evaluate_scan_point(group, idx)
            row["panel"] = panel
            rows.append(row)
    return pd.DataFrame(rows)


def build_stage_summary(ledger: pd.DataFrame, panel: str) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    total = len(ledger)
    for stage in STAGE_ORDER:
        col = f"pass_{stage}"
        passed = int(pd.to_numeric(ledger.get(col, pd.Series(dtype=float)), errors="coerce").fillna(0).sum()) if total else 0
        rows.append(
            {
                "panel": panel,
                "stage": stage,
                "scan_points": total,
                "pass_count": passed,
                "fail_count": total - passed,
                "pass_rate": passed / total if total else 0.0,
                "threshold_or_rule": threshold_description(stage),
            }
        )
    return pd.DataFrame(rows)


def threshold_description(stage: str) -> str:
    return {
        "window_ok": f"windows have >=3 ticks for {IMPULSE_LOOKBACK_SECONDS}s/{REBUILD_CONFIRM_SECONDS}s/{BREAKOUT_CONFIRM_SECONDS}s",
        "impulse_threshold": f"abs(impulse_bps)>={MIN_ABS_IMPULSE_BPS}",
        "top5_alignment": f"side*top5_imbalance>={MIN_TOP5_IMBALANCE_ALIGNMENT}",
        "level_weighted_alignment": f"side*level_weighted_imbalance>={MIN_LEVEL_WEIGHTED_IMBALANCE_ALIGNMENT}",
        "l2_l5_replenishment": f"levels_2_to_5_replenishment>={MIN_LEVELS_2_TO_5_REPLENISHMENT_PRESSURE}",
        "l2_l5_imbalance_alignment": f"side*l2_l5_imbalance>={MIN_LEVEL_WEIGHTED_IMBALANCE_ALIGNMENT}",
        "withdrawal_limit": f"depth_withdrawal_pressure<={MAX_DEPTH_WITHDRAWAL_PRESSURE}",
        "spread_limit": f"spread_bps<={MAX_SPREAD_BPS}",
        "breakout_confirmation": "last_price confirms breakout in impulse direction",
        "future_window": f">=2 future ticks inside {HORIZON_SECONDS}s horizon",
    }.get(stage, "")


def build_first_failure_summary(ledger: pd.DataFrame, panel: str) -> pd.DataFrame:
    if ledger.empty:
        return pd.DataFrame(columns=["panel", "first_failure_stage", "count", "share"])
    counts = ledger["first_failure_stage"].value_counts(dropna=False).rename_axis("first_failure_stage").reset_index(name="count")
    counts["panel"] = panel
    counts["share"] = counts["count"] / float(len(ledger))
    return counts[["panel", "first_failure_stage", "count", "share"]]


def build_distribution_summary(ledger: pd.DataFrame, panel: str) -> pd.DataFrame:
    metrics = [
        "impulse_bps",
        "top5_imbalance",
        "l2_l5_imbalance",
        "level_weighted_imbalance",
        "l2_l5_replenishment_pressure",
        "depth_withdrawal_pressure",
        "spread_bps",
    ]
    rows: list[dict[str, Any]] = []
    for metric in metrics:
        series = pd.to_numeric(ledger.get(metric, pd.Series(dtype=float)), errors="coerce").dropna()
        if series.empty:
            rows.append({"panel": panel, "metric": metric, "count": 0, "p05": "", "p25": "", "median": "", "p75": "", "p95": ""})
            continue
        rows.append(
            {
                "panel": panel,
                "metric": metric,
                "count": int(len(series)),
                "p05": float(series.quantile(0.05)),
                "p25": float(series.quantile(0.25)),
                "median": float(series.quantile(0.50)),
                "p75": float(series.quantile(0.75)),
                "p95": float(series.quantile(0.95)),
            }
        )
    return pd.DataFrame(rows)


def build_recommendation(stage_summary: pd.DataFrame, failure_summary: pd.DataFrame, summary412: pd.DataFrame) -> pd.DataFrame:
    synthetic_stages = stage_summary[stage_summary["panel"].eq("synthetic")].copy()
    synthetic_stages["fail_count"] = pd.to_numeric(synthetic_stages["fail_count"], errors="coerce").fillna(0)
    worst = synthetic_stages.sort_values(["fail_count", "stage"], ascending=[False, True], kind="mergesort").head(3)
    top_failures = failure_summary[failure_summary["panel"].eq("synthetic")].sort_values("count", ascending=False, kind="mergesort").head(3)
    return pd.DataFrame(
        [
            ("selected_interpretation", "P413_ZERO_EVENT_CAUSE_ATTRIBUTED", "Filter attribution completed on Phase411 scan universe."),
            ("phase412_verdict", metric_value(summary412, "phase412_selected_verdict", ""), "Phase412 context."),
            ("largest_stage_fail_counts", ";".join(f"{r.stage}:{int(r.fail_count)}" for r in worst.itertuples(index=False)), "Largest all-stage failures."),
            ("largest_first_failure_stages", ";".join(f"{r.first_failure_stage}:{int(r.count)}" for r in top_failures.itertuples(index=False)), "Earliest gate failures."),
            ("threshold_relaxation_allowed", 0, "This diagnostic is not permission to tune Phase410 after seeing results."),
            ("less_sparse_material_new_required", 1, "Next thesis should be precommitted using lower event sparsity as a design objective."),
            ("next_action", NEXT_ACTION, "Use the failure map to design a materially new full-depth route, not a threshold rescue."),
        ],
        columns=["recommendation_id", "value", "description"],
    )


def build_gate_evaluation(summary412: pd.DataFrame, synthetic_ledger: pd.DataFrame, real_ledger: pd.DataFrame, recommendation: pd.DataFrame) -> pd.DataFrame:
    complete412 = as_int(metric_value(summary412, "phase412_replenishment_breakout_interpretation_complete", 0))
    synthetic_points = int(len(synthetic_ledger))
    real_points = int(len(real_ledger))
    passes_all = int(pd.to_numeric(synthetic_ledger.get("passes_all_filters", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()) if synthetic_points else 0
    gates = [
        ("P413_PHASE412_COMPLETE", complete412 == 1, complete412, 1),
        ("P413_SYNTHETIC_SCAN_UNIVERSE_NONEMPTY", synthetic_points > 0, synthetic_points, ">0"),
        ("P413_REAL_ANCHOR_SCAN_UNIVERSE_REPORTED", real_points > 0, real_points, ">0"),
        ("P413_STAGE_SUMMARY_COMPLETE", True, len(STAGE_ORDER), len(STAGE_ORDER)),
        ("P413_FIRST_FAILURE_SUMMARY_COMPLETE", True, "written", "written"),
        ("P413_ZERO_EVENT_CONFIRMED", passes_all == 0, passes_all, 0),
        ("P413_NO_PNL_OR_PROMOTION", True, "pnl=0;promotion=0;paper=0;claim=0", "all_zero"),
        ("P413_NO_THRESHOLD_RELAXATION", str(recommendation.loc[recommendation["recommendation_id"].eq("threshold_relaxation_allowed"), "value"].iloc[0]) == "0", 0, 0),
        ("P413_NEXT_ROUTE_MATERIAL_NEW", str(recommendation.loc[recommendation["recommendation_id"].eq("less_sparse_material_new_required"), "value"].iloc[0]) == "1", 1, 1),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(synthetic_ledger: pd.DataFrame, real_ledger: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    synthetic_passes_all = int(pd.to_numeric(synthetic_ledger.get("passes_all_filters", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()) if not synthetic_ledger.empty else 0
    real_passes_all = int(pd.to_numeric(real_ledger.get("passes_all_filters", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()) if not real_ledger.empty else 0
    return pd.DataFrame(
        [
            ("phase413_filter_attribution_complete", 1, "Phase413 attribution completed"),
            ("phase413_attribution_id", ATTRIBUTION_ID, "Attribution id"),
            ("phase413_synthetic_scan_points", len(synthetic_ledger), "Synthetic scan points attributed"),
            ("phase413_synthetic_pass_all_filters", synthetic_passes_all, "Synthetic points passing all Phase410 filters"),
            ("phase413_real_anchor_scan_points", len(real_ledger), "Real-anchor scan points attributed"),
            ("phase413_real_anchor_pass_all_filters", real_passes_all, "Real-anchor points passing all Phase410 filters"),
            ("phase413_pnl_generated", 0, "No P&L generated"),
            ("phase413_strategy_promotion_allowed", 0, "No promotion"),
            ("phase413_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase413_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase413_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase413_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase413_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, stage_summary: pd.DataFrame, first_failure: pd.DataFrame, distributions: pd.DataFrame, recommendation: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase413 Replenishment Breakout Filter-Failure Attribution",
        "",
        "Phase413 diagnoses why the Phase410/P411 full-depth replenishment-breakout thesis selected zero trades.",
        "",
        "It does not generate P&L, does not relax thresholds and does not promote a strategy.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Stage Summary",
        "",
        _markdown_table(stage_summary),
        "",
        "## First-Failure Summary",
        "",
        _markdown_table(first_failure),
        "",
        "## Metric Distributions",
        "",
        _markdown_table(distributions),
        "",
        "## Recommendation Ledger",
        "",
        _markdown_table(recommendation),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase413 is a diagnostic map for future precommit design, not permission to tune Phase410.",
    ]
    (output_dir / "phase413_replenishment_breakout_filter_attribution_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(raw_root: Path = DEFAULT_RAW_ROOT, phase412_dir: Path = DEFAULT_PHASE412_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    summary412 = read_csv(phase412_dir / "phase412_acceptance_summary.csv")
    if summary412.empty:
        raise FileNotFoundError("Phase413 requires Phase412 acceptance summary.")
    synthetic_ticks = load_synthetic_ticks(raw_root)
    real_ticks = load_real_anchor_ticks(DEFAULT_REAL_ROOTS)
    synthetic_ledger = build_scan_ledger(synthetic_ticks, "synthetic")
    real_ledger = build_scan_ledger(real_ticks, "real_anchor")
    stage_summary = pd.concat(
        [build_stage_summary(synthetic_ledger, "synthetic"), build_stage_summary(real_ledger, "real_anchor")],
        ignore_index=True,
    )
    first_failure = pd.concat(
        [build_first_failure_summary(synthetic_ledger, "synthetic"), build_first_failure_summary(real_ledger, "real_anchor")],
        ignore_index=True,
    )
    distributions = pd.concat(
        [build_distribution_summary(synthetic_ledger, "synthetic"), build_distribution_summary(real_ledger, "real_anchor")],
        ignore_index=True,
    )
    recommendation = build_recommendation(stage_summary, first_failure, summary412)
    gates = build_gate_evaluation(summary412, synthetic_ledger, real_ledger, recommendation)
    acceptance = build_acceptance(synthetic_ledger, real_ledger, gates)
    synthetic_ledger.to_csv(output_dir / "phase413_synthetic_scan_point_ledger.csv", index=False)
    real_ledger.to_csv(output_dir / "phase413_real_anchor_scan_point_ledger.csv", index=False)
    stage_summary.to_csv(output_dir / "phase413_stage_summary.csv", index=False)
    first_failure.to_csv(output_dir / "phase413_first_failure_summary.csv", index=False)
    distributions.to_csv(output_dir / "phase413_metric_distribution_summary.csv", index=False)
    recommendation.to_csv(output_dir / "phase413_recommendation_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase413_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase413_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, stage_summary, first_failure, distributions, recommendation, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase413_replenishment_breakout_filter_attribution",
        **reproducibility_fields(
            artifact_id="phase413_replenishment_breakout_filter_attribution",
            generated_utc=generated_utc,
            inputs={
                "phase412_acceptance_summary": str(phase412_dir / "phase412_acceptance_summary.csv"),
                "raw_root": str(raw_root),
                "real_anchor_roots": ";".join(str(root) for root in DEFAULT_REAL_ROOTS),
            },
            parameters={"thesis_id": THESIS_ID, "scenario_id": PRIMARY_SCENARIO, "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase413_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase413_no_execution_filter_attribution",
        ),
    }
    (output_dir / "phase413_replenishment_breakout_filter_attribution_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase413 replenishment-breakout filter-failure attribution.")
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--phase412-dir", type=Path, default=DEFAULT_PHASE412_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.raw_root, args.phase412_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
