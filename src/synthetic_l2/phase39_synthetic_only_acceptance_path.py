from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


BROKER_BLOCKER_GATES = [
    "zerodha_real_fill_required_for_synthetic_only",
    "contract_note_required_for_synthetic_only",
    "broker_reconciliation_required_for_synthetic_only",
]


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def _metric(frame: pd.DataFrame, metric: str) -> int:
    matched = frame[frame["metric"].astype(str).eq(metric)]
    if matched.empty:
        raise KeyError(metric)
    return int(matched["value"].iloc[0])


def _boolish(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def _strategy_replay_rollup(strategy_id: str, phase25_summary: pd.DataFrame, phase29_summary: pd.DataFrame) -> dict[str, object]:
    p25 = phase25_summary[
        phase25_summary["model_id"].astype(str).eq(strategy_id)
        & phase25_summary["model_type"].astype(str).eq("strategy")
    ]
    p29 = phase29_summary[phase29_summary["model_id"].astype(str).eq(strategy_id)]
    frames = []
    if len(p25):
        frames.append(("phase25_event_order_replay", p25))
    if len(p29):
        frames.append(("phase29_partial_proxy_replay", p29))
    if not frames:
        return {
            "synthetic_replay_source": "none",
            "synthetic_trade_rows": 0,
            "execution_profiles": 0,
            "positive_after_cost_profiles": 0,
            "realistic_positive_profiles": 0,
            "best_mean_net_return": 0.0,
        }

    combined = pd.concat([frame.assign(_source=source) for source, frame in frames], ignore_index=True)
    realistic = combined[combined["execution_profile"].astype(str).isin(["retail_marketable_default", "stressed_retail"])]
    return {
        "synthetic_replay_source": "+".join(source for source, _ in frames),
        "synthetic_trade_rows": int(combined["trades"].sum()),
        "execution_profiles": int(combined["execution_profile"].nunique()),
        "positive_after_cost_profiles": int((combined["mean_net_return"] > 0).sum()),
        "realistic_positive_profiles": int((realistic["mean_net_return"] > 0).sum()),
        "best_mean_net_return": float(combined["mean_net_return"].max()),
    }


def build_policy(phase25_overall: pd.DataFrame, phase29_overall: pd.DataFrame, phase38_summary: pd.DataFrame) -> pd.DataFrame:
    phase25_trades = _metric(phase25_overall, "phase25_total_trades")
    phase29_trades = _metric(phase29_overall, "phase29_total_replay_trades")
    phase25_positive = _metric(phase25_overall, "phase25_positive_strategy_profile_rows")
    phase29_realistic_positive = _metric(phase29_overall, "phase29_realistic_positive_rows")
    class_b_days = _metric(phase38_summary, "phase38_class_b_promoted_days")

    rows = [
        {
            "policy_id": "synthetic_experiment_continuation",
            "allowed": bool(phase25_trades + phase29_trades > 0),
            "acceptance_scope": "synthetic_only_experiment",
            "evidence_status": "allowed_without_zerodha_fills_or_contract_notes",
            "observed_value": f"{phase25_trades + phase29_trades} synthetic/proxy replay trade rows available",
            "boundary": "May run experiments/redesign diagnostics; does not promote strategies or imply broker readiness.",
        },
        {
            "policy_id": "synthetic_strategy_acceptance",
            "allowed": bool(phase25_positive > 0 or phase29_realistic_positive > 0),
            "acceptance_scope": "synthetic_only_strategy_promotion",
            "evidence_status": "blocked_by_current_strategy_economics",
            "observed_value": f"phase25_positive_profiles={phase25_positive}; phase29_realistic_positive_profiles={phase29_realistic_positive}",
            "boundary": "No current alpha strategy may be accepted until synthetic replay clears positive after-cost economics.",
        },
        {
            "policy_id": "paper_or_live_broker_acceptance",
            "allowed": False,
            "acceptance_scope": "real_broker_or_paper_live",
            "evidence_status": "blocked_by_missing_zerodha_fills_and_contract_notes",
            "observed_value": "Zerodha fills/contract notes are unavailable for this experiment path",
            "boundary": "Broker/paper/live readiness remains closed; broker reconciliation is not waived outside synthetic-only scope.",
        },
        {
            "policy_id": "class_b_real_data_replay_acceptance",
            "allowed": bool(class_b_days > 0),
            "acceptance_scope": "real_l2_multiday_acceptance",
            "evidence_status": "blocked_by_phase38_class_b_gate" if class_b_days == 0 else "available_for_real_data_acceptance_replay",
            "observed_value": f"phase38_class_b_promoted_days={class_b_days}",
            "boundary": "Real-data acceptance replay still requires promoted Class B days and remains separate from synthetic-only experiments.",
        },
    ]
    return pd.DataFrame(rows)


def build_gate_ledger(policy: pd.DataFrame, phase25_overall: pd.DataFrame, phase29_overall: pd.DataFrame) -> pd.DataFrame:
    phase25_trades = _metric(phase25_overall, "phase25_total_trades")
    phase29_trades = _metric(phase29_overall, "phase29_total_replay_trades")
    phase25_positive = _metric(phase25_overall, "phase25_positive_strategy_profile_rows")
    phase29_positive = _metric(phase29_overall, "phase29_realistic_positive_rows")
    rows = [
        {
            "gate_id": "synthetic_only_scope_declared",
            "gate_group": "scope",
            "passed_for_synthetic_experiments": True,
            "passed_for_strategy_acceptance": False,
            "observed_value": "synthetic-only acceptance path selected because Zerodha fills/contract notes are unavailable",
            "required_next_action": "",
        },
        {
            "gate_id": "synthetic_event_replay_available",
            "gate_group": "synthetic_evidence",
            "passed_for_synthetic_experiments": bool(phase25_trades + phase29_trades > 0),
            "passed_for_strategy_acceptance": False,
            "observed_value": f"phase25_trades={phase25_trades}; phase29_trades={phase29_trades}",
            "required_next_action": "" if phase25_trades + phase29_trades > 0 else "Run synthetic event replay before experiments continue.",
        },
        {
            "gate_id": "positive_after_cost_economics",
            "gate_group": "economics",
            "passed_for_synthetic_experiments": True,
            "passed_for_strategy_acceptance": bool(phase25_positive > 0 or phase29_positive > 0),
            "observed_value": f"phase25_positive_profiles={phase25_positive}; phase29_realistic_positive_profiles={phase29_positive}",
            "required_next_action": "Redesign strategy signals/labels until synthetic replay clears after-cost economics.",
        },
    ]
    for gate_id in BROKER_BLOCKER_GATES:
        rows.append(
            {
                "gate_id": gate_id,
                "gate_group": "broker_evidence_deferred",
                "passed_for_synthetic_experiments": True,
                "passed_for_strategy_acceptance": False,
                "observed_value": "deferred only inside synthetic-only experiment scope",
                "required_next_action": "Provide Zerodha fill/contract-note/reconciliation evidence before broker, paper, or live readiness.",
            }
        )
    rows.append(
        {
            "gate_id": "real_broker_or_paper_acceptance_closed",
            "gate_group": "broker_boundary",
            "passed_for_synthetic_experiments": True,
            "passed_for_strategy_acceptance": False,
            "observed_value": "synthetic-only path does not claim real fill quality or contract-note cost reconciliation",
            "required_next_action": "Keep broker acceptance closed until real execution artifacts exist.",
        }
    )
    return pd.DataFrame(rows)


def build_strategy_decisions(decisions: pd.DataFrame, phase25_summary: pd.DataFrame, phase29_summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for record in decisions.to_dict("records"):
        strategy_id = str(record["strategy_id"])
        rollup = _strategy_replay_rollup(strategy_id, phase25_summary, phase29_summary)
        evidence_scope = str(record.get("evidence_scope", ""))
        is_alpha = not evidence_scope.startswith("non_alpha")
        synthetic_replay_available = int(rollup["synthetic_trade_rows"]) > 0
        realistic_positive = int(rollup["realistic_positive_profiles"]) > 0
        experiment_allowed = bool(synthetic_replay_available or not is_alpha)
        if is_alpha and synthetic_replay_available:
            experiment_status = "synthetic_experiment_allowed_redesign_required"
            next_action = "Continue synthetic-only redesign/diagnostics; do not promote until realistic after-cost replay turns positive."
        elif is_alpha:
            experiment_status = "hypothesis_only_no_current_synthetic_replay"
            next_action = "Add a synthetic replayable signal/label before spending more acceptance compute."
        else:
            experiment_status = "control_or_risk_plumbing_allowed"
            next_action = "Use only as execution/risk control plumbing; exclude from alpha promotion."
        rows.append(
            {
                "strategy_id": strategy_id,
                "strategy_name": record.get("strategy_name", ""),
                "evidence_scope": evidence_scope,
                "current_decision": record.get("current_decision", ""),
                "synthetic_experiment_allowed": experiment_allowed,
                "synthetic_strategy_acceptance_ready": bool(_boolish(record.get("acceptance_ready", False)) and realistic_positive),
                "paper_or_live_acceptance_ready": False,
                "synthetic_replay_available": synthetic_replay_available,
                "synthetic_replay_source": rollup["synthetic_replay_source"],
                "synthetic_trade_rows": rollup["synthetic_trade_rows"],
                "execution_profiles": rollup["execution_profiles"],
                "positive_after_cost_profiles": rollup["positive_after_cost_profiles"],
                "realistic_positive_profiles": rollup["realistic_positive_profiles"],
                "best_mean_net_return": rollup["best_mean_net_return"],
                "experiment_status": experiment_status,
                "next_action": next_action,
            }
        )
    return pd.DataFrame(rows).sort_values(["synthetic_experiment_allowed", "strategy_id"], ascending=[False, True], kind="mergesort")


def build_experiment_queue(strategy_decision: pd.DataFrame) -> pd.DataFrame:
    allowed = strategy_decision[strategy_decision["synthetic_experiment_allowed"].astype(bool)].copy()
    rows = []
    for priority, record in enumerate(allowed.to_dict("records"), start=1):
        if str(record["evidence_scope"]).startswith("non_alpha"):
            track = "control_risk_plumbing"
        elif int(record["synthetic_trade_rows"]) > 0:
            track = "alpha_redesign_diagnostics"
        else:
            track = "hypothesis_backlog"
        rows.append(
            {
                "priority": priority,
                "strategy_id": record["strategy_id"],
                "strategy_name": record["strategy_name"],
                "experiment_track": track,
                "allowed_scope": "synthetic_only",
                "must_not_claim": "paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation",
                "synthetic_trade_rows": int(record["synthetic_trade_rows"]),
                "next_action": record["next_action"],
            }
        )
    return pd.DataFrame(rows)


def build_summary(policy: pd.DataFrame, gate_ledger: pd.DataFrame, strategy_decision: pd.DataFrame) -> pd.DataFrame:
    alpha = strategy_decision[~strategy_decision["evidence_scope"].astype(str).str.startswith("non_alpha")]
    rows = [
        ("phase39_policy_rows", int(len(policy)), "Synthetic-only acceptance policy rows"),
        ("phase39_gate_rows", int(len(gate_ledger)), "Synthetic-only gate ledger rows"),
        ("phase39_broker_blockers_deferred_for_synthetic_only", int(gate_ledger["gate_group"].eq("broker_evidence_deferred").sum()), "Broker evidence gates deferred only for synthetic-only experiments"),
        ("phase39_strategies_evaluated", int(len(strategy_decision)), "Strategy/control families evaluated"),
        ("phase39_alpha_strategies_evaluated", int(len(alpha)), "Alpha strategy families evaluated"),
        ("phase39_synthetic_experiment_allowed_strategies", int(strategy_decision["synthetic_experiment_allowed"].astype(bool).sum()), "Families allowed to continue in synthetic-only experiments"),
        ("phase39_synthetic_strategy_acceptance_ready", int(strategy_decision["synthetic_strategy_acceptance_ready"].astype(bool).sum()), "Families accepted for synthetic-only strategy promotion"),
        ("phase39_paper_or_live_acceptance_ready", int(strategy_decision["paper_or_live_acceptance_ready"].astype(bool).sum()), "Families ready for paper/live broker acceptance"),
        ("phase39_synthetic_replay_available_strategies", int(strategy_decision["synthetic_replay_available"].astype(bool).sum()), "Families with current synthetic replay artifacts"),
        ("phase39_total_existing_synthetic_replay_trades", int(strategy_decision["synthetic_trade_rows"].sum()), "Existing strategy/control synthetic/proxy replay trade rows available"),
        ("phase39_realistic_positive_strategy_rows", int(strategy_decision["realistic_positive_profiles"].gt(0).sum()), "Families with at least one realistic positive profile"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase 39 Synthetic-Only Acceptance Path",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This phase records the explicit synthetic-only path selected because Zerodha fills and contract notes are unavailable.",
        "It allows controlled synthetic experiments and redesign diagnostics to continue, but it does not promote current strategies and does not open paper/live broker readiness.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase39_synthetic_only_acceptance_path_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase39(paths: dict[str, Path], output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    decisions = _read_csv(paths["phase30_decision_ledger"])
    phase25_summary = _read_csv(paths["phase25_summary"])
    phase25_overall = _read_csv(paths["phase25_overall"])
    phase29_summary = _read_csv(paths["phase29_summary"])
    phase29_overall = _read_csv(paths["phase29_overall"])
    phase38_summary = _read_csv(paths["phase38_summary"])

    policy = build_policy(phase25_overall, phase29_overall, phase38_summary)
    gate_ledger = build_gate_ledger(policy, phase25_overall, phase29_overall)
    strategy_decision = build_strategy_decisions(decisions, phase25_summary, phase29_summary)
    experiment_queue = build_experiment_queue(strategy_decision)
    summary = build_summary(policy, gate_ledger, strategy_decision)

    frames = {
        "Summary": summary,
        "Policy": policy,
        "Gate Ledger": gate_ledger,
        "Strategy Decisions": strategy_decision,
        "Experiment Queue": experiment_queue,
    }
    summary.to_csv(output_dir / "synthetic_only_acceptance_summary.csv", index=False)
    policy.to_csv(output_dir / "synthetic_only_acceptance_policy.csv", index=False)
    gate_ledger.to_csv(output_dir / "synthetic_only_gate_ledger.csv", index=False)
    strategy_decision.to_csv(output_dir / "synthetic_only_strategy_decision.csv", index=False)
    experiment_queue.to_csv(output_dir / "synthetic_only_experiment_queue.csv", index=False)
    write_report(output_dir, frames)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase39_synthetic_only_experiment_path_not_broker_acceptance",
        "synthetic_experiment_allowed_strategies": int(strategy_decision["synthetic_experiment_allowed"].astype(bool).sum()),
        "synthetic_strategy_acceptance_ready": int(strategy_decision["synthetic_strategy_acceptance_ready"].astype(bool).sum()),
        "paper_or_live_acceptance_ready": int(strategy_decision["paper_or_live_acceptance_ready"].astype(bool).sum()),
        "broker_evidence_deferred_only_for_synthetic_scope": True,
        "not_paper_or_live_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase39",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={
                "acceptance_path": "synthetic_only",
                "broker_evidence_semantics": "zerodha_fills_contract_notes_deferred_only_for_synthetic_experiments",
                "strategy_acceptance_rule": "must_have_realistic_positive_after_cost_synthetic_replay",
                "paper_live_rule": "always_false_without_real_fills_and_contract_notes",
            },
            outputs={
                "summary": str(output_dir / "synthetic_only_acceptance_summary.csv"),
                "policy": str(output_dir / "synthetic_only_acceptance_policy.csv"),
                "gate_ledger": str(output_dir / "synthetic_only_gate_ledger.csv"),
                "strategy_decision": str(output_dir / "synthetic_only_strategy_decision.csv"),
                "experiment_queue": str(output_dir / "synthetic_only_experiment_queue.csv"),
                "report": str(output_dir / "phase39_synthetic_only_acceptance_path_report.md"),
                "manifest": str(output_dir / "phase39_synthetic_only_acceptance_path_manifest.json"),
            },
            random_seed="none_deterministic_synthetic_only_acceptance_path",
            scenario_ids="current_phase25_phase29_phase30_phase38_synthetic_only_path",
            cost_model_version="existing_phase25_phase29_zerodha_cost_profiles",
            latency_model_version="existing_phase25_phase29_execution_profiles",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase39_synthetic_only_acceptance_path_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Phase 39 synthetic-only acceptance path artifacts.")
    parser.add_argument("--phase30-decision-ledger", type=Path, default=Path("outputs/phase30/strategy_family_decision_ledger.csv"))
    parser.add_argument("--phase25-summary", type=Path, default=Path("outputs/phase25/event_replay_summary.csv"))
    parser.add_argument("--phase25-overall", type=Path, default=Path("outputs/phase25/event_replay_overall_summary.csv"))
    parser.add_argument("--phase29-summary", type=Path, default=Path("outputs/phase29/partial_strategy_proxy_summary.csv"))
    parser.add_argument("--phase29-overall", type=Path, default=Path("outputs/phase29/partial_strategy_proxy_overall_summary.csv"))
    parser.add_argument("--phase38-summary", type=Path, default=Path("outputs/phase38/class_b_promotion_summary.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase39"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase39(
        {
            "phase30_decision_ledger": args.phase30_decision_ledger,
            "phase25_summary": args.phase25_summary,
            "phase25_overall": args.phase25_overall,
            "phase29_summary": args.phase29_summary,
            "phase29_overall": args.phase29_overall,
            "phase38_summary": args.phase38_summary,
        },
        args.output_dir,
        args.base_dir,
    )


if __name__ == "__main__":
    main()
