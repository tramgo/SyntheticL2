# Phase358 Full-Depth Market-Neutral Fade Execution

Generated: 2026-08-11T15:23:52.073592+00:00

Phase358 executes the Phase357 precommitted full-depth family on the current local panel using Phase356 materialized scenario/trade evidence.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase358_full_depth_market_neutral_fade_execution_complete | 1 | Phase358 execution completed |
| phase358_phase357_precommit_present | 1 | Phase357 family contract present |
| phase358_primary_scenario_id | P356_CONTROL_DEPTH_2_5_FADE_VARIANT | Primary full-depth family row |
| phase358_primary_trade_rows | 12 | Primary trade rows |
| phase358_primary_diagnostic_trade_dates | 7 | Primary dates |
| phase358_primary_symbols | 9 | Primary symbols |
| phase358_primary_positive_symbols | 6 | Primary positive symbols |
| phase358_primary_positive_symbol_date_cells | 6 | Primary positive symbol/date cells |
| phase358_primary_net_pnl_inr | 1821.89 | Primary net PnL |
| phase358_primary_annualized_return_pct | 26.2352 | Primary fixed-capital annualized return |
| phase358_primary_above12 | 1 | Primary above 12% |
| phase358_primary_event_floor_met | 0 | Primary >=30 event floor |
| phase358_primary_acceptance_candidate | 0 | Primary acceptance candidate |
| phase358_guard_annualized_return_pct | 25.7443 | Depth guard annualized return |
| phase358_top5_reference_annualized_return_pct | 24.5055 | Top-five reference annualized return |
| phase358_control_rows | 4 | Control rows |
| phase358_acceptance_candidate_rows | 0 | Acceptance candidates |
| phase358_strategy_promotion_allowed | 0 | No promotion |
| phase358_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase358_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase358_next_best_action | restore_phase350_real_date_expansion_for_unseen_event_floor_no_paper_live | Recommended next milestone |

## Interpretation

| interpretation_id | value | evidence | decision |
| --- | --- | --- | --- |
| primary_positive | 1 | annualized=26.235235651058197; net=1821.8913646568187 | Full-depth family remains a positive sparse clue. |
| event_floor_failed | 1 | trade_rows=12; required=30 | No acceptance until unseen real-date expansion increases event count. |
| top5_reference_not_primary | 1 | primary=26.235235651058197; top5=24.505496732765117 | Keep depth-levels-2-5 fade as primary family. |
| paper_live_closed | 1 | promotion=0; paper_live=0; deployable_claim=0 | Research clue only. |

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
| P358_PHASE357_PRECOMMIT_PRESENT | 1 | Phase357 family contract present |
| P358_PRIMARY_FULL_DEPTH_EXECUTED | 1 | P356_CONTROL_DEPTH_2_5_FADE_VARIANT |
| P358_COST200_FIXED_CAPITAL | 1 | Inherited Phase356 cost200 fixed-capital scoring |
| P358_EVENT_FLOOR_CHECKED | 1 | event_floor_met=0 |
| P358_CONTROLS_AVAILABLE | 1 | control_rows=4 |
| P358_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM | 1 | closed |

No promotion, paper/live acceptance, or deployable profitability claim is opened.
