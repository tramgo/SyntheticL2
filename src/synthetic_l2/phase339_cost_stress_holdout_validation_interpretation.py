from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE338_DIR = Path("outputs/phase338")
DEFAULT_PHASE330_DIR = Path("outputs/phase330")
DEFAULT_REAL_ROOTS = [Path("real_data_sample/l2_multiday_panel"), Path("derived_real_l2_receive_flow_features_phase176")]
DEFAULT_OUTPUT_DIR = Path("outputs/phase339")

NEXT_ACTION = "run_phase340_official_catalyst_calendar_acquisition_precommit_no_paper_live"
REPAIR_ACTION = "repair_phase339_cost_stress_holdout_validation_interpretation"

ANNUALIZED_THRESHOLD_PCT = 12.0
ROBUST_EVENT_FLOOR = 30
MIN_POSITIVE_SYMBOL_DATE_CELLS = 2


def read_parquet(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_parquet(path)


def build_survivor_ledger(scenarios: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame()
    primary = scenarios[
        scenarios["cost_profile"].astype(str).eq("zerodha_2x_all_in_cost_proxy")
        & scenarios["execution_policy"].astype(str).eq("taker_entry_taker_exit")
        & scenarios["holdout_acceptance_candidate"].astype(int).eq(1)
    ].copy()
    if primary.empty:
        return pd.DataFrame()
    columns = [
        "source_scenario_id",
        "freeze_rank",
        "lane_id",
        "horizon_seconds",
        "signal_quantile",
        "spread_max_quantile",
        "depth_share_min_quantile",
        "top_n_per_event",
        "side_policy",
        "execution_policy",
        "cost_profile",
        "initial_capital_inr",
        "fixed_notional_inr",
        "max_concurrent_positions",
        "scheduled_event_rows",
        "symbol_rows",
        "observed_trade_dates",
        "trade_rows",
        "positive_symbol_date_cells",
        "net_pnl_inr",
        "annualized_return_pct",
        "side_flip_annualized_return_pct",
        "random_side_annualized_return_pct",
        "control_pass",
        "holdout_acceptance_candidate",
    ]
    return primary[columns].sort_values(["annualized_return_pct", "positive_symbol_date_cells", "scheduled_event_rows"], ascending=[False, False, False]).reset_index(drop=True)


def build_failure_mode_ledger(phase338: pd.DataFrame, scenarios: pd.DataFrame, passive: pd.DataFrame) -> pd.DataFrame:
    primary_acceptance = as_int(metric_value(phase338, "phase338_holdout_acceptance_candidate_rows", 0))
    passive_above12 = as_int(metric_value(phase338, "phase338_passive_aware_cost200_above12_rows", 0))
    passive_acceptance = as_int(metric_value(phase338, "phase338_passive_aware_cost200_acceptance_rows", 0))
    synthetic_partition = str(metric_value(phase338, "phase338_holdout_partition_method", "")).startswith("event_hash")
    rows = [
        {
            "failure_or_limit": "passive_aware_charter_not_primary_rescue",
            "observed_value": f"passive_above12={passive_above12};passive_acceptance={passive_acceptance}",
            "interpretation": "Passive-aware execution with fill/adverse/flatten penalties did not produce 2x-cost above-12 rows; keep it diagnostic.",
        },
        {
            "failure_or_limit": "synthetic_holdout_not_deployable_profitability",
            "observed_value": int(synthetic_partition),
            "interpretation": "The holdout partition is synthetic/deterministic from the generated feature matrix, so it cannot by itself prove live profitability.",
        },
        {
            "failure_or_limit": "primary_route_survived_but_requires_replication",
            "observed_value": primary_acceptance,
            "interpretation": "Primary taker route survived Phase338, so the next honest step is controlled replication precommit rather than paper/live promotion.",
        },
        {
            "failure_or_limit": "do_not_tune_same_holdout",
            "observed_value": "closed",
            "interpretation": "Do not add filters, weaken cost stress, lower event floor, or reuse holdout outcomes for tuning.",
        },
    ]
    return pd.DataFrame(rows)


def build_decision_ledger(phase338: pd.DataFrame, survivors: pd.DataFrame, failures: pd.DataFrame) -> pd.DataFrame:
    primary_acceptance = as_int(metric_value(phase338, "phase338_holdout_acceptance_candidate_rows", 0))
    best_candidate = str(metric_value(phase338, "phase338_best_holdout_candidate", ""))
    best_ann = metric_value(phase338, "phase338_best_holdout_annualized_return_pct", "")
    best_events = as_int(metric_value(phase338, "phase338_best_holdout_scheduled_events", 0))
    best_cells = as_int(metric_value(phase338, "phase338_best_holdout_positive_symbol_date_cells", 0))
    passive_acceptance = as_int(metric_value(phase338, "phase338_passive_aware_cost200_acceptance_rows", 0))
    rows = [
        ("phase338_execution_complete", 1, "Phase338 hard gates passed before interpretation.", "Phase338 can be interpreted."),
        ("primary_taker_route_survived_synthetic_holdout", int(primary_acceptance > 0), f"acceptance_rows={primary_acceptance}", "Primary taker execution remains the only surviving route."),
        ("best_survivor_preserved", best_candidate, f"annualized={best_ann};events={best_events};symbol_date_cells={best_cells}", "Preserve the best Phase338 survivor for replication precommit."),
        ("survivor_rows_preserved", int(len(survivors)), f"primary_acceptance={primary_acceptance}", "Carry forward all Phase338 primary 2x-cost survivors."),
        ("passive_aware_route_status", "diagnostic_failed_not_primary_rescue", f"passive_acceptance={passive_acceptance}", "Attached passive-aware charter did not produce accepted 2x-cost diagnostics."),
        ("synthetic_holdout_boundary", "not_deployable_profitability", "synthetic event-hash partition", "Do not claim live profitability from synthetic holdout evidence."),
        ("paper_live_or_promotion_allowed", 0, "closed", "No paper/live, promotion, or deployable profitability opens from Phase339."),
        ("next_route", "P340_OFFICIAL_CATALYST_CALENDAR_ACQUISITION_PRECOMMIT", NEXT_ACTION, "Acquire and align official NSE/SEBI/BSE catalyst calendars before any catalyst-grounded real-day survivor diagnostic."),
    ]
    return pd.DataFrame(rows, columns=["decision_id", "decision_value", "evidence", "interpretation"])


def build_real_day_contract(survivors: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("input_survivors", "outputs/phase339/phase339_survivor_ledger.csv", "Use only Phase339-preserved Phase338 primary 2x-cost survivors."),
        ("survivor_rows", len(survivors), "Survivors cannot be expanded by post-hoc search."),
        ("official_catalyst_calendar_required", 1, "Do not rely on synthetic event labels for catalyst-grounded real-day validation."),
        ("official_sources", "NSE corporate announcements;NSE financial results;SEBI corporate filings index;BSE corporate filings as cross-check", "Use exchange/regulator-published filings and announcements as the catalyst calendar source."),
        ("real_data_root", "real_data_sample/l2_multiday_panel", "Use already-downloaded local real Zerodha WebSocket top-five L2 after official catalyst dates are aligned."),
        ("derived_real_feature_root", "derived_real_l2_receive_flow_features_phase176", "Use local Phase176 real receive-flow features for the first live-day compatibility diagnostic."),
        ("local_real_dates_available", 7, "Current local imported real panel has seven dates and thirty-two symbols."),
        ("real_day_goal", "official_catalyst_aligned_schema_compatibility_and_survivor_directional_diagnostic", "Test whether the synthetic survivor has an honest real-day analogue only after official catalyst-date alignment; do not claim direct strategy validation if schemas differ."),
        ("schema_gap_must_be_logged", 1, "Phase340 must explicitly log synthetic Phase330 vs real Phase176 schema gaps."),
        ("annualized_threshold_pct", ANNUALIZED_THRESHOLD_PCT, "Do not lower >12% annualized threshold."),
        ("robust_event_floor", ROBUST_EVENT_FLOOR, "Do not accept sparse sub-30-event pockets."),
        ("minimum_positive_symbol_date_cells", MIN_POSITIVE_SYMBOL_DATE_CELLS, "Breadth must not be single symbol/date."),
        ("cost_profile_required", "zerodha_2x_all_in_cost_proxy", "2x Zerodha all-in cost stress remains required."),
        ("cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha equity intraday cost formula."),
        ("fixed_capital_denominator", "required", "Annualized return remains fixed-capital, not unlimited capital."),
        ("full_top_five_depth_required", 1, "Top-five market-by-price depth remains core."),
        ("levels_2_to_5_materiality_required", 1, "Levels 2-5/beyond-L1 materiality remains required."),
        ("l1_only_allowed", 0, "No L1-only variants."),
        ("net_edge_live_mask_allowed", 0, "No future outcome/net-edge live masks."),
        ("passive_aware_status", "diagnostic_failed_not_primary_rescue", "Do not use passive-aware diagnostics to rescue acceptance."),
        ("holdout_tuning_allowed", 0, "No tuning on Phase338 holdout outcomes."),
        ("strategy_replay_allowed", 0, "Phase339 is interpretation only."),
        ("strategy_promotion_allowed", 0, "No promotion."),
        ("paper_or_live_acceptance_allowed", 0, "No paper/live acceptance."),
        ("deployable_profitability_claim_allowed", 0, "No deployable profitability claim."),
        ("phase340_precommit_allowed_next", 1, "If gates pass, Phase340 may precommit official catalyst calendar acquisition and alignment."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_real_event_overlap_ledger(phase330_dir: Path, real_roots: list[Path]) -> pd.DataFrame:
    feature_path = phase330_dir / "phase330_event_catalyst_expanded_feature_matrix.parquet"
    if not feature_path.exists():
        return pd.DataFrame()
    events = pd.read_parquet(feature_path)
    events["trade_date"] = events["event_time_ist"].astype(str).str.slice(0, 10)
    event_keys = events[["trade_date", "symbol", "event_id", "event_type"]].drop_duplicates()
    rows: list[dict[str, object]] = []
    for root in real_roots:
        real_keys = []
        if root.exists():
            for path in root.rglob("*.parquet"):
                text = str(path)
                date_match = re.search(r"trade_date=([0-9-]+)", text)
                symbol_match = re.search(r"symbol=([^\\/]+)", text)
                if date_match and symbol_match:
                    real_keys.append((date_match.group(1), symbol_match.group(1)))
        real_frame = pd.DataFrame(real_keys, columns=["trade_date", "symbol"]).drop_duplicates() if real_keys else pd.DataFrame(columns=["trade_date", "symbol"])
        overlap = event_keys.merge(real_frame, on=["trade_date", "symbol"], how="inner") if not real_frame.empty else pd.DataFrame(columns=event_keys.columns)
        sbin_overlap = overlap[overlap["symbol"].astype(str).eq("SBIN")] if not overlap.empty else pd.DataFrame()
        rows.append(
            {
                "real_root": str(root),
                "real_date_rows": int(real_frame["trade_date"].nunique()) if not real_frame.empty else 0,
                "real_symbol_rows": int(real_frame["symbol"].nunique()) if not real_frame.empty else 0,
                "event_calendar_date_rows": int(event_keys["trade_date"].nunique()),
                "event_calendar_symbol_rows": int(event_keys["symbol"].nunique()),
                "overlap_event_symbol_rows": int(len(overlap)),
                "overlap_date_rows": int(overlap["trade_date"].nunique()) if not overlap.empty else 0,
                "overlap_symbol_rows": int(overlap["symbol"].nunique()) if not overlap.empty else 0,
                "overlap_dates": ";".join(sorted(overlap["trade_date"].astype(str).unique().tolist())) if not overlap.empty else "",
                "overlap_event_types": ";".join(sorted(overlap["event_type"].astype(str).unique().tolist())) if not overlap.empty else "",
                "sbin_overlap_date_rows": int(sbin_overlap["trade_date"].nunique()) if not sbin_overlap.empty else 0,
                "sbin_overlap_dates": ";".join(sorted(sbin_overlap["trade_date"].astype(str).unique().tolist())) if not sbin_overlap.empty else "",
                "interpretation": "real L2 overlaps event-catalyst calendar" if not overlap.empty else "no overlap between local real L2 and event-catalyst calendar",
            }
        )
    return pd.DataFrame(rows)


def build_gate_evaluation(phase338: pd.DataFrame, survivors: pd.DataFrame, decisions: pd.DataFrame, contract: pd.DataFrame, overlap: pd.DataFrame) -> pd.DataFrame:
    phase338_complete = as_int(metric_value(phase338, "phase338_cost_stress_holdout_validation_execution_complete", 0))
    phase338_gates = as_int(metric_value(phase338, "phase338_hard_gate_pass_rows", 0))
    phase338_gate_rows = as_int(metric_value(phase338, "phase338_hard_gate_rows", 1))
    primary_acceptance = as_int(metric_value(phase338, "phase338_holdout_acceptance_candidate_rows", 0))
    passive_acceptance = as_int(metric_value(phase338, "phase338_passive_aware_cost200_acceptance_rows", 1))
    claim = as_int(metric_value(phase338, "phase338_deployable_profitability_claim_allowed", 1))
    replay = as_int(metric_value(phase338, "phase338_strategy_replay_allowed", 1))
    contract_lookup = contract.set_index("contract_id")["contract_value"].to_dict() if not contract.empty else {}
    overlap_dates = int(overlap["overlap_date_rows"].max()) if not overlap.empty else 0
    sbin_overlap_dates = int(overlap["sbin_overlap_date_rows"].max()) if not overlap.empty else 0
    rows = [
        ("P339_PHASE338_COMPLETE", phase338_complete == 1, phase338_complete, 1),
        ("P339_PHASE338_GATES_PASSED", phase338_gates == phase338_gate_rows, f"{phase338_gates}/{phase338_gate_rows}", "all"),
        ("P339_PRIMARY_SURVIVORS_PRESENT", primary_acceptance > 0 and len(survivors) > 0, f"phase338={primary_acceptance};ledger={len(survivors)}", ">0"),
        ("P339_PASSIVE_STATUS_RECORDED", passive_acceptance == 0, passive_acceptance, 0),
        ("P339_SYNTHETIC_BOUNDARY_RECORDED", "not_deployable_profitability" in decisions["decision_value"].astype(str).tolist(), "recorded", "recorded"),
        ("P339_REAL_DAY_CONTRACT_PRESENT", len(contract) >= 20, len(contract), ">=20"),
        ("P339_REAL_EVENT_DATE_OVERLAP_PRESENT", overlap_dates > 0, overlap_dates, ">0"),
        ("P339_SBIN_EVENT_DATE_OVERLAP_PRESENT", sbin_overlap_dates > 0, sbin_overlap_dates, ">0"),
        ("P339_FULL_DEPTH_PRESERVED", as_int(contract_lookup.get("full_top_five_depth_required", 0)) == 1 and as_int(contract_lookup.get("levels_2_to_5_materiality_required", 0)) == 1, f"top5={contract_lookup.get('full_top_five_depth_required')};l2_l5={contract_lookup.get('levels_2_to_5_materiality_required')}", "both=1"),
        ("P339_NO_LOOKAHEAD_OR_L1_ONLY", as_int(contract_lookup.get("l1_only_allowed", 1)) == 0 and as_int(contract_lookup.get("net_edge_live_mask_allowed", 1)) == 0, f"l1={contract_lookup.get('l1_only_allowed')};lookahead={contract_lookup.get('net_edge_live_mask_allowed')}", "both=0"),
        ("P339_BOUNDARIES_CLOSED", replay == 0 and claim == 0 and as_int(contract_lookup.get("deployable_profitability_claim_allowed", 1)) == 0, f"replay={replay};claim={claim};contract_claim={contract_lookup.get('deployable_profitability_claim_allowed')}", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(phase338: pd.DataFrame, survivors: pd.DataFrame, decisions: pd.DataFrame, contract: pd.DataFrame, gates: pd.DataFrame, overlap: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    complete = int(hard_pass == hard_rows)
    best = survivors.head(1)
    max_overlap_dates = int(overlap["overlap_date_rows"].max()) if not overlap.empty else 0
    max_overlap_symbols = int(overlap["overlap_symbol_rows"].max()) if not overlap.empty else 0
    max_sbin_dates = int(overlap["sbin_overlap_date_rows"].max()) if not overlap.empty else 0
    overlap_date_list = str(overlap.sort_values("overlap_date_rows", ascending=False)["overlap_dates"].iloc[0]) if not overlap.empty else ""
    overlap_types = str(overlap.sort_values("overlap_date_rows", ascending=False)["overlap_event_types"].iloc[0]) if not overlap.empty else ""
    return pd.DataFrame(
        [
            ("phase339_cost_stress_holdout_validation_interpretation_complete", complete, "Phase339 interpretation completed"),
            ("phase339_primary_taker_route_survived_synthetic_holdout", int(len(survivors) > 0), "Primary taker route survived synthetic holdout"),
            ("phase339_survivor_rows_preserved", int(len(survivors)), "Phase338 survivor rows preserved"),
            ("phase339_best_survivor_candidate", best.iloc[0]["source_scenario_id"] if not best.empty else "", "Best survivor candidate"),
            ("phase339_best_survivor_annualized_return_pct", float(best.iloc[0]["annualized_return_pct"]) if not best.empty else "", "Best survivor annualized return"),
            ("phase339_best_survivor_scheduled_events", int(best.iloc[0]["scheduled_event_rows"]) if not best.empty else 0, "Best survivor scheduled events"),
            ("phase339_best_survivor_positive_symbol_date_cells", int(best.iloc[0]["positive_symbol_date_cells"]) if not best.empty else 0, "Best survivor positive symbol-date cells"),
            ("phase339_passive_aware_route_status", "diagnostic_failed_not_primary_rescue", "Passive-aware route status"),
            ("phase339_passive_aware_cost200_acceptance_rows", metric_value(phase338, "phase338_passive_aware_cost200_acceptance_rows", 0), "Passive-aware 2x-cost acceptance rows"),
            ("phase339_synthetic_holdout_boundary", "not_deployable_profitability", "Synthetic holdout boundary"),
            ("phase339_selected_next_route", "P340_OFFICIAL_CATALYST_CALENDAR_ACQUISITION_PRECOMMIT", "Selected next route"),
            ("phase339_contract_rows", int(len(contract)), "Phase340 official catalyst calendar contract rows"),
            ("phase339_real_event_overlap_date_rows", max_overlap_dates, "Local real dates overlapping event-catalyst calendar"),
            ("phase339_real_event_overlap_symbol_rows", max_overlap_symbols, "Symbols on overlapping real/event dates"),
            ("phase339_real_event_overlap_dates", overlap_date_list, "Overlapping real/event dates"),
            ("phase339_real_event_overlap_event_types", overlap_types, "Overlapping event types"),
            ("phase339_sbin_real_event_overlap_date_rows", max_sbin_dates, "SBIN real/event overlap dates"),
            ("phase339_strategy_replay_allowed", 0, "No replay"),
            ("phase339_strategy_promotion_allowed", 0, "No promotion"),
            ("phase339_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase339_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase339_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase339_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase339_next_best_action", NEXT_ACTION if complete else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase339 Cost-Stress Holdout Validation Interpretation",
        "",
        "Phase339 interprets the Phase338 synthetic holdout execution.",
        "It preserves the primary taker survivors, records that passive-aware diagnostics did not rescue the edge, requires official NSE/SEBI/BSE catalyst-calendar alignment before real-day diagnostics, and keeps paper/live/profitability claims closed.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase339_cost_stress_holdout_validation_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase338_dir: Path = DEFAULT_PHASE338_DIR, phase330_dir: Path = DEFAULT_PHASE330_DIR, real_roots: list[Path] = DEFAULT_REAL_ROOTS, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase338 = read_csv(phase338_dir / "phase338_acceptance_summary.csv")
    scenarios = read_parquet(phase338_dir / "phase338_holdout_scenario_summary.parquet")
    passive = read_csv(phase338_dir / "phase338_passive_aware_diagnostic_ledger.csv")
    survivors = build_survivor_ledger(scenarios)
    failures = build_failure_mode_ledger(phase338, scenarios, passive)
    decisions = build_decision_ledger(phase338, survivors, failures)
    contract = build_real_day_contract(survivors)
    overlap = build_real_event_overlap_ledger(phase330_dir, real_roots)
    gates = build_gate_evaluation(phase338, survivors, decisions, contract, overlap)
    acceptance = build_acceptance(phase338, survivors, decisions, contract, gates, overlap)

    survivors.to_csv(output_dir / "phase339_survivor_ledger.csv", index=False)
    failures.to_csv(output_dir / "phase339_failure_and_limit_ledger.csv", index=False)
    decisions.to_csv(output_dir / "phase339_decision_ledger.csv", index=False)
    contract.to_csv(output_dir / "phase339_phase340_real_day_diagnostic_contract.csv", index=False)
    overlap.to_csv(output_dir / "phase339_real_event_overlap_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase339_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase339_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        acceptance,
        {
            "Survivor ledger": survivors,
            "Failure and limit ledger": failures,
            "Decision ledger": decisions,
            "Phase340 real-day diagnostic contract": contract,
            "Real/event overlap ledger": overlap,
            "Gates": gates,
        },
    )

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase339_cost_stress_holdout_validation_interpretation",
        **reproducibility_fields(
            artifact_id="phase339",
            generated_utc=generated_utc,
            inputs={
                "phase338_acceptance": str(phase338_dir / "phase338_acceptance_summary.csv"),
                "phase338_scenarios": str(phase338_dir / "phase338_holdout_scenario_summary.parquet"),
                "phase338_passive_diagnostics": str(phase338_dir / "phase338_passive_aware_diagnostic_ledger.csv"),
                "phase330_event_calendar": str(phase330_dir / "phase330_event_catalyst_expanded_feature_matrix.parquet"),
                "real_roots": ";".join(str(root) for root in real_roots),
            },
            parameters={
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "robust_event_floor": ROBUST_EVENT_FLOOR,
                "min_positive_symbol_date_cells": MIN_POSITIVE_SYMBOL_DATE_CELLS,
            },
            outputs={"acceptance_summary": str(output_dir / "phase339_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_interpretation_only",
        ),
    }
    (output_dir / "phase339_cost_stress_holdout_validation_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Interpret Phase338 cost-stress holdout validation.")
    parser.add_argument("--phase338-dir", type=Path, default=DEFAULT_PHASE338_DIR)
    parser.add_argument("--phase330-dir", type=Path, default=DEFAULT_PHASE330_DIR)
    parser.add_argument("--real-root", type=Path, action="append", default=None)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase338_dir, args.phase330_dir, args.real_root or DEFAULT_REAL_ROOTS, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
