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


DEFAULT_PHASE453_DIR = Path("outputs/phase453")
DEFAULT_PHASE451_DIR = Path("outputs/phase451")
DEFAULT_DENSE_ROOT = Path("raw_synthetic_l2_dense_full_year")
DEFAULT_OUTPUT_DIR = Path("outputs/phase454")

THESIS_ID = "P454_CONTIGUOUS_TICK_WINDOW_CROSS_ASSET_ETF_PRESSURE_PRECOMMIT"
NEXT_ACTION = "run_phase455_contiguous_cross_asset_etf_pressure_no_paper_live"
REPAIR_ACTION = "repair_phase454_precommit_inputs"

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


def cval(contract: pd.DataFrame, key: str, default: str = "") -> str:
    rows = contract.loc[contract["contract_id"].astype(str).eq(key), "contract_value"].astype(str).tolist()
    return rows[0] if rows else default


def slist(value: str) -> list[str]:
    return [x.strip() for x in str(value).split(";") if x.strip()]


def build_input_registry(phase451_contract: pd.DataFrame, dense_root: Path) -> pd.DataFrame:
    months = slist(cval(phase451_contract, "months"))
    symbols = slist(cval(phase451_contract, "source_instruments")) + slist(cval(phase451_contract, "target_symbols"))
    selected = []
    for month in months:
        for symbol in symbols:
            path = dense_root / f"trade_month={month}" / f"symbol={symbol}" / "part-00000.parquet"
            selected.append({"trade_month": month, "symbol": symbol, "path": str(path), "exists": int(path.exists())})
    files = pd.DataFrame(selected)
    rows = [
        ("phase451_contract_available", int(not phase451_contract.empty), "Prior source/target/month contract available."),
        ("dense_root_exists", int(dense_root.exists()), "Dense root exists."),
        ("selected_file_rows", len(files), "Frozen file rows."),
        ("selected_files_present", int(files["exists"].sum()) if not files.empty else 0, "Selected files present."),
        ("months", ";".join(months), "Frozen months inherited from Phase451."),
        ("symbols", ";".join(symbols), "Frozen source plus target symbols inherited from Phase451."),
        ("window_rows_per_symbol_date", WINDOW_ROWS_PER_SYMBOL_DATE, "Contiguous rows required per symbol/date."),
        ("entry_index", ENTRY_INDEX, "Frozen entry index."),
        ("horizon_ticks", HORIZON_TICKS, "Frozen horizon."),
        ("guard_ticks", GUARD_TICKS, "Frozen guard."),
    ]
    return pd.DataFrame(rows, columns=["input_id", "value", "description"]), files


def build_contract(phase451_contract: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("thesis_id", THESIS_ID, "Phase454 repaired access precommit."),
        ("repair_type", "contiguous_raw_tick_window_access", "Repairs Phase452 sparse-stride access failure."),
        ("source_instruments", cval(phase451_contract, "source_instruments"), "Keep Phase451 ETF proxies."),
        ("target_symbols", cval(phase451_contract, "target_symbols"), "Keep Phase451 targets."),
        ("months", cval(phase451_contract, "months"), "Keep Phase451 months."),
        ("entry_index", str(ENTRY_INDEX), "Keep Phase452 event index."),
        ("horizon_ticks", str(HORIZON_TICKS), "Keep Phase451 horizon."),
        ("guard_ticks", str(GUARD_TICKS), "Guard rows beyond horizon."),
        ("window_rows_per_symbol_date", str(WINDOW_ROWS_PER_SYMBOL_DATE), "Minimum contiguous rows per symbol/date."),
        ("max_events_per_target_date", str(MAX_EVENTS_PER_TARGET_DATE), "Keep low-turnover cap."),
        ("side_rule", "unchanged_from_phase451_cross_asset_etf_pressure", "No signal/side rescue after Phase452."),
        ("controls_required", cval(phase451_contract, "controls_required"), "Keep Phase451 controls."),
        ("cost_model", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha cost model."),
        ("cost_multiplier", str(COST_MULTIPLIER), "Cost200."),
        ("capital_policy", f"fixed_initial_capital_{int(INITIAL_CAPITAL_INR)}_inr_order_notional_{int(ORDER_NOTIONAL_INR)}_inr_cost200", "Fixed capital and notional."),
        ("acceptance_floor", cval(phase451_contract, "acceptance_floor"), "Keep Phase451 acceptance floor."),
        ("forbidden", "threshold_relaxation;side_rule_change;source_universe_change;catalyst_rescue;market_maker_rescue;promotion;paper_live;deployable_profitability_claim", "Closed boundaries."),
        ("execution_results_generated_now", "0", "Precommit only."),
    ]
    frame = pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])
    frame.loc[len(frame)] = ("contract_hash", sha256_frame(frame), "Hash of frozen repair contract rows above.")
    return frame


def build_gates(phase453: pd.DataFrame, inputs: pd.DataFrame, files: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    forbidden = contract.loc[contract["contract_id"].eq("forbidden"), "contract_value"].astype(str).str.cat(sep=" ")
    gates = [
        ("P454_PHASE453_AVAILABLE", as_int(scalar(phase453, "phase453_cross_asset_interpretation_complete", 0)) == 1, scalar(phase453, "phase453_cross_asset_interpretation_complete", 0), 1),
        ("P454_REPAIR_NEXT_ACTION_MATCHED", "contiguous" in str(scalar(phase453, "phase453_next_best_action", "")), scalar(phase453, "phase453_next_best_action", ""), "contiguous_repair"),
        ("P454_SOURCE_NOT_CLOSED", as_int(scalar(phase453, "phase453_cross_asset_source_closed", 1)) == 0, scalar(phase453, "phase453_cross_asset_source_closed", 1), 0),
        ("P454_STRIDE_CONTRACT_CLOSED", as_int(scalar(phase453, "phase453_stride_contract_closed", 0)) == 1, scalar(phase453, "phase453_stride_contract_closed", 0), 1),
        ("P454_CONTIGUOUS_WINDOW_FROZEN", int(cval(contract, "window_rows_per_symbol_date", "0")) >= ENTRY_INDEX + HORIZON_TICKS + 1, cval(contract, "window_rows_per_symbol_date"), f">={ENTRY_INDEX + HORIZON_TICKS + 1}"),
        ("P454_SELECTED_FILES_PRESENT", int(files["exists"].sum()) == len(files), int(files["exists"].sum()), len(files)),
        ("P454_NO_SIGNAL_OR_SIDE_CHANGE", cval(contract, "side_rule") == "unchanged_from_phase451_cross_asset_etf_pressure", cval(contract, "side_rule"), "unchanged"),
        ("P454_LOW_TURNOVER_CAP_RETAINED", cval(contract, "max_events_per_target_date") == str(MAX_EVENTS_PER_TARGET_DATE), cval(contract, "max_events_per_target_date"), MAX_EVENTS_PER_TARGET_DATE),
        ("P454_COST200_FIXED_CAPITAL", "cost200" in cval(contract, "capital_policy"), cval(contract, "capital_policy"), "cost200_fixed_capital"),
        ("P454_RESULTS_NOT_GENERATED", cval(contract, "execution_results_generated_now") == "0", cval(contract, "execution_results_generated_now"), 0),
        ("P454_BOUNDARIES_CLOSED", all(x in forbidden for x in ["promotion", "paper_live", "deployable_profitability_claim"]), forbidden, "closed"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase454_contiguous_precommit_complete", 1, "Phase454 precommit completed"),
            ("phase454_thesis_id", THESIS_ID, "Repaired execution-access thesis"),
            ("phase454_window_rows_per_symbol_date", WINDOW_ROWS_PER_SYMBOL_DATE, "Contiguous rows per symbol/date"),
            ("phase454_execution_results_generated", 0, "Precommit only"),
            ("phase454_strategy_promotion_allowed", 0, "No promotion"),
            ("phase454_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase454_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase454_execution_allowed_next", int(hard_pass == hard_rows), "Whether Phase455 may execute"),
            ("phase454_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase454_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase454_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, inputs: pd.DataFrame, files: pd.DataFrame, contract: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase454 Contiguous Tick-Window Cross-Asset ETF Pressure Precommit",
        "",
        "Phase454 repairs only the Phase452 data-access mismatch by freezing contiguous raw tick windows per symbol/date. It does not change the Phase451 signal source or side rule.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Input Registry",
        "",
        _markdown_table(inputs),
        "",
        "## Selected Files",
        "",
        _markdown_table(files),
        "",
        "## Frozen Phase455 Contract",
        "",
        _markdown_table(contract),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: commit this precommit before Phase455 generates any trades or P&L.",
    ]
    (output_dir / "phase454_contiguous_cross_asset_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase453_dir: Path = DEFAULT_PHASE453_DIR, phase451_dir: Path = DEFAULT_PHASE451_DIR, dense_root: Path = DEFAULT_DENSE_ROOT, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase453 = read_csv(phase453_dir / "phase453_acceptance_summary.csv")
    phase451_contract = read_csv(phase451_dir / "phase451_frozen_phase452_contract.csv")
    if phase453.empty or phase451_contract.empty:
        raise FileNotFoundError("Phase454 requires Phase453 acceptance and Phase451 frozen contract.")
    inputs, files = build_input_registry(phase451_contract, dense_root)
    contract = build_contract(phase451_contract)
    gates = build_gates(phase453, inputs, files, contract)
    acceptance = build_acceptance(gates)
    inputs.to_csv(output_dir / "phase454_input_registry.csv", index=False)
    files.to_csv(output_dir / "phase454_selected_files.csv", index=False)
    contract.to_csv(output_dir / "phase454_frozen_phase455_contract.csv", index=False)
    gates.to_csv(output_dir / "phase454_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase454_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, inputs, files, contract, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase454_contiguous_cross_asset_precommit",
        **reproducibility_fields(
            artifact_id="phase454_contiguous_cross_asset_precommit",
            generated_utc=generated_utc,
            inputs={"phase453_acceptance_summary": str(phase453_dir / "phase453_acceptance_summary.csv"), "phase451_contract": str(phase451_dir / "phase451_frozen_phase452_contract.csv"), "dense_root": str(dense_root)},
            parameters={"thesis_id": THESIS_ID, "contract_hash": sha256_frame(contract)},
            outputs={"acceptance_summary": str(output_dir / "phase454_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase455_contiguous_tick_window",
        ),
    }
    (output_dir / "phase454_contiguous_cross_asset_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase454 contiguous cross-asset precommit.")
    parser.add_argument("--phase453-dir", type=Path, default=DEFAULT_PHASE453_DIR)
    parser.add_argument("--phase451-dir", type=Path, default=DEFAULT_PHASE451_DIR)
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase453_dir, args.phase451_dir, args.dense_root, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
