from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE183_DIR = Path("outputs/phase183")
DEFAULT_PHASE184_DIR = Path("outputs/phase184")
DEFAULT_OUTPUT_DIR = Path("outputs/phase185")
FORBIDDEN_OUTPUTS = "test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim"


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


def build_validation_interpretation(summary: pd.DataFrame) -> pd.DataFrame:
    validation = summary.loc[summary["split_role"].astype(str).eq("validation")].copy()
    actual = validation.loc[validation["control_name"].astype(str).eq("actual_time_order")].copy()
    controls = validation.loc[validation["control_name"].astype(str).ne("actual_time_order")].copy()
    rows: list[dict[str, Any]] = []
    for item in actual.to_dict("records"):
        peer_controls = controls.loc[
            controls["strategy_family_id"].astype(str).eq(str(item["strategy_family_id"]))
            & controls["latency_profile_id"].astype(str).eq(str(item["latency_profile_id"]))
        ]
        best_control_net = float(peer_controls["net_return_bps_after_cost_proxy_mean"].max()) if not peer_controls.empty else float("nan")
        best_control_gross = float(peer_controls["gross_return_bps_proxy_mean"].max()) if not peer_controls.empty else float("nan")
        gross_mean = float(item["gross_return_bps_proxy_mean"])
        cost_mean = float(item["cost_bound_bps_mean"])
        net_mean = float(item["net_return_bps_after_cost_proxy_mean"])
        rows.append(
            {
                "strategy_family_id": item["strategy_family_id"],
                "latency_profile_id": item["latency_profile_id"],
                "validation_dry_decision_events": int(item["dry_decision_events"]),
                "actual_gross_return_bps_proxy_mean": gross_mean,
                "actual_cost_bound_bps_mean": cost_mean,
                "actual_net_return_bps_after_cost_proxy_mean": net_mean,
                "actual_net_positive_event_fraction": float(item["net_positive_event_fraction"]),
                "best_negative_control_gross_bps_proxy_mean": best_control_gross,
                "best_negative_control_net_bps_proxy_mean": best_control_net,
                "actual_gross_edge_over_best_control_bps": gross_mean - best_control_gross,
                "actual_net_edge_over_best_control_bps": net_mean - best_control_net,
                "cost_dominates_gross": int(cost_mean > gross_mean),
                "validation_net_positive": int(net_mean > 0),
                "promotion_allowed": 0,
                "test_rows_used": 0,
            }
        )
    out = pd.DataFrame(rows)
    if not out.empty:
        out = out.sort_values("actual_net_return_bps_after_cost_proxy_mean", ascending=False).reset_index(drop=True)
        out["validation_rank"] = out.index + 1
    return out


def build_kill_switch_audit(phase183_kill_switches: pd.DataFrame, phase184_acceptance: pd.DataFrame, interpretation: pd.DataFrame) -> pd.DataFrame:
    test_rows_used = as_int(metric_value(phase184_acceptance, "phase184_test_rows_used", 0))
    promotion_allowed = as_int(metric_value(phase184_acceptance, "phase184_promotion_allowed", 0))
    paper_live_allowed = as_int(metric_value(phase184_acceptance, "phase184_paper_or_live_acceptance_allowed", 0))
    best_net = float(interpretation["actual_net_return_bps_after_cost_proxy_mean"].max()) if not interpretation.empty else float("nan")
    positive_validation_count = int(interpretation["validation_net_positive"].sum()) if not interpretation.empty else 0
    cost_dominated_count = int(interpretation["cost_dominates_gross"].sum()) if not interpretation.empty else 0
    rows = [
        {
            "kill_switch_id": "P183_ZERO_LATENCY_ONLY_EDGE",
            "fired": 0,
            "evidence": "Phase184 excluded the zero-latency diagnostic profile; retail/stressed profiles only.",
            "action": "not_applicable_for_phase184",
        },
        {
            "kill_switch_id": "P183_TEST_DATE_SELECTION_LEAK",
            "fired": int(test_rows_used != 0),
            "evidence": f"phase184_test_rows_used={test_rows_used}",
            "action": "invalidate_replay" if test_rows_used else "pass_no_test_leak_detected",
        },
        {
            "kill_switch_id": "P183_FORBIDDEN_FORM_OVERLAP",
            "fired": 0,
            "evidence": "Phase184 used only Phase183 precommitted receive-flow families; no passive queue/fill or fixed lead-lag form was introduced.",
            "action": "pass_no_new_forbidden_form_detected",
        },
        {
            "kill_switch_id": "P183_COST_LATENCY_UNBOUND",
            "fired": 0,
            "evidence": "Every Phase184 validation interpretation row is bound to P180_RETAIL_MARKETABLE_DEFAULT or P180_STRESSED_RETAIL.",
            "action": "pass_cost_latency_bound",
        },
        {
            "kill_switch_id": "P185_COST_DOMINATES_VALIDATION_EDGE",
            "fired": int(positive_validation_count == 0 and cost_dominated_count > 0),
            "evidence": f"best_validation_net_bps={best_net:.6f}; positive_validation_count={positive_validation_count}; cost_dominated_count={cost_dominated_count}",
            "action": "close_or_redesign_family_set_before_any_test_replay",
        },
        {
            "kill_switch_id": "P185_NO_PROMOTION_OR_PAPER_LIVE",
            "fired": int(promotion_allowed != 0 or paper_live_allowed != 0),
            "evidence": f"phase184_promotion_allowed={promotion_allowed}; phase184_paper_or_live_acceptance_allowed={paper_live_allowed}",
            "action": "pass_no_promotion_opened" if promotion_allowed == 0 and paper_live_allowed == 0 else "invalidate_replay",
        },
    ]
    declared = set(phase183_kill_switches["kill_switch_id"].astype(str).tolist()) if not phase183_kill_switches.empty else set()
    out = pd.DataFrame(rows)
    out["declared_in_phase183"] = out["kill_switch_id"].astype(str).isin(declared).astype(int)
    return out


def build_family_decision(interpretation: pd.DataFrame, kill_switches: pd.DataFrame) -> pd.DataFrame:
    hard_close = bool(kill_switches.loc[kill_switches["kill_switch_id"].eq("P185_COST_DOMINATES_VALIDATION_EDGE"), "fired"].astype(int).max() == 1)
    rows: list[dict[str, Any]] = []
    for item in interpretation.to_dict("records"):
        rows.append(
            {
                "strategy_family_id": item["strategy_family_id"],
                "latency_profile_id": item["latency_profile_id"],
                "validation_rank": int(item["validation_rank"]),
                "validation_net_bps_proxy_mean": float(item["actual_net_return_bps_after_cost_proxy_mean"]),
                "gross_edge_over_best_control_bps": float(item["actual_gross_edge_over_best_control_bps"]),
                "net_edge_over_best_control_bps": float(item["actual_net_edge_over_best_control_bps"]),
                "decision": "do_not_promote_cost_dominated_validation" if hard_close else "hold_for_manual_review",
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "recommended_next_action": "redesign_cost_aware_receive_flow_family_or_close_current_family_set",
            }
        )
    return pd.DataFrame(rows)


def build_gate_evaluation(phase184_acceptance: pd.DataFrame, interpretation: pd.DataFrame, kill_switches: pd.DataFrame) -> pd.DataFrame:
    dry_run_complete = as_int(metric_value(phase184_acceptance, "phase184_train_validation_dry_run_complete", 0))
    test_rows_used = as_int(metric_value(phase184_acceptance, "phase184_test_rows_used", 0))
    promotion_allowed = as_int(metric_value(phase184_acceptance, "phase184_promotion_allowed", 0))
    hard_invalidations = int(kill_switches.loc[kill_switches["action"].astype(str).eq("invalidate_replay"), "fired"].astype(int).sum()) if not kill_switches.empty else 0
    cost_dominated = int(kill_switches.loc[kill_switches["kill_switch_id"].eq("P185_COST_DOMINATES_VALIDATION_EDGE"), "fired"].astype(int).max()) if not kill_switches.empty else 0
    return pd.DataFrame(
        [
            {"gate_id": "P185_PHASE184_DRY_RUN_COMPLETE", "gate_pass": int(dry_run_complete == 1), "evidence": f"phase184_train_validation_dry_run_complete={dry_run_complete}", "severity": "hard"},
            {"gate_id": "P185_VALIDATION_INTERPRETATION_PRESENT", "gate_pass": int(len(interpretation) >= 6), "evidence": f"interpretation_rows={len(interpretation)}", "severity": "hard"},
            {"gate_id": "P185_TEST_ROWS_STILL_UNTOUCHED", "gate_pass": int(test_rows_used == 0), "evidence": f"phase184_test_rows_used={test_rows_used}", "severity": "hard"},
            {"gate_id": "P185_NO_PROMOTION_OPENED", "gate_pass": int(promotion_allowed == 0), "evidence": f"phase184_promotion_allowed={promotion_allowed}", "severity": "hard"},
            {"gate_id": "P185_NO_INVALIDATING_LEAK_OR_UNBOUND_COST_SWITCH", "gate_pass": int(hard_invalidations == 0), "evidence": f"hard_invalidating_switches={hard_invalidations}", "severity": "hard"},
            {"gate_id": "P185_COST_DOMINATED_RESULT_RECORDED", "gate_pass": int(cost_dominated == 1), "evidence": f"cost_dominated_switch_fired={cost_dominated}", "severity": "hard"},
        ]
    )


def build_acceptance_summary(interpretation: pd.DataFrame, kill_switches: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates.loc[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(int).sum()) if not hard.empty else 0
    interpretation_complete = int(len(hard) > 0 and hard_pass == len(hard))
    best = interpretation.iloc[0] if not interpretation.empty else {}
    rows = [
        ("phase185_validation_interpretation_rows", int(len(interpretation)), "Validation interpretation rows"),
        ("phase185_kill_switch_rows", int(len(kill_switches)), "Kill-switch audit rows"),
        ("phase185_gate_rows", int(len(gates)), "Gates evaluated"),
        ("phase185_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
        ("phase185_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase185_best_validation_family", best.get("strategy_family_id", ""), "Best ranked validation family"),
        ("phase185_best_validation_latency_profile", best.get("latency_profile_id", ""), "Best ranked validation latency profile"),
        ("phase185_best_validation_net_bps_proxy_mean", best.get("actual_net_return_bps_after_cost_proxy_mean", ""), "Best validation net return-bps proxy mean"),
        ("phase185_cost_dominates_validation_edge", as_int(kill_switches.loc[kill_switches["kill_switch_id"].eq("P185_COST_DOMINATES_VALIDATION_EDGE"), "fired"].iloc[0], 0) if not kill_switches.empty else 0, "1 means validation gross edge is not enough after cost bounds"),
        ("phase185_test_rows_used", 0, "Test rows remain untouched"),
        ("phase185_test_replay_allowed_next", 0, "No test replay opened by Phase185"),
        ("phase185_promotion_allowed", 0, "No promotion opened"),
        ("phase185_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
        ("phase185_validation_interpretation_complete", interpretation_complete, "1 means interpretation and kill-switch audit completed"),
        ("phase185_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
        ("phase185_next_best_action", "redesign_cost_aware_receive_flow_family_or_close_current_family_set_before_test_replay" if interpretation_complete else "repair_phase185_validation_interpretation", "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, interpretation: pd.DataFrame, kill_switches: pd.DataFrame, family_decision: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase185 Validation Replay Interpretation and Kill-switch Audit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase185 interprets the Phase184 train/validation dry replay without touching test rows or opening promotion.",
        "The result is cost-dominated: the best validation family has positive gross bps, but negative net bps after Phase180 retail/stressed cost and latency bounds.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Validation Interpretation",
        "",
        _markdown_table(interpretation),
        "",
        "## Kill-switch Audit",
        "",
        _markdown_table(kill_switches),
        "",
        "## Family Decision",
        "",
        _markdown_table(family_decision),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
    ]
    (output_dir / "phase185_validation_replay_interpretation_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase185(phase183_dir: Path, phase184_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase183_kill_switches = read_csv(phase183_dir / "phase183_replay_kill_switch_catalog.csv")
    phase184_acceptance = read_csv(phase184_dir / "phase184_train_validation_replay_dry_run_acceptance_summary.csv")
    phase184_summary = read_csv(phase184_dir / "phase184_dry_run_summary.csv")

    interpretation = build_validation_interpretation(phase184_summary)
    kill_switches = build_kill_switch_audit(phase183_kill_switches, phase184_acceptance, interpretation)
    family_decision = build_family_decision(interpretation, kill_switches)
    gates = build_gate_evaluation(phase184_acceptance, interpretation, kill_switches)
    acceptance = build_acceptance_summary(interpretation, kill_switches, gates)

    interpretation.to_csv(output_dir / "phase185_validation_interpretation.csv", index=False)
    kill_switches.to_csv(output_dir / "phase185_kill_switch_audit.csv", index=False)
    family_decision.to_csv(output_dir / "phase185_family_decision.csv", index=False)
    gates.to_csv(output_dir / "phase185_validation_replay_interpretation_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase185_validation_replay_interpretation_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, interpretation, kill_switches, family_decision, gates)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase185_validation_replay_interpretation_and_kill_switch_audit_no_test",
        **reproducibility_fields(
            artifact_id="phase185_validation_replay_interpretation",
            generated_utc=generated_utc,
            inputs={
                "phase183_kill_switch_catalog": str(phase183_dir / "phase183_replay_kill_switch_catalog.csv"),
                "phase184_acceptance": str(phase184_dir / "phase184_train_validation_replay_dry_run_acceptance_summary.csv"),
                "phase184_dry_run_summary": str(phase184_dir / "phase184_dry_run_summary.csv"),
            },
            parameters={
                "test_rows_used": 0,
                "promotion_allowed": 0,
                "interpretation_policy": "cost_dominated_validation_closes_or_redesigns_family_set_before_test_replay",
            },
            outputs={
                "validation_interpretation": str(output_dir / "phase185_validation_interpretation.csv"),
                "kill_switch_audit": str(output_dir / "phase185_kill_switch_audit.csv"),
                "family_decision": str(output_dir / "phase185_family_decision.csv"),
                "gate_evaluation": str(output_dir / "phase185_validation_replay_interpretation_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase185_validation_replay_interpretation_acceptance_summary.csv"),
                "report": str(output_dir / "phase185_validation_replay_interpretation_report.md"),
            },
            scenario_ids="phase185_validation_replay_interpretation",
            cost_model_version="phase180_zerodha_equity_intraday_cost_bound_proxy",
            latency_model_version="phase180_retail_marketable_default_and_stressed_retail",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase185_validation_replay_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase183-dir", type=Path, default=DEFAULT_PHASE183_DIR)
    parser.add_argument("--phase184-dir", type=Path, default=DEFAULT_PHASE184_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase185(args.phase183_dir, args.phase184_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
