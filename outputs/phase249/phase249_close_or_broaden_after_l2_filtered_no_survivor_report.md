# Phase249 Close or Broaden After L2-filtered No-survivor Search

Generated UTC: 2026-07-29T09:28:40.866006+00:00

Phase249 closes the current single-name bar-return reversal branch under the present evidence and opens only materially different research routes.
It does not download data, rerun holdout dates, relax thresholds, promote a strategy, or open paper/live acceptance.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase249_close_or_broaden_complete | 1 | Phase249 close/broaden decision completed |
| phase249_closed_scope | single_name_bar_return_reversal_with_top5_depth_filters | Scope closed under current evidence |
| phase249_phase248_variant_rows | 1728 | Phase248 variants considered |
| phase249_phase248_cost200_positive_rows | 0 | Phase248 2x-cost positive variants |
| phase249_phase248_survivor_rows | 0 | Phase248 controlled survivors |
| phase249_closure_rows | 3 | Closure ledger rows |
| phase249_failure_attribution_rows | 5 | Failure attribution rows |
| phase249_broaden_queue_rows | 4 | Materially different broaden routes |
| phase249_selected_next_route | P249_PAIR_OR_BASKET_RELATIVE_VALUE | Highest-priority next route |
| phase249_threshold_relaxation_only_allowed | 0 | No threshold relaxation loop |
| phase249_download_more_dates_now_allowed | 0 | No raw-date download in Phase249 |
| phase249_replay_execution_allowed_now | 0 | No replay execution in Phase249 |
| phase249_strategy_promotion_allowed | 0 | No strategy promotion from Phase249 |
| phase249_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase249 |
| phase249_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase249 |
| phase249_hard_gate_pass_rows | 6 | Hard gates passed |
| phase249_hard_gate_rows | 6 | Hard gates evaluated |
| phase249_next_best_action | run_phase250_pair_basket_relative_value_precommit_no_downloads_no_2026_07_17_or_2026_07_20_tuning_no_paper_live | Recommended next milestone |

## Closure Ledger

| decision_id | scope | decision | observed_value | required_value | rationale | reuse_allowed_without_material_redesign |
| --- | --- | --- | --- | --- | --- | --- |
| P249_CLOSE_SINGLE_NAME_BAR_RETURN_REVERSAL | single_name_bar_return_reversal_with_top5_depth_filters | closed_for_current_evidence_set | 0 | >0 controlled survivors | Phase248 found no controlled survivor after adding top-five imbalance, spread/liquidity, event-intensity and range/market guards. | 0 |
| P249_BLOCK_THRESHOLD_RELAXATION_LOOP | phase248_variant_thresholds | blocked | 0 | >0 positive at 2x modeled costs | Relaxing thresholds after zero 2x-cost positives would optimize toward cost-fragile sparse artifacts. | 0 |
| P249_NO_MORE_DOWNLOADS_FOR_CLOSED_BRANCH | fresh_real_l2_dates | blocked_for_closed_parent | 0 | future_holdout_precommit_allowed=1 | No candidate qualifies for fresh holdout, so more date downloads would spend disk without a testable frozen candidate. | 0 |

## Failure Attribution

| failure_mode | observed_metric | observed_value | interpretation |
| --- | --- | --- | --- |
| cost_floor_dominates_l2_filtered_reversal | phase248_cost200_positive_variant_rows | 0 | No combined-filter variant survived 2.0x modeled Zerodha costs. |
| sparse_positive_artifacts | phase248_best_trade_rows | 1 | Best apparent candidate had one trade, one date and one symbol, so it is not a strategy. |
| no_controlled_survivors | phase248_survivor_candidate_rows | 0 | No candidate reached the control stage with sufficient cost-stress and breadth. |
| gate_failed_P248_COST200_POSITIVE_VARIANTS_FOUND | P248_COST200_POSITIVE_VARIANTS_FOUND | 0 | Gate failed against requirement >0 positive at 2x cost. |
| gate_failed_P248_CONTROLLED_SURVIVOR_FOUND | P248_CONTROLLED_SURVIVOR_FOUND | 0 | Gate failed against requirement >0 controlled survivors. |

## Material Broaden Queue

| priority | route_id | route | why_materially_different | allowed_sources | precommit_next | replay_allowed_now |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | P249_PAIR_OR_BASKET_RELATIVE_VALUE | pair_or_basket_relative_value | Moves from single-name reversal to cross-sectional / market-neutral effects where common market shock is hedged. | same existing real event bars plus symbol basket normalization; no new raw downloads | phase250_pair_basket_relative_value_precommit | 0 |
| 2 | P249_TOP5_DEPTH_PREDICTIVE_TARGET | top5_depth_as_predictive_target_or_source | Uses L2 imbalance transitions as the signal source/target rather than only a filter around bar reversal. | avg_top5_market_by_price_imbalance, avg_l1_imbalance, quote churn, depth refresh, future mid returns | phase250_top5_depth_predictive_target_precommit | 0 |
| 3 | P249_OPENING_SHOCK_SEPARATION | opening_shock_vs_normal_intraday_separation | Separates open-auction shock/price-discovery behavior from normal intraday microstructure instead of mixing regimes. | event-bar time buckets already available in Phase235/246 outputs | phase250_opening_shock_separation_precommit | 0 |
| 4 | P249_CONSERVATIVE_PASSIVE_FILL_MODEL | passive_limit_order_queue_model_only_if_fill_probability_conservative | Tests whether maker-style execution can overcome taker cost drag, but only with pessimistic fill probability and adverse-selection controls. | top-five market-by-price depth, spread, quote churn, depth refresh, stale quote duration | phase250_passive_fill_model_precommit | 0 |

## Guardrail Ledger

| guardrail_id | requirement | active |
| --- | --- | --- |
| P249_NO_PROFITABILITY_CLAIM | No deployable profitability claim because Phase248 found zero survivors. | 1 |
| P249_NO_MORE_DATE_DOWNLOAD | No more fresh real L2 date downloads until a materially new frozen candidate exists. | 1 |
| P249_NO_HOLDOUT_TUNING | 2026-07-17 and 2026-07-20 remain forbidden tuning dates for descendants. | 1 |
| P249_NO_THRESHOLD_RELAXATION_ONLY | Threshold relaxation alone is blocked; next route must be materially different. | 1 |
| P249_COST_STRESS_FIRST_REMAINS | 2.0x modeled Zerodha cost positivity remains a first-class search objective. | 1 |
| P249_RANDOM_SIDE_SIDE_FLIP_REMAIN | Random-side and side-flip controls remain mandatory before holdout. | 1 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P249_PHASE248_WORK_ORDER_PRESENT | True | close_or_broaden_phase248_l2_imbalance_regime_filtered_search_no_downloads_no_paper_live | Phase248 next action asks close/broaden | hard |
| P249_CLOSURE_LEDGER_WRITTEN | True | 3 | >=3 closure rows | hard |
| P249_FAILURE_ATTRIBUTION_WRITTEN | True | 5 | >=3 failure attribution rows | hard |
| P249_MATERIAL_BROADEN_QUEUE_WRITTEN | True | 4 | >=3 materially different routes | hard |
| P249_GUARDRAILS_ACTIVE | True | all active | all guardrails active | hard |
| P249_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE | True | 0 | 0 | hard |
