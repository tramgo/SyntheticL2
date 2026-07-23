# Phase146 Real-anchor Minimum Unlock Audit

Generated UTC: 2026-07-23T08:22:51.145258+00:00

Phase146 is a read-only audit gate. It reconciles Phase96, Phase110, Phase115, Phase143, and Phase145 evidence before strategy replay is allowed to proceed.
It does not contact Azure, does not import data, and does not infer readiness from partial downloads.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase146_hard_gate_rows | 6 | Hard unlock-audit gates evaluated |
| phase146_hard_gate_pass_rows | 4 | Hard unlock-audit gates passed |
| phase146_minimum_ready_real_days | 5 | Minimum ready real-anchor days required before replay unlock |
| phase146_phase115_ready_real_anchor_days | 3 | Ready real-anchor days reported by Phase115/110 |
| phase146_days_needed_for_min | 2 | Additional ready real-anchor days still needed |
| phase146_required_date_rows | 2 | Required download/import dates checked by Phase143 |
| phase146_required_dates_satisfied | 0 | Required dates ready in scratch or target |
| phase146_phase145_import_executed | 0 | Whether Phase145 ran Phase115 import on this pass |
| phase146_minimum_unlock_audit_pass | 0 | 1 means all hard audit gates passed |
| phase146_strategy_replay_allowed | 0 | 1 means downstream strategy replay can open under this audit |
| phase146_next_best_action | download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase145_phase146 | Recommended next milestone |

## Gate Evaluation

| gate | pass | observed | required | severity |
| --- | --- | --- | --- | --- |
| phase96_phase110_phase115_ready_day_consistency | True | phase96=3;phase110=3;phase115=3 | all_ready_day_counts_equal | hard |
| minimum_ready_real_anchor_days | False | 3 | 5 | hard |
| phase115_days_needed_arithmetic | True | 2 | 2 | hard |
| replay_unlock_flag_consistency | True | phase96=0;phase110=0;phase115=0 | all_unlock_flags_equal | hard |
| phase145_post_download_refresh_clean | True | 0 | 0 | hard |
| configured_required_dates_satisfied | False | 0/2 | all_required_dates_ready_in_scratch_or_target | diagnostic_until_minimum_days_pass |
| phase115_import_ran_after_download | False | 0 | 1 | diagnostic_until_required_dates_satisfied |
| phase146_strategy_replay_can_open | False | 0 | 1 | hard |

## Evidence Snapshot

| phase | source_path | source_exists | metric | value |
| --- | --- | --- | --- | --- |
| phase95 | outputs\phase95\real_anchor_panel_acceptance_summary.csv | True | phase95_ready_anchor_days |  |
| phase95 | outputs\phase95\real_anchor_panel_acceptance_summary.csv | True | phase95_strategy_replay_unlocked |  |
| phase96 | outputs\phase115\subruns\phase96\real_anchor_panel_builder_acceptance_summary.csv | True | phase96_ready_anchor_days | 3 |
| phase96 | outputs\phase115\subruns\phase96\real_anchor_panel_builder_acceptance_summary.csv | True | phase96_max_ready_dates_in_panel | 3 |
| phase96 | outputs\phase115\subruns\phase96\real_anchor_panel_builder_acceptance_summary.csv | True | phase96_strategy_replay_unlocked | 0 |
| phase110 | outputs\phase115\subruns\phase110\phase110_multiday_replay_unlock_acceptance_summary.csv | True | phase110_ready_real_anchor_days | 3 |
| phase110 | outputs\phase115\subruns\phase110\phase110_multiday_replay_unlock_acceptance_summary.csv | True | phase110_required_ready_real_days_min | 5 |
| phase110 | outputs\phase115\subruns\phase110\phase110_multiday_replay_unlock_acceptance_summary.csv | True | phase110_days_needed_for_min | 2 |
| phase110 | outputs\phase115\subruns\phase110\phase110_multiday_replay_unlock_acceptance_summary.csv | True | phase110_replay_unlock_allowed | 0 |
| phase115 | outputs\phase115\phase115_real_panel_refresh_acceptance_summary.csv | True | phase115_phase96_ready_anchor_days | 3 |
| phase115 | outputs\phase115\phase115_real_panel_refresh_acceptance_summary.csv | True | phase115_phase110_ready_real_anchor_days | 3 |
| phase115 | outputs\phase115\phase115_real_panel_refresh_acceptance_summary.csv | True | phase115_phase110_days_needed_for_min | 2 |
| phase115 | outputs\phase115\phase115_real_panel_refresh_acceptance_summary.csv | True | phase115_replay_unlock_allowed | 0 |
| phase142 | outputs\phase142\phase142_local_real_l2_download_verifier_acceptance_summary.csv | True | phase142_ready_date_rows | 5 |
| phase142 | outputs\phase142\phase142_local_real_l2_download_verifier_acceptance_summary.csv | True | phase142_canonical_symbol_partition_rows | 96 |
| phase142 | outputs\phase142\phase142_local_real_l2_download_verifier_acceptance_summary.csv | True | phase142_nested_trade_date_symbol_partition_rows | 64 |
| phase143 | outputs\phase143\phase143_real_l2_two_date_preflight_acceptance_summary.csv | True | phase143_required_date_rows | 2 |
| phase143 | outputs\phase143\phase143_real_l2_two_date_preflight_acceptance_summary.csv | True | phase143_required_dates_satisfied | 0 |
| phase143 | outputs\phase143\phase143_real_l2_two_date_preflight_acceptance_summary.csv | True | phase143_can_run_phase115_import_now | 0 |
| phase145 | outputs\phase145\phase145_real_l2_post_download_refresh_acceptance_summary.csv | True | phase145_failed_steps | 0 |
| phase145 | outputs\phase145\phase145_real_l2_post_download_refresh_acceptance_summary.csv | True | phase145_phase115_import_executed | 0 |
| phase145 | outputs\phase145\phase145_real_l2_post_download_refresh_acceptance_summary.csv | True | phase145_ready_real_anchor_days | 3 |
| phase145 | outputs\phase145\phase145_real_l2_post_download_refresh_acceptance_summary.csv | True | phase145_days_needed_for_min | 2 |
| phase96 | outputs\phase115\subruns\phase96\real_anchor_panel_manifest.csv | True | phase96_manifest_exists | 1 |
