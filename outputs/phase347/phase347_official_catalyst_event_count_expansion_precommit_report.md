# Phase347 Official-Catalyst Event-Count Expansion Precommit

Generated: 2026-08-11T08:42:18.671106+00:00

Phase347 precommits a disk-aware event-count expansion around official catalyst days. It does not execute the rerun and does not open paper/live acceptance.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase347_official_catalyst_event_count_expansion_precommit_complete | 1 | Phase347 precommit completed |
| phase347_phase346_complete | 1 | Phase346 complete |
| phase347_candidate_grid_rows | 10 | Sparse control-passing candidate rows carried forward |
| phase347_official_source_priority_rows | 4 | Official source priority rows |
| phase347_official_timestamp_authority_rows | 3 | Official timestamp authority-capable rows |
| phase347_local_real_l2_dates | 7 | Local real L2 dates available |
| phase347_official_calendar_rows | 117 | Existing official catalyst calendar rows |
| phase347_inventory_date_rows | 7 | Existing inventory date rows |
| phase347_existing_no_lookahead_work_order_rows | 98 | Existing Phase341 no-lookahead work order rows |
| phase347_max_candidate_trade_rows | 19 | Maximum Phase346 candidate trade rows |
| phase347_additional_candidate_trade_rows_needed | 11 | Additional candidate trade rows needed to reach event floor |
| phase347_max_new_dates_per_increment | 1 | Disk-aware increment size |
| phase347_estimated_targeted_date_increments | 5 | Estimated targeted date increments |
| phase347_full_top_five_depth_required | 1 | Full top-five depth required |
| phase347_levels_2_to_5_materiality_required | 1 | Levels 2-5 materiality required |
| phase347_l1_only_allowed | 0 | No L1-only variants |
| phase347_fixed_capital_denominator_required | 1 | Fixed-capital denominator required |
| phase347_strategy_promotion_allowed | 0 | No promotion |
| phase347_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase347_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase347_hard_gate_pass_rows | 8 | Passed hard gates |
| phase347_hard_gate_rows | 8 | Hard gates |
| phase347_next_best_action | run_phase348_official_catalyst_event_count_expansion_execution_no_paper_live | Recommended next action |

## Official source priority

| source_id | priority | role | description | reference_url | official_timestamp_authority_allowed | paper_live_or_profit_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| NSE_CORPORATE_ANNOUNCEMENTS | 1 | primary_timestamp_authority | official exchange corporate announcements for symbol-level market disclosures | https://www.nseindia.com/companies-listing/corporate-filings-announcements | 1 | 0 |
| BSE_CORPORATE_ANNOUNCEMENTS | 2 | official_cross_check | official exchange cross-check for dual-listed company disclosures and timing disputes | https://www.bseindia.com/corporates/ann.html | 1 | 0 |
| SEBI_CORPORATE_FILINGS_AND_ORDERS | 3 | regulatory_context_and_material_action_source | regulatory filings, orders, circulars, and enforcement context; use as timestamp authority only when event publication timing is explicit | https://www.sebi.gov.in/curation/corporate_filings.html | 1 | 0 |
| NEWS_ANNOTATION_ONLY | 4 | context_not_timestamp_authority | news may explain catalyst context but must not replace official announcement timing | not_applicable | 0 | 0 |

## Candidate grid

| phase347_grid_id | scenario_id | family_id | entry_timing_policy | horizon_seconds | depth_threshold_quantile | annualized_return_pct | net_pnl_inr | trade_rows | additional_trade_rows_needed | control_pass | min_trade_rows_required | fixed_capital_required | full_top_five_depth_required | levels_2_to_5_materiality_required | l1_only_allowed | official_catalyst_required | paper_live_or_profit_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P347_GRID_000 | P345_0065_P344_SBIN_AND_BANK_CATALYST_DIAGNOSTIC_delay_300s_H1800_Q0p75 | P344_SBIN_AND_BANK_CATALYST_DIAGNOSTIC | delay_300s | 1800 | 0.75 | 57.2124 | 1135.17 | 2 | 28 | 1 | 30 | 1 | 1 | 1 | 0 | 1 | 0 |
| P347_GRID_001 | P345_0062_P344_SBIN_AND_BANK_CATALYST_DIAGNOSTIC_delay_300s_H900_Q0p75 | P344_SBIN_AND_BANK_CATALYST_DIAGNOSTIC | delay_300s | 900 | 0.75 | 39.221 | 778.194 | 2 | 28 | 1 | 30 | 1 | 1 | 1 | 0 | 1 | 0 |
| P347_GRID_002 | P345_0012_P344_CATALYST_CATEGORY_CONTINUATION_delay_60s_H900_Q0p0 | P344_CATALYST_CATEGORY_CONTINUATION | delay_60s | 900 | 0 | 38.2127 | 2274.57 | 19 | 11 | 1 | 30 | 1 | 1 | 1 | 0 | 1 | 0 |
| P347_GRID_003 | P345_0007_P344_CATALYST_CATEGORY_CONTINUATION_market_open_or_first_tick_after_announcement_H1800_Q0p5 | P344_CATALYST_CATEGORY_CONTINUATION | market_open_or_first_tick_after_announcement | 1800 | 0.5 | 35.184 | 1745.24 | 11 | 19 | 1 | 30 | 1 | 1 | 1 | 0 | 1 | 0 |
| P347_GRID_004 | P345_0026_P344_CATALYST_CATEGORY_CONTINUATION_delay_300s_H1800_Q0p75 | P344_CATALYST_CATEGORY_CONTINUATION | delay_300s | 1800 | 0.75 | 35.0616 | 347.834 | 2 | 28 | 1 | 30 | 1 | 1 | 1 | 0 | 1 | 0 |
| P347_GRID_005 | P345_0004_P344_CATALYST_CATEGORY_CONTINUATION_market_open_or_first_tick_after_announcement_H900_Q0p5 | P344_CATALYST_CATEGORY_CONTINUATION | market_open_or_first_tick_after_announcement | 900 | 0.5 | 31.5051 | 1562.75 | 11 | 19 | 1 | 30 | 1 | 1 | 1 | 0 | 1 | 0 |
| P347_GRID_006 | P345_0015_P344_CATALYST_CATEGORY_CONTINUATION_delay_60s_H1800_Q0p0 | P344_CATALYST_CATEGORY_CONTINUATION | delay_60s | 1800 | 0 | 30.131 | 1793.51 | 19 | 11 | 1 | 30 | 1 | 1 | 1 | 0 | 1 | 0 |
| P347_GRID_007 | P345_0006_P344_CATALYST_CATEGORY_CONTINUATION_market_open_or_first_tick_after_announcement_H1800_Q0p0 | P344_CATALYST_CATEGORY_CONTINUATION | market_open_or_first_tick_after_announcement | 1800 | 0 | 29.0403 | 1728.59 | 19 | 11 | 1 | 30 | 1 | 1 | 1 | 0 | 1 | 0 |
| P347_GRID_008 | P345_0008_P344_CATALYST_CATEGORY_CONTINUATION_market_open_or_first_tick_after_announcement_H1800_Q0p75 | P344_CATALYST_CATEGORY_CONTINUATION | market_open_or_first_tick_after_announcement | 1800 | 0.75 | 12.6679 | 377.02 | 6 | 24 | 1 | 30 | 1 | 1 | 1 | 0 | 1 | 0 |
| P347_GRID_009 | P345_0003_P344_CATALYST_CATEGORY_CONTINUATION_market_open_or_first_tick_after_announcement_H900_Q0p0 | P344_CATALYST_CATEGORY_CONTINUATION | market_open_or_first_tick_after_announcement | 900 | 0 | 12.4724 | 742.405 | 19 | 11 | 1 | 30 | 1 | 1 | 1 | 0 | 1 | 0 |

## Existing event inventory

| announcement_date | official_calendar_rows | symbols | local_real_l2_date_present | real_l2_matched_symbol_rows | matched_catalyst_rows | no_lookahead_work_order_rows | work_order_symbols |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-07-08 | 6 | 4 | 1 | 4 | 6 | 3 | 3 |
| 2026-07-09 | 16 | 10 | 1 | 10 | 16 | 6 | 4 |
| 2026-07-10 | 14 | 12 | 1 | 12 | 14 | 18 | 12 |
| 2026-07-13 | 21 | 7 | 1 | 7 | 21 | 12 | 9 |
| 2026-07-14 | 22 | 14 | 1 | 14 | 22 | 24 | 8 |
| 2026-07-15 | 14 | 11 | 1 | 11 | 14 | 20 | 13 |
| 2026-07-16 | 24 | 11 | 1 | 11 | 24 | 15 | 11 |

## Expansion work order

| work_order_id | work_type | priority | action | target_dates | target_symbols | max_new_dates_per_increment | disk_scope | success_condition | paper_live_or_profit_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P347_WO_001_OFFICIAL_SOURCE_REFRESH | official_catalyst_source_refresh | 1 | refresh NSE corporate announcements and add BSE/SEBI official cross-check columns for candidate symbols | next_available_unseen_official_catalyst_dates | ADANIPORTS;AXISBANK;BHARTIARTL;DRREDDY;HCLTECH;HDFCBANK;ICICIBANK;KOTAKBANK;M&M;RELIANCE;SBIN;TCS | 1 | metadata_only | official catalyst rows include source_id, symbol, announcement_time_ist, announcement_date, description, and no-lookahead timestamp authority | 0 |
| P347_WO_002_TARGETED_REAL_L2_DOWNLOAD | targeted_real_l2_download | 2 | download only date/exchange/symbol partitions that intersect official catalyst rows and candidate symbols | one_new_official_catalyst_matched_date_at_a_time | ADANIPORTS;AXISBANK;BHARTIARTL;DRREDDY;HCLTECH;HDFCBANK;ICICIBANK;KOTAKBANK;M&M;RELIANCE;SBIN;TCS | 1 | targeted_partitions_not_full_panel | add at least 11 candidate trade opportunities before acceptance re-evaluation; keep top-five book state persisted | 0 |
| P347_WO_003_NO_LOOKAHEAD_JOIN_REFRESH | no_lookahead_event_l2_join_refresh | 3 | rebuild official-catalyst to real-L2 work order using first tick at or after official announcement time | all_local_plus_new_targeted_dates | ADANIPORTS;AXISBANK;BHARTIARTL;DRREDDY;HCLTECH;HDFCBANK;ICICIBANK;KOTAKBANK;M&M;RELIANCE;SBIN;TCS | 1 | derived_csv_only | all replay candidates have no_lookahead_rule_applied=1 and full L1-L5 Zerodha top-five fields available | 0 |
| P347_WO_004_PHASE345_CANDIDATE_RERUN_PREP | candidate_grid_rerun_preparation | 4 | prepare Phase348 execution to rerun only Phase347 candidate grid rows on expanded event-count universe | all_local_plus_new_targeted_dates | ADANIPORTS;AXISBANK;BHARTIARTL;DRREDDY;HCLTECH;HDFCBANK;ICICIBANK;KOTAKBANK;M&M;RELIANCE;SBIN;TCS | 1 | scenario_outputs_only | candidate scenarios must reach >= 30 trades, beat controls, and remain > 12.0% fixed-capital annualized before any later acceptance discussion | 0 |

Phase348 may execute the targeted expansion only under this contract.