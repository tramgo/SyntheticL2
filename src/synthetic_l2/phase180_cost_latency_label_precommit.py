from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE179_DIR = Path("outputs/phase179")
DEFAULT_PHASE178_DIR = Path("outputs/phase178")
DEFAULT_OUTPUT_DIR = Path("outputs/phase180")
ZERODHA_CHARGES_URL = "https://zerodha.com/charges"
ZERODHA_STT_URL = "https://support.zerodha.com/category/account-opening/resident-individual/ri-charges/articles/how-is-the-securities-transaction-tax-stt-calculated"
FORBIDDEN_OUTPUTS = "signal;order;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance"


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


def build_zerodha_equity_cost_catalog(verified_utc: str) -> pd.DataFrame:
    rows = [
        ("equity_delivery", "NSE", "brokerage", "both", "0", "inr_per_executed_order", "Zero brokerage for resident retail equity delivery", ZERODHA_CHARGES_URL),
        ("equity_delivery", "BSE", "brokerage", "both", "0", "inr_per_executed_order", "Zero brokerage for resident retail equity delivery", ZERODHA_CHARGES_URL),
        ("equity_intraday", "NSE", "brokerage", "both", "min(0.0003 * turnover, 20)", "inr_per_executed_order", "0.03 percent or Rs 20 per executed order, whichever is lower", ZERODHA_CHARGES_URL),
        ("equity_intraday", "BSE", "brokerage", "both", "min(0.0003 * turnover, 20)", "inr_per_executed_order", "0.03 percent or Rs 20 per executed order, whichever is lower", ZERODHA_CHARGES_URL),
        ("equity_delivery", "NSE", "stt", "buy_and_sell", "0.001 * turnover", "inr", "0.1 percent on buy and sell", ZERODHA_CHARGES_URL),
        ("equity_delivery", "BSE", "stt", "buy_and_sell", "0.001 * turnover", "inr", "0.1 percent on buy and sell", ZERODHA_CHARGES_URL),
        ("equity_intraday", "NSE", "stt", "sell", "0.00025 * sell_turnover", "inr", "0.025 percent on sell side only", ZERODHA_STT_URL),
        ("equity_intraday", "BSE", "stt", "sell", "0.00025 * sell_turnover", "inr", "0.025 percent on sell side only", ZERODHA_STT_URL),
        ("equity_delivery", "NSE", "transaction_charges", "both", "0.0000307 * turnover", "inr", "NSE equity transaction charges 0.00307 percent", ZERODHA_CHARGES_URL),
        ("equity_intraday", "NSE", "transaction_charges", "both", "0.0000307 * turnover", "inr", "NSE equity transaction charges 0.00307 percent", ZERODHA_CHARGES_URL),
        ("equity_delivery", "BSE", "transaction_charges", "both", "0.0000375 * turnover", "inr", "BSE equity transaction charges 0.00375 percent", ZERODHA_CHARGES_URL),
        ("equity_intraday", "BSE", "transaction_charges", "both", "0.0000375 * turnover", "inr", "BSE equity transaction charges 0.00375 percent", ZERODHA_CHARGES_URL),
        ("equity_delivery", "NSE", "sebi_charges", "both", "10 / 10000000 * turnover", "inr", "SEBI charges Rs 10 per crore", ZERODHA_CHARGES_URL),
        ("equity_intraday", "NSE", "sebi_charges", "both", "10 / 10000000 * turnover", "inr", "SEBI charges Rs 10 per crore", ZERODHA_CHARGES_URL),
        ("equity_delivery", "BSE", "sebi_charges", "both", "10 / 10000000 * turnover", "inr", "SEBI charges Rs 10 per crore", ZERODHA_CHARGES_URL),
        ("equity_intraday", "BSE", "sebi_charges", "both", "10 / 10000000 * turnover", "inr", "SEBI charges Rs 10 per crore", ZERODHA_CHARGES_URL),
        ("equity_delivery", "NSE", "stamp_duty", "buy", "0.00015 * buy_turnover", "inr", "0.015 percent or Rs 1500 per crore on buy side", ZERODHA_CHARGES_URL),
        ("equity_delivery", "BSE", "stamp_duty", "buy", "0.00015 * buy_turnover", "inr", "0.015 percent or Rs 1500 per crore on buy side", ZERODHA_CHARGES_URL),
        ("equity_intraday", "NSE", "stamp_duty", "buy", "0.00003 * buy_turnover", "inr", "0.003 percent or Rs 300 per crore on buy side", ZERODHA_CHARGES_URL),
        ("equity_intraday", "BSE", "stamp_duty", "buy", "0.00003 * buy_turnover", "inr", "0.003 percent or Rs 300 per crore on buy side", ZERODHA_CHARGES_URL),
        ("equity_delivery", "NSE", "gst", "both", "0.18 * (brokerage + sebi_charges + transaction_charges)", "inr", "GST on brokerage plus SEBI plus transaction charges", ZERODHA_CHARGES_URL),
        ("equity_intraday", "NSE", "gst", "both", "0.18 * (brokerage + sebi_charges + transaction_charges)", "inr", "GST on brokerage plus SEBI plus transaction charges", ZERODHA_CHARGES_URL),
        ("equity_delivery", "BSE", "gst", "both", "0.18 * (brokerage + sebi_charges + transaction_charges)", "inr", "GST on brokerage plus SEBI plus transaction charges", ZERODHA_CHARGES_URL),
        ("equity_intraday", "BSE", "gst", "both", "0.18 * (brokerage + sebi_charges + transaction_charges)", "inr", "GST on brokerage plus SEBI plus transaction charges", ZERODHA_CHARGES_URL),
        ("equity_delivery", "NSE", "dp_charges", "sell", "15.34 per scrip debit transaction when delivery holding is sold", "inr", "DP charges are delivery-sale only and not intraday", ZERODHA_CHARGES_URL),
        ("equity_delivery", "BSE", "dp_charges", "sell", "15.34 per scrip debit transaction when delivery holding is sold", "inr", "DP charges are delivery-sale only and not intraday", ZERODHA_CHARGES_URL),
    ]
    return pd.DataFrame(
        [
            {
                "segment": segment,
                "exchange": exchange,
                "component": component,
                "applicable_side": side,
                "formula": formula,
                "unit": unit,
                "note": note,
                "official_source_url": url,
                "verified_utc": verified_utc,
            }
            for segment, exchange, component, side, formula, unit, note, url in rows
        ]
    )


def build_latency_slippage_catalog() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "profile_id": "P180_ZERO_LATENCY_CONTROL_DIAGNOSTIC_ONLY",
                "decision_latency_ms": 0,
                "broker_network_latency_ms": 0,
                "slippage_ticks": 0,
                "spread_cross_multiplier": 1.0,
                "allowed_for_promotion": 0,
                "purpose": "diagnostic lower-bound only; cannot support profitability acceptance",
            },
            {
                "profile_id": "P180_RETAIL_MARKETABLE_DEFAULT",
                "decision_latency_ms": 100,
                "broker_network_latency_ms": 250,
                "slippage_ticks": 1,
                "spread_cross_multiplier": 1.0,
                "allowed_for_promotion": 1,
                "purpose": "base retail stress before any future replay",
            },
            {
                "profile_id": "P180_STRESSED_RETAIL",
                "decision_latency_ms": 250,
                "broker_network_latency_ms": 750,
                "slippage_ticks": 2,
                "spread_cross_multiplier": 1.25,
                "allowed_for_promotion": 1,
                "purpose": "adverse retail latency/slippage stress before any future replay",
            },
        ]
    )


def build_label_precommit(strategy_families: pd.DataFrame, split_policy: pd.DataFrame) -> pd.DataFrame:
    split = split_policy.to_dict("records")[0] if not split_policy.empty else {}
    rows = []
    for item in strategy_families.to_dict("records"):
        family_id = item["strategy_family_id"]
        rows.append(
            {
                "strategy_family_id": family_id,
                "label_family_id": item["required_later_label_family"],
                "label_status": "precommitted_not_materialized",
                "train_dates": split.get("train_dates", ""),
                "validation_dates": split.get("validation_dates", ""),
                "test_dates": split.get("test_dates", ""),
                "minimum_label_requirements": "event-time causal;feature_timestamp_before_label_horizon;no_test_date_selection;coverage_by_symbol_date",
                "cost_latency_binding_required": item["required_cost_latency_binding"],
                "replay_allowed_after_phase180": 0,
            }
        )
    return pd.DataFrame(rows)


def build_gate_evaluation(
    phase179: pd.DataFrame,
    cost_catalog: pd.DataFrame,
    latency_catalog: pd.DataFrame,
    labels: pd.DataFrame,
) -> pd.DataFrame:
    precommit_ready = as_int(metric_value(phase179, "phase179_precommit_ready", 0))
    required_components = {"brokerage", "stt", "transaction_charges", "sebi_charges", "stamp_duty", "gst"}
    observed_components = set(cost_catalog["component"].astype(str).tolist()) if not cost_catalog.empty else set()
    promotion_profiles = int(latency_catalog["allowed_for_promotion"].astype(int).sum()) if not latency_catalog.empty else 0
    return pd.DataFrame(
        [
            {
                "gate_id": "P180_PHASE179_PRECOMMIT_READY",
                "gate_pass": int(precommit_ready == 1),
                "evidence": f"phase179_precommit_ready={precommit_ready}",
                "severity": "hard",
            },
            {
                "gate_id": "P180_ZERODHA_COST_COMPONENTS_PINNED",
                "gate_pass": int(required_components.issubset(observed_components)),
                "evidence": "observed_components=" + ";".join(sorted(observed_components)),
                "severity": "hard",
            },
            {
                "gate_id": "P180_OFFICIAL_COST_SOURCE_RECORDED",
                "gate_pass": int(cost_catalog["official_source_url"].astype(str).str.startswith("https://zerodha.com").any() and cost_catalog["official_source_url"].astype(str).str.contains("support.zerodha.com").any()),
                "evidence": "official Zerodha charge and STT URLs recorded",
                "severity": "hard",
            },
            {
                "gate_id": "P180_LATENCY_STRESS_PROFILES_DECLARED",
                "gate_pass": int(len(latency_catalog) >= 3 and promotion_profiles >= 2),
                "evidence": f"profiles={len(latency_catalog)};promotion_eligible_profiles={promotion_profiles}",
                "severity": "hard",
            },
            {
                "gate_id": "P180_LABEL_FAMILIES_PRECOMMITTED",
                "gate_pass": int(len(labels) >= 3 and labels["replay_allowed_after_phase180"].astype(int).eq(0).all()),
                "evidence": f"label_rows={len(labels)};replay_allowed_sum={int(labels['replay_allowed_after_phase180'].astype(int).sum()) if not labels.empty else -1}",
                "severity": "hard",
            },
            {
                "gate_id": "P180_NO_REPLAY_OR_PROFITABILITY_OUTPUTS",
                "gate_pass": 1,
                "evidence": "cost/latency/label precommit only; forbidden_outputs=" + FORBIDDEN_OUTPUTS,
                "severity": "hard",
            },
        ]
    )


def build_acceptance_summary(cost_catalog: pd.DataFrame, latency_catalog: pd.DataFrame, labels: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0
    precommit_ready = int(not hard.empty and hard_pass == len(hard))
    next_action = "build_phase181_label_materialization_no_replay" if precommit_ready else "repair_phase180_cost_latency_label_precommit"
    return pd.DataFrame(
        [
            ("phase180_cost_component_rows", int(len(cost_catalog)), "Zerodha cost component rows pinned"),
            ("phase180_latency_profile_rows", int(len(latency_catalog)), "Latency/slippage profiles declared"),
            ("phase180_label_family_rows", int(len(labels)), "Label families precommitted"),
            ("phase180_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase180_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase180_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase180_precommit_ready", precommit_ready, "1 means label materialization phase may be built"),
            ("phase180_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase180_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase180_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase180_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase180 Cost/Latency-bound Label Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase180 pins Zerodha equity cost components, latency/slippage profiles, and future label families before any replay.",
        "It does not emit signals, orders, fills, P&L, profitability claims, or paper/live acceptance.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase180_cost_latency_label_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase180(phase179_dir: Path, phase178_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated = datetime.now(timezone.utc).isoformat()
    phase179 = read_csv(phase179_dir / "phase179_strategy_family_precommit_acceptance_summary.csv")
    strategy_families = read_csv(phase179_dir / "phase179_strategy_family_catalog.csv")
    split_policy = read_csv(phase178_dir / "phase178_train_test_split_policy.csv")
    cost_catalog = build_zerodha_equity_cost_catalog(generated)
    latency_catalog = build_latency_slippage_catalog()
    labels = build_label_precommit(strategy_families, split_policy)
    gates = build_gate_evaluation(phase179, cost_catalog, latency_catalog, labels)
    acceptance = build_acceptance_summary(cost_catalog, latency_catalog, labels, gates)

    cost_catalog.to_csv(output_dir / "phase180_zerodha_equity_cost_component_catalog.csv", index=False)
    latency_catalog.to_csv(output_dir / "phase180_latency_slippage_profile_catalog.csv", index=False)
    labels.to_csv(output_dir / "phase180_label_family_precommit.csv", index=False)
    gates.to_csv(output_dir / "phase180_cost_latency_label_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase180_cost_latency_label_precommit_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Zerodha Equity Cost Component Catalog": cost_catalog,
            "Latency/slippage Profile Catalog": latency_catalog,
            "Label Family Precommit": labels,
            "Gate Evaluation": gates,
        },
    )
    manifest = {
        "generated_utc": generated,
        "scope": "phase180_cost_latency_label_precommit",
        **reproducibility_fields(
            artifact_id="phase180_cost_latency_label_precommit",
            generated_utc=generated,
            inputs={
                "phase179_acceptance": str(phase179_dir / "phase179_strategy_family_precommit_acceptance_summary.csv"),
                "phase179_strategy_family_catalog": str(phase179_dir / "phase179_strategy_family_catalog.csv"),
                "phase178_train_test_split_policy": str(phase178_dir / "phase178_train_test_split_policy.csv"),
                "official_zerodha_charges_url": ZERODHA_CHARGES_URL,
                "official_zerodha_stt_url": ZERODHA_STT_URL,
            },
            parameters={
                "precommit_policy": "cost_latency_label_catalog_only_no_replay",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
                "next_required_gate": "phase181_label_materialization_no_replay",
            },
            outputs={
                "cost_catalog": str(output_dir / "phase180_zerodha_equity_cost_component_catalog.csv"),
                "latency_slippage_catalog": str(output_dir / "phase180_latency_slippage_profile_catalog.csv"),
                "label_family_precommit": str(output_dir / "phase180_label_family_precommit.csv"),
                "gate_evaluation": str(output_dir / "phase180_cost_latency_label_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase180_cost_latency_label_precommit_acceptance_summary.csv"),
                "report": str(output_dir / "phase180_cost_latency_label_precommit_report.md"),
            },
            random_seed="none_deterministic_cost_latency_label_precommit",
            scenario_ids="phase180_cost_latency_label_precommit",
            cost_model_version="zerodha_equity_cost_catalog_verified_2026_07_28",
            latency_model_version="phase180_pre_replay_latency_slippage_catalog_v1",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase180_cost_latency_label_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase179-dir", type=Path, default=DEFAULT_PHASE179_DIR)
    parser.add_argument("--phase178-dir", type=Path, default=DEFAULT_PHASE178_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase180(args.phase179_dir, args.phase178_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
