# Phase115 Real Panel Refresh Orchestrator

Generated UTC: 2026-07-19T22:54:44.178181+00:00

Phase115 runs the real-panel refresh chain in one command: discovery, import planning/copy, integrity, Phase96 readiness, Phase110 replay unlock, and final discovery.
By default it is dry-run safe and writes subrun outputs under outputs/phase115/subruns.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase115_steps | 6 | Refresh orchestration steps executed |
| phase115_failed_steps | 0 | Refresh orchestration steps failed |
| phase115_execute_import | 0 | 1 means Phase113 copied files into the drop-zone |
| phase115_phase111_additional_real_dates_found | 0 | Final Phase111 additional-date discovery flag |
| phase115_phase113_copied_files | 0 | Files copied by Phase113 |
| phase115_phase114_dry_run_integrity_ready | 1 | Dry-run integrity-ready flag |
| phase115_phase114_executed_import_integrity_pass | 0 | Executed import integrity pass flag |
| phase115_phase96_ready_anchor_days | 1 | Ready real anchor days after refresh |
| phase115_phase110_ready_real_anchor_days | 1 | Ready real anchor days in replay unlock gate |
| phase115_phase110_days_needed_for_min | 4 | Additional ready days needed for minimum unlock |
| phase115_replay_unlock_allowed | 0 | 1 means strategy replay may reopen |
| phase115_strategy_replay_allowed | 0 | Compatibility alias for replay unlock decision |
| phase115_recommend_next_action | collect_or_import_more_real_l2_days_then_run_phase115_with_execute_import | Recommended next milestone |

## Step Ledger

| step_id | description | status | started_utc | ended_utc | elapsed_seconds | error |
| --- | --- | --- | --- | --- | --- | --- |
| P115_PHASE111_INITIAL_DISCOVERY | Discover candidate real panels before import. | completed | 2026-07-19T22:53:22.401780+00:00 | 2026-07-19T22:53:45.509785+00:00 | 23.108 |  |
| P115_PHASE113_IMPORT_PLAN_OR_EXECUTE | Create or execute drop-zone import plan. | completed | 2026-07-19T22:53:45.509856+00:00 | 2026-07-19T22:53:46.895604+00:00 | 1.38575 |  |
| P115_PHASE114_IMPORT_INTEGRITY | Verify drop-zone import integrity or dry-run readiness. | completed | 2026-07-19T22:53:46.895655+00:00 | 2026-07-19T22:53:54.078550+00:00 | 7.1829 |  |
| P115_PHASE96_PANEL_READINESS | Rebuild real anchor panel readiness after import step. | completed | 2026-07-19T22:53:54.078613+00:00 | 2026-07-19T22:54:18.698488+00:00 | 24.6199 |  |
| P115_PHASE110_REPLAY_UNLOCK_GATE | Re-evaluate replay unlock gate after readiness refresh. | completed | 2026-07-19T22:54:18.698555+00:00 | 2026-07-19T22:54:18.796661+00:00 | 0.098106 |  |
| P115_PHASE111_FINAL_DISCOVERY | Refresh candidate discovery after import/readiness/gate run. | completed | 2026-07-19T22:54:18.796711+00:00 | 2026-07-19T22:54:44.143129+00:00 | 25.3464 |  |
