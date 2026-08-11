# Phase356 Market-Context Clue Validation Execution

Generated: 2026-08-11T15:15:11.170813+00:00

Phase356 executes the Phase355 frozen clue and required controls on the current local real-L2 panel.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase356_market_context_clue_validation_execution_complete | 1 | Phase356 execution completed |
| phase356_frozen_trade_rows | 14 | Frozen validation trade rows |
| phase356_frozen_annualized_return_pct | 24.5055 | Frozen annualized return |
| phase356_frozen_net_pnl_inr | 1701.77 | Frozen net PnL |
| phase356_frozen_above12 | 1 | Frozen above 12% |
| phase356_frozen_event_floor_met | 0 | Frozen >=30 events |
| phase356_control_rows | 6 | Control scenario rows |
| phase356_control_dominates_frozen | 1 | Any control annualized return greater than frozen |
| phase356_acceptance_candidate_rows | 0 | Acceptance candidates |
| phase356_strategy_promotion_allowed | 0 | No promotion |
| phase356_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase356_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase356_next_best_action | restore_phase350_real_date_expansion_for_unseen_event_floor_no_paper_live | Recommended next milestone |

## Scenario summary

| scenario_id | control_id | scenario_role | trade_rows | diagnostic_trade_dates | symbols | positive_trade_rows | positive_symbols | positive_symbol_date_cells | net_pnl_inr | annualized_return_pct | above12 | event_floor_met | breadth_met | acceptance_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P356_CONTROL_DEPTH_2_5_GUARD_TOP5_FADE | depth_2_5_guard | full_depth_guard | 13 | 7 | 10 | 8 | 6 | 6 | 1787.8 | 25.7443 | 1 | 0 | 1 | 0 |
| P356_CONTROL_DEPTH_2_5_FADE_VARIANT | depth_2_5_fade_variant | full_depth_control | 12 | 7 | 9 | 8 | 6 | 6 | 1821.89 | 26.2352 | 1 | 0 | 1 | 0 |
| P356_FROZEN_NIFTYBEES_LB900_MARKET_NEUTRAL_TOP5_FADE | frozen_clue | frozen_validation | 14 | 7 | 11 | 8 | 6 | 6 | 1701.77 | 24.5055 | 1 | 0 | 1 | 0 |
| P356_CONTROL_NIFTYBEES_LB300_MARKET_NEUTRAL_TOP5_FADE | lookback_swap_300s | control | 13 | 7 | 10 | 8 | 6 | 6 | 1601.2 | 23.0573 | 1 | 0 | 1 | 0 |
| P356_CONTROL_BANKBEES_LB900_MARKET_NEUTRAL_TOP5_FADE | proxy_swap_bankbees | control | 13 | 7 | 9 | 7 | 5 | 5 | 1408.63 | 20.2843 | 1 | 0 | 1 | 0 |
| P356_CONTROL_DETERMINISTIC_ALTERNATE_SIDE | random_side_deterministic | control | 14 | 7 | 11 | 3 | 1 | 1 | -2194.53 | -31.6012 | 0 | 0 | 0 | 0 |
| P356_CONTROL_SIDE_FLIP | side_flip | control | 14 | 7 | 11 | 1 | 1 | 1 | -6317.83 | -90.9767 | 0 | 0 | 0 | 0 |

## Gate evaluation

| gate_id | passed | evidence |
| --- | --- | --- |
| P356_PHASE355_PRECOMMIT_PRESENT | 1 | Phase355 frozen contract present |
| P356_FROZEN_CLUE_RECONCILED | 1 | trade_rows=14 |
| P356_EVENT_FLOOR_CHECKED | 1 | event_floor_met=0 |
| P356_CONTROLS_EXECUTED | 1 | control_rows=6 |
| P356_CONTROL_DOMINANCE_RECORDED | 1 | control_dominates=1 |
| P356_COST200_FIXED_CAPITAL | 1 | 2x Zerodha cost and fixed INR 250000 |
| P356_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM | 1 | closed |

No promotion, paper/live acceptance, or deployable profitability claim is opened.
