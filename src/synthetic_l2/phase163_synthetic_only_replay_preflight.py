from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE162_DIR = Path("outputs/phase162")
DEFAULT_PHASE39_DIR = Path("outputs/phase39")
DEFAULT_PHASE116_DIR = Path("outputs/phase116")
DEFAULT_PHASE136_DIR = Path("outputs/phase136")
DEFAULT_PHASE52_DIR = Path("outputs/phase52")
DEFAULT_DENSE_ROOT = Path("raw_synthetic_l2_phase162_distributional_full_year")
DEFAULT_OUTPUT_DIR = Path("outputs/phase163")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns or "value" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def to_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def build_preflight_gate_ledger(
    phase162_summary: pd.DataFrame,
    phase39_policy: pd.DataFrame,
    blocklist: pd.DataFrame,
    phase136_summary: pd.DataFrame,
    dense_root: Path,
) -> pd.DataFrame:
    synthetic_policy = phase39_policy[phase39_policy["policy_id"].astype(str).eq("synthetic_experiment_continuation")]
    paper_policy = phase39_policy[phase39_policy["policy_id"].astype(str).eq("paper_or_live_broker_acceptance")]
    strategy_acceptance_policy = phase39_policy[phase39_policy["policy_id"].astype(str).eq("synthetic_strategy_acceptance")]
    dense_files = list(dense_root.glob("profile=*/trade_month=*/symbol=*/part-00000.parquet")) if dense_root.exists() else []
    expected_files = to_int(metric_value(phase162_summary, "phase162_expected_partition_files", 0))
    rows = [
        {
            "gate_id": "phase162_full_year_materialization_passed",
            "gate_group": "realism_materialization",
            "required_for_replay_execution": True,
            "observed_value": metric_value(phase162_summary, "phase162_full_year_realism_audit_pass", "missing"),
            "passed": to_int(metric_value(phase162_summary, "phase162_full_year_realism_audit_pass", 0)) == 1,
            "failure_action": "Rerun/fix Phase162 before any synthetic-only replay execution.",
        },
        {
            "gate_id": "phase162_full_year_scope_complete",
            "gate_group": "realism_materialization",
            "required_for_replay_execution": True,
            "observed_value": (
                f"months={metric_value(phase162_summary, 'phase162_months_materialized', 'missing')}; "
                f"symbols={metric_value(phase162_summary, 'phase162_symbols_materialized', 'missing')}; "
                f"missing_shards={metric_value(phase162_summary, 'phase162_missing_partition_files', 'missing')}"
            ),
            "passed": (
                to_int(metric_value(phase162_summary, "phase162_months_materialized", 0)) >= 12
                and to_int(metric_value(phase162_summary, "phase162_symbols_materialized", 0)) >= 32
                and to_int(metric_value(phase162_summary, "phase162_missing_partition_files", 1)) == 0
            ),
            "failure_action": "Complete all month/symbol shards before replay.",
        },
        {
            "gate_id": "phase162_dense_parquet_root_present",
            "gate_group": "local_storage",
            "required_for_replay_execution": True,
            "observed_value": f"root={dense_root}; parquet_files={len(dense_files)}; expected_files={expected_files}",
            "passed": dense_root.exists() and len(dense_files) >= expected_files and expected_files > 0,
            "failure_action": "Regenerate or restore the local Phase162 dense parquet lake.",
        },
        {
            "gate_id": "phase39_synthetic_only_experiment_policy_open",
            "gate_group": "synthetic_only_policy",
            "required_for_replay_execution": True,
            "observed_value": synthetic_policy["allowed"].iloc[0] if not synthetic_policy.empty else "missing",
            "passed": boolish(synthetic_policy["allowed"].iloc[0]) if not synthetic_policy.empty else False,
            "failure_action": "Revisit Phase39 synthetic-only acceptance path before replay.",
        },
        {
            "gate_id": "broker_paper_live_acceptance_remains_closed",
            "gate_group": "broker_boundary",
            "required_for_replay_execution": True,
            "observed_value": paper_policy["allowed"].iloc[0] if not paper_policy.empty else "missing",
            "passed": (not boolish(paper_policy["allowed"].iloc[0])) if not paper_policy.empty else False,
            "failure_action": "Do not run this preflight if it would imply broker/paper/live readiness.",
        },
        {
            "gate_id": "strategy_promotion_still_not_open",
            "gate_group": "promotion_boundary",
            "required_for_replay_execution": True,
            "observed_value": strategy_acceptance_policy["allowed"].iloc[0] if not strategy_acceptance_policy.empty else "missing",
            "passed": (not boolish(strategy_acceptance_policy["allowed"].iloc[0])) if not strategy_acceptance_policy.empty else False,
            "failure_action": "Separate replay diagnostics from promotion/acceptance claims.",
        },
        {
            "gate_id": "phase116_blocklist_present_and_enforced",
            "gate_group": "blocklist",
            "required_for_replay_execution": True,
            "observed_value": f"blocked_families={len(blocklist)}",
            "passed": not blocklist.empty and "same_shard_continuation_allowed" in blocklist.columns,
            "failure_action": "Do not open replay until closed strategy families can be excluded.",
        },
        {
            "gate_id": "phase136_deep_book_branch_closed",
            "gate_group": "blocklist",
            "required_for_replay_execution": True,
            "observed_value": metric_value(phase136_summary, "phase136_outcome", "missing"),
            "passed": str(metric_value(phase136_summary, "phase136_outcome", "")).startswith("A_CLEAN_FALSIFICATION"),
            "failure_action": "Do not reopen the closed top-five-depth passive branch inside this replay.",
        },
    ]
    return pd.DataFrame(rows)


def build_blocklist_exclusion(blocklist: pd.DataFrame) -> pd.DataFrame:
    if blocklist.empty:
        return pd.DataFrame(
            columns=[
                "blocked_family_id",
                "blocked_strategy_ids",
                "same_shard_continuation_allowed",
                "phase163_replay_status",
                "phase163_reason",
            ]
        )
    frame = blocklist.copy()
    frame["phase163_replay_status"] = frame["same_shard_continuation_allowed"].astype(str).str.lower().map(
        {"false": "excluded_from_phase163_phase164_replay", "true": "review_before_use"}
    ).fillna("excluded_until_reviewed")
    frame["phase163_reason"] = frame["block_reason"].astype(str)
    return frame[
        [
            "blocked_family_id",
            "blocked_strategy_ids",
            "same_shard_continuation_allowed",
            "unlock_condition",
            "phase163_replay_status",
            "phase163_reason",
        ]
    ]


def build_replay_work_queue(phase39_queue: pd.DataFrame, blocklist: pd.DataFrame) -> pd.DataFrame:
    if phase39_queue.empty:
        return pd.DataFrame()
    blocked_ids: set[str] = set()
    if not blocklist.empty and "blocked_strategy_ids" in blocklist.columns:
        for raw in blocklist["blocked_strategy_ids"].dropna().astype(str):
            blocked_ids.update(part.strip() for part in raw.replace(";", ",").split(",") if part.strip())
    rows: list[dict[str, Any]] = []
    for record in phase39_queue.to_dict("records"):
        strategy_id = str(record["strategy_id"])
        track = str(record.get("experiment_track", ""))
        is_control = track == "control_risk_plumbing"
        exact_blocked = strategy_id in blocked_ids
        if exact_blocked:
            status = "excluded_blocklisted_exact_strategy_id"
            allowed = False
            next_action = "Do not replay; Phase116 blocklist contains this exact strategy id."
        elif is_control:
            status = "allowed_as_control_or_risk_plumbing_only"
            allowed = True
            next_action = "May run only as a control/risk-plumbing diagnostic; exclude from alpha promotion."
        else:
            status = "allowed_for_synthetic_only_replay_diagnostics"
            allowed = True
            next_action = (
                "May run in Phase164 synthetic-only replay diagnostics on Phase162 data; "
                "do not reuse retired dense marketable rules and do not claim broker/paper/live readiness."
            )
        rows.append(
            {
                "priority": int(record.get("priority", len(rows) + 1)),
                "strategy_id": strategy_id,
                "strategy_name": record.get("strategy_name", ""),
                "experiment_track": track,
                "phase163_synthetic_only_replay_allowed": allowed,
                "phase163_replay_status": status,
                "must_not_claim": "paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation; strategy_promotion",
                "phase162_input_root": str(DEFAULT_DENSE_ROOT),
                "next_action": next_action,
            }
        )
    return pd.DataFrame(rows).sort_values(["phase163_synthetic_only_replay_allowed", "priority"], ascending=[False, True], kind="mergesort")


def build_phase164_contract(gates: pd.DataFrame, work_queue: pd.DataFrame, blocklist_exclusion: pd.DataFrame) -> pd.DataFrame:
    preflight_pass = bool(gates["passed"].astype(bool).all()) if not gates.empty else False
    alpha_allowed = int(
        (
            work_queue["phase163_synthetic_only_replay_allowed"].astype(bool)
            & ~work_queue["experiment_track"].astype(str).eq("control_risk_plumbing")
        ).sum()
    ) if not work_queue.empty else 0
    return pd.DataFrame(
        [
            {
                "contract_id": "P164_SYNTHETIC_ONLY_FULL_YEAR_REPLAY",
                "contract_status": "open_for_implementation" if preflight_pass and alpha_allowed > 0 else "closed",
                "input_dense_root": str(DEFAULT_DENSE_ROOT),
                "input_inventory": str(DEFAULT_PHASE162_DIR / "phase162_dense_full_year_inventory.csv"),
                "allowed_scope": "synthetic_only_replay_diagnostics",
                "allowed_strategy_rows": alpha_allowed,
                "control_rows": int(work_queue["experiment_track"].astype(str).eq("control_risk_plumbing").sum()) if not work_queue.empty else 0,
                "excluded_blocklist_rows": int(blocklist_exclusion["phase163_replay_status"].astype(str).str.contains("excluded", na=False).sum()) if not blocklist_exclusion.empty else 0,
                "required_cost_model": "zerodha_equity_intraday_nse_order_formula_v2_2026_07_14_or_successor_with_documented_components",
                "required_execution_profiles": "zero_latency_control;retail_marketable_default;stressed_retail",
                "required_outputs": "trade_ledger;daily_symbol_summary;strategy_profile_summary;risk_summary;acceptance_summary;manifest",
                "forbidden_outputs": "broker_acceptance;paper_live_readiness;contract_note_reconciliation_claim;promoted_buy_sell_signal;deployable_profitability_claim",
            }
        ]
    )


def summarize(gates: pd.DataFrame, work_queue: pd.DataFrame, blocklist_exclusion: pd.DataFrame, phase162_summary: pd.DataFrame) -> pd.DataFrame:
    required = gates[gates["required_for_replay_execution"].astype(bool)].copy()
    required_pass = int(required["passed"].astype(bool).sum()) if not required.empty else 0
    preflight_pass = bool(len(required) > 0 and required_pass == len(required))
    allowed_rows = int(work_queue["phase163_synthetic_only_replay_allowed"].astype(bool).sum()) if not work_queue.empty else 0
    alpha_allowed = int(
        (
            work_queue["phase163_synthetic_only_replay_allowed"].astype(bool)
            & ~work_queue["experiment_track"].astype(str).eq("control_risk_plumbing")
        ).sum()
    ) if not work_queue.empty else 0
    return pd.DataFrame(
        [
            ("phase163_required_gate_rows", int(len(required)), "Required synthetic-only replay preflight gates"),
            ("phase163_required_gate_pass_rows", required_pass, "Required preflight gates passed"),
            ("phase163_synthetic_only_replay_preflight_pass", int(preflight_pass), "1 means guarded synthetic-only replay may be implemented next"),
            ("phase163_synthetic_only_replay_execution_allowed", int(preflight_pass and alpha_allowed > 0), "1 means Phase164 synthetic-only replay execution may open"),
            ("phase163_phase162_months", metric_value(phase162_summary, "phase162_months_materialized", "missing"), "Phase162 months available"),
            ("phase163_phase162_dense_rows", metric_value(phase162_summary, "phase162_dense_rows", "missing"), "Phase162 dense rows available"),
            ("phase163_phase162_dense_bytes", metric_value(phase162_summary, "phase162_dense_bytes", "missing"), "Phase162 dense bytes available"),
            ("phase163_work_queue_rows", int(len(work_queue)), "Rows in Phase163 replay work queue"),
            ("phase163_alpha_replay_allowed_rows", alpha_allowed, "Alpha strategy rows allowed for synthetic-only replay diagnostics"),
            ("phase163_control_replay_allowed_rows", int(work_queue["experiment_track"].astype(str).eq("control_risk_plumbing").sum()) if not work_queue.empty else 0, "Control/risk-plumbing rows allowed only as diagnostics"),
            ("phase163_blocklisted_family_rows", int(len(blocklist_exclusion)), "Phase116 blocklisted family rows enforced"),
            ("phase163_strategy_promotion_allowed", 0, "Strategy promotion remains closed"),
            ("phase163_paper_or_live_acceptance_allowed", 0, "Broker/paper/live acceptance remains closed"),
            ("phase163_azure_read_policy", "forbidden_for_analysis_download_first_then_local", "No direct Python Azure scanning for replay inputs"),
            ("phase163_next_best_action", "implement_phase164_synthetic_only_full_year_replay_on_phase162_data", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase163 Synthetic-only Replay Preflight",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase163 decides whether the Phase162 full-year generated L2 lake can be used for guarded synthetic-only replay diagnostics.",
        "It opens only synthetic-only replay execution for the next phase. It does not run P&L replay itself, does not promote strategies, and keeps broker/paper/live acceptance closed.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase163_synthetic_only_replay_preflight_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase163(
    phase162_dir: Path,
    phase39_dir: Path,
    phase116_dir: Path,
    phase136_dir: Path,
    phase52_dir: Path,
    dense_root: Path,
    output_dir: Path,
    base_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase162_summary = read_csv(phase162_dir / "phase162_full_year_materialization_acceptance_summary.csv")
    phase39_policy = read_csv(phase39_dir / "synthetic_only_acceptance_policy.csv")
    phase39_queue = read_csv(phase39_dir / "synthetic_only_experiment_queue.csv")
    blocklist = read_csv(phase116_dir / "strategy_replay_blocklist.csv")
    phase136_summary = read_csv(phase136_dir / "phase136_deep_book_verdict_acceptance_summary.csv")
    phase52_summary = read_csv(phase52_dir / "dense_replay_acceptance_summary_partial.csv")

    gates = build_preflight_gate_ledger(phase162_summary, phase39_policy, blocklist, phase136_summary, dense_root)
    blocklist_exclusion = build_blocklist_exclusion(blocklist)
    work_queue = build_replay_work_queue(phase39_queue, blocklist)
    contract = build_phase164_contract(gates, work_queue, blocklist_exclusion)
    acceptance = summarize(gates, work_queue, blocklist_exclusion, phase162_summary)
    historical_dense_replay = phase52_summary.copy()
    if not historical_dense_replay.empty:
        historical_dense_replay["phase163_use"] = "historical_falsification_context_only_not_replay_input"

    gates.to_csv(output_dir / "phase163_preflight_gate_ledger.csv", index=False)
    blocklist_exclusion.to_csv(output_dir / "phase163_blocklist_exclusion_ledger.csv", index=False)
    work_queue.to_csv(output_dir / "phase163_synthetic_only_replay_work_queue.csv", index=False)
    contract.to_csv(output_dir / "phase163_phase164_replay_contract.csv", index=False)
    historical_dense_replay.to_csv(output_dir / "phase163_historical_dense_replay_context.csv", index=False)
    acceptance.to_csv(output_dir / "phase163_synthetic_only_replay_preflight_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Preflight Gate Ledger": gates,
            "Phase164 Replay Contract": contract,
            "Replay Work Queue": work_queue,
            "Blocklist Exclusion Ledger": blocklist_exclusion,
            "Historical Dense Replay Context": historical_dense_replay,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase163_synthetic_only_replay_preflight",
        **reproducibility_fields(
            artifact_id="phase163",
            generated_utc=generated_utc,
            inputs={
                "phase162_acceptance_summary": str(phase162_dir / "phase162_full_year_materialization_acceptance_summary.csv"),
                "phase39_policy": str(phase39_dir / "synthetic_only_acceptance_policy.csv"),
                "phase39_queue": str(phase39_dir / "synthetic_only_experiment_queue.csv"),
                "phase116_blocklist": str(phase116_dir / "strategy_replay_blocklist.csv"),
                "phase136_verdict_summary": str(phase136_dir / "phase136_deep_book_verdict_acceptance_summary.csv"),
                "phase52_historical_dense_replay": str(phase52_dir / "dense_replay_acceptance_summary_partial.csv"),
                "dense_root": str(dense_root),
            },
            parameters={
                "preflight_scope": "synthetic_only_replay_execution_not_strategy_promotion",
                "strategy_promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "azure_read_policy": "forbidden_for_analysis_download_first_then_local",
            },
            outputs={
                "gate_ledger": str(output_dir / "phase163_preflight_gate_ledger.csv"),
                "blocklist_exclusion": str(output_dir / "phase163_blocklist_exclusion_ledger.csv"),
                "work_queue": str(output_dir / "phase163_synthetic_only_replay_work_queue.csv"),
                "phase164_contract": str(output_dir / "phase163_phase164_replay_contract.csv"),
                "acceptance_summary": str(output_dir / "phase163_synthetic_only_replay_preflight_acceptance_summary.csv"),
                "report": str(output_dir / "phase163_synthetic_only_replay_preflight_report.md"),
                "manifest": str(output_dir / "phase163_synthetic_only_replay_preflight_manifest.json"),
            },
            random_seed="none_deterministic_phase163_preflight",
            scenario_ids="phase163_phase162_full_year_synthetic_only_replay_preflight",
            cost_model_version="zerodha_equity_intraday_nse_order_formula_v2_2026_07_14_required_for_phase164",
            latency_model_version="phase12_execution_profiles_required_for_phase164",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase163_synthetic_only_replay_preflight_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase163 synthetic-only replay preflight.")
    parser.add_argument("--phase162-dir", type=Path, default=DEFAULT_PHASE162_DIR)
    parser.add_argument("--phase39-dir", type=Path, default=DEFAULT_PHASE39_DIR)
    parser.add_argument("--phase116-dir", type=Path, default=DEFAULT_PHASE116_DIR)
    parser.add_argument("--phase136-dir", type=Path, default=DEFAULT_PHASE136_DIR)
    parser.add_argument("--phase52-dir", type=Path, default=DEFAULT_PHASE52_DIR)
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase163(
        args.phase162_dir,
        args.phase39_dir,
        args.phase116_dir,
        args.phase136_dir,
        args.phase52_dir,
        args.dense_root,
        args.output_dir,
        args.base_dir,
    )


if __name__ == "__main__":
    main()
