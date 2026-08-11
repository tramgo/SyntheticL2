# Phase350 SAS Targeted One-Date Download

Generated: 2026-08-11T09:03:18.943959+00:00

Phase350 safely attempts a one-date targeted official-catalyst L2 download. SAS values and signed URLs are never written to outputs.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase350_sas_targeted_one_date_download_attempted | 1 | Phase350 attempted |
| phase350_phase349_complete | 1 | Phase349 complete |
| phase350_sas_env_present | 0 | Supported SAS env var present |
| phase350_local_only_verify | 0 | Local-only verify mode |
| phase350_dry_run | 0 | Dry-run mode |
| phase350_candidate_symbol_rows | 12 | Candidate symbol rows |
| phase350_existing_local_dates_before | 7 | Local real L2 dates before |
| phase350_target_trade_date |  | Selected target trade date |
| phase350_download_manifest_rows | 0 | Download manifest rows |
| phase350_downloaded_file_rows | 0 | Downloaded file rows |
| phase350_new_real_l2_dates_added | 0 | New local real L2 dates added |
| phase350_secret_material_recorded | 0 | No secret material recorded |
| phase350_strategy_promotion_allowed | 0 | No promotion |
| phase350_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase350_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase350_hard_gate_pass_rows | 4 | Passed hard gates |
| phase350_hard_gate_rows | 6 | Hard gates |
| phase350_next_best_action | set_fresh_blob_sas_env_or_local_drop_then_rerun_phase350_no_paper_live | Recommended next action |

## Access ledger

| access_route | available | evidence | secret_material_recorded |
| --- | --- | --- | --- |
| sas_env | 0 | no supported SAS env var present | 0 |

## Download manifest

_No rows._

## Gate evaluation

| gate_id | passed | observed | required |
| --- | --- | --- | --- |
| P350_PHASE349_COMPLETE | True | 1 | 1 |
| P350_SECRET_INPUT_NOT_PERSISTED | True | not_recorded | not_recorded |
| P350_SAS_OR_LOCAL_VERIFY_ROUTE_AVAILABLE | False | 0 | 1 |
| P350_TARGET_DATE_DISCOVERED_OR_LOCAL_VERIFY | False |  | target_date |
| P350_DOWNLOAD_EXECUTED_OR_SAFE_WAIT | True | downloaded_rows=0;dry_run=0;sas_present=0 | safe |
| P350_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM | True | closed | closed |