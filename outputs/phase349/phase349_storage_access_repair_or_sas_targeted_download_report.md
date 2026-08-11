# Phase349 Storage Access Repair Or SAS Targeted Download Precommit

Generated: 2026-08-11T08:56:35.759565+00:00

Phase349 converts the Phase348 storage-access block into a safe repair and targeted-download contract. It does not store secrets and does not execute a download.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase349_storage_access_repair_or_sas_targeted_download_precommit_complete | 1 | Phase349 precommit completed |
| phase349_phase348_attempted | 1 | Phase348 attempted |
| phase349_sas_env_inputs_present | 0 | Any supported SAS environment input present |
| phase349_repair_option_rows | 4 | Storage repair options |
| phase349_phase350_contract_rows | 12 | Phase350 execution contract rows |
| phase349_command_contract_rows | 3 | Safe command contract rows |
| phase349_candidate_grid_rows | 10 | Candidate grid rows |
| phase349_secret_material_recorded | 0 | No secret material recorded |
| phase349_strategy_promotion_allowed | 0 | No promotion |
| phase349_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase349_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase349_hard_gate_pass_rows | 7 | Passed hard gates |
| phase349_hard_gate_rows | 7 | Hard gates |
| phase349_next_best_action | provide_sas_or_install_azcopy_then_run_phase350_targeted_download_no_paper_live | Recommended next action |

## SAS environment input inventory

| input_name | present | secret_value_recorded | use |
| --- | --- | --- | --- |
| AZURE_STORAGE_SAS_TOKEN | 0 | 0 | Phase350 may consume this in-memory environment variable; Phase349 never writes the value. |
| AZURE_BLOB_SERVICE_SAS_URL | 0 | 0 | Phase350 may consume this in-memory environment variable; Phase349 never writes the value. |
| STCTRADE1RAMIC_BLOB_SAS_URL | 0 | 0 | Phase350 may consume this in-memory environment variable; Phase349 never writes the value. |
| STCTRADE1RAMIC_SAS_TOKEN | 0 | 0 | Phase350 may consume this in-memory environment variable; Phase349 never writes the value. |

## Repair options

| repair_option_id | priority | route | action | why | ready_now | secret_material_recorded |
| --- | --- | --- | --- | --- | --- | --- |
| P349_OPT_001_USE_FRESH_BLOB_SAS_ENV | 1 | sas_https_without_az_login | Provide a fresh blob service SAS URL or SAS token via an environment variable, then run Phase350 targeted one-date download. | Bypasses the local Azure CLI TLS token-refresh failure and avoids storing secrets in repo outputs. | 0 | 0 |
| P349_OPT_002_INSTALL_OR_PROVIDE_AZCOPY | 2 | azcopy_with_sas | Install azcopy or add it to PATH, then use SAS-protected URLs for targeted partition copies. | AzCopy is better for resumable targeted Azure Blob/File downloads when storage access is SAS-based. | 0 | 0 |
| P349_OPT_003_REPAIR_AZURE_CLI_CA_CHAIN | 3 | az_cli_auth_mode_login | Repair Azure CLI certificate trust or configure the proxy CA bundle, then retry az storage listing/download. | Current az login-mode route fails on certificate verification before storage listing can proceed. | 0 | 0 |
| P349_OPT_004_LOCAL_DROPZONE_ONE_DATE | 4 | manual_local_drop | Drop one official-catalyst-matched date partition into the local real L2 panel, then run Phase350 local verification. | Works when cloud access cannot be repaired immediately and disk space is tight. | 0 | 0 |

## Phase350 execution contract

| contract_id | contract_value | description |
| --- | --- | --- |
| phase350_scope | targeted_one_new_official_catalyst_matched_date | Download or verify only one new date increment. |
| target_symbols | ADANIPORTS;AXISBANK;BHARTIARTL;DRREDDY;HCLTECH;HDFCBANK;ICICIBANK;KOTAKBANK;M&M;RELIANCE;SBIN;TCS | Candidate symbols from Phase347; do not download unrelated full panel. |
| max_new_dates_per_increment | 1 | Disk-aware increment size. |
| target_partition_shape | raw_l2/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | Expected Zerodha-websocket-like raw top-five L2 partition shape. |
| full_top_five_depth_required | 1 | Persist bid/ask price, quantity and order-count levels 1-5. |
| levels_2_to_5_materiality_required | 1 | Do not reduce to L1-only features. |
| official_catalyst_timestamp_authority_required | 1 | Use official NSE/BSE/SEBI-style timestamp authority. |
| no_lookahead_join_required | 1 | Entry/replay time must be first tick at or after official announcement time. |
| candidate_grid_rows | 10 | Rerun only Phase347 candidate grid rows after expansion. |
| additional_candidate_trade_rows_needed | 11 | Minimum additional candidate rows before acceptance re-evaluation. |
| paper_live_or_profit_claim_allowed | 0 | No paper/live or deployable profitability claim. |
| secret_persistence_allowed | 0 | Do not write SAS, connection strings, account keys or signed URLs to repo outputs. |

## Safe command contract

| command_id | shell | template | safe_logging | secret_material_recorded |
| --- | --- | --- | --- | --- |
| P349_CMD_001_SET_SAS_IN_PROCESS | PowerShell | $env:AZURE_BLOB_SERVICE_SAS_URL='<paste fresh blob service SAS URL only in your local shell>'; python scripts\run_phase350_sas_targeted_one_date_download.py | Do not echo the environment variable; Phase350 must redact signed URLs. | 0 |
| P349_CMD_002_SET_TOKEN_IN_PROCESS | PowerShell | $env:AZURE_STORAGE_SAS_TOKEN='<paste fresh SAS token only in your local shell>'; python scripts\run_phase350_sas_targeted_one_date_download.py | Do not echo the environment variable; Phase350 must redact signed URLs. | 0 |
| P349_CMD_003_LOCAL_DROP_VERIFY | PowerShell | python scripts\run_phase350_sas_targeted_one_date_download.py --local-only-verify | Use only after manually dropping a new trade_date=YYYY-MM-DD partition. | 0 |

No paper/live acceptance or profitability claim is opened.