# Phase148 Real L2 Download Refresh Workflow

Generated UTC: 2026-07-23T08:33:43.4739048Z

Phase148 is an operational wrapper for the AzCopy-first real L2 path.
It optionally runs the AzCopy download helper, always runs Phase147 local intake, conditionally runs Phase145 only when Phase147 says a required date is ready for import, and then runs Phase146.
Python remains local-only; Azure bulk I/O remains in AzCopy.

## Acceptance Summary

"metric","value","description"
"phase148_steps","4","Workflow steps attempted or skipped"
"phase148_failed_steps","0","Workflow steps failed"
"phase148_download_ran","0","1 means AzCopy helper was executed by this workflow"
"phase148_phase147_can_run_phase145_now","0","Phase147 intake readiness flag"
"phase148_phase145_ran","0","1 means Phase145 was run by this workflow"
"phase148_phase146_strategy_replay_allowed","0","Phase146 final replay gate"
"phase148_phase146_days_needed_for_min","2","Additional ready real-anchor days still needed"
"phase148_strategy_replay_allowed","0","Workflow never overrides Phase146"
"phase148_next_best_action","download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase148","Recommended next milestone"

## Step Ledger

"step_id","description","status","started_utc","ended_utc","elapsed_seconds","exit_code","command","error"
"P148_DOWNLOAD_SKIPPED","Skip AzCopy download and validate current local landing zone.","skipped","2026-07-23T08:33:41.7393140Z","2026-07-23T08:33:41.7393140Z","0","0","SkipDownload",""
"P148_PHASE147_INTAKE_AUDIT","Audit local AzCopy landing-zone completeness.","completed","2026-07-23T08:33:41.7593136Z","2026-07-23T08:33:42.6130056Z","0.854","0","python scripts\run_phase147_azcopy_download_intake_audit.py --scratch-root scratch_azcopy_selected\raw_l2 --target-root real_data_sample\l2_multiday_panel --required-dates 2026-07-10 2026-07-14",""
"P148_PHASE145_SKIPPED","Skip Phase145 because Phase147 says no required date is ready for import.","skipped","2026-07-23T08:33:42.6380048Z","2026-07-23T08:33:42.6380048Z","0","0","phase147_can_run_phase145_now=0",""
"P148_PHASE146_UNLOCK_AUDIT","Run final real-anchor minimum unlock audit.","completed","2026-07-23T08:33:42.6380048Z","2026-07-23T08:33:43.4509071Z","0.813","0","python scripts\run_phase146_real_anchor_minimum_unlock_audit.py",""
