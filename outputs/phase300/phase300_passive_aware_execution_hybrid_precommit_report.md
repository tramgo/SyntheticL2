# Phase300 Passive-Aware Execution of Directional L2 Signals Precommit

Phase300 freezes the execution-realism charter before any Phase300 results are generated.

This is not market-making. It is passive-aware execution of already-discovered directional top-five-depth signals.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase300_precommit_complete | 1 | Phase300 passive-aware execution precommit completed |
| phase300_selected_route | P300_PASSIVE_AWARE_DIRECTIONAL_L2_EXECUTION_HYBRID | Selected route |
| phase300_charter_rows | 29 | Charter rows |
| phase300_input_registry_rows | 9 | Input registry rows |
| phase300_execution_work_order_rows | 10 | Execution work-order rows |
| phase300_directional_signal_seed_rows | 16 | Directional seed rows from Phase299 |
| phase300_raw_depth_schema_columns_present | 30 | Required raw depth columns present |
| phase300_l1_only_variant_rows | 0 | L1-only rows |
| phase300_net_edge_live_mask_rows | 0 | Live leakage rows |
| phase300_fill_model_required | 1 | Passive fill model required |
| phase300_adverse_selection_required | 1 | Adverse selection penalty required |
| phase300_forced_flatten_cost_required | 1 | Forced flatten cost required |
| phase300_cost200_required | 1 | 2x cost stress required |
| phase300_fixed_capital_required | 1 | Fixed capital denominator required |
| phase300_min_event_rows | 30 | Acceptance event floor |
| phase300_annualized_threshold_pct | 12 | Acceptance annualized threshold |
| phase300_results_generated | 0 | Precommit only; no Phase300 results generated |
| phase300_strategy_replay_allowed | 0 | No replay |
| phase300_strategy_promotion_allowed | 0 | No promotion |
| phase300_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase300_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase300_hard_gate_pass_rows | 10 | Passed hard gates |
| phase300_hard_gate_rows | 10 | Hard gates |
| phase300_next_best_action | run_phase300_passive_aware_execution_hybrid_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P300_PRECOMMIT_PHASE299_WORK_ORDER_PRESENT | True | run_phase300_passive_aware_execution_hybrid_precommit_no_paper_live | Phase299 routes to Phase300 | hard |
| P300_PRECOMMIT_INPUTS_VERSION_PINNED | True | seeds=16;schema_cols=30 | directional seeds and raw depth schema present | hard |
| P300_PRECOMMIT_L1_ONLY_FORBIDDEN | True | 0 | 0 | hard |
| P300_PRECOMMIT_NO_LOOKAHEAD | True | 0 | 0 | hard |
| P300_PRECOMMIT_FILL_MODEL_REQUIRED | True | fill_model | required | hard |
| P300_PRECOMMIT_ADVERSE_SELECTION_REQUIRED | True | adverse_selection_penalty | required | hard |
| P300_PRECOMMIT_FORCED_FLATTEN_REQUIRED | True | forced_flatten_cost | required | hard |
| P300_PRECOMMIT_COST200_FIXED_CAPITAL | True | cost200;fixed_initial_capital | required | hard |
| P300_PRECOMMIT_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all zero | hard |
| P300_PRECOMMIT_RESULTS_NOT_GENERATED | True | 0 | 0 | hard |

## Charter

| charter_item | value | description |
| --- | --- | --- |
| charter_id | P300_PASSIVE_AWARE_DIRECTIONAL_L2_EXECUTION | Phase300 precommit charter. |
| status | PRECOMMIT_NO_RESULTS_GENERATED | Commit this charter before generating Phase300 backtest results. |
| thesis | directional_l2_edge_may_need_passive_aware_execution_to_survive_retail_costs | Prior taker-style edges were thin versus 2x Zerodha cost stress. |
| not_market_making | 1 | This is passive-aware execution of directional signals, not two-sided continuous retail market-making. |
| directional_signal_source | P235;P268;P280;P281;P282;P298_sparse_directional_signal_seeds | Reuse validated directional signals; no fresh alpha search in Phase300. |
| raw_book_state_source | P51_raw_dense_full_year_lake;P298_schema_audit | Use top-five market-by-price depth levels 1-5 price/qty/order-count. |
| levels_2_to_5_materiality_required | 1 | No L1-only variants. |
| cost_model | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha NSE equity intraday cost model. |
| cost_stress | cost200 | 2x cost stress required. |
| capital_denominator | fixed_initial_capital | No unlimited-capital annualization. |
| initial_notional_cap | lt_100000_INR | Per-order fixed notional must be below the charter cap. |
| isolation_unit | strategy_symbol_date | Per strategy, symbol, date isolation is required for scoring diagnostics. |
| fill_model | P(fill\|queue_depth,side,horizon)_from_raw_depth_levels_1_to_5 | Passive fills must be probabilistic, not assumed. |
| retail_queue_prior | back_of_queue_pessimistic | Retail order starts behind displayed queue. |
| adverse_selection_penalty | fill_conditioned_toxicity_penalty_required | Passive fills are penalized for being more likely when informed flow is against us. |
| forced_flatten_cost | leftover_inventory_pays_taker_spread_plus_full_statutory_costs | No free spread saving by refusing to exit. |
| entry_policy | passive_limit_entry_wait_cancel_or_cross_if_edge_exceeds_total_cost | Hybrid entry policy. |
| exit_policy | passive_when_calm_aggressive_when_risk_or_signal_expiry | Never stay exposed merely to save spread. |
| brokerage_and_taxes | brokerage_per_executed_order_STT_sell_side_txn_GST_SEBI_stamp | Costs apply to passive and aggressive executions; no maker rebate assumed. |
| no_lookahead | net_edge_live_mask_rows_must_equal_0 | Labels may not be used as live masks. |
| acceptance_event_floor | 30 | A sparse >12% result below 30 events is discovery-only. |
| acceptance_annualized_threshold_pct | 12.0 | Cost200 annualized threshold. |
| acceptance_breadth | multi_symbol_and_multi_date_positive | Not a single-day/single-symbol pocket. |
| rank_stability | rank_stable_1x_to_2x_cost | No cost-stress ordering reversal. |
| kill_switch | close_if_no_robust_cost200_above12_or_best_below_30_or_only_survives_by_weakening_penalty | Do not iterate to rescue after honest failure. |
| strategy_replay_allowed | 0 | Boundary remains closed. |
| strategy_promotion_allowed | 0 | Boundary remains closed. |
| paper_or_live_acceptance_allowed | 0 | Boundary remains closed. |
| deployable_profitability_claim_allowed | 0 | Boundary remains closed. |

## Input Registry

| input_id | value | description |
| --- | --- | --- |
| phase299_work_order | run_phase300_passive_aware_execution_hybrid_precommit_no_paper_live | Phase299 must route to Phase300. |
| phase299_selected_route | P300_PASSIVE_AWARE_DIRECTIONAL_L2_EXECUTION_PRECOMMIT | Selected next route. |
| phase299_directional_signal_seed_rows | 16 | Directional seeds available. |
| phase298_raw_depth_schema_columns_present | 30 | Required raw levels 1-5 price/qty/order-count columns present in Phase298 schema audit. |
| phase298_l1_only_variant_rows | 0 | L1-only rows from Phase298. |
| phase298_net_edge_live_mask_rows | 0 | Live leakage rows from Phase298. |
| cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned cost model. |
| raw_dense_source | raw_synthetic_l2_dense_full_year | Raw dense lake root. |
| execution_result_generation_allowed_by_this_phase | 0 | This precommit does not generate Phase300 backtest results. |

## Execution Work Order

| step_id | required_action | description |
| --- | --- | --- |
| 1_signal_intake | load_phase299_directional_signal_seeds | Reuse directional seeds from prior phases; no new alpha grid. |
| 2_raw_depth_features | compute_queue_depth_spread_microprice_depth_slope_replenishment_from_levels_1_to_5 | Feature update uses full top-five market-by-price depth. |
| 3_passive_entry_model | estimate_fill_probability_from_queue_depth_side_horizon_with_back_of_queue_prior | Passive entry cannot fill deterministically. |
| 4_cancel_or_cross | cancel_if_market_moves_away_cross_only_if_expected_move_exceeds_total_cost | Hybrid policy. |
| 5_adverse_selection | apply_fill_conditioned_toxicity_penalty_to_all_passive_fills | Filled passive orders pay toxicity penalty. |
| 6_exit_policy | exit_passively_when_calm_aggressively_on_risk_signal_expiry_or_eod | Do not hold exposure to save spread. |
| 7_forced_flatten | charge_taker_spread_and_full_statutory_cost_for_leftover_inventory | End-of-signal or EOD inventory must be flattened. |
| 8_cost_scoring | zerodha_costs_cost200_fixed_initial_capital_initial_notional_lt_100000 | Pinned retail cost model and fixed capital. |
| 9_acceptance | events_ge_30_annualized_gt_12_cost200_breadth_rank_stability | Sparse <30-event sparks are clues only. |
| 10_boundaries | replay_0_promotion_0_paper_live_0_profitability_claim_0 | No promotion on Phase300 precommit or training run. |
