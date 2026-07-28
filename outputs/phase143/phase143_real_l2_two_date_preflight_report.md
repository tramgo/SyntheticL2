# Phase143 Real L2 Two-Date Acquisition Preflight

Generated UTC: 2026-07-28T15:11:58.066750+00:00

Phase143 is an executable guard before the next Phase115 import/refresh.
It checks whether the configured next two real L2 dates are already ready in scratch or target, and emits the exact next command path.
It does not contact Azure and does not unlock strategy replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase143_current_ready_real_anchor_days | 5 | Ready real-anchor days from latest Phase115/110 |
| phase143_days_needed_for_min | 0 | Additional ready real days needed for minimum unlock before this preflight |
| phase143_required_date_rows | 2 | Required next-date rows checked |
| phase143_required_dates_satisfied | 2 | Required dates already ready in scratch or target |
| phase143_required_dates_target_ready | 2 | Required dates already ready in canonical target |
| phase143_required_dates_scratch_ready | 2 | Required dates ready in scratch for Phase115 import |
| phase143_all_required_dates_satisfied | 1 | 1 means configured required dates are locally ready in scratch or target |
| phase143_can_run_phase115_import_now | 0 | 1 means at least one required date is ready in scratch but not yet imported |
| phase143_strategy_replay_allowed | 0 | Preflight never unlocks strategy replay |
| phase143_next_best_action | download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase142_phase143 | Recommended next milestone |

## Required Date Status

| trade_date | scratch_ready_for_import | target_already_ready | scratch_parquet_files | target_parquet_files | scratch_bytes | target_bytes | required_date_satisfied | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-07-10 | True | True | 50509 | 50509 | 1765607327 | 1765607327 | True | already_imported |
| 2026-07-14 | True | True | 49732 | 49732 | 1750854292 | 1750854292 | True | already_imported |

## Next Command Plan

| step | action | runs_now | command | why |
| --- | --- | --- | --- | --- |
| 2 | verify_local_downloads | True | python scripts/run_phase142_local_real_l2_download_verifier.py --roots scratch_azcopy_selected/raw_l2 real_data_sample/l2_multiday_panel | Confirms local coverage/schema/readability before Phase115 import. |
| 3 | import_ready_scratch_dates | False | python scripts/run_phase115_real_panel_refresh_orchestrator.py --source-root scratch_azcopy_selected/raw_l2 --target-root real_data_sample/l2_multiday_panel --execute-import | No required date is locally ready in scratch but missing from target. |
| 4 | review_phase115_unlock_state | True | Import-Csv outputs/phase115/phase115_real_panel_refresh_acceptance_summary.csv | Replay remains closed unless Phase110/Phase115 explicitly prove the minimum real-anchor gate. |
