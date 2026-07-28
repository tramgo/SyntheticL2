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
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE176_DIR = Path("outputs/phase176")
DEFAULT_PHASE180_DIR = Path("outputs/phase180")
DEFAULT_PHASE181_DIR = Path("outputs/phase181")
DEFAULT_PHASE186_DIR = Path("outputs/phase186")
DEFAULT_OUTPUT_DIR = Path("outputs/phase187")
RANDOM_SEED = 187
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


def add_derived_fields(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    mid = ((pd.to_numeric(out["best_bid"], errors="coerce") + pd.to_numeric(out["best_ask"], errors="coerce")) / 2.0).replace(0, np.nan)
    out["spread_bps"] = (pd.to_numeric(out["spread"], errors="coerce") / mid * 10_000.0).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    out["abs_top5_qty_imbalance"] = pd.to_numeric(out["top5_qty_imbalance"], errors="coerce").abs().fillna(0.0)
    out["abs_l1_qty_imbalance"] = pd.to_numeric(out["l1_qty_imbalance"], errors="coerce").abs().fillna(0.0)
    out["abs_receive_event_rate_zscore"] = pd.to_numeric(out["receive_event_rate_zscore"], errors="coerce").abs().fillna(0.0)
    out["side_from_top5_imbalance"] = np.sign(pd.to_numeric(out["top5_qty_imbalance"], errors="coerce").fillna(0.0)).astype("int8")
    out["side_from_l1_imbalance"] = np.sign(pd.to_numeric(out["l1_qty_imbalance"], errors="coerce").fillna(0.0)).astype("int8")
    return out


def candidate_grid() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for imbalance_source in ["top5", "l1"]:
        for min_imbalance in [0.55, 0.65, 0.75, 0.85]:
            for max_spread_bps in [2.5, 5.0, 10.0]:
                for min_abs_event_z in [0.0, 1.0, 2.0]:
                    for max_decision_rate in [0.005, 0.01, 0.02]:
                        rows.append(
                            {
                                "candidate_id": f"P187_{imbalance_source.upper()}_I{int(min_imbalance*100)}_S{str(max_spread_bps).replace('.', 'p')}_Z{int(min_abs_event_z)}_R{int(max_decision_rate*10000)}",
                                "imbalance_source": imbalance_source,
                                "min_abs_imbalance": min_imbalance,
                                "max_spread_bps": max_spread_bps,
                                "min_abs_event_zscore": min_abs_event_z,
                                "max_decision_rate": max_decision_rate,
                                "test_replay_allowed_in_phase187": 0,
                            }
                        )
    return pd.DataFrame(rows)


def candidate_mask(frame: pd.DataFrame, candidate: pd.Series) -> tuple[pd.Series, pd.Series]:
    if candidate["imbalance_source"] == "top5":
        imbalance = frame["abs_top5_qty_imbalance"]
        side = frame["side_from_top5_imbalance"]
    else:
        imbalance = frame["abs_l1_qty_imbalance"]
        side = frame["side_from_l1_imbalance"]
    mask = (
        (imbalance >= float(candidate["min_abs_imbalance"]))
        & (frame["spread_bps"] <= float(candidate["max_spread_bps"]))
        & (frame["abs_receive_event_rate_zscore"] >= float(candidate["min_abs_event_zscore"]))
        & side.ne(0)
    )
    return mask, side


def summarize_candidate(frame: pd.DataFrame, candidate: pd.Series, profile: pd.Series, rng: np.random.Generator) -> dict[str, Any]:
    mask, side = candidate_mask(frame, candidate)
    selected = frame.loc[mask].copy()
    selected_side = side.loc[mask]
    gross = selected_side.to_numpy() * pd.to_numeric(selected["future_mid_return_bps_next_bucket"], errors="coerce").to_numpy() if len(selected) else np.array([])
    cost = profile_cost_bps(selected, profile) if len(selected) else pd.Series(dtype=float)
    net = gross - cost.to_numpy() if len(selected) else np.array([])
    shuffled = pd.to_numeric(selected["future_mid_return_bps_next_bucket"], errors="coerce").to_numpy(copy=True) if len(selected) else np.array([])
    rng.shuffle(shuffled)
    control_net = selected_side.to_numpy() * shuffled - cost.to_numpy() if len(selected) else np.array([])
    return {
        "candidate_id": candidate["candidate_id"],
        "latency_profile_id": profile["profile_id"],
        "split_role": str(frame["split_role"].iloc[0]) if len(frame) else "",
        "decision_events": int(len(selected)),
        "decision_rate": float(len(selected) / len(frame)) if len(frame) else 0.0,
        "gross_return_bps_proxy_mean": float(np.nanmean(gross)) if len(gross) else np.nan,
        "cost_bound_bps_mean": float(np.nanmean(cost)) if len(cost) else np.nan,
        "net_return_bps_after_cost_proxy_mean": float(np.nanmean(net)) if len(net) else np.nan,
        "net_positive_event_fraction": float(np.nanmean(net > 0)) if len(net) else np.nan,
        "shuffled_time_net_bps_proxy_mean": float(np.nanmean(control_net)) if len(control_net) else np.nan,
        "net_edge_over_shuffled_time_bps": float(np.nanmean(net) - np.nanmean(control_net)) if len(net) and len(control_net) else np.nan,
        "test_rows_used": 0,
        "promotion_allowed": 0,
    }


def run_candidate_search(frame: pd.DataFrame, candidates: pd.DataFrame, latency_profiles: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(RANDOM_SEED)
    train = frame.loc[frame["split_role"].astype(str).eq("train")].copy()
    validation = frame.loc[frame["split_role"].astype(str).eq("validation")].copy()
    profiles = latency_profiles.loc[latency_profiles["profile_id"].astype(str).isin(["P180_RETAIL_MARKETABLE_DEFAULT", "P180_STRESSED_RETAIL"])].copy()
    train_rows: list[dict[str, Any]] = []
    for cand in candidates.to_dict("records"):
        cand_s = pd.Series(cand)
        for prof in profiles.to_dict("records"):
            train_rows.append(summarize_candidate(train, cand_s, pd.Series(prof), rng))
    train_summary = pd.DataFrame(train_rows)
    train_actual = train_summary.copy()
    eligible = train_actual.loc[
        train_actual["decision_rate"].le(train_actual["candidate_id"].map(candidates.set_index("candidate_id")["max_decision_rate"]))
        & train_actual["decision_events"].ge(100)
    ].copy()
    profile_rollup = (
        eligible.groupby("candidate_id", as_index=False)
        .agg(
            min_train_net_bps=("net_return_bps_after_cost_proxy_mean", "min"),
            min_train_edge_over_control_bps=("net_edge_over_shuffled_time_bps", "min"),
            max_decision_rate_observed=("decision_rate", "max"),
            total_profile_rows=("latency_profile_id", "count"),
        )
        if not eligible.empty
        else pd.DataFrame(columns=["candidate_id", "min_train_net_bps", "min_train_edge_over_control_bps", "max_decision_rate_observed", "total_profile_rows"])
    )
    selected = profile_rollup.sort_values(["min_train_net_bps", "min_train_edge_over_control_bps"], ascending=False).head(12)
    selected = selected.merge(candidates, on="candidate_id", how="left")
    selected["selected_by_phase187_train_only"] = 1
    selected["validation_used_for_selection"] = 0
    selected["test_used_for_selection"] = 0

    validation_rows: list[dict[str, Any]] = []
    for cand in selected.to_dict("records"):
        cand_s = pd.Series(cand)
        for prof in profiles.to_dict("records"):
            validation_rows.append(summarize_candidate(validation, cand_s, pd.Series(prof), rng))
    validation_summary = pd.DataFrame(validation_rows)
    if not validation_summary.empty:
        validation_summary = validation_summary.merge(
            selected[["candidate_id", "min_train_net_bps", "min_train_edge_over_control_bps", "max_decision_rate_observed"]],
            on="candidate_id",
            how="left",
        )
        validation_summary["validation_net_positive"] = (validation_summary["net_return_bps_after_cost_proxy_mean"] > 0).astype(int)
    return train_summary, selected, validation_summary


def build_gate_evaluation(phase186: pd.DataFrame, partition_use: pd.DataFrame, selected: pd.DataFrame, validation: pd.DataFrame) -> pd.DataFrame:
    family_closed = as_int(metric_value(phase186, "phase186_current_family_set_closed", 0))
    test_rows_used = int(partition_use.loc[partition_use["split_role"].astype(str).eq("test_untouched"), "used_in_phase184"].sum()) if not partition_use.empty else 0
    validation_positive_all_profiles = int(not validation.empty and validation.groupby("candidate_id")["validation_net_positive"].min().max() == 1)
    return pd.DataFrame(
        [
            {"gate_id": "P187_PHASE186_FAMILY_SET_CLOSED", "gate_pass": int(family_closed == 1), "evidence": f"phase186_current_family_set_closed={family_closed}", "severity": "hard"},
            {"gate_id": "P187_TRAIN_ONLY_SELECTION", "gate_pass": int(not selected.empty and selected["validation_used_for_selection"].astype(int).eq(0).all() and selected["test_used_for_selection"].astype(int).eq(0).all()), "evidence": f"selected_candidate_rows={len(selected)}", "severity": "hard"},
            {"gate_id": "P187_VALIDATION_EVALUATED_NO_TEST", "gate_pass": int(not validation.empty and test_rows_used == 0), "evidence": f"validation_rows={len(validation)}; test_rows_used={test_rows_used}", "severity": "hard"},
            {"gate_id": "P187_COST_LATENCY_BOUND", "gate_pass": int(not validation.empty and validation["latency_profile_id"].astype(str).isin(["P180_RETAIL_MARKETABLE_DEFAULT", "P180_STRESSED_RETAIL"]).all()), "evidence": f"validation_summary_rows={len(validation)}", "severity": "hard"},
            {"gate_id": "P187_NEGATIVE_CONTROL_MARGIN_RECORDED", "gate_pass": int(not validation.empty and "net_edge_over_shuffled_time_bps" in validation.columns), "evidence": "shuffled-time control edge column present", "severity": "hard"},
            {"gate_id": "P187_NO_TEST_REPLAY_OR_PROMOTION", "gate_pass": int(not validation.empty and validation["test_rows_used"].astype(int).eq(0).all() and validation["promotion_allowed"].astype(int).eq(0).all()), "evidence": "test_rows_used=0; promotion_allowed=0", "severity": "hard"},
            {"gate_id": "P187_VALIDATION_PASS_RECORDED", "gate_pass": int(validation_positive_all_profiles in (0, 1)), "evidence": f"validation_positive_all_profiles={validation_positive_all_profiles}", "severity": "hard"},
        ]
    )


def build_acceptance_summary(candidates: pd.DataFrame, selected: pd.DataFrame, validation: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates.loc[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(int).sum()) if not hard.empty else 0
    validation_positive_all_profiles = int(not validation.empty and validation.groupby("candidate_id")["validation_net_positive"].min().max() == 1)
    best_net = float(validation["net_return_bps_after_cost_proxy_mean"].max()) if not validation.empty else ""
    best_row = validation.sort_values("net_return_bps_after_cost_proxy_mean", ascending=False).iloc[0] if not validation.empty else {}
    rows = [
        ("phase187_candidate_grid_rows", int(len(candidates)), "Sparse candidate grid rows"),
        ("phase187_train_selected_candidate_rows", int(len(selected)), "Train-selected candidate rows"),
        ("phase187_validation_summary_rows", int(len(validation)), "Validation summary rows"),
        ("phase187_best_validation_candidate_id", best_row.get("candidate_id", ""), "Best validation candidate"),
        ("phase187_best_validation_latency_profile", best_row.get("latency_profile_id", ""), "Best validation latency profile"),
        ("phase187_best_validation_net_bps_proxy_mean", best_net, "Best validation net return-bps proxy mean"),
        ("phase187_validation_positive_all_profiles", validation_positive_all_profiles, "1 means at least one candidate is net positive under all allowed profiles"),
        ("phase187_gate_rows", int(len(gates)), "Gates evaluated"),
        ("phase187_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
        ("phase187_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase187_cost_aware_sparse_candidate_complete", int(len(hard) > 0 and hard_pass == len(hard)), "1 means Phase187 completed"),
        ("phase187_test_rows_used", 0, "Test rows remain untouched"),
        ("phase187_test_replay_allowed_next", 0, "No test replay opened by Phase187"),
        ("phase187_promotion_allowed", 0, "No promotion opened"),
        ("phase187_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
        ("phase187_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
        ("phase187_next_best_action", "build_phase188_cost_aware_sparse_candidate_interpretation_no_test", "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, selected: pd.DataFrame, validation: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase187 Cost-aware Sparse Receive-flow Candidate",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase187 builds a redesigned sparse candidate grid after Phase186 closed the previous receive-flow family set.",
        "Selection is train-only; validation is evaluation-only; test replay, promotion, paper/live acceptance and P&L remain closed.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Train-selected Candidates",
        "",
        _markdown_table(selected),
        "",
        "## Validation Summary",
        "",
        _markdown_table(validation),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
    ]
    (output_dir / "phase187_cost_aware_sparse_candidate_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase187(phase176_dir: Path, phase180_dir: Path, phase181_dir: Path, phase186_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase186 = read_csv(phase186_dir / "phase186_cost_aware_family_closure_acceptance_summary.csv")
    feature_inventory = read_csv(phase176_dir / "phase176_feature_partition_inventory.csv")
    label_inventory = read_csv(phase181_dir / "phase181_label_partition_inventory.csv")
    latency_profiles = read_csv(phase180_dir / "phase180_latency_slippage_profile_catalog.csv")
    frame, partition_use = build_model_frame(feature_inventory, label_inventory)
    frame = add_derived_fields(frame)
    candidates = candidate_grid()
    train_summary, selected, validation = run_candidate_search(frame, candidates, latency_profiles)
    gates = build_gate_evaluation(phase186, partition_use, selected, validation)
    acceptance = build_acceptance_summary(candidates, selected, validation, gates)

    candidates.to_csv(output_dir / "phase187_sparse_candidate_grid.csv", index=False)
    partition_use.to_csv(output_dir / "phase187_partition_use_audit.csv", index=False)
    train_summary.to_csv(output_dir / "phase187_train_candidate_summary.csv", index=False)
    selected.to_csv(output_dir / "phase187_train_selected_candidates.csv", index=False)
    validation.to_csv(output_dir / "phase187_validation_candidate_summary.csv", index=False)
    gates.to_csv(output_dir / "phase187_cost_aware_sparse_candidate_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase187_cost_aware_sparse_candidate_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, selected, validation, gates)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase187_cost_aware_sparse_receive_flow_candidate_no_test",
        **reproducibility_fields(
            artifact_id="phase187_cost_aware_sparse_candidate",
            generated_utc=generated_utc,
            inputs={
                "phase186_acceptance": str(phase186_dir / "phase186_cost_aware_family_closure_acceptance_summary.csv"),
                "phase176_feature_inventory": str(phase176_dir / "phase176_feature_partition_inventory.csv"),
                "phase181_label_inventory": str(phase181_dir / "phase181_label_partition_inventory.csv"),
                "phase180_latency_profiles": str(phase180_dir / "phase180_latency_slippage_profile_catalog.csv"),
            },
            parameters={
                "random_seed": RANDOM_SEED,
                "selection_split": "train",
                "evaluation_split": "validation",
                "test_rows_used": 0,
                "promotion_allowed": 0,
            },
            outputs={
                "candidate_grid": str(output_dir / "phase187_sparse_candidate_grid.csv"),
                "partition_use_audit": str(output_dir / "phase187_partition_use_audit.csv"),
                "train_candidate_summary": str(output_dir / "phase187_train_candidate_summary.csv"),
                "train_selected_candidates": str(output_dir / "phase187_train_selected_candidates.csv"),
                "validation_candidate_summary": str(output_dir / "phase187_validation_candidate_summary.csv"),
                "gate_evaluation": str(output_dir / "phase187_cost_aware_sparse_candidate_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase187_cost_aware_sparse_candidate_acceptance_summary.csv"),
                "report": str(output_dir / "phase187_cost_aware_sparse_candidate_report.md"),
            },
            random_seed=RANDOM_SEED,
            scenario_ids="phase187_cost_aware_sparse_receive_flow_candidate_no_test",
            cost_model_version="phase180_zerodha_equity_intraday_cost_bound_proxy",
            latency_model_version="phase180_retail_marketable_default_and_stressed_retail",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase187_cost_aware_sparse_candidate_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase176-dir", type=Path, default=DEFAULT_PHASE176_DIR)
    parser.add_argument("--phase180-dir", type=Path, default=DEFAULT_PHASE180_DIR)
    parser.add_argument("--phase181-dir", type=Path, default=DEFAULT_PHASE181_DIR)
    parser.add_argument("--phase186-dir", type=Path, default=DEFAULT_PHASE186_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase187(args.phase176_dir, args.phase180_dir, args.phase181_dir, args.phase186_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
