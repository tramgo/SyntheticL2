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
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE342_DIR = Path("outputs/phase342")
DEFAULT_OUTPUT_DIR = Path("outputs/phase343")

NEXT_ACTION = "run_phase344_official_catalyst_native_full_depth_strategy_search_precommit_no_paper_live"
REPAIR_ACTION = "repair_phase343_official_catalyst_real_day_diagnostic_interpretation"

PROFITABLE_ANNUALIZED_THRESHOLD_PCT = 12.0


def build_failure_ledger(phase342: pd.DataFrame, portfolio: pd.DataFrame) -> pd.DataFrame:
    capacity = portfolio[portfolio["scope"].eq("capacity_capped_portfolio_diagnostic")].iloc[0]
    isolated = portfolio[portfolio["scope"].eq("isolated_all_events_diagnostic")].iloc[0]
    rows = [
        {
            "failure_or_limit": "capacity_capped_real_diagnostic_negative",
            "observed": f"net_pnl={capacity['net_pnl_inr']};annualized={capacity['annualized_return_pct']}",
            "interpretation": "The fixed-capital capacity-capped official-catalyst real-L2 diagnostic is negative.",
        },
        {
            "failure_or_limit": "isolated_all_events_real_diagnostic_negative",
            "observed": f"net_pnl={isolated['net_pnl_inr']};annualized={isolated['annualized_return_pct']}",
            "interpretation": "The all-events isolated diagnostic is also negative, so the failure is not only a capacity allocator artifact.",
        },
        {
            "failure_or_limit": "current_synthetic_survivor_failed_real_transfer",
            "observed": metric_value(phase342, "phase342_capacity_capped_annualized_return_pct", ""),
            "interpretation": "The Phase338/339 synthetic survivor did not transfer profitably to official-catalyst real L2.",
        },
        {
            "failure_or_limit": "do_not_rescue_failed_survivor",
            "observed": "closed",
            "interpretation": "Do not rescue by lowering costs, using unlimited capital, weakening no-lookahead timing, changing to L1-only, or tuning the same failed route.",
        },
    ]
    return pd.DataFrame(rows)


def build_clue_ledger(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame()
    rows = []
    for scope, frame in [
        ("capacity_selected", trades[trades["capacity_selected"].astype(int).eq(1)].copy()),
        ("isolated_all_events", trades.copy()),
    ]:
        grouped = (
            frame.groupby("description", dropna=False)
            .agg(
                rows=("net_pnl_inr", "size"),
                positive_rows=("net_pnl_inr", lambda s: int((s > 0).sum())),
                net_pnl_inr=("net_pnl_inr", "sum"),
                avg_mid_return_bps=("mid_return_bps", "mean"),
                symbols=("symbol", "nunique"),
                dates=("diagnostic_trade_date", "nunique"),
            )
            .reset_index()
        )
        grouped["scope"] = scope
        grouped["diagnostic_clue_only"] = 1
        grouped["acceptance_allowed"] = 0
        rows.append(grouped)
    out = pd.concat(rows, ignore_index=True)
    return out.sort_values(["scope", "net_pnl_inr"], ascending=[True, False]).reset_index(drop=True)


def build_decision_ledger(phase342: pd.DataFrame, portfolio: pd.DataFrame, clues: pd.DataFrame) -> pd.DataFrame:
    cap_ann = float(metric_value(phase342, "phase342_capacity_capped_annualized_return_pct", 0.0))
    cap_net = float(metric_value(phase342, "phase342_capacity_capped_net_pnl_inr", 0.0))
    iso_ann = float(metric_value(phase342, "phase342_isolated_all_events_annualized_return_pct", 0.0))
    clue_rows = int(len(clues[clues["net_pnl_inr"].astype(float) > 0])) if not clues.empty else 0
    close_current = int(cap_ann <= PROFITABLE_ANNUALIZED_THRESHOLD_PCT or cap_net <= 0.0)
    rows = [
        ("phase342_execution_complete", 1, "Phase342 gates passed and produced official-catalyst real-L2 diagnostics.", "Interpretation may proceed."),
        ("current_survivor_route_profitable_real_diagnostic", int(cap_ann > PROFITABLE_ANNUALIZED_THRESHOLD_PCT and cap_net > 0.0), f"capacity_ann={cap_ann};capacity_net={cap_net}", "The current survivor route is not profitable on the official-catalyst real diagnostic."),
        ("current_survivor_route_closed", close_current, f"capacity_ann={cap_ann};isolated_ann={iso_ann}", "Close the Phase338/339 survivor route for acceptance."),
        ("diagnostic_clues_preserved", clue_rows, "Positive category/symbol pockets exist but are diagnostic only.", "Preserve clues for a material-new official-catalyst-native search."),
        ("next_route", "P344_OFFICIAL_CATALYST_NATIVE_FULL_DEPTH_STRATEGY_SEARCH_PRECOMMIT", NEXT_ACTION, "Search a materially different real official-catalyst/full-depth route; do not tune the failed synthetic survivor."),
        ("paper_live_or_profit_claim_allowed", 0, "closed", "No paper/live, promotion, or deployable profitability claim opens."),
    ]
    return pd.DataFrame(rows, columns=["decision_id", "decision_value", "evidence", "interpretation"])


def build_phase344_contract(clues: pd.DataFrame) -> pd.DataFrame:
    positive_capacity = clues[(clues["scope"].eq("capacity_selected")) & (clues["net_pnl_inr"].astype(float) > 0)].copy() if not clues.empty else pd.DataFrame()
    clue_descriptions = ";".join(positive_capacity["description"].astype(str).tolist()[:10]) if not positive_capacity.empty else ""
    rows = [
        ("input_real_trade_ledger", "outputs/phase342/phase342_real_day_trade_diagnostic_ledger.csv", "Use Phase342 official-catalyst real-L2 diagnostics as evidence, not as tuned labels."),
        ("input_official_calendar", "outputs/phase340/phase340_official_catalyst_calendar.csv", "Use official exchange catalyst rows, not synthetic event labels."),
        ("failed_survivor_closed", 1, "Do not continue the Phase338/339 synthetic survivor as an accepted or tuned route."),
        ("material_new_required", 1, "Next search must be official-catalyst-native and real-L2/full-depth, not a threshold tweak of the failed survivor."),
        ("preserved_diagnostic_clues", clue_descriptions, "Positive pockets such as catalyst categories may seed hypotheses but not acceptance."),
        ("full_top_five_depth_required", 1, "Use top-five bid/ask price, quantity, and order-count fields."),
        ("levels_2_to_5_materiality_required", 1, "Keep levels beyond L1 material to the strategy features."),
        ("l1_only_allowed", 0, "No L1-only variants."),
        ("no_lookahead_required", 1, "Keep Phase341 catalyst timing rules."),
        ("fixed_capital_denominator_required", 1, "No unlimited-capital return math."),
        ("cost_profile_required", "zerodha_2x_all_in_cost_proxy", "Keep 2x Zerodha all-in cost stress."),
        ("cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned cost formula."),
        ("annualized_threshold_pct", PROFITABLE_ANNUALIZED_THRESHOLD_PCT, "Keep user threshold."),
        ("paper_or_live_allowed", 0, "No paper/live acceptance."),
        ("deployable_profitability_claim_allowed", 0, "No deployable claim."),
        ("phase344_precommit_allowed_next", 1, "Open Phase344 precommit if Phase343 gates pass."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_gate_evaluation(phase342: pd.DataFrame, failures: pd.DataFrame, decisions: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(phase342, "phase342_official_catalyst_real_day_survivor_diagnostic_execution_complete", 0))
    cap_ann = float(metric_value(phase342, "phase342_capacity_capped_annualized_return_pct", 0.0))
    cap_net = float(metric_value(phase342, "phase342_capacity_capped_net_pnl_inr", 0.0))
    rows = [
        ("P343_PHASE342_COMPLETE", complete == 1, complete, 1),
        ("P343_REAL_DIAGNOSTIC_NEGATIVE_RECOGNIZED", cap_ann < PROFITABLE_ANNUALIZED_THRESHOLD_PCT and cap_net < 0, f"ann={cap_ann};net={cap_net}", "negative or below threshold"),
        ("P343_CURRENT_SURVIVOR_CLOSED", "current_survivor_route_closed" in decisions["decision_id"].astype(str).tolist(), "recorded", "recorded"),
        ("P343_NO_RESCUE_BOUNDARY_RECORDED", failures["failure_or_limit"].astype(str).eq("do_not_rescue_failed_survivor").any(), "recorded", "recorded"),
        ("P343_MATERIAL_NEW_CONTRACT_PRESENT", len(contract) >= 12, len(contract), ">=12"),
        ("P343_FULL_DEPTH_AND_NO_LOOKAHEAD_PRESERVED", contract.set_index("contract_id").loc["full_top_five_depth_required", "contract_value"] == 1 and contract.set_index("contract_id").loc["no_lookahead_required", "contract_value"] == 1, "preserved", "preserved"),
        ("P343_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", True, "closed", "closed"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed", "required"])


def write_outputs(phase342_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase342 = read_csv(phase342_dir / "phase342_acceptance_summary.csv")
    trades = pd.read_csv(phase342_dir / "phase342_real_day_trade_diagnostic_ledger.csv")
    portfolio = pd.read_csv(phase342_dir / "phase342_real_day_portfolio_summary.csv")
    failures = build_failure_ledger(phase342, portfolio)
    clues = build_clue_ledger(trades)
    decisions = build_decision_ledger(phase342, portfolio, clues)
    contract = build_phase344_contract(clues)
    gates = build_gate_evaluation(phase342, failures, decisions, contract)
    passed = int(gates["passed"].astype(bool).sum())
    total = int(len(gates))
    summary = pd.DataFrame(
        [
            ("phase343_official_catalyst_real_day_diagnostic_interpretation_complete", 1, "Phase343 interpretation completed"),
            ("phase343_phase342_complete", as_int(metric_value(phase342, "phase342_official_catalyst_real_day_survivor_diagnostic_execution_complete", 0)), "Phase342 complete"),
            ("phase343_capacity_capped_net_pnl_inr", metric_value(phase342, "phase342_capacity_capped_net_pnl_inr", ""), "Capacity-capped real diagnostic net PnL"),
            ("phase343_capacity_capped_annualized_return_pct", metric_value(phase342, "phase342_capacity_capped_annualized_return_pct", ""), "Capacity-capped real diagnostic annualized return"),
            ("phase343_current_survivor_route_closed", 1, "Current Phase338/339 survivor route closed for acceptance"),
            ("phase343_diagnostic_clue_rows", len(clues), "Diagnostic clue rows preserved"),
            ("phase343_positive_capacity_clue_rows", int(len(clues[(clues["scope"].eq("capacity_selected")) & (clues["net_pnl_inr"].astype(float) > 0)])) if not clues.empty else 0, "Positive capacity-selected clue rows"),
            ("phase343_selected_next_route", "P344_OFFICIAL_CATALYST_NATIVE_FULL_DEPTH_STRATEGY_SEARCH_PRECOMMIT", "Selected next route"),
            ("phase343_strategy_promotion_allowed", 0, "No promotion"),
            ("phase343_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase343_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase343_hard_gate_pass_rows", passed, "Passed hard gates"),
            ("phase343_hard_gate_rows", total, "Hard gates"),
            ("phase343_next_best_action", NEXT_ACTION if passed == total else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )
    report = "\n".join(
        [
            "# Phase343 Official-Catalyst Real-Day Diagnostic Interpretation",
            "",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
            "Phase343 closes the current synthetic survivor route for acceptance after negative official-catalyst real-L2 diagnostics.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Failure ledger",
            "",
            _markdown_table(failures),
            "",
            "## Decision ledger",
            "",
            _markdown_table(decisions),
            "",
            "## Top diagnostic clues",
            "",
            _markdown_table(clues.head(20)),
            "",
            "No promotion, paper/live acceptance, or deployable profitability claim is opened by Phase343.",
        ]
    )
    outputs = {
        "summary": output_dir / "phase343_acceptance_summary.csv",
        "failure_ledger": output_dir / "phase343_failure_and_limit_ledger.csv",
        "clue_ledger": output_dir / "phase343_diagnostic_clue_ledger.csv",
        "decision_ledger": output_dir / "phase343_decision_ledger.csv",
        "contract": output_dir / "phase343_phase344_material_new_contract.csv",
        "gates": output_dir / "phase343_gate_evaluation.csv",
        "report": output_dir / "phase343_official_catalyst_real_day_diagnostic_interpretation_report.md",
        "manifest": output_dir / "phase343_official_catalyst_real_day_diagnostic_interpretation_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    failures.to_csv(outputs["failure_ledger"], index=False)
    clues.to_csv(outputs["clue_ledger"], index=False)
    decisions.to_csv(outputs["decision_ledger"], index=False)
    contract.to_csv(outputs["contract"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    outputs["report"].write_text(report, encoding="utf-8")
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "phase": 343,
        "generated_at_utc": generated_utc,
        "phase342_dir": str(phase342_dir),
        "output_dir": str(output_dir),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase343",
            generated_utc=generated_utc,
            inputs={
                "phase342_acceptance": str(phase342_dir / "phase342_acceptance_summary.csv"),
                "phase342_trade_ledger": str(phase342_dir / "phase342_real_day_trade_diagnostic_ledger.csv"),
            },
            parameters={"annualized_threshold_pct": PROFITABLE_ANNUALIZED_THRESHOLD_PCT},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase342-dir", type=Path, default=DEFAULT_PHASE342_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase342_dir, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
