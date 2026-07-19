from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase95_real_anchor_panel_contract import EXPECTED_SYMBOLS
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_DENSE_ROOT = Path("raw_synthetic_l2_dense_full_year")
DEFAULT_OUTPUT_DIR = Path("outputs/phase120")
DEFAULT_PHASE66_DIR = Path("outputs/phase66")
DEFAULT_PHASE68_DIR = Path("outputs/phase68")
DEFAULT_PHASE69_DIR = Path("outputs/phase69")
DEFAULT_PHASE119_DIR = Path("outputs/phase119")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def read_metric_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["metric", "value", "description"])
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    value = rows.iloc[0]
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def path_parts(path_text: str) -> tuple[str, str]:
    parts = Path(path_text).parts
    month = ""
    symbol = ""
    for part in parts:
        if part.startswith("trade_month="):
            month = part.split("=", 1)[1]
        if part.startswith("symbol="):
            symbol = part.split("=", 1)[1]
    return month, symbol


def build_dense_shard_universe(base_dir: Path, dense_root: Path) -> pd.DataFrame:
    root = base_dir / dense_root
    files = sorted(root.glob("trade_month=*/symbol=*/part-00000.parquet"))
    rows = []
    for index, path in enumerate(files, start=1):
        month, symbol = path_parts(str(path.relative_to(base_dir)))
        rows.append(
            {
                "sorted_shard_index": index,
                "shard_path": str(path.relative_to(base_dir)),
                "trade_month": month,
                "symbol": symbol,
                "is_expected_symbol": symbol in EXPECTED_SYMBOLS,
            }
        )
    return pd.DataFrame(rows)


def inventory_coverage(inventory: pd.DataFrame, label_source: str) -> pd.DataFrame:
    if inventory.empty or "shard_path" not in inventory.columns:
        return pd.DataFrame(columns=["label_source", "shard_path", "trade_month", "symbol"])
    rows = []
    for item in inventory["shard_path"].astype(str).unique():
        month, symbol = path_parts(item)
        rows.append({"label_source": label_source, "shard_path": item, "trade_month": month, "symbol": symbol})
    return pd.DataFrame(rows)


def build_current_label_coverage(base_dir: Path, phase66_dir: Path, phase68_dir: Path, phase69_dir: Path) -> pd.DataFrame:
    frames = [
        inventory_coverage(read_csv(base_dir / phase66_dir / "passive_label_file_inventory.csv"), "phase66_adverse_selection"),
        inventory_coverage(read_csv(base_dir / phase68_dir / "replenishment_label_file_inventory.csv"), "phase68_replenishment"),
        inventory_coverage(read_csv(base_dir / phase69_dir / "spread_transition_file_inventory.csv"), "phase69_spread_transition"),
    ]
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def build_coverage_summary(universe: pd.DataFrame, coverage: pd.DataFrame, phase119: pd.DataFrame) -> pd.DataFrame:
    universe_months = int(universe["trade_month"].nunique()) if not universe.empty else 0
    universe_symbols = int(universe["symbol"].nunique()) if not universe.empty else 0
    current_months = int(coverage["trade_month"].nunique()) if not coverage.empty else 0
    current_symbols = int(coverage["symbol"].nunique()) if not coverage.empty else 0
    phase119_max_symbols = as_int(metric_value(phase119, "phase119_max_candidate_symbols"))
    phase119_max_dates = as_int(metric_value(phase119, "phase119_max_candidate_trade_dates"))
    rows = [
        ("phase120_dense_shard_rows", int(len(universe)), "Dense full-year symbol/month parquet shards available"),
        ("phase120_dense_months", universe_months, "Distinct dense trade_month partitions available"),
        ("phase120_dense_symbols", universe_symbols, "Distinct dense symbols available"),
        ("phase120_current_label_source_rows", int(len(coverage)), "Current passive label inventory rows across Phase66/68/69"),
        ("phase120_current_label_months", current_months, "Distinct trade_month partitions already labeled by passive label stages"),
        ("phase120_current_label_symbols", current_symbols, "Distinct symbols already labeled by passive label stages"),
        ("phase120_phase119_max_joined_symbols", phase119_max_symbols, "Max symbols in Phase119 joined candidates"),
        ("phase120_phase119_max_joined_trade_dates", phase119_max_dates, "Max trade dates in Phase119 joined candidates"),
        ("phase120_label_breadth_gap_symbols", max(0, 20 - phase119_max_symbols), "Additional joined-candidate symbol breadth needed for Phase119 gate"),
        ("phase120_label_breadth_gap_trade_dates", max(0, 4 - phase119_max_dates), "Additional joined-candidate trade-date breadth needed for Phase119 gate"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def build_stage_plan(universe: pd.DataFrame) -> pd.DataFrame:
    shard_count = int(len(universe))
    stages = [
        {
            "stage_id": "P120_LABEL_STAGE_01_MIN_BREADTH",
            "limit_shards": min(128, shard_count),
            "expected_months": "2026-01|2026-02|2026-03|2026-04",
            "purpose": "Expand passive labels from one month to four months across the 32-symbol universe.",
        },
        {
            "stage_id": "P120_LABEL_STAGE_02_TRAIN_HALF",
            "limit_shards": min(192, shard_count),
            "expected_months": "2026-01|2026-02|2026-03|2026-04|2026-05|2026-06",
            "purpose": "Cover the train half of the synthetic year for pre-replay label stability.",
        },
        {
            "stage_id": "P120_LABEL_STAGE_03_FULL_YEAR_LABELS",
            "limit_shards": shard_count,
            "expected_months": "2026-01..2026-12",
            "purpose": "Full-year label-only coverage if Stage 01/02 improve adverse-selection and breadth gates.",
        },
    ]
    rows = []
    for stage in stages:
        limit = int(stage["limit_shards"])
        subset = universe.sort_values("sorted_shard_index").head(limit) if not universe.empty else pd.DataFrame()
        rows.append(
            {
                **stage,
                "expected_symbols": int(subset["symbol"].nunique()) if not subset.empty else 0,
                "expected_trade_months_from_manifest": int(subset["trade_month"].nunique()) if not subset.empty else 0,
                "phase66_command": f"python scripts/run_phase66_passive_adverse_selection_labels.py --limit-shards {limit} --output-dir outputs/phase120/{stage['stage_id']}/phase66",
                "phase68_command": f"python scripts/run_phase68_replenishment_after_touch_labels.py --limit-shards {limit} --output-dir outputs/phase120/{stage['stage_id']}/phase68",
                "phase69_command": f"python scripts/run_phase69_spread_transition_labels.py --limit-shards {limit} --output-dir outputs/phase120/{stage['stage_id']}/phase69",
                "phase119_command_after_labels": (
                    "python scripts/run_phase119_richer_passive_label_builder.py "
                    f"--phase66-dir outputs/phase120/{stage['stage_id']}/phase66 "
                    f"--phase68-dir outputs/phase120/{stage['stage_id']}/phase68 "
                    f"--phase69-dir outputs/phase120/{stage['stage_id']}/phase69 "
                    f"--output-dir outputs/phase120/{stage['stage_id']}/phase119"
                ),
                "run_now_recommended": stage["stage_id"] == "P120_LABEL_STAGE_01_MIN_BREADTH",
            }
        )
    return pd.DataFrame(rows)


def build_month_symbol_targets(universe: pd.DataFrame, coverage: pd.DataFrame) -> pd.DataFrame:
    if universe.empty:
        return pd.DataFrame()
    labeled = set()
    if not coverage.empty:
        labeled = set(zip(coverage["trade_month"].astype(str), coverage["symbol"].astype(str)))
    rows = []
    for item in universe.to_dict("records"):
        key = (str(item["trade_month"]), str(item["symbol"]))
        rows.append(
            {
                "sorted_shard_index": item["sorted_shard_index"],
                "trade_month": item["trade_month"],
                "symbol": item["symbol"],
                "shard_path": item["shard_path"],
                "already_labeled_by_any_passive_stage": key in labeled,
                "target_priority": 2 if key in labeled else 1,
            }
        )
    return pd.DataFrame(rows).sort_values(["target_priority", "sorted_shard_index"], kind="mergesort")


def build_acceptance_summary(summary: pd.DataFrame, stage_plan: pd.DataFrame) -> pd.DataFrame:
    metric = {str(row["metric"]): row["value"] for row in summary.to_dict("records")}
    current_months = as_int(metric.get("phase120_current_label_months"))
    dense_months = as_int(metric.get("phase120_dense_months"))
    stage1_limit = int(stage_plan.loc[stage_plan["stage_id"].eq("P120_LABEL_STAGE_01_MIN_BREADTH"), "limit_shards"].iloc[0]) if not stage_plan.empty else 0
    return pd.DataFrame(
        [
            ("phase120_dense_shards_available", as_int(metric.get("phase120_dense_shard_rows")), "Dense full-year symbol/month shards available"),
            ("phase120_current_label_months", current_months, "Months currently covered by passive labels"),
            ("phase120_dense_months_available", dense_months, "Months available in dense lake"),
            ("phase120_phase119_pre_replay_candidate_rows", 0, "Current Phase119 pre-replay candidates passing all gates"),
            ("phase120_stage_plan_rows", int(len(stage_plan)), "Label-only expansion stages emitted"),
            ("phase120_next_stage_limit_shards", stage1_limit, "Recommended next label-only expansion shard limit"),
            ("phase120_label_expansion_allowed", 1 if dense_months > current_months else 0, "1 means label coverage can expand without replay"),
            ("phase120_replay_allowed", 0, "Replay remains closed"),
            ("phase120_next_best_action", "run_phase120_stage_01_label_only_expansion_then_rerun_phase119_on_expanded_labels", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase120 Passive Label Coverage Expansion Plan",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase120 converts the Phase119 breadth failure into a staged label-only coverage plan.",
        "It does not open replay. It identifies how to expand passive labels from the current one-month run toward four-month, train-half, and full-year label coverage.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase120_passive_label_coverage_expansion_plan_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def run_phase120(
    base_dir: Path,
    dense_root: Path,
    output_dir: Path,
    phase66_dir: Path,
    phase68_dir: Path,
    phase69_dir: Path,
    phase119_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    universe = build_dense_shard_universe(base_dir, dense_root)
    coverage = build_current_label_coverage(base_dir, phase66_dir, phase68_dir, phase69_dir)
    phase119 = read_metric_table(base_dir / phase119_dir / "phase119_richer_passive_label_builder_acceptance_summary.csv")
    summary = build_coverage_summary(universe, coverage, phase119)
    stage_plan = build_stage_plan(universe)
    targets = build_month_symbol_targets(universe, coverage)
    acceptance = build_acceptance_summary(summary, stage_plan)

    universe.to_csv(output_dir / "dense_shard_universe.csv", index=False)
    coverage.to_csv(output_dir / "current_passive_label_coverage.csv", index=False)
    targets.to_csv(output_dir / "passive_label_month_symbol_targets.csv", index=False)
    stage_plan.to_csv(output_dir / "passive_label_expansion_stage_plan.csv", index=False)
    summary.to_csv(output_dir / "passive_label_coverage_summary.csv", index=False)
    acceptance.to_csv(output_dir / "phase120_passive_label_coverage_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Coverage Summary": summary,
            "Passive Label Expansion Stage Plan": stage_plan,
            "Top Month/Symbol Targets": targets.head(64),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase120_passive_label_coverage_expansion_plan",
        "dense_shards_available": int(len(universe)),
        "replay_allowed": 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase120",
            generated_utc=generated_utc,
            inputs={
                "dense_root": str(dense_root),
                "phase66_inventory": str(phase66_dir / "passive_label_file_inventory.csv"),
                "phase68_inventory": str(phase68_dir / "replenishment_label_file_inventory.csv"),
                "phase69_inventory": str(phase69_dir / "spread_transition_file_inventory.csv"),
                "phase119_acceptance": str(phase119_dir / "phase119_richer_passive_label_builder_acceptance_summary.csv"),
            },
            parameters={
                "stage_01_limit_shards": 128,
                "stage_02_limit_shards": 192,
                "policy": "label_only_expansion_no_replay",
                "breadth_gate_symbols": 20,
                "breadth_gate_trade_dates": 4,
            },
            outputs={
                "dense_shard_universe": str(output_dir / "dense_shard_universe.csv"),
                "current_passive_label_coverage": str(output_dir / "current_passive_label_coverage.csv"),
                "passive_label_month_symbol_targets": str(output_dir / "passive_label_month_symbol_targets.csv"),
                "passive_label_expansion_stage_plan": str(output_dir / "passive_label_expansion_stage_plan.csv"),
                "coverage_summary": str(output_dir / "passive_label_coverage_summary.csv"),
                "acceptance_summary": str(output_dir / "phase120_passive_label_coverage_acceptance_summary.csv"),
                "report": str(output_dir / "phase120_passive_label_coverage_expansion_plan_report.md"),
                "manifest": str(output_dir / "phase120_passive_label_coverage_expansion_plan_manifest.json"),
            },
            random_seed="none_deterministic_coverage_plan",
            scenario_ids="phase120_passive_label_coverage_expansion_after_phase119_breadth_failure",
            cost_model_version="not_applicable_label_coverage_plan",
            latency_model_version="not_applicable_label_coverage_plan",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase120_passive_label_coverage_expansion_plan_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase120 passive label coverage expansion plan.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--phase66-dir", type=Path, default=DEFAULT_PHASE66_DIR)
    parser.add_argument("--phase68-dir", type=Path, default=DEFAULT_PHASE68_DIR)
    parser.add_argument("--phase69-dir", type=Path, default=DEFAULT_PHASE69_DIR)
    parser.add_argument("--phase119-dir", type=Path, default=DEFAULT_PHASE119_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase120(
        base_dir=args.base_dir,
        dense_root=args.dense_root,
        output_dir=args.output_dir,
        phase66_dir=args.phase66_dir,
        phase68_dir=args.phase68_dir,
        phase69_dir=args.phase69_dir,
        phase119_dir=args.phase119_dir,
    )


if __name__ == "__main__":
    main()
