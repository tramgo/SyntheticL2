# Phase404 Liquidity-Vacuum Continuation Precommit

Phase404 freezes a materially new full-depth L2 thesis after Phase403 closed the passive-aware directional rescue route.

The thesis is continuation under a catalyst liquidity vacuum: trade with the impulse only when top-five and levels 2-5 depth align with that impulse and replenishment is weak.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase404_liquidity_vacuum_continuation_precommit_complete | 1 | Phase404 precommit completed |
| phase404_thesis_id | P404_CATALYST_LIQUIDITY_VACUUM_CONTINUATION_FULL_DEPTH | Frozen thesis |
| phase404_material_new_vs_phase403 | 1 | Continuation/liquidity-vacuum thesis, not same reversal/passive rescue |
| phase404_contract_rows | 13 | Contract rows |
| phase404_phase401_ready_event_feature_rows | 270 | Ready input rows |
| phase404_min_abs_impulse_bps | 2.5 | Fixed threshold |
| phase404_min_abs_top5_imbalance | 0.1 | Fixed threshold |
| phase404_min_abs_l2_l5_imbalance | 0.1 | Fixed threshold |
| phase404_max_replenishment_ratio | 0.75 | Liquidity-vacuum threshold |
| phase404_parameter_search_allowed | 0 | No search |
| phase404_execution_allowed_next | 1 | Whether Phase405 may run |
| phase404_strategy_promotion_allowed | 0 | No promotion |
| phase404_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase404_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase404_hard_gate_pass_rows | 9 | Passed hard gates |
| phase404_hard_gate_rows | 9 | Hard gates |
| phase404_next_best_action | run_phase405_liquidity_vacuum_continuation_execution_no_paper_live | Recommended next action |

## Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| thesis_id | P404_CATALYST_LIQUIDITY_VACUUM_CONTINUATION_FULL_DEPTH | Materially new thesis after Phase403 closure. |
| material_difference | liquidity_vacuum_continuation_not_reversal_not_passive_rescue | Do not reuse same reversal/passive-aware rescue route. |
| entry_side | continue_catalyst_impulse_side | Direction follows the post-catalyst impulse. |
| impulse_filter | abs(impulse_bps)>=2.5 | Fixed threshold, no search. |
| top5_alignment | sign(decision_top5_qty_imbalance)==impulse_side and abs>= 0.1 | Full top-five confirmation. |
| l2_l5_alignment | sign(decision_l2_l5_qty_imbalance)==impulse_side and abs>= 0.1 | Levels 2-5 materiality required. |
| liquidity_vacuum | replenishment_ratio<=0.75 | Continuation only when visible replenishment is weak. |
| timing | decision_delay=120;horizon=900 | Reuse current event-feature timing. |
| execution_profile | taker_entry_taker_exit_cost200_fixed_capital | No passive fill rescue; all-in Zerodha 2x cost stress. |
| capital | initial=250000.0;notional=100000.0;max_concurrent=2 | Fixed capital annualization, no unlimited capital. |
| acceptance | selected_events>=30;annualized>12.0;breadth_multi_symbol_date | Same acceptance discipline. |
| controls | side_flip_and_depth_removed_controls | Controls must be logged. |
| forbidden | parameter_search;same_route_rescue;promotion;paper_live;deployable_profit_claim | Boundaries remain closed. |

## Input Registry

| input_id | value | description |
| --- | --- | --- |
| phase403_material_new_required | 1 | Phase403 requires material-new thesis. |
| phase403_same_route_rescue_allowed | 0 | Must be zero. |
| phase401_event_feature_rows | 273 | Latest real-L2 event feature rows. |
| phase401_ready_event_feature_rows | 270 | Ready latest real-L2 event feature rows. |
| required_columns_present | 1 | All columns required for execution. |
| cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned cost model. |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P404_PHASE403_MATERIAL_NEW_REQUIRED | True | 1 | 1 | hard |
| P404_SAME_ROUTE_RESCUE_CLOSED | True | 0 | 0 | hard |
| P404_EVENT_FEATURE_INPUT_PRESENT | True | 270 | >0 | hard |
| P404_REQUIRED_COLUMNS_PRESENT | True | 1 | 1 | hard |
| P404_NOT_REVERSAL_OR_PASSIVE_RESCUE | True | liquidity_vacuum_continuation | material_new | hard |
| P404_FULL_DEPTH_L2_L5_REQUIRED | True | l2_l5_alignment | present | hard |
| P404_FIXED_THRESHOLDS_NO_SEARCH | True | fixed_thresholds | no_grid_search | hard |
| P404_COST200_FIXED_CAPITAL | True | cost=2.0;capital=250000.0;notional=100000.0 | cost200_fixed_capital | hard |
| P404_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

No promotion, paper/live acceptance, deployable profitability claim, or parameter search is opened.
