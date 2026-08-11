# Phase378 Next-Day 2026-07-24 Downloader

Generated: 2026-08-11T19:43:58.039080+00:00

Phase378 selects the next target from Phase377 pending post-close catalyst rows, downloads/verifies the full-universe real L2 day when SAS is available, and does not run a strategy retest.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase378_next_day_20260724_downloader_complete | 1 | Phase378 complete if all hard gates pass |
| phase378_target_trade_date | 2026-07-24 | Next target date from Phase377 pending post-close rows |
| phase378_pending_post_close_event_rows | 18 | Known pending post-close catalyst rows unlocked by target |
| phase378_sas_env_present | 1 | Supported SAS env present |
| phase378_truststore_injected | 1 | Truststore injected before HTTPS calls |
| phase378_dry_run | 0 | Dry-run mode |
| phase378_workers | 128 | Concurrent workers |
| phase378_discovered_file_rows | 50103 | Discovered target file rows |
| phase378_discovered_symbols | 32 | Discovered target symbols |
| phase378_download_manifest_rows | 50103 | Download manifest rows |
| phase378_existing_file_rows | 50097 | Existing/skipped file rows |
| phase378_downloaded_file_rows | 6 | Downloaded file rows |
| phase378_error_file_rows | 0 | Per-file error rows |
| phase378_local_symbols_after | 32 | Local symbols after |
| phase378_local_parquet_files_after | 50103 | Local parquet files after |
| phase378_local_bytes_after | 1759706001 | Local bytes after |
| phase378_local_full_universe_after | 1 | Full universe local after |
| phase378_estimated_selected_after_target | 31.8764 | Estimated selected trades after adding target pending events |
| phase378_event_floor_after_target_estimate | 1 | Whether target estimate reaches 30-event floor |
| phase378_acceptance_retest_allowed_now | 0 | No retest in this phase |
| phase378_strategy_promotion_allowed | 0 | No promotion |
| phase378_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase378_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase378_hard_gate_pass_rows | 7 | Passed hard gates |
| phase378_hard_gate_rows | 7 | Hard gates |
| phase378_next_best_action | refresh_catalyst_event_count_after_20260724_no_paper_live | Recommended next milestone |

## Pending post-close events

| source_id | symbol | announcement_time_ist | announcement_date | market_session | diagnostic_trade_date | diagnostic_start_rule | diagnostic_real_l2_available | description | text | attachment_url | seq_id | no_lookahead_rule_applied |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NSE_CORPORATE_ANNOUNCEMENTS | BPCL | 23-Jul-2026 16:59:09 | 2026-07-23 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Analysts/Institutional Investor Meet/Con. Call Updates | Bharat Petroleum Corporation Limited has informed the Exchange about Link of Recording | https://nsearchives.nseindia.com/corporate/BPCL26_23072026165840_1stexaudiorecording23726s.pdf | 106708242 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | CIPLA | 23-Jul-2026 19:28:07 | 2026-07-23 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Analysts/Institutional Investor Meet/Con. Call Updates | Cipla Limited has informed the Exchange about Link of Recording | https://nsearchives.nseindia.com/corporate/CIPLA_23072026192748_Earnings_call_audio_CoveringSigned.pdf | 106708657 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | DRREDDY | 23-Jul-2026 20:52:04 | 2026-07-23 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Copy of Newspaper Publication | Dr. Reddy's Laboratories Limited has informed the Exchange about Copy of Newspaper Publication | https://nsearchives.nseindia.com/corporate/DRREDDY_23072026205157_SEintimation_newspaperpublication_23072026.pdf | 106708749 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | DRREDDY | 23-Jul-2026 21:13:36 | 2026-07-23 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Shareholders meeting | Dr. Reddy's Laboratories Limited has informed the Exchange regarding Proceedings of Annual General Meeting held on July 23, 2026. Further, the company has submitted the Exchange a copy of Srutinizers report along with voting results. | https://nsearchives.nseindia.com/corporate/DRREDDY_23072026211307_SE_Itimation_AGM_outcome_signed.pdf | 106708761 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | DRREDDY | 23-Jul-2026 21:18:07 | 2026-07-23 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Change in Director(s) | Dr. Reddy's Laboratories Limited has informed the Exchange regarding Change in Director(s) of the company. | https://nsearchives.nseindia.com/corporate/DRREDDY_23072026211751_SEintimation_Regulation_30_Director_and_Stat_Auditor_signed.pdf | 106708768 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | DRREDDY | 23-Jul-2026 21:20:01 | 2026-07-23 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Change in Auditors | Dr. Reddy's Laboratories Limited has informed the Exchange regarding Change in Auditors of the company. | https://nsearchives.nseindia.com/corporate/DRREDDY_23072026211951_SEintimation_Regulation_30_Director_and_Stat_Auditor_signed.pdf | 106708771 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | ICICIBANK | 23-Jul-2026 18:05:02 | 2026-07-23 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Analysts/Institutional Investor Meet/Con. Call Updates | ICICI Bank Limited has informed the Exchange about the transcripts of the call with media and of earnings call with the analysts and investors on the financial results for the quarter ended June 30, 2026. | https://nsearchives.nseindia.com/corporate/ICICI2022_23072026180406_NSEBSE_23072026.pdf | 106708461 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | ICICIBANK | 23-Jul-2026 18:56:18 | 2026-07-23 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Analysts/Institutional Investor Meet/Con. Call Updates | ICICI Bank Limited has informed the Exchange about the transcripts of the call with media and of earnings call with the analysts and investors on the financial results for the quarter ended June 30, 2026. | https://nsearchives.nseindia.com/corporate/ICICI2022_23072026185521_NSEBSE.pdf | 106708594 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | INFY | 23-Jul-2026 16:20:26 | 2026-07-23 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Outcome of Board Meeting | Infosys Limited has submitted to the Exchange, the financial results for the period ended Jun 30, 2026. | https://nsearchives.nseindia.com/corporate/Infosys_23072026161911_Outcome23072026V1_1.pdf | 106708149 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | INFY | 23-Jul-2026 16:43:21 | 2026-07-23 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Updates | Infosys Limited has informed the Exchange regarding 'Appointed of Ashiss Kumar Dash as the Chief Executive Officer Designate effective July 23, 2026'. | https://nsearchives.nseindia.com/corporate/Infosys_23072026164257_Outcome23072026V1_1.pdf | 106708206 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | INFY | 23-Jul-2026 21:04:09 | 2026-07-23 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Updates | Infosys Limited has informed the Exchange regarding 'Report Of Auditors On Financial Statements For The Quarter Ended June 30, 2026 With UDIN'. | https://nsearchives.nseindia.com/corporate/Infosys_23072026210352_SE_filing_Auditors_report_with_UDIN-July_2026.pdf | 106708755 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | ITC | 23-Jul-2026 18:03:26 | 2026-07-23 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Shareholders meeting | ITC Limited has informed the Exchange regarding Proceedings of  Annual General Meeting held on July 23, 2026. Further, the company has informed the Exchange regarding voting results. | https://nsearchives.nseindia.com/corporate/ITC_23072026180304_SE_VotingResults_.pdf | 106708449 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | ITC | 23-Jul-2026 18:13:25 | 2026-07-23 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | General Updates | ITC Limited has informed the address delivered by the Chairman at the 115th Annual General Meeting of the Company on the theme    ITC: Partnering India in its Defining Decade . | https://nsearchives.nseindia.com/corporate/ITC_23072026181315_SE_chairmanspeech_.pdf | 106708490 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | ITC | 23-Jul-2026 18:21:35 | 2026-07-23 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Change in Director(s) | ITC Limited has informed the Exchange regarding Change in Director(s) of the company. | https://nsearchives.nseindia.com/corporate/ITC_23072026182127_SE_Director_.pdf | 106708509 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | ITC | 23-Jul-2026 20:42:12 | 2026-07-23 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Credit Rating- New | ITC Limited has informed the Exchange about Intimation of ESG rating assigned by Crisil ESG Ratings & Analytics Limited | https://nsearchives.nseindia.com/corporate/ITC_23072026204201_SE_ESG_.pdf | 106708738 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | NESTLEIND | 23-Jul-2026 18:26:02 | 2026-07-23 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Analysts/Institutional Investor Meet/Con. Call Updates | Nestle India Limited has informed the Exchange about the Intimation of an analyst/ institutional investors meet (virtual) schedule for 4th August 2026 at 2PM (IST) | https://nsearchives.nseindia.com/corporate/NESTLEIND1_23072026182359_AnalystsMeet4Aug2026signed.pdf | 106708516 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | ULTRACEMCO | 23-Jul-2026 18:40:56 | 2026-07-23 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Analysts/Institutional Investor Meet/Con. Call Updates | UltraTech Cement Limited has informed the Exchange about Transcript | https://nsearchives.nseindia.com/corporate/ULTRACEMCO1_23072026184045_SE_Letter_-_Transcript.pdf | 106708557 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | ULTRACEMCO | 23-Jul-2026 18:45:39 | 2026-07-23 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Credit Rating | UltraTech Cement Limited has informed the Exchange about Credit Rating | https://nsearchives.nseindia.com/corporate/ULTRACEMCO1_23072026184530_Credit_Rating_SE_Letter.pdf | 106708565 | 1 |

## Access ledger

| access_route | available | result | evidence | secret_material_recorded |
| --- | --- | --- | --- | --- |
| file_sas_env | 1 | file_sas_discovery_attempted | env=AZURE_STORAGE_SAS_TOKEN;shares_checked=1;rows=50103 | 0 |

## Gate evaluation

| gate_id | passed | evidence |
| --- | --- | --- |
| P378_PHASE377_PRESENT | 1 | Phase377 complete |
| P378_TARGET_SELECTED | 1 | 2026-07-24 |
| P378_SAS_OR_SAFE_WAIT | 1 | sas_present=1 |
| P378_DISCOVERY_OR_WAIT_RECORDED | 1 | discovered_rows=50103; error=0 |
| P378_FULL_UNIVERSE_VERIFIED_OR_PENDING | 1 | local_symbols=32 |
| P378_NO_SECRET_MATERIAL_RECORDED | 1 | secret_rows=0 |
| P378_NO_STRATEGY_RETEST_OR_PROMOTION | 1 | download_and_event_floor_estimate_only |

No strategy retest, promotion, paper/live acceptance, or deployable profitability claim is opened.
