from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from synthetic_l2.phase12_execution_simulator import EXECUTION_PROFILES, _zerodha_order_formula_charges
from synthetic_l2.reproducibility import reproducibility_fields


STRATEGY_IDS = ["S01", "S02", "S05", "S07", "S09"]
BASELINE_IDS = ["B01", "B03", "B06"]


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    text = frame.copy()
    for column in text.columns:
        text[column] = text[column].map(lambda value: "" if pd.isna(value) else (f"{value:.6g}" if isinstance(value, float) else str(value)))
    headers = [str(column) for column in text.columns]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |" for row in text.values.tolist())
    return "\n".join(lines)


def load_event_features(path: Path) -> pd.DataFrame:
    frame = pq.read_table(path).to_pandas()
    ordered = frame.sort_values(
        ["feed_profile", "trade_date", "stage_b2_bucket", "scenario_day", "symbol", "receive_sequence"],
        kind="mergesort",
    ).reset_index(drop=True)
    group_cols = ["feed_profile", "trade_date", "stage_b2_bucket", "scenario_day", "symbol"]
    grouped = ordered.groupby(group_cols, sort=False)
    ordered["next_mid_price"] = grouped["mid_price"].shift(-1)
    ordered["event_return_fwd"] = ordered["next_mid_price"] / ordered["mid_price"] - 1.0
    ordered["momentum_3_event"] = grouped["mid_return_event"].transform(lambda values: values.rolling(3, min_periods=1).sum())
    ordered["local_volatility_6_event"] = grouped["mid_return_event"].transform(lambda values: values.rolling(6, min_periods=2).std()).fillna(0.0)
    ordered["microprice_dev"] = (ordered["microprice_l1"] - ordered["mid_price"]) / ordered["mid_price"].replace(0.0, np.nan)
    ordered["liquidity_score"] = ordered["event_intensity_proxy"].astype(float) / ordered["spread_ticks"].clip(lower=1).astype(float)
    ordered["next_is_bad_feed"] = (
        grouped["is_duplicate"].shift(-1).fillna(False).astype(bool)
        | grouped["is_disconnect_gap"].shift(-1).fillna(False).astype(bool)
        | grouped["is_out_of_order_injected"].shift(-1).fillna(False).astype(bool)
    )
    return ordered


def build_event_signals(features: pd.DataFrame) -> dict[str, pd.Series]:
    q = features[
        [
            "mlofi_qty_event",
            "momentum_3_event",
            "event_intensity_proxy",
            "l5_imbalance",
            "l1_imbalance",
            "microprice_dev",
        ]
    ].quantile([0.2, 0.8]).to_dict()
    wide_spread_limit = features["spread_ticks"].quantile(0.8)
    nontrend = ~features["regime_code"].astype(str).isin(["D03", "D04", "D05", "D06"])

    s01 = np.sign(features["momentum_3_event"]).where(
        (features["momentum_3_event"].abs() >= max(abs(q["momentum_3_event"][0.2]), abs(q["momentum_3_event"][0.8])))
        & (np.sign(features["momentum_3_event"]) == np.sign(features["mlofi_qty_event"]))
        & (features["spread_ticks"] <= wide_spread_limit),
        0,
    )
    s02 = np.sign(features["mlofi_qty_event"]).where(
        features["mlofi_qty_event"].abs() >= max(abs(q["mlofi_qty_event"][0.2]), abs(q["mlofi_qty_event"][0.8])),
        0,
    )
    s05 = np.sign(features["microprice_dev"]).where(
        features["microprice_dev"].abs() >= max(abs(q["microprice_dev"][0.2]), abs(q["microprice_dev"][0.8])),
        0,
    )
    s07 = -np.sign(features["l5_imbalance"]).where(
        nontrend & (features["l5_imbalance"].abs() >= max(abs(q["l5_imbalance"][0.2]), abs(q["l5_imbalance"][0.8]))),
        0,
    )
    s09 = np.sign(features["l1_imbalance"]).where(
        features["l1_imbalance"].abs() >= max(abs(q["l1_imbalance"][0.2]), abs(q["l1_imbalance"][0.8])),
        0,
    )
    b03 = np.sign(features["momentum_3_event"]).where(features["momentum_3_event"].abs() > 0, 0)
    b06 = -np.sign(features["l1_imbalance"]).where(features["l1_imbalance"].abs() >= max(abs(q["l1_imbalance"][0.2]), abs(q["l1_imbalance"][0.8])), 0)
    deterministic = ((features["receive_sequence"].astype("int64") * 1103515245 + 12345) % 2).replace({0: -1, 1: 1})
    b01 = deterministic.where(s09.ne(0), 0)
    return {
        "S01": pd.Series(s01, index=features.index).fillna(0).astype("int8"),
        "S02": pd.Series(s02, index=features.index).fillna(0).astype("int8"),
        "S05": pd.Series(s05, index=features.index).fillna(0).astype("int8"),
        "S07": pd.Series(s07, index=features.index).fillna(0).astype("int8"),
        "S09": pd.Series(s09, index=features.index).fillna(0).astype("int8"),
        "B01": pd.Series(b01, index=features.index).fillna(0).astype("int8"),
        "B03": pd.Series(b03, index=features.index).fillna(0).astype("int8"),
        "B06": pd.Series(b06, index=features.index).fillna(0).astype("int8"),
    }


def _latency_shift(frame: pd.DataFrame, signal: pd.Series, latency_events: int) -> pd.Series:
    if latency_events <= 0:
        return signal
    group_cols = ["feed_profile", "trade_date", "stage_b2_bucket", "scenario_day", "symbol"]
    return signal.groupby([frame[col] for col in group_cols], sort=False).shift(latency_events).fillna(0).astype("int8")


def simulate_signal(
    features: pd.DataFrame,
    signal: pd.Series,
    model_id: str,
    model_type: str,
    profile: dict,
) -> pd.DataFrame:
    total_latency = int(profile["decision_latency_events"] + profile["broker_latency_events"])
    executable = _latency_shift(features, signal, total_latency)
    mask = executable.ne(0) & features["next_mid_price"].notna()
    if bool(profile.get("cancel_on_stale_or_disconnect", False)):
        mask &= ~(features["is_disconnect_gap"].astype(bool) | features["is_out_of_order_injected"].astype(bool) | features["next_is_bad_feed"].astype(bool))
    trades = features.loc[
        mask,
        [
            "feed_profile",
            "stage_b2_bucket",
            "quarter_profile",
            "scenario_day",
            "trade_date",
            "receive_sequence",
            "symbol",
            "regime_code",
            "regime_family",
            "mid_price",
            "next_mid_price",
            "spread_ticks",
            "event_intensity_proxy",
            "local_volatility_6_event",
            "is_market_shock_day",
            "is_symbol_shock",
            "is_disconnect_gap",
        ],
    ].copy()
    trades["model_id"] = model_id
    trades["model_type"] = model_type
    trades["execution_profile"] = profile["execution_profile"]
    trades["latency_events"] = total_latency
    trades["side"] = executable.loc[mask].astype("int8").to_numpy()

    tick_size = np.where(trades["mid_price"] < 250.0, 0.01, 0.05)
    gross_return = trades["side"] * (trades["next_mid_price"] / trades["mid_price"] - 1.0)
    spread_cost = ((trades["spread_ticks"].clip(lower=1) * tick_size) / 2.0) / trades["mid_price"]
    slippage_cost = (float(profile["fixed_slippage_ticks"]) * tick_size) / trades["mid_price"]
    internal_bps_cost = (float(profile["impact_bps"]) + float(profile["fees_bps"])) / 10000.0
    charges = _zerodha_order_formula_charges(
        trades,
        order_notional_inr=float(profile.get("order_notional_inr", 100_000.0)),
        apply_charges=bool(profile.get("apply_zerodha_equity_intraday_charges", False)),
    )
    for column in charges.columns:
        trades[column] = charges[column]
    trades["gross_return"] = gross_return
    trades["spread_crossing_cost_return"] = spread_cost
    trades["slippage_cost_return"] = slippage_cost
    trades["internal_bps_cost_return"] = internal_bps_cost
    trades["cost_return"] = spread_cost + slippage_cost + internal_bps_cost + trades["zerodha_charge_return"]
    trades["net_return"] = trades["gross_return"] - trades["cost_return"]
    trades["net_pnl_inr"] = trades["gross_return"] * trades["entry_notional_inr"] - (
        trades["spread_crossing_cost_return"] + trades["slippage_cost_return"] + trades["internal_bps_cost_return"]
    ) * trades["entry_notional_inr"] - trades["zerodha_total_charges_inr"]
    trades["replay_scope"] = "stage_b2_event_order_replay_not_acceptance"
    return trades


def summarize_trades(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame()
    grouped = trades.groupby(["model_id", "model_type", "execution_profile"], sort=True)
    summary = grouped.agg(
        trades=("net_return", "size"),
        symbols=("symbol", "nunique"),
        scenario_days=("scenario_day", "nunique"),
        mean_gross_return=("gross_return", "mean"),
        mean_cost_return=("cost_return", "mean"),
        mean_zerodha_charge_return=("zerodha_charge_return", "mean"),
        mean_net_return=("net_return", "mean"),
        win_rate_net=("net_return", lambda values: float((values > 0).mean())),
        total_net_pnl_inr=("net_pnl_inr", "sum"),
        market_shock_trade_fraction=("is_market_shock_day", "mean"),
        disconnect_trade_fraction=("is_disconnect_gap", "mean"),
    ).reset_index()
    summary["acceptance_ready"] = False
    summary["replay_status"] = "event_order_replay_not_acceptance"
    return summary


def risk_summary(trades: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if trades.empty:
        return pd.DataFrame(rows)
    for keys, group in trades.groupby(["model_id", "model_type", "execution_profile"], sort=True):
        model_id, model_type, execution_profile = keys
        ordered = group.sort_values(["trade_date", "receive_sequence"], kind="mergesort").copy()
        ordered["running_net_pnl_inr"] = ordered.groupby("trade_date", sort=False)["net_pnl_inr"].cumsum()
        ordered["running_peak"] = ordered.groupby("trade_date", sort=False)["running_net_pnl_inr"].cummax()
        ordered["drawdown_inr"] = ordered["running_net_pnl_inr"] - ordered["running_peak"]
        daily = ordered.groupby("trade_date", sort=True).agg(
            daily_net_pnl_inr=("net_pnl_inr", "sum"),
            max_intraday_drawdown_inr=("drawdown_inr", "min"),
            trades=("net_pnl_inr", "size"),
        )
        rows.append(
            {
                "model_id": model_id,
                "model_type": model_type,
                "execution_profile": execution_profile,
                "trade_dates": int(daily.shape[0]),
                "worst_daily_net_pnl_inr": float(daily["daily_net_pnl_inr"].min()),
                "tail_loss_1pct_trade_pnl_inr": float(ordered["net_pnl_inr"].quantile(0.01)),
                "max_intraday_drawdown_inr": float(daily["max_intraday_drawdown_inr"].min()),
                "daily_loss_breach_days": int((daily["daily_net_pnl_inr"] < -75_000.0).sum()),
                "drawdown_breach_days": int((daily["max_intraday_drawdown_inr"] < -100_000.0).sum()),
                "risk_status": "risk_breached_proxy" if ((daily["daily_net_pnl_inr"] < -75_000.0).any() or (daily["max_intraday_drawdown_inr"] < -100_000.0).any()) else "risk_not_breached_proxy",
            }
        )
    return pd.DataFrame(rows)


def baseline_comparison(summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if summary.empty:
        return pd.DataFrame(rows)
    baselines = summary[summary["model_type"].eq("baseline")]
    strategies = summary[summary["model_type"].eq("strategy")]
    for row in strategies.to_dict("records"):
        comp = baselines[baselines["execution_profile"].eq(row["execution_profile"])]
        best_baseline = float(comp["mean_net_return"].max()) if len(comp) else np.nan
        rows.append(
            {
                "model_id": row["model_id"],
                "execution_profile": row["execution_profile"],
                "strategy_mean_net_return": row["mean_net_return"],
                "best_baseline_mean_net_return": best_baseline,
                "net_return_lift_vs_best_baseline": row["mean_net_return"] - best_baseline if pd.notna(best_baseline) else np.nan,
                "beats_best_baseline_proxy": bool(row["mean_net_return"] > best_baseline) if pd.notna(best_baseline) else False,
                "comparison_scope": "stage_b2_event_replay_proxy",
            }
        )
    return pd.DataFrame(rows)


def replay_summary(summary: pd.DataFrame, risk: pd.DataFrame, comparison: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"metric": "phase25_models_replayed", "value": int(summary["model_id"].nunique()), "description": "Strategies and baselines replayed"},
            {"metric": "phase25_strategy_models_replayed", "value": int(summary.loc[summary["model_type"].eq("strategy"), "model_id"].nunique()), "description": "Strategy models replayed"},
            {"metric": "phase25_baseline_models_replayed", "value": int(summary.loc[summary["model_type"].eq("baseline"), "model_id"].nunique()), "description": "Baseline models replayed"},
            {"metric": "phase25_execution_profiles", "value": int(summary["execution_profile"].nunique()), "description": "Execution profiles evaluated"},
            {"metric": "phase25_total_trades", "value": int(summary["trades"].sum()), "description": "Total event-order replay trades"},
            {"metric": "phase25_positive_strategy_profile_rows", "value": int((summary["model_type"].eq("strategy") & (summary["mean_net_return"] > 0)).sum()), "description": "Strategy/profile rows with positive mean net return"},
            {"metric": "phase25_risk_breached_rows", "value": int((risk["risk_status"].astype(str) == "risk_breached_proxy").sum()), "description": "Model/profile rows with proxy risk breaches"},
            {"metric": "phase25_beats_best_baseline_rows", "value": int(comparison["beats_best_baseline_proxy"].astype(bool).sum()) if len(comparison) else 0, "description": "Strategy/profile rows beating best baseline proxy"},
            {"metric": "phase25_acceptance_ready", "value": 0, "description": "Event replay is execution evidence, not acceptance evidence"},
        ]
    )


def write_report(output_dir: Path, summary: pd.DataFrame, risk: pd.DataFrame, comparison: pd.DataFrame, overall: pd.DataFrame) -> None:
    lines = [
        "# Phase 25 Event Replay Expansion",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This milestone expands actual strategy execution over the Stage B2 event-ordered feature product.",
        "It produces trade/order-style replay rows with Zerodha order-formula costs where applicable.",
        "It is stronger than static planning, but it is still not acceptance-grade because it uses a small Stage B2 engineering subset.",
        "",
        "## Summary",
        "",
        _markdown_table(overall),
        "",
        "## Replay Summary",
        "",
        _markdown_table(summary),
        "",
        "## Risk Summary",
        "",
        _markdown_table(risk),
        "",
        "## Baseline Comparison",
        "",
        _markdown_table(comparison),
        "",
    ]
    (output_dir / "phase25_event_replay_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase25(event_features_path: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    features = load_event_features(event_features_path)
    signals = build_event_signals(features)
    trade_frames = []
    for model_id in STRATEGY_IDS + BASELINE_IDS:
        model_type = "strategy" if model_id.startswith("S") else "baseline"
        for profile in EXECUTION_PROFILES:
            trade_frames.append(simulate_signal(features, signals[model_id], model_id, model_type, profile))
    trades = pd.concat(trade_frames, ignore_index=True) if trade_frames else pd.DataFrame()
    summary = summarize_trades(trades)
    risk = risk_summary(trades)
    comparison = baseline_comparison(summary)
    overall = replay_summary(summary, risk, comparison)

    pq.write_table(pa.Table.from_pandas(trades, preserve_index=False), output_dir / "event_replay_trade_ledger.parquet", compression="zstd")
    summary.to_csv(output_dir / "event_replay_summary.csv", index=False)
    risk.to_csv(output_dir / "event_replay_risk_summary.csv", index=False)
    comparison.to_csv(output_dir / "event_replay_baseline_comparison.csv", index=False)
    overall.to_csv(output_dir / "event_replay_overall_summary.csv", index=False)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "event_feature_rows": int(len(features)),
        "trade_rows": int(len(trades)),
        "model_profile_rows": int(len(summary)),
        "scope": "phase25_event_replay_expansion_not_acceptance_evidence",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase25",
            generated_utc=generated_utc,
            inputs={"event_features": str(event_features_path), "execution_profiles": "src.synthetic_l2.phase12_execution_simulator.EXECUTION_PROFILES"},
            parameters={"strategy_ids": STRATEGY_IDS, "baseline_ids": BASELINE_IDS},
            outputs={
                "trade_ledger": str(output_dir / "event_replay_trade_ledger.parquet"),
                "summary": str(output_dir / "event_replay_summary.csv"),
                "risk_summary": str(output_dir / "event_replay_risk_summary.csv"),
                "baseline_comparison": str(output_dir / "event_replay_baseline_comparison.csv"),
                "overall_summary": str(output_dir / "event_replay_overall_summary.csv"),
                "report": str(output_dir / "phase25_event_replay_report.md"),
                "manifest": str(output_dir / "phase25_event_replay_manifest.json"),
            },
            random_seed="deterministic_baseline_b01_receive_sequence_hash",
            scenario_ids="stage_b2_event_ordered_development_subset",
            cost_model_version="zerodha_equity_intraday_nse_order_formula_v2_2026_07_14",
            latency_model_version="phase12_execution_profiles_event_latency_counts",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase25_event_replay_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, summary, risk, comparison, overall)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run event-order strategy replay expansion over Stage B2 features.")
    parser.add_argument("--event-features", type=Path, default=Path("outputs/stage_b2/stage_b2_event_feature_panel.parquet"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase25"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase25(args.event_features, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
