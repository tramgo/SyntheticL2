from __future__ import annotations

import argparse
import json
import os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase340_official_catalyst_calendar_acquisition_precommit import TICKERS
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_EXISTING_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_UNSEEN_ROOT = Path("real_data_sample/l2_unseen_validation")
DEFAULT_OUTPUT_DIR = Path("outputs/phase370")
SUPPORTED_SAS_ENV_NAMES = [
    "AZURE_STORAGE_SAS_TOKEN",
    "AZURE_BLOB_SERVICE_SAS_URL",
    "STCTRADE1RAMIC_BLOB_SAS_URL",
    "STCTRADE1RAMIC_SAS_TOKEN",
]


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def next_weekday(value: str) -> str:
    dt = date.fromisoformat(value) + timedelta(days=1)
    while dt.weekday() >= 5:
        dt += timedelta(days=1)
    return dt.isoformat()


def discover_real_keys(root: Path) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if not root.exists():
        return pd.DataFrame(columns=["root", "trade_date", "symbol", "parquet_files", "bytes"])
    for symbol_dir in root.glob("trade_date=*/exchange=NSE/symbol=*"):
        if not symbol_dir.is_dir():
            continue
        trade_date = ""
        symbol = ""
        for part in symbol_dir.parts:
            if part.startswith("trade_date="):
                trade_date = part.split("=", 1)[1]
            elif part.startswith("symbol="):
                symbol = part.split("=", 1)[1].upper()
        files = list(symbol_dir.glob("*.parquet"))
        if trade_date and symbol:
            rows.append(
                {
                    "root": str(root),
                    "trade_date": trade_date,
                    "symbol": symbol,
                    "parquet_files": len(files),
                    "bytes": int(sum(path.stat().st_size for path in files)),
                }
            )
    return pd.DataFrame(rows, columns=["root", "trade_date", "symbol", "parquet_files", "bytes"])


def build_date_inventory(keys: pd.DataFrame) -> pd.DataFrame:
    if keys.empty:
        return pd.DataFrame(columns=["trade_date", "symbols", "parquet_files", "bytes", "full_universe"])
    grouped = (
        keys.groupby("trade_date", as_index=False)
        .agg(symbols=("symbol", "nunique"), parquet_files=("parquet_files", "sum"), bytes=("bytes", "sum"))
        .sort_values("trade_date")
    )
    grouped["full_universe"] = (grouped["symbols"].astype(int) >= len(TICKERS)).astype(int)
    return grouped


def write_outputs(existing_root: Path, unseen_root: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()

    phase369 = read_csv(Path("outputs/phase369/phase369_acceptance_summary.csv"))
    phase359_elig = read_csv(Path("outputs/phase359/phase359_no_lookahead_official_catalyst_eligibility.csv"))
    phase359_inventory = read_csv(Path("outputs/phase359/phase359_local_unseen_real_l2_inventory.csv"))
    if phase369.empty or phase359_elig.empty or phase359_inventory.empty:
        raise FileNotFoundError("Phase370 requires Phase369 and Phase359 artifacts")

    existing_keys = discover_real_keys(existing_root)
    unseen_keys = discover_real_keys(unseen_root)
    local_keys = pd.concat([existing_keys, unseen_keys], ignore_index=True)
    date_inventory = build_date_inventory(local_keys)

    known_phase359_dates = sorted(phase359_inventory["trade_date"].dropna().astype(str).unique().tolist())
    post_close_unmapped = phase359_elig[
        phase359_elig["market_session"].astype(str).eq("post_close")
        & phase359_elig["diagnostic_trade_date"].fillna("").astype(str).eq("")
    ].copy()
    if not post_close_unmapped.empty:
        latest_announcement_date = sorted(post_close_unmapped["announcement_date"].dropna().astype(str).unique().tolist())[-1]
        target_trade_date = next_weekday(latest_announcement_date)
    else:
        latest_known = sorted(known_phase359_dates)[-1]
        target_trade_date = next_weekday(latest_known)

    target_symbols = sorted(post_close_unmapped["symbol"].dropna().astype(str).unique().tolist()) if not post_close_unmapped.empty else TICKERS
    target_rows = len(post_close_unmapped)
    target_local = local_keys[local_keys["trade_date"].astype(str).eq(target_trade_date)].copy() if not local_keys.empty else pd.DataFrame()
    target_symbol_count = int(target_local["symbol"].nunique()) if not target_local.empty else 0
    target_full_universe_present = int(target_symbol_count >= len(TICKERS))
    target_file_rows = int(target_local["parquet_files"].sum()) if not target_local.empty else 0
    target_bytes = int(target_local["bytes"].sum()) if not target_local.empty else 0

    current_work_rows = as_int(metric_value(phase369, "phase369_current_no_lookahead_work_rows"))
    current_selected_trades = as_int(metric_value(phase369, "phase369_phase366_selected_trades"))
    selected_yield = current_selected_trades / current_work_rows if current_work_rows else 0.0
    estimated_selected_from_target = target_rows * selected_yield
    estimated_selected_after_one_day = current_selected_trades + estimated_selected_from_target
    event_floor_after_one_day = int(estimated_selected_after_one_day >= 30)

    sas_env_present_names = [name for name in SUPPORTED_SAS_ENV_NAMES if os.environ.get(name)]
    sas_env_present = int(bool(sas_env_present_names))

    target_contract = pd.DataFrame(
        [
            {
                "contract_id": "P370_PRIMARY_ONE_DAY_TARGET",
                "target_trade_date": target_trade_date,
                "target_symbols": ";".join(target_symbols),
                "full_universe_required": 1,
                "expected_partition_shape": "real_data_sample/l2_unseen_validation/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet",
                "known_carry_forward_event_rows_if_added": target_rows,
                "acceptance_retest_allowed_after_this_one_day": 0,
            },
            {
                "contract_id": "P370_VERIFY_ONLY_NO_SECRET_PERSISTENCE",
                "target_trade_date": target_trade_date,
                "target_symbols": "ALL_32_REQUIRED",
                "full_universe_required": 1,
                "expected_partition_shape": "raw_l2/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet or local unseen validation equivalent",
                "known_carry_forward_event_rows_if_added": target_rows,
                "acceptance_retest_allowed_after_this_one_day": 0,
            },
        ]
    )

    verifier = pd.DataFrame(
        [
            {
                "check_id": "P370_TARGET_DATE_LOCAL_PRESENT",
                "passed": int(target_symbol_count > 0),
                "observed": f"symbols={target_symbol_count}; files={target_file_rows}; bytes={target_bytes}",
                "required": ">=1 symbol for partial verify; 32 symbols for full-universe",
            },
            {
                "check_id": "P370_TARGET_DATE_FULL_UNIVERSE",
                "passed": target_full_universe_present,
                "observed": f"symbols={target_symbol_count}/{len(TICKERS)}",
                "required": f"{len(TICKERS)} symbols",
            },
            {
                "check_id": "P370_KNOWN_CARRY_FORWARD_EVENTS",
                "passed": int(target_rows > 0),
                "observed": target_rows,
                "required": ">0 known post-close catalyst rows from previous local day",
            },
            {
                "check_id": "P370_ONE_DAY_STILL_BELOW_EVENT_FLOOR",
                "passed": int(event_floor_after_one_day == 0),
                "observed": f"estimated_selected_after_one_day={estimated_selected_after_one_day:.3f}",
                "required": "<30 means no acceptance retest yet",
            },
            {
                "check_id": "P370_SAS_ENV_PRESENT_NOW",
                "passed": sas_env_present,
                "observed": f"supported_env_names_present={len(sas_env_present_names)}",
                "required": "1 for direct SAS download in this shell",
            },
        ]
    )

    gates = pd.DataFrame(
        [
            ("P370_PHASE369_COMPLETE", int(as_int(metric_value(phase369, "phase369_official_catalyst_real_l2_expansion_readiness_complete")) == 1), "Phase369 complete"),
            ("P370_TARGET_DATE_SELECTED", int(bool(target_trade_date)), target_trade_date),
            ("P370_LOCAL_ROOTS_SCANNED", 1, f"roots={existing_root};{unseen_root}"),
            ("P370_FULL_UNIVERSE_REQUIREMENT_RETAINED", 1, f"required_symbols={len(TICKERS)}"),
            ("P370_NO_ACCEPTANCE_RETEST_ON_ONE_DAY_TARGET", int(event_floor_after_one_day == 0), f"estimated_selected_after_one_day={estimated_selected_after_one_day:.3f}"),
            ("P370_NO_SECRET_MATERIAL_RECORDED", 1, "only env presence flags recorded"),
            ("P370_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "closed"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )

    summary = pd.DataFrame(
        [
            ("phase370_one_day_real_l2_drop_verifier_complete", int(gates["passed"].astype(int).all()), "Phase370 complete if all hard gates pass"),
            ("phase370_target_trade_date", target_trade_date, "Primary one-day target"),
            ("phase370_target_known_carry_forward_event_rows", target_rows, "Known post-close events that become eligible if target day exists"),
            ("phase370_target_symbols_from_known_events", len(target_symbols), "Symbols in known carry-forward events"),
            ("phase370_target_full_universe_local_present", target_full_universe_present, "Full target date already present locally"),
            ("phase370_target_local_symbol_count", target_symbol_count, "Local target symbols found"),
            ("phase370_target_local_parquet_files", target_file_rows, "Local target parquet files found"),
            ("phase370_target_local_bytes", target_bytes, "Local target bytes found"),
            ("phase370_sas_env_present_now", sas_env_present, "Supported SAS env present now"),
            ("phase370_estimated_selected_after_one_day", estimated_selected_after_one_day, "Estimated selected trades after adding known one-day carry-forward events"),
            ("phase370_event_floor_after_one_day_estimate", event_floor_after_one_day, "Whether one-day target likely reaches 30-event floor"),
            ("phase370_acceptance_retest_allowed_now", 0, "No acceptance retest without verified full-universe event-floor evidence"),
            ("phase370_strategy_promotion_allowed", 0, "No promotion"),
            ("phase370_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase370_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase370_hard_gate_pass_rows", int(gates["passed"].astype(int).sum()), "Passed hard gates"),
            ("phase370_hard_gate_rows", len(gates), "Hard gates"),
            ("phase370_next_best_action", f"download_or_local_drop_full_universe_real_l2_for_{target_trade_date}_then_rerun_phase370_verify_no_paper_live", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )

    outputs = {
        "summary": output_dir / "phase370_acceptance_summary.csv",
        "date_inventory": output_dir / "phase370_local_date_inventory.csv",
        "target_contract": output_dir / "phase370_one_day_target_contract.csv",
        "known_events": output_dir / "phase370_known_carry_forward_events.csv",
        "verifier": output_dir / "phase370_verifier_ledger.csv",
        "gates": output_dir / "phase370_gate_evaluation.csv",
        "report": output_dir / "phase370_one_day_real_l2_drop_verifier_report.md",
        "manifest": output_dir / "phase370_one_day_real_l2_drop_verifier_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    date_inventory.to_csv(outputs["date_inventory"], index=False)
    target_contract.to_csv(outputs["target_contract"], index=False)
    post_close_unmapped.to_csv(outputs["known_events"], index=False)
    verifier.to_csv(outputs["verifier"], index=False)
    gates.to_csv(outputs["gates"], index=False)

    report = "\n".join(
        [
            "# Phase370 One-Day Real L2 Drop Verifier",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase370 selects and verifies the next disk-safe one-day official-catalyst real L2 target. It does not download data, does not run a strategy retest, and opens no promotion, paper/live acceptance, or deployable profitability claim.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Local date inventory",
            "",
            _markdown_table(date_inventory),
            "",
            "## One-day target contract",
            "",
            _markdown_table(target_contract),
            "",
            "## Verifier ledger",
            "",
            _markdown_table(verifier),
            "",
            "## Gate evaluation",
            "",
            _markdown_table(gates),
            "",
            f"Phase370 decision: target `{target_trade_date}` as the next one-day full-universe real L2 drop/download. The current workspace does not have a verified full-universe target day, and one day alone is not expected to reach the event floor.",
            "",
            "No promotion, paper/live acceptance, or deployable profitability claim is opened.",
        ]
    )
    outputs["report"].write_text(report + "\n", encoding="utf-8")

    manifest = {
        "phase": 370,
        "generated_at_utc": generated_utc,
        "outputs": {key: str(value) for key, value in outputs.items()},
        "supported_sas_env_names_checked": SUPPORTED_SAS_ENV_NAMES,
        "reproducibility": reproducibility_fields(
            artifact_id="phase370_one_day_real_l2_drop_verifier",
            generated_utc=generated_utc,
            inputs={
                "phase369_summary": "outputs/phase369/phase369_acceptance_summary.csv",
                "phase359_eligibility": "outputs/phase359/phase359_no_lookahead_official_catalyst_eligibility.csv",
                "existing_root": str(existing_root),
                "unseen_root": str(unseen_root),
            },
            parameters={
                "target_trade_date": target_trade_date,
                "required_symbols": len(TICKERS),
                "download_executed": False,
                "strategy_retest_executed": False,
                "secret_material_recorded": 0,
            },
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": str(summary[summary["metric"].eq("phase370_next_best_action")]["value"].iloc[0]),
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--existing-root", type=Path, default=DEFAULT_EXISTING_ROOT)
    parser.add_argument("--unseen-root", type=Path, default=DEFAULT_UNSEEN_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.existing_root, args.unseen_root, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))
