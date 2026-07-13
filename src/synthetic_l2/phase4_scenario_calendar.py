from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


REGIME_FAMILIES = {
    "D01": "Normal balanced",
    "D02": "Low-volatility sideways",
    "D03": "High-volatility sideways",
    "D04": "Gradual bullish trend",
    "D05": "Strong rally",
    "D06": "Gradual bearish trend",
    "D07": "Sell-off/panic",
    "D08": "Gap-up continuation",
    "D09": "Gap-up fade",
    "D10": "Gap-down continuation",
    "D11": "Gap-down recovery",
    "D12": "Event day",
    "D13": "Liquidity-stressed",
    "D14": "Expiry-like",
    "D15": "Rotation day",
    "D16": "Index-dominated day",
    "D17": "Stock-specific dispersion",
    "D18": "False-breakout day",
    "D19": "Trend reversal day",
    "D20": "Shock-and-normalize",
}


BASE_TYPICAL_COUNTS = {
    "D01": 12,
    "D02": 7,
    "D03": 5,
    "D04": 6,
    "D05": 3,
    "D06": 5,
    "D07": 3,
    "D08": 2,
    "D09": 1,
    "D10": 2,
    "D11": 1,
    "D12": 5,
    "D15": 2,
    "D17": 2,
    "D18": 3,
    "D19": 2,
    "D13": 1,
    "D20": 1,
}

SEED_PROFILES = {
    "Q-A": {
        "seed": 4101,
        "description": "typical mix",
        "counts": BASE_TYPICAL_COUNTS,
    },
    "Q-B": {
        "seed": 4102,
        "description": "bullish/high-momentum",
        "counts": {
            **BASE_TYPICAL_COUNTS,
            "D01": 9,
            "D02": 5,
            "D03": 4,
            "D04": 10,
            "D05": 7,
            "D06": 3,
            "D07": 1,
            "D08": 4,
            "D09": 1,
            "D10": 1,
            "D11": 1,
            "D12": 5,
            "D15": 3,
            "D17": 2,
            "D18": 3,
            "D19": 2,
            "D13": 1,
            "D20": 1,
        },
    },
    "Q-C": {
        "seed": 4103,
        "description": "stressed/volatile",
        "counts": {
            **BASE_TYPICAL_COUNTS,
            "D01": 5,
            "D02": 3,
            "D03": 8,
            "D04": 4,
            "D05": 2,
            "D06": 7,
            "D07": 6,
            "D08": 1,
            "D09": 2,
            "D10": 3,
            "D11": 1,
            "D12": 5,
            "D15": 3,
            "D17": 3,
            "D18": 4,
            "D19": 2,
            "D13": 2,
            "D20": 2,
        },
    },
}

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


@dataclass(frozen=True)
class DayParams:
    vol_multiplier: float
    event_rate_multiplier: float
    spread_multiplier: float
    depth_multiplier: float
    correlation_multiplier: float
    shock_probability: float
    gap_probability: float


PARAMS_BY_REGIME = {
    "D01": DayParams(1.00, 1.00, 1.00, 1.00, 1.00, 0.02, 0.01),
    "D02": DayParams(0.65, 0.80, 0.85, 1.05, 0.80, 0.01, 0.00),
    "D03": DayParams(1.45, 1.15, 1.20, 0.95, 1.05, 0.05, 0.02),
    "D04": DayParams(1.10, 1.10, 1.00, 1.00, 1.10, 0.03, 0.01),
    "D05": DayParams(1.65, 1.35, 1.10, 0.90, 1.35, 0.07, 0.04),
    "D06": DayParams(1.15, 1.10, 1.05, 0.95, 1.15, 0.04, 0.01),
    "D07": DayParams(2.20, 1.55, 1.75, 0.65, 1.70, 0.20, 0.10),
    "D08": DayParams(1.35, 1.20, 1.05, 0.95, 1.20, 0.05, 0.35),
    "D09": DayParams(1.45, 1.20, 1.15, 0.90, 1.10, 0.06, 0.35),
    "D10": DayParams(1.55, 1.30, 1.25, 0.85, 1.30, 0.08, 0.35),
    "D11": DayParams(1.50, 1.25, 1.20, 0.90, 1.20, 0.06, 0.35),
    "D12": DayParams(1.60, 1.35, 1.25, 0.85, 1.20, 0.18, 0.05),
    "D13": DayParams(1.35, 0.80, 2.00, 0.50, 0.90, 0.08, 0.02),
    "D14": DayParams(1.35, 1.60, 1.25, 0.80, 1.20, 0.07, 0.02),
    "D15": DayParams(1.15, 1.10, 1.05, 1.00, 0.65, 0.04, 0.01),
    "D16": DayParams(1.25, 1.20, 1.05, 0.95, 1.45, 0.06, 0.02),
    "D17": DayParams(1.25, 1.15, 1.10, 0.95, 0.55, 0.08, 0.01),
    "D18": DayParams(1.40, 1.20, 1.15, 0.90, 0.85, 0.06, 0.02),
    "D19": DayParams(1.50, 1.25, 1.15, 0.90, 1.00, 0.07, 0.02),
    "D20": DayParams(2.00, 1.45, 1.60, 0.70, 1.55, 0.30, 0.05),
}


def load_observed_anchor(phase3_dir: Path) -> dict:
    path = phase3_dir / "daily_regime_observation.csv"
    if not path.exists():
        return {"observed_regime_code": None, "observed_regime": None}
    frame = pd.read_csv(path)
    if frame.empty:
        return {"observed_regime_code": None, "observed_regime": None}
    row = frame.iloc[0]
    return {
        "observed_regime_code": row.get("daily_regime_code"),
        "observed_regime": row.get("daily_regime"),
        "observed_regime_evidence_label": row.get("evidence_label"),
    }


def load_ticker_states(phase3_dir: Path) -> dict[str, str]:
    path = phase3_dir / "ticker_state_profile.csv"
    if not path.exists():
        return {}
    frame = pd.read_csv(path)
    return dict(zip(frame["symbol"], frame["ticker_state"]))


def expand_regime_counts(counts: dict[str, int]) -> list[str]:
    regimes: list[str] = []
    for code, count in counts.items():
        regimes.extend([code] * int(count))
    if len(regimes) != 63:
        raise ValueError(f"Scenario profile must contain exactly 63 days, got {len(regimes)}")
    return regimes


def business_dates(start_date: str, periods: int) -> list[pd.Timestamp]:
    return list(pd.bdate_range(start=start_date, periods=periods))


def choose_shock_symbols(rng: random.Random, regime_code: str, ticker_states: dict[str, str]) -> list[str]:
    if regime_code in {"D07", "D16", "D20"}:
        count = rng.randint(8, 18)
    elif regime_code in {"D12", "D15", "D17", "D18", "D19"}:
        count = rng.randint(2, 6)
    elif regime_code == "D13":
        count = rng.randint(4, 10)
    else:
        count = rng.randint(0, 3)

    stress_names = [symbol for symbol, state in ticker_states.items() if state in {"illiquid/stale", "spread stress", "laggard"}]
    pool = stress_names + [symbol for symbol in SYMBOLS if symbol not in stress_names]
    selected: list[str] = []
    for symbol in pool:
        if symbol not in selected:
            selected.append(symbol)
        if len(selected) >= count:
            break
    if len(selected) < count:
        selected = rng.sample(SYMBOLS, min(count, len(SYMBOLS)))
    return selected


def intraday_template(regime_code: str) -> str:
    if regime_code in {"D07", "D20"}:
        return "shock_liquidity_recovery"
    if regime_code in {"D08", "D09", "D10", "D11"}:
        return "gap_open_then_path"
    if regime_code in {"D04", "D05", "D06"}:
        return "trend_with_lulls"
    if regime_code in {"D13"}:
        return "liquidity_stress"
    if regime_code in {"D18", "D19"}:
        return "breakout_reversal"
    if regime_code in {"D12", "D14"}:
        return "event_cluster"
    if regime_code in {"D15", "D17"}:
        return "dispersion_rotation"
    return "normal_open_lull_close"


def build_calendar(profile_name: str, profile: dict, start_date: str, anchor: dict, ticker_states: dict[str, str]) -> pd.DataFrame:
    rng = random.Random(profile["seed"])
    regimes = expand_regime_counts(profile["counts"])
    rng.shuffle(regimes)

    observed = anchor.get("observed_regime_code")
    if observed in regimes:
        regimes[0] = observed

    dates = business_dates(start_date, len(regimes))
    rows: list[dict] = []
    for day_index, (date, regime_code) in enumerate(zip(dates, regimes), start=1):
        params = PARAMS_BY_REGIME[regime_code]
        is_gap_day = rng.random() < params.gap_probability or regime_code in {"D08", "D09", "D10", "D11"}
        is_market_shock_day = rng.random() < params.shock_probability or regime_code in {"D07", "D20"}
        event_cluster = regime_code in {"D12", "D14"} or rng.random() < 0.04
        shock_symbols = choose_shock_symbols(rng, regime_code, ticker_states) if (is_market_shock_day or event_cluster or regime_code in {"D13", "D17"}) else []

        rows.append(
            {
                "quarter_profile": profile_name,
                "profile_description": profile["description"],
                "seed": profile["seed"],
                "scenario_day": day_index,
                "trade_date": date.date().isoformat(),
                "weekday": date.day_name(),
                "regime_code": regime_code,
                "regime_family": REGIME_FAMILIES[regime_code],
                "intraday_template": intraday_template(regime_code),
                "vol_multiplier": params.vol_multiplier,
                "event_rate_multiplier": params.event_rate_multiplier,
                "spread_multiplier": params.spread_multiplier,
                "depth_multiplier": params.depth_multiplier,
                "correlation_multiplier": params.correlation_multiplier,
                "is_gap_day": is_gap_day,
                "is_market_shock_day": is_market_shock_day,
                "event_cluster": event_cluster,
                "shock_symbol_count": len(shock_symbols),
                "shock_symbols": "|".join(shock_symbols),
                "observed_anchor_regime_code": anchor.get("observed_regime_code"),
                "observed_anchor_evidence": anchor.get("observed_regime_evidence_label"),
                "evidence_label": "synthetic_scenario_design",
            }
        )
    return pd.DataFrame(rows)


def build_mix_summary(calendar: pd.DataFrame) -> pd.DataFrame:
    summary = calendar.groupby(["quarter_profile", "regime_code", "regime_family"], sort=True).agg(
        days=("scenario_day", "count"),
        gap_days=("is_gap_day", "sum"),
        market_shock_days=("is_market_shock_day", "sum"),
        event_cluster_days=("event_cluster", "sum"),
        avg_vol_multiplier=("vol_multiplier", "mean"),
        avg_spread_multiplier=("spread_multiplier", "mean"),
        avg_depth_multiplier=("depth_multiplier", "mean"),
    ).reset_index()
    summary["share"] = summary["days"] / 63.0
    return summary


def build_profile_summary(calendar: pd.DataFrame) -> pd.DataFrame:
    return calendar.groupby("quarter_profile", sort=True).agg(
        days=("scenario_day", "count"),
        unique_regimes=("regime_code", "nunique"),
        gap_days=("is_gap_day", "sum"),
        market_shock_days=("is_market_shock_day", "sum"),
        event_cluster_days=("event_cluster", "sum"),
        avg_vol_multiplier=("vol_multiplier", "mean"),
        avg_event_rate_multiplier=("event_rate_multiplier", "mean"),
        avg_spread_multiplier=("spread_multiplier", "mean"),
        avg_depth_multiplier=("depth_multiplier", "mean"),
        avg_correlation_multiplier=("correlation_multiplier", "mean"),
    ).reset_index()


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    text_frame = frame.copy()
    for column in text_frame.columns:
        text_frame[column] = text_frame[column].map(lambda value: "" if pd.isna(value) else str(value))
    headers = [str(column) for column in text_frame.columns]
    rows = text_frame.values.tolist()
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def write_report(output_dir: Path, calendar: pd.DataFrame, profile_summary: pd.DataFrame, anchor: dict) -> None:
    lines = [
        "# Phase 4 Synthetic Scenario Calendar Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase creates deterministic synthetic-quarter scenario calendars.",
        "It designs regime coverage and stress conditions; it does not generate prices, books or strategy results.",
        "",
        "## Observed Anchor",
        "",
        f"- Observed one-day candidate regime: {anchor.get('observed_regime_code')} / {anchor.get('observed_regime')}",
        f"- Evidence label: {anchor.get('observed_regime_evidence_label')}",
        "",
        "## Profile Summary",
        "",
        _markdown_table(profile_summary),
        "",
        "## Outputs",
        "",
        "- `scenario_calendar.csv`",
        "- `scenario_calendar.jsonl`",
        "- `regime_mix_summary.csv`",
        "- `profile_summary.csv`",
        "- `scenario_manifest.json`",
        "",
    ]
    (output_dir / "phase4_scenario_calendar_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase4(phase3_dir: Path, output_dir: Path, start_date: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    anchor = load_observed_anchor(phase3_dir)
    ticker_states = load_ticker_states(phase3_dir)

    calendars = [
        build_calendar(profile_name, profile, start_date, anchor, ticker_states)
        for profile_name, profile in SEED_PROFILES.items()
    ]
    calendar = pd.concat(calendars, ignore_index=True)
    mix_summary = build_mix_summary(calendar)
    profile_summary = build_profile_summary(calendar)

    calendar.to_csv(output_dir / "scenario_calendar.csv", index=False)
    calendar.to_json(output_dir / "scenario_calendar.jsonl", orient="records", lines=True)
    mix_summary.to_csv(output_dir / "regime_mix_summary.csv", index=False)
    profile_summary.to_csv(output_dir / "profile_summary.csv", index=False)
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "phase3_dir": str(phase3_dir),
        "start_date": start_date,
        "profiles": list(SEED_PROFILES),
        "calendar_rows": int(len(calendar)),
        "days_per_profile": 63,
        "symbols": SYMBOLS,
        "observed_anchor": anchor,
        "evidence_scope": "synthetic_scenario_design_not_market_forecast",
    }
    (output_dir / "scenario_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, calendar, profile_summary, anchor)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Phase 4 synthetic scenario calendars.")
    parser.add_argument("--phase3-dir", type=Path, default=Path("outputs/phase3"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase4"))
    parser.add_argument("--start-date", default="2026-07-14")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase4(args.phase3_dir, args.output_dir, args.start_date)


if __name__ == "__main__":
    main()
