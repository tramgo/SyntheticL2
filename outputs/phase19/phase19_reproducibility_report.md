# Phase 19 Reproducibility Report

Generated UTC: 2026-07-13T20:19:37.818066+00:00

## Scope

This phase audits whether current manifests contain the metadata needed for exact regeneration.
It treats aliases and inferred references as useful but not as strong as exact versioned fields.

## Coverage Status Summary

| coverage_status | field_checks |
| --- | --- |
| manifest_missing_or_unreadable | 10 |
| missing | 176 |
| present_alias_or_inferred | 33 |
| present_exact | 31 |

## Artifact Summary

| artifact_id | manifest_path | required_fields | present_exact | present_alias_or_inferred | missing_fields | manifest_missing_or_unreadable_fields | exact_regeneration_ready |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | 10 | 0 | 1 | 9 | 0 | False |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | 10 | 0 | 1 | 9 | 0 | False |
| phase1 | outputs/phase1/phase1_manifest.json | 10 | 0 | 0 | 0 | 10 | False |
| phase10 | outputs/phase10/storage_manifest.json | 10 | 0 | 1 | 9 | 0 | False |
| phase11 | outputs/phase11/strategy_validation_manifest.json | 10 | 0 | 2 | 8 | 0 | False |
| phase11_strategy_modules | outputs/phase11/strategy_module_registry_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase12 | outputs/phase12/execution_manifest.json | 10 | 1 | 3 | 6 | 0 | False |
| phase12_event_backtest | outputs/phase12/event_backtest_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase13 | outputs/phase13/experiment_design_manifest.json | 10 | 0 | 1 | 9 | 0 | False |
| phase13_smoke_run | outputs/phase13/experiment_run_manifest.json | 10 | 0 | 1 | 9 | 0 | False |
| phase14 | outputs/phase14/quality_validation_manifest.json | 10 | 0 | 2 | 8 | 0 | False |
| phase15 | outputs/phase15/acceptance_gates_manifest.json | 10 | 0 | 2 | 8 | 0 | False |
| phase16 | outputs/phase16/metrics_reporting_manifest.json | 10 | 0 | 2 | 8 | 0 | False |
| phase17 | outputs/phase17/work_packages_manifest.json | 10 | 0 | 1 | 9 | 0 | False |
| phase18 | outputs/phase18/technology_stack_manifest.json | 10 | 0 | 1 | 9 | 0 | False |
| phase1_event_reconstruction | outputs/phase1/event_reconstruction/event_reconstruction_manifest.json | 10 | 10 | 0 | 0 | 0 | True |
| phase2 | outputs/phase2/calibration_manifest.json | 10 | 0 | 2 | 8 | 0 | False |
| phase3 | outputs/phase3/regime_manifest.json | 10 | 0 | 2 | 8 | 0 | False |
| phase4 | outputs/phase4/scenario_manifest.json | 10 | 0 | 2 | 8 | 0 | False |
| phase5 | outputs/phase5/price_process_manifest.json | 10 | 0 | 2 | 8 | 0 | False |
| phase6 | outputs/phase6/l2_book_manifest.json | 10 | 0 | 2 | 8 | 0 | False |
| phase7 | outputs/phase7/shock_library_manifest.json | 10 | 0 | 2 | 8 | 0 | False |
| phase8 | outputs/phase8/retail_feed_manifest.json | 10 | 0 | 2 | 8 | 0 | False |
| phase9 | outputs/phase9/data_product_manifest.json | 10 | 0 | 1 | 9 | 0 | False |
| stage_a1 | outputs/stage_a1/manifest_check.json | 10 | 0 | 0 | 10 | 0 | False |

## Reproducibility Gaps

| required_field | coverage_status | artifact_count | affected_artifacts | recommended_action |
| --- | --- | --- | --- | --- |
| calibration_dataset_id | manifest_missing_or_unreadable | 1 | phase1 | Record real-data calibration dataset identifier and date range. |
| configuration_hash | manifest_missing_or_unreadable | 1 | phase1 | Serialize effective config and store a stable hash per artifact. |
| cost_model_version | manifest_missing_or_unreadable | 1 | phase1 | Version execution/cost assumptions and cost schedule. |
| creation_timestamp | manifest_missing_or_unreadable | 1 | phase1 | Store generated_utc or creation_timestamp in every manifest. |
| generator_version | manifest_missing_or_unreadable | 1 | phase1 | Add generator_version or code hash to every phase manifest. |
| latency_model_version | manifest_missing_or_unreadable | 1 | phase1 | Version feed latency/drop/duplication assumptions. |
| random_seed | manifest_missing_or_unreadable | 1 | phase1 | Record seed or seed-plan reference for every stochastic artifact. |
| regime_calendar_version | manifest_missing_or_unreadable | 1 | phase1 | Record scenario/regime calendar version for generated artifacts. |
| scenario_ids | manifest_missing_or_unreadable | 1 | phase1 | Record scenario IDs/profiles represented by each generated artifact. |
| ticker_metadata_version | manifest_missing_or_unreadable | 1 | phase1 | Version ticker universe and metadata source. |
| calibration_dataset_id | missing | 19 | dashboard;duckdb;phase10;phase13;phase13_smoke_run;phase14;phase15;phase16;phase17;phase18;phase2;phase3;phase4;phase5;phase6;phase7;phase8;phase9;stage_a1 | Record real-data calibration dataset identifier and date range. |
| configuration_hash | missing | 21 | dashboard;duckdb;phase10;phase11;phase12;phase13;phase13_smoke_run;phase14;phase15;phase16;phase17;phase18;phase2;phase3;phase4;phase5;phase6;phase7;phase8;phase9;stage_a1 | Serialize effective config and store a stable hash per artifact. |
| cost_model_version | missing | 19 | dashboard;duckdb;phase10;phase11;phase13;phase13_smoke_run;phase14;phase16;phase17;phase18;phase2;phase3;phase4;phase5;phase6;phase7;phase8;phase9;stage_a1 | Version execution/cost assumptions and cost schedule. |
| creation_timestamp | missing | 1 | stage_a1 | Store generated_utc or creation_timestamp in every manifest. |
| generator_version | missing | 21 | dashboard;duckdb;phase10;phase11;phase12;phase13;phase13_smoke_run;phase14;phase15;phase16;phase17;phase18;phase2;phase3;phase4;phase5;phase6;phase7;phase8;phase9;stage_a1 | Add generator_version or code hash to every phase manifest. |
| latency_model_version | missing | 20 | dashboard;duckdb;phase10;phase11;phase13;phase13_smoke_run;phase14;phase15;phase16;phase17;phase18;phase2;phase3;phase4;phase5;phase6;phase7;phase8;phase9;stage_a1 | Version feed latency/drop/duplication assumptions. |
| random_seed | missing | 20 | dashboard;duckdb;phase10;phase11;phase12;phase13;phase13_smoke_run;phase14;phase15;phase17;phase18;phase2;phase3;phase4;phase5;phase6;phase7;phase8;phase9;stage_a1 | Record seed or seed-plan reference for every stochastic artifact. |
| regime_calendar_version | missing | 20 | dashboard;duckdb;phase10;phase11;phase12;phase13;phase13_smoke_run;phase15;phase16;phase17;phase18;phase2;phase3;phase4;phase5;phase6;phase7;phase8;phase9;stage_a1 | Record scenario/regime calendar version for generated artifacts. |
| scenario_ids | missing | 21 | dashboard;duckdb;phase10;phase11;phase12;phase13;phase13_smoke_run;phase14;phase15;phase16;phase17;phase18;phase2;phase3;phase4;phase5;phase6;phase7;phase8;phase9;stage_a1 | Record scenario IDs/profiles represented by each generated artifact. |
| ticker_metadata_version | missing | 14 | dashboard;duckdb;phase10;phase11;phase12;phase13;phase13_smoke_run;phase14;phase15;phase16;phase17;phase18;phase9;stage_a1 | Version ticker universe and metadata source. |

## Remediation Status

| remediation_status | field_checks | artifacts |
| --- | --- | --- |
| add_field_in_generator | 176 | 21 |
| complete_exact | 31 | 4 |
| normalize_alias_to_exact_field | 33 | 20 |
| recover_or_rerun_manifest | 10 | 1 |

## Normalized Manifest Overlay

The overlay provides exact required-field manifests for current audit artifacts without rewriting historical source manifests.
It is a reproducibility bridge, not proof that every original phase generator already emits normalized manifests.

| overlay_metric | value |
| --- | --- |
| normalized_overlay_artifacts | 25 |
| exact_field_overlay_ready_artifacts | 25 |
| normalizer_default_fields | 187 |
| source_manifest_exact_or_alias_fields | 63 |
| normalized_field_rows | 250 |

| artifact_id | source_manifest_path | normalized_manifest_path | source_manifest_exists | required_fields | normalized_fields_present | normalizer_default_fields | source_manifest_exact_or_alias_fields | exact_field_overlay_ready |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stage_a1 | outputs/stage_a1/manifest_check.json | outputs\phase19\normalized_manifests\stage_a1.normalized_manifest.json | True | 10 | 10 | 10 | 0 | True |
| phase1 | outputs/phase1/phase1_manifest.json | outputs\phase19\normalized_manifests\phase1.normalized_manifest.json | False | 10 | 10 | 10 | 0 | True |
| phase1_event_reconstruction | outputs/phase1/event_reconstruction/event_reconstruction_manifest.json | outputs\phase19\normalized_manifests\phase1_event_reconstruction.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase2 | outputs/phase2/calibration_manifest.json | outputs\phase19\normalized_manifests\phase2.normalized_manifest.json | True | 10 | 10 | 8 | 2 | True |
| phase3 | outputs/phase3/regime_manifest.json | outputs\phase19\normalized_manifests\phase3.normalized_manifest.json | True | 10 | 10 | 8 | 2 | True |
| phase4 | outputs/phase4/scenario_manifest.json | outputs\phase19\normalized_manifests\phase4.normalized_manifest.json | True | 10 | 10 | 8 | 2 | True |
| phase5 | outputs/phase5/price_process_manifest.json | outputs\phase19\normalized_manifests\phase5.normalized_manifest.json | True | 10 | 10 | 8 | 2 | True |
| phase6 | outputs/phase6/l2_book_manifest.json | outputs\phase19\normalized_manifests\phase6.normalized_manifest.json | True | 10 | 10 | 8 | 2 | True |
| phase7 | outputs/phase7/shock_library_manifest.json | outputs\phase19\normalized_manifests\phase7.normalized_manifest.json | True | 10 | 10 | 8 | 2 | True |
| phase8 | outputs/phase8/retail_feed_manifest.json | outputs\phase19\normalized_manifests\phase8.normalized_manifest.json | True | 10 | 10 | 9 | 1 | True |
| phase9 | outputs/phase9/data_product_manifest.json | outputs\phase19\normalized_manifests\phase9.normalized_manifest.json | True | 10 | 10 | 9 | 1 | True |
| phase10 | outputs/phase10/storage_manifest.json | outputs\phase19\normalized_manifests\phase10.normalized_manifest.json | True | 10 | 10 | 9 | 1 | True |
| phase11 | outputs/phase11/strategy_validation_manifest.json | outputs\phase19\normalized_manifests\phase11.normalized_manifest.json | True | 10 | 10 | 8 | 2 | True |
| phase11_strategy_modules | outputs/phase11/strategy_module_registry_manifest.json | outputs\phase19\normalized_manifests\phase11_strategy_modules.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase12 | outputs/phase12/execution_manifest.json | outputs\phase19\normalized_manifests\phase12.normalized_manifest.json | True | 10 | 10 | 6 | 4 | True |
| phase12_event_backtest | outputs/phase12/event_backtest_manifest.json | outputs\phase19\normalized_manifests\phase12_event_backtest.normalized_manifest.json | True | 10 | 10 | 0 | 10 | True |
| phase13 | outputs/phase13/experiment_design_manifest.json | outputs\phase19\normalized_manifests\phase13.normalized_manifest.json | True | 10 | 10 | 9 | 1 | True |
| phase13_smoke_run | outputs/phase13/experiment_run_manifest.json | outputs\phase19\normalized_manifests\phase13_smoke_run.normalized_manifest.json | True | 10 | 10 | 9 | 1 | True |
| phase14 | outputs/phase14/quality_validation_manifest.json | outputs\phase19\normalized_manifests\phase14.normalized_manifest.json | True | 10 | 10 | 8 | 2 | True |
| phase15 | outputs/phase15/acceptance_gates_manifest.json | outputs\phase19\normalized_manifests\phase15.normalized_manifest.json | True | 10 | 10 | 8 | 2 | True |
| phase16 | outputs/phase16/metrics_reporting_manifest.json | outputs\phase19\normalized_manifests\phase16.normalized_manifest.json | True | 10 | 10 | 8 | 2 | True |
| phase17 | outputs/phase17/work_packages_manifest.json | outputs\phase19\normalized_manifests\phase17.normalized_manifest.json | True | 10 | 10 | 9 | 1 | True |
| phase18 | outputs/phase18/technology_stack_manifest.json | outputs\phase19\normalized_manifests\phase18.normalized_manifest.json | True | 10 | 10 | 9 | 1 | True |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | outputs\phase19\normalized_manifests\dashboard.normalized_manifest.json | True | 10 | 10 | 9 | 1 | True |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | outputs\phase19\normalized_manifests\duckdb.normalized_manifest.json | True | 10 | 10 | 9 | 1 | True |

## Highest Priority Remediation Rows

| artifact_id | manifest_path | required_field | current_coverage_status | matched_aliases | remediation_status | recommended_value_source | recommended_action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| phase1 | outputs/phase1/phase1_manifest.json | calibration_dataset_id | manifest_missing_or_unreadable |  | recover_or_rerun_manifest | manifest_missing_or_unreadable | Recover the manifest or rerun the generating phase with the normalized manifest schema. |
| phase1 | outputs/phase1/phase1_manifest.json | configuration_hash | manifest_missing_or_unreadable |  | recover_or_rerun_manifest | manifest_missing_or_unreadable | Recover the manifest or rerun the generating phase with the normalized manifest schema. |
| phase1 | outputs/phase1/phase1_manifest.json | cost_model_version | manifest_missing_or_unreadable |  | recover_or_rerun_manifest | manifest_missing_or_unreadable | Recover the manifest or rerun the generating phase with the normalized manifest schema. |
| phase1 | outputs/phase1/phase1_manifest.json | creation_timestamp | manifest_missing_or_unreadable |  | recover_or_rerun_manifest | manifest_missing_or_unreadable | Recover the manifest or rerun the generating phase with the normalized manifest schema. |
| phase1 | outputs/phase1/phase1_manifest.json | generator_version | manifest_missing_or_unreadable |  | recover_or_rerun_manifest | manifest_missing_or_unreadable | Recover the manifest or rerun the generating phase with the normalized manifest schema. |
| phase1 | outputs/phase1/phase1_manifest.json | latency_model_version | manifest_missing_or_unreadable |  | recover_or_rerun_manifest | manifest_missing_or_unreadable | Recover the manifest or rerun the generating phase with the normalized manifest schema. |
| phase1 | outputs/phase1/phase1_manifest.json | random_seed | manifest_missing_or_unreadable |  | recover_or_rerun_manifest | manifest_missing_or_unreadable | Recover the manifest or rerun the generating phase with the normalized manifest schema. |
| phase1 | outputs/phase1/phase1_manifest.json | regime_calendar_version | manifest_missing_or_unreadable |  | recover_or_rerun_manifest | manifest_missing_or_unreadable | Recover the manifest or rerun the generating phase with the normalized manifest schema. |
| phase1 | outputs/phase1/phase1_manifest.json | scenario_ids | manifest_missing_or_unreadable |  | recover_or_rerun_manifest | manifest_missing_or_unreadable | Recover the manifest or rerun the generating phase with the normalized manifest schema. |
| phase1 | outputs/phase1/phase1_manifest.json | ticker_metadata_version | manifest_missing_or_unreadable |  | recover_or_rerun_manifest | manifest_missing_or_unreadable | Recover the manifest or rerun the generating phase with the normalized manifest schema. |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | calibration_dataset_id | missing |  | add_field_in_generator | Record real-data source ID/date range or synthetic upstream artifact ID. | Record real-data calibration dataset identifier and date range. |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | configuration_hash | missing |  | add_field_in_generator | Hash the effective runtime configuration, inputs and materially relevant defaults. | Serialize effective config and store a stable hash per artifact. |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | cost_model_version | missing |  | add_field_in_generator | Record cost schedule artifact/version or explicit not_applicable_no_execution_costs. | Version execution/cost assumptions and cost schedule. |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | generator_version | missing |  | add_field_in_generator | Use git commit SHA or package version for the code that generated the artifact. | Add generator_version or code hash to every phase manifest. |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | latency_model_version | missing |  | add_field_in_generator | Record feed/execution latency model artifact/version or explicit not_applicable_no_latency_model. | Version feed latency/drop/duplication assumptions. |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | random_seed | missing |  | add_field_in_generator | Record integer seed, seed-plan artifact, or explicit not_applicable_deterministic. | Record seed or seed-plan reference for every stochastic artifact. |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | regime_calendar_version | missing |  | add_field_in_generator | Record scenario/regime calendar artifact and generator version. | Record scenario/regime calendar version for generated artifacts. |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | scenario_ids | missing |  | add_field_in_generator | Record scenario profile/day IDs or explicit not_applicable_observed_real_sample. | Record scenario IDs/profiles represented by each generated artifact. |
| dashboard | outputs/dashboard/validation_dashboard_manifest.json | ticker_metadata_version | missing |  | add_field_in_generator | Record ticker universe version and exchange metadata source/date. | Version ticker universe and metadata source. |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | calibration_dataset_id | missing |  | add_field_in_generator | Record real-data source ID/date range or synthetic upstream artifact ID. | Record real-data calibration dataset identifier and date range. |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | configuration_hash | missing |  | add_field_in_generator | Hash the effective runtime configuration, inputs and materially relevant defaults. | Serialize effective config and store a stable hash per artifact. |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | cost_model_version | missing |  | add_field_in_generator | Record cost schedule artifact/version or explicit not_applicable_no_execution_costs. | Version execution/cost assumptions and cost schedule. |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | generator_version | missing |  | add_field_in_generator | Use git commit SHA or package version for the code that generated the artifact. | Add generator_version or code hash to every phase manifest. |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | latency_model_version | missing |  | add_field_in_generator | Record feed/execution latency model artifact/version or explicit not_applicable_no_latency_model. | Version feed latency/drop/duplication assumptions. |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | random_seed | missing |  | add_field_in_generator | Record integer seed, seed-plan artifact, or explicit not_applicable_deterministic. | Record seed or seed-plan reference for every stochastic artifact. |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | regime_calendar_version | missing |  | add_field_in_generator | Record scenario/regime calendar artifact and generator version. | Record scenario/regime calendar version for generated artifacts. |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | scenario_ids | missing |  | add_field_in_generator | Record scenario profile/day IDs or explicit not_applicable_observed_real_sample. | Record scenario IDs/profiles represented by each generated artifact. |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | ticker_metadata_version | missing |  | add_field_in_generator | Record ticker universe version and exchange metadata source/date. | Version ticker universe and metadata source. |
| phase10 | outputs/phase10/storage_manifest.json | calibration_dataset_id | missing |  | add_field_in_generator | Record real-data source ID/date range or synthetic upstream artifact ID. | Record real-data calibration dataset identifier and date range. |
| phase10 | outputs/phase10/storage_manifest.json | configuration_hash | missing |  | add_field_in_generator | Hash the effective runtime configuration, inputs and materially relevant defaults. | Serialize effective config and store a stable hash per artifact. |
| phase10 | outputs/phase10/storage_manifest.json | cost_model_version | missing |  | add_field_in_generator | Record cost schedule artifact/version or explicit not_applicable_no_execution_costs. | Version execution/cost assumptions and cost schedule. |
| phase10 | outputs/phase10/storage_manifest.json | generator_version | missing |  | add_field_in_generator | Use git commit SHA or package version for the code that generated the artifact. | Add generator_version or code hash to every phase manifest. |
| phase10 | outputs/phase10/storage_manifest.json | latency_model_version | missing |  | add_field_in_generator | Record feed/execution latency model artifact/version or explicit not_applicable_no_latency_model. | Version feed latency/drop/duplication assumptions. |
| phase10 | outputs/phase10/storage_manifest.json | random_seed | missing |  | add_field_in_generator | Record integer seed, seed-plan artifact, or explicit not_applicable_deterministic. | Record seed or seed-plan reference for every stochastic artifact. |
| phase10 | outputs/phase10/storage_manifest.json | regime_calendar_version | missing |  | add_field_in_generator | Record scenario/regime calendar artifact and generator version. | Record scenario/regime calendar version for generated artifacts. |
| phase10 | outputs/phase10/storage_manifest.json | scenario_ids | missing |  | add_field_in_generator | Record scenario profile/day IDs or explicit not_applicable_observed_real_sample. | Record scenario IDs/profiles represented by each generated artifact. |
| phase10 | outputs/phase10/storage_manifest.json | ticker_metadata_version | missing |  | add_field_in_generator | Record ticker universe version and exchange metadata source/date. | Version ticker universe and metadata source. |
| phase11 | outputs/phase11/strategy_validation_manifest.json | configuration_hash | missing |  | add_field_in_generator | Hash the effective runtime configuration, inputs and materially relevant defaults. | Serialize effective config and store a stable hash per artifact. |
| phase11 | outputs/phase11/strategy_validation_manifest.json | cost_model_version | missing |  | add_field_in_generator | Record cost schedule artifact/version or explicit not_applicable_no_execution_costs. | Version execution/cost assumptions and cost schedule. |
| phase11 | outputs/phase11/strategy_validation_manifest.json | generator_version | missing |  | add_field_in_generator | Use git commit SHA or package version for the code that generated the artifact. | Add generator_version or code hash to every phase manifest. |
