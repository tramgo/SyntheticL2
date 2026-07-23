# Phase149 Research State Auditor

Generated UTC: 2026-07-23T18:58:32.075004+00:00

Phase149 reconciles current phase scripts, output evidence, branch states, and replay gates.
It does not run strategies, contact Azure, import data, or unlock replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase149_phase_rows | 168 | Phase rows discovered from scripts and outputs |
| phase149_runner_phase_rows | 166 | Phase rows with at least one runner |
| phase149_acceptance_phase_rows | 118 | Phase rows with acceptance summaries |
| phase149_branch_rows | 4 | Current research branches summarized |
| phase149_hard_gate_rows | 8 | Hard global-state gates evaluated |
| phase149_hard_gate_pass_rows | 8 | Hard global-state gates passed |
| phase149_strategy_replay_allowed | 0 | Phase149 never unlocks strategy replay |
| phase149_next_best_action | add_AZURE_STORAGE_SAS_TOKEN_or_AZURE_STORAGE_KEY_then_rerun_phase174 | Recommended next milestone |

## Branch Status Summary

| branch | status | evidence | current_next_action |
| --- | --- | --- | --- |
| real_l2_anchor_gate | gated | Phase146/148 keep strategy replay closed until at least five ready real-anchor days are proven. | use_phase174_secure_download_orchestrator_for_required_real_l2_dates |
| real_receive_flow_source | gated_waiting_for_two_more_real_l2_dates | Phase172 ready_dates=3, additional_dates_needed=2; Phase174 download_ran=0; Phase175 activation_ready=0. | add_AZURE_STORAGE_SAS_TOKEN_or_AZURE_STORAGE_KEY_then_rerun_phase174_phase172_before_phase176 |
| top_five_depth_passive | closed_clean_falsification | Phase136 Outcome A closes the branch after Phase132 kill-switch and Phase116 blocklist verification. | do_not_open_phase134_or_phase135_for_this_branch |
| dense_synthetic_replay | not_promoted | Partial/smoke dense replay artifacts remain non-promotional and do not override replay gates. | only_continue_if_precommitted_and_not_blocklisted |

## Global Gate Evaluation

| gate | pass | observed | required | severity |
| --- | --- | --- | --- | --- |
| phase149_real_l2_replay_gate_closed | True | 0 | 0 | hard |
| phase149_real_receive_flow_replay_gate_closed | True | 0 | 0 | hard |
| phase149_secure_download_gate_recorded | True | 1 | 1 | hard |
| phase149_secure_orchestrator_replay_gate_closed | True | 0 | 0 | hard |
| phase149_receive_flow_feature_schema_recorded | True | 1 | 1 | hard |
| phase149_receive_flow_feature_schema_replay_gate_closed | True | 0 | 0 | hard |
| phase149_deep_book_branch_closed | True | 1 | 1 | hard |
| phase149_no_promoted_strategy_replay | True | 0 | 0 | hard |

## Phase Status Ledger

| phase | runner_count | output_rows | has_runner | has_outputs | has_acceptance_summary | status | branch | strategy_replay_allowed | next_action | runner | output_dir |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 91 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase91_cross_symbol_regime_imbalance_replay.py | outputs\phase91 |
| 92 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase92_low_turnover_event_window_precommit.py | outputs\phase92 |
| 93 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase93_low_turnover_event_window_replay.py | outputs\phase93 |
| 94 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase94_generator_realism_calibration_audit.py | outputs\phase94 |
| 95 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase95_real_anchor_panel_contract.py | outputs\phase95 |
| 96 | 1 | 1 | True | True | True | gated_waiting_for_more_real_anchor_days | real_l2_anchor_gate | 0 |  | scripts\run_phase96_real_anchor_panel_builder.py | outputs\phase96 |
| 97 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase97_generator_recalibration_patch_plan.py | outputs\phase97 |
| 98 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase98_generator_calibration_config_contract.py | outputs\phase98 |
| 99 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase99_generator_calibration_wiring_verifier.py | outputs\phase99 |
| 100 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase100_calibrated_generator_quality_smoke.py | outputs\phase100 |
| 101 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase101_calibrated_phase49_shard_quality_audit.py | outputs\phase101 |
| 102 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase102_anchored_price_volatility_patch_audit.py | outputs\phase102 |
| 103 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase103_calibrated_realism_rerun.py | outputs\phase103 |
| 104 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase104_real_anchor_cadence_profile_audit.py | outputs\phase104 |
| 105 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase105_source_mid_volatility_scale_audit.py | outputs\phase105 |
| 106 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase106_full_symbol_calibrated_realism_audit.py | outputs\phase106 |
| 107 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase107_symbol_aware_calibration_contract.py | outputs\phase107 |
| 108 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase108_symbol_aware_generator_override_audit.py | outputs\phase108 |
| 109 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase109_residual_imbalance_floor_audit.py | outputs\phase109 |
| 110 | 1 | 1 | True | True | True | gated_waiting_for_more_real_anchor_days | real_l2_anchor_gate | 0 |  | scripts\run_phase110_multiday_replay_unlock_gate.py | outputs\phase110 |
| 111 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase111_real_anchor_ingest_discovery.py | outputs\phase111 |
| 112 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase112_dropzone_phase96_compatibility.py | outputs\phase112 |
| 113 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase113_real_l2_dropzone_importer.py | outputs\phase113 |
| 114 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase114_dropzone_import_integrity_verifier.py | outputs\phase114 |
| 115 | 1 | 1 | True | True | True | gated_waiting_for_more_real_anchor_days | real_l2_anchor_gate | 0 |  | scripts\run_phase115_real_panel_refresh_orchestrator.py | outputs\phase115 |
| 116 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase116_profitability_verdict_and_research_gate.py | outputs\phase116 |
| 117 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase117_real_anchor_acquisition_work_order.py | outputs\phase117 |
| 118 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase118_richer_passive_hypothesis_precommit.py | outputs\phase118 |
| 119 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase119_richer_passive_label_builder.py | outputs\phase119 |
| 120 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase120_passive_label_coverage_expansion_plan.py | outputs\phase120 |
| 121 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase121_passive_branch_retirement_gate.py | outputs\phase121 |
| 122 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase122_non_trading_forecast_filter_precommit.py | outputs\phase122 |
| 123 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase123_filter_label_matrix_builder.py | outputs\phase123 |
| 124 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase124_non_trading_filter_baselines.py | outputs\phase124 |
| 125 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase125_filter_integration_contract.py | outputs\phase125 |
| 126 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase126_candidate_generation_permission_ledger.py | outputs\phase126 |
| 127 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase127_allowed_universe_precommit_queue.py | outputs\phase127 |
| 128 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase128_next_label_design_spec.py | outputs\phase128 |
| 129 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase129_allowed_context_label_matrix.py | outputs\phase129 |
| 130 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase130_no_replay_diagnostic_baselines.py | outputs\phase130 |
| 131 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase131_deep_book_feature_precommit.py | outputs\phase131 |
| 132 | 1 | 1 | True | True | True | closed_kill_switch | top_five_depth_passive | 0 | stop_update_phase116_blocklist | scripts\run_phase132_deep_book_feature_diagnostics.py | outputs\phase132 |
| 133 | 1 | 1 | True | True | True | execution_contract_pinned_phase134_closed | top_five_depth_passive | 0 | stop_update_phase116_blocklist_do_not_open_phase134 | scripts\run_phase133_passive_execution_model_upgrade.py | outputs\phase133 |
| 136 | 1 | 1 | True | True | True | closed_clean_falsification | top_five_depth_passive | 0 | wait_for_real_l2_anchor_unlock_or_start_new_precommitted_non_blocklisted_research_branch | scripts\run_phase136_deep_book_verdict_and_handoff.py | outputs\phase136 |
| 137 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase137_post_phase132_real_anchor_restart.py | outputs\phase137 |
| 138 | 0 | 1 | False | True | False | script_only |  |  |  |  | outputs\phase138 |
| 139 | 0 | 1 | False | True | False | smoke_or_partial |  |  |  |  | outputs\phase139_smoke |
| 142 | 1 | 1 | True | True | True | gated_waiting_for_more_real_anchor_days | real_l2_anchor_gate | 0 |  | scripts\run_phase142_local_real_l2_download_verifier.py | outputs\phase142 |
| 143 | 1 | 1 | True | True | True | gated_waiting_for_more_real_anchor_days | real_l2_anchor_gate | 0 | download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase142_phase143 | scripts\run_phase143_real_l2_two_date_preflight.py | outputs\phase143 |
| 145 | 1 | 1 | True | True | True | gated_waiting_for_more_real_anchor_days | real_l2_anchor_gate | 0 | download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase145 | scripts\run_phase145_real_l2_post_download_refresh.py | outputs\phase145 |
| 146 | 1 | 1 | True | True | True | gated_waiting_for_more_real_anchor_days | real_l2_anchor_gate | 0 | download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase145_phase146 | scripts\run_phase146_real_anchor_minimum_unlock_audit.py | outputs\phase146 |
| 147 | 1 | 1 | True | True | True | gated_waiting_for_more_real_anchor_days | real_l2_anchor_gate | 0 | download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase147 | scripts\run_phase147_azcopy_download_intake_audit.py | outputs\phase147 |
| 148 | 1 | 1 | True | True | True | gated_waiting_for_more_real_anchor_days | real_l2_anchor_gate | 0 | download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase148 | scripts\run_phase148_real_l2_download_refresh_workflow.ps1 | outputs\phase148 |
| 149 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase149_research_state_auditor.py | outputs\phase149 |
| 150 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase150_real_l2_duckdb_catalog.py | outputs\phase150 |
| 151 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase151_real_l2_duckdb_query_benchmark.py | outputs\phase151 |
| 152 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase152_real_l2_microstructure_profile.py | outputs\phase152 |
| 153 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase153_real_synthetic_microstructure_gap_audit.py | outputs\phase153 |
| 154 | 1 | 2 | True | True | True | smoke_or_partial |  |  |  | scripts\run_phase154_full_partition_real_cadence_anchor.py | outputs\phase154\|outputs\phase154_smoke |
| 155 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase155_full_partition_cadence_calibration_contract.py | outputs\phase155 |
| 156 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase156_symbol_aware_tail_cadence_smoke.py | outputs\phase156 |
| 157 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase157_full_partition_cadence_rewire_audit.py | outputs\phase157 |
| 158 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase158_phase106_style_full_realism_audit.py | outputs\phase158 |
| 159 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase159_distributional_cadence_smoke.py | outputs\phase159 |
| 160 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase160_phase159_noncadence_realism_audit.py | outputs\phase160 |
| 161 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase161_combined_realism_handoff_gate.py | outputs\phase161 |
| 162 | 1 | 2 | True | True | True | smoke_or_partial |  |  |  | scripts\run_phase162_phase159_full_year_materialization_audit.py | outputs\phase162\|outputs\phase162_smoke |
| 163 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase163_synthetic_only_replay_preflight.py | outputs\phase163 |
| 164 | 1 | 2 | True | True | True | smoke_or_partial |  |  |  | scripts\run_phase164_synthetic_only_full_year_replay.py | outputs\phase164\|outputs\phase164_smoke |
| 165 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase165_phase164_full_year_replay_verdict.py | outputs\phase165 |
| 166 | 1 | 2 | True | True | True | smoke_or_partial |  |  |  | scripts\run_phase166_cross_symbol_lead_lag_cache.py | outputs\phase166\|outputs\phase166_smoke |
| 167 | 1 | 2 | True | True | True | smoke_or_partial |  |  |  | scripts\run_phase167_s08_cross_symbol_lead_lag_replay.py | outputs\phase167\|outputs\phase167_smoke |
| 168 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase168_s08_closure_verdict.py | outputs\phase168 |
| 169 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase169_post_s08_research_queue.py | outputs\phase169 |
| 170 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase170_filter_conditioned_feasibility_matrix.py | outputs\phase170 |
| 171 | 1 | 1 | True | True | True | source_contract_declared_no_replay | real_receive_flow_source | 0 | run_download_first_real_l2_receive_flow_availability_audit_or_collect_broker_order_telemetry | scripts\run_phase171_external_orderflow_source_contract.py | outputs\phase171 |
| 172 | 1 | 1 | True | True | True | local_receive_flow_structural_ready_but_day_count_gated | real_receive_flow_source | 0 | download_at_least_2_additional_real_l2_dates_then_rerun_phase172 | scripts\run_phase172_real_l2_receive_flow_availability_audit.py | outputs\phase172 |
| 173 | 1 | 1 | True | True | True | download_preflight_waiting_for_sas_or_key_or_tls_fix | real_receive_flow_download_gate | 0 | provide_share_sas_or_storage_key_or_repair_azure_cli_tls_then_run_phase148_download | scripts\run_phase173_real_l2_download_credential_preflight.py | outputs\phase173 |
| 174 | 1 | 1 | True | True | True | secure_download_skipped_no_credential | real_receive_flow_download_gate | 0 | add_AZURE_STORAGE_SAS_TOKEN_or_AZURE_STORAGE_KEY_to_env_or_process_then_rerun_phase174 | scripts\run_phase174_secure_real_l2_download_orchestrator.ps1 | outputs\phase174 |
| 175 | 1 | 1 | True | True | True | receive_flow_feature_schema_precommitted_gated | real_receive_flow_source | 0 | add_AZURE_STORAGE_SAS_TOKEN_or_AZURE_STORAGE_KEY_then_rerun_phase174_phase172_before_phase176 | scripts\run_phase175_receive_flow_feature_schema_precommit.py | outputs\phase175 |
