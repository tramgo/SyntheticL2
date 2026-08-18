from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase363_liquidity_replenished_catalyst_impulse_diagnostic import (
    ANNUALIZED_THRESHOLD_PCT,
    FIXED_NOTIONAL_INR,
    INITIAL_CAPITAL_INR,
    ROBUST_EVENT_FLOOR,
    TRADING_DAYS_PER_YEAR,
)
from synthetic_l2.phase481_real_l2_capacity_sensitivity_precommit import (
    NEXT_ACTION as PHASE481_NEXT_ACTION,
    PHASE401_TRADES,
    PRIMARY_SCENARIO_ID,
    SIDE_FLIP_SCENARIO_ID,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE481_DIR = Path("outputs/phase481")
DEFAULT_OUTPUT_DIR = Path("outputs/phase482")
THESIS_ID = "P482_REAL_L2_CAPACITY_SENSITIVITY"
NEXT_ACTION_ACCEPTED_DIAGNOSTIC = "interpret_phase482_capacity_sensitivity_before_any_acceptance_no_paper_live"
NEXT_ACTION_REJECTED = "interpret_phase482_capacity_sensitivity_or_add_materially_new_real_l2_signal_no_paper_live"
REPAIR_ACTION = "repair_phase482_real_l2_capacity_sensitivity"


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def select_by_policy(frame: pd.DataFrame, policy: pd.Series) -> pd.DataFrame:
    out = frame.sort_values(["decision_ms", "canonical_work_order_id"], kind="mergesort").copy()
    out["capacity_selected"] = 0
    if as_int(policy.get("all_ready_events", 0)) == 1:
        out["capacity_selected"] = 1
        return out
    max_concurrent = as_int(policy.get("max_concurrent_positions", 0), 0)
    per_symbol_date_cap = as_int(policy.get("per_symbol_date_cap", 0), 0)
    per_trade_date_cap = as_int(policy.get("per_trade_date_cap", 0), 0)
    selected_ids: set[str] = set()
    if max_concurrent > 0:
        active_exits: list[int] = []
        for row in out.itertuples(index=False):
            active_exits = [x for x in active_exits if x > int(row.decision_ms)]
            if len(active_exits) < max_concurrent:
                selected_ids.add(str(row.canonical_work_order_id))
                active_exits.append(int(row.exit_ms))
    elif per_symbol_date_cap > 0:
        for _, group in out.groupby(["diagnostic_trade_date", "symbol"], sort=False):
            for value in group.head(per_symbol_date_cap)["canonical_work_order_id"].astype(str):
                selected_ids.add(value)
    elif per_trade_date_cap > 0:
        for _, group in out.groupby("diagnostic_trade_date", sort=False):
            for value in group.head(per_trade_date_cap)["canonical_work_order_id"].astype(str):
                selected_ids.add(value)
    out["capacity_selected"] = out["canonical_work_order_id"].astype(str).isin(selected_ids).astype(int)
    return out


def summarize_policy(trades: pd.DataFrame, policy: pd.Series) -> pd.DataFrame:
    rows = []
    policy_id = str(policy["capacity_policy_id"])
    policy_role = str(policy["policy_role"])
    acceptance_role = str(policy["acceptance_role"])
    for scenario_id, frame in trades.groupby("scenario_id", sort=False):
        selected = select_by_policy(frame, policy)
        cap = selected[selected["capacity_selected"].astype(int).eq(1)].copy()
        days = int(cap["diagnostic_trade_date"].nunique()) if not cap.empty else 0
        net = float(cap["net_pnl_inr"].sum()) if not cap.empty else 0.0
        annualized = (net / INITIAL_CAPITAL_INR) * (TRADING_DAYS_PER_YEAR / max(1, days)) * 100.0
        by_symbol = cap.groupby("symbol")["net_pnl_inr"].sum() if not cap.empty else pd.Series(dtype=float)
        by_symbol_date = cap.groupby(["symbol", "diagnostic_trade_date"])["net_pnl_inr"].sum() if not cap.empty else pd.Series(dtype=float)
        rows.append(
            {
                "capacity_policy_id": policy_id,
                "policy_role": policy_role,
                "acceptance_role": acceptance_role,
                "scenario_id": scenario_id,
                "scenario_role": str(frame["scenario_role"].iloc[0]),
                "scheduled_event_rows": int(len(frame)),
                "capacity_selected_trade_rows": int(len(cap)),
                "diagnostic_trade_dates": days,
                "symbols": int(cap["symbol"].nunique()) if not cap.empty else 0,
                "positive_trade_rows": int((cap["net_pnl_inr"] > 0).sum()) if not cap.empty else 0,
                "positive_symbols": int((by_symbol > 0).sum()) if not cap.empty else 0,
                "positive_symbol_date_cells": int((by_symbol_date > 0).sum()) if not cap.empty else 0,
                "net_pnl_inr": net,
                "annualized_return_pct": annualized,
                "above12": int(annualized > ANNUALIZED_THRESHOLD_PCT),
                "event_floor_met": int(len(cap) >= ROBUST_EVENT_FLOOR),
                "breadth_met": int((by_symbol > 0).sum() >= 2 and (by_symbol_date > 0).sum() >= 2),
                "capital_feasible": int(acceptance_role != "diagnostic_only"),
                "max_notional_if_concurrent_inr": float(as_int(policy.get("max_concurrent_positions", 0), 0) * FIXED_NOTIONAL_INR)
                if as_int(policy.get("max_concurrent_positions", 0), 0) > 0
                else "",
                "capital_ratio_if_concurrent": float(as_int(policy.get("max_concurrent_positions", 0), 0) * FIXED_NOTIONAL_INR / INITIAL_CAPITAL_INR)
                if as_int(policy.get("max_concurrent_positions", 0), 0) > 0
                else "",
            }
        )
    summary = pd.DataFrame(rows)
    if summary.empty:
        return summary
    primary_by_policy = summary[summary["scenario_id"].astype(str).eq(PRIMARY_SCENARIO_ID)].copy()
    side_by_policy = summary[summary["scenario_id"].astype(str).eq(SIDE_FLIP_SCENARIO_ID)].copy()
    side_map = dict(zip(side_by_policy["capacity_policy_id"], side_by_policy["annualized_return_pct"]))
    accepted = []
    for row in summary.itertuples(index=False):
        primary = str(row.scenario_id) == PRIMARY_SCENARIO_ID
        side_ann = float(side_map.get(row.capacity_policy_id, -1e9))
        beats_side_flip = int(float(row.annualized_return_pct) > side_ann) if primary else 0
        accepted.append(
            int(
                primary
                and int(row.capital_feasible) == 1
                and int(row.above12) == 1
                and int(row.event_floor_met) == 1
                and int(row.breadth_met) == 1
                and beats_side_flip == 1
            )
        )
    summary["beats_side_flip_control"] = [
        int(float(row.annualized_return_pct) > float(side_map.get(row.capacity_policy_id, -1e9))) if str(row.scenario_id) == PRIMARY_SCENARIO_ID else 0
        for row in summary.itertuples(index=False)
    ]
    summary["acceptance_candidate"] = accepted
    return summary.sort_values(["acceptance_candidate", "capital_feasible", "annualized_return_pct"], ascending=[False, False, False], kind="mergesort")


def build_policy_trades(trades: pd.DataFrame, catalog: pd.DataFrame) -> pd.DataFrame:
    frames = []
    for _, policy in catalog.iterrows():
        for scenario_id, frame in trades.groupby("scenario_id", sort=False):
            selected = select_by_policy(frame, policy)
            selected = selected.copy()
            selected.insert(0, "capacity_policy_id", str(policy["capacity_policy_id"]))
            selected.insert(1, "policy_role", str(policy["policy_role"]))
            selected.insert(2, "acceptance_role", str(policy["acceptance_role"]))
            frames.append(selected)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def build_gates(phase481: pd.DataFrame, catalog: pd.DataFrame, scenario_summary: pd.DataFrame, policy_trades: pd.DataFrame) -> pd.DataFrame:
    primary = scenario_summary[scenario_summary["scenario_id"].astype(str).eq(PRIMARY_SCENARIO_ID)].copy()
    feasible_primary = primary[primary["capital_feasible"].astype(int).eq(1)].copy()
    accepted = int(feasible_primary["acceptance_candidate"].astype(int).sum()) if not feasible_primary.empty else 0
    all_ready = primary[primary["capacity_policy_id"].astype(str).eq("P481_ALL_READY_DIAGNOSTIC")].copy()
    cost_ok = not policy_trades.empty and policy_trades["cost_model_version"].astype(str).eq(ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION).all()
    rows = [
        ("P482_PHASE481_PRECOMMIT_USED", as_int(scalar(phase481, "phase481_real_l2_capacity_sensitivity_precommit_complete", 0)) == 1, scalar(phase481, "phase481_real_l2_capacity_sensitivity_precommit_complete", 0), 1),
        ("P482_POLICY_GRID_MATCHES_PRECOMMIT", len(catalog) == 6 and int(scenario_summary["capacity_policy_id"].nunique()) == 6, int(scenario_summary["capacity_policy_id"].nunique()), 6),
        ("P482_NO_DOWNLOAD_USED", True, "reused_phase401_trade_ledger", "no_download"),
        ("P482_COST200_RETAINED", cost_ok, int(cost_ok), 1),
        ("P482_EVENT_FLOOR_EVALUATED", not primary.empty and int(primary["event_floor_met"].astype(int).max()) in [0, 1], int(primary["event_floor_met"].astype(int).max()) if not primary.empty else "", "evaluated"),
        ("P482_ALL_READY_DIAGNOSTIC_NOT_ACCEPTANCE", not all_ready.empty and all_ready["capital_feasible"].astype(int).eq(0).all(), "diagnostic_only", "diagnostic_only"),
        ("P482_ONLY_BASELINE_CAPITAL_FEASIBLE", int(primary["capital_feasible"].astype(int).sum()) == 1, int(primary["capital_feasible"].astype(int).sum()), 1),
        ("P482_ACCEPTANCE_CANDIDATE_EVALUATED", accepted >= 0, accepted, "evaluated"),
        ("P482_NO_PROMOTION_PAPER_LIVE_OR_CLAIM", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame(
        [{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows]
    )


def build_acceptance(gates: pd.DataFrame, scenario_summary: pd.DataFrame) -> pd.DataFrame:
    gate_pass = int(gates["passed"].astype(bool).sum())
    gate_rows = int(len(gates))
    primary = scenario_summary[scenario_summary["scenario_id"].astype(str).eq(PRIMARY_SCENARIO_ID)].copy()
    feasible_primary = primary[primary["capital_feasible"].astype(int).eq(1)].copy()
    best_feasible = feasible_primary.sort_values("annualized_return_pct", ascending=False, kind="mergesort").iloc[0].to_dict() if not feasible_primary.empty else {}
    best_any = primary.sort_values("annualized_return_pct", ascending=False, kind="mergesort").iloc[0].to_dict() if not primary.empty else {}
    accepted = int(feasible_primary["acceptance_candidate"].astype(int).sum()) if not feasible_primary.empty else 0
    return pd.DataFrame(
        [
            ("phase482_real_l2_capacity_sensitivity_complete", int(gate_pass == gate_rows), "Phase482 complete if all gates pass"),
            ("phase482_thesis_id", THESIS_ID, "Phase482 thesis"),
            ("phase482_capacity_policy_rows", int(scenario_summary["capacity_policy_id"].nunique()) if not scenario_summary.empty else 0, "Policies executed"),
            ("phase482_best_feasible_policy_id", best_feasible.get("capacity_policy_id", ""), "Best capital-feasible primary policy"),
            ("phase482_best_feasible_selected_trades", best_feasible.get("capacity_selected_trade_rows", ""), "Best feasible selected trades"),
            ("phase482_best_feasible_net_pnl_inr", best_feasible.get("net_pnl_inr", ""), "Best feasible net PnL"),
            ("phase482_best_feasible_annualized_return_pct", best_feasible.get("annualized_return_pct", ""), "Best feasible annualized return"),
            ("phase482_best_feasible_event_floor_met", best_feasible.get("event_floor_met", ""), "Best feasible event floor"),
            ("phase482_best_feasible_above12", best_feasible.get("above12", ""), "Best feasible above 12 percent"),
            ("phase482_best_feasible_beats_side_flip", best_feasible.get("beats_side_flip_control", ""), "Best feasible side-flip dominance"),
            ("phase482_best_any_primary_policy_id", best_any.get("capacity_policy_id", ""), "Best primary policy including diagnostic-only"),
            ("phase482_best_any_primary_selected_trades", best_any.get("capacity_selected_trade_rows", ""), "Best any selected trades"),
            ("phase482_best_any_primary_annualized_return_pct", best_any.get("annualized_return_pct", ""), "Best any annualized return"),
            ("phase482_cost200_acceptance_candidate_rows", accepted, "Capital-feasible accepted primary rows"),
            ("phase482_strategy_promotion_allowed", 0, "No promotion"),
            ("phase482_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase482_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase482_hard_gate_pass_rows", gate_pass, "Passed hard gates"),
            ("phase482_hard_gate_rows", gate_rows, "Hard gates"),
            ("phase482_next_best_action", NEXT_ACTION_ACCEPTED_DIAGNOSTIC if accepted > 0 else NEXT_ACTION_REJECTED, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, scenario_summary: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase482 Real-L2 Capacity Sensitivity",
        "",
        "Phase482 executes the frozen Phase481 capacity policy grid on the already-materialized Phase401 real-L2 trade ledger. No download and no signal rebuild were performed.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Scenario Summary",
        "",
        _markdown_table(scenario_summary),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: all-ready policy is diagnostic-only; no paper/live, no promotion, no deployable profitability claim.",
    ]
    (output_dir / "phase482_real_l2_capacity_sensitivity_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase481_dir: Path = DEFAULT_PHASE481_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase481 = read_csv(phase481_dir / "phase481_acceptance_summary.csv")
    catalog = read_csv(phase481_dir / "phase481_capacity_policy_catalog.csv")
    trades = read_csv(PHASE401_TRADES)
    if phase481.empty or catalog.empty or trades.empty:
        raise FileNotFoundError("Phase482 requires Phase481 precommit and Phase401 trade ledger.")
    scenario_summary = pd.concat([summarize_policy(trades, policy) for _, policy in catalog.iterrows()], ignore_index=True)
    policy_trades = build_policy_trades(trades, catalog)
    gates = build_gates(phase481, catalog, scenario_summary, policy_trades)
    acceptance = build_acceptance(gates, scenario_summary)
    scenario_summary.to_csv(output_dir / "phase482_scenario_summary.csv", index=False)
    policy_trades.to_csv(output_dir / "phase482_policy_trade_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase482_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase482_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, scenario_summary, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase482_real_l2_capacity_sensitivity",
        **reproducibility_fields(
            artifact_id="phase482_real_l2_capacity_sensitivity",
            generated_utc=generated_utc,
            inputs={
                "phase481_acceptance": str(phase481_dir / "phase481_acceptance_summary.csv"),
                "phase481_policy_catalog": str(phase481_dir / "phase481_capacity_policy_catalog.csv"),
                "phase401_trade_ledger": str(PHASE401_TRADES),
            },
            parameters={
                "phase481_next_action": PHASE481_NEXT_ACTION,
                "thesis_id": THESIS_ID,
                "primary_scenario_id": PRIMARY_SCENARIO_ID,
                "side_flip_scenario_id": SIDE_FLIP_SCENARIO_ID,
                "download_executed": False,
                "signal_rebuild_executed": False,
            },
            outputs={"acceptance_summary": str(output_dir / "phase482_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase482_reuses_phase401_event_timing",
        ),
    }
    (output_dir / "phase482_real_l2_capacity_sensitivity_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase482 real-L2 capacity sensitivity.")
    parser.add_argument("--phase481-dir", type=Path, default=DEFAULT_PHASE481_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    out = run(args.phase481_dir, args.output_dir)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
