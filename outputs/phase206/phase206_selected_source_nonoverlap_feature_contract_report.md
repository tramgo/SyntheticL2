# Phase206 Selected Source Non-overlap Feature Contract

Generated UTC: 2026-07-28T20:47:03.653857+00:00

Phase206 checks the selected Phase205 receive-flow context source against failed/blocked prior forms and catalogs allowed feature families.
It does not fit models, run replay, emit orders/fills/P&L, promote anything, or open paper/live acceptance.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase206_feature_catalog_rows | 6 | Selected source feature-family catalog rows |
| phase206_blocked_reference_rows | 14 | Blocked/failed reference rows checked |
| phase206_nonoverlap_audit_rows | 6 | Non-overlap audit rows |
| phase206_nonoverlap_pass_rows | 6 | Rows passing non-overlap audit |
| phase206_guardrail_rows | 5 | Guardrail contract rows |
| phase206_phase207_work_order_rows | 3 | Phase207 work-order rows |
| phase206_gate_rows | 7 | Gates evaluated |
| phase206_hard_gate_rows | 7 | Hard gates evaluated |
| phase206_hard_gate_pass_rows | 7 | Hard gates passed |
| phase206_nonoverlap_feature_contract_complete | 1 | 1 means Phase206 completed |
| phase206_model_fit_allowed | 0 | No model fitting opened |
| phase206_strategy_replay_allowed | 0 | No strategy replay opened |
| phase206_test_replay_allowed_next | 0 | No test replay opened |
| phase206_promotion_allowed | 0 | No promotion opened |
| phase206_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase206_forbidden_outputs | strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;model_fit | Outputs forbidden in this phase |
| phase206_next_best_action | run_phase207_allowed_feature_matrix_precommit_no_model_no_replay | Recommended next milestone |

## Selected Source Feature Catalog

| phase206_feature_id | source_phase175_feature_id | selected_route_id | feature_family | definition | minimum_input_columns | minimum_source_days | allowed_horizons | leakage_control | phase175_forbidden_use | phase206_allowed_role | model_fit_allowed | strategy_replay_allowed | test_replay_allowed_next | promotion_allowed | paper_or_live_acceptance_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P206_RECEIVE_EVENT_RATE_ZSCORE | P175_RECEIVE_EVENT_RATE_ZSCORE | P205_REAL_RECEIVE_FLOW_CONTEXT_SOURCE_REFRESH | receive_cadence | Per symbol/time bucket received-tick count standardized by same-symbol intraday baseline. | collector_received_utc_ms;trade_date;tradingsymbol | 5 | 1s;5s;15s;60s with coverage/staleness reporting | baseline statistics fitted on train dates only before test-date transform | do_not_convert_directly_to_trade_signal_without_phase176_precommit | source_quality_or_context_feature | 0 | 0 | 0 | 0 | 0 |
| P206_QUOTE_CHURN_RATE | P175_QUOTE_CHURN_RATE | P205_REAL_RECEIVE_FLOW_CONTEXT_SOURCE_REFRESH | book_state_churn | Rate of top-of-book price/quantity state changes in a bounded receive-time bucket. | collector_received_utc_ms;buy_1_price;buy_1_quantity;sell_1_price;sell_1_quantity | 5 | 1s;5s;15s;60s with symbol-specific coverage gates | computed only from events received at or before the feature timestamp | no future quote state, no posthoc threshold tuning on P&L | source_quality_or_context_feature | 0 | 0 | 0 | 0 | 0 |
| P206_DEPTH_REFRESH_INTENSITY | P175_DEPTH_REFRESH_INTENSITY | P205_REAL_RECEIVE_FLOW_CONTEXT_SOURCE_REFRESH | top_five_depth_churn | Receive-time rate of visible depth quantity changes across depth rows 1-5 on both sides. | collector_received_utc_ms;buy_1_quantity..buy_5_quantity;sell_1_quantity..sell_5_quantity | 5 | 1s;5s;15s;60s with depth-field completeness gates | uses top-five market-by-price state only; no inferred hidden order events | must not be described as exchange order-by-order L3/L4 data | top_five_market_by_price_churn_not_l3_l4_order_by_order | 0 | 0 | 0 | 0 | 0 |
| P206_STALE_QUOTE_DURATION | P175_STALE_QUOTE_DURATION | P205_REAL_RECEIVE_FLOW_CONTEXT_SOURCE_REFRESH | feed_staleness | Elapsed receive time since last top-of-book or depth-quantity state change. | collector_received_utc_ms;buy_1_price;buy_1_quantity;sell_1_price;sell_1_quantity;depth_quantities | 5 | event_time;1s;5s;15s | forward state duration censored at the current timestamp; no future duration completion | no fill-quality inference without later broker/order telemetry | source_quality_or_context_feature | 0 | 0 | 0 | 0 | 0 |
| P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | P205_REAL_RECEIVE_FLOW_CONTEXT_SOURCE_REFRESH | cross_symbol_receive_flow | Number/share of universe symbols with at least one received tick in the same 1-second bucket. | collector_received_utc_ms;trade_date;tradingsymbol | 5 | 1s native synchrony source plus 5s/15s aggregations | computed from contemporaneous receive buckets only; target symbol exclusion required in ablation | no reuse of Phase167 fixed S08 score or blocked lead-lag formula | target_excluded_synchrony_context_not_fixed_s08_score | 0 | 0 | 0 | 0 | 0 |
| P206_RECEIVE_FLOW_REGIME_STATE | P175_RECEIVE_FLOW_REGIME_STATE | P205_REAL_RECEIVE_FLOW_CONTEXT_SOURCE_REFRESH | source_quality_context | Unsupervised context label from cadence/churn/staleness/synchrony features for filtering only. | P175_RECEIVE_EVENT_RATE_ZSCORE;P175_QUOTE_CHURN_RATE;P175_STALE_QUOTE_DURATION;P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | 5 | daily fitted context with intraday labels | fit context model on train dates only; report train/test date separation | filter/context only until a separate strategy precommit phase opens | filter_context_only_until_future_precommit | 0 | 0 | 0 | 0 | 0 |

## Blocked Reference Catalog

| blocked_reference_id | blocked_source | blocked_form | blocked_token | recommended_status | unlock_condition |
| --- | --- | --- | --- | --- | --- |
| PHASE164_S01_GUARDED_DIAGNOSTIC | phase165_phase164_full_year_replay_verdict | P164_S01_MLOFI_BREAKOUT | S01 | block_current_phase164_form | new precommitted feature hypothesis, changed label/execution contract, or real-anchor evidence; do not rerun same Phase164 form hoping for profit |
| PHASE164_S02_GUARDED_DIAGNOSTIC | phase165_phase164_full_year_replay_verdict | P164_S02_MULTI_LEVEL_OFI | S02 | block_current_phase164_form | new precommitted feature hypothesis, changed label/execution contract, or real-anchor evidence; do not rerun same Phase164 form hoping for profit |
| PHASE164_S03_GUARDED_DIAGNOSTIC | phase165_phase164_full_year_replay_verdict | P164_S03_LIQUIDITY_VACUUM | S03 | block_current_phase164_form | new precommitted feature hypothesis, changed label/execution contract, or real-anchor evidence; do not rerun same Phase164 form hoping for profit |
| PHASE164_S04_GUARDED_DIAGNOSTIC | phase165_phase164_full_year_replay_verdict | P164_S04_TRADE_FLOW_DEPTH | S04 | block_current_phase164_form | new precommitted feature hypothesis, changed label/execution contract, or real-anchor evidence; do not rerun same Phase164 form hoping for profit |
| PHASE164_S05_GUARDED_DIAGNOSTIC | phase165_phase164_full_year_replay_verdict | P164_S05_MICROPRICE_FILTER | S05 | block_current_phase164_form | new precommitted feature hypothesis, changed label/execution contract, or real-anchor evidence; do not rerun same Phase164 form hoping for profit |
| PHASE164_S06_GUARDED_DIAGNOSTIC | phase165_phase164_full_year_replay_verdict | P164_S06_ABSORPTION_REVERSAL | S06 | block_current_phase164_form | new precommitted feature hypothesis, changed label/execution contract, or real-anchor evidence; do not rerun same Phase164 form hoping for profit |
| PHASE164_S07_GUARDED_DIAGNOSTIC | phase165_phase164_full_year_replay_verdict | P164_S07_IMBALANCE_MEAN_REVERSION | S07 | block_current_phase164_form | new precommitted feature hypothesis, changed label/execution contract, or real-anchor evidence; do not rerun same Phase164 form hoping for profit |
| PHASE164_S09_GUARDED_DIAGNOSTIC | phase165_phase164_full_year_replay_verdict | P164_S09_QUEUE_IMBALANCE_SCALP | S09 | block_current_phase164_form | new precommitted feature hypothesis, changed label/execution contract, or real-anchor evidence; do not rerun same Phase164 form hoping for profit |
| PHASE167_S08_CROSS_SYMBOL_LEAD_LAG_CONTINUATION | phase168_s08_closure | fixed_score_threshold_0_42_market_sector_etf_lagged_depth_pressure_continuation | S08 | block_current_phase167_s08_form | new precommitted feature form, different label/execution contract, or real-anchor evidence; do not rerun this same S08 form shard-after-shard hoping for profit |
| P197_PRIOR_CONTEXT_P197_TIME_OF_DAY_CONTEXT | phase197_prior_context_feature_precommit | intraday_time_context | P197_TIME_OF_DAY_CONTEXT | do_not_reuse_as_model_search_without_new_contract | Allowed only if Phase206 catalog records a materially different feature purpose and no replay/model fitting. |
| P197_PRIOR_CONTEXT_P197_SYMBOL_LIQUIDITY_REGIME | phase197_prior_context_feature_precommit | symbol_liquidity_regime | P197_SYMBOL_LIQUIDITY_REGIME | do_not_reuse_as_model_search_without_new_contract | Allowed only if Phase206 catalog records a materially different feature purpose and no replay/model fitting. |
| P197_PRIOR_CONTEXT_P197_MARKET_CONTEXT_LAGGED | phase197_prior_context_feature_precommit | lagged_market_context | P197_MARKET_CONTEXT_LAGGED | do_not_reuse_as_model_search_without_new_contract | Allowed only if Phase206 catalog records a materially different feature purpose and no replay/model fitting. |
| P197_PRIOR_CONTEXT_P197_ASSET_CLASS_PROXY | phase197_prior_context_feature_precommit | instrument_context | P197_ASSET_CLASS_PROXY | do_not_reuse_as_model_search_without_new_contract | Allowed only if Phase206 catalog records a materially different feature purpose and no replay/model fitting. |
| P197_PRIOR_CONTEXT_P197_MICROSTRUCTURE_TRANSFORMS | phase197_prior_context_feature_precommit | nonlinear_microstructure_context | P197_MICROSTRUCTURE_TRANSFORMS | do_not_reuse_as_model_search_without_new_contract | Allowed only if Phase206 catalog records a materially different feature purpose and no replay/model fitting. |

## Selected Source Non-overlap Audit

| phase206_feature_id | blocked_reference_rows_checked | blocked_forms_digest_available | overlaps_phase164_blocked_strategy_token | overlaps_phase167_fixed_s08_form | overlaps_prior_phase197_context_search_without_new_contract | nonoverlap_pass | audit_note | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P206_RECEIVE_EVENT_RATE_ZSCORE | 14 | 1 | 0 | 0 | 0 | 1 | Feature is source/context contract only; no model fit or replay in Phase206. | 0 |
| P206_QUOTE_CHURN_RATE | 14 | 1 | 0 | 0 | 0 | 1 | Feature is source/context contract only; no model fit or replay in Phase206. | 0 |
| P206_DEPTH_REFRESH_INTENSITY | 14 | 1 | 0 | 0 | 0 | 1 | Feature is source/context contract only; no model fit or replay in Phase206. | 0 |
| P206_STALE_QUOTE_DURATION | 14 | 1 | 0 | 0 | 0 | 1 | Feature is source/context contract only; no model fit or replay in Phase206. | 0 |
| P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | 14 | 1 | 0 | 0 | 0 | 1 | Feature is source/context contract only; no model fit or replay in Phase206. | 0 |
| P206_RECEIVE_FLOW_REGIME_STATE | 14 | 1 | 0 | 0 | 0 | 1 | Feature is source/context contract only; no model fit or replay in Phase206. | 0 |

## Guardrail Contract

| guardrail_id | requirement | required |
| --- | --- | --- |
| P206_NO_MODEL_FIT | Phase206 may catalog features and overlap only; no model fitting, signal scoring or threshold search. | 1 |
| P206_TARGET_SYMBOL_EXCLUSION_FOR_SYNCHRONY | Any future cross-symbol synchrony feature must precommit target-symbol exclusion and must not reuse Phase167 fixed S08 score. | 1 |
| P206_TOP_FIVE_TERMINOLOGY | Depth features must be described as Zerodha top-five market-by-price book state, not exchange L3/L4 order-by-order data. | 1 |
| P206_TRAIN_ONLY_BASELINES_NEXT | Any future baseline/context fitting must be train-date only before validation/test transform. | 1 |
| P206_REPLAY_STAYS_CLOSED | No strategy replay, test replay, order/fill/P&L, promotion or paper/live acceptance may be emitted from Phase206. | 1 |

## Phase207 Work Order

| work_order_id | action | input_feature_rows | allowed_scope | strategy_replay_allowed |
| --- | --- | --- | --- | --- |
| P207_WO01_BUILD_ALLOWED_FEATURE_MATRIX | materialize a feature-availability matrix for the Phase206 catalog, no model fitting | 6 | feature_matrix_no_replay | 0 |
| P207_WO02_TARGET_EXCLUSION_ABLATION_SPEC | precommit target-symbol exclusion and negative-control ablations for cross-symbol synchrony | 6 | ablation_spec_no_replay | 0 |
| P207_WO03_LEAKAGE_AND_TERMINOLOGY_AUDIT | audit leakage controls and L1/top-five terminology before any feature matrix is used downstream | 6 | quality_audit_no_replay | 0 |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P206_PHASE205_COMPLETE | True | phase205_complete=1 | hard |
| P206_FEATURE_CATALOG_RECORDED | True | feature_rows=6 | hard |
| P206_BLOCKED_REFERENCE_CATALOG_RECORDED | True | blocked_rows=14 | hard |
| P206_NONOVERLAP_AUDIT_PASSED | True | nonoverlap_pass_rows=6 | hard |
| P206_GUARDRAILS_RECORDED | True | guardrail_rows=5 | hard |
| P206_PHASE207_WORK_ORDER_RECORDED | True | work_order_rows=3 | hard |
| P206_NO_MODEL_FIT_REPLAY_OR_PROMOTION | True | forbidden_flag_sum=0 | hard |
