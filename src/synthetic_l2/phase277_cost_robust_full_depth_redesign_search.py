from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase271_fixed_capital_concurrency_and_capacity_return_analysis import schedule_events_for_scenario
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE275_DIR = Path("outputs/phase275")
DEFAULT_PHASE276_DIR = Path("outputs/phase276")
DEFAULT_OUTPUT_DIR = Path("outputs/phase277")

SELECTED_ROUTE = "P277_COST_ROBUST_FULL_DEPTH_REDESIGN_SEARCH"
NEXT_ACTION = "run_phase278_cost_robust_redesign_interpretation_no_paper_live"
REPAIR_ACTION = "repair_phase277_cost_robust_full_depth_redesign_search"

ANNUALIZED_THRESHOLD_PCT = 12.0
INITIAL_CAPITAL_GRID_INR = [100_000.0]
FIXED_NOTIONAL_GRID_INR = [50_000.0, 75_000.0, 100_000.0]
MAX_CONCURRENT_GRID = [1, 2]
QUANTILES = [0.50, 0.60, 0.70, 0.80, 0.90]
TARGET_COST_PROFILE = "cost200"

FULL_DEPTH_COLUMNS = [
    "avg_cum_top5_qty_imbalance",
    "avg_depth_beyond_l1_qty_imbalance",
    "avg_level_weighted_depth_imbalance",
    "depth_replenishment_pressure",
    "depth_withdrawal_pressure",
    "top5_churn_pressure",
    "avg_spread_bps",
]


def parse_contract_value(route: pd.DataFrame, contract_id: str) -> str:
    if route.empty:
        return ""
    rows = route.loc[route["contract_id"].astype(str).eq(contract_id), "contract_value"]
    return "" if rows.empty else str(rows.iloc[0])


def prepare_event_universe(ledger: pd.DataFrame, anchor_profiles: list[str]) -> pd.DataFrame:
    if ledger.empty:
        raise FileNotFoundError("Phase275 sample scheduled-event ledger is empty.")
    frame = ledger.copy()
    frame = frame[frame["cost_profile"].astype(str).eq(TARGET_COST_PROFILE)].copy()
    if anchor_profiles:
        anchored = frame[frame["phase275_scope_profile_id"].astype(str).isin(anchor_profiles)].copy()
        if not anchored.empty:
            frame = anchored
    if frame.empty:
        raise ValueError("No cost200 rows available for Phase277 redesign search.")
    for col in FULL_DEPTH_COLUMNS + ["gross_edge_bps", "modeled_cost_bps", "cost_multiplier", "horizon", "richer_event_bar_id", "candidate_rank"]:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
    frame["zerodha_round_trip_charge_bps"] = frame["modeled_cost_bps"] / frame["cost_multiplier"].replace(0, 2.0)
    frame["depth_replenish_withdraw_ratio"] = frame["depth_replenishment_pressure"] / (frame["depth_withdrawal_pressure"] + 1.0)
    frame["depth_consensus_imbalance"] = (
        frame["avg_cum_top5_qty_imbalance"]
        + frame["avg_depth_beyond_l1_qty_imbalance"]
        + frame["avg_level_weighted_depth_imbalance"]
    ) / 3.0
    frame["event_sparsity_pressure"] = frame["avg_spread_bps"] * (frame["top5_churn_pressure"] + 1.0)
    keys = [
        "phase275_scope_profile_id",
        "synthetic_seed",
        "synthetic_regime",
        "trade_date",
        "exchange",
        "symbol",
        "richer_event_bar_id",
        "candidate_id",
    ]
    frame = frame.drop_duplicates([col for col in keys if col in frame.columns]).reset_index(drop=True)
    frame["richer_event_bar_id"] = pd.to_numeric(frame["richer_event_bar_id"], errors="coerce").fillna(0).astype(int)
    frame["horizon"] = pd.to_numeric(frame["horizon"], errors="coerce").fillna(1).astype(int).clip(lower=1)
    frame["candidate_rank"] = pd.to_numeric(frame["candidate_rank"], errors="coerce").fillna(999999).astype(int)
    return frame.sort_values(["trade_date", "exchange", "richer_event_bar_id", "candidate_rank", "candidate_id", "symbol"]).reset_index(drop=True)


def build_variant_masks(events: pd.DataFrame) -> list[dict[str, Any]]:
    variants: list[dict[str, Any]] = [
        {
            "variant_id": "P277_BASE_ALL_COST200_EVENTS",
            "family": "baseline",
            "feature_rule": "all cost200 anchor events",
            "uses_top5": 1,
            "uses_levels_2_to_5": 1,
            "mask": pd.Series(True, index=events.index),
        }
    ]

    def add_quantile_variants(feature: str, family: str, direction: str, label: str) -> None:
        values = pd.to_numeric(events[feature], errors="coerce").fillna(0.0)
        for q in QUANTILES:
            threshold = float(values.quantile(q if direction == "ge" else 1.0 - q))
            if direction == "ge":
                mask = values >= threshold
                comparator = ">="
            else:
                mask = values <= threshold
                comparator = "<="
            variants.append(
                {
                    "variant_id": f"P277_{label}_{direction.upper()}_Q{int(q * 100)}",
                    "family": family,
                    "feature_rule": f"{feature} {comparator} {threshold:.6f}",
                    "threshold_quantile": q,
                    "threshold_value": threshold,
                    "uses_top5": int(feature in {"avg_cum_top5_qty_imbalance", "top5_churn_pressure", "depth_consensus_imbalance", "event_sparsity_pressure"}),
                    "uses_levels_2_to_5": int(feature in {"avg_depth_beyond_l1_qty_imbalance", "avg_level_weighted_depth_imbalance", "depth_consensus_imbalance", "depth_replenish_withdraw_ratio"}),
                    "mask": mask,
                }
            )

    add_quantile_variants("avg_cum_top5_qty_imbalance", "top5_imbalance", "ge", "TOP5_IMBALANCE")
    add_quantile_variants("avg_depth_beyond_l1_qty_imbalance", "levels_2_to_5_depth", "ge", "BEYOND_L1_IMBALANCE")
    add_quantile_variants("avg_level_weighted_depth_imbalance", "levels_2_to_5_depth", "ge", "WEIGHTED_DEPTH")
    add_quantile_variants("depth_consensus_imbalance", "top5_and_levels_2_to_5_consensus", "ge", "DEPTH_CONSENSUS")
    add_quantile_variants("depth_replenish_withdraw_ratio", "depth_replenishment_withdrawal", "ge", "REPLENISH_WITHDRAW")
    add_quantile_variants("avg_spread_bps", "spread_regime", "le", "SPREAD")
    add_quantile_variants("top5_churn_pressure", "event_sparsity", "le", "CHURN")
    add_quantile_variants("event_sparsity_pressure", "spread_and_churn_sparsity", "le", "SPARSITY_PRESSURE")

    consensus = pd.to_numeric(events["depth_consensus_imbalance"], errors="coerce").fillna(0.0)
    spread = pd.to_numeric(events["avg_spread_bps"], errors="coerce").fillna(0.0)
    churn = pd.to_numeric(events["top5_churn_pressure"], errors="coerce").fillna(0.0)
    ratio = pd.to_numeric(events["depth_replenish_withdraw_ratio"], errors="coerce").fillna(0.0)
    for q in [0.60, 0.70, 0.80]:
        c_thr = float(consensus.quantile(q))
        s_thr = float(spread.quantile(1.0 - q))
        ch_thr = float(churn.quantile(1.0 - q))
        r_thr = float(ratio.quantile(q))
        variants.append(
            {
                "variant_id": f"P277_CONSENSUS_SPREAD_Q{int(q * 100)}",
                "family": "consensus_spread_filter",
                "feature_rule": f"depth_consensus_imbalance >= {c_thr:.6f} and avg_spread_bps <= {s_thr:.6f}",
                "threshold_quantile": q,
                "threshold_value": c_thr,
                "uses_top5": 1,
                "uses_levels_2_to_5": 1,
                "mask": (consensus >= c_thr) & (spread <= s_thr),
            }
        )
        variants.append(
            {
                "variant_id": f"P277_REPLENISH_CHURN_Q{int(q * 100)}",
                "family": "replenishment_churn_filter",
                "feature_rule": f"depth_replenish_withdraw_ratio >= {r_thr:.6f} and top5_churn_pressure <= {ch_thr:.6f}",
                "threshold_quantile": q,
                "threshold_value": r_thr,
                "uses_top5": 1,
                "uses_levels_2_to_5": 1,
                "mask": (ratio >= r_thr) & (churn <= ch_thr),
            }
        )
    return variants


def evaluate_variants(events: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    scenario_rows: list[dict[str, Any]] = []
    sample_ledgers: list[pd.DataFrame] = []
    variants = build_variant_masks(events)
    for variant in variants:
        selected = events[variant["mask"]].copy()
        if selected.empty:
            continue
        for initial_capital in INITIAL_CAPITAL_GRID_INR:
            for fixed_notional in FIXED_NOTIONAL_GRID_INR:
                for max_concurrent in MAX_CONCURRENT_GRID:
                    scenario, ledger = schedule_events_for_scenario(
                        events=selected,
                        scope_id=variant["variant_id"],
                        scope_candidate_id=";".join(sorted(selected["candidate_id"].astype(str).unique())),
                        initial_capital_inr=initial_capital,
                        fixed_notional_inr=fixed_notional,
                        max_concurrent_positions=max_concurrent,
                        cost_profile=TARGET_COST_PROFILE,
                        cost_multiplier=2.0,
                        extra_slippage_bps=0.0,
                    )
                    scenario.update(
                        {
                            "phase277_variant_id": variant["variant_id"],
                            "redesign_family": variant["family"],
                            "feature_rule": variant["feature_rule"],
                            "threshold_quantile": variant.get("threshold_quantile", ""),
                            "threshold_value": variant.get("threshold_value", ""),
                            "uses_top5": variant["uses_top5"],
                            "uses_levels_2_to_5": variant["uses_levels_2_to_5"],
                            "l1_only_variant": 0,
                            "selected_event_rows": int(len(selected)),
                            "cost200_above12_diagnostic": int(float(scenario["mechanical_one_date_annualized_portfolio_return_pct"]) > ANNUALIZED_THRESHOLD_PCT),
                            "portfolio_claim_allowed": 0,
                            "strategy_replay_allowed": 0,
                            "promotion_allowed": 0,
                            "paper_or_live_acceptance_allowed": 0,
                            "deployable_profitability_claim_allowed": 0,
                        }
                    )
                    scenario_rows.append(scenario)
                    if len(sample_ledgers) < 12 and variant["variant_id"] in {
                        "P277_BASE_ALL_COST200_EVENTS",
                        "P277_BEYOND_L1_IMBALANCE_GE_Q50",
                        "P277_CHURN_LE_Q50",
                        "P277_SPREAD_LE_Q80",
                    }:
                        ledger = ledger.copy()
                        ledger["phase277_variant_id"] = variant["variant_id"]
                        ledger["redesign_family"] = variant["family"]
                        ledger["feature_rule"] = variant["feature_rule"]
                        sample_ledgers.append(ledger)
    scenarios = pd.DataFrame(scenario_rows)
    ledger = pd.concat(sample_ledgers, ignore_index=True) if sample_ledgers else pd.DataFrame()
    return scenarios, ledger


def build_variant_summary(scenarios: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame()
    frame = scenarios.copy()
    for col in [
        "mechanical_one_date_annualized_portfolio_return_pct",
        "realized_net_pnl_inr",
        "cost200_above12_diagnostic",
        "scheduled_event_rows",
        "max_drawdown_inr",
    ]:
        frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
    grouped = (
        frame.groupby(["phase277_variant_id", "redesign_family", "feature_rule"], dropna=False)
        .agg(
            scenario_rows=("scenario_id", "nunique"),
            selected_event_rows=("selected_event_rows", "max"),
            cost200_above12_scenario_rows=("cost200_above12_diagnostic", "sum"),
            min_annualized_pct=("mechanical_one_date_annualized_portfolio_return_pct", "min"),
            median_annualized_pct=("mechanical_one_date_annualized_portfolio_return_pct", "median"),
            max_annualized_pct=("mechanical_one_date_annualized_portfolio_return_pct", "max"),
            max_net_pnl_inr=("realized_net_pnl_inr", "max"),
            min_net_pnl_inr=("realized_net_pnl_inr", "min"),
            max_scheduled_event_rows=("scheduled_event_rows", "max"),
            worst_drawdown_inr=("max_drawdown_inr", "min"),
            uses_top5=("uses_top5", "max"),
            uses_levels_2_to_5=("uses_levels_2_to_5", "max"),
            l1_only_variant=("l1_only_variant", "max"),
        )
        .reset_index()
    )
    grouped["above12_fraction"] = grouped["cost200_above12_scenario_rows"] / grouped["scenario_rows"]
    grouped["median_above12"] = (grouped["median_annualized_pct"] > ANNUALIZED_THRESHOLD_PCT).astype(int)
    grouped["worst_case_above12"] = (grouped["min_annualized_pct"] > ANNUALIZED_THRESHOLD_PCT).astype(int)
    return grouped.sort_values(
        ["median_above12", "cost200_above12_scenario_rows", "max_annualized_pct", "median_annualized_pct"],
        ascending=[False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_gate_evaluation(phase276_summary: pd.DataFrame, route: pd.DataFrame, events: pd.DataFrame, scenarios: pd.DataFrame, summary: pd.DataFrame) -> pd.DataFrame:
    phase276_complete = as_int(metric_value(phase276_summary, "phase276_interpretation_complete", 0))
    phase276_next = str(metric_value(phase276_summary, "phase276_next_best_action", ""))
    full_depth_present = all(col in events.columns for col in FULL_DEPTH_COLUMNS)
    l1_only_rows = int(scenarios["l1_only_variant"].astype(int).sum()) if not scenarios.empty else 0
    cost200_above = as_int(metric_value(summary, "phase277_cost200_above12_scenario_rows", 0))
    rows = [
        ("P277_PHASE276_WORK_ORDER_PRESENT", "run_phase277_cost_robust_full_depth_redesign_search" in phase276_next, phase276_next, "Phase276 next action targets Phase277", "hard"),
        ("P277_PHASE276_INTERPRETATION_COMPLETE", phase276_complete == 1, phase276_complete, "Phase276 complete", "hard"),
        ("P277_ROUTE_CONTRACT_PRESENT", int(route["contract_id"].astype(str).eq("P277_SEARCH_TYPE").sum()) == 1, len(route), "Phase277 route contract present", "hard"),
        ("P277_COST200_EVENT_UNIVERSE_PRESENT", len(events) > 0, len(events), ">0 cost200 full-depth events", "hard"),
        ("P277_FULL_DEPTH_FEATURES_PRESENT", full_depth_present, ";".join(FULL_DEPTH_COLUMNS), "top-five and levels 2-5 features present", "hard"),
        ("P277_VARIANTS_EVALUATED", len(scenarios) > 0, len(scenarios), ">0 redesign scenarios", "hard"),
        ("P277_L1_ONLY_FORBIDDEN", l1_only_rows == 0, l1_only_rows, "0 L1-only variants", "hard"),
        ("P277_OUTCOME_CLASSIFIED", cost200_above >= 0, f"cost200_above12={cost200_above}", "positive or negative outcome classified", "hard"),
        ("P277_BOUNDARIES_CLOSED", bool(not scenarios.empty and scenarios["strategy_replay_allowed"].astype(int).eq(0).all() and scenarios["paper_or_live_acceptance_allowed"].astype(int).eq(0).all() and scenarios["deployable_profitability_claim_allowed"].astype(int).eq(0).all()), "replay=0;paper=0;claim=0", "no replay/paper/live/claim", "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def build_acceptance_summary(scenarios: pd.DataFrame, variant_summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    best = scenarios.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0] if not scenarios.empty else pd.Series(dtype=object)
    cost200_above = int(pd.to_numeric(scenarios.get("cost200_above12_diagnostic", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()) if not scenarios.empty else 0
    median_above = int(variant_summary["median_above12"].astype(int).sum()) if not variant_summary.empty else 0
    worst_above = int(variant_summary["worst_case_above12"].astype(int).sum()) if not variant_summary.empty else 0
    next_action = NEXT_ACTION if hard_pass == len(hard) else REPAIR_ACTION
    rows = [
        ("phase277_cost_robust_redesign_search_complete", 1, "Phase277 cost-robust full-depth redesign search completed"),
        ("phase277_selected_route", SELECTED_ROUTE, "Selected route"),
        ("phase277_variant_rows", len(variant_summary), "Redesign variants evaluated"),
        ("phase277_scenario_rows", len(scenarios), "Cost200 redesign scenarios evaluated"),
        ("phase277_full_depth_variant_rows", int((variant_summary["uses_top5"].astype(int).eq(1) & variant_summary["uses_levels_2_to_5"].astype(int).eq(1)).sum()) if not variant_summary.empty else 0, "Variants using top-five and levels 2-5 features"),
        ("phase277_l1_only_variant_rows", int(variant_summary["l1_only_variant"].astype(int).sum()) if not variant_summary.empty else 0, "L1-only variants"),
        ("phase277_cost200_above12_scenario_rows", cost200_above, "Cost200 above-12 redesign scenarios"),
        ("phase277_cost200_median_above12_variant_rows", median_above, "Cost200 variants with median annualized above 12%"),
        ("phase277_cost200_worst_case_above12_variant_rows", worst_above, "Cost200 variants with worst-case annualized above 12%"),
        ("phase277_best_variant_id", best.get("phase277_variant_id", ""), "Best redesign variant"),
        ("phase277_best_redesign_family", best.get("redesign_family", ""), "Best redesign family"),
        ("phase277_best_realized_net_pnl_inr", best.get("realized_net_pnl_inr", ""), "Best realized net P&L"),
        ("phase277_best_cost200_annualized_pct", best.get("mechanical_one_date_annualized_portfolio_return_pct", ""), "Best cost200 annualized diagnostic"),
        ("phase277_best_scheduled_event_rows", best.get("scheduled_event_rows", ""), "Best scheduled event rows"),
        ("phase277_strategy_replay_allowed", 0, "No strategy replay unlocked"),
        ("phase277_strategy_promotion_allowed", 0, "No strategy promotion unlocked"),
        ("phase277_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
        ("phase277_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        ("phase277_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase277_hard_gate_rows", len(hard), "Hard gates evaluated"),
        ("phase277_next_best_action", next_action, "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase277 Cost-robust Full-depth Redesign Search",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase277 searches observable full-depth L2 filters for cost200 robustness.",
        "Selection rules use top-five depth, levels 2-5 depth, replenishment/withdrawal, spread, churn, and event sparsity features only; gross/net edge is used only for post-selection scoring.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    phase275_dir: Path = DEFAULT_PHASE275_DIR,
    phase276_dir: Path = DEFAULT_PHASE276_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase276_summary = read_csv(phase276_dir / "phase276_acceptance_summary.csv")
    route = read_csv(phase276_dir / "phase276_next_route_contract.csv")
    ledger = read_csv(phase275_dir / "phase275_sample_synthetic_scheduled_event_ledger.csv")
    if phase276_summary.empty:
        raise FileNotFoundError("Missing Phase276 acceptance summary.")
    if route.empty:
        raise FileNotFoundError("Missing Phase276 next route contract.")
    anchors = [item.strip() for item in parse_contract_value(route, "P277_ANCHOR_PROFILES").split(";") if item.strip()]
    events = prepare_event_universe(ledger, anchors)
    scenarios, sample_ledger = evaluate_variants(events)
    variant_summary = build_variant_summary(scenarios)
    acceptance_placeholder = build_acceptance_summary(scenarios, variant_summary, pd.DataFrame(columns=["severity", "passed"]))
    gates = build_gate_evaluation(phase276_summary, route, events, scenarios, acceptance_placeholder)
    acceptance = build_acceptance_summary(scenarios, variant_summary, gates)

    events.to_csv(output_dir / "phase277_cost200_redesign_event_universe.csv", index=False)
    scenarios.to_csv(output_dir / "phase277_cost_robust_redesign_scenario_results.csv", index=False)
    variant_summary.to_csv(output_dir / "phase277_cost_robust_redesign_variant_summary.csv", index=False)
    sample_ledger.to_csv(output_dir / "phase277_sample_redesign_scheduled_event_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase277_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase277_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase277_cost_robust_full_depth_redesign_search_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Top Variant Summary": variant_summary.head(20),
            "Top Scenarios": scenarios.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).head(20),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase277_cost_robust_full_depth_redesign_search",
        **reproducibility_fields(
            artifact_id="phase277",
            generated_utc=generated_utc,
            inputs={
                "phase275_sample_synthetic_scheduled_event_ledger": str(phase275_dir / "phase275_sample_synthetic_scheduled_event_ledger.csv"),
                "phase276_acceptance_summary": str(phase276_dir / "phase276_acceptance_summary.csv"),
                "phase276_next_route_contract": str(phase276_dir / "phase276_next_route_contract.csv"),
            },
            parameters={
                "selected_route": SELECTED_ROUTE,
                "target_cost_profile": TARGET_COST_PROFILE,
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "initial_capital_grid_inr": INITIAL_CAPITAL_GRID_INR,
                "fixed_notional_grid_inr": FIXED_NOTIONAL_GRID_INR,
                "max_concurrent_grid": MAX_CONCURRENT_GRID,
                "quantiles": QUANTILES,
                "full_depth_columns": FULL_DEPTH_COLUMNS,
                "l1_only_variant_allowed": 0,
                "strategy_replay_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "cost200_redesign_event_universe": str(output_dir / "phase277_cost200_redesign_event_universe.csv"),
                "cost_robust_redesign_scenario_results": str(output_dir / "phase277_cost_robust_redesign_scenario_results.csv"),
                "cost_robust_redesign_variant_summary": str(output_dir / "phase277_cost_robust_redesign_variant_summary.csv"),
                "sample_redesign_scheduled_event_ledger": str(output_dir / "phase277_sample_redesign_scheduled_event_ledger.csv"),
                "gate_evaluation": str(output_dir / "phase277_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase277_acceptance_summary.csv"),
                "report": str(output_dir / "phase277_cost_robust_full_depth_redesign_search_report.md"),
                "manifest": str(output_dir / "phase277_cost_robust_full_depth_redesign_search_manifest.json"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase277_no_new_live_latency_synthetic_redesign",
        ),
    }
    (output_dir / "phase277_cost_robust_full_depth_redesign_search_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase277 cost-robust full-depth redesign search.")
    parser.add_argument("--phase275-dir", type=Path, default=DEFAULT_PHASE275_DIR)
    parser.add_argument("--phase276-dir", type=Path, default=DEFAULT_PHASE276_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase275_dir=args.phase275_dir, phase276_dir=args.phase276_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
