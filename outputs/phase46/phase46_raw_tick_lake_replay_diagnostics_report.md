# Phase 46 Raw Tick-Lake Replay Diagnostics

Generated UTC: 2026-07-16T14:52:40.820664+00:00

This phase reads the Phase 45 partitioned raw websocket-like L2 lake, reconstructs event features from L1-L5 depth fields, and runs a raw-source forward-edge diagnostic.
It proves the raw lake can be used as the experiment source instead of the compact Phase 42 parquet. It is not strategy acceptance evidence.

## Integrity Summary

| metric | value | description |
| --- | --- | --- |
| phase46_partition_rows | 8064 | Raw date/exchange/symbol partitions scanned |
| phase46_inventory_rows | 3012294 | Rows declared by Phase45 inventory |
| phase46_raw_rows_loaded | 3012294 | Raw rows loaded from partitioned parquet lake |
| phase46_symbols | 32 | Symbols loaded from raw lake |
| phase46_trade_dates | 252 | Trade dates loaded from raw lake |
| phase46_feed_profiles | 5 | Feed profiles loaded from raw lake |
| phase46_l1_l5_depth_complete | 1 | All L1-L5 price and quantity fields present/nonzero |
| phase46_inventory_row_match | 1 | Loaded row count matches inventory |
| phase46_feature_rows_reconstructed | 3012294 | Rows with raw-derived feature reconstruction |
| phase46_mid_price_null_rows | 0 | Rows with missing reconstructed mid price |
| phase46_synthetic_full_year_acceptance_ready | 0 | Raw-lake replay diagnostic is experiment plumbing, not acceptance |

## Replay Summary

| metric | value | description |
| --- | --- | --- |
| phase46_raw_edge_candidate_rows | 72 | Raw-derived forward-edge candidates evaluated |
| phase46_total_raw_edge_signals | 1.1334e+07 | Total raw-derived feature-threshold signals evaluated |
| phase46_raw_replay_candidate_rows | 0 | Raw-derived rows passing pre-replay screen |
| phase46_best_raw_mean_net_edge_return | 0.00273094 | Best raw-derived mean net edge return |
| phase46_best_raw_precision_lift_vs_baseline | 0.87609 | Best raw-derived precision lift |
| phase46_best_raw_directional_precision | 0.525373 | Best raw-derived directional precision |

## Top Raw Forward-Edge Results

| raw_label_candidate_id | thesis_id | feature_column | direction_multiplier | threshold_quantile | threshold_value | forward_horizon_events | signals | baseline_any_edge_rate | directional_precision | precision_lift_vs_baseline | mean_net_edge_return | candidate_for_raw_replay |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| raw_momentum_fade_q98_1e | raw_momentum_fade | momentum_3_event | -1 | 0.98 | 0.0130066 | 1 | 54569 | 0.591039 | 0.517803 | 0.87609 | 0.00273094 | False |
| raw_momentum_fade_q98_3e | raw_momentum_fade | momentum_3_event | -1 | 0.98 | 0.0130066 | 3 | 51179 | 0.72703 | 0.519901 | 0.715102 | 0.00215985 | False |
| raw_momentum_fade_q98_6e | raw_momentum_fade | momentum_3_event | -1 | 0.98 | 0.0130066 | 6 | 47374 | 0.800318 | 0.525373 | 0.656454 | 0.00215779 | False |
| raw_momentum_fade_q95_1e | raw_momentum_fade | momentum_3_event | -1 | 0.95 | 0.00910506 | 1 | 139513 | 0.591039 | 0.472286 | 0.799078 | 0.0011405 | False |
| raw_momentum_fade_q95_3e | raw_momentum_fade | momentum_3_event | -1 | 0.95 | 0.00910506 | 3 | 132410 | 0.72703 | 0.481829 | 0.662736 | 0.00063607 | False |
| raw_momentum_fade_q95_6e | raw_momentum_fade | momentum_3_event | -1 | 0.95 | 0.00910506 | 6 | 123405 | 0.800318 | 0.493497 | 0.616626 | 0.000456527 | False |
| raw_momentum_fade_q90_1e | raw_momentum_fade | momentum_3_event | -1 | 0.9 | 0.00672531 | 1 | 282869 | 0.591039 | 0.43943 | 0.743487 | 0.000370207 | False |
| raw_momentum_fade_q90_3e | raw_momentum_fade | momentum_3_event | -1 | 0.9 | 0.00672531 | 3 | 270563 | 0.72703 | 0.460529 | 0.633438 | 2.40561e-05 | False |
| raw_momentum_fade_q90_6e | raw_momentum_fade | momentum_3_event | -1 | 0.9 | 0.00672531 | 6 | 254234 | 0.800318 | 0.471035 | 0.588559 | -0.000244506 | False |
| raw_microprice_fade_q98_6e | raw_microprice_fade | microprice_dev | -1 | 0.98 | 0.000144058 | 6 | 53768 | 0.800318 | 0.439369 | 0.548993 | -0.000502079 | False |
| raw_microprice_fade_q95_6e | raw_microprice_fade | microprice_dev | -1 | 0.95 | 0.000116599 | 6 | 134652 | 0.800318 | 0.417565 | 0.521749 | -0.000507797 | False |
| raw_microprice_fade_q90_6e | raw_microprice_fade | microprice_dev | -1 | 0.9 | 9.0187e-05 | 6 | 270550 | 0.800318 | 0.398821 | 0.498328 | -0.000772657 | False |
| raw_microprice_fade_q95_3e | raw_microprice_fade | microprice_dev | -1 | 0.95 | 0.000116599 | 3 | 140729 | 0.72703 | 0.376134 | 0.517357 | -0.000830558 | False |
| raw_microprice_fade_q98_3e | raw_microprice_fade | microprice_dev | -1 | 0.98 | 0.000144058 | 3 | 56146 | 0.72703 | 0.39928 | 0.549194 | -0.000858847 | False |
| raw_l5_imbalance_fade_q98_6e | raw_l5_imbalance_fade | l5_imbalance | -1 | 0.98 | 0.739712 | 6 | 54880 | 0.800318 | 0.373816 | 0.467084 | -0.000912187 | False |
| raw_l1_imbalance_fade_q98_6e | raw_l1_imbalance_fade | l1_imbalance | -1 | 0.98 | 0.739691 | 6 | 56527 | 0.800318 | 0.376935 | 0.470981 | -0.000912443 | False |
| raw_microprice_fade_q90_3e | raw_microprice_fade | microprice_dev | -1 | 0.9 | 9.0187e-05 | 3 | 282296 | 0.72703 | 0.357695 | 0.491995 | -0.000943829 | False |
| raw_l1_imbalance_fade_q98_3e | raw_l1_imbalance_fade | l1_imbalance | -1 | 0.98 | 0.739691 | 3 | 58833 | 0.72703 | 0.32803 | 0.451192 | -0.000965286 | False |
| raw_l5_imbalance_fade_q98_3e | raw_l5_imbalance_fade | l5_imbalance | -1 | 0.98 | 0.739712 | 3 | 57164 | 0.72703 | 0.32489 | 0.446873 | -0.000967666 | False |
| raw_l5_imbalance_fade_q98_1e | raw_l5_imbalance_fade | l5_imbalance | -1 | 0.98 | 0.739712 | 1 | 58662 | 0.591039 | 0.246275 | 0.416682 | -0.000968138 | False |
| raw_l1_imbalance_fade_q98_1e | raw_l1_imbalance_fade | l1_imbalance | -1 | 0.98 | 0.739691 | 1 | 60352 | 0.591039 | 0.250994 | 0.424666 | -0.000975621 | False |
| raw_l1_imbalance_fade_q95_6e | raw_l1_imbalance_fade | l1_imbalance | -1 | 0.95 | 0.697068 | 6 | 135815 | 0.800318 | 0.375503 | 0.469193 | -0.000999031 | False |
| raw_l5_imbalance_fade_q95_6e | raw_l5_imbalance_fade | l5_imbalance | -1 | 0.95 | 0.697087 | 6 | 135969 | 0.800318 | 0.375975 | 0.469782 | -0.00100495 | False |
| raw_l5_imbalance_fade_q90_1e | raw_l5_imbalance_fade | l5_imbalance | -1 | 0.9 | 0.577998 | 1 | 290376 | 0.591039 | 0.264626 | 0.44773 | -0.00101152 | False |
| raw_l1_imbalance_fade_q90_1e | raw_l1_imbalance_fade | l1_imbalance | -1 | 0.9 | 0.578341 | 1 | 290377 | 0.591039 | 0.26458 | 0.447653 | -0.00101163 | False |
| raw_l1_imbalance_fade_q90_6e | raw_l1_imbalance_fade | l1_imbalance | -1 | 0.9 | 0.578341 | 6 | 270758 | 0.800318 | 0.384262 | 0.480136 | -0.00101291 | False |
| raw_l5_imbalance_fade_q90_6e | raw_l5_imbalance_fade | l5_imbalance | -1 | 0.9 | 0.577998 | 6 | 270778 | 0.800318 | 0.384278 | 0.480156 | -0.00101438 | False |
| raw_l5_imbalance_fade_q90_3e | raw_l5_imbalance_fade | l5_imbalance | -1 | 0.9 | 0.577998 | 3 | 282799 | 0.72703 | 0.340949 | 0.468961 | -0.00101548 | False |
| raw_l1_imbalance_fade_q90_3e | raw_l1_imbalance_fade | l1_imbalance | -1 | 0.9 | 0.578341 | 3 | 282779 | 0.72703 | 0.340902 | 0.468897 | -0.00101569 | False |
| raw_l1_imbalance_fade_q95_3e | raw_l1_imbalance_fade | l1_imbalance | -1 | 0.95 | 0.697068 | 3 | 141737 | 0.72703 | 0.329074 | 0.452628 | -0.00102206 | False |
| raw_l1_imbalance_fade_q95_1e | raw_l1_imbalance_fade | l1_imbalance | -1 | 0.95 | 0.697068 | 1 | 145476 | 0.591039 | 0.251677 | 0.425822 | -0.00102495 | False |
| raw_l5_imbalance_fade_q95_3e | raw_l5_imbalance_fade | l5_imbalance | -1 | 0.95 | 0.697087 | 3 | 141866 | 0.72703 | 0.32862 | 0.452003 | -0.00102888 | False |
| raw_microprice_fade_q95_1e | raw_microprice_fade | microprice_dev | -1 | 0.95 | 0.000116599 | 1 | 144577 | 0.591039 | 0.302254 | 0.511395 | -0.00103144 | False |
| raw_l5_imbalance_fade_q95_1e | raw_l5_imbalance_fade | l5_imbalance | -1 | 0.95 | 0.697087 | 1 | 145604 | 0.591039 | 0.250776 | 0.424297 | -0.00103296 | False |
| raw_microprice_fade_q90_1e | raw_microprice_fade | microprice_dev | -1 | 0.9 | 9.0187e-05 | 1 | 289738 | 0.591039 | 0.28533 | 0.482761 | -0.00104599 | False |
| raw_l5_imbalance_follow_q90_3e | raw_l5_imbalance_follow | l5_imbalance | 1 | 0.9 | 0.577998 | 3 | 282799 | 0.72703 | 0.339545 | 0.46703 | -0.00105436 | False |
| raw_l1_imbalance_follow_q90_3e | raw_l1_imbalance_follow | l1_imbalance | 1 | 0.9 | 0.578341 | 3 | 282779 | 0.72703 | 0.339711 | 0.467258 | -0.00105465 | False |
| raw_l5_imbalance_follow_q90_6e | raw_l5_imbalance_follow | l5_imbalance | 1 | 0.9 | 0.577998 | 6 | 270778 | 0.800318 | 0.379883 | 0.474665 | -0.0010555 | False |
| raw_l1_imbalance_follow_q90_6e | raw_l1_imbalance_follow | l1_imbalance | 1 | 0.9 | 0.578341 | 6 | 270758 | 0.800318 | 0.379826 | 0.474594 | -0.00105746 | False |
| raw_l5_imbalance_follow_q90_1e | raw_l5_imbalance_follow | l5_imbalance | 1 | 0.9 | 0.577998 | 1 | 290376 | 0.591039 | 0.261778 | 0.442912 | -0.00105828 | False |
| raw_l1_imbalance_follow_q90_1e | raw_l1_imbalance_follow | l1_imbalance | 1 | 0.9 | 0.578341 | 1 | 290377 | 0.591039 | 0.261653 | 0.4427 | -0.00105868 | False |
| raw_microprice_fade_q98_1e | raw_microprice_fade | microprice_dev | -1 | 0.98 | 0.000144058 | 1 | 57657 | 0.591039 | 0.333229 | 0.563803 | -0.00107856 | False |
| raw_l5_imbalance_follow_q95_1e | raw_l5_imbalance_follow | l5_imbalance | 1 | 0.95 | 0.697087 | 1 | 145604 | 0.591039 | 0.244828 | 0.414234 | -0.00110145 | False |
| raw_l5_imbalance_follow_q95_3e | raw_l5_imbalance_follow | l5_imbalance | 1 | 0.95 | 0.697087 | 3 | 141866 | 0.72703 | 0.329494 | 0.453205 | -0.00110544 | False |
| raw_l1_imbalance_follow_q95_1e | raw_l1_imbalance_follow | l1_imbalance | 1 | 0.95 | 0.697068 | 1 | 145476 | 0.591039 | 0.243415 | 0.411842 | -0.00110891 | False |
| raw_l1_imbalance_follow_q95_3e | raw_l1_imbalance_follow | l1_imbalance | 1 | 0.95 | 0.697068 | 3 | 141737 | 0.72703 | 0.328206 | 0.451434 | -0.00111172 | False |
| raw_l1_imbalance_follow_q98_1e | raw_l1_imbalance_follow | l1_imbalance | 1 | 0.98 | 0.739691 | 1 | 60352 | 0.591039 | 0.237639 | 0.402071 | -0.00112617 | False |
| raw_l5_imbalance_follow_q95_6e | raw_l5_imbalance_follow | l5_imbalance | 1 | 0.95 | 0.697087 | 6 | 135969 | 0.800318 | 0.369908 | 0.462201 | -0.00112923 | False |
| raw_l1_imbalance_follow_q95_6e | raw_l1_imbalance_follow | l1_imbalance | 1 | 0.95 | 0.697068 | 6 | 135815 | 0.800318 | 0.368995 | 0.46106 | -0.00113459 | False |
| raw_l5_imbalance_follow_q98_1e | raw_l5_imbalance_follow | l5_imbalance | 1 | 0.98 | 0.739712 | 1 | 58662 | 0.591039 | 0.23153 | 0.391734 | -0.00113534 | False |
| raw_l5_imbalance_follow_q98_3e | raw_l5_imbalance_follow | l5_imbalance | 1 | 0.98 | 0.739712 | 3 | 57164 | 0.72703 | 0.316528 | 0.435371 | -0.00113607 | False |
| raw_l1_imbalance_follow_q98_3e | raw_l1_imbalance_follow | l1_imbalance | 1 | 0.98 | 0.739691 | 3 | 58833 | 0.72703 | 0.322455 | 0.443524 | -0.00113668 | False |
| raw_microprice_follow_q90_1e | raw_microprice_follow | microprice_dev | 1 | 0.9 | 9.0187e-05 | 1 | 289738 | 0.591039 | 0.283321 | 0.479362 | -0.0011397 | False |
| raw_l1_imbalance_follow_q98_6e | raw_l1_imbalance_follow | l1_imbalance | 1 | 0.98 | 0.739691 | 6 | 56527 | 0.800318 | 0.362535 | 0.452988 | -0.00118952 | False |
| raw_l5_imbalance_follow_q98_6e | raw_l5_imbalance_follow | l5_imbalance | 1 | 0.98 | 0.739712 | 6 | 54880 | 0.800318 | 0.35789 | 0.447184 | -0.0011917 | False |
| raw_microprice_follow_q95_1e | raw_microprice_follow | microprice_dev | 1 | 0.95 | 0.000116599 | 1 | 144577 | 0.591039 | 0.293159 | 0.496006 | -0.00122091 | False |
| raw_microprice_follow_q90_3e | raw_microprice_follow | microprice_dev | 1 | 0.9 | 9.0187e-05 | 3 | 282296 | 0.72703 | 0.352276 | 0.484541 | -0.00124185 | False |
| raw_microprice_follow_q98_1e | raw_microprice_follow | microprice_dev | 1 | 0.98 | 0.000144058 | 1 | 57657 | 0.591039 | 0.321817 | 0.544494 | -0.00127277 | False |
| raw_microprice_follow_q90_6e | raw_microprice_follow | microprice_dev | 1 | 0.9 | 9.0187e-05 | 6 | 270550 | 0.800318 | 0.386213 | 0.482574 | -0.00141301 | False |
| raw_microprice_follow_q95_3e | raw_microprice_follow | microprice_dev | 1 | 0.95 | 0.000116599 | 3 | 140729 | 0.72703 | 0.360103 | 0.495307 | -0.00142193 | False |
| raw_microprice_follow_q98_3e | raw_microprice_follow | microprice_dev | 1 | 0.98 | 0.000144058 | 3 | 56146 | 0.72703 | 0.381434 | 0.524647 | -0.00149227 | False |
| raw_microprice_follow_q95_6e | raw_microprice_follow | microprice_dev | 1 | 0.95 | 0.000116599 | 6 | 134652 | 0.800318 | 0.389812 | 0.487071 | -0.00174488 | False |
| raw_momentum_follow_q90_6e | raw_momentum_follow | momentum_3_event | 1 | 0.9 | 0.00672531 | 6 | 254234 | 0.800318 | 0.419897 | 0.524662 | -0.00184738 | False |
| raw_microprice_follow_q98_6e | raw_microprice_follow | microprice_dev | 1 | 0.98 | 0.000144058 | 6 | 53768 | 0.800318 | 0.400498 | 0.500424 | -0.00184888 | False |
| raw_momentum_follow_q90_3e | raw_momentum_follow | momentum_3_event | 1 | 0.9 | 0.00672531 | 3 | 270563 | 0.72703 | 0.38299 | 0.526787 | -0.0021153 | False |
| raw_momentum_follow_q90_1e | raw_momentum_follow | momentum_3_event | 1 | 0.9 | 0.00672531 | 1 | 282869 | 0.591039 | 0.322181 | 0.54511 | -0.00246086 | False |
| raw_momentum_follow_q95_6e | raw_momentum_follow | momentum_3_event | 1 | 0.95 | 0.00910506 | 6 | 123405 | 0.800318 | 0.412552 | 0.515485 | -0.00258286 | False |
| raw_momentum_follow_q95_3e | raw_momentum_follow | momentum_3_event | 1 | 0.95 | 0.00910506 | 3 | 132410 | 0.72703 | 0.384533 | 0.528909 | -0.00276135 | False |
| raw_momentum_follow_q95_1e | raw_momentum_follow | momentum_3_event | 1 | 0.95 | 0.00910506 | 1 | 139513 | 0.591039 | 0.332672 | 0.562859 | -0.00326503 | False |
| raw_momentum_follow_q98_6e | raw_momentum_follow | momentum_3_event | 1 | 0.98 | 0.0130066 | 6 | 47374 | 0.800318 | 0.397623 | 0.496831 | -0.00433235 | False |
| raw_momentum_follow_q98_3e | raw_momentum_follow | momentum_3_event | 1 | 0.98 | 0.0130066 | 3 | 51179 | 0.72703 | 0.371051 | 0.510365 | -0.00433322 | False |
| raw_momentum_follow_q98_1e | raw_momentum_follow | momentum_3_event | 1 | 0.98 | 0.0130066 | 1 | 54569 | 0.591039 | 0.332863 | 0.563183 | -0.00490394 | False |

## Feature Sample

| trade_date | exchange | symbol | feed_profile | annual_event_id | mid_price | spread | l1_imbalance | l5_imbalance | microprice_dev | momentum_3_event |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 1 | 1818.7 | 0.4 | 0.236407 | 0.231646 | 2.59973e-05 | 0 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 2 | 1826.4 | 0.4 | 0.224018 | 0.227279 | 2.45312e-05 | 0.00423379 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 3 | 1828.2 | 0.4 | 0.22108 | 0.219719 | 2.41855e-05 | 0.00521934 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 4 | 1826 | 0.4 | 0.221939 | 0.215969 | 2.43087e-05 | 0.00401597 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 5 | 1825.6 | 0.4 | 0.21671 | 0.215789 | 2.37413e-05 | -0.000436882 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 6 | 1824.6 | 0.4 | 0.204663 | 0.207743 | 2.24338e-05 | -0.00197019 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 7 | 1827.9 | 0.4 | 0.221939 | 0.220588 | 2.42835e-05 | 0.00104179 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 8 | 1836.6 | 0.4 | 0.243182 | 0.237701 | 2.64817e-05 | 0.00602041 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 9 | 1812.4 | 0.4 | 0.217277 | 0.215771 | 2.39768e-05 | -0.00660835 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 10 | 1835.3 | 0.4 | 0.205195 | 0.207639 | 2.23609e-05 | 0.00421822 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 11 | 1834.2 | 0.4 | 0.206266 | 0.207002 | 2.24911e-05 | -0.0011407 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 12 | 1830.8 | 0.4 | 0.21197 | 0.208627 | 2.3156e-05 | 0.0101822 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 13 | 1833.6 | 0.4 | 0.222222 | 0.220737 | 2.42389e-05 | -0.00092364 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 14 | 1841.7 | 0.4 | 0.224771 | 0.22639 | 2.4409e-05 | 0.00409326 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 15 | 1845.9 | 0.4 | 0.229064 | 0.225442 | 2.48187e-05 | 0.00822743 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 16 | 1850.1 | 0.4 | 0.229064 | 0.224797 | 2.47623e-05 | 0.00897335 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 17 | 1852.7 | 0.4 | 0.22335 | 0.220896 | 2.41108e-05 | 0.00596114 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 18 | 1850.4 | 0.4 | 0.229469 | 0.226375 | 2.48021e-05 | 0.00243921 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 19 | 1845.2 | 0.4 | 0.194896 | 0.195688 | 2.11246e-05 | -0.00264631 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 20 | 1847.7 | 0.4 | 0.210127 | 0.208935 | 2.27447e-05 | -0.00269677 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 21 | 1849 | 0.4 | 0.205195 | 0.21039 | 2.21952e-05 | -0.000751759 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 22 | 1851 | 0.4 | 0.223077 | 0.220211 | 2.41034e-05 | 0.00314011 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 23 | 1854.6 | 0.4 | 0.211443 | 0.216157 | 2.2802e-05 | 0.00373014 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 24 | 1855.8 | 0.4 | 0.205729 | 0.210413 | 2.21715e-05 | 0.0036736 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 25 | 1858.1 | 0.4 | 0.221939 | 0.220588 | 2.38888e-05 | 0.00383129 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 26 | 1861 | 0.4 | 0.222222 | 0.221215 | 2.3882e-05 | 0.00344713 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 27 | 1860.9 | 0.4 | 0.215426 | 0.214453 | 2.31528e-05 | 0.00274636 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 28 | 1859.7 | 0.4 | 0.205729 | 0.208091 | 2.2125e-05 | 0.00086215 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 29 | 1811.5 | 0.4 | 0.211587 | 0.208951 | 2.33604e-05 | -0.0266167 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 30 | 1861.3 | 0.4 | 0.206718 | 0.210702 | 2.22123e-05 | 0.000928021 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 31 | 1859.5 | 0.4 | 0.206186 | 0.207398 | 2.21765e-05 | 0.000605805 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 32 | 1862 | 0.4 | 0.221374 | 0.219994 | 2.37781e-05 | 0.0278684 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 33 | 1860.7 | 0.4 | 0.205195 | 0.207639 | 2.20557e-05 | -0.000320793 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 34 | 1862.1 | 0.4 | 0.205195 | 0.210816 | 2.20391e-05 | 0.00139868 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 35 | 1854.6 | 0.4 | 0.193023 | 0.195622 | 2.08156e-05 | -0.00397348 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 36 | 1854.9 | 0.4 | 0.217507 | 0.216102 | 2.34521e-05 | -0.00311355 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 37 | 1857.2 | 0.4 | 0.221939 | 0.220588 | 2.39004e-05 | -0.00262599 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 38 | 1861.1 | 0.4 | 0.210526 | 0.215097 | 2.26239e-05 | 0.00350165 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 39 | 1858.2 | 0.4 | 0.212121 | 0.20933 | 2.28308e-05 | 0.00178168 |
| 2026-01-01 | NSE | ADANIPORTS | disconnect_scenario | 40 | 1863.6 | 0.4 | 0.216867 | 0.220238 | 2.3274e-05 | 0.00344776 |
