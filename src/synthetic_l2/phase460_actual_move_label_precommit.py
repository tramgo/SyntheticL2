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


DEFAULT_PHASE459_DIR = Path("outputs/phase459")
DEFAULT_DENSE_ROOT = Path("raw_synthetic_l2_dense_full_year")
DEFAULT_OUTPUT_DIR = Path("outputs/phase460")

THESIS_ID = "P460_ACTUAL_MOVE_CANDIDATE_LABEL_SOURCE_PRECOMMIT"
SELECTED_SOURCE_ID = "actual_move_candidate_labels_for_past_only_l2_feature_learning"
NEXT_ACTION = "run_phase461_actual_move_candidate_label_materialization_no_pnl"
REPAIR_ACTION = "repair_phase460_precommit_inputs"

TARGET_SYMBOLS = ["AXISBANK", "HDFCBANK", "ICICIBANK", "INFY", "HCLTECH", "TCS", "RELIANCE"]
MONTHS = ["2026-01", "2026-02", "2026-03"]
WINDOW_START_ROWS = [0, 5_000, 10_000, 20_000, 50_000]
FEATURE_LOOKBACK_TICKS = 20
ENTRY_INDEX = 20
HORIZON_TICKS = 240
WINDOW_ROWS_PER_SYMBOL_DATE = max(WINDOW_START_ROWS) + ENTRY_INDEX + HORIZON_TICKS + 1
MIN_ABS_FORWARD_MOVE_BPS = 2.0
INITIAL_CAPITAL_INR = 1_000_000.0
ORDER_NOTIONAL_INR = 100_000.0
COST_MULTIPLIER = 2.0


def sha256_frame(frame: pd.DataFrame) -> str:
    return hashlib.sha256(frame.to_csv(index=False, lineterminator="\n").encode("utf-8")).hexdigest()


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def build_prior_boundary(phase459: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("P459", "delayed_fixed_window_cross_asset", scalar(phase459, "phase459_selected_verdict", ""), "closed; next action requires actual move-candidate label source or pausing fixed-window routes"),
        ("P458", "fixed_row_5000_windows", "zero_gross_edge", "do not tune row offsets after result"),
        ("P455", "first_window_cross_asset", "zero_gross_edge", "do not tune first-window thresholds or side rules"),
    ]
    return pd.DataFrame(rows, columns=["phase", "route", "verdict_or_status", "boundary"])


def build_input_registry(dense_root: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    files = []
    for month in MONTHS:
        for symbol in TARGET_SYMBOLS:
            path = dense_root / f"trade_month={month}" / f"symbol={symbol}" / "part-00000.parquet"
            files.append({"trade_month": month, "symbol": symbol, "path": str(path), "exists": int(path.exists())})
    file_frame = pd.DataFrame(files)
    rows = [
        ("dense_root_exists", int(dense_root.exists()), "Dense raw L1-L5 root exists."),
        ("selected_file_rows", len(file_frame), "Frozen selected file rows."),
        ("selected_files_present", int(file_frame["exists"].sum()) if not file_frame.empty else 0, "Selected files present."),
        ("months", ";".join(MONTHS), "Frozen months."),
        ("target_symbols", ";".join(TARGET_SYMBOLS), "Frozen target symbols."),
        ("window_start_rows", ";".join(str(x) for x in WINDOW_START_ROWS), "Frozen candidate offsets per symbol/date."),
        ("feature_lookback_ticks", FEATURE_LOOKBACK_TICKS, "Past-only feature lookback."),
        ("entry_index", ENTRY_INDEX, "Entry index after feature window."),
        ("horizon_ticks", HORIZON_TICKS, "Forward label horizon."),
        ("min_abs_forward_move_bps", MIN_ABS_FORWARD_MOVE_BPS, "Actual non-flat move label floor."),
    ]
    return pd.DataFrame(rows, columns=["input_id", "value", "description"]), file_frame


def build_contract() -> pd.DataFrame:
    rows = [
        ("thesis_id", THESIS_ID, "Phase460 actual-move label-source precommit."),
        ("selected_source", SELECTED_SOURCE_ID, "Materially new label source after fixed-window failures."),
        ("material_difference", "candidate_selection_by_actual_forward_move_labels_not_fixed_clock_windows", "A label dataset source, not a tradable signal by itself."),
        ("target_symbols", ";".join(TARGET_SYMBOLS), "Frozen target symbols."),
        ("months", ";".join(MONTHS), "Frozen months."),
        ("window_start_rows", ";".join(str(x) for x in WINDOW_START_ROWS), "Frozen candidate offsets to inspect."),
        ("feature_lookback_ticks", str(FEATURE_LOOKBACK_TICKS), "All features must end before entry tick."),
        ("entry_index", str(ENTRY_INDEX), "Entry tick index inside candidate window."),
        ("horizon_ticks", str(HORIZON_TICKS), "Forward return label horizon."),
        ("min_abs_forward_move_bps", str(MIN_ABS_FORWARD_MOVE_BPS), "Minimum non-flat forward move for positive/negative label inclusion."),
        ("primary_features", "past_only_L1_L5_spread_imbalance_depth_shape_churn_and_recent_mid_return", "L1-L5 features available for later fit."),
        ("label_columns", "forward_return_bps;label_side;abs_forward_return_bps;move_candidate", "Label columns to materialize."),
        ("allowed_outputs", "label_ledger;feature_label_summary;gate_evaluation;manifest;report", "No trading P&L output in Phase461."),
        ("forbidden", "strategy_pnl;paper_live;deployable_profitability_claim;future_label_as_signal;threshold_tuning_after_label_result", "Closed boundaries."),
        ("cost_model_reference", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Kept for downstream replay but not charged in label materialization."),
        ("capital_policy_reference", f"fixed_initial_capital_{int(INITIAL_CAPITAL_INR)}_inr_order_notional_{int(ORDER_NOTIONAL_INR)}_inr_cost200", "Downstream replay denominator remains fixed."),
        ("execution_results_generated_now", "0", "Precommit only."),
    ]
    frame = pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])
    frame.loc[len(frame)] = ("contract_hash", sha256_frame(frame), "Hash of frozen contract rows above.")
    return frame


def val(inputs: pd.DataFrame, key: str, default: Any = "") -> Any:
    rows = inputs.loc[inputs["input_id"].eq(key), "value"].tolist()
    return rows[0] if rows else default


def cval(contract: pd.DataFrame, key: str, default: str = "") -> str:
    rows = contract.loc[contract["contract_id"].eq(key), "contract_value"].astype(str).tolist()
    return rows[0] if rows else default


def build_gates(phase459: pd.DataFrame, inputs: pd.DataFrame, files: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    forbidden = cval(contract, "forbidden")
    gates = [
        ("P460_PHASE459_AVAILABLE", as_int(scalar(phase459, "phase459_delayed_cross_asset_interpretation_complete", 0)) == 1, scalar(phase459, "phase459_delayed_cross_asset_interpretation_complete", 0), 1),
        ("P460_NEXT_ACTION_MATCHED", "actual_move_candidate_label_source" in str(scalar(phase459, "phase459_next_best_action", "")), scalar(phase459, "phase459_next_best_action", ""), "actual_move_candidate_label_source"),
        ("P460_DENSE_ROOT_PRESENT", as_int(val(inputs, "dense_root_exists", 0)) == 1, val(inputs, "dense_root_exists", 0), 1),
        ("P460_SELECTED_FILES_PRESENT", int(files["exists"].sum()) == len(files), int(files["exists"].sum()), len(files)),
        ("P460_MULTIPLE_OFFSETS_FROZEN", len(WINDOW_START_ROWS) >= 3, len(WINDOW_START_ROWS), ">=3"),
        ("P460_LABEL_SOURCE_NOT_TRADABLE_SIGNAL", "future_label_as_signal" in forbidden, forbidden, "future_label_as_signal_forbidden"),
        ("P460_PAST_ONLY_FEATURES_PRECOMMITTED", "past_only" in cval(contract, "primary_features"), cval(contract, "primary_features"), "past_only"),
        ("P460_NO_PNL_OUTPUTS", "strategy_pnl" in forbidden and "strategy_pnl" not in cval(contract, "allowed_outputs"), cval(contract, "allowed_outputs"), "no_strategy_pnl"),
        ("P460_RESULTS_NOT_GENERATED", cval(contract, "execution_results_generated_now") == "0", cval(contract, "execution_results_generated_now"), 0),
        ("P460_BOUNDARIES_CLOSED", all(x in forbidden for x in ["paper_live", "deployable_profitability_claim"]), forbidden, "closed"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase460_actual_move_label_precommit_complete", 1, "Phase460 precommit completed"),
            ("phase460_thesis_id", THESIS_ID, "Actual-move label-source thesis"),
            ("phase460_selected_source_id", SELECTED_SOURCE_ID, "Selected label source"),
            ("phase460_execution_results_generated", 0, "Precommit only"),
            ("phase460_strategy_promotion_allowed", 0, "No promotion"),
            ("phase460_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase460_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase460_phase461_allowed_next", int(hard_pass == hard_rows), "Whether Phase461 may materialize labels"),
            ("phase460_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase460_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase460_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, prior: pd.DataFrame, inputs: pd.DataFrame, files: pd.DataFrame, contract: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase460 Actual-Move Candidate Label Source Precommit",
        "",
        "Phase460 freezes an actual non-flat move-candidate label source after fixed-window routes produced zero gross edge.",
        "",
        "Important boundary: actual forward movement is a label source for research, not a tradable signal available at order time.",
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
        "## Frozen Phase461 Contract",
        "",
        _markdown_table(contract),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: commit this precommit before Phase461 materializes labels. Phase461 must not emit P&L or acceptance as a strategy.",
    ]
    (output_dir / "phase460_actual_move_label_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase459_dir: Path = DEFAULT_PHASE459_DIR, dense_root: Path = DEFAULT_DENSE_ROOT, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase459 = read_csv(phase459_dir / "phase459_acceptance_summary.csv")
    if phase459.empty:
        raise FileNotFoundError("Phase460 requires Phase459 acceptance.")
    prior = build_prior_boundary(phase459)
    inputs, files = build_input_registry(dense_root)
    contract = build_contract()
    gates = build_gates(phase459, inputs, files, contract)
    acceptance = build_acceptance(gates)
    prior.to_csv(output_dir / "phase460_prior_boundary.csv", index=False)
    inputs.to_csv(output_dir / "phase460_input_registry.csv", index=False)
    files.to_csv(output_dir / "phase460_selected_files.csv", index=False)
    contract.to_csv(output_dir / "phase460_frozen_phase461_contract.csv", index=False)
    gates.to_csv(output_dir / "phase460_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase460_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, prior, inputs, files, contract, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase460_actual_move_label_precommit",
        **reproducibility_fields(
            artifact_id="phase460_actual_move_label_precommit",
            generated_utc=generated_utc,
            inputs={"phase459_acceptance_summary": str(phase459_dir / "phase459_acceptance_summary.csv"), "dense_root": str(dense_root)},
            parameters={"thesis_id": THESIS_ID, "contract_hash": sha256_frame(contract)},
            outputs={"acceptance_summary": str(output_dir / "phase460_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase461_label_materialization_only",
        ),
    }
    (output_dir / "phase460_actual_move_label_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase460 actual-move label precommit.")
    parser.add_argument("--phase459-dir", type=Path, default=DEFAULT_PHASE459_DIR)
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase459_dir, args.dense_root, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
