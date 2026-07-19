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


DEFAULT_OUTPUT_DIR = Path("outputs/phase118")
DEFAULT_PHASE66_DIR = Path("outputs/phase66")
DEFAULT_PHASE67_DIR = Path("outputs/phase67")
DEFAULT_PHASE68_DIR = Path("outputs/phase68")
DEFAULT_PHASE69_DIR = Path("outputs/phase69")
DEFAULT_PHASE89_DIR = Path("outputs/phase89")
DEFAULT_PHASE116_DIR = Path("outputs/phase116")
DEFAULT_PHASE117_DIR = Path("outputs/phase117")


def read_metric_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["metric", "value", "description"])
    return pd.read_csv(path)


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


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    return int(round(as_float(value, float(default))))


def build_label_failure_ledger(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    p66 = tables["phase66"]
    p67 = tables["phase67"]
    p68 = tables["phase68"]
    p69 = tables["phase69"]
    p89 = tables["phase89"]
    return pd.DataFrame(
        [
            {
                "evidence_id": "P66_PASSIVE_ADVERSE_SELECTION_LABELS",
                "scope": "simple join/fade passive imbalance labels",
                "rows_or_candidates": as_int(metric_value(p66, "phase66_candidate_orders")),
                "candidate_rows": as_int(metric_value(p66, "phase66_label_candidate_rows")),
                "best_after_cost_bps": as_float(metric_value(p66, "phase66_best_mean_after_cost_bps_if_touched")),
                "survives_gate": 0,
                "decision": "simple_passive_imbalance_labels_failed",
            },
            {
                "evidence_id": "P67_FEATURE_DESIGN_BUDGET",
                "scope": "post-Phase66 feature-design budget gate",
                "rows_or_candidates": as_int(metric_value(p67, "phase67_feature_families_queued")),
                "candidate_rows": as_int(metric_value(p67, "phase67_allow_full_year_replay_now")),
                "best_after_cost_bps": as_float(metric_value(p67, "phase67_source_phase66_best_after_cost_bps")),
                "survives_gate": as_int(metric_value(p67, "phase67_allow_full_year_replay_now")),
                "decision": "full_year_replay_blocked_by_budget_gate",
            },
            {
                "evidence_id": "P68_REPLENISHMENT_AFTER_TOUCH",
                "scope": "post-touch replenishment labels",
                "rows_or_candidates": as_int(metric_value(p68, "phase68_inferred_touches")),
                "candidate_rows": as_int(metric_value(p68, "phase68_label_candidate_rows")),
                "best_after_cost_bps": as_float(metric_value(p68, "phase68_best_mean_after_cost_bps_if_touched")),
                "survives_gate": 0,
                "decision": "replenishment_label_gate_failed",
            },
            {
                "evidence_id": "P69_SPREAD_TRANSITION_LABELS",
                "scope": "spread compression/expansion transition labels",
                "rows_or_candidates": as_int(metric_value(p69, "phase69_signal_rows")),
                "candidate_rows": as_int(metric_value(p69, "phase69_label_candidate_rows")),
                "best_after_cost_bps": as_float(metric_value(p69, "phase69_best_mean_after_cost_bps")),
                "survives_gate": as_int(metric_value(p69, "phase69_survives_spread_transition_gate")),
                "decision": "spread_transition_label_gate_failed",
            },
            {
                "evidence_id": "P89_SIMPLE_PASSIVE_QUEUE_COST_FLOOR",
                "scope": "simple passive queue expected-value replay under pessimistic/base/optimistic fills",
                "rows_or_candidates": as_int(metric_value(p89, "phase89_fill_assumption_rows")),
                "candidate_rows": as_int(metric_value(p89, "phase89_all_assumption_survivor_candidates")),
                "best_after_cost_bps": None,
                "best_expected_net_pnl_inr": as_float(metric_value(p89, "phase89_best_test_expected_net_pnl_inr")),
                "survives_gate": as_int(metric_value(p89, "phase89_passive_queue_cost_floor_pass")),
                "decision": "simple_passive_queue_replay_failed",
            },
        ]
    )


def build_richer_passive_feature_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "feature_family_id": "P118_QUEUE_RECOVERY_AFTER_ADVERSE_TOUCH",
                "hypothesis": "A passive fill is only acceptable after an adverse touch if L1/L5 replenishment and spread non-expansion jointly indicate queue recovery.",
                "uses_prior_failed_evidence": "P66 adverse-selection labels; P68 replenishment labels; P69 spread-transition labels",
                "allowed_features": "pre-touch imbalance bucket, replenishment bucket, spread transition bucket, event intensity bucket, time-of-day bucket, symbol liquidity tier",
                "forbidden_features": "future return, realized next-bar P&L, post-entry labels unavailable at order decision time",
                "direction_policy": "maker only; quote on the side implied by precommitted queue-recovery condition",
                "turnover_policy": "low turnover only; no dense event-by-event marketable conversion",
            },
            {
                "feature_family_id": "P118_SPREAD_COMPRESSION_MAKER_ONLY",
                "hypothesis": "When spread expansion is followed by reliable compression without adverse markout, a maker order may earn spread without paying the taker spread penalty.",
                "uses_prior_failed_evidence": "P69 spread-transition labels; P89 passive queue cost floor",
                "allowed_features": "spread transition state, recent spread percentile, depth imbalance persistence, shock flag, symbol liquidity tier",
                "forbidden_features": "candidate ranking by test P&L or optimistic-only fill results",
                "direction_policy": "maker only; no crossing; stale quote cancellation mandatory",
                "turnover_policy": "one candidate per symbol per event-window; daily order budget capped before replay",
            },
            {
                "feature_family_id": "P118_REPLENISHMENT_STABILITY_FILTER",
                "hypothesis": "Passive fills are least toxic where post-touch replenishment is stable across train months and adverse-selection labels are below a strict ceiling.",
                "uses_prior_failed_evidence": "P68 replenishment buckets; P66 passive adverse-selection buckets",
                "allowed_features": "replenishment bucket stability, adverse-selection bucket, depth rebuild rate, symbol liquidity tier",
                "forbidden_features": "single-symbol pocket selection, threshold widening after replay, HDFCBANK-only revival",
                "direction_policy": "maker only; side chosen by pre-touch label family",
                "turnover_policy": "must survive minimum symbol/month breadth before any replay expansion",
            },
        ]
    )


def build_pre_replay_feasibility_gates() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "gate_id": "P118_NO_PNL_SELECTION",
                "stage": "pre_replay",
                "requirement": "Candidate filters must be selected from label quality and train-only feature distributions, not directional P&L.",
                "pass_threshold": "no test P&L field used in candidate construction",
                "failure_action": "discard candidate spec and rewrite precommit",
            },
            {
                "gate_id": "P118_ADVERSE_SELECTION_CEILING",
                "stage": "pre_replay",
                "requirement": "Candidate buckets must show materially lower adverse-selection risk than simple Phase66/68 labels.",
                "pass_threshold": "train adverse-selection rate <= 0.45 and at least 10 percentage points below simple passive baseline",
                "failure_action": "do not run replay",
            },
            {
                "gate_id": "P118_REPLENISHMENT_AND_SPREAD_CONFIRMATION",
                "stage": "pre_replay",
                "requirement": "Candidate must combine replenishment and non-expanding/compressing spread context.",
                "pass_threshold": "replenishment stability pass == 1 and spread non-expansion/compression pass == 1",
                "failure_action": "keep as label research only",
            },
            {
                "gate_id": "P118_BREADTH_BEFORE_REPLAY",
                "stage": "pre_replay",
                "requirement": "Candidate label rows must span enough symbols and months to avoid a one-pocket illusion.",
                "pass_threshold": "symbols >= 20 and train months >= 4 before replay",
                "failure_action": "collect more real/synthetic label coverage before replay",
            },
            {
                "gate_id": "P118_FILL_MODEL_CONSERVATISM",
                "stage": "replay_gate",
                "requirement": "Replay, if later allowed, must pass pessimistic, base and optimistic fill models separately.",
                "pass_threshold": "all_fill_assumptions_pass == 1; optimistic-only success rejected",
                "failure_action": "retire feature family",
            },
            {
                "gate_id": "P118_COMPUTE_BUDGET",
                "stage": "replay_gate",
                "requirement": "No large dense replay is allowed until pre-replay label gates pass.",
                "pass_threshold": "bounded pilot first; full-year replay only after pilot pass and Phase117/115 real-anchor path reviewed",
                "failure_action": "block same-family shard continuation",
            },
        ]
    )


def build_candidate_spec_template(contract: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for family in contract.to_dict("records"):
        rows.append(
            {
                "candidate_template_id": f"{family['feature_family_id']}_STRICT",
                "feature_family_id": family["feature_family_id"],
                "threshold_policy": "train_only_strict",
                "adverse_selection_rate_max": 0.45,
                "symbols_min": 20,
                "train_months_min": 4,
                "replenishment_required": True,
                "spread_non_expansion_required": True,
                "max_daily_orders_per_symbol": 20,
                "pilot_replay_allowed_now": False,
                "why_not_allowed_now": "Phase66/68/69/89 current labels have zero candidate rows and Phase116/117 keep replay gates closed.",
            }
        )
    return pd.DataFrame(rows)


def build_replay_permission_gate(tables: dict[str, pd.DataFrame], label_ledger: pd.DataFrame) -> pd.DataFrame:
    phase116 = tables["phase116"]
    phase117 = tables["phase117"]
    accepted = as_int(metric_value(phase116, "phase116_accepted_strategy_rows"))
    same_family_allowed = as_int(metric_value(phase116, "phase116_same_family_shard_continuation_allowed"))
    replay_allowed = as_int(metric_value(phase117, "phase117_strategy_replay_allowed"))
    label_candidates = int(pd.to_numeric(label_ledger["candidate_rows"], errors="coerce").fillna(0).sum())
    return pd.DataFrame(
        [
            {
                "permission_id": "P118_LABEL_ONLY_DESIGN",
                "permission": "allowed",
                "evidence": "Richer passive feature contract and gates may be designed without replay.",
            },
            {
                "permission_id": "P118_BOUNDED_PILOT_REPLAY",
                "permission": "closed",
                "evidence": f"current_label_candidate_rows={label_candidates}; requires label gates to pass first",
            },
            {
                "permission_id": "P118_FULL_YEAR_REPLAY",
                "permission": "closed",
                "evidence": f"phase116_accepted_strategy_rows={accepted}; same_family_allowed={same_family_allowed}; phase117_strategy_replay_allowed={replay_allowed}",
            },
            {
                "permission_id": "P118_SAME_FAMILY_DENSE_SHARDS",
                "permission": "blocked",
                "evidence": "Phase116 blocks continuation of current failed dense/cross-symbol/event-window families.",
            },
        ]
    )


def build_acceptance_summary(
    label_ledger: pd.DataFrame,
    contract: pd.DataFrame,
    gates: pd.DataFrame,
    specs: pd.DataFrame,
    permission: pd.DataFrame,
) -> pd.DataFrame:
    surviving_prior = int(pd.to_numeric(label_ledger["survives_gate"], errors="coerce").fillna(0).sum())
    label_candidates = int(pd.to_numeric(label_ledger["candidate_rows"], errors="coerce").fillna(0).sum())
    pilot_open = int(permission["permission_id"].eq("P118_BOUNDED_PILOT_REPLAY").loc[permission["permission"].eq("allowed")].sum())
    return pd.DataFrame(
        [
            ("phase118_prior_label_evidence_rows", int(len(label_ledger)), "Prior passive/liquidity label and replay evidence rows reviewed"),
            ("phase118_prior_surviving_gate_rows", surviving_prior, "Prior passive/liquidity rows that survived their gate"),
            ("phase118_prior_candidate_rows", label_candidates, "Candidate rows found by prior passive/liquidity gates"),
            ("phase118_feature_family_rows", int(len(contract)), "New richer passive feature families precommitted"),
            ("phase118_candidate_template_rows", int(len(specs)), "Candidate templates emitted for future label construction"),
            ("phase118_pre_replay_gate_rows", int(len(gates)), "Pre-replay and replay gates locked"),
            ("phase118_bounded_pilot_replay_allowed", pilot_open, "1 means a bounded replay may run immediately"),
            ("phase118_full_year_replay_allowed", 0, "Full-year replay remains closed"),
            ("phase118_next_best_action", "implement_label_builder_for_p118_richer_passive_features_before_any_replay", "Recommended next milestone"),
            ("phase118_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model version carried into any future replay"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase118 Richer Passive Hypothesis Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase118 precommits a materially different passive/liquidity-resilience branch after simple passive labels and simple passive queue replay failed.",
        "It is deliberately label-only: no bounded or full-year replay is allowed until adverse-selection, replenishment and spread-transition feasibility gates pass.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase118_richer_passive_hypothesis_precommit_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def run_phase118(
    base_dir: Path,
    output_dir: Path,
    phase66_dir: Path,
    phase67_dir: Path,
    phase68_dir: Path,
    phase69_dir: Path,
    phase89_dir: Path,
    phase116_dir: Path,
    phase117_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    tables = {
        "phase66": read_metric_table(base_dir / phase66_dir / "passive_label_acceptance_summary.csv"),
        "phase67": read_metric_table(base_dir / phase67_dir / "feature_design_acceptance_summary.csv"),
        "phase68": read_metric_table(base_dir / phase68_dir / "replenishment_acceptance_summary.csv"),
        "phase69": read_metric_table(base_dir / phase69_dir / "spread_transition_acceptance_summary.csv"),
        "phase89": read_metric_table(base_dir / phase89_dir / "passive_queue_cost_floor_acceptance_summary.csv"),
        "phase116": read_metric_table(base_dir / phase116_dir / "phase116_profitability_verdict_acceptance_summary.csv"),
        "phase117": read_metric_table(base_dir / phase117_dir / "phase117_real_anchor_acquisition_acceptance_summary.csv"),
    }
    label_ledger = build_label_failure_ledger(tables)
    contract = build_richer_passive_feature_contract()
    gates = build_pre_replay_feasibility_gates()
    specs = build_candidate_spec_template(contract)
    permission = build_replay_permission_gate(tables, label_ledger)
    acceptance = build_acceptance_summary(label_ledger, contract, gates, specs, permission)

    label_ledger.to_csv(output_dir / "prior_passive_label_failure_ledger.csv", index=False)
    contract.to_csv(output_dir / "richer_passive_feature_contract.csv", index=False)
    gates.to_csv(output_dir / "pre_replay_feasibility_gates.csv", index=False)
    specs.to_csv(output_dir / "candidate_spec_template.csv", index=False)
    permission.to_csv(output_dir / "replay_permission_gate.csv", index=False)
    acceptance.to_csv(output_dir / "phase118_richer_passive_precommit_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Prior Passive Label Failure Ledger": label_ledger,
            "Richer Passive Feature Contract": contract,
            "Pre-Replay Feasibility Gates": gates,
            "Candidate Spec Template": specs,
            "Replay Permission Gate": permission,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase118_richer_passive_hypothesis_precommit",
        "bounded_pilot_replay_allowed": int(
            acceptance.loc[acceptance["metric"].eq("phase118_bounded_pilot_replay_allowed"), "value"].iloc[0]
        ),
        "full_year_replay_allowed": int(
            acceptance.loc[acceptance["metric"].eq("phase118_full_year_replay_allowed"), "value"].iloc[0]
        ),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase118",
            generated_utc=generated_utc,
            inputs={
                "phase66_acceptance": str(phase66_dir / "passive_label_acceptance_summary.csv"),
                "phase67_acceptance": str(phase67_dir / "feature_design_acceptance_summary.csv"),
                "phase68_acceptance": str(phase68_dir / "replenishment_acceptance_summary.csv"),
                "phase69_acceptance": str(phase69_dir / "spread_transition_acceptance_summary.csv"),
                "phase89_acceptance": str(phase89_dir / "passive_queue_cost_floor_acceptance_summary.csv"),
                "phase116_acceptance": str(phase116_dir / "phase116_profitability_verdict_acceptance_summary.csv"),
                "phase117_acceptance": str(phase117_dir / "phase117_real_anchor_acquisition_acceptance_summary.csv"),
            },
            parameters={
                "precommit_policy": "label_feasibility_first_no_pnl_selection",
                "replay_policy": "bounded_pilot_closed_until_p118_pre_replay_gates_pass",
                "full_year_policy": "full_year_replay_closed_until_bounded_pilot_and_real_anchor_gates_pass",
            },
            outputs={
                "prior_passive_label_failure_ledger": str(output_dir / "prior_passive_label_failure_ledger.csv"),
                "richer_passive_feature_contract": str(output_dir / "richer_passive_feature_contract.csv"),
                "pre_replay_feasibility_gates": str(output_dir / "pre_replay_feasibility_gates.csv"),
                "candidate_spec_template": str(output_dir / "candidate_spec_template.csv"),
                "replay_permission_gate": str(output_dir / "replay_permission_gate.csv"),
                "acceptance_summary": str(output_dir / "phase118_richer_passive_precommit_acceptance_summary.csv"),
                "report": str(output_dir / "phase118_richer_passive_hypothesis_precommit_report.md"),
                "manifest": str(output_dir / "phase118_richer_passive_hypothesis_precommit_manifest.json"),
            },
            random_seed="none_deterministic_precommit",
            scenario_ids="phase118_richer_passive_precommit_after_simple_passive_failure",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_pre_replay_design_gate",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase118_richer_passive_hypothesis_precommit_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase118 richer passive hypothesis precommit.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--phase66-dir", type=Path, default=DEFAULT_PHASE66_DIR)
    parser.add_argument("--phase67-dir", type=Path, default=DEFAULT_PHASE67_DIR)
    parser.add_argument("--phase68-dir", type=Path, default=DEFAULT_PHASE68_DIR)
    parser.add_argument("--phase69-dir", type=Path, default=DEFAULT_PHASE69_DIR)
    parser.add_argument("--phase89-dir", type=Path, default=DEFAULT_PHASE89_DIR)
    parser.add_argument("--phase116-dir", type=Path, default=DEFAULT_PHASE116_DIR)
    parser.add_argument("--phase117-dir", type=Path, default=DEFAULT_PHASE117_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase118(
        base_dir=args.base_dir,
        output_dir=args.output_dir,
        phase66_dir=args.phase66_dir,
        phase67_dir=args.phase67_dir,
        phase68_dir=args.phase68_dir,
        phase69_dir=args.phase69_dir,
        phase89_dir=args.phase89_dir,
        phase116_dir=args.phase116_dir,
        phase117_dir=args.phase117_dir,
    )


if __name__ == "__main__":
    main()
