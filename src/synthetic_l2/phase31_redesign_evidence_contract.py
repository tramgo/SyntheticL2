from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


CONTRACT_REQUIREMENTS: dict[str, list[tuple[str, str, str, str]]] = {
    "S01": [
        ("new_event_signal_thesis", "signal_design", "A new event-level momentum/breakout thesis that forecasts beyond spread and Zerodha charge hurdle.", "No current S01 proxy survived Phase 25/26/27 realistic execution."),
        ("sub_second_mlofi_horizon", "feature_engineering", "Acceptance-grade sub-second and 1s/5s MLOFI lookbacks from received tick deltas, not 5-minute proxy features.", "Current proxy feature horizon is too coarse for breakout execution."),
        ("charged_retail_replay_pass", "execution_economics", "Retail and stressed profiles must be positive after spread, latency, slippage and Zerodha formula charges.", "Phase 25/26/27 realistic charged evidence has zero candidate rows."),
        ("multi_day_real_holdout", "real_data", "At least multi-day Class B real tick holdout with no reuse of the design day.", "One-day proxy evidence cannot prove stability."),
        ("negative_control_falsification", "robustness", "Breakout signal must beat shuffled-time and inverted-signal controls after costs.", "Needed to rule out artifact exploitation."),
    ],
    "S02": [
        ("new_ofi_signal_thesis", "signal_design", "A redesigned OFI direction model with a quantified fee/spread hurdle before replay.", "Current OFI proxy is negative after execution costs."),
        ("multi_level_ofi_event_features", "feature_engineering", "Acceptance-grade multi-level OFI features at event and short-horizon clocks.", "Static imbalance and coarse MLOFI are insufficient."),
        ("charged_retail_replay_pass", "execution_economics", "Retail and stressed profiles must be positive after spread, latency, slippage and Zerodha formula charges.", "Phase 25/26/27 realistic charged evidence has zero candidate rows."),
        ("multi_day_real_holdout", "real_data", "Multi-day real tick holdout across at least liquid bank and non-bank symbols.", "Single-day evidence cannot prove OFI stability."),
        ("negative_control_falsification", "robustness", "OFI direction must beat lagged, shuffled and sign-inverted controls after costs.", "Needed to rule out microstructure artifact fit."),
    ],
    "S03": [
        ("acceptance_grade_withdrawal_label", "label_engineering", "Explicit depth-withdrawal and replenishment labels from multi-day received ticks.", "Phase 28 labels are weak market-by-price proxies."),
        ("sweep_and_vacuum_event_label", "label_engineering", "Liquidity-vacuum/sweep labels with common-shock and crossed-book filters.", "Current labels cannot prove true vacuum events."),
        ("timestamp_skew_control", "data_quality", "Timestamp skew and simultaneous market-shock controls before causal replay.", "Needed before treating S03 event labels as causal."),
        ("broker_fill_cost_reconciliation", "broker_evidence", "Broker/exchange fill and cost reconciliation for marketable entries.", "Current costs are formula/model evidence, not broker fills."),
        ("charged_retail_replay_pass", "execution_economics", "Phase 29-style replay must become positive in retail and stressed profiles.", "Current S03 proxy replay is negative after costs."),
    ],
    "S04": [
        ("aggressive_trade_flow_label", "label_engineering", "Acceptance-grade signed aggressive trade imbalance labels.", "Current trade-side is weakly inferred from market-by-price updates."),
        ("depth_confirmation_label", "label_engineering", "Depth-confirmation/exhaustion labels that distinguish true flow from quote churn.", "Current labels cannot verify exhaustion."),
        ("common_shock_control", "robustness", "Common-shock and market-wide move controls before promotion replay.", "Needed to avoid labeling broad moves as strategy edge."),
        ("broker_fill_cost_reconciliation", "broker_evidence", "Broker/exchange fill and cost reconciliation for marketable entries.", "Current costs are formula/model evidence, not broker fills."),
        ("charged_retail_replay_pass", "execution_economics", "Phase 29-style replay must become positive in retail and stressed profiles.", "Current S04 proxy replay is negative after costs."),
    ],
    "S05": [
        ("new_microprice_trigger", "signal_design", "A microprice trigger that explicitly requires forecast edge greater than spread plus Zerodha charge hurdle.", "Standalone microprice proxy did not survive realistic execution."),
        ("event_level_microprice_markouts", "feature_engineering", "Event-level markout curves for 1/2/3/5 event horizons and short clock horizons.", "Current edge scan did not clear cost hurdle."),
        ("zero_latency_edge_to_retail_bridge", "execution_economics", "Demonstrate that the tiny Phase 26 zero-latency controls survive realistic latency/slippage.", "Zero-latency evidence alone is not tradable."),
        ("multi_day_real_holdout", "real_data", "Multi-day real tick validation across symbols with different spread regimes.", "Needed before retesting as a filter or entry signal."),
    ],
    "S06": [
        ("acceptance_grade_absorption_label", "label_engineering", "Absorption/replenishment labels with signed flow and visible-depth recovery.", "Phase 28 absorption labels are proxy-only."),
        ("flow_reversal_label", "label_engineering", "Flow-reversal labels separating replenishment from stale-book updates.", "Current labels cannot prove participant absorption."),
        ("broker_fill_cost_reconciliation", "broker_evidence", "Broker/exchange fill and cost reconciliation for reversal entries.", "Current replay uses model fills/costs."),
        ("charged_retail_replay_pass", "execution_economics", "Phase 29-style replay must become positive in retail and stressed profiles.", "Current S06 proxy replay is negative after costs."),
        ("multi_day_real_holdout", "real_data", "Multi-day validation across high- and low-liquidity names.", "Needed to test whether absorption generalizes."),
    ],
    "S07": [
        ("new_mean_reversion_trigger", "signal_design", "A mean-reversion trigger that avoids catching broad market moves and clears the fee/spread hurdle.", "Current S07 realistic variants all failed after costs."),
        ("replenishment_and_imbalance_features", "feature_engineering", "Event-level replenishment, imbalance persistence and spread-regime features.", "Current imbalance proxy is too weak."),
        ("zero_latency_edge_to_retail_bridge", "execution_economics", "Demonstrate that Phase 26 zero-latency positives survive realistic latency/slippage/costs.", "Frictionless edge is not tradable."),
        ("negative_control_falsification", "robustness", "Must beat inverted, lagged and shuffled imbalance controls after costs.", "Needed before further compute expansion."),
        ("multi_day_real_holdout", "real_data", "Multi-day real tick validation across spread/liquidity regimes.", "Current evidence is one-day/proxy-limited."),
    ],
    "S08": [
        ("lead_lag_causal_label", "label_engineering", "Causal lead/lag labels with timestamp-skew, simultaneous-shock and self-impact controls.", "Phase 28 lead-lag labels are weak 5s bucket proxies."),
        ("sector_and_index_mapping", "feature_engineering", "Explicit sector/index/leader mapping for cross-symbol OFI tests.", "Current proxy uses broad ex-self market flow."),
        ("out_of_sample_lead_lag_stability", "robustness", "Lead-lag sign and magnitude must be stable out-of-sample and across symbol groups.", "Single-day bucket correlation is not enough."),
        ("charged_retail_replay_pass", "execution_economics", "Phase 29-style replay must become positive in retail and stressed profiles.", "Current S08 proxy replay is negative after costs."),
        ("multi_day_real_holdout", "real_data", "Multi-day real tick validation with clock-skew audit.", "Needed before any lead-lag promotion."),
    ],
    "S09": [
        ("queue_imbalance_hurdle_trigger", "signal_design", "A queue-imbalance trigger that requires expected markout above spread, slippage and Zerodha charges.", "Current queue-imbalance proxy is a benchmark and failed realistic costs."),
        ("event_level_queue_markouts", "feature_engineering", "Event-level L1/L5 queue markouts and spread-state conditioning.", "Accuracy alone is insufficient for scalping."),
        ("zero_latency_edge_to_retail_bridge", "execution_economics", "Demonstrate that Phase 26 zero-latency positives survive realistic latency/slippage/costs.", "Frictionless edge is not tradable."),
        ("negative_control_falsification", "robustness", "Must beat random-side, inverted-side and stale-book controls after costs.", "Needed before queue-imbalance is more than a benchmark."),
        ("multi_day_real_holdout", "real_data", "Multi-day real tick validation across queue/spread regimes.", "One-day/proxy evidence is insufficient."),
    ],
}


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def build_contract(decisions: pd.DataFrame, redesign: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    alpha_decisions = decisions[decisions["current_decision"].astype(str).str.startswith("reject_")].copy()
    rows: list[dict] = []
    for _, decision in alpha_decisions.sort_values("strategy_id").iterrows():
        strategy_id = str(decision["strategy_id"])
        priority_rows = redesign[redesign["strategy_id"].eq(strategy_id)]
        priority = str(priority_rows["redesign_priority"].iloc[0]) if len(priority_rows) else "unknown"
        for idx, (requirement_id, evidence_domain, required_artifact, blocker) in enumerate(CONTRACT_REQUIREMENTS[strategy_id], start=1):
            rows.append(
                {
                    "strategy_id": strategy_id,
                    "strategy_name": decision["strategy_name"],
                    "redesign_priority": priority,
                    "contract_requirement_id": f"{strategy_id}_{idx:02d}_{requirement_id}",
                    "evidence_domain": evidence_domain,
                    "required_artifact_or_test": required_artifact,
                    "current_evidence_status": "missing_or_proxy_only",
                    "acceptance_requirement_met": False,
                    "replay_expansion_allowed": False,
                    "blocking_reason": blocker,
                    "source_phase30_decision": decision["current_decision"],
                }
            )
    contract = pd.DataFrame(rows)
    spec = (
        contract.groupby(["strategy_id", "strategy_name", "redesign_priority"], sort=True)
        .agg(
            contract_requirements=("contract_requirement_id", "count"),
            evidence_domains=("evidence_domain", lambda values: ";".join(sorted(set(map(str, values))))),
            open_requirements=("acceptance_requirement_met", lambda values: int((~values.astype(bool)).sum())),
            replay_expansion_allowed=("replay_expansion_allowed", "any"),
        )
        .reset_index()
    )
    spec["redesign_contract_status"] = "blocked_no_replay_until_contract_evidence"
    gate = spec[["strategy_id", "strategy_name", "redesign_priority", "contract_requirements", "open_requirements", "replay_expansion_allowed", "redesign_contract_status"]].copy()
    gate["next_action"] = gate["strategy_id"].map(_next_action)
    return spec, contract, gate


def _next_action(strategy_id: str) -> str:
    if strategy_id in {"S03", "S04", "S06", "S08"}:
        return "Build acceptance-grade event labels and multi-day/broker evidence before another replay expansion."
    if strategy_id in {"S05", "S07", "S09"}:
        return "Bridge the zero-latency diagnostic edge into charged retail/stressed execution before replay expansion."
    return "Write a materially new event-level signal thesis with explicit fee/spread hurdle before replay expansion."


def build_overall_summary(spec: pd.DataFrame, contract: pd.DataFrame, gate: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"metric": "phase31_strategy_redesign_specs", "value": int(len(spec)), "description": "Alpha strategy families with redesign evidence specs"},
            {"metric": "phase31_contract_requirement_rows", "value": int(len(contract)), "description": "Requirement rows that must be met before replay expansion"},
            {"metric": "phase31_open_contract_requirements", "value": int((~contract["acceptance_requirement_met"].astype(bool)).sum()), "description": "Currently open requirement rows"},
            {"metric": "phase31_replay_allowed_rows", "value": int(gate["replay_expansion_allowed"].astype(bool).sum()), "description": "Strategy rows allowed back into replay expansion now"},
            {"metric": "phase31_replay_blocked_rows", "value": int((~gate["replay_expansion_allowed"].astype(bool)).sum()), "description": "Strategy rows blocked from more replay compute"},
            {"metric": "phase31_acceptance_ready_rows", "value": 0, "description": "Rows with all redesign evidence satisfied"},
            {"metric": "phase31_label_engineering_requirements", "value": int(contract["evidence_domain"].eq("label_engineering").sum()), "description": "Acceptance-grade label requirements"},
            {"metric": "phase31_broker_evidence_requirements", "value": int(contract["evidence_domain"].eq("broker_evidence").sum()), "description": "Broker/fill/cost reconciliation requirements"},
            {"metric": "phase31_execution_economics_requirements", "value": int(contract["evidence_domain"].eq("execution_economics").sum()), "description": "Cost-survival execution requirements"},
        ]
    )


def write_report(output_dir: Path, overall: pd.DataFrame, spec: pd.DataFrame, contract: pd.DataFrame, gate: pd.DataFrame) -> None:
    lines = [
        "# Phase 31 Redesign Evidence Contract",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This milestone converts the Phase 30 reject/redesign verdict into a no-replay-until evidence contract.",
        "Every alpha strategy remains blocked from additional replay expansion until its missing redesign evidence is produced.",
        "",
        "## Overall Summary",
        "",
        _markdown_table(overall),
        "",
        "## Strategy Redesign Specs",
        "",
        _markdown_table(spec),
        "",
        "## Replay Gate",
        "",
        _markdown_table(gate),
        "",
        "## Evidence Contract Ledger",
        "",
        _markdown_table(contract),
        "",
    ]
    (output_dir / "phase31_redesign_evidence_contract_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase31(phase30_decision_ledger: Path, phase30_redesign_queue: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    decisions = _read_csv(phase30_decision_ledger)
    redesign = _read_csv(phase30_redesign_queue)
    spec, contract, gate = build_contract(decisions, redesign)
    overall = build_overall_summary(spec, contract, gate)

    spec.to_csv(output_dir / "strategy_redesign_spec_catalog.csv", index=False)
    contract.to_csv(output_dir / "redesign_evidence_contract_ledger.csv", index=False)
    gate.to_csv(output_dir / "replay_expansion_gate.csv", index=False)
    overall.to_csv(output_dir / "redesign_evidence_contract_overall_summary.csv", index=False)
    write_report(output_dir, overall, spec, contract, gate)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "strategy_redesign_specs": int(len(spec)),
        "contract_requirement_rows": int(len(contract)),
        "replay_allowed_rows": int(gate["replay_expansion_allowed"].astype(bool).sum()),
        "scope": "phase31_redesign_evidence_contract_no_replay_until_gate",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase31",
            generated_utc=generated_utc,
            inputs={
                "phase30_decision_ledger": str(phase30_decision_ledger),
                "phase30_redesign_queue": str(phase30_redesign_queue),
            },
            parameters={
                "contract_policy": "all_phase30_rejected_alpha_families_blocked_from_replay_until_contract_requirements_are_met",
                "contract_requirements": CONTRACT_REQUIREMENTS,
            },
            outputs={
                "strategy_redesign_spec_catalog": str(output_dir / "strategy_redesign_spec_catalog.csv"),
                "redesign_evidence_contract_ledger": str(output_dir / "redesign_evidence_contract_ledger.csv"),
                "replay_expansion_gate": str(output_dir / "replay_expansion_gate.csv"),
                "overall_summary": str(output_dir / "redesign_evidence_contract_overall_summary.csv"),
                "report": str(output_dir / "phase31_redesign_evidence_contract_report.md"),
                "manifest": str(output_dir / "phase31_redesign_evidence_contract_manifest.json"),
            },
            random_seed="none_deterministic_contract_rules",
            scenario_ids="phase30_rejected_alpha_strategy_families",
            cost_model_version="zerodha_equity_intraday_nse_order_formula_v2_2026_07_14",
            latency_model_version="phase12_execution_profiles_event_latency_counts",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase31_redesign_evidence_contract_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 31 redesign evidence contracts from Phase 30 decisions.")
    parser.add_argument("--phase30-decision-ledger", type=Path, default=Path("outputs/phase30/strategy_family_decision_ledger.csv"))
    parser.add_argument("--phase30-redesign-queue", type=Path, default=Path("outputs/phase30/strategy_redesign_queue.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase31"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase31(args.phase30_decision_ledger, args.phase30_redesign_queue, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
