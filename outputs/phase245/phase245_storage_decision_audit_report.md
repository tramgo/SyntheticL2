# Phase245 Storage Decision Audit

Generated UTC: 2026-07-29T08:33:08.841246+00:00

Phase245 is a non-destructive storage audit supporting the Phase244 future-holdout precommit.
It sizes workspace storage, identifies cleanup/archive candidates, and records download readiness without deleting files or downloading new raw dates.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase245_storage_decision_audit_complete | 1 | Phase245 storage audit completed |
| phase245_free_gb_now | 90.4129 | Free GB on workspace drive |
| phase245_inventory_rows | 34 | Storage inventory rows |
| phase245_cleanup_candidate_rows | 25 | Rows requiring user review before cleanup/archive |
| phase245_target_holdout_dates | 3 | Target future holdout dates from Phase244 |
| phase245_projected_required_gb | 7.5 | Conservative space needed for target fresh dates |
| phase245_projected_free_gb_after_target | 82.9129 | Projected free GB after target download |
| phase245_local_download_feasible_by_space_only | 1 | Space-only feasibility; still needs user storage decision |
| phase245_destructive_cleanup_allowed_now | 0 | No cleanup/delete action is allowed by Phase245 |
| phase245_download_more_dates_now_allowed | 0 | No additional raw-date download in Phase245 |
| phase245_holdout_execution_allowed_now | 0 | No holdout run in Phase245 |
| phase245_strategy_promotion_allowed | 0 | No strategy promotion from Phase245 |
| phase245_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase245 |
| phase245_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase245 |
| phase245_hard_gate_pass_rows | 6 | Hard gates passed |
| phase245_hard_gate_rows | 6 | Hard gates evaluated |
| phase245_next_best_action | choose_local_c_drive_download_or_cleanup_policy_then_run_phase246_fresh_holdout_download_no_tuning_no_paper_live | Recommended next milestone |

## Download Readiness Decision

| decision_id | free_gb_now | target_holdout_dates | min_holdout_dates | conservative_gb_per_date | projected_required_gb | projected_free_gb_after_target | min_free_gb_after_download | local_download_feasible_by_space_only | download_allowed_now | decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P245_LOCAL_C_DRIVE_DOWNLOAD_READINESS | 90.4129 | 3 | 2 | 2.5 | 7.5 | 82.9129 | 40 | 1 | 0 | storage_choice_still_required_before_download |

## Storage Inventory

| path | name | bytes | gb | files | category |
| --- | --- | --- | --- | --- | --- |
| raw_synthetic_l2_dense_full_year | raw_synthetic_l2_dense_full_year | 70591392905 | 65.7434 | 384 | synthetic_raw |
| real_data_sample | real_data_sample | 14087725499 | 13.1202 | 400813 | real_raw_or_sample |
| scratch_azcopy_selected | scratch_azcopy_selected | 5242732235 | 4.88267 | 149308 | scratch |
| raw_synthetic_l2_phase166_cross_symbol_lead_lag_cache | raw_synthetic_l2_phase166_cross_symbol_lead_lag_cache | 4635703054 | 4.31733 | 12 | synthetic_raw |
| raw_synthetic_l2_phase162_distributional_full_year | raw_synthetic_l2_phase162_distributional_full_year | 4141341739 | 3.85693 | 384 | synthetic_raw |
| outputs | outputs | 1576066201 | 1.46783 | 2323 | outputs |
| raw_synthetic_l2_phase108_symbol_aware_generator_overrides | raw_synthetic_l2_phase108_symbol_aware_generator_overrides | 926229441 | 0.862618 | 384 | synthetic_raw |
| raw_synthetic_l2_phase109_residual_imbalance_floor | raw_synthetic_l2_phase109_residual_imbalance_floor | 926197929 | 0.862589 | 384 | synthetic_raw |
| raw_synthetic_l2_phase106_full_symbol_calibrated_realism | raw_synthetic_l2_phase106_full_symbol_calibrated_realism | 879367260 | 0.818975 | 384 | synthetic_raw |
| raw_synthetic_l2_full_year | raw_synthetic_l2_full_year | 491002806 | 0.457282 | 8064 | synthetic_raw |
| raw_synthetic_l2_phase166_cross_symbol_lead_lag_cache_smoke | raw_synthetic_l2_phase166_cross_symbol_lead_lag_cache_smoke | 402215738 | 0.374593 | 1 | synthetic_raw |
| raw_synthetic_l2_phase156_symbol_tail_cadence_smoke | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke | 357833393 | 0.333258 | 32 | synthetic_raw |
| raw_synthetic_l2_phase159_distributional_cadence_smoke | raw_synthetic_l2_phase159_distributional_cadence_smoke | 357615839 | 0.333056 | 32 | synthetic_raw |
| raw_synthetic_l2_phase162_smoke | raw_synthetic_l2_phase162_smoke | 357615839 | 0.333056 | 32 | synthetic_raw |
| raw_synthetic_l2_dense_phase50_multisymbol_x64 | raw_synthetic_l2_dense_phase50_multisymbol_x64 | 269683823 | 0.251163 | 36 | synthetic_raw |
| raw_synthetic_l2_dense_phase51_smoke | raw_synthetic_l2_dense_phase51_smoke | 199480956 | 0.185781 | 1 | synthetic_raw |
| derived_real_l2_receive_flow_features_phase176 | derived_real_l2_receive_flow_features_phase176 | 178919247 | 0.166632 | 896 | derived_or_code |
| raw_synthetic_l2_full_year_compact_monthly | raw_synthetic_l2_full_year_compact_monthly | 177847919 | 0.165634 | 12 | synthetic_raw |
| derived_real_l2_receive_flow_labels_phase181 | derived_real_l2_receive_flow_labels_phase181 | 91602391 | 0.0853114 | 896 | derived_or_code |
| raw_synthetic_l2_dense_phase49_hdfcbank_x64 | raw_synthetic_l2_dense_phase49_hdfcbank_x64 | 90102511 | 0.0839145 | 12 | synthetic_raw |
| raw_synthetic_l2_phase101_calibrated_quality | raw_synthetic_l2_phase101_calibrated_quality | 69299190 | 0.0645399 | 36 | synthetic_raw |
| raw_synthetic_l2_phase102_anchored_price_quality | raw_synthetic_l2_phase102_anchored_price_quality | 68697202 | 0.0639793 | 36 | synthetic_raw |
| scratch_azcopy_smoke | scratch_azcopy_smoke | 56202239 | 0.0523424 | 1578 | scratch |
| scratch_azure_l2_selected_smoke | scratch_azure_l2_selected_smoke | 38177099 | 0.0355552 | 1076 | scratch |
| raw_synthetic_l2_phase105_source_mid_volatility_scale | raw_synthetic_l2_phase105_source_mid_volatility_scale | 27508190 | 0.025619 | 12 | synthetic_raw |
| raw_synthetic_l2_phase104_real_anchor_cadence | raw_synthetic_l2_phase104_real_anchor_cadence | 27191598 | 0.0253241 | 12 | synthetic_raw |
| derived_phase214_event_surprise_conditional_labels | derived_phase214_event_surprise_conditional_labels | 18480705 | 0.0172115 | 512 | derived_or_code |
| src | src | 11768355 | 0.0109601 | 531 | derived_or_code |
| derived_phase226_cost_aware_event_labels | derived_phase226_cost_aware_event_labels | 3640228 | 0.00339023 | 256 | derived_or_code |
| Plan | Plan | 541220 | 0.00050405 | 2 | derived_or_code |
| scripts | scripts | 324980 | 0.000302661 | 513 | derived_or_code |
| raw_synthetic_l2_phase45_sample | raw_synthetic_l2_phase45_sample | 93728 | 8.7291e-05 | 2 | synthetic_raw |
| scratch_azcopy_oauth_probe | scratch_azcopy_oauth_probe | 0 | 0 | 0 | scratch |
| scratch_azure_l2_download | scratch_azure_l2_download | 0 | 0 | 0 | scratch |

## Cleanup Candidate Ledger

| path | gb | files | cleanup_class | destructive_action_allowed_now | requires_user_approval | recommended_action | rationale |
| --- | --- | --- | --- | --- | --- | --- | --- |
| raw_synthetic_l2_dense_full_year | 65.7434 | 384 | archive_candidate_after_manifest_check | 0 | 1 | archive_or_move_if_space_needed | large generated raw synthetic artifact; archive or move before deletion |
| scratch_azcopy_selected | 4.88267 | 149308 | likely_safe_after_user_review | 0 | 1 | review_then_archive_or_delete | scratch/smoke artifact; not needed for current Phase244 frozen candidate unless user wants to preserve it |
| raw_synthetic_l2_phase166_cross_symbol_lead_lag_cache | 4.31733 | 12 | archive_candidate_after_manifest_check | 0 | 1 | archive_or_move_if_space_needed | large generated raw synthetic artifact; archive or move before deletion |
| raw_synthetic_l2_phase162_distributional_full_year | 3.85693 | 384 | archive_candidate_after_manifest_check | 0 | 1 | archive_or_move_if_space_needed | large generated raw synthetic artifact; archive or move before deletion |
| raw_synthetic_l2_phase108_symbol_aware_generator_overrides | 0.862618 | 384 | archive_candidate_after_manifest_check | 0 | 1 | archive_or_move_if_space_needed | large generated raw synthetic artifact; archive or move before deletion |
| raw_synthetic_l2_phase109_residual_imbalance_floor | 0.862589 | 384 | archive_candidate_after_manifest_check | 0 | 1 | archive_or_move_if_space_needed | large generated raw synthetic artifact; archive or move before deletion |
| raw_synthetic_l2_phase106_full_symbol_calibrated_realism | 0.818975 | 384 | archive_candidate_after_manifest_check | 0 | 1 | archive_or_move_if_space_needed | large generated raw synthetic artifact; archive or move before deletion |
| raw_synthetic_l2_full_year | 0.457282 | 8064 | archive_candidate_after_manifest_check | 0 | 1 | archive_or_move_if_space_needed | large generated raw synthetic artifact; archive or move before deletion |
| raw_synthetic_l2_phase166_cross_symbol_lead_lag_cache_smoke | 0.374593 | 1 | likely_safe_after_user_review | 0 | 1 | review_then_archive_or_delete | scratch/smoke artifact; not needed for current Phase244 frozen candidate unless user wants to preserve it |
| raw_synthetic_l2_phase156_symbol_tail_cadence_smoke | 0.333258 | 32 | likely_safe_after_user_review | 0 | 1 | review_then_archive_or_delete | scratch/smoke artifact; not needed for current Phase244 frozen candidate unless user wants to preserve it |
| raw_synthetic_l2_phase159_distributional_cadence_smoke | 0.333056 | 32 | likely_safe_after_user_review | 0 | 1 | review_then_archive_or_delete | scratch/smoke artifact; not needed for current Phase244 frozen candidate unless user wants to preserve it |
| raw_synthetic_l2_phase162_smoke | 0.333056 | 32 | likely_safe_after_user_review | 0 | 1 | review_then_archive_or_delete | scratch/smoke artifact; not needed for current Phase244 frozen candidate unless user wants to preserve it |
| raw_synthetic_l2_dense_phase50_multisymbol_x64 | 0.251163 | 36 | archive_candidate_after_manifest_check | 0 | 1 | archive_or_move_if_space_needed | large generated raw synthetic artifact; archive or move before deletion |
| raw_synthetic_l2_dense_phase51_smoke | 0.185781 | 1 | likely_safe_after_user_review | 0 | 1 | review_then_archive_or_delete | scratch/smoke artifact; not needed for current Phase244 frozen candidate unless user wants to preserve it |
| raw_synthetic_l2_full_year_compact_monthly | 0.165634 | 12 | archive_candidate_after_manifest_check | 0 | 1 | archive_or_move_if_space_needed | large generated raw synthetic artifact; archive or move before deletion |
| raw_synthetic_l2_dense_phase49_hdfcbank_x64 | 0.0839145 | 12 | archive_candidate_after_manifest_check | 0 | 1 | archive_or_move_if_space_needed | large generated raw synthetic artifact; archive or move before deletion |
| raw_synthetic_l2_phase101_calibrated_quality | 0.0645399 | 36 | archive_candidate_after_manifest_check | 0 | 1 | archive_or_move_if_space_needed | large generated raw synthetic artifact; archive or move before deletion |
| raw_synthetic_l2_phase102_anchored_price_quality | 0.0639793 | 36 | archive_candidate_after_manifest_check | 0 | 1 | archive_or_move_if_space_needed | large generated raw synthetic artifact; archive or move before deletion |
| scratch_azcopy_smoke | 0.0523424 | 1578 | likely_safe_after_user_review | 0 | 1 | review_then_archive_or_delete | scratch/smoke artifact; not needed for current Phase244 frozen candidate unless user wants to preserve it |
| scratch_azure_l2_selected_smoke | 0.0355552 | 1076 | likely_safe_after_user_review | 0 | 1 | review_then_archive_or_delete | scratch/smoke artifact; not needed for current Phase244 frozen candidate unless user wants to preserve it |
| raw_synthetic_l2_phase105_source_mid_volatility_scale | 0.025619 | 12 | archive_candidate_after_manifest_check | 0 | 1 | archive_or_move_if_space_needed | large generated raw synthetic artifact; archive or move before deletion |
| raw_synthetic_l2_phase104_real_anchor_cadence | 0.0253241 | 12 | archive_candidate_after_manifest_check | 0 | 1 | archive_or_move_if_space_needed | large generated raw synthetic artifact; archive or move before deletion |
| raw_synthetic_l2_phase45_sample | 8.7291e-05 | 2 | archive_candidate_after_manifest_check | 0 | 1 | archive_or_move_if_space_needed | large generated raw synthetic artifact; archive or move before deletion |
| scratch_azcopy_oauth_probe | 0 | 0 | likely_safe_after_user_review | 0 | 1 | review_then_archive_or_delete | scratch/smoke artifact; not needed for current Phase244 frozen candidate unless user wants to preserve it |
| scratch_azure_l2_download | 0 | 0 | likely_safe_after_user_review | 0 | 1 | review_then_archive_or_delete | scratch/smoke artifact; not needed for current Phase244 frozen candidate unless user wants to preserve it |
| real_data_sample | 13.1202 | 400813 | preserve_current_real_holdout | 0 | 0 | preserve | contains downloaded real L2 holdout data and seed samples |
| outputs | 1.46783 | 2323 | preserve_research_evidence | 0 | 0 | preserve | contains committed CSV/report evidence and ignored parquet outputs |
| derived_real_l2_receive_flow_features_phase176 | 0.166632 | 896 | preserve_by_default | 0 | 0 | preserve | code/plan/derived artifact; not a first cleanup target |
| derived_real_l2_receive_flow_labels_phase181 | 0.0853114 | 896 | preserve_by_default | 0 | 0 | preserve | code/plan/derived artifact; not a first cleanup target |
| derived_phase214_event_surprise_conditional_labels | 0.0172115 | 512 | preserve_by_default | 0 | 0 | preserve | code/plan/derived artifact; not a first cleanup target |
| src | 0.0109601 | 531 | preserve_by_default | 0 | 0 | preserve | code/plan/derived artifact; not a first cleanup target |
| derived_phase226_cost_aware_event_labels | 0.00339023 | 256 | preserve_by_default | 0 | 0 | preserve | code/plan/derived artifact; not a first cleanup target |
| Plan | 0.00050405 | 2 | preserve_by_default | 0 | 0 | preserve | code/plan/derived artifact; not a first cleanup target |
| scripts | 0.000302661 | 513 | preserve_by_default | 0 | 0 | preserve | code/plan/derived artifact; not a first cleanup target |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P245_PHASE244_STORAGE_GATE_OBSERVED | True | phase244_storage_decision_required=1 | Phase244 requires storage decision | hard |
| P245_STORAGE_INVENTORY_WRITTEN | True | 34 | >0 inventory rows | hard |
| P245_CLEANUP_LEDGER_NON_DESTRUCTIVE | True | 0 | all destructive actions disabled | hard |
| P245_DOWNLOAD_READINESS_WRITTEN | True | 1 | one readiness decision row | hard |
| P245_NO_DOWNLOAD_EXECUTED | True | 0 | 0 | hard |
| P245_NO_PAPER_LIVE_OR_PROFIT_CLAIM | True | 0 | 0 | hard |
