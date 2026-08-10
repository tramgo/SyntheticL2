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
from synthetic_l2.zerodha_costs import (
    ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
    calculate_equity_intraday_nse_charges,
)


DEFAULT_PHASE310_DIR = Path("outputs/phase310")
DEFAULT_PHASE311_DIR = Path("outputs/phase311")
DEFAULT_OUTPUT_DIR = Path("outputs/phase312")

NEXT_ACTION = "run_phase313_event_catalyst_strategy_search_interpretation_no_replay"
REPAIR_ACTION = "repair_phase312_event_catalyst_strategy_search_training_only"

INITIAL_CAPITAL_GRID_INR = [100_000.0, 250_000.0, 500_000.0]
ANNUALIZED_THRESHOLD_PCT = 12.0
OBSERVED_TRADE_DATES = 1


def signed_signal(row: pd.Series, family_id: str) -> float:
    if family_id == "event_depth_pressure_continuation":
        return float(row["event_l2_l5_pressure"])
    if family_id == "event_depth_pressure_reversal":
        return -float(row["event_l2_l5_pressure"])
    if family_id == "pre_event_pressure_shift_continuation":
        return float(row["event_l2_l5_pressure"]) - float(row["pre_mean_l2_l5_pressure"])
    if family_id == "pre_event_pressure_shift_reversal":
        return -(float(row["event_l2_l5_pressure"]) - float(row["pre_mean_l2_l5_pressure"]))
    micro_dislocation = (float(row["event_l1_microprice"]) / float(row["event_l1_mid"]) - 1.0) if float(row["event_l1_mid"]) else 0.0
    if family_id == "microprice_dislocation_continuation":
        return micro_dislocation
    if family_id == "microprice_dislocation_reversal":
        return -micro_dislocation
    pre_trend = (float(row["event_l1_mid"]) / float(row["pre_mean_l1_mid"]) - 1.0) if float(row["pre_mean_l1_mid"]) else 0.0
    if family_id == "pre_event_trend_reversal":
        return -pre_trend
    if family_id == "pre_event_trend_continuation":
        return pre_trend
    return 0.0


def threshold_mask(abs_signal: pd.Series, policy: str) -> pd.Series:
    if policy == "all_nonzero_signal":
        return abs_signal > 0
    if policy == "top_50pct_abs_signal":
        return abs_signal >= abs_signal.quantile(0.50)
    if policy == "top_25pct_abs_signal":
        return abs_signal >= abs_signal.quantile(0.75)
    return pd.Series(False, index=abs_signal.index)


def cost_multiplier_and_slip(cost_profile: str) -> tuple[float, float]:
    if cost_profile == "zerodha_plus_1bp_slippage":
        return 1.0, 1.0
    if cost_profile == "zerodha_plus_2bp_slippage":
        return 1.0, 2.0
    if cost_profile == "zerodha_2x_all_in_cost_proxy":
        return 2.0, 0.0
    return 1.0, 0.0


def trade_cost_inr(notional: float, gross_return_bps: float, cost_profile: str) -> float:
    exit_value = max(0.0, notional * (1.0 + abs(gross_return_bps) / 10_000.0))
    charges = calculate_equity_intraday_nse_charges(
        buy_value_inr=notional,
        sell_value_inr=exit_value,
        buy_quantity=1.0,
        sell_quantity=1.0,
        buy_orders=1,
        sell_orders=1,
    )
    cost_mult, extra_slip_bps = cost_multiplier_and_slip(cost_profile)
    slippage = (notional + exit_value) * extra_slip_bps / 10_000.0
    return float(charges.total_charges) * cost_mult + slippage


def evaluate_scenario(features: pd.DataFrame, family_id: str, grid_row: pd.Series, initial_capital: float) -> tuple[dict[str, Any], pd.DataFrame]:
    horizon = as_int(grid_row["horizon_seconds"])
    target_col = f"target_return_{horizon}s_bps"
    if target_col not in features.columns:
        return {}, pd.DataFrame()
    frame = features.copy()
    frame["signal"] = frame.apply(lambda row: signed_signal(row, family_id), axis=1)
    frame["abs_signal"] = frame["signal"].abs()
    frame = frame[threshold_mask(frame["abs_signal"], str(grid_row["threshold_policy"]))].copy()
    frame = frame[frame["signal"].ne(0)].copy()
    if frame.empty:
        return {}, pd.DataFrame()
    frame["side"] = frame["signal"].map(lambda value: 1 if value > 0 else -1)
    frame["signed_return_bps"] = frame["side"] * pd.to_numeric(frame[target_col], errors="coerce")
    frame = frame.sort_values(["abs_signal", "symbol"], ascending=[False, True]).reset_index(drop=True)
    max_concurrent = as_int(grid_row["max_concurrent_positions"])
    notional = float(grid_row["fixed_notional_inr"])
    selected = frame.head(max_concurrent).copy()
    affordable = int(initial_capital // notional)
    selected = selected.head(max(0, affordable)).copy()
    if selected.empty:
        return {}, pd.DataFrame()
    selected["fixed_notional_inr"] = notional
    selected["initial_capital_inr"] = initial_capital
    selected["gross_pnl_inr"] = notional * selected["signed_return_bps"] / 10_000.0
    selected["cost_inr"] = selected["signed_return_bps"].map(lambda bps: trade_cost_inr(notional, float(bps), str(grid_row["cost_profile"])))
    selected["net_pnl_inr"] = selected["gross_pnl_inr"] - selected["cost_inr"]
    net_pnl = float(selected["net_pnl_inr"].sum())
    gross_pnl = float(selected["gross_pnl_inr"].sum())
    portfolio_return_pct = net_pnl / initial_capital * 100.0
    annualized_pct = portfolio_return_pct * 252.0 / OBSERVED_TRADE_DATES
    scenario_id = (
        f"P312_{family_id}_H{horizon}_{grid_row['threshold_policy']}_"
        f"N{int(notional)}_C{max_concurrent}_{grid_row['cost_profile']}_CAP{int(initial_capital)}"
    )
    selected.insert(0, "scenario_id", scenario_id)
    selected.insert(1, "family_id", family_id)
    summary = {
        "scenario_id": scenario_id,
        "family_id": family_id,
        "horizon_seconds": horizon,
        "threshold_policy": grid_row["threshold_policy"],
        "fixed_notional_inr": notional,
        "initial_capital_inr": initial_capital,
        "max_concurrent_positions": max_concurrent,
        "cost_profile": grid_row["cost_profile"],
        "candidate_signal_rows": int(len(frame)),
        "scheduled_trade_rows": int(len(selected)),
        "gross_pnl_inr": gross_pnl,
        "net_pnl_inr": net_pnl,
        "portfolio_return_pct": portfolio_return_pct,
        "annualized_return_pct_sparse": annualized_pct,
        "annualized_above_12pct_sparse": int(annualized_pct >= ANNUALIZED_THRESHOLD_PCT),
        "positive_net_pnl": int(net_pnl > 0),
        "observed_trade_dates": OBSERVED_TRADE_DATES,
        "deployable_profitability_claim_allowed": 0,
    }
    return summary, selected


def run_search(features: pd.DataFrame, families: pd.DataFrame, grid: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    summaries: list[dict[str, Any]] = []
    ledgers: list[pd.DataFrame] = []
    for family_id in families["family_id"].astype(str):
        for _, grid_row in grid.iterrows():
            for initial_capital in INITIAL_CAPITAL_GRID_INR:
                summary, ledger = evaluate_scenario(features, family_id, grid_row, initial_capital)
                if summary:
                    summaries.append(summary)
                    if len(ledgers) < 200:
                        ledgers.append(ledger)
    variants = pd.DataFrame(summaries)
    trades = pd.concat(ledgers, ignore_index=True) if ledgers else pd.DataFrame()
    return variants, trades


def build_gate_evaluation(phase311: pd.DataFrame, variants: pd.DataFrame) -> pd.DataFrame:
    precommit = as_int(metric_value(phase311, "phase311_strategy_search_precommit_complete", 0))
    execution_allowed = as_int(metric_value(phase311, "phase311_strategy_search_execution_allowed_next", 0))
    rows = [
        ("P312_PHASE311_PRECOMMIT_COMPLETE", precommit == 1, precommit, 1),
        ("P312_PHASE311_EXECUTION_ALLOWED", execution_allowed == 1, execution_allowed, 1),
        ("P312_VARIANTS_EVALUATED", len(variants) > 0, len(variants), ">0"),
        ("P312_FIXED_CAPITAL_USED", variants["initial_capital_inr"].nunique() >= 1 if not variants.empty else False, variants["initial_capital_inr"].nunique() if not variants.empty else 0, ">=1"),
        ("P312_ZERODHA_COSTS_USED", variants["cost_profile"].astype(str).str.contains("zerodha").all() if not variants.empty else False, "zerodha", "all"),
        ("P312_NO_REPLAY_PROMOTION_OR_PAPER_LIVE", True, "replay=0;promotion=0;paper=0", "all_zero"),
        ("P312_NO_DEPLOYABLE_PROFITABILITY_CLAIM", True, 0, 0),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in rows])


def build_acceptance(variants: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    best = variants.sort_values("annualized_return_pct_sparse", ascending=False).head(1) if not variants.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("phase312_strategy_search_training_complete", 1, "Phase312 event-catalyst strategy search training-only completed"),
            ("phase312_variant_rows", int(len(variants)), "Evaluated scenario rows"),
            ("phase312_positive_net_pnl_rows", int(variants["positive_net_pnl"].sum()) if not variants.empty else 0, "Rows with positive net P&L"),
            ("phase312_sparse_above12_annualized_rows", int(variants["annualized_above_12pct_sparse"].sum()) if not variants.empty else 0, "Sparse annualized rows above 12%"),
            ("phase312_best_scenario_id", best["scenario_id"].iloc[0] if not best.empty else "", "Best sparse annualized scenario"),
            ("phase312_best_annualized_return_pct_sparse", float(best["annualized_return_pct_sparse"].iloc[0]) if not best.empty else 0.0, "Best sparse annualized return"),
            ("phase312_best_net_pnl_inr", float(best["net_pnl_inr"].iloc[0]) if not best.empty else 0.0, "Best net P&L"),
            ("phase312_best_scheduled_trade_rows", int(best["scheduled_trade_rows"].iloc[0]) if not best.empty else 0, "Best scheduled trades"),
            ("phase312_observed_trade_dates", OBSERVED_TRADE_DATES, "Observed synthetic event dates"),
            ("phase312_strategy_replay_allowed", 0, "No replay"),
            ("phase312_strategy_promotion_allowed", 0, "No promotion"),
            ("phase312_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase312_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase312_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase312_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase312_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, variants: pd.DataFrame, trades: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase312 Event-Catalyst Strategy Search Training Only",
        "",
        "Phase312 executes the precommitted event-catalyst strategy search on the synthetic feature matrix.",
        "Above-12% annualized rows are sparse research leads only because the run has one observed synthetic event date.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Top scenarios",
        "",
        _markdown_table(variants.sort_values("annualized_return_pct_sparse", ascending=False).head(50) if not variants.empty else variants),
        "",
        "## Sample scheduled trades",
        "",
        _markdown_table(trades.head(80) if not trades.empty else trades),
        "",
        "## Gates",
        "",
        _markdown_table(gates),
    ]
    (output_dir / "phase312_event_catalyst_strategy_search_training_only_report.md").write_text("\n".join(lines), encoding="utf-8")


def run(phase310_dir: Path = DEFAULT_PHASE310_DIR, phase311_dir: Path = DEFAULT_PHASE311_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase311 = read_csv(phase311_dir / "phase311_acceptance_summary.csv")
    features = read_csv(phase310_dir / "phase310_event_catalyst_feature_matrix.csv")
    families = read_csv(phase311_dir / "phase311_strategy_family_catalog.csv")
    grid = read_csv(phase311_dir / "phase311_strategy_search_grid.csv")
    variants, trades = run_search(features, families, grid)
    gates = build_gate_evaluation(phase311, variants)
    acceptance = build_acceptance(variants, gates)

    variants.to_csv(output_dir / "phase312_strategy_variant_results.csv", index=False)
    trades.to_csv(output_dir / "phase312_sample_scheduled_trade_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase312_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase312_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, variants, trades, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase312_event_catalyst_strategy_search_training_only",
        **reproducibility_fields(
            artifact_id="phase312",
            generated_utc=generated_utc,
            inputs={
                "phase310_feature_matrix": str(phase310_dir / "phase310_event_catalyst_feature_matrix.csv"),
                "phase311_acceptance": str(phase311_dir / "phase311_acceptance_summary.csv"),
                "phase311_grid": str(phase311_dir / "phase311_strategy_search_grid.csv"),
            },
            parameters={"observed_trade_dates": OBSERVED_TRADE_DATES, "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT},
            outputs={"acceptance_summary": str(output_dir / "phase312_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_feature_matrix_training_search",
        ),
    }
    (output_dir / "phase312_event_catalyst_strategy_search_training_only_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase312 event-catalyst strategy search training-only.")
    parser.add_argument("--phase310-dir", type=Path, default=DEFAULT_PHASE310_DIR)
    parser.add_argument("--phase311-dir", type=Path, default=DEFAULT_PHASE311_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase310_dir, args.phase311_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
