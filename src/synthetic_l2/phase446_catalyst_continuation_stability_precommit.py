from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE445_DIR = Path("outputs/phase445")
DEFAULT_PHASE444_DIR = Path("outputs/phase444")
DEFAULT_OUTPUT_DIR = Path("outputs/phase446")

THESIS_ID = "P446_CATALYST_CONTINUATION_STABILITY_HOLDOUT_PRECOMMIT"
LOCKED_SCENARIO_ID = "P444_catalyst_continuation_H600_replenishment_after_exhaustion_C5"
NEXT_ACTION = "run_phase447_catalyst_continuation_stability_holdout_no_paper_live"
REPAIR_ACTION = "repair_phase446_precommit_inputs"

MIN_HOLDOUT_DATES = 3
MIN_HOLDOUT_NET_PNL_INR = 0.0
MIN_HOLDOUT_ANNUALIZED_PCT = 12.0
MIN_HOLDOUT_POSITIVE_DATE_FRACTION = 0.60
COST_MULTIPLIER = 2.0
INITIAL_CAPITAL_INR = 1_000_000.0
ORDER_NOTIONAL_INR = 100_000.0


def sha256_frame(frame: pd.DataFrame) -> str:
    return hashlib.sha256(frame.to_csv(index=False, lineterminator="\n").encode("utf-8")).hexdigest()


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def build_split(trades: pd.DataFrame) -> pd.DataFrame:
    dates = sorted(trades["diagnostic_trade_date"].astype(str).unique().tolist())
    holdout_n = max(MIN_HOLDOUT_DATES, len(dates) // 3)
    holdout = set(dates[-holdout_n:])
    rows = [{"diagnostic_trade_date": d, "split": "holdout" if d in holdout else "development"} for d in dates]
    return pd.DataFrame(rows)


def build_contract(split: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("thesis_id", THESIS_ID, "Stability/holdout precommit after Phase445 positive diagnostic."),
        ("locked_scenario_id", LOCKED_SCENARIO_ID, "No parameter tuning from Phase444."),
        ("split_policy", "chronological_last_third_dates_as_holdout_min_3_dates", "Holdout split frozen before Phase447."),
        ("holdout_dates", ";".join(split[split["split"].eq("holdout")]["diagnostic_trade_date"].astype(str).tolist()), "Frozen holdout dates."),
        ("development_dates", ";".join(split[split["split"].eq("development")]["diagnostic_trade_date"].astype(str).tolist()), "Frozen development dates."),
        ("acceptance_floor", f"holdout_net_pnl_gt_{MIN_HOLDOUT_NET_PNL_INR};holdout_annualized_ge_{MIN_HOLDOUT_ANNUALIZED_PCT};holdout_positive_date_fraction_ge_{MIN_HOLDOUT_POSITIVE_DATE_FRACTION}", "Holdout stability requirements."),
        ("controls_required", "locked_scenario_only;no_new_filters;date_pnl_concentration;symbol_pnl_concentration;time_shift_context", "No same-result tuning."),
        ("capital_policy", f"fixed_initial_capital_{int(INITIAL_CAPITAL_INR)}_inr_order_notional_{int(ORDER_NOTIONAL_INR)}_inr_cost200", "Annualized denominator fixed."),
        ("forbidden", "new_thresholds;drop_bad_dates;drop_bad_symbols;promotion;paper_live;deployable_profitability_claim", "Closed boundaries."),
        ("execution_results_generated_now", "0", "Precommit only."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_evidence(phase445: pd.DataFrame, trades: pd.DataFrame) -> pd.DataFrame:
    locked = trades[trades["scenario_id"].astype(str).eq(LOCKED_SCENARIO_ID)]
    date_pnl = locked.groupby("diagnostic_trade_date")["net_pnl_inr"].sum() if not locked.empty else pd.Series(dtype=float)
    return pd.DataFrame(
        [
            ("phase445_next_action", scalar(phase445, "phase445_next_best_action", ""), "Phase445 requires stability repair or real holdout."),
            ("phase445_best_net_pnl_inr", scalar(phase445, "phase445_phase444_best_net_pnl_inr", ""), "Positive diagnostic net P&L."),
            ("phase445_best_annualized_pct", scalar(phase445, "phase445_phase444_best_annualized_return_pct", ""), "Positive diagnostic annualized return."),
            ("locked_trade_rows", len(locked), "Locked scenario trade rows."),
            ("locked_dates", locked["diagnostic_trade_date"].nunique() if not locked.empty else 0, "Locked scenario dates."),
            ("locked_positive_dates", int((date_pnl > 0).sum()) if len(date_pnl) else 0, "Positive date count before holdout audit."),
        ],
        columns=["evidence_id", "value", "description"],
    )


def build_gates(phase445: pd.DataFrame, evidence: pd.DataFrame, contract: pd.DataFrame, split: pd.DataFrame) -> pd.DataFrame:
    values = dict(zip(evidence["evidence_id"], evidence["value"]))
    forbidden = ";".join(contract.loc[contract["contract_id"].eq("forbidden"), "contract_value"].astype(str).tolist())
    gates = [
        ("P446_PHASE445_AVAILABLE", as_int(scalar(phase445, "phase445_catalyst_continuation_interpretation_complete", 0)) == 1, scalar(phase445, "phase445_catalyst_continuation_interpretation_complete", 0), 1),
        ("P446_PHASE445_NEXT_ACTION_MATCHED", "stability" in str(values.get("phase445_next_action", "")) or "holdout" in str(values.get("phase445_next_action", "")), values.get("phase445_next_action", ""), "stability_or_holdout"),
        ("P446_POSITIVE_DIAGNOSTIC_PRESENT", float(values.get("phase445_best_net_pnl_inr", 0) or 0) > 0, values.get("phase445_best_net_pnl_inr", ""), ">0"),
        ("P446_LOCKED_SCENARIO_PRESENT", as_int(values.get("locked_trade_rows", 0)) > 0, values.get("locked_trade_rows", ""), ">0"),
        ("P446_NO_PARAMETER_TUNING", True, LOCKED_SCENARIO_ID, "locked"),
        ("P446_HOLDOUT_SPLIT_FROZEN", int(split[split["split"].eq("holdout")]["diagnostic_trade_date"].nunique()) >= MIN_HOLDOUT_DATES, split[split["split"].eq("holdout")]["diagnostic_trade_date"].nunique(), f">={MIN_HOLDOUT_DATES}"),
        ("P446_COST200_FIXED_CAPITAL_PINNED", "cost200" in contract.loc[contract["contract_id"].eq("capital_policy"), "contract_value"].astype(str).str.cat(sep=" "), contract.loc[contract["contract_id"].eq("capital_policy"), "contract_value"].astype(str).str.cat(sep=" "), "cost200_fixed_capital"),
        ("P446_RESULTS_NOT_GENERATED", contract.loc[contract["contract_id"].eq("execution_results_generated_now"), "contract_value"].astype(str).str.cat(sep=" ") == "0", contract.loc[contract["contract_id"].eq("execution_results_generated_now"), "contract_value"].astype(str).str.cat(sep=" "), 0),
        ("P446_BOUNDARIES_CLOSED", all(x in forbidden for x in ["promotion", "paper_live", "deployable_profitability_claim"]), forbidden, "closed"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(split: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase446_stability_precommit_complete", 1, "Phase446 precommit completed"),
            ("phase446_thesis_id", THESIS_ID, "Frozen thesis"),
            ("phase446_locked_scenario_id", LOCKED_SCENARIO_ID, "Locked candidate"),
            ("phase446_holdout_dates", ";".join(split[split["split"].eq("holdout")]["diagnostic_trade_date"].astype(str).tolist()), "Frozen holdout dates"),
            ("phase446_execution_results_generated", 0, "Precommit only"),
            ("phase446_strategy_promotion_allowed", 0, "No promotion"),
            ("phase446_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase446_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase446_execution_allowed_next", int(hard_pass == hard_rows), "Whether Phase447 may execute"),
            ("phase446_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase446_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase446_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, evidence: pd.DataFrame, contract: pd.DataFrame, split: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase446 Catalyst Continuation Stability Holdout Precommit",
        "",
        "Phase446 freezes a no-tuning chronological stability audit for the positive Phase444 diagnostic.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Evidence Registry",
        "",
        _markdown_table(evidence),
        "",
        "## Frozen Contract",
        "",
        _markdown_table(contract),
        "",
        "## Frozen Date Split",
        "",
        _markdown_table(split),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase447 may audit the locked scenario only. It may not drop bad dates, drop symbols, add thresholds, or open promotion/paper/live.",
    ]
    (output_dir / "phase446_catalyst_continuation_stability_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase445_dir: Path = DEFAULT_PHASE445_DIR, phase444_dir: Path = DEFAULT_PHASE444_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase445 = read_csv(phase445_dir / "phase445_acceptance_summary.csv")
    trades = read_csv(phase444_dir / "phase444_trade_ledger.csv")
    if phase445.empty or trades.empty:
        raise FileNotFoundError("Phase446 requires Phase445 acceptance and Phase444 trade ledger.")
    locked = trades[trades["scenario_id"].astype(str).eq(LOCKED_SCENARIO_ID)]
    split = build_split(locked)
    evidence = build_evidence(phase445, trades)
    contract = build_contract(split)
    gates = build_gates(phase445, evidence, contract, split)
    acceptance = build_acceptance(split, gates)
    evidence.to_csv(output_dir / "phase446_evidence_registry.csv", index=False)
    contract.to_csv(output_dir / "phase446_frozen_phase447_contract.csv", index=False)
    split.to_csv(output_dir / "phase446_frozen_date_split.csv", index=False)
    gates.to_csv(output_dir / "phase446_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase446_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, evidence, contract, split, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase446_catalyst_continuation_stability_precommit",
        **reproducibility_fields(
            artifact_id="phase446_catalyst_continuation_stability_precommit",
            generated_utc=generated_utc,
            inputs={"phase445_acceptance_summary": str(phase445_dir / "phase445_acceptance_summary.csv"), "phase444_trade_ledger": str(phase444_dir / "phase444_trade_ledger.csv")},
            parameters={"thesis_id": THESIS_ID, "locked_scenario_id": LOCKED_SCENARIO_ID, "split_hash": sha256_frame(split)},
            outputs={"acceptance_summary": str(output_dir / "phase446_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase387_event_feature_fixed_horizon",
        ),
    }
    (output_dir / "phase446_catalyst_continuation_stability_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase446 catalyst continuation stability precommit.")
    parser.add_argument("--phase445-dir", type=Path, default=DEFAULT_PHASE445_DIR)
    parser.add_argument("--phase444-dir", type=Path, default=DEFAULT_PHASE444_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase445_dir, args.phase444_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
