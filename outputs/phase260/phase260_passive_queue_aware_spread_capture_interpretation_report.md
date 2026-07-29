# Phase260 Passive Queue-aware Spread-capture Interpretation

Generated UTC: 2026-07-29T11:23:48.444859+00:00

Phase260 interprets the Phase259 passive/queue-aware training search.
It closes Phase259 candidates for promotion because there are no survivors, but keeps the full-depth passive route open for one repair/broaden precommit because sparse base-charge edge exists.
It does not download data, run replay execution, promote a strategy, open paper/live acceptance or claim deployable profitability.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase260_interpretation_complete | 1 | Phase260 passive search interpretation completed |
| phase260_phase259_variant_rows | 3888 | Phase259 variants interpreted |
| phase260_phase259_full_depth_variant_rows | 3888 | Full-depth variants interpreted |
| phase260_phase259_cost100_positive_variant_rows | 6 | Phase259 variants positive at base charges |
| phase260_phase259_cost200_positive_variant_rows | 0 | Phase259 variants positive at 2x charges |
| phase260_phase259_survivor_candidate_rows | 0 | Phase259 survivors |
| phase260_phase259_best_opportunity_rows | 1 | Best Phase259 opportunity rows |
| phase260_close_phase259_for_promotion | 1 | Close Phase259 candidates for promotion |
| phase260_full_passive_route_closed | 0 | Do not fully close passive route yet |
| phase260_full_top_five_depth_preserved | 1 | Preserve full top-five depth |
| phase260_selected_next_route | P260_PASSIVE_OPPORTUNITY_BREADTH_AND_FILL_MODEL_REPAIR_PRECOMMIT | Selected next route |
| phase260_next_route_contract_rows | 7 | Next route contract rows |
| phase260_hard_gate_pass_rows | 7 | Hard gates passed |
| phase260_hard_gate_rows | 7 | Hard gates evaluated |
| phase260_download_more_dates_now_allowed | 0 | No new download in Phase260 |
| phase260_replay_execution_allowed_now | 0 | No replay execution in Phase260 |
| phase260_strategy_promotion_allowed | 0 | No strategy promotion from Phase260 |
| phase260_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase260 |
| phase260_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase260 |
| phase260_next_best_action | run_phase261_passive_opportunity_breadth_fill_model_repair_precommit_full_top5_depth_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P260_PHASE259_WORK_ORDER_PRESENT | True | run_phase260_passive_queue_aware_spread_capture_interpretation_no_paper_live | Phase259 next action targets Phase260 | hard |
| P260_PHASE259_SEARCH_EXECUTED | True | 3888 | >0 Phase259 variants | hard |
| P260_NO_SURVIVOR_RECOGNIZED | True | 0 | 0 Phase259 survivors | hard |
| P260_FULL_DEPTH_PRESERVED | True | 3888/3888 | all interpreted variants used full top-five depth | hard |
| P260_PROMOTION_CLOSED | True | 1 | no promotion from Phase259 | hard |
| P260_NEXT_ROUTE_SELECTED | True | P260_PASSIVE_OPPORTUNITY_BREADTH_AND_FILL_MODEL_REPAIR_PRECOMMIT | repair/broaden contract written | hard |
| P260_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE | True | 0 | 0 | hard |

## Failure Mode Ledger

| failure_mode | evidence | severity | closed_or_requires_repair |
| --- | --- | --- | --- |
| base_charge_edge_sparse | positive_1x=6; best_1x=7.249843402049745; best_opportunities=1; best_symbols=1 | hard | 1 |
| cost_stress_failure | positive_1p5=0; positive_2x=0; best_2x=-75.43135659795024 | hard | 1 |
| no_survivor_after_controls | survivors=0 | hard | 1 |
| opportunity_surface_too_sparse | nonzero_variant_rows=3096; total_variants=3888 | medium | 0 |
| full_depth_route_not_invalidated | all Phase259 variants used full top-five depth and levels 2-5 | important_context | 0 |

## Decision Ledger

| decision_id | decision_value | evidence | description |
| --- | --- | --- | --- |
| close_first_passive_search_for_promotion | 1 | survivors=0 | Do not promote Phase259 candidates |
| do_not_close_full_passive_route_yet | 1 | positive_1x=6; positive_2x=0 | Sparse base edge justifies one repair/broaden pass |
| preserve_full_top_five_depth_surface | 1 | full_depth=3888; variants=3888 | Full top-five depth remains mandatory |
| repair_opportunity_breadth_required | 1 | best opportunity and symbol breadth are too small | Broaden passive opportunity surface before next search |
| repair_fill_model_required | 1 | fill-equivalent rows are too sparse | Separate opportunity generation from fill-probability model |
| selected_next_route | P260_PASSIVE_OPPORTUNITY_BREADTH_AND_FILL_MODEL_REPAIR_PRECOMMIT | passive repair/broaden route | Next materially different action |

## Next Route Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P261_INPUT | outputs/phase254/phase254_richer_raw_top5_depth_event_bars.parquet | Use existing compact raw top-five depth event bars; no new download required |
| P261_DEPTH_REQUIREMENT | levels_1_to_5_required | Use full Zerodha top-five market-by-price book; L1-only candidates remain forbidden |
| P261_REPAIR_1 | separate_opportunity_filter_from_fill_probability | Avoid filtering away most passive opportunities before fill model scores them |
| P261_REPAIR_2 | calibrate_fill_probability_grid | Search conservative fill haircuts and non-fill rates rather than one fixed formula |
| P261_REPAIR_3 | broaden_spread_and_replenishment_thresholds | Broaden opportunity count while retaining queue-adversity controls |
| P261_CONTROLS | random_side;side_flip;cost_stress;queue_adversity;nonfill_stress | Controls required before any candidate can survive |
| P261_FORBIDDEN | paper_live_or_deployable_profitability_claim | No paper/live acceptance or deployable profitability claim |
