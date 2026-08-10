# Phase324 Event-Catalyst Breadth Expansion Precommit

Phase324 precommits the event-breadth expansion needed after Phase323 found profitable but sparse fixed-capital research leads.
It does not materialize rows, join depth, run strategy search, replay, promote, or claim profitability.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase324_breadth_expansion_precommit_complete | 1 | Phase324 event-catalyst breadth expansion precommit completed |
| phase324_target_event_rows | 50 | Preferred total event rows for Phase325 |
| phase324_minimum_event_rows | 40 | Minimum total event rows for Phase325 |
| phase324_robust_event_floor | 30 | Robustness floor from Phase323 interpretation |
| phase324_min_symbols_per_event | 32 | Minimum symbols per event |
| phase324_contract_rows | 18 | Expansion contract rows |
| phase324_work_order_rows | 8 | Phase325 work-order rows |
| phase324_full_depth_required | 1 | Depth levels 1-5 required |
| phase324_depth_beyond_l1_required | 1 | Depth levels 2-5 materiality required |
| phase324_l1_only_candidate_allowed | 0 | No L1-only candidate path |
| phase324_fixed_capital_required | 1 | Fixed capital denominator required |
| phase324_cost200_required | 1 | 2x cost stress required |
| phase324_strategy_replay_allowed | 0 | No replay |
| phase324_strategy_promotion_allowed | 0 | No promotion |
| phase324_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase324_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase324_hard_gate_pass_rows | 9 | Passed hard gates |
| phase324_hard_gate_rows | 9 | Hard gates |
| phase324_next_best_action | run_phase325_event_catalyst_breadth_expansion_materialization_no_replay | Recommended next action |

## Breadth expansion contract

| contract_id | contract_value | description |
| --- | --- | --- |
| selected_route | P324_EVENT_CATALYST_BREADTH_EXPANSION_PRECOMMIT | Expand the event-catalyst universe before further acceptance decisions. |
| preserved_strategy_family | P321_DEPTH_ACCEL_REVERSAL | Carry forward the Phase323 best full-depth clue. |
| target_event_rows | 50 | Preferred total synthetic catalyst events for Phase325. |
| minimum_event_rows | 40 | Minimum total synthetic catalyst events before Phase326 join/materialization. |
| robust_event_floor | 30 | Acceptance floor that Phase322 could not satisfy. |
| minimum_symbols_per_event | 32 | Preserve full 32-symbol universe per event. |
| window_seconds | pre=900;post=1800 | Use the same event-relative window as Phase317/320. |
| source_root | raw_synthetic_l2_dense_full_year | Use the existing full-year dense top-five book-state source. |
| candidate_selection | row_level_dense_buckets_distinct_dates | Avoid row-group midpoint false positives; use dense row-level buckets. |
| full_depth_required | depth_levels_1_to_5 | Preserve top-five market-by-price depth. |
| depth_beyond_l1_required | depth_levels_2_to_5_material | No L1-only candidate path. |
| cost_model_preserved | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Future search must keep documented Zerodha costs. |
| fixed_capital_required | required | No unlimited-capital annualized return. |
| cost200_required | required | Keep 2x cost-stress scoring. |
| target_live_separation | required | target_ fields stay outcomes, not live signals. |
| net_edge_live_mask | forbidden | No lookahead live mask. |
| phase324_execution_now | precommit_only | Do not materialize new joins in Phase324. |
| boundaries | replay=0;promotion=0;paper=0;claim=0 | No boundary change. |

## Phase325 work order

| work_order_id | scope | description |
| --- | --- | --- |
| discover_dense_source_inventory | raw_synthetic_l2_dense_full_year/trade_month=*/symbol=*/part-*.parquet | Inventory available synthetic top-five depth files. |
| select_row_level_dense_buckets | reference_symbol=HDFCBANK; distinct_event_dates; target=50; minimum=40 | Select actual dense row-level windows, not only file metadata. |
| validate_symbol_coverage | symbols_per_event>=32 | Reject events missing full symbol breadth. |
| write_expanded_event_ledger | event_sources/event_catalysts/generated/phase325_expanded_synthetic_events.csv | Materialize expanded event ledger. |
| write_expanded_work_order | outputs/phase325/phase325_event_symbol_work_order.csv | Create event-symbol join work order. |
| preserve_phase323_family_seed | P321_DEPTH_ACCEL_REVERSAL | Carry preserved strategy clue into later search, without optimizing on future labels. |
| run_quality_gates | event_rows>=40;symbols=32;depth=top5;no_replay | Gate Phase325 before any join/search. |
| next_join_precommit | run_phase326_event_catalyst_expanded_top5_depth_join_precommit_no_replay | Prepare expanded top-five-depth join after breadth is materialized. |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P324_PHASE323_COMPLETE | True | 1 | 1 | hard |
| P324_RESEARCH_LEAD_PRESENT | True | 1 | 1 | hard |
| P324_ACCEPTANCE_NOT_ALREADY_OPEN | True | 0 | 0 | hard |
| P324_CURRENT_BREADTH_BELOW_FLOOR | True | 10 | <30 | hard |
| P324_EXPANDED_BREADTH_TARGET_EXCEEDS_FLOOR | True | 40 | >=30 | hard |
| P324_CONTRACT_ROWS_PRESENT | True | 18 | >=18 | hard |
| P324_WORK_ORDER_ROWS_PRESENT | True | 8 | >=8 | hard |
| P324_DEPTH_AND_COST_BOUNDARIES_PRESENT | True | present | present | hard |
| P324_NO_REPLAY_PROMOTION_OR_PAPER_LIVE | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |

