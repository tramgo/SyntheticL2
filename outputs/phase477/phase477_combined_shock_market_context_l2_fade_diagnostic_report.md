# Phase477 Combined Shock Market-Context L2 Fade Diagnostic

Phase477 executes the frozen Phase476 combined-clue diagnostic: shock/catalyst context plus market-neutral depth-2-5 fade, with controls.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase477_combined_shock_market_context_l2_fade_diagnostic_complete | 1 | Phase477 diagnostic completed |
| phase477_thesis_id | P477_COMBINED_SHOCK_MARKET_CONTEXT_L2_FADE_DIAGNOSTIC | Diagnostic thesis |
| phase477_best_primary_scenario_id | horizon_1800_deep_l25_fade_top10_cost200 | Best deep L2-L5 fade scenario |
| phase477_best_primary_trade_count | 10 | Best primary trade count |
| phase477_best_primary_net_pnl_inr | -360.106 | Best primary net P&L |
| phase477_best_primary_annualized_return_pct | -45.3733 | Best primary fixed-capital annualized return |
| phase477_primary_positive_scenario_rows | 0 | Positive primary scenarios |
| phase477_primary_above12_scenario_rows | 0 | Primary scenarios above 12% |
| phase477_best_primary_acceptance_event_floor_met | 0 | Acceptance event floor met |
| phase477_fixed_capital_inr | 100000 | Reusable capital denominator |
| phase477_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Cost model version |
| phase477_zerodha_cost_source_url | https://zerodha.com/charges/ | Cost source |
| phase477_strategy_promotion_allowed | 0 | No promotion |
| phase477_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase477_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase477_phase478_allowed_next | 0 | Allows expansion precommit only if all gates pass |
| phase477_hard_gate_pass_rows | 11 | Passed hard gates |
| phase477_hard_gate_rows | 14 | Hard gates |
| phase477_next_best_action | interpret_phase477_combined_clue_failure_or_close_synthetic_branch | Recommended next action |

## Candidate Summary

| horizon_ticks | candidate_rows | holdout_days | symbols | train_l25_abs_q75 | train_source_event_l25_ofi_abs_q75 |
| --- | --- | --- | --- | --- | --- |
| 480 | 35 | 2 | 7 | 0.439597 | 122 |
| 960 | 35 | 2 | 7 | 0.439597 | 122 |
| 1800 | 35 | 2 | 7 | 0.439597 | 122 |

## Scenario Summary

| scenario_id | horizon_ticks | rule_id | top_count | candidate_rows | trade_count | holdout_days | gross_pnl_inr | zerodha_total_charges_inr | adverse_slippage_inr | net_pnl_inr | annualized_return_pct | win_rate | avg_net_per_trade_inr | max_daily_drawdown_inr | diagnostic_event_floor_met | acceptance_event_floor_met | acceptance_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| horizon_480_deep_l25_fade_top10_cost200 | 480 | deep_l25_fade | 10 | 35 | 10 | 2 | -269.008 | 825.932 | 198.357 | -1293.3 | -162.955 | 0.1 | -129.33 | -339.872 | 1 | 0 | 0 |
| horizon_480_deep_l25_fade_top20_cost200 | 480 | deep_l25_fade | 20 | 35 | 20 | 2 | -739.879 | 1651.92 | 396.799 | -2788.6 | -351.364 | 0.05 | -139.43 | -1172.36 | 1 | 0 | 0 |
| horizon_480_deep_l25_fade_top40_cost200 | 480 | deep_l25_fade | 40 | 35 | 34 | 2 | -898.705 | 2808.41 | 674.828 | -4381.95 | -552.125 | 0.0588235 | -128.881 | -2096.73 | 1 | 1 | 0 |
| horizon_480_top1_fade_reference_top10_cost200 | 480 | top1_fade_reference | 10 | 35 | 10 | 2 | -269.008 | 825.932 | 198.357 | -1293.3 | -162.955 | 0.1 | -129.33 | -339.872 | 1 | 0 | 0 |
| horizon_480_top1_fade_reference_top20_cost200 | 480 | top1_fade_reference | 20 | 35 | 20 | 2 | -739.879 | 1651.92 | 396.799 | -2788.6 | -351.364 | 0.05 | -139.43 | -1172.36 | 1 | 0 | 0 |
| horizon_480_top1_fade_reference_top40_cost200 | 480 | top1_fade_reference | 40 | 35 | 35 | 2 | -809.267 | 2890.92 | 694.499 | -4394.68 | -553.73 | 0.0571429 | -125.562 | -2109.46 | 1 | 1 | 0 |
| horizon_480_deep_l25_momentum_control_top10_cost200 | 480 | deep_l25_momentum_control | 10 | 35 | 10 | 2 | 269.008 | 825.924 | 198.357 | -755.273 | -95.1644 | 0.2 | -75.5273 | -274.676 | 1 | 0 | 0 |
| horizon_480_deep_l25_momentum_control_top20_cost200 | 480 | deep_l25_momentum_control | 20 | 35 | 20 | 2 | 739.879 | 1651.9 | 396.799 | -1308.82 | -164.911 | 0.2 | -65.441 | -876.785 | 1 | 0 | 0 |
| horizon_480_deep_l25_momentum_control_top40_cost200 | 480 | deep_l25_momentum_control | 40 | 35 | 34 | 2 | 898.705 | 2808.39 | 674.828 | -2584.51 | -325.648 | 0.205882 | -76.015 | -1386.28 | 1 | 1 | 0 |
| horizon_480_deterministic_alternate_control_top10_cost200 | 480 | deterministic_alternate_control | 10 | 35 | 10 | 2 | 370.678 | 825.922 | 198.357 | -653.602 | -82.3538 | 0.3 | -65.3602 | -304.636 | 1 | 0 | 0 |
| horizon_480_deterministic_alternate_control_top20_cost200 | 480 | deterministic_alternate_control | 20 | 35 | 20 | 2 | 555.998 | 1651.9 | 396.799 | -1492.7 | -188.081 | 0.25 | -74.6352 | -1055.8 | 1 | 0 | 0 |
| horizon_480_deterministic_alternate_control_top40_cost200 | 480 | deterministic_alternate_control | 40 | 35 | 35 | 2 | 1038.32 | 2890.89 | 694.499 | -2547.07 | -320.93 | 0.228571 | -72.7733 | -1693.35 | 1 | 1 | 0 |
| horizon_960_deep_l25_fade_top10_cost200 | 960 | deep_l25_fade | 10 | 35 | 10 | 2 | 176.962 | 825.952 | 198.357 | -847.347 | -106.766 | 0.2 | -84.7347 | -348.415 | 1 | 0 | 0 |
| horizon_960_deep_l25_fade_top20_cost200 | 960 | deep_l25_fade | 20 | 35 | 20 | 2 | -340.873 | 1651.95 | 396.799 | -2389.62 | -301.093 | 0.1 | -119.481 | -1290.35 | 1 | 0 | 0 |
| horizon_960_deep_l25_fade_top40_cost200 | 960 | deep_l25_fade | 40 | 35 | 34 | 2 | -317.879 | 2808.45 | 674.828 | -3801.16 | -478.946 | 0.176471 | -111.799 | -2057.75 | 1 | 1 | 0 |
| horizon_960_top1_fade_reference_top10_cost200 | 960 | top1_fade_reference | 10 | 35 | 10 | 2 | 176.962 | 825.952 | 198.357 | -847.347 | -106.766 | 0.2 | -84.7347 | -348.415 | 1 | 0 | 0 |
| horizon_960_top1_fade_reference_top20_cost200 | 960 | top1_fade_reference | 20 | 35 | 20 | 2 | -340.873 | 1651.95 | 396.799 | -2389.62 | -301.093 | 0.1 | -119.481 | -1290.35 | 1 | 0 | 0 |
| horizon_960_top1_fade_reference_top40_cost200 | 960 | top1_fade_reference | 40 | 35 | 35 | 2 | -261.179 | 2890.95 | 694.499 | -3846.63 | -484.676 | 0.171429 | -109.904 | -2103.23 | 1 | 1 | 0 |
| horizon_960_deep_l25_momentum_control_top10_cost200 | 960 | deep_l25_momentum_control | 10 | 35 | 10 | 2 | -176.962 | 825.957 | 198.357 | -1201.28 | -151.361 | 0.3 | -120.128 | -266.139 | 1 | 0 | 0 |
| horizon_960_deep_l25_momentum_control_top20_cost200 | 960 | deep_l25_momentum_control | 20 | 35 | 20 | 2 | 340.873 | 1651.94 | 396.799 | -1707.87 | -215.192 | 0.35 | -85.3935 | -758.791 | 1 | 0 | 0 |
| horizon_960_deep_l25_momentum_control_top40_cost200 | 960 | deep_l25_momentum_control | 40 | 35 | 34 | 2 | 317.879 | 2808.44 | 674.828 | -3165.39 | -398.839 | 0.264706 | -93.0996 | -1425.26 | 1 | 1 | 0 |
| horizon_960_deterministic_alternate_control_top10_cost200 | 960 | deterministic_alternate_control | 10 | 35 | 10 | 2 | 296.287 | 825.95 | 198.357 | -728.02 | -91.7305 | 0.4 | -72.802 | -240.728 | 1 | 0 | 0 |
| horizon_960_deterministic_alternate_control_top20_cost200 | 960 | deterministic_alternate_control | 20 | 35 | 20 | 2 | 245.672 | 1651.94 | 396.799 | -1803.07 | -227.187 | 0.3 | -90.1536 | -1301.84 | 1 | 0 | 0 |
| horizon_960_deterministic_alternate_control_top40_cost200 | 960 | deterministic_alternate_control | 40 | 35 | 35 | 2 | 709.159 | 2890.94 | 694.499 | -2876.28 | -362.411 | 0.285714 | -82.1794 | -2036.07 | 1 | 1 | 0 |
| horizon_1800_deep_l25_fade_top10_cost200 | 1800 | deep_l25_fade | 10 | 35 | 10 | 2 | 664.228 | 825.977 | 198.357 | -360.106 | -45.3733 | 0.2 | -36.0106 | -319.913 | 1 | 0 | 0 |
| horizon_1800_deep_l25_fade_top20_cost200 | 1800 | deep_l25_fade | 20 | 35 | 20 | 2 | 733.322 | 1651.99 | 396.799 | -1315.46 | -165.748 | 0.15 | -65.7731 | -1084.38 | 1 | 0 | 0 |
| horizon_1800_deep_l25_fade_top40_cost200 | 1800 | deep_l25_fade | 40 | 35 | 34 | 2 | 397.639 | 2808.52 | 674.828 | -3085.71 | -388.799 | 0.147059 | -90.756 | -1912.3 | 1 | 1 | 0 |
| horizon_1800_top1_fade_reference_top10_cost200 | 1800 | top1_fade_reference | 10 | 35 | 10 | 2 | 664.228 | 825.977 | 198.357 | -360.106 | -45.3733 | 0.2 | -36.0106 | -319.913 | 1 | 0 | 0 |
| horizon_1800_top1_fade_reference_top20_cost200 | 1800 | top1_fade_reference | 20 | 35 | 20 | 2 | 733.322 | 1651.99 | 396.799 | -1315.46 | -165.748 | 0.15 | -65.7731 | -1084.38 | 1 | 0 | 0 |
| horizon_1800_top1_fade_reference_top40_cost200 | 1800 | top1_fade_reference | 40 | 35 | 35 | 2 | 395.614 | 2891.03 | 694.499 | -3189.91 | -401.929 | 0.142857 | -91.1403 | -2016.5 | 1 | 1 | 0 |
| horizon_1800_deep_l25_momentum_control_top10_cost200 | 1800 | deep_l25_momentum_control | 10 | 35 | 10 | 2 | -664.228 | 825.997 | 198.357 | -1688.58 | -212.761 | 0 | -168.858 | -294.657 | 1 | 0 | 0 |
| horizon_1800_deep_l25_momentum_control_top20_cost200 | 1800 | deep_l25_momentum_control | 20 | 35 | 20 | 2 | -733.322 | 1652.01 | 396.799 | -2782.13 | -350.548 | 0 | -139.106 | -964.807 | 1 | 0 | 0 |
| horizon_1800_deep_l25_momentum_control_top40_cost200 | 1800 | deep_l25_momentum_control | 40 | 35 | 34 | 2 | -397.639 | 2808.53 | 674.828 | -3881 | -489.005 | 0.0882353 | -114.147 | -1570.78 | 1 | 1 | 0 |
| horizon_1800_deterministic_alternate_control_top10_cost200 | 1800 | deterministic_alternate_control | 10 | 35 | 10 | 2 | -468.373 | 825.994 | 198.357 | -1492.72 | -188.083 | 0.1 | -149.272 | -302.812 | 1 | 0 | 0 |
| horizon_1800_deterministic_alternate_control_top20_cost200 | 1800 | deterministic_alternate_control | 20 | 35 | 20 | 2 | -549.148 | 1652.01 | 396.799 | -2597.95 | -327.342 | 0.1 | -129.898 | -1231.4 | 1 | 0 | 0 |
| horizon_1800_deterministic_alternate_control_top40_cost200 | 1800 | deterministic_alternate_control | 40 | 35 | 35 | 2 | -361.076 | 2891.04 | 694.499 | -3946.61 | -497.273 | 0.171429 | -112.76 | -2023.45 | 1 | 1 | 0 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P477_PHASE476_CONTRACT_USED | True | 1 | 1 | hard |
| P477_THESIS_MATCHES_CONTRACT | True | P477_COMBINED_SHOCK_MARKET_CONTEXT_L2_FADE_DIAGNOSTIC | P477_COMBINED_SHOCK_MARKET_CONTEXT_L2_FADE_DIAGNOSTIC | hard |
| P477_CLOSED_PHASE338_NOT_USED | True | 0 | 0 | hard |
| P477_NOT_PHASE475_GRID_ONLY | True | 0 | 0 | hard |
| P477_FULL_DEPTH_DEEP_FADE_RULE_EXECUTED | True | deep_l25_fade | present | hard |
| P477_CANDIDATES_PRESENT_ALL_HORIZONS | True | 3 | 3 | hard |
| P477_COST200_INCLUDED | True | 2 | 2 | hard |
| P477_FIXED_CAPITAL_USED | True | 100000 | 100000 | hard |
| P477_PRIMARY_POSITIVE_SCENARIO_EXISTS | False | 0 | >0 | hard |
| P477_PRIMARY_ABOVE_12PCT_SCENARIO_EXISTS | False | 0 | >0 | hard |
| P477_BEST_PRIMARY_TRADE_COUNT_GE_10 | True | 10 | >=10 | hard |
| P477_BEST_PRIMARY_BEATS_BEST_CONTROL | False | primary=-45.37334984148784;control=-45.37334984148784 | primary>control | hard |
| P477_ACCEPTANCE_EVENT_FLOOR_CHECKED | True | 0 | checked | hard |
| P477_NO_PAPER_LIVE_OR_CLAIM | True | paper=0;claim=0 | all_zero | hard |

Boundary: Phase477 is diagnostic only. It is not paper/live acceptance and not a deployable profitability claim.
