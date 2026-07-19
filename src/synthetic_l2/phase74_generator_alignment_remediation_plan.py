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


DEFAULT_OUTPUT_DIR = Path("outputs/phase74")


def metric_value(path: Path, metric: str, default: Any = None) -> Any:
    frame = pd.read_csv(path)
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    value = rows.iloc[0]
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def build_remediation_actions() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "priority": 1,
                "remediation_id": "R74_timestamp_unit_contract",
                "area": "timestamp_alignment",
                "issue": "Dense lake column callback_received_utc_ms behaves like seconds in generated data despite the _ms suffix.",
                "required_change": "Add a timestamp unit contract artifact and validator that reports observed min/max deltas and names the alignment unit used by every cross-symbol study.",
                "acceptance_gate": "Timestamp unit inferred consistently for every symbol partition in the target month; mismatches fail the run.",
                "unblocks": "Reliable cross-symbol alignment and replay comparability.",
            },
            {
                "priority": 2,
                "remediation_id": "R74_synchronous_cross_symbol_bars",
                "area": "cross_symbol_alignment",
                "issue": "Phase70 used per-symbol event bars; Phase73 timestamp recheck stayed positive but failed precision.",
                "required_change": "Build a reusable timestamp-aligned matrix with coverage/staleness diagnostics and target-side tradability filters.",
                "acceptance_gate": "At least 95% of selected symbol/bucket cells have fresh observations within the declared staleness limit.",
                "unblocks": "A cleaner HDFCBANK lead-lag refinement without sequence-alignment ambiguity.",
            },
            {
                "priority": 3,
                "remediation_id": "R74_shock_panel_balance",
                "area": "shock_scenarios",
                "issue": "Phase73 found shock coverage concentrated in one audited month.",
                "required_change": "Create or select a scenario-balanced shock panel with multiple market-shock and symbol-shock months before replaying shock rules.",
                "acceptance_gate": "At least two market-shock months and at least two symbol-shock months with two or more shocked symbols each.",
                "unblocks": "Retesting Phase71 shock mean-reversion without one-scenario concentration.",
            },
            {
                "priority": 4,
                "remediation_id": "R74_cost_drag_filter",
                "area": "execution_costs",
                "issue": "Positive near-misses still lose too much gross edge to costs or fail precision gates.",
                "required_change": "Add pre-trade filters that reject candidate rules where validation cost drag exceeds 50% of absolute gross edge.",
                "acceptance_gate": "Every promoted candidate reports gross edge, cost drag, precision and target/month stability before replay.",
                "unblocks": "Prevents expensive replay of rules that are technically positive but operationally fragile.",
            },
        ]
    )


def build_retest_queue() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "retest_id": "RT74_hdfcbank_timestamp_refinement",
                "source_near_miss": "NM70_HDFCBANK_LEAD_LAG",
                "allowed_after": "R74_timestamp_unit_contract,R74_synchronous_cross_symbol_bars,R74_cost_drag_filter",
                "experiment": "Refine HDFCBANK lead-lag with timestamp bars, staleness filtering, lower-turnover thresholds and disjoint-month validation.",
                "not_allowed_yet": "No direct full-year replay from Phase70/73 because precision is below gate.",
            },
            {
                "retest_id": "RT74_market_shock_mean_reversion",
                "source_near_miss": "NM71_MARKET_SHOCK_MEAN_REVERSION",
                "allowed_after": "R74_shock_panel_balance,R74_cost_drag_filter",
                "experiment": "Retest market-shock mean reversion on a balanced shock panel with enough trade count and matched no-shock controls.",
                "not_allowed_yet": "No direct replay from Phase71 because trade count was below the predeclared minimum.",
            },
        ]
    )


def build_acceptance_summary(base_dir: Path, actions: pd.DataFrame, retests: pd.DataFrame) -> pd.DataFrame:
    phase73 = base_dir / "outputs/phase73/timestamp_alignment_shock_panel_acceptance_summary.csv"
    return pd.DataFrame(
        [
            ("phase74_source_phase73_allow_replay_expansion", int(metric_value(phase73, "phase73_allow_replay_expansion", 0)), "Phase73 replay-expansion gate"),
            ("phase74_remediation_actions", int(len(actions)), "Concrete remediation actions declared"),
            ("phase74_retest_queue_items", int(len(retests)), "Near-miss retests queued behind remediation gates"),
            ("phase74_allow_replay_expansion_now", 0, "0 means no near-miss replay expansion before remediation gates pass"),
            ("phase74_next_implementation", "timestamp_unit_contract_and_synchronous_matrix_validator", "Next implementation step"),
            ("phase74_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model retained for future gates"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase74 Generator and Alignment Remediation Plan",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase74 turns the Phase73 audit into implementation requirements.",
        "It keeps replay expansion closed until timestamp alignment, shock-panel balance and cost-drag gates are remediated.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase74_generator_alignment_remediation_plan_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase74(base_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    actions = build_remediation_actions()
    retests = build_retest_queue()
    acceptance = build_acceptance_summary(base_dir, actions, retests)

    actions.to_csv(output_dir / "remediation_action_plan.csv", index=False)
    retests.to_csv(output_dir / "near_miss_retest_queue.csv", index=False)
    acceptance.to_csv(output_dir / "remediation_acceptance_summary.csv", index=False)
    write_report(output_dir, {"Acceptance Summary": acceptance, "Remediation Action Plan": actions, "Near-Miss Retest Queue": retests})

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase74_generator_alignment_remediation_plan",
        "allow_replay_expansion_now": 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase74",
            generated_utc=generated_utc,
            inputs={
                "phase72_audit": "outputs/phase72/research_audit_acceptance_summary.csv",
                "phase73_acceptance": "outputs/phase73/timestamp_alignment_shock_panel_acceptance_summary.csv",
            },
            parameters={"decision_rule": "declare_remediation_gates_before_near_miss_replay_expansion"},
            outputs={
                "remediation_action_plan": str(output_dir / "remediation_action_plan.csv"),
                "near_miss_retest_queue": str(output_dir / "near_miss_retest_queue.csv"),
                "acceptance_summary": str(output_dir / "remediation_acceptance_summary.csv"),
                "report": str(output_dir / "phase74_generator_alignment_remediation_plan_report.md"),
                "manifest": str(output_dir / "phase74_generator_alignment_remediation_plan_manifest.json"),
            },
            random_seed="none_deterministic_remediation_plan",
            scenario_ids="phase74_post_phase73_remediation",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_remediation_plan",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase74_generator_alignment_remediation_plan_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase74 generator/alignment remediation plan.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase74(args.base_dir, args.output_dir)


if __name__ == "__main__":
    main()
