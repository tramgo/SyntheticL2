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
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE446_DIR = Path("outputs/phase446")
DEFAULT_PHASE444_DIR = Path("outputs/phase444")
DEFAULT_OUTPUT_DIR = Path("outputs/phase447")

PHASE_ID = "P447_CATALYST_CONTINUATION_STABILITY_HOLDOUT_EXECUTION"
DEFAULT_LOCKED_SCENARIO_ID = "P444_catalyst_continuation_H600_replenishment_after_exhaustion_C5"
NEXT_ACTION_ACCEPTED = "precommit_real_l2_or_larger_chronological_holdout_confirmation"
NEXT_ACTION_REJECTED = "reject_catalyst_continuation_stability_or_precommit_new_source_edge"

MIN_HOLDOUT_NET_PNL_INR = 0.0
MIN_HOLDOUT_ANNUALIZED_PCT = 12.0
MIN_HOLDOUT_POSITIVE_DATE_FRACTION = 0.60
INITIAL_CAPITAL_INR = 1_000_000.0
ORDER_NOTIONAL_INR = 100_000.0


def sha256_frame(frame: pd.DataFrame) -> str:
    return hashlib.sha256(frame.to_csv(index=False, lineterminator="\n").encode("utf-8")).hexdigest()


def contract_value(contract: pd.DataFrame, key: str, default: str = "") -> str:
    if contract.empty or "contract_id" not in contract.columns:
        return default
    values = contract.loc[contract["contract_id"].astype(str).eq(key), "contract_value"].astype(str).tolist()
    return values[0] if values else default


def semicolon_list(value: str) -> list[str]:
    return [x.strip() for x in str(value).split(";") if x.strip()]


def annualized_return_pct(net_pnl_inr: float, distinct_dates: int) -> float:
    return (float(net_pnl_inr) / INITIAL_CAPITAL_INR) * (252.0 / max(1, int(distinct_dates))) * 100.0


def summarize_trades(trades: pd.DataFrame, split_name: str) -> dict[str, Any]:
    if trades.empty:
        return {
            "split": split_name,
            "completed_round_trips": 0,
            "trade_dates": 0,
            "symbols": 0,
            "positive_date_fraction": 0.0,
            "gross_pnl_inr": 0.0,
            "cost200_inr": 0.0,
            "net_pnl_inr": 0.0,
            "annualized_return_pct": 0.0,
        }
    date_pnl = trades.groupby("diagnostic_trade_date", dropna=False)["net_pnl_inr"].sum()
    distinct_dates = int(trades["diagnostic_trade_date"].nunique())
    net = float(trades["net_pnl_inr"].sum())
    return {
        "split": split_name,
        "completed_round_trips": int(len(trades)),
        "trade_dates": distinct_dates,
        "symbols": int(trades["symbol"].nunique()),
        "positive_date_fraction": float((date_pnl > 0).mean()) if len(date_pnl) else 0.0,
        "gross_pnl_inr": float(trades["gross_pnl_inr"].sum()),
        "cost200_inr": float(trades["cost200_inr"].sum()),
        "net_pnl_inr": net,
        "annualized_return_pct": annualized_return_pct(net, distinct_dates),
    }


def build_split_summary(locked: pd.DataFrame, frozen_split: pd.DataFrame) -> pd.DataFrame:
    joined = locked.merge(frozen_split, on="diagnostic_trade_date", how="left")
    rows = []
    for split_name in ["development", "holdout", "all_locked"]:
        subset = joined if split_name == "all_locked" else joined[joined["split"].astype(str).eq(split_name)]
        rows.append(summarize_trades(subset, split_name))
    return pd.DataFrame(rows)


def build_date_pnl(locked: pd.DataFrame, frozen_split: pd.DataFrame) -> pd.DataFrame:
    joined = locked.merge(frozen_split, on="diagnostic_trade_date", how="left")
    if joined.empty:
        return pd.DataFrame(columns=["diagnostic_trade_date", "split", "completed_round_trips", "symbols", "gross_pnl_inr", "cost200_inr", "net_pnl_inr"])
    grouped = (
        joined.groupby(["diagnostic_trade_date", "split"], dropna=False)
        .agg(
            completed_round_trips=("scenario_id", "size"),
            symbols=("symbol", "nunique"),
            gross_pnl_inr=("gross_pnl_inr", "sum"),
            cost200_inr=("cost200_inr", "sum"),
            net_pnl_inr=("net_pnl_inr", "sum"),
        )
        .reset_index()
        .sort_values(["diagnostic_trade_date", "split"])
    )
    return grouped


def build_symbol_pnl(locked: pd.DataFrame, frozen_split: pd.DataFrame) -> pd.DataFrame:
    joined = locked.merge(frozen_split, on="diagnostic_trade_date", how="left")
    if joined.empty:
        return pd.DataFrame(columns=["split", "symbol", "completed_round_trips", "trade_dates", "net_pnl_inr"])
    return (
        joined.groupby(["split", "symbol"], dropna=False)
        .agg(
            completed_round_trips=("scenario_id", "size"),
            trade_dates=("diagnostic_trade_date", "nunique"),
            gross_pnl_inr=("gross_pnl_inr", "sum"),
            cost200_inr=("cost200_inr", "sum"),
            net_pnl_inr=("net_pnl_inr", "sum"),
        )
        .reset_index()
        .sort_values(["split", "net_pnl_inr"], ascending=[True, False])
    )


def build_control_context(phase444_dir: Path, locked_scenario_id: str) -> pd.DataFrame:
    controls = read_csv(phase444_dir / "phase444_best_scenario_controls.csv")
    if controls.empty:
        return pd.DataFrame(columns=["control", "net_pnl_inr", "annualized_return_pct", "positive_date_fraction", "note"])
    out = controls[controls["scenario_id"].astype(str).eq(locked_scenario_id)].copy()
    out["note"] = out["control"].map(
        {
            "l1_only": "L1-only ablation context; not used for holdout selection.",
            "reversal": "Opposite-direction control context; not used for holdout selection.",
            "time_shifted_catalyst": "Temporal catalyst-shift control context; not used for holdout selection.",
        }
    ).fillna("Control context; not used for holdout selection.")
    return out[["control", "net_pnl_inr", "annualized_return_pct", "positive_date_fraction", "note"]]


def build_gates(
    phase446: pd.DataFrame,
    contract: pd.DataFrame,
    split: pd.DataFrame,
    locked: pd.DataFrame,
    split_summary: pd.DataFrame,
    locked_scenario_id: str,
) -> pd.DataFrame:
    holdout = split_summary[split_summary["split"].eq("holdout")]
    holdout_row = holdout.iloc[0].to_dict() if not holdout.empty else {}
    frozen_holdout_dates = sorted(split[split["split"].astype(str).eq("holdout")]["diagnostic_trade_date"].astype(str).tolist())
    contract_holdout_dates = sorted(semicolon_list(contract_value(contract, "holdout_dates")))
    observed_scenarios = sorted(locked["scenario_id"].astype(str).unique().tolist()) if not locked.empty else []
    gates = [
        ("P447_PHASE446_PRECOMMIT_AVAILABLE", as_int(phase446.loc[phase446["metric"].eq("phase446_stability_precommit_complete"), "value"].iloc[0]) == 1 if not phase446.empty and phase446["metric"].eq("phase446_stability_precommit_complete").any() else False, "phase446_stability_precommit_complete", 1),
        ("P447_LOCKED_SCENARIO_ONLY", observed_scenarios == [locked_scenario_id], ";".join(observed_scenarios), locked_scenario_id),
        ("P447_FROZEN_HOLDOUT_DATES_MATCH", frozen_holdout_dates == contract_holdout_dates, ";".join(frozen_holdout_dates), ";".join(contract_holdout_dates)),
        ("P447_NO_PARAMETER_TUNING", True, "Phase447 reads Phase446 locked contract and filters only locked scenario/date split.", "no tuning"),
        ("P447_HOLDOUT_TRADES_PRESENT", int(holdout_row.get("completed_round_trips", 0)) > 0, holdout_row.get("completed_round_trips", 0), ">0"),
        ("P447_HOLDOUT_NET_PNL_POSITIVE", float(holdout_row.get("net_pnl_inr", 0.0)) > MIN_HOLDOUT_NET_PNL_INR, holdout_row.get("net_pnl_inr", 0.0), f">{MIN_HOLDOUT_NET_PNL_INR}"),
        ("P447_HOLDOUT_ANNUALIZED_GE_12", float(holdout_row.get("annualized_return_pct", 0.0)) >= MIN_HOLDOUT_ANNUALIZED_PCT, holdout_row.get("annualized_return_pct", 0.0), f">={MIN_HOLDOUT_ANNUALIZED_PCT}"),
        ("P447_HOLDOUT_POSITIVE_DATE_FRACTION_GE_0_60", float(holdout_row.get("positive_date_fraction", 0.0)) >= MIN_HOLDOUT_POSITIVE_DATE_FRACTION, holdout_row.get("positive_date_fraction", 0.0), f">={MIN_HOLDOUT_POSITIVE_DATE_FRACTION}"),
        ("P447_COST200_FIXED_CAPITAL", "cost200" in contract_value(contract, "capital_policy") and "1000000" in contract_value(contract, "capital_policy"), contract_value(contract, "capital_policy"), "cost200_fixed_1000000_capital"),
        ("P447_NO_PROMOTION_PAPER_LIVE", True, "execution-only stability audit", "closed"),
    ]
    return pd.DataFrame([{"gate_id": gid, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gid, passed, observed, required in gates])


def build_acceptance(split_summary: pd.DataFrame, gates: pd.DataFrame, locked_scenario_id: str) -> pd.DataFrame:
    holdout = split_summary[split_summary["split"].eq("holdout")]
    holdout_row = holdout.iloc[0].to_dict() if not holdout.empty else {}
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    accepted = int(hard_pass == hard_rows)
    rows = [
        ("phase447_stability_holdout_complete", 1, "Phase447 holdout audit completed"),
        ("phase447_thesis_id", PHASE_ID, "Holdout execution thesis"),
        ("phase447_locked_scenario_id", locked_scenario_id, "Locked scenario audited"),
        ("phase447_holdout_completed_round_trips", int(holdout_row.get("completed_round_trips", 0)), "Holdout trades"),
        ("phase447_holdout_trade_dates", int(holdout_row.get("trade_dates", 0)), "Holdout dates"),
        ("phase447_holdout_symbols", int(holdout_row.get("symbols", 0)), "Holdout symbols"),
        ("phase447_holdout_gross_pnl_inr", float(holdout_row.get("gross_pnl_inr", 0.0)), "Holdout gross P&L"),
        ("phase447_holdout_cost200_inr", float(holdout_row.get("cost200_inr", 0.0)), "Holdout Zerodha cost200"),
        ("phase447_holdout_net_pnl_inr", float(holdout_row.get("net_pnl_inr", 0.0)), "Holdout net P&L after cost200"),
        ("phase447_holdout_annualized_return_pct", float(holdout_row.get("annualized_return_pct", 0.0)), "Holdout annualized return with fixed INR 1,000,000 capital"),
        ("phase447_holdout_positive_date_fraction", float(holdout_row.get("positive_date_fraction", 0.0)), "Holdout positive-date fraction"),
        ("phase447_acceptance_survivor", accepted, "Accepted only if every hard holdout gate passes"),
        ("phase447_strategy_promotion_allowed", 0, "No paper/live/deployable promotion in Phase447"),
        ("phase447_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase447_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase447_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase447_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase447_next_best_action", NEXT_ACTION_ACCEPTED if accepted else NEXT_ACTION_REJECTED, "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(
    output_dir: Path,
    acceptance: pd.DataFrame,
    split_summary: pd.DataFrame,
    date_pnl: pd.DataFrame,
    symbol_pnl: pd.DataFrame,
    controls: pd.DataFrame,
    gates: pd.DataFrame,
) -> None:
    lines = [
        "# Phase447 Catalyst Continuation Stability Holdout Execution",
        "",
        "Phase447 executes the Phase446 frozen chronological holdout. It does not tune parameters, drop losing dates, drop symbols, or make a paper/live claim.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Split Summary",
        "",
        _markdown_table(split_summary),
        "",
        "## Date P&L",
        "",
        _markdown_table(date_pnl),
        "",
        "## Symbol P&L",
        "",
        _markdown_table(symbol_pnl),
        "",
        "## Phase444 Control Context",
        "",
        _markdown_table(controls),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Verdict: the locked Phase444 diagnostic is accepted only if all hard Phase447 gates pass. Otherwise it remains a useful clue, not a tradable/stable strategy.",
    ]
    (output_dir / "phase447_catalyst_continuation_stability_holdout_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase446_dir: Path = DEFAULT_PHASE446_DIR, phase444_dir: Path = DEFAULT_PHASE444_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase446 = read_csv(phase446_dir / "phase446_acceptance_summary.csv")
    contract = read_csv(phase446_dir / "phase446_frozen_phase447_contract.csv")
    frozen_split = read_csv(phase446_dir / "phase446_frozen_date_split.csv")
    trades = read_csv(phase444_dir / "phase444_trade_ledger.csv")
    if phase446.empty or contract.empty or frozen_split.empty or trades.empty:
        raise FileNotFoundError("Phase447 requires Phase446 acceptance/contract/date split and Phase444 trade ledger.")

    locked_scenario_id = contract_value(contract, "locked_scenario_id", DEFAULT_LOCKED_SCENARIO_ID)
    locked = trades[trades["scenario_id"].astype(str).eq(locked_scenario_id)].copy()
    if locked.empty:
        raise ValueError(f"Locked scenario not found in Phase444 ledger: {locked_scenario_id}")

    frozen_split["diagnostic_trade_date"] = frozen_split["diagnostic_trade_date"].astype(str)
    locked["diagnostic_trade_date"] = locked["diagnostic_trade_date"].astype(str)
    split_summary = build_split_summary(locked, frozen_split)
    date_pnl = build_date_pnl(locked, frozen_split)
    symbol_pnl = build_symbol_pnl(locked, frozen_split)
    controls = build_control_context(phase444_dir, locked_scenario_id)
    gates = build_gates(phase446, contract, frozen_split, locked, split_summary, locked_scenario_id)
    acceptance = build_acceptance(split_summary, gates, locked_scenario_id)

    split_summary.to_csv(output_dir / "phase447_split_summary.csv", index=False)
    date_pnl.to_csv(output_dir / "phase447_date_pnl.csv", index=False)
    symbol_pnl.to_csv(output_dir / "phase447_symbol_pnl.csv", index=False)
    controls.to_csv(output_dir / "phase447_control_context.csv", index=False)
    gates.to_csv(output_dir / "phase447_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase447_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, split_summary, date_pnl, symbol_pnl, controls, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase447_catalyst_continuation_stability_holdout_execution",
        **reproducibility_fields(
            artifact_id="phase447_catalyst_continuation_stability_holdout_execution",
            generated_utc=generated_utc,
            inputs={
                "phase446_acceptance_summary": str(phase446_dir / "phase446_acceptance_summary.csv"),
                "phase446_frozen_phase447_contract": str(phase446_dir / "phase446_frozen_phase447_contract.csv"),
                "phase446_frozen_date_split": str(phase446_dir / "phase446_frozen_date_split.csv"),
                "phase444_trade_ledger": str(phase444_dir / "phase444_trade_ledger.csv"),
            },
            parameters={
                "phase_id": PHASE_ID,
                "locked_scenario_id": locked_scenario_id,
                "initial_capital_inr": INITIAL_CAPITAL_INR,
                "order_notional_inr": ORDER_NOTIONAL_INR,
                "min_holdout_annualized_pct": MIN_HOLDOUT_ANNUALIZED_PCT,
                "min_holdout_positive_date_fraction": MIN_HOLDOUT_POSITIVE_DATE_FRACTION,
                "frozen_split_hash": sha256_frame(frozen_split),
            },
            outputs={"acceptance_summary": str(output_dir / "phase447_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase387_event_feature_fixed_horizon",
        ),
    }
    (output_dir / "phase447_catalyst_continuation_stability_holdout_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase447 catalyst continuation stability holdout.")
    parser.add_argument("--phase446-dir", type=Path, default=DEFAULT_PHASE446_DIR)
    parser.add_argument("--phase444-dir", type=Path, default=DEFAULT_PHASE444_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase446_dir, args.phase444_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
