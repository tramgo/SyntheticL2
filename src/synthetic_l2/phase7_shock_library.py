from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


COUNTERFACTUAL_VARIANTS = [
    "no_shock",
    "positive_shock",
    "negative_shock",
    "quick_recovery",
    "continuation",
]

MARKET_SHOCK_BY_REGIME = {
    "D05": "relief_rally",
    "D07": "broad_risk_off",
    "D08": "global_overnight_gap",
    "D09": "global_overnight_gap_fade",
    "D10": "global_overnight_gap_down",
    "D11": "gap_down_recovery",
    "D12": "scheduled_event_decision",
    "D13": "liquidity_stress_episode",
    "D14": "expiry_like_flow",
    "D16": "index_dominated_flow",
    "D20": "shock_and_normalize",
}

TICKER_SHOCK_TYPES = [
    "earnings_beat",
    "earnings_miss",
    "guidance_change",
    "regulatory_action",
    "block_volume_burst",
    "headline_rumor_reversal",
    "liquidity_disappearance",
    "sharp_move_absorption",
    "false_breakout_depth_withdrawal",
]

SYMBOLS = [
    "ADANIPORTS",
    "AXISBANK",
    "BAJAJ-AUTO",
    "BANKBEES",
    "BHARTIARTL",
    "BPCL",
    "BRITANNIA",
    "CIPLA",
    "DRREDDY",
    "GOLDBEES",
    "HCLTECH",
    "HDFCBANK",
    "HINDUNILVR",
    "ICICIBANK",
    "INFY",
    "ITBEES",
    "ITC",
    "JUNIORBEES",
    "KOTAKBANK",
    "LT",
    "M&M",
    "MARUTI",
    "NESTLEIND",
    "NIFTYBEES",
    "ONGC",
    "RELIANCE",
    "SBIN",
    "SUNPHARMA",
    "TCS",
    "TECHM",
    "ULTRACEMCO",
    "WIPRO",
]


def load_inputs(phase4_dir: Path, phase6_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    calendar = pd.read_csv(phase4_dir / "scenario_calendar.csv")
    book_summary = pd.read_csv(phase6_dir / "l2_book_summary.csv")
    return calendar, book_summary


def event_time_for(regime_code: str, rng: random.Random, variant: str) -> tuple[str, int]:
    if regime_code in {"D08", "D09", "D10", "D11"}:
        return "09:15:00", rng.choice([15, 30, 45])
    if regime_code in {"D14"}:
        return rng.choice(["14:45:00", "15:00:00", "15:15:00"]), rng.choice([20, 30, 45])
    if regime_code in {"D12", "D20"}:
        return rng.choice(["10:30:00", "11:45:00", "13:15:00", "14:00:00"]), rng.choice([30, 45, 60, 90])
    if variant == "quick_recovery":
        return rng.choice(["10:00:00", "12:30:00", "14:30:00"]), rng.choice([15, 20, 30])
    return rng.choice(["09:45:00", "10:45:00", "12:15:00", "13:45:00", "14:45:00"]), rng.choice([20, 30, 45, 60])


def base_direction(regime_code: str, variant: str) -> int:
    if variant == "no_shock":
        return 0
    if variant == "positive_shock":
        return 1
    if variant == "negative_shock":
        return -1
    if regime_code in {"D05", "D08", "D11"}:
        return 1
    if regime_code in {"D07", "D10", "D13", "D20"}:
        return -1
    return 1 if variant == "continuation" else -1


def parameterize_event(regime_code: str, scope: str, variant: str, rng: random.Random, day: pd.Series) -> dict:
    direction = base_direction(regime_code, variant)
    if variant == "no_shock":
        magnitude = 0.0
        vol_mult = 1.0
        event_mult = 1.0
        spread_mult = 1.0
        depth_bid = 1.0
        depth_ask = 1.0
        flow_bias = 0.0
    else:
        stress = float(day.get("vol_multiplier", 1.0))
        magnitude = direction * rng.uniform(8, 75) * stress
        if regime_code in {"D07", "D20"}:
            magnitude *= 1.5
        if scope == "ticker":
            magnitude *= rng.uniform(0.7, 1.8)
        vol_mult = rng.uniform(1.3, 3.0) * stress
        event_mult = rng.uniform(1.2, 2.8) * float(day.get("event_rate_multiplier", 1.0))
        spread_mult = rng.uniform(1.1, 2.5) * float(day.get("spread_multiplier", 1.0))
        if direction < 0:
            depth_bid = rng.uniform(0.35, 0.80) * float(day.get("depth_multiplier", 1.0))
            depth_ask = rng.uniform(0.75, 1.20) * float(day.get("depth_multiplier", 1.0))
        elif direction > 0:
            depth_bid = rng.uniform(0.75, 1.20) * float(day.get("depth_multiplier", 1.0))
            depth_ask = rng.uniform(0.35, 0.80) * float(day.get("depth_multiplier", 1.0))
        else:
            depth_bid = depth_ask = float(day.get("depth_multiplier", 1.0))
        flow_bias = direction * rng.uniform(0.25, 0.85)

    if variant == "quick_recovery":
        recovery_half_life = rng.choice([5, 10, 15])
        reversal_probability = rng.uniform(0.55, 0.85)
        drift_after_jump = -0.6 * magnitude
    elif variant == "continuation":
        recovery_half_life = rng.choice([45, 60, 90, 120])
        reversal_probability = rng.uniform(0.05, 0.25)
        drift_after_jump = 0.45 * magnitude
    else:
        recovery_half_life = rng.choice([15, 30, 45, 60])
        reversal_probability = rng.uniform(0.20, 0.55)
        drift_after_jump = rng.uniform(-0.2, 0.2) * magnitude

    start_time, duration = event_time_for(regime_code, rng, variant)
    return {
        "start_time": start_time,
        "duration_minutes": duration,
        "price_jump_bps": round(magnitude, 4),
        "drift_after_jump_bps": round(drift_after_jump, 4),
        "volatility_multiplier": round(vol_mult, 4),
        "event_rate_multiplier": round(event_mult, 4),
        "spread_multiplier": round(spread_mult, 4),
        "depth_multiplier_bid": round(depth_bid, 4),
        "depth_multiplier_ask": round(depth_ask, 4),
        "buy_sell_flow_bias": round(flow_bias, 4),
        "correlation_multiplier": round(float(day.get("correlation_multiplier", 1.0)) * (1.0 if variant == "no_shock" else rng.uniform(1.0, 1.8)), 4),
        "recovery_half_life_minutes": recovery_half_life,
        "reversal_probability": round(reversal_probability, 4),
    }


def required_l2_effects(shock_type: str, direction: int) -> str:
    if "risk_off" in shock_type or direction < 0:
        return "bid withdrawal;sell sweep;spread widening;high event intensity;depth recovery"
    if "gap" in shock_type:
        return "opening price discovery;spread widening;volume burst;normalization"
    if "liquidity" in shock_type:
        return "visible depth thinning;spread widening;stale pockets;replenishment test"
    if "event" in shock_type or "decision" in shock_type:
        return "pre-event lull;two-sided volatility;directional follow-through or fade"
    return "ask depletion;buy trade burst;spread widening;normalization"


def generate_events(calendar: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict] = []
    candidate_days = calendar[(calendar["is_market_shock_day"]) | (calendar["event_cluster"]) | (calendar["shock_symbol_count"] > 0)].copy()
    for day in candidate_days.itertuples(index=False):
        day_series = pd.Series(day._asdict())
        rng = random.Random(int(day.seed) * 100003 + int(day.scenario_day))
        regime_code = str(day.regime_code)
        shock_symbols = [symbol for symbol in str(day.shock_symbols).split("|") if symbol and symbol != "nan"]
        market_shock_type = MARKET_SHOCK_BY_REGIME.get(regime_code, "sudden_macro_surprise")
        counterfactual_group = f"{day.quarter_profile}-{int(day.scenario_day):03d}-{regime_code}"

        if bool(day.is_market_shock_day) or bool(day.event_cluster):
            for variant in COUNTERFACTUAL_VARIANTS:
                params = parameterize_event(regime_code, "market", variant, rng, day_series)
                direction = base_direction(regime_code, variant)
                rows.append(
                    {
                        "shock_id": f"{counterfactual_group}-M-{variant}",
                        "counterfactual_group": counterfactual_group,
                        "variant": variant,
                        "quarter_profile": day.quarter_profile,
                        "scenario_day": int(day.scenario_day),
                        "trade_date": day.trade_date,
                        "regime_code": regime_code,
                        "regime_family": day.regime_family,
                        "scope": "market",
                        "target": "ALL",
                        "shock_type": market_shock_type,
                        "required_l2_effects": required_l2_effects(market_shock_type, direction),
                        "evidence_label": "synthetic_shock_design",
                        **params,
                    }
                )

        for symbol_index, symbol in enumerate(shock_symbols):
            shock_type = TICKER_SHOCK_TYPES[(symbol_index + int(day.scenario_day)) % len(TICKER_SHOCK_TYPES)]
            for variant in ["positive_shock", "negative_shock", "quick_recovery", "continuation"]:
                params = parameterize_event(regime_code, "ticker", variant, rng, day_series)
                direction = base_direction(regime_code, variant)
                rows.append(
                    {
                        "shock_id": f"{counterfactual_group}-T-{symbol}-{variant}",
                        "counterfactual_group": f"{counterfactual_group}-{symbol}",
                        "variant": variant,
                        "quarter_profile": day.quarter_profile,
                        "scenario_day": int(day.scenario_day),
                        "trade_date": day.trade_date,
                        "regime_code": regime_code,
                        "regime_family": day.regime_family,
                        "scope": "ticker",
                        "target": symbol,
                        "shock_type": shock_type,
                        "required_l2_effects": required_l2_effects(shock_type, direction),
                        "evidence_label": "synthetic_shock_design",
                        **params,
                    }
                )
    existing_targets = {row["target"] for row in rows if row["scope"] == "ticker"}
    missing_targets = [symbol for symbol in SYMBOLS if symbol not in existing_targets]
    supplement_days = calendar[calendar["regime_code"].isin(["D12", "D17", "D18", "D19"])].copy()
    if supplement_days.empty:
        supplement_days = candidate_days
    for symbol_index, symbol in enumerate(missing_targets):
        day = supplement_days.iloc[symbol_index % len(supplement_days)]
        rng = random.Random(int(day["seed"]) * 100003 + int(day["scenario_day"]) + sum(ord(ch) for ch in symbol))
        regime_code = str(day["regime_code"])
        counterfactual_group = f"{day['quarter_profile']}-{int(day['scenario_day']):03d}-{regime_code}-{symbol}-coverage"
        shock_type = TICKER_SHOCK_TYPES[symbol_index % len(TICKER_SHOCK_TYPES)]
        for variant in ["positive_shock", "negative_shock", "quick_recovery", "continuation"]:
            params = parameterize_event(regime_code, "ticker", variant, rng, day)
            direction = base_direction(regime_code, variant)
            rows.append(
                {
                    "shock_id": f"{counterfactual_group}-T-{variant}",
                    "counterfactual_group": counterfactual_group,
                    "variant": variant,
                    "quarter_profile": day["quarter_profile"],
                    "scenario_day": int(day["scenario_day"]),
                    "trade_date": day["trade_date"],
                    "regime_code": regime_code,
                    "regime_family": day["regime_family"],
                    "scope": "ticker",
                    "target": symbol,
                    "shock_type": shock_type,
                    "required_l2_effects": required_l2_effects(shock_type, direction),
                    "evidence_label": "synthetic_shock_design_coverage_supplement",
                    **params,
                }
            )
    return pd.DataFrame(rows)


def build_summary(events: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    by_type = events.groupby(["scope", "shock_type", "variant"], sort=True).agg(
        events=("shock_id", "count"),
        median_abs_jump_bps=("price_jump_bps", lambda value: value.abs().median()),
        median_volatility_multiplier=("volatility_multiplier", "median"),
        median_spread_multiplier=("spread_multiplier", "median"),
    ).reset_index()
    by_day = events.groupby(["quarter_profile", "scenario_day", "trade_date", "regime_code"], sort=True).agg(
        events=("shock_id", "count"),
        market_events=("scope", lambda value: int((value == "market").sum())),
        ticker_events=("scope", lambda value: int((value == "ticker").sum())),
        targets=("target", lambda value: "|".join(sorted(set(v for v in value if v != "ALL")))[:1000]),
    ).reset_index()
    return by_type, by_day


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    text_frame = frame.copy()
    for column in text_frame.columns:
        text_frame[column] = text_frame[column].map(lambda value: "" if pd.isna(value) else str(value))
    headers = [str(column) for column in text_frame.columns]
    rows = text_frame.values.tolist()
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def validate_events(events: pd.DataFrame) -> dict:
    return {
        "shock_events": int(len(events)),
        "market_events": int((events["scope"] == "market").sum()),
        "ticker_events": int((events["scope"] == "ticker").sum()),
        "counterfactual_groups": int(events["counterfactual_group"].nunique()),
        "scenario_days": int(events[["quarter_profile", "scenario_day"]].drop_duplicates().shape[0]),
        "target_symbols": int(events.loc[events["scope"] == "ticker", "target"].nunique()),
        "variants": int(events["variant"].nunique()),
        "null_required_effect_rows": int(events["required_l2_effects"].isna().sum()),
        "invalid_duration_rows": int((events["duration_minutes"] <= 0).sum()),
    }


def write_report(output_dir: Path, validation: dict, by_type: pd.DataFrame, by_day: pd.DataFrame) -> None:
    lines = [
        "# Phase 7 Shock Library Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase generates a synthetic shock/event schedule with required L2 effects and counterfactual variants.",
        "It does not yet mutate the Phase 6 book-state stream; Phase 8+ can consume these events.",
        "",
        "## Validation",
        "",
        *(f"- {key}: {value}" for key, value in validation.items()),
        "",
        "## Top Shock-Type Rows",
        "",
        _markdown_table(by_type.sort_values("events", ascending=False).head(12)),
        "",
        "## Most Populated Scenario Days",
        "",
        _markdown_table(by_day.sort_values("events", ascending=False).head(12)),
        "",
        "## Outputs",
        "",
        "- `shock_library.csv`",
        "- `shock_library.jsonl`",
        "- `shock_type_summary.csv`",
        "- `shock_day_summary.csv`",
        "- `shock_library_manifest.json`",
        "",
    ]
    (output_dir / "phase7_shock_library_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase7(phase4_dir: Path, phase6_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    calendar, book_summary = load_inputs(phase4_dir, phase6_dir)
    events = generate_events(calendar)
    by_type, by_day = build_summary(events)
    validation = validate_events(events)
    events.to_csv(output_dir / "shock_library.csv", index=False)
    events.to_json(output_dir / "shock_library.jsonl", orient="records", lines=True)
    by_type.to_csv(output_dir / "shock_type_summary.csv", index=False)
    by_day.to_csv(output_dir / "shock_day_summary.csv", index=False)
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "phase4_dir": str(phase4_dir),
        "phase6_dir": str(phase6_dir),
        "phase6_book_event_labels": sorted(book_summary["book_event_label"].unique().tolist()) if "book_event_label" in book_summary else [],
        "validation": validation,
        "evidence_scope": "synthetic_shock_event_design",
    }
    (output_dir / "shock_library_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, validation, by_type, by_day)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Phase 7 synthetic event and shock library.")
    parser.add_argument("--phase4-dir", type=Path, default=Path("outputs/phase4"))
    parser.add_argument("--phase6-dir", type=Path, default=Path("outputs/phase6"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase7"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase7(args.phase4_dir, args.phase6_dir, args.output_dir)


if __name__ == "__main__":
    main()
