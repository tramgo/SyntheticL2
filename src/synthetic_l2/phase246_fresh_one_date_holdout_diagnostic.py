from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase241_one_date_unseen_real_l2_diagnostic import (
    build_controls,
    materialize_one_date_features,
    replay_frozen_candidate,
    summarize_diagnostic,
)
from synthetic_l2.phase235_real_anchor_microprice_replay import materialize_event_bars
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_RAW_ROOT = Path("real_data_sample/l2_unseen_validation")
DEFAULT_PHASE244_DIR = Path("outputs/phase244")
DEFAULT_OUTPUT_DIR = Path("outputs/phase246")
DEFAULT_TRADE_DATE = "2026-07-20"
SOURCE_HORIZON_SEC = 15


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def metric_value(path: Path, metric: str, default: Any = None) -> Any:
    frame = read_csv(path)
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def load_phase244_candidate(phase244_dir: Path) -> dict[str, Any]:
    spec_path = phase244_dir / "phase244_frozen_candidate_spec.csv"
    spec = read_csv(spec_path)
    if spec.empty:
        raise FileNotFoundError(spec_path)
    row = spec.iloc[0].to_dict()
    if as_int(row.get("frozen_for_future_holdout", 0), 0) != 1:
        raise ValueError("Phase244 candidate is not explicitly frozen for future holdout")
    if as_int(row.get("parameter_tuning_allowed_in_future_holdout", 1), 1) != 0:
        raise ValueError("Phase244 candidate does not explicitly forbid future-holdout parameter tuning")
    return row


def count_raw_files(raw_root: Path, trade_date: str) -> tuple[int, int]:
    date_root = raw_root / f"trade_date={trade_date}" / "exchange=NSE"
    if not date_root.exists():
        return 0, 0
    symbol_dirs = [path for path in date_root.glob("symbol=*") if path.is_dir()]
    files = sum(1 for path in date_root.rglob("*.parquet") if path.is_file())
    return len(symbol_dirs), files


def build_gate_evaluation(
    summary: pd.DataFrame,
    controls: pd.DataFrame,
    phase244_dir: Path,
    trade_date: str,
    requested_policy: str,
) -> pd.DataFrame:
    row = summary.iloc[0].to_dict() if not summary.empty else {}
    trades = as_int(row.get("diagnostic_trade_rows", 0), 0)
    net = as_float(row.get("diagnostic_net_pnl_inr", 0.0), 0.0)
    symbols = as_int(row.get("diagnostic_symbols", 0), 0)
    raw_files = as_int(row.get("raw_parquet_files", 0), 0)
    event_bars = as_int(row.get("materialized_event_bars", 0), 0)
    control_pass = int(controls["passed"].astype(bool).sum()) if not controls.empty else 0
    min_trades = as_int(metric_value(phase244_dir / "phase244_acceptance_summary.csv", "phase244_min_holdout_trades_required", 20), 20)
    min_symbols = as_int(metric_value(phase244_dir / "phase244_acceptance_summary.csv", "phase244_min_holdout_symbols_required", 10), 10)
    return pd.DataFrame(
        [
            ("P246_ONE_NEW_DATE_POLICY_SELECTED", requested_policy == "one_new_date_first", requested_policy, "one_new_date_first", "hard"),
            ("P246_FORBIDDEN_TUNING_DATE_EXCLUDED", trade_date != "2026-07-17", trade_date, "not 2026-07-17", "hard"),
            ("P246_RAW_L2_PRESENT", raw_files > 0, raw_files, ">0 raw parquet files", "hard"),
            ("P246_EVENT_BARS_MATERIALIZED", event_bars > 0, event_bars, ">0 event bars", "hard"),
            ("P246_FROZEN_PHASE244_CANDIDATE_REPLAYED", trades >= 1, trades, ">=1 frozen-candidate trade", "hard"),
            ("P246_DIAGNOSTIC_NET_POSITIVE", net > 0, net, ">0 net P&L after modeled costs", "diagnostic"),
            ("P246_DIAGNOSTIC_MIN_TRADES", trades >= min_trades, trades, f">={min_trades} trades", "diagnostic"),
            ("P246_DIAGNOSTIC_MIN_SYMBOLS", symbols >= min_symbols, symbols, f">={min_symbols} symbols", "diagnostic"),
            ("P246_DIAGNOSTIC_CONTROLS", control_pass == len(controls) and len(controls) > 0, f"{control_pass}/{len(controls)}", "4/4 controls", "diagnostic"),
            ("P246_FULL_ACCEPTANCE_CLOSED_ONE_DATE_ONLY", True, 1, 1, "hard"),
            ("P246_NO_TUNING_PROMOTION_PAPER_OR_LIVE", True, 0, 0, "hard"),
        ],
        columns=["gate_id", "passed", "observed_value", "required_value", "severity"],
    )


def write_report(path: Path, tables: dict[str, pd.DataFrame], trade_date: str) -> None:
    lines = [
        "# Phase246 Fresh One-date Holdout Diagnostic",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        f"Phase246 applies the frozen Phase244 candidate to one fresh unseen real L2 date (`{trade_date}`) using the disk-conscious one-date-first policy.",
        "It is an early-falsification diagnostic only: one date can reject the candidate, but one date cannot accept or promote it.",
        "No thresholds, horizons, symbols, costs, controls, paper/live routing or profitability claims are changed by this phase.",
        "",
    ]
    for title, table in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(table), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    raw_root: Path = DEFAULT_RAW_ROOT,
    phase244_dir: Path = DEFAULT_PHASE244_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    trade_date: str = DEFAULT_TRADE_DATE,
    requested_policy: str = "one_new_date_first",
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    candidate = load_phase244_candidate(phase244_dir)
    raw_symbol_dirs, raw_parquet_files = count_raw_files(raw_root, trade_date)
    features_15s, symbol_inventory = materialize_one_date_features(raw_root, trade_date)
    if symbol_inventory.empty and raw_parquet_files:
        symbol_inventory = pd.DataFrame(
            [
                {
                    "trade_date": trade_date,
                    "exchange": "NSE",
                    "symbol": "__unmaterialized__",
                    "source_1s_rows": 0,
                    "raw_parquet_files": raw_parquet_files,
                }
            ]
        )
    bars = materialize_event_bars(features_15s) if not features_15s.empty else pd.DataFrame()
    trades, labeled_bars = replay_frozen_candidate(bars, candidate) if not bars.empty else (pd.DataFrame(), bars)
    summary = summarize_diagnostic(trades, bars, symbol_inventory, candidate)
    if not summary.empty:
        summary.loc[:, "raw_symbol_dirs"] = raw_symbol_dirs
    controls = build_controls(trades)
    gates = build_gate_evaluation(summary, controls, phase244_dir, trade_date, requested_policy)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    diagnostic = gates[gates["severity"].astype(str).eq("diagnostic")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    diagnostic_pass = int(diagnostic["passed"].astype(bool).sum()) if not diagnostic.empty else 0
    diagnostic_survived = int(diagnostic_pass == len(diagnostic) and not diagnostic.empty)
    next_action = (
        "download_second_fresh_unseen_date_for_phase244_candidate_no_tuning_no_paper_live"
        if diagnostic_survived
        else "close_or_redesign_phase244_candidate_after_phase246_one_date_failure_no_more_downloads_no_paper_live"
    )
    summary_row = summary.iloc[0].to_dict() if not summary.empty else {}
    acceptance = pd.DataFrame(
        [
            ("phase246_fresh_one_date_holdout_diagnostic_complete", 1, "Phase246 one-date fresh holdout diagnostic completed"),
            ("phase246_trade_date", trade_date, "Fresh unseen real date used"),
            ("phase246_requested_policy", requested_policy, "Storage/download policy selected"),
            ("phase246_candidate_id", candidate.get("candidate_id", ""), "Frozen Phase244 candidate"),
            ("phase246_parameter_tuning_used", 0, "No Phase246 parameter tuning"),
            ("phase246_raw_symbol_dirs", raw_symbol_dirs, "Raw symbol directories represented"),
            ("phase246_raw_parquet_files", raw_parquet_files, "Raw parquet files represented"),
            ("phase246_source_feature_rows_15s", int(len(features_15s)), "15-second source feature rows materialized"),
            ("phase246_real_event_bar_rows", int(len(bars)), "Phase235-compatible event bars materialized"),
            ("phase246_trade_rows", as_int(summary_row.get("diagnostic_trade_rows", 0), 0), "Frozen candidate trades selected"),
            ("phase246_net_pnl_inr", as_float(summary_row.get("diagnostic_net_pnl_inr", 0.0), 0.0), "One-date diagnostic net P&L after costs"),
            ("phase246_symbols", as_int(summary_row.get("diagnostic_symbols", 0), 0), "Symbols represented in selected trades"),
            ("phase246_control_pass_rows", int(controls["passed"].astype(bool).sum()) if not controls.empty else 0, "Controls passed"),
            ("phase246_control_rows", int(len(controls)), "Controls evaluated"),
            ("phase246_diagnostic_gate_pass_rows", diagnostic_pass, "Diagnostic gates passed"),
            ("phase246_diagnostic_gate_rows", int(len(diagnostic)), "Diagnostic gates evaluated"),
            ("phase246_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase246_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase246_one_date_diagnostic_candidate_survived", diagnostic_survived, "One-date diagnostic survived; still not acceptance"),
            ("phase246_full_acceptance_allowed", 0, "One-date diagnostic cannot satisfy full acceptance"),
            ("phase246_strategy_promotion_allowed", 0, "No strategy promotion from Phase246"),
            ("phase246_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase246"),
            ("phase246_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase246"),
            ("phase246_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    features_15s.to_parquet(output_dir / "phase246_source_features_15s.parquet", index=False)
    bars.to_parquet(output_dir / "phase246_real_event_bars.parquet", index=False)
    labeled_bars.to_parquet(output_dir / "phase246_labeled_real_event_bars.parquet", index=False)
    trades.to_csv(output_dir / "phase246_trade_ledger.csv", index=False)
    summary.to_csv(output_dir / "phase246_diagnostic_summary.csv", index=False)
    symbol_inventory.to_csv(output_dir / "phase246_symbol_inventory.csv", index=False)
    controls.to_csv(output_dir / "phase246_control_summary.csv", index=False)
    gates.to_csv(output_dir / "phase246_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase246_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase246_fresh_one_date_holdout_diagnostic_report.md",
        {
            "Acceptance Summary": acceptance,
            "Diagnostic Summary": summary,
            "Controls": controls,
            "Gate Evaluation": gates,
            "Symbol Inventory": symbol_inventory,
        },
        trade_date=trade_date,
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase246_fresh_one_date_holdout_diagnostic",
        **reproducibility_fields(
            artifact_id="phase246",
            generated_utc=generated_utc,
            inputs={
                "raw_root": str(raw_root),
                "phase244_frozen_candidate_spec": str(phase244_dir / "phase244_frozen_candidate_spec.csv"),
            },
            parameters={
                "trade_date": trade_date,
                "source_horizon_sec": SOURCE_HORIZON_SEC,
                "requested_policy": requested_policy,
                "parameter_tuning_used": 0,
                "one_date_only_disk_conscious_policy": 1,
                "full_acceptance_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "source_features_15s": str(output_dir / "phase246_source_features_15s.parquet"),
                "real_event_bars": str(output_dir / "phase246_real_event_bars.parquet"),
                "labeled_real_event_bars": str(output_dir / "phase246_labeled_real_event_bars.parquet"),
                "trade_ledger": str(output_dir / "phase246_trade_ledger.csv"),
                "diagnostic_summary": str(output_dir / "phase246_diagnostic_summary.csv"),
                "symbol_inventory": str(output_dir / "phase246_symbol_inventory.csv"),
                "control_summary": str(output_dir / "phase246_control_summary.csv"),
                "gate_evaluation": str(output_dir / "phase246_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase246_acceptance_summary.csv"),
                "report": str(output_dir / "phase246_fresh_one_date_holdout_diagnostic_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase246_phase244_frozen_event_bar_adapter_one_new_date",
        ),
    }
    (output_dir / "phase246_fresh_one_date_holdout_diagnostic_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase246 one fresh unseen date holdout diagnostic.")
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--phase244-dir", type=Path, default=DEFAULT_PHASE244_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--trade-date", default=DEFAULT_TRADE_DATE)
    parser.add_argument("--requested-policy", default="one_new_date_first")
    args = parser.parse_args()
    manifest = run(
        raw_root=args.raw_root,
        phase244_dir=args.phase244_dir,
        output_dir=args.output_dir,
        trade_date=args.trade_date,
        requested_policy=args.requested_policy,
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
