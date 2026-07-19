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


DEFAULT_OUTPUT_DIR = Path("outputs/phase127")
DEFAULT_PHASE126_DIR = Path("outputs/phase126")
DEFAULT_PHASE117_DIR = Path("outputs/phase117")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


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


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def build_allowed_context_queue(ledger: pd.DataFrame) -> pd.DataFrame:
    if ledger.empty:
        return pd.DataFrame()
    frame = ledger.copy()
    frame["candidate_generation_allowed"] = pd.to_numeric(frame["candidate_generation_allowed"], errors="coerce").fillna(0).astype(int)
    frame["realism_review_flag"] = pd.to_numeric(frame["realism_review_flag"], errors="coerce").fillna(0).astype(int)
    allowed = frame[frame["candidate_generation_allowed"].eq(1)].copy()
    allowed["priority_bucket"] = allowed["realism_review_flag"].map({0: "P1_clean_allowed", 1: "P2_allowed_with_realism_review"})
    allowed["precommit_scope"] = "label_or_feature_design_only"
    allowed["strategy_replay_allowed"] = 0
    allowed["must_include_guardrail"] = allowed["realism_review_flag"].map(
        {0: "standard_no_replay_guardrail", 1: "realism_review_required_before_any_future_replay_gate"}
    )
    allowed = allowed.sort_values(["priority_bucket", "trade_month", "symbol"], kind="mergesort").reset_index(drop=True)
    allowed.insert(0, "queue_rank", range(1, len(allowed) + 1))
    return allowed[
        [
            "queue_rank",
            "trade_month",
            "symbol",
            "priority_bucket",
            "realism_review_flag",
            "opportunity_abstention_flag",
            "candidate_generation_allowed",
            "precommit_scope",
            "strategy_replay_allowed",
            "must_include_guardrail",
            "why",
        ]
    ]


def build_blocked_context_ledger(ledger: pd.DataFrame) -> pd.DataFrame:
    if ledger.empty:
        return pd.DataFrame()
    frame = ledger.copy()
    frame["candidate_generation_allowed"] = pd.to_numeric(frame["candidate_generation_allowed"], errors="coerce").fillna(0).astype(int)
    blocked = frame[frame["candidate_generation_allowed"].eq(0)].copy()
    blocked["blocked_reason"] = "opportunity_abstention_filter"
    blocked["override_allowed"] = False
    blocked["strategy_replay_allowed"] = 0
    return blocked[
        [
            "trade_month",
            "symbol",
            "realism_review_flag",
            "opportunity_abstention_flag",
            "blocked_reason",
            "override_allowed",
            "strategy_replay_allowed",
            "why",
        ]
    ].sort_values(["trade_month", "symbol"], kind="mergesort")


def build_precommit_work_packages(queue: pd.DataFrame) -> pd.DataFrame:
    if queue.empty:
        return pd.DataFrame()
    rows = []
    clean = queue[queue["priority_bucket"].eq("P1_clean_allowed")]
    review = queue[queue["priority_bucket"].eq("P2_allowed_with_realism_review")]
    for package_id, label, frame in [
        ("P127_WP01_CLEAN_CONTEXT_LABEL_DESIGN", "clean_allowed_contexts", clean),
        ("P127_WP02_REALISM_REVIEW_CONTEXT_LABEL_DESIGN", "allowed_with_realism_review", review),
    ]:
        rows.append(
            {
                "work_package_id": package_id,
                "context_bucket": label,
                "symbol_month_rows": int(len(frame)),
                "symbols": int(frame["symbol"].nunique()) if not frame.empty else 0,
                "months": int(frame["trade_month"].nunique()) if not frame.empty else 0,
                "allowed_deliverable": "new_feature_label_matrix_or_precommit_spec",
                "forbidden_deliverable": "buy_sell_signal_or_pnl_replay",
                "next_command_policy": "must consume candidate_generation_permission_ledger before selecting rows",
                "strategy_replay_allowed": 0,
            }
        )
    return pd.DataFrame(rows)


def build_guardrails() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "guardrail_id": "P127_USE_PERMISSION_LEDGER",
                "requirement": "Future synthetic candidate design must start from Phase126 allowed rows.",
                "enforcement": "Allowed queue and blocked ledger are emitted separately.",
            },
            {
                "guardrail_id": "P127_BLOCK_ABSTENTION_ROWS",
                "requirement": "Rows blocked by opportunity-abstention cannot be used for candidate generation.",
                "enforcement": "override_allowed is false for every blocked row.",
            },
            {
                "guardrail_id": "P127_REALISM_WARNINGS_SURVIVE",
                "requirement": "Allowed rows with realism-risk flags must remain marked.",
                "enforcement": "Priority bucket separates clean rows from realism-review rows.",
            },
            {
                "guardrail_id": "P127_NO_REPLAY",
                "requirement": "The precommit queue cannot open strategy replay.",
                "enforcement": "strategy_replay_allowed remains 0 in all outputs.",
            },
        ]
    )


def build_gate_evaluation(queue: pd.DataFrame, blocked: pd.DataFrame, packages: pd.DataFrame, phase117: pd.DataFrame) -> pd.DataFrame:
    ready_days = as_int(metric_value(phase117, "phase117_current_ready_real_anchor_days"))
    days_needed = as_int(metric_value(phase117, "phase117_additional_days_needed_for_min"))
    return pd.DataFrame(
        [
            {"gate_id": "P127_ALLOWED_QUEUE_EXISTS", "gate_pass": int(not queue.empty), "evidence": f"allowed_rows={len(queue)}"},
            {"gate_id": "P127_BLOCKED_LEDGER_EXISTS", "gate_pass": int(not blocked.empty), "evidence": f"blocked_rows={len(blocked)}"},
            {
                "gate_id": "P127_WORK_PACKAGES_DECLARED",
                "gate_pass": int(not packages.empty and len(packages) >= 2),
                "evidence": f"work_packages={len(packages)}",
            },
            {
                "gate_id": "P127_NO_REPLAY",
                "gate_pass": int(
                    (queue.empty or queue["strategy_replay_allowed"].sum() == 0)
                    and (blocked.empty or blocked["strategy_replay_allowed"].sum() == 0)
                    and (packages.empty or packages["strategy_replay_allowed"].sum() == 0)
                ),
                "evidence": "all emitted strategy_replay_allowed fields are 0",
            },
            {
                "gate_id": "P127_REAL_ANCHOR_STILL_PRIMARY",
                "gate_pass": int(ready_days < 5 and days_needed > 0),
                "evidence": f"ready_real_anchor_days={ready_days}; days_needed={days_needed}",
            },
        ]
    )


def build_acceptance_summary(queue: pd.DataFrame, blocked: pd.DataFrame, packages: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    clean = int(queue["priority_bucket"].eq("P1_clean_allowed").sum()) if not queue.empty else 0
    review = int(queue["priority_bucket"].eq("P2_allowed_with_realism_review").sum()) if not queue.empty else 0
    return pd.DataFrame(
        [
            ("phase127_allowed_context_rows", int(len(queue)), "Symbol/month contexts allowed for precommit design only"),
            ("phase127_clean_allowed_context_rows", clean, "Allowed contexts without realism-review warning"),
            ("phase127_realism_review_context_rows", review, "Allowed contexts retaining realism-review warning"),
            ("phase127_blocked_context_rows", int(len(blocked)), "Contexts blocked from candidate generation"),
            ("phase127_work_package_rows", int(len(packages)), "Precommit-design work packages emitted"),
            ("phase127_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase127_all_gates_pass", int(gates["gate_pass"].astype(bool).all()) if not gates.empty else 0, "1 means queue obeys guardrails"),
            ("phase127_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase127_next_best_action", "design_next_label_matrix_only_from_phase127_allowed_contexts_or_continue_real_anchor_acquisition", "Recommended next milestone"),
            ("phase127_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model retained for audit continuity"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase127 Allowed-Universe Precommit Queue",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase127 converts the Phase126 permission ledger into an allowed universe for future label/precommit design.",
        "It separates clean allowed contexts, realism-review contexts and blocked contexts. Replay remains closed.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase127_allowed_universe_precommit_queue_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase127(base_dir: Path, output_dir: Path, phase126_dir: Path, phase117_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    ledger = read_csv(base_dir / phase126_dir / "candidate_generation_permission_ledger.csv")
    phase117 = read_metric_table(base_dir / phase117_dir / "phase117_real_anchor_acquisition_acceptance_summary.csv")
    queue = build_allowed_context_queue(ledger)
    blocked = build_blocked_context_ledger(ledger)
    packages = build_precommit_work_packages(queue)
    guardrails = build_guardrails()
    gates = build_gate_evaluation(queue, blocked, packages, phase117)
    acceptance = build_acceptance_summary(queue, blocked, packages, gates)

    queue.to_csv(output_dir / "allowed_context_precommit_queue.csv", index=False)
    blocked.to_csv(output_dir / "blocked_context_ledger.csv", index=False)
    packages.to_csv(output_dir / "precommit_work_packages.csv", index=False)
    guardrails.to_csv(output_dir / "allowed_universe_guardrails.csv", index=False)
    gates.to_csv(output_dir / "allowed_universe_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase127_allowed_universe_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Precommit Work Packages": packages,
            "Allowed Queue Sample": queue.head(50),
            "Blocked Context Sample": blocked.head(50),
            "Guardrails": guardrails,
            "Gate Evaluation": gates,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase127_allowed_universe_precommit_queue",
        "strategy_replay_allowed": 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase127",
            generated_utc=generated_utc,
            inputs={
                "phase126_permission_ledger": str(phase126_dir / "candidate_generation_permission_ledger.csv"),
                "phase117_acceptance": str(phase117_dir / "phase117_real_anchor_acquisition_acceptance_summary.csv"),
            },
            parameters={
                "queue_scope": "future_label_or_feature_precommit_design_only",
                "blocked_policy": "opportunity_abstention_rows_cannot_be_used",
                "replay_policy": "closed",
            },
            outputs={
                "allowed_queue": str(output_dir / "allowed_context_precommit_queue.csv"),
                "blocked_ledger": str(output_dir / "blocked_context_ledger.csv"),
                "work_packages": str(output_dir / "precommit_work_packages.csv"),
                "guardrails": str(output_dir / "allowed_universe_guardrails.csv"),
                "gates": str(output_dir / "allowed_universe_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase127_allowed_universe_acceptance_summary.csv"),
                "report": str(output_dir / "phase127_allowed_universe_precommit_queue_report.md"),
                "manifest": str(output_dir / "phase127_allowed_universe_precommit_queue_manifest.json"),
            },
            random_seed="none_deterministic_queue",
            scenario_ids="phase127_allowed_precommit_universe_from_phase126_permissions",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_precommit_queue",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase127_allowed_universe_precommit_queue_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase127 allowed-universe precommit queue.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--phase126-dir", type=Path, default=DEFAULT_PHASE126_DIR)
    parser.add_argument("--phase117-dir", type=Path, default=DEFAULT_PHASE117_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase127(base_dir=args.base_dir, output_dir=args.output_dir, phase126_dir=args.phase126_dir, phase117_dir=args.phase117_dir)


if __name__ == "__main__":
    main()
