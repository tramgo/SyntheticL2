from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE356_DIR = Path("outputs/phase356")
DEFAULT_OUTPUT_DIR = Path("outputs/phase357")
ROBUST_EVENT_FLOOR = 30
ANNUALIZED_THRESHOLD_PCT = 12.0


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def write_outputs(phase356_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    scenarios = read_csv(phase356_dir / "phase356_scenario_summary.csv")
    summary356 = read_csv(phase356_dir / "phase356_acceptance_summary.csv")
    if scenarios.empty or summary356.empty:
        raise FileNotFoundError(f"Phase356 evidence incomplete under {phase356_dir}")

    full_depth_rows = scenarios.loc[scenarios["control_id"].astype(str).isin(["depth_2_5_fade_variant", "depth_2_5_guard"])].copy()
    best_full_depth = full_depth_rows.sort_values("annualized_return_pct", ascending=False).iloc[0]
    frozen_top5 = scenarios.loc[scenarios["control_id"].astype(str).eq("frozen_clue")].iloc[0]

    family_contract = pd.DataFrame(
        [
            ("family_id", "P357_FULL_DEPTH_MARKET_NEUTRAL_FADE", "Frozen family identifier"),
            ("source_phase", "Phase356", "Derived from Phase356 controls that dominated the Phase355 frozen top-five clue"),
            ("primary_proxy", "NIFTYBEES", "No proxy tuning before validation"),
            ("primary_lookback_seconds", 900, "No lookback tuning before validation"),
            ("market_context", "abs(NIFTYBEES 900s pre-entry return) <= 1.0 bps", "Market-neutral context"),
            ("primary_side_rule", "fade depth-levels-2-5 imbalance", "Full-depth primary side rule"),
            ("guard_rule", "top-five fade allowed only with non-contradictory depth-levels-2-5 context", "Full-depth guard rule"),
            ("scope", "capacity-selected official-catalyst real L2 events", "Same event scope as Phase354/356 clue"),
            ("cost_profile", "zerodha_2x_all_in_cost_proxy", "Pinned cost stress"),
            ("initial_capital_inr", 250000, "Fixed-capital annualization denominator"),
            ("current_best_scenario", best_full_depth["scenario_id"], "Best full-depth Phase356 row"),
            ("current_best_trade_rows", best_full_depth["trade_rows"], "Current sparse count"),
            ("current_best_annualized_pct", best_full_depth["annualized_return_pct"], "Current diagnostic annualized return"),
            ("current_best_net_pnl_inr", best_full_depth["net_pnl_inr"], "Current diagnostic net PnL"),
            ("top5_reference_annualized_pct", frozen_top5["annualized_return_pct"], "Reference top-five frozen clue"),
        ],
        columns=["field", "frozen_value", "description"],
    )

    validation_contract = pd.DataFrame(
        [
            ("P357_NO_POST_HOC_TUNING", "No change to proxy, lookback, market-neutral threshold, event scope, costs, or capital denominator.", 1),
            ("P357_FULL_DEPTH_PRIMARY", "Depth-levels-2-5 fade/guard is primary; top-five-only clue is reference, not primary.", 1),
            ("P357_EVENT_FLOOR", f"At least {ROBUST_EVENT_FLOOR} events/trades required before acceptance.", 1),
            ("P357_ABOVE12", f"Annualized return must remain > {ANNUALIZED_THRESHOLD_PCT}% at cost200 fixed capital.", 1),
            ("P357_BREADTH", "At least two positive symbols and two positive symbol/date cells.", 1),
            ("P357_CONTROLS", "Side flip, deterministic alternate side, proxy swap, lookback swap, top-five-only reference, and depth-guard ablation required.", 1),
            ("P357_UNSEEN_REAL_DATES_FIRST", "If current panel remains below event floor, restore Phase350 real-date expansion before acceptance.", 1),
            ("P357_NO_PROMOTION_PAPER_LIVE", "No strategy promotion, paper/live acceptance or deployable profitability claim.", 1),
        ],
        columns=["contract_id", "requirement", "hard_gate"],
    )

    control_catalog = pd.DataFrame(
        [
            ("side_flip", "Flip the full-depth fade side.", "must_be_negative_or_weaker"),
            ("deterministic_alternate_side", "Alternate long/short over the same selected events.", "must_be_negative_or_weaker"),
            ("proxy_swap_bankbees", "Use BANKBEES under same market-neutral logic.", "robustness_control"),
            ("lookback_swap_300s", "Use 300s NIFTYBEES lookback.", "robustness_control"),
            ("top5_only_reference", "Original Phase355 top-five fade clue.", "reference_not_primary"),
            ("depth_guard_ablation", "Remove or invert depth-levels-2-5 guard.", "must_not_improve_cleanly"),
        ],
        columns=["control_id", "description", "required_interpretation"],
    )

    boundary = pd.DataFrame(
        [
            ("current_family_is_sparse_clue", 1, "Best full-depth family row remains below event floor"),
            ("strategy_replay_allowed", 0, "No replay unlock"),
            ("strategy_promotion_allowed", 0, "No promotion"),
            ("paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ],
        columns=["boundary", "value", "description"],
    )

    summary = pd.DataFrame(
        [
            ("phase357_full_depth_market_neutral_fade_precommit_complete", 1, "Phase357 precommit completed"),
            ("phase357_phase356_complete", 1, "Phase356 evidence present"),
            ("phase357_best_full_depth_scenario", best_full_depth["scenario_id"], "Best full-depth scenario"),
            ("phase357_best_full_depth_trade_rows", best_full_depth["trade_rows"], "Best full-depth trade rows"),
            ("phase357_best_full_depth_annualized_pct", best_full_depth["annualized_return_pct"], "Best full-depth annualized return"),
            ("phase357_best_full_depth_net_pnl_inr", best_full_depth["net_pnl_inr"], "Best full-depth net PnL"),
            ("phase357_event_floor_required", ROBUST_EVENT_FLOOR, "Required event floor"),
            ("phase357_execution_allowed_next", 1, "Phase358 execution allowed"),
            ("phase357_strategy_promotion_allowed", 0, "No promotion"),
            ("phase357_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase357_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase357_next_best_action", "run_phase358_full_depth_market_neutral_fade_execution_no_paper_live_or_restore_phase350_real_dates", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )

    gates = pd.DataFrame(
        [
            ("P357_PHASE356_COMPLETE", 1, "Phase356 evidence present"),
            ("P357_FULL_DEPTH_DOMINANCE_RECOGNIZED", int(float(best_full_depth["annualized_return_pct"]) > float(frozen_top5["annualized_return_pct"])), "Depth variant beats top-five clue"),
            ("P357_SPARSE_RECOGNIZED", int(int(best_full_depth["trade_rows"]) < ROBUST_EVENT_FLOOR), f"trade_rows={best_full_depth['trade_rows']}"),
            ("P357_CONTRACT_PRESENT", int(len(validation_contract) >= 8), f"contract_rows={len(validation_contract)}"),
            ("P357_CONTROLS_PRESENT", int(len(control_catalog) >= 6), f"control_rows={len(control_catalog)}"),
            ("P357_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "closed"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )

    outputs = {
        "summary": output_dir / "phase357_acceptance_summary.csv",
        "family": output_dir / "phase357_family_contract.csv",
        "validation": output_dir / "phase357_validation_contract.csv",
        "controls": output_dir / "phase357_control_catalog.csv",
        "boundary": output_dir / "phase357_boundary_ledger.csv",
        "gates": output_dir / "phase357_gate_evaluation.csv",
        "report": output_dir / "phase357_full_depth_market_neutral_fade_precommit_report.md",
        "manifest": output_dir / "phase357_full_depth_market_neutral_fade_precommit_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    family_contract.to_csv(outputs["family"], index=False)
    validation_contract.to_csv(outputs["validation"], index=False)
    control_catalog.to_csv(outputs["controls"], index=False)
    boundary.to_csv(outputs["boundary"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    report = "\n".join(
        [
            "# Phase357 Full-Depth Market-Neutral Fade Precommit",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase357 freezes the Phase356 interpretation that depth-levels-2-5 variants outperformed the top-five-only frozen clue. It is a precommit only.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Family contract",
            "",
            _markdown_table(family_contract),
            "",
            "## Validation contract",
            "",
            _markdown_table(validation_contract),
            "",
            "## Control catalog",
            "",
            _markdown_table(control_catalog),
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
        "phase": 357,
        "generated_at_utc": generated_utc,
        "phase356_dir": str(phase356_dir),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase357_full_depth_market_neutral_fade_precommit",
            generated_utc=generated_utc,
            inputs={"phase356_dir": str(phase356_dir)},
            parameters={"robust_event_floor": ROBUST_EVENT_FLOOR, "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT},
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_precommit_only",
        ),
        "next_action": "run_phase358_full_depth_market_neutral_fade_execution_no_paper_live_or_restore_phase350_real_dates",
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase356-dir", type=Path, default=DEFAULT_PHASE356_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase356_dir, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
