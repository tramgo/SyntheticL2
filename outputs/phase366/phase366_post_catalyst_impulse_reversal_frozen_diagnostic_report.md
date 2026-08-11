# Phase366 Post-Catalyst Impulse Reversal Frozen Diagnostic

Generated: 2026-08-11T16:02:52.015701+00:00

Phase366 executes the Phase365 frozen reversal thesis by extracting the exact primary and registered controls from Phase363. It performs no parameter search and opens no promotion, paper/live acceptance, or deployable profitability claim.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase366_post_catalyst_impulse_reversal_frozen_diagnostic_complete | 1 | Phase366 completed |
| phase366_primary_scenario_id | P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | Frozen primary |
| phase366_primary_trade_rows | 12 | Primary selected trades |
| phase366_primary_dates | 8 | Primary dates |
| phase366_primary_symbols | 7 | Primary symbols |
| phase366_primary_positive_symbols | 3 | Primary positive symbols |
| phase366_primary_net_pnl_inr | 3106.73 | Primary net PnL |
| phase366_primary_annualized_return_pct | 39.1448 | Primary annualized return |
| phase366_primary_above12 | 1 | Primary above 12% |
| phase366_primary_event_floor_met | 0 | Primary event floor |
| phase366_acceptance_candidate_rows | 0 | Acceptance candidates |
| phase366_side_flip_annualized_return_pct | -99.1323 | Side flip annualized return |
| phase366_strict_replenishment_annualized_return_pct | -3.64241 | Strict replenishment annualized return |
| phase366_weaker_depth_annualized_return_pct | 30.8419 | Weaker depth annualized return |
| phase366_shorter_delay_annualized_return_pct | 18.0597 | Shorter delay annualized return |
| phase366_strategy_promotion_allowed | 0 | No promotion |
| phase366_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase366_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase366_hard_gate_pass_rows | 7 | Passed hard gates |
| phase366_hard_gate_rows | 7 | Hard gates |
| phase366_next_best_action | interpret_phase366_or_expand_real_dates_for_reversal_falsification_no_paper_live | Recommended next milestone |

## Frozen scenario/control summary

| scenario_id | scenario_role | scheduled_event_rows | capacity_selected_trade_rows | diagnostic_trade_dates | symbols | positive_trade_rows | positive_symbols | positive_symbol_date_cells | net_pnl_inr | annualized_return_pct | above12 | event_floor_met | breadth_met | acceptance_candidate | phase366_role | control_id | source_scenario_id | present |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | impulse_reversal_control | 16 | 12 | 8 | 7 | 6 | 3 | 4 | 3106.73 | 39.1448 | 1 | 0 | 1 | 0 | primary_frozen_reversal | primary | P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | 1 |
| P362_D120_I2p5_D0p25_R0p0_CONTINUATION | impulse_continuation | 16 | 12 | 8 | 7 | 2 | 1 | 2 | -7867.64 | -99.1323 | 0 | 0 | 0 | 0 | side_flip_continuation | side_flip | P362_D120_I2p5_D0p25_R0p0_CONTINUATION | 1 |
| P362_D120_I2p5_D0p25_R0p1_REVERSAL_CONTROL | impulse_reversal_control | 9 | 9 | 8 | 7 | 3 | 2 | 3 | -289.08 | -3.64241 | 0 | 0 | 1 | 0 | stricter_replenishment | stricter_replenishment | P362_D120_I2p5_D0p25_R0p1_REVERSAL_CONTROL | 1 |
| P362_D120_I2p5_D0p15_R0p0_REVERSAL_CONTROL | impulse_reversal_control | 23 | 16 | 8 | 9 | 7 | 4 | 5 | 2447.77 | 30.8419 | 1 | 0 | 1 | 0 | weaker_depth | weaker_depth | P362_D120_I2p5_D0p15_R0p0_REVERSAL_CONTROL | 1 |
| P362_D60_I2p5_D0p25_R0p0_REVERSAL_CONTROL | impulse_reversal_control | 16 | 10 | 6 | 8 | 5 | 3 | 5 | 1074.99 | 18.0597 | 1 | 0 | 1 | 0 | shorter_delay | shorter_delay | P362_D60_I2p5_D0p25_R0p0_REVERSAL_CONTROL | 1 |

## Interpretation

| interpretation_id | value | evidence | decision |
| --- | --- | --- | --- |
| primary_positive_sparse | 1 | ann=39.144819884564285; trades=12 | Primary remains a positive sparse clue, not acceptance. |
| side_flip_negative_control_pass | 1 | primary=39.144819884564285; side_flip=-99.13225678941524 | Reversal dominates same-filter continuation side flip. |
| strict_replenishment_fragility | 1 | strict_replenishment_ann=-3.6424119335008 | Clue weakens under stricter replenishment, so robustness is not established. |
| acceptance_closed | 1 | event_floor=0; acceptance=0 | No promotion, paper/live acceptance or deployable profitability claim. |

## Gate evaluation

| gate_id | passed | evidence |
| --- | --- | --- |
| P366_PHASE365_PRECOMMIT_PRESENT | 1 | Phase365 precommit complete |
| P366_PRIMARY_FROZEN_ROW_PRESENT | 1 | P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL |
| P366_REGISTERED_CONTROLS_PRESENT | 1 | present=5/5 |
| P366_FULL_DEPTH_COST200_INHERITED | 1 | Inherited from Phase363 full-depth cost200 diagnostic |
| P366_EVENT_FLOOR_CHECKED | 1 | event_floor_met=0 |
| P366_NO_SEARCH_OR_PARAMETER_EXPANSION | 1 | frozen extraction only |
| P366_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM | 1 | closed |

No promotion, paper/live acceptance, or deployable profitability claim is opened.
