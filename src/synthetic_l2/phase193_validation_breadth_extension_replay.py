from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase184_train_validation_replay_dry_run import build_model_frame, profile_cost_bps
from synthetic_l2.phase187_cost_aware_sparse_candidate import add_derived_fields, candidate_mask
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE176_DIR = Path("outputs/phase176")
DEFAULT_PHASE180_DIR = Path("outputs/phase180")
DEFAULT_PHASE181_DIR = Path("outputs/phase181")
DEFAULT_PHASE191_DIR = Path("outputs/phase191")
DEFAULT_OUTPUT_DIR = Path("outputs/phase193")
RANDOM_SEED = 193
EXPECTED_CONTRACT_HASH = "6aec9abe7f1da4c49372eb44b3fa050e44c1b8105dd4bc0c47efd9357af697d1"
EVALUATION_ROLES = {"validation", "unassigned"}
FORBIDDEN_OUTPUTS = "test_result;test_replay_execution;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def frozen_candidate(phase191_dir: Path) -> pd.Series:
    contract = read_csv(phase191_dir / "phase191_frozen_candidate_contract.csv")
    if contract.empty:
        raise ValueError("Phase191 frozen candidate contract is missing.")
    row = contract.iloc[0].copy()
    if str(row.get("candidate_contract_hash", "")) != EXPECTED_CONTRACT_HASH:
        raise ValueError("Phase191 frozen candidate hash mismatch; abort before validation extension replay.")
    return row


def selected_extension_events(frame: pd.DataFrame, candidate: pd.Series, profile: pd.Series, rng: np.random.Generator) -> pd.DataFrame:
    evaluation = frame.loc[frame["split_role"].astype(str).isin(EVALUATION_ROLES)].copy()
    evaluation = evaluation.loc[~evaluation["split_role"].astype(str).eq("test_untouched")].copy()
    mask, side = candidate_mask(evaluation, candidate)
    selected = evaluation.loc[mask].copy()
    selected["candidate_id"] = candidate["candidate_id"]
    selected["candidate_contract_hash"] = candidate["candidate_contract_hash"]
    selected["latency_profile_id"] = profile["profile_id"]
    selected["dry_side"] = side.loc[mask].astype(int)
    selected["gross_return_bps_proxy"] = selected["dry_side"] * pd.to_numeric(selected["future_mid_return_bps_next_bucket"], errors="coerce")
    selected["cost_bound_bps"] = profile_cost_bps(selected, profile)
    selected["net_return_bps_after_cost_proxy"] = selected["gross_return_bps_proxy"] - selected["cost_bound_bps"]
    shuffled_time = pd.to_numeric(selected["future_mid_return_bps_next_bucket"], errors="coerce").to_numpy(copy=True)
    rng.shuffle(shuffled_time)
    selected["shuffled_time_net_bps_proxy"] = selected["dry_side"].to_numpy() * shuffled_time - selected["cost_bound_bps"].to_numpy()
    shuffled_symbol = selected["future_mid_return_bps_next_bucket"].sample(frac=1.0, random_state=RANDOM_SEED).to_numpy(copy=True) if len(selected) else np.array([])
    selected["shuffled_symbol_net_bps_proxy"] = selected["dry_side"].to_numpy() * shuffled_symbol - selected["cost_bound_bps"].to_numpy()
    selected["net_edge_over_shuffled_time_bps"] = selected["net_return_bps_after_cost_proxy"] - selected["shuffled_time_net_bps_proxy"]
    selected["net_edge_over_shuffled_symbol_bps"] = selected["net_return_bps_after_cost_proxy"] - selected["shuffled_symbol_net_bps_proxy"]
    selected["test_rows_used"] = 0
    selected["promotion_allowed"] = 0
    return selected


def summarize_group(events: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    if events.empty:
        return pd.DataFrame()
    out = (
        events.groupby(group_cols, as_index=False)
        .agg(
            decision_events=("bucket_ms", "count"),
            symbols=("symbol", "nunique"),
            dates=("trade_date", "nunique"),
            gross_return_bps_proxy_mean=("gross_return_bps_proxy", "mean"),
            cost_bound_bps_mean=("cost_bound_bps", "mean"),
            net_return_bps_after_cost_proxy_mean=("net_return_bps_after_cost_proxy", "mean"),
            net_positive_event_fraction=("net_return_bps_after_cost_proxy", lambda s: float((s > 0).mean())),
            shuffled_time_net_bps_proxy_mean=("shuffled_time_net_bps_proxy", "mean"),
            shuffled_symbol_net_bps_proxy_mean=("shuffled_symbol_net_bps_proxy", "mean"),
            net_edge_over_shuffled_time_bps_mean=("net_edge_over_shuffled_time_bps", "mean"),
            net_edge_over_shuffled_symbol_bps_mean=("net_edge_over_shuffled_symbol_bps", "mean"),
        )
    )
    out["net_positive_group"] = (out["net_return_bps_after_cost_proxy_mean"] > 0).astype(int)
    out["beats_shuffled_time_group"] = (out["net_edge_over_shuffled_time_bps_mean"] > 0).astype(int)
    out["beats_shuffled_symbol_group"] = (out["net_edge_over_shuffled_symbol_bps_mean"] > 0).astype(int)
    return out


def build_partition_use(partition_use: pd.DataFrame) -> pd.DataFrame:
    if partition_use.empty:
        return partition_use
    out = partition_use.copy()
    out["used_in_phase193"] = out["split_role"].astype(str).isin(EVALUATION_ROLES).astype(int)
    out.loc[out["split_role"].astype(str).eq("test_untouched"), "used_in_phase193"] = 0
    return out


def build_interpretation(events: pd.DataFrame, frame: pd.DataFrame, by_date: pd.DataFrame, by_symbol: pd.DataFrame) -> pd.DataFrame:
    if events.empty:
        return pd.DataFrame()
    total_events = len(events)
    by_symbol_rank = by_symbol.sort_values("decision_events", ascending=False).copy()
    top_symbol_share = float(by_symbol_rank["decision_events"].iloc[0] / total_events) if len(by_symbol_rank) else 1.0
    top3_symbol_share = float(by_symbol_rank["decision_events"].head(3).sum() / total_events) if len(by_symbol_rank) else 1.0
    date_positive_fraction = float(by_date["net_positive_group"].mean()) if not by_date.empty else 0.0
    symbol_positive_fraction = float(by_symbol["net_positive_group"].mean()) if not by_symbol.empty else 0.0
    min_profile_net = float(events.groupby("latency_profile_id")["net_return_bps_after_cost_proxy"].mean().min())
    min_time_edge = float(events.groupby("latency_profile_id")["net_edge_over_shuffled_time_bps"].mean().min())
    min_symbol_edge = float(events.groupby("latency_profile_id")["net_edge_over_shuffled_symbol_bps"].mean().min())
    extension_dates = sorted(events.loc[events["split_role"].astype(str).eq("unassigned"), "trade_date"].astype(str).unique().tolist())
    original_validation_dates = sorted(events.loc[events["split_role"].astype(str).eq("validation"), "trade_date"].astype(str).unique().tolist())
    evaluation_rows = int(frame.loc[frame["split_role"].astype(str).isin(EVALUATION_ROLES)].shape[0])
    decision_rate = float(total_events / evaluation_rows) if evaluation_rows else 0.0
    breadth_warning = int(symbol_positive_fraction < 0.25)
    date_count_warning = int(events["trade_date"].nunique() < 2)
    concentration_warning = int(top_symbol_share > 0.35 or top3_symbol_share > 0.70)
    if min_profile_net > 0 and min_time_edge > 0 and min_symbol_edge > 0 and date_positive_fraction >= 1.0 and concentration_warning == 0 and breadth_warning == 0 and date_count_warning == 0:
        verdict = "validation_breadth_expanded_candidate_promising_test_precommit_review_still_required"
    elif min_profile_net > 0 and min_time_edge > 0 and min_symbol_edge > 0 and date_positive_fraction >= 1.0:
        verdict = "validation_breadth_expanded_but_symbol_breadth_or_concentration_still_limited"
    elif date_positive_fraction < 1.0:
        verdict = "validation_extension_mixed_or_negative_by_date_add_more_validation_or_redesign_before_test"
    else:
        verdict = "validation_extension_failed_cost_or_control_check_redesign_before_test"
    return pd.DataFrame(
        [
            {
                "candidate_id": str(events["candidate_id"].iloc[0]),
                "candidate_contract_hash": str(events["candidate_contract_hash"].iloc[0]),
                "evaluation_split_roles": ";".join(sorted(EVALUATION_ROLES)),
                "original_validation_dates": ";".join(original_validation_dates),
                "extension_validation_dates": ";".join(extension_dates),
                "validation_extension_decision_events": int(total_events),
                "evaluation_rows": evaluation_rows,
                "decision_rate": decision_rate,
                "validation_symbols_with_events": int(events["symbol"].nunique()),
                "validation_dates_with_events": int(events["trade_date"].nunique()),
                "overall_net_bps_proxy_mean": float(events["net_return_bps_after_cost_proxy"].mean()),
                "overall_gross_bps_proxy_mean": float(events["gross_return_bps_proxy"].mean()),
                "overall_cost_bps_mean": float(events["cost_bound_bps"].mean()),
                "min_profile_net_bps_proxy_mean": min_profile_net,
                "min_profile_edge_over_shuffled_time_bps": min_time_edge,
                "min_profile_edge_over_shuffled_symbol_bps": min_symbol_edge,
                "date_positive_fraction": date_positive_fraction,
                "symbol_positive_fraction": symbol_positive_fraction,
                "top_symbol_event_share": top_symbol_share,
                "top3_symbol_event_share": top3_symbol_share,
                "concentration_warning": concentration_warning,
                "breadth_warning": breadth_warning,
                "date_count_warning": date_count_warning,
                "phase193_verdict": verdict,
                "test_replay_allowed_by_phase193": 0,
                "promotion_allowed": 0,
            }
        ]
    )


def build_gates(candidate: pd.Series, partition_use: pd.DataFrame, interpretation: pd.DataFrame, by_date: pd.DataFrame, by_symbol: pd.DataFrame) -> pd.DataFrame:
    interp = interpretation.iloc[0] if not interpretation.empty else {}
    test_partitions_used = int(partition_use.loc[partition_use["split_role"].astype(str).eq("test_untouched"), "used_in_phase193"].sum()) if not partition_use.empty else 0
    extension_rows = int(partition_use.loc[partition_use["split_role"].astype(str).eq("unassigned"), "rows_joined"].sum()) if not partition_use.empty else 0
    max_decision_rate = as_float(candidate.get("max_decision_rate", 0.0))
    decision_rate = as_float(interp.get("decision_rate", 1.0))
    return pd.DataFrame(
        [
            {"gate_id": "P193_PHASE191_HASH_MATCH", "gate_pass": int(str(candidate.get("candidate_contract_hash", "")) == EXPECTED_CONTRACT_HASH), "evidence": f"candidate_contract_hash={candidate.get('candidate_contract_hash', '')}", "severity": "hard"},
            {"gate_id": "P193_EXTENSION_ROWS_PRESENT", "gate_pass": int(extension_rows > 0), "evidence": f"unassigned_extension_rows={extension_rows}", "severity": "hard"},
            {"gate_id": "P193_TEST_UNTOUCHED_EXCLUDED", "gate_pass": int(test_partitions_used == 0), "evidence": f"test_partitions_used={test_partitions_used}", "severity": "hard"},
            {"gate_id": "P193_DATE_SYMBOL_AUDITS_PRESENT", "gate_pass": int(not by_date.empty and not by_symbol.empty), "evidence": f"date_rows={len(by_date)}; symbol_rows={len(by_symbol)}", "severity": "hard"},
            {"gate_id": "P193_NEGATIVE_CONTROLS_PRESENT", "gate_pass": int(not interpretation.empty and "min_profile_edge_over_shuffled_time_bps" in interpretation.columns and "min_profile_edge_over_shuffled_symbol_bps" in interpretation.columns), "evidence": "shuffled_time;shuffled_symbol", "severity": "hard"},
            {"gate_id": "P193_DECISION_RATE_BUDGET_RESPECTED", "gate_pass": int(decision_rate <= max_decision_rate), "evidence": f"decision_rate={decision_rate}; max_decision_rate={max_decision_rate}", "severity": "hard"},
            {"gate_id": "P193_NO_TEST_REPLAY_OR_PROMOTION", "gate_pass": int(not interpretation.empty and int(interp.get("test_replay_allowed_by_phase193", 1)) == 0 and int(interp.get("promotion_allowed", 1)) == 0), "evidence": "test_replay_allowed_by_phase193=0; promotion_allowed=0", "severity": "hard"},
        ]
    )


def acceptance_rows(interpretation: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates.loc[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(int).sum()) if not hard.empty else 0
    interp = interpretation.iloc[0] if not interpretation.empty else {}
    rows = [
        ("phase193_interpretation_rows", int(len(interpretation)), "Interpretation rows"),
        ("phase193_gate_rows", int(len(gates)), "Gates evaluated"),
        ("phase193_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
        ("phase193_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase193_candidate_id", interp.get("candidate_id", ""), "Frozen candidate evaluated"),
        ("phase193_candidate_contract_hash", interp.get("candidate_contract_hash", ""), "Frozen contract hash"),
        ("phase193_original_validation_dates", interp.get("original_validation_dates", ""), "Original validation dates represented in events"),
        ("phase193_extension_validation_dates", interp.get("extension_validation_dates", ""), "Added validation-extension dates represented in events"),
        ("phase193_validation_dates_with_events", interp.get("validation_dates_with_events", ""), "Validation/extension dates with decision events"),
        ("phase193_validation_extension_decision_events", interp.get("validation_extension_decision_events", ""), "Dry decision events across validation plus extension"),
        ("phase193_decision_rate", interp.get("decision_rate", ""), "Decision-event rate over evaluation rows"),
        ("phase193_min_profile_net_bps_proxy_mean", interp.get("min_profile_net_bps_proxy_mean", ""), "Minimum profile net bps"),
        ("phase193_min_profile_edge_over_shuffled_time_bps", interp.get("min_profile_edge_over_shuffled_time_bps", ""), "Minimum profile edge over shuffled-time control"),
        ("phase193_min_profile_edge_over_shuffled_symbol_bps", interp.get("min_profile_edge_over_shuffled_symbol_bps", ""), "Minimum profile edge over shuffled-symbol control"),
        ("phase193_symbol_positive_fraction", interp.get("symbol_positive_fraction", ""), "Fraction of symbol/profile groups net positive"),
        ("phase193_breadth_warning", interp.get("breadth_warning", ""), "1 means symbol breadth remains weak"),
        ("phase193_date_count_warning", interp.get("date_count_warning", ""), "1 means fewer than two validation dates"),
        ("phase193_concentration_warning", interp.get("concentration_warning", ""), "1 means event concentration warning"),
        ("phase193_verdict", interp.get("phase193_verdict", ""), "Validation-breadth verdict"),
        ("phase193_validation_breadth_extension_complete", int(len(hard) > 0 and hard_pass == len(hard)), "1 means Phase193 completed"),
        ("phase193_test_replay_execution", 0, "No untouched test replay executed"),
        ("phase193_test_result_allowed", 0, "No test result emitted"),
        ("phase193_promotion_allowed", 0, "No promotion opened"),
        ("phase193_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
        ("phase193_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
        ("phase193_next_best_action", "add_more_validation_dates_or_redesign_before_any_test_replay", "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase193 Validation Breadth Extension Replay",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase193 evaluates the Phase191 frozen sparse candidate on original validation plus newly downloaded unassigned real dates.",
        "It excludes `test_untouched`, emits no orders/fills/P&L, and does not open promotion or paper/live acceptance.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase193_validation_breadth_extension_replay_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase193(phase176_dir: Path, phase180_dir: Path, phase181_dir: Path, phase191_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    candidate = frozen_candidate(phase191_dir)
    feature_inventory = read_csv(phase176_dir / "phase176_feature_partition_inventory.csv")
    label_inventory = read_csv(phase181_dir / "phase181_label_partition_inventory.csv")
    latency_profiles = read_csv(phase180_dir / "phase180_latency_slippage_profile_catalog.csv")
    allowed_profiles = [item.strip() for item in str(candidate.get("allowed_latency_profiles", "")).split(";") if item.strip()]
    profiles = latency_profiles.loc[latency_profiles["profile_id"].astype(str).isin(allowed_profiles)].copy()
    frame, partition_use = build_model_frame(feature_inventory, label_inventory)
    frame = add_derived_fields(frame)
    partition_use = build_partition_use(partition_use)
    rng = np.random.default_rng(RANDOM_SEED)
    events = pd.concat([selected_extension_events(frame, candidate, pd.Series(profile), rng) for profile in profiles.to_dict("records")], ignore_index=True)
    by_date = summarize_group(events, ["candidate_id", "latency_profile_id", "split_role", "trade_date"])
    by_symbol = summarize_group(events, ["candidate_id", "latency_profile_id", "symbol"])
    interpretation = build_interpretation(events, frame, by_date, by_symbol)
    gates = build_gates(candidate, partition_use, interpretation, by_date, by_symbol)
    acceptance = acceptance_rows(interpretation, gates)

    events.to_csv(output_dir / "phase193_validation_extension_event_audit.csv", index=False)
    by_date.to_csv(output_dir / "phase193_validation_extension_by_date.csv", index=False)
    by_symbol.to_csv(output_dir / "phase193_validation_extension_by_symbol.csv", index=False)
    partition_use.to_csv(output_dir / "phase193_partition_use_audit.csv", index=False)
    interpretation.to_csv(output_dir / "phase193_validation_breadth_extension_interpretation.csv", index=False)
    gates.to_csv(output_dir / "phase193_validation_breadth_extension_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase193_validation_breadth_extension_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Interpretation": interpretation,
            "By Date": by_date,
            "By Symbol": by_symbol,
            "Gate Evaluation": gates,
        },
    )

    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase193_validation_breadth_extension_replay_no_test",
        **reproducibility_fields(
            artifact_id="phase193_validation_breadth_extension_replay",
            generated_utc=generated,
            inputs={
                "phase176_feature_inventory": str(phase176_dir / "phase176_feature_partition_inventory.csv"),
                "phase181_label_inventory": str(phase181_dir / "phase181_label_partition_inventory.csv"),
                "phase180_latency_profiles": str(phase180_dir / "phase180_latency_slippage_profile_catalog.csv"),
                "phase191_frozen_candidate": str(phase191_dir / "phase191_frozen_candidate_contract.csv"),
            },
            parameters={
                "evaluation_split_roles": ";".join(sorted(EVALUATION_ROLES)),
                "excluded_split_roles": "test_untouched",
                "expected_candidate_contract_hash": EXPECTED_CONTRACT_HASH,
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "event_audit": str(output_dir / "phase193_validation_extension_event_audit.csv"),
                "by_date": str(output_dir / "phase193_validation_extension_by_date.csv"),
                "by_symbol": str(output_dir / "phase193_validation_extension_by_symbol.csv"),
                "partition_use": str(output_dir / "phase193_partition_use_audit.csv"),
                "interpretation": str(output_dir / "phase193_validation_breadth_extension_interpretation.csv"),
                "gate_evaluation": str(output_dir / "phase193_validation_breadth_extension_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase193_validation_breadth_extension_acceptance_summary.csv"),
                "report": str(output_dir / "phase193_validation_breadth_extension_replay_report.md"),
            },
            random_seed=str(RANDOM_SEED),
            scenario_ids="phase193_validation_breadth_extension_replay_no_test",
            cost_model_version="phase180_latency_slippage_profile_catalog",
            latency_model_version="phase180_latency_slippage_profile_catalog",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase193_validation_breadth_extension_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase176-dir", type=Path, default=DEFAULT_PHASE176_DIR)
    parser.add_argument("--phase180-dir", type=Path, default=DEFAULT_PHASE180_DIR)
    parser.add_argument("--phase181-dir", type=Path, default=DEFAULT_PHASE181_DIR)
    parser.add_argument("--phase191-dir", type=Path, default=DEFAULT_PHASE191_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase193(args.phase176_dir, args.phase180_dir, args.phase181_dir, args.phase191_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
