# Phase434 Strategy Decision and Non-Threshold Source Precommit

Phase434 responds to Phase433 by choosing the execution path rather than continuing same-threshold full-depth sweeps.

Selected source: `supervised_full_depth_event_ranker`.

This is not a profitability result. It is a frozen source decision that allows Phase435 to execute a materially different strategy test: a train-only supervised event ranker using L1-L5 book state and cost-aware forward labels.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase434_strategy_decision_precommit_complete | 1 | Phase434 source decision completed |
| phase434_thesis_id | P434_SUPERVISED_FULL_DEPTH_EVENT_RANKER_SOURCE_PRECOMMIT | Frozen thesis/source precommit |
| phase434_selected_source_id | supervised_full_depth_event_ranker | Selected materially new source |
| phase434_selected_source_uses_l2_l5 | 1 | Selected source uses full top-five depth |
| phase434_selected_source_non_threshold | 1 | Selected source is not another threshold-family sweep |
| phase434_execution_results_generated | 0 | Precommit only |
| phase434_strategy_promotion_allowed | 0 | No promotion |
| phase434_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase434_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase434_execution_allowed_next | 1 | Whether Phase435 may execute |
| phase434_hard_gate_pass_rows | 11 | Passed hard gates |
| phase434_hard_gate_rows | 11 | Hard gates |
| phase434_next_best_action | run_phase435_supervised_full_depth_event_ranker_no_paper_live | Recommended next action |

## Prior Evidence Boundary

| phase | route | verdict_or_status | reason_for_not_continuing |
| --- | --- | --- | --- |
| P409 | retail_two_sided_market_maker_cancel_latency | P409_CANCEL_RACE_MARKET_MAKER_FALSIFIED | attached cancel-included charter line already tested; do not reopen without new external execution source |
| P423 | pair_spread_convergence | P423_PAIR_SPREAD_POSITIVE_LEAD_FALSIFIED_BY_REALISM_RETEST | realism retest closed the route; do not repair with same-stack tuning |
| P426 | queue_depletion_continuation | P426_QUEUE_DEPLETION_CONTINUATION_REJECTED_ZERO_SYNTHETIC_EVENTS | queue-depletion continuation failed acceptance; broader sweep was already attempted next |
| P433 | geometry_consistent_full_depth_threshold_family_sweep | P433_GEOMETRY_CONSISTENT_FULL_DEPTH_SWEEP_REJECTED_NEGATIVE_SPARSE | threshold-family sweep produced active but sparse negative cost200 trades; no same-threshold tuning |

## Source Scorecard

| source_id | material_new_axis | uses_l2_l5_core | non_threshold_source | can_execute_next | why_selected |
| --- | --- | --- | --- | --- | --- |
| supervised_full_depth_event_ranker | learned event ranking from full-depth L1-L5 feature vectors and cost-aware forward labels | 1 | 1 | 1 | moves away from hand-threshold sweeps; ranks only the best events per symbol/date under fixed cost-aware labels |
| more_same_threshold_sweep | none | 1 | 0 | 0 | rejected: Phase433 forbids same-threshold family tuning after negative sparse result |
| retail_market_maker_cancel_latency_rescue | none_without_new_external_execution_source | 1 | 0 | 0 | rejected: attached cancel-included route already ran through Phase407-409 and was falsified |
| fresh_real_l2_download_only | data_breadth_without_new_signal_source | 1 | 1 | 0 | not selected now: useful later, but low disk space and no frozen new candidate makes it a storage-first detour |

## Frozen Phase435 Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| thesis_id | P434_SUPERVISED_FULL_DEPTH_EVENT_RANKER_SOURCE_PRECOMMIT | Phase434 selected source precommit. |
| selected_source | supervised_full_depth_event_ranker | Materially new non-threshold source for Phase435. |
| source_row_hash | a1feccfc33856342e93122e87a0148bdafb9e1809e4f29b17bfea16f60452eaa | Hash of selected source row. |
| model_family | train_only_regularized_event_ranker_logistic_or_tree_baseline | Phase435 may compare simple rankers but must choose from train-only scoring. |
| primary_features | L1_mid_spread_volume_plus_L2_to_L5_depth_shape_imbalance_slope_pressure_replenishment | Full top-five book state remains core. |
| label_design | forward_3_ticks_cost_aware_net_bps_and_tradeability_label | Label must subtract pinned Zerodha cost model before ranking. |
| capital_policy | fixed_initial_capital_1000000_inr_order_notional_100000_inr_cost200 | Annualized return denominator is fixed capital, not unlimited capital. |
| selection_policy | train_only_top_k_event_budget_per_symbol_date_then_validation_execution | No validation/test threshold tuning. |
| controls_required | l1_only_feature_ablation_side_flip_time_shuffle_real_anchor_cross_check | Controls must be emitted by Phase435. |
| acceptance_floor | annualized_return_pct_ge_12_cost200_and_event_floor_ge_30_and_positive_date_fraction_ge_0p60 | Profitability threshold remains the user's >12% annualized bar with breadth. |
| forbidden | same_threshold_family_tuning;market_maker_rescue_without_external_execution_source;promotion;paper_live;deployable_profitability_claim | Closed boundaries. |
| execution_results_generated_now | 0 | Phase434 freezes the source only. |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P434_PHASE433_AVAILABLE | True | P433 evidence row present | present | hard |
| P434_PHASE433_NEXT_ACTION_MATCHED | True | threshold-family sweep produced active but sparse negative cost200 trades; no same-threshold tuning | no same-threshold tuning | hard |
| P434_ATTACHED_CANCEL_CHARTER_RECONCILED | True | P409 cancel-latency evidence row present | present | hard |
| P434_SELECTED_SOURCE_PRESENT | True | 1 | 1 | hard |
| P434_SELECTED_SOURCE_USES_L2_L5 | True | 1 | 1 | hard |
| P434_SELECTED_SOURCE_NON_THRESHOLD | True | 1 | 1 | hard |
| P434_PHASE435_EXECUTION_ALLOWED | True | 1 | 1 | hard |
| P434_COST200_FIXED_CAPITAL_PRECOMMITTED | True | fixed_initial_capital_1000000_inr_order_notional_100000_inr_cost200 | cost200 fixed capital | hard |
| P434_CONTROLS_PRECOMMITTED | True | l1_only_feature_ablation_side_flip_time_shuffle_real_anchor_cross_check | l1/control set | hard |
| P434_RESULTS_NOT_GENERATED | True | 0 | 0 | hard |
| P434_BOUNDARIES_CLOSED | True | same_threshold_family_tuning;market_maker_rescue_without_external_execution_source;promotion;paper_live;deployable_profitability_claim | closed | hard |

Boundary: Phase435 may execute the selected supervised full-depth event-ranker source, but may not rescue the same Phase427/431 threshold families or reopen the attached cancel-latency market-maker route without a new external execution source.
