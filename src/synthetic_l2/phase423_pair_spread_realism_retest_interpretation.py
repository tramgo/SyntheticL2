from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase422_pair_spread_realism_retest_execution import NEXT_ACTION as PHASE422_NEXT_ACTION
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE422_DIR = Path("outputs/phase422")
DEFAULT_OUTPUT_DIR = Path("outputs/phase423")

VERDICT = "P423_PAIR_SPREAD_POSITIVE_LEAD_FALSIFIED_BY_REALISM_RETEST"
NEXT_ACTION = "stop_pair_spread_convergence_route_or_precommit_material_new_full_depth_source"
REPAIR_ACTION = "repair_phase423_interpretation_inputs"


def failed_gates(gates: pd.DataFrame) -> str:
    if gates.empty:
        return ""
    failed = gates.loc[gates["passed"].astype(str).str.lower().isin(["false", "0"])]
    return ";".join(failed["gate_id"].astype(str).tolist())


def scenario_value(scenarios: pd.DataFrame, scenario_id: str, column: str, default: object = "") -> object:
    if scenarios.empty or "scenario_id" not in scenarios.columns:
        return default
    row = scenarios[scenarios["scenario_id"].astype(str).eq(scenario_id)]
    return row[column].iloc[0] if not row.empty and column in row.columns else default


def build_decision(acceptance422: pd.DataFrame, gates422: pd.DataFrame, synthetic: pd.DataFrame, real_anchor: pd.DataFrame, syn_diag: pd.DataFrame, real_diag: pd.DataFrame) -> pd.DataFrame:
    syn_raw = int(pd.to_numeric(syn_diag.get("raw_selected_before_forward_filter", pd.Series(dtype=float)), errors="coerce").fillna(0).sum())
    syn_kept = int(pd.to_numeric(syn_diag.get("selected_trades", pd.Series(dtype=float)), errors="coerce").fillna(0).sum())
    real_raw = int(pd.to_numeric(real_diag.get("raw_selected_before_forward_filter", pd.Series(dtype=float)), errors="coerce").fillna(0).sum())
    real_kept = int(pd.to_numeric(real_diag.get("selected_trades", pd.Series(dtype=float)), errors="coerce").fillna(0).sum())
    real_ann = float(scenario_value(real_anchor, "P422_PRIMARY_PAIR_SPREAD_REALISM_RETEST", "annualized_return_pct", 0))
    real_net = float(scenario_value(real_anchor, "P422_PRIMARY_PAIR_SPREAD_REALISM_RETEST", "net_pnl_inr", 0))
    real_trades = int(scenario_value(real_anchor, "P422_PRIMARY_PAIR_SPREAD_REALISM_RETEST", "completed_round_trips", 0))
    real_dates = int(scenario_value(real_anchor, "P422_PRIMARY_PAIR_SPREAD_REALISM_RETEST", "trade_dates", 0))
    real_pairs = int(scenario_value(real_anchor, "P422_PRIMARY_PAIR_SPREAD_REALISM_RETEST", "pairs", 0))
    return pd.DataFrame(
        [
            ("selected_verdict", VERDICT, "Phase418 positive synthetic lead did not survive the precommitted Phase421 realism retest.", "terminal_for_this_route"),
            ("phase422_next_action_matched", PHASE422_NEXT_ACTION, "Phase423 implements the Phase422 next-action string.", "basis"),
            ("synthetic_raw_selections_before_forward_filter", syn_raw, "Synthetic signal opportunities existed before realism filtering.", "evidence"),
            ("synthetic_selections_after_forward_filter", syn_kept, "No synthetic trades survived the 250 ms forward-time filter.", "falsification"),
            ("synthetic_primary_completed_round_trips", metric_value(acceptance422, "phase422_primary_completed_round_trips", 0), "Synthetic primary after realism filter.", "falsification"),
            ("synthetic_primary_annualized_return_pct", metric_value(acceptance422, "phase422_primary_annualized_return_pct", 0), "Annualized return uses fixed INR 1,000,000 capital.", "falsification"),
            ("full_depth_unique_gate_passed", int(str(scenario_value(gates422, "P422_FULL_DEPTH_UNIQUE_GATE", "passed", "False")).lower() == "true"), "Full-depth L2-L5 edge did not beat the removed-depth control by the required margin.", "falsification"),
            ("forward_tick_exact_gate_passed", int(str(scenario_value(gates422, "P422_FORWARD_TICKS_ENFORCED", "passed", "False")).lower() == "true"), "Exact post-entry aligned tick indexing was not available, so the tick-count rule remains failed/proxy-only.", "caveat"),
            ("real_anchor_raw_selections_before_forward_filter", real_raw, "Real-anchor pair panel was active.", "real_anchor"),
            ("real_anchor_selections_after_forward_filter", real_kept, "Real-anchor trades survived timing filter.", "real_anchor"),
            ("real_anchor_primary_completed_round_trips", real_trades, "Real-anchor primary completed round trips.", "real_anchor_negative"),
            ("real_anchor_primary_trade_dates", real_dates, "Real-anchor date breadth.", "real_anchor_negative"),
            ("real_anchor_primary_pairs", real_pairs, "Real-anchor pair breadth.", "real_anchor_negative"),
            ("real_anchor_primary_net_pnl_inr", real_net, "Real-anchor cost200 net P&L.", "real_anchor_negative"),
            ("real_anchor_primary_annualized_return_pct", real_ann, "Real-anchor fixed-capital annualized return.", "real_anchor_negative"),
            ("same_family_tuning_allowed", 0, "Do not tune the same pair-spread convergence route after realism falsification.", "closed"),
            ("strategy_promotion_allowed", 0, "No accepted survivor.", "closed"),
            ("paper_or_live_acceptance_allowed", 0, "No paper/live acceptance.", "closed"),
            ("deployable_profitability_claim_allowed", 0, "No deployable claim.", "closed"),
            ("next_action", NEXT_ACTION, "Move to a materially new full-depth source if strategy search continues.", "next"),
        ],
        columns=["decision_id", "decision_value", "evidence", "status"],
    )


def build_durable_byproducts() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("pair_alignment_panel", "Pair tick alignment across synthetic and real-anchor panels remains reusable.", "preserve"),
            ("real_anchor_pair_loader", "Local real L2 loader normalizes symbol/trade_date metadata and top-five depth fields.", "preserve"),
            ("zerodha_cost200_pair_ledger", "Both synthetic and real-anchor ledgers retain gross, cost100, cost200 and net P&L.", "preserve"),
            ("forward_time_filter", "Minimum 250 ms forward-time realism filter is reusable.", "preserve"),
            ("forward_tick_index_repair", "Exact post-entry aligned tick count was not implemented in Phase422 and should be added before any future tick-count gate is claimed.", "required_if_reused"),
        ],
        columns=["artifact_id", "description", "status"],
    )


def build_gates(acceptance422: pd.DataFrame, gates422: pd.DataFrame, decision: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(acceptance422, "phase422_pair_spread_realism_retest_execution_complete", 0))
    hard_rows = int(metric_value(acceptance422, "phase422_hard_gate_rows", 0))
    hard_pass = int(metric_value(acceptance422, "phase422_hard_gate_pass_rows", 0))
    syn_trips = as_int(metric_value(acceptance422, "phase422_primary_completed_round_trips", 0))
    syn_ann = float(metric_value(acceptance422, "phase422_primary_annualized_return_pct", 0))
    verdict = str(decision.loc[decision["decision_id"].eq("selected_verdict"), "decision_value"].iloc[0])
    gates = [
        ("P423_PHASE422_COMPLETE", complete == 1, complete, 1),
        ("P423_PHASE422_GATES_EVALUATED", hard_rows == 17, hard_rows, 17),
        ("P423_PHASE422_FAILED_GATES_PRESENT", hard_pass < hard_rows and failed_gates(gates422) != "", f"passed={hard_pass}/{hard_rows};failed={failed_gates(gates422)}", "failed_gates_nonempty"),
        ("P423_SYNTHETIC_LEAD_ELIMINATED_BY_REALISM", syn_trips == 0 and syn_ann == 0.0, f"trips={syn_trips};annualized={syn_ann}", "zero_trades_after_forward_filter"),
        ("P423_REAL_ANCHOR_NEGATIVE_CONFIRMED", float(decision.loc[decision["decision_id"].eq("real_anchor_primary_annualized_return_pct"), "decision_value"].iloc[0]) < 0, decision.loc[decision["decision_id"].eq("real_anchor_primary_annualized_return_pct"), "decision_value"].iloc[0], "<0"),
        ("P423_FULL_DEPTH_UNIQUE_FAILURE_RECORDED", "P422_FULL_DEPTH_UNIQUE_GATE" in failed_gates(gates422), failed_gates(gates422), "contains_full_depth_gate"),
        ("P423_VERDICT_PRESENT", verdict == VERDICT, verdict, VERDICT),
        ("P423_NO_SAME_FAMILY_TUNING", str(decision.loc[decision["decision_id"].eq("same_family_tuning_allowed"), "decision_value"].iloc[0]) == "0", 0, 0),
        ("P423_BOUNDARIES_CLOSED", str(decision.loc[decision["decision_id"].eq("paper_or_live_acceptance_allowed"), "decision_value"].iloc[0]) == "0", "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(acceptance422: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase423_pair_spread_realism_retest_interpretation_complete", 1, "Phase423 interpretation completed"),
            ("phase423_selected_verdict", VERDICT, "Selected verdict"),
            ("phase423_phase422_primary_completed_round_trips", metric_value(acceptance422, "phase422_primary_completed_round_trips", 0), "Phase422 synthetic primary round trips"),
            ("phase423_phase422_primary_annualized_return_pct", metric_value(acceptance422, "phase422_primary_annualized_return_pct", 0), "Phase422 synthetic primary annualized return"),
            ("phase423_phase422_hard_gate_pass_rows", metric_value(acceptance422, "phase422_hard_gate_pass_rows", 0), "Phase422 hard gates passed"),
            ("phase423_phase422_hard_gate_rows", metric_value(acceptance422, "phase422_hard_gate_rows", 0), "Phase422 hard gates"),
            ("phase423_pair_spread_positive_lead_preserved", 0, "Lead is falsified for this route"),
            ("phase423_same_family_tuning_allowed", 0, "No same-family tuning"),
            ("phase423_strategy_promotion_allowed", 0, "No promotion"),
            ("phase423_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase423_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase423_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase423_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase423_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, decision: pd.DataFrame, byproducts: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase423 Pair-Spread Realism Retest Interpretation",
        "",
        "Phase423 formally interprets Phase422: the Phase418 positive pair-spread lead is falsified by the precommitted realism retest.",
        "",
        "The synthetic lead depended on same-timestamp or too-fast exits. After the 250 ms forward-time filter, synthetic primary trades fell to zero. The real-anchor pair replay was active, but it was negative after Zerodha cost200.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Decision Ledger",
        "",
        _markdown_table(decision),
        "",
        "## Durable Byproducts",
        "",
        _markdown_table(byproducts),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: the pair-spread convergence route is closed for acceptance. Continue only with a materially new full-depth L2 source or thesis.",
    ]
    (output_dir / "phase423_pair_spread_realism_retest_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase422_dir: Path = DEFAULT_PHASE422_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    acceptance422 = read_csv(phase422_dir / "phase422_acceptance_summary.csv")
    gates422 = read_csv(phase422_dir / "phase422_gate_evaluation.csv")
    synthetic = read_csv(phase422_dir / "phase422_synthetic_scenario_summary.csv")
    real_anchor = read_csv(phase422_dir / "phase422_real_anchor_scenario_summary.csv")
    syn_diag = read_csv(phase422_dir / "phase422_synthetic_pair_scan_diagnostics.csv")
    real_diag = read_csv(phase422_dir / "phase422_real_anchor_pair_scan_diagnostics.csv")
    if acceptance422.empty or gates422.empty or synthetic.empty or real_anchor.empty:
        raise FileNotFoundError("Phase423 requires Phase422 acceptance, gates, synthetic summary and real-anchor summary.")
    decision = build_decision(acceptance422, gates422, synthetic, real_anchor, syn_diag, real_diag)
    byproducts = build_durable_byproducts()
    gates = build_gates(acceptance422, gates422, decision)
    acceptance = build_acceptance(acceptance422, gates)
    decision.to_csv(output_dir / "phase423_decision_ledger.csv", index=False)
    byproducts.to_csv(output_dir / "phase423_durable_byproducts.csv", index=False)
    gates.to_csv(output_dir / "phase423_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase423_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, decision, byproducts, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase423_pair_spread_realism_retest_interpretation",
        **reproducibility_fields(
            artifact_id="phase423_pair_spread_realism_retest_interpretation",
            generated_utc=generated_utc,
            inputs={
                "phase422_acceptance_summary": str(phase422_dir / "phase422_acceptance_summary.csv"),
                "phase422_gate_evaluation": str(phase422_dir / "phase422_gate_evaluation.csv"),
                "phase422_synthetic_scenario_summary": str(phase422_dir / "phase422_synthetic_scenario_summary.csv"),
                "phase422_real_anchor_scenario_summary": str(phase422_dir / "phase422_real_anchor_scenario_summary.csv"),
            },
            parameters={"selected_verdict": VERDICT, "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase423_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase422_min_forward_time_retest",
        ),
    }
    (output_dir / "phase423_pair_spread_realism_retest_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase423 pair-spread realism retest interpretation.")
    parser.add_argument("--phase422-dir", type=Path, default=DEFAULT_PHASE422_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase422_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
