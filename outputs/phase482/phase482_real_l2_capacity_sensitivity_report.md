# Phase482 Real-L2 Capacity Sensitivity

Phase482 executes the frozen Phase481 capacity policy grid on the already-materialized Phase401 real-L2 trade ledger. No download and no signal rebuild were performed.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase482_real_l2_capacity_sensitivity_complete | 1 | Phase482 complete if all gates pass |
| phase482_thesis_id | P482_REAL_L2_CAPACITY_SENSITIVITY | Phase482 thesis |
| phase482_capacity_policy_rows | 5 | Policies executed |
| phase482_best_feasible_policy_id | P481_MAX5_CONCURRENT | Best capital-feasible primary policy |
| phase482_best_feasible_selected_trades | 32 | Best feasible selected trades |
| phase482_best_feasible_net_pnl_inr | 4231.58 | Best feasible net PnL |
| phase482_best_feasible_annualized_return_pct | 30.4674 | Best feasible annualized return |
| phase482_best_feasible_event_floor_met | 1 | Best feasible event floor |
| phase482_best_feasible_above12 | 1 | Best feasible above 12 percent |
| phase482_best_feasible_beats_side_flip | 1 | Best feasible side-flip dominance |
| phase482_best_any_primary_policy_id | P481_ALL_READY_DIAGNOSTIC | Best primary policy including diagnostic-only |
| phase482_best_any_primary_selected_trades | 34 | Best any selected trades |
| phase482_best_any_primary_annualized_return_pct | 37.9534 | Best any annualized return |
| phase482_cost200_acceptance_candidate_rows | 1 | Capital-feasible accepted primary rows |
| phase482_strategy_promotion_allowed | 0 | No promotion |
| phase482_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase482_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase482_hard_gate_pass_rows | 8 | Passed hard gates |
| phase482_hard_gate_rows | 8 | Hard gates |
| phase482_next_best_action | interpret_phase482_capacity_sensitivity_before_any_acceptance_no_paper_live | Recommended next action |

## Scenario Summary

| capacity_policy_id | policy_role | acceptance_role | scenario_id | scenario_role | scheduled_event_rows | capacity_selected_trade_rows | diagnostic_trade_dates | symbols | positive_trade_rows | positive_symbols | positive_symbol_date_cells | net_pnl_inr | annualized_return_pct | above12 | event_floor_met | breadth_met | capital_feasible | beats_side_flip_control | acceptance_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P481_BASELINE_MAX3_CONCURRENT | baseline | primary | P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | impulse_reversal_control | 34 | 28 | 14 | 12 | 12 | 3 | 7 | 2536.45 | 18.2625 | 1 | 0 | 1 | 1 | 1 | 0 |
| P481_BASELINE_MAX3_CONCURRENT | baseline | primary | P362_D120_I2p5_D0p25_R0p0_CONTINUATION | impulse_continuation | 34 | 28 | 14 | 12 | 4 | 1 | 4 | -13432.6 | -96.7144 | 0 | 0 | 0 | 1 | 0 | 0 |
| P481_MAX5_CONCURRENT | looser_capacity | sensitivity | P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | impulse_reversal_control | 34 | 32 | 14 | 12 | 14 | 3 | 7 | 4231.58 | 30.4674 | 1 | 1 | 1 | 1 | 1 | 1 |
| P481_MAX5_CONCURRENT | looser_capacity | sensitivity | P362_D120_I2p5_D0p25_R0p0_CONTINUATION | impulse_continuation | 34 | 32 | 14 | 12 | 5 | 2 | 5 | -16742.5 | -120.546 | 0 | 1 | 1 | 1 | 0 | 0 |
| P481_ONE_PER_SYMBOL_DATE | breadth_first | sensitivity | P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | impulse_reversal_control | 34 | 23 | 14 | 14 | 8 | 4 | 8 | -1308.08 | -9.41816 | 0 | 0 | 1 | 1 | 1 | 0 |
| P481_ONE_PER_SYMBOL_DATE | breadth_first | sensitivity | P362_D120_I2p5_D0p25_R0p0_CONTINUATION | impulse_continuation | 34 | 23 | 14 | 14 | 5 | 2 | 5 | -7621.91 | -54.8777 | 0 | 0 | 1 | 1 | 0 | 0 |
| P481_TWO_PER_TRADE_DATE | date_balanced | sensitivity | P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | impulse_reversal_control | 34 | 23 | 14 | 12 | 8 | 3 | 5 | 438.576 | 3.15775 | 0 | 0 | 1 | 1 | 1 | 0 |
| P481_TWO_PER_TRADE_DATE | date_balanced | sensitivity | P362_D120_I2p5_D0p25_R0p0_CONTINUATION | impulse_continuation | 34 | 23 | 14 | 12 | 4 | 1 | 4 | -9399.76 | -67.6783 | 0 | 0 | 0 | 1 | 0 | 0 |
| P481_ALL_READY_DIAGNOSTIC | upper_bound_diagnostic | diagnostic_only | P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | impulse_reversal_control | 34 | 34 | 14 | 14 | 15 | 4 | 8 | 5271.31 | 37.9534 | 1 | 1 | 1 | 0 | 1 | 0 |
| P481_ALL_READY_DIAGNOSTIC | upper_bound_diagnostic | diagnostic_only | P362_D120_I2p5_D0p25_R0p0_CONTINUATION | impulse_continuation | 34 | 34 | 14 | 14 | 5 | 2 | 5 | -18543 | -133.51 | 0 | 1 | 1 | 0 | 0 | 0 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P482_PHASE481_PRECOMMIT_USED | True | 1 | 1 | hard |
| P482_POLICY_GRID_MATCHES_PRECOMMIT | True | 5 | 5 | hard |
| P482_NO_DOWNLOAD_USED | True | reused_phase401_trade_ledger | no_download | hard |
| P482_COST200_RETAINED | True | 1 | 1 | hard |
| P482_EVENT_FLOOR_EVALUATED | True | 1 | evaluated | hard |
| P482_ALL_READY_DIAGNOSTIC_NOT_ACCEPTANCE | True | diagnostic_only | diagnostic_only | hard |
| P482_ACCEPTANCE_CANDIDATE_EVALUATED | True | 1 | >=0 | hard |
| P482_NO_PROMOTION_PAPER_LIVE_OR_CLAIM | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: all-ready policy is diagnostic-only; no paper/live, no promotion, no deployable profitability claim.
