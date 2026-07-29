from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE222_DIR = Path("outputs/phase222")
DEFAULT_OUTPUT_DIR = Path("outputs/phase223")
MIN_DECISION_EVENTS_FOR_INTERPRETATION = 100
MIN_VALIDATION_NET_AFTER_COST_BPS = 0.0
MIN_ACTUAL_VS_SHUFFLE_NET_EDGE_BPS = 0.0
REQUIRED_COST_PROFILES = ["P180_RETAIL_MARKETABLE_DEFAULT", "P180_STRESSED_RETAIL"]
FORBIDDEN_OUTPUTS = "test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export;broader_replay_unlock"
NEXT_ACTION = "run_phase224_event_only_signal_replay_closure_or_redesign_precommit_no_test"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = "") -> Any:
    if frame.empty or "metric" not in frame.columns or "value" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def numeric(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = frame.copy()
    for col in columns:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def build_candidate_interpretation(summary: pd.DataFrame) -> pd.DataFrame:
    if summary.empty:
        return pd.DataFrame()
    frame = summary[
        summary["split_role"].astype(str).eq("validation")
        & summary["latency_profile_id"].astype(str).isin(REQUIRED_COST_PROFILES)
    ].copy()
    if frame.empty:
        return frame
    frame = numeric(
        frame,
        [
            "horizon_sec",
            "threshold",
            "decision_events",
            "hit_rate",
            "gross_label_payoff_bps_proxy_mean",
            "cost_bound_bps_mean",
            "net_after_cost_bps_proxy_mean",
            "net_positive_event_fraction",
            "test_rows_used",
            "promotion_allowed",
            "paper_or_live_acceptance_allowed",
            "profitability_claim_allowed",
        ],
    )
    keys = [
        "phase221_candidate_id",
        "phase219_model_fit_id",
        "model_family",
        "target_label",
        "horizon_sec",
        "threshold",
        "latency_profile_id",
    ]
    actual = frame[frame["control_name"].astype(str).eq("actual_label_order")].copy()
    shuffle = frame[frame["control_name"].astype(str).eq("shuffled_event_label_control")][keys + ["net_after_cost_bps_proxy_mean", "hit_rate"]].rename(
        columns={
            "net_after_cost_bps_proxy_mean": "shuffle_net_after_cost_bps_proxy_mean",
            "hit_rate": "shuffle_hit_rate",
        }
    )
    interpretation = actual.merge(shuffle, on=keys, how="left")
    interpretation["actual_vs_shuffle_net_edge_bps"] = interpretation["net_after_cost_bps_proxy_mean"] - interpretation["shuffle_net_after_cost_bps_proxy_mean"]
    interpretation["actual_vs_shuffle_hit_rate_edge"] = interpretation["hit_rate"] - interpretation["shuffle_hit_rate"]
    interpretation["passes_min_decision_events"] = (interpretation["decision_events"] >= MIN_DECISION_EVENTS_FOR_INTERPRETATION).astype(int)
    interpretation["passes_cost_positive"] = (interpretation["net_after_cost_bps_proxy_mean"] > MIN_VALIDATION_NET_AFTER_COST_BPS).astype(int)
    interpretation["passes_actual_vs_shuffle_net"] = (interpretation["actual_vs_shuffle_net_edge_bps"] > MIN_ACTUAL_VS_SHUFFLE_NET_EDGE_BPS).astype(int)
    interpretation["cost_dominates_gross_edge"] = (interpretation["cost_bound_bps_mean"] >= interpretation["gross_label_payoff_bps_proxy_mean"].abs()).astype(int)
    pass_cols = ["passes_min_decision_events", "passes_cost_positive", "passes_actual_vs_shuffle_net"]
    interpretation["interpretation_pass"] = interpretation[pass_cols].min(axis=1).astype(int)
    interpretation["broader_replay_allowed_next"] = 0
    interpretation["test_replay_allowed_next"] = 0
    interpretation["promotion_allowed"] = 0
    interpretation["paper_or_live_acceptance_allowed"] = 0
    interpretation["profitability_claim_allowed"] = 0
    interpretation["verdict"] = interpretation.apply(
        lambda r: "insufficient_cost_positive_validation_edge" if int(r["interpretation_pass"]) == 0 else "cost_positive_validation_candidate_requires_new_precommit",
        axis=1,
    )
    return interpretation.sort_values(
        ["interpretation_pass", "net_after_cost_bps_proxy_mean", "actual_vs_shuffle_net_edge_bps", "decision_events"],
        ascending=[False, False, False, False],
    ).reset_index(drop=True)


def build_profile_summary(interpretation: pd.DataFrame) -> pd.DataFrame:
    if interpretation.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for profile, part in interpretation.groupby("latency_profile_id", sort=True):
        net = pd.to_numeric(part["net_after_cost_bps_proxy_mean"], errors="coerce")
        edge = pd.to_numeric(part["actual_vs_shuffle_net_edge_bps"], errors="coerce")
        passing = pd.to_numeric(part["interpretation_pass"], errors="coerce").fillna(0).astype(int)
        cost_dom = pd.to_numeric(part["cost_dominates_gross_edge"], errors="coerce").fillna(0).astype(int)
        rows.append(
            {
                "latency_profile_id": profile,
                "validation_rows": len(part),
                "decision_events": int(pd.to_numeric(part["decision_events"], errors="coerce").fillna(0).sum()),
                "best_validation_net_after_cost_bps_proxy": float(net.max()) if not net.dropna().empty else 0.0,
                "worst_validation_net_after_cost_bps_proxy": float(net.min()) if not net.dropna().empty else 0.0,
                "positive_net_rows": int((net > 0).sum()),
                "actual_beats_shuffle_rows": int((edge > 0).sum()),
                "passing_interpretation_rows": int(passing.sum()),
                "cost_dominates_rows": int(cost_dom.sum()),
                "broader_replay_allowed_next": 0,
                "test_replay_allowed_next": 0,
            }
        )
    return pd.DataFrame(rows)


def build_target_summary(interpretation: pd.DataFrame) -> pd.DataFrame:
    if interpretation.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    group_cols = ["target_label", "horizon_sec"]
    for keys, part in interpretation.groupby(group_cols, sort=True):
        target_label, horizon_sec = keys
        net = pd.to_numeric(part["net_after_cost_bps_proxy_mean"], errors="coerce")
        decisions = pd.to_numeric(part["decision_events"], errors="coerce").fillna(0)
        rows.append(
            {
                "target_label": target_label,
                "horizon_sec": int(horizon_sec),
                "validation_profile_threshold_rows": len(part),
                "decision_events": int(decisions.sum()),
                "active_rows": int((decisions > 0).sum()),
                "best_validation_net_after_cost_bps_proxy": float(net.max()) if not net.dropna().empty else 0.0,
                "positive_net_rows": int((net > 0).sum()),
                "interpretation_pass_rows": int(pd.to_numeric(part["interpretation_pass"], errors="coerce").fillna(0).sum()),
            }
        )
    return pd.DataFrame(rows)


def build_phase224_work_order(interpretation: pd.DataFrame) -> pd.DataFrame:
    passing_rows = int(pd.to_numeric(interpretation["interpretation_pass"], errors="coerce").fillna(0).sum()) if not interpretation.empty else 0
    positive_rows = int((pd.to_numeric(interpretation["net_after_cost_bps_proxy_mean"], errors="coerce") > 0).sum()) if not interpretation.empty else 0
    return pd.DataFrame(
        [
            {
                "phase224_work_order_id": "P224_EVENT_ONLY_SIGNAL_REPLAY_CLOSURE_OR_REDESIGN_PRECOMMIT",
                "work_order": "Close the current event-only signal replay branch for broader replay/test unless a material redesign is precommitted from Phase223 evidence.",
                "phase223_passing_interpretation_rows": passing_rows,
                "phase223_positive_net_validation_rows": positive_rows,
                "recommended_decision": "close_current_signal_replay_candidate_set_and_precommit_redesign",
                "allowed_next_scope": "closure_or_redesign_precommit_only_no_test_no_broader_replay",
                "broader_replay_allowed_next": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "profitability_claim_allowed": 0,
            }
        ]
    )


def build_forbidden_execution_ledger() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "forbidden_output": item,
                "emitted_in_phase223": 0,
                "allowed_in_phase223": 0,
                "rationale": "Phase223 interprets aggregate Phase222 validation replay outputs only and emits no broader replay, test, order/fill, P&L, promotion, paper/live, row-level prediction, or profitability artifact.",
            }
            for item in FORBIDDEN_OUTPUTS.split(";")
        ]
    )


def build_gates(phase222: pd.DataFrame, interpretation: pd.DataFrame, profile_summary: pd.DataFrame, work_order: pd.DataFrame, forbidden: pd.DataFrame) -> pd.DataFrame:
    phase222_complete = as_int(metric_value(phase222, "phase222_event_only_train_validation_signal_replay_dry_run_complete", 0))
    validation_rows = len(interpretation)
    profile_rows = len(profile_summary)
    passing_rows = int(pd.to_numeric(interpretation["interpretation_pass"], errors="coerce").fillna(0).sum()) if not interpretation.empty else 0
    positive_rows = int((pd.to_numeric(interpretation["net_after_cost_bps_proxy_mean"], errors="coerce") > 0).sum()) if not interpretation.empty else 0
    test_rows_used = int(pd.to_numeric(interpretation["test_rows_used"], errors="coerce").fillna(0).sum()) if not interpretation.empty else 0
    forbidden_emitted = int(pd.to_numeric(forbidden["emitted_in_phase223"], errors="coerce").fillna(0).sum()) if not forbidden.empty else 1
    forbidden_flags = 0
    for frame in [interpretation, profile_summary, work_order]:
        for col in ["broader_replay_allowed_next", "test_replay_allowed_next", "promotion_allowed", "paper_or_live_acceptance_allowed", "profitability_claim_allowed"]:
            if not frame.empty and col in frame.columns:
                forbidden_flags += int(pd.to_numeric(frame[col], errors="coerce").fillna(0).sum())
    return pd.DataFrame(
        [
            ("P223_PHASE222_COMPLETE", phase222_complete == 1, f"phase222_complete={phase222_complete}", "hard"),
            ("P223_VALIDATION_INTERPRETATION_RECORDED", validation_rows == 40, f"validation_rows={validation_rows}", "hard"),
            ("P223_COST_PROFILE_INTERPRETATION_RECORDED", profile_rows == len(REQUIRED_COST_PROFILES), f"profile_rows={profile_rows}", "hard"),
            ("P223_NO_COST_POSITIVE_VALIDATION_PASS", passing_rows == 0 and positive_rows == 0, f"passing_rows={passing_rows}; positive_rows={positive_rows}", "hard"),
            ("P223_PHASE224_WORK_ORDER_RECORDED", len(work_order) == 1, f"work_order_rows={len(work_order)}", "hard"),
            ("P223_TEST_ROWS_UNTOUCHED", test_rows_used == 0, f"test_rows_used={test_rows_used}", "hard"),
            ("P223_FORBIDDEN_OUTPUTS_CLEAN", forbidden_emitted == 0 and forbidden_flags == 0, f"forbidden_emitted={forbidden_emitted}; forbidden_flags={forbidden_flags}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(interpretation: pd.DataFrame, profile_summary: pd.DataFrame, target_summary: pd.DataFrame, work_order: pd.DataFrame, forbidden: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    net = pd.to_numeric(interpretation["net_after_cost_bps_proxy_mean"], errors="coerce") if not interpretation.empty else pd.Series(dtype=float)
    edge = pd.to_numeric(interpretation["actual_vs_shuffle_net_edge_bps"], errors="coerce") if not interpretation.empty else pd.Series(dtype=float)
    decisions = pd.to_numeric(interpretation["decision_events"], errors="coerce").fillna(0) if not interpretation.empty else pd.Series(dtype=float)
    pass_rows = int(pd.to_numeric(interpretation["interpretation_pass"], errors="coerce").fillna(0).sum()) if not interpretation.empty else 0
    positive_rows = int((net > 0).sum()) if not interpretation.empty else 0
    cost_dominates_rows = int(pd.to_numeric(interpretation["cost_dominates_gross_edge"], errors="coerce").fillna(0).sum()) if not interpretation.empty else 0
    return pd.DataFrame(
        [
            ("phase223_interpretation_rows", len(interpretation), "Validation interpretation rows"),
            ("phase223_profile_summary_rows", len(profile_summary), "Cost profile summary rows"),
            ("phase223_target_summary_rows", len(target_summary), "Target/horizon summary rows"),
            ("phase223_validation_decision_events", int(decisions.sum()), "Validation decision events interpreted"),
            ("phase223_positive_net_validation_rows", positive_rows, "Rows with positive validation net-after-cost proxy"),
            ("phase223_passing_interpretation_rows", pass_rows, "Rows passing interpretation gates"),
            ("phase223_cost_dominates_rows", cost_dominates_rows, "Rows where cost bound dominates gross proxy edge"),
            ("phase223_best_validation_net_after_cost_bps_proxy", float(net.max()) if not net.dropna().empty else 0.0, "Best validation net-after-cost proxy"),
            ("phase223_worst_validation_net_after_cost_bps_proxy", float(net.min()) if not net.dropna().empty else 0.0, "Worst validation net-after-cost proxy"),
            ("phase223_best_actual_vs_shuffle_net_edge_bps", float(edge.max()) if not edge.dropna().empty else 0.0, "Best actual-vs-shuffled net edge"),
            ("phase223_phase224_work_order_rows", len(work_order), "Phase224 work-order rows"),
            ("phase223_forbidden_execution_rows", len(forbidden), "Forbidden execution rows"),
            ("phase223_gate_rows", len(gates), "Gates evaluated"),
            ("phase223_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase223_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase223_event_only_signal_replay_validation_interpretation_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase223 completed"),
            ("phase223_broader_replay_allowed_next", 0, "No broader replay opened"),
            ("phase223_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase223_test_rows_used", 0, "No sealed test rows used"),
            ("phase223_promotion_allowed", 0, "No promotion opened"),
            ("phase223_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase223_profitability_claim_allowed", 0, "No profitability claim is allowed"),
            ("phase223_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase223_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase223 Event-only Signal Replay Validation Interpretation",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase223 interprets Phase222 aggregate train/validation signal replay outputs.",
        "It decides whether broader replay or sealed test should remain closed; it emits no order/fill, P&L, row-level prediction, promotion, paper/live, or profitability artifact.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase223_event_only_signal_replay_validation_interpretation_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase223(phase222_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase222 = read_csv(phase222_dir / "phase222_signal_replay_acceptance_summary.csv")
    replay_summary = read_csv(phase222_dir / "phase222_signal_replay_summary.csv")
    threshold_activation = read_csv(phase222_dir / "phase222_threshold_activation_summary.csv")
    negative_controls = read_csv(phase222_dir / "phase222_negative_control_summary.csv")

    interpretation = build_candidate_interpretation(replay_summary)
    profile_summary = build_profile_summary(interpretation)
    target_summary = build_target_summary(interpretation)
    work_order = build_phase224_work_order(interpretation)
    forbidden = build_forbidden_execution_ledger()
    gates = build_gates(phase222, interpretation, profile_summary, work_order, forbidden)
    acceptance = build_acceptance(interpretation, profile_summary, target_summary, work_order, forbidden, gates)

    interpretation.to_csv(output_dir / "phase223_validation_interpretation.csv", index=False)
    profile_summary.to_csv(output_dir / "phase223_cost_profile_summary.csv", index=False)
    target_summary.to_csv(output_dir / "phase223_target_horizon_summary.csv", index=False)
    work_order.to_csv(output_dir / "phase223_phase224_work_order.csv", index=False)
    forbidden.to_csv(output_dir / "phase223_execution_forbidden_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase223_validation_interpretation_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase223_validation_interpretation_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Validation Interpretation": interpretation,
            "Cost Profile Summary": profile_summary,
            "Target Horizon Summary": target_summary,
            "Phase224 Work Order": work_order,
            "Forbidden Execution Ledger": forbidden,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase223_event_only_signal_replay_validation_interpretation_no_test",
        **reproducibility_fields(
            artifact_id="phase223_event_only_signal_replay_validation_interpretation",
            generated_utc=generated,
            inputs={
                "phase222_acceptance": str(phase222_dir / "phase222_signal_replay_acceptance_summary.csv"),
                "phase222_replay_summary": str(phase222_dir / "phase222_signal_replay_summary.csv"),
                "phase222_threshold_activation": str(phase222_dir / "phase222_threshold_activation_summary.csv"),
                "phase222_negative_controls": str(phase222_dir / "phase222_negative_control_summary.csv"),
            },
            parameters={
                "required_cost_profiles": ";".join(REQUIRED_COST_PROFILES),
                "min_decision_events_for_interpretation": str(MIN_DECISION_EVENTS_FOR_INTERPRETATION),
                "min_validation_net_after_cost_bps": str(MIN_VALIDATION_NET_AFTER_COST_BPS),
                "min_actual_vs_shuffle_net_edge_bps": str(MIN_ACTUAL_VS_SHUFFLE_NET_EDGE_BPS),
                "broader_replay_allowed_next": "0",
                "test_replay_allowed_next": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "interpretation": str(output_dir / "phase223_validation_interpretation.csv"),
                "profile_summary": str(output_dir / "phase223_cost_profile_summary.csv"),
                "target_summary": str(output_dir / "phase223_target_horizon_summary.csv"),
                "work_order": str(output_dir / "phase223_phase224_work_order.csv"),
                "forbidden": str(output_dir / "phase223_execution_forbidden_ledger.csv"),
                "gates": str(output_dir / "phase223_validation_interpretation_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase223_validation_interpretation_acceptance_summary.csv"),
                "report": str(output_dir / "phase223_event_only_signal_replay_validation_interpretation_report.md"),
            },
            scenario_ids="phase223_event_only_signal_replay_validation_interpretation_no_test",
            cost_model_version="phase180_zerodha_equity_cost_component_catalog_bound",
            latency_model_version="phase180_latency_slippage_profile_catalog_bound",
            base_dir=base_dir,
        ),
        "phase222_rows": {
            "replay_summary_rows": int(len(replay_summary)),
            "threshold_activation_rows": int(len(threshold_activation)),
            "negative_control_rows": int(len(negative_controls)),
        },
    }
    (output_dir / "phase223_validation_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Interpret Phase222 event-only signal replay validation results without opening test replay.")
    parser.add_argument("--phase222-dir", type=Path, default=DEFAULT_PHASE222_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase223(args.phase222_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
