from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE307_DIR = Path("outputs/phase307")
DEFAULT_OUTPUT_DIR = Path("outputs/phase308")

NEXT_ACTION = "run_phase309_event_catalyst_feature_precommit_no_strategy_search"
REPAIR_ACTION = "repair_phase308_event_catalyst_join_quality_audit"

BASE_COLUMNS = [
    "event_id",
    "event_time_ist",
    "event_type",
    "symbol",
    "relative_second",
    "exchange_timestamp_ms",
    "last_price",
    "volume_traded",
]

DEPTH_COLUMNS = [
    f"{side}_{level}_{field}"
    for level in range(1, 6)
    for side in ("buy", "sell")
    for field in ("price", "quantity", "orders")
]

REQUIRED_COLUMNS = BASE_COLUMNS + DEPTH_COLUMNS


def quality_bool(value: bool) -> int:
    return int(bool(value))


def read_joined(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=REQUIRED_COLUMNS)
    return pd.read_parquet(path)


def build_symbol_quality(joined: pd.DataFrame) -> pd.DataFrame:
    if joined.empty:
        return pd.DataFrame(
            columns=[
                "event_id",
                "symbol",
                "rows",
                "relative_second_min",
                "relative_second_max",
                "distinct_relative_seconds",
                "duplicate_event_symbol_second_rows",
                "non_crossed_l1_rows",
                "bid_depth_monotonic_rows",
                "ask_depth_monotonic_rows",
                "positive_depth_quantity_rows",
                "positive_depth_order_rows",
            ]
        )
    rows: list[dict[str, object]] = []
    for (event_id, symbol), group in joined.groupby(["event_id", "symbol"], dropna=False):
        bid_mono = pd.Series(True, index=group.index)
        ask_mono = pd.Series(True, index=group.index)
        for level in range(1, 5):
            bid_mono &= group[f"buy_{level}_price"] >= group[f"buy_{level + 1}_price"]
            ask_mono &= group[f"sell_{level}_price"] <= group[f"sell_{level + 1}_price"]
        qty_cols = [f"{side}_{level}_quantity" for level in range(1, 6) for side in ("buy", "sell")]
        order_cols = [f"{side}_{level}_orders" for level in range(1, 6) for side in ("buy", "sell")]
        rows.append(
            {
                "event_id": event_id,
                "symbol": symbol,
                "rows": int(len(group)),
                "relative_second_min": int(group["relative_second"].min()),
                "relative_second_max": int(group["relative_second"].max()),
                "distinct_relative_seconds": int(group["relative_second"].nunique()),
                "duplicate_event_symbol_second_rows": int(group.duplicated(["event_id", "symbol", "relative_second"]).sum()),
                "non_crossed_l1_rows": int((group["buy_1_price"] < group["sell_1_price"]).sum()),
                "bid_depth_monotonic_rows": int(bid_mono.sum()),
                "ask_depth_monotonic_rows": int(ask_mono.sum()),
                "positive_depth_quantity_rows": int((group[qty_cols] > 0).all(axis=1).sum()),
                "positive_depth_order_rows": int((group[order_cols] > 0).all(axis=1).sum()),
            }
        )
    return pd.DataFrame(rows)


def build_issue_ledger(joined: pd.DataFrame, symbol_quality: pd.DataFrame) -> pd.DataFrame:
    issues: list[dict[str, object]] = []
    missing = [column for column in REQUIRED_COLUMNS if column not in joined.columns]
    if missing:
        issues.append({"issue_id": "missing_required_columns", "severity": "hard", "observed": "|".join(missing), "required": "all_required_columns_present"})
    if joined.empty:
        issues.append({"issue_id": "empty_joined_dataset", "severity": "hard", "observed": 0, "required": ">0"})
    if not joined.empty:
        null_cells = int(joined[REQUIRED_COLUMNS].isna().sum().sum()) if not missing else -1
        if null_cells != 0:
            issues.append({"issue_id": "required_null_cells", "severity": "hard", "observed": null_cells, "required": 0})
        if int(joined["symbol"].nunique()) < 32:
            issues.append({"issue_id": "insufficient_symbol_breadth", "severity": "hard", "observed": int(joined["symbol"].nunique()), "required": ">=32"})
        if int(joined["event_id"].nunique()) < 1:
            issues.append({"issue_id": "no_materialized_events", "severity": "hard", "observed": int(joined["event_id"].nunique()), "required": ">=1"})
    if not symbol_quality.empty:
        for metric in [
            "non_crossed_l1_rows",
            "bid_depth_monotonic_rows",
            "ask_depth_monotonic_rows",
            "positive_depth_quantity_rows",
            "positive_depth_order_rows",
        ]:
            failing = symbol_quality[symbol_quality[metric].astype(int) != symbol_quality["rows"].astype(int)]
            if not failing.empty:
                issues.append({"issue_id": f"{metric}_not_all_rows", "severity": "hard", "observed": int(len(failing)), "required": 0})
        coverage_fail = symbol_quality[
            (symbol_quality["relative_second_min"].astype(int) > -900)
            | (symbol_quality["relative_second_max"].astype(int) < 1800)
        ]
        if not coverage_fail.empty:
            issues.append({"issue_id": "incomplete_relative_window", "severity": "hard", "observed": int(len(coverage_fail)), "required": 0})
    return pd.DataFrame(issues, columns=["issue_id", "severity", "observed", "required"])


def build_gate_evaluation(phase307: pd.DataFrame, joined: pd.DataFrame, symbol_quality: pd.DataFrame, issues: pd.DataFrame) -> pd.DataFrame:
    hard_issues = int(issues["severity"].astype(str).eq("hard").sum()) if not issues.empty else 0
    full_depth_cols_present = set(DEPTH_COLUMNS).issubset(set(joined.columns))
    required_cols_present = set(REQUIRED_COLUMNS).issubset(set(joined.columns))
    joined_rows = int(len(joined))
    symbols = int(joined["symbol"].nunique()) if not joined.empty and "symbol" in joined.columns else 0
    events = int(joined["event_id"].nunique()) if not joined.empty and "event_id" in joined.columns else 0
    gates = [
        ("P308_PHASE307_MATERIALIZED_ROWS", as_int(metric_value(phase307, "phase307_materialized_join_rows", 0)) > 0, metric_value(phase307, "phase307_materialized_join_rows", ""), ">0"),
        ("P308_REQUIRED_COLUMNS_PRESENT", required_cols_present, quality_bool(required_cols_present), 1),
        ("P308_FULL_DEPTH_COLUMNS_PRESENT", full_depth_cols_present, quality_bool(full_depth_cols_present), 1),
        ("P308_JOINED_ROWS_NONEMPTY", joined_rows > 0, joined_rows, ">0"),
        ("P308_SYMBOL_BREADTH_32", symbols >= 32, symbols, ">=32"),
        ("P308_EVENT_BREADTH_NONZERO", events >= 1, events, ">=1"),
        ("P308_NO_HARD_QUALITY_ISSUES", hard_issues == 0, hard_issues, 0),
        ("P308_NO_STRATEGY_SEARCH_OPENED", True, "strategy_search_allowed_now=0", 0),
        ("P308_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(joined: pd.DataFrame, symbol_quality: pd.DataFrame, issues: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    hard_issues = int(issues["severity"].astype(str).eq("hard").sum()) if not issues.empty else 0
    next_action = NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION
    required_null_cells = int(joined[REQUIRED_COLUMNS].isna().sum().sum()) if not joined.empty and set(REQUIRED_COLUMNS).issubset(set(joined.columns)) else 0
    return pd.DataFrame(
        [
            ("phase308_join_quality_audit_complete", 1, "Phase308 joined event/depth quality audit completed"),
            ("phase308_joined_rows", int(len(joined)), "Joined rows audited"),
            ("phase308_materialized_event_rows", int(joined["event_id"].nunique()) if not joined.empty else 0, "Distinct materialized events"),
            ("phase308_materialized_symbols", int(joined["symbol"].nunique()) if not joined.empty else 0, "Distinct materialized symbols"),
            ("phase308_symbol_quality_rows", int(len(symbol_quality)), "Event-symbol quality rows"),
            ("phase308_required_columns_present", int(set(REQUIRED_COLUMNS).issubset(set(joined.columns))), "Required joined columns present"),
            ("phase308_full_depth_columns_present", int(set(DEPTH_COLUMNS).issubset(set(joined.columns))), "Depth levels 1-5 columns present"),
            ("phase308_required_null_cells", required_null_cells, "Null cells in required columns"),
            ("phase308_hard_issue_rows", hard_issues, "Hard issue rows"),
            ("phase308_strategy_search_allowed_now", 0, "No strategy search in Phase308"),
            ("phase308_strategy_replay_allowed", 0, "No replay"),
            ("phase308_strategy_promotion_allowed", 0, "No promotion"),
            ("phase308_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase308_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase308_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase308_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase308_next_best_action", next_action, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, symbol_quality: pd.DataFrame, issues: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase308 Event-Catalyst Join Quality Audit",
        "",
        "Phase308 audits the Phase307 joined event/top-five-depth artifact before any feature construction or strategy search.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Symbol quality preview",
        "",
        _markdown_table(symbol_quality.head(80)),
        "",
        "## Issue ledger",
        "",
        _markdown_table(issues if not issues.empty else pd.DataFrame([{"issue_id": "none", "severity": "", "observed": "", "required": ""}])),
        "",
        "## Gates",
        "",
        _markdown_table(gates),
    ]
    (output_dir / "phase308_event_catalyst_join_quality_audit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase307_dir: Path = DEFAULT_PHASE307_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase307 = read_csv(phase307_dir / "phase307_acceptance_summary.csv")
    joined_path = phase307_dir / "phase307_joined_event_top5_depth.parquet"
    joined = read_joined(joined_path)
    symbol_quality = build_symbol_quality(joined)
    issues = build_issue_ledger(joined, symbol_quality)
    gates = build_gate_evaluation(phase307, joined, symbol_quality, issues)
    acceptance = build_acceptance(joined, symbol_quality, issues, gates)

    symbol_quality.to_csv(output_dir / "phase308_event_symbol_join_quality.csv", index=False)
    issues.to_csv(output_dir / "phase308_join_quality_issue_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase308_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase308_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, symbol_quality, issues, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase308_event_catalyst_join_quality_audit",
        **reproducibility_fields(
            artifact_id="phase308",
            generated_utc=generated_utc,
            inputs={
                "phase307_acceptance": str(phase307_dir / "phase307_acceptance_summary.csv"),
                "phase307_joined_parquet": str(joined_path),
            },
            parameters={"required_columns": REQUIRED_COLUMNS, "depth_columns": DEPTH_COLUMNS},
            outputs={"acceptance_summary": str(output_dir / "phase308_acceptance_summary.csv")},
            cost_model_version="not_applicable_quality_audit_only",
            latency_model_version="not_applicable_quality_audit_only",
        ),
    }
    (output_dir / "phase308_event_catalyst_join_quality_audit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Phase307 joined event-catalyst top-five depth artifact.")
    parser.add_argument("--phase307-dir", type=Path, default=DEFAULT_PHASE307_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase307_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
