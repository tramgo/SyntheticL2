# Phase334 Cost-Stress Margin Redesign Precommit

Phase334 precommits a narrow redesign around the Phase333-preserved depth-acceleration reversal near miss.
It is not a replay, promotion, paper/live gate, or profitability claim.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase334_cost_stress_margin_redesign_precommit_complete | 1 | Phase334 precommit completed |
| phase334_preserved_family | P331_DEPTH_ACCEL_REVERSAL | Family preserved from Phase333 |
| phase334_design_lane_rows | 4 | Design lanes |
| phase334_search_contract_rows | 14 | Search contract rows |
| phase334_phase335_work_order_rows | 9 | Phase335 work-order rows |
| phase334_best_cost200_prior_annualized_return_pct | 11.517554062957867 | Prior best 2x-cost annualized return |
| phase334_required_annualized_threshold_pct | 12 | Required annualized threshold |
| phase334_required_cost_profile | zerodha_2x_all_in_cost_proxy | Required cost profile |
| phase334_full_depth_required | 1 | Full top-five depth required |
| phase334_levels_2_to_5_required | 1 | Levels 2-5 materiality required |
| phase334_l1_only_allowed | 0 | No L1-only variants |
| phase334_net_edge_live_mask_allowed | 0 | No net-edge/future-outcome live masks |
| phase334_strategy_replay_allowed | 0 | No replay |
| phase334_strategy_promotion_allowed | 0 | No promotion |
| phase334_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase334_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase334_strategy_search_execution_allowed_next | 1 | Phase335 training-only execution allowed next |
| phase334_hard_gate_pass_rows | 10 | Passed hard gates |
| phase334_hard_gate_rows | 10 | Hard gates |
| phase334_next_best_action | run_phase335_cost_stress_margin_redesign_training_only_no_replay | Recommended next action |

## Design lanes

| lane_id | preserved_family | hypothesis | allowed_live_filters | forbidden_filters | cost_stress_required | full_depth_required | levels_2_to_5_required | passive_diagnostic_required | primary_execution_policy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P334_LANE_A_STRICTER_DEPTH_ACCEL_EDGE | P331_DEPTH_ACCEL_REVERSAL | The 2x-cost miss is small enough that stricter live depth-acceleration reversal entries may lift average edge per trade above the cost-stress hurdle. | abs_depth_accel_quantile>=0.95; spread_bps<=recent_median; depth_l1_l5_qty_share_bidask_material | future_return; net_edge; target; realized_pnl; post_entry_outcome | 1 | 1 | 1 | 1 | taker_entry_taker_exit |
| P334_LANE_B_TURNOVER_COMPRESSION | P331_DEPTH_ACCEL_REVERSAL | Reduce cost drag by allowing only the strongest one or two symbols per event while preserving at least 30 scheduled events. | rank_abs_signal_within_event<=1_or_2; event_bucket=all_or_macro; max_trade_rows_per_event_cap | sort_by_future_pnl; sort_by_target_return; realized_winner_selection | 1 | 1 | 1 | 1 | taker_entry_taker_exit |
| P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | P331_DEPTH_ACCEL_REVERSAL | The 0.482445937 percentage-point gap may close if trades avoid wide-spread/weak-book states using only live top-five depth quality. | spread_bps_quantile<=0.50; top5_notional_depth_quantile>=0.50; order_count_imbalance_l1_l5_material | post_trade_slippage; fill_success_after_entry; realized_exit_quality | 1 | 1 | 1 | 1 | taker_entry_taker_exit |
| P334_LANE_D_HORIZON_AND_EXIT_MARGIN | P331_DEPTH_ACCEL_REVERSAL | Cost-stress margin may improve by testing nearby exit horizons and forced-flat timing around the 900-second near miss without looking at future labels during signal formation. | horizon_seconds in 600,900,1200,1500; no_new_target_columns_as_features; fixed_event_scheduler | choose_horizon_per_event_from_realized_pnl; use_future_return_as_mask | 1 | 1 | 1 | 1 | taker_entry_taker_exit |

## Search contract

| contract_id | contract_value | description |
| --- | --- | --- |
| input_matrix | outputs/phase330/phase330_feature_matrix.parquet | Use the existing expanded full-depth event feature matrix. |
| scenario_source | outputs/phase332/phase332_scenario_summary.parquet | Use Phase332 only for precommitted clue selection and diagnostic comparison. |
| preserved_family | P331_DEPTH_ACCEL_REVERSAL | Only redesign around the Phase333-preserved family. |
| annualized_threshold_pct | 12 | Do not lower the user profitability threshold. |
| cost_profile_required | zerodha_2x_all_in_cost_proxy | Acceptance diagnostics require 2x Zerodha all-in cost stress. |
| robust_event_floor | 30 | Acceptance-grade diagnostics require at least 30 scheduled events. |
| fixed_capital_denominator | required | Annualized return must use fixed initial capital. |
| full_depth_top5_required | 1 | Use top-five market-by-price depth and features using levels beyond L1. |
| l1_only_allowed | 0 | No L1-only strategy variant is allowed. |
| net_edge_live_mask_allowed | 0 | No future outcome or net-edge live masks are allowed. |
| passive_aware_policy | diagnostic_required_not_primary_rescue | Passive-aware fill/adverse-selection/forced-flatten penalties remain in diagnostics. |
| strategy_replay_allowed | 0 | Phase334 is precommit only. |
| paper_or_live_allowed | 0 | No paper/live acceptance opens here. |
| profitability_claim_allowed | 0 | No deployable profitability claim opens here. |

## Phase335 work order

| work_order_id | lane_id | action | requirements |
| --- | --- | --- | --- |
| P334_LANE_A_STRICTER_DEPTH_ACCEL_EDGE_GRID | P334_LANE_A_STRICTER_DEPTH_ACCEL_EDGE | build_training_only_redesign_grid | cost200 required; fixed capital; full top-five depth; no future masks |
| P334_LANE_A_STRICTER_DEPTH_ACCEL_EDGE_CONTROLS | P334_LANE_A_STRICTER_DEPTH_ACCEL_EDGE | attach_controls | side flip; random side; family-neutral broadness; passive-aware diagnostic |
| P334_LANE_B_TURNOVER_COMPRESSION_GRID | P334_LANE_B_TURNOVER_COMPRESSION | build_training_only_redesign_grid | cost200 required; fixed capital; full top-five depth; no future masks |
| P334_LANE_B_TURNOVER_COMPRESSION_CONTROLS | P334_LANE_B_TURNOVER_COMPRESSION | attach_controls | side flip; random side; family-neutral broadness; passive-aware diagnostic |
| P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_GRID | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | build_training_only_redesign_grid | cost200 required; fixed capital; full top-five depth; no future masks |
| P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_CONTROLS | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | attach_controls | side flip; random side; family-neutral broadness; passive-aware diagnostic |
| P334_LANE_D_HORIZON_AND_EXIT_MARGIN_GRID | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | build_training_only_redesign_grid | cost200 required; fixed capital; full top-five depth; no future masks |
| P334_LANE_D_HORIZON_AND_EXIT_MARGIN_CONTROLS | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | attach_controls | side flip; random side; family-neutral broadness; passive-aware diagnostic |
| P334_ACCEPTANCE_AND_REPORTING | all | write_phase335_outputs | scenario surface; top candidates; cost200 above12 count; acceptance-grade count; no replay claim |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P334_PHASE333_COMPLETE | True | 1 | 1 | hard |
| P334_NEAR_MISS_PRESERVED | True | 1 | 1 | hard |
| P334_COST200_NOT_ALREADY_ACCEPTED | True | 0 | 0 | hard |
| P334_BEST_COST200_WITHIN_REDESIGN_RANGE | True | 11.5176 | >=10 and <12 | hard |
| P334_DESIGN_LANES_PRESENT | True | 4 | >=4 | hard |
| P334_CONTRACT_ROWS_PRESENT | True | 14 | >=12 | hard |
| P334_WORK_ORDER_PRESENT | True | 9 | >=9 | hard |
| P334_FULL_DEPTH_REQUIRED | True | all | all=1 | hard |
| P334_LEVELS_2_TO_5_REQUIRED | True | all | all=1 | hard |
| P334_NO_REPLAY_OR_CLAIM | True | replay=0;claim=0 | both_zero | hard |

