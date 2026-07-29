from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE164_LEDGER = Path("outputs/phase164/phase164_aggregate_trade_ledger.csv")
DEFAULT_PHASE229_DIR = Path("outputs/phase229")
DEFAULT_OUTPUT_DIR = Path("outputs/phase230")

REALISTIC_EXECUTION_PROFILES = {"retail_marketable_default", "stressed_retail"}
CONTROL_EXECUTION_PROFILES = {"zero_latency_spread_only_control"}
GROUP_SCOPES: dict[str, list[str]] = {
    "strategy_profile": ["strategy_id", "execution_profile"],
    "strategy_symbol_profile": ["strategy_id", "execution_profile", "symbol"],
    "strategy_date_profile": ["strategy_id", "execution_profile", "trade_date"],
    "strategy_symbol_date_profile": ["strategy_id", "execution_profile", "symbol", "trade_date"],
}


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


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def prepare_ledger(ledger: pd.DataFrame) -> pd.DataFrame:
    if ledger.empty:
        return ledger
    out = ledger.copy()
    for col in ["trades", "sum_gross_return", "sum_cost_return", "sum_net_return", "net_pnl_inr"]:
        out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0.0)
    out["is_realistic_profile"] = out["execution_profile"].astype(str).isin(REALISTIC_EXECUTION_PROFILES)
    out["is_control_profile"] = out["execution_profile"].astype(str).isin(CONTROL_EXECUTION_PROFILES)
    out["original_net_return"] = out["sum_gross_return"] - out["sum_cost_return"]
    out["inverse_net_return"] = -out["sum_gross_return"] - out["sum_cost_return"]
    out["oracle_signed_net_return"] = out["sum_gross_return"].abs() - out["sum_cost_return"]
    out["original_net_pnl_inr"] = out["original_net_return"] * 100000.0
    out["inverse_net_pnl_inr"] = out["inverse_net_return"] * 100000.0
    out["oracle_signed_net_pnl_inr"] = out["oracle_signed_net_return"] * 100000.0
    out["abs_gross_to_cost_ratio"] = (
        out["sum_gross_return"].abs()
        / out["sum_cost_return"].where(out["sum_cost_return"].abs() > 0, pd.NA).abs()
    )
    return out


def summarize_variant_group(frame: pd.DataFrame, scope_name: str, keys: list[str]) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame()
    group = frame.groupby(keys, as_index=False).agg(
        rows=("strategy_id", "size"),
        trades=("trades", "sum"),
        gross_return=("sum_gross_return", "sum"),
        cost_return=("sum_cost_return", "sum"),
        original_net_return=("original_net_return", "sum"),
        inverse_net_return=("inverse_net_return", "sum"),
        oracle_signed_net_return=("oracle_signed_net_return", "sum"),
        original_net_pnl_inr=("original_net_pnl_inr", "sum"),
        inverse_net_pnl_inr=("inverse_net_pnl_inr", "sum"),
        oracle_signed_net_pnl_inr=("oracle_signed_net_pnl_inr", "sum"),
    )
    group.insert(0, "scope", scope_name)
    group["original_positive"] = group["original_net_return"] > 0
    group["inverse_positive"] = group["inverse_net_return"] > 0
    group["oracle_signed_positive"] = group["oracle_signed_net_return"] > 0
    group["turnover_bucket"] = pd.cut(
        group["trades"],
        bins=[-1, 1, 5, 25, 100, 1000, float("inf")],
        labels=["single_trade", "2_to_5", "6_to_25", "26_to_100", "101_to_1000", "over_1000"],
    ).astype(str)
    group["abs_gross_to_cost_ratio"] = (
        group["gross_return"].abs()
        / group["cost_return"].where(group["cost_return"].abs() > 0, pd.NA).abs()
    )
    return group


def build_variant_screen(ledger: pd.DataFrame) -> pd.DataFrame:
    if ledger.empty:
        return pd.DataFrame()
    realistic = ledger[ledger["is_realistic_profile"]].copy()
    frames = [summarize_variant_group(realistic, scope, keys) for scope, keys in GROUP_SCOPES.items()]
    frames = [frame for frame in frames if not frame.empty]
    if not frames:
        return pd.DataFrame()
    screen = pd.concat(frames, ignore_index=True, sort=False)
    screen["best_expanded_variant"] = "original"
    screen["best_expanded_net_return"] = screen["original_net_return"]
    screen["best_expanded_net_pnl_inr"] = screen["original_net_pnl_inr"]
    inverse_better = screen["inverse_net_return"] > screen["best_expanded_net_return"]
    screen.loc[inverse_better, "best_expanded_variant"] = "inverse_contrarian"
    screen.loc[inverse_better, "best_expanded_net_return"] = screen.loc[inverse_better, "inverse_net_return"]
    screen.loc[inverse_better, "best_expanded_net_pnl_inr"] = screen.loc[inverse_better, "inverse_net_pnl_inr"]
    oracle_better = screen["oracle_signed_net_return"] > screen["best_expanded_net_return"]
    screen.loc[oracle_better, "best_expanded_variant"] = "oracle_signed_upper_bound"
    screen.loc[oracle_better, "best_expanded_net_return"] = screen.loc[oracle_better, "oracle_signed_net_return"]
    screen.loc[oracle_better, "best_expanded_net_pnl_inr"] = screen.loc[oracle_better, "oracle_signed_net_pnl_inr"]
    screen["best_expanded_positive"] = screen["best_expanded_net_return"] > 0
    return screen.sort_values(
        ["best_expanded_net_return", "abs_gross_to_cost_ratio", "trades"],
        ascending=[False, False, True],
        kind="mergesort",
    )


def build_expansion_catalog(screen: pd.DataFrame) -> pd.DataFrame:
    if screen.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for scope, group in screen.groupby("scope", sort=True):
        best = group.head(1)
        rows.append(
            {
                "expansion_id": f"P230_{scope.upper()}_BEST_OF_ORIGINAL_INVERSE_ORACLE",
                "scope": scope,
                "groups_tested": int(len(group)),
                "positive_original_groups": int(group["original_positive"].sum()),
                "positive_inverse_groups": int(group["inverse_positive"].sum()),
                "positive_oracle_signed_groups": int(group["oracle_signed_positive"].sum()),
                "best_expanded_variant": best["best_expanded_variant"].iloc[0] if not best.empty else "none",
                "best_expanded_net_return": float(best["best_expanded_net_return"].iloc[0]) if not best.empty else 0.0,
                "best_expanded_net_pnl_inr": float(best["best_expanded_net_pnl_inr"].iloc[0]) if not best.empty else 0.0,
                "best_trades": int(best["trades"].iloc[0]) if not best.empty else 0,
                "interpretation": "no_positive_group_after_costs" if int(group["best_expanded_positive"].sum()) == 0 else "candidate_requires_strict_holdout_validation",
            }
        )
    return pd.DataFrame(rows).sort_values("best_expanded_net_return", ascending=False, kind="mergesort")


def build_next_strategy_work_order(catalog: pd.DataFrame) -> pd.DataFrame:
    positive_groups = int(catalog["positive_oracle_signed_groups"].sum()) if not catalog.empty else 0
    if positive_groups > 0:
        action = "validate_positive_expanded_groups_on_chronological_holdout"
        rationale = "At least one expanded original/inverse/oracle group clears modeled costs and needs holdout validation."
    else:
        action = "design_materially_new_execution_or_horizon_contract"
        rationale = (
            "Original, inverse and oracle-signed variants of the current Phase164 signal set do not clear realistic costs. "
            "Next search must reduce cost drag structurally through fewer trades, longer horizons, passive/limit assumptions "
            "where modelable, or a genuinely new edge source."
        )
    return pd.DataFrame(
        [
            {
                "work_order_id": "P231_MATERIAL_NEW_LOW_TURNOVER_HIGH_EDGE_STRATEGY_FORMS",
                "action": action,
                "rationale": rationale,
                "candidate_family_1": "opening_range_or_event_window_continuation_with_minimum_expected_move_filter",
                "candidate_family_2": "longer_horizon_cross_sectional_relative_strength_with_turnover_cap",
                "candidate_family_3": "passive_or_midpoint_control_only_if_fill_model_is_explicitly_pessimistic",
                "forbidden_shortcut": "do_not_tune_synthetic_generator_to_create_profit",
            }
        ]
    )


def build_gate_evaluation(ledger: pd.DataFrame, screen: pd.DataFrame, catalog: pd.DataFrame) -> pd.DataFrame:
    realistic_rows = int(ledger["is_realistic_profile"].sum()) if not ledger.empty else 0
    scopes_tested = int(screen["scope"].nunique()) if not screen.empty else 0
    positive_expanded = int(screen["best_expanded_positive"].sum()) if not screen.empty else 0
    positive_oracle = int(screen["oracle_signed_positive"].sum()) if not screen.empty else 0
    return pd.DataFrame(
        [
            {
                "gate_id": "P230_PHASE164_LEDGER_AVAILABLE",
                "passed": len(ledger) > 0,
                "observed_value": int(len(ledger)),
                "required_value": ">0 ledger rows",
                "interpretation": "Full-year synthetic daily/symbol/profile trade ledger is available.",
            },
            {
                "gate_id": "P230_REALISTIC_PROFILE_ROWS_AVAILABLE",
                "passed": realistic_rows > 0,
                "observed_value": realistic_rows,
                "required_value": ">0 realistic rows",
                "interpretation": "Search is evaluated under realistic retail/stressed profiles.",
            },
            {
                "gate_id": "P230_MULTIPLE_EXPANSION_SCOPES_TESTED",
                "passed": scopes_tested >= 4,
                "observed_value": scopes_tested,
                "required_value": ">=4 grouping scopes",
                "interpretation": "Search tests low-turnover selective scopes instead of only full portfolio rows.",
            },
            {
                "gate_id": "P230_EXPANDED_REALISTIC_PROFITABLE_GROUP_FOUND",
                "passed": positive_expanded > 0,
                "observed_value": positive_expanded,
                "required_value": ">0 original/inverse/oracle best groups",
                "interpretation": "If this fails, expanded variants of the current signal set still do not clear modeled costs.",
            },
            {
                "gate_id": "P230_ORACLE_SIGNED_UPPER_BOUND_CLEARS_COST",
                "passed": positive_oracle > 0,
                "observed_value": positive_oracle,
                "required_value": ">0 oracle-signed groups",
                "interpretation": "This is an upper-bound feasibility check; failure means even perfect sign choice at tested scopes cannot beat costs.",
            },
        ]
    )


def metric_frame(rows: list[tuple[str, Any, str]]) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase230 Low-turnover High-edge Strategy Search",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase230 expands beyond the Phase229 ranking by testing original, inverse/contrarian and oracle-signed variants",
        "of the Phase164 full-year synthetic trade ledger across lower-turnover grouping scopes.",
        "The oracle-signed variant is an infeasible upper bound, not a tradable strategy; it asks whether any available",
        "directional signal magnitude could clear modeled realistic costs if sign selection were perfect at that scope.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase230_low_turnover_high_edge_strategy_search_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase230(phase164_ledger_path: Path, phase229_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase229_acceptance = read_csv(phase229_dir / "phase229_strategy_search_acceptance_summary.csv")
    ledger = prepare_ledger(read_csv(phase164_ledger_path))
    screen = build_variant_screen(ledger)
    catalog = build_expansion_catalog(screen)
    work_order = build_next_strategy_work_order(catalog)
    gates = build_gate_evaluation(ledger, screen, catalog)

    best = screen.head(1)
    positive_expanded = int(screen["best_expanded_positive"].sum()) if not screen.empty else 0
    positive_oracle = int(screen["oracle_signed_positive"].sum()) if not screen.empty else 0
    next_action = (
        "run_phase231_validate_positive_expanded_strategy_groups_no_paper_live"
        if positive_expanded > 0
        else "run_phase231_material_new_strategy_forms_longer_horizon_or_pessimistic_passive_no_generator_profit_tuning"
    )
    acceptance = metric_frame(
        [
            ("phase230_low_turnover_high_edge_search_complete", 1, "Phase230 search completed"),
            ("phase230_phase229_positive_realistic_candidate_rows", as_int(metric_value(phase229_acceptance, "phase229_positive_realistic_candidate_rows", 0)), "Inherited Phase229 positive realistic candidates"),
            ("phase230_phase164_ledger_rows", int(len(ledger)), "Phase164 ledger rows scanned"),
            ("phase230_realistic_ledger_rows", int(ledger["is_realistic_profile"].sum()) if not ledger.empty else 0, "Realistic retail/stressed rows scanned"),
            ("phase230_group_scope_rows", int(len(catalog)), "Expansion scope rows summarized"),
            ("phase230_variant_group_rows", int(len(screen)), "Variant groups tested across scopes"),
            ("phase230_positive_expanded_group_rows", positive_expanded, "Positive original/inverse/oracle best groups"),
            ("phase230_positive_oracle_signed_group_rows", positive_oracle, "Positive oracle-signed upper-bound groups"),
            ("phase230_best_scope", best["scope"].iloc[0] if not best.empty else "none", "Best expanded scope"),
            ("phase230_best_strategy_id", best["strategy_id"].iloc[0] if not best.empty and "strategy_id" in best.columns else "none", "Best expanded strategy id where present"),
            ("phase230_best_execution_profile", best["execution_profile"].iloc[0] if not best.empty and "execution_profile" in best.columns else "none", "Best expanded execution profile"),
            ("phase230_best_expanded_variant", best["best_expanded_variant"].iloc[0] if not best.empty else "none", "Best among original/inverse/oracle variants"),
            ("phase230_best_expanded_net_return", float(best["best_expanded_net_return"].iloc[0]) if not best.empty else 0.0, "Best expanded net return"),
            ("phase230_best_expanded_net_pnl_inr", float(best["best_expanded_net_pnl_inr"].iloc[0]) if not best.empty else 0.0, "Best expanded net P&L INR"),
            ("phase230_strategy_promotion_allowed", 0, "No promotion from synthetic expansion alone"),
            ("phase230_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from synthetic expansion alone"),
            ("phase230_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from synthetic expansion alone"),
            ("phase230_next_best_action", next_action, "Next strategy-discovery milestone"),
        ]
    )

    screen.to_csv(output_dir / "phase230_variant_group_screen.csv", index=False)
    catalog.to_csv(output_dir / "phase230_expansion_catalog.csv", index=False)
    work_order.to_csv(output_dir / "phase230_phase231_work_order.csv", index=False)
    gates.to_csv(output_dir / "phase230_strategy_search_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase230_strategy_search_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Expansion Catalog": catalog,
            "Top Variant Groups": screen.head(12),
            "Phase231 Work Order": work_order,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase230_low_turnover_high_edge_strategy_search",
        **reproducibility_fields(
            artifact_id="phase230",
            generated_utc=generated_utc,
            inputs={
                "phase164_aggregate_trade_ledger": str(phase164_ledger_path),
                "phase229_acceptance_summary": str(phase229_dir / "phase229_strategy_search_acceptance_summary.csv"),
            },
            parameters={
                "realistic_execution_profiles": sorted(REALISTIC_EXECUTION_PROFILES),
                "tested_variants": ["original", "inverse_contrarian", "oracle_signed_upper_bound"],
                "group_scopes": GROUP_SCOPES,
                "oracle_signed_upper_bound_is_tradable": 0,
                "generator_profit_tuning_allowed": 0,
            },
            outputs={
                "variant_group_screen": str(output_dir / "phase230_variant_group_screen.csv"),
                "expansion_catalog": str(output_dir / "phase230_expansion_catalog.csv"),
                "phase231_work_order": str(output_dir / "phase230_phase231_work_order.csv"),
                "gate_evaluation": str(output_dir / "phase230_strategy_search_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase230_strategy_search_acceptance_summary.csv"),
                "report": str(output_dir / "phase230_low_turnover_high_edge_strategy_search_report.md"),
                "manifest": str(output_dir / "phase230_low_turnover_high_edge_strategy_search_manifest.json"),
            },
            random_seed="none_deterministic_phase164_ledger_screen",
            scenario_ids="phase164_full_year_realistic_profiles",
            cost_model_version="zerodha_equity_intraday_nse_order_formula_v2_2026_07_14",
            latency_model_version="phase164_existing_execution_profiles",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase230_low_turnover_high_edge_strategy_search_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Expand strategy search toward lower-turnover/high-edge variants.")
    parser.add_argument("--phase164-ledger", type=Path, default=DEFAULT_PHASE164_LEDGER)
    parser.add_argument("--phase229-dir", type=Path, default=DEFAULT_PHASE229_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase230(
        phase164_ledger_path=args.phase164_ledger,
        phase229_dir=args.phase229_dir,
        output_dir=args.output_dir,
        base_dir=args.base_dir,
    )


if __name__ == "__main__":
    main()
