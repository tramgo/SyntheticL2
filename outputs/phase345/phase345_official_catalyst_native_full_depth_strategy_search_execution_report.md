# Phase345 Official-Catalyst-Native Full-Depth Strategy Search Execution

Generated: 2026-08-11T08:23:26.041837+00:00

Phase345 executes the Phase344 material-new official-catalyst-native full-depth grid. Results remain diagnostic until interpreted.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase345_official_catalyst_native_full_depth_strategy_search_execution_complete | 1 | Phase345 execution completed |
| phase345_phase344_complete | 1 | Phase344 complete |
| phase345_grid_rows | 67 | Search grid rows |
| phase345_trade_rows | 6566 | Scenario trade rows |
| phase345_capacity_summary_rows | 67 | Capacity-capped scenario summaries |
| phase345_capacity_above12_rows | 11 | Capacity scenarios above 12% |
| phase345_acceptance_candidate_rows | 0 | Acceptance candidate rows |
| phase345_best_capacity_scenario_id | P345_0002_P344_CATALYST_CATEGORY_CONTINUATION_market_open_or_first_tick_after_announcement_H300_Q0p75 | Best capacity scenario |
| phase345_best_capacity_family_id | P344_CATALYST_CATEGORY_CONTINUATION | Best capacity family |
| phase345_best_capacity_annualized_return_pct | 73.0862 | Best capacity annualized return |
| phase345_best_capacity_net_pnl_inr | 2175.19 | Best capacity net PnL |
| phase345_best_capacity_trade_rows | 6 | Best capacity trade rows |
| phase345_best_capacity_control_pass | 0 | Best capacity control pass |
| phase345_strategy_promotion_allowed | 0 | No promotion |
| phase345_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase345_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase345_hard_gate_pass_rows | 7 | Passed hard gates |
| phase345_hard_gate_rows | 7 | Hard gates |
| phase345_next_best_action | run_phase346_official_catalyst_native_search_interpretation_no_paper_live | Recommended next action |

## Top capacity scenarios

| scenario_id | scope | family_id | entry_timing_policy | horizon_seconds | depth_threshold_quantile | trade_rows | diagnostic_trade_dates | symbols | positive_symbol_date_cells | net_pnl_inr | side_flip_net_pnl_inr | random_side_net_pnl_inr | annualized_return_pct | side_flip_annualized_return_pct | random_side_annualized_return_pct | control_pass | above12 | acceptance_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P345_0002_P344_CATALYST_CATEGORY_CONTINUATION_market_open_or_first_tick_after_announcement_H300_Q0p75 | capacity_capped | P344_CATALYST_CATEGORY_CONTINUATION | market_open_or_first_tick_after_announcement | 300 | 0.75 | 6 | 3 | 5 | 5 | 2175.19 | -4824.3 | 2175.19 | 73.0862 | -162.097 | 73.0862 | 0 | 1 | 0 |
| P345_0065_P344_SBIN_AND_BANK_CATALYST_DIAGNOSTIC_delay_300s_H1800_Q0p75 | capacity_capped | P344_SBIN_AND_BANK_CATALYST_DIAGNOSTIC | delay_300s | 1800 | 0.75 | 2 | 2 | 2 | 1 | 1135.17 | -1922.53 | -1775.52 | 57.2124 | -96.8956 | -89.4863 | 1 | 1 | 0 |
| P345_0062_P344_SBIN_AND_BANK_CATALYST_DIAGNOSTIC_delay_300s_H900_Q0p75 | capacity_capped | P344_SBIN_AND_BANK_CATALYST_DIAGNOSTIC | delay_300s | 900 | 0.75 | 2 | 2 | 2 | 1 | 778.194 | -1502.48 | 624.189 | 39.221 | -75.7248 | 31.4591 | 1 | 1 | 0 |
| P345_0012_P344_CATALYST_CATEGORY_CONTINUATION_delay_60s_H900_Q0p0 | capacity_capped | P344_CATALYST_CATEGORY_CONTINUATION | delay_60s | 900 | 0 | 19 | 6 | 11 | 7 | 2274.57 | -9467.32 | -2692.21 | 38.2127 | -159.051 | -45.2292 | 1 | 1 | 0 |
| P345_0007_P344_CATALYST_CATEGORY_CONTINUATION_market_open_or_first_tick_after_announcement_H1800_Q0p5 | capacity_capped | P344_CATALYST_CATEGORY_CONTINUATION | market_open_or_first_tick_after_announcement | 1800 | 0.5 | 11 | 5 | 8 | 4 | 1745.24 | -6179.55 | -2269.95 | 35.184 | -124.58 | -45.7622 | 1 | 1 | 0 |
| P345_0026_P344_CATALYST_CATEGORY_CONTINUATION_delay_300s_H1800_Q0p75 | capacity_capped | P344_CATALYST_CATEGORY_CONTINUATION | delay_300s | 1800 | 0.75 | 2 | 1 | 2 | 1 | 347.834 | -1100.21 | -1100.21 | 35.0616 | -110.901 | -110.901 | 1 | 1 | 0 |
| P345_0004_P344_CATALYST_CATEGORY_CONTINUATION_market_open_or_first_tick_after_announcement_H900_Q0p5 | capacity_capped | P344_CATALYST_CATEGORY_CONTINUATION | market_open_or_first_tick_after_announcement | 900 | 0.5 | 11 | 5 | 8 | 5 | 1562.75 | -6043.33 | -2850.67 | 31.5051 | -121.834 | -57.4694 | 1 | 1 | 0 |
| P345_0015_P344_CATALYST_CATEGORY_CONTINUATION_delay_60s_H1800_Q0p0 | capacity_capped | P344_CATALYST_CATEGORY_CONTINUATION | delay_60s | 1800 | 0 | 19 | 6 | 11 | 8 | 1793.51 | -9056.37 | 1387.65 | 30.131 | -152.147 | 23.3125 | 1 | 1 | 0 |
| P345_0006_P344_CATALYST_CATEGORY_CONTINUATION_market_open_or_first_tick_after_announcement_H1800_Q0p0 | capacity_capped | P344_CATALYST_CATEGORY_CONTINUATION | market_open_or_first_tick_after_announcement | 1800 | 0 | 19 | 6 | 10 | 7 | 1728.59 | -9289.1 | -8031.67 | 29.0403 | -156.057 | -134.932 | 1 | 1 | 0 |
| P345_0008_P344_CATALYST_CATEGORY_CONTINUATION_market_open_or_first_tick_after_announcement_H1800_Q0p75 | capacity_capped | P344_CATALYST_CATEGORY_CONTINUATION | market_open_or_first_tick_after_announcement | 1800 | 0.75 | 6 | 3 | 5 | 3 | 377.02 | -2910.25 | -3928.1 | 12.6679 | -97.7842 | -131.984 | 1 | 1 | 0 |
| P345_0003_P344_CATALYST_CATEGORY_CONTINUATION_market_open_or_first_tick_after_announcement_H900_Q0p0 | capacity_capped | P344_CATALYST_CATEGORY_CONTINUATION | market_open_or_first_tick_after_announcement | 900 | 0 | 19 | 6 | 10 | 6 | 742.405 | -8314.57 | -6974.15 | 12.4724 | -139.685 | -117.166 | 1 | 1 | 0 |
| P345_0013_P344_CATALYST_CATEGORY_CONTINUATION_delay_60s_H900_Q0p5 | capacity_capped | P344_CATALYST_CATEGORY_CONTINUATION | delay_60s | 900 | 0.5 | 6 | 4 | 5 | 1 | 409.963 | -2639.33 | 405.763 | 10.3311 | -66.5112 | 10.2252 | 1 | 0 | 0 |
| P345_0010_P344_CATALYST_CATEGORY_CONTINUATION_delay_60s_H300_Q0p5 | capacity_capped | P344_CATALYST_CATEGORY_CONTINUATION | delay_60s | 300 | 0.5 | 6 | 4 | 5 | 1 | 370.565 | -2632.83 | -1065.58 | 9.33825 | -66.3473 | -26.8526 | 1 | 0 | 0 |
| P345_0005_P344_CATALYST_CATEGORY_CONTINUATION_market_open_or_first_tick_after_announcement_H900_Q0p75 | capacity_capped | P344_CATALYST_CATEGORY_CONTINUATION | market_open_or_first_tick_after_announcement | 900 | 0.75 | 6 | 3 | 5 | 3 | 27.4459 | -2586.3 | -1011.16 | 0.922184 | -86.8997 | -33.9751 | 1 | 0 | 0 |
| P345_0048_P344_FULL_DEPTH_CATALYST_REACTION_FILTER_delay_300s_H900_Q0p0 | capacity_capped | P344_FULL_DEPTH_CATALYST_REACTION_FILTER | delay_300s | 900 | 0 | 36 | 7 | 18 | 10 | -71.7239 | -13473.9 | -5087.76 | -1.03282 | -194.024 | -73.2638 | 1 | 0 | 0 |
| P345_0001_P344_CATALYST_CATEGORY_CONTINUATION_market_open_or_first_tick_after_announcement_H300_Q0p5 | capacity_capped | P344_CATALYST_CATEGORY_CONTINUATION | market_open_or_first_tick_after_announcement | 300 | 0.5 | 11 | 5 | 8 | 4 | -93.6227 | -4495.03 | -2515.28 | -1.88743 | -90.6197 | -50.708 | 1 | 0 | 0 |
| P345_0009_P344_CATALYST_CATEGORY_CONTINUATION_delay_60s_H300_Q0p0 | capacity_capped | P344_CATALYST_CATEGORY_CONTINUATION | delay_60s | 300 | 0 | 19 | 6 | 11 | 5 | -114.896 | -7222.36 | -2538.66 | -1.93026 | -121.336 | -42.6496 | 1 | 0 | 0 |
| P345_0061_P344_SBIN_AND_BANK_CATALYST_DIAGNOSTIC_delay_300s_H900_Q0p5 | capacity_capped | P344_SBIN_AND_BANK_CATALYST_DIAGNOSTIC | delay_300s | 900 | 0.5 | 7 | 4 | 3 | 1 | -105.292 | -2481.72 | -131.946 | -2.65336 | -62.5394 | -3.32505 | 1 | 0 | 0 |
| P345_0047_P344_FULL_DEPTH_CATALYST_REACTION_FILTER_delay_300s_H300_Q0p75 | capacity_capped | P344_FULL_DEPTH_CATALYST_REACTION_FILTER | delay_300s | 300 | 0.75 | 1 | 1 | 1 | 0 | -59.4448 | -294.053 | -59.4448 | -5.99204 | -29.6406 | -5.99204 | 0 | 0 | 0 |
| P345_0000_P344_CATALYST_CATEGORY_CONTINUATION_market_open_or_first_tick_after_announcement_H300_Q0p0 | capacity_capped | P344_CATALYST_CATEGORY_CONTINUATION | market_open_or_first_tick_after_announcement | 300 | 0 | 19 | 6 | 10 | 7 | -477.294 | -7256.53 | -6493.03 | -8.01853 | -121.91 | -109.083 | 1 | 0 | 0 |

## Gate evaluation

| gate_id | passed | observed | required |
| --- | --- | --- | --- |
| P345_PHASE344_COMPLETE | True | 1 | 1 |
| P345_EXECUTION_ALLOWED_BY_PRECOMMIT | True | 1 | 1 |
| P345_GRID_RECONCILED | True | 67/67 | all |
| P345_TRADE_ROWS_PRESENT | True | 6566 | >0 |
| P345_CAPACITY_SUMMARIES_PRESENT | True | present | present |
| P345_ACCEPTANCE_STATUS_RECORDED | True | 0 | recorded |
| P345_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM | True | closed | closed |

No promotion, paper/live acceptance, or deployable profitability claim is opened by Phase345.