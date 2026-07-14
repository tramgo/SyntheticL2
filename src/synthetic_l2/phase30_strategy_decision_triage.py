from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


ALPHA_STRATEGIES = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09"]
RUNNABLE_PROXY_STRATEGIES = ["S01", "S02", "S05", "S07", "S09"]
PARTIAL_PROXY_STRATEGIES = ["S03", "S04", "S06", "S08"]
NON_ALPHA_CONTROLS = ["S10", "S11"]


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def _metric(frame: pd.DataFrame, metric: str, default: int | float = 0) -> int | float:
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    value = rows.iloc[0]
    try:
        as_float = float(value)
    except (TypeError, ValueError):
        return default
    return int(as_float) if as_float.is_integer() else as_float


def _best_value(frame: pd.DataFrame, mask: pd.Series, column: str) -> float | None:
    values = frame.loc[mask, column]
    if values.empty:
        return None
    return float(values.max())


def _strategy_name(strategy_id: str, m02: pd.DataFrame) -> str:
    rows = m02.loc[m02["strategy_id"].eq(strategy_id), "name"]
    return str(rows.iloc[0]) if len(rows) else strategy_id


def build_execution_evidence(paths: dict[str, Path]) -> pd.DataFrame:
    phase25 = _read_csv(paths["phase25_summary"])
    phase25_overall = _read_csv(paths["phase25_overall"])
    phase26 = _read_csv(paths["phase26_candidates"])
    phase26_overall = _read_csv(paths["phase26_overall"])
    phase27_family = _read_csv(paths["phase27_family"])
    phase27_overall = _read_csv(paths["phase27_overall"])
    phase28_support = _read_csv(paths["phase28_support"])
    phase28_overall = _read_csv(paths["phase28_overall"])
    phase29 = _read_csv(paths["phase29_summary"])
    phase29_candidates = _read_csv(paths["phase29_candidates"])
    phase29_overall = _read_csv(paths["phase29_overall"])

    rows: list[dict] = []
    for strategy_id in RUNNABLE_PROXY_STRATEGIES:
        p25_rows = phase25[phase25["model_id"].eq(strategy_id)]
        p26_rows = phase26[phase26["parent_strategy_id"].eq(strategy_id)]
        rows.append(
            {
                "strategy_id": strategy_id,
                "evidence_scope": "runnable_proxy_event_replay_salvage_feature_edge",
                "phase25_profile_rows": int(len(p25_rows)),
                "phase25_trades": int(p25_rows["trades"].sum()) if len(p25_rows) else 0,
                "phase25_best_mean_net_return": _best_value(phase25, phase25["model_id"].eq(strategy_id), "mean_net_return"),
                "phase25_positive_after_cost_rows": int((p25_rows["mean_net_return"] > 0).sum()) if len(p25_rows) else 0,
                "phase25_acceptance_ready_rows": int(p25_rows["acceptance_ready"].astype(bool).sum()) if len(p25_rows) else 0,
                "phase26_variant_profile_rows": int(len(p26_rows)),
                "phase26_realistic_positive_rows": int((p26_rows["realistic_charged_profile"].astype(bool) & p26_rows["positive_after_costs"].astype(bool)).sum()) if len(p26_rows) else 0,
                "phase26_zero_latency_positive_control_rows": int(p26_rows["zero_latency_positive_control"].astype(bool).sum()) if len(p26_rows) else 0,
                "phase26_salvage_candidate_rows": int(p26_rows["salvage_candidate_proxy"].astype(bool).sum()) if len(p26_rows) else 0,
                "phase27_candidate_profile_rows": int(_metric(phase27_overall, "phase27_candidate_profile_rows")),
                "phase27_realistic_cost_clearing_rows": int(_metric(phase27_overall, "phase27_realistic_cost_clearing_rows")),
                "phase28_proxy_rows": 0,
                "phase29_profile_rows": 0,
                "phase29_trades": 0,
                "phase29_realistic_positive_rows": 0,
                "phase29_proxy_candidate_rows": 0,
                "acceptance_ready_rows": 0,
                "evidence_note": "Phase25 direct event replay found no positive strategy/profile rows; Phase26 found no realistic salvage rows; Phase27 found no feature family clearing costs.",
            }
        )

    for strategy_id in PARTIAL_PROXY_STRATEGIES:
        p28_rows = phase28_support[phase28_support["strategy_id"].eq(strategy_id)]
        p29_rows = phase29[phase29["model_id"].eq(strategy_id)]
        p29_candidate_rows = phase29_candidates[phase29_candidates["model_id"].eq(strategy_id)]
        rows.append(
            {
                "strategy_id": strategy_id,
                "evidence_scope": "partial_proxy_label_replay",
                "phase25_profile_rows": 0,
                "phase25_trades": 0,
                "phase25_best_mean_net_return": None,
                "phase25_positive_after_cost_rows": 0,
                "phase25_acceptance_ready_rows": 0,
                "phase26_variant_profile_rows": 0,
                "phase26_realistic_positive_rows": 0,
                "phase26_zero_latency_positive_control_rows": 0,
                "phase26_salvage_candidate_rows": 0,
                "phase27_candidate_profile_rows": 0,
                "phase27_realistic_cost_clearing_rows": 0,
                "phase28_proxy_rows": int(p28_rows["proxy_rows"].iloc[0]) if len(p28_rows) else 0,
                "phase29_profile_rows": int(len(p29_rows)),
                "phase29_trades": int(p29_rows["trades"].sum()) if len(p29_rows) else 0,
                "phase29_realistic_positive_rows": int((p29_candidate_rows["realistic_charged_profile"].astype(bool) & p29_candidate_rows["positive_after_costs"].astype(bool)).sum()) if len(p29_candidate_rows) else 0,
                "phase29_proxy_candidate_rows": int(p29_candidate_rows["partial_proxy_candidate"].astype(bool).sum()) if len(p29_candidate_rows) else 0,
                "acceptance_ready_rows": int(p29_rows["acceptance_ready"].astype(bool).sum()) if len(p29_rows) else 0,
                "evidence_note": "Phase28 engineered weak proxy labels; Phase29 replay found no positive rows after costs and no proxy candidates, so labels are diagnostic only.",
            }
        )

    for strategy_id in NON_ALPHA_CONTROLS:
        rows.append(
            {
                "strategy_id": strategy_id,
                "evidence_scope": "non_alpha_control_or_risk_filter",
                "phase25_profile_rows": 0,
                "phase25_trades": 0,
                "phase25_best_mean_net_return": None,
                "phase25_positive_after_cost_rows": 0,
                "phase25_acceptance_ready_rows": 0,
                "phase26_variant_profile_rows": 0,
                "phase26_realistic_positive_rows": 0,
                "phase26_zero_latency_positive_control_rows": 0,
                "phase26_salvage_candidate_rows": 0,
                "phase27_candidate_profile_rows": 0,
                "phase27_realistic_cost_clearing_rows": 0,
                "phase28_proxy_rows": 0,
                "phase29_profile_rows": 0,
                "phase29_trades": 0,
                "phase29_realistic_positive_rows": 0,
                "phase29_proxy_candidate_rows": 0,
                "acceptance_ready_rows": 0,
                "evidence_note": "Classified as research/risk plumbing, not an alpha candidate for promotion.",
            }
        )

    evidence = pd.DataFrame(rows)
    evidence["total_execution_profile_rows"] = (
        evidence["phase25_profile_rows"] + evidence["phase26_variant_profile_rows"] + evidence["phase27_candidate_profile_rows"] + evidence["phase29_profile_rows"]
    )
    evidence["total_replay_trades_directly_attributed"] = evidence["phase25_trades"] + evidence["phase29_trades"]
    evidence["realistic_positive_execution_rows"] = (
        evidence["phase26_realistic_positive_rows"] + evidence["phase27_realistic_cost_clearing_rows"] + evidence["phase29_realistic_positive_rows"]
    )
    evidence["candidate_rows"] = evidence["phase26_salvage_candidate_rows"] + evidence["phase29_proxy_candidate_rows"]
    evidence["source_totals_note"] = (
        f"Workspace-level execution totals: Phase25={int(_metric(phase25_overall, 'phase25_total_trades'))}, "
        f"Phase26={int(_metric(phase26_overall, 'phase26_total_replay_trades'))}, "
        f"Phase27={int(_metric(phase27_overall, 'phase27_total_replay_trades'))}, "
        f"Phase28_proxy_labels={int(_metric(phase28_overall, 'phase28_total_proxy_label_rows'))}, "
        f"Phase29={int(_metric(phase29_overall, 'phase29_total_replay_trades'))}."
    )
    _ = phase27_family
    return evidence.sort_values("strategy_id").reset_index(drop=True)


def build_decision_ledger(m02: pd.DataFrame, evidence: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict] = []
    evidence_by_id = {row["strategy_id"]: row for row in evidence.to_dict("records")}
    for strategy_id in ALPHA_STRATEGIES + NON_ALPHA_CONTROLS:
        ev = evidence_by_id[strategy_id]
        if strategy_id in RUNNABLE_PROXY_STRATEGIES:
            decision = "reject_current_signal_form_redesign_required"
            action = "Do not spend more compute promoting the current proxy signal. Redesign only if a new event-level hypothesis can clear spread, Zerodha charges, and latency."
            blocker = "No realistic positive rows in Phase25/26/27 execution evidence."
        elif strategy_id in PARTIAL_PROXY_STRATEGIES:
            decision = "reject_current_proxy_label_execution_form"
            action = "Keep only as a research hypothesis until multi-day Class B labels and broker/exchange reconciliation exist; redesign label logic before more promotion work."
            blocker = "Weak proxy labels plus Phase29 no positive/candidate rows after costs."
        else:
            decision = "non_alpha_control_do_not_promote"
            action = "Keep as execution/risk plumbing or risk filter only; exclude from alpha promotion queue."
            blocker = "Not an alpha strategy under current product evidence."
        rows.append(
            {
                "strategy_id": strategy_id,
                "strategy_name": _strategy_name(strategy_id, m02),
                "evidence_scope": ev["evidence_scope"],
                "current_decision": decision,
                "promotion_ready": False,
                "acceptance_ready": False,
                "realistic_positive_execution_rows": int(ev["realistic_positive_execution_rows"]),
                "candidate_rows": int(ev["candidate_rows"]),
                "acceptance_ready_rows": int(ev["acceptance_ready_rows"]),
                "blocking_reason": blocker,
                "next_action": action,
            }
        )
    return pd.DataFrame(rows)


def build_redesign_queue(decisions: pd.DataFrame, evidence: pd.DataFrame) -> pd.DataFrame:
    merged = decisions.merge(evidence[["strategy_id", "phase26_zero_latency_positive_control_rows", "phase28_proxy_rows", "phase29_trades"]], on="strategy_id", how="left")
    rows: list[dict] = []
    for record in merged.to_dict("records"):
        decision = record["current_decision"]
        if decision == "non_alpha_control_do_not_promote":
            priority = "exclude"
            redesign_theme = "Do not redesign as alpha in this lane."
            required_evidence = "None for alpha promotion; maintain only if execution/risk plumbing remains useful."
        elif int(record.get("phase26_zero_latency_positive_control_rows") or 0) > 0:
            priority = "medium"
            redesign_theme = "Cost-aware trigger redesign around the tiny zero-latency edge; explicitly test whether edge survives spread, latency, and Zerodha charges."
            required_evidence = "New event-level feature definition, charged retail/stressed replay, and multi-day real tick validation."
        elif int(record.get("phase28_proxy_rows") or 0) > 0:
            priority = "medium"
            redesign_theme = "Replace weak market-by-price proxy labels with acceptance-grade event labels before more replay expansion."
            required_evidence = "Multi-day Class B labels, timestamp-skew/common-shock controls, and broker/exchange fill-cost reconciliation."
        else:
            priority = "low"
            redesign_theme = "Do not iterate current signal without a materially new hypothesis."
            required_evidence = "A new signal thesis that forecasts beyond spread and fee hurdle before full execution replay."
        rows.append(
            {
                "strategy_id": record["strategy_id"],
                "strategy_name": record["strategy_name"],
                "redesign_priority": priority,
                "redesign_theme": redesign_theme,
                "required_evidence_before_next_execution_expansion": required_evidence,
            }
        )
    return pd.DataFrame(rows).sort_values(["redesign_priority", "strategy_id"], kind="mergesort").reset_index(drop=True)


def build_overall_summary(decisions: pd.DataFrame, evidence: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"metric": "phase30_strategy_families_triaged", "value": int(len(decisions)), "description": "Strategy/control families given an execution-evidence decision"},
            {"metric": "phase30_alpha_families_triaged", "value": int(decisions["strategy_id"].isin(ALPHA_STRATEGIES).sum()), "description": "Alpha strategy families triaged"},
            {"metric": "phase30_reject_or_redesign_rows", "value": int(decisions["current_decision"].astype(str).str.startswith("reject_").sum()), "description": "Rows rejected in current form or redesign-only"},
            {"metric": "phase30_non_alpha_control_rows", "value": int(decisions["current_decision"].eq("non_alpha_control_do_not_promote").sum()), "description": "Rows classified as non-alpha/risk-only controls"},
            {"metric": "phase30_promotion_ready_rows", "value": int(decisions["promotion_ready"].astype(bool).sum()), "description": "Rows ready for promotion"},
            {"metric": "phase30_acceptance_ready_rows", "value": int(decisions["acceptance_ready"].astype(bool).sum()), "description": "Rows with acceptance-ready evidence"},
            {"metric": "phase30_realistic_positive_execution_rows", "value": int(evidence["realistic_positive_execution_rows"].sum()), "description": "Realistic charged execution rows across triaged families"},
            {"metric": "phase30_candidate_rows", "value": int(evidence["candidate_rows"].sum()), "description": "Salvage/proxy candidate rows across triaged families"},
            {"metric": "phase30_proxy_label_only_families", "value": int((evidence["phase28_proxy_rows"] > 0).sum()), "description": "Families supported only by weak proxy labels"},
        ]
    )


def write_report(output_dir: Path, overall: pd.DataFrame, decisions: pd.DataFrame, evidence: pd.DataFrame, redesign: pd.DataFrame) -> None:
    lines = [
        "# Phase 30 Strategy Decision Triage",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This milestone answers the execution question directly: after Phase 25-29 replays, no current strategy family has realistic positive execution evidence or acceptance-ready status.",
        "The outcome is therefore not promotion; it is rejection of current signal forms, redesign gating, or non-alpha classification.",
        "",
        "## Overall Summary",
        "",
        _markdown_table(overall),
        "",
        "## Decision Ledger",
        "",
        _markdown_table(decisions),
        "",
        "## Execution Evidence Summary",
        "",
        _markdown_table(evidence),
        "",
        "## Redesign Queue",
        "",
        _markdown_table(redesign),
        "",
    ]
    (output_dir / "phase30_strategy_decision_triage_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase30(paths: dict[str, Path], output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    m02 = _read_csv(paths["phase20_m02"])
    evidence = build_execution_evidence(paths)
    decisions = build_decision_ledger(m02, evidence)
    redesign = build_redesign_queue(decisions, evidence)
    overall = build_overall_summary(decisions, evidence)

    decisions.to_csv(output_dir / "strategy_family_decision_ledger.csv", index=False)
    evidence.to_csv(output_dir / "strategy_family_execution_evidence_summary.csv", index=False)
    redesign.to_csv(output_dir / "strategy_redesign_queue.csv", index=False)
    overall.to_csv(output_dir / "strategy_rejection_or_redesign_overall_summary.csv", index=False)
    write_report(output_dir, overall, decisions, evidence, redesign)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "strategy_families_triaged": int(len(decisions)),
        "alpha_families_triaged": int(decisions["strategy_id"].isin(ALPHA_STRATEGIES).sum()),
        "promotion_ready_rows": int(decisions["promotion_ready"].astype(bool).sum()),
        "acceptance_ready_rows": int(decisions["acceptance_ready"].astype(bool).sum()),
        "scope": "phase30_execution_evidence_decision_triage_not_strategy_acceptance",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase30",
            generated_utc=generated_utc,
            inputs={name: str(path) for name, path in paths.items()},
            parameters={
                "alpha_strategies": ALPHA_STRATEGIES,
                "runnable_proxy_strategies": RUNNABLE_PROXY_STRATEGIES,
                "partial_proxy_strategies": PARTIAL_PROXY_STRATEGIES,
                "non_alpha_controls": NON_ALPHA_CONTROLS,
                "decision_policy": "reject_current_form_when_no_realistic_positive_or_acceptance_ready_rows_after_phase25_29",
            },
            outputs={
                "decision_ledger": str(output_dir / "strategy_family_decision_ledger.csv"),
                "execution_evidence_summary": str(output_dir / "strategy_family_execution_evidence_summary.csv"),
                "redesign_queue": str(output_dir / "strategy_redesign_queue.csv"),
                "overall_summary": str(output_dir / "strategy_rejection_or_redesign_overall_summary.csv"),
                "report": str(output_dir / "phase30_strategy_decision_triage_report.md"),
                "manifest": str(output_dir / "phase30_strategy_decision_triage_manifest.json"),
            },
            random_seed="none_deterministic_execution_evidence_rollup",
            scenario_ids="phase25_phase26_phase27_phase28_phase29_current_workspace_evidence",
            cost_model_version="zerodha_equity_intraday_nse_order_formula_v2_2026_07_14",
            latency_model_version="phase12_execution_profiles_event_latency_counts",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase30_strategy_decision_triage_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 30 execution-evidence strategy decision triage.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase30"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--phase20-m02", type=Path, default=Path("outputs/phase20_m02/strategy_support_decision_summary.csv"))
    parser.add_argument("--phase25-summary", type=Path, default=Path("outputs/phase25/event_replay_summary.csv"))
    parser.add_argument("--phase25-overall", type=Path, default=Path("outputs/phase25/event_replay_overall_summary.csv"))
    parser.add_argument("--phase26-candidates", type=Path, default=Path("outputs/phase26/strategy_salvage_candidate_summary.csv"))
    parser.add_argument("--phase26-overall", type=Path, default=Path("outputs/phase26/strategy_salvage_overall_summary.csv"))
    parser.add_argument("--phase27-family", type=Path, default=Path("outputs/phase27/feature_edge_family_summary.csv"))
    parser.add_argument("--phase27-overall", type=Path, default=Path("outputs/phase27/feature_edge_overall_summary.csv"))
    parser.add_argument("--phase28-support", type=Path, default=Path("outputs/phase28/strategy_support_upgrade_summary.csv"))
    parser.add_argument("--phase28-overall", type=Path, default=Path("outputs/phase28/richer_event_label_overall_summary.csv"))
    parser.add_argument("--phase29-summary", type=Path, default=Path("outputs/phase29/partial_strategy_proxy_summary.csv"))
    parser.add_argument("--phase29-candidates", type=Path, default=Path("outputs/phase29/partial_strategy_proxy_candidate_summary.csv"))
    parser.add_argument("--phase29-overall", type=Path, default=Path("outputs/phase29/partial_strategy_proxy_overall_summary.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "phase20_m02": args.phase20_m02,
        "phase25_summary": args.phase25_summary,
        "phase25_overall": args.phase25_overall,
        "phase26_candidates": args.phase26_candidates,
        "phase26_overall": args.phase26_overall,
        "phase27_family": args.phase27_family,
        "phase27_overall": args.phase27_overall,
        "phase28_support": args.phase28_support,
        "phase28_overall": args.phase28_overall,
        "phase29_summary": args.phase29_summary,
        "phase29_candidates": args.phase29_candidates,
        "phase29_overall": args.phase29_overall,
    }
    run_phase30(paths, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
