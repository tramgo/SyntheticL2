from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase64")


def metric_value(path: Path, metric: str, default: Any = None) -> Any:
    frame = pd.read_csv(path)
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    value = rows.iloc[0]
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def as_int(value: Any) -> int:
    if pd.isna(value):
        return 0
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def as_float(value: Any) -> float:
    if pd.isna(value):
        return 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def build_strategy_family_ledger(base_dir: Path) -> pd.DataFrame:
    p53 = base_dir / "outputs/phase53/edge_diagnostics_summary.csv"
    p54 = base_dir / "outputs/phase54/selective_dense_replay_acceptance_summary.csv"
    p55 = base_dir / "outputs/phase55/cost_aware_edge_acceptance_summary.csv"
    p56 = base_dir / "outputs/phase56/cost_clearing_acceptance_summary.csv"
    p57 = base_dir / "outputs/phase57/interaction_ranker_acceptance_summary.csv"
    p58 = base_dir / "outputs/phase58/disjoint_candidate_acceptance_summary.csv"
    p59 = base_dir / "outputs/phase59/stability_acceptance_summary.csv"
    p60 = base_dir / "outputs/phase60/lower_frequency_acceptance_summary.csv"
    p61 = base_dir / "outputs/phase61/wider_sweep_acceptance_summary.csv"
    p62 = base_dir / "outputs/phase62/regime_symbol_acceptance_summary.csv"
    p63 = base_dir / "outputs/phase63/kotakbank_acceptance_summary.csv"

    rows = [
        {
            "strategy_family_id": "F01_dense_marketable_bruteforce",
            "phases": "52,53",
            "decision": "retired",
            "deployable": False,
            "best_evidence": "Phase53 found zero profitable aggregate strategy/profile rows after retail costs.",
            "primary_failure_mode": "costs_overwhelmed_dense_taker_signals",
            "gross_positive_evidence": as_int(metric_value(p53, "phase53_gross_positive_strategy_profiles")),
            "after_cost_positive_evidence": as_int(metric_value(p53, "phase53_profitable_strategy_profiles")),
            "net_pnl_inr": None,
            "trade_count": as_int(metric_value(p53, "phase53_dense_trade_rows_observed")),
            "scale_recommendation": as_int(metric_value(p53, "phase53_recommend_continue_phase52_bruteforce")),
            "required_next_action": "do_not_continue_bruteforce_shard_replay",
        },
        {
            "strategy_family_id": "F02_selective_marketable_controls",
            "phases": "54",
            "decision": "retired",
            "deployable": False,
            "best_evidence": "Phase54 produced one after-cost positive row only in nondeployable controls and zero deployable retail candidates.",
            "primary_failure_mode": "positive_only_under_nondeployable_control_assumptions",
            "gross_positive_evidence": None,
            "after_cost_positive_evidence": as_int(metric_value(p54, "phase54_positive_after_cost_rows")),
            "net_pnl_inr": as_float(metric_value(p54, "phase54_best_net_pnl_inr")),
            "trade_count": as_int(metric_value(p54, "phase54_trade_rows")),
            "scale_recommendation": as_int(metric_value(p54, "phase54_recommend_scale_to_full_year")),
            "required_next_action": "keep_as_control_not_live_candidate",
        },
        {
            "strategy_family_id": "F03_cost_aware_taker_edge_mining",
            "phases": "55",
            "decision": "retired",
            "deployable": False,
            "best_evidence": "Phase55 found no deployable positive after-cost candidates; the positive ceiling was oracle-only.",
            "primary_failure_mode": "oracle_positive_but_retail_deployable_negative",
            "gross_positive_evidence": as_int(metric_value(p55, "phase55_non_deployable_oracle_positive_rows")),
            "after_cost_positive_evidence": as_int(metric_value(p55, "phase55_deployable_positive_after_cost_rows")),
            "net_pnl_inr": as_float(metric_value(p55, "phase55_best_traded_deployable_net_pnl_inr")),
            "trade_count": as_int(metric_value(p55, "phase55_trade_rows")),
            "scale_recommendation": as_int(metric_value(p55, "phase55_recommend_scale_deployable_to_full_year")),
            "required_next_action": "do_not_scale_oracle_edges",
        },
        {
            "strategy_family_id": "F04_no_lookahead_dense_rule_labels",
            "phases": "56",
            "decision": "retired",
            "deployable": False,
            "best_evidence": "Phase56 evaluated 180 no-lookahead rules and found zero positive test rules after retail costs.",
            "primary_failure_mode": "no_test_rule_cleared_costs",
            "gross_positive_evidence": None,
            "after_cost_positive_evidence": as_int(metric_value(p56, "phase56_positive_test_rule_rows")),
            "net_pnl_inr": as_float(metric_value(p56, "phase56_best_traded_test_net_pnl_inr")),
            "trade_count": as_int(metric_value(p56, "phase56_rule_rows_evaluated")),
            "scale_recommendation": as_int(metric_value(p56, "phase56_recommend_scale_to_wider_dense_replay")),
            "required_next_action": "do_not_widen_dense_no_lookahead_rules",
        },
        {
            "strategy_family_id": "F05_supervised_interaction_cells",
            "phases": "57,58,59",
            "decision": "retired",
            "deployable": False,
            "best_evidence": "Phase57 found one candidate, but Phase58 emitted zero disjoint trades and Phase59 found zero positive stable validation rows.",
            "primary_failure_mode": "non_repeating_sparse_cell_and_failed_stability_validation",
            "gross_positive_evidence": as_int(metric_value(p57, "phase57_scale_candidate_rows")),
            "after_cost_positive_evidence": as_int(metric_value(p59, "phase59_positive_validation_rows")),
            "net_pnl_inr": as_float(metric_value(p59, "phase59_best_traded_validation_net_pnl_inr")),
            "trade_count": as_int(metric_value(p58, "phase58_trade_rows")),
            "scale_recommendation": as_int(metric_value(p59, "phase59_recommend_scale_to_month_sweep")),
            "required_next_action": "retire_sparse_interaction_cell_family",
        },
        {
            "strategy_family_id": "F06_lower_frequency_event_bar_momentum",
            "phases": "60,61,62,63",
            "decision": "retired",
            "deployable": False,
            "best_evidence": "Phase60 passed initial validation, then Phase61 lost -88,748.03 INR, Phase62 found only a tiny KOTAKBANK clue, and Phase63 falsified that clue at -24,100.26 INR.",
            "primary_failure_mode": "initial_validation_edge_did_not_survive_wider_symbol_month_falsification",
            "gross_positive_evidence": as_int(metric_value(p60, "phase60_scale_candidate_rows")),
            "after_cost_positive_evidence": as_int(metric_value(p63, "phase63_survives_kotakbank_falsification")),
            "net_pnl_inr": as_float(metric_value(p63, "phase63_net_pnl_inr")),
            "trade_count": as_int(metric_value(p63, "phase63_trades")),
            "scale_recommendation": 0,
            "required_next_action": str(metric_value(p63, "phase63_recommend_next_action")),
        },
        {
            "strategy_family_id": "F07_passive_limit_queue_capture",
            "phases": "64_next",
            "decision": "next_active_research_branch",
            "deployable": False,
            "best_evidence": "Marketable-taker families repeatedly failed after spread, slippage, impact and Zerodha charges; a different mechanism must be tested.",
            "primary_failure_mode": "not_yet_tested_and_passive_fills_are_unobserved_assumptions",
            "gross_positive_evidence": None,
            "after_cost_positive_evidence": None,
            "net_pnl_inr": None,
            "trade_count": None,
            "scale_recommendation": 1,
            "required_next_action": "implement_passive_queue_assumption_sensitivity_before_any_profit_claim",
        },
    ]
    ledger = pd.DataFrame(rows)
    ledger["can_continue_same_shard_family"] = ledger["decision"].eq("next_active_research_branch")
    return ledger


def build_next_research_queue() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "priority": 1,
                "research_item": "passive_limit_queue_capture_sensitivity",
                "phase": "65",
                "why_now": "All dense marketable-taker families are retired; passive queue capture is the nearest genuinely different L2 mechanism.",
                "minimum_deliverable": "Replay simulator with explicit queue-position assumptions, fill probability catalog, maker adverse-selection model and Zerodha cost handling.",
                "acceptance_gate": "Positive after-cost P&L must survive pessimistic, base and optimistic fill assumptions separately; no single assumed queue model may be enough.",
                "risk_note": "Zerodha top-five market-by-price data cannot directly observe order identity or true queue position.",
            },
            {
                "priority": 2,
                "research_item": "passive_adverse_selection_labels",
                "phase": "66",
                "why_now": "A passive order can earn spread only if post-fill adverse selection does not dominate.",
                "minimum_deliverable": "No-lookahead labels for whether a hypothetical bid/ask queue fill is followed by favorable or adverse mid-price movement.",
                "acceptance_gate": "Labels must be generated without future leakage and reported by symbol, time-of-day, spread bucket and depth bucket.",
                "risk_note": "Fill labels remain hypothetical until real broker fills or richer exchange/order data are available.",
            },
            {
                "priority": 3,
                "research_item": "strategy_stop_rule_and_experiment_budgeting",
                "phase": "67",
                "why_now": "The recent phases show how easy it is to over-iterate a dead family.",
                "minimum_deliverable": "Machine-readable stop/continue gates applied before large full-year runs.",
                "acceptance_gate": "A strategy family cannot request more shards unless it passes a predeclared out-of-sample gate.",
                "risk_note": "This protects compute and attention from false-positive chasing.",
            },
        ]
    )


def build_acceptance_summary(ledger: pd.DataFrame, next_queue: pd.DataFrame) -> pd.DataFrame:
    retired = ledger[ledger["decision"].eq("retired")]
    active = ledger[ledger["decision"].eq("next_active_research_branch")]
    marketable_retired = retired["strategy_family_id"].str.contains("marketable|taker|dense|event_bar|interaction|lookahead", case=False).sum()
    return pd.DataFrame(
        [
            ("phase64_strategy_families_reviewed", int(len(ledger)), "Strategy families in the decision ledger"),
            ("phase64_retired_family_count", int(len(retired)), "Families explicitly retired by evidence"),
            ("phase64_active_next_branch_count", int(len(active)), "New active research branches"),
            ("phase64_marketable_taker_family_retired_count", int(marketable_retired), "Retired marketable/taker-like families"),
            ("phase64_continue_phase60_shard_by_shard", 0, "0 means do not continue Phase60 shard-by-shard replay"),
            ("phase64_next_priority_research_item", str(next_queue.iloc[0]["research_item"]), "Highest-priority next experiment"),
            ("phase64_next_priority_phase", str(next_queue.iloc[0]["phase"]), "Suggested next phase number"),
            ("phase64_requires_passive_assumption_sensitivity", 1, "Passive fills require assumption sensitivity because true queue position is unavailable"),
            ("phase64_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha retail intraday cost model used by retired taker-family evidence"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase64 Strategy-Family Decision Ledger",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase64 converts the Phase53-63 evidence into a stop/continue ledger.",
        "The main decision is to stop continuing the failed marketable-taker momentum families shard-by-shard.",
        "The next branch is passive limit-order queue-capture research, handled as an assumption-sensitivity problem because the Zerodha top-five market-by-price feed does not reveal true queue position.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase64_strategy_family_decision_ledger_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase64(base_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    ledger = build_strategy_family_ledger(base_dir)
    next_queue = build_next_research_queue()
    acceptance = build_acceptance_summary(ledger, next_queue)

    ledger.to_csv(output_dir / "strategy_family_decision_ledger.csv", index=False)
    next_queue.to_csv(output_dir / "next_research_queue.csv", index=False)
    acceptance.to_csv(output_dir / "strategy_family_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Strategy Family Decision Ledger": ledger,
            "Next Research Queue": next_queue,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase64_strategy_family_decision_ledger",
        "retired_family_count": int(acceptance.loc[acceptance["metric"].eq("phase64_retired_family_count"), "value"].iloc[0]),
        "next_priority_research_item": str(
            acceptance.loc[acceptance["metric"].eq("phase64_next_priority_research_item"), "value"].iloc[0]
        ),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase64",
            generated_utc=generated_utc,
            inputs={
                "phase53_acceptance": "outputs/phase53/edge_diagnostics_summary.csv",
                "phase54_acceptance": "outputs/phase54/selective_dense_replay_acceptance_summary.csv",
                "phase55_acceptance": "outputs/phase55/cost_aware_edge_acceptance_summary.csv",
                "phase56_acceptance": "outputs/phase56/cost_clearing_acceptance_summary.csv",
                "phase57_acceptance": "outputs/phase57/interaction_ranker_acceptance_summary.csv",
                "phase58_acceptance": "outputs/phase58/disjoint_candidate_acceptance_summary.csv",
                "phase59_acceptance": "outputs/phase59/stability_acceptance_summary.csv",
                "phase60_acceptance": "outputs/phase60/lower_frequency_acceptance_summary.csv",
                "phase61_acceptance": "outputs/phase61/wider_sweep_acceptance_summary.csv",
                "phase62_acceptance": "outputs/phase62/regime_symbol_acceptance_summary.csv",
                "phase63_acceptance": "outputs/phase63/kotakbank_acceptance_summary.csv",
            },
            parameters={
                "decision_rule": "retire_family_when_wider_or_disjoint_validation_fails_after_retail_costs",
                "next_branch_rule": "activate_passive_queue_capture_only_as_assumption_sensitivity_research",
            },
            outputs={
                "ledger": str(output_dir / "strategy_family_decision_ledger.csv"),
                "next_queue": str(output_dir / "next_research_queue.csv"),
                "acceptance_summary": str(output_dir / "strategy_family_acceptance_summary.csv"),
                "report": str(output_dir / "phase64_strategy_family_decision_ledger_report.md"),
                "manifest": str(output_dir / "phase64_strategy_family_decision_ledger_manifest.json"),
            },
            random_seed="none_deterministic_decision_ledger",
            scenario_ids="phase64_phase53_to_phase63_decision_rollup",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_decision_ledger",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase64_strategy_family_decision_ledger_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Phase64 stop/continue decision ledger for tested strategy families.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase64(args.base_dir, args.output_dir)


if __name__ == "__main__":
    main()
