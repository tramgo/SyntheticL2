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


DEFAULT_OUTPUT_DIR = Path("outputs/phase126")
DEFAULT_PHASE125_DIR = Path("outputs/phase125")
DEFAULT_PHASE116_DIR = Path("outputs/phase116")
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


def build_permission_ledger(flags: pd.DataFrame) -> pd.DataFrame:
    if flags.empty:
        return pd.DataFrame(
            columns=[
                "trade_month",
                "symbol",
                "realism_review_flag",
                "opportunity_abstention_flag",
                "candidate_generation_allowed",
                "candidate_generation_status",
                "strategy_replay_allowed",
                "why",
            ]
        )
    pivot = (
        flags.pivot_table(
            index=["trade_month", "symbol"],
            columns="filter_id",
            values="filter_flag",
            aggfunc="max",
            fill_value=0,
        )
        .reset_index()
        .rename_axis(None, axis=1)
    )
    if "P125_REGIME_REALISM_RISK" not in pivot.columns:
        pivot["P125_REGIME_REALISM_RISK"] = 0
    if "P125_OPPORTUNITY_ABSTENTION" not in pivot.columns:
        pivot["P125_OPPORTUNITY_ABSTENTION"] = 0
    pivot["realism_review_flag"] = pivot["P125_REGIME_REALISM_RISK"].astype(int)
    pivot["opportunity_abstention_flag"] = pivot["P125_OPPORTUNITY_ABSTENTION"].astype(int)
    pivot["candidate_generation_allowed"] = (pivot["opportunity_abstention_flag"].eq(0)).astype(int)
    pivot["candidate_generation_status"] = pivot["candidate_generation_allowed"].map({1: "allowed_for_precommit_design_only", 0: "blocked_by_opportunity_abstention_filter"})
    pivot["strategy_replay_allowed"] = 0
    pivot["why"] = pivot.apply(
        lambda row: (
            "blocked: low-opportunity symbol/month; no candidate generation or replay"
            if int(row["opportunity_abstention_flag"]) == 1
            else (
                "allowed for label/precommit design with realism-review warning; replay still closed"
                if int(row["realism_review_flag"]) == 1
                else "allowed for label/precommit design only; replay still closed"
            )
        ),
        axis=1,
    )
    return pivot[
        [
            "trade_month",
            "symbol",
            "realism_review_flag",
            "opportunity_abstention_flag",
            "candidate_generation_allowed",
            "candidate_generation_status",
            "strategy_replay_allowed",
            "why",
        ]
    ].sort_values(["trade_month", "symbol"], kind="mergesort")


def build_month_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    if ledger.empty:
        return pd.DataFrame()
    return (
        ledger.groupby("trade_month", sort=True)
        .agg(
            symbol_month_rows=("symbol", "count"),
            candidate_generation_allowed_rows=("candidate_generation_allowed", "sum"),
            opportunity_blocked_rows=("opportunity_abstention_flag", "sum"),
            realism_review_rows=("realism_review_flag", "sum"),
        )
        .reset_index()
        .assign(
            allowed_fraction=lambda df: df["candidate_generation_allowed_rows"] / df["symbol_month_rows"],
            opportunity_blocked_fraction=lambda df: df["opportunity_blocked_rows"] / df["symbol_month_rows"],
            realism_review_fraction=lambda df: df["realism_review_rows"] / df["symbol_month_rows"],
        )
    )


def build_symbol_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    if ledger.empty:
        return pd.DataFrame()
    return (
        ledger.groupby("symbol", sort=True)
        .agg(
            months=("trade_month", "nunique"),
            candidate_generation_allowed_months=("candidate_generation_allowed", "sum"),
            opportunity_blocked_months=("opportunity_abstention_flag", "sum"),
            realism_review_months=("realism_review_flag", "sum"),
        )
        .reset_index()
        .assign(
            allowed_fraction=lambda df: df["candidate_generation_allowed_months"] / df["months"],
            opportunity_blocked_fraction=lambda df: df["opportunity_blocked_months"] / df["months"],
            realism_review_fraction=lambda df: df["realism_review_months"] / df["months"],
        )
        .sort_values(["opportunity_blocked_months", "realism_review_months", "symbol"], ascending=[False, False, True], kind="mergesort")
    )


def build_guardrails() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "guardrail_id": "P126_PRECOMMIT_ONLY",
                "requirement": "Allowed rows may be used only for future feature-label/precommit design.",
                "enforcement": "candidate_generation_status never implies replay or profitability.",
            },
            {
                "guardrail_id": "P126_ABSTENTION_BLOCKS_GENERATION",
                "requirement": "Opportunity-abstention rows block future candidate generation.",
                "enforcement": "candidate_generation_allowed is 0 when opportunity_abstention_flag is 1.",
            },
            {
                "guardrail_id": "P126_REALISM_REVIEW_WARNING",
                "requirement": "Realism-risk rows must be marked for generator/evidence review.",
                "enforcement": "realism_review_flag is retained even when candidate generation is allowed.",
            },
            {
                "guardrail_id": "P126_REPLAY_CLOSED",
                "requirement": "No row may open strategy replay.",
                "enforcement": "strategy_replay_allowed is 0 for all symbol/month permissions.",
            },
        ]
    )


def build_gate_evaluation(ledger: pd.DataFrame, phase116: pd.DataFrame, phase117: pd.DataFrame) -> pd.DataFrame:
    global_replay_lock = as_int(metric_value(phase116, "phase116_same_family_shard_continuation_allowed"))
    ready_real_days = as_int(metric_value(phase117, "phase117_current_ready_real_anchor_days"))
    needed_real_days = as_int(metric_value(phase117, "phase117_additional_days_needed_for_min"))
    return pd.DataFrame(
        [
            {"gate_id": "P126_PERMISSION_LEDGER_EXISTS", "gate_pass": int(not ledger.empty), "evidence": f"rows={len(ledger)}"},
            {
                "gate_id": "P126_ABSTENTION_ENFORCED",
                "gate_pass": int(
                    (ledger.empty)
                    or ledger.loc[ledger["opportunity_abstention_flag"].eq(1), "candidate_generation_allowed"].sum() == 0
                ),
                "evidence": "opportunity-abstention rows have candidate_generation_allowed=0",
            },
            {
                "gate_id": "P126_ROW_REPLAY_LOCK",
                "gate_pass": int((ledger.empty) or ledger["strategy_replay_allowed"].sum() == 0),
                "evidence": "all row-level strategy_replay_allowed values are 0",
            },
            {
                "gate_id": "P126_GLOBAL_REPLAY_LOCK",
                "gate_pass": int(global_replay_lock == 0),
                "evidence": f"phase116_same_family_shard_continuation_allowed={global_replay_lock}",
            },
            {
                "gate_id": "P126_REAL_ANCHOR_STILL_BLOCKED",
                "gate_pass": int(ready_real_days < 5 and needed_real_days > 0),
                "evidence": f"ready_real_anchor_days={ready_real_days}; days_needed={needed_real_days}",
            },
        ]
    )


def build_acceptance_summary(ledger: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    rows = int(len(ledger))
    allowed = int(ledger["candidate_generation_allowed"].sum()) if not ledger.empty else 0
    blocked = int(ledger["opportunity_abstention_flag"].sum()) if not ledger.empty else 0
    realism = int(ledger["realism_review_flag"].sum()) if not ledger.empty else 0
    return pd.DataFrame(
        [
            ("phase126_symbol_month_rows", rows, "Symbol/month permission rows"),
            ("phase126_candidate_generation_allowed_rows", allowed, "Rows allowed for future precommit/label design only"),
            ("phase126_opportunity_blocked_rows", blocked, "Rows blocked by opportunity-abstention filter"),
            ("phase126_realism_review_rows", realism, "Rows flagged for realism review"),
            ("phase126_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase126_all_gates_pass", int(gates["gate_pass"].astype(bool).all()) if not gates.empty else 0, "1 means permission ledger obeys guardrails"),
            ("phase126_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase126_next_best_action", "use_permission_ledger_for_future_precommit_design_and_continue_real_anchor_acquisition", "Recommended next milestone"),
            ("phase126_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model retained for audit continuity"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase126 Candidate-Generation Permission Ledger",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase126 converts Phase125 diagnostic/abstention filters into a symbol/month permission ledger for future precommit design.",
        "The ledger can block candidate generation in low-opportunity rows, but it cannot open strategy replay.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase126_candidate_generation_permission_ledger_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def run_phase126(base_dir: Path, output_dir: Path, phase125_dir: Path, phase116_dir: Path, phase117_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    flags = read_csv(base_dir / phase125_dir / "filter_symbol_month_flags.csv")
    phase116 = read_metric_table(base_dir / phase116_dir / "phase116_profitability_verdict_acceptance_summary.csv")
    phase117 = read_metric_table(base_dir / phase117_dir / "phase117_real_anchor_acquisition_acceptance_summary.csv")
    ledger = build_permission_ledger(flags)
    month_summary = build_month_summary(ledger)
    symbol_summary = build_symbol_summary(ledger)
    guardrails = build_guardrails()
    gates = build_gate_evaluation(ledger, phase116, phase117)
    acceptance = build_acceptance_summary(ledger, gates)

    ledger.to_csv(output_dir / "candidate_generation_permission_ledger.csv", index=False)
    month_summary.to_csv(output_dir / "candidate_generation_month_summary.csv", index=False)
    symbol_summary.to_csv(output_dir / "candidate_generation_symbol_summary.csv", index=False)
    guardrails.to_csv(output_dir / "candidate_generation_guardrails.csv", index=False)
    gates.to_csv(output_dir / "candidate_generation_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase126_candidate_generation_permission_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Month Summary": month_summary,
            "Symbol Summary": symbol_summary.head(40),
            "Guardrails": guardrails,
            "Gate Evaluation": gates,
            "Permission Ledger Sample": ledger.head(40),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase126_candidate_generation_permission_ledger",
        "strategy_replay_allowed": 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase126",
            generated_utc=generated_utc,
            inputs={
                "phase125_filter_flags": str(phase125_dir / "filter_symbol_month_flags.csv"),
                "phase116_acceptance": str(phase116_dir / "phase116_profitability_verdict_acceptance_summary.csv"),
                "phase117_acceptance": str(phase117_dir / "phase117_real_anchor_acquisition_acceptance_summary.csv"),
            },
            parameters={
                "permission_scope": "candidate_generation_precommit_design_only",
                "replay_policy": "closed",
                "abstention_policy": "opportunity_abstention_blocks_candidate_generation",
            },
            outputs={
                "permission_ledger": str(output_dir / "candidate_generation_permission_ledger.csv"),
                "month_summary": str(output_dir / "candidate_generation_month_summary.csv"),
                "symbol_summary": str(output_dir / "candidate_generation_symbol_summary.csv"),
                "guardrails": str(output_dir / "candidate_generation_guardrails.csv"),
                "gates": str(output_dir / "candidate_generation_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase126_candidate_generation_permission_acceptance_summary.csv"),
                "report": str(output_dir / "phase126_candidate_generation_permission_ledger_report.md"),
                "manifest": str(output_dir / "phase126_candidate_generation_permission_ledger_manifest.json"),
            },
            random_seed="none_deterministic_permission_ledger",
            scenario_ids="phase126_candidate_generation_permission_from_phase125_filters",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_permission_ledger",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase126_candidate_generation_permission_ledger_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase126 candidate-generation permission ledger.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--phase125-dir", type=Path, default=DEFAULT_PHASE125_DIR)
    parser.add_argument("--phase116-dir", type=Path, default=DEFAULT_PHASE116_DIR)
    parser.add_argument("--phase117-dir", type=Path, default=DEFAULT_PHASE117_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase126(
        base_dir=args.base_dir,
        output_dir=args.output_dir,
        phase125_dir=args.phase125_dir,
        phase116_dir=args.phase116_dir,
        phase117_dir=args.phase117_dir,
    )


if __name__ == "__main__":
    main()
