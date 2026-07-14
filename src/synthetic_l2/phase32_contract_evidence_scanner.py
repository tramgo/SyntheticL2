from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def _metric(frame: pd.DataFrame, metric: str, default: int = 0) -> int:
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return int(float(rows.iloc[0]))


def _evidence_status(row: pd.Series, context: dict[str, pd.DataFrame]) -> tuple[str, str, str, bool]:
    domain = str(row["evidence_domain"])
    strategy_id = str(row["strategy_id"])
    req = str(row["contract_requirement_id"])

    if domain == "label_engineering":
        support = context["phase28_support"]
        matches = support[support["strategy_id"].eq(strategy_id)]
        if len(matches):
            proxy_rows = int(matches["proxy_rows"].iloc[0])
            return (
                "proxy_available_not_acceptance",
                "outputs/phase28/strategy_support_upgrade_summary.csv; outputs/phase28/event_label_summary.csv",
                f"Phase 28 has {proxy_rows} weak proxy label rows for {strategy_id}, but acceptance_ready is false.",
                False,
            )
        return ("missing", "", "No current label proxy artifact maps to this strategy requirement.", False)

    if domain == "feature_engineering":
        phase1 = context["phase1_summary"]
        feature_catalog = context["phase28_feature_catalog"]
        if strategy_id in set(feature_catalog["strategy_id"].astype(str)):
            return (
                "proxy_available_not_acceptance",
                "outputs/phase28/feature_label_catalog.csv",
                "Phase 28 feature-label proxy exists, but its catalog states acceptance blockers remain.",
                False,
            )
        rows = int(phase1["rows"].sum())
        withdrawal = int(phase1["inferred_withdrawal_rows"].sum()) if "inferred_withdrawal_rows" in phase1.columns else 0
        replenishment = int(phase1["inferred_replenishment_rows"].sum()) if "inferred_replenishment_rows" in phase1.columns else 0
        return (
            "partial_proxy_available_not_acceptance",
            "outputs/phase1/phase1_feature_summary.csv",
            f"Phase 1 has {rows} received-delta rows with {withdrawal} withdrawal and {replenishment} replenishment proxy rows, but not acceptance-grade redesigned features.",
            False,
        )

    if domain == "broker_evidence":
        checklist = context["broker_checklist"]
        missing = int((~checklist["file_exists_now"].astype(bool)).sum())
        return (
            "external_evidence_missing",
            "outputs/phase20_m01/broker_evidence_import_checklist.csv; outputs/phase16/broker_reconciliation_readiness.csv",
            f"{missing} broker/external evidence files are still missing; formula costs exist but broker fills/contract notes do not.",
            False,
        )

    if domain == "execution_economics":
        phase30 = context["phase30_overall"]
        positive_rows = _metric(phase30, "phase30_realistic_positive_execution_rows")
        candidate_rows = _metric(phase30, "phase30_candidate_rows")
        return (
            "negative_execution_evidence_available",
            "outputs/phase30/strategy_rejection_or_redesign_overall_summary.csv; outputs/phase25; outputs/phase26; outputs/phase27; outputs/phase29",
            f"Current realistic-positive rows={positive_rows} and candidate rows={candidate_rows}; this is blocking evidence, not satisfaction.",
            False,
        )

    if domain == "real_data":
        stage_a2 = context["stage_a2_readiness"].iloc[0]
        days = int(stage_a2["current_sample_days_available"])
        required = int(stage_a2["required_complete_days_min"])
        return (
            "one_day_real_sample_available_multiday_missing",
            "outputs/stage_a2/stage_a2_readiness_summary.csv",
            f"{days} current sample day is available; minimum required complete days is {required}.",
            False,
        )

    if domain == "data_quality":
        stage_a2 = context["stage_a2_readiness"].iloc[0]
        open_rows = int(stage_a2["open_contract_rows"])
        return (
            "diagnostics_contract_open",
            "outputs/stage_a2/stage_a2_readiness_summary.csv; outputs/stage_a2/capture_diagnostics_gap_summary.csv",
            f"Stage A2 capture diagnostics exist, but {open_rows} contract rows remain open.",
            False,
        )

    if domain == "robustness":
        return (
            "proxy_robustness_available_new_control_missing",
            "outputs/phase13; outputs/phase16; outputs/phase31/redesign_evidence_contract_ledger.csv",
            "Earlier robustness/proxy artifacts exist, but the Phase 31 strategy-specific negative controls have not been generated.",
            False,
        )

    if domain == "signal_design":
        return (
            "not_started_new_thesis_required",
            "",
            "No new post-Phase-30 cost-aware signal thesis artifact exists for this requirement.",
            False,
        )

    return ("unknown", "", f"No scanner rule for evidence domain {domain}.", False)


def scan_contract(paths: dict[str, Path], output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    contract = _read_csv(paths["phase31_contract"])
    context = {
        "phase1_summary": _read_csv(paths["phase1_summary"]),
        "phase28_support": _read_csv(paths["phase28_support"]),
        "phase28_feature_catalog": _read_csv(paths["phase28_feature_catalog"]),
        "phase30_overall": _read_csv(paths["phase30_overall"]),
        "stage_a2_readiness": _read_csv(paths["stage_a2_readiness"]),
        "broker_checklist": _read_csv(paths["broker_checklist"]),
        "broker_readiness": _read_csv(paths["broker_readiness"]),
    }

    rows = []
    for record in contract.to_dict("records"):
        status, source, note, met = _evidence_status(pd.Series(record), context)
        rows.append(
            {
                **record,
                "scanner_evidence_status": status,
                "available_evidence_source": source,
                "scanner_note": note,
                "scanner_acceptance_requirement_met": bool(met),
                "scanner_replay_expansion_allowed": False,
            }
        )
    scanned = pd.DataFrame(rows)
    availability = (
        scanned.groupby(["evidence_domain", "scanner_evidence_status"], sort=True)
        .agg(
            requirement_rows=("contract_requirement_id", "count"),
            strategies=("strategy_id", "nunique"),
            acceptance_met_rows=("scanner_acceptance_requirement_met", "sum"),
        )
        .reset_index()
    )
    acquisition = (
        scanned.groupby(["scanner_evidence_status", "evidence_domain"], sort=True)
        .agg(
            requirement_rows=("contract_requirement_id", "count"),
            strategies=("strategy_id", lambda values: ";".join(sorted(set(map(str, values))))),
            example_required_artifact_or_test=("required_artifact_or_test", "first"),
            available_evidence_source=("available_evidence_source", "first"),
        )
        .reset_index()
    )
    acquisition["next_action"] = acquisition["scanner_evidence_status"].map(_next_action)

    strategy = (
        scanned.groupby(["strategy_id", "strategy_name", "redesign_priority"], sort=True)
        .agg(
            requirement_rows=("contract_requirement_id", "count"),
            proxy_or_partial_available_rows=("scanner_evidence_status", lambda values: int(sum("proxy" in str(v) or "one_day" in str(v) or "negative_execution" in str(v) for v in values))),
            external_missing_rows=("scanner_evidence_status", lambda values: int(sum("missing" in str(v) or "not_started" in str(v) for v in values))),
            acceptance_met_rows=("scanner_acceptance_requirement_met", "sum"),
            replay_allowed_rows=("scanner_replay_expansion_allowed", "sum"),
        )
        .reset_index()
    )
    strategy["evidence_scan_status"] = "blocked_scanned_evidence_not_acceptance_ready"

    overall = pd.DataFrame(
        [
            {"metric": "phase32_contract_rows_scanned", "value": int(len(scanned)), "description": "Phase 31 contract rows scanned against current artifacts"},
            {"metric": "phase32_proxy_or_partial_available_rows", "value": int(strategy["proxy_or_partial_available_rows"].sum()), "description": "Rows with some current proxy/partial/negative evidence"},
            {"metric": "phase32_external_or_new_artifact_missing_rows", "value": int(strategy["external_missing_rows"].sum()), "description": "Rows requiring external evidence or new signal artifacts"},
            {"metric": "phase32_acceptance_met_rows", "value": int(scanned["scanner_acceptance_requirement_met"].sum()), "description": "Rows that scanner can mark acceptance-met now"},
            {"metric": "phase32_replay_allowed_rows", "value": int(scanned["scanner_replay_expansion_allowed"].sum()), "description": "Rows allowed back into replay after scan"},
            {"metric": "phase32_strategy_rows_scanned", "value": int(strategy["strategy_id"].nunique()), "description": "Strategy families scanned"},
            {"metric": "phase32_acquisition_queue_rows", "value": int(len(acquisition)), "description": "Evidence acquisition queue rows"},
        ]
    )

    scanned.to_csv(output_dir / "contract_evidence_scan_ledger.csv", index=False)
    availability.to_csv(output_dir / "evidence_availability_summary.csv", index=False)
    acquisition.to_csv(output_dir / "evidence_acquisition_queue.csv", index=False)
    strategy.to_csv(output_dir / "strategy_evidence_scan_summary.csv", index=False)
    overall.to_csv(output_dir / "contract_evidence_scan_overall_summary.csv", index=False)
    write_report(output_dir, overall, availability, strategy, acquisition, scanned)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "contract_rows_scanned": int(len(scanned)),
        "acceptance_met_rows": int(scanned["scanner_acceptance_requirement_met"].sum()),
        "replay_allowed_rows": int(scanned["scanner_replay_expansion_allowed"].sum()),
        "scope": "phase32_contract_evidence_scanner_current_artifacts_not_acceptance",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase32",
            generated_utc=generated_utc,
            inputs={name: str(path) for name, path in paths.items()},
            parameters={
                "scanner_policy": "current proxy evidence can be recorded but cannot satisfy Phase 31 acceptance requirements",
                "domains_scanned": sorted(scanned["evidence_domain"].unique().tolist()),
            },
            outputs={
                "scan_ledger": str(output_dir / "contract_evidence_scan_ledger.csv"),
                "availability_summary": str(output_dir / "evidence_availability_summary.csv"),
                "acquisition_queue": str(output_dir / "evidence_acquisition_queue.csv"),
                "strategy_summary": str(output_dir / "strategy_evidence_scan_summary.csv"),
                "overall_summary": str(output_dir / "contract_evidence_scan_overall_summary.csv"),
                "report": str(output_dir / "phase32_contract_evidence_scanner_report.md"),
                "manifest": str(output_dir / "phase32_contract_evidence_scanner_manifest.json"),
            },
            random_seed="none_deterministic_evidence_scanner_rules",
            scenario_ids="phase31_contract_rows_current_workspace_artifacts",
            cost_model_version="zerodha_equity_intraday_nse_order_formula_v2_2026_07_14",
            latency_model_version="phase12_execution_profiles_event_latency_counts",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase32_contract_evidence_scanner_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def _next_action(status: str) -> str:
    if status == "external_evidence_missing":
        return "Import broker fills, contract-note charges, strategy-order linkage and reconciliation tolerances."
    if status == "not_started_new_thesis_required":
        return "Write and register a new cost-aware signal thesis before more replay compute."
    if "multiday_missing" in status:
        return "Collect or import multi-day Class B real tick data and rerun capture diagnostics."
    if "proxy_available" in status:
        return "Upgrade proxy evidence into acceptance-grade labels/features, then rerun the contract scanner."
    if "negative_execution" in status:
        return "Do not replay current form; redesign until the expected edge exceeds cost and latency hurdle."
    return "Create the missing artifact/test named by the Phase 31 contract row."


def write_report(
    output_dir: Path,
    overall: pd.DataFrame,
    availability: pd.DataFrame,
    strategy: pd.DataFrame,
    acquisition: pd.DataFrame,
    scanned: pd.DataFrame,
) -> None:
    lines = [
        "# Phase 32 Contract Evidence Scanner",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This milestone scans Phase 31 no-replay-until requirements against currently available workspace artifacts.",
        "It records proxy/partial/negative evidence where present, but does not mark any requirement acceptance-met.",
        "",
        "## Overall Summary",
        "",
        _markdown_table(overall),
        "",
        "## Evidence Availability Summary",
        "",
        _markdown_table(availability),
        "",
        "## Strategy Evidence Scan Summary",
        "",
        _markdown_table(strategy),
        "",
        "## Evidence Acquisition Queue",
        "",
        _markdown_table(acquisition),
        "",
        "## Contract Evidence Scan Ledger",
        "",
        _markdown_table(scanned),
        "",
    ]
    (output_dir / "phase32_contract_evidence_scanner_report.md").write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan Phase 31 evidence contracts against current workspace artifacts.")
    parser.add_argument("--phase31-contract", type=Path, default=Path("outputs/phase31/redesign_evidence_contract_ledger.csv"))
    parser.add_argument("--phase1-summary", type=Path, default=Path("outputs/phase1/phase1_feature_summary.csv"))
    parser.add_argument("--phase28-support", type=Path, default=Path("outputs/phase28/strategy_support_upgrade_summary.csv"))
    parser.add_argument("--phase28-feature-catalog", type=Path, default=Path("outputs/phase28/feature_label_catalog.csv"))
    parser.add_argument("--phase30-overall", type=Path, default=Path("outputs/phase30/strategy_rejection_or_redesign_overall_summary.csv"))
    parser.add_argument("--stage-a2-readiness", type=Path, default=Path("outputs/stage_a2/stage_a2_readiness_summary.csv"))
    parser.add_argument("--broker-checklist", type=Path, default=Path("outputs/phase20_m01/broker_evidence_import_checklist.csv"))
    parser.add_argument("--broker-readiness", type=Path, default=Path("outputs/phase16/broker_reconciliation_readiness.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase32"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "phase31_contract": args.phase31_contract,
        "phase1_summary": args.phase1_summary,
        "phase28_support": args.phase28_support,
        "phase28_feature_catalog": args.phase28_feature_catalog,
        "phase30_overall": args.phase30_overall,
        "stage_a2_readiness": args.stage_a2_readiness,
        "broker_checklist": args.broker_checklist,
        "broker_readiness": args.broker_readiness,
    }
    scan_contract(paths, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
