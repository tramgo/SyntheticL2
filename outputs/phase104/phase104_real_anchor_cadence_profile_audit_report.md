# Phase103 Calibrated Realism Rerun

Generated UTC: 2026-07-19T22:04:46.814833+00:00

Phase103 compares the patched calibrated dense synthetic shard against the available real Zerodha WebSocket anchor.
This is a one-symbol calibrated readout, not permission to reopen strategy replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase103_profile_id | P103_HDFCBANK_REAL_ANCHOR_CADENCE_VOL | Calibrated synthetic profile audited |
| phase103_real_symbols_profiled | 1 | Real WebSocket symbols profiled |
| phase103_synthetic_symbols_profiled | 1 | Synthetic dense symbols profiled |
| phase103_compared_symbols | 1 | Symbols present in both real and synthetic profiles |
| phase103_symbol_metric_anchor_rows | 8 | Symbol/metric calibration anchors compared |
| phase103_calibration_gap_rows | 1 | Anchor rows outside ratio gates |
| phase103_calibration_gap_fraction | 0.125 | Fraction of compared symbol/metric anchors outside gates |
| phase103_severe_metric_gap_count | 1 | Metrics where more than half of symbols fail calibration gates |
| phase103_calibrated_realism_patch_pass | 0 | 1 means patched calibrated HDFCBANK shard passes one-symbol realism readout |
| phase103_strategy_replay_allowed | 0 | Strategy replay remains closed until multiday and broader-symbol realism gates pass |
| phase103_recommend_next_action | expand_calibrated_realism_rerun_to_32_symbols_or_collect_multiday_real_panel | Recommended next milestone |

## Calibration Gap Summary

| category | metric | symbol_metrics | gap_count | gap_fraction | median_synthetic_to_real_ratio | min_synthetic_to_real_ratio | max_synthetic_to_real_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L1 imbalance scale | median_abs_l1_imbalance | 1 | 0 | 0 | 0.857227 | 0.857227 | 0.857227 |
| displayed L1 depth scale | median_l1_depth | 1 | 0 | 0 | 0.805583 | 0.805583 | 0.805583 |
| displayed L5 depth scale | median_l5_depth | 1 | 0 | 0 | 0.429062 | 0.429062 | 0.429062 |
| median spread scale | median_spread_bps | 1 | 0 | 0 | 1.003 | 1.003 | 1.003 |
| one-tick volatility scale | one_tick_return_std | 1 | 1 | 1 | 13.4052 | 13.4052 | 13.4052 |
| received tick cadence | median_gap_ms | 1 | 0 | 0 | 1 | 1 | 1 |
| tail received tick cadence | p90_gap_ms | 1 | 0 | 0 | 0.692 | 0.692 | 0.692 |
| tail spread scale | p90_spread_bps | 1 | 0 | 0 | 0.983351 | 0.983351 | 0.983351 |

## Real vs Calibrated Synthetic Comparison

| symbol | category | metric | real_value | synthetic_value | synthetic_to_real_ratio | lower_ratio_gate | upper_ratio_gate | calibration_gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HDFCBANK | received tick cadence | median_gap_ms | 500 | 500 | 1 | 0.2 | 5 | False |
| HDFCBANK | tail received tick cadence | p90_gap_ms | 1000 | 692 | 0.692 | 0.2 | 5 | False |
| HDFCBANK | median spread scale | median_spread_bps | 1.22137 | 1.22504 | 1.003 | 0.25 | 4 | False |
| HDFCBANK | tail spread scale | p90_spread_bps | 3.05055 | 2.99976 | 0.983351 | 0.25 | 4 | False |
| HDFCBANK | displayed L1 depth scale | median_l1_depth | 1003 | 808 | 0.805583 | 0.1 | 10 | False |
| HDFCBANK | displayed L5 depth scale | median_l5_depth | 16007 | 6868 | 0.429062 | 0.1 | 10 | False |
| HDFCBANK | L1 imbalance scale | median_abs_l1_imbalance | 0.667698 | 0.572368 | 0.857227 | 0.25 | 4 | False |
| HDFCBANK | one-tick volatility scale | one_tick_return_std | 0.00012355 | 0.00165621 | 13.4052 | 0.1 | 10 | True |

## Remediation Queue

| priority | work_item | why | minimum_deliverable | acceptance_gate |
| --- | --- | --- | --- | --- |
| 1 | collect_multi_day_real_anchor_panel | A single real WebSocket day cannot identify regime frequencies, annual tails, month effects, or stable cross-regime calibration. | At least 5-10 full real trading days across normal, volatile, and shock-like sessions with the same 54-column WebSocket schema. | Real anchor profile table has multiple dates per symbol and reports stable cadence/spread/depth ranges before strategy mining resumes. |
| 2 | calibrate_one_tick_return_std | 100.00% of symbol anchors are outside ratio gates; median synthetic/real ratio=13.405. | Adjust generator calibration for one-tick volatility scale and rerun Phase94 comparison. | Gap fraction <= 25% for this metric on the current one-day anchor, then confirm with multi-day real panel. |
| 3 | calibrate_median_abs_l1_imbalance | 0.00% of symbol anchors are outside ratio gates; median synthetic/real ratio=0.857. | Adjust generator calibration for L1 imbalance scale and rerun Phase94 comparison. | Gap fraction <= 25% for this metric on the current one-day anchor, then confirm with multi-day real panel. |
| 4 | calibrate_median_l1_depth | 0.00% of symbol anchors are outside ratio gates; median synthetic/real ratio=0.806. | Adjust generator calibration for displayed L1 depth scale and rerun Phase94 comparison. | Gap fraction <= 25% for this metric on the current one-day anchor, then confirm with multi-day real panel. |
| 5 | calibrate_median_l5_depth | 0.00% of symbol anchors are outside ratio gates; median synthetic/real ratio=0.429. | Adjust generator calibration for displayed L5 depth scale and rerun Phase94 comparison. | Gap fraction <= 25% for this metric on the current one-day anchor, then confirm with multi-day real panel. |
| 6 | calibrate_median_spread_bps | 0.00% of symbol anchors are outside ratio gates; median synthetic/real ratio=1.003. | Adjust generator calibration for median spread scale and rerun Phase94 comparison. | Gap fraction <= 25% for this metric on the current one-day anchor, then confirm with multi-day real panel. |
| 7 | freeze_strategy_replay_until_calibration_gate | Phase93 explicitly stopped strategy mining; new strategy branches would be fishing unless realism gaps are triaged. | Machine-readable gate that blocks Phase95+ strategy replay unless Phase94 calibration_replay_resume_allowed=1. | No new strategy replay milestone is marked ready while calibration audit fails. |
