# Phase320 Event-Catalyst Multi-Event Feature Materialization

Phase320 materializes a compact event-symbol feature matrix from the accepted Phase317/318 top-five market-by-price depth join.
It keeps target response columns separated from live signal columns and does not run strategy search, replay, promotion, paper/live acceptance, or profitability claims.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase320_multievent_feature_materialization_complete | 1 | Phase320 multi-event feature materialization completed |
| phase320_feature_matrix_rows | 320 | Compact event-symbol feature matrix rows |
| phase320_event_rows | 10 | Distinct events |
| phase320_symbol_rows | 32 | Distinct symbols |
| phase320_source_tick_rows | 28350310 | Joined ticks represented |
| phase320_min_source_tick_rows_per_event_symbol | 78283 | Minimum raw tick support per event-symbol row |
| phase320_live_feature_columns | 38 | Live feature columns |
| phase320_depth_feature_columns | 23 | Depth-aware live feature columns |
| phase320_target_columns | 5 | Separated target columns |
| phase320_live_feature_null_cells | 0 | Live feature null cells |
| phase320_target_null_cells | 0 | Target null cells |
| phase320_target_columns_used_as_live_features | 0 | Target columns used as live features |
| phase320_full_depth_required | 1 | Depth levels 1-5 required |
| phase320_depth_beyond_l1_required | 1 | Depth levels 2-5 materiality required |
| phase320_l1_only_variant_rows_allowed | 0 | No L1-only variants allowed |
| phase320_net_edge_live_mask_rows_allowed | 0 | No net-edge live lookahead mask allowed |
| phase320_strategy_search_allowed_now | 0 | No strategy search in Phase320 |
| phase320_strategy_replay_allowed | 0 | No replay |
| phase320_strategy_promotion_allowed | 0 | No promotion |
| phase320_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase320_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase320_hard_gate_pass_rows | 11 | Passed hard gates |
| phase320_hard_gate_rows | 11 | Hard gates |
| phase320_next_best_action | run_phase321_event_catalyst_multievent_strategy_search_precommit_no_replay | Recommended next action |

## Feature quality

| metric | value | description |
| --- | --- | --- |
| feature_matrix_rows | 320 | Expected compact event-symbol rows. |
| event_rows | 10 | Distinct events. |
| symbol_rows | 32 | Distinct symbols. |
| source_tick_rows | 28350310 | Joined ticks represented by the compact matrix. |
| min_source_tick_rows_per_event_symbol | 78283 | Minimum raw tick support per event-symbol row. |
| live_feature_columns | 38 | Columns available to live signal modeling. |
| depth_feature_columns | 23 | Live feature columns using depth levels 1-5 or 2-5. |
| target_columns | 5 | Separated target/response columns. |
| live_feature_null_cells | 0 | Null cells across live feature columns. |
| target_null_cells | 0 | Null cells across target columns. |
| joined_rows_expected | 28350310 | Phase318 accepted joined rows. |
| joined_rows_represented | 28350310 | Source rows represented in matrix. |
| target_columns_used_as_live_features | 0 | Must remain zero. |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P320_PHASE319_COMPLETE | True | 1 | 1 | hard |
| P320_FEATURE_MATRIX_ROWS | True | 320 | 320 | hard |
| P320_EVENT_BREADTH | True | 10 | >=10 | hard |
| P320_SYMBOL_BREADTH | True | 32 | >=32 | hard |
| P320_JOIN_ROWS_REPRESENTED | True | 28350310/28350310 | equal | hard |
| P320_MIN_RAW_TICKS_PRESENT | True | 78283 | >0 | hard |
| P320_LIVE_FEATURE_COLUMNS_PRESENT | True | 38 | >=35 | hard |
| P320_DEPTH_FEATURE_COLUMNS_PRESENT | True | 23 | >=20 | hard |
| P320_TARGET_COLUMNS_SEPARATED | True | targets=5;live_target_cols=0 | 5_targets_and_0_live_targets | hard |
| P320_NO_STRATEGY_SEARCH_OPENED | True | strategy_search_allowed_now=0 | 0 | hard |
| P320_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |
