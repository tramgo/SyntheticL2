# Phase302 Terminal Retail Top-Five Depth Alpha Thesis Report

Phase302 closes the tested retail directional top-five market-by-price depth alpha route for acceptance.

This is a scope-specific closure, not a claim that all top-five depth data is useless. The closed scope is the Phase298-Phase301 route: directional signals derived from raw tick-level top-five market-by-price book state, then rescued with passive-aware execution, Zerodha-style cost200 stress, fixed initial capital, queue/adverse-selection penalties, and forced flattening.

## Verdict

| metric | value | description |
| --- | --- | --- |
| phase302_selected_verdict | P302_RETAIL_TOP5_L2_ALPHA_THESIS_CLOSED_FOR_ACCEPTANCE | Selected terminal verdict |
| phase302_closed_scope | retail_directional_top_five_market_by_price_depth_alpha_with_passive_aware_rescue | Closed scope |
| phase302_phase300_cost200_acceptance_survivor_rows | 0 | Cost200 acceptance survivors |
| phase302_phase300_kill_switch_triggered | 1 | Phase300 kill switch |
| phase302_material_new_source_or_thesis_required | 1 | Required before continuing |
| phase302_next_best_action | do_not_continue_retail_top5_l2_alpha_rescue_without_material_new_source_or_thesis | Recommended next action |

## Evidence chain

| phase | evidence_role | key_observation | acceptance_read |
| --- | --- | --- | --- |
| 298 | raw_top_five_market_by_price_depth_strategy_sweep | raw_events=9596; variants=576; scenarios=1152; best_annualized=382.9973530062694; best_events=3 | Sparse directional clues preserved; direct acceptance closed. |
| 299 | raw_dense_sweep_interpretation_and_passive_route_selection | directional_signal_seeds=16; above12_below_30_events=9; passive_fill_required=1; profitability_claim_allowed=0 | Only seed-level continuation allowed; no profitability claim. |
| 300 | passive_aware_execution_hybrid_with_cost200_and_fixed_capital | scenarios=108; above12=17; event_floor=0; breadth=0; survivors=0; kill_switch=1 | Passive-aware rescue failed acceptance; sparse pockets remain diagnostic only. |
| 301 | interpretation_and_kill_switch_audit | selected_outcome=P301_PASSIVE_AWARE_EXECUTION_FALSIFIED; terminal_report_required=1; kill_switch_rows=7; do_not_rescue=1 | Route is closed and must be reported as terminal for acceptance. |

## Durable by-products

| byproduct_id | classification | kept_for | not_kept_for |
| --- | --- | --- | --- |
| P302_RAW_DENSE_TOP5_BOOK_STATE_LAKE | reusable_infrastructure | future material-new thesis work requiring tick-level top-five market-by-price depth | rescuing the closed retail directional route |
| P302_ZERODHA_COST200_MODEL | reusable_cost_model | all future India NSE intraday tests using zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | weakening costs to create a survivor |
| P302_PASSIVE_BACK_OF_QUEUE_FILL_HARNESS | reusable_execution_model | future limit-order experiments where passive fills are explicitly modeled | assuming all passive orders fill at touch |
| P302_ADVERSE_SELECTION_AND_FORCED_FLATTEN_AUDIT | reusable_realism_guard | detecting fragile maker-like edge that disappears after fill realism | adding guardrails after results to hide losses |
| P302_NEGATIVE_EVIDENCE_LEDGER | research_memory | preventing repeated shard-by-shard searches of the same falsified route | claiming full-depth L2 can never contain alpha |

## Closure decisions

| decision_id | decision_value | evidence | decision_status |
| --- | --- | --- | --- |
| selected_terminal_verdict | P302_RETAIL_TOP5_L2_ALPHA_THESIS_CLOSED_FOR_ACCEPTANCE | Phase300/301 evidence has no acceptance survivor. | close_tested_route |
| closed_scope | retail_directional_top_five_market_by_price_depth_alpha_with_passive_aware_rescue | Scope is narrower than all possible L2 research. | scope_boundary |
| close_for_acceptance | 1 | survivors=0 | closed |
| close_for_replay_or_promotion | 1 | replay=0;promotion=0;paper_live=0;profitability_claim=0 | closed |
| do_not_continue_with_more_filters | 1 | phase301_do_not_rescue=1 | closed |
| best_sparse_pocket_preserved | P300_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-01_Q99_DL3_H6_P300_FILL_OPTIMISTIC_BACK_OF_QUEUE_P300_PASSIVE_ENTRY_PASSIVE_EXIT_FORCED_FLATTEN_CAP1000000_NOT75000_CONC4_COST200 | ann=287.9689503602893;events=2 | diagnostic_only |
| broadest_case_preserved | P300_ALL_PHASE299_SEEDS_P300_FILL_BASE_BACK_OF_QUEUE_P300_PASSIVE_ENTRY_PASSIVE_EXIT_FORCED_FLATTEN_CAP1000000_NOT75000_CONC4_COST200 | ann=8.230380462356296;events=26 | diagnostic_only |
| material_new_source_or_thesis_required | 1 | same-route rescue is closed | required |
| next_best_action | do_not_continue_retail_top5_l2_alpha_rescue_without_material_new_source_or_thesis | terminal report complete | next |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P302_PHASE301_TERMINAL_REQUIRED | True | 1 | 1 | hard |
| P302_PHASE300_NO_ACCEPTANCE_SURVIVOR | True | 0 | 0 | hard |
| P302_PHASE300_KILL_SWITCH_FIRED | True | 1 | 1 | hard |
| P302_SCENARIOS_AUDITED | True | 108 | >0 | hard |
| P302_EVIDENCE_CHAIN_PRESENT | True | 4 | 4 | hard |
| P302_BYPRODUCTS_CATALOGED | True | 5 | >=5 | hard |
| P302_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |
| P302_TERMINAL_DECISION_PRESENT | True | P302_RETAIL_TOP5_L2_ALPHA_THESIS_CLOSED_FOR_ACCEPTANCE | P302_RETAIL_TOP5_L2_ALPHA_THESIS_CLOSED_FOR_ACCEPTANCE | hard |
| P302_MATERIAL_NEW_REQUIREMENT_PRESENT | True | 1 | 1 | hard |
| P302_NEXT_ACTION_PRESENT | True | do_not_continue_retail_top5_l2_alpha_rescue_without_material_new_source_or_thesis | do_not_continue_retail_top5_l2_alpha_rescue_without_material_new_source_or_thesis | hard |

## Boundary

No replay, promotion, paper/live acceptance, or deployable profitability claim is opened by this report. Sparse annualized pockets are preserved as diagnostic clues only.
