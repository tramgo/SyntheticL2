from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase184_train_validation_replay_dry_run import build_model_frame, profile_cost_bps
from synthetic_l2.phase187_cost_aware_sparse_candidate import add_derived_fields
from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE176_DIR = Path("outputs/phase176")
DEFAULT_PHASE180_DIR = Path("outputs/phase180")
DEFAULT_PHASE181_DIR = Path("outputs/phase181")
DEFAULT_PHASE194_DIR = Path("outputs/phase194")
DEFAULT_OUTPUT_DIR = Path("outputs/phase195")
RANDOM_SEED = 195
ALLOWED_PROFILES = {"P180_RETAIL_MARKETABLE_DEFAULT", "P180_STRESSED_RETAIL"}
EVALUATION_ROLES = {"validation", "unassigned"}
FORBIDDEN_OUTPUTS = "test_result;test_replay_execution;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim"


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


def candidate_grid() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for imbalance_source in ["top5", "l1"]:
        for side_mode in ["follow_imbalance", "fade_imbalance"]:
            for min_imbalance in [0.60, 0.70, 0.80, 0.90]:
                for max_spread_bps in [1.5, 2.5, 5.0]:
                    for min_abs_event_zscore in [0.0, 1.0, 2.0]:
                        for min_quote_churn in [0, 1]:
                            for max_decision_rate in [0.005, 0.01]:
                                rows.append(
                                    {
                                        "candidate_id": (
                                            "P195_"
                                            f"{imbalance_source.upper()}_"
                                            f"{side_mode.replace('_imbalance', '').upper()}_"
                                            f"I{int(min_imbalance * 100)}_"
                                            f"S{str(max_spread_bps).replace('.', 'p')}_"
                                            f"Z{int(min_abs_event_zscore)}_"
                                            f"Q{min_quote_churn}_"
                                            f"R{int(max_decision_rate * 10000)}"
                                        ),
                                        "imbalance_source": imbalance_source,
                                        "side_mode": side_mode,
                                        "min_abs_imbalance": min_imbalance,
                                        "max_spread_bps": max_spread_bps,
                                        "min_abs_event_zscore": min_abs_event_zscore,
                                        "min_quote_churn_count": min_quote_churn,
                                        "max_decision_rate": max_decision_rate,
                                        "test_replay_allowed_in_phase195": 0,
                                    }
                                )
    return pd.DataFrame(rows)


def candidate_mask_and_side(frame: pd.DataFrame, candidate: pd.Series) -> tuple[pd.Series, pd.Series]:
    if str(candidate["imbalance_source"]) == "top5":
        imbalance_abs = frame["abs_top5_qty_imbalance"]
        raw_side = np.sign(pd.to_numeric(frame["top5_qty_imbalance"], errors="coerce").fillna(0.0)).astype("int8")
    else:
        imbalance_abs = frame["abs_l1_qty_imbalance"]
        raw_side = np.sign(pd.to_numeric(frame["l1_qty_imbalance"], errors="coerce").fillna(0.0)).astype("int8")
    side = -raw_side if str(candidate["side_mode"]) == "fade_imbalance" else raw_side
    mask = (
        imbalance_abs.ge(float(candidate["min_abs_imbalance"]))
        & frame["spread_bps"].le(float(candidate["max_spread_bps"]))
        & frame["abs_receive_event_rate_zscore"].ge(float(candidate["min_abs_event_zscore"]))
        & pd.to_numeric(frame["quote_churn_count"], errors="coerce").fillna(0).ge(float(candidate["min_quote_churn_count"]))
        & side.ne(0)
    )
    return mask, pd.Series(side, index=frame.index)


def selected_events(frame: pd.DataFrame, candidate: pd.Series, profile: pd.Series, rng: np.random.Generator) -> pd.DataFrame:
    mask, side = candidate_mask_and_side(frame, candidate)
    selected = frame.loc[mask].copy()
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


def summarize_candidate(frame: pd.DataFrame, candidate: pd.Series, profile: pd.Series, rng: np.random.Generator, split_bucket: str) -> dict[str, Any]:
    events = selected_events(frame, candidate, profile, rng)
    max_rate = float(candidate["max_decision_rate"])
    return {
        "candidate_id": candidate["candidate_id"],
        "latency_profile_id": profile["profile_id"],
        "split_bucket": split_bucket,
        "decision_events": int(len(events)),
        "decision_rate": float(len(events) / len(frame)) if len(frame) else 0.0,
        "max_decision_rate": max_rate,
        "decision_rate_pass": int((len(events) / len(frame) if len(frame) else 0.0) <= max_rate),
        "dates_with_events": int(events["trade_date"].nunique()) if len(events) else 0,
        "symbols_with_events": int(events["symbol"].nunique()) if len(events) else 0,
        "net_return_bps_after_cost_proxy_mean": float(events["net_return_bps_after_cost_proxy"].mean()) if len(events) else np.nan,
        "gross_return_bps_proxy_mean": float(events["gross_return_bps_proxy"].mean()) if len(events) else np.nan,
        "cost_bound_bps_mean": float(events["cost_bound_bps"].mean()) if len(events) else np.nan,
        "net_edge_over_shuffled_time_bps_mean": float(events["net_edge_over_shuffled_time_bps"].mean()) if len(events) else np.nan,
        "net_positive_event_fraction": float((events["net_return_bps_after_cost_proxy"] > 0).mean()) if len(events) else np.nan,
        "test_rows_used": 0,
        "promotion_allowed": 0,
    }


def summarize_by_date_symbol(events: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if events.empty:
        empty = pd.DataFrame()
        return empty, empty
    by_date = (
        events.groupby(["candidate_id", "latency_profile_id", "split_role", "trade_date"], as_index=False)
        .agg(
            decision_events=("bucket_ms", "count"),
            symbols=("symbol", "nunique"),
            net_return_bps_after_cost_proxy_mean=("net_return_bps_after_cost_proxy", "mean"),
            net_edge_over_shuffled_time_bps_mean=("net_edge_over_shuffled_time_bps", "mean"),
        )
    )
    by_date["net_positive_group"] = (by_date["net_return_bps_after_cost_proxy_mean"] > 0).astype(int)
    by_date["beats_shuffled_time_group"] = (by_date["net_edge_over_shuffled_time_bps_mean"] > 0).astype(int)
    by_symbol = (
        events.groupby(["candidate_id", "latency_profile_id", "symbol"], as_index=False)
        .agg(
            decision_events=("bucket_ms", "count"),
            dates=("trade_date", "nunique"),
            net_return_bps_after_cost_proxy_mean=("net_return_bps_after_cost_proxy", "mean"),
            net_edge_over_shuffled_time_bps_mean=("net_edge_over_shuffled_time_bps", "mean"),
        )
    )
    by_symbol["net_positive_group"] = (by_symbol["net_return_bps_after_cost_proxy_mean"] > 0).astype(int)
    by_symbol["beats_shuffled_time_group"] = (by_symbol["net_edge_over_shuffled_time_bps_mean"] > 0).astype(int)
    return by_date, by_symbol


def run_search(frame: pd.DataFrame, candidates: pd.DataFrame, profiles: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(RANDOM_SEED)
    train = frame.loc[frame["split_role"].astype(str).eq("train")].copy()
    validation = frame.loc[frame["split_role"].astype(str).eq("validation")].copy()
    extension = frame.loc[frame["split_role"].astype(str).eq("unassigned")].copy()
    evaluation = frame.loc[frame["split_role"].astype(str).isin(EVALUATION_ROLES)].copy()
    train_rows: list[dict[str, Any]] = []
    for cand in candidates.to_dict("records"):
        cand_s = pd.Series(cand)
        for prof in profiles.to_dict("records"):
            train_rows.append(summarize_candidate(train, cand_s, pd.Series(prof), rng, "train"))
    train_summary = pd.DataFrame(train_rows)
    eligible = train_summary.loc[
        train_summary["decision_events"].ge(100)
        & train_summary["decision_rate_pass"].astype(int).eq(1)
        & train_summary["net_return_bps_after_cost_proxy_mean"].gt(0)
        & train_summary["net_edge_over_shuffled_time_bps_mean"].gt(0)
    ].copy()
    train_rollup = (
        eligible.groupby("candidate_id", as_index=False)
        .agg(
            min_train_net_bps=("net_return_bps_after_cost_proxy_mean", "min"),
            min_train_edge_bps=("net_edge_over_shuffled_time_bps_mean", "min"),
            max_train_decision_rate=("decision_rate", "max"),
            min_train_events=("decision_events", "min"),
        )
        if not eligible.empty
        else pd.DataFrame(columns=["candidate_id", "min_train_net_bps", "min_train_edge_bps", "max_train_decision_rate", "min_train_events"])
    )
    selected = train_rollup.sort_values(["min_train_net_bps", "min_train_edge_bps"], ascending=False).head(24)
    selected = selected.merge(candidates, on="candidate_id", how="left")
    selected["selected_by_phase195_train_only"] = 1
    selected["validation_used_for_selection"] = 0
    selected["extension_used_for_selection"] = 0
    selected["test_used_for_selection"] = 0

    evaluation_rows: list[dict[str, Any]] = []
    all_eval_events: list[pd.DataFrame] = []
    for cand in selected.to_dict("records"):
        cand_s = pd.Series(cand)
        for prof in profiles.to_dict("records"):
            prof_s = pd.Series(prof)
            evaluation_rows.append(summarize_candidate(validation, cand_s, prof_s, rng, "validation"))
            evaluation_rows.append(summarize_candidate(extension, cand_s, prof_s, rng, "validation_extension"))
            events = selected_events(evaluation, cand_s, prof_s, rng)
            all_eval_events.append(events)
    evaluation_summary = pd.DataFrame(evaluation_rows)
    event_audit = pd.concat(all_eval_events, ignore_index=True) if all_eval_events else pd.DataFrame()
    by_date, by_symbol = summarize_by_date_symbol(event_audit)
    if not evaluation_summary.empty:
        evaluation_summary = evaluation_summary.merge(
            selected[["candidate_id", "min_train_net_bps", "min_train_edge_bps", "max_train_decision_rate"]],
            on="candidate_id",
            how="left",
        )
    return train_summary, selected, evaluation_summary, by_date, by_symbol


def build_candidate_decision(selected: pd.DataFrame, evaluation: pd.DataFrame, by_date: pd.DataFrame, by_symbol: pd.DataFrame) -> pd.DataFrame:
    if selected.empty or evaluation.empty or by_date.empty or by_symbol.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    selected_lookup = selected.set_index("candidate_id")
    for candidate_id in selected["candidate_id"].astype(str).tolist():
        eval_rows = evaluation.loc[evaluation["candidate_id"].astype(str).eq(candidate_id)].copy()
        date_rows = by_date.loc[by_date["candidate_id"].astype(str).eq(candidate_id)].copy()
        symbol_rows = by_symbol.loc[by_symbol["candidate_id"].astype(str).eq(candidate_id)].copy()
        by_date_positive_fraction = float(date_rows["net_positive_group"].mean()) if not date_rows.empty else 0.0
        by_date_control_fraction = float(date_rows["beats_shuffled_time_group"].mean()) if not date_rows.empty else 0.0
        by_symbol_positive_fraction = float(symbol_rows["net_positive_group"].mean()) if not symbol_rows.empty else 0.0
        min_extension_net = float(eval_rows.loc[eval_rows["split_bucket"].eq("validation_extension"), "net_return_bps_after_cost_proxy_mean"].min()) if not eval_rows.empty else np.nan
        min_validation_net = float(eval_rows.loc[eval_rows["split_bucket"].eq("validation"), "net_return_bps_after_cost_proxy_mean"].min()) if not eval_rows.empty else np.nan
        passes = int(
            by_date_positive_fraction >= 1.0
            and by_date_control_fraction >= 1.0
            and by_symbol_positive_fraction >= 0.25
            and np.isfinite(min_extension_net)
            and min_extension_net > 0
            and np.isfinite(min_validation_net)
            and min_validation_net > 0
        )
        row = selected_lookup.loc[candidate_id].to_dict()
        rows.append(
            {
                "candidate_id": candidate_id,
                "min_train_net_bps": row.get("min_train_net_bps", np.nan),
                "min_validation_net_bps": min_validation_net,
                "min_extension_net_bps": min_extension_net,
                "date_positive_fraction": by_date_positive_fraction,
                "date_control_positive_fraction": by_date_control_fraction,
                "symbol_positive_fraction": by_symbol_positive_fraction,
                "validation_extension_gate_pass": passes,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["validation_extension_gate_pass", "min_extension_net_bps", "date_positive_fraction", "symbol_positive_fraction"],
        ascending=False,
    )


def build_partition_use(partition_use: pd.DataFrame) -> pd.DataFrame:
    if partition_use.empty:
        return partition_use
    out = partition_use.copy()
    out["used_in_phase195_train_selection"] = out["split_role"].astype(str).eq("train").astype(int)
    out["used_in_phase195_validation_screen"] = out["split_role"].astype(str).isin(EVALUATION_ROLES).astype(int)
    out.loc[out["split_role"].astype(str).eq("test_untouched"), ["used_in_phase195_train_selection", "used_in_phase195_validation_screen"]] = 0
    return out


def build_gates(phase194: pd.DataFrame, partition_use: pd.DataFrame, selected: pd.DataFrame, decisions: pd.DataFrame) -> pd.DataFrame:
    phase194_complete = as_int(metric_value(phase194, "phase194_fragility_decision_complete", 0))
    test_rows_used = int(partition_use.loc[partition_use["split_role"].astype(str).eq("test_untouched"), "used_in_phase195_validation_screen"].sum()) if not partition_use.empty else 0
    passing_candidates = int(decisions["validation_extension_gate_pass"].astype(int).sum()) if not decisions.empty else 0
    return pd.DataFrame(
        [
            {"gate_id": "P195_PHASE194_CLOSURE_COMPLETE", "gate_pass": int(phase194_complete == 1), "evidence": f"phase194_fragility_decision_complete={phase194_complete}", "severity": "hard"},
            {"gate_id": "P195_TRAIN_ONLY_SELECTION", "gate_pass": int(not selected.empty and selected["validation_used_for_selection"].astype(int).eq(0).all() and selected["extension_used_for_selection"].astype(int).eq(0).all() and selected["test_used_for_selection"].astype(int).eq(0).all()), "evidence": f"selected_candidate_rows={len(selected)}", "severity": "hard"},
            {"gate_id": "P195_VALIDATION_EXTENSION_EVALUATED_NO_TEST", "gate_pass": int(test_rows_used == 0 and not decisions.empty), "evidence": f"test_rows_used={test_rows_used}; decision_rows={len(decisions)}", "severity": "hard"},
            {"gate_id": "P195_DATE_AND_SYMBOL_BREADTH_GATES_APPLIED", "gate_pass": int(not decisions.empty and {'date_positive_fraction', 'symbol_positive_fraction', 'validation_extension_gate_pass'}.issubset(decisions.columns)), "evidence": "date_positive_fraction;symbol_positive_fraction;validation_extension_gate_pass", "severity": "hard"},
            {"gate_id": "P195_PASSING_CANDIDATE_RECORDED", "gate_pass": int(passing_candidates >= 0), "evidence": f"passing_candidates={passing_candidates}", "severity": "hard"},
            {"gate_id": "P195_NO_TEST_REPLAY_OR_PROMOTION", "gate_pass": int((decisions.empty or (decisions["test_replay_allowed_next"].astype(int).eq(0).all() and decisions["promotion_allowed"].astype(int).eq(0).all()))), "evidence": "test_replay_allowed_next=0; promotion_allowed=0", "severity": "hard"},
        ]
    )


def build_acceptance(candidates: pd.DataFrame, selected: pd.DataFrame, decisions: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates.loc[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(int).sum()) if not hard.empty else 0
    passing = decisions.loc[decisions["validation_extension_gate_pass"].astype(int).eq(1)] if not decisions.empty else pd.DataFrame()
    best = decisions.iloc[0] if not decisions.empty else {}
    next_action = "precommit_new_candidate_contract_no_test" if not passing.empty else "redesign_or_expand_feature_family_no_test"
    return pd.DataFrame(
        [
            ("phase195_candidate_grid_rows", int(len(candidates)), "Redesigned candidate grid rows"),
            ("phase195_train_selected_candidate_rows", int(len(selected)), "Train-selected candidate rows"),
            ("phase195_candidate_decision_rows", int(len(decisions)), "Candidate decision rows"),
            ("phase195_passing_extension_gate_candidates", int(len(passing)), "Candidates passing date and symbol breadth extension gates"),
            ("phase195_best_candidate_id", best.get("candidate_id", ""), "Top redesign candidate by extension screen"),
            ("phase195_best_min_extension_net_bps", best.get("min_extension_net_bps", ""), "Best candidate minimum extension net bps"),
            ("phase195_best_date_positive_fraction", best.get("date_positive_fraction", ""), "Best candidate date-positive fraction"),
            ("phase195_best_symbol_positive_fraction", best.get("symbol_positive_fraction", ""), "Best candidate symbol-positive fraction"),
            ("phase195_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase195_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase195_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase195_redesign_search_complete", int(len(hard) > 0 and hard_pass == len(hard)), "1 means Phase195 completed"),
            ("phase195_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase195_promotion_allowed", 0, "No promotion opened"),
            ("phase195_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase195_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase195_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase195 Receive-flow Redesign Candidate Search",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase195 searches redesigned receive-flow candidates after Phase194 closed the prior sparse candidate.",
        "Selection is train-only. Validation and unassigned extension dates are evaluation-only. The untouched test split remains excluded.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase195_receive_flow_redesign_candidate_search_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase195(phase176_dir: Path, phase180_dir: Path, phase181_dir: Path, phase194_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase194 = read_csv(phase194_dir / "phase194_sparse_candidate_fragility_acceptance_summary.csv")
    feature_inventory = read_csv(phase176_dir / "phase176_feature_partition_inventory.csv")
    label_inventory = read_csv(phase181_dir / "phase181_label_partition_inventory.csv")
    latency_profiles = read_csv(phase180_dir / "phase180_latency_slippage_profile_catalog.csv")
    profiles = latency_profiles.loc[latency_profiles["profile_id"].astype(str).isin(ALLOWED_PROFILES)].copy()
    frame, partition_use = build_model_frame(feature_inventory, label_inventory)
    frame = add_derived_fields(frame)
    partition_use = build_partition_use(partition_use)
    candidates = candidate_grid()
    train_summary, selected, evaluation, by_date, by_symbol = run_search(frame, candidates, profiles)
    decisions = build_candidate_decision(selected, evaluation, by_date, by_symbol)
    gates = build_gates(phase194, partition_use, selected, decisions)
    acceptance = build_acceptance(candidates, selected, decisions, gates)

    candidates.to_csv(output_dir / "phase195_redesign_candidate_grid.csv", index=False)
    partition_use.to_csv(output_dir / "phase195_partition_use_audit.csv", index=False)
    train_summary.to_csv(output_dir / "phase195_train_candidate_summary.csv", index=False)
    selected.to_csv(output_dir / "phase195_train_selected_candidates.csv", index=False)
    evaluation.to_csv(output_dir / "phase195_validation_extension_summary.csv", index=False)
    by_date.to_csv(output_dir / "phase195_validation_extension_by_date.csv", index=False)
    by_symbol.to_csv(output_dir / "phase195_validation_extension_by_symbol.csv", index=False)
    decisions.to_csv(output_dir / "phase195_redesign_candidate_decision.csv", index=False)
    gates.to_csv(output_dir / "phase195_receive_flow_redesign_candidate_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase195_receive_flow_redesign_candidate_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Top Candidate Decisions": decisions.head(24),
            "Train-selected Candidates": selected,
            "Validation Extension Summary": evaluation.head(96),
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase195_receive_flow_redesign_candidate_search_no_test",
        **reproducibility_fields(
            artifact_id="phase195_receive_flow_redesign_candidate_search",
            generated_utc=generated,
            inputs={
                "phase176_feature_inventory": str(phase176_dir / "phase176_feature_partition_inventory.csv"),
                "phase181_label_inventory": str(phase181_dir / "phase181_label_partition_inventory.csv"),
                "phase180_latency_profiles": str(phase180_dir / "phase180_latency_slippage_profile_catalog.csv"),
                "phase194_acceptance": str(phase194_dir / "phase194_sparse_candidate_fragility_acceptance_summary.csv"),
            },
            parameters={
                "selection_split": "train",
                "evaluation_roles": ";".join(sorted(EVALUATION_ROLES)),
                "excluded_role": "test_untouched",
                "required_date_positive_fraction": 1.0,
                "required_symbol_positive_fraction": 0.25,
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "candidate_grid": str(output_dir / "phase195_redesign_candidate_grid.csv"),
                "partition_use": str(output_dir / "phase195_partition_use_audit.csv"),
                "train_summary": str(output_dir / "phase195_train_candidate_summary.csv"),
                "selected": str(output_dir / "phase195_train_selected_candidates.csv"),
                "evaluation": str(output_dir / "phase195_validation_extension_summary.csv"),
                "by_date": str(output_dir / "phase195_validation_extension_by_date.csv"),
                "by_symbol": str(output_dir / "phase195_validation_extension_by_symbol.csv"),
                "decisions": str(output_dir / "phase195_redesign_candidate_decision.csv"),
                "gate_evaluation": str(output_dir / "phase195_receive_flow_redesign_candidate_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase195_receive_flow_redesign_candidate_acceptance_summary.csv"),
                "report": str(output_dir / "phase195_receive_flow_redesign_candidate_search_report.md"),
            },
            random_seed=str(RANDOM_SEED),
            scenario_ids="phase195_receive_flow_redesign_candidate_search_no_test",
            cost_model_version="phase180_retail_default_and_stressed_profiles",
            latency_model_version="phase180_retail_default_and_stressed_profiles",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase195_receive_flow_redesign_candidate_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase176-dir", type=Path, default=DEFAULT_PHASE176_DIR)
    parser.add_argument("--phase180-dir", type=Path, default=DEFAULT_PHASE180_DIR)
    parser.add_argument("--phase181-dir", type=Path, default=DEFAULT_PHASE181_DIR)
    parser.add_argument("--phase194-dir", type=Path, default=DEFAULT_PHASE194_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase195(args.phase176_dir, args.phase180_dir, args.phase181_dir, args.phase194_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
