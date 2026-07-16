# Phase 51 Full Dense Lake Materializer

Generated UTC: 2026-07-16T19:06:57.687996+00:00

This phase materializes the Phase50 full symbol-month dense target schedule into a local ignored Parquet lake.
It is the heavy raw-input generation milestone; acceptance remains closed until strategies are replayed on this dense lake.

## Summary

| metric | value | description |
| --- | --- | --- |
| phase51_schedule_shards | 384 | Scheduled symbol-month dense shards |
| phase51_source_rows | 3012294 | Source compact monthly rows materialized |
| phase51_target_dense_rows | 5974626961 | Target dense rows from Phase50 schedule |
| phase51_materialized_dense_rows | 5974626961 | Dense rows actually materialized |
| phase51_materialized_partition_files | 384 | Dense parquet files written |
| phase51_materialized_dense_bytes | 70591392905 | Compressed bytes actually written |
| phase51_estimated_dense_bytes | 8.93783e+10 | Phase50 estimated compressed bytes |
| phase51_bytes_vs_estimate_ratio | 0.789805 | Actual compressed bytes divided by estimate |
| phase51_elapsed_seconds | 13100.4 | Elapsed materialization seconds |
| phase51_rows_per_second | 456065 | Observed materialization throughput |
| phase51_available_disk_gb_after_run | 99.2011 | Free disk after materialization |
| phase51_dense_output_root | raw_synthetic_l2_dense_full_year | Local full dense lake root; ignored by Git |
| phase51_full_80gb_dense_lake_materialized | 1 | Full 80GB-class dense full-year lake materialized |
| phase51_synthetic_full_year_acceptance_ready | 0 | Dense input lake materialized; strategy acceptance still requires replay results |

## Materialization Inventory

| trade_month | symbol | source_rows | target_dense_rows | dense_rows | target_dense_multiplier | file_path | bytes | completed_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | ADANIPORTS | 8221 | 16305649 | 16305649 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=ADANIPORTS\part-00000.parquet | 199480956 | 2026-07-16T15:29:11.603364+00:00 |
| 2026-01 | AXISBANK | 8225 | 16313583 | 16313583 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=AXISBANK\part-00000.parquet | 187144855 | 2026-07-16T15:29:46.712904+00:00 |
| 2026-01 | BAJAJ-AUTO | 8221 | 16305649 | 16305649 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BAJAJ-AUTO\part-00000.parquet | 215171454 | 2026-07-16T15:30:23.081900+00:00 |
| 2026-01 | BANKBEES | 8216 | 16295732 | 16295732 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BANKBEES\part-00000.parquet | 190571553 | 2026-07-16T15:31:03.471440+00:00 |
| 2026-01 | BHARTIARTL | 8229 | 16321516 | 16321516 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BHARTIARTL\part-00000.parquet | 194040736 | 2026-07-16T15:31:40.614527+00:00 |
| 2026-01 | BPCL | 8228 | 16319533 | 16319533 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BPCL\part-00000.parquet | 176871106 | 2026-07-16T15:32:16.734452+00:00 |
| 2026-01 | BRITANNIA | 8228 | 16319533 | 16319533 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BRITANNIA\part-00000.parquet | 212897353 | 2026-07-16T15:32:57.835891+00:00 |
| 2026-01 | CIPLA | 8216 | 16295732 | 16295732 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=CIPLA\part-00000.parquet | 198987686 | 2026-07-16T15:33:40.736773+00:00 |
| 2026-01 | DRREDDY | 8218 | 16299699 | 16299699 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=DRREDDY\part-00000.parquet | 191922938 | 2026-07-16T15:34:22.419399+00:00 |
| 2026-01 | GOLDBEES | 8222 | 16307632 | 16307632 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=GOLDBEES\part-00000.parquet | 176231503 | 2026-07-16T15:35:03.846388+00:00 |
| 2026-01 | HCLTECH | 8218 | 16299699 | 16299699 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=HCLTECH\part-00000.parquet | 195495820 | 2026-07-16T15:35:50.336950+00:00 |
| 2026-01 | HDFCBANK | 8220 | 16303665 | 16303665 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=HDFCBANK\part-00000.parquet | 183042827 | 2026-07-16T15:36:36.352328+00:00 |
| 2026-01 | HINDUNILVR | 8207 | 16277881 | 16277881 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=HINDUNILVR\part-00000.parquet | 196189507 | 2026-07-16T15:37:13.328318+00:00 |
| 2026-01 | ICICIBANK | 8219 | 16301682 | 16301682 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=ICICIBANK\part-00000.parquet | 188223500 | 2026-07-16T15:37:48.932404+00:00 |
| 2026-01 | INFY | 8225 | 16313583 | 16313583 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=INFY\part-00000.parquet | 186435023 | 2026-07-16T15:38:25.002299+00:00 |
| 2026-01 | ITBEES | 8225 | 16313583 | 16313583 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=ITBEES\part-00000.parquet | 175223744 | 2026-07-16T15:39:02.334100+00:00 |
| 2026-01 | ITC | 8227 | 16317549 | 16317549 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=ITC\part-00000.parquet | 175928098 | 2026-07-16T15:39:38.902050+00:00 |
| 2026-01 | JUNIORBEES | 8209 | 16281848 | 16281848 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=JUNIORBEES\part-00000.parquet | 194039871 | 2026-07-16T15:40:15.491930+00:00 |
| 2026-01 | KOTAKBANK | 8218 | 16299699 | 16299699 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=KOTAKBANK\part-00000.parquet | 180857178 | 2026-07-16T15:40:51.833019+00:00 |
| 2026-01 | LT | 8218 | 16299699 | 16299699 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=LT\part-00000.parquet | 201863440 | 2026-07-16T15:41:28.113481+00:00 |
| 2026-01 | M&M | 8227 | 16317549 | 16317549 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=M&M\part-00000.parquet | 198838311 | 2026-07-16T15:42:05.155981+00:00 |
| 2026-01 | MARUTI | 8229 | 16321516 | 16321516 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=MARUTI\part-00000.parquet | 212147525 | 2026-07-16T15:42:42.700118+00:00 |
| 2026-01 | NESTLEIND | 8216 | 16295732 | 16295732 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=NESTLEIND\part-00000.parquet | 197526913 | 2026-07-16T15:43:19.739686+00:00 |
| 2026-01 | NIFTYBEES | 8231 | 16325483 | 16325483 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=NIFTYBEES\part-00000.parquet | 177652626 | 2026-07-16T15:43:55.416444+00:00 |
| 2026-01 | ONGC | 8219 | 16301682 | 16301682 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=ONGC\part-00000.parquet | 177598475 | 2026-07-16T15:44:31.997973+00:00 |
| 2026-01 | RELIANCE | 8214 | 16291765 | 16291765 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=RELIANCE\part-00000.parquet | 186225288 | 2026-07-16T15:45:09.322755+00:00 |
| 2026-01 | SBIN | 8215 | 16293748 | 16293748 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=SBIN\part-00000.parquet | 185549706 | 2026-07-16T15:45:46.550087+00:00 |
| 2026-01 | SUNPHARMA | 8220 | 16303665 | 16303665 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=SUNPHARMA\part-00000.parquet | 198295517 | 2026-07-16T15:46:24.730071+00:00 |
| 2026-01 | TCS | 8228 | 16319533 | 16319533 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=TCS\part-00000.parquet | 200263740 | 2026-07-16T15:47:02.499145+00:00 |
| 2026-01 | TECHM | 8217 | 16297715 | 16297715 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=TECHM\part-00000.parquet | 201631100 | 2026-07-16T15:47:38.492287+00:00 |
| 2026-01 | ULTRACEMCO | 8237 | 16337384 | 16337384 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=ULTRACEMCO\part-00000.parquet | 210681805 | 2026-07-16T15:48:16.233636+00:00 |
| 2026-01 | WIPRO | 8239 | 16341350 | 16341350 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=WIPRO\part-00000.parquet | 179573761 | 2026-07-16T15:48:52.765357+00:00 |
| 2026-02 | ADANIPORTS | 7475 | 14826022 | 14826022 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=ADANIPORTS\part-00000.parquet | 182757324 | 2026-07-16T15:49:27.324700+00:00 |
| 2026-02 | AXISBANK | 7473 | 14822055 | 14822055 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=AXISBANK\part-00000.parquet | 174699632 | 2026-07-16T15:50:00.249951+00:00 |
| 2026-02 | BAJAJ-AUTO | 7480 | 14835939 | 14835939 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=BAJAJ-AUTO\part-00000.parquet | 196166319 | 2026-07-16T15:50:33.818255+00:00 |
| 2026-02 | BANKBEES | 7465 | 14806188 | 14806188 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=BANKBEES\part-00000.parquet | 173729917 | 2026-07-16T15:51:06.365534+00:00 |
| 2026-02 | BHARTIARTL | 7484 | 14843873 | 14843873 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=BHARTIARTL\part-00000.parquet | 180029188 | 2026-07-16T15:51:39.314707+00:00 |
| 2026-02 | BPCL | 7474 | 14824038 | 14824038 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=BPCL\part-00000.parquet | 161388124 | 2026-07-16T15:52:12.011520+00:00 |
| 2026-02 | BRITANNIA | 7460 | 14796271 | 14796271 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=BRITANNIA\part-00000.parquet | 192025225 | 2026-07-16T15:52:45.634354+00:00 |
| 2026-02 | CIPLA | 7468 | 14812138 | 14812138 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=CIPLA\part-00000.parquet | 182612525 | 2026-07-16T15:53:23.443932+00:00 |
| 2026-02 | DRREDDY | 7462 | 14800237 | 14800237 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=DRREDDY\part-00000.parquet | 175663151 | 2026-07-16T15:53:57.088806+00:00 |
| 2026-02 | GOLDBEES | 7468 | 14812138 | 14812138 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=GOLDBEES\part-00000.parquet | 160805798 | 2026-07-16T15:54:28.875737+00:00 |
| 2026-02 | HCLTECH | 7465 | 14806188 | 14806188 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=HCLTECH\part-00000.parquet | 175752834 | 2026-07-16T15:55:01.673540+00:00 |
| 2026-02 | HDFCBANK | 7476 | 14828005 | 14828005 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=HDFCBANK\part-00000.parquet | 166747293 | 2026-07-16T15:55:34.792515+00:00 |
| 2026-02 | HINDUNILVR | 7463 | 14802221 | 14802221 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=HINDUNILVR\part-00000.parquet | 181485512 | 2026-07-16T15:56:07.203137+00:00 |
| 2026-02 | ICICIBANK | 7469 | 14814121 | 14814121 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=ICICIBANK\part-00000.parquet | 172428373 | 2026-07-16T15:56:39.549656+00:00 |
| 2026-02 | INFY | 7459 | 14794287 | 14794287 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=INFY\part-00000.parquet | 172235168 | 2026-07-16T15:57:11.897906+00:00 |
| 2026-02 | ITBEES | 7480 | 14835939 | 14835939 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=ITBEES\part-00000.parquet | 160123919 | 2026-07-16T15:57:44.219444+00:00 |
| 2026-02 | ITC | 7486 | 14847839 | 14847839 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=ITC\part-00000.parquet | 164732131 | 2026-07-16T15:58:17.249148+00:00 |
| 2026-02 | JUNIORBEES | 7478 | 14831972 | 14831972 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=JUNIORBEES\part-00000.parquet | 179551082 | 2026-07-16T15:58:50.774077+00:00 |
| 2026-02 | KOTAKBANK | 7467 | 14810155 | 14810155 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=KOTAKBANK\part-00000.parquet | 165639741 | 2026-07-16T15:59:23.916730+00:00 |
| 2026-02 | LT | 7464 | 14804204 | 14804204 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=LT\part-00000.parquet | 183495855 | 2026-07-16T15:59:56.673706+00:00 |
| 2026-02 | M&M | 7457 | 14790320 | 14790320 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=M&M\part-00000.parquet | 179953236 | 2026-07-16T16:00:30.007742+00:00 |
| 2026-02 | MARUTI | 7466 | 14808171 | 14808171 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=MARUTI\part-00000.parquet | 192067961 | 2026-07-16T16:01:03.997493+00:00 |
| 2026-02 | NESTLEIND | 7466 | 14808171 | 14808171 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=NESTLEIND\part-00000.parquet | 181612952 | 2026-07-16T16:01:36.142693+00:00 |
| 2026-02 | NIFTYBEES | 7458 | 14792304 | 14792304 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=NIFTYBEES\part-00000.parquet | 164860841 | 2026-07-16T16:02:09.103913+00:00 |
| 2026-02 | ONGC | 7473 | 14822055 | 14822055 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=ONGC\part-00000.parquet | 163922094 | 2026-07-16T16:02:43.259164+00:00 |
| 2026-02 | RELIANCE | 7453 | 14782387 | 14782387 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=RELIANCE\part-00000.parquet | 170069188 | 2026-07-16T16:03:17.183462+00:00 |
| 2026-02 | SBIN | 7472 | 14820072 | 14820072 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=SBIN\part-00000.parquet | 172354358 | 2026-07-16T16:03:50.706304+00:00 |
| 2026-02 | SUNPHARMA | 7472 | 14820072 | 14820072 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=SUNPHARMA\part-00000.parquet | 179135196 | 2026-07-16T16:04:24.151284+00:00 |
| 2026-02 | TCS | 7464 | 14804204 | 14804204 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=TCS\part-00000.parquet | 181992263 | 2026-07-16T16:04:55.323972+00:00 |
| 2026-02 | TECHM | 7443 | 14762553 | 14762553 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=TECHM\part-00000.parquet | 180724165 | 2026-07-16T16:05:27.034826+00:00 |
| 2026-02 | ULTRACEMCO | 7465 | 14806188 | 14806188 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=ULTRACEMCO\part-00000.parquet | 191969298 | 2026-07-16T16:05:58.605941+00:00 |
| 2026-02 | WIPRO | 7465 | 14806188 | 14806188 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=WIPRO\part-00000.parquet | 162754559 | 2026-07-16T16:06:29.541090+00:00 |
| 2026-03 | ADANIPORTS | 8213 | 16289782 | 16289782 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=ADANIPORTS\part-00000.parquet | 200027669 | 2026-07-16T16:07:04.653278+00:00 |
| 2026-03 | AXISBANK | 8218 | 16299699 | 16299699 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=AXISBANK\part-00000.parquet | 186179887 | 2026-07-16T16:07:38.494832+00:00 |
| 2026-03 | BAJAJ-AUTO | 8221 | 16305649 | 16305649 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=BAJAJ-AUTO\part-00000.parquet | 215714127 | 2026-07-16T16:08:14.106533+00:00 |
| 2026-03 | BANKBEES | 8225 | 16313583 | 16313583 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=BANKBEES\part-00000.parquet | 189495495 | 2026-07-16T16:08:48.468846+00:00 |
| 2026-03 | BHARTIARTL | 8226 | 16315566 | 16315566 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=BHARTIARTL\part-00000.parquet | 194532664 | 2026-07-16T16:09:24.466787+00:00 |
| 2026-03 | BPCL | 8232 | 16327466 | 16327466 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=BPCL\part-00000.parquet | 179553721 | 2026-07-16T16:09:59.085834+00:00 |
| 2026-03 | BRITANNIA | 8209 | 16281848 | 16281848 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=BRITANNIA\part-00000.parquet | 211540056 | 2026-07-16T16:10:34.216656+00:00 |
| 2026-03 | CIPLA | 8232 | 16327466 | 16327466 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=CIPLA\part-00000.parquet | 200495215 | 2026-07-16T16:11:08.567277+00:00 |
| 2026-03 | DRREDDY | 8214 | 16291765 | 16291765 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=DRREDDY\part-00000.parquet | 192635231 | 2026-07-16T16:11:43.065710+00:00 |
| 2026-03 | GOLDBEES | 8218 | 16299699 | 16299699 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=GOLDBEES\part-00000.parquet | 177361961 | 2026-07-16T16:12:16.888529+00:00 |
| 2026-03 | HCLTECH | 8221 | 16305649 | 16305649 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=HCLTECH\part-00000.parquet | 193465981 | 2026-07-16T16:12:51.677132+00:00 |
| 2026-03 | HDFCBANK | 8220 | 16303665 | 16303665 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=HDFCBANK\part-00000.parquet | 182264554 | 2026-07-16T16:13:25.675653+00:00 |
| 2026-03 | HINDUNILVR | 8216 | 16295732 | 16295732 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=HINDUNILVR\part-00000.parquet | 197902687 | 2026-07-16T16:14:00.174794+00:00 |
| 2026-03 | ICICIBANK | 8216 | 16295732 | 16295732 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=ICICIBANK\part-00000.parquet | 187734755 | 2026-07-16T16:14:34.397145+00:00 |
| 2026-03 | INFY | 8210 | 16283831 | 16283831 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=INFY\part-00000.parquet | 186393894 | 2026-07-16T16:15:08.244496+00:00 |
| 2026-03 | ITBEES | 8210 | 16283831 | 16283831 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=ITBEES\part-00000.parquet | 176442647 | 2026-07-16T16:15:42.835392+00:00 |
| 2026-03 | ITC | 8198 | 16260030 | 16260030 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=ITC\part-00000.parquet | 177630496 | 2026-07-16T16:16:17.158970+00:00 |
| 2026-03 | JUNIORBEES | 8213 | 16289782 | 16289782 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=JUNIORBEES\part-00000.parquet | 194473205 | 2026-07-16T16:16:51.495617+00:00 |
| 2026-03 | KOTAKBANK | 8216 | 16295732 | 16295732 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=KOTAKBANK\part-00000.parquet | 180956447 | 2026-07-16T16:17:25.328224+00:00 |
| 2026-03 | LT | 8215 | 16293748 | 16293748 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=LT\part-00000.parquet | 200870957 | 2026-07-16T16:18:00.146396+00:00 |
| 2026-03 | M&M | 8216 | 16295732 | 16295732 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=M&M\part-00000.parquet | 198103397 | 2026-07-16T16:18:34.220501+00:00 |
| 2026-03 | MARUTI | 8225 | 16313583 | 16313583 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=MARUTI\part-00000.parquet | 212175830 | 2026-07-16T16:19:10.486640+00:00 |
| 2026-03 | NESTLEIND | 8221 | 16305649 | 16305649 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=NESTLEIND\part-00000.parquet | 198015486 | 2026-07-16T16:19:44.436810+00:00 |
| 2026-03 | NIFTYBEES | 8218 | 16299699 | 16299699 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=NIFTYBEES\part-00000.parquet | 177831385 | 2026-07-16T16:20:18.695262+00:00 |
| 2026-03 | ONGC | 8215 | 16293748 | 16293748 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=ONGC\part-00000.parquet | 178460669 | 2026-07-16T16:20:52.663449+00:00 |
| 2026-03 | RELIANCE | 8223 | 16309616 | 16309616 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=RELIANCE\part-00000.parquet | 187478820 | 2026-07-16T16:21:27.207382+00:00 |
| 2026-03 | SBIN | 8205 | 16273914 | 16273914 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=SBIN\part-00000.parquet | 185701473 | 2026-07-16T16:22:01.044788+00:00 |
| 2026-03 | SUNPHARMA | 8220 | 16303665 | 16303665 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=SUNPHARMA\part-00000.parquet | 197027541 | 2026-07-16T16:22:35.363008+00:00 |
| 2026-03 | TCS | 8227 | 16317549 | 16317549 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=TCS\part-00000.parquet | 199238068 | 2026-07-16T16:23:10.443235+00:00 |
| 2026-03 | TECHM | 8211 | 16285815 | 16285815 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=TECHM\part-00000.parquet | 200094010 | 2026-07-16T16:23:44.405107+00:00 |
| 2026-03 | ULTRACEMCO | 8221 | 16305649 | 16305649 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=ULTRACEMCO\part-00000.parquet | 211913806 | 2026-07-16T16:24:20.060050+00:00 |
| 2026-03 | WIPRO | 8228 | 16319533 | 16319533 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=WIPRO\part-00000.parquet | 178304728 | 2026-07-16T16:24:53.795239+00:00 |
| 2026-04 | ADANIPORTS | 8211 | 16285815 | 16285815 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=ADANIPORTS\part-00000.parquet | 200168175 | 2026-07-16T16:25:32.272311+00:00 |
| 2026-04 | AXISBANK | 8212 | 16287798 | 16287798 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=AXISBANK\part-00000.parquet | 189338192 | 2026-07-16T16:26:07.098785+00:00 |
| 2026-04 | BAJAJ-AUTO | 8215 | 16293748 | 16293748 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=BAJAJ-AUTO\part-00000.parquet | 213065012 | 2026-07-16T16:26:42.034537+00:00 |
| 2026-04 | BANKBEES | 8222 | 16307632 | 16307632 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=BANKBEES\part-00000.parquet | 191020805 | 2026-07-16T16:27:18.354132+00:00 |
| 2026-04 | BHARTIARTL | 8227 | 16317549 | 16317549 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=BHARTIARTL\part-00000.parquet | 195788742 | 2026-07-16T16:27:54.859153+00:00 |
| 2026-04 | BPCL | 8222 | 16307632 | 16307632 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=BPCL\part-00000.parquet | 178805583 | 2026-07-16T16:28:30.803055+00:00 |
| 2026-04 | BRITANNIA | 8213 | 16289782 | 16289782 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=BRITANNIA\part-00000.parquet | 211164112 | 2026-07-16T16:29:07.572827+00:00 |
| 2026-04 | CIPLA | 8218 | 16299699 | 16299699 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=CIPLA\part-00000.parquet | 199753445 | 2026-07-16T16:29:45.069509+00:00 |
| 2026-04 | DRREDDY | 8203 | 16269947 | 16269947 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=DRREDDY\part-00000.parquet | 194029349 | 2026-07-16T16:30:20.767565+00:00 |
| 2026-04 | GOLDBEES | 8217 | 16297715 | 16297715 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=GOLDBEES\part-00000.parquet | 175238725 | 2026-07-16T16:30:57.512086+00:00 |
| 2026-04 | HCLTECH | 8215 | 16293748 | 16293748 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=HCLTECH\part-00000.parquet | 193657282 | 2026-07-16T16:31:32.615636+00:00 |
| 2026-04 | HDFCBANK | 8212 | 16287798 | 16287798 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=HDFCBANK\part-00000.parquet | 182210045 | 2026-07-16T16:32:08.796364+00:00 |
| 2026-04 | HINDUNILVR | 8201 | 16265981 | 16265981 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=HINDUNILVR\part-00000.parquet | 198072653 | 2026-07-16T16:32:42.918109+00:00 |
| 2026-04 | ICICIBANK | 8221 | 16305649 | 16305649 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=ICICIBANK\part-00000.parquet | 189425480 | 2026-07-16T16:33:18.765376+00:00 |
| 2026-04 | INFY | 8197 | 16258047 | 16258047 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=INFY\part-00000.parquet | 188318127 | 2026-07-16T16:33:54.820639+00:00 |
| 2026-04 | ITBEES | 8229 | 16321516 | 16321516 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=ITBEES\part-00000.parquet | 174716608 | 2026-07-16T16:34:31.922179+00:00 |
| 2026-04 | ITC | 8212 | 16287798 | 16287798 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=ITC\part-00000.parquet | 178053582 | 2026-07-16T16:35:07.409420+00:00 |
| 2026-04 | JUNIORBEES | 8223 | 16309616 | 16309616 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=JUNIORBEES\part-00000.parquet | 197228212 | 2026-07-16T16:35:43.235495+00:00 |
| 2026-04 | KOTAKBANK | 8215 | 16293748 | 16293748 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=KOTAKBANK\part-00000.parquet | 181533059 | 2026-07-16T16:36:18.566317+00:00 |
| 2026-04 | LT | 8198 | 16260030 | 16260030 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=LT\part-00000.parquet | 201227024 | 2026-07-16T16:36:54.497472+00:00 |
| 2026-04 | M&M | 8214 | 16291765 | 16291765 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=M&M\part-00000.parquet | 201150468 | 2026-07-16T16:37:30.544019+00:00 |
| 2026-04 | MARUTI | 8209 | 16281848 | 16281848 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=MARUTI\part-00000.parquet | 211739123 | 2026-07-16T16:38:06.588803+00:00 |
| 2026-04 | NESTLEIND | 8215 | 16293748 | 16293748 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=NESTLEIND\part-00000.parquet | 199606119 | 2026-07-16T16:38:40.499999+00:00 |
| 2026-04 | NIFTYBEES | 8217 | 16297715 | 16297715 | 1983.41 | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=NIFTYBEES\part-00000.parquet | 178670566 | 2026-07-16T16:39:14.715410+00:00 |
