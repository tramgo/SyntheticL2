# Phase257 Richer Raw Top-five Depth Strategy-search Interpretation

Generated UTC: 2026-07-29T11:03:34.633537+00:00

Phase257 interprets the Phase256 full-depth cost-aware taker strategy search.
It closes the current taker-threshold family after no survivor was found, while preserving the full Zerodha top-five depth surface as the core project input.
It selects a passive/queue-aware spread-capture precommit as the next materially different route.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase257_interpretation_complete | 1 | Phase257 strategy-search interpretation completed |
| phase257_phase256_variant_rows | 2376 | Phase256 variants interpreted |
| phase257_phase256_full_depth_variant_rows | 2376 | Full top-five depth variants interpreted |
| phase257_phase256_survivor_candidate_rows | 0 | Phase256 survivor candidates |
| phase257_phase256_cost100_positive_variant_rows | 0 | Phase256 variants positive at 1x cost |
| phase257_closed_taker_threshold_route | 1 | Close current taker-threshold route |
| phase257_full_top_five_depth_preserved | 1 | Preserve full top-five depth as core surface |
| phase257_threshold_relaxation_only_allowed | 0 | Do not continue by simple threshold relaxation |
| phase257_selected_next_route | P257_PASSIVE_QUEUE_AWARE_SPREAD_CAPTURE_PRECOMMIT | Selected materially different route |
| phase257_next_route_contract_rows | 7 | Next route contract rows |
| phase257_hard_gate_pass_rows | 7 | Hard gates passed |
| phase257_hard_gate_rows | 7 | Hard gates evaluated |
| phase257_download_more_dates_now_allowed | 0 | No new download in Phase257 |
| phase257_replay_execution_allowed_now | 0 | No replay execution in Phase257 |
| phase257_strategy_promotion_allowed | 0 | No strategy promotion from Phase257 |
| phase257_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase257 |
| phase257_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase257 |
| phase257_next_best_action | run_phase258_passive_queue_aware_spread_capture_precommit_full_top5_depth_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P257_PHASE256_WORK_ORDER_PRESENT | True | run_phase257_richer_raw_top5_depth_strategy_search_interpretation_no_paper_live | Phase256 next action targets Phase257 | hard |
| P257_PHASE256_SEARCH_EXECUTED | True | 2376 | >0 Phase256 variants available for interpretation | hard |
| P257_NO_SURVIVOR_RECOGNIZED | True | 0 | 0 Phase256 survivors | hard |
| P257_FULL_DEPTH_PRESERVED | True | 2376/2376 | all interpreted variants used full top-five depth | hard |
| P257_TAKER_BRANCH_CLOSED | True | 1 | close taker threshold route | hard |
| P257_NEXT_ROUTE_SELECTED | True | 1 | passive/queue-aware route contract written | hard |
| P257_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE | True | 0 | 0 | hard |

## Failure Mode Ledger

| failure_mode | evidence | severity | closed_by_phase257 |
| --- | --- | --- | --- |
| taker_cost_floor_dominates_gross_edge | best_cost100_net=-411.49029712563254; best_cost200_net=-1218.3826175402583; cost100_positive=0 | hard | 1 |
| no_cost_stress_survivor | survivor_candidate_rows=0 | hard | 1 |
| best_candidate_too_sparse_for_breadth | best_trade_rows=8; best_symbols=5 | medium | 1 |
| full_depth_signal_not_invalidated | Phase255 found healthy_full_depth_features=11/11 and max_abs_full_depth_ic=0.1475390528147801 | important_context | 0 |
| gross_edge_exists_but_is_insufficient | gross_positive_variants=1188; net_positive_variants=0 | important_context | 1 |

## Decision Ledger

| decision_id | decision_value | evidence | description |
| --- | --- | --- | --- |
| close_phase256_taker_threshold_search | 1 | variants=2376; survivors=0 | Close current taker-threshold search family |
| preserve_full_top_five_depth_surface | 1 | full_depth_rows=2376; variants=2376 | Keep levels 1-5 depth as core input |
| do_not_repeat_threshold_relaxation_only | 1 | cost100_positive=0 | Avoid simply relaxing thresholds on same taker model |
| cost_dominance_confirmed | 1 | max_gross=14361.504711738551; max_cost=45592.94635115765; median_cost=11442.96794243862 | Costs dominate the searched gross edge |
| selected_next_route | P257_PASSIVE_QUEUE_AWARE_SPREAD_CAPTURE_PRECOMMIT | passive/queue-aware route | Next materially different route |

## Next Route Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P258_INPUT | outputs/phase254/phase254_richer_raw_top5_depth_event_bars.parquet | Use existing compact raw top-five depth event bars; no new download required |
| P258_DEPTH_REQUIREMENT | levels_1_to_5_required | Use full Zerodha top-five market-by-price book; no L1-only candidate is allowed |
| P258_ORDER_MODEL | passive_queue_aware_limit_order_proxy | Model quote placement, queue adversity, cancel/replace pressure and non-fill risk |
| P258_EDGE_SOURCE | spread_capture_minus_adverse_selection | Shift from taker edge to passive spread capture and adverse-selection controls |
| P258_COST_MODEL | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Carry modeled Zerodha charges; passive fill still pays statutory/brokerage cost stack |
| P258_CONTROLS | random_side;side_flip;cost_stress;queue_adversity | Controls must remain active before any promotion |
| P258_FORBIDDEN | paper_live_or_deployable_profitability_claim | No paper/live acceptance or deployable profitability claim from Phase257/P258 precommit |
