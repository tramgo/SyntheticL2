# Phase453 Cross-Asset ETF Pressure Interpretation

Phase453 interprets Phase452 as an execution-access failure: sparse stride sampling was incompatible with a fixed 240-tick horizon after month filtering.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase453_cross_asset_interpretation_complete | 1 | Phase453 interpretation completed |
| phase453_thesis_id | P453_CROSS_ASSET_ETF_PRESSURE_INTERPRETATION | Interpretation thesis |
| phase453_selected_verdict | P453_CROSS_ASSET_ETF_PRESSURE_EXECUTION_ACCESS_REPAIR_REQUIRED | Selected verdict |
| phase453_cross_asset_source_closed | 0 | Source remains eligible only under repaired access contract |
| phase453_stride_contract_closed | 1 | Sparse stride/horizon contract closed |
| phase453_execution_results_generated | 0 | Interpretation only |
| phase453_strategy_promotion_allowed | 0 | No promotion |
| phase453_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase453_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase453_hard_gate_pass_rows | 7 | Passed hard gates |
| phase453_hard_gate_rows | 7 | Hard gates |
| phase453_next_best_action | precommit_phase454_contiguous_tick_window_cross_asset_etf_pressure_no_results | Recommended next action |

## Decision Ledger

| decision_id | decision_value | description | required_or_implication |
| --- | --- | --- | --- |
| selected_verdict | P453_CROSS_ASSET_ETF_PRESSURE_EXECUTION_ACCESS_REPAIR_REQUIRED | Phase452 did not produce executable trades because sparse stride conflicted with fixed tick horizon. | repair_execution_access |
| phase452_completed_round_trips | 0 | Observed Phase452 trades. | zero_is_not_strategy_edge_evidence |
| phase452_acceptance_survivor | 0 | No survivor. | 0 |
| failed_gate_ids | P452_COMPLETED_ROUND_TRIPS_GE_30;P452_DATE_BREADTH_GE_5;P452_SYMBOL_BREADTH_GE_3;P452_POSITIVE_DATE_FRACTION_GE_0_60;P452_ANNUALIZED_GE_12_COST200;P452_TIME_SHIFT_NOT_DOMINANT;P452_SIDE_FLIP_NOT_DOMINANT;P452_TARGET_ONLY_NOT_DOMINANT;P452_ETF_L1_ONLY_NOT_DOMINANT | Failed hard gates. | basis |
| cross_asset_source_closed | 0 | Source is not closed by zero-trade execution-access failure. | 0 |
| phase451_stride_contract_closed | 1 | The sparse-stride plus 240-tick-horizon access contract is closed. | 1 |
| profitability_claim_allowed | 0 | Zero-trade execution does not imply profitability. | 0 |
| paper_live_or_promotion_allowed | 0 | No paper/live or promotion. | 0 |
| next_action | precommit_phase454_contiguous_tick_window_cross_asset_etf_pressure_no_results | Repair with contiguous raw tick windows before execution. | precommit_repair_first |

## Required Repair Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| repair_source | same_cross_asset_etf_pressure_source | Not a new alpha result; repairs data-access mechanics. |
| required_change | contiguous_raw_tick_windows_per_symbol_date | Retain at least EVENT_INDEX + horizon + guard rows per date. |
| forbidden_change | no_threshold_relaxation_or_side_rule_change | No signal rescue after seeing Phase452. |
| horizon_ticks | 240 | Keep Phase451 frozen horizon. |
| entry_index | 20 | Keep Phase452 event index. |
| max_events_per_target_date | 1 | Keep low-turnover cap. |
| cost_model | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Keep cost model. |
| cost_multiplier | 2.0 | Keep cost200. |
| capital_policy | fixed_initial_capital_1000000_inr_order_notional_100000_inr_cost200 | Keep fixed capital/notional. |
| execution_results_generated_now | 0 | Phase453 interpretation only. |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P453_PHASE452_COMPLETE | True | 1 | 1 | hard |
| P453_ZERO_TRADE_BASIS_RECORDED | True | 0 | 0 | hard |
| P453_SOURCE_NOT_FALSELY_CLOSED | True | 0 | 0 | hard |
| P453_STRIDE_CONTRACT_CLOSED | True | 1 | 1 | hard |
| P453_REPAIR_CONTRACT_PRESENT | True | 10 | >=8 | hard |
| P453_NO_RESULTS_GENERATED | True | 0 | 0 | hard |
| P453_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: the cross-asset source may be retested only after a new precommit that repairs contiguous raw tick-window access without changing signal thresholds or side rules.
