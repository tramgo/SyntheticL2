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


DEFAULT_PHASE468_DIR = Path("outputs/phase468")
DEFAULT_PHASE467_DIR = Path("outputs/phase467")
DEFAULT_OUTPUT_DIR = Path("outputs/phase469")

THESIS_ID = "P469_SOURCE_EVENT_AWARE_FEATURE_REPAIR_PRECOMMIT"
NEXT_ACTION = "run_phase470_materialize_source_event_aware_l1_l5_feature_matrix_no_model_no_pnl"

FAILED_GATE_ID = "P468_FEATURE_VARIATION_PRESENT"
SOURCE_EVENT_LOOKBACKS = [1, 3, 5]
MIN_VARYING_FEATURES = 18
MIN_L2_L5_VARYING_FEATURES = 8

REPLACED_CONSTANT_FEATURES = [
    "recent_mid_return_bps",
    "ofi_l1_lookback",
    "ofi_l25_lookback",
    "l25_replenishment_events",
    "l25_withdrawal_events",
    "spread_change_lookback_bps",
]

REPAIR_FEATURES = [
    ("source_event_mid_return_1", "source_event_price", "mid return versus previous distinct source event", 0),
    ("source_event_mid_return_3", "source_event_price", "mid return versus three source events back", 0),
    ("source_event_mid_return_5", "source_event_price", "mid return versus five source events back", 0),
    ("source_event_l1_ofi_1", "source_event_ofi", "signed L1 depth change versus previous source event", 0),
    ("source_event_l1_ofi_3", "source_event_ofi", "signed L1 depth change versus three source events back", 0),
    ("source_event_l25_ofi_1", "source_event_ofi", "signed L2-L5 depth change versus previous source event", 1),
    ("source_event_l25_ofi_3", "source_event_ofi", "signed L2-L5 depth change versus three source events back", 1),
    ("source_event_l25_replenishment_count_5", "source_event_churn", "positive L2-L5 depth-change count across last five source events", 1),
    ("source_event_l25_withdrawal_count_5", "source_event_churn", "negative L2-L5 depth-change count across last five source events", 1),
    ("source_event_spread_change_3_bps", "source_event_spread", "spread change versus three source events back", 0),
    ("source_event_spread_vol_5_bps", "source_event_spread", "spread volatility across last five source events", 0),
]


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def hash_frame(frame: pd.DataFrame) -> str:
    return hashlib.sha256(frame.to_json(orient="records", date_format="iso").encode("utf-8")).hexdigest()


def build_repair_contract(base_features: pd.DataFrame) -> pd.DataFrame:
    retained = base_features[~base_features["feature_name"].astype(str).isin(REPLACED_CONSTANT_FEATURES)].copy()
    repair = pd.DataFrame(
        [
            {
                "feature_name": name,
                "feature_family": family,
                "timestamp_rule": "computed from distinct source_annual_event_id rows at or before entry only",
                "description": description,
                "uses_l2_l5_depth": uses_l25,
                "allowed_as_model_input": 1,
            }
            for name, family, description, uses_l25 in REPAIR_FEATURES
        ]
    )
    combined = pd.concat([retained, repair], ignore_index=True)
    combined["allowed_as_model_input"] = combined["allowed_as_model_input"].astype(int)
    combined["uses_l2_l5_depth"] = combined["uses_l2_l5_depth"].astype(int)
    return combined


def build_decision(phase468: pd.DataFrame, gates: pd.DataFrame, quality: pd.DataFrame) -> pd.DataFrame:
    failed = gates.loc[~gates["passed"].astype(bool)].copy()
    constant = quality.loc[quality["unique_values"].astype(int).le(1), "feature_name"].astype(str).tolist()
    rows = [
        ("selected_verdict", "P469_REPAIR_CONSTANT_DENSE_SUBTICK_FEATURES", "Phase468 matrix exists but the variation gate failed."),
        ("phase468_matrix_rows", scalar(phase468, "phase468_matrix_rows", 0), "Phase468 matrix rows."),
        ("phase468_move_candidate_rows", scalar(phase468, "phase468_move_candidate_rows", 0), "Phase468 move candidates."),
        ("phase468_failed_gate_ids", ";".join(failed["gate_id"].astype(str).tolist()), "Failed Phase468 gates."),
        ("constant_feature_names", ";".join(constant), "Features with one unique value."),
        ("source_event_lookbacks", ";".join(str(x) for x in SOURCE_EVENT_LOOKBACKS), "Distinct source-event lookbacks selected."),
        ("same_20_dense_tick_churn_reuse_allowed", 0, "Do not reuse the constant dense-subtick churn features."),
        ("model_fit_allowed", 0, "No model fit in Phase469/470."),
        ("strategy_pnl_allowed", 0, "No strategy P&L."),
        ("paper_or_live_acceptance_allowed", 0, "No paper/live."),
    ]
    return pd.DataFrame(rows, columns=["decision_id", "decision_value", "description"])


def build_gates(phase468: pd.DataFrame, gates468: pd.DataFrame, base_features: pd.DataFrame, repair_features: pd.DataFrame, decision: pd.DataFrame) -> pd.DataFrame:
    failed_gate = gates468.loc[gates468["gate_id"].astype(str).eq(FAILED_GATE_ID)]
    failed_gate_confirmed = (not failed_gate.empty) and (not bool(failed_gate.iloc[0]["passed"]))
    feature_names = set(repair_features["feature_name"].astype(str))
    decision_map = dict(zip(decision["decision_id"].astype(str), decision["decision_value"]))
    rows = [
        ("P469_PHASE468_COMPLETE", as_int(scalar(phase468, "phase468_richer_past_only_l1_l5_feature_matrix_complete", 0)) == 1, scalar(phase468, "phase468_richer_past_only_l1_l5_feature_matrix_complete", 0), 1),
        ("P469_PHASE468_VARIATION_FAILURE_CONFIRMED", failed_gate_confirmed, FAILED_GATE_ID if failed_gate_confirmed else "", FAILED_GATE_ID),
        ("P469_PHASE469_MODEL_PRECOMMIT_BLOCKED_BY_PHASE468", as_int(scalar(phase468, "phase468_phase469_allowed_next", 1)) == 0, scalar(phase468, "phase468_phase469_allowed_next", 1), 0),
        ("P469_CONSTANT_FEATURES_REPLACED", set(REPLACED_CONSTANT_FEATURES).isdisjoint(feature_names), ";".join(sorted(set(REPLACED_CONSTANT_FEATURES) & feature_names)), "empty"),
        ("P469_SOURCE_EVENT_REPAIR_FEATURES_ADDED", set(name for name, *_ in REPAIR_FEATURES).issubset(feature_names), len(set(name for name, *_ in REPAIR_FEATURES) & feature_names), len(REPAIR_FEATURES)),
        ("P469_REPAIRED_FEATURE_COUNT_GE_25", len(repair_features) >= 25, len(repair_features), ">=25"),
        ("P469_REPAIRED_L2_L5_FEATURE_COUNT_GE_10", int(repair_features["uses_l2_l5_depth"].sum()) >= 10, int(repair_features["uses_l2_l5_depth"].sum()), ">=10"),
        ("P469_MIN_VARYING_FEATURE_FLOOR_RAISED", MIN_VARYING_FEATURES >= 18, MIN_VARYING_FEATURES, ">=18"),
        ("P469_SOURCE_EVENT_LOOKBACKS_PINNED", SOURCE_EVENT_LOOKBACKS == [1, 3, 5], ";".join(str(x) for x in SOURCE_EVENT_LOOKBACKS), "1;3;5"),
        ("P469_SAME_CONSTANT_REUSE_REJECTED", as_int(decision_map.get("same_20_dense_tick_churn_reuse_allowed", 1)) == 0, decision_map.get("same_20_dense_tick_churn_reuse_allowed", ""), 0),
        ("P469_NO_MODEL_FIT", True, "precommit_only", "no_model_fit"),
        ("P469_NO_STRATEGY_PNL", True, "precommit_only", "no_pnl"),
        ("P469_NO_PAPER_LIVE_OR_CLAIM", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in rows])


def build_acceptance(gates: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    all_pass = int(hard_pass == hard_rows)
    rows = [
        ("phase469_source_event_aware_feature_repair_precommit_complete", 1, "Phase469 precommit completed"),
        ("phase469_thesis_id", THESIS_ID, "Precommit thesis"),
        ("phase469_repaired_feature_count", int(len(features)), "Repaired feature count"),
        ("phase469_repaired_l2_l5_feature_count", int(features["uses_l2_l5_depth"].sum()), "Repaired L2-L5 feature count"),
        ("phase469_replaced_constant_feature_count", len(REPLACED_CONSTANT_FEATURES), "Constant features replaced"),
        ("phase469_source_event_lookbacks", ";".join(str(x) for x in SOURCE_EVENT_LOOKBACKS), "Pinned source-event lookbacks"),
        ("phase469_min_varying_feature_floor", MIN_VARYING_FEATURES, "Phase470 variation floor"),
        ("phase469_model_fit_generated", 0, "No model fit"),
        ("phase469_strategy_pnl_generated", 0, "No strategy P&L"),
        ("phase469_strategy_promotion_allowed", 0, "No promotion"),
        ("phase469_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase469_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase469_phase470_allowed_next", all_pass, "Allows repaired matrix materialization only"),
        ("phase469_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase469_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase469_next_best_action", NEXT_ACTION if all_pass else "repair_phase469_contract_before_materialization", "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, decision: pd.DataFrame, features: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase469 Source-Event-Aware Feature Repair Precommit",
        "",
        "Phase469 freezes a repair for Phase468's constant dense-subtick churn features. It does not materialize the repaired matrix yet.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Decision Ledger",
        "",
        _markdown_table(decision),
        "",
        "## Repaired Feature Contract",
        "",
        _markdown_table(features),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase470 may materialize the repaired matrix only. Model fitting, strategy replay and P&L remain closed.",
    ]
    (output_dir / "phase469_source_event_aware_feature_repair_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase468_dir: Path = DEFAULT_PHASE468_DIR, phase467_dir: Path = DEFAULT_PHASE467_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase468 = read_csv(phase468_dir / "phase468_acceptance_summary.csv")
    gates468 = read_csv(phase468_dir / "phase468_gate_evaluation.csv")
    quality = read_csv(phase468_dir / "phase468_feature_quality.csv")
    base_features = read_csv(phase467_dir / "phase467_feature_contract.csv")
    repaired_features = build_repair_contract(base_features)
    decision = build_decision(phase468, gates468, quality)
    gates = build_gates(phase468, gates468, base_features, repaired_features, decision)
    acceptance = build_acceptance(gates, repaired_features)
    repaired_features.to_csv(output_dir / "phase469_repaired_feature_contract.csv", index=False)
    decision.to_csv(output_dir / "phase469_decision_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase469_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase469_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, decision, repaired_features, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase469_source_event_aware_feature_repair_precommit",
        "repaired_feature_contract_hash": hash_frame(repaired_features),
        **reproducibility_fields(
            artifact_id="phase469_source_event_aware_feature_repair_precommit",
            generated_utc=generated_utc,
            inputs={"phase468_acceptance_summary": str(phase468_dir / "phase468_acceptance_summary.csv")},
            parameters={"thesis_id": THESIS_ID, "source_event_lookbacks": SOURCE_EVENT_LOOKBACKS, "min_varying_features": MIN_VARYING_FEATURES},
            outputs={"acceptance_summary": str(output_dir / "phase469_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase469_precommit_no_execution",
        ),
    }
    (output_dir / "phase469_source_event_aware_feature_repair_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase469 source-event-aware feature repair precommit.")
    parser.add_argument("--phase468-dir", type=Path, default=DEFAULT_PHASE468_DIR)
    parser.add_argument("--phase467-dir", type=Path, default=DEFAULT_PHASE467_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    out = run(args.phase468_dir, args.phase467_dir, args.output_dir)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
