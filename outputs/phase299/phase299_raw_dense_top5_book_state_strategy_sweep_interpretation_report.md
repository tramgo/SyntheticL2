# Phase299 Raw Dense Top-Five Book-State Strategy Sweep Interpretation

Phase299 closes Phase298 for direct acceptance and preserves its high-annualized sparse pockets only as directional-signal seeds.

The selected next route is a Phase300 passive-aware execution precommit. Phase300 must freeze fill probability, adverse-selection, and forced-flatten rules before producing results.

No replay, promotion, paper/live acceptance, or deployable profitability claim is opened.

## Phase298 Summary

| metric | value | description |
| --- | --- | --- |
| phase298_raw_dense_sweep_complete | 1 | Phase298 raw dense top-five book-state strategy sweep completed |
| phase298_selected_route | P298_RAW_DENSE_TOP5_BOOK_STATE_STRATEGY_SWEEP | Selected route |
| phase298_dense_root | raw_synthetic_l2_dense_full_year | Raw dense lake root |
| phase298_symbol_rows | 1 | Symbols in bounded sweep |
| phase298_trade_month_rows | 12 | Trade months in bounded sweep |
| phase298_source_file_rows | 12 | Dense shard files scanned |
| phase298_sample_stride | 256 | Deterministic dense-row sample stride |
| phase298_sampled_dense_rows | 729132 | Sampled raw dense rows |
| phase298_shard_trade_date_rows | 252 | Shard-date rows sampled |
| phase298_raw_event_rows | 9596 | Raw dense candidate event rows |
| phase298_variant_rows | 576 | Raw-book-state variants evaluated |
| phase298_scenario_rows | 1152 | Cost200 fixed-capital scenarios evaluated |
| phase298_sparse_above12_scenario_rows | 0 | Above-12 sparse diagnostic rows |
| phase298_robust_portfolio_floor_scenario_rows | 0 | Robust floor rows |
| phase298_robust_portfolio_above12_scenario_rows | 0 | Robust above-12 rows |
| phase298_best_variant_id | P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-01_Q99_DL3_H6 | Best variant |
| phase298_best_strategy_family | P298_RAW_MICROPRICE_DEPTH_REVERSAL | Best family |
| phase298_best_cost200_annualized_pct | 382.9973530062694 | Best fixed-capital annualized diagnostic |
| phase298_best_realized_net_pnl_inr | 15198.307658978945 | Best net P&L |
| phase298_best_scheduled_event_rows | 3 | Best scheduled events |
| phase298_best_observed_trade_dates | 1 | Best observed dates |
| phase298_best_initial_capital_inr | 1000000.0 | Fixed initial capital denominator |
| phase298_raw_book_state_l1_l5_required | 1 | Raw levels 1-5 required |
| phase298_levels_2_to_5_required | 1 | Levels 2-5 materiality required |
| phase298_l1_only_variant_rows | 0 | L1-only variants |
| phase298_net_edge_live_mask_rows | 0 | Net edge live masks |
| phase298_annualized_denominator | fixed_initial_capital | Annualized denominator |
| phase298_strategy_replay_allowed | 0 | No replay |
| phase298_strategy_promotion_allowed | 0 | No promotion |
| phase298_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase298_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase298_hard_gate_pass_rows | 13 | Passed hard gates |
| phase298_hard_gate_rows | 13 | Hard gates |
| phase298_next_best_action | run_phase299_raw_dense_top5_book_state_strategy_sweep_interpretation_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P299_PHASE298_SWEEP_COMPLETE | True | 1 | Phase298 sweep complete | hard |
| P299_PHASE298_NEXT_ACTION_PRESENT | True | run_phase299_raw_dense_top5_book_state_strategy_sweep_interpretation_no_paper_live | Phase298 routes to Phase299 interpretation | hard |
| P299_PHASE298_GATES_PASS | True | 13/13 | Phase298 hard gates pass | hard |
| P299_RANKED_INTERPRETATION_PRESENT | True | 576 | >0 ranked variants | hard |
| P299_CLOSES_PHASE298_FOR_DIRECT_ACCEPTANCE | True | 1 | Phase298 closed for direct acceptance | hard |
| P299_NO_ACCEPTANCE_SURVIVOR | True | sparse_above12=0;robust_above12=0 | no Phase298 survivor | hard |
| P299_BEST_BELOW_PHASE300_EVENT_FLOOR | True | 3 | <30 | hard |
| P299_DIRECTIONAL_SEEDS_PRESERVED | True | 16 | >0 | hard |
| P299_RAW_TOP5_BOOK_SCOPE | True | l1_only=0;live_mask=0 | levels 1-5 and no leakage | hard |
| P299_FIXED_CAPITAL_DENOMINATOR | True | fixed_initial_capital | fixed_initial_capital | hard |
| P299_NEXT_ROUTE_SELECTED | True | P300_PASSIVE_AWARE_DIRECTIONAL_L2_EXECUTION_PRECOMMIT | P300_PASSIVE_AWARE_DIRECTIONAL_L2_EXECUTION_PRECOMMIT | hard |
| P299_BOUNDARIES_CLOSED | True | replay=0;paper=0;claim=0 | no replay/paper/live/claim | hard |
| P299_PHASE300_CONTRACT_PRESENT | True | 13 | Phase300 route contract rows | hard |

## Interpretation Ledger

| finding_id | evidence | severity | finding_present | interpretation |
| --- | --- | --- | --- | --- |
| phase298_executed | scenario_rows=1152 | evidence | 1 | Phase298 executed on raw dense top-five book-state artifacts. |
| phase298_no_direct_acceptance_survivor | sparse_above12=0;robust_above12=0 | hard_negative | 1 | No direct Phase298 survivor is accepted or promoted. |
| phase298_best_is_sparse_spark | best_ann=382.9973530062694;best_events=3;best_dates=1 | research_clue | 1 | The best result is a sparse fixed-capital annualized spark, not a strategy. |
| above12_below_floor_variants_preserved | rows=9 | research_clue | 1 | High annualized pockets below the 30-event floor are preserved only as directional-signal seeds. |
| directional_signal_seeds_preserved | rows=16 | next_input | 1 | Reuse existing directional signals; do not run a fresh alpha search in Phase300. |
| raw_depth_scope_preserved | bid/ask price, quantity, order-count depth levels 1-5 | constraint | 1 | Phase300 must continue using top-five market-by-price depth levels, including levels 2-5. |
| taker_cost_problem_identified | prior candidates crossed spread on entry/exit | design_gap | 1 | The next lever is passive-aware execution, not more taker-only threshold mining. |
| next_route_selected | P300_PASSIVE_AWARE_DIRECTIONAL_L2_EXECUTION_PRECOMMIT | next_action | 1 | Route to Phase300 passive-aware execution precommit before generating results. |

## Decision Ledger

| decision_id | decision_value | evidence | description |
| --- | --- | --- | --- |
| close_phase298_for_direct_acceptance | 1 | no_sparse_or_robust_acceptance_rows | No replay, promotion, paper/live, or profitability claim is opened. |
| preserve_best_sparse_spark_as_seed | P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-01_Q99_DL3_H6 | family=P298_RAW_MICROPRICE_DEPTH_REVERSAL;ann=382.9973530062694;events=3 | Use only as a directional signal seed. |
| do_not_add_new_alpha_search_in_phase300 | 1 | charter_requires_reuse_validated_directional_signals | Phase300 tests execution realism, not a new signal grid. |
| require_passive_fill_model | 1 | passive_fill_probability_from_queue_depth_required | No assumed passive fills. |
| require_adverse_selection_penalty | 1 | fill_conditioned_toxicity_penalty_required | Filled passive orders must pay adverse-selection penalty. |
| require_forced_flatten_cost | 1 | inventory_leftover_pays_taker_flatten | No free spread saving by refusing to exit. |
| selected_next_route | P300_PASSIVE_AWARE_DIRECTIONAL_L2_EXECUTION_PRECOMMIT | only remaining retail cost-side lever | Freeze Phase300 passive-aware execution charter before results. |

## Phase300 Route Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P300_THESIS | passive_aware_execution_of_directional_top5_depth_signals | Test the retail-available cost-side lever after taker-only edges failed. |
| P300_INPUT_DIRECTIONAL_SIGNALS | P235;P268;P280;P281;P282;P298_sparse_directional_seeds | Reuse existing directional L2 signals; no new alpha search. |
| P300_INPUT_FILL_MODEL | P260_to_P269_passive_queue_depth_features | Estimate P(fill \| queue depth, side, horizon) from raw depth state. |
| P300_INPUT_TOXICITY | P130_and_P280_to_P282_adverse_selection_toxicity_estimates | Apply fill-conditioned toxicity/adverse-selection penalty. |
| P300_INPUT_FEED_FILTER | P130_feed_imperfection_regime_filter | Skip toxic or degraded feed windows where applicable. |
| P300_INPUT_COST_MODEL | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha NSE equity intraday model with cost200 stress. |
| P300_INPUT_RAW_BOOK | P51_raw_dense_lake;P298_schema_audit | Use raw top-five market-by-price depth levels 1-5 price/qty/order-count. |
| P300_FORBID_L1_ONLY | l1_only_variant_rows_must_equal_0 | Levels 2-5 materiality remains required. |
| P300_FORBID_LOOKAHEAD | net_edge_live_mask_rows_must_equal_0 | No net-edge labels may be used as live masks. |
| P300_REQUIRED_EXECUTION_POLICY | passive_entry_wait_cancel_or_cross;passive_exit_when_calm;aggressive_exit_when_risk_or_expiry | Hybrid execution policy, not two-sided market-making. |
| P300_REQUIRED_PENALTIES | fill_probability;adverse_selection;forced_flatten | All three realism penalties are mandatory. |
| P300_ACCEPTANCE_BAR | events_ge_30;annualized_gt_12pct_cost200;multi_symbol_date_breadth;rank_stable_1x_to_2x | Sparse >12% pockets below 30 events are discovery-only. |
| P300_BOUNDARY | replay_0;promotion_0;paper_live_0;profitability_claim_0 | Synthetic-only precommit; no acceptance flip. |

## Family Interpretation

| strategy_family | scenario_rows | variant_rows | max_scheduled_event_rows | cost200_above12_sparse_diagnostic_rows | robust_portfolio_floor_above12_rows | sparse_floor_met_rows | robust_portfolio_floor_met_rows | min_annualized_pct | median_annualized_pct | max_annualized_pct | max_net_pnl_inr | best_variant_id | close_for_direct_acceptance | preserve_for_passive_aware_execution |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL | 288 | 144 | 6 | 0 | 0 | 0 | 0 | -19.6156 | -4.16713 | 382.997 | 15658 | P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-01_Q99_DL3_H6 | 1 | 1 |
| P298_RAW_ORDERCOUNT_PRESSURE_CONTINUATION | 288 | 144 | 6 | 0 | 0 | 0 | 0 | -39.5878 | -1.04178 | 2.52844 | 802.679 | P298_RAW_ORDERCOUNT_PRESSURE_CONTINUATION_HDFCBANK_2026-01_Q99_DL3_H6 | 1 | 1 |
| P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION | 288 | 144 | 6 | 0 | 0 | 0 | 0 | -39.5878 | -1.04178 | 1.9451 | 540.304 | P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION_HDFCBANK_2026-11_Q99_DL3_H6 | 1 | 1 |
| P298_RAW_TOP5_PRESSURE_CONTINUATION | 288 | 144 | 6 | 0 | 0 | 0 | 0 | -39.5878 | -1.19061 | -0.219323 | -47.1922 | P298_RAW_TOP5_PRESSURE_CONTINUATION_HDFCBANK_2026-05_Q95_DL1_H6 | 1 | 0 |

## Top Ranked Variants

| phase298_variant_id | strategy_family | symbol | threshold_quantile | daily_event_limit | exit_horizon_ticks | scenario_rows | selected_event_rows | max_scheduled_event_rows | cost200_above12_sparse_diagnostic_rows | robust_portfolio_floor_above12_rows | sparse_floor_met_rows | robust_portfolio_floor_met_rows | min_annualized_pct | median_annualized_pct | max_annualized_pct | max_net_pnl_inr | best_scenario_id | above12_but_below_phase300_floor | phase298_acceptance_survivor | preserve_as_directional_signal_seed | close_for_direct_acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-01_Q99_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.99 | 3 | 6 | 2 | 3 | 3 | 0 | 0 | 0 | 0 | 382.997 | 382.997 | 382.997 | 15198.3 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-01_Q99_DL3_H6_CAP1000000_NOT100000_CONC1_COST200 | 1 | 0 | 1 | 1 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-09_Q99_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.99 | 3 | 6 | 2 | 6 | 6 | 0 | 0 | 0 | 0 | 5.79169 | 101.541 | 197.29 | 15658 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-09_Q99_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 | 1 | 0 | 1 | 1 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-01_Q95_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.95 | 3 | 6 | 2 | 6 | 6 | 0 | 0 | 0 | 0 | 2.78547 | 98.5348 | 194.284 | 15419.4 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-01_Q95_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 | 1 | 0 | 1 | 1 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-12_Q99_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.99 | 3 | 6 | 2 | 3 | 3 | 0 | 0 | 0 | 0 | 31.829 | 31.829 | 31.829 | 1263.06 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-12_Q99_DL3_H6_CAP1000000_NOT100000_CONC1_COST200 | 1 | 0 | 1 | 1 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-03_Q95_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.95 | 3 | 6 | 2 | 6 | 6 | 0 | 0 | 0 | 0 | 12.9295 | 14.422 | 15.9145 | 1263.06 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-03_Q95_DL3_H6_CAP1000000_NOT100000_CONC1_COST200 | 1 | 0 | 1 | 1 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-03_Q99_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.99 | 3 | 6 | 2 | 6 | 6 | 0 | 0 | 0 | 0 | 12.9295 | 14.422 | 15.9145 | 1263.06 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-03_Q99_DL3_H6_CAP1000000_NOT100000_CONC1_COST200 | 1 | 0 | 1 | 1 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-12_Q95_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.95 | 3 | 6 | 2 | 6 | 6 | 0 | 0 | 0 | 0 | 11.2966 | 13.6056 | 15.9145 | 1263.06 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-12_Q95_DL3_H6_CAP1000000_NOT100000_CONC1_COST200 | 1 | 0 | 1 | 1 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-04_Q95_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.95 | 3 | 6 | 2 | 9 | 6 | 0 | 0 | 0 | 0 | -1.11444 | 6.09483 | 13.3041 | 1583.82 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-04_Q95_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 | 1 | 0 | 1 | 1 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-04_Q99_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.99 | 3 | 6 | 2 | 9 | 6 | 0 | 0 | 0 | 0 | -1.11444 | 6.09483 | 13.3041 | 1583.82 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-04_Q99_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 | 1 | 0 | 1 | 1 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-06_Q99_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.99 | 3 | 6 | 2 | 6 | 6 | 0 | 0 | 0 | 0 | 9.89443 | 10.4841 | 11.0737 | 878.866 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-06_Q99_DL3_H6_CAP1000000_NOT100000_CONC1_COST200 | 0 | 0 | 1 | 1 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-09_Q95_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.95 | 3 | 6 | 2 | 12 | 6 | 0 | 0 | 0 | 0 | -9.61646 | -3.36031 | 2.89584 | 459.658 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-09_Q95_DL3_H6_CAP1000000_NOT100000_CONC1_COST200 | 0 | 0 | 1 | 1 |
| P298_RAW_ORDERCOUNT_PRESSURE_CONTINUATION_HDFCBANK_2026-01_Q99_DL3_H6 | P298_RAW_ORDERCOUNT_PRESSURE_CONTINUATION | HDFCBANK | 0.99 | 3 | 6 | 2 | 24 | 6 | 0 | 0 | 0 | 0 | 0.0346291 | 1.28153 | 2.52844 | 802.679 | P271_P298_RAW_ORDERCOUNT_PRESSURE_CONTINUATION_HDFCBANK_2026-01_Q99_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 | 0 | 0 | 1 | 1 |
| P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION_HDFCBANK_2026-11_Q99_DL3_H6 | P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION | HDFCBANK | 0.99 | 3 | 6 | 2 | 21 | 6 | 0 | 0 | 0 | 0 | -2.30756 | -0.181232 | 1.9451 | 540.304 | P271_P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION_HDFCBANK_2026-11_Q99_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 | 0 | 0 | 1 | 1 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-02_Q99_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.99 | 3 | 6 | 2 | 6 | 6 | 0 | 0 | 0 | 0 | -11.0859 | -4.97323 | 1.13942 | 90.4304 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-02_Q99_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 | 0 | 0 | 1 | 1 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-11_Q99_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.99 | 3 | 6 | 2 | 6 | 6 | 0 | 0 | 0 | 0 | -11.0859 | -4.97323 | 1.13942 | 90.4304 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-11_Q99_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 | 0 | 0 | 1 | 1 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-06_Q95_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.95 | 3 | 6 | 2 | 12 | 6 | 0 | 0 | 0 | 0 | -5.13221 | -2.36378 | 0.404648 | 64.2298 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-06_Q95_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 | 0 | 0 | 1 | 1 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-05_Q95_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.95 | 3 | 6 | 2 | 9 | 6 | 0 | 0 | 0 | 0 | -0.0723884 | -0.0650069 | -0.0576254 | -6.86017 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-05_Q95_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 | 0 | 0 | 0 | 1 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-05_Q99_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.99 | 3 | 6 | 2 | 9 | 6 | 0 | 0 | 0 | 0 | -0.0723884 | -0.0650069 | -0.0576254 | -6.86017 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-05_Q99_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 | 0 | 0 | 0 | 1 |
| P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION_HDFCBANK_2026-07_Q95_DL1_H1 | P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION | HDFCBANK | 0.95 | 1 | 1 | 2 | 19 | 2 | 0 | 0 | 0 | 0 | -0.438646 | -0.328984 | -0.219323 | -165.362 | P271_P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION_HDFCBANK_2026-07_Q95_DL1_H1_CAP1000000_NOT100000_CONC1_COST200 | 0 | 0 | 0 | 1 |
| P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION_HDFCBANK_2026-07_Q95_DL1_H3 | P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION | HDFCBANK | 0.95 | 1 | 3 | 2 | 19 | 2 | 0 | 0 | 0 | 0 | -0.438646 | -0.328984 | -0.219323 | -165.362 | P271_P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION_HDFCBANK_2026-07_Q95_DL1_H3_CAP1000000_NOT100000_CONC1_COST200 | 0 | 0 | 0 | 1 |
