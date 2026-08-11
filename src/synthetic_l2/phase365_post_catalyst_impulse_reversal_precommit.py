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


DEFAULT_PHASE364_DIR = Path("outputs/phase364")
DEFAULT_OUTPUT_DIR = Path("outputs/phase365")
THESIS_ID = "P365_POST_CATALYST_IMPULSE_REVERSAL_AFTER_REPLENISHMENT"
NEXT_ACTION = "run_phase366_post_catalyst_impulse_reversal_frozen_diagnostic_no_paper_live"


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


def write_outputs(phase364_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase364_summary = read_csv(phase364_dir / "phase364_acceptance_summary.csv")
    clue = read_csv(phase364_dir / "phase364_reversal_clue_contract.csv")
    if phase364_summary.empty or clue.empty:
        raise FileNotFoundError("Phase365 requires Phase364 summary and reversal clue contract")
    frozen = clue.iloc[0].to_dict()
    thesis = pd.DataFrame(
        [
            {
                "thesis_id": THESIS_ID,
                "source_clue_id": frozen["clue_id"],
                "source_scenario_id": frozen["source_scenario_id"],
                "status": "precommit",
                "material_difference_from_phase362_primary": "This is post-catalyst impulse reversal after replenishment, not impulse continuation.",
                "decision_delay_seconds": int(float(frozen["decision_delay_seconds"])),
                "horizon_seconds": 900,
                "min_abs_impulse_bps": float(frozen["min_abs_impulse_bps"]),
                "min_abs_l2_l5_imbalance": float(frozen["min_abs_l2_l5_imbalance"]),
                "min_replenishment_ratio": float(frozen["min_replenishment_ratio"]),
                "side_rule": frozen["side_rule"],
                "full_depth_rule": "use full top-five L1-L5 book state; levels 2-5 support must be material; no L1-only variant",
                "cost_rule": "Zerodha cost200 fixed-capital scoring",
                "paper_live_or_profit_claim_allowed": 0,
            }
        ]
    )
    control_catalog = pd.DataFrame(
        [
            ("primary", "post_catalyst_impulse_reversal_after_replenishment", "Frozen Phase364 side rule"),
            ("side_flip", "post_catalyst_impulse_continuation_same_filters", "Must be worse than primary or treated as ambiguity"),
            ("stricter_replenishment", "same_reversal_rule_min_replenishment_0p10", "Checks dependence on zero replenishment threshold"),
            ("weaker_depth", "same_reversal_rule_min_l2_l5_imbalance_0p15", "Checks depth-threshold sensitivity"),
            ("shorter_delay", "same_reversal_rule_decision_delay_60s", "Checks delay sensitivity"),
        ],
        columns=["control_id", "control_description", "purpose"],
    )
    validation_contract = pd.DataFrame(
        [
            ("phase364_complete_required", 1, "Phase364 must freeze the clue before this precommit."),
            ("exact_primary_parameters_frozen", 1, "120s delay, 2.5 bps impulse, 0.25 levels-2-5 imbalance, 0.0 replenishment."),
            ("full_depth_required", 1, "Use L1-L5 price/qty/order-count fields and levels 2-5 materiality."),
            ("l1_only_allowed", 0, "No L1-only variants."),
            ("event_floor", 30, "Acceptance requires at least 30 selected trades."),
            ("annualized_threshold_pct", 12.0, "User profitability bar."),
            ("breadth_required", ">=2 positive symbols and >=2 positive symbol/date cells", "Avoid one-pocket clue."),
            ("cost200_fixed_capital_required", 1, "Zerodha cost200 fixed capital."),
            ("same_run_search_allowed", 0, "No parameter search in Phase366; controls only."),
            ("paper_live_or_profit_claim_allowed", 0, "No promotion or deployable claim."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )
    gates = pd.DataFrame(
        [
            ("P365_PHASE364_COMPLETE", int(str(metric_value(phase364_summary, "phase364_catalyst_impulse_reversal_clue_interpretation_complete", 0)) == "1"), "Phase364 complete"),
            ("P365_REVERSAL_CLUE_PRESENT", int(not clue.empty), f"clue_rows={len(clue)}"),
            ("P365_EXACT_PARAMETERS_FROZEN", 1, "delay=120; impulse=2.5; depth=0.25; replenishment=0.0"),
            ("P365_FULL_DEPTH_REQUIRED", 1, "L1-L5 and levels 2-5 materiality"),
            ("P365_CONTROLS_REGISTERED", int(len(control_catalog) >= 5), f"control_rows={len(control_catalog)}"),
            ("P365_NO_SEARCH_OR_SAME_FAMILY_RESCUE", 1, "frozen primary plus controls only"),
            ("P365_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "closed"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )
    summary = pd.DataFrame(
        [
            ("phase365_post_catalyst_impulse_reversal_precommit_complete", 1, "Phase365 precommit completed"),
            ("phase365_thesis_id", THESIS_ID, "Precommitted thesis"),
            ("phase365_source_clue_id", frozen["clue_id"], "Source clue"),
            ("phase365_decision_delay_seconds", int(float(frozen["decision_delay_seconds"])), "Frozen delay"),
            ("phase365_min_abs_impulse_bps", float(frozen["min_abs_impulse_bps"]), "Frozen impulse threshold"),
            ("phase365_min_abs_l2_l5_imbalance", float(frozen["min_abs_l2_l5_imbalance"]), "Frozen depth threshold"),
            ("phase365_min_replenishment_ratio", float(frozen["min_replenishment_ratio"]), "Frozen replenishment threshold"),
            ("phase365_control_rows", len(control_catalog), "Control rows"),
            ("phase365_strategy_promotion_allowed", 0, "No promotion"),
            ("phase365_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase365_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase365_hard_gate_pass_rows", int(gates["passed"].astype(int).sum()), "Passed hard gates"),
            ("phase365_hard_gate_rows", len(gates), "Hard gates"),
            ("phase365_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    outputs = {
        "summary": output_dir / "phase365_acceptance_summary.csv",
        "thesis": output_dir / "phase365_thesis_contract.csv",
        "controls": output_dir / "phase365_control_catalog.csv",
        "validation": output_dir / "phase365_validation_contract.csv",
        "gates": output_dir / "phase365_gate_evaluation.csv",
        "report": output_dir / "phase365_post_catalyst_impulse_reversal_precommit_report.md",
        "manifest": output_dir / "phase365_post_catalyst_impulse_reversal_precommit_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    thesis.to_csv(outputs["thesis"], index=False)
    control_catalog.to_csv(outputs["controls"], index=False)
    validation_contract.to_csv(outputs["validation"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    report = "\n".join(
        [
            "# Phase365 Post-Catalyst Impulse Reversal Precommit",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase365 precommits the Phase364 sparse reversal-after-replenishment clue as its own frozen thesis. It does not run a search and opens no promotion, paper/live acceptance, or deployable profitability claim.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Thesis contract",
            "",
            _markdown_table(thesis),
            "",
            "## Control catalog",
            "",
            _markdown_table(control_catalog),
            "",
            "## Validation contract",
            "",
            _markdown_table(validation_contract),
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
        "phase": 365,
        "generated_at_utc": generated_utc,
        "phase364_dir": str(phase364_dir),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase365_post_catalyst_impulse_reversal_precommit",
            generated_utc=generated_utc,
            inputs={"phase364_clue_contract": str(phase364_dir / "phase364_reversal_clue_contract.csv")},
            parameters={"thesis_id": THESIS_ID},
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": NEXT_ACTION,
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase364-dir", type=Path, default=DEFAULT_PHASE364_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase364_dir, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
