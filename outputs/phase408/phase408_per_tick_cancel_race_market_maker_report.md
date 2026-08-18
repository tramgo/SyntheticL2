# Phase408 Per-Tick Cancel-Race Market-Maker Execution

Phase408 executes the Phase407 cancel-latency charter using a bounded per-tick market-by-price cancel-race simulator.

Fills remain inferred from received ticks and last-price/quote crossings; exact exchange queue identity is not claimed.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase408_per_tick_cancel_race_market_maker_complete | 1 | Phase408 execution completed |
| phase408_synthetic_scenario_rows | 45 | Synthetic scenario rows |
| phase408_real_anchor_scenario_rows | 45 | Real-anchor scenario rows |
| phase408_best_scenario_id | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C150_D10_M0p25_J40720260817 | Best synthetic scenario |
| phase408_best_scenario_grid_id | P407_C150_D10_M0p25_J40720260817 | Best grid id |
| phase408_best_cancel_latency_ms | 150 | Best cancel latency |
| phase408_best_completed_round_trips | 152 | Best completed round trips |
| phase408_best_trade_dates | 5 | Best trade dates |
| phase408_best_symbols | 5 | Best symbols |
| phase408_best_positive_date_fraction | 0 | Best positive date fraction |
| phase408_best_net_pnl_inr | -47401.8 | Best net PnL |
| phase408_best_annualized_return_pct | -238.905 | Best annualized return |
| phase408_cost200_acceptance_survivor_rows | 0 | Cost200 acceptance survivors |
| phase408_kill_switch_triggered | 1 | Kill if no survivors or hard gates fail |
| phase408_strategy_promotion_allowed | 0 | No promotion |
| phase408_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase408_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase408_hard_gate_pass_rows | 15 | Passed hard gates |
| phase408_hard_gate_rows | 18 | Hard gates |
| phase408_next_best_action | interpret_phase408_cancel_race_market_maker_no_paper_live | Recommended next action |

## Top Synthetic Scenarios

| panel | scenario_id | scenario_grid_id | cancel_latency_ms | decide_latency_ms | move_threshold_spread_fraction | quote_side_rows | cancel_attempted_rows | cancel_succeeded_rows | cancel_lost_race_rows | completed_round_trips | trade_dates | symbols | positive_date_fraction | net_pnl_inr | annualized_return_pct | above12 | event_floor_met | date_breadth_met | symbol_breadth_met | positive_date_fraction_met | cost200_acceptance_survivor | avg_effective_cancel_latency_ms | avg_lost_race_net_pnl_inr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| synthetic_dense | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C150_D10_M0p25_J40720260817 | P407_C150_D10_M0p25_J40720260817 | 150 | 10 | 0.25 | 300 | 152 | 0 | 152 | 152 | 5 | 5 | 0 | -47401.8 | -238.905 | 0 | 1 | 1 | 1 | 0 | 0 | 148.282 | -311.854 |
| synthetic_dense | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C150_D10_M0p5_J40720260817 | P407_C150_D10_M0p5_J40720260817 | 150 | 10 | 0.5 | 300 | 152 | 0 | 152 | 152 | 5 | 5 | 0 | -47401.8 | -238.905 | 0 | 1 | 1 | 1 | 0 | 0 | 149.778 | -311.854 |
| synthetic_dense | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C150_D10_M0p75_J40720260817 | P407_C150_D10_M0p75_J40720260817 | 150 | 10 | 0.75 | 300 | 152 | 0 | 152 | 152 | 5 | 5 | 0 | -47401.8 | -238.905 | 0 | 1 | 1 | 1 | 0 | 0 | 148.324 | -311.854 |
| synthetic_dense | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C150_D20_M0p25_J40720260817 | P407_C150_D20_M0p25_J40720260817 | 150 | 20 | 0.25 | 300 | 152 | 0 | 152 | 152 | 5 | 5 | 0 | -47401.8 | -238.905 | 0 | 1 | 1 | 1 | 0 | 0 | 149.962 | -311.854 |
| synthetic_dense | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C150_D20_M0p5_J40720260817 | P407_C150_D20_M0p5_J40720260817 | 150 | 20 | 0.5 | 300 | 152 | 0 | 152 | 152 | 5 | 5 | 0 | -47401.8 | -238.905 | 0 | 1 | 1 | 1 | 0 | 0 | 151.147 | -311.854 |
| synthetic_dense | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C150_D20_M0p75_J40720260817 | P407_C150_D20_M0p75_J40720260817 | 150 | 20 | 0.75 | 300 | 152 | 0 | 152 | 152 | 5 | 5 | 0 | -47401.8 | -238.905 | 0 | 1 | 1 | 1 | 0 | 0 | 149.837 | -311.854 |
| synthetic_dense | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C150_D50_M0p25_J40720260817 | P407_C150_D50_M0p25_J40720260817 | 150 | 50 | 0.25 | 300 | 152 | 0 | 152 | 152 | 5 | 5 | 0 | -47401.8 | -238.905 | 0 | 1 | 1 | 1 | 0 | 0 | 150.131 | -311.854 |
| synthetic_dense | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C150_D50_M0p5_J40720260817 | P407_C150_D50_M0p5_J40720260817 | 150 | 50 | 0.5 | 300 | 152 | 0 | 152 | 152 | 5 | 5 | 0 | -47401.8 | -238.905 | 0 | 1 | 1 | 1 | 0 | 0 | 149.454 | -311.854 |
| synthetic_dense | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C150_D50_M0p75_J40720260817 | P407_C150_D50_M0p75_J40720260817 | 150 | 50 | 0.75 | 300 | 152 | 0 | 152 | 152 | 5 | 5 | 0 | -47401.8 | -238.905 | 0 | 1 | 1 | 1 | 0 | 0 | 151.667 | -311.854 |
| synthetic_dense | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C250_D10_M0p25_J40720260817 | P407_C250_D10_M0p25_J40720260817 | 250 | 10 | 0.25 | 300 | 152 | 0 | 152 | 152 | 5 | 5 | 0 | -47401.8 | -238.905 | 0 | 1 | 1 | 1 | 0 | 0 | 249.589 | -311.854 |
| synthetic_dense | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C250_D10_M0p5_J40720260817 | P407_C250_D10_M0p5_J40720260817 | 250 | 10 | 0.5 | 300 | 152 | 0 | 152 | 152 | 5 | 5 | 0 | -47401.8 | -238.905 | 0 | 1 | 1 | 1 | 0 | 0 | 249.178 | -311.854 |
| synthetic_dense | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C250_D10_M0p75_J40720260817 | P407_C250_D10_M0p75_J40720260817 | 250 | 10 | 0.75 | 300 | 152 | 0 | 152 | 152 | 5 | 5 | 0 | -47401.8 | -238.905 | 0 | 1 | 1 | 1 | 0 | 0 | 248.106 | -311.854 |
| synthetic_dense | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C250_D20_M0p25_J40720260817 | P407_C250_D20_M0p25_J40720260817 | 250 | 20 | 0.25 | 300 | 152 | 0 | 152 | 152 | 5 | 5 | 0 | -47401.8 | -238.905 | 0 | 1 | 1 | 1 | 0 | 0 | 248.618 | -311.854 |
| synthetic_dense | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C250_D20_M0p5_J40720260817 | P407_C250_D20_M0p5_J40720260817 | 250 | 20 | 0.5 | 300 | 152 | 0 | 152 | 152 | 5 | 5 | 0 | -47401.8 | -238.905 | 0 | 1 | 1 | 1 | 0 | 0 | 249.85 | -311.854 |
| synthetic_dense | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C250_D20_M0p75_J40720260817 | P407_C250_D20_M0p75_J40720260817 | 250 | 20 | 0.75 | 300 | 152 | 0 | 152 | 152 | 5 | 5 | 0 | -47401.8 | -238.905 | 0 | 1 | 1 | 1 | 0 | 0 | 251.214 | -311.854 |

## Real Anchor Scenarios

| panel | scenario_id | scenario_grid_id | cancel_latency_ms | decide_latency_ms | move_threshold_spread_fraction | quote_side_rows | cancel_attempted_rows | cancel_succeeded_rows | cancel_lost_race_rows | completed_round_trips | trade_dates | symbols | positive_date_fraction | net_pnl_inr | annualized_return_pct | above12 | event_floor_met | date_breadth_met | symbol_breadth_met | positive_date_fraction_met | cost200_acceptance_survivor | avg_effective_cancel_latency_ms | avg_lost_race_net_pnl_inr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| real_anchor_reserved | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C150_D10_M0p25_J40720260817 | P407_C150_D10_M0p25_J40720260817 | 150 | 10 | 0.25 | 36 | 14 | 1 | 13 | 32 | 1 | 3 | 0 | -6273.62 | -158.095 | 0 | 1 | 0 | 1 | 0 | 0 | 151.145 | -259.614 |
| real_anchor_reserved | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C150_D10_M0p5_J40720260817 | P407_C150_D10_M0p5_J40720260817 | 150 | 10 | 0.5 | 36 | 11 | 1 | 10 | 32 | 1 | 3 | 0 | -6273.62 | -158.095 | 0 | 1 | 0 | 1 | 0 | 0 | 141.135 | -294.331 |
| real_anchor_reserved | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C150_D10_M0p75_J40720260817 | P407_C150_D10_M0p75_J40720260817 | 150 | 10 | 0.75 | 36 | 9 | 1 | 8 | 32 | 1 | 3 | 0 | -6273.62 | -158.095 | 0 | 1 | 0 | 1 | 0 | 0 | 147.487 | -322.428 |
| real_anchor_reserved | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C150_D20_M0p25_J40720260817 | P407_C150_D20_M0p25_J40720260817 | 150 | 20 | 0.25 | 36 | 14 | 1 | 13 | 32 | 1 | 3 | 0 | -6273.62 | -158.095 | 0 | 1 | 0 | 1 | 0 | 0 | 147.966 | -259.614 |
| real_anchor_reserved | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C150_D20_M0p5_J40720260817 | P407_C150_D20_M0p5_J40720260817 | 150 | 20 | 0.5 | 36 | 11 | 1 | 10 | 32 | 1 | 3 | 0 | -6273.62 | -158.095 | 0 | 1 | 0 | 1 | 0 | 0 | 150.354 | -294.331 |
| real_anchor_reserved | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C150_D20_M0p75_J40720260817 | P407_C150_D20_M0p75_J40720260817 | 150 | 20 | 0.75 | 36 | 9 | 1 | 8 | 32 | 1 | 3 | 0 | -6273.62 | -158.095 | 0 | 1 | 0 | 1 | 0 | 0 | 147.995 | -322.428 |
| real_anchor_reserved | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C150_D50_M0p25_J40720260817 | P407_C150_D50_M0p25_J40720260817 | 150 | 50 | 0.25 | 36 | 14 | 1 | 13 | 32 | 1 | 3 | 0 | -6273.62 | -158.095 | 0 | 1 | 0 | 1 | 0 | 0 | 149.062 | -259.614 |
| real_anchor_reserved | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C150_D50_M0p5_J40720260817 | P407_C150_D50_M0p5_J40720260817 | 150 | 50 | 0.5 | 36 | 11 | 1 | 10 | 32 | 1 | 3 | 0 | -6273.62 | -158.095 | 0 | 1 | 0 | 1 | 0 | 0 | 147.4 | -294.331 |
| real_anchor_reserved | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C150_D50_M0p75_J40720260817 | P407_C150_D50_M0p75_J40720260817 | 150 | 50 | 0.75 | 36 | 9 | 1 | 8 | 32 | 1 | 3 | 0 | -6273.62 | -158.095 | 0 | 1 | 0 | 1 | 0 | 0 | 145.862 | -322.428 |
| real_anchor_reserved | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C250_D10_M0p25_J40720260817 | P407_C250_D10_M0p25_J40720260817 | 250 | 10 | 0.25 | 36 | 14 | 1 | 13 | 32 | 1 | 3 | 0 | -6273.62 | -158.095 | 0 | 1 | 0 | 1 | 0 | 0 | 243.134 | -259.614 |
| real_anchor_reserved | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C250_D10_M0p5_J40720260817 | P407_C250_D10_M0p5_J40720260817 | 250 | 10 | 0.5 | 36 | 11 | 1 | 10 | 32 | 1 | 3 | 0 | -6273.62 | -158.095 | 0 | 1 | 0 | 1 | 0 | 0 | 249.289 | -294.331 |
| real_anchor_reserved | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C250_D10_M0p75_J40720260817 | P407_C250_D10_M0p75_J40720260817 | 250 | 10 | 0.75 | 36 | 9 | 1 | 8 | 32 | 1 | 3 | 0 | -6273.62 | -158.095 | 0 | 1 | 0 | 1 | 0 | 0 | 249.023 | -322.428 |
| real_anchor_reserved | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C250_D20_M0p25_J40720260817 | P407_C250_D20_M0p25_J40720260817 | 250 | 20 | 0.25 | 36 | 14 | 1 | 13 | 32 | 1 | 3 | 0 | -6273.62 | -158.095 | 0 | 1 | 0 | 1 | 0 | 0 | 247.002 | -259.614 |
| real_anchor_reserved | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C250_D20_M0p5_J40720260817 | P407_C250_D20_M0p5_J40720260817 | 250 | 20 | 0.5 | 36 | 11 | 1 | 10 | 32 | 1 | 3 | 0 | -6273.62 | -158.095 | 0 | 1 | 0 | 1 | 0 | 0 | 252.473 | -294.331 |
| real_anchor_reserved | P408_P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER_P407_C250_D20_M0p75_J40720260817 | P407_C250_D20_M0p75_J40720260817 | 250 | 20 | 0.75 | 36 | 9 | 1 | 8 | 32 | 1 | 3 | 0 | -6273.62 | -158.095 | 0 | 1 | 0 | 1 | 0 | 0 | 246.524 | -322.428 |

## Latency Curves

| decide_latency_ms | move_threshold_spread_fraction | latency_curve_points | net_pnl_curve | latency_pnl_range_inr | latency_material_effect | latency_monotone_decreasing |
| --- | --- | --- | --- | --- | --- | --- |
| 10 | 0.25 | 5 | -47401.7856;-47401.7856;-47401.7856;-47401.7856;-47401.7856 | 0 | 0 | 0 |
| 10 | 0.5 | 5 | -47401.7856;-47401.7856;-47401.7856;-47401.7856;-47401.7856 | 0 | 0 | 0 |
| 10 | 0.75 | 5 | -47401.7856;-47401.7856;-47401.7856;-47401.7856;-47401.7856 | 0 | 0 | 0 |
| 20 | 0.25 | 5 | -47401.7856;-47401.7856;-47401.7856;-47401.7856;-47401.7856 | 0 | 0 | 0 |
| 20 | 0.5 | 5 | -47401.7856;-47401.7856;-47401.7856;-47401.7856;-47401.7856 | 0 | 0 | 0 |
| 20 | 0.75 | 5 | -47401.7856;-47401.7856;-47401.7856;-47401.7856;-47401.7856 | 0 | 0 | 0 |
| 50 | 0.25 | 5 | -47401.7856;-47401.7856;-47401.7856;-47401.7856;-47401.7856 | 0 | 0 | 0 |
| 50 | 0.5 | 5 | -47401.7856;-47401.7856;-47401.7856;-47401.7856;-47401.7856 | 0 | 0 | 0 |
| 50 | 0.75 | 5 | -47401.7856;-47401.7856;-47401.7856;-47401.7856;-47401.7856 | 0 | 0 | 0 |

## Hard Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| MM_INPUTS_VALIDATED | True | synthetic_scenarios=45;real_scenarios=45 | >0 | hard |
| MM_TICK_LOOP_PRESENT | True | per_tick_window_loop | present | hard |
| MM_CANCEL_RACE_APPLIED | True | cancel_attempted;succeeded;lost_race | logged | hard |
| MM_LATENCY_HONEST | True | 150 | >=150 | hard |
| MM_NO_REBATE_ASSUMED | True | maker_rebate=0 | 0 | hard |
| MM_TWO_SIDED_REQUIRED | True | bid_and_ask_quoted_each_window | required | hard |
| MM_FULL_DEPTH_L2_L5 | True | l2_l5_signal_abs_filter | required | hard |
| MM_NO_LOOKAHEAD | True | ticks_sorted_exchange_timestamp_and_forward_loop | required | hard |
| MM_COST200_SCORING | True | cost_multiplier=2.0;capital=1000000.0;notional=100000.0 | cost200_fixed_capital | hard |
| MM_EVENT_FLOOR | True | 152 | >=30 | hard |
| MM_DATE_BREADTH | True | 5 | >=5 | hard |
| MM_SYMBOL_BREADTH | True | 5 | >=3 | hard |
| MM_POSITIVE_DATE_FRACTION | False | 0 | >=0.6 | hard |
| MM_ANNUALIZED_FLOOR | False | -238.905 | >=12.0 | hard |
| MM_NO_RANK_REVERSAL | True | 1 | 1 | hard |
| MM_LATENCY_MONOTONICITY | False | 0 | 1 | hard |
| MM_REAL_ANCHOR_CROSS_CHECK | True | 1 | 1 | hard |
| MM_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |

No promotion, paper/live acceptance, deployable profitability claim, or maker rebate is opened.
