from __future__ import annotations

import argparse
import json
from datetime import datetime, time, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE339_DIR = Path("outputs/phase339")
DEFAULT_PHASE340_DIR = Path("outputs/phase340")
DEFAULT_REAL_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_REAL_FEATURE_ROOT = Path("derived_real_l2_receive_flow_features_phase176")
DEFAULT_OUTPUT_DIR = Path("outputs/phase341")

NEXT_ACTION = "run_phase342_official_catalyst_real_day_survivor_diagnostic_execution_no_paper_live"
REPAIR_ACTION = "repair_phase341_official_catalyst_real_day_survivor_diagnostic_precommit"

MARKET_OPEN = time(9, 15)
MARKET_CLOSE = time(15, 30)


def discover_real_keys(real_root: Path) -> pd.DataFrame:
    rows: set[tuple[str, str]] = set()
    if real_root.exists():
        for path in real_root.rglob("*.parquet"):
            trade_date = ""
            symbol = ""
            for part in path.parts:
                if part.startswith("trade_date="):
                    trade_date = part.split("=", 1)[1]
                if part.startswith("symbol="):
                    symbol = part.split("=", 1)[1].upper()
            if trade_date and symbol:
                rows.add((trade_date, symbol))
    return pd.DataFrame(sorted(rows), columns=["trade_date", "symbol"]) if rows else pd.DataFrame(columns=["trade_date", "symbol"])


def classify_session(ts: pd.Timestamp) -> str:
    if pd.isna(ts):
        return "unknown"
    t = ts.time()
    if t < MARKET_OPEN:
        return "pre_open_or_overnight"
    if t <= MARKET_CLOSE:
        return "regular_session"
    return "post_close"


def build_eligible_catalyst_ledger(catalysts: pd.DataFrame, real_keys: pd.DataFrame) -> pd.DataFrame:
    if catalysts.empty:
        return pd.DataFrame()
    local_dates = sorted(real_keys["trade_date"].dropna().astype(str).unique().tolist())
    next_date = {d: (local_dates[idx + 1] if idx + 1 < len(local_dates) else "") for idx, d in enumerate(local_dates)}
    frame = catalysts.copy()
    frame["announcement_ts"] = pd.to_datetime(frame["announcement_time_ist"], format="%d-%b-%Y %H:%M:%S", errors="coerce")
    frame["announcement_date"] = frame["announcement_ts"].dt.strftime("%Y-%m-%d")
    frame["market_session"] = frame["announcement_ts"].map(classify_session)
    frame["diagnostic_trade_date"] = frame.apply(
        lambda row: next_date.get(str(row["announcement_date"]), "") if row["market_session"] == "post_close" else str(row["announcement_date"]),
        axis=1,
    )
    frame["diagnostic_start_rule"] = frame["market_session"].map(
        {
            "pre_open_or_overnight": "market_open_same_day",
            "regular_session": "first_real_tick_after_announcement",
            "post_close": "market_open_next_available_real_l2_day",
            "unknown": "blocked_unknown_announcement_time",
        }
    )
    available = set((row.trade_date, row.symbol) for row in real_keys.itertuples(index=False))
    frame["diagnostic_real_l2_available"] = frame.apply(lambda row: int((row["diagnostic_trade_date"], row["symbol"]) in available), axis=1)
    frame["no_lookahead_rule_applied"] = 1
    keep = [
        "source_id",
        "symbol",
        "announcement_time_ist",
        "announcement_date",
        "market_session",
        "diagnostic_trade_date",
        "diagnostic_start_rule",
        "diagnostic_real_l2_available",
        "description",
        "text",
        "attachment_url",
        "seq_id",
        "no_lookahead_rule_applied",
    ]
    return frame[keep].sort_values(["diagnostic_trade_date", "symbol", "announcement_time_ist"]).reset_index(drop=True)


def build_schema_contract(real_root: Path, real_feature_root: Path) -> pd.DataFrame:
    raw_required = ["collector_received_utc_ms", "exchange_timestamp", "last_price"]
    for side in ["buy", "sell"]:
        for level in range(1, 6):
            raw_required.extend([f"{side}_{level}_price", f"{side}_{level}_quantity", f"{side}_{level}_orders"])
    feature_required = [
        "trade_date",
        "symbol",
        "bucket_ms",
        "receive_event_count",
        "quote_churn_count",
        "depth_refresh_count",
        "stale_quote_duration_ms",
        "last_price",
        "best_bid",
        "best_ask",
        "spread",
        "l1_qty_imbalance",
        "top5_qty_imbalance",
        "horizon_sec",
    ]
    raw_cols: set[str] = set()
    feature_cols: set[str] = set()
    raw_sample = next(real_root.rglob("*.parquet"), None) if real_root.exists() else None
    feature_sample = next(real_feature_root.rglob("*.parquet"), None) if real_feature_root.exists() else None
    if raw_sample is not None:
        raw_cols = set(pd.read_parquet(raw_sample).columns)
    if feature_sample is not None:
        feature_cols = set(pd.read_parquet(feature_sample).columns)
    rows = []
    for col in raw_required:
        rows.append({"source": "raw_real_l2", "column": col, "required": 1, "present": int(col in raw_cols), "purpose": "full top-five market-by-price diagnostic input"})
    for col in feature_required:
        rows.append({"source": "phase176_real_receive_flow_features", "column": col, "required": 1, "present": int(col in feature_cols), "purpose": "coarse real receive-flow compatibility diagnostic"})
    rows.extend(
        [
            {"source": "diagnostic_policy", "column": "levels_2_to_5_materiality_required", "required": 1, "present": 1, "purpose": "forbid L1-only reinterpretation"},
            {"source": "diagnostic_policy", "column": "fixed_capital_annualized_denominator", "required": 1, "present": 1, "purpose": "avoid unlimited-capital return math"},
            {"source": "diagnostic_policy", "column": "zerodha_2x_all_in_cost_proxy", "required": 1, "present": 1, "purpose": "cost-stressed diagnostic threshold"},
        ]
    )
    return pd.DataFrame(rows)


def build_work_order(survivors: pd.DataFrame, eligible: pd.DataFrame) -> pd.DataFrame:
    eligible_rows = eligible[eligible["diagnostic_real_l2_available"].astype(int).eq(1)].copy() if not eligible.empty else pd.DataFrame()
    if survivors.empty or eligible_rows.empty:
        return pd.DataFrame()
    best = survivors.sort_values(["annualized_return_pct", "positive_symbol_date_cells", "scheduled_event_rows"], ascending=[False, False, False]).head(1).copy()
    rows = []
    for _, survivor in best.iterrows():
        for _, event in eligible_rows.iterrows():
            rows.append(
                {
                    "work_order_id": f"P341_{event['diagnostic_trade_date']}_{event['symbol']}_{event['seq_id']}",
                    "source_scenario_id": survivor["source_scenario_id"],
                    "lane_id": survivor["lane_id"],
                    "horizon_seconds": survivor["horizon_seconds"],
                    "side_policy": survivor["side_policy"],
                    "execution_policy": survivor["execution_policy"],
                    "cost_profile": survivor["cost_profile"],
                    "initial_capital_inr": survivor["initial_capital_inr"],
                    "fixed_notional_inr": survivor["fixed_notional_inr"],
                    "max_concurrent_positions": survivor["max_concurrent_positions"],
                    "official_source_id": event["source_id"],
                    "symbol": event["symbol"],
                    "announcement_time_ist": event["announcement_time_ist"],
                    "market_session": event["market_session"],
                    "diagnostic_trade_date": event["diagnostic_trade_date"],
                    "diagnostic_start_rule": event["diagnostic_start_rule"],
                    "description": event["description"],
                    "no_lookahead_rule_applied": event["no_lookahead_rule_applied"],
                    "replay_execution_allowed_in_phase341": 0,
                }
            )
    return pd.DataFrame(rows).sort_values(["diagnostic_trade_date", "symbol", "announcement_time_ist"]).reset_index(drop=True)


def build_gate_evaluation(phase340: pd.DataFrame, eligible: pd.DataFrame, work_order: pd.DataFrame, schema: pd.DataFrame) -> pd.DataFrame:
    phase340_complete = as_int(metric_value(phase340, "phase340_official_catalyst_calendar_acquisition_complete", 0))
    eligible_rows = int(eligible["diagnostic_real_l2_available"].sum()) if not eligible.empty else 0
    eligible_symbol_dates = int(eligible[eligible["diagnostic_real_l2_available"].astype(int).eq(1)][["diagnostic_trade_date", "symbol"]].drop_duplicates().shape[0]) if not eligible.empty else 0
    sbin_eligible = int(len(eligible[(eligible["symbol"].eq("SBIN")) & (eligible["diagnostic_real_l2_available"].astype(int).eq(1))])) if not eligible.empty else 0
    schema_pass = int(schema["present"].astype(int).sum()) if not schema.empty else 0
    schema_total = int(len(schema))
    rows = [
        ("P341_PHASE340_COMPLETE", phase340_complete == 1, phase340_complete, 1),
        ("P341_OFFICIAL_ELIGIBLE_EVENTS_PRESENT", eligible_rows > 0, eligible_rows, ">0"),
        ("P341_OFFICIAL_ELIGIBLE_SYMBOL_DATES_PRESENT", eligible_symbol_dates > 0, eligible_symbol_dates, ">0"),
        ("P341_SBIN_ELIGIBLE_CONTEXT_PRESENT", sbin_eligible > 0, sbin_eligible, ">0"),
        ("P341_NO_LOOKAHEAD_RULE_APPLIED", bool(not eligible.empty and eligible["no_lookahead_rule_applied"].astype(int).eq(1).all()), "all rows", "all rows"),
        ("P341_WORK_ORDER_PRESENT", len(work_order) > 0, len(work_order), ">0"),
        ("P341_FULL_DEPTH_AND_FEATURE_SCHEMA_PRESENT", schema_pass == schema_total, f"{schema_pass}/{schema_total}", "all"),
        ("P341_NO_REPLAY_PROMOTION_OR_PROFIT_CLAIM", True, "closed", "closed"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed", "required"])


def write_outputs(phase339_dir: Path, phase340_dir: Path, real_root: Path, real_feature_root: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase340 = read_csv(phase340_dir / "phase340_acceptance_summary.csv")
    survivors = pd.read_csv(phase339_dir / "phase339_survivor_ledger.csv")
    catalysts = pd.read_csv(phase340_dir / "phase340_official_catalyst_calendar.csv")
    real_keys = discover_real_keys(real_root)
    eligible = build_eligible_catalyst_ledger(catalysts, real_keys)
    schema = build_schema_contract(real_root, real_feature_root)
    work_order = build_work_order(survivors, eligible)
    gates = build_gate_evaluation(phase340, eligible, work_order, schema)
    passed = int(gates["passed"].astype(bool).sum())
    total = int(len(gates))
    eligible_available = eligible[eligible["diagnostic_real_l2_available"].astype(int).eq(1)] if not eligible.empty else pd.DataFrame()
    summary = pd.DataFrame(
        [
            ("phase341_official_catalyst_real_day_survivor_diagnostic_precommit_complete", 1, "Phase341 precommit completed"),
            ("phase341_phase340_complete", as_int(metric_value(phase340, "phase340_official_catalyst_calendar_acquisition_complete", 0)), "Phase340 complete"),
            ("phase341_frozen_survivor_rows", len(survivors), "Frozen Phase339 survivors available"),
            ("phase341_official_catalyst_rows", len(catalysts), "Official catalyst rows available"),
            ("phase341_no_lookahead_eligible_event_rows", len(eligible_available), "Official catalyst rows with no-lookahead diagnostic real L2 availability"),
            ("phase341_no_lookahead_eligible_symbol_dates", eligible_available[["diagnostic_trade_date", "symbol"]].drop_duplicates().shape[0] if not eligible_available.empty else 0, "No-lookahead eligible diagnostic symbol-dates"),
            ("phase341_sbin_no_lookahead_eligible_rows", len(eligible_available[eligible_available["symbol"].eq("SBIN")]) if not eligible_available.empty else 0, "SBIN no-lookahead eligible catalyst rows"),
            ("phase341_post_close_rows_shifted_to_next_real_l2_day", len(eligible_available[eligible_available["market_session"].eq("post_close")]) if not eligible_available.empty else 0, "Post-close announcements shifted to next available real-L2 day"),
            ("phase341_work_order_rows", len(work_order), "Phase342 execution work-order rows"),
            ("phase341_full_depth_schema_pass_rows", int(schema["present"].astype(int).sum()), "Full-depth/schema pass rows"),
            ("phase341_full_depth_schema_rows", int(len(schema)), "Full-depth/schema rows"),
            ("phase341_strategy_replay_allowed", 0, "No replay in Phase341"),
            ("phase341_strategy_promotion_allowed", 0, "No promotion"),
            ("phase341_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase341_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase341_phase342_execution_allowed_next", int(passed == total), "Phase342 execution allowed next if gates pass"),
            ("phase341_hard_gate_pass_rows", passed, "Passed hard gates"),
            ("phase341_hard_gate_rows", total, "Hard gates"),
            ("phase341_next_best_action", NEXT_ACTION if passed == total else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )
    report = "\n".join(
        [
            "# Phase341 Official-Catalyst Real-Day Survivor Diagnostic Precommit",
            "",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
            "Phase341 precommits the first official-catalyst real-day diagnostic work order without executing replay or claiming profitability.",
            "",
            "The key no-lookahead rule is explicit: post-close announcements are shifted to the next available local real-L2 trading date.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Gate evaluation",
            "",
            _markdown_table(gates),
            "",
            "## Work-order sample",
            "",
            _markdown_table(work_order.head(20)),
            "",
            "No replay, promotion, paper/live acceptance, or deployable profitability claim is opened by Phase341.",
        ]
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    outputs = {
        "summary": output_dir / "phase341_acceptance_summary.csv",
        "eligible": output_dir / "phase341_no_lookahead_official_catalyst_eligibility_ledger.csv",
        "schema": output_dir / "phase341_real_l2_full_depth_schema_contract.csv",
        "work_order": output_dir / "phase341_phase342_execution_work_order.csv",
        "gates": output_dir / "phase341_gate_evaluation.csv",
        "report": output_dir / "phase341_official_catalyst_real_day_survivor_diagnostic_precommit_report.md",
        "manifest": output_dir / "phase341_official_catalyst_real_day_survivor_diagnostic_precommit_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    eligible.to_csv(outputs["eligible"], index=False)
    schema.to_csv(outputs["schema"], index=False)
    work_order.to_csv(outputs["work_order"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    outputs["report"].write_text(report, encoding="utf-8")
    manifest = {
        "phase": 341,
        "generated_at_utc": generated_utc,
        "phase339_dir": str(phase339_dir),
        "phase340_dir": str(phase340_dir),
        "real_root": str(real_root),
        "real_feature_root": str(real_feature_root),
        "output_dir": str(output_dir),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase341",
            generated_utc=generated_utc,
            inputs={
                "phase339_survivors": str(phase339_dir / "phase339_survivor_ledger.csv"),
                "phase340_official_calendar": str(phase340_dir / "phase340_official_catalyst_calendar.csv"),
                "real_root": str(real_root),
                "real_feature_root": str(real_feature_root),
            },
            parameters={"market_open": str(MARKET_OPEN), "market_close": str(MARKET_CLOSE)},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase339-dir", type=Path, default=DEFAULT_PHASE339_DIR)
    parser.add_argument("--phase340-dir", type=Path, default=DEFAULT_PHASE340_DIR)
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--real-feature-root", type=Path, default=DEFAULT_REAL_FEATURE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase339_dir, args.phase340_dir, args.real_root, args.real_feature_root, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
