# Phase303 Material-New Thesis and Source Selector

Phase303 responds to Phase302's terminal closure by selecting only a genuinely material-new path. It does not reopen the closed retail directional top-five depth rescue route.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase303_material_new_selector_complete | 1 | Phase303 material-new thesis/source selector completed |
| phase303_selected_route | P303_EXTERNAL_EVENT_CATALYST_PLUS_L2_RESPONSE_SOURCE_ACQUISITION | Selected route |
| phase303_candidate_rows | 5 | Candidate routes evaluated |
| phase303_rejected_same_route_rows | 1 | Same-route candidates rejected |
| phase303_selected_requires_external_source | 1 | Selected route requires new external source |
| phase303_selected_uses_top_five_depth_levels_1_to_5 | 1 | Selected route keeps top-five market-by-price levels 1-5 |
| phase303_work_order_rows | 5 | Work-order rows emitted |
| phase303_strategy_search_allowed_now | 0 | No strategy search until the new source exists |
| phase303_strategy_replay_allowed | 0 | No replay |
| phase303_strategy_promotion_allowed | 0 | No promotion |
| phase303_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase303_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase303_hard_gate_pass_rows | 8 | Passed hard gates |
| phase303_hard_gate_rows | 8 | Hard gates |
| phase303_next_best_action | acquire_or_build_material_new_event_catalyst_source_before_any_new_l2_strategy_search | Recommended next action |

## Candidate catalog

| candidate_id | candidate_type | material_new_source | material_new_thesis | uses_top_five_depth_levels_1_to_5 | requires_external_data | reason | decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P303_SAME_DIRECTIONAL_TOP5_RESCUE | rejected_same_route | 0 | 0 | 1 | 0 | Only changes filters/execution around the Phase298-302 closed route. | reject |
| P303_TWO_SIDED_RETAIL_MARKET_MAKING | rejected_scope | 0 | 1 | 1 | 0 | Retail has no maker rebate, weak queue priority and slow cancels; prior charter excludes live market-making. | reject_for_live_acceptance |
| P303_EXTERNAL_EVENT_CATALYST_PLUS_L2_RESPONSE | material_new_source_and_thesis | 1 | 1 | 1 | 1 | Adds exogenous event/news/calendar state before interpreting L2 response; not a same-signal rescue. | select |
| P303_BROKER_FILL_CONTRACT_NOTE_RECONCILIATION | material_new_execution_source | 1 | 0 | 0 | 1 | Would validate execution economics, but user stated Zerodha fills/contract notes are unavailable. | defer_until_available |
| P303_DERIVATIVES_OR_INDEX_FUTURES_LEAD_SOURCE | material_new_cross_market_source | 1 | 1 | 1 | 1 | Adds a cross-market lead source; useful if futures/options/index feed can be acquired. | candidate_after_event_catalyst |

## Work order

| work_order_id | action | selected_candidate_id | deliverable |
| --- | --- | --- | --- |
| P303_WO_01 | define_event_source_schema | P303_EXTERNAL_EVENT_CATALYST_PLUS_L2_RESPONSE | event_time_ist,event_type,symbol_scope,index_scope,source_url_or_file,confidence,embargo_safe_flag |
| P303_WO_02 | create_or_import_event_calendar | P303_EXTERNAL_EVENT_CATALYST_PLUS_L2_RESPONSE | No strategy search until at least one event source file exists. |
| P303_WO_03 | join_events_to_top5_depth_response | P303_EXTERNAL_EVENT_CATALYST_PLUS_L2_RESPONSE | Use tick-level top-five market-by-price levels 1-5 before/after event time. |
| P303_WO_04 | precommit_acceptance_gates | P303_EXTERNAL_EVENT_CATALYST_PLUS_L2_RESPONSE | Fixed capital, Zerodha cost200, event/breadth floors, no paper/live/profitability claim. |
| P303_WO_05 | run_only_after_source_exists | P303_EXTERNAL_EVENT_CATALYST_PLUS_L2_RESPONSE | Do not mine Phase302-closed same-route filters while waiting for source. |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P303_PHASE302_TERMINAL_COMPLETE | True | 1 | 1 | hard |
| P303_PHASE302_MATERIAL_NEW_REQUIRED | True | 1 | 1 | hard |
| P303_SAME_ROUTE_REJECTED | True | 1 | 1 | hard |
| P303_SELECTED_ROUTE_IS_MATERIAL_NEW | True | 1 | 1 | hard |
| P303_FULL_DEPTH_RETAINED | True | 1 | 1 | hard |
| P303_EXTERNAL_SOURCE_REQUIREMENT_EXPLICIT | True | 1 | 1 | hard |
| P303_WORK_ORDER_PRESENT | True | 5 | >=5 | hard |
| P303_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: no strategy search, replay, promotion, paper/live acceptance or profitability claim is opened until the new event-catalyst source exists and is joined to tick-level top-five market-by-price depth levels 1-5.
