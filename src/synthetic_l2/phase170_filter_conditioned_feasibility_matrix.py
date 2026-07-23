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


DEFAULT_PHASE129_DIR = Path("outputs/phase129")
DEFAULT_PHASE130_DIR = Path("outputs/phase130")
DEFAULT_PHASE169_DIR = Path("outputs/phase169")
DEFAULT_OUTPUT_DIR = Path("outputs/phase170")
FORBIDDEN_OUTPUTS = "buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = "missing") -> Any:
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"] if "metric" in frame.columns else pd.Series(dtype=object)
    if rows.empty:
        return default
    return rows.iloc[0]


def to_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def build_feasibility_matrix(label_matrix: pd.DataFrame) -> pd.DataFrame:
    frame = label_matrix.copy()
    for col in [
        "candidate_generation_allowed",
        "strategy_replay_allowed",
        "p129_regime_stability_label",
        "p129_liquidity_opportunity_label",
        "p129_cost_toxicity_refinement_label",
    ]:
        frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0).astype(int)
    frame["is_regime_stable"] = frame["p129_regime_stability_label"].eq(1)
    frame["is_liquidity_opportunity"] = frame["p129_liquidity_opportunity_label"].eq(1)
    frame["is_cost_non_toxic"] = frame["p129_cost_toxicity_refinement_label"].eq(0)
    frame["tier_strict_stable_liquid_non_toxic"] = (
        frame["is_regime_stable"] & frame["is_liquidity_opportunity"] & frame["is_cost_non_toxic"]
    ).astype(int)
    frame["tier_stable_non_toxic"] = (frame["is_regime_stable"] & frame["is_cost_non_toxic"]).astype(int)
    frame["tier_liquid_non_toxic"] = (frame["is_liquidity_opportunity"] & frame["is_cost_non_toxic"]).astype(int)
    frame["phase170_context_score"] = (
        frame["is_regime_stable"].astype(int) * 2
        + frame["is_liquidity_opportunity"].astype(int)
        + frame["is_cost_non_toxic"].astype(int) * 2
        - frame["realism_review_flag"].astype(int)
    )
    frame["phase170_feasibility_bucket"] = "blocked_or_low_quality"
    frame.loc[frame["tier_liquid_non_toxic"].eq(1), "phase170_feasibility_bucket"] = "liquid_non_toxic_context"
    frame.loc[frame["tier_stable_non_toxic"].eq(1), "phase170_feasibility_bucket"] = "stable_non_toxic_context"
    frame.loc[frame["tier_strict_stable_liquid_non_toxic"].eq(1), "phase170_feasibility_bucket"] = "strict_stable_liquid_non_toxic_context"
    frame["phase170_scope"] = "filter_conditioned_context_feasibility_no_replay"
    frame["strategy_replay_allowed"] = 0
    frame["forbidden_outputs"] = FORBIDDEN_OUTPUTS
    keep = [
        "trade_month",
        "symbol",
        "priority_bucket",
        "realism_review_flag",
        "candidate_generation_allowed",
        "rows_scanned",
        "feed_imperfection_rate",
        "median_spread_bps",
        "p90_spread_bps",
        "mean_l1_depth",
        "mean_l5_depth",
        "one_tick_return_std",
        "passive_min_adverse_rate",
        "passive_max_cost_clearing_rate",
        "p129_regime_stability_label",
        "p129_liquidity_opportunity_label",
        "p129_cost_toxicity_refinement_label",
        "p129_cost_toxicity_refinement_bucket",
        "tier_strict_stable_liquid_non_toxic",
        "tier_stable_non_toxic",
        "tier_liquid_non_toxic",
        "phase170_context_score",
        "phase170_feasibility_bucket",
        "phase170_scope",
        "strategy_replay_allowed",
        "forbidden_outputs",
    ]
    return frame[keep].sort_values(["phase170_context_score", "trade_month", "symbol"], ascending=[False, True, True], kind="mergesort")


def build_tier_summary(matrix: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for tier_col, label in [
        ("tier_strict_stable_liquid_non_toxic", "strict_stable_liquid_non_toxic"),
        ("tier_stable_non_toxic", "stable_non_toxic"),
        ("tier_liquid_non_toxic", "liquid_non_toxic"),
    ]:
        subset = matrix[matrix[tier_col].eq(1)]
        rows.append(
            {
                "tier_id": label,
                "rows": int(len(subset)),
                "symbols": int(subset["symbol"].nunique()) if not subset.empty else 0,
                "months": int(subset["trade_month"].nunique()) if not subset.empty else 0,
                "median_spread_bps": float(subset["median_spread_bps"].median()) if not subset.empty else 0.0,
                "median_feed_imperfection_rate": float(subset["feed_imperfection_rate"].median()) if not subset.empty else 0.0,
                "strategy_replay_allowed": 0,
                "interpretation": "context_filter_only_not_signal",
            }
        )
    return pd.DataFrame(rows)


def build_model_evidence(selection: pd.DataFrame) -> pd.DataFrame:
    frame = selection.copy()
    frame["strategy_replay_allowed"] = 0
    frame["phase170_use"] = "diagnostic_filter_only"
    return frame


def build_overlap_audit(forbidden: pd.DataFrame) -> pd.DataFrame:
    blocked_tokens = ";".join(forbidden.get("source_strategy_id", pd.Series(dtype=str)).astype(str).tolist())
    rows = [
        {
            "candidate_design_id": "P170_FILTER_CONTEXT_ONLY",
            "overlaps_blocked_trade_family": 0,
            "blocked_reference_tokens": blocked_tokens,
            "why": "Phase170 emits context filters only and no side/order/P&L replay.",
        },
        {
            "candidate_design_id": "P170_REOPEN_TAKER_PASSIVE_OR_S08",
            "overlaps_blocked_trade_family": 1,
            "blocked_reference_tokens": blocked_tokens,
            "why": "Any replay using closed Phase164, simple passive or Phase167 S08 forms is forbidden.",
        },
    ]
    return pd.DataFrame(rows)


def build_gate_evaluation(matrix: pd.DataFrame, tiers: pd.DataFrame, model_evidence: pd.DataFrame, overlap: pd.DataFrame, phase169_summary: pd.DataFrame) -> pd.DataFrame:
    strict = tiers[tiers["tier_id"].eq("strict_stable_liquid_non_toxic")].iloc[0]
    selected_source = str(metric_value(phase169_summary, "phase169_selected_synthetic_source", "missing"))
    return pd.DataFrame(
        [
            {
                "gate_id": "P170_PHASE169_SOURCE_MATCH",
                "gate_pass": int(selected_source == "P130_FILTER_CONDITIONED_DIAGNOSTICS"),
                "evidence": selected_source,
            },
            {
                "gate_id": "P170_MATRIX_PRESENT",
                "gate_pass": int(len(matrix) > 0),
                "evidence": f"matrix_rows={len(matrix)}",
            },
            {
                "gate_id": "P170_DIAGNOSTIC_MODELS_PRESENT",
                "gate_pass": int(len(model_evidence) >= 3 and model_evidence["model_selected"].astype(bool).all()),
                "evidence": f"selected_models={len(model_evidence)}",
            },
            {
                "gate_id": "P170_STRICT_TIER_TOO_NARROW_FOR_REPLAY",
                "gate_pass": int(int(strict["rows"]) < 50 or int(strict["symbols"]) < 10),
                "evidence": f"strict_rows={int(strict['rows'])}; strict_symbols={int(strict['symbols'])}; strict_months={int(strict['months'])}",
            },
            {
                "gate_id": "P170_BLOCKED_FAMILY_OVERLAP_AUDITED",
                "gate_pass": int(len(overlap) >= 2 and overlap["overlaps_blocked_trade_family"].astype(int).max() == 1),
                "evidence": "overlap audit includes safe context-only row and blocked reopen row",
            },
            {
                "gate_id": "P170_NO_REPLAY",
                "gate_pass": int(matrix["strategy_replay_allowed"].astype(int).sum() == 0 and tiers["strategy_replay_allowed"].astype(int).sum() == 0),
                "evidence": "all replay flags are 0",
            },
        ]
    )


def build_acceptance_summary(matrix: pd.DataFrame, tiers: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    strict = tiers[tiers["tier_id"].eq("strict_stable_liquid_non_toxic")].iloc[0]
    stable = tiers[tiers["tier_id"].eq("stable_non_toxic")].iloc[0]
    liquid = tiers[tiers["tier_id"].eq("liquid_non_toxic")].iloc[0]
    replay_ready = int(int(strict["rows"]) >= 50 and int(strict["symbols"]) >= 10 and int(strict["months"]) >= 6)
    return pd.DataFrame(
        [
            ("phase170_matrix_rows", int(len(matrix)), "Filter-conditioned context rows"),
            ("phase170_strict_context_rows", int(strict["rows"]), "Stable, liquid and non-toxic rows"),
            ("phase170_strict_context_symbols", int(strict["symbols"]), "Strict-tier symbols"),
            ("phase170_strict_context_months", int(strict["months"]), "Strict-tier months"),
            ("phase170_stable_non_toxic_rows", int(stable["rows"]), "Stable and non-toxic rows"),
            ("phase170_liquid_non_toxic_rows", int(liquid["rows"]), "Liquid and non-toxic rows"),
            ("phase170_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase170_all_gates_pass", int(gates["gate_pass"].astype(bool).all()), "1 means matrix obeys no-replay guardrails"),
            ("phase170_replay_ready", replay_ready, "1 means context matrix alone is broad enough to request replay precommit"),
            ("phase170_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase170_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase170_next_best_action", "do_not_replay_filter_only_contexts_design_new_external_or_orderflow_feature_source", "Recommended next milestone"),
            ("phase170_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model retained for audit continuity"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase170 Filter-conditioned Feasibility Matrix",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase170 converts Phase129/130 diagnostic filters into a no-replay context feasibility matrix.",
        "It emits no trade side, no order intent, no fill model, no P&L replay and no profitability claim.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame.head(80)), ""])
    (output_dir / "phase170_filter_conditioned_feasibility_matrix_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase170(phase129_dir: Path, phase130_dir: Path, phase169_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    label_matrix = read_csv(phase129_dir / "allowed_context_label_matrix.csv")
    model_selection = read_csv(phase130_dir / "diagnostic_model_selection.csv")
    phase169_summary = read_csv(phase169_dir / "phase169_post_s08_research_queue_acceptance_summary.csv")
    forbidden = read_csv(phase169_dir / "phase169_forbidden_family_ledger.csv")
    matrix = build_feasibility_matrix(label_matrix)
    tiers = build_tier_summary(matrix)
    model_evidence = build_model_evidence(model_selection)
    overlap = build_overlap_audit(forbidden)
    gates = build_gate_evaluation(matrix, tiers, model_evidence, overlap, phase169_summary)
    acceptance = build_acceptance_summary(matrix, tiers, gates)

    matrix.to_csv(output_dir / "phase170_filter_conditioned_context_matrix.csv", index=False)
    tiers.to_csv(output_dir / "phase170_context_tier_summary.csv", index=False)
    model_evidence.to_csv(output_dir / "phase170_diagnostic_model_evidence.csv", index=False)
    overlap.to_csv(output_dir / "phase170_blocked_family_overlap_audit.csv", index=False)
    gates.to_csv(output_dir / "phase170_feasibility_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase170_filter_conditioned_feasibility_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Context Tier Summary": tiers,
            "Diagnostic Model Evidence": model_evidence,
            "Blocked Family Overlap Audit": overlap,
            "Gate Evaluation": gates,
            "Context Matrix Sample": matrix.head(40),
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase170_filter_conditioned_feasibility_matrix",
        **reproducibility_fields(
            artifact_id="phase170_filter_conditioned_feasibility_matrix",
            generated_utc=generated_utc,
            inputs={
                "phase129_label_matrix": str(phase129_dir / "allowed_context_label_matrix.csv"),
                "phase130_model_selection": str(phase130_dir / "diagnostic_model_selection.csv"),
                "phase169_research_queue": str(phase169_dir / "phase169_next_research_queue.csv"),
                "phase169_forbidden_family_ledger": str(phase169_dir / "phase169_forbidden_family_ledger.csv"),
            },
            parameters={
                "strict_replay_width_requirement": "rows>=50_symbols>=10_months>=6",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
                "strategy_replay_allowed": 0,
            },
            outputs={
                "context_matrix": str(output_dir / "phase170_filter_conditioned_context_matrix.csv"),
                "tier_summary": str(output_dir / "phase170_context_tier_summary.csv"),
                "model_evidence": str(output_dir / "phase170_diagnostic_model_evidence.csv"),
                "overlap_audit": str(output_dir / "phase170_blocked_family_overlap_audit.csv"),
                "acceptance_summary": str(output_dir / "phase170_filter_conditioned_feasibility_acceptance_summary.csv"),
            },
            random_seed="none_deterministic_phase170_matrix",
            scenario_ids="phase129_phase130_filter_diagnostics_post_phase169",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_no_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase170_filter_conditioned_feasibility_matrix_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase129-dir", type=Path, default=DEFAULT_PHASE129_DIR)
    parser.add_argument("--phase130-dir", type=Path, default=DEFAULT_PHASE130_DIR)
    parser.add_argument("--phase169-dir", type=Path, default=DEFAULT_PHASE169_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase170(args.phase129_dir, args.phase130_dir, args.phase169_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
