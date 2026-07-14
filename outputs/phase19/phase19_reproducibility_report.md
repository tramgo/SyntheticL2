# Phase 19 Reproducibility Report

Generated UTC: 2026-07-14T16:15:38.152966+00:00

## Scope

This phase audits whether current manifests contain the metadata needed for exact regeneration.
It treats aliases and inferred references as useful but not as strong as exact versioned fields.

## Coverage Status Summary

| coverage_status | field_checks |
| --- | --- |
| present_exact | 310 |

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
| phase3 | outputs/phase3/regime_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase4 | outputs/phase4/scenario_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase5 | outputs/phase5/price_process_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase6 | outputs/phase6/l2_book_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase7 | outputs/phase7/shock_library_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase8 | outputs/phase8/retail_feed_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase9 | outputs/phase9/data_product_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| stage_a1 | outputs/stage_a1/manifest_check.json | 10 | 10 | 0 | 0 | 0 | True |

## Reproducibility Gaps

_No rows._

## Remediation Status

| remediation_status | field_checks | artifacts |
| --- | --- | --- |
| complete_exact | 310 | 31 |

## Normalized Manifest Overlay

The overlay provides exact required-field manifests for current audit artifacts without rewriting historical source manifests.
It is a reproducibility bridge, not proof that every original phase generator already emits normalized manifests.

| overlay_metric | value |
| --- | --- |
| normalized_overlay_artifacts | 31 |
| exact_field_overlay_ready_artifacts | 31 |
| normalizer_default_fields | 0 |
| source_manifest_exact_or_alias_fields | 310 |
| normalized_field_rows | 310 |

| artifact_id | source_manifest_path | normalized_manifest_path | source_manifest_exists | required_fields | normalized_fields_present | normalizer_default_fields | source_manifest_exact_or_alias_fields | exact_field_overlay_ready |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stage_a1 | outputs/stage_a1/manifest_check.json | outputs\phase19\normalized_manifests\stage_a1.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase1 | outputs/phase1/phase1_manifest.json | outputs\phase19\normalized_manifests\phase1.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase1_event_reconstruction | outputs/phase1/event_reconstruction/event_reconstruction_manifest.json | outputs\phase19\normalized_manifests\phase1_event_reconstruction.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
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
