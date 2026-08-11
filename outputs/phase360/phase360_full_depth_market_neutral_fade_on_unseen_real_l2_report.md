# Phase360 Full-Depth Market-Neutral Fade on Unseen Real L2

Generated: 2026-08-11T15:33:15.232712+00:00

Phase360 executes the Phase357/358 full-depth market-neutral fade family on the Phase359 unseen official-catalyst real L2 work order. It uses NIFTYBEES 900-second market-neutral context, top-five and depth-levels-2-5 filters, depth-levels-2-5 fade side selection, Zerodha cost200 fixed-capital scoring, and deterministic controls. It opens no promotion, paper/live acceptance, or deployable profitability claim.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase360_full_depth_market_neutral_fade_unseen_execution_complete | 1 | Phase360 execution completed |
| phase360_phase359_work_order_rows | 25 | Phase359 work-order rows |
| phase360_filled_event_rows | 25 | Filled raw L2 event rows |
| phase360_primary_eligible_event_rows | 11 | Rows passing market-neutral, top-five and depth 2-5 filters |
| phase360_primary_capacity_selected_trade_rows | 5 | Primary capacity-selected rows |
| phase360_primary_diagnostic_trade_dates | 2 | Primary dates |
| phase360_primary_symbols | 4 | Primary symbols |
| phase360_primary_positive_symbols | 2 | Primary positive symbols |
| phase360_primary_positive_symbol_date_cells | 2 | Primary positive symbol/date cells |
| phase360_primary_net_pnl_inr | -939.536 | Primary net PnL |
| phase360_primary_annualized_return_pct | -47.3526 | Primary annualized return |
| phase360_primary_above12 | 0 | Primary above 12% |
| phase360_primary_event_floor_met | 0 | Primary >=30 event floor |
| phase360_acceptance_candidate_rows | 0 | Acceptance candidates |
| phase360_strategy_promotion_allowed | 0 | No promotion |
| phase360_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase360_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase360_hard_gate_pass_rows | 8 | Passed hard gates |
| phase360_hard_gate_rows | 8 | Hard gates |
| phase360_next_best_action | interpret_phase360_and_decide_expand_or_close_no_paper_live | Recommended next milestone |

## Scenario summary

| scenario_id | scenario_role | scheduled_event_rows | capacity_selected_trade_rows | diagnostic_trade_dates | symbols | positive_trade_rows | positive_symbols | positive_symbol_date_cells | net_pnl_inr | annualized_return_pct | above12 | event_floor_met | breadth_met | acceptance_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P360_UNSEEN_P357_FULL_DEPTH_MARKET_NEUTRAL_DEPTH_2_5_FADE | primary_full_depth_depth_2_5_fade | 11 | 5 | 2 | 4 | 3 | 2 | 2 | -939.536 | -47.3526 | 0 | 0 | 1 | 0 |
| P360_UNSEEN_TOP5_REFERENCE_MARKET_NEUTRAL_FADE | top5_reference | 11 | 5 | 2 | 4 | 3 | 2 | 2 | -939.536 | -47.3526 | 0 | 0 | 1 | 0 |
| P360_UNSEEN_SIDE_FLIP_CONTROL | side_flip_control | 11 | 5 | 2 | 4 | 2 | 2 | 2 | -696.636 | -35.1105 | 0 | 0 | 1 | 0 |
| P360_UNSEEN_DETERMINISTIC_ALTERNATE_SIDE_CONTROL | deterministic_alternate_side_control | 11 | 5 | 2 | 4 | 2 | 1 | 1 | -939.636 | -47.3577 | 0 | 0 | 0 | 0 |

## Gate evaluation

| gate_id | passed | evidence |
| --- | --- | --- |
| P360_PHASE359_COMPLETE | 1 | Phase359 complete |
| P360_WORK_ORDER_PRESENT | 1 | work_rows=25 |
| P360_FILLED_EVENTS_PRESENT | 1 | filled=25 |
| P360_FULL_DEPTH_FILTER_APPLIED | 1 | eligible_primary=11 |
| P360_COST200_FIXED_CAPITAL | 1 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 |
| P360_EVENT_FLOOR_CHECKED | 1 | event_floor_met=0 |
| P360_CONTROLS_EXECUTED | 1 | scenario_rows=4 |
| P360_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM | 1 | closed |

No promotion, paper/live acceptance, or deployable profitability claim is opened.
