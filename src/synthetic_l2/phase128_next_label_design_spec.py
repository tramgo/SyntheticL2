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


DEFAULT_OUTPUT_DIR = Path("outputs/phase128")
DEFAULT_PHASE127_DIR = Path("outputs/phase127")
DEFAULT_PHASE123_DIR = Path("outputs/phase123")
DEFAULT_PHASE117_DIR = Path("outputs/phase117")


FORBIDDEN_SIGNALS = "buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim"


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


def normalize_allowed_queue(queue: pd.DataFrame) -> pd.DataFrame:
    if queue.empty:
        return pd.DataFrame()
    frame = queue.copy()
    for column in ["realism_review_flag", "opportunity_abstention_flag", "candidate_generation_allowed", "strategy_replay_allowed"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0).astype(int)
    frame["trade_month"] = frame["trade_month"].astype(str)
    frame["symbol"] = frame["symbol"].astype(str)
    return frame


def build_feature_snapshot(queue: pd.DataFrame, label_matrix: pd.DataFrame) -> pd.DataFrame:
    if queue.empty:
        return pd.DataFrame()
    if label_matrix.empty:
        snapshot = queue.copy()
    else:
        matrix = label_matrix.copy()
        matrix["trade_month"] = matrix["trade_month"].astype(str)
        matrix["symbol"] = matrix["symbol"].astype(str)
        keep_columns = [
            "trade_month",
            "symbol",
            "train_split",
            "rows_scanned",
            "regime_count",
            "feed_profile_count",
            "market_shock_rows",
            "symbol_shock_rows",
            "feed_imperfection_rate",
            "median_spread_bps",
            "p90_spread_bps",
            "mean_l1_depth",
            "mean_l5_depth",
            "one_tick_return_std",
            "passive_min_adverse_rate",
            "passive_max_cost_clearing_rate",
            "cost_toxicity_label",
            "regime_realism_risk_label",
            "opportunity_abstention_label",
            "label_source",
        ]
        available = [column for column in keep_columns if column in matrix.columns]
        snapshot = queue.merge(matrix[available], on=["trade_month", "symbol"], how="left", validate="one_to_one")

    snapshot["phase128_scope"] = "allowed_context_label_design_only"
    snapshot["strategy_replay_allowed"] = 0
    snapshot["forbidden_outputs"] = FORBIDDEN_SIGNALS
    return snapshot.sort_values(["priority_bucket", "trade_month", "symbol"], kind="mergesort").reset_index(drop=True)


def build_blocked_exclusion_ledger(blocked: pd.DataFrame) -> pd.DataFrame:
    if blocked.empty:
        return pd.DataFrame()
    frame = blocked.copy()
    frame["phase128_exclusion_reason"] = frame.get("blocked_reason", "blocked_by_phase127").astype(str)
    frame["can_enter_label_design"] = 0
    frame["can_enter_replay"] = 0
    frame["override_required_for_future_use"] = "new_real_anchor_evidence_and_new_permission_ledger"
    return frame.sort_values(["trade_month", "symbol"], kind="mergesort").reset_index(drop=True)


def build_label_design_specs(snapshot: pd.DataFrame) -> pd.DataFrame:
    allowed_rows = int(len(snapshot))
    clean_rows = int(snapshot["priority_bucket"].eq("P1_clean_allowed").sum()) if not snapshot.empty else 0
    review_rows = int(snapshot["priority_bucket"].eq("P2_allowed_with_realism_review").sum()) if not snapshot.empty else 0
    symbols = int(snapshot["symbol"].nunique()) if not snapshot.empty else 0
    months = int(snapshot["trade_month"].nunique()) if not snapshot.empty else 0

    return pd.DataFrame(
        [
            {
                "label_design_id": "P128_REGIME_STABILITY_LABEL",
                "purpose": "Separate realism-stable contexts from contexts that need generator/real-anchor review before future hypothesis work.",
                "input_scope": "phase127_allowed_contexts_only",
                "allowed_context_rows": allowed_rows,
                "clean_context_rows": clean_rows,
                "realism_review_context_rows": review_rows,
                "symbols": symbols,
                "months": months,
                "candidate_features": "feed_imperfection_rate;regime_count;feed_profile_count;market_shock_rows;symbol_shock_rows;median_spread_bps;p90_spread_bps;one_tick_return_std",
                "candidate_label_rule": "label contexts with low feed-imperfection and bounded spread/volatility as realism-stable; retain realism-review as a separate stratum",
                "forbidden_inputs": FORBIDDEN_SIGNALS,
                "deliverable_type": "non_trading_label_matrix",
                "strategy_replay_allowed": 0,
            },
            {
                "label_design_id": "P128_LIQUIDITY_OPPORTUNITY_LABEL",
                "purpose": "Identify allowed contexts with enough depth/spread activity to justify future non-replay hypothesis design.",
                "input_scope": "phase127_allowed_contexts_only",
                "allowed_context_rows": allowed_rows,
                "clean_context_rows": clean_rows,
                "realism_review_context_rows": review_rows,
                "symbols": symbols,
                "months": months,
                "candidate_features": "median_spread_bps;p90_spread_bps;mean_l1_depth;mean_l5_depth;one_tick_return_std;rows_scanned",
                "candidate_label_rule": "rank allowed contexts by depth-adjusted spread and volatility without assigning trade side or order intent",
                "forbidden_inputs": FORBIDDEN_SIGNALS,
                "deliverable_type": "non_trading_label_matrix",
                "strategy_replay_allowed": 0,
            },
            {
                "label_design_id": "P128_COST_TOXICITY_REFINEMENT_LABEL",
                "purpose": "Turn broad passive-toxicity failures into diagnostic buckets for future feature discovery, not a replay permission.",
                "input_scope": "phase127_allowed_contexts_only",
                "allowed_context_rows": allowed_rows,
                "clean_context_rows": clean_rows,
                "realism_review_context_rows": review_rows,
                "symbols": symbols,
                "months": months,
                "candidate_features": "passive_min_adverse_rate;passive_max_cost_clearing_rate;cost_toxicity_label;median_spread_bps;p90_spread_bps;mean_l1_depth",
                "candidate_label_rule": "bucket allowed contexts into toxicity regimes while preserving the closed replay gate",
                "forbidden_inputs": FORBIDDEN_SIGNALS,
                "deliverable_type": "non_trading_label_matrix",
                "strategy_replay_allowed": 0,
            },
        ]
    )


def build_guardrails() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "guardrail_id": "P128_ALLOWED_CONTEXTS_ONLY",
                "requirement": "Phase128 may consume only Phase127 allowed-context rows for label design.",
                "enforcement": "Feature snapshot is an inner design set derived from allowed_context_precommit_queue.csv.",
            },
            {
                "guardrail_id": "P128_BLOCKED_CONTEXTS_EXCLUDED",
                "requirement": "Phase127 blocked rows cannot enter Phase128 label design.",
                "enforcement": "Blocked rows are emitted only in an exclusion ledger with can_enter_label_design=0.",
            },
            {
                "guardrail_id": "P128_NO_TRADING_OUTPUTS",
                "requirement": "Phase128 cannot emit buy/sell signals, order models, fills, P&L, or profitability claims.",
                "enforcement": f"Every spec records forbidden inputs and outputs: {FORBIDDEN_SIGNALS}.",
            },
            {
                "guardrail_id": "P128_REALISM_REVIEW_PRESERVED",
                "requirement": "Allowed contexts with realism-review warnings must remain separated.",
                "enforcement": "Specs and snapshot preserve priority_bucket and realism_review_flag.",
            },
            {
                "guardrail_id": "P128_REAL_ANCHOR_REMAINS_PRIMARY",
                "requirement": "More real Zerodha L2 days remain the primary unlock for future replay.",
                "enforcement": "Acceptance summary carries Phase117 ready-day blocker forward.",
            },
        ]
    )


def build_gate_evaluation(
    snapshot: pd.DataFrame,
    blocked_exclusion: pd.DataFrame,
    specs: pd.DataFrame,
    phase117: pd.DataFrame,
) -> pd.DataFrame:
    ready_days = as_int(metric_value(phase117, "phase117_current_ready_real_anchor_days"))
    days_needed = as_int(metric_value(phase117, "phase117_additional_days_needed_for_min"))
    replay_closed = int(
        (snapshot.empty or snapshot["strategy_replay_allowed"].sum() == 0)
        and (blocked_exclusion.empty or blocked_exclusion["can_enter_replay"].sum() == 0)
        and (specs.empty or specs["strategy_replay_allowed"].sum() == 0)
    )
    return pd.DataFrame(
        [
            {"gate_id": "P128_ALLOWED_FEATURE_SNAPSHOT_EXISTS", "gate_pass": int(not snapshot.empty), "evidence": f"snapshot_rows={len(snapshot)}"},
            {
                "gate_id": "P128_ALL_SNAPSHOT_ROWS_ALLOWED",
                "gate_pass": int(not snapshot.empty and snapshot["candidate_generation_allowed"].eq(1).all()),
                "evidence": "candidate_generation_allowed=1 for every snapshot row",
            },
            {
                "gate_id": "P128_BLOCKED_ROWS_EXCLUDED",
                "gate_pass": int(not blocked_exclusion.empty and blocked_exclusion["can_enter_label_design"].sum() == 0),
                "evidence": f"excluded_blocked_rows={len(blocked_exclusion)}",
            },
            {
                "gate_id": "P128_LABEL_DESIGNS_DECLARED",
                "gate_pass": int(len(specs) == 3),
                "evidence": f"label_design_specs={len(specs)}",
            },
            {"gate_id": "P128_NO_REPLAY", "gate_pass": replay_closed, "evidence": "all replay-permission fields remain 0"},
            {
                "gate_id": "P128_REAL_ANCHOR_STILL_PRIMARY",
                "gate_pass": int(ready_days < 5 and days_needed > 0),
                "evidence": f"ready_real_anchor_days={ready_days}; days_needed={days_needed}",
            },
        ]
    )


def build_acceptance_summary(
    snapshot: pd.DataFrame,
    blocked_exclusion: pd.DataFrame,
    specs: pd.DataFrame,
    gates: pd.DataFrame,
    phase117: pd.DataFrame,
) -> pd.DataFrame:
    clean = int(snapshot["priority_bucket"].eq("P1_clean_allowed").sum()) if not snapshot.empty else 0
    review = int(snapshot["priority_bucket"].eq("P2_allowed_with_realism_review").sum()) if not snapshot.empty else 0
    ready_days = as_int(metric_value(phase117, "phase117_current_ready_real_anchor_days"))
    days_needed = as_int(metric_value(phase117, "phase117_additional_days_needed_for_min"))
    return pd.DataFrame(
        [
            ("phase128_allowed_feature_snapshot_rows", int(len(snapshot)), "Allowed context rows joined to Phase123 feature diagnostics"),
            ("phase128_clean_allowed_context_rows", clean, "Allowed feature rows without realism-review warning"),
            ("phase128_realism_review_context_rows", review, "Allowed feature rows retaining realism-review warning"),
            ("phase128_blocked_exclusion_rows", int(len(blocked_exclusion)), "Phase127 blocked rows excluded from label design"),
            ("phase128_label_design_spec_rows", int(len(specs)), "Next label designs declared"),
            ("phase128_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase128_all_gates_pass", int(gates["gate_pass"].astype(bool).all()) if not gates.empty else 0, "1 means Phase128 obeys no-replay guardrails"),
            ("phase128_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase128_current_ready_real_anchor_days", ready_days, "Real anchor days currently ready from Phase117"),
            ("phase128_additional_real_anchor_days_needed", days_needed, "Additional real anchor days needed before replay unlock"),
            ("phase128_next_best_action", "build_phase129_allowed_context_label_matrix_no_replay_or_continue_real_anchor_acquisition", "Recommended next milestone"),
            ("phase128_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model retained for audit continuity"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase128 Next Label Design Spec",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase128 converts the Phase127 allowed universe into concrete no-replay label-design specifications.",
        "It does not create trading signals, simulate orders, claim profitability, or reopen strategy replay.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase128_next_label_design_spec_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase128(base_dir: Path, output_dir: Path, phase127_dir: Path, phase123_dir: Path, phase117_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    queue = normalize_allowed_queue(read_csv(base_dir / phase127_dir / "allowed_context_precommit_queue.csv"))
    blocked = read_csv(base_dir / phase127_dir / "blocked_context_ledger.csv")
    label_matrix = read_csv(base_dir / phase123_dir / "filter_label_matrix.csv")
    phase117 = read_metric_table(base_dir / phase117_dir / "phase117_real_anchor_acquisition_acceptance_summary.csv")

    snapshot = build_feature_snapshot(queue, label_matrix)
    blocked_exclusion = build_blocked_exclusion_ledger(blocked)
    specs = build_label_design_specs(snapshot)
    guardrails = build_guardrails()
    gates = build_gate_evaluation(snapshot, blocked_exclusion, specs, phase117)
    acceptance = build_acceptance_summary(snapshot, blocked_exclusion, specs, gates, phase117)

    snapshot.to_csv(output_dir / "allowed_context_feature_snapshot.csv", index=False)
    blocked_exclusion.to_csv(output_dir / "blocked_context_exclusion_ledger.csv", index=False)
    specs.to_csv(output_dir / "next_label_design_specs.csv", index=False)
    guardrails.to_csv(output_dir / "label_design_guardrails.csv", index=False)
    gates.to_csv(output_dir / "label_design_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase128_next_label_design_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Next Label Design Specs": specs,
            "Allowed Feature Snapshot Sample": snapshot.head(50),
            "Blocked Exclusion Sample": blocked_exclusion.head(50),
            "Guardrails": guardrails,
            "Gate Evaluation": gates,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase128_next_label_design_spec",
        "strategy_replay_allowed": 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase128",
            generated_utc=generated_utc,
            inputs={
                "phase127_allowed_queue": str(phase127_dir / "allowed_context_precommit_queue.csv"),
                "phase127_blocked_ledger": str(phase127_dir / "blocked_context_ledger.csv"),
                "phase123_filter_label_matrix": str(phase123_dir / "filter_label_matrix.csv"),
                "phase117_acceptance": str(phase117_dir / "phase117_real_anchor_acquisition_acceptance_summary.csv"),
            },
            parameters={
                "design_scope": "allowed_context_label_design_only",
                "blocked_policy": "excluded_from_label_design_and_replay",
                "replay_policy": "closed",
                "forbidden_outputs": FORBIDDEN_SIGNALS,
            },
            outputs={
                "allowed_feature_snapshot": str(output_dir / "allowed_context_feature_snapshot.csv"),
                "blocked_exclusion": str(output_dir / "blocked_context_exclusion_ledger.csv"),
                "label_design_specs": str(output_dir / "next_label_design_specs.csv"),
                "guardrails": str(output_dir / "label_design_guardrails.csv"),
                "gates": str(output_dir / "label_design_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase128_next_label_design_acceptance_summary.csv"),
                "report": str(output_dir / "phase128_next_label_design_spec_report.md"),
                "manifest": str(output_dir / "phase128_next_label_design_spec_manifest.json"),
            },
            random_seed="none_deterministic_label_design_spec",
            scenario_ids="phase128_allowed_context_no_replay_label_design",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_label_design_spec",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase128_next_label_design_spec_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase128 next-label design spec from Phase127 allowed contexts.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--phase127-dir", type=Path, default=DEFAULT_PHASE127_DIR)
    parser.add_argument("--phase123-dir", type=Path, default=DEFAULT_PHASE123_DIR)
    parser.add_argument("--phase117-dir", type=Path, default=DEFAULT_PHASE117_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase128(
        base_dir=args.base_dir,
        output_dir=args.output_dir,
        phase127_dir=args.phase127_dir,
        phase123_dir=args.phase123_dir,
        phase117_dir=args.phase117_dir,
    )


if __name__ == "__main__":
    main()
