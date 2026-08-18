# Phase413 Replenishment Breakout Filter-Failure Attribution

Phase413 diagnoses why the Phase410/P411 full-depth replenishment-breakout thesis selected zero trades.

It does not generate P&L, does not relax thresholds and does not promote a strategy.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase413_filter_attribution_complete | 1 | Phase413 attribution completed |
| phase413_attribution_id | P413_REPLENISHMENT_BREAKOUT_FILTER_FAILURE_ATTRIBUTION | Attribution id |
| phase413_synthetic_scan_points | 840 | Synthetic scan points attributed |
| phase413_synthetic_pass_all_filters | 0 | Synthetic points passing all Phase410 filters |
| phase413_real_anchor_scan_points | 10 | Real-anchor scan points attributed |
| phase413_real_anchor_pass_all_filters | 0 | Real-anchor points passing all Phase410 filters |
| phase413_pnl_generated | 0 | No P&L generated |
| phase413_strategy_promotion_allowed | 0 | No promotion |
| phase413_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase413_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase413_hard_gate_pass_rows | 9 | Passed hard gates |
| phase413_hard_gate_rows | 9 | Hard gates |
| phase413_next_best_action | precommit_material_new_less_sparse_full_depth_l2_thesis_using_phase413_failure_map | Recommended next action |

## Stage Summary

| panel | stage | scan_points | pass_count | fail_count | pass_rate | threshold_or_rule |
| --- | --- | --- | --- | --- | --- | --- |
| synthetic | window_ok | 840 | 840 | 0 | 1 | windows have >=3 ticks for 30s/20s/10s |
| synthetic | impulse_threshold | 840 | 647 | 193 | 0.770238 | abs(impulse_bps)>=4.0 |
| synthetic | top5_alignment | 840 | 238 | 602 | 0.283333 | side*top5_imbalance>=0.15 |
| synthetic | level_weighted_alignment | 840 | 238 | 602 | 0.283333 | side*level_weighted_imbalance>=0.15 |
| synthetic | l2_l5_replenishment | 840 | 7 | 833 | 0.00833333 | levels_2_to_5_replenishment>=0.12 |
| synthetic | l2_l5_imbalance_alignment | 840 | 238 | 602 | 0.283333 | side*l2_l5_imbalance>=0.15 |
| synthetic | withdrawal_limit | 840 | 825 | 15 | 0.982143 | depth_withdrawal_pressure<=0.1 |
| synthetic | spread_limit | 840 | 840 | 0 | 1 | spread_bps<=8.0 |
| synthetic | breakout_confirmation | 840 | 0 | 840 | 0 | last_price confirms breakout in impulse direction |
| synthetic | future_window | 840 | 840 | 0 | 1 | >=2 future ticks inside 180s horizon |
| real_anchor | window_ok | 10 | 10 | 0 | 1 | windows have >=3 ticks for 30s/20s/10s |
| real_anchor | impulse_threshold | 10 | 8 | 2 | 0.8 | abs(impulse_bps)>=4.0 |
| real_anchor | top5_alignment | 10 | 6 | 4 | 0.6 | side*top5_imbalance>=0.15 |
| real_anchor | level_weighted_alignment | 10 | 6 | 4 | 0.6 | side*level_weighted_imbalance>=0.15 |
| real_anchor | l2_l5_replenishment | 10 | 1 | 9 | 0.1 | levels_2_to_5_replenishment>=0.12 |
| real_anchor | l2_l5_imbalance_alignment | 10 | 5 | 5 | 0.5 | side*l2_l5_imbalance>=0.15 |
| real_anchor | withdrawal_limit | 10 | 6 | 4 | 0.6 | depth_withdrawal_pressure<=0.1 |
| real_anchor | spread_limit | 10 | 10 | 0 | 1 | spread_bps<=8.0 |
| real_anchor | breakout_confirmation | 10 | 1 | 9 | 0.1 | last_price confirms breakout in impulse direction |
| real_anchor | future_window | 10 | 10 | 0 | 1 | >=2 future ticks inside 180s horizon |

## First-Failure Summary

| panel | first_failure_stage | count | share |
| --- | --- | --- | --- |
| synthetic | top5_alignment | 483 | 0.575 |
| synthetic | impulse_threshold | 193 | 0.229762 |
| synthetic | l2_l5_replenishment | 157 | 0.186905 |
| synthetic | breakout_confirmation | 7 | 0.00833333 |
| real_anchor | top5_alignment | 4 | 0.4 |
| real_anchor | l2_l5_replenishment | 3 | 0.3 |
| real_anchor | impulse_threshold | 2 | 0.2 |
| real_anchor | breakout_confirmation | 1 | 0.1 |

## Metric Distributions

| panel | metric | count | p05 | p25 | median | p75 | p95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| synthetic | impulse_bps | 840 | -56.434 | -0.0637578 | 25.7229 | 81.0568 | 113.156 |
| synthetic | top5_imbalance | 840 | -0.575228 | -0.20464 | 0.0168067 | 0.0585036 | 0.454342 |
| synthetic | l2_l5_imbalance | 840 | -0.57529 | -0.204709 | 0.0170068 | 0.0584708 | 0.454286 |
| synthetic | level_weighted_imbalance | 840 | -0.575307 | -0.204508 | 0.0169831 | 0.0585471 | 0.454485 |
| synthetic | l2_l5_replenishment_pressure | 840 | 0 | 0 | 0 | 0.016607 | 0.0813161 |
| synthetic | depth_withdrawal_pressure | 840 | 0 | 0 | 0.0135987 | 0.0373959 | 0.0755493 |
| synthetic | spread_bps | 840 | 1.21418 | 1.50602 | 1.80148 | 1.93311 | 3.83436 |
| real_anchor | impulse_bps | 10 | -815.133 | -2.98647 | 5.23401 | 3632.1 | 5013.73 |
| real_anchor | top5_imbalance | 10 | -0.59708 | -0.393838 | -0.146611 | -0.0322248 | 0.447847 |
| real_anchor | l2_l5_imbalance | 10 | -0.571389 | -0.462871 | -0.0954733 | 0.0436931 | 0.355482 |
| real_anchor | level_weighted_imbalance | 10 | -0.690666 | -0.295936 | -0.260515 | -0.219365 | 0.592531 |
| real_anchor | l2_l5_replenishment_pressure | 10 | 0 | 0 | 0.0162162 | 0.0580126 | 0.251002 |
| real_anchor | depth_withdrawal_pressure | 10 | 0 | 0 | 0.0634768 | 0.319798 | 0.689228 |
| real_anchor | spread_bps | 10 | 0.827981 | 1.37245 | 1.82934 | 3.66695 | 4.42117 |

## Recommendation Ledger

| recommendation_id | value | description |
| --- | --- | --- |
| selected_interpretation | P413_ZERO_EVENT_CAUSE_ATTRIBUTED | Filter attribution completed on Phase411 scan universe. |
| phase412_verdict | P412_REPLENISHMENT_BREAKOUT_REJECTED_AS_ZERO_EVENT_FORM | Phase412 context. |
| largest_stage_fail_counts | breakout_confirmation:840;l2_l5_replenishment:833;l2_l5_imbalance_alignment:602 | Largest all-stage failures. |
| largest_first_failure_stages | top5_alignment:483;impulse_threshold:193;l2_l5_replenishment:157 | Earliest gate failures. |
| threshold_relaxation_allowed | 0 | This diagnostic is not permission to tune Phase410 after seeing results. |
| less_sparse_material_new_required | 1 | Next thesis should be precommitted using lower event sparsity as a design objective. |
| next_action | precommit_material_new_less_sparse_full_depth_l2_thesis_using_phase413_failure_map | Use the failure map to design a materially new full-depth route, not a threshold rescue. |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P413_PHASE412_COMPLETE | True | 1 | 1 | hard |
| P413_SYNTHETIC_SCAN_UNIVERSE_NONEMPTY | True | 840 | >0 | hard |
| P413_REAL_ANCHOR_SCAN_UNIVERSE_REPORTED | True | 10 | >0 | hard |
| P413_STAGE_SUMMARY_COMPLETE | True | 10 | 10 | hard |
| P413_FIRST_FAILURE_SUMMARY_COMPLETE | True | written | written | hard |
| P413_ZERO_EVENT_CONFIRMED | True | 0 | 0 | hard |
| P413_NO_PNL_OR_PROMOTION | True | pnl=0;promotion=0;paper=0;claim=0 | all_zero | hard |
| P413_NO_THRESHOLD_RELAXATION | True | 0 | 0 | hard |
| P413_NEXT_ROUTE_MATERIAL_NEW | True | 1 | 1 | hard |

Boundary: Phase413 is a diagnostic map for future precommit design, not permission to tune Phase410.
