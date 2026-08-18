# Phase478 Real Expansion Reconciliation After Phase477

Phase478 reconciles the rejected synthetic Phase477 diagnostic with prior unseen real-L2 evidence and selects the next real-data expansion action.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase478_real_expansion_reconciliation_complete | 1 | Phase478 complete if all gates pass |
| phase478_thesis_id | P478_REAL_EXPANSION_RECONCILIATION_AFTER_PHASE477 | Phase478 thesis |
| phase478_local_real_l2_file_rows | 199513 | Local real L2 parquet files found |
| phase478_local_real_l2_date_rows | 4 | Local dated real L2 dates found |
| phase478_supported_sas_env_present | 0 | SAS env available |
| phase478_az_account_available | 1 | Azure account probe success |
| phase478_az_storage_list_available | 0 | Azure storage list success |
| phase478_strategy_promotion_allowed | 0 | No promotion |
| phase478_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase478_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase478_phase479_allowed_next | 1 | Allows repair/download precommit only |
| phase478_hard_gate_pass_rows | 9 | Passed hard gates |
| phase478_hard_gate_rows | 9 | Hard gates |
| phase478_next_best_action | repair_azure_cli_tls_or_provide_fresh_sas_then_download_one_disk_safe_official_catalyst_l2_day | Recommended next action |

## Branch Reconciliation

| branch_id | evidence_source | status | net_pnl_inr | annualized_return_pct | trade_rows | acceptance_allowed | next_use |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P477_SYNTHETIC_COMBINED_SHOCK_MARKET_CONTEXT_L2_FADE | outputs/phase477 | rejected | -360.106 | -45.3733 | 10 | 0 | negative_control_only |
| P360_UNSEEN_REAL_FULL_DEPTH_MARKET_NEUTRAL_FADE | outputs/phase360 | unseen_real_failed | -939.536 | -47.3526 | 5 | 0 | requires_more_real_dates_or_close |
| P369_REAL_DATE_EXPANSION_READINESS | outputs/phase369 | data_expansion_required | 0 | 0 | 12 | 0 | download_or_local_drop_one_disk_safe_day |

## Access Probe

| probe_id | available | evidence | secret_material_recorded |
| --- | --- | --- | --- |
| supported_sas_env_present | 0 | present_count=0; names_redacted= | 0 |
| az_account_show | 1 | {
  "name": "Visual Studio Enterprise Subscription",
  "tenantId": "bfbf2bf5-10dc-4b2a-9000-b5487375c998",
  "user": "ramagovindaraja.thiruvadi@citi.com"
} | 0 |
| az_storage_container_list_login | 0 | ERROR: HTTPSConnectionPool(host='login.microsoftonline.com', port=443): Max retries exceeded with url: /bfbf2bf5-10dc-4b2a-9000-b5487375c998/v2.0/.well-known/openid-configuration (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1032)'))) | 0 |

## Local Real L2 Inventory Sample

| root | path | trade_date | symbol | bytes |
| --- | --- | --- | --- | --- |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034501_461115-000006.parquet |  | ADANIPORTS | 34112 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034515_232603-000033.parquet |  | ADANIPORTS | 34212 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034529_231528-000065.parquet |  | ADANIPORTS | 34472 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034543_231400-000097.parquet |  | ADANIPORTS | 34437 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034557_482643-000129.parquet |  | ADANIPORTS | 34470 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034611_479693-000161.parquet |  | ADANIPORTS | 34512 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034625_480672-000193.parquet |  | ADANIPORTS | 34495 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034639_483870-000225.parquet |  | ADANIPORTS | 34548 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034653_480389-000257.parquet |  | ADANIPORTS | 34458 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034707_481783-000289.parquet |  | ADANIPORTS | 35373 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034721_980155-000321.parquet |  | ADANIPORTS | 36251 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034735_981274-000353.parquet |  | ADANIPORTS | 36284 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034750_229849-000385.parquet |  | ADANIPORTS | 36103 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034804_227127-000417.parquet |  | ADANIPORTS | 35666 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034818_230261-000449.parquet |  | ADANIPORTS | 34494 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034832_227665-000481.parquet |  | ADANIPORTS | 34493 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034846_477541-000513.parquet |  | ADANIPORTS | 34511 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034900_478354-000545.parquet |  | ADANIPORTS | 34703 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034914_479080-000577.parquet |  | ADANIPORTS | 36083 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034928_731007-000609.parquet |  | ADANIPORTS | 35951 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034942_979559-000641.parquet |  | ADANIPORTS | 36053 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034957_231624-000673.parquet |  | ADANIPORTS | 36076 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035011_478207-000705.parquet |  | ADANIPORTS | 34692 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035025_495713-000737.parquet |  | ADANIPORTS | 34656 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035039_738678-000769.parquet |  | ADANIPORTS | 34457 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035054_230514-000801.parquet |  | ADANIPORTS | 34756 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035108_480289-000833.parquet |  | ADANIPORTS | 34155 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035122_732362-000865.parquet |  | ADANIPORTS | 34467 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035137_230061-000897.parquet |  | ADANIPORTS | 34448 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035151_481390-000929.parquet |  | ADANIPORTS | 34698 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035206_235457-000961.parquet |  | ADANIPORTS | 35407 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035220_233434-000993.parquet |  | ADANIPORTS | 36041 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035234_737155-001025.parquet |  | ADANIPORTS | 36016 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035249_232163-001057.parquet |  | ADANIPORTS | 36008 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035303_984955-001089.parquet |  | ADANIPORTS | 36021 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035318_233173-001121.parquet |  | ADANIPORTS | 34173 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035332_982798-001153.parquet |  | ADANIPORTS | 34536 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035347_984333-001185.parquet |  | ADANIPORTS | 34471 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035402_731867-001217.parquet |  | ADANIPORTS | 35325 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035417_483044-001249.parquet |  | ADANIPORTS | 36054 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035431_731495-001281.parquet |  | ADANIPORTS | 35930 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035446_235988-001313.parquet |  | ADANIPORTS | 36031 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035500_733284-001345.parquet |  | ADANIPORTS | 36241 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035515_481896-001377.parquet |  | ADANIPORTS | 36213 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035529_730921-001409.parquet |  | ADANIPORTS | 36052 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035543_985028-001441.parquet |  | ADANIPORTS | 35973 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035557_981634-001473.parquet |  | ADANIPORTS | 35832 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035612_481566-001505.parquet |  | ADANIPORTS | 35745 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035626_733834-001537.parquet |  | ADANIPORTS | 35573 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035640_980021-001569.parquet |  | ADANIPORTS | 35210 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035654_982313-001601.parquet |  | ADANIPORTS | 35664 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035708_979853-001633.parquet |  | ADANIPORTS | 35002 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035723_229871-001665.parquet |  | ADANIPORTS | 34484 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035737_228886-001697.parquet |  | ADANIPORTS | 34635 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035751_230127-001729.parquet |  | ADANIPORTS | 34448 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035805_482891-001761.parquet |  | ADANIPORTS | 34523 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035819_730624-001793.parquet |  | ADANIPORTS | 34492 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035833_731320-001825.parquet |  | ADANIPORTS | 34593 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035847_730797-001857.parquet |  | ADANIPORTS | 34745 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035901_734269-001889.parquet |  | ADANIPORTS | 34707 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035915_730479-001921.parquet |  | ADANIPORTS | 35886 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035929_981693-001953.parquet |  | ADANIPORTS | 35866 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035944_235704-001985.parquet |  | ADANIPORTS | 35594 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-035958_479197-002017.parquet |  | ADANIPORTS | 35440 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040012_980756-002049.parquet |  | ADANIPORTS | 34795 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040027_737410-002081.parquet |  | ADANIPORTS | 34507 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040041_983563-002113.parquet |  | ADANIPORTS | 34702 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040056_234847-002145.parquet |  | ADANIPORTS | 34375 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040110_229514-002177.parquet |  | ADANIPORTS | 34523 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040124_480433-002209.parquet |  | ADANIPORTS | 34472 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040138_728870-002241.parquet |  | ADANIPORTS | 34526 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040152_979299-002273.parquet |  | ADANIPORTS | 34462 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040206_979994-002305.parquet |  | ADANIPORTS | 35591 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040221_230810-002337.parquet |  | ADANIPORTS | 35958 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040235_483171-002369.parquet |  | ADANIPORTS | 35775 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040249_984150-002401.parquet |  | ADANIPORTS | 36131 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040304_231840-002433.parquet |  | ADANIPORTS | 35842 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040318_487736-002465.parquet |  | ADANIPORTS | 34684 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040332_729766-002497.parquet |  | ADANIPORTS | 34155 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040346_730621-002529.parquet |  | ADANIPORTS | 34406 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040400_979944-002561.parquet |  | ADANIPORTS | 34470 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040415_229802-002593.parquet |  | ADANIPORTS | 34446 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040429_480189-002625.parquet |  | ADANIPORTS | 34509 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040443_478197-002657.parquet |  | ADANIPORTS | 34527 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040457_731179-002689.parquet |  | ADANIPORTS | 34518 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040512_231882-002721.parquet |  | ADANIPORTS | 34429 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040526_497243-002753.parquet |  | ADANIPORTS | 34417 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040541_233069-002785.parquet |  | ADANIPORTS | 34668 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040555_486035-002817.parquet |  | ADANIPORTS | 34453 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040609_732995-002849.parquet |  | ADANIPORTS | 34692 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040623_731054-002881.parquet |  | ADANIPORTS | 34712 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040638_229961-002913.parquet |  | ADANIPORTS | 34751 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040652_229871-002945.parquet |  | ADANIPORTS | 34747 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040706_480219-002977.parquet |  | ADANIPORTS | 34730 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040720_485291-003009.parquet |  | ADANIPORTS | 34713 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040734_733898-003041.parquet |  | ADANIPORTS | 34718 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040749_230471-003073.parquet |  | ADANIPORTS | 34742 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040803_479800-003105.parquet |  | ADANIPORTS | 35024 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040817_480165-003137.parquet |  | ADANIPORTS | 35895 |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-040831_734061-003169.parquet |  | ADANIPORTS | 35935 |

## Next Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| selected_next_action | repair_azure_cli_tls_or_provide_fresh_sas_then_download_one_disk_safe_official_catalyst_l2_day | Real-date expansion is the only credible next path after Phase477 rejection. |
| local_real_l2_date_count_observed | 4 | Local dated real L2 partitions found by this audit. |
| fresh_sas_env_available | 0 | Supported SAS env variables present in this process. |
| az_storage_login_list_available | 0 | Azure CLI storage list via login succeeded. |
| one_day_disk_safe_increment_required | 1 | Do not attempt broad 80GB downloads while disk is constrained. |
| target_download_scope | one_full_universe_official_catalyst_l2_day | One new day first, then verify schema and event overlap. |
| required_partition_shape | raw_l2/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | Expected local shape. |
| acceptance_retest_allowed_now | 0 | No acceptance retest until new real L2 event breadth exists. |
| strategy_promotion_allowed | 0 | No strategy promotion. |
| paper_or_live_acceptance_allowed | 0 | No paper/live. |
| deployable_profitability_claim_allowed | 0 | No deployable claim. |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P478_PHASE477_REJECTION_USED | True | 0 | 0 | hard |
| P478_PHASE360_UNSEEN_REAL_EVIDENCE_USED | True | 1 | 1 | hard |
| P478_PHASE369_EXPANSION_READINESS_USED | True | 1 | 1 | hard |
| P478_BRANCH_RECONCILIATION_ROWS_PRESENT | True | 3 | >=3 | hard |
| P478_ACCESS_PROBED_WITHOUT_SECRETS | True | 0 | 0 | hard |
| P478_REAL_EXPANSION_SELECTED_NEXT | True | repair_azure_cli_tls_or_provide_fresh_sas_then_download_one_disk_safe_official_catalyst_l2_day | repair_or_sas_download | hard |
| P478_ONE_DAY_DISK_SAFE_INCREMENT_REQUIRED | True | 1 | 1 | hard |
| P478_NO_ACCEPTANCE_RETEST_NOW | True | 0 | 0 | hard |
| P478_NO_PROMOTION_PAPER_LIVE_OR_CLAIM | True | paper=0;claim=0 | all_zero | hard |

Boundary: Phase478 does not run another strategy shard. It selects one disk-safe real-data expansion step and keeps paper/live closed.
