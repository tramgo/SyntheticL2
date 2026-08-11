from __future__ import annotations

import argparse
import json
from datetime import datetime, time, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase340_official_catalyst_calendar_acquisition_precommit import (
    TICKERS,
    build_source_catalog,
    fetch_nse_json,
    normalize_announcements,
    nse_session,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_EXISTING_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_UNSEEN_ROOT = Path("real_data_sample/l2_unseen_validation")
DEFAULT_PHASE357_DIR = Path("outputs/phase357")
DEFAULT_OUTPUT_DIR = Path("outputs/phase359")

MARKET_OPEN = time(9, 15)
MARKET_CLOSE = time(15, 30)
PRIMARY_SCENARIO_ID = "P356_CONTROL_DEPTH_2_5_FADE_VARIANT"
NEXT_ACTION = "run_phase360_full_depth_market_neutral_fade_on_unseen_real_l2_no_paper_live"
REPAIR_ACTION = "repair_phase359_unseen_catalyst_or_full_depth_inputs_no_paper_live"


def discover_real_keys(real_root: Path) -> pd.DataFrame:
    rows: set[tuple[str, str, int, int]] = set()
    if real_root.exists():
        for symbol_dir in real_root.glob("trade_date=*/exchange=NSE/symbol=*"):
            if not symbol_dir.is_dir():
                continue
            trade_date = ""
            symbol = ""
            for part in symbol_dir.parts:
                if part.startswith("trade_date="):
                    trade_date = part.split("=", 1)[1]
                if part.startswith("symbol="):
                    symbol = part.split("=", 1)[1].upper()
            files = list(symbol_dir.glob("*.parquet"))
            if trade_date and symbol:
                rows.add((trade_date, symbol, len(files), int(sum(p.stat().st_size for p in files))))
    columns = ["trade_date", "symbol", "parquet_files", "bytes"]
    return pd.DataFrame(sorted(rows), columns=columns) if rows else pd.DataFrame(columns=columns)


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def fetch_official_catalysts(local_dates: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    source_rows: list[dict[str, Any]] = []
    catalyst_frames: list[pd.DataFrame] = []
    endpoints = {
        "NSE_CORPORATE_ANNOUNCEMENTS": "https://www.nseindia.com/api/corporate-announcements?index=equities&from_date={date}&to_date={date}",
        "NSE_FINANCIAL_RESULTS": "https://www.nseindia.com/api/corporates-financial-results?index=equities&from_date={date}&to_date={date}",
    }
    try:
        session = nse_session()
        for source_id, endpoint in endpoints.items():
            for date_text in local_dates:
                rows, ledger = fetch_nse_json(session, endpoint, date_text)
                ledger["source_id"] = source_id
                source_rows.append(ledger)
                catalyst_frames.append(normalize_announcements(rows, source_id, local_dates))
    except Exception as exc:  # pragma: no cover - network environment dependent
        source_rows.append(
            {
                "source_url": "nse_session_or_fetch",
                "trade_date": ";".join(local_dates),
                "http_status": 0,
                "content_type": "",
                "response_bytes": 0,
                "ok": 0,
                "source_id": "NSE_FETCH_EXCEPTION",
                "error_type": type(exc).__name__,
                "error_text": str(exc)[:240],
            }
        )
    catalysts = pd.concat(catalyst_frames, ignore_index=True) if catalyst_frames else pd.DataFrame()
    if not catalysts.empty:
        catalysts = catalysts.drop_duplicates(["source_id", "symbol", "announcement_time_ist", "seq_id", "text"]).reset_index(drop=True)
    source_ledger = pd.DataFrame(source_rows)
    return catalysts, source_ledger


def classify_session(ts: pd.Timestamp) -> str:
    if pd.isna(ts):
        return "unknown"
    t = ts.time()
    if t < MARKET_OPEN:
        return "pre_open_or_overnight"
    if t <= MARKET_CLOSE:
        return "regular_session"
    return "post_close"


def build_no_lookahead_eligibility(catalysts: pd.DataFrame, real_keys: pd.DataFrame) -> pd.DataFrame:
    if catalysts.empty:
        return pd.DataFrame(
            columns=[
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
        )
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
            "post_close": "market_open_next_available_unseen_real_l2_day",
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


def build_full_depth_schema(unseen_root: Path) -> pd.DataFrame:
    required = ["collector_received_utc_ms", "exchange_timestamp", "last_price"]
    for side in ["buy", "sell"]:
        for level in range(1, 6):
            required.extend([f"{side}_{level}_price", f"{side}_{level}_quantity", f"{side}_{level}_orders"])
    sample = next(unseen_root.rglob("*.parquet"), None) if unseen_root.exists() else None
    columns: set[str] = set()
    sample_path = ""
    if sample is not None:
        sample_path = str(sample)
        columns = set(pd.read_parquet(sample).columns)
    rows = [
        {
            "source": "unseen_raw_real_l2",
            "sample_path": sample_path,
            "column": col,
            "required": 1,
            "present": int(col in columns),
            "purpose": "full top-five market-by-price diagnostic input",
        }
        for col in required
    ]
    rows.extend(
        [
            {
                "source": "diagnostic_policy",
                "sample_path": "",
                "column": "levels_2_to_5_materiality_required",
                "required": 1,
                "present": 1,
                "purpose": "forbid L1-only reinterpretation",
            },
            {
                "source": "diagnostic_policy",
                "sample_path": "",
                "column": "fixed_capital_denominator_required",
                "required": 1,
                "present": 1,
                "purpose": "avoid unlimited-capital return math",
            },
            {
                "source": "diagnostic_policy",
                "sample_path": "",
                "column": "zerodha_2x_all_in_cost_proxy_required",
                "required": 1,
                "present": 1,
                "purpose": "preserve cost200 hurdle",
            },
        ]
    )
    return pd.DataFrame(rows)


def build_phase360_work_order(eligible: pd.DataFrame, phase357_contract: pd.DataFrame) -> pd.DataFrame:
    eligible_rows = eligible[eligible["diagnostic_real_l2_available"].astype(int).eq(1)].copy() if not eligible.empty else pd.DataFrame()
    family_id = "P357_FULL_DEPTH_MARKET_NEUTRAL_FADE"
    if not phase357_contract.empty and "family_id" in phase357_contract.columns:
        family_id = str(phase357_contract["family_id"].iloc[0])
    rows = []
    for row in eligible_rows.itertuples(index=False):
        rows.append(
            {
                "phase360_work_order_id": f"P359_{row.diagnostic_trade_date}_{row.symbol}_{row.seq_id}",
                "family_id": family_id,
                "primary_scenario_id": PRIMARY_SCENARIO_ID,
                "source_id": row.source_id,
                "symbol": row.symbol,
                "announcement_time_ist": row.announcement_time_ist,
                "announcement_date": row.announcement_date,
                "market_session": row.market_session,
                "diagnostic_trade_date": row.diagnostic_trade_date,
                "diagnostic_start_rule": row.diagnostic_start_rule,
                "description": row.description,
                "no_lookahead_rule_applied": row.no_lookahead_rule_applied,
                "full_depth_levels_1_to_5_required": 1,
                "levels_2_to_5_materiality_required": 1,
                "cost_profile": "zerodha_2x_all_in_cost_proxy",
                "paper_live_or_profit_claim_allowed": 0,
            }
        )
    return pd.DataFrame(rows)


def build_gates(existing_keys: pd.DataFrame, unseen_keys: pd.DataFrame, catalysts: pd.DataFrame, source_ledger: pd.DataFrame, eligible: pd.DataFrame, schema: pd.DataFrame, work_order: pd.DataFrame) -> pd.DataFrame:
    existing_dates = set(existing_keys["trade_date"].astype(str)) if not existing_keys.empty else set()
    unseen_dates = set(unseen_keys["trade_date"].astype(str)) if not unseen_keys.empty else set()
    new_dates = sorted(unseen_dates - existing_dates)
    schema_pass = int(schema["present"].astype(int).sum()) if not schema.empty else 0
    schema_total = int(len(schema))
    ok_fetches = int(source_ledger["ok"].fillna(0).astype(int).sum()) if "ok" in source_ledger.columns and not source_ledger.empty else 0
    eligible_rows = int(eligible["diagnostic_real_l2_available"].sum()) if not eligible.empty else 0
    gates = [
        ("P359_UNSEEN_LOCAL_DATES_PRESENT", len(new_dates) > 0, ";".join(new_dates), ">0 new dates"),
        ("P359_FULL_UNIVERSE_SYMBOLS_PRESENT", unseen_keys["symbol"].nunique() >= len(TICKERS) if not unseen_keys.empty else False, unseen_keys["symbol"].nunique() if not unseen_keys.empty else 0, f">={len(TICKERS)}"),
        ("P359_OFFICIAL_NSE_FETCH_ATTEMPTED", len(source_ledger) > 0, len(source_ledger), ">0"),
        ("P359_OFFICIAL_NSE_FETCH_OK", ok_fetches > 0, ok_fetches, ">0"),
        ("P359_OFFICIAL_CATALYST_ROWS_PRESENT", len(catalysts) > 0, len(catalysts), ">0"),
        ("P359_NO_LOOKAHEAD_ELIGIBLE_EVENTS_PRESENT", eligible_rows > 0, eligible_rows, ">0"),
        ("P359_FULL_DEPTH_SCHEMA_PRESENT", schema_pass == schema_total, f"{schema_pass}/{schema_total}", "all"),
        ("P359_PHASE360_WORK_ORDER_PRESENT", len(work_order) > 0, len(work_order), ">0"),
        ("P359_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", True, "closed", "closed"),
    ]
    return pd.DataFrame(gates, columns=["gate_id", "passed", "observed", "required"])


def write_outputs(existing_root: Path, unseen_root: Path, phase357_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    existing_keys = discover_real_keys(existing_root)
    unseen_keys = discover_real_keys(unseen_root)
    existing_dates = set(existing_keys["trade_date"].astype(str)) if not existing_keys.empty else set()
    unseen_dates = sorted(set(unseen_keys["trade_date"].astype(str)) - existing_dates) if not unseen_keys.empty else []
    catalysts, source_ledger = fetch_official_catalysts(unseen_dates)
    source_catalog = build_source_catalog()
    eligible = build_no_lookahead_eligibility(catalysts, unseen_keys)
    schema = build_full_depth_schema(unseen_root)
    phase357_contract = read_csv(phase357_dir / "phase357_family_contract.csv")
    work_order = build_phase360_work_order(eligible, phase357_contract)
    gates = build_gates(existing_keys, unseen_keys, catalysts, source_ledger, eligible, schema, work_order)
    passed = int(gates["passed"].astype(bool).sum())
    total = int(len(gates))
    eligible_available = eligible[eligible["diagnostic_real_l2_available"].astype(int).eq(1)] if not eligible.empty else pd.DataFrame()
    summary = pd.DataFrame(
        [
            ("phase359_local_unseen_real_l2_catalyst_expansion_complete", int(passed == total), "Phase359 completed if all hard gates pass"),
            ("phase359_existing_real_l2_dates", len(existing_dates), "Existing multiday local real L2 dates"),
            ("phase359_unseen_real_l2_dates", len(unseen_dates), "New unseen local real L2 dates detected"),
            ("phase359_unseen_date_list", ";".join(unseen_dates), "Unseen date list"),
            ("phase359_unseen_symbol_date_rows", len(unseen_keys), "Unseen symbol/date rows"),
            ("phase359_unseen_symbols", unseen_keys["symbol"].nunique() if not unseen_keys.empty else 0, "Unseen symbols"),
            ("phase359_official_source_response_rows", len(source_ledger), "Official source response rows"),
            ("phase359_official_source_ok_rows", int(source_ledger["ok"].fillna(0).astype(int).sum()) if "ok" in source_ledger.columns and not source_ledger.empty else 0, "Official source OK rows"),
            ("phase359_official_catalyst_rows", len(catalysts), "Official catalyst rows for unseen dates"),
            ("phase359_official_catalyst_symbols", catalysts["symbol"].nunique() if not catalysts.empty else 0, "Official catalyst symbols"),
            ("phase359_no_lookahead_eligible_event_rows", len(eligible_available), "No-lookahead eligible events with unseen real L2"),
            ("phase359_no_lookahead_eligible_symbol_dates", eligible_available[["diagnostic_trade_date", "symbol"]].drop_duplicates().shape[0] if not eligible_available.empty else 0, "Eligible symbol/date cells"),
            ("phase359_phase360_work_order_rows", len(work_order), "Phase360 work-order rows"),
            ("phase359_full_depth_schema_pass_rows", int(schema["present"].astype(int).sum()) if not schema.empty else 0, "Schema pass rows"),
            ("phase359_full_depth_schema_rows", len(schema), "Schema rows"),
            ("phase359_strategy_promotion_allowed", 0, "No promotion"),
            ("phase359_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase359_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase359_hard_gate_pass_rows", passed, "Passed hard gates"),
            ("phase359_hard_gate_rows", total, "Hard gates"),
            ("phase359_next_best_action", NEXT_ACTION if passed == total else REPAIR_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    inventory = unseen_keys.sort_values(["trade_date", "symbol"]).reset_index(drop=True)
    report = "\n".join(
        [
            "# Phase359 Local Unseen Real L2 Catalyst Expansion",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase359 registers local unseen real L2 dates already present on disk, fetches official NSE catalyst rows for those dates, applies no-lookahead eligibility, verifies full L1-L5 market-by-price schema, and emits a Phase360 work order. It does not download more data and does not open promotion, paper/live, or profitability claims.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Gate evaluation",
            "",
            _markdown_table(gates),
            "",
            "## Unseen date inventory",
            "",
            _markdown_table(inventory.groupby("trade_date", as_index=False).agg(symbols=("symbol", "nunique"), parquet_files=("parquet_files", "sum"), bytes=("bytes", "sum")) if not inventory.empty else pd.DataFrame()),
            "",
            "## No-lookahead eligible events",
            "",
            _markdown_table(eligible_available.head(50) if not eligible_available.empty else pd.DataFrame()),
            "",
            "No promotion, paper/live acceptance, or deployable profitability claim is opened.",
        ]
    )
    outputs = {
        "summary": output_dir / "phase359_acceptance_summary.csv",
        "inventory": output_dir / "phase359_local_unseen_real_l2_inventory.csv",
        "source_catalog": output_dir / "phase359_official_source_catalog.csv",
        "source_response_ledger": output_dir / "phase359_official_source_response_ledger.csv",
        "calendar": output_dir / "phase359_official_catalyst_calendar.csv",
        "eligibility": output_dir / "phase359_no_lookahead_official_catalyst_eligibility.csv",
        "schema": output_dir / "phase359_full_depth_schema_contract.csv",
        "work_order": output_dir / "phase359_phase360_execution_work_order.csv",
        "gates": output_dir / "phase359_gate_evaluation.csv",
        "report": output_dir / "phase359_local_unseen_real_l2_catalyst_expansion_report.md",
        "manifest": output_dir / "phase359_local_unseen_real_l2_catalyst_expansion_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    inventory.to_csv(outputs["inventory"], index=False)
    source_catalog.to_csv(outputs["source_catalog"], index=False)
    source_ledger.to_csv(outputs["source_response_ledger"], index=False)
    catalysts.to_csv(outputs["calendar"], index=False)
    eligible.to_csv(outputs["eligibility"], index=False)
    schema.to_csv(outputs["schema"], index=False)
    work_order.to_csv(outputs["work_order"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    outputs["report"].write_text(report + "\n", encoding="utf-8")
    manifest = {
        "phase": 359,
        "generated_at_utc": generated_utc,
        "existing_root": str(existing_root),
        "unseen_root": str(unseen_root),
        "phase357_dir": str(phase357_dir),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase359_local_unseen_real_l2_catalyst_expansion",
            generated_utc=generated_utc,
            inputs={"existing_root": str(existing_root), "unseen_root": str(unseen_root), "phase357_dir": str(phase357_dir)},
            parameters={"primary_scenario_id": PRIMARY_SCENARIO_ID, "official_sources": ["NSE_CORPORATE_ANNOUNCEMENTS", "NSE_FINANCIAL_RESULTS"]},
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": str(summary[summary["metric"].eq("phase359_next_best_action")]["value"].iloc[0]),
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--existing-root", type=Path, default=DEFAULT_EXISTING_ROOT)
    parser.add_argument("--unseen-root", type=Path, default=DEFAULT_UNSEEN_ROOT)
    parser.add_argument("--phase357-dir", type=Path, default=DEFAULT_PHASE357_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.existing_root, args.unseen_root, args.phase357_dir, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
