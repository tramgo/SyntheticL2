from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_OUTPUT_DIR = Path("outputs/phase136")
DEFAULT_PHASE116_DIR = Path("outputs/phase116")
DEFAULT_PHASE132_DIR = Path("outputs/phase132")
DEFAULT_PHASE133_DIR = Path("outputs/phase133")
BLOCKLIST_FAMILY_ID = "DEEP_BOOK_LABEL_LIFT"
FORBIDDEN_OUTPUTS = "strategy_code;buy_sell_signal;order_arrival_stream;live_tagged_fill_model;pnl_replay;profitability_claim"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    value = rows.iloc[0]
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def verify_blocklist(blocklist: pd.DataFrame) -> pd.DataFrame:
    if blocklist.empty or "blocked_family_id" not in blocklist.columns:
        present = False
        blocked_strategy_ids = ""
    else:
        rows = blocklist[blocklist["blocked_family_id"].astype(str).eq(BLOCKLIST_FAMILY_ID)]
        present = not rows.empty
        blocked_strategy_ids = str(rows["blocked_strategy_ids"].iloc[0]) if present and "blocked_strategy_ids" in rows.columns else ""
    return pd.DataFrame(
        [
            {
                "verification_id": "P136_PHASE116_BLOCKLIST_ENTRY",
                "blocked_family_id": BLOCKLIST_FAMILY_ID,
                "entry_present": present,
                "blocked_strategy_ids": blocked_strategy_ids,
                "required_blocked_strategy_ids_contains": "phase131_phase132_top_five_depth_feature_diagnostics",
                "verification_pass": bool(present and "phase131_phase132_top_five_depth_feature_diagnostics" in blocked_strategy_ids),
            }
        ]
    )


def choose_outcome(phase132_summary: pd.DataFrame, phase133_summary: pd.DataFrame, blocklist_verification: pd.DataFrame) -> str:
    phase132_kill = as_int(metric_value(phase132_summary, "phase132_kill_switch_fired", 0))
    phase132_survivors = as_int(metric_value(phase132_summary, "phase132_surviving_feature_rows", 0))
    phase133_phase134_open = as_int(metric_value(phase133_summary, "phase133_phase134_open_allowed", 0))
    blocklist_ok = bool(blocklist_verification["verification_pass"].astype(bool).all()) if not blocklist_verification.empty else False
    if phase132_kill == 1 or phase132_survivors == 0 or phase133_phase134_open == 0:
        return "A_CLEAN_FALSIFICATION" if blocklist_ok else "A_CLEAN_FALSIFICATION_BLOCKLIST_REVIEW_REQUIRED"
    return "B_OR_C_REQUIRES_PHASE134_PHASE135_EVIDENCE_NOT_AVAILABLE"


def build_gate_evaluation(phase132_summary: pd.DataFrame, phase133_summary: pd.DataFrame, blocklist_verification: pd.DataFrame, outcome: str) -> pd.DataFrame:
    phase132_kill = as_int(metric_value(phase132_summary, "phase132_kill_switch_fired", 0))
    phase132_survivors = as_int(metric_value(phase132_summary, "phase132_surviving_feature_rows", 0))
    phase132_blocklist = as_int(metric_value(phase132_summary, "phase132_phase116_blocklist_entry_present", 0))
    phase133_gates = as_int(metric_value(phase133_summary, "phase133_hard_gate_pass_rows", 0))
    phase133_gate_rows = as_int(metric_value(phase133_summary, "phase133_hard_gate_rows", 0))
    phase133_phase134_open = as_int(metric_value(phase133_summary, "phase133_phase134_open_allowed", 0))
    phase133_replay = as_int(metric_value(phase133_summary, "phase133_strategy_replay_allowed", 0))
    blocklist_ok = bool(blocklist_verification["verification_pass"].astype(bool).all()) if not blocklist_verification.empty else False
    rows = [
        ("phase136_phase132_kill_switch_fired", bool(phase132_kill == 1), phase132_kill, 1, "hard"),
        ("phase136_no_surviving_phase132_features", bool(phase132_survivors == 0), phase132_survivors, 0, "hard"),
        ("phase136_phase132_blocklist_evidence_present", bool(phase132_blocklist == 1), phase132_blocklist, 1, "hard"),
        ("phase136_phase116_blocklist_entry_verified", blocklist_ok, int(blocklist_ok), 1, "hard"),
        ("phase136_phase133_contract_gates_passed", bool(phase133_gates == phase133_gate_rows and phase133_gate_rows > 0), f"{phase133_gates}/{phase133_gate_rows}", "all_phase133_hard_gates", "hard"),
        ("phase136_phase134_not_opened", bool(phase133_phase134_open == 0), phase133_phase134_open, 0, "hard"),
        ("phase136_strategy_replay_remains_closed", bool(phase133_replay == 0), phase133_replay, 0, "hard"),
        ("phase136_outcome_a_selected", outcome.startswith("A_CLEAN_FALSIFICATION"), outcome, "A_CLEAN_FALSIFICATION", "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate", "pass", "observed", "required", "severity"])


def build_verdict(outcome: str, phase132_summary: pd.DataFrame, phase133_summary: pd.DataFrame, contract: dict[str, Any]) -> dict[str, Any]:
    return {
        "verdict_id": "phase136_deep_book_verdict",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "outcome": outcome,
        "decision": "deep_book_top_five_passive_branch_closed",
        "reason": "Phase132 fired the kill-switch with zero surviving top-five-depth feature rows; Phase133 respected the kill-switch and kept Phase134 closed.",
        "phase132": {
            "kill_switch_fired": as_int(metric_value(phase132_summary, "phase132_kill_switch_fired", 0)),
            "surviving_feature_rows": as_int(metric_value(phase132_summary, "phase132_surviving_feature_rows", 0)),
            "blocklist_entry_present": as_int(metric_value(phase132_summary, "phase132_phase116_blocklist_entry_present", 0)),
            "strategy_replay_allowed": as_int(metric_value(phase132_summary, "phase132_strategy_replay_allowed", 0)),
        },
        "phase133": {
            "contract_version": contract.get("contract_version", ""),
            "hard_gate_rows": as_int(metric_value(phase133_summary, "phase133_hard_gate_rows", 0)),
            "hard_gate_pass_rows": as_int(metric_value(phase133_summary, "phase133_hard_gate_pass_rows", 0)),
            "phase134_open_allowed": as_int(metric_value(phase133_summary, "phase133_phase134_open_allowed", 0)),
            "strategy_replay_allowed": as_int(metric_value(phase133_summary, "phase133_strategy_replay_allowed", 0)),
        },
        "forbidden_outputs": FORBIDDEN_OUTPUTS,
        "next_best_action": "wait_for_real_l2_anchor_unlock_or_start_new_precommitted_non_blocklisted_research_branch",
    }


def summarize(gates: pd.DataFrame, outcome: str, phase132_summary: pd.DataFrame, phase133_summary: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["pass"].astype(bool).sum()) if not hard.empty else 0
    hard_total = int(len(hard))
    return pd.DataFrame(
        [
            ("phase136_hard_gate_rows", hard_total, "Hard closure-verdict gates evaluated"),
            ("phase136_hard_gate_pass_rows", hard_pass, "Hard closure-verdict gates passed"),
            ("phase136_outcome", outcome, "Selected Phase136 outcome"),
            ("phase136_clean_falsification_selected", int(outcome.startswith("A_CLEAN_FALSIFICATION")), "1 means Outcome A closes the branch"),
            ("phase136_phase132_kill_switch_fired", as_int(metric_value(phase132_summary, "phase132_kill_switch_fired", 0)), "Inherited Phase132 kill-switch flag"),
            ("phase136_phase132_surviving_feature_rows", as_int(metric_value(phase132_summary, "phase132_surviving_feature_rows", 0)), "Inherited Phase132 surviving feature rows"),
            ("phase136_phase133_phase134_open_allowed", as_int(metric_value(phase133_summary, "phase133_phase134_open_allowed", 0)), "Inherited Phase133 Phase134-open flag"),
            ("phase136_strategy_replay_allowed", 0, "Phase136 never unlocks strategy replay"),
            ("phase136_next_best_action", "wait_for_real_l2_anchor_unlock_or_start_new_precommitted_non_blocklisted_research_branch", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_markdown_verdict(output_dir: Path, verdict: dict[str, Any], gates: pd.DataFrame, acceptance: pd.DataFrame, blocklist_verification: pd.DataFrame) -> None:
    lines = [
        "# Phase136 Deep-book Verdict and Handoff",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        f"Outcome: `{verdict['outcome']}`",
        "",
        "The top-five-depth passive branch is closed as a clean falsification. Phase132 fired the kill-switch, Phase116 contains the corresponding blocklist entry, and Phase133 kept Phase134 closed after producing the passive execution contract.",
        "",
        "No Phase134 precommit, Phase135 replay, buy/sell signal, order-arrival stream, live-tagged fill model, or deployable profitability claim is emitted.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "## Blocklist Verification",
        "",
        _markdown_table(blocklist_verification),
        "",
    ]
    (output_dir / "phase136_deep_book_clean_falsification_verdict.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase136(output_dir: Path, base_dir: Path, phase116_dir: Path, phase132_dir: Path, phase133_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase132_summary = read_csv(phase132_dir / "phase132_deep_book_feature_diagnostics_acceptance_summary.csv")
    phase133_summary = read_csv(phase133_dir / "phase133_passive_execution_model_upgrade_acceptance_summary.csv")
    blocklist = read_csv(phase116_dir / "strategy_replay_blocklist.csv")
    contract = read_json(phase133_dir / "phase133_execution_contract.json")
    blocklist_verification = verify_blocklist(blocklist)
    outcome = choose_outcome(phase132_summary, phase133_summary, blocklist_verification)
    gates = build_gate_evaluation(phase132_summary, phase133_summary, blocklist_verification, outcome)
    acceptance = summarize(gates, outcome, phase132_summary, phase133_summary)
    verdict = build_verdict(outcome, phase132_summary, phase133_summary, contract)

    (output_dir / "phase136_deep_book_verdict.json").write_text(json.dumps(verdict, indent=2), encoding="utf-8")
    blocklist_verification.to_csv(output_dir / "phase136_blocklist_verification.csv", index=False)
    gates.to_csv(output_dir / "phase136_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase136_deep_book_verdict_acceptance_summary.csv", index=False)
    write_markdown_verdict(output_dir, verdict, gates, acceptance, blocklist_verification)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase136_deep_book_verdict_and_handoff",
        **reproducibility_fields(
            artifact_id="phase136",
            generated_utc=generated_utc,
            inputs={
                "phase116_blocklist": str(phase116_dir / "strategy_replay_blocklist.csv"),
                "phase132_summary": str(phase132_dir / "phase132_deep_book_feature_diagnostics_acceptance_summary.csv"),
                "phase133_summary": str(phase133_dir / "phase133_passive_execution_model_upgrade_acceptance_summary.csv"),
                "phase133_contract": str(phase133_dir / "phase133_execution_contract.json"),
            },
            parameters={
                "blocklist_family_id": BLOCKLIST_FAMILY_ID,
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
                "outcome_policy": "Outcome_A_when_phase132_kill_switch_or_zero_survivors_or_phase133_keeps_phase134_closed",
            },
            outputs={
                "verdict_json": str(output_dir / "phase136_deep_book_verdict.json"),
                "verdict_markdown": str(output_dir / "phase136_deep_book_clean_falsification_verdict.md"),
                "blocklist_verification": str(output_dir / "phase136_blocklist_verification.csv"),
                "gate_evaluation": str(output_dir / "phase136_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase136_deep_book_verdict_acceptance_summary.csv"),
                "manifest": str(output_dir / "phase136_deep_book_verdict_manifest.json"),
            },
            random_seed="none_deterministic_verdict",
            scenario_ids="phase136_deep_book_verdict_and_handoff",
            cost_model_version=str(contract.get("zerodha_cost_model_version", "not_applicable")),
            latency_model_version=str(contract.get("contract_version", "not_applicable")),
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase136_deep_book_verdict_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase136 deep-book verdict and handoff.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--phase116-dir", type=Path, default=DEFAULT_PHASE116_DIR)
    parser.add_argument("--phase132-dir", type=Path, default=DEFAULT_PHASE132_DIR)
    parser.add_argument("--phase133-dir", type=Path, default=DEFAULT_PHASE133_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase136(args.output_dir, args.base_dir, args.phase116_dir, args.phase132_dir, args.phase133_dir)


if __name__ == "__main__":
    main()
