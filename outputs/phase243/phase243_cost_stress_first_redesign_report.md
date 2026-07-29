# Phase243 Cost-stress-first Redesign Search

Generated UTC: 2026-07-29T08:20:47.216364+00:00

Phase243 runs the redesign queue opened by Phase242 without using the 2026-07-17 holdout for tuning and without downloading more real dates.
It searches stricter, lower-turnover variants and requires 1.5x/2.0x cost survival before random-side control evaluation.
Survivors are research candidates for a future holdout only; no paper/live acceptance or deployable profitability claim is opened.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase243_cost_stress_first_redesign_complete | 1 | Phase243 redesign search completed |
| phase243_training_event_bar_rows | 28793 | Training/discovery event bars used |
| phase243_forbidden_holdout_dates | 2026-07-17 | Dates excluded from tuning |
| phase243_expanded_variant_rows | 3920 | Redesigned variants evaluated |
| phase243_net_positive_variant_rows | 792 | Net-positive variants after base costs |
| phase243_cost150_positive_variant_rows | 609 | Positive under 1.5x costs |
| phase243_cost200_positive_variant_rows | 487 | Positive under 2.0x costs |
| phase243_controlled_candidate_rows | 161 | Cost-stress survivors with full controls evaluated |
| phase243_survivor_candidate_rows | 113 | Candidates passing side flip, random side and cost stress controls |
| phase243_best_candidate_id | P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 | Best Phase243 survivor/candidate |
| phase243_best_training_net_pnl_inr | 8576.39 | Best training/discovery net P&L |
| phase243_best_cost200_net_pnl_inr | 5033.27 | Best 2x-cost net P&L |
| phase243_best_random_beat_fraction | 0.997 | Best random-side beat fraction |
| phase243_best_trade_rows | 29 | Best selected trades |
| phase243_best_dates | 5 | Best dates represented |
| phase243_best_symbols | 13 | Best symbols represented |
| phase243_hard_gate_pass_rows | 6 | Hard gates passed |
| phase243_hard_gate_rows | 6 | Hard gates evaluated |
| phase243_future_holdout_precommit_allowed | 1 | A future holdout precommit may be opened, but no current holdout acceptance |
| phase243_download_more_dates_now_allowed | 0 | No additional raw-date download in Phase243 |
| phase243_holdout_parameter_tuning_allowed | 0 | No 2026-07-17 tuning |
| phase243_strategy_promotion_allowed | 0 | No strategy promotion from Phase243 |
| phase243_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase243 |
| phase243_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase243 |
| phase243_next_best_action | precommit_future_holdout_for_phase243_candidate_after_storage_decision_no_2026_07_17_tuning_no_paper_live | Recommended next milestone |

## Best Candidate

| candidate_id | family_id | signal_source | direction | horizon_event_bars | event_quantile | signal_quantile | event_window_score_threshold | signal_abs_threshold | training_trades | training_net_pnl_inr | training_gross_pnl_inr | training_cost_pnl_drag_inr | cost150_net_pnl_inr_x | cost200_net_pnl_inr_x | training_dates | training_symbols | training_positive_dates | training_min_date_net_pnl_inr | training_max_date_contribution_abs | training_max_symbol_contribution_abs | training_precision_cost_clear | cost_stress_pass | side_flip_net_pnl_inr | side_flip_pass | random_p95_net_pnl_inr | random_beat_fraction | random_side_pass | cost150_net_pnl_inr_y | cost150_pass | cost200_net_pnl_inr_y | cost200_pass | control_pass_rows | phase243_candidate_survived |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 | bar_return_reversal | bar_return | reversal | 8 | 0.99 | 0.9 | 15.5881 | 0.00779013 | 29 | 8576.39 | 12119.5 | 3543.12 | 6804.83 | 5033.27 | 5 | 13 | 4 | -970.633 | 0.599293 | 0.497184 | 0.586207 | True | -15662.6 | True | 4577.69 | 0.997 | True | 6804.83 | True | 5033.27 | True | 4 | True |

## Survivor Candidates

| candidate_id | family_id | signal_source | direction | horizon_event_bars | event_quantile | signal_quantile | event_window_score_threshold | signal_abs_threshold | training_trades | training_net_pnl_inr | training_gross_pnl_inr | training_cost_pnl_drag_inr | cost150_net_pnl_inr_x | cost200_net_pnl_inr_x | training_dates | training_symbols | training_positive_dates | training_min_date_net_pnl_inr | training_max_date_contribution_abs | training_max_symbol_contribution_abs | training_precision_cost_clear | cost_stress_pass | side_flip_net_pnl_inr | side_flip_pass | random_p95_net_pnl_inr | random_beat_fraction | random_side_pass | cost150_net_pnl_inr_y | cost150_pass | cost200_net_pnl_inr_y | cost200_pass | control_pass_rows | phase243_candidate_survived |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 | bar_return_reversal | bar_return | reversal | 8 | 0.99 | 0.9 | 15.5881 | 0.00779013 | 29 | 8576.39 | 12119.5 | 3543.12 | 6804.83 | 5033.27 | 5 | 13 | 4 | -970.633 | 0.599293 | 0.497184 | 0.586207 | True | -15662.6 | True | 4577.69 | 0.997 | True | 6804.83 | True | 5033.27 | True | 4 | True |
| P243_TOP5_IMBALANCE_CONTINUATION_H20_EQ0_95_SQ0_975 | avg_top5_market_by_price_imbalance_continuation | avg_top5_market_by_price_imbalance | continuation | 20 | 0.95 | 0.975 | 8.3341 | 0.565967 | 32 | 4790.8 | 8365.57 | 3574.78 | 3003.41 | 1216.02 | 7 | 15 | 5 | -2737.16 | 0.912604 | 0.29607 | 0.59375 | True | -11940.4 | True | 2218.21 | 0.995 | True | 3003.41 | True | 1216.02 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H8_EQ0_985_SQ0_925 | bar_return_reversal | bar_return | reversal | 8 | 0.985 | 0.925 | 13.2983 | 0.0075835 | 32 | 8445.4 | 12361.2 | 3915.82 | 6487.49 | 4529.58 | 5 | 15 | 4 | -970.633 | 0.533692 | 0.504895 | 0.59375 | True | -16277 | True | 4617.86 | 0.994 | True | 6487.49 | True | 4529.58 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H6_EQ0_9_SQ0_985 | bar_return_reversal | bar_return | reversal | 6 | 0.9 | 0.985 | 5.96138 | 0.00685438 | 42 | 8298.76 | 13417.1 | 5118.3 | 5739.6 | 3180.45 | 5 | 16 | 4 | -148.124 | 0.618934 | 0.467812 | 0.571429 | True | -18535.4 | True | 3790.89 | 0.994 | True | 5739.6 | True | 3180.45 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H8_EQ0_9_SQ0_985 | bar_return_reversal | bar_return | reversal | 8 | 0.9 | 0.985 | 5.96138 | 0.00685918 | 42 | 8137.22 | 13255.5 | 5118.3 | 5578.07 | 3018.92 | 5 | 16 | 4 | -1988.51 | 0.598717 | 0.443165 | 0.547619 | True | -18373.8 | True | 3971.8 | 0.994 | True | 5578.07 | True | 3018.92 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H15_EQ0_99_SQ0_95 | bar_return_reversal | bar_return | reversal | 15 | 0.99 | 0.95 | 15.5881 | 0.00915609 | 14 | 6839.46 | 8618.59 | 1779.13 | 5949.89 | 5060.32 | 4 | 10 | 3 | -21.1795 | 0.677115 | 0.363023 | 0.714286 | True | -10397.7 | True | 4502.26 | 0.993 | True | 5949.89 | True | 5060.32 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H6_EQ0_985_SQ0_925 | bar_return_reversal | bar_return | reversal | 6 | 0.985 | 0.925 | 13.2983 | 0.00756605 | 32 | 6841.24 | 10757.1 | 3915.82 | 4883.33 | 2925.42 | 5 | 15 | 4 | -776.325 | 0.653052 | 0.529061 | 0.59375 | True | -14672.9 | True | 4088.08 | 0.993 | True | 4883.33 | True | 2925.42 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H10_EQ0_925_SQ0_985 | bar_return_reversal | bar_return | reversal | 10 | 0.925 | 0.985 | 6.90861 | 0.0077261 | 31 | 6014.8 | 9788.44 | 3773.64 | 4127.98 | 2241.16 | 5 | 14 | 4 | -2041.86 | 0.504374 | 0.573079 | 0.516129 | True | -13562.1 | True | 3510.16 | 0.993 | True | 4127.98 | True | 2241.16 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H4_EQ0_985_SQ0_925 | bar_return_reversal | bar_return | reversal | 4 | 0.985 | 0.925 | 13.2983 | 0.00753115 | 32 | 5532.33 | 9448.15 | 3915.82 | 3574.41 | 1616.5 | 5 | 15 | 3 | -37.1793 | 0.625869 | 0.470534 | 0.5625 | True | -13364 | True | 3499.21 | 0.993 | True | 3574.41 | True | 1616.5 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H8_EQ0_925_SQ0_985 | bar_return_reversal | bar_return | reversal | 8 | 0.925 | 0.985 | 6.90861 | 0.00768821 | 32 | 8445.4 | 12361.2 | 3915.82 | 6487.49 | 4529.58 | 5 | 15 | 4 | -970.633 | 0.533692 | 0.504895 | 0.59375 | True | -16277 | True | 4622.48 | 0.991 | True | 6487.49 | True | 4529.58 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H4_EQ0_95_SQ0_985 | bar_return_reversal | bar_return | reversal | 4 | 0.95 | 0.985 | 8.3341 | 0.00836433 | 22 | 6127.42 | 8883.21 | 2755.79 | 4749.53 | 3371.63 | 5 | 12 | 4 | -396.233 | 0.57615 | 0.295413 | 0.636364 | True | -11639 | True | 3681.54 | 0.99 | True | 4749.53 | True | 3371.63 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H10_EQ0_99_SQ0_95 | bar_return_reversal | bar_return | reversal | 10 | 0.99 | 0.95 | 15.5881 | 0.00909046 | 15 | 6201.9 | 8114.8 | 1912.9 | 5245.45 | 4289 | 4 | 11 | 3 | -1250.41 | 0.66637 | 0.413616 | 0.6 | True | -10027.7 | True | 4469.51 | 0.989 | True | 5245.45 | True | 4289 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H4_EQ0_995_SQ0_9 | bar_return_reversal | bar_return | reversal | 4 | 0.995 | 0.9 | 19.4975 | 0.00908069 | 15 | 6100.35 | 8013.26 | 1912.9 | 5143.9 | 4187.45 | 4 | 11 | 3 | -638.317 | 0.725456 | 0.288569 | 0.666667 | True | -9926.16 | True | 4251.84 | 0.989 | True | 5143.9 | True | 4187.45 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H4_EQ0_975_SQ0_975 | bar_return_reversal | bar_return | reversal | 4 | 0.975 | 0.975 | 10.9692 | 0.00870421 | 18 | 6059.36 | 8348.63 | 2289.28 | 4914.72 | 3770.08 | 5 | 12 | 3 | -638.317 | 0.733907 | 0.290521 | 0.666667 | True | -10637.9 | True | 4331.73 | 0.989 | True | 4914.72 | True | 3770.08 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H8_EQ0_995_SQ0_9 | bar_return_reversal | bar_return | reversal | 8 | 0.995 | 0.9 | 19.4975 | 0.00908069 | 15 | 7955.22 | 9868.13 | 1912.9 | 6998.77 | 6042.32 | 4 | 11 | 3 | -1586.87 | 0.753453 | 0.350152 | 0.733333 | True | -11781 | True | 5396.42 | 0.988 | True | 6998.77 | True | 6042.32 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H4_EQ0_985_SQ0_95 | bar_return_reversal | bar_return | reversal | 4 | 0.985 | 0.95 | 13.2983 | 0.00836567 | 22 | 6127.42 | 8883.21 | 2755.79 | 4749.53 | 3371.63 | 5 | 12 | 4 | -396.233 | 0.57615 | 0.295413 | 0.636364 | True | -11639 | True | 3995.13 | 0.988 | True | 4749.53 | True | 3371.63 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H6_EQ0_985_SQ0_9 | bar_return_reversal | bar_return | reversal | 6 | 0.985 | 0.9 | 13.2983 | 0.00684752 | 43 | 7639.9 | 12871 | 5231.06 | 5024.37 | 2408.84 | 5 | 16 | 3 | -238.443 | 0.67231 | 0.508156 | 0.55814 | True | -18102 | True | 3714.32 | 0.988 | True | 5024.37 | True | 2408.84 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H12_EQ0_99_SQ0_95 | bar_return_reversal | bar_return | reversal | 12 | 0.99 | 0.95 | 15.5881 | 0.00913339 | 14 | 6535.06 | 8314.2 | 1779.13 | 5645.5 | 4755.93 | 4 | 10 | 3 | -1015.98 | 0.687913 | 0.370132 | 0.714286 | True | -10093.3 | True | 4945.49 | 0.987 | True | 5645.5 | True | 4755.93 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H8_EQ0_985_SQ0_95 | bar_return_reversal | bar_return | reversal | 8 | 0.985 | 0.95 | 13.2983 | 0.00837371 | 22 | 7158.18 | 9913.97 | 2755.79 | 5780.29 | 4402.39 | 5 | 12 | 3 | -1043.64 | 0.718028 | 0.389141 | 0.590909 | True | -12669.8 | True | 4637.66 | 0.987 | True | 5780.29 | True | 4402.39 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H10_EQ0_995_SQ0_9 | bar_return_reversal | bar_return | reversal | 10 | 0.995 | 0.9 | 19.4975 | 0.00908069 | 15 | 6201.9 | 8114.8 | 1912.9 | 5245.45 | 4289 | 4 | 11 | 3 | -1250.41 | 0.66637 | 0.413616 | 0.6 | True | -10027.7 | True | 4471.49 | 0.987 | True | 5245.45 | True | 4289 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H6_EQ0_925_SQ0_985 | bar_return_reversal | bar_return | reversal | 6 | 0.925 | 0.985 | 6.90861 | 0.00761142 | 32 | 6841.24 | 10757.1 | 3915.82 | 4883.33 | 2925.42 | 5 | 15 | 4 | -776.325 | 0.653052 | 0.529061 | 0.59375 | True | -14672.9 | True | 4202.35 | 0.987 | True | 4883.33 | True | 2925.42 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H8_EQ0_95_SQ0_975 | bar_return_reversal | bar_return | reversal | 8 | 0.95 | 0.975 | 8.3341 | 0.00725207 | 35 | 7114.38 | 11358.3 | 4243.9 | 4992.43 | 2870.48 | 5 | 16 | 4 | -1688.68 | 0.541064 | 0.506879 | 0.571429 | True | -15602.2 | True | 4437.14 | 0.987 | True | 4992.43 | True | 2870.48 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H8_EQ0_985_SQ0_9 | bar_return_reversal | bar_return | reversal | 8 | 0.985 | 0.9 | 13.2983 | 0.00685033 | 43 | 7723.71 | 12954.8 | 5231.06 | 5108.18 | 2492.65 | 5 | 16 | 4 | -1988.51 | 0.630771 | 0.466891 | 0.534884 | True | -18185.8 | True | 4478.83 | 0.987 | True | 5108.18 | True | 2492.65 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H8_EQ0_975_SQ0_975 | bar_return_reversal | bar_return | reversal | 8 | 0.975 | 0.975 | 10.9692 | 0.00872473 | 18 | 7196.37 | 9485.64 | 2289.28 | 6051.73 | 4907.09 | 5 | 12 | 3 | -1586.87 | 0.80615 | 0.387076 | 0.611111 | True | -11774.9 | True | 4912.97 | 0.986 | True | 6051.73 | True | 4907.09 | True | 4 | True |
| P243_BAR_RETURN_REVERSAL_H4_EQ0_95_SQ0_99 | bar_return_reversal | bar_return | reversal | 4 | 0.95 | 0.99 | 8.3341 | 0.00909046 | 15 | 6100.35 | 8013.26 | 1912.9 | 5143.9 | 4187.45 | 4 | 11 | 3 | -638.317 | 0.725456 | 0.288569 | 0.666667 | True | -9926.16 | True | 4175.78 | 0.986 | True | 5143.9 | True | 4187.45 | True | 4 | True |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P243_PHASE242_WORK_ORDER_PRESENT | True | run_phase243_cost_stress_first_redesign_search_without_2026_07_17_holdout_tuning_no_paper_live | Phase242 next action targets Phase243 | hard |
| P243_VARIANTS_EVALUATED | True | 3920 | >=3000 redesigned variants | hard |
| P243_COST200_SURVIVORS_FOUND | True | 487 | >0 variants positive at 2x costs | hard |
| P243_RANDOM_SIDE_CONTROLLED_SURVIVOR_FOUND | True | 113 | >0 variants pass side flip, random side, 1.5x and 2.0x cost | hard |
| P243_HOLDOUT_DATE_NOT_USED_FOR_TUNING | True | 2026-07-17 | 2026-07-17 excluded | hard |
| P243_NO_DOWNLOAD_OR_PAPER_LIVE_OR_PROFIT_CLAIM | True | 0 | 0 | hard |
