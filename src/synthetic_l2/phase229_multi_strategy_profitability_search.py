from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_OUTPUT_DIR = Path("outputs/phase229")
DEFAULT_PHASE164_SUMMARY = Path("outputs/phase164/phase164_strategy_profile_summary.csv")
DEFAULT_PHASE164_LEDGER = Path("outputs/phase164/phase164_aggregate_trade_ledger.csv")
DEFAULT_PHASE52_SUMMARY = Path("outputs/phase52/dense_replay_strategy_summary_partial.csv")
DEFAULT_PHASE167_SUMMARY = Path("outputs/phase167/phase167_s08_strategy_profile_summary.csv")


REALISTIC_EXECUTION_PROFILES = {"retail_marketable_default", "stressed_retail"}
CONTROL_EXECUTION_PROFILES = {"zero_latency_spread_only_control"}


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def bool_sum(series: pd.Series) -> int:
    return int(series.fillna(False).astype(bool).sum())


def add_source(frame: pd.DataFrame, source_phase: str) -> pd.DataFrame:
    if frame.empty:
        return frame
    out = frame.copy()
    out.insert(0, "source_phase", source_phase)
    return out


def normalize_summary(frame: pd.DataFrame, source_phase: str) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame()
    out = add_source(frame, source_phase)
    if "source_strategy_id" not in out.columns:
        out["source_strategy_id"] = out["strategy_id"].astype(str)
    if "feature_family" not in out.columns:
        out["feature_family"] = out["strategy_id"].astype(str)
    if "feature_status" not in out.columns:
        out["feature_status"] = "legacy_dense_replay"
    if "annual_net_pnl_inr" not in out.columns and "net_pnl_inr" in out.columns:
        out["annual_net_pnl_inr"] = out["net_pnl_inr"]
    if "mean_net_return_per_trade" not in out.columns and "mean_net_return" in out.columns:
        out["mean_net_return_per_trade"] = out["mean_net_return"]
    if "mean_gross_return_per_trade" not in out.columns and "mean_gross_return" in out.columns:
        out["mean_gross_return_per_trade"] = out["mean_gross_return"]
    if "mean_cost_return_per_trade" not in out.columns and "mean_cost_return" in out.columns:
        out["mean_cost_return_per_trade"] = out["mean_cost_return"]
    for col in [
        "trades",
        "trade_dates",
        "annual_net_pnl_inr",
        "mean_net_return_per_trade",
        "mean_gross_return_per_trade",
        "mean_cost_return_per_trade",
        "worst_daily_net_pnl_inr",
        "max_drawdown_inr",
        "worst_trade_pnl_inr",
        "positive_day_fraction",
        "annualized_sharpe_proxy",
    ]:
        if col not in out.columns:
            out[col] = 0
        out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0)
    if "positive_after_costs" not in out.columns:
        out["positive_after_costs"] = out["annual_net_pnl_inr"] > 0
    if "risk_proxy_pass" not in out.columns:
        out["risk_proxy_pass"] = False
    if "synthetic_replay_candidate" not in out.columns:
        dense_col = "dense_replay_candidate"
        out["synthetic_replay_candidate"] = out[dense_col] if dense_col in out.columns else (
            out["positive_after_costs"].astype(bool) & out["risk_proxy_pass"].astype(bool)
        )
    return out


def build_universe(summaries: list[pd.DataFrame]) -> pd.DataFrame:
    normalized = [frame for frame in summaries if not frame.empty]
    if not normalized:
        return pd.DataFrame()
    cols = [
        "source_phase",
        "strategy_id",
        "source_strategy_id",
        "feature_family",
        "feature_status",
        "execution_profile",
        "trade_dates",
        "trades",
        "annual_net_pnl_inr",
        "mean_net_return_per_trade",
        "mean_gross_return_per_trade",
        "mean_cost_return_per_trade",
        "worst_daily_net_pnl_inr",
        "max_drawdown_inr",
        "worst_trade_pnl_inr",
        "positive_day_fraction",
        "annualized_sharpe_proxy",
        "positive_after_costs",
        "risk_proxy_pass",
        "synthetic_replay_candidate",
    ]
    universe = pd.concat(normalized, ignore_index=True, sort=False)
    for col in cols:
        if col not in universe.columns:
            universe[col] = ""
    universe["is_realistic_profile"] = universe["execution_profile"].astype(str).isin(REALISTIC_EXECUTION_PROFILES)
    universe["is_control_profile"] = universe["execution_profile"].astype(str).isin(CONTROL_EXECUTION_PROFILES)
    universe["cost_drag_ratio_to_abs_gross"] = (
        universe["mean_cost_return_per_trade"].abs()
        / universe["mean_gross_return_per_trade"].abs().where(universe["mean_gross_return_per_trade"].abs() > 0, pd.NA)
    )
    return universe[cols + ["is_realistic_profile", "is_control_profile", "cost_drag_ratio_to_abs_gross"]]


def build_candidate_ranking(universe: pd.DataFrame) -> pd.DataFrame:
    if universe.empty:
        return pd.DataFrame()
    ranking = universe.copy()
    ranking["candidate_class"] = "rejected_negative_after_cost"
    ranking.loc[
        ranking["annual_net_pnl_inr"].gt(0) & ranking["is_realistic_profile"],
        "candidate_class",
    ] = "synthetic_profitable_realistic_profile_candidate"
    ranking.loc[
        ranking["annual_net_pnl_inr"].gt(0) & ranking["is_control_profile"],
        "candidate_class",
    ] = "diagnostic_control_profitable_only_not_tradable"
    ranking["next_diagnostic"] = "increase_edge_or_reduce_turnover_before_replay"
    ranking.loc[
        ranking["mean_gross_return_per_trade"].abs().le(ranking["mean_cost_return_per_trade"].abs()),
        "next_diagnostic",
    ] = "gross_edge_smaller_than_cost_drag"
    ranking.loc[
        ranking["trades"].gt(100000),
        "next_diagnostic",
    ] = "turnover_too_high_costs_dominate"
    ranking.loc[
        ranking["annual_net_pnl_inr"].gt(0) & ranking["is_realistic_profile"],
        "next_diagnostic",
    ] = "validate_candidate_on_sealed_synthetic_holdout_before_any_claim"
    return ranking.sort_values(
        ["annual_net_pnl_inr", "mean_net_return_per_trade", "positive_day_fraction"],
        ascending=[False, False, False],
        kind="mergesort",
    )


def build_family_summary(universe: pd.DataFrame) -> pd.DataFrame:
    if universe.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for (source_phase, source_strategy_id, feature_family), group in universe.groupby(
        ["source_phase", "source_strategy_id", "feature_family"], sort=True
    ):
        realistic = group[group["is_realistic_profile"]]
        controls = group[group["is_control_profile"]]
        best = group.sort_values("annual_net_pnl_inr", ascending=False, kind="mergesort").head(1)
        best_realistic = realistic.sort_values("annual_net_pnl_inr", ascending=False, kind="mergesort").head(1)
        rows.append(
            {
                "source_phase": source_phase,
                "source_strategy_id": source_strategy_id,
                "feature_family": feature_family,
                "profiles_evaluated": int(len(group)),
                "realistic_profiles_evaluated": int(len(realistic)),
                "control_profiles_evaluated": int(len(controls)),
                "total_trades": int(group["trades"].sum()),
                "positive_after_cost_profiles": bool_sum(group["positive_after_costs"]),
                "synthetic_candidate_profiles": bool_sum(group["synthetic_replay_candidate"]),
                "best_strategy_id": best["strategy_id"].iloc[0] if not best.empty else "none",
                "best_execution_profile": best["execution_profile"].iloc[0] if not best.empty else "none",
                "best_annual_net_pnl_inr": float(best["annual_net_pnl_inr"].iloc[0]) if not best.empty else 0.0,
                "best_realistic_execution_profile": best_realistic["execution_profile"].iloc[0] if not best_realistic.empty else "none",
                "best_realistic_annual_net_pnl_inr": float(best_realistic["annual_net_pnl_inr"].iloc[0]) if not best_realistic.empty else 0.0,
            }
        )
    return pd.DataFrame(rows).sort_values("best_realistic_annual_net_pnl_inr", ascending=False, kind="mergesort")


def build_gate_evaluation(universe: pd.DataFrame, ranking: pd.DataFrame) -> pd.DataFrame:
    strategy_count = int(universe["strategy_id"].nunique()) if not universe.empty else 0
    realistic_rows = int(universe["is_realistic_profile"].sum()) if not universe.empty else 0
    positive_realistic = int(
        (
            ranking["annual_net_pnl_inr"].gt(0)
            & ranking["is_realistic_profile"].astype(bool)
        ).sum()
    ) if not ranking.empty else 0
    positive_any = int(ranking["annual_net_pnl_inr"].gt(0).sum()) if not ranking.empty else 0
    return pd.DataFrame(
        [
            {
                "gate_id": "P229_INPUT_UNIVERSE_AVAILABLE",
                "passed": len(universe) > 0,
                "observed_value": int(len(universe)),
                "required_value": ">0 strategy/profile rows",
                "interpretation": "Existing synthetic replay summaries are available for strategy discovery.",
            },
            {
                "gate_id": "P229_SEVERAL_STRATEGIES_EVALUATED",
                "passed": strategy_count >= 3,
                "observed_value": strategy_count,
                "required_value": ">=3 distinct strategy ids",
                "interpretation": "The phase tests several existing strategy forms instead of a single shard loop.",
            },
            {
                "gate_id": "P229_REALISTIC_COST_PROFILES_EVALUATED",
                "passed": realistic_rows > 0,
                "observed_value": realistic_rows,
                "required_value": ">0 retail/stressed profile rows",
                "interpretation": "Ranking includes costed realistic retail execution profiles.",
            },
            {
                "gate_id": "P229_SYNTHETIC_PROFITABLE_REALISTIC_CANDIDATE_FOUND",
                "passed": positive_realistic > 0,
                "observed_value": positive_realistic,
                "required_value": ">0 positive realistic net-after-cost rows",
                "interpretation": "If this fails, no tested strategy is currently profitable after realistic modeled costs.",
            },
            {
                "gate_id": "P229_SYNTHETIC_PROFITABLE_ANY_PROFILE_FOUND",
                "passed": positive_any > 0,
                "observed_value": positive_any,
                "required_value": ">0 positive net-after-cost rows",
                "interpretation": "Diagnostic control profitability is tracked separately from realistic tradability.",
            },
        ]
    )


def metric_frame(metrics: list[tuple[str, Any, str]]) -> pd.DataFrame:
    return pd.DataFrame(metrics, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase229 Multi-strategy Profitability Search",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase229 pivots from additional guardrail-only work into a concrete strategy-discovery screen.",
        "It ranks already executed synthetic tick/depth strategy replays net of modeled Zerodha-style costs.",
        "A positive row here means synthetic-candidate evidence only; it is not paper/live readiness or a deployable profitability claim.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase229_multi_strategy_profitability_search_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase229(
    phase164_summary_path: Path,
    phase52_summary_path: Path,
    phase167_summary_path: Path,
    phase164_ledger_path: Path,
    output_dir: Path,
    base_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase164 = normalize_summary(read_csv(phase164_summary_path), "phase164_full_year_synthetic")
    phase52 = normalize_summary(read_csv(phase52_summary_path), "phase52_dense_partial")
    phase167 = normalize_summary(read_csv(phase167_summary_path), "phase167_cross_symbol_s08")
    universe = build_universe([phase164, phase52, phase167])
    ranking = build_candidate_ranking(universe)
    family_summary = build_family_summary(universe)
    gates = build_gate_evaluation(universe, ranking)

    ledger = read_csv(phase164_ledger_path)
    ledger_rows = int(len(ledger))
    ledger_trade_dates = int(ledger["trade_date"].nunique()) if not ledger.empty and "trade_date" in ledger.columns else 0
    ledger_symbols = int(ledger["symbol"].nunique()) if not ledger.empty and "symbol" in ledger.columns else 0
    best = ranking.head(1)
    positive_realistic = int(
        (
            ranking["annual_net_pnl_inr"].gt(0)
            & ranking["is_realistic_profile"].astype(bool)
        ).sum()
    ) if not ranking.empty else 0
    next_action = (
        "run_phase230_validate_profitable_synthetic_candidates_no_paper_live"
        if positive_realistic > 0
        else "run_phase230_expand_low_turnover_high_edge_strategy_search_no_generator_profit_tuning"
    )
    acceptance = metric_frame(
        [
            ("phase229_multi_strategy_profitability_search_complete", 1, "Strategy discovery ranking completed"),
            ("phase229_source_summary_rows", int(len(universe)), "Strategy/profile summary rows ranked"),
            ("phase229_distinct_strategy_ids", int(universe["strategy_id"].nunique()) if not universe.empty else 0, "Distinct strategy ids evaluated"),
            ("phase229_realistic_profile_rows", int(universe["is_realistic_profile"].sum()) if not universe.empty else 0, "Retail/stressed profile rows evaluated"),
            ("phase229_control_profile_rows", int(universe["is_control_profile"].sum()) if not universe.empty else 0, "Zero-latency control profile rows evaluated"),
            ("phase229_phase164_trade_ledger_rows", ledger_rows, "Phase164 daily/symbol/profile ledger rows referenced"),
            ("phase229_phase164_trade_dates", ledger_trade_dates, "Phase164 trade dates referenced"),
            ("phase229_phase164_symbols", ledger_symbols, "Phase164 symbols referenced"),
            ("phase229_positive_realistic_candidate_rows", positive_realistic, "Positive net-after-cost realistic profile rows"),
            ("phase229_positive_any_profile_rows", int(ranking["annual_net_pnl_inr"].gt(0).sum()) if not ranking.empty else 0, "Positive net-after-cost rows across all profiles"),
            ("phase229_best_strategy_id", best["strategy_id"].iloc[0] if not best.empty else "none", "Best strategy/profile by annual net P&L"),
            ("phase229_best_execution_profile", best["execution_profile"].iloc[0] if not best.empty else "none", "Best execution profile by annual net P&L"),
            ("phase229_best_annual_net_pnl_inr", float(best["annual_net_pnl_inr"].iloc[0]) if not best.empty else 0.0, "Best annual net P&L in ranked universe"),
            ("phase229_strategy_promotion_allowed", 0, "No promotion from synthetic search alone"),
            ("phase229_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from synthetic search alone"),
            ("phase229_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from synthetic search alone"),
            ("phase229_next_best_action", next_action, "Next strategy-discovery milestone"),
        ]
    )

    universe.to_csv(output_dir / "phase229_strategy_universe_summary.csv", index=False)
    ranking.to_csv(output_dir / "phase229_profitable_candidate_ranking.csv", index=False)
    family_summary.to_csv(output_dir / "phase229_family_profitability_summary.csv", index=False)
    gates.to_csv(output_dir / "phase229_strategy_search_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase229_strategy_search_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Top Ranked Strategy/Profile Rows": ranking.head(12),
            "Family Summary": family_summary,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase229_multi_strategy_profitability_search",
        **reproducibility_fields(
            artifact_id="phase229",
            generated_utc=generated_utc,
            inputs={
                "phase164_strategy_profile_summary": str(phase164_summary_path),
                "phase52_dense_replay_strategy_summary_partial": str(phase52_summary_path),
                "phase167_s08_strategy_profile_summary": str(phase167_summary_path),
                "phase164_aggregate_trade_ledger": str(phase164_ledger_path),
            },
            parameters={
                "realistic_execution_profiles": sorted(REALISTIC_EXECUTION_PROFILES),
                "control_execution_profiles": sorted(CONTROL_EXECUTION_PROFILES),
                "profitability_metric": "annual_net_pnl_inr_after_modeled_costs",
                "strategy_promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "strategy_universe_summary": str(output_dir / "phase229_strategy_universe_summary.csv"),
                "profitable_candidate_ranking": str(output_dir / "phase229_profitable_candidate_ranking.csv"),
                "family_profitability_summary": str(output_dir / "phase229_family_profitability_summary.csv"),
                "gate_evaluation": str(output_dir / "phase229_strategy_search_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase229_strategy_search_acceptance_summary.csv"),
                "report": str(output_dir / "phase229_multi_strategy_profitability_search_report.md"),
                "manifest": str(output_dir / "phase229_multi_strategy_profitability_search_manifest.json"),
            },
            random_seed="none_deterministic_existing_replay_ranking",
            scenario_ids="phase164_full_year_phase52_dense_partial_phase167_s08",
            cost_model_version="zerodha_equity_intraday_nse_order_formula_v2_2026_07_14",
            latency_model_version="existing_replay_execution_profiles_reused",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase229_multi_strategy_profitability_search_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rank existing synthetic strategy replays for net-after-cost profitability.")
    parser.add_argument("--phase164-summary", type=Path, default=DEFAULT_PHASE164_SUMMARY)
    parser.add_argument("--phase164-ledger", type=Path, default=DEFAULT_PHASE164_LEDGER)
    parser.add_argument("--phase52-summary", type=Path, default=DEFAULT_PHASE52_SUMMARY)
    parser.add_argument("--phase167-summary", type=Path, default=DEFAULT_PHASE167_SUMMARY)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase229(
        phase164_summary_path=args.phase164_summary,
        phase52_summary_path=args.phase52_summary,
        phase167_summary_path=args.phase167_summary,
        phase164_ledger_path=args.phase164_ledger,
        output_dir=args.output_dir,
        base_dir=args.base_dir,
    )


if __name__ == "__main__":
    main()
