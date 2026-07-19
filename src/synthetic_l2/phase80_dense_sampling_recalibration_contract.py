from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase61_lower_frequency_candidate_sweep import _safe_path
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase80")
DEFAULT_COMPACT_ROOT = Path("raw_synthetic_l2_full_year_compact_monthly")
DEFAULT_PHASE79_DIR = Path("outputs/phase79")


def entropy(counts: pd.Series) -> float:
    values = counts.astype(float)
    total = float(values.sum())
    if total <= 0:
        return 0.0
    probs = values[values > 0] / total
    return float(-(probs * np.log2(probs)).sum())


def compact_monthly_diversity(compact_root: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    pattern = (compact_root / "**" / "*.parquet").as_posix().replace("'", "''")
    con = duckdb.connect()
    try:
        detail = con.execute(
            f"""
            select
                trade_month,
                trade_date,
                regime_code,
                feed_profile,
                count(*)::bigint as row_count,
                sum(case when coalesce(is_market_shock_day, false) then 1 else 0 end)::bigint as market_shock_rows,
                sum(case when coalesce(is_symbol_shock, false) then 1 else 0 end)::bigint as symbol_shock_rows
            from read_parquet('{pattern}', union_by_name=true)
            group by trade_month, trade_date, regime_code, feed_profile
            order by trade_month, trade_date, regime_code, feed_profile
            """
        ).fetchdf()
    finally:
        con.close()
    rows: list[dict[str, Any]] = []
    for month, group in detail.groupby("trade_month", sort=True):
        regime_counts = group.groupby("regime_code", sort=True)["row_count"].sum()
        feed_counts = group.groupby("feed_profile", sort=True)["row_count"].sum()
        rows.append(
            {
                "trade_month": month,
                "compact_rows": int(group["row_count"].sum()),
                "compact_days": int(group["trade_date"].nunique()),
                "compact_regime_codes": int(regime_counts.shape[0]),
                "compact_regime_entropy_bits": entropy(regime_counts),
                "compact_feed_profiles": int(feed_counts.shape[0]),
                "compact_feed_entropy_bits": entropy(feed_counts),
                "compact_market_shock_rows": int(group["market_shock_rows"].sum()),
                "compact_symbol_shock_rows": int(group["symbol_shock_rows"].sum()),
            }
        )
    return pd.DataFrame(rows), detail


def compare_dense_prefix_to_compact(compact: pd.DataFrame, phase79_monthly: pd.DataFrame) -> pd.DataFrame:
    dense = phase79_monthly.rename(
        columns={
            "regime_codes": "dense_prefix_regime_codes",
            "regime_entropy_bits": "dense_prefix_regime_entropy_bits",
            "feed_profiles": "dense_prefix_feed_profiles",
            "feed_profile_entropy_bits": "dense_prefix_feed_entropy_bits",
            "market_shock_symbols": "dense_prefix_market_shock_symbols",
            "symbol_shock_symbols": "dense_prefix_symbol_shock_symbols",
        }
    )
    merged = compact.merge(
        dense[
            [
                "trade_month",
                "dense_prefix_regime_codes",
                "dense_prefix_regime_entropy_bits",
                "dense_prefix_feed_profiles",
                "dense_prefix_feed_entropy_bits",
                "dense_prefix_market_shock_symbols",
                "dense_prefix_symbol_shock_symbols",
            ]
        ],
        on="trade_month",
        how="left",
    )
    merged["regime_code_capture_fraction"] = merged["dense_prefix_regime_codes"] / merged["compact_regime_codes"].replace(0, np.nan)
    merged["regime_entropy_capture_fraction"] = merged["dense_prefix_regime_entropy_bits"] / merged["compact_regime_entropy_bits"].replace(0, np.nan)
    merged["feed_profile_capture_fraction"] = merged["dense_prefix_feed_profiles"] / merged["compact_feed_profiles"].replace(0, np.nan)
    merged["dense_prefix_sampling_bias"] = (
        merged["regime_code_capture_fraction"].lt(0.50)
        | merged["regime_entropy_capture_fraction"].fillna(0.0).lt(0.25)
        | merged["feed_profile_capture_fraction"].lt(0.75)
    )
    return merged


def patch_contract(comparison: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "contract_id": "P80_STRATIFIED_DENSE_REPLAY_WINDOW",
                "patch_target": "strategy_replay_and_generator_audit_readers",
                "required_change": "Replace local_sequence_id prefix sampling with stratified source-day/regime/feed-profile sampling or explicit full-month source-day windows.",
                "evidence": f"{int(comparison['dense_prefix_sampling_bias'].sum())}/{int(len(comparison))} months show dense-prefix scenario capture bias.",
                "acceptance_gate": "For every replay validation month, sampled windows must capture at least 50% of compact regime codes, 50% of compact regime entropy, and 75% of compact feed profiles unless the test explicitly targets a single regime.",
            },
            {
                "contract_id": "P80_SOURCE_DAY_BALANCED_ACCEPTANCE",
                "patch_target": "future_phase79_and_strategy_falsification_runs",
                "required_change": "Report compact-source diversity and dense-window capture side by side before any profitability result can be interpreted.",
                "evidence": "Phase79 failed because dense-prefix windows saw one regime per month while compact months contain 7-14 regimes.",
                "acceptance_gate": "Profitability reports must include source-day/regime coverage evidence and mark results invalid if coverage gate fails.",
            },
            {
                "contract_id": "P80_NO_MORE_PREFIX_ONLY_FALSIFICATION",
                "patch_target": "phase77_like_disjoint_retests",
                "required_change": "Retain Phase77 as a falsification of the prefix/common-overlap HDFCBANK pocket, but do not generalize it to full generator diversity without stratified replay.",
                "evidence": "Phase77 used common-overlap prefix windows inherited from Phase75/76; Phase80 shows those windows are scenario-narrow.",
                "acceptance_gate": "New disjoint retests must be rerun with stratified windows before broad family-level conclusions are finalized.",
            },
        ]
    )


def summarize(compact: pd.DataFrame, comparison: pd.DataFrame) -> pd.DataFrame:
    compact_pass = bool(
        int(compact["compact_regime_codes"].min()) >= 4
        and float(compact["compact_regime_entropy_bits"].median()) >= 1.0
        and int(compact["compact_feed_profiles"].min()) >= 3
        and int((compact["compact_market_shock_rows"] > 0).sum()) >= 6
        and int((compact["compact_symbol_shock_rows"] > 0).sum()) >= 6
    )
    biased_months = int(comparison["dense_prefix_sampling_bias"].sum()) if not comparison.empty else 0
    dense_prefix_capture_pass = bool(biased_months == 0)
    return pd.DataFrame(
        [
            ("phase80_compact_months_audited", int(len(compact)), "Compact monthly source months audited"),
            ("phase80_compact_min_regime_codes", int(compact["compact_regime_codes"].min()), "Minimum compact regime codes per month"),
            ("phase80_compact_median_regime_entropy_bits", float(compact["compact_regime_entropy_bits"].median()), "Median compact regime entropy"),
            ("phase80_compact_min_feed_profiles", int(compact["compact_feed_profiles"].min()), "Minimum compact feed profiles per month"),
            ("phase80_compact_generator_diversity_pass", int(compact_pass), "1 means compact source generator diversity is acceptable"),
            ("phase80_dense_prefix_biased_months", biased_months, "Months where dense-prefix windows under-capture compact diversity"),
            ("phase80_dense_prefix_capture_pass", int(dense_prefix_capture_pass), "1 means dense-prefix scan windows capture compact diversity"),
            ("phase80_replay_sampling_recalibration_required", int(compact_pass and not dense_prefix_capture_pass), "1 means replay/audit sampling must be recalibrated before new mining"),
            ("phase80_recommend_next_action", "implement_stratified_dense_window_reader", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase80 Dense Sampling Recalibration Contract",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase80 reconciles the Phase79 dense-prefix diversity failure against the compact monthly source lake.",
        "It distinguishes a genuinely weak generator from a biased dense-prefix replay window.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase80_dense_sampling_recalibration_contract_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase80(compact_root: Path, phase79_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase79_monthly = pd.read_csv(phase79_dir / "monthly_scenario_diversity.csv")
    compact, compact_detail = compact_monthly_diversity(compact_root)
    comparison = compare_dense_prefix_to_compact(compact, phase79_monthly)
    contract = patch_contract(comparison)
    acceptance = summarize(compact, comparison)

    compact.to_csv(output_dir / "compact_monthly_scenario_diversity.csv", index=False)
    compact_detail.to_csv(output_dir / "compact_daily_scenario_detail.csv", index=False)
    comparison.to_csv(output_dir / "dense_prefix_vs_compact_diversity.csv", index=False)
    contract.to_csv(output_dir / "dense_sampling_recalibration_contract.csv", index=False)
    acceptance.to_csv(output_dir / "dense_sampling_recalibration_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Dense Prefix vs Compact Diversity": comparison,
            "Dense Sampling Recalibration Contract": contract,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase80_dense_sampling_recalibration_contract",
        "replay_sampling_recalibration_required": int(
            acceptance.loc[acceptance["metric"].eq("phase80_replay_sampling_recalibration_required"), "value"].iloc[0]
        ),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase80",
            generated_utc=generated_utc,
            inputs={
                "compact_monthly_raw_lake": str(compact_root),
                "phase79_monthly_scenario_diversity": str(phase79_dir / "monthly_scenario_diversity.csv"),
            },
            parameters={
                "bias_definition": "dense_prefix_captures_lt_50pct_regime_codes_or_lt_25pct_entropy_or_lt_75pct_feed_profiles",
                "contract_policy": "no_prefix_only_profitability_or_falsification_without_coverage_table",
            },
            outputs={
                "compact_monthly_diversity": str(output_dir / "compact_monthly_scenario_diversity.csv"),
                "comparison": str(output_dir / "dense_prefix_vs_compact_diversity.csv"),
                "contract": str(output_dir / "dense_sampling_recalibration_contract.csv"),
                "acceptance_summary": str(output_dir / "dense_sampling_recalibration_acceptance_summary.csv"),
                "report": str(output_dir / "phase80_dense_sampling_recalibration_contract_report.md"),
                "manifest": str(output_dir / "phase80_dense_sampling_recalibration_contract_manifest.json"),
            },
            random_seed="none_deterministic_sampling_contract",
            scenario_ids="phase80_dense_prefix_vs_compact_source_diversity",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_sampling_contract",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase80_dense_sampling_recalibration_contract_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create dense sampling recalibration contract from compact-vs-prefix diversity evidence.")
    parser.add_argument("--compact-root", type=Path, default=DEFAULT_COMPACT_ROOT)
    parser.add_argument("--phase79-dir", type=Path, default=DEFAULT_PHASE79_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase80(args.compact_root, args.phase79_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
