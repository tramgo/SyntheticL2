# Phase269 Full-depth Liquidity-shock Two-lane Training Interpretation

Generated UTC: 2026-08-02T02:44:31.886159+00:00

Phase269 interprets Phase268 after adding the fixed-notional annualized-return research lens.
It preserves profitable exploratory leads, but explicitly refuses to treat fixed-notional annualization as portfolio annual return.
The next step is a capital/concurrency/capacity return precommit, while full Zerodha top-five rows 1-5 and levels 2-5 remain mandatory.
This is not replay execution, strategy promotion, paper/live acceptance, or a deployable profitability claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase269_interpretation_complete | 1 | Phase269 two-lane training interpretation completed |
| phase269_phase268_variant_rows | 1200 | Phase268 variants interpreted |
| phase269_phase268_full_depth_variant_rows | 1200 | Full-depth variants interpreted |
| phase269_phase268_l2_l5_variant_rows | 1200 | Levels 2-5 variants interpreted |
| phase269_phase268_l1_only_variant_rows | 0 | L1-only variants interpreted |
| phase269_phase268_exploratory_candidate_rows | 22 | Exploratory candidates |
| phase269_phase268_annualized_profitable_research_lead_rows | 17 | Fixed-notional annualized 1x research leads |
| phase269_phase268_cost200_annualized_profitable_research_lead_rows | 0 | Fixed-notional annualized 2x research leads |
| phase269_phase268_acceptance_grade_candidate_rows | 0 | Acceptance-grade candidates |
| phase269_annualization_notional_inr | 100000.0 | Fixed notional denominator |
| phase269_annualization_formula | net_pnl_inr / 100000 * 252 | Annualization formula |
| phase269_annualization_is_portfolio_return | 0 | Annualization is portfolio return flag |
| phase269_best_research_lead_candidate_id | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | Top fixed-notional annualized research lead |
| phase269_best_research_lead_family_id | P268_BID_ABSORPTION_BREADTH_REPAIR | Top lead family |
| phase269_best_research_lead_cost100_annualized_return_pct | 197.073 | Top lead 1x annualized proxy |
| phase269_best_research_lead_cost200_annualized_return_pct | 9.55202 | Top lead 2x annualized proxy |
| phase269_best_research_lead_events | 9 | Top lead event rows |
| phase269_best_research_lead_symbols | 4 | Top lead symbols |
| phase269_best_research_lead_shuffle_margin_inr | 0 | Top lead shuffled-label margin |
| phase269_preserve_research_leads | 1 | Preserve research leads |
| phase269_do_not_claim_portfolio_annual_return | 1 | Do not claim portfolio annual return |
| phase269_do_not_promote_or_replay_phase268 | 1 | Do not promote/replay Phase268 |
| phase269_selected_next_route | P269_FIXED_CAPITAL_CONCURRENCY_AND_CAPACITY_RETURN_PRECOMMIT | Selected next route |
| phase269_next_route_contract_rows | 7 | Next route contract rows |
| phase269_hard_gate_pass_rows | 8 | Hard gates passed |
| phase269_hard_gate_rows | 8 | Hard gates evaluated |
| phase269_download_more_dates_now_allowed | 0 | No new download in Phase269 |
| phase269_replay_execution_allowed_now | 0 | No replay execution in Phase269 |
| phase269_strategy_promotion_allowed | 0 | No strategy promotion from Phase269 |
| phase269_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase269 |
| phase269_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase269 |
| phase269_next_best_action | run_phase270_fixed_capital_concurrency_and_capacity_return_precommit_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P269_PHASE268_WORK_ORDER_PRESENT | True | run_phase269_full_depth_liquidity_shock_two_lane_training_interpretation_no_paper_live | Phase268 next action targets Phase269 | hard |
| P269_PHASE268_SEARCH_EXECUTED | True | summary=1200;rows=1200 | Phase268 variants present | hard |
| P269_FULL_DEPTH_RECOGNIZED | True | full_depth=1200;l2_l5=1200;l1_only=0;variants=1200 | all variants full-depth and no L1-only | hard |
| P269_RESEARCH_LEADS_RANKED | True | 17 | all annualized research leads ranked | hard |
| P269_ANNUALIZATION_NOT_PORTFOLIO_RECOGNIZED | True | 0 | annualized proxy is not portfolio return | hard |
| P269_NO_ACCEPTANCE_RECOGNIZED | True | 0 | 0 acceptance-grade candidates | hard |
| P269_CAPITAL_MODEL_NEXT_ROUTE_SELECTED | True | P269_FIXED_CAPITAL_CONCURRENCY_AND_CAPACITY_RETURN_PRECOMMIT | capital-aware precommit selected | hard |
| P269_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE | True | 0 | 0 | hard |

## Ranked Annualized Research Leads

| candidate_id | family_id | horizon | imbalance_quantile | shock_quantile | spread_regime | cost100_event_rows | symbols | trade_dates | cost100_net_pnl_inr | cost100_annualized_return_pct | cost150_net_pnl_inr | cost200_net_pnl_inr | cost200_annualized_return_pct | cost200_avg_net_per_event | shuffle_label_margin_inr | side_flip_degrades | random_side_beat | acceptance_grade_candidate | fixed_notional_proxy_only | portfolio_return_validated | needs_capital_concurrency_capacity_model | acceptance_blockers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | P268_BID_ABSORPTION_BREADTH_REPAIR | 10 | 0.9 | 0.75 | high | 9 | 4 | 1 | 782.036 | 197.073 | 409.97 | 37.9048 | 9.55202 | 4.21165 | 0 | 1 | 1 | 0 | 1 | 0 | 1 | not_2x_annualized_above_12pct;acceptance_grade_zero;events_lt_30;symbols_lt_8;shuffle_margin_lt_100;cost200_avg_lt_25 |
| P268_P268_WITHDRAWAL_REVERSAL_ROBUSTNESS_REPAIR_H10_IQ0p9_SQ0p75_SPMID | P268_WITHDRAWAL_REVERSAL_ROBUSTNESS_REPAIR | 10 | 0.9 | 0.75 | mid | 29 | 11 | 1 | 572.854 | 144.359 | -626.023 | -1824.9 | -459.875 | -62.9276 | 0 | 1 | 1 | 0 | 1 | 0 | 1 | not_2x_annualized_above_12pct;acceptance_grade_zero;events_lt_30;shuffle_margin_lt_100;cost200_avg_lt_25 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION | P268_BID_ABSORPTION_BREADTH_REPAIR | 10 | 0.9 | 0.75 | compression | 11 | 7 | 1 | 570.273 | 143.709 | 115.527 | -339.22 | -85.4834 | -30.8382 | -1.13687e-13 | 1 | 1 | 0 | 1 | 0 | 1 | not_2x_annualized_above_12pct;acceptance_grade_zero;events_lt_30;symbols_lt_8;shuffle_margin_lt_100;cost200_avg_lt_25 |
| P268_P268_ASK_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPMID | P268_ASK_ABSORPTION_BREADTH_REPAIR | 10 | 0.9 | 0.5 | mid | 15 | 7 | 1 | 557.056 | 140.378 | -63.0533 | -683.162 | -172.157 | -45.5442 | -1.13687e-13 | 1 | 1 | 0 | 1 | 0 | 1 | not_2x_annualized_above_12pct;acceptance_grade_zero;events_lt_30;symbols_lt_8;shuffle_margin_lt_100;cost200_avg_lt_25 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p6_SPHIGH | P268_BID_ABSORPTION_BREADTH_REPAIR | 10 | 0.9 | 0.6 | high | 11 | 6 | 1 | 388.008 | 97.778 | -66.7387 | -521.485 | -131.414 | -47.4078 | 0 | 1 | 1 | 0 | 1 | 0 | 1 | not_2x_annualized_above_12pct;acceptance_grade_zero;events_lt_30;symbols_lt_8;shuffle_margin_lt_100;cost200_avg_lt_25 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p9_SPHIGH | P268_BID_ABSORPTION_BREADTH_REPAIR | 10 | 0.9 | 0.9 | high | 6 | 2 | 1 | 334.056 | 84.182 | 86.0121 | -162.032 | -40.8319 | -27.0053 | 5.68434e-14 | 1 | 1 | 0 | 1 | 0 | 1 | not_2x_annualized_above_12pct;acceptance_grade_zero;events_lt_30;symbols_lt_8;shuffle_margin_lt_100;cost200_avg_lt_25 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPCOMPRESSION | P268_BID_ABSORPTION_BREADTH_REPAIR | 10 | 0.9 | 0.5 | compression | 14 | 8 | 1 | 284.094 | 71.5917 | -294.675 | -873.443 | -220.108 | -62.3888 | 0 | 1 | 1 | 0 | 1 | 0 | 1 | not_2x_annualized_above_12pct;acceptance_grade_zero;events_lt_30;shuffle_margin_lt_100;cost200_avg_lt_25 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p6_SPCOMPRESSION | P268_BID_ABSORPTION_BREADTH_REPAIR | 10 | 0.9 | 0.6 | compression | 14 | 8 | 1 | 284.094 | 71.5917 | -294.675 | -873.443 | -220.108 | -62.3888 | 0 | 1 | 1 | 0 | 1 | 0 | 1 | not_2x_annualized_above_12pct;acceptance_grade_zero;events_lt_30;shuffle_margin_lt_100;cost200_avg_lt_25 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPHIGH | P268_BID_ABSORPTION_BREADTH_REPAIR | 10 | 0.9 | 0.5 | high | 12 | 7 | 1 | 247.498 | 62.3694 | -248.589 | -744.677 | -187.659 | -62.0564 | -2.84217e-14 | 1 | 1 | 0 | 1 | 0 | 1 | not_2x_annualized_above_12pct;acceptance_grade_zero;events_lt_30;symbols_lt_8;shuffle_margin_lt_100;cost200_avg_lt_25 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPLOW | P268_BID_ABSORPTION_BREADTH_REPAIR | 10 | 0.9 | 0.5 | low | 12 | 6 | 1 | 227.374 | 57.2982 | -268.713 | -764.801 | -192.73 | -63.7334 | 5.68434e-14 | 1 | 1 | 0 | 1 | 0 | 1 | not_2x_annualized_above_12pct;acceptance_grade_zero;events_lt_30;symbols_lt_8;shuffle_margin_lt_100;cost200_avg_lt_25 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H6_IQ0p9_SQ0p5_SPLOW | P268_BID_ABSORPTION_BREADTH_REPAIR | 6 | 0.9 | 0.5 | low | 12 | 6 | 1 | 212.804 | 53.6267 | -283.283 | -779.37 | -196.401 | -64.9475 | 0 | 1 | 1 | 0 | 1 | 0 | 1 | not_2x_annualized_above_12pct;acceptance_grade_zero;events_lt_30;symbols_lt_8;shuffle_margin_lt_100;cost200_avg_lt_25 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H6_IQ0p9_SQ0p75_SPCOMPRESSION | P268_BID_ABSORPTION_BREADTH_REPAIR | 6 | 0.9 | 0.75 | compression | 13 | 7 | 1 | 194.874 | 49.1084 | -342.553 | -879.981 | -221.755 | -67.6909 | 5.68434e-14 | 1 | 1 | 0 | 1 | 0 | 1 | not_2x_annualized_above_12pct;acceptance_grade_zero;events_lt_30;symbols_lt_8;shuffle_margin_lt_100;cost200_avg_lt_25 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H6_IQ0p9_SQ0p6_SPLOW | P268_BID_ABSORPTION_BREADTH_REPAIR | 6 | 0.9 | 0.6 | low | 10 | 5 | 1 | 176.716 | 44.5325 | -236.69 | -650.096 | -163.824 | -65.0096 | 2.84217e-14 | 1 | 1 | 0 | 1 | 0 | 1 | not_2x_annualized_above_12pct;acceptance_grade_zero;events_lt_30;symbols_lt_8;shuffle_margin_lt_100;cost200_avg_lt_25 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p9_SPCOMPRESSION | P268_BID_ABSORPTION_BREADTH_REPAIR | 10 | 0.9 | 0.9 | compression | 8 | 5 | 1 | 129.469 | 32.6262 | -201.256 | -531.98 | -134.059 | -66.4975 | 2.84217e-14 | 1 | 1 | 0 | 1 | 0 | 1 | not_2x_annualized_above_12pct;acceptance_grade_zero;events_lt_30;symbols_lt_8;shuffle_margin_lt_100;cost200_avg_lt_25 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H6_IQ0p9_SQ0p75_SPLOW | P268_BID_ABSORPTION_BREADTH_REPAIR | 6 | 0.9 | 0.75 | low | 8 | 5 | 1 | 112.929 | 28.4582 | -217.796 | -548.52 | -138.227 | -68.565 | 1.42109e-14 | 1 | 1 | 0 | 1 | 0 | 1 | not_2x_annualized_above_12pct;acceptance_grade_zero;events_lt_30;symbols_lt_8;shuffle_margin_lt_100;cost200_avg_lt_25 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p6_SPLOW | P268_BID_ABSORPTION_BREADTH_REPAIR | 10 | 0.9 | 0.6 | low | 10 | 5 | 1 | 101.408 | 25.5548 | -311.998 | -725.404 | -182.802 | -72.5404 | 1.42109e-14 | 1 | 1 | 0 | 1 | 0 | 1 | not_2x_annualized_above_12pct;acceptance_grade_zero;events_lt_30;symbols_lt_8;shuffle_margin_lt_100;cost200_avg_lt_25 |
| P268_P268_WITHDRAWAL_REVERSAL_ROBUSTNESS_REPAIR_H10_IQ0p75_SQ0p75_SPMID | P268_WITHDRAWAL_REVERSAL_ROBUSTNESS_REPAIR | 10 | 0.75 | 0.75 | mid | 51 | 11 | 1 | 74.4531 | 18.7622 | -2033.92 | -4142.29 | -1043.86 | -81.2213 | -2.27374e-13 | 1 | 1 | 0 | 1 | 0 | 1 | not_2x_annualized_above_12pct;acceptance_grade_zero;shuffle_margin_lt_100;cost200_avg_lt_25 |

## Interpretation Ledger

| finding_id | evidence | severity | finding_present | interpretation |
| --- | --- | --- | --- | --- |
| profitable_fixed_notional_research_leads_found | annualized_1x_leads=17; best_1x_annualized=197.07298375832715 | research_positive | 1 | There are profit-hunting leads worth preserving. |
| no_cost200_annualized_profitable_research_leads | cost200_annualized_leads=0; best_2x_annualized=9.552022158327203 | hard | 1 | No lead clears the 12% fixed-notional proxy under 2x modeled costs. |
| no_acceptance_grade_candidate | acceptance_grade_candidates=0 | hard | 1 | No candidate is acceptance-grade yet. |
| annualization_not_portfolio_return | phase268_annualization_is_portfolio_return=0 | hard | 1 | Annualized values are fixed-notional proxies, not capital-account portfolio returns. |
| best_lead_breadth_and_shuffle_fragile | events=9;symbols=4;shuffle_margin=0.0 | hard | 1 | Best lead remains sparse or shuffle-fragile. |
| capital_concurrency_capacity_missing | capital_concurrency_model=not_yet_materialized;capacity_model=not_yet_materialized | hard | 1 | Next phase must convert fixed-notional proxies into capital-aware return evidence. |
| full_depth_surface_preserved | full_depth=1200;l2_l5=1200;l1_only=0;variants=1200 | important_context | 1 | Full-depth L2/L2-L5 objective remains intact. |

## Decision Ledger

| decision_id | decision_value | evidence | description |
| --- | --- | --- | --- |
| preserve_phase268_research_leads | 1 | annualized_1x_research_leads=17 | Keep the leads for next-stage capital-aware analysis. |
| do_not_claim_portfolio_annual_return | 1 | annualization_formula=net_pnl_inr / 100000 * 252 | Annualized values are fixed-notional proxies only. |
| do_not_promote_or_replay_phase268 | 1 | acceptance_grade_candidates=0 | No replay, promotion, paper/live, or deployable profitability claim. |
| require_fixed_capital_concurrency_model | 1 | small-event annualized proxy can overstate deployable return | Next phase must model simultaneous capital use, per-event notional, and capacity. |
| preserve_full_depth_requirement | 1 | rows_1_to_5_and_l2_l5_required | Full-depth Zerodha top-five depth remains mandatory. |
| selected_next_route | P269_FIXED_CAPITAL_CONCURRENCY_AND_CAPACITY_RETURN_PRECOMMIT | capital-aware return precommit | Next materially necessary action. |

## Next Route Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P270_INPUT | outputs/phase268/phase268_two_lane_variant_results.csv and outputs/phase268/phase268_exploratory_event_ledger.csv | Use Phase268 research leads and event ledger; no replay yet. |
| P270_RETURN_TYPE | fixed_capital_portfolio_return_model | Convert fixed-notional annualized proxy into capital-aware return evidence. |
| P270_CAPITAL_ACCOUNTING | initial_capital;per_trade_notional;max_concurrent_positions;capital_reuse;cash_drag | Explicitly model capital constraints instead of assuming unlimited capital. |
| P270_CAPACITY_ACCOUNTING | events_per_day;symbol_capacity;turnover;cost_stress;slippage_sensitivity | Check if small-event pockets remain meaningful after capacity and turnover limits. |
| P270_DEPTH_REQUIREMENT | full_top_five_rows_1_to_5_and_levels_2_to_5_required | Capital-aware analysis must still use the full-depth L2 signal surface. |
| P270_FORBIDDEN | paper_live_or_deployable_profitability_claim;portfolio_return_claim_without_capital_model;l1_only | No claim until capital/capacity model exists and L1-only remains forbidden. |
| P270_OUTPUT | capital_return_precommit_and_candidate_capacity_contract | Write the contract for a later capital-aware analysis/search. |
