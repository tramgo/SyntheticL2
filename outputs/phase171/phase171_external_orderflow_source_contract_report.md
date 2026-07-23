# Phase171 External/Order-flow Feature Source Contract

Generated UTC: 2026-07-23T16:05:40.325220+00:00

Phase171 responds to Phase170 by refusing replay and declaring the next genuinely new data axis required for further research.
It is a source contract/work-order only: no signal, order stream, fill model, P&L replay, or profitability claim is emitted.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase171_source_contract_rows | 3 | External/order-flow source candidates declared |
| phase171_selected_source_id | P171_REAL_MULTIDAY_RECEIVE_EVENT_FLOW | Highest-priority allowed next data axis |
| phase171_work_order_rows | 3 | Work-order rows emitted |
| phase171_overlap_audit_rows | 3 | Blocked-family overlap audit rows |
| phase171_gate_rows | 6 | Gates evaluated |
| phase171_all_gates_pass | 1 | 1 means contract obeys guardrails |
| phase171_strategy_replay_allowed | 0 | No strategy replay opened |
| phase171_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase171_azure_read_policy | forbidden_for_analysis_download_first_then_local | No direct Python Azure strategy scans |
| phase171_next_best_action | run_download_first_real_l2_receive_flow_availability_audit_or_collect_broker_order_telemetry | Recommended next milestone |
| phase171_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Cost model retained for audit continuity |

## Source Contract

| source_id | source_class | priority | current_availability | why_new_axis | required_local_layout | minimum_source_gate | allowed_feature_examples | forbidden_overlap | first_allowed_deliverable | strategy_replay_allowed | blocked_by_phase170 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P171_REAL_MULTIDAY_RECEIVE_EVENT_FLOW | external_real_l2_orderflow_proxy | 1 | partial_or_unknown_until_local_real_l2_refresh | Uses multiday real receive-event cadence, quote-churn and cross-symbol synchrony rather than synthetic depth-price twitch signals. | real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | >=5 ready real anchor days; >=30 symbols per day; local DuckDB catalog refreshed; no Azure scan during analysis | receive_event_rate_zscore;quote_churn_rate;depth_refresh_intensity;cross_symbol_arrival_synchrony;stale_quote_duration | no Phase164 S01-S07/S09 signal formulas; no Phase167 fixed S08 score; no passive queue replay | availability_and_feature_schema_audit_no_replay | 0 | 1 |
| P171_BROKER_ORDER_TELEMETRY | own_order_and_latency_telemetry | 2 | not_available_in_workspace | Would add own decision/order/ack/fill/reject/cancel timing, which is absent from Zerodha market-depth callbacks. | broker_logs/orders/trade_date=YYYY-MM-DD/*.parquet_or_csv plus order id linkage | actual broker/order telemetry with timestamps, status transitions and fill/reject outcomes; contract-note costs if available | decision_to_order_latency;order_ack_latency;cancel_latency;reject_rate;partial_fill_rate | no synthetic fills used as broker evidence; no broker-readiness claim without actual logs | schema_contract_and_missing_evidence_ledger | 0 | 0 |
| P171_EXTERNAL_REGIME_CONTEXT | external_market_context | 3 | not_available_in_workspace | Would add non-book context such as index/sector regime, macro calendar or volatility proxy, not another top-five-depth transform. | external_context/trade_date=YYYY-MM-DD/*.parquet_or_csv | timestamped context series with license/provenance, no future leakage and train/test split coverage | index_regime_state;sector_dispersion;volatility_proxy;calendar_event_flag | no posthoc P&L selection; no forward-filled future macro labels | external_context_contract_no_replay | 0 | 0 |

## Selected Source Work Order

| work_order_id | selected_source_id | step | action | required_before_execution | local_only_command_family | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| P171_WO01_DOWNLOAD_FIRST_REAL_RECEIVE_FLOW_SOURCE | P171_REAL_MULTIDAY_RECEIVE_EVENT_FLOW | 1 | refresh_real_l2_local_panel | download/import at least 2 additional ready real L2 day(s) | AzCopy download first, then Phase147/Phase145/Phase146 local verification | 0 |
| P171_WO02_RECEIVE_FLOW_SCHEMA_AUDIT | P171_REAL_MULTIDAY_RECEIVE_EVENT_FLOW | 2 | build_receive_event_flow_feature_schema | Phase146 real-anchor unlock audit must show local ready dates; otherwise emit missing-evidence ledger only | DuckDB scans over downloaded local Parquet | 0 |
| P171_WO03_NO_REPLAY_PRECOMMIT_GATE | P171_REAL_MULTIDAY_RECEIVE_EVENT_FLOW | 3 | precommit_feature_quality_gates_before_any_signal | feature schema coverage >=5 days and no blocked-family overlap | no strategy command allowed | 0 |

## Blocked Family Overlap Audit

| source_id | blocked_family_rows_checked | overlaps_blocked_current_form | overlap_detail | strategy_replay_allowed |
| --- | --- | --- | --- | --- |
| P171_REAL_MULTIDAY_RECEIVE_EVENT_FLOW | 9 | 0 | none_detected_by_contract_scope | 0 |
| P171_BROKER_ORDER_TELEMETRY | 9 | 0 | none_detected_by_contract_scope | 0 |
| P171_EXTERNAL_REGIME_CONTEXT | 9 | 0 | none_detected_by_contract_scope | 0 |

## Gate Evaluation

| gate_id | gate_pass | evidence |
| --- | --- | --- |
| P171_PHASE170_REPLAY_BLOCK_CONFIRMED | 1 | phase170_replay_ready=0 |
| P171_SOURCE_CONTRACT_ROWS | 1 | source_rows=3 |
| P171_SELECTED_SOURCE_IS_NEW_AXIS | 1 | Uses multiday real receive-event cadence, quote-churn and cross-symbol synchrony rather than synthetic depth-price twitch signals. |
| P171_BLOCKED_OVERLAP_AUDITED | 1 | overlap_rows=3 |
| P171_NO_REPLAY | 1 | all strategy_replay_allowed fields are 0 |
| P171_DOWNLOAD_FIRST_LOCAL_FIRST | 1 | work order requires download-first local analysis |
