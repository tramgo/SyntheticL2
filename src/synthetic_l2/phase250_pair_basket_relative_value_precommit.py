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


DEFAULT_PHASE235_BARS = Path("outputs/phase235/phase235_real_event_bars.parquet")
DEFAULT_PHASE249_DIR = Path("outputs/phase249")
DEFAULT_OUTPUT_DIR = Path("outputs/phase250")
FORBIDDEN_TUNING_DATES = ("2026-07-17", "2026-07-20")


PAIR_GROUPS: dict[str, list[str]] = {
    "bank_finance": ["AXISBANK", "HDFCBANK", "ICICIBANK", "KOTAKBANK", "SBIN"],
    "information_technology": ["HCLTECH", "INFY", "TCS", "TECHM", "WIPRO"],
    "auto": ["BAJAJ-AUTO", "M&M", "MARUTI"],
    "pharma": ["CIPLA", "DRREDDY", "SUNPHARMA"],
    "consumer": ["BRITANNIA", "HINDUNILVR", "ITC", "NESTLEIND"],
    "energy": ["BPCL", "ONGC", "RELIANCE"],
    "infra_capital_goods": ["ADANIPORTS", "LT", "ULTRACEMCO"],
    "index_etf_basket": ["BANKBEES", "NIFTYBEES", "JUNIORBEES"],
}

BENCHMARK_ONLY = {
    "BHARTIARTL": "single telecom name in current universe; usable only against broad basket unless a telecom peer appears",
    "GOLDBEES": "commodity ETF; keep out of equity-sector pair residuals",
    "ITBEES": "sector ETF; usable as IT basket reference, not as a single-name equity peer",
}


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


def load_event_bar_profile(event_bars_path: Path) -> tuple[pd.DataFrame, dict[str, Any]]:
    bars = pd.read_parquet(event_bars_path)
    symbols = sorted(bars["symbol"].astype(str).unique().tolist()) if "symbol" in bars.columns else []
    profile = {
        "rows": int(len(bars)),
        "dates": int(bars["trade_date"].nunique()) if "trade_date" in bars.columns else 0,
        "symbols": int(len(symbols)),
        "symbol_list": symbols,
        "columns": list(bars.columns),
    }
    return bars, profile


def build_universe(symbols: list[str]) -> pd.DataFrame:
    available = set(symbols)
    rows: list[dict[str, Any]] = []
    for group_id, group_symbols in PAIR_GROUPS.items():
        present = [symbol for symbol in group_symbols if symbol in available]
        for symbol in group_symbols:
            if symbol not in available:
                continue
            rows.append(
                {
                    "symbol": symbol,
                    "peer_group_id": group_id,
                    "group_size_available": len(present),
                    "role": "pair_and_basket" if len(present) >= 2 else "basket_only",
                    "phase251_allowed": int(len(present) >= 2),
                    "notes": "eligible for peer residuals and market-neutral baskets",
                }
            )
    assigned = {row["symbol"] for row in rows}
    for symbol in symbols:
        if symbol in assigned:
            continue
        rows.append(
            {
                "symbol": symbol,
                "peer_group_id": "benchmark_or_singleton",
                "group_size_available": 1,
                "role": "benchmark_or_excluded",
                "phase251_allowed": 0,
                "notes": BENCHMARK_ONLY.get(symbol, "not enough same-group peers in current universe"),
            }
        )
    return pd.DataFrame(rows).sort_values(["phase251_allowed", "peer_group_id", "symbol"], ascending=[False, True, True]).reset_index(drop=True)


def build_feature_contract(columns: list[str]) -> pd.DataFrame:
    required_rows = [
        ("trade_date", "input", "date partition and train/holdout exclusion key"),
        ("symbol", "input", "cross-sectional and peer grouping key"),
        ("source_event_bar_id", "input", "same event-bar clock used for cross-symbol alignment"),
        ("open_mid_price", "input", "event-bar opening mid"),
        ("close_mid_price", "input", "event-bar closing mid and future-return anchor"),
        ("bar_return", "input", "symbol event-bar return used for residual construction"),
        ("avg_top5_market_by_price_imbalance", "input", "top-five market-by-price depth imbalance, not universal L5 data"),
        ("avg_l1_imbalance", "input", "secondary top-of-book pressure check"),
        ("avg_spread", "input", "liquidity/spread guard"),
        ("avg_event_intensity_proxy", "input", "activity/volume-style guard"),
        ("taker_round_trip_cost_floor_bps", "input", "modeled Zerodha cost and spread floor"),
        ("abs_bar_return_bps", "input", "recent move magnitude / volatility comparison proxy"),
        ("peer_group_id", "phase251_derived", "static group assignment from the Phase250 universe catalog"),
        ("basket_return", "phase251_derived", "leave-one-out peer or benchmark basket return"),
        ("symbol_residual_return", "phase251_derived", "symbol return minus basket return"),
        ("relative_top5_imbalance", "phase251_derived", "symbol top-five imbalance minus peer/basket imbalance"),
        ("cross_sectional_rank", "phase251_derived", "within-event residual rank used for long/short baskets"),
        ("market_beta_proxy", "phase251_optional", "rough broad-basket sensitivity; do not tune on forbidden dates"),
    ]
    present = set(columns)
    rows = [
        {
            "feature_name": name,
            "source_stage": stage,
            "required_for_phase251": int(stage in {"input", "phase251_derived"}),
            "present_now": int(stage != "input" or name in present),
            "purpose": purpose,
        }
        for name, stage, purpose in required_rows
    ]
    return pd.DataFrame(rows)


def build_candidate_family_catalog() -> pd.DataFrame:
    rows = [
        {
            "family_id": "P250_SECTOR_PAIR_RESIDUAL_REVERSION",
            "hypothesis": "A stock stretched versus its same-sector peer basket reverts after common market movement is hedged.",
            "required_inputs": "bar_return, peer_group_id, basket_return, symbol_residual_return, taker_round_trip_cost_floor_bps",
            "top_five_depth_use": "veto residual reversion when top-five imbalance confirms continuation pressure",
            "market_neutrality": "long/short pair or leave-one-out sector basket",
        },
        {
            "family_id": "P250_INDEX_BASKET_RESIDUAL_REVERSION",
            "hypothesis": "A stock residual versus NIFTYBEES/BANKBEES/JUNIORBEES style baskets reverts only when cost floor is small.",
            "required_inputs": "bar_return, benchmark basket return, symbol_residual_return, spread and cost floor",
            "top_five_depth_use": "require depth pressure to disagree with the stretched price impulse",
            "market_neutrality": "single stock versus benchmark ETF proxy where available",
        },
        {
            "family_id": "P250_TOP5_IMBALANCE_RELATIVE_DIVERGENCE",
            "hypothesis": "Relative top-five depth pressure predicts near-term convergence better than absolute bar reversal.",
            "required_inputs": "avg_top5_market_by_price_imbalance, relative_top5_imbalance, future close-mid return",
            "top_five_depth_use": "primary signal source rather than a decorative filter",
            "market_neutrality": "ranked long/short within sector or broad basket",
        },
        {
            "family_id": "P250_MARKET_NEUTRAL_LONG_SHORT_BASKET",
            "hypothesis": "Long the strongest residual/depth-confirmed names and short the weakest residual/depth-confirmed names within each event window.",
            "required_inputs": "cross_sectional_rank, symbol_residual_return, relative_top5_imbalance, cost floor",
            "top_five_depth_use": "must support selected long/short ranks after spread/liquidity filtering",
            "market_neutrality": "notional-balanced long and short legs; costs applied per leg",
        },
    ]
    return pd.DataFrame(rows)


def build_acceptance_contract() -> pd.DataFrame:
    rows = [
        ("P250_NO_FORBIDDEN_TUNING_DATES", "Phase251 search must exclude 2026-07-17 and 2026-07-20 from parameter selection.", "hard"),
        ("P250_EXISTING_BARS_ONLY", "Phase251 starts from existing Phase235 real event bars; no new raw L2 download until a frozen materially new survivor exists.", "hard"),
        ("P250_MIN_GROUPS", "At least 5 peer groups with 2 or more available symbols must be present.", "hard"),
        ("P250_MIN_GROUPED_SYMBOLS", "At least 20 symbols must be eligible for peer/basket construction.", "hard"),
        ("P250_MARKET_NEUTRAL_NOTIONALS", "Pair/basket variants must balance long and short notional before cost and risk scoring.", "hard"),
        ("P250_COST_PER_LEG", "Zerodha-modeled costs, spread and slippage must be applied per leg; pair/basket costs are not single-leg costs.", "hard"),
        ("P250_2X_COST_FIRST", "No survivor may proceed without positive 2.0x modeled-cost net P&L.", "hard"),
        ("P250_CONTROLS_REQUIRED", "Side-flip, random-side, concentration and cost-stress controls remain mandatory.", "hard"),
        ("P250_BREADTH_REQUIRED", "Any training survivor must use at least 4 dates, 8 symbols and 20 trades before holdout precommit.", "hard"),
        ("P250_NO_PROFIT_CLAIM", "Phase250 is a precommit only: no replay execution, paper/live acceptance or deployable profitability claim.", "hard"),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "requirement", "severity"])


def build_gate_evaluation(
    phase249_dir: Path,
    profile: dict[str, Any],
    universe: pd.DataFrame,
    feature_contract: pd.DataFrame,
    family_catalog: pd.DataFrame,
    acceptance_contract: pd.DataFrame,
) -> pd.DataFrame:
    selected_route = str(metric_value(phase249_dir / "phase249_acceptance_summary.csv", "phase249_selected_next_route", ""))
    next_action = str(metric_value(phase249_dir / "phase249_acceptance_summary.csv", "phase249_next_best_action", ""))
    grouped = universe.loc[universe["phase251_allowed"].astype(int).eq(1)]
    groups = int(grouped["peer_group_id"].nunique()) if not grouped.empty else 0
    grouped_symbols = int(grouped["symbol"].nunique()) if not grouped.empty else 0
    required_inputs_present = bool(feature_contract.loc[feature_contract["source_stage"].eq("input"), "present_now"].astype(bool).all())
    rows = [
        ("P250_PHASE249_ROUTE_SELECTED", selected_route == "P249_PAIR_OR_BASKET_RELATIVE_VALUE", selected_route, "P249_PAIR_OR_BASKET_RELATIVE_VALUE", "hard"),
        ("P250_PHASE249_WORK_ORDER_PRESENT", "run_phase250_pair_basket_relative_value_precommit" in next_action, next_action, "Phase249 next action points to Phase250 pair/basket precommit", "hard"),
        ("P250_EVENT_BARS_AVAILABLE", profile["rows"] > 0, profile["rows"], ">0 Phase235 real event bars", "hard"),
        ("P250_FORBIDDEN_DATES_NOT_USED_FOR_TUNING", True, ",".join(FORBIDDEN_TUNING_DATES), "Excluded from Phase251 parameter search", "hard"),
        ("P250_REQUIRED_INPUT_FEATURES_PRESENT", required_inputs_present, int(required_inputs_present), "all required input features present", "hard"),
        ("P250_MIN_GROUPS_AVAILABLE", groups >= 5, groups, ">=5 peer groups", "hard"),
        ("P250_MIN_GROUPED_SYMBOLS_AVAILABLE", grouped_symbols >= 20, grouped_symbols, ">=20 eligible grouped symbols", "hard"),
        ("P250_CANDIDATE_FAMILIES_REGISTERED", len(family_catalog) >= 4, len(family_catalog), ">=4 materially different pair/basket families", "hard"),
        ("P250_ACCEPTANCE_CONTRACT_REGISTERED", len(acceptance_contract) >= 10, len(acceptance_contract), ">=10 acceptance contract rows", "hard"),
        ("P250_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase250 Pair/Basket Relative-value Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase250 opens a materially different route after the single-name bar-return reversal branch failed cost robustness.",
        "It precommits the Phase251 training-only search contract for pair/basket relative-value strategies using existing real event bars only.",
        "No raw data download, replay execution, strategy promotion, paper/live acceptance or deployable profitability claim is allowed in this phase.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    event_bars_path: Path = DEFAULT_PHASE235_BARS,
    phase249_dir: Path = DEFAULT_PHASE249_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    _, profile = load_event_bar_profile(event_bars_path)
    universe = build_universe(profile["symbol_list"])
    feature_contract = build_feature_contract(profile["columns"])
    family_catalog = build_candidate_family_catalog()
    acceptance_contract = build_acceptance_contract()
    gates = build_gate_evaluation(phase249_dir, profile, universe, feature_contract, family_catalog, acceptance_contract)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    grouped = universe.loc[universe["phase251_allowed"].astype(int).eq(1)]
    next_action = "run_phase251_training_only_pair_basket_relative_value_search_no_downloads_no_2026_07_17_or_2026_07_20_tuning_no_paper_live"
    acceptance = pd.DataFrame(
        [
            ("phase250_pair_basket_precommit_complete", 1, "Phase250 pair/basket precommit completed"),
            ("phase250_selected_route", "P249_PAIR_OR_BASKET_RELATIVE_VALUE", "Selected materially different route"),
            ("phase250_training_event_bar_rows", profile["rows"], "Existing Phase235 event-bar rows available"),
            ("phase250_training_dates", profile["dates"], "Existing Phase235 dates available before forbidden-date exclusion"),
            ("phase250_training_symbols", profile["symbols"], "Existing Phase235 symbols available"),
            ("phase250_forbidden_tuning_dates", ",".join(FORBIDDEN_TUNING_DATES), "Dates excluded from Phase251 parameter selection"),
            ("phase250_pair_group_rows", int(grouped["peer_group_id"].nunique()) if not grouped.empty else 0, "Peer groups with at least two eligible symbols"),
            ("phase250_grouped_symbols", int(grouped["symbol"].nunique()) if not grouped.empty else 0, "Symbols eligible for pair/basket construction"),
            ("phase250_candidate_family_rows", len(family_catalog), "Candidate families registered"),
            ("phase250_feature_contract_rows", len(feature_contract), "Feature contract rows"),
            ("phase250_required_input_features_present", int(feature_contract.loc[feature_contract["source_stage"].eq("input"), "present_now"].astype(bool).all()), "Required Phase235 input columns present"),
            ("phase250_acceptance_contract_rows", len(acceptance_contract), "Acceptance contract rows"),
            ("phase250_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase250_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase250_phase251_training_search_allowed_next", int(hard_pass == len(hard)), "Whether Phase251 training search is allowed next"),
            ("phase250_download_more_dates_now_allowed", 0, "No raw-date download in Phase250"),
            ("phase250_replay_execution_allowed_now", 0, "No replay execution in Phase250"),
            ("phase250_strategy_promotion_allowed", 0, "No strategy promotion from Phase250"),
            ("phase250_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase250"),
            ("phase250_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase250"),
            ("phase250_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    universe.to_csv(output_dir / "phase250_pair_basket_universe.csv", index=False)
    feature_contract.to_csv(output_dir / "phase250_feature_contract.csv", index=False)
    family_catalog.to_csv(output_dir / "phase250_candidate_family_catalog.csv", index=False)
    acceptance_contract.to_csv(output_dir / "phase250_acceptance_contract.csv", index=False)
    gates.to_csv(output_dir / "phase250_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase250_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase250_pair_basket_relative_value_precommit_report.md",
        {
            "Acceptance Summary": acceptance,
            "Pair/Basket Universe": universe,
            "Feature Contract": feature_contract,
            "Candidate Family Catalog": family_catalog,
            "Acceptance Contract": acceptance_contract,
            "Gate Evaluation": gates,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase250_pair_basket_relative_value_precommit",
        **reproducibility_fields(
            artifact_id="phase250",
            generated_utc=generated_utc,
            inputs={
                "event_bars_path": str(event_bars_path),
                "phase249_dir": str(phase249_dir),
                "forbidden_tuning_dates": list(FORBIDDEN_TUNING_DATES),
            },
            parameters={
                "selected_route": "P249_PAIR_OR_BASKET_RELATIVE_VALUE",
                "download_more_dates_now_allowed": 0,
                "replay_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "universe": str(output_dir / "phase250_pair_basket_universe.csv"),
                "feature_contract": str(output_dir / "phase250_feature_contract.csv"),
                "candidate_family_catalog": str(output_dir / "phase250_candidate_family_catalog.csv"),
                "acceptance_contract": str(output_dir / "phase250_acceptance_contract.csv"),
                "gate_evaluation": str(output_dir / "phase250_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase250_acceptance_summary.csv"),
                "report": str(output_dir / "phase250_pair_basket_relative_value_precommit_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_precommit_only",
        ),
    }
    (output_dir / "phase250_pair_basket_relative_value_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase250 pair/basket relative-value precommit.")
    parser.add_argument("--event-bars-path", type=Path, default=DEFAULT_PHASE235_BARS)
    parser.add_argument("--phase249-dir", type=Path, default=DEFAULT_PHASE249_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(event_bars_path=args.event_bars_path, phase249_dir=args.phase249_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
