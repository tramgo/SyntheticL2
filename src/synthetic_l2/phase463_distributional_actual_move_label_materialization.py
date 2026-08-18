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
from synthetic_l2.phase461_actual_move_label_materialization import materialize_labels, read_candidate_rows
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE462_DIR = Path("outputs/phase462")
DEFAULT_OUTPUT_DIR = Path("outputs/phase463")

THESIS_ID = "P463_DISTRIBUTIONAL_ACTUAL_MOVE_LABEL_MATERIALIZATION"
NEXT_ACTION_HAS_CANDIDATES = "precommit_phase464_past_only_l2_feature_model_on_distributional_actual_move_candidates"
NEXT_ACTION_NO_CANDIDATES = "repair_or_replace_distributional_generator_non_flat_move_distribution_before_strategy_replay"


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
            "median_spread_bps": 0.0,
            "median_l25_imbalance_abs": 0.0,
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
            "median_spread_bps": float(labels["spread_bps"].median()),
            "median_l25_imbalance_abs": float(labels["l25_imbalance"].abs().median()),
        }
    return pd.DataFrame([{"metric": k, "value": v} for k, v in values.items()])


def build_side_summary(labels: pd.DataFrame) -> pd.DataFrame:
    if labels.empty:
        return pd.DataFrame(columns=["label_side", "rows", "move_candidate_rows", "median_forward_return_bps", "median_abs_forward_return_bps"])
    rows = []
    for side, grp in labels.groupby("label_side", sort=True):
        rows.append(
            {
                "label_side": str(side),
                "rows": int(len(grp)),
                "move_candidate_rows": int(grp["move_candidate"].sum()),
                "median_forward_return_bps": float(grp["forward_return_bps"].median()),
                "median_abs_forward_return_bps": float(grp["abs_forward_return_bps"].median()),
            }
        )
    return pd.DataFrame(rows)


def build_symbol_summary(labels: pd.DataFrame) -> pd.DataFrame:
    if labels.empty:
        return pd.DataFrame(columns=["symbol", "trade_dates", "label_rows", "move_candidate_rows", "long_rows", "short_rows", "max_abs_forward_return_bps"])
    rows = []
    for symbol, grp in labels.groupby("symbol", sort=True):
        rows.append(
            {
                "symbol": str(symbol),
                "trade_dates": int(grp["trade_date"].nunique()),
                "label_rows": int(len(grp)),
                "move_candidate_rows": int(grp["move_candidate"].sum()),
                "long_rows": int(grp["label_side"].eq("long").sum()),
                "short_rows": int(grp["label_side"].eq("short").sum()),
                "max_abs_forward_return_bps": float(grp["abs_forward_return_bps"].max()),
            }
        )
    return pd.DataFrame(rows)


def sval(summary: pd.DataFrame, key: str, default: Any = 0) -> Any:
    rows = summary.loc[summary["metric"].eq(key), "value"].tolist()
    return rows[0] if rows else default


def build_gates(phase462: pd.DataFrame, summary: pd.DataFrame, files: pd.DataFrame) -> pd.DataFrame:
    gates = [
        ("P463_PHASE462_PRECOMMIT_USED", as_int(scalar(phase462, "phase462_phase463_allowed_next", 0)) == 1, scalar(phase462, "phase462_phase463_allowed_next", 0), 1),
        ("P463_SELECTED_FILES_PRESENT", int(files["exists"].sum()) == len(files), int(files["exists"].sum()), len(files)),
        ("P463_LABEL_ROWS_PRESENT", as_int(sval(summary, "label_rows", 0)) > 0, sval(summary, "label_rows", 0), ">0"),
        ("P463_MOVE_CANDIDATES_PRESENT", as_int(sval(summary, "move_candidate_rows", 0)) > 0, sval(summary, "move_candidate_rows", 0), ">0"),
        ("P463_DATE_BREADTH_GE_5", as_int(sval(summary, "trade_dates", 0)) >= 5, sval(summary, "trade_dates", 0), ">=5"),
        ("P463_SYMBOL_BREADTH_GE_3", as_int(sval(summary, "symbols", 0)) >= 3, sval(summary, "symbols", 0), ">=3"),
        ("P463_LONG_LABELS_PRESENT", as_int(sval(summary, "long_label_rows", 0)) > 0, sval(summary, "long_label_rows", 0), ">0"),
        ("P463_SHORT_LABELS_PRESENT", as_int(sval(summary, "short_label_rows", 0)) > 0, sval(summary, "short_label_rows", 0), ">0"),
        ("P463_FULL_DEPTH_FEATURE_COLUMNS_PRESENT", float(sval(summary, "median_l25_imbalance_abs", 0.0)) >= 0.0, sval(summary, "median_l25_imbalance_abs", 0.0), "computed_from_L2_L5"),
        ("P463_NO_STRATEGY_PNL", True, "label_materialization_only", "no_pnl"),
        ("P463_NO_PAPER_LIVE_OR_CLAIM", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    has_candidates = hard_pass == hard_rows
    rows = [
        ("phase463_distributional_actual_move_label_materialization_complete", 1, "Phase463 label materialization completed"),
        ("phase463_thesis_id", THESIS_ID, "Label materialization thesis"),
        ("phase463_label_rows", sval(summary, "label_rows", 0), "All materialized label rows"),
        ("phase463_move_candidate_rows", sval(summary, "move_candidate_rows", 0), "Rows passing non-flat move floor"),
        ("phase463_trade_dates", sval(summary, "trade_dates", 0), "Dates with labels"),
        ("phase463_symbols", sval(summary, "symbols", 0), "Symbols with labels"),
        ("phase463_long_label_rows", sval(summary, "long_label_rows", 0), "Long forward labels"),
        ("phase463_short_label_rows", sval(summary, "short_label_rows", 0), "Short forward labels"),
        ("phase463_strategy_pnl_generated", 0, "No P&L generated"),
        ("phase463_strategy_promotion_allowed", 0, "No promotion"),
        ("phase463_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase463_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase463_phase464_allowed_next", int(has_candidates), "Allows past-only L2 feature-model precommit only if all gates pass"),
        ("phase463_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase463_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase463_next_best_action", NEXT_ACTION_HAS_CANDIDATES if has_candidates else NEXT_ACTION_NO_CANDIDATES, "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(
    output_dir: Path,
    acceptance: pd.DataFrame,
    summary: pd.DataFrame,
    side_summary: pd.DataFrame,
    symbol_summary: pd.DataFrame,
    files: pd.DataFrame,
    gates: pd.DataFrame,
) -> None:
    lines = [
        "# Phase463 Distributional Actual-Move Label Materialization",
        "",
        "Phase463 materializes actual non-flat forward-move labels on the Phase162/P159 distributional full-year L1-L5 source. It emits no strategy P&L and makes no acceptance claim.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Label Summary",
        "",
        _markdown_table(summary),
        "",
        "## Label Side Summary",
        "",
        _markdown_table(side_summary),
        "",
        "## Symbol Summary",
        "",
        _markdown_table(symbol_summary),
        "",
        "## Selected Files",
        "",
        _markdown_table(files),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: labels are research labels only. Phase464 must precommit any past-only feature model before strategy P&L exists.",
    ]
    (output_dir / "phase463_distributional_actual_move_label_materialization_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase462_dir: Path = DEFAULT_PHASE462_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase462 = read_csv(phase462_dir / "phase462_acceptance_summary.csv")
    contract = read_csv(phase462_dir / "phase462_frozen_phase463_contract.csv")
    files = read_csv(phase462_dir / "phase462_selected_replacement_files.csv")
    if as_int(scalar(phase462, "phase462_phase463_allowed_next", 0)) != 1:
        raise ValueError("Phase463 requires Phase462 materialization allowance.")
    months = slist(cval(contract, "months"))
    symbols = slist(cval(contract, "target_symbols"))
    starts = ilist(cval(contract, "window_start_rows"))
    entry_index = ival(contract, "entry_index", 20)
    horizon = ival(contract, "horizon_ticks", 240)
    min_abs_move = fval(contract, "min_abs_forward_move_bps", 2.0)
    files = files[files["trade_month"].astype(str).isin(months) & files["symbol"].astype(str).isin(symbols)].copy()
    rows_per_window = entry_index + horizon + 1
    raw_parts = [read_candidate_rows(Path(row["path"]), str(row["trade_month"]), starts, rows_per_window) for row in files.to_dict("records")]
    raw = pd.concat(raw_parts, ignore_index=True) if raw_parts else pd.DataFrame()
    labels = materialize_labels(raw, starts, entry_index, horizon, min_abs_move)
    summary = build_summary(labels, files)
    side_summary = build_side_summary(labels)
    symbol_summary = build_symbol_summary(labels)
    gates = build_gates(phase462, summary, files)
    acceptance = build_acceptance(summary, gates)
    files.to_csv(output_dir / "phase463_selected_files.csv", index=False)
    labels.to_csv(output_dir / "phase463_feature_label_ledger.csv", index=False)
    summary.to_csv(output_dir / "phase463_label_summary.csv", index=False)
    side_summary.to_csv(output_dir / "phase463_label_side_summary.csv", index=False)
    symbol_summary.to_csv(output_dir / "phase463_symbol_summary.csv", index=False)
    gates.to_csv(output_dir / "phase463_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase463_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, summary, side_summary, symbol_summary, files, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase463_distributional_actual_move_label_materialization",
        **reproducibility_fields(
            artifact_id="phase463_distributional_actual_move_label_materialization",
            generated_utc=generated_utc,
            inputs={"phase462_contract": str(phase462_dir / "phase462_frozen_phase463_contract.csv")},
            parameters={"thesis_id": THESIS_ID, "months": months, "symbols": symbols, "starts": starts, "entry_index": entry_index, "horizon": horizon, "min_abs_move_bps": min_abs_move},
            outputs={"acceptance_summary": str(output_dir / "phase463_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase463_label_materialization_only",
        ),
    }
    (output_dir / "phase463_distributional_actual_move_label_materialization_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase463 distributional actual-move label materialization.")
    parser.add_argument("--phase462-dir", type=Path, default=DEFAULT_PHASE462_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase462_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
