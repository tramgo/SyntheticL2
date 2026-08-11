from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE346_DIR = Path("outputs/phase346")
DEFAULT_PHASE340_DIR = Path("outputs/phase340")
DEFAULT_PHASE341_DIR = Path("outputs/phase341")
DEFAULT_REAL_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_OUTPUT_DIR = Path("outputs/phase347")

ANNUALIZED_THRESHOLD_PCT = 12.0
ROBUST_EVENT_FLOOR = 30
MAX_NEW_DATES_PER_INCREMENT = 1
NEXT_ACTION = "run_phase348_official_catalyst_event_count_expansion_execution_no_paper_live"
REPAIR_ACTION = "repair_phase347_official_catalyst_event_count_expansion_precommit"


def local_real_l2_dates(real_root: Path) -> list[str]:
    if not real_root.exists():
        return []
    out = []
    for path in real_root.iterdir():
        if path.is_dir() and path.name.startswith("trade_date="):
            out.append(path.name.split("=", 1)[1])
    return sorted(out)


def source_priority_catalog() -> pd.DataFrame:
    rows = [
        (
            "NSE_CORPORATE_ANNOUNCEMENTS",
            1,
            "primary_timestamp_authority",
            "official exchange corporate announcements for symbol-level market disclosures",
            "https://www.nseindia.com/companies-listing/corporate-filings-announcements",
            1,
            0,
        ),
        (
            "BSE_CORPORATE_ANNOUNCEMENTS",
            2,
            "official_cross_check",
            "official exchange cross-check for dual-listed company disclosures and timing disputes",
            "https://www.bseindia.com/corporates/ann.html",
            1,
            0,
        ),
        (
            "SEBI_CORPORATE_FILINGS_AND_ORDERS",
            3,
            "regulatory_context_and_material_action_source",
            "regulatory filings, orders, circulars, and enforcement context; use as timestamp authority only when event publication timing is explicit",
            "https://www.sebi.gov.in/curation/corporate_filings.html",
            1,
            0,
        ),
        (
            "NEWS_ANNOTATION_ONLY",
            4,
            "context_not_timestamp_authority",
            "news may explain catalyst context but must not replace official announcement timing",
            "not_applicable",
            0,
            0,
        ),
    ]
    return pd.DataFrame(
        rows,
        columns=[
            "source_id",
            "priority",
            "role",
            "description",
            "reference_url",
            "official_timestamp_authority_allowed",
            "paper_live_or_profit_claim_allowed",
        ],
    )


def build_candidate_grid(clues: pd.DataFrame) -> pd.DataFrame:
    candidates = clues[clues["phase347_candidate"].astype(int).eq(1)].copy()
    candidates["phase347_grid_id"] = [f"P347_GRID_{i:03d}" for i in range(len(candidates))]
    candidates["min_trade_rows_required"] = ROBUST_EVENT_FLOOR
    candidates["additional_trade_rows_needed"] = (ROBUST_EVENT_FLOOR - candidates["trade_rows"].astype(int)).clip(lower=0)
    candidates["fixed_capital_required"] = 1
    candidates["full_top_five_depth_required"] = 1
    candidates["levels_2_to_5_materiality_required"] = 1
    candidates["l1_only_allowed"] = 0
    candidates["official_catalyst_required"] = 1
    candidates["paper_live_or_profit_claim_allowed"] = 0
    return candidates[
        [
            "phase347_grid_id",
            "scenario_id",
            "family_id",
            "entry_timing_policy",
            "horizon_seconds",
            "depth_threshold_quantile",
            "annualized_return_pct",
            "net_pnl_inr",
            "trade_rows",
            "additional_trade_rows_needed",
            "control_pass",
            "min_trade_rows_required",
            "fixed_capital_required",
            "full_top_five_depth_required",
            "levels_2_to_5_materiality_required",
            "l1_only_allowed",
            "official_catalyst_required",
            "paper_live_or_profit_claim_allowed",
        ]
    ].reset_index(drop=True)


def build_existing_event_inventory(calendar: pd.DataFrame, overlap: pd.DataFrame, phase341_work: pd.DataFrame, real_dates: list[str]) -> pd.DataFrame:
    by_date = calendar.groupby("announcement_date", dropna=False).agg(official_calendar_rows=("symbol", "size"), symbols=("symbol", "nunique")).reset_index()
    overlap_by_date = overlap.groupby("trade_date", dropna=False).agg(real_l2_matched_symbol_rows=("symbol", "size"), matched_catalyst_rows=("official_catalyst_rows", lambda s: int(pd.to_numeric(s, errors="coerce").fillna(0).sum()))).reset_index()
    work_by_date = phase341_work.groupby("diagnostic_trade_date", dropna=False).agg(no_lookahead_work_order_rows=("work_order_id", "size"), work_order_symbols=("symbol", "nunique")).reset_index()
    out = by_date.merge(overlap_by_date, left_on="announcement_date", right_on="trade_date", how="left")
    out = out.merge(work_by_date, left_on="announcement_date", right_on="diagnostic_trade_date", how="left")
    out["local_real_l2_date_present"] = out["announcement_date"].astype(str).isin(real_dates).astype(int)
    for col in ["real_l2_matched_symbol_rows", "matched_catalyst_rows", "no_lookahead_work_order_rows", "work_order_symbols"]:
        out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0).astype(int)
    return out[
        [
            "announcement_date",
            "official_calendar_rows",
            "symbols",
            "local_real_l2_date_present",
            "real_l2_matched_symbol_rows",
            "matched_catalyst_rows",
            "no_lookahead_work_order_rows",
            "work_order_symbols",
        ]
    ].sort_values("announcement_date").reset_index(drop=True)


def build_expansion_work_order(candidate_grid: pd.DataFrame, inventory: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    max_trade_rows = int(candidate_grid["trade_rows"].astype(int).max()) if not candidate_grid.empty else 0
    additional_needed = max(0, ROBUST_EVENT_FLOOR - max_trade_rows)
    candidate_symbols = sorted(
        set(
            [
                "SBIN",
                "AXISBANK",
                "HDFCBANK",
                "ICICIBANK",
                "KOTAKBANK",
                "ADANIPORTS",
                "BHARTIARTL",
                "DRREDDY",
                "HCLTECH",
                "M&M",
                "RELIANCE",
                "TCS",
            ]
        )
    )
    rows = [
        {
            "work_order_id": "P347_WO_001_OFFICIAL_SOURCE_REFRESH",
            "work_type": "official_catalyst_source_refresh",
            "priority": 1,
            "action": "refresh NSE corporate announcements and add BSE/SEBI official cross-check columns for candidate symbols",
            "target_dates": "next_available_unseen_official_catalyst_dates",
            "target_symbols": ";".join(candidate_symbols),
            "max_new_dates_per_increment": MAX_NEW_DATES_PER_INCREMENT,
            "disk_scope": "metadata_only",
            "success_condition": "official catalyst rows include source_id, symbol, announcement_time_ist, announcement_date, description, and no-lookahead timestamp authority",
            "paper_live_or_profit_claim_allowed": 0,
        },
        {
            "work_order_id": "P347_WO_002_TARGETED_REAL_L2_DOWNLOAD",
            "work_type": "targeted_real_l2_download",
            "priority": 2,
            "action": "download only date/exchange/symbol partitions that intersect official catalyst rows and candidate symbols",
            "target_dates": "one_new_official_catalyst_matched_date_at_a_time",
            "target_symbols": ";".join(candidate_symbols),
            "max_new_dates_per_increment": MAX_NEW_DATES_PER_INCREMENT,
            "disk_scope": "targeted_partitions_not_full_panel",
            "success_condition": f"add at least {additional_needed} candidate trade opportunities before acceptance re-evaluation; keep top-five book state persisted",
            "paper_live_or_profit_claim_allowed": 0,
        },
        {
            "work_order_id": "P347_WO_003_NO_LOOKAHEAD_JOIN_REFRESH",
            "work_type": "no_lookahead_event_l2_join_refresh",
            "priority": 3,
            "action": "rebuild official-catalyst to real-L2 work order using first tick at or after official announcement time",
            "target_dates": "all_local_plus_new_targeted_dates",
            "target_symbols": ";".join(candidate_symbols),
            "max_new_dates_per_increment": MAX_NEW_DATES_PER_INCREMENT,
            "disk_scope": "derived_csv_only",
            "success_condition": "all replay candidates have no_lookahead_rule_applied=1 and full L1-L5 Zerodha top-five fields available",
            "paper_live_or_profit_claim_allowed": 0,
        },
        {
            "work_order_id": "P347_WO_004_PHASE345_CANDIDATE_RERUN_PREP",
            "work_type": "candidate_grid_rerun_preparation",
            "priority": 4,
            "action": "prepare Phase348 execution to rerun only Phase347 candidate grid rows on expanded event-count universe",
            "target_dates": "all_local_plus_new_targeted_dates",
            "target_symbols": ";".join(candidate_symbols),
            "max_new_dates_per_increment": MAX_NEW_DATES_PER_INCREMENT,
            "disk_scope": "scenario_outputs_only",
            "success_condition": f"candidate scenarios must reach >= {ROBUST_EVENT_FLOOR} trades, beat controls, and remain > {ANNUALIZED_THRESHOLD_PCT}% fixed-capital annualized before any later acceptance discussion",
            "paper_live_or_profit_claim_allowed": 0,
        },
    ]
    return pd.DataFrame(rows)


def build_gate_evaluation(phase346: pd.DataFrame, candidate_grid: pd.DataFrame, source_catalog: pd.DataFrame, work_order: pd.DataFrame, inventory: pd.DataFrame) -> pd.DataFrame:
    phase346_complete = as_int(metric_value(phase346, "phase346_official_catalyst_native_search_interpretation_complete", 0))
    candidates = len(candidate_grid)
    local_dates = int(inventory["local_real_l2_date_present"].sum()) if not inventory.empty else 0
    rows = [
        ("P347_PHASE346_COMPLETE", phase346_complete == 1, phase346_complete, 1),
        ("P347_SPARSE_CANDIDATES_PRESENT", candidates > 0, candidates, ">0"),
        ("P347_OFFICIAL_SOURCE_PRIORITY_PRESENT", source_catalog["official_timestamp_authority_allowed"].astype(int).sum() >= 3, int(source_catalog["official_timestamp_authority_allowed"].astype(int).sum()), ">=3 official-capable sources"),
        ("P347_TARGETED_DISK_SCOPE_RECORDED", work_order["disk_scope"].astype(str).str.contains("targeted_partitions_not_full_panel").any(), "targeted", "targeted"),
        ("P347_FULL_DEPTH_AND_L2_L5_PRESERVED", candidate_grid["full_top_five_depth_required"].astype(int).eq(1).all() and candidate_grid["levels_2_to_5_materiality_required"].astype(int).eq(1).all(), "preserved", "preserved"),
        ("P347_FIXED_CAPITAL_AND_COSTS_PRESERVED", candidate_grid["fixed_capital_required"].astype(int).eq(1).all(), "fixed_capital", "fixed_capital"),
        ("P347_LOCAL_BASELINE_INVENTORY_PRESENT", local_dates >= 1, local_dates, ">=1"),
        ("P347_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", True, "closed", "closed"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed", "required"])


def write_outputs(phase346_dir: Path, phase340_dir: Path, phase341_dir: Path, real_root: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase346 = read_csv(phase346_dir / "phase346_acceptance_summary.csv")
    contract = pd.read_csv(phase346_dir / "phase346_phase347_execution_contract.csv")
    clues = pd.read_csv(phase346_dir / "phase346_candidate_clue_ledger.csv")
    calendar = pd.read_csv(phase340_dir / "phase340_official_catalyst_calendar.csv")
    overlap = pd.read_csv(phase340_dir / "phase340_official_catalyst_real_l2_overlap.csv")
    phase341_work = pd.read_csv(phase341_dir / "phase341_phase342_execution_work_order.csv")
    real_dates = local_real_l2_dates(real_root)
    source_catalog = source_priority_catalog()
    candidate_grid = build_candidate_grid(clues)
    inventory = build_existing_event_inventory(calendar, overlap, phase341_work, real_dates)
    work_order = build_expansion_work_order(candidate_grid, inventory, contract)
    gates = build_gate_evaluation(phase346, candidate_grid, source_catalog, work_order, inventory)
    passed = int(gates["passed"].astype(bool).sum())
    total = int(len(gates))
    max_candidate_trade_rows = int(candidate_grid["trade_rows"].astype(int).max()) if not candidate_grid.empty else 0
    additional_needed = max(0, ROBUST_EVENT_FLOOR - max_candidate_trade_rows)
    estimated_increment_count = int(math.ceil(additional_needed / max(1, max_candidate_trade_rows / max(1, len(real_dates))))) if additional_needed > 0 else 0
    summary = pd.DataFrame(
        [
            ("phase347_official_catalyst_event_count_expansion_precommit_complete", 1, "Phase347 precommit completed"),
            ("phase347_phase346_complete", as_int(metric_value(phase346, "phase346_official_catalyst_native_search_interpretation_complete", 0)), "Phase346 complete"),
            ("phase347_candidate_grid_rows", len(candidate_grid), "Sparse control-passing candidate rows carried forward"),
            ("phase347_official_source_priority_rows", len(source_catalog), "Official source priority rows"),
            ("phase347_official_timestamp_authority_rows", int(source_catalog["official_timestamp_authority_allowed"].astype(int).sum()), "Official timestamp authority-capable rows"),
            ("phase347_local_real_l2_dates", len(real_dates), "Local real L2 dates available"),
            ("phase347_official_calendar_rows", len(calendar), "Existing official catalyst calendar rows"),
            ("phase347_inventory_date_rows", len(inventory), "Existing inventory date rows"),
            ("phase347_existing_no_lookahead_work_order_rows", len(phase341_work), "Existing Phase341 no-lookahead work order rows"),
            ("phase347_max_candidate_trade_rows", max_candidate_trade_rows, "Maximum Phase346 candidate trade rows"),
            ("phase347_additional_candidate_trade_rows_needed", additional_needed, "Additional candidate trade rows needed to reach event floor"),
            ("phase347_max_new_dates_per_increment", MAX_NEW_DATES_PER_INCREMENT, "Disk-aware increment size"),
            ("phase347_estimated_targeted_date_increments", estimated_increment_count, "Estimated targeted date increments"),
            ("phase347_full_top_five_depth_required", 1, "Full top-five depth required"),
            ("phase347_levels_2_to_5_materiality_required", 1, "Levels 2-5 materiality required"),
            ("phase347_l1_only_allowed", 0, "No L1-only variants"),
            ("phase347_fixed_capital_denominator_required", 1, "Fixed-capital denominator required"),
            ("phase347_strategy_promotion_allowed", 0, "No promotion"),
            ("phase347_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase347_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase347_hard_gate_pass_rows", passed, "Passed hard gates"),
            ("phase347_hard_gate_rows", total, "Hard gates"),
            ("phase347_next_best_action", NEXT_ACTION if passed == total else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )
    report = "\n".join(
        [
            "# Phase347 Official-Catalyst Event-Count Expansion Precommit",
            "",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
            "Phase347 precommits a disk-aware event-count expansion around official catalyst days. It does not execute the rerun and does not open paper/live acceptance.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Official source priority",
            "",
            _markdown_table(source_catalog),
            "",
            "## Candidate grid",
            "",
            _markdown_table(candidate_grid.head(20)),
            "",
            "## Existing event inventory",
            "",
            _markdown_table(inventory),
            "",
            "## Expansion work order",
            "",
            _markdown_table(work_order),
            "",
            "Phase348 may execute the targeted expansion only under this contract.",
        ]
    )
    outputs = {
        "summary": output_dir / "phase347_acceptance_summary.csv",
        "source_catalog": output_dir / "phase347_official_source_priority_catalog.csv",
        "candidate_grid": output_dir / "phase347_candidate_execution_grid.csv",
        "inventory": output_dir / "phase347_existing_event_inventory.csv",
        "work_order": output_dir / "phase347_event_count_expansion_work_order.csv",
        "gates": output_dir / "phase347_gate_evaluation.csv",
        "report": output_dir / "phase347_official_catalyst_event_count_expansion_precommit_report.md",
        "manifest": output_dir / "phase347_official_catalyst_event_count_expansion_precommit_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    source_catalog.to_csv(outputs["source_catalog"], index=False)
    candidate_grid.to_csv(outputs["candidate_grid"], index=False)
    inventory.to_csv(outputs["inventory"], index=False)
    work_order.to_csv(outputs["work_order"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    outputs["report"].write_text(report, encoding="utf-8")
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "phase": 347,
        "generated_at_utc": generated_utc,
        "phase346_dir": str(phase346_dir),
        "phase340_dir": str(phase340_dir),
        "phase341_dir": str(phase341_dir),
        "real_root": str(real_root),
        "output_dir": str(output_dir),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase347_official_catalyst_event_count_expansion_precommit",
            generated_utc=generated_utc,
            inputs={
                "phase346_dir": str(phase346_dir),
                "phase340_dir": str(phase340_dir),
                "phase341_dir": str(phase341_dir),
                "real_root": str(real_root),
            },
            parameters={
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "robust_event_floor": ROBUST_EVENT_FLOOR,
                "max_new_dates_per_increment": MAX_NEW_DATES_PER_INCREMENT,
            },
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": NEXT_ACTION if passed == total else REPAIR_ACTION,
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase346-dir", type=Path, default=DEFAULT_PHASE346_DIR)
    parser.add_argument("--phase340-dir", type=Path, default=DEFAULT_PHASE340_DIR)
    parser.add_argument("--phase341-dir", type=Path, default=DEFAULT_PHASE341_DIR)
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase346_dir, args.phase340_dir, args.phase341_dir, args.real_root, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
