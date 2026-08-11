# Phase391 Interpret Phase390 Capacity Sensitivity

Generated: 2026-08-11T20:17:47.022784+00:00

| metric | value | description |
| --- | --- | --- |
| phase391_interpret_phase390_capacity_sensitivity_complete | 1 | Phase391 complete |
| phase391_best_capacity | 4 | Best capacity by selected trades |
| phase391_best_capacity_selected_trade_rows | 26 | Best selected trades |
| phase391_best_capacity_gap | 4 | Gap to event floor |
| phase391_best_annualized_return_pct_capital_adjusted | 27.6939 | Best annualized return |
| phase391_all_capacity_rows_profitable | 1 | All capacities above 12% |
| phase391_any_sensitivity_acceptance_shape | 0 | Any sensitivity row passes shape gates |
| phase391_strategy_promotion_allowed | 0 | No promotion |
| phase391_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase391_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase391_next_best_action | add_more_real_l2_days_or_precommit_event_deduplication_policy_no_paper_live | Recommended next action |

| decision_id | value | evidence | decision |
| --- | --- | --- | --- |
| P391_CAPACITY_SENSITIVITY_PROFITABLE | 1 | all capacity ladder rows remain above 12% annualized after capital adjustment | Capacity sensitivity does not kill the economics. |
| P391_CAPACITY_FLOOR_STILL_FAILS | 1 | best_capacity=4; best_selected=26; required=30 | Even capacity 4 does not reach the 30 selected-trade floor. |
| P391_NO_PROMOTION_FROM_SENSITIVITY | 1 | sensitivity_acceptance_shape rows are zero and promotion_allowed is zero | No promotion, paper/live action, or deployable profitability claim. |
