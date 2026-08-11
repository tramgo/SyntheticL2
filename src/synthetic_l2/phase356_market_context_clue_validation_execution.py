from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE354_DIR = Path("outputs/phase354")
DEFAULT_PHASE355_DIR = Path("outputs/phase355")
DEFAULT_OUTPUT_DIR = Path("outputs/phase356")
FROZEN_SCENARIO_ID = "P354_capacity_selected_events_NIFTYBEES_LB900_market_neutral_top5_fade"
INITIAL_CAPITAL_INR = 250_000.0
ROBUST_EVENT_FLOOR = 30
ANNUALIZED_THRESHOLD_PCT = 12.0


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


def side_top5_fade(frame: pd.DataFrame) -> pd.Series:
    return -np.sign(pd.to_numeric(frame["entry_top5_qty_imbalance"], errors="coerce").fillna(0.0))


def side_deep_fade(frame: pd.DataFrame) -> pd.Series:
    return -np.sign(pd.to_numeric(frame["entry_l2_l5_qty_imbalance"], errors="coerce").fillna(0.0))


def selected_base(enriched: pd.DataFrame, *, proxy_symbol: str, lookback_seconds: int) -> pd.DataFrame:
    frame = enriched.copy()
    return frame.loc[
        frame["capacity_selected"].fillna(0).astype(int).eq(1)
        & frame["proxy_symbol"].astype(str).eq(proxy_symbol)
        & frame["lookback_seconds"].astype(int).eq(int(lookback_seconds))
        & pd.to_numeric(frame["proxy_pre_return_bps"], errors="coerce").abs().le(1.0)
        & pd.to_numeric(frame["entry_top5_qty_imbalance"], errors="coerce").abs().ge(0.25)
    ].copy()


def score_rows(frame: pd.DataFrame, side: pd.Series, scenario_id: str, control_id: str, role: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    valid = side.ne(0)
    selected = frame.loc[valid].copy()
    selected_side = side.loc[valid]
    gross = selected_side * (selected["exit_mid"].astype(float) - selected["entry_mid"].astype(float)) * selected["quantity"].astype(float)
    net = gross - selected["zerodha_charges_2x_inr"].astype(float)
    selected["scenario_id"] = scenario_id
    selected["control_id"] = control_id
    selected["scenario_role"] = role
    selected["side"] = np.where(selected_side > 0, "long", "short")
    selected["gross_pnl_inr"] = gross.values
    selected["cost200_inr"] = selected["zerodha_charges_2x_inr"].astype(float).values
    selected["net_pnl_inr"] = net.values
    days = int(selected["diagnostic_trade_date"].nunique()) if not selected.empty else 0
    net_sum = float(net.sum())
    annualized = (net_sum / INITIAL_CAPITAL_INR) * (252.0 / max(1, days)) * 100.0
    by_symbol = selected.assign(_net=net.values).groupby("symbol")["_net"].sum() if not selected.empty else pd.Series(dtype=float)
    by_symbol_date = selected.assign(_net=net.values).groupby(["symbol", "diagnostic_trade_date"])["_net"].sum() if not selected.empty else pd.Series(dtype=float)
    row = {
        "scenario_id": scenario_id,
        "control_id": control_id,
        "scenario_role": role,
        "trade_rows": int(len(selected)),
        "diagnostic_trade_dates": days,
        "symbols": int(selected["symbol"].nunique()) if not selected.empty else 0,
        "positive_trade_rows": int((net > 0).sum()),
        "positive_symbols": int((by_symbol > 0).sum()),
        "positive_symbol_date_cells": int((by_symbol_date > 0).sum()),
        "net_pnl_inr": net_sum,
        "annualized_return_pct": annualized,
        "above12": int(annualized > ANNUALIZED_THRESHOLD_PCT),
        "event_floor_met": int(len(selected) >= ROBUST_EVENT_FLOOR),
        "breadth_met": int((by_symbol > 0).sum() >= 2 and (by_symbol_date > 0).sum() >= 2),
        "acceptance_candidate": int(
            annualized > ANNUALIZED_THRESHOLD_PCT
            and len(selected) >= ROBUST_EVENT_FLOOR
            and (by_symbol > 0).sum() >= 2
            and (by_symbol_date > 0).sum() >= 2
        ),
    }
    keep_cols = [
        "scenario_id",
        "control_id",
        "scenario_role",
        "work_order_id",
        "symbol",
        "diagnostic_trade_date",
        "description",
        "proxy_symbol",
        "lookback_seconds",
        "proxy_pre_return_bps",
        "entry_top5_qty_imbalance",
        "entry_l2_l5_qty_imbalance",
        "side",
        "entry_mid",
        "exit_mid",
        "quantity",
        "gross_pnl_inr",
        "cost200_inr",
        "net_pnl_inr",
    ]
    return selected[[c for c in keep_cols if c in selected.columns]].copy(), row


def evaluate(phase354_dir: Path, phase355_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    enriched = read_csv(phase354_dir / "phase354_market_context_event_ledger.csv")
    frozen_contract = read_csv(phase355_dir / "phase355_frozen_clue_contract.csv")
    validation_contract = read_csv(phase355_dir / "phase355_validation_contract.csv")
    if enriched.empty or frozen_contract.empty or validation_contract.empty:
        raise FileNotFoundError("Phase354/Phase355 evidence is incomplete")

    scenario_rows: list[dict[str, Any]] = []
    trade_frames: list[pd.DataFrame] = []

    frozen_base = selected_base(enriched, proxy_symbol="NIFTYBEES", lookback_seconds=900)
    frozen_trades, frozen_row = score_rows(
        frozen_base,
        side_top5_fade(frozen_base),
        "P356_FROZEN_NIFTYBEES_LB900_MARKET_NEUTRAL_TOP5_FADE",
        "frozen_clue",
        "frozen_validation",
    )
    trade_frames.append(frozen_trades)
    scenario_rows.append(frozen_row)

    side_flip_trades, side_flip_row = score_rows(
        frozen_base,
        -side_top5_fade(frozen_base),
        "P356_CONTROL_SIDE_FLIP",
        "side_flip",
        "control",
    )
    trade_frames.append(side_flip_trades)
    scenario_rows.append(side_flip_row)

    alt_side = pd.Series([1 if i % 2 == 0 else -1 for i in range(len(frozen_base))], index=frozen_base.index, dtype=float)
    alt_trades, alt_row = score_rows(
        frozen_base,
        alt_side,
        "P356_CONTROL_DETERMINISTIC_ALTERNATE_SIDE",
        "random_side_deterministic",
        "control",
    )
    trade_frames.append(alt_trades)
    scenario_rows.append(alt_row)

    bank_base = selected_base(enriched, proxy_symbol="BANKBEES", lookback_seconds=900)
    bank_trades, bank_row = score_rows(
        bank_base,
        side_top5_fade(bank_base),
        "P356_CONTROL_BANKBEES_LB900_MARKET_NEUTRAL_TOP5_FADE",
        "proxy_swap_bankbees",
        "control",
    )
    trade_frames.append(bank_trades)
    scenario_rows.append(bank_row)

    lb300_base = selected_base(enriched, proxy_symbol="NIFTYBEES", lookback_seconds=300)
    lb300_trades, lb300_row = score_rows(
        lb300_base,
        side_top5_fade(lb300_base),
        "P356_CONTROL_NIFTYBEES_LB300_MARKET_NEUTRAL_TOP5_FADE",
        "lookback_swap_300s",
        "control",
    )
    trade_frames.append(lb300_trades)
    scenario_rows.append(lb300_row)

    deep = pd.to_numeric(frozen_base["entry_l2_l5_qty_imbalance"], errors="coerce").fillna(0.0)
    top5 = pd.to_numeric(frozen_base["entry_top5_qty_imbalance"], errors="coerce").fillna(0.0)
    guard_base = frozen_base.loc[(np.sign(deep).eq(np.sign(top5))) | (deep.abs().lt(0.10))].copy()
    guard_trades, guard_row = score_rows(
        guard_base,
        side_top5_fade(guard_base),
        "P356_CONTROL_DEPTH_2_5_GUARD_TOP5_FADE",
        "depth_2_5_guard",
        "full_depth_guard",
    )
    trade_frames.append(guard_trades)
    scenario_rows.append(guard_row)

    deep_variant_base = frozen_base.loc[deep.abs().ge(0.25)].copy()
    deep_trades, deep_row = score_rows(
        deep_variant_base,
        side_deep_fade(deep_variant_base),
        "P356_CONTROL_DEPTH_2_5_FADE_VARIANT",
        "depth_2_5_fade_variant",
        "full_depth_control",
    )
    trade_frames.append(deep_trades)
    scenario_rows.append(deep_row)

    scenarios = pd.DataFrame(scenario_rows).sort_values(["scenario_role", "annualized_return_pct"], ascending=[False, False])
    trades = pd.concat(trade_frames, ignore_index=True) if trade_frames else pd.DataFrame()
    frozen = scenarios.loc[scenarios["control_id"].eq("frozen_clue")].iloc[0]
    controls = scenarios.loc[~scenarios["control_id"].eq("frozen_clue")].copy()
    control_dominates = int((controls["annualized_return_pct"].astype(float) > float(frozen["annualized_return_pct"])).any()) if not controls.empty else 0
    summary = pd.DataFrame(
        [
            ("phase356_market_context_clue_validation_execution_complete", 1, "Phase356 execution completed"),
            ("phase356_frozen_trade_rows", frozen["trade_rows"], "Frozen validation trade rows"),
            ("phase356_frozen_annualized_return_pct", frozen["annualized_return_pct"], "Frozen annualized return"),
            ("phase356_frozen_net_pnl_inr", frozen["net_pnl_inr"], "Frozen net PnL"),
            ("phase356_frozen_above12", frozen["above12"], "Frozen above 12%"),
            ("phase356_frozen_event_floor_met", frozen["event_floor_met"], "Frozen >=30 events"),
            ("phase356_control_rows", len(controls), "Control scenario rows"),
            ("phase356_control_dominates_frozen", control_dominates, "Any control annualized return greater than frozen"),
            ("phase356_acceptance_candidate_rows", int(scenarios["acceptance_candidate"].sum()), "Acceptance candidates"),
            ("phase356_strategy_promotion_allowed", 0, "No promotion"),
            ("phase356_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase356_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase356_next_best_action", "restore_phase350_real_date_expansion_for_unseen_event_floor_no_paper_live", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    gates = pd.DataFrame(
        [
            ("P356_PHASE355_PRECOMMIT_PRESENT", 1, "Phase355 frozen contract present"),
            ("P356_FROZEN_CLUE_RECONCILED", int(int(frozen["trade_rows"]) == 14), f"trade_rows={frozen['trade_rows']}"),
            ("P356_EVENT_FLOOR_CHECKED", 1, f"event_floor_met={frozen['event_floor_met']}"),
            ("P356_CONTROLS_EXECUTED", int(len(controls) >= 6), f"control_rows={len(controls)}"),
            ("P356_CONTROL_DOMINANCE_RECORDED", 1, f"control_dominates={control_dominates}"),
            ("P356_COST200_FIXED_CAPITAL", 1, "2x Zerodha cost and fixed INR 250000"),
            ("P356_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "closed"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )
    return scenarios, trades, summary, gates


def write_outputs(phase354_dir: Path, phase355_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    scenarios, trades, summary, gates = evaluate(phase354_dir, phase355_dir)
    outputs = {
        "summary": output_dir / "phase356_acceptance_summary.csv",
        "scenarios": output_dir / "phase356_scenario_summary.csv",
        "trades": output_dir / "phase356_trade_ledger.csv",
        "gates": output_dir / "phase356_gate_evaluation.csv",
        "report": output_dir / "phase356_market_context_clue_validation_execution_report.md",
        "manifest": output_dir / "phase356_market_context_clue_validation_execution_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    scenarios.to_csv(outputs["scenarios"], index=False)
    trades.to_csv(outputs["trades"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    report = "\n".join(
        [
            "# Phase356 Market-Context Clue Validation Execution",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase356 executes the Phase355 frozen clue and required controls on the current local real-L2 panel.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Scenario summary",
            "",
            _markdown_table(scenarios),
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
        "phase": 356,
        "generated_at_utc": generated_utc,
        "phase354_dir": str(phase354_dir),
        "phase355_dir": str(phase355_dir),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase356_market_context_clue_validation_execution",
            generated_utc=generated_utc,
            inputs={"phase354_dir": str(phase354_dir), "phase355_dir": str(phase355_dir)},
            parameters={"frozen_scenario_id": FROZEN_SCENARIO_ID, "event_floor": ROBUST_EVENT_FLOOR},
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase354_phase342_entry_exit_timestamps",
        ),
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase354-dir", type=Path, default=DEFAULT_PHASE354_DIR)
    parser.add_argument("--phase355-dir", type=Path, default=DEFAULT_PHASE355_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase354_dir, args.phase355_dir, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
