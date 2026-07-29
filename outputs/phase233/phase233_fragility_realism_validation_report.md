# Phase233 Fragility and Realism Validation

Generated UTC: 2026-07-29T06:24:40.657097+00:00

Phase233 stresses the single Phase232 survivor across nearby horizons/thresholds, cost multipliers, feed/regime slices and shock slices.
It remains synthetic-only validation and does not promote a strategy or permit paper/live use.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase233_fragility_realism_validation_complete | 1 | Phase233 validation completed |
| phase233_phase232_survivor_rows | 1 | Phase232 validated candidates available |
| phase233_parent_candidate_id | P231_MICROPRICE_REVERSAL_H3_Q0_9 | Parent Phase232 candidate stressed |
| phase233_neighbor_candidate_rows | 12 | Parameter-neighborhood candidates replayed |
| phase233_neighbor_pass_rows | 7 | Neighbor cells passing train/test stability |
| phase233_parent_test_2x_cost_net_pnl_inr | 179610 | Parent test net P&L under 2x cost drag |
| phase233_gate_pass_rows | 5 | Phase233 gates passed |
| phase233_gate_rows | 5 | Phase233 gates evaluated |
| phase233_fragility_realism_pass | 1 | 1 means Phase233 candidate passes this synthetic fragility/realism layer |
| phase233_strategy_promotion_allowed | 0 | No promotion from synthetic validation alone |
| phase233_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from synthetic validation alone |
| phase233_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from synthetic validation alone |
| phase233_next_best_action | run_phase234_prepare_real_anchor_or_sealed_generator_holdout_for_phase233_candidate_no_paper_live | Next validation milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | interpretation |
| --- | --- | --- | --- | --- |
| P233_PHASE232_SURVIVOR_AVAILABLE | True | 1 | >0 Phase232 validated candidates | Phase233 has a validated synthetic candidate to stress. |
| P233_PARENT_REPLAY_STILL_PASSES | True | 1 | 1 | Parent candidate still passes under the Phase233 recomputation path. |
| P233_PARAMETER_NEIGHBORHOOD_HAS_SURVIVORS | True | 7 | >=2 passing neighbor cells | Candidate should not be a single-cell threshold/horizon accident. |
| P233_TEST_2X_COST_STRESS_PASS | True | 1 | 1 | Parent test split remains positive under 2x cost drag. |
| P233_TEST_FEED_AND_REGIME_BREADTH_PASS | True | feed_positive=5;regime_positive=5 | >=1 feed profile and >=2 regime slices positive | Candidate should not depend on exactly one synthetic regime slice. |

## Neighbor Candidate Summary

| candidate_id | parent_candidate_id | family_id | signal_source | direction | horizon_event_bars | threshold_quantile | event_window_score_threshold | abs_microprice_dev_threshold | parent_horizon_event_bars | parent_threshold_quantile | train_trades | train_net_pnl_inr | train_gross_pnl_inr | train_cost_pnl_drag_inr | train_positive_months | train_months | train_symbols | train_days | train_min_month_net_pnl_inr | train_leave_one_month_min_net_pnl_inr | train_max_month_contribution_abs | train_max_symbol_contribution_abs | train_gross_to_cost_ratio | test_trades | test_net_pnl_inr | test_gross_pnl_inr | test_cost_pnl_drag_inr | test_positive_months | test_months | test_symbols | test_days | test_min_month_net_pnl_inr | test_leave_one_month_min_net_pnl_inr | test_max_month_contribution_abs | test_max_symbol_contribution_abs | test_gross_to_cost_ratio | train_positive | test_positive | test_stable | fragility_neighbor_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P233_MICROPRICE_REVERSAL_H4_Q0_875 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | P231_MICROPRICE_REVERSAL | avg_microprice_dev | reversal | 4 | 0.875 | 48.4975 | 8.71008e-05 | 3 | 0.9 | 532 | 461370 | 533710 | 72339.8 | 4 | 6 | 9 | 26 | -9863.59 | 261025 | 0.43424 | 0.3 | 7.37782 | 434 | 393327 | 450784 | 57457 | 6 | 6 | 9 | 24 | 5897.84 | 263588 | 0.32985 | 0.206041 | 7.84559 | True | True | True | True |
| P233_MICROPRICE_REVERSAL_H3_Q0_875 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | P231_MICROPRICE_REVERSAL | avg_microprice_dev | reversal | 3 | 0.875 | 48.4975 | 8.71008e-05 | 3 | 0.9 | 742 | 423530 | 525499 | 101969 | 5 | 6 | 9 | 28 | -8061.11 | 244144 | 0.423549 | 0.292544 | 5.15352 | 593 | 376481 | 456715 | 80234.2 | 6 | 6 | 9 | 25 | 3942.66 | 240502 | 0.361184 | 0.218037 | 5.69227 | True | True | True | True |
| P233_MICROPRICE_REVERSAL_H4_Q0_9 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | P231_MICROPRICE_REVERSAL | avg_microprice_dev | reversal | 4 | 0.9 | 54.3162 | 0.00010257 | 3 | 0.9 | 337 | 323766 | 371334 | 47567.1 | 5 | 6 | 8 | 16 | -4164.46 | 150382 | 0.535522 | 0.31226 | 7.80652 | 257 | 231100 | 265523 | 34423.2 | 4 | 6 | 8 | 18 | -11140.7 | 130993 | 0.433175 | 0.355211 | 7.71349 | True | True | True | True |
| P233_MICROPRICE_REVERSAL_H3_Q0_9 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | P231_MICROPRICE_REVERSAL | avg_microprice_dev | reversal | 3 | 0.9 | 54.3162 | 0.00010257 | 3 | 0.9 | 471 | 353035 | 420199 | 67164.4 | 6 | 6 | 8 | 18 | 331.929 | 184299 | 0.477958 | 0.289776 | 6.25628 | 365 | 229963 | 280316 | 50353.1 | 4 | 6 | 8 | 19 | -15418.8 | 116948 | 0.491447 | 0.315216 | 5.567 | True | True | True | True |
| P233_MICROPRICE_REVERSAL_H5_Q0_875 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | P231_MICROPRICE_REVERSAL | avg_microprice_dev | reversal | 5 | 0.875 | 48.4975 | 8.71008e-05 | 3 | 0.9 | 309 | 326013 | 367020 | 41007.5 | 5 | 6 | 9 | 22 | -329.902 | 148291 | 0.545137 | 0.330002 | 8.95007 | 296 | 193527 | 231768 | 38240.8 | 4 | 6 | 9 | 23 | -18082.4 | 117821 | 0.391192 | 0.236314 | 6.06075 | True | True | True | True |
| P233_MICROPRICE_REVERSAL_H3_Q0_925 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | P231_MICROPRICE_REVERSAL | avg_microprice_dev | reversal | 3 | 0.925 | 62.0817 | 0.000114883 | 3 | 0.9 | 280 | 274454 | 315927 | 41473.1 | 4 | 5 | 7 | 12 | -17557.2 | 160589 | 0.414876 | 0.304664 | 7.61763 | 202 | 180521 | 209511 | 28989.9 | 6 | 6 | 7 | 15 | 10230.8 | 91534.8 | 0.492941 | 0.332293 | 7.22702 | True | True | True | True |
| P233_MICROPRICE_REVERSAL_H4_Q0_925 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | P231_MICROPRICE_REVERSAL | avg_microprice_dev | reversal | 4 | 0.925 | 62.0817 | 0.000114883 | 3 | 0.9 | 191 | 242485 | 270528 | 28043.3 | 4 | 5 | 7 | 12 | -12800 | 109040 | 0.550325 | 0.316152 | 9.64681 | 134 | 160233 | 178844 | 18610.5 | 6 | 6 | 7 | 15 | 10232 | 80590.3 | 0.497045 | 0.288425 | 9.60983 | True | True | True | True |
| P233_MICROPRICE_REVERSAL_H5_Q0_9 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | P231_MICROPRICE_REVERSAL | avg_microprice_dev | reversal | 5 | 0.9 | 54.3162 | 0.00010257 | 3 | 0.9 | 176 | 208074 | 232088 | 24013.5 | 5 | 6 | 8 | 14 | -2149.04 | 76243.5 | 0.633576 | 0.264619 | 9.66488 | 167 | 101210 | 122683 | 21472.7 | 4 | 6 | 7 | 18 | -21088.1 | 33355.6 | 0.670431 | 0.663007 | 5.71342 | True | True | False | False |
| P233_MICROPRICE_REVERSAL_H2_Q0_875 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | P231_MICROPRICE_REVERSAL | avg_microprice_dev | reversal | 2 | 0.875 | 48.4975 | 8.71008e-05 | 3 | 0.9 | 937 | 298078 | 426749 | 128670 | 5 | 6 | 9 | 29 | -15806.4 | 161378 | 0.458604 | 0.281295 | 3.3166 | 766 | 97116.7 | 200738 | 103621 | 3 | 6 | 9 | 29 | -22559.7 | 13982.2 | 0.856027 | 0.655342 | 1.93723 | True | True | False | False |
| P233_MICROPRICE_REVERSAL_H5_Q0_925 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | P231_MICROPRICE_REVERSAL | avg_microprice_dev | reversal | 5 | 0.925 | 62.0817 | 0.000114883 | 3 | 0.9 | 84 | 153256 | 165226 | 11970.3 | 2 | 4 | 7 | 9 | -8139.39 | 20874.1 | 0.863796 | 0.361631 | 13.803 | 82 | 71052 | 81859.4 | 10807.4 | 4 | 5 | 5 | 14 | -6495.82 | 1490.96 | 0.979016 | 0.495391 | 7.57439 | True | True | False | False |
| P233_MICROPRICE_REVERSAL_H2_Q0_925 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | P231_MICROPRICE_REVERSAL | avg_microprice_dev | reversal | 2 | 0.925 | 62.0817 | 0.000114883 | 3 | 0.9 | 352 | 227447 | 279488 | 52040.5 | 4 | 5 | 8 | 13 | -11687.9 | 89870.2 | 0.604875 | 0.312554 | 5.37059 | 263 | 41722.6 | 79796.7 | 38074.1 | 5 | 6 | 7 | 16 | -30058.4 | 6877.67 | 0.835157 | 1.02633 | 2.09582 | True | True | False | False |
| P233_MICROPRICE_REVERSAL_H2_Q0_9 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | P231_MICROPRICE_REVERSAL | avg_microprice_dev | reversal | 2 | 0.9 | 54.3162 | 0.00010257 | 3 | 0.9 | 598 | 277908 | 363050 | 85141.7 | 4 | 6 | 8 | 18 | -23340 | 151411 | 0.455178 | 0.327952 | 4.26407 | 481 | 41629.9 | 108180 | 66549.9 | 2 | 6 | 8 | 21 | -28499.2 | -19161.7 | 1.46029 | 1.24978 | 1.62554 | True | True | False | False |

## Cost Multiplier Summary

| split | cost_multiplier | net_pnl_inr | positive_months | leave_one_month_min_net_pnl_inr | gross_to_cost_ratio | cost_multiplier_pass |
| --- | --- | --- | --- | --- | --- | --- |
| train | 1 | 353035 | 6 | 184299 | 6.25628 | True |
| train | 1.25 | 336244 | 6 | 170318 | 5.00502 | True |
| train | 1.5 | 319453 | 4 | 156337 | 4.17085 | True |
| train | 2 | 285870 | 4 | 128375 | 3.12814 | True |
| test | 1 | 229963 | 4 | 116948 | 5.567 | True |
| test | 1.25 | 217375 | 4 | 106789 | 4.4536 | True |
| test | 1.5 | 204786 | 4 | 96629.7 | 3.71134 | True |
| test | 2 | 179610 | 4 | 76311.1 | 2.7835 | True |

## Realism Slice Summary

| split | slice_name | slice_value | trades | symbols | days | net_pnl_inr | gross_pnl_inr | cost_pnl_drag_inr | positive_slice |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train | feed_profile | disconnect_scenario | 90 | 8 | 14 | 107034 | 119827 | 12792.9 | True |
| train | feed_profile | good_retail | 89 | 8 | 15 | 60621.8 | 73339.3 | 12717.4 | True |
| train | feed_profile | ideal_research | 121 | 8 | 16 | 56544.4 | 73804.7 | 17260.3 | True |
| train | feed_profile | normal_retail | 87 | 8 | 15 | 53688.7 | 66135.1 | 12446.4 | True |
| train | feed_profile | stressed_retail | 84 | 8 | 15 | 75145.2 | 87092.5 | 11947.3 | True |
| train | regime_code | D04 | 5 | 1 | 1 | -12471.7 | -11904.9 | 566.818 | False |
| train | regime_code | D05 | 18 | 4 | 4 | -1351.51 | 773.677 | 2125.19 | False |
| train | regime_code | D07 | 320 | 8 | 5 | 418337 | 465301 | 46964.1 | True |
| train | regime_code | D08 | 37 | 6 | 3 | -17346.5 | -12591.5 | 4754.97 | False |
| train | regime_code | D10 | 9 | 2 | 2 | 5363.63 | 6399.9 | 1036.27 | True |
| train | regime_code | D12 | 9 | 2 | 1 | -1823.33 | -737.584 | 1085.75 | False |
| train | regime_code | D20 | 73 | 8 | 2 | -37673.3 | -27042 | 10631.2 | False |
| train | shock_bar | False | 49 | 3 | 7 | -12898.4 | -7177.97 | 5720.39 | False |
| train | shock_bar | True | 422 | 8 | 11 | 365933 | 427377 | 61444 | True |
| train | market_shock_bar | 0 | 49 | 3 | 7 | -12898.4 | -7177.97 | 5720.39 | False |
| train | market_shock_bar | 1 | 422 | 8 | 11 | 365933 | 427377 | 61444 | True |
| train | symbol_shock_bar | 0 | 190 | 6 | 18 | 31393.9 | 55514.3 | 24120.4 | True |
| train | symbol_shock_bar | 1 | 281 | 6 | 7 | 321641 | 364685 | 43044 | True |
| test | feed_profile | disconnect_scenario | 77 | 8 | 18 | 76626.5 | 87277.4 | 10650.9 | True |
| test | feed_profile | good_retail | 63 | 8 | 18 | 32680.2 | 41281.1 | 8600.82 | True |
| test | feed_profile | ideal_research | 93 | 8 | 19 | 23582.2 | 36488.3 | 12906.1 | True |
| test | feed_profile | normal_retail | 67 | 8 | 18 | 45662.5 | 54870.1 | 9207.63 | True |
| test | feed_profile | stressed_retail | 65 | 8 | 16 | 51411.4 | 60399 | 8987.62 | True |
| test | regime_code | D03 | 10 | 2 | 1 | 4010.11 | 5212.51 | 1202.39 | True |
| test | regime_code | D05 | 40 | 2 | 3 | 5055.5 | 9723.19 | 4667.69 | True |
| test | regime_code | D07 | 201 | 8 | 5 | 183229 | 212397 | 29167.6 | True |
| test | regime_code | D08 | 10 | 2 | 1 | -4050.92 | -2892.43 | 1158.49 | False |
| test | regime_code | D10 | 14 | 2 | 2 | 6580.58 | 8260.63 | 1680.05 | True |
| test | regime_code | D12 | 20 | 2 | 4 | -11237.3 | -8896.99 | 2340.32 | False |
| test | regime_code | D20 | 70 | 7 | 3 | 46375.4 | 56511.9 | 10136.5 | True |
| test | shock_bar | False | 94 | 2 | 11 | 357.974 | 11406.9 | 11048.9 | True |
| test | shock_bar | True | 271 | 8 | 8 | 229605 | 268909 | 39304.2 | True |
| test | market_shock_bar | 0 | 94 | 2 | 11 | 357.974 | 11406.9 | 11048.9 | True |
| test | market_shock_bar | 1 | 271 | 8 | 8 | 229605 | 268909 | 39304.2 | True |
| test | symbol_shock_bar | 0 | 182 | 5 | 19 | 11963.4 | 34394.5 | 22431.1 | True |
| test | symbol_shock_bar | 1 | 183 | 6 | 8 | 217999 | 245921 | 27921.9 | True |
