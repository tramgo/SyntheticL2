# Phase266 Full-depth Liquidity-shock Absorption Event Interpretation

Generated UTC: 2026-08-02T02:20:58.309296+00:00

Phase266 interprets the Phase265 full-depth liquidity-shock/absorption training search.
It keeps the core Zerodha top-five depth objective intact: rows 1-5 are required, levels 2-5 must be material, and L1-only variants remain forbidden.
The Phase265 lead is treated as a promising but unaccepted research pocket because it is 2x-cost positive but breadth-fragile and economically weak versus shuffled-label control.
This is not replay execution, strategy promotion, paper/live acceptance, or a deployable profitability claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase266_interpretation_complete | 1 | Phase266 liquidity-shock interpretation completed |
| phase266_phase265_variant_rows | 432 | Phase265 variants interpreted |
| phase266_phase265_full_depth_variant_rows | 432 | Full-depth variants interpreted |
| phase266_phase265_l2_l5_variant_rows | 432 | Levels 2-5 variants interpreted |
| phase266_phase265_l1_only_variant_rows | 0 | L1-only variants interpreted |
| phase266_phase265_cost100_positive_variant_rows | 38 | Phase265 variants positive at 1x charges |
| phase266_phase265_cost150_positive_variant_rows | 6 | Phase265 variants positive at 1.5x charges |
| phase266_phase265_cost200_positive_variant_rows | 2 | Phase265 variants positive at 2x charges |
| phase266_phase265_survivor_candidate_rows | 0 | Phase265 survivors |
| phase266_best_candidate_id | P265_P265_L2L5_BID_ABSORPTION_CONTINUATION_H10_IQ0p9_SQ0p75_SPHIGH | Best Phase265 candidate |
| phase266_best_family_id | P265_L2L5_BID_ABSORPTION_CONTINUATION | Best Phase265 family |
| phase266_best_cost100_net_pnl_inr | 782.036 | Best 1x-charge net P&L |
| phase266_best_cost200_net_pnl_inr | 37.9048 | Best 2x-charge net P&L |
| phase266_best_cost200_avg_net_per_event_inr | 4.21165 | Best 2x average net per event |
| phase266_best_event_rows | 9 | Best event rows |
| phase266_best_symbols | 4 | Best symbol breadth |
| phase266_best_trade_dates | 1 | Best date breadth |
| phase266_best_shuffle_label_net_pnl_inr | 782.036 | Best shuffled-label net P&L |
| phase266_best_shuffle_label_margin_inr | 1.13687e-13 | Best 1x P&L minus shuffled-label P&L |
| phase266_close_phase265_for_promotion | 1 | Close Phase265 for promotion |
| phase266_close_phase265_for_replay | 1 | Close Phase265 for replay |
| phase266_recognize_promising_but_unaccepted_2x_pocket | 1 | Recognize 2x-positive pocket as research lead only |
| phase266_close_current_narrow_liquidity_shock_candidate | 1 | Close narrow candidate for acceptance |
| phase266_full_top_five_depth_preserved | 1 | Preserve full top-five depth |
| phase266_threshold_relaxation_only_allowed | 0 | Threshold relaxation only remains forbidden |
| phase266_selected_next_route | P266_FULL_DEPTH_LIQUIDITY_SHOCK_BREADTH_AND_SHUFFLE_ROBUSTNESS_REPAIR_PRECOMMIT | Selected next route |
| phase266_next_route_contract_rows | 8 | Next route contract rows |
| phase266_hard_gate_pass_rows | 8 | Hard gates passed |
| phase266_hard_gate_rows | 8 | Hard gates evaluated |
| phase266_download_more_dates_now_allowed | 0 | No new download in Phase266 |
| phase266_replay_execution_allowed_now | 0 | No replay execution in Phase266 |
| phase266_strategy_promotion_allowed | 0 | No strategy promotion from Phase266 |
| phase266_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase266 |
| phase266_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase266 |
| phase266_next_best_action | run_phase267_full_depth_liquidity_shock_breadth_shuffle_robustness_repair_precommit_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P266_PHASE265_WORK_ORDER_PRESENT | True | run_phase266_full_depth_liquidity_shock_absorption_event_interpretation_no_paper_live | Phase265 next action targets Phase266 | hard |
| P266_PHASE265_SEARCH_EXECUTED | True | summary=432;rows=432 | Phase265 variants present | hard |
| P266_FULL_DEPTH_RECOGNIZED | True | full_depth=432;l2_l5=432;l1_only=0;variants=432 | all variants full-depth and no L1-only | hard |
| P266_NO_SURVIVOR_RECOGNIZED | True | 0 | 0 Phase265 survivors | hard |
| P266_2X_POSITIVE_BUT_BREADTH_FRAGILE_RECOGNIZED | True | positive_2x=2;best_events=9;best_symbols=4 | 2x-positive pocket must be treated as fragile | hard |
| P266_SHUFFLE_MARGIN_FRAGILITY_RECOGNIZED | True | 1.13687e-13 | shuffled-label separation too small: <100.0 | hard |
| P266_NEXT_ROUTE_SELECTED | True | P266_FULL_DEPTH_LIQUIDITY_SHOCK_BREADTH_AND_SHUFFLE_ROBUSTNESS_REPAIR_PRECOMMIT | Phase267 repair route contract written | hard |
| P266_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE | True | 0 | 0 | hard |

## Failure Mode Ledger

| failure_mode | evidence | severity | closed_or_requires_repair | interpretation |
| --- | --- | --- | --- | --- |
| no_survivor_after_full_control_stack | survivors=0 | hard | 1 | No Phase265 candidate can be promoted or replayed. |
| positive_2x_edge_exists_but_is_tiny_and_sparse | positive_1x=38; positive_1p5=6; positive_2x=2; best_cost100=782.0356498346316; best_cost200=37.90484983463176; best_cost200_avg=4.211649981625751 | hard | 1 | The best result is positive under 2x costs, but the remaining edge per event is too small to treat as robust. |
| best_candidate_breadth_fragile | best_events=9; best_symbols=4; best_dates=1; required_events=30; required_symbols=8; required_dates=1 | hard | 1 | The lead pocket is too narrow for acceptance. |
| positive_2x_breadth_rows_absent | cost200_positive_rows=2; cost200_positive_breadth_rows=0 | hard | 1 | 2x-positive rows do not survive breadth requirements. |
| shuffle_label_margin_not_economic | best_cost100=782.0356498346316; shuffle_label_net=782.0356498346315; shuffle_margin=1.1368683772161603e-13; required_margin=100.0 | hard | 1 | The lead row's shuffled-label separation is effectively not robust enough for acceptance. |
| full_depth_surface_preserved_not_invalidated | full_depth=432; l2_l5=432; l1_only=0; variants=432 | important_context | 1 | Full top-five and levels 2-5 depth remain mandatory and were respected. |

## Decision Ledger

| decision_id | decision_value | evidence | description |
| --- | --- | --- | --- |
| close_phase265_for_promotion | 1 | survivors=0 | Do not promote Phase265 candidates. |
| close_phase265_for_replay | 1 | survivors=0 | Do not execute strategy replay from Phase265. |
| recognize_promising_but_unaccepted_2x_pocket | 1 | positive_2x=2; best=P265_P265_L2L5_BID_ABSORPTION_CONTINUATION_H10_IQ0p9_SQ0p75_SPHIGH | Keep the mechanism alive as a research lead, not as an accepted strategy. |
| close_current_narrow_liquidity_shock_candidate | 1 | best_events=9; best_symbols=4; best_dates=1 | The current narrow pocket is closed for acceptance. |
| preserve_full_top_five_depth_surface | 1 | full_depth=432; l2_l5=432; l1_only=0; variants=432 | Full top-five L2 depth remains the core project surface. |
| threshold_relaxation_only_allowed | 0 | positive pocket is sparse and shuffle-fragile | Do not continue by merely loosening thresholds. |
| material_breadth_and_shuffle_robustness_repair_required | 1 | best candidate is 2x-positive but too sparse and economically weak versus shuffled-label control | Next work must repair breadth and label/control robustness. |
| selected_next_route | P266_FULL_DEPTH_LIQUIDITY_SHOCK_BREADTH_AND_SHUFFLE_ROBUSTNESS_REPAIR_PRECOMMIT | full-depth breadth + shuffle-robustness repair precommit | Next materially different action. |

## Next Route Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P267_INPUT | outputs/phase265/phase265_liquidity_shock_variant_results.csv plus outputs/phase254/phase254_richer_raw_top5_depth_event_bars.parquet | Reuse current full-depth event-bar surface; no new download in the precommit. |
| P267_DEPTH_REQUIREMENT | levels_1_to_5_required_l2_l5_required | Every candidate must use top-five market-by-price rows 1-5 and material levels 2-5 evidence. |
| P267_FORBIDDEN | l1_only;threshold_relaxation_only;paper_live_or_deployable_profitability_claim | No L1-only route, no naked threshold loosening, and no paper/live/profitability acceptance. |
| P267_REPAIR_TARGET | breadth_and_shuffle_robustness | Repair the Phase265 failure by requiring broader events and economically material shuffled-label separation. |
| P267_EVENT_GENERALIZATION | bid_absorption;ask_absorption;spread_compression_absorption;withdrawal_reversal;market_regime_confirmed_absorption | Generalize the mechanism across full-depth families, not by only reusing the top row. |
| P267_ACCEPTANCE_FLOORS | events>=30;symbols>=8;dates>=1;cost200_net>0;cost200_avg_net_per_event>=25;shuffle_margin>=100 | Training candidate floors before any future replay discussion. |
| P267_CONTROLS | side_flip;random_side;shuffled_label_margin;cost_stress_1p5_2x;breadth;no_l1_only | All controls must be explicit in the candidate ledger. |
| P267_NEXT_IF_FAILS | close_liquidity_shock_absorption_route_or_require_more_unseen_real_dates | If breadth/robustness repair fails, stop this route or use fresh unseen real dates rather than overfitting current date. |

## Top Phase265 Variants

| candidate_id | family_id | uses_full_top_five_depth | uses_depth_beyond_l1 | uses_l1_only | horizon | imbalance_quantile | imbalance_min | shock_quantile | shock_min | spread_regime | symbols | trade_dates | cost100_event_rows | cost100_net_pnl_inr | cost100_gross_pnl_inr | cost100_cost_inr | cost100_win_rate | cost100_profit_factor | cost100_avg_net_per_event | cost100_max_drawdown_inr | cost100_cost_hurdle_hit_rate | cost150_event_rows | cost150_net_pnl_inr | cost150_gross_pnl_inr | cost150_cost_inr | cost150_win_rate | cost150_profit_factor | cost150_avg_net_per_event | cost150_max_drawdown_inr | cost150_cost_hurdle_hit_rate | cost200_event_rows | cost200_net_pnl_inr | cost200_gross_pnl_inr | cost200_cost_inr | cost200_win_rate | cost200_profit_factor | cost200_avg_net_per_event | cost200_max_drawdown_inr | cost200_cost_hurdle_hit_rate | side_flip_net_pnl_inr | side_flip_degrades | random_side_net_pnl_inr | random_side_beat | shuffle_label_net_pnl_inr | shuffle_label_beat | survivor_candidate | has_events |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P265_P265_L2L5_BID_ABSORPTION_CONTINUATION_H10_IQ0p9_SQ0p75_SPHIGH | P265_L2L5_BID_ABSORPTION_CONTINUATION | 1 | 1 | 0 | 10 | 0.9 | 0.462853 | 0.75 | 7530.25 | high | 4 | 1 | 9 | 782.036 | 1526.17 | 744.131 | 0.888889 | 3.19759 | 86.8928 | 0 | 0.888889 | 9 | 409.97 | 1526.17 | 1116.2 | 0.888889 | 2.03215 | 45.5522 | 0 | 0.888889 | 9 | 37.9048 | 1526.17 | 1488.26 | 0.666667 | 1.0847 | 4.21165 | -4.49011 | 0.666667 | -2270.3 | 1 | -574.198 | 1 | 782.036 | 1 | 0 | 1 |
| P265_P265_L2L5_ASK_ABSORPTION_CONTINUATION_H10_IQ0p9_SQ0p75_SPLOW | P265_L2L5_ASK_ABSORPTION_CONTINUATION | 1 | 1 | 0 | 10 | 0.9 | 0.462853 | 0.75 | 7530.25 | low | 3 | 1 | 3 | 258.336 | 506.38 | 248.044 | 0.666667 | 14.8708 | 86.112 | -18.6244 | 0.666667 | 3 | 134.314 | 506.38 | 372.065 | 0.666667 | 3.23988 | 44.7714 | -59.965 | 0.666667 | 3 | 10.2925 | 506.38 | 496.087 | 0.666667 | 1.1016 | 3.43082 | -101.306 | 0.666667 | -754.423 | 1 | -269.507 | 1 | 258.336 | 1 | 0 | 1 |
| P265_P265_L2L5_ASK_ABSORPTION_CONTINUATION_H10_IQ0p9_SQ0p9_SPMID | P265_L2L5_ASK_ABSORPTION_CONTINUATION | 1 | 1 | 0 | 10 | 0.9 | 0.462853 | 0.9 | 16804 | mid | 1 | 1 | 1 | -29.5968 | 53.0844 | 82.6812 | 0 | 0 | -29.5968 | 0 | 0 | 1 | -70.9374 | 53.0844 | 124.022 | 0 | 0 | -70.9374 | 0 | 0 | 1 | -112.278 | 53.0844 | 165.362 | 0 | 0 | -112.278 | 0 | 0 | -135.766 | 1 | -29.5968 | 0 | -29.5968 | 0 | 0 | 1 |
| P265_P265_L2L5_ASK_ABSORPTION_CONTINUATION_H6_IQ0p9_SQ0p9_SPMID | P265_L2L5_ASK_ABSORPTION_CONTINUATION | 1 | 1 | 0 | 6 | 0.9 | 0.462853 | 0.9 | 16804 | mid | 1 | 1 | 1 | -46.0713 | 36.6099 | 82.6812 | 0 | 0 | -46.0713 | 0 | 0 | 1 | -87.4119 | 36.6099 | 124.022 | 0 | 0 | -87.4119 | 0 | 0 | 1 | -128.752 | 36.6099 | 165.362 | 0 | 0 | -128.752 | 0 | 0 | -119.291 | 1 | -46.0713 | 0 | -46.0713 | 0 | 0 | 1 |
| P265_P265_L2L5_BID_ABSORPTION_CONTINUATION_H10_IQ0p9_SQ0p9_SPHIGH | P265_L2L5_BID_ABSORPTION_CONTINUATION | 1 | 1 | 0 | 10 | 0.9 | 0.462853 | 0.9 | 16804 | high | 2 | 1 | 6 | 334.056 | 830.143 | 496.087 | 0.833333 | 1.93872 | 55.6759 | 0 | 0.833333 | 6 | 86.0121 | 830.143 | 744.131 | 0.833333 | 1.21655 | 14.3353 | 0 | 0.833333 | 6 | -162.032 | 830.143 | 992.174 | 0.5 | 0.637937 | -27.0053 | -8.98023 | 0.5 | -1326.23 | 1 | 12.3111 | 1 | 334.056 | 1 | 0 | 1 |
| P265_P265_L2L5_ASK_ABSORPTION_CONTINUATION_H3_IQ0p9_SQ0p9_SPMID | P265_L2L5_ASK_ABSORPTION_CONTINUATION | 1 | 1 | 0 | 3 | 0.9 | 0.462853 | 0.9 | 16804 | mid | 1 | 1 | 1 | -95.4947 | -12.8135 | 82.6812 | 0 | 0 | -95.4947 | 0 | 0 | 1 | -136.835 | -12.8135 | 124.022 | 0 | 0 | -136.835 | 0 | 0 | 1 | -178.176 | -12.8135 | 165.362 | 0 | 0 | -178.176 | 0 | 0 | -69.8677 | 0 | -69.8677 | 0 | -95.4947 | 0 | 0 | 1 |
| P265_P265_L2L5_ASK_ABSORPTION_CONTINUATION_H6_IQ0p9_SQ0p75_SPLOW | P265_L2L5_ASK_ABSORPTION_CONTINUATION | 1 | 1 | 0 | 6 | 0.9 | 0.462853 | 0.75 | 7530.25 | low | 3 | 1 | 3 | 3.55142 | 251.595 | 248.044 | 0.333333 | 1.16606 | 1.18381 | -21.3868 | 0.333333 | 3 | -120.47 | 251.595 | 372.065 | 0 | 0 | -40.1568 | -104.068 | 0 | 3 | -244.492 | 251.595 | 496.087 | 0 | 0 | -81.4974 | -186.749 | 0 | -499.639 | 1 | -369.084 | 1 | 3.55142 | 0 | 0 | 1 |
| P265_P265_L2L5_ASK_ABSORPTION_CONTINUATION_H3_IQ0p9_SQ0p75_SPLOW | P265_L2L5_ASK_ABSORPTION_CONTINUATION | 1 | 1 | 0 | 3 | 0.9 | 0.462853 | 0.75 | 7530.25 | low | 3 | 1 | 3 | 2.3178 | 250.361 | 248.044 | 0.666667 | 1.05464 | 0.772599 | -42.4169 | 0.666667 | 3 | -121.704 | 250.361 | 372.065 | 0 | 0 | -40.568 | -114.526 | 0 | 3 | -245.726 | 250.361 | 496.087 | 0 | 0 | -81.9086 | -197.207 | 0 | -498.405 | 1 | -311.899 | 1 | 2.3178 | 0 | 0 | 1 |
| P265_P265_SPREAD_COMPRESSION_ABSORPTION_H10_IQ0p9_SQ0p9_SPHIGH | P265_SPREAD_COMPRESSION_ABSORPTION | 1 | 1 | 0 | 10 | 0.9 | 0.462853 | 0.9 | 175098 | high | 2 | 1 | 5 | 152.32 | 565.726 | 413.406 | 0.8 | 1.42803 | 30.4639 | 0 | 0.8 | 5 | -54.3834 | 565.726 | 620.109 | 0.8 | 0.863084 | -10.8767 | 0 | 0.8 | 5 | -261.086 | 565.726 | 826.812 | 0.4 | 0.416596 | -52.2173 | -4.49011 | 0.4 | -979.132 | 1 | -169.425 | 1 | 152.32 | 0 | 0 | 1 |
| P265_P265_SPREAD_COMPRESSION_ABSORPTION_H10_IQ0p9_SQ0p6_SPMID | P265_SPREAD_COMPRESSION_ABSORPTION | 1 | 1 | 0 | 10 | 0.9 | 0.462853 | 0.6 | 46088 | mid | 5 | 1 | 9 | 478.248 | 1222.38 | 744.131 | 0.444444 | 2.16218 | 53.1387 | -268.105 | 0.444444 | 9 | 106.183 | 1222.38 | 1116.2 | 0.444444 | 1.17176 | 11.7981 | -367.487 | 0.444444 | 9 | -265.883 | 1222.38 | 1488.26 | 0.333333 | 0.683939 | -29.5425 | -574.19 | 0.333333 | -1966.51 | 1 | -1156.75 | 1 | 478.248 | 0 | 0 | 1 |
| P265_P265_SPREAD_COMPRESSION_ABSORPTION_H10_IQ0p9_SQ0p75_SPMID | P265_SPREAD_COMPRESSION_ABSORPTION | 1 | 1 | 0 | 10 | 0.9 | 0.462853 | 0.75 | 80028.5 | mid | 4 | 1 | 8 | 380.355 | 1041.8 | 661.45 | 0.375 | 1.92429 | 47.5444 | -268.105 | 0.375 | 8 | 49.6304 | 1041.8 | 992.174 | 0.375 | 1.08028 | 6.2038 | -424.04 | 0.375 | 8 | -281.094 | 1041.8 | 1322.9 | 0.25 | 0.665857 | -35.1368 | -589.402 | 0.25 | -1703.25 | 1 | -1254.64 | 1 | 380.355 | 0 | 0 | 1 |
| P265_P265_L2L5_BID_ABSORPTION_CONTINUATION_H10_IQ0p9_SQ0p75_SPCOMPRESSION | P265_L2L5_BID_ABSORPTION_CONTINUATION | 1 | 1 | 0 | 10 | 0.9 | 0.462853 | 0.75 | 7530.25 | compression | 7 | 1 | 11 | 570.273 | 1479.77 | 909.493 | 0.727273 | 1.84485 | 51.843 | -484.716 | 0.727273 | 11 | 115.527 | 1479.77 | 1364.24 | 0.636364 | 1.13833 | 10.5024 | -567.397 | 0.636364 | 11 | -339.22 | 1479.77 | 1818.99 | 0.454545 | 0.66397 | -30.8382 | -650.079 | 0.454545 | -2389.26 | 1 | -830.817 | 1 | 570.273 | 0 | 0 | 1 |
| P265_P265_L2L5_ASK_ABSORPTION_CONTINUATION_H6_IQ0p9_SQ0p9_SPHIGH | P265_L2L5_ASK_ABSORPTION_CONTINUATION | 1 | 1 | 0 | 6 | 0.9 | 0.462853 | 0.9 | 16804 | high | 2 | 1 | 2 | -199.752 | -34.3893 | 165.362 | 0 | 0 | -99.8759 | -57.0491 | 0 | 2 | -282.433 | -34.3893 | 248.044 | 0 | 0 | -141.216 | -98.3897 | 0 | 2 | -365.114 | -34.3893 | 330.725 | 0 | 0 | -182.557 | -139.73 | 0 | -130.973 | 0 | -199.752 | 0 | -199.752 | 0 | 0 | 1 |
| P265_P265_L2L5_ASK_ABSORPTION_CONTINUATION_H3_IQ0p75_SQ0p9_SPMID | P265_L2L5_ASK_ABSORPTION_CONTINUATION | 1 | 1 | 0 | 3 | 0.75 | 0.321783 | 0.9 | 16804 | mid | 2 | 1 | 3 | -128.118 | 119.926 | 248.044 | 0 | 0 | -42.706 | -122.501 | 0 | 3 | -252.14 | 119.926 | 372.065 | 0 | 0 | -84.0466 | -205.183 | 0 | 3 | -376.161 | 119.926 | 496.087 | 0 | 0 | -125.387 | -287.864 | 0 | -367.969 | 1 | -256.62 | 1 | -128.118 | 0 | 0 | 1 |
| P265_P265_SPREAD_COMPRESSION_ABSORPTION_H10_IQ0p9_SQ0p9_SPMID | P265_SPREAD_COMPRESSION_ABSORPTION | 1 | 1 | 0 | 10 | 0.9 | 0.462853 | 0.9 | 175098 | mid | 2 | 1 | 5 | 32.5956 | 446.002 | 413.406 | 0.2 | 1.09193 | 6.51913 | -268.105 | 0.2 | 5 | -174.107 | 446.002 | 620.109 | 0.2 | 0.665141 | -34.8215 | -350.786 | 0.2 | 5 | -380.81 | 446.002 | 826.812 | 0.2 | 0.444319 | -76.1621 | -433.467 | 0.2 | -859.408 | 1 | -760.373 | 1 | 32.5956 | 0 | 0 | 1 |
| P265_P265_L2L5_ASK_ABSORPTION_CONTINUATION_H6_IQ0p6_SQ0p9_SPHIGH | P265_L2L5_ASK_ABSORPTION_CONTINUATION | 1 | 1 | 0 | 6 | 0.6 | 0.235897 | 0.9 | 16804 | high | 3 | 1 | 5 | 23.9334 | 437.339 | 413.406 | 0.2 | 1.07329 | 4.78668 | -126.812 | 0.2 | 5 | -182.77 | 437.339 | 620.109 | 0.2 | 0.628461 | -36.5539 | -209.493 | 0.2 | 5 | -389.473 | 437.339 | 826.812 | 0.2 | 0.407456 | -77.8945 | -292.174 | 0.2 | -850.745 | 1 | -53.1676 | 1 | 23.9334 | 0 | 0 | 1 |
| P265_P265_L2L5_ASK_ABSORPTION_CONTINUATION_H3_IQ0p9_SQ0p9_SPHIGH | P265_L2L5_ASK_ABSORPTION_CONTINUATION | 1 | 1 | 0 | 3 | 0.9 | 0.462853 | 0.9 | 16804 | high | 2 | 1 | 2 | -302.554 | -137.192 | 165.362 | 0 | 0 | -151.277 | -82.6812 | 0 | 2 | -385.235 | -137.192 | 248.044 | 0 | 0 | -192.618 | -124.022 | 0 | 2 | -467.917 | -137.192 | 330.725 | 0 | 0 | -233.958 | -165.362 | 0 | -28.1705 | 0 | -302.554 | 0 | -302.554 | 0 | 0 | 1 |
| P265_P265_SPREAD_COMPRESSION_ABSORPTION_H10_IQ0p75_SQ0p9_SPHIGH | P265_SPREAD_COMPRESSION_ABSORPTION | 1 | 1 | 0 | 10 | 0.75 | 0.321783 | 0.9 | 175098 | high | 4 | 1 | 7 | 104.01 | 682.778 | 578.768 | 0.714286 | 1.16666 | 14.8586 | -268.217 | 0.714286 | 7 | -185.374 | 682.778 | 868.153 | 0.714286 | 0.737713 | -26.482 | -309.558 | 0.714286 | 7 | -474.758 | 682.778 | 1157.54 | 0.428571 | 0.405379 | -67.8226 | -355.389 | 0.428571 | -1261.55 | 1 | -451.84 | 1 | 104.01 | 0 | 0 | 1 |
| P265_P265_SPREAD_COMPRESSION_ABSORPTION_H6_IQ0p9_SQ0p9_SPLOW | P265_SPREAD_COMPRESSION_ABSORPTION | 1 | 1 | 0 | 6 | 0.9 | 0.462853 | 0.9 | 175098 | low | 3 | 1 | 4 | -148.61 | 182.114 | 330.725 | 0 | 0 | -37.1526 | -25.912 | 0 | 4 | -313.973 | 182.114 | 496.087 | 0 | 0 | -78.4932 | -149.934 | 0 | 4 | -479.335 | 182.114 | 661.45 | 0 | 0 | -119.834 | -273.956 | 0 | -512.839 | 1 | -225.973 | 1 | -148.61 | 0 | 0 | 1 |
| P265_P265_L2L5_ASK_ABSORPTION_CONTINUATION_H6_IQ0p75_SQ0p9_SPMID | P265_L2L5_ASK_ABSORPTION_CONTINUATION | 1 | 1 | 0 | 6 | 0.75 | 0.321783 | 0.9 | 16804 | mid | 2 | 1 | 3 | -237.128 | 10.9153 | 248.044 | 0 | 0 | -79.0428 | -150.166 | 0 | 3 | -361.15 | 10.9153 | 372.065 | 0 | 0 | -120.383 | -232.847 | 0 | 3 | -485.172 | 10.9153 | 496.087 | 0 | 0 | -161.724 | -315.528 | 0 | -258.959 | 1 | -194.302 | 0 | -237.128 | 0 | 0 | 1 |
