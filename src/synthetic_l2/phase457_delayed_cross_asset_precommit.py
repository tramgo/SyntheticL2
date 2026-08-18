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


DEFAULT_PHASE456_DIR = Path("outputs/phase456")
DEFAULT_DENSE_ROOT = Path("raw_synthetic_l2_dense_full_year")
DEFAULT_OUTPUT_DIR = Path("outputs/phase457")

THESIS_ID = "P457_DELAYED_INTRADAY_CROSS_ASSET_DISPLACEMENT_PRECOMMIT"
SELECTED_SOURCE_ID = "delayed_intraday_cross_asset_etf_displacement"
NEXT_ACTION = "run_phase458_delayed_intraday_cross_asset_displacement_no_paper_live"
REPAIR_ACTION = "repair_phase457_precommit_inputs"

ETF_PROXIES = ["NIFTYBEES", "BANKBEES", "ITBEES"]
TARGET_SYMBOLS = ["AXISBANK", "HDFCBANK", "ICICIBANK", "INFY", "HCLTECH", "TCS", "RELIANCE"]
MONTHS = ["2026-01", "2026-02", "2026-03"]
WINDOW_START_ROW = 5_000
ENTRY_INDEX = 20
HORIZON_TICKS = 240
GUARD_TICKS = 10
WINDOW_ROWS_PER_SYMBOL_DATE = ENTRY_INDEX + HORIZON_TICKS + GUARD_TICKS + 1
MAX_EVENTS_PER_TARGET_DATE = 1
INITIAL_CAPITAL_INR = 1_000_000.0
ORDER_NOTIONAL_INR = 100_000.0
COST_MULTIPLIER = 2.0


def sha256_frame(frame: pd.DataFrame) -> str:
    return hashlib.sha256(frame.to_csv(index=False, lineterminator="\n").encode("utf-8")).hexdigest()


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def build_input_registry(dense_root: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    symbols = ETF_PROXIES + TARGET_SYMBOLS
    selected = []
    for month in MONTHS:
        for symbol in symbols:
            path = dense_root / f"trade_month={month}" / f"symbol={symbol}" / "part-00000.parquet"
            selected.append({"trade_month": month, "symbol": symbol, "path": str(path), "exists": int(path.exists())})
    files = pd.DataFrame(selected)
    rows = [
        ("dense_root_exists", int(dense_root.exists()), "Dense root exists."),
        ("selected_file_rows", len(files), "Frozen selected file rows."),
        ("selected_files_present", int(files["exists"].sum()) if not files.empty else 0, "Selected files present."),
        ("months", ";".join(MONTHS), "Frozen months."),
        ("source_instruments", ";".join(ETF_PROXIES), "ETF/index proxies."),
        ("target_symbols", ";".join(TARGET_SYMBOLS), "Target symbols."),
        ("window_start_row", WINDOW_START_ROW, "Delayed intraday row offset; not first-window."),
        ("window_rows_per_symbol_date", WINDOW_ROWS_PER_SYMBOL_DATE, "Rows needed from each delayed window."),
        ("entry_index", ENTRY_INDEX, "Entry row within delayed window."),
        ("horizon_ticks", HORIZON_TICKS, "Fixed horizon."),
        ("guard_ticks", GUARD_TICKS, "Guard rows."),
    ]
    return pd.DataFrame(rows, columns=["input_id", "value", "description"]), files


def build_contract() -> pd.DataFrame:
    rows = [
        ("thesis_id", THESIS_ID, "Phase457 delayed timing-source precommit."),
        ("selected_source", SELECTED_SOURCE_ID, "Materially new timing/label source after Phase456."),
        ("material_difference", "delayed_intraday_window_not_first_window_cross_asset_pressure", "Changes timing/label source, not thresholds or side-rule tuning."),
        ("source_instruments", ";".join(ETF_PROXIES), "ETF/index-proxy source instruments."),
        ("target_symbols", ";".join(TARGET_SYMBOLS), "Frozen target basket."),
        ("months", ";".join(MONTHS), "Frozen bounded execution months."),
        ("window_start_row", str(WINDOW_START_ROW), "Start delayed contiguous window at this per-symbol/date row."),
        ("window_rows_per_symbol_date", str(WINDOW_ROWS_PER_SYMBOL_DATE), "Keep contiguous rows for entry plus horizon."),
        ("entry_index", str(ENTRY_INDEX), "Entry index within window."),
        ("horizon_ticks", str(HORIZON_TICKS), "Fixed exit horizon."),
        ("guard_ticks", str(GUARD_TICKS), "Guard ticks."),
        ("max_events_per_target_date", str(MAX_EVENTS_PER_TARGET_DATE), "Low-turnover cap."),
        ("side_rule", "long_when_delayed_etf_proxy_pressure_and_target_l2_l5_pressure_agree_short_when_opposite", "Frozen side rule."),
        ("controls_required", "source_time_shift;side_flip;target_only_l1_l5;etf_l1_only_ablation", "Required controls."),
        ("cost_model", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha equity intraday NSE formula."),
        ("cost_multiplier", str(COST_MULTIPLIER), "Cost200."),
        ("capital_policy", f"fixed_initial_capital_{int(INITIAL_CAPITAL_INR)}_inr_order_notional_{int(ORDER_NOTIONAL_INR)}_inr_cost200", "Fixed capital and notional."),
        ("acceptance_floor", "round_trips_ge_30;dates_ge_5;symbols_ge_3;positive_date_fraction_ge_0p60;annualized_ge_12_cost200;controls_not_dominant", "User profitability bar with breadth."),
        ("forbidden", "first_window_cross_asset_rescue;threshold_relaxation;side_rule_tuning;catalyst_rescue;market_maker_rescue;promotion;paper_live;deployable_profitability_claim", "Closed boundaries."),
        ("execution_results_generated_now", "0", "Precommit only."),
    ]
    frame = pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])
    frame.loc[len(frame)] = ("contract_hash", sha256_frame(frame), "Hash of frozen contract rows above.")
    return frame


def build_prior_boundary(phase456: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("P456", "first_window_cross_asset_etf_pressure", scalar(phase456, "phase456_selected_verdict", ""), "closed: first-window form produced zero gross edge and failed controls"),
        ("P455", "contiguous_first_window_execution", scalar(phase456, "phase456_same_form_rescue_allowed", ""), "same-form rescue not allowed"),
    ]
    return pd.DataFrame(rows, columns=["phase", "route", "verdict_or_status", "boundary"])


def val(inputs: pd.DataFrame, key: str, default: Any = "") -> Any:
    rows = inputs.loc[inputs["input_id"].eq(key), "value"].tolist()
    return rows[0] if rows else default


def cval(contract: pd.DataFrame, key: str, default: str = "") -> str:
    rows = contract.loc[contract["contract_id"].eq(key), "contract_value"].astype(str).tolist()
    return rows[0] if rows else default


def build_gates(phase456: pd.DataFrame, inputs: pd.DataFrame, files: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    forbidden = cval(contract, "forbidden")
    gates = [
        ("P457_PHASE456_AVAILABLE", as_int(scalar(phase456, "phase456_cross_asset_interpretation_complete", 0)) == 1, scalar(phase456, "phase456_cross_asset_interpretation_complete", 0), 1),
        ("P457_NEXT_ACTION_MATCHED", "material_new_timing" in str(scalar(phase456, "phase456_next_best_action", "")), scalar(phase456, "phase456_next_best_action", ""), "material_new_timing"),
        ("P457_NOT_FIRST_WINDOW", int(val(inputs, "window_start_row", 0)) > 0, val(inputs, "window_start_row", 0), ">0"),
        ("P457_CONTIGUOUS_WINDOW_FROZEN", int(cval(contract, "window_rows_per_symbol_date", "0")) >= ENTRY_INDEX + HORIZON_TICKS + 1, cval(contract, "window_rows_per_symbol_date"), f">={ENTRY_INDEX + HORIZON_TICKS + 1}"),
        ("P457_SELECTED_FILES_PRESENT", int(files["exists"].sum()) == len(files), int(files["exists"].sum()), len(files)),
        ("P457_LOW_TURNOVER_CAP_RETAINED", cval(contract, "max_events_per_target_date") == "1", cval(contract, "max_events_per_target_date"), 1),
        ("P457_COST200_FIXED_CAPITAL", "cost200" in cval(contract, "capital_policy"), cval(contract, "capital_policy"), "cost200_fixed_capital"),
        ("P457_CONTROLS_PRECOMMITTED", "source_time_shift" in cval(contract, "controls_required"), cval(contract, "controls_required"), "controls"),
        ("P457_RESULTS_NOT_GENERATED", cval(contract, "execution_results_generated_now") == "0", cval(contract, "execution_results_generated_now"), 0),
        ("P457_BOUNDARIES_CLOSED", all(x in forbidden for x in ["promotion", "paper_live", "deployable_profitability_claim"]), forbidden, "closed"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase457_delayed_cross_asset_precommit_complete", 1, "Phase457 precommit completed"),
            ("phase457_thesis_id", THESIS_ID, "Delayed timing-source thesis"),
            ("phase457_selected_source_id", SELECTED_SOURCE_ID, "Selected source"),
            ("phase457_execution_results_generated", 0, "Precommit only"),
            ("phase457_strategy_promotion_allowed", 0, "No promotion"),
            ("phase457_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase457_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase457_execution_allowed_next", int(hard_pass == hard_rows), "Whether Phase458 may execute"),
            ("phase457_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase457_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase457_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, prior: pd.DataFrame, inputs: pd.DataFrame, files: pd.DataFrame, contract: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase457 Delayed Intraday Cross-Asset Displacement Precommit",
        "",
        "Phase457 freezes a materially new timing/label source after Phase456 closed the first-window cross-asset form.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Prior Boundary",
        "",
        _markdown_table(prior),
        "",
        "## Input Registry",
        "",
        _markdown_table(inputs),
        "",
        "## Selected Files",
        "",
        _markdown_table(files),
        "",
        "## Frozen Phase458 Contract",
        "",
        _markdown_table(contract),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: commit this precommit before Phase458 generates delayed-window trades or P&L.",
    ]
    (output_dir / "phase457_delayed_cross_asset_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase456_dir: Path = DEFAULT_PHASE456_DIR, dense_root: Path = DEFAULT_DENSE_ROOT, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase456 = read_csv(phase456_dir / "phase456_acceptance_summary.csv")
    if phase456.empty:
        raise FileNotFoundError("Phase457 requires Phase456 acceptance.")
    prior = build_prior_boundary(phase456)
    inputs, files = build_input_registry(dense_root)
    contract = build_contract()
    gates = build_gates(phase456, inputs, files, contract)
    acceptance = build_acceptance(gates)
    prior.to_csv(output_dir / "phase457_prior_boundary.csv", index=False)
    inputs.to_csv(output_dir / "phase457_input_registry.csv", index=False)
    files.to_csv(output_dir / "phase457_selected_files.csv", index=False)
    contract.to_csv(output_dir / "phase457_frozen_phase458_contract.csv", index=False)
    gates.to_csv(output_dir / "phase457_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase457_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, prior, inputs, files, contract, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase457_delayed_cross_asset_precommit",
        **reproducibility_fields(
            artifact_id="phase457_delayed_cross_asset_precommit",
            generated_utc=generated_utc,
            inputs={"phase456_acceptance_summary": str(phase456_dir / "phase456_acceptance_summary.csv"), "dense_root": str(dense_root)},
            parameters={"thesis_id": THESIS_ID, "contract_hash": sha256_frame(contract)},
            outputs={"acceptance_summary": str(output_dir / "phase457_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase458_delayed_contiguous_tick_window",
        ),
    }
    (output_dir / "phase457_delayed_cross_asset_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase457 delayed cross-asset precommit.")
    parser.add_argument("--phase456-dir", type=Path, default=DEFAULT_PHASE456_DIR)
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase456_dir, args.dense_root, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
