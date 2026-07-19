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


DEFAULT_OUTPUT_DIR = Path("outputs/phase88")


SUMMARY_FILES = {
    "phase41": Path("outputs/phase41/full_year_synthetic_tick_experiment_summary.csv"),
    "phase42": Path("outputs/phase42/native_full_year_l2_experiment_summary.csv"),
    "phase43": Path("outputs/phase43/cost_salvage_summary.csv"),
    "phase52": Path("outputs/phase52_checkpoint_smoke/dense_replay_acceptance_summary.csv"),
    "phase54": Path("outputs/phase54/selective_dense_replay_acceptance_summary.csv"),
    "phase55": Path("outputs/phase55/cost_aware_edge_acceptance_summary.csv"),
    "phase56": Path("outputs/phase56/cost_clearing_acceptance_summary.csv"),
    "phase60": Path("outputs/phase60/lower_frequency_acceptance_summary.csv"),
    "phase61": Path("outputs/phase61/wider_sweep_acceptance_summary.csv"),
    "phase63": Path("outputs/phase63/kotakbank_acceptance_summary.csv"),
    "phase77": Path("outputs/phase77/disjoint_month_acceptance_summary.csv"),
    "phase84": Path("outputs/phase84/cached_stratified_hdfcbank_acceptance_summary.csv"),
    "phase87": Path("outputs/phase87/precommitted_composite_replay_acceptance_summary.csv"),
}


def read_metric_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["metric", "value", "description"])
    return pd.read_csv(path)


def metric_value(tables: dict[str, pd.DataFrame], phase: str, metric: str, default: Any = None) -> Any:
    frame = tables.get(phase, pd.DataFrame())
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    value = rows.iloc[0]
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    return int(round(as_float(value, float(default))))


def build_profitability_ledger(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = [
        {
            "evidence_id": "P41_all_profile_synthetic_positive",
            "source_phase": "41",
            "strategy_scope": "deterministic full-year expansion across all model/profile rows",
            "positive_pocket_observed": True,
            "accepted_survivor": False,
            "best_net_pnl_inr": as_float(metric_value(tables, "phase41", "phase41_best_annualized_net_pnl_inr")),
            "realistic_or_retail_positive_rows": as_int(
                metric_value(tables, "phase41", "phase41_profitable_realistic_model_profile_rows")
            ),
            "total_trades_or_rows": as_int(metric_value(tables, "phase41", "phase41_trade_rows_loaded")),
            "failure_mode": "positive only outside realistic retail/stressed profiles",
            "decision": "not_deployable_evidence",
        },
        {
            "evidence_id": "P42_native_full_year_l2_negative",
            "source_phase": "42",
            "strategy_scope": "native full-year L2 event-state strategy/profile replay",
            "positive_pocket_observed": False,
            "accepted_survivor": False,
            "best_net_pnl_inr": as_float(metric_value(tables, "phase42", "phase42_best_annual_net_pnl_inr")),
            "realistic_or_retail_positive_rows": as_int(
                metric_value(tables, "phase42", "phase42_profitable_realistic_strategy_profile_rows")
            ),
            "total_trades_or_rows": as_int(metric_value(tables, "phase42", "phase42_total_strategy_trades")),
            "failure_mode": "all annual strategy/profile rows negative after costs",
            "decision": "retired",
        },
        {
            "evidence_id": "P43_cost_salvage_oracle_like_positive",
            "source_phase": "43",
            "strategy_scope": "cost-aware salvage variants across profiles",
            "positive_pocket_observed": True,
            "accepted_survivor": False,
            "best_net_pnl_inr": as_float(metric_value(tables, "phase43", "phase43_best_annual_net_pnl_inr")),
            "realistic_or_retail_positive_rows": as_int(
                metric_value(tables, "phase43", "phase43_positive_realistic_variant_profile_rows")
            ),
            "total_trades_or_rows": as_int(metric_value(tables, "phase43", "phase43_total_variant_trades")),
            "failure_mode": "positive variants did not survive realistic retail profiles",
            "decision": "retired",
        },
        {
            "evidence_id": "P52_dense_replay_checkpoint_negative",
            "source_phase": "52",
            "strategy_scope": "dense tick replay checkpoint",
            "positive_pocket_observed": False,
            "accepted_survivor": False,
            "best_net_pnl_inr": None,
            "realistic_or_retail_positive_rows": as_int(
                metric_value(tables, "phase52", "phase52_positive_after_cost_rows")
            ),
            "total_trades_or_rows": as_int(metric_value(tables, "phase52", "phase52_dense_replay_trade_rows")),
            "failure_mode": "zero positive strategy/profile rows after Zerodha retail costs",
            "decision": "do_not_continue_dense_bruteforce",
        },
        {
            "evidence_id": "P54_selective_control_positive",
            "source_phase": "54",
            "strategy_scope": "bounded selective dense replay",
            "positive_pocket_observed": True,
            "accepted_survivor": False,
            "best_net_pnl_inr": as_float(metric_value(tables, "phase54", "phase54_best_net_pnl_inr")),
            "realistic_or_retail_positive_rows": as_int(
                metric_value(tables, "phase54", "phase54_deployable_positive_after_cost_rows")
            ),
            "total_trades_or_rows": as_int(metric_value(tables, "phase54", "phase54_trade_rows")),
            "failure_mode": "positive only under nondeployable zero-latency/spread-only control",
            "decision": "control_only",
        },
        {
            "evidence_id": "P55_cost_aware_oracle_positive",
            "source_phase": "55",
            "strategy_scope": "cost-aware edge mining",
            "positive_pocket_observed": True,
            "accepted_survivor": False,
            "best_net_pnl_inr": as_float(metric_value(tables, "phase55", "phase55_best_any_net_pnl_inr")),
            "realistic_or_retail_positive_rows": as_int(
                metric_value(tables, "phase55", "phase55_deployable_positive_after_cost_rows")
            ),
            "total_trades_or_rows": as_int(metric_value(tables, "phase55", "phase55_trade_rows")),
            "failure_mode": "oracle ceiling positive but deployable candidate negative",
            "decision": "retired",
        },
        {
            "evidence_id": "P56_no_lookahead_rules_negative",
            "source_phase": "56",
            "strategy_scope": "no-lookahead cost-clearing rule discovery",
            "positive_pocket_observed": False,
            "accepted_survivor": False,
            "best_net_pnl_inr": as_float(metric_value(tables, "phase56", "phase56_best_traded_test_net_pnl_inr")),
            "realistic_or_retail_positive_rows": as_int(
                metric_value(tables, "phase56", "phase56_positive_test_rule_rows")
            ),
            "total_trades_or_rows": as_int(metric_value(tables, "phase56", "phase56_rule_rows_evaluated")),
            "failure_mode": "zero positive no-lookahead test rules after retail costs",
            "decision": "retired",
        },
        {
            "evidence_id": "P60_to_P61_lower_frequency_failed_wider_sweep",
            "source_phase": "60,61",
            "strategy_scope": "lower-frequency event-bar continuation candidate",
            "positive_pocket_observed": True,
            "accepted_survivor": False,
            "best_net_pnl_inr": as_float(metric_value(tables, "phase60", "phase60_best_traded_validation_net_pnl_inr")),
            "realistic_or_retail_positive_rows": as_int(metric_value(tables, "phase60", "phase60_scale_candidate_rows")),
            "total_trades_or_rows": as_int(metric_value(tables, "phase61", "phase61_trade_rows")),
            "failure_mode": (
                "initial validation candidate failed wider sweep with "
                f"net_pnl_inr={as_float(metric_value(tables, 'phase61', 'phase61_net_pnl_inr')):.2f}"
            ),
            "decision": "retired",
        },
        {
            "evidence_id": "P63_kotakbank_falsification",
            "source_phase": "63",
            "strategy_scope": "KOTAKBANK-only follow-up from Phase62 clue",
            "positive_pocket_observed": False,
            "accepted_survivor": False,
            "best_net_pnl_inr": as_float(metric_value(tables, "phase63", "phase63_net_pnl_inr")),
            "realistic_or_retail_positive_rows": as_int(
                metric_value(tables, "phase63", "phase63_survives_kotakbank_falsification")
            ),
            "total_trades_or_rows": as_int(metric_value(tables, "phase63", "phase63_trades")),
            "failure_mode": "single-symbol clue negative after costs",
            "decision": str(metric_value(tables, "phase63", "phase63_recommend_next_action")),
        },
        {
            "evidence_id": "P77_HDFCBANK_disjoint_month_failed",
            "source_phase": "77",
            "strategy_scope": "HDFCBANK lead-lag disjoint-month retest",
            "positive_pocket_observed": True,
            "accepted_survivor": False,
            "best_net_pnl_inr": as_float(metric_value(tables, "phase77", "phase77_total_net_pnl_inr")),
            "realistic_or_retail_positive_rows": as_int(
                metric_value(tables, "phase77", "phase77_hdfcbank_disjoint_retest_pass")
            ),
            "total_trades_or_rows": as_int(metric_value(tables, "phase77", "phase77_total_trades")),
            "failure_mode": "only 3 of 10 valid months positive and aggregate net P&L negative",
            "decision": str(metric_value(tables, "phase77", "phase77_recommend_next_action")),
        },
        {
            "evidence_id": "P84_HDFCBANK_cached_stratified_full_year_failed",
            "source_phase": "84",
            "strategy_scope": "cached stratified HDFCBANK full-year retest",
            "positive_pocket_observed": True,
            "accepted_survivor": False,
            "best_net_pnl_inr": as_float(metric_value(tables, "phase84", "phase84_total_net_pnl_inr")),
            "realistic_or_retail_positive_rows": as_int(
                metric_value(tables, "phase84", "phase84_cached_stratified_hdfcbank_pass")
            ),
            "total_trades_or_rows": as_int(metric_value(tables, "phase84", "phase84_total_trades")),
            "failure_mode": "full-year cached stratified retest lost materially after costs",
            "decision": str(metric_value(tables, "phase84", "phase84_recommend_next_action")),
        },
        {
            "evidence_id": "P87_precommitted_composite_family_failed",
            "source_phase": "87",
            "strategy_scope": "Phase86-precommitted composite event-intensity/absolute-move families",
            "positive_pocket_observed": True,
            "accepted_survivor": False,
            "best_net_pnl_inr": as_float(metric_value(tables, "phase87", "phase87_best_test_net_pnl_inr")),
            "realistic_or_retail_positive_rows": as_int(metric_value(tables, "phase87", "phase87_full_pass_candidates")),
            "total_trades_or_rows": as_int(metric_value(tables, "phase87", "phase87_precommitted_candidate_rows")),
            "failure_mode": "best test pocket failed train gates and no precommitted candidate passed both splits",
            "decision": str(metric_value(tables, "phase87", "phase87_recommend_next_action")),
        },
    ]
    return pd.DataFrame(rows)


def build_retirement_ledger(profitability: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "family_id": "DENSE_MARKETABLE_TAKER_MICRO_MOMENTUM",
                "source_evidence": "P42,P52,P54,P55,P56",
                "decision": "retired",
                "more_shards_allowed": False,
                "why": "Dense marketable/taker variants repeatedly fail after spread, slippage, impact and Zerodha retail charges.",
                "resume_condition": "Only if a new precommitted signal class has ex-ante expected edge above costs and uses disjoint validation before replay expansion.",
            },
            {
                "family_id": "LOWER_FREQUENCY_EVENT_BAR_CONTINUATION",
                "source_evidence": "P60,P61,P63",
                "decision": "retired",
                "more_shards_allowed": False,
                "why": "The Phase60 validation pocket did not survive wider symbol/month sweep or KOTAKBANK follow-up.",
                "resume_condition": "Do not resume this rule family; use only as a negative-control benchmark.",
            },
            {
                "family_id": "HDFCBANK_CROSS_SYMBOL_LEAD_LAG",
                "source_evidence": "P77,P84",
                "decision": "retired",
                "more_shards_allowed": False,
                "why": "Disjoint-month and cached stratified retests are aggregate negative with zero accepted pass months under the final gate.",
                "resume_condition": "Only a genuinely new cross-symbol feature with predeclared train/test/month gates may use HDFCBANK again.",
            },
            {
                "family_id": "COMPOSITE_EVENT_INTENSITY_ABS_MOVE",
                "source_evidence": "P85,P86,P87",
                "decision": "retired",
                "more_shards_allowed": False,
                "why": "The cost-budget design stage produced candidates, but locked replay found zero train/test/full survivors.",
                "resume_condition": "Do not widen thresholds; design a new feature class instead.",
            },
            {
                "family_id": "SYNTHETIC_PROFITABILITY_CLAIM",
                "source_evidence": ",".join(profitability["evidence_id"].astype(str).tolist()),
                "decision": "not_established",
                "more_shards_allowed": False,
                "why": "Positive pockets exist, but no dense tick-level retail-cost strategy has passed robustness, breadth and train/test gates.",
                "resume_condition": "A future profitability claim requires a precommitted survivor with after-cost P&L, breadth, positive-month persistence and adverse-selection controls.",
            },
        ]
    )


def build_next_feature_class_gate() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "priority": 1,
                "next_action_id": "P89_passive_queue_capture_cost_floor",
                "feature_class": "passive_limit_queue_capture_with_adverse_selection",
                "why_this_is_different": "It tests a different economic mechanism: earning spread/queue edge rather than paying spread as a taker.",
                "minimum_implementation": "Construct no-lookahead hypothetical passive fills at L1 with pessimistic/base/optimistic queue-position assumptions, adverse-selection markouts and Zerodha charge model.",
                "go_no_go_gate": "All fill-assumption tiers must report after-cost P&L, hit rate, adverse markout and positive-month breadth; optimistic-only success is not a survivor.",
            },
            {
                "priority": 2,
                "next_action_id": "P90_cross_symbol_regime_imbalance_precommit",
                "feature_class": "sector_or_index_conditioned_cross_symbol_imbalance",
                "why_this_is_different": "It lowers turnover and requires cross-sectional context rather than single-symbol dense twitch signals.",
                "minimum_implementation": "Precommit sector/index imbalance features, symbols, train/test months, max turnover and cost-budget thresholds before replay.",
                "go_no_go_gate": "Must beat Zerodha retail costs in train and test with no single symbol/month contributing the majority of P&L.",
            },
            {
                "priority": 3,
                "next_action_id": "P91_event_window_low_turnover_shock_response",
                "feature_class": "low_turnover_event_window_reversal_or_continuation",
                "why_this_is_different": "It trades fewer, larger expected moves where retail cost drag is less dominant.",
                "minimum_implementation": "Define shock windows from generator state and received-event features, then precommit entry/exit horizons and cost floors.",
                "go_no_go_gate": "Must pass disjoint-month validation and show gross edge comfortably above spread/slippage/impact/charges.",
            },
        ]
    )


def build_acceptance_summary(profitability: pd.DataFrame, retirement: pd.DataFrame, next_gate: pd.DataFrame) -> pd.DataFrame:
    accepted = int(profitability["accepted_survivor"].astype(bool).sum())
    positive_pockets = int(profitability["positive_pocket_observed"].astype(bool).sum())
    retired = int(retirement["decision"].astype(str).eq("retired").sum())
    more_shards_allowed = int(retirement["more_shards_allowed"].astype(bool).any())
    return pd.DataFrame(
        [
            ("phase88_profitability_evidence_rows", int(len(profitability)), "Profitability evidence rows reviewed"),
            ("phase88_positive_pocket_rows", positive_pockets, "Rows where some positive synthetic P&L pocket was observed"),
            ("phase88_accepted_survivor_rows", accepted, "Rows accepted as robust retail-cost survivors"),
            ("phase88_retired_family_rows", retired, "Strategy families retired by cumulative evidence"),
            ("phase88_more_same_family_shards_allowed", more_shards_allowed, "1 means continuing same-family shard replay is allowed"),
            ("phase88_next_best_action", str(next_gate.iloc[0]["next_action_id"]), "Recommended next milestone"),
            ("phase88_strategy_pivot_required", 1 if accepted == 0 else 0, "1 means pivot to a new feature class before more replay scale"),
            ("phase88_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha retail intraday cost model used by cited evidence"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase88 Strategy Pivot Decision Ledger",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase88 answers the post-Phase87 question: synthetic profitability pockets have appeared, but no dense tick-level retail-cost strategy family has produced an accepted survivor.",
        "The decision is to stop shard-by-shard continuation for the retired families and pivot to a new feature class with predeclared gates.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase88_strategy_pivot_decision_ledger_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase88(base_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    tables = {phase: read_metric_table(base_dir / path) for phase, path in SUMMARY_FILES.items()}
    profitability = build_profitability_ledger(tables)
    retirement = build_retirement_ledger(profitability)
    next_gate = build_next_feature_class_gate()
    acceptance = build_acceptance_summary(profitability, retirement, next_gate)

    profitability.to_csv(output_dir / "profitability_evidence_ledger.csv", index=False)
    retirement.to_csv(output_dir / "retired_strategy_family_ledger.csv", index=False)
    next_gate.to_csv(output_dir / "next_feature_class_gate.csv", index=False)
    acceptance.to_csv(output_dir / "strategy_pivot_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Profitability Evidence Ledger": profitability,
            "Retired Strategy Family Ledger": retirement,
            "Next Feature Class Gate": next_gate,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {"generated_utc": generated_utc, "scope": "phase88_strategy_pivot_decision_ledger"}
    manifest.update(
        reproducibility_fields(
            artifact_id="phase88",
            generated_utc=generated_utc,
            inputs={phase: str(path) for phase, path in SUMMARY_FILES.items()},
            parameters={
                "decision_policy": "no_more_same_family_shards_without_precommitted_new_feature_class",
                "profitability_policy": "positive_pockets_are_not_accepted_survivors_without_retail_cost_train_test_breadth_gates",
                "next_feature_priority": "passive_queue_capture_cost_floor",
            },
            outputs={
                "profitability_evidence_ledger": str(output_dir / "profitability_evidence_ledger.csv"),
                "retired_strategy_family_ledger": str(output_dir / "retired_strategy_family_ledger.csv"),
                "next_feature_class_gate": str(output_dir / "next_feature_class_gate.csv"),
                "acceptance_summary": str(output_dir / "strategy_pivot_acceptance_summary.csv"),
                "report": str(output_dir / "phase88_strategy_pivot_decision_ledger_report.md"),
                "manifest": str(output_dir / "phase88_strategy_pivot_decision_ledger_manifest.json"),
            },
            random_seed="none_deterministic_decision_ledger",
            scenario_ids="phase88_post_phase87_strategy_pivot",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_decision_gate",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase88_strategy_pivot_decision_ledger_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase88 strategy pivot decision ledger.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase88(args.base_dir, args.output_dir)


if __name__ == "__main__":
    main()
