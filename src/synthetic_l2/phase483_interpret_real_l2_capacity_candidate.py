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
from synthetic_l2.phase363_liquidity_replenished_catalyst_impulse_diagnostic import INITIAL_CAPITAL_INR
from synthetic_l2.phase363_liquidity_replenished_catalyst_impulse_diagnostic import FIXED_NOTIONAL_INR, MAX_CONCURRENT_POSITIONS
from synthetic_l2.phase481_real_l2_capacity_sensitivity_precommit import PRIMARY_SCENARIO_ID, SIDE_FLIP_SCENARIO_ID
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE482_DIR = Path("outputs/phase482")
DEFAULT_OUTPUT_DIR = Path("outputs/phase483")
THESIS_ID = "P483_INTERPRET_REAL_L2_CAPACITY_CANDIDATE"
SELECTED_POLICY = "P481_BASELINE_MAX2_CONCURRENT"
SELECTED_VERDICT = "P483_RESEARCH_CANDIDATE_REQUIRES_INDEPENDENT_HOLDOUT"
REJECTED_VERDICT = "P483_CAPACITY_CANDIDATE_REJECTED_BY_CONCENTRATION_AND_DATE_ROBUSTNESS"
NEXT_ACTION = "precommit_independent_holdout_or_walk_forward_for_P481_MAX5_CONCURRENT_no_paper_live"
REJECTED_NEXT_ACTION = "stop_acceptance_for_phase482_candidate_or_require_materially_new_real_l2_signal_no_paper_live"
REPAIR_ACTION = "repair_phase483_capacity_candidate_interpretation"


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def selected_trades(policy_trades: pd.DataFrame, scenario_id: str = PRIMARY_SCENARIO_ID) -> pd.DataFrame:
    return policy_trades[
        policy_trades["capacity_policy_id"].astype(str).eq(SELECTED_POLICY)
        & policy_trades["scenario_id"].astype(str).eq(scenario_id)
        & policy_trades["capacity_selected"].astype(int).eq(1)
    ].copy()


def build_diagnostics(summary482: pd.DataFrame, policy_trades: pd.DataFrame) -> pd.DataFrame:
    primary = selected_trades(policy_trades, PRIMARY_SCENARIO_ID)
    side = selected_trades(policy_trades, SIDE_FLIP_SCENARIO_ID)
    by_date = primary.groupby("diagnostic_trade_date")["net_pnl_inr"].sum().sort_index() if not primary.empty else pd.Series(dtype=float)
    by_symbol = primary.groupby("symbol")["net_pnl_inr"].sum().sort_values(ascending=False) if not primary.empty else pd.Series(dtype=float)
    top_date_share = float(by_date.max() / primary["net_pnl_inr"].sum()) if not by_date.empty and float(primary["net_pnl_inr"].sum()) > 0 else 0.0
    top_symbol_share = float(by_symbol.max() / primary["net_pnl_inr"].sum()) if not by_symbol.empty and float(primary["net_pnl_inr"].sum()) > 0 else 0.0
    notional_cap = MAX_CONCURRENT_POSITIONS * FIXED_NOTIONAL_INR
    return pd.DataFrame(
        [
            ("selected_policy", SELECTED_POLICY, "Best capital-feasible Phase482 primary policy."),
            ("primary_selected_trades", len(primary), "Capacity-selected primary trades."),
            ("primary_dates", int(primary["diagnostic_trade_date"].nunique()) if not primary.empty else 0, "Diagnostic dates represented."),
            ("primary_symbols", int(primary["symbol"].nunique()) if not primary.empty else 0, "Symbols represented."),
            ("primary_net_pnl_inr", float(primary["net_pnl_inr"].sum()) if not primary.empty else 0.0, "Selected primary net PnL."),
            ("primary_positive_date_rows", int((by_date > 0).sum()) if not by_date.empty else 0, "Positive dates."),
            ("primary_positive_date_fraction", float((by_date > 0).mean()) if not by_date.empty else 0.0, "Positive-date fraction."),
            ("primary_positive_symbol_rows", int((by_symbol > 0).sum()) if not by_symbol.empty else 0, "Positive symbols."),
            ("top_date_net_share", top_date_share, "Top profitable date contribution divided by total net PnL."),
            ("top_symbol_net_share", top_symbol_share, "Top profitable symbol contribution divided by total net PnL."),
            ("side_flip_net_pnl_inr", float(side["net_pnl_inr"].sum()) if not side.empty else 0.0, "Same policy side-flip net PnL."),
            ("capital_notional_cap_inr", notional_cap, "Max5 concurrent positions times INR 100,000 notional."),
            ("initial_capital_inr", INITIAL_CAPITAL_INR, "Pinned capital denominator."),
            ("capital_feasible_ratio", notional_cap / INITIAL_CAPITAL_INR, "Max simultaneous notional divided by capital."),
            ("phase482_acceptance_candidate_rows", scalar(summary482, "phase482_cost200_acceptance_candidate_rows", ""), "Phase482 candidate rows."),
        ],
        columns=["diagnostic_id", "value", "description"],
    )


def build_contribution_tables(policy_trades: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    primary = selected_trades(policy_trades, PRIMARY_SCENARIO_ID)
    if primary.empty:
        return pd.DataFrame(), pd.DataFrame()
    by_date = primary.groupby("diagnostic_trade_date", as_index=False).agg(
        selected_trades=("canonical_work_order_id", "count"),
        net_pnl_inr=("net_pnl_inr", "sum"),
        symbols=("symbol", lambda s: int(pd.Series(s).nunique())),
    )
    by_date["positive"] = (by_date["net_pnl_inr"] > 0).astype(int)
    by_symbol = primary.groupby("symbol", as_index=False).agg(
        selected_trades=("canonical_work_order_id", "count"),
        net_pnl_inr=("net_pnl_inr", "sum"),
        dates=("diagnostic_trade_date", lambda s: int(pd.Series(s).nunique())),
    )
    by_symbol["positive"] = (by_symbol["net_pnl_inr"] > 0).astype(int)
    return by_date.sort_values("diagnostic_trade_date", kind="mergesort"), by_symbol.sort_values("net_pnl_inr", ascending=False, kind="mergesort")


def diagnostic_value(diagnostics: pd.DataFrame, key: str, default: Any = "") -> Any:
    rows = diagnostics.loc[diagnostics["diagnostic_id"].eq(key), "value"]
    return rows.iloc[0] if not rows.empty else default


def build_gate_evaluation(summary482: pd.DataFrame, scenario482: pd.DataFrame, diagnostics: pd.DataFrame) -> pd.DataFrame:
    selected_row = scenario482[
        scenario482["capacity_policy_id"].astype(str).eq(SELECTED_POLICY)
        & scenario482["scenario_id"].astype(str).eq(PRIMARY_SCENARIO_ID)
    ].copy()
    selected = selected_row.iloc[0].to_dict() if not selected_row.empty else {}
    all_ready_row = scenario482[
        scenario482["capacity_policy_id"].astype(str).eq("P481_ALL_READY_DIAGNOSTIC")
        & scenario482["scenario_id"].astype(str).eq(PRIMARY_SCENARIO_ID)
    ].copy()
    positive_date_fraction = float(diagnostic_value(diagnostics, "primary_positive_date_fraction", 0.0))
    top_date_share = float(diagnostic_value(diagnostics, "top_date_net_share", 1.0))
    top_symbol_share = float(diagnostic_value(diagnostics, "top_symbol_net_share", 1.0))
    capital_ratio = float(diagnostic_value(diagnostics, "capital_feasible_ratio", 9.0))
    side_net = float(diagnostic_value(diagnostics, "side_flip_net_pnl_inr", 0.0))
    primary_net = float(diagnostic_value(diagnostics, "primary_net_pnl_inr", 0.0))
    rows = [
        ("P483_PHASE482_COMPLETE", as_int(scalar(summary482, "phase482_real_l2_capacity_sensitivity_complete", 0)) == 1, scalar(summary482, "phase482_real_l2_capacity_sensitivity_complete", 0), 1),
        ("P483_SELECTED_POLICY_CAPITAL_FEASIBLE", int(selected.get("capital_feasible", 0) or 0) == 1 and capital_ratio <= 1.0, f"capital_feasible={selected.get('capital_feasible','')};ratio={capital_ratio}", "true_and_ratio<=1"),
        ("P483_SELECTED_POLICY_EVENT_FLOOR_EVALUATED", selected.get("capacity_selected_trade_rows", "") != "", selected.get("capacity_selected_trade_rows", ""), "evaluated"),
        ("P483_SELECTED_POLICY_ABOVE12_EVALUATED", selected.get("annualized_return_pct", "") != "", selected.get("annualized_return_pct", ""), "evaluated"),
        ("P483_SELECTED_POLICY_BREADTH_EVALUATED", selected.get("symbols", "") != "", f"symbols={selected.get('symbols','')};dates={selected.get('diagnostic_trade_dates','')}", "evaluated"),
        ("P483_SIDE_FLIP_EVALUATED", side_net != 0.0 or primary_net != 0.0, f"primary={primary_net};side_flip={side_net}", "evaluated"),
        ("P483_POSITIVE_DATE_FRACTION_EVALUATED", positive_date_fraction >= 0.0, positive_date_fraction, "evaluated"),
        ("P483_CONCENTRATION_EVALUATED", top_date_share >= 0.0 and top_symbol_share >= 0.0, f"top_date={top_date_share};top_symbol={top_symbol_share}", "evaluated"),
        ("P483_ALL_READY_NOT_USED_FOR_ACCEPTANCE", not all_ready_row.empty and int(all_ready_row.iloc[0].get("capital_feasible", 1)) == 0, "diagnostic_only", "diagnostic_only"),
        ("P483_NO_PROMOTION_PAPER_LIVE_OR_CLAIM", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame(
        [{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows]
    )


def build_verdict(gates: pd.DataFrame, diagnostics: pd.DataFrame) -> pd.DataFrame:
    process_pass = bool(gates["passed"].astype(bool).all())
    positive_date_fraction = float(diagnostic_value(diagnostics, "primary_positive_date_fraction", 0.0))
    top_date_share = float(diagnostic_value(diagnostics, "top_date_net_share", 1.0))
    top_symbol_share = float(diagnostic_value(diagnostics, "top_symbol_net_share", 1.0))
    selected_row = read_csv(DEFAULT_PHASE482_DIR / "phase482_scenario_summary.csv")
    selected = selected_row[
        selected_row["capacity_policy_id"].astype(str).eq(SELECTED_POLICY)
        & selected_row["scenario_id"].astype(str).eq(PRIMARY_SCENARIO_ID)
    ].iloc[0]
    event_floor = int(selected.get("event_floor_met", 0) or 0)
    above12 = int(selected.get("above12", 0) or 0)
    breadth = int(selected.get("breadth_met", 0) or 0)
    candidate_quality_pass = process_pass and event_floor == 1 and above12 == 1 and breadth == 1 and positive_date_fraction >= 0.50 and top_date_share <= 0.60 and top_symbol_share <= 0.60
    verdict = SELECTED_VERDICT if candidate_quality_pass else REJECTED_VERDICT
    next_action = NEXT_ACTION if candidate_quality_pass else REJECTED_NEXT_ACTION
    return pd.DataFrame(
        [
            ("selected_verdict", verdict, "Phase482 max5 result can advance only if profitability is not too date/symbol concentrated.", "candidate" if candidate_quality_pass else "rejected"),
            ("event_floor_pass", event_floor, f"selected_trades={selected.get('capacity_selected_trade_rows', '')}", "quality_check"),
            ("above12_pass", above12, f"annualized_return_pct={selected.get('annualized_return_pct', '')}", "quality_check"),
            ("breadth_pass", breadth, f"symbols={selected.get('symbols', '')};dates={selected.get('diagnostic_trade_dates', '')}", "quality_check"),
            ("positive_date_fraction_pass", int(positive_date_fraction >= 0.50), f"positive_date_fraction={positive_date_fraction}", "quality_check"),
            ("concentration_pass", int(top_date_share <= 0.60 and top_symbol_share <= 0.60), f"top_date_share={top_date_share};top_symbol_share={top_symbol_share}", "quality_check"),
            ("paper_live_allowed", 0, "No paper/live from this interpretation.", "closed"),
            ("promotion_allowed", 0, "No strategy promotion from this interpretation.", "closed"),
            ("deployable_profitability_claim_allowed", 0, "No deployable profitability claim.", "closed"),
            ("next_action", next_action, "Do not tune Phase482 after seeing this result.", "next"),
        ],
        columns=["verdict_id", "verdict_value", "evidence", "status"],
    )


def build_acceptance(gates: pd.DataFrame, verdict: pd.DataFrame, diagnostics: pd.DataFrame) -> pd.DataFrame:
    gate_pass = int(gates["passed"].astype(bool).sum())
    gate_rows = int(len(gates))
    complete = int(gate_pass == gate_rows)
    selected_verdict = verdict.loc[verdict["verdict_id"].eq("selected_verdict"), "verdict_value"].iloc[0]
    research_candidate = int(selected_verdict == SELECTED_VERDICT)
    next_action = verdict.loc[verdict["verdict_id"].eq("next_action"), "verdict_value"].iloc[0]
    return pd.DataFrame(
        [
            ("phase483_interpret_real_l2_capacity_candidate_complete", complete, "Phase483 complete if all interpretation-process gates pass"),
            ("phase483_thesis_id", THESIS_ID, "Phase483 thesis"),
            ("phase483_selected_policy", SELECTED_POLICY, "Selected Phase482 policy"),
            ("phase483_selected_verdict", selected_verdict, "Selected verdict"),
            ("phase483_selected_trades", diagnostic_value(diagnostics, "primary_selected_trades", ""), "Selected primary trades"),
            ("phase483_net_pnl_inr", diagnostic_value(diagnostics, "primary_net_pnl_inr", ""), "Selected primary net PnL"),
            ("phase483_positive_date_fraction", diagnostic_value(diagnostics, "primary_positive_date_fraction", ""), "Positive-date fraction"),
            ("phase483_top_date_net_share", diagnostic_value(diagnostics, "top_date_net_share", ""), "Top date net contribution share"),
            ("phase483_top_symbol_net_share", diagnostic_value(diagnostics, "top_symbol_net_share", ""), "Top symbol net contribution share"),
            ("phase483_research_candidate_allowed", research_candidate, "Can advance only to independent holdout precommit"),
            ("phase483_strategy_promotion_allowed", 0, "No promotion"),
            ("phase483_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase483_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase483_hard_gate_pass_rows", gate_pass, "Passed hard gates"),
            ("phase483_hard_gate_rows", gate_rows, "Hard gates"),
            ("phase483_next_best_action", next_action if complete else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, diagnostics: pd.DataFrame, by_date: pd.DataFrame, by_symbol: pd.DataFrame, gates: pd.DataFrame, verdict: pd.DataFrame) -> None:
    lines = [
        "# Phase483 Interpret Real-L2 Capacity Candidate",
        "",
        "Phase483 interprets the Phase482 max5 concurrent capital-feasible candidate before any acceptance or paper/live claim.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Diagnostics",
        "",
        _markdown_table(diagnostics),
        "",
        "## Contribution by Date",
        "",
        _markdown_table(by_date),
        "",
        "## Contribution by Symbol",
        "",
        _markdown_table(by_symbol),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "## Verdict",
        "",
        _markdown_table(verdict),
        "",
        "Boundary: the result may advance to independent holdout precommit only; no promotion, paper/live, or deployable profitability claim.",
    ]
    (output_dir / "phase483_interpret_real_l2_capacity_candidate_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase482_dir: Path = DEFAULT_PHASE482_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    summary482 = read_csv(phase482_dir / "phase482_acceptance_summary.csv")
    scenario482 = read_csv(phase482_dir / "phase482_scenario_summary.csv")
    policy_trades = read_csv(phase482_dir / "phase482_policy_trade_ledger.csv")
    if summary482.empty or scenario482.empty or policy_trades.empty:
        raise FileNotFoundError("Phase483 requires Phase482 summary, scenario summary and policy trade ledger.")
    diagnostics = build_diagnostics(summary482, policy_trades)
    by_date, by_symbol = build_contribution_tables(policy_trades)
    gates = build_gate_evaluation(summary482, scenario482, diagnostics)
    verdict = build_verdict(gates, diagnostics)
    acceptance = build_acceptance(gates, verdict, diagnostics)
    diagnostics.to_csv(output_dir / "phase483_candidate_diagnostics.csv", index=False)
    by_date.to_csv(output_dir / "phase483_candidate_by_date.csv", index=False)
    by_symbol.to_csv(output_dir / "phase483_candidate_by_symbol.csv", index=False)
    gates.to_csv(output_dir / "phase483_gate_evaluation.csv", index=False)
    verdict.to_csv(output_dir / "phase483_verdict_ledger.csv", index=False)
    acceptance.to_csv(output_dir / "phase483_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, diagnostics, by_date, by_symbol, gates, verdict)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase483_interpret_real_l2_capacity_candidate",
        **reproducibility_fields(
            artifact_id="phase483_interpret_real_l2_capacity_candidate",
            generated_utc=generated_utc,
            inputs={
                "phase482_acceptance": str(phase482_dir / "phase482_acceptance_summary.csv"),
                "phase482_scenario_summary": str(phase482_dir / "phase482_scenario_summary.csv"),
                "phase482_policy_trade_ledger": str(phase482_dir / "phase482_policy_trade_ledger.csv"),
            },
            parameters={"selected_policy": SELECTED_POLICY, "verdict": verdict.loc[verdict["verdict_id"].eq("selected_verdict"), "verdict_value"].iloc[0]},
            outputs={"acceptance_summary": str(output_dir / "phase483_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase483_interpretation_only",
        ),
    }
    (output_dir / "phase483_interpret_real_l2_capacity_candidate_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase483 interpretation for Phase482 capacity candidate.")
    parser.add_argument("--phase482-dir", type=Path, default=DEFAULT_PHASE482_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    out = run(args.phase482_dir, args.output_dir)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
