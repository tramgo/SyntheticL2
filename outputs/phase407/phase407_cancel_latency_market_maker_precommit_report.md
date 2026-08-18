# Phase407 Cancel-Latency Market-Maker Realism Precommit

Phase407 records the attached cancel-race charter before any result generation.

It reopens the retail two-sided quoting family only as a material-new, per-tick cancel-race simulator. It does not reopen the P302 directional route and it assumes no maker rebate.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase407_cancel_latency_market_maker_precommit_complete | 1 | Phase407 precommit completed |
| phase407_charter_id | P407_CANCEL_LATENCY_MARKET_MAKER_REALISM | Charter id |
| phase407_latency_grid_rows | 45 | Precommitted latency grid rows |
| phase407_latency_grid_hash | 36a685cb9286bd75bf41384e61c3aacc57d9a63c0b5344d07cf056be416a98e3 | Latency grid hash |
| phase407_jitter_seed | 40720260817 | Pinned jitter seed |
| phase407_real_anchor_date_count | 16 | Local real anchor dates |
| phase407_per_tick_cancel_race_required | 1 | Phase408 must implement per-tick loop |
| phase407_sub100ms_latency_forbidden | 1 | No cancel latency below 100 ms |
| phase407_maker_rebate_assumed | 0 | No maker rebate |
| phase407_cost_multiplier | 2 | Cost200 |
| phase407_initial_capital_inr | 1e+06 | Fixed capital |
| phase407_fixed_notional_per_side_inr | 100000 | Per-side notional |
| phase407_results_generated | 0 | Precommit only |
| phase407_strategy_promotion_allowed | 0 | No promotion |
| phase407_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase407_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase407_hard_gate_pass_rows | 14 | Passed hard gates |
| phase407_hard_gate_rows | 14 | Hard gates |
| phase407_next_best_action | run_phase408_per_tick_cancel_race_market_maker_no_paper_live | Recommended next action |

## Charter

| charter_item | value | description |
| --- | --- | --- |
| charter_id | P407_CANCEL_LATENCY_MARKET_MAKER_REALISM | Phase407 cancel-latency retail two-sided quoting precommit. |
| attachment_sha256 | 4dc4a03759bf58ec8e3d9058bebfe3610b42dbe81395acd5a0c270bb30cb24f3 | Hash of the attached charter text. |
| status | PRECOMMIT_NO_RESULTS_GENERATED | Commit before generating cancel-race results. |
| scope | retail_two_sided_quoting_with_honest_per_tick_cancel_race | Reopens P263 only under material-new cancel-race machinery. |
| p263_relationship | conservative_zero_cancel_closure_stands_until_this_test | This strengthens or supersedes P263; it does not erase it. |
| p300_p302_relationship | directional_passive_aware_closure_stands | This does not reopen P302 directional microstructure closure. |
| p403_relationship | material_new_full_depth_l2_thesis | Per-tick cancel race is new machinery, not same-stack rescue. |
| raw_dense_input | raw_synthetic_l2_dense_full_year_from_phase298 | Per-tick top-five market-by-price lake. |
| full_depth_requirement | levels_1_to_5_price_quantity_orders_with_levels_2_to_5_signal | No L1-only variants. |
| real_anchor_requirement | at_least_3_verified_real_l2_anchor_days | Reserve at least one anchor for cross-check. |
| latency_grid_hash | 36a685cb9286bd75bf41384e61c3aacc57d9a63c0b5344d07cf056be416a98e3 | Hash of precommitted latency grid. |
| cancel_latency_ms_allowed | 150;250;400;700;1000 | No sub-100ms fantasy cancel latency. |
| decide_latency_ms_allowed | 10;20;50 | Trigger-to-decide latency grid. |
| move_threshold_spread_fraction_allowed | 0.25;0.5;0.75 | Cancel trigger threshold grid. |
| jitter_seed | 40720260817 | Pinned deterministic jitter seed. |
| two_sided_required | 1 | Bid and ask must be live simultaneously in the quote window. |
| per_tick_loop_required | 1 | Forbidden to use P262 per-bar EV shortcut or P300 per-event fill draw. |
| cancel_race_required | 1 | Log cancel attempted, succeeded, and lost-race counts. |
| no_rebate | 1 | No maker rebate assumed. |
| cost_model | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha cost model. |
| cost_multiplier | 2 | Cost200 scoring. |
| fixed_capital | 1e+06 | Fixed capital denominator. |
| fixed_notional_per_side | 100000 | Per-side notional at retail scale. |
| acceptance_round_trips | 30 | Completed round-trip floor. |
| acceptance_date_breadth | 5 | Minimum distinct dates. |
| acceptance_symbol_breadth | 3 | Minimum distinct symbols. |
| acceptance_positive_date_fraction | 0.6 | Minimum positive date fraction. |
| acceptance_annualized_pct | 12 | Cost200 fixed-capital annualized floor. |
| strategy_replay_allowed | 0 | Boundary remains closed. |
| strategy_promotion_allowed | 0 | Boundary remains closed. |
| paper_or_live_acceptance_allowed | 0 | Boundary remains closed. |
| deployable_profitability_claim_allowed | 0 | Boundary remains closed. |

## Input Registry

| input_id | value | description |
| --- | --- | --- |
| phase298_dense_root | raw_synthetic_l2_dense_full_year | Raw dense source root. |
| phase298_raw_book_state_l1_l5_required | 1 | Full-depth source requirement. |
| phase298_levels_2_to_5_required | 1 | Levels 2-5 materiality. |
| phase298_l1_only_variant_rows | 0 | Must be zero. |
| phase298_net_edge_live_mask_rows | 0 | Must be zero. |
| phase298_schema_present_columns_min | 30 | Minimum present L1-L5 price/quantity/order columns in Phase298 schema audit. |
| phase300_cost200_survivors | 0 | P300 closure context. |
| phase302_do_not_continue_same_route | 1 | Directional route closure context. |
| phase403_material_new_thesis_required | 1 | P403 requirement. |
| real_anchor_dates | 2026-07-08;2026-07-09;2026-07-10;2026-07-13;2026-07-14;2026-07-15;2026-07-16;2026-07-17;2026-07-20;2026-07-21;2026-07-22;2026-07-23;2026-07-24;2026-07-27;2026-08-03;2026-08-04 | Verified local real L2 anchor dates. |
| real_anchor_date_count | 16 | At least 3 required. |
| execution_results_generated_now | 0 | Precommit only. |

## Latency Grid

| scenario_grid_id | cancel_latency_ms | decide_latency_ms | move_threshold_spread_fraction | jitter_seed | jitter_distribution | maker_rebate_assumed | cost_multiplier |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P407_C150_D10_M0p25_J40720260817 | 150 | 10 | 0.25 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C150_D10_M0p5_J40720260817 | 150 | 10 | 0.5 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C150_D10_M0p75_J40720260817 | 150 | 10 | 0.75 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C150_D20_M0p25_J40720260817 | 150 | 20 | 0.25 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C150_D20_M0p5_J40720260817 | 150 | 20 | 0.5 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C150_D20_M0p75_J40720260817 | 150 | 20 | 0.75 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C150_D50_M0p25_J40720260817 | 150 | 50 | 0.25 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C150_D50_M0p5_J40720260817 | 150 | 50 | 0.5 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C150_D50_M0p75_J40720260817 | 150 | 50 | 0.75 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C250_D10_M0p25_J40720260817 | 250 | 10 | 0.25 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C250_D10_M0p5_J40720260817 | 250 | 10 | 0.5 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C250_D10_M0p75_J40720260817 | 250 | 10 | 0.75 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C250_D20_M0p25_J40720260817 | 250 | 20 | 0.25 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C250_D20_M0p5_J40720260817 | 250 | 20 | 0.5 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C250_D20_M0p75_J40720260817 | 250 | 20 | 0.75 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C250_D50_M0p25_J40720260817 | 250 | 50 | 0.25 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C250_D50_M0p5_J40720260817 | 250 | 50 | 0.5 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C250_D50_M0p75_J40720260817 | 250 | 50 | 0.75 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C400_D10_M0p25_J40720260817 | 400 | 10 | 0.25 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C400_D10_M0p5_J40720260817 | 400 | 10 | 0.5 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C400_D10_M0p75_J40720260817 | 400 | 10 | 0.75 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C400_D20_M0p25_J40720260817 | 400 | 20 | 0.25 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C400_D20_M0p5_J40720260817 | 400 | 20 | 0.5 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C400_D20_M0p75_J40720260817 | 400 | 20 | 0.75 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C400_D50_M0p25_J40720260817 | 400 | 50 | 0.25 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C400_D50_M0p5_J40720260817 | 400 | 50 | 0.5 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C400_D50_M0p75_J40720260817 | 400 | 50 | 0.75 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C700_D10_M0p25_J40720260817 | 700 | 10 | 0.25 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C700_D10_M0p5_J40720260817 | 700 | 10 | 0.5 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C700_D10_M0p75_J40720260817 | 700 | 10 | 0.75 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C700_D20_M0p25_J40720260817 | 700 | 20 | 0.25 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C700_D20_M0p5_J40720260817 | 700 | 20 | 0.5 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C700_D20_M0p75_J40720260817 | 700 | 20 | 0.75 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C700_D50_M0p25_J40720260817 | 700 | 50 | 0.25 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C700_D50_M0p5_J40720260817 | 700 | 50 | 0.5 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C700_D50_M0p75_J40720260817 | 700 | 50 | 0.75 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C1000_D10_M0p25_J40720260817 | 1000 | 10 | 0.25 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C1000_D10_M0p5_J40720260817 | 1000 | 10 | 0.5 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C1000_D10_M0p75_J40720260817 | 1000 | 10 | 0.75 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C1000_D20_M0p25_J40720260817 | 1000 | 20 | 0.25 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C1000_D20_M0p5_J40720260817 | 1000 | 20 | 0.5 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C1000_D20_M0p75_J40720260817 | 1000 | 20 | 0.75 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C1000_D50_M0p25_J40720260817 | 1000 | 50 | 0.25 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C1000_D50_M0p5_J40720260817 | 1000 | 50 | 0.5 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |
| P407_C1000_D50_M0p75_J40720260817 | 1000 | 50 | 0.75 | 40720260817 | stable_truncated_lognormal_rtt_variance_proxy | 0 | 2 |

## Execution Hard-Gate Contract

| gate_id | requirement | severity | phase407_precommitted |
| --- | --- | --- | --- |
| MM_INPUTS_VALIDATED | all five inputs present and schema checked | hard | 1 |
| MM_TICK_LOOP_PRESENT | per-tick loop over resting quote window | hard | 1 |
| MM_CANCEL_RACE_APPLIED | cancel-attempted cancel-succeeded cancel-lost-race counts logged | hard | 1 |
| MM_LATENCY_HONEST | cancel_latency_ms >= 150 in every scenario | hard | 1 |
| MM_NO_REBATE_ASSUMED | full Zerodha charges, no maker rebate | hard | 1 |
| MM_TWO_SIDED_REQUIRED | bid and ask live simultaneously | hard | 1 |
| MM_FULL_DEPTH_L2_L5 | at least one signal from levels 2-5 | hard | 1 |
| MM_NO_LOOKAHEAD | feature timestamps precede quote-post timestamps and loop is time ordered | hard | 1 |
| MM_COST200_SCORING | cost_multiplier=2, fixed capital, per-side notional <= 100000 | hard | 1 |
| MM_EVENT_FLOOR | at least 30 completed round trips | hard | 1 |
| MM_DATE_BREADTH | at least 5 trade dates with round trips | hard | 1 |
| MM_SYMBOL_BREADTH | at least 3 symbols with round trips | hard | 1 |
| MM_POSITIVE_DATE_FRACTION | at least 60 percent positive round-trip dates | hard | 1 |
| MM_ANNUALIZED_FLOOR | fixed-capital annualized return >= 12 percent at cost200 | hard | 1 |
| MM_NO_RANK_REVERSAL | best cost200 scenario remains top quartile at cost100 | hard | 1 |
| MM_LATENCY_MONOTONICITY | net PnL decreases as cancel latency increases for winner | hard | 1 |
| MM_REAL_ANCHOR_CROSS_CHECK | winning scenario sign preserved on reserved real anchor day | hard | 1 |
| MM_BOUNDARIES_CLOSED | replay=0 promotion=0 paper_live=0 claim=0 | hard | 1 |

## Precommit Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P407_ATTACHMENT_PRESENT | True | 1 | 1 | hard |
| P407_ATTACHMENT_CANCEL_RACE_CHARTER | True | cancel_race=1;p407=1 | cancel_race_p407 | hard |
| P407_PHASE298_RAW_DENSE_PRESENT | True | raw_synthetic_l2_dense_full_year | raw_synthetic_l2_dense_full_year | hard |
| P407_FULL_DEPTH_SCHEMA_PRESENT | True | 30 | >=30 | hard |
| P407_L1_ONLY_FORBIDDEN | True | 0 | 0 | hard |
| P407_NO_LOOKAHEAD_SOURCE | True | 0 | 0 | hard |
| P407_REAL_ANCHORS_AT_LEAST_THREE | True | 16 | >=3 | hard |
| P407_LATENCY_GRID_PINNED | True | 45 | 45 | hard |
| P407_LATENCY_HONEST | True | 150 | >=150 | hard |
| P407_NO_REBATE_PINNED | True | 0 | 0 | hard |
| P407_COST200_FIXED_CAPITAL_PINNED | True | cost=2.0;capital=1000000.0;notional=100000.0 | cost200_fixed_capital | hard |
| P407_ALL_MM_HARD_GATES_PRECOMMITTED | True | 18 | 18 | hard |
| P407_RESULTS_NOT_GENERATED | True | 0 | 0 | hard |
| P407_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |

No Phase407 execution results are generated by this precommit.
