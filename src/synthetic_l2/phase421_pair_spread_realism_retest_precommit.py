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
from synthetic_l2.phase417_pair_spread_convergence_precommit import (
    ANNUALIZED_THRESHOLD_PCT,
    COST_MULTIPLIER,
    ENTRY_ZSCORE,
    EXIT_ZSCORE,
    INITIAL_CAPITAL_INR,
    LEG_NOTIONAL_INR,
    LOOKBACK_TICKS,
    MAX_HOLD_TICKS,
    MIN_COMPLETED_ROUND_TRIPS,
    MIN_PAIRS,
    MIN_POSITIVE_DATE_FRACTION,
    MIN_TRADE_DATES,
    PAIRS,
    STOP_ZSCORE,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE420_DIR = Path("outputs/phase420")
DEFAULT_OUTPUT_DIR = Path("outputs/phase421")

THESIS_ID = "P421_PAIR_SPREAD_REALISM_RETEST_FULL_DEPTH_UNIQUE_GATE"
NEXT_ACTION = "run_phase422_pair_spread_realism_retest_execution_no_paper_live"
REPAIR_ACTION = "repair_phase421_pair_spread_realism_retest_precommit"

MIN_FORWARD_HOLD_MS = 250.0
MIN_FORWARD_TICKS_AFTER_ENTRY = 3
MIN_L2_L5_EDGE_DELTA_VS_REMOVED_PCT = 5.0
REQUIRE_REAL_ANCHOR_PAIR_DATES = 5
ALIGN_TOLERANCE_MS = 1_000
MAX_ROWS_PER_SYMBOL_MONTH = 25_000


def sha256_frame(frame: pd.DataFrame) -> str:
    payload = frame.to_csv(index=False, lineterminator="\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def build_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("thesis_id", THESIS_ID, "Realism repair precommit for the Phase418 positive pair lead."),
            ("relationship_to_phase418", "same_pair_family_allowed_only_as_precommitted_repair_not_promotion", "This is a repair retest, not a new acceptance claim."),
            ("phase420_blockers_addressed", "full_depth_contribution;timing_realism;real_anchor_pair_panel;cost_rank", "All Phase420 required repairs are in scope."),
            ("pair_catalog", ";".join(f"{a}/{b}" for a, b in PAIRS), "Same frozen Phase417 pairs."),
            ("entry_signal", "same_pair_spread_zscore_form_as_phase417", "Signal form unchanged to isolate repairs."),
            ("minimum_forward_time", f"hold_ms>={MIN_FORWARD_HOLD_MS}", "Blocks same-timestamp exits."),
            ("minimum_forward_ticks", f"ticks_after_entry>={MIN_FORWARD_TICKS_AFTER_ENTRY}", "Requires actual forward ticks after entry."),
            ("full_depth_unique_gate", f"primary_annualized_minus_l2_removed>={MIN_L2_L5_EDGE_DELTA_VS_REMOVED_PCT}", "Levels 2-5 must add value versus removal."),
            ("real_anchor_requirement", f"real_anchor_pair_dates>={REQUIRE_REAL_ANCHOR_PAIR_DATES}", "Use existing local real pair coverage."),
            ("execution_profile", "taker_entry_both_legs_taker_exit_both_legs_cost200", "No passive fill, no maker rebate."),
            ("cost_model", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha equity intraday NSE formula."),
            ("cost_multiplier", COST_MULTIPLIER, "Cost200 acceptance scoring."),
            ("capital", f"initial={INITIAL_CAPITAL_INR};leg_notional={LEG_NOTIONAL_INR}", "Fixed capital denominator."),
            ("acceptance", f"round_trips>={MIN_COMPLETED_ROUND_TRIPS};dates>={MIN_TRADE_DATES};pairs>={MIN_PAIRS};positive_date_fraction>={MIN_POSITIVE_DATE_FRACTION};annualized>={ANNUALIZED_THRESHOLD_PCT}", "Same profitability acceptance discipline."),
            ("forbidden", "promotion_before_phase422;paper_live;deployable_claim;dropping_l2_l5_gate;dropping_forward_time_rule", "Closed boundaries."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def build_parameter_freeze() -> pd.DataFrame:
    rows = [
        ("P421_LOOKBACK_TICKS", LOOKBACK_TICKS, "same_as_phase417"),
        ("P421_ENTRY_ZSCORE", ENTRY_ZSCORE, "same_as_phase417"),
        ("P421_EXIT_ZSCORE", EXIT_ZSCORE, "same_as_phase417"),
        ("P421_STOP_ZSCORE", STOP_ZSCORE, "same_as_phase417"),
        ("P421_MAX_HOLD_TICKS", MAX_HOLD_TICKS, "same_as_phase417"),
        ("P421_MIN_FORWARD_HOLD_MS", MIN_FORWARD_HOLD_MS, "new_repair"),
        ("P421_MIN_FORWARD_TICKS_AFTER_ENTRY", MIN_FORWARD_TICKS_AFTER_ENTRY, "new_repair"),
        ("P421_MIN_L2_L5_EDGE_DELTA_VS_REMOVED_PCT", MIN_L2_L5_EDGE_DELTA_VS_REMOVED_PCT, "new_repair"),
        ("P421_REQUIRE_REAL_ANCHOR_PAIR_DATES", REQUIRE_REAL_ANCHOR_PAIR_DATES, "new_repair"),
        ("P421_ALIGN_TOLERANCE_MS", ALIGN_TOLERANCE_MS, "same_as_phase418"),
        ("P421_MAX_ROWS_PER_SYMBOL_MONTH", MAX_ROWS_PER_SYMBOL_MONTH, "bounded_execution"),
    ]
    return pd.DataFrame(rows, columns=["parameter_id", "value", "status"])


def build_execution_hard_gates() -> pd.DataFrame:
    gates = [
        ("P422_PHASE421_PRECOMMIT_USED", "Execution must read Phase421 frozen contract."),
        ("P422_FORWARD_TIME_ENFORCED", f"Exit must be at least {MIN_FORWARD_HOLD_MS} ms after entry."),
        ("P422_FORWARD_TICKS_ENFORCED", f"Exit must be at least {MIN_FORWARD_TICKS_AFTER_ENTRY} aligned ticks after entry."),
        ("P422_FULL_DEPTH_UNIQUE_GATE", "Primary must beat L2-L5 removed control by required margin."),
        ("P422_REAL_ANCHOR_PAIR_PANEL_USED", "Use local real-anchor pair dates if available."),
        ("P422_PAIR_MARKET_NEUTRAL", "Equal notional long/short pair exposure."),
        ("P422_TAKER_ONLY", "No passive fill and no maker rebate."),
        ("P422_NO_LOOKAHEAD", "Rolling features before entry only."),
        ("P422_COST200_FIXED_CAPITAL", "Zerodha cost200 with fixed capital."),
        ("P422_BREADTH_AND_RETURN_GATES", "Event/date/pair/positive-date/annualized gates must pass."),
        ("P422_COST_RANK_RECORDED", "Cost100 and cost200 rank must be recorded."),
        ("P422_BOUNDARIES_CLOSED", "No promotion, paper/live or deployable claim in execution phase."),
    ]
    return pd.DataFrame(
        [{"gate_id": gate, "requirement": requirement, "severity": "hard", "phase421_precommitted": 1} for gate, requirement in gates]
    )


def build_input_registry(summary420: pd.DataFrame, fd: pd.DataFrame, timing: pd.DataFrame, real_anchor: pd.DataFrame) -> pd.DataFrame:
    real_pairs = int(pd.to_numeric(real_anchor.get("real_anchor_pair_available", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()) if not real_anchor.empty else 0
    min_overlap = int(pd.to_numeric(real_anchor.get("overlap_dates", pd.Series(dtype=float)), errors="coerce").fillna(0).min()) if not real_anchor.empty else 0
    return pd.DataFrame(
        [
            ("phase420_complete", scalar(summary420, "phase420_pair_spread_repair_audit_complete", ""), "Phase420 audit complete."),
            ("phase420_positive_lead_preserved", scalar(summary420, "phase420_phase418_positive_lead_preserved", ""), "Lead still alive."),
            ("phase420_acceptance_allowed", scalar(summary420, "phase420_acceptance_allowed", ""), "Must be zero before repair."),
            ("phase420_full_depth_contribution_pass", fd.loc[fd["audit_id"].eq("full_depth_contribution_pass"), "value"].iloc[0] if not fd.empty else "", "Must be zero blocker."),
            ("phase420_timing_realism_pass", timing.loc[timing["audit_id"].eq("timing_realism_pass"), "value"].iloc[0] if not timing.empty else "", "Must be zero blocker."),
            ("phase420_same_timestamp_share", timing.loc[timing["audit_id"].eq("same_timestamp_share"), "value"].iloc[0] if not timing.empty else "", "Timing blocker magnitude."),
            ("phase420_real_anchor_pair_available_count", real_pairs, "Real-anchor pair availability."),
            ("phase420_min_overlap_dates_per_pair", min_overlap, "Minimum overlap dates across frozen pairs."),
            ("execution_results_generated_now", 0, "Precommit only."),
        ],
        columns=["input_id", "value", "description"],
    )


def build_gates(inputs: pd.DataFrame, contract: pd.DataFrame, freeze: pd.DataFrame, exec_gates: pd.DataFrame) -> pd.DataFrame:
    values = dict(zip(inputs["input_id"], inputs["value"]))
    forbidden = ";".join(contract.loc[contract["contract_id"].eq("forbidden"), "contract_value"].astype(str).tolist())
    gates = [
        ("P421_PHASE420_COMPLETE", str(values.get("phase420_complete", "")) == "1", values.get("phase420_complete", ""), 1),
        ("P421_POSITIVE_LEAD_PRESERVED", str(values.get("phase420_positive_lead_preserved", "")) == "1", values.get("phase420_positive_lead_preserved", ""), 1),
        ("P421_ACCEPTANCE_STILL_BLOCKED", str(values.get("phase420_acceptance_allowed", "")) == "0", values.get("phase420_acceptance_allowed", ""), 0),
        ("P421_FULL_DEPTH_BLOCKER_ACKNOWLEDGED", as_int(values.get("phase420_full_depth_contribution_pass", 1)) == 0, values.get("phase420_full_depth_contribution_pass", ""), 0),
        ("P421_TIMING_BLOCKER_ACKNOWLEDGED", as_int(values.get("phase420_timing_realism_pass", 1)) == 0, values.get("phase420_timing_realism_pass", ""), 0),
        ("P421_REAL_ANCHOR_PANEL_AVAILABLE", as_int(values.get("phase420_min_overlap_dates_per_pair", 0)) >= REQUIRE_REAL_ANCHOR_PAIR_DATES, values.get("phase420_min_overlap_dates_per_pair", ""), f">={REQUIRE_REAL_ANCHOR_PAIR_DATES}"),
        ("P421_FORWARD_TIME_RULE_FROZEN", MIN_FORWARD_HOLD_MS > 0 and MIN_FORWARD_TICKS_AFTER_ENTRY > 0, f"ms={MIN_FORWARD_HOLD_MS};ticks={MIN_FORWARD_TICKS_AFTER_ENTRY}", "positive"),
        ("P421_FULL_DEPTH_UNIQUE_GATE_FROZEN", MIN_L2_L5_EDGE_DELTA_VS_REMOVED_PCT > 0, MIN_L2_L5_EDGE_DELTA_VS_REMOVED_PCT, ">0"),
        ("P421_FIXED_PARAMETERS_FROZEN", len(freeze) >= 11, len(freeze), ">=11"),
        ("P421_EXECUTION_HARD_GATES_PRECOMMITTED", len(exec_gates) == 12, len(exec_gates), 12),
        ("P421_RESULTS_NOT_GENERATED", as_int(values.get("execution_results_generated_now", 1)) == 0, values.get("execution_results_generated_now", ""), 0),
        ("P421_FORBIDDEN_BOUNDARIES_CLOSED", all(x in forbidden for x in ["promotion_before_phase422", "paper_live", "deployable_claim", "dropping_l2_l5_gate"]), forbidden, "closed_routes_listed"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(contract: pd.DataFrame, freeze: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase421_pair_spread_realism_retest_precommit_complete", 1, "Phase421 precommit completed"),
            ("phase421_thesis_id", THESIS_ID, "Frozen repair retest"),
            ("phase421_contract_rows", len(contract), "Contract rows"),
            ("phase421_parameter_freeze_rows", len(freeze), "Frozen parameter rows"),
            ("phase421_parameter_freeze_hash", sha256_frame(freeze), "Parameter freeze hash"),
            ("phase421_min_forward_hold_ms", MIN_FORWARD_HOLD_MS, "New timing rule"),
            ("phase421_min_forward_ticks_after_entry", MIN_FORWARD_TICKS_AFTER_ENTRY, "New timing rule"),
            ("phase421_min_l2_l5_edge_delta_vs_removed_pct", MIN_L2_L5_EDGE_DELTA_VS_REMOVED_PCT, "New full-depth unique gate"),
            ("phase421_execution_results_generated", 0, "Precommit only"),
            ("phase421_strategy_promotion_allowed", 0, "No promotion"),
            ("phase421_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase421_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase421_execution_allowed_next", int(hard_pass == hard_rows), "Whether Phase422 may run"),
            ("phase421_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase421_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase421_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, contract: pd.DataFrame, freeze: pd.DataFrame, inputs: pd.DataFrame, exec_gates: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase421 Pair-Spread Realism Retest Precommit",
        "",
        "Phase421 freezes the repair retest required by Phase420 before any new pair-spread execution.",
        "",
        "It keeps the positive lead alive while requiring minimum forward time/ticks and a full-depth unique contribution gate.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Frozen Contract",
        "",
        _markdown_table(contract),
        "",
        "## Frozen Parameters",
        "",
        _markdown_table(freeze),
        "",
        "## Input Registry",
        "",
        _markdown_table(inputs),
        "",
        "## Phase422 Hard-Gate Contract",
        "",
        _markdown_table(exec_gates),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "No Phase421 result, promotion, paper/live acceptance or deployable claim is generated.",
    ]
    (output_dir / "phase421_pair_spread_realism_retest_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase420_dir: Path = DEFAULT_PHASE420_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    summary420 = read_csv(phase420_dir / "phase420_acceptance_summary.csv")
    fd = read_csv(phase420_dir / "phase420_full_depth_contribution_audit.csv")
    timing = read_csv(phase420_dir / "phase420_timing_realism_audit.csv")
    real_anchor = read_csv(phase420_dir / "phase420_real_anchor_pair_availability.csv")
    if summary420.empty or fd.empty or timing.empty or real_anchor.empty:
        raise FileNotFoundError("Phase421 requires Phase420 audit outputs.")
    contract = build_contract()
    freeze = build_parameter_freeze()
    exec_gates = build_execution_hard_gates()
    inputs = build_input_registry(summary420, fd, timing, real_anchor)
    gates = build_gates(inputs, contract, freeze, exec_gates)
    acceptance = build_acceptance(contract, freeze, gates)
    contract.to_csv(output_dir / "phase421_frozen_contract.csv", index=False)
    freeze.to_csv(output_dir / "phase421_parameter_freeze.csv", index=False)
    inputs.to_csv(output_dir / "phase421_input_registry.csv", index=False)
    exec_gates.to_csv(output_dir / "phase421_execution_hard_gate_contract.csv", index=False)
    gates.to_csv(output_dir / "phase421_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase421_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, contract, freeze, inputs, exec_gates, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase421_pair_spread_realism_retest_precommit",
        **reproducibility_fields(
            artifact_id="phase421_pair_spread_realism_retest_precommit",
            generated_utc=generated_utc,
            inputs={"phase420_acceptance_summary": str(phase420_dir / "phase420_acceptance_summary.csv")},
            parameters={"thesis_id": THESIS_ID, "parameter_freeze_hash": sha256_frame(freeze), "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase421_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase421_precommit_min_forward_time",
        ),
    }
    (output_dir / "phase421_pair_spread_realism_retest_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase421 pair-spread realism retest precommit.")
    parser.add_argument("--phase420-dir", type=Path, default=DEFAULT_PHASE420_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase420_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
