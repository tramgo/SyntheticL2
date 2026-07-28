# Phase149 Research State Auditor

Generated UTC: 2026-07-28T20:53:24.407085+00:00

Phase149 reconciles current phase scripts, output evidence, branch states, and replay gates.
It does not run strategies, contact Azure, import data, or unlock replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase149_phase_rows | 200 | Phase rows discovered from scripts and outputs |
| phase149_runner_phase_rows | 198 | Phase rows with at least one runner |
| phase149_acceptance_phase_rows | 150 | Phase rows with acceptance summaries |
| phase149_branch_rows | 4 | Current research branches summarized |
| phase149_hard_gate_rows | 143 | Hard global-state gates evaluated |
| phase149_hard_gate_pass_rows | 143 | Hard global-state gates passed |
| phase149_strategy_replay_allowed | 0 | Phase149 never unlocks strategy replay |
| phase149_next_best_action | run_phase208_feature_matrix_quality_gate_no_model_no_replay | Recommended next milestone |

## Branch Status Summary

| branch | status | evidence | current_next_action |
| --- | --- | --- | --- |
| real_l2_anchor_gate | gated | Phase146/148 keep strategy replay closed until at least five ready real-anchor days are proven. | use_phase174_secure_download_orchestrator_for_required_real_l2_dates |
| real_receive_flow_source | allowed_feature_matrix_precommitted_phase208_quality_gate_pending_no_model_no_replay | Phase172 ready_dates=7, additional_dates_needed=0; Phase174 download_ran=1; Phase175 activation_ready=1; Phase176 features_materialized=1; Phase177 quality_audit_ran=1; Phase178 handoff_ready=1; Phase179 precommit_ready=1; Phase180 precommit_ready=1; Phase181 labels_materialized=1; Phase182 label_audit_pass=1; Phase183 replay_readiness=1; Phase184 dry_run_complete=1, test_rows_used=0, promotion_allowed=0; Phase185 interpretation_complete=1, cost_dominates=1, test_replay_allowed_next=0; Phase186 family_set_closed=1, reuse_without_redesign_allowed=0, test_replay_allowed_next=0; Phase187 candidate_complete=1, validation_positive_all_profiles=1, test_replay_allowed_next=0; Phase188 interpretation_complete=1, breadth_warning=1, date_count_warning=1, test_replay_allowed_next=0; Phase189 decision_complete=1, test_precommit_allowed=0, test_replay_allowed_next=0; Phase190 decision_complete=1, additional_validation_breadth_available_now=0, test_replay_execution=0; Phase191 precommit_complete=1, test_replay_execution=0, test_result_allowed=0; Phase192 download_complete=1, test_replay_execution=0; Phase193 extension_complete=1, extension_dates=2026-07-15;2026-07-16, min_profile_net=9.085299933825853, breadth_warning=1, test_replay_execution=0; Phase194 fragility_decision_complete=1, all_extension_profile_dates_negative=1, test_replay_allowed_next=0; Phase195 redesign_search_complete=1, passing_extension_gate_candidates=0, best_candidate=P195_TOP5_FOLLOW_I80_S1p5_Z1_Q1_R50, best_min_extension_net=-12.410960684628158, test_replay_allowed_next=0; Phase196 expanded_model_search_complete=1, train_selected_model_rows=0, passing_extension_gate_models=0, best_model=nan, test_replay_allowed_next=0; Phase197 feature_precommit_complete=1, ready_feature_families=5, strategy_replay_allowed=0, test_replay_allowed_next=0; Phase198 context_model_search_complete=1, train_selected_model_rows=0, passing_extension_gate_models=0, best_model=nan, best_family=nan, test_replay_allowed_next=0; Phase199 branch_decision_complete=1, current_branch_paused=1, material_redesign_required=1, test_replay_allowed_next=0; Phase200 precommit_complete=1, selected_hypothesis=P200_QUEUE_PASSIVE_QUEUE_POSITION_PROXY, label_contract_rows=6, stage_action_rows=4, test_replay_allowed_next=0; Phase201 stage01_complete=1, joined_rows=696, pre_replay_candidates=0, max_symbols=4, max_dates=4, test_replay_allowed_next=0; Phase202 redesign_precommit_complete=1, redesigned_feature_rows=4, acceptance_contract_rows=4, phase203_action_rows=3, test_replay_allowed_next=0; Phase203 label_materialization_complete=1, materialized_label_rows=696, redesigned_candidate_pass_rows=0, max_symbols=4, max_dates=4, adverse_selection_ceiling_met=0, candidate_gate_open=0, test_replay_allowed_next=0; Phase204 closure_decision_complete=1, passive_redesign_closed_for_replay=1, material_new_source_required=1, threshold_widening_allowed=0, test_replay_allowed_next=0; Phase205 material_new_source_precommit_complete=1, selected_route=P205_REAL_RECEIVE_FLOW_CONTEXT_SOURCE_REFRESH, phase206_work_order_rows=3, test_replay_allowed_next=0; Phase206 nonoverlap_feature_contract_complete=1, feature_catalog_rows=6, blocked_reference_rows=14, nonoverlap_pass_rows=6, model_fit_allowed=0, test_replay_allowed_next=0; Phase207 feature_matrix_precommit_complete=1, matrix_rows=24, available_rows=24, trade_dates=7, symbols=32, model_fit_allowed=0, test_replay_allowed_next=0. | run_phase208_feature_matrix_quality_gate_no_model_no_replay |
| top_five_depth_passive | closed_clean_falsification | Phase136 Outcome A closes the branch after Phase132 kill-switch and Phase116 blocklist verification. | do_not_open_phase134_or_phase135_for_this_branch |
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
| phase149_deep_book_branch_closed | True | 1 | 1 | hard |
| phase149_no_promoted_strategy_replay | True | 0 | 0 | hard |

## Phase Status Ledger

| phase | runner_count | output_rows | has_runner | has_outputs | has_acceptance_summary | status | branch | strategy_replay_allowed | pnl_allowed | test_rows_used | test_replay_execution | test_result_allowed | test_replay_allowed_next | untouched_test_replay_precommit_allowed | reuse_without_redesign_allowed | additional_validation_breadth_available_now | may_relabel_test_as_validation | breadth_warning | date_count_warning | promotion_allowed | paper_or_live_acceptance_allowed | next_action | runner | output_dir |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 123 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase123_filter_label_matrix_builder.py | outputs\phase123 |
| 124 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase124_non_trading_filter_baselines.py | outputs\phase124 |
| 125 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase125_filter_integration_contract.py | outputs\phase125 |
| 126 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase126_candidate_generation_permission_ledger.py | outputs\phase126 |
| 127 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase127_allowed_universe_precommit_queue.py | outputs\phase127 |
| 128 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase128_next_label_design_spec.py | outputs\phase128 |
| 129 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase129_allowed_context_label_matrix.py | outputs\phase129 |
| 130 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase130_no_replay_diagnostic_baselines.py | outputs\phase130 |
| 131 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase131_deep_book_feature_precommit.py | outputs\phase131 |
| 132 | 1 | 1 | True | True | True | closed_kill_switch | top_five_depth_passive | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | stop_update_phase116_blocklist | scripts\run_phase132_deep_book_feature_diagnostics.py | outputs\phase132 |
| 133 | 1 | 1 | True | True | True | execution_contract_pinned_phase134_closed | top_five_depth_passive | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | stop_update_phase116_blocklist_do_not_open_phase134 | scripts\run_phase133_passive_execution_model_upgrade.py | outputs\phase133 |
| 136 | 1 | 1 | True | True | True | closed_clean_falsification | top_five_depth_passive | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | wait_for_real_l2_anchor_unlock_or_start_new_precommitted_non_blocklisted_research_branch | scripts\run_phase136_deep_book_verdict_and_handoff.py | outputs\phase136 |
| 137 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase137_post_phase132_real_anchor_restart.py | outputs\phase137 |
| 138 | 0 | 1 | False | True | False | script_only |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | outputs\phase138 |
| 139 | 0 | 1 | False | True | False | smoke_or_partial |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | outputs\phase139_smoke |
| 142 | 1 | 1 | True | True | True | gated_waiting_for_more_real_anchor_days | real_l2_anchor_gate | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase142_local_real_l2_download_verifier.py | outputs\phase142 |
| 143 | 1 | 1 | True | True | True | gated_waiting_for_more_real_anchor_days | real_l2_anchor_gate | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase142_phase143 | scripts\run_phase143_real_l2_two_date_preflight.py | outputs\phase143 |
| 145 | 1 | 1 | True | True | True | gated_waiting_for_more_real_anchor_days | real_l2_anchor_gate | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase145 | scripts\run_phase145_real_l2_post_download_refresh.py | outputs\phase145 |
| 146 | 1 | 1 | True | True | True | gated_waiting_for_more_real_anchor_days | real_l2_anchor_gate | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase145_phase146 | scripts\run_phase146_real_anchor_minimum_unlock_audit.py | outputs\phase146 |
| 147 | 1 | 1 | True | True | True | gated_waiting_for_more_real_anchor_days | real_l2_anchor_gate | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase147 | scripts\run_phase147_azcopy_download_intake_audit.py | outputs\phase147 |
| 148 | 1 | 1 | True | True | True | gated_waiting_for_more_real_anchor_days | real_l2_anchor_gate | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase148 | scripts\run_phase148_real_l2_download_refresh_workflow.ps1 | outputs\phase148 |
| 149 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase149_research_state_auditor.py | outputs\phase149 |
| 150 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase150_real_l2_duckdb_catalog.py | outputs\phase150 |
| 151 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase151_real_l2_duckdb_query_benchmark.py | outputs\phase151 |
| 152 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase152_real_l2_microstructure_profile.py | outputs\phase152 |
| 153 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase153_real_synthetic_microstructure_gap_audit.py | outputs\phase153 |
| 154 | 1 | 2 | True | True | True | smoke_or_partial |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase154_full_partition_real_cadence_anchor.py | outputs\phase154\|outputs\phase154_smoke |
| 155 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase155_full_partition_cadence_calibration_contract.py | outputs\phase155 |
| 156 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase156_symbol_aware_tail_cadence_smoke.py | outputs\phase156 |
| 157 | 1 | 1 | True | True | True | evidence_present |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | scripts\run_phase157_full_partition_cadence_rewire_audit.py | outputs\phase157 |
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
