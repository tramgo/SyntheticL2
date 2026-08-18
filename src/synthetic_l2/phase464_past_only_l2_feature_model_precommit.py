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


DEFAULT_PHASE463_DIR = Path("outputs/phase463")
DEFAULT_OUTPUT_DIR = Path("outputs/phase464")

THESIS_ID = "P464_PAST_ONLY_L1_L5_FEATURE_MODEL_PRECOMMIT"
MODEL_FAMILY_ID = "class_weighted_regularized_logistic_direction_model_with_tree_baseline_diagnostic"
NEXT_ACTION = "run_phase465_train_holdout_past_only_l1_l5_label_model_no_strategy_pnl"

PAST_ONLY_FEATURES = [
    "recent_mid_return_bps",
    "spread_bps",
    "l1_imbalance",
    "l25_imbalance",
    "volume_delta_lookback",
]
FULL_DEPTH_REQUIRED_FEATURES = ["l25_imbalance"]
LABEL_COLUMNS = ["forward_return_bps", "abs_forward_return_bps", "label_side", "move_candidate"]
FORBIDDEN_AS_FEATURES = [
    "forward_return_bps",
    "abs_forward_return_bps",
    "label_side",
    "move_candidate",
    "exit_price",
    "exit_row",
]
TRAIN_MONTHS = ["2026-01", "2026-02"]
HOLDOUT_MONTHS = ["2026-03"]
MIN_TRAIN_ROWS = 500
MIN_HOLDOUT_ROWS = 200
MIN_TRAIN_MOVE_CANDIDATES = 250
MIN_HOLDOUT_MOVE_CANDIDATES = 100


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def hash_frame(frame: pd.DataFrame) -> str:
    return hashlib.sha256(frame.to_json(orient="records", date_format="iso").encode("utf-8")).hexdigest()


def add_split(ledger: pd.DataFrame) -> pd.DataFrame:
    out = ledger.copy()
    out["trade_month"] = out["trade_date"].astype(str).str.slice(0, 7)
    out["phase464_split"] = out["trade_month"].map(lambda m: "train" if m in TRAIN_MONTHS else ("holdout" if m in HOLDOUT_MONTHS else "unused"))
    return out


def split_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    if ledger.empty:
        return pd.DataFrame(columns=["phase464_split", "rows", "move_candidate_rows", "long_rows", "short_rows", "trade_dates", "symbols"])
    rows = []
    for split, grp in ledger.groupby("phase464_split", sort=True):
        rows.append(
            {
                "phase464_split": str(split),
                "rows": int(len(grp)),
                "move_candidate_rows": int(grp["move_candidate"].astype(int).sum()),
                "long_rows": int(grp["label_side"].astype(str).eq("long").sum()),
                "short_rows": int(grp["label_side"].astype(str).eq("short").sum()),
                "trade_dates": int(grp["trade_date"].nunique()),
                "symbols": int(grp["symbol"].nunique()),
            }
        )
    return pd.DataFrame(rows)


def split_value(summary: pd.DataFrame, split: str, column: str, default: Any = 0) -> Any:
    rows = summary.loc[summary["phase464_split"].astype(str).eq(split), column].tolist()
    return rows[0] if rows else default


def feature_contract() -> pd.DataFrame:
    rows = []
    for feature in PAST_ONLY_FEATURES:
        if feature == "recent_mid_return_bps":
            source = "entry row minus prior lookback mid price; computed before/at entry"
        elif feature == "spread_bps":
            source = "best ask minus best bid at entry"
        elif feature == "l1_imbalance":
            source = "top-of-book quantity imbalance at entry"
        elif feature == "l25_imbalance":
            source = "levels 2-5 bid/ask quantity imbalance at entry"
        else:
            source = "entry volume minus prior lookback volume"
        rows.append(
            {
                "feature_name": feature,
                "allowed_as_model_input": 1,
                "timestamp_rule": "must be observable at or before entry row",
                "source_definition": source,
                "full_depth_l2_l5_feature": int(feature in FULL_DEPTH_REQUIRED_FEATURES),
            }
        )
    for label in LABEL_COLUMNS:
        rows.append(
            {
                "feature_name": label,
                "allowed_as_model_input": 0,
                "timestamp_rule": "future label only; forbidden as predictor",
                "source_definition": "computed using exit row after horizon",
                "full_depth_l2_l5_feature": 0,
            }
        )
    return pd.DataFrame(rows)


def model_contract(split: pd.DataFrame, feature_hash: str) -> pd.DataFrame:
    rows = [
        ("phase464_thesis_id", THESIS_ID, "Precommit thesis"),
        ("model_family_id", MODEL_FAMILY_ID, "Allowed model family"),
        ("primary_model", "class_weighted_l2_regularized_logistic_regression", "Simple regularized baseline for direction/move labels"),
        ("diagnostic_baseline", "depth_feature_threshold_and_shuffled_label_controls", "Controls only, not promotion"),
        ("training_split", ";".join(TRAIN_MONTHS), "Training months"),
        ("holdout_split", ";".join(HOLDOUT_MONTHS), "Untouched holdout month"),
        ("allowed_features", ";".join(PAST_ONLY_FEATURES), "Feature columns allowed as inputs"),
        ("required_full_depth_features", ";".join(FULL_DEPTH_REQUIRED_FEATURES), "L2-L5 feature columns required"),
        ("forbidden_feature_columns", ";".join(FORBIDDEN_AS_FEATURES), "Leakage columns forbidden as predictors"),
        ("label_columns", ";".join(LABEL_COLUMNS), "Future labels retained only as targets"),
        ("minimum_train_rows", MIN_TRAIN_ROWS, "Training-row floor"),
        ("minimum_holdout_rows", MIN_HOLDOUT_ROWS, "Holdout-row floor"),
        ("minimum_train_move_candidates", MIN_TRAIN_MOVE_CANDIDATES, "Train candidate floor"),
        ("minimum_holdout_move_candidates", MIN_HOLDOUT_MOVE_CANDIDATES, "Holdout candidate floor"),
        ("split_summary_hash", hash_frame(split), "Frozen split summary hash"),
        ("feature_contract_hash", feature_hash, "Frozen feature contract hash"),
        ("phase465_allowed_next", 1, "Allows model fit/evaluation only"),
        ("strategy_pnl_allowed", 0, "No strategy P&L in Phase464/465"),
        ("strategy_promotion_allowed", 0, "No promotion"),
        ("paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("deployable_profitability_claim_allowed", 0, "No deployable claim"),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def input_evidence(phase463: pd.DataFrame, split: pd.DataFrame, ledger: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("phase463_phase464_allowed_next", scalar(phase463, "phase463_phase464_allowed_next", 0), "Phase463 allowance"),
        ("phase463_move_candidate_rows", scalar(phase463, "phase463_move_candidate_rows", 0), "Phase463 candidates"),
        ("phase463_long_label_rows", scalar(phase463, "phase463_long_label_rows", 0), "Phase463 long labels"),
        ("phase463_short_label_rows", scalar(phase463, "phase463_short_label_rows", 0), "Phase463 short labels"),
        ("ledger_rows", int(len(ledger)), "Rows in Phase463 ledger"),
        ("train_rows", split_value(split, "train", "rows", 0), "Training rows"),
        ("holdout_rows", split_value(split, "holdout", "rows", 0), "Holdout rows"),
        ("train_move_candidates", split_value(split, "train", "move_candidate_rows", 0), "Training move candidates"),
        ("holdout_move_candidates", split_value(split, "holdout", "move_candidate_rows", 0), "Holdout move candidates"),
        ("train_dates", split_value(split, "train", "trade_dates", 0), "Training trade dates"),
        ("holdout_dates", split_value(split, "holdout", "trade_dates", 0), "Holdout trade dates"),
        ("symbols", int(ledger["symbol"].nunique()) if not ledger.empty else 0, "Ledger symbol breadth"),
    ]
    return pd.DataFrame(rows, columns=["evidence_id", "observed_value", "description"])


def build_gates(phase463: pd.DataFrame, ledger: pd.DataFrame, split: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    columns = set(ledger.columns)
    allowed_feature_set = set(PAST_ONLY_FEATURES)
    forbidden_set = set(FORBIDDEN_AS_FEATURES)
    gates = [
        ("P464_PHASE463_PRECOMMIT_USED", as_int(scalar(phase463, "phase463_phase464_allowed_next", 0)) == 1, scalar(phase463, "phase463_phase464_allowed_next", 0), 1),
        ("P464_LEDGER_ROWS_PRESENT", len(ledger) > 0, len(ledger), ">0"),
        ("P464_MOVE_CANDIDATES_PRESENT", as_int(scalar(phase463, "phase463_move_candidate_rows", 0)) > 0, scalar(phase463, "phase463_move_candidate_rows", 0), ">0"),
        ("P464_TRAIN_SPLIT_ROWS", as_int(split_value(split, "train", "rows", 0)) >= MIN_TRAIN_ROWS, split_value(split, "train", "rows", 0), f">={MIN_TRAIN_ROWS}"),
        ("P464_HOLDOUT_SPLIT_ROWS", as_int(split_value(split, "holdout", "rows", 0)) >= MIN_HOLDOUT_ROWS, split_value(split, "holdout", "rows", 0), f">={MIN_HOLDOUT_ROWS}"),
        ("P464_TRAIN_MOVE_CANDIDATES", as_int(split_value(split, "train", "move_candidate_rows", 0)) >= MIN_TRAIN_MOVE_CANDIDATES, split_value(split, "train", "move_candidate_rows", 0), f">={MIN_TRAIN_MOVE_CANDIDATES}"),
        ("P464_HOLDOUT_MOVE_CANDIDATES", as_int(split_value(split, "holdout", "move_candidate_rows", 0)) >= MIN_HOLDOUT_MOVE_CANDIDATES, split_value(split, "holdout", "move_candidate_rows", 0), f">={MIN_HOLDOUT_MOVE_CANDIDATES}"),
        ("P464_FEATURE_COLUMNS_PRESENT", allowed_feature_set.issubset(columns), ";".join(sorted(allowed_feature_set & columns)), ";".join(PAST_ONLY_FEATURES)),
        ("P464_FULL_DEPTH_L2_L5_FEATURE_REQUIRED", set(FULL_DEPTH_REQUIRED_FEATURES).issubset(allowed_feature_set) and int(features["full_depth_l2_l5_feature"].sum()) >= 1, ";".join(FULL_DEPTH_REQUIRED_FEATURES), ">=1 L2-L5 feature"),
        ("P464_FORBIDDEN_LABELS_NOT_MODEL_INPUTS", forbidden_set.isdisjoint(allowed_feature_set), ";".join(sorted(forbidden_set & allowed_feature_set)), "empty"),
        ("P464_BOTH_DIRECTIONS_IN_TRAIN_AND_HOLDOUT", as_int(split_value(split, "train", "long_rows", 0)) > 0 and as_int(split_value(split, "train", "short_rows", 0)) > 0 and as_int(split_value(split, "holdout", "long_rows", 0)) > 0 and as_int(split_value(split, "holdout", "short_rows", 0)) > 0, f"train_long={split_value(split, 'train', 'long_rows', 0)};train_short={split_value(split, 'train', 'short_rows', 0)};holdout_long={split_value(split, 'holdout', 'long_rows', 0)};holdout_short={split_value(split, 'holdout', 'short_rows', 0)}", "all >0"),
        ("P464_NO_STRATEGY_PNL", True, "precommit_only", "no_pnl"),
        ("P464_NO_PAPER_LIVE_OR_CLAIM", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def acceptance(gates: pd.DataFrame, split: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    all_pass = int(hard_pass == hard_rows)
    rows = [
        ("phase464_past_only_l1_l5_feature_model_precommit_complete", 1, "Phase464 precommit completed"),
        ("phase464_thesis_id", THESIS_ID, "Precommit thesis"),
        ("phase464_model_family_id", MODEL_FAMILY_ID, "Selected model family"),
        ("phase464_train_rows", split_value(split, "train", "rows", 0), "Training rows"),
        ("phase464_holdout_rows", split_value(split, "holdout", "rows", 0), "Holdout rows"),
        ("phase464_train_move_candidate_rows", split_value(split, "train", "move_candidate_rows", 0), "Training move candidates"),
        ("phase464_holdout_move_candidate_rows", split_value(split, "holdout", "move_candidate_rows", 0), "Holdout move candidates"),
        ("phase464_execution_results_generated", 0, "Precommit only"),
        ("phase464_strategy_pnl_generated", 0, "No strategy P&L"),
        ("phase464_strategy_promotion_allowed", 0, "No promotion"),
        ("phase464_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase464_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase464_phase465_allowed_next", all_pass, "Allows model fit/evaluation only if all gates pass"),
        ("phase464_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase464_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase464_next_best_action", NEXT_ACTION if all_pass else "repair_phase463_label_split_before_model_fit", "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance_summary: pd.DataFrame, evidence: pd.DataFrame, split: pd.DataFrame, features: pd.DataFrame, contract: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase464 Past-Only L1-L5 Feature-Model Precommit",
        "",
        "Phase464 freezes a model-fit contract over Phase463 actual-move labels. It does not train a model, emit strategy P&L, or make any acceptance claim.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance_summary),
        "",
        "## Input Evidence",
        "",
        _markdown_table(evidence),
        "",
        "## Split Summary",
        "",
        _markdown_table(split),
        "",
        "## Feature Contract",
        "",
        _markdown_table(features),
        "",
        "## Frozen Phase465 Model Contract",
        "",
        _markdown_table(contract),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: future label columns are targets only. Phase465 may train/evaluate a past-only model, but strategy replay and P&L remain closed until separately precommitted.",
    ]
    (output_dir / "phase464_past_only_l1_l5_feature_model_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase463_dir: Path = DEFAULT_PHASE463_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase463 = read_csv(phase463_dir / "phase463_acceptance_summary.csv")
    ledger = read_csv(phase463_dir / "phase463_feature_label_ledger.csv")
    ledger = add_split(ledger)
    split = split_summary(ledger)
    features = feature_contract()
    contract = model_contract(split, hash_frame(features))
    evidence = input_evidence(phase463, split, ledger)
    gates = build_gates(phase463, ledger, split, features)
    acceptance_summary = acceptance(gates, split)
    ledger[["trade_date", "symbol", "candidate_start_row", "phase464_split", *PAST_ONLY_FEATURES, *LABEL_COLUMNS]].to_csv(output_dir / "phase464_split_label_matrix_preview.csv", index=False)
    split.to_csv(output_dir / "phase464_split_summary.csv", index=False)
    features.to_csv(output_dir / "phase464_feature_contract.csv", index=False)
    contract.to_csv(output_dir / "phase464_frozen_phase465_model_contract.csv", index=False)
    evidence.to_csv(output_dir / "phase464_input_evidence.csv", index=False)
    gates.to_csv(output_dir / "phase464_gate_evaluation.csv", index=False)
    acceptance_summary.to_csv(output_dir / "phase464_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance_summary, evidence, split, features, contract, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase464_past_only_l1_l5_feature_model_precommit",
        "contract_hash": hash_frame(contract),
        **reproducibility_fields(
            artifact_id="phase464_past_only_l1_l5_feature_model_precommit",
            generated_utc=generated_utc,
            inputs={"phase463_feature_label_ledger": str(phase463_dir / "phase463_feature_label_ledger.csv")},
            parameters={
                "thesis_id": THESIS_ID,
                "model_family_id": MODEL_FAMILY_ID,
                "train_months": TRAIN_MONTHS,
                "holdout_months": HOLDOUT_MONTHS,
                "past_only_features": PAST_ONLY_FEATURES,
                "forbidden_as_features": FORBIDDEN_AS_FEATURES,
            },
            outputs={"acceptance_summary": str(output_dir / "phase464_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase464_precommit_no_execution",
        ),
    }
    (output_dir / "phase464_past_only_l1_l5_feature_model_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase464 past-only L1-L5 feature-model precommit.")
    parser.add_argument("--phase463-dir", type=Path, default=DEFAULT_PHASE463_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    out = run(args.phase463_dir, args.output_dir)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
