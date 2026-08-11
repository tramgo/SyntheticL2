# Phase354 Real-Catalyst Market-Context L2 Diagnostic

Generated: 2026-08-11T15:08:44.436580+00:00

Phase354 tests a structural real-data thesis: official-catalyst trades require entry-time full-depth state plus NIFTYBEES/BANKBEES market-proxy context, rather than raw catalyst or raw imbalance alone.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase354_real_catalyst_market_context_diagnostic_complete | 1 | Phase354 diagnostic completed |
| phase354_enriched_event_rows | 392 | Proxy-enriched event rows |
| phase354_scenario_rows | 48 | Scenario rows evaluated |
| phase354_trade_rows | 606 | Trade rows evaluated |
| phase354_above12_rows | 4 | Above-12 rows |
| phase354_acceptance_candidate_rows | 0 | Acceptance candidates |
| phase354_best_scenario_id | P354_capacity_selected_events_NIFTYBEES_LB900_market_neutral_top5_fade | Best scenario |
| phase354_best_annualized_return_pct | 24.5055 | Best annualized return |
| phase354_best_net_pnl_inr | 1701.77 | Best net PnL |
| phase354_strategy_promotion_allowed | 0 | No promotion |
| phase354_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase354_deployable_profitability_claim_allowed | 0 | No profitability claim |
| phase354_next_best_action | restore_phase350_real_date_expansion_or_precommit_non_directional_liquidity_forecast_no_paper_live | Recommended next milestone |

## Top scenarios

| scenario_id | scope | proxy_symbol | lookback_seconds | rule_id | trade_rows | diagnostic_trade_dates | symbols | positive_trade_rows | positive_symbols | positive_symbol_date_cells | net_pnl_inr | annualized_return_pct | above12 | event_floor_met | breadth_met | acceptance_candidate | uses_real_l2 | uses_market_proxy_l2 | uses_official_catalyst_events | uses_full_depth_1_5 | uses_depth_2_5 | l1_only_variant |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P354_capacity_selected_events_NIFTYBEES_LB900_market_neutral_top5_fade | capacity_selected_events | NIFTYBEES | 900 | market_neutral_top5_fade | 14 | 7 | 11 | 8 | 6 | 6 | 1701.77 | 24.5055 | 1 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 0 | 0 |
| P354_capacity_selected_events_NIFTYBEES_LB300_market_neutral_top5_fade | capacity_selected_events | NIFTYBEES | 300 | market_neutral_top5_fade | 13 | 7 | 10 | 8 | 6 | 6 | 1601.2 | 23.0573 | 1 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 0 | 0 |
| P354_capacity_selected_events_BANKBEES_LB300_market_neutral_top5_fade | capacity_selected_events | BANKBEES | 300 | market_neutral_top5_fade | 13 | 7 | 9 | 7 | 5 | 5 | 1570.02 | 22.6083 | 1 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 0 | 0 |
| P354_capacity_selected_events_BANKBEES_LB900_market_neutral_top5_fade | capacity_selected_events | BANKBEES | 900 | market_neutral_top5_fade | 13 | 7 | 9 | 7 | 5 | 5 | 1408.63 | 20.2843 | 1 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 0 | 0 |
| P354_lead_catalyst_categories_NIFTYBEES_LB900_market_stretched_deep_fade | lead_catalyst_categories | NIFTYBEES | 900 | market_stretched_deep_fade | 2 | 2 | 2 | 1 | 1 | 1 | -18.9804 | -0.956613 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 |
| P354_lead_catalyst_categories_BANKBEES_LB300_market_stretched_deep_fade | lead_catalyst_categories | BANKBEES | 300 | market_stretched_deep_fade | 2 | 2 | 2 | 1 | 1 | 1 | -18.9804 | -0.956613 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 |
| P354_lead_catalyst_categories_BANKBEES_LB900_market_stretched_deep_fade | lead_catalyst_categories | BANKBEES | 900 | market_stretched_deep_fade | 2 | 2 | 2 | 1 | 1 | 1 | -18.9804 | -0.956613 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 |
| P354_all_official_catalyst_events_BANKBEES_LB300_market_stretched_deep_fade | all_official_catalyst_events | BANKBEES | 300 | market_stretched_deep_fade | 3 | 2 | 3 | 1 | 1 | 1 | -106.146 | -5.34977 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 |
| P354_capacity_selected_events_BANKBEES_LB300_market_stretched_deep_fade | capacity_selected_events | BANKBEES | 300 | market_stretched_deep_fade | 3 | 2 | 3 | 1 | 1 | 1 | -106.146 | -5.34977 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 |
| P354_all_official_catalyst_events_BANKBEES_LB900_market_stretched_deep_fade | all_official_catalyst_events | BANKBEES | 900 | market_stretched_deep_fade | 3 | 3 | 3 | 1 | 1 | 1 | -196.396 | -6.59889 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 |
| P354_capacity_selected_events_BANKBEES_LB900_market_stretched_deep_fade | capacity_selected_events | BANKBEES | 900 | market_stretched_deep_fade | 3 | 3 | 3 | 1 | 1 | 1 | -196.396 | -6.59889 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 |
| P354_lead_catalyst_categories_NIFTYBEES_LB300_market_stretched_deep_fade | lead_catalyst_categories | NIFTYBEES | 300 | market_stretched_deep_fade | 3 | 3 | 3 | 1 | 1 | 1 | -270.113 | -9.07581 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 |
| P354_all_official_catalyst_events_NIFTYBEES_LB900_market_stretched_deep_fade | all_official_catalyst_events | NIFTYBEES | 900 | market_stretched_deep_fade | 4 | 3 | 4 | 1 | 1 | 1 | -283.561 | -9.52766 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 |
| P354_capacity_selected_events_NIFTYBEES_LB900_market_stretched_deep_fade | capacity_selected_events | NIFTYBEES | 900 | market_stretched_deep_fade | 4 | 3 | 4 | 1 | 1 | 1 | -283.561 | -9.52766 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 |
| P354_all_official_catalyst_events_NIFTYBEES_LB300_market_stretched_deep_fade | all_official_catalyst_events | NIFTYBEES | 300 | market_stretched_deep_fade | 4 | 3 | 4 | 1 | 1 | 1 | -357.279 | -12.0046 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 |
| P354_capacity_selected_events_NIFTYBEES_LB300_market_stretched_deep_fade | capacity_selected_events | NIFTYBEES | 300 | market_stretched_deep_fade | 4 | 3 | 4 | 1 | 1 | 1 | -357.279 | -12.0046 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 |
| P354_lead_catalyst_categories_NIFTYBEES_LB900_market_confirmed_top5_follow | lead_catalyst_categories | NIFTYBEES | 900 | market_confirmed_top5_follow | 5 | 3 | 4 | 1 | 1 | 1 | -728.528 | -24.4785 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 0 |
| P354_lead_catalyst_categories_BANKBEES_LB900_market_confirmed_top5_follow | lead_catalyst_categories | BANKBEES | 900 | market_confirmed_top5_follow | 4 | 4 | 2 | 0 | 0 | 0 | -1017.38 | -25.6379 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 0 |
| P354_lead_catalyst_categories_BANKBEES_LB300_market_confirmed_deep_follow | lead_catalyst_categories | BANKBEES | 300 | market_confirmed_deep_follow | 4 | 4 | 3 | 0 | 0 | 0 | -1050.42 | -26.4707 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 |
| P354_all_official_catalyst_events_BANKBEES_LB900_market_confirmed_top5_follow | all_official_catalyst_events | BANKBEES | 900 | market_confirmed_top5_follow | 6 | 5 | 4 | 0 | 0 | 0 | -1413.76 | -28.5014 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 0 |

## Gate evaluation

| gate_id | passed | evidence |
| --- | --- | --- |
| P354_PHASE342_LEDGER_PRESENT | 1 | filled_rows=98 |
| P354_MARKET_PROXY_L2_PRESENT | 1 | NIFTYBEES/BANKBEES proxy context joined |
| P354_REAL_L2_AND_OFFICIAL_CATALYST_USED | 1 | Phase342 real L2 plus official catalyst lineage |
| P354_MARKET_CONTEXT_RULES_EVALUATED | 1 | scenario_rows=48 |
| P354_L1_ONLY_FORBIDDEN | 1 | No L1-only variants |
| P354_COST200_FIXED_CAPITAL | 1 | 2x Zerodha cost and fixed INR 250000 annualization |
| P354_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM | 1 | closed |

No promotion, paper/live acceptance, or deployable profitability claim is opened.
