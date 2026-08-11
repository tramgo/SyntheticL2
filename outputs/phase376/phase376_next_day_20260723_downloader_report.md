# Phase376 Next-Day 2026-07-23 Downloader

Generated: 2026-08-11T19:22:56.138254+00:00

Phase376 selects the next target from Phase375 pending post-close catalyst rows, downloads/verifies the full-universe real L2 day when SAS is available, and does not run a strategy retest.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase376_next_day_20260723_downloader_complete | 1 | Phase376 complete if all hard gates pass |
| phase376_target_trade_date | 2026-07-23 | Next target date from Phase375 pending post-close rows |
| phase376_pending_post_close_event_rows | 14 | Known pending post-close catalyst rows unlocked by target |
| phase376_sas_env_present | 1 | Supported SAS env present |
| phase376_truststore_injected | 1 | Truststore injected before HTTPS calls |
| phase376_dry_run | 0 | Dry-run mode |
| phase376_workers | 128 | Concurrent workers |
| phase376_discovered_file_rows | 49929 | Discovered target file rows |
| phase376_discovered_symbols | 32 | Discovered target symbols |
| phase376_download_manifest_rows | 49929 | Download manifest rows |
| phase376_existing_file_rows | 49929 | Existing/skipped file rows |
| phase376_downloaded_file_rows | 0 | Downloaded file rows |
| phase376_error_file_rows | 0 | Per-file error rows |
| phase376_local_symbols_after | 32 | Local symbols after |
| phase376_local_parquet_files_after | 49929 | Local parquet files after |
| phase376_local_bytes_after | 1758380336 | Local bytes after |
| phase376_local_full_universe_after | 1 | Full universe local after |
| phase376_estimated_selected_after_target | 29.0447 | Estimated selected trades after adding target pending events |
| phase376_event_floor_after_target_estimate | 0 | Whether target estimate reaches 30-event floor |
| phase376_acceptance_retest_allowed_now | 0 | No retest in this phase |
| phase376_strategy_promotion_allowed | 0 | No promotion |
| phase376_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase376_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase376_hard_gate_pass_rows | 7 | Passed hard gates |
| phase376_hard_gate_rows | 7 | Hard gates |
| phase376_next_best_action | refresh_catalyst_event_count_after_20260723_no_paper_live | Recommended next milestone |

## Pending post-close events

| source_id | symbol | announcement_time_ist | announcement_date | market_session | diagnostic_trade_date | diagnostic_start_rule | diagnostic_real_l2_available | description | text | attachment_url | seq_id | no_lookahead_rule_applied |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NSE_CORPORATE_ANNOUNCEMENTS | BAJAJ-AUTO | 22-Jul-2026 20:31:27 | 2026-07-22 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Shareholders meeting | Bajaj Auto Limited has submitted the Exchange a copy Srutinizers report of  19th Annual General Meeting held on July 21, 2026. Further, the company has informed the Exchange regarding voting results. | https://nsearchives.nseindia.com/corporate/lkwalimbe_bajajauto_co_in_22072026203113_SE_Intimation_AGM_VR_Signed.pdf | 106707142 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | BHARTIARTL | 22-Jul-2026 16:13:11 | 2026-07-22 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Action(s) taken or orders passed | Bharti Airtel Limited has informed the Exchange about Action(s) taken or orders passed | https://nsearchives.nseindia.com/corporate/BHARTIARTL_22072026160914_BhartiAirtelReg30disclosure.pdf | 106706585 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | BPCL | 22-Jul-2026 20:46:39 | 2026-07-22 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Investor Presentation | Bharat Petroleum Corporation Limited has informed the Exchange about Investor Presentation | https://nsearchives.nseindia.com/corporate/BPCL22_22072026204629_stexinvestorhandouts22726s.pdf | 106707155 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | DRREDDY | 22-Jul-2026 16:18:02 | 2026-07-22 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Outcome of Board Meeting | Dr. Reddy's Laboratories Limited has submitted to the Exchange, the financial results for the period ended Jun 30, 2026. | https://nsearchives.nseindia.com/corporate/DRREDDY_22072026161515_SE_Intimation_Outcome_results_22072026_1.pdf | 106706597 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | DRREDDY | 22-Jul-2026 16:21:28 | 2026-07-22 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Change in Management | Dr. Reddy's Laboratories Limited has informed the Exchange about change in Management | https://nsearchives.nseindia.com/corporate/DRREDDY_22072026162110_SE_intimation_Reg30_change_in_mgt_auditor_22072026_1.pdf | 106706606 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | DRREDDY | 22-Jul-2026 16:44:07 | 2026-07-22 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | General Updates | Dr. Reddy's Laboratories Limited has informed the Exchange about allotment of Employee Stock Options | https://nsearchives.nseindia.com/corporate/DRREDDY_22072026164348_SE_intimation_ESOP_grants_final_with_annexure.pdf | 106706646 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | DRREDDY | 22-Jul-2026 16:48:23 | 2026-07-22 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Investor Presentation | Dr. Reddy's Laboratories Limited has informed the Exchange about Investor Presentation | https://nsearchives.nseindia.com/corporate/DRREDDY_22072026164806_SEintimation_Investor_presentation_22072026.pdf | 106706656 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | HCLTECH | 22-Jul-2026 18:57:42 | 2026-07-22 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Updates | HCL Technologies Limited has informed the Exchange regarding 'Release:  TIM Brasil partners with HCLTech to transform customer experience with South America s first cross-platform eSIM transfer capability '. | https://nsearchives.nseindia.com/corporate/HCLTECH_22072026185707_Release22July2026.pdf | 106706995 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | HINDUNILVR | 22-Jul-2026 20:03:51 | 2026-07-22 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Analysts/Institutional Investor Meet/Con. Call Updates | Intimation of Earnings Conference Call for the quarter ended 30th June, 2026 | https://nsearchives.nseindia.com/corporate/HINDUNILVR_22072026200316_28072026EarningConferenceCallIntimationsigned.pdf | 106707122 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | M&M | 22-Jul-2026 17:48:35 | 2026-07-22 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Updates | Mahindra & Mahindra Limited has informed the Exchange regarding ''Transfer of Equity Shares by Mahindra & Mahindra Employees Stock Option Trust to the Stock Option Grantees'.'. | https://nsearchives.nseindia.com/corporate/Deepak_22072026174658_Employeeslist22072026.pdf | 106706794 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | RELIANCE | 22-Jul-2026 16:09:43 | 2026-07-22 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Copy of Newspaper Publication | Newspaper clippings - Postal Ballot Notice and other related informationThe newspaper clippings of the advertisement on the captioned subject published today i.e., July 22, 2026 in the newspapers viz. The Times of India (English) and Maharashtra Times (Marathi) are enclosed for information and records. | https://nsearchives.nseindia.com/corporate/PVIVINMA_22072026160927_SENPClipping.pdf | 106706565 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | TCS | 22-Jul-2026 16:33:09 | 2026-07-22 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Updates | Tata Consultancy Services Limited has informed the Exchange regarding 'Press Release - TCS study reveals Physical AI is now mainstream as manufacturers scale AI implementation'. | https://nsearchives.nseindia.com/corporate/TCS_CORPCS_22072026163254_PR_22July26_signed.pdf | 106706625 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | ULTRACEMCO | 22-Jul-2026 19:07:08 | 2026-07-22 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Copy of Newspaper Publication | UltraTech Cement Limited has informed the Exchange about Copy of Newspaper Publication regarding the 26th Annual General Meeting of the Company | https://nsearchives.nseindia.com/corporate/ULTRACEMCO_22072026190702_SE_Intimation22072026.pdf | 106707026 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | WIPRO | 22-Jul-2026 19:11:57 | 2026-07-22 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | General Updates | Wipro Limited has informed the Exchange about Intimation under Regulation 30 of SEBI (Listing Obligations and Disclosure Requirements) Regulations, 2015 | https://nsearchives.nseindia.com/corporate/Wipro_Secretarial_22072026191054_Reg30SEIntimation22072026.pdf | 106707035 | 1 |

## Access ledger

| access_route | available | result | evidence | secret_material_recorded |
| --- | --- | --- | --- | --- |
| file_sas_env | 1 | file_sas_discovery_attempted | env=AZURE_STORAGE_SAS_TOKEN;shares_checked=1;rows=49929 | 0 |

## Gate evaluation

| gate_id | passed | evidence |
| --- | --- | --- |
| P376_PHASE375_PRESENT | 1 | Phase375 complete |
| P376_TARGET_SELECTED | 1 | 2026-07-23 |
| P376_SAS_OR_SAFE_WAIT | 1 | sas_present=1 |
| P376_DISCOVERY_OR_WAIT_RECORDED | 1 | discovered_rows=49929; error=0 |
| P376_FULL_UNIVERSE_VERIFIED_OR_PENDING | 1 | local_symbols=32 |
| P376_NO_SECRET_MATERIAL_RECORDED | 1 | secret_rows=0 |
| P376_NO_STRATEGY_RETEST_OR_PROMOTION | 1 | download_and_event_floor_estimate_only |

No strategy retest, promotion, paper/live acceptance, or deployable profitability claim is opened.
