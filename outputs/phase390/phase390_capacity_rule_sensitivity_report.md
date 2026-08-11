# Phase390 Capacity Rule Sensitivity

Generated: 2026-08-11T20:16:51.216845+00:00

| metric | value | description |
| --- | --- | --- |
| phase390_capacity_rule_sensitivity_complete | 1 | Phase390 complete |
| phase390_capacity_ladder | 2;3;4 | Capacities tested |
| phase390_best_capacity | 4 | Best sensitivity capacity |
| phase390_best_selected_trade_rows | 26 | Best selected trades |
| phase390_best_annualized_return_pct_capital_adjusted | 27.6939 | Best capital-adjusted annualized return |
| phase390_best_sensitivity_acceptance_shape | 0 | Would pass shape gates as sensitivity |
| phase390_promotion_allowed | 0 | No promotion from sensitivity |
| phase390_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase390_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase390_next_best_action | interpret_phase390_capacity_sensitivity_no_paper_live | Recommended next action |

| capacity | capital_base_inr | scheduled_event_rows | capacity_selected_trade_rows | diagnostic_trade_dates | symbols | positive_symbols | positive_symbol_date_cells | net_pnl_inr | annualized_return_pct_capital_adjusted | above12 | event_floor_met | breadth_met | sensitivity_acceptance_shape | promotion_allowed | scenario_id | scenario_role | side_flip_annualized_return_pct_capital_adjusted | side_flip_selected_trade_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 250000 | 30 | 21 | 12 | 12 | 4 | 7 | 2244.12 | 18.8506 | 1 | 0 | 1 | 0 | 0 | P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | impulse_reversal_control | -87.5263 | 21 |
| 3 | 300000 | 30 | 24 | 12 | 12 | 4 | 7 | 3787.61 | 26.5132 | 1 | 0 | 1 | 0 | 0 | P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | impulse_reversal_control | -91.878 | 24 |
| 4 | 400000 | 30 | 26 | 12 | 12 | 4 | 7 | 5275.02 | 27.6939 | 1 | 0 | 1 | 0 | 0 | P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | impulse_reversal_control | -80.9804 | 26 |

| gate_id | passed | evidence |
| --- | --- | --- |
| P390_PHASE389_PRECOMMIT_PRESENT | 1 | Phase389 complete |
| P390_LADDER_EXECUTED | 1 | ladder=[2, 3, 4] |
| P390_CAPITAL_ADJUSTED_RETURNS | 1 | capital_base=max(250k, capacity*100k) |
| P390_ALPHA_COST_DEPTH_UNCHANGED | 1 | reused Phase387 raw trades |
| P390_NO_PROMOTION_PAPER_LIVE | 1 | sensitivity_only |
