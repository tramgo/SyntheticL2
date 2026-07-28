# Phase115 Real Panel Refresh Orchestrator

Generated UTC: 2026-07-28T15:11:10.847374+00:00

Phase115 runs the real-panel refresh chain in one command: discovery, import planning/copy, integrity, Phase96 readiness, Phase110 replay unlock, and final discovery.
By default it is dry-run safe and writes subrun outputs under outputs/phase115/subruns.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase115_steps | 6 | Refresh orchestration steps executed |
| phase115_failed_steps | 0 | Refresh orchestration steps failed |
| phase115_execute_import | 1 | 1 means Phase113 copied files into the drop-zone |
| phase115_phase111_additional_real_dates_found | 0 | Final Phase111 additional-date discovery flag |
| phase115_phase113_copied_files | 100241 | Files copied by Phase113 |
| phase115_phase114_dry_run_integrity_ready | 0 | Dry-run integrity-ready flag |
| phase115_phase114_executed_import_integrity_pass | 1 | Executed import integrity pass flag |
| phase115_phase96_ready_anchor_days | 5 | Ready real anchor days after refresh |
| phase115_phase110_ready_real_anchor_days | 5 | Ready real anchor days in replay unlock gate |
| phase115_phase110_days_needed_for_min | 0 | Additional ready days needed for minimum unlock |
| phase115_replay_unlock_allowed | 0 | 1 means strategy replay may reopen |
| phase115_strategy_replay_allowed | 0 | Compatibility alias for replay unlock decision |
| phase115_recommend_next_action | collect_or_import_more_real_l2_days_then_run_phase115_with_execute_import | Recommended next milestone |

## Step Ledger

| step_id | description | status | started_utc | ended_utc | elapsed_seconds | error |
| --- | --- | --- | --- | --- | --- | --- |
| P115_PHASE111_INITIAL_DISCOVERY | Discover candidate real panels before import. | completed | 2026-07-28T15:04:10.242844+00:00 | 2026-07-28T15:04:10.349460+00:00 | 0.106616 |  |
| P115_PHASE113_IMPORT_PLAN_OR_EXECUTE | Create or execute drop-zone import plan. | completed | 2026-07-28T15:04:10.349552+00:00 | 2026-07-28T15:08:37.035393+00:00 | 266.686 |  |
| P115_PHASE114_IMPORT_INTEGRITY | Verify drop-zone import integrity or dry-run readiness. | completed | 2026-07-28T15:08:37.035441+00:00 | 2026-07-28T15:09:31.788997+00:00 | 54.7536 |  |
| P115_PHASE96_PANEL_READINESS | Rebuild real anchor panel readiness after import step. | completed | 2026-07-28T15:09:31.789041+00:00 | 2026-07-28T15:11:10.671986+00:00 | 98.8829 |  |
| P115_PHASE110_REPLAY_UNLOCK_GATE | Re-evaluate replay unlock gate after readiness refresh. | completed | 2026-07-28T15:11:10.672037+00:00 | 2026-07-28T15:11:10.755595+00:00 | 0.083558 |  |
| P115_PHASE111_FINAL_DISCOVERY | Refresh candidate discovery after import/readiness/gate run. | completed | 2026-07-28T15:11:10.755627+00:00 | 2026-07-28T15:11:10.826408+00:00 | 0.070781 |  |
