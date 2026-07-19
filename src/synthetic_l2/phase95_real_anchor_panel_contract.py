from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_REAL_ROOT = Path("real_data_sample")
DEFAULT_PHASE94_DIR = Path("outputs/phase94")
DEFAULT_OUTPUT_DIR = Path("outputs/phase95")
EXPECTED_SYMBOLS = {
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
}


def metric_value(path: Path, metric: str, default: Any = None) -> Any:
    if not path.exists():
        return default
    frame = pd.read_csv(path)
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    value = rows.iloc[0]
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def discover_real_panels(real_root: Path) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    candidate_roots = [path for path in sorted(real_root.iterdir()) if path.is_dir()] if real_root.exists() else []
    for root in candidate_roots:
        parquet_files = sorted(root.rglob("*.parquet"))
        if not parquet_files:
            continue
        symbol_dirs = [path for path in root.glob("symbol=*") if path.is_dir()]
        symbols = sorted(path.name.replace("symbol=", "") for path in symbol_dirs)
        inferred_dates: set[str] = set()
        for part in root.rglob("trade_date=*"):
            if part.is_dir():
                inferred_dates.add(part.name.replace("trade_date=", ""))
        if not inferred_dates and "single_day" in root.name:
            inferred_dates.add("unknown_single_day")
        rows.append(
            {
                "panel_root": str(root),
                "panel_name": root.name,
                "parquet_files": int(len(parquet_files)),
                "symbol_partitions": int(len(symbols)),
                "expected_symbol_fraction": len(set(symbols).intersection(EXPECTED_SYMBOLS)) / len(EXPECTED_SYMBOLS),
                "missing_expected_symbols": "|".join(sorted(EXPECTED_SYMBOLS.difference(symbols))),
                "inferred_dates": "|".join(sorted(inferred_dates)) if inferred_dates else "unknown",
                "inferred_date_count": int(len(inferred_dates)) if inferred_dates else 1,
                "usable_for_schema_anchor": bool(len(parquet_files) > 0 and len(symbols) >= 30),
                "usable_for_multi_day_calibration": bool(len(inferred_dates) >= 5 and len(symbols) >= 30),
            }
        )
    return pd.DataFrame(rows)


def build_required_panel_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "requirement_id": "P95_MIN_REAL_DAYS",
                "requirement": "Collect at least 5 complete NSE trading days before generator recalibration is considered stable; 10 days preferred.",
                "acceptance_gate": "real_distinct_trade_dates >= 5",
                "why": "One real day cannot identify regime frequencies, tails, month effects, or stable calibration distributions.",
            },
            {
                "requirement_id": "P95_SYMBOL_UNIVERSE",
                "requirement": "Each accepted day should cover the fixed 32-symbol universe or explicitly document missing symbols.",
                "acceptance_gate": "expected_symbol_fraction >= 0.95 for each accepted day",
                "why": "Cross-sectional spread/depth/cadence calibration needs broad symbol coverage.",
            },
            {
                "requirement_id": "P95_SCHEMA",
                "requirement": "Persist the Zerodha WebSocket 54-column schema plus capture diagnostics when available.",
                "acceptance_gate": "L1-L5 price, quantity, order-count fields present for bid and ask",
                "why": "Generator calibration depends on visible top-five book state and received tick timing.",
            },
            {
                "requirement_id": "P95_TIMING",
                "requirement": "Preserve callback receive timestamps, exchange timestamps, local monotonic time, and receive ordering.",
                "acceptance_gate": "monotonic/order violation, duplicate timestamp, stale interval, and gap metrics can be computed per symbol/day",
                "why": "Phase94 found tail cadence calibration gaps; timing evidence is mandatory.",
            },
            {
                "requirement_id": "P95_MARKET_CONTEXT",
                "requirement": "Include a mix of normal, volatile, and shock-like sessions where practical.",
                "acceptance_gate": "panel labels include at least one high-volatility or news/shock-like day before full-year recalibration claims",
                "why": "Synthetic regime and shock assumptions cannot be validated from a calm single day.",
            },
            {
                "requirement_id": "P95_REPLAY_LOCK",
                "requirement": "No new strategy replay branch may be opened until Phase94 calibration gaps are rerun against the multi-day panel.",
                "acceptance_gate": "phase94_strategy_replay_resume_allowed == 1 after rerun",
                "why": "Phase93 stopped strategy mining; Phase94 confirmed calibration gaps.",
            },
        ]
    )


def build_collection_manifest_template() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "field": "trade_date",
                "required": True,
                "example": "2026-07-20",
                "description": "NSE trading date represented by the captured WebSocket ticks.",
            },
            {
                "field": "session_label",
                "required": True,
                "example": "normal|volatile|shock_like|expiry|event",
                "description": "Human or rule-based context label for calibration stratification.",
            },
            {
                "field": "symbols_expected",
                "required": True,
                "example": "|".join(sorted(EXPECTED_SYMBOLS)),
                "description": "Expected fixed universe for the capture day.",
            },
            {
                "field": "symbols_observed",
                "required": True,
                "example": "ADANIPORTS|AXISBANK|...",
                "description": "Observed symbols with at least one readable L2 tick.",
            },
            {
                "field": "capture_start_ist",
                "required": True,
                "example": "09:15:00",
                "description": "Intended market-open capture start in IST.",
            },
            {
                "field": "capture_end_ist",
                "required": True,
                "example": "15:30:00",
                "description": "Intended market-close capture end in IST.",
            },
            {
                "field": "collector_version",
                "required": True,
                "example": "zerodha_websocket_l2_collector_vX",
                "description": "Collector/script version or git commit used for capture.",
            },
            {
                "field": "known_incidents",
                "required": False,
                "example": "disconnect 10:42-10:44; reconnect ok",
                "description": "Disconnects, subscription failures, parser issues, or machine/network incidents.",
            },
        ]
    )


def summarize(panels: pd.DataFrame, phase94_dir: Path) -> pd.DataFrame:
    usable_schema_panels = int(panels["usable_for_schema_anchor"].sum()) if not panels.empty else 0
    usable_multi_day_panels = int(panels["usable_for_multi_day_calibration"].sum()) if not panels.empty else 0
    max_dates = int(panels["inferred_date_count"].max()) if not panels.empty else 0
    max_symbol_fraction = float(panels["expected_symbol_fraction"].max()) if not panels.empty else 0.0
    phase94_pass = metric_value(phase94_dir / "generator_realism_calibration_acceptance_summary.csv", "phase94_generator_calibration_pass", 0)
    phase94_resume = metric_value(phase94_dir / "generator_realism_calibration_acceptance_summary.csv", "phase94_strategy_replay_resume_allowed", 0)
    ready = bool(usable_multi_day_panels > 0 and float(phase94_pass) == 1 and float(phase94_resume) == 1)
    return pd.DataFrame(
        [
            ("phase95_real_panel_roots_found", int(len(panels)), "Real-data panel roots with Parquet files discovered"),
            ("phase95_schema_anchor_panel_roots", usable_schema_panels, "Panel roots usable for schema/single-day anchors"),
            ("phase95_multi_day_calibration_panel_roots", usable_multi_day_panels, "Panel roots meeting the multi-day calibration gate"),
            ("phase95_max_inferred_real_dates", max_dates, "Maximum inferred real date count across panel roots"),
            ("phase95_max_expected_symbol_fraction", max_symbol_fraction, "Best expected-symbol coverage fraction across panel roots"),
            ("phase95_phase94_generator_calibration_pass", int(float(phase94_pass)), "Phase94 generator calibration pass flag"),
            ("phase95_phase94_strategy_resume_allowed", int(float(phase94_resume)), "Phase94 strategy replay resume flag"),
            ("phase95_real_anchor_panel_ready", int(ready), "1 means real anchor panel is ready and strategy replay may reopen"),
            ("phase95_recommend_next_action", "collect_5_to_10_real_websocket_l2_days_then_rerun_phase94", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase95 Real Anchor Panel Contract",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase95 converts the Phase94 calibration stop into a concrete real-data acquisition contract.",
        "The current workspace is scanned for available real L2 panels, and strategy replay remains closed until a multi-day real anchor panel exists and Phase94 passes on rerun.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase95_real_anchor_panel_contract_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase95(real_root: Path, phase94_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    panels = discover_real_panels(real_root)
    contract = build_required_panel_contract()
    template = build_collection_manifest_template()
    acceptance = summarize(panels, phase94_dir)

    panels.to_csv(output_dir / "available_real_panel_inventory.csv", index=False)
    contract.to_csv(output_dir / "required_real_anchor_panel_contract.csv", index=False)
    template.to_csv(output_dir / "real_anchor_collection_manifest_template.csv", index=False)
    acceptance.to_csv(output_dir / "real_anchor_panel_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Available Real Panel Inventory": panels,
            "Required Real Anchor Panel Contract": contract,
            "Collection Manifest Template": template,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {"generated_utc": generated_utc, "scope": "phase95_real_anchor_panel_contract"}
    manifest.update(
        reproducibility_fields(
            artifact_id="phase95",
            generated_utc=generated_utc,
            inputs={
                "real_root": str(real_root),
                "phase94_summary": str(phase94_dir / "generator_realism_calibration_acceptance_summary.csv"),
            },
            parameters={
                "minimum_real_days": 5,
                "preferred_real_days": 10,
                "expected_symbols": sorted(EXPECTED_SYMBOLS),
                "strategy_replay_policy": "closed_until_multiday_panel_and_phase94_pass",
            },
            outputs={
                "panel_inventory": str(output_dir / "available_real_panel_inventory.csv"),
                "required_contract": str(output_dir / "required_real_anchor_panel_contract.csv"),
                "manifest_template": str(output_dir / "real_anchor_collection_manifest_template.csv"),
                "acceptance_summary": str(output_dir / "real_anchor_panel_acceptance_summary.csv"),
                "report": str(output_dir / "phase95_real_anchor_panel_contract_report.md"),
                "manifest": str(output_dir / "phase95_real_anchor_panel_contract_manifest.json"),
            },
            random_seed="none_deterministic_real_panel_contract",
            scenario_ids="phase95_post_phase94_real_anchor_panel_gate",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_data_contract",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase95_real_anchor_panel_contract_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create real anchor panel acquisition/readiness contract.")
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--phase94-dir", type=Path, default=DEFAULT_PHASE94_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase95(args.real_root, args.phase94_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
