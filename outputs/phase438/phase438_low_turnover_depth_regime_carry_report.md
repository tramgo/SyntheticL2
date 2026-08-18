# Phase438 Low-Turnover Full-Depth Regime Carry Execution

Phase438 executes the Phase437 lower-turnover source: one early-session full-depth regime trade per symbol/date with longer hold horizons.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase438_low_turnover_depth_regime_complete | 1 | Phase438 execution completed |
| phase438_thesis_id | P438_LOW_TURNOVER_FULL_DEPTH_REGIME_CARRY_EXECUTION | Execution thesis |
| phase438_synthetic_tick_rows_loaded | 1920000 | Synthetic tick rows loaded |
| phase438_synthetic_trade_dates_loaded | 12 | Synthetic dates loaded |
| phase438_synthetic_symbols_loaded | 32 | Synthetic symbols loaded |
| phase438_best_scenario_id | P438_depth_regime_snapback_E120_H2400_D5 | Best active synthetic scenario |
| phase438_best_family_id | depth_regime_snapback | Best family |
| phase438_best_completed_round_trips | 384 | Best round trips |
| phase438_best_trade_dates | 12 | Best trade dates |
| phase438_best_symbols | 32 | Best symbols |
| phase438_best_positive_date_fraction | 0 | Best positive date fraction |
| phase438_best_gross_pnl_inr | -4844.56 | Best gross P&L |
| phase438_best_cost200_inr | 63222 | Best cost200 charges |
| phase438_best_net_pnl_inr | -68066.6 | Best net P&L |
| phase438_best_annualized_return_pct | -142.94 | Best annualized return |
| phase438_real_anchor_best_annualized_return_pct | -10.1693 | Real-anchor best annualized return |
| phase438_cost200_acceptance_survivor_rows | 0 | Synthetic acceptance survivors before controls |
| phase438_strategy_promotion_allowed | 0 | No promotion |
| phase438_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase438_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase438_hard_gate_pass_rows | 11 | Passed hard gates |
| phase438_hard_gate_rows | 14 | Hard gates |
| phase438_next_best_action | interpret_phase438_low_turnover_depth_regime_carry_no_paper_live | Recommended next action |

## Synthetic Scenario Summary

| panel | scenario_id | family_id | completed_round_trips | trade_dates | symbols | positive_date_fraction | gross_pnl_inr | cost200_inr | net_pnl_inr | annualized_return_pct | acceptance_survivor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| synthetic | P438_depth_regime_snapback_E120_H2400_D5 | depth_regime_snapback | 384 | 12 | 32 | 0 | -4844.56 | 63222 | -68066.6 | -142.94 | 0 |
| synthetic | P438_depth_regime_snapback_E240_H2400_D5 | depth_regime_snapback | 384 | 12 | 32 | 0 | -4996.96 | 63224 | -68221 | -143.264 | 0 |
| synthetic | P438_depth_regime_snapback_E120_H1200_D5 | depth_regime_snapback | 384 | 12 | 32 | 0 | -5924.82 | 63218.9 | -69143.7 | -145.202 | 0 |
| synthetic | P438_depth_regime_snapback_E480_H2400_D5 | depth_regime_snapback | 384 | 12 | 32 | 0 | -6024.36 | 63224.3 | -69248.7 | -145.422 | 0 |
| synthetic | P438_depth_regime_snapback_E240_H1200_D5 | depth_regime_snapback | 384 | 12 | 32 | 0 | -6077.22 | 63220.9 | -69298.1 | -145.526 | 0 |
| synthetic | P438_depth_regime_snapback_E480_H1200_D5 | depth_regime_snapback | 384 | 12 | 32 | 0 | -6827.53 | 63223.6 | -70051.1 | -147.107 | 0 |
| synthetic | P438_depth_regime_carry_E480_H3600_D5 | depth_regime_carry | 384 | 12 | 32 | 0 | -7380.38 | 63220.8 | -70601.2 | -148.263 | 0 |
| synthetic | P438_depth_regime_snapback_E120_H3600_D5 | depth_regime_snapback | 384 | 12 | 32 | 0 | -7412.53 | 63219.5 | -70632.1 | -148.327 | 0 |
| synthetic | P438_depth_regime_snapback_E240_H3600_D5 | depth_regime_snapback | 384 | 12 | 32 | 0 | -7564.93 | 63221.6 | -70786.5 | -148.652 | 0 |
| synthetic | P438_depth_regime_carry_E240_H3600_D5 | depth_regime_carry | 384 | 12 | 32 | 0 | -10113.8 | 63222.5 | -73336.3 | -154.006 | 0 |
| synthetic | P438_depth_regime_carry_E120_H3600_D5 | depth_regime_carry | 384 | 12 | 32 | 0 | -10266.2 | 63220.5 | -73486.7 | -154.322 | 0 |
| synthetic | P438_depth_regime_snapback_E480_H3600_D5 | depth_regime_snapback | 384 | 12 | 32 | 0 | -10306.4 | 63220.1 | -73526.5 | -154.406 | 0 |
| synthetic | P438_depth_regime_carry_E480_H1200_D5 | depth_regime_carry | 384 | 12 | 32 | 0 | -10846.1 | 63224.6 | -74070.7 | -155.548 | 0 |
| synthetic | P438_depth_regime_carry_E240_H1200_D5 | depth_regime_carry | 384 | 12 | 32 | 0 | -11595.5 | 63221.9 | -74817.5 | -157.117 | 0 |
| synthetic | P438_depth_regime_carry_E480_H2400_D5 | depth_regime_carry | 384 | 12 | 32 | 0 | -11660.6 | 63225.3 | -74885.9 | -157.26 | 0 |
| synthetic | P438_depth_regime_carry_E120_H1200_D5 | depth_regime_carry | 384 | 12 | 32 | 0 | -11747.9 | 63219.9 | -74967.8 | -157.432 | 0 |
| synthetic | P438_depth_regime_carry_E240_H2400_D5 | depth_regime_carry | 384 | 12 | 32 | 0 | -12687.2 | 63225.1 | -75912.3 | -159.416 | 0 |
| synthetic | P438_depth_regime_carry_E120_H2400_D5 | depth_regime_carry | 384 | 12 | 32 | 0 | -12839.6 | 63223.1 | -76062.7 | -159.732 | 0 |

## Control Summary For Best Scenario

| control | panel | scenario_id | family_id | completed_round_trips | trade_dates | symbols | positive_date_fraction | gross_pnl_inr | cost200_inr | net_pnl_inr | annualized_return_pct | acceptance_survivor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| l1_only | synthetic_l1_only | P438_depth_regime_snapback_E120_H2400_D5 | depth_regime_snapback | 384 | 12 | 32 | 0 | -4844.56 | 63222 | -68066.6 | -142.94 | 0 |
| side_flip | synthetic_side_flip | P438_depth_regime_snapback_E120_H2400_D5 | depth_regime_snapback | 384 | 12 | 32 | 0 | -12839.6 | 63223.1 | -76062.7 | -159.732 | 0 |
| time_shuffle | synthetic_time_shuffle | P438_depth_regime_snapback_E120_H2400_D5 | depth_regime_snapback | 384 | 12 | 32 | 0 | -11093.2 | 63223 | -74316.2 | -156.064 | 0 |

## Real-Anchor Summary

| panel | scenario_id | family_id | completed_round_trips | trade_dates | symbols | positive_date_fraction | gross_pnl_inr | cost200_inr | net_pnl_inr | annualized_return_pct | acceptance_survivor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| real_anchor | P438_depth_regime_carry_E480_H3600_D5 | depth_regime_carry | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| real_anchor | P438_depth_regime_carry_E480_H2400_D5 | depth_regime_carry | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| real_anchor | P438_depth_regime_snapback_E480_H3600_D5 | depth_regime_snapback | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| real_anchor | P438_depth_regime_snapback_E480_H1200_D5 | depth_regime_snapback | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| real_anchor | P438_depth_regime_carry_E480_H1200_D5 | depth_regime_carry | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| real_anchor | P438_depth_regime_snapback_E480_H2400_D5 | depth_regime_snapback | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| real_anchor | P438_depth_regime_carry_E240_H3600_D5 | depth_regime_carry | 5 | 2 | 3 | 0 | 19.12 | 826.209 | -807.089 | -10.1693 | 0 |
| real_anchor | P438_depth_regime_carry_E240_H1200_D5 | depth_regime_carry | 5 | 2 | 3 | 0 | 19.12 | 826.209 | -807.089 | -10.1693 | 0 |
| real_anchor | P438_depth_regime_carry_E240_H2400_D5 | depth_regime_carry | 5 | 2 | 3 | 0 | 19.12 | 826.209 | -807.089 | -10.1693 | 0 |
| real_anchor | P438_depth_regime_snapback_E240_H3600_D5 | depth_regime_snapback | 5 | 2 | 3 | 0 | -301.39 | 826.221 | -1127.61 | -14.2079 | 0 |
| real_anchor | P438_depth_regime_snapback_E240_H1200_D5 | depth_regime_snapback | 5 | 2 | 3 | 0 | -301.39 | 826.221 | -1127.61 | -14.2079 | 0 |
| real_anchor | P438_depth_regime_snapback_E240_H2400_D5 | depth_regime_snapback | 5 | 2 | 3 | 0 | -301.39 | 826.221 | -1127.61 | -14.2079 | 0 |
| real_anchor | P438_depth_regime_carry_E120_H2400_D5 | depth_regime_carry | 8 | 2 | 6 | 0 | 178.11 | 1316.84 | -1138.73 | -14.348 | 0 |
| real_anchor | P438_depth_regime_carry_E120_H1200_D5 | depth_regime_carry | 8 | 2 | 6 | 0 | 178.11 | 1316.84 | -1138.73 | -14.348 | 0 |
| real_anchor | P438_depth_regime_carry_E120_H3600_D5 | depth_regime_carry | 8 | 2 | 6 | 0 | 178.11 | 1316.84 | -1138.73 | -14.348 | 0 |
| real_anchor | P438_depth_regime_snapback_E120_H1200_D5 | depth_regime_snapback | 8 | 2 | 6 | 0 | -687.9 | 1316.47 | -2004.37 | -25.2551 | 0 |
| real_anchor | P438_depth_regime_snapback_E120_H2400_D5 | depth_regime_snapback | 8 | 2 | 6 | 0 | -687.9 | 1316.47 | -2004.37 | -25.2551 | 0 |
| real_anchor | P438_depth_regime_snapback_E120_H3600_D5 | depth_regime_snapback | 8 | 2 | 6 | 0 | -687.9 | 1316.47 | -2004.37 | -25.2551 | 0 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P438_PHASE437_PRECOMMIT_USED | True | run_phase438_low_turnover_depth_regime_carry_no_paper_live | phase437_next_action | hard |
| P438_LOW_TURNOVER_ONE_TRADE_PER_SYMBOL_DATE | True | 384 | one_per_symbol_date | hard |
| P438_FULL_DEPTH_PRIMARY_PRESENT | True | P438_depth_regime_snapback_E120_H2400_D5 | full_depth_pressure | hard |
| P438_L1_ONLY_CONTROL | False | 0 | >=5 pct pts | hard |
| P438_SIDE_FLIP_CONTROL_NOT_DOMINANT | True | -159.732 | primary>=side_flip | hard |
| P438_TIME_SHUFFLE_CONTROL_NOT_DOMINANT | True | -156.064 | primary>=time_shuffle | hard |
| P438_COST200_FIXED_CAPITAL | True | cost=2.0;capital=1000000.0;notional=100000.0 | cost200_fixed_capital | hard |
| P438_EVENT_FLOOR | True | 384 | >=30 | hard |
| P438_DATE_BREADTH | True | 12 | >=5 | hard |
| P438_SYMBOL_BREADTH | True | 32 | >=5 | hard |
| P438_POSITIVE_DATE_FRACTION | False | 0 | >=0.6 | hard |
| P438_ANNUALIZED_FLOOR | False | -142.94 | >=12.0 | hard |
| P438_REAL_ANCHOR_CROSS_CHECK | True | -25.2551 | same_sign | hard |
| P438_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: no strategy promotion, paper/live acceptance or deployable profitability claim is generated by Phase438.
