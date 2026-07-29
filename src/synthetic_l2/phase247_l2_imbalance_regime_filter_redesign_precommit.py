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


DEFAULT_PHASE244_DIR = Path("outputs/phase244")
DEFAULT_PHASE246_DIR = Path("outputs/phase246")
DEFAULT_OUTPUT_DIR = Path("outputs/phase247")
FORBIDDEN_TUNING_DATES = ("2026-07-17", "2026-07-20")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(path: Path, metric: str, default: Any = None) -> Any:
    frame = read_csv(path)
    if frame.empty or "metric" not in frame.columns:
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


def build_failure_attribution(phase246_dir: Path) -> pd.DataFrame:
    acceptance = phase246_dir / "phase246_acceptance_summary.csv"
    controls = read_csv(phase246_dir / "phase246_control_summary.csv")
    gates = read_csv(phase246_dir / "phase246_gate_evaluation.csv")
    rows: list[dict[str, Any]] = []
    rows.append(
        {
            "failure_id": "P247_BAR_REVERSAL_ALONE_FAILED_FRESH_DATE",
            "observed_value": as_int(metric_value(acceptance, "phase246_one_date_diagnostic_candidate_survived", 0)),
            "required_value": 1,
            "interpretation": "Frozen bar-return reversal did not survive one fresh unseen date; redesign required before any more downloads.",
        }
    )
    for control in controls.to_dict("records"):
        if str(control.get("passed")).lower() != "true":
            rows.append(
                {
                    "failure_id": f"P247_CONTROL_FAIL_{control.get('control_id')}",
                    "observed_value": control.get("net_pnl_inr", ""),
                    "required_value": "control_pass=True",
                    "interpretation": "Existing candidate is not robust enough under the configured control.",
                }
            )
    for gate in gates.to_dict("records"):
        if str(gate.get("severity")) == "diagnostic" and str(gate.get("passed")).lower() != "true":
            rows.append(
                {
                    "failure_id": f"P247_GATE_FAIL_{gate.get('gate_id')}",
                    "observed_value": gate.get("observed_value", ""),
                    "required_value": gate.get("required_value", ""),
                    "interpretation": "One-date diagnostic gate failed; do not continue this frozen candidate date-by-date.",
                }
            )
    return pd.DataFrame(rows)


def build_feature_availability() -> pd.DataFrame:
    rows = [
        ("bar_return", "required", "existing Phase235/246 event-bar field", "primary reversal trigger retained but no longer sufficient alone"),
        ("avg_top5_market_by_price_imbalance", "required", "top-five market-by-price depth field", "confirm reversal pressure or veto continuation-aligned depth"),
        ("avg_l1_imbalance", "optional_confirmation", "best bid/ask depth field", "secondary order-book pressure check"),
        ("avg_spread", "required", "event-bar spread field", "avoid expensive or unstable spread states"),
        ("taker_round_trip_cost_floor_bps", "required", "modeled Zerodha cost and spread floor", "cost floor remains embedded in every replay"),
        ("avg_event_intensity_proxy", "required", "tick/update intensity proxy", "avoid weak bars with insufficient market activity"),
        ("abs_bar_return_bps", "required", "bar move size field", "compare bar move with recent volatility/range regime"),
        ("market_direction_proxy", "required_if_available", "NIFTYBEES or index proxy to be materialized in Phase248 if present", "veto reversal trades aligned with broad market continuation"),
        ("news_event_calendar", "blocked_external_optional", "not currently available locally", "do not fabricate news labels; leave as explicit external data gap"),
    ]
    return pd.DataFrame(rows, columns=["feature_or_filter", "status", "source", "purpose"])


def build_redesign_candidate_catalog(phase244_dir: Path) -> pd.DataFrame:
    candidate_id = metric_value(phase244_dir / "phase244_acceptance_summary.csv", "phase244_candidate_id", "")
    rows = [
        {
            "redesign_id": "P247_REVERSAL_L2_CONFIRMATION",
            "parent_candidate_id": candidate_id,
            "entry_logic": "bar_return reversal only when top-five market-by-price imbalance points against continuation and toward reversal",
            "required_filters": "avg_top5_market_by_price_imbalance directional confirmation; spread guard; event-intensity guard; cost floor",
            "tuning_scope": "training_only_excludes_2026_07_17_and_2026_07_20",
            "holdout_execution_now_allowed": 0,
        },
        {
            "redesign_id": "P247_REVERSAL_L2_DIVERGENCE",
            "parent_candidate_id": candidate_id,
            "entry_logic": "large bar-return reversal only when price impulse and top-five imbalance diverge",
            "required_filters": "bar_return sign opposite depth-pressure sign; spread guard; recent-volatility normalization",
            "tuning_scope": "training_only_excludes_2026_07_17_and_2026_07_20",
            "holdout_execution_now_allowed": 0,
        },
        {
            "redesign_id": "P247_RANGE_ONLY_REVERSAL",
            "parent_candidate_id": candidate_id,
            "entry_logic": "bar-return reversal only in range-bound / non-trending volatility states",
            "required_filters": "recent volatility/range filter; market-direction veto if proxy available; spread guard",
            "tuning_scope": "training_only_excludes_2026_07_17_and_2026_07_20",
            "holdout_execution_now_allowed": 0,
        },
        {
            "redesign_id": "P247_COMBINED_STRICT_REVERSAL",
            "parent_candidate_id": candidate_id,
            "entry_logic": "strict conjunction of reversal trigger, top-five imbalance confirmation, range regime, liquidity/spread and market-direction veto",
            "required_filters": "all P247 required filters; smallest turnover first; 2x-cost-positive objective",
            "tuning_scope": "training_only_excludes_2026_07_17_and_2026_07_20",
            "holdout_execution_now_allowed": 0,
        },
    ]
    return pd.DataFrame(rows)


def build_acceptance_contract() -> pd.DataFrame:
    rows = [
        ("H247_NO_HOLDOUT_TUNING", f"Exclude {';'.join(FORBIDDEN_TUNING_DATES)} from threshold, filter and parameter selection", "hard"),
        ("H247_L2_FILTER_REQUIRED", "At least one top-five market-by-price imbalance filter must be active", "hard"),
        ("H247_RANGE_OR_MARKET_VETO_REQUIRED", "At least one range-regime or market-direction veto must be active if the needed proxy exists", "hard"),
        ("H247_LIQUIDITY_SPREAD_GUARD_REQUIRED", "Spread/liquidity guard must be active before any replay candidate can be opened", "hard"),
        ("H247_COST_STRESS_FIRST_OBJECTIVE", "Candidate ranking must prefer positive 2.0x-cost net P&L before base-cost headline P&L", "hard"),
        ("H247_RANDOM_SIDE_AND_SIDE_FLIP_CONTROLS", "Random-side beat >=0.95 and side-flip net negative remain required", "hard"),
        ("H247_NO_MORE_DATE_DOWNLOAD_FOR_FAILED_PARENT", "Do not download more fresh dates for the failed Phase244 parent candidate", "hard"),
        ("H247_NO_PAPER_LIVE", "No paper/live/deployable profitability claim from the redesign precommit", "hard"),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "requirement", "requirement_type"])


def build_gate_evaluation(failures: pd.DataFrame, features: pd.DataFrame, candidates: pd.DataFrame, contract: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("P247_PHASE246_FAILURE_OBSERVED", not failures.empty, len(failures), ">0 failure attribution rows", "hard"),
        ("P247_TOP5_IMBALANCE_INCLUDED", bool(features["feature_or_filter"].astype(str).eq("avg_top5_market_by_price_imbalance").any()), "avg_top5_market_by_price_imbalance", "present", "hard"),
        ("P247_REDESIGN_CATALOG_WRITTEN", len(candidates) >= 3, len(candidates), ">=3 redesign candidates", "hard"),
        ("P247_ACCEPTANCE_CONTRACT_WRITTEN", len(contract) >= 6, len(contract), ">=6 contract rows", "hard"),
        ("P247_NO_HOLDOUT_TUNING", True, ";".join(FORBIDDEN_TUNING_DATES), "excluded from tuning", "hard"),
        ("P247_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase247 L2 Imbalance / Regime-filter Redesign Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase247 converts the Phase246 failure into a bounded redesign contract.",
        "It explicitly rejects bar-return reversal as a standalone strategy and requires top-five market-by-price imbalance, spread/liquidity, volatility/range and market-direction checks before the next training-only search.",
        "No new raw date is downloaded, no holdout data is tuned, and no paper/live or deployable profitability claim is opened.",
        "",
    ]
    for title, table in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(table), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase244_dir: Path = DEFAULT_PHASE244_DIR, phase246_dir: Path = DEFAULT_PHASE246_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    failures = build_failure_attribution(phase246_dir)
    features = build_feature_availability()
    candidates = build_redesign_candidate_catalog(phase244_dir)
    contract = build_acceptance_contract()
    gates = build_gate_evaluation(failures, features, candidates, contract)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    next_action = "run_phase248_training_only_l2_imbalance_regime_filtered_redesign_no_2026_07_17_or_2026_07_20_tuning_no_downloads_no_paper_live"
    acceptance = pd.DataFrame(
        [
            ("phase247_l2_imbalance_regime_filter_redesign_precommit_complete", 1, "Phase247 redesign precommit completed"),
            ("phase247_parent_candidate_id", metric_value(phase244_dir / "phase244_acceptance_summary.csv", "phase244_candidate_id", ""), "Failed frozen Phase244 parent candidate"),
            ("phase247_failure_attribution_rows", len(failures), "Phase246 failure rows attributed"),
            ("phase247_feature_filter_rows", len(features), "Required/optional feature filter rows"),
            ("phase247_redesign_candidate_rows", len(candidates), "Redesign candidate families precommitted"),
            ("phase247_acceptance_contract_rows", len(contract), "Acceptance contract rows"),
            ("phase247_forbidden_tuning_dates", ";".join(FORBIDDEN_TUNING_DATES), "Dates excluded from tuning"),
            ("phase247_l2_imbalance_filter_required", 1, "Top-five market-by-price imbalance filter required"),
            ("phase247_range_or_market_veto_required", 1, "Range-regime or market-direction veto required"),
            ("phase247_cost_stress_first_objective", 1, "2x cost stress prioritized in candidate ranking"),
            ("phase247_no_more_downloads_for_failed_parent_allowed", 1, "No more raw-date downloads for failed parent candidate"),
            ("phase247_training_search_allowed_next", 1, "Phase248 training-only redesign search may run next"),
            ("phase247_holdout_execution_allowed_now", 0, "No holdout execution in Phase247"),
            ("phase247_strategy_promotion_allowed", 0, "No strategy promotion from Phase247"),
            ("phase247_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase247"),
            ("phase247_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase247"),
            ("phase247_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase247_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase247_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    failures.to_csv(output_dir / "phase247_failure_attribution.csv", index=False)
    features.to_csv(output_dir / "phase247_required_filter_catalog.csv", index=False)
    candidates.to_csv(output_dir / "phase247_redesign_candidate_catalog.csv", index=False)
    contract.to_csv(output_dir / "phase247_acceptance_contract.csv", index=False)
    gates.to_csv(output_dir / "phase247_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase247_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase247_l2_imbalance_regime_filter_redesign_precommit_report.md",
        {
            "Acceptance Summary": acceptance,
            "Failure Attribution": failures,
            "Required Filter Catalog": features,
            "Redesign Candidate Catalog": candidates,
            "Acceptance Contract": contract,
            "Gate Evaluation": gates,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase247_l2_imbalance_regime_filter_redesign_precommit",
        **reproducibility_fields(
            artifact_id="phase247",
            generated_utc=generated_utc,
            inputs={
                "phase244_dir": str(phase244_dir),
                "phase246_dir": str(phase246_dir),
            },
            parameters={
                "forbidden_tuning_dates": FORBIDDEN_TUNING_DATES,
                "holdout_tuning_allowed": 0,
                "download_execution_allowed": 0,
                "holdout_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "failure_attribution": str(output_dir / "phase247_failure_attribution.csv"),
                "required_filter_catalog": str(output_dir / "phase247_required_filter_catalog.csv"),
                "redesign_candidate_catalog": str(output_dir / "phase247_redesign_candidate_catalog.csv"),
                "acceptance_contract": str(output_dir / "phase247_acceptance_contract.csv"),
                "gate_evaluation": str(output_dir / "phase247_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase247_acceptance_summary.csv"),
                "report": str(output_dir / "phase247_l2_imbalance_regime_filter_redesign_precommit_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_precommit_only",
        ),
    }
    (output_dir / "phase247_l2_imbalance_regime_filter_redesign_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Precommit Phase247 L2 imbalance / regime-filter redesign.")
    parser.add_argument("--phase244-dir", type=Path, default=DEFAULT_PHASE244_DIR)
    parser.add_argument("--phase246-dir", type=Path, default=DEFAULT_PHASE246_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase244_dir=args.phase244_dir, phase246_dir=args.phase246_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
