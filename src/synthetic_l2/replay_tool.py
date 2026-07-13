from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


TIER_CONFIG = {
    "tier_a": {
        "path": Path("outputs/phase9/tier_a/raw_synthetic_events.parquet"),
        "order_columns": ["trade_date", "feed_profile", "quarter_profile", "symbol", "event_ts", "source_sequence", "event_id"],
        "optional_filters": ["trade_date", "feed_profile", "quarter_profile", "symbol", "event_kind"],
    },
    "tier_b": {
        "path": Path("outputs/phase9/tier_b/compact_l2_state.parquet"),
        "order_columns": ["trade_date", "feed_profile", "quarter_profile", "symbol", "bar_index", "collector_received_utc_ms", "receive_sequence", "source_sequence"],
        "optional_filters": ["trade_date", "feed_profile", "quarter_profile", "symbol", "regime_code"],
    },
    "tier_c": {
        "path": Path("outputs/phase9/tier_c/features_5m.parquet"),
        "order_columns": ["trade_date", "feed_profile", "quarter_profile", "symbol", "bar_index", "collector_received_utc_ms"],
        "optional_filters": ["trade_date", "feed_profile", "quarter_profile", "symbol", "regime_code"],
    },
}


def _apply_filters(frame: pd.DataFrame, filters: dict[str, str | None], allowed_filters: Iterable[str]) -> pd.DataFrame:
    out = frame
    for column in allowed_filters:
        value = filters.get(column)
        if value is not None and column in out.columns:
            out = out[out[column].astype(str) == str(value)]
    return out


def _available_order_columns(frame: pd.DataFrame, configured_order: list[str]) -> list[str]:
    return [column for column in configured_order if column in frame.columns]


def _hash_frame(frame: pd.DataFrame) -> str:
    csv_bytes = frame.to_csv(index=False).encode("utf-8")
    return hashlib.sha256(csv_bytes).hexdigest()


def replay_tier(
    tier: str,
    output_path: Path | None = None,
    *,
    limit: int | None = None,
    filters: dict[str, str | None] | None = None,
    columns: list[str] | None = None,
) -> tuple[pd.DataFrame, dict]:
    if tier not in TIER_CONFIG:
        raise ValueError(f"Unknown tier {tier!r}; expected one of {sorted(TIER_CONFIG)}")
    config = TIER_CONFIG[tier]
    source_path = config["path"]
    if not source_path.exists():
        raise FileNotFoundError(source_path)
    frame = pd.read_parquet(source_path, columns=columns)
    filters = filters or {}
    frame = _apply_filters(frame, filters, config["optional_filters"])
    order_columns = _available_order_columns(frame, config["order_columns"])
    if order_columns:
        frame = frame.sort_values(order_columns, kind="mergesort")
    if limit is not None:
        frame = frame.head(limit)
    frame = frame.reset_index(drop=True)

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        pq.write_table(pa.Table.from_pandas(frame, preserve_index=False), output_path, compression="zstd")

    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "tier": tier,
        "source_path": str(source_path),
        "output_path": str(output_path) if output_path is not None else None,
        "rows": int(len(frame)),
        "columns": list(frame.columns),
        "order_columns": order_columns,
        "filters": {key: value for key, value in filters.items() if value is not None},
        "limit": limit,
        "sha256_csv_ordered_rows": _hash_frame(frame),
        "deterministic_ordering": bool(order_columns),
    }
    return frame, manifest


def validate_replay(output_dir: Path, sample_limit: int = 5000) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifests = []
    summaries = []
    for tier in TIER_CONFIG:
        output_path = output_dir / f"{tier}_replay_sample.parquet"
        frame, manifest = replay_tier(tier, output_path, limit=sample_limit)
        manifests.append(manifest)
        summaries.append(
            {
                "tier": tier,
                "source_path": manifest["source_path"],
                "sample_path": str(output_path),
                "sample_rows": manifest["rows"],
                "deterministic_ordering": manifest["deterministic_ordering"],
                "order_columns": ";".join(manifest["order_columns"]),
                "sha256_csv_ordered_rows": manifest["sha256_csv_ordered_rows"],
            }
        )

    summary = pd.DataFrame(summaries)
    summary.to_csv(output_dir / "replay_validation_summary.csv", index=False)
    (output_dir / "replay_validation_manifest.json").write_text(
        json.dumps(
            {
                "generated_utc": datetime.now(timezone.utc).isoformat(),
                "sample_limit_per_tier": sample_limit,
                "tiers": manifests,
                "all_tiers_have_deterministic_ordering": bool(summary["deterministic_ordering"].all()),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Replay Tool Validation Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This validates deterministic replay ordering for Phase 9 Tier A, Tier B and Tier C Parquet products.",
        "The replay tool supports tier selection, symbol/date/profile filters, column projection, row limits and ordered Parquet export.",
        "",
        "## Validation Summary",
        "",
        "| Tier | Sample rows | Deterministic ordering | Order columns | SHA256 |",
        "| --- | ---: | --- | --- | --- |",
    ]
    for row in summaries:
        lines.append(
            f"| {row['tier']} | {row['sample_rows']} | {row['deterministic_ordering']} | {row['order_columns']} | {row['sha256_csv_ordered_rows']} |"
        )
    (output_dir / "replay_validation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replay deterministic Phase 9 synthetic L2 products.")
    parser.add_argument("--tier", choices=sorted(TIER_CONFIG), help="Replay a single tier. If omitted, validate all tiers.")
    parser.add_argument("--output", type=Path, help="Output Parquet path for a single-tier replay.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/replay"))
    parser.add_argument("--limit", type=int, default=5000)
    parser.add_argument("--trade-date")
    parser.add_argument("--feed-profile")
    parser.add_argument("--quarter-profile")
    parser.add_argument("--symbol")
    parser.add_argument("--regime-code")
    parser.add_argument("--event-kind")
    parser.add_argument("--columns", help="Comma-separated column projection.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.tier:
        filters = {
            "trade_date": args.trade_date,
            "feed_profile": args.feed_profile,
            "quarter_profile": args.quarter_profile,
            "symbol": args.symbol,
            "regime_code": args.regime_code,
            "event_kind": args.event_kind,
        }
        columns = [column.strip() for column in args.columns.split(",")] if args.columns else None
        output = args.output or (args.output_dir / f"{args.tier}_replay.parquet")
        _, manifest = replay_tier(args.tier, output, limit=args.limit, filters=filters, columns=columns)
        output.with_suffix(".manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    else:
        validate_replay(args.output_dir, sample_limit=args.limit)


if __name__ == "__main__":
    main()
