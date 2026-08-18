# Phase432 Geometry-Consistent Full-Depth Feature Sweep

Phase432 executes the Phase431 timing-geometry repair: same Phase427 feature thresholds, panel-specific feasible max-hold windows, exact forward ticks and Zerodha cost200.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase432_geometry_consistent_full_depth_sweep_complete | 1 | Phase432 execution completed |
| phase432_synthetic_grid_rows_evaluated | 486 | Synthetic scenario rows |
| phase432_real_anchor_grid_rows_evaluated | 486 | Real-anchor scenario rows |
| phase432_best_scenario_id | P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S8p0_I0p25_D0p1 | Best synthetic scenario by annualized return |
| phase432_best_family_id | depth_pressure_continuation | Best synthetic family |
| phase432_best_completed_round_trips | 10 | Best round trips |
| phase432_best_trade_dates | 2 | Best trade dates |
| phase432_best_symbols | 1 | Best symbols |
| phase432_best_positive_date_fraction | 0 | Best positive date fraction |
| phase432_best_net_pnl_inr | -1604.19 | Best net P&L |
| phase432_best_annualized_return_pct | -20.2127 | Best annualized return |
| phase432_active_synthetic_scenario_rows | 27 | Synthetic scenarios with at least one trade |
| phase432_cost200_acceptance_survivor_rows | 0 | Accepted synthetic scenarios before control gates |
| phase432_control_rows | 25 | Control rows |
| phase432_strategy_promotion_allowed | 0 | No promotion |
| phase432_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase432_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase432_hard_gate_pass_rows | 11 | Passed hard gates |
| phase432_hard_gate_rows | 17 | Hard gates |
| phase432_next_best_action | interpret_phase432_geometry_consistent_full_depth_feature_sweep_no_paper_live | Recommended next action |

## Top Synthetic Scenarios

| panel | scenario_id | family_id | completed_round_trips | trade_dates | symbols | positive_date_fraction | net_pnl_inr | gross_pnl_inr | cost200_inr | annualized_return_pct | acceptance_survivor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| synthetic | P432_synthetic_book_slope_migration_L360_F3_M2500_S12p0_I0p55_D0p4 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L360_F3_M2500_S12p0_I0p55_D0p25 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L360_F3_M2500_S12p0_I0p55_D0p1 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L180_F3_M2500_S8p0_I0p25_D0p4 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L180_F3_M2500_S8p0_I0p4_D0p1 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L180_F3_M2500_S8p0_I0p4_D0p25 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L180_F3_M2500_S8p0_I0p4_D0p4 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L180_F3_M2500_S8p0_I0p55_D0p1 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L180_F3_M2500_S8p0_I0p55_D0p25 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L180_F3_M2500_S8p0_I0p55_D0p4 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L180_F3_M2500_S12p0_I0p25_D0p1 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L180_F3_M2500_S4p0_I0p4_D0p1 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L180_F3_M2500_S4p0_I0p4_D0p25 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L180_F3_M2500_S4p0_I0p4_D0p4 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L180_F3_M2500_S4p0_I0p55_D0p1 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L180_F3_M2500_S4p0_I0p55_D0p25 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L180_F3_M2500_S4p0_I0p55_D0p4 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L180_F3_M2500_S8p0_I0p25_D0p1 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L180_F3_M2500_S8p0_I0p25_D0p25 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L60_F3_M2500_S12p0_I0p4_D0p25 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L60_F3_M2500_S12p0_I0p4_D0p4 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L60_F3_M2500_S12p0_I0p55_D0p1 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L60_F3_M2500_S12p0_I0p55_D0p25 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L60_F3_M2500_S12p0_I0p55_D0p4 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L180_F3_M2500_S4p0_I0p25_D0p1 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L180_F3_M2500_S4p0_I0p25_D0p25 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L180_F3_M2500_S4p0_I0p25_D0p4 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L60_F3_M2500_S8p0_I0p4_D0p4 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L60_F3_M2500_S8p0_I0p55_D0p1 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P432_synthetic_book_slope_migration_L60_F3_M2500_S8p0_I0p55_D0p25 | book_slope_migration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Top Synthetic Controls

| scenario_id | family_id | l1_only_annualized_return_pct | l1_only_trips | side_flip_annualized_return_pct | side_flip_trips |
| --- | --- | --- | --- | --- | --- |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S8p0_I0p25_D0p1 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S8p0_I0p25_D0p25 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S8p0_I0p25_D0p4 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S12p0_I0p25_D0p1 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S12p0_I0p25_D0p25 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S12p0_I0p25_D0p4 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L180_F3_M2500_S4p0_I0p25_D0p1 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L180_F3_M2500_S4p0_I0p25_D0p25 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L180_F3_M2500_S4p0_I0p25_D0p4 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L360_F3_M2500_S12p0_I0p25_D0p1 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L360_F3_M2500_S12p0_I0p25_D0p25 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L360_F3_M2500_S12p0_I0p25_D0p4 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L180_F3_M2500_S8p0_I0p25_D0p1 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L180_F3_M2500_S8p0_I0p25_D0p25 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L180_F3_M2500_S8p0_I0p25_D0p4 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L180_F3_M2500_S12p0_I0p25_D0p1 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L180_F3_M2500_S12p0_I0p25_D0p25 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L180_F3_M2500_S12p0_I0p25_D0p4 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L360_F3_M2500_S4p0_I0p25_D0p1 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L360_F3_M2500_S4p0_I0p25_D0p25 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L360_F3_M2500_S4p0_I0p25_D0p4 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L360_F3_M2500_S8p0_I0p25_D0p1 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L360_F3_M2500_S8p0_I0p25_D0p25 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L360_F3_M2500_S8p0_I0p25_D0p4 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S4p0_I0p25_D0p4 | depth_pressure_continuation | -20.2127 | 10 | -30.2194 | 10 |

## Cross-Panel Comparison

| synthetic_scenario_id | real_anchor_scenario_id | family_id | synthetic_round_trips | synthetic_annualized_return_pct | synthetic_positive_date_fraction | real_anchor_round_trips | real_anchor_annualized_return_pct | real_anchor_positive_date_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S8p0_I0p25_D0p1 | P432_real_anchor_depth_pressure_continuation_L60_F3_M2500_S8p0_I0p25_D0p1 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S8p0_I0p25_D0p25 | P432_real_anchor_depth_pressure_continuation_L60_F3_M2500_S8p0_I0p25_D0p25 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S8p0_I0p25_D0p4 | P432_real_anchor_depth_pressure_continuation_L60_F3_M2500_S8p0_I0p25_D0p4 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S12p0_I0p25_D0p1 | P432_real_anchor_depth_pressure_continuation_L60_F3_M2500_S12p0_I0p25_D0p1 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S12p0_I0p25_D0p25 | P432_real_anchor_depth_pressure_continuation_L60_F3_M2500_S12p0_I0p25_D0p25 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S12p0_I0p25_D0p4 | P432_real_anchor_depth_pressure_continuation_L60_F3_M2500_S12p0_I0p25_D0p4 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L180_F3_M2500_S4p0_I0p25_D0p1 | P432_real_anchor_depth_pressure_continuation_L180_F3_M2500_S4p0_I0p25_D0p1 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L180_F3_M2500_S4p0_I0p25_D0p25 | P432_real_anchor_depth_pressure_continuation_L180_F3_M2500_S4p0_I0p25_D0p25 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L180_F3_M2500_S4p0_I0p25_D0p4 | P432_real_anchor_depth_pressure_continuation_L180_F3_M2500_S4p0_I0p25_D0p4 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L360_F3_M2500_S12p0_I0p25_D0p1 | P432_real_anchor_depth_pressure_continuation_L360_F3_M2500_S12p0_I0p25_D0p1 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L360_F3_M2500_S12p0_I0p25_D0p25 | P432_real_anchor_depth_pressure_continuation_L360_F3_M2500_S12p0_I0p25_D0p25 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L360_F3_M2500_S12p0_I0p25_D0p4 | P432_real_anchor_depth_pressure_continuation_L360_F3_M2500_S12p0_I0p25_D0p4 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L180_F3_M2500_S8p0_I0p25_D0p1 | P432_real_anchor_depth_pressure_continuation_L180_F3_M2500_S8p0_I0p25_D0p1 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L180_F3_M2500_S8p0_I0p25_D0p25 | P432_real_anchor_depth_pressure_continuation_L180_F3_M2500_S8p0_I0p25_D0p25 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L180_F3_M2500_S8p0_I0p25_D0p4 | P432_real_anchor_depth_pressure_continuation_L180_F3_M2500_S8p0_I0p25_D0p4 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L180_F3_M2500_S12p0_I0p25_D0p1 | P432_real_anchor_depth_pressure_continuation_L180_F3_M2500_S12p0_I0p25_D0p1 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L180_F3_M2500_S12p0_I0p25_D0p25 | P432_real_anchor_depth_pressure_continuation_L180_F3_M2500_S12p0_I0p25_D0p25 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L180_F3_M2500_S12p0_I0p25_D0p4 | P432_real_anchor_depth_pressure_continuation_L180_F3_M2500_S12p0_I0p25_D0p4 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L360_F3_M2500_S4p0_I0p25_D0p1 | P432_real_anchor_depth_pressure_continuation_L360_F3_M2500_S4p0_I0p25_D0p1 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L360_F3_M2500_S4p0_I0p25_D0p25 | P432_real_anchor_depth_pressure_continuation_L360_F3_M2500_S4p0_I0p25_D0p25 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L360_F3_M2500_S4p0_I0p25_D0p4 | P432_real_anchor_depth_pressure_continuation_L360_F3_M2500_S4p0_I0p25_D0p4 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L360_F3_M2500_S8p0_I0p25_D0p1 | P432_real_anchor_depth_pressure_continuation_L360_F3_M2500_S8p0_I0p25_D0p1 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L360_F3_M2500_S8p0_I0p25_D0p25 | P432_real_anchor_depth_pressure_continuation_L360_F3_M2500_S8p0_I0p25_D0p25 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L360_F3_M2500_S8p0_I0p25_D0p4 | P432_real_anchor_depth_pressure_continuation_L360_F3_M2500_S8p0_I0p25_D0p4 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S4p0_I0p25_D0p4 | P432_real_anchor_depth_pressure_continuation_L60_F3_M2500_S4p0_I0p25_D0p4 | depth_pressure_continuation | 10 | -20.2127 | 0 | 0 | 0 | 0 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P432_EXECUTION_COMPLETE | True | 1 | 1 | hard |
| P432_PHASE431_PRECOMMIT_USED | True | run_phase432_geometry_consistent_full_depth_feature_sweep_no_paper_live | run_phase432 | hard |
| P432_SYNTHETIC_GRID_ROWS_EVALUATED | True | 486 | 486 | hard |
| P432_REAL_ANCHOR_GRID_ROWS_EVALUATED | True | 486 | 486 | hard |
| P432_PANEL_SPECIFIC_GEOMETRY | True | synthetic_2500_real_500 | present | hard |
| P432_EXACT_FORWARD_TICK_INDEXING | True | phase428_exact_index_engine | present | hard |
| P432_FULL_DEPTH_PRIMARY_FEATURES | True | phase427_l2_l5_families | present | hard |
| P432_L1_ONLY_CONTROL | False | 0 | >=5.0 | hard |
| P432_SIDE_FLIP_CONTROL | True | -30.2194 | best>=side_flip | hard |
| P432_COST200_FIXED_CAPITAL | True | cost=2.0;capital=1000000.0;notional=100000.0 | cost200_fixed_capital | hard |
| P432_EVENT_FLOOR | False | 10 | >=30 | hard |
| P432_DATE_BREADTH | False | 2 | >=5 | hard |
| P432_SYMBOL_BREADTH | False | 1 | >=5 | hard |
| P432_POSITIVE_DATE_FRACTION | False | 0 | >=0.6 | hard |
| P432_ANNUALIZED_FLOOR | False | -20.2127 | >=12.0 | hard |
| P432_REAL_ANCHOR_CROSS_CHECK | True | 0 | same_sign | hard |
| P432_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: no promotion, paper/live acceptance or deployable profitability claim is generated by Phase432.
