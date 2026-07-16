# Phase 19 Reproducibility Report

Generated UTC: 2026-07-16T15:23:13.520861+00:00

## Scope

This phase audits whether current manifests contain the metadata needed for exact regeneration.
It treats aliases and inferred references as useful but not as strong as exact versioned fields.

## Coverage Status Summary

| coverage_status | field_checks |
| --- | --- |
| present_exact | 680 |

## Artifact Summary

| artifact_id | manifest_path | required_fields | present_exact | present_alias_or_inferred | missing_fields | manifest_missing_or_unreadable_fields | exact_regeneration_ready |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| horizon_readiness | outputs/horizon_readiness/horizon_readiness_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase1 | outputs/phase1/phase1_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase10 | outputs/phase10/storage_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase11 | outputs/phase11/strategy_validation_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase11_strategy_modules | outputs/phase11/strategy_module_registry_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase12 | outputs/phase12/execution_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase12_event_backtest | outputs/phase12/event_backtest_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase13 | outputs/phase13/experiment_design_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase13_smoke_run | outputs/phase13/experiment_run_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase14 | outputs/phase14/quality_validation_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase15 | outputs/phase15/acceptance_gates_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase16 | outputs/phase16/metrics_reporting_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase17 | outputs/phase17/work_packages_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase18 | outputs/phase18/technology_stack_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase1_event_reconstruction | outputs/phase1/event_reconstruction/event_reconstruction_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase2 | outputs/phase2/calibration_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase20 | outputs/phase20/acceptance_hardening_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase20_m01 | outputs/phase20_m01/broker_evidence_contract_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase20_m02 | outputs/phase20_m02/strategy_support_contract_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase20_m03 | outputs/phase20_m03/predictive_validation_contract_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase20_m04 | outputs/phase20_m04/robustness_execution_contract_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase20_m05 | outputs/phase20_m05/lifecycle_economic_replay_contract_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase20_m06 | outputs/phase20_m06/realism_rerun_contract_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase20_m07 | outputs/phase20_m07/real_multiday_acceptance_contract_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase21 | outputs/phase21/phase21_decision_framework_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase22 | outputs/phase22/phase22_real_data_integration_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase23 | outputs/phase23/phase23_key_risk_register_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase25 | outputs/phase25/phase25_event_replay_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase26 | outputs/phase26/phase26_strategy_salvage_scan_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase27 | outputs/phase27/phase27_feature_edge_scan_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase28 | outputs/phase28/phase28_richer_event_label_support_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase29 | outputs/phase29/phase29_partial_strategy_proxy_replay_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase3 | outputs/phase3/regime_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase30 | outputs/phase30/phase30_strategy_decision_triage_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase31 | outputs/phase31/phase31_redesign_evidence_contract_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase32 | outputs/phase32/phase32_contract_evidence_scanner_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase33 | outputs/phase33/phase33_broker_evidence_intake_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase34 | outputs/phase34/phase34_real_data_multiday_readiness_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase35 | outputs/phase35/phase35_stage_a2_computable_diagnostics_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase36 | outputs/phase36/phase36_collector_instrumentation_package_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase37 | outputs/phase37/phase37_collector_ledger_verifier_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase38 | outputs/phase38/phase38_class_b_promotion_gate_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase39 | outputs/phase39/phase39_synthetic_only_acceptance_path_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase4 | outputs/phase4/scenario_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase41 | outputs/phase41/phase41_full_year_synthetic_tick_experiment_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase42 | outputs/phase42/phase42_native_full_year_l2_experiment_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase43 | outputs/phase43/phase43_native_full_year_cost_salvage_scan_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase44 | outputs/phase44/phase44_native_full_year_forward_edge_label_mining_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase45 | outputs/phase45/phase45_raw_tick_lake_materialization_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase46 | outputs/phase46/phase46_raw_tick_lake_replay_diagnostics_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase47 | outputs/phase47/phase47_raw_lake_duckdb_catalog_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase48 | outputs/phase48/phase48_raw_lake_compaction_benchmark_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase49 | outputs/phase49/phase49_dense_tick_rate_expansion_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase5 | outputs/phase5/price_process_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase50 | outputs/phase50/phase50_dense_lake_shard_planner_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase6 | outputs/phase6/l2_book_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase7 | outputs/phase7/shock_library_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase8 | outputs/phase8/retail_feed_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase9 | outputs/phase9/data_product_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| stage_a1 | outputs/stage_a1/manifest_check.json | 10 | 10 | 0 | 0 | 0 | True |
| stage_a2 | outputs/stage_a2/stage_a2_capture_diagnostics_contract_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| stage_b1 | outputs/stage_b1/stage_b1_structural_synthetic_proof_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| stage_b2 | outputs/stage_b2/stage_b2_event_driven_synthetic_proof_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| stage_c | outputs/stage_c/stage_c_medium_pilot_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| stage_d | outputs/stage_d/stage_d_three_month_study_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| stage_e | outputs/stage_e/stage_e_full_year_readiness_manifest.json | 10 | 10 | 0 | 0 | 0 | True |

## Reproducibility Gaps

_No rows._

## Remediation Status

| remediation_status | field_checks | artifacts |
| --- | --- | --- |
| complete_exact | 680 | 68 |

## Normalized Manifest Overlay

The overlay provides exact required-field manifests for current audit artifacts without rewriting historical source manifests.
It is a reproducibility bridge, not proof that every original phase generator already emits normalized manifests.

| overlay_metric | value |
| --- | --- |
| normalized_overlay_artifacts | 68 |
| exact_field_overlay_ready_artifacts | 68 |
| normalizer_default_fields | 0 |
| source_manifest_exact_or_alias_fields | 680 |
| normalized_field_rows | 680 |

| artifact_id | source_manifest_path | normalized_manifest_path | source_manifest_exists | required_fields | normalized_fields_present | normalizer_default_fields | source_manifest_exact_or_alias_fields | exact_field_overlay_ready |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stage_a1 | outputs/stage_a1/manifest_check.json | outputs\phase19\normalized_manifests\stage_a1.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase1 | outputs/phase1/phase1_manifest.json | outputs\phase19\normalized_manifests\phase1.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase1_event_reconstruction | outputs/phase1/event_reconstruction/event_reconstruction_manifest.json | outputs\phase19\normalized_manifests\phase1_event_reconstruction.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| stage_a2 | outputs/stage_a2/stage_a2_capture_diagnostics_contract_manifest.json | outputs\phase19\normalized_manifests\stage_a2.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| stage_b1 | outputs/stage_b1/stage_b1_structural_synthetic_proof_manifest.json | outputs\phase19\normalized_manifests\stage_b1.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| stage_b2 | outputs/stage_b2/stage_b2_event_driven_synthetic_proof_manifest.json | outputs\phase19\normalized_manifests\stage_b2.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| stage_c | outputs/stage_c/stage_c_medium_pilot_manifest.json | outputs\phase19\normalized_manifests\stage_c.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| stage_d | outputs/stage_d/stage_d_three_month_study_manifest.json | outputs\phase19\normalized_manifests\stage_d.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| stage_e | outputs/stage_e/stage_e_full_year_readiness_manifest.json | outputs\phase19\normalized_manifests\stage_e.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase21 | outputs/phase21/phase21_decision_framework_manifest.json | outputs\phase19\normalized_manifests\phase21.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase22 | outputs/phase22/phase22_real_data_integration_manifest.json | outputs\phase19\normalized_manifests\phase22.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase23 | outputs/phase23/phase23_key_risk_register_manifest.json | outputs\phase19\normalized_manifests\phase23.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase25 | outputs/phase25/phase25_event_replay_manifest.json | outputs\phase19\normalized_manifests\phase25.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase26 | outputs/phase26/phase26_strategy_salvage_scan_manifest.json | outputs\phase19\normalized_manifests\phase26.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase27 | outputs/phase27/phase27_feature_edge_scan_manifest.json | outputs\phase19\normalized_manifests\phase27.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase28 | outputs/phase28/phase28_richer_event_label_support_manifest.json | outputs\phase19\normalized_manifests\phase28.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase29 | outputs/phase29/phase29_partial_strategy_proxy_replay_manifest.json | outputs\phase19\normalized_manifests\phase29.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase30 | outputs/phase30/phase30_strategy_decision_triage_manifest.json | outputs\phase19\normalized_manifests\phase30.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase31 | outputs/phase31/phase31_redesign_evidence_contract_manifest.json | outputs\phase19\normalized_manifests\phase31.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase32 | outputs/phase32/phase32_contract_evidence_scanner_manifest.json | outputs\phase19\normalized_manifests\phase32.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase33 | outputs/phase33/phase33_broker_evidence_intake_manifest.json | outputs\phase19\normalized_manifests\phase33.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase34 | outputs/phase34/phase34_real_data_multiday_readiness_manifest.json | outputs\phase19\normalized_manifests\phase34.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase35 | outputs/phase35/phase35_stage_a2_computable_diagnostics_manifest.json | outputs\phase19\normalized_manifests\phase35.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase36 | outputs/phase36/phase36_collector_instrumentation_package_manifest.json | outputs\phase19\normalized_manifests\phase36.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase37 | outputs/phase37/phase37_collector_ledger_verifier_manifest.json | outputs\phase19\normalized_manifests\phase37.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase38 | outputs/phase38/phase38_class_b_promotion_gate_manifest.json | outputs\phase19\normalized_manifests\phase38.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase39 | outputs/phase39/phase39_synthetic_only_acceptance_path_manifest.json | outputs\phase19\normalized_manifests\phase39.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase41 | outputs/phase41/phase41_full_year_synthetic_tick_experiment_manifest.json | outputs\phase19\normalized_manifests\phase41.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase42 | outputs/phase42/phase42_native_full_year_l2_experiment_manifest.json | outputs\phase19\normalized_manifests\phase42.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase43 | outputs/phase43/phase43_native_full_year_cost_salvage_scan_manifest.json | outputs\phase19\normalized_manifests\phase43.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase44 | outputs/phase44/phase44_native_full_year_forward_edge_label_mining_manifest.json | outputs\phase19\normalized_manifests\phase44.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase45 | outputs/phase45/phase45_raw_tick_lake_materialization_manifest.json | outputs\phase19\normalized_manifests\phase45.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase46 | outputs/phase46/phase46_raw_tick_lake_replay_diagnostics_manifest.json | outputs\phase19\normalized_manifests\phase46.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase47 | outputs/phase47/phase47_raw_lake_duckdb_catalog_manifest.json | outputs\phase19\normalized_manifests\phase47.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase48 | outputs/phase48/phase48_raw_lake_compaction_benchmark_manifest.json | outputs\phase19\normalized_manifests\phase48.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase49 | outputs/phase49/phase49_dense_tick_rate_expansion_manifest.json | outputs\phase19\normalized_manifests\phase49.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase50 | outputs/phase50/phase50_dense_lake_shard_planner_manifest.json | outputs\phase19\normalized_manifests\phase50.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase2 | outputs/phase2/calibration_manifest.json | outputs\phase19\normalized_manifests\phase2.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase3 | outputs/phase3/regime_manifest.json | outputs\phase19\normalized_manifests\phase3.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase4 | outputs/phase4/scenario_manifest.json | outputs\phase19\normalized_manifests\phase4.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase5 | outputs/phase5/price_process_manifest.json | outputs\phase19\normalized_manifests\phase5.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase6 | outputs/phase6/l2_book_manifest.json | outputs\phase19\normalized_manifests\phase6.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase7 | outputs/phase7/shock_library_manifest.json | outputs\phase19\normalized_manifests\phase7.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase8 | outputs/phase8/retail_feed_manifest.json | outputs\phase19\normalized_manifests\phase8.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase9 | outputs/phase9/data_product_manifest.json | outputs\phase19\normalized_manifests\phase9.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase10 | outputs/phase10/storage_manifest.json | outputs\phase19\normalized_manifests\phase10.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase11 | outputs/phase11/strategy_validation_manifest.json | outputs\phase19\normalized_manifests\phase11.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase11_strategy_modules | outputs/phase11/strategy_module_registry_manifest.json | outputs\phase19\normalized_manifests\phase11_strategy_modules.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase12 | outputs/phase12/execution_manifest.json | outputs\phase19\normalized_manifests\phase12.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase12_event_backtest | outputs/phase12/event_backtest_manifest.json | outputs\phase19\normalized_manifests\phase12_event_backtest.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase13 | outputs/phase13/experiment_design_manifest.json | outputs\phase19\normalized_manifests\phase13.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase13_smoke_run | outputs/phase13/experiment_run_manifest.json | outputs\phase19\normalized_manifests\phase13_smoke_run.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase14 | outputs/phase14/quality_validation_manifest.json | outputs\phase19\normalized_manifests\phase14.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase15 | outputs/phase15/acceptance_gates_manifest.json | outputs\phase19\normalized_manifests\phase15.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase16 | outputs/phase16/metrics_reporting_manifest.json | outputs\phase19\normalized_manifests\phase16.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase17 | outputs/phase17/work_packages_manifest.json | outputs\phase19\normalized_manifests\phase17.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase18 | outputs/phase18/technology_stack_manifest.json | outputs\phase19\normalized_manifests\phase18.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase20 | outputs/phase20/acceptance_hardening_manifest.json | outputs\phase19\normalized_manifests\phase20.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase20_m01 | outputs/phase20_m01/broker_evidence_contract_manifest.json | outputs\phase19\normalized_manifests\phase20_m01.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase20_m02 | outputs/phase20_m02/strategy_support_contract_manifest.json | outputs\phase19\normalized_manifests\phase20_m02.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase20_m03 | outputs/phase20_m03/predictive_validation_contract_manifest.json | outputs\phase19\normalized_manifests\phase20_m03.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase20_m04 | outputs/phase20_m04/robustness_execution_contract_manifest.json | outputs\phase19\normalized_manifests\phase20_m04.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase20_m05 | outputs/phase20_m05/lifecycle_economic_replay_contract_manifest.json | outputs\phase19\normalized_manifests\phase20_m05.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase20_m06 | outputs/phase20_m06/realism_rerun_contract_manifest.json | outputs\phase19\normalized_manifests\phase20_m06.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase20_m07 | outputs/phase20_m07/real_multiday_acceptance_contract_manifest.json | outputs\phase19\normalized_manifests\phase20_m07.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| horizon_readiness | outputs/horizon_readiness/horizon_readiness_manifest.json | outputs\phase19\normalized_manifests\horizon_readiness.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | outputs\phase19\normalized_manifests\dashboard.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | outputs\phase19\normalized_manifests\duckdb.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |

## Highest Priority Remediation Rows

| artifact_id | manifest_path | required_field | current_coverage_status | matched_aliases | remediation_status | recommended_value_source | recommended_action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | calibration_dataset_id | present_exact | calibration_dataset_id | complete_exact | calibration_dataset_id | No remediation required. |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | configuration_hash | present_exact | configuration_hash | complete_exact | configuration_hash | No remediation required. |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | cost_model_version | present_exact | cost_model_version | complete_exact | cost_model_version | No remediation required. |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | creation_timestamp | present_exact | creation_timestamp;generated_utc | complete_exact | creation_timestamp | No remediation required. |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | generator_version | present_exact | generator_version | complete_exact | generator_version | No remediation required. |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | latency_model_version | present_exact | latency_model_version | complete_exact | latency_model_version | No remediation required. |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | random_seed | present_exact | random_seed | complete_exact | random_seed | No remediation required. |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | regime_calendar_version | present_exact | regime_calendar_version | complete_exact | regime_calendar_version | No remediation required. |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | scenario_ids | present_exact | scenario_ids | complete_exact | scenario_ids | No remediation required. |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | ticker_metadata_version | present_exact | ticker_metadata_version | complete_exact | ticker_metadata_version | No remediation required. |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | calibration_dataset_id | present_exact | calibration_dataset_id | complete_exact | calibration_dataset_id | No remediation required. |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | configuration_hash | present_exact | configuration_hash | complete_exact | configuration_hash | No remediation required. |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | cost_model_version | present_exact | cost_model_version | complete_exact | cost_model_version | No remediation required. |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | creation_timestamp | present_exact | creation_timestamp;generated_utc | complete_exact | creation_timestamp | No remediation required. |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | generator_version | present_exact | generator_version | complete_exact | generator_version | No remediation required. |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | latency_model_version | present_exact | latency_model_version | complete_exact | latency_model_version | No remediation required. |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | random_seed | present_exact | random_seed | complete_exact | random_seed | No remediation required. |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | regime_calendar_version | present_exact | regime_calendar_version | complete_exact | regime_calendar_version | No remediation required. |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | scenario_ids | present_exact | scenario_ids | complete_exact | scenario_ids | No remediation required. |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | ticker_metadata_version | present_exact | ticker_metadata_version | complete_exact | ticker_metadata_version | No remediation required. |
| horizon_readiness | outputs/horizon_readiness/horizon_readiness_manifest.json | calibration_dataset_id | present_exact | calibration_dataset_id | complete_exact | calibration_dataset_id | No remediation required. |
| horizon_readiness | outputs/horizon_readiness/horizon_readiness_manifest.json | configuration_hash | present_exact | configuration_hash | complete_exact | configuration_hash | No remediation required. |
| horizon_readiness | outputs/horizon_readiness/horizon_readiness_manifest.json | cost_model_version | present_exact | cost_model_version | complete_exact | cost_model_version | No remediation required. |
| horizon_readiness | outputs/horizon_readiness/horizon_readiness_manifest.json | creation_timestamp | present_exact | creation_timestamp;generated_utc | complete_exact | creation_timestamp | No remediation required. |
| horizon_readiness | outputs/horizon_readiness/horizon_readiness_manifest.json | generator_version | present_exact | generator_version | complete_exact | generator_version | No remediation required. |
| horizon_readiness | outputs/horizon_readiness/horizon_readiness_manifest.json | latency_model_version | present_exact | latency_model_version | complete_exact | latency_model_version | No remediation required. |
| horizon_readiness | outputs/horizon_readiness/horizon_readiness_manifest.json | random_seed | present_exact | random_seed | complete_exact | random_seed | No remediation required. |
| horizon_readiness | outputs/horizon_readiness/horizon_readiness_manifest.json | regime_calendar_version | present_exact | regime_calendar_version | complete_exact | regime_calendar_version | No remediation required. |
| horizon_readiness | outputs/horizon_readiness/horizon_readiness_manifest.json | scenario_ids | present_exact | scenario_ids | complete_exact | scenario_ids | No remediation required. |
| horizon_readiness | outputs/horizon_readiness/horizon_readiness_manifest.json | ticker_metadata_version | present_exact | ticker_metadata_version | complete_exact | ticker_metadata_version | No remediation required. |
| phase1 | outputs/phase1/phase1_manifest.json | calibration_dataset_id | present_exact | calibration_dataset_id | complete_exact | calibration_dataset_id | No remediation required. |
| phase1 | outputs/phase1/phase1_manifest.json | configuration_hash | present_exact | configuration_hash | complete_exact | configuration_hash | No remediation required. |
| phase1 | outputs/phase1/phase1_manifest.json | cost_model_version | present_exact | cost_model_version | complete_exact | cost_model_version | No remediation required. |
| phase1 | outputs/phase1/phase1_manifest.json | creation_timestamp | present_exact | creation_timestamp;generated_utc | complete_exact | creation_timestamp | No remediation required. |
| phase1 | outputs/phase1/phase1_manifest.json | generator_version | present_exact | generator_version | complete_exact | generator_version | No remediation required. |
| phase1 | outputs/phase1/phase1_manifest.json | latency_model_version | present_exact | latency_model_version | complete_exact | latency_model_version | No remediation required. |
| phase1 | outputs/phase1/phase1_manifest.json | random_seed | present_exact | random_seed | complete_exact | random_seed | No remediation required. |
| phase1 | outputs/phase1/phase1_manifest.json | regime_calendar_version | present_exact | regime_calendar_version | complete_exact | regime_calendar_version | No remediation required. |
| phase1 | outputs/phase1/phase1_manifest.json | scenario_ids | present_exact | scenario_ids | complete_exact | scenario_ids | No remediation required. |
| phase1 | outputs/phase1/phase1_manifest.json | ticker_metadata_version | present_exact | ticker_metadata_version | complete_exact | ticker_metadata_version | No remediation required. |
