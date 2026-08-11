# Phase372 SAS One-Day 2026-07-21 Downloader

Generated: 2026-08-11T18:29:49.995506+00:00

Phase372 is the target-specific full-universe downloader/verifier harness for the Phase370/371 `2026-07-21` real L2 target. It reads SAS only from environment variables, writes no signed URLs or tokens, and does not run a strategy retest.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase372_sas_one_day_20260721_downloader_complete | 1 | Phase372 complete if all hard gates pass |
| phase372_target_trade_date | 2026-07-21 | Target date |
| phase372_sas_env_present | 1 | Supported SAS env present |
| phase372_truststore_injected | 1 | Truststore injected before HTTPS calls |
| phase372_dry_run | 0 | Dry-run mode |
| phase372_max_files | 0 | Max files; 0 means all target files |
| phase372_workers | 96 | Concurrent workers for Azure File downloads |
| phase372_discovered_blob_rows | 50187 | Discovered target blob rows |
| phase372_discovered_symbols | 32 | Discovered target symbols |
| phase372_download_manifest_rows | 50187 | Download manifest rows |
| phase372_downloaded_file_rows | 18 | Downloaded file rows |
| phase372_local_symbols_before | 32 | Local symbols before |
| phase372_local_symbols_after | 32 | Local symbols after |
| phase372_local_full_universe_after | 1 | Full universe local after |
| phase372_secret_material_recorded | 0 | No secret material should be recorded |
| phase372_strategy_promotion_allowed | 0 | No promotion |
| phase372_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase372_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase372_hard_gate_pass_rows | 6 | Passed hard gates |
| phase372_hard_gate_rows | 6 | Hard gates |
| phase372_next_best_action | rerun_phase370_one_day_real_l2_drop_verifier_no_paper_live | Recommended next milestone |

## Access ledger

| access_route | available | result | evidence | secret_material_recorded |
| --- | --- | --- | --- | --- |
| file_sas_env | 1 | file_sas_discovery_attempted | env=AZURE_FILE_SERVICE_SAS_URL;shares_checked=1;rows=50187 | 0 |

## Discovery manifest sample

| trade_date | exchange | symbol | relative_file | share | file_path_redacted |
| --- | --- | --- | --- | --- | --- |
| 2026-07-21 | NSE | ADANIPORTS | part-034500_914265-000001.parquet | ctrade1-l2-data | raw_l2/trade_date=2026-07-21/exchange=NSE/symbol=ADANIPORTS/part-REDACTED.parquet |
| 2026-07-21 | NSE | ADANIPORTS | part-034515_360270-000033.parquet | ctrade1-l2-data | raw_l2/trade_date=2026-07-21/exchange=NSE/symbol=ADANIPORTS/part-REDACTED.parquet |
| 2026-07-21 | NSE | ADANIPORTS | part-034529_361550-000065.parquet | ctrade1-l2-data | raw_l2/trade_date=2026-07-21/exchange=NSE/symbol=ADANIPORTS/part-REDACTED.parquet |
| 2026-07-21 | NSE | ADANIPORTS | part-034543_110506-000097.parquet | ctrade1-l2-data | raw_l2/trade_date=2026-07-21/exchange=NSE/symbol=ADANIPORTS/part-REDACTED.parquet |
| 2026-07-21 | NSE | ADANIPORTS | part-034556_863825-000129.parquet | ctrade1-l2-data | raw_l2/trade_date=2026-07-21/exchange=NSE/symbol=ADANIPORTS/part-REDACTED.parquet |
| 2026-07-21 | NSE | ADANIPORTS | part-034610_614537-000161.parquet | ctrade1-l2-data | raw_l2/trade_date=2026-07-21/exchange=NSE/symbol=ADANIPORTS/part-REDACTED.parquet |
| 2026-07-21 | NSE | ADANIPORTS | part-034624_116830-000193.parquet | ctrade1-l2-data | raw_l2/trade_date=2026-07-21/exchange=NSE/symbol=ADANIPORTS/part-REDACTED.parquet |
| 2026-07-21 | NSE | ADANIPORTS | part-034637_869268-000225.parquet | ctrade1-l2-data | raw_l2/trade_date=2026-07-21/exchange=NSE/symbol=ADANIPORTS/part-REDACTED.parquet |
| 2026-07-21 | NSE | ADANIPORTS | part-034651_612583-000257.parquet | ctrade1-l2-data | raw_l2/trade_date=2026-07-21/exchange=NSE/symbol=ADANIPORTS/part-REDACTED.parquet |
| 2026-07-21 | NSE | ADANIPORTS | part-034705_115157-000289.parquet | ctrade1-l2-data | raw_l2/trade_date=2026-07-21/exchange=NSE/symbol=ADANIPORTS/part-REDACTED.parquet |
| 2026-07-21 | NSE | ADANIPORTS | part-034718_864470-000321.parquet | ctrade1-l2-data | raw_l2/trade_date=2026-07-21/exchange=NSE/symbol=ADANIPORTS/part-REDACTED.parquet |
| 2026-07-21 | NSE | ADANIPORTS | part-034732_613260-000353.parquet | ctrade1-l2-data | raw_l2/trade_date=2026-07-21/exchange=NSE/symbol=ADANIPORTS/part-REDACTED.parquet |
| 2026-07-21 | NSE | ADANIPORTS | part-034746_368815-000385.parquet | ctrade1-l2-data | raw_l2/trade_date=2026-07-21/exchange=NSE/symbol=ADANIPORTS/part-REDACTED.parquet |
| 2026-07-21 | NSE | ADANIPORTS | part-034800_112778-000417.parquet | ctrade1-l2-data | raw_l2/trade_date=2026-07-21/exchange=NSE/symbol=ADANIPORTS/part-REDACTED.parquet |
| 2026-07-21 | NSE | ADANIPORTS | part-034813_863908-000449.parquet | ctrade1-l2-data | raw_l2/trade_date=2026-07-21/exchange=NSE/symbol=ADANIPORTS/part-REDACTED.parquet |
| 2026-07-21 | NSE | ADANIPORTS | part-034827_615359-000481.parquet | ctrade1-l2-data | raw_l2/trade_date=2026-07-21/exchange=NSE/symbol=ADANIPORTS/part-REDACTED.parquet |
| 2026-07-21 | NSE | ADANIPORTS | part-034841_364268-000513.parquet | ctrade1-l2-data | raw_l2/trade_date=2026-07-21/exchange=NSE/symbol=ADANIPORTS/part-REDACTED.parquet |
| 2026-07-21 | NSE | ADANIPORTS | part-034854_864630-000545.parquet | ctrade1-l2-data | raw_l2/trade_date=2026-07-21/exchange=NSE/symbol=ADANIPORTS/part-REDACTED.parquet |
| 2026-07-21 | NSE | ADANIPORTS | part-034908_612502-000577.parquet | ctrade1-l2-data | raw_l2/trade_date=2026-07-21/exchange=NSE/symbol=ADANIPORTS/part-REDACTED.parquet |
| 2026-07-21 | NSE | ADANIPORTS | part-034922_363190-000609.parquet | ctrade1-l2-data | raw_l2/trade_date=2026-07-21/exchange=NSE/symbol=ADANIPORTS/part-REDACTED.parquet |

## Local inventory after

| trade_date | symbol | parquet_files | bytes |
| --- | --- | --- | --- |
| 2026-07-21 | ADANIPORTS | 1569 | 54573121 |
| 2026-07-21 | AXISBANK | 1568 | 56459562 |
| 2026-07-21 | BAJAJ-AUTO | 1568 | 55799875 |
| 2026-07-21 | BANKBEES | 1569 | 54922511 |
| 2026-07-21 | BHARTIARTL | 1568 | 55069104 |
| 2026-07-21 | BPCL | 1569 | 54310835 |
| 2026-07-21 | BRITANNIA | 1568 | 54058239 |
| 2026-07-21 | CIPLA | 1569 | 54734233 |
| 2026-07-21 | DRREDDY | 1569 | 54707905 |
| 2026-07-21 | GOLDBEES | 1568 | 54471274 |
| 2026-07-21 | HCLTECH | 1568 | 55018761 |
| 2026-07-21 | HDFCBANK | 1568 | 56478251 |
| 2026-07-21 | HINDUNILVR | 1568 | 54619961 |
| 2026-07-21 | ICICIBANK | 1568 | 56292144 |
| 2026-07-21 | INFY | 1568 | 56155639 |
| 2026-07-21 | ITBEES | 1569 | 54115847 |
| 2026-07-21 | ITC | 1569 | 55708762 |
| 2026-07-21 | JUNIORBEES | 1568 | 54910416 |
| 2026-07-21 | KOTAKBANK | 1568 | 55409892 |
| 2026-07-21 | LT | 1569 | 55004117 |
| 2026-07-21 | M&M | 1568 | 55363512 |
| 2026-07-21 | MARUTI | 1568 | 55175825 |
| 2026-07-21 | NESTLEIND | 1568 | 54501837 |
| 2026-07-21 | NIFTYBEES | 1568 | 54633121 |
| 2026-07-21 | ONGC | 1569 | 54869558 |
| 2026-07-21 | RELIANCE | 1568 | 55627621 |
| 2026-07-21 | SBIN | 1568 | 55654096 |
| 2026-07-21 | SUNPHARMA | 1568 | 54790362 |
| 2026-07-21 | TCS | 1569 | 55444595 |
| 2026-07-21 | TECHM | 1569 | 54915825 |
| 2026-07-21 | ULTRACEMCO | 1568 | 55304186 |
| 2026-07-21 | WIPRO | 1568 | 54671581 |

## Gate evaluation

| gate_id | passed | evidence |
| --- | --- | --- |
| P372_PHASE371_TARGET_PRESENT | 1 | 2026-07-21 |
| P372_FULL_UNIVERSE_SYMBOL_CONTRACT | 1 | symbols=32 |
| P372_SAS_ENV_OR_SAFE_WAIT | 1 | sas_present=1 |
| P372_DISCOVERY_OR_WAIT_RECORDED | 1 | discovered_rows=50187; error_recorded=0 |
| P372_NO_SECRET_MATERIAL_RECORDED | 1 | secret_rows=0 |
| P372_NO_STRATEGY_RETEST_OR_PROMOTION | 1 | download_only |

No promotion, paper/live acceptance, or deployable profitability claim is opened.
