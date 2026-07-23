from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase133")
DEFAULT_PHASE6_DIR = Path("outputs/phase6")
DEFAULT_PHASE89_DIR = Path("outputs/phase89")
DEFAULT_PHASE131_DIR = Path("outputs/phase131")
DEFAULT_PHASE132_DIR = Path("outputs/phase132")
FORBIDDEN_OUTPUTS = "strategy_code;buy_sell_signal;order_arrival_stream;live_tagged_fill_model;pnl_replay;profitability_claim"
CONTRACT_VERSION = "phase133_retail_passive_visible_depth_fill_model_v1_2026_07_23"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
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


def build_latency_distribution() -> pd.DataFrame:
    rows = [
        ("p01", 25, "best_case_local_stack_but_not_zero_latency"),
        ("p05", 50, "lower_tail_retail_websocket_to_order_path"),
        ("p25", 90, "fast_retail_path"),
        ("p50", 175, "central_mass"),
        ("p75", 300, "central_mass_upper"),
        ("p90", 550, "fat_right_tail"),
        ("p95", 900, "fat_right_tail"),
        ("p99", 1750, "pathological_retail_network_or_app_delay"),
    ]
    return pd.DataFrame(rows, columns=["quantile", "latency_ms", "description"])


def build_cancel_intensity_inputs(feature_matrix: pd.DataFrame) -> pd.DataFrame:
    if feature_matrix.empty or "p131_mean_cancel_intensity_depth_levels_2_5" not in feature_matrix.columns:
        base = pd.DataFrame(
            [
                {
                    "depth_level": level,
                    "cancel_intensity_source": "fallback_no_phase132_matrix",
                    "cancel_intensity_mean": 0.0,
                    "cancel_intensity_p50": 0.0,
                    "cancel_intensity_p90": 0.0,
                    "cancel_intensity_multiplier": 1.0 + 0.05 * level,
                }
                for level in range(1, 6)
            ]
        )
        return base
    values = pd.to_numeric(feature_matrix["p131_mean_cancel_intensity_depth_levels_2_5"], errors="coerce").fillna(0.0)
    mean_cancel = float(values.mean())
    p50_cancel = float(values.quantile(0.50))
    p90_cancel = float(values.quantile(0.90))
    rows: list[dict[str, Any]] = []
    for level in range(1, 6):
        level_factor = 0.70 + 0.15 * level
        rows.append(
            {
                "depth_level": level,
                "cancel_intensity_source": "phase132_top_five_depth_feature_matrix.p131_mean_cancel_intensity_depth_levels_2_5",
                "cancel_intensity_mean": mean_cancel,
                "cancel_intensity_p50": p50_cancel,
                "cancel_intensity_p90": p90_cancel,
                "cancel_intensity_multiplier": float(min(1.50, 1.0 + level_factor * p50_cancel / max(p90_cancel, 1.0))),
            }
        )
    return pd.DataFrame(rows)


def build_phase6_generator_anchor(phase6_summary: pd.DataFrame) -> pd.DataFrame:
    if phase6_summary.empty:
        return pd.DataFrame(
            [
                {
                    "anchor_id": "phase6_missing_fallback",
                    "source_rows": 0,
                    "book_state_update_fraction": 0.0,
                    "spread_widening_fraction": 0.0,
                    "best_price_shift_fraction": 0.0,
                    "median_event_intensity_proxy": 1.0,
                    "median_l5_quantity": 0.0,
                    "fill_probability_scale": 1.0,
                }
            ]
        )
    frame = phase6_summary.copy()
    frame["rows"] = pd.to_numeric(frame["rows"], errors="coerce").fillna(0.0)
    total_rows = float(frame["rows"].sum())
    labels = frame.groupby("book_event_label", sort=True)["rows"].sum()
    event_intensity = pd.to_numeric(frame["median_event_intensity_proxy"], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    bid_l5 = pd.to_numeric(frame["median_bid_l5_qty"], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    ask_l5 = pd.to_numeric(frame["median_ask_l5_qty"], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    median_l5_qty = float(pd.concat([bid_l5, ask_l5]).median()) if not bid_l5.empty or not ask_l5.empty else 0.0
    median_intensity = float(event_intensity.median()) if not event_intensity.empty else 1.0
    spread_widening_fraction = float(labels.get("spread_widening", 0.0) / max(total_rows, 1.0))
    best_price_shift_fraction = float(labels.get("best_price_shift", 0.0) / max(total_rows, 1.0))
    fill_scale = float(min(max((1.0 - 0.50 * spread_widening_fraction - 0.25 * best_price_shift_fraction) * min(max(median_intensity, 0.50), 1.50), 0.50), 1.25))
    return pd.DataFrame(
        [
            {
                "anchor_id": "phase6_generator_event_depth_anchor",
                "source_rows": int(total_rows),
                "book_state_update_fraction": float(labels.get("book_state_update", 0.0) / max(total_rows, 1.0)),
                "spread_widening_fraction": spread_widening_fraction,
                "best_price_shift_fraction": best_price_shift_fraction,
                "median_event_intensity_proxy": median_intensity,
                "median_l5_quantity": median_l5_qty,
                "fill_probability_scale": fill_scale,
            }
        ]
    )


def build_fill_model_catalog(cancel_inputs: pd.DataFrame, phase6_anchor: pd.DataFrame) -> pd.DataFrame:
    latency = build_latency_distribution()
    median_latency = float(latency.loc[latency["quantile"].eq("p50"), "latency_ms"].iloc[0])
    phase6_scale = float(phase6_anchor["fill_probability_scale"].iloc[0]) if not phase6_anchor.empty else 1.0
    rows: list[dict[str, Any]] = []
    for depth_level in range(1, 6):
        cancel_multiplier = float(cancel_inputs.loc[cancel_inputs["depth_level"].eq(depth_level), "cancel_intensity_multiplier"].iloc[0])
        for queue_percentile, queue_factor in [(0.10, 0.80), (0.25, 0.55), (0.50, 0.32), (0.75, 0.16), (0.90, 0.08)]:
            latency_factor = float(np.exp(-median_latency / (325.0 + 40.0 * depth_level)))
            depth_factor = 1.0 / (1.0 + 0.18 * (depth_level - 1))
            raw_prob = 0.65 * phase6_scale * queue_factor * latency_factor * depth_factor * cancel_multiplier
            fill_probability = float(min(max(raw_prob, 0.005), 0.60))
            rows.append(
                {
                    "model_id": CONTRACT_VERSION,
                    "depth_level": depth_level,
                    "queue_percentile": queue_percentile,
                    "latency_ms": median_latency,
                    "cancel_intensity_multiplier": cancel_multiplier,
                    "phase6_fill_probability_scale": phase6_scale,
                    "queue_factor": queue_factor,
                    "latency_factor": latency_factor,
                    "depth_factor": depth_factor,
                    "fill_probability": fill_probability,
                    "model_formula": "clip(0.65*phase6_fill_probability_scale*queue_factor*exp(-latency_ms/(325+40*depth_level))*depth_factor*cancel_intensity_multiplier,0.005,0.60)",
                }
            )
    return pd.DataFrame(rows)


def infer_depth_level(candidate_id: str, feature_name: str) -> int:
    text = f"{candidate_id} {feature_name}".upper()
    if "L5" in text:
        return 5
    if "L1" in text or "MICROPRICE" in text:
        return 1
    return 2


def infer_queue_percentile(candidate_id: str) -> float:
    text = candidate_id.upper()
    if "_Q0_9" in text:
        return 0.90
    if "_Q0_75" in text:
        return 0.75
    if "_Q0_5" in text:
        return 0.50
    return 0.50


def build_phase89_sanity_replay(phase89_fill: pd.DataFrame, fill_catalog: pd.DataFrame) -> pd.DataFrame:
    if phase89_fill.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for item in phase89_fill.to_dict("records"):
        candidate_id = str(item.get("candidate_id", ""))
        feature_name = str(item.get("feature_name", ""))
        depth_level = infer_depth_level(candidate_id, feature_name)
        queue_percentile = infer_queue_percentile(candidate_id)
        model_rows = fill_catalog[
            fill_catalog["depth_level"].astype(int).eq(depth_level)
            & np.isclose(fill_catalog["queue_percentile"].astype(float), queue_percentile)
        ]
        model_fill_prob = float(model_rows["fill_probability"].iloc[0]) if not model_rows.empty else 0.05
        prior_fill_prob = float(pd.to_numeric(pd.Series([item.get("base_fill_prob", 0.0)]), errors="coerce").fillna(0.0).iloc[0])
        prior_test_fills = float(pd.to_numeric(pd.Series([item.get("test_expected_fills", 0.0)]), errors="coerce").fillna(0.0).iloc[0])
        prior_test_pnl = float(pd.to_numeric(pd.Series([item.get("test_expected_net_pnl_inr", 0.0)]), errors="coerce").fillna(0.0).iloc[0])
        fill_ratio = float(min(model_fill_prob / max(prior_fill_prob, 0.01), 1.0))
        p133_expected_fills = prior_test_fills * fill_ratio
        p133_expected_net_pnl = prior_test_pnl * fill_ratio
        rows.append(
            {
                "candidate_id": candidate_id,
                "feature_name": feature_name,
                "fill_assumption": item.get("fill_assumption", ""),
                "inferred_depth_level": depth_level,
                "inferred_queue_percentile": queue_percentile,
                "phase89_base_fill_prob": prior_fill_prob,
                "phase133_model_fill_prob": model_fill_prob,
                "fill_ratio_vs_phase89": fill_ratio,
                "phase89_test_expected_fills": prior_test_fills,
                "phase133_test_expected_fills": p133_expected_fills,
                "phase89_test_expected_net_pnl_inr": prior_test_pnl,
                "phase133_test_expected_net_pnl_inr": p133_expected_net_pnl,
                "directionally_consistent_with_phase89": bool((prior_test_pnl < 0 and p133_expected_net_pnl < 0) or (prior_test_pnl == 0 and p133_expected_net_pnl == 0) or (prior_test_pnl > 0 and p133_expected_net_pnl > 0)),
                "phase133_passive_branch_survives": False,
                "strategy_replay_allowed": 0,
            }
        )
    return pd.DataFrame(rows)


def build_contract(
    phase132_summary: pd.DataFrame,
    phase6_anchor: pd.DataFrame,
    cancel_inputs: pd.DataFrame,
    latency_distribution: pd.DataFrame,
    fill_catalog: pd.DataFrame,
) -> dict[str, Any]:
    kill_switch_fired = as_int(metric_value(phase132_summary, "phase132_kill_switch_fired", 1), 1)
    surviving_features = as_int(metric_value(phase132_summary, "phase132_surviving_feature_rows", 0), 0)
    return {
        "contract_version": CONTRACT_VERSION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "retail_passive_visible_top_five_market_by_price_execution_model",
        "terminology": {
            "market_data_scope": "Zerodha WebSocket Level-2/top-five market-by-price depth",
            "book_depth_levels": "depth_level_1..depth_level_5 are visible aggregated bid/ask price levels, not market-data L1-L5 tiers",
            "queue_position_limit": "true exchange queue position is unobserved and modelled conservatively",
        },
        "zerodha_cost_model_version": ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        "phase132_kill_switch_fired": kill_switch_fired,
        "phase132_surviving_feature_rows": surviving_features,
        "phase134_open_allowed": False,
        "model_inputs": {
            "phase6_generator_anchor_source": "outputs/phase133/phase133_phase6_generator_anchor.csv",
            "cancel_intensity_source": "outputs/phase132/top_five_depth_feature_matrix.csv",
            "latency_distribution_source": "phase133_contract_static_retail_distribution",
            "fill_probability_catalog_source": "outputs/phase133/phase133_fill_probability_catalog.csv",
        },
        "phase6_generator_anchor": phase6_anchor.to_dict("records"),
        "latency_distribution": latency_distribution.to_dict("records"),
        "cancel_intensity_by_depth_level": cancel_inputs.to_dict("records"),
        "fill_probability_formula": fill_catalog["model_formula"].iloc[0] if not fill_catalog.empty else "",
        "guardrails": [
            "no_new_strategies",
            "no_order_arrival_stream",
            "no_live_tagged_fill_model",
            "no_pnl_replay_promotion",
            "phase134_remains_closed_when_phase132_kill_switch_fired",
        ],
    }


def evaluate_gates(phase132_summary: pd.DataFrame, sanity: pd.DataFrame, contract: dict[str, Any]) -> pd.DataFrame:
    kill_switch_fired = as_int(metric_value(phase132_summary, "phase132_kill_switch_fired", 1), 1)
    surviving_features = as_int(metric_value(phase132_summary, "phase132_surviving_feature_rows", 0), 0)
    directional_consistency = bool(not sanity.empty and sanity["directionally_consistent_with_phase89"].astype(bool).all())
    no_survivors_promoted = bool(not sanity.empty and not sanity["phase133_passive_branch_survives"].astype(bool).any())
    rows = [
        ("phase133_contract_created", True, contract.get("contract_version", ""), "non_empty_contract_version", "hard"),
        ("phase133_phase132_kill_switch_respected", bool(kill_switch_fired == 1 and contract.get("phase134_open_allowed") is False), f"kill_switch={kill_switch_fired};phase134_open_allowed={contract.get('phase134_open_allowed')}", "kill_switch_blocks_phase134", "hard"),
        ("phase133_no_phase132_surviving_features_promoted", bool(surviving_features == 0 and no_survivors_promoted), f"surviving_features={surviving_features};sanity_survivors={int(sanity['phase133_passive_branch_survives'].astype(bool).sum()) if not sanity.empty else 0}", "zero_promoted_survivors", "hard"),
        ("phase133_phase89_sanity_direction_consistent", directional_consistency, int(directional_consistency), 1, "hard"),
        ("phase133_strategy_replay_remains_closed", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate", "pass", "observed", "required", "severity"])


def summarize(gates: pd.DataFrame, phase132_summary: pd.DataFrame, sanity: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["pass"].astype(bool).sum()) if not hard.empty else 0
    hard_total = int(len(hard))
    best_p133_pnl = float(pd.to_numeric(sanity["phase133_test_expected_net_pnl_inr"], errors="coerce").max()) if not sanity.empty else 0.0
    worst_p133_pnl = float(pd.to_numeric(sanity["phase133_test_expected_net_pnl_inr"], errors="coerce").min()) if not sanity.empty else 0.0
    kill_switch_fired = as_int(metric_value(phase132_summary, "phase132_kill_switch_fired", 1), 1)
    surviving_features = as_int(metric_value(phase132_summary, "phase132_surviving_feature_rows", 0), 0)
    phase134_open = bool(hard_pass == hard_total and kill_switch_fired == 0 and surviving_features > 0)
    return pd.DataFrame(
        [
            ("phase133_hard_gate_rows", hard_total, "Hard execution-model gates evaluated"),
            ("phase133_hard_gate_pass_rows", hard_pass, "Hard execution-model gates passed"),
            ("phase133_contract_created", 1, "Pinned execution contract emitted"),
            ("phase133_phase132_kill_switch_fired", kill_switch_fired, "Inherited Phase132 kill-switch flag"),
            ("phase133_phase132_surviving_feature_rows", surviving_features, "Inherited Phase132 surviving feature rows"),
            ("phase133_phase89_sanity_rows", int(len(sanity)), "Phase89 fill-assumption rows re-evaluated under Phase133 fill model"),
            ("phase133_best_sanity_test_expected_net_pnl_inr", best_p133_pnl, "Best Phase133 sanity replay expected test PnL"),
            ("phase133_worst_sanity_test_expected_net_pnl_inr", worst_p133_pnl, "Worst Phase133 sanity replay expected test PnL"),
            ("phase133_phase134_open_allowed", int(phase134_open), "1 means Phase134 precommit may open"),
            ("phase133_strategy_replay_allowed", 0, "Phase133 never unlocks strategy replay"),
            ("phase133_next_best_action", "stop_update_phase116_blocklist_do_not_open_phase134" if not phase134_open else "run_phase134_deep_book_passive_strategy_precommit", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase133 Retail Passive Execution Model Upgrade",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase133 emits a conservative visible-depth passive-fill contract and sanity-checks Phase89 passive queue-capture evidence under that contract.",
        "It creates no strategy definitions, no order-arrival stream, no live-tagged fill model, and no promoted profitability claim.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase133_passive_execution_model_upgrade_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase133(output_dir: Path, base_dir: Path, phase6_dir: Path, phase89_dir: Path, phase131_dir: Path, phase132_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase132_summary = read_csv(phase132_dir / "phase132_deep_book_feature_diagnostics_acceptance_summary.csv")
    phase132_matrix = read_csv(phase132_dir / "top_five_depth_feature_matrix.csv")
    phase89_fill = read_csv(phase89_dir / "passive_candidate_fill_assumption_results.csv")
    phase131_cost_regimes = read_csv(phase131_dir / "phase131_cost_regimes.csv")
    phase6_summary = read_csv(phase6_dir / "l2_book_summary.csv")

    latency_distribution = build_latency_distribution()
    phase6_anchor = build_phase6_generator_anchor(phase6_summary)
    cancel_inputs = build_cancel_intensity_inputs(phase132_matrix)
    fill_catalog = build_fill_model_catalog(cancel_inputs, phase6_anchor)
    sanity = build_phase89_sanity_replay(phase89_fill, fill_catalog)
    contract = build_contract(phase132_summary, phase6_anchor, cancel_inputs, latency_distribution, fill_catalog)
    gates = evaluate_gates(phase132_summary, sanity, contract)
    acceptance = summarize(gates, phase132_summary, sanity)

    (output_dir / "phase133_execution_contract.json").write_text(json.dumps(contract, indent=2), encoding="utf-8")
    phase6_anchor.to_csv(output_dir / "phase133_phase6_generator_anchor.csv", index=False)
    latency_distribution.to_csv(output_dir / "phase133_latency_distribution.csv", index=False)
    cancel_inputs.to_csv(output_dir / "phase133_cancel_intensity_inputs.csv", index=False)
    fill_catalog.to_csv(output_dir / "phase133_fill_probability_catalog.csv", index=False)
    sanity.to_csv(output_dir / "phase133_phase89_sanity_replay.csv", index=False)
    phase131_cost_regimes.to_csv(output_dir / "phase133_inherited_phase131_cost_regimes.csv", index=False)
    gates.to_csv(output_dir / "phase133_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase133_passive_execution_model_upgrade_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Latency Distribution": latency_distribution,
            "Phase6 Generator Anchor": phase6_anchor,
            "Cancel Intensity Inputs": cancel_inputs,
            "Phase89 Sanity Replay": sanity.head(60),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase133_passive_execution_model_upgrade",
        **reproducibility_fields(
            artifact_id="phase133",
            generated_utc=generated_utc,
            inputs={
                "phase6_summary": str(phase6_dir / "l2_book_summary.csv"),
                "phase89_fill_assumption_results": str(phase89_dir / "passive_candidate_fill_assumption_results.csv"),
                "phase131_cost_regimes": str(phase131_dir / "phase131_cost_regimes.csv"),
                "phase132_summary": str(phase132_dir / "phase132_deep_book_feature_diagnostics_acceptance_summary.csv"),
                "phase132_feature_matrix": str(phase132_dir / "top_five_depth_feature_matrix.csv"),
            },
            parameters={
                "contract_version": CONTRACT_VERSION,
                "zerodha_cost_model_version": ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
                "phase6_summary_rows_loaded": int(len(phase6_summary)),
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
                "phase134_open_policy": "closed_when_phase132_kill_switch_fired_or_zero_surviving_features",
            },
            outputs={
                "execution_contract": str(output_dir / "phase133_execution_contract.json"),
                "phase6_generator_anchor": str(output_dir / "phase133_phase6_generator_anchor.csv"),
                "latency_distribution": str(output_dir / "phase133_latency_distribution.csv"),
                "cancel_intensity_inputs": str(output_dir / "phase133_cancel_intensity_inputs.csv"),
                "fill_probability_catalog": str(output_dir / "phase133_fill_probability_catalog.csv"),
                "phase89_sanity_replay": str(output_dir / "phase133_phase89_sanity_replay.csv"),
                "gate_evaluation": str(output_dir / "phase133_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase133_passive_execution_model_upgrade_acceptance_summary.csv"),
                "report": str(output_dir / "phase133_passive_execution_model_upgrade_report.md"),
                "manifest": str(output_dir / "phase133_passive_execution_model_upgrade_manifest.json"),
            },
            random_seed="none_deterministic_execution_contract",
            scenario_ids="phase133_passive_execution_model_upgrade",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version=CONTRACT_VERSION,
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase133_passive_execution_model_upgrade_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase133 passive execution model upgrade.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--phase6-dir", type=Path, default=DEFAULT_PHASE6_DIR)
    parser.add_argument("--phase89-dir", type=Path, default=DEFAULT_PHASE89_DIR)
    parser.add_argument("--phase131-dir", type=Path, default=DEFAULT_PHASE131_DIR)
    parser.add_argument("--phase132-dir", type=Path, default=DEFAULT_PHASE132_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase133(args.output_dir, args.base_dir, args.phase6_dir, args.phase89_dir, args.phase131_dir, args.phase132_dir)


if __name__ == "__main__":
    main()
