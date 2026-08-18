from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, calculate_equity_intraday_nse_charges


DEFAULT_PHASE451_DIR = Path("outputs/phase451")
DEFAULT_DENSE_ROOT = Path("raw_synthetic_l2_dense_full_year")
DEFAULT_OUTPUT_DIR = Path("outputs/phase452")

THESIS_ID = "P452_CROSS_ASSET_ETF_PRESSURE_EXECUTION"
PRIMARY_SCENARIO_ID = "P452_cross_asset_etf_pressure_primary"
TIME_SHIFT_SCENARIO_ID = "P452_cross_asset_etf_pressure_source_time_shift"
SIDE_FLIP_SCENARIO_ID = "P452_cross_asset_etf_pressure_side_flip"
TARGET_ONLY_SCENARIO_ID = "P452_cross_asset_target_only_l1_l5"
ETF_L1_ONLY_SCENARIO_ID = "P452_cross_asset_etf_l1_only"
NEXT_ACTION = "interpret_phase452_cross_asset_etf_pressure_no_paper_live"

ETF_PROXIES = ["NIFTYBEES", "BANKBEES", "ITBEES"]
TARGET_SYMBOLS = ["AXISBANK", "HDFCBANK", "ICICIBANK", "INFY", "HCLTECH", "TCS", "RELIANCE"]
MONTHS = [f"2026-{m:02d}" for m in range(1, 7)]
BANK_TARGETS = {"AXISBANK", "HDFCBANK", "ICICIBANK"}
IT_TARGETS = {"INFY", "HCLTECH", "TCS"}

INITIAL_CAPITAL_INR = 1_000_000.0
ORDER_NOTIONAL_INR = 100_000.0
COST_MULTIPLIER = 2.0
HORIZON_TICKS = 240
STOP_BPS = 18.0
TAKE_PROFIT_BPS = 30.0
SAMPLE_STRIDE = 4096
BATCH_SIZE = 250_000
EVENT_INDEX = 20

NEEDED_COLUMNS = [
    "exchange_timestamp_ms",
    "trade_date",
    "exchange",
    "symbol",
    "last_price",
    "buy_1_price",
    "sell_1_price",
    "buy_1_quantity",
    "sell_1_quantity",
    "buy_2_quantity",
    "buy_3_quantity",
    "buy_4_quantity",
    "buy_5_quantity",
    "sell_2_quantity",
    "sell_3_quantity",
    "sell_4_quantity",
    "sell_5_quantity",
]


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def contract_value(contract: pd.DataFrame, key: str, default: str = "") -> str:
    rows = contract.loc[contract["contract_id"].astype(str).eq(key), "contract_value"].astype(str).tolist()
    return rows[0] if rows else default


def split_list(value: str) -> list[str]:
    return [x.strip() for x in str(value).split(";") if x.strip()]


def file_for(dense_root: Path, month: str, symbol: str) -> Path:
    return dense_root / f"trade_month={month}" / f"symbol={symbol}" / "part-00000.parquet"


def selected_files(dense_root: Path, months: list[str], symbols: list[str]) -> pd.DataFrame:
    rows = []
    for month in months:
        for symbol in symbols:
            path = file_for(dense_root, month, symbol)
            rows.append({"trade_month": month, "symbol": symbol, "path": str(path), "exists": int(path.exists())})
    return pd.DataFrame(rows)


def read_strided_partition(path: Path, month: str) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=NEEDED_COLUMNS)
    pf = pq.ParquetFile(path)
    parts = []
    offset = 0
    for batch in pf.iter_batches(batch_size=BATCH_SIZE, columns=NEEDED_COLUMNS):
        df = batch.to_pandas()
        if df.empty:
            continue
        keep = (pd.RangeIndex(offset, offset + len(df)) % SAMPLE_STRIDE) == 0
        sample = df.loc[keep].copy()
        sample = sample[sample["trade_date"].astype(str).str.startswith(month)]
        if not sample.empty:
            parts.append(sample)
        offset += len(df)
    return pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=NEEDED_COLUMNS)


def build_tick_features(raw: pd.DataFrame) -> pd.DataFrame:
    if raw.empty:
        return raw
    out = raw.sort_values(["trade_date", "symbol", "exchange_timestamp_ms"]).copy()
    bid_l25 = out[["buy_2_quantity", "buy_3_quantity", "buy_4_quantity", "buy_5_quantity"]].sum(axis=1)
    ask_l25 = out[["sell_2_quantity", "sell_3_quantity", "sell_4_quantity", "sell_5_quantity"]].sum(axis=1)
    out["mid_price"] = (out["buy_1_price"] + out["sell_1_price"]) / 2.0
    out["l1_imbalance"] = (out["buy_1_quantity"] - out["sell_1_quantity"]) / (out["buy_1_quantity"] + out["sell_1_quantity"] + 1.0)
    out["l25_imbalance"] = (bid_l25 - ask_l25) / (bid_l25 + ask_l25 + 1.0)
    out["spread_bps"] = ((out["sell_1_price"] - out["buy_1_price"]) / out["mid_price"] * 10_000.0).fillna(0.0)
    return out.reset_index(drop=True)


def daily_metrics(features: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (trade_date, symbol), grp in features.groupby(["trade_date", "symbol"], sort=False):
        g = grp.reset_index(drop=True)
        if len(g) <= EVENT_INDEX + HORIZON_TICKS + 1:
            continue
        entry_i = EVENT_INDEX + 1
        start_mid = float(g.loc[0, "mid_price"])
        event_mid = float(g.loc[EVENT_INDEX, "mid_price"])
        rows.append(
            {
                "trade_date": str(trade_date),
                "symbol": str(symbol),
                "row_count": len(g),
                "entry_row": entry_i,
                "source_ret_bps": ((event_mid - start_mid) / start_mid * 10_000.0) if start_mid else 0.0,
                "event_l1_imbalance": float(g.loc[EVENT_INDEX, "l1_imbalance"]),
                "event_l25_imbalance": float(g.loc[EVENT_INDEX, "l25_imbalance"]),
                "event_spread_bps": float(g.loc[EVENT_INDEX, "spread_bps"]),
            }
        )
    return pd.DataFrame(rows)


def target_proxy(symbol: str) -> str:
    if symbol in BANK_TARGETS:
        return "BANKBEES"
    if symbol in IT_TARGETS:
        return "ITBEES"
    return "NIFTYBEES"


def build_events(metrics: pd.DataFrame, scenario_id: str, *, side_flip: bool = False, source_shift: int = 0, target_only: bool = False, etf_l1_only: bool = False) -> pd.DataFrame:
    rows = []
    if metrics.empty:
        return pd.DataFrame()
    keyed = {(r["trade_date"], r["symbol"]): r for r in metrics.to_dict("records")}
    dates = sorted(metrics["trade_date"].astype(str).unique().tolist())
    date_index = {d: i for i, d in enumerate(dates)}
    by_index = {i: d for d, i in date_index.items()}
    for target in TARGET_SYMBOLS:
        proxy = target_proxy(target)
        for date in dates:
            target_row = keyed.get((date, target))
            if not target_row:
                continue
            proxy_date = by_index.get(date_index[date] + source_shift)
            proxy_row = keyed.get((proxy_date, proxy)) if proxy_date is not None else None
            if target_only:
                raw_score = float(target_row["event_l25_imbalance"])
            elif proxy_row:
                proxy_depth = float(proxy_row["event_l1_imbalance"] if etf_l1_only else proxy_row["event_l25_imbalance"])
                raw_score = float(proxy_row["source_ret_bps"]) / 25.0 + 2.0 * proxy_depth + 0.5 * float(target_row["event_l25_imbalance"])
            else:
                continue
            side_sign = 1 if raw_score > 0 else -1
            # Frozen agreement requirement for the primary and ETF controls.
            if not target_only and raw_score * float(target_row["event_l25_imbalance"]) <= 0:
                continue
            if side_flip:
                side_sign *= -1
            rows.append(
                {
                    "scenario_id": scenario_id,
                    "trade_date": date,
                    "symbol": target,
                    "proxy_symbol": proxy if not target_only else "target_only",
                    "proxy_date": proxy_date if proxy_date is not None else date,
                    "side": "long" if side_sign > 0 else "short",
                    "side_sign": side_sign,
                    "raw_score": raw_score,
                    "target_l25_imbalance": target_row["event_l25_imbalance"],
                    "target_l1_imbalance": target_row["event_l1_imbalance"],
                    "source_shift_days": source_shift,
                    "target_only": int(target_only),
                    "etf_l1_only": int(etf_l1_only),
                    "entry_row": target_row["entry_row"],
                }
            )
    return pd.DataFrame(rows)


def simulate(events: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    if events.empty:
        return pd.DataFrame()
    keyed = {key: grp.reset_index(drop=True) for key, grp in features.groupby(["trade_date", "symbol"], sort=False)}
    rows = []
    for event in events.to_dict("records"):
        g = keyed.get((event["trade_date"], event["symbol"]))
        if g is None:
            continue
        entry_i = int(event["entry_row"])
        if entry_i + 1 >= len(g):
            continue
        entry = float(g.loc[entry_i, "mid_price"])
        side = int(event["side_sign"])
        stop = entry * (1.0 - side * STOP_BPS / 10_000.0)
        target = entry * (1.0 + side * TAKE_PROFIT_BPS / 10_000.0)
        exit_i = min(entry_i + HORIZON_TICKS, len(g) - 1)
        for j in range(entry_i + 1, min(entry_i + HORIZON_TICKS, len(g) - 1) + 1):
            px = float(g.loc[j, "mid_price"])
            if (side > 0 and (px <= stop or px >= target)) or (side < 0 and (px >= stop or px <= target)):
                exit_i = j
                break
        exit_price = float(g.loc[exit_i, "mid_price"])
        qty = max(1, int(ORDER_NOTIONAL_INR // max(entry, 0.01)))
        buy_value = entry * qty if side > 0 else exit_price * qty
        sell_value = exit_price * qty if side > 0 else entry * qty
        gross = (exit_price - entry) * qty * side
        charges = calculate_equity_intraday_nse_charges(
            buy_value_inr=buy_value,
            sell_value_inr=sell_value,
            buy_quantity=qty,
            sell_quantity=qty,
            buy_orders=1,
            sell_orders=1,
        )
        out = dict(event)
        out.update(
            {
                "exit_row": exit_i,
                "entry_price": entry,
                "exit_price": exit_price,
                "quantity": qty,
                "gross_pnl_inr": gross,
                "cost200_inr": charges.total_charges * COST_MULTIPLIER,
                "net_pnl_inr": gross - charges.total_charges * COST_MULTIPLIER,
                "cost_model_version": charges.model_version,
            }
        )
        rows.append(out)
    return pd.DataFrame(rows)


def summarize(ledger: pd.DataFrame, scenario_id: str) -> dict[str, Any]:
    if ledger.empty:
        return {"scenario_id": scenario_id, "completed_round_trips": 0, "trade_dates": 0, "symbols": 0, "positive_date_fraction": 0.0, "gross_pnl_inr": 0.0, "cost200_inr": 0.0, "net_pnl_inr": 0.0, "annualized_return_pct": 0.0, "acceptance_survivor": 0}
    date_pnl = ledger.groupby("trade_date")["net_pnl_inr"].sum()
    dates = int(ledger["trade_date"].nunique())
    net = float(ledger["net_pnl_inr"].sum())
    annualized = (net / INITIAL_CAPITAL_INR) * (252.0 / max(1, dates)) * 100.0
    pos = float((date_pnl > 0).mean()) if len(date_pnl) else 0.0
    survivor = int(len(ledger) >= 30 and dates >= 5 and ledger["symbol"].nunique() >= 3 and pos >= 0.60 and annualized >= 12.0)
    return {"scenario_id": scenario_id, "completed_round_trips": int(len(ledger)), "trade_dates": dates, "symbols": int(ledger["symbol"].nunique()), "positive_date_fraction": pos, "gross_pnl_inr": float(ledger["gross_pnl_inr"].sum()), "cost200_inr": float(ledger["cost200_inr"].sum()), "net_pnl_inr": net, "annualized_return_pct": annualized, "acceptance_survivor": survivor}


def build_gates(phase451: pd.DataFrame, primary: dict[str, Any], controls: pd.DataFrame, files: pd.DataFrame) -> pd.DataFrame:
    cmap = {r["scenario_id"]: r for r in controls.to_dict("records")}
    gates = [
        ("P452_PHASE451_PRECOMMIT_USED", as_int(scalar(phase451, "phase451_execution_allowed_next", 0)) == 1, scalar(phase451, "phase451_execution_allowed_next", 0), 1),
        ("P452_REQUIRED_FILES_PRESENT", int(files["exists"].sum()) == len(files), int(files["exists"].sum()), len(files)),
        ("P452_LOW_TURNOVER_CAP_APPLIED", True, "max_one_event_per_target_date", "applied"),
        ("P452_CROSS_ASSET_SOURCE_USED", True, "NIFTYBEES;BANKBEES;ITBEES", "etf_proxies"),
        ("P452_FULL_DEPTH_L2_L5_PRIMARY", True, "ETF and target l2_l5 pressure used", "levels_2_to_5"),
        ("P452_COMPLETED_ROUND_TRIPS_GE_30", int(primary["completed_round_trips"]) >= 30, primary["completed_round_trips"], ">=30"),
        ("P452_DATE_BREADTH_GE_5", int(primary["trade_dates"]) >= 5, primary["trade_dates"], ">=5"),
        ("P452_SYMBOL_BREADTH_GE_3", int(primary["symbols"]) >= 3, primary["symbols"], ">=3"),
        ("P452_POSITIVE_DATE_FRACTION_GE_0_60", float(primary["positive_date_fraction"]) >= 0.60, primary["positive_date_fraction"], ">=0.60"),
        ("P452_ANNUALIZED_GE_12_COST200", float(primary["annualized_return_pct"]) >= 12.0, primary["annualized_return_pct"], ">=12.0"),
        ("P452_TIME_SHIFT_NOT_DOMINANT", float(primary["net_pnl_inr"]) > float(cmap.get(TIME_SHIFT_SCENARIO_ID, {}).get("net_pnl_inr", 0.0)), f"primary={primary['net_pnl_inr']};shift={cmap.get(TIME_SHIFT_SCENARIO_ID, {}).get('net_pnl_inr', '')}", "primary_gt_shift"),
        ("P452_SIDE_FLIP_NOT_DOMINANT", float(primary["net_pnl_inr"]) > float(cmap.get(SIDE_FLIP_SCENARIO_ID, {}).get("net_pnl_inr", 0.0)), f"primary={primary['net_pnl_inr']};side_flip={cmap.get(SIDE_FLIP_SCENARIO_ID, {}).get('net_pnl_inr', '')}", "primary_gt_side_flip"),
        ("P452_TARGET_ONLY_NOT_DOMINANT", float(primary["net_pnl_inr"]) > float(cmap.get(TARGET_ONLY_SCENARIO_ID, {}).get("net_pnl_inr", 0.0)), f"primary={primary['net_pnl_inr']};target_only={cmap.get(TARGET_ONLY_SCENARIO_ID, {}).get('net_pnl_inr', '')}", "primary_gt_target_only"),
        ("P452_ETF_L1_ONLY_NOT_DOMINANT", float(primary["net_pnl_inr"]) > float(cmap.get(ETF_L1_ONLY_SCENARIO_ID, {}).get("net_pnl_inr", 0.0)), f"primary={primary['net_pnl_inr']};etf_l1={cmap.get(ETF_L1_ONLY_SCENARIO_ID, {}).get('net_pnl_inr', '')}", "primary_gt_etf_l1"),
        ("P452_COST200_FIXED_CAPITAL", True, f"cost={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR};notional={ORDER_NOTIONAL_INR}", "cost200_fixed_capital"),
        ("P452_NO_PROMOTION_PAPER_LIVE", True, "promotion=0;paper_live=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(primary: dict[str, Any], gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    survivor = int(hard_pass == hard_rows)
    rows = [
        ("phase452_cross_asset_execution_complete", 1, "Phase452 execution completed"),
        ("phase452_thesis_id", THESIS_ID, "Execution thesis"),
        ("phase452_best_scenario_id", PRIMARY_SCENARIO_ID, "Primary scenario"),
        ("phase452_best_completed_round_trips", primary["completed_round_trips"], "Primary completed round trips"),
        ("phase452_best_trade_dates", primary["trade_dates"], "Primary dates"),
        ("phase452_best_symbols", primary["symbols"], "Primary symbols"),
        ("phase452_best_positive_date_fraction", primary["positive_date_fraction"], "Primary positive-date fraction"),
        ("phase452_best_gross_pnl_inr", primary["gross_pnl_inr"], "Primary gross P&L"),
        ("phase452_best_cost200_inr", primary["cost200_inr"], "Primary Zerodha cost200"),
        ("phase452_best_net_pnl_inr", primary["net_pnl_inr"], "Primary net P&L"),
        ("phase452_best_annualized_return_pct", primary["annualized_return_pct"], "Fixed-capital annualized return"),
        ("phase452_acceptance_survivor", survivor, "Accepted only if every hard gate passes"),
        ("phase452_strategy_promotion_allowed", 0, "No promotion"),
        ("phase452_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase452_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase452_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase452_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase452_next_best_action", NEXT_ACTION, "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, summary: pd.DataFrame, gates: pd.DataFrame, files: pd.DataFrame) -> None:
    lines = [
        "# Phase452 Cross-Asset ETF Pressure Execution",
        "",
        "Phase452 executes the Phase451 frozen cross-asset ETF pressure source with a low-turnover one-event-per-target-date cap.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Scenario Summary",
        "",
        _markdown_table(summary),
        "",
        "## Selected Files",
        "",
        _markdown_table(files),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: no strategy promotion, paper/live acceptance or deployable profitability claim is emitted by Phase452.",
    ]
    (output_dir / "phase452_cross_asset_etf_pressure_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase451_dir: Path = DEFAULT_PHASE451_DIR, dense_root: Path = DEFAULT_DENSE_ROOT, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase451 = read_csv(phase451_dir / "phase451_acceptance_summary.csv")
    contract = read_csv(phase451_dir / "phase451_frozen_phase452_contract.csv")
    if as_int(scalar(phase451, "phase451_execution_allowed_next", 0)) != 1:
        raise ValueError("Phase452 requires Phase451 execution allowance.")
    months = split_list(contract_value(contract, "months", ";".join(MONTHS)))
    symbols = split_list(contract_value(contract, "source_instruments", ";".join(ETF_PROXIES))) + split_list(contract_value(contract, "target_symbols", ";".join(TARGET_SYMBOLS)))
    files = selected_files(dense_root, months, symbols)
    raw_parts = [read_strided_partition(Path(row["path"]), str(row["trade_month"])) for row in files.to_dict("records")]
    raw = pd.concat(raw_parts, ignore_index=True) if raw_parts else pd.DataFrame(columns=NEEDED_COLUMNS)
    features = build_tick_features(raw)
    metrics = daily_metrics(features)
    scenarios = [
        (PRIMARY_SCENARIO_ID, dict()),
        (TIME_SHIFT_SCENARIO_ID, {"source_shift": 1}),
        (SIDE_FLIP_SCENARIO_ID, {"side_flip": True}),
        (TARGET_ONLY_SCENARIO_ID, {"target_only": True}),
        (ETF_L1_ONLY_SCENARIO_ID, {"etf_l1_only": True}),
    ]
    ledgers = []
    summaries = []
    for scenario_id, kwargs in scenarios:
        events = build_events(metrics, scenario_id, **kwargs)
        ledger = simulate(events, features)
        if not ledger.empty:
            ledgers.append(ledger)
        summaries.append(summarize(ledger, scenario_id))
    trade_ledger = pd.concat(ledgers, ignore_index=True) if ledgers else pd.DataFrame()
    summary = pd.DataFrame(summaries)
    primary = summary[summary["scenario_id"].eq(PRIMARY_SCENARIO_ID)].iloc[0].to_dict()
    controls = summary[~summary["scenario_id"].eq(PRIMARY_SCENARIO_ID)].copy()
    gates = build_gates(phase451, primary, controls, files)
    acceptance = build_acceptance(primary, gates)

    files.to_csv(output_dir / "phase452_selected_files.csv", index=False)
    metrics.to_csv(output_dir / "phase452_daily_signal_metrics.csv", index=False)
    trade_ledger.to_csv(output_dir / "phase452_trade_ledger.csv", index=False)
    summary.to_csv(output_dir / "phase452_scenario_summary.csv", index=False)
    controls.to_csv(output_dir / "phase452_control_summary.csv", index=False)
    gates.to_csv(output_dir / "phase452_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase452_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, summary, gates, files)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase452_cross_asset_etf_pressure_execution",
        **reproducibility_fields(
            artifact_id="phase452_cross_asset_etf_pressure_execution",
            generated_utc=generated_utc,
            inputs={"phase451_acceptance_summary": str(phase451_dir / "phase451_acceptance_summary.csv"), "dense_root": str(dense_root)},
            parameters={"thesis_id": THESIS_ID, "months": months, "symbols": symbols, "sample_stride": SAMPLE_STRIDE, "horizon_ticks": HORIZON_TICKS},
            outputs={"acceptance_summary": str(output_dir / "phase452_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase452_cross_asset_fixed_tick_horizon",
        ),
    }
    (output_dir / "phase452_cross_asset_etf_pressure_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase452 cross-asset ETF pressure execution.")
    parser.add_argument("--phase451-dir", type=Path, default=DEFAULT_PHASE451_DIR)
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase451_dir, args.dense_root, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
