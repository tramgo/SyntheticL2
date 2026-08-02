# Phase263 Passive Opportunity Breadth and Fill-model Interpretation

Generated UTC: 2026-08-02T01:58:51.601108+00:00

Phase263 interprets the Phase262 broadened passive opportunity/fill-model training search.
It closes the repaired passive spread-capture/fill-model route for promotion because no variants survived breadth, cost-stress and control gates.
It preserves the core Zerodha top-five depth objective and selects a materially different full-depth liquidity-shock/absorption event route for Phase264.
This is not replay execution, strategy promotion, paper/live acceptance or a deployable profitability claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase263_interpretation_complete | 1 | Phase263 passive opportunity/fill-model interpretation completed |
| phase263_phase262_variant_rows | 2592 | Phase262 variants interpreted |
| phase263_phase262_full_depth_variant_rows | 2592 | Full-depth variants interpreted |
| phase263_phase262_l2_l5_variant_rows | 2592 | Levels 2-5 variants interpreted |
| phase263_phase262_l1_only_variant_rows | 0 | L1-only variants interpreted |
| phase263_phase262_cost100_positive_variant_rows | 5 | Phase262 variants positive at base charges |
| phase263_phase262_cost200_positive_variant_rows | 0 | Phase262 variants positive at 2x charges |
| phase263_phase262_survivor_candidate_rows | 0 | Phase262 survivors |
| phase263_phase262_best_cost100_expected_net_pnl_inr | -17.14255650345248 | Best Phase262 1x expected net P&L |
| phase263_phase262_best_cost200_expected_net_pnl_inr | -55.442989223856685 | Best Phase262 2x expected net P&L |
| phase263_close_phase262_for_promotion | 1 | Close Phase262 candidates for promotion |
| phase263_close_passive_spread_capture_fill_model_route | 1 | Close repaired passive route for now |
| phase263_full_top_five_depth_preserved | 1 | Preserve full top-five depth |
| phase263_threshold_relaxation_only_allowed | 0 | Threshold relaxation only remains forbidden |
| phase263_selected_next_route | P263_FULL_DEPTH_LIQUIDITY_SHOCK_ABSORPTION_EVENT_PRECOMMIT | Selected next route |
| phase263_next_route_contract_rows | 7 | Next route contract rows |
| phase263_hard_gate_pass_rows | 8 | Hard gates passed |
| phase263_hard_gate_rows | 8 | Hard gates evaluated |
| phase263_download_more_dates_now_allowed | 0 | No new download in Phase263 |
| phase263_replay_execution_allowed_now | 0 | No replay execution in Phase263 |
| phase263_strategy_promotion_allowed | 0 | No strategy promotion from Phase263 |
| phase263_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase263 |
| phase263_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase263 |
| phase263_next_best_action | run_phase264_full_depth_liquidity_shock_absorption_event_precommit_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P263_PHASE262_WORK_ORDER_PRESENT | True | run_phase263_passive_opportunity_breadth_fill_model_interpretation_no_paper_live | Phase262 next action targets Phase263 | hard |
| P263_PHASE262_SEARCH_EXECUTED | True | summary=2592;rows=2592 | Phase262 variants present | hard |
| P263_NO_SURVIVOR_RECOGNIZED | True | 0 | 0 Phase262 survivors | hard |
| P263_NO_2X_COST_POSITIVE_RECOGNIZED | True | 0 | 0 variants positive at 2x costs | hard |
| P263_FULL_DEPTH_PRESERVED | True | full_depth=2592;l2_l5=2592;l1_only=0;variants=2592 | all variants full-depth and no L1-only | hard |
| P263_PASSIVE_ROUTE_CLOSED | True | 1 | passive route closed for now | hard |
| P263_NEXT_ROUTE_SELECTED | True | P263_FULL_DEPTH_LIQUIDITY_SHOCK_ABSORPTION_EVENT_PRECOMMIT | Phase264 next route contract written | hard |
| P263_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE | True | 0 | 0 | hard |

## Failure Mode Ledger

| failure_mode | evidence | severity | closed_or_requires_repair |
| --- | --- | --- | --- |
| cost_stress_failure | positive_1x=5; positive_1p5=0; positive_2x=0; best_2x=-55.442989223856685 | hard | 1 |
| no_survivor_after_full_control_stack | survivors=0 | hard | 1 |
| best_ranked_candidate_negative_even_at_base_cost | best_1x=-17.14255650345248; best_2x=-55.442989223856685 | hard | 1 |
| opportunity_and_fill_breadth_too_sparse | best_opportunities=5; best_symbols=4; best_fill_equivalent=0.4632302472678699 | hard | 1 |
| queue_and_nonfill_stress_not_survived | queue_surviving_variants=6; nonfill_surviving_variants=3 | hard | 0 |
| positive_base_edge_not_robust | positive_1x=5; nonzero_variants=2592; total_variants=2592 | medium | 1 |
| full_depth_surface_preserved_not_invalidated | full_depth=2592; l2_l5=2592; l1_only=0; variants=2592 | important_context | 1 |

## Decision Ledger

| decision_id | decision_value | evidence | description |
| --- | --- | --- | --- |
| close_phase262_for_promotion | 1 | survivors=0 | Do not promote Phase262 candidates |
| close_passive_spread_capture_fill_model_route | 1 | positive_1x=5; positive_2x=0; survivors=0 | The repaired passive spread-capture/fill-model route is closed for now |
| preserve_full_top_five_depth_surface | 1 | full_depth=2592; l2_l5=2592; l1_only=0; variants=2592 | Full top-five L2 depth remains mandatory |
| threshold_relaxation_only_allowed | 0 | two consecutive passive searches failed survivor/cost-stress gates | Do not continue by merely relaxing passive thresholds |
| materially_different_route_required | 1 | passive route failed after repair; full-depth signal surface still useful | Open a different mechanism rather than another passive spread-capture tweak |
| selected_next_route | P263_FULL_DEPTH_LIQUIDITY_SHOCK_ABSORPTION_EVENT_PRECOMMIT | full-depth liquidity shock / absorption event source | Next materially different action |

## Next Route Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P264_INPUT | outputs/phase254/phase254_richer_raw_top5_depth_event_bars.parquet | Use existing richer raw Zerodha top-five event bars; no new download required |
| P264_DEPTH_REQUIREMENT | levels_1_to_5_required_l2_l5_required | Use full top-five market-by-price rows 1-5 with explicit levels 2-5 features; L1-only variants forbidden |
| P264_ROUTE | full_depth_liquidity_shock_absorption_event_model | Move from passive spread capture to directional liquidity-shock/absorption events |
| P264_EVENT_FEATURES | replenishment;withdrawal;top5_churn;order_churn;l2_l5_imbalance;spread_compression_expansion;level_weighted_imbalance | Use depth dynamics rather than only static imbalance or bar return |
| P264_LABELS | future_mid_return_h3_h6_h10_cost_hurdled | Evaluate directional continuation/reversal labels after realistic Zerodha cost floors |
| P264_CONTROLS | random_side;side_flip;cost_stress;shuffle_label;event_breadth;no_l1_only | Controls required before any candidate can survive |
| P264_FORBIDDEN | paper_live_or_deployable_profitability_claim;threshold_relaxation_only | No paper/live acceptance, deployable profitability claim, or mere passive-threshold relaxation |
