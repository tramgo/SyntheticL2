from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase67")


def metric_value(path: Path, metric: str, default: Any = None) -> Any:
    frame = pd.read_csv(path)
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    value = rows.iloc[0]
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def build_feature_design_queue() -> pd.DataFrame:
    rows = [
        {
            "priority": 1,
            "feature_family_id": "F67_replenishment_after_touch",
            "hypothesis": "After a best-bid/best-ask touch, rapid visible replenishment may identify liquidity support/resistance better than static imbalance.",
            "required_inputs": "L1-L5 quantity changes, touch inference, local sequence ordering, spread and mid-price path.",
            "first_experiment": "No-lookahead label discovery for post-touch depth replenishment and next-100-tick mid outcome.",
            "small_sample_budget": "32 shards x 250k rows",
            "scale_gate": "At least 2 disjoint symbols and 2 disjoint months positive after costs; adverse-selection rate <= 45%; cost-clearing rate >= 55%.",
            "reason_for_priority": "Phase66 showed static imbalance touches were adverse; replenishment tests whether dynamic book repair carries different information.",
        },
        {
            "priority": 2,
            "feature_family_id": "F67_spread_compression_expansion",
            "hypothesis": "Transitions from wide-to-tight or tight-to-wide spreads may be more informative than the spread level alone.",
            "required_inputs": "Spread bps, rolling spread rank, mid-price movement, L1-L5 depth state.",
            "first_experiment": "Event-bar label discovery for spread regime transitions with taker and passive variants separated.",
            "small_sample_budget": "32 shards x 250k rows",
            "scale_gate": "Positive no-lookahead validation under retail costs and stable sign across at least 50% of active symbols.",
            "reason_for_priority": "Marketable and passive static imbalance failed; spread transition features may target liquidity regime changes instead of directional imbalance.",
        },
        {
            "priority": 3,
            "feature_family_id": "F67_cross_symbol_lead_lag",
            "hypothesis": "Index/bank/IT ETF and large-cap quote moves may lead slower constituents enough to beat costs at lower frequency.",
            "required_inputs": "Synchronized event-time bars by symbol, sector/ETF groups, lagged returns, lagged OFI/MLOFI proxies.",
            "first_experiment": "DuckDB event-bar matrix build plus no-lookahead lead-lag label scan.",
            "small_sample_budget": "1 month all 32 symbols at event-bar frequency",
            "scale_gate": "Disjoint-month positive after-cost validation with turnover low enough that cost drag < 50% of gross edge.",
            "reason_for_priority": "Single-symbol tick-local features repeatedly failed; cross-symbol information is a genuinely different axis in the plan.",
        },
        {
            "priority": 4,
            "feature_family_id": "F67_shock_resilience_mean_reversion",
            "hypothesis": "Synthetic shock/reconnect/regime tags may identify overreaction pockets where lower turnover mean reversion survives costs.",
            "required_inputs": "Regime code, shock flags, feed profile, event bars, post-shock liquidity normalization.",
            "first_experiment": "Regime-conditioned lower-frequency labels for shock recovery windows.",
            "small_sample_budget": "All shock-tagged shards with capped rows",
            "scale_gate": "Positive after-cost P&L in at least two shock classes and negative-control non-shock comparison not driving the result.",
            "reason_for_priority": "The generator explicitly contains regimes and shocks; these should be used as falsifiable stress-test features, not ignored.",
        },
    ]
    return pd.DataFrame(rows)


def build_budget_gates() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "gate_id": "G67_01_small_before_large",
                "rule": "No feature family may request a full-year replay before passing a bounded small-sample discovery and disjoint validation.",
                "required_evidence": "Discovery artifact, disjoint validation artifact, acceptance summary and manifest.",
                "failure_action": "retire_or_redesign_feature_family",
            },
            {
                "gate_id": "G67_02_no_oracle_promotion",
                "rule": "Oracle, zero-latency, zero-cost or hindsight-positive rows cannot be promoted to deployable candidates.",
                "required_evidence": "Candidate catalog must mark deployable=false for oracle/control rows.",
                "failure_action": "keep_as_control_only",
            },
            {
                "gate_id": "G67_03_cost_drag_limit",
                "rule": "A candidate cannot scale if cost drag consumes more than 50% of gross edge on validation.",
                "required_evidence": "gross_pnl_proxy_inr, cost_pnl_drag_proxy_inr and net_pnl_inr reported on validation.",
                "failure_action": "reduce_turnover_or_retire",
            },
            {
                "gate_id": "G67_04_stability",
                "rule": "A candidate cannot scale if it is positive only in one symbol, one month, or one sparse interaction cell.",
                "required_evidence": "Symbol, month and bucket/stability rollups.",
                "failure_action": "falsification_probe_or_retire",
            },
            {
                "gate_id": "G67_05_passive_fill_honesty",
                "rule": "Passive results must be reported as assumption sensitivity until real fills, contract notes or true queue data are available.",
                "required_evidence": "Queue profile catalog and pessimistic/base/optimistic sensitivity outputs.",
                "failure_action": "do_not_claim_live_fill_profitability",
            },
        ]
    )


def build_acceptance_summary(base_dir: Path, feature_queue: pd.DataFrame, budget_gates: pd.DataFrame) -> pd.DataFrame:
    phase66 = base_dir / "outputs/phase66/passive_label_acceptance_summary.csv"
    phase66_survives = int(float(metric_value(phase66, "phase66_survives_label_gate", 0)))
    phase66_best_after_cost = float(metric_value(phase66, "phase66_best_mean_after_cost_bps_if_touched", 0.0))
    rows = [
        ("phase67_source_phase66_survives_label_gate", phase66_survives, "Phase66 passive imbalance label gate"),
        ("phase67_source_phase66_best_after_cost_bps", phase66_best_after_cost, "Best Phase66 after-cost touch label"),
        ("phase67_feature_families_queued", int(len(feature_queue)), "New feature families queued for bounded testing"),
        ("phase67_budget_gates_declared", int(len(budget_gates)), "Predeclared gates before large replay"),
        ("phase67_allow_full_year_replay_now", 0, "0 means no new full-year replay until a new family passes the declared gates"),
        ("phase67_next_priority_feature_family", str(feature_queue.iloc[0]["feature_family_id"]), "Highest-priority next feature family"),
        ("phase67_next_priority_experiment", str(feature_queue.iloc[0]["first_experiment"]), "Next bounded experiment"),
        ("phase67_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model to preserve in next experiments"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase67 Feature Design and Experiment-Budget Gate",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase67 responds to the failed Phase66 passive imbalance labels by returning to feature design under strict budget gates.",
        "The purpose is to prevent another expensive full-year replay until a genuinely new feature family passes small, disjoint, cost-aware tests.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase67_feature_design_budget_gate_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase67(base_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    feature_queue = build_feature_design_queue()
    budget_gates = build_budget_gates()
    acceptance = build_acceptance_summary(base_dir, feature_queue, budget_gates)

    feature_queue.to_csv(output_dir / "feature_design_queue.csv", index=False)
    budget_gates.to_csv(output_dir / "experiment_budget_gates.csv", index=False)
    acceptance.to_csv(output_dir / "feature_design_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Feature Design Queue": feature_queue,
            "Experiment Budget Gates": budget_gates,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase67_feature_design_budget_gate",
        "next_priority_feature_family": str(feature_queue.iloc[0]["feature_family_id"]),
        "allow_full_year_replay_now": 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase67",
            generated_utc=generated_utc,
            inputs={
                "phase64_next_research_queue": "outputs/phase64/next_research_queue.csv",
                "phase66_acceptance": "outputs/phase66/passive_label_acceptance_summary.csv",
            },
            parameters={
                "decision_rule": "after_phase66_failure_return_to_feature_design_and_require_predeclared_budget_gates",
                "next_family": str(feature_queue.iloc[0]["feature_family_id"]),
            },
            outputs={
                "feature_design_queue": str(output_dir / "feature_design_queue.csv"),
                "experiment_budget_gates": str(output_dir / "experiment_budget_gates.csv"),
                "acceptance_summary": str(output_dir / "feature_design_acceptance_summary.csv"),
                "report": str(output_dir / "phase67_feature_design_budget_gate_report.md"),
                "manifest": str(output_dir / "phase67_feature_design_budget_gate_manifest.json"),
            },
            random_seed="none_deterministic_research_gate",
            scenario_ids="phase67_feature_design_after_phase66_failure",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_research_gate",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase67_feature_design_budget_gate_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Declare the next feature-design queue and experiment-budget gates.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase67(args.base_dir, args.output_dir)


if __name__ == "__main__":
    main()
