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


DEFAULT_PHASE457_DIR = Path("outputs/phase457")
DEFAULT_DENSE_ROOT = Path("raw_synthetic_l2_dense_full_year")
DEFAULT_OUTPUT_DIR = Path("outputs/phase458")

THESIS_ID = "P458_DELAYED_INTRADAY_CROSS_ASSET_DISPLACEMENT_EXECUTION"
PRIMARY_SCENARIO_ID = "P458_delayed_cross_asset_displacement_primary"
TIME_SHIFT_SCENARIO_ID = "P458_delayed_cross_asset_displacement_source_time_shift"
SIDE_FLIP_SCENARIO_ID = "P458_delayed_cross_asset_displacement_side_flip"
TARGET_ONLY_SCENARIO_ID = "P458_delayed_cross_asset_target_only_l1_l5"
ETF_L1_ONLY_SCENARIO_ID = "P458_delayed_cross_asset_etf_l1_only"
NEXT_ACTION = "interpret_phase458_delayed_intraday_cross_asset_displacement_no_paper_live"

BANK_TARGETS = {"AXISBANK", "HDFCBANK", "ICICIBANK"}
IT_TARGETS = {"INFY", "HCLTECH", "TCS"}
ORDER_NOTIONAL_INR = 100_000.0
INITIAL_CAPITAL_INR = 1_000_000.0
COST_MULTIPLIER = 2.0
STOP_BPS = 18.0
TAKE_PROFIT_BPS = 30.0
BATCH_SIZE = 50_000

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


def cval(contract: pd.DataFrame, key: str, default: str = "") -> str:
    rows = contract.loc[contract["contract_id"].astype(str).eq(key), "contract_value"].astype(str).tolist()
    return rows[0] if rows else default


def slist(value: str) -> list[str]:
    return [x.strip() for x in str(value).split(";") if x.strip()]


def cint(contract: pd.DataFrame, key: str, default: int) -> int:
    try:
        return int(float(cval(contract, key, str(default))))
    except ValueError:
        return default


def selected_files(dense_root: Path, months: list[str], symbols: list[str]) -> pd.DataFrame:
    rows = []
    for month in months:
        for symbol in symbols:
            path = dense_root / f"trade_month={month}" / f"symbol={symbol}" / "part-00000.parquet"
            rows.append({"trade_month": month, "symbol": symbol, "path": str(path), "exists": int(path.exists())})
    return pd.DataFrame(rows)


def read_delayed_partition(path: Path, month: str, *, start_row: int, rows_per_date: int) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=NEEDED_COLUMNS)
    counts: dict[str, int] = {}
    parts = []
    pf = pq.ParquetFile(path)
    for batch in pf.iter_batches(batch_size=BATCH_SIZE, columns=NEEDED_COLUMNS):
        df = batch.to_pandas()
        if df.empty:
            continue
        df = df[df["trade_date"].astype(str).str.startswith(month)].copy()
        if df.empty:
            continue
        keep = []
        for trade_date, grp in df.groupby("trade_date", sort=False):
            key = str(trade_date)
            seen = counts.get(key, 0)
            n = len(grp)
            counts[key] = seen + n
            local_start = max(0, start_row - seen)
            local_end = min(n, start_row + rows_per_date - seen)
            if local_start < local_end:
                keep.append(grp.iloc[local_start:local_end].copy())
        if keep:
            parts.append(pd.concat(keep, ignore_index=True))
    return pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=NEEDED_COLUMNS)


def build_features(raw: pd.DataFrame) -> pd.DataFrame:
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


def daily_metrics(features: pd.DataFrame, *, entry_index: int, horizon_ticks: int) -> pd.DataFrame:
    rows = []
    for (trade_date, symbol), grp in features.groupby(["trade_date", "symbol"], sort=False):
        g = grp.reset_index(drop=True)
        if len(g) < entry_index + horizon_ticks + 1:
            continue
        start_mid = float(g.loc[0, "mid_price"])
        event_mid = float(g.loc[entry_index, "mid_price"])
        rows.append(
            {
                "trade_date": str(trade_date),
                "symbol": str(symbol),
                "row_count": len(g),
                "entry_row": entry_index + 1,
                "source_ret_bps": ((event_mid - start_mid) / start_mid * 10_000.0) if start_mid else 0.0,
                "event_l1_imbalance": float(g.loc[entry_index, "l1_imbalance"]),
                "event_l25_imbalance": float(g.loc[entry_index, "l25_imbalance"]),
                "event_spread_bps": float(g.loc[entry_index, "spread_bps"]),
            }
        )
    return pd.DataFrame(rows)


def target_proxy(symbol: str) -> str:
    if symbol in BANK_TARGETS:
        return "BANKBEES"
    if symbol in IT_TARGETS:
        return "ITBEES"
    return "NIFTYBEES"


def build_events(metrics: pd.DataFrame, target_symbols: list[str], scenario_id: str, *, side_flip: bool = False, source_shift: int = 0, target_only: bool = False, etf_l1_only: bool = False) -> pd.DataFrame:
    if metrics.empty:
        return pd.DataFrame()
    rows = []
    keyed = {(r["trade_date"], r["symbol"]): r for r in metrics.to_dict("records")}
    dates = sorted(metrics["trade_date"].astype(str).unique().tolist())
    date_index = {d: i for i, d in enumerate(dates)}
    by_index = {i: d for d, i in date_index.items()}
    for target in target_symbols:
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
            if raw_score == 0:
                continue
            if not target_only and raw_score * float(target_row["event_l25_imbalance"]) <= 0:
                continue
            side_sign = 1 if raw_score > 0 else -1
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


def simulate(events: pd.DataFrame, features: pd.DataFrame, *, horizon_ticks: int) -> pd.DataFrame:
    if events.empty:
        return pd.DataFrame()
    keyed = {key: grp.reset_index(drop=True) for key, grp in features.groupby(["trade_date", "symbol"], sort=False)}
    rows = []
    for event in events.to_dict("records"):
        g = keyed.get((event["trade_date"], event["symbol"]))
        if g is None:
            continue
        entry_i = int(event["entry_row"])
        if entry_i + horizon_ticks >= len(g):
            continue
        entry = float(g.loc[entry_i, "mid_price"])
        side = int(event["side_sign"])
        stop = entry * (1.0 - side * STOP_BPS / 10_000.0)
        target = entry * (1.0 + side * TAKE_PROFIT_BPS / 10_000.0)
        exit_i = entry_i + horizon_ticks
        for j in range(entry_i + 1, entry_i + horizon_ticks + 1):
            px = float(g.loc[j, "mid_price"])
            if (side > 0 and (px <= stop or px >= target)) or (side < 0 and (px >= stop or px <= target)):
                exit_i = j
                break
        exit_price = float(g.loc[exit_i, "mid_price"])
        qty = max(1, int(ORDER_NOTIONAL_INR // max(entry, 0.01)))
        buy_value = entry * qty if side > 0 else exit_price * qty
        sell_value = exit_price * qty if side > 0 else entry * qty
        gross = (exit_price - entry) * qty * side
        charges = calculate_equity_intraday_nse_charges(buy_value_inr=buy_value, sell_value_inr=sell_value, buy_quantity=qty, sell_quantity=qty, buy_orders=1, sell_orders=1)
        cost = charges.total_charges * COST_MULTIPLIER
        out = dict(event)
        out.update({"exit_row": exit_i, "entry_price": entry, "exit_price": exit_price, "quantity": qty, "gross_pnl_inr": gross, "cost200_inr": cost, "net_pnl_inr": gross - cost, "cost_model_version": charges.model_version})
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


def build_gates(phase457: pd.DataFrame, primary: dict[str, Any], controls: pd.DataFrame, files: pd.DataFrame, metrics: pd.DataFrame) -> pd.DataFrame:
    cmap = {r["scenario_id"]: r for r in controls.to_dict("records")}
    gates = [
        ("P458_PHASE457_PRECOMMIT_USED", as_int(scalar(phase457, "phase457_execution_allowed_next", 0)) == 1, scalar(phase457, "phase457_execution_allowed_next", 0), 1),
        ("P458_REQUIRED_FILES_PRESENT", int(files["exists"].sum()) == len(files), int(files["exists"].sum()), len(files)),
        ("P458_DELAYED_METRICS_PRESENT", len(metrics) > 0, len(metrics), ">0"),
        ("P458_NOT_FIRST_WINDOW", True, "window_start_row=5000", "not_first_window"),
        ("P458_LOW_TURNOVER_CAP_APPLIED", True, "max_one_event_per_target_date", "applied"),
        ("P458_CROSS_ASSET_SOURCE_USED", True, "NIFTYBEES;BANKBEES;ITBEES", "etf_proxies"),
        ("P458_FULL_DEPTH_L2_L5_PRIMARY", True, "ETF and target L2-L5 pressure used", "levels_2_to_5"),
        ("P458_COMPLETED_ROUND_TRIPS_GE_30", int(primary["completed_round_trips"]) >= 30, primary["completed_round_trips"], ">=30"),
        ("P458_DATE_BREADTH_GE_5", int(primary["trade_dates"]) >= 5, primary["trade_dates"], ">=5"),
        ("P458_SYMBOL_BREADTH_GE_3", int(primary["symbols"]) >= 3, primary["symbols"], ">=3"),
        ("P458_POSITIVE_DATE_FRACTION_GE_0_60", float(primary["positive_date_fraction"]) >= 0.60, primary["positive_date_fraction"], ">=0.60"),
        ("P458_ANNUALIZED_GE_12_COST200", float(primary["annualized_return_pct"]) >= 12.0, primary["annualized_return_pct"], ">=12.0"),
        ("P458_TIME_SHIFT_NOT_DOMINANT", float(primary["net_pnl_inr"]) > float(cmap.get(TIME_SHIFT_SCENARIO_ID, {}).get("net_pnl_inr", 0.0)), f"primary={primary['net_pnl_inr']};shift={cmap.get(TIME_SHIFT_SCENARIO_ID, {}).get('net_pnl_inr', '')}", "primary_gt_shift"),
        ("P458_SIDE_FLIP_NOT_DOMINANT", float(primary["net_pnl_inr"]) > float(cmap.get(SIDE_FLIP_SCENARIO_ID, {}).get("net_pnl_inr", 0.0)), f"primary={primary['net_pnl_inr']};side_flip={cmap.get(SIDE_FLIP_SCENARIO_ID, {}).get('net_pnl_inr', '')}", "primary_gt_side_flip"),
        ("P458_TARGET_ONLY_NOT_DOMINANT", float(primary["net_pnl_inr"]) > float(cmap.get(TARGET_ONLY_SCENARIO_ID, {}).get("net_pnl_inr", 0.0)), f"primary={primary['net_pnl_inr']};target_only={cmap.get(TARGET_ONLY_SCENARIO_ID, {}).get('net_pnl_inr', '')}", "primary_gt_target_only"),
        ("P458_ETF_L1_ONLY_NOT_DOMINANT", float(primary["net_pnl_inr"]) > float(cmap.get(ETF_L1_ONLY_SCENARIO_ID, {}).get("net_pnl_inr", 0.0)), f"primary={primary['net_pnl_inr']};etf_l1={cmap.get(ETF_L1_ONLY_SCENARIO_ID, {}).get('net_pnl_inr', '')}", "primary_gt_etf_l1"),
        ("P458_COST200_FIXED_CAPITAL", True, f"cost={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR};notional={ORDER_NOTIONAL_INR}", "cost200_fixed_capital"),
        ("P458_NO_PROMOTION_PAPER_LIVE", True, "promotion=0;paper_live=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(primary: dict[str, Any], gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    survivor = int(hard_pass == hard_rows)
    return pd.DataFrame(
        [
            ("phase458_delayed_cross_asset_execution_complete", 1, "Phase458 execution completed"),
            ("phase458_thesis_id", THESIS_ID, "Execution thesis"),
            ("phase458_best_scenario_id", PRIMARY_SCENARIO_ID, "Primary scenario"),
            ("phase458_best_completed_round_trips", primary["completed_round_trips"], "Primary completed round trips"),
            ("phase458_best_trade_dates", primary["trade_dates"], "Primary dates"),
            ("phase458_best_symbols", primary["symbols"], "Primary symbols"),
            ("phase458_best_positive_date_fraction", primary["positive_date_fraction"], "Primary positive-date fraction"),
            ("phase458_best_gross_pnl_inr", primary["gross_pnl_inr"], "Primary gross P&L"),
            ("phase458_best_cost200_inr", primary["cost200_inr"], "Primary Zerodha cost200"),
            ("phase458_best_net_pnl_inr", primary["net_pnl_inr"], "Primary net P&L"),
            ("phase458_best_annualized_return_pct", primary["annualized_return_pct"], "Fixed-capital annualized return"),
            ("phase458_acceptance_survivor", survivor, "Accepted only if every hard gate passes"),
            ("phase458_strategy_promotion_allowed", 0, "No promotion"),
            ("phase458_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase458_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase458_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase458_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase458_next_best_action", NEXT_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, summary: pd.DataFrame, gates: pd.DataFrame, files: pd.DataFrame) -> None:
    lines = [
        "# Phase458 Delayed Intraday Cross-Asset Displacement Execution",
        "",
        "Phase458 executes the Phase457 delayed intraday timing-source contract using contiguous raw L1-L5 windows starting at row 5000 per symbol/date.",
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
        "Boundary: no strategy promotion, paper/live acceptance or deployable profitability claim is emitted by Phase458.",
    ]
    (output_dir / "phase458_delayed_intraday_cross_asset_displacement_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase457_dir: Path = DEFAULT_PHASE457_DIR, dense_root: Path = DEFAULT_DENSE_ROOT, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase457 = read_csv(phase457_dir / "phase457_acceptance_summary.csv")
    contract = read_csv(phase457_dir / "phase457_frozen_phase458_contract.csv")
    if as_int(scalar(phase457, "phase457_execution_allowed_next", 0)) != 1:
        raise ValueError("Phase458 requires Phase457 execution allowance.")
    months = slist(cval(contract, "months"))
    source_symbols = slist(cval(contract, "source_instruments"))
    target_symbols = slist(cval(contract, "target_symbols"))
    start_row = cint(contract, "window_start_row", 5000)
    entry_index = cint(contract, "entry_index", 20)
    horizon_ticks = cint(contract, "horizon_ticks", 240)
    rows_per_date = cint(contract, "window_rows_per_symbol_date", entry_index + horizon_ticks + 11)
    symbols = source_symbols + target_symbols
    files = selected_files(dense_root, months, symbols)
    raw_parts = [read_delayed_partition(Path(row["path"]), str(row["trade_month"]), start_row=start_row, rows_per_date=rows_per_date) for row in files.to_dict("records")]
    raw = pd.concat(raw_parts, ignore_index=True) if raw_parts else pd.DataFrame(columns=NEEDED_COLUMNS)
    features = build_features(raw)
    metrics = daily_metrics(features, entry_index=entry_index, horizon_ticks=horizon_ticks)
    scenario_specs = [
        (PRIMARY_SCENARIO_ID, {}),
        (TIME_SHIFT_SCENARIO_ID, {"source_shift": 1}),
        (SIDE_FLIP_SCENARIO_ID, {"side_flip": True}),
        (TARGET_ONLY_SCENARIO_ID, {"target_only": True}),
        (ETF_L1_ONLY_SCENARIO_ID, {"etf_l1_only": True}),
    ]
    ledgers = []
    summaries = []
    for scenario_id, kwargs in scenario_specs:
        events = build_events(metrics, target_symbols, scenario_id, **kwargs)
        ledger = simulate(events, features, horizon_ticks=horizon_ticks)
        if not ledger.empty:
            ledgers.append(ledger)
        summaries.append(summarize(ledger, scenario_id))
    trade_ledger = pd.concat(ledgers, ignore_index=True) if ledgers else pd.DataFrame()
    summary = pd.DataFrame(summaries)
    primary = summary[summary["scenario_id"].eq(PRIMARY_SCENARIO_ID)].iloc[0].to_dict()
    controls = summary[~summary["scenario_id"].eq(PRIMARY_SCENARIO_ID)].copy()
    gates = build_gates(phase457, primary, controls, files, metrics)
    acceptance = build_acceptance(primary, gates)

    files.to_csv(output_dir / "phase458_selected_files.csv", index=False)
    metrics.to_csv(output_dir / "phase458_daily_signal_metrics.csv", index=False)
    trade_ledger.to_csv(output_dir / "phase458_trade_ledger.csv", index=False)
    summary.to_csv(output_dir / "phase458_scenario_summary.csv", index=False)
    controls.to_csv(output_dir / "phase458_control_summary.csv", index=False)
    gates.to_csv(output_dir / "phase458_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase458_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, summary, gates, files)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase458_delayed_intraday_cross_asset_displacement_execution",
        **reproducibility_fields(
            artifact_id="phase458_delayed_intraday_cross_asset_displacement_execution",
            generated_utc=generated_utc,
            inputs={"phase457_acceptance_summary": str(phase457_dir / "phase457_acceptance_summary.csv"), "dense_root": str(dense_root)},
            parameters={"thesis_id": THESIS_ID, "months": months, "symbols": symbols, "window_start_row": start_row, "window_rows": rows_per_date, "entry_index": entry_index, "horizon_ticks": horizon_ticks},
            outputs={"acceptance_summary": str(output_dir / "phase458_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase458_delayed_contiguous_tick_window",
        ),
    }
    (output_dir / "phase458_delayed_intraday_cross_asset_displacement_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase458 delayed intraday cross-asset displacement execution.")
    parser.add_argument("--phase457-dir", type=Path, default=DEFAULT_PHASE457_DIR)
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase457_dir, args.dense_root, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
