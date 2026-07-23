# Phase175 Receive-flow Feature Schema Precommit

Generated UTC: 2026-07-23T18:57:48.679306+00:00

Phase175 precommits the real receive-flow feature schema and activation gates before any materialization or strategy replay.
It is not a strategy phase: no signals, orders, fills, P&L, profitability claims, or paper/live acceptance are emitted.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase175_feature_schema_rows | 6 | Precommitted receive-flow feature rows |
| phase175_feature_quality_gate_rows | 12 | Feature quality gates declared |
| phase175_activation_gate_rows | 6 | Activation gates evaluated |
| phase175_hard_gate_rows | 5 | Hard gates evaluated |
| phase175_hard_gate_pass_rows | 5 | Hard gates passed |
| phase175_activation_ready | 0 | 1 means feature materialization may open |
| phase175_ready_receive_flow_dates | 3 | Ready receive-flow dates inherited from Phase172 |
| phase175_additional_dates_needed | 2 | Additional real L2 dates still needed |
| phase175_strategy_replay_allowed | 0 | No strategy replay opened |
| phase175_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase175_forbidden_outputs | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance | Outputs forbidden in this phase |
| phase175_next_best_action | add_AZURE_STORAGE_SAS_TOKEN_or_AZURE_STORAGE_KEY_then_rerun_phase174_phase172_before_phase176 | Recommended next milestone |

## Feature Schema

| feature_id | feature_family | definition | minimum_input_columns | minimum_source_days | allowed_horizons | leakage_control | forbidden_use |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P175_RECEIVE_EVENT_RATE_ZSCORE | receive_cadence | Per symbol/time bucket received-tick count standardized by same-symbol intraday baseline. | collector_received_utc_ms;trade_date;tradingsymbol | 5 | 1s;5s;15s;60s with coverage/staleness reporting | baseline statistics fitted on train dates only before test-date transform | do_not_convert_directly_to_trade_signal_without_phase176_precommit |
| P175_QUOTE_CHURN_RATE | book_state_churn | Rate of top-of-book price/quantity state changes in a bounded receive-time bucket. | collector_received_utc_ms;buy_1_price;buy_1_quantity;sell_1_price;sell_1_quantity | 5 | 1s;5s;15s;60s with symbol-specific coverage gates | computed only from events received at or before the feature timestamp | no future quote state, no posthoc threshold tuning on P&L |
| P175_DEPTH_REFRESH_INTENSITY | top_five_depth_churn | Receive-time rate of visible depth quantity changes across depth rows 1-5 on both sides. | collector_received_utc_ms;buy_1_quantity..buy_5_quantity;sell_1_quantity..sell_5_quantity | 5 | 1s;5s;15s;60s with depth-field completeness gates | uses top-five market-by-price state only; no inferred hidden order events | must not be described as exchange order-by-order L3/L4 data |
| P175_STALE_QUOTE_DURATION | feed_staleness | Elapsed receive time since last top-of-book or depth-quantity state change. | collector_received_utc_ms;buy_1_price;buy_1_quantity;sell_1_price;sell_1_quantity;depth_quantities | 5 | event_time;1s;5s;15s | forward state duration censored at the current timestamp; no future duration completion | no fill-quality inference without later broker/order telemetry |
| P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | cross_symbol_receive_flow | Number/share of universe symbols with at least one received tick in the same 1-second bucket. | collector_received_utc_ms;trade_date;tradingsymbol | 5 | 1s native synchrony source plus 5s/15s aggregations | computed from contemporaneous receive buckets only; target symbol exclusion required in ablation | no reuse of Phase167 fixed S08 score or blocked lead-lag formula |
| P175_RECEIVE_FLOW_REGIME_STATE | source_quality_context | Unsupervised context label from cadence/churn/staleness/synchrony features for filtering only. | P175_RECEIVE_EVENT_RATE_ZSCORE;P175_QUOTE_CHURN_RATE;P175_STALE_QUOTE_DURATION;P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | 5 | daily fitted context with intraday labels | fit context model on train dates only; report train/test date separation | filter/context only until a separate strategy precommit phase opens |

## Feature Quality Gate Catalog

| feature_id | quality_gate_id | gate_definition | minimum_required | failure_action |
| --- | --- | --- | --- | --- |
| P175_RECEIVE_EVENT_RATE_ZSCORE | P175_RECEIVE_EVENT_RATE_ZSCORE_COVERAGE | train and test coverage must be reported by date, symbol and horizon before any strategy precommit | >=5 ready dates and >=30 symbols/date | do_not_activate_feature |
| P175_RECEIVE_EVENT_RATE_ZSCORE | P175_RECEIVE_EVENT_RATE_ZSCORE_LEAKAGE | feature timestamp must be <= label/signal decision timestamp; train-fitted transforms only | zero known future-leakage rows | block_feature_family_and_emit_leakage_ledger |
| P175_QUOTE_CHURN_RATE | P175_QUOTE_CHURN_RATE_COVERAGE | train and test coverage must be reported by date, symbol and horizon before any strategy precommit | >=5 ready dates and >=30 symbols/date | do_not_activate_feature |
| P175_QUOTE_CHURN_RATE | P175_QUOTE_CHURN_RATE_LEAKAGE | feature timestamp must be <= label/signal decision timestamp; train-fitted transforms only | zero known future-leakage rows | block_feature_family_and_emit_leakage_ledger |
| P175_DEPTH_REFRESH_INTENSITY | P175_DEPTH_REFRESH_INTENSITY_COVERAGE | train and test coverage must be reported by date, symbol and horizon before any strategy precommit | >=5 ready dates and >=30 symbols/date | do_not_activate_feature |
| P175_DEPTH_REFRESH_INTENSITY | P175_DEPTH_REFRESH_INTENSITY_LEAKAGE | feature timestamp must be <= label/signal decision timestamp; train-fitted transforms only | zero known future-leakage rows | block_feature_family_and_emit_leakage_ledger |
| P175_STALE_QUOTE_DURATION | P175_STALE_QUOTE_DURATION_COVERAGE | train and test coverage must be reported by date, symbol and horizon before any strategy precommit | >=5 ready dates and >=30 symbols/date | do_not_activate_feature |
| P175_STALE_QUOTE_DURATION | P175_STALE_QUOTE_DURATION_LEAKAGE | feature timestamp must be <= label/signal decision timestamp; train-fitted transforms only | zero known future-leakage rows | block_feature_family_and_emit_leakage_ledger |
| P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_COVERAGE | train and test coverage must be reported by date, symbol and horizon before any strategy precommit | >=5 ready dates and >=30 symbols/date | do_not_activate_feature |
| P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_LEAKAGE | feature timestamp must be <= label/signal decision timestamp; train-fitted transforms only | zero known future-leakage rows | block_feature_family_and_emit_leakage_ledger |
| P175_RECEIVE_FLOW_REGIME_STATE | P175_RECEIVE_FLOW_REGIME_STATE_COVERAGE | train and test coverage must be reported by date, symbol and horizon before any strategy precommit | >=5 ready dates and >=30 symbols/date | do_not_activate_feature |
| P175_RECEIVE_FLOW_REGIME_STATE | P175_RECEIVE_FLOW_REGIME_STATE_LEAKAGE | feature timestamp must be <= label/signal decision timestamp; train-fitted transforms only | zero known future-leakage rows | block_feature_family_and_emit_leakage_ledger |

## Forbidden Overlap Ledger

| blocked_family | phase175_action | overlap_allowed |
| --- | --- | --- |
| PHASE164_S01_TO_S07_S09_SYNTHETIC_FORMS | do_not_reuse_signal_formula_or_threshold | 0 |
| PHASE167_S08_FIXED_CROSS_SYMBOL_LEAD_LAG_FORM | cross-symbol synchrony may be a source feature, but Phase167 fixed S08 score is forbidden | 0 |
| PHASE131_TO_136_TOP_FIVE_DEPTH_PASSIVE_BRANCH | top-five depth churn may be audited as source quality, but passive queue/fill claims remain closed | 0 |

## Activation Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P175_SOURCE_IS_PHASE171_REAL_RECEIVE_FLOW | 1 | phase171_selected_source_id=P171_REAL_MULTIDAY_RECEIVE_EVENT_FLOW | hard |
| P175_PHASE172_STRUCTURAL_GATES_PASS | 1 | phase172_hard_gate_pass_rows=5/5 | hard |
| P175_MINIMUM_REAL_DAYS_AVAILABLE | 0 | ready_dates=3;minimum=5;additional_needed=2 | activation |
| P175_SECURE_DOWNLOAD_PATH_EXISTS | 1 | phase174_download_ran=0;runner=scripts/run_phase174_secure_real_l2_download_orchestrator.ps1 | hard |
| P175_FEATURE_SCHEMA_DECLARED | 1 | feature_rows=6 | hard |
| P175_NO_REPLAY_OR_PROFITABILITY_OUTPUTS | 1 | schema and gates only; forbidden_outputs=buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance | hard |
