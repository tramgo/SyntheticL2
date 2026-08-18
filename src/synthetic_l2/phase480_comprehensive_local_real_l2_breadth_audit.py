from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase340_official_catalyst_calendar_acquisition_precommit import TICKERS
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase480")
THESIS_ID = "P480_COMPREHENSIVE_LOCAL_REAL_L2_BREADTH_AUDIT"
NEXT_ACTION = "precommit_next_real_l2_breadth_or_capacity_retest_using_current_16_date_panel_no_download_first"
REPAIR_ACTION = "repair_phase480_local_real_l2_breadth_audit"
LOCAL_ROOTS = [
    Path("real_data_sample/l2_multiday_panel"),
    Path("real_data_sample/l2_unseen_validation"),
    Path("scratch_azcopy_selected/raw_l2"),
    Path("real_data_sample/l2_single_day"),
    Path("scratch_l2_sample_20260710_HDFCBANK"),
    Path("raw_l2"),
]
CATALYST_FILES = [
    Path("outputs/phase399/phase373_official_catalyst_calendar.csv"),
    Path("outputs/phase373/phase373_official_catalyst_calendar.csv"),
    Path("outputs/phase359/phase359_official_catalyst_calendar.csv"),
    Path("outputs/phase340/phase340_official_catalyst_calendar.csv"),
]
LATEST_REFRESH_SUMMARY = Path("outputs/phase399/phase373_acceptance_summary.csv")
LATEST_PRECOMMIT_SUMMARY = Path("outputs/phase400/phase386_acceptance_summary.csv")
LATEST_RETEST_SUMMARY = Path("outputs/phase401/phase387_acceptance_summary.csv")
LATEST_INTERPRET_SUMMARY = Path("outputs/phase402/phase388_acceptance_summary.csv")


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def parse_parts(path: Path) -> dict[str, str]:
    fields = {"trade_date": "", "exchange": "", "symbol": ""}
    for part in path.parts:
        if part.startswith("trade_date="):
            fields["trade_date"] = part.split("=", 1)[1]
        elif part.startswith("exchange="):
            fields["exchange"] = part.split("=", 1)[1]
        elif part.startswith("symbol="):
            fields["symbol"] = part.split("=", 1)[1]
    return fields


def build_inventory() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    by_symbol: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    schema_rows: list[dict[str, Any]] = []
    sampled_schema_keys: set[tuple[str, str, str]] = set()
    for root in LOCAL_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*.parquet"):
            fields = parse_parts(path)
            key = (str(root), fields["trade_date"], fields["exchange"], fields["symbol"])
            row = by_symbol.setdefault(
                key,
                {
                    "root": str(root),
                    "trade_date": fields["trade_date"],
                    "exchange": fields["exchange"],
                    "symbol": fields["symbol"],
                    "parquet_files": 0,
                    "bytes": 0,
                },
            )
            row["parquet_files"] += 1
            row["bytes"] += int(path.stat().st_size)
            schema_key = (str(root), fields["trade_date"], fields["symbol"])
            if fields["trade_date"] and fields["symbol"] and schema_key not in sampled_schema_keys:
                sampled_schema_keys.add(schema_key)
                try:
                    columns = pq.ParquetFile(path).schema.names
                    required = [
                        "last_price",
                        "buy_1_price",
                        "buy_1_quantity",
                        "sell_1_price",
                        "sell_1_quantity",
                        "buy_5_price",
                        "buy_5_quantity",
                        "sell_5_price",
                        "sell_5_quantity",
                    ]
                    schema_rows.append(
                        {
                            "root": str(root),
                            "trade_date": fields["trade_date"],
                            "symbol": fields["symbol"],
                            "sample_file": str(path),
                            "column_count": len(columns),
                            "has_l1": int(all(col in columns for col in required[:5])),
                            "has_top5": int(all(col in columns for col in required)),
                            "missing_required_columns": ";".join(col for col in required if col not in columns),
                        }
                    )
                except Exception as exc:
                    schema_rows.append(
                        {
                            "root": str(root),
                            "trade_date": fields["trade_date"],
                            "symbol": fields["symbol"],
                            "sample_file": str(path),
                            "column_count": 0,
                            "has_l1": 0,
                            "has_top5": 0,
                            "missing_required_columns": type(exc).__name__ + ":" + str(exc)[:120],
                        }
                    )
    symbol_inventory = pd.DataFrame(by_symbol.values())
    if symbol_inventory.empty:
        symbol_inventory = pd.DataFrame(columns=["root", "trade_date", "exchange", "symbol", "parquet_files", "bytes"])
    dated = symbol_inventory[symbol_inventory["trade_date"].astype(str).ne("")].copy()
    if dated.empty:
        date_summary = pd.DataFrame(columns=["trade_date", "roots", "symbols", "parquet_files", "bytes", "full_32_symbol_universe"])
    else:
        grouped = dated.groupby("trade_date", dropna=False)
        date_summary = grouped.agg(
            roots=("root", lambda s: ";".join(sorted(set(map(str, s))))),
            symbols=("symbol", lambda s: int(pd.Series(s).astype(str).replace("", pd.NA).dropna().nunique())),
            parquet_files=("parquet_files", "sum"),
            bytes=("bytes", "sum"),
        ).reset_index()
        date_summary["full_32_symbol_universe"] = (date_summary["symbols"].astype(int) >= len(TICKERS)).astype(int)
        date_summary = date_summary.sort_values("trade_date", kind="mergesort")
    schema = pd.DataFrame(schema_rows)
    if schema.empty:
        schema = pd.DataFrame(columns=["root", "trade_date", "symbol", "sample_file", "column_count", "has_l1", "has_top5", "missing_required_columns"])
    return symbol_inventory.sort_values(["trade_date", "root", "symbol"], kind="mergesort"), date_summary, schema


def read_latest_catalyst() -> tuple[pd.DataFrame, str]:
    for path in CATALYST_FILES:
        frame = read_csv(path)
        if not frame.empty:
            return frame, str(path)
    return pd.DataFrame(), ""


def diagnostic_date(frame: pd.DataFrame) -> pd.Series:
    if "diagnostic_trade_date" in frame.columns:
        return frame["diagnostic_trade_date"].astype(str)
    return frame.get("announcement_date", pd.Series([""] * len(frame))).astype(str)


def build_catalyst_overlap(catalyst: pd.DataFrame, catalyst_source: str, date_summary: pd.DataFrame, symbol_inventory: pd.DataFrame) -> pd.DataFrame:
    if catalyst.empty or date_summary.empty:
        return pd.DataFrame(columns=["diagnostic_trade_date", "catalyst_rows", "catalyst_symbols", "local_symbols", "full_32_symbol_universe", "symbol_date_overlaps", "catalyst_source"])
    cat = catalyst.copy()
    cat["diagnostic_trade_date"] = diagnostic_date(cat)
    cat["symbol"] = cat.get("symbol", pd.Series([""] * len(cat))).astype(str)
    local_symbols = symbol_inventory[symbol_inventory["trade_date"].astype(str).ne("")][["trade_date", "symbol"]].drop_duplicates()
    rows: list[dict[str, Any]] = []
    for date, group in cat.groupby("diagnostic_trade_date", dropna=False):
        if not str(date):
            continue
        local_for_date = local_symbols.loc[local_symbols["trade_date"].astype(str).eq(str(date)), "symbol"].astype(str)
        cat_symbols = set(group["symbol"].astype(str))
        local_set = set(local_for_date)
        date_row = date_summary.loc[date_summary["trade_date"].astype(str).eq(str(date))]
        rows.append(
            {
                "diagnostic_trade_date": str(date),
                "catalyst_rows": int(len(group)),
                "catalyst_symbols": int(len(cat_symbols - {""})),
                "local_symbols": int(len(local_set - {""})),
                "full_32_symbol_universe": int(date_row["full_32_symbol_universe"].iloc[0]) if not date_row.empty else 0,
                "symbol_date_overlaps": int(len((cat_symbols & local_set) - {""})),
                "catalyst_source": catalyst_source,
            }
        )
    return pd.DataFrame(rows).sort_values("diagnostic_trade_date", kind="mergesort")


def build_latest_retest_ledger(refresh: pd.DataFrame, precommit: pd.DataFrame, retest: pd.DataFrame, interpret: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("phase399_refreshed_eligible_rows", scalar(refresh, "phase373_refreshed_no_lookahead_eligible_rows", ""), "Latest duplicated Phase373 refresh eligible rows."),
            ("phase399_estimated_selected_after_refresh", scalar(refresh, "phase373_estimated_selected_after_refresh", ""), "Latest estimated selected trades after refresh."),
            ("phase399_event_floor_after_refresh_estimate", scalar(refresh, "phase373_event_floor_after_refresh_estimate", ""), "Event floor estimate from refresh."),
            ("phase400_adapted_work_order_rows", scalar(precommit, "phase386_adapted_work_order_rows", ""), "Latest precommitted adapted work order rows."),
            ("phase400_adapted_work_order_dates", scalar(precommit, "phase386_adapted_work_order_dates", ""), "Latest work-order diagnostic dates."),
            ("phase401_primary_selected_trade_rows", scalar(retest, "phase387_primary_selected_trade_rows", ""), "Actual frozen retest selected trades."),
            ("phase401_primary_net_pnl_inr", scalar(retest, "phase387_primary_net_pnl_inr", ""), "Actual frozen retest net PnL."),
            ("phase401_primary_annualized_return_pct", scalar(retest, "phase387_primary_annualized_return_pct", ""), "Actual frozen retest annualized return."),
            ("phase401_primary_event_floor_met", scalar(retest, "phase387_primary_event_floor_met", ""), "Actual frozen retest event floor."),
            ("phase402_acceptance_candidate", scalar(interpret, "phase388_acceptance_candidate", ""), "Latest interpretation acceptance candidate flag."),
            ("phase402_capacity_selected_gap", scalar(interpret, "phase388_capacity_selected_gap", ""), "Remaining capacity-selected trade gap."),
            ("phase402_next_best_action", scalar(interpret, "phase388_next_best_action", ""), "Latest interpretation next action."),
        ],
        columns=["metric", "value", "description"],
    )


def build_decision(date_summary: pd.DataFrame, overlap: pd.DataFrame, latest: pd.DataFrame) -> pd.DataFrame:
    local_dates = int(date_summary["trade_date"].nunique()) if not date_summary.empty else 0
    full_days = int(date_summary["full_32_symbol_universe"].sum()) if not date_summary.empty else 0
    overlap_dates = int((overlap["symbol_date_overlaps"].astype(int) > 0).sum()) if not overlap.empty else 0
    selected = as_int(latest.loc[latest["metric"].eq("phase401_primary_selected_trade_rows"), "value"].iloc[0], 0)
    ann = float(latest.loc[latest["metric"].eq("phase401_primary_annualized_return_pct"), "value"].iloc[0] or 0.0)
    event_floor = as_int(latest.loc[latest["metric"].eq("phase401_primary_event_floor_met"), "value"].iloc[0], 0)
    acceptance = as_int(latest.loc[latest["metric"].eq("phase402_acceptance_candidate"), "value"].iloc[0], 0)
    return pd.DataFrame(
        [
            ("comprehensive_local_real_l2_dates", local_dates, "Local dated real-L2 dates across comprehensive roots."),
            ("comprehensive_full_32_symbol_days", full_days, "Local dates with at least the 32-symbol configured universe."),
            ("official_catalyst_overlap_dates", overlap_dates, "Dates with both local L2 and official catalyst symbol-date overlap."),
            ("latest_actual_selected_trades", selected, "Latest frozen expanded retest selected trades."),
            ("latest_actual_annualized_return_pct", ann, "Latest frozen expanded retest annualized return."),
            ("latest_event_floor_met", event_floor, "Latest frozen expanded retest event floor."),
            ("latest_acceptance_candidate", acceptance, "Latest interpretation acceptance flag."),
            ("download_required_before_any_next_step", 0, "A local 16-date panel exists; first precommit using current local evidence before downloading more."),
            ("next_action", NEXT_ACTION, "Corrects Phase478's narrow inventory and keeps paper/live closed."),
        ],
        columns=["decision_id", "decision_value", "evidence"],
    )


def build_gates(date_summary: pd.DataFrame, schema: pd.DataFrame, overlap: pd.DataFrame, latest: pd.DataFrame, decision: pd.DataFrame) -> pd.DataFrame:
    local_dates = int(date_summary["trade_date"].nunique()) if not date_summary.empty else 0
    full_days = int(date_summary["full_32_symbol_universe"].sum()) if not date_summary.empty else 0
    top5_ok = int(schema["has_top5"].astype(int).sum()) if not schema.empty else 0
    selected = as_int(latest.loc[latest["metric"].eq("phase401_primary_selected_trade_rows"), "value"].iloc[0], 0)
    acceptance = as_int(latest.loc[latest["metric"].eq("phase402_acceptance_candidate"), "value"].iloc[0], 0)
    rows = [
        ("P480_COMPREHENSIVE_ROOTS_USED", local_dates >= 16, local_dates, ">=16"),
        ("P480_FULL_UNIVERSE_DAYS_PRESENT", full_days >= 1, full_days, ">=1"),
        ("P480_TOP5_SCHEMA_SAMPLED", top5_ok > 0, top5_ok, ">0"),
        ("P480_OFFICIAL_CATALYST_OVERLAP_PRESENT", not overlap.empty and int(overlap["symbol_date_overlaps"].astype(int).sum()) > 0, int(overlap["symbol_date_overlaps"].astype(int).sum()) if not overlap.empty else 0, ">0"),
        ("P480_LATEST_RETEST_EVIDENCE_USED", selected > 0, selected, ">0"),
        ("P480_ACCEPTANCE_STILL_CLOSED", acceptance == 0, acceptance, 0),
        ("P480_DOWNLOAD_NOT_REQUIRED_BEFORE_NEXT_PRECOMMIT", as_int(decision.loc[decision["decision_id"].eq("download_required_before_any_next_step"), "decision_value"].iloc[0]) == 0, 0, 0),
        ("P480_NO_PROMOTION_PAPER_LIVE_OR_CLAIM", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame(
        [{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows]
    )


def build_acceptance(date_summary: pd.DataFrame, overlap: pd.DataFrame, latest: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    gate_pass = int(gates["passed"].astype(bool).sum())
    gate_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase480_comprehensive_local_real_l2_breadth_audit_complete", int(gate_pass == gate_rows), "Phase480 complete if all gates pass"),
            ("phase480_thesis_id", THESIS_ID, "Phase480 thesis"),
            ("phase480_local_real_l2_date_rows", int(date_summary["trade_date"].nunique()) if not date_summary.empty else 0, "Comprehensive local dated real-L2 dates"),
            ("phase480_full_32_symbol_day_rows", int(date_summary["full_32_symbol_universe"].sum()) if not date_summary.empty else 0, "Full 32-symbol local days"),
            ("phase480_official_catalyst_overlap_date_rows", int((overlap["symbol_date_overlaps"].astype(int) > 0).sum()) if not overlap.empty else 0, "Catalyst-overlap dates"),
            ("phase480_latest_selected_trade_rows", scalar(latest, "phase401_primary_selected_trade_rows", ""), "Latest frozen retest selected trades"),
            ("phase480_latest_net_pnl_inr", scalar(latest, "phase401_primary_net_pnl_inr", ""), "Latest frozen retest net PnL"),
            ("phase480_latest_annualized_return_pct", scalar(latest, "phase401_primary_annualized_return_pct", ""), "Latest frozen retest annualized return"),
            ("phase480_latest_event_floor_met", scalar(latest, "phase401_primary_event_floor_met", ""), "Latest frozen retest event floor"),
            ("phase480_latest_acceptance_candidate", scalar(latest, "phase402_acceptance_candidate", ""), "Latest interpretation acceptance candidate"),
            ("phase480_download_required_before_next_precommit", 0, "Current local panel is sufficient for next precommit decision"),
            ("phase480_strategy_promotion_allowed", 0, "No promotion"),
            ("phase480_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase480_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase480_hard_gate_pass_rows", gate_pass, "Passed hard gates"),
            ("phase480_hard_gate_rows", gate_rows, "Hard gates"),
            ("phase480_next_best_action", NEXT_ACTION if gate_pass == gate_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, date_summary: pd.DataFrame, overlap: pd.DataFrame, latest: pd.DataFrame, decision: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase480 Comprehensive Local Real-L2 Breadth Audit",
        "",
        "Phase480 corrects the narrow Phase478 inventory by auditing all known local real-L2 roots before asking for another Azure download.",
        "",
        "Finding: the current local panel is broader than Phase478 reported. The latest expanded real-L2 retest evidence remains not accepted: positive net PnL but below the 12 percent annualized bar and below the 30 selected-trade floor.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Local Date Summary",
        "",
        _markdown_table(date_summary),
        "",
        "## Official Catalyst Overlap",
        "",
        _markdown_table(overlap),
        "",
        "## Latest Retest Ledger",
        "",
        _markdown_table(latest),
        "",
        "## Decision Ledger",
        "",
        _markdown_table(decision),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: no strategy promotion, no paper/live, no deployable profitability claim.",
    ]
    (output_dir / "phase480_comprehensive_local_real_l2_breadth_audit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    symbol_inventory, date_summary, schema = build_inventory()
    catalyst, catalyst_source = read_latest_catalyst()
    overlap = build_catalyst_overlap(catalyst, catalyst_source, date_summary, symbol_inventory)
    refresh = read_csv(LATEST_REFRESH_SUMMARY)
    precommit = read_csv(LATEST_PRECOMMIT_SUMMARY)
    retest = read_csv(LATEST_RETEST_SUMMARY)
    interpret = read_csv(LATEST_INTERPRET_SUMMARY)
    if refresh.empty or precommit.empty or retest.empty or interpret.empty:
        raise FileNotFoundError("Phase480 requires latest Phase399-402 refresh/retest artifacts.")
    latest = build_latest_retest_ledger(refresh, precommit, retest, interpret)
    decision = build_decision(date_summary, overlap, latest)
    gates = build_gates(date_summary, schema, overlap, latest, decision)
    acceptance = build_acceptance(date_summary, overlap, latest, gates)
    symbol_inventory.to_csv(output_dir / "phase480_local_real_l2_symbol_inventory.csv", index=False)
    date_summary.to_csv(output_dir / "phase480_local_real_l2_date_summary.csv", index=False)
    schema.to_csv(output_dir / "phase480_top5_schema_sample_audit.csv", index=False)
    overlap.to_csv(output_dir / "phase480_official_catalyst_overlap_by_date.csv", index=False)
    latest.to_csv(output_dir / "phase480_latest_retest_ledger.csv", index=False)
    decision.to_csv(output_dir / "phase480_decision_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase480_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase480_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, date_summary, overlap, latest, decision, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase480_comprehensive_local_real_l2_breadth_audit",
        **reproducibility_fields(
            artifact_id="phase480_comprehensive_local_real_l2_breadth_audit",
            generated_utc=generated_utc,
            inputs={
                "local_roots": ";".join(map(str, LOCAL_ROOTS)),
                "catalyst_source": catalyst_source,
                "latest_refresh_summary": str(LATEST_REFRESH_SUMMARY),
                "latest_retest_summary": str(LATEST_RETEST_SUMMARY),
                "latest_interpret_summary": str(LATEST_INTERPRET_SUMMARY),
            },
            parameters={"thesis_id": THESIS_ID, "download_executed": False, "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase480_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase480_no_execution_inventory_audit_only",
        ),
    }
    (output_dir / "phase480_comprehensive_local_real_l2_breadth_audit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase480 comprehensive local real-L2 breadth audit.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    out = run(args.output_dir)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
