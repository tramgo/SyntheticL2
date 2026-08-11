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


DEFAULT_PHASE342_LEDGER = Path("outputs/phase342/phase342_real_day_trade_diagnostic_ledger.csv")
DEFAULT_OUTPUT_DIR = Path("outputs/phase353")
INITIAL_CAPITAL_INR = 250_000.0
ANNUALIZED_THRESHOLD_PCT = 12.0
ROBUST_EVENT_FLOOR = 30


RULES = [
    ("follow_l2_l5", "entry_l2_l5_qty_imbalance", 1, "Follow depth-levels-2-5 quantity imbalance."),
    ("fade_l2_l5", "entry_l2_l5_qty_imbalance", -1, "Fade depth-levels-2-5 quantity imbalance."),
    ("follow_top5", "entry_top5_qty_imbalance", 1, "Follow top-five quantity imbalance."),
    ("fade_top5", "entry_top5_qty_imbalance", -1, "Fade top-five quantity imbalance."),
    ("follow_order", "entry_top5_order_imbalance", 1, "Follow top-five order-count imbalance."),
    ("fade_order", "entry_top5_order_imbalance", -1, "Fade top-five order-count imbalance."),
]

LEAD_CATEGORIES = {
    "General Updates",
    "Updates",
    "Credit Rating",
    "Press Release",
    "Analysts/Institutional Investor Meet/Con. Call Updates",
}


def load_ledger(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    frame = frame.loc[frame["status"].astype(str).eq("filled")].copy()
    numeric = [
        "entry_mid",
        "exit_mid",
        "quantity",
        "zerodha_charges_2x_inr",
        "entry_l2_l5_qty_imbalance",
        "entry_top5_qty_imbalance",
        "entry_top5_order_imbalance",
        "capacity_selected",
    ]
    for column in numeric:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame


def scope_frames(ledger: pd.DataFrame) -> list[tuple[str, pd.DataFrame]]:
    return [
        ("all_official_catalyst_events", ledger),
        ("lead_catalyst_categories", ledger.loc[ledger["description"].astype(str).isin(LEAD_CATEGORIES)]),
        ("capacity_selected_events", ledger.loc[ledger["capacity_selected"].fillna(0).astype(int).eq(1)]),
    ]


def evaluate(ledger: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    scenario_rows: list[dict[str, Any]] = []
    trade_rows: list[dict[str, Any]] = []
    for scope, frame in scope_frames(ledger):
        if frame.empty:
            continue
        diagnostic_days = int(frame["diagnostic_trade_date"].nunique())
        for rule_id, column, multiplier, description in RULES:
            signal = np.sign(frame[column].fillna(0.0).astype(float)) * float(multiplier)
            pnl = signal * (frame["exit_mid"].astype(float) - frame["entry_mid"].astype(float)) * frame["quantity"].astype(float)
            net = pnl - frame["zerodha_charges_2x_inr"].astype(float)
            valid = signal.ne(0)
            selected = frame.loc[valid].copy()
            selected_net = net.loc[valid]
            selected_signal = signal.loc[valid]
            scenario_id = f"P353_{scope}_{rule_id}"
            for idx, row in selected.iterrows():
                trade_rows.append(
                    {
                        "scenario_id": scenario_id,
                        "scope": scope,
                        "rule_id": rule_id,
                        "work_order_id": row["work_order_id"],
                        "symbol": row["symbol"],
                        "diagnostic_trade_date": row["diagnostic_trade_date"],
                        "description": row["description"],
                        "side": "long" if selected_signal.loc[idx] > 0 else "short",
                        "entry_mid": row["entry_mid"],
                        "exit_mid": row["exit_mid"],
                        "quantity": row["quantity"],
                        "gross_pnl_inr": float(pnl.loc[idx]),
                        "cost200_inr": row["zerodha_charges_2x_inr"],
                        "net_pnl_inr": float(selected_net.loc[idx]),
                        "entry_l2_l5_qty_imbalance": row["entry_l2_l5_qty_imbalance"],
                        "entry_top5_qty_imbalance": row["entry_top5_qty_imbalance"],
                        "entry_top5_order_imbalance": row["entry_top5_order_imbalance"],
                        "uses_full_depth_1_5": 1,
                        "uses_depth_2_5_materiality": 1 if "l2_l5" in rule_id else 0,
                        "l1_only_variant": 0,
                    }
                )
            net_sum = float(selected_net.sum())
            annualized = (net_sum / INITIAL_CAPITAL_INR) * (252.0 / max(1, diagnostic_days)) * 100.0
            positive_symbol_dates = int(
                (selected.assign(_net=selected_net.values).groupby(["symbol", "diagnostic_trade_date"])["_net"].sum() > 0).sum()
            )
            positive_symbols = int((selected.assign(_net=selected_net.values).groupby("symbol")["_net"].sum() > 0).sum())
            scenario_rows.append(
                {
                    "scenario_id": scenario_id,
                    "scope": scope,
                    "rule_id": rule_id,
                    "rule_description": description,
                    "trade_rows": int(len(selected)),
                    "diagnostic_trade_dates": diagnostic_days,
                    "symbols": int(selected["symbol"].nunique()),
                    "positive_trade_rows": int((selected_net > 0).sum()),
                    "positive_symbol_date_cells": positive_symbol_dates,
                    "positive_symbols": positive_symbols,
                    "net_pnl_inr": net_sum,
                    "annualized_return_pct": annualized,
                    "above12": int(annualized > ANNUALIZED_THRESHOLD_PCT),
                    "event_floor_met": int(len(selected) >= ROBUST_EVENT_FLOOR),
                    "breadth_met": int(positive_symbols >= 2 and positive_symbol_dates >= 2),
                    "acceptance_candidate": int(
                        annualized > ANNUALIZED_THRESHOLD_PCT
                        and len(selected) >= ROBUST_EVENT_FLOOR
                        and positive_symbols >= 2
                        and positive_symbol_dates >= 2
                    ),
                    "cost_model_version": ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
                    "cost_profile": "zerodha_2x_all_in_cost_proxy",
                    "initial_capital_inr": INITIAL_CAPITAL_INR,
                    "uses_real_l2": 1,
                    "uses_official_catalyst_events": 1,
                    "uses_full_depth_1_5": 1,
                    "l1_only_variant": 0,
                }
            )
    scenarios = pd.DataFrame(scenario_rows).sort_values(["annualized_return_pct", "trade_rows"], ascending=[False, False])
    trades = pd.DataFrame(trade_rows)
    best = scenarios.iloc[0] if not scenarios.empty else pd.Series(dtype=object)
    summary = pd.DataFrame(
        [
            ("phase353_real_catalyst_l2_side_selection_complete", 1, "Phase353 diagnostic completed"),
            ("phase353_phase342_filled_input_rows", len(ledger), "Filled Phase342 rows used"),
            ("phase353_scenario_rows", len(scenarios), "Scenario rows evaluated"),
            ("phase353_trade_rows", len(trades), "Trade rows evaluated"),
            ("phase353_above12_rows", int(scenarios["above12"].sum()) if not scenarios.empty else 0, "Above-12 rows"),
            ("phase353_acceptance_candidate_rows", int(scenarios["acceptance_candidate"].sum()) if not scenarios.empty else 0, "Acceptance candidates"),
            ("phase353_best_scenario_id", best.get("scenario_id", ""), "Best scenario"),
            ("phase353_best_annualized_return_pct", best.get("annualized_return_pct", 0), "Best annualized return"),
            ("phase353_best_net_pnl_inr", best.get("net_pnl_inr", 0), "Best net PnL"),
            ("phase353_strategy_promotion_allowed", 0, "No promotion"),
            ("phase353_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase353_deployable_profitability_claim_allowed", 0, "No profitability claim"),
            ("phase353_next_best_action", "restore_phase350_real_date_expansion_or_precommit_material_new_thesis_no_paper_live", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    return scenarios, trades, summary


def write_outputs(ledger_path: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    ledger = load_ledger(ledger_path)
    scenarios, trades, summary = evaluate(ledger)
    gates = pd.DataFrame(
        [
            ("P353_PHASE342_LEDGER_PRESENT", 1, f"filled_rows={len(ledger)}"),
            ("P353_REAL_L2_USED", 1, "Phase342 real L2 diagnostic ledger"),
            ("P353_OFFICIAL_CATALYST_USED", 1, "Phase340/342 official catalyst work order lineage"),
            ("P353_FULL_DEPTH_SIDE_RULES_PRESENT", 1, "top-five and depth-levels-2-5 rules evaluated"),
            ("P353_L1_ONLY_FORBIDDEN", int(scenarios.empty or scenarios["l1_only_variant"].sum() == 0), "No L1-only variants"),
            ("P353_COST200_FIXED_CAPITAL", 1, "2x Zerodha cost and fixed INR 250000 annualization"),
            ("P353_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "closed"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )
    outputs = {
        "summary": output_dir / "phase353_acceptance_summary.csv",
        "scenarios": output_dir / "phase353_scenario_summary.csv",
        "trades": output_dir / "phase353_trade_ledger.csv",
        "gates": output_dir / "phase353_gate_evaluation.csv",
        "report": output_dir / "phase353_real_catalyst_l2_side_selection_diagnostic_report.md",
        "manifest": output_dir / "phase353_real_catalyst_l2_side_selection_diagnostic_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    scenarios.to_csv(outputs["scenarios"], index=False)
    trades.to_csv(outputs["trades"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    report = "\n".join(
        [
            "# Phase353 Real-Catalyst L2 Side-Selection Diagnostic",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase353 tests a materially different real-data lever: selecting long/short direction from entry top-five and depth-levels-2-5 imbalance on official-catalyst real L2 events, instead of inheriting the prior long-only survivor direction.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Top scenarios",
            "",
            _markdown_table(scenarios.head(20)),
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
        "phase": 353,
        "generated_at_utc": generated_utc,
        "ledger_path": str(ledger_path),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase353_real_catalyst_l2_side_selection_diagnostic",
            generated_utc=generated_utc,
            inputs={"ledger_path": str(ledger_path)},
            parameters={"rules": [rule[0] for rule in RULES], "initial_capital_inr": INITIAL_CAPITAL_INR},
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase342_entry_exit_timestamps_reused",
        ),
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=DEFAULT_PHASE342_LEDGER)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.ledger, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
