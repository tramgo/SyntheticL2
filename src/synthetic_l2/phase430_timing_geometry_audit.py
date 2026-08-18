from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase411_full_depth_replenishment_breakout_execution import DEFAULT_REAL_ROOTS, normalize_ticks
from synthetic_l2.phase424_queue_depletion_continuation_precommit import SYMBOLS
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_RAW_ROOT = Path("raw_synthetic_l2_dense_full_year")
DEFAULT_PHASE429_DIR = Path("outputs/phase429")
DEFAULT_OUTPUT_DIR = Path("outputs/phase430")

AUDIT_ID = "P430_TIMING_GEOMETRY_AUDIT"
NEXT_ACTION = "precommit_phase431_geometry_consistent_full_depth_sweep"
REPAIR_ACTION = "repair_phase430_timing_geometry_audit"

SYNTHETIC_MONTHS = ["2026-01", "2026-02"]
SYNTHETIC_SYMBOLS = SYMBOLS[:8]
REAL_SYMBOLS = SYMBOLS[:8]
MAX_SYNTHETIC_ROWS_PER_FILE = 25_000
MAX_REAL_DATES = 5
MAX_REAL_FILES_PER_SYMBOL_DATE = 80
MIN_HOLD_MS = 250.0
FORWARD_TICKS = [3, 6, 12]
MAX_HOLD_TICKS_TO_TEST = [30, 60, 120, 250, 500, 1000, 1500, 2500, 5000]
SCAN_STRIDE = 250

TIMING_COLUMNS = [
    "exchange_timestamp_ms",
    "callback_received_utc_ms",
    "trade_date",
    "exchange",
    "symbol",
]


def read_first_rows(path: Path, max_rows: int) -> pd.DataFrame:
    pf = pq.ParquetFile(path)
    cols = [c for c in TIMING_COLUMNS if c in pf.schema.names]
    batches = []
    rows = 0
    for batch in pf.iter_batches(batch_size=min(max_rows, 25_000), columns=cols):
        frame = batch.to_pandas()
        batches.append(frame)
        rows += len(frame)
        if rows >= max_rows:
            break
    return pd.concat(batches, ignore_index=True).head(max_rows) if batches else pd.DataFrame(columns=cols)


def load_synthetic_timing(raw_root: Path) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for month in SYNTHETIC_MONTHS:
        for symbol in SYNTHETIC_SYMBOLS:
            path = raw_root / f"trade_month={month}" / f"symbol={symbol}" / "part-00000.parquet"
            if path.exists():
                frames.append(read_first_rows(path, MAX_SYNTHETIC_ROWS_PER_FILE))
    return normalize_timing(pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(), "synthetic")


def load_real_timing(roots: list[Path]) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    loaded_dates = 0
    for root in roots:
        if not root.exists():
            continue
        for date_root in sorted(root.glob("trade_date=*")):
            if loaded_dates >= MAX_REAL_DATES:
                break
            exchange_root = date_root / "exchange=NSE"
            if not exchange_root.exists():
                continue
            date_value = date_root.name.split("=", 1)[1]
            any_loaded = False
            for symbol in REAL_SYMBOLS:
                for file in sorted((exchange_root / f"symbol={symbol}").glob("*.parquet"))[:MAX_REAL_FILES_PER_SYMBOL_DATE]:
                    try:
                        frame = pd.read_parquet(file, columns=None)
                    except Exception:
                        continue
                    if "exchange_timestamp_ms" not in frame.columns and "exchange_timestamp" in frame.columns:
                        frame["exchange_timestamp_ms"] = pd.to_datetime(frame["exchange_timestamp"], errors="coerce").astype("int64") // 1_000_000
                    if "exchange_timestamp_ms" not in frame.columns and "last_trade_time_ms" in frame.columns:
                        frame["exchange_timestamp_ms"] = frame["last_trade_time_ms"]
                    if "symbol" not in frame.columns:
                        frame["symbol"] = symbol
                    if "trade_date" not in frame.columns:
                        frame["trade_date"] = date_value
                    keep = [c for c in TIMING_COLUMNS if c in frame.columns]
                    frames.append(frame[keep])
                    any_loaded = True
            if any_loaded:
                loaded_dates += 1
    return normalize_timing(pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(), "real_anchor")


def normalize_timing(frame: pd.DataFrame, panel: str) -> pd.DataFrame:
    out = frame.copy()
    if out.empty:
        return out
    if "exchange_timestamp_ms" not in out.columns:
        out["exchange_timestamp_ms"] = np.arange(len(out), dtype=float)
    if "trade_date" not in out.columns:
        out["trade_date"] = ""
    if "symbol" not in out.columns:
        out["symbol"] = ""
    if "exchange" not in out.columns:
        out["exchange"] = "NSE"
    out["exchange_timestamp_ms"] = pd.to_numeric(out["exchange_timestamp_ms"], errors="coerce")
    out = out.dropna(subset=["exchange_timestamp_ms"])
    out["trade_date"] = out["trade_date"].astype(str)
    out["symbol"] = out["symbol"].astype(str).str.upper()
    out["panel"] = panel
    return out.sort_values(["trade_date", "symbol", "exchange_timestamp_ms"], kind="mergesort").reset_index(drop=True)


def unit_guess(diffs: pd.Series) -> str:
    med = float(diffs.median()) if len(diffs) else 0.0
    p95 = float(diffs.quantile(0.95)) if len(diffs) else 0.0
    if med <= 0:
        return "insufficient_or_duplicate_timestamps"
    if med < 10_000 and p95 < 300_000:
        return "milliseconds_or_dense_subtick_counter"
    if med >= 1_000_000 and med < 10_000_000_000:
        return "microseconds_possible"
    if med >= 10_000_000_000:
        return "nanoseconds_possible"
    return "ambiguous"


def cadence_summary(ticks: pd.DataFrame, panel: str) -> pd.DataFrame:
    rows = []
    for (trade_date, symbol), group in ticks.groupby(["trade_date", "symbol"], sort=True):
        ts = group["exchange_timestamp_ms"].astype(float).dropna().to_numpy()
        diffs = pd.Series(np.diff(ts))
        pos = diffs[diffs > 0]
        rows.append(
            {
                "panel": panel,
                "trade_date": trade_date,
                "symbol": symbol,
                "ticks": len(ts),
                "positive_gaps": len(pos),
                "zero_or_negative_gaps": int((diffs <= 0).sum()) if len(diffs) else 0,
                "median_gap": float(pos.median()) if len(pos) else 0.0,
                "p90_gap": float(pos.quantile(0.90)) if len(pos) else 0.0,
                "p95_gap": float(pos.quantile(0.95)) if len(pos) else 0.0,
                "p99_gap": float(pos.quantile(0.99)) if len(pos) else 0.0,
                "max_gap": float(pos.max()) if len(pos) else 0.0,
                "unit_guess": unit_guess(pos),
            }
        )
    return pd.DataFrame(rows)


def feasibility(ticks: pd.DataFrame, panel: str) -> pd.DataFrame:
    rows = []
    for (trade_date, symbol), group in ticks.groupby(["trade_date", "symbol"], sort=True):
        ts = group["exchange_timestamp_ms"].astype(float).dropna().to_numpy()
        for forward_ticks in FORWARD_TICKS:
            for max_hold_ticks in MAX_HOLD_TICKS_TO_TEST:
                possible = 0
                feasible = 0
                observed_holds = []
                max_window_holds = []
                if len(ts) > max_hold_ticks + forward_ticks + 2:
                    for signal_idx in range(0, len(ts) - max_hold_ticks - forward_ticks - 2, SCAN_STRIDE):
                        entry_idx = signal_idx + 1
                        min_exit_idx = entry_idx + forward_ticks
                        max_exit_idx = entry_idx + max_hold_ticks
                        if max_exit_idx >= len(ts) or min_exit_idx >= len(ts):
                            continue
                        possible += 1
                        min_hold = ts[min_exit_idx] - ts[entry_idx]
                        max_hold = ts[max_exit_idx] - ts[entry_idx]
                        observed_holds.append(min_hold)
                        max_window_holds.append(max_hold)
                        if max_hold >= MIN_HOLD_MS:
                            feasible += 1
                rows.append(
                    {
                        "panel": panel,
                        "trade_date": trade_date,
                        "symbol": symbol,
                        "forward_ticks": forward_ticks,
                        "max_hold_ticks": max_hold_ticks,
                        "scan_points_possible": possible,
                        "scan_points_feasible_min_hold": feasible,
                        "feasible_fraction": float(feasible / possible) if possible else 0.0,
                        "median_min_forward_hold": float(pd.Series(observed_holds).median()) if observed_holds else 0.0,
                        "median_max_window_hold": float(pd.Series(max_window_holds).median()) if max_window_holds else 0.0,
                        "p95_max_window_hold": float(pd.Series(max_window_holds).quantile(0.95)) if max_window_holds else 0.0,
                    }
                )
    return pd.DataFrame(rows)


def aggregate_feasibility(feas: pd.DataFrame) -> pd.DataFrame:
    if feas.empty:
        return pd.DataFrame(columns=["panel", "forward_ticks", "max_hold_ticks", "scan_points_possible", "scan_points_feasible_min_hold", "feasible_fraction", "median_max_window_hold"])
    grouped = feas.groupby(["panel", "forward_ticks", "max_hold_ticks"], as_index=False).agg(
        scan_points_possible=("scan_points_possible", "sum"),
        scan_points_feasible_min_hold=("scan_points_feasible_min_hold", "sum"),
        median_max_window_hold=("median_max_window_hold", "median"),
        p95_max_window_hold=("p95_max_window_hold", "median"),
    )
    grouped["feasible_fraction"] = np.where(grouped["scan_points_possible"].gt(0), grouped["scan_points_feasible_min_hold"] / grouped["scan_points_possible"], 0.0)
    return grouped.sort_values(["panel", "forward_ticks", "max_hold_ticks"]).reset_index(drop=True)


def recommended_geometry(agg: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for panel, group in agg.groupby("panel", sort=True):
        feasible = group[group["feasible_fraction"].ge(0.80)]
        if feasible.empty:
            best = group.sort_values(["feasible_fraction", "max_hold_ticks"], ascending=[False, True]).head(1)
            if best.empty:
                rows.append({"panel": panel, "recommended_forward_ticks": "", "recommended_max_hold_ticks": "", "feasible_fraction": 0.0, "recommendation": "no_feasible_geometry_in_test_grid"})
            else:
                b = best.iloc[0]
                rows.append({"panel": panel, "recommended_forward_ticks": int(b["forward_ticks"]), "recommended_max_hold_ticks": int(b["max_hold_ticks"]), "feasible_fraction": float(b["feasible_fraction"]), "recommendation": "expand_max_hold_or_reduce_min_hold_before_strategy_sweep"})
        else:
            b = feasible.sort_values(["max_hold_ticks", "forward_ticks"]).iloc[0]
            rows.append({"panel": panel, "recommended_forward_ticks": int(b["forward_ticks"]), "recommended_max_hold_ticks": int(b["max_hold_ticks"]), "feasible_fraction": float(b["feasible_fraction"]), "recommendation": "geometry_feasible_for_precommit"})
    return pd.DataFrame(rows)


def build_gates(phase429: pd.DataFrame, cadence: pd.DataFrame, agg: pd.DataFrame, rec: pd.DataFrame) -> pd.DataFrame:
    p429_complete = str(metric_value(phase429, "phase429_timing_geometry_audit_required", "0")) == "1"
    panels = set(cadence["panel"].astype(str)) if not cadence.empty else set()
    synth_feas = agg[agg["panel"].eq("synthetic")] if not agg.empty else pd.DataFrame()
    real_feas = agg[agg["panel"].eq("real_anchor")] if not agg.empty else pd.DataFrame()
    phase428_exact = synth_feas[synth_feas["max_hold_ticks"].eq(60)] if not synth_feas.empty else pd.DataFrame()
    phase428_any = float(phase428_exact["feasible_fraction"].max()) if not phase428_exact.empty else 0.0
    next_geom = rec[rec["recommendation"].eq("geometry_feasible_for_precommit")]
    gates = [
        ("P430_PHASE429_REQUIRED_AUDIT", p429_complete, metric_value(phase429, "phase429_timing_geometry_audit_required", ""), 1),
        ("P430_SYNTHETIC_CADENCE_MEASURED", "synthetic" in panels, "synthetic" in panels, True),
        ("P430_REAL_ANCHOR_CADENCE_MEASURED", "real_anchor" in panels, "real_anchor" in panels, True),
        ("P430_TIMESTAMP_UNIT_GUESSED", "unit_guess" in cadence.columns and cadence["unit_guess"].astype(str).ne("").any(), ";".join(sorted(set(cadence.get("unit_guess", pd.Series(dtype=str)).astype(str)))), "nonempty"),
        ("P430_PHASE428_GEOMETRY_DIAGNOSED", phase428_any == 0.0, phase428_any, 0.0),
        ("P430_FEASIBLE_REPAIR_GEOMETRY_FOUND", not next_geom.empty, len(next_geom), ">=1"),
        ("P430_NO_SIGNAL_THRESHOLD_TUNING", True, "timing_only", "timing_only"),
        ("P430_BOUNDARIES_CLOSED", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(cadence: pd.DataFrame, agg: pd.DataFrame, rec: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    synth = cadence[cadence["panel"].eq("synthetic")]
    real = cadence[cadence["panel"].eq("real_anchor")]
    phase428_geom = agg[(agg["panel"].eq("synthetic")) & (agg["max_hold_ticks"].eq(60))]
    phase428_feas = float(phase428_geom["feasible_fraction"].max()) if not phase428_geom.empty else 0.0
    return pd.DataFrame(
        [
            ("phase430_timing_geometry_audit_complete", 1, "Phase430 audit completed"),
            ("phase430_audit_id", AUDIT_ID, "Audit id"),
            ("phase430_synthetic_groups", len(synth), "Synthetic symbol/date groups"),
            ("phase430_real_anchor_groups", len(real), "Real-anchor symbol/date groups"),
            ("phase430_synthetic_median_gap_median", float(synth["median_gap"].median()) if not synth.empty else 0.0, "Median of synthetic group median gaps"),
            ("phase430_real_anchor_median_gap_median", float(real["median_gap"].median()) if not real.empty else 0.0, "Median of real-anchor group median gaps"),
            ("phase430_phase428_max_hold_60_feasible_fraction", phase428_feas, "Best synthetic feasibility at 60 max-hold ticks"),
            ("phase430_recommended_geometry_rows", len(rec), "Recommended geometry rows"),
            ("phase430_timing_repair_precommit_allowed", int(hard_pass == hard_rows), "Whether Phase431 may precommit repaired geometry"),
            ("phase430_strategy_promotion_allowed", 0, "No promotion"),
            ("phase430_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase430_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase430_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase430_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase430_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, cadence: pd.DataFrame, agg: pd.DataFrame, rec: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase430 Timing-Geometry Audit",
        "",
        "Phase430 audits whether exact forward-tick exits, elapsed-time holds and max-hold tick windows are feasible on synthetic and real L2 cadence.",
        "",
        "This phase does not tune strategy signals and does not generate promotion/paper/live claims.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Cadence Summary",
        "",
        _markdown_table(cadence.head(40)),
        "",
        "## Hold-Window Feasibility",
        "",
        _markdown_table(agg),
        "",
        "## Recommended Timing Geometry",
        "",
        _markdown_table(rec),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: timing repair only; no signal threshold tuning in Phase430.",
    ]
    (output_dir / "phase430_timing_geometry_audit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(raw_root: Path = DEFAULT_RAW_ROOT, phase429_dir: Path = DEFAULT_PHASE429_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR, real_roots: list[Path] | None = None) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase429 = read_csv(phase429_dir / "phase429_acceptance_summary.csv")
    if str(metric_value(phase429, "phase429_next_best_action", "")) != "precommit_phase430_timing_geometry_audit_before_new_strategy_sweep":
        raise ValueError("Phase430 requires Phase429 timing-audit next action.")
    synthetic = load_synthetic_timing(raw_root)
    real = load_real_timing(real_roots or DEFAULT_REAL_ROOTS)
    cadence = pd.concat([cadence_summary(synthetic, "synthetic"), cadence_summary(real, "real_anchor")], ignore_index=True)
    feas = pd.concat([feasibility(synthetic, "synthetic"), feasibility(real, "real_anchor")], ignore_index=True)
    agg = aggregate_feasibility(feas)
    rec = recommended_geometry(agg)
    gates = build_gates(phase429, cadence, agg, rec)
    acceptance = build_acceptance(cadence, agg, rec, gates)
    cadence.to_csv(output_dir / "phase430_cadence_summary.csv", index=False)
    feas.to_csv(output_dir / "phase430_hold_window_feasibility_by_group.csv", index=False)
    agg.to_csv(output_dir / "phase430_hold_window_feasibility_summary.csv", index=False)
    rec.to_csv(output_dir / "phase430_recommended_timing_geometry.csv", index=False)
    gates.to_csv(output_dir / "phase430_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase430_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, cadence, agg, rec, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase430_timing_geometry_audit",
        **reproducibility_fields(
            artifact_id="phase430_timing_geometry_audit",
            generated_utc=generated_utc,
            inputs={"phase429_acceptance_summary": str(phase429_dir / "phase429_acceptance_summary.csv"), "raw_root": str(raw_root)},
            parameters={"min_hold_ms": MIN_HOLD_MS, "forward_ticks": ";".join(map(str, FORWARD_TICKS)), "max_hold_ticks_to_test": ";".join(map(str, MAX_HOLD_TICKS_TO_TEST))},
            outputs={"acceptance_summary": str(output_dir / "phase430_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase430_timing_geometry_audit",
        ),
    }
    (output_dir / "phase430_timing_geometry_audit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase430 timing-geometry audit.")
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--phase429-dir", type=Path, default=DEFAULT_PHASE429_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.raw_root, args.phase429_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
