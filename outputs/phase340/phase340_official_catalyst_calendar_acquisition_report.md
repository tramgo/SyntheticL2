# Phase340 Official Catalyst Calendar Acquisition

Generated: 2026-08-11T07:15:20.072477+00:00

Phase340 acquires official NSE catalyst rows for the local real-L2 dates and records SEBI/BSE as regulator/cross-check sources before any real-day strategy diagnostic.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase340_official_catalyst_calendar_acquisition_complete | 1 | Phase340 completed |
| phase340_local_real_l2_date_rows | 7 | Local real L2 dates scanned |
| phase340_nse_announcement_source_ok_dates | 7 | NSE announcement fetch OK dates |
| phase340_official_catalyst_rows | 117 | Official catalyst rows for ticker universe and local dates |
| phase340_official_catalyst_symbols | 25 | Symbols with official catalyst rows |
| phase340_same_day_real_l2_catalyst_symbol_dates | 69 | Official catalyst symbol-dates with same-day local real L2 |
| phase340_sbin_official_catalyst_rows | 9 | SBIN official catalyst rows |
| phase340_sbin_official_catalyst_dates | 2026-07-08;2026-07-09;2026-07-10;2026-07-13;2026-07-14;2026-07-15;2026-07-16 | SBIN official catalyst dates |
| phase340_strategy_replay_allowed | 0 | No replay |
| phase340_strategy_promotion_allowed | 0 | No promotion |
| phase340_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase340_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase340_hard_gate_pass_rows | 8 | Passed hard gates |
| phase340_hard_gate_rows | 8 | Hard gates |
| phase340_next_best_action | run_phase341_official_catalyst_real_day_survivor_diagnostic_precommit_no_paper_live | Recommended next action |

## Gate evaluation

| gate_id | passed | observed | required |
| --- | --- | --- | --- |
| P340_PHASE339_COMPLETE | True | 1 | 1 |
| P340_OFFICIAL_NSE_ANNOUNCEMENTS_FETCHED | True | 7/7 | all local dates |
| P340_OFFICIAL_CATALYST_ROWS_PRESENT | True | 117 | >0 |
| P340_SAME_DAY_REAL_L2_OVERLAP_PRESENT | True | 69 | >0 |
| P340_SBIN_OFFICIAL_CONTEXT_PRESENT | True | 9 | >0 |
| P340_SOURCE_CATALOG_PRESENT | True | NSE/SEBI/BSE cataloged | present |
| P340_PHASE341_CONTRACT_PRESENT | True | 15 | >=12 |
| P340_NO_REPLAY_PROMOTION_OR_PROFIT_CLAIM | True | closed | closed |

## SBIN official catalyst context

| source_id | symbol | announcement_time_ist | description | text |
| --- | --- | --- | --- | --- |
| NSE_CORPORATE_ANNOUNCEMENTS | SBIN | 08-Jul-2026 15:25:29 | Credit Rating | State Bank Of India has informed the Exchange about Credit Rating |
| NSE_CORPORATE_ANNOUNCEMENTS | SBIN | 08-Jul-2026 20:27:40 | General Updates | State Bank of India has informed the Exchange about Update on IPO of SBI Funds Management Limited |
| NSE_CORPORATE_ANNOUNCEMENTS | SBIN | 08-Jul-2026 23:59:50 | General Updates | State Bank Of India has informed the Exchange about Update on IPO of SBI Funds Management Limited |
| NSE_CORPORATE_ANNOUNCEMENTS | SBIN | 09-Jul-2026 23:03:55 | General Updates | State Bank of India has informed the Exchange about Update on IPO of SBI Funds Management Limited |
| NSE_CORPORATE_ANNOUNCEMENTS | SBIN | 10-Jul-2026 22:26:10 | General Updates | State Bank of India has informed the Exchange about Update on IPO of SBI Funds Management Limited |
| NSE_CORPORATE_ANNOUNCEMENTS | SBIN | 13-Jul-2026 17:06:47 | General Updates | State Bank of India has informed the Exchange about Raising of Senior Unsecured Bond |
| NSE_CORPORATE_ANNOUNCEMENTS | SBIN | 14-Jul-2026 18:02:49 | Credit Rating | State Bank Of India has informed the Exchange about Credit Rating |
| NSE_CORPORATE_ANNOUNCEMENTS | SBIN | 15-Jul-2026 20:24:55 | Appointment | State Bank Of India has informed the Exchange regarding Appointment of Mr. Sunil Ramgopal Agrawal as Chief Financial Officer (Designate) w.e.f. July 15, 2026. |
| NSE_CORPORATE_ANNOUNCEMENTS | SBIN | 16-Jul-2026 22:52:22 | General Updates | State Bank of India has informed the Exchange about Update on IPO of SBI Funds Management Limited |

No replay, promotion, paper/live acceptance, or deployable profitability claim is opened by Phase340.