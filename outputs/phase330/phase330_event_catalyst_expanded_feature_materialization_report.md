# Phase330 Event-Catalyst Expanded Feature Materialization

Phase330 materializes a compact event-symbol feature matrix from the repaired Phase327 and accepted Phase328 top-five market-by-price depth join.
It keeps target response columns separated from live signal columns and does not run strategy search, replay, promotion, paper/live acceptance, or profitability claims.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase330_expanded_feature_materialization_complete | 1 | Phase330 expanded feature materialization completed |
| phase330_feature_matrix_rows | 1600 | Compact event-symbol feature matrix rows |
| phase330_event_rows | 50 | Distinct events |
| phase330_symbol_rows | 32 | Distinct symbols |
| phase330_source_tick_rows | 141708530 | Joined ticks represented |
| phase330_min_source_tick_rows_per_event_symbol | 78007 | Minimum raw tick support per event-symbol row |
| phase330_live_feature_columns | 38 | Live feature columns |
| phase330_depth_feature_columns | 23 | Depth-aware live feature columns |
| phase330_target_columns | 5 | Separated target columns |
| phase330_live_feature_null_cells | 0 | Live feature null cells |
| phase330_target_null_cells | 0 | Target null cells |
| phase330_target_columns_used_as_live_features | 0 | Target columns used as live features |
| phase330_matrix_parquet_written | 1 | Feature matrix parquet written |
| phase330_matrix_parquet_bytes | 440746 | Feature matrix parquet bytes |
| phase330_full_depth_required | 1 | Depth levels 1-5 required |
| phase330_depth_beyond_l1_required | 1 | Depth levels 2-5 materiality required |
| phase330_l1_only_variant_rows_allowed | 0 | No L1-only variants allowed |
| phase330_net_edge_live_mask_rows_allowed | 0 | No net-edge live lookahead mask allowed |
| phase330_strategy_search_allowed_now | 0 | No strategy search in Phase330 |
| phase330_strategy_replay_allowed | 0 | No replay |
| phase330_strategy_promotion_allowed | 0 | No promotion |
| phase330_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase330_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase330_hard_gate_pass_rows | 12 | Passed hard gates |
| phase330_hard_gate_rows | 12 | Hard gates |
| phase330_next_best_action | run_phase331_event_catalyst_expanded_strategy_search_precommit_no_replay | Recommended next action |

## Feature quality

| metric | value | description |
| --- | --- | --- |
| feature_matrix_rows | 1600 | Expected compact event-symbol rows. |
| event_rows | 50 | Distinct events. |
| symbol_rows | 32 | Distinct symbols. |
| source_tick_rows | 141708530 | Joined ticks represented by the compact matrix. |
| min_source_tick_rows_per_event_symbol | 78007 | Minimum raw tick support per event-symbol row. |
| live_feature_columns | 38 | Columns available to live signal modeling. |
| depth_feature_columns | 23 | Live feature columns using depth levels 1-5 or 2-5. |
| target_columns | 5 | Separated target/response columns. |
| live_feature_null_cells | 0 | Null cells across live feature columns. |
| target_null_cells | 0 | Null cells across target columns. |
| joined_rows_expected | 141708530 | Phase328 accepted joined rows. |
| joined_rows_represented | 141708530 | Source rows represented in matrix. |
| target_columns_used_as_live_features | 0 | Must remain zero. |
| matrix_parquet_written | 1 | Feature matrix parquet was written. |
| matrix_parquet_bytes | 440746 | Feature matrix parquet size in bytes. |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P330_PHASE329_COMPLETE | True | 1 | 1 | hard |
| P330_FEATURE_MATRIX_ROWS | True | 1600 | 1600 | hard |
| P330_EVENT_BREADTH | True | 50 | >=50 | hard |
| P330_SYMBOL_BREADTH | True | 32 | >=32 | hard |
| P330_JOIN_ROWS_REPRESENTED | True | 141708530/141708530 | equal | hard |
| P330_MIN_RAW_TICKS_PRESENT | True | 78007 | >0 | hard |
| P330_LIVE_FEATURE_COLUMNS_PRESENT | True | 38 | >=35 | hard |
| P330_DEPTH_FEATURE_COLUMNS_PRESENT | True | 23 | >=20 | hard |
| P330_TARGET_COLUMNS_SEPARATED | True | targets=5;live_target_cols=0 | 5_targets_and_0_live_targets | hard |
| P330_MATRIX_PARQUET_WRITTEN | True | written=1;bytes=440746 | written_and_nonempty | hard |
| P330_NO_STRATEGY_SEARCH_OPENED | True | strategy_search_allowed_now=0 | 0 | hard |
| P330_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |
