# Phase480 Comprehensive Local Real-L2 Breadth Audit

Phase480 corrects the narrow Phase478 inventory by auditing all known local real-L2 roots before asking for another Azure download.

Finding: the current local panel is broader than Phase478 reported. The latest expanded real-L2 retest evidence remains not accepted: positive net PnL but below the 12 percent annualized bar and below the 30 selected-trade floor.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase480_comprehensive_local_real_l2_breadth_audit_complete | 1 | Phase480 complete if all gates pass |
| phase480_thesis_id | P480_COMPREHENSIVE_LOCAL_REAL_L2_BREADTH_AUDIT | Phase480 thesis |
| phase480_local_real_l2_date_rows | 16 | Comprehensive local dated real-L2 dates |
| phase480_full_32_symbol_day_rows | 16 | Full 32-symbol local days |
| phase480_official_catalyst_overlap_date_rows | 16 | Catalyst-overlap dates |
| phase480_latest_selected_trade_rows | 25 | Latest frozen retest selected trades |
| phase480_latest_net_pnl_inr | 992.9649840110026 | Latest frozen retest net PnL |
| phase480_latest_annualized_return_pct | 7.149347884879218 | Latest frozen retest annualized return |
| phase480_latest_event_floor_met | 0 | Latest frozen retest event floor |
| phase480_latest_acceptance_candidate | 0 | Latest interpretation acceptance candidate |
| phase480_download_required_before_next_precommit | 0 | Current local panel is sufficient for next precommit decision |
| phase480_strategy_promotion_allowed | 0 | No promotion |
| phase480_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase480_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase480_hard_gate_pass_rows | 8 | Passed hard gates |
| phase480_hard_gate_rows | 8 | Hard gates |
| phase480_next_best_action | precommit_next_real_l2_breadth_or_capacity_retest_using_current_16_date_panel_no_download_first | Recommended next action |

## Local Date Summary

| trade_date | roots | symbols | parquet_files | bytes | full_32_symbol_universe |
| --- | --- | --- | --- | --- | --- |
| 2026-07-08 | real_data_sample\l2_multiday_panel;scratch_azcopy_selected\raw_l2 | 32 | 41014 | 1439784898 | 1 |
| 2026-07-09 | real_data_sample\l2_multiday_panel;scratch_azcopy_selected\raw_l2 | 32 | 57120 | 2012756334 | 1 |
| 2026-07-10 | real_data_sample\l2_multiday_panel;scratch_azcopy_selected\raw_l2 | 32 | 101018 | 3531214654 | 1 |
| 2026-07-13 | real_data_sample\l2_multiday_panel | 32 | 50205 | 1764005784 | 1 |
| 2026-07-14 | real_data_sample\l2_multiday_panel;scratch_azcopy_selected\raw_l2 | 32 | 99464 | 3501708584 | 1 |
| 2026-07-15 | real_data_sample\l2_multiday_panel | 32 | 50010 | 1756113023 | 1 |
| 2026-07-16 | real_data_sample\l2_multiday_panel | 32 | 50283 | 1763034702 | 1 |
| 2026-07-17 | real_data_sample\l2_unseen_validation | 32 | 50787 | 1788505298 | 1 |
| 2026-07-20 | real_data_sample\l2_unseen_validation | 32 | 50421 | 1773570501 | 1 |
| 2026-07-21 | real_data_sample\l2_unseen_validation | 32 | 50187 | 1763772568 | 1 |
| 2026-07-22 | real_data_sample\l2_unseen_validation | 32 | 50018 | 1753883840 | 1 |
| 2026-07-23 | real_data_sample\l2_unseen_validation | 32 | 49929 | 1758380336 | 1 |
| 2026-07-24 | real_data_sample\l2_unseen_validation | 32 | 50103 | 1759706001 | 1 |
| 2026-07-27 | real_data_sample\l2_unseen_validation | 32 | 5665 | 198041216 | 1 |
| 2026-08-03 | real_data_sample\l2_unseen_validation | 32 | 50073 | 1751944736 | 1 |
| 2026-08-04 | real_data_sample\l2_unseen_validation | 32 | 50499 | 1761442001 | 1 |

## Official Catalyst Overlap

| diagnostic_trade_date | catalyst_rows | catalyst_symbols | local_symbols | full_32_symbol_universe | symbol_date_overlaps | catalyst_source |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-07-08 | 6 | 4 | 32 | 1 | 4 | outputs\phase399\phase373_official_catalyst_calendar.csv |
| 2026-07-09 | 16 | 10 | 32 | 1 | 10 | outputs\phase399\phase373_official_catalyst_calendar.csv |
| 2026-07-10 | 14 | 12 | 32 | 1 | 12 | outputs\phase399\phase373_official_catalyst_calendar.csv |
| 2026-07-13 | 21 | 7 | 32 | 1 | 7 | outputs\phase399\phase373_official_catalyst_calendar.csv |
| 2026-07-14 | 22 | 14 | 32 | 1 | 14 | outputs\phase399\phase373_official_catalyst_calendar.csv |
| 2026-07-15 | 14 | 11 | 32 | 1 | 11 | outputs\phase399\phase373_official_catalyst_calendar.csv |
| 2026-07-16 | 24 | 11 | 32 | 1 | 11 | outputs\phase399\phase373_official_catalyst_calendar.csv |
| 2026-07-17 | 17 | 11 | 32 | 1 | 11 | outputs\phase399\phase373_official_catalyst_calendar.csv |
| 2026-07-20 | 21 | 8 | 32 | 1 | 8 | outputs\phase399\phase373_official_catalyst_calendar.csv |
| 2026-07-21 | 17 | 12 | 32 | 1 | 12 | outputs\phase399\phase373_official_catalyst_calendar.csv |
| 2026-07-22 | 20 | 15 | 32 | 1 | 15 | outputs\phase399\phase373_official_catalyst_calendar.csv |
| 2026-07-23 | 28 | 8 | 32 | 1 | 8 | outputs\phase399\phase373_official_catalyst_calendar.csv |
| 2026-07-24 | 26 | 17 | 32 | 1 | 17 | outputs\phase399\phase373_official_catalyst_calendar.csv |
| 2026-07-27 | 12 | 10 | 32 | 1 | 10 | outputs\phase399\phase373_official_catalyst_calendar.csv |
| 2026-08-03 | 11 | 9 | 32 | 1 | 9 | outputs\phase399\phase373_official_catalyst_calendar.csv |
| 2026-08-04 | 31 | 13 | 32 | 1 | 13 | outputs\phase399\phase373_official_catalyst_calendar.csv |

## Latest Retest Ledger

| metric | value | description |
| --- | --- | --- |
| phase399_refreshed_eligible_rows | 273 | Latest duplicated Phase373 refresh eligible rows. |
| phase399_estimated_selected_after_refresh | 36.19512195121951 | Latest estimated selected trades after refresh. |
| phase399_event_floor_after_refresh_estimate | 1 | Event floor estimate from refresh. |
| phase400_adapted_work_order_rows | 273 | Latest precommitted adapted work order rows. |
| phase400_adapted_work_order_dates | 16 | Latest work-order diagnostic dates. |
| phase401_primary_selected_trade_rows | 25 | Actual frozen retest selected trades. |
| phase401_primary_net_pnl_inr | 992.9649840110026 | Actual frozen retest net PnL. |
| phase401_primary_annualized_return_pct | 7.149347884879218 | Actual frozen retest annualized return. |
| phase401_primary_event_floor_met | 0 | Actual frozen retest event floor. |
| phase402_acceptance_candidate | 0 | Latest interpretation acceptance candidate flag. |
| phase402_capacity_selected_gap | 5 | Remaining capacity-selected trade gap. |
| phase402_next_best_action | precommit_capacity_rule_sensitivity_or_add_more_real_l2_no_paper_live | Latest interpretation next action. |

## Decision Ledger

| decision_id | decision_value | evidence |
| --- | --- | --- |
| comprehensive_local_real_l2_dates | 16 | Local dated real-L2 dates across comprehensive roots. |
| comprehensive_full_32_symbol_days | 16 | Local dates with at least the 32-symbol configured universe. |
| official_catalyst_overlap_dates | 16 | Dates with both local L2 and official catalyst symbol-date overlap. |
| latest_actual_selected_trades | 25 | Latest frozen expanded retest selected trades. |
| latest_actual_annualized_return_pct | 7.14935 | Latest frozen expanded retest annualized return. |
| latest_event_floor_met | 0 | Latest frozen expanded retest event floor. |
| latest_acceptance_candidate | 0 | Latest interpretation acceptance flag. |
| download_required_before_any_next_step | 0 | A local 16-date panel exists; first precommit using current local evidence before downloading more. |
| next_action | precommit_next_real_l2_breadth_or_capacity_retest_using_current_16_date_panel_no_download_first | Corrects Phase478's narrow inventory and keeps paper/live closed. |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P480_COMPREHENSIVE_ROOTS_USED | True | 16 | >=16 | hard |
| P480_FULL_UNIVERSE_DAYS_PRESENT | True | 16 | >=1 | hard |
| P480_TOP5_SCHEMA_SAMPLED | True | 640 | >0 | hard |
| P480_OFFICIAL_CATALYST_OVERLAP_PRESENT | True | 172 | >0 | hard |
| P480_LATEST_RETEST_EVIDENCE_USED | True | 25 | >0 | hard |
| P480_ACCEPTANCE_STILL_CLOSED | True | 0 | 0 | hard |
| P480_DOWNLOAD_NOT_REQUIRED_BEFORE_NEXT_PRECOMMIT | True | 0 | 0 | hard |
| P480_NO_PROMOTION_PAPER_LIVE_OR_CLAIM | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: no strategy promotion, no paper/live, no deployable profitability claim.
