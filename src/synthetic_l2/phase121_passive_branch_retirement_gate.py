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


DEFAULT_OUTPUT_DIR = Path("outputs/phase121")
DEFAULT_PHASE120_DIR = Path("outputs/phase120")
STAGES = {
    "stage01_min_breadth": Path("P120_LABEL_STAGE_01_MIN_BREADTH"),
    "stage02_train_half": Path("P120_LABEL_STAGE_02_TRAIN_HALF"),
}


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


def build_stage_evidence(base_dir: Path, phase120_dir: Path) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for stage_id, stage_path in STAGES.items():
        root = base_dir / phase120_dir / stage_path
        p66 = read_metric_table(root / "phase66" / "passive_label_acceptance_summary.csv")
        p68 = read_metric_table(root / "phase68" / "replenishment_acceptance_summary.csv")
        p69 = read_metric_table(root / "phase69" / "spread_transition_acceptance_summary.csv")
        p119 = read_metric_table(root / "phase119" / "phase119_richer_passive_label_builder_acceptance_summary.csv")
        rows.append(
            {
                "stage_id": stage_id,
                "stage_root": str(phase120_dir / stage_path),
                "shards_scanned": as_int(metric_value(p66, "phase66_shards_scanned")),
                "phase66_candidate_orders": as_int(metric_value(p66, "phase66_candidate_orders")),
                "phase66_inferred_touches": as_int(metric_value(p66, "phase66_inferred_touches")),
                "phase66_label_candidate_rows": as_int(metric_value(p66, "phase66_label_candidate_rows")),
                "phase66_best_after_cost_bps": as_float(metric_value(p66, "phase66_best_mean_after_cost_bps_if_touched")),
                "phase68_label_candidate_rows": as_int(metric_value(p68, "phase68_label_candidate_rows")),
                "phase68_best_after_cost_bps": as_float(metric_value(p68, "phase68_best_mean_after_cost_bps_if_touched")),
                "phase68_best_adverse_selection_rate": as_float(metric_value(p68, "phase68_best_adverse_selection_rate"), 1.0),
                "phase69_signal_rows": as_int(metric_value(p69, "phase69_signal_rows")),
                "phase69_label_candidate_rows": as_int(metric_value(p69, "phase69_label_candidate_rows")),
                "phase69_best_after_cost_bps": as_float(metric_value(p69, "phase69_best_mean_after_cost_bps")),
                "phase119_joined_label_candidate_rows": as_int(metric_value(p119, "phase119_joined_label_candidate_rows")),
                "phase119_pre_replay_candidate_rows": as_int(metric_value(p119, "phase119_pre_replay_candidate_rows")),
                "phase119_max_candidate_symbols": as_int(metric_value(p119, "phase119_max_candidate_symbols")),
                "phase119_max_candidate_trade_dates": as_int(metric_value(p119, "phase119_max_candidate_trade_dates")),
                "phase119_bounded_pilot_replay_allowed": as_int(metric_value(p119, "phase119_bounded_pilot_replay_allowed")),
            }
        )
    return pd.DataFrame(rows)


def build_failure_basis(stage_evidence: pd.DataFrame) -> pd.DataFrame:
    if stage_evidence.empty:
        return pd.DataFrame()
    final = stage_evidence.sort_values("shards_scanned").iloc[-1]
    rows = [
        {
            "failure_id": "P121_ADVERSE_SELECTION_TOXICITY",
            "evidence": f"best_train_half_replenishment_adverse_selection_rate={final['phase68_best_adverse_selection_rate']}",
            "decision": "hard_fail",
            "why_it_matters": "Passive fills are expected to be toxic if nearly all inferred touches are followed by adverse markout.",
        },
        {
            "failure_id": "P121_NO_LABEL_CANDIDATES",
            "evidence": (
                f"phase66={final['phase66_label_candidate_rows']}; "
                f"phase68={final['phase68_label_candidate_rows']}; phase69={final['phase69_label_candidate_rows']}"
            ),
            "decision": "hard_fail",
            "why_it_matters": "The component label gates produced no candidate buckets even before replay.",
        },
        {
            "failure_id": "P121_NO_JOINED_PRE_REPLAY_CANDIDATES",
            "evidence": f"phase119_pre_replay_candidate_rows={final['phase119_pre_replay_candidate_rows']}",
            "decision": "hard_fail",
            "why_it_matters": "The richer composite label builder could form candidates but none passed all feasibility gates.",
        },
        {
            "failure_id": "P121_SYMBOL_BREADTH_SHORTFALL",
            "evidence": f"max_joined_symbols={final['phase119_max_candidate_symbols']}; required_symbols=20",
            "decision": "hard_fail",
            "why_it_matters": "A passive label pocket across four symbols is not broad enough to justify replay.",
        },
        {
            "failure_id": "P121_AFTER_COST_LABEL_NEGATIVE",
            "evidence": (
                f"best_phase66_bps={final['phase66_best_after_cost_bps']}; "
                f"best_phase68_bps={final['phase68_best_after_cost_bps']}; "
                f"best_phase69_bps={final['phase69_best_after_cost_bps']}"
            ),
            "decision": "hard_fail",
            "why_it_matters": "The best label buckets remain negative after the Zerodha cost floor.",
        },
    ]
    return pd.DataFrame(rows)


def build_retirement_ledger() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "family_id": "P66_NAIVE_PASSIVE_IMBALANCE",
                "decision": "retired",
                "replay_allowed": False,
                "full_year_label_stage03_allowed": False,
                "resume_condition": "Only as a negative-control label family.",
            },
            {
                "family_id": "P68_REPLENISHMENT_AFTER_TOUCH",
                "decision": "retired_as_standalone_alpha",
                "replay_allowed": False,
                "full_year_label_stage03_allowed": False,
                "resume_condition": "Only if a future non-P&L label source reduces adverse-selection rate below 0.45 across at least 20 symbols.",
            },
            {
                "family_id": "P69_SPREAD_TRANSITION",
                "decision": "retired_as_standalone_alpha",
                "replay_allowed": False,
                "full_year_label_stage03_allowed": False,
                "resume_condition": "Only as context inside a new non-toxic feature class, not as standalone spread-transition replay.",
            },
            {
                "family_id": "P118_RICHER_PASSIVE_LABEL_COMPOSITE",
                "decision": "retired_pending_new_feature_source",
                "replay_allowed": False,
                "full_year_label_stage03_allowed": False,
                "resume_condition": "Requires a materially new feature source that passes adverse-selection and breadth gates before any bounded replay.",
            },
        ]
    )


def build_next_research_queue() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "priority": 1,
                "next_item": "real_anchor_data_acquisition",
                "phase_reference": "Phase117",
                "why": "The current synthetic strategy families are falsified or replay-locked; adding real WebSocket L2 days is the cleanest source of new evidence.",
                "allowed_now": True,
                "forbidden": "Do not claim profitability from synthetic-only pockets.",
            },
            {
                "priority": 2,
                "next_item": "new_non_passive_non_taker_feature_source_precommit",
                "phase_reference": "new_phase",
                "why": "Both taker and passive-simple mechanisms failed; a new branch must use a genuinely different edge source before replay.",
                "allowed_now": True,
                "forbidden": "No threshold widening of P66/P68/P69/P118 candidates.",
            },
            {
                "priority": 3,
                "next_item": "full_year_passive_label_stage03",
                "phase_reference": "Phase120 Stage03",
                "why": "Only useful as final confirmation/negative-control, not as a path to replay after Stage02 hard failures.",
                "allowed_now": False,
                "forbidden": "Do not run unless explicitly needed for audit completeness.",
            },
        ]
    )


def build_acceptance_summary(stage_evidence: pd.DataFrame, failure_basis: pd.DataFrame, retirement: pd.DataFrame) -> pd.DataFrame:
    final = stage_evidence.sort_values("shards_scanned").iloc[-1] if not stage_evidence.empty else {}
    hard_failures = int(failure_basis["decision"].astype(str).eq("hard_fail").sum()) if not failure_basis.empty else 0
    replay_allowed = int(retirement["replay_allowed"].astype(bool).any()) if not retirement.empty else 0
    stage03_allowed = int(retirement["full_year_label_stage03_allowed"].astype(bool).any()) if not retirement.empty else 0
    return pd.DataFrame(
        [
            ("phase121_stage_rows_reviewed", int(len(stage_evidence)), "Phase120 passive label expansion stages reviewed"),
            ("phase121_max_shards_reviewed", as_int(final.get("shards_scanned", 0)), "Largest label-only expansion reviewed"),
            ("phase121_train_half_candidate_orders", as_int(final.get("phase66_candidate_orders", 0)), "Train-half hypothetical passive candidate orders reviewed"),
            ("phase121_train_half_inferred_touches", as_int(final.get("phase66_inferred_touches", 0)), "Train-half inferred passive touches reviewed"),
            ("phase121_train_half_pre_replay_candidates", as_int(final.get("phase119_pre_replay_candidate_rows", 0)), "Train-half richer passive pre-replay candidates"),
            ("phase121_hard_failure_rows", hard_failures, "Hard failure bases recorded"),
            ("phase121_retired_family_rows", int(len(retirement)), "Passive families retired or blocked"),
            ("phase121_passive_replay_allowed", replay_allowed, "1 means passive bounded replay may run"),
            ("phase121_stage03_full_year_label_allowed", stage03_allowed, "1 means full-year passive label Stage03 should run now"),
            ("phase121_next_best_action", "return_to_real_anchor_acquisition_or_precommit_new_non_passive_feature_source", "Recommended next milestone"),
            ("phase121_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model used by passive label evidence"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase121 Passive Branch Retirement Gate",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase121 reviews the Phase120 Stage 01 and Stage 02 label-only expansions before allowing any more passive work.",
        "The verdict is to retire the current passive branch from replay: broader train-half coverage did not produce a single pre-replay candidate and adverse-selection remains toxic.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase121_passive_branch_retirement_gate_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase121(base_dir: Path, phase120_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    stage_evidence = build_stage_evidence(base_dir, phase120_dir)
    failure_basis = build_failure_basis(stage_evidence)
    retirement = build_retirement_ledger()
    next_queue = build_next_research_queue()
    acceptance = build_acceptance_summary(stage_evidence, failure_basis, retirement)

    stage_evidence.to_csv(output_dir / "passive_stage_evidence_ledger.csv", index=False)
    failure_basis.to_csv(output_dir / "passive_failure_basis.csv", index=False)
    retirement.to_csv(output_dir / "passive_retirement_ledger.csv", index=False)
    next_queue.to_csv(output_dir / "next_research_queue.csv", index=False)
    acceptance.to_csv(output_dir / "phase121_passive_branch_retirement_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Passive Stage Evidence Ledger": stage_evidence,
            "Passive Failure Basis": failure_basis,
            "Passive Retirement Ledger": retirement,
            "Next Research Queue": next_queue,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase121_passive_branch_retirement_gate",
        "passive_replay_allowed": int(
            acceptance.loc[acceptance["metric"].eq("phase121_passive_replay_allowed"), "value"].iloc[0]
        ),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase121",
            generated_utc=generated_utc,
            inputs={
                "stage01_root": str(phase120_dir / STAGES["stage01_min_breadth"]),
                "stage02_root": str(phase120_dir / STAGES["stage02_train_half"]),
            },
            parameters={
                "decision_policy": "retire_passive_branch_when_train_half_label_expansion_has_zero_pre_replay_candidates",
                "stage03_policy": "do_not_run_full_year_passive_labels_after_train_half_hard_failure_unless_audit_only",
                "replay_policy": "passive_replay_closed",
            },
            outputs={
                "stage_evidence": str(output_dir / "passive_stage_evidence_ledger.csv"),
                "failure_basis": str(output_dir / "passive_failure_basis.csv"),
                "retirement": str(output_dir / "passive_retirement_ledger.csv"),
                "next_queue": str(output_dir / "next_research_queue.csv"),
                "acceptance": str(output_dir / "phase121_passive_branch_retirement_acceptance_summary.csv"),
                "report": str(output_dir / "phase121_passive_branch_retirement_gate_report.md"),
                "manifest": str(output_dir / "phase121_passive_branch_retirement_gate_manifest.json"),
            },
            random_seed="none_deterministic_decision_gate",
            scenario_ids="phase121_passive_retirement_after_phase120_stage02",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_decision_gate",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase121_passive_branch_retirement_gate_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase121 passive branch retirement gate.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--phase120-dir", type=Path, default=DEFAULT_PHASE120_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase121(base_dir=args.base_dir, phase120_dir=args.phase120_dir, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
