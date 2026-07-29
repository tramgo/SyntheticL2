# Phase239 Unseen-date Acquisition / Materialization Audit Report

Generated UTC: 2026-07-29T07:18:28.199468+00:00

Phase239 audits whether the Phase238 unseen-date validation requirement can be executed now.
It does not validate the strategy, tune thresholds, print secrets, or unlock paper/live trading.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase239_unseen_date_acquisition_audit_complete | 1 | Phase239 acquisition/materialization audit completed |
| phase239_local_unseen_candidate_dates | 0 | Local dates not in Phase237 discovery sample |
| phase239_min_unseen_validation_dates_required | 5 | Minimum unseen dates required by Phase238 |
| phase239_target_unseen_date_rows | 5 | Target unseen date rows planned |
| phase239_az_cli_available | 1 | Azure CLI availability |
| phase239_azcopy_available | 0 | AzCopy availability |
| phase239_azure_storage_listing_ready | 1 | Whether Azure storage listing is readable now |
| phase239_download_plan_rows | 7 | Download/materialization plan rows |
| phase239_hard_gate_pass_rows | 3 | Hard Phase239 gates passed |
| phase239_hard_gate_rows | 4 | Hard Phase239 gates evaluated |
| phase239_validation_execution_allowed_now | 0 | Phase239 does not execute validation |
| phase239_strategy_promotion_allowed | 0 | No strategy promotion from Phase239 |
| phase239_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase239 |
| phase239_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase239 |
| phase239_next_best_action | run_phase240_execute_unseen_real_l2_download_and_materialization_no_paper_live | Recommended next milestone |

## Local Real L2 Inventory

| root | data_kind | trade_date | is_phase237_discovery_date | is_unseen_candidate_date |
| --- | --- | --- | --- | --- |
| real_data_sample\l2_multiday_panel | raw_l2_parquet | 2026-07-08 | True | False |
| real_data_sample\l2_multiday_panel | raw_l2_parquet | 2026-07-09 | True | False |
| real_data_sample\l2_multiday_panel | raw_l2_parquet | 2026-07-10 | True | False |
| real_data_sample\l2_multiday_panel | raw_l2_parquet | 2026-07-13 | True | False |
| real_data_sample\l2_multiday_panel | raw_l2_parquet | 2026-07-14 | True | False |
| real_data_sample\l2_multiday_panel | raw_l2_parquet | 2026-07-15 | True | False |
| real_data_sample\l2_multiday_panel | raw_l2_parquet | 2026-07-16 | True | False |
| scratch_azcopy_selected\raw_l2 | raw_l2_parquet | 2026-07-08 | True | False |
| scratch_azcopy_selected\raw_l2 | raw_l2_parquet | 2026-07-09 | True | False |
| scratch_azcopy_selected\raw_l2 | raw_l2_parquet | 2026-07-10 | True | False |
| scratch_azcopy_selected\raw_l2 | raw_l2_parquet | 2026-07-14 | True | False |
| derived_real_l2_receive_flow_features_phase176 | derived_receive_flow_features | 2026-07-08 | True | False |
| derived_real_l2_receive_flow_features_phase176 | derived_receive_flow_features | 2026-07-09 | True | False |
| derived_real_l2_receive_flow_features_phase176 | derived_receive_flow_features | 2026-07-10 | True | False |
| derived_real_l2_receive_flow_features_phase176 | derived_receive_flow_features | 2026-07-13 | True | False |
| derived_real_l2_receive_flow_features_phase176 | derived_receive_flow_features | 2026-07-14 | True | False |
| derived_real_l2_receive_flow_features_phase176 | derived_receive_flow_features | 2026-07-15 | True | False |
| derived_real_l2_receive_flow_features_phase176 | derived_receive_flow_features | 2026-07-16 | True | False |

## Azure Access Preflight

| check_id | passed | observed_value | required_value | interpretation |
| --- | --- | --- | --- | --- |
| P239_AZ_CLI_AVAILABLE | True | C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin\az.CMD | az on PATH or SDK credential alternative | Azure CLI is available for a possible download path. |
| P239_AZCOPY_AVAILABLE | False |  | azcopy optional | AzCopy is not on PATH; use Azure CLI or Python SDK download path. |
| P239_CURRENT_PROCESS_STORAGE_SECRET_AVAILABLE | True | present | fresh SAS/connection string or working az login | A current-process storage secret exists. |
| P239_AZ_LOGIN_STORAGE_LIST_READABLE | False | FileNotFoundError(2, 'The system cannot find the file specified', None, 2, None) | readable storage container listing | Azure CLI storage listing failed before data download. |
| P239_FILE_SERVICE_SAS_SHARE_READABLE | True | ctrade1-l2-data | ctrade1-l2-data | SAS can read the Azure Files L2 share. |
| P239_FILE_SERVICE_RAW_L2_DATES_READABLE | True | 1970-01-01;2026-07-08;2026-07-09;2026-07-10;2026-07-13;2026-07-14;2026-07-15;2026-07-16;2026-07-17;2026-07-20;2026-07-21;2026-07-22;2026-07-23;2026-07-24;2026-07-27;2026-07-28;2026-07-29 | raw_l2/trade_date=* | SAS can list raw_l2 trade-date directories. |
| P239_FILE_SERVICE_TARGET_UNSEEN_DATES_AVAILABLE | True | 2026-07-17;2026-07-20;2026-07-21;2026-07-22;2026-07-23 | 2026-07-17;2026-07-20;2026-07-21;2026-07-22;2026-07-23 | All target unseen dates are visible in Azure Files raw_l2. |

## Target Unseen Dates

| target_trade_date | already_materialized_locally | required_for_phase238_primary_validation | expected_source_prefix | target_raw_root | target_feature_root | holiday_calendar_check_required |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-07-17 | False | True | raw_l2/trade_date=2026-07-17/exchange=NSE/ | real_data_sample/l2_unseen_validation/trade_date=2026-07-17/exchange=NSE/ | derived_real_l2_receive_flow_features_phase239/trade_date=2026-07-17/exchange=NSE/ | True |
| 2026-07-20 | False | True | raw_l2/trade_date=2026-07-20/exchange=NSE/ | real_data_sample/l2_unseen_validation/trade_date=2026-07-20/exchange=NSE/ | derived_real_l2_receive_flow_features_phase239/trade_date=2026-07-20/exchange=NSE/ | True |
| 2026-07-21 | False | True | raw_l2/trade_date=2026-07-21/exchange=NSE/ | real_data_sample/l2_unseen_validation/trade_date=2026-07-21/exchange=NSE/ | derived_real_l2_receive_flow_features_phase239/trade_date=2026-07-21/exchange=NSE/ | True |
| 2026-07-22 | False | True | raw_l2/trade_date=2026-07-22/exchange=NSE/ | real_data_sample/l2_unseen_validation/trade_date=2026-07-22/exchange=NSE/ | derived_real_l2_receive_flow_features_phase239/trade_date=2026-07-22/exchange=NSE/ | True |
| 2026-07-23 | False | True | raw_l2/trade_date=2026-07-23/exchange=NSE/ | real_data_sample/l2_unseen_validation/trade_date=2026-07-23/exchange=NSE/ | derived_real_l2_receive_flow_features_phase239/trade_date=2026-07-23/exchange=NSE/ | True |

## Download and Materialization Plan

| step_order | download_task | trade_date | preferred_method | ready_to_execute_now | source | destination | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | download_raw_l2_date | 2026-07-17 | azure_files_python_sdk | 1 | stctrade1ramic/ctrade1-l2-data:raw_l2/trade_date=2026-07-17/exchange=NSE/ | real_data_sample/l2_unseen_validation/trade_date=2026-07-17/exchange=NSE/ | Execute only with fresh SAS/working az login and TLS trust fixed; do not print secrets. |
| 2 | download_raw_l2_date | 2026-07-20 | azure_files_python_sdk | 1 | stctrade1ramic/ctrade1-l2-data:raw_l2/trade_date=2026-07-20/exchange=NSE/ | real_data_sample/l2_unseen_validation/trade_date=2026-07-20/exchange=NSE/ | Execute only with fresh SAS/working az login and TLS trust fixed; do not print secrets. |
| 3 | download_raw_l2_date | 2026-07-21 | azure_files_python_sdk | 1 | stctrade1ramic/ctrade1-l2-data:raw_l2/trade_date=2026-07-21/exchange=NSE/ | real_data_sample/l2_unseen_validation/trade_date=2026-07-21/exchange=NSE/ | Execute only with fresh SAS/working az login and TLS trust fixed; do not print secrets. |
| 4 | download_raw_l2_date | 2026-07-22 | azure_files_python_sdk | 1 | stctrade1ramic/ctrade1-l2-data:raw_l2/trade_date=2026-07-22/exchange=NSE/ | real_data_sample/l2_unseen_validation/trade_date=2026-07-22/exchange=NSE/ | Execute only with fresh SAS/working az login and TLS trust fixed; do not print secrets. |
| 5 | download_raw_l2_date | 2026-07-23 | azure_files_python_sdk | 1 | stctrade1ramic/ctrade1-l2-data:raw_l2/trade_date=2026-07-23/exchange=NSE/ | real_data_sample/l2_unseen_validation/trade_date=2026-07-23/exchange=NSE/ | Execute only with fresh SAS/working az login and TLS trust fixed; do not print secrets. |
| 6 | materialize_phase235_adapter_features | 2026-07-17;2026-07-20;2026-07-21;2026-07-22;2026-07-23 | reuse_phase176_materializer_contract | 0 | real_data_sample/l2_unseen_validation/ | derived_real_l2_receive_flow_features_phase239/ | Run after raw unseen dates are downloaded and schema/date/symbol coverage is verified. |
| 7 | run_frozen_phase237_validation | 2026-07-17;2026-07-20;2026-07-21;2026-07-22;2026-07-23 | phase240_or_phase239_validation_runner | 0 | derived_real_l2_receive_flow_features_phase239/ | outputs/phase240/ | Apply frozen Phase238 candidate only; no threshold tuning on unseen validation dates. |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P239_LOCAL_UNSEEN_DATES_AVAILABLE | False | 0 | >=5 | hard |
| P239_AZURE_DOWNLOAD_READY_NOW | True | 1 | 1 | soft |
| P239_TARGET_UNSEEN_DATE_PLAN_WRITTEN | True | 5 | 5 | hard |
| P239_DOWNLOAD_AND_MATERIALIZATION_PLAN_WRITTEN | True | 7 | >0 rows | hard |
| P239_NO_VALIDATION_OR_PROMOTION_UNLOCK | True | 0 | 0 | hard |
