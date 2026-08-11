from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE342_LEDGER = Path("outputs/phase342/phase342_real_day_trade_diagnostic_ledger.csv")
DEFAULT_REAL_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_OUTPUT_DIR = Path("outputs/phase354")
INITIAL_CAPITAL_INR = 250_000.0
ANNUALIZED_THRESHOLD_PCT = 12.0
ROBUST_EVENT_FLOOR = 30
PROXY_SYMBOLS = ["NIFTYBEES", "BANKBEES"]
LOOKBACK_SECONDS = [300, 900]
LEAD_CATEGORIES = {
    "General Updates",
    "Updates",
    "Credit Rating",
    "Press Release",
    "Analysts/Institutional Investor Meet/Con. Call Updates",
}


RULES = [
    {
        "rule_id": "market_confirmed_deep_follow",
        "description": "Follow depth-levels-2-5 imbalance only when market proxy pre-return agrees.",
        "min_abs_market_bps": 1.0,
        "min_abs_deep": 0.25,
        "side": "follow_deep",
        "requires_agreement": True,
    },
    {
        "rule_id": "market_confirmed_top5_follow",
        "description": "Follow top-five imbalance only when market proxy pre-return agrees.",
        "min_abs_market_bps": 1.0,
        "min_abs_deep": 0.25,
        "side": "follow_top5",
        "requires_agreement": True,
    },
    {
        "rule_id": "market_stretched_deep_fade",
        "description": "Fade depth-levels-2-5 imbalance when market proxy is already stretched in the same direction.",
        "min_abs_market_bps": 4.0,
        "min_abs_deep": 0.25,
        "side": "fade_deep",
        "requires_agreement": True,
    },
    {
        "rule_id": "market_neutral_top5_fade",
        "description": "Fade top-five imbalance only when market proxy pre-return is quiet.",
        "max_abs_market_bps": 1.0,
        "min_abs_deep": 0.25,
        "side": "fade_top5",
        "requires_agreement": False,
    },
]


def load_ledger(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    frame = frame.loc[frame["status"].astype(str).eq("filled")].copy()
    numeric = [
        "entry_ms",
        "exit_ms",
        "entry_mid",
        "exit_mid",
        "quantity",
        "zerodha_charges_2x_inr",
        "entry_l2_l5_qty_imbalance",
        "entry_top5_qty_imbalance",
        "capacity_selected",
    ]
    for column in numeric:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame


def load_proxy(real_root: Path, trade_date: str, proxy_symbol: str) -> pd.DataFrame:
    path = real_root / f"trade_date={trade_date}" / "exchange=NSE" / f"symbol={proxy_symbol}" / "*.parquet"
    con = duckdb.connect()
    try:
        frame = con.execute(
            """
            select
                collector_received_utc_ms as ts_ms,
                ((buy_1_price + sell_1_price) / 2.0) as mid_price,
                (sell_1_price - buy_1_price) as spread,
                last_price
            from read_parquet(?)
            where buy_1_price > 0 and sell_1_price > 0 and sell_1_price >= buy_1_price
            order by collector_received_utc_ms
            """,
            [path.as_posix()],
        ).fetchdf()
    finally:
        con.close()
    return frame


def nearest_mid(proxy: pd.DataFrame, ts_ms: float) -> float | None:
    if proxy.empty:
        return None
    idx = int(np.searchsorted(proxy["ts_ms"].to_numpy(), ts_ms, side="right") - 1)
    if idx < 0:
        idx = 0
    return float(proxy.iloc[idx]["mid_price"])


def enrich_with_market_context(ledger: pd.DataFrame, real_root: Path) -> pd.DataFrame:
    proxy_cache: dict[tuple[str, str], pd.DataFrame] = {}
    rows: list[dict[str, Any]] = []
    for _, row in ledger.iterrows():
        trade_date = str(row["diagnostic_trade_date"])
        for proxy_symbol in PROXY_SYMBOLS:
            key = (trade_date, proxy_symbol)
            if key not in proxy_cache:
                try:
                    proxy_cache[key] = load_proxy(real_root, trade_date, proxy_symbol)
                except Exception:
                    proxy_cache[key] = pd.DataFrame()
            proxy = proxy_cache[key]
            entry_mid = nearest_mid(proxy, float(row["entry_ms"]))
            exit_mid = nearest_mid(proxy, float(row["exit_ms"]))
            for lookback in LOOKBACK_SECONDS:
                lookback_mid = nearest_mid(proxy, float(row["entry_ms"]) - lookback * 1000.0)
                if entry_mid is None or lookback_mid is None or lookback_mid <= 0:
                    pre_return_bps = np.nan
                else:
                    pre_return_bps = (entry_mid / lookback_mid - 1.0) * 10000.0
                if entry_mid is None or exit_mid is None or entry_mid <= 0:
                    proxy_event_return_bps = np.nan
                else:
                    proxy_event_return_bps = (exit_mid / entry_mid - 1.0) * 10000.0
                enriched = row.to_dict()
                enriched.update(
                    {
                        "proxy_symbol": proxy_symbol,
                        "lookback_seconds": lookback,
                        "proxy_entry_mid": entry_mid,
                        "proxy_lookback_mid": lookback_mid,
                        "proxy_exit_mid": exit_mid,
                        "proxy_pre_return_bps": pre_return_bps,
                        "proxy_event_return_bps": proxy_event_return_bps,
                    }
                )
                rows.append(enriched)
    return pd.DataFrame(rows)


def scope_frames(frame: pd.DataFrame) -> list[tuple[str, pd.DataFrame]]:
    return [
        ("all_official_catalyst_events", frame),
        ("lead_catalyst_categories", frame.loc[frame["description"].astype(str).isin(LEAD_CATEGORIES)]),
        ("capacity_selected_events", frame.loc[frame["capacity_selected"].fillna(0).astype(int).eq(1)]),
    ]


def side_for_rule(rule: dict[str, Any], frame: pd.DataFrame) -> pd.Series:
    if rule["side"] == "follow_deep":
        return np.sign(frame["entry_l2_l5_qty_imbalance"].astype(float))
    if rule["side"] == "fade_deep":
        return -np.sign(frame["entry_l2_l5_qty_imbalance"].astype(float))
    if rule["side"] == "follow_top5":
        return np.sign(frame["entry_top5_qty_imbalance"].astype(float))
    if rule["side"] == "fade_top5":
        return -np.sign(frame["entry_top5_qty_imbalance"].astype(float))
    raise ValueError(f"Unknown rule side {rule['side']}")


def evaluate(enriched: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    scenario_rows: list[dict[str, Any]] = []
    trade_rows: list[dict[str, Any]] = []
    for scope, scope_frame in scope_frames(enriched):
        if scope_frame.empty:
            continue
        for proxy_symbol in PROXY_SYMBOLS:
            for lookback in LOOKBACK_SECONDS:
                base = scope_frame.loc[
                    scope_frame["proxy_symbol"].astype(str).eq(proxy_symbol)
                    & scope_frame["lookback_seconds"].astype(int).eq(int(lookback))
                    & scope_frame["proxy_pre_return_bps"].notna()
                ].copy()
                if base.empty:
                    continue
                for rule in RULES:
                    side = side_for_rule(rule, base)
                    mask = side.ne(0)
                    if "min_abs_market_bps" in rule:
                        mask &= base["proxy_pre_return_bps"].abs().ge(float(rule["min_abs_market_bps"]))
                    if "max_abs_market_bps" in rule:
                        mask &= base["proxy_pre_return_bps"].abs().le(float(rule["max_abs_market_bps"]))
                    if rule.get("requires_agreement", False):
                        raw_signal = side if not str(rule["side"]).startswith("fade") else -side
                        mask &= np.sign(base["proxy_pre_return_bps"]).eq(np.sign(raw_signal))
                    if "deep" in str(rule["side"]):
                        mask &= base["entry_l2_l5_qty_imbalance"].abs().ge(float(rule["min_abs_deep"]))
                    else:
                        mask &= base["entry_top5_qty_imbalance"].abs().ge(float(rule["min_abs_deep"]))
                    selected = base.loc[mask].copy()
                    selected_side = side.loc[mask]
                    if selected.empty:
                        continue
                    gross = selected_side * (selected["exit_mid"].astype(float) - selected["entry_mid"].astype(float)) * selected["quantity"].astype(float)
                    net = gross - selected["zerodha_charges_2x_inr"].astype(float)
                    scenario_id = f"P354_{scope}_{proxy_symbol}_LB{lookback}_{rule['rule_id']}"
                    for idx, row in selected.iterrows():
                        trade_rows.append(
                            {
                                "scenario_id": scenario_id,
                                "scope": scope,
                                "proxy_symbol": proxy_symbol,
                                "lookback_seconds": lookback,
                                "rule_id": rule["rule_id"],
                                "work_order_id": row["work_order_id"],
                                "symbol": row["symbol"],
                                "diagnostic_trade_date": row["diagnostic_trade_date"],
                                "description": row["description"],
                                "side": "long" if selected_side.loc[idx] > 0 else "short",
                                "entry_mid": row["entry_mid"],
                                "exit_mid": row["exit_mid"],
                                "quantity": row["quantity"],
                                "proxy_pre_return_bps": row["proxy_pre_return_bps"],
                                "proxy_event_return_bps": row["proxy_event_return_bps"],
                                "entry_l2_l5_qty_imbalance": row["entry_l2_l5_qty_imbalance"],
                                "entry_top5_qty_imbalance": row["entry_top5_qty_imbalance"],
                                "gross_pnl_inr": float(gross.loc[idx]),
                                "cost200_inr": row["zerodha_charges_2x_inr"],
                                "net_pnl_inr": float(net.loc[idx]),
                            }
                        )
                    diagnostic_days = int(selected["diagnostic_trade_date"].nunique())
                    net_sum = float(net.sum())
                    annualized = (net_sum / INITIAL_CAPITAL_INR) * (252.0 / max(1, diagnostic_days)) * 100.0
                    by_symbol = selected.assign(_net=net.values).groupby("symbol")["_net"].sum()
                    by_symbol_date = selected.assign(_net=net.values).groupby(["symbol", "diagnostic_trade_date"])["_net"].sum()
                    positive_symbols = int((by_symbol > 0).sum())
                    positive_symbol_dates = int((by_symbol_date > 0).sum())
                    scenario_rows.append(
                        {
                            "scenario_id": scenario_id,
                            "scope": scope,
                            "proxy_symbol": proxy_symbol,
                            "lookback_seconds": lookback,
                            "rule_id": rule["rule_id"],
                            "trade_rows": int(len(selected)),
                            "diagnostic_trade_dates": diagnostic_days,
                            "symbols": int(selected["symbol"].nunique()),
                            "positive_trade_rows": int((net > 0).sum()),
                            "positive_symbols": positive_symbols,
                            "positive_symbol_date_cells": positive_symbol_dates,
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
                            "uses_real_l2": 1,
                            "uses_market_proxy_l2": 1,
                            "uses_official_catalyst_events": 1,
                            "uses_full_depth_1_5": 1,
                            "uses_depth_2_5": int("deep" in str(rule["side"])),
                            "l1_only_variant": 0,
                        }
                    )
    scenarios = pd.DataFrame(scenario_rows).sort_values(["annualized_return_pct", "trade_rows"], ascending=[False, False])
    trades = pd.DataFrame(trade_rows)
    best = scenarios.iloc[0] if not scenarios.empty else pd.Series(dtype=object)
    summary = pd.DataFrame(
        [
            ("phase354_real_catalyst_market_context_diagnostic_complete", 1, "Phase354 diagnostic completed"),
            ("phase354_enriched_event_rows", len(enriched), "Proxy-enriched event rows"),
            ("phase354_scenario_rows", len(scenarios), "Scenario rows evaluated"),
            ("phase354_trade_rows", len(trades), "Trade rows evaluated"),
            ("phase354_above12_rows", int(scenarios["above12"].sum()) if not scenarios.empty else 0, "Above-12 rows"),
            ("phase354_acceptance_candidate_rows", int(scenarios["acceptance_candidate"].sum()) if not scenarios.empty else 0, "Acceptance candidates"),
            ("phase354_best_scenario_id", best.get("scenario_id", ""), "Best scenario"),
            ("phase354_best_annualized_return_pct", best.get("annualized_return_pct", 0), "Best annualized return"),
            ("phase354_best_net_pnl_inr", best.get("net_pnl_inr", 0), "Best net PnL"),
            ("phase354_strategy_promotion_allowed", 0, "No promotion"),
            ("phase354_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase354_deployable_profitability_claim_allowed", 0, "No profitability claim"),
            ("phase354_next_best_action", "restore_phase350_real_date_expansion_or_precommit_non_directional_liquidity_forecast_no_paper_live", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    return scenarios, trades, summary


def write_outputs(ledger_path: Path, real_root: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    ledger = load_ledger(ledger_path)
    enriched = enrich_with_market_context(ledger, real_root)
    scenarios, trades, summary = evaluate(enriched)
    gates = pd.DataFrame(
        [
            ("P354_PHASE342_LEDGER_PRESENT", 1, f"filled_rows={len(ledger)}"),
            ("P354_MARKET_PROXY_L2_PRESENT", int(enriched["proxy_pre_return_bps"].notna().sum() > 0), "NIFTYBEES/BANKBEES proxy context joined"),
            ("P354_REAL_L2_AND_OFFICIAL_CATALYST_USED", 1, "Phase342 real L2 plus official catalyst lineage"),
            ("P354_MARKET_CONTEXT_RULES_EVALUATED", int(len(scenarios) > 0), f"scenario_rows={len(scenarios)}"),
            ("P354_L1_ONLY_FORBIDDEN", int(scenarios.empty or scenarios["l1_only_variant"].sum() == 0), "No L1-only variants"),
            ("P354_COST200_FIXED_CAPITAL", 1, "2x Zerodha cost and fixed INR 250000 annualization"),
            ("P354_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "closed"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )
    outputs = {
        "summary": output_dir / "phase354_acceptance_summary.csv",
        "enriched": output_dir / "phase354_market_context_event_ledger.csv",
        "scenarios": output_dir / "phase354_scenario_summary.csv",
        "trades": output_dir / "phase354_trade_ledger.csv",
        "gates": output_dir / "phase354_gate_evaluation.csv",
        "report": output_dir / "phase354_real_catalyst_market_context_diagnostic_report.md",
        "manifest": output_dir / "phase354_real_catalyst_market_context_diagnostic_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    enriched.to_csv(outputs["enriched"], index=False)
    scenarios.to_csv(outputs["scenarios"], index=False)
    trades.to_csv(outputs["trades"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    report = "\n".join(
        [
            "# Phase354 Real-Catalyst Market-Context L2 Diagnostic",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase354 tests a structural real-data thesis: official-catalyst trades require entry-time full-depth state plus NIFTYBEES/BANKBEES market-proxy context, rather than raw catalyst or raw imbalance alone.",
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
        "phase": 354,
        "generated_at_utc": generated_utc,
        "ledger_path": str(ledger_path),
        "real_root": str(real_root),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase354_real_catalyst_market_context_diagnostic",
            generated_utc=generated_utc,
            inputs={"ledger_path": str(ledger_path), "real_root": str(real_root)},
            parameters={"proxy_symbols": PROXY_SYMBOLS, "lookback_seconds": LOOKBACK_SECONDS, "initial_capital_inr": INITIAL_CAPITAL_INR},
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase342_entry_exit_timestamps_with_proxy_lookback",
        ),
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=DEFAULT_PHASE342_LEDGER)
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.ledger, args.real_root, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
