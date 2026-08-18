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


DEFAULT_PHASE461_DIR = Path("outputs/phase461")
DEFAULT_PHASE162_DIR = Path("outputs/phase162")
DEFAULT_DISTRIBUTIONAL_ROOT = Path("raw_synthetic_l2_phase162_distributional_full_year")
DEFAULT_PROFILE_ID = "P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE"
DEFAULT_OUTPUT_DIR = Path("outputs/phase462")

THESIS_ID = "P462_DISTRIBUTIONAL_LABEL_SOURCE_REPLACEMENT_PRECOMMIT"
SELECTED_SOURCE_ID = "phase162_p159_distributional_full_year_l1_l5_replacement_for_flat_phase461_source"
NEXT_ACTION = "run_phase463_actual_move_label_materialization_on_phase162_distributional_l1_l5_no_pnl"

TARGET_SYMBOLS = ["AXISBANK", "HDFCBANK", "ICICIBANK", "INFY", "HCLTECH", "TCS", "RELIANCE"]
MONTHS = ["2026-01", "2026-02", "2026-03"]
WINDOW_START_ROWS = [0, 5000, 10000, 20000, 50000]
ENTRY_INDEX = 20
HORIZON_TICKS = 240
MIN_ABS_FORWARD_MOVE_BPS = 2.0


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def hash_frame(frame: pd.DataFrame) -> str:
    payload = frame.to_json(orient="records", date_format="iso")
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def profile_root(root: Path, profile_id: str) -> Path:
    return root / f"profile={profile_id}"


def selected_files(root: Path, profile_id: str) -> pd.DataFrame:
    base = profile_root(root, profile_id)
    rows = []
    for month in MONTHS:
        for symbol in TARGET_SYMBOLS:
            path = base / f"trade_month={month}" / f"symbol={symbol}" / "part-00000.parquet"
            rows.append(
                {
                    "trade_month": month,
                    "symbol": symbol,
                    "profile_id": profile_id,
                    "path": str(path),
                    "exists": int(path.exists()),
                    "bytes": int(path.stat().st_size) if path.exists() else 0,
                }
            )
    return pd.DataFrame(rows)


def build_contract(selected: pd.DataFrame) -> pd.DataFrame:
    contract_rows = [
        ("phase462_thesis_id", THESIS_ID, "Precommit thesis"),
        ("selected_source_id", SELECTED_SOURCE_ID, "Replacement label source"),
        ("prior_flat_source_root", "raw_synthetic_l2_dense_full_year", "Phase461 source that produced zero non-flat labels"),
        ("replacement_dense_root", str(DEFAULT_DISTRIBUTIONAL_ROOT), "Distributional full-year dense root"),
        ("replacement_profile_id", DEFAULT_PROFILE_ID, "Distributional profile"),
        ("target_symbols", ";".join(TARGET_SYMBOLS), "Target symbols"),
        ("months", ";".join(MONTHS), "Target months"),
        ("window_start_rows", ";".join(str(x) for x in WINDOW_START_ROWS), "Candidate start rows"),
        ("entry_index", ENTRY_INDEX, "Entry row inside each candidate window"),
        ("horizon_ticks", HORIZON_TICKS, "Forward label horizon"),
        ("min_abs_forward_move_bps", MIN_ABS_FORWARD_MOVE_BPS, "Actual-move floor"),
        ("selected_file_count", int(len(selected)), "Frozen replacement file count"),
        ("selected_file_hash", hash_frame(selected), "Hash of replacement file registry"),
        ("phase463_allowed_next", 1, "Allows label materialization only"),
        ("strategy_pnl_allowed", 0, "No P&L in Phase462 or Phase463 label materialization"),
        ("strategy_promotion_allowed", 0, "No promotion"),
        ("paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("deployable_profitability_claim_allowed", 0, "No deployable claim"),
    ]
    return pd.DataFrame(contract_rows, columns=["contract_id", "contract_value", "description"])


def build_input_evidence(phase461: pd.DataFrame, phase162: pd.DataFrame, selected: pd.DataFrame) -> pd.DataFrame:
    root = profile_root(DEFAULT_DISTRIBUTIONAL_ROOT, DEFAULT_PROFILE_ID)
    rows = [
        ("phase461_next_action", scalar(phase461, "phase461_next_best_action", ""), "Phase461 requested repair/replacement after flat labels"),
        ("phase461_move_candidate_rows", scalar(phase461, "phase461_move_candidate_rows", 0), "Flat-source move candidates"),
        ("phase461_long_label_rows", scalar(phase461, "phase461_long_label_rows", 0), "Flat-source long labels"),
        ("phase461_short_label_rows", scalar(phase461, "phase461_short_label_rows", 0), "Flat-source short labels"),
        ("phase162_profile_id", scalar(phase162, "phase162_profile_id", ""), "Distributional profile evidence"),
        ("phase162_months_materialized", scalar(phase162, "phase162_months_materialized", 0), "Materialized months"),
        ("phase162_symbols_materialized", scalar(phase162, "phase162_symbols_materialized", 0), "Materialized symbols"),
        ("phase162_partition_files", scalar(phase162, "phase162_partition_files", 0), "Distributional partition files"),
        ("phase162_expected_partition_files", scalar(phase162, "phase162_expected_partition_files", 0), "Expected partition files"),
        ("phase162_missing_partition_files", scalar(phase162, "phase162_missing_partition_files", 0), "Missing partition files"),
        ("phase162_full_year_realism_audit_pass", scalar(phase162, "phase162_full_year_realism_audit_pass", 0), "Realism audit pass"),
        ("phase162_strategy_replay_allowed", scalar(phase162, "phase162_strategy_replay_allowed", 1), "Replay remained closed in Phase162"),
        ("replacement_profile_root_exists", int(root.exists()), "Replacement profile root"),
        ("selected_files_present", int(selected["exists"].sum()), "Selected replacement files present"),
        ("selected_files_expected", int(len(selected)), "Selected replacement files expected"),
        ("selected_files_bytes", int(selected["bytes"].sum()), "Selected replacement bytes"),
    ]
    return pd.DataFrame(rows, columns=["evidence_id", "observed_value", "description"])


def build_gates(phase461: pd.DataFrame, phase162: pd.DataFrame, selected: pd.DataFrame) -> pd.DataFrame:
    root = profile_root(DEFAULT_DISTRIBUTIONAL_ROOT, DEFAULT_PROFILE_ID)
    gates = [
        (
            "P462_PHASE461_REPAIR_REQUESTED",
            str(scalar(phase461, "phase461_next_best_action", "")).startswith("pause_or_repair_synthetic_generator"),
            scalar(phase461, "phase461_next_best_action", ""),
            "repair_or_replace_after_flat_labels",
        ),
        ("P462_PHASE461_ZERO_MOVE_CANDIDATES_CONFIRMED", as_int(scalar(phase461, "phase461_move_candidate_rows", 1)) == 0, scalar(phase461, "phase461_move_candidate_rows", ""), 0),
        ("P462_PHASE162_DISTRIBUTIONAL_PROFILE_SELECTED", scalar(phase162, "phase162_profile_id", "") == DEFAULT_PROFILE_ID, scalar(phase162, "phase162_profile_id", ""), DEFAULT_PROFILE_ID),
        ("P462_PHASE162_FULL_YEAR_SCOPE_COMPLETE", as_int(scalar(phase162, "phase162_months_materialized", 0)) >= 12 and as_int(scalar(phase162, "phase162_symbols_materialized", 0)) >= 32, f"months={scalar(phase162, 'phase162_months_materialized', 0)};symbols={scalar(phase162, 'phase162_symbols_materialized', 0)}", "months>=12;symbols>=32"),
        ("P462_PHASE162_NO_MISSING_PARTITIONS", as_int(scalar(phase162, "phase162_missing_partition_files", 1)) == 0, scalar(phase162, "phase162_missing_partition_files", ""), 0),
        ("P462_PHASE162_REALISM_AUDIT_PASSED", as_int(scalar(phase162, "phase162_full_year_realism_audit_pass", 0)) == 1, scalar(phase162, "phase162_full_year_realism_audit_pass", ""), 1),
        ("P462_PHASE162_REPLAY_WAS_CLOSED", as_int(scalar(phase162, "phase162_strategy_replay_allowed", 1)) == 0, scalar(phase162, "phase162_strategy_replay_allowed", ""), 0),
        ("P462_REPLACEMENT_PROFILE_ROOT_PRESENT", root.exists(), str(root), "exists"),
        ("P462_SELECTED_FILES_PRESENT", int(selected["exists"].sum()) == len(selected), int(selected["exists"].sum()), len(selected)),
        ("P462_LABEL_ONLY_NEXT", True, NEXT_ACTION, "label_materialization_only"),
        ("P462_NO_STRATEGY_PNL", True, "precommit_only", "no_pnl"),
        ("P462_NO_PAPER_LIVE_OR_CLAIM", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(gates: pd.DataFrame, selected: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    all_pass = int(hard_pass == hard_rows)
    rows = [
        ("phase462_distributional_label_source_replacement_precommit_complete", 1, "Phase462 precommit completed"),
        ("phase462_thesis_id", THESIS_ID, "Precommit thesis"),
        ("phase462_selected_source_id", SELECTED_SOURCE_ID, "Selected replacement source"),
        ("phase462_replacement_profile_id", DEFAULT_PROFILE_ID, "Replacement profile"),
        ("phase462_replacement_selected_files", int(len(selected)), "Frozen selected files"),
        ("phase462_replacement_files_present", int(selected["exists"].sum()), "Present files"),
        ("phase462_execution_results_generated", 0, "Precommit only"),
        ("phase462_strategy_pnl_generated", 0, "No strategy P&L"),
        ("phase462_strategy_promotion_allowed", 0, "No promotion"),
        ("phase462_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase462_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase462_phase463_allowed_next", all_pass, "Allows Phase463 label materialization only if all gates pass"),
        ("phase462_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase462_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase462_next_best_action", NEXT_ACTION if all_pass else "repair_phase162_distributional_source_availability_before_label_materialization", "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, evidence: pd.DataFrame, contract: pd.DataFrame, selected: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase462 Distributional Label-Source Replacement Precommit",
        "",
        "Phase462 responds to Phase461's flat-label finding by freezing a replacement label source: the Phase162/P159 distributional full-year L1-L5 lake. It does not run strategy P&L.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Input Evidence",
        "",
        _markdown_table(evidence),
        "",
        "## Frozen Phase463 Contract",
        "",
        _markdown_table(contract),
        "",
        "## Selected Replacement Files",
        "",
        _markdown_table(selected),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase463 may materialize actual-move labels from the replacement source only. Strategy replay, promotion, paper/live and deployable profitability claims remain closed.",
    ]
    (output_dir / "phase462_distributional_label_source_replacement_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase461_dir: Path = DEFAULT_PHASE461_DIR, phase162_dir: Path = DEFAULT_PHASE162_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase461 = read_csv(phase461_dir / "phase461_acceptance_summary.csv")
    phase162 = read_csv(phase162_dir / "phase162_full_year_materialization_acceptance_summary.csv")
    selected = selected_files(DEFAULT_DISTRIBUTIONAL_ROOT, DEFAULT_PROFILE_ID)
    contract = build_contract(selected)
    evidence = build_input_evidence(phase461, phase162, selected)
    gates = build_gates(phase461, phase162, selected)
    acceptance = build_acceptance(gates, selected)
    selected.to_csv(output_dir / "phase462_selected_replacement_files.csv", index=False)
    contract.to_csv(output_dir / "phase462_frozen_phase463_contract.csv", index=False)
    evidence.to_csv(output_dir / "phase462_input_evidence.csv", index=False)
    gates.to_csv(output_dir / "phase462_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase462_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, evidence, contract, selected, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase462_distributional_label_source_replacement_precommit",
        "contract_hash": hash_frame(contract),
        **reproducibility_fields(
            artifact_id="phase462_distributional_label_source_replacement_precommit",
            generated_utc=generated_utc,
            inputs={
                "phase461_acceptance_summary": str(phase461_dir / "phase461_acceptance_summary.csv"),
                "phase162_acceptance_summary": str(phase162_dir / "phase162_full_year_materialization_acceptance_summary.csv"),
                "replacement_dense_root": str(DEFAULT_DISTRIBUTIONAL_ROOT),
            },
            parameters={
                "thesis_id": THESIS_ID,
                "selected_source_id": SELECTED_SOURCE_ID,
                "profile_id": DEFAULT_PROFILE_ID,
                "months": MONTHS,
                "symbols": TARGET_SYMBOLS,
                "starts": WINDOW_START_ROWS,
                "entry_index": ENTRY_INDEX,
                "horizon_ticks": HORIZON_TICKS,
                "min_abs_forward_move_bps": MIN_ABS_FORWARD_MOVE_BPS,
            },
            outputs={"acceptance_summary": str(output_dir / "phase462_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase462_precommit_no_execution",
        ),
    }
    (output_dir / "phase462_distributional_label_source_replacement_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase462 distributional label-source replacement precommit.")
    parser.add_argument("--phase461-dir", type=Path, default=DEFAULT_PHASE461_DIR)
    parser.add_argument("--phase162-dir", type=Path, default=DEFAULT_PHASE162_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase461_dir, args.phase162_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
