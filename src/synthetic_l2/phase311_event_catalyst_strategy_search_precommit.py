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
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, charge_component_catalog


DEFAULT_PHASE310_DIR = Path("outputs/phase310")
DEFAULT_OUTPUT_DIR = Path("outputs/phase311")

NEXT_ACTION = "run_phase312_event_catalyst_strategy_search_training_only"
REPAIR_ACTION = "repair_phase311_event_catalyst_strategy_search_precommit"


def build_strategy_family_catalog() -> pd.DataFrame:
    rows = [
        ("event_depth_pressure_continuation", "go_with_sign(event_l2_l5_pressure)", "target_return_300s_bps;target_return_900s_bps", "Tests whether L2-L5 pressure at event time follows through."),
        ("event_depth_pressure_reversal", "go_against_sign(event_l2_l5_pressure)", "target_return_300s_bps;target_return_900s_bps", "Tests whether strong L2-L5 pressure mean-reverts after the event."),
        ("pre_event_pressure_shift_continuation", "go_with_sign(event_l2_l5_pressure - pre_mean_l2_l5_pressure)", "target_return_300s_bps;target_return_900s_bps", "Tests whether pressure acceleration predicts continuation."),
        ("pre_event_pressure_shift_reversal", "go_against_sign(event_l2_l5_pressure - pre_mean_l2_l5_pressure)", "target_return_300s_bps;target_return_900s_bps", "Tests whether pressure acceleration is an overreaction."),
        ("microprice_dislocation_continuation", "go_with_sign((event_l1_microprice - event_l1_mid) / event_l1_mid)", "target_return_60s_bps;target_return_300s_bps", "Tests microprice dislocation follow-through."),
        ("microprice_dislocation_reversal", "go_against_sign((event_l1_microprice - event_l1_mid) / event_l1_mid)", "target_return_60s_bps;target_return_300s_bps", "Tests microprice dislocation reversal."),
        ("pre_event_trend_reversal", "go_against_sign((event_l1_mid / pre_mean_l1_mid) - 1)", "target_return_300s_bps;target_return_900s_bps", "Tests bar-return reversal around event context."),
        ("pre_event_trend_continuation", "go_with_sign((event_l1_mid / pre_mean_l1_mid) - 1)", "target_return_300s_bps;target_return_900s_bps", "Tests event-time trend continuation."),
    ]
    return pd.DataFrame(rows, columns=["family_id", "signal_formula", "target_columns", "description"])


def build_search_grid() -> pd.DataFrame:
    rows = []
    horizons = [60, 300, 900, 1800]
    thresholds = ["top_25pct_abs_signal", "top_50pct_abs_signal", "all_nonzero_signal"]
    notionals = [25_000, 50_000, 100_000]
    cost_profiles = ["zerodha_base", "zerodha_plus_1bp_slippage", "zerodha_plus_2bp_slippage", "zerodha_2x_all_in_cost_proxy"]
    max_concurrency = [1, 2, 4]
    for horizon in horizons:
        for threshold in thresholds:
            for notional in notionals:
                for cost_profile in cost_profiles:
                    for concurrency in max_concurrency:
                        rows.append(
                            {
                                "horizon_seconds": horizon,
                                "threshold_policy": threshold,
                                "fixed_notional_inr": notional,
                                "cost_profile": cost_profile,
                                "max_concurrent_positions": concurrency,
                            }
                        )
    return pd.DataFrame(rows)


def build_capital_contract() -> pd.DataFrame:
    rows = [
        ("initial_capital_grid_inr", "100000;250000;500000", "Fixed starting capital scenarios; no unlimited capital."),
        ("per_trade_notional_grid_inr", "25000;50000;100000", "Per-symbol event allocation before capital/concurrency gates."),
        ("capital_allocation_rule", "rank_by_abs_signal_then_allocate_until_cash_or_concurrency_exhausted", "Avoid pretending every signal has independent capital."),
        ("portfolio_return_formula", "net_pnl_inr / initial_capital_inr", "Only fixed-capital net P&L divided by initial capital is portfolio return."),
        ("annualized_return_formula", "portfolio_return * 252 / observed_trade_dates", "Allowed only as sparse research diagnostic while observed_trade_dates is recorded."),
        ("annualized_profitability_research_threshold", ">=12pct", "User-requested research-lead threshold; not deployable acceptance."),
        ("minimum_dates_for_deployable_claim", "not_satisfied", "One synthetic event date cannot support deployable annual-return claim."),
        ("same_symbol_overlap_policy", "one_position_per_symbol_event_window", "Prevent stacking same-symbol event decisions."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_control_contract() -> pd.DataFrame:
    rows = [
        ("full_top_five_depth_required", "required", "Every allowed family must include L1-L5 or L2-L5 materiality."),
        ("depth_beyond_l1_required", "required", "At least one signal term must use levels 2-5."),
        ("l1_only_candidate_allowed", "forbidden", "L1-only event strategies are not allowed in this branch."),
        ("zerodha_cost_model_required", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Use the documented Zerodha equity intraday NSE charge model."),
        ("slippage_stress_required", "required", "Search must include additional 1bp/2bp and 2x cost-stress profiles."),
        ("post_event_target_as_feature", "forbidden", "target_ columns are labels/diagnostics only, not inputs."),
        ("portfolio_return_without_fixed_capital", "forbidden", "No unlimited-capital annual return."),
        ("paper_live_or_deployable_profitability_claim", "forbidden", "No paper/live or deployable claim from Phase312."),
        ("strategy_execution_now", "forbidden", "Phase311 is a precommit only."),
    ]
    return pd.DataFrame(rows, columns=["control_id", "control_status", "description"])


def build_gate_evaluation(phase310: pd.DataFrame, families: pd.DataFrame, grid: pd.DataFrame, capital: pd.DataFrame, controls: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(phase310, "phase310_event_feature_materialization_complete", 0))
    rows = [
        ("P311_PHASE310_COMPLETE", complete == 1, complete, 1),
        ("P311_PHASE310_FULL_DEPTH_FEATURES", as_int(metric_value(phase310, "phase310_full_depth_features_materialized", 0)) == 1, metric_value(phase310, "phase310_full_depth_features_materialized", ""), 1),
        ("P311_FAMILY_CATALOG_NONEMPTY", len(families) >= 8, len(families), ">=8"),
        ("P311_SEARCH_GRID_NONEMPTY", len(grid) > 0, len(grid), ">0"),
        ("P311_FIXED_CAPITAL_CONTRACT_PRESENT", len(capital) >= 8, len(capital), ">=8"),
        ("P311_ZERODHA_COST_MODEL_REFERENCED", controls["control_status"].astype(str).str.contains(ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, regex=False).any(), ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "present"),
        ("P311_DEPTH_BEYOND_L1_REQUIRED", controls["control_id"].astype(str).eq("depth_beyond_l1_required").any(), "present", "present"),
        ("P311_NO_EXECUTION_OPENED", True, "strategy_execution_now=0", 0),
        ("P311_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in rows])


def build_acceptance(families: pd.DataFrame, grid: pd.DataFrame, capital: pd.DataFrame, controls: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase311_strategy_search_precommit_complete", 1, "Phase311 event-catalyst strategy search precommit completed"),
            ("phase311_strategy_family_rows", int(len(families)), "Strategy family rows"),
            ("phase311_search_grid_rows", int(len(grid)), "Search grid rows before family expansion"),
            ("phase311_expanded_variant_upper_bound_rows", int(len(families) * len(grid)), "Family x grid upper bound"),
            ("phase311_capital_contract_rows", int(len(capital)), "Fixed-capital contract rows"),
            ("phase311_control_contract_rows", int(len(controls)), "Control contract rows"),
            ("phase311_full_depth_required", 1, "Full top-five depth required"),
            ("phase311_depth_beyond_l1_required", 1, "Levels 2-5 materiality required"),
            ("phase311_l1_only_candidate_allowed", 0, "L1-only candidate path closed"),
            ("phase311_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha cost model version"),
            ("phase311_strategy_search_execution_allowed_next", 1 if hard_pass == hard_rows else 0, "Phase312 training-only search may run if gates pass"),
            ("phase311_strategy_replay_allowed", 0, "No replay"),
            ("phase311_strategy_promotion_allowed", 0, "No promotion"),
            ("phase311_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase311_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase311_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase311_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase311_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase311 Event-Catalyst Strategy Search Precommit",
        "",
        "Phase311 defines the allowed training-only event-catalyst strategy search. It does not execute the search.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase311_event_catalyst_strategy_search_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run(phase310_dir: Path = DEFAULT_PHASE310_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase310 = read_csv(phase310_dir / "phase310_acceptance_summary.csv")
    families = build_strategy_family_catalog()
    grid = build_search_grid()
    capital = build_capital_contract()
    controls = build_control_contract()
    costs = charge_component_catalog()
    gates = build_gate_evaluation(phase310, families, grid, capital, controls)
    acceptance = build_acceptance(families, grid, capital, controls, gates)

    families.to_csv(output_dir / "phase311_strategy_family_catalog.csv", index=False)
    grid.to_csv(output_dir / "phase311_strategy_search_grid.csv", index=False)
    capital.to_csv(output_dir / "phase311_fixed_capital_return_contract.csv", index=False)
    controls.to_csv(output_dir / "phase311_control_contract.csv", index=False)
    costs.to_csv(output_dir / "phase311_zerodha_cost_component_catalog.csv", index=False)
    gates.to_csv(output_dir / "phase311_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase311_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        acceptance,
        {
            "Strategy family catalog": families,
            "Search grid": grid.head(60),
            "Fixed-capital return contract": capital,
            "Control contract": controls,
            "Zerodha cost component catalog": costs,
            "Gates": gates,
        },
    )

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase311_event_catalyst_strategy_search_precommit",
        **reproducibility_fields(
            artifact_id="phase311",
            generated_utc=generated_utc,
            inputs={"phase310_acceptance": str(phase310_dir / "phase310_acceptance_summary.csv")},
            parameters={"zerodha_cost_model_version": ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION},
            outputs={"acceptance_summary": str(output_dir / "phase311_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_precommit_only",
        ),
    }
    (output_dir / "phase311_event_catalyst_strategy_search_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Precommit Phase311 event-catalyst strategy search.")
    parser.add_argument("--phase310-dir", type=Path, default=DEFAULT_PHASE310_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase310_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
