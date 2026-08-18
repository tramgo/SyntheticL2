from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_ATTACHMENT = Path(r"c:\Users\Ramic\Downloads\cancel_included.txt")
DEFAULT_PHASE263_DIR = Path("outputs/phase263")
DEFAULT_PHASE300_DIR = Path("outputs/phase300")
DEFAULT_PHASE302_DIR = Path("outputs/phase302")
DEFAULT_PHASE403_DIR = Path("outputs/phase403")
DEFAULT_PHASE298_DIR = Path("outputs/phase298")
DEFAULT_EXISTING_REAL_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_UNSEEN_REAL_ROOT = Path("real_data_sample/l2_unseen_validation")
DEFAULT_OUTPUT_DIR = Path("outputs/phase407")

CHARTER_ID = "P407_CANCEL_LATENCY_MARKET_MAKER_REALISM"
NEXT_ACTION = "run_phase408_per_tick_cancel_race_market_maker_no_paper_live"
REPAIR_ACTION = "repair_phase407_cancel_latency_market_maker_precommit"

CANCEL_LATENCY_MS = [150, 250, 400, 700, 1000]
DECIDE_LATENCY_MS = [10, 20, 50]
MOVE_THRESHOLD_SPREAD_FRACTION = [0.25, 0.50, 0.75]
JITTER_SEED = 407_20260817
INITIAL_CAPITAL_INR = 1_000_000.0
FIXED_NOTIONAL_PER_SIDE_INR = 100_000.0
COST_MULTIPLIER = 2.0
MIN_ROUND_TRIPS = 30
MIN_TRADE_DATES = 5
MIN_SYMBOLS = 3
MIN_POSITIVE_DATE_FRACTION = 0.60
ANNUALIZED_THRESHOLD_PCT = 12.0


def sha256_frame(frame: pd.DataFrame) -> str:
    payload = frame.to_csv(index=False, lineterminator="\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def attachment_digest(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"present": 0, "bytes": 0, "sha256": "", "contains_cancel_race": 0, "contains_p407": 0}
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="replace").lower()
    return {
        "present": 1,
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "contains_cancel_race": int("cancel" in text and "race" in text),
        "contains_p407": int("p407" in text or "phase 407" in text),
    }


def real_anchor_dates(*roots: Path) -> list[str]:
    dates: set[str] = set()
    for root in roots:
        if not root.exists():
            continue
        for path in root.glob("trade_date=*"):
            if path.is_dir():
                dates.add(path.name.split("=", 1)[1])
    return sorted(dates)


def build_latency_grid() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for cancel_ms in CANCEL_LATENCY_MS:
        for decide_ms in DECIDE_LATENCY_MS:
            for move_frac in MOVE_THRESHOLD_SPREAD_FRACTION:
                rows.append(
                    {
                        "scenario_grid_id": f"P407_C{cancel_ms}_D{decide_ms}_M{str(move_frac).replace('.', 'p')}_J{JITTER_SEED}",
                        "cancel_latency_ms": cancel_ms,
                        "decide_latency_ms": decide_ms,
                        "move_threshold_spread_fraction": move_frac,
                        "jitter_seed": JITTER_SEED,
                        "jitter_distribution": "stable_truncated_lognormal_rtt_variance_proxy",
                        "maker_rebate_assumed": 0,
                        "cost_multiplier": COST_MULTIPLIER,
                    }
                )
    return pd.DataFrame(rows)


def build_charter(attachment_info: dict[str, Any], latency_hash: str) -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("charter_id", CHARTER_ID, "Phase407 cancel-latency retail two-sided quoting precommit."),
            ("attachment_sha256", attachment_info["sha256"], "Hash of the attached charter text."),
            ("status", "PRECOMMIT_NO_RESULTS_GENERATED", "Commit before generating cancel-race results."),
            ("scope", "retail_two_sided_quoting_with_honest_per_tick_cancel_race", "Reopens P263 only under material-new cancel-race machinery."),
            ("p263_relationship", "conservative_zero_cancel_closure_stands_until_this_test", "This strengthens or supersedes P263; it does not erase it."),
            ("p300_p302_relationship", "directional_passive_aware_closure_stands", "This does not reopen P302 directional microstructure closure."),
            ("p403_relationship", "material_new_full_depth_l2_thesis", "Per-tick cancel race is new machinery, not same-stack rescue."),
            ("raw_dense_input", "raw_synthetic_l2_dense_full_year_from_phase298", "Per-tick top-five market-by-price lake."),
            ("full_depth_requirement", "levels_1_to_5_price_quantity_orders_with_levels_2_to_5_signal", "No L1-only variants."),
            ("real_anchor_requirement", "at_least_3_verified_real_l2_anchor_days", "Reserve at least one anchor for cross-check."),
            ("latency_grid_hash", latency_hash, "Hash of precommitted latency grid."),
            ("cancel_latency_ms_allowed", ";".join(str(x) for x in CANCEL_LATENCY_MS), "No sub-100ms fantasy cancel latency."),
            ("decide_latency_ms_allowed", ";".join(str(x) for x in DECIDE_LATENCY_MS), "Trigger-to-decide latency grid."),
            ("move_threshold_spread_fraction_allowed", ";".join(str(x) for x in MOVE_THRESHOLD_SPREAD_FRACTION), "Cancel trigger threshold grid."),
            ("jitter_seed", JITTER_SEED, "Pinned deterministic jitter seed."),
            ("two_sided_required", 1, "Bid and ask must be live simultaneously in the quote window."),
            ("per_tick_loop_required", 1, "Forbidden to use P262 per-bar EV shortcut or P300 per-event fill draw."),
            ("cancel_race_required", 1, "Log cancel attempted, succeeded, and lost-race counts."),
            ("no_rebate", 1, "No maker rebate assumed."),
            ("cost_model", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha cost model."),
            ("cost_multiplier", COST_MULTIPLIER, "Cost200 scoring."),
            ("fixed_capital", INITIAL_CAPITAL_INR, "Fixed capital denominator."),
            ("fixed_notional_per_side", FIXED_NOTIONAL_PER_SIDE_INR, "Per-side notional at retail scale."),
            ("acceptance_round_trips", MIN_ROUND_TRIPS, "Completed round-trip floor."),
            ("acceptance_date_breadth", MIN_TRADE_DATES, "Minimum distinct dates."),
            ("acceptance_symbol_breadth", MIN_SYMBOLS, "Minimum distinct symbols."),
            ("acceptance_positive_date_fraction", MIN_POSITIVE_DATE_FRACTION, "Minimum positive date fraction."),
            ("acceptance_annualized_pct", ANNUALIZED_THRESHOLD_PCT, "Cost200 fixed-capital annualized floor."),
            ("strategy_replay_allowed", 0, "Boundary remains closed."),
            ("strategy_promotion_allowed", 0, "Boundary remains closed."),
            ("paper_or_live_acceptance_allowed", 0, "Boundary remains closed."),
            ("deployable_profitability_claim_allowed", 0, "Boundary remains closed."),
        ],
        columns=["charter_item", "value", "description"],
    )


def build_input_registry(
    phase298: pd.DataFrame,
    phase298_schema: pd.DataFrame,
    phase300: pd.DataFrame,
    phase302: pd.DataFrame,
    phase403: pd.DataFrame,
    anchor_dates: list[str],
) -> pd.DataFrame:
    schema_present = 0
    if not phase298_schema.empty and "book_level_present_columns" in phase298_schema.columns:
        schema_present = int(pd.to_numeric(phase298_schema["book_level_present_columns"], errors="coerce").fillna(0).min())
    return pd.DataFrame(
        [
            ("phase298_dense_root", metric_value(phase298, "phase298_dense_root", ""), "Raw dense source root."),
            ("phase298_raw_book_state_l1_l5_required", metric_value(phase298, "phase298_raw_book_state_l1_l5_required", ""), "Full-depth source requirement."),
            ("phase298_levels_2_to_5_required", metric_value(phase298, "phase298_levels_2_to_5_required", ""), "Levels 2-5 materiality."),
            ("phase298_l1_only_variant_rows", metric_value(phase298, "phase298_l1_only_variant_rows", ""), "Must be zero."),
            ("phase298_net_edge_live_mask_rows", metric_value(phase298, "phase298_net_edge_live_mask_rows", ""), "Must be zero."),
            ("phase298_schema_present_columns_min", schema_present, "Minimum present L1-L5 price/quantity/order columns in Phase298 schema audit."),
            ("phase300_cost200_survivors", metric_value(phase300, "phase300_cost200_acceptance_survivor_rows", ""), "P300 closure context."),
            ("phase302_do_not_continue_same_route", metric_value(phase302, "phase302_do_not_continue_same_route", ""), "Directional route closure context."),
            ("phase403_material_new_thesis_required", metric_value(phase403, "phase403_material_new_thesis_required", ""), "P403 requirement."),
            ("real_anchor_dates", ";".join(anchor_dates), "Verified local real L2 anchor dates."),
            ("real_anchor_date_count", len(anchor_dates), "At least 3 required."),
            ("execution_results_generated_now", 0, "Precommit only."),
        ],
        columns=["input_id", "value", "description"],
    )


def build_hard_gate_contract() -> pd.DataFrame:
    gates = [
        ("MM_INPUTS_VALIDATED", "all five inputs present and schema checked"),
        ("MM_TICK_LOOP_PRESENT", "per-tick loop over resting quote window"),
        ("MM_CANCEL_RACE_APPLIED", "cancel-attempted cancel-succeeded cancel-lost-race counts logged"),
        ("MM_LATENCY_HONEST", "cancel_latency_ms >= 150 in every scenario"),
        ("MM_NO_REBATE_ASSUMED", "full Zerodha charges, no maker rebate"),
        ("MM_TWO_SIDED_REQUIRED", "bid and ask live simultaneously"),
        ("MM_FULL_DEPTH_L2_L5", "at least one signal from levels 2-5"),
        ("MM_NO_LOOKAHEAD", "feature timestamps precede quote-post timestamps and loop is time ordered"),
        ("MM_COST200_SCORING", "cost_multiplier=2, fixed capital, per-side notional <= 100000"),
        ("MM_EVENT_FLOOR", "at least 30 completed round trips"),
        ("MM_DATE_BREADTH", "at least 5 trade dates with round trips"),
        ("MM_SYMBOL_BREADTH", "at least 3 symbols with round trips"),
        ("MM_POSITIVE_DATE_FRACTION", "at least 60 percent positive round-trip dates"),
        ("MM_ANNUALIZED_FLOOR", "fixed-capital annualized return >= 12 percent at cost200"),
        ("MM_NO_RANK_REVERSAL", "best cost200 scenario remains top quartile at cost100"),
        ("MM_LATENCY_MONOTONICITY", "net PnL decreases as cancel latency increases for winner"),
        ("MM_REAL_ANCHOR_CROSS_CHECK", "winning scenario sign preserved on reserved real anchor day"),
        ("MM_BOUNDARIES_CLOSED", "replay=0 promotion=0 paper_live=0 claim=0"),
    ]
    return pd.DataFrame(
        [{"gate_id": gate, "requirement": requirement, "severity": "hard", "phase407_precommitted": 1} for gate, requirement in gates]
    )


def build_gate_evaluation(attachment_info: dict[str, Any], inputs: pd.DataFrame, latency_grid: pd.DataFrame, hard_contract: pd.DataFrame) -> pd.DataFrame:
    input_value = dict(zip(inputs["input_id"], inputs["value"]))
    anchor_count = as_int(input_value.get("real_anchor_date_count", 0))
    schema_cols = as_int(input_value.get("phase298_schema_present_columns_min", 0))
    cancel_min = int(pd.to_numeric(latency_grid["cancel_latency_ms"], errors="coerce").min())
    gates = [
        ("P407_ATTACHMENT_PRESENT", attachment_info["present"] == 1, attachment_info["present"], 1),
        ("P407_ATTACHMENT_CANCEL_RACE_CHARTER", attachment_info["contains_cancel_race"] == 1 and attachment_info["contains_p407"] == 1, f"cancel_race={attachment_info['contains_cancel_race']};p407={attachment_info['contains_p407']}", "cancel_race_p407"),
        ("P407_PHASE298_RAW_DENSE_PRESENT", str(input_value.get("phase298_dense_root", "")) == "raw_synthetic_l2_dense_full_year", input_value.get("phase298_dense_root", ""), "raw_synthetic_l2_dense_full_year"),
        ("P407_FULL_DEPTH_SCHEMA_PRESENT", schema_cols >= 30, schema_cols, ">=30"),
        ("P407_L1_ONLY_FORBIDDEN", as_int(input_value.get("phase298_l1_only_variant_rows", 1)) == 0, input_value.get("phase298_l1_only_variant_rows", ""), 0),
        ("P407_NO_LOOKAHEAD_SOURCE", as_int(input_value.get("phase298_net_edge_live_mask_rows", 1)) == 0, input_value.get("phase298_net_edge_live_mask_rows", ""), 0),
        ("P407_REAL_ANCHORS_AT_LEAST_THREE", anchor_count >= 3, anchor_count, ">=3"),
        ("P407_LATENCY_GRID_PINNED", len(latency_grid) == 45, len(latency_grid), 45),
        ("P407_LATENCY_HONEST", cancel_min >= 150, cancel_min, ">=150"),
        ("P407_NO_REBATE_PINNED", int(latency_grid["maker_rebate_assumed"].astype(int).sum()) == 0, int(latency_grid["maker_rebate_assumed"].astype(int).sum()), 0),
        ("P407_COST200_FIXED_CAPITAL_PINNED", COST_MULTIPLIER == 2.0 and INITIAL_CAPITAL_INR >= 1_000_000.0 and FIXED_NOTIONAL_PER_SIDE_INR <= 100_000.0, f"cost={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR};notional={FIXED_NOTIONAL_PER_SIDE_INR}", "cost200_fixed_capital"),
        ("P407_ALL_MM_HARD_GATES_PRECOMMITTED", len(hard_contract) == 18, len(hard_contract), 18),
        ("P407_RESULTS_NOT_GENERATED", as_int(input_value.get("execution_results_generated_now", 1)) == 0, input_value.get("execution_results_generated_now", ""), 0),
        ("P407_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(charter: pd.DataFrame, inputs: pd.DataFrame, latency_grid: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase407_cancel_latency_market_maker_precommit_complete", 1, "Phase407 precommit completed"),
            ("phase407_charter_id", CHARTER_ID, "Charter id"),
            ("phase407_latency_grid_rows", len(latency_grid), "Precommitted latency grid rows"),
            ("phase407_latency_grid_hash", str(charter.loc[charter["charter_item"].eq("latency_grid_hash"), "value"].iloc[0]), "Latency grid hash"),
            ("phase407_jitter_seed", JITTER_SEED, "Pinned jitter seed"),
            ("phase407_real_anchor_date_count", inputs.loc[inputs["input_id"].eq("real_anchor_date_count"), "value"].iloc[0], "Local real anchor dates"),
            ("phase407_per_tick_cancel_race_required", 1, "Phase408 must implement per-tick loop"),
            ("phase407_sub100ms_latency_forbidden", 1, "No cancel latency below 100 ms"),
            ("phase407_maker_rebate_assumed", 0, "No maker rebate"),
            ("phase407_cost_multiplier", COST_MULTIPLIER, "Cost200"),
            ("phase407_initial_capital_inr", INITIAL_CAPITAL_INR, "Fixed capital"),
            ("phase407_fixed_notional_per_side_inr", FIXED_NOTIONAL_PER_SIDE_INR, "Per-side notional"),
            ("phase407_results_generated", 0, "Precommit only"),
            ("phase407_strategy_promotion_allowed", 0, "No promotion"),
            ("phase407_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase407_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase407_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase407_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase407_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, charter: pd.DataFrame, inputs: pd.DataFrame, latency_grid: pd.DataFrame, hard_contract: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase407 Cancel-Latency Market-Maker Realism Precommit",
        "",
        "Phase407 records the attached cancel-race charter before any result generation.",
        "",
        "It reopens the retail two-sided quoting family only as a material-new, per-tick cancel-race simulator. It does not reopen the P302 directional route and it assumes no maker rebate.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Charter",
        "",
        _markdown_table(charter),
        "",
        "## Input Registry",
        "",
        _markdown_table(inputs),
        "",
        "## Latency Grid",
        "",
        _markdown_table(latency_grid.head(60)),
        "",
        "## Execution Hard-Gate Contract",
        "",
        _markdown_table(hard_contract),
        "",
        "## Precommit Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "No Phase407 execution results are generated by this precommit.",
    ]
    (output_dir / "phase407_cancel_latency_market_maker_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    attachment: Path = DEFAULT_ATTACHMENT,
    phase263_dir: Path = DEFAULT_PHASE263_DIR,
    phase300_dir: Path = DEFAULT_PHASE300_DIR,
    phase302_dir: Path = DEFAULT_PHASE302_DIR,
    phase403_dir: Path = DEFAULT_PHASE403_DIR,
    phase298_dir: Path = DEFAULT_PHASE298_DIR,
    existing_real_root: Path = DEFAULT_EXISTING_REAL_ROOT,
    unseen_real_root: Path = DEFAULT_UNSEEN_REAL_ROOT,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    attachment_info = attachment_digest(attachment)
    phase298 = read_csv(phase298_dir / "phase298_acceptance_summary.csv")
    phase298_schema = read_csv(phase298_dir / "phase298_raw_book_schema_audit.csv")
    phase300 = read_csv(phase300_dir / "phase300_acceptance_summary.csv")
    phase302 = read_csv(phase302_dir / "phase302_acceptance_summary.csv")
    phase403 = read_csv(phase403_dir / "phase403_acceptance_summary.csv")
    if phase298.empty or phase300.empty or phase302.empty or phase403.empty:
        raise FileNotFoundError("Phase407 requires Phase298, Phase300, Phase302 and Phase403 summaries.")
    latency_grid = build_latency_grid()
    latency_hash = sha256_frame(latency_grid)
    anchors = real_anchor_dates(existing_real_root, unseen_real_root)
    charter = build_charter(attachment_info, latency_hash)
    inputs = build_input_registry(phase298, phase298_schema, phase300, phase302, phase403, anchors)
    hard_contract = build_hard_gate_contract()
    gates = build_gate_evaluation(attachment_info, inputs, latency_grid, hard_contract)
    acceptance = build_acceptance(charter, inputs, latency_grid, gates)

    charter.to_csv(output_dir / "phase407_cancel_latency_charter.csv", index=False)
    latency_grid.to_csv(output_dir / "phase407_latency_grid.csv", index=False)
    inputs.to_csv(output_dir / "phase407_input_registry.csv", index=False)
    hard_contract.to_csv(output_dir / "phase407_execution_hard_gate_contract.csv", index=False)
    gates.to_csv(output_dir / "phase407_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase407_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, charter, inputs, latency_grid, hard_contract, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase407_cancel_latency_market_maker_precommit",
        **reproducibility_fields(
            artifact_id="phase407_cancel_latency_market_maker_precommit",
            generated_utc=generated_utc,
            inputs={
                "attachment": str(attachment),
                "phase298_acceptance_summary": str(phase298_dir / "phase298_acceptance_summary.csv"),
                "phase298_schema": str(phase298_dir / "phase298_raw_book_schema_audit.csv"),
                "phase300_acceptance_summary": str(phase300_dir / "phase300_acceptance_summary.csv"),
                "phase302_acceptance_summary": str(phase302_dir / "phase302_acceptance_summary.csv"),
                "phase403_acceptance_summary": str(phase403_dir / "phase403_acceptance_summary.csv"),
            },
            parameters={
                "charter_id": CHARTER_ID,
                "latency_grid_hash": latency_hash,
                "jitter_seed": JITTER_SEED,
                "results_generated": 0,
                "next_action": NEXT_ACTION,
            },
            outputs={"acceptance_summary": str(output_dir / "phase407_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase407_precommitted_cancel_latency_grid",
        ),
    }
    (output_dir / "phase407_cancel_latency_market_maker_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase407 cancel-latency market-maker realism precommit.")
    parser.add_argument("--attachment", type=Path, default=DEFAULT_ATTACHMENT)
    parser.add_argument("--phase263-dir", type=Path, default=DEFAULT_PHASE263_DIR)
    parser.add_argument("--phase300-dir", type=Path, default=DEFAULT_PHASE300_DIR)
    parser.add_argument("--phase302-dir", type=Path, default=DEFAULT_PHASE302_DIR)
    parser.add_argument("--phase403-dir", type=Path, default=DEFAULT_PHASE403_DIR)
    parser.add_argument("--phase298-dir", type=Path, default=DEFAULT_PHASE298_DIR)
    parser.add_argument("--existing-real-root", type=Path, default=DEFAULT_EXISTING_REAL_ROOT)
    parser.add_argument("--unseen-real-root", type=Path, default=DEFAULT_UNSEEN_REAL_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(
        args.attachment,
        args.phase263_dir,
        args.phase300_dir,
        args.phase302_dir,
        args.phase403_dir,
        args.phase298_dir,
        args.existing_real_root,
        args.unseen_real_root,
        args.output_dir,
    )
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()
