from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase359_local_unseen_real_l2_catalyst_expansion import (
    build_full_depth_schema,
    build_no_lookahead_eligibility,
    discover_real_keys,
    fetch_official_catalysts,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_EXISTING_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_UNSEEN_ROOT = Path("real_data_sample/l2_unseen_validation")
DEFAULT_OUTPUT_DIR = Path("outputs/phase373")
TARGET_DATE = "2026-07-21"
EVENT_FLOOR = 30


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


def event_key(frame: pd.DataFrame) -> pd.Series:
    fields = ["source_id", "symbol", "announcement_time_ist", "seq_id", "diagnostic_trade_date"]
    for field in fields:
        if field not in frame.columns:
            frame[field] = ""
    return frame[fields].fillna("").astype(str).agg("|".join, axis=1)


def build_work_order(eligible: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    ready = eligible[eligible["diagnostic_real_l2_available"].astype(int).eq(1)].copy() if not eligible.empty else pd.DataFrame()
    for row in ready.itertuples(index=False):
        rows.append(
            {
                "phase373_work_order_id": f"P373_{row.diagnostic_trade_date}_{row.symbol}_{row.seq_id}",
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


def write_outputs(existing_root: Path, unseen_root: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()

    phase341_summary = read_csv(Path("outputs/phase341/phase341_acceptance_summary.csv"))
    phase359_elig = read_csv(Path("outputs/phase359/phase359_no_lookahead_official_catalyst_eligibility.csv"))
    phase366_summary = read_csv(Path("outputs/phase366/phase366_acceptance_summary.csv"))
    phase370_summary = read_csv(Path("outputs/phase370/phase370_acceptance_summary.csv"))
    phase372_summary = read_csv(Path("outputs/phase372/phase372_acceptance_summary.csv"))
    if phase341_summary.empty or phase359_elig.empty or phase366_summary.empty or phase370_summary.empty or phase372_summary.empty:
        raise FileNotFoundError("Phase373 requires Phase341, Phase359, Phase366, Phase370 and Phase372 artifacts")

    existing_keys = discover_real_keys(existing_root)
    unseen_keys = discover_real_keys(unseen_root)
    local_keys = pd.concat([existing_keys, unseen_keys], ignore_index=True)
    local_dates = sorted(local_keys["trade_date"].dropna().astype(str).unique().tolist())
    target_local = local_keys[local_keys["trade_date"].astype(str).eq(TARGET_DATE)].copy()
    target_symbols = int(target_local["symbol"].nunique()) if not target_local.empty else 0
    target_full_universe = int(as_int(metric_value(phase370_summary, "phase370_target_full_universe_local_present")) == 1 and target_symbols >= 32)

    catalysts, source_ledger = fetch_official_catalysts(local_dates)
    eligibility = build_no_lookahead_eligibility(catalysts, local_keys)
    ready = eligibility[eligibility["diagnostic_real_l2_available"].astype(int).eq(1)].copy() if not eligibility.empty else pd.DataFrame()
    previous_ready = phase359_elig[phase359_elig["diagnostic_real_l2_available"].astype(int).eq(1)].copy()
    previous_keys = set(event_key(previous_ready).tolist())
    ready = ready.copy()
    ready["event_key"] = event_key(ready)
    new_ready = ready[~ready["event_key"].isin(previous_keys)].copy()
    target_ready = ready[ready["diagnostic_trade_date"].astype(str).eq(TARGET_DATE)].copy()
    target_carry_forward = target_ready[target_ready["announcement_date"].astype(str).lt(TARGET_DATE)].copy()
    work_order = build_work_order(ready.drop(columns=["event_key"], errors="ignore"))
    schema = build_full_depth_schema(unseen_root)

    phase341_events = as_int(metric_value(phase341_summary, "phase341_no_lookahead_eligible_event_rows"))
    refreshed_events = int(len(ready))
    combined_refreshed_work_rows = phase341_events + refreshed_events
    phase366_selected = as_int(metric_value(phase366_summary, "phase366_primary_trade_rows"))
    phase369_work_rows = 123
    selected_yield = phase366_selected / phase369_work_rows if phase369_work_rows else 0.0
    estimated_selected_after_refresh = phase366_selected + max(0, refreshed_events - as_int(metric_value(read_csv(Path("outputs/phase359/phase359_acceptance_summary.csv")), "phase359_no_lookahead_eligible_event_rows"))) * selected_yield
    event_floor_after_refresh = int(estimated_selected_after_refresh >= EVENT_FLOOR)

    gates = pd.DataFrame(
        [
            ("P373_PHASE372_TARGET_VERIFIED", target_full_universe, f"target_symbols={target_symbols}"),
            ("P373_OFFICIAL_FETCH_ATTEMPTED", int(len(source_ledger) > 0), f"source_rows={len(source_ledger)}"),
            ("P373_OFFICIAL_FETCH_OK", int(source_ledger.get("ok", pd.Series(dtype=int)).fillna(0).astype(int).sum() > 0), f"ok_rows={int(source_ledger.get('ok', pd.Series(dtype=int)).fillna(0).astype(int).sum())}"),
            ("P373_REFRESHED_ELIGIBLE_EVENTS_PRESENT", int(refreshed_events > 0), f"ready_rows={refreshed_events}"),
            ("P373_TARGET_DATE_EVENTS_PRESENT", int(len(target_ready) > 0), f"target_ready_rows={len(target_ready)}"),
            ("P373_FULL_DEPTH_SCHEMA_RETAINED", int(schema["present"].astype(int).sum() == len(schema)), f"schema={int(schema['present'].astype(int).sum())}/{len(schema)}"),
            ("P373_EVENT_FLOOR_CHECKED", 1, f"estimated_selected_after_refresh={estimated_selected_after_refresh:.3f}; floor={EVENT_FLOOR}"),
            ("P373_NO_STRATEGY_RETEST_OR_PROMOTION", 1, "event_count_refresh_only"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )

    summary = pd.DataFrame(
        [
            ("phase373_refreshed_catalyst_event_count_after_20260721_complete", int(gates["passed"].astype(int).all()), "Phase373 complete if all hard gates pass"),
            ("phase373_local_trade_dates", ";".join(local_dates), "Local trade dates included in refresh"),
            ("phase373_target_trade_date", TARGET_DATE, "Newly verified target date"),
            ("phase373_target_full_universe_local_present", target_full_universe, "Target full universe present"),
            ("phase373_official_source_response_rows", len(source_ledger), "Official source response rows"),
            ("phase373_official_source_ok_rows", int(source_ledger.get("ok", pd.Series(dtype=int)).fillna(0).astype(int).sum()), "Official source OK rows"),
            ("phase373_official_catalyst_rows", len(catalysts), "Official catalyst rows fetched"),
            ("phase373_refreshed_no_lookahead_eligible_rows", refreshed_events, "Refreshed eligible rows with local L2"),
            ("phase373_previous_phase359_eligible_rows", len(previous_ready), "Previous Phase359 eligible rows"),
            ("phase373_new_eligible_rows_vs_phase359", len(new_ready), "New eligible rows after adding target date"),
            ("phase373_target_date_eligible_rows", len(target_ready), "Eligible rows whose diagnostic date is target"),
            ("phase373_target_carry_forward_rows", len(target_carry_forward), "Prior-date post-close rows carried into target date"),
            ("phase373_combined_phase341_plus_refreshed_work_rows", combined_refreshed_work_rows, "Phase341 plus refreshed Phase359-like work rows"),
            ("phase373_estimated_selected_after_refresh", estimated_selected_after_refresh, "Estimated selected trades after refresh at observed yield"),
            ("phase373_event_floor_after_refresh_estimate", event_floor_after_refresh, "Whether estimate reaches event floor"),
            ("phase373_acceptance_retest_allowed_now", 0, "No retest in this phase"),
            ("phase373_strategy_promotion_allowed", 0, "No promotion"),
            ("phase373_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase373_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase373_hard_gate_pass_rows", int(gates["passed"].astype(int).sum()), "Passed hard gates"),
            ("phase373_hard_gate_rows", len(gates), "Hard gates"),
            ("phase373_next_best_action", "interpret_phase373_or_download_next_official_catalyst_real_l2_day_no_paper_live", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )

    outputs = {
        "summary": output_dir / "phase373_acceptance_summary.csv",
        "local_inventory": output_dir / "phase373_local_real_l2_inventory.csv",
        "source_ledger": output_dir / "phase373_official_source_response_ledger.csv",
        "catalysts": output_dir / "phase373_official_catalyst_calendar.csv",
        "eligibility": output_dir / "phase373_no_lookahead_official_catalyst_eligibility.csv",
        "new_events": output_dir / "phase373_new_eligible_events_vs_phase359.csv",
        "work_order": output_dir / "phase373_refreshed_execution_work_order.csv",
        "schema": output_dir / "phase373_full_depth_schema_contract.csv",
        "gates": output_dir / "phase373_gate_evaluation.csv",
        "report": output_dir / "phase373_refreshed_catalyst_event_count_after_20260721_report.md",
        "manifest": output_dir / "phase373_refreshed_catalyst_event_count_after_20260721_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    local_keys.to_csv(outputs["local_inventory"], index=False)
    source_ledger.to_csv(outputs["source_ledger"], index=False)
    catalysts.to_csv(outputs["catalysts"], index=False)
    eligibility.to_csv(outputs["eligibility"], index=False)
    new_ready.drop(columns=["event_key"], errors="ignore").to_csv(outputs["new_events"], index=False)
    work_order.to_csv(outputs["work_order"], index=False)
    schema.to_csv(outputs["schema"], index=False)
    gates.to_csv(outputs["gates"], index=False)

    report = "\n".join(
        [
            "# Phase373 Refreshed Catalyst Event Count After 2026-07-21",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase373 refreshes official-catalyst no-lookahead eligibility after the Phase372 `2026-07-21` full-universe real L2 day was downloaded and verified. It does not run a strategy retest and opens no promotion, paper/live acceptance, or deployable profitability claim.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## New eligible events versus Phase359",
            "",
            _markdown_table(new_ready.drop(columns=["event_key"], errors="ignore").head(40)),
            "",
            "## Gate evaluation",
            "",
            _markdown_table(gates),
            "",
            "No strategy retest, promotion, paper/live acceptance, or deployable profitability claim is opened.",
        ]
    )
    outputs["report"].write_text(report + "\n", encoding="utf-8")

    manifest = {
        "phase": 373,
        "generated_at_utc": generated_utc,
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase373_refreshed_catalyst_event_count_after_20260721",
            generated_utc=generated_utc,
            inputs={
                "phase341_summary": "outputs/phase341/phase341_acceptance_summary.csv",
                "phase359_eligibility": "outputs/phase359/phase359_no_lookahead_official_catalyst_eligibility.csv",
                "phase370_summary": "outputs/phase370/phase370_acceptance_summary.csv",
                "phase372_summary": "outputs/phase372/phase372_acceptance_summary.csv",
            },
            parameters={"target_date": TARGET_DATE, "event_floor": EVENT_FLOOR, "strategy_retest_executed": False},
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": str(summary[summary["metric"].eq("phase373_next_best_action")]["value"].iloc[0]),
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
