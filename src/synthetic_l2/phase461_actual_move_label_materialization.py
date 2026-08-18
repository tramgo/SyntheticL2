from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE460_DIR = Path("outputs/phase460")
DEFAULT_DENSE_ROOT = Path("raw_synthetic_l2_dense_full_year")
DEFAULT_OUTPUT_DIR = Path("outputs/phase461")

THESIS_ID = "P461_ACTUAL_MOVE_CANDIDATE_LABEL_MATERIALIZATION"
NEXT_ACTION_HAS_CANDIDATES = "precommit_phase462_past_only_l2_feature_model_on_actual_move_candidates"
NEXT_ACTION_NO_CANDIDATES = "pause_or_repair_synthetic_generator_non_flat_move_distribution_before_strategy_replay"

BATCH_SIZE = 50_000
NEEDED_COLUMNS = [
    "exchange_timestamp_ms",
    "trade_date",
    "exchange",
    "symbol",
    "last_price",
    "buy_1_price",
    "sell_1_price",
    "buy_1_quantity",
    "sell_1_quantity",
    "buy_2_quantity",
    "buy_3_quantity",
    "buy_4_quantity",
    "buy_5_quantity",
    "sell_2_quantity",
    "sell_3_quantity",
    "sell_4_quantity",
    "sell_5_quantity",
    "volume_traded",
]


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def cval(contract: pd.DataFrame, key: str, default: str = "") -> str:
    rows = contract.loc[contract["contract_id"].astype(str).eq(key), "contract_value"].astype(str).tolist()
    return rows[0] if rows else default


def slist(value: str) -> list[str]:
    return [x.strip() for x in str(value).split(";") if x.strip()]


def ilist(value: str) -> list[int]:
    return [int(float(x.strip())) for x in str(value).split(";") if x.strip()]


def fval(contract: pd.DataFrame, key: str, default: float) -> float:
    try:
        return float(cval(contract, key, str(default)))
    except ValueError:
        return default


def ival(contract: pd.DataFrame, key: str, default: int) -> int:
    try:
        return int(float(cval(contract, key, str(default))))
    except ValueError:
        return default


def selected_files(dense_root: Path, months: list[str], symbols: list[str]) -> pd.DataFrame:
    rows = []
    for month in months:
        for symbol in symbols:
            path = dense_root / f"trade_month={month}" / f"symbol={symbol}" / "part-00000.parquet"
            rows.append({"trade_month": month, "symbol": symbol, "path": str(path), "exists": int(path.exists())})
    return pd.DataFrame(rows)


def read_candidate_rows(path: Path, month: str, starts: list[int], rows_per_window: int) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=NEEDED_COLUMNS + ["candidate_start_row", "window_local_row"])
    max_end = max(starts) + rows_per_window
    counts: dict[str, int] = {}
    parts = []
    pf = pq.ParquetFile(path)
    for batch in pf.iter_batches(batch_size=BATCH_SIZE, columns=NEEDED_COLUMNS):
        df = batch.to_pandas()
        if df.empty:
            continue
        df = df[df["trade_date"].astype(str).str.startswith(month)].copy()
        if df.empty:
            continue
        keep_frames = []
        for trade_date, grp in df.groupby("trade_date", sort=False):
            key = str(trade_date)
            seen = counts.get(key, 0)
            n = len(grp)
            counts[key] = seen + n
            if seen >= max_end or seen + n <= min(starts):
                continue
            windows = []
            for start in starts:
                local_start = max(0, start - seen)
                local_end = min(n, start + rows_per_window - seen)
                if local_start < local_end:
                    window = grp.iloc[local_start:local_end].copy()
                    absolute_rows = range(seen + local_start, seen + local_end)
                    window["candidate_start_row"] = start
                    window["window_local_row"] = [row - start for row in absolute_rows]
                    windows.append(window)
            if windows:
                keep_frames.append(pd.concat(windows, ignore_index=False))
        if keep_frames:
            parts.append(pd.concat(keep_frames, ignore_index=True))
    return pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=NEEDED_COLUMNS + ["candidate_start_row", "window_local_row"])


def features_for_group(g: pd.DataFrame, entry_index: int, horizon: int, min_abs_move_bps: float) -> dict[str, Any] | None:
    local_entry = entry_index
    local_exit = local_entry + horizon
    if local_exit >= len(g):
        return None
    start = int(g.loc[0, "candidate_start_row"])
    entry = float(g.loc[local_entry, "mid_price"])
    exit_px = float(g.loc[local_exit, "mid_price"])
    if entry <= 0:
        return None
    bid_l25 = g.loc[local_entry, ["buy_2_quantity", "buy_3_quantity", "buy_4_quantity", "buy_5_quantity"]].sum()
    ask_l25 = g.loc[local_entry, ["sell_2_quantity", "sell_3_quantity", "sell_4_quantity", "sell_5_quantity"]].sum()
    bid_l1 = float(g.loc[local_entry, "buy_1_quantity"])
    ask_l1 = float(g.loc[local_entry, "sell_1_quantity"])
    lookback_start = max(0, local_entry - 20)
    prior = float(g.loc[lookback_start, "mid_price"])
    forward = (exit_px - entry) / entry * 10_000.0
    abs_forward = abs(forward)
    return {
        "candidate_start_row": start,
        "entry_row": local_entry,
        "exit_row": local_exit,
        "entry_price": entry,
        "exit_price": exit_px,
        "recent_mid_return_bps": ((entry - prior) / prior * 10_000.0) if prior else 0.0,
        "spread_bps": float(g.loc[local_entry, "spread_bps"]),
        "l1_imbalance": (bid_l1 - ask_l1) / (bid_l1 + ask_l1 + 1.0),
        "l25_imbalance": (float(bid_l25) - float(ask_l25)) / (float(bid_l25) + float(ask_l25) + 1.0),
        "volume_delta_lookback": float(g.loc[local_entry, "volume_traded"] - g.loc[lookback_start, "volume_traded"]),
        "forward_return_bps": forward,
        "abs_forward_return_bps": abs_forward,
        "label_side": "long" if forward > 0 else ("short" if forward < 0 else "flat"),
        "move_candidate": int(abs_forward >= min_abs_move_bps),
    }


def materialize_labels(raw: pd.DataFrame, starts: list[int], entry_index: int, horizon: int, min_abs_move_bps: float) -> pd.DataFrame:
    if raw.empty:
        return pd.DataFrame()
    out = raw.sort_values(["trade_date", "symbol", "candidate_start_row", "window_local_row", "exchange_timestamp_ms"]).copy()
    out["mid_price"] = (out["buy_1_price"] + out["sell_1_price"]) / 2.0
    out["spread_bps"] = ((out["sell_1_price"] - out["buy_1_price"]) / out["mid_price"] * 10_000.0).fillna(0.0)
    rows = []
    for (trade_date, symbol, candidate_start), grp in out.groupby(["trade_date", "symbol", "candidate_start_row"], sort=False):
        g = grp.reset_index(drop=True)
        if int(candidate_start) not in starts:
            continue
        rec = features_for_group(g, entry_index, horizon, min_abs_move_bps)
        if rec:
            rec.update({"trade_date": str(trade_date), "symbol": str(symbol), "exchange": str(g.loc[0, "exchange"])})
            rows.append(rec)
    return pd.DataFrame(rows)


def build_summary(labels: pd.DataFrame, files: pd.DataFrame) -> pd.DataFrame:
    if labels.empty:
        values = {
            "selected_files": len(files),
            "files_present": int(files["exists"].sum()) if not files.empty else 0,
            "label_rows": 0,
            "move_candidate_rows": 0,
            "trade_dates": 0,
            "symbols": 0,
            "long_label_rows": 0,
            "short_label_rows": 0,
            "flat_label_rows": 0,
            "median_abs_forward_return_bps": 0.0,
            "max_abs_forward_return_bps": 0.0,
        }
    else:
        values = {
            "selected_files": len(files),
            "files_present": int(files["exists"].sum()) if not files.empty else 0,
            "label_rows": len(labels),
            "move_candidate_rows": int(labels["move_candidate"].sum()),
            "trade_dates": int(labels["trade_date"].nunique()),
            "symbols": int(labels["symbol"].nunique()),
            "long_label_rows": int(labels["label_side"].eq("long").sum()),
            "short_label_rows": int(labels["label_side"].eq("short").sum()),
            "flat_label_rows": int(labels["label_side"].eq("flat").sum()),
            "median_abs_forward_return_bps": float(labels["abs_forward_return_bps"].median()),
            "max_abs_forward_return_bps": float(labels["abs_forward_return_bps"].max()),
        }
    return pd.DataFrame([{"metric": k, "value": v} for k, v in values.items()])


def sval(summary: pd.DataFrame, key: str, default: Any = 0) -> Any:
    rows = summary.loc[summary["metric"].eq(key), "value"].tolist()
    return rows[0] if rows else default


def build_gates(phase460: pd.DataFrame, summary: pd.DataFrame, files: pd.DataFrame) -> pd.DataFrame:
    gates = [
        ("P461_PHASE460_PRECOMMIT_USED", as_int(scalar(phase460, "phase460_phase461_allowed_next", 0)) == 1, scalar(phase460, "phase460_phase461_allowed_next", 0), 1),
        ("P461_SELECTED_FILES_PRESENT", int(files["exists"].sum()) == len(files), int(files["exists"].sum()), len(files)),
        ("P461_LABEL_ROWS_PRESENT", as_int(sval(summary, "label_rows", 0)) > 0, sval(summary, "label_rows", 0), ">0"),
        ("P461_MOVE_CANDIDATES_PRESENT", as_int(sval(summary, "move_candidate_rows", 0)) > 0, sval(summary, "move_candidate_rows", 0), ">0"),
        ("P461_DATE_BREADTH_GE_5", as_int(sval(summary, "trade_dates", 0)) >= 5, sval(summary, "trade_dates", 0), ">=5"),
        ("P461_SYMBOL_BREADTH_GE_3", as_int(sval(summary, "symbols", 0)) >= 3, sval(summary, "symbols", 0), ">=3"),
        ("P461_LONG_OR_SHORT_LABELS_PRESENT", as_int(sval(summary, "long_label_rows", 0)) + as_int(sval(summary, "short_label_rows", 0)) > 0, f"long={sval(summary, 'long_label_rows', 0)};short={sval(summary, 'short_label_rows', 0)}", ">0"),
        ("P461_NO_STRATEGY_PNL", True, "label_materialization_only", "no_pnl"),
        ("P461_NO_PAPER_LIVE_OR_CLAIM", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    has_candidates = hard_pass == hard_rows
    return pd.DataFrame(
        [
            ("phase461_actual_move_label_materialization_complete", 1, "Phase461 label materialization completed"),
            ("phase461_thesis_id", THESIS_ID, "Label materialization thesis"),
            ("phase461_label_rows", sval(summary, "label_rows", 0), "All materialized label rows"),
            ("phase461_move_candidate_rows", sval(summary, "move_candidate_rows", 0), "Rows passing non-flat move floor"),
            ("phase461_trade_dates", sval(summary, "trade_dates", 0), "Dates with labels"),
            ("phase461_symbols", sval(summary, "symbols", 0), "Symbols with labels"),
            ("phase461_long_label_rows", sval(summary, "long_label_rows", 0), "Long forward labels"),
            ("phase461_short_label_rows", sval(summary, "short_label_rows", 0), "Short forward labels"),
            ("phase461_strategy_pnl_generated", 0, "No P&L generated"),
            ("phase461_strategy_promotion_allowed", 0, "No promotion"),
            ("phase461_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase461_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase461_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase461_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase461_next_best_action", NEXT_ACTION_HAS_CANDIDATES if has_candidates else NEXT_ACTION_NO_CANDIDATES, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, summary: pd.DataFrame, gates: pd.DataFrame, files: pd.DataFrame) -> None:
    lines = [
        "# Phase461 Actual-Move Candidate Label Materialization",
        "",
        "Phase461 materializes actual non-flat forward-move labels from dense raw L1-L5 data. It emits no P&L and makes no strategy acceptance claim.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Label Summary",
        "",
        _markdown_table(summary),
        "",
        "## Selected Files",
        "",
        _markdown_table(files),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: actual forward move labels are research labels only. A later phase must precommit past-only modeling/replay before any strategy P&L.",
    ]
    (output_dir / "phase461_actual_move_label_materialization_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase460_dir: Path = DEFAULT_PHASE460_DIR, dense_root: Path = DEFAULT_DENSE_ROOT, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase460 = read_csv(phase460_dir / "phase460_acceptance_summary.csv")
    contract = read_csv(phase460_dir / "phase460_frozen_phase461_contract.csv")
    if as_int(scalar(phase460, "phase460_phase461_allowed_next", 0)) != 1:
        raise ValueError("Phase461 requires Phase460 materialization allowance.")
    months = slist(cval(contract, "months"))
    symbols = slist(cval(contract, "target_symbols"))
    starts = ilist(cval(contract, "window_start_rows"))
    entry_index = ival(contract, "entry_index", 20)
    horizon = ival(contract, "horizon_ticks", 240)
    min_abs_move = fval(contract, "min_abs_forward_move_bps", 2.0)
    rows_per_window = entry_index + horizon + 1
    files = selected_files(dense_root, months, symbols)
    raw_parts = [read_candidate_rows(Path(row["path"]), str(row["trade_month"]), starts, rows_per_window) for row in files.to_dict("records")]
    raw = pd.concat(raw_parts, ignore_index=True) if raw_parts else pd.DataFrame(columns=NEEDED_COLUMNS)
    labels = materialize_labels(raw, starts, entry_index, horizon, min_abs_move)
    summary = build_summary(labels, files)
    gates = build_gates(phase460, summary, files)
    acceptance = build_acceptance(summary, gates)
    files.to_csv(output_dir / "phase461_selected_files.csv", index=False)
    labels.to_csv(output_dir / "phase461_feature_label_ledger.csv", index=False)
    summary.to_csv(output_dir / "phase461_label_summary.csv", index=False)
    gates.to_csv(output_dir / "phase461_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase461_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, summary, gates, files)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase461_actual_move_label_materialization",
        **reproducibility_fields(
            artifact_id="phase461_actual_move_label_materialization",
            generated_utc=generated_utc,
            inputs={"phase460_acceptance_summary": str(phase460_dir / "phase460_acceptance_summary.csv"), "dense_root": str(dense_root)},
            parameters={"thesis_id": THESIS_ID, "months": months, "symbols": symbols, "starts": starts, "entry_index": entry_index, "horizon": horizon, "min_abs_move_bps": min_abs_move},
            outputs={"acceptance_summary": str(output_dir / "phase461_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase461_label_materialization_only",
        ),
    }
    (output_dir / "phase461_actual_move_label_materialization_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase461 actual-move label materialization.")
    parser.add_argument("--phase460-dir", type=Path, default=DEFAULT_PHASE460_DIR)
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase460_dir, args.dense_root, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
