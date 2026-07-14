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
from synthetic_l2.phase25_event_replay_expansion import _markdown_table, risk_summary, summarize_trades
from synthetic_l2.reproducibility import reproducibility_fields


PARTIAL_STRATEGIES = ["S03", "S04", "S06", "S08"]
MIN_TRADES_FOR_PROXY_CANDIDATE = 50


def _tick_size(mid_price: pd.Series) -> np.ndarray:
    return np.where(mid_price.astype(float) < 250.0, 0.01, 0.05)


def _latency_shift(frame: pd.DataFrame, signal: pd.Series, latency_events: int, group_cols: list[str]) -> pd.Series:
    if latency_events <= 0:
        return signal
    return signal.groupby([frame[col] for col in group_cols], sort=False).shift(latency_events).fillna(0).astype("int8")


def load_label_panel(path: Path) -> pd.DataFrame:
    frame = pq.read_table(path).to_pandas()
    frame = frame.sort_values(["symbol", "event_ts_receive_ms", "sequence_local"], kind="mergesort").reset_index(drop=True)
    return frame


def build_row_signal(frame: pd.DataFrame, strategy_id: str) -> pd.Series:
    if strategy_id == "S03":
        signal = np.sign(frame["mlofi_qty"].fillna(0)).where(frame["s03_reversal_candidate_proxy"].astype(bool), 0)
    elif strategy_id == "S04":
        signal = frame["trade_side_sign"].where(frame["s04_trade_flow_depth_confirm_proxy"].astype(bool), 0)
    elif strategy_id == "S06":
        signal = -frame["s06_absorption_side"].where(frame["s06_absorption_like_proxy"].astype(bool), 0)
    else:
        raise ValueError(f"Unsupported row-label strategy: {strategy_id}")
    return pd.Series(signal, index=frame.index).fillna(0).astype("int8")


def simulate_row_strategy(frame: pd.DataFrame, signal: pd.Series, strategy_id: str, profile: dict) -> pd.DataFrame:
    total_latency = int(profile["decision_latency_events"] + profile["broker_latency_events"])
    executable = _latency_shift(frame, signal, total_latency, ["symbol"])
    mask = executable.ne(0) & frame["next_mid_1"].notna() & frame["usable_short_horizon"].astype(bool)
    if bool(profile.get("cancel_on_stale_or_disconnect", False)):
        mask &= ~(frame["stale_gap_gt_5s"].astype(bool) | frame["stale_gap_gt_15s"].astype(bool))
    trades = frame.loc[
        mask,
        [
            "trading_date",
            "event_ts_receive_ms",
            "sequence_local",
            "symbol",
            "mid_price",
            "next_mid_1",
            "spread_ticks",
            "mlofi_qty",
            "l1_imbalance",
            "l5_imbalance",
            "cum_volume_increment",
            "stale_gap_gt_5s",
            "stale_gap_gt_15s",
        ],
    ].copy()
    trades = trades.rename(columns={"trading_date": "trade_date", "event_ts_receive_ms": "receive_sequence", "next_mid_1": "next_mid_price"})
    trades["model_id"] = strategy_id
    trades["model_type"] = "partial_strategy_proxy"
    trades["execution_profile"] = profile["execution_profile"]
    trades["latency_events"] = total_latency
    trades["side"] = executable.loc[mask].astype("int8").to_numpy()
    trades["feed_profile"] = "real_received_tick_delta_proxy"
    trades["stage_b2_bucket"] = "phase28_richer_event_label"
    trades["quarter_profile"] = "real_one_day"
    trades["scenario_day"] = 1
    trades["regime_code"] = "real_sample_day"
    trades["regime_family"] = "real_received_tick_delta"
    trades["event_intensity_proxy"] = 1.0 / trades["receive_sequence"].diff().abs().replace(0, np.nan).fillna(1.0)
    trades["local_volatility_6_event"] = np.nan
    trades["is_market_shock_day"] = False
    trades["is_symbol_shock"] = False
    trades["is_disconnect_gap"] = trades["stale_gap_gt_5s"].astype(bool) | trades["stale_gap_gt_15s"].astype(bool)
    trades["proxy_label_source"] = "phase28_weak_market_by_price_label"
    return apply_costs(trades, profile)


def build_s08_bucket_panel(frame: pd.DataFrame) -> pd.DataFrame:
    usable = frame[frame["usable_short_horizon"].astype(bool)].copy()
    usable["bucket_5s"] = (usable["event_ts_receive_ms"].astype("int64") // 5000) * 5000
    symbol_bucket = (
        usable.groupby(["bucket_5s", "symbol"], sort=True)
        .agg(
            trade_date=("trading_date", "first"),
            mid_price=("mid_price", "last"),
            spread_ticks=("spread_ticks", "median"),
            symbol_mlofi=("mlofi_qty", "sum"),
            symbol_events=("symbol", "size"),
        )
        .reset_index()
    )
    market = symbol_bucket.groupby("bucket_5s", sort=True).agg(market_mlofi=("symbol_mlofi", "sum")).reset_index()
    panel = symbol_bucket.merge(market, on="bucket_5s", how="left").sort_values(["symbol", "bucket_5s"], kind="mergesort")
    panel["ex_self_market_mlofi"] = panel["market_mlofi"] - panel["symbol_mlofi"]
    panel["next_mid_price"] = panel.groupby("symbol", sort=False)["mid_price"].shift(-1)
    panel["side_signal"] = np.sign(panel["ex_self_market_mlofi"].fillna(0)).astype("int8")
    return panel


def simulate_s08(panel: pd.DataFrame, profile: dict) -> pd.DataFrame:
    total_latency = int(profile["decision_latency_events"] + profile["broker_latency_events"])
    signal = pd.Series(panel["side_signal"].to_numpy(), index=panel.index).astype("int8")
    executable = _latency_shift(panel, signal, total_latency, ["symbol"])
    mask = executable.ne(0) & panel["next_mid_price"].notna()
    trades = panel.loc[mask, ["trade_date", "bucket_5s", "symbol", "mid_price", "next_mid_price", "spread_ticks", "ex_self_market_mlofi", "symbol_events"]].copy()
    trades = trades.rename(columns={"bucket_5s": "receive_sequence"})
    trades["model_id"] = "S08"
    trades["model_type"] = "partial_strategy_proxy"
    trades["execution_profile"] = profile["execution_profile"]
    trades["latency_events"] = total_latency
    trades["side"] = executable.loc[mask].astype("int8").to_numpy()
    trades["feed_profile"] = "real_received_5s_lead_lag_proxy"
    trades["stage_b2_bucket"] = "phase28_lead_lag_bucket"
    trades["quarter_profile"] = "real_one_day"
    trades["scenario_day"] = 1
    trades["regime_code"] = "real_sample_day"
    trades["regime_family"] = "real_received_tick_delta"
    trades["event_intensity_proxy"] = trades["symbol_events"].astype(float)
    trades["local_volatility_6_event"] = np.nan
    trades["is_market_shock_day"] = False
    trades["is_symbol_shock"] = False
    trades["is_disconnect_gap"] = False
    trades["proxy_label_source"] = "phase28_weak_5s_receive_bucket_lead_lag"
    return apply_costs(trades, profile)


def apply_costs(trades: pd.DataFrame, profile: dict) -> pd.DataFrame:
    if trades.empty:
        return trades
    tick_size = _tick_size(trades["mid_price"])
    gross_return = trades["side"] * (trades["next_mid_price"] / trades["mid_price"] - 1.0)
    spread_cost = ((trades["spread_ticks"].clip(lower=1).astype(float) * tick_size) / 2.0) / trades["mid_price"].astype(float)
    slippage_cost = (float(profile["fixed_slippage_ticks"]) * tick_size) / trades["mid_price"].astype(float)
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
    trades["replay_scope"] = "phase29_partial_strategy_proxy_replay_not_acceptance"
    return trades


def baseline_comparison(summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in summary.iterrows():
        comp = summary[(summary["execution_profile"].eq(row["execution_profile"])) & (summary["model_id"].ne(row["model_id"]))]
        peer_best = float(comp["mean_net_return"].max()) if len(comp) else np.nan
        rows.append(
            {
                "model_id": row["model_id"],
                "execution_profile": row["execution_profile"],
                "trades": int(row["trades"]),
                "mean_net_return": float(row["mean_net_return"]),
                "best_peer_partial_strategy_mean_net_return": peer_best,
                "lift_vs_best_peer_partial_strategy": float(row["mean_net_return"] - peer_best) if pd.notna(peer_best) else np.nan,
                "positive_after_costs": bool(row["mean_net_return"] > 0),
                "beats_peer_proxy": bool(row["mean_net_return"] > peer_best) if pd.notna(peer_best) else False,
                "enough_trades_for_proxy_candidate": bool(row["trades"] >= MIN_TRADES_FOR_PROXY_CANDIDATE),
            }
        )
    return pd.DataFrame(rows)


def candidate_summary(comparison: pd.DataFrame, risk: pd.DataFrame) -> pd.DataFrame:
    merged = comparison.merge(risk[["model_id", "execution_profile", "risk_status"]], on=["model_id", "execution_profile"], how="left")
    merged["realistic_charged_profile"] = ~merged["execution_profile"].astype(str).eq("zero_latency_spread_only_control")
    merged["risk_not_breached_proxy"] = merged["risk_status"].astype(str).eq("risk_not_breached_proxy")
    merged["partial_proxy_candidate"] = (
        merged["realistic_charged_profile"]
        & merged["positive_after_costs"]
        & merged["enough_trades_for_proxy_candidate"]
        & merged["risk_not_breached_proxy"]
    )
    return merged.sort_values(["partial_proxy_candidate", "mean_net_return"], ascending=[False, False], kind="mergesort").reset_index(drop=True)


def overall_summary(summary: pd.DataFrame, candidates: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"metric": "phase29_partial_strategies_replayed", "value": int(summary["model_id"].nunique()), "description": "Partial strategy proxy families replayed"},
            {"metric": "phase29_strategy_profile_rows", "value": int(len(summary)), "description": "Strategy/profile summary rows"},
            {"metric": "phase29_total_replay_trades", "value": int(summary["trades"].sum()) if len(summary) else 0, "description": "Total partial-strategy proxy replay trades"},
            {"metric": "phase29_positive_after_cost_rows", "value": int(candidates["positive_after_costs"].sum()) if len(candidates) else 0, "description": "Rows with positive mean net return after costs"},
            {"metric": "phase29_realistic_positive_rows", "value": int((candidates["realistic_charged_profile"] & candidates["positive_after_costs"]).sum()) if len(candidates) else 0, "description": "Retail/stressed rows positive after costs"},
            {"metric": "phase29_proxy_candidate_rows", "value": int(candidates["partial_proxy_candidate"].sum()) if len(candidates) else 0, "description": "Rows passing realistic, positive, trade-count and proxy-risk checks"},
            {"metric": "phase29_acceptance_ready", "value": 0, "description": "Partial strategy replay uses weak proxy labels, not acceptance evidence"},
        ]
    )


def write_report(output_dir: Path, overall: pd.DataFrame, summary: pd.DataFrame, risk: pd.DataFrame, candidates: pd.DataFrame) -> None:
    lines = [
        "# Phase 29 Partial Strategy Proxy Replay",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This milestone converts the Phase 28 weak proxy labels for S03/S04/S06/S08 into executable replay signals.",
        "It is an execution diagnostic, not strategy acceptance evidence.",
        "",
        "## Overall Summary",
        "",
        _markdown_table(overall),
        "",
        "## Strategy/Profile Summary",
        "",
        _markdown_table(summary),
        "",
        "## Candidate Summary",
        "",
        _markdown_table(candidates),
        "",
        "## Risk Summary",
        "",
        _markdown_table(risk),
        "",
    ]
    (output_dir / "phase29_partial_strategy_proxy_replay_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase29(label_panel_path: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    frame = load_label_panel(label_panel_path)
    s08_panel = build_s08_bucket_panel(frame)
    trade_frames = []
    for profile in EXECUTION_PROFILES:
        for strategy_id in ["S03", "S04", "S06"]:
            trade_frames.append(simulate_row_strategy(frame, build_row_signal(frame, strategy_id), strategy_id, profile))
        trade_frames.append(simulate_s08(s08_panel, profile))
    trades = pd.concat([part for part in trade_frames if not part.empty], ignore_index=True) if trade_frames else pd.DataFrame()
    summary = summarize_trades(trades)
    risk = risk_summary(trades)
    comparison = baseline_comparison(summary)
    candidates = candidate_summary(comparison, risk)
    overall = overall_summary(summary, candidates)

    pq.write_table(pa.Table.from_pandas(trades, preserve_index=False), output_dir / "partial_strategy_proxy_trade_ledger.parquet", compression="zstd")
    summary.to_csv(output_dir / "partial_strategy_proxy_summary.csv", index=False)
    risk.to_csv(output_dir / "partial_strategy_proxy_risk_summary.csv", index=False)
    comparison.to_csv(output_dir / "partial_strategy_proxy_peer_comparison.csv", index=False)
    candidates.to_csv(output_dir / "partial_strategy_proxy_candidate_summary.csv", index=False)
    overall.to_csv(output_dir / "partial_strategy_proxy_overall_summary.csv", index=False)
    write_report(output_dir, overall, summary, risk, candidates)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "input_label_rows": int(len(frame)),
        "trade_rows": int(len(trades)),
        "strategy_profile_rows": int(len(summary)),
        "scope": "phase29_partial_strategy_proxy_replay_not_acceptance_evidence",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase29",
            generated_utc=generated_utc,
            inputs={"phase28_richer_event_label_panel": str(label_panel_path)},
            parameters={
                "partial_strategies": PARTIAL_STRATEGIES,
                "min_trades_for_proxy_candidate": MIN_TRADES_FOR_PROXY_CANDIDATE,
                "execution_profiles": "src.synthetic_l2.phase12_execution_simulator.EXECUTION_PROFILES",
            },
            outputs={
                "trade_ledger": str(output_dir / "partial_strategy_proxy_trade_ledger.parquet"),
                "summary": str(output_dir / "partial_strategy_proxy_summary.csv"),
                "risk_summary": str(output_dir / "partial_strategy_proxy_risk_summary.csv"),
                "peer_comparison": str(output_dir / "partial_strategy_proxy_peer_comparison.csv"),
                "candidate_summary": str(output_dir / "partial_strategy_proxy_candidate_summary.csv"),
                "overall_summary": str(output_dir / "partial_strategy_proxy_overall_summary.csv"),
                "report": str(output_dir / "phase29_partial_strategy_proxy_replay_report.md"),
                "manifest": str(output_dir / "phase29_partial_strategy_proxy_replay_manifest.json"),
            },
            random_seed="none_deterministic_label_signal_rules",
            scenario_ids="phase28_one_day_proxy_label_panel",
            cost_model_version="zerodha_equity_intraday_nse_order_formula_v2_2026_07_14",
            latency_model_version="phase12_execution_profiles_event_latency_counts",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase29_partial_strategy_proxy_replay_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 29 partial strategy proxy replay over Phase 28 labels.")
    parser.add_argument("--label-panel", type=Path, default=Path("outputs/phase28/richer_event_label_panel.parquet"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase29"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase29(args.label_panel, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
