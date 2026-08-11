# Phase359 Local Unseen Real L2 Catalyst Expansion

Generated: 2026-08-11T15:29:27.265494+00:00

Phase359 registers local unseen real L2 dates already present on disk, fetches official NSE catalyst rows for those dates, applies no-lookahead eligibility, verifies full L1-L5 market-by-price schema, and emits a Phase360 work order. It does not download more data and does not open promotion, paper/live, or profitability claims.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase359_local_unseen_real_l2_catalyst_expansion_complete | 1 | Phase359 completed if all hard gates pass |
| phase359_existing_real_l2_dates | 7 | Existing multiday local real L2 dates |
| phase359_unseen_real_l2_dates | 2 | New unseen local real L2 dates detected |
| phase359_unseen_date_list | 2026-07-17;2026-07-20 | Unseen date list |
| phase359_unseen_symbol_date_rows | 64 | Unseen symbol/date rows |
| phase359_unseen_symbols | 32 | Unseen symbols |
| phase359_official_source_response_rows | 4 | Official source response rows |
| phase359_official_source_ok_rows | 4 | Official source OK rows |
| phase359_official_catalyst_rows | 38 | Official catalyst rows for unseen dates |
| phase359_official_catalyst_symbols | 15 | Official catalyst symbols |
| phase359_no_lookahead_eligible_event_rows | 25 | No-lookahead eligible events with unseen real L2 |
| phase359_no_lookahead_eligible_symbol_dates | 15 | Eligible symbol/date cells |
| phase359_phase360_work_order_rows | 25 | Phase360 work-order rows |
| phase359_full_depth_schema_pass_rows | 36 | Schema pass rows |
| phase359_full_depth_schema_rows | 36 | Schema rows |
| phase359_strategy_promotion_allowed | 0 | No promotion |
| phase359_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase359_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase359_hard_gate_pass_rows | 9 | Passed hard gates |
| phase359_hard_gate_rows | 9 | Hard gates |
| phase359_next_best_action | run_phase360_full_depth_market_neutral_fade_on_unseen_real_l2_no_paper_live | Recommended next milestone |

## Gate evaluation

| gate_id | passed | observed | required |
| --- | --- | --- | --- |
| P359_UNSEEN_LOCAL_DATES_PRESENT | True | 2026-07-17;2026-07-20 | >0 new dates |
| P359_FULL_UNIVERSE_SYMBOLS_PRESENT | True | 32 | >=32 |
| P359_OFFICIAL_NSE_FETCH_ATTEMPTED | True | 4 | >0 |
| P359_OFFICIAL_NSE_FETCH_OK | True | 4 | >0 |
| P359_OFFICIAL_CATALYST_ROWS_PRESENT | True | 38 | >0 |
| P359_NO_LOOKAHEAD_ELIGIBLE_EVENTS_PRESENT | True | 25 | >0 |
| P359_FULL_DEPTH_SCHEMA_PRESENT | True | 36/36 | all |
| P359_PHASE360_WORK_ORDER_PRESENT | True | 25 | >0 |
| P359_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM | True | closed | closed |

## Unseen date inventory

| trade_date | symbols | parquet_files | bytes |
| --- | --- | --- | --- |
| 2026-07-17 | 32 | 50787 | 1788505298 |
| 2026-07-20 | 32 | 50421 | 1773570501 |

## No-lookahead eligible events

| source_id | symbol | announcement_time_ist | announcement_date | market_session | diagnostic_trade_date | diagnostic_start_rule | diagnostic_real_l2_available | description | text | attachment_url | seq_id | no_lookahead_rule_applied |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NSE_CORPORATE_ANNOUNCEMENTS | BPCL | 17-Jul-2026 14:13:29 | 2026-07-17 | regular_session | 2026-07-17 | first_real_tick_after_announcement | 1 | Analysts/Institutional Investor Meet/Con. Call Updates | Bharat Petroleum Corporation Limited has informed the Exchange about Schedule of meet | https://nsearchives.nseindia.com/corporate/BPCL26_17072026141133_stexconcall17072026s.pdf | 106701384 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | BRITANNIA | 17-Jul-2026 00:04:13 | 2026-07-17 | pre_open_or_overnight | 2026-07-17 | market_open_same_day | 1 | Updates | Britannia Industries Limited has informed the Exchange regarding 'Annual Report for FY 2025-26 and Notice of the 107th AGM'. | https://nsearchives.nseindia.com/corporate/BRITANNIA1_17072026000322_Intimation_Signed.pdf | 106700938 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | BRITANNIA | 17-Jul-2026 02:41:00 | 2026-07-17 | pre_open_or_overnight | 2026-07-17 | market_open_same_day | 1 | General Updates | Communication to the Shareholders describing the brief provisions of the Income Tax Act, 2025 and the documents required for Deduction of Tax at Source (TDS) on Final Dividend for the financial year ended 31 March 2026. | https://nsearchives.nseindia.com/corporate/BRITANNIA1_17072026024017_Intimation_Signed.pdf | 106700956 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | SBIN | 17-Jul-2026 10:23:45 | 2026-07-17 | regular_session | 2026-07-17 | first_real_tick_after_announcement | 1 | General Updates | State Bank of India has informed the Exchange about Update on IPO of SBI Funds Management Limited | https://nsearchives.nseindia.com/corporate/SBIN_17072026102320_BSE_NSE_SBIFunds_17072026.pdf | 106701118 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | TECHM | 17-Jul-2026 13:57:27 | 2026-07-17 | regular_session | 2026-07-17 | first_real_tick_after_announcement | 1 | Copy of Newspaper Publication | Tech Mahindra Limited has informed the Exchange about Copy of Newspaper Publication | https://nsearchives.nseindia.com/corporate/TECHM_17072026135714_SEintimationnewpaperadvFR_Q1FY27_.pdf | 106701371 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | AXISBANK | 20-Jul-2026 15:19:45 | 2026-07-20 | regular_session | 2026-07-20 | first_real_tick_after_announcement | 1 | Copy of Newspaper Publication | Axis Bank Limited has informed the Exchange about Copy of Newspaper Publication | https://nsearchives.nseindia.com/corporate/AXISBANK1_20072026151927_Newspaper_PublicationSigned.pdf | 106703402 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | BAJAJ-AUTO | 17-Jul-2026 16:27:40 | 2026-07-17 | post_close | 2026-07-20 | market_open_next_available_unseen_real_l2_day | 1 | Certificate under SEBI (Depositories and Participants) Regulations, 2018 | Bajaj Auto Limited has informed the Exchange about Certificate under SEBI (Depositories and Participants) Regulations, 2018 | https://nsearchives.nseindia.com/corporate/lkwalimbe_bajajauto_co_in_17072026162642_74_5___002_.pdf | 106701591 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | BHARTIARTL | 17-Jul-2026 16:13:26 | 2026-07-17 | post_close | 2026-07-20 | market_open_next_available_unseen_real_l2_day | 1 | Action(s) taken or orders passed | Bharti Airtel Limited has informed the Exchange about Action(s) taken or orders passed. | https://nsearchives.nseindia.com/corporate/BHARTIARTL_17072026161117_Reg30DoTJuly17AP.pdf | 106701559 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | BHARTIARTL | 17-Jul-2026 19:31:45 | 2026-07-17 | post_close | 2026-07-20 | market_open_next_available_unseen_real_l2_day | 1 | Action(s) taken or orders passed | Bharti Airtel Limited has informed the Exchange about Action(s) taken or orders passed. | https://nsearchives.nseindia.com/corporate/BHARTIARTL_17072026193135_Reg30DoTJuly17UPE.pdf | 106702038 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | BRITANNIA | 17-Jul-2026 16:58:52 | 2026-07-17 | post_close | 2026-07-20 | market_open_next_available_unseen_real_l2_day | 1 | Copy of Newspaper Publication | Britannia Industries Limited has informed the Exchange about Copy of Newspaper Publication | https://nsearchives.nseindia.com/corporate/BRITANNIA1_17072026165838_SEIntimation_signed.pdf | 106701684 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | HCLTECH | 17-Jul-2026 18:51:06 | 2026-07-17 | post_close | 2026-07-20 | market_open_next_available_unseen_real_l2_day | 1 | Updates | Release: "HCLTech expands India footprint with Global Technology Center in GIFT City." | https://nsearchives.nseindia.com/corporate/HCLTECH_17072026185033_Release17July2026.pdf | 106701955 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | HCLTECH | 20-Jul-2026 13:16:48 | 2026-07-20 | regular_session | 2026-07-20 | first_real_tick_after_announcement | 1 | Updates | HCL Technologies Limited has informed the Exchange regarding Release:  HCLTech named a Customers  Choice in 2026 Gartner® Peer Insights  Voice of the Customer for Outsourced Digital Workplace Services . | https://nsearchives.nseindia.com/corporate/HCLTECH_20072026131626_Release20July2026.pdf | 106703288 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | ITC | 20-Jul-2026 14:44:43 | 2026-07-20 | regular_session | 2026-07-20 | first_real_tick_after_announcement | 1 | Copy of Newspaper Publication | ITC Limited has informed the Exchange about Copy of Newspaper Publication | https://nsearchives.nseindia.com/corporate/ITC_20072026144416_SELetter.pdf | 106703368 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | LT | 17-Jul-2026 17:00:01 | 2026-07-17 | post_close | 2026-07-20 | market_open_next_available_unseen_real_l2_day | 1 | Analysts/Institutional Investor Meet/Con. Call Updates | Larsen & Toubro Limited has informed the Exchange about Schedule of meet | https://nsearchives.nseindia.com/corporate/PAM_17072026165939_Intimation17072026.pdf | 106701686 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | LT | 20-Jul-2026 09:09:48 | 2026-07-20 | pre_open_or_overnight | 2026-07-20 | market_open_same_day | 1 | Bagging/Receiving of orders/contracts | Larsen & Toubro Limited has informed the Exchange about Bagging/Receiving of orders/contracts | https://nsearchives.nseindia.com/corporate/PAM_20072026090928_PressRelease20072026.pdf | 106702971 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | ONGC | 17-Jul-2026 18:35:05 | 2026-07-17 | post_close | 2026-07-20 | market_open_next_available_unseen_real_l2_day | 1 | Press Release | Oil & Natural Gas Corporation Limited has informed the Exchange regarding a press release dated July 17, 2026, titled "Hon ble Lieutenant Governor of Ladakh Marks ONGC s Landmark Completion of Two Deep Geothermal Wells at Puga". | https://nsearchives.nseindia.com/corporate/ONGC_17072026183328_PressRelease17072026.pdf | 106701922 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | RELIANCE | 17-Jul-2026 19:07:44 | 2026-07-17 | post_close | 2026-07-20 | market_open_next_available_unseen_real_l2_day | 1 | Outcome of Board Meeting | Please find attached Consolidated and Standalone unaudited financial results for the quarter ended June 30, 2026. | https://nsearchives.nseindia.com/corporate/kavinavora_17072026190726_SE_FR_1.pdf | 106701986 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | RELIANCE | 17-Jul-2026 19:19:47 | 2026-07-17 | post_close | 2026-07-20 | market_open_next_available_unseen_real_l2_day | 1 | Press Release | In continuation of our letter of today''s date on the Consolidated and Standalone Unaudited Financial Results for the quarter ended June 30, 2026, we attach a copy of media release being issued by the Company | https://nsearchives.nseindia.com/corporate/kavinavora_17072026191923_SE_MR_1.pdf | 106702014 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | RELIANCE | 17-Jul-2026 19:23:12 | 2026-07-17 | post_close | 2026-07-20 | market_open_next_available_unseen_real_l2_day | 1 | Investor Presentation | Reliance Industries Limited has informed the Exchange about Investor Presentation | https://nsearchives.nseindia.com/corporate/kavinavora_17072026192250_SE_Presentation_1.pdf | 106702019 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | ULTRACEMCO | 20-Jul-2026 14:22:16 | 2026-07-20 | regular_session | 2026-07-20 | first_real_tick_after_announcement | 1 | Outcome of Board Meeting | UltraTech Cement Limited has submitted to the Exchange, the financial results for the period ended June 30, 2026. | https://nsearchives.nseindia.com/corporate/ULTRACEMCO1_20072026142206_Outcome_of_BM.pdf | 106703342 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | ULTRACEMCO | 20-Jul-2026 14:26:28 | 2026-07-20 | regular_session | 2026-07-20 | first_real_tick_after_announcement | 1 | Investor Presentation | UltraTech Cement Limited has informed the Exchange about Investor Presentation | https://nsearchives.nseindia.com/corporate/ULTRACEMCO1_20072026142500_SEinvestorpresentation.pdf | 106703346 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | ULTRACEMCO | 20-Jul-2026 14:28:05 | 2026-07-20 | regular_session | 2026-07-20 | first_real_tick_after_announcement | 1 | Press Release | UltraTech Cement Limited has informed the Exchange regarding a press release dated July 20, 2026, titled "Quarter ended 30th June, 2026". | https://nsearchives.nseindia.com/corporate/ULTRACEMCO1_20072026142756_Outcome_of_BM.pdf | 106703351 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | ULTRACEMCO | 20-Jul-2026 14:42:09 | 2026-07-20 | regular_session | 2026-07-20 | first_real_tick_after_announcement | 1 | Appointment | UltraTech Cement Limited has informed the Exchange regarding re-appointment of  Mr. Vivek Agrawal as Whole-time Director and Chief Marketing Officer of the company w.e.f. January 01, 2027. | https://nsearchives.nseindia.com/corporate/ULTRACEMCO1_20072026144153_SEIntimation_WTD_re-appointment.pdf | 106703362 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | WIPRO | 17-Jul-2026 16:12:41 | 2026-07-17 | post_close | 2026-07-20 | market_open_next_available_unseen_real_l2_day | 1 | Copy of Newspaper Publication | Wipro Limited has informed the Exchange about Newspaper Advertisement - Regulation 47 of SEBI (Listing Obligations and Disclosure Requirements) Regulations, 2015 | https://nsearchives.nseindia.com/corporate/Cslogin_17072026161225_Reg47NewspaperAd.pdf | 106701555 | 1 |
| NSE_CORPORATE_ANNOUNCEMENTS | WIPRO | 17-Jul-2026 16:30:50 | 2026-07-17 | post_close | 2026-07-20 | market_open_next_available_unseen_real_l2_day | 1 | Analysts/Institutional Investor Meet/Con. Call Updates | Wipro Limited has informed the Exchange about Transcript of the Analyst / Institutional Investor Meeting held on July 16, 2026. | https://nsearchives.nseindia.com/corporate/Cslogin_17072026162727_SEIntimation17072026.pdf | 106701598 | 1 |

No promotion, paper/live acceptance, or deployable profitability claim is opened.
