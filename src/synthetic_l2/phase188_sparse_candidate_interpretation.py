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
DEFAULT_PHASE187_DIR = Path("outputs/phase187")
DEFAULT_OUTPUT_DIR = Path("outputs/phase188")
RANDOM_SEED = 188
FORBIDDEN_OUTPUTS = "test_result;test_replay;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = "") -> Any:
    if frame.empty or "metric" not in frame.columns or "value" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def best_candidate_row(phase187_acceptance: pd.DataFrame, selected: pd.DataFrame) -> pd.Series:
    candidate_id = str(metric_value(phase187_acceptance, "phase187_best_validation_candidate_id", ""))
    rows = selected.loc[selected["candidate_id"].astype(str).eq(candidate_id)]
    if rows.empty:
        raise ValueError(f"Best Phase187 candidate not found in selected candidates: {candidate_id}")
    return rows.iloc[0]


def selected_validation_events(frame: pd.DataFrame, candidate: pd.Series, profile: pd.Series, rng: np.random.Generator) -> pd.DataFrame:
    validation = frame.loc[frame["split_role"].astype(str).eq("validation")].copy()
    mask, side = candidate_mask(validation, candidate)
    selected = validation.loc[mask].copy()
    selected["candidate_id"] = candidate["candidate_id"]
    selected["latency_profile_id"] = profile["profile_id"]
    selected["dry_side"] = side.loc[mask].astype(int)
    selected["gross_return_bps_proxy"] = selected["dry_side"] * pd.to_numeric(selected["future_mid_return_bps_next_bucket"], errors="coerce")
    selected["cost_bound_bps"] = profile_cost_bps(selected, profile)
    selected["net_return_bps_after_cost_proxy"] = selected["gross_return_bps_proxy"] - selected["cost_bound_bps"]
    shuffled = pd.to_numeric(selected["future_mid_return_bps_next_bucket"], errors="coerce").to_numpy(copy=True)
    rng.shuffle(shuffled)
    selected["shuffled_time_net_bps_proxy"] = selected["dry_side"].to_numpy() * shuffled - selected["cost_bound_bps"].to_numpy()
    selected["net_edge_over_shuffled_time_bps"] = selected["net_return_bps_after_cost_proxy"] - selected["shuffled_time_net_bps_proxy"]
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
            net_edge_over_shuffled_time_bps_mean=("net_edge_over_shuffled_time_bps", "mean"),
        )
    )
    out["net_positive_group"] = (out["net_return_bps_after_cost_proxy_mean"] > 0).astype(int)
    out["beats_shuffled_group"] = (out["net_edge_over_shuffled_time_bps_mean"] > 0).astype(int)
    return out


def build_interpretation(events: pd.DataFrame, by_date: pd.DataFrame, by_symbol: pd.DataFrame) -> pd.DataFrame:
    if events.empty:
        return pd.DataFrame()
    total_events = len(events)
    by_symbol_rank = by_symbol.sort_values("decision_events", ascending=False).copy()
    top_symbol_share = float(by_symbol_rank["decision_events"].iloc[0] / total_events) if len(by_symbol_rank) else 1.0
    top3_symbol_share = float(by_symbol_rank["decision_events"].head(3).sum() / total_events) if len(by_symbol_rank) else 1.0
    date_positive_fraction = float(by_date["net_positive_group"].mean()) if not by_date.empty else 0.0
    symbol_positive_fraction = float(by_symbol["net_positive_group"].mean()) if not by_symbol.empty else 0.0
    min_profile_net = float(events.groupby("latency_profile_id")["net_return_bps_after_cost_proxy"].mean().min())
    min_profile_control_edge = float(events.groupby("latency_profile_id")["net_edge_over_shuffled_time_bps"].mean().min())
    breadth_warning = int(symbol_positive_fraction < 0.25)
    date_count_warning = int(events["trade_date"].nunique() < 2)
    concentration_warning = int(top_symbol_share > 0.35 or top3_symbol_share > 0.70)
    if min_profile_net > 0 and min_profile_control_edge > 0 and concentration_warning == 0 and breadth_warning == 0 and date_count_warning == 0:
        robustness_interpretation = "promising_broad_enough_for_test_replay_precommit_review"
    elif min_profile_net > 0 and min_profile_control_edge > 0:
        robustness_interpretation = "promising_but_breadth_limited_requires_phase189_precommit_or_redesign_decision"
    else:
        robustness_interpretation = "needs_redesign_or_manual_review"
    return pd.DataFrame(
        [
            {
                "candidate_id": str(events["candidate_id"].iloc[0]),
                "validation_decision_events": int(total_events),
                "validation_symbols_with_events": int(events["symbol"].nunique()),
                "validation_dates_with_events": int(events["trade_date"].nunique()),
                "overall_net_bps_proxy_mean": float(events["net_return_bps_after_cost_proxy"].mean()),
                "overall_gross_bps_proxy_mean": float(events["gross_return_bps_proxy"].mean()),
                "overall_cost_bps_mean": float(events["cost_bound_bps"].mean()),
                "min_profile_net_bps_proxy_mean": min_profile_net,
                "min_profile_edge_over_shuffled_bps": min_profile_control_edge,
                "date_positive_fraction": date_positive_fraction,
                "symbol_positive_fraction": symbol_positive_fraction,
                "top_symbol_event_share": top_symbol_share,
                "top3_symbol_event_share": top3_symbol_share,
                "concentration_warning": concentration_warning,
                "breadth_warning": breadth_warning,
                "date_count_warning": date_count_warning,
                "robustness_interpretation": robustness_interpretation,
                "test_replay_allowed_by_phase188": 0,
                "promotion_allowed": 0,
            }
        ]
    )


def build_gate_evaluation(phase187: pd.DataFrame, interpretation: pd.DataFrame, by_date: pd.DataFrame, by_symbol: pd.DataFrame) -> pd.DataFrame:
    candidate_complete = as_int(metric_value(phase187, "phase187_cost_aware_sparse_candidate_complete", 0))
    positive_all_profiles = as_int(metric_value(phase187, "phase187_validation_positive_all_profiles", 0))
    interp = interpretation.iloc[0] if not interpretation.empty else {}
    return pd.DataFrame(
        [
            {"gate_id": "P188_PHASE187_CANDIDATE_COMPLETE", "gate_pass": int(candidate_complete == 1), "evidence": f"phase187_cost_aware_sparse_candidate_complete={candidate_complete}", "severity": "hard"},
            {"gate_id": "P188_VALIDATION_POSITIVE_ALL_PROFILES_ACKNOWLEDGED", "gate_pass": int(positive_all_profiles == 1), "evidence": f"phase187_validation_positive_all_profiles={positive_all_profiles}", "severity": "hard"},
            {"gate_id": "P188_DATE_SYMBOL_CONCENTRATION_AUDIT_PRESENT", "gate_pass": int(not by_date.empty and not by_symbol.empty), "evidence": f"date_rows={len(by_date)}; symbol_rows={len(by_symbol)}", "severity": "hard"},
            {"gate_id": "P188_NEGATIVE_CONTROL_MARGIN_POSITIVE", "gate_pass": int(float(interp.get("min_profile_edge_over_shuffled_bps", 0)) > 0), "evidence": f"min_profile_edge_over_shuffled_bps={interp.get('min_profile_edge_over_shuffled_bps', '')}", "severity": "hard"},
            {"gate_id": "P188_CONCENTRATION_REVIEW_RECORDED", "gate_pass": int("concentration_warning" in interpretation.columns), "evidence": f"concentration_warning={interp.get('concentration_warning', '')}", "severity": "hard"},
            {"gate_id": "P188_BREADTH_REVIEW_RECORDED", "gate_pass": int("breadth_warning" in interpretation.columns and "date_count_warning" in interpretation.columns), "evidence": f"breadth_warning={interp.get('breadth_warning', '')}; date_count_warning={interp.get('date_count_warning', '')}", "severity": "hard"},
            {"gate_id": "P188_NO_TEST_REPLAY_OR_PROMOTION", "gate_pass": int(not interpretation.empty and int(interp.get("test_replay_allowed_by_phase188", 1)) == 0 and int(interp.get("promotion_allowed", 1)) == 0), "evidence": "test_replay_allowed_by_phase188=0; promotion_allowed=0", "severity": "hard"},
        ]
    )


def build_acceptance_summary(interpretation: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates.loc[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(int).sum()) if not hard.empty else 0
    interp = interpretation.iloc[0] if not interpretation.empty else {}
    rows = [
        ("phase188_interpretation_rows", int(len(interpretation)), "Interpretation rows"),
        ("phase188_gate_rows", int(len(gates)), "Gates evaluated"),
        ("phase188_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
        ("phase188_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase188_candidate_id", interp.get("candidate_id", ""), "Interpreted candidate"),
        ("phase188_validation_decision_events", interp.get("validation_decision_events", ""), "Validation dry decision events interpreted"),
        ("phase188_min_profile_net_bps_proxy_mean", interp.get("min_profile_net_bps_proxy_mean", ""), "Minimum profile validation net bps"),
        ("phase188_min_profile_edge_over_shuffled_bps", interp.get("min_profile_edge_over_shuffled_bps", ""), "Minimum profile edge over shuffled-time control"),
        ("phase188_top_symbol_event_share", interp.get("top_symbol_event_share", ""), "Top symbol decision-event share"),
        ("phase188_top3_symbol_event_share", interp.get("top3_symbol_event_share", ""), "Top 3 symbol decision-event share"),
        ("phase188_concentration_warning", interp.get("concentration_warning", ""), "1 means concentration review warning"),
        ("phase188_symbol_positive_fraction", interp.get("symbol_positive_fraction", ""), "Fraction of symbol/profile groups net positive"),
        ("phase188_breadth_warning", interp.get("breadth_warning", ""), "1 means symbol breadth is weak"),
        ("phase188_date_count_warning", interp.get("date_count_warning", ""), "1 means validation evidence has fewer than two dates"),
        ("phase188_robustness_interpretation", interp.get("robustness_interpretation", ""), "Interpretation verdict"),
        ("phase188_interpretation_complete", int(len(hard) > 0 and hard_pass == len(hard)), "1 means Phase188 interpretation completed"),
        ("phase188_test_replay_allowed_next", 0, "No test replay opened by Phase188"),
        ("phase188_promotion_allowed", 0, "No promotion opened"),
        ("phase188_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
        ("phase188_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
        ("phase188_next_best_action", "build_phase189_untouched_test_replay_precommit_or_redesign_decision", "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, interpretation: pd.DataFrame, by_date: pd.DataFrame, by_symbol: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase188 Cost-aware Sparse Candidate Interpretation",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase188 interprets the Phase187 validation-positive sparse candidate without opening test replay or promotion.",
        "It audits date/symbol concentration, negative-control margin and profile robustness.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Interpretation",
        "",
        _markdown_table(interpretation),
        "",
        "## By Date",
        "",
        _markdown_table(by_date),
        "",
        "## By Symbol",
        "",
        _markdown_table(by_symbol.sort_values("decision_events", ascending=False).head(40) if not by_symbol.empty else by_symbol),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
    ]
    (output_dir / "phase188_sparse_candidate_interpretation_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase188(phase176_dir: Path, phase180_dir: Path, phase181_dir: Path, phase187_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase187 = read_csv(phase187_dir / "phase187_cost_aware_sparse_candidate_acceptance_summary.csv")
    selected = read_csv(phase187_dir / "phase187_train_selected_candidates.csv")
    feature_inventory = read_csv(phase176_dir / "phase176_feature_partition_inventory.csv")
    label_inventory = read_csv(phase181_dir / "phase181_label_partition_inventory.csv")
    latency_profiles = read_csv(phase180_dir / "phase180_latency_slippage_profile_catalog.csv")
    frame, _partition_use = build_model_frame(feature_inventory, label_inventory)
    frame = add_derived_fields(frame)
    candidate = best_candidate_row(phase187, selected)
    profiles = latency_profiles.loc[latency_profiles["profile_id"].astype(str).isin(["P180_RETAIL_MARKETABLE_DEFAULT", "P180_STRESSED_RETAIL"])].copy()
    rng = np.random.default_rng(RANDOM_SEED)
    events = pd.concat([selected_validation_events(frame, candidate, pd.Series(profile), rng) for profile in profiles.to_dict("records")], ignore_index=True)
    by_date = summarize_group(events, ["candidate_id", "latency_profile_id", "trade_date"])
    by_symbol = summarize_group(events, ["candidate_id", "latency_profile_id", "symbol"])
    interpretation = build_interpretation(events, by_date, by_symbol)
    gates = build_gate_evaluation(phase187, interpretation, by_date, by_symbol)
    acceptance = build_acceptance_summary(interpretation, gates)

    events.to_csv(output_dir / "phase188_validation_event_audit.csv", index=False)
    by_date.to_csv(output_dir / "phase188_validation_by_date.csv", index=False)
    by_symbol.to_csv(output_dir / "phase188_validation_by_symbol.csv", index=False)
    interpretation.to_csv(output_dir / "phase188_sparse_candidate_interpretation.csv", index=False)
    gates.to_csv(output_dir / "phase188_sparse_candidate_interpretation_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase188_sparse_candidate_interpretation_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, interpretation, by_date, by_symbol, gates)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase188_cost_aware_sparse_candidate_interpretation_no_test",
        **reproducibility_fields(
            artifact_id="phase188_sparse_candidate_interpretation",
            generated_utc=generated_utc,
            inputs={
                "phase187_acceptance": str(phase187_dir / "phase187_cost_aware_sparse_candidate_acceptance_summary.csv"),
                "phase187_selected": str(phase187_dir / "phase187_train_selected_candidates.csv"),
                "phase176_feature_inventory": str(phase176_dir / "phase176_feature_partition_inventory.csv"),
                "phase181_label_inventory": str(phase181_dir / "phase181_label_partition_inventory.csv"),
                "phase180_latency_profiles": str(phase180_dir / "phase180_latency_slippage_profile_catalog.csv"),
            },
            parameters={"random_seed": RANDOM_SEED, "test_replay_allowed_next": 0, "promotion_allowed": 0},
            outputs={
                "event_audit": str(output_dir / "phase188_validation_event_audit.csv"),
                "by_date": str(output_dir / "phase188_validation_by_date.csv"),
                "by_symbol": str(output_dir / "phase188_validation_by_symbol.csv"),
                "interpretation": str(output_dir / "phase188_sparse_candidate_interpretation.csv"),
                "gate_evaluation": str(output_dir / "phase188_sparse_candidate_interpretation_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase188_sparse_candidate_interpretation_acceptance_summary.csv"),
                "report": str(output_dir / "phase188_sparse_candidate_interpretation_report.md"),
            },
            random_seed=RANDOM_SEED,
            scenario_ids="phase188_cost_aware_sparse_candidate_interpretation_no_test",
            cost_model_version="phase180_zerodha_equity_intraday_cost_bound_proxy",
            latency_model_version="phase180_retail_marketable_default_and_stressed_retail",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase188_sparse_candidate_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase176-dir", type=Path, default=DEFAULT_PHASE176_DIR)
    parser.add_argument("--phase180-dir", type=Path, default=DEFAULT_PHASE180_DIR)
    parser.add_argument("--phase181-dir", type=Path, default=DEFAULT_PHASE181_DIR)
    parser.add_argument("--phase187-dir", type=Path, default=DEFAULT_PHASE187_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase188(args.phase176_dir, args.phase180_dir, args.phase181_dir, args.phase187_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
