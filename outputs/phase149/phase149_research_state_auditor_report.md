# Phase149 Research State Auditor

Generated UTC: 2026-07-23T08:47:28.623805+00:00

Phase149 reconciles current phase scripts, output evidence, branch states, and replay gates.
It does not run strategies, contact Azure, import data, or unlock replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase149_phase_rows | 142 | Phase rows discovered from scripts and outputs |
| phase149_runner_phase_rows | 140 | Phase rows with at least one runner |
| phase149_acceptance_phase_rows | 91 | Phase rows with acceptance summaries |
| phase149_branch_rows | 3 | Current research branches summarized |
| phase149_hard_gate_rows | 3 | Hard global-state gates evaluated |
| phase149_hard_gate_pass_rows | 3 | Hard global-state gates passed |
| phase149_strategy_replay_allowed | 0 | Phase149 never unlocks strategy replay |
| phase149_next_best_action | download_real_l2_anchor_dates_with_phase148_or_start_new_precommitted_non_blocklisted_branch | Recommended next milestone |

## Branch Status Summary

| branch | status | evidence | current_next_action |
| --- | --- | --- | --- |
| real_l2_anchor_gate | gated | Phase146/148 keep strategy replay closed until at least five ready real-anchor days are proven. | download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase148 |
| top_five_depth_passive | closed_clean_falsification | Phase136 Outcome A closes the branch after Phase132 kill-switch and Phase116 blocklist verification. | do_not_open_phase134_or_phase135_for_this_branch |
| dense_synthetic_replay | not_promoted | Partial/smoke dense replay artifacts remain non-promotional and do not override replay gates. | only_continue_if_precommitted_and_not_blocklisted |

## Global Gate Evaluation

| gate | pass | observed | required | severity |
| --- | --- | --- | --- | --- |
| phase149_real_l2_replay_gate_closed | True | 0 | 0 | hard |
| phase149_deep_book_branch_closed | True | 1 | 1 | hard |
| phase149_no_promoted_strategy_replay | True | 0 | 0 | hard |

## Phase Status Ledger

| phase | runner_count | output_rows | has_runner | has_outputs | has_acceptance_summary | status | branch | strategy_replay_allowed | next_action | runner | output_dir |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 65 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase65_passive_queue_sensitivity.py | outputs\phase65 |
| 66 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase66_passive_adverse_selection_labels.py | outputs\phase66 |
| 67 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase67_feature_design_budget_gate.py | outputs\phase67 |
| 68 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase68_replenishment_after_touch_labels.py | outputs\phase68 |
| 69 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase69_spread_transition_labels.py | outputs\phase69 |
| 70 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase70_cross_symbol_lead_lag_labels.py | outputs\phase70 |
| 71 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase71_shock_resilience_labels.py | outputs\phase71 |
| 72 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase72_research_audit_generator_assumptions.py | outputs\phase72 |
| 73 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase73_timestamp_alignment_shock_panel_audit.py | outputs\phase73 |
| 74 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase74_generator_alignment_remediation_plan.py | outputs\phase74 |
| 75 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase75_timestamp_contract_matrix_validator.py | outputs\phase75 |
| 76 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase76_common_overlap_matrix_validator.py | outputs\phase76 |
| 77 | 1 | 2 | True | True | True | smoke_or_partial |  |  |  | scripts\run_phase77_hdfcbank_disjoint_month_retest.py | outputs\phase77\|outputs\phase77_smoke |
| 78 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase78_post_falsification_research_gate.py | outputs\phase78 |
| 79 | 1 | 2 | True | True | True | smoke_or_partial |  |  |  | scripts\run_phase79_generator_scenario_diversity_audit.py | outputs\phase79\|outputs\phase79_smoke |
| 80 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase80_dense_sampling_recalibration_contract.py | outputs\phase80 |
| 81 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase81_stratified_dense_window_reader.py | outputs\phase81 |
| 82 | 1 | 2 | True | True | True | smoke_or_partial |  |  |  | scripts\run_phase82_stratified_hdfcbank_retest.py | outputs\phase82\|outputs\phase82_smoke |
| 83 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase83_stratified_source_event_bar_cache.py | outputs\phase83 |
| 84 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase84_cached_stratified_hdfcbank_retest.py | outputs\phase84 |
| 85 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase85_cost_budget_signal_design.py | outputs\phase85 |
| 86 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase86_composite_signal_precommit.py | outputs\phase86 |
| 87 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase87_precommitted_composite_signal_replay.py | outputs\phase87 |
| 88 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase88_strategy_pivot_decision_ledger.py | outputs\phase88 |
| 89 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase89_passive_queue_capture_cost_floor.py | outputs\phase89 |
| 90 | 1 | 1 | True | True | True | evidence_present |  |  |  | scripts\run_phase90_cross_symbol_regime_imbalance_precommit.py | outputs\phase90 |
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
| 149 | 1 | 1 | True | True | False | script_only |  |  |  | scripts\run_phase149_research_state_auditor.py | outputs\phase149 |
