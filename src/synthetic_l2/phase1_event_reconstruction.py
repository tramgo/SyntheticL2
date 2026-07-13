from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


def load_deltas(delta_dir: Path) -> pd.DataFrame:
    files = sorted(delta_dir.glob("symbol=*/received_tick_deltas.parquet"))
    if not files:
        raise FileNotFoundError(f"No received-tick delta parquet files under {delta_dir}")
    frames = [pd.read_parquet(path) for path in files]
    return pd.concat(frames, ignore_index=True)


def classify_events(deltas: pd.DataFrame) -> pd.DataFrame:
    out = deltas[
        [
            "trading_date",
            "event_ts_receive",
            "event_ts_receive_ms",
            "symbol",
            "sequence_local",
            "book_valid",
            "elapsed_ms",
            "cum_volume_increment",
            "price_change",
            "mid_change",
            "mlofi_qty",
            "inferred_depth_withdrawal",
            "inferred_depth_replenishment",
            "aggressor_side_inference",
            "stale_gap_gt_5s",
            "stale_gap_gt_15s",
        ]
    ].copy()
    volume_inc = out["cum_volume_increment"].fillna(0) > 0
    buy_pressure = out["aggressor_side_inference"].eq("buy_pressure_weak")
    sell_pressure = out["aggressor_side_inference"].eq("sell_pressure_weak")
    withdrawal = out["inferred_depth_withdrawal"].fillna(False).astype(bool)
    replenishment = out["inferred_depth_replenishment"].fillna(False).astype(bool)
    stale_or_invalid = out["stale_gap_gt_15s"].fillna(False).astype(bool) | ~out["book_valid"].fillna(False).astype(bool)

    out["trade_side_classification"] = np.select(
        [
            volume_inc & buy_pressure,
            volume_inc & sell_pressure,
            volume_inc,
        ],
        [
            "buy_pressure_weak",
            "sell_pressure_weak",
            "unknown_trade_side",
        ],
        default="no_volume_increment",
    )
    out["depth_event_classification"] = np.select(
        [
            withdrawal & replenishment,
            withdrawal,
            replenishment,
        ],
        [
            "mixed_withdrawal_and_replenishment",
            "withdrawal_or_cancel_proxy",
            "addition_or_replenishment_proxy",
        ],
        default="no_visible_depth_qty_event",
    )
    out["queue_event_proxy"] = np.select(
        [
            volume_inc & withdrawal,
            volume_inc & replenishment,
            replenishment,
            withdrawal,
        ],
        [
            "consume_visible_depth_proxy",
            "trade_plus_replenishment_proxy",
            "add_or_replenish_visible_depth_proxy",
            "cancel_or_withdraw_visible_depth_proxy",
        ],
        default="no_visible_queue_event_proxy",
    )
    out["event_inference_confidence"] = np.select(
        [
            stale_or_invalid,
            volume_inc & (buy_pressure | sell_pressure) & (withdrawal ^ replenishment),
            volume_inc & (buy_pressure | sell_pressure),
            withdrawal ^ replenishment,
        ],
        [
            "low_stale_or_invalid_book",
            "medium_trade_and_one_sided_depth_move",
            "medium_trade_side_from_price_move",
            "medium_one_sided_depth_move",
        ],
        default="low_or_ambiguous_market_by_price_delta",
    )
    out["direct_exchange_observation"] = False
    out["inference_limit"] = "top_five_market_by_price_state_delta_not_order_identity"
    return out


def event_summary(events: pd.DataFrame) -> pd.DataFrame:
    return (
        events.groupby("symbol", sort=True)
        .agg(
            rows=("symbol", "count"),
            volume_increment_rows=("cum_volume_increment", lambda values: int((values.fillna(0) > 0).sum())),
            buy_pressure_rows=("trade_side_classification", lambda values: int((values == "buy_pressure_weak").sum())),
            sell_pressure_rows=("trade_side_classification", lambda values: int((values == "sell_pressure_weak").sum())),
            unknown_trade_side_rows=("trade_side_classification", lambda values: int((values == "unknown_trade_side").sum())),
            withdrawal_proxy_rows=("depth_event_classification", lambda values: int(values.astype(str).str.contains("withdrawal").sum())),
            replenishment_proxy_rows=("depth_event_classification", lambda values: int(values.astype(str).str.contains("replenishment").sum())),
            consume_visible_depth_proxy_rows=("queue_event_proxy", lambda values: int((values == "consume_visible_depth_proxy").sum())),
            add_or_replenish_proxy_rows=("queue_event_proxy", lambda values: int((values == "add_or_replenish_visible_depth_proxy").sum())),
            cancel_or_withdraw_proxy_rows=("queue_event_proxy", lambda values: int((values == "cancel_or_withdraw_visible_depth_proxy").sum())),
            medium_confidence_rows=("event_inference_confidence", lambda values: int(values.astype(str).str.startswith("medium").sum())),
            low_confidence_rows=("event_inference_confidence", lambda values: int(values.astype(str).str.startswith("low").sum())),
            stale_or_invalid_low_confidence_rows=("event_inference_confidence", lambda values: int((values == "low_stale_or_invalid_book").sum())),
        )
        .reset_index()
    )


def quality_summary(events: pd.DataFrame) -> pd.DataFrame:
    total_rows = int(len(events))
    volume_rows = int((events["cum_volume_increment"].fillna(0) > 0).sum())
    medium_rows = int(events["event_inference_confidence"].astype(str).str.startswith("medium").sum())
    rows = [
        {
            "inference_area": "trade_classification",
            "eligible_rows": volume_rows,
            "classified_rows": int(events["trade_side_classification"].isin(["buy_pressure_weak", "sell_pressure_weak"]).sum()),
            "ambiguous_rows": int((events["trade_side_classification"] == "unknown_trade_side").sum()),
            "direct_exchange_observation": False,
            "confidence_basis": "volume increment plus last-price direction",
            "acceptance_grade": False,
            "limitation": "Aggressor side is weak because the feed does not expose trade prints with aggressor flags.",
        },
        {
            "inference_area": "replenishment",
            "eligible_rows": total_rows,
            "classified_rows": int(events["depth_event_classification"].astype(str).str.contains("replenishment").sum()),
            "ambiguous_rows": int((events["depth_event_classification"] == "mixed_withdrawal_and_replenishment").sum()),
            "direct_exchange_observation": False,
            "confidence_basis": "positive visible L1-L5 quantity deltas between received ticks",
            "acceptance_grade": False,
            "limitation": "Cannot separate new passive orders from revealed/shifted liquidity or book-level aggregation effects.",
        },
        {
            "inference_area": "add_cancel_consume",
            "eligible_rows": total_rows,
            "classified_rows": int((events["queue_event_proxy"] != "no_visible_queue_event_proxy").sum()),
            "ambiguous_rows": int((events["queue_event_proxy"] == "trade_plus_replenishment_proxy").sum()),
            "direct_exchange_observation": False,
            "confidence_basis": "visible quantity deltas combined with volume increments",
            "acceptance_grade": False,
            "limitation": "Cannot identify individual orders, queue priority, hidden liquidity or exact cancel/trade causality.",
        },
        {
            "inference_area": "overall_confidence",
            "eligible_rows": total_rows,
            "classified_rows": medium_rows,
            "ambiguous_rows": total_rows - medium_rows,
            "direct_exchange_observation": False,
            "confidence_basis": "book validity, stale-gap labels, trade-side and one-sided depth movement",
            "acceptance_grade": False,
            "limitation": "All event labels are received-market-by-price inference labels, not exchange event truth.",
        },
    ]
    return pd.DataFrame(rows)


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    text = frame.copy()
    for column in text.columns:
        text[column] = text[column].map(lambda value: "" if pd.isna(value) else str(value))
    headers = [str(column) for column in text.columns]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |" for row in text.values.tolist())
    return "\n".join(lines)


def write_report(output_dir: Path, summary: pd.DataFrame, quality: pd.DataFrame) -> None:
    totals = {
        "symbols": int(summary["symbol"].nunique()),
        "rows": int(summary["rows"].sum()),
        "volume_increment_rows": int(summary["volume_increment_rows"].sum()),
        "classified_trade_side_rows": int(summary["buy_pressure_rows"].sum() + summary["sell_pressure_rows"].sum()),
        "replenishment_proxy_rows": int(summary["replenishment_proxy_rows"].sum()),
        "queue_event_proxy_rows": int(
            summary["consume_visible_depth_proxy_rows"].sum()
            + summary["add_or_replenish_proxy_rows"].sum()
            + summary["cancel_or_withdraw_proxy_rows"].sum()
        ),
        "medium_confidence_rows": int(summary["medium_confidence_rows"].sum()),
        "low_confidence_rows": int(summary["low_confidence_rows"].sum()),
    }
    lines = [
        "# Phase 1 Event Reconstruction Inference Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This companion artifact converts received-tick deltas into explicit event-inference labels.",
        "It is intentionally not exchange-order truth: Zerodha top-five market-by-price snapshots cannot identify individual orders, hidden liquidity, exact queue position or true passive fills.",
        "",
        "## Totals",
        "",
        *(f"- {key}: {value}" for key, value in totals.items()),
        "",
        "## Inference Quality",
        "",
        _markdown_table(quality),
        "",
        "## Symbol Summary",
        "",
        _markdown_table(summary),
        "",
    ]
    (output_dir / "event_reconstruction_report.md").write_text("\n".join(lines), encoding="utf-8")


def run(delta_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    deltas = load_deltas(delta_dir)
    events = classify_events(deltas)
    summary = event_summary(events)
    quality = quality_summary(events)
    summary.to_csv(output_dir / "event_reconstruction_summary.csv", index=False)
    quality.to_csv(output_dir / "event_reconstruction_quality.csv", index=False)
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "delta_dir": str(delta_dir),
        "rows_evaluated": int(len(events)),
        "symbols": int(events["symbol"].nunique()),
        "classified_trade_side_rows": int(events["trade_side_classification"].isin(["buy_pressure_weak", "sell_pressure_weak"]).sum()),
        "replenishment_proxy_rows": int(events["depth_event_classification"].astype(str).str.contains("replenishment").sum()),
        "queue_event_proxy_rows": int((events["queue_event_proxy"] != "no_visible_queue_event_proxy").sum()),
        "direct_exchange_observation": False,
        "acceptance_grade": False,
        "scope": "received_tick_market_by_price_event_inference_not_exchange_truth",
    }
    (output_dir / "event_reconstruction_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, summary, quality)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build received-tick event reconstruction inference summaries from Phase 1 deltas.")
    parser.add_argument("--delta-dir", type=Path, default=Path("outputs/phase1/received_tick_deltas_by_symbol"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase1/event_reconstruction"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run(args.delta_dir, args.output_dir)


if __name__ == "__main__":
    main()
