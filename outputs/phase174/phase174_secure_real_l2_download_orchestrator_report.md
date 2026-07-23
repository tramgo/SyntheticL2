# Phase174 Secure Real L2 Download Orchestrator

Generated UTC: 2026-07-23T18:52:12.7273576Z

Phase174 loads Azure credential variable names from .env or the process environment without printing or persisting secret values.
If a SAS or account key is available, it runs Phase148 download/import refresh and then reruns Phase172.
If no credential is available, it records a no-secret skipped-download ledger.

## Acceptance Summary

"metric","value","description"
"phase174_required_dates","2026-07-10,2026-07-14","Dates this secure orchestrator is configured to acquire"
"phase174_env_path_checked",".env","Environment file checked for Azure credential names"
"phase174_azure_credential_names_loaded","","Loaded Azure credential variable names only; secret values are not recorded"
"phase174_sas_available","0","1 means SAS is present in process environment"
"phase174_account_key_available","0","1 means account key is present in process environment"
"phase174_download_ran","0","1 means Phase148 was invoked with download enabled"
"phase174_phase172_reran","0","1 means Phase172 was rerun after download/import"
"phase174_failed_steps","0","Workflow steps failed"
"phase174_phase173_download_ready_now","0","Phase173 download readiness after .env load"
"phase174_phase172_additional_dates_needed","2","Additional complete local real L2 dates still needed"
"phase174_strategy_replay_allowed","0","Secure download orchestration does not unlock strategy replay"
"phase174_paper_or_live_acceptance_allowed","0","Paper/live remains closed"
"phase174_next_best_action","add_AZURE_STORAGE_SAS_TOKEN_or_AZURE_STORAGE_KEY_to_env_or_process_then_rerun_phase174","Recommended next milestone"

## Step Ledger

"step_id","description","status","started_utc","ended_utc","elapsed_seconds","exit_code","command","error"
"P174_LOAD_ENV","Load Azure download credentials from .env into process environment if present; do not print or persist secret values.","completed","2026-07-23T18:52:11.2069807Z","2026-07-23T18:52:11.2099766Z","0.003","0","Import-DotEnvAzureCredentials .env",""
"P174_PHASE173_PREFLIGHT","Refresh no-secret credential/download preflight after loading .env.","completed","2026-07-23T18:52:11.2608646Z","2026-07-23T18:52:12.6239809Z","1.363","0","python scripts\run_phase173_real_l2_download_credential_preflight.py --dates 2026-07-10 2026-07-14 --storage-account stctrade1ramic --share-name ctrade1-l2-data --azure-cli-probe-status not_reprobed_by_phase174 --azure-cli-probe-evidence phase174_uses_env_credential_path_first_to_avoid_secret_leakage",""
"P174_DOWNLOAD_SKIPPED_NO_CREDENTIAL","Skip Phase148 download because neither SAS nor account key is available in .env or process environment.","skipped","2026-07-23T18:52:12.6339830Z","2026-07-23T18:52:12.6339830Z","0","0","credential_available=0",""
