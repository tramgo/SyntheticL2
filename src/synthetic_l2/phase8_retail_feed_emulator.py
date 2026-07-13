from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from synthetic_l2.reproducibility import reproducibility_fields


FEED_PROFILES = {
    "ideal_research": {
        "median_latency_ms": 0,
        "jitter_ms": 0,
        "tail_probability": 0.0,
        "tail_latency_ms": 0,
        "drop_probability": 0.0,
        "duplicate_probability": 0.0,
        "batch_ms": 0,
        "out_of_order_probability": 0.0,
        "disconnect_probability": 0.0,
    },
    "good_retail": {
        "median_latency_ms": 75,
        "jitter_ms": 35,
        "tail_probability": 0.01,
        "tail_latency_ms": 400,
        "drop_probability": 0.001,
        "duplicate_probability": 0.001,
        "batch_ms": 50,
        "out_of_order_probability": 0.001,
        "disconnect_probability": 0.0,
    },
    "normal_retail": {
        "median_latency_ms": 220,
        "jitter_ms": 120,
        "tail_probability": 0.03,
        "tail_latency_ms": 900,
        "drop_probability": 0.003,
        "duplicate_probability": 0.002,
        "batch_ms": 100,
        "out_of_order_probability": 0.003,
        "disconnect_probability": 0.0,
    },
    "stressed_retail": {
        "median_latency_ms": 500,
        "jitter_ms": 280,
        "tail_probability": 0.08,
        "tail_latency_ms": 2500,
        "drop_probability": 0.01,
        "duplicate_probability": 0.006,
        "batch_ms": 250,
        "out_of_order_probability": 0.01,
        "disconnect_probability": 0.002,
    },
    "disconnect_scenario": {
        "median_latency_ms": 350,
        "jitter_ms": 220,
        "tail_probability": 0.12,
        "tail_latency_ms": 5000,
        "drop_probability": 0.015,
        "duplicate_probability": 0.004,
        "batch_ms": 500,
        "out_of_order_probability": 0.015,
        "disconnect_probability": 0.008,
    },
}


def load_inputs(phase6_dir: Path, phase7_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    states = pq.read_table(phase6_dir / "l2_book_states_5m.parquet").to_pandas()
    shocks = pd.read_csv(phase7_dir / "shock_library.csv")
    return states, shocks


def build_shock_day_index(shocks: pd.DataFrame) -> set[tuple[str, int]]:
    active = shocks[shocks["variant"] != "no_shock"]
    return set(zip(active["quarter_profile"], active["scenario_day"].astype(int)))


def stable_profile_seed(profile_name: str) -> int:
    return sum((idx + 1) * ord(ch) for idx, ch in enumerate(profile_name)) % (2**32)


def emulate_profile(states: pd.DataFrame, profile_name: str, profile: dict, shock_days: set[tuple[str, int]]) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(stable_profile_seed(profile_name))
    feed = states.copy()
    feed["source_sequence"] = np.arange(len(feed), dtype=np.int64)
    feed["feed_profile"] = profile_name
    feed["exchange_ts"] = pd.to_datetime(feed["bar_start"])
    feed["exchange_ts_ms"] = (feed["exchange_ts"].astype("int64") // 1_000_000).astype("int64")
    feed["is_shock_day_from_library"] = [
        (qp, int(day)) in shock_days for qp, day in zip(feed["quarter_profile"], feed["scenario_day"])
    ]

    shock_mult = np.where(feed["is_shock_day_from_library"].to_numpy(), 1.65, 1.0)
    latency = rng.normal(profile["median_latency_ms"], profile["jitter_ms"], len(feed))
    latency = np.maximum(0, latency)
    tail_mask = rng.random(len(feed)) < (profile["tail_probability"] * shock_mult)
    latency[tail_mask] += rng.exponential(profile["tail_latency_ms"], tail_mask.sum())

    disconnect_mask = rng.random(len(feed)) < (profile["disconnect_probability"] * shock_mult)
    if disconnect_mask.any():
        latency[disconnect_mask] += rng.integers(2_000, 30_000, disconnect_mask.sum())

    receive_ms = feed["exchange_ts_ms"].to_numpy() + latency.astype("int64")
    batch_ms = int(profile["batch_ms"])
    if batch_ms > 0:
        receive_ms = (receive_ms // batch_ms) * batch_ms

    out_of_order_mask = rng.random(len(feed)) < (profile["out_of_order_probability"] * shock_mult)
    receive_ms[out_of_order_mask] -= rng.integers(1, max(2, batch_ms + 250), out_of_order_mask.sum())
    feed["collector_received_utc_ms"] = receive_ms
    feed["collector_received_utc"] = pd.to_datetime(feed["collector_received_utc_ms"], unit="ms", utc=True).astype(str)
    feed["latency_ms"] = feed["collector_received_utc_ms"] - feed["exchange_ts_ms"]
    feed["is_disconnect_gap"] = disconnect_mask
    feed["is_out_of_order_injected"] = out_of_order_mask
    feed["is_duplicate"] = False
    feed["is_dropped_in_profile"] = False

    drop_probability = profile["drop_probability"] * shock_mult
    drop_mask = rng.random(len(feed)) < drop_probability
    kept = feed.loc[~drop_mask].copy()
    dropped = feed.loc[drop_mask, ["feed_profile", "quarter_profile", "scenario_day", "trade_date", "bar_index", "symbol", "source_sequence"]].copy()
    if len(dropped):
        dropped["drop_reason"] = np.where(
            dropped[["quarter_profile", "scenario_day"]].apply(tuple, axis=1).isin(shock_days),
            "shock_day_drop",
            "random_profile_drop",
        )

    duplicate_mask = rng.random(len(kept)) < (profile["duplicate_probability"] * np.where(kept["is_shock_day_from_library"], 1.5, 1.0))
    duplicates = kept.loc[duplicate_mask].copy()
    if len(duplicates):
        duplicates["is_duplicate"] = True
        duplicates["collector_received_utc_ms"] += rng.integers(1, 250, len(duplicates))
        duplicates["collector_received_utc"] = pd.to_datetime(duplicates["collector_received_utc_ms"], unit="ms", utc=True).astype(str)
        duplicates["latency_ms"] = duplicates["collector_received_utc_ms"] - duplicates["exchange_ts_ms"]
        duplicates["is_out_of_order_injected"] = False

    observed = pd.concat([kept, duplicates], ignore_index=True)
    observed = observed.sort_values(["collector_received_utc_ms", "symbol", "source_sequence"], kind="mergesort").reset_index(drop=True)
    observed["receive_sequence"] = np.arange(len(observed), dtype=np.int64)
    observed["receive_order_violation"] = observed.groupby("symbol")["collector_received_utc_ms"].diff().fillna(0) < 0
    return observed, dropped


def validate_feed(observed: pd.DataFrame, dropped: pd.DataFrame, source_rows: int) -> pd.DataFrame:
    rows = []
    for profile, group in observed.groupby("feed_profile", sort=True):
        drop_count = int((dropped["feed_profile"] == profile).sum()) if len(dropped) else 0
        duplicate_count = int(group["is_duplicate"].sum())
        source_kept = int(group.loc[~group["is_duplicate"], "source_sequence"].nunique())
        rows.append(
            {
                "feed_profile": profile,
                "observed_rows": int(len(group)),
                "source_rows": source_rows,
                "source_kept_rows": source_kept,
                "dropped_rows": drop_count,
                "duplicate_rows": duplicate_count,
                "drop_fraction": drop_count / source_rows,
                "duplicate_fraction": duplicate_count / max(source_kept, 1),
                "median_latency_ms": float(group["latency_ms"].median()),
                "p95_latency_ms": float(group["latency_ms"].quantile(0.95)),
                "p99_latency_ms": float(group["latency_ms"].quantile(0.99)),
                "disconnect_gap_rows": int(group["is_disconnect_gap"].sum()),
                "out_of_order_injected_rows": int(group["is_out_of_order_injected"].sum()),
                "receive_order_violation_rows": int(group["receive_order_violation"].sum()),
                "symbols": int(group["symbol"].nunique()),
            }
        )
    return pd.DataFrame(rows)


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    text_frame = frame.copy()
    for column in text_frame.columns:
        text_frame[column] = text_frame[column].map(lambda value: "" if pd.isna(value) else str(value))
    headers = [str(column) for column in text_frame.columns]
    rows = text_frame.values.tolist()
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def write_report(output_dir: Path, validation: pd.DataFrame) -> None:
    lines = [
        "# Phase 8 Retail Feed Emulator Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase emulates retail receive-feed effects over synthetic L2 book states.",
        "Latency profiles are test profiles, not measured Zerodha production latencies.",
        "",
        "## Feed Profile Validation",
        "",
        _markdown_table(validation),
        "",
        "## Outputs",
        "",
        "- `retail_feed_observations.parquet`",
        "- `retail_feed_dropped_events.csv`",
        "- `feed_profile_summary.csv`",
        "- `retail_feed_manifest.json`",
        "",
    ]
    (output_dir / "phase8_retail_feed_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase8(phase6_dir: Path, phase7_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    states, shocks = load_inputs(phase6_dir, phase7_dir)
    shock_days = build_shock_day_index(shocks)
    observed_parts = []
    dropped_parts = []
    for profile_name, profile in FEED_PROFILES.items():
        print(f"[phase8] emulating {profile_name}", flush=True)
        observed, dropped = emulate_profile(states, profile_name, profile, shock_days)
        observed_parts.append(observed)
        dropped_parts.append(dropped)
    observed_all = pd.concat(observed_parts, ignore_index=True)
    dropped_all = pd.concat(dropped_parts, ignore_index=True) if dropped_parts else pd.DataFrame()
    validation = validate_feed(observed_all, dropped_all, len(states))

    pq.write_table(pa.Table.from_pandas(observed_all, preserve_index=False), output_dir / "retail_feed_observations.parquet", compression="zstd")
    dropped_all.to_csv(output_dir / "retail_feed_dropped_events.csv", index=False)
    validation.to_csv(output_dir / "feed_profile_summary.csv", index=False)
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "phase6_dir": str(phase6_dir),
        "phase7_dir": str(phase7_dir),
        "source_rows_per_profile": int(len(states)),
        "profiles": sorted(FEED_PROFILES),
        "validation": validation.to_dict(orient="records"),
        "evidence_scope": "synthetic_retail_feed_test_profiles",
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase8",
            generated_utc=generated_utc,
            inputs={"phase6_dir": str(phase6_dir), "phase7_dir": str(phase7_dir)},
            parameters={
                "feed_profiles": FEED_PROFILES,
                "stable_profile_seeds": {name: stable_profile_seed(name) for name in FEED_PROFILES},
            },
            outputs={
                "retail_feed_observations": str(output_dir / "retail_feed_observations.parquet"),
                "retail_feed_dropped_events": str(output_dir / "retail_feed_dropped_events.csv"),
                "feed_profile_summary": str(output_dir / "feed_profile_summary.csv"),
                "report": str(output_dir / "phase8_retail_feed_report.md"),
            },
            random_seed={name: stable_profile_seed(name) for name in FEED_PROFILES},
            scenario_ids="outputs/phase4/scenario_calendar.csv_via_phase6_phase7",
            cost_model_version="not_applicable_no_execution_costs",
            latency_model_version="phase8_feed_profiles_v1",
        )
    )
    (output_dir / "retail_feed_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, validation)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Phase 8 synthetic retail-feed observations.")
    parser.add_argument("--phase6-dir", type=Path, default=Path("outputs/phase6"))
    parser.add_argument("--phase7-dir", type=Path, default=Path("outputs/phase7"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase8"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase8(args.phase6_dir, args.phase7_dir, args.output_dir)


if __name__ == "__main__":
    main()
