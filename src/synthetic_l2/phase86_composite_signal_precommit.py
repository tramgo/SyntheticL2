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


DEFAULT_OUTPUT_DIR = Path("outputs/phase86")
DEFAULT_PHASE85_DIR = Path("outputs/phase85")


def load_phase85_contract(phase85_dir: Path) -> pd.DataFrame:
    path = phase85_dir / "precommit_signal_filter_contract.csv"
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def selected_filter_seeds(contract: pd.DataFrame) -> pd.DataFrame:
    allowed = contract[contract["allowed"].astype(str).str.lower().eq("true")].copy()
    if allowed.empty:
        return pd.DataFrame()
    keep = allowed[
        allowed["feature_name"].isin(["event_intensity", "abs_bar_return"])
        & allowed["quantile"].astype(float).isin([0.90, 0.95, 0.975, 0.99])
    ].copy()
    return keep.sort_values(["fraction_abs_return_ge_1_25x_cost", "feature_name"], ascending=[False, True], kind="mergesort").head(6)


def build_signal_family(seeds: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {
            "family_id": "P86_INTENSITY_MOMENTUM_CONTINUATION",
            "hypothesis": "High event-intensity bars with same-sign current bar return may continue for one source-event bar when cost budget is favorable.",
            "direction_rule": "side = sign(bar_return)",
            "required_filters": "event_intensity_seed AND abs_bar_return_seed AND one_way_cost_hurdle_bps <= symbol_month_p75_cost_hurdle_bps",
            "excluded_conditions": "ETF targets excluded only if later cross-symbol variant is used; no HDFCBANK leader rule reuse.",
            "position_model": "single_bar_marketable_entry_exit_proxy",
            "why_not_posthoc": "Feature seeds are imported from Phase85 cost-budget ranking before directional P&L is evaluated.",
        },
        {
            "family_id": "P86_INTENSITY_MEAN_REVERSION",
            "hypothesis": "Extreme high event-intensity bars may overreact and reverse for one source-event bar when current bar move is large.",
            "direction_rule": "side = -sign(bar_return)",
            "required_filters": "event_intensity_seed AND abs_bar_return_seed AND one_way_cost_hurdle_bps <= symbol_month_p75_cost_hurdle_bps",
            "excluded_conditions": "No HDFCBANK leader rule reuse; no symbol-specific tuning before disjoint validation.",
            "position_model": "single_bar_marketable_entry_exit_proxy",
            "why_not_posthoc": "Continuation and reversion are both precommitted as competing hypotheses before P&L inspection.",
        },
        {
            "family_id": "P86_SHOCK_INTENSITY_REVERSAL",
            "hypothesis": "On market/symbol shock bars, high intensity plus large current move may reverse after liquidity shock exhaustion.",
            "direction_rule": "side = -sign(bar_return)",
            "required_filters": "shock_bar AND event_intensity_seed AND abs_bar_return_seed",
            "excluded_conditions": "Must report shock and non-shock separately; no pooling-only acceptance.",
            "position_model": "single_bar_marketable_entry_exit_proxy",
            "why_not_posthoc": "Shock split is motivated by Phase72/79/83 generator shock diagnostics before replay.",
        },
    ]
    frame = pd.DataFrame(rows)
    if not seeds.empty:
        intensity = seeds[seeds["feature_name"].eq("event_intensity")].head(3)
        move = seeds[seeds["feature_name"].eq("abs_bar_return")].head(3)
        frame["event_intensity_seed_thresholds"] = "|".join(f"q{row.quantile}:{row.threshold}" for row in intensity.itertuples(index=False))
        frame["abs_bar_return_seed_thresholds"] = "|".join(f"q{row.quantile}:{row.threshold}" for row in move.itertuples(index=False))
    return frame


def validation_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "gate_id": "P86_SPLIT_LOCK",
                "requirement": "Use train months 2026-01 through 2026-06 only for selecting among precommitted families; test months 2026-07 through 2026-12 are untouched until final evaluation.",
                "pass_threshold": "No thresholds may be changed after Phase86.",
            },
            {
                "gate_id": "P86_COST_CLEARANCE",
                "requirement": "A candidate must have positive after-cost net P&L and precision_cost_clear >= 0.55 on both train and test.",
                "pass_threshold": "train_pass=1 and test_pass=1",
            },
            {
                "gate_id": "P86_BREADTH",
                "requirement": "A candidate must trade at least 1000 bars in train and 1000 bars in test, with at least 20 symbols represented.",
                "pass_threshold": "train_trades>=1000; test_trades>=1000; train_symbols>=20; test_symbols>=20",
            },
            {
                "gate_id": "P86_MONTH_STABILITY",
                "requirement": "At least 4/6 test months must be after-cost positive, and no single month may contribute more than 50% of total test net P&L.",
                "pass_threshold": "test_positive_months>=4 and max_month_contribution_abs<=0.50",
            },
            {
                "gate_id": "P86_COST_DRAG",
                "requirement": "Cost drag divided by absolute gross P&L must be <= 0.60 on test.",
                "pass_threshold": "test_cost_drag_to_abs_gross_ratio<=0.60",
            },
            {
                "gate_id": "P86_RETIREMENT",
                "requirement": "If no precommitted family passes, retire this composite family class rather than widening thresholds in the same run.",
                "pass_threshold": "No in-run threshold widening allowed",
            },
        ]
    )


def run_plan(seeds: pd.DataFrame, families: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("phase86_selected_filter_seed_rows", int(len(seeds)), "Phase85 filter seeds selected for precommit"),
            ("phase86_precommitted_family_rows", int(len(families)), "Composite signal families precommitted"),
            ("phase86_validation_gate_rows", int(len(gates)), "Validation gates locked before P&L replay"),
            ("phase86_train_months", "2026-01|2026-02|2026-03|2026-04|2026-05|2026-06", "Train months for family selection"),
            ("phase86_test_months", "2026-07|2026-08|2026-09|2026-10|2026-11|2026-12", "Untouched test months for final evaluation"),
            ("phase86_ready_for_replay", int(len(seeds) > 0 and len(families) > 0 and len(gates) >= 5), "1 means Phase87 replay may run"),
            ("phase86_recommend_next_action", "run_precommitted_composite_signal_replay", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase86 Composite Signal Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase86 locks the next signal-family experiment before directional P&L is inspected.",
        "It uses Phase85 cost-budget seeds but precommits family definitions, train/test split, and retirement gates.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase86_composite_signal_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase86(phase85_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    contract = load_phase85_contract(phase85_dir)
    seeds = selected_filter_seeds(contract)
    families = build_signal_family(seeds)
    gates = validation_contract()
    acceptance = run_plan(seeds, families, gates)

    seeds.to_csv(output_dir / "selected_filter_seeds.csv", index=False)
    families.to_csv(output_dir / "precommitted_composite_signal_families.csv", index=False)
    gates.to_csv(output_dir / "precommitted_validation_gates.csv", index=False)
    acceptance.to_csv(output_dir / "composite_signal_precommit_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Selected Filter Seeds": seeds,
            "Precommitted Composite Signal Families": families,
            "Precommitted Validation Gates": gates,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase86_composite_signal_precommit",
        "ready_for_replay": int(acceptance.loc[acceptance["metric"].eq("phase86_ready_for_replay"), "value"].iloc[0]),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase86",
            generated_utc=generated_utc,
            inputs={"phase85_precommit_filter_contract": str(phase85_dir / "precommit_signal_filter_contract.csv")},
            parameters={
                "train_months": "2026-01..2026-06",
                "test_months": "2026-07..2026-12",
                "no_posthoc_threshold_widening": True,
            },
            outputs={
                "selected_filter_seeds": str(output_dir / "selected_filter_seeds.csv"),
                "families": str(output_dir / "precommitted_composite_signal_families.csv"),
                "validation_gates": str(output_dir / "precommitted_validation_gates.csv"),
                "acceptance_summary": str(output_dir / "composite_signal_precommit_acceptance_summary.csv"),
                "report": str(output_dir / "phase86_composite_signal_precommit_report.md"),
                "manifest": str(output_dir / "phase86_composite_signal_precommit_manifest.json"),
            },
            random_seed="none_deterministic_precommit_contract",
            scenario_ids="phase86_phase85_cost_budget_filter_seeds",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase83_source_event_ordinal_alignment",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase86_composite_signal_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Precommit next composite signal-family replay.")
    parser.add_argument("--phase85-dir", type=Path, default=DEFAULT_PHASE85_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase86(args.phase85_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
