from __future__ import annotations

from dataclasses import dataclass, asdict


DEFAULT_PROFILE_ID = "P98_LEGACY_DEFAULT"


@dataclass(frozen=True)
class GeneratorCalibrationProfile:
    profile_id: str = DEFAULT_PROFILE_ID
    event_timing_tail_gap_multiplier: float = 1.0
    event_timing_burst_throttle_fraction: float = 0.0
    price_micro_step_spread_fraction: float = 0.08
    price_jump_size_scale: float = 1.0
    price_anchor_source_events: bool = False
    book_l1_quantity_skew_scale: float = 1.0
    book_depth_ladder_multiplier: float = 1.0
    book_l1_l5_share_ratio: float = 1.0
    spread_preserve_current_scale: float = 1.0

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
}


def get_calibration_profile(profile_id: str | None) -> GeneratorCalibrationProfile:
    key = profile_id or DEFAULT_PROFILE_ID
    if key not in PROFILES:
        allowed = ", ".join(sorted(PROFILES))
        raise ValueError(f"Unknown generator calibration profile {key!r}. Allowed profiles: {allowed}")
    return PROFILES[key]
