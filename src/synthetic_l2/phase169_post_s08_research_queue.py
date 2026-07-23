from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase169")
DEFAULT_PHASE121_DIR = Path("outputs/phase121")
DEFAULT_PHASE130_DIR = Path("outputs/phase130")
DEFAULT_PHASE136_DIR = Path("outputs/phase136")
DEFAULT_PHASE165_DIR = Path("outputs/phase165")
DEFAULT_PHASE168_DIR = Path("outputs/phase168")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = "missing") -> Any:
    if frame.empty or "metric" not in frame.columns or "value" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def to_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def build_closure_ledger(
    phase121: pd.DataFrame,
    phase130: pd.DataFrame,
    phase136: pd.DataFrame,
    phase165: pd.DataFrame,
    phase168: pd.DataFrame,
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "closure_id": "P121_SIMPLE_PASSIVE_BRANCH_RETIRED",
                "scope": "simple_passive_queue_and_richer_passive_label_branch",
                "status": "closed",
                "evidence": metric_value(phase121, "phase121_next_best_action", "missing"),
                "strategy_replay_allowed": to_int(metric_value(phase121, "phase121_passive_replay_allowed", 0)),
                "best_net_pnl_inr": "not_applicable_closure_summary",
            },
            {
                "closure_id": "P130_NON_TRADING_DIAGNOSTICS_AVAILABLE",
                "scope": "non_trading_filter_diagnostics",
                "status": "available_for_gating_not_replay",
                "evidence": metric_value(phase130, "phase130_next_best_action", "missing"),
                "strategy_replay_allowed": to_int(metric_value(phase130, "phase130_strategy_replay_allowed", 0)),
                "best_net_pnl_inr": "not_applicable_no_replay",
            },
            {
                "closure_id": "P136_DEEP_BOOK_PASSIVE_BRANCH_FALSIFIED",
                "scope": "top_five_depth_passive_branch",
                "status": "closed",
                "evidence": metric_value(phase136, "phase136_next_best_action", "missing"),
                "strategy_replay_allowed": 0,
                "best_net_pnl_inr": "not_applicable_closure_summary",
            },
            {
                "closure_id": "P165_PHASE164_FULL_YEAR_FORMS_FALSIFIED",
                "scope": "phase164_s01_s07_s09_guarded_diagnostic_forms",
                "status": "closed",
                "evidence": metric_value(phase165, "phase165_outcome", "missing"),
                "strategy_replay_allowed": to_int(metric_value(phase165, "phase165_strategy_promotion_allowed", 0)),
                "best_net_pnl_inr": to_float(metric_value(phase165, "phase165_best_annual_net_pnl_inr", 0.0)),
            },
            {
                "closure_id": "P168_S08_CURRENT_FORM_FALSIFIED",
                "scope": "phase167_s08_cross_symbol_lead_lag_current_form",
                "status": "closed",
                "evidence": metric_value(phase168, "phase168_outcome", "missing"),
                "strategy_replay_allowed": to_int(metric_value(phase168, "phase168_strategy_promotion_allowed", 0)),
                "best_net_pnl_inr": to_float(metric_value(phase168, "phase168_best_annual_net_pnl_inr", 0.0)),
            },
        ]
    )


def build_forbidden_family_ledger(phase165_blocklist: pd.DataFrame, phase168_blocklist: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if not phase165_blocklist.empty:
        for record in phase165_blocklist.to_dict("records"):
            rows.append(
                {
                    "blocked_family_id": record.get("blocked_family_id", "missing"),
                    "source_strategy_id": record.get("source_strategy_id", "missing"),
                    "blocked_scope": record.get("phase164_strategy_ids", "missing"),
                    "recommended_status": record.get("recommended_status", "blocked"),
                    "unlock_condition": record.get("unlock_condition", "new precommitted hypothesis required"),
                }
            )
    if not phase168_blocklist.empty:
        for record in phase168_blocklist.to_dict("records"):
            rows.append(
                {
                    "blocked_family_id": record.get("blocked_family_id", "missing"),
                    "source_strategy_id": record.get("source_strategy_id", "missing"),
                    "blocked_scope": record.get("blocked_form", "missing"),
                    "recommended_status": record.get("recommended_status", "blocked"),
                    "unlock_condition": record.get("unlock_condition", "new precommitted hypothesis required"),
                }
            )
    return pd.DataFrame(rows)


def build_candidate_source_evaluation(phase130: pd.DataFrame, phase168: pd.DataFrame) -> pd.DataFrame:
    diagnostic_ready = to_int(metric_value(phase130, "phase130_all_gates_pass", 0)) == 1
    replay_closed = to_int(metric_value(phase130, "phase130_strategy_replay_allowed", 1)) == 0
    s08_closed = str(metric_value(phase168, "phase168_outcome", "")) == "A_S08_CURRENT_FORM_FALSIFIED"
    return pd.DataFrame(
        [
            {
                "candidate_source_id": "REAL_L2_ANCHOR_ACQUISITION",
                "priority": 1,
                "source_type": "external_real_data",
                "allowed_next_step": "download_first_local_catalog_refresh",
                "why": "Real Zerodha L2 remains the strongest unlock for calibration and acceptance.",
                "strategy_replay_allowed": 0,
                "selected_for_synthetic_continuation": 0,
            },
            {
                "candidate_source_id": "P130_FILTER_CONDITIONED_DIAGNOSTICS",
                "priority": 2,
                "source_type": "non_trading_diagnostic_feature_source",
                "allowed_next_step": "phase170_filter_conditioned_feasibility_matrix_no_replay",
                "why": "It is not a blocked taker/passive/cross-symbol trading form and can gate future hypotheses without emitting orders.",
                "strategy_replay_allowed": 0,
                "selected_for_synthetic_continuation": int(diagnostic_ready and replay_closed and s08_closed),
            },
            {
                "candidate_source_id": "REOPEN_PHASE164_OR_PHASE167_FORMS",
                "priority": 99,
                "source_type": "blocked_replay_family",
                "allowed_next_step": "none",
                "why": "Phase165 and Phase168 closed these forms with full-year negative after-cost evidence.",
                "strategy_replay_allowed": 0,
                "selected_for_synthetic_continuation": 0,
            },
        ]
    )


def build_next_queue(candidate_sources: pd.DataFrame) -> pd.DataFrame:
    selected = candidate_sources[candidate_sources["selected_for_synthetic_continuation"].eq(1)].copy()
    rows = []
    if not selected.empty:
        rows.append(
            {
                "queue_rank": 1,
                "next_phase": "Phase170",
                "next_item": "filter_conditioned_feasibility_matrix_no_replay",
                "input_source": "outputs/phase130/diagnostic_model_selection.csv;outputs/phase129/allowed_context_label_matrix.csv;outputs/phase168/phase168_s08_blocklist_candidate_update.csv",
                "deliverable": "candidate feature-source feasibility matrix with blocked-family overlap audit",
                "forbidden_deliverable": "buy_sell_signal;order_arrival;fill_model;pnl_replay;profitability_claim",
                "strategy_replay_allowed": 0,
                "reason": "Advance only the diagnostic filter source; no trading replay until a future precommit clears overlap and evidence gates.",
            }
        )
    rows.append(
        {
            "queue_rank": 2,
            "next_phase": "real_anchor",
            "next_item": "continue_download_first_real_l2_acquisition",
            "input_source": "Azure storage downloaded to local Parquet before analysis",
            "deliverable": "local real L2 catalog and calibration refresh",
            "forbidden_deliverable": "direct_python_azure_strategy_scan",
            "strategy_replay_allowed": 0,
            "reason": "Real L2 remains primary; heavy analysis must stay local-first.",
        }
    )
    return pd.DataFrame(rows)


def build_gate_evaluation(closure: pd.DataFrame, forbidden: pd.DataFrame, candidate_sources: pd.DataFrame, queue: pd.DataFrame) -> pd.DataFrame:
    closed_required = closure[closure["closure_id"].isin(["P165_PHASE164_FULL_YEAR_FORMS_FALSIFIED", "P168_S08_CURRENT_FORM_FALSIFIED"])]
    selected = candidate_sources[candidate_sources["selected_for_synthetic_continuation"].eq(1)]
    return pd.DataFrame(
        [
            {
                "gate_id": "P169_PHASE165_AND_PHASE168_CLOSED",
                "gate_pass": int(not closed_required.empty and closed_required["status"].eq("closed").all()),
                "evidence": ";".join(closed_required["closure_id"].astype(str).tolist()),
            },
            {
                "gate_id": "P169_FORBIDDEN_FAMILY_LEDGER_PRESENT",
                "gate_pass": int(len(forbidden) >= 9),
                "evidence": f"forbidden_rows={len(forbidden)}",
            },
            {
                "gate_id": "P169_SELECTED_SOURCE_IS_NON_TRADING",
                "gate_pass": int(len(selected) == 1 and selected["source_type"].iloc[0] == "non_trading_diagnostic_feature_source"),
                "evidence": ";".join(selected["candidate_source_id"].astype(str).tolist()) if not selected.empty else "none",
            },
            {
                "gate_id": "P169_NO_REPLAY_UNLOCK",
                "gate_pass": int(
                    candidate_sources["strategy_replay_allowed"].astype(int).sum() == 0
                    and queue["strategy_replay_allowed"].astype(int).sum() == 0
                ),
                "evidence": "all strategy_replay_allowed fields are 0",
            },
            {
                "gate_id": "P169_AZURE_POLICY_LOCAL_FIRST",
                "gate_pass": int(queue["forbidden_deliverable"].astype(str).str.contains("direct_python_azure_strategy_scan").any()),
                "evidence": "real_anchor queue forbids direct Python Azure strategy scans",
            },
        ]
    )


def build_acceptance_summary(closure: pd.DataFrame, forbidden: pd.DataFrame, candidate_sources: pd.DataFrame, queue: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    selected = candidate_sources[candidate_sources["selected_for_synthetic_continuation"].eq(1)]
    selected_id = selected["candidate_source_id"].iloc[0] if not selected.empty else "none"
    return pd.DataFrame(
        [
            ("phase169_closure_rows", int(len(closure)), "Closure evidence rows consolidated"),
            ("phase169_forbidden_family_rows", int(len(forbidden)), "Blocked strategy-family/form rows carried forward"),
            ("phase169_candidate_source_rows", int(len(candidate_sources)), "Candidate next-source rows evaluated"),
            ("phase169_selected_synthetic_source", selected_id, "Selected synthetic-only source, if any"),
            ("phase169_next_queue_rows", int(len(queue)), "Next work-queue rows emitted"),
            ("phase169_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase169_all_gates_pass", int(gates["gate_pass"].astype(bool).all()) if not gates.empty else 0, "1 means queue obeys closure guardrails"),
            ("phase169_strategy_replay_allowed", 0, "No strategy replay is opened by Phase169"),
            ("phase169_paper_or_live_acceptance_allowed", 0, "Paper/live acceptance remains closed"),
            ("phase169_azure_read_policy", "forbidden_for_analysis_download_first_then_local", "No direct Python Azure scanning"),
            ("phase169_next_best_action", "implement_phase170_filter_conditioned_feasibility_matrix_no_replay", "Recommended next milestone"),
            ("phase169_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model retained for audit continuity"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase169 Post-S08 Research Queue",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase169 consolidates the latest closures and emits the next safe research queue.",
        "It does not run a strategy and does not open replay; it prevents rerunning closed forms under new names.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase169_post_s08_research_queue_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase169(
    output_dir: Path,
    phase121_dir: Path,
    phase130_dir: Path,
    phase136_dir: Path,
    phase165_dir: Path,
    phase168_dir: Path,
    base_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase121 = read_csv(phase121_dir / "phase121_passive_branch_retirement_acceptance_summary.csv")
    phase130 = read_csv(phase130_dir / "phase130_no_replay_diagnostic_baselines_acceptance_summary.csv")
    phase136 = read_csv(phase136_dir / "phase136_deep_book_verdict_acceptance_summary.csv")
    phase165 = read_csv(phase165_dir / "phase165_full_year_replay_verdict_acceptance_summary.csv")
    phase168 = read_csv(phase168_dir / "phase168_s08_closure_acceptance_summary.csv")
    phase165_blocklist = read_csv(phase165_dir / "phase165_blocklist_candidate_update.csv")
    phase168_blocklist = read_csv(phase168_dir / "phase168_s08_blocklist_candidate_update.csv")

    closure = build_closure_ledger(phase121, phase130, phase136, phase165, phase168)
    forbidden = build_forbidden_family_ledger(phase165_blocklist, phase168_blocklist)
    candidate_sources = build_candidate_source_evaluation(phase130, phase168)
    queue = build_next_queue(candidate_sources)
    gates = build_gate_evaluation(closure, forbidden, candidate_sources, queue)
    acceptance = build_acceptance_summary(closure, forbidden, candidate_sources, queue, gates)

    closure.to_csv(output_dir / "phase169_closure_evidence_ledger.csv", index=False)
    forbidden.to_csv(output_dir / "phase169_forbidden_family_ledger.csv", index=False)
    candidate_sources.to_csv(output_dir / "phase169_candidate_source_evaluation.csv", index=False)
    queue.to_csv(output_dir / "phase169_next_research_queue.csv", index=False)
    gates.to_csv(output_dir / "phase169_research_queue_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase169_post_s08_research_queue_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Closure Evidence Ledger": closure,
            "Forbidden Family Ledger": forbidden,
            "Candidate Source Evaluation": candidate_sources,
            "Next Research Queue": queue,
            "Gate Evaluation": gates,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase169_post_s08_research_queue",
        **reproducibility_fields(
            artifact_id="phase169_post_s08_research_queue",
            generated_utc=generated_utc,
            inputs={
                "phase121_acceptance": str(phase121_dir / "phase121_passive_branch_retirement_acceptance_summary.csv"),
                "phase130_acceptance": str(phase130_dir / "phase130_no_replay_diagnostic_baselines_acceptance_summary.csv"),
                "phase136_acceptance": str(phase136_dir / "phase136_deep_book_verdict_acceptance_summary.csv"),
                "phase165_acceptance": str(phase165_dir / "phase165_full_year_replay_verdict_acceptance_summary.csv"),
                "phase168_acceptance": str(phase168_dir / "phase168_s08_closure_acceptance_summary.csv"),
            },
            parameters={
                "queue_policy": "real_anchor_primary_and_synthetic_only_filter_conditioned_no_replay_next",
                "strategy_replay_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "azure_read_policy": "forbidden_for_analysis_download_first_then_local",
            },
            outputs={
                "acceptance_summary": str(output_dir / "phase169_post_s08_research_queue_acceptance_summary.csv"),
                "closure_ledger": str(output_dir / "phase169_closure_evidence_ledger.csv"),
                "forbidden_family_ledger": str(output_dir / "phase169_forbidden_family_ledger.csv"),
                "candidate_source_evaluation": str(output_dir / "phase169_candidate_source_evaluation.csv"),
                "next_research_queue": str(output_dir / "phase169_next_research_queue.csv"),
            },
            random_seed="none_deterministic_phase169_queue",
            scenario_ids="post_phase168_current_research_state",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_queue_only",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase169_post_s08_research_queue_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--phase121-dir", type=Path, default=DEFAULT_PHASE121_DIR)
    parser.add_argument("--phase130-dir", type=Path, default=DEFAULT_PHASE130_DIR)
    parser.add_argument("--phase136-dir", type=Path, default=DEFAULT_PHASE136_DIR)
    parser.add_argument("--phase165-dir", type=Path, default=DEFAULT_PHASE165_DIR)
    parser.add_argument("--phase168-dir", type=Path, default=DEFAULT_PHASE168_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase169(args.output_dir, args.phase121_dir, args.phase130_dir, args.phase136_dir, args.phase165_dir, args.phase168_dir, args.base_dir)


if __name__ == "__main__":
    main()
