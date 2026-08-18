from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE450_DIR = Path("outputs/phase450")
DEFAULT_DENSE_ROOT = Path("raw_synthetic_l2_dense_full_year")
DEFAULT_OUTPUT_DIR = Path("outputs/phase451")

THESIS_ID = "P451_CROSS_ASSET_ETF_PRESSURE_PRECOMMIT"
SELECTED_SOURCE_ID = "cross_asset_etf_depth_pressure_lead_lag"
NEXT_ACTION = "run_phase452_cross_asset_etf_pressure_no_paper_live"
REPAIR_ACTION = "repair_phase451_precommit_inputs"

ETF_PROXIES = ["NIFTYBEES", "BANKBEES", "ITBEES"]
TARGET_SYMBOLS = ["AXISBANK", "HDFCBANK", "ICICIBANK", "INFY", "HCLTECH", "TCS", "RELIANCE"]
MONTHS = [f"2026-{m:02d}" for m in range(1, 7)]

INITIAL_CAPITAL_INR = 1_000_000.0
ORDER_NOTIONAL_INR = 100_000.0
COST_MULTIPLIER = 2.0


def sha256_frame(frame: pd.DataFrame) -> str:
    return hashlib.sha256(frame.to_csv(index=False, lineterminator="\n").encode("utf-8")).hexdigest()


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def build_input_registry(dense_root: Path) -> pd.DataFrame:
    available_symbols = set()
    available_months = set()
    for month_dir in dense_root.glob("trade_month=*"):
        if not month_dir.is_dir():
            continue
        month = month_dir.name.split("=", 1)[-1]
        available_months.add(month)
        for symbol_dir in month_dir.glob("symbol=*"):
            if symbol_dir.is_dir():
                available_symbols.add(symbol_dir.name.split("=", 1)[-1])
    needed = ETF_PROXIES + TARGET_SYMBOLS
    missing_symbols = sorted(set(needed) - available_symbols)
    missing_months = sorted(set(MONTHS) - available_months)
    files = list(dense_root.rglob("*.parquet")) if dense_root.exists() else []
    rows = [
        ("dense_root_exists", int(dense_root.exists()), "Raw dense L1-L5 lake root exists."),
        ("dense_parquet_file_count", len(files), "Current dense Parquet file count."),
        ("available_symbol_count", len(available_symbols), "Symbols available under dense root."),
        ("available_month_count", len(available_months), "Trade months available under dense root."),
        ("etf_proxies", ";".join(ETF_PROXIES), "Cross-asset source instruments."),
        ("target_symbols", ";".join(TARGET_SYMBOLS), "Liquid target symbols."),
        ("months", ";".join(MONTHS), "Frozen execution months."),
        ("missing_required_symbols", ";".join(missing_symbols), "Must be empty."),
        ("missing_required_months", ";".join(missing_months), "Must be empty."),
        ("cost_multiplier", COST_MULTIPLIER, "Cost200 scoring."),
        ("initial_capital_inr", INITIAL_CAPITAL_INR, "Fixed capital denominator."),
        ("order_notional_inr", ORDER_NOTIONAL_INR, "Fixed order notional."),
    ]
    return pd.DataFrame(rows, columns=["input_id", "value", "description"])


def val(inputs: pd.DataFrame, key: str, default: Any = "") -> Any:
    rows = inputs.loc[inputs["input_id"].eq(key), "value"].tolist()
    return rows[0] if rows else default


def build_prior_boundary(phase450: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("P450", "depth_curvature_dynamic_route", scalar(phase450, "phase450_selected_verdict", ""), "closed; next action requires new low-turnover external or cross-asset source edge"),
        ("P447", "catalyst_continuation_stability", "rejected_by_frozen_holdout", "do not tune/reuse catalyst continuation as source"),
        ("P409", "retail_two_sided_market_maker_cancel_latency", "falsified", "do not reopen attached cancel-included charter without new external execution source"),
        ("P435", "supervised_full_depth_event_ranker", "rejected", "do not retry ranker without materially different label/source"),
    ]
    return pd.DataFrame(rows, columns=["phase", "route", "verdict_or_status", "reason_for_not_continuing"])


def build_contract() -> pd.DataFrame:
    rows = [
        ("thesis_id", THESIS_ID, "Phase451 selected source precommit."),
        ("selected_source", SELECTED_SOURCE_ID, "Materially new low-turnover cross-asset source."),
        ("market_hypothesis", "etf_proxy_l2_l5_depth_pressure_and_return_leads_constituent_short_horizon_move", "ETF/order-book pressure may reveal basket demand before all constituents adjust."),
        ("source_instruments", ";".join(ETF_PROXIES), "ETF/index-proxy source instruments."),
        ("target_symbols", ";".join(TARGET_SYMBOLS), "Frozen target basket."),
        ("months", ";".join(MONTHS), "Frozen bounded execution months before results."),
        ("feature_family", "etf_return_bps_plus_etf_l2_l5_imbalance_pressure_minus_target_l1_l2_l5_confirmation", "Primary source is cross-asset ETF pressure plus full-depth target confirmation."),
        ("entry_logic", "one_low_turnover_taker_event_per_target_date_when_proxy_pressure_agrees_with_target_depth", "Low turnover before costs."),
        ("max_events_per_target_date", "1", "No dense churning."),
        ("horizon_ticks", "240", "Fixed exit horizon."),
        ("stop_bps", "18.0", "Fixed stop."),
        ("take_profit_bps", "30.0", "Fixed take profit."),
        ("sample_stride", "4096", "Deterministic bounded scan stride."),
        ("controls_required", "source_time_shift;side_flip;target_only_l1_l5_without_etf_proxy;etf_l1_only_ablation", "Controls required in Phase452."),
        ("cost_model", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha equity intraday NSE formula."),
        ("capital_policy", f"fixed_initial_capital_{int(INITIAL_CAPITAL_INR)}_inr_order_notional_{int(ORDER_NOTIONAL_INR)}_inr_cost200", "Annualized denominator is fixed capital."),
        ("acceptance_floor", "round_trips_ge_30;dates_ge_5;symbols_ge_3;positive_date_fraction_ge_0p60;annualized_ge_12_cost200;controls_not_dominant", "User profitability bar with breadth."),
        ("forbidden", "same_depth_curvature_rescue;catalyst_rescue;market_maker_rescue;supervised_ranker_retry;promotion;paper_live;deployable_profitability_claim", "Closed boundaries."),
        ("execution_results_generated_now", "0", "Precommit only."),
    ]
    frame = pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])
    frame.loc[len(frame)] = ("contract_hash", sha256_frame(frame), "Hash of frozen contract rows above.")
    return frame


def build_source_scorecard() -> pd.DataFrame:
    rows = [
        (SELECTED_SOURCE_ID, "cross_asset_external_proxy_plus_full_depth_confirmation", 1, 1, 1, "selected: lower turnover and external/cross-asset information source after Phase450"),
        ("another_depth_curvature_threshold", "none", 1, 0, 0, "rejected: Phase450 closed same-source rescue"),
        ("another_catalyst_continuation", "none", 1, 0, 0, "rejected: Phase447 holdout failed"),
        ("another_market_maker_cancel_race", "none", 1, 0, 0, "rejected: Phase407-409 already falsified attached charter"),
    ]
    return pd.DataFrame(rows, columns=["source_id", "material_new_axis", "uses_l2_l5_core", "low_turnover_or_external", "can_execute_next", "why_selected"])


def build_gates(phase450: pd.DataFrame, inputs: pd.DataFrame, scorecard: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    selected = scorecard[scorecard["source_id"].eq(SELECTED_SOURCE_ID)]
    forbidden = contract.loc[contract["contract_id"].eq("forbidden"), "contract_value"].astype(str).str.cat(sep=" ")
    gates = [
        ("P451_PHASE450_AVAILABLE", int(scalar(phase450, "phase450_depth_curvature_interpretation_complete", 0)) == 1, scalar(phase450, "phase450_depth_curvature_interpretation_complete", 0), 1),
        ("P451_NEXT_ACTION_MATCHED", "cross_asset_source_edge" in str(scalar(phase450, "phase450_next_best_action", "")) or "external" in str(scalar(phase450, "phase450_next_best_action", "")), scalar(phase450, "phase450_next_best_action", ""), "external_or_cross_asset"),
        ("P451_SELECTED_SOURCE_PRESENT", len(selected) == 1, len(selected), 1),
        ("P451_SELECTED_SOURCE_USES_L2_L5", int(selected["uses_l2_l5_core"].iloc[0]) == 1 if len(selected) else False, int(selected["uses_l2_l5_core"].iloc[0]) if len(selected) else "", 1),
        ("P451_SELECTED_SOURCE_LOW_TURNOVER_EXTERNAL", int(selected["low_turnover_or_external"].iloc[0]) == 1 if len(selected) else False, int(selected["low_turnover_or_external"].iloc[0]) if len(selected) else "", 1),
        ("P451_DENSE_ROOT_PRESENT", as_int(val(inputs, "dense_root_exists", 0)) == 1 and as_int(val(inputs, "dense_parquet_file_count", 0)) > 0, f"exists={val(inputs, 'dense_root_exists')};files={val(inputs, 'dense_parquet_file_count')}", "exists_and_files"),
        ("P451_REQUIRED_SYMBOLS_AVAILABLE", str(val(inputs, "missing_required_symbols", "")) == "", val(inputs, "missing_required_symbols", ""), "empty"),
        ("P451_REQUIRED_MONTHS_AVAILABLE", str(val(inputs, "missing_required_months", "")) == "", val(inputs, "missing_required_months", ""), "empty"),
        ("P451_COST200_FIXED_CAPITAL", "cost200" in contract.loc[contract["contract_id"].eq("capital_policy"), "contract_value"].astype(str).str.cat(sep=" "), contract.loc[contract["contract_id"].eq("capital_policy"), "contract_value"].astype(str).str.cat(sep=" "), "cost200_fixed_capital"),
        ("P451_RESULTS_NOT_GENERATED", contract.loc[contract["contract_id"].eq("execution_results_generated_now"), "contract_value"].astype(str).str.cat(sep=" ") == "0", contract.loc[contract["contract_id"].eq("execution_results_generated_now"), "contract_value"].astype(str).str.cat(sep=" "), 0),
        ("P451_BOUNDARIES_CLOSED", all(x in forbidden for x in ["promotion", "paper_live", "deployable_profitability_claim"]), forbidden, "closed"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase451_cross_asset_precommit_complete", 1, "Phase451 precommit completed"),
            ("phase451_thesis_id", THESIS_ID, "Frozen thesis/source precommit"),
            ("phase451_selected_source_id", SELECTED_SOURCE_ID, "Selected source"),
            ("phase451_execution_results_generated", 0, "Precommit only"),
            ("phase451_strategy_promotion_allowed", 0, "No promotion"),
            ("phase451_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase451_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase451_execution_allowed_next", int(hard_pass == hard_rows), "Whether Phase452 may execute"),
            ("phase451_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase451_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase451_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, prior: pd.DataFrame, scorecard: pd.DataFrame, inputs: pd.DataFrame, contract: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase451 Cross-Asset ETF Pressure Source Precommit",
        "",
        "Phase451 freezes a low-turnover external/cross-asset source after Phase450 closed the high-turnover depth-curvature route.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Prior Boundary",
        "",
        _markdown_table(prior),
        "",
        "## Source Scorecard",
        "",
        _markdown_table(scorecard),
        "",
        "## Input Registry",
        "",
        _markdown_table(inputs),
        "",
        "## Frozen Phase452 Contract",
        "",
        _markdown_table(contract),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase452 may execute only this cross-asset ETF pressure source. It may not rescue Phase449, catalyst continuation, market making or supervised-ranker routes.",
    ]
    (output_dir / "phase451_cross_asset_etf_pressure_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase450_dir: Path = DEFAULT_PHASE450_DIR, dense_root: Path = DEFAULT_DENSE_ROOT, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase450 = read_csv(phase450_dir / "phase450_acceptance_summary.csv")
    if phase450.empty:
        raise FileNotFoundError("Phase451 requires outputs/phase450/phase450_acceptance_summary.csv")
    prior = build_prior_boundary(phase450)
    scorecard = build_source_scorecard()
    inputs = build_input_registry(dense_root)
    contract = build_contract()
    gates = build_gates(phase450, inputs, scorecard, contract)
    acceptance = build_acceptance(gates)
    prior.to_csv(output_dir / "phase451_prior_boundary.csv", index=False)
    scorecard.to_csv(output_dir / "phase451_source_scorecard.csv", index=False)
    inputs.to_csv(output_dir / "phase451_input_registry.csv", index=False)
    contract.to_csv(output_dir / "phase451_frozen_phase452_contract.csv", index=False)
    gates.to_csv(output_dir / "phase451_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase451_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, prior, scorecard, inputs, contract, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase451_cross_asset_etf_pressure_precommit",
        **reproducibility_fields(
            artifact_id="phase451_cross_asset_etf_pressure_precommit",
            generated_utc=generated_utc,
            inputs={"phase450_acceptance_summary": str(phase450_dir / "phase450_acceptance_summary.csv"), "dense_root": str(dense_root)},
            parameters={"thesis_id": THESIS_ID, "selected_source_id": SELECTED_SOURCE_ID, "contract_hash": sha256_frame(contract)},
            outputs={"acceptance_summary": str(output_dir / "phase451_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase452_cross_asset_fixed_tick_horizon",
        ),
    }
    (output_dir / "phase451_cross_asset_etf_pressure_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase451 cross-asset ETF pressure precommit.")
    parser.add_argument("--phase450-dir", type=Path, default=DEFAULT_PHASE450_DIR)
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase450_dir, args.dense_root, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
