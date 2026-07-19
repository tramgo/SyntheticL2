# Phase110 Multiday Replay Unlock Gate

Generated UTC: 2026-07-19T22:45:23.599152+00:00

Phase110 consolidates the clean one-day Phase109 realism result with the real multiday panel requirement.
It deliberately keeps strategy replay closed unless all unlock gates pass.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase110_gate_rows | 5 | Replay unlock gates evaluated |
| phase110_gate_pass_rows | 2 | Replay unlock gates passing |
| phase110_one_day_realism_gate_pass | 1 | 1 means Phase109 one-day full-symbol realism passed |
| phase110_ready_real_anchor_days | 1 | Ready real anchor days currently available |
| phase110_required_ready_real_days_min | 5 | Minimum ready real days required |
| phase110_target_ready_real_days | 10 | Preferred ready real days target |
| phase110_days_needed_for_min | 4 | Additional ready days required for minimum multiday unlock |
| phase110_replay_unlock_allowed | 0 | 1 means strategy replay may reopen |
| phase110_strategy_replay_allowed | 0 | Compatibility alias for replay unlock decision |
| phase110_recommend_next_action | collect_4_more_ready_real_websocket_l2_days_then_rerun_phase96_and_multiday_realism | Recommended next milestone |

## Replay Unlock Gates

| gate_id | gate_pass | evidence | next_action_if_fail |
| --- | --- | --- | --- |
| P110_ONE_DAY_FULL_SYMBOL_REALISM_PASS | True | phase109_full_symbol_calibrated_realism_pass=1; phase109_calibration_gap_rows=0 | rerun_symbol_aware_generator_calibration |
| P110_PHASE109_REPLAY_LOCK_PRESERVED | True | phase109_strategy_replay_allowed=0 | restore_strategy_replay_lock |
| P110_MIN_MULTIDAY_REAL_PANEL_AVAILABLE | False | phase96_ready_anchor_days=1; required_min=5 | collect_more_real_websocket_l2_days |
| P110_PHASE96_PANEL_READY_FOR_RERUN | False | phase96_panels_ready_for_phase94_rerun=0 | rerun_phase96_after_multiday_real_panel_ingest |
| P110_PHASE96_STRATEGY_UNLOCK | False | phase96_strategy_replay_unlocked=0 | keep_strategy_replay_closed_until_multiday_realism_passes |

## Acquisition Queue

| priority | work_item | current_ready_days | required_ready_days | target_ready_days | days_needed_for_min | days_needed_for_target | observed_ready_dates | acceptance_gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | collect_minimum_multiday_real_anchor_panel | 1 | 5 | 10 | 4 | 9 | 2026-07-13 | Phase96 ready_anchor_days >= 5 and panels_ready_for_phase94_rerun >= 1. |
| 2 | rerun_phase109_style_calibrated_realism_on_multiday_panel | 1 | 5 | 10 | 4 | 9 | 2026-07-13 | 0 severe metric gaps and acceptable total gap fraction on the multiday panel. |
| 3 | only_then_consider_strategy_replay | 1 | 5 | 10 | 4 | 9 | 2026-07-13 | Phase110 replay_unlock_allowed=1. |
