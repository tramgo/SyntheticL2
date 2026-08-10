from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE305_DIR = Path("outputs/phase305")
DEFAULT_PHASE51_DIR = Path("outputs/phase51")
DEFAULT_PHASE298_DIR = Path("outputs/phase298")
DEFAULT_OUTPUT_DIR = Path("outputs/phase306")

NEXT_ACTION = "run_phase307_event_catalyst_top5_depth_join_materialization_no_strategy_search"
REPAIR_ACTION = "repair_phase306_event_catalyst_top5_depth_join_precommit"

PRE_EVENT_SECONDS = 900
POST_EVENT_SECONDS = 1800
EVENT_BUCKET_SECONDS = 1


def event_month(event_time_ist: str) -> str:
    ts = pd.to_datetime(event_time_ist, errors="coerce")
    if pd.isna(ts):
        return ""
    return str(ts.strftime("%Y-%m"))


def expand_event_universe(events: pd.DataFrame, inventory: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    if events.empty or inventory.empty:
        return pd.DataFrame()
    for event_idx, event in events.reset_index(drop=True).iterrows():
        month = event_month(str(event.get("event_time_ist", "")))
        month_inv = inventory[inventory["trade_month"].astype(str).eq(month)].copy()
        if str(event.get("symbol_scope", "")).strip().upper() != "ALL":
            symbols = {s.strip() for s in str(event.get("symbol_scope", "")).replace("|", ",").split(",") if s.strip()}
            month_inv = month_inv[month_inv["symbol"].astype(str).isin(symbols)]
        for _, inv in month_inv.iterrows():
            rows.append(
                {
                    "event_id": f"P306_EVT_{event_idx + 1:04d}",
                    "event_time_ist": event.get("event_time_ist", ""),
                    "event_type": event.get("event_type", ""),
                    "symbol": inv.get("symbol", ""),
                    "trade_month": month,
                    "dense_file_path": inv.get("file_path", ""),
                    "dense_rows": inv.get("dense_rows", ""),
                    "pre_event_seconds": PRE_EVENT_SECONDS,
                    "post_event_seconds": POST_EVENT_SECONDS,
                    "event_bucket_seconds": EVENT_BUCKET_SECONDS,
                    "source_url_or_file": event.get("source_url_or_file", ""),
                }
            )
    return pd.DataFrame(rows)


def build_join_contract() -> pd.DataFrame:
    rows = [
        ("P306_JOIN_CLOCK", "event_time_ist", "Join windows are centered on observable event timestamp."),
        ("P306_PRE_WINDOW", PRE_EVENT_SECONDS, "Seconds before event for pre-catalyst top-five depth context."),
        ("P306_POST_WINDOW", POST_EVENT_SECONDS, "Seconds after event for response measurement."),
        ("P306_BUCKET_SECONDS", EVENT_BUCKET_SECONDS, "One-second bucket for joined event/depth response features."),
        ("P306_FULL_DEPTH_REQUIRED", 1, "Use top-five market-by-price depth levels 1-5; no L1-only join."),
        ("P306_NO_DIRECTIONAL_LABEL", 1, "Event source provides catalyst timing, not bullish/bearish truth labels."),
        ("P306_NO_STRATEGY_SEARCH", 1, "Materialization precommit only; no P&L, replay or optimization."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_gate_evaluation(phase305: pd.DataFrame, universe: pd.DataFrame, schema_audit: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    imported = as_int(metric_value(phase305, "phase305_imported_event_rows", 0))
    full_depth_pass = bool(not schema_audit.empty and schema_audit["raw_book_state_schema_pass"].astype(int).min() == 1)
    gates = [
        ("P306_PHASE305_IMPORTED_EVENTS", imported > 0, imported, ">0"),
        ("P306_EVENT_UNIVERSE_EXPANDED", len(universe) > 0, len(universe), ">0"),
        ("P306_FULL_DEPTH_SCHEMA_AVAILABLE", full_depth_pass, int(full_depth_pass), 1),
        ("P306_JOIN_CONTRACT_PRESENT", len(contract) >= 7, len(contract), ">=7"),
        ("P306_NO_L1_ONLY_JOIN", True, "full_depth_levels_1_to_5_required", "required"),
        ("P306_NO_DIRECTIONAL_LABEL_FROM_EVENT", True, "event_timestamp_only", "required"),
        ("P306_NO_STRATEGY_SEARCH_OPENED", True, "strategy_search_allowed_now=0", 0),
        ("P306_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(events: pd.DataFrame, universe: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase306_join_precommit_complete", 1, "Phase306 event-catalyst top-five depth join precommit completed"),
            ("phase306_imported_event_rows", len(events), "Imported event-catalyst rows available"),
            ("phase306_event_universe_rows", len(universe), "Event x symbol join work-order rows"),
            ("phase306_event_rows_with_depth_month", int(universe["event_id"].nunique()) if not universe.empty else 0, "Distinct events with matching dense month"),
            ("phase306_symbol_rows", int(universe["symbol"].nunique()) if not universe.empty else 0, "Symbols in join universe"),
            ("phase306_pre_event_seconds", PRE_EVENT_SECONDS, "Pre-event window"),
            ("phase306_post_event_seconds", POST_EVENT_SECONDS, "Post-event window"),
            ("phase306_event_bucket_seconds", EVENT_BUCKET_SECONDS, "Join bucket size"),
            ("phase306_full_depth_levels_1_to_5_required", 1, "Top-five market-by-price depth required"),
            ("phase306_strategy_search_allowed_now", 0, "No strategy search in Phase306"),
            ("phase306_strategy_replay_allowed", 0, "No replay"),
            ("phase306_strategy_promotion_allowed", 0, "No promotion"),
            ("phase306_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase306_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase306_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase306_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase306_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, contract: pd.DataFrame, universe: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase306 Event-Catalyst Top-Five Depth Join Precommit",
        "",
        "Phase306 precommits the event-catalyst to top-five market-by-price depth join. It does not materialize joined features and does not run strategy search.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Join contract",
        "",
        _markdown_table(contract),
        "",
        "## Event-symbol universe",
        "",
        _markdown_table(universe.head(80)),
        "",
        "## Gates",
        "",
        _markdown_table(gates),
    ]
    (output_dir / "phase306_event_catalyst_top5_depth_join_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    phase305_dir: Path = DEFAULT_PHASE305_DIR,
    phase51_dir: Path = DEFAULT_PHASE51_DIR,
    phase298_dir: Path = DEFAULT_PHASE298_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase305 = read_csv(phase305_dir / "phase305_acceptance_summary.csv")
    events = read_csv(phase305_dir / "phase305_imported_event_catalyst_ledger.csv")
    inventory = read_csv(phase51_dir / "full_dense_lake_inventory.csv")
    schema_audit = read_csv(phase298_dir / "phase298_raw_book_schema_audit.csv")
    contract = build_join_contract()
    universe = expand_event_universe(events, inventory)
    gates = build_gate_evaluation(phase305, universe, schema_audit, contract)
    acceptance = build_acceptance(events, universe, gates)

    contract.to_csv(output_dir / "phase306_event_catalyst_top5_depth_join_contract.csv", index=False)
    universe.to_csv(output_dir / "phase306_event_symbol_join_work_order.csv", index=False)
    gates.to_csv(output_dir / "phase306_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase306_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, contract, universe, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase306_event_catalyst_top5_depth_join_precommit",
        **reproducibility_fields(
            artifact_id="phase306",
            generated_utc=generated_utc,
            inputs={
                "phase305_acceptance": str(phase305_dir / "phase305_acceptance_summary.csv"),
                "phase305_imported_events": str(phase305_dir / "phase305_imported_event_catalyst_ledger.csv"),
                "phase51_dense_inventory": str(phase51_dir / "full_dense_lake_inventory.csv"),
                "phase298_schema_audit": str(phase298_dir / "phase298_raw_book_schema_audit.csv"),
            },
            parameters={
                "pre_event_seconds": PRE_EVENT_SECONDS,
                "post_event_seconds": POST_EVENT_SECONDS,
                "event_bucket_seconds": EVENT_BUCKET_SECONDS,
                "next_action": NEXT_ACTION,
            },
            outputs={"acceptance_summary": str(output_dir / "phase306_acceptance_summary.csv")},
            cost_model_version="not_applicable_join_precommit_only",
            latency_model_version="not_applicable_join_precommit_only",
        ),
    }
    (output_dir / "phase306_event_catalyst_top5_depth_join_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Phase306 event-catalyst top-five depth join precommit.")
    parser.add_argument("--phase305-dir", type=Path, default=DEFAULT_PHASE305_DIR)
    parser.add_argument("--phase51-dir", type=Path, default=DEFAULT_PHASE51_DIR)
    parser.add_argument("--phase298-dir", type=Path, default=DEFAULT_PHASE298_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase305_dir, args.phase51_dir, args.phase298_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
