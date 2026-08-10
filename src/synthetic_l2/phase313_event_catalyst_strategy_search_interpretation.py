from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE312_DIR = Path("outputs/phase312")
DEFAULT_OUTPUT_DIR = Path("outputs/phase313")

NEXT_ACTION = "run_phase314_event_catalyst_multievent_synthetic_breadth_precommit_no_replay"
REPAIR_ACTION = "repair_phase313_event_catalyst_strategy_search_interpretation"


def summarize_family(variants: pd.DataFrame) -> pd.DataFrame:
    if variants.empty:
        return pd.DataFrame()
    grouped = variants.groupby("family_id", dropna=False).agg(
        scenario_rows=("scenario_id", "count"),
        positive_net_pnl_rows=("positive_net_pnl", "sum"),
        sparse_above12_rows=("annualized_above_12pct_sparse", "sum"),
        best_net_pnl_inr=("net_pnl_inr", "max"),
        median_net_pnl_inr=("net_pnl_inr", "median"),
        best_sparse_annualized_pct=("annualized_return_pct_sparse", "max"),
        median_sparse_annualized_pct=("annualized_return_pct_sparse", "median"),
        max_scheduled_trades=("scheduled_trade_rows", "max"),
    ).reset_index()
    grouped["positive_net_pnl_fraction"] = grouped["positive_net_pnl_rows"] / grouped["scenario_rows"]
    grouped["sparse_above12_fraction"] = grouped["sparse_above12_rows"] / grouped["scenario_rows"]
    return grouped.sort_values(["sparse_above12_rows", "best_sparse_annualized_pct"], ascending=[False, False])


def summarize_cost_stress(variants: pd.DataFrame) -> pd.DataFrame:
    if variants.empty:
        return pd.DataFrame()
    grouped = variants.groupby("cost_profile", dropna=False).agg(
        scenario_rows=("scenario_id", "count"),
        positive_net_pnl_rows=("positive_net_pnl", "sum"),
        sparse_above12_rows=("annualized_above_12pct_sparse", "sum"),
        best_net_pnl_inr=("net_pnl_inr", "max"),
        best_sparse_annualized_pct=("annualized_return_pct_sparse", "max"),
    ).reset_index()
    grouped["positive_net_pnl_fraction"] = grouped["positive_net_pnl_rows"] / grouped["scenario_rows"]
    return grouped.sort_values("cost_profile")


def build_interpretation(acceptance: pd.DataFrame, variants: pd.DataFrame, family: pd.DataFrame, cost: pd.DataFrame) -> pd.DataFrame:
    best_id = str(metric_value(acceptance, "phase312_best_scenario_id", ""))
    observed_dates = as_int(metric_value(acceptance, "phase312_observed_trade_dates", 0))
    best_trades = as_int(metric_value(acceptance, "phase312_best_scheduled_trade_rows", 0))
    sparse_rows = as_int(metric_value(acceptance, "phase312_sparse_above12_annualized_rows", 0))
    best_family = str(variants.sort_values("annualized_return_pct_sparse", ascending=False)["family_id"].iloc[0]) if not variants.empty else ""
    cost200_rows = int(variants[variants["cost_profile"].astype(str).eq("zerodha_2x_all_in_cost_proxy")]["annualized_above_12pct_sparse"].sum()) if not variants.empty else 0
    rows = [
        ("phase312_positive_sparse_leads_exist", int(sparse_rows > 0), f"sparse_above12_rows={sparse_rows}", "Useful training clue exists."),
        ("best_cluster_family", best_family, best_id, "Best sparse annualized scenario family."),
        ("cost_stress_sparse_leads_exist", int(cost200_rows > 0), f"2x_cost_sparse_above12_rows={cost200_rows}", "Checks whether any clue survives 2x all-in-cost proxy."),
        ("insufficient_event_breadth_for_acceptance", int(observed_dates < 5), f"observed_trade_dates={observed_dates}", "One synthetic event date is not acceptance breadth."),
        ("insufficient_trade_breadth_for_acceptance", int(best_trades < 30), f"best_scheduled_trades={best_trades}", "Best scenario is too sparse for robust portfolio claim."),
        ("replay_or_promotion_allowed", 0, "closed", "No replay/promotion from Phase313."),
        ("deployable_profitability_claim_allowed", 0, "closed", "No deployable claim from one-event synthetic evidence."),
        ("selected_next_route", "P314_EVENT_CATALYST_MULTIEVENT_SYNTHETIC_BREADTH_PRECOMMIT", NEXT_ACTION, "Build more synthetic event breadth before broader search/replay."),
    ]
    return pd.DataFrame(rows, columns=["decision_id", "decision_value", "evidence", "interpretation"])


def build_gate_evaluation(phase312: pd.DataFrame, interpretation: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(phase312, "phase312_strategy_search_training_complete", 0))
    deployable_claim = as_int(metric_value(phase312, "phase312_deployable_profitability_claim_allowed", 1))
    selected = interpretation[interpretation["decision_id"].astype(str).eq("selected_next_route")]
    rows = [
        ("P313_PHASE312_COMPLETE", complete == 1, complete, 1),
        ("P313_INTERPRETATION_ROWS_PRESENT", len(interpretation) >= 8, len(interpretation), ">=8"),
        ("P313_PROFITABILITY_CLAIM_CLOSED", deployable_claim == 0, deployable_claim, 0),
        ("P313_NEXT_ROUTE_SELECTED", not selected.empty, selected["decision_value"].iloc[0] if not selected.empty else "", "selected"),
        ("P313_NO_REPLAY_PROMOTION_OR_PAPER_LIVE", True, "replay=0;promotion=0;paper=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in rows])


def build_acceptance(interpretation: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    lookup = interpretation.set_index("decision_id")["decision_value"].to_dict() if not interpretation.empty else {}
    return pd.DataFrame(
        [
            ("phase313_interpretation_complete", 1, "Phase313 event-catalyst strategy-search interpretation completed"),
            ("phase313_positive_sparse_leads_exist", lookup.get("phase312_positive_sparse_leads_exist", 0), "Sparse positive training leads exist"),
            ("phase313_cost_stress_sparse_leads_exist", lookup.get("cost_stress_sparse_leads_exist", 0), "2x-cost sparse training leads exist"),
            ("phase313_insufficient_event_breadth_for_acceptance", lookup.get("insufficient_event_breadth_for_acceptance", 1), "Event breadth insufficient for acceptance"),
            ("phase313_insufficient_trade_breadth_for_acceptance", lookup.get("insufficient_trade_breadth_for_acceptance", 1), "Trade breadth insufficient for acceptance"),
            ("phase313_replay_allowed", 0, "No replay"),
            ("phase313_strategy_promotion_allowed", 0, "No promotion"),
            ("phase313_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase313_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase313_selected_next_route", lookup.get("selected_next_route", ""), "Selected next route"),
            ("phase313_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase313_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase313_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase313 Event-Catalyst Strategy Search Interpretation",
        "",
        "Phase313 interprets Phase312 training-only results. It does not replay, promote, or claim deployable profitability.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase313_event_catalyst_strategy_search_interpretation_report.md").write_text("\n".join(lines), encoding="utf-8")


def run(phase312_dir: Path = DEFAULT_PHASE312_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase312 = read_csv(phase312_dir / "phase312_acceptance_summary.csv")
    variants = read_csv(phase312_dir / "phase312_strategy_variant_results.csv")
    family = summarize_family(variants)
    cost = summarize_cost_stress(variants)
    interpretation = build_interpretation(phase312, variants, family, cost)
    gates = build_gate_evaluation(phase312, interpretation)
    acceptance = build_acceptance(interpretation, gates)

    family.to_csv(output_dir / "phase313_family_interpretation_summary.csv", index=False)
    cost.to_csv(output_dir / "phase313_cost_stress_interpretation_summary.csv", index=False)
    interpretation.to_csv(output_dir / "phase313_interpretation_decision_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase313_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase313_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        acceptance,
        {
            "Family interpretation": family,
            "Cost stress interpretation": cost,
            "Decision ledger": interpretation,
            "Gates": gates,
        },
    )

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase313_event_catalyst_strategy_search_interpretation",
        **reproducibility_fields(
            artifact_id="phase313",
            generated_utc=generated_utc,
            inputs={
                "phase312_acceptance": str(phase312_dir / "phase312_acceptance_summary.csv"),
                "phase312_variant_results": str(phase312_dir / "phase312_strategy_variant_results.csv"),
            },
            parameters={"policy": "interpret_training_leads_no_replay"},
            outputs={"acceptance_summary": str(output_dir / "phase313_acceptance_summary.csv")},
            cost_model_version="inherits_phase312",
            latency_model_version="not_applicable_interpretation_only",
        ),
    }
    (output_dir / "phase313_event_catalyst_strategy_search_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Interpret Phase312 event-catalyst strategy search.")
    parser.add_argument("--phase312-dir", type=Path, default=DEFAULT_PHASE312_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase312_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
