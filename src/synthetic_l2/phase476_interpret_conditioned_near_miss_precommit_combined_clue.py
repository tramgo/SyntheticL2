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
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE358_DIR = Path("outputs/phase358")
DEFAULT_PHASE475_DIR = Path("outputs/phase475")
DEFAULT_OUTPUT_DIR = Path("outputs/phase476")

THESIS_ID = "P476_INTERPRET_CONDITIONED_NEAR_MISS_PRECOMMIT_COMBINED_CLUE"
NEXT_ACTION = "run_phase477_combined_shock_market_context_l2_fade_diagnostic"
MIN_ANNUALIZED_RETURN_PCT = 12.0
MIN_REAL_EVENT_FLOOR = 30


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def build_clue_comparison(phase358: pd.DataFrame, phase475: pd.DataFrame, phase475_scenarios: pd.DataFrame) -> pd.DataFrame:
    best475 = phase475_scenarios.sort_values(["annualized_return_pct", "net_pnl_inr"], ascending=False).iloc[0]
    required_net_for_12pct = 100_000.0 * (MIN_ANNUALIZED_RETURN_PCT / 100.0) * (float(best475["holdout_days"]) / 252.0)
    rows = [
        {
            "clue_id": "P358_REAL_OFFICIAL_CATALYST_MARKET_CONTEXT_FADE",
            "source": "real_official_catalyst_l2_panel",
            "status": "positive_but_sparse",
            "best_scenario": scalar(phase358, "phase358_primary_scenario_id", ""),
            "trade_rows": as_int(scalar(phase358, "phase358_primary_trade_rows", 0)),
            "event_or_holdout_days": as_int(scalar(phase358, "phase358_primary_diagnostic_trade_dates", 0)),
            "net_pnl_inr": float(scalar(phase358, "phase358_primary_net_pnl_inr", 0.0)),
            "annualized_return_pct": float(scalar(phase358, "phase358_primary_annualized_return_pct", 0.0)),
            "above_12pct": as_int(scalar(phase358, "phase358_primary_above12", 0)),
            "acceptance_candidate": as_int(scalar(phase358, "phase358_primary_acceptance_candidate", 0)),
            "main_limitation": "event_floor_not_met",
        },
        {
            "clue_id": "P475_SYNTHETIC_SHOCK_ONLY_NEAR_BREAK_EVEN",
            "source": "synthetic_distributional_l2_branch",
            "status": "negative_but_near_break_even",
            "best_scenario": str(best475["scenario_id"]),
            "trade_rows": int(best475["trade_count"]),
            "event_or_holdout_days": int(best475["holdout_days"]),
            "net_pnl_inr": float(best475["net_pnl_inr"]),
            "annualized_return_pct": float(best475["annualized_return_pct"]),
            "above_12pct": int(float(best475["annualized_return_pct"]) >= MIN_ANNUALIZED_RETURN_PCT),
            "acceptance_candidate": 0,
            "main_limitation": f"needs_{required_net_for_12pct - float(best475['net_pnl_inr']):.2f}_inr_more_net_for_12pct",
        },
    ]
    return pd.DataFrame(rows)


def build_permission_ledger(comparison: pd.DataFrame) -> pd.DataFrame:
    real = comparison[comparison["clue_id"].eq("P358_REAL_OFFICIAL_CATALYST_MARKET_CONTEXT_FADE")].iloc[0]
    synthetic = comparison[comparison["clue_id"].eq("P475_SYNTHETIC_SHOCK_ONLY_NEAR_BREAK_EVEN")].iloc[0]
    rows = [
        ("same_phase475_filter_grid_rescue_allowed", 0, "Phase475 had zero positive net scenarios; no same-family filter tweak."),
        ("phase358_route_promotion_allowed", 0, "Phase358 was positive but sparse and below real event floor."),
        ("combined_clue_followup_allowed", 1, "Both clues point to catalyst/shock context plus full-depth market-context fade."),
        ("paper_or_live_acceptance_allowed", 0, "No paper/live from sparse real clue or negative synthetic clue."),
        ("deployable_profitability_claim_allowed", 0, "No deployable claim until expanded real/synthetic validation passes."),
        ("real_event_floor_required", MIN_REAL_EVENT_FLOOR, "Acceptance must require broader official-catalyst real event count."),
        ("synthetic_shock_condition_required", "shock_only_or_official_catalyst_window", "Use catalyst/shock context as condition, not as direction label."),
        ("market_context_l2_fade_required", "depth_2_5_market_neutral_fade", "Carry the Phase358 positive real clue into the next test."),
        ("full_depth_l1_l5_required", 1, "Keep top-five market-by-price depth levels 1-5; levels 2-5 must be material."),
        ("zerodha_cost200_required", 1, "Keep Zerodha order-formula charges plus cost stress/slippage."),
        ("fixed_capital_annualization_required", 1, "No unlimited-capital annual return math."),
        ("phase358_net_pnl_inr", float(real["net_pnl_inr"]), "Real clue net P&L."),
        ("phase475_net_pnl_inr", float(synthetic["net_pnl_inr"]), "Synthetic near-miss net P&L."),
    ]
    return pd.DataFrame(rows, columns=["decision_id", "decision_value", "description"])


def build_phase477_contract() -> pd.DataFrame:
    rows = [
        ("phase477_thesis_id", "P477_COMBINED_SHOCK_MARKET_CONTEXT_L2_FADE_DIAGNOSTIC", "Material new combined-clue diagnostic."),
        ("source_clue_real", "P358_REAL_OFFICIAL_CATALYST_MARKET_CONTEXT_FADE", "Positive sparse real official-catalyst market-context fade clue."),
        ("source_clue_synthetic", "P475_SYNTHETIC_SHOCK_ONLY_NEAR_BREAK_EVEN", "Near-break-even synthetic shock-only clue."),
        ("use_closed_phase338_survivor", 0, "Do not reopen the closed Phase338/339 survivor route."),
        ("use_phase475_same_grid_only", 0, "Do not perform a same-horizon/same-filter rescue."),
        ("required_live_signal_family", "market_neutral_depth_2_5_fade_under_catalyst_or_shock_context", "Combined clue family."),
        ("required_depth_scope", "l1_l5_with_l2_l5_materiality", "Full Zerodha-style top-five depth required."),
        ("required_cost_scope", "zerodha_order_formula_plus_cost200", "Use real cost formula and stressed slippage."),
        ("required_capital_scope", "fixed_initial_capital", "Annualized returns use fixed capital denominator."),
        ("minimum_trade_rows_for_research_lead", 10, "Minimum diagnostic research rows."),
        ("minimum_real_event_rows_for_acceptance", MIN_REAL_EVENT_FLOOR, "No acceptance below real event floor."),
        ("strategy_promotion_allowed", 0, "No promotion in Phase477."),
        ("paper_or_live_acceptance_allowed", 0, "No paper/live in Phase477."),
        ("deployable_profitability_claim_allowed", 0, "No deployable claim in Phase477."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_gates(phase358: pd.DataFrame, phase475: pd.DataFrame, comparison: pd.DataFrame, permissions: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    perm = dict(zip(permissions["decision_id"].astype(str), permissions["decision_value"]))
    c = dict(zip(contract["contract_id"].astype(str), contract["contract_value"]))
    synthetic = comparison[comparison["clue_id"].eq("P475_SYNTHETIC_SHOCK_ONLY_NEAR_BREAK_EVEN")].iloc[0]
    real = comparison[comparison["clue_id"].eq("P358_REAL_OFFICIAL_CATALYST_MARKET_CONTEXT_FADE")].iloc[0]
    rows = [
        ("P476_PHASE475_COMPLETE", as_int(scalar(phase475, "phase475_catalyst_liquidity_conditioned_replay_complete", 0)) == 1, scalar(phase475, "phase475_catalyst_liquidity_conditioned_replay_complete", 0), 1),
        ("P476_PHASE475_REJECTION_CONFIRMED", as_int(scalar(phase475, "phase475_phase476_allowed_next", 1)) == 0, scalar(phase475, "phase475_phase476_allowed_next", 1), 0),
        ("P476_PHASE358_REAL_CLUE_COMPLETE", as_int(scalar(phase358, "phase358_full_depth_market_neutral_fade_execution_complete", 0)) == 1, scalar(phase358, "phase358_full_depth_market_neutral_fade_execution_complete", 0), 1),
        ("P476_PHASE358_POSITIVE_BUT_SPARSE_CONFIRMED", float(real["net_pnl_inr"]) > 0 and as_int(real["acceptance_candidate"]) == 0, f"net={real['net_pnl_inr']};acceptance={real['acceptance_candidate']}", "net>0;acceptance=0"),
        ("P476_PHASE475_NEAR_MISS_NEGATIVE_CONFIRMED", float(synthetic["net_pnl_inr"]) < 0 and float(synthetic["annualized_return_pct"]) > -5.0, f"net={synthetic['net_pnl_inr']};ann={synthetic['annualized_return_pct']}", "net<0;ann>-5"),
        ("P476_SAME_PHASE475_GRID_RESCUE_BLOCKED", as_int(perm.get("same_phase475_filter_grid_rescue_allowed", 1)) == 0, perm.get("same_phase475_filter_grid_rescue_allowed", ""), 0),
        ("P476_CLOSED_PHASE338_SURVIVOR_NOT_REOPENED", as_int(c.get("use_closed_phase338_survivor", 1)) == 0, c.get("use_closed_phase338_survivor", ""), 0),
        ("P476_COMBINED_FOLLOWUP_ALLOWED", as_int(perm.get("combined_clue_followup_allowed", 0)) == 1, perm.get("combined_clue_followup_allowed", ""), 1),
        ("P476_FULL_DEPTH_REQUIRED", str(c.get("required_depth_scope", "")) == "l1_l5_with_l2_l5_materiality", c.get("required_depth_scope", ""), "l1_l5_with_l2_l5_materiality"),
        ("P476_COST200_AND_FIXED_CAPITAL_REQUIRED", str(c.get("required_cost_scope", "")) == "zerodha_order_formula_plus_cost200" and str(c.get("required_capital_scope", "")) == "fixed_initial_capital", f"cost={c.get('required_cost_scope','')};capital={c.get('required_capital_scope','')}", "cost200;fixed"),
        ("P476_PHASE477_CONTRACT_PRESENT", str(c.get("phase477_thesis_id", "")).startswith("P477_"), c.get("phase477_thesis_id", ""), "P477_*"),
        ("P476_NO_PAPER_LIVE_OR_CLAIM", as_int(perm.get("paper_or_live_acceptance_allowed", 1)) == 0 and as_int(perm.get("deployable_profitability_claim_allowed", 1)) == 0, "paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    all_pass = int(hard_pass == hard_rows)
    rows = [
        ("phase476_interpret_conditioned_near_miss_precommit_complete", 1, "Phase476 interpretation/precommit completed"),
        ("phase476_thesis_id", THESIS_ID, "Phase476 thesis"),
        ("phase476_same_phase475_grid_rescue_allowed", 0, "Same-grid rescue remains blocked"),
        ("phase476_combined_clue_followup_allowed", all_pass, "Allows Phase477 combined-clue diagnostic if all gates pass"),
        ("phase476_strategy_promotion_allowed", 0, "No promotion"),
        ("phase476_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase476_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase476_phase477_allowed_next", all_pass, "Allows Phase477 execution only"),
        ("phase476_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase476_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase476_next_best_action", NEXT_ACTION if all_pass else "repair_phase476_combined_clue_contract", "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, comparison: pd.DataFrame, permissions: pd.DataFrame, contract: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase476 Interpret Conditioned Near-Miss and Precommit Combined Clue",
        "",
        "Phase476 interprets the Phase475 synthetic near-miss alongside the Phase358 real official-catalyst market-context fade clue.",
        "",
        "It blocks same-grid rescue and precommits a materially new Phase477 combined-clue diagnostic.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Clue Comparison",
        "",
        _markdown_table(comparison),
        "",
        "## Permission Ledger",
        "",
        _markdown_table(permissions),
        "",
        "## Phase477 Contract",
        "",
        _markdown_table(contract),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase476 is not a profitability claim. Phase477 may execute only the frozen combined-clue diagnostic.",
    ]
    (output_dir / "phase476_interpret_conditioned_near_miss_precommit_combined_clue_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase358_dir: Path = DEFAULT_PHASE358_DIR, phase475_dir: Path = DEFAULT_PHASE475_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase358 = read_csv(phase358_dir / "phase358_acceptance_summary.csv")
    phase475 = read_csv(phase475_dir / "phase475_acceptance_summary.csv")
    phase475_scenarios = read_csv(phase475_dir / "phase475_scenario_summary.csv")
    comparison = build_clue_comparison(phase358, phase475, phase475_scenarios)
    permissions = build_permission_ledger(comparison)
    contract = build_phase477_contract()
    gates = build_gates(phase358, phase475, comparison, permissions, contract)
    acceptance = build_acceptance(gates)
    comparison.to_csv(output_dir / "phase476_clue_comparison_ledger.csv", index=False)
    permissions.to_csv(output_dir / "phase476_permission_ledger.csv", index=False)
    contract.to_csv(output_dir / "phase476_phase477_contract.csv", index=False)
    gates.to_csv(output_dir / "phase476_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase476_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, comparison, permissions, contract, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase476_interpret_conditioned_near_miss_precommit_combined_clue",
        **reproducibility_fields(
            artifact_id="phase476_interpret_conditioned_near_miss_precommit_combined_clue",
            generated_utc=generated_utc,
            inputs={
                "phase358_acceptance": str(phase358_dir / "phase358_acceptance_summary.csv"),
                "phase475_acceptance": str(phase475_dir / "phase475_acceptance_summary.csv"),
                "phase475_scenarios": str(phase475_dir / "phase475_scenario_summary.csv"),
            },
            parameters={"thesis_id": THESIS_ID, "min_annualized_return_pct": MIN_ANNUALIZED_RETURN_PCT, "min_real_event_floor": MIN_REAL_EVENT_FLOOR},
            outputs={"acceptance_summary": str(output_dir / "phase476_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase476_precommit_no_execution",
        ),
    }
    (output_dir / "phase476_interpret_conditioned_near_miss_precommit_combined_clue_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase476 combined-clue interpretation/precommit.")
    parser.add_argument("--phase358-dir", type=Path, default=DEFAULT_PHASE358_DIR)
    parser.add_argument("--phase475-dir", type=Path, default=DEFAULT_PHASE475_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    out = run(args.phase358_dir, args.phase475_dir, args.output_dir)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
