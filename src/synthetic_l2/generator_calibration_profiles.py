from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Mapping


DEFAULT_PROFILE_ID = "P98_LEGACY_DEFAULT"


@dataclass(frozen=True)
class GeneratorCalibrationProfile:
    profile_id: str = DEFAULT_PROFILE_ID
    event_timing_tail_gap_multiplier: float = 1.0
    event_timing_burst_throttle_fraction: float = 0.0
    price_micro_step_spread_fraction: float = 0.08
    price_jump_size_scale: float = 1.0
    price_anchor_source_events: bool = False
    source_mid_return_scale: float = 1.0
    book_l1_quantity_skew_scale: float = 1.0
    book_depth_ladder_multiplier: float = 1.0
    book_l1_l5_share_ratio: float = 1.0
    spread_preserve_current_scale: float = 1.0
    symbol_depth_scale_overrides: Mapping[str, float] | None = None
    symbol_l1_imbalance_scale_overrides: Mapping[str, float] | None = None
    symbol_l1_imbalance_min_abs_overrides: Mapping[str, float] | None = None
    symbol_tail_gap_multiplier_overrides: Mapping[str, float] | None = None

    def to_manifest(self) -> dict[str, float | str]:
        return asdict(self)


PROFILES: dict[str, GeneratorCalibrationProfile] = {
    DEFAULT_PROFILE_ID: GeneratorCalibrationProfile(),
    "P98_TIMING_ONLY_CONSERVATIVE": GeneratorCalibrationProfile(
        profile_id="P98_TIMING_ONLY_CONSERVATIVE",
        event_timing_tail_gap_multiplier=2.0,
        event_timing_burst_throttle_fraction=0.10,
        price_anchor_source_events=True,
    ),
    "P98_TIMING_VOL_MODERATE": GeneratorCalibrationProfile(
        profile_id="P98_TIMING_VOL_MODERATE",
        event_timing_tail_gap_multiplier=4.0,
        event_timing_burst_throttle_fraction=0.20,
        price_micro_step_spread_fraction=0.0,
        price_jump_size_scale=0.75,
        price_anchor_source_events=True,
    ),
    "P98_FULL_BOOK_REBALANCE_BASE": GeneratorCalibrationProfile(
        profile_id="P98_FULL_BOOK_REBALANCE_BASE",
        event_timing_tail_gap_multiplier=4.0,
        event_timing_burst_throttle_fraction=0.20,
        price_micro_step_spread_fraction=0.0,
        price_jump_size_scale=0.75,
        price_anchor_source_events=True,
        book_l1_quantity_skew_scale=1.50,
        book_depth_ladder_multiplier=0.80,
        book_l1_l5_share_ratio=0.85,
    ),
    "P98_FULL_BOOK_REBALANCE_STRONG": GeneratorCalibrationProfile(
        profile_id="P98_FULL_BOOK_REBALANCE_STRONG",
        event_timing_tail_gap_multiplier=6.0,
        event_timing_burst_throttle_fraction=0.35,
        price_micro_step_spread_fraction=0.0,
        price_jump_size_scale=0.60,
        price_anchor_source_events=True,
        book_l1_quantity_skew_scale=1.75,
        book_depth_ladder_multiplier=0.65,
        book_l1_l5_share_ratio=0.85,
    ),
    "P103_HDFCBANK_REAL_ANCHOR_CADENCE_VOL": GeneratorCalibrationProfile(
        profile_id="P103_HDFCBANK_REAL_ANCHOR_CADENCE_VOL",
        event_timing_tail_gap_multiplier=500.0,
        event_timing_burst_throttle_fraction=0.0,
        price_micro_step_spread_fraction=0.0,
        price_jump_size_scale=0.50,
        price_anchor_source_events=True,
        book_l1_quantity_skew_scale=1.50,
        book_depth_ladder_multiplier=0.80,
        book_l1_l5_share_ratio=0.85,
    ),
    "P104_HDFCBANK_REAL_ANCHOR_CADENCE_VOL_PRICE_SCALE": GeneratorCalibrationProfile(
        profile_id="P104_HDFCBANK_REAL_ANCHOR_CADENCE_VOL_PRICE_SCALE",
        event_timing_tail_gap_multiplier=500.0,
        event_timing_burst_throttle_fraction=0.0,
        price_micro_step_spread_fraction=0.0,
        price_jump_size_scale=0.50,
        price_anchor_source_events=True,
        source_mid_return_scale=0.075,
        book_l1_quantity_skew_scale=1.50,
        book_depth_ladder_multiplier=0.80,
        book_l1_l5_share_ratio=0.85,
    ),
    "P108_SYMBOL_AWARE_CADENCE_DEPTH_IMBALANCE": GeneratorCalibrationProfile(
        profile_id="P108_SYMBOL_AWARE_CADENCE_DEPTH_IMBALANCE",
        event_timing_tail_gap_multiplier=500.0,
        event_timing_burst_throttle_fraction=0.0,
        price_micro_step_spread_fraction=0.0,
        price_jump_size_scale=0.50,
        price_anchor_source_events=True,
        source_mid_return_scale=0.075,
        book_l1_quantity_skew_scale=1.50,
        book_depth_ladder_multiplier=0.80,
        book_l1_l5_share_ratio=0.85,
        symbol_depth_scale_overrides={
            "BAJAJ-AUTO": 0.06454677297141195,
            "BRITANNIA": 0.05163999113132655,
            "GOLDBEES": 14.044356617647058,
            "ITBEES": 241.68565720748018,
            "ITC": 16.714264705882353,
            "LT": 0.0702189781021897,
            "M&M": 0.06178406476970165,
            "MARUTI": 0.0548095168588527,
            "ULTRACEMCO": 0.0410599883517763,
        },
        symbol_l1_imbalance_scale_overrides={
            "AXISBANK": 4.0,
            "BAJAJ-AUTO": 4.0,
            "BHARTIARTL": 4.0,
            "BPCL": 4.0,
            "BRITANNIA": 4.0,
            "HINDUNILVR": 4.0,
            "INFY": 4.0,
            "KOTAKBANK": 4.0,
            "LT": 4.0,
            "MARUTI": 4.0,
            "ONGC": 4.0,
            "SBIN": 4.0,
            "TCS": 4.0,
            "TECHM": 4.0,
            "WIPRO": 4.0,
        },
        symbol_tail_gap_multiplier_overrides={
            "ADANIPORTS": 635.0823699421966,
            "AXISBANK": 441.4056358381433,
            "BHARTIARTL": 5.706791907514476,
            "BPCL": 648.5895953757225,
            "BRITANNIA": 650.3219653179191,
            "CIPLA": 646.1439306358382,
            "DRREDDY": 645.7037572254335,
            "GOLDBEES": 634.8471098265896,
            "HINDUNILVR": 639.3641618497111,
            "ITBEES": 644.8809248554913,
            "ITC": 641.3599710982659,
            "JUNIORBEES": 6.864161849710983,
            "KOTAKBANK": 9.21242774566474,
            "LT": 5.420086705202312,
            "NESTLEIND": 641.0459537572254,
            "ONGC": 5.804913294797687,
            "SUNPHARMA": 631.1112716763006,
            "TECHM": 5.057369942196532,
            "ULTRACEMCO": 651.0336705202312,
        },
    ),
    "P109_SYMBOL_AWARE_RESIDUAL_IMBALANCE_FLOOR": GeneratorCalibrationProfile(
        profile_id="P109_SYMBOL_AWARE_RESIDUAL_IMBALANCE_FLOOR",
        event_timing_tail_gap_multiplier=500.0,
        event_timing_burst_throttle_fraction=0.0,
        price_micro_step_spread_fraction=0.0,
        price_jump_size_scale=0.50,
        price_anchor_source_events=True,
        source_mid_return_scale=0.075,
        book_l1_quantity_skew_scale=1.50,
        book_depth_ladder_multiplier=0.80,
        book_l1_l5_share_ratio=0.85,
        symbol_depth_scale_overrides={
            "BAJAJ-AUTO": 0.06454677297141195,
            "BRITANNIA": 0.05163999113132655,
            "GOLDBEES": 14.044356617647058,
            "ITBEES": 241.68565720748018,
            "ITC": 16.714264705882353,
            "LT": 0.0702189781021897,
            "M&M": 0.06178406476970165,
            "MARUTI": 0.0548095168588527,
            "ULTRACEMCO": 0.0410599883517763,
        },
        symbol_l1_imbalance_scale_overrides={
            "AXISBANK": 4.0,
            "BAJAJ-AUTO": 4.0,
            "BHARTIARTL": 4.0,
            "BPCL": 4.0,
            "BRITANNIA": 4.0,
            "HINDUNILVR": 4.0,
            "INFY": 4.0,
            "KOTAKBANK": 4.0,
            "LT": 4.0,
            "MARUTI": 4.0,
            "ONGC": 4.0,
            "SBIN": 4.0,
            "TCS": 4.0,
            "TECHM": 4.0,
            "WIPRO": 4.0,
        },
        symbol_l1_imbalance_min_abs_overrides={
            "AXISBANK": 0.35,
            "BAJAJ-AUTO": 0.35,
            "BHARTIARTL": 0.35,
            "BPCL": 0.35,
            "BRITANNIA": 0.35,
            "HINDUNILVR": 0.35,
            "INFY": 0.35,
            "KOTAKBANK": 0.35,
            "LT": 0.35,
            "MARUTI": 0.35,
            "ONGC": 0.35,
            "SBIN": 0.35,
            "TCS": 0.35,
            "TECHM": 0.35,
            "WIPRO": 0.35,
        },
        symbol_tail_gap_multiplier_overrides={
            "ADANIPORTS": 635.0823699421966,
            "AXISBANK": 441.4056358381433,
            "BHARTIARTL": 5.706791907514476,
            "BPCL": 648.5895953757225,
            "BRITANNIA": 650.3219653179191,
            "CIPLA": 646.1439306358382,
            "DRREDDY": 645.7037572254335,
            "GOLDBEES": 634.8471098265896,
            "HINDUNILVR": 639.3641618497111,
            "ITBEES": 644.8809248554913,
            "ITC": 641.3599710982659,
            "JUNIORBEES": 6.864161849710983,
            "KOTAKBANK": 9.21242774566474,
            "LT": 5.420086705202312,
            "NESTLEIND": 641.0459537572254,
            "ONGC": 5.804913294797687,
            "SUNPHARMA": 631.1112716763006,
            "TECHM": 5.057369942196532,
            "ULTRACEMCO": 651.0336705202312,
        },
    ),
}


def get_calibration_profile(profile_id: str | None) -> GeneratorCalibrationProfile:
    key = profile_id or DEFAULT_PROFILE_ID
    if key not in PROFILES:
        allowed = ", ".join(sorted(PROFILES))
        raise ValueError(f"Unknown generator calibration profile {key!r}. Allowed profiles: {allowed}")
    return PROFILES[key]
