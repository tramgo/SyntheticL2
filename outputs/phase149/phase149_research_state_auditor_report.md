# Phase149 Research State Auditor

Generated UTC: 2026-08-02T06:47:55.731698+00:00

Phase149 reconciles current phase scripts, output evidence, branch states, and replay gates.
It does not run strategies, contact Azure, import data, or unlock replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase149_phase_rows | 270 | Phase rows discovered from scripts and outputs |
| phase149_runner_phase_rows | 268 | Phase rows with at least one runner |
| phase149_acceptance_phase_rows | 220 | Phase rows with acceptance summaries |
| phase149_branch_rows | 5 | Current research branches summarized |
| phase149_hard_gate_rows | 322 | Hard global-state gates evaluated |
| phase149_hard_gate_pass_rows | 322 | Hard global-state gates passed |
| phase149_strategy_replay_allowed | 0 | Phase149 never unlocks strategy replay |
| phase149_next_best_action | run_phase278_cost_robust_redesign_interpretation_no_paper_live | Recommended next milestone |

## Branch Status Summary

| branch | status | evidence | current_next_action |
| --- | --- | --- | --- |
| real_l2_anchor_gate | gated | Phase146/148 keep strategy replay closed until at least five ready real-anchor days are proven. | use_phase174_secure_download_orchestrator_for_required_real_l2_dates |
| real_receive_flow_source | cost_robust_redesign_interpretation_open | Phase172 ready_dates=7, additional_dates_needed=0; Phase174 download_ran=1; Phase175 activation_ready=1; Phase176 features_materialized=1; Phase177 quality_audit_ran=1; Phase178 handoff_ready=1; Phase179 precommit_ready=1; Phase180 precommit_ready=1; Phase181 labels_materialized=1; Phase182 label_audit_pass=1; Phase183 replay_readiness=1; Phase184 dry_run_complete=1, test_rows_used=0, promotion_allowed=0; Phase185 interpretation_complete=1, cost_dominates=1, test_replay_allowed_next=0; Phase186 family_set_closed=1, reuse_without_redesign_allowed=0, test_replay_allowed_next=0; Phase187 candidate_complete=1, validation_positive_all_profiles=1, test_replay_allowed_next=0; Phase188 interpretation_complete=1, breadth_warning=1, date_count_warning=1, test_replay_allowed_next=0; Phase189 decision_complete=1, test_precommit_allowed=0, test_replay_allowed_next=0; Phase190 decision_complete=1, additional_validation_breadth_available_now=0, test_replay_execution=0; Phase191 precommit_complete=1, test_replay_execution=0, test_result_allowed=0; Phase192 download_complete=1, test_replay_execution=0; Phase193 extension_complete=1, extension_dates=2026-07-15;2026-07-16, min_profile_net=9.085299933825853, breadth_warning=1, test_replay_execution=0; Phase194 fragility_decision_complete=1, all_extension_profile_dates_negative=1, test_replay_allowed_next=0; Phase195 redesign_search_complete=1, passing_extension_gate_candidates=0, best_candidate=P195_TOP5_FOLLOW_I80_S1p5_Z1_Q1_R50, best_min_extension_net=-12.410960684628158, test_replay_allowed_next=0; Phase196 expanded_model_search_complete=1, train_selected_model_rows=0, passing_extension_gate_models=0, best_model=nan, test_replay_allowed_next=0; Phase197 feature_precommit_complete=1, ready_feature_families=5, strategy_replay_allowed=0, test_replay_allowed_next=0; Phase198 context_model_search_complete=1, train_selected_model_rows=0, passing_extension_gate_models=0, best_model=nan, best_family=nan, test_replay_allowed_next=0; Phase199 branch_decision_complete=1, current_branch_paused=1, material_redesign_required=1, test_replay_allowed_next=0; Phase200 precommit_complete=1, selected_hypothesis=P200_QUEUE_PASSIVE_QUEUE_POSITION_PROXY, label_contract_rows=6, stage_action_rows=4, test_replay_allowed_next=0; Phase201 stage01_complete=1, joined_rows=696, pre_replay_candidates=0, max_symbols=4, max_dates=4, test_replay_allowed_next=0; Phase202 redesign_precommit_complete=1, redesigned_feature_rows=4, acceptance_contract_rows=4, phase203_action_rows=3, test_replay_allowed_next=0; Phase203 label_materialization_complete=1, materialized_label_rows=696, redesigned_candidate_pass_rows=0, max_symbols=4, max_dates=4, adverse_selection_ceiling_met=0, candidate_gate_open=0, test_replay_allowed_next=0; Phase204 closure_decision_complete=1, passive_redesign_closed_for_replay=1, material_new_source_required=1, threshold_widening_allowed=0, test_replay_allowed_next=0; Phase205 material_new_source_precommit_complete=1, selected_route=P205_REAL_RECEIVE_FLOW_CONTEXT_SOURCE_REFRESH, phase206_work_order_rows=3, test_replay_allowed_next=0; Phase206 nonoverlap_feature_contract_complete=1, feature_catalog_rows=6, blocked_reference_rows=14, nonoverlap_pass_rows=6, model_fit_allowed=0, test_replay_allowed_next=0; Phase207 feature_matrix_precommit_complete=1, matrix_rows=24, available_rows=24, trade_dates=7, symbols=32, model_fit_allowed=0, test_replay_allowed_next=0; Phase208 quality_gate_complete=1, quality_rows=24, quality_pass_rows=24, blocking_gaps=0, model_fit_allowed=0, test_replay_allowed_next=0; Phase209 model_fit_precommit_spec_complete=1, model_spec_rows=3, feature_set_rows=24, label_target_rows=3, split_control_rows=4, model_fit_execution_allowed=0, test_replay_allowed_next=0; Phase210 train_validation_model_fit_dry_run_complete=1, joined_rows=1641001, model_fit_rows=12, validation_metric_rows=12, negative_control_rows=12, test_rows_used=0, strategy_replay_allowed=0, profitability_claim_allowed=0; Phase211 interpretation_complete=1, interpretation_rows=12, passing_rows=0, candidate_opened_for_replay=0, strategy_replay_allowed=0, profitability_claim_allowed=0; Phase212 closure_complete=1, families_closed=3, redesign_rows=3, model_fit_allowed_next=0, strategy_replay_allowed=0, profitability_claim_allowed=0; Phase213 source_precommit_complete=1, selected_source=P213_EVENT_SURPRISE_CONDITIONAL_LABEL_SOURCE, label_contract_rows=3, phase214_work_order_rows=1, model_fit_allowed_next=0, strategy_replay_allowed=0; Phase214 label_materialization_complete=1, label_rows=1641001, event_surprise_rows=130231, quality_pass_rows=512, sealed_test_rows_used=0, strategy_replay_allowed=0; Phase215 quality_interpretation_complete=1, passing_rows=14, families_with_interpretable_rows=3, phase216_work_order_rows=1, model_fit_allowed_next=0, strategy_replay_allowed=0; Phase216 event_only_precommit_complete=1, target_rows=7, full_train_validation_targets=7, excluded_targets=10, model_fit_allowed_next=0, strategy_replay_allowed=0; Phase217 design_matrix_precommit_complete=1, target_scope_rows=7, feature_binding_rows=42, target_row_observation_scope=384282, row_level_export_allowed=0, model_fit_allowed_next=0, strategy_replay_allowed=0; Phase218 model_fit_precommit_complete=1, dry_run_precommitted_for_phase219=1, model_specs=3, target_contracts=7, feature_contracts=18, phase218_model_fit_execution_allowed=0, strategy_replay_allowed=0; Phase219 model_fit_dry_run_complete=1, event_only_joined_rows=129852, model_fit_rows=21, validation_metric_rows=21, control_rows=42, model_fit_execution=1, strategy_replay_allowed=0, test_rows_used=0; Phase220 validation_interpretation_complete=1, passing_candidates=5, candidate_families=1, best_mse_improvement_vs_base=0.0100934445514009, best_correlation=0.2205753672014153, candidate_opened_for_phase221=1, strategy_replay_allowed=0; Phase221 signal_replay_precommit_complete=1, frozen_candidates=5, signal_rules=5, phase222_replay_precommitted=1, phase221_replay_execution_allowed=0, test_replay_allowed_next=0, profitability_claim_allowed=0; Phase222 signal_replay_dry_run_complete=1, event_only_joined_rows=127215, replay_summary_rows=240, validation_decision_events=89481, best_validation_net_after_cost_bps_proxy=-11.998805192630435, strategy_replay_execution=1, test_rows_used=0, profitability_claim_allowed=0; Phase223 validation_interpretation_complete=1, interpretation_rows=40, positive_net_validation_rows=0, passing_interpretation_rows=0, best_validation_net_after_cost_bps_proxy=-13.420731450576811, best_actual_vs_shuffle_net_edge_bps=1.0000000000000053, phase224_work_order_rows=1, broader_replay_allowed_next=0, test_rows_used=0, profitability_claim_allowed=0; Phase224 closure_or_redesign_complete=1, candidate_set_closed_for_broader=1, candidate_set_closed_for_test=1, failure_modes=4, redesign_routes=3, selected_redesign_route=P224_COST_AWARE_ACTIONABLE_EVENT_LABELS, phase225_work_order_rows=1, model_fit_allowed_next=0, broader_replay_allowed_next=0, profitability_claim_allowed=0; Phase225 cost_aware_redesign_precommit_complete=1, cost_hurdles=2, label_contracts=3, negative_controls=3, selected_route=P224_COST_AWARE_ACTIONABLE_EVENT_LABELS, label_materialization_allowed_next=1, model_fit_allowed_next=0, strategy_replay_allowed=0, test_rows_used=0, profitability_claim_allowed=0; Phase226 cost_aware_label_materialization_complete=1, availability_rows=3, available_horizons=2, blocked_horizons=1, label_partitions=256, total_label_rows=45631, actionable_rows=136, quality_pass_rows=0, sealed_test_rows_available=184909, test_rows_used=0, model_fit_allowed_next=0, profitability_claim_allowed=0; Phase227 quality_interpretation_complete=1, quality_rows=4, horizon_rows=3, failure_modes=4, actionable_rows=136, quality_pass_rows=0, fit_precommit_candidates=0, phase228_work_order_rows=1, model_fit_allowed_next=0, test_rows_used=0, profitability_claim_allowed=0; Phase228 closure_or_relaxation_complete=1, closed_for_fit=1, closed_for_replay=1, redesign_routes=3, guardrails=3, selected_route=P228_SOURCE_EXPANSION_AND_AVAILABLE_HORIZON_REPAIR, phase229_work_order_rows=1, label_materialization_allowed_next=0, threshold_widening_allowed=0, model_fit_allowed_next=0, profitability_claim_allowed=0; Phase229 multi_strategy_search_complete=1, distinct_strategy_ids=12, realistic_profile_rows=24, positive_realistic_candidates=0, positive_any_profile_rows=0, best_strategy=P164_S06_ABSORPTION_REVERSAL, best_annual_net_pnl=-189512.60575493483; Phase230 low_turnover_high_edge_complete=1, variant_group_rows=28162, positive_expanded_groups=0, positive_oracle_signed_groups=0, best_scope=strategy_symbol_date_profile, best_variant=original, best_net_pnl=-100.5200932874, profitability_claim_allowed=0; Phase231 material_new_forms_complete=1, candidate_rows=72, train_pass=7, test_pass=8, synthetic_candidates=3, best_candidate=P231_MICROPRICE_REVERSAL_H3_Q0_9, best_test_net_pnl=229962.8071718807, profitability_claim_allowed=0; Phase232 validation_complete=1, validated_candidates=1, negative_control_pass=3, cost_stress_pass=3, holdout_stability_pass=1, best_candidate=P231_MICROPRICE_REVERSAL_H3_Q0_9, best_test_net_pnl=229962.80717188073, profitability_claim_allowed=0; Phase233 fragility_realism_complete=1, pass=1, neighbor_pass=7, parent_test_2x_cost_net=179609.71039338846, profitability_claim_allowed=0; Phase234 holdout_preparation_complete=1, selected_route=P234_REAL_ANCHOR_EVENT_BAR_ADAPTER_PREP, real_anchor_route_ready=1, required_schema_present=11/11, phase235_work_order_rows=4, profitability_claim_allowed=0; Phase235 real_anchor_replay_complete=1, pass=0, trades=1, net_pnl=637.4164403580107, dates=1, symbols=1, profitability_claim_allowed=0; Phase236 neighbor_search_complete=1, positive_variants=7, breadth_passing_variants=0, best_candidate=P233_MICROPRICE_REVERSAL_H5_Q0_9, best_net_pnl=1447.6958002712238, best_trades=1, profitability_claim_allowed=0; Phase237 threshold_transfer_complete=1, breadth_positive_candidates=3, best_candidate=P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95, best_family=bar_return_reversal, best_net_pnl=7041.523067663933, best_trades=71, phase238_opened=1, profitability_claim_allowed=0; Phase238 validation_precommit_complete=1, candidate=P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95, local_unseen_dates_available=0, min_unseen_dates_required=5, phase239_work_order_rows=4, profitability_claim_allowed=0; Phase239 unseen_date_audit_complete=1, local_unseen_dates=0, target_unseen_dates=5, azure_ready=1, download_plan_rows=7, profitability_claim_allowed=0; Phase240 raw_l2_download_complete=0, partial_attempt=1, target_dates=2026-07-17, completed_files=50787, failed_files=0, completed_dates=1, profitability_claim_allowed=0; Phase241 one_date_complete=1, candidate=P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95, trade_date=2026-07-17, trades=15, net_pnl=700.4370638369003, controls=1/4, survived=0, profitability_claim_allowed=0; Phase242 closed_candidate=P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95, redesign_queue_rows=3, download_more_dates_allowed=0, holdout_tuning_allowed=0, profitability_claim_allowed=0; Phase243 redesign_complete=1, survivors=113, best_candidate=P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9, best_2x_cost_net=5033.27266663252, random_beat=0.997, future_holdout_precommit_allowed=1, profitability_claim_allowed=0; Phase244 precommit_complete=1, frozen_candidate=P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9, min_holdout_dates=2, storage_decision_required=1, download_now_allowed=0, holdout_execution_now=0, profitability_claim_allowed=0; Phase245 storage_audit_complete=1, free_gb=90.4128532409668, projected_required_gb=7.5, local_feasible_space_only=1, cleanup_candidates=25, download_now_allowed=0; Phase246 one_date_complete=1, candidate=P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9, trade_date=2026-07-20, trades=9, net_pnl=645.9481647866867, symbols=9, controls=2/4, survived=0, profitability_claim_allowed=0; Phase247 redesign_precommit_complete=1, parent=P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9, redesign_candidates=4, l2_filter_required=1, forbidden_tuning_dates=2026-07-17;2026-07-20, training_search_allowed_next=1, profitability_claim_allowed=0; Phase248 search_complete=1, variants=1728, cost200_positive=0, controlled=0, survivors=0, best=P248_COMBINED_STRICT_REVERSAL_H8_EQ0_99_BQ0_85_TQ0_8_SP0_75_IQ0_25_RQ0_75, best_cost200=-37.83447968607757, future_holdout_precommit_allowed=0, profitability_claim_allowed=0; Phase249 close_or_broaden_complete=1, closed_scope=single_name_bar_return_reversal_with_top5_depth_filters, selected_next_route=P249_PAIR_OR_BASKET_RELATIVE_VALUE, broaden_queue_rows=4, threshold_relaxation_only_allowed=0, download_now_allowed=0, profitability_claim_allowed=0; Phase250 pair_basket_precommit_complete=1, selected_route=P249_PAIR_OR_BASKET_RELATIVE_VALUE, grouped_symbols=29, candidate_families=4, phase251_allowed=1, download_now_allowed=0, replay_now_allowed=0, profitability_claim_allowed=0; Phase251 pair_basket_search_complete=1, variants=3840, full_top_five_depth_variants=3840, depth_beyond_l1_variants=3840, base_positive=0, cost200_positive=0, survivors=0, best=P251_SECTOR_PAIR_RESIDUAL_REVERSION_H10_RQ0_95_TQ0_8_DQ0_5_SP0_75_IQ0_5_RB1, best_net=-1681.1779513204742, profitability_claim_allowed=0; Phase252 close_or_broaden_complete=1, closed_scope=aggregate_pair_basket_relative_value_on_phase235_event_bars, selected_next_route=P252_RICHER_RAW_TOP5_DEPTH_EVENT_BARS, raw_depth_schema=30/30, download_now_allowed=0, profitability_claim_allowed=0; Phase253 richer_raw_depth_precommit_complete=1, usable_raw_roots=3, schema=38/38, raw_depth_level_columns=30, feature_catalog_rows=26, phase254_allowed=1, profitability_claim_allowed=0; Phase254 richer_raw_depth_materialization_complete=1, event_bars=1636, dates=1, symbols=32, source_ticks=32426, excluded_invalid_ticks=4, hard_gates=8/8, profitability_claim_allowed=0; Phase255 feature_quality_interpretation_complete=1, healthy_features=18/18, healthy_full_depth_features=11/11, max_abs_full_depth_ic=0.1475390528147801, top_full_depth_feature=avg_order_count_imbalance_l1_l5, strategy_search_allowed_next=1, profitability_claim_allowed=0; Phase256 strategy_search_complete=1, variants=2376, full_depth_variants=2376, cost100_positive=0, cost200_positive=0, survivors=0, best=P256_AVG_DEPTH_BEYOND_L1_QTY_IMBALANCE_FOLLOW_H10_TQ0p95_SPQ0p5_CQ0p75, best_cost100=-411.49029712563254, best_cost200=-1218.3826175402583, profitability_claim_allowed=0; Phase257 interpretation_complete=1, closed_taker_threshold=1, full_depth_preserved=1, selected_next_route=P257_PASSIVE_QUEUE_AWARE_SPREAD_CAPTURE_PRECOMMIT, threshold_relaxation_only_allowed=0, profitability_claim_allowed=0; Phase258 passive_queue_precommit_complete=1, route=P258_PASSIVE_QUEUE_AWARE_SPREAD_CAPTURE, families=5, controls=7, full_depth_required=1, l1_only_allowed=0, profitability_claim_allowed=0; Phase259 passive_training_search_complete=1, variants=3888, full_depth_variants=3888, cost100_positive=6, cost200_positive=0, survivors=0, best=P259_P258_PASSIVE_BID_REPLENISHMENT_H10_SPQ0p5_QQ0p5_CQ0p75_I0p05_RQ0p75_CF0p75, best_cost100=7.249843402049745, best_cost200=-75.43135659795024, profitability_claim_allowed=0; Phase260 interpretation_complete=1, close_phase259_for_promotion=1, full_passive_route_closed=0, selected_next_route=P260_PASSIVE_OPPORTUNITY_BREADTH_AND_FILL_MODEL_REPAIR_PRECOMMIT, full_depth_preserved=1, profitability_claim_allowed=0; Phase261 passive_repair_precommit_complete=1, route=P261_PASSIVE_OPPORTUNITY_BREADTH_AND_FILL_MODEL_REPAIR, fill_grid=12, families=5, full_depth_required=1, levels_2_to_5_required=1, l1_only_allowed=0, profitability_claim_allowed=0; Phase262 passive_training_search_complete=1, variants=2592, full_depth_variants=2592, levels_2_to_5_variants=2592, l1_only_variants=0, fill_models=12, cost100_positive=5, cost200_positive=0, survivors=0, best=P262_P262_TWO_SIDED_SPREAD_CAPTURE_LOW_CHURN_H10_SPQ0p75_RQ0p4_CQ0p4_PQ0p5_I0p0_CF0p5_P261_FILL_conservative_low_fill_QA0p75, best_cost100=-17.14255650345248, best_cost200=-55.442989223856685, profitability_claim_allowed=0; Phase263 interpretation_complete=1, close_passive_route=1, full_depth_preserved=1, threshold_relaxation_only_allowed=0, selected_next_route=P263_FULL_DEPTH_LIQUIDITY_SHOCK_ABSORPTION_EVENT_PRECOMMIT, profitability_claim_allowed=0; Phase264 liquidity_shock_precommit_complete=1, route=P264_FULL_DEPTH_LIQUIDITY_SHOCK_ABSORPTION_EVENT_MODEL, features=16, families=5, controls=8, full_depth_required=1, levels_2_to_5_required=1, l1_only_allowed=0, profitability_claim_allowed=0. Phase265 liquidity_shock_training_search_complete=1, variants=432, full_depth_variants=432, levels_2_to_5_variants=432, l1_only_variants=0, cost100_positive=38, cost200_positive=2, survivors=0, best=P265_P265_L2L5_BID_ABSORPTION_CONTINUATION_H10_IQ0p9_SQ0p75_SPHIGH, best_cost100=782.0356498346316, best_cost200=37.90484983463176, profitability_claim_allowed=0. Phase266 interpretation_complete=1, close_phase265_for_replay=1, full_depth_preserved=1, selected_next_route=P266_FULL_DEPTH_LIQUIDITY_SHOCK_BREADTH_AND_SHUFFLE_ROBUSTNESS_REPAIR_PRECOMMIT, best_cost200_avg=4.211649981625751, best_shuffle_margin=1.1368683772161603e-13, profitability_claim_allowed=0. Phase267 repair_precommit_complete=1, exploratory_lane_enabled=1, exploratory_controls_are_filters=0, acceptance_events=30, acceptance_symbols=8, full_depth_required=1, levels_2_to_5_required=1, l1_only_allowed=0, profitability_claim_allowed=0. Phase268 two_lane_training_search_complete=1, variants=1200, full_depth_variants=1200, levels_2_to_5_variants=1200, l1_only_variants=0, exploratory_candidates=22, annualized_research_leads=17, cost200_annualized_research_leads=0, acceptance_grade_candidates=0, best=P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH, best_cost100_annualized=197.07298375832715, best_cost200_annualized=9.552022158327203, best_cost200=37.90484983463176, profitability_claim_allowed=0. Phase269 interpretation_complete=1, preserve_research_leads=1, do_not_claim_portfolio_annual_return=1, do_not_promote_or_replay=1, selected_next_route=P269_FIXED_CAPITAL_CONCURRENCY_AND_CAPACITY_RETURN_PRECOMMIT, profitability_claim_allowed=0. Phase270 fixed_capital_precommit_complete=1, capital_contract_rows=8, concurrency_capacity_rows=8, unlimited_capital_allowed=0, portfolio_claim_without_scheduler_allowed=0, fixed_proxy_as_portfolio_allowed=0, profitability_claim_allowed=0. Phase271 fixed_capital_analysis_complete=1, scopes=18, scenarios=4320, cost100_above12=58, cost200_above12=6, best=P271_CAND003_CAP100000_NOT100000_CONC1_COST100, best_mechanical_annualized=137.4701128605055, portfolio_claim_allowed=0, profitability_claim_allowed=0. Phase272 interpretation_complete=1, priority_candidates=2, pooled_above12=0, best_candidate=P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION, best=P271_CAND003_CAP100000_NOT100000_CONC1_COST100, selected_next_route=P272_FOCUSED_CAPITAL_AWARE_CANDIDATE_FOLLOWTHROUGH_SEARCH, portfolio_claim_allowed=0, profitability_claim_allowed=0. Phase273 followthrough_search_complete=1, scopes=3, order_policies=5, scenarios=3600, cost100_above12=332, cost200_above12=121, best=P271_P273_TOP2_PRIORITY_SUBSET_TIME_REVERSE_RANK_CAP100000_NOT125000_CONC1_COST100, best_mechanical_annualized=190.6353099362237, portfolio_claim_allowed=0, profitability_claim_allowed=0. Phase274 interpretation_complete=1, cost200_survivor_profiles=3, median_positive_profiles=2, worst_case_positive_profiles=0, best_scope_profile=TOP2_PRIORITY_SUBSET:cost200, selected_next_route=P274_FOCUSED_CAPITAL_MULTIDAY_SYNTHETIC_FOLLOWTHROUGH_SEARCH, portfolio_claim_allowed=0, profitability_claim_allowed=0. Phase275 multiday_synthetic_complete=1, scenarios=4800, synthetic_dates=8, cost100_above12=2, cost200_above12=0, best=P271_P275_TOP2_PRIORITY_SUBSET_REVERSE_RANK_TIME_BASE_BOOTSTRAP_SEED202_CAP100000_NOT100000_CONC1_COST100, best_synthetic_annualized=15.091000980326113, portfolio_claim_allowed=0, profitability_claim_allowed=0. Phase276 interpretation_complete=1, selected_next_route=P276_COST_ROBUST_FULL_DEPTH_REDESIGN_SEARCH, normal_cost_sparse_positive_profiles=2, cost200_failed_profiles=3, as_is_promotion_allowed=0, portfolio_claim_allowed=0, profitability_claim_allowed=0. Phase277 cost_robust_redesign_complete=1, variants=47, scenarios=282, cost200_above12=0, best_variant=P277_REPLENISH_WITHDRAW_GE_Q90, best_cost200_annualized=9.370481974163102, profitability_claim_allowed=0. | run_phase278_cost_robust_redesign_interpretation_no_paper_live |
| top_five_depth_passive | closed_clean_falsification | Phase136 Outcome A closes the branch after Phase132 kill-switch and Phase116 blocklist verification. | do_not_open_phase134_or_phase135_for_this_branch |
| synthetic_strategy_discovery | cost_robust_redesign_interpretation_open | Phase229 ranked 12 strategy ids and found 0 positive realistic candidates; Phase230 tested 28162 original/inverse/oracle variant groups and found 0 positive expanded groups and 0 positive oracle-signed upper-bound groups; Phase231 replayed 72 material-new candidates and found 3 train+test synthetic candidates, led by P231_MICROPRICE_REVERSAL_H3_Q0_9 with test net P&L 229962.8071718807; Phase232 validated 1 candidate after cost stress, side-flip, random-side and holdout stability checks; Phase233 passed fragility/realism with 7 passing neighbors and parent test 2x cost net P&L 179609.71039338846; Phase234 selected P234_REAL_ANCHOR_EVENT_BAR_ADAPTER_PREP with real_anchor_route_ready=1 and 11/11 required real L2 schema rows present; Phase235 real-anchor replay selected 1 trades with net P&L 637.4164403580107, but breadth was 1 dates and 1 symbols; Phase236 replayed 12 neighbors and found 7 positive real-anchor variants, but 0 breadth-passing variants; Phase237 evaluated 3584 threshold-transfer variants and opened P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 for Phase238 with net P&L 7041.523067663933, 71 trades, 6 dates and 21 symbols; Phase238 froze P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 and found 0 local unseen validation dates available; Phase239 found Azure Files target unseen dates reachable with azure_ready=1, while local unseen dates remain 0; Phase240 started/resumed raw unseen L2 download with completed_files=50787, failed_files=0, completed_dates=1; Phase241 replayed the frozen candidate on one unseen date with trades=15, net P&L=700.4370638369003, controls=1/4, survived=0; Phase242 closed P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 and opened 3 redesign rows without more downloads or holdout tuning; Phase243 found 113 cost-stress/random-side survivors, led by P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9, with 2x-cost net 5033.27266663252 and random beat 0.997; Phase244 froze P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 for future holdout with storage_decision_required=1, download_now_allowed=0; Phase245 found local space feasible by estimate with free_gb=90.4128532409668, projected_required_gb=7.5, but still blocks downloads until policy choice; Phase246 downloaded and replayed one fresh unseen date 2026-07-20, producing trades=9, net P&L=645.9481647866867, controls=2/4, survived=0; Phase247 precommitted 4 L2-imbalance/regime-filter redesign families with holdout tuning dates 2026-07-17;2026-07-20 excluded; Phase248 evaluated 1728 combined-filter variants and found 0 controlled survivors, with 0 positive at 2x cost; Phase249 closed single_name_bar_return_reversal_with_top5_depth_filters and selected P249_PAIR_OR_BASKET_RELATIVE_VALUE as the next materially different route; Phase250 precommitted pair/basket relative-value search with grouped_symbols=29, candidate_families=4, no_download=0, replay_now=0, profitability_claim_allowed=0; Phase251 executed 3840 pair/basket variants with full_top_five_depth_variants=3840 and depth_beyond_l1_variants=3840, finding base_positive=0, cost200_positive=0 and survivors=0; Phase252 closed aggregate_pair_basket_relative_value_on_phase235_event_bars and selected P252_RICHER_RAW_TOP5_DEPTH_EVENT_BARS after confirming raw_depth_schema=30/30; Phase253 precommitted richer raw top-five depth materialization with usable_raw_roots=3, schema=38/38, feature_catalog_rows=26 and phase254_allowed=1; Phase254 materialized 1636 richer raw-depth event bars from 32426 source ticks across 32 symbols, excluding 4 invalid raw ticks before aggregation; Phase255 audited 18 features, including 11 full-depth features, found healthy_full_depth=11, max_abs_full_depth_ic=0.1475390528147801, and opened strategy_search_allowed_next=1; Phase256 searched 2376 full-depth cost-aware variants, found cost100_positive=0, cost200_positive=0, survivors=0, with best_cost100=-411.49029712563254 and best_cost200=-1218.3826175402583; Phase257 closed_taker_threshold=1, preserved_full_depth=1, selected_next_route=P257_PASSIVE_QUEUE_AWARE_SPREAD_CAPTURE_PRECOMMIT, next_route_contract_rows=7; Phase258 precommitted P258_PASSIVE_QUEUE_AWARE_SPREAD_CAPTURE with families=5, controls=7, full_depth_required=1, l1_only_allowed=0; Phase259 searched 3888 passive full-depth variants, found cost100_positive=6, cost200_positive=0, survivors=0, best_cost100=7.249843402049745, best_cost200=-75.43135659795024; Phase260 closed Phase259 for promotion=1, kept full_passive_route_closed=0, and selected P260_PASSIVE_OPPORTUNITY_BREADTH_AND_FILL_MODEL_REPAIR_PRECOMMIT with contract_rows=7; Phase261 precommitted P261_PASSIVE_OPPORTUNITY_BREADTH_AND_FILL_MODEL_REPAIR with fill_grid=12, families=5, full_depth_required=1, levels_2_to_5_required=1, l1_only_allowed=0; Phase262 searched 2592 passive full-depth/fill-model variants, found cost100_positive=5, cost200_positive=0, survivors=0, best_cost100=-17.14255650345248, best_cost200=-55.442989223856685; Phase263 closed_passive_route=1, preserved_full_depth=1, and selected P263_FULL_DEPTH_LIQUIDITY_SHOCK_ABSORPTION_EVENT_PRECOMMIT with contract_rows=7; Phase264 precommitted P264_FULL_DEPTH_LIQUIDITY_SHOCK_ABSORPTION_EVENT_MODEL with features=16, families=5, labels=5, controls=8, full_depth_required=1, levels_2_to_5_required=1, l1_only_allowed=0; Phase265 searched 432 full-depth liquidity-shock variants, full_depth_variants=432, levels_2_to_5_variants=432, l1_only_variants=0, cost100_positive=38, cost150_positive=6, cost200_positive=2, survivors=0, best=P265_P265_L2L5_BID_ABSORPTION_CONTINUATION_H10_IQ0p9_SQ0p75_SPHIGH, best_cost100=782.0356498346316, best_cost200=37.90484983463176; Phase266 interpreted Phase265 with close_phase265_for_replay=1, recognized_unaccepted_2x_pocket=1, full_depth_preserved=1, threshold_relaxation_only_allowed=0, selected_next_route=P266_FULL_DEPTH_LIQUIDITY_SHOCK_BREADTH_AND_SHUFFLE_ROBUSTNESS_REPAIR_PRECOMMIT, best_cost200_avg=4.211649981625751, best_shuffle_margin=1.1368683772161603e-13; Phase267 precommitted a two-lane repair with exploratory_lane_enabled=1, exploratory_controls_are_filters=0, acceptance_events=30, acceptance_symbols=8, full_depth_required=1, levels_2_to_5_required=1, l1_only_allowed=0; Phase268 searched 1200 two-lane full-depth variants, found exploratory_candidates=22, annualized_research_leads=17, cost200_annualized_research_leads=0, acceptance_grade_candidates=0, cost100_positive=25, cost200_positive=2, best=P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH, best_cost100_annualized=197.07298375832715, best_cost200_annualized=9.552022158327203, best_shuffle_margin=0.0; Phase269 ranked 17 fixed-notional annualized research leads, preserved_research_leads=1, portfolio_return_claim_allowed=0, selected_next_route=P269_FIXED_CAPITAL_CONCURRENCY_AND_CAPACITY_RETURN_PRECOMMIT; Phase270 precommitted capital/concurrency/capacity return modeling with capital_contract_rows=8, concurrency_capacity_rows=8, unlimited_capital_allowed=0, fixed_proxy_as_portfolio_allowed=0; Phase271 scheduled pooled and per-candidate fixed-capital scenarios with scopes=18, scenarios=4320, cost100_above12=58, cost200_above12=6, best=P271_CAND003_CAP100000_NOT100000_CONC1_COST100, best_mechanical_annualized=137.4701128605055, portfolio_claim_allowed=0; Phase272 interpreted those pockets with priority_candidates=2, pooled_above12=0, best_candidate=P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION, selected_next_route=P272_FOCUSED_CAPITAL_AWARE_CANDIDATE_FOLLOWTHROUGH_SEARCH; Phase273 follow-through searched scopes=3, order_policies=5, scenarios=3600, cost100_above12=332, cost200_above12=121, best=P271_P273_TOP2_PRIORITY_SUBSET_TIME_REVERSE_RANK_CAP100000_NOT125000_CONC1_COST100, best_mechanical_annualized=190.6353099362237; Phase274 interpreted Phase273 with cost200_survivor_profiles=3, median_positive_profiles=2, worst_case_positive_profiles=0, selected_next_route=P274_FOCUSED_CAPITAL_MULTIDAY_SYNTHETIC_FOLLOWTHROUGH_SEARCH; Phase275 executed multiday synthetic follow-through with scenarios=4800, synthetic_dates=8, cost100_above12=2, cost200_above12=0, best=P271_P275_TOP2_PRIORITY_SUBSET_REVERSE_RANK_TIME_BASE_BOOTSTRAP_SEED202_CAP100000_NOT100000_CONC1_COST100, best_synthetic_annualized=15.091000980326113; Phase276 interpreted Phase275 as fragile with normal_cost_sparse_positive_profiles=2, cost200_failed_profiles=3, selected_next_route=P276_COST_ROBUST_FULL_DEPTH_REDESIGN_SEARCH; Phase277 searched cost-robust full-depth redesign variants=47, scenarios=282, cost200_above12=0, best_variant=P277_REPLENISH_WITHDRAW_GE_Q90, best_cost200_annualized=9.370481974163102. | run_phase278_cost_robust_redesign_interpretation_no_paper_live |
| dense_synthetic_replay | not_promoted | Partial/smoke dense replay artifacts remain non-promotional and do not override replay gates. | only_continue_if_precommitted_and_not_blocklisted |

## Global Gate Evaluation

| gate | pass | observed | required | severity |
| --- | --- | --- | --- | --- |
| phase149_real_l2_replay_gate_closed | True | 0 | 0 | hard |
| phase149_real_receive_flow_source_gate_open_or_explicitly_blocked | True | 1 | 0_or_1_tracked_by_phase172 | hard |
| phase149_secure_download_gate_recorded | True | 1 | 1 | hard |
| phase149_secure_orchestrator_replay_gate_closed | True | 0 | 0 | hard |
| phase149_receive_flow_feature_schema_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_feature_schema_replay_gate_closed | True | 0 | 0 | hard |
| phase149_receive_flow_materializer_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_materializer_replay_gate_closed | True | 0 | 0 | hard |
| phase149_receive_flow_quality_audit_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_quality_audit_replay_gate_closed | True | 0 | 0 | hard |
| phase149_receive_flow_handoff_precommit_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_handoff_replay_gate_closed | True | 0 | 0 | hard |
| phase149_receive_flow_strategy_family_precommit_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_strategy_family_replay_gate_closed | True | 0 | 0 | hard |
| phase149_receive_flow_cost_latency_label_precommit_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_cost_latency_label_replay_gate_closed | True | 0 | 0 | hard |
| phase149_receive_flow_label_materialization_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_label_materialization_replay_gate_closed | True | 0 | 0 | hard |
| phase149_receive_flow_label_quality_leakage_audit_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_label_quality_leakage_replay_gate_closed | True | 0 | 0 | hard |
| phase149_receive_flow_replay_readiness_precommit_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_replay_readiness_replay_gate_closed | True | 0 | 0 | hard |
| phase149_receive_flow_replay_readiness_pnl_gate_closed | True | 0 | 0 | hard |
| phase149_receive_flow_train_validation_dry_run_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_train_validation_dry_run_test_gate_closed | True | 0 | 0 | hard |
| phase149_receive_flow_train_validation_dry_run_promotion_gate_closed | True | 0 | 0 | hard |
| phase149_receive_flow_train_validation_dry_run_paper_live_gate_closed | True | 0 | 0 | hard |
| phase149_receive_flow_validation_interpretation_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_validation_interpretation_test_rows_closed | True | 0 | 0 | hard |
| phase149_receive_flow_validation_interpretation_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_validation_interpretation_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_validation_interpretation_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_current_family_closure_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_current_family_reuse_without_redesign_closed | True | 0 | 0 | hard |
| phase149_receive_flow_current_family_closure_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_current_family_closure_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_current_family_closure_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_cost_aware_sparse_candidate_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_cost_aware_sparse_candidate_test_rows_closed | True | 0 | 0 | hard |
| phase149_receive_flow_cost_aware_sparse_candidate_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_cost_aware_sparse_candidate_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_cost_aware_sparse_candidate_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_sparse_candidate_interpretation_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_sparse_candidate_interpretation_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_sparse_candidate_interpretation_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_sparse_candidate_interpretation_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_test_precommit_decision_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_test_precommit_allowed_closed | True | 0 | 0 | hard |
| phase149_receive_flow_test_replay_still_closed | True | 0 | 0 | hard |
| phase149_receive_flow_test_precommit_decision_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_test_precommit_decision_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase190_diagnostic_spec_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase190_test_replay_not_executed | True | 0 | 0 | hard |
| phase149_receive_flow_phase190_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase190_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase190_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase191_diagnostic_precommit_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase191_test_replay_not_executed | True | 0 | 0 | hard |
| phase149_receive_flow_phase191_test_result_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase191_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase191_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase191_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase192_real_validation_download_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase192_test_replay_not_executed | True | 0 | 0 | hard |
| phase149_receive_flow_phase192_test_result_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase192_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase192_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase193_validation_extension_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase193_test_replay_not_executed | True | 0 | 0 | hard |
| phase149_receive_flow_phase193_test_result_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase193_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase193_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase194_fragility_decision_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase194_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase194_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase194_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase195_redesign_search_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase195_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase195_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase195_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase196_expanded_model_search_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase196_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase196_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase196_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase197_non_receive_flow_feature_precommit_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase197_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase197_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase197_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase197_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase198_context_model_search_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase198_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase198_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase198_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase199_branch_decision_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase199_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase199_test_precommit_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase199_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase199_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase199_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase200_material_hypothesis_precommit_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase200_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase200_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase200_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase200_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase201_stage01_label_expansion_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase201_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase201_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase201_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase201_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase202_passive_feature_redesign_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase202_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase202_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase202_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase202_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase203_redesigned_label_materialization_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase203_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase203_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase203_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase203_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase204_passive_redesign_closure_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase204_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase204_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase204_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase204_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase205_material_new_source_precommit_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase205_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase205_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase205_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase205_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase206_nonoverlap_feature_contract_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase206_model_fit_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase206_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase206_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase206_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase206_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase207_allowed_feature_matrix_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase207_model_fit_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase207_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase207_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase207_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase207_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase208_feature_matrix_quality_gate_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase208_model_fit_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase208_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase208_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase208_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase208_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase209_model_fit_precommit_spec_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase209_model_fit_execution_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase209_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase209_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase209_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase209_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase210_train_validation_model_fit_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase210_model_fit_executed | True | 1 | 1 | hard |
| phase149_receive_flow_phase210_test_rows_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase210_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase210_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase210_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase210_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase210_profitability_claim_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase211_validation_interpretation_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase211_candidate_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase211_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase211_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase211_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase211_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase211_profitability_claim_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase212_closure_redesign_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase212_candidate_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase212_model_fit_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase212_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase212_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase212_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase212_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase212_profitability_claim_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase213_material_source_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase213_model_fit_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase213_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase213_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase213_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase213_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase213_profitability_claim_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase214_label_materialization_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase214_model_fit_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase214_sealed_test_rows_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase214_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase214_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase214_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase214_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase214_profitability_claim_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase215_label_quality_interpretation_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase215_model_fit_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase215_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase215_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase215_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase215_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase215_profitability_claim_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase216_event_only_target_precommit_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase216_model_fit_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase216_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase216_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase216_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase216_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase216_profitability_claim_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase217_design_matrix_precommit_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase217_row_level_export_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase217_model_fit_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase217_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase217_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase217_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase217_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase217_profitability_claim_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase218_model_fit_precommit_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase218_phase219_fit_dry_run_precommitted | True | 1 | 1 | hard |
| phase149_receive_flow_phase218_model_fit_execution_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase218_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase218_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase218_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase218_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase218_profitability_claim_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase219_model_fit_dry_run_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase219_model_fit_execution_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase219_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase219_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase219_test_rows_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase219_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase219_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase219_profitability_claim_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase220_validation_interpretation_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase220_phase221_candidate_opened | True | 1 | 1 | hard |
| phase149_receive_flow_phase220_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase220_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase220_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase220_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase220_profitability_claim_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase221_signal_replay_precommit_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase221_phase222_replay_dry_run_precommitted | True | 1 | 1 | hard |
| phase149_receive_flow_phase221_replay_execution_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase221_next_replay_scope_opened | True | 1 | 1 | hard |
| phase149_receive_flow_phase221_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase221_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase221_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase221_profitability_claim_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase222_signal_replay_dry_run_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase222_strategy_replay_execution_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase222_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase222_test_rows_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase222_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase222_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase222_profitability_claim_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase223_validation_interpretation_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase223_no_passing_interpretation_rows | True | 0 | 0 | hard |
| phase149_receive_flow_phase223_phase224_work_order_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase223_broader_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase223_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase223_test_rows_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase223_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase223_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase223_profitability_claim_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase224_closure_or_redesign_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase224_candidate_set_closed_for_broader | True | 1 | 1 | hard |
| phase149_receive_flow_phase224_candidate_set_closed_for_test | True | 1 | 1 | hard |
| phase149_receive_flow_phase224_reuse_without_redesign_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase224_phase225_work_order_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase224_model_fit_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase224_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase224_broader_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase224_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase224_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase224_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase224_profitability_claim_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase225_cost_aware_redesign_precommit_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase225_label_materialization_next_opened | True | 1 | 1 | hard |
| phase149_receive_flow_phase225_phase226_work_order_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase225_model_fit_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase225_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase225_broader_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase225_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase225_test_rows_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase225_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase225_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase225_profitability_claim_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase226_label_materialization_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase226_available_horizons_materialized | True | 2 | 2 | hard |
| phase149_receive_flow_phase226_actionable_rows_recorded | True | 136 | >0 | hard |
| phase149_receive_flow_phase226_quality_failure_recorded | True | 0 | 0 | hard |
| phase149_receive_flow_phase226_model_fit_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase226_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase226_broader_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase226_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase226_test_rows_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase226_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase226_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase226_profitability_claim_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase227_label_quality_interpretation_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase227_no_fit_precommit_candidates | True | 0 | 0 | hard |
| phase149_receive_flow_phase227_phase228_work_order_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase227_model_fit_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase227_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase227_broader_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase227_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase227_test_rows_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase227_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase227_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase227_profitability_claim_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase228_closure_or_relaxation_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase228_current_label_set_closed_for_fit | True | 1 | 1 | hard |
| phase149_receive_flow_phase228_current_label_set_closed_for_replay | True | 1 | 1 | hard |
| phase149_receive_flow_phase228_phase229_work_order_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_phase228_label_materialization_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase228_threshold_widening_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase228_model_fit_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase228_strategy_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase228_broader_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase228_test_replay_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase228_test_rows_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase228_promotion_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase228_paper_live_closed | True | 0 | 0 | hard |
| phase149_receive_flow_phase228_profitability_claim_closed | True | 0 | 0 | hard |
| phase149_deep_book_branch_closed | True | 1 | 1 | hard |
| phase149_no_promoted_strategy_replay | True | 0 | 0 | hard |

## Phase Status Ledger

| phase | runner_count | output_rows | has_runner | has_outputs | has_acceptance_summary | status | branch | strategy_replay_allowed | pnl_allowed | test_rows_used | test_replay_execution | test_result_allowed | test_replay_allowed_next | untouched_test_replay_precommit_allowed | reuse_without_redesign_allowed | additional_validation_breadth_available_now | may_relabel_test_as_validation | breadth_warning | date_count_warning | promotion_allowed | paper_or_live_acceptance_allowed | next_action | runner | output_dir |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 198 | 1 | 1 | True | True | True | non_receive_flow_context_model_search_no_train_survivor_no_test | real_receive_flow_source |  |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | expand_or_pause_non_receive_flow_context_branch_no_test | scripts\run_phase198_non_receive_flow_context_model_search.py | outputs\phase198 |
| 199 | 1 | 1 | True | True | True | current_receive_flow_context_branch_paused_material_redesign_required_no_test | real_receive_flow_source | 0 |  |  |  |  | 0 | 0 |  |  |  |  |  | 0 | 0 | run_phase200_material_new_hypothesis_precommit_no_test | scripts\run_phase199_branch_pause_or_material_redesign_decision.py | outputs\phase199 |
| 200 | 1 | 1 | True | True | True | material_new_passive_queue_hypothesis_precommitted_label_expansion_pending_no_test | real_receive_flow_source | 0 |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase201_passive_queue_label_only_stage01_expansion_no_replay | scripts\run_phase200_material_new_hypothesis_precommit.py | outputs\phase200 |
| 201 | 1 | 1 | True | True | True | passive_queue_stage01_label_expansion_complete_no_replay_candidate_redesign_pending | real_receive_flow_source | 0 |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase202_passive_feature_redesign_precommit_no_replay | scripts\run_phase201_passive_queue_label_stage01_acceptance.py | outputs\phase201 |
| 202 | 1 | 1 | True | True | True | passive_feature_redesign_precommitted_label_materialization_pending_no_replay | real_receive_flow_source | 0 |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase203_redesigned_passive_label_materialization_no_replay | scripts\run_phase202_passive_feature_redesign_precommit.py | outputs\phase202 |
| 203 | 1 | 1 | True | True | True | redesigned_passive_labels_materialized_candidate_gate_closed_no_replay | real_receive_flow_source | 0 |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | redesign_passive_labels_or_expand_label_materialization_before_replay | scripts\run_phase203_redesigned_passive_label_materialization.py | outputs\phase203 |
| 204 | 1 | 1 | True | True | True | passive_redesign_closed_for_replay_material_new_source_or_label_breadth_pending_no_replay | real_receive_flow_source | 0 |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase205_material_new_source_precommit_or_label_breadth_plan_no_replay | scripts\run_phase204_passive_redesign_closure_decision.py | outputs\phase204 |
| 205 | 1 | 1 | True | True | True | material_new_source_precommitted_phase206_contract_pending_no_replay | real_receive_flow_source | 0 |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase206_selected_source_nonoverlap_feature_contract_no_replay | scripts\run_phase205_material_new_source_precommit.py | outputs\phase205 |
| 206 | 1 | 1 | True | True | True | selected_source_nonoverlap_feature_contract_complete_phase207_matrix_pending_no_replay | real_receive_flow_source | 0 |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase207_allowed_feature_matrix_precommit_no_model_no_replay | scripts\run_phase206_selected_source_nonoverlap_feature_contract.py | outputs\phase206 |
| 207 | 1 | 1 | True | True | True | allowed_feature_matrix_precommitted_phase208_quality_gate_pending_no_model_no_replay | real_receive_flow_source | 0 |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase208_feature_matrix_quality_gate_no_model_no_replay | scripts\run_phase207_allowed_feature_matrix_precommit.py | outputs\phase207 |
| 208 | 1 | 1 | True | True | True | feature_matrix_quality_gate_complete_phase209_model_precommit_pending_no_execution_no_replay | real_receive_flow_source | 0 |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase209_model_fit_precommit_spec_no_execution_no_replay | scripts\run_phase208_feature_matrix_quality_gate.py | outputs\phase208 |
| 209 | 1 | 1 | True | True | True | model_fit_precommit_spec_complete_phase210_train_validation_fit_dry_run_pending_no_replay_no_test | real_receive_flow_source | 0 |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase210_train_validation_model_fit_dry_run_no_replay_no_test | scripts\run_phase209_model_fit_precommit_spec.py | outputs\phase209 |
| 210 | 1 | 1 | True | True | True | train_validation_model_fit_dry_run_complete_phase211_validation_interpretation_pending_no_replay_no_test | real_receive_flow_source | 0 |  | 0 |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase211_model_fit_validation_interpretation_no_replay_no_test | scripts\run_phase210_train_validation_model_fit_dry_run.py | outputs\phase210 |
| 211 | 1 | 1 | True | True | True | model_fit_validation_interpretation_complete_phase212_closure_or_redesign_pending_no_replay_no_test | real_receive_flow_source | 0 |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase212_model_family_closure_or_redesign_precommit_no_replay_no_test | scripts\run_phase211_model_fit_validation_interpretation.py | outputs\phase211 |
| 212 | 1 | 1 | True | True | True | model_family_closure_or_redesign_precommit_complete_phase213_material_new_source_pending_no_replay_no_test | real_receive_flow_source | 0 |  |  |  |  | 0 |  | 0 |  |  |  |  | 0 | 0 | run_phase213_material_new_model_source_precommit_no_replay_no_test | scripts\run_phase212_model_family_closure_or_redesign_precommit.py | outputs\phase212 |
| 213 | 1 | 1 | True | True | True | material_new_model_source_precommit_complete_phase214_event_surprise_label_materialization_pending_no_model_no_replay_no_test | real_receive_flow_source | 0 |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase214_event_surprise_label_contract_materialization_no_model_no_replay_no_test | scripts\run_phase213_material_new_model_source_precommit.py | outputs\phase213 |
| 214 | 1 | 1 | True | True | True | event_surprise_label_materialization_complete_phase215_quality_interpretation_pending_no_model_no_replay_no_test | real_receive_flow_source | 0 |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase215_event_surprise_label_quality_interpretation_no_model_no_replay_no_test | scripts\run_phase214_event_surprise_label_materialization.py | outputs\phase214 |
| 215 | 1 | 1 | True | True | True | event_surprise_label_quality_interpretation_complete_phase216_event_only_target_precommit_pending_no_model_no_replay_no_test | real_receive_flow_source | 0 |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase216_event_surprise_label_redesign_or_event_only_target_precommit_no_model_no_replay_no_test | scripts\run_phase215_event_surprise_label_quality_interpretation.py | outputs\phase215 |
| 216 | 1 | 1 | True | True | True | event_surprise_event_only_target_precommit_complete_phase217_design_matrix_precommit_pending_no_model_no_replay_no_test | real_receive_flow_source | 0 |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase217_event_only_design_matrix_precommit_no_model_no_replay_no_test | scripts\run_phase216_event_surprise_event_only_target_precommit.py | outputs\phase216 |
| 217 | 1 | 1 | True | True | True | event_only_design_matrix_precommit_complete_phase218_model_fit_precommit_or_stop_pending_no_replay_no_test | real_receive_flow_source | 0 |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase218_event_only_model_fit_precommit_or_stop_no_replay_no_test | scripts\run_phase217_event_only_design_matrix_precommit.py | outputs\phase217 |
| 218 | 1 | 1 | True | True | True | event_only_model_fit_precommit_complete_phase219_train_validation_fit_dry_run_pending_no_replay_no_test | real_receive_flow_source | 0 |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase219_event_only_train_validation_model_fit_dry_run_no_replay_no_test | scripts\run_phase218_event_only_model_fit_precommit_or_stop.py | outputs\phase218 |
| 219 | 1 | 1 | True | True | True | event_only_train_validation_model_fit_dry_run_complete_phase220_validation_interpretation_pending_no_replay_no_test | real_receive_flow_source | 0 |  | 0 |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase220_event_only_model_fit_validation_interpretation_no_replay_no_test | scripts\run_phase219_event_only_train_validation_model_fit_dry_run.py | outputs\phase219 |
| 220 | 1 | 1 | True | True | True | event_only_model_fit_validation_interpretation_complete_phase221_signal_replay_precommit_or_stop_pending_no_replay_no_test | real_receive_flow_source | 0 |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase221_event_only_signal_replay_precommit_or_stop_no_replay_no_test | scripts\run_phase220_event_only_model_fit_validation_interpretation.py | outputs\phase220 |
| 221 | 1 | 1 | True | True | True | event_only_signal_replay_precommit_complete_phase222_train_validation_replay_dry_run_pending_no_test | real_receive_flow_source |  |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase222_event_only_train_validation_signal_replay_dry_run_no_test | scripts\run_phase221_event_only_signal_replay_precommit_or_stop.py | outputs\phase221 |
| 222 | 1 | 1 | True | True | True | event_only_train_validation_signal_replay_dry_run_complete_phase223_validation_interpretation_pending_no_test | real_receive_flow_source |  |  | 0 |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase223_event_only_signal_replay_validation_interpretation_no_test | scripts\run_phase222_event_only_train_validation_signal_replay_dry_run.py | outputs\phase222 |
| 223 | 1 | 1 | True | True | True | event_only_signal_replay_validation_interpretation_complete_phase224_closure_or_redesign_precommit_pending_no_test | real_receive_flow_source |  |  | 0 |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase224_event_only_signal_replay_closure_or_redesign_precommit_no_test | scripts\run_phase223_event_only_signal_replay_validation_interpretation.py | outputs\phase223 |
| 224 | 1 | 1 | True | True | True | event_only_signal_replay_candidate_set_closed_phase225_cost_aware_redesign_precommit_pending_no_fit_no_replay_no_test | real_receive_flow_source | 0 |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase225_cost_aware_event_source_redesign_precommit_no_fit_no_replay_no_test | scripts\run_phase224_event_only_signal_replay_closure_or_redesign_precommit.py | outputs\phase224 |
| 225 | 1 | 1 | True | True | True | cost_aware_event_source_redesign_precommit_complete_phase226_label_materialization_pending_no_fit_no_replay_no_test | real_receive_flow_source | 0 |  | 0 |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase226_cost_aware_event_label_materialization_dry_run_no_fit_no_replay_no_test | scripts\run_phase225_cost_aware_event_source_redesign_precommit.py | outputs\phase225 |
| 226 | 1 | 1 | True | True | True | cost_aware_event_label_materialization_complete_phase227_quality_interpretation_pending_no_fit_no_replay_no_test | real_receive_flow_source | 0 |  | 0 |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase227_cost_aware_event_label_quality_interpretation_no_fit_no_replay_no_test | scripts\run_phase226_cost_aware_event_label_materialization_dry_run.py | outputs\phase226 |
| 227 | 1 | 1 | True | True | True | cost_aware_event_label_quality_interpretation_complete_phase228_closure_or_redesign_pending_no_fit_no_replay_no_test | real_receive_flow_source | 0 |  | 0 |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase228_cost_aware_label_redesign_closure_or_relaxation_precommit_no_fit_no_replay_no_test | scripts\run_phase227_cost_aware_event_label_quality_interpretation.py | outputs\phase227 |
| 228 | 1 | 1 | True | True | True | cost_aware_label_set_closed_phase229_source_expansion_precommit_pending_no_materialization_no_fit_no_replay_no_test | real_receive_flow_source | 0 |  | 0 |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase229_cost_aware_source_expansion_precommit_no_materialization_no_fit_no_replay_no_test | scripts\run_phase228_cost_aware_label_redesign_closure_or_relaxation_precommit.py | outputs\phase228 |
| 229 | 1 | 1 | True | True | True | multi_strategy_profitability_search_complete | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase230_expand_low_turnover_high_edge_strategy_search_no_generator_profit_tuning | scripts\run_phase229_multi_strategy_profitability_search.py | outputs\phase229 |
| 230 | 1 | 1 | True | True | True | low_turnover_high_edge_expansion_complete | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase231_material_new_strategy_forms_longer_horizon_or_pessimistic_passive_no_generator_profit_tuning | scripts\run_phase230_low_turnover_high_edge_strategy_search.py | outputs\phase230 |
| 231 | 1 | 1 | True | True | True | material_new_strategy_forms_positive_synthetic_candidates_found | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase232_validate_phase231_candidates_on_stricter_holdout_and_negative_controls_no_paper_live | scripts\run_phase231_material_new_strategy_forms.py | outputs\phase231 |
| 232 | 1 | 1 | True | True | True | phase231_candidate_validated_by_stricter_controls | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase233_fragility_and_realism_validation_for_phase232_candidates_no_paper_live | scripts\run_phase232_validate_phase231_candidates.py | outputs\phase232 |
| 233 | 1 | 1 | True | True | True | phase232_candidate_passed_fragility_realism_validation | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase234_prepare_real_anchor_or_sealed_generator_holdout_for_phase233_candidate_no_paper_live | scripts\run_phase233_fragility_realism_validation.py | outputs\phase233 |
| 234 | 1 | 1 | True | True | True | phase233_candidate_prepared_for_real_anchor_adapter | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase235_build_real_anchor_event_bar_microprice_reversal_adapter_no_paper_live | scripts\run_phase234_prepare_holdout.py | outputs\phase234 |
| 235 | 1 | 1 | True | True | True | phase233_candidate_failed_real_anchor_breadth_on_adapter | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase236_close_or_redesign_microprice_reversal_after_real_anchor_failure_no_paper_live | scripts\run_phase235_real_anchor_microprice_replay.py | outputs\phase235 |
| 236 | 1 | 1 | True | True | True | real_anchor_neighbor_positive_pockets_breadth_failed | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase237_redesign_threshold_transfer_or_expand_real_anchor_strategy_family_no_paper_live | scripts\run_phase236_real_anchor_neighbor_search.py | outputs\phase236 |
| 237 | 1 | 1 | True | True | True | real_anchor_threshold_transfer_candidate_opened_for_validation | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase238_precommit_unseen_real_anchor_or_walk_forward_validation_for_phase237_candidate_no_paper_live | scripts\run_phase237_threshold_transfer_search.py | outputs\phase237 |
| 238 | 1 | 1 | True | True | True | phase237_candidate_validation_precommitted_unseen_dates_needed | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase239_acquire_or_materialize_unseen_real_anchor_validation_dates_no_paper_live | scripts\run_phase238_validation_precommit.py | outputs\phase238 |
| 239 | 1 | 1 | True | True | True | unseen_real_l2_dates_available_for_download | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase240_execute_unseen_real_l2_download_and_materialization_no_paper_live | scripts\run_phase239_unseen_date_acquisition.py | outputs\phase239 |
| 240 | 1 | 1 | True | True | True | unseen_raw_l2_download_partial_or_in_progress | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | resume_phase240_unseen_raw_l2_download_no_paper_live | scripts\run_phase240_unseen_l2_downloader.py | outputs\phase240 |
| 241 | 1 | 1 | True | True | True | one_date_unseen_diagnostic_positive_but_fragile | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | close_or_redesign_phase237_candidate_after_one_date_unseen_real_l2_diagnostic_failure_no_paper_live | scripts\run_phase241_one_date_unseen_real_l2_diagnostic.py | outputs\phase241 |
| 242 | 1 | 1 | True | True | True | phase237_candidate_closed_redesign_queue_opened | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase243_cost_stress_first_redesign_search_without_2026_07_17_holdout_tuning_no_paper_live | scripts\run_phase242_close_or_redesign_after_one_date_diagnostic.py | outputs\phase242 |
| 243 | 1 | 1 | True | True | True | cost_stress_first_redesign_candidate_found_future_holdout_precommit_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | precommit_future_holdout_for_phase243_candidate_after_storage_decision_no_2026_07_17_tuning_no_paper_live | scripts\run_phase243_cost_stress_first_redesign_search.py | outputs\phase243 |
| 244 | 1 | 1 | True | True | True | future_holdout_precommitted_storage_decision_required | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | choose_storage_option_then_download_fresh_unseen_dates_for_phase244_frozen_candidate_no_tuning_no_paper_live | scripts\run_phase244_future_holdout_precommit.py | outputs\phase244 |
| 245 | 1 | 1 | True | True | True | storage_audit_local_space_feasible_policy_choice_required | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | choose_local_c_drive_download_or_cleanup_policy_then_run_phase246_fresh_holdout_download_no_tuning_no_paper_live | scripts\run_phase245_storage_decision_audit.py | outputs\phase245 |
| 246 | 1 | 1 | True | True | True | phase244_candidate_failed_one_fresh_date_diagnostic_redesign_required | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | close_or_redesign_phase244_candidate_after_phase246_one_date_failure_no_more_downloads_no_paper_live | scripts\run_phase246_fresh_one_date_holdout_diagnostic.py | outputs\phase246 |
| 247 | 1 | 1 | True | True | True | l2_imbalance_regime_filter_training_search_precommitted | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase248_training_only_l2_imbalance_regime_filtered_redesign_no_2026_07_17_or_2026_07_20_tuning_no_downloads_no_paper_live | scripts\run_phase247_l2_imbalance_regime_filter_redesign_precommit.py | outputs\phase247 |
| 248 | 1 | 1 | True | True | True | l2_imbalance_regime_filtered_search_no_survivor_broaden_or_close | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | close_or_broaden_phase248_l2_imbalance_regime_filtered_search_no_downloads_no_paper_live | scripts\run_phase248_l2_imbalance_regime_filtered_redesign_search.py | outputs\phase248 |
| 249 | 1 | 1 | True | True | True | single_name_reversal_closed_pair_basket_precommit_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase250_pair_basket_relative_value_precommit_no_downloads_no_2026_07_17_or_2026_07_20_tuning_no_paper_live | scripts\run_phase249_close_or_broaden_after_l2_filtered_no_survivor.py | outputs\phase249 |
| 250 | 1 | 1 | True | True | True | pair_basket_relative_value_training_search_precommitted | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase251_training_only_pair_basket_relative_value_search_no_downloads_no_2026_07_17_or_2026_07_20_tuning_no_paper_live | scripts\run_phase250_pair_basket_relative_value_precommit.py | outputs\phase250 |
| 251 | 1 | 1 | True | True | True | pair_basket_relative_value_no_survivor_broaden_or_close | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | close_or_broaden_phase251_pair_basket_relative_value_search_no_downloads_no_paper_live | scripts\run_phase251_pair_basket_relative_value_search.py | outputs\phase251 |
| 252 | 1 | 1 | True | True | True | aggregate_pair_basket_closed_richer_raw_depth_precommit_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase253_richer_raw_top5_depth_feature_materialization_precommit_no_new_downloads_no_paper_live | scripts\run_phase252_close_or_broaden_after_pair_basket_no_survivor.py | outputs\phase252 |
| 253 | 1 | 1 | True | True | True | richer_raw_top5_depth_materialization_precommitted | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase254_materialize_richer_raw_top5_depth_event_bars_existing_raw_only_no_paper_live | scripts\run_phase253_richer_raw_top5_depth_feature_materialization_precommit.py | outputs\phase253 |
| 254 | 1 | 1 | True | True | True | richer_raw_top5_depth_materialized_quality_interpretation_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase255_richer_raw_depth_feature_quality_interpretation_no_replay_no_paper_live | scripts\run_phase254_materialize_richer_raw_top5_depth_event_bars.py | outputs\phase254 |
| 255 | 1 | 1 | True | True | True | richer_raw_top5_depth_quality_passed_strategy_search_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase256_richer_raw_top5_depth_cost_aware_strategy_search_training_only_no_paper_live | scripts\run_phase255_richer_raw_depth_feature_quality_interpretation.py | outputs\phase255 |
| 256 | 1 | 1 | True | True | True | richer_raw_top5_depth_taker_search_no_survivor_interpretation_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase257_richer_raw_top5_depth_strategy_search_interpretation_no_paper_live | scripts\run_phase256_richer_raw_top5_depth_cost_aware_strategy_search.py | outputs\phase256 |
| 257 | 1 | 1 | True | True | True | passive_queue_aware_spread_capture_precommit_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase258_passive_queue_aware_spread_capture_precommit_full_top5_depth_no_paper_live | scripts\run_phase257_richer_raw_top5_depth_strategy_search_interpretation.py | outputs\phase257 |
| 258 | 1 | 1 | True | True | True | passive_queue_aware_spread_capture_training_search_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase259_passive_queue_aware_spread_capture_training_search_full_top5_depth_no_paper_live | scripts\run_phase258_passive_queue_aware_spread_capture_precommit.py | outputs\phase258 |
| 259 | 1 | 1 | True | True | True | passive_queue_aware_training_search_no_survivor_interpretation_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase260_passive_queue_aware_spread_capture_interpretation_no_paper_live | scripts\run_phase259_passive_queue_aware_spread_capture_training_search.py | outputs\phase259 |
| 260 | 1 | 1 | True | True | True | passive_opportunity_breadth_fill_model_repair_precommit_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase261_passive_opportunity_breadth_fill_model_repair_precommit_full_top5_depth_no_paper_live | scripts\run_phase260_passive_queue_aware_spread_capture_interpretation.py | outputs\phase260 |
| 261 | 1 | 1 | True | True | True | passive_opportunity_breadth_fill_model_training_search_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase262_passive_opportunity_breadth_fill_model_training_search_full_top5_depth_no_paper_live | scripts\run_phase261_passive_opportunity_breadth_fill_model_repair_precommit.py | outputs\phase261 |
| 262 | 1 | 1 | True | True | True | passive_opportunity_breadth_fill_model_training_no_survivor_interpretation_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase263_passive_opportunity_breadth_fill_model_interpretation_no_paper_live | scripts\run_phase262_passive_opportunity_breadth_fill_model_training_search.py | outputs\phase262 |
| 263 | 1 | 1 | True | True | True | full_depth_liquidity_shock_absorption_event_precommit_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase264_full_depth_liquidity_shock_absorption_event_precommit_no_paper_live | scripts\run_phase263_passive_opportunity_breadth_fill_model_interpretation.py | outputs\phase263 |
| 264 | 1 | 1 | True | True | True | full_depth_liquidity_shock_absorption_event_training_search_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase265_full_depth_liquidity_shock_absorption_event_training_search_no_paper_live | scripts\run_phase264_full_depth_liquidity_shock_absorption_event_precommit.py | outputs\phase264 |
| 265 | 1 | 1 | True | True | True | full_depth_liquidity_shock_training_no_survivor_interpretation_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase266_full_depth_liquidity_shock_absorption_event_interpretation_no_paper_live | scripts\run_phase265_full_depth_liquidity_shock_absorption_event_training_search.py | outputs\phase265 |
| 266 | 1 | 1 | True | True | True | full_depth_liquidity_shock_breadth_shuffle_repair_precommit_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase267_full_depth_liquidity_shock_breadth_shuffle_robustness_repair_precommit_no_paper_live | scripts\run_phase266_full_depth_liquidity_shock_absorption_event_interpretation.py | outputs\phase266 |
| 267 | 1 | 1 | True | True | True | full_depth_liquidity_shock_two_lane_training_search_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase268_full_depth_liquidity_shock_breadth_shuffle_robustness_repair_training_search_no_paper_live | scripts\run_phase267_full_depth_liquidity_shock_breadth_shuffle_robustness_repair_precommit.py | outputs\phase267 |
| 268 | 1 | 1 | True | True | True | full_depth_liquidity_shock_two_lane_training_no_acceptance_interpretation_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase269_full_depth_liquidity_shock_two_lane_training_interpretation_no_paper_live | scripts\run_phase268_full_depth_liquidity_shock_breadth_shuffle_robustness_repair_training_search.py | outputs\phase268 |
| 269 | 1 | 1 | True | True | True | fixed_capital_concurrency_capacity_return_precommit_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase270_fixed_capital_concurrency_and_capacity_return_precommit_no_paper_live | scripts\run_phase269_full_depth_liquidity_shock_two_lane_training_interpretation.py | outputs\phase269 |
| 270 | 1 | 1 | True | True | True | fixed_capital_concurrency_capacity_return_analysis_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase271_fixed_capital_concurrency_and_capacity_return_analysis_no_paper_live | scripts\run_phase270_fixed_capital_concurrency_and_capacity_return_precommit.py | outputs\phase270 |
| 271 | 1 | 1 | True | True | True | fixed_capital_capacity_return_interpretation_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase272_fixed_capital_capacity_return_interpretation_no_paper_live | scripts\run_phase271_fixed_capital_concurrency_and_capacity_return_analysis.py | outputs\phase271 |
| 272 | 1 | 1 | True | True | True | focused_capital_aware_candidate_followthrough_search_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase273_focused_capital_aware_candidate_followthrough_search_no_paper_live | scripts\run_phase272_fixed_capital_capacity_return_interpretation.py | outputs\phase272 |
| 273 | 1 | 1 | True | True | True | focused_capital_followthrough_interpretation_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase274_focused_capital_followthrough_interpretation_no_paper_live | scripts\run_phase273_focused_capital_aware_candidate_followthrough_search.py | outputs\phase273 |
| 274 | 1 | 1 | True | True | True | focused_capital_multiday_synthetic_followthrough_search_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase275_focused_capital_multiday_synthetic_followthrough_search_no_paper_live | scripts\run_phase274_focused_capital_followthrough_interpretation.py | outputs\phase274 |
| 275 | 1 | 1 | True | True | True | multiday_synthetic_followthrough_interpretation_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase276_multiday_synthetic_followthrough_interpretation_no_paper_live | scripts\run_phase275_focused_capital_multiday_synthetic_followthrough_search.py | outputs\phase275 |
| 276 | 1 | 1 | True | True | True | cost_robust_full_depth_redesign_search_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase277_cost_robust_full_depth_redesign_search_no_paper_live | scripts\run_phase276_multiday_synthetic_followthrough_interpretation.py | outputs\phase276 |
| 277 | 1 | 1 | True | True | True | cost_robust_redesign_interpretation_open | synthetic_strategy_discovery | 0 |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | run_phase278_cost_robust_redesign_interpretation_no_paper_live | scripts\run_phase277_cost_robust_full_depth_redesign_search.py | outputs\phase277 |
