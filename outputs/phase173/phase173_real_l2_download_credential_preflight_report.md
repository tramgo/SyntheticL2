# Phase173 Real L2 Download Credential Preflight

Generated UTC: 2026-07-23T18:52:12.430376+00:00

Phase173 records whether the next two-date real L2 download can be executed now.
It never records SAS signatures, account keys, passwords, or broker credentials.
It does not contact Azure, run AzCopy, import data, unlock replay, or run strategy P&L.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase173_required_date_rows | 2 | Dates required for next acquisition attempt |
| phase173_azcopy_available | 1 | AzCopy availability |
| phase173_download_credential_available | 0 | SAS or account key available in environment |
| phase173_azure_cli_usable_for_sas | 0 | Azure CLI can be used to generate or locate download credentials |
| phase173_download_ready_now | 0 | 1 means Phase148 can run download immediately |
| phase173_additional_dates_needed | 2 | Additional complete local real L2 dates still needed |
| phase173_strategy_replay_allowed | 0 | Credential preflight never opens replay |
| phase173_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase173_next_best_action | provide_share_sas_or_storage_key_or_repair_azure_cli_tls_then_run_phase148_download | Recommended next milestone |

## Preflight Evidence

| metric | value | description |
| --- | --- | --- |
| phase173_storage_account | stctrade1ramic | Configured Azure Files storage account |
| phase173_share_name | ctrade1-l2-data | Configured Azure Files share |
| phase173_required_dates | 2026-07-10,2026-07-14 | Real L2 dates needed to satisfy Phase172 minimum |
| phase173_azcopy_path | C:\Users\Ramic\AppData\Local\Temp\azcopy_windows_amd64_20260723123603\azcopy_windows_amd64_10.32.4\azcopy.exe | Resolved AzCopy executable path, if present |
| phase173_azcopy_available | 1 | 1 means AzCopy can be launched |
| phase173_sas_token_available_in_env | 0 | 1 means AZURE_STORAGE_SAS_TOKEN is set; value is never recorded |
| phase173_account_key_available_in_env | 0 | 1 means AZURE_STORAGE_KEY is set; value is never recorded |
| phase173_azure_cli_probe_status | not_reprobed_by_phase174 | Current Azure CLI metadata/auth probe result |
| phase173_azure_cli_probe_evidence | phase174_uses_env_credential_path_first_to_avoid_secret_leakage | Redacted CLI evidence captured outside secret values |
| phase173_phase172_ready_receive_flow_dates | 3 | Ready local receive-flow dates from Phase172 |
| phase173_phase172_additional_dates_needed | 2 | Additional complete local real L2 dates needed |
| phase173_phase148_download_ran | 0 | Latest Phase148 download flag |
| phase173_phase147_required_dates_satisfied | 0 | Latest local intake satisfied date count |
| phase173_phase146_days_needed_for_min | 2 | Latest real-anchor gate days still needed |
| phase173_phase146_strategy_replay_allowed | 0 | Latest real-anchor replay gate |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P173_AZCOPY_AVAILABLE | 1 | azcopy resolved | hard_for_download |
| P173_DOWNLOAD_CREDENTIAL_AVAILABLE | 0 | sas_env=0;account_key_env=0 | hard_for_download |
| P173_AZURE_CLI_USABLE_FOR_SAS | 0 | phase174_uses_env_credential_path_first_to_avoid_secret_leakage | alternative_path |
| P173_TWO_DATES_STILL_REQUIRED | 1 | phase172_needed=2;phase146_needed=2 | status |
| P173_REPLAY_REMAINS_CLOSED | 1 | phase146_strategy_replay_allowed=0 | safety |
