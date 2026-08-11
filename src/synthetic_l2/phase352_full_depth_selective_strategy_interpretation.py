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


DEFAULT_PHASE351_DIR = Path("outputs/phase351")
DEFAULT_OUTPUT_DIR = Path("outputs/phase352")
DEFAULT_PLAN_PATH = Path("Plan/zerodha_l2_synthetic_data_strategy_validation_plan.md")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def write_outputs(phase351_dir: Path, output_dir: Path, plan_path: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()

    acceptance351 = read_csv(phase351_dir / "phase351_acceptance_summary.csv")
    scenarios = read_csv(phase351_dir / "phase351_scenario_summary.csv")
    event_ledger = read_csv(phase351_dir / "phase351_event_ledger.csv")
    gates351 = read_csv(phase351_dir / "phase351_gate_evaluation.csv")

    if acceptance351.empty or scenarios.empty or event_ledger.empty:
        raise FileNotFoundError(f"Phase351 evidence incomplete under {phase351_dir}")

    scenario_rows = len(scenarios)
    event_rows = len(event_ledger)
    above12_rows = as_int(metric_value(acceptance351, "phase351_above12_rows", 0))
    acceptance_candidate_rows = as_int(metric_value(acceptance351, "phase351_acceptance_candidate_rows", 0))
    positive_event_rows = int((event_ledger["expected_net_pnl_inr"].astype(float) > 0).sum())
    positive_strategy_rows = int((scenarios["expected_net_pnl_inr"].astype(float) > 0).sum())
    best = scenarios.sort_values("annualized_pct_fixed_capital", ascending=False).iloc[0]
    worst = scenarios.sort_values("annualized_pct_fixed_capital", ascending=True).iloc[0]
    hard_gate_pass_rows = int(gates351["passed"].astype(int).sum()) if not gates351.empty and "passed" in gates351.columns else 0
    hard_gate_rows = len(gates351)

    decision_rows = [
        {
            "decision_id": "phase351_evidence_complete",
            "decision_value": 1,
            "evidence": f"scenario_rows={scenario_rows}; event_rows={event_rows}; gates={hard_gate_pass_rows}/{hard_gate_rows}",
            "interpretation": "Phase351 can be interpreted.",
        },
        {
            "decision_id": "hidden_positive_pockets_exist",
            "decision_value": int(positive_event_rows > 0 or positive_strategy_rows > 0),
            "evidence": f"positive_event_rows={positive_event_rows}; positive_strategy_rows={positive_strategy_rows}",
            "interpretation": "No positive symbol/date or scenario pocket was found in Phase351.",
        },
        {
            "decision_id": "phase351_expand_same_branch",
            "decision_value": 0,
            "evidence": f"above12={above12_rows}; acceptance_candidates={acceptance_candidate_rows}; positive_event_rows={positive_event_rows}",
            "interpretation": "Do not widen the same bounded synthetic branch without a material new thesis.",
        },
        {
            "decision_id": "phase351_branch_closed_for_acceptance",
            "decision_value": 1,
            "evidence": f"best_ann={as_float(best['annualized_pct_fixed_capital'])}; best_net={as_float(best['expected_net_pnl_inr'])}",
            "interpretation": "Close Phase351 as a negative synthetic full-depth selective-search result.",
        },
        {
            "decision_id": "real_date_expansion_route_remains_open_if_access_restored",
            "decision_value": 1,
            "evidence": "Phase348/350 failed only to add a new unseen real L2 date; Phase342/343 real holdout remains completed and negative.",
            "interpretation": "If fresh SAS/local drop exists, rerun Phase350; otherwise precommit a materially new thesis.",
        },
    ]
    decision = pd.DataFrame(decision_rows)

    top = scenarios.sort_values("annualized_pct_fixed_capital", ascending=False).head(20).copy()
    top["diagnostic_clue_only"] = 1
    top["expand_same_branch_allowed"] = 0
    top["acceptance_allowed"] = 0

    failure_rows = [
        {
            "failure_or_limit": "no_positive_event_rows",
            "observed": positive_event_rows,
            "interpretation": "The branch has no hidden profitable symbol/date pocket in the bounded evidence.",
        },
        {
            "failure_or_limit": "no_above12_scenarios",
            "observed": above12_rows,
            "interpretation": "No scenario reached the user's >12% annualized diagnostic threshold.",
        },
        {
            "failure_or_limit": "no_acceptance_candidates",
            "observed": acceptance_candidate_rows,
            "interpretation": "No scenario passed event floor, breadth and profitability criteria.",
        },
        {
            "failure_or_limit": "passive_reduces_loss_but_does_not_rescue",
            "observed": str(best["execution_profile"]),
            "interpretation": "The best result is a passive-aware profile, but it remains negative.",
        },
    ]
    failure = pd.DataFrame(failure_rows)

    summary_rows = [
        ("phase352_full_depth_selective_interpretation_complete", 1, "Phase352 interpretation completed"),
        ("phase352_phase351_complete", 1, "Phase351 evidence present"),
        ("phase352_phase351_scenario_rows", scenario_rows, "Phase351 scenario rows interpreted"),
        ("phase352_phase351_event_rows", event_rows, "Phase351 event rows interpreted"),
        ("phase352_phase351_positive_event_rows", positive_event_rows, "Positive daily/symbol event rows"),
        ("phase352_phase351_above12_rows", above12_rows, "Above-12 fixed-capital annualized rows"),
        ("phase352_phase351_acceptance_candidate_rows", acceptance_candidate_rows, "Acceptance candidate rows"),
        ("phase352_best_strategy_id", str(best["strategy_id"]), "Best Phase351 strategy"),
        ("phase352_best_execution_profile", str(best["execution_profile"]), "Best Phase351 execution profile"),
        ("phase352_best_annualized_pct", as_float(best["annualized_pct_fixed_capital"]), "Best fixed-capital annualized return"),
        ("phase352_best_expected_net_pnl_inr", as_float(best["expected_net_pnl_inr"]), "Best expected net PnL"),
        ("phase352_worst_annualized_pct", as_float(worst["annualized_pct_fixed_capital"]), "Worst fixed-capital annualized return"),
        ("phase352_close_phase351_for_acceptance", 1, "Close Phase351 branch for acceptance"),
        ("phase352_expand_same_branch_allowed", 0, "No same-branch expansion without material new thesis"),
        ("phase352_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned cost model"),
        ("phase352_strategy_promotion_allowed", 0, "No promotion"),
        ("phase352_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase352_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        (
            "phase352_next_best_action",
            "restore_phase350_real_date_expansion_or_precommit_material_new_thesis_no_paper_live",
            "Recommended next milestone",
        ),
    ]
    summary = pd.DataFrame(summary_rows, columns=["metric", "value", "description"])

    gate_rows = [
        ("P352_PHASE351_COMPLETE", 1, "Phase351 evidence files present"),
        ("P352_HIDDEN_POCKET_AUDITED", 1, f"positive_event_rows={positive_event_rows}"),
        ("P352_ZERO_ACCEPTANCE_RECOGNIZED", int(acceptance_candidate_rows == 0), f"acceptance_candidates={acceptance_candidate_rows}"),
        ("P352_CLOSE_OR_ROUTE_DECIDED", 1, "Close same branch; route to real-date expansion or material-new thesis"),
        ("P352_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "closed"),
    ]
    gates = pd.DataFrame(gate_rows, columns=["gate_id", "passed", "evidence"])

    outputs = {
        "summary": output_dir / "phase352_acceptance_summary.csv",
        "decision": output_dir / "phase352_decision_ledger.csv",
        "failure": output_dir / "phase352_failure_ledger.csv",
        "top": output_dir / "phase352_top_scenario_interpretation.csv",
        "gates": output_dir / "phase352_gate_evaluation.csv",
        "report": output_dir / "phase352_full_depth_selective_strategy_interpretation_report.md",
        "manifest": output_dir / "phase352_full_depth_selective_strategy_interpretation_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    decision.to_csv(outputs["decision"], index=False)
    failure.to_csv(outputs["failure"], index=False)
    top.to_csv(outputs["top"], index=False)
    gates.to_csv(outputs["gates"], index=False)

    report = "\n".join(
        [
            "# Phase352 Full-Depth Selective Strategy Interpretation",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase352 interprets Phase351. The key result is that the bounded full-depth selective synthetic branch has no hidden positive symbol/date pockets and no scenario above the 12% fixed-capital diagnostic bar.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Decision ledger",
            "",
            _markdown_table(decision),
            "",
            "## Failure ledger",
            "",
            _markdown_table(failure),
            "",
            "## Top Phase351 scenarios",
            "",
            _markdown_table(top.head(10)),
            "",
            "## Gate evaluation",
            "",
            _markdown_table(gates),
            "",
            "No promotion, paper/live acceptance, or deployable profitability claim is opened.",
        ]
    )
    outputs["report"].write_text(report + "\n", encoding="utf-8")

    manifest = {
        "phase": 352,
        "generated_at_utc": generated_utc,
        "phase351_dir": str(phase351_dir),
        "plan_path": str(plan_path),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase352_full_depth_selective_strategy_interpretation",
            generated_utc=generated_utc,
            inputs={"phase351_dir": str(phase351_dir), "plan_path": str(plan_path)},
            parameters={"positive_event_rows": positive_event_rows, "acceptance_candidate_rows": acceptance_candidate_rows},
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_interpretation_only",
        ),
        "next_action": str(summary.loc[summary["metric"].eq("phase352_next_best_action"), "value"].iloc[0]),
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase351-dir", type=Path, default=DEFAULT_PHASE351_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--plan-path", type=Path, default=DEFAULT_PLAN_PATH)
    args = parser.parse_args()
    outputs = write_outputs(args.phase351_dir, args.output_dir, args.plan_path)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
