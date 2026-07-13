# Phase 19 Reproducibility Report

Generated UTC: 2026-07-13T19:15:17.336758+00:00

## Scope

This phase audits whether current manifests contain the metadata needed for exact regeneration.
It treats aliases and inferred references as useful but not as strong as exact versioned fields.

## Coverage Status Summary

| coverage_status | field_checks |
| --- | --- |
| manifest_missing_or_unreadable | 10 |
| missing | 168 |
| present_alias_or_inferred | 32 |

## Artifact Summary

| artifact_id | manifest_path | required_fields | present_exact | present_alias_or_inferred | missing_fields | manifest_missing_or_unreadable_fields | exact_regeneration_ready |
| --- | --- | --- | --- | --- | --- | --- | --- |
| duckdb | outputs/duckdb/duckdb_workspace_manifest.json | 10 | 0 | 1 | 9 | 0 | False |
| phase1 | outputs/phase1/phase1_manifest.json | 10 | 0 | 0 | 0 | 10 | False |
| phase10 | outputs/phase10/storage_manifest.json | 10 | 0 | 1 | 9 | 0 | False |
| phase11 | outputs/phase11/strategy_validation_manifest.json | 10 | 0 | 2 | 8 | 0 | False |
| phase12 | outputs/phase12/execution_manifest.json | 10 | 0 | 4 | 6 | 0 | False |
| phase13 | outputs/phase13/experiment_design_manifest.json | 10 | 0 | 1 | 9 | 0 | False |
| phase13_smoke_run | outputs/phase13/experiment_run_manifest.json | 10 | 0 | 1 | 9 | 0 | False |
| phase14 | outputs/phase14/quality_validation_manifest.json | 10 | 0 | 2 | 8 | 0 | False |
| phase15 | outputs/phase15/acceptance_gates_manifest.json | 10 | 0 | 2 | 8 | 0 | False |
| phase16 | outputs/phase16/metrics_reporting_manifest.json | 10 | 0 | 1 | 9 | 0 | False |
| phase17 | outputs/phase17/work_packages_manifest.json | 10 | 0 | 1 | 9 | 0 | False |
| phase18 | outputs/phase18/technology_stack_manifest.json | 10 | 0 | 1 | 9 | 0 | False |
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
| calibration_dataset_id | missing | 18 | duckdb;phase10;phase13;phase13_smoke_run;phase14;phase15;phase16;phase17;phase18;phase2;phase3;phase4;phase5;phase6;phase7;phase8;phase9;stage_a1 | Record real-data calibration dataset identifier and date range. |
| configuration_hash | missing | 20 | duckdb;phase10;phase11;phase12;phase13;phase13_smoke_run;phase14;phase15;phase16;phase17;phase18;phase2;phase3;phase4;phase5;phase6;phase7;phase8;phase9;stage_a1 | Serialize effective config and store a stable hash per artifact. |
| cost_model_version | missing | 18 | duckdb;phase10;phase11;phase13;phase13_smoke_run;phase14;phase16;phase17;phase18;phase2;phase3;phase4;phase5;phase6;phase7;phase8;phase9;stage_a1 | Version execution/cost assumptions and cost schedule. |
| creation_timestamp | missing | 1 | stage_a1 | Store generated_utc or creation_timestamp in every manifest. |
| generator_version | missing | 20 | duckdb;phase10;phase11;phase12;phase13;phase13_smoke_run;phase14;phase15;phase16;phase17;phase18;phase2;phase3;phase4;phase5;phase6;phase7;phase8;phase9;stage_a1 | Add generator_version or code hash to every phase manifest. |
| latency_model_version | missing | 19 | duckdb;phase10;phase11;phase13;phase13_smoke_run;phase14;phase15;phase16;phase17;phase18;phase2;phase3;phase4;phase5;phase6;phase7;phase8;phase9;stage_a1 | Version feed latency/drop/duplication assumptions. |
| random_seed | missing | 20 | duckdb;phase10;phase11;phase12;phase13;phase13_smoke_run;phase14;phase15;phase16;phase17;phase18;phase2;phase3;phase4;phase5;phase6;phase7;phase8;phase9;stage_a1 | Record seed or seed-plan reference for every stochastic artifact. |
| regime_calendar_version | missing | 19 | duckdb;phase10;phase11;phase12;phase13;phase13_smoke_run;phase15;phase16;phase17;phase18;phase2;phase3;phase4;phase5;phase6;phase7;phase8;phase9;stage_a1 | Record scenario/regime calendar version for generated artifacts. |
| scenario_ids | missing | 20 | duckdb;phase10;phase11;phase12;phase13;phase13_smoke_run;phase14;phase15;phase16;phase17;phase18;phase2;phase3;phase4;phase5;phase6;phase7;phase8;phase9;stage_a1 | Record scenario IDs/profiles represented by each generated artifact. |
| ticker_metadata_version | missing | 13 | duckdb;phase10;phase11;phase12;phase13;phase13_smoke_run;phase14;phase15;phase16;phase17;phase18;phase9;stage_a1 | Version ticker universe and metadata source. |
