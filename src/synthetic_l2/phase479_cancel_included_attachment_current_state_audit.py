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


DEFAULT_ATTACHMENT = Path(r"C:\Users\Ramic\Downloads\cancel_included.txt")
DEFAULT_OUTPUT_DIR = Path("outputs/phase479")
THESIS_ID = "P479_CANCEL_INCLUDED_ATTACHMENT_CURRENT_STATE_AUDIT"
ATTACHMENT_CHARTER_ID = "P407_CANCEL_LATENCY_MARKET_MAKER_REALISM"
NEXT_ACTION = "do_not_rerun_or_tune_cancel_included_market_maker_continue_phase478_real_l2_one_day_expansion"
REPAIR_ACTION = "repair_phase479_cancel_included_attachment_audit"


def text_hash(path: Path) -> str:
    if not path.exists():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def has_all(text: str, needles: list[str]) -> bool:
    lowered = text.lower()
    return all(needle.lower() in lowered for needle in needles)


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def build_attachment_requirement_audit(attachment_text: str, phase407: pd.DataFrame, phase408: pd.DataFrame, phase409: pd.DataFrame, gates408: pd.DataFrame) -> pd.DataFrame:
    best_net = scalar(phase408, "phase408_best_net_pnl_inr", "")
    best_ann = scalar(phase408, "phase408_best_annualized_return_pct", "")
    rows = [
        (
            "charter_scope_recognized",
            has_all(attachment_text, ["retail two-sided quoting", "cancel-race", "Zerodha top-5"]),
            "Attachment text contains the retail two-sided quoting cancel-race scope.",
            ATTACHMENT_CHARTER_ID,
        ),
        (
            "phase407_precommit_exists",
            as_int(scalar(phase407, "phase407_cancel_latency_market_maker_precommit_complete", 0)) == 1,
            "Phase407 precommit completed before results.",
            scalar(phase407, "phase407_charter_id", ""),
        ),
        (
            "latency_grid_precommitted",
            as_int(scalar(phase407, "phase407_latency_grid_rows", 0)) == 45,
            "Phase407 pinned 45 cancel latency, decision latency, move-threshold scenarios.",
            scalar(phase407, "phase407_latency_grid_hash", ""),
        ),
        (
            "per_tick_cancel_race_executed",
            as_int(scalar(phase408, "phase408_per_tick_cancel_race_market_maker_complete", 0)) == 1,
            "Phase408 executed the per-tick cancel-race simulator.",
            scalar(phase408, "phase408_best_scenario_id", ""),
        ),
        (
            "all_required_named_gates_evaluated",
            len(gates408) == 18,
            "Attachment says 17 hard gates, but enumerates 18 named gates; Phase408 evaluated 18.",
            len(gates408),
        ),
        (
            "breadth_was_not_the_problem",
            as_int(scalar(phase408, "phase408_best_completed_round_trips", 0)) >= 30
            and as_int(scalar(phase408, "phase408_best_trade_dates", 0)) >= 5
            and as_int(scalar(phase408, "phase408_best_symbols", 0)) >= 3,
            "Best Phase408 route met event/date/symbol breadth.",
            f"round_trips={scalar(phase408, 'phase408_best_completed_round_trips', '')};dates={scalar(phase408, 'phase408_best_trade_dates', '')};symbols={scalar(phase408, 'phase408_best_symbols', '')}",
        ),
        (
            "profitability_failed_materially",
            float(scalar(phase408, "phase408_best_annualized_return_pct", 0.0)) < 12.0,
            "Best Phase408 route failed the 12 percent cost200 annualized floor.",
            f"net_pnl_inr={best_net};annualized_pct={best_ann}",
        ),
        (
            "kill_switch_fired",
            as_int(scalar(phase408, "phase408_kill_switch_triggered", 0)) == 1,
            "Phase408 kill switch fired.",
            scalar(phase408, "phase408_kill_switch_triggered", ""),
        ),
        (
            "phase409_terminal_verdict_exists",
            str(scalar(phase409, "phase409_selected_verdict", "")) == "P409_CANCEL_RACE_MARKET_MAKER_FALSIFIED",
            "Phase409 upgraded the P263 closure to strong falsification for the tested route.",
            scalar(phase409, "phase409_selected_verdict", ""),
        ),
        (
            "no_tune_it_outcome_preserved",
            as_int(scalar(phase409, "phase409_same_family_tuning_allowed", 1)) == 0,
            "The attachment permits only survive or falsified; no tuning path remains open.",
            scalar(phase409, "phase409_same_family_tuning_allowed", ""),
        ),
    ]
    return pd.DataFrame(
        [
            {
                "requirement_id": requirement_id,
                "satisfied": bool(satisfied),
                "evidence": evidence,
                "observed_value": observed,
            }
            for requirement_id, satisfied, evidence, observed in rows
        ]
    )


def build_decision_ledger(phase408: pd.DataFrame, phase409: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "decision_id": "cancel_included_attachment_status",
                "decision": "already_precommitted_executed_and_falsified_in_phase407_409",
                "evidence": "Phase407 precommit, Phase408 per-tick cancel-race run, Phase409 terminal interpretation exist.",
                "action_allowed": "current_state_audit_only",
            },
            {
                "decision_id": "best_cancel_race_result",
                "decision": "failed_cost200_profitability",
                "evidence": f"net_pnl_inr={scalar(phase408, 'phase408_best_net_pnl_inr', '')};annualized_pct={scalar(phase408, 'phase408_best_annualized_return_pct', '')};survivors={scalar(phase408, 'phase408_cost200_acceptance_survivor_rows', '')}",
                "action_allowed": "negative_evidence_only",
            },
            {
                "decision_id": "retail_market_maker_family_status",
                "decision": scalar(phase409, "phase409_selected_verdict", ""),
                "evidence": "Same-family tuning is forbidden by the attachment and by Phase409.",
                "action_allowed": "reopen_only_with_new_external_execution_source",
            },
            {
                "decision_id": "post_phase478_path",
                "decision": "continue_real_l2_one_day_expansion",
                "evidence": "Phase478 selected one disk-safe official-catalyst real-L2 day expansion after synthetic and sparse-real failures.",
                "action_allowed": NEXT_ACTION,
            },
        ]
    )


def build_gates(requirements: pd.DataFrame, decision: pd.DataFrame) -> pd.DataFrame:
    req_pass = int(requirements["satisfied"].astype(bool).sum())
    req_rows = int(len(requirements))
    rows = [
        ("P479_ATTACHMENT_READ", req_rows > 0, req_rows, ">0"),
        ("P479_PHASE407_409_ARTIFACTS_RECOGNIZED", req_pass == req_rows, f"{req_pass}/{req_rows}", f"{req_rows}/{req_rows}"),
        ("P479_CANCEL_INCLUDED_ALREADY_EXECUTED", decision["decision"].astype(str).str.contains("phase407_409", case=False, regex=False).any(), "phase407_409", "present"),
        ("P479_NO_MARKET_MAKER_TUNING", decision["action_allowed"].astype(str).str.contains("negative_evidence_only", case=False, regex=False).any(), "negative_evidence_only", "required"),
        ("P479_REAL_L2_EXPANSION_REMAINS_NEXT", decision["decision"].astype(str).eq("continue_real_l2_one_day_expansion").any(), NEXT_ACTION, NEXT_ACTION),
        ("P479_NO_PROMOTION_PAPER_LIVE_OR_CLAIM", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame(
        [
            {
                "gate_id": gate_id,
                "passed": bool(passed),
                "observed_value": observed,
                "required_value": required,
                "severity": "hard",
            }
            for gate_id, passed, observed, required in rows
        ]
    )


def build_acceptance(attachment_path: Path, attachment_text: str, requirements: pd.DataFrame, gates: pd.DataFrame, phase408: pd.DataFrame) -> pd.DataFrame:
    gate_pass = int(gates["passed"].astype(bool).sum())
    gate_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase479_cancel_included_attachment_audit_complete", int(gate_pass == gate_rows), "Phase479 complete if all gates pass"),
            ("phase479_thesis_id", THESIS_ID, "Phase479 thesis"),
            ("phase479_attachment_path", str(attachment_path), "Attachment audited"),
            ("phase479_attachment_sha256", text_hash(attachment_path), "Attachment content hash"),
            ("phase479_attachment_charter_status", "already_executed_in_phase407_409", "Current-state status"),
            ("phase479_attachment_requirement_pass_rows", int(requirements["satisfied"].astype(bool).sum()), "Attachment requirements satisfied by existing artifacts"),
            ("phase479_attachment_requirement_rows", int(len(requirements)), "Audited attachment requirement rows"),
            ("phase479_phase408_best_net_pnl_inr", scalar(phase408, "phase408_best_net_pnl_inr", ""), "Best Phase408 net PnL"),
            ("phase479_phase408_best_annualized_return_pct", scalar(phase408, "phase408_best_annualized_return_pct", ""), "Best Phase408 annualized return"),
            ("phase479_market_maker_tuning_allowed", 0, "No same-family tuning"),
            ("phase479_strategy_promotion_allowed", 0, "No promotion"),
            ("phase479_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase479_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase479_hard_gate_pass_rows", gate_pass, "Passed hard gates"),
            ("phase479_hard_gate_rows", gate_rows, "Hard gates"),
            ("phase479_next_best_action", NEXT_ACTION if gate_pass == gate_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, requirements: pd.DataFrame, decision: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase479 Cancel-Included Attachment Current-State Audit",
        "",
        "Phase479 handles the attached cancel-included market-maker charter in the current Phase478+ plan state.",
        "",
        "Finding: the attached charter is already represented and executed by Phase407-409. Phase408 did run the per-tick cancel-race model; Phase409 falsified the tested retail two-sided top-five L2 market-maker route. Therefore this attachment does not open a new tuning shard.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Attachment Requirement Audit",
        "",
        _markdown_table(requirements),
        "",
        "## Decision Ledger",
        "",
        _markdown_table(decision),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: no market-maker resurrection, no paper/live, no deployable profitability claim. The next practical path remains one disk-safe real-L2 catalyst-day expansion.",
    ]
    (output_dir / "phase479_cancel_included_attachment_current_state_audit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(attachment_path: Path = DEFAULT_ATTACHMENT, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    attachment_text = attachment_path.read_text(encoding="utf-8", errors="replace") if attachment_path.exists() else ""
    phase407 = read_csv(Path("outputs/phase407/phase407_acceptance_summary.csv"))
    phase408 = read_csv(Path("outputs/phase408/phase408_acceptance_summary.csv"))
    phase409 = read_csv(Path("outputs/phase409/phase409_acceptance_summary.csv"))
    gates408 = read_csv(Path("outputs/phase408/phase408_gate_evaluation.csv"))
    if not attachment_text:
        raise FileNotFoundError(f"Attachment text not found or empty: {attachment_path}")
    if phase407.empty or phase408.empty or phase409.empty or gates408.empty:
        raise FileNotFoundError("Phase479 requires Phase407, Phase408, and Phase409 current-state outputs.")
    requirements = build_attachment_requirement_audit(attachment_text, phase407, phase408, phase409, gates408)
    decision = build_decision_ledger(phase408, phase409)
    gates = build_gates(requirements, decision)
    acceptance = build_acceptance(attachment_path, attachment_text, requirements, gates, phase408)
    requirements.to_csv(output_dir / "phase479_attachment_requirement_audit.csv", index=False)
    decision.to_csv(output_dir / "phase479_decision_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase479_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase479_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, requirements, decision, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase479_cancel_included_attachment_current_state_audit",
        **reproducibility_fields(
            artifact_id="phase479_cancel_included_attachment_current_state_audit",
            generated_utc=generated_utc,
            inputs={
                "attachment": str(attachment_path),
                "phase407_acceptance_summary": "outputs/phase407/phase407_acceptance_summary.csv",
                "phase408_acceptance_summary": "outputs/phase408/phase408_acceptance_summary.csv",
                "phase408_gate_evaluation": "outputs/phase408/phase408_gate_evaluation.csv",
                "phase409_acceptance_summary": "outputs/phase409/phase409_acceptance_summary.csv",
            },
            parameters={"thesis_id": THESIS_ID, "next_action": NEXT_ACTION, "new_strategy_run": False},
            outputs={"acceptance_summary": str(output_dir / "phase479_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase407_precommitted_cancel_latency_grid_already_executed",
        ),
    }
    (output_dir / "phase479_cancel_included_attachment_current_state_audit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase479 cancel-included attachment current-state audit.")
    parser.add_argument("--attachment", type=Path, default=DEFAULT_ATTACHMENT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    out = run(args.attachment, args.output_dir)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
