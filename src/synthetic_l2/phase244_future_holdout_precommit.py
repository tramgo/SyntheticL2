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


DEFAULT_PHASE243_DIR = Path("outputs/phase243")
DEFAULT_OUTPUT_DIR = Path("outputs/phase244")
FORBIDDEN_TUNING_DATE = "2026-07-17"
MIN_HOLDOUT_DATES = 2
TARGET_HOLDOUT_DATES = 3
MIN_TRADES = 20
MIN_SYMBOLS = 10


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


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def load_best_candidate(phase243_dir: Path) -> dict[str, Any]:
    controlled = read_csv(phase243_dir / "phase243_controlled_candidate_summary.csv")
    if controlled.empty:
        raise FileNotFoundError(phase243_dir / "phase243_controlled_candidate_summary.csv")
    survivors = controlled[controlled["phase243_candidate_survived"].astype(str).str.lower().eq("true")].copy()
    if survivors.empty:
        raise ValueError("Phase243 has no survivor candidate to precommit")
    survivors["_rank_random"] = pd.to_numeric(survivors["random_beat_fraction"], errors="coerce")
    survivors["_rank_2x"] = pd.to_numeric(survivors.get("cost200_net_pnl_inr_y", survivors.get("cost200_net_pnl_inr_x")), errors="coerce")
    survivors = survivors.sort_values(["_rank_random", "_rank_2x"], ascending=[False, False])
    return survivors.iloc[0].drop(labels=["_rank_random", "_rank_2x"]).to_dict()


def build_frozen_candidate_spec(best: dict[str, Any]) -> pd.DataFrame:
    fields = [
        "candidate_id",
        "family_id",
        "signal_source",
        "direction",
        "horizon_event_bars",
        "event_quantile",
        "signal_quantile",
        "event_window_score_threshold",
        "signal_abs_threshold",
        "training_trades",
        "training_dates",
        "training_symbols",
        "training_net_pnl_inr",
        "cost150_net_pnl_inr_x",
        "cost200_net_pnl_inr_x",
        "random_beat_fraction",
        "control_pass_rows",
    ]
    row = {field: best.get(field, "") for field in fields}
    row["frozen_for_future_holdout"] = 1
    row["parameter_tuning_allowed_in_future_holdout"] = 0
    row["forbidden_tuning_date"] = FORBIDDEN_TUNING_DATE
    row["paper_or_live_acceptance_allowed"] = 0
    row["deployable_profitability_claim_allowed"] = 0
    return pd.DataFrame([row])


def build_storage_decision_options() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "option_id": "H244_A_STORAGE_FREE_LOCAL",
                "description": "Free or archive local scratch/smoke/raw data before downloading more unseen real dates",
                "allowed_now": 1,
                "download_allowed_without_user_storage_decision": 0,
                "expected_effect": "enables 2-3 date holdout without new disk pressure",
            },
            {
                "option_id": "H244_B_EXTERNAL_OR_SECONDARY_DISK",
                "description": "Attach or choose a larger storage location for unseen raw L2 dates",
                "allowed_now": 1,
                "download_allowed_without_user_storage_decision": 0,
                "expected_effect": "preserves current local artifacts and shifts raw date footprint off C drive",
            },
            {
                "option_id": "H244_C_ONE_DATE_ONLY_DIAGNOSTIC",
                "description": "Use only already downloaded 2026-07-17 as diagnostic if storage is not expanded",
                "allowed_now": 1,
                "download_allowed_without_user_storage_decision": 0,
                "expected_effect": "fastest but cannot satisfy acceptance and must not tune thresholds",
            },
        ]
    )


def build_holdout_contract(best: dict[str, Any]) -> pd.DataFrame:
    rows = [
        ("H244_FREEZE_CANDIDATE", "Candidate id, horizon, signal source, direction and thresholds are frozen before holdout", "hard"),
        ("H244_NO_2026_07_17_TUNING", "The existing 2026-07-17 holdout cannot be used for threshold or parameter selection", "hard"),
        ("H244_STORAGE_DECISION_REQUIRED", "Choose local cleanup/archive or external storage before downloading more raw dates", "hard"),
        ("H244_MIN_DATES", f"Minimum {MIN_HOLDOUT_DATES} fresh unseen dates; target {TARGET_HOLDOUT_DATES} dates", "acceptance"),
        ("H244_MIN_TRADES", f"At least {MIN_TRADES} frozen-candidate trades after materialization", "acceptance"),
        ("H244_MIN_SYMBOLS", f"At least {MIN_SYMBOLS} symbols represented in selected trades", "acceptance"),
        ("H244_COST_CONTROLS", "Net P&L positive at base, 1.5x and 2.0x modeled Zerodha costs", "acceptance"),
        ("H244_RANDOM_SIDE_CONTROL", "Random-side beat fraction at least 0.95 on the holdout", "acceptance"),
        ("H244_SIDE_FLIP_CONTROL", "Side-flipped net P&L must be negative", "acceptance"),
        ("H244_NO_PAPER_LIVE", "No paper/live/deployable profitability claim from precommit or download phases", "hard"),
    ]
    frame = pd.DataFrame(rows, columns=["contract_id", "requirement", "requirement_type"])
    frame["candidate_id"] = best.get("candidate_id", "")
    return frame


def build_gate_evaluation(best: dict[str, Any], contract: pd.DataFrame, storage_options: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("P244_PHASE243_SURVIVOR_SELECTED", bool(best.get("candidate_id")), best.get("candidate_id", ""), "non-empty Phase243 survivor", "hard"),
        ("P244_CANDIDATE_FROZEN", True, best.get("candidate_id", ""), "candidate spec frozen for future holdout", "hard"),
        ("P244_NO_HOLDOUT_TUNING", True, FORBIDDEN_TUNING_DATE, "2026-07-17 cannot be used for tuning", "hard"),
        ("P244_STORAGE_DECISION_OPTIONS_WRITTEN", len(storage_options) >= 3, len(storage_options), ">=3 storage options", "hard"),
        ("P244_HOLDOUT_CONTRACT_WRITTEN", len(contract) >= 10, len(contract), ">=10 contract requirements", "hard"),
        ("P244_DOWNLOAD_NOT_ALLOWED_NOW", True, 0, "no raw download until storage decision", "hard"),
        ("P244_NO_PAPER_LIVE_OR_PROFIT_CLAIM", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase244 Future Holdout Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase244 freezes the best Phase243 survivor for future holdout testing and defines the storage decision required before any more raw L2 downloads.",
        "It does not download data, tune on 2026-07-17, run a holdout, open paper/live trading, or claim deployable profitability.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase243_dir: Path = DEFAULT_PHASE243_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    best = load_best_candidate(phase243_dir)
    frozen = build_frozen_candidate_spec(best)
    storage_options = build_storage_decision_options()
    contract = build_holdout_contract(best)
    gates = build_gate_evaluation(best, contract, storage_options)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    next_action = "choose_storage_option_then_download_fresh_unseen_dates_for_phase244_frozen_candidate_no_tuning_no_paper_live"
    acceptance = pd.DataFrame(
        [
            ("phase244_future_holdout_precommit_complete", 1, "Phase244 future holdout precommit completed"),
            ("phase244_candidate_id", best.get("candidate_id", ""), "Frozen Phase243 candidate"),
            ("phase244_best_training_net_pnl_inr", as_float(best.get("training_net_pnl_inr", 0.0)), "Training/discovery net P&L"),
            ("phase244_best_cost200_net_pnl_inr", as_float(best.get("cost200_net_pnl_inr_y", best.get("cost200_net_pnl_inr_x", 0.0))), "2x-cost training/discovery net P&L"),
            ("phase244_best_random_beat_fraction", as_float(best.get("random_beat_fraction", 0.0)), "Training random-side beat fraction"),
            ("phase244_min_holdout_dates_required", MIN_HOLDOUT_DATES, "Minimum fresh unseen holdout dates"),
            ("phase244_target_holdout_dates", TARGET_HOLDOUT_DATES, "Target fresh unseen holdout dates"),
            ("phase244_min_holdout_trades_required", MIN_TRADES, "Minimum frozen-candidate holdout trades"),
            ("phase244_min_holdout_symbols_required", MIN_SYMBOLS, "Minimum holdout symbols"),
            ("phase244_storage_decision_required", 1, "Storage decision required before more raw downloads"),
            ("phase244_download_more_dates_now_allowed", 0, "No additional raw-date download in Phase244"),
            ("phase244_holdout_parameter_tuning_allowed", 0, "No 2026-07-17 or future holdout tuning"),
            ("phase244_future_holdout_execution_allowed_now", 0, "Precommit only; no holdout run in Phase244"),
            ("phase244_strategy_promotion_allowed", 0, "No strategy promotion from Phase244"),
            ("phase244_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase244"),
            ("phase244_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase244"),
            ("phase244_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase244_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase244_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    frozen.to_csv(output_dir / "phase244_frozen_candidate_spec.csv", index=False)
    storage_options.to_csv(output_dir / "phase244_storage_decision_options.csv", index=False)
    contract.to_csv(output_dir / "phase244_future_holdout_contract.csv", index=False)
    gates.to_csv(output_dir / "phase244_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase244_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase244_future_holdout_precommit_report.md",
        {
            "Acceptance Summary": acceptance,
            "Frozen Candidate Spec": frozen,
            "Storage Decision Options": storage_options,
            "Future Holdout Contract": contract,
            "Gate Evaluation": gates,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase244_future_holdout_precommit",
        **reproducibility_fields(
            artifact_id="phase244",
            generated_utc=generated_utc,
            inputs={"phase243_dir": str(phase243_dir)},
            parameters={
                "forbidden_tuning_date": FORBIDDEN_TUNING_DATE,
                "min_holdout_dates": MIN_HOLDOUT_DATES,
                "target_holdout_dates": TARGET_HOLDOUT_DATES,
                "min_trades": MIN_TRADES,
                "min_symbols": MIN_SYMBOLS,
                "download_more_dates_now_allowed": 0,
                "holdout_execution_allowed_now": 0,
            },
            outputs={
                "frozen_candidate_spec": str(output_dir / "phase244_frozen_candidate_spec.csv"),
                "storage_decision_options": str(output_dir / "phase244_storage_decision_options.csv"),
                "future_holdout_contract": str(output_dir / "phase244_future_holdout_contract.csv"),
                "gate_evaluation": str(output_dir / "phase244_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase244_acceptance_summary.csv"),
                "report": str(output_dir / "phase244_future_holdout_precommit_report.md"),
            },
            random_seed="none_deterministic_precommit",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase235_training_discovery_event_bar_adapter_precommit_only",
        ),
    }
    (output_dir / "phase244_future_holdout_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase244 future holdout precommit.")
    parser.add_argument("--phase243-dir", type=Path, default=DEFAULT_PHASE243_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase243_dir=args.phase243_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
