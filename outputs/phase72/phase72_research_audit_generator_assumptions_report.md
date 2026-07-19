# Phase72 Research Audit and Generator-Assumption Review

Generated UTC: 2026-07-19T19:52:25.097378+00:00

Phase72 consolidates the Phase52-71 strategy-mining evidence after multiple feature families failed bounded gates.
The audit prevents another broad full-year replay until the generator/execution assumptions behind the near-misses are reviewed.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase72_families_reviewed | 12 | Strategy families reviewed across Phase52-71 |
| phase72_scale_ready_family_count | 0 | Families currently allowed to scale |
| phase72_near_miss_count | 2 | Positive but non-scaling near misses |
| phase72_generator_assumption_items | 5 | Generator/execution assumption areas requiring review |
| phase72_allow_more_full_year_strategy_replay_now | 0 | 0 means do not launch another full-year strategy replay now |
| phase72_recommend_next_action | timestamp_aligned_cross_symbol_matrix_and_shock_panel_audit | Next implementation focus |
| phase72_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Cost model retained for future gates |

## Research Family Audit

| strategy_family_id | phases | decision | deployable | best_evidence | primary_failure_mode | gross_positive_evidence | after_cost_positive_evidence | net_pnl_inr | trade_count | scale_recommendation | required_next_action | can_continue_same_shard_family |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F01_dense_marketable_bruteforce | 52,53 | retired | False | Phase53 found zero profitable aggregate strategy/profile rows after retail costs. | costs_overwhelmed_dense_taker_signals | 3 | 0 |  | 8.26538e+08 | 0 | do_not_continue_bruteforce_shard_replay | False |
| F02_selective_marketable_controls | 54 | retired | False | Phase54 produced one after-cost positive row only in nondeployable controls and zero deployable retail candidates. | positive_only_under_nondeployable_control_assumptions |  | 1 | 7856.21 | 456 | 0 | keep_as_control_not_live_candidate | False |
| F03_cost_aware_taker_edge_mining | 55 | retired | False | Phase55 found no deployable positive after-cost candidates; the positive ceiling was oracle-only. | oracle_positive_but_retail_deployable_negative | 1 | 0 | -13367.6 | 490 | 0 | do_not_scale_oracle_edges | False |
| F04_no_lookahead_dense_rule_labels | 56 | retired | False | Phase56 evaluated 180 no-lookahead rules and found zero positive test rules after retail costs. | no_test_rule_cleared_costs |  | 0 | -4829.7 | 180 | 0 | do_not_widen_dense_no_lookahead_rules | False |
| F05_supervised_interaction_cells | 57,58,59 | retired | False | Phase57 found one candidate, but Phase58 emitted zero disjoint trades and Phase59 found zero positive stable validation rows. | non_repeating_sparse_cell_and_failed_stability_validation | 1 | 0 | -785962 | 0 | 0 | retire_sparse_interaction_cell_family | False |
| F06_lower_frequency_event_bar_momentum | 60,61,62,63 | retired | False | Phase60 passed initial validation, then Phase61 lost -88,748.03 INR, Phase62 found only a tiny KOTAKBANK clue, and Phase63 falsified that clue at -24,100.26 INR. | initial_validation_edge_did_not_survive_wider_symbol_month_falsification | 1 | 0 | -24100.3 | 155 | 0 | retire_phase60_candidate_family | False |
| F07_passive_limit_queue_capture | 64_next | next_active_research_branch | False | Marketable-taker families repeatedly failed after spread, slippage, impact and Zerodha charges; a different mechanism must be tested. | not_yet_tested_and_passive_fills_are_unobserved_assumptions |  |  |  |  | 1 | implement_passive_queue_assumption_sensitivity_before_any_profit_claim | True |
| F08_naive_passive_imbalance | 65,66 | retired | False | Phase65 had zero surviving queue profiles and best expected P&L -1020667.89 INR; Phase66 had zero adverse-selection label candidates. | passive_touches_were_adverse_selection_traps |  |  | -1.02067e+06 | 68850 | 0 | do_not_widen_naive_passive_imbalance | False |
| F09_replenishment_after_touch | 68 | retired | False | Phase68 best after-cost bucket was -13.24 bps with zero cost-clearing buckets. | replenishment_improved_loss_but_did_not_clear_cost_or_adverse_selection |  |  |  | 68850 | 0 | do_not_target_replenishment_replay | False |
| F10_spread_transition | 69 | retired | False | Phase69 produced 319500 labels but best after-cost bucket was -10.03 bps. | spread_transition_direction_did_not_clear_costs |  |  |  | 319500 | 0 | do_not_target_spread_transition_replay | False |
| F11_cross_symbol_lead_lag | 70 | watchlist_near_miss | False | Phase70 best rule was positive at 38915.75 INR but failed precision/cost-drag gates. | positive_pnl_but_precision_and_cost_drag_gate_failed |  |  | 38915.7 |  | 0 | do_not_replay_without_feature_refinement_or_cost_reduction | False |
| F12_shock_resilience | 71 | watchlist_near_miss | False | Phase71 best shock rule was positive at 13311.38 INR but failed sample-size gate. | positive_shock_near_miss_but_insufficient_trade_count |  |  | 13311.4 |  | 0 | audit_generator_shock_frequency_and_retest_only_if_sample_size_is_designed | False |

## Near-Miss Watchlist

| near_miss_id | phase | rule_id | net_pnl_inr | failed_gate | diagnosis | allowed_next_action |
| --- | --- | --- | --- | --- | --- | --- |
| NM70_HDFCBANK_LEAD_LAG | 70 | P70_MEGA_HDFCBANK_MOMENTUM_Q70 | 38915.7 | precision_cost_clear_lt_0_55_and_cost_drag_gt_0_50_abs_gross | Positive P&L exists but is too dependent on large winners and too expensive relative to gross edge. | feature_refinement_only_no_disjoint_replay_yet |
| NM71_MARKET_SHOCK_MEAN_REVERSION | 71 | P71_SHOCK_MEAN_REVERSION_B10000_market_shock_Q90 | 13311.4 | trades_lt_100 | Positive shock mean-reversion row passes several quality tests but has only 72 trades. | generator_shock_frequency_audit_before_replay |

## Generator Assumption Review

| assumption_area | finding | risk | recommended_change |
| --- | --- | --- | --- |
| cost_drag_vs_signal_scale | Most candidate gross edges are smaller than spread, slippage, impact and Zerodha retail charges. | More shard replay will mostly measure cost drag, not discover deployable edge. | Prioritize lower-turnover event bars, stronger entry filters, or maker-only assumptions with explicit adverse-selection labels. |
| synthetic_spread_dynamics | Phase69 found spread changes are present but sub-0.5 bps at the tested horizon. | Spread-transition features may be too weak unless generator spread shocks or liquidity regime changes are more expressive. | Audit spread process calibration against real sample and add documented sensitivity scenarios for wider/narrower spread dynamics. |
| passive_fill_observability | Passive fills remain inferred because Zerodha top-five market-by-price data lacks order identity and true queue position. | Passive profitability can be overstated if queue assumptions are not pessimistic and sensitivity-tested. | Keep all passive results labeled hypothetical until real fills or richer queue data exist. |
| shock_frequency_and_sample_size | Shock mean-reversion produced a positive near-miss but failed trade-count gates. | Shock results can be one-scenario artifacts unless frequency and diversity are intentionally controlled. | Before replaying shock rules, audit shock schedule diversity and generate a scenario-balanced shock panel. |
| cross_symbol_alignment | Cross-symbol lead-lag produced the strongest near-miss but failed precision and cost-drag gates. | Event bars aligned by per-symbol local sequence may not represent synchronous tradable time. | Build a timestamp-aligned cross-symbol bar matrix before deciding whether lead-lag is genuinely dead. |
