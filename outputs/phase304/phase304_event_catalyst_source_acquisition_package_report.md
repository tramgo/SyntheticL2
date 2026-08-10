# Phase304 Event-Catalyst Source Acquisition Package

Phase304 creates the acquisition package for the material-new external event-catalyst source selected by Phase303. It deliberately does not run strategy search.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase304_source_acquisition_package_complete | 1 | Phase304 source acquisition package completed |
| phase304_required_schema_rows | 7 | Required event schema rows |
| phase304_optional_schema_rows | 5 | Optional event schema rows |
| phase304_dropzone_file_rows | 1 | CSV files inventoried in dropzone |
| phase304_non_template_source_file_rows | 0 | Non-template source files currently present |
| phase304_external_event_rows_imported | 0 | No event rows imported in Phase304 |
| phase304_strategy_search_allowed_now | 0 | No strategy search until source is populated and audited |
| phase304_strategy_replay_allowed | 0 | No replay |
| phase304_strategy_promotion_allowed | 0 | No promotion |
| phase304_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase304_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase304_hard_gate_pass_rows | 8 | Passed hard gates |
| phase304_hard_gate_rows | 8 | Hard gates |
| phase304_next_best_action | populate_event_catalyst_dropzone_then_run_phase305_event_catalyst_source_import_audit | Recommended next action |

## Required schema

| column_name | data_type | required_status | description |
| --- | --- | --- | --- |
| event_time_ist | datetime_ist | required | Timestamp at which the market could first react; no future publication time allowed. |
| event_type | category | required | One of macro_release, rbi_policy, earnings_result, corporate_announcement, index_rebalance, block_deal, sector_news, other. |
| symbol_scope | pipe_or_comma_symbols | required | NSE symbols affected directly; use ALL if index-wide. |
| index_scope | category | required | NIFTY50, BANKNIFTY, SECTOR, ALL, or NONE. |
| source_url_or_file | string | required | External URL or local evidence file path backing the event. |
| confidence | float_0_to_1 | required | Confidence that timestamp/scope are usable without hindsight. |
| embargo_safe_flag | int_0_or_1 | required | 1 only if the event time is observable no later than the reaction window start. |
| event_title | string | optional | Human-readable event title. |
| expected_impact_side | category | optional | unknown, bullish, bearish, mixed; optional metadata only, not a label. |
| source_provider | string | optional | NSE, BSE, RBI, company_ir, news_vendor, manual_ledger, etc. |
| source_published_time_ist | datetime_ist | optional | Publication time if different from event time. |
| notes | string | optional | Free-text notes for source audit. |

## Allowed event types

| event_type | description |
| --- | --- |
| macro_release | Scheduled or surprise macro release affecting broad market or sector. |
| rbi_policy | RBI policy/rate/liquidity event with timestamped release. |
| earnings_result | Company result or guidance event with symbol-specific scope. |
| corporate_announcement | Exchange/company announcement with timestamped public release. |
| index_rebalance | Index inclusion/exclusion/rebalance event with known effective or announcement time. |
| block_deal | Large block/bulk deal or ownership event when externally timestamped. |
| sector_news | Sector-wide catalyst from an external feed or manual evidence ledger. |
| other | Allowed only with notes and source evidence. |

## Dropzone inventory

| path | row_count | required_columns_present | read_error |
| --- | --- | --- | --- |
| event_sources\event_catalysts\dropzone\event_catalyst_events_template.csv | 1 | 1 |  |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P304_PHASE303_SELECTOR_COMPLETE | True | 1 | 1 | hard |
| P304_PHASE303_SELECTED_EXTERNAL_SOURCE | True | 1 | 1 | hard |
| P304_REQUIRED_SCHEMA_DECLARED | True | 7 | 7 | hard |
| P304_TEMPLATE_EMITTED | True | 12 | 12 | hard |
| P304_DROPZONE_INVENTORIED | True | 1 | >=0 | hard |
| P304_NO_STRATEGY_SEARCH_OPENED | True | strategy_search_allowed_now=0 | 0 | hard |
| P304_EXTERNAL_ROWS_STILL_REQUIRED | True | 0 | 0 | hard |
| P304_FULL_DEPTH_JOIN_REQUIREMENT_RETAINED | True | 1 | 1 | hard |

Next action: `populate_event_catalyst_dropzone_then_run_phase305_event_catalyst_source_import_audit`.
