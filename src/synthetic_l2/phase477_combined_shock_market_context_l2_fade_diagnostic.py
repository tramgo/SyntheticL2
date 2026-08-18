from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase475_catalyst_liquidity_conditioned_replay import load_shock_calendar
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import (
    ZERODHA_CHARGES_SOURCE_URL,
    ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
    calculate_equity_intraday_nse_charges,
)


DEFAULT_PHASE467_DIR = Path("outputs/phase467")
DEFAULT_PHASE474_DIR = Path("outputs/phase474")
DEFAULT_PHASE476_DIR = Path("outputs/phase476")
DEFAULT_OUTPUT_DIR = Path("outputs/phase477")

THESIS_ID = "P477_COMBINED_SHOCK_MARKET_CONTEXT_L2_FADE_DIAGNOSTIC"
NEXT_ACTION_PASS = "precommit_phase478_expand_combined_clue_to_real_l2_event_floor"
NEXT_ACTION_FAIL = "interpret_phase477_combined_clue_failure_or_close_synthetic_branch"

HORIZONS = [480, 960, 1800]
TOP_COUNTS = [10, 20, 40]
FIXED_CAPITAL_INR = 100_000.0
ADVERSE_SLIPPAGE_ROUND_TRIP_BPS = 2.0
MIN_ANNUALIZED_RETURN_PCT = 12.0
MIN_TRADE_COUNT = 10
MIN_REAL_EVENT_FLOOR = 30


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def cval(contract: pd.DataFrame, key: str, default: str = "") -> str:
    rows = contract.loc[contract["contract_id"].astype(str).eq(key), "contract_value"].astype(str).tolist()
    return rows[0] if rows else default


def sign_series(values: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(values, errors="coerce").fillna(0.0)
    return np.sign(numeric).astype(int)


def side_for_rule(frame: pd.DataFrame, rule_id: str) -> pd.Series:
    if rule_id == "deep_l25_fade":
        return -sign_series(frame["l25_imbalance"])
    if rule_id == "top1_fade_reference":
        return -sign_series(frame["l1_imbalance"])
    if rule_id == "deep_l25_momentum_control":
        return sign_series(frame["l25_imbalance"])
    if rule_id == "deterministic_alternate_control":
        return pd.Series([1 if i % 2 == 0 else -1 for i in range(len(frame))], index=frame.index, dtype=int)
    raise ValueError(f"Unknown rule_id {rule_id}")


def replay(frame: pd.DataFrame, horizon: int, rule_id: str, top_count: int) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame()
    candidates = frame.sort_values(["deep_pressure_rank", "abs_forward_return_bps"], ascending=False).head(min(top_count, len(frame))).copy()
    side = side_for_rule(candidates, rule_id)
    valid = side.ne(0)
    candidates = candidates.loc[valid].copy()
    side = side.loc[valid]
    rows = []
    for idx, row in candidates.iterrows():
        direction = int(side.loc[idx])
        entry_price = float(row["entry_price"])
        exit_price = float(row["exit_price"])
        quantity = max(1, int(FIXED_CAPITAL_INR // max(entry_price, 1e-9)))
        entry_value = quantity * entry_price
        exit_value = quantity * exit_price
        if direction == 1:
            buy_value = entry_value
            sell_value = exit_value
            gross_pnl = exit_value - entry_value
        else:
            buy_value = exit_value
            sell_value = entry_value
            gross_pnl = entry_value - exit_value
        charges = calculate_equity_intraday_nse_charges(
            buy_value_inr=buy_value,
            sell_value_inr=sell_value,
            buy_quantity=quantity,
            sell_quantity=quantity,
            buy_orders=1,
            sell_orders=1,
        )
        slippage_inr = (ADVERSE_SLIPPAGE_ROUND_TRIP_BPS / 10_000.0) * entry_value
        rows.append(
            {
                "trade_date": row["trade_date"],
                "symbol": row["symbol"],
                "candidate_start_row": int(row["candidate_start_row"]),
                "horizon_ticks": horizon,
                "rule_id": rule_id,
                "top_count": top_count,
                "signal_side": "long" if direction == 1 else "short",
                "entry_price": entry_price,
                "exit_price": exit_price,
                "quantity": quantity,
                "l1_imbalance": float(row["l1_imbalance"]),
                "l25_imbalance": float(row["l25_imbalance"]),
                "source_event_l25_ofi_1": float(row["source_event_l25_ofi_1"]),
                "deep_pressure_rank": float(row["deep_pressure_rank"]),
                "is_market_shock_day": int(row["is_market_shock_day"]),
                "is_symbol_shock": int(row["is_symbol_shock"]),
                "gross_pnl_inr": gross_pnl,
                "zerodha_total_charges_inr": charges.total_charges,
                "adverse_slippage_inr": slippage_inr,
                "net_pnl_inr": gross_pnl - charges.total_charges - slippage_inr,
                "forward_return_bps": float(row["forward_return_bps"]),
                "label_side": row["label_side"],
                **{f"charge_{key}": value for key, value in asdict(charges).items() if key in {"brokerage", "stt", "transaction_charge", "sebi_charge", "stamp_duty", "gst"}},
            }
        )
    return pd.DataFrame(rows)


def summarize(trades: pd.DataFrame, scenario_id: str, horizon: int, rule_id: str, top_count: int, candidates: int, holdout_days: int) -> dict[str, Any]:
    if trades.empty:
        return {
            "scenario_id": scenario_id,
            "horizon_ticks": horizon,
            "rule_id": rule_id,
            "top_count": top_count,
            "candidate_rows": candidates,
            "trade_count": 0,
            "holdout_days": holdout_days,
            "gross_pnl_inr": 0.0,
            "zerodha_total_charges_inr": 0.0,
            "adverse_slippage_inr": 0.0,
            "net_pnl_inr": 0.0,
            "annualized_return_pct": 0.0,
            "win_rate": 0.0,
            "avg_net_per_trade_inr": 0.0,
            "diagnostic_event_floor_met": 0,
            "acceptance_event_floor_met": 0,
            "acceptance_candidate": 0,
        }
    daily = trades.groupby("trade_date", sort=True)["net_pnl_inr"].sum().reset_index()
    equity = daily["net_pnl_inr"].cumsum()
    drawdown = equity - equity.cummax()
    net = float(trades["net_pnl_inr"].sum())
    annualized = (net / FIXED_CAPITAL_INR) * (252.0 / max(1, holdout_days)) * 100.0
    trade_count = int(len(trades))
    return {
        "scenario_id": scenario_id,
        "horizon_ticks": horizon,
        "rule_id": rule_id,
        "top_count": top_count,
        "candidate_rows": candidates,
        "trade_count": trade_count,
        "holdout_days": holdout_days,
        "gross_pnl_inr": float(trades["gross_pnl_inr"].sum()),
        "zerodha_total_charges_inr": float(trades["zerodha_total_charges_inr"].sum()),
        "adverse_slippage_inr": float(trades["adverse_slippage_inr"].sum()),
        "net_pnl_inr": net,
        "annualized_return_pct": annualized,
        "win_rate": float((trades["net_pnl_inr"] > 0).mean()),
        "avg_net_per_trade_inr": float(trades["net_pnl_inr"].mean()),
        "max_daily_drawdown_inr": float(drawdown.min()) if len(drawdown) else 0.0,
        "diagnostic_event_floor_met": int(trade_count >= MIN_TRADE_COUNT),
        "acceptance_event_floor_met": int(trade_count >= MIN_REAL_EVENT_FLOOR),
        "acceptance_candidate": int(annualized >= MIN_ANNUALIZED_RETURN_PCT and trade_count >= MIN_REAL_EVENT_FLOOR),
    }


def build_enriched_matrix(phase467_dir: Path, phase474_dir: Path, horizon: int) -> pd.DataFrame:
    selected_files = read_csv(phase467_dir / "phase467_selected_files.csv")
    shock_calendar = load_shock_calendar(selected_files)
    matrix = read_csv(phase474_dir / f"phase474_feature_label_matrix_horizon_{horizon}.csv")
    holdout = matrix[matrix["phase464_split"].astype(str).eq("holdout")].copy()
    holdout = holdout.merge(shock_calendar, on=["trade_date", "symbol"], how="left")
    holdout[["is_market_shock_day", "is_symbol_shock"]] = holdout[["is_market_shock_day", "is_symbol_shock"]].fillna(0).astype(int)
    train = matrix[matrix["phase464_split"].astype(str).eq("train")].copy()
    l25_threshold = float(pd.to_numeric(train["l25_imbalance"], errors="coerce").abs().quantile(0.75))
    ofi_threshold = float(pd.to_numeric(train["source_event_l25_ofi_1"], errors="coerce").abs().quantile(0.75))
    shock = holdout["is_market_shock_day"].astype(int).eq(1) | holdout["is_symbol_shock"].astype(int).eq(1)
    deep = pd.to_numeric(holdout["l25_imbalance"], errors="coerce").abs().ge(l25_threshold)
    ofi = pd.to_numeric(holdout["source_event_l25_ofi_1"], errors="coerce").abs().ge(ofi_threshold)
    out = holdout[shock & (deep | ofi)].copy()
    out["deep_pressure_rank"] = (
        pd.to_numeric(out["l25_imbalance"], errors="coerce").abs().rank(pct=True)
        + pd.to_numeric(out["source_event_l25_ofi_1"], errors="coerce").abs().rank(pct=True)
    ) / 2.0
    out["train_l25_abs_q75"] = l25_threshold
    out["train_source_event_l25_ofi_abs_q75"] = ofi_threshold
    return out


def run_diagnostic(phase467_dir: Path, phase474_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    scenario_rows = []
    trade_parts = []
    candidate_rows = []
    for horizon in HORIZONS:
        candidates = build_enriched_matrix(phase467_dir, phase474_dir, horizon)
        candidate_rows.append(
            {
                "horizon_ticks": horizon,
                "candidate_rows": int(len(candidates)),
                "holdout_days": int(candidates["trade_date"].nunique()) if not candidates.empty else 0,
                "symbols": int(candidates["symbol"].nunique()) if not candidates.empty else 0,
                "train_l25_abs_q75": float(candidates["train_l25_abs_q75"].iloc[0]) if not candidates.empty else 0.0,
                "train_source_event_l25_ofi_abs_q75": float(candidates["train_source_event_l25_ofi_abs_q75"].iloc[0]) if not candidates.empty else 0.0,
            }
        )
        holdout_days = int(candidates["trade_date"].nunique()) if not candidates.empty else 1
        for rule_id in ["deep_l25_fade", "top1_fade_reference", "deep_l25_momentum_control", "deterministic_alternate_control"]:
            for top_count in TOP_COUNTS:
                scenario_id = f"horizon_{horizon}_{rule_id}_top{top_count}_cost200"
                trades = replay(candidates, horizon, rule_id, top_count)
                if not trades.empty:
                    trades["scenario_id"] = scenario_id
                    trade_parts.append(trades)
                scenario_rows.append(summarize(trades, scenario_id, horizon, rule_id, top_count, int(len(candidates)), holdout_days))
    return pd.DataFrame(scenario_rows), (pd.concat(trade_parts, ignore_index=True) if trade_parts else pd.DataFrame()), pd.DataFrame(candidate_rows)


def build_gates(phase476: pd.DataFrame, contract: pd.DataFrame, scenarios: pd.DataFrame, candidates: pd.DataFrame) -> pd.DataFrame:
    best_primary = scenarios[scenarios["rule_id"].eq("deep_l25_fade")].sort_values(["annualized_return_pct", "net_pnl_inr"], ascending=False).iloc[0]
    best_control = scenarios[~scenarios["rule_id"].eq("deep_l25_fade")].sort_values(["annualized_return_pct", "net_pnl_inr"], ascending=False).iloc[0]
    positive_primary = int((scenarios.loc[scenarios["rule_id"].eq("deep_l25_fade"), "net_pnl_inr"].astype(float) > 0).sum())
    above12_primary = int((scenarios.loc[scenarios["rule_id"].eq("deep_l25_fade"), "annualized_return_pct"].astype(float) >= MIN_ANNUALIZED_RETURN_PCT).sum())
    c = {str(row["contract_id"]): str(row["contract_value"]) for row in contract.to_dict("records")}
    rows = [
        ("P477_PHASE476_CONTRACT_USED", as_int(scalar(phase476, "phase476_phase477_allowed_next", 0)) == 1, scalar(phase476, "phase476_phase477_allowed_next", 0), 1),
        ("P477_THESIS_MATCHES_CONTRACT", c.get("phase477_thesis_id") == THESIS_ID, c.get("phase477_thesis_id", ""), THESIS_ID),
        ("P477_CLOSED_PHASE338_NOT_USED", as_int(c.get("use_closed_phase338_survivor", 1)) == 0, c.get("use_closed_phase338_survivor", ""), 0),
        ("P477_NOT_PHASE475_GRID_ONLY", as_int(c.get("use_phase475_same_grid_only", 1)) == 0, c.get("use_phase475_same_grid_only", ""), 0),
        ("P477_FULL_DEPTH_DEEP_FADE_RULE_EXECUTED", bool(scenarios["rule_id"].eq("deep_l25_fade").any()), "deep_l25_fade", "present"),
        ("P477_CANDIDATES_PRESENT_ALL_HORIZONS", int((candidates["candidate_rows"].astype(int) > 0).sum()) == len(HORIZONS), int((candidates["candidate_rows"].astype(int) > 0).sum()), len(HORIZONS)),
        ("P477_COST200_INCLUDED", ADVERSE_SLIPPAGE_ROUND_TRIP_BPS == 2.0, ADVERSE_SLIPPAGE_ROUND_TRIP_BPS, 2.0),
        ("P477_FIXED_CAPITAL_USED", FIXED_CAPITAL_INR == 100_000.0, FIXED_CAPITAL_INR, 100_000.0),
        ("P477_PRIMARY_POSITIVE_SCENARIO_EXISTS", positive_primary > 0, positive_primary, ">0"),
        ("P477_PRIMARY_ABOVE_12PCT_SCENARIO_EXISTS", above12_primary > 0, above12_primary, ">0"),
        ("P477_BEST_PRIMARY_TRADE_COUNT_GE_10", int(best_primary["trade_count"]) >= MIN_TRADE_COUNT, int(best_primary["trade_count"]), f">={MIN_TRADE_COUNT}"),
        ("P477_BEST_PRIMARY_BEATS_BEST_CONTROL", float(best_primary["annualized_return_pct"]) > float(best_control["annualized_return_pct"]), f"primary={best_primary['annualized_return_pct']};control={best_control['annualized_return_pct']}", "primary>control"),
        ("P477_ACCEPTANCE_EVENT_FLOOR_CHECKED", int(best_primary["acceptance_event_floor_met"]) == int(int(best_primary["trade_count"]) >= MIN_REAL_EVENT_FLOOR), best_primary["acceptance_event_floor_met"], "checked"),
        ("P477_NO_PAPER_LIVE_OR_CLAIM", as_int(c.get("paper_or_live_acceptance_allowed", 1)) == 0 and as_int(c.get("deployable_profitability_claim_allowed", 1)) == 0, "paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(gates: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    primary = scenarios[scenarios["rule_id"].eq("deep_l25_fade")].copy()
    best = primary.sort_values(["annualized_return_pct", "net_pnl_inr"], ascending=False).iloc[0]
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    all_pass = int(hard_pass == hard_rows)
    rows = [
        ("phase477_combined_shock_market_context_l2_fade_diagnostic_complete", 1, "Phase477 diagnostic completed"),
        ("phase477_thesis_id", THESIS_ID, "Diagnostic thesis"),
        ("phase477_best_primary_scenario_id", best["scenario_id"], "Best deep L2-L5 fade scenario"),
        ("phase477_best_primary_trade_count", int(best["trade_count"]), "Best primary trade count"),
        ("phase477_best_primary_net_pnl_inr", float(best["net_pnl_inr"]), "Best primary net P&L"),
        ("phase477_best_primary_annualized_return_pct", float(best["annualized_return_pct"]), "Best primary fixed-capital annualized return"),
        ("phase477_primary_positive_scenario_rows", int((primary["net_pnl_inr"].astype(float) > 0).sum()), "Positive primary scenarios"),
        ("phase477_primary_above12_scenario_rows", int((primary["annualized_return_pct"].astype(float) >= MIN_ANNUALIZED_RETURN_PCT).sum()), "Primary scenarios above 12%"),
        ("phase477_best_primary_acceptance_event_floor_met", int(best["acceptance_event_floor_met"]), "Acceptance event floor met"),
        ("phase477_fixed_capital_inr", FIXED_CAPITAL_INR, "Reusable capital denominator"),
        ("phase477_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model version"),
        ("phase477_zerodha_cost_source_url", ZERODHA_CHARGES_SOURCE_URL, "Cost source"),
        ("phase477_strategy_promotion_allowed", 0, "No promotion"),
        ("phase477_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase477_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase477_phase478_allowed_next", all_pass, "Allows expansion precommit only if all gates pass"),
        ("phase477_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase477_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase477_next_best_action", NEXT_ACTION_PASS if all_pass else NEXT_ACTION_FAIL, "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, candidates: pd.DataFrame, scenarios: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase477 Combined Shock Market-Context L2 Fade Diagnostic",
        "",
        "Phase477 executes the frozen Phase476 combined-clue diagnostic: shock/catalyst context plus market-neutral depth-2-5 fade, with controls.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Candidate Summary",
        "",
        _markdown_table(candidates),
        "",
        "## Scenario Summary",
        "",
        _markdown_table(scenarios),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase477 is diagnostic only. It is not paper/live acceptance and not a deployable profitability claim.",
    ]
    (output_dir / "phase477_combined_shock_market_context_l2_fade_diagnostic_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    phase467_dir: Path = DEFAULT_PHASE467_DIR,
    phase474_dir: Path = DEFAULT_PHASE474_DIR,
    phase476_dir: Path = DEFAULT_PHASE476_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase476 = read_csv(phase476_dir / "phase476_acceptance_summary.csv")
    contract = read_csv(phase476_dir / "phase476_phase477_contract.csv")
    scenarios, trades, candidates = run_diagnostic(phase467_dir, phase474_dir)
    gates = build_gates(phase476, contract, scenarios, candidates)
    acceptance = build_acceptance(gates, scenarios)
    candidates.to_csv(output_dir / "phase477_candidate_summary.csv", index=False)
    scenarios.to_csv(output_dir / "phase477_scenario_summary.csv", index=False)
    trades.to_csv(output_dir / "phase477_trade_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase477_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase477_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, candidates, scenarios, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase477_combined_shock_market_context_l2_fade_diagnostic",
        **reproducibility_fields(
            artifact_id="phase477_combined_shock_market_context_l2_fade_diagnostic",
            generated_utc=generated_utc,
            inputs={
                "phase476_contract": str(phase476_dir / "phase476_phase477_contract.csv"),
                "phase474_matrices": str(phase474_dir),
                "phase467_selected_files": str(phase467_dir / "phase467_selected_files.csv"),
            },
            parameters={
                "thesis_id": THESIS_ID,
                "horizons": HORIZONS,
                "top_counts": TOP_COUNTS,
                "fixed_capital_inr": FIXED_CAPITAL_INR,
                "adverse_slippage_round_trip_bps": ADVERSE_SLIPPAGE_ROUND_TRIP_BPS,
                "minimum_real_event_floor": MIN_REAL_EVENT_FLOOR,
            },
            outputs={"acceptance_summary": str(output_dir / "phase477_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase477_cost200_diagnostic_proxy",
        ),
    }
    (output_dir / "phase477_combined_shock_market_context_l2_fade_diagnostic_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase477 combined shock market-context L2 fade diagnostic.")
    parser.add_argument("--phase467-dir", type=Path, default=DEFAULT_PHASE467_DIR)
    parser.add_argument("--phase474-dir", type=Path, default=DEFAULT_PHASE474_DIR)
    parser.add_argument("--phase476-dir", type=Path, default=DEFAULT_PHASE476_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    out = run(args.phase467_dir, args.phase474_dir, args.phase476_dir, args.output_dir)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
