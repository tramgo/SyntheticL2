# Phase94 Generator Realism Calibration Audit

Generated UTC: 2026-07-19T21:31:02.810602+00:00

Phase94 executes the stop condition from Phase93: strategy mining pauses and the generator/calibration evidence is audited.
The audit compares one-day real Zerodha WebSocket anchors against the synthetic compact full-year lake and consolidates Phase79/80/83/93 realism context.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase94_real_symbols_profiled | 32 | Real one-day WebSocket symbols profiled |
| phase94_synthetic_symbols_profiled | 32 | Synthetic compact symbols profiled |
| phase94_compared_symbols | 32 | Symbols present in both real and synthetic profiles |
| phase94_symbol_metric_anchor_rows | 256 | Symbol/metric calibration anchors compared |
| phase94_calibration_gap_rows | 72 | Anchor rows outside ratio gates |
| phase94_calibration_gap_fraction | 0.28125 | Fraction of compared symbol/metric anchors outside gates |
| phase94_severe_metric_gap_count | 2 | Metrics where more than half of symbols fail calibration gates |
| phase94_generator_calibration_pass | 0 | 1 means current generator calibration is strong enough to reopen strategy mining |
| phase94_strategy_replay_resume_allowed | 0 | 1 means strategy mining may resume immediately |
| phase94_recommend_next_action | collect_multi_day_real_anchor_panel_and_calibrate_gaps | Recommended next milestone |

## Calibration Gap Summary

| category | metric | symbol_metrics | gap_count | gap_fraction | median_synthetic_to_real_ratio | min_synthetic_to_real_ratio | max_synthetic_to_real_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L1 imbalance scale | median_abs_l1_imbalance | 32 | 15 | 0.46875 | 0.272869 | 0 | 1.08119 |
| displayed L1 depth scale | median_l1_depth | 32 | 7 | 0.21875 | 2.14155 | 0.00596584 | 26.9333 |
| displayed L5 depth scale | median_l5_depth | 32 | 9 | 0.28125 | 1.63643 | 0.00316706 | 22.2265 |
| median spread scale | median_spread_bps | 32 | 0 | 0 | 1.01068 | 0.752995 | 2.00224 |
| one-tick volatility scale | one_tick_return_std | 32 | 17 | 0.53125 | 10.1737 | 4.73618 | 22.9252 |
| received tick cadence | median_gap_ms | 32 | 4 | 0.125 | 0.4 | 0.140154 | 0.601202 |
| tail received tick cadence | p90_gap_ms | 32 | 20 | 0.625 | 0.125541 | 0.00110984 | 0.5 |
| tail spread scale | p90_spread_bps | 32 | 0 | 0 | 1.13458 | 0.981459 | 1.34712 |

## Audit Context Ledger

| audit_item | evidence | decision | required_action |
| --- | --- | --- | --- |
| strategy_mining_status | Phase93 pass=0.0 | strategy_mining_stopped_until_generator_audit | Do not run new strategy replay until calibration gaps are triaged. |
| compact_generator_diversity | Phase80 compact diversity pass=1.0 | compact_scenario_diversity_acceptable | Keep compact regime/feed diversity design; do not revert to prefix-only sampling. |
| dense_prefix_sampling_bias | Phase80 biased months=12.0 | prefix_sampling_not_allowed_for_acceptance | Require stratified windows/cached bars for any replay evidence. |
| stratified_replay_cache | Phase83 pass=1.0 | coverage_cache_usable | Use Phase83-like coverage tables for future replay audits. |
| real_anchor_calibration | 72/256 symbol-metric anchors outside ratio gates | calibration_triage_required | Rank spread/depth/cadence/volatility gaps and collect more real days before restarting strategy mining. |

## Remediation Queue

| priority | work_item | why | minimum_deliverable | acceptance_gate |
| --- | --- | --- | --- | --- |
| 1 | collect_multi_day_real_anchor_panel | A single real WebSocket day cannot identify regime frequencies, annual tails, month effects, or stable cross-regime calibration. | At least 5-10 full real trading days across normal, volatile, and shock-like sessions with the same 54-column WebSocket schema. | Real anchor profile table has multiple dates per symbol and reports stable cadence/spread/depth ranges before strategy mining resumes. |
| 2 | calibrate_p90_gap_ms | 62.50% of symbol anchors are outside ratio gates; median synthetic/real ratio=0.126. | Adjust generator calibration for tail received tick cadence and rerun Phase94 comparison. | Gap fraction <= 25% for this metric on the current one-day anchor, then confirm with multi-day real panel. |
| 3 | calibrate_one_tick_return_std | 53.12% of symbol anchors are outside ratio gates; median synthetic/real ratio=10.174. | Adjust generator calibration for one-tick volatility scale and rerun Phase94 comparison. | Gap fraction <= 25% for this metric on the current one-day anchor, then confirm with multi-day real panel. |
| 4 | calibrate_median_abs_l1_imbalance | 46.88% of symbol anchors are outside ratio gates; median synthetic/real ratio=0.273. | Adjust generator calibration for L1 imbalance scale and rerun Phase94 comparison. | Gap fraction <= 25% for this metric on the current one-day anchor, then confirm with multi-day real panel. |
| 5 | calibrate_median_l5_depth | 28.12% of symbol anchors are outside ratio gates; median synthetic/real ratio=1.636. | Adjust generator calibration for displayed L5 depth scale and rerun Phase94 comparison. | Gap fraction <= 25% for this metric on the current one-day anchor, then confirm with multi-day real panel. |
| 6 | calibrate_median_l1_depth | 21.88% of symbol anchors are outside ratio gates; median synthetic/real ratio=2.142. | Adjust generator calibration for displayed L1 depth scale and rerun Phase94 comparison. | Gap fraction <= 25% for this metric on the current one-day anchor, then confirm with multi-day real panel. |
| 7 | freeze_strategy_replay_until_calibration_gate | Phase93 explicitly stopped strategy mining; new strategy branches would be fishing unless realism gaps are triaged. | Machine-readable gate that blocks Phase95+ strategy replay unless Phase94 calibration_replay_resume_allowed=1. | No new strategy replay milestone is marked ready while calibration audit fails. |
