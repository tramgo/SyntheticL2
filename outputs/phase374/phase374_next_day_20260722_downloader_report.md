# Phase374 Next-Day 2026-07-22 Downloader

Generated: 2026-08-11T18:56:17.245360+00:00

Phase374 selects the next target from Phase373 pending post-close catalyst rows, downloads/verifies the full-universe real L2 day when SAS is available, and does not run a strategy retest.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase374_next_day_20260722_downloader_complete | 1 | Phase374 complete if all hard gates pass |
| phase374_target_trade_date | 2026-07-22 | Next target date from Phase373 pending post-close rows |
| phase374_pending_post_close_event_rows | 9 | Known pending post-close catalyst rows unlocked by target |
| phase374_sas_env_present | 1 | Supported SAS env present |
| phase374_truststore_injected | 1 | Truststore injected before HTTPS calls |
| phase374_dry_run | 0 | Dry-run mode |
| phase374_workers | 96 | Concurrent workers |
| phase374_discovered_file_rows | 50018 | Discovered target file rows |
| phase374_discovered_symbols | 32 | Discovered target symbols |
| phase374_download_manifest_rows | 50018 | Download manifest rows |
| phase374_existing_file_rows | 49985 | Existing/skipped file rows |
| phase374_downloaded_file_rows | 33 | Downloaded file rows |
| phase374_error_file_rows | 0 | Per-file error rows |
| phase374_local_symbols_after | 32 | Local symbols after |
| phase374_local_parquet_files_after | 50018 | Local parquet files after |
| phase374_local_bytes_after | 1753883840 | Local bytes after |
| phase374_local_full_universe_after | 1 | Full universe local after |
| phase374_estimated_selected_after_target | 26.8694 | Estimated selected trades after adding target pending events |
| phase374_event_floor_after_target_estimate | 0 | Whether target estimate reaches 30-event floor |
| phase374_acceptance_retest_allowed_now | 0 | No retest in this phase |
| phase374_strategy_promotion_allowed | 0 | No promotion |
| phase374_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase374_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase374_hard_gate_pass_rows | 7 | Passed hard gates |
| phase374_hard_gate_rows | 7 | Hard gates |
| phase374_next_best_action | refresh_catalyst_event_count_after_20260722_no_paper_live | Recommended next milestone |

## Pending post-close events

| source_id | symbol | announcement_time_ist | announcement_date | market_session | diagnostic_trade_date | diagnostic_start_rule | diagnostic_real_l2_available | description | text | attachment_url | seq_id | no_lookahead_rule_applied |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NSE_CORPORATE_ANNOUNCEMENTS | AXISBANK | 21-Jul-2026 16:44:03 | 2026-07-21 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | ESOP/ESOS/ESPS | Axis Bank Limited has informed the Exchange regarding Allotment of 116524  Shares. | https://nsearchives.nseindia.com/corporate/AXISBANK1_21072026164341_SE21072026.pdf | 106705112 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | BAJAJ-AUTO | 21-Jul-2026 19:01:27 | 2026-07-21 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Shareholders meeting | Bajaj Auto Limited has informed the Exchange regarding summary of proceedings of the 19th Annual General Meeting held on July 21, 2026 | https://nsearchives.nseindia.com/corporate/lkwalimbe_bajajauto_co_in_21072026190115_SE_Proceedings_AGM.pdf | 106705514 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | BAJAJ-AUTO | 21-Jul-2026 20:34:04 | 2026-07-21 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Analysts/Institutional Investor Meet/Con. Call Updates | Bajaj Auto Limited has informed the Exchange about Link of Recording | https://nsearchives.nseindia.com/corporate/lkwalimbe_bajajauto_co_in_21072026203347_SE_-_Q1_FY27_Recording.pdf | 106705680 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | HCLTECH | 21-Jul-2026 18:21:08 | 2026-07-21 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Copy of Newspaper Publication | HCL Technologies Limited has informed the Exchange about Copy of Newspaper Publication | https://nsearchives.nseindia.com/corporate/HCLTECH_21072026182052_Stock_Exchange_Intimation_PostAGM_NP_Ad.pdf | 106705416 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | ICICIBANK | 21-Jul-2026 23:20:36 | 2026-07-21 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | General Updates | ICICI Bank Limited has informed the Exchange about Disclosure under Regulation 30 read with Para A of Schedule III and Regulation 46(2) of the Securities and Exchange Board of India (Listing Obligations and Disclosure Requirements) Regulations, 2015. | https://nsearchives.nseindia.com/corporate/ICICI2022_21072026231248_NSEBSE_21072026.pdf | 106705817 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | INFY | 21-Jul-2026 15:36:37 | 2026-07-21 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Updates | Infosys Limited has informed the Exchange regarding 'Disclosure Under Regulation 30 Of SEBI LODR Regulations'. | https://nsearchives.nseindia.com/corporate/Infosys_21072026153557_SE_filing_Reg_30_disclosure.pdf | 106704970 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | SBIN | 21-Jul-2026 16:12:21 | 2026-07-21 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | Press Release | State Bank of India has informed the Exchange regarding a press release dated July 21, 2026, titled "Listing of SBI Funds Management Limited". | https://nsearchives.nseindia.com/corporate/SBIN_21072026161210_BSE_NSE_PressRelease_21072026.pdf | 106705034 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | TECHM | 21-Jul-2026 20:56:40 | 2026-07-21 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | General Updates | Tech Mahindra Limited has informed the Exchange about General Updates | https://nsearchives.nseindia.com/corporate/Apekshakhemka_21072026205630_Signed_-_SE_intimation_ESG_rating_crisil.pdf | 106705690 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | WIPRO | 21-Jul-2026 19:23:03 | 2026-07-21 | post_close |  | market_open_next_available_unseen_real_l2_day | 0 | General Updates | Wipro Limited has informed the Exchange about Intimation under Regulation 30 of SEBI (Listing Obligations and Disclosure Requirements) Regulations, 2015 | https://nsearchives.nseindia.com/corporate/Cslogin_21072026191548_Reg30SEIntimation21072026.pdf | 106705563 | 1 |

## Access ledger

| access_route | available | result | evidence | secret_material_recorded |
| --- | --- | --- | --- | --- |
| file_sas_env | 1 | file_sas_discovery_attempted | env=AZURE_FILE_SERVICE_SAS_URL;shares_checked=1;rows=50018 | 0 |

## Gate evaluation

| gate_id | passed | evidence |
| --- | --- | --- |
| P374_PHASE373_PRESENT | 1 | Phase373 complete |
| P374_TARGET_SELECTED | 1 | 2026-07-22 |
| P374_SAS_OR_SAFE_WAIT | 1 | sas_present=1 |
| P374_DISCOVERY_OR_WAIT_RECORDED | 1 | discovered_rows=50018; error=0 |
| P374_FULL_UNIVERSE_VERIFIED_OR_PENDING | 1 | local_symbols=32 |
| P374_NO_SECRET_MATERIAL_RECORDED | 1 | secret_rows=0 |
| P374_NO_STRATEGY_RETEST_OR_PROMOTION | 1 | download_and_event_floor_estimate_only |

No strategy retest, promotion, paper/live acceptance, or deployable profitability claim is opened.
