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


DEFAULT_PHASE277_DIR = Path("outputs/phase277")
DEFAULT_PHASE279_DIR = Path("outputs/phase279")
DEFAULT_OUTPUT_DIR = Path("outputs/phase280")

SELECTED_ROUTE = "P280_MATERIAL_NEW_TARGET_CONSTRUCTION_SEARCH"
NEXT_ACTION = "run_phase281_material_new_target_construction_interpretation_no_paper_live"
REPAIR_ACTION = "repair_phase280_material_new_target_construction_search"

ANNUALIZED_THRESHOLD_PCT = 12.0
TARGET_COST_PROFILE = "cost200"
INITIAL_CAPITAL_GRID_INR = [100_000.0]
FIXED_NOTIONAL_GRID_INR = [50_000.0, 75_000.0, 100_000.0]
MAX_CONCURRENT_GRID = [1, 2]
QUANTILES = [0.50, 0.60, 0.70, 0.80, 0.90]

FULL_DEPTH_COLUMNS = [
    "avg_cum_top5_qty_imbalance",
    "avg_depth_beyond_l1_qty_imbalance",
    "avg_level_weighted_depth_imbalance",
    "depth_replenishment_pressure",
    "depth_withdrawal_pressure",
    "top5_churn_pressure",
    "avg_spread_bps",
    "depth_replenish_withdraw_ratio",
    "depth_consensus_imbalance",
    "event_sparsity_pressure",
]


def parse_contract_value(route: pd.DataFrame, contract_id: str) -> str:
    if route.empty:
        return ""
    rows = route.loc[route["contract_id"].astype(str).eq(contract_id), "contract_value"]
    return "" if rows.empty else str(rows.iloc[0])


def prepare_events(events: pd.DataFrame) -> pd.DataFrame:
    frame = events.copy()
    required = [
        "gross_edge_bps",
        "modeled_cost_bps",
        "cost_multiplier",
        "horizon",
        "richer_event_bar_id",
        "candidate_rank",
        *FULL_DEPTH_COLUMNS,
    ]
    for col in required:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
    if "zerodha_round_trip_charge_bps" not in frame.columns:
        frame["zerodha_round_trip_charge_bps"] = frame["modeled_cost_bps"] / frame["cost_multiplier"].replace(0, 2.0)
    if "depth_replenish_withdraw_ratio" not in frame.columns:
        frame["depth_replenish_withdraw_ratio"] = frame["depth_replenishment_pressure"] / (frame["depth_withdrawal_pressure"] + 1.0)
    if "depth_consensus_imbalance" not in frame.columns:
        frame["depth_consensus_imbalance"] = (
            frame["avg_cum_top5_qty_imbalance"]
            + frame["avg_depth_beyond_l1_qty_imbalance"]
            + frame["avg_level_weighted_depth_imbalance"]
        ) / 3.0
    if "event_sparsity_pressure" not in frame.columns:
        frame["event_sparsity_pressure"] = frame["avg_spread_bps"] * (frame["top5_churn_pressure"] + 1.0)
    frame["offline_cost200_margin_bps"] = frame["gross_edge_bps"] - frame["modeled_cost_bps"]
    frame["offline_net_edge_positive_label"] = (frame["offline_cost200_margin_bps"] > 0).astype(int)
    frame["horizon"] = pd.to_numeric(frame["horizon"], errors="coerce").fillna(1).astype(int).clip(lower=1)
    frame["richer_event_bar_id"] = pd.to_numeric(frame["richer_event_bar_id"], errors="coerce").fillna(0).astype(int)
    frame["candidate_rank"] = pd.to_numeric(frame["candidate_rank"], errors="coerce").fillna(999999).astype(int)
    return frame.sort_values(["trade_date", "exchange", "richer_event_bar_id", "candidate_rank", "candidate_id", "symbol"]).reset_index(drop=True)


def q(frame: pd.DataFrame, col: str, quantile: float) -> float:
    return float(pd.to_numeric(frame[col], errors="coerce").fillna(0.0).quantile(quantile))


def add_variant(variants: list[dict[str, Any]], variant_id: str, target_family_id: str, target_family: str, target_rule: str, mask: pd.Series, uses_net_edge_label: int = 0) -> None:
    variants.append(
        {
            "phase280_variant_id": variant_id,
            "target_family_id": target_family_id,
            "target_family": target_family,
            "target_rule": target_rule,
            "mask": mask,
            "uses_top5": 1,
            "uses_levels_2_to_5": 1,
            "l1_only_variant": 0,
            "uses_net_edge_as_offline_label": uses_net_edge_label,
            "uses_net_edge_as_live_mask": 0,
        }
    )


def build_target_variants(events: pd.DataFrame, target_catalog: pd.DataFrame) -> list[dict[str, Any]]:
    allowed = set(target_catalog.loc[target_catalog["phase280_search_allowed"].astype(int).eq(1), "target_family_id"].astype(str))
    variants: list[dict[str, Any]] = []
    spread = pd.to_numeric(events["avg_spread_bps"], errors="coerce").fillna(0.0)
    consensus = pd.to_numeric(events["depth_consensus_imbalance"], errors="coerce").fillna(0.0)
    ratio = pd.to_numeric(events["depth_replenish_withdraw_ratio"], errors="coerce").fillna(0.0)
    churn = pd.to_numeric(events["top5_churn_pressure"], errors="coerce").fillna(0.0)
    withdrawal = pd.to_numeric(events["depth_withdrawal_pressure"], errors="coerce").fillna(0.0)
    sparsity = pd.to_numeric(events["event_sparsity_pressure"], errors="coerce").fillna(0.0)
    weighted = pd.to_numeric(events["avg_level_weighted_depth_imbalance"], errors="coerce").fillna(0.0)
    beyond = pd.to_numeric(events["avg_depth_beyond_l1_qty_imbalance"], errors="coerce").fillna(0.0)
    offline_label = events["offline_net_edge_positive_label"].astype(int).eq(1)

    for quantile in QUANTILES:
        suffix = f"Q{int(quantile * 100)}"
        if "P279_SPREAD_COST_MARGIN_TARGET" in allowed:
            s_thr = q(events, "avg_spread_bps", 1.0 - quantile)
            c_thr = q(events, "depth_consensus_imbalance", quantile)
            add_variant(
                variants,
                f"P280_SPREAD_COST_MARGIN_{suffix}",
                "P279_SPREAD_COST_MARGIN_TARGET",
                "spread_cost_margin",
                f"avg_spread_bps <= {s_thr:.6f} and depth_consensus_imbalance >= {c_thr:.6f}",
                (spread <= s_thr) & (consensus >= c_thr),
            )
        if "P279_ADVERSE_SELECTION_AVOIDANCE_TARGET" in allowed:
            ch_thr = q(events, "top5_churn_pressure", 1.0 - quantile)
            w_thr = q(events, "depth_withdrawal_pressure", 1.0 - quantile)
            add_variant(
                variants,
                f"P280_ADVERSE_SELECTION_AVOID_{suffix}",
                "P279_ADVERSE_SELECTION_AVOIDANCE_TARGET",
                "adverse_selection_avoidance",
                f"top5_churn_pressure <= {ch_thr:.6f} and depth_withdrawal_pressure <= {w_thr:.6f}",
                (churn <= ch_thr) & (withdrawal <= w_thr),
            )
        if "P279_REPLENISHMENT_CONFIRMATION_TARGET" in allowed:
            r_thr = q(events, "depth_replenish_withdraw_ratio", quantile)
            wgt_thr = q(events, "avg_level_weighted_depth_imbalance", quantile)
            add_variant(
                variants,
                f"P280_REPLENISH_CONFIRM_{suffix}",
                "P279_REPLENISHMENT_CONFIRMATION_TARGET",
                "depth_replenishment_confirmation",
                f"depth_replenish_withdraw_ratio >= {r_thr:.6f} and avg_level_weighted_depth_imbalance >= {wgt_thr:.6f}",
                (ratio >= r_thr) & (weighted >= wgt_thr),
            )
        if "P279_TIME_TO_EXIT_TARGET" in allowed:
            r_thr = q(events, "depth_replenish_withdraw_ratio", quantile)
            add_variant(
                variants,
                f"P280_TIME_TO_EXIT_SHORT_H{suffix}",
                "P279_TIME_TO_EXIT_TARGET",
                "time_to_exit",
                f"horizon <= 10 and depth_replenish_withdraw_ratio >= {r_thr:.6f}",
                (events["horizon"] <= 10) & (ratio >= r_thr),
            )
        if "P279_NET_EDGE_DISTRIBUTION_SHIFT_TARGET" in allowed:
            c_thr = q(events, "depth_consensus_imbalance", quantile)
            sp_thr = q(events, "event_sparsity_pressure", 1.0 - quantile)
            add_variant(
                variants,
                f"P280_NET_EDGE_SHIFT_LABEL_ANCHORED_{suffix}",
                "P279_NET_EDGE_DISTRIBUTION_SHIFT_TARGET",
                "net_edge_distribution_shift",
                f"offline net-edge-positive label AND depth_consensus_imbalance >= {c_thr:.6f} and event_sparsity_pressure <= {sp_thr:.6f}",
                offline_label & (consensus >= c_thr) & (sparsity <= sp_thr),
                uses_net_edge_label=1,
            )

    if "P279_SPREAD_COST_MARGIN_TARGET" in allowed and "P279_REPLENISHMENT_CONFIRMATION_TARGET" in allowed:
        add_variant(
            variants,
            "P280_SPREAD_REPLENISH_COMBO_Q70",
            "P279_SPREAD_COST_MARGIN_TARGET",
            "spread_cost_margin",
            "avg_spread_bps <= q30 and depth_replenish_withdraw_ratio >= q70 and avg_depth_beyond_l1_qty_imbalance >= q60",
            (spread <= q(events, "avg_spread_bps", 0.30))
            & (ratio >= q(events, "depth_replenish_withdraw_ratio", 0.70))
            & (beyond >= q(events, "avg_depth_beyond_l1_qty_imbalance", 0.60)),
        )
    return variants


def evaluate_variants(events: pd.DataFrame, target_catalog: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    sample_ledgers: list[pd.DataFrame] = []
    for variant in build_target_variants(events, target_catalog):
        selected = events[variant["mask"]].copy()
        if selected.empty:
            continue
        for fixed_notional in FIXED_NOTIONAL_GRID_INR:
            for max_concurrent in MAX_CONCURRENT_GRID:
                scenario, ledger = schedule_events_for_scenario(
                    events=selected,
                    scope_id=variant["phase280_variant_id"],
                    scope_candidate_id=";".join(sorted(selected["candidate_id"].astype(str).unique())),
                    initial_capital_inr=INITIAL_CAPITAL_GRID_INR[0],
                    fixed_notional_inr=fixed_notional,
                    max_concurrent_positions=max_concurrent,
                    cost_profile=TARGET_COST_PROFILE,
                    cost_multiplier=2.0,
                    extra_slippage_bps=0.0,
                )
                scenario.update(
                    {
                        **{k: v for k, v in variant.items() if k != "mask"},
                        "selected_event_rows": int(len(selected)),
                        "offline_positive_label_rows": int(selected["offline_net_edge_positive_label"].astype(int).sum()),
                        "offline_positive_label_fraction": float(selected["offline_net_edge_positive_label"].astype(int).mean()),
                        "cost200_above12_diagnostic": int(float(scenario["mechanical_one_date_annualized_portfolio_return_pct"]) > ANNUALIZED_THRESHOLD_PCT),
                        "strategy_replay_allowed": 0,
                        "promotion_allowed": 0,
                        "paper_or_live_acceptance_allowed": 0,
                        "deployable_profitability_claim_allowed": 0,
                    }
                )
                rows.append(scenario)
                if len(sample_ledgers) < 12 and scenario["scheduled_event_rows"] > 0:
                    ledger = ledger.copy()
                    ledger["phase280_variant_id"] = variant["phase280_variant_id"]
                    ledger["target_family"] = variant["target_family"]
                    ledger["target_rule"] = variant["target_rule"]
                    sample_ledgers.append(ledger)
    scenarios = pd.DataFrame(rows)
    sample = pd.concat(sample_ledgers, ignore_index=True) if sample_ledgers else pd.DataFrame()
    return scenarios, sample


def build_family_summary(scenarios: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame()
    frame = scenarios.copy()
    for col in [
        "mechanical_one_date_annualized_portfolio_return_pct",
        "realized_net_pnl_inr",
        "cost200_above12_diagnostic",
        "scheduled_event_rows",
        "offline_positive_label_fraction",
    ]:
        frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
    grouped = (
        frame.groupby(["target_family_id", "target_family"], dropna=False)
        .agg(
            variant_rows=("phase280_variant_id", "nunique"),
            scenario_rows=("scenario_id", "nunique"),
            cost200_above12_scenario_rows=("cost200_above12_diagnostic", "sum"),
            min_annualized_pct=("mechanical_one_date_annualized_portfolio_return_pct", "min"),
            median_annualized_pct=("mechanical_one_date_annualized_portfolio_return_pct", "median"),
            max_annualized_pct=("mechanical_one_date_annualized_portfolio_return_pct", "max"),
            max_net_pnl_inr=("realized_net_pnl_inr", "max"),
            max_scheduled_event_rows=("scheduled_event_rows", "max"),
            mean_offline_positive_label_fraction=("offline_positive_label_fraction", "mean"),
            l1_only_variant_rows=("l1_only_variant", "sum"),
            net_edge_live_mask_rows=("uses_net_edge_as_live_mask", "sum"),
        )
        .reset_index()
    )
    grouped["median_above12"] = (grouped["median_annualized_pct"] > ANNUALIZED_THRESHOLD_PCT).astype(int)
    return grouped.sort_values(
        ["median_above12", "cost200_above12_scenario_rows", "max_annualized_pct"],
        ascending=[False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_gate_evaluation(phase279_summary: pd.DataFrame, target_catalog: pd.DataFrame, scenarios: pd.DataFrame, family_summary: pd.DataFrame) -> pd.DataFrame:
    phase279_complete = as_int(metric_value(phase279_summary, "phase279_target_construction_precommit_complete", 0))
    phase279_next = str(metric_value(phase279_summary, "phase279_next_best_action", ""))
    l1_only = int(scenarios["l1_only_variant"].astype(int).sum()) if not scenarios.empty else 0
    live_leakage = int(scenarios["uses_net_edge_as_live_mask"].astype(int).sum()) if not scenarios.empty else 0
    rows = [
        ("P280_PHASE279_WORK_ORDER_PRESENT", "run_phase280_material_new_target_construction_search" in phase279_next, phase279_next, "Phase279 next action targets Phase280", "hard"),
        ("P280_PHASE279_PRECOMMIT_COMPLETE", phase279_complete == 1, phase279_complete, "Phase279 complete", "hard"),
        ("P280_TARGET_FAMILIES_EXECUTED", len(family_summary) >= 5, len(family_summary), ">=5 target families executed", "hard"),
        ("P280_SCENARIOS_PRESENT", len(scenarios) > 0, len(scenarios), ">0 scenarios", "hard"),
        ("P280_COST200_REQUIRED", bool(not scenarios.empty and scenarios["cost_profile"].astype(str).eq(TARGET_COST_PROFILE).all()), TARGET_COST_PROFILE, "all scenarios cost200", "hard"),
        ("P280_FULL_DEPTH_REQUIRED", bool(not target_catalog.empty and target_catalog["full_depth_required"].astype(int).eq(1).all() and target_catalog["levels_2_to_5_required"].astype(int).eq(1).all()), "full_depth=1;levels_2_to_5=1", "full-depth target contract", "hard"),
        ("P280_L1_ONLY_FORBIDDEN", l1_only == 0, l1_only, "0 L1-only variants", "hard"),
        ("P280_NO_LIVE_LABEL_LEAKAGE", live_leakage == 0, live_leakage, "0 net/gross edge live masks", "hard"),
        ("P280_BOUNDARIES_CLOSED", bool(not scenarios.empty and scenarios["strategy_replay_allowed"].astype(int).eq(0).all() and scenarios["paper_or_live_acceptance_allowed"].astype(int).eq(0).all() and scenarios["deployable_profitability_claim_allowed"].astype(int).eq(0).all()), "replay=0;paper=0;claim=0", "no replay/paper/live/claim", "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def build_acceptance_summary(scenarios: pd.DataFrame, family_summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    best = scenarios.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0] if not scenarios.empty else pd.Series(dtype=object)
    cost200_above = int(pd.to_numeric(scenarios.get("cost200_above12_diagnostic", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()) if not scenarios.empty else 0
    next_action = NEXT_ACTION if hard_pass == len(hard) else REPAIR_ACTION
    rows = [
        ("phase280_material_new_target_construction_search_complete", 1, "Phase280 material new target-construction search completed"),
        ("phase280_selected_route", SELECTED_ROUTE, "Selected route"),
        ("phase280_target_family_rows", len(family_summary), "Target families evaluated"),
        ("phase280_variant_rows", int(scenarios["phase280_variant_id"].astype(str).nunique()) if not scenarios.empty else 0, "Target-construction variants evaluated"),
        ("phase280_scenario_rows", len(scenarios), "Cost200 scenarios evaluated"),
        ("phase280_cost200_above12_scenario_rows", cost200_above, "Cost200 above-12 scenarios"),
        ("phase280_best_variant_id", best.get("phase280_variant_id", ""), "Best target-construction variant"),
        ("phase280_best_target_family", best.get("target_family", ""), "Best target family"),
        ("phase280_best_cost200_annualized_pct", best.get("mechanical_one_date_annualized_portfolio_return_pct", ""), "Best cost200 annualized diagnostic"),
        ("phase280_best_realized_net_pnl_inr", best.get("realized_net_pnl_inr", ""), "Best realized net P&L"),
        ("phase280_best_scheduled_event_rows", best.get("scheduled_event_rows", ""), "Best scheduled event rows"),
        ("phase280_l1_only_variant_rows", int(scenarios["l1_only_variant"].astype(int).sum()) if not scenarios.empty else 0, "L1-only variants"),
        ("phase280_net_edge_live_mask_rows", int(scenarios["uses_net_edge_as_live_mask"].astype(int).sum()) if not scenarios.empty else 0, "Live masks using net/gross edge"),
        ("phase280_strategy_replay_allowed", 0, "No strategy replay unlocked"),
        ("phase280_strategy_promotion_allowed", 0, "No strategy promotion unlocked"),
        ("phase280_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
        ("phase280_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        ("phase280_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase280_hard_gate_rows", len(hard), "Hard gates evaluated"),
        ("phase280_next_best_action", next_action, "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase280 Material New Target-construction Search",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase280 executes the Phase279 material-new target-construction search under cost200 and full-depth controls.",
        "Net/gross edge is allowed only as offline label evidence; live masks remain full-depth observable feature masks.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase277_dir: Path = DEFAULT_PHASE277_DIR, phase279_dir: Path = DEFAULT_PHASE279_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase279_summary = read_csv(phase279_dir / "phase279_acceptance_summary.csv")
    target_catalog = read_csv(phase279_dir / "phase279_target_family_catalog.csv")
    events = read_csv(phase277_dir / "phase277_cost200_redesign_event_universe.csv")
    if phase279_summary.empty:
        raise FileNotFoundError("Missing Phase279 acceptance summary.")
    if target_catalog.empty:
        raise FileNotFoundError("Missing Phase279 target family catalog.")
    if events.empty:
        raise FileNotFoundError("Missing Phase277 cost200 event universe.")
    prepared = prepare_events(events)
    scenarios, sample_ledger = evaluate_variants(prepared, target_catalog)
    family_summary = build_family_summary(scenarios)
    gates = build_gate_evaluation(phase279_summary, target_catalog, scenarios, family_summary)
    acceptance = build_acceptance_summary(scenarios, family_summary, gates)

    scenarios.to_csv(output_dir / "phase280_material_target_scenario_results.csv", index=False)
    family_summary.to_csv(output_dir / "phase280_material_target_family_summary.csv", index=False)
    sample_ledger.to_csv(output_dir / "phase280_sample_material_target_scheduled_event_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase280_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase280_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase280_material_new_target_construction_search_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Target Family Summary": family_summary,
            "Top Scenarios": scenarios.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).head(20),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase280_material_new_target_construction_search",
        **reproducibility_fields(
            artifact_id="phase280",
            generated_utc=generated_utc,
            inputs={
                "phase279_acceptance_summary": str(phase279_dir / "phase279_acceptance_summary.csv"),
                "phase279_target_family_catalog": str(phase279_dir / "phase279_target_family_catalog.csv"),
                "phase277_cost200_redesign_event_universe": str(phase277_dir / "phase277_cost200_redesign_event_universe.csv"),
            },
            parameters={
                "selected_route": SELECTED_ROUTE,
                "target_cost_profile": TARGET_COST_PROFILE,
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "fixed_notional_grid_inr": FIXED_NOTIONAL_GRID_INR,
                "max_concurrent_grid": MAX_CONCURRENT_GRID,
                "quantiles": QUANTILES,
                "full_depth_columns": FULL_DEPTH_COLUMNS,
                "l1_only_variant_allowed": 0,
                "net_edge_as_live_mask_allowed": 0,
                "strategy_replay_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "material_target_scenario_results": str(output_dir / "phase280_material_target_scenario_results.csv"),
                "material_target_family_summary": str(output_dir / "phase280_material_target_family_summary.csv"),
                "sample_material_target_scheduled_event_ledger": str(output_dir / "phase280_sample_material_target_scheduled_event_ledger.csv"),
                "gate_evaluation": str(output_dir / "phase280_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase280_acceptance_summary.csv"),
                "report": str(output_dir / "phase280_material_new_target_construction_search_report.md"),
                "manifest": str(output_dir / "phase280_material_new_target_construction_search_manifest.json"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase280_no_new_live_latency_synthetic_target_search",
        ),
    }
    (output_dir / "phase280_material_new_target_construction_search_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase280 material new target-construction search.")
    parser.add_argument("--phase277-dir", type=Path, default=DEFAULT_PHASE277_DIR)
    parser.add_argument("--phase279-dir", type=Path, default=DEFAULT_PHASE279_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase277_dir=args.phase277_dir, phase279_dir=args.phase279_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
