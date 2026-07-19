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


DEFAULT_OUTPUT_DIR = Path("outputs/phase116")


INPUTS = {
    "phase52_dense_acceptance": Path("outputs/phase52/dense_replay_acceptance_summary_partial.csv"),
    "phase52_dense_strategy": Path("outputs/phase52/dense_replay_strategy_summary_partial.csv"),
    "phase82_hdfcbank_smoke": Path("outputs/phase82_smoke/stratified_hdfcbank_acceptance_summary.csv"),
    "phase84_hdfcbank_full": Path("outputs/phase84/cached_stratified_hdfcbank_acceptance_summary.csv"),
    "phase91_cross_symbol_acceptance": Path("outputs/phase91/cross_symbol_replay_acceptance_summary.csv"),
    "phase91_cross_symbol_candidates": Path("outputs/phase91/cross_symbol_candidate_results.csv"),
    "phase93_event_window_acceptance": Path("outputs/phase93/event_window_replay_acceptance_summary.csv"),
    "phase93_event_window_candidates": Path("outputs/phase93/event_window_candidate_results.csv"),
    "phase115_real_panel_refresh": Path("outputs/phase115/phase115_real_panel_refresh_acceptance_summary.csv"),
}


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
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


def bool_count(frame: pd.DataFrame, column: str) -> int:
    if frame.empty or column not in frame.columns:
        return 0
    return int(frame[column].astype(str).str.lower().isin(["true", "1", "yes"]).sum())


def positive_count(frame: pd.DataFrame, column: str) -> int:
    if frame.empty or column not in frame.columns:
        return 0
    return int((pd.to_numeric(frame[column], errors="coerce").fillna(0.0) > 0.0).sum())


def min_float(frame: pd.DataFrame, column: str) -> float | None:
    if frame.empty or column not in frame.columns:
        return None
    series = pd.to_numeric(frame[column], errors="coerce").dropna()
    if series.empty:
        return None
    return float(series.min())


def max_float(frame: pd.DataFrame, column: str) -> float | None:
    if frame.empty or column not in frame.columns:
        return None
    series = pd.to_numeric(frame[column], errors="coerce").dropna()
    if series.empty:
        return None
    return float(series.max())


def build_dense_strategy_verdict(strategy: pd.DataFrame) -> pd.DataFrame:
    if strategy.empty:
        return pd.DataFrame(
            columns=[
                "strategy_id",
                "execution_profile",
                "trade_dates",
                "trades",
                "annual_net_pnl_inr",
                "mean_net_return_per_trade",
                "after_cost_profitable",
                "decision",
            ]
        )
    frame = strategy.copy()
    frame["annual_net_pnl_inr"] = pd.to_numeric(frame.get("annual_net_pnl_inr"), errors="coerce")
    frame["mean_net_return_per_trade"] = pd.to_numeric(frame.get("mean_net_return_per_trade"), errors="coerce")
    frame["after_cost_profitable"] = frame["annual_net_pnl_inr"].fillna(0.0) > 0.0
    frame["decision"] = frame["after_cost_profitable"].map({True: "positive_but_requires_gate_review", False: "retired_negative_after_costs"})
    columns = [
        "strategy_id",
        "execution_profile",
        "trade_dates",
        "trades",
        "annual_net_pnl_inr",
        "mean_net_return_per_trade",
        "after_cost_profitable",
        "decision",
    ]
    return frame[[column for column in columns if column in frame.columns]].sort_values(
        ["after_cost_profitable", "annual_net_pnl_inr"], ascending=[False, False]
    )


def build_profitability_verdict(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    p52_accept = tables["phase52_dense_acceptance"]
    p52_strategy = tables["phase52_dense_strategy"]
    p82 = tables["phase82_hdfcbank_smoke"]
    p84 = tables["phase84_hdfcbank_full"]
    p91_accept = tables["phase91_cross_symbol_acceptance"]
    p91 = tables["phase91_cross_symbol_candidates"]
    p93_accept = tables["phase93_event_window_acceptance"]
    p93 = tables["phase93_event_window_candidates"]
    p115 = tables["phase115_real_panel_refresh"]

    rows = [
        {
            "evidence_id": "P52_DENSE_TICK_FULL_YEAR_PARTIAL_REPLAY",
            "scope": "dense L1/microprice/one-tick-momentum replay across scanned full-year shards",
            "trades_or_rows": as_int(metric_value(p52_accept, "phase52_dense_replay_trade_rows")),
            "positive_after_cost_rows": as_int(metric_value(p52_accept, "phase52_positive_after_cost_rows")),
            "accepted_strategy_rows": as_int(metric_value(p52_accept, "phase52_dense_replay_candidate_rows")),
            "best_net_pnl_inr": max_float(p52_strategy, "annual_net_pnl_inr"),
            "worst_net_pnl_inr": min_float(p52_strategy, "annual_net_pnl_inr"),
            "positive_pockets_observed": False,
            "verdict": "falsified_for_same_family_continuation",
            "next_action": "do_not_continue_dense_taker_shards_without_new_edge_hypothesis",
        },
        {
            "evidence_id": "P82_HDFCBANK_STRATIFIED_SMOKE",
            "scope": "HDFCBANK lead-lag stratified smoke retest",
            "trades_or_rows": as_int(metric_value(p82, "phase82_total_trades")),
            "positive_after_cost_rows": as_int(metric_value(p82, "phase82_positive_months")),
            "accepted_strategy_rows": as_int(metric_value(p82, "phase82_stratified_hdfcbank_retest_pass")),
            "best_net_pnl_inr": as_float(metric_value(p82, "phase82_total_net_pnl_inr")),
            "worst_net_pnl_inr": as_float(metric_value(p82, "phase82_total_net_pnl_inr")),
            "positive_pockets_observed": False,
            "verdict": "falsified",
            "next_action": str(metric_value(p82, "phase82_recommend_next_action", "retire_hdfcbank_lead_lag")),
        },
        {
            "evidence_id": "P84_HDFCBANK_CACHED_STRATIFIED_FULL_YEAR",
            "scope": "HDFCBANK cached stratified full-year retest",
            "trades_or_rows": as_int(metric_value(p84, "phase84_total_trades")),
            "positive_after_cost_rows": as_int(metric_value(p84, "phase84_positive_months")),
            "accepted_strategy_rows": as_int(metric_value(p84, "phase84_cached_stratified_hdfcbank_pass")),
            "best_net_pnl_inr": as_float(metric_value(p84, "phase84_total_net_pnl_inr")),
            "worst_net_pnl_inr": as_float(metric_value(p84, "phase84_total_net_pnl_inr")),
            "positive_pockets_observed": as_int(metric_value(p84, "phase84_positive_months")) > 0,
            "verdict": "falsified_despite_positive_month_pockets",
            "next_action": str(metric_value(p84, "phase84_recommend_next_action", "retire_hdfcbank_lead_lag")),
        },
        {
            "evidence_id": "P91_CROSS_SYMBOL_REGIME_IMBALANCE",
            "scope": "cross-symbol market/sector/symbol-vs-sector imbalance candidates",
            "trades_or_rows": int(pd.to_numeric(p91.get("test_trades", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()) if not p91.empty else 0,
            "positive_after_cost_rows": positive_count(p91, "test_net_pnl_inr"),
            "accepted_strategy_rows": bool_count(p91, "phase91_candidate_pass"),
            "best_net_pnl_inr": max_float(p91, "test_net_pnl_inr"),
            "worst_net_pnl_inr": min_float(p91, "test_net_pnl_inr"),
            "positive_pockets_observed": positive_count(p91, "test_net_pnl_inr") > 0,
            "verdict": "no_accepted_survivor",
            "next_action": str(metric_value(p91_accept, "phase91_recommend_next_action", "do_not_scale_cross_symbol_candidates")),
        },
        {
            "evidence_id": "P93_LOW_TURNOVER_EVENT_WINDOW",
            "scope": "low-turnover shock continuation/reversal event-window candidates",
            "trades_or_rows": int(pd.to_numeric(p93.get("test_trades", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()) if not p93.empty else 0,
            "positive_after_cost_rows": positive_count(p93, "test_net_pnl_inr"),
            "accepted_strategy_rows": bool_count(p93, "phase93_candidate_pass"),
            "best_net_pnl_inr": max_float(p93, "test_net_pnl_inr"),
            "worst_net_pnl_inr": min_float(p93, "test_net_pnl_inr"),
            "positive_pockets_observed": positive_count(p93, "test_net_pnl_inr") > 0,
            "verdict": "no_accepted_survivor",
            "next_action": str(metric_value(p93_accept, "phase93_recommend_next_action", "do_not_scale_event_window_candidates")),
        },
        {
            "evidence_id": "P115_REAL_PANEL_REFRESH_GATE",
            "scope": "real-anchor refresh and replay unlock gate",
            "trades_or_rows": as_int(metric_value(p115, "phase115_steps")),
            "positive_after_cost_rows": 0,
            "accepted_strategy_rows": as_int(metric_value(p115, "phase115_strategy_replay_allowed")),
            "best_net_pnl_inr": None,
            "worst_net_pnl_inr": None,
            "positive_pockets_observed": False,
            "verdict": "real_strategy_replay_locked",
            "next_action": str(metric_value(p115, "phase115_recommend_next_action", "collect_or_import_more_real_l2_days")),
        },
    ]
    return pd.DataFrame(rows)


def build_replay_blocklist() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "blocked_family_id": "DENSE_L1_IMBALANCE_MARKETABLE",
                "blocked_strategy_ids": "DENSE_S01_L1_IMBALANCE",
                "block_reason": "Phase52 dense replay found negative annual net P&L in every execution profile.",
                "same_shard_continuation_allowed": False,
                "unlock_condition": "new precommitted non-taker or materially different feature class plus train/test/month gates",
            },
            {
                "blocked_family_id": "DENSE_MICROPRICE_MARKETABLE",
                "blocked_strategy_ids": "DENSE_S02_MICROPRICE",
                "block_reason": "Phase52 dense replay found negative annual net P&L in every execution profile.",
                "same_shard_continuation_allowed": False,
                "unlock_condition": "new precommitted non-taker or materially different feature class plus train/test/month gates",
            },
            {
                "blocked_family_id": "DENSE_ONE_TICK_MOMENTUM_MARKETABLE",
                "blocked_strategy_ids": "DENSE_S03_1T_MOMENTUM",
                "block_reason": "Phase52 dense replay found negative annual net P&L in every execution profile.",
                "same_shard_continuation_allowed": False,
                "unlock_condition": "new precommitted non-taker or materially different feature class plus train/test/month gates",
            },
            {
                "blocked_family_id": "HDFCBANK_LEAD_LAG",
                "blocked_strategy_ids": "phase77_phase82_phase84_hdfcbank_rechecks",
                "block_reason": "Disjoint and cached stratified HDFCBANK retests produced zero pass months/zero accepted survivor.",
                "same_shard_continuation_allowed": False,
                "unlock_condition": "only a newly specified cross-symbol feature may include HDFCBANK; do not rerun the retired rule",
            },
            {
                "blocked_family_id": "CROSS_SYMBOL_IMBALANCE_CURRENT_RULES",
                "blocked_strategy_ids": "P90_MARKET_IMBALANCE_CONTINUATION;P90_SECTOR_IMBALANCE_CONTINUATION;P90_SYMBOL_SECTOR_DIVERGENCE_REVERSION",
                "block_reason": "Phase91 found positive pockets but zero candidate pass rows.",
                "same_shard_continuation_allowed": False,
                "unlock_condition": "redesign features and precommit new gates before replay",
            },
            {
                "blocked_family_id": "LOW_TURNOVER_EVENT_WINDOW_CURRENT_RULES",
                "blocked_strategy_ids": "P92_SHOCK_CONTINUATION;P92_BOOK_DISLOCATION_REVERSAL;P92_SHOCK_EXHAUSTION_REVERSAL",
                "block_reason": "Phase93 found positive pockets but zero candidate pass rows.",
                "same_shard_continuation_allowed": False,
                "unlock_condition": "new event-window hypothesis with stronger gross edge over retail costs",
            },
        ]
    )


def build_next_best_action_gate(verdict: pd.DataFrame, p115: pd.DataFrame) -> pd.DataFrame:
    accepted = int(verdict["accepted_strategy_rows"].fillna(0).astype(float).sum())
    replay_allowed = as_int(metric_value(p115, "phase115_strategy_replay_allowed"))
    ready_days = as_int(metric_value(p115, "phase115_phase110_ready_real_anchor_days"))
    days_needed = as_int(metric_value(p115, "phase115_phase110_days_needed_for_min"))
    if replay_allowed:
        next_action = "precommit_new_feature_class_then_run_bounded_replay"
        compute_policy = "bounded_only"
    else:
        next_action = "collect_or_import_more_real_l2_days_then_run_phase115_with_execute_import"
        compute_policy = "no_more_large_dense_strategy_shards"
    return pd.DataFrame(
        [
            {
                "gate_id": "P116_NO_ACCEPTED_PROFITABILITY",
                "gate_status": "closed" if accepted == 0 else "review_required",
                "evidence": f"accepted_strategy_rows={accepted}",
                "policy": "synthetic positive pockets are not profitability proof",
            },
            {
                "gate_id": "P116_REAL_REPLAY_UNLOCK",
                "gate_status": "open" if replay_allowed else "closed",
                "evidence": f"ready_real_anchor_days={ready_days}; days_needed_for_min={days_needed}",
                "policy": "real-anchor replay stays closed until Phase115/Phase110 unlocks it",
            },
            {
                "gate_id": "P116_COMPUTE_BUDGET",
                "gate_status": compute_policy,
                "evidence": "Phase52 scanned 797M+ dense simulated trades with zero positive-after-cost rows",
                "policy": "large shard continuation requires a materially new precommitted edge hypothesis",
            },
            {
                "gate_id": "P116_NEXT_BEST_ACTION",
                "gate_status": next_action,
                "evidence": "latest evidence favors real-anchor expansion and hypothesis redesign over brute-force shard replay",
                "policy": "spend next milestone on data unlock or new-feature precommit, not repeated failed-family replay",
            },
        ]
    )


def build_acceptance_summary(
    verdict: pd.DataFrame,
    strategy_verdict: pd.DataFrame,
    blocklist: pd.DataFrame,
    next_gate: pd.DataFrame,
) -> pd.DataFrame:
    accepted_rows = int(verdict["accepted_strategy_rows"].fillna(0).astype(float).sum())
    positive_pocket_rows = int(verdict["positive_pockets_observed"].astype(bool).sum())
    dense_positive_rows = int(strategy_verdict["after_cost_profitable"].astype(bool).sum()) if not strategy_verdict.empty else 0
    same_shard_allowed = int(blocklist["same_shard_continuation_allowed"].astype(bool).any())
    next_action = str(next_gate.loc[next_gate["gate_id"].eq("P116_NEXT_BEST_ACTION"), "gate_status"].iloc[0])
    return pd.DataFrame(
        [
            ("phase116_profitability_evidence_rows", int(len(verdict)), "Latest profitability and replay-lock evidence rows reviewed"),
            ("phase116_dense_strategy_profile_rows", int(len(strategy_verdict)), "Dense strategy/profile rows reviewed from Phase52"),
            ("phase116_dense_positive_after_cost_rows", dense_positive_rows, "Dense strategy/profile rows positive after costs"),
            ("phase116_positive_pocket_evidence_rows", positive_pocket_rows, "Evidence rows with isolated positive pockets"),
            ("phase116_accepted_strategy_rows", accepted_rows, "Accepted profitable strategy rows across reviewed evidence"),
            ("phase116_blocklisted_family_rows", int(len(blocklist)), "Strategy families blocked from same-shard continuation"),
            ("phase116_same_family_shard_continuation_allowed", same_shard_allowed, "1 means more same-family shard replay is allowed"),
            ("phase116_strategy_replay_gate", "closed" if accepted_rows == 0 else "review_required", "Profitability gate for current strategy families"),
            ("phase116_next_best_action", next_action, "Recommended next milestone"),
            ("phase116_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha equity intraday NSE cost model version"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase116 Profitability Verdict and Research Gate",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase116 updates the stop/continue decision using the latest dense replay, candidate replay and real-anchor gate evidence.",
        "The current verdict is intentionally blunt: no strategy family has an accepted profitable survivor, so more same-family dense shards are blocked.",
        "The next useful work is either importing/collecting enough real L2 days to unlock real-anchor replay or precommitting a genuinely new edge hypothesis before any bounded synthetic replay.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase116_profitability_verdict_and_research_gate_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def run_phase116(base_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    tables = {name: read_csv(base_dir / path) for name, path in INPUTS.items()}
    dense_strategy = build_dense_strategy_verdict(tables["phase52_dense_strategy"])
    verdict = build_profitability_verdict(tables)
    blocklist = build_replay_blocklist()
    next_gate = build_next_best_action_gate(verdict, tables["phase115_real_panel_refresh"])
    acceptance = build_acceptance_summary(verdict, dense_strategy, blocklist, next_gate)

    dense_strategy.to_csv(output_dir / "dense_strategy_profile_verdict.csv", index=False)
    verdict.to_csv(output_dir / "profitability_verdict_ledger.csv", index=False)
    blocklist.to_csv(output_dir / "strategy_replay_blocklist.csv", index=False)
    next_gate.to_csv(output_dir / "next_best_action_gate.csv", index=False)
    acceptance.to_csv(output_dir / "phase116_profitability_verdict_acceptance_summary.csv", index=False)

    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Dense Strategy Profile Verdict": dense_strategy,
            "Profitability Verdict Ledger": verdict,
            "Strategy Replay Blocklist": blocklist,
            "Next Best Action Gate": next_gate,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase116_profitability_verdict_and_research_gate",
        "accepted_strategy_rows": int(
            acceptance.loc[acceptance["metric"].eq("phase116_accepted_strategy_rows"), "value"].iloc[0]
        ),
        "same_family_shard_continuation_allowed": int(
            acceptance.loc[
                acceptance["metric"].eq("phase116_same_family_shard_continuation_allowed"), "value"
            ].iloc[0]
        ),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase116",
            generated_utc=generated_utc,
            inputs={name: str(path) for name, path in INPUTS.items()},
            parameters={
                "profitability_policy": "accepted_profitable_strategy_requires_after_cost_survival_plus_replay_gate_pass",
                "compute_policy": "block_more_same_family_dense_shards_after_phase52_zero_positive_after_cost_rows",
                "real_anchor_policy": "strategy_replay_remains_closed_until_phase115_or_phase110_unlocks_multiday_panel",
            },
            outputs={
                "dense_strategy_profile_verdict": str(output_dir / "dense_strategy_profile_verdict.csv"),
                "profitability_verdict_ledger": str(output_dir / "profitability_verdict_ledger.csv"),
                "strategy_replay_blocklist": str(output_dir / "strategy_replay_blocklist.csv"),
                "next_best_action_gate": str(output_dir / "next_best_action_gate.csv"),
                "acceptance_summary": str(output_dir / "phase116_profitability_verdict_acceptance_summary.csv"),
                "report": str(output_dir / "phase116_profitability_verdict_and_research_gate_report.md"),
                "manifest": str(output_dir / "phase116_profitability_verdict_and_research_gate_manifest.json"),
            },
            random_seed="none_deterministic_decision_gate",
            scenario_ids="phase116_latest_profitability_and_replay_lock_verdict",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_decision_gate",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase116_profitability_verdict_and_research_gate_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase116 profitability verdict and next research gate.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase116(args.base_dir, args.output_dir)


if __name__ == "__main__":
    main()
