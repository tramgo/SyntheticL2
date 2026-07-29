# Phase149 Research State Auditor

Generated UTC: 2026-07-29T07:03:21.470601+00:00

Phase149 reconciles current phase scripts, output evidence, branch states, and replay gates.
It does not run strategies, contact Azure, import data, or unlock replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase149_phase_rows | 230 | Phase rows discovered from scripts and outputs |
| phase149_runner_phase_rows | 228 | Phase rows with at least one runner |
| phase149_acceptance_phase_rows | 180 | Phase rows with acceptance summaries |
| phase149_branch_rows | 5 | Current research branches summarized |
| phase149_hard_gate_rows | 322 | Hard global-state gates evaluated |
| phase149_hard_gate_pass_rows | 322 | Hard global-state gates passed |
| phase149_strategy_replay_allowed | 0 | Phase149 never unlocks strategy replay |
| phase149_next_best_action | run_phase238_precommit_unseen_real_anchor_or_walk_forward_validation_for_phase237_candidate_no_paper_live | Recommended next milestone |

## Branch Status Summary

| branch | status | evidence | current_next_action |
| --- | --- | --- | --- |
| real_l2_anchor_gate | gated | Phase146/148 keep strategy replay closed until at least five ready real-anchor days are proven. | use_phase174_secure_download_orchestrator_for_required_real_l2_dates |
| real_receive_flow_source | cost_aware_label_set_closed_phase229_source_expansion_precommit_pending_no_materialization_no_fit_no_replay_no_test | Phase172 ready_dates=7, additional_dates_needed=0; Phase174 download_ran=1; Phase175 activation_ready=1; Phase176 features_materialized=1; Phase177 quality_audit_ran=1; Phase178 handoff_ready=1; Phase179 precommit_ready=1; Phase180 precommit_ready=1; Phase181 labels_materialized=1; Phase182 label_audit_pass=1; Phase183 replay_readiness=1; Phase184 dry_run_complete=1, test_rows_used=0, promotion_allowed=0; Phase185 interpretation_complete=1, cost_dominates=1, test_replay_allowed_next=0; Phase186 family_set_closed=1, reuse_without_redesign_allowed=0, test_replay_allowed_next=0; Phase187 candidate_complete=1, validation_positive_all_profiles=1, test_replay_allowed_next=0; Phase188 interpretation_complete=1, breadth_warning=1, date_count_warning=1, test_replay_allowed_next=0; Phase189 decision_complete=1, test_precommit_allowed=0, test_replay_allowed_next=0; Phase190 decision_complete=1, additional_validation_breadth_available_now=0, test_replay_execution=0; Phase191 precommit_complete=1, test_replay_execution=0, test_result_allowed=0; Phase192 download_complete=1, test_replay_execution=0; Phase193 extension_complete=1, extension_dates=2026-07-15;2026-07-16, min_profile_net=9.085299933825853, breadth_warning=1, test_replay_execution=0; Phase194 fragility_decision_complete=1, all_extension_profile_dates_negative=1, test_replay_allowed_next=0; Phase195 redesign_search_complete=1, passing_extension_gate_candidates=0, best_candidate=P195_TOP5_FOLLOW_I80_S1p5_Z1_Q1_R50, best_min_extension_net=-12.410960684628158, test_replay_allowed_next=0; Phase196 expanded_model_search_complete=1, train_selected_model_rows=0, passing_extension_gate_models=0, best_model=nan, test_replay_allowed_next=0; Phase197 feature_precommit_complete=1, ready_feature_families=5, strategy_replay_allowed=0, test_replay_allowed_next=0; Phase198 context_model_search_complete=1, train_selected_model_rows=0, passing_extension_gate_models=0, best_model=nan, best_family=nan, test_replay_allowed_next=0; Phase199 branch_decision_complete=1, current_branch_paused=1, material_redesign_required=1, test_replay_allowed_next=0; Phase200 precommit_complete=1, selected_hypothesis=P200_QUEUE_PASSIVE_QUEUE_POSITION_PROXY, label_contract_rows=6, stage_action_rows=4, test_replay_allowed_next=0; Phase201 stage01_complete=1, joined_rows=696, pre_replay_candidates=0, max_symbols=4, max_dates=4, test_replay_allowed_next=0; Phase202 redesign_precommit_complete=1, redesigned_feature_rows=4, acceptance_contract_rows=4, phase203_action_rows=3, test_replay_allowed_next=0; Phase203 label_materialization_complete=1, materialized_label_rows=696, redesigned_candidate_pass_rows=0, max_symbols=4, max_dates=4, adverse_selection_ceiling_met=0, candidate_gate_open=0, test_replay_allowed_next=0; Phase204 closure_decision_complete=1, passive_redesign_closed_for_replay=1, material_new_source_required=1, threshold_widening_allowed=0, test_replay_allowed_next=0; Phase205 material_new_source_precommit_complete=1, selected_route=P205_REAL_RECEIVE_FLOW_CONTEXT_SOURCE_REFRESH, phase206_work_order_rows=3, test_replay_allowed_next=0; Phase206 nonoverlap_feature_contract_complete=1, feature_catalog_rows=6, blocked_reference_rows=14, nonoverlap_pass_rows=6, model_fit_allowed=0, test_replay_allowed_next=0; Phase207 feature_matrix_precommit_complete=1, matrix_rows=24, available_rows=24, trade_dates=7, symbols=32, model_fit_allowed=0, test_replay_allowed_next=0; Phase208 quality_gate_complete=1, quality_rows=24, quality_pass_rows=24, blocking_gaps=0, model_fit_allowed=0, test_replay_allowed_next=0; Phase209 model_fit_precommit_spec_complete=1, model_spec_rows=3, feature_set_rows=24, label_target_rows=3, split_control_rows=4, model_fit_execution_allowed=0, test_replay_allowed_next=0; Phase210 train_validation_model_fit_dry_run_complete=1, joined_rows=1641001, model_fit_rows=12, validation_metric_rows=12, negative_control_rows=12, test_rows_used=0, strategy_replay_allowed=0, profitability_claim_allowed=0; Phase211 interpretation_complete=1, interpretation_rows=12, passing_rows=0, candidate_opened_for_replay=0, strategy_replay_allowed=0, profitability_claim_allowed=0; Phase212 closure_complete=1, families_closed=3, redesign_rows=3, model_fit_allowed_next=0, strategy_replay_allowed=0, profitability_claim_allowed=0; Phase213 source_precommit_complete=1, selected_source=P213_EVENT_SURPRISE_CONDITIONAL_LABEL_SOURCE, label_contract_rows=3, phase214_work_order_rows=1, model_fit_allowed_next=0, strategy_replay_allowed=0; Phase214 label_materialization_complete=1, label_rows=1641001, event_surprise_rows=130231, quality_pass_rows=512, sealed_test_rows_used=0, strategy_replay_allowed=0; Phase215 quality_interpretation_complete=1, passing_rows=14, families_with_interpretable_rows=3, phase216_work_order_rows=1, model_fit_allowed_next=0, strategy_replay_allowed=0; Phase216 event_only_precommit_complete=1, target_rows=7, full_train_validation_targets=7, excluded_targets=10, model_fit_allowed_next=0, strategy_replay_allowed=0; Phase217 design_matrix_precommit_complete=1, target_scope_rows=7, feature_binding_rows=42, target_row_observation_scope=384282, row_level_export_allowed=0, model_fit_allowed_next=0, strategy_replay_allowed=0; Phase218 model_fit_precommit_complete=1, dry_run_precommitted_for_phase219=1, model_specs=3, target_contracts=7, feature_contracts=18, phase218_model_fit_execution_allowed=0, strategy_replay_allowed=0; Phase219 model_fit_dry_run_complete=1, event_only_joined_rows=129852, model_fit_rows=21, validation_metric_rows=21, control_rows=42, model_fit_execution=1, strategy_replay_allowed=0, test_rows_used=0; Phase220 validation_interpretation_complete=1, passing_candidates=5, candidate_families=1, best_mse_improvement_vs_base=0.0100934445514009, best_correlation=0.2205753672014153, candidate_opened_for_phase221=1, strategy_replay_allowed=0; Phase221 signal_replay_precommit_complete=1, frozen_candidates=5, signal_rules=5, phase222_replay_precommitted=1, phase221_replay_execution_allowed=0, test_replay_allowed_next=0, profitability_claim_allowed=0; Phase222 signal_replay_dry_run_complete=1, event_only_joined_rows=127215, replay_summary_rows=240, validation_decision_events=89481, best_validation_net_after_cost_bps_proxy=-11.998805192630435, strategy_replay_execution=1, test_rows_used=0, profitability_claim_allowed=0; Phase223 validation_interpretation_complete=1, interpretation_rows=40, positive_net_validation_rows=0, passing_interpretation_rows=0, best_validation_net_after_cost_bps_proxy=-13.420731450576811, best_actual_vs_shuffle_net_edge_bps=1.0000000000000053, phase224_work_order_rows=1, broader_replay_allowed_next=0, test_rows_used=0, profitability_claim_allowed=0; Phase224 closure_or_redesign_complete=1, candidate_set_closed_for_broader=1, candidate_set_closed_for_test=1, failure_modes=4, redesign_routes=3, selected_redesign_route=P224_COST_AWARE_ACTIONABLE_EVENT_LABELS, phase225_work_order_rows=1, model_fit_allowed_next=0, broader_replay_allowed_next=0, profitability_claim_allowed=0; Phase225 cost_aware_redesign_precommit_complete=1, cost_hurdles=2, label_contracts=3, negative_controls=3, selected_route=P224_COST_AWARE_ACTIONABLE_EVENT_LABELS, label_materialization_allowed_next=1, model_fit_allowed_next=0, strategy_replay_allowed=0, test_rows_used=0, profitability_claim_allowed=0; Phase226 cost_aware_label_materialization_complete=1, availability_rows=3, available_horizons=2, blocked_horizons=1, label_partitions=256, total_label_rows=45631, actionable_rows=136, quality_pass_rows=0, sealed_test_rows_available=184909, test_rows_used=0, model_fit_allowed_next=0, profitability_claim_allowed=0; Phase227 quality_interpretation_complete=1, quality_rows=4, horizon_rows=3, failure_modes=4, actionable_rows=136, quality_pass_rows=0, fit_precommit_candidates=0, phase228_work_order_rows=1, model_fit_allowed_next=0, test_rows_used=0, profitability_claim_allowed=0; Phase228 closure_or_relaxation_complete=1, closed_for_fit=1, closed_for_replay=1, redesign_routes=3, guardrails=3, selected_route=P228_SOURCE_EXPANSION_AND_AVAILABLE_HORIZON_REPAIR, phase229_work_order_rows=1, label_materialization_allowed_next=0, threshold_widening_allowed=0, model_fit_allowed_next=0, profitability_claim_allowed=0; Phase229 multi_strategy_search_complete=1, distinct_strategy_ids=12, realistic_profile_rows=24, positive_realistic_candidates=0, positive_any_profile_rows=0, best_strategy=P164_S06_ABSORPTION_REVERSAL, best_annual_net_pnl=-189512.60575493483; Phase230 low_turnover_high_edge_complete=1, variant_group_rows=28162, positive_expanded_groups=0, positive_oracle_signed_groups=0, best_scope=strategy_symbol_date_profile, best_variant=original, best_net_pnl=-100.5200932874, profitability_claim_allowed=0; Phase231 material_new_forms_complete=1, candidate_rows=72, train_pass=7, test_pass=8, synthetic_candidates=3, best_candidate=P231_MICROPRICE_REVERSAL_H3_Q0_9, best_test_net_pnl=229962.8071718807, profitability_claim_allowed=0; Phase232 validation_complete=1, validated_candidates=1, negative_control_pass=3, cost_stress_pass=3, holdout_stability_pass=1, best_candidate=P231_MICROPRICE_REVERSAL_H3_Q0_9, best_test_net_pnl=229962.80717188073, profitability_claim_allowed=0; Phase233 fragility_realism_complete=1, pass=1, neighbor_pass=7, parent_test_2x_cost_net=179609.71039338846, profitability_claim_allowed=0; Phase234 holdout_preparation_complete=1, selected_route=P234_REAL_ANCHOR_EVENT_BAR_ADAPTER_PREP, real_anchor_route_ready=1, required_schema_present=11/11, phase235_work_order_rows=4, profitability_claim_allowed=0; Phase235 real_anchor_replay_complete=1, pass=0, trades=1, net_pnl=637.4164403580107, dates=1, symbols=1, profitability_claim_allowed=0; Phase236 neighbor_search_complete=1, positive_variants=7, breadth_passing_variants=0, best_candidate=P233_MICROPRICE_REVERSAL_H5_Q0_9, best_net_pnl=1447.6958002712238, best_trades=1, profitability_claim_allowed=0; Phase237 threshold_transfer_complete=1, breadth_positive_candidates=3, best_candidate=P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95, best_family=bar_return_reversal, best_net_pnl=7041.523067663933, best_trades=71, phase238_opened=1, profitability_claim_allowed=0. | run_phase238_precommit_unseen_real_anchor_or_walk_forward_validation_for_phase237_candidate_no_paper_live |
| top_five_depth_passive | closed_clean_falsification | Phase136 Outcome A closes the branch after Phase132 kill-switch and Phase116 blocklist verification. | do_not_open_phase134_or_phase135_for_this_branch |
| synthetic_strategy_discovery | real_anchor_threshold_transfer_candidate_opened_for_validation | Phase229 ranked 12 strategy ids and found 0 positive realistic candidates; Phase230 tested 28162 original/inverse/oracle variant groups and found 0 positive expanded groups and 0 positive oracle-signed upper-bound groups; Phase231 replayed 72 material-new candidates and found 3 train+test synthetic candidates, led by P231_MICROPRICE_REVERSAL_H3_Q0_9 with test net P&L 229962.8071718807; Phase232 validated 1 candidate after cost stress, side-flip, random-side and holdout stability checks; Phase233 passed fragility/realism with 7 passing neighbors and parent test 2x cost net P&L 179609.71039338846; Phase234 selected P234_REAL_ANCHOR_EVENT_BAR_ADAPTER_PREP with real_anchor_route_ready=1 and 11/11 required real L2 schema rows present; Phase235 real-anchor replay selected 1 trades with net P&L 637.4164403580107, but breadth was 1 dates and 1 symbols; Phase236 replayed 12 neighbors and found 7 positive real-anchor variants, but 0 breadth-passing variants; Phase237 evaluated 3584 threshold-transfer variants and opened P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 for Phase238 with net P&L 7041.523067663933, 71 trades, 6 dates and 21 symbols. | run_phase238_precommit_unseen_real_anchor_or_walk_forward_validation_for_phase237_candidate_no_paper_live |
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
| 158 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase158_phase106_style_full_realism_audit.py | outputs\phase158 |
| 159 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase159_distributional_cadence_smoke.py | outputs\phase159 |
| 160 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase160_phase159_noncadence_realism_audit.py | outputs\phase160 |
| 161 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase161_combined_realism_handoff_gate.py | outputs\phase161 |
| 162 | 1 | 2 | True | True | True | smoke_or_partial |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase162_phase159_full_year_materialization_audit.py | outputs\phase162\|outputs\phase162_smoke |
| 163 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase163_synthetic_only_replay_preflight.py | outputs\phase163 |
| 164 | 1 | 2 | True | True | True | smoke_or_partial |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase164_synthetic_only_full_year_replay.py | outputs\phase164\|outputs\phase164_smoke |
| 165 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase165_phase164_full_year_replay_verdict.py | outputs\phase165 |
| 166 | 1 | 2 | True | True | True | smoke_or_partial |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase166_cross_symbol_lead_lag_cache.py | outputs\phase166\|outputs\phase166_smoke |
| 167 | 1 | 2 | True | True | True | smoke_or_partial |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase167_s08_cross_symbol_lead_lag_replay.py | outputs\phase167\|outputs\phase167_smoke |
| 168 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase168_s08_closure_verdict.py | outputs\phase168 |
| 169 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase169_post_s08_research_queue.py | outputs\phase169 |
| 170 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase170_filter_conditioned_feasibility_matrix.py | outputs\phase170 |
| 171 | 1 | 1 | True | True | True | source_contract_declared_no_replay | real_receive_flow_source | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | run_download_first_real_l2_receive_flow_availability_audit_or_collect_broker_order_telemetry | scripts\run_phase171_external_orderflow_source_contract.py | outputs\phase171 |
| 172 | 1 | 1 | True | True | True | local_receive_flow_structural_ready_but_day_count_gated | real_receive_flow_source | 1 |  |  |  |  |  |  |  |  |  |  |  |  |  | build_phase173_receive_flow_feature_schema_no_replay | scripts\run_phase172_real_l2_receive_flow_availability_audit.py | outputs\phase172 |
| 173 | 1 | 1 | True | True | True | download_preflight_ready | real_receive_flow_download_gate | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | run_phase148_with_download_for_required_dates_then_rerun_phase172 | scripts\run_phase173_real_l2_download_credential_preflight.py | outputs\phase173 |
| 174 | 1 | 1 | True | True | True | secure_download_executed | real_receive_flow_download_gate | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | inspect_phase148_phase172_outputs_then_download_remaining_dates_if_needed | scripts\run_phase174_secure_real_l2_download_orchestrator.ps1 | outputs\phase174 |
| 175 | 1 | 1 | True | True | True | receive_flow_feature_schema_activation_ready | real_receive_flow_source | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | run_phase176_receive_flow_feature_materialization_no_strategy | scripts\run_phase175_receive_flow_feature_schema_precommit.py | outputs\phase175 |
| 176 | 1 | 1 | True | True | True | receive_flow_features_materialized_no_replay | real_receive_flow_source | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | run_phase177_feature_quality_audit | scripts\run_phase176_receive_flow_feature_materializer.py | outputs\phase176 |
| 177 | 1 | 1 | True | True | True | receive_flow_feature_quality_audited_no_replay | real_receive_flow_source | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | run_phase178_receive_flow_feature_handoff_precommit_no_strategy | scripts\run_phase177_receive_flow_feature_quality_audit.py | outputs\phase177 |
| 178 | 1 | 1 | True | True | True | receive_flow_feature_handoff_precommitted_no_replay | real_receive_flow_source | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | build_phase179_strategy_family_precommit_no_replay | scripts\run_phase178_receive_flow_feature_handoff_precommit.py | outputs\phase178 |
| 179 | 1 | 1 | True | True | True | strategy_family_precommitted_no_replay | real_receive_flow_source | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | build_phase180_cost_latency_bound_label_precommit_no_replay | scripts\run_phase179_strategy_family_precommit.py | outputs\phase179 |
| 180 | 1 | 1 | True | True | True | cost_latency_label_precommitted_no_replay | real_receive_flow_source | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | build_phase181_label_materialization_no_replay | scripts\run_phase180_cost_latency_label_precommit.py | outputs\phase180 |
| 181 | 1 | 1 | True | True | True | labels_materialized_no_replay | real_receive_flow_source | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | build_phase182_label_quality_leakage_audit_no_replay | scripts\run_phase181_label_materialization.py | outputs\phase181 |
| 182 | 1 | 1 | True | True | True | label_quality_leakage_audited_no_replay | real_receive_flow_source | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | build_phase183_replay_readiness_precommit_no_pnl | scripts\run_phase182_label_quality_leakage_audit.py | outputs\phase182 |
| 183 | 1 | 1 | True | True | True | replay_readiness_precommitted_no_pnl | real_receive_flow_source | 0 | 0 |  |  |  |  |  |  |  |  |  |  |  |  | build_phase184_train_validation_replay_dry_run_no_test_no_promotion | scripts\run_phase183_replay_readiness_precommit.py | outputs\phase183 |
| 184 | 1 | 1 | True | True | True | train_validation_replay_dry_run_complete_no_test_no_promotion | real_receive_flow_source |  |  | 0 |  |  |  |  |  |  |  |  |  | 0 | 0 | build_phase185_validation_replay_interpretation_and_kill_switch_audit_no_test | scripts\run_phase184_train_validation_replay_dry_run.py | outputs\phase184 |
| 185 | 1 | 1 | True | True | True | validation_interpretation_cost_dominated_no_test_no_promotion | real_receive_flow_source |  |  | 0 |  |  | 0 |  |  |  |  |  |  | 0 | 0 | redesign_cost_aware_receive_flow_family_or_close_current_family_set_before_test_replay | scripts\run_phase185_validation_replay_interpretation.py | outputs\phase185 |
| 186 | 1 | 1 | True | True | True | current_family_set_closed_cost_aware_redesign_pending | real_receive_flow_source |  |  |  |  |  | 0 |  | 0 |  |  |  |  | 0 | 0 | build_phase187_cost_aware_sparse_receive_flow_candidate_no_test | scripts\run_phase186_cost_aware_family_closure_precommit.py | outputs\phase186 |
| 187 | 1 | 1 | True | True | True | cost_aware_sparse_candidate_validation_interpretation_pending | real_receive_flow_source |  |  | 0 |  |  | 0 |  |  |  |  |  |  | 0 | 0 | build_phase188_cost_aware_sparse_candidate_interpretation_no_test | scripts\run_phase187_cost_aware_sparse_candidate.py | outputs\phase187 |
| 188 | 1 | 1 | True | True | True | sparse_candidate_interpreted_phase189_decision_pending | real_receive_flow_source |  |  |  |  |  | 0 |  |  |  |  | 1 | 1 | 0 | 0 | build_phase189_untouched_test_replay_precommit_or_redesign_decision | scripts\run_phase188_sparse_candidate_interpretation.py | outputs\phase188 |
| 189 | 1 | 1 | True | True | True | test_replay_deferred_validation_breadth_pending | real_receive_flow_source |  |  |  |  |  | 0 | 0 |  |  |  |  |  | 0 | 0 | build_phase190_additional_validation_breadth_or_diagnostic_test_spec_no_execution | scripts\run_phase189_test_replay_precommit_decision.py | outputs\phase189 |
| 190 | 1 | 1 | True | True | True | diagnostic_test_spec_written_validation_breadth_pending | real_receive_flow_source |  |  |  | 0 |  | 0 |  |  | 0 | 0 |  |  | 0 | 0 | add_real_validation_date_or_build_phase191_diagnostic_test_replay_precommit_no_execution | scripts\run_phase190_validation_breadth_or_diagnostic_test_spec.py | outputs\phase190 |
| 191 | 1 | 1 | True | True | True | diagnostic_test_replay_precommitted_no_execution | real_receive_flow_source |  |  |  | 0 | 0 | 0 |  |  |  |  |  |  | 0 | 0 | either_add_real_validation_date_or_explicitly_authorize_phase192_diagnostic_test_replay | scripts\run_phase191_diagnostic_test_replay_precommit.py | outputs\phase191 |
| 192 | 1 | 1 | True | True | True | real_validation_date_downloaded_no_test | real_receive_flow_source |  |  |  | 0 | 0 |  |  |  |  |  |  |  | 0 | 0 | run_phase172_phase176_phase181_then_validation_breadth_replay | scripts\run_phase192_azure_real_validation_date_download.py | outputs\phase192 |
| 193 | 1 | 1 | True | True | True | validation_breadth_extended_mixed_negative_by_date_no_test | real_receive_flow_source |  |  |  | 0 | 0 |  |  |  |  |  | 1 | 0 | 0 | 0 | add_more_validation_dates_or_redesign_before_any_test_replay | scripts\run_phase193_validation_breadth_extension_replay.py | outputs\phase193 |
| 194 | 1 | 1 | True | True | True | frozen_sparse_candidate_closed_for_test_replay_redesign_required | real_receive_flow_source |  |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | redesign_receive_flow_candidate_with_date_and_symbol_breadth_gates_before_test | scripts\run_phase194_sparse_candidate_fragility_decision.py | outputs\phase194 |
| 195 | 1 | 1 | True | True | True | redesign_search_no_extension_gate_survivor_no_test | real_receive_flow_source |  |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | redesign_or_expand_feature_family_no_test | scripts\run_phase195_receive_flow_redesign_candidate_search.py | outputs\phase195 |
| 196 | 1 | 1 | True | True | True | expanded_feature_model_search_no_train_survivor_no_test | real_receive_flow_source |  |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | expand_non_receive_flow_features_or_pause_this_branch_no_test | scripts\run_phase196_expanded_feature_model_search.py | outputs\phase196 |
| 197 | 1 | 1 | True | True | True | non_receive_flow_feature_expansion_precommitted_phase198_ready_no_test | real_receive_flow_source | 0 |  |  |  |  | 0 |  |  |  |  |  |  | 0 | 0 | run_phase198_non_receive_flow_context_model_search_no_test | scripts\run_phase197_non_receive_flow_feature_expansion_precommit.py | outputs\phase197 |
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
