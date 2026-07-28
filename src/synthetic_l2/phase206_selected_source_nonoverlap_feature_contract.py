from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE165_DIR = Path("outputs/phase165")
DEFAULT_PHASE168_DIR = Path("outputs/phase168")
DEFAULT_PHASE175_DIR = Path("outputs/phase175")
DEFAULT_PHASE197_DIR = Path("outputs/phase197")
DEFAULT_PHASE205_DIR = Path("outputs/phase205")
DEFAULT_OUTPUT_DIR = Path("outputs/phase206")
FORBIDDEN_OUTPUTS = "strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;model_fit"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = "") -> Any:
    if frame.empty or "metric" not in frame.columns or "value" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def build_blocked_reference_catalog(phase165_blocklist: pd.DataFrame, phase168_blocklist: pd.DataFrame, phase197_contract: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for record in phase165_blocklist.to_dict("records"):
        rows.append(
            {
                "blocked_reference_id": record.get("blocked_family_id", ""),
                "blocked_source": "phase165_phase164_full_year_replay_verdict",
                "blocked_form": record.get("phase164_strategy_ids", ""),
                "blocked_token": record.get("source_strategy_id", ""),
                "recommended_status": record.get("recommended_status", "blocked"),
                "unlock_condition": record.get("unlock_condition", ""),
            }
        )
    for record in phase168_blocklist.to_dict("records"):
        rows.append(
            {
                "blocked_reference_id": record.get("blocked_family_id", ""),
                "blocked_source": "phase168_s08_closure",
                "blocked_form": record.get("blocked_form", ""),
                "blocked_token": record.get("source_strategy_id", ""),
                "recommended_status": record.get("recommended_status", "blocked"),
                "unlock_condition": record.get("unlock_condition", ""),
            }
        )
    for record in phase197_contract.to_dict("records"):
        rows.append(
            {
                "blocked_reference_id": f"P197_PRIOR_CONTEXT_{record.get('feature_id', '')}",
                "blocked_source": "phase197_prior_context_feature_precommit",
                "blocked_form": record.get("feature_family", ""),
                "blocked_token": record.get("feature_id", ""),
                "recommended_status": "do_not_reuse_as_model_search_without_new_contract",
                "unlock_condition": "Allowed only if Phase206 catalog records a materially different feature purpose and no replay/model fitting.",
            }
        )
    return pd.DataFrame(rows)


def build_feature_family_catalog(phase175_schema: pd.DataFrame, phase205_contract: pd.DataFrame) -> pd.DataFrame:
    selected_route = str(metric_value(phase205_contract, "phase205_selected_route_id", "P205_REAL_RECEIVE_FLOW_CONTEXT_SOURCE_REFRESH"))
    rows: list[dict[str, Any]] = []
    for record in phase175_schema.to_dict("records"):
        feature_id = str(record.get("feature_id", ""))
        family = str(record.get("feature_family", ""))
        forbidden_use = str(record.get("forbidden_use", ""))
        allowed_role = "source_quality_or_context_feature"
        if "CROSS_SYMBOL" in feature_id:
            allowed_role = "target_excluded_synchrony_context_not_fixed_s08_score"
        elif "REGIME_STATE" in feature_id:
            allowed_role = "filter_context_only_until_future_precommit"
        elif "DEPTH_REFRESH" in feature_id:
            allowed_role = "top_five_market_by_price_churn_not_l3_l4_order_by_order"
        rows.append(
            {
                "phase206_feature_id": feature_id.replace("P175_", "P206_"),
                "source_phase175_feature_id": feature_id,
                "selected_route_id": selected_route,
                "feature_family": family,
                "definition": record.get("definition", ""),
                "minimum_input_columns": record.get("minimum_input_columns", ""),
                "minimum_source_days": record.get("minimum_source_days", ""),
                "allowed_horizons": record.get("allowed_horizons", ""),
                "leakage_control": record.get("leakage_control", ""),
                "phase175_forbidden_use": forbidden_use,
                "phase206_allowed_role": allowed_role,
                "model_fit_allowed": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
            }
        )
    return pd.DataFrame(rows)


def build_nonoverlap_audit(feature_catalog: pd.DataFrame, blocked_catalog: pd.DataFrame) -> pd.DataFrame:
    blocked_forms = ";".join(blocked_catalog.get("blocked_form", pd.Series(dtype=str)).astype(str).tolist()).lower()
    blocked_tokens = ";".join(blocked_catalog.get("blocked_token", pd.Series(dtype=str)).astype(str).tolist()).lower()
    rows: list[dict[str, Any]] = []
    for record in feature_catalog.to_dict("records"):
        feature_text = " ".join(
            [
                str(record.get("phase206_feature_id", "")),
                str(record.get("feature_family", "")),
                str(record.get("definition", "")),
                str(record.get("phase206_allowed_role", "")),
            ]
        ).lower()
        explicitly_excludes_s08 = "not fixed_s08_score" in feature_text.replace(" ", "_") or "not_fixed_s08_score" in feature_text.replace(" ", "_")
        overlaps_fixed_s08 = int("s08" in feature_text and "fixed" in feature_text and "score" in feature_text and not explicitly_excludes_s08)
        overlaps_phase164_token = int(any(token and token in feature_text for token in ["s01", "s02", "s03", "s04", "s05", "s06", "s07", "s09"]))
        overlaps_prior_context = int(str(record.get("source_phase175_feature_id", "")).replace("P175_", "P197_") in blocked_tokens)
        rows.append(
            {
                "phase206_feature_id": record.get("phase206_feature_id", ""),
                "blocked_reference_rows_checked": len(blocked_catalog),
                "blocked_forms_digest_available": int(bool(blocked_forms)),
                "overlaps_phase164_blocked_strategy_token": overlaps_phase164_token,
                "overlaps_phase167_fixed_s08_form": overlaps_fixed_s08,
                "overlaps_prior_phase197_context_search_without_new_contract": overlaps_prior_context,
                "nonoverlap_pass": int(overlaps_phase164_token == 0 and overlaps_fixed_s08 == 0),
                "audit_note": "Feature is source/context contract only; no model fit or replay in Phase206.",
                "strategy_replay_allowed": 0,
            }
        )
    return pd.DataFrame(rows)


def build_guardrail_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "guardrail_id": "P206_NO_MODEL_FIT",
                "requirement": "Phase206 may catalog features and overlap only; no model fitting, signal scoring or threshold search.",
                "required": 1,
            },
            {
                "guardrail_id": "P206_TARGET_SYMBOL_EXCLUSION_FOR_SYNCHRONY",
                "requirement": "Any future cross-symbol synchrony feature must precommit target-symbol exclusion and must not reuse Phase167 fixed S08 score.",
                "required": 1,
            },
            {
                "guardrail_id": "P206_TOP_FIVE_TERMINOLOGY",
                "requirement": "Depth features must be described as Zerodha top-five market-by-price book state, not exchange L3/L4 order-by-order data.",
                "required": 1,
            },
            {
                "guardrail_id": "P206_TRAIN_ONLY_BASELINES_NEXT",
                "requirement": "Any future baseline/context fitting must be train-date only before validation/test transform.",
                "required": 1,
            },
            {
                "guardrail_id": "P206_REPLAY_STAYS_CLOSED",
                "requirement": "No strategy replay, test replay, order/fill/P&L, promotion or paper/live acceptance may be emitted from Phase206.",
                "required": 1,
            },
        ]
    )


def build_phase207_work_order(feature_catalog: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "work_order_id": "P207_WO01_BUILD_ALLOWED_FEATURE_MATRIX",
                "action": "materialize a feature-availability matrix for the Phase206 catalog, no model fitting",
                "input_feature_rows": len(feature_catalog),
                "allowed_scope": "feature_matrix_no_replay",
                "strategy_replay_allowed": 0,
            },
            {
                "work_order_id": "P207_WO02_TARGET_EXCLUSION_ABLATION_SPEC",
                "action": "precommit target-symbol exclusion and negative-control ablations for cross-symbol synchrony",
                "input_feature_rows": len(feature_catalog),
                "allowed_scope": "ablation_spec_no_replay",
                "strategy_replay_allowed": 0,
            },
            {
                "work_order_id": "P207_WO03_LEAKAGE_AND_TERMINOLOGY_AUDIT",
                "action": "audit leakage controls and L1/top-five terminology before any feature matrix is used downstream",
                "input_feature_rows": len(feature_catalog),
                "allowed_scope": "quality_audit_no_replay",
                "strategy_replay_allowed": 0,
            },
        ]
    )


def build_gates(
    phase205_acceptance: pd.DataFrame,
    feature_catalog: pd.DataFrame,
    blocked_catalog: pd.DataFrame,
    nonoverlap: pd.DataFrame,
    guardrails: pd.DataFrame,
    work_order: pd.DataFrame,
) -> pd.DataFrame:
    phase205_complete = as_int(metric_value(phase205_acceptance, "phase205_material_new_source_precommit_complete", 0))
    nonoverlap_pass = int(nonoverlap["nonoverlap_pass"].astype(int).all()) if not nonoverlap.empty else 0
    replay_sum = 0
    for frame, cols in [
        (feature_catalog, ["model_fit_allowed", "strategy_replay_allowed", "test_replay_allowed_next", "promotion_allowed", "paper_or_live_acceptance_allowed"]),
        (nonoverlap, ["strategy_replay_allowed"]),
        (work_order, ["strategy_replay_allowed"]),
    ]:
        for col in cols:
            if not frame.empty and col in frame.columns:
                replay_sum += int(frame[col].astype(int).sum())
    return pd.DataFrame(
        [
            ("P206_PHASE205_COMPLETE", phase205_complete == 1, f"phase205_complete={phase205_complete}", "hard"),
            ("P206_FEATURE_CATALOG_RECORDED", len(feature_catalog) >= 6, f"feature_rows={len(feature_catalog)}", "hard"),
            ("P206_BLOCKED_REFERENCE_CATALOG_RECORDED", len(blocked_catalog) >= 8, f"blocked_rows={len(blocked_catalog)}", "hard"),
            ("P206_NONOVERLAP_AUDIT_PASSED", nonoverlap_pass == 1, f"nonoverlap_pass_rows={int(nonoverlap['nonoverlap_pass'].astype(int).sum()) if not nonoverlap.empty else 0}", "hard"),
            ("P206_GUARDRAILS_RECORDED", len(guardrails) >= 5 and guardrails["required"].astype(int).eq(1).all(), f"guardrail_rows={len(guardrails)}", "hard"),
            ("P206_PHASE207_WORK_ORDER_RECORDED", len(work_order) == 3 and work_order["strategy_replay_allowed"].astype(int).eq(0).all(), f"work_order_rows={len(work_order)}", "hard"),
            ("P206_NO_MODEL_FIT_REPLAY_OR_PROMOTION", replay_sum == 0, f"forbidden_flag_sum={replay_sum}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(
    feature_catalog: pd.DataFrame,
    blocked_catalog: pd.DataFrame,
    nonoverlap: pd.DataFrame,
    guardrails: pd.DataFrame,
    work_order: pd.DataFrame,
    gates: pd.DataFrame,
) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("phase206_feature_catalog_rows", len(feature_catalog), "Selected source feature-family catalog rows"),
            ("phase206_blocked_reference_rows", len(blocked_catalog), "Blocked/failed reference rows checked"),
            ("phase206_nonoverlap_audit_rows", len(nonoverlap), "Non-overlap audit rows"),
            ("phase206_nonoverlap_pass_rows", int(nonoverlap["nonoverlap_pass"].astype(int).sum()) if not nonoverlap.empty else 0, "Rows passing non-overlap audit"),
            ("phase206_guardrail_rows", len(guardrails), "Guardrail contract rows"),
            ("phase206_phase207_work_order_rows", len(work_order), "Phase207 work-order rows"),
            ("phase206_gate_rows", len(gates), "Gates evaluated"),
            ("phase206_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase206_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase206_nonoverlap_feature_contract_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase206 completed"),
            ("phase206_model_fit_allowed", 0, "No model fitting opened"),
            ("phase206_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase206_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase206_promotion_allowed", 0, "No promotion opened"),
            ("phase206_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase206_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase206_next_best_action", "run_phase207_allowed_feature_matrix_precommit_no_model_no_replay", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase206 Selected Source Non-overlap Feature Contract",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase206 checks the selected Phase205 receive-flow context source against failed/blocked prior forms and catalogs allowed feature families.",
        "It does not fit models, run replay, emit orders/fills/P&L, promote anything, or open paper/live acceptance.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase206_selected_source_nonoverlap_feature_contract_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase206(
    phase165_dir: Path,
    phase168_dir: Path,
    phase175_dir: Path,
    phase197_dir: Path,
    phase205_dir: Path,
    output_dir: Path,
    base_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase165_blocklist = read_csv(phase165_dir / "phase165_blocklist_candidate_update.csv")
    phase168_blocklist = read_csv(phase168_dir / "phase168_s08_blocklist_candidate_update.csv")
    phase175_schema = read_csv(phase175_dir / "phase175_receive_flow_feature_schema.csv")
    phase197_contract = read_csv(phase197_dir / "phase197_non_receive_flow_feature_contract.csv")
    phase205_acceptance = read_csv(phase205_dir / "phase205_material_new_source_acceptance_summary.csv")

    blocked_catalog = build_blocked_reference_catalog(phase165_blocklist, phase168_blocklist, phase197_contract)
    feature_catalog = build_feature_family_catalog(phase175_schema, phase205_acceptance)
    nonoverlap = build_nonoverlap_audit(feature_catalog, blocked_catalog)
    guardrails = build_guardrail_contract()
    work_order = build_phase207_work_order(feature_catalog)
    gates = build_gates(phase205_acceptance, feature_catalog, blocked_catalog, nonoverlap, guardrails, work_order)
    acceptance = build_acceptance(feature_catalog, blocked_catalog, nonoverlap, guardrails, work_order, gates)

    blocked_catalog.to_csv(output_dir / "phase206_blocked_reference_catalog.csv", index=False)
    feature_catalog.to_csv(output_dir / "phase206_selected_source_feature_catalog.csv", index=False)
    nonoverlap.to_csv(output_dir / "phase206_selected_source_nonoverlap_audit.csv", index=False)
    guardrails.to_csv(output_dir / "phase206_guardrail_contract.csv", index=False)
    work_order.to_csv(output_dir / "phase206_phase207_work_order.csv", index=False)
    gates.to_csv(output_dir / "phase206_nonoverlap_feature_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase206_nonoverlap_feature_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Selected Source Feature Catalog": feature_catalog,
            "Blocked Reference Catalog": blocked_catalog,
            "Selected Source Non-overlap Audit": nonoverlap,
            "Guardrail Contract": guardrails,
            "Phase207 Work Order": work_order,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase206_selected_source_nonoverlap_feature_contract_no_model_no_replay",
        **reproducibility_fields(
            artifact_id="phase206_selected_source_nonoverlap_feature_contract",
            generated_utc=generated,
            inputs={
                "phase165_blocklist": str(phase165_dir / "phase165_blocklist_candidate_update.csv"),
                "phase168_blocklist": str(phase168_dir / "phase168_s08_blocklist_candidate_update.csv"),
                "phase175_schema": str(phase175_dir / "phase175_receive_flow_feature_schema.csv"),
                "phase197_contract": str(phase197_dir / "phase197_non_receive_flow_feature_contract.csv"),
                "phase205_acceptance": str(phase205_dir / "phase205_material_new_source_acceptance_summary.csv"),
            },
            parameters={
                "contract_scope": "selected_source_nonoverlap_feature_contract",
                "model_fit_allowed": "0",
                "strategy_replay_allowed": "0",
                "test_replay_allowed_next": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "blocked_catalog": str(output_dir / "phase206_blocked_reference_catalog.csv"),
                "feature_catalog": str(output_dir / "phase206_selected_source_feature_catalog.csv"),
                "nonoverlap": str(output_dir / "phase206_selected_source_nonoverlap_audit.csv"),
                "guardrails": str(output_dir / "phase206_guardrail_contract.csv"),
                "work_order": str(output_dir / "phase206_phase207_work_order.csv"),
                "gates": str(output_dir / "phase206_nonoverlap_feature_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase206_nonoverlap_feature_acceptance_summary.csv"),
                "report": str(output_dir / "phase206_selected_source_nonoverlap_feature_contract_report.md"),
            },
            scenario_ids="phase206_selected_source_nonoverlap_feature_contract_no_model_no_replay",
            cost_model_version="not_applicable_no_strategy_replay",
            latency_model_version="not_applicable_no_strategy_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase206_nonoverlap_feature_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Phase206 selected source non-overlap feature contract.")
    parser.add_argument("--phase165-dir", type=Path, default=DEFAULT_PHASE165_DIR)
    parser.add_argument("--phase168-dir", type=Path, default=DEFAULT_PHASE168_DIR)
    parser.add_argument("--phase175-dir", type=Path, default=DEFAULT_PHASE175_DIR)
    parser.add_argument("--phase197-dir", type=Path, default=DEFAULT_PHASE197_DIR)
    parser.add_argument("--phase205-dir", type=Path, default=DEFAULT_PHASE205_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase206(args.phase165_dir, args.phase168_dir, args.phase175_dir, args.phase197_dir, args.phase205_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
