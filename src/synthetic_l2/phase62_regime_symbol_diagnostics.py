from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE61_DIR = Path("outputs/phase61")
DEFAULT_OUTPUT_DIR = Path("outputs/phase62")
ETF_SYMBOLS = {"BANKBEES", "GOLDBEES", "ITBEES", "JUNIORBEES", "NIFTYBEES"}


def _safe_path(path: str | Path) -> str:
    return Path(path).as_posix().replace("'", "''")


def load_phase61_inputs(phase61_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    daily = pd.read_csv(phase61_dir / "wider_sweep_daily_symbol.csv")
    inventory = pd.read_csv(phase61_dir / "wider_sweep_file_inventory.csv")
    candidate = pd.read_csv(phase61_dir / "phase60_candidate_replayed.csv")
    return daily, inventory, candidate


def enrich_with_inventory(daily: pd.DataFrame, inventory: pd.DataFrame) -> pd.DataFrame:
    frame = daily.merge(inventory, on="shard_index", how="left")
    path_text = frame["shard_path"].astype(str)
    frame["trade_month_partition"] = path_text.str.extract(r"trade_month=([^\\/]+)")
    frame["partition_symbol"] = path_text.str.extract(r"symbol=([^\\/]+)")
    frame["instrument_class"] = frame["symbol"].where(~frame["symbol"].isin(ETF_SYMBOLS), "ETF")
    frame.loc[~frame["symbol"].isin(ETF_SYMBOLS), "instrument_class"] = "EQUITY"
    frame["loss_reason"] = "mixed"
    frame.loc[frame["gross_pnl_proxy_inr"] < 0, "loss_reason"] = "wrong_direction"
    frame.loc[(frame["gross_pnl_proxy_inr"] >= 0) & (frame["net_pnl_inr"] < 0), "loss_reason"] = "cost_drag_over_gross_edge"
    frame.loc[frame["net_pnl_inr"] > 0, "loss_reason"] = "positive_after_costs"
    return frame


def shard_metadata(inventory: pd.DataFrame, max_rows_per_shard: int | None) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    con = duckdb.connect()
    try:
        for _, item in inventory.iterrows():
            shard_index = int(item["shard_index"])
            path = str(item["shard_path"])
            filter_sql = ""
            if max_rows_per_shard is not None:
                filter_sql = f"where local_sequence_id <= {int(max_rows_per_shard)}"
            sql = f"""
            select
                {shard_index}::integer as shard_index,
                any_value(trade_month)::varchar as trade_month,
                any_value(symbol)::varchar as symbol,
                mode(regime_code)::varchar as dominant_regime_code,
                mode(feed_profile)::varchar as dominant_feed_profile,
                count(*)::bigint as bounded_rows,
                count(distinct trade_date)::integer as bounded_trade_dates,
                count(distinct regime_code)::integer as regime_codes_seen,
                count(distinct feed_profile)::integer as feed_profiles_seen,
                avg(case when coalesce(is_market_shock_day, false) then 1.0 else 0.0 end)::double as market_shock_row_fraction,
                avg(case when coalesce(is_symbol_shock, false) then 1.0 else 0.0 end)::double as symbol_shock_row_fraction,
                avg(case when coalesce(is_disconnect_gap, false) then 1.0 else 0.0 end)::double as disconnect_row_fraction,
                avg(case when coalesce(is_out_of_order_injected, false) then 1.0 else 0.0 end)::double as out_of_order_row_fraction
            from read_parquet('{_safe_path(path)}', union_by_name=true)
            {filter_sql}
            """
            rows.append(con.execute(sql).fetchdf().iloc[0].to_dict())
    finally:
        con.close()
    return pd.DataFrame(rows)


def aggregate(frame: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    grouped = (
        frame.groupby(group_cols, dropna=False, sort=True)
        .agg(
            shard_symbol_rows=("net_pnl_inr", "size"),
            symbols=("symbol", "nunique"),
            trade_dates=("trade_date", "nunique"),
            trades=("trades", "sum"),
            net_pnl_inr=("net_pnl_inr", "sum"),
            gross_pnl_proxy_inr=("gross_pnl_proxy_inr", "sum"),
            cost_pnl_drag_proxy_inr=("cost_pnl_drag_proxy_inr", "sum"),
            positive_rows=("positive_after_costs", "sum"),
            mean_precision_cost_clear=("precision_cost_clear", "mean"),
        )
        .reset_index()
    )
    grouped["positive_row_fraction"] = grouped["positive_rows"] / grouped["shard_symbol_rows"].where(grouped["shard_symbol_rows"] != 0, 1)
    grouped["mean_net_pnl_per_trade_inr"] = grouped["net_pnl_inr"] / grouped["trades"].where(grouped["trades"] != 0, 1)
    grouped["cost_drag_to_abs_gross_ratio"] = grouped["cost_pnl_drag_proxy_inr"] / grouped["gross_pnl_proxy_inr"].abs().where(
        grouped["gross_pnl_proxy_inr"].abs() > 0,
        pd.NA,
    )
    return grouped.sort_values(["net_pnl_inr", "trades"], ascending=[False, False], kind="mergesort").reset_index(drop=True)


def concentration(frame: pd.DataFrame) -> pd.DataFrame:
    sorted_rows = frame.sort_values("net_pnl_inr", ascending=False, kind="mergesort").copy()
    total = float(frame["net_pnl_inr"].sum())
    gross_positive = float(frame.loc[frame["net_pnl_inr"] > 0, "net_pnl_inr"].sum())
    gross_negative = float(frame.loc[frame["net_pnl_inr"] < 0, "net_pnl_inr"].sum())
    return pd.DataFrame(
        [
            {
                "metric": "total_net_pnl_inr",
                "value": total,
                "description": "Total Phase61 wider-sweep net P&L",
            },
            {
                "metric": "positive_rows",
                "value": int((frame["net_pnl_inr"] > 0).sum()),
                "description": "Shard-symbol rows positive after costs",
            },
            {
                "metric": "negative_rows",
                "value": int((frame["net_pnl_inr"] < 0).sum()),
                "description": "Shard-symbol rows negative after costs",
            },
            {
                "metric": "positive_net_pnl_inr",
                "value": gross_positive,
                "description": "Sum of positive shard-symbol net P&L",
            },
            {
                "metric": "negative_net_pnl_inr",
                "value": gross_negative,
                "description": "Sum of negative shard-symbol net P&L",
            },
            {
                "metric": "top_5_rows_net_pnl_inr",
                "value": float(sorted_rows.head(5)["net_pnl_inr"].sum()),
                "description": "Net P&L concentration in best five shard-symbol rows",
            },
            {
                "metric": "worst_5_rows_net_pnl_inr",
                "value": float(sorted_rows.tail(5)["net_pnl_inr"].sum()),
                "description": "Net P&L concentration in worst five shard-symbol rows",
            },
        ]
    )


def acceptance_summary(
    enriched: pd.DataFrame,
    symbol_rollup: pd.DataFrame,
    month_rollup: pd.DataFrame,
    regime_rollup: pd.DataFrame,
    feed_rollup: pd.DataFrame,
) -> pd.DataFrame:
    viable_symbols = symbol_rollup[(symbol_rollup["net_pnl_inr"] > 0) & (symbol_rollup["trades"] >= 10)]
    viable_months = month_rollup[(month_rollup["net_pnl_inr"] > 0) & (month_rollup["trades"] >= 50)]
    viable_regimes = regime_rollup[(regime_rollup["net_pnl_inr"] > 0) & (regime_rollup["trades"] >= 50)]
    viable_feeds = feed_rollup[(feed_rollup["net_pnl_inr"] > 0) & (feed_rollup["trades"] >= 50)]
    rows = [
        ("phase62_source_rows", int(len(enriched)), "Phase61 shard-symbol rows diagnosed"),
        ("phase62_total_trades", int(enriched["trades"].sum()), "Total candidate trades diagnosed"),
        ("phase62_total_net_pnl_inr", float(enriched["net_pnl_inr"].sum()), "Total Phase61 wider-sweep net P&L"),
        ("phase62_positive_symbol_rows", int((enriched["net_pnl_inr"] > 0).sum()), "Shard-symbol rows positive after costs"),
        ("phase62_positive_symbol_fraction", float((enriched["net_pnl_inr"] > 0).mean()), "Fraction of shard-symbol rows positive"),
        ("phase62_viable_symbol_count", int(len(viable_symbols)), "Symbols with positive aggregate P&L and at least 10 trades"),
        ("phase62_viable_month_count", int(len(viable_months)), "Trade-month partitions with positive aggregate P&L and at least 50 trades"),
        ("phase62_viable_regime_count", int(len(viable_regimes)), "Dominant regimes with positive aggregate P&L and at least 50 trades"),
        ("phase62_viable_feed_profile_count", int(len(viable_feeds)), "Dominant feed profiles with positive aggregate P&L and at least 50 trades"),
        ("phase62_recommend_regime_symbol_specialization", int(len(viable_symbols) > 0 or len(viable_months) > 0 or len(viable_regimes) > 0), "1 means a narrower specialization deserves a follow-up bounded replay"),
        ("phase62_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha retail intraday cost model"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase62 Regime and Symbol Dependence Diagnostics",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase62 diagnoses why the Phase60 lower-frequency candidate failed the Phase61 wider sweep.",
        "It rolls the wider-sweep P&L up by symbol, month partition, instrument class, dominant regime, feed profile and loss reason.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase62_regime_symbol_diagnostics_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase62(phase61_dir: Path, output_dir: Path, base_dir: Path, max_rows_per_shard: int | None) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    daily, inventory, candidate = load_phase61_inputs(phase61_dir)
    enriched = enrich_with_inventory(daily, inventory)
    metadata = shard_metadata(inventory, max_rows_per_shard)
    enriched = enriched.merge(metadata, on=["shard_index", "symbol"], how="left", suffixes=("", "_metadata"))

    symbol_rollup = aggregate(enriched, ["symbol", "instrument_class"])
    month_rollup = aggregate(enriched, ["trade_month_partition"])
    class_rollup = aggregate(enriched, ["instrument_class"])
    regime_rollup = aggregate(enriched, ["dominant_regime_code"])
    feed_rollup = aggregate(enriched, ["dominant_feed_profile"])
    loss_rollup = aggregate(enriched, ["loss_reason"])
    shock_rollup = aggregate(
        enriched.assign(
            market_shock_bucket=enriched["market_shock_row_fraction"].gt(0).map({True: "market_shock_rows_present", False: "no_market_shock_rows"}),
            symbol_shock_bucket=enriched["symbol_shock_row_fraction"].gt(0).map({True: "symbol_shock_rows_present", False: "no_symbol_shock_rows"}),
        ),
        ["market_shock_bucket", "symbol_shock_bucket"],
    )
    pnl_concentration = concentration(enriched)
    acceptance = acceptance_summary(enriched, symbol_rollup, month_rollup, regime_rollup, feed_rollup)

    enriched.to_csv(output_dir / "phase61_enriched_daily_symbol.csv", index=False)
    metadata.to_csv(output_dir / "phase61_shard_metadata.csv", index=False)
    symbol_rollup.to_csv(output_dir / "symbol_dependence_rollup.csv", index=False)
    month_rollup.to_csv(output_dir / "month_dependence_rollup.csv", index=False)
    class_rollup.to_csv(output_dir / "instrument_class_rollup.csv", index=False)
    regime_rollup.to_csv(output_dir / "regime_dependence_rollup.csv", index=False)
    feed_rollup.to_csv(output_dir / "feed_profile_dependence_rollup.csv", index=False)
    loss_rollup.to_csv(output_dir / "loss_reason_rollup.csv", index=False)
    shock_rollup.to_csv(output_dir / "shock_dependence_rollup.csv", index=False)
    pnl_concentration.to_csv(output_dir / "pnl_concentration_summary.csv", index=False)
    acceptance.to_csv(output_dir / "regime_symbol_acceptance_summary.csv", index=False)

    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Candidate": candidate,
            "Symbol Rollup": symbol_rollup,
            "Month Rollup": month_rollup,
            "Instrument Class Rollup": class_rollup,
            "Regime Rollup": regime_rollup,
            "Feed Profile Rollup": feed_rollup,
            "Loss Reason Rollup": loss_rollup,
            "Shock Rollup": shock_rollup,
            "P&L Concentration": pnl_concentration,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase62_regime_symbol_dependence_diagnostics",
        "phase61_dir": str(phase61_dir),
        "source_rows": int(len(enriched)),
        "recommend_regime_symbol_specialization": int(
            acceptance.loc[acceptance["metric"] == "phase62_recommend_regime_symbol_specialization", "value"].iloc[0]
        ),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase62",
            generated_utc=generated_utc,
            inputs={
                "phase61_daily_symbol": str(phase61_dir / "wider_sweep_daily_symbol.csv"),
                "phase61_inventory": str(phase61_dir / "wider_sweep_file_inventory.csv"),
                "phase61_candidate": str(phase61_dir / "phase60_candidate_replayed.csv"),
            },
            parameters={
                "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_metadata",
                "diagnostic_rollups": "symbol;month;instrument_class;regime;feed_profile;loss_reason;shock",
            },
            outputs={
                "enriched_daily_symbol": str(output_dir / "phase61_enriched_daily_symbol.csv"),
                "shard_metadata": str(output_dir / "phase61_shard_metadata.csv"),
                "symbol_rollup": str(output_dir / "symbol_dependence_rollup.csv"),
                "month_rollup": str(output_dir / "month_dependence_rollup.csv"),
                "class_rollup": str(output_dir / "instrument_class_rollup.csv"),
                "regime_rollup": str(output_dir / "regime_dependence_rollup.csv"),
                "feed_rollup": str(output_dir / "feed_profile_dependence_rollup.csv"),
                "loss_rollup": str(output_dir / "loss_reason_rollup.csv"),
                "shock_rollup": str(output_dir / "shock_dependence_rollup.csv"),
                "concentration": str(output_dir / "pnl_concentration_summary.csv"),
                "acceptance_summary": str(output_dir / "regime_symbol_acceptance_summary.csv"),
                "report": str(output_dir / "phase62_regime_symbol_diagnostics_report.md"),
                "manifest": str(output_dir / "phase62_regime_symbol_diagnostics_manifest.json"),
            },
            random_seed="none_deterministic_phase61_rollup",
            scenario_ids="phase62_phase61_wider_sweep_diagnostics",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase62_rollup_only_not_new_execution",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase62_regime_symbol_diagnostics_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnose symbol/regime dependence in Phase61 wider sweep outputs.")
    parser.add_argument("--phase61-dir", type=Path, default=DEFAULT_PHASE61_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--max-rows-per-shard", type=int, default=250_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase62(args.phase61_dir, args.output_dir, args.base_dir, args.max_rows_per_shard)


if __name__ == "__main__":
    main()
