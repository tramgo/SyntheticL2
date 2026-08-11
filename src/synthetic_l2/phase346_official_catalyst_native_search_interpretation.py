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


DEFAULT_PHASE345_DIR = Path("outputs/phase345")
DEFAULT_OUTPUT_DIR = Path("outputs/phase346")

ANNUALIZED_THRESHOLD_PCT = 12.0
ROBUST_EVENT_FLOOR = 30
NEXT_ACTION = "run_phase347_official_catalyst_event_count_expansion_precommit_no_paper_live"
REPAIR_ACTION = "repair_phase346_official_catalyst_native_search_interpretation"


def above_threshold_capacity(scenarios: pd.DataFrame) -> pd.DataFrame:
    frame = scenarios[
        scenarios["scope"].astype(str).eq("capacity_capped")
        & (scenarios["annualized_return_pct"].astype(float) > ANNUALIZED_THRESHOLD_PCT)
    ].copy()
    if frame.empty:
        return frame
    frame["trade_shortfall_to_floor"] = ROBUST_EVENT_FLOOR - frame["trade_rows"].astype(int)
    frame["trade_shortfall_to_floor"] = frame["trade_shortfall_to_floor"].clip(lower=0)
    frame["phase346_clue_tier"] = frame.apply(
        lambda row: "control_passing_sparse_high_return"
        if as_int(row["control_pass"]) == 1 and as_int(row["trade_rows"]) < ROBUST_EVENT_FLOOR
        else "control_failed_sparse_high_return"
        if as_int(row["control_pass"]) == 0
        else "unexpected_review",
        axis=1,
    )
    frame["paper_live_or_profit_claim_allowed"] = 0
    frame["phase347_candidate"] = (
        frame["control_pass"].astype(int).eq(1)
        & frame["trade_rows"].astype(int).lt(ROBUST_EVENT_FLOOR)
    ).astype(int)
    return frame.sort_values(
        ["phase347_candidate", "annualized_return_pct", "trade_rows"],
        ascending=[False, False, False],
    ).reset_index(drop=True)


def build_family_ledger(clues: pd.DataFrame) -> pd.DataFrame:
    if clues.empty:
        return pd.DataFrame(
            columns=[
                "family_id",
                "candidate_scenarios",
                "max_annualized_return_pct",
                "sum_net_pnl_inr",
                "max_trade_rows",
                "recommended_phase347_use",
            ]
        )
    grouped = (
        clues.groupby("family_id", dropna=False)
        .agg(
            candidate_scenarios=("phase347_candidate", "sum"),
            high_return_scenarios=("scenario_id", "size"),
            max_annualized_return_pct=("annualized_return_pct", "max"),
            sum_net_pnl_inr=("net_pnl_inr", "sum"),
            max_trade_rows=("trade_rows", "max"),
            control_passing_rows=("control_pass", "sum"),
        )
        .reset_index()
    )
    grouped["recommended_phase347_use"] = grouped.apply(
        lambda row: "carry_forward_with_event_count_expansion"
        if as_int(row["candidate_scenarios"]) > 0
        else "retain_as_negative_or_context_control",
        axis=1,
    )
    return grouped.sort_values(
        ["candidate_scenarios", "max_annualized_return_pct"],
        ascending=[False, False],
    ).reset_index(drop=True)


def build_decision_ledger(summary: pd.DataFrame, clues: pd.DataFrame, family: pd.DataFrame) -> pd.DataFrame:
    acceptance_rows = as_int(metric_value(summary, "phase345_acceptance_candidate_rows", 0))
    above12_rows = as_int(metric_value(summary, "phase345_capacity_above12_rows", 0))
    best_trade_rows = as_int(metric_value(summary, "phase345_best_capacity_trade_rows", 0))
    phase347_candidates = int(clues["phase347_candidate"].sum()) if not clues.empty else 0
    max_trade_rows = int(clues["trade_rows"].astype(int).max()) if not clues.empty else 0
    lead_family = str(family.iloc[0]["family_id"]) if not family.empty else ""
    rows = [
        (
            "phase345_search_complete",
            1,
            f"grid_rows={metric_value(summary, 'phase345_grid_rows', '')};trade_rows={metric_value(summary, 'phase345_trade_rows', '')}",
            "Interpretation may proceed.",
        ),
        (
            "profitable_strategy_claim_allowed",
            0,
            f"acceptance_candidate_rows={acceptance_rows}",
            "No deployable or accepted profitability claim opens because Phase345 accepted zero candidates.",
        ),
        (
            "high_return_pockets_exist",
            int(above12_rows > 0),
            f"capacity_above12_rows={above12_rows};best_trade_rows={best_trade_rows}",
            "The high-return pockets are real research clues, but sparse.",
        ),
        (
            "event_count_is_primary_blocker",
            int(phase347_candidates > 0 and max_trade_rows < ROBUST_EVENT_FLOOR),
            f"phase347_candidates={phase347_candidates};max_trade_rows={max_trade_rows};floor={ROBUST_EVENT_FLOOR}",
            "The next useful action is event-count expansion, not weaker controls or unlimited-capital math.",
        ),
        (
            "selected_phase347_lead_family",
            lead_family,
            "family ledger ranks control-passing sparse high-return pockets first",
            "Carry only control-passing sparse families into the next precommit.",
        ),
        (
            "paper_live_or_profit_claim_allowed",
            0,
            "closed",
            "No paper/live acceptance or deployable profitability claim.",
        ),
    ]
    return pd.DataFrame(rows, columns=["decision_id", "decision_value", "evidence", "interpretation"])


def build_phase347_contract(clues: pd.DataFrame, family: pd.DataFrame) -> pd.DataFrame:
    candidate = clues[clues["phase347_candidate"].astype(int).eq(1)].copy() if not clues.empty else pd.DataFrame()
    families = ";".join(family[family["recommended_phase347_use"].eq("carry_forward_with_event_count_expansion")]["family_id"].astype(str).tolist())
    scenario_ids = ";".join(candidate["scenario_id"].astype(str).tolist()[:20]) if not candidate.empty else ""
    rows = [
        ("input_phase345_summary", "outputs/phase345/phase345_acceptance_summary.csv", "Use Phase345 as the executed evidence base."),
        ("input_phase345_scenarios", "outputs/phase345/phase345_strategy_scenario_summary.csv", "Use capacity-capped scenario results."),
        ("phase345_acceptance_candidates_required", 0, "Phase347 must not inherit accepted status; there are no accepted candidates."),
        ("annualized_threshold_pct", ANNUALIZED_THRESHOLD_PCT, "Keep the user threshold."),
        ("minimum_trade_rows_required", ROBUST_EVENT_FLOOR, "Do not accept sparse results below the event floor."),
        ("fixed_capital_denominator_required", 1, "Annual return must remain fixed-capital based."),
        ("unlimited_capital_return_math_allowed", 0, "No unlimited-capital annualization."),
        ("official_catalyst_calendar_required", 1, "Use NSE/BSE/SEBI-style official catalyst rows as timestamp authority."),
        ("real_l2_event_matched_days_required", 1, "Expand only with real Zerodha-websocket-like top-five L2 days matched to official catalyst days."),
        ("full_top_five_depth_required", 1, "Use top-five bid/ask price, quantity, and order-count fields."),
        ("levels_2_to_5_materiality_required", 1, "Keep levels beyond L1 material to features and filters."),
        ("l1_only_allowed", 0, "No L1-only variants."),
        ("zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha intraday NSE equity charge formula."),
        ("cost_stress_required", "zerodha_2x_all_in_cost_proxy", "Keep the 2x all-in cost stress."),
        ("carry_forward_family_ids", families, "Families eligible for event-count expansion."),
        ("carry_forward_scenario_ids", scenario_ids, "Sparse high-return control-passing scenarios eligible for precommit."),
        ("paper_or_live_allowed", 0, "No paper/live acceptance."),
        ("deployable_profitability_claim_allowed", 0, "No deployable profitability claim."),
        ("phase347_precommit_allowed_next", int(not candidate.empty), "Open Phase347 only if sparse control-passing high-return clues exist."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_gate_evaluation(summary: pd.DataFrame, clues: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    phase345_complete = as_int(metric_value(summary, "phase345_official_catalyst_native_full_depth_strategy_search_execution_complete", 0))
    acceptance_rows = as_int(metric_value(summary, "phase345_acceptance_candidate_rows", 0))
    above12_rows = as_int(metric_value(summary, "phase345_capacity_above12_rows", 0))
    candidates = int(clues["phase347_candidate"].sum()) if not clues.empty else 0
    contract_index = contract.set_index("contract_id")
    rows = [
        ("P346_PHASE345_COMPLETE", phase345_complete == 1, phase345_complete, 1),
        ("P346_ZERO_ACCEPTANCE_RECOGNIZED", acceptance_rows == 0, acceptance_rows, 0),
        ("P346_HIGH_RETURN_CLUES_RECOGNIZED", above12_rows == len(clues), f"{len(clues)}/{above12_rows}", "all above12 rows"),
        ("P346_EVENT_COUNT_EXPANSION_CANDIDATES_RECORDED", candidates > 0, candidates, ">0"),
        ("P346_FULL_DEPTH_CONTRACT_PRESERVED", as_int(contract_index.loc["full_top_five_depth_required", "contract_value"]) == 1 and as_int(contract_index.loc["levels_2_to_5_materiality_required", "contract_value"]) == 1, "preserved", "preserved"),
        ("P346_OFFICIAL_CATALYST_AND_FIXED_CAPITAL_PRESERVED", as_int(contract_index.loc["official_catalyst_calendar_required", "contract_value"]) == 1 and as_int(contract_index.loc["fixed_capital_denominator_required", "contract_value"]) == 1, "preserved", "preserved"),
        ("P346_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", True, "closed", "closed"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed", "required"])


def write_outputs(phase345_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = read_csv(phase345_dir / "phase345_acceptance_summary.csv")
    scenarios = pd.read_csv(phase345_dir / "phase345_strategy_scenario_summary.csv")
    clues = above_threshold_capacity(scenarios)
    family = build_family_ledger(clues)
    decisions = build_decision_ledger(summary, clues, family)
    contract = build_phase347_contract(clues, family)
    gates = build_gate_evaluation(summary, clues, contract)
    passed = int(gates["passed"].astype(bool).sum())
    total = int(len(gates))
    next_action = NEXT_ACTION if passed == total and as_int(contract.set_index("contract_id").loc["phase347_precommit_allowed_next", "contract_value"]) == 1 else REPAIR_ACTION
    acceptance = pd.DataFrame(
        [
            ("phase346_official_catalyst_native_search_interpretation_complete", 1, "Phase346 interpretation completed"),
            ("phase346_phase345_complete", as_int(metric_value(summary, "phase345_official_catalyst_native_full_depth_strategy_search_execution_complete", 0)), "Phase345 complete"),
            ("phase346_phase345_acceptance_candidate_rows", as_int(metric_value(summary, "phase345_acceptance_candidate_rows", 0)), "Phase345 acceptance candidates"),
            ("phase346_capacity_above12_rows", len(clues), "Capacity-capped rows above 12%"),
            ("phase346_control_passing_sparse_candidate_rows", int(clues["phase347_candidate"].sum()) if not clues.empty else 0, "Control-passing sparse Phase347 candidate rows"),
            ("phase346_best_trade_rows", as_int(metric_value(summary, "phase345_best_capacity_trade_rows", 0)), "Best Phase345 capacity trade rows"),
            ("phase346_max_candidate_trade_rows", int(clues["trade_rows"].astype(int).max()) if not clues.empty else 0, "Maximum trade rows among high-return clues"),
            ("phase346_event_count_expansion_recommended", as_int(contract.set_index("contract_id").loc["phase347_precommit_allowed_next", "contract_value"]), "Event-count expansion recommended"),
            ("phase346_strategy_promotion_allowed", 0, "No promotion"),
            ("phase346_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase346_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase346_hard_gate_pass_rows", passed, "Passed hard gates"),
            ("phase346_hard_gate_rows", total, "Hard gates"),
            ("phase346_next_best_action", next_action, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )
    report = "\n".join(
        [
            "# Phase346 Official-Catalyst-Native Search Interpretation",
            "",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
            "Phase346 interprets Phase345 high-return pockets without opening paper/live acceptance or a profitability claim.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(acceptance),
            "",
            "## Candidate clue ledger",
            "",
            _markdown_table(clues.head(20)),
            "",
            "## Family ledger",
            "",
            _markdown_table(family),
            "",
            "## Decision ledger",
            "",
            _markdown_table(decisions),
            "",
            "## Phase347 execution contract",
            "",
            _markdown_table(contract),
            "",
            "The next branch is event-count expansion around official catalyst days using full top-five L2 depth. It is not a relaxation of controls.",
        ]
    )
    outputs = {
        "summary": output_dir / "phase346_acceptance_summary.csv",
        "clues": output_dir / "phase346_candidate_clue_ledger.csv",
        "family": output_dir / "phase346_family_interpretation_ledger.csv",
        "decisions": output_dir / "phase346_decision_ledger.csv",
        "contract": output_dir / "phase346_phase347_execution_contract.csv",
        "gates": output_dir / "phase346_gate_evaluation.csv",
        "report": output_dir / "phase346_official_catalyst_native_search_interpretation_report.md",
        "manifest": output_dir / "phase346_official_catalyst_native_search_interpretation_manifest.json",
    }
    acceptance.to_csv(outputs["summary"], index=False)
    clues.to_csv(outputs["clues"], index=False)
    family.to_csv(outputs["family"], index=False)
    decisions.to_csv(outputs["decisions"], index=False)
    contract.to_csv(outputs["contract"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    outputs["report"].write_text(report, encoding="utf-8")
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "phase": 346,
        "generated_at_utc": generated_utc,
        "phase345_dir": str(phase345_dir),
        "output_dir": str(output_dir),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase346_official_catalyst_native_search_interpretation",
            generated_utc=generated_utc,
            inputs={"phase345_dir": str(phase345_dir)},
            parameters={
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "robust_event_floor": ROBUST_EVENT_FLOOR,
            },
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": next_action,
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase345-dir", type=Path, default=DEFAULT_PHASE345_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase345_dir, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
