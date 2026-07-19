from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase56_cost_clearing_label_discovery import DEFAULT_ORDER_NOTIONAL_INR
from synthetic_l2.phase61_lower_frequency_candidate_sweep import profile_cost_bps, retail_profile
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase85")
DEFAULT_PHASE83_DIR = Path("outputs/phase83")
EDGE_QUANTILES = [0.50, 0.70, 0.80, 0.90, 0.95, 0.975, 0.99]
SAFETY_MULTIPLIERS = [1.0, 1.25, 1.5, 2.0]


def load_bars(phase83_dir: Path) -> pd.DataFrame:
    path = phase83_dir / "stratified_source_event_bars.parquet"
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_parquet(path)


def add_cost_budget_columns(bars: pd.DataFrame) -> pd.DataFrame:
    frame = bars.copy()
    profile = retail_profile()
    slippage_ticks = float(profile["fixed_slippage_ticks"])
    impact_bps = float(profile["impact_bps"]) + float(profile.get("fees_bps", 0.0))
    zerodha_bps = profile_cost_bps(profile)
    spread_bps = frame["avg_spread"].astype(float) / frame["close_mid_price"].replace(0, np.nan).astype(float) * 10000.0
    frame["spread_cross_bps"] = spread_bps
    frame["half_spread_bps"] = spread_bps / 2.0
    frame["slippage_bps"] = slippage_ticks * spread_bps
    frame["impact_plus_execution_bps"] = impact_bps
    frame["zerodha_charge_bps"] = zerodha_bps
    frame["one_way_cost_hurdle_bps"] = frame["half_spread_bps"] + frame["slippage_bps"] + frame["impact_plus_execution_bps"] + frame["zerodha_charge_bps"]
    frame["abs_next_return_bps"] = frame["next_bar_return"].abs() * 10000.0
    return frame


def symbol_month_budget(frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    valid = frame[frame["next_bar_return"].notna()].copy()
    for (month, symbol), group in valid.groupby(["trade_month", "symbol"], sort=True):
        row: dict[str, Any] = {
            "trade_month": month,
            "symbol": symbol,
            "bars": int(len(group)),
            "median_cost_hurdle_bps": float(group["one_way_cost_hurdle_bps"].median()),
            "p75_cost_hurdle_bps": float(group["one_way_cost_hurdle_bps"].quantile(0.75)),
            "p90_cost_hurdle_bps": float(group["one_way_cost_hurdle_bps"].quantile(0.90)),
            "median_spread_cross_bps": float(group["spread_cross_bps"].median()),
            "median_abs_next_return_bps": float(group["abs_next_return_bps"].median()),
            "p90_abs_next_return_bps": float(group["abs_next_return_bps"].quantile(0.90)),
            "p95_abs_next_return_bps": float(group["abs_next_return_bps"].quantile(0.95)),
            "p99_abs_next_return_bps": float(group["abs_next_return_bps"].quantile(0.99)),
        }
        for multiplier in SAFETY_MULTIPLIERS:
            hurdle = group["one_way_cost_hurdle_bps"] * float(multiplier)
            row[f"fraction_abs_return_ge_{str(multiplier).replace('.', '_')}x_cost"] = float((group["abs_next_return_bps"] >= hurdle).mean())
        row["cost_budget_status"] = (
            "tail_edge_available"
            if row["fraction_abs_return_ge_1_25x_cost"] >= 0.10 and row["p95_abs_next_return_bps"] >= row["median_cost_hurdle_bps"] * 1.25
            else "cost_budget_tight"
        )
        rows.append(row)
    return pd.DataFrame(rows)


def monthly_budget_summary(symbol_month: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for month, group in symbol_month.groupby("trade_month", sort=True):
        rows.append(
            {
                "trade_month": month,
                "symbols": int(group["symbol"].nunique()),
                "median_symbol_cost_hurdle_bps": float(group["median_cost_hurdle_bps"].median()),
                "median_symbol_p95_abs_next_return_bps": float(group["p95_abs_next_return_bps"].median()),
                "median_fraction_abs_return_ge_1_25x_cost": float(group["fraction_abs_return_ge_1_25x_cost"].median()),
                "tail_edge_available_symbols": int(group["cost_budget_status"].eq("tail_edge_available").sum()),
                "tail_edge_available_fraction": float(group["cost_budget_status"].eq("tail_edge_available").mean()),
            }
        )
    return pd.DataFrame(rows)


def feature_cost_budget_scan(frame: pd.DataFrame) -> pd.DataFrame:
    features = [
        ("abs_bar_return", frame["bar_return"].abs() * 10000.0),
        ("abs_l1_imbalance", frame["avg_l1_imbalance"].abs()),
        ("abs_l5_imbalance", frame["avg_l5_imbalance"].abs()),
        ("abs_microprice_dev_bps", frame["avg_microprice_dev"].abs() * 10000.0),
        ("event_intensity", frame["avg_event_intensity_proxy"].astype(float)),
    ]
    rows: list[dict[str, Any]] = []
    valid = frame[frame["next_bar_return"].notna()].copy()
    for feature_name, values in features:
        valid_feature = valid.copy()
        valid_feature[feature_name] = values.loc[valid.index].astype(float)
        for quantile in EDGE_QUANTILES:
            threshold = float(valid_feature[feature_name].quantile(quantile))
            selected = valid_feature[valid_feature[feature_name] >= threshold].copy()
            if selected.empty:
                continue
            rows.append(
                {
                    "feature_name": feature_name,
                    "quantile": quantile,
                    "threshold": threshold,
                    "selected_bars": int(len(selected)),
                    "selected_fraction": float(len(selected) / len(valid_feature)),
                    "mean_abs_next_return_bps": float(selected["abs_next_return_bps"].mean()),
                    "median_abs_next_return_bps": float(selected["abs_next_return_bps"].median()),
                    "median_cost_hurdle_bps": float(selected["one_way_cost_hurdle_bps"].median()),
                    "fraction_abs_return_ge_1x_cost": float((selected["abs_next_return_bps"] >= selected["one_way_cost_hurdle_bps"]).mean()),
                    "fraction_abs_return_ge_1_25x_cost": float((selected["abs_next_return_bps"] >= selected["one_way_cost_hurdle_bps"] * 1.25).mean()),
                    "fraction_abs_return_ge_1_5x_cost": float((selected["abs_next_return_bps"] >= selected["one_way_cost_hurdle_bps"] * 1.5).mean()),
                    "candidate_budget_status": "eligible_filter_seed"
                    if float((selected["abs_next_return_bps"] >= selected["one_way_cost_hurdle_bps"] * 1.25).mean()) >= 0.15
                    else "insufficient_cost_clearance",
                }
            )
    return pd.DataFrame(rows).sort_values(
        ["fraction_abs_return_ge_1_25x_cost", "mean_abs_next_return_bps"],
        ascending=[False, False],
        kind="mergesort",
    )


def precommit_contract(feature_scan: pd.DataFrame) -> pd.DataFrame:
    eligible = feature_scan[feature_scan["candidate_budget_status"].eq("eligible_filter_seed")].head(10).copy()
    if eligible.empty:
        return pd.DataFrame(
            [
                {
                    "contract_id": "P85_NO_REPLAY_WITHOUT_COST_BUDGET_EDGE",
                    "allowed": False,
                    "rule": "No new strategy replay may run unless its pre-signal filter has >=15% of selected bars clearing 1.25x one-way cost in Phase85 or a later cost-budget audit.",
                    "evidence": "No simple feature filter cleared the eligibility threshold.",
                    "next_action": "design stronger regime-conditioned composite features before replay",
                }
            ]
        )
    rows = []
    for rank, row in enumerate(eligible.itertuples(index=False), start=1):
        rows.append(
            {
                "contract_id": f"P85_ELIGIBLE_FILTER_SEED_{rank:02d}",
                "allowed": True,
                "feature_name": row.feature_name,
                "quantile": row.quantile,
                "threshold": row.threshold,
                "fraction_abs_return_ge_1_25x_cost": row.fraction_abs_return_ge_1_25x_cost,
                "rule": "May be used only as a pre-filter seed; direction and execution logic still require disjoint validation.",
                "next_action": "combine_with_regime_context_and_validate_direction_out_of_sample",
            }
        )
    return pd.DataFrame(rows)


def summarize(symbol_month: pd.DataFrame, monthly: pd.DataFrame, feature_scan: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    eligible_filters = int(feature_scan["candidate_budget_status"].eq("eligible_filter_seed").sum()) if not feature_scan.empty else 0
    tail_fraction = float(symbol_month["cost_budget_status"].eq("tail_edge_available").mean()) if not symbol_month.empty else 0.0
    allowed_contracts = int(contract["allowed"].astype(bool).sum()) if "allowed" in contract else 0
    gate_pass = bool(allowed_contracts > 0)
    return pd.DataFrame(
        [
            ("phase85_symbol_month_rows", int(len(symbol_month)), "Symbol-month cost budget rows"),
            ("phase85_tail_edge_available_symbol_month_fraction", tail_fraction, "Fraction of symbol-months with tail edge available"),
            ("phase85_feature_filter_rows", int(len(feature_scan)), "Feature filter budget rows"),
            ("phase85_eligible_filter_seeds", eligible_filters, "Feature filters passing cost-budget eligibility"),
            ("phase85_allowed_precommit_contracts", allowed_contracts, "Allowed precommit filter contracts"),
            ("phase85_cost_budget_signal_design_pass", int(gate_pass), "1 means at least one filter seed can move to precommitted signal design"),
            (
                "phase85_recommend_next_action",
                "precommit_composite_regime_conditioned_signal_family" if gate_pass else "design_stronger_composite_features_before_replay",
                "Recommended next milestone",
            ),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase85 Cost-Budget Signal Design Gate",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase85 creates a cost-budget gate for future strategy work using the Phase83 cached stratified bars.",
        "It estimates one-way retail execution hurdles from spread, slippage, impact, and Zerodha charges before allowing any new replay branch.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase85_cost_budget_signal_design_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase85(phase83_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    bars = add_cost_budget_columns(load_bars(phase83_dir))
    symbol_month = symbol_month_budget(bars)
    monthly = monthly_budget_summary(symbol_month)
    feature_scan = feature_cost_budget_scan(bars)
    contract = precommit_contract(feature_scan)
    acceptance = summarize(symbol_month, monthly, feature_scan, contract)

    symbol_month.to_csv(output_dir / "symbol_month_cost_budget.csv", index=False)
    monthly.to_csv(output_dir / "monthly_cost_budget_summary.csv", index=False)
    feature_scan.to_csv(output_dir / "feature_filter_cost_budget_scan.csv", index=False)
    contract.to_csv(output_dir / "precommit_signal_filter_contract.csv", index=False)
    acceptance.to_csv(output_dir / "cost_budget_signal_design_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Monthly Cost Budget Summary": monthly,
            "Top Feature Filter Cost-Budget Rows": feature_scan.head(25),
            "Precommit Signal Filter Contract": contract,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase85_cost_budget_signal_design",
        "cost_budget_signal_design_pass": int(
            acceptance.loc[acceptance["metric"].eq("phase85_cost_budget_signal_design_pass"), "value"].iloc[0]
        ),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase85",
            generated_utc=generated_utc,
            inputs={"phase83_bar_cache": str(phase83_dir / "stratified_source_event_bars.parquet")},
            parameters={
                "execution_profile": "retail_marketable_default",
                "order_notional_inr": DEFAULT_ORDER_NOTIONAL_INR,
                "eligibility": "feature_filter_selected_bars_fraction_abs_next_return_ge_1_25x_cost_ge_0_15",
            },
            outputs={
                "symbol_month_budget": str(output_dir / "symbol_month_cost_budget.csv"),
                "monthly_budget": str(output_dir / "monthly_cost_budget_summary.csv"),
                "feature_scan": str(output_dir / "feature_filter_cost_budget_scan.csv"),
                "precommit_contract": str(output_dir / "precommit_signal_filter_contract.csv"),
                "acceptance_summary": str(output_dir / "cost_budget_signal_design_acceptance_summary.csv"),
                "report": str(output_dir / "phase85_cost_budget_signal_design_report.md"),
                "manifest": str(output_dir / "phase85_cost_budget_signal_design_manifest.json"),
            },
            random_seed="none_deterministic_cost_budget_gate",
            scenario_ids="phase85_phase83_cached_stratified_bars",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase83_source_event_ordinal_alignment",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase85_cost_budget_signal_design_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build cost-budget signal design gate.")
    parser.add_argument("--phase83-dir", type=Path, default=DEFAULT_PHASE83_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase85(args.phase83_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
