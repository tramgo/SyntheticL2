from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


WORK_PACKAGES = [
    ("WP1", "Data intake and audit", "Stage A1; Phase 1; Phase 10", "partial_current"),
    ("WP2", "Feature and event reconstruction", "Phase 1; Phase 9; Phase 11", "partial_current"),
    ("WP3", "Regime/scenario framework", "Phase 3; Phase 4; Phase 7", "implemented_proxy"),
    ("WP4", "Price and cross-ticker simulator", "Phase 5; Phase 7", "implemented_proxy"),
    ("WP5", "L2 event simulator", "Phase 6; Phase 9", "partial_proxy"),
    ("WP6", "Retail feed emulator", "Phase 8", "implemented_proxy"),
    ("WP7", "Storage pipeline", "Phase 9; Phase 10; DuckDB workspace", "partial_current"),
    ("WP8", "Backtester", "Phase 12; Phase 15", "partial_proxy"),
    ("WP9", "Strategy suite", "Phase 11; Phase 13", "partial_proxy"),
    ("WP10", "Validation and reporting", "Phase 14; Phase 15; Phase 16", "partial_current"),
]


DELIVERABLES = [
    ("WP1", "schema detector", "implemented", "outputs/stage_a1/schema_report.csv", "Real-sample schema audit exists."),
    ("WP1", "data-quality checks", "implemented", "outputs/stage_a1/data_quality_report.csv", "Per-symbol quality checks exist."),
    ("WP1", "sample-day profile", "implemented", "outputs/stage_a1/stage_a1_report.md", "Sample-day profile report exists."),
    ("WP1", "size report", "implemented", "outputs/phase10/phase10_storage_report.md", "Storage inventory and size estimates exist."),
    ("WP1", "canonical Parquet conversion", "implemented", "outputs/stage_a1/compact_ticks_by_symbol", "Compact per-symbol Parquet conversion exists."),
    ("WP2", "L1/L5 imbalance", "implemented", "outputs/phase9/tier_c/features_5m.parquet", "Feature product contains imbalance proxies."),
    ("WP2", "MLOFI", "implemented_proxy", "outputs/phase11/strategy_feature_availability.csv", "MLOFI strategy support is proxy-level."),
    ("WP2", "trade classification", "implemented_proxy", "outputs/phase1/event_reconstruction/event_reconstruction_quality.csv", "Weak aggressor-side labels are summarized with explicit inference-quality limits; not exchange aggressor truth."),
    ("WP2", "microprice", "implemented", "outputs/phase9/tier_c/features_5m.parquet", "Microprice feature is available in Tier C."),
    ("WP2", "liquidity withdrawal", "implemented_proxy", "outputs/phase11/strategy_feature_availability.csv", "Liquidity-withdrawal features are proxy-supported."),
    ("WP2", "replenishment", "implemented_proxy", "outputs/phase1/event_reconstruction/event_reconstruction_summary.csv", "Visible-depth replenishment proxies are reconstructed from received market-by-price deltas with ambiguity flags."),
    ("WP2", "book shape", "implemented_proxy", "outputs/phase9/tier_c/features_5m.parquet", "Book-shape proxies are available in 5-minute features."),
    ("WP2", "regime-independent baseline features", "implemented", "outputs/phase11/baseline_strategy_matrix.csv", "Baseline strategy features are registered."),
    ("WP3", "regime definitions", "implemented", "outputs/phase3/intraday_market_states.csv", "Intraday market-state definitions exist."),
    ("WP3", "scenario YAML/JSON", "implemented", "outputs/phase4/scenario_manifest.json", "Scenario profiles exist as structured JSON/manifest artifacts."),
    ("WP3", "daily calendar generator", "implemented", "outputs/phase4/scenario_calendar.csv", "Daily scenario calendar exists."),
    ("WP3", "intraday state generator", "implemented", "outputs/phase3/intraday_market_states.csv", "Intraday state grid exists."),
    ("WP3", "shock injector", "implemented_proxy", "outputs/phase7/shock_library.csv", "Shock library exists; injector is represented by generated shock annotations."),
    ("WP4", "market/sector/ticker factors", "implemented_proxy", "outputs/phase5/price_paths_5m.parquet", "Synthetic price paths include cross-sectional structure proxies."),
    ("WP4", "stochastic volatility", "implemented_proxy", "outputs/phase5/daily_price_summary.csv", "Volatility regime effects are represented at proxy level."),
    ("WP4", "jump process", "implemented_proxy", "outputs/phase7/shock_library.csv", "Jump/shock events are registered."),
    ("WP4", "correlation controls", "implemented_proxy", "outputs/phase7/shock_day_summary.csv", "Market/ticker shock grouping provides proxy correlation controls."),
    ("WP4", "price-grid enforcement", "implemented", "outputs/phase5/price_paths_5m.parquet", "Price grid validation passed in Phase 5/6 artifacts."),
    ("WP5", "additions/cancellations/trades", "implemented_proxy", "outputs/phase1/event_reconstruction/event_reconstruction_quality.csv", "Add/cancel/consume proxies are explicitly summarized from visible quantity deltas and volume increments; individual-order causality remains unavailable."),
    ("WP5", "five-level reconstruction", "implemented", "outputs/phase6/l2_book_states_5m.parquet", "Five-level L2 state product exists."),
    ("WP5", "resilience", "implemented_proxy", "outputs/phase6/l2_book_summary.csv", "Spread/depth structural checks exist."),
    ("WP5", "spread/depth dynamics", "implemented_proxy", "outputs/phase6/l2_book_states_5m.parquet", "Spread/depth dynamics are generated at 5-minute granularity."),
    ("WP5", "activity seasonality", "implemented_proxy", "outputs/phase8/feed_profile_summary.csv", "Feed/event profiles carry activity-seasonality effects."),
    ("WP6", "receive latency", "implemented", "outputs/phase8/feed_profile_summary.csv", "Latency profiles exist."),
    ("WP6", "batching", "implemented", "outputs/phase8/retail_feed_observations.parquet", "Batched retail observations exist."),
    ("WP6", "gaps", "implemented", "outputs/phase8/retail_feed_dropped_events.csv", "Dropped/gap events are recorded."),
    ("WP6", "duplicates", "implemented", "outputs/phase8/feed_profile_summary.csv", "Duplicate observations are summarized."),
    ("WP6", "reconnects", "implemented_proxy", "outputs/phase8/feed_profile_summary.csv", "Disconnect/reconnect proxy states exist."),
    ("WP6", "asynchronous ticker stream", "implemented_proxy", "outputs/phase8/retail_feed_observations.parquet", "Per-symbol retail feed observations are asynchronous proxies."),
    ("WP7", "raw/delta/resampled Parquet", "implemented_proxy", "outputs/phase9/tier_d/resampled_features_15m.parquet", "Raw synthetic, compact state, 5-minute features and a 15-minute resampled feature panel exist; exact tick-delta resampling remains not acceptance-grade."),
    ("WP7", "partitioning", "implemented", "outputs/phase10/partition_recommendations.csv", "Partition recommendations exist."),
    ("WP7", "compression benchmark", "implemented_proxy", "outputs/phase10/size_estimates.csv", "Compression/size estimates exist; full benchmark matrix is not exhaustive."),
    ("WP7", "replay tool", "implemented", "outputs/replay/replay_validation_report.md", "Standalone deterministic replay CLI exists for Phase 9 Tier A/B/C products."),
    ("WP7", "metadata manifest", "implemented", "outputs/duckdb/duckdb_workspace_manifest.json", "Cross-phase manifest exists."),
    ("WP8", "event-driven engine", "implemented_proxy", "outputs/phase12/event_backtest_order_summary.csv", "Event-driven order lifecycle proxy covers signal, submission, arrival, fill/reject and P&L/risk update over sampled Phase 12 trade events."),
    ("WP8", "market and limit orders", "implemented_proxy", "outputs/phase12/order_model_catalog.csv", "Market, marketable-limit, passive-limit, cancel/replace, partial-fill and rejection scenarios are cataloged and exercised as proxy order models."),
    ("WP8", "latency", "implemented_proxy", "outputs/phase12/execution_profiles.csv", "Latency profiles are applied."),
    ("WP8", "partial fills", "implemented_proxy", "outputs/phase12_order_lifecycle/partial_fill_summary.csv", "Deterministic partial-fill and queue-position bucket proxy exists over the sampled Phase 12 trade ledger."),
    ("WP8", "slippage", "implemented_proxy", "outputs/phase12/cost_schedule.csv", "Fixed slippage ticks are modeled as a proxy."),
    ("WP8", "fees", "implemented_proxy", "outputs/phase12/cost_schedule.csv", "Zerodha-sourced equity intraday charge schedule exists as a normalized bps proxy; order-notional caps and contract-note rounding are not acceptance-grade."),
    ("WP8", "risk controls", "implemented_proxy", "outputs/phase12_order_lifecycle/risk_control_summary.csv", "Sampled risk-control proxy exists for position limits, drawdown, tail loss and daily loss halts."),
    ("WP9", "S01-S11 modules", "partial_proxy", "outputs/phase11/strategy_validation_matrix.csv", "S01-S11 are registered; only proxy signals are implemented."),
    ("WP9", "shared feature interface", "implemented_proxy", "outputs/phase11/strategy_feature_availability.csv", "Strategy-feature availability matrix exists."),
    ("WP9", "baseline strategies", "implemented_proxy", "outputs/phase11/baseline_strategy_matrix.csv", "Baseline registry exists."),
    ("WP9", "parameter registry", "implemented_proxy", "outputs/phase13/parameter_grid.csv", "Initial parameter grid exists."),
    ("WP10", "synthetic realism dashboard", "implemented_proxy", "outputs/dashboard/synthetic_l2_validation_dashboard.html", "Static validation dashboard exists over Phase 14-17 quality, acceptance, metrics and gap evidence."),
    ("WP10", "strategy performance reports", "implemented_proxy", "outputs/phase16/phase16_metrics_reporting_report.md", "Proxy performance report exists."),
    ("WP10", "robustness matrix", "implemented_proxy", "outputs/phase13/experiment_run_summary.csv", "Pre-registered experiment rows have a deterministic proxy smoke ledger; full robustness validation is not acceptance-grade yet."),
    ("WP10", "failed-test log", "implemented", "outputs/phase15/acceptance_blockers.csv", "Acceptance blockers provide failed-test log."),
    ("WP10", "promotion/rejection decision", "implemented", "outputs/phase15/strategy_acceptance_summary.csv", "All strategies currently blocked/not promotable."),
]


STATUS_RANK = {
    "implemented": 4,
    "implemented_proxy": 3,
    "partial_current": 2,
    "partial_proxy": 1,
    "missing": 0,
}


def _evidence_exists(base_dir: Path, evidence_path: str) -> bool:
    if not evidence_path:
        return False
    return (base_dir / evidence_path).exists()


def build_deliverable_traceability(base_dir: Path) -> pd.DataFrame:
    rows = []
    for wp_id, deliverable, status, evidence_path, note in DELIVERABLES:
        evidence_exists = _evidence_exists(base_dir, evidence_path)
        evidence_status = "present" if evidence_exists else ("not_required_for_missing" if status == "missing" else "missing_evidence")
        rows.append(
            {
                "work_package_id": wp_id,
                "deliverable": deliverable,
                "implementation_status": status,
                "status_rank": STATUS_RANK[status],
                "evidence_path": evidence_path,
                "evidence_status": evidence_status,
                "acceptance_grade": status == "implemented",
                "note": note,
            }
        )
    return pd.DataFrame(rows)


def build_work_package_registry(deliverables: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for wp_id, name, evidence_phase, planned_status in WORK_PACKAGES:
        subset = deliverables[deliverables["work_package_id"] == wp_id]
        missing = int((subset["implementation_status"] == "missing").sum())
        implemented = int((subset["implementation_status"] == "implemented").sum())
        proxy_or_partial = int(len(subset) - implemented - missing)
        min_rank = int(subset["status_rank"].min()) if len(subset) else 0
        if missing:
            current_status = "blocked_by_missing_deliverables"
        elif min_rank < STATUS_RANK["implemented"]:
            current_status = "partial_or_proxy_complete"
        else:
            current_status = "implemented_current_evidence"
        rows.append(
            {
                "work_package_id": wp_id,
                "work_package_name": name,
                "evidence_phase_or_artifact": evidence_phase,
                "planned_status": planned_status,
                "deliverables": int(len(subset)),
                "implemented_deliverables": implemented,
                "proxy_or_partial_deliverables": proxy_or_partial,
                "missing_deliverables": missing,
                "current_status": current_status,
            }
        )
    return pd.DataFrame(rows)


def build_gap_backlog(deliverables: pd.DataFrame) -> pd.DataFrame:
    gaps = deliverables[deliverables["implementation_status"] != "implemented"].copy()
    priority_map = {
        "missing": "P0",
        "partial_proxy": "P1",
        "partial_current": "P1",
        "implemented_proxy": "P2",
    }
    gaps["priority"] = gaps["implementation_status"].map(priority_map).fillna("P3")
    gaps["recommended_next_action"] = gaps.apply(
        lambda row: _recommend_next_action(str(row["work_package_id"]), str(row["deliverable"]), str(row["implementation_status"])),
        axis=1,
    )
    return gaps[
        [
            "priority",
            "work_package_id",
            "deliverable",
            "implementation_status",
            "evidence_path",
            "evidence_status",
            "recommended_next_action",
            "note",
        ]
    ].sort_values(["priority", "work_package_id", "deliverable"], kind="mergesort")


def _recommend_next_action(wp_id: str, deliverable: str, status: str) -> str:
    if status == "missing" and wp_id == "WP7":
        return "Build replay CLI over Tier A/Tier B Parquet with symbol/date/profile filters and deterministic ordering checks."
    if status == "missing" and wp_id == "WP8":
        return "Extend execution simulator with order lifecycle, queue/partial-fill model and risk-control state."
    if wp_id == "WP10" and "dashboard" in deliverable and status.startswith("partial"):
        return "Create static or interactive dashboard from Phase 14-16 CSV outputs."
    if wp_id == "WP13":
        return "No action mapped."
    if status.startswith("partial"):
        return "Promote proxy to current evidence by adding validation checks and acceptance-grade outputs."
    if status == "implemented_proxy":
        return "Document assumptions and add sensitivity/holdout validation before using for promotion."
    return "No action required for current phase."


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    text = frame.copy()
    for column in text.columns:
        text[column] = text[column].map(lambda value: "" if pd.isna(value) else str(value))
    headers = [str(column) for column in text.columns]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in text.values.tolist())
    return "\n".join(lines)


def write_report(output_dir: Path, registry: pd.DataFrame, deliverables: pd.DataFrame, gaps: pd.DataFrame) -> None:
    status_summary = registry.groupby("current_status", sort=True).size().reset_index(name="work_packages")
    deliverable_summary = deliverables.groupby("implementation_status", sort=True).size().reset_index(name="deliverables")
    lines = [
        "# Phase 17 Implementation Work Packages Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase converts WP1-WP10 into an evidence-backed implementation registry.",
        "It does not claim acceptance completion; it identifies which deliverables are implemented, proxy/partial, or missing.",
        "",
        "## Work Package Status Summary",
        "",
        _markdown_table(status_summary),
        "",
        "## Deliverable Status Summary",
        "",
        _markdown_table(deliverable_summary),
        "",
        "## Work Package Registry",
        "",
        _markdown_table(registry),
        "",
        "## Highest Priority Gaps",
        "",
        _markdown_table(gaps.head(20)),
        "",
    ]
    (output_dir / "phase17_work_packages_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase17(output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    deliverables = build_deliverable_traceability(base_dir)
    registry = build_work_package_registry(deliverables)
    gaps = build_gap_backlog(deliverables)

    registry.to_csv(output_dir / "work_package_registry.csv", index=False)
    deliverables.to_csv(output_dir / "deliverable_traceability.csv", index=False)
    gaps.to_csv(output_dir / "implementation_gap_backlog.csv", index=False)
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "work_packages": int(len(registry)),
        "deliverables": int(len(deliverables)),
        "implemented_deliverables": int((deliverables["implementation_status"] == "implemented").sum()),
        "proxy_or_partial_deliverables": int(deliverables["implementation_status"].isin(["implemented_proxy", "partial_current", "partial_proxy"]).sum()),
        "missing_deliverables": int((deliverables["implementation_status"] == "missing").sum()),
        "work_packages_blocked_by_missing_deliverables": int((registry["current_status"] == "blocked_by_missing_deliverables").sum()),
        "acceptance_grade_deliverables": int(deliverables["acceptance_grade"].sum()),
        "scope": "phase17_work_package_traceability_and_gap_backlog",
    }
    (output_dir / "work_packages_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, registry, deliverables, gaps)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 17 work-package traceability artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase17"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase17(args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
