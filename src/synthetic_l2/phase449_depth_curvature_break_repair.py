from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict
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


DEFAULT_PHASE448_DIR = Path("outputs/phase448")
DEFAULT_DENSE_ROOT = Path("raw_synthetic_l2_dense_full_year")
DEFAULT_OUTPUT_DIR = Path("outputs/phase449")

THESIS_ID = "P449_DEPTH_CURVATURE_BREAK_REPAIR_EXECUTION"
PRIMARY_SCENARIO_ID = "P449_depth_curvature_repair_primary"
L1_ONLY_SCENARIO_ID = "P449_depth_curvature_repair_l1_only_ablation"
SIDE_FLIP_SCENARIO_ID = "P449_depth_curvature_repair_side_flip_control"
STATIC_SCENARIO_ID = "P449_depth_curvature_static_snapshot_control"
TIME_SHIFT_SCENARIO_ID = "P449_depth_curvature_time_shift_control"
NEXT_ACTION = "interpret_phase449_depth_curvature_break_repair_no_paper_live"

INITIAL_CAPITAL_INR = 1_000_000.0
ORDER_NOTIONAL_INR = 100_000.0
COST_MULTIPLIER = 2.0
HORIZON_TICKS = 60
STOP_BPS = 10.0
TAKE_PROFIT_BPS = 16.0
MIN_EVENT_SPACING_TICKS = 120
DEFAULT_STRIDE = 768
DEFAULT_MAX_FILES = 36
DEFAULT_BATCH_SIZE = 250_000

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
    if contract.empty:
        return default
    rows = contract.loc[contract["contract_id"].astype(str).eq(key), "contract_value"].astype(str).tolist()
    return rows[0] if rows else default


def parse_partition(path: Path) -> tuple[str, str]:
    text = str(path).replace("\\", "/")
    month = re.search(r"trade_month=([^/]+)", text)
    symbol = re.search(r"symbol=([^/]+)", text)
    return (month.group(1) if month else "", symbol.group(1) if symbol else "")


def select_files(dense_root: Path, max_files: int) -> pd.DataFrame:
    paths = sorted(dense_root.rglob("*.parquet"))
    rows = []
    for path in paths:
        month, symbol = parse_partition(path)
        rows.append({"path": str(path), "trade_month": month, "symbol": symbol})
    frame = pd.DataFrame(rows)
    if frame.empty:
        return frame
    # Deterministic breadth-first selection across months and symbols.
    frame = frame.sort_values(["trade_month", "symbol", "path"]).drop_duplicates(["trade_month", "symbol"], keep="first")
    month_order = sorted(frame["trade_month"].dropna().astype(str).unique().tolist())
    symbol_order = sorted(frame["symbol"].dropna().astype(str).unique().tolist())
    picked: list[dict[str, Any]] = []
    for symbol in symbol_order:
        for month in month_order:
            rows = frame[frame["trade_month"].eq(month) & frame["symbol"].eq(symbol)]
            if rows.empty:
                continue
            picked.append(rows.iloc[0].to_dict())
            if len(picked) >= max_files:
                return pd.DataFrame(picked).reset_index(drop=True)
    selected = pd.DataFrame(picked)
    if len(selected) < max_files:
        selected = pd.concat([selected, frame.loc[~frame["path"].isin(selected["path"])]], ignore_index=True).head(max_files)
    return selected.head(max_files).reset_index(drop=True)


def read_strided_file(path: Path, stride: int, batch_size: int) -> pd.DataFrame:
    pf = pq.ParquetFile(path)
    parts = []
    offset = 0
    for batch in pf.iter_batches(batch_size=batch_size, columns=NEEDED_COLUMNS):
        df = batch.to_pandas()
        if df.empty:
            continue
        keep = (pd.RangeIndex(offset, offset + len(df)) % stride) == 0
        parts.append(df.loc[keep].copy())
        offset += len(df)
    return pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=NEEDED_COLUMNS)


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.sort_values(["trade_date", "symbol", "exchange_timestamp_ms"]).copy()
    bid_l25 = out[["buy_2_quantity", "buy_3_quantity", "buy_4_quantity", "buy_5_quantity"]].sum(axis=1)
    ask_l25 = out[["sell_2_quantity", "sell_3_quantity", "sell_4_quantity", "sell_5_quantity"]].sum(axis=1)
    bid_near = out["buy_2_quantity"] + out["buy_3_quantity"]
    bid_far = out["buy_4_quantity"] + out["buy_5_quantity"]
    ask_near = out["sell_2_quantity"] + out["sell_3_quantity"]
    ask_far = out["sell_4_quantity"] + out["sell_5_quantity"]
    out["mid_price"] = (out["buy_1_price"] + out["sell_1_price"]) / 2.0
    out["spread_bps"] = ((out["sell_1_price"] - out["buy_1_price"]) / out["mid_price"] * 10_000.0).replace([float("inf"), -float("inf")], 0.0)
    out["l1_imbalance"] = (out["buy_1_quantity"] - out["sell_1_quantity"]) / (out["buy_1_quantity"] + out["sell_1_quantity"] + 1.0)
    out["l25_imbalance"] = (bid_l25 - ask_l25) / (bid_l25 + ask_l25 + 1.0)
    out["bid_curvature"] = (bid_near - bid_far) / (bid_l25 + 1.0)
    out["ask_curvature"] = (ask_near - ask_far) / (ask_l25 + 1.0)
    grp = out.groupby(["trade_date", "symbol"], sort=False)
    out["bid_curvature_repair"] = grp["bid_curvature"].diff(3).fillna(0.0)
    out["ask_curvature_repair"] = grp["ask_curvature"].diff(3).fillna(0.0)
    out["dynamic_curvature_score"] = (out["bid_curvature_repair"] - out["ask_curvature_repair"]) + 0.5 * out["l25_imbalance"]
    out["static_curvature_score"] = (out["bid_curvature"] - out["ask_curvature"]) + 0.5 * out["l25_imbalance"]
    out["l1_only_score"] = out["l1_imbalance"]
    return out.reset_index(drop=True)


def pick_events(features: pd.DataFrame, scenario_id: str, score_column: str, *, side_flip: bool = False, time_shift: bool = False) -> pd.DataFrame:
    if features.empty:
        return pd.DataFrame()
    rows = []
    for (_, _), grp in features.groupby(["trade_date", "symbol"], sort=False):
        g = grp.reset_index(drop=True).copy()
        if len(g) <= HORIZON_TICKS + 5:
            continue
        score = g[score_column].shift(5).fillna(0.0) if time_shift else g[score_column]
        work = g.assign(abs_score=score.abs(), signed_score=score).iloc[5 : len(g) - HORIZON_TICKS].copy()
        work = work.sort_values("abs_score", ascending=False)
        used: list[int] = []
        for idx, row in work.iterrows():
            pos = int(idx)
            if any(abs(pos - u) < MIN_EVENT_SPACING_TICKS for u in used):
                continue
            signed = float(row["signed_score"])
            if signed == 0:
                continue
            side_sign = 1 if signed > 0 else -1
            if side_flip:
                side_sign *= -1
            used.append(pos)
            rows.append(
                {
                    "scenario_id": scenario_id,
                    "trade_date": row["trade_date"],
                    "exchange": row["exchange"],
                    "symbol": row["symbol"],
                    "event_row": pos,
                    "side": "long" if side_sign > 0 else "short",
                    "side_sign": side_sign,
                    "score_column": score_column,
                    "signed_score": signed,
                    "abs_score": abs(signed),
                    "l1_imbalance": row["l1_imbalance"],
                    "l25_imbalance": row["l25_imbalance"],
                    "bid_curvature": row["bid_curvature"],
                    "ask_curvature": row["ask_curvature"],
                    "bid_curvature_repair": row["bid_curvature_repair"],
                    "ask_curvature_repair": row["ask_curvature_repair"],
                    "entry_mid": row["mid_price"],
                    "entry_spread_bps": row["spread_bps"],
                }
            )
            if len(used) >= 2:
                break
    return pd.DataFrame(rows)


def simulate_trades(events: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    if events.empty:
        return pd.DataFrame()
    ledgers = []
    keyed = {key: grp.reset_index(drop=True) for key, grp in features.groupby(["trade_date", "symbol"], sort=False)}
    for row in events.to_dict("records"):
        g = keyed.get((row["trade_date"], row["symbol"]))
        if g is None:
            continue
        i = int(row["event_row"])
        if i + 1 >= len(g):
            continue
        entry = float(g.loc[i + 1, "mid_price"])
        side = int(row["side_sign"])
        stop = entry * (1.0 - side * STOP_BPS / 10_000.0)
        target = entry * (1.0 + side * TAKE_PROFIT_BPS / 10_000.0)
        exit_idx = min(i + HORIZON_TICKS, len(g) - 1)
        for j in range(i + 2, min(i + HORIZON_TICKS, len(g) - 1) + 1):
            px = float(g.loc[j, "mid_price"])
            if (side > 0 and (px <= stop or px >= target)) or (side < 0 and (px >= stop or px <= target)):
                exit_idx = j
                break
        exit_price = float(g.loc[exit_idx, "mid_price"])
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
        cost = charges.total_charges * COST_MULTIPLIER
        out = dict(row)
        out.update(
            {
                "entry_row": i + 1,
                "exit_row": exit_idx,
                "entry_price": entry,
                "exit_price": exit_price,
                "quantity": qty,
                "gross_pnl_inr": gross,
                "cost200_inr": cost,
                "net_pnl_inr": gross - cost,
                "cost_model_version": charges.model_version,
            }
        )
        ledgers.append(out)
    return pd.DataFrame(ledgers)


def summarize(ledger: pd.DataFrame, scenario_id: str) -> dict[str, Any]:
    if ledger.empty:
        return {
            "scenario_id": scenario_id,
            "completed_round_trips": 0,
            "trade_dates": 0,
            "symbols": 0,
            "positive_date_fraction": 0.0,
            "gross_pnl_inr": 0.0,
            "cost200_inr": 0.0,
            "net_pnl_inr": 0.0,
            "annualized_return_pct": 0.0,
            "acceptance_survivor": 0,
        }
    date_pnl = ledger.groupby("trade_date")["net_pnl_inr"].sum()
    dates = int(ledger["trade_date"].nunique())
    net = float(ledger["net_pnl_inr"].sum())
    annualized = (net / INITIAL_CAPITAL_INR) * (252.0 / max(1, dates)) * 100.0
    positive_date_fraction = float((date_pnl > 0).mean()) if len(date_pnl) else 0.0
    survivor = int(len(ledger) >= 30 and dates >= 5 and ledger["symbol"].nunique() >= 3 and positive_date_fraction >= 0.60 and annualized >= 12.0)
    return {
        "scenario_id": scenario_id,
        "completed_round_trips": int(len(ledger)),
        "trade_dates": dates,
        "symbols": int(ledger["symbol"].nunique()),
        "positive_date_fraction": positive_date_fraction,
        "gross_pnl_inr": float(ledger["gross_pnl_inr"].sum()),
        "cost200_inr": float(ledger["cost200_inr"].sum()),
        "net_pnl_inr": net,
        "annualized_return_pct": annualized,
        "acceptance_survivor": survivor,
    }


def build_gates(phase448: pd.DataFrame, primary: dict[str, Any], controls: pd.DataFrame, selected_files: pd.DataFrame) -> pd.DataFrame:
    control_map = {str(r["scenario_id"]): r for r in controls.to_dict("records")}
    l1 = control_map.get(L1_ONLY_SCENARIO_ID, {})
    side = control_map.get(SIDE_FLIP_SCENARIO_ID, {})
    static = control_map.get(STATIC_SCENARIO_ID, {})
    shifted = control_map.get(TIME_SHIFT_SCENARIO_ID, {})
    gates = [
        ("P449_PHASE448_PRECOMMIT_USED", as_int(scalar(phase448, "phase448_execution_allowed_next", 0)) == 1, scalar(phase448, "phase448_execution_allowed_next", 0), 1),
        ("P449_RAW_FILES_SCANNED", len(selected_files) > 0, len(selected_files), ">0"),
        ("P449_FULL_DEPTH_L2_L5_PRIMARY", True, "dynamic_curvature_score uses buy/sell quantities at levels 2-5", "levels_2_to_5"),
        ("P449_COMPLETED_ROUND_TRIPS_GE_30", int(primary["completed_round_trips"]) >= 30, primary["completed_round_trips"], ">=30"),
        ("P449_DATE_BREADTH_GE_5", int(primary["trade_dates"]) >= 5, primary["trade_dates"], ">=5"),
        ("P449_SYMBOL_BREADTH_GE_3", int(primary["symbols"]) >= 3, primary["symbols"], ">=3"),
        ("P449_POSITIVE_DATE_FRACTION_GE_0_60", float(primary["positive_date_fraction"]) >= 0.60, primary["positive_date_fraction"], ">=0.60"),
        ("P449_ANNUALIZED_GE_12_COST200", float(primary["annualized_return_pct"]) >= 12.0, primary["annualized_return_pct"], ">=12.0"),
        ("P449_L1_ONLY_NOT_DOMINANT", float(primary["net_pnl_inr"]) > float(l1.get("net_pnl_inr", 0.0)), f"primary={primary['net_pnl_inr']};l1={l1.get('net_pnl_inr', '')}", "primary_gt_l1"),
        ("P449_SIDE_FLIP_NOT_DOMINANT", float(primary["net_pnl_inr"]) > float(side.get("net_pnl_inr", 0.0)), f"primary={primary['net_pnl_inr']};side_flip={side.get('net_pnl_inr', '')}", "primary_gt_side_flip"),
        ("P449_STATIC_SNAPSHOT_NOT_DOMINANT", float(primary["net_pnl_inr"]) > float(static.get("net_pnl_inr", 0.0)), f"primary={primary['net_pnl_inr']};static={static.get('net_pnl_inr', '')}", "primary_gt_static"),
        ("P449_TIME_SHIFT_NOT_DOMINANT", float(primary["net_pnl_inr"]) > float(shifted.get("net_pnl_inr", 0.0)), f"primary={primary['net_pnl_inr']};shift={shifted.get('net_pnl_inr', '')}", "primary_gt_shift"),
        ("P449_COST200_FIXED_CAPITAL", True, f"cost={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR};notional={ORDER_NOTIONAL_INR}", "cost200_fixed_capital"),
        ("P449_NO_PROMOTION_PAPER_LIVE", True, "promotion=0;paper_live=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(primary: dict[str, Any], gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    survivor = int(hard_pass == hard_rows)
    rows = [
        ("phase449_depth_curvature_execution_complete", 1, "Phase449 execution completed"),
        ("phase449_thesis_id", THESIS_ID, "Execution thesis"),
        ("phase449_best_scenario_id", PRIMARY_SCENARIO_ID, "Primary scenario"),
        ("phase449_best_completed_round_trips", primary["completed_round_trips"], "Primary completed round trips"),
        ("phase449_best_trade_dates", primary["trade_dates"], "Primary dates"),
        ("phase449_best_symbols", primary["symbols"], "Primary symbols"),
        ("phase449_best_positive_date_fraction", primary["positive_date_fraction"], "Primary positive-date fraction"),
        ("phase449_best_gross_pnl_inr", primary["gross_pnl_inr"], "Primary gross P&L"),
        ("phase449_best_cost200_inr", primary["cost200_inr"], "Primary Zerodha cost200"),
        ("phase449_best_net_pnl_inr", primary["net_pnl_inr"], "Primary net P&L"),
        ("phase449_best_annualized_return_pct", primary["annualized_return_pct"], "Fixed-capital annualized return"),
        ("phase449_acceptance_survivor", survivor, "Accepted only if every hard gate passes"),
        ("phase449_strategy_promotion_allowed", 0, "No promotion"),
        ("phase449_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase449_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase449_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase449_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase449_next_best_action", NEXT_ACTION, "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, scenario_summary: pd.DataFrame, gates: pd.DataFrame, selected_files: pd.DataFrame) -> None:
    lines = [
        "# Phase449 Depth-Curvature Break/Repair Execution",
        "",
        "Phase449 executes the Phase448 frozen depth-curvature source on deterministic strided raw dense L1-L5 Parquet shards.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Scenario Summary",
        "",
        _markdown_table(scenario_summary),
        "",
        "## Selected Files",
        "",
        _markdown_table(selected_files),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: no paper/live acceptance, strategy promotion or deployable profitability claim is emitted by Phase449.",
    ]
    (output_dir / "phase449_depth_curvature_break_repair_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase448_dir: Path = DEFAULT_PHASE448_DIR, dense_root: Path = DEFAULT_DENSE_ROOT, output_dir: Path = DEFAULT_OUTPUT_DIR, max_files: int = DEFAULT_MAX_FILES, stride: int = DEFAULT_STRIDE, batch_size: int = DEFAULT_BATCH_SIZE) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase448 = read_csv(phase448_dir / "phase448_acceptance_summary.csv")
    if as_int(scalar(phase448, "phase448_execution_allowed_next", 0)) != 1:
        raise ValueError("Phase449 requires Phase448 execution allowance.")
    selected_files = select_files(dense_root, max_files)
    samples = []
    for row in selected_files.to_dict("records"):
        sample = read_strided_file(Path(row["path"]), stride=stride, batch_size=batch_size)
        samples.append(sample)
    raw = pd.concat(samples, ignore_index=True) if samples else pd.DataFrame(columns=NEEDED_COLUMNS)
    features = build_features(raw)
    scenarios = [
        (PRIMARY_SCENARIO_ID, "dynamic_curvature_score", False, False),
        (L1_ONLY_SCENARIO_ID, "l1_only_score", False, False),
        (SIDE_FLIP_SCENARIO_ID, "dynamic_curvature_score", True, False),
        (STATIC_SCENARIO_ID, "static_curvature_score", False, False),
        (TIME_SHIFT_SCENARIO_ID, "dynamic_curvature_score", False, True),
    ]
    ledgers = []
    summaries = []
    for scenario_id, score_col, side_flip, time_shift in scenarios:
        events = pick_events(features, scenario_id, score_col, side_flip=side_flip, time_shift=time_shift)
        ledger = simulate_trades(events, features)
        if not ledger.empty:
            ledgers.append(ledger)
        summaries.append(summarize(ledger, scenario_id))
    trade_ledger = pd.concat(ledgers, ignore_index=True) if ledgers else pd.DataFrame()
    scenario_summary = pd.DataFrame(summaries)
    primary = scenario_summary[scenario_summary["scenario_id"].eq(PRIMARY_SCENARIO_ID)].iloc[0].to_dict()
    controls = scenario_summary[~scenario_summary["scenario_id"].eq(PRIMARY_SCENARIO_ID)].copy()
    gates = build_gates(phase448, primary, controls, selected_files)
    acceptance = build_acceptance(primary, gates)

    selected_files.to_csv(output_dir / "phase449_selected_files.csv", index=False)
    features.head(5000).to_csv(output_dir / "phase449_feature_sample.csv", index=False)
    trade_ledger.to_csv(output_dir / "phase449_trade_ledger.csv", index=False)
    scenario_summary.to_csv(output_dir / "phase449_scenario_summary.csv", index=False)
    controls.to_csv(output_dir / "phase449_control_summary.csv", index=False)
    gates.to_csv(output_dir / "phase449_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase449_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, scenario_summary, gates, selected_files)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase449_depth_curvature_break_repair_execution",
        **reproducibility_fields(
            artifact_id="phase449_depth_curvature_break_repair_execution",
            generated_utc=generated_utc,
            inputs={"phase448_acceptance_summary": str(phase448_dir / "phase448_acceptance_summary.csv"), "dense_root": str(dense_root)},
            parameters={"thesis_id": THESIS_ID, "max_files": max_files, "stride": stride, "batch_size": batch_size, "horizon_ticks": HORIZON_TICKS},
            outputs={"acceptance_summary": str(output_dir / "phase449_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase449_fixed_tick_horizon",
        ),
    }
    (output_dir / "phase449_depth_curvature_break_repair_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase449 depth-curvature break/repair execution.")
    parser.add_argument("--phase448-dir", type=Path, default=DEFAULT_PHASE448_DIR)
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-files", type=int, default=DEFAULT_MAX_FILES)
    parser.add_argument("--stride", type=int, default=DEFAULT_STRIDE)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    args = parser.parse_args()
    acceptance = run(args.phase448_dir, args.dense_root, args.output_dir, args.max_files, args.stride, args.batch_size)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
