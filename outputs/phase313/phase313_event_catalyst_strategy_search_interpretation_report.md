# Phase313 Event-Catalyst Strategy Search Interpretation

Phase313 interprets Phase312 training-only results. It does not replay, promote, or claim deployable profitability.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase313_interpretation_complete | 1 | Phase313 event-catalyst strategy-search interpretation completed |
| phase313_positive_sparse_leads_exist | 1 | Sparse positive training leads exist |
| phase313_cost_stress_sparse_leads_exist | 1 | 2x-cost sparse training leads exist |
| phase313_insufficient_event_breadth_for_acceptance | 1 | Event breadth insufficient for acceptance |
| phase313_insufficient_trade_breadth_for_acceptance | 1 | Trade breadth insufficient for acceptance |
| phase313_replay_allowed | 0 | No replay |
| phase313_strategy_promotion_allowed | 0 | No promotion |
| phase313_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase313_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase313_selected_next_route | P314_EVENT_CATALYST_MULTIEVENT_SYNTHETIC_BREADTH_PRECOMMIT | Selected next route |
| phase313_hard_gate_pass_rows | 5 | Passed hard gates |
| phase313_hard_gate_rows | 5 | Hard gates |
| phase313_next_best_action | run_phase314_event_catalyst_multievent_synthetic_breadth_precommit_no_replay | Recommended next action |

## Family interpretation

| family_id | scenario_rows | positive_net_pnl_rows | sparse_above12_rows | best_net_pnl_inr | median_net_pnl_inr | best_sparse_annualized_pct | median_sparse_annualized_pct | max_scheduled_trades | positive_net_pnl_fraction | sparse_above12_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pre_event_trend_reversal | 1296 | 1050 | 768 | 3074.38 | 216.009 | 187.915 | 23.8455 | 4 | 0.810185 | 0.592593 |
| pre_event_pressure_shift_reversal | 1296 | 720 | 561 | 1941.12 | 48.0961 | 215.856 | 5.20096 | 4 | 0.555556 | 0.43287 |
| event_depth_pressure_reversal | 1296 | 573 | 399 | 928.921 | -51.7609 | 103.835 | -4.62671 | 4 | 0.44213 | 0.30787 |
| microprice_dislocation_reversal | 1296 | 453 | 291 | 1420.92 | -82.7299 | 149.319 | -9.23678 | 4 | 0.349537 | 0.224537 |
| microprice_dislocation_continuation | 1296 | 540 | 252 | 1143.88 | -86.0334 | 66.3362 | -7.65235 | 4 | 0.416667 | 0.194444 |
| pre_event_pressure_shift_continuation | 1296 | 168 | 60 | 317.631 | -291.905 | 33.8007 | -29.0452 | 4 | 0.12963 | 0.0462963 |
| event_depth_pressure_continuation | 1296 | 237 | 54 | 102.841 | -153.61 | 25.9158 | -15.8394 | 4 | 0.18287 | 0.0416667 |
| pre_event_trend_continuation | 1296 | 0 | 0 | -26.3203 | -463.323 | -1.32654 | -51.5836 | 4 | 0 | 0 |

## Cost stress interpretation

| cost_profile | scenario_rows | positive_net_pnl_rows | sparse_above12_rows | best_net_pnl_inr | best_sparse_annualized_pct | positive_net_pnl_fraction |
| --- | --- | --- | --- | --- | --- | --- |
| zerodha_2x_all_in_cost_proxy | 2592 | 780 | 495 | 2743.53 | 195.012 | 0.300926 |
| zerodha_base | 2592 | 1038 | 669 | 3074.38 | 215.856 | 0.400463 |
| zerodha_plus_1bp_slippage | 2592 | 984 | 624 | 2994.04 | 210.792 | 0.37963 |
| zerodha_plus_2bp_slippage | 2592 | 939 | 597 | 2913.7 | 205.729 | 0.362269 |

## Decision ledger

| decision_id | decision_value | evidence | interpretation |
| --- | --- | --- | --- |
| phase312_positive_sparse_leads_exist | 1 | sparse_above12_rows=2385 | Useful training clue exists. |
| best_cluster_family | pre_event_pressure_shift_reversal | P312_pre_event_pressure_shift_reversal_H900_all_nonzero_signal_N100000_C2_zerodha_base_CAP100000 | Best sparse annualized scenario family. |
| cost_stress_sparse_leads_exist | 1 | 2x_cost_sparse_above12_rows=495 | Checks whether any clue survives 2x all-in-cost proxy. |
| insufficient_event_breadth_for_acceptance | 1 | observed_trade_dates=1 | One synthetic event date is not acceptance breadth. |
| insufficient_trade_breadth_for_acceptance | 1 | best_scheduled_trades=1 | Best scenario is too sparse for robust portfolio claim. |
| replay_or_promotion_allowed | 0 | closed | No replay/promotion from Phase313. |
| deployable_profitability_claim_allowed | 0 | closed | No deployable claim from one-event synthetic evidence. |
| selected_next_route | P314_EVENT_CATALYST_MULTIEVENT_SYNTHETIC_BREADTH_PRECOMMIT | run_phase314_event_catalyst_multievent_synthetic_breadth_precommit_no_replay | Build more synthetic event breadth before broader search/replay. |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P313_PHASE312_COMPLETE | True | 1 | 1 | hard |
| P313_INTERPRETATION_ROWS_PRESENT | True | 8 | >=8 | hard |
| P313_PROFITABILITY_CLAIM_CLOSED | True | 0 | 0 | hard |
| P313_NEXT_ROUTE_SELECTED | True | P314_EVENT_CATALYST_MULTIEVENT_SYNTHETIC_BREADTH_PRECOMMIT | selected | hard |
| P313_NO_REPLAY_PROMOTION_OR_PAPER_LIVE | True | replay=0;promotion=0;paper=0 | all_zero | hard |
