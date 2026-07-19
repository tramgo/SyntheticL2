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


DEFAULT_OUTPUT_DIR = Path("outputs/phase78")
DEFAULT_PHASE72_DIR = Path("outputs/phase72")
DEFAULT_PHASE77_DIR = Path("outputs/phase77")


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    match = frame[frame["metric"].eq(metric)]
    if match.empty:
        return default
    return match.iloc[0]["value"]


def build_decision_ledger(phase72_family: pd.DataFrame, phase77_acceptance: pd.DataFrame) -> pd.DataFrame:
    total_net = float(metric_value(phase77_acceptance, "phase77_total_net_pnl_inr", 0.0))
    positive_month_fraction = float(metric_value(phase77_acceptance, "phase77_positive_month_fraction", 0.0))
    pass_month_fraction = float(metric_value(phase77_acceptance, "phase77_pass_month_fraction", 0.0))
    hdfcbank_pass = int(float(metric_value(phase77_acceptance, "phase77_hdfcbank_disjoint_retest_pass", 0)))
    prior_retired = int(phase72_family["deployable"].astype(str).str.lower().eq("false").sum()) if not phase72_family.empty else 0
    return pd.DataFrame(
        [
            {
                "research_branch": "hdfcbank_cross_symbol_lead_lag",
                "source_phases": "70,73,76,77",
                "decision": "retired_after_disjoint_falsification" if hdfcbank_pass == 0 else "eligible_for_controlled_expansion",
                "deployable": False if hdfcbank_pass == 0 else True,
                "evidence": (
                    f"Phase77 non-January retest total_net_pnl_inr={total_net:.2f}, "
                    f"positive_month_fraction={positive_month_fraction:.2f}, pass_month_fraction={pass_month_fraction:.2f}."
                ),
                "primary_failure_mode": "positive_january_common_overlap_pocket_did_not_repeat_out_of_sample"
                if hdfcbank_pass == 0
                else "none_at_phase78_gate",
                "allowed_next_action": "do_not_expand_more_shards_for_this_rule; redesign_features_or_generator_assumptions_first"
                if hdfcbank_pass == 0
                else "expand_with_position_sizing_drawdown_and_disjoint_day_controls",
            },
            {
                "research_branch": "broad_dense_marketable_strategy_mining",
                "source_phases": "52,53,54,55,56,57,58,59,60,61,62,63,64,72",
                "decision": "closed_to_blind_shard_replay",
                "deployable": False,
                "evidence": f"Phase72 audit recorded {prior_retired} non-deployable/retired rows before the HDFCBANK retest.",
                "primary_failure_mode": "cost_drag_and_non_repeating_synthetic_edges",
                "allowed_next_action": "only_resume_after_new_signal_class_has_precommitted_falsification_gate",
            },
            {
                "research_branch": "synthetic_generator_realism_and_feature_redesign",
                "source_phases": "72,74,75,76,77",
                "decision": "next_active_research_branch",
                "deployable": False,
                "evidence": "Timestamp contracts and common-overlap matrices can now be built; strategy edges still fail disjoint survival.",
                "primary_failure_mode": "strategy_search_outpaced_generator_assumption_validation",
                "allowed_next_action": "audit_generator_scenario_diversity_and_design_new_signal_classes_before_more_replay_volume",
            },
        ]
    )


def build_next_queue() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "priority": 1,
                "next_action_id": "P79_generator_scenario_diversity_audit",
                "objective": "Quantify whether synthetic months are diverse enough in shocks, trend/fade regimes, spread states, and cross-symbol correlation to support strategy falsification.",
                "why_now": "Phase77 shows a January edge did not repeat; before more strategies, verify whether generator scenarios are rich or merely producing isolated pockets.",
                "acceptance_gate": "scenario coverage table passes minimum diversity thresholds; otherwise generator calibration is the blocker.",
            },
            {
                "priority": 2,
                "next_action_id": "P80_cost_budget_signal_design",
                "objective": "Derive minimum required gross edge by symbol/month under Zerodha costs, spread, slippage and impact, then filter future labels before strategy replay.",
                "why_now": "Most failed branches were gross-signal-too-small relative to costs.",
                "acceptance_gate": "future candidate labels must clear ex-ante cost-budget thresholds before any replay expansion.",
            },
            {
                "priority": 3,
                "next_action_id": "P81_new_signal_family_precommit",
                "objective": "Precommit one new signal family that uses stronger regime context rather than dense taker momentum alone.",
                "why_now": "Continuing HDFCBANK lead-lag or passive imbalance as-is is now negative expected research value.",
                "acceptance_gate": "disjoint-month and adverse-selection gates specified before mining results are inspected.",
            },
        ]
    )


def summarize(decision_ledger: pd.DataFrame, next_queue: pd.DataFrame) -> pd.DataFrame:
    retired = int(decision_ledger["decision"].astype(str).str.contains("retired|closed", regex=True).sum())
    active = int(decision_ledger["decision"].astype(str).eq("next_active_research_branch").sum())
    return pd.DataFrame(
        [
            ("phase78_decision_rows", int(len(decision_ledger)), "Research branch decisions recorded"),
            ("phase78_retired_or_closed_rows", retired, "Branches retired or closed to blind replay"),
            ("phase78_active_research_rows", active, "Branches allowed as next active research work"),
            ("phase78_next_queue_rows", int(len(next_queue)), "Prioritized next actions"),
            ("phase78_broad_shard_replay_allowed", 0, "1 means more broad shard replay is allowed immediately"),
            ("phase78_recommend_next_action", "P79_generator_scenario_diversity_audit", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase78 Post-Falsification Research Gate",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase78 records the research decision after Phase77 falsified the HDFCBANK lead-lag clue out of sample.",
        "It prevents broad shard replay from becoming the default next step without a redesigned signal or generator-realism gate.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase78_post_falsification_research_gate_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase78(phase72_dir: Path, phase77_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase72_family = pd.read_csv(phase72_dir / "research_family_audit.csv")
    phase77_acceptance = pd.read_csv(phase77_dir / "disjoint_month_acceptance_summary.csv")
    decision_ledger = build_decision_ledger(phase72_family, phase77_acceptance)
    next_queue = build_next_queue()
    acceptance = summarize(decision_ledger, next_queue)

    decision_ledger.to_csv(output_dir / "post_falsification_decision_ledger.csv", index=False)
    next_queue.to_csv(output_dir / "next_research_queue.csv", index=False)
    acceptance.to_csv(output_dir / "post_falsification_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Post-Falsification Decision Ledger": decision_ledger,
            "Next Research Queue": next_queue,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {"generated_utc": generated_utc, "scope": "phase78_post_falsification_research_gate"}
    manifest.update(
        reproducibility_fields(
            artifact_id="phase78",
            generated_utc=generated_utc,
            inputs={
                "phase72_family_audit": str(phase72_dir / "research_family_audit.csv"),
                "phase77_acceptance_summary": str(phase77_dir / "disjoint_month_acceptance_summary.csv"),
            },
            parameters={
                "broad_shard_replay_policy": "disallowed_after_phase77_failure_until_new_signal_or_generator_gate",
                "next_queue_policy": "scenario_diversity_then_cost_budget_then_new_signal_precommit",
            },
            outputs={
                "decision_ledger": str(output_dir / "post_falsification_decision_ledger.csv"),
                "next_research_queue": str(output_dir / "next_research_queue.csv"),
                "acceptance_summary": str(output_dir / "post_falsification_acceptance_summary.csv"),
                "report": str(output_dir / "phase78_post_falsification_research_gate_report.md"),
                "manifest": str(output_dir / "phase78_post_falsification_research_gate_manifest.json"),
            },
            random_seed="none_deterministic_research_gate",
            scenario_ids="phase78_post_phase77_research_decision",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_decision_gate",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase78_post_falsification_research_gate_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record post-Phase77 research branch decision and next queue.")
    parser.add_argument("--phase72-dir", type=Path, default=DEFAULT_PHASE72_DIR)
    parser.add_argument("--phase77-dir", type=Path, default=DEFAULT_PHASE77_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase78(args.phase72_dir, args.phase77_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
