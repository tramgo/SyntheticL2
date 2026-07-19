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


DEFAULT_OUTPUT_DIR = Path("outputs/phase125")
DEFAULT_PHASE123_DIR = Path("outputs/phase123")
DEFAULT_PHASE124_DIR = Path("outputs/phase124")
DEFAULT_PHASE116_DIR = Path("outputs/phase116")
DEFAULT_PHASE117_DIR = Path("outputs/phase117")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def read_metric_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["metric", "value", "description"])
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    value = rows.iloc[0]
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def parse_threshold_model(model_id: str) -> tuple[str, str, float]:
    prefix = "threshold_"
    if not model_id.startswith(prefix):
        return "", "", 0.0
    body = model_id[len(prefix) :]
    if "_ge_" in body:
        feature, value = body.rsplit("_ge_", 1)
        return feature, "ge", float(value)
    if "_le_" in body:
        feature, value = body.rsplit("_le_", 1)
        return feature, "le", float(value)
    return "", "", 0.0


def build_integration_rules(selection: pd.DataFrame) -> pd.DataFrame:
    rows = []
    selected = selection[selection["model_selected"].astype(str).str.lower().isin(["true", "1", "yes"])].copy() if not selection.empty else pd.DataFrame()
    for item in selected.to_dict("records"):
        feature, direction, threshold = parse_threshold_model(str(item["selected_model_id"]))
        if not feature:
            continue
        if str(item["label"]) == "regime_realism_risk_label":
            action = "flag_symbol_month_for_realism_review"
            usage_scope = "generator_diagnostics_and_evidence_weighting"
        elif str(item["label"]) == "opportunity_abstention_label":
            action = "disable_future_strategy_candidate_generation_for_symbol_month"
            usage_scope = "pre_replay_abstention_filter_only"
        else:
            action = "diagnostic_flag_only"
            usage_scope = "diagnostics_only"
        rows.append(
            {
                "filter_id": f"P125_{str(item['label']).replace('_label', '').upper()}",
                "source_label": item["label"],
                "selected_model_id": item["selected_model_id"],
                "feature": feature,
                "direction": direction,
                "threshold": threshold,
                "holdout_brier": item.get("best_brier"),
                "brier_improvement": item.get("brier_improvement"),
                "holdout_auc": item.get("holdout_auc"),
                "integration_action": action,
                "usage_scope": usage_scope,
                "may_block_candidate_generation": str(item["label"]) == "opportunity_abstention_label",
                "may_change_order_side_or_size": False,
                "may_open_replay": False,
                "may_support_profitability_claim": False,
            }
        )
    return pd.DataFrame(rows)


def apply_rules(matrix: pd.DataFrame, rules: pd.DataFrame) -> pd.DataFrame:
    if matrix.empty or rules.empty:
        return pd.DataFrame()
    rows = []
    for rule in rules.to_dict("records"):
        feature = str(rule["feature"])
        if feature not in matrix.columns:
            continue
        values = pd.to_numeric(matrix[feature], errors="coerce").fillna(0.0)
        threshold = float(rule["threshold"])
        if str(rule["direction"]) == "ge":
            flag = values >= threshold
        else:
            flag = values <= threshold
        frame = matrix[["trade_month", "symbol", feature]].copy()
        frame["filter_id"] = rule["filter_id"]
        frame["source_label"] = rule["source_label"]
        frame["filter_flag"] = flag.astype(int)
        frame["integration_action"] = rule["integration_action"]
        frame["may_open_replay"] = 0
        rows.append(frame.rename(columns={feature: "feature_value"}))
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def build_filter_impact(flags: pd.DataFrame) -> pd.DataFrame:
    if flags.empty:
        return pd.DataFrame()
    return (
        flags.groupby(["filter_id", "source_label", "integration_action"], sort=True)
        .agg(
            rows=("filter_flag", "count"),
            flagged_rows=("filter_flag", "sum"),
            symbols=("symbol", "nunique"),
            months=("trade_month", "nunique"),
        )
        .reset_index()
        .assign(flagged_fraction=lambda df: df["flagged_rows"] / df["rows"].replace(0, pd.NA))
    )


def build_guardrails() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "guardrail_id": "P125_NO_TRADE_SIGNAL",
                "requirement": "Integrated filters may only emit diagnostic or abstention flags.",
                "enforcement": "No side, order model, order quantity, or entry/exit field is emitted.",
            },
            {
                "guardrail_id": "P125_NO_REPLAY_OPEN",
                "requirement": "Filter integration cannot open strategy replay.",
                "enforcement": "may_open_replay is false for every rule and strategy_replay_allowed remains 0.",
            },
            {
                "guardrail_id": "P125_NO_PROFITABILITY_CLAIM",
                "requirement": "Filter holdout calibration does not imply trading profitability.",
                "enforcement": "Reports call the filters diagnostics/abstention only.",
            },
            {
                "guardrail_id": "P125_REAL_ANCHOR_PRECEDENCE",
                "requirement": "Real-anchor acquisition remains the higher-priority path for strategy evidence.",
                "enforcement": "Phase117-ready-day blocker is carried into acceptance summary.",
            },
        ]
    )


def build_gate_evaluation(rules: pd.DataFrame, flags: pd.DataFrame, phase116: pd.DataFrame) -> pd.DataFrame:
    replay_allowed = as_int(metric_value(phase116, "phase116_same_family_shard_continuation_allowed"))
    return pd.DataFrame(
        [
            {
                "gate_id": "P125_SELECTED_RULES_PRESENT",
                "gate_pass": int(not rules.empty),
                "evidence": f"rules={len(rules)}",
            },
            {
                "gate_id": "P125_FLAGS_GENERATED",
                "gate_pass": int(not flags.empty),
                "evidence": f"flag_rows={len(flags)}",
            },
            {
                "gate_id": "P125_RULES_CANNOT_OPEN_REPLAY",
                "gate_pass": int((not rules.empty) and not rules["may_open_replay"].astype(bool).any()),
                "evidence": "all may_open_replay false",
            },
            {
                "gate_id": "P125_GLOBAL_REPLAY_LOCK",
                "gate_pass": int(replay_allowed == 0),
                "evidence": f"phase116_same_family_shard_continuation_allowed={replay_allowed}",
            },
        ]
    )


def build_acceptance_summary(rules: pd.DataFrame, flags: pd.DataFrame, impact: pd.DataFrame, gates: pd.DataFrame, phase117: pd.DataFrame) -> pd.DataFrame:
    ready_days = as_int(metric_value(phase117, "phase117_current_ready_real_anchor_days"))
    needed_days = as_int(metric_value(phase117, "phase117_additional_days_needed_for_min"))
    abstention_rules = int(rules["may_block_candidate_generation"].astype(bool).sum()) if not rules.empty else 0
    flagged_rows = int(flags["filter_flag"].sum()) if not flags.empty else 0
    return pd.DataFrame(
        [
            ("phase125_filter_rules", int(len(rules)), "Selected non-trading filter rules integrated"),
            ("phase125_abstention_filter_rules", abstention_rules, "Rules allowed to block future candidate generation only"),
            ("phase125_filter_flag_rows", int(len(flags)), "Symbol/month filter flag rows emitted"),
            ("phase125_flagged_symbol_month_rows", flagged_rows, "Total flagged symbol/month rows across all filters"),
            ("phase125_filter_impact_rows", int(len(impact)), "Filter impact summary rows"),
            ("phase125_gate_rows", int(len(gates)), "Integration gates evaluated"),
            ("phase125_all_gates_pass", int(gates["gate_pass"].astype(bool).all()) if not gates.empty else 0, "1 means integration contract is internally consistent"),
            ("phase125_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase125_ready_real_anchor_days", ready_days, "Real-anchor days still available"),
            ("phase125_real_anchor_days_needed_for_min", needed_days, "Additional real days still needed for minimum strategy replay gate"),
            ("phase125_next_best_action", "use_filters_as_diagnostics_only_and_continue_real_anchor_acquisition", "Recommended next milestone"),
            ("phase125_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Cost model retained for audit continuity"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase125 Filter Integration Contract",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase125 packages selected Phase124 filters as diagnostic/abstention integration rules.",
        "The contract deliberately emits no buy/sell signals and does not open strategy replay.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase125_filter_integration_contract_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase125(base_dir: Path, output_dir: Path, phase123_dir: Path, phase124_dir: Path, phase116_dir: Path, phase117_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    matrix = read_csv(base_dir / phase123_dir / "filter_label_matrix.csv")
    selection = read_csv(base_dir / phase124_dir / "filter_baseline_model_selection.csv")
    phase116 = read_metric_table(base_dir / phase116_dir / "phase116_profitability_verdict_acceptance_summary.csv")
    phase117 = read_metric_table(base_dir / phase117_dir / "phase117_real_anchor_acquisition_acceptance_summary.csv")
    rules = build_integration_rules(selection)
    flags = apply_rules(matrix, rules)
    impact = build_filter_impact(flags)
    guardrails = build_guardrails()
    gates = build_gate_evaluation(rules, flags, phase116)
    acceptance = build_acceptance_summary(rules, flags, impact, gates, phase117)

    rules.to_csv(output_dir / "filter_integration_rules.csv", index=False)
    flags.to_csv(output_dir / "filter_symbol_month_flags.csv", index=False)
    impact.to_csv(output_dir / "filter_impact_summary.csv", index=False)
    guardrails.to_csv(output_dir / "filter_integration_guardrails.csv", index=False)
    gates.to_csv(output_dir / "filter_integration_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase125_filter_integration_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Filter Integration Rules": rules,
            "Filter Impact Summary": impact,
            "Guardrails": guardrails,
            "Gate Evaluation": gates,
            "Filter Flags Sample": flags.head(40),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase125_filter_integration_contract",
        "strategy_replay_allowed": 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase125",
            generated_utc=generated_utc,
            inputs={
                "phase123_filter_label_matrix": str(phase123_dir / "filter_label_matrix.csv"),
                "phase124_model_selection": str(phase124_dir / "filter_baseline_model_selection.csv"),
                "phase116_acceptance": str(phase116_dir / "phase116_profitability_verdict_acceptance_summary.csv"),
                "phase117_acceptance": str(phase117_dir / "phase117_real_anchor_acquisition_acceptance_summary.csv"),
            },
            parameters={
                "integration_policy": "diagnostic_and_abstention_only",
                "replay_policy": "closed",
                "profitability_policy": "no_profitability_claim",
            },
            outputs={
                "rules": str(output_dir / "filter_integration_rules.csv"),
                "flags": str(output_dir / "filter_symbol_month_flags.csv"),
                "impact": str(output_dir / "filter_impact_summary.csv"),
                "guardrails": str(output_dir / "filter_integration_guardrails.csv"),
                "gates": str(output_dir / "filter_integration_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase125_filter_integration_acceptance_summary.csv"),
                "report": str(output_dir / "phase125_filter_integration_contract_report.md"),
                "manifest": str(output_dir / "phase125_filter_integration_contract_manifest.json"),
            },
            random_seed="none_deterministic_integration_contract",
            scenario_ids="phase125_non_trading_filter_integration_contract",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_filter_integration",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase125_filter_integration_contract_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase125 non-trading filter integration contract.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--phase123-dir", type=Path, default=DEFAULT_PHASE123_DIR)
    parser.add_argument("--phase124-dir", type=Path, default=DEFAULT_PHASE124_DIR)
    parser.add_argument("--phase116-dir", type=Path, default=DEFAULT_PHASE116_DIR)
    parser.add_argument("--phase117-dir", type=Path, default=DEFAULT_PHASE117_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase125(
        base_dir=args.base_dir,
        output_dir=args.output_dir,
        phase123_dir=args.phase123_dir,
        phase124_dir=args.phase124_dir,
        phase116_dir=args.phase116_dir,
        phase117_dir=args.phase117_dir,
    )


if __name__ == "__main__":
    main()
