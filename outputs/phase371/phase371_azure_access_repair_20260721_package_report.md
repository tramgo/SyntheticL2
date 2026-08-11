# Phase371 Azure Access Repair and 2026-07-21 Download Package

Generated: 2026-08-11T17:28:30.774106+00:00

Phase371 probes current non-secret access state and emits a safe command package for the Phase370 one-day target. It does not download data, persist secrets, run a strategy retest, or open promotion/paper/live claims.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase371_azure_access_repair_20260721_package_complete | 1 | Phase371 complete if all hard gates pass |
| phase371_target_trade_date | 2026-07-21 | Target date |
| phase371_known_carry_forward_event_rows | 13 | Known events unlocked by target date |
| phase371_az_cli_present | 1 | Azure CLI present |
| phase371_az_account_context_available | 1 | Azure account context available |
| phase371_az_storage_login_list_available | 0 | Azure storage login-mode list available |
| phase371_az_cli_certificate_failure | 1 | Certificate failure observed |
| phase371_azcopy_present | 0 | AzCopy present on PATH |
| phase371_supported_sas_env_present | 0 | Supported SAS env present |
| phase371_target_local_full_universe_present | 0 | Target full-universe already local |
| phase371_direct_download_route_available_now | 0 | SAS or login-mode storage listing available now |
| phase371_any_route_available_now | 0 | Direct, azcopy, or local target route available now |
| phase371_secret_material_recorded | 0 | No secret material recorded |
| phase371_strategy_promotion_allowed | 0 | No promotion |
| phase371_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase371_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase371_hard_gate_pass_rows | 6 | Passed hard gates |
| phase371_hard_gate_rows | 6 | Hard gates |
| phase371_next_best_action | download_or_local_drop_full_universe_real_l2_for_2026-07-21_then_rerun_phase370_verify_no_paper_live | Recommended next milestone |

## Access probe ledger

| probe_id | available | result | evidence | secret_material_recorded |
| --- | --- | --- | --- | --- |
| P371_AZ_CLI_PRESENT | 1 | az_on_path | version probe omitted from artifact; command availability only | 0 |
| P371_AZ_ACCOUNT_CONTEXT | 1 | account_context_available | {   "tenantId": "bfbf2bf5-10dc-4b2a-9000-b5487375c998" }  | 0 |
| P371_AZ_STORAGE_LOGIN_LIST | 0 | azure_cli_certificate_failure | WARNING: Connection verification disabled by environment variable AZURE_CLI_DISABLE_CONNECTION_VERIFICATION ERROR: HTTPSConnectionPool(host='login.microsoftonline.com', port=443): Max retries exceeded with url: /bfbf2bf5-10dc-4b2a-9000-b5487375c998/oauth2/v2.0/token (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1032)'))) Certificate verification failed. This typically happens when using  | 0 |
| P371_AZCOPY_PRESENT | 0 | azcopy_not_on_path | azcopy command was not found on PATH | 0 |
| P371_SUPPORTED_SAS_ENV_PRESENT | 0 | sas_env_absent | supported_env_names_present=0 | 0 |
| P371_TARGET_LOCAL_ALREADY_VERIFIED | 0 | target_full_universe_absent | target_trade_date=2026-07-21 | 0 |

## Safe command catalog

| command_id | priority | shell | command_template | safe_logging | secret_material_recorded |
| --- | --- | --- | --- | --- | --- |
| P371_CMD_001_SAS_ENV_THEN_PHASE350_OR_CUSTOM_DOWNLOAD | 1 | PowerShell | $env:AZURE_BLOB_SERVICE_SAS_URL='<paste fresh blob service SAS URL only in this shell>'; python scripts\run_phase371_azure_access_repair_20260721_package.py | Do not echo the env var; Phase371 records presence only. | 0 |
| P371_CMD_002_AZCOPY_ONE_DAY_TEMPLATE | 2 | PowerShell | azcopy copy 'https://stctrade1ramic.blob.core.windows.net/<container>/raw_l2/trade_date=2026-07-21/exchange=NSE?<SAS>' 'real_data_sample/l2_unseen_validation/trade_date=2026-07-21/exchange=NSE' --recursive=true | Use only with SAS in your shell/history discipline; do not commit signed URLs. | 0 |
| P371_CMD_003_LOCAL_DROP_VERIFY | 3 | PowerShell | Copy one local full-universe partition into real_data_sample\l2_unseen_validation\trade_date=2026-07-21\exchange=NSE\symbol=<SYMBOL>\*.parquet, then run: python scripts\run_phase370_one_day_real_l2_drop_verifier.py | No secrets required; verifier checks local files only. | 0 |
| P371_CMD_004_REPAIR_AZ_CLI_CA | 4 | PowerShell | Repair corporate/root CA bundle for Azure CLI token refresh, then retry: az storage container list --account-name stctrade1ramic --auth-mode login -o table | Read-only list command; no secret output expected. | 0 |

## 2026-07-21 verification contract

| contract_id | contract_value | requirement |
| --- | --- | --- |
| P371_TARGET_DATE | 2026-07-21 | Next one-day full-universe L2 target selected by Phase370. |
| P371_REQUIRED_SYMBOLS | 32 | All project symbols must be present for full-universe verification. |
| P371_EXPECTED_LOCAL_SHAPE | real_data_sample/l2_unseen_validation/trade_date=2026-07-21/exchange=NSE/symbol=SYMBOL/*.parquet | Local drop/download target consumed by Phase370 verifier. |
| P371_KNOWN_CARRY_FORWARD_EVENTS | 13 | Known 2026-07-20 post-close official catalyst rows unlocked by 2026-07-21 L2. |
| P371_AFTER_DROP_VERIFY_COMMAND | python scripts/run_phase370_one_day_real_l2_drop_verifier.py | Rerun local verifier before any strategy retest. |

## Gate evaluation

| gate_id | passed | evidence |
| --- | --- | --- |
| P371_PHASE370_TARGET_PRESENT | 1 | 2026-07-21 |
| P371_AZURE_ACCESS_PROBED | 1 | az_present=1; account_probe=1; storage_probe=0 |
| P371_DOWNLOAD_ROUTE_CLASSIFIED | 1 | direct_download_available=0; local_drop_available=1 |
| P371_SAFE_COMMAND_PACKAGE_WRITTEN | 1 | commands=4 |
| P371_NO_SECRET_MATERIAL_RECORDED | 1 | secret_rows=0 |
| P371_NO_STRATEGY_RETEST_OR_PROMOTION | 1 | download_package_only |

Phase371 decision: current login-mode Azure storage access remains unavailable because the storage list probe fails; no supported SAS env var is present and AzCopy is not on PATH. The next executable path is a fresh in-process SAS or a manual local drop for the full-universe 2026-07-21 partition, followed by Phase370 verification.

No promotion, paper/live acceptance, or deployable profitability claim is opened.
