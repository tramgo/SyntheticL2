from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.phase12_execution_simulator import EXECUTION_PROFILES, _zerodha_order_formula_charges
from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


FEATURE_THESES = [
    ("F01_momentum_follow", "momentum_3_event", 1, "follow recent event momentum"),
    ("F02_momentum_fade", "momentum_3_event", -1, "fade recent event momentum"),
    ("F03_mlofi_follow", "mlofi_qty_event", 1, "follow multi-level order-flow imbalance"),
    ("F04_mlofi_fade", "mlofi_qty_event", -1, "fade multi-level order-flow imbalance"),
    ("F05_microprice_follow", "microprice_dev", 1, "follow microprice deviation"),
    ("F06_microprice_fade", "microprice_dev", -1, "fade microprice deviation"),
    ("F07_l1_imbalance_follow", "l1_imbalance", 1, "follow level-1 queue imbalance"),
    ("F08_l1_imbalance_fade", "l1_imbalance", -1, "fade level-1 queue imbalance"),
    ("F09_l5_imbalance_follow", "l5_imbalance", 1, "follow level-5 queue imbalance"),
    ("F10_l5_imbalance_fade", "l5_imbalance", -1, "fade level-5 queue imbalance"),
]

FORWARD_HORIZON_EVENTS = [1, 3, 6, 12]
ABS_THRESHOLD_QUANTILES = [0.90, 0.95, 0.98]
SPREAD_QUANTILES = [0.50, 0.75]
MIN_SIGNALS_FOR_REPLAY_CANDIDATE = 5_000
MIN_PRECISION_LIFT_FOR_REPLAY_CANDIDATE = 1.25


def load_events(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    columns = [
        "annual_event_id",
        "feed_profile",
        "synthetic_year_day",
        "synthetic_trade_date",
        "symbol",
        "regime_code",
        "mid_price",
        "next_mid_price",
        "tick_size",
        "spread_ticks",
        "event_intensity_proxy",
        "is_market_shock_day",
        "is_duplicate",
        "is_disconnect_gap",
        "is_out_of_order_injected",
        "l1_imbalance",
        "l5_imbalance",
        "momentum_3_event",
        "local_volatility_6_event",
        "mlofi_qty_event",
        "microprice_dev",
        "next_is_bad_feed",
    ]
    events = pq.read_table(path, columns=columns).to_pandas()
    return events.sort_values(["feed_profile", "synthetic_year_day", "symbol", "annual_event_id"], kind="mergesort").reset_index(drop=True)


def retail_cost_return(events: pd.DataFrame) -> pd.Series:
    retail = next(profile for profile in EXECUTION_PROFILES if profile["execution_profile"] == "retail_marketable_default")
    spread = ((events["spread_ticks"].clip(lower=1).astype(float) * events["tick_size"].astype(float)) / 2.0) / events["mid_price"].astype(float)
    slippage = (float(retail["fixed_slippage_ticks"]) * events["tick_size"].astype(float)) / events["mid_price"].astype(float)
    impact = float(retail["impact_bps"]) / 10_000.0
    charge_frame = events[["symbol", "mid_price", "next_mid_price"]].copy()
    charge_frame["next_mid_price"] = charge_frame["next_mid_price"].fillna(charge_frame["mid_price"])
    charge_frame["side"] = 1
    charges = _zerodha_order_formula_charges(
        charge_frame,
        order_notional_inr=float(retail.get("order_notional_inr", 100_000.0)),
        apply_charges=True,
    )
    return spread + slippage + impact + charges["zerodha_charge_return"].astype(float)


def add_forward_labels(events: pd.DataFrame) -> pd.DataFrame:
    out = events.copy()
    groups = out.groupby(["feed_profile", "synthetic_year_day", "symbol"], sort=False)["mid_price"]
    out["retail_cost_hurdle_return"] = retail_cost_return(out)
    for horizon in FORWARD_HORIZON_EVENTS:
        future_mid = groups.shift(-horizon)
        out[f"forward_mid_return_{horizon}e"] = future_mid / out["mid_price"] - 1.0
        out[f"cost_clear_long_{horizon}e"] = out[f"forward_mid_return_{horizon}e"] > out["retail_cost_hurdle_return"]
        out[f"cost_clear_short_{horizon}e"] = -out[f"forward_mid_return_{horizon}e"] > out["retail_cost_hurdle_return"]
        out[f"any_cost_clear_edge_{horizon}e"] = out[f"cost_clear_long_{horizon}e"] | out[f"cost_clear_short_{horizon}e"]
    return out


def build_label_catalog(events: pd.DataFrame) -> pd.DataFrame:
    rows = []
    spread_limits = {q: float(events["spread_ticks"].quantile(q)) for q in SPREAD_QUANTILES}
    for thesis_id, feature_column, direction_multiplier, thesis in FEATURE_THESES:
        abs_values = events[feature_column].astype(float).abs().replace([np.inf, -np.inf], np.nan).dropna()
        for threshold_q in ABS_THRESHOLD_QUANTILES:
            threshold_value = float(abs_values.quantile(threshold_q)) if len(abs_values) else 0.0
            for spread_q, spread_limit in spread_limits.items():
                for horizon in FORWARD_HORIZON_EVENTS:
                    rows.append(
                        {
                            "label_candidate_id": f"{thesis_id}_q{int(threshold_q * 100)}_sp{int(spread_q * 100)}_{horizon}e",
                            "thesis_id": thesis_id,
                            "feature_column": feature_column,
                            "direction_multiplier": int(direction_multiplier),
                            "thesis": thesis,
                            "abs_threshold_quantile": float(threshold_q),
                            "abs_threshold_value": threshold_value,
                            "spread_quantile": float(spread_q),
                            "spread_tick_limit": spread_limit,
                            "forward_horizon_events": int(horizon),
                            "label_scope": "native_full_year_forward_edge_label_mining_not_acceptance",
                        }
                    )
    return pd.DataFrame(rows)


def evaluate_candidate(events: pd.DataFrame, candidate: dict[str, object]) -> dict[str, object]:
    feature = events[str(candidate["feature_column"])].astype(float)
    signal_side = np.sign(feature) * int(candidate["direction_multiplier"])
    clean_feed = ~(
        events["is_duplicate"].astype(bool)
        | events["is_disconnect_gap"].astype(bool)
        | events["is_out_of_order_injected"].astype(bool)
        | events["next_is_bad_feed"].astype(bool)
    )
    tradable = (
        clean_feed
        & events["mid_price"].notna()
        & feature.notna()
        & (feature.abs() >= float(candidate["abs_threshold_value"]))
        & (events["spread_ticks"].astype(float) <= float(candidate["spread_tick_limit"]))
    )
    signal = pd.Series(signal_side, index=events.index).where(tradable, 0).fillna(0).astype("int8")
    horizon = int(candidate["forward_horizon_events"])
    forward = events[f"forward_mid_return_{horizon}e"].astype(float)
    valid = signal.ne(0) & forward.notna()
    baseline_valid = clean_feed & forward.notna() & (events["spread_ticks"].astype(float) <= float(candidate["spread_tick_limit"]))
    if not bool(valid.any()):
        baseline_rate = float(events.loc[baseline_valid, f"any_cost_clear_edge_{horizon}e"].mean()) if bool(baseline_valid.any()) else 0.0
        return {
            **candidate,
            "signals": 0,
            "baseline_observations": int(baseline_valid.sum()),
            "baseline_any_edge_rate": baseline_rate,
            "directional_precision": 0.0,
            "precision_lift_vs_baseline": 0.0,
            "mean_directional_forward_return": 0.0,
            "mean_retail_cost_hurdle_return": 0.0,
            "mean_net_edge_return": 0.0,
            "median_net_edge_return": 0.0,
            "annual_positive_label_days": 0,
            "candidate_for_replay": False,
        }
    signed_forward = signal.loc[valid].astype(float) * forward.loc[valid]
    hurdle = events.loc[valid, "retail_cost_hurdle_return"].astype(float)
    net_edge = signed_forward - hurdle
    clear = net_edge > 0.0
    baseline_rate = float(events.loc[baseline_valid, f"any_cost_clear_edge_{horizon}e"].mean()) if bool(baseline_valid.any()) else 0.0
    daily = pd.DataFrame(
        {
            "synthetic_year_day": events.loc[valid, "synthetic_year_day"].to_numpy(),
            "net_edge": net_edge.to_numpy(),
            "clear": clear.to_numpy(),
        }
    )
    daily_summary = daily.groupby("synthetic_year_day", sort=True).agg(day_mean_net_edge=("net_edge", "mean"), day_clear_rate=("clear", "mean"))
    precision = float(clear.mean())
    lift = float(precision / baseline_rate) if baseline_rate > 0 else 0.0
    mean_net = float(net_edge.mean())
    candidate_for_replay = (
        int(valid.sum()) >= MIN_SIGNALS_FOR_REPLAY_CANDIDATE
        and precision >= baseline_rate
        and lift >= MIN_PRECISION_LIFT_FOR_REPLAY_CANDIDATE
        and mean_net > 0.0
    )
    return {
        **candidate,
        "signals": int(valid.sum()),
        "baseline_observations": int(baseline_valid.sum()),
        "baseline_any_edge_rate": baseline_rate,
        "directional_precision": precision,
        "precision_lift_vs_baseline": lift,
        "mean_directional_forward_return": float(signed_forward.mean()),
        "mean_retail_cost_hurdle_return": float(hurdle.mean()),
        "mean_net_edge_return": mean_net,
        "median_net_edge_return": float(net_edge.median()),
        "annual_positive_label_days": int((daily_summary["day_mean_net_edge"] > 0).sum()),
        "candidate_for_replay": bool(candidate_for_replay),
    }


def evaluate_catalog(events: pd.DataFrame, catalog: pd.DataFrame) -> pd.DataFrame:
    rows = [evaluate_candidate(events, candidate) for candidate in catalog.to_dict("records")]
    return pd.DataFrame(rows).sort_values(
        ["candidate_for_replay", "mean_net_edge_return", "precision_lift_vs_baseline", "signals"],
        ascending=[False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_thesis_rollup(results: pd.DataFrame) -> pd.DataFrame:
    return (
        results.groupby(["thesis_id", "feature_column"], sort=True)
        .agg(
            candidate_rows=("candidate_for_replay", "sum"),
            tested_rows=("label_candidate_id", "count"),
            total_signals=("signals", "sum"),
            best_directional_precision=("directional_precision", "max"),
            best_precision_lift=("precision_lift_vs_baseline", "max"),
            best_mean_net_edge_return=("mean_net_edge_return", "max"),
            best_positive_label_days=("annual_positive_label_days", "max"),
        )
        .reset_index()
        .sort_values(["candidate_rows", "best_mean_net_edge_return", "best_precision_lift"], ascending=[False, False, False], kind="mergesort")
    )


def build_summary(events: pd.DataFrame, catalog: pd.DataFrame, results: pd.DataFrame) -> pd.DataFrame:
    candidate_rows = results[results["candidate_for_replay"]]
    rows = [
        ("phase44_input_event_rows", int(len(events)), "Native full-year L2 event rows labelled"),
        ("phase44_label_candidates_registered", int(len(catalog)), "Forward-edge feature/threshold/horizon candidates registered"),
        ("phase44_label_candidate_rows_evaluated", int(len(results)), "Candidate rows evaluated"),
        ("phase44_replay_candidate_rows", int(len(candidate_rows)), "Rows that clear the pre-replay label edge screen"),
        ("phase44_total_signals_evaluated", int(results["signals"].sum()), "Total feature-threshold signals evaluated"),
        ("phase44_best_mean_net_edge_return", float(results["mean_net_edge_return"].max()) if len(results) else 0.0, "Best mean signed forward return after retail hurdle"),
        ("phase44_best_precision_lift_vs_baseline", float(results["precision_lift_vs_baseline"].max()) if len(results) else 0.0, "Best directional precision lift against baseline any-edge rate"),
        ("phase44_best_directional_precision", float(results["directional_precision"].max()) if len(results) else 0.0, "Best directional cost-clear precision"),
        ("phase44_synthetic_full_year_acceptance_ready", 0, "Forward label mining is pre-replay redesign evidence, not acceptance"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase 44 Native Full-Year Forward Edge Label Mining",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This phase mines the Phase 42 native 252-day synthetic L2 event stream for forward labels that can clear a retail Zerodha-style cost hurdle.",
        "It is a redesign pre-replay screen: it can nominate label/signal candidates for later replay, but it is not strategy acceptance evidence.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase44_native_full_year_forward_edge_label_mining_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase44(events_path: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    events = add_forward_labels(load_events(events_path))
    catalog = build_label_catalog(events)
    results = evaluate_catalog(events, catalog)
    rollup = build_thesis_rollup(results)
    summary = build_summary(events, catalog, results)
    catalog.to_csv(output_dir / "forward_edge_label_candidate_catalog.csv", index=False)
    results.to_csv(output_dir / "forward_edge_label_mining_results.csv", index=False)
    rollup.to_csv(output_dir / "forward_edge_label_thesis_rollup.csv", index=False)
    summary.to_csv(output_dir / "forward_edge_label_mining_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Summary": summary,
            "Replay Candidate Rows": results[results["candidate_for_replay"]].head(80),
            "Top Label Mining Results": results.head(80),
            "Thesis Rollup": rollup,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase44_native_full_year_forward_edge_label_mining_not_acceptance",
        "label_candidates_registered": int(len(catalog)),
        "label_candidate_rows_evaluated": int(len(results)),
        "replay_candidate_rows": int(results["candidate_for_replay"].sum()),
        "synthetic_full_year_acceptance_ready": 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase44",
            generated_utc=generated_utc,
            inputs={"native_full_year_l2_event_state": str(events_path)},
            parameters={
                "feature_theses": [row[0] for row in FEATURE_THESES],
                "forward_horizon_events": FORWARD_HORIZON_EVENTS,
                "abs_threshold_quantiles": ABS_THRESHOLD_QUANTILES,
                "spread_quantiles": SPREAD_QUANTILES,
                "minimum_signals_for_replay_candidate": MIN_SIGNALS_FOR_REPLAY_CANDIDATE,
                "minimum_precision_lift_for_replay_candidate": MIN_PRECISION_LIFT_FOR_REPLAY_CANDIDATE,
                "acceptance_boundary": "synthetic_only_pre_replay_redesign_evidence_not_acceptance",
            },
            outputs={
                "summary": str(output_dir / "forward_edge_label_mining_summary.csv"),
                "candidate_catalog": str(output_dir / "forward_edge_label_candidate_catalog.csv"),
                "results": str(output_dir / "forward_edge_label_mining_results.csv"),
                "thesis_rollup": str(output_dir / "forward_edge_label_thesis_rollup.csv"),
                "report": str(output_dir / "phase44_native_full_year_forward_edge_label_mining_report.md"),
                "manifest": str(output_dir / "phase44_native_full_year_forward_edge_label_mining_manifest.json"),
            },
            random_seed="none_deterministic_native_full_year_forward_label_mining",
            scenario_ids="phase42_native_252_day_l2_event_state_forward_edge_labels",
            cost_model_version="phase12_zerodha_equity_intraday_cost_model_retail_hurdle",
            latency_model_version="phase12_retail_marketable_default_pre_replay_hurdle",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase44_native_full_year_forward_edge_label_mining_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run native full-year forward-edge label mining.")
    parser.add_argument("--events", type=Path, default=Path("outputs/phase42/native_full_year_l2_event_state.parquet"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase44"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase44(args.events, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()
