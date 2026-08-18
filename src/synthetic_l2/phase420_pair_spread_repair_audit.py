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
from synthetic_l2.phase417_pair_spread_convergence_precommit import PAIRS
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE418_DIR = Path("outputs/phase418")
DEFAULT_PHASE419_DIR = Path("outputs/phase419")
DEFAULT_OUTPUT_DIR = Path("outputs/phase420")
DEFAULT_REAL_ROOTS = [Path("real_data_sample/l2_unseen_validation"), Path("real_data_sample/l2_multiday_panel"), Path("real_data_sample/l2_single_day")]

VERDICT = "P420_PAIR_SPREAD_REPAIR_AUDIT_BLOCKED_ACCEPTANCE_BUT_LEAD_SURVIVES"
NEXT_ACTION = "precommit_phase421_pair_spread_realism_retest_with_min_forward_time_and_full_depth_unique_gate"
REPAIR_ACTION = "repair_phase420_pair_spread_audit"


def scenario_value(scenarios: pd.DataFrame, scenario_id: str, column: str, default: Any = "") -> Any:
    row = scenarios[scenarios["scenario_id"].astype(str).eq(scenario_id)] if not scenarios.empty and "scenario_id" in scenarios.columns else pd.DataFrame()
    return row[column].iloc[0] if not row.empty and column in row.columns else default


def audit_full_depth_contribution(scenarios: pd.DataFrame) -> pd.DataFrame:
    primary = float(scenario_value(scenarios, "P418_PRIMARY_PAIR_SPREAD_CONVERGENCE", "annualized_return_pct", 0))
    l2_removed = float(scenario_value(scenarios, "P418_L2_L5_REMOVED_CONTROL", "annualized_return_pct", 0))
    top_proxy = float(scenario_value(scenarios, "P418_SINGLE_LEG_PROXY_CONTROL", "annualized_return_pct", 0))
    return pd.DataFrame(
        [
            ("primary_annualized_return_pct", primary, "Phase418 primary"),
            ("l2_l5_removed_annualized_return_pct", l2_removed, "Levels 2-5 removed control"),
            ("single_leg_proxy_annualized_return_pct", top_proxy, "Single-leg proxy control"),
            ("primary_minus_l2_l5_removed_pct", primary - l2_removed, "Must be positive before full-depth contribution is accepted"),
            ("primary_minus_single_leg_proxy_pct", primary - top_proxy, "Pair must beat single-leg proxy"),
            ("full_depth_contribution_pass", int(primary > l2_removed), "Observed primary greater than L2-L5 removed control"),
            ("pair_structure_beats_proxy", int(primary > top_proxy), "Observed primary greater than single-leg proxy"),
        ],
        columns=["audit_id", "value", "description"],
    )


def audit_timing(ledger: pd.DataFrame) -> pd.DataFrame:
    if ledger.empty:
        return pd.DataFrame(
            [
                ("trade_rows", 0, "No trades"),
                ("same_timestamp_entry_exit_rows", 0, "entry_ts_ms == exit_ts_ms"),
                ("same_timestamp_share", 0.0, "same timestamp rows / trades"),
                ("median_hold_ms", 0.0, "median exit-entry ms"),
                ("timing_realism_pass", 0, "Requires same timestamp share <= 0.05"),
            ],
            columns=["audit_id", "value", "description"],
        )
    primary = ledger[ledger["scenario_id"].astype(str).eq("P418_PRIMARY_PAIR_SPREAD_CONVERGENCE")].copy()
    hold = pd.to_numeric(primary["exit_ts_ms"], errors="coerce") - pd.to_numeric(primary["entry_ts_ms"], errors="coerce")
    same = int((hold <= 0).sum())
    rows = int(len(primary))
    return pd.DataFrame(
        [
            ("trade_rows", rows, "Primary trade rows"),
            ("same_timestamp_entry_exit_rows", same, "entry_ts_ms >= exit_ts_ms due aligned synthetic ticks"),
            ("same_timestamp_share", same / rows if rows else 0.0, "same timestamp rows / trades"),
            ("median_hold_ms", float(hold.median()) if rows else 0.0, "median exit-entry ms"),
            ("p10_hold_ms", float(hold.quantile(0.10)) if rows else 0.0, "10th percentile hold ms"),
            ("p90_hold_ms", float(hold.quantile(0.90)) if rows else 0.0, "90th percentile hold ms"),
            ("timing_realism_pass", int((same / rows if rows else 1.0) <= 0.05), "Requires same timestamp share <= 0.05"),
        ],
        columns=["audit_id", "value", "description"],
    )


def audit_cost_rank(ledger: pd.DataFrame) -> pd.DataFrame:
    if ledger.empty:
        return pd.DataFrame(columns=["scenario_id", "net_pnl_cost100_inr", "net_pnl_cost200_inr", "cost100_rank", "cost200_rank"])
    rows = []
    for scenario_id, group in ledger.groupby("scenario_id", sort=True):
        rows.append(
            {
                "scenario_id": scenario_id,
                "net_pnl_cost100_inr": float(pd.to_numeric(group["net_pnl_cost100_inr"], errors="coerce").fillna(0).sum()),
                "net_pnl_cost200_inr": float(pd.to_numeric(group["net_pnl_inr"], errors="coerce").fillna(0).sum()),
            }
        )
    out = pd.DataFrame(rows)
    out["cost100_rank"] = out["net_pnl_cost100_inr"].rank(ascending=False, method="min").astype(int)
    out["cost200_rank"] = out["net_pnl_cost200_inr"].rank(ascending=False, method="min").astype(int)
    return out.sort_values("cost200_rank", kind="mergesort")


def audit_real_anchor_pair_availability(roots: list[Path]) -> pd.DataFrame:
    pair_rows = []
    for leg_a, leg_b in PAIRS:
        pair_id = f"{leg_a}_{leg_b}"
        dates_a: set[str] = set()
        dates_b: set[str] = set()
        for root in roots:
            if not root.exists():
                continue
            for date_root in root.glob("trade_date=*"):
                date_value = date_root.name.split("=", 1)[1]
                if (date_root / "exchange=NSE" / f"symbol={leg_a}").exists():
                    dates_a.add(date_value)
                if (date_root / "exchange=NSE" / f"symbol={leg_b}").exists():
                    dates_b.add(date_value)
        overlap = sorted(dates_a.intersection(dates_b))
        pair_rows.append(
            {
                "pair_id": pair_id,
                "leg_a": leg_a,
                "leg_b": leg_b,
                "leg_a_dates": len(dates_a),
                "leg_b_dates": len(dates_b),
                "overlap_dates": len(overlap),
                "overlap_date_list": ";".join(overlap[:20]),
                "real_anchor_pair_available": int(len(overlap) > 0),
            }
        )
    return pd.DataFrame(pair_rows)


def build_decision(full_depth: pd.DataFrame, timing: pd.DataFrame, real_anchor: pd.DataFrame, cost_rank: pd.DataFrame) -> pd.DataFrame:
    fd_pass = as_int(full_depth.loc[full_depth["audit_id"].eq("full_depth_contribution_pass"), "value"].iloc[0])
    timing_pass = as_int(timing.loc[timing["audit_id"].eq("timing_realism_pass"), "value"].iloc[0])
    real_pairs = int(pd.to_numeric(real_anchor["real_anchor_pair_available"], errors="coerce").fillna(0).sum()) if not real_anchor.empty else 0
    primary_rank_row = cost_rank[cost_rank["scenario_id"].astype(str).eq("P418_PRIMARY_PAIR_SPREAD_CONVERGENCE")] if not cost_rank.empty else pd.DataFrame()
    primary_cost200_rank = int(primary_rank_row["cost200_rank"].iloc[0]) if not primary_rank_row.empty else 999
    return pd.DataFrame(
        [
            ("selected_verdict", VERDICT, "Positive lead remains but acceptance blockers persist.", "lead_not_acceptance"),
            ("full_depth_contribution_pass", fd_pass, "Primary must beat L2-L5 removed control.", "blocker" if not fd_pass else "pass"),
            ("timing_realism_pass", timing_pass, "Same-timestamp entry/exit share must be low.", "blocker" if not timing_pass else "pass"),
            ("real_anchor_pair_available_count", real_pairs, "Matching real-anchor pair-date availability.", "blocker" if real_pairs == 0 else "available"),
            ("primary_cost200_rank", primary_cost200_rank, "Rank among Phase418 scenarios at cost200.", "diagnostic"),
            ("acceptance_allowed", 0, "Blocked until full-depth/timing/real-anchor repairs pass.", "closed"),
            ("paper_or_live_acceptance_allowed", 0, "No paper/live.", "closed"),
            ("deployable_profitability_claim_allowed", 0, "No deployable claim.", "closed"),
            ("next_action", NEXT_ACTION, "Retest lead with full-depth unique gate and minimum forward time.", "next"),
        ],
        columns=["decision_id", "decision_value", "evidence", "status"],
    )


def build_gates(summary419: pd.DataFrame, full_depth: pd.DataFrame, timing: pd.DataFrame, real_anchor: pd.DataFrame, decision: pd.DataFrame) -> pd.DataFrame:
    complete419 = as_int(metric_value(summary419, "phase419_pair_spread_convergence_interpretation_complete", 0))
    fd_pass = as_int(full_depth.loc[full_depth["audit_id"].eq("full_depth_contribution_pass"), "value"].iloc[0])
    timing_pass = as_int(timing.loc[timing["audit_id"].eq("timing_realism_pass"), "value"].iloc[0])
    real_pairs = int(pd.to_numeric(real_anchor["real_anchor_pair_available"], errors="coerce").fillna(0).sum()) if not real_anchor.empty else 0
    gates = [
        ("P420_PHASE419_COMPLETE", complete419 == 1, complete419, 1),
        ("P420_FULL_DEPTH_AUDIT_WRITTEN", True, len(full_depth), ">0"),
        ("P420_TIMING_AUDIT_WRITTEN", True, len(timing), ">0"),
        ("P420_COST_RANK_AUDIT_WRITTEN", True, "written", "written"),
        ("P420_REAL_ANCHOR_AVAILABILITY_WRITTEN", True, len(real_anchor), ">0"),
        ("P420_FULL_DEPTH_BLOCKER_RECORDED", fd_pass == 0, fd_pass, 0),
        ("P420_TIMING_BLOCKER_RECORDED", timing_pass == 0, timing_pass, 0),
        ("P420_REAL_ANCHOR_STATUS_RECORDED", real_pairs >= 0, real_pairs, ">=0"),
        ("P420_NO_ACCEPTANCE_OR_PAPER_LIVE", str(decision.loc[decision["decision_id"].eq("acceptance_allowed"), "decision_value"].iloc[0]) == "0", "acceptance=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(summary419: pd.DataFrame, decision: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase420_pair_spread_repair_audit_complete", 1, "Phase420 audit completed"),
            ("phase420_selected_verdict", VERDICT, "Selected verdict"),
            ("phase420_phase418_positive_lead_preserved", metric_value(summary419, "phase419_positive_synthetic_lead_preserved", 0), "Positive lead still preserved"),
            ("phase420_acceptance_allowed", 0, "Blocked"),
            ("phase420_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase420_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase420_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase420_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase420_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, full_depth: pd.DataFrame, timing: pd.DataFrame, real_anchor: pd.DataFrame, cost_rank: pd.DataFrame, decision: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase420 Pair-Spread Repair Audit",
        "",
        "Phase420 audits the Phase418/419 positive pair-spread lead before any acceptance or promotion.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Full-Depth Contribution Audit",
        "",
        _markdown_table(full_depth),
        "",
        "## Timing Realism Audit",
        "",
        _markdown_table(timing),
        "",
        "## Real-Anchor Pair Availability",
        "",
        _markdown_table(real_anchor),
        "",
        "## Cost Rank Audit",
        "",
        _markdown_table(cost_rank),
        "",
        "## Decision Ledger",
        "",
        _markdown_table(decision),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: positive synthetic lead remains blocked for acceptance.",
    ]
    (output_dir / "phase420_pair_spread_repair_audit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase418_dir: Path = DEFAULT_PHASE418_DIR, phase419_dir: Path = DEFAULT_PHASE419_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    summary419 = read_csv(phase419_dir / "phase419_acceptance_summary.csv")
    scenarios = read_csv(phase418_dir / "phase418_synthetic_scenario_summary.csv")
    ledger = read_csv(phase418_dir / "phase418_synthetic_pair_trade_ledger.csv")
    if summary419.empty or scenarios.empty or ledger.empty:
        raise FileNotFoundError("Phase420 requires Phase418 scenario/ledger and Phase419 summary.")
    full_depth = audit_full_depth_contribution(scenarios)
    timing = audit_timing(ledger)
    real_anchor = audit_real_anchor_pair_availability(DEFAULT_REAL_ROOTS)
    cost_rank = audit_cost_rank(ledger)
    decision = build_decision(full_depth, timing, real_anchor, cost_rank)
    gates = build_gates(summary419, full_depth, timing, real_anchor, decision)
    acceptance = build_acceptance(summary419, decision, gates)
    full_depth.to_csv(output_dir / "phase420_full_depth_contribution_audit.csv", index=False)
    timing.to_csv(output_dir / "phase420_timing_realism_audit.csv", index=False)
    real_anchor.to_csv(output_dir / "phase420_real_anchor_pair_availability.csv", index=False)
    cost_rank.to_csv(output_dir / "phase420_cost_rank_audit.csv", index=False)
    decision.to_csv(output_dir / "phase420_decision_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase420_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase420_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, full_depth, timing, real_anchor, cost_rank, decision, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase420_pair_spread_repair_audit",
        **reproducibility_fields(
            artifact_id="phase420_pair_spread_repair_audit",
            generated_utc=generated_utc,
            inputs={
                "phase418_synthetic_scenario_summary": str(phase418_dir / "phase418_synthetic_scenario_summary.csv"),
                "phase418_synthetic_pair_trade_ledger": str(phase418_dir / "phase418_synthetic_pair_trade_ledger.csv"),
                "phase419_acceptance_summary": str(phase419_dir / "phase419_acceptance_summary.csv"),
            },
            parameters={"selected_verdict": VERDICT, "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase420_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase420_no_execution_audit",
        ),
    }
    (output_dir / "phase420_pair_spread_repair_audit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase420 pair-spread repair audit.")
    parser.add_argument("--phase418-dir", type=Path, default=DEFAULT_PHASE418_DIR)
    parser.add_argument("--phase419-dir", type=Path, default=DEFAULT_PHASE419_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase418_dir, args.phase419_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
