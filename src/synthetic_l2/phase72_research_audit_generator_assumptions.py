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


DEFAULT_OUTPUT_DIR = Path("outputs/phase72")


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


def build_family_audit(base_dir: Path) -> pd.DataFrame:
    ledger = pd.read_csv(base_dir / "outputs/phase64/strategy_family_decision_ledger.csv")
    phase65 = base_dir / "outputs/phase65/passive_acceptance_summary.csv"
    phase66 = base_dir / "outputs/phase66/passive_label_acceptance_summary.csv"
    phase68 = base_dir / "outputs/phase68/replenishment_acceptance_summary.csv"
    phase69 = base_dir / "outputs/phase69/spread_transition_acceptance_summary.csv"
    phase70 = base_dir / "outputs/phase70/lead_lag_acceptance_summary.csv"
    phase71 = base_dir / "outputs/phase71/shock_acceptance_summary.csv"
    rows = ledger.to_dict("records")
    rows.extend(
        [
            {
                "strategy_family_id": "F08_naive_passive_imbalance",
                "phases": "65,66",
                "decision": "retired",
                "deployable": False,
                "best_evidence": f"Phase65 had zero surviving queue profiles and best expected P&L {metric_value(phase65, 'phase65_best_expected_net_pnl_inr'):.2f} INR; Phase66 had zero adverse-selection label candidates.",
                "primary_failure_mode": "passive_touches_were_adverse_selection_traps",
                "net_pnl_inr": metric_value(phase65, "phase65_best_expected_net_pnl_inr"),
                "trade_count": metric_value(phase66, "phase66_inferred_touches"),
                "scale_recommendation": 0,
                "required_next_action": "do_not_widen_naive_passive_imbalance",
                "can_continue_same_shard_family": False,
            },
            {
                "strategy_family_id": "F09_replenishment_after_touch",
                "phases": "68",
                "decision": "retired",
                "deployable": False,
                "best_evidence": f"Phase68 best after-cost bucket was {metric_value(phase68, 'phase68_best_mean_after_cost_bps_if_touched'):.2f} bps with zero cost-clearing buckets.",
                "primary_failure_mode": "replenishment_improved_loss_but_did_not_clear_cost_or_adverse_selection",
                "net_pnl_inr": None,
                "trade_count": metric_value(phase68, "phase68_inferred_touches"),
                "scale_recommendation": 0,
                "required_next_action": "do_not_target_replenishment_replay",
                "can_continue_same_shard_family": False,
            },
            {
                "strategy_family_id": "F10_spread_transition",
                "phases": "69",
                "decision": "retired",
                "deployable": False,
                "best_evidence": f"Phase69 produced {metric_value(phase69, 'phase69_signal_rows'):.0f} labels but best after-cost bucket was {metric_value(phase69, 'phase69_best_mean_after_cost_bps'):.2f} bps.",
                "primary_failure_mode": "spread_transition_direction_did_not_clear_costs",
                "net_pnl_inr": None,
                "trade_count": metric_value(phase69, "phase69_signal_rows"),
                "scale_recommendation": 0,
                "required_next_action": "do_not_target_spread_transition_replay",
                "can_continue_same_shard_family": False,
            },
            {
                "strategy_family_id": "F11_cross_symbol_lead_lag",
                "phases": "70",
                "decision": "watchlist_near_miss",
                "deployable": False,
                "best_evidence": f"Phase70 best rule was positive at {metric_value(phase70, 'phase70_best_net_pnl_inr'):.2f} INR but failed precision/cost-drag gates.",
                "primary_failure_mode": "positive_pnl_but_precision_and_cost_drag_gate_failed",
                "net_pnl_inr": metric_value(phase70, "phase70_best_net_pnl_inr"),
                "trade_count": None,
                "scale_recommendation": 0,
                "required_next_action": "do_not_replay_without_feature_refinement_or_cost_reduction",
                "can_continue_same_shard_family": False,
            },
            {
                "strategy_family_id": "F12_shock_resilience",
                "phases": "71",
                "decision": "watchlist_near_miss",
                "deployable": False,
                "best_evidence": f"Phase71 best shock rule was positive at {metric_value(phase71, 'phase71_best_net_pnl_inr'):.2f} INR but failed sample-size gate.",
                "primary_failure_mode": "positive_shock_near_miss_but_insufficient_trade_count",
                "net_pnl_inr": metric_value(phase71, "phase71_best_net_pnl_inr"),
                "trade_count": None,
                "scale_recommendation": 0,
                "required_next_action": "audit_generator_shock_frequency_and_retest_only_if_sample_size_is_designed",
                "can_continue_same_shard_family": False,
            },
        ]
    )
    return pd.DataFrame(rows)


def build_near_miss_table(base_dir: Path) -> pd.DataFrame:
    phase70 = pd.read_csv(base_dir / "outputs/phase70/lead_lag_rule_results.csv")
    phase71 = pd.read_csv(base_dir / "outputs/phase71/shock_rule_results.csv")
    rows: list[dict[str, Any]] = []
    if not phase70.empty:
        top70 = phase70.iloc[0]
        rows.append(
            {
                "near_miss_id": "NM70_HDFCBANK_LEAD_LAG",
                "phase": 70,
                "rule_id": top70["rule_id"],
                "net_pnl_inr": float(top70["net_pnl_inr"]),
                "failed_gate": "precision_cost_clear_lt_0_55_and_cost_drag_gt_0_50_abs_gross",
                "diagnosis": "Positive P&L exists but is too dependent on large winners and too expensive relative to gross edge.",
                "allowed_next_action": "feature_refinement_only_no_disjoint_replay_yet",
            }
        )
    if not phase71.empty:
        top71 = phase71.iloc[0]
        rows.append(
            {
                "near_miss_id": "NM71_MARKET_SHOCK_MEAN_REVERSION",
                "phase": 71,
                "rule_id": top71["rule_id"],
                "net_pnl_inr": float(top71["net_pnl_inr"]),
                "failed_gate": "trades_lt_100",
                "diagnosis": "Positive shock mean-reversion row passes several quality tests but has only 72 trades.",
                "allowed_next_action": "generator_shock_frequency_audit_before_replay",
            }
        )
    return pd.DataFrame(rows)


def build_generator_assumption_review() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "assumption_area": "cost_drag_vs_signal_scale",
                "finding": "Most candidate gross edges are smaller than spread, slippage, impact and Zerodha retail charges.",
                "risk": "More shard replay will mostly measure cost drag, not discover deployable edge.",
                "recommended_change": "Prioritize lower-turnover event bars, stronger entry filters, or maker-only assumptions with explicit adverse-selection labels.",
            },
            {
                "assumption_area": "synthetic_spread_dynamics",
                "finding": "Phase69 found spread changes are present but sub-0.5 bps at the tested horizon.",
                "risk": "Spread-transition features may be too weak unless generator spread shocks or liquidity regime changes are more expressive.",
                "recommended_change": "Audit spread process calibration against real sample and add documented sensitivity scenarios for wider/narrower spread dynamics.",
            },
            {
                "assumption_area": "passive_fill_observability",
                "finding": "Passive fills remain inferred because Zerodha top-five market-by-price data lacks order identity and true queue position.",
                "risk": "Passive profitability can be overstated if queue assumptions are not pessimistic and sensitivity-tested.",
                "recommended_change": "Keep all passive results labeled hypothetical until real fills or richer queue data exist.",
            },
            {
                "assumption_area": "shock_frequency_and_sample_size",
                "finding": "Shock mean-reversion produced a positive near-miss but failed trade-count gates.",
                "risk": "Shock results can be one-scenario artifacts unless frequency and diversity are intentionally controlled.",
                "recommended_change": "Before replaying shock rules, audit shock schedule diversity and generate a scenario-balanced shock panel.",
            },
            {
                "assumption_area": "cross_symbol_alignment",
                "finding": "Cross-symbol lead-lag produced the strongest near-miss but failed precision and cost-drag gates.",
                "risk": "Event bars aligned by per-symbol local sequence may not represent synchronous tradable time.",
                "recommended_change": "Build a timestamp-aligned cross-symbol bar matrix before deciding whether lead-lag is genuinely dead.",
            },
        ]
    )


def build_acceptance_summary(family_audit: pd.DataFrame, near_misses: pd.DataFrame, assumptions: pd.DataFrame) -> pd.DataFrame:
    scale_ready = int(
        (
            family_audit["deployable"].fillna(False).astype(str).str.lower().eq("true")
            & (family_audit["scale_recommendation"].fillna(0).astype(float) > 0)
        ).sum()
    )
    return pd.DataFrame(
        [
            ("phase72_families_reviewed", int(len(family_audit)), "Strategy families reviewed across Phase52-71"),
            ("phase72_scale_ready_family_count", scale_ready, "Families currently allowed to scale"),
            ("phase72_near_miss_count", int(len(near_misses)), "Positive but non-scaling near misses"),
            ("phase72_generator_assumption_items", int(len(assumptions)), "Generator/execution assumption areas requiring review"),
            ("phase72_allow_more_full_year_strategy_replay_now", 0, "0 means do not launch another full-year strategy replay now"),
            ("phase72_recommend_next_action", "timestamp_aligned_cross_symbol_matrix_and_shock_panel_audit", "Next implementation focus"),
            ("phase72_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model retained for future gates"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase72 Research Audit and Generator-Assumption Review",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase72 consolidates the Phase52-71 strategy-mining evidence after multiple feature families failed bounded gates.",
        "The audit prevents another broad full-year replay until the generator/execution assumptions behind the near-misses are reviewed.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase72_research_audit_generator_assumptions_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase72(base_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    family_audit = build_family_audit(base_dir)
    near_misses = build_near_miss_table(base_dir)
    assumptions = build_generator_assumption_review()
    acceptance = build_acceptance_summary(family_audit, near_misses, assumptions)

    family_audit.to_csv(output_dir / "research_family_audit.csv", index=False)
    near_misses.to_csv(output_dir / "near_miss_watchlist.csv", index=False)
    assumptions.to_csv(output_dir / "generator_assumption_review.csv", index=False)
    acceptance.to_csv(output_dir / "research_audit_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Research Family Audit": family_audit,
            "Near-Miss Watchlist": near_misses,
            "Generator Assumption Review": assumptions,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase72_research_audit_generator_assumptions",
        "allow_more_full_year_strategy_replay_now": 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase72",
            generated_utc=generated_utc,
            inputs={
                "phase64_family_ledger": "outputs/phase64/strategy_family_decision_ledger.csv",
                "phase70_results": "outputs/phase70/lead_lag_rule_results.csv",
                "phase71_results": "outputs/phase71/shock_rule_results.csv",
            },
            parameters={
                "decision_rule": "audit_before_more_replay_when_all_bounded_feature_families_fail_scale_gates",
            },
            outputs={
                "family_audit": str(output_dir / "research_family_audit.csv"),
                "near_miss_watchlist": str(output_dir / "near_miss_watchlist.csv"),
                "generator_assumption_review": str(output_dir / "generator_assumption_review.csv"),
                "acceptance_summary": str(output_dir / "research_audit_acceptance_summary.csv"),
                "report": str(output_dir / "phase72_research_audit_generator_assumptions_report.md"),
                "manifest": str(output_dir / "phase72_research_audit_generator_assumptions_manifest.json"),
            },
            random_seed="none_deterministic_research_audit",
            scenario_ids="phase72_phase52_to_phase71_audit",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_research_audit",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase72_research_audit_generator_assumptions_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase72 research audit and generator assumption review.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase72(args.base_dir, args.output_dir)


if __name__ == "__main__":
    main()
