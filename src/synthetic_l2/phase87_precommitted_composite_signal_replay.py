from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase56_cost_clearing_label_discovery import DEFAULT_ORDER_NOTIONAL_INR
from synthetic_l2.phase61_lower_frequency_candidate_sweep import profile_cost_bps, retail_profile
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase87")
DEFAULT_PHASE83_DIR = Path("outputs/phase83")
DEFAULT_PHASE86_DIR = Path("outputs/phase86")
TRAIN_MONTHS = {"2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"}
TEST_MONTHS = {"2026-07", "2026-08", "2026-09", "2026-10", "2026-11", "2026-12"}


def parse_thresholds(value: str) -> list[tuple[float, float]]:
    pairs: list[tuple[float, float]] = []
    for token in str(value).split("|"):
        match = re.match(r"q([0-9.]+):(.+)", token)
        if match:
            pairs.append((float(match.group(1)), float(match.group(2))))
    return pairs


def load_inputs(phase83_dir: Path, phase86_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    bars_path = phase83_dir / "stratified_source_event_bars.parquet"
    families_path = phase86_dir / "precommitted_composite_signal_families.csv"
    gates_path = phase86_dir / "precommitted_validation_gates.csv"
    for path in [bars_path, families_path, gates_path]:
        if not path.exists():
            raise FileNotFoundError(path)
    return pd.read_parquet(bars_path), pd.read_csv(families_path), pd.read_csv(gates_path)


def add_cost_columns(bars: pd.DataFrame) -> pd.DataFrame:
    frame = bars.copy()
    profile = retail_profile()
    slippage_ticks = float(profile["fixed_slippage_ticks"])
    impact_bps = float(profile["impact_bps"]) + float(profile.get("fees_bps", 0.0))
    zerodha_bps = profile_cost_bps(profile)
    spread_bps = frame["avg_spread"].astype(float) / frame["close_mid_price"].replace(0, np.nan).astype(float) * 10000.0
    frame["spread_cross_bps"] = spread_bps
    frame["one_way_cost_hurdle_bps"] = (spread_bps / 2.0) + (slippage_ticks * spread_bps) + impact_bps + zerodha_bps
    p75 = (
        frame.groupby(["trade_month", "symbol"], sort=True)["one_way_cost_hurdle_bps"]
        .quantile(0.75)
        .rename("symbol_month_p75_cost_hurdle_bps")
        .reset_index()
    )
    frame = frame.merge(p75, on=["trade_month", "symbol"], how="left")
    return frame


def build_candidate_specs(families: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for family in families.itertuples(index=False):
        intensity_thresholds = parse_thresholds(family.event_intensity_seed_thresholds)
        move_thresholds = parse_thresholds(family.abs_bar_return_seed_thresholds)
        for intensity_q, intensity_threshold in intensity_thresholds:
            for move_q, move_threshold in move_thresholds:
                rows.append(
                    {
                        "candidate_id": f"{family.family_id}_I{str(intensity_q).replace('.', '_')}_M{str(move_q).replace('.', '_')}",
                        "family_id": family.family_id,
                        "direction_rule": family.direction_rule,
                        "intensity_quantile": intensity_q,
                        "event_intensity_threshold": intensity_threshold,
                        "abs_bar_return_quantile": move_q,
                        "abs_bar_return_threshold_bps": move_threshold,
                        "requires_shock_bar": "shock_bar" in str(family.required_filters),
                    }
                )
    return pd.DataFrame(rows)


def candidate_trades(bars: pd.DataFrame, spec: dict[str, Any]) -> pd.DataFrame:
    frame = bars[bars["next_bar_return"].notna()].copy()
    selected = frame[
        (frame["avg_event_intensity_proxy"].astype(float) >= float(spec["event_intensity_threshold"]))
        & ((frame["bar_return"].abs() * 10000.0) >= float(spec["abs_bar_return_threshold_bps"]))
    ].copy()
    if bool(spec["requires_shock_bar"]):
        selected = selected[(selected["is_market_shock_bar"].astype(bool)) | (selected["is_symbol_shock_bar"].astype(bool))].copy()
    else:
        selected = selected[selected["one_way_cost_hurdle_bps"].le(selected["symbol_month_p75_cost_hurdle_bps"])].copy()
    if selected.empty:
        return selected
    if str(spec["direction_rule"]).strip() == "side = -sign(bar_return)":
        selected["side"] = -np.sign(selected["bar_return"].astype(float))
    else:
        selected["side"] = np.sign(selected["bar_return"].astype(float))
    selected = selected[selected["side"].ne(0)].copy()
    selected["gross_return"] = selected["side"].astype(float) * selected["next_bar_return"].astype(float)
    selected["cost_return"] = selected["one_way_cost_hurdle_bps"].astype(float) / 10000.0
    selected["net_return"] = selected["gross_return"] - selected["cost_return"]
    selected["gross_pnl_inr"] = selected["gross_return"] * DEFAULT_ORDER_NOTIONAL_INR
    selected["cost_pnl_drag_inr"] = selected["cost_return"] * DEFAULT_ORDER_NOTIONAL_INR
    selected["net_pnl_inr"] = selected["net_return"] * DEFAULT_ORDER_NOTIONAL_INR
    selected["candidate_id"] = spec["candidate_id"]
    selected["family_id"] = spec["family_id"]
    selected["split"] = np.where(selected["trade_month"].isin(TRAIN_MONTHS), "train", np.where(selected["trade_month"].isin(TEST_MONTHS), "test", "excluded"))
    return selected[selected["split"].isin(["train", "test"])].copy()


def split_metrics(trades: pd.DataFrame, split: str) -> dict[str, Any]:
    group = trades[trades["split"].eq(split)].copy()
    if group.empty:
        return {
            f"{split}_trades": 0,
            f"{split}_symbols": 0,
            f"{split}_net_pnl_inr": 0.0,
            f"{split}_gross_pnl_inr": 0.0,
            f"{split}_cost_pnl_drag_inr": 0.0,
            f"{split}_precision_cost_clear": 0.0,
            f"{split}_positive_months": 0,
            f"{split}_months": 0,
            f"{split}_cost_drag_to_abs_gross_ratio": np.nan,
            f"{split}_max_month_contribution_abs": np.nan,
        }
    month_net = group.groupby("trade_month", sort=True)["net_pnl_inr"].sum()
    gross = float(group["gross_pnl_inr"].sum())
    cost = float(group["cost_pnl_drag_inr"].sum())
    total_net = float(group["net_pnl_inr"].sum())
    if abs(total_net) > 0:
        max_contrib = float(month_net.abs().max() / abs(total_net))
    else:
        max_contrib = np.nan
    return {
        f"{split}_trades": int(len(group)),
        f"{split}_symbols": int(group["symbol"].nunique()),
        f"{split}_net_pnl_inr": total_net,
        f"{split}_gross_pnl_inr": gross,
        f"{split}_cost_pnl_drag_inr": cost,
        f"{split}_precision_cost_clear": float((group["gross_return"] > group["cost_return"]).mean()),
        f"{split}_positive_months": int((month_net > 0).sum()),
        f"{split}_months": int(month_net.shape[0]),
        f"{split}_cost_drag_to_abs_gross_ratio": cost / abs(gross) if abs(gross) > 0 else np.nan,
        f"{split}_max_month_contribution_abs": max_contrib,
    }


def evaluate_candidate(spec: dict[str, Any], trades: pd.DataFrame) -> dict[str, Any]:
    row = dict(spec)
    row.update(split_metrics(trades, "train"))
    row.update(split_metrics(trades, "test"))
    row["train_pass"] = bool(row["train_net_pnl_inr"] > 0 and row["train_precision_cost_clear"] >= 0.55 and row["train_trades"] >= 1000 and row["train_symbols"] >= 20)
    row["test_pass"] = bool(
        row["test_net_pnl_inr"] > 0
        and row["test_precision_cost_clear"] >= 0.55
        and row["test_trades"] >= 1000
        and row["test_symbols"] >= 20
        and row["test_positive_months"] >= 4
        and (pd.notna(row["test_max_month_contribution_abs"]) and row["test_max_month_contribution_abs"] <= 0.50)
        and (pd.notna(row["test_cost_drag_to_abs_gross_ratio"]) and row["test_cost_drag_to_abs_gross_ratio"] <= 0.60)
    )
    row["phase87_candidate_pass"] = bool(row["train_pass"] and row["test_pass"])
    return row


def run_replay(bars: pd.DataFrame, specs: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    result_rows: list[dict[str, Any]] = []
    trade_frames: list[pd.DataFrame] = []
    monthly_rows: list[dict[str, Any]] = []
    for spec in specs.to_dict("records"):
        trades = candidate_trades(bars, spec)
        result_rows.append(evaluate_candidate(spec, trades))
        if not trades.empty:
            trade_frames.append(trades)
            monthly = trades.groupby(["candidate_id", "family_id", "split", "trade_month"], sort=True).agg(
                trades=("symbol", "count"),
                symbols=("symbol", "nunique"),
                net_pnl_inr=("net_pnl_inr", "sum"),
                gross_pnl_inr=("gross_pnl_inr", "sum"),
                cost_pnl_drag_inr=("cost_pnl_drag_inr", "sum"),
                precision_cost_clear=("gross_return", lambda s: float((s > trades.loc[s.index, "cost_return"]).mean())),
            ).reset_index()
            monthly_rows.append(monthly)
    results = pd.DataFrame(result_rows).sort_values(["phase87_candidate_pass", "test_net_pnl_inr"], ascending=[False, False], kind="mergesort")
    trades_all = pd.concat(trade_frames, ignore_index=True) if trade_frames else pd.DataFrame()
    monthly_all = pd.concat(monthly_rows, ignore_index=True) if monthly_rows else pd.DataFrame()
    return results, monthly_all, trades_all


def summarize(results: pd.DataFrame, specs: pd.DataFrame) -> pd.DataFrame:
    passed = int(results["phase87_candidate_pass"].sum()) if not results.empty else 0
    train_pass = int(results["train_pass"].sum()) if not results.empty else 0
    test_pass = int(results["test_pass"].sum()) if not results.empty else 0
    best_test = float(results["test_net_pnl_inr"].max()) if not results.empty else 0.0
    return pd.DataFrame(
        [
            ("phase87_precommitted_candidate_rows", int(len(specs)), "Precommitted candidates replayed"),
            ("phase87_train_pass_candidates", train_pass, "Candidates passing train gates"),
            ("phase87_test_pass_candidates", test_pass, "Candidates passing test gates"),
            ("phase87_full_pass_candidates", passed, "Candidates passing both train and test gates"),
            ("phase87_best_test_net_pnl_inr", best_test, "Best test after-cost net P&L"),
            ("phase87_composite_signal_replay_pass", int(passed > 0), "1 means at least one precommitted family survives"),
            (
                "phase87_recommend_next_action",
                "expand_surviving_composite_family_with_risk_controls" if passed > 0 else "retire_precommitted_composite_family_or_design_new_feature_class",
                "Recommended next milestone",
            ),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase87 Precommitted Composite Signal Replay",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase87 executes only the Phase86-precommitted composite signal families on the Phase83 cached stratified bars.",
        "No thresholds are widened in this replay.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase87_precommitted_composite_signal_replay_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase87(phase83_dir: Path, phase86_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    bars_raw, families, gates = load_inputs(phase83_dir, phase86_dir)
    bars = add_cost_columns(bars_raw)
    specs = build_candidate_specs(families)
    results, monthly, trades = run_replay(bars, specs)
    acceptance = summarize(results, specs)
    specs.to_csv(output_dir / "precommitted_candidate_specs.csv", index=False)
    results.to_csv(output_dir / "precommitted_candidate_results.csv", index=False)
    monthly.to_csv(output_dir / "precommitted_candidate_monthly.csv", index=False)
    trades.to_csv(output_dir / "precommitted_candidate_trades.csv", index=False)
    acceptance.to_csv(output_dir / "precommitted_composite_replay_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Candidate Results": results,
            "Validation Gates": gates,
            "Monthly Results Sample": monthly.head(80),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase87_precommitted_composite_signal_replay",
        "composite_signal_replay_pass": int(
            acceptance.loc[acceptance["metric"].eq("phase87_composite_signal_replay_pass"), "value"].iloc[0]
        ),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase87",
            generated_utc=generated_utc,
            inputs={
                "phase83_bar_cache": str(phase83_dir / "stratified_source_event_bars.parquet"),
                "phase86_precommit": str(phase86_dir / "precommitted_composite_signal_families.csv"),
            },
            parameters={
                "train_months": "|".join(sorted(TRAIN_MONTHS)),
                "test_months": "|".join(sorted(TEST_MONTHS)),
                "threshold_policy": "phase86_locked_no_widening",
            },
            outputs={
                "candidate_specs": str(output_dir / "precommitted_candidate_specs.csv"),
                "candidate_results": str(output_dir / "precommitted_candidate_results.csv"),
                "monthly": str(output_dir / "precommitted_candidate_monthly.csv"),
                "trades": str(output_dir / "precommitted_candidate_trades.csv"),
                "acceptance_summary": str(output_dir / "precommitted_composite_replay_acceptance_summary.csv"),
                "report": str(output_dir / "phase87_precommitted_composite_signal_replay_report.md"),
                "manifest": str(output_dir / "phase87_precommitted_composite_signal_replay_manifest.json"),
            },
            random_seed="none_deterministic_precommitted_composite_replay",
            scenario_ids="phase87_phase86_locked_composite_family",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase83_source_event_ordinal_alignment",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase87_precommitted_composite_signal_replay_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replay Phase86 precommitted composite signal families.")
    parser.add_argument("--phase83-dir", type=Path, default=Path("outputs/phase83"))
    parser.add_argument("--phase86-dir", type=Path, default=Path("outputs/phase86"))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase87(args.phase83_dir, args.phase86_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
