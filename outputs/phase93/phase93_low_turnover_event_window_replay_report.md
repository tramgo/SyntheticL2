# Phase93 Low-Turnover Event-Window Replay

Generated UTC: 2026-07-19T21:19:55.320034+00:00

Phase93 mechanically replays only the Phase92-precommitted low-turnover event-window candidates.
No thresholds are widened. If this phase fails, the predeclared next action is to stop strategy mining and return to generator realism/calibration audit.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase93_precommitted_candidate_rows | 12 | Phase92 candidate specs replayed without threshold changes |
| phase93_train_pass_candidates | 0 | Candidates passing train gates |
| phase93_test_pass_candidates | 0 | Candidates passing test gates |
| phase93_full_pass_candidates | 0 | Candidates passing both train and test gates |
| phase93_best_train_net_pnl_inr | 999.654 | Best train after-cost net P&L |
| phase93_best_test_net_pnl_inr | 38990.4 | Best test after-cost net P&L |
| phase93_low_turnover_event_replay_pass | 0 | 1 means at least one low-turnover event-window candidate survives |
| phase93_recommend_next_action | stop_strategy_mining_return_to_generator_realism_calibration_audit | Recommended next milestone |

## Candidate Results

| candidate_id | family_id | direction_rule | requires_shock_bar | event_window_score_quantile | event_window_score_threshold | abs_bar_return_bps_quantile | abs_bar_return_bps_threshold | book_dislocation_score_quantile | book_dislocation_score_threshold | max_taker_round_trip_cost_floor_bps | train_months | test_months | train_trades | train_symbols | train_days | train_net_pnl_inr | train_gross_pnl_inr | train_cost_pnl_drag_inr | train_precision_cost_clear | train_positive_months | train_max_day_trade_fraction | train_max_month_contribution_abs | train_max_symbol_contribution_abs | train_abs_gross_to_cost_drag_ratio | test_trades | test_symbols | test_days | test_net_pnl_inr | test_gross_pnl_inr | test_cost_pnl_drag_inr | test_precision_cost_clear | test_positive_months | test_max_day_trade_fraction | test_max_month_contribution_abs | test_max_symbol_contribution_abs | test_abs_gross_to_cost_drag_ratio | train_pass | test_pass | phase93_candidate_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P92_SHOCK_CONTINUATION_E0_95_M0_95 | P92_SHOCK_CONTINUATION | side = sign(bar_return) | True | 0.95 | 72.3652 | 0.95 | 166.608 | 0 | 0 | 10.9053 | 4 | 5 | 41 | 1 | 7 | 999.654 | 5448.81 | 4449.15 | 0.487805 | 1 | 0.292683 | 20.8882 | 1 | 1.22468 | 35 | 1 | 7 | 38990.4 | 42795.2 | 3804.73 | 0.714286 | 4 | 0.228571 | 0.535541 | 1 | 11.2479 | False | False | False |
| P92_SHOCK_CONTINUATION_E0_95_M0_975 | P92_SHOCK_CONTINUATION | side = sign(bar_return) | True | 0.95 | 72.3652 | 0.975 | 215.813 | 0 | 0 | 10.9053 | 4 | 4 | 17 | 1 | 5 | -3.96318 | 1842.03 | 1845.99 | 0.529412 | 2 | 0.529412 | 2929.65 | 1 | 0.997853 | 21 | 1 | 6 | 16648.6 | 18933.3 | 2284.69 | 0.619048 | 3 | 0.333333 | 0.6974 | 1 | 8.28703 | False | False | False |
| P92_SHOCK_CONTINUATION_E0_975_M0_975 | P92_SHOCK_CONTINUATION | side = sign(bar_return) | True | 0.975 | 89.9766 | 0.975 | 215.813 | 0 | 0 | 10.9053 | 4 | 4 | 17 | 1 | 5 | -3.96318 | 1842.03 | 1845.99 | 0.529412 | 2 | 0.529412 | 2929.65 | 1 | 0.997853 | 21 | 1 | 6 | 16648.6 | 18933.3 | 2284.69 | 0.619048 | 3 | 0.333333 | 0.6974 | 1 | 8.28703 | False | False | False |
| P92_SHOCK_CONTINUATION_E0_975_M0_95 | P92_SHOCK_CONTINUATION | side = sign(bar_return) | True | 0.975 | 89.9766 | 0.95 | 166.608 | 0 | 0 | 10.9053 | 4 | 5 | 32 | 1 | 7 | -7544.48 | -4070.52 | 3473.96 | 0.4375 | 1 | 0.34375 | 1.53897 | 1 | 1.17173 | 24 | 1 | 7 | 14688.7 | 17299.9 | 2611.16 | 0.583333 | 4 | 0.291667 | 0.790453 | 1 | 6.62537 | False | False | False |
| P92_BOOK_DISLOCATION_REVERSAL_E0_95_M0_95 | P92_BOOK_DISLOCATION_REVERSAL | side = -sign(bar_return) | False | 0.95 | 72.3652 | 0.95 | 166.608 | 0.95 | 2.63561 | 10.9053 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  | False | False | False |
| P92_BOOK_DISLOCATION_REVERSAL_E0_95_M0_975 | P92_BOOK_DISLOCATION_REVERSAL | side = -sign(bar_return) | False | 0.95 | 72.3652 | 0.975 | 215.813 | 0.95 | 2.63561 | 10.9053 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  | False | False | False |
| P92_BOOK_DISLOCATION_REVERSAL_E0_975_M0_95 | P92_BOOK_DISLOCATION_REVERSAL | side = -sign(bar_return) | False | 0.975 | 89.9766 | 0.95 | 166.608 | 0.95 | 2.63561 | 10.9053 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  | False | False | False |
| P92_BOOK_DISLOCATION_REVERSAL_E0_975_M0_975 | P92_BOOK_DISLOCATION_REVERSAL | side = -sign(bar_return) | False | 0.975 | 89.9766 | 0.975 | 215.813 | 0.95 | 2.63561 | 10.9053 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  | False | False | False |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | side = -sign(bar_return) | True | 0.975 | 89.9766 | 0.95 | 166.608 | 0 | 0 | 10.9053 | 4 | 5 | 32 | 1 | 7 | 596.568 | 4070.52 | 3473.96 | 0.53125 | 3 | 0.34375 | 20.5552 | 1 | 1.17173 | 24 | 1 | 7 | -19911 | -17299.9 | 2611.16 | 0.416667 | 1 | 0.291667 | 0.615868 | 1 | 6.62537 | False | False | False |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | side = -sign(bar_return) | True | 0.95 | 72.3652 | 0.975 | 215.813 | 0 | 0 | 10.9053 | 4 | 4 | 17 | 1 | 5 | -3688.01 | -1842.03 | 1845.99 | 0.470588 | 2 | 0.529412 | 3.32498 | 1 | 0.997853 | 21 | 1 | 6 | -21218 | -18933.3 | 2284.69 | 0.380952 | 1 | 0.333333 | 0.577932 | 1 | 8.28703 | False | False | False |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | side = -sign(bar_return) | True | 0.975 | 89.9766 | 0.975 | 215.813 | 0 | 0 | 10.9053 | 4 | 4 | 17 | 1 | 5 | -3688.01 | -1842.03 | 1845.99 | 0.470588 | 2 | 0.529412 | 3.32498 | 1 | 0.997853 | 21 | 1 | 6 | -21218 | -18933.3 | 2284.69 | 0.380952 | 1 | 0.333333 | 0.577932 | 1 | 8.28703 | False | False | False |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | side = -sign(bar_return) | True | 0.95 | 72.3652 | 0.95 | 166.608 | 0 | 0 | 10.9053 | 4 | 5 | 41 | 1 | 7 | -9897.96 | -5448.81 | 4449.15 | 0.487805 | 3 | 0.292683 | 2.21929 | 1 | 1.22468 | 35 | 1 | 7 | -46599.9 | -42795.2 | 3804.73 | 0.285714 | 1 | 0.228571 | 0.471384 | 1 | 11.2479 | False | False | False |

## Monthly Summary

| candidate_id | family_id | split | trade_month | trades | symbols | net_pnl_inr | gross_pnl_inr | cost_pnl_drag_inr | precision_cost_clear |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | test | 2026-07 | 4 | 1 | -8876.03 | -8441.72 | 434.303 | 0 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | test | 2026-08 | 7 | 1 | -5481.53 | -4720.13 | 761.4 | 0.428571 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | test | 2026-09 | 9 | 1 | -12732.3 | -11753.5 | 978.84 | 0.111111 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | test | 2026-11 | 10 | 1 | 2456.46 | 3543.9 | 1087.44 | 0.6 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | test | 2026-12 | 5 | 1 | -21966.4 | -21423.7 | 542.744 | 0 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | train | 2026-02 | 10 | 1 | 2456.46 | 3543.9 | 1087.44 | 0.6 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | train | 2026-03 | 5 | 1 | -21966.4 | -21423.7 | 542.744 | 0 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | train | 2026-04 | 14 | 1 | 7127.22 | 8644.16 | 1516.93 | 0.5 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | train | 2026-06 | 12 | 1 | 2484.8 | 3786.83 | 1302.04 | 0.583333 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | test | 2026-08 | 7 | 1 | -5481.53 | -4720.13 | 761.4 | 0.428571 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | test | 2026-09 | 7 | 1 | -8106.08 | -7344.27 | 761.807 | 0.142857 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | test | 2026-11 | 4 | 1 | 4632.18 | 5067.75 | 435.571 | 1 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | test | 2026-12 | 3 | 1 | -12262.6 | -11936.7 | 325.915 | 0 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | train | 2026-02 | 4 | 1 | 4632.18 | 5067.75 | 435.571 | 1 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | train | 2026-03 | 3 | 1 | -12262.6 | -11936.7 | 325.915 | 0 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | train | 2026-04 | 9 | 1 | 5147.78 | 6123.49 | 975.712 | 0.444444 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | train | 2026-06 | 1 | 1 | -1205.4 | -1096.61 | 108.791 | 0 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | test | 2026-07 | 1 | 1 | -2241.7 | -2133.01 | 108.694 | 0 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | test | 2026-08 | 7 | 1 | -5481.53 | -4720.13 | 761.4 | 0.428571 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | test | 2026-09 | 7 | 1 | -8106.08 | -7344.27 | 761.807 | 0.142857 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | test | 2026-11 | 6 | 1 | 8180.85 | 8834.19 | 653.341 | 1 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | test | 2026-12 | 3 | 1 | -12262.6 | -11936.7 | 325.915 | 0 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | train | 2026-02 | 6 | 1 | 8180.85 | 8834.19 | 653.341 | 1 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | train | 2026-03 | 3 | 1 | -12262.6 | -11936.7 | 325.915 | 0 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | train | 2026-04 | 13 | 1 | 4587.45 | 5996.33 | 1408.87 | 0.461538 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | train | 2026-06 | 10 | 1 | 90.8364 | 1176.66 | 1085.83 | 0.5 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | test | 2026-08 | 7 | 1 | -5481.53 | -4720.13 | 761.4 | 0.428571 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | test | 2026-09 | 7 | 1 | -8106.08 | -7344.27 | 761.807 | 0.142857 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | test | 2026-11 | 4 | 1 | 4632.18 | 5067.75 | 435.571 | 1 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | test | 2026-12 | 3 | 1 | -12262.6 | -11936.7 | 325.915 | 0 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | train | 2026-02 | 4 | 1 | 4632.18 | 5067.75 | 435.571 | 1 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | train | 2026-03 | 3 | 1 | -12262.6 | -11936.7 | 325.915 | 0 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | train | 2026-04 | 9 | 1 | 5147.78 | 6123.49 | 975.712 | 0.444444 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | train | 2026-06 | 1 | 1 | -1205.4 | -1096.61 | 108.791 | 0 |
| P92_SHOCK_CONTINUATION_E0_95_M0_95 | P92_SHOCK_CONTINUATION | test | 2026-07 | 4 | 1 | 8007.42 | 8441.72 | 434.303 | 1 |
| P92_SHOCK_CONTINUATION_E0_95_M0_95 | P92_SHOCK_CONTINUATION | test | 2026-08 | 7 | 1 | 3958.73 | 4720.13 | 761.4 | 0.571429 |
| P92_SHOCK_CONTINUATION_E0_95_M0_95 | P92_SHOCK_CONTINUATION | test | 2026-09 | 9 | 1 | 10774.7 | 11753.5 | 978.84 | 0.888889 |
| P92_SHOCK_CONTINUATION_E0_95_M0_95 | P92_SHOCK_CONTINUATION | test | 2026-11 | 10 | 1 | -4631.35 | -3543.9 | 1087.44 | 0.4 |
| P92_SHOCK_CONTINUATION_E0_95_M0_95 | P92_SHOCK_CONTINUATION | test | 2026-12 | 5 | 1 | 20881 | 21423.7 | 542.744 | 1 |
| P92_SHOCK_CONTINUATION_E0_95_M0_95 | P92_SHOCK_CONTINUATION | train | 2026-02 | 10 | 1 | -4631.35 | -3543.9 | 1087.44 | 0.4 |
| P92_SHOCK_CONTINUATION_E0_95_M0_95 | P92_SHOCK_CONTINUATION | train | 2026-03 | 5 | 1 | 20881 | 21423.7 | 542.744 | 1 |
| P92_SHOCK_CONTINUATION_E0_95_M0_95 | P92_SHOCK_CONTINUATION | train | 2026-04 | 14 | 1 | -10161.1 | -8644.16 | 1516.93 | 0.428571 |
| P92_SHOCK_CONTINUATION_E0_95_M0_95 | P92_SHOCK_CONTINUATION | train | 2026-06 | 12 | 1 | -5088.87 | -3786.83 | 1302.04 | 0.416667 |
| P92_SHOCK_CONTINUATION_E0_95_M0_975 | P92_SHOCK_CONTINUATION | test | 2026-08 | 7 | 1 | 3958.73 | 4720.13 | 761.4 | 0.571429 |
| P92_SHOCK_CONTINUATION_E0_95_M0_975 | P92_SHOCK_CONTINUATION | test | 2026-09 | 7 | 1 | 6582.47 | 7344.27 | 761.807 | 0.857143 |
| P92_SHOCK_CONTINUATION_E0_95_M0_975 | P92_SHOCK_CONTINUATION | test | 2026-11 | 4 | 1 | -5503.32 | -5067.75 | 435.571 | 0 |
| P92_SHOCK_CONTINUATION_E0_95_M0_975 | P92_SHOCK_CONTINUATION | test | 2026-12 | 3 | 1 | 11610.7 | 11936.7 | 325.915 | 1 |
| P92_SHOCK_CONTINUATION_E0_95_M0_975 | P92_SHOCK_CONTINUATION | train | 2026-02 | 4 | 1 | -5503.32 | -5067.75 | 435.571 | 0 |
| P92_SHOCK_CONTINUATION_E0_95_M0_975 | P92_SHOCK_CONTINUATION | train | 2026-03 | 3 | 1 | 11610.7 | 11936.7 | 325.915 | 1 |
| P92_SHOCK_CONTINUATION_E0_95_M0_975 | P92_SHOCK_CONTINUATION | train | 2026-04 | 9 | 1 | -7099.2 | -6123.49 | 975.712 | 0.555556 |
| P92_SHOCK_CONTINUATION_E0_95_M0_975 | P92_SHOCK_CONTINUATION | train | 2026-06 | 1 | 1 | 987.815 | 1096.61 | 108.791 | 1 |
| P92_SHOCK_CONTINUATION_E0_975_M0_95 | P92_SHOCK_CONTINUATION | test | 2026-07 | 1 | 1 | 2024.32 | 2133.01 | 108.694 | 1 |
| P92_SHOCK_CONTINUATION_E0_975_M0_95 | P92_SHOCK_CONTINUATION | test | 2026-08 | 7 | 1 | 3958.73 | 4720.13 | 761.4 | 0.571429 |
| P92_SHOCK_CONTINUATION_E0_975_M0_95 | P92_SHOCK_CONTINUATION | test | 2026-09 | 7 | 1 | 6582.47 | 7344.27 | 761.807 | 0.857143 |
| P92_SHOCK_CONTINUATION_E0_975_M0_95 | P92_SHOCK_CONTINUATION | test | 2026-11 | 6 | 1 | -9487.53 | -8834.19 | 653.341 | 0 |
| P92_SHOCK_CONTINUATION_E0_975_M0_95 | P92_SHOCK_CONTINUATION | test | 2026-12 | 3 | 1 | 11610.7 | 11936.7 | 325.915 | 1 |
| P92_SHOCK_CONTINUATION_E0_975_M0_95 | P92_SHOCK_CONTINUATION | train | 2026-02 | 6 | 1 | -9487.53 | -8834.19 | 653.341 | 0 |
| P92_SHOCK_CONTINUATION_E0_975_M0_95 | P92_SHOCK_CONTINUATION | train | 2026-03 | 3 | 1 | 11610.7 | 11936.7 | 325.915 | 1 |
| P92_SHOCK_CONTINUATION_E0_975_M0_95 | P92_SHOCK_CONTINUATION | train | 2026-04 | 13 | 1 | -7405.2 | -5996.33 | 1408.87 | 0.461538 |
| P92_SHOCK_CONTINUATION_E0_975_M0_95 | P92_SHOCK_CONTINUATION | train | 2026-06 | 10 | 1 | -2262.49 | -1176.66 | 1085.83 | 0.5 |

## Symbol Summary

| candidate_id | family_id | split | symbol | trades | months | net_pnl_inr | gross_pnl_inr | cost_pnl_drag_inr | precision_cost_clear |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | test | GOLDBEES | 35 | 5 | -46599.9 | -42795.2 | 3804.73 | 0.285714 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | train | GOLDBEES | 41 | 4 | -9897.96 | -5448.81 | 4449.15 | 0.487805 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | test | GOLDBEES | 21 | 4 | -21218 | -18933.3 | 2284.69 | 0.380952 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | train | GOLDBEES | 17 | 4 | -3688.01 | -1842.03 | 1845.99 | 0.470588 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | test | GOLDBEES | 24 | 5 | -19911 | -17299.9 | 2611.16 | 0.416667 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | train | GOLDBEES | 32 | 4 | 596.568 | 4070.52 | 3473.96 | 0.53125 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | test | GOLDBEES | 21 | 4 | -21218 | -18933.3 | 2284.69 | 0.380952 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | train | GOLDBEES | 17 | 4 | -3688.01 | -1842.03 | 1845.99 | 0.470588 |
| P92_SHOCK_CONTINUATION_E0_95_M0_95 | P92_SHOCK_CONTINUATION | test | GOLDBEES | 35 | 5 | 38990.4 | 42795.2 | 3804.73 | 0.714286 |
| P92_SHOCK_CONTINUATION_E0_95_M0_95 | P92_SHOCK_CONTINUATION | train | GOLDBEES | 41 | 4 | 999.654 | 5448.81 | 4449.15 | 0.487805 |
| P92_SHOCK_CONTINUATION_E0_95_M0_975 | P92_SHOCK_CONTINUATION | test | GOLDBEES | 21 | 4 | 16648.6 | 18933.3 | 2284.69 | 0.619048 |
| P92_SHOCK_CONTINUATION_E0_95_M0_975 | P92_SHOCK_CONTINUATION | train | GOLDBEES | 17 | 4 | -3.96318 | 1842.03 | 1845.99 | 0.529412 |
| P92_SHOCK_CONTINUATION_E0_975_M0_95 | P92_SHOCK_CONTINUATION | test | GOLDBEES | 24 | 5 | 14688.7 | 17299.9 | 2611.16 | 0.583333 |
| P92_SHOCK_CONTINUATION_E0_975_M0_95 | P92_SHOCK_CONTINUATION | train | GOLDBEES | 32 | 4 | -7544.48 | -4070.52 | 3473.96 | 0.4375 |
| P92_SHOCK_CONTINUATION_E0_975_M0_975 | P92_SHOCK_CONTINUATION | test | GOLDBEES | 21 | 4 | 16648.6 | 18933.3 | 2284.69 | 0.619048 |
| P92_SHOCK_CONTINUATION_E0_975_M0_975 | P92_SHOCK_CONTINUATION | train | GOLDBEES | 17 | 4 | -3.96318 | 1842.03 | 1845.99 | 0.529412 |
