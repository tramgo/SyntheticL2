# Phase97 Generator Recalibration Patch Plan

Generated UTC: 2026-07-19T21:37:50.292662+00:00

Phase97 converts Phase94 calibration gaps and Phase96 real-panel readiness into an ordered generator recalibration plan.
It does not reopen strategy replay; it preserves the lock until real-anchor coverage and calibration gates pass.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase97_patch_metric_rows | 8 | Calibration metrics mapped into generator patch plan |
| phase97_severe_patch_rows | 2 | Metrics with >=50% symbol-anchor gap fraction |
| phase97_material_or_severe_patch_rows | 4 | Metrics with >=25% symbol-anchor gap fraction |
| phase97_strategy_replay_allowed | 0 | 1 means strategy replay may resume |
| phase97_generator_recalibration_required | 1 | 1 means generator/data calibration work remains required |
| phase97_recommend_next_action | extend_real_anchor_panel_then_patch_timing_volatility_book_shape | Recommended next milestone |

## Patch Plan

| priority | metric | category | severity | gap_fraction | median_synthetic_to_real_ratio | generator_layer | patch_intent | primary_knobs | validation_metric | requires_multiday_confirmation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | p90_gap_ms | tail received tick cadence | severe | 0.625 | 0.125541 | event_timing_point_process | increase tail inter-arrival gaps or reduce over-dense burst persistence where synthetic/real ratio is too low | hawkes_baseline_intensity\|self_excitation_decay\|retail_feed_throttle\|disconnect_gap_injection | p90_gap_ms gap_fraction <= 0.25 and median synthetic_to_real_ratio within [0.20, 5.00] | True |
| 2 | one_tick_return_std | one-tick volatility scale | severe | 0.53125 | 10.1737 | efficient_price_and_microprice_noise | reduce synthetic one-tick volatility scale when synthetic/real ratio is too high | per_tick_volatility_multiplier\|jump_size_scale\|microprice_noise_scale\|shock_decay | one_tick_return_std gap_fraction <= 0.25 and median synthetic_to_real_ratio within [0.10, 10.00] | True |
| 3 | median_abs_l1_imbalance | L1 imbalance scale | material | 0.46875 | 0.272869 | l1_queue_size_and_imbalance_model | increase or reshape displayed L1 imbalance dispersion when synthetic imbalance is too muted | l1_quantity_skew_scale\|bid_ask_copula_strength\|queue_replenishment_asymmetry | median_abs_l1_imbalance gap_fraction <= 0.25 and median synthetic_to_real_ratio within [0.25, 4.00] | True |
| 4 | median_l5_depth | displayed L5 depth scale | material | 0.28125 | 1.63643 | l2_depth_shape_model | rebalance L2 depth ladder scale and cross-symbol heterogeneity | depth_ladder_multiplier\|level_decay_curve\|symbol_liquidity_scale\|etf_equity_depth_split | median_l5_depth gap_fraction <= 0.25 and median synthetic_to_real_ratio within [0.10, 10.00] | True |
| 5 | median_l1_depth | displayed L1 depth scale | watch | 0.21875 | 2.14155 | l1_depth_scale_model | rebalance top-of-book displayed depth scale after L5 shape adjustment | l1_base_depth_multiplier\|l1_l5_share_ratio\|symbol_depth_shrinkage | median_l1_depth gap_fraction <= 0.25 and median synthetic_to_real_ratio within [0.10, 10.00] | True |
| 6 | median_gap_ms | received tick cadence | watch | 0.125 | 0.4 | event_timing_point_process | monitor median cadence while fixing p90 cadence; avoid making the full stream too sparse | baseline_intensity_floor\|symbol_activity_scale | median_gap_ms gap_fraction <= 0.25 | True |
| 7 | median_spread_bps | median spread scale | pass | 0 | 1.01068 | spread_model | preserve current spread calibration unless future multi-day anchors contradict it | spread_tick_distribution\|symbol_spread_scale\|regime_spread_multiplier | median_spread_bps remains gap_fraction <= 0.25 | True |
| 8 | p90_spread_bps | tail spread scale | pass | 0 | 1.13458 | spread_tail_model | preserve current tail spread calibration unless future multi-day anchors contradict it | spread_tail_multiplier\|shock_spread_widening\|feed_profile_spread_noise | p90_spread_bps remains gap_fraction <= 0.25 | True |

## Patch Sequence

| sequence | stage | action | exit_gate |
| --- | --- | --- | --- |
| 1 | real_anchor_extension | Collect or ingest at least 5 ready real L2 days, 10 preferred, then rerun Phase96 and Phase94. | phase96_panels_ready_for_phase94_rerun=1 |
| 2 | timing_patch | Patch p90_gap_ms first because event cadence affects all replay horizons and forward-fill/staleness assumptions. | p90_gap_ms gap_fraction <= 0.25 without breaking median_gap_ms |
| 3 | volatility_patch | Patch one_tick_return_std after timing because current synthetic one-tick volatility is too high relative to the real anchor. | one_tick_return_std gap_fraction <= 0.25 |
| 4 | book_shape_patch | Patch L1 imbalance and L1/L5 depth scales together so the book ladder remains internally consistent. | median_abs_l1_imbalance, median_l1_depth, and median_l5_depth gap_fraction <= 0.25 |
| 5 | preserve_passing_spread_anchor | Keep median and p90 spread calibration within current passing gates while other patches are applied. | median_spread_bps and p90_spread_bps gap_fraction remain <= 0.25 |
| 6 | replay_gate_review | Only after Phase94 passes on multi-day anchors may a new strategy-family precommit be created. | phase94_strategy_replay_resume_allowed=1 |

## Strategy Replay Lock

| lock_id | strategy_replay_allowed | phase94_strategy_resume_allowed | phase96_strategy_replay_unlocked | decision | allowed_next_action |
| --- | --- | --- | --- | --- | --- |
| P97_STRATEGY_REPLAY_LOCK | False | 0 | 0 | replay_closed | generator_recalibration_and_real_panel_collection |
