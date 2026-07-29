from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, metric_value, read_csv
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE254_DIR = Path("outputs/phase254")
DEFAULT_OUTPUT_DIR = Path("outputs/phase255")
DEFAULT_INPUT_PARQUET = DEFAULT_PHASE254_DIR / "phase254_richer_raw_top5_depth_event_bars.parquet"

FEATURE_COLUMNS = [
    "avg_spread_bps",
    "bar_return_bps",
    "avg_cum_top5_qty_imbalance",
    "avg_depth_beyond_l1_qty_imbalance",
    "avg_level_weighted_depth_imbalance",
    "avg_depth_slope_bid",
    "avg_depth_slope_ask",
    "avg_depth_convexity_bid",
    "avg_depth_convexity_ask",
    "avg_order_count_imbalance_l1_l5",
    "avg_qty_per_order_bid_l1_l5",
    "avg_qty_per_order_ask_l1_l5",
    "top5_qty_churn_sum",
    "top5_order_churn_sum",
    "depth_replenishment_pressure",
    "depth_withdrawal_pressure",
    "l1_price_shift_abs_sum",
    "volume_increment_sum",
]

FULL_DEPTH_COLUMNS = [
    "avg_depth_beyond_l1_qty_imbalance",
    "avg_level_weighted_depth_imbalance",
    "avg_depth_slope_bid",
    "avg_depth_slope_ask",
    "avg_depth_convexity_bid",
    "avg_depth_convexity_ask",
    "avg_order_count_imbalance_l1_l5",
    "top5_qty_churn_sum",
    "top5_order_churn_sum",
    "depth_replenishment_pressure",
    "depth_withdrawal_pressure",
]

LABEL_COLUMNS = ["future_return_h3", "future_return_h6", "future_return_h10"]


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def load_event_bars(input_parquet: Path) -> pd.DataFrame:
    if not input_parquet.exists():
        raise FileNotFoundError(f"Missing Phase254 richer event bars: {input_parquet}")
    con = duckdb.connect()
    try:
        return con.execute(f"select * from read_parquet('{input_parquet.as_posix()}')").fetchdf()
    finally:
        con.close()


def summarize_feature_quality(frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    total = len(frame)
    for column in FEATURE_COLUMNS:
        series = pd.to_numeric(frame[column], errors="coerce") if column in frame.columns else pd.Series(dtype="float64")
        non_null = int(series.notna().sum())
        finite = int(series.replace([float("inf"), float("-inf")], pd.NA).notna().sum())
        cleaned = series.replace([float("inf"), float("-inf")], pd.NA).dropna()
        std = safe_float(cleaned.std(ddof=0), 0.0) if not cleaned.empty else 0.0
        unique = int(cleaned.nunique()) if not cleaned.empty else 0
        missing_pct = 1.0 - (non_null / total) if total else 1.0
        finite_pct = finite / total if total else 0.0
        healthy = missing_pct <= 0.01 and finite_pct >= 0.99 and std > 1e-9 and unique >= 5
        rows.append(
            {
                "feature": column,
                "is_full_depth_feature": int(column in FULL_DEPTH_COLUMNS),
                "rows": total,
                "non_null_rows": non_null,
                "missing_pct": missing_pct,
                "finite_pct": finite_pct,
                "unique_values": unique,
                "std": std,
                "mean": safe_float(cleaned.mean(), 0.0) if not cleaned.empty else 0.0,
                "median": safe_float(cleaned.median(), 0.0) if not cleaned.empty else 0.0,
                "p01": safe_float(cleaned.quantile(0.01), 0.0) if not cleaned.empty else 0.0,
                "p99": safe_float(cleaned.quantile(0.99), 0.0) if not cleaned.empty else 0.0,
                "healthy_for_search": int(healthy),
            }
        )
    return pd.DataFrame(rows)


def summarize_depth_contribution(frame: pd.DataFrame) -> pd.DataFrame:
    bid_share = pd.to_numeric(frame["avg_cum_buy_qty_l2_l5"], errors="coerce") / pd.to_numeric(
        frame["avg_cum_buy_qty_l1_l5"], errors="coerce"
    ).replace(0, pd.NA)
    ask_share = pd.to_numeric(frame["avg_cum_sell_qty_l2_l5"], errors="coerce") / pd.to_numeric(
        frame["avg_cum_sell_qty_l1_l5"], errors="coerce"
    ).replace(0, pd.NA)
    top5_imb = pd.to_numeric(frame["avg_cum_top5_qty_imbalance"], errors="coerce")
    beyond_imb = pd.to_numeric(frame["avg_depth_beyond_l1_qty_imbalance"], errors="coerce")
    corr = safe_float(top5_imb.corr(beyond_imb), 0.0)
    rows = [
        ("median_bid_depth_share_from_levels_2_5", safe_float(bid_share.median(), 0.0), "Median share of visible bid quantity contributed by levels 2-5"),
        ("median_ask_depth_share_from_levels_2_5", safe_float(ask_share.median(), 0.0), "Median share of visible ask quantity contributed by levels 2-5"),
        ("p10_bid_depth_share_from_levels_2_5", safe_float(bid_share.quantile(0.10), 0.0), "10th percentile bid quantity share from levels 2-5"),
        ("p10_ask_depth_share_from_levels_2_5", safe_float(ask_share.quantile(0.10), 0.0), "10th percentile ask quantity share from levels 2-5"),
        ("top5_vs_beyond_l1_imbalance_corr", corr, "Correlation between cumulative top-five imbalance and levels 2-5 imbalance"),
        ("beyond_l1_imbalance_std", safe_float(beyond_imb.std(ddof=0), 0.0), "Variation of levels 2-5 imbalance"),
        ("top5_imbalance_std", safe_float(top5_imb.std(ddof=0), 0.0), "Variation of cumulative top-five imbalance"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def summarize_label_association(frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for feature in FEATURE_COLUMNS:
        x = pd.to_numeric(frame[feature], errors="coerce")
        for label in LABEL_COLUMNS:
            y = pd.to_numeric(frame[label], errors="coerce")
            pair = pd.DataFrame({"x": x, "y": y}).replace([float("inf"), float("-inf")], pd.NA).dropna()
            if len(pair) < 30 or pair["x"].nunique() < 5 or pair["y"].nunique() < 5:
                pearson = 0.0
                spearman = 0.0
                top_minus_bottom_bps = 0.0
            else:
                pearson = safe_float(pair["x"].corr(pair["y"], method="pearson"), 0.0)
                spearman = safe_float(pair["x"].rank(method="average").corr(pair["y"].rank(method="average")), 0.0)
                ranked = pair.assign(bucket=pd.qcut(pair["x"].rank(method="first"), 5, labels=False, duplicates="drop"))
                low = ranked.loc[ranked["bucket"].eq(ranked["bucket"].min()), "y"].mean()
                high = ranked.loc[ranked["bucket"].eq(ranked["bucket"].max()), "y"].mean()
                top_minus_bottom_bps = safe_float((high - low) * 10000.0, 0.0)
            rows.append(
                {
                    "feature": feature,
                    "is_full_depth_feature": int(feature in FULL_DEPTH_COLUMNS),
                    "label": label,
                    "usable_pair_rows": len(pair),
                    "pearson_ic": pearson,
                    "spearman_ic": spearman,
                    "abs_spearman_ic": abs(spearman),
                    "top_minus_bottom_future_return_bps": top_minus_bottom_bps,
                }
            )
    return pd.DataFrame(rows).sort_values(["abs_spearman_ic", "usable_pair_rows"], ascending=[False, False])


def build_gate_evaluation(
    phase254_dir: Path,
    stats: dict[str, Any],
    feature_quality: pd.DataFrame,
    depth_contribution: pd.DataFrame,
    label_association: pd.DataFrame,
) -> pd.DataFrame:
    phase254_next = str(metric_value(phase254_dir / "phase254_acceptance_summary.csv", "phase254_next_best_action", ""))
    healthy_features = int(feature_quality["healthy_for_search"].sum()) if not feature_quality.empty else 0
    healthy_full_depth = int(
        feature_quality.loc[feature_quality["is_full_depth_feature"].eq(1), "healthy_for_search"].sum()
    ) if not feature_quality.empty else 0
    median_bid_share = safe_float(depth_contribution.loc[depth_contribution["metric"].eq("median_bid_depth_share_from_levels_2_5"), "value"].iloc[0], 0.0)
    median_ask_share = safe_float(depth_contribution.loc[depth_contribution["metric"].eq("median_ask_depth_share_from_levels_2_5"), "value"].iloc[0], 0.0)
    beyond_std = safe_float(depth_contribution.loc[depth_contribution["metric"].eq("beyond_l1_imbalance_std"), "value"].iloc[0], 0.0)
    corr = safe_float(depth_contribution.loc[depth_contribution["metric"].eq("top5_vs_beyond_l1_imbalance_corr"), "value"].iloc[0], 0.0)
    max_abs_full_depth_ic = safe_float(
        label_association.loc[label_association["is_full_depth_feature"].eq(1), "abs_spearman_ic"].max(), 0.0
    ) if not label_association.empty else 0.0
    rows = [
        ("P255_PHASE254_WORK_ORDER_PRESENT", "run_phase255_richer_raw_depth_feature_quality_interpretation" in phase254_next, phase254_next, "Phase254 next action targets Phase255", "hard"),
        ("P255_INPUT_EVENT_BARS_PRESENT", as_int(stats.get("event_bar_rows", 0)) >= 1000, stats.get("event_bar_rows", 0), ">=1000 richer raw-depth event bars", "hard"),
        ("P255_SYMBOL_BREADTH_RETAINED", as_int(stats.get("symbols", 0)) >= 20, stats.get("symbols", 0), ">=20 symbols", "hard"),
        ("P255_HEALTHY_FEATURE_COUNT", healthy_features >= 12, healthy_features, ">=12 healthy features", "hard"),
        ("P255_HEALTHY_FULL_DEPTH_FEATURE_COUNT", healthy_full_depth >= 8, healthy_full_depth, ">=8 healthy full-depth features", "hard"),
        ("P255_LEVELS_2_5_DEPTH_SHARE_MATERIAL", median_bid_share >= 0.25 and median_ask_share >= 0.25, f"bid={median_bid_share:.4f};ask={median_ask_share:.4f}", "median levels 2-5 share >=25% on both sides", "hard"),
        ("P255_BEYOND_L1_IMBALANCE_NOT_DEGENERATE", beyond_std > 1e-6 and abs(corr) < 0.995, f"std={beyond_std:.6g};corr={corr:.6g}", "levels 2-5 imbalance varies and is not identical to top-five imbalance", "hard"),
        ("P255_FULL_DEPTH_LABEL_ASSOCIATION_VISIBLE", max_abs_full_depth_ic >= 0.02, f"{max_abs_full_depth_ic:.6f}", ">=0.02 absolute Spearman IC for at least one full-depth feature/horizon", "hard"),
        ("P255_NO_REPLAY_PROMOTION_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase255 Richer Raw Top-five Depth Feature-quality Interpretation",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase255 audits the Phase254 compact event-bar product before any strategy search consumes it.",
        "It checks feature health, levels 2-5 contribution inside Zerodha's top-five market-by-price book, and simple future-return label association.",
        "It does not execute replay, promote a strategy, open paper/live acceptance or claim profitability.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    input_parquet: Path = DEFAULT_INPUT_PARQUET,
    phase254_dir: Path = DEFAULT_PHASE254_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    frame = load_event_bars(input_parquet)
    stats = {
        "event_bar_rows": len(frame),
        "symbols": int(frame["symbol"].nunique()) if "symbol" in frame.columns else 0,
        "trade_dates": int(frame["trade_date"].nunique()) if "trade_date" in frame.columns else 0,
        "source_tick_rows": int(pd.to_numeric(frame.get("source_tick_count", pd.Series(dtype="float64")), errors="coerce").sum()),
    }
    feature_quality = summarize_feature_quality(frame)
    depth_contribution = summarize_depth_contribution(frame)
    label_association = summarize_label_association(frame)
    gates = build_gate_evaluation(phase254_dir, stats, feature_quality, depth_contribution, label_association)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    healthy_features = int(feature_quality["healthy_for_search"].sum()) if not feature_quality.empty else 0
    healthy_full_depth = int(feature_quality.loc[feature_quality["is_full_depth_feature"].eq(1), "healthy_for_search"].sum()) if not feature_quality.empty else 0
    max_abs_ic = safe_float(label_association["abs_spearman_ic"].max(), 0.0) if not label_association.empty else 0.0
    max_abs_full_depth_ic = safe_float(
        label_association.loc[label_association["is_full_depth_feature"].eq(1), "abs_spearman_ic"].max(), 0.0
    ) if not label_association.empty else 0.0
    top_full_depth = label_association.loc[label_association["is_full_depth_feature"].eq(1)].head(1)
    top_feature = str(top_full_depth["feature"].iloc[0]) if not top_full_depth.empty else ""
    top_label = str(top_full_depth["label"].iloc[0]) if not top_full_depth.empty else ""
    strategy_search_allowed_next = int(hard_pass == len(hard))
    next_action = (
        "run_phase256_richer_raw_top5_depth_cost_aware_strategy_search_training_only_no_paper_live"
        if strategy_search_allowed_next
        else "repair_phase254_or_phase255_richer_raw_depth_feature_quality_before_strategy_search"
    )
    acceptance = pd.DataFrame(
        [
            ("phase255_feature_quality_interpretation_complete", 1, "Phase255 richer raw-depth feature quality interpretation completed"),
            ("phase255_input_event_bar_rows", stats["event_bar_rows"], "Phase254 richer raw-depth event bars audited"),
            ("phase255_trade_dates", stats["trade_dates"], "Trade dates represented"),
            ("phase255_symbols", stats["symbols"], "Symbols represented"),
            ("phase255_source_tick_rows", stats["source_tick_rows"], "Source raw ticks represented by audited event bars"),
            ("phase255_feature_rows", len(feature_quality), "Features audited"),
            ("phase255_full_depth_feature_rows", int(feature_quality["is_full_depth_feature"].sum()), "Audited features using levels 2-5/top-five depth shape"),
            ("phase255_healthy_feature_rows", healthy_features, "Healthy features by missingness/finite/variation gate"),
            ("phase255_healthy_full_depth_feature_rows", healthy_full_depth, "Healthy full-depth features"),
            ("phase255_max_abs_spearman_ic", max_abs_ic, "Maximum absolute Spearman IC across audited feature/label pairs"),
            ("phase255_max_abs_full_depth_spearman_ic", max_abs_full_depth_ic, "Maximum absolute Spearman IC for full-depth features"),
            ("phase255_top_full_depth_feature", top_feature, "Top full-depth feature by absolute Spearman IC"),
            ("phase255_top_full_depth_label", top_label, "Top full-depth horizon label by absolute Spearman IC"),
            ("phase255_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase255_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase255_strategy_search_allowed_next", strategy_search_allowed_next, "Whether Phase256 training-only cost-aware strategy search is allowed next"),
            ("phase255_replay_execution_allowed_now", 0, "No replay execution in Phase255"),
            ("phase255_strategy_promotion_allowed", 0, "No strategy promotion from Phase255"),
            ("phase255_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase255"),
            ("phase255_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase255"),
            ("phase255_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    feature_quality.to_csv(output_dir / "phase255_feature_quality_audit.csv", index=False)
    depth_contribution.to_csv(output_dir / "phase255_full_depth_contribution_summary.csv", index=False)
    label_association.to_csv(output_dir / "phase255_feature_label_association.csv", index=False)
    gates.to_csv(output_dir / "phase255_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase255_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase255_richer_raw_depth_feature_quality_interpretation_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Full Depth Contribution Summary": depth_contribution,
            "Feature Quality Audit": feature_quality,
            "Top Feature Label Associations": label_association.head(30),
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase255_richer_raw_depth_feature_quality_interpretation",
        **reproducibility_fields(
            artifact_id="phase255",
            generated_utc=generated_utc,
            inputs={"input_parquet": str(input_parquet), "phase254_dir": str(phase254_dir)},
            parameters={
                "feature_columns": FEATURE_COLUMNS,
                "full_depth_columns": FULL_DEPTH_COLUMNS,
                "label_columns": LABEL_COLUMNS,
                "strategy_search_allowed_next": strategy_search_allowed_next,
                "replay_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "feature_quality_audit": str(output_dir / "phase255_feature_quality_audit.csv"),
                "full_depth_contribution_summary": str(output_dir / "phase255_full_depth_contribution_summary.csv"),
                "feature_label_association": str(output_dir / "phase255_feature_label_association.csv"),
                "gate_evaluation": str(output_dir / "phase255_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase255_acceptance_summary.csv"),
                "report": str(output_dir / "phase255_richer_raw_depth_feature_quality_interpretation_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase255_no_replay_feature_quality_interpretation",
        ),
    }
    (output_dir / "phase255_richer_raw_depth_feature_quality_interpretation_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase255 richer raw top-five depth feature quality interpretation.")
    parser.add_argument("--input-parquet", type=Path, default=DEFAULT_INPUT_PARQUET)
    parser.add_argument("--phase254-dir", type=Path, default=DEFAULT_PHASE254_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(input_parquet=args.input_parquet, phase254_dir=args.phase254_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
