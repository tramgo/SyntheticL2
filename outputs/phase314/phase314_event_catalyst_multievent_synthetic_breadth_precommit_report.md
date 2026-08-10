# Phase314 Event-Catalyst Multi-Event Synthetic Breadth Precommit

Phase314 precommits the synthetic multi-event breadth expansion selected by Phase313.
It does not generate events, run joins, replay strategies, promote strategies, or claim deployable profitability.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase314_multievent_breadth_precommit_complete | 1 | Phase314 multi-event synthetic breadth precommit completed |
| phase314_breadth_contract_rows | 10 | Breadth contract rows |
| phase314_generation_work_order_rows | 6 | Generation work-order rows |
| phase314_control_rows | 8 | Control rows |
| phase314_min_synthetic_event_dates | 10 | Minimum synthetic event dates for next materialization |
| phase314_min_symbols_per_event | 32 | Minimum symbol universe target per event |
| phase314_full_depth_required | 1 | Full top-five market-by-price depth required |
| phase314_depth_beyond_l1_required | 1 | Levels 2-5 materiality required |
| phase314_replay_allowed | 0 | No replay |
| phase314_strategy_promotion_allowed | 0 | No promotion |
| phase314_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase314_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase314_hard_gate_pass_rows | 7 | Passed hard gates |
| phase314_hard_gate_rows | 7 | Hard gates |
| phase314_next_best_action | run_phase315_event_catalyst_multievent_synthetic_breadth_materialization_no_replay | Recommended next action |

## Breadth contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P314_MIN_SYNTHETIC_EVENT_DATES | >=10 | Generate at least 10 synthetic event dates before rerunning event-catalyst search. |
| P314_MIN_SYMBOLS_PER_EVENT | 32 | Each synthetic event should cover the 32-symbol universe when dense rows exist. |
| P314_SOURCE_CLOCK_POLICY | discover_from_dense_row_level_or_row_group_coverage | Do not assume NSE-clock-normal rows; choose timestamps from actual dense coverage. |
| P314_EVENT_WINDOW_SECONDS | pre=900;post=1800 | Preserve Phase306/307 event window for comparability. |
| P314_EVENT_TYPE_POLICY | synthetic_calendar_rbi_policy_like | Synthetic-calendar events are catalyst timestamps only, not real RBI dates. |
| P314_TRAINING_ONLY_POLICY | no_replay_no_promotion_no_paper_live | Breadth expansion is still synthetic-only training research. |
| P314_FULL_DEPTH_POLICY | levels_1_to_5_required | Every generated event must retain full top-five market-by-price depth. |
| P314_L2_L5_MATERIALITY_POLICY | required | The next search must preserve depth-beyond-L1 features. |
| P314_ACCEPTANCE_FLOOR_FOR_FUTURE | >=10_events_now;>=30_trades_for_candidate_interpretation | Increase breadth before interpreting annualized leads. |
| P314_NEXT | run_phase315_event_catalyst_multievent_synthetic_breadth_materialization_no_replay | Materialize the multi-event synthetic event ledger and rerun join/features/search pipeline. |

## Generation work order

| work_order_id | scope | description |
| --- | --- | --- |
| event_timestamp_discovery | raw_synthetic_l2_dense_full_year | Discover candidate timestamps from dense parquet metadata and row-level samples. |
| cross_symbol_overlap | 32_symbol_universe | Keep event timestamps that have broad symbol coverage for the same event window. |
| event_spacing | prefer_distinct_synthetic_dates_and_nonoverlapping_windows | Avoid near-duplicate adjacent windows. |
| calendar_labeling | synthetic_calendar_event_id | Label generated rows as synthetic-calendar events, not real-world events. |
| phase315_outputs | event_sources/event_catalysts/generated/phase315_multievent_synthetic_calendar.csv | Write generated event ledger separately from verified external event sources. |
| phase316_join | rerun_event_catalyst_join_for_multievent_ledger | Join multi-event ledger to top-five depth before feature/search rerun. |

## Controls

| control_id | control_status | description |
| --- | --- | --- |
| real_event_date_claim | forbidden | Synthetic-calendar rows must not be described as real-world RBI/news dates. |
| directional_event_label | forbidden | Event rows provide timing only; no bullish/bearish truth label. |
| l1_only_candidate | forbidden | Full-depth branch cannot collapse to L1-only. |
| unlimited_capital_return | forbidden | Future annualized return must retain fixed-capital denominator. |
| paper_live_acceptance | forbidden | No paper/live claim from synthetic breadth expansion. |
| deployable_profitability_claim | forbidden | No deployable claim until independent breadth and acceptance gates exist. |
| zerodha_cost_stress | required | Future search keeps Zerodha cost model and stress profiles. |
| sparse_annualized_label | required | Annualized >12% remains a sparse research lead until breadth gates pass. |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P314_PHASE313_COMPLETE | True | 1 | 1 | hard |
| P314_PHASE313_ROUTE_SELECTED | True | P314_EVENT_CATALYST_MULTIEVENT_SYNTHETIC_BREADTH_PRECOMMIT | P314 selected | hard |
| P314_CONTRACT_ROWS_PRESENT | True | 10 | >=10 | hard |
| P314_WORK_ORDER_ROWS_PRESENT | True | 6 | >=6 | hard |
| P314_CONTROLS_PRESENT | True | 8 | >=8 | hard |
| P314_NO_REPLAY_PROMOTION_OR_PAPER_LIVE | True | replay=0;promotion=0;paper=0 | all_zero | hard |
| P314_PROFITABILITY_CLAIM_CLOSED | True | 0 | 0 | hard |
