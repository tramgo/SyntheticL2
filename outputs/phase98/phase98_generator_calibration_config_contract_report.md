# Phase98 Generator Calibration Config Contract

Generated UTC: 2026-07-19T21:40:43.472434+00:00

Phase98 turns the Phase97 patch plan into explicit generator calibration knobs, candidate profiles, wiring targets and validation gates.
It does not change generated data yet and does not reopen strategy replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase98_patch_metric_rows | 8 | Phase97 patch metrics consumed |
| phase98_severe_metric_rows | 2 | Severe Phase97 metrics requiring calibration |
| phase98_generator_knob_rows | 8 | Generator knobs cataloged for calibration wiring |
| phase98_candidate_profile_rows | 4 | Candidate calibration profiles defined |
| phase98_validation_gate_rows | 7 | Validation gates locked before generator patch execution |
| phase98_strategy_replay_allowed | 0 | 1 means strategy replay may resume now |
| phase98_ready_for_generator_patch_wiring | 1 | 1 means Phase99 may wire calibration profiles into generator code |
| phase98_recommend_next_action | wire_calibration_profiles_into_generator_then_rerun_phase94_quality_only | Recommended next milestone |

## Generator Knob Catalog

| knob_id | generator_phase | current_observed_pattern | default_value | candidate_values | target_metric | expected_effect | risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| event_timing.tail_gap_multiplier | phase49_phase51_dense_timing | dense_subtick_id adds millisecond offsets, creating over-dense tail cadence in Phase94 | 1 | 2.0\|4.0\|6.0\|8.0 | p90_gap_ms | increase synthetic tail inter-arrival gaps while preserving enough median event density | too high may make active symbols artificially sparse |
| event_timing.burst_throttle_fraction | phase49_phase51_dense_timing | dense repeats preserve source-event bursts too aggressively | 0 | 0.10\|0.20\|0.35 | p90_gap_ms | thin or stagger dense burst repetitions to reduce unrealistic burst persistence | may reduce rows and change storage-size assumptions |
| price.micro_step_spread_fraction | phase49_phase51_dense_price | dense micro-step uses spread * 0.08 and Phase94 shows high one-tick volatility | 0.08 | 0.02\|0.03\|0.04\|0.05 | one_tick_return_std | reduce synthetic one-tick volatility without changing spread anchors | too low may suppress legitimate short-horizon movement |
| price.jump_size_scale | phase45_phase51_price_state | Phase94 median synthetic/real one_tick_return_std ratio slightly exceeds upper gate | 1 | 0.45\|0.60\|0.75\|0.90 | one_tick_return_std | reduce generator jump contribution while preserving regime ranking | may flatten shock days if applied globally instead of regime-conditionally |
| book.l1_quantity_skew_scale | phase45_add_depth_levels | l1_imbalance is clipped and converted directly into bid/ask quantity skew; Phase94 shows muted median_abs_l1_imbalance | 1 | 1.25\|1.50\|1.75\|2.00 | median_abs_l1_imbalance | increase displayed L1 imbalance dispersion | can create unrealistic one-sided displayed quantity if not clipped |
| book.depth_ladder_multiplier | phase45_add_depth_levels | base_qty = 100 + event_intensity * 250 with level_weight = 1 + 0.35*(level-1) | 1 | 0.50\|0.65\|0.80\|1.20 | median_l5_depth | rebalance L5 displayed depth scale and cross-symbol heterogeneity | must be coordinated with L1 depth so ladder shape remains plausible |
| book.l1_l5_share_ratio | phase45_add_depth_levels | level weights create deterministic ladder shape from the same base quantity | 1 | 0.70\|0.85\|1.15\|1.30 | median_l1_depth\|median_l5_depth | adjust top-of-book share relative to deeper displayed book | may pass L1 but fail L5 unless jointly validated |
| spread.preserve_current_scale | phase45_phase51_spread | Phase94 median and p90 spread anchors pass | 1 | 1.0 | median_spread_bps\|p90_spread_bps | hold spread distribution stable during timing/volatility/book patches | do not accidentally fix failing metrics by breaking passing spread anchors |

## Candidate Calibration Profiles

| profile_id | scope | description | event_timing.tail_gap_multiplier | event_timing.burst_throttle_fraction | price.micro_step_spread_fraction | price.jump_size_scale | book.l1_quantity_skew_scale | book.depth_ladder_multiplier | book.l1_l5_share_ratio | spread.preserve_current_scale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P98_TIMING_ONLY_CONSERVATIVE | timing | Smallest timing patch; tests whether tail cadence can improve without reducing median event support too far. | 2 | 0.1 | 0.08 | 1 | 1 | 1 | 1 | 1 |
| P98_TIMING_VOL_MODERATE | timing_volatility | Moderate timing and volatility patch matching the two severe Phase97 gaps. | 4 | 0.2 | 0.04 | 0.75 | 1 | 1 | 1 | 1 |
| P98_FULL_BOOK_REBALANCE_BASE | timing_volatility_book | Base full patch: timing and volatility plus L1 imbalance/depth rebalance. | 4 | 0.2 | 0.04 | 0.75 | 1.5 | 0.8 | 0.85 | 1 |
| P98_FULL_BOOK_REBALANCE_STRONG | timing_volatility_book | Stronger full patch for sensitivity testing if base patch under-corrects cadence/volatility. | 6 | 0.35 | 0.03 | 0.6 | 1.75 | 0.65 | 0.85 | 1 |

## Validation Contract

| gate_id | requirement | pass_threshold |
| --- | --- | --- |
| P98_NO_STRATEGY_REPLAY | Calibration profiles may only produce generator quality and Phase94-style anchor evidence. | No P&L replay or strategy promotion artifacts generated by calibration runs. |
| P98_REAL_PANEL_FIRST | Preferred path is to extend the real panel before finalizing any generator patch. | Phase96 panels_ready_for_phase94_rerun=1 before declaring calibration fixed. |
| P98_TIMING | Tail cadence severe gap must clear without breaking median cadence. | p90_gap_ms gap_fraction<=0.25 and median_gap_ms gap_fraction<=0.25 |
| P98_VOLATILITY | One-tick volatility severe gap must clear. | one_tick_return_std gap_fraction<=0.25 |
| P98_BOOK_SHAPE | L1 imbalance and L1/L5 depth must jointly clear material gap gates. | median_abs_l1_imbalance, median_l1_depth and median_l5_depth gap_fraction<=0.25 |
| P98_SPREAD_PRESERVATION | Passing spread anchors must remain passing. | median_spread_bps and p90_spread_bps gap_fraction<=0.25 |
| P98_REOPEN_STRATEGY_REPLAY | Strategy replay can reopen only after Phase94 passes on an adequate real anchor panel. | phase94_strategy_replay_resume_allowed=1 and phase96_strategy_replay_unlocked=1 |

## Wiring Targets

| target_file | target_function | knobs_to_wire | current_code_anchor | patch_requirement |
| --- | --- | --- | --- | --- |
| src/synthetic_l2/phase45_raw_tick_lake_materializer.py | add_depth_levels | book.l1_quantity_skew_scale\|book.depth_ladder_multiplier\|book.l1_l5_share_ratio\|spread.preserve_current_scale | base_qty = 100 + intensity * 250; level_weight = 1.0 + 0.35 * (level - 1) | Accept a calibration profile object and apply depth/imbalance multipliers without changing default output when profile is absent. |
| src/synthetic_l2/phase49_dense_tick_rate_expansion.py | densify_frame | event_timing.tail_gap_multiplier\|event_timing.burst_throttle_fraction\|price.micro_step_spread_fraction\|price.jump_size_scale | callback_received_utc_ms += dense_subtick_id; micro_step = spread * 0.08 | Support calibrated subtick spacing/throttle and micro-step scaling while preserving deterministic dense ids. |
| src/synthetic_l2/phase51_full_dense_lake_materializer.py | _densify_chunk | event_timing.tail_gap_multiplier\|event_timing.burst_throttle_fraction\|price.micro_step_spread_fraction\|price.jump_size_scale | callback_received_utc_ms += dense_subtick_id; micro_step = spread * 0.08 | Apply the same calibrated dense timing/price behavior used by Phase49 so shard and full-lake generation remain consistent. |
| src/synthetic_l2/phase94_generator_realism_calibration_audit.py | run_phase94 | profile_id\|calibration_profile_manifest | compares real anchor profile vs synthetic compact profile | Record active generator calibration profile in the audit manifest and compare against the same gates. |
