# Phase174 Secure Real L2 Download Orchestrator

Generated UTC: 2026-07-28T14:58:15.4428849Z

Phase174 loads Azure credential variable names from .env or the process environment without printing or persisting secret values.
If a SAS or account key is available, it runs Phase148 download/import refresh and then reruns Phase172.
If no credential is available, it records a no-secret skipped-download ledger.

## Acceptance Summary

"metric","value","description"
"phase174_required_dates","2026-07-10,2026-07-14","Dates this secure orchestrator is configured to acquire"
"phase174_env_path_checked",".env","Environment file checked for Azure credential names"
"phase174_azure_credential_names_loaded","","Loaded Azure credential variable names only; secret values are not recorded"
"phase174_sas_available","1","1 means SAS is present in process environment"
"phase174_account_key_available","0","1 means account key is present in process environment"
"phase174_download_ran","1","1 means Phase148 was invoked with download enabled"
"phase174_phase172_reran","1","1 means Phase172 was rerun after download/import"
"phase174_failed_steps","0","Workflow steps failed"
"phase174_phase173_download_ready_now","1","Phase173 download readiness after .env load"
"phase174_phase172_additional_dates_needed","2","Additional complete local real L2 dates still needed"
"phase174_strategy_replay_allowed","0","Secure download orchestration does not unlock strategy replay"
"phase174_paper_or_live_acceptance_allowed","0","Paper/live remains closed"
"phase174_next_best_action","inspect_phase148_phase172_outputs_then_download_remaining_dates_if_needed","Recommended next milestone"

## Step Ledger

"step_id","description","status","started_utc","ended_utc","elapsed_seconds","exit_code","command","error"
"P174_LOAD_ENV","Load Azure download credentials from .env into process environment if present; do not print or persist secret values.","completed","2026-07-28T14:16:29.4950843Z","2026-07-28T14:16:29.4960837Z","0.001","0","Import-DotEnvAzureCredentials .env",""
"P174_PHASE173_PREFLIGHT","Refresh no-secret credential/download preflight after loading .env.","completed","2026-07-28T14:16:29.5217887Z","2026-07-28T14:16:30.9819095Z","1.46","0","python scripts\run_phase173_real_l2_download_credential_preflight.py --dates 2026-07-10,2026-07-14 --storage-account stctrade1ramic --share-name ctrade1-l2-data --azure-cli-probe-status not_reprobed_by_phase174 --azure-cli-probe-evidence phase174_uses_env_credential_path_first_to_avoid_secret_leakage",""
"P174_PHASE148_DOWNLOAD_REFRESH","Run Phase148 with download enabled using inherited environment credentials.","completed","2026-07-28T14:16:30.9843648Z","2026-07-28T14:55:35.2320318Z","2344.248","0","powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_phase148_real_l2_download_refresh_workflow.ps1 -Dates 2026-07-10,2026-07-14 -StorageAccount stctrade1ramic -ShareName ctrade1-l2-data -RemoteRoot raw_l2 -ScratchRoot scratch_azcopy_selected\raw_l2 -TargetRoot real_data_sample\l2_multiday_panel -Python python",""
"P174_PHASE172_RERUN","Rerun Phase172 after download/import refresh.","completed","2026-07-28T14:55:35.2579432Z","2026-07-28T14:58:14.8351351Z","159.577","0","python scripts\run_phase172_real_l2_receive_flow_availability_audit.py",""
