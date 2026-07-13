from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


FILL_PROFILES = [
    {
        "fill_model": "optimistic_marketable",
        "base_fill_ratio": 1.0,
        "shock_haircut": 0.05,
        "wide_spread_haircut": 0.02,
        "disconnect_haircut": 0.25,
        "queue_position_bucket": "front_or_marketable",
    },
    {
        "fill_model": "neutral_partial",
        "base_fill_ratio": 0.75,
        "shock_haircut": 0.15,
        "wide_spread_haircut": 0.08,
        "disconnect_haircut": 0.40,
        "queue_position_bucket": "middle_queue_proxy",
    },
    {
        "fill_model": "pessimistic_partial",
        "base_fill_ratio": 0.45,
        "shock_haircut": 0.25,
        "wide_spread_haircut": 0.15,
        "disconnect_haircut": 0.60,
        "queue_position_bucket": "back_queue_proxy",
    },
]

RISK_LIMITS = {
    "max_abs_position_units": 15.0,
    "daily_loss_limit_units": -0.75,
    "tail_loss_quantile": 0.01,
    "drawdown_warn_units": -1.0,
}


def load_trade_sample(path: Path) -> pd.DataFrame:
    return pd.read_parquet(path)


def _fill_ratio(base: pd.DataFrame, profile: dict) -> pd.Series:
    ratio = pd.Series(float(profile["base_fill_ratio"]), index=base.index)
    ratio -= np.where(base["is_market_shock_day"].astype(bool) | base["is_symbol_shock"].astype(bool), profile["shock_haircut"], 0.0)
    ratio -= np.where(base["spread_ticks"].astype(float) >= 8, profile["wide_spread_haircut"], 0.0)
    disconnect_flag = base["is_disconnect_gap"].astype(bool) if "is_disconnect_gap" in base else pd.Series(False, index=base.index)
    ratio -= np.where(disconnect_flag, profile["disconnect_haircut"], 0.0)
    return ratio.clip(lower=0.0, upper=1.0)


def build_order_lifecycle(trade_sample: pd.DataFrame) -> pd.DataFrame:
    base = trade_sample.sort_values(
        ["strategy_id", "execution_profile", "trade_date", "feed_profile", "symbol", "bar_index"],
        kind="mergesort",
    ).reset_index(drop=True)
    rows = []
    for profile in FILL_PROFILES:
        frame = base.copy()
        frame["fill_model"] = profile["fill_model"]
        frame["queue_position_bucket"] = profile["queue_position_bucket"]
        frame["submitted_notional"] = 1.0
        frame["submitted_side"] = frame["side"]
        frame["fill_ratio"] = _fill_ratio(frame, profile)
        frame["filled_notional"] = frame["submitted_notional"] * frame["fill_ratio"]
        frame["unfilled_notional"] = frame["submitted_notional"] - frame["filled_notional"]
        frame["is_full_fill"] = frame["fill_ratio"] >= 0.999
        frame["is_partial_fill"] = (frame["fill_ratio"] > 0) & (frame["fill_ratio"] < 0.999)
        frame["is_no_fill"] = frame["fill_ratio"] <= 0
        frame["filled_net_pnl_units"] = frame["net_return"] * frame["filled_notional"]
        frame["filled_gross_pnl_units"] = frame["gross_return"] * frame["filled_notional"]
        frame["filled_cost_units"] = frame["cost_return"] * frame["filled_notional"]
        frame["position_delta_units"] = frame["submitted_side"] * frame["filled_notional"]
        rows.append(frame)
    lifecycle = pd.concat(rows, ignore_index=True)
    group_cols = ["strategy_id", "execution_profile", "fill_model", "trade_date"]
    lifecycle["running_position_units"] = lifecycle.groupby(group_cols, sort=False)["position_delta_units"].cumsum()
    lifecycle["running_pnl_units"] = lifecycle.groupby(group_cols, sort=False)["filled_net_pnl_units"].cumsum()
    lifecycle["running_peak_pnl_units"] = lifecycle.groupby(group_cols, sort=False)["running_pnl_units"].cummax()
    lifecycle["running_drawdown_units"] = lifecycle["running_pnl_units"] - lifecycle["running_peak_pnl_units"]
    lifecycle["position_limit_breach"] = lifecycle["running_position_units"].abs() > RISK_LIMITS["max_abs_position_units"]
    lifecycle["daily_loss_limit_breach"] = lifecycle["running_pnl_units"] <= RISK_LIMITS["daily_loss_limit_units"]
    lifecycle["daily_halt_triggered"] = lifecycle.groupby(group_cols, sort=False)["daily_loss_limit_breach"].cummax().astype(bool)
    lifecycle["risk_trade_allowed"] = ~lifecycle["daily_halt_triggered"].groupby(
        [lifecycle[col] for col in group_cols], sort=False
    ).shift(1).fillna(False).astype(bool)
    lifecycle["risk_adjusted_filled_net_pnl_units"] = np.where(
        lifecycle["risk_trade_allowed"],
        lifecycle["filled_net_pnl_units"],
        0.0,
    )
    return lifecycle


def summarize_fills(lifecycle: pd.DataFrame) -> pd.DataFrame:
    return (
        lifecycle.groupby(["strategy_id", "execution_profile", "fill_model"], sort=True)
        .agg(
            orders=("fill_ratio", "size"),
            mean_fill_ratio=("fill_ratio", "mean"),
            full_fill_fraction=("is_full_fill", "mean"),
            partial_fill_fraction=("is_partial_fill", "mean"),
            no_fill_fraction=("is_no_fill", "mean"),
            submitted_notional=("submitted_notional", "sum"),
            filled_notional=("filled_notional", "sum"),
            unfilled_notional=("unfilled_notional", "sum"),
            filled_net_pnl_units=("filled_net_pnl_units", "sum"),
            filled_cost_units=("filled_cost_units", "sum"),
        )
        .reset_index()
    )


def summarize_risk(lifecycle: pd.DataFrame) -> pd.DataFrame:
    grouped = lifecycle.groupby(["strategy_id", "execution_profile", "fill_model"], sort=True)
    rows = []
    for keys, group in grouped:
        pnl = group["filled_net_pnl_units"].astype(float)
        risk_adj = group["risk_adjusted_filled_net_pnl_units"].astype(float)
        rows.append(
            {
                "strategy_id": keys[0],
                "execution_profile": keys[1],
                "fill_model": keys[2],
                "orders": int(len(group)),
                "max_abs_position_units": float(group["running_position_units"].abs().max()) if len(group) else 0.0,
                "max_drawdown_units": float(group["running_drawdown_units"].min()) if len(group) else 0.0,
                "tail_loss_1pct_units": float(pnl.quantile(RISK_LIMITS["tail_loss_quantile"])) if len(pnl) else None,
                "position_limit_breach_rows": int(group["position_limit_breach"].sum()),
                "daily_loss_limit_breach_rows": int(group["daily_loss_limit_breach"].sum()),
                "daily_halt_rows": int(group["daily_halt_triggered"].sum()),
                "risk_adjusted_net_pnl_units": float(risk_adj.sum()),
                "risk_adjusted_mean_return_units": float(risk_adj.mean()) if len(risk_adj) else None,
                "risk_limits": json.dumps(RISK_LIMITS, sort_keys=True),
            }
        )
    return pd.DataFrame(rows)


def write_report(output_dir: Path, fill_summary: pd.DataFrame, risk_summary: pd.DataFrame, lifecycle_rows: int) -> None:
    fill_status = fill_summary.groupby("fill_model", sort=True).agg(
        strategy_profiles=("strategy_id", "size"),
        mean_fill_ratio=("mean_fill_ratio", "mean"),
        partial_fill_fraction=("partial_fill_fraction", "mean"),
        no_fill_fraction=("no_fill_fraction", "mean"),
    ).reset_index()
    risk_status = risk_summary.groupby("fill_model", sort=True).agg(
        strategy_profiles=("strategy_id", "size"),
        max_drawdown_units=("max_drawdown_units", "min"),
        position_limit_breach_rows=("position_limit_breach_rows", "sum"),
        daily_loss_limit_breach_rows=("daily_loss_limit_breach_rows", "sum"),
    ).reset_index()

    def md(frame: pd.DataFrame) -> str:
        text = frame.copy()
        for col in text.columns:
            text[col] = text[col].map(lambda value: "" if pd.isna(value) else (f"{value:.6g}" if isinstance(value, float) else str(value)))
        headers = [str(col) for col in text.columns]
        lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
        lines.extend("| " + " | ".join(row) + " |" for row in text.values.tolist())
        return "\n".join(lines)

    lines = [
        "# Phase 12 Order Lifecycle and Risk Proxy Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This layer adds deterministic partial-fill, queue-position bucket and risk-control proxy evidence over the Phase 12 sampled trade ledger.",
        "It is not exchange queue truth and must not be used as acceptance-grade passive-fill validation.",
        "",
        f"Lifecycle rows: {lifecycle_rows}",
        "",
        "## Fill Model Summary",
        "",
        md(fill_status),
        "",
        "## Risk Summary",
        "",
        md(risk_status),
        "",
        "## Risk Limits",
        "",
        "```json",
        json.dumps(RISK_LIMITS, indent=2, sort_keys=True),
        "```",
        "",
    ]
    (output_dir / "order_lifecycle_risk_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase12_lifecycle_risk(trade_sample_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    trade_sample = load_trade_sample(trade_sample_path)
    lifecycle = build_order_lifecycle(trade_sample)
    fill_summary = summarize_fills(lifecycle)
    risk_summary = summarize_risk(lifecycle)
    pq.write_table(pa.Table.from_pandas(lifecycle, preserve_index=False), output_dir / "order_lifecycle_sample.parquet", compression="zstd")
    fill_summary.to_csv(output_dir / "partial_fill_summary.csv", index=False)
    risk_summary.to_csv(output_dir / "risk_control_summary.csv", index=False)
    fill_profiles = pd.DataFrame(FILL_PROFILES)
    fill_profiles.to_csv(output_dir / "fill_model_catalog.csv", index=False)
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "trade_sample_path": str(trade_sample_path),
        "input_trade_rows": int(len(trade_sample)),
        "lifecycle_rows": int(len(lifecycle)),
        "fill_models": int(len(fill_profiles)),
        "strategy_profile_fill_rows": int(len(fill_summary)),
        "strategy_profile_risk_rows": int(len(risk_summary)),
        "scope": "sampled_order_lifecycle_partial_fill_and_risk_proxy",
        "not_acceptance_grade": True,
        "risk_limits": RISK_LIMITS,
    }
    (output_dir / "order_lifecycle_risk_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, fill_summary, risk_summary, len(lifecycle))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 12 order-lifecycle, partial-fill and risk-control proxy artifacts.")
    parser.add_argument("--trade-sample", type=Path, default=Path("outputs/phase12/trade_ledger_sample.parquet"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase12_order_lifecycle"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase12_lifecycle_risk(args.trade_sample, args.output_dir)


if __name__ == "__main__":
    main()
