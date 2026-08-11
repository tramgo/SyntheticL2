# Phase353 Real-Catalyst L2 Side-Selection Diagnostic

Generated: 2026-08-11T15:05:05.132674+00:00

Phase353 tests a materially different real-data lever: selecting long/short direction from entry top-five and depth-levels-2-5 imbalance on official-catalyst real L2 events, instead of inheriting the prior long-only survivor direction.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase353_real_catalyst_l2_side_selection_complete | 1 | Phase353 diagnostic completed |
| phase353_phase342_filled_input_rows | 98 | Filled Phase342 rows used |
| phase353_scenario_rows | 18 | Scenario rows evaluated |
| phase353_trade_rows | 1174 | Trade rows evaluated |
| phase353_above12_rows | 0 | Above-12 rows |
| phase353_acceptance_candidate_rows | 0 | Acceptance candidates |
| phase353_best_scenario_id | P353_capacity_selected_events_fade_top5 | Best scenario |
| phase353_best_annualized_return_pct | -11.4594 | Best annualized return |
| phase353_best_net_pnl_inr | -795.793 | Best net PnL |
| phase353_strategy_promotion_allowed | 0 | No promotion |
| phase353_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase353_deployable_profitability_claim_allowed | 0 | No profitability claim |
| phase353_next_best_action | restore_phase350_real_date_expansion_or_precommit_material_new_thesis_no_paper_live | Recommended next milestone |

## Top scenarios

| scenario_id | scope | rule_id | rule_description | trade_rows | diagnostic_trade_dates | symbols | positive_trade_rows | positive_symbol_date_cells | positive_symbols | net_pnl_inr | annualized_return_pct | above12 | event_floor_met | breadth_met | acceptance_candidate | cost_model_version | cost_profile | initial_capital_inr | uses_real_l2 | uses_official_catalyst_events | uses_full_depth_1_5 | l1_only_variant |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P353_capacity_selected_events_fade_top5 | capacity_selected_events | fade_top5 | Fade top-five quantity imbalance. | 37 | 7 | 16 | 13 | 10 | 9 | -795.793 | -11.4594 | 0 | 1 | 1 | 0 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | zerodha_2x_all_in_cost_proxy | 250000 | 1 | 1 | 1 | 0 |
| P353_capacity_selected_events_fade_l2_l5 | capacity_selected_events | fade_l2_l5 | Fade depth-levels-2-5 quantity imbalance. | 37 | 7 | 16 | 11 | 8 | 7 | -2417.69 | -34.8148 | 0 | 1 | 1 | 0 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | zerodha_2x_all_in_cost_proxy | 250000 | 1 | 1 | 1 | 0 |
| P353_capacity_selected_events_fade_order | capacity_selected_events | fade_order | Fade top-five order-count imbalance. | 37 | 7 | 16 | 10 | 7 | 6 | -3678.49 | -52.9703 | 0 | 1 | 1 | 0 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | zerodha_2x_all_in_cost_proxy | 250000 | 1 | 1 | 1 | 0 |
| P353_lead_catalyst_categories_fade_order | lead_catalyst_categories | fade_order | Fade top-five order-count imbalance. | 62 | 7 | 18 | 19 | 9 | 6 | -7489.08 | -107.843 | 0 | 1 | 1 | 0 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | zerodha_2x_all_in_cost_proxy | 250000 | 1 | 1 | 1 | 0 |
| P353_lead_catalyst_categories_fade_top5 | lead_catalyst_categories | fade_top5 | Fade top-five quantity imbalance. | 63 | 7 | 19 | 22 | 13 | 8 | -7672.42 | -110.483 | 0 | 1 | 1 | 0 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | zerodha_2x_all_in_cost_proxy | 250000 | 1 | 1 | 1 | 0 |
| P353_capacity_selected_events_follow_order | capacity_selected_events | follow_order | Follow top-five order-count imbalance. | 37 | 7 | 16 | 7 | 6 | 3 | -8499.69 | -122.396 | 0 | 1 | 1 | 0 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | zerodha_2x_all_in_cost_proxy | 250000 | 1 | 1 | 1 | 0 |
| P353_lead_catalyst_categories_fade_l2_l5 | lead_catalyst_categories | fade_l2_l5 | Fade depth-levels-2-5 quantity imbalance. | 63 | 7 | 19 | 21 | 12 | 7 | -8515.22 | -122.619 | 0 | 1 | 1 | 0 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | zerodha_2x_all_in_cost_proxy | 250000 | 1 | 1 | 1 | 0 |
| P353_capacity_selected_events_follow_l2_l5 | capacity_selected_events | follow_l2_l5 | Follow depth-levels-2-5 quantity imbalance. | 37 | 7 | 16 | 6 | 5 | 3 | -9760.49 | -140.551 | 0 | 1 | 1 | 0 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | zerodha_2x_all_in_cost_proxy | 250000 | 1 | 1 | 1 | 0 |
| P353_capacity_selected_events_follow_top5 | capacity_selected_events | follow_top5 | Follow top-five quantity imbalance. | 37 | 7 | 16 | 4 | 3 | 2 | -11382.4 | -163.906 | 0 | 1 | 1 | 0 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | zerodha_2x_all_in_cost_proxy | 250000 | 1 | 1 | 1 | 0 |
| P353_all_official_catalyst_events_fade_order | all_official_catalyst_events | fade_order | Fade top-five order-count imbalance. | 92 | 7 | 21 | 26 | 13 | 7 | -12221.7 | -175.993 | 0 | 1 | 1 | 0 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | zerodha_2x_all_in_cost_proxy | 250000 | 1 | 1 | 1 | 0 |
| P353_lead_catalyst_categories_follow_l2_l5 | lead_catalyst_categories | follow_l2_l5 | Follow depth-levels-2-5 quantity imbalance. | 63 | 7 | 19 | 16 | 11 | 8 | -12247.4 | -176.363 | 0 | 1 | 1 | 0 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | zerodha_2x_all_in_cost_proxy | 250000 | 1 | 1 | 1 | 0 |
| P353_lead_catalyst_categories_follow_order | lead_catalyst_categories | follow_order | Follow top-five order-count imbalance. | 62 | 7 | 18 | 17 | 13 | 7 | -12942.7 | -186.375 | 0 | 1 | 1 | 0 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | zerodha_2x_all_in_cost_proxy | 250000 | 1 | 1 | 1 | 0 |
| P353_lead_catalyst_categories_follow_top5 | lead_catalyst_categories | follow_top5 | Follow top-five quantity imbalance. | 63 | 7 | 19 | 15 | 10 | 7 | -13090.2 | -188.499 | 0 | 1 | 1 | 0 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | zerodha_2x_all_in_cost_proxy | 250000 | 1 | 1 | 1 | 0 |
| P353_all_official_catalyst_events_follow_l2_l5 | all_official_catalyst_events | follow_l2_l5 | Follow depth-levels-2-5 quantity imbalance. | 98 | 7 | 23 | 28 | 18 | 8 | -14275.2 | -205.563 | 0 | 1 | 1 | 0 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | zerodha_2x_all_in_cost_proxy | 250000 | 1 | 1 | 1 | 0 |
| P353_all_official_catalyst_events_follow_top5 | all_official_catalyst_events | follow_top5 | Follow top-five quantity imbalance. | 98 | 7 | 23 | 26 | 16 | 8 | -15673.1 | -225.692 | 0 | 1 | 1 | 0 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | zerodha_2x_all_in_cost_proxy | 250000 | 1 | 1 | 1 | 0 |
| P353_all_official_catalyst_events_fade_top5 | all_official_catalyst_events | fade_top5 | Fade top-five quantity imbalance. | 98 | 7 | 23 | 33 | 21 | 9 | -16613.6 | -239.236 | 0 | 1 | 1 | 0 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | zerodha_2x_all_in_cost_proxy | 250000 | 1 | 1 | 1 | 0 |
| P353_all_official_catalyst_events_fade_l2_l5 | all_official_catalyst_events | fade_l2_l5 | Fade depth-levels-2-5 quantity imbalance. | 98 | 7 | 23 | 31 | 19 | 10 | -18011.5 | -259.366 | 0 | 1 | 1 | 0 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | zerodha_2x_all_in_cost_proxy | 250000 | 1 | 1 | 1 | 0 |
| P353_all_official_catalyst_events_follow_order | all_official_catalyst_events | follow_order | Follow top-five order-count imbalance. | 92 | 7 | 21 | 27 | 19 | 8 | -18081.3 | -260.371 | 0 | 1 | 1 | 0 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | zerodha_2x_all_in_cost_proxy | 250000 | 1 | 1 | 1 | 0 |

## Gate evaluation

| gate_id | passed | evidence |
| --- | --- | --- |
| P353_PHASE342_LEDGER_PRESENT | 1 | filled_rows=98 |
| P353_REAL_L2_USED | 1 | Phase342 real L2 diagnostic ledger |
| P353_OFFICIAL_CATALYST_USED | 1 | Phase340/342 official catalyst work order lineage |
| P353_FULL_DEPTH_SIDE_RULES_PRESENT | 1 | top-five and depth-levels-2-5 rules evaluated |
| P353_L1_ONLY_FORBIDDEN | 1 | No L1-only variants |
| P353_COST200_FIXED_CAPITAL | 1 | 2x Zerodha cost and fixed INR 250000 annualization |
| P353_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM | 1 | closed |

No promotion, paper/live acceptance, or deployable profitability claim is opened.
