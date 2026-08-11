from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

try:
    import truststore
except Exception:  # pragma: no cover - optional local TLS helper
    truststore = None

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE339_DIR = Path("outputs/phase339")
DEFAULT_REAL_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_OUTPUT_DIR = Path("outputs/phase340")

NEXT_ACTION = "run_phase341_official_catalyst_real_day_survivor_diagnostic_precommit_no_paper_live"
REPAIR_ACTION = "repair_phase340_official_catalyst_calendar_acquisition"

TICKERS = [
    "ADANIPORTS",
    "AXISBANK",
    "BAJAJ-AUTO",
    "BANKBEES",
    "BHARTIARTL",
    "BPCL",
    "BRITANNIA",
    "CIPLA",
    "DRREDDY",
    "GOLDBEES",
    "HCLTECH",
    "HDFCBANK",
    "HINDUNILVR",
    "ICICIBANK",
    "INFY",
    "ITBEES",
    "ITC",
    "JUNIORBEES",
    "KOTAKBANK",
    "LT",
    "M&M",
    "MARUTI",
    "NESTLEIND",
    "NIFTYBEES",
    "ONGC",
    "RELIANCE",
    "SBIN",
    "SUNPHARMA",
    "TCS",
    "TECHM",
    "ULTRACEMCO",
    "WIPRO",
]


def discover_local_real_dates(real_root: Path) -> list[str]:
    dates: set[str] = set()
    if real_root.exists():
        for path in real_root.rglob("*.parquet"):
            for part in path.parts:
                if part.startswith("trade_date="):
                    dates.add(part.split("=", 1)[1])
    return sorted(dates)


def build_source_catalog() -> pd.DataFrame:
    rows = [
        {
            "source_id": "NSE_CORPORATE_ANNOUNCEMENTS",
            "authority": "exchange_official",
            "url": "https://www.nseindia.com/companies-listing/corporate-filings-announcements",
            "api_template": "https://www.nseindia.com/api/corporate-announcements?index=equities&from_date={dd-mm-yyyy}&to_date={dd-mm-yyyy}",
            "role": "primary listed-company announcement source",
            "used_in_phase340": 1,
        },
        {
            "source_id": "NSE_FINANCIAL_RESULTS",
            "authority": "exchange_official",
            "url": "https://www.nseindia.com/companies-listing/corporate-filings-financial-results",
            "api_template": "https://www.nseindia.com/api/corporates-financial-results?index=equities&from_date={dd-mm-yyyy}&to_date={dd-mm-yyyy}",
            "role": "financial-results catalyst source",
            "used_in_phase340": 1,
        },
        {
            "source_id": "NSE_CORPORATE_ACTIONS",
            "authority": "exchange_official",
            "url": "https://www.nseindia.com/companies-listing/corporate-filings-actions",
            "api_template": "",
            "role": "corporate-action cross-check source",
            "used_in_phase340": 0,
        },
        {
            "source_id": "SEBI_CORPORATE_FILINGS_INDEX",
            "authority": "regulator_official",
            "url": "https://www.sebi.gov.in/curation/corporate_filings.html",
            "api_template": "",
            "role": "regulator-level routing/check source for NSE/BSE corporate filings",
            "used_in_phase340": 0,
        },
        {
            "source_id": "BSE_CORPORATE_ANNOUNCEMENTS",
            "authority": "exchange_official_cross_check",
            "url": "https://www.bseindia.com/corporates",
            "api_template": "",
            "role": "BSE cross-check for company announcements where available",
            "used_in_phase340": 0,
        },
    ]
    return pd.DataFrame(rows)


def nse_session() -> requests.Session:
    if truststore is not None:
        truststore.inject_into_ssl()
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json,text/plain,*/*",
            "Referer": "https://www.nseindia.com/companies-listing/corporate-filings-announcements",
        }
    )
    session.get("https://www.nseindia.com", timeout=25)
    return session


def fetch_nse_json(session: requests.Session, endpoint: str, date_text: str) -> tuple[list[dict], dict]:
    query_date = datetime.strptime(date_text, "%Y-%m-%d").strftime("%d-%m-%Y")
    url = endpoint.format(date=query_date)
    response = session.get(url, timeout=30)
    ledger = {
        "source_url": url,
        "trade_date": date_text,
        "http_status": response.status_code,
        "content_type": response.headers.get("content-type", ""),
        "response_bytes": len(response.content),
        "ok": int(response.status_code == 200),
    }
    if response.status_code != 200:
        return [], ledger
    try:
        data = response.json()
        if isinstance(data, list):
            return data, ledger
        return [], ledger
    except ValueError:
        ledger["ok"] = 0
        return [], ledger


def normalize_announcements(rows: list[dict], source_id: str, local_dates: list[str]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame(
            columns=[
                "source_id",
                "symbol",
                "announcement_time_ist",
                "announcement_date",
                "description",
                "text",
                "attachment_url",
                "seq_id",
                "same_day_real_l2_available",
                "ticker_in_universe",
            ]
        )
    frame = pd.DataFrame(rows)
    symbol = frame.get("symbol", pd.Series(dtype=str)).astype(str).str.upper()
    dt_text = frame.get("an_dt", pd.Series(dtype=str)).astype(str)
    out = pd.DataFrame(
        {
            "source_id": source_id,
            "symbol": symbol,
            "announcement_time_ist": dt_text,
            "announcement_date": pd.to_datetime(dt_text, format="%d-%b-%Y %H:%M:%S", errors="coerce").dt.strftime("%Y-%m-%d"),
            "description": frame.get("desc", pd.Series(dtype=str)).astype(str),
            "text": frame.get("attchmntText", pd.Series(dtype=str)).astype(str),
            "attachment_url": frame.get("attchmntFile", pd.Series(dtype=str)).astype(str),
            "seq_id": frame.get("seq_id", pd.Series(dtype=str)).astype(str),
        }
    )
    out["same_day_real_l2_available"] = out["announcement_date"].isin(local_dates).astype(int)
    out["ticker_in_universe"] = out["symbol"].isin(TICKERS).astype(int)
    return out[out["ticker_in_universe"].eq(1)].sort_values(["announcement_date", "symbol", "announcement_time_ist"]).reset_index(drop=True)


def build_overlap(catalysts: pd.DataFrame, real_root: Path) -> pd.DataFrame:
    real_keys: set[tuple[str, str]] = set()
    if real_root.exists():
        for path in real_root.rglob("*.parquet"):
            date = ""
            symbol = ""
            for part in path.parts:
                if part.startswith("trade_date="):
                    date = part.split("=", 1)[1]
                if part.startswith("symbol="):
                    symbol = part.split("=", 1)[1].upper()
            if date and symbol:
                real_keys.add((date, symbol))
    real = pd.DataFrame(sorted(real_keys), columns=["trade_date", "symbol"]) if real_keys else pd.DataFrame(columns=["trade_date", "symbol"])
    if catalysts.empty:
        return pd.DataFrame(columns=["announcement_date", "symbol", "official_catalyst_rows", "real_l2_same_day"])
    grouped = catalysts.groupby(["announcement_date", "symbol"], dropna=False).size().reset_index(name="official_catalyst_rows")
    grouped = grouped.rename(columns={"announcement_date": "trade_date"})
    overlap = grouped.merge(real.assign(real_l2_same_day=1), on=["trade_date", "symbol"], how="left")
    overlap["real_l2_same_day"] = overlap["real_l2_same_day"].fillna(0).astype(int)
    return overlap.sort_values(["trade_date", "symbol"]).reset_index(drop=True)


def build_phase341_contract() -> pd.DataFrame:
    rows = [
        ("input_official_calendar", "outputs/phase340/phase340_official_catalyst_calendar.csv", "Use official NSE announcements/results rows only; synthetic labels are not catalyst truth."),
        ("input_survivors", "outputs/phase339/phase339_survivor_ledger.csv", "Use frozen Phase339 survivors only; no new alpha search."),
        ("real_l2_root", "real_data_sample/l2_multiday_panel", "Use local downloaded Zerodha WebSocket top-five L2 data first to protect disk."),
        ("same_day_alignment", "required", "A catalyst diagnostic row requires same trade_date and symbol in official calendar and real L2."),
        ("sbin_context", "required_if_available", "Report SBIN catalyst rows separately because the user explicitly asked for SBI catalyst context."),
        ("full_top_five_depth_required", 1, "Use bid/ask price/quantity/order count levels 1-5; no L1-only shortcut."),
        ("levels_2_to_5_materiality_required", 1, "Feature contribution from levels beyond best bid/ask must be logged."),
        ("fixed_capital_denominator", "required", "Annualized return must use fixed capital, not unlimited capital."),
        ("annualized_threshold_pct", 12.0, "Keep the user's profitability threshold."),
        ("robust_event_floor", 30, "Treat sparse fewer-than-30 event results as diagnostic only."),
        ("cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Keep Zerodha all-in cost model."),
        ("cost_profile_required", "zerodha_2x_all_in_cost_proxy", "Use 2x cost stress."),
        ("passive_aware_route_status", "diagnostic_failed_not_primary_rescue", "Do not rescue with passive-aware assumptions."),
        ("paper_or_live_allowed", 0, "No paper/live acceptance from this diagnostic."),
        ("deployable_profitability_claim_allowed", 0, "No deployable claim from same-day official catalyst diagnostic."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_gate_evaluation(phase339: pd.DataFrame, catalysts: pd.DataFrame, overlap: pd.DataFrame, source_ledger: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    phase339_complete = as_int(metric_value(phase339, "phase339_cost_stress_holdout_validation_interpretation_complete", 0))
    nse_ok_dates = int(source_ledger[source_ledger["source_id"].eq("NSE_CORPORATE_ANNOUNCEMENTS")]["ok"].sum()) if not source_ledger.empty else 0
    local_dates = int(source_ledger["trade_date"].nunique()) if not source_ledger.empty else 0
    same_day_rows = int(overlap["real_l2_same_day"].sum()) if not overlap.empty else 0
    sbin_rows = int(len(catalysts[catalysts["symbol"].eq("SBIN")])) if not catalysts.empty else 0
    rows = [
        ("P340_PHASE339_COMPLETE", phase339_complete == 1, phase339_complete, 1),
        ("P340_OFFICIAL_NSE_ANNOUNCEMENTS_FETCHED", nse_ok_dates == local_dates and local_dates > 0, f"{nse_ok_dates}/{local_dates}", "all local dates"),
        ("P340_OFFICIAL_CATALYST_ROWS_PRESENT", len(catalysts) > 0, len(catalysts), ">0"),
        ("P340_SAME_DAY_REAL_L2_OVERLAP_PRESENT", same_day_rows > 0, same_day_rows, ">0"),
        ("P340_SBIN_OFFICIAL_CONTEXT_PRESENT", sbin_rows > 0, sbin_rows, ">0"),
        ("P340_SOURCE_CATALOG_PRESENT", True, "NSE/SEBI/BSE cataloged", "present"),
        ("P340_PHASE341_CONTRACT_PRESENT", len(contract) >= 12, len(contract), ">=12"),
        ("P340_NO_REPLAY_PROMOTION_OR_PROFIT_CLAIM", True, "closed", "closed"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed", "required"])


def write_outputs(phase339_dir: Path, real_root: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase339 = read_csv(phase339_dir / "phase339_acceptance_summary.csv")
    local_dates = discover_local_real_dates(real_root)
    source_catalog = build_source_catalog()
    session = nse_session()
    endpoints = {
        "NSE_CORPORATE_ANNOUNCEMENTS": "https://www.nseindia.com/api/corporate-announcements?index=equities&from_date={date}&to_date={date}",
        "NSE_FINANCIAL_RESULTS": "https://www.nseindia.com/api/corporates-financial-results?index=equities&from_date={date}&to_date={date}",
    }
    source_rows: list[dict] = []
    catalyst_frames: list[pd.DataFrame] = []
    for source_id, endpoint in endpoints.items():
        for date_text in local_dates:
            rows, ledger = fetch_nse_json(session, endpoint, date_text)
            ledger["source_id"] = source_id
            source_rows.append(ledger)
            catalyst_frames.append(normalize_announcements(rows, source_id, local_dates))
    catalysts = pd.concat(catalyst_frames, ignore_index=True) if catalyst_frames else pd.DataFrame()
    if not catalysts.empty:
        catalysts = catalysts.drop_duplicates(["source_id", "symbol", "announcement_time_ist", "seq_id", "text"]).reset_index(drop=True)
    source_ledger = pd.DataFrame(source_rows)
    overlap = build_overlap(catalysts, real_root)
    contract = build_phase341_contract()
    gates = build_gate_evaluation(phase339, catalysts, overlap, source_ledger, contract)
    passed = int(gates["passed"].astype(bool).sum())
    total = int(len(gates))
    sbin = catalysts[catalysts["symbol"].eq("SBIN")] if not catalysts.empty else pd.DataFrame()
    summary = pd.DataFrame(
        [
            ("phase340_official_catalyst_calendar_acquisition_complete", 1, "Phase340 completed"),
            ("phase340_local_real_l2_date_rows", len(local_dates), "Local real L2 dates scanned"),
            ("phase340_nse_announcement_source_ok_dates", int(source_ledger[source_ledger["source_id"].eq("NSE_CORPORATE_ANNOUNCEMENTS")]["ok"].sum()), "NSE announcement fetch OK dates"),
            ("phase340_official_catalyst_rows", len(catalysts), "Official catalyst rows for ticker universe and local dates"),
            ("phase340_official_catalyst_symbols", catalysts["symbol"].nunique() if not catalysts.empty else 0, "Symbols with official catalyst rows"),
            ("phase340_same_day_real_l2_catalyst_symbol_dates", int(overlap["real_l2_same_day"].sum()) if not overlap.empty else 0, "Official catalyst symbol-dates with same-day local real L2"),
            ("phase340_sbin_official_catalyst_rows", len(sbin), "SBIN official catalyst rows"),
            ("phase340_sbin_official_catalyst_dates", ";".join(sorted(sbin["announcement_date"].dropna().unique().tolist())) if not sbin.empty else "", "SBIN official catalyst dates"),
            ("phase340_strategy_replay_allowed", 0, "No replay"),
            ("phase340_strategy_promotion_allowed", 0, "No promotion"),
            ("phase340_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase340_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase340_hard_gate_pass_rows", passed, "Passed hard gates"),
            ("phase340_hard_gate_rows", total, "Hard gates"),
            ("phase340_next_best_action", NEXT_ACTION if passed == total else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )
    report = "\n".join(
        [
            "# Phase340 Official Catalyst Calendar Acquisition",
            "",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
            "Phase340 acquires official NSE catalyst rows for the local real-L2 dates and records SEBI/BSE as regulator/cross-check sources before any real-day strategy diagnostic.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Gate evaluation",
            "",
            _markdown_table(gates),
            "",
            "## SBIN official catalyst context",
            "",
            _markdown_table(sbin[["source_id", "symbol", "announcement_time_ist", "description", "text"]].head(20) if not sbin.empty else pd.DataFrame()),
            "",
            "No replay, promotion, paper/live acceptance, or deployable profitability claim is opened by Phase340.",
        ]
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "phase": 340,
        "generated_at_utc": generated_utc,
        "phase339_dir": str(phase339_dir),
        "real_root": str(real_root),
        "output_dir": str(output_dir),
        "local_real_dates": local_dates,
        "ticker_count": len(TICKERS),
        "outputs": {},
        "reproducibility": reproducibility_fields(
            artifact_id="phase340",
            generated_utc=generated_utc,
            inputs={
                "phase339_acceptance": str(phase339_dir / "phase339_acceptance_summary.csv"),
                "real_root": str(real_root),
            },
            parameters={
                "ticker_count": len(TICKERS),
                "local_real_dates": local_dates,
                "official_sources": ["NSE_CORPORATE_ANNOUNCEMENTS", "NSE_FINANCIAL_RESULTS"],
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
    }
    outputs = {
        "summary": output_dir / "phase340_acceptance_summary.csv",
        "source_catalog": output_dir / "phase340_official_source_catalog.csv",
        "source_response_ledger": output_dir / "phase340_official_source_response_ledger.csv",
        "calendar": output_dir / "phase340_official_catalyst_calendar.csv",
        "overlap": output_dir / "phase340_official_catalyst_real_l2_overlap.csv",
        "contract": output_dir / "phase340_phase341_real_day_survivor_diagnostic_contract.csv",
        "gates": output_dir / "phase340_gate_evaluation.csv",
        "report": output_dir / "phase340_official_catalyst_calendar_acquisition_report.md",
        "manifest": output_dir / "phase340_official_catalyst_calendar_acquisition_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    source_catalog.to_csv(outputs["source_catalog"], index=False)
    source_ledger.to_csv(outputs["source_response_ledger"], index=False)
    catalysts.to_csv(outputs["calendar"], index=False)
    overlap.to_csv(outputs["overlap"], index=False)
    contract.to_csv(outputs["contract"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    outputs["report"].write_text(report, encoding="utf-8")
    manifest["outputs"] = {key: str(value) for key, value in outputs.items()}
    outputs["manifest"].write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase339-dir", type=Path, default=DEFAULT_PHASE339_DIR)
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase339_dir, args.real_root, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
