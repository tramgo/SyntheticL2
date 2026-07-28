# Phase214 Event-surprise Conditional Label Materialization

Generated UTC: 2026-07-28T21:34:30.234183+00:00

Phase214 materializes event-surprise conditional labels over train and validation partitions only.
It records sealed test inventory but uses zero sealed test rows and emits no model, replay, P&L, promotion, or profitability claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase214_label_partition_rows | 512 | Materialized train/validation label partition rows |
| phase214_label_rows | 1641001 | Materialized conditional label rows |
| phase214_event_surprise_rows | 130231 | Rows with event-surprise bucket active |
| phase214_quality_rows | 512 | Partition quality rows |
| phase214_quality_pass_rows | 512 | Partition quality rows passed |
| phase214_split_balance_rows | 8 | Split/horizon balance rows |
| phase214_sealed_test_inventory_rows | 128 | Sealed test inventory rows recorded |
| phase214_sealed_test_rows_used | 0 | Sealed test rows used |
| phase214_forbidden_execution_rows | 13 | Forbidden execution rows |
| phase214_gate_rows | 8 | Gates evaluated |
| phase214_hard_gate_rows | 8 | Hard gates evaluated |
| phase214_hard_gate_pass_rows | 8 | Hard gates passed |
| phase214_event_surprise_label_materialization_complete | 1 | 1 means Phase214 completed |
| phase214_model_fit_allowed_next | 0 | No model fit opened |
| phase214_strategy_replay_allowed | 0 | No strategy replay opened |
| phase214_test_replay_allowed_next | 0 | No test replay opened |
| phase214_promotion_allowed | 0 | No promotion opened |
| phase214_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase214_profitability_claim_allowed | 0 | No profitability claim is allowed |
| phase214_forbidden_outputs | model_fit;model_prediction;strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export | Outputs forbidden in this phase |
| phase214_next_best_action | run_phase215_event_surprise_label_quality_interpretation_no_model_no_replay_no_test | Recommended next milestone |

## Train Conditional Baselines

| symbol | horizon_sec | spread_regime | liquidity_regime | receive_event_rate_zscore_bucket | baseline_mid_return_bps | baseline_abs_return_bps | baseline_spread_change_bps | baseline_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ADANIPORTS | 1 | high | high | normal | 0 | 0 | 0 | 1381 |
| ADANIPORTS | 1 | high | high | positive | 0 | 0 | 0 | 94 |
| ADANIPORTS | 1 | high | low | normal | 0 | 0.271227 | 0 | 1870 |
| ADANIPORTS | 1 | high | low | positive | 0 | 0 | 0 | 145 |
| ADANIPORTS | 1 | high | mid | normal | 0 | 0 | 0 | 1919 |
| ADANIPORTS | 1 | high | mid | positive | 0 | 0 | 0 | 127 |
| ADANIPORTS | 1 | low | high | normal | 0 | 0 | 0 | 2645 |
| ADANIPORTS | 1 | low | high | positive | 0 | 0 | 0 | 185 |
| ADANIPORTS | 1 | low | low | normal | 0 | 0 | 0 | 2126 |
| ADANIPORTS | 1 | low | low | positive | 0 | 0 | 0 | 158 |
| ADANIPORTS | 1 | low | mid | normal | 0 | 0 | 0 | 2252 |
| ADANIPORTS | 1 | low | mid | positive | 0 | 0 | 0 | 173 |
| ADANIPORTS | 1 | mid | high | normal | 0 | 0 | 0 | 1758 |
| ADANIPORTS | 1 | mid | high | positive | 0 | 0 | 0 | 111 |
| ADANIPORTS | 1 | mid | low | normal | 0 | 0 | 0 | 1776 |
| ADANIPORTS | 1 | mid | low | positive | 0 | 0 | 0 | 104 |
| ADANIPORTS | 1 | mid | mid | normal | 0 | 0 | 0 | 1776 |
| ADANIPORTS | 1 | mid | mid | positive | 0 | 0 | 0 | 116 |
| ADANIPORTS | 5 | high | high | normal | 0 | 0.546627 | -0.544232 | 599 |
| ADANIPORTS | 5 | high | high | positive | 0 | 0.544247 | -0.547241 | 49 |
| ADANIPORTS | 5 | high | low | normal | 0 | 0.552044 | -0.544558 | 831 |
| ADANIPORTS | 5 | high | low | positive | 0 | 0.542476 | -0.542446 | 77 |
| ADANIPORTS | 5 | high | mid | normal | 0 | 0.550191 | -0.544447 | 844 |
| ADANIPORTS | 5 | high | mid | positive | 0 | 0.553679 | -0.544232 | 65 |
| ADANIPORTS | 5 | low | high | normal | 0 | 0.272732 | 0 | 1168 |
| ADANIPORTS | 5 | low | high | positive | 0 | 0.274959 | 0 | 101 |
| ADANIPORTS | 5 | low | low | normal | 0 | 0.271599 | 0 | 927 |
| ADANIPORTS | 5 | low | low | positive | 0 | 0.136043 | 0 | 84 |
| ADANIPORTS | 5 | low | mid | normal | 0 | 0.273426 | 0 | 1007 |
| ADANIPORTS | 5 | low | mid | positive | 0 | 0.273314 | 0 | 75 |
| ADANIPORTS | 5 | mid | high | normal | 0 | 0.27933 | 0 | 781 |
| ADANIPORTS | 5 | mid | high | positive | 0 | 0.543257 | 0 | 55 |
| ADANIPORTS | 5 | mid | low | normal | 0 | 0.542064 | 0 | 783 |
| ADANIPORTS | 5 | mid | low | positive | 0 | 0.54739 | 0 | 51 |
| ADANIPORTS | 5 | mid | mid | normal | 0 | 0.544173 | 0 | 782 |
| ADANIPORTS | 5 | mid | mid | positive | 0 | 0.276216 | 0 | 62 |
| ADANIPORTS | 15 | high | high | normal | 0.271363 | 1.36874 | -1.09158 | 223 |
| ADANIPORTS | 15 | high | high | positive | -5000.41 | 5000.41 | -6.29688 | 2 |
| ADANIPORTS | 15 | high | low | normal | 0 | 1.37627 | -1.08419 | 327 |
| ADANIPORTS | 15 | high | low | positive | -1.65627 | 1.65627 | 0 | 1 |
| ADANIPORTS | 15 | high | mid | normal | 0 | 1.63041 | -1.09322 | 332 |
| ADANIPORTS | 15 | low | high | normal | 0 | 1.09197 | 0.546478 | 436 |
| ADANIPORTS | 15 | low | high | positive | -3.5865 | 3.5865 | 0.55177 | 1 |
| ADANIPORTS | 15 | low | low | normal | 0 | 0.826754 | 6.14042e-13 | 356 |
| ADANIPORTS | 15 | low | low | positive | -7.15879 | 7.15879 | 1.25209e-12 | 1 |
| ADANIPORTS | 15 | low | mid | normal | 0 | 1.10571 | 0.546844 | 394 |
| ADANIPORTS | 15 | low | mid | positive | -0.550282 | 0.550282 | 0 | 2 |
| ADANIPORTS | 15 | mid | high | normal | 0 | 1.35785 | 0 | 310 |
| ADANIPORTS | 15 | mid | low | normal | -0.270307 | 1.90062 | 0 | 287 |
| ADANIPORTS | 15 | mid | mid | normal | 0 | 1.11869 | 0 | 271 |
| ADANIPORTS | 60 | high | high | normal | -0.273351 | 3.01924 | -1.08846 | 51 |
| ADANIPORTS | 60 | high | high | positive | -10000 | 10000 | -9.84091 | 1 |
| ADANIPORTS | 60 | high | low | normal | -0.95388 | 3.32577 | -1.10453 | 80 |
| ADANIPORTS | 60 | high | mid | normal | -0.137639 | 3.29425 | -1.11568 | 84 |
| ADANIPORTS | 60 | low | high | normal | 0 | 1.90804 | 0.547346 | 104 |
| ADANIPORTS | 60 | low | low | normal | 0 | 1.91262 | 0.545971 | 79 |
| ADANIPORTS | 60 | low | mid | normal | 0 | 2.75931 | 1.08404 | 91 |
| ADANIPORTS | 60 | mid | high | normal | -0.544203 | 2.77647 | 0 | 89 |
| ADANIPORTS | 60 | mid | low | normal | -0.408934 | 3.54771 | 0 | 86 |
| ADANIPORTS | 60 | mid | mid | normal | 0.825855 | 2.99255 | 0 | 75 |
| AXISBANK | 1 | high | high | normal | 0 | 0 | 0 | 1626 |
| AXISBANK | 1 | high | high | positive | 0 | 0 | 0 | 79 |
| AXISBANK | 1 | high | low | normal | 0 | 0.378043 | 0 | 2514 |
| AXISBANK | 1 | high | low | positive | 0 | 0 | 0 | 144 |
| AXISBANK | 1 | high | mid | normal | 0 | 0 | 0 | 2376 |
| AXISBANK | 1 | high | mid | positive | 0 | 0 | 0 | 97 |
| AXISBANK | 1 | low | high | normal | 0 | 0 | 0 | 3516 |
| AXISBANK | 1 | low | high | positive | 0 | 0 | 0 | 139 |
| AXISBANK | 1 | low | low | normal | 0 | 0 | 0 | 2810 |
| AXISBANK | 1 | low | low | positive | 0 | 0 | 0 | 152 |
| AXISBANK | 1 | low | mid | normal | 0 | 0 | 0 | 2966 |
| AXISBANK | 1 | low | mid | positive | 0 | 0 | 0 | 151 |
| AXISBANK | 1 | mid | high | normal | 0 | 0 | 0 | 2461 |
| AXISBANK | 1 | mid | high | positive | 0 | 0 | 0 | 123 |
| AXISBANK | 1 | mid | low | normal | 0 | 0 | 0 | 2227 |
| AXISBANK | 1 | mid | low | positive | 0 | 0 | 0 | 99 |
| AXISBANK | 1 | mid | mid | normal | 0 | 0 | 0 | 2486 |
| AXISBANK | 1 | mid | mid | positive | 0 | 0 | 0 | 110 |
| AXISBANK | 5 | high | high | normal | 0 | 0.757117 | -0.756487 | 573 |
| AXISBANK | 5 | high | high | positive | 0.18905 | 0.761211 | -0.757535 | 40 |
| AXISBANK | 5 | high | low | normal | 0 | 0.754973 | -0.757978 | 860 |
| AXISBANK | 5 | high | low | positive | 0 | 0.757978 | -0.757475 | 68 |
| AXISBANK | 5 | high | mid | normal | 0 | 0.384438 | -0.757547 | 801 |
| AXISBANK | 5 | high | mid | positive | 0 | 0.757805 | -0.758352 | 44 |
| AXISBANK | 5 | low | high | normal | 0 | 0.3796 | 0 | 1256 |
| AXISBANK | 5 | low | high | positive | 0 | 0.378468 | 0 | 60 |
| AXISBANK | 5 | low | low | normal | 0 | 0.380011 | 0 | 1001 |
| AXISBANK | 5 | low | low | positive | 0 | 0.379169 | 0 | 78 |
| AXISBANK | 5 | low | mid | normal | 0 | 0.37896 | 0 | 1051 |
| AXISBANK | 5 | low | mid | positive | 0 | 0.755601 | 1.72449e-12 | 73 |
| AXISBANK | 5 | mid | high | normal | 0 | 0.383465 | 0 | 841 |
| AXISBANK | 5 | mid | high | positive | 0 | 0.383818 | 0 | 45 |
| AXISBANK | 5 | mid | low | normal | 0 | 0.383465 | 0 | 757 |
| AXISBANK | 5 | mid | low | positive | 0 | 0.383465 | 0 | 52 |
| AXISBANK | 5 | mid | mid | normal | 0 | 0.38323 | 0 | 870 |
| AXISBANK | 5 | mid | mid | positive | 0 | 0.383642 | 0 | 61 |
| AXISBANK | 15 | high | high | normal | 0.378874 | 1.53087 | -0.768551 | 217 |
| AXISBANK | 15 | high | low | normal | 0 | 1.52248 | -0.762835 | 341 |
| AXISBANK | 15 | high | mid | normal | 0 | 1.1377 | -0.759965 | 301 |
| AXISBANK | 15 | high | mid | positive | 0 | 0 | 0 | 1 |
| AXISBANK | 15 | low | high | normal | 0 | 1.13813 | 1.75044e-12 | 505 |
| AXISBANK | 15 | low | low | normal | 0 | 1.1515 | 1.74299e-12 | 380 |
| AXISBANK | 15 | low | mid | normal | 0 | 1.13878 | 1.74306e-12 | 439 |
| AXISBANK | 15 | mid | high | normal | 0 | 1.14987 | 0 | 250 |
| AXISBANK | 15 | mid | low | normal | 0 | 1.15554 | -1.71901e-12 | 251 |
| AXISBANK | 15 | mid | mid | normal | 0 | 1.15123 | 0 | 258 |
| AXISBANK | 60 | high | high | normal | -0.189746 | 3.0702 | -1.51604 | 62 |
| AXISBANK | 60 | high | low | normal | -0.381971 | 3.79838 | -1.51659 | 93 |
| AXISBANK | 60 | high | mid | normal | -0.189638 | 3.25564 | -0.770795 | 64 |
| AXISBANK | 60 | low | high | normal | 0 | 3.0341 | 0.758093 | 115 |
| AXISBANK | 60 | low | low | normal | -1.51432 | 3.80902 | 0.757217 | 98 |
| AXISBANK | 60 | low | mid | normal | 0 | 2.65343 | 0.750076 | 112 |
| AXISBANK | 60 | mid | high | normal | 0.189387 | 3.60954 | 0 | 68 |
| AXISBANK | 60 | mid | low | normal | 0 | 2.84444 | 0 | 54 |
| AXISBANK | 60 | mid | mid | normal | 0 | 2.6968 | -0.757748 | 74 |
| BAJAJ-AUTO | 1 | high | high | normal | 0 | 0.243971 | 0 | 1430 |
| BAJAJ-AUTO | 1 | high | high | positive | 0 | 0.122312 | 0 | 96 |
| BAJAJ-AUTO | 1 | high | low | normal | 0 | 0.245179 | 0 | 1690 |
| BAJAJ-AUTO | 1 | high | low | positive | 0 | 0 | 0 | 115 |
| BAJAJ-AUTO | 1 | high | mid | normal | 0 | 0.244523 | 0 | 1657 |
| BAJAJ-AUTO | 1 | high | mid | positive | 0 | 0 | 0 | 96 |
| BAJAJ-AUTO | 1 | low | high | normal | 0 | 0 | 0 | 2527 |
| BAJAJ-AUTO | 1 | low | high | positive | 0 | 0 | 0 | 148 |
| BAJAJ-AUTO | 1 | low | low | normal | 0 | 0 | 0 | 2338 |
| BAJAJ-AUTO | 1 | low | low | positive | 0 | 0 | 0 | 120 |
| BAJAJ-AUTO | 1 | low | mid | normal | 0 | 0 | 0 | 2451 |
| BAJAJ-AUTO | 1 | low | mid | positive | 0 | 0 | 0 | 166 |
| BAJAJ-AUTO | 1 | mid | high | normal | 0 | 0 | 0 | 1662 |
| BAJAJ-AUTO | 1 | mid | high | positive | 0 | 0 | 0 | 104 |
| BAJAJ-AUTO | 1 | mid | low | normal | 0 | 0 | 0 | 1616 |
| BAJAJ-AUTO | 1 | mid | low | positive | 0 | 0 | 0 | 100 |
| BAJAJ-AUTO | 1 | mid | mid | normal | 0 | 0 | 0 | 1689 |
| BAJAJ-AUTO | 1 | mid | mid | positive | 0 | 0 | 0 | 94 |
| BAJAJ-AUTO | 5 | high | high | normal | 0 | 0.491485 | -0.489884 | 612 |
| BAJAJ-AUTO | 5 | high | high | positive | 0 | 0.490533 | -0.490942 | 61 |
| BAJAJ-AUTO | 5 | high | low | normal | 0 | 0.491618 | -0.490436 | 727 |
| BAJAJ-AUTO | 5 | high | low | positive | 0 | 0.73364 | -0.489464 | 77 |
| BAJAJ-AUTO | 5 | high | mid | normal | 0 | 0.491739 | -0.488329 | 715 |
| BAJAJ-AUTO | 5 | high | mid | positive | 0 | 0.490701 | 0 | 59 |
| BAJAJ-AUTO | 5 | low | high | normal | 0 | 0.245812 | 0 | 928 |
| BAJAJ-AUTO | 5 | low | high | positive | 0 | 0.246281 | 0 | 60 |
| BAJAJ-AUTO | 5 | low | low | normal | 0 | 0.246169 | 0 | 812 |
| BAJAJ-AUTO | 5 | low | low | positive | 0 | 0.246548 | 0 | 61 |
| BAJAJ-AUTO | 5 | low | mid | normal | 0 | 0.245706 | 0 | 899 |
| BAJAJ-AUTO | 5 | low | mid | positive | 0 | 0.246585 | 0 | 79 |
| BAJAJ-AUTO | 5 | mid | high | normal | 0 | 0.246196 | 0 | 970 |
| BAJAJ-AUTO | 5 | mid | high | positive | 0 | 0.246999 | 0 | 71 |
| BAJAJ-AUTO | 5 | mid | low | normal | 0 | 0.246148 | 0 | 931 |
| BAJAJ-AUTO | 5 | mid | low | positive | 0 | 0.245555 | 0 | 95 |
| BAJAJ-AUTO | 5 | mid | mid | normal | 0 | 0.2465 | 0 | 947 |
| BAJAJ-AUTO | 5 | mid | mid | positive | 0 | 0.489951 | 0 | 82 |
| BAJAJ-AUTO | 15 | high | high | normal | 0 | 1.23297 | -0.977829 | 256 |
| BAJAJ-AUTO | 15 | high | high | positive | -5000.61 | 5000.61 | -3.19918 | 2 |
| BAJAJ-AUTO | 15 | high | low | normal | 0 | 1.23265 | -0.978905 | 289 |
| BAJAJ-AUTO | 15 | high | mid | normal | 0 | 0.986315 | -0.981595 | 271 |
| BAJAJ-AUTO | 15 | high | mid | positive | 0.737137 | 0.737137 | 0.491425 | 1 |
| BAJAJ-AUTO | 15 | low | high | normal | 0 | 1.22419 | 0.492078 | 376 |
| BAJAJ-AUTO | 15 | low | high | positive | 0.490244 | 0.490244 | 0 | 3 |
| BAJAJ-AUTO | 15 | low | low | normal | 0 | 1.22618 | 0.978645 | 340 |
| BAJAJ-AUTO | 15 | low | low | positive | 3.42248 | 3.42248 | 2.93355 | 3 |
| BAJAJ-AUTO | 15 | low | mid | normal | 0 | 0.984628 | 0.492641 | 358 |
| BAJAJ-AUTO | 15 | low | mid | positive | -1.35576 | 1.60282 | 1.23224 | 2 |
| BAJAJ-AUTO | 15 | mid | high | normal | 0 | 0.981319 | 0 | 334 |
| BAJAJ-AUTO | 15 | mid | high | positive | 0 | 0 | 0 | 1 |
| BAJAJ-AUTO | 15 | mid | low | normal | 0 | 0.982053 | 0 | 339 |
| BAJAJ-AUTO | 15 | mid | low | positive | 1.10624 | 1.10624 | -1.23079 | 2 |
| BAJAJ-AUTO | 15 | mid | mid | normal | -0.244022 | 0.983974 | 0 | 362 |
| BAJAJ-AUTO | 15 | mid | mid | positive | -1.23067 | 2.70275 | -0.492108 | 4 |
| BAJAJ-AUTO | 60 | high | high | normal | 0.491594 | 2.21359 | -0.492611 | 63 |
| BAJAJ-AUTO | 60 | high | high | positive | -10000 | 10000 | -3.93972 | 1 |
| BAJAJ-AUTO | 60 | high | low | normal | -0.984204 | 3.67972 | -1.47765 | 73 |
| BAJAJ-AUTO | 60 | high | mid | normal | 0.245628 | 3.41314 | -0.982946 | 75 |
| BAJAJ-AUTO | 60 | low | high | normal | 0.368075 | 3.07869 | 1.4637 | 88 |
| BAJAJ-AUTO | 60 | low | low | normal | 0 | 2.33245 | 0.984955 | 80 |
| BAJAJ-AUTO | 60 | low | mid | normal | 0 | 3.19957 | 0.983974 | 86 |
| BAJAJ-AUTO | 60 | mid | high | normal | -0.736865 | 2.69707 | 0 | 93 |
| BAJAJ-AUTO | 60 | mid | low | normal | 0 | 2.95789 | 0 | 92 |
| BAJAJ-AUTO | 60 | mid | mid | normal | -0.49255 | 2.46536 | -0.489608 | 89 |
| BANKBEES | 1 | high | high | normal | 0 | 0.0841425 | 0 | 2279 |
| BANKBEES | 1 | high | high | positive | 0 | 0.0833451 | 0 | 145 |
| BANKBEES | 1 | high | low | normal | 0 | 0.0842194 | 0 | 2332 |
| BANKBEES | 1 | high | low | positive | 0 | 0.08423 | 0 | 138 |
| BANKBEES | 1 | high | mid | normal | 0 | 0.0842708 | 0 | 2388 |
| BANKBEES | 1 | high | mid | positive | 0 | 0.0833948 | 0 | 158 |
| BANKBEES | 1 | low | high | normal | 0 | 0 | 0 | 2450 |
| BANKBEES | 1 | low | high | positive | 0 | 0 | 0 | 170 |
| BANKBEES | 1 | low | low | normal | 0 | 0 | 0 | 2690 |
| BANKBEES | 1 | low | low | positive | 0 | 0 | 0 | 150 |
| BANKBEES | 1 | low | mid | normal | 0 | 0 | 0 | 2687 |
| BANKBEES | 1 | low | mid | positive | 0 | 0 | 0 | 158 |
| BANKBEES | 1 | mid | high | normal | 0 | 0 | 0 | 2576 |
| BANKBEES | 1 | mid | high | positive | 0 | 0 | 0 | 219 |
| BANKBEES | 1 | mid | low | normal | 0 | 0 | 0 | 2380 |
| BANKBEES | 1 | mid | low | positive | 0 | 0.083568 | 0 | 153 |
| BANKBEES | 1 | mid | mid | normal | 0 | 0.0832619 | 0 | 2529 |
| BANKBEES | 1 | mid | mid | positive | 0 | 0 | 0 | 157 |
| BANKBEES | 5 | high | high | normal | 0 | 0.250959 | -0.166461 | 816 |
| BANKBEES | 5 | high | high | positive | 0 | 0.336967 | -0.337145 | 62 |
| BANKBEES | 5 | high | low | normal | 0 | 0.250774 | -0.166696 | 826 |
| BANKBEES | 5 | high | low | positive | 0 | 0.252622 | -0.336724 | 52 |
| BANKBEES | 5 | high | mid | normal | 0 | 0.252561 | -0.16701 | 848 |
| BANKBEES | 5 | high | mid | positive | 0 | 0.249688 | -0.167099 | 54 |
| BANKBEES | 5 | low | high | normal | 0 | 0.166763 | 0 | 883 |
| BANKBEES | 5 | low | high | positive | 0 | 0.166549 | 0 | 55 |
| BANKBEES | 5 | low | low | normal | 0 | 0.0835827 | 0 | 928 |
| BANKBEES | 5 | low | low | positive | 0 | 0.0837852 | 0 | 70 |
| BANKBEES | 5 | low | mid | normal | 0 | 0.166461 | 0 | 921 |
| BANKBEES | 5 | low | mid | positive | 0 | 0.168805 | 0 | 50 |
| BANKBEES | 5 | mid | high | normal | 0 | 0.167027 | 0 | 865 |
| BANKBEES | 5 | mid | high | positive | 0 | 0.209304 | 0 | 70 |
| BANKBEES | 5 | mid | low | normal | 0 | 0.167084 | 0 | 823 |
| BANKBEES | 5 | mid | low | positive | 0 | 0.16853 | 0 | 52 |
| BANKBEES | 5 | mid | mid | normal | 0 | 0.168418 | 0 | 906 |
| BANKBEES | 5 | mid | mid | positive | 0 | 0.336512 | 0 | 54 |
| BANKBEES | 15 | high | high | normal | 0 | 0.668215 | -0.499908 | 313 |
| BANKBEES | 15 | high | low | normal | 0 | 0.588948 | -0.337476 | 307 |
| BANKBEES | 15 | high | mid | normal | 0 | 0.58899 | -0.337355 | 330 |
| BANKBEES | 15 | low | high | normal | 0 | 0.420975 | 0.170223 | 355 |
| BANKBEES | 15 | low | low | normal | 0 | 0.417885 | 0.167012 | 365 |
| BANKBEES | 15 | low | mid | normal | 0 | 0.668078 | 0.333955 | 342 |
| BANKBEES | 15 | mid | high | normal | 0 | 0.505591 | 0 | 304 |
| BANKBEES | 15 | mid | low | normal | 0 | 0.421122 | 0 | 302 |
| BANKBEES | 15 | mid | mid | normal | 0 | 0.501505 | 0 | 325 |
| BANKBEES | 60 | high | high | normal | -0.423967 | 1.49917 | -0.837386 | 74 |
| BANKBEES | 60 | high | low | normal | -0.167044 | 1.42049 | -0.842481 | 75 |
| BANKBEES | 60 | high | mid | normal | -0.0835471 | 1.25122 | -1.01092 | 90 |
| BANKBEES | 60 | low | high | normal | 0 | 1.6664 | 0.677197 | 84 |
| BANKBEES | 60 | low | low | normal | 0 | 1.43158 | 0.503073 | 84 |
| BANKBEES | 60 | low | mid | normal | 0.167666 | 2.02012 | 0.846539 | 90 |
| BANKBEES | 60 | mid | high | normal | -0.0833709 | 1.42364 | 0.166776 | 86 |
| BANKBEES | 60 | mid | low | normal | 0 | 1.34829 | -0.167136 | 85 |
| BANKBEES | 60 | mid | mid | normal | -0.336953 | 1.178 | 1.89744e-12 | 71 |
| BHARTIARTL | 1 | high | high | normal | 0 | 0.260464 | 0 | 1585 |
| BHARTIARTL | 1 | high | high | positive | 0 | 0.259848 | 0 | 125 |
| BHARTIARTL | 1 | high | low | normal | 0 | 0.261308 | 0 | 2291 |
| BHARTIARTL | 1 | high | low | positive | 0 | 0.261465 | 0 | 164 |
| BHARTIARTL | 1 | high | mid | normal | 0 | 0.261063 | 0 | 2198 |
| BHARTIARTL | 1 | high | mid | positive | 0 | 0.261626 | -0.255951 | 170 |
| BHARTIARTL | 1 | low | high | normal | 0 | 0 | 0 | 3462 |
| BHARTIARTL | 1 | low | high | positive | 0 | 0 | 0 | 246 |
| BHARTIARTL | 1 | low | low | normal | 0 | 0 | 0 | 2931 |
| BHARTIARTL | 1 | low | low | positive | 0 | 0 | 0 | 201 |
| BHARTIARTL | 1 | low | mid | normal | 0 | 0 | 0 | 3020 |
| BHARTIARTL | 1 | low | mid | positive | 0 | 0 | 0 | 177 |
| BHARTIARTL | 1 | mid | high | normal | 0 | 0.255751 | 0 | 2558 |
| BHARTIARTL | 1 | mid | high | positive | 0 | 0.259128 | 0 | 184 |
| BHARTIARTL | 1 | mid | low | normal | 0 | 0.258244 | 0 | 2399 |
| BHARTIARTL | 1 | mid | low | positive | 0 | 0.258251 | 0 | 175 |
| BHARTIARTL | 1 | mid | mid | normal | 0 | 0 | 0 | 2661 |
| BHARTIARTL | 1 | mid | mid | positive | 0 | 0.255754 | 0 | 181 |
| BHARTIARTL | 5 | high | high | normal | 0 | 0.523334 | -0.521451 | 610 |
| BHARTIARTL | 5 | high | high | positive | 0 | 0.782207 | -1.0352 | 72 |
| BHARTIARTL | 5 | high | low | normal | 0 | 0.776247 | -0.52276 | 824 |
| BHARTIARTL | 5 | high | low | positive | 0 | 0.77689 | -1.04508 | 96 |
| BHARTIARTL | 5 | high | mid | normal | 0 | 0.523629 | -0.522398 | 859 |
| BHARTIARTL | 5 | high | mid | positive | 0 | 1.04131 | -1.03351 | 93 |
| BHARTIARTL | 5 | low | high | normal | 0 | 0.260845 | 0 | 1009 |
| BHARTIARTL | 5 | low | high | positive | 0 | 0.261301 | 0 | 115 |
| BHARTIARTL | 5 | low | low | normal | 0 | 0 | 0 | 812 |
| BHARTIARTL | 5 | low | low | positive | 0 | 0.517451 | 1.16845e-12 | 95 |
| BHARTIARTL | 5 | low | mid | normal | 0 | 0 | 0 | 816 |
| BHARTIARTL | 5 | low | mid | positive | 0 | 0.516596 | 1.17091e-12 | 104 |
| BHARTIARTL | 5 | mid | high | normal | 0 | 0.265006 | 0 | 890 |
| BHARTIARTL | 5 | mid | high | positive | 0 | 0.777656 | 0 | 116 |
| BHARTIARTL | 5 | mid | low | normal | 0 | 0.517337 | 0 | 876 |
| BHARTIARTL | 5 | mid | low | positive | 0 | 0.778314 | 0 | 110 |
| BHARTIARTL | 5 | mid | mid | normal | 0 | 0.265509 | 0 | 906 |
| BHARTIARTL | 5 | mid | mid | positive | 0 | 0.774254 | 0 | 122 |
| BHARTIARTL | 15 | high | high | normal | 0 | 1.04737 | -1.04447 | 228 |
| BHARTIARTL | 15 | high | high | positive | -1.2949 | 1.2949 | -1.55388 | 1 |
| BHARTIARTL | 15 | high | low | normal | 0 | 1.56697 | -1.04402 | 330 |
| BHARTIARTL | 15 | high | mid | normal | 0 | 1.30828 | -1.03748 | 331 |
| BHARTIARTL | 15 | high | mid | positive | -3.61421 | 3.61421 | -2.06526 | 3 |
| BHARTIARTL | 15 | low | high | normal | 0 | 0.783147 | 1.174e-12 | 413 |
| BHARTIARTL | 15 | low | high | positive | -3.89621 | 3.89621 | 2.59747 | 1 |
| BHARTIARTL | 15 | low | low | normal | 0 | 1.0363 | 1.18427e-12 | 321 |
| BHARTIARTL | 15 | low | low | positive | 0.775094 | 0.775094 | 0.516729 | 3 |
| BHARTIARTL | 15 | low | mid | normal | 0 | 0.531816 | 1.17685e-12 | 301 |
| BHARTIARTL | 15 | mid | high | normal | 0 | 1.03391 | 0 | 328 |
| BHARTIARTL | 15 | mid | high | positive | -1.80515 | 1.80515 | -0.515756 | 1 |
| BHARTIARTL | 15 | mid | low | normal | 0 | 1.30634 | 0 | 315 |
| BHARTIARTL | 15 | mid | low | positive | -0.258278 | 2.33179 | 0.517679 | 3 |
| BHARTIARTL | 15 | mid | mid | normal | 0 | 1.29581 | 0 | 362 |
| BHARTIARTL | 15 | mid | mid | positive | 0.775251 | 0.775251 | 0.518636 | 2 |
| BHARTIARTL | 60 | high | high | normal | 1.05292 | 3.60124 | -1.56695 | 52 |
| BHARTIARTL | 60 | high | low | normal | 0 | 4.13864 | -1.04698 | 77 |
| BHARTIARTL | 60 | high | mid | normal | -1.04682 | 3.87237 | -1.0475 | 63 |
| BHARTIARTL | 60 | low | high | normal | 0 | 1.44639 | 0.256812 | 108 |
| BHARTIARTL | 60 | low | low | normal | 0 | 2.86832 | 0.521663 | 70 |
| BHARTIARTL | 60 | low | mid | normal | 0 | 1.82916 | 1.18427e-12 | 75 |
| BHARTIARTL | 60 | mid | high | normal | -0.260444 | 2.09008 | 1.18147e-12 | 85 |
| BHARTIARTL | 60 | mid | low | normal | 0.651319 | 2.60075 | 0 | 98 |
| BHARTIARTL | 60 | mid | mid | normal | 0.261069 | 2.97985 | 0 | 112 |
| BPCL | 1 | high | high | normal | 0 | 0 | 0 | 827 |
| BPCL | 1 | high | high | positive | 0 | 0 | 0 | 45 |
| BPCL | 1 | high | low | normal | 0 | 0 | 0 | 1088 |
| BPCL | 1 | high | low | positive | 0 | 0 | 0 | 51 |
| BPCL | 1 | high | mid | normal | 0 | 0 | 0 | 991 |
| BPCL | 1 | high | mid | positive | 0 | 0 | 0 | 43 |
| BPCL | 1 | low | high | normal | 0 | 0 | 0 | 2319 |
| BPCL | 1 | low | high | positive | 0 | 0 | 0 | 100 |
| BPCL | 1 | low | low | normal | 0 | 0 | 0 | 2292 |
| BPCL | 1 | low | low | positive | 0 | 0 | 0 | 94 |
| BPCL | 1 | low | mid | normal | 0 | 0 | 0 | 2305 |
| BPCL | 1 | low | mid | positive | 0 | 0 | 0 | 85 |
| BPCL | 1 | mid | high | normal | 0 | 0 | 0 | 1353 |
| BPCL | 1 | mid | high | positive | 0 | 0 | 0 | 76 |
| BPCL | 1 | mid | low | normal | 0 | 0 | 0 | 1127 |
| BPCL | 1 | mid | low | positive | 0 | 0 | 0 | 70 |
| BPCL | 1 | mid | mid | normal | 0 | 0 | 0 | 1349 |
| BPCL | 1 | mid | mid | positive | 0 | 0 | 0 | 91 |
| BPCL | 5 | high | high | normal | 0 | 0 | 0 | 446 |
| BPCL | 5 | high | high | positive | 0 | 0.802246 | 0 | 29 |
| BPCL | 5 | high | low | normal | 0 | 1.81943e-12 | 0 | 599 |
| BPCL | 5 | high | low | positive | 0 | 0.801668 | -0.801346 | 26 |
| BPCL | 5 | high | mid | normal | 0 | 0.800448 | 0 | 540 |
| BPCL | 5 | high | mid | positive | 0 | 0 | 0 | 24 |
| BPCL | 5 | low | high | normal | 0 | 0 | 0 | 1333 |
| BPCL | 5 | low | high | positive | 0 | 0.804505 | 0 | 54 |
| BPCL | 5 | low | low | normal | 0 | 0 | 0 | 1308 |
| BPCL | 5 | low | low | positive | 0 | 0 | 0 | 58 |
| BPCL | 5 | low | mid | normal | 0 | 0 | 0 | 1344 |
| BPCL | 5 | low | mid | positive | 0 | 0 | 0 | 37 |
| BPCL | 5 | mid | high | normal | 0 | 0 | 0 | 763 |
| BPCL | 5 | mid | high | positive | 0 | 0 | 0 | 39 |
| BPCL | 5 | mid | low | normal | 0 | 0 | 0 | 639 |
| BPCL | 5 | mid | low | positive | 0 | 0 | 0 | 36 |
| BPCL | 5 | mid | mid | normal | 0 | 0 | 0 | 753 |
| BPCL | 5 | mid | mid | positive | 0 | 0 | 0 | 44 |
| BPCL | 15 | high | high | normal | 0 | 0.815395 | -1.87705e-12 | 180 |
| BPCL | 15 | high | high | positive | 0 | 0 | 0 | 1 |
| BPCL | 15 | high | low | normal | 0 | 0.824946 | -1.60359 | 216 |
| BPCL | 15 | high | mid | normal | 0 | 0.813935 | -1.60398 | 207 |
| BPCL | 15 | high | mid | positive | 3.24867 | 3.24867 | 0.0114859 | 2 |
| BPCL | 15 | low | high | normal | 0 | 0 | 0 | 470 |
| BPCL | 15 | low | low | normal | 0 | 0.821355 | 0 | 469 |
| BPCL | 15 | low | low | positive | 0.00451382 | 1.21988 | 1.61765 | 4 |
| BPCL | 15 | low | mid | normal | 0 | 0.801603 | 0 | 461 |
| BPCL | 15 | mid | high | normal | 0 | 0.805412 | 0 | 321 |
| BPCL | 15 | mid | low | normal | 0 | 0.811985 | 0 | 282 |
| BPCL | 15 | mid | low | positive | -3.20616 | 3.20616 | 1.82249e-12 | 1 |
| BPCL | 15 | mid | mid | normal | 0 | 0.805607 | 0 | 324 |
| BPCL | 15 | mid | mid | positive | -1.62641 | 1.62641 | 0 | 5 |
| BPCL | 60 | high | high | normal | 0 | 1.62061 | -3.21466 | 34 |
| BPCL | 60 | high | low | normal | -0.804699 | 3.25336 | -1.61711 | 50 |
| BPCL | 60 | high | mid | normal | -1.82967e-12 | 1.62747 | -1.62787 | 53 |
| BPCL | 60 | low | high | normal | 0 | 1.61108 | 1.83144e-12 | 126 |
| BPCL | 60 | low | low | normal | 0 | 2.41371 | 1.82703e-12 | 109 |
| BPCL | 60 | low | mid | normal | -0.400802 | 2.45533 | 0 | 112 |
| BPCL | 60 | mid | high | normal | 0 | 2.40539 | 0 | 85 |
| BPCL | 60 | mid | low | normal | 0 | 2.44051 | -1.83357e-12 | 86 |
| BPCL | 60 | mid | mid | normal | -9.25261e-13 | 2.4615 | 0 | 84 |
| BPCL | 60 | mid | mid | positive | -3.25309 | 3.25309 | 1.84917e-12 | 1 |
| BRITANNIA | 1 | high | high | normal | 0 | 0 | 0 | 802 |
| BRITANNIA | 1 | high | high | positive | 0 | 0 | 0 | 132 |
| BRITANNIA | 1 | high | low | normal | 0 | 0 | 0 | 1263 |
| BRITANNIA | 1 | high | low | positive | 0 | 0 | 0 | 234 |
| BRITANNIA | 1 | high | mid | normal | 0 | 0 | 0 | 1162 |
| BRITANNIA | 1 | high | mid | positive | 0 | 0 | 0 | 186 |
| BRITANNIA | 1 | low | high | normal | 0 | 0 | 0 | 1773 |
| BRITANNIA | 1 | low | high | positive | 0 | 0 | 0 | 288 |
| BRITANNIA | 1 | low | low | normal | 0 | 0 | 0 | 1437 |
| BRITANNIA | 1 | low | low | positive | 0 | 0 | 0 | 242 |
| BRITANNIA | 1 | low | mid | normal | 0 | 0 | 0 | 1537 |
| BRITANNIA | 1 | low | mid | positive | 0 | 0 | 0 | 245 |
| BRITANNIA | 1 | mid | high | normal | 0 | 0 | 0 | 927 |
| BRITANNIA | 1 | mid | high | positive | 0 | 0 | 0 | 171 |
| BRITANNIA | 1 | mid | low | normal | 0 | 0 | 0 | 789 |
| BRITANNIA | 1 | mid | low | positive | 0 | 0 | 0 | 133 |
| BRITANNIA | 1 | mid | mid | normal | 0 | 0 | 0 | 931 |
| BRITANNIA | 1 | mid | mid | positive | 0 | 0 | 0 | 157 |
| BRITANNIA | 5 | high | high | normal | 0 | 0 | 0 | 520 |
| BRITANNIA | 5 | high | high | positive | 0 | 0.466266 | 0 | 94 |
| BRITANNIA | 5 | high | low | normal | 0 | 0 | 0 | 806 |
| BRITANNIA | 5 | high | low | positive | 0 | 0.465506 | 0 | 168 |
| BRITANNIA | 5 | high | mid | normal | 0 | 0 | 0 | 752 |
| BRITANNIA | 5 | high | mid | positive | 0 | 0.464965 | 0 | 128 |
| BRITANNIA | 5 | low | high | normal | 0 | 0 | 0 | 1091 |
| BRITANNIA | 5 | low | high | positive | 0 | 0.465962 | 0 | 187 |
| BRITANNIA | 5 | low | low | normal | 0 | 0 | 0 | 858 |
| BRITANNIA | 5 | low | low | positive | 0 | 0.466374 | 0 | 157 |
| BRITANNIA | 5 | low | mid | normal | 0 | 0 | 0 | 943 |
| BRITANNIA | 5 | low | mid | positive | 0 | 0.466298 | 0 | 164 |
| BRITANNIA | 5 | mid | high | normal | 0 | 0 | 0 | 562 |
| BRITANNIA | 5 | mid | high | positive | 0 | 0.465831 | 0 | 121 |
| BRITANNIA | 5 | mid | low | normal | 0 | 0 | 0 | 486 |
| BRITANNIA | 5 | mid | low | positive | 0 | 0.465224 | 0 | 102 |
| BRITANNIA | 5 | mid | mid | normal | 0 | 0 | 0 | 547 |
| BRITANNIA | 5 | mid | mid | positive | 0 | 0.467356 | 0 | 120 |
| BRITANNIA | 15 | high | high | normal | 0 | 0.926721 | -0.931034 | 214 |
| BRITANNIA | 15 | high | high | positive | 0 | 0.929066 | 0 | 25 |
| BRITANNIA | 15 | high | low | normal | 0 | 0.470544 | -0.928117 | 323 |
| BRITANNIA | 15 | high | low | positive | 0 | 0.69885 | -0.932988 | 28 |
| BRITANNIA | 15 | high | mid | normal | 0 | 0.471476 | 0 | 312 |
| BRITANNIA | 15 | high | mid | positive | 0 | 0.465962 | -0.928679 | 24 |
| BRITANNIA | 15 | low | high | normal | 0 | 0.470466 | 0 | 452 |
| BRITANNIA | 15 | low | high | positive | 0 | 0.930384 | 0.929908 | 36 |
| BRITANNIA | 15 | low | low | normal | 0 | 0.93112 | 0 | 362 |
| BRITANNIA | 15 | low | low | positive | 0 | 0.929822 | 0 | 28 |
| BRITANNIA | 15 | low | mid | normal | 0 | 0.466374 | 0 | 379 |
| BRITANNIA | 15 | low | mid | positive | 0 | 0.932642 | 0 | 32 |
| BRITANNIA | 15 | mid | high | normal | 0 | 0.467552 | 0 | 216 |
| BRITANNIA | 15 | mid | high | positive | 0 | 0.931663 | 0 | 27 |
| BRITANNIA | 15 | mid | low | normal | 0 | 0.466614 | 0 | 210 |
| BRITANNIA | 15 | mid | low | positive | -0.466244 | 1.39496 | -0.929195 | 21 |
| BRITANNIA | 15 | mid | mid | normal | 0 | 0.9298 | 0 | 228 |
| BRITANNIA | 15 | mid | mid | positive | 0 | 0.929562 | 0 | 24 |
| BRITANNIA | 60 | high | high | normal | 0.231481 | 1.86099 | -1.8609 | 30 |
| BRITANNIA | 60 | high | low | normal | -0.464048 | 2.32944 | -0.933445 | 56 |
| BRITANNIA | 60 | high | low | positive | -4996.51 | 5003.49 | -5.14281 | 2 |
| BRITANNIA | 60 | high | mid | normal | -0.464868 | 1.86047 | -1.85408 | 46 |
| BRITANNIA | 60 | low | high | normal | -0.232385 | 2.33727 | 0 | 118 |
| BRITANNIA | 60 | low | high | positive | 0.931663 | 1.86194 | 0.930665 | 7 |
| BRITANNIA | 60 | low | low | normal | 0 | 1.41196 | 0.931446 | 95 |
| BRITANNIA | 60 | low | low | positive | 0.936373 | 0.936373 | 3.71713 | 3 |
| BRITANNIA | 60 | low | mid | normal | 0 | 2.32656 | 0.933315 | 113 |
| BRITANNIA | 60 | low | mid | positive | 0 | 1.86038 | 0 | 5 |
| BRITANNIA | 60 | mid | high | normal | 0.464598 | 2.32721 | -0.929023 | 89 |
| BRITANNIA | 60 | mid | high | positive | 0.933228 | 0.933228 | 0 | 1 |
| BRITANNIA | 60 | mid | low | normal | 0 | 1.40089 | -0.926612 | 85 |
| BRITANNIA | 60 | mid | low | positive | -0.933686 | 1.63301 | -0.00101985 | 4 |
| BRITANNIA | 60 | mid | mid | normal | 0 | 1.3975 | 0 | 84 |
| BRITANNIA | 60 | mid | mid | positive | -1.39639 | 1.39639 | 0.930925 | 1 |
| CIPLA | 1 | high | high | normal | 0 | 0 | 0 | 1049 |
| CIPLA | 1 | high | high | positive | 0 | 0 | 0 | 66 |
| CIPLA | 1 | high | low | normal | 0 | 0 | 0 | 1556 |
| CIPLA | 1 | high | low | positive | 0 | 0 | 0 | 103 |
| CIPLA | 1 | high | mid | normal | 0 | 0 | 0 | 1411 |
| CIPLA | 1 | high | mid | positive | 0 | 0 | 0 | 79 |
| CIPLA | 1 | low | high | normal | 0 | 0 | 0 | 2007 |
| CIPLA | 1 | low | high | positive | 0 | 0 | 0 | 121 |
| CIPLA | 1 | low | low | normal | 0 | 0 | 0 | 1710 |
| CIPLA | 1 | low | low | positive | 0 | 0 | 0 | 90 |
| CIPLA | 1 | low | mid | normal | 0 | 0 | 0 | 1945 |
| CIPLA | 1 | low | mid | positive | 0 | 0 | 0 | 116 |
| CIPLA | 1 | mid | high | normal | 0 | 0 | 0 | 1855 |
| CIPLA | 1 | mid | high | positive | 0 | 0 | 0 | 98 |
| CIPLA | 1 | mid | low | normal | 0 | 0 | 0 | 1653 |
| CIPLA | 1 | mid | low | positive | 0 | 0 | 0 | 86 |
| CIPLA | 1 | mid | mid | normal | 0 | 0 | 0 | 1702 |
| CIPLA | 1 | mid | mid | positive | 0 | 0 | 0 | 99 |
| CIPLA | 5 | high | high | normal | 0 | 0.345429 | 0 | 538 |
| CIPLA | 5 | high | high | positive | 0 | 0.344828 | 0 | 41 |
| CIPLA | 5 | high | low | normal | 0 | 0.344738 | 0 | 790 |
| CIPLA | 5 | high | low | positive | 0 | 0.343991 | 0 | 60 |
| CIPLA | 5 | high | mid | normal | 0 | 0.344637 | 0 | 735 |
| CIPLA | 5 | high | mid | positive | 0 | 0 | 0 | 40 |
| CIPLA | 5 | low | high | normal | 0 | 0 | 0 | 1038 |
| CIPLA | 5 | low | high | positive | 0 | 0 | 0 | 67 |
| CIPLA | 5 | low | low | normal | 0 | 0 | 0 | 910 |
| CIPLA | 5 | low | low | positive | 0 | 0.344578 | 0 | 46 |
| CIPLA | 5 | low | mid | normal | 0 | 0 | 0 | 997 |
| CIPLA | 5 | low | mid | positive | 0 | 0 | 0 | 72 |
| CIPLA | 5 | mid | high | normal | 0 | 0.345375 | 0 | 961 |
| CIPLA | 5 | mid | high | positive | 0 | 0.344804 | 0 | 51 |
| CIPLA | 5 | mid | low | normal | 0 | 0 | 0 | 843 |
| CIPLA | 5 | mid | low | positive | 0 | 0 | 0 | 47 |
| CIPLA | 5 | mid | mid | normal | 0 | 0 | 0 | 892 |
| CIPLA | 5 | mid | mid | positive | 0 | 0 | 0 | 41 |
| CIPLA | 15 | high | high | normal | 0 | 1.03345 | -0.697301 | 222 |
| CIPLA | 15 | high | high | positive | 0 | 0 | 0 | 1 |
| CIPLA | 15 | high | low | normal | 0 | 1.03427 | -0.693133 | 306 |
| CIPLA | 15 | high | low | positive | 0.345722 | 0.345722 | -0.691443 | 1 |
| CIPLA | 15 | high | mid | normal | 0 | 0.693626 | -0.690942 | 277 |
| CIPLA | 15 | high | mid | positive | 0.689631 | 0.689631 | 0 | 1 |
| CIPLA | 15 | low | high | normal | 0 | 0.695882 | 1.56718e-12 | 416 |
| CIPLA | 15 | low | high | positive | 0 | 0 | 0 | 1 |
| CIPLA | 15 | low | low | normal | 0 | 0.695713 | 1.57338e-12 | 360 |
| CIPLA | 15 | low | low | positive | -0.347029 | 1.38274 | 0 | 7 |
| CIPLA | 15 | low | mid | normal | 0 | 0.69197 | 0 | 385 |
| CIPLA | 15 | low | mid | positive | 1.89807 | 2.41588 | 0 | 4 |
| CIPLA | 15 | mid | high | normal | 0 | 0.698275 | 0 | 330 |
| CIPLA | 15 | mid | high | positive | -3.45011 | 3.45011 | 0.687545 | 2 |
| CIPLA | 15 | mid | low | normal | 0 | 0.692305 | 0 | 298 |
| CIPLA | 15 | mid | mid | normal | 0 | 0.693493 | 0 | 330 |
| CIPLA | 15 | mid | mid | positive | 0.518278 | 0.518278 | 1.03656 | 2 |
| CIPLA | 60 | high | high | normal | -0.345466 | 2.76192 | -1.38569 | 54 |
| CIPLA | 60 | high | low | normal | 0 | 2.08464 | -1.38971 | 77 |
| CIPLA | 60 | high | mid | normal | -0.344756 | 2.24861 | -1.38277 | 70 |
| CIPLA | 60 | low | high | normal | 0 | 2.42441 | 0.689655 | 110 |
| CIPLA | 60 | low | low | normal | 0 | 2.77229 | 7.8402e-13 | 84 |
| CIPLA | 60 | low | mid | normal | 0 | 2.08243 | 0.690323 | 102 |
| CIPLA | 60 | low | mid | positive | 4.16074 | 4.16074 | 1.57674e-12 | 1 |
| CIPLA | 60 | mid | high | normal | 0 | 2.41947 | -1.57118e-12 | 81 |
| CIPLA | 60 | mid | low | normal | 0 | 2.77542 | 0 | 84 |
| CIPLA | 60 | mid | mid | normal | 0 | 2.42685 | 0 | 77 |
| DRREDDY | 1 | high | high | normal | 0 | 0 | 0 | 1257 |
| DRREDDY | 1 | high | high | positive | 0 | 0 | 0 | 515 |
| DRREDDY | 1 | high | low | normal | 0 | 0.391957 | 0 | 1835 |
| DRREDDY | 1 | high | low | positive | 0 | 0 | 0 | 643 |
| DRREDDY | 1 | high | mid | normal | 0 | 0.372329 | 0 | 1673 |
| DRREDDY | 1 | high | mid | positive | 0 | 0 | 0 | 709 |
| DRREDDY | 1 | low | high | normal | 0 | 0 | 0 | 2963 |
| DRREDDY | 1 | low | high | positive | 0 | 0 | 0 | 793 |
| DRREDDY | 1 | low | low | normal | 0 | 0 | 0 | 2204 |
| DRREDDY | 1 | low | low | positive | 0 | 0 | 0 | 669 |
| DRREDDY | 1 | low | mid | normal | 0 | 0 | 0 | 2460 |
| DRREDDY | 1 | low | mid | positive | 0 | 0 | 0 | 720 |
| DRREDDY | 1 | mid | high | normal | 0 | 0 | 0 | 2078 |
| DRREDDY | 1 | mid | high | positive | 0 | 0 | 0 | 686 |
| DRREDDY | 1 | mid | low | normal | 0 | 0 | 0 | 2263 |
| DRREDDY | 1 | mid | low | positive | 0 | 0 | 0 | 680 |
| DRREDDY | 1 | mid | mid | normal | 0 | 0 | 0 | 2253 |
| DRREDDY | 1 | mid | mid | positive | 0 | 0 | 0 | 728 |
| DRREDDY | 5 | high | high | normal | 0 | 0.744491 | -0.785901 | 556 |
| DRREDDY | 5 | high | high | positive | 0 | 0.402625 | -0.390808 | 150 |
| DRREDDY | 5 | high | low | normal | 0 | 0.802037 | -0.800336 | 790 |
| DRREDDY | 5 | high | low | positive | 0 | 0.787526 | -0.801138 | 190 |
| DRREDDY | 5 | high | mid | normal | 0 | 0.80186 | -0.800576 | 779 |
| DRREDDY | 5 | high | mid | positive | 0 | 0.805315 | -0.786937 | 197 |
| DRREDDY | 5 | low | high | normal | 0 | 0.740001 | 0 | 1102 |
| DRREDDY | 5 | low | high | positive | 0 | 0.787123 | 0.783638 | 227 |
| DRREDDY | 5 | low | low | normal | 0 | 0.803503 | 1.82666e-12 | 801 |
| DRREDDY | 5 | low | low | positive | 0 | 0.788706 | 0.786102 | 189 |
| DRREDDY | 5 | low | mid | normal | 0 | 0.802166 | 0 | 860 |
| DRREDDY | 5 | low | mid | positive | 0 | 0.805477 | 0.785546 | 216 |
| DRREDDY | 5 | mid | high | normal | 0 | 0.403112 | 0 | 603 |
| DRREDDY | 5 | mid | high | positive | 0 | 0.402149 | 0 | 166 |
| DRREDDY | 5 | mid | low | normal | 0 | 0.736472 | 0 | 638 |
| DRREDDY | 5 | mid | low | positive | 0 | 0.783745 | 0 | 196 |
| DRREDDY | 5 | mid | mid | normal | 0 | 0.736025 | 0 | 647 |
| DRREDDY | 5 | mid | mid | positive | 0 | 0.782167 | 0 | 189 |
| DRREDDY | 15 | high | high | normal | 0 | 1.60481 | -1.48821 | 189 |
| DRREDDY | 15 | high | high | positive | 0 | 1.57909 | -1.56335 | 43 |
| DRREDDY | 15 | high | low | normal | 0 | 1.60154 | -1.48456 | 286 |
| DRREDDY | 15 | high | low | positive | 0.391374 | 1.17583 | -1.57159 | 57 |
| DRREDDY | 15 | high | mid | normal | 0 | 1.60739 | -1.56814 | 247 |
| DRREDDY | 15 | high | mid | positive | 0 | 1.57425 | -0.78796 | 65 |
| DRREDDY | 15 | low | high | normal | 1.83211e-12 | 1.48187 | 0.784375 | 421 |
| DRREDDY | 15 | low | high | positive | 0 | 1.57468 | 1.79147e-12 | 62 |
| DRREDDY | 15 | low | low | normal | 0 | 1.96607 | 0.805899 | 298 |
| DRREDDY | 15 | low | low | positive | 0.393205 | 1.95611 | 1.56544 | 53 |
| DRREDDY | 15 | low | mid | normal | 0 | 1.20875 | 0.787433 | 327 |
| DRREDDY | 15 | low | mid | positive | 0.984721 | 1.96862 | 0.789766 | 56 |
| DRREDDY | 15 | mid | high | normal | 0 | 1.57543 | -1.76185e-12 | 196 |
| DRREDDY | 15 | mid | high | positive | 0 | 1.57928 | 0 | 61 |
| DRREDDY | 15 | mid | low | normal | 0 | 1.85785 | 0 | 216 |
| DRREDDY | 15 | mid | low | positive | 0.392305 | 1.96384 | 0 | 62 |
| DRREDDY | 15 | mid | mid | normal | 0 | 1.54724 | 0 | 236 |
| DRREDDY | 15 | mid | mid | positive | 0.393236 | 1.9606 | 0 | 68 |
| DRREDDY | 60 | high | high | normal | 1.14177 | 4.38268 | -1.60888 | 54 |
| DRREDDY | 60 | high | high | positive | 0.98436 | 5.09468 | -1.57239 | 10 |
| DRREDDY | 60 | high | low | normal | 0.401171 | 2.81917 | -1.48843 | 75 |
| DRREDDY | 60 | high | low | positive | 0 | 1.57468 | -1.57066 | 7 |
| DRREDDY | 60 | high | mid | normal | 0 | 3.2095 | -1.60038 | 59 |
| DRREDDY | 60 | high | mid | positive | 0.393252 | 4.72395 | -2.35483 | 28 |
| DRREDDY | 60 | low | high | normal | 0 | 3.21854 | 0.802907 | 102 |
| DRREDDY | 60 | low | high | positive | 1.57487 | 2.76374 | 0.787464 | 19 |
| DRREDDY | 60 | low | low | normal | -1.17412 | 4.42104 | 0.805932 | 73 |
| DRREDDY | 60 | low | low | positive | 0.198083 | 6.67321 | 1.18025 | 18 |
| DRREDDY | 60 | low | mid | normal | 0.402641 | 3.71885 | 0.802085 | 75 |
| DRREDDY | 60 | low | mid | positive | -1.37801 | 4.34504 | 1.57022 | 14 |
| DRREDDY | 60 | mid | high | normal | 0.382075 | 4.17491 | 8.90335e-13 | 46 |
| DRREDDY | 60 | mid | high | positive | -1.77406 | 3.35383 | -0.391405 | 14 |
| DRREDDY | 60 | mid | low | normal | 0.401252 | 3.46899 | 0 | 56 |
| DRREDDY | 60 | mid | low | positive | 4.31973 | 6.46706 | 0.786999 | 16 |
| DRREDDY | 60 | mid | mid | normal | 1.20788 | 4.09836 | 0 | 57 |
| DRREDDY | 60 | mid | mid | positive | -1.17952 | 5.11751 | 0 | 17 |
| GOLDBEES | 1 | high | high | normal | 0 | 0 | 0 | 1287 |
| GOLDBEES | 1 | high | high | positive | 0 | 0 | 0 | 77 |
| GOLDBEES | 1 | high | low | normal | 0 | 0 | 0 | 1559 |
| GOLDBEES | 1 | high | low | positive | 0 | 0 | 0 | 102 |
| GOLDBEES | 1 | high | mid | normal | 0 | 0 | 0 | 1465 |
| GOLDBEES | 1 | high | mid | positive | 0 | 0 | 0 | 115 |
| GOLDBEES | 1 | low | high | normal | 0 | 0 | 0 | 3382 |
| GOLDBEES | 1 | low | high | positive | 0 | 0 | 0 | 236 |
| GOLDBEES | 1 | low | low | normal | 0 | 0 | 0 | 2964 |
| GOLDBEES | 1 | low | low | positive | 0 | 0 | 0 | 213 |
| GOLDBEES | 1 | low | mid | normal | 0 | 0 | 0 | 3200 |
| GOLDBEES | 1 | low | mid | positive | 0 | 0 | 0 | 244 |
| GOLDBEES | 1 | mid | high | normal | 0 | 0 | 0 | 1407 |
| GOLDBEES | 1 | mid | high | positive | 0 | 0 | 0 | 90 |
| GOLDBEES | 1 | mid | low | normal | 0 | 0 | 0 | 1515 |
| GOLDBEES | 1 | mid | low | positive | 0 | 0 | 0 | 126 |
| GOLDBEES | 1 | mid | mid | normal | 0 | 0 | 0 | 1549 |
| GOLDBEES | 1 | mid | mid | positive | 0 | 0 | 0 | 102 |
| GOLDBEES | 5 | high | high | normal | 0 | 0.421923 | 0 | 559 |
| GOLDBEES | 5 | high | high | positive | 0 | 0.422199 | -0.843633 | 32 |
| GOLDBEES | 5 | high | low | normal | 0 | 0.422315 | -1.19892e-12 | 644 |
| GOLDBEES | 5 | high | low | positive | 0 | 0.422386 | 0 | 43 |
| GOLDBEES | 5 | high | mid | normal | 0 | 0.421941 | 0 | 624 |
| GOLDBEES | 5 | high | mid | positive | 0 | 0 | 0 | 59 |
| GOLDBEES | 5 | low | high | normal | 0 | 0 | 0 | 1408 |
| GOLDBEES | 5 | low | high | positive | 0 | 0 | 0 | 120 |
| GOLDBEES | 5 | low | low | normal | 0 | 0 | 0 | 1272 |
| GOLDBEES | 5 | low | low | positive | 0 | 0 | 0 | 110 |
| GOLDBEES | 5 | low | mid | normal | 0 | 0 | 0 | 1373 |
| GOLDBEES | 5 | low | mid | positive | 0 | 0 | 0 | 104 |
| GOLDBEES | 5 | mid | high | normal | 0 | 0 | 0 | 600 |
| GOLDBEES | 5 | mid | high | positive | 0 | 0 | 0 | 41 |
| GOLDBEES | 5 | mid | low | normal | 0 | 0.421336 | 0 | 634 |
| GOLDBEES | 5 | mid | low | positive | 0 | 0.421692 | 0 | 57 |
| GOLDBEES | 5 | mid | mid | normal | 0 | 0.421727 | 0 | 620 |
| GOLDBEES | 5 | mid | mid | positive | 0 | 0 | 0 | 61 |
| GOLDBEES | 15 | high | high | normal | 0 | 0.844096 | -0.843668 | 225 |
| GOLDBEES | 15 | high | low | normal | 0 | 0.426949 | -0.844773 | 239 |
| GOLDBEES | 15 | high | mid | normal | 0 | 0.427515 | -0.844666 | 234 |
| GOLDBEES | 15 | low | high | normal | 0 | 0.842495 | 0 | 532 |
| GOLDBEES | 15 | low | high | positive | -10000 | 10000 | -0.844773 | 1 |
| GOLDBEES | 15 | low | low | normal | 0 | 0.843419 | 0 | 489 |
| GOLDBEES | 15 | low | mid | normal | 0 | 0.422922 | 0 | 514 |
| GOLDBEES | 15 | mid | high | normal | 0 | 0.422851 | 0 | 214 |
| GOLDBEES | 15 | mid | low | normal | 0 | 0.426913 | 0 | 245 |
| GOLDBEES | 15 | mid | mid | normal | 0 | 0.42303 | 0 | 250 |
| GOLDBEES | 60 | high | high | normal | 0.425864 | 1.26783 | -0.84606 | 56 |
| GOLDBEES | 60 | high | low | normal | 0.421941 | 1.27516 | -0.844934 | 60 |
| GOLDBEES | 60 | high | mid | normal | -0.421834 | 1.68663 | -0.844844 | 71 |
| GOLDBEES | 60 | low | high | normal | -0.421621 | 1.6867 | 0 | 138 |
| GOLDBEES | 60 | low | high | positive | -10000 | 10000 | -0.844773 | 1 |
| GOLDBEES | 60 | low | low | normal | 0 | 1.48371 | 1.19968e-12 | 112 |
| GOLDBEES | 60 | low | mid | normal | 0 | 1.28178 | 1.21362e-12 | 129 |
| GOLDBEES | 60 | mid | high | normal | -0.422083 | 1.26657 | 0 | 49 |
| GOLDBEES | 60 | mid | low | normal | 0.422833 | 1.70114 | 0 | 72 |
| GOLDBEES | 60 | mid | mid | normal | -0.42187 | 1.69047 | -0.843597 | 51 |
| HCLTECH | 1 | high | high | normal | 0 | 0 | 0 | 1301 |
| HCLTECH | 1 | high | high | positive | 0 | 0 | 0 | 176 |
| HCLTECH | 1 | high | low | normal | 0 | 0 | 0 | 2151 |
| HCLTECH | 1 | high | low | positive | 0 | 0 | 0 | 264 |
| HCLTECH | 1 | high | mid | normal | 0 | 0 | 0 | 2047 |
| HCLTECH | 1 | high | mid | positive | 0 | 0 | 0 | 248 |
| HCLTECH | 1 | low | high | normal | 0 | 0 | 0 | 3248 |
| HCLTECH | 1 | low | high | positive | 0 | 0 | 0 | 487 |
| HCLTECH | 1 | low | low | normal | 0 | 0 | 0 | 2447 |
| HCLTECH | 1 | low | low | positive | 0 | 0 | 0 | 342 |
| HCLTECH | 1 | low | mid | normal | 0 | 0 | 0 | 2672 |
| HCLTECH | 1 | low | mid | positive | 0 | 0 | 0 | 382 |
| HCLTECH | 1 | mid | high | normal | 0 | 0 | 0 | 1896 |
| HCLTECH | 1 | mid | high | positive | 0 | 0 | 0 | 318 |
| HCLTECH | 1 | mid | low | normal | 0 | 0 | 0 | 1883 |
| HCLTECH | 1 | mid | low | positive | 0 | 0 | 0 | 339 |
| HCLTECH | 1 | mid | mid | normal | 0 | 0 | 0 | 1959 |
| HCLTECH | 1 | mid | mid | positive | 0 | 0 | 0 | 340 |
| HCLTECH | 5 | high | high | normal | 0 | 0.431872 | 0 | 419 |
| HCLTECH | 5 | high | high | positive | 0 | 0.431872 | -0.852297 | 111 |
| HCLTECH | 5 | high | low | normal | 0 | 0.436129 | -0.421319 | 716 |
| HCLTECH | 5 | high | low | positive | 0 | 0.434179 | -1.94386e-12 | 173 |
| HCLTECH | 5 | high | mid | normal | 0 | 0.43262 | 0 | 681 |
| HCLTECH | 5 | high | mid | positive | 0 | 0.432769 | -0.854226 | 175 |
| HCLTECH | 5 | low | high | normal | 0 | 0.429682 | 0 | 1081 |
| HCLTECH | 5 | low | high | positive | 0 | 0.430923 | 0 | 291 |
| HCLTECH | 5 | low | low | normal | 0 | 0.430459 | 0 | 761 |
| HCLTECH | 5 | low | low | positive | 0 | 0.431444 | 0 | 235 |
| HCLTECH | 5 | low | mid | normal | 0 | 0.430052 | 0 | 841 |
| HCLTECH | 5 | low | mid | positive | 0 | 0.430812 | 0 | 240 |
| HCLTECH | 5 | mid | high | normal | 0 | 0.431854 | 0 | 707 |
| HCLTECH | 5 | mid | high | positive | 0 | 0.431053 | 0 | 180 |
| HCLTECH | 5 | mid | low | normal | 0 | 0.430422 | 0 | 713 |
| HCLTECH | 5 | mid | low | positive | 0 | 0.430793 | 0 | 191 |
| HCLTECH | 5 | mid | mid | normal | 0 | 0.431835 | 0 | 777 |
| HCLTECH | 5 | mid | mid | positive | 0 | 0.432451 | 0 | 159 |
| HCLTECH | 15 | high | high | normal | -0.429563 | 1.30427 | -0.865183 | 174 |
| HCLTECH | 15 | high | high | positive | 0 | 1.29938 | -0.863894 | 21 |
| HCLTECH | 15 | high | low | normal | 0 | 1.29182 | -0.865632 | 270 |
| HCLTECH | 15 | high | low | positive | 0 | 1.2898 | -0.863801 | 28 |
| HCLTECH | 15 | high | mid | normal | 0 | 0.864528 | -0.864192 | 275 |
| HCLTECH | 15 | high | mid | positive | -0.864342 | 2.99529 | -0.867943 | 27 |
| HCLTECH | 15 | low | high | normal | 0 | 0.867717 | 1.97897e-12 | 414 |
| HCLTECH | 15 | low | high | positive | 0 | 1.50834 | 0.856571 | 38 |
| HCLTECH | 15 | low | low | normal | 0 | 0.872677 | 0.858406 | 324 |
| HCLTECH | 15 | low | low | positive | -0.432264 | 1.72518 | 1.97845e-12 | 29 |
| HCLTECH | 15 | low | mid | normal | 0 | 0.8726 | 0.859882 | 328 |
| HCLTECH | 15 | low | mid | positive | 0 | 1.72901 | 9.76733e-13 | 40 |
| HCLTECH | 15 | mid | high | normal | 0 | 1.29394 | 0 | 305 |
| HCLTECH | 15 | mid | high | positive | -0.651545 | 1.29066 | -0.863579 | 20 |
| HCLTECH | 15 | mid | low | normal | 0 | 1.29994 | 0 | 291 |
| HCLTECH | 15 | mid | low | positive | 0.645134 | 1.08194 | -0.430311 | 30 |
| HCLTECH | 15 | mid | mid | normal | 0 | 0.866515 | 0 | 302 |
| HCLTECH | 15 | mid | mid | positive | 0 | 1.28134 | 0 | 27 |
| HCLTECH | 60 | high | high | normal | -1.07522 | 4.10095 | -0.863148 | 54 |
| HCLTECH | 60 | high | high | positive | 13.5453 | 13.5453 | -1.30361 | 2 |
| HCLTECH | 60 | high | low | normal | 0.429443 | 3.4416 | -0.860141 | 79 |
| HCLTECH | 60 | high | low | positive | 2.58153 | 2.58153 | -0.86479 | 3 |
| HCLTECH | 60 | high | mid | normal | -0.867341 | 4.04344 | -1.71468 | 62 |
| HCLTECH | 60 | high | mid | positive | -4.53269 | 7.12987 | -0.431947 | 2 |
| HCLTECH | 60 | low | high | normal | 0.429277 | 2.15843 | 0.862199 | 110 |
| HCLTECH | 60 | low | high | positive | 2.59864 | 2.59864 | 1.73243 | 1 |
| HCLTECH | 60 | low | low | normal | -0.859882 | 2.5861 | 0.859808 | 73 |
| HCLTECH | 60 | low | low | positive | 2.16581 | 2.61063 | 0 | 7 |
| HCLTECH | 60 | low | mid | normal | -0.858922 | 3.45587 | 0.860289 | 91 |
| HCLTECH | 60 | low | mid | positive | 0.223536 | 3.91924 | -9.89312e-13 | 4 |
| HCLTECH | 60 | mid | high | normal | -0.647169 | 2.37256 | 0 | 76 |
| HCLTECH | 60 | mid | high | positive | 5.16981 | 5.16981 | 0.855103 | 2 |
| HCLTECH | 60 | mid | low | normal | -0.430533 | 3.4665 | 0 | 79 |
| HCLTECH | 60 | mid | low | positive | 5.40229 | 13.221 | -0.861681 | 4 |
| HCLTECH | 60 | mid | mid | normal | -0.863334 | 3.43598 | 0 | 87 |
| HCLTECH | 60 | mid | mid | positive | -1.73183 | 1.94805 | -0.863727 | 4 |
| HDFCBANK | 1 | high | high | normal | 0 | 0.302939 | 0 | 2462 |
| HDFCBANK | 1 | high | high | positive | 0 | 0 | 0 | 190 |
| HDFCBANK | 1 | high | low | normal | 0 | 0.303177 | 0 | 3090 |
| HDFCBANK | 1 | high | low | positive | 0 | 0.151231 | 0 | 234 |
| HDFCBANK | 1 | high | mid | normal | 0 | 0.303141 | 0 | 3165 |
| HDFCBANK | 1 | high | mid | positive | 0 | 0 | 0 | 214 |
| HDFCBANK | 1 | low | high | normal | 0 | 0 | 0 | 4353 |
| HDFCBANK | 1 | low | high | positive | 0 | 0 | 0 | 382 |
| HDFCBANK | 1 | low | low | normal | 0 | 0 | 0 | 3689 |
| HDFCBANK | 1 | low | low | positive | 0 | 0 | 0 | 259 |
| HDFCBANK | 1 | low | mid | normal | 0 | 0 | 0 | 4027 |
| HDFCBANK | 1 | low | mid | positive | 0 | 0 | 0 | 289 |
| HDFCBANK | 1 | mid | high | normal | 0 | 0 | 0 | 2754 |
| HDFCBANK | 1 | mid | high | positive | 0 | 0 | 0 | 179 |
| HDFCBANK | 1 | mid | low | normal | 0 | 0 | 0 | 2867 |
| HDFCBANK | 1 | mid | low | positive | 0 | 0 | 0 | 182 |
| HDFCBANK | 1 | mid | mid | normal | 0 | 0 | 0 | 2750 |
| HDFCBANK | 1 | mid | mid | positive | 0 | 0 | 0 | 192 |
| HDFCBANK | 5 | high | high | normal | 0 | 0.606134 | -0.606061 | 690 |
| HDFCBANK | 5 | high | high | positive | 0 | 0.607137 | -0.605694 | 86 |
| HDFCBANK | 5 | high | low | normal | 0 | 0.607211 | -0.606907 | 848 |
| HDFCBANK | 5 | high | low | positive | 0 | 0.304813 | -0.606833 | 97 |
| HDFCBANK | 5 | high | mid | normal | 0 | 0.608328 | -0.607091 | 827 |
| HDFCBANK | 5 | high | mid | positive | 0.302179 | 0.606189 | -0.60573 | 115 |
| HDFCBANK | 5 | low | high | normal | 0 | 0.303113 | 0 | 1285 |
| HDFCBANK | 5 | low | high | positive | 0 | 0.303934 | 0 | 158 |
| HDFCBANK | 5 | low | low | normal | 0 | 0.30337 | 0 | 1062 |
| HDFCBANK | 5 | low | low | positive | 0 | 0.608328 | 0 | 117 |
| HDFCBANK | 5 | low | mid | normal | 0 | 0.303472 | 0 | 1194 |
| HDFCBANK | 5 | low | mid | positive | 0 | 0.304516 | 0 | 134 |
| HDFCBANK | 5 | mid | high | normal | 0 | 0.308176 | 0 | 578 |
| HDFCBANK | 5 | mid | high | positive | 0 | 0.305064 | 0 | 91 |
| HDFCBANK | 5 | mid | low | normal | 0 | 0.304192 | 0 | 662 |
| HDFCBANK | 5 | mid | low | positive | 0 | 0.304953 | 0 | 102 |
| HDFCBANK | 5 | mid | mid | normal | 0 | 0.304618 | 0 | 620 |
| HDFCBANK | 5 | mid | mid | positive | 0 | 0.455544 | 0 | 84 |
| HDFCBANK | 15 | high | high | normal | 0 | 1.5193 | -0.60781 | 259 |
| HDFCBANK | 15 | high | high | positive | -10000 | 10000 | -3.0326 | 1 |
| HDFCBANK | 15 | high | low | normal | 0.303122 | 1.23276 | -0.610305 | 300 |
| HDFCBANK | 15 | high | mid | normal | 0.302599 | 1.21407 | -0.607275 | 321 |
| HDFCBANK | 15 | low | high | normal | 0 | 0.907551 | 0 | 468 |
| HDFCBANK | 15 | low | low | normal | 0 | 1.20747 | 1.37627e-12 | 418 |
| HDFCBANK | 15 | low | mid | normal | 0 | 0.91352 | 0 | 442 |
| HDFCBANK | 15 | mid | high | normal | 0 | 0.91788 | 0 | 244 |
| HDFCBANK | 15 | mid | low | normal | 0 | 0.609812 | 0 | 254 |
| HDFCBANK | 15 | mid | mid | normal | 0 | 0.907634 | 0 | 236 |
| HDFCBANK | 60 | high | high | normal | -0.303426 | 2.43365 | -1.21104 | 60 |
| HDFCBANK | 60 | high | high | positive | -10000 | 10000 | -3.0326 | 1 |
| HDFCBANK | 60 | high | low | normal | 0 | 2.46662 | -1.21109 | 79 |
| HDFCBANK | 60 | high | mid | normal | 1.06379 | 2.12579 | -0.607239 | 88 |
| HDFCBANK | 60 | low | high | normal | -0.605309 | 2.11666 | 1.37158e-12 | 123 |
| HDFCBANK | 60 | low | low | normal | 0 | 2.43799 | 1.37936e-12 | 104 |
| HDFCBANK | 60 | low | mid | normal | 0 | 2.11615 | 1.38141e-12 | 109 |
| HDFCBANK | 60 | mid | high | normal | -0.605749 | 2.12986 | -1.37565e-12 | 61 |
| HDFCBANK | 60 | mid | low | normal | 0.605235 | 1.82816 | 0 | 62 |
| HDFCBANK | 60 | mid | mid | normal | -0.606006 | 1.82726 | 0 | 53 |
| HINDUNILVR | 1 | high | high | normal | 0 | 0 | 0 | 1603 |
| HINDUNILVR | 1 | high | high | positive | 0 | 0.231849 | 0 | 98 |
| HINDUNILVR | 1 | high | low | normal | 0 | 0 | 0 | 2061 |
| HINDUNILVR | 1 | high | low | positive | 0 | 0 | 0 | 152 |
| HINDUNILVR | 1 | high | mid | normal | 0 | 0 | 0 | 2029 |
| HINDUNILVR | 1 | high | mid | positive | 0 | 0.231059 | 0 | 130 |
| HINDUNILVR | 1 | low | high | normal | 0 | 0 | 0 | 2475 |
| HINDUNILVR | 1 | low | high | positive | 0 | 0 | 0 | 184 |
| HINDUNILVR | 1 | low | low | normal | 0 | 0 | 0 | 2160 |
| HINDUNILVR | 1 | low | low | positive | 0 | 0 | 0 | 149 |
| HINDUNILVR | 1 | low | mid | normal | 0 | 0 | 0 | 2278 |
| HINDUNILVR | 1 | low | mid | positive | 0 | 0 | 0 | 157 |
| HINDUNILVR | 1 | mid | high | normal | 0 | 0 | 0 | 1822 |
| HINDUNILVR | 1 | mid | high | positive | 0 | 0 | 0 | 113 |
| HINDUNILVR | 1 | mid | low | normal | 0 | 0 | 0 | 1660 |
| HINDUNILVR | 1 | mid | low | positive | 0 | 0 | 0 | 113 |
| HINDUNILVR | 1 | mid | mid | normal | 0 | 0 | 0 | 1797 |
| HINDUNILVR | 1 | mid | mid | positive | 0 | 0 | 0 | 96 |
| HINDUNILVR | 5 | high | high | normal | 0 | 0.464253 | -2.12206e-12 | 707 |
| HINDUNILVR | 5 | high | high | positive | 0 | 0.694605 | -0.464317 | 73 |
| HINDUNILVR | 5 | high | low | normal | 0 | 0.463951 | -2.11015e-12 | 865 |
| HINDUNILVR | 5 | high | low | positive | 0 | 0.695749 | -0.46307 | 65 |
| HINDUNILVR | 5 | high | mid | normal | 0 | 0.463478 | -0.46031 | 876 |
| HINDUNILVR | 5 | high | mid | positive | 0 | 0.69385 | -0.9273 | 73 |
| HINDUNILVR | 5 | low | high | normal | 0 | 0.230234 | 0 | 1039 |
| HINDUNILVR | 5 | low | high | positive | 0 | 0.465772 | 0 | 108 |
| HINDUNILVR | 5 | low | low | normal | 0 | 0.231176 | 0 | 936 |
| HINDUNILVR | 5 | low | low | positive | 0 | 0.692937 | 0 | 81 |
| HINDUNILVR | 5 | low | mid | normal | 0 | 0.231235 | 0 | 1015 |
| HINDUNILVR | 5 | low | mid | positive | 0 | 0.466168 | 0 | 77 |
| HINDUNILVR | 5 | mid | high | normal | 0 | 0.460469 | 0 | 733 |
| HINDUNILVR | 5 | mid | high | positive | 0 | 0.463951 | 0 | 74 |
| HINDUNILVR | 5 | mid | low | normal | 0 | 0.232823 | 0 | 728 |
| HINDUNILVR | 5 | mid | low | positive | 0 | 0.463887 | 0 | 60 |
| HINDUNILVR | 5 | mid | mid | normal | 0 | 0.462829 | 0 | 720 |
| HINDUNILVR | 5 | mid | mid | positive | 0.231246 | 0.695225 | 0 | 56 |
| HINDUNILVR | 15 | high | high | normal | 0 | 1.16475 | -0.923585 | 272 |
| HINDUNILVR | 15 | high | high | positive | 0.23204 | 0.23204 | -1.85688 | 7 |
| HINDUNILVR | 15 | high | low | normal | -0.230553 | 1.16214 | -0.925241 | 321 |
| HINDUNILVR | 15 | high | low | positive | -1.15958 | 1.39027 | -0.926848 | 7 |
| HINDUNILVR | 15 | high | mid | normal | 0 | 1.16632 | -0.465214 | 335 |
| HINDUNILVR | 15 | high | mid | positive | 0 | 1.85185 | 0 | 7 |
| HINDUNILVR | 15 | low | high | normal | 0 | 0.921022 | 2.11123e-12 | 395 |
| HINDUNILVR | 15 | low | high | positive | 0 | 2.10011 | 0.463843 | 9 |
| HINDUNILVR | 15 | low | low | normal | 0 | 0.930427 | 0.460649 | 373 |
| HINDUNILVR | 15 | low | low | positive | 2.09873 | 2.09873 | 1.39916 | 1 |
| HINDUNILVR | 15 | low | mid | normal | 0 | 0.928053 | 0.463897 | 373 |
| HINDUNILVR | 15 | low | mid | positive | 0.232748 | 1.63195 | 0.697229 | 8 |
| HINDUNILVR | 15 | mid | high | normal | 0 | 1.16131 | 0 | 287 |
| HINDUNILVR | 15 | mid | high | positive | 0.23175 | 0.695314 | -6.4463e-05 | 2 |
| HINDUNILVR | 15 | mid | low | normal | 0 | 1.15487 | 0 | 266 |
| HINDUNILVR | 15 | mid | low | positive | 0.813068 | 0.813068 | -0.235541 | 4 |
| HINDUNILVR | 15 | mid | mid | normal | 0 | 0.927967 | 0 | 269 |
| HINDUNILVR | 15 | mid | mid | positive | 0 | 1.85982 | -0.466461 | 7 |
| HINDUNILVR | 60 | high | high | normal | 0.468362 | 2.09312 | -0.923489 | 69 |
| HINDUNILVR | 60 | high | low | normal | -0.231487 | 3.00201 | -0.928441 | 76 |
| HINDUNILVR | 60 | high | mid | normal | 0 | 2.78125 | -0.930406 | 77 |
| HINDUNILVR | 60 | high | mid | positive | 2.78093 | 2.78093 | 0 | 1 |
| HINDUNILVR | 60 | low | high | normal | 0 | 1.1614 | 0.467008 | 98 |
| HINDUNILVR | 60 | low | high | positive | -5.59265 | 5.59265 | 1.39153 | 2 |
| HINDUNILVR | 60 | low | low | normal | 0 | 3.51626 | 0.467257 | 75 |
| HINDUNILVR | 60 | low | mid | normal | 0 | 1.62349 | 0.464285 | 79 |
| HINDUNILVR | 60 | mid | high | normal | -0.578445 | 3.00629 | 0 | 76 |
| HINDUNILVR | 60 | mid | low | normal | 0.46456 | 3.01215 | -0.229853 | 94 |
| HINDUNILVR | 60 | mid | mid | normal | 0 | 3.74243 | 0 | 93 |
| ICICIBANK | 1 | high | high | normal | 0 | 0.356697 | 0 | 1979 |
| ICICIBANK | 1 | high | high | positive | 0 | 0.355745 | 0 | 116 |
| ICICIBANK | 1 | high | low | normal | 0 | 0.356608 | 0 | 2563 |
| ICICIBANK | 1 | high | low | positive | 0 | 0.17779 | 0 | 164 |
| ICICIBANK | 1 | high | mid | normal | 0 | 0.356494 | 0 | 2732 |
| ICICIBANK | 1 | high | mid | positive | 0 | 0.356964 | 0 | 155 |
| ICICIBANK | 1 | low | high | normal | 0 | 0 | 0 | 3768 |
| ICICIBANK | 1 | low | high | positive | 0 | 0 | 0 | 200 |
| ICICIBANK | 1 | low | low | normal | 0 | 0 | 0 | 3333 |
| ICICIBANK | 1 | low | low | positive | 0 | 0 | 0 | 206 |
| ICICIBANK | 1 | low | mid | normal | 0 | 0 | 0 | 3323 |
| ICICIBANK | 1 | low | mid | positive | 0 | 0 | 0 | 227 |
| ICICIBANK | 1 | mid | high | normal | 0 | 0 | 0 | 2585 |
| ICICIBANK | 1 | mid | high | positive | 0 | 0 | 0 | 128 |
| ICICIBANK | 1 | mid | low | normal | 0 | 0 | 0 | 2391 |
| ICICIBANK | 1 | mid | low | positive | 0 | 0 | 0 | 123 |
| ICICIBANK | 1 | mid | mid | normal | 0 | 0 | 0 | 2490 |
| ICICIBANK | 1 | mid | mid | positive | 0 | 0 | 0 | 115 |
| ICICIBANK | 5 | high | high | normal | 0 | 0.362102 | -0.713051 | 620 |
| ICICIBANK | 5 | high | high | positive | 0 | 0.712784 | -0.713738 | 60 |
| ICICIBANK | 5 | high | low | normal | 0 | 0.362568 | -0.713241 | 787 |
| ICICIBANK | 5 | high | low | positive | 0 | 0.713343 | -0.721124 | 82 |
| ICICIBANK | 5 | high | mid | normal | 0 | 0.712289 | -0.713165 | 862 |
| ICICIBANK | 5 | high | mid | positive | -8.11064e-13 | 1.07731 | -0.719645 | 78 |
| ICICIBANK | 5 | low | high | normal | 0 | 0.356468 | 0 | 1233 |
| ICICIBANK | 5 | low | high | positive | 0 | 0.721917 | 0 | 92 |
| ICICIBANK | 5 | low | low | normal | 0 | 0 | 0 | 1052 |
| ICICIBANK | 5 | low | low | positive | 0 | 0.721839 | 0 | 94 |
| ICICIBANK | 5 | low | mid | normal | 0 | 0.356595 | 0 | 1056 |
| ICICIBANK | 5 | low | mid | positive | 0 | 0.714209 | 0 | 103 |
| ICICIBANK | 5 | mid | high | normal | 0 | 0.71347 | 0 | 770 |
| ICICIBANK | 5 | mid | high | positive | 0 | 0.722883 | 0 | 67 |
| ICICIBANK | 5 | mid | low | normal | 0 | 0.362188 | 0 | 769 |
| ICICIBANK | 5 | mid | low | positive | 0 | 0.722987 | -1.64009e-12 | 58 |
| ICICIBANK | 5 | mid | mid | normal | 0 | 0.361376 | 0 | 768 |
| ICICIBANK | 5 | mid | mid | positive | 0 | 0.721683 | 0 | 61 |
| ICICIBANK | 15 | high | high | normal | 1.61912e-12 | 1.42526 | -0.72223 | 191 |
| ICICIBANK | 15 | high | low | normal | 0 | 1.42531 | -0.722217 | 254 |
| ICICIBANK | 15 | high | mid | normal | -0.356214 | 1.4443 | -0.722857 | 249 |
| ICICIBANK | 15 | low | high | normal | 0 | 1.42313 | 1.62114e-12 | 433 |
| ICICIBANK | 15 | low | low | normal | 0 | 1.07158 | 8.08325e-13 | 360 |
| ICICIBANK | 15 | low | mid | normal | 0 | 1.08511 | 1.63808e-12 | 396 |
| ICICIBANK | 15 | mid | high | normal | 0 | 1.08637 | 0 | 348 |
| ICICIBANK | 15 | mid | low | normal | 0 | 1.42554 | 0 | 358 |
| ICICIBANK | 15 | mid | mid | normal | 0 | 1.0846 | 0 | 354 |
| ICICIBANK | 60 | high | high | normal | -0.355973 | 2.89593 | -0.725268 | 39 |
| ICICIBANK | 60 | high | low | normal | 0.71314 | 2.88205 | -1.42842 | 69 |
| ICICIBANK | 60 | high | mid | normal | -0.356519 | 2.85347 | -1.42827 | 51 |
| ICICIBANK | 60 | low | high | normal | 0 | 2.16677 | 1.62172e-12 | 105 |
| ICICIBANK | 60 | low | low | normal | 0 | 2.68551 | 1.62805e-12 | 90 |
| ICICIBANK | 60 | low | mid | normal | 0 | 2.85063 | 1.62236e-12 | 104 |
| ICICIBANK | 60 | mid | high | normal | 0.362188 | 2.52826 | 0 | 101 |
| ICICIBANK | 60 | mid | low | normal | 0 | 2.16959 | 0 | 86 |
| ICICIBANK | 60 | mid | mid | normal | -0.36105 | 2.84535 | 0 | 95 |
| INFY | 1 | high | high | normal | 0 | 0.465224 | 0 | 1933 |
| INFY | 1 | high | high | positive | 0 | 0 | 0 | 135 |
| INFY | 1 | high | low | normal | 0 | 0 | 0 | 3146 |
| INFY | 1 | high | low | positive | 0 | 0.229927 | 0 | 220 |
| INFY | 1 | high | mid | normal | 0 | 0.461171 | 0 | 2766 |
| INFY | 1 | high | mid | positive | 0 | 0 | 0 | 201 |
| INFY | 1 | low | high | normal | 0 | 0 | 0 | 4216 |
| INFY | 1 | low | high | positive | 0 | 0 | 0 | 312 |
| INFY | 1 | low | low | normal | 0 | 0 | 0 | 3397 |
| INFY | 1 | low | low | positive | 0 | 0 | 0 | 201 |
| INFY | 1 | low | mid | normal | 0 | 0 | 0 | 3683 |
| INFY | 1 | low | mid | positive | 0 | 0 | 0 | 235 |
| INFY | 1 | mid | high | normal | 0 | 0 | 0 | 2446 |
| INFY | 1 | mid | high | positive | 0 | 0.466092 | 0 | 174 |
| INFY | 1 | mid | low | normal | 0 | 0 | 0 | 2101 |
| INFY | 1 | mid | low | positive | 0 | 0 | 0 | 152 |
| INFY | 1 | mid | mid | normal | 0 | 0 | 0 | 2436 |
| INFY | 1 | mid | mid | positive | 0 | 0 | 0 | 174 |
| INFY | 5 | high | high | normal | 0 | 0.930709 | -0.93314 | 595 |
| INFY | 5 | high | high | positive | 0 | 0.932271 | -0.934798 | 72 |
| INFY | 5 | high | low | normal | 0 | 0.474676 | -0.934732 | 912 |
| INFY | 5 | high | low | positive | 0 | 0.467814 | -0.934056 | 135 |
| INFY | 5 | high | mid | normal | 0 | 0.931836 | -0.934951 | 830 |
| INFY | 5 | high | mid | positive | 0 | 0.932184 | -0.934274 | 95 |
| INFY | 5 | low | high | normal | 0 | 0.930449 | 0 | 1235 |
| INFY | 5 | low | high | positive | 0 | 0.933663 | 0 | 163 |
| INFY | 5 | low | low | normal | 0 | 0.931229 | 0 | 997 |
| INFY | 5 | low | low | positive | 0 | 0.941056 | 2.13036e-12 | 108 |
| INFY | 5 | low | mid | normal | 0 | 0.474181 | 0 | 1111 |
| INFY | 5 | low | mid | positive | 0 | 0.933315 | 0 | 120 |
| INFY | 5 | mid | high | normal | 0 | 0.474541 | 0 | 706 |
| INFY | 5 | mid | high | positive | 0 | 0.472925 | 0 | 92 |
| INFY | 5 | mid | low | normal | 0 | 0.474338 | 0 | 631 |
| INFY | 5 | mid | low | positive | 0 | 0.470418 | 0 | 80 |
| INFY | 5 | mid | mid | normal | 0 | 0.474992 | 0 | 690 |
| INFY | 5 | mid | mid | positive | 0 | 0.944644 | 0 | 102 |
| INFY | 15 | high | high | normal | 0 | 1.8685 | -1.86402 | 188 |
| INFY | 15 | high | high | positive | -0.472791 | 0.472791 | 0.945582 | 1 |
| INFY | 15 | high | low | normal | 0 | 1.42308 | -1.86441 | 304 |
| INFY | 15 | high | low | positive | 5.5991 | 5.5991 | -1.86637 | 1 |
| INFY | 15 | high | mid | normal | 0 | 1.86572 | -0.945828 | 250 |
| INFY | 15 | low | high | normal | 0 | 1.40384 | 0.930103 | 438 |
| INFY | 15 | low | high | positive | -2.83059 | 2.83059 | -2.14534e-12 | 1 |
| INFY | 15 | low | low | normal | 0 | 1.42254 | 0.930709 | 355 |
| INFY | 15 | low | mid | normal | 0 | 1.42308 | 2.15919e-12 | 423 |
| INFY | 15 | mid | high | normal | 0 | 1.4163 | 0 | 343 |
| INFY | 15 | mid | low | normal | 1.06304e-12 | 1.40574 | 0 | 312 |
| INFY | 15 | mid | mid | normal | 0 | 1.64398 | 0 | 326 |
| INFY | 60 | high | high | normal | -0.468274 | 3.72978 | -1.86437 | 57 |
| INFY | 60 | high | low | normal | 0.700271 | 3.76622 | -1.86829 | 96 |
| INFY | 60 | high | mid | normal | 0.233013 | 3.49474 | -1.86641 | 68 |
| INFY | 60 | low | high | normal | -0.934187 | 3.32305 | 0.934361 | 107 |
| INFY | 60 | low | low | normal | 0.93375 | 3.3111 | 0.932184 | 89 |
| INFY | 60 | low | mid | normal | 0.233612 | 3.26112 | 0.933097 | 114 |
| INFY | 60 | mid | high | normal | 2.12211e-12 | 3.51902 | 0 | 80 |
| INFY | 60 | mid | low | normal | 0.468296 | 4.20129 | 0 | 59 |
| INFY | 60 | mid | mid | normal | 0.466157 | 3.81607 | 0 | 69 |
| ITBEES | 1 | high | high | normal | 0 | 0 | 0 | 44 |
| ITBEES | 1 | high | high | positive | 0 | 1.63079 | -1.16482e-12 | 13 |
| ITBEES | 1 | high | low | normal | 0 | 0 | 0 | 36 |
| ITBEES | 1 | high | low | positive | 0 | 0 | 0 | 8 |
| ITBEES | 1 | high | mid | normal | 0 | 0 | 0 | 49 |
| ITBEES | 1 | high | mid | positive | 0 | 0 | 0 | 6 |
| ITBEES | 1 | low | high | normal | 0 | 0 | 0 | 292 |
| ITBEES | 1 | low | high | positive | 0 | 0 | 0 | 64 |
| ITBEES | 1 | low | low | normal | 0 | 0 | 0 | 436 |
| ITBEES | 1 | low | low | positive | 0 | 0 | 0 | 87 |
| ITBEES | 1 | low | mid | normal | 0 | 0 | 0 | 348 |
| ITBEES | 1 | low | mid | positive | 0 | 0 | 0 | 78 |
| ITBEES | 1 | mid | high | normal | 0 | 0 | 0 | 3309 |
| ITBEES | 1 | mid | high | positive | 0 | 0 | 0 | 584 |
| ITBEES | 1 | mid | low | normal | 0 | 0 | 0 | 3211 |
| ITBEES | 1 | mid | low | positive | 0 | 0 | 0 | 528 |
| ITBEES | 1 | mid | mid | normal | 0 | 0 | 0 | 3370 |
| ITBEES | 1 | mid | mid | positive | 0 | 0 | 0 | 586 |
| ITBEES | 5 | high | high | normal | 0 | 0 | 0 | 30 |
| ITBEES | 5 | high | high | positive | -1.63079 | 1.63079 | -3.26158 | 10 |
| ITBEES | 5 | high | low | normal | 0 | 0 | 0 | 26 |
| ITBEES | 5 | high | low | positive | 0 | 0 | 0 | 5 |
| ITBEES | 5 | high | mid | normal | 0 | 0 | 0 | 34 |
| ITBEES | 5 | high | mid | positive | 1.63079 | 1.63079 | -3.26158 | 3 |
| ITBEES | 5 | low | high | normal | 0 | 0 | 0 | 380 |
| ITBEES | 5 | low | high | positive | 0 | 0 | 0 | 99 |
| ITBEES | 5 | low | low | normal | 0 | 0 | 0 | 446 |
| ITBEES | 5 | low | low | positive | 0 | 0 | 0 | 92 |
| ITBEES | 5 | low | mid | normal | 0 | 0 | 0 | 425 |
| ITBEES | 5 | low | mid | positive | 0 | 0 | 0 | 85 |
| ITBEES | 5 | mid | high | normal | 0 | 0 | 0 | 1837 |
| ITBEES | 5 | mid | high | positive | 0 | 0 | 0 | 285 |
| ITBEES | 5 | mid | low | normal | 0 | 0 | 0 | 1804 |
| ITBEES | 5 | mid | low | positive | 0 | 0 | 0 | 269 |
| ITBEES | 5 | mid | mid | normal | 0 | 0 | 0 | 1892 |
| ITBEES | 5 | mid | mid | positive | 0 | 0 | 0 | 279 |
| ITBEES | 15 | high | high | normal | -0.815395 | 1.63079 | -3.27013 | 10 |
| ITBEES | 15 | high | high | positive | 0 | 1.63079 | -1.15875e-12 | 3 |
| ITBEES | 15 | high | low | normal | -0.816593 | 2.45594 | -1.16655e-12 | 10 |
| ITBEES | 15 | high | mid | normal | 0 | 0.815395 | -5.79373e-13 | 16 |
| ITBEES | 15 | low | high | normal | 0 | 1.63212 | 0 | 151 |
| ITBEES | 15 | low | high | positive | 0 | 1.64015 | 0 | 23 |
| ITBEES | 15 | low | low | normal | 0 | 0 | 0 | 174 |
| ITBEES | 15 | low | low | positive | 0 | 0 | 0 | 17 |
| ITBEES | 15 | low | mid | normal | 0 | 0 | 0 | 164 |
| ITBEES | 15 | low | mid | positive | 0 | 0 | 0 | 21 |
| ITBEES | 15 | mid | high | normal | 0 | 0 | 0 | 755 |
| ITBEES | 15 | mid | high | positive | 0 | 0 | 0 | 30 |
| ITBEES | 15 | mid | low | normal | 0 | 0 | 0 | 752 |
| ITBEES | 15 | mid | low | positive | 0 | 1.62212 | -5.65989e-13 | 20 |
| ITBEES | 15 | mid | mid | normal | 0 | 0 | 0 | 770 |
| ITBEES | 15 | mid | mid | positive | 0 | 0 | 0 | 27 |
| ITBEES | 60 | high | high | normal | -1.6372 | 1.638 | -3.27332 | 11 |
| ITBEES | 60 | high | low | normal | 0 | 3.28192 | -3.26158 | 15 |
| ITBEES | 60 | high | mid | normal | -1.63854 | 1.6415 | -3.24992 | 22 |
| ITBEES | 60 | low | high | normal | 0 | 3.26584 | 0 | 54 |
| ITBEES | 60 | low | high | positive | -6.51997 | 6.51997 | 3.27279 | 3 |
| ITBEES | 60 | low | low | normal | 0 | 3.27708 | 0 | 71 |
| ITBEES | 60 | low | mid | normal | 0 | 1.63533 | 1.16007e-12 | 56 |
| ITBEES | 60 | low | mid | positive | -0.00213245 | 3.26531 | 1.16007e-12 | 2 |
| ITBEES | 60 | mid | high | normal | 0 | 1.62575 | 0 | 175 |
| ITBEES | 60 | mid | high | positive | -10000 | 10000 | -3.22217 | 1 |
| ITBEES | 60 | mid | low | normal | 0 | 3.21699 | 0 | 157 |
| ITBEES | 60 | mid | low | positive | -8.03342 | 8.03342 | -3.21337 | 1 |
| ITBEES | 60 | mid | mid | normal | 0 | 1.63159 | 0 | 170 |
| ITBEES | 60 | mid | mid | positive | 0 | 0 | 0 | 1 |
| ITC | 1 | high | high | normal | 0 | 0 | 0 | 996 |
| ITC | 1 | high | high | positive | 0 | 0 | 0 | 84 |
| ITC | 1 | high | low | normal | 0 | 0 | 0 | 1044 |
| ITC | 1 | high | low | positive | 0 | 0 | 0 | 73 |
| ITC | 1 | high | mid | normal | 0 | 0 | 0 | 818 |
| ITC | 1 | high | mid | positive | 0 | 0 | 0 | 67 |
| ITC | 1 | low | high | normal | 0 | 0 | 0 | 3469 |
| ITC | 1 | low | high | positive | 0 | 0 | 0 | 206 |
| ITC | 1 | low | low | normal | 0 | 0 | 0 | 2642 |
| ITC | 1 | low | low | positive | 0 | 0 | 0 | 162 |
| ITC | 1 | low | mid | normal | 0 | 0 | 0 | 2880 |
| ITC | 1 | low | mid | positive | 0 | 0 | 0 | 147 |
| ITC | 1 | mid | high | normal | 0 | 0 | 0 | 2546 |
| ITC | 1 | mid | high | positive | 0 | 0 | 0 | 177 |
| ITC | 1 | mid | low | normal | 0 | 0 | 0 | 3315 |
| ITC | 1 | mid | low | positive | 0 | 0 | 0 | 245 |
| ITC | 1 | mid | mid | normal | 0 | 0 | 0 | 3548 |
| ITC | 1 | mid | mid | positive | 0 | 0 | 0 | 245 |
| ITC | 5 | high | high | normal | 0 | 0 | 0 | 588 |
| ITC | 5 | high | high | positive | 0 | 0 | 0 | 95 |
| ITC | 5 | high | low | normal | 0 | 0 | 0 | 697 |
| ITC | 5 | high | low | positive | 0 | 0 | 0 | 58 |
| ITC | 5 | high | mid | normal | 0 | 0 | 0 | 647 |
| ITC | 5 | high | mid | positive | 0 | 0 | 0 | 70 |
| ITC | 5 | low | high | normal | 0 | 0 | 0 | 1144 |
| ITC | 5 | low | high | positive | 0 | 0.883314 | 0 | 101 |
| ITC | 5 | low | low | normal | 0 | 0 | 0 | 762 |
| ITC | 5 | low | low | positive | 0 | 0.881756 | 0 | 71 |
| ITC | 5 | low | mid | normal | 0 | 0 | 0 | 810 |
| ITC | 5 | low | mid | positive | 0 | 0.885347 | 0 | 71 |
| ITC | 5 | mid | high | normal | 0 | 0 | 0 | 802 |
| ITC | 5 | mid | high | positive | 0 | 0 | 0 | 77 |
| ITC | 5 | mid | low | normal | 0 | 0 | 0 | 1112 |
| ITC | 5 | mid | low | positive | 0 | 0 | 0 | 107 |
| ITC | 5 | mid | mid | normal | 0 | 0 | 0 | 1176 |
| ITC | 5 | mid | mid | positive | 0 | 0 | 0 | 117 |
| ITC | 15 | high | high | normal | 0 | 0.882846 | -2.0051e-12 | 232 |
| ITC | 15 | high | low | normal | 0 | 0.884017 | -1.76632 | 248 |
| ITC | 15 | high | low | positive | 0 | 0 | 0 | 1 |
| ITC | 15 | high | mid | normal | 0 | 0.883158 | 0 | 242 |
| ITC | 15 | low | high | normal | 0 | 0.886603 | 0 | 423 |
| ITC | 15 | low | low | normal | 0 | 0.883314 | 0 | 297 |
| ITC | 15 | low | low | positive | -10000 | 10000 | -1.77447 | 1 |
| ITC | 15 | low | mid | normal | 0 | 0.888494 | 2.00771e-12 | 317 |
| ITC | 15 | low | mid | positive | -3.10366 | 3.10366 | 0.886761 | 2 |
| ITC | 15 | mid | high | normal | 0 | 0.88433 | 0 | 317 |
| ITC | 15 | mid | low | normal | 0 | 0.883236 | 0 | 424 |
| ITC | 15 | mid | low | positive | -0.88199 | 0.88199 | 1.76398 | 1 |
| ITC | 15 | mid | mid | normal | 0 | 0.883236 | 0 | 438 |
| ITC | 60 | high | high | normal | 0 | 0.889284 | -1.77101 | 59 |
| ITC | 60 | high | low | normal | 0 | 1.77038 | -1.76975 | 57 |
| ITC | 60 | high | mid | normal | 0 | 1.77667 | -1.76819 | 62 |
| ITC | 60 | low | high | normal | 0 | 1.77667 | 2.0256e-12 | 109 |
| ITC | 60 | low | low | normal | 0 | 1.77179 | 0 | 84 |
| ITC | 60 | low | low | positive | -10000 | 10000 | -1.77447 | 1 |
| ITC | 60 | low | mid | normal | 0 | 1.77699 | 0.878503 | 82 |
| ITC | 60 | mid | high | normal | 0 | 0.888889 | 0 | 77 |
| ITC | 60 | mid | low | normal | -0.882768 | 0.888573 | 0 | 103 |
| ITC | 60 | mid | mid | normal | 0 | 0.889126 | 0 | 106 |
| JUNIORBEES | 1 | high | high | normal | 0 | 0.128239 | 0 | 2745 |
| JUNIORBEES | 1 | high | high | positive | 0 | 0.0646797 | 0 | 226 |
| JUNIORBEES | 1 | high | low | normal | 0 | 0.0646323 | 0 | 2642 |
| JUNIORBEES | 1 | high | low | positive | 0 | 0.0641342 | 0 | 231 |
| JUNIORBEES | 1 | high | mid | normal | 0 | 0.0647178 | 0 | 2649 |
| JUNIORBEES | 1 | high | mid | positive | 0 | 0.0642022 | 0 | 211 |
| JUNIORBEES | 1 | low | high | normal | 0 | 0.0641178 | 0 | 2488 |
| JUNIORBEES | 1 | low | high | positive | 0 | 0.0641309 | 0 | 185 |
| JUNIORBEES | 1 | low | low | normal | 0 | 0 | 0 | 3043 |
| JUNIORBEES | 1 | low | low | positive | 0 | 0 | 0 | 255 |
| JUNIORBEES | 1 | low | mid | normal | 0 | 0 | 0 | 2974 |
| JUNIORBEES | 1 | low | mid | positive | 0 | 0 | 0 | 205 |
| JUNIORBEES | 1 | mid | high | normal | 0 | 0.0641939 | 0 | 3042 |
| JUNIORBEES | 1 | mid | high | positive | 0 | 0.0641612 | 0 | 252 |
| JUNIORBEES | 1 | mid | low | normal | 0 | 0.0641906 | 0 | 2576 |
| JUNIORBEES | 1 | mid | low | positive | 0 | 0.0642376 | 0 | 192 |
| JUNIORBEES | 1 | mid | mid | normal | 0 | 0.0641943 | 0 | 2943 |
| JUNIORBEES | 1 | mid | mid | positive | 0 | 0.0646291 | 0 | 223 |
| JUNIORBEES | 5 | high | high | normal | 0 | 0.261486 | -0.129436 | 814 |
| JUNIORBEES | 5 | high | high | positive | 0 | 0.257618 | -0.12822 | 96 |
| JUNIORBEES | 5 | high | low | normal | 0 | 0.256667 | -0.1293 | 792 |
| JUNIORBEES | 5 | high | low | positive | 0 | 0.12839 | 0 | 75 |
| JUNIORBEES | 5 | high | mid | normal | 0 | 0.320661 | -0.129264 | 799 |
| JUNIORBEES | 5 | high | mid | positive | 0 | 0.320552 | -0.129363 | 77 |
| JUNIORBEES | 5 | low | high | normal | 0 | 0.191756 | 0 | 747 |
| JUNIORBEES | 5 | low | high | positive | 0 | 0.192561 | 0.129372 | 67 |
| JUNIORBEES | 5 | low | low | normal | 0 | 0.0642756 | 0 | 947 |
| JUNIORBEES | 5 | low | low | positive | 0 | 0.0641112 | 0 | 95 |
| JUNIORBEES | 5 | low | mid | normal | 0 | 0.0647266 | 0 | 925 |
| JUNIORBEES | 5 | low | mid | positive | 0 | 0.06466 | 0 | 69 |
| JUNIORBEES | 5 | mid | high | normal | 0 | 0.192569 | 0 | 991 |
| JUNIORBEES | 5 | mid | high | positive | 0 | 0.193881 | 0 | 103 |
| JUNIORBEES | 5 | mid | low | normal | 0 | 0.130783 | 0 | 816 |
| JUNIORBEES | 5 | mid | low | positive | 0 | 0.256313 | 0 | 93 |
| JUNIORBEES | 5 | mid | mid | normal | 0 | 0.192347 | 0 | 927 |
| JUNIORBEES | 5 | mid | mid | positive | 0 | 0.192408 | 0 | 106 |
| JUNIORBEES | 15 | high | high | normal | -0.0641797 | 0.449004 | -0.512701 | 336 |
| JUNIORBEES | 15 | high | low | normal | 0.0646425 | 0.577152 | -0.384744 | 325 |
| JUNIORBEES | 15 | high | mid | normal | 0.128236 | 0.647023 | -0.384998 | 309 |
| JUNIORBEES | 15 | high | mid | positive | 0.0641178 | 0.0641178 | -0.128236 | 1 |
| JUNIORBEES | 15 | low | high | normal | -0.0640326 | 0.640332 | 0.38518 | 282 |
| JUNIORBEES | 15 | low | low | normal | 0 | 0.323203 | 0 | 366 |
| JUNIORBEES | 15 | low | mid | normal | 0 | 0.323318 | 0 | 358 |
| JUNIORBEES | 15 | mid | high | normal | 0 | 0.44937 | 0 | 354 |
| JUNIORBEES | 15 | mid | low | normal | 0 | 0.384736 | -0.127853 | 281 |
| JUNIORBEES | 15 | mid | mid | normal | 0 | 0.320586 | 0 | 330 |
| JUNIORBEES | 60 | high | high | normal | -0.19239 | 1.04607 | -0.769482 | 87 |
| JUNIORBEES | 60 | high | low | normal | 0.22523 | 0.934094 | -0.834053 | 80 |
| JUNIORBEES | 60 | high | mid | normal | 0.517307 | 1.09945 | -0.769902 | 75 |
| JUNIORBEES | 60 | low | high | normal | -0.0640742 | 1.90009 | 1.66244 | 75 |
| JUNIORBEES | 60 | low | low | normal | 0 | 0.904412 | 0.646797 | 84 |
| JUNIORBEES | 60 | low | mid | normal | -0.0640911 | 1.22047 | 0.775921 | 103 |
| JUNIORBEES | 60 | mid | high | normal | 0 | 0.611422 | -0.129023 | 82 |
| JUNIORBEES | 60 | mid | low | normal | 0 | 1.25477 | -0.386525 | 80 |
| JUNIORBEES | 60 | mid | mid | normal | 0.0323162 | 0.77059 | 0 | 72 |
| KOTAKBANK | 1 | high | high | normal | 0 | 0 | 0 | 1346 |
| KOTAKBANK | 1 | high | high | positive | 0 | 0 | 0 | 72 |
| KOTAKBANK | 1 | high | low | normal | 0 | 0 | 0 | 2259 |
| KOTAKBANK | 1 | high | low | positive | 0 | 0 | 0 | 115 |
| KOTAKBANK | 1 | high | mid | normal | 0 | 0 | 0 | 2104 |
| KOTAKBANK | 1 | high | mid | positive | 0 | 0 | 0 | 99 |
| KOTAKBANK | 1 | low | high | normal | 0 | 0 | 0 | 4389 |
| KOTAKBANK | 1 | low | high | positive | 0 | 0 | 0 | 213 |
| KOTAKBANK | 1 | low | low | normal | 0 | 0 | 0 | 3530 |
| KOTAKBANK | 1 | low | low | positive | 0 | 0 | 0 | 194 |
| KOTAKBANK | 1 | low | mid | normal | 0 | 0 | 0 | 3983 |
| KOTAKBANK | 1 | low | mid | positive | 0 | 0 | 0 | 208 |
| KOTAKBANK | 1 | mid | high | normal | 0 | 0 | 0 | 1812 |
| KOTAKBANK | 1 | mid | high | positive | 0 | 0 | 0 | 105 |
| KOTAKBANK | 1 | mid | low | normal | 0 | 0 | 0 | 1726 |
| KOTAKBANK | 1 | mid | low | positive | 0 | 0 | 0 | 113 |
| KOTAKBANK | 1 | mid | mid | normal | 0 | 0 | 0 | 1690 |
| KOTAKBANK | 1 | mid | mid | positive | 0 | 0 | 0 | 93 |
| KOTAKBANK | 5 | high | high | normal | 0 | 0.661026 | -1.5333e-12 | 485 |
| KOTAKBANK | 5 | high | high | positive | 0 | 0.674536 | -1.34309 | 39 |
| KOTAKBANK | 5 | high | low | normal | 0 | 0.670556 | -1.49993e-12 | 765 |
| KOTAKBANK | 5 | high | low | positive | 0 | 0.675493 | -1.3395 | 65 |
| KOTAKBANK | 5 | high | mid | normal | 0 | 0.663504 | -1.49943e-12 | 714 |
| KOTAKBANK | 5 | high | mid | positive | 0 | 0.673537 | -1.31813 | 49 |
| KOTAKBANK | 5 | low | high | normal | 0 | 0 | 0 | 1486 |
| KOTAKBANK | 5 | low | high | positive | 0 | 0 | 0 | 104 |
| KOTAKBANK | 5 | low | low | normal | 0 | 0 | 0 | 1222 |
| KOTAKBANK | 5 | low | low | positive | 0 | 0.659326 | 0 | 115 |
| KOTAKBANK | 5 | low | mid | normal | 0 | 0 | 0 | 1361 |
| KOTAKBANK | 5 | low | mid | positive | 0 | 0.328926 | 0 | 122 |
| KOTAKBANK | 5 | mid | high | normal | 0 | 0.658892 | 0 | 622 |
| KOTAKBANK | 5 | mid | high | positive | 0 | 0.669165 | 0 | 70 |
| KOTAKBANK | 5 | mid | low | normal | 0 | 0.658935 | 0 | 588 |
| KOTAKBANK | 5 | mid | low | positive | 0 | 0.669703 | 0 | 51 |
| KOTAKBANK | 5 | mid | mid | normal | 0 | 0.658762 | 0 | 591 |
| KOTAKBANK | 5 | mid | mid | positive | 0 | 0.671051 | -1.31562 | 55 |
| KOTAKBANK | 15 | high | high | normal | -1.49421e-12 | 1.31796 | -1.31857 | 195 |
| KOTAKBANK | 15 | high | low | normal | 0 | 1.34382 | -1.31796 | 307 |
| KOTAKBANK | 15 | high | mid | normal | 0 | 1.31987 | -1.31813 | 275 |
| KOTAKBANK | 15 | low | high | normal | 0 | 1.33289 | 0 | 543 |
| KOTAKBANK | 15 | low | low | normal | 0 | 1.32406 | 0 | 460 |
| KOTAKBANK | 15 | low | mid | normal | 0 | 1.33842 | 0 | 498 |
| KOTAKBANK | 15 | mid | high | normal | 0 | 1.31553 | 0 | 234 |
| KOTAKBANK | 15 | mid | low | normal | 0 | 1.31683 | 0 | 205 |
| KOTAKBANK | 15 | mid | mid | normal | 0 | 0.677277 | -1.52602e-12 | 226 |
| KOTAKBANK | 60 | high | high | normal | 0 | 2.63487 | -1.343 | 39 |
| KOTAKBANK | 60 | high | low | normal | 0.658545 | 2.63557 | -1.34599 | 57 |
| KOTAKBANK | 60 | high | mid | normal | 0.337906 | 3.29392 | -1.31913 | 68 |
| KOTAKBANK | 60 | low | high | normal | 0 | 1.35172 | 1.49884e-12 | 94 |
| KOTAKBANK | 60 | low | low | normal | 0 | 2.63522 | 7.48186e-13 | 90 |
| KOTAKBANK | 60 | low | mid | normal | 0 | 2.00682 | 1.53891e-12 | 81 |
| KOTAKBANK | 60 | mid | high | normal | -0.662861 | 3.94763 | 0 | 112 |
| KOTAKBANK | 60 | mid | low | normal | -0.66289 | 2.63453 | 0 | 98 |
| KOTAKBANK | 60 | mid | mid | normal | 0 | 3.38891 | 0 | 101 |
| LT | 1 | high | high | normal | 0 | 0.12837 | 0 | 2369 |
| LT | 1 | high | high | positive | 0 | 0 | 0 | 135 |
| LT | 1 | high | low | normal | 0 | 0.128342 | 0 | 2546 |
| LT | 1 | high | low | positive | 0 | 0.126758 | 0 | 138 |
| LT | 1 | high | mid | normal | 0 | 0.128818 | 0 | 2547 |
| LT | 1 | high | mid | positive | 0 | 0 | 0 | 125 |
| LT | 1 | low | high | normal | 0 | 0 | 0 | 3096 |
| LT | 1 | low | high | positive | 0 | 0 | 0 | 163 |
| LT | 1 | low | low | normal | 0 | 0 | 0 | 2632 |
| LT | 1 | low | low | positive | 0 | 0 | 0 | 151 |
| LT | 1 | low | mid | normal | 0 | 0 | 0 | 3025 |
| LT | 1 | low | mid | positive | 0 | 0 | 0 | 156 |
| LT | 1 | mid | high | normal | 0 | 0 | 0 | 2686 |
| LT | 1 | mid | high | positive | 0 | 0 | 0 | 144 |
| LT | 1 | mid | low | normal | 0 | 0 | 0 | 2968 |
| LT | 1 | mid | low | positive | 0 | 0 | 0 | 159 |
| LT | 1 | mid | mid | normal | 0 | 0 | 0 | 2822 |
| LT | 1 | mid | mid | positive | 0 | 0 | 0 | 178 |
| LT | 5 | high | high | normal | 0 | 0.507692 | -0.503651 | 767 |
| LT | 5 | high | high | positive | 0 | 0.701995 | -0.512287 | 62 |
| LT | 5 | high | low | normal | 0 | 0.508757 | -0.507795 | 863 |
| LT | 5 | high | low | positive | 0 | 0.638855 | -0.767636 | 70 |
| LT | 5 | high | mid | normal | 0 | 0.508828 | -0.507743 | 906 |
| LT | 5 | high | mid | positive | 0 | 0.38011 | -0.381047 | 60 |
| LT | 5 | low | high | normal | 0 | 0.128468 | 0 | 1008 |
| LT | 5 | low | high | positive | 0 | 0.128629 | 0 | 87 |
| LT | 5 | low | low | normal | 0 | 0.254913 | 0 | 854 |
| LT | 5 | low | low | positive | 0 | 0.640148 | 0.508684 | 72 |
| LT | 5 | low | mid | normal | 0 | 0.253577 | 0 | 952 |
| LT | 5 | low | mid | positive | 0 | 0.255268 | 0 | 94 |
| LT | 5 | mid | high | normal | 0 | 0.257296 | 0 | 842 |
| LT | 5 | mid | high | positive | 0 | 0.63505 | 0 | 59 |
| LT | 5 | mid | low | normal | 0 | 0.254659 | 0 | 894 |
| LT | 5 | mid | low | positive | 0 | 0.255995 | 0 | 72 |
| LT | 5 | mid | mid | normal | 0 | 0.254858 | 0 | 829 |
| LT | 5 | mid | mid | positive | 0 | 0.511012 | 0 | 69 |
| LT | 15 | high | high | normal | -0.127304 | 1.21301 | -1.01064 | 268 |
| LT | 15 | high | low | normal | -5.72961e-13 | 0.898761 | -1.01487 | 326 |
| LT | 15 | high | mid | normal | 0 | 1.01586 | -1.01804 | 343 |
| LT | 15 | low | high | normal | 0 | 1.00805 | 0.256151 | 387 |
| LT | 15 | low | low | normal | 0 | 1.01715 | 0.25608 | 326 |
| LT | 15 | low | mid | normal | 0 | 1.02015 | 0.257013 | 346 |
| LT | 15 | mid | high | normal | 0 | 1.01406 | 0 | 317 |
| LT | 15 | mid | low | normal | 0 | 0.892738 | 0 | 320 |
| LT | 15 | mid | mid | normal | 0 | 0.888658 | 0 | 310 |
| LT | 60 | high | high | normal | 0 | 2.92729 | -1.52306 | 67 |
| LT | 60 | high | low | normal | -1.14866 | 2.66682 | -1.26861 | 78 |
| LT | 60 | high | mid | normal | -0.127016 | 3.0802 | -1.27016 | 83 |
| LT | 60 | low | high | normal | 0 | 2.49378 | 0.509042 | 100 |
| LT | 60 | low | low | normal | -0.317393 | 2.684 | 0.509658 | 86 |
| LT | 60 | low | mid | normal | -0.25443 | 2.1604 | 0.508861 | 85 |
| LT | 60 | mid | high | normal | -0.0635389 | 2.27621 | 1.15946e-12 | 78 |
| LT | 60 | mid | low | normal | -0.508873 | 3.04588 | -0.254165 | 81 |
| LT | 60 | mid | mid | normal | -0.318766 | 2.64524 | 0 | 82 |
| M&M | 1 | high | high | normal | 0 | 0.160026 | 0 | 2021 |
| M&M | 1 | high | high | positive | 0 | 0 | 0 | 91 |
| M&M | 1 | high | low | normal | 0 | 0.160285 | 0 | 2376 |
| M&M | 1 | high | low | positive | 0 | 0 | 0 | 125 |
| M&M | 1 | high | mid | normal | 0 | 0.16022 | 0 | 2292 |
| M&M | 1 | high | mid | positive | 0 | 0 | 0 | 120 |
| M&M | 1 | low | high | normal | 0 | 0 | 0 | 2668 |
| M&M | 1 | low | high | positive | 0 | 0 | 0 | 127 |
| M&M | 1 | low | low | normal | 0 | 0 | 0 | 2614 |
| M&M | 1 | low | low | positive | 0 | 0 | 0 | 127 |
| M&M | 1 | low | mid | normal | 0 | 0 | 0 | 2680 |
| M&M | 1 | low | mid | positive | 0 | 0 | 0 | 122 |
| M&M | 1 | mid | high | normal | 0 | 0 | 0 | 2800 |
| M&M | 1 | mid | high | positive | 0 | 0 | 0 | 121 |
| M&M | 1 | mid | low | normal | 0 | 0 | 0 | 2470 |
| M&M | 1 | mid | low | positive | 0 | 0 | 0 | 119 |
| M&M | 1 | mid | mid | normal | 0 | 0 | 0 | 2743 |
| M&M | 1 | mid | mid | positive | 0 | 0 | 0 | 112 |
| M&M | 5 | high | high | normal | 0 | 0.479635 | -0.321146 | 776 |
| M&M | 5 | high | high | positive | 0 | 0.805023 | -0.641941 | 39 |
| M&M | 5 | high | low | normal | 0 | 0.482594 | -0.321399 | 883 |
| M&M | 5 | high | low | positive | 0 | 0.644527 | -0.322534 | 61 |
| M&M | 5 | high | mid | normal | 0 | 0.483162 | -0.32128 | 830 |
| M&M | 5 | high | mid | positive | 0 | 0.482789 | 0 | 73 |
| M&M | 5 | low | high | normal | 0 | 0 | 0 | 910 |
| M&M | 5 | low | high | positive | 0 | 0.320917 | 0 | 64 |
| M&M | 5 | low | low | normal | 0 | 0 | 0 | 936 |
| M&M | 5 | low | low | positive | 0 | 0.160811 | 0 | 48 |
| M&M | 5 | low | mid | normal | 0 | 0 | 0 | 981 |
| M&M | 5 | low | mid | positive | 0 | 0.161977 | 0 | 63 |
| M&M | 5 | mid | high | normal | 0 | 0.161285 | 0 | 938 |
| M&M | 5 | mid | high | positive | 0 | 0.321983 | -0.15978 | 64 |
| M&M | 5 | mid | low | normal | 0 | 0.319813 | 0 | 820 |
| M&M | 5 | mid | low | positive | 0 | 0.481628 | 0 | 44 |
| M&M | 5 | mid | mid | normal | 0 | 0.319514 | 0 | 875 |
| M&M | 5 | mid | mid | positive | 0 | 0.323782 | 0 | 50 |
| M&M | 15 | high | high | normal | 0 | 1.11889 | -0.962757 | 263 |
| M&M | 15 | high | low | normal | 0 | 1.28673 | -0.965437 | 323 |
| M&M | 15 | high | mid | normal | -0.157581 | 1.28211 | -0.96343 | 296 |
| M&M | 15 | low | high | normal | 0 | 0.800884 | 1.45591e-12 | 333 |
| M&M | 15 | low | low | normal | 0 | 0.643863 | 0 | 343 |
| M&M | 15 | low | mid | normal | 0 | 0.798811 | 1.46383e-12 | 375 |
| M&M | 15 | mid | high | normal | 0 | 0.806387 | 0 | 376 |
| M&M | 15 | mid | low | normal | 0 | 1.12633 | 0 | 306 |
| M&M | 15 | mid | mid | normal | 0 | 0.804797 | 0 | 328 |
| M&M | 60 | high | high | normal | -0.0799872 | 2.57145 | -1.27863 | 70 |
| M&M | 60 | high | low | normal | -0.479862 | 3.67941 | -0.966261 | 75 |
| M&M | 60 | high | mid | normal | 0 | 3.35587 | -1.60725 | 79 |
| M&M | 60 | low | high | normal | -0.560134 | 2.55806 | 0.321937 | 82 |
| M&M | 60 | low | low | normal | 0 | 1.76217 | 0.639376 | 77 |
| M&M | 60 | low | mid | normal | 0 | 2.24711 | 0.322342 | 96 |
| M&M | 60 | mid | high | normal | 0 | 3.72868 | 0 | 93 |
| M&M | 60 | mid | low | normal | -0.480723 | 2.8879 | -1.46657e-12 | 93 |
| M&M | 60 | mid | mid | normal | 0.800102 | 2.75415 | 0 | 75 |
| MARUTI | 1 | high | high | normal | 0 | 0.350128 | 0 | 1584 |
| MARUTI | 1 | high | high | positive | 0 | 0.359701 | 0 | 102 |
| MARUTI | 1 | high | low | normal | 0 | 0 | 0 | 2315 |
| MARUTI | 1 | high | low | positive | 0 | 0 | 0 | 144 |
| MARUTI | 1 | high | mid | normal | 0 | 0 | 0 | 2100 |
| MARUTI | 1 | high | mid | positive | 0 | 0 | 0 | 130 |
| MARUTI | 1 | low | high | normal | 0 | 0 | 0 | 3359 |
| MARUTI | 1 | low | high | positive | 0 | 0 | 0 | 207 |
| MARUTI | 1 | low | low | normal | 0 | 0 | 0 | 2829 |
| MARUTI | 1 | low | low | positive | 0 | 0 | 0 | 206 |
| MARUTI | 1 | low | mid | normal | 0 | 0 | 0 | 3325 |
| MARUTI | 1 | low | mid | positive | 0 | 0 | 0 | 229 |
| MARUTI | 1 | mid | high | normal | 0 | 0 | 0 | 2340 |
| MARUTI | 1 | mid | high | positive | 0 | 0 | 0 | 130 |
| MARUTI | 1 | mid | low | normal | 0 | 0 | 0 | 2097 |
| MARUTI | 1 | mid | low | positive | 0 | 0 | 0 | 133 |
| MARUTI | 1 | mid | mid | normal | 0 | 0 | 0 | 2042 |
| MARUTI | 1 | mid | mid | positive | 0 | 0 | 0 | 128 |
| MARUTI | 5 | high | high | normal | 0 | 0.362582 | -0.700403 | 547 |
| MARUTI | 5 | high | high | positive | 0 | 0.724218 | -0.722753 | 46 |
| MARUTI | 5 | high | low | normal | 0 | 0.364392 | -0.717798 | 796 |
| MARUTI | 5 | high | low | positive | 0 | 0.540482 | -0.721983 | 80 |
| MARUTI | 5 | high | mid | normal | 0 | 0.362463 | -0.714988 | 726 |
| MARUTI | 5 | high | mid | positive | 0 | 0.720813 | -0.721696 | 64 |
| MARUTI | 5 | low | high | normal | 0 | 0.35926 | 0 | 1174 |
| MARUTI | 5 | low | high | positive | 0 | 0.358976 | 0 | 99 |
| MARUTI | 5 | low | low | normal | 0 | 0.349901 | 0 | 1012 |
| MARUTI | 5 | low | low | positive | 0 | 0.360933 | 0 | 95 |
| MARUTI | 5 | low | mid | normal | 0 | 0 | 0 | 1168 |
| MARUTI | 5 | low | mid | positive | 0 | 0.358359 | 0 | 120 |
| MARUTI | 5 | mid | high | normal | 0 | 0.361337 | 0 | 847 |
| MARUTI | 5 | mid | high | positive | 0 | 0.362713 | 0 | 72 |
| MARUTI | 5 | mid | low | normal | 0 | 0.361226 | 0 | 754 |
| MARUTI | 5 | mid | low | positive | 0 | 0.363848 | 0 | 51 |
| MARUTI | 5 | mid | mid | normal | 0 | 0.36137 | 0 | 730 |
| MARUTI | 5 | mid | mid | positive | 0 | 0.362739 | 0 | 64 |
| MARUTI | 15 | high | high | normal | 0 | 1.42273 | -1.43277 | 201 |
| MARUTI | 15 | high | high | positive | -1.09381 | 1.09381 | -0.729208 | 1 |
| MARUTI | 15 | high | low | normal | 0 | 1.43534 | -1.43302 | 315 |
| MARUTI | 15 | high | low | positive | -2.16419 | 2.16419 | -4.32838 | 1 |
| MARUTI | 15 | high | mid | normal | 0 | 1.43526 | -1.4259 | 262 |
| MARUTI | 15 | high | mid | positive | -10000 | 10000 | -15.1521 | 1 |
| MARUTI | 15 | low | high | normal | 0 | 1.08727 | 0 | 460 |
| MARUTI | 15 | low | low | normal | 0 | 1.08364 | 0 | 398 |
| MARUTI | 15 | low | mid | normal | 0 | 0.728491 | 0 | 454 |
| MARUTI | 15 | low | mid | positive | -0.724953 | 0.724953 | 0 | 2 |
| MARUTI | 15 | mid | high | normal | 0 | 1.07772 | 0 | 310 |
| MARUTI | 15 | mid | low | normal | 0 | 1.07666 | 0 | 258 |
| MARUTI | 15 | mid | mid | normal | 0 | 1.08794 | 0 | 280 |
| MARUTI | 60 | high | high | normal | -0.361324 | 2.5184 | -1.42363 | 50 |
| MARUTI | 60 | high | high | positive | -10000 | 10000 | -15.1521 | 1 |
| MARUTI | 60 | high | low | normal | 0 | 2.4935 | -1.44943 | 85 |
| MARUTI | 60 | high | mid | normal | 0.358809 | 3.64126 | -1.44645 | 65 |
| MARUTI | 60 | low | high | normal | 0 | 2.16263 | 0.718856 | 111 |
| MARUTI | 60 | low | low | normal | -0.179921 | 2.17328 | 0 | 94 |
| MARUTI | 60 | low | mid | normal | 0.360477 | 2.86913 | 0.721787 | 115 |
| MARUTI | 60 | mid | high | normal | -0.724953 | 3.26205 | 0 | 83 |
| MARUTI | 60 | mid | low | normal | 0 | 2.16092 | 0 | 66 |
| MARUTI | 60 | mid | mid | normal | 0.359706 | 3.05443 | 0 | 70 |
| NESTLEIND | 1 | high | high | normal | 0 | 0 | 0 | 1150 |
| NESTLEIND | 1 | high | high | positive | 0 | 0 | 0 | 59 |
| NESTLEIND | 1 | high | low | normal | 0 | 0 | 0 | 1451 |
| NESTLEIND | 1 | high | low | positive | 0 | 0 | 0 | 84 |
| NESTLEIND | 1 | high | mid | normal | 0 | 0 | 0 | 1464 |
| NESTLEIND | 1 | high | mid | positive | 0 | 0 | 0 | 72 |
| NESTLEIND | 1 | low | high | normal | 0 | 0 | 0 | 2030 |
| NESTLEIND | 1 | low | high | positive | 0 | 0 | 0 | 104 |
| NESTLEIND | 1 | low | low | normal | 0 | 0 | 0 | 1956 |
| NESTLEIND | 1 | low | low | positive | 0 | 0 | 0 | 78 |
| NESTLEIND | 1 | low | mid | normal | 0 | 0 | 0 | 1898 |
| NESTLEIND | 1 | low | mid | positive | 0 | 0 | 0 | 88 |
| NESTLEIND | 1 | mid | high | normal | 0 | 0 | 0 | 1630 |
| NESTLEIND | 1 | mid | high | positive | 0 | 0 | 0 | 68 |
| NESTLEIND | 1 | mid | low | normal | 0 | 0 | 0 | 1397 |
| NESTLEIND | 1 | mid | low | positive | 0 | 0 | 0 | 75 |
| NESTLEIND | 1 | mid | mid | normal | 0 | 0 | 0 | 1593 |
| NESTLEIND | 1 | mid | mid | positive | 0 | 0 | 0 | 78 |
| NESTLEIND | 5 | high | high | normal | 0 | 0.344649 | 0 | 648 |
| NESTLEIND | 5 | high | high | positive | 0 | 0.339697 | -0.339559 | 38 |
| NESTLEIND | 5 | high | low | normal | 0 | 0.343808 | 0 | 785 |
| NESTLEIND | 5 | high | low | positive | 0 | 0.342264 | 0 | 50 |
| NESTLEIND | 5 | high | mid | normal | 0 | 0.344163 | -1.56314e-12 | 789 |
| NESTLEIND | 5 | high | mid | positive | 0 | 0.341542 | -0.682384 | 49 |
| NESTLEIND | 5 | low | high | normal | 0 | 0.343454 | 0 | 1037 |
| NESTLEIND | 5 | low | high | positive | 0 | 0.679232 | 0 | 71 |
| NESTLEIND | 5 | low | low | normal | 0 | 0 | 0 | 1079 |
| NESTLEIND | 5 | low | low | positive | 0 | 0.341064 | 0 | 37 |
| NESTLEIND | 5 | low | mid | normal | 0 | 0.340194 | 0 | 1009 |
| NESTLEIND | 5 | low | mid | positive | 0 | 0.344092 | 0 | 62 |
| NESTLEIND | 5 | mid | high | normal | 0 | 0.341565 | 0 | 835 |
| NESTLEIND | 5 | mid | high | positive | 0 | 0.680473 | 0 | 42 |
| NESTLEIND | 5 | mid | low | normal | 0 | 0.3416 | 0 | 689 |
| NESTLEIND | 5 | mid | low | positive | 0 | 0.679025 | 0 | 32 |
| NESTLEIND | 5 | mid | mid | normal | 0 | 0.341799 | 0 | 797 |
| NESTLEIND | 5 | mid | mid | positive | 0 | 0.51108 | 0 | 44 |
| NESTLEIND | 15 | high | high | normal | 0 | 1.02627 | -0.68937 | 237 |
| NESTLEIND | 15 | high | high | positive | -0.342185 | 0.342185 | -0.679163 | 2 |
| NESTLEIND | 15 | high | low | normal | -0.339443 | 1.02131 | -0.688942 | 315 |
| NESTLEIND | 15 | high | low | positive | -2.03197 | 2.03197 | -0.688658 | 5 |
| NESTLEIND | 15 | high | mid | normal | -1.56572e-12 | 1.02096 | -0.689655 | 317 |
| NESTLEIND | 15 | high | mid | positive | -0.343489 | 0.343489 | -0.686978 | 3 |
| NESTLEIND | 15 | low | high | normal | 0 | 1.01906 | 0.679048 | 405 |
| NESTLEIND | 15 | low | high | positive | 0.854555 | 1.53883 | 1.0261 | 6 |
| NESTLEIND | 15 | low | low | normal | 0 | 0.690799 | 1.56099e-12 | 392 |
| NESTLEIND | 15 | low | low | positive | -1.0203 | 3.08415 | 1.36925 | 4 |
| NESTLEIND | 15 | low | mid | normal | 0 | 1.02103 | 1.55517e-12 | 377 |
| NESTLEIND | 15 | low | mid | positive | 0 | 0 | 1.35745 | 3 |
| NESTLEIND | 15 | mid | high | normal | 0 | 1.03194 | 0 | 316 |
| NESTLEIND | 15 | mid | high | positive | -0.853834 | 2.053 | -1.36524 | 6 |
| NESTLEIND | 15 | mid | low | normal | 0 | 0.687155 | 0 | 254 |
| NESTLEIND | 15 | mid | low | positive | 1.3683 | 1.71157 | 0.685473 | 2 |
| NESTLEIND | 15 | mid | mid | normal | 0 | 1.02124 | 0 | 299 |
| NESTLEIND | 60 | high | high | normal | 0.680773 | 2.75161 | -1.38117 | 62 |
| NESTLEIND | 60 | high | low | normal | -0.688919 | 2.37546 | -1.36333 | 85 |
| NESTLEIND | 60 | high | mid | normal | -0.68147 | 2.71499 | -1.35777 | 84 |
| NESTLEIND | 60 | low | high | normal | -0.680203 | 2.73308 | 0.683691 | 103 |
| NESTLEIND | 60 | low | low | normal | -0.34408 | 2.05777 | 0.679745 | 106 |
| NESTLEIND | 60 | low | mid | normal | 0 | 2.03611 | 0.678841 | 93 |
| NESTLEIND | 60 | mid | high | normal | -0.343678 | 2.7149 | 0 | 79 |
| NESTLEIND | 60 | mid | high | positive | 0.687002 | 0.687002 | 1.374 | 1 |
| NESTLEIND | 60 | mid | low | normal | 0 | 2.22348 | -1.56784e-12 | 54 |
| NESTLEIND | 60 | mid | mid | normal | 0.340414 | 2.74678 | -1.56324e-12 | 73 |
| NIFTYBEES | 1 | high | high | normal | 0 | 0 | 0 | 1770 |
| NIFTYBEES | 1 | high | high | positive | 0 | 0 | 0 | 107 |
| NIFTYBEES | 1 | high | low | normal | 0 | 0 | 0 | 2251 |
| NIFTYBEES | 1 | high | low | positive | 0 | 0 | 0 | 154 |
| NIFTYBEES | 1 | high | mid | normal | 0 | 0 | 0 | 2443 |
| NIFTYBEES | 1 | high | mid | positive | 0 | 0 | 0 | 144 |
| NIFTYBEES | 1 | low | high | normal | 0 | 0 | 0 | 3298 |
| NIFTYBEES | 1 | low | high | positive | 0 | 0 | 0 | 181 |
| NIFTYBEES | 1 | low | low | normal | 0 | 0 | 0 | 2608 |
| NIFTYBEES | 1 | low | low | positive | 0 | 0 | 0 | 134 |
| NIFTYBEES | 1 | low | mid | normal | 0 | 0 | 0 | 2647 |
| NIFTYBEES | 1 | low | mid | positive | 0 | 0 | 0 | 167 |
| NIFTYBEES | 1 | mid | high | normal | 0 | 0 | 0 | 2509 |
| NIFTYBEES | 1 | mid | high | positive | 0 | 0 | 0 | 141 |
| NIFTYBEES | 1 | mid | low | normal | 0 | 0 | 0 | 2695 |
| NIFTYBEES | 1 | mid | low | positive | 0 | 0 | 0 | 166 |
| NIFTYBEES | 1 | mid | mid | normal | 0 | 0 | 0 | 2686 |
| NIFTYBEES | 1 | mid | mid | positive | 0 | 0 | 0 | 160 |
| NIFTYBEES | 5 | high | high | normal | 0 | 0.182772 | 0 | 601 |
| NIFTYBEES | 5 | high | high | positive | 0 | 0.182379 | 0 | 40 |
| NIFTYBEES | 5 | high | low | normal | 0 | 0.182825 | 0 | 784 |
| NIFTYBEES | 5 | high | low | positive | 0 | 0.182876 | 0 | 52 |
| NIFTYBEES | 5 | high | mid | normal | 0 | 0.182732 | 0 | 811 |
| NIFTYBEES | 5 | high | mid | positive | 0 | 0.181855 | 0 | 47 |
| NIFTYBEES | 5 | low | high | normal | 0 | 0 | 0 | 1132 |
| NIFTYBEES | 5 | low | high | positive | 0 | 0.181812 | 0 | 76 |
| NIFTYBEES | 5 | low | low | normal | 0 | 0 | 0 | 855 |
| NIFTYBEES | 5 | low | low | positive | 0 | 0 | 0 | 49 |
| NIFTYBEES | 5 | low | mid | normal | 0 | 0 | 0 | 873 |
| NIFTYBEES | 5 | low | mid | positive | 0 | 0.181845 | 0 | 74 |
| NIFTYBEES | 5 | mid | high | normal | 0 | 0.181795 | 0 | 900 |
| NIFTYBEES | 5 | mid | high | positive | 0 | 0.181798 | 0 | 56 |
| NIFTYBEES | 5 | mid | low | normal | 0 | 0.18165 | 0 | 991 |
| NIFTYBEES | 5 | mid | low | positive | 0 | 0 | 0 | 74 |
| NIFTYBEES | 5 | mid | mid | normal | 0 | 0.181633 | 0 | 1015 |
| NIFTYBEES | 5 | mid | mid | positive | 0 | 0.181775 | 0 | 66 |
| NIFTYBEES | 15 | high | high | normal | 0 | 0.368929 | -0.726889 | 219 |
| NIFTYBEES | 15 | high | low | normal | 0 | 0.365564 | -0.366119 | 301 |
| NIFTYBEES | 15 | high | mid | normal | 0 | 0.365417 | -0.368019 | 323 |
| NIFTYBEES | 15 | low | high | normal | 0 | 0.36404 | 2.07974e-12 | 405 |
| NIFTYBEES | 15 | low | low | normal | 0 | 0.36545 | 2.067e-12 | 293 |
| NIFTYBEES | 15 | low | mid | normal | 0 | 0.363967 | 0.363501 | 316 |
| NIFTYBEES | 15 | mid | high | normal | 0 | 0.365992 | 0 | 348 |
| NIFTYBEES | 15 | mid | low | normal | 0 | 0.363583 | 0 | 379 |
| NIFTYBEES | 15 | mid | mid | normal | 0 | 0.183332 | 0 | 359 |
| NIFTYBEES | 60 | high | high | normal | 2.09025e-12 | 0.909537 | -1.09144 | 49 |
| NIFTYBEES | 60 | high | low | normal | 0.181926 | 1.09075 | -1.09088 | 92 |
| NIFTYBEES | 60 | high | mid | normal | 0.18164 | 0.909422 | -1.09131 | 84 |
| NIFTYBEES | 60 | low | high | normal | -0.181812 | 1.28034 | 0.36762 | 119 |
| NIFTYBEES | 60 | low | low | normal | 0.181984 | 1.09104 | 0.727339 | 62 |
| NIFTYBEES | 60 | low | mid | normal | 0 | 1.09032 | 0.366275 | 74 |
| NIFTYBEES | 60 | mid | high | normal | -0.273241 | 1.36686 | 0 | 76 |
| NIFTYBEES | 60 | mid | low | normal | 0.181855 | 0.909678 | -1.03273e-12 | 90 |
| NIFTYBEES | 60 | mid | mid | normal | 0.181762 | 1.28008 | -0.363286 | 93 |
| ONGC | 1 | high | high | normal | 0 | 0 | 0 | 1651 |
| ONGC | 1 | high | high | positive | 0 | 0 | 0 | 113 |
| ONGC | 1 | high | low | normal | 0 | 0 | 0 | 1963 |
| ONGC | 1 | high | low | positive | 0 | 0 | 0 | 140 |
| ONGC | 1 | high | mid | normal | 0 | 0 | 0 | 1961 |
| ONGC | 1 | high | mid | positive | 0 | 0 | 0 | 138 |
| ONGC | 1 | low | high | normal | 0 | 0 | 0 | 2404 |
| ONGC | 1 | low | high | positive | 0 | 0 | 0 | 152 |
| ONGC | 1 | low | low | normal | 0 | 0 | 0 | 2240 |
| ONGC | 1 | low | low | positive | 0 | 0 | 0 | 145 |
| ONGC | 1 | low | mid | normal | 0 | 0 | 0 | 2256 |
| ONGC | 1 | low | mid | positive | 0 | 0 | 0 | 151 |
| ONGC | 1 | mid | high | normal | 0 | 0 | 0 | 1919 |
| ONGC | 1 | mid | high | positive | 0 | 0 | 0 | 129 |
| ONGC | 1 | mid | low | normal | 0 | 0 | 0 | 1760 |
| ONGC | 1 | mid | low | positive | 0 | 0 | 0 | 122 |
| ONGC | 1 | mid | mid | normal | 0 | 0 | 0 | 1908 |
| ONGC | 1 | mid | mid | positive | 0 | 0 | 0 | 146 |
| ONGC | 5 | high | high | normal | 0 | 0.205036 | -1.16424e-12 | 686 |
| ONGC | 5 | high | high | positive | 0 | 0.612645 | -0.410164 | 53 |
| ONGC | 5 | high | low | normal | 0 | 0.407465 | -0.407191 | 787 |
| ONGC | 5 | high | low | positive | 0 | 0.204687 | -0.409098 | 59 |
| ONGC | 5 | high | mid | normal | 0 | 0.205225 | -0.407266 | 765 |
| ONGC | 5 | high | mid | positive | 0 | 0.204893 | 0 | 65 |
| ONGC | 5 | low | high | normal | 0 | 0 | 0 | 1037 |
| ONGC | 5 | low | high | positive | 0 | 0.204344 | 0 | 65 |
| ONGC | 5 | low | low | normal | 0 | 0 | 0 | 1007 |
| ONGC | 5 | low | low | positive | 0 | 0.408405 | 0 | 59 |
| ONGC | 5 | low | mid | normal | 0 | 0 | 0 | 990 |
| ONGC | 5 | low | mid | positive | 0 | 0.204507 | 0 | 65 |
| ONGC | 5 | mid | high | normal | 0 | 0.204578 | 0 | 833 |
| ONGC | 5 | mid | high | positive | 0 | 0.204855 | 0 | 70 |
| ONGC | 5 | mid | low | normal | 0 | 0.20452 | 0 | 773 |
| ONGC | 5 | mid | low | positive | 0 | 0 | 0 | 59 |
| ONGC | 5 | mid | mid | normal | 0 | 0.204597 | 0 | 878 |
| ONGC | 5 | mid | mid | positive | 0 | 0.204989 | 0 | 65 |
| ONGC | 15 | high | high | normal | 0 | 1.22669 | -0.817804 | 280 |
| ONGC | 15 | high | low | normal | 0.203251 | 1.02212 | -0.818381 | 314 |
| ONGC | 15 | high | low | positive | -0.204767 | 0.204767 | -0.409534 | 1 |
| ONGC | 15 | high | mid | normal | 0.20378 | 1.02395 | -0.81787 | 306 |
| ONGC | 15 | low | high | normal | 0 | 0.81782 | 0.406549 | 398 |
| ONGC | 15 | low | low | normal | 0 | 0.412797 | 0 | 364 |
| ONGC | 15 | low | low | positive | 1.02629 | 1.02629 | 1.23155 | 1 |
| ONGC | 15 | low | mid | normal | 0 | 0.41301 | 1.15948e-12 | 397 |
| ONGC | 15 | mid | high | normal | -0.204482 | 1.02256 | 0 | 294 |
| ONGC | 15 | mid | low | normal | 0 | 0.817511 | 0 | 292 |
| ONGC | 15 | mid | mid | normal | 0 | 0.612126 | 0 | 296 |
| ONGC | 60 | high | high | normal | 0.101028 | 2.3567 | -1.0216 | 72 |
| ONGC | 60 | high | low | normal | 0.508787 | 2.45271 | -1.22021 | 78 |
| ONGC | 60 | high | mid | normal | -0.409249 | 2.04604 | -1.62242 | 67 |
| ONGC | 60 | low | high | normal | -0.203032 | 1.84015 | 0.818172 | 110 |
| ONGC | 60 | low | low | normal | 0 | 2.46442 | 0.408388 | 80 |
| ONGC | 60 | low | mid | normal | 0 | 1.74256 | 0.408914 | 104 |
| ONGC | 60 | mid | high | normal | 0 | 2.66448 | 0 | 63 |
| ONGC | 60 | mid | low | normal | -1.15726e-12 | 2.25101 | 0 | 87 |
| ONGC | 60 | mid | mid | normal | 0.409794 | 1.43161 | -0.408639 | 79 |
| RELIANCE | 1 | high | high | normal | 0 | 0 | 0 | 1512 |
| RELIANCE | 1 | high | high | positive | 0 | 0 | 0 | 104 |
| RELIANCE | 1 | high | low | normal | 0 | 0 | 0 | 2077 |
| RELIANCE | 1 | high | low | positive | 0 | 0 | 0 | 115 |
| RELIANCE | 1 | high | mid | normal | 0 | 0.383862 | 0 | 2110 |
| RELIANCE | 1 | high | mid | positive | 0 | 0 | 0 | 122 |
| RELIANCE | 1 | low | high | normal | 0 | 0 | 0 | 3696 |
| RELIANCE | 1 | low | high | positive | 0 | 0 | 0 | 189 |
| RELIANCE | 1 | low | low | normal | 0 | 0 | 0 | 3139 |
| RELIANCE | 1 | low | low | positive | 0 | 0 | 0 | 169 |
| RELIANCE | 1 | low | mid | normal | 0 | 0 | 0 | 3241 |
| RELIANCE | 1 | low | mid | positive | 0 | 0 | 0 | 208 |
| RELIANCE | 1 | mid | high | normal | 0 | 0 | 0 | 3233 |
| RELIANCE | 1 | mid | high | positive | 0 | 0 | 0 | 185 |
| RELIANCE | 1 | mid | low | normal | 0 | 0 | 0 | 3246 |
| RELIANCE | 1 | mid | low | positive | 0 | 0 | 0 | 173 |
| RELIANCE | 1 | mid | mid | normal | 0 | 0 | 0 | 3323 |
| RELIANCE | 1 | mid | mid | positive | 0 | 0 | 0 | 181 |
| RELIANCE | 5 | high | high | normal | 0 | 0.767342 | -0.767048 | 471 |
| RELIANCE | 5 | high | high | positive | 0 | 0.38844 | -0.38432 | 42 |
| RELIANCE | 5 | high | low | normal | 0 | 0.392603 | -0.768492 | 631 |
| RELIANCE | 5 | high | low | positive | 0 | 0.7756 | -0.778938 | 50 |
| RELIANCE | 5 | high | mid | normal | 0 | 0.391719 | -0.768802 | 610 |
| RELIANCE | 5 | high | mid | positive | 0 | 0.388455 | -0.768108 | 50 |
| RELIANCE | 5 | low | high | normal | 0 | 0.382892 | 0 | 1167 |
| RELIANCE | 5 | low | high | positive | 0 | 0.766812 | 1.75838e-12 | 92 |
| RELIANCE | 5 | low | low | normal | 0 | 0 | 0 | 1001 |
| RELIANCE | 5 | low | low | positive | 0 | 0.385602 | 0 | 78 |
| RELIANCE | 5 | low | mid | normal | 0 | 0 | 0 | 1013 |
| RELIANCE | 5 | low | mid | positive | 0 | 0.387342 | 0 | 95 |
| RELIANCE | 5 | mid | high | normal | 0 | 0.38786 | 0 | 994 |
| RELIANCE | 5 | mid | high | positive | 0 | 0.391206 | 0 | 81 |
| RELIANCE | 5 | mid | low | normal | 0 | 0.384349 | 0 | 1014 |
| RELIANCE | 5 | mid | low | positive | 0 | 0.387447 | 0 | 74 |
| RELIANCE | 5 | mid | mid | normal | 0 | 0.384578 | 0 | 1086 |
| RELIANCE | 5 | mid | mid | positive | 0 | 0.390442 | 0 | 81 |
| RELIANCE | 15 | high | high | normal | 0 | 1.16297 | -1.53286 | 181 |
| RELIANCE | 15 | high | low | normal | 0 | 1.16203 | -0.775735 | 245 |
| RELIANCE | 15 | high | mid | normal | -0.383818 | 1.17477 | -0.783423 | 233 |
| RELIANCE | 15 | low | high | normal | 0 | 0.77991 | 1.74768e-12 | 458 |
| RELIANCE | 15 | low | low | normal | 0 | 0.781556 | 1.74775e-12 | 402 |
| RELIANCE | 15 | low | mid | normal | 0 | 0.784437 | 0 | 402 |
| RELIANCE | 15 | mid | high | normal | 0 | 0.777696 | 0 | 332 |
| RELIANCE | 15 | mid | low | normal | 0 | 0.766195 | 0 | 325 |
| RELIANCE | 15 | mid | mid | normal | 0 | 0.774833 | 0 | 364 |
| RELIANCE | 60 | high | high | normal | 0 | 2.68879 | -0.777333 | 57 |
| RELIANCE | 60 | high | low | normal | 0.768315 | 2.33046 | -0.785022 | 79 |
| RELIANCE | 60 | high | mid | normal | -0.385719 | 2.11883 | -1.53374 | 72 |
| RELIANCE | 60 | low | high | normal | -0.384216 | 2.30317 | 0.766959 | 105 |
| RELIANCE | 60 | low | low | normal | 0 | 1.56746 | 0.765257 | 87 |
| RELIANCE | 60 | low | mid | normal | -0.76802 | 1.56709 | 1.74782e-12 | 100 |
| RELIANCE | 60 | mid | high | normal | -0.388794 | 1.93016 | 0 | 82 |
| RELIANCE | 60 | mid | low | normal | 0 | 1.93738 | 0 | 78 |
| RELIANCE | 60 | mid | mid | normal | 0.382438 | 2.71087 | 0 | 79 |
| SBIN | 1 | high | high | normal | 0 | 2.21855e-12 | 0 | 1314 |
| SBIN | 1 | high | high | positive | 0 | 0 | 0 | 86 |
| SBIN | 1 | high | low | normal | 0 | 0.481904 | 0 | 2241 |
| SBIN | 1 | high | low | positive | 0 | 0.481696 | 0 | 151 |
| SBIN | 1 | high | mid | normal | 0 | 0.480561 | 0 | 2038 |
| SBIN | 1 | high | mid | positive | 0 | 0.482672 | 0 | 114 |
| SBIN | 1 | low | high | normal | 0 | 0 | 0 | 3592 |
| SBIN | 1 | low | high | positive | 0 | 0 | 0 | 208 |
| SBIN | 1 | low | low | normal | 0 | 0 | 0 | 2710 |
| SBIN | 1 | low | low | positive | 0 | 0 | 0 | 144 |
| SBIN | 1 | low | mid | normal | 0 | 0 | 0 | 2938 |
| SBIN | 1 | low | mid | positive | 0 | 0 | 0 | 166 |
| SBIN | 1 | mid | high | normal | 0 | 0 | 0 | 3051 |
| SBIN | 1 | mid | high | positive | 0 | 0 | 0 | 174 |
| SBIN | 1 | mid | low | normal | 0 | 0 | 0 | 3010 |
| SBIN | 1 | mid | low | positive | 0 | 0 | 0 | 174 |
| SBIN | 1 | mid | mid | normal | 0 | 0 | 0 | 3244 |
| SBIN | 1 | mid | mid | positive | 0 | 0 | 0 | 182 |
| SBIN | 5 | high | high | normal | 0 | 0.492841 | -0.974421 | 436 |
| SBIN | 5 | high | high | positive | -0.481918 | 0.487829 | -0.481093 | 52 |
| SBIN | 5 | high | low | normal | 0 | 0.487995 | -0.971534 | 731 |
| SBIN | 5 | high | low | positive | 0 | 0.974089 | -0.974896 | 89 |
| SBIN | 5 | high | mid | normal | 0 | 0.488043 | -0.972101 | 629 |
| SBIN | 5 | high | mid | positive | 0 | 0.975895 | -0.974421 | 75 |
| SBIN | 5 | low | high | normal | 0 | 0.965298 | 0 | 1127 |
| SBIN | 5 | low | high | positive | 0 | 0.965065 | 2.19674e-12 | 122 |
| SBIN | 5 | low | low | normal | 0 | 0.492441 | 0 | 819 |
| SBIN | 5 | low | low | positive | 0 | 0.974279 | 0.961864 | 82 |
| SBIN | 5 | low | mid | normal | 0 | 0.958359 | 0 | 923 |
| SBIN | 5 | low | mid | positive | 0 | 0.974326 | 0.960661 | 83 |
| SBIN | 5 | mid | high | normal | 0 | 0.487662 | 0 | 1009 |
| SBIN | 5 | mid | high | positive | 0 | 0.487045 | 0 | 80 |
| SBIN | 5 | mid | low | normal | 0 | 0.487424 | 0 | 1021 |
| SBIN | 5 | mid | low | positive | -0.240419 | 0.488091 | -0.958543 | 84 |
| SBIN | 5 | mid | mid | normal | 0 | 0.487234 | 0 | 1095 |
| SBIN | 5 | mid | mid | positive | 0 | 0.487424 | 0 | 103 |
| SBIN | 15 | high | high | normal | 0 | 1.46356 | -0.977971 | 188 |
| SBIN | 15 | high | low | normal | 0 | 1.92623 | -0.974944 | 315 |
| SBIN | 15 | high | mid | normal | 0 | 1.4627 | -0.975372 | 257 |
| SBIN | 15 | low | high | normal | 0 | 1.46306 | 2.21709e-12 | 431 |
| SBIN | 15 | low | high | positive | -10000 | 10000 | -0.964925 | 1 |
| SBIN | 15 | low | low | normal | 0 | 1.44893 | 0.964739 | 307 |
| SBIN | 15 | low | mid | normal | 0 | 1.46177 | 2.19908e-12 | 357 |
| SBIN | 15 | mid | high | normal | 0 | 1.44865 | 0 | 352 |
| SBIN | 15 | mid | low | normal | 0 | 1.46042 | 0 | 350 |
| SBIN | 15 | mid | mid | normal | 0 | 0.975182 | 0 | 385 |
| SBIN | 60 | high | high | normal | -0.969665 | 2.43796 | -1.95308 | 36 |
| SBIN | 60 | high | low | normal | -0.979349 | 3.89428 | -1.92995 | 64 |
| SBIN | 60 | high | mid | normal | -0.486263 | 3.86063 | -1.94799 | 51 |
| SBIN | 60 | low | high | normal | 0 | 2.92298 | 0.965204 | 113 |
| SBIN | 60 | low | high | positive | -10000 | 10000 | -0.964925 | 1 |
| SBIN | 60 | low | low | normal | 0 | 2.90733 | 0.966698 | 78 |
| SBIN | 60 | low | mid | normal | 0 | 3.41314 | 0.482183 | 90 |
| SBIN | 60 | mid | high | normal | -2.21601e-12 | 3.41347 | 0 | 95 |
| SBIN | 60 | mid | low | normal | 0 | 2.90093 | 0 | 103 |
| SBIN | 60 | mid | mid | normal | -0.486239 | 2.92355 | 0 | 109 |
| SUNPHARMA | 1 | high | high | normal | 0 | 0.257559 | 0 | 1520 |
| SUNPHARMA | 1 | high | high | positive | 0 | 0 | 0 | 106 |
| SUNPHARMA | 1 | high | low | normal | 0 | 0 | 0 | 2207 |
| SUNPHARMA | 1 | high | low | positive | 0 | 0 | 0 | 158 |
| SUNPHARMA | 1 | high | mid | normal | 0 | 0.257526 | 0 | 2149 |
| SUNPHARMA | 1 | high | mid | positive | 0 | 0.258178 | 0 | 163 |
| SUNPHARMA | 1 | low | high | normal | 0 | 0 | 0 | 2436 |
| SUNPHARMA | 1 | low | high | positive | 0 | 0 | 0 | 140 |
| SUNPHARMA | 1 | low | low | normal | 0 | 0 | 0 | 2172 |
| SUNPHARMA | 1 | low | low | positive | 0 | 0 | 0 | 135 |
| SUNPHARMA | 1 | low | mid | normal | 0 | 0 | 0 | 2260 |
| SUNPHARMA | 1 | low | mid | positive | 0 | 0 | 0 | 116 |
| SUNPHARMA | 1 | mid | high | normal | 0 | 0 | 0 | 2435 |
| SUNPHARMA | 1 | mid | high | positive | 0 | 0 | 0 | 155 |
| SUNPHARMA | 1 | mid | low | normal | 0 | 0 | 0 | 1994 |
| SUNPHARMA | 1 | mid | low | positive | 0 | 0 | 0 | 129 |
| SUNPHARMA | 1 | mid | mid | normal | 0 | 0 | 0 | 2193 |
| SUNPHARMA | 1 | mid | mid | positive | 0 | 0 | 0 | 114 |
| SUNPHARMA | 5 | high | high | normal | 0 | 0.518068 | -0.516142 | 613 |
| SUNPHARMA | 5 | high | high | positive | 0 | 0.775174 | -1.03186 | 65 |
| SUNPHARMA | 5 | high | low | normal | 0 | 0.518538 | -0.516662 | 881 |
| SUNPHARMA | 5 | high | low | positive | 0 | 0.515849 | -0.516529 | 99 |
| SUNPHARMA | 5 | high | mid | normal | 0 | 0.517773 | -0.516569 | 887 |
| SUNPHARMA | 5 | high | mid | positive | -0.258104 | 0.772658 | -0.516462 | 89 |
| SUNPHARMA | 5 | low | high | normal | 0 | 0.258846 | 0 | 915 |
| SUNPHARMA | 5 | low | high | positive | 0 | 0.258833 | 5.85698e-13 | 78 |
| SUNPHARMA | 5 | low | low | normal | 0 | 0 | 0 | 851 |
| SUNPHARMA | 5 | low | low | positive | 0 | 0.515185 | 0 | 73 |
| SUNPHARMA | 5 | low | mid | normal | 0 | 0 | 0 | 875 |
| SUNPHARMA | 5 | low | mid | positive | 0 | 0.515916 | 0 | 74 |
| SUNPHARMA | 5 | mid | high | normal | 0 | 0.514933 | 0 | 1015 |
| SUNPHARMA | 5 | mid | high | positive | 0 | 0.515597 | 0 | 87 |
| SUNPHARMA | 5 | mid | low | normal | 0 | 0.264466 | 0 | 795 |
| SUNPHARMA | 5 | mid | low | positive | 0 | 0.772698 | 0 | 74 |
| SUNPHARMA | 5 | mid | mid | normal | 0 | 0.264999 | 0 | 862 |
| SUNPHARMA | 5 | mid | mid | positive | 0 | 0.515159 | 0 | 69 |
| SUNPHARMA | 15 | high | high | normal | 0 | 1.29219 | -1.03386 | 228 |
| SUNPHARMA | 15 | high | high | positive | 0.129022 | 1.54727 | -0.516516 | 8 |
| SUNPHARMA | 15 | high | low | normal | 0.262331 | 1.29169 | -1.03295 | 324 |
| SUNPHARMA | 15 | high | low | positive | 1.808 | 1.808 | -1.54985 | 4 |
| SUNPHARMA | 15 | high | mid | normal | 0 | 1.28961 | -1.03616 | 316 |
| SUNPHARMA | 15 | high | mid | positive | -0.902156 | 1.29177 | -0.774733 | 16 |
| SUNPHARMA | 15 | low | high | normal | 0 | 0.53111 | 0.514946 | 335 |
| SUNPHARMA | 15 | low | high | positive | 0 | 0.644779 | 0 | 18 |
| SUNPHARMA | 15 | low | low | normal | 0 | 0.528919 | 1.17448e-12 | 333 |
| SUNPHARMA | 15 | low | low | positive | 0 | 0.772817 | 0.516649 | 5 |
| SUNPHARMA | 15 | low | mid | normal | 0 | 0.774453 | 1.17703e-12 | 335 |
| SUNPHARMA | 15 | low | mid | positive | 0 | 0.515929 | 1.1726e-12 | 13 |
| SUNPHARMA | 15 | mid | high | normal | -0.257566 | 1.03517 | -1.20546e-12 | 369 |
| SUNPHARMA | 15 | mid | high | positive | -0.258151 | 1.41656 | -0.515119 | 14 |
| SUNPHARMA | 15 | mid | low | normal | 0 | 1.03324 | 0 | 299 |
| SUNPHARMA | 15 | mid | low | positive | 0 | 1.55019 | 0 | 7 |
| SUNPHARMA | 15 | mid | mid | normal | 0.25737 | 1.29141 | 0 | 312 |
| SUNPHARMA | 15 | mid | mid | positive | 1.8031 | 1.8031 | -0.515172 | 7 |
| SUNPHARMA | 60 | high | high | normal | -0.386997 | 2.58042 | -1.03295 | 60 |
| SUNPHARMA | 60 | high | low | normal | 0.904635 | 2.06572 | -1.54931 | 74 |
| SUNPHARMA | 60 | high | low | positive | -1.29192 | 1.29192 | -1.55031 | 1 |
| SUNPHARMA | 60 | high | mid | normal | -0.129199 | 2.57431 | -1.30379 | 76 |
| SUNPHARMA | 60 | high | mid | positive | -4999.23 | 5000.77 | -6.21041 | 2 |
| SUNPHARMA | 60 | low | high | normal | -0.38699 | 2.45389 | 0.517411 | 84 |
| SUNPHARMA | 60 | low | high | positive | 3.09685 | 3.09685 | 0 | 1 |
| SUNPHARMA | 60 | low | low | normal | 0 | 2.06265 | 0.515637 | 83 |
| SUNPHARMA | 60 | low | low | positive | 5.67347 | 5.67347 | -1.17272e-12 | 1 |
| SUNPHARMA | 60 | low | mid | normal | 0.514655 | 1.82642 | 0.51573 | 84 |
| SUNPHARMA | 60 | low | mid | positive | 1.03037 | 1.03037 | 1.03037 | 3 |
| SUNPHARMA | 60 | mid | high | normal | 0.261604 | 2.3204 | -1.17621e-12 | 98 |
| SUNPHARMA | 60 | mid | high | positive | 0.772575 | 2.0605 | 1.03018 | 2 |
| SUNPHARMA | 60 | mid | low | normal | 0 | 1.8146 | 0 | 85 |
| SUNPHARMA | 60 | mid | low | positive | 3.86558 | 3.86558 | -0.515411 | 1 |
| SUNPHARMA | 60 | mid | mid | normal | 0.773994 | 3.10752 | -1.17097e-12 | 85 |
| TCS | 1 | high | high | normal | 0 | 0.24335 | 0 | 1835 |
| TCS | 1 | high | high | positive | 0 | 0.47463 | -0.474572 | 148 |
| TCS | 1 | high | low | normal | 0 | 0.243558 | 0 | 2636 |
| TCS | 1 | high | low | positive | 0 | 0.243938 | -0.471642 | 203 |
| TCS | 1 | high | mid | normal | 0 | 0.242521 | 0 | 2450 |
| TCS | 1 | high | mid | positive | 0 | 0.241388 | 0 | 227 |
| TCS | 1 | low | high | normal | 0 | 0 | 0 | 3570 |
| TCS | 1 | low | high | positive | 0 | 0 | 0 | 314 |
| TCS | 1 | low | low | normal | 0 | 0 | 0 | 2972 |
| TCS | 1 | low | low | positive | 0 | 0 | 0 | 276 |
| TCS | 1 | low | mid | normal | 0 | 0 | 0 | 3268 |
| TCS | 1 | low | mid | positive | 0 | 0 | 0 | 298 |
| TCS | 1 | mid | high | normal | 0 | 0.240883 | 0 | 3146 |
| TCS | 1 | mid | high | positive | 0 | 0.241179 | 0 | 271 |
| TCS | 1 | mid | low | normal | 0 | 0.240929 | 0 | 2944 |
| TCS | 1 | mid | low | positive | 0 | 0.241179 | 0 | 253 |
| TCS | 1 | mid | mid | normal | 0 | 0.24101 | 0 | 3047 |
| TCS | 1 | mid | mid | positive | 0 | 0.240955 | 0 | 274 |
| TCS | 5 | high | high | normal | 0 | 0.965146 | -0.487972 | 530 |
| TCS | 5 | high | high | positive | 0 | 1.20928 | -0.963182 | 73 |
| TCS | 5 | high | low | normal | 0 | 0.73278 | -0.961955 | 787 |
| TCS | 5 | high | low | positive | 0 | 0.731765 | -0.969139 | 112 |
| TCS | 5 | high | mid | normal | 0 | 0.959877 | -0.958199 | 681 |
| TCS | 5 | high | mid | positive | 0 | 0.962117 | -0.963182 | 139 |
| TCS | 5 | low | high | normal | 0 | 0.721102 | 2.21566e-12 | 978 |
| TCS | 5 | low | high | positive | 0 | 0.488055 | 0.480989 | 197 |
| TCS | 5 | low | low | normal | 0 | 0.723423 | 2.21879e-12 | 852 |
| TCS | 5 | low | low | positive | 0 | 0.724253 | 0.48266 | 154 |
| TCS | 5 | low | mid | normal | 0 | 0.719943 | 2.18965e-12 | 898 |
| TCS | 5 | low | mid | positive | 0 | 0.605478 | 2.21534e-12 | 186 |
| TCS | 5 | mid | high | normal | 0 | 0.718838 | 0 | 908 |
| TCS | 5 | mid | high | positive | 0 | 0.721987 | 0 | 173 |
| TCS | 5 | mid | low | normal | 0 | 0.722578 | 0 | 819 |
| TCS | 5 | mid | low | positive | 0 | 0.972976 | 0 | 135 |
| TCS | 5 | mid | mid | normal | 0 | 0.721076 | 0 | 888 |
| TCS | 5 | mid | mid | positive | 0 | 0.731654 | -0.480077 | 152 |
| TCS | 15 | high | high | normal | -0.239521 | 2.15745 | -1.4394 | 209 |
| TCS | 15 | high | low | normal | 0 | 1.9246 | -0.978318 | 288 |
| TCS | 15 | high | low | positive | -0.487211 | 0.487211 | 0 | 1 |
| TCS | 15 | high | mid | normal | 0 | 1.9198 | -1.45089 | 277 |
| TCS | 15 | high | mid | positive | 0.976181 | 0.976181 | -0.976181 | 1 |
| TCS | 15 | low | high | normal | -0.240512 | 1.4451 | 0.483664 | 420 |
| TCS | 15 | low | low | normal | 0.240538 | 1.68829 | 0.485696 | 356 |
| TCS | 15 | low | low | positive | -0.729232 | 1.46108 | 1.94753 | 2 |
| TCS | 15 | low | mid | normal | 0 | 1.6818 | 0.48308 | 375 |
| TCS | 15 | low | mid | positive | 4.13938 | 4.13938 | 2.43493 | 1 |
| TCS | 15 | mid | high | normal | 0 | 1.69426 | 0 | 339 |
| TCS | 15 | mid | high | positive | 0.244481 | 0.963066 | -2.18976e-12 | 3 |
| TCS | 15 | mid | low | normal | -0.24351 | 1.68913 | 0 | 324 |
| TCS | 15 | mid | low | positive | -0.730834 | 0.730834 | -0.487223 | 1 |
| TCS | 15 | mid | mid | normal | 0 | 1.70719 | -0.48085 | 343 |
| TCS | 15 | mid | mid | positive | 3.41112 | 3.41112 | 0.48847 | 2 |
| TCS | 60 | high | high | normal | -1.21172 | 4.20569 | -1.46265 | 56 |
| TCS | 60 | high | low | normal | 0.484161 | 3.88291 | -0.977601 | 70 |
| TCS | 60 | high | mid | normal | 0 | 3.40931 | -1.44477 | 73 |
| TCS | 60 | low | high | normal | -1.4498 | 3.60707 | 0.482614 | 107 |
| TCS | 60 | low | low | normal | -0.729676 | 3.6281 | 0.4866 | 92 |
| TCS | 60 | low | mid | normal | 0.724848 | 2.92006 | 0.487294 | 89 |
| TCS | 60 | mid | high | normal | 0.962603 | 3.14488 | 0 | 81 |
| TCS | 60 | mid | low | normal | 0.361665 | 3.38969 | 0 | 82 |
| TCS | 60 | mid | mid | normal | 0 | 2.91992 | -2.19663e-12 | 89 |
| TECHM | 1 | high | high | normal | 0 | 0.344009 | 0 | 862 |
| TECHM | 1 | high | high | positive | 0 | 0.344258 | 0 | 135 |
| TECHM | 1 | high | low | normal | 0 | 0.343909 | 0 | 1574 |
| TECHM | 1 | high | low | positive | 0 | 0 | 0 | 167 |
| TECHM | 1 | high | mid | normal | 0 | 0.341361 | 0 | 1412 |
| TECHM | 1 | high | mid | positive | 0 | 0.34323 | 0 | 165 |
| TECHM | 1 | low | high | normal | 0 | 0 | 0 | 2425 |
| TECHM | 1 | low | high | positive | 0 | 0 | 0 | 337 |
| TECHM | 1 | low | low | normal | 0 | 0 | 0 | 1799 |
| TECHM | 1 | low | low | positive | 0 | 0 | 0 | 197 |
| TECHM | 1 | low | mid | normal | 0 | 0 | 0 | 1972 |
| TECHM | 1 | low | mid | positive | 0 | 0 | 0 | 242 |
| TECHM | 1 | mid | high | normal | 0 | 0 | 0 | 1711 |
| TECHM | 1 | mid | high | positive | 0 | 0 | 0 | 233 |
| TECHM | 1 | mid | low | normal | 0 | 0 | 0 | 1722 |
| TECHM | 1 | mid | low | positive | 0 | 0 | 0 | 246 |
| TECHM | 1 | mid | mid | normal | 0 | 0 | 0 | 1831 |
| TECHM | 1 | mid | mid | positive | 0 | 0 | 0 | 252 |
| TECHM | 5 | high | high | normal | 0 | 0.689037 | -0.688942 | 483 |
| TECHM | 5 | high | high | positive | 0.344151 | 0.85916 | -0.701732 | 68 |
| TECHM | 5 | high | low | normal | 0 | 0.695701 | -0.690703 | 815 |
| TECHM | 5 | high | low | positive | 0.17175 | 1.03988 | -0.69973 | 122 |
| TECHM | 5 | high | mid | normal | 0 | 0.690429 | -0.68918 | 740 |
| TECHM | 5 | high | mid | positive | 0 | 1.01843 | -0.698983 | 113 |
| TECHM | 5 | low | high | normal | 0 | 0.349363 | 0 | 1176 |
| TECHM | 5 | low | high | positive | 0 | 0.344424 | 0 | 159 |
| TECHM | 5 | low | low | normal | 0 | 0.349601 | 0 | 877 |
| TECHM | 5 | low | low | positive | 0 | 0.688824 | 0 | 109 |
| TECHM | 5 | low | mid | normal | 0 | 0.349223 | 0 | 948 |
| TECHM | 5 | low | mid | positive | 0 | 0.698519 | 7.81487e-13 | 138 |
| TECHM | 5 | mid | high | normal | 0 | 0.349601 | 0 | 728 |
| TECHM | 5 | mid | high | positive | 0 | 0.344459 | 0 | 99 |
| TECHM | 5 | mid | low | normal | 0 | 0.349589 | 0 | 667 |
| TECHM | 5 | mid | low | positive | 0 | 0.3503 | 0 | 125 |
| TECHM | 5 | mid | mid | normal | 0 | 0.349528 | 0 | 744 |
| TECHM | 5 | mid | mid | positive | 0 | 0.349308 | 0 | 109 |
| TECHM | 15 | high | high | normal | 0 | 1.39767 | -1.37687 | 152 |
| TECHM | 15 | high | high | positive | 0.527204 | 2.10003 | -1.03558 | 10 |
| TECHM | 15 | high | low | normal | 0 | 1.39533 | -1.37765 | 279 |
| TECHM | 15 | high | low | positive | -1.02944 | 6.19941 | 0 | 3 |
| TECHM | 15 | high | mid | normal | 0.344299 | 1.3938 | -1.37867 | 242 |
| TECHM | 15 | high | mid | positive | 1.89187 | 10.5146 | 1.72398 | 2 |
| TECHM | 15 | low | high | normal | 0 | 1.04774 | 0.6879 | 457 |
| TECHM | 15 | low | high | positive | 1.04752 | 1.72153 | 0.698348 | 11 |
| TECHM | 15 | low | low | normal | 0 | 1.37452 | 0.689014 | 327 |
| TECHM | 15 | low | low | positive | -0.183574 | 1.92114 | 1.71879 | 4 |
| TECHM | 15 | low | mid | normal | 0 | 1.04882 | 0.688587 | 386 |
| TECHM | 15 | low | mid | positive | 0.351568 | 0.700501 | 2.09629 | 9 |
| TECHM | 15 | mid | high | normal | 0 | 1.21437 | 0 | 330 |
| TECHM | 15 | mid | high | positive | 0 | 0.349412 | -7.8012e-13 | 12 |
| TECHM | 15 | mid | low | normal | 0 | 1.05038 | 0 | 353 |
| TECHM | 15 | mid | low | positive | -0.174795 | 3.13173 | -0.692619 | 6 |
| TECHM | 15 | mid | mid | normal | 0 | 1.37542 | 0 | 346 |
| TECHM | 15 | mid | mid | positive | -1.03292 | 2.41941 | -7.81245e-13 | 14 |
| TECHM | 60 | high | high | normal | 0.172301 | 3.81218 | -1.39871 | 34 |
| TECHM | 60 | high | low | normal | 0.688587 | 3.49479 | -1.39611 | 71 |
| TECHM | 60 | high | low | positive | 6.42499 | 6.42499 | -0.361265 | 2 |
| TECHM | 60 | high | mid | normal | 0.70109 | 3.45399 | -1.3816 | 57 |
| TECHM | 60 | high | mid | positive | 19.2503 | 19.2503 | 6.30009 | 1 |
| TECHM | 60 | low | high | normal | -0.687592 | 3.10013 | 0.698836 | 115 |
| TECHM | 60 | low | high | positive | 4.92178 | 4.92178 | 0 | 1 |
| TECHM | 60 | low | low | normal | 0.348913 | 2.75321 | 0.699203 | 78 |
| TECHM | 60 | low | low | positive | 2.10844 | 2.10844 | -1.40563 | 1 |
| TECHM | 60 | low | mid | normal | 0 | 3.09215 | 0.700476 | 99 |
| TECHM | 60 | mid | high | normal | -0.350238 | 3.09992 | -0.687616 | 93 |
| TECHM | 60 | mid | high | positive | -1.22309 | 1.22309 | -1.7471 | 2 |
| TECHM | 60 | mid | low | normal | 0 | 3.14103 | 0 | 93 |
| TECHM | 60 | mid | mid | normal | -0.346862 | 2.75587 | -0.687829 | 92 |
| TECHM | 60 | mid | mid | positive | -1.02927 | 1.02927 | 0.686177 | 1 |
| ULTRACEMCO | 1 | high | high | normal | 0 | 0 | 0 | 778 |
| ULTRACEMCO | 1 | high | high | positive | 0 | 0 | 0 | 83 |
| ULTRACEMCO | 1 | high | low | normal | 0 | 0 | 0 | 1277 |
| ULTRACEMCO | 1 | high | low | positive | 0 | 0 | 0 | 168 |
| ULTRACEMCO | 1 | high | mid | normal | 0 | 0 | 0 | 1158 |
| ULTRACEMCO | 1 | high | mid | positive | 0 | 0 | 0 | 143 |
| ULTRACEMCO | 1 | low | high | normal | 0 | 0 | 0 | 2020 |
| ULTRACEMCO | 1 | low | high | positive | 0 | 0 | 0 | 240 |
| ULTRACEMCO | 1 | low | low | normal | 0 | 0 | 0 | 1428 |
| ULTRACEMCO | 1 | low | low | positive | 0 | 0 | 0 | 177 |
| ULTRACEMCO | 1 | low | mid | normal | 0 | 0 | 0 | 1619 |
| ULTRACEMCO | 1 | low | mid | positive | 0 | 0 | 0 | 182 |
| ULTRACEMCO | 1 | mid | high | normal | 0 | 0 | 0 | 1253 |
| ULTRACEMCO | 1 | mid | high | positive | 0 | 0 | 0 | 94 |
| ULTRACEMCO | 1 | mid | low | normal | 0 | 0 | 0 | 1324 |
| ULTRACEMCO | 1 | mid | low | positive | 0 | 0 | 0 | 104 |
| ULTRACEMCO | 1 | mid | mid | normal | 0 | 0 | 0 | 1398 |
| ULTRACEMCO | 1 | mid | mid | positive | 0 | 0 | 0 | 101 |
| ULTRACEMCO | 5 | high | high | normal | 0 | 0.432283 | 0 | 439 |
| ULTRACEMCO | 5 | high | high | positive | 0 | 0.427917 | 0 | 46 |
| ULTRACEMCO | 5 | high | low | normal | 0 | 0.428137 | 0 | 771 |
| ULTRACEMCO | 5 | high | low | positive | 0 | 0.428293 | 0 | 90 |
| ULTRACEMCO | 5 | high | mid | normal | 0 | 0.428082 | 0 | 657 |
| ULTRACEMCO | 5 | high | mid | positive | 0 | 0.427817 | 0 | 84 |
| ULTRACEMCO | 5 | low | high | normal | 0 | 0 | 0 | 1237 |
| ULTRACEMCO | 5 | low | high | positive | 0 | 0 | 0 | 139 |
| ULTRACEMCO | 5 | low | low | normal | 0 | 0 | 0 | 853 |
| ULTRACEMCO | 5 | low | low | positive | 0 | 0 | 0 | 100 |
| ULTRACEMCO | 5 | low | mid | normal | 0 | 0 | 0 | 1000 |
| ULTRACEMCO | 5 | low | mid | positive | 0 | 0 | 0 | 108 |
| ULTRACEMCO | 5 | mid | high | normal | 0 | 0.428156 | 0 | 713 |
| ULTRACEMCO | 5 | mid | high | positive | 0 | 0 | 0 | 51 |
| ULTRACEMCO | 5 | mid | low | normal | 0 | 0 | 0 | 765 |
| ULTRACEMCO | 5 | mid | low | positive | 0 | 0 | 0 | 50 |
| ULTRACEMCO | 5 | mid | mid | normal | 0 | 0 | 0 | 792 |
| ULTRACEMCO | 5 | mid | mid | positive | 0 | 0.427917 | 0 | 58 |
| ULTRACEMCO | 15 | high | high | normal | -0.427771 | 0.879237 | -0.857082 | 177 |
| ULTRACEMCO | 15 | high | high | positive | -2.14069 | 2.14069 | -0.855615 | 3 |
| ULTRACEMCO | 15 | high | low | normal | 0 | 0.864958 | -0.856806 | 314 |
| ULTRACEMCO | 15 | high | low | positive | 0 | 0.85918 | -1.71299 | 5 |
| ULTRACEMCO | 15 | high | mid | normal | 0 | 0.857155 | -0.856935 | 267 |
| ULTRACEMCO | 15 | high | mid | positive | 0 | 0 | 0 | 2 |
| ULTRACEMCO | 15 | low | high | normal | 0 | 0.429424 | 0 | 499 |
| ULTRACEMCO | 15 | low | high | positive | -0.214124 | 0.642406 | 0.428247 | 8 |
| ULTRACEMCO | 15 | low | low | normal | 0 | 0.432601 | 0 | 359 |
| ULTRACEMCO | 15 | low | low | positive | 0 | 0.428211 | 0.856421 | 3 |
| ULTRACEMCO | 15 | low | mid | normal | 0 | 0.432507 | 0 | 428 |
| ULTRACEMCO | 15 | low | mid | positive | -0.213602 | 0.64141 | 0 | 4 |
| ULTRACEMCO | 15 | mid | high | normal | 0 | 0.856164 | 0 | 283 |
| ULTRACEMCO | 15 | mid | high | positive | 0 | 0 | 0 | 1 |
| ULTRACEMCO | 15 | mid | low | normal | 0 | 0.854226 | 0 | 288 |
| ULTRACEMCO | 15 | mid | low | positive | 0 | 0.426913 | 0.853825 | 3 |
| ULTRACEMCO | 15 | mid | mid | normal | 0 | 0.433802 | 0 | 297 |
| ULTRACEMCO | 15 | mid | mid | positive | -0.856678 | 0.856678 | 0 | 1 |
| ULTRACEMCO | 60 | high | high | normal | -0.427004 | 2.13922 | -0.867566 | 45 |
| ULTRACEMCO | 60 | high | low | normal | -0.427881 | 2.16892 | -0.864641 | 77 |
| ULTRACEMCO | 60 | high | mid | normal | -0.429406 | 2.13904 | -0.865127 | 73 |
| ULTRACEMCO | 60 | low | high | normal | 0.427241 | 1.73604 | 0.854482 | 125 |
| ULTRACEMCO | 60 | low | low | normal | 0 | 1.73078 | 0.856494 | 107 |
| ULTRACEMCO | 60 | low | mid | normal | 0 | 1.29988 | 0.86408 | 95 |
| ULTRACEMCO | 60 | mid | high | normal | 0 | 1.76546 | -0.855578 | 75 |
| ULTRACEMCO | 60 | mid | low | normal | -0.428156 | 2.16844 | -0.85419 | 61 |
| ULTRACEMCO | 60 | mid | mid | normal | -0.427954 | 2.15233 | 0 | 82 |
| WIPRO | 1 | high | high | normal | 0 | 0 | 0 | 1426 |
| WIPRO | 1 | high | high | positive | 0 | 0 | 0 | 272 |
| WIPRO | 1 | high | low | normal | 0 | 0 | 0 | 1570 |
| WIPRO | 1 | high | low | positive | 0 | 0 | 0 | 316 |
| WIPRO | 1 | high | mid | normal | 0 | 0 | 0 | 1604 |
| WIPRO | 1 | high | mid | positive | 0 | 0 | 0 | 363 |
| WIPRO | 1 | low | high | normal | 0 | 0 | 0 | 2047 |
| WIPRO | 1 | low | high | positive | 0 | 0 | 0 | 320 |
| WIPRO | 1 | low | low | normal | 0 | 0 | 0 | 1913 |
| WIPRO | 1 | low | low | positive | 0 | 0 | 0 | 336 |
| WIPRO | 1 | low | mid | normal | 0 | 0 | 0 | 1931 |
| WIPRO | 1 | low | mid | positive | 0 | 0 | 0 | 340 |
| WIPRO | 1 | mid | high | normal | 0 | 0 | 0 | 1755 |
| WIPRO | 1 | mid | high | positive | 0 | 0 | 0 | 307 |
| WIPRO | 1 | mid | low | normal | 0 | 0 | 0 | 1670 |
| WIPRO | 1 | mid | low | positive | 0 | 0 | 0 | 324 |
| WIPRO | 1 | mid | mid | normal | 0 | 0 | 0 | 1764 |
| WIPRO | 1 | mid | mid | positive | 0 | 0 | 0 | 312 |
| WIPRO | 5 | high | high | normal | 0 | 0.567215 | -0.568715 | 667 |
| WIPRO | 5 | high | high | positive | 0 | 0.288155 | -0.57496 | 124 |
| WIPRO | 5 | high | low | normal | 0 | 0.568634 | -0.568893 | 721 |
| WIPRO | 5 | high | low | positive | 0 | 0.570207 | -0.570174 | 163 |
| WIPRO | 5 | high | mid | normal | 0 | 0.568037 | -0.56823 | 753 |
| WIPRO | 5 | high | mid | positive | 0 | 0.569687 | -0.575954 | 144 |
| WIPRO | 5 | low | high | normal | 0 | 0.288077 | 0 | 885 |
| WIPRO | 5 | low | high | positive | 0 | 0.568634 | 1.61864e-12 | 165 |
| WIPRO | 5 | low | low | normal | 0 | 0.287969 | 0 | 817 |
| WIPRO | 5 | low | low | positive | 0 | 0.572565 | 0.568279 | 154 |
| WIPRO | 5 | low | mid | normal | 0 | 0.284904 | 0 | 854 |
| WIPRO | 5 | low | mid | positive | 0 | 0.575556 | 1.61712e-12 | 147 |
| WIPRO | 5 | mid | high | normal | 0 | 0.285837 | 0 | 773 |
| WIPRO | 5 | mid | high | positive | 0 | 0.568359 | 0 | 137 |
| WIPRO | 5 | mid | low | normal | 0 | 0.568141 | 0 | 746 |
| WIPRO | 5 | mid | low | positive | 0 | 0.287944 | 0 | 151 |
| WIPRO | 5 | mid | mid | normal | 0 | 0.288052 | 0 | 810 |
| WIPRO | 5 | mid | mid | positive | 0 | 0.569128 | 0 | 126 |
| WIPRO | 15 | high | high | normal | 0 | 1.13717 | -0.575159 | 254 |
| WIPRO | 15 | high | high | positive | 0 | 1.15032 | -1.15224 | 23 |
| WIPRO | 15 | high | low | normal | 0 | 1.13633 | -1.13699 | 286 |
| WIPRO | 15 | high | low | positive | -0.286372 | 0.858334 | -1.13937 | 30 |
| WIPRO | 15 | high | mid | normal | -0.284487 | 1.13871 | -1.13611 | 278 |
| WIPRO | 15 | high | mid | positive | -0.142163 | 0.858194 | -0.576618 | 42 |
| WIPRO | 15 | low | high | normal | 0 | 0.863869 | 0.575929 | 348 |
| WIPRO | 15 | low | high | positive | 0 | 1.13816 | 0.574986 | 28 |
| WIPRO | 15 | low | low | normal | 0 | 0.863682 | 0.569736 | 319 |
| WIPRO | 15 | low | low | positive | 0.432094 | 1.4398 | 1.43762 | 22 |
| WIPRO | 15 | low | mid | normal | 0 | 0.855456 | 0.571119 | 323 |
| WIPRO | 15 | low | mid | positive | 0.568844 | 1.15151 | 1.15294 | 25 |
| WIPRO | 15 | mid | high | normal | -8.09851e-13 | 1.13772 | 0 | 296 |
| WIPRO | 15 | mid | high | positive | -0.284366 | 0.853048 | 0 | 23 |
| WIPRO | 15 | mid | low | normal | 0 | 1.1397 | 0 | 291 |
| WIPRO | 15 | mid | low | positive | -0.28777 | 1.29397 | -8.17891e-13 | 24 |
| WIPRO | 15 | mid | mid | normal | 0 | 1.15022 | 0 | 307 |
| WIPRO | 15 | mid | mid | positive | -0.142462 | 1.14581 | 0 | 24 |
| WIPRO | 60 | high | high | normal | 0 | 2.00143 | -1.13749 | 61 |
| WIPRO | 60 | high | high | positive | 1.73055 | 1.73055 | -1.15058 | 5 |
| WIPRO | 60 | high | low | normal | -0.56993 | 1.72811 | -1.13986 | 76 |
| WIPRO | 60 | high | low | positive | -1.15121 | 1.72642 | -1.13931 | 7 |
| WIPRO | 60 | high | mid | normal | -0.287724 | 2.73786 | -1.14193 | 76 |
| WIPRO | 60 | high | mid | positive | -0.00190385 | 2.73671 | -1.43879 | 10 |
| WIPRO | 60 | low | high | normal | 0.284485 | 2.00931 | 0.578838 | 96 |
| WIPRO | 60 | low | high | positive | -1.58648 | 1.58648 | 0.288201 | 2 |
| WIPRO | 60 | low | low | normal | 0 | 2.30934 | 0.57872 | 87 |
| WIPRO | 60 | low | low | positive | -1.99096 | 4.88393 | 0.576984 | 7 |
| WIPRO | 60 | low | mid | normal | 0 | 1.44718 | 0.571854 | 90 |
| WIPRO | 60 | low | mid | positive | 0 | 1.99033 | 1.15105 | 5 |
| WIPRO | 60 | mid | high | normal | -0.854603 | 2.30448 | 0 | 77 |
| WIPRO | 60 | mid | high | positive | 3.15184 | 3.15184 | 0.572408 | 4 |
| WIPRO | 60 | mid | low | normal | 0 | 1.99407 | -0.567972 | 61 |
| WIPRO | 60 | mid | low | positive | 0.288243 | 1.72946 | 0.576485 | 7 |
| WIPRO | 60 | mid | mid | normal | 0 | 2.86442 | 0 | 66 |
| WIPRO | 60 | mid | mid | positive | -0.575755 | 4.03505 | 1.15151 | 3 |

## Label Partition Inventory

| horizon_sec | trade_date | exchange | symbol | split_role | rows | event_surprise_rows | label_file | bytes | test_rows_used |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-07-08 | NSE | ADANIPORTS | train | 3617 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ADANIPORTS\event_surprise_conditional_labels.parquet | 37070 | 0 |
| 1 | 2026-07-08 | NSE | AXISBANK | train | 5829 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=AXISBANK\event_surprise_conditional_labels.parquet | 54916 | 0 |
| 1 | 2026-07-08 | NSE | BAJAJ-AUTO | train | 3323 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=BAJAJ-AUTO\event_surprise_conditional_labels.parquet | 35267 | 0 |
| 1 | 2026-07-08 | NSE | BANKBEES | train | 5645 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=BANKBEES\event_surprise_conditional_labels.parquet | 52859 | 0 |
| 1 | 2026-07-08 | NSE | BHARTIARTL | train | 3952 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=BHARTIARTL\event_surprise_conditional_labels.parquet | 39963 | 0 |
| 1 | 2026-07-08 | NSE | BPCL | train | 2852 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=BPCL\event_surprise_conditional_labels.parquet | 31216 | 0 |
| 1 | 2026-07-08 | NSE | BRITANNIA | train | 2151 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=BRITANNIA\event_surprise_conditional_labels.parquet | 26412 | 0 |
| 1 | 2026-07-08 | NSE | CIPLA | train | 2953 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=CIPLA\event_surprise_conditional_labels.parquet | 32544 | 0 |
| 1 | 2026-07-08 | NSE | DRREDDY | train | 2935 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=DRREDDY\event_surprise_conditional_labels.parquet | 32330 | 0 |
| 1 | 2026-07-08 | NSE | GOLDBEES | train | 4078 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=GOLDBEES\event_surprise_conditional_labels.parquet | 40577 | 0 |
| 1 | 2026-07-08 | NSE | HCLTECH | train | 2706 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=HCLTECH\event_surprise_conditional_labels.parquet | 30641 | 0 |
| 1 | 2026-07-08 | NSE | HDFCBANK | train | 6816 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=HDFCBANK\event_surprise_conditional_labels.parquet | 62288 | 0 |
| 1 | 2026-07-08 | NSE | HINDUNILVR | train | 3470 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=HINDUNILVR\event_surprise_conditional_labels.parquet | 36410 | 0 |
| 1 | 2026-07-08 | NSE | ICICIBANK | train | 6210 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ICICIBANK\event_surprise_conditional_labels.parquet | 57684 | 0 |
| 1 | 2026-07-08 | NSE | INFY | train | 5152 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=INFY\event_surprise_conditional_labels.parquet | 49651 | 0 |
| 1 | 2026-07-08 | NSE | ITBEES | train | 2355 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ITBEES\event_surprise_conditional_labels.parquet | 26610 | 0 |
| 1 | 2026-07-08 | NSE | ITC | train | 4271 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ITC\event_surprise_conditional_labels.parquet | 42774 | 0 |
| 1 | 2026-07-08 | NSE | JUNIORBEES | train | 5241 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=JUNIORBEES\event_surprise_conditional_labels.parquet | 49945 | 0 |
| 1 | 2026-07-08 | NSE | KOTAKBANK | train | 4944 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=KOTAKBANK\event_surprise_conditional_labels.parquet | 47874 | 0 |
| 1 | 2026-07-08 | NSE | LT | train | 6328 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=LT\event_surprise_conditional_labels.parquet | 58567 | 0 |
| 1 | 2026-07-08 | NSE | M&M | train | 6037 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=M&M\event_surprise_conditional_labels.parquet | 56393 | 0 |
| 1 | 2026-07-08 | NSE | MARUTI | train | 4917 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=MARUTI\event_surprise_conditional_labels.parquet | 47843 | 0 |
| 1 | 2026-07-08 | NSE | NESTLEIND | train | 2943 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=NESTLEIND\event_surprise_conditional_labels.parquet | 32322 | 0 |
| 1 | 2026-07-08 | NSE | NIFTYBEES | train | 5016 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=NIFTYBEES\event_surprise_conditional_labels.parquet | 48143 | 0 |
| 1 | 2026-07-08 | NSE | ONGC | train | 4121 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ONGC\event_surprise_conditional_labels.parquet | 41650 | 0 |
| 1 | 2026-07-08 | NSE | RELIANCE | train | 6547 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=RELIANCE\event_surprise_conditional_labels.parquet | 60070 | 0 |
| 1 | 2026-07-08 | NSE | SBIN | train | 5499 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=SBIN\event_surprise_conditional_labels.parquet | 52281 | 0 |
| 1 | 2026-07-08 | NSE | SUNPHARMA | train | 3352 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=SUNPHARMA\event_surprise_conditional_labels.parquet | 35470 | 0 |
| 1 | 2026-07-08 | NSE | TCS | train | 3904 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=TCS\event_surprise_conditional_labels.parquet | 39663 | 0 |
| 1 | 2026-07-08 | NSE | TECHM | train | 2802 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=TECHM\event_surprise_conditional_labels.parquet | 31361 | 0 |
| 1 | 2026-07-08 | NSE | ULTRACEMCO | train | 3043 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ULTRACEMCO\event_surprise_conditional_labels.parquet | 33200 | 0 |
| 1 | 2026-07-08 | NSE | WIPRO | train | 2625 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=WIPRO\event_surprise_conditional_labels.parquet | 30037 | 0 |
| 1 | 2026-07-09 | NSE | ADANIPORTS | train | 5553 | 509 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ADANIPORTS\event_surprise_conditional_labels.parquet | 56075 | 0 |
| 1 | 2026-07-09 | NSE | AXISBANK | train | 7446 | 529 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=AXISBANK\event_surprise_conditional_labels.parquet | 70396 | 0 |
| 1 | 2026-07-09 | NSE | BAJAJ-AUTO | train | 5049 | 328 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=BAJAJ-AUTO\event_surprise_conditional_labels.parquet | 51379 | 0 |
| 1 | 2026-07-09 | NSE | BANKBEES | train | 8885 | 855 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=BANKBEES\event_surprise_conditional_labels.parquet | 83309 | 0 |
| 1 | 2026-07-09 | NSE | BHARTIARTL | train | 9411 | 960 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=BHARTIARTL\event_surprise_conditional_labels.parquet | 88411 | 0 |
| 1 | 2026-07-09 | NSE | BPCL | train | 4696 | 365 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=BPCL\event_surprise_conditional_labels.parquet | 48129 | 0 |
| 1 | 2026-07-09 | NSE | BRITANNIA | train | 4229 | 909 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=BRITANNIA\event_surprise_conditional_labels.parquet | 45862 | 0 |
| 1 | 2026-07-09 | NSE | CIPLA | train | 4886 | 421 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=CIPLA\event_surprise_conditional_labels.parquet | 49312 | 0 |
| 1 | 2026-07-09 | NSE | DRREDDY | train | 9053 | 5218 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=DRREDDY\event_surprise_conditional_labels.parquet | 88176 | 0 |
| 1 | 2026-07-09 | NSE | GOLDBEES | train | 6407 | 590 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=GOLDBEES\event_surprise_conditional_labels.parquet | 61635 | 0 |
| 1 | 2026-07-09 | NSE | HCLTECH | train | 5477 | 1575 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=HCLTECH\event_surprise_conditional_labels.parquet | 55889 | 0 |
| 1 | 2026-07-09 | NSE | HDFCBANK | train | 9419 | 866 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=HDFCBANK\event_surprise_conditional_labels.parquet | 87645 | 0 |
| 1 | 2026-07-09 | NSE | HINDUNILVR | train | 6946 | 659 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=HINDUNILVR\event_surprise_conditional_labels.parquet | 67320 | 0 |
| 1 | 2026-07-09 | NSE | ICICIBANK | train | 9152 | 822 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ICICIBANK\event_surprise_conditional_labels.parquet | 85507 | 0 |
| 1 | 2026-07-09 | NSE | INFY | train | 7566 | 541 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=INFY\event_surprise_conditional_labels.parquet | 70684 | 0 |
| 1 | 2026-07-09 | NSE | ITBEES | train | 3872 | 705 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ITBEES\event_surprise_conditional_labels.parquet | 41417 | 0 |
| 1 | 2026-07-09 | NSE | ITC | train | 7309 | 789 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ITC\event_surprise_conditional_labels.parquet | 68432 | 0 |
| 1 | 2026-07-09 | NSE | JUNIORBEES | train | 8589 | 815 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=JUNIORBEES\event_surprise_conditional_labels.parquet | 80818 | 0 |
| 1 | 2026-07-09 | NSE | KOTAKBANK | train | 8943 | 760 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=KOTAKBANK\event_surprise_conditional_labels.parquet | 82897 | 0 |
| 1 | 2026-07-09 | NSE | LT | train | 9072 | 805 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=LT\event_surprise_conditional_labels.parquet | 85093 | 0 |
| 1 | 2026-07-09 | NSE | M&M | train | 7704 | 592 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=M&M\event_surprise_conditional_labels.parquet | 72614 | 0 |
| 1 | 2026-07-09 | NSE | MARUTI | train | 7379 | 729 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=MARUTI\event_surprise_conditional_labels.parquet | 70395 | 0 |
| 1 | 2026-07-09 | NSE | NESTLEIND | train | 4454 | 287 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=NESTLEIND\event_surprise_conditional_labels.parquet | 46882 | 0 |
| 1 | 2026-07-09 | NSE | NIFTYBEES | train | 8019 | 657 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=NIFTYBEES\event_surprise_conditional_labels.parquet | 74044 | 0 |
| 1 | 2026-07-09 | NSE | ONGC | train | 5782 | 543 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ONGC\event_surprise_conditional_labels.parquet | 57650 | 0 |
| 1 | 2026-07-09 | NSE | RELIANCE | train | 9017 | 790 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=RELIANCE\event_surprise_conditional_labels.parquet | 84285 | 0 |
| 1 | 2026-07-09 | NSE | SBIN | train | 7833 | 590 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=SBIN\event_surprise_conditional_labels.parquet | 73566 | 0 |
| 1 | 2026-07-09 | NSE | SUNPHARMA | train | 7322 | 773 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=SUNPHARMA\event_surprise_conditional_labels.parquet | 70246 | 0 |
| 1 | 2026-07-09 | NSE | TCS | train | 7969 | 807 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=TCS\event_surprise_conditional_labels.parquet | 75762 | 0 |
| 1 | 2026-07-09 | NSE | TECHM | train | 4929 | 1291 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=TECHM\event_surprise_conditional_labels.parquet | 51540 | 0 |
| 1 | 2026-07-09 | NSE | ULTRACEMCO | train | 3979 | 185 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ULTRACEMCO\event_surprise_conditional_labels.parquet | 41684 | 0 |
| 1 | 2026-07-09 | NSE | WIPRO | train | 5788 | 1976 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=WIPRO\event_surprise_conditional_labels.parquet | 58881 | 0 |
| 1 | 2026-07-10 | NSE | ADANIPORTS | train | 9546 | 704 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ADANIPORTS\event_surprise_conditional_labels.parquet | 88527 | 0 |
| 1 | 2026-07-10 | NSE | AXISBANK | train | 10801 | 565 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=AXISBANK\event_surprise_conditional_labels.parquet | 97342 | 0 |
| 1 | 2026-07-10 | NSE | BAJAJ-AUTO | train | 9727 | 711 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=BAJAJ-AUTO\event_surprise_conditional_labels.parquet | 90469 | 0 |
| 1 | 2026-07-10 | NSE | BANKBEES | train | 9229 | 593 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=BANKBEES\event_surprise_conditional_labels.parquet | 84349 | 0 |
| 1 | 2026-07-10 | NSE | BHARTIARTL | train | 11365 | 663 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=BHARTIARTL\event_surprise_conditional_labels.parquet | 102290 | 0 |
| 1 | 2026-07-10 | NSE | BPCL | train | 6758 | 290 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=BPCL\event_surprise_conditional_labels.parquet | 63081 | 0 |
| 1 | 2026-07-10 | NSE | BRITANNIA | train | 6029 | 879 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=BRITANNIA\event_surprise_conditional_labels.parquet | 59652 | 0 |
| 1 | 2026-07-10 | NSE | CIPLA | train | 7907 | 437 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=CIPLA\event_surprise_conditional_labels.parquet | 73326 | 0 |
| 1 | 2026-07-10 | NSE | DRREDDY | train | 13141 | 925 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=DRREDDY\event_surprise_conditional_labels.parquet | 117867 | 0 |
| 1 | 2026-07-10 | NSE | GOLDBEES | train | 9148 | 715 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=GOLDBEES\event_surprise_conditional_labels.parquet | 84353 | 0 |
| 1 | 2026-07-10 | NSE | HCLTECH | train | 14317 | 1321 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=HCLTECH\event_surprise_conditional_labels.parquet | 126019 | 0 |
| 1 | 2026-07-10 | NSE | HDFCBANK | train | 15043 | 1255 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=HDFCBANK\event_surprise_conditional_labels.parquet | 130691 | 0 |
| 1 | 2026-07-10 | NSE | HINDUNILVR | train | 8661 | 533 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=HINDUNILVR\event_surprise_conditional_labels.parquet | 80552 | 0 |
| 1 | 2026-07-10 | NSE | ICICIBANK | train | 11236 | 612 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ICICIBANK\event_surprise_conditional_labels.parquet | 100668 | 0 |
| 1 | 2026-07-10 | NSE | INFY | train | 15210 | 1263 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=INFY\event_surprise_conditional_labels.parquet | 132749 | 0 |
| 1 | 2026-07-10 | NSE | ITBEES | train | 6822 | 1249 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ITBEES\event_surprise_conditional_labels.parquet | 62577 | 0 |
| 1 | 2026-07-10 | NSE | ITC | train | 11084 | 617 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ITC\event_surprise_conditional_labels.parquet | 97925 | 0 |
| 1 | 2026-07-10 | NSE | JUNIORBEES | train | 13252 | 1165 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=JUNIORBEES\event_surprise_conditional_labels.parquet | 118247 | 0 |
| 1 | 2026-07-10 | NSE | KOTAKBANK | train | 10164 | 452 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=KOTAKBANK\event_surprise_conditional_labels.parquet | 92326 | 0 |
| 1 | 2026-07-10 | NSE | LT | train | 10640 | 544 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=LT\event_surprise_conditional_labels.parquet | 95863 | 0 |
| 1 | 2026-07-10 | NSE | M&M | train | 9987 | 472 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=M&M\event_surprise_conditional_labels.parquet | 89801 | 0 |
| 1 | 2026-07-10 | NSE | MARUTI | train | 11104 | 680 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=MARUTI\event_surprise_conditional_labels.parquet | 99877 | 0 |
| 1 | 2026-07-10 | NSE | NESTLEIND | train | 7878 | 419 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=NESTLEIND\event_surprise_conditional_labels.parquet | 73637 | 0 |
| 1 | 2026-07-10 | NSE | NIFTYBEES | train | 11226 | 697 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=NIFTYBEES\event_surprise_conditional_labels.parquet | 99904 | 0 |
| 1 | 2026-07-10 | NSE | ONGC | train | 9395 | 693 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ONGC\event_surprise_conditional_labels.parquet | 86669 | 0 |
| 1 | 2026-07-10 | NSE | RELIANCE | train | 11459 | 656 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=RELIANCE\event_surprise_conditional_labels.parquet | 102561 | 0 |
| 1 | 2026-07-10 | NSE | SBIN | train | 12205 | 809 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=SBIN\event_surprise_conditional_labels.parquet | 109742 | 0 |
| 1 | 2026-07-10 | NSE | SUNPHARMA | train | 9908 | 443 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=SUNPHARMA\event_surprise_conditional_labels.parquet | 90680 | 0 |
| 1 | 2026-07-10 | NSE | TCS | train | 16259 | 1457 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=TCS\event_surprise_conditional_labels.parquet | 144159 | 0 |
| 1 | 2026-07-10 | NSE | TECHM | train | 9551 | 683 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=TECHM\event_surprise_conditional_labels.parquet | 89415 | 0 |
| 1 | 2026-07-10 | NSE | ULTRACEMCO | train | 6525 | 1107 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ULTRACEMCO\event_surprise_conditional_labels.parquet | 64098 | 0 |
| 1 | 2026-07-10 | NSE | WIPRO | train | 10157 | 914 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=WIPRO\event_surprise_conditional_labels.parquet | 94164 | 0 |
| 1 | 2026-07-13 | NSE | ADANIPORTS | validation | 9453 | 709 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ADANIPORTS\event_surprise_conditional_labels.parquet | 88713 | 0 |
| 1 | 2026-07-13 | NSE | AXISBANK | validation | 10797 | 565 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=AXISBANK\event_surprise_conditional_labels.parquet | 97857 | 0 |
| 1 | 2026-07-13 | NSE | BAJAJ-AUTO | validation | 14298 | 1285 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=BAJAJ-AUTO\event_surprise_conditional_labels.parquet | 127729 | 0 |
| 1 | 2026-07-13 | NSE | BANKBEES | validation | 13183 | 1133 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=BANKBEES\event_surprise_conditional_labels.parquet | 115659 | 0 |
| 1 | 2026-07-13 | NSE | BHARTIARTL | validation | 11538 | 667 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=BHARTIARTL\event_surprise_conditional_labels.parquet | 103894 | 0 |
| 1 | 2026-07-13 | NSE | BPCL | validation | 8034 | 1851 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=BPCL\event_surprise_conditional_labels.parquet | 74861 | 0 |
| 1 | 2026-07-13 | NSE | BRITANNIA | validation | 6759 | 1368 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=BRITANNIA\event_surprise_conditional_labels.parquet | 65613 | 0 |
| 1 | 2026-07-13 | NSE | CIPLA | validation | 8387 | 528 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=CIPLA\event_surprise_conditional_labels.parquet | 78584 | 0 |
| 1 | 2026-07-13 | NSE | DRREDDY | validation | 8735 | 207 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=DRREDDY\event_surprise_conditional_labels.parquet | 80685 | 0 |
| 1 | 2026-07-13 | NSE | GOLDBEES | validation | 8947 | 661 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=GOLDBEES\event_surprise_conditional_labels.parquet | 83151 | 0 |
| 1 | 2026-07-13 | NSE | HCLTECH | validation | 14296 | 1317 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=HCLTECH\event_surprise_conditional_labels.parquet | 128472 | 0 |
| 1 | 2026-07-13 | NSE | HDFCBANK | validation | 16565 | 1513 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=HDFCBANK\event_surprise_conditional_labels.parquet | 147703 | 0 |
| 1 | 2026-07-13 | NSE | HINDUNILVR | validation | 8591 | 529 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=HINDUNILVR\event_surprise_conditional_labels.parquet | 80772 | 0 |
| 1 | 2026-07-13 | NSE | ICICIBANK | validation | 13716 | 1031 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ICICIBANK\event_surprise_conditional_labels.parquet | 122345 | 0 |
| 1 | 2026-07-13 | NSE | INFY | validation | 16206 | 1459 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=INFY\event_surprise_conditional_labels.parquet | 141151 | 0 |
| 1 | 2026-07-13 | NSE | ITBEES | validation | 8304 | 2136 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ITBEES\event_surprise_conditional_labels.parquet | 79030 | 0 |
| 1 | 2026-07-13 | NSE | ITC | validation | 8757 | 217 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ITC\event_surprise_conditional_labels.parquet | 77051 | 0 |
| 1 | 2026-07-13 | NSE | JUNIORBEES | validation | 11801 | 933 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=JUNIORBEES\event_surprise_conditional_labels.parquet | 105885 | 0 |
| 1 | 2026-07-13 | NSE | KOTAKBANK | validation | 9402 | 322 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=KOTAKBANK\event_surprise_conditional_labels.parquet | 85801 | 0 |
| 1 | 2026-07-13 | NSE | LT | validation | 11478 | 670 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=LT\event_surprise_conditional_labels.parquet | 104024 | 0 |
| 1 | 2026-07-13 | NSE | M&M | validation | 14145 | 1139 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=M&M\event_surprise_conditional_labels.parquet | 126631 | 0 |
| 1 | 2026-07-13 | NSE | MARUTI | validation | 15406 | 1359 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=MARUTI\event_surprise_conditional_labels.parquet | 135777 | 0 |
| 1 | 2026-07-13 | NSE | NESTLEIND | validation | 9035 | 586 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=NESTLEIND\event_surprise_conditional_labels.parquet | 83561 | 0 |
| 1 | 2026-07-13 | NSE | NIFTYBEES | validation | 13039 | 980 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=NIFTYBEES\event_surprise_conditional_labels.parquet | 114837 | 0 |
| 1 | 2026-07-13 | NSE | ONGC | validation | 10644 | 853 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ONGC\event_surprise_conditional_labels.parquet | 97408 | 0 |
| 1 | 2026-07-13 | NSE | RELIANCE | validation | 13219 | 962 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=RELIANCE\event_surprise_conditional_labels.parquet | 117141 | 0 |
| 1 | 2026-07-13 | NSE | SBIN | validation | 13084 | 932 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=SBIN\event_surprise_conditional_labels.parquet | 117020 | 0 |
| 1 | 2026-07-13 | NSE | SUNPHARMA | validation | 9572 | 713 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=SUNPHARMA\event_surprise_conditional_labels.parquet | 89229 | 0 |
| 1 | 2026-07-13 | NSE | TCS | validation | 16806 | 1550 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=TCS\event_surprise_conditional_labels.parquet | 150197 | 0 |
| 1 | 2026-07-13 | NSE | TECHM | validation | 11316 | 954 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=TECHM\event_surprise_conditional_labels.parquet | 104167 | 0 |
| 1 | 2026-07-13 | NSE | ULTRACEMCO | validation | 6783 | 1317 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ULTRACEMCO\event_surprise_conditional_labels.parquet | 66374 | 0 |
| 1 | 2026-07-13 | NSE | WIPRO | validation | 11490 | 1011 | derived_phase214_event_surprise_conditional_labels\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=WIPRO\event_surprise_conditional_labels.parquet | 105586 | 0 |
| 5 | 2026-07-08 | NSE | ADANIPORTS | train | 1617 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ADANIPORTS\event_surprise_conditional_labels.parquet | 22382 | 0 |
| 5 | 2026-07-08 | NSE | AXISBANK | train | 1699 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=AXISBANK\event_surprise_conditional_labels.parquet | 22979 | 0 |
| 5 | 2026-07-08 | NSE | BAJAJ-AUTO | train | 1594 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BAJAJ-AUTO\event_surprise_conditional_labels.parquet | 22206 | 0 |
| 5 | 2026-07-08 | NSE | BANKBEES | train | 1693 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BANKBEES\event_surprise_conditional_labels.parquet | 22868 | 0 |
| 5 | 2026-07-08 | NSE | BHARTIARTL | train | 1616 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BHARTIARTL\event_surprise_conditional_labels.parquet | 22350 | 0 |
| 5 | 2026-07-08 | NSE | BPCL | train | 1578 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BPCL\event_surprise_conditional_labels.parquet | 21859 | 0 |
| 5 | 2026-07-08 | NSE | BRITANNIA | train | 1525 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BRITANNIA\event_surprise_conditional_labels.parquet | 21633 | 0 |
| 5 | 2026-07-08 | NSE | CIPLA | train | 1572 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=CIPLA\event_surprise_conditional_labels.parquet | 22016 | 0 |
| 5 | 2026-07-08 | NSE | DRREDDY | train | 1582 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=DRREDDY\event_surprise_conditional_labels.parquet | 22093 | 0 |
| 5 | 2026-07-08 | NSE | GOLDBEES | train | 1642 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=GOLDBEES\event_surprise_conditional_labels.parquet | 22508 | 0 |
| 5 | 2026-07-08 | NSE | HCLTECH | train | 1564 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=HCLTECH\event_surprise_conditional_labels.parquet | 21974 | 0 |
| 5 | 2026-07-08 | NSE | HDFCBANK | train | 1745 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=HDFCBANK\event_surprise_conditional_labels.parquet | 23307 | 0 |
| 5 | 2026-07-08 | NSE | HINDUNILVR | train | 1618 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=HINDUNILVR\event_surprise_conditional_labels.parquet | 22387 | 0 |
| 5 | 2026-07-08 | NSE | ICICIBANK | train | 1722 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ICICIBANK\event_surprise_conditional_labels.parquet | 23154 | 0 |
| 5 | 2026-07-08 | NSE | INFY | train | 1682 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=INFY\event_surprise_conditional_labels.parquet | 22831 | 0 |
| 5 | 2026-07-08 | NSE | ITBEES | train | 1585 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ITBEES\event_surprise_conditional_labels.parquet | 21162 | 0 |
| 5 | 2026-07-08 | NSE | ITC | train | 1643 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ITC\event_surprise_conditional_labels.parquet | 22521 | 0 |
| 5 | 2026-07-08 | NSE | JUNIORBEES | train | 1685 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=JUNIORBEES\event_surprise_conditional_labels.parquet | 22864 | 0 |
| 5 | 2026-07-08 | NSE | KOTAKBANK | train | 1664 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=KOTAKBANK\event_surprise_conditional_labels.parquet | 22700 | 0 |
| 5 | 2026-07-08 | NSE | LT | train | 1733 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=LT\event_surprise_conditional_labels.parquet | 23191 | 0 |
| 5 | 2026-07-08 | NSE | M&M | train | 1714 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=M&M\event_surprise_conditional_labels.parquet | 23061 | 0 |
| 5 | 2026-07-08 | NSE | MARUTI | train | 1679 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=MARUTI\event_surprise_conditional_labels.parquet | 22812 | 0 |
| 5 | 2026-07-08 | NSE | NESTLEIND | train | 1580 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=NESTLEIND\event_surprise_conditional_labels.parquet | 22058 | 0 |
| 5 | 2026-07-08 | NSE | NIFTYBEES | train | 1687 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=NIFTYBEES\event_surprise_conditional_labels.parquet | 22822 | 0 |
| 5 | 2026-07-08 | NSE | ONGC | train | 1628 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ONGC\event_surprise_conditional_labels.parquet | 22419 | 0 |
| 5 | 2026-07-08 | NSE | RELIANCE | train | 1731 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=RELIANCE\event_surprise_conditional_labels.parquet | 23190 | 0 |
| 5 | 2026-07-08 | NSE | SBIN | train | 1686 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=SBIN\event_surprise_conditional_labels.parquet | 22851 | 0 |
| 5 | 2026-07-08 | NSE | SUNPHARMA | train | 1600 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=SUNPHARMA\event_surprise_conditional_labels.parquet | 22224 | 0 |
| 5 | 2026-07-08 | NSE | TCS | train | 1651 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=TCS\event_surprise_conditional_labels.parquet | 22595 | 0 |
| 5 | 2026-07-08 | NSE | TECHM | train | 1574 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=TECHM\event_surprise_conditional_labels.parquet | 22025 | 0 |
| 5 | 2026-07-08 | NSE | ULTRACEMCO | train | 1577 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ULTRACEMCO\event_surprise_conditional_labels.parquet | 22080 | 0 |
| 5 | 2026-07-08 | NSE | WIPRO | train | 1569 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=WIPRO\event_surprise_conditional_labels.parquet | 21991 | 0 |
| 5 | 2026-07-09 | NSE | ADANIPORTS | train | 2448 | 240 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=ADANIPORTS\event_surprise_conditional_labels.parquet | 30636 | 0 |
| 5 | 2026-07-09 | NSE | AXISBANK | train | 2522 | 268 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=AXISBANK\event_surprise_conditional_labels.parquet | 31190 | 0 |
| 5 | 2026-07-09 | NSE | BAJAJ-AUTO | train | 2390 | 210 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=BAJAJ-AUTO\event_surprise_conditional_labels.parquet | 29953 | 0 |
| 5 | 2026-07-09 | NSE | BANKBEES | train | 2537 | 318 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=BANKBEES\event_surprise_conditional_labels.parquet | 31146 | 0 |
| 5 | 2026-07-09 | NSE | BHARTIARTL | train | 2558 | 667 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=BHARTIARTL\event_surprise_conditional_labels.parquet | 31930 | 0 |
| 5 | 2026-07-09 | NSE | BPCL | train | 2421 | 192 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=BPCL\event_surprise_conditional_labels.parquet | 30003 | 0 |
| 5 | 2026-07-09 | NSE | BRITANNIA | train | 2364 | 732 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=BRITANNIA\event_surprise_conditional_labels.parquet | 30296 | 0 |
| 5 | 2026-07-09 | NSE | CIPLA | train | 2407 | 209 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=CIPLA\event_surprise_conditional_labels.parquet | 29914 | 0 |
| 5 | 2026-07-09 | NSE | DRREDDY | train | 2539 | 1216 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=DRREDDY\event_surprise_conditional_labels.parquet | 31758 | 0 |
| 5 | 2026-07-09 | NSE | GOLDBEES | train | 2469 | 316 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=GOLDBEES\event_surprise_conditional_labels.parquet | 30680 | 0 |
| 5 | 2026-07-09 | NSE | HCLTECH | train | 2462 | 664 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=HCLTECH\event_surprise_conditional_labels.parquet | 31055 | 0 |
| 5 | 2026-07-09 | NSE | HDFCBANK | train | 2557 | 459 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=HDFCBANK\event_surprise_conditional_labels.parquet | 31919 | 0 |
| 5 | 2026-07-09 | NSE | HINDUNILVR | train | 2484 | 428 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=HINDUNILVR\event_surprise_conditional_labels.parquet | 31177 | 0 |
| 5 | 2026-07-09 | NSE | ICICIBANK | train | 2548 | 441 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=ICICIBANK\event_surprise_conditional_labels.parquet | 31839 | 0 |
| 5 | 2026-07-09 | NSE | INFY | train | 2532 | 296 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=INFY\event_surprise_conditional_labels.parquet | 31297 | 0 |
| 5 | 2026-07-09 | NSE | ITBEES | train | 2350 | 431 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=ITBEES\event_surprise_conditional_labels.parquet | 29712 | 0 |
| 5 | 2026-07-09 | NSE | ITC | train | 2527 | 403 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=ITC\event_surprise_conditional_labels.parquet | 31041 | 0 |
| 5 | 2026-07-09 | NSE | JUNIORBEES | train | 2525 | 325 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=JUNIORBEES\event_surprise_conditional_labels.parquet | 31340 | 0 |
| 5 | 2026-07-09 | NSE | KOTAKBANK | train | 2555 | 489 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=KOTAKBANK\event_surprise_conditional_labels.parquet | 31682 | 0 |
| 5 | 2026-07-09 | NSE | LT | train | 2557 | 446 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=LT\event_surprise_conditional_labels.parquet | 31860 | 0 |
| 5 | 2026-07-09 | NSE | M&M | train | 2505 | 321 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=M&M\event_surprise_conditional_labels.parquet | 31104 | 0 |
| 5 | 2026-07-09 | NSE | MARUTI | train | 2493 | 410 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=MARUTI\event_surprise_conditional_labels.parquet | 31202 | 0 |
| 5 | 2026-07-09 | NSE | NESTLEIND | train | 2386 | 165 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=NESTLEIND\event_surprise_conditional_labels.parquet | 29897 | 0 |
| 5 | 2026-07-09 | NSE | NIFTYBEES | train | 2514 | 237 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=NIFTYBEES\event_surprise_conditional_labels.parquet | 31056 | 0 |
| 5 | 2026-07-09 | NSE | ONGC | train | 2451 | 220 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=ONGC\event_surprise_conditional_labels.parquet | 30140 | 0 |
| 5 | 2026-07-09 | NSE | RELIANCE | train | 2539 | 402 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=RELIANCE\event_surprise_conditional_labels.parquet | 31382 | 0 |
| 5 | 2026-07-09 | NSE | SBIN | train | 2520 | 387 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=SBIN\event_surprise_conditional_labels.parquet | 31336 | 0 |
| 5 | 2026-07-09 | NSE | SUNPHARMA | train | 2517 | 487 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=SUNPHARMA\event_surprise_conditional_labels.parquet | 31453 | 0 |
| 5 | 2026-07-09 | NSE | TCS | train | 2530 | 506 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=TCS\event_surprise_conditional_labels.parquet | 31641 | 0 |
| 5 | 2026-07-09 | NSE | TECHM | train | 2392 | 586 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=TECHM\event_surprise_conditional_labels.parquet | 30523 | 0 |
| 5 | 2026-07-09 | NSE | ULTRACEMCO | train | 2358 | 99 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=ULTRACEMCO\event_surprise_conditional_labels.parquet | 29302 | 0 |
| 5 | 2026-07-09 | NSE | WIPRO | train | 2447 | 779 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=WIPRO\event_surprise_conditional_labels.parquet | 30994 | 0 |
| 5 | 2026-07-10 | NSE | ADANIPORTS | train | 4276 | 379 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=ADANIPORTS\event_surprise_conditional_labels.parquet | 45752 | 0 |
| 5 | 2026-07-10 | NSE | AXISBANK | train | 4310 | 253 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=AXISBANK\event_surprise_conditional_labels.parquet | 45638 | 0 |
| 5 | 2026-07-10 | NSE | BAJAJ-AUTO | train | 4202 | 435 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=BAJAJ-AUTO\event_surprise_conditional_labels.parquet | 45426 | 0 |
| 5 | 2026-07-10 | NSE | BANKBEES | train | 4105 | 201 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=BANKBEES\event_surprise_conditional_labels.parquet | 43102 | 0 |
| 5 | 2026-07-10 | NSE | BHARTIARTL | train | 4351 | 256 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=BHARTIARTL\event_surprise_conditional_labels.parquet | 46022 | 0 |
| 5 | 2026-07-10 | NSE | BPCL | train | 4073 | 155 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=BPCL\event_surprise_conditional_labels.parquet | 42422 | 0 |
| 5 | 2026-07-10 | NSE | BRITANNIA | train | 3917 | 509 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=BRITANNIA\event_surprise_conditional_labels.parquet | 42392 | 0 |
| 5 | 2026-07-10 | NSE | CIPLA | train | 4190 | 256 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=CIPLA\event_surprise_conditional_labels.parquet | 44584 | 0 |
| 5 | 2026-07-10 | NSE | DRREDDY | train | 4375 | 504 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=DRREDDY\event_surprise_conditional_labels.parquet | 46999 | 0 |
| 5 | 2026-07-10 | NSE | GOLDBEES | train | 4250 | 311 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=GOLDBEES\event_surprise_conditional_labels.parquet | 45100 | 0 |
| 5 | 2026-07-10 | NSE | HCLTECH | train | 4425 | 1091 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=HCLTECH\event_surprise_conditional_labels.parquet | 47676 | 0 |
| 5 | 2026-07-10 | NSE | HDFCBANK | train | 4448 | 525 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=HDFCBANK\event_surprise_conditional_labels.parquet | 47538 | 0 |
| 5 | 2026-07-10 | NSE | HINDUNILVR | train | 4184 | 239 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=HINDUNILVR\event_surprise_conditional_labels.parquet | 44483 | 0 |
| 5 | 2026-07-10 | NSE | ICICIBANK | train | 4342 | 254 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=ICICIBANK\event_surprise_conditional_labels.parquet | 45835 | 0 |
| 5 | 2026-07-10 | NSE | INFY | train | 4460 | 671 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=INFY\event_surprise_conditional_labels.parquet | 48019 | 0 |
| 5 | 2026-07-10 | NSE | ITBEES | train | 4066 | 696 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=ITBEES\event_surprise_conditional_labels.parquet | 41600 | 0 |
| 5 | 2026-07-10 | NSE | ITC | train | 4335 | 364 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=ITC\event_surprise_conditional_labels.parquet | 45630 | 0 |
| 5 | 2026-07-10 | NSE | JUNIORBEES | train | 4329 | 456 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=JUNIORBEES\event_surprise_conditional_labels.parquet | 46443 | 0 |
| 5 | 2026-07-10 | NSE | KOTAKBANK | train | 4285 | 181 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=KOTAKBANK\event_surprise_conditional_labels.parquet | 45132 | 0 |
| 5 | 2026-07-10 | NSE | LT | train | 4270 | 199 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=LT\event_surprise_conditional_labels.parquet | 45057 | 0 |
| 5 | 2026-07-10 | NSE | M&M | train | 4236 | 185 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=M&M\event_surprise_conditional_labels.parquet | 44641 | 0 |
| 5 | 2026-07-10 | NSE | MARUTI | train | 4273 | 281 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=MARUTI\event_surprise_conditional_labels.parquet | 45232 | 0 |
| 5 | 2026-07-10 | NSE | NESTLEIND | train | 4127 | 260 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=NESTLEIND\event_surprise_conditional_labels.parquet | 44229 | 0 |
| 5 | 2026-07-10 | NSE | NIFTYBEES | train | 4295 | 297 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=NIFTYBEES\event_surprise_conditional_labels.parquet | 45347 | 0 |
| 5 | 2026-07-10 | NSE | ONGC | train | 4237 | 340 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=ONGC\event_surprise_conditional_labels.parquet | 44856 | 0 |
| 5 | 2026-07-10 | NSE | RELIANCE | train | 4360 | 241 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=RELIANCE\event_surprise_conditional_labels.parquet | 45384 | 0 |
| 5 | 2026-07-10 | NSE | SBIN | train | 4354 | 383 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=SBIN\event_surprise_conditional_labels.parquet | 46410 | 0 |
| 5 | 2026-07-10 | NSE | SUNPHARMA | train | 4285 | 221 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=SUNPHARMA\event_surprise_conditional_labels.parquet | 45293 | 0 |
| 5 | 2026-07-10 | NSE | TCS | train | 4481 | 815 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=TCS\event_surprise_conditional_labels.parquet | 48542 | 0 |
| 5 | 2026-07-10 | NSE | TECHM | train | 4254 | 456 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=TECHM\event_surprise_conditional_labels.parquet | 45886 | 0 |
| 5 | 2026-07-10 | NSE | ULTRACEMCO | train | 4018 | 627 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=ULTRACEMCO\event_surprise_conditional_labels.parquet | 43500 | 0 |
| 5 | 2026-07-10 | NSE | WIPRO | train | 4321 | 532 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=WIPRO\event_surprise_conditional_labels.parquet | 46590 | 0 |
| 5 | 2026-07-13 | NSE | ADANIPORTS | validation | 4268 | 364 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=ADANIPORTS\event_surprise_conditional_labels.parquet | 46060 | 0 |
| 5 | 2026-07-13 | NSE | AXISBANK | validation | 4285 | 345 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=AXISBANK\event_surprise_conditional_labels.parquet | 45623 | 0 |
| 5 | 2026-07-13 | NSE | BAJAJ-AUTO | validation | 4384 | 969 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=BAJAJ-AUTO\event_surprise_conditional_labels.parquet | 47624 | 0 |
| 5 | 2026-07-13 | NSE | BANKBEES | validation | 4285 | 427 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=BANKBEES\event_surprise_conditional_labels.parquet | 45456 | 0 |
| 5 | 2026-07-13 | NSE | BHARTIARTL | validation | 4367 | 320 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=BHARTIARTL\event_surprise_conditional_labels.parquet | 46221 | 0 |
| 5 | 2026-07-13 | NSE | BPCL | validation | 4189 | 901 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=BPCL\event_surprise_conditional_labels.parquet | 45280 | 0 |
| 5 | 2026-07-13 | NSE | BRITANNIA | validation | 4043 | 795 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=BRITANNIA\event_surprise_conditional_labels.parquet | 43611 | 0 |
| 5 | 2026-07-13 | NSE | CIPLA | validation | 4212 | 328 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=CIPLA\event_surprise_conditional_labels.parquet | 45025 | 0 |
| 5 | 2026-07-13 | NSE | DRREDDY | validation | 4258 | 96 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=DRREDDY\event_surprise_conditional_labels.parquet | 44559 | 0 |
| 5 | 2026-07-13 | NSE | GOLDBEES | validation | 4227 | 306 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=GOLDBEES\event_surprise_conditional_labels.parquet | 45070 | 0 |
| 5 | 2026-07-13 | NSE | HCLTECH | validation | 4400 | 961 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=HCLTECH\event_surprise_conditional_labels.parquet | 47664 | 0 |
| 5 | 2026-07-13 | NSE | HDFCBANK | validation | 4473 | 677 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=HDFCBANK\event_surprise_conditional_labels.parquet | 48428 | 0 |
| 5 | 2026-07-13 | NSE | HINDUNILVR | validation | 4217 | 257 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=HINDUNILVR\event_surprise_conditional_labels.parquet | 45018 | 0 |
| 5 | 2026-07-13 | NSE | ICICIBANK | validation | 4388 | 488 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=ICICIBANK\event_surprise_conditional_labels.parquet | 47078 | 0 |
| 5 | 2026-07-13 | NSE | INFY | validation | 4471 | 789 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=INFY\event_surprise_conditional_labels.parquet | 48481 | 0 |
| 5 | 2026-07-13 | NSE | ITBEES | validation | 4192 | 950 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=ITBEES\event_surprise_conditional_labels.parquet | 45610 | 0 |
| 5 | 2026-07-13 | NSE | ITC | validation | 4227 | 119 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=ITC\event_surprise_conditional_labels.parquet | 43196 | 0 |
| 5 | 2026-07-13 | NSE | JUNIORBEES | validation | 4245 | 401 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=JUNIORBEES\event_surprise_conditional_labels.parquet | 45472 | 0 |
| 5 | 2026-07-13 | NSE | KOTAKBANK | validation | 4253 | 176 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=KOTAKBANK\event_surprise_conditional_labels.parquet | 44718 | 0 |
| 5 | 2026-07-13 | NSE | LT | validation | 4319 | 320 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=LT\event_surprise_conditional_labels.parquet | 45995 | 0 |
| 5 | 2026-07-13 | NSE | M&M | validation | 4396 | 552 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=M&M\event_surprise_conditional_labels.parquet | 47504 | 0 |
| 5 | 2026-07-13 | NSE | MARUTI | validation | 4442 | 580 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=MARUTI\event_surprise_conditional_labels.parquet | 47825 | 0 |
| 5 | 2026-07-13 | NSE | NESTLEIND | validation | 4206 | 424 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=NESTLEIND\event_surprise_conditional_labels.parquet | 45162 | 0 |
| 5 | 2026-07-13 | NSE | NIFTYBEES | validation | 4323 | 447 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=NIFTYBEES\event_surprise_conditional_labels.parquet | 46353 | 0 |
| 5 | 2026-07-13 | NSE | ONGC | validation | 4308 | 507 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=ONGC\event_surprise_conditional_labels.parquet | 45620 | 0 |
| 5 | 2026-07-13 | NSE | RELIANCE | validation | 4366 | 587 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=RELIANCE\event_surprise_conditional_labels.parquet | 46302 | 0 |
| 5 | 2026-07-13 | NSE | SBIN | validation | 4353 | 499 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=SBIN\event_surprise_conditional_labels.parquet | 46802 | 0 |
| 5 | 2026-07-13 | NSE | SUNPHARMA | validation | 4236 | 387 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=SUNPHARMA\event_surprise_conditional_labels.parquet | 45698 | 0 |
| 5 | 2026-07-13 | NSE | TCS | validation | 4484 | 911 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=TCS\event_surprise_conditional_labels.parquet | 48696 | 0 |
| 5 | 2026-07-13 | NSE | TECHM | validation | 4288 | 713 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=TECHM\event_surprise_conditional_labels.parquet | 46563 | 0 |
| 5 | 2026-07-13 | NSE | ULTRACEMCO | validation | 4084 | 764 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=ULTRACEMCO\event_surprise_conditional_labels.parquet | 44244 | 0 |
| 5 | 2026-07-13 | NSE | WIPRO | validation | 4288 | 712 | derived_phase214_event_surprise_conditional_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=WIPRO\event_surprise_conditional_labels.parquet | 46551 | 0 |
| 15 | 2026-07-08 | NSE | ADANIPORTS | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=ADANIPORTS\event_surprise_conditional_labels.parquet | 14626 | 0 |
| 15 | 2026-07-08 | NSE | AXISBANK | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=AXISBANK\event_surprise_conditional_labels.parquet | 14614 | 0 |
| 15 | 2026-07-08 | NSE | BAJAJ-AUTO | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=BAJAJ-AUTO\event_surprise_conditional_labels.parquet | 14621 | 0 |
| 15 | 2026-07-08 | NSE | BANKBEES | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=BANKBEES\event_surprise_conditional_labels.parquet | 14608 | 0 |
| 15 | 2026-07-08 | NSE | BHARTIARTL | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=BHARTIARTL\event_surprise_conditional_labels.parquet | 14617 | 0 |
| 15 | 2026-07-08 | NSE | BPCL | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=BPCL\event_surprise_conditional_labels.parquet | 14567 | 0 |
| 15 | 2026-07-08 | NSE | BRITANNIA | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=BRITANNIA\event_surprise_conditional_labels.parquet | 14617 | 0 |
| 15 | 2026-07-08 | NSE | CIPLA | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=CIPLA\event_surprise_conditional_labels.parquet | 14517 | 0 |
| 15 | 2026-07-08 | NSE | DRREDDY | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=DRREDDY\event_surprise_conditional_labels.parquet | 14610 | 0 |
| 15 | 2026-07-08 | NSE | GOLDBEES | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=GOLDBEES\event_surprise_conditional_labels.parquet | 14618 | 0 |
| 15 | 2026-07-08 | NSE | HCLTECH | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=HCLTECH\event_surprise_conditional_labels.parquet | 14607 | 0 |
| 15 | 2026-07-08 | NSE | HDFCBANK | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=HDFCBANK\event_surprise_conditional_labels.parquet | 14612 | 0 |
| 15 | 2026-07-08 | NSE | HINDUNILVR | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=HINDUNILVR\event_surprise_conditional_labels.parquet | 14542 | 0 |
| 15 | 2026-07-08 | NSE | ICICIBANK | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=ICICIBANK\event_surprise_conditional_labels.parquet | 14619 | 0 |
| 15 | 2026-07-08 | NSE | INFY | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=INFY\event_surprise_conditional_labels.parquet | 14594 | 0 |
| 15 | 2026-07-08 | NSE | ITBEES | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=ITBEES\event_surprise_conditional_labels.parquet | 14247 | 0 |
| 15 | 2026-07-08 | NSE | ITC | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=ITC\event_surprise_conditional_labels.parquet | 14512 | 0 |
| 15 | 2026-07-08 | NSE | JUNIORBEES | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=JUNIORBEES\event_surprise_conditional_labels.parquet | 14618 | 0 |
| 15 | 2026-07-08 | NSE | KOTAKBANK | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=KOTAKBANK\event_surprise_conditional_labels.parquet | 14616 | 0 |
| 15 | 2026-07-08 | NSE | LT | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=LT\event_surprise_conditional_labels.parquet | 14502 | 0 |
| 15 | 2026-07-08 | NSE | M&M | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=M&M\event_surprise_conditional_labels.parquet | 14586 | 0 |
| 15 | 2026-07-08 | NSE | MARUTI | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=MARUTI\event_surprise_conditional_labels.parquet | 14603 | 0 |
| 15 | 2026-07-08 | NSE | NESTLEIND | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=NESTLEIND\event_surprise_conditional_labels.parquet | 14617 | 0 |
| 15 | 2026-07-08 | NSE | NIFTYBEES | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=NIFTYBEES\event_surprise_conditional_labels.parquet | 14616 | 0 |
| 15 | 2026-07-08 | NSE | ONGC | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=ONGC\event_surprise_conditional_labels.parquet | 14591 | 0 |
| 15 | 2026-07-08 | NSE | RELIANCE | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=RELIANCE\event_surprise_conditional_labels.parquet | 14538 | 0 |
| 15 | 2026-07-08 | NSE | SBIN | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=SBIN\event_surprise_conditional_labels.parquet | 14593 | 0 |
| 15 | 2026-07-08 | NSE | SUNPHARMA | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=SUNPHARMA\event_surprise_conditional_labels.parquet | 14538 | 0 |
| 15 | 2026-07-08 | NSE | TCS | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=TCS\event_surprise_conditional_labels.parquet | 14586 | 0 |
| 15 | 2026-07-08 | NSE | TECHM | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=TECHM\event_surprise_conditional_labels.parquet | 14595 | 0 |
| 15 | 2026-07-08 | NSE | ULTRACEMCO | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=ULTRACEMCO\event_surprise_conditional_labels.parquet | 14621 | 0 |
| 15 | 2026-07-08 | NSE | WIPRO | train | 583 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=WIPRO\event_surprise_conditional_labels.parquet | 14600 | 0 |
| 15 | 2026-07-09 | NSE | ADANIPORTS | train | 858 | 5 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=ADANIPORTS\event_surprise_conditional_labels.parquet | 16792 | 0 |
| 15 | 2026-07-09 | NSE | AXISBANK | train | 858 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=AXISBANK\event_surprise_conditional_labels.parquet | 16724 | 0 |
| 15 | 2026-07-09 | NSE | BAJAJ-AUTO | train | 858 | 11 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=BAJAJ-AUTO\event_surprise_conditional_labels.parquet | 16865 | 0 |
| 15 | 2026-07-09 | NSE | BANKBEES | train | 859 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=BANKBEES\event_surprise_conditional_labels.parquet | 16688 | 0 |
| 15 | 2026-07-09 | NSE | BHARTIARTL | train | 858 | 14 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=BHARTIARTL\event_surprise_conditional_labels.parquet | 16929 | 0 |
| 15 | 2026-07-09 | NSE | BPCL | train | 858 | 8 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=BPCL\event_surprise_conditional_labels.parquet | 16781 | 0 |
| 15 | 2026-07-09 | NSE | BRITANNIA | train | 857 | 175 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=BRITANNIA\event_surprise_conditional_labels.parquet | 17396 | 0 |
| 15 | 2026-07-09 | NSE | CIPLA | train | 858 | 10 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=CIPLA\event_surprise_conditional_labels.parquet | 16821 | 0 |
| 15 | 2026-07-09 | NSE | DRREDDY | train | 858 | 525 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=DRREDDY\event_surprise_conditional_labels.parquet | 17460 | 0 |
| 15 | 2026-07-09 | NSE | GOLDBEES | train | 859 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=GOLDBEES\event_surprise_conditional_labels.parquet | 16671 | 0 |
| 15 | 2026-07-09 | NSE | HCLTECH | train | 858 | 129 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=HCLTECH\event_surprise_conditional_labels.parquet | 17424 | 0 |
| 15 | 2026-07-09 | NSE | HDFCBANK | train | 858 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=HDFCBANK\event_surprise_conditional_labels.parquet | 16684 | 0 |
| 15 | 2026-07-09 | NSE | HINDUNILVR | train | 858 | 52 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=HINDUNILVR\event_surprise_conditional_labels.parquet | 17082 | 0 |
| 15 | 2026-07-09 | NSE | ICICIBANK | train | 858 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=ICICIBANK\event_surprise_conditional_labels.parquet | 16690 | 0 |
| 15 | 2026-07-09 | NSE | INFY | train | 858 | 2 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=INFY\event_surprise_conditional_labels.parquet | 16712 | 0 |
| 15 | 2026-07-09 | NSE | ITBEES | train | 859 | 85 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=ITBEES\event_surprise_conditional_labels.parquet | 17248 | 0 |
| 15 | 2026-07-09 | NSE | ITC | train | 858 | 4 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=ITC\event_surprise_conditional_labels.parquet | 16739 | 0 |
| 15 | 2026-07-09 | NSE | JUNIORBEES | train | 859 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=JUNIORBEES\event_surprise_conditional_labels.parquet | 16687 | 0 |
| 15 | 2026-07-09 | NSE | KOTAKBANK | train | 858 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=KOTAKBANK\event_surprise_conditional_labels.parquet | 16682 | 0 |
| 15 | 2026-07-09 | NSE | LT | train | 858 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=LT\event_surprise_conditional_labels.parquet | 16536 | 0 |
| 15 | 2026-07-09 | NSE | M&M | train | 858 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=M&M\event_surprise_conditional_labels.parquet | 16652 | 0 |
| 15 | 2026-07-09 | NSE | MARUTI | train | 858 | 3 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=MARUTI\event_surprise_conditional_labels.parquet | 16769 | 0 |
| 15 | 2026-07-09 | NSE | NESTLEIND | train | 858 | 10 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=NESTLEIND\event_surprise_conditional_labels.parquet | 16841 | 0 |
| 15 | 2026-07-09 | NSE | NIFTYBEES | train | 859 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=NIFTYBEES\event_surprise_conditional_labels.parquet | 16690 | 0 |
| 15 | 2026-07-09 | NSE | ONGC | train | 858 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=ONGC\event_surprise_conditional_labels.parquet | 16697 | 0 |
| 15 | 2026-07-09 | NSE | RELIANCE | train | 858 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=RELIANCE\event_surprise_conditional_labels.parquet | 16571 | 0 |
| 15 | 2026-07-09 | NSE | SBIN | train | 858 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=SBIN\event_surprise_conditional_labels.parquet | 16663 | 0 |
| 15 | 2026-07-09 | NSE | SUNPHARMA | train | 858 | 90 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=SUNPHARMA\event_surprise_conditional_labels.parquet | 17187 | 0 |
| 15 | 2026-07-09 | NSE | TCS | train | 858 | 10 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=TCS\event_surprise_conditional_labels.parquet | 16839 | 0 |
| 15 | 2026-07-09 | NSE | TECHM | train | 858 | 43 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=TECHM\event_surprise_conditional_labels.parquet | 17048 | 0 |
| 15 | 2026-07-09 | NSE | ULTRACEMCO | train | 858 | 2 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=ULTRACEMCO\event_surprise_conditional_labels.parquet | 16732 | 0 |
| 15 | 2026-07-09 | NSE | WIPRO | train | 858 | 180 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=WIPRO\event_surprise_conditional_labels.parquet | 17252 | 0 |
| 15 | 2026-07-10 | NSE | ADANIPORTS | train | 1502 | 2 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=ADANIPORTS\event_surprise_conditional_labels.parquet | 21781 | 0 |
| 15 | 2026-07-10 | NSE | AXISBANK | train | 1502 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=AXISBANK\event_surprise_conditional_labels.parquet | 21719 | 0 |
| 15 | 2026-07-10 | NSE | BAJAJ-AUTO | train | 1502 | 7 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=BAJAJ-AUTO\event_surprise_conditional_labels.parquet | 21887 | 0 |
| 15 | 2026-07-10 | NSE | BANKBEES | train | 1501 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=BANKBEES\event_surprise_conditional_labels.parquet | 21705 | 0 |
| 15 | 2026-07-10 | NSE | BHARTIARTL | train | 1502 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=BHARTIARTL\event_surprise_conditional_labels.parquet | 21725 | 0 |
| 15 | 2026-07-10 | NSE | BPCL | train | 1502 | 5 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=BPCL\event_surprise_conditional_labels.parquet | 21756 | 0 |
| 15 | 2026-07-10 | NSE | BRITANNIA | train | 1501 | 70 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=BRITANNIA\event_surprise_conditional_labels.parquet | 22240 | 0 |
| 15 | 2026-07-10 | NSE | CIPLA | train | 1502 | 9 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=CIPLA\event_surprise_conditional_labels.parquet | 21864 | 0 |
| 15 | 2026-07-10 | NSE | DRREDDY | train | 1502 | 2 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=DRREDDY\event_surprise_conditional_labels.parquet | 21799 | 0 |
| 15 | 2026-07-10 | NSE | GOLDBEES | train | 1501 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=GOLDBEES\event_surprise_conditional_labels.parquet | 21708 | 0 |
| 15 | 2026-07-10 | NSE | HCLTECH | train | 1502 | 131 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=HCLTECH\event_surprise_conditional_labels.parquet | 22671 | 0 |
| 15 | 2026-07-10 | NSE | HDFCBANK | train | 1502 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=HDFCBANK\event_surprise_conditional_labels.parquet | 21753 | 0 |
| 15 | 2026-07-10 | NSE | HINDUNILVR | train | 1502 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=HINDUNILVR\event_surprise_conditional_labels.parquet | 21523 | 0 |
| 15 | 2026-07-10 | NSE | ICICIBANK | train | 1502 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=ICICIBANK\event_surprise_conditional_labels.parquet | 21717 | 0 |
| 15 | 2026-07-10 | NSE | INFY | train | 1501 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=INFY\event_surprise_conditional_labels.parquet | 21734 | 0 |
| 15 | 2026-07-10 | NSE | ITBEES | train | 1501 | 56 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=ITBEES\event_surprise_conditional_labels.parquet | 21507 | 0 |
| 15 | 2026-07-10 | NSE | ITC | train | 1502 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=ITC\event_surprise_conditional_labels.parquet | 21680 | 0 |
| 15 | 2026-07-10 | NSE | JUNIORBEES | train | 1500 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=JUNIORBEES\event_surprise_conditional_labels.parquet | 21704 | 0 |
| 15 | 2026-07-10 | NSE | KOTAKBANK | train | 1502 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=KOTAKBANK\event_surprise_conditional_labels.parquet | 21723 | 0 |
| 15 | 2026-07-10 | NSE | LT | train | 1502 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=LT\event_surprise_conditional_labels.parquet | 21496 | 0 |
| 15 | 2026-07-10 | NSE | M&M | train | 1502 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=M&M\event_surprise_conditional_labels.parquet | 21691 | 0 |
| 15 | 2026-07-10 | NSE | MARUTI | train | 1502 | 2 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=MARUTI\event_surprise_conditional_labels.parquet | 21744 | 0 |
| 15 | 2026-07-10 | NSE | NESTLEIND | train | 1502 | 21 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=NESTLEIND\event_surprise_conditional_labels.parquet | 22033 | 0 |
| 15 | 2026-07-10 | NSE | NIFTYBEES | train | 1501 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=NIFTYBEES\event_surprise_conditional_labels.parquet | 21716 | 0 |
| 15 | 2026-07-10 | NSE | ONGC | train | 1502 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=ONGC\event_surprise_conditional_labels.parquet | 21732 | 0 |
| 15 | 2026-07-10 | NSE | RELIANCE | train | 1501 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=RELIANCE\event_surprise_conditional_labels.parquet | 21510 | 0 |
| 15 | 2026-07-10 | NSE | SBIN | train | 1502 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=SBIN\event_surprise_conditional_labels.parquet | 21731 | 0 |
| 15 | 2026-07-10 | NSE | SUNPHARMA | train | 1502 | 2 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=SUNPHARMA\event_surprise_conditional_labels.parquet | 21792 | 0 |
| 15 | 2026-07-10 | NSE | TCS | train | 1501 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=TCS\event_surprise_conditional_labels.parquet | 21740 | 0 |
| 15 | 2026-07-10 | NSE | TECHM | train | 1502 | 28 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=TECHM\event_surprise_conditional_labels.parquet | 22222 | 0 |
| 15 | 2026-07-10 | NSE | ULTRACEMCO | train | 1501 | 28 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=ULTRACEMCO\event_surprise_conditional_labels.parquet | 22025 | 0 |
| 15 | 2026-07-10 | NSE | WIPRO | train | 1502 | 61 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=WIPRO\event_surprise_conditional_labels.parquet | 22125 | 0 |
| 15 | 2026-07-13 | NSE | ADANIPORTS | validation | 1502 | 6 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=ADANIPORTS\event_surprise_conditional_labels.parquet | 21902 | 0 |
| 15 | 2026-07-13 | NSE | AXISBANK | validation | 1502 | 3 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=AXISBANK\event_surprise_conditional_labels.parquet | 21862 | 0 |
| 15 | 2026-07-13 | NSE | BAJAJ-AUTO | validation | 1502 | 66 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=BAJAJ-AUTO\event_surprise_conditional_labels.parquet | 22413 | 0 |
| 15 | 2026-07-13 | NSE | BANKBEES | validation | 1502 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=BANKBEES\event_surprise_conditional_labels.parquet | 21743 | 0 |
| 15 | 2026-07-13 | NSE | BHARTIARTL | validation | 1502 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=BHARTIARTL\event_surprise_conditional_labels.parquet | 21805 | 0 |
| 15 | 2026-07-13 | NSE | BPCL | validation | 1502 | 47 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=BPCL\event_surprise_conditional_labels.parquet | 22149 | 0 |
| 15 | 2026-07-13 | NSE | BRITANNIA | validation | 1502 | 77 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=BRITANNIA\event_surprise_conditional_labels.parquet | 22309 | 0 |
| 15 | 2026-07-13 | NSE | CIPLA | validation | 1502 | 22 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=CIPLA\event_surprise_conditional_labels.parquet | 22099 | 0 |
| 15 | 2026-07-13 | NSE | DRREDDY | validation | 1502 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=DRREDDY\event_surprise_conditional_labels.parquet | 21792 | 0 |
| 15 | 2026-07-13 | NSE | GOLDBEES | validation | 1502 | 4 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=GOLDBEES\event_surprise_conditional_labels.parquet | 21872 | 0 |
| 15 | 2026-07-13 | NSE | HCLTECH | validation | 1502 | 179 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=HCLTECH\event_surprise_conditional_labels.parquet | 22742 | 0 |
| 15 | 2026-07-13 | NSE | HDFCBANK | validation | 1502 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=HDFCBANK\event_surprise_conditional_labels.parquet | 21776 | 0 |
| 15 | 2026-07-13 | NSE | HINDUNILVR | validation | 1502 | 4 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=HINDUNILVR\event_surprise_conditional_labels.parquet | 21860 | 0 |
| 15 | 2026-07-13 | NSE | ICICIBANK | validation | 1502 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=ICICIBANK\event_surprise_conditional_labels.parquet | 21807 | 0 |
| 15 | 2026-07-13 | NSE | INFY | validation | 1502 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=INFY\event_surprise_conditional_labels.parquet | 21773 | 0 |
| 15 | 2026-07-13 | NSE | ITBEES | validation | 1502 | 151 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=ITBEES\event_surprise_conditional_labels.parquet | 22509 | 0 |
| 15 | 2026-07-13 | NSE | ITC | validation | 1502 | 2 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=ITC\event_surprise_conditional_labels.parquet | 21696 | 0 |
| 15 | 2026-07-13 | NSE | JUNIORBEES | validation | 1502 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=JUNIORBEES\event_surprise_conditional_labels.parquet | 21737 | 0 |
| 15 | 2026-07-13 | NSE | KOTAKBANK | validation | 1502 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=KOTAKBANK\event_surprise_conditional_labels.parquet | 21736 | 0 |
| 15 | 2026-07-13 | NSE | LT | validation | 1502 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=LT\event_surprise_conditional_labels.parquet | 21763 | 0 |
| 15 | 2026-07-13 | NSE | M&M | validation | 1502 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=M&M\event_surprise_conditional_labels.parquet | 21718 | 0 |
| 15 | 2026-07-13 | NSE | MARUTI | validation | 1502 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=MARUTI\event_surprise_conditional_labels.parquet | 21790 | 0 |
| 15 | 2026-07-13 | NSE | NESTLEIND | validation | 1502 | 31 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=NESTLEIND\event_surprise_conditional_labels.parquet | 22078 | 0 |
| 15 | 2026-07-13 | NSE | NIFTYBEES | validation | 1502 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=NIFTYBEES\event_surprise_conditional_labels.parquet | 21818 | 0 |
| 15 | 2026-07-13 | NSE | ONGC | validation | 1502 | 6 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=ONGC\event_surprise_conditional_labels.parquet | 21876 | 0 |
| 15 | 2026-07-13 | NSE | RELIANCE | validation | 1502 | 4 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=RELIANCE\event_surprise_conditional_labels.parquet | 21864 | 0 |
| 15 | 2026-07-13 | NSE | SBIN | validation | 1502 | 2 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=SBIN\event_surprise_conditional_labels.parquet | 21816 | 0 |
| 15 | 2026-07-13 | NSE | SUNPHARMA | validation | 1502 | 3 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=SUNPHARMA\event_surprise_conditional_labels.parquet | 21852 | 0 |
| 15 | 2026-07-13 | NSE | TCS | validation | 1502 | 3 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=TCS\event_surprise_conditional_labels.parquet | 21835 | 0 |
| 15 | 2026-07-13 | NSE | TECHM | validation | 1502 | 106 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=TECHM\event_surprise_conditional_labels.parquet | 22576 | 0 |
| 15 | 2026-07-13 | NSE | ULTRACEMCO | validation | 1502 | 29 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=ULTRACEMCO\event_surprise_conditional_labels.parquet | 22113 | 0 |
| 15 | 2026-07-13 | NSE | WIPRO | validation | 1502 | 92 | derived_phase214_event_surprise_conditional_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=WIPRO\event_surprise_conditional_labels.parquet | 22337 | 0 |
| 60 | 2026-07-08 | NSE | ADANIPORTS | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=ADANIPORTS\event_surprise_conditional_labels.parquet | 11414 | 0 |
| 60 | 2026-07-08 | NSE | AXISBANK | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=AXISBANK\event_surprise_conditional_labels.parquet | 11404 | 0 |
| 60 | 2026-07-08 | NSE | BAJAJ-AUTO | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=BAJAJ-AUTO\event_surprise_conditional_labels.parquet | 11414 | 0 |
| 60 | 2026-07-08 | NSE | BANKBEES | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=BANKBEES\event_surprise_conditional_labels.parquet | 11376 | 0 |
| 60 | 2026-07-08 | NSE | BHARTIARTL | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=BHARTIARTL\event_surprise_conditional_labels.parquet | 11413 | 0 |
| 60 | 2026-07-08 | NSE | BPCL | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=BPCL\event_surprise_conditional_labels.parquet | 11383 | 0 |
| 60 | 2026-07-08 | NSE | BRITANNIA | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=BRITANNIA\event_surprise_conditional_labels.parquet | 11410 | 0 |
| 60 | 2026-07-08 | NSE | CIPLA | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=CIPLA\event_surprise_conditional_labels.parquet | 11361 | 0 |
| 60 | 2026-07-08 | NSE | DRREDDY | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=DRREDDY\event_surprise_conditional_labels.parquet | 11376 | 0 |
| 60 | 2026-07-08 | NSE | GOLDBEES | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=GOLDBEES\event_surprise_conditional_labels.parquet | 11404 | 0 |
| 60 | 2026-07-08 | NSE | HCLTECH | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=HCLTECH\event_surprise_conditional_labels.parquet | 11378 | 0 |
| 60 | 2026-07-08 | NSE | HDFCBANK | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=HDFCBANK\event_surprise_conditional_labels.parquet | 11404 | 0 |
| 60 | 2026-07-08 | NSE | HINDUNILVR | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=HINDUNILVR\event_surprise_conditional_labels.parquet | 11391 | 0 |
| 60 | 2026-07-08 | NSE | ICICIBANK | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=ICICIBANK\event_surprise_conditional_labels.parquet | 11411 | 0 |
| 60 | 2026-07-08 | NSE | INFY | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=INFY\event_surprise_conditional_labels.parquet | 11384 | 0 |
| 60 | 2026-07-08 | NSE | ITBEES | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=ITBEES\event_surprise_conditional_labels.parquet | 11393 | 0 |
| 60 | 2026-07-08 | NSE | ITC | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=ITC\event_surprise_conditional_labels.parquet | 11379 | 0 |
| 60 | 2026-07-08 | NSE | JUNIORBEES | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=JUNIORBEES\event_surprise_conditional_labels.parquet | 11386 | 0 |
| 60 | 2026-07-08 | NSE | KOTAKBANK | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=KOTAKBANK\event_surprise_conditional_labels.parquet | 11289 | 0 |
| 60 | 2026-07-08 | NSE | LT | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=LT\event_surprise_conditional_labels.parquet | 11350 | 0 |
| 60 | 2026-07-08 | NSE | M&M | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=M&M\event_surprise_conditional_labels.parquet | 11351 | 0 |
| 60 | 2026-07-08 | NSE | MARUTI | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=MARUTI\event_surprise_conditional_labels.parquet | 11395 | 0 |
| 60 | 2026-07-08 | NSE | NESTLEIND | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=NESTLEIND\event_surprise_conditional_labels.parquet | 11409 | 0 |
| 60 | 2026-07-08 | NSE | NIFTYBEES | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=NIFTYBEES\event_surprise_conditional_labels.parquet | 11409 | 0 |
| 60 | 2026-07-08 | NSE | ONGC | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=ONGC\event_surprise_conditional_labels.parquet | 11386 | 0 |
| 60 | 2026-07-08 | NSE | RELIANCE | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=RELIANCE\event_surprise_conditional_labels.parquet | 11383 | 0 |
| 60 | 2026-07-08 | NSE | SBIN | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=SBIN\event_surprise_conditional_labels.parquet | 11384 | 0 |
| 60 | 2026-07-08 | NSE | SUNPHARMA | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=SUNPHARMA\event_surprise_conditional_labels.parquet | 11381 | 0 |
| 60 | 2026-07-08 | NSE | TCS | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=TCS\event_surprise_conditional_labels.parquet | 11356 | 0 |
| 60 | 2026-07-08 | NSE | TECHM | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=TECHM\event_surprise_conditional_labels.parquet | 11367 | 0 |
| 60 | 2026-07-08 | NSE | ULTRACEMCO | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=ULTRACEMCO\event_surprise_conditional_labels.parquet | 11414 | 0 |
| 60 | 2026-07-08 | NSE | WIPRO | train | 147 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-08\exchange=NSE\symbol=WIPRO\event_surprise_conditional_labels.parquet | 11362 | 0 |
| 60 | 2026-07-09 | NSE | ADANIPORTS | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=ADANIPORTS\event_surprise_conditional_labels.parquet | 11954 | 0 |
| 60 | 2026-07-09 | NSE | AXISBANK | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=AXISBANK\event_surprise_conditional_labels.parquet | 11944 | 0 |
| 60 | 2026-07-09 | NSE | BAJAJ-AUTO | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=BAJAJ-AUTO\event_surprise_conditional_labels.parquet | 11956 | 0 |
| 60 | 2026-07-09 | NSE | BANKBEES | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=BANKBEES\event_surprise_conditional_labels.parquet | 11908 | 0 |
| 60 | 2026-07-09 | NSE | BHARTIARTL | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=BHARTIARTL\event_surprise_conditional_labels.parquet | 11954 | 0 |
| 60 | 2026-07-09 | NSE | BPCL | train | 216 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=BPCL\event_surprise_conditional_labels.parquet | 11953 | 0 |
| 60 | 2026-07-09 | NSE | BRITANNIA | train | 215 | 20 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=BRITANNIA\event_surprise_conditional_labels.parquet | 12127 | 0 |
| 60 | 2026-07-09 | NSE | CIPLA | train | 216 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=CIPLA\event_surprise_conditional_labels.parquet | 11930 | 0 |
| 60 | 2026-07-09 | NSE | DRREDDY | train | 216 | 143 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=DRREDDY\event_surprise_conditional_labels.parquet | 12150 | 0 |
| 60 | 2026-07-09 | NSE | GOLDBEES | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=GOLDBEES\event_surprise_conditional_labels.parquet | 11944 | 0 |
| 60 | 2026-07-09 | NSE | HCLTECH | train | 216 | 21 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=HCLTECH\event_surprise_conditional_labels.parquet | 12120 | 0 |
| 60 | 2026-07-09 | NSE | HDFCBANK | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=HDFCBANK\event_surprise_conditional_labels.parquet | 11944 | 0 |
| 60 | 2026-07-09 | NSE | HINDUNILVR | train | 216 | 3 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=HINDUNILVR\event_surprise_conditional_labels.parquet | 12047 | 0 |
| 60 | 2026-07-09 | NSE | ICICIBANK | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=ICICIBANK\event_surprise_conditional_labels.parquet | 11949 | 0 |
| 60 | 2026-07-09 | NSE | INFY | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=INFY\event_surprise_conditional_labels.parquet | 11924 | 0 |
| 60 | 2026-07-09 | NSE | ITBEES | train | 216 | 5 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=ITBEES\event_surprise_conditional_labels.parquet | 12044 | 0 |
| 60 | 2026-07-09 | NSE | ITC | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=ITC\event_surprise_conditional_labels.parquet | 11921 | 0 |
| 60 | 2026-07-09 | NSE | JUNIORBEES | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=JUNIORBEES\event_surprise_conditional_labels.parquet | 11922 | 0 |
| 60 | 2026-07-09 | NSE | KOTAKBANK | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=KOTAKBANK\event_surprise_conditional_labels.parquet | 11949 | 0 |
| 60 | 2026-07-09 | NSE | LT | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=LT\event_surprise_conditional_labels.parquet | 11882 | 0 |
| 60 | 2026-07-09 | NSE | M&M | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=M&M\event_surprise_conditional_labels.parquet | 11883 | 0 |
| 60 | 2026-07-09 | NSE | MARUTI | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=MARUTI\event_surprise_conditional_labels.parquet | 11936 | 0 |
| 60 | 2026-07-09 | NSE | NESTLEIND | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=NESTLEIND\event_surprise_conditional_labels.parquet | 11951 | 0 |
| 60 | 2026-07-09 | NSE | NIFTYBEES | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=NIFTYBEES\event_surprise_conditional_labels.parquet | 11949 | 0 |
| 60 | 2026-07-09 | NSE | ONGC | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=ONGC\event_surprise_conditional_labels.parquet | 11924 | 0 |
| 60 | 2026-07-09 | NSE | RELIANCE | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=RELIANCE\event_surprise_conditional_labels.parquet | 11913 | 0 |
| 60 | 2026-07-09 | NSE | SBIN | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=SBIN\event_surprise_conditional_labels.parquet | 11924 | 0 |
| 60 | 2026-07-09 | NSE | SUNPHARMA | train | 216 | 10 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=SUNPHARMA\event_surprise_conditional_labels.parquet | 12069 | 0 |
| 60 | 2026-07-09 | NSE | TCS | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=TCS\event_surprise_conditional_labels.parquet | 11888 | 0 |
| 60 | 2026-07-09 | NSE | TECHM | train | 216 | 6 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=TECHM\event_surprise_conditional_labels.parquet | 12047 | 0 |
| 60 | 2026-07-09 | NSE | ULTRACEMCO | train | 216 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=ULTRACEMCO\event_surprise_conditional_labels.parquet | 11957 | 0 |
| 60 | 2026-07-09 | NSE | WIPRO | train | 216 | 42 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-09\exchange=NSE\symbol=WIPRO\event_surprise_conditional_labels.parquet | 12091 | 0 |
| 60 | 2026-07-10 | NSE | ADANIPORTS | train | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=ADANIPORTS\event_surprise_conditional_labels.parquet | 13328 | 0 |
| 60 | 2026-07-10 | NSE | AXISBANK | train | 377 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=AXISBANK\event_surprise_conditional_labels.parquet | 13284 | 0 |
| 60 | 2026-07-10 | NSE | BAJAJ-AUTO | train | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=BAJAJ-AUTO\event_surprise_conditional_labels.parquet | 13327 | 0 |
| 60 | 2026-07-10 | NSE | BANKBEES | train | 376 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=BANKBEES\event_surprise_conditional_labels.parquet | 13207 | 0 |
| 60 | 2026-07-10 | NSE | BHARTIARTL | train | 377 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=BHARTIARTL\event_surprise_conditional_labels.parquet | 13297 | 0 |
| 60 | 2026-07-10 | NSE | BPCL | train | 377 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=BPCL\event_surprise_conditional_labels.parquet | 13260 | 0 |
| 60 | 2026-07-10 | NSE | BRITANNIA | train | 377 | 3 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=BRITANNIA\event_surprise_conditional_labels.parquet | 13376 | 0 |
| 60 | 2026-07-10 | NSE | CIPLA | train | 377 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=CIPLA\event_surprise_conditional_labels.parquet | 13212 | 0 |
| 60 | 2026-07-10 | NSE | DRREDDY | train | 377 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=DRREDDY\event_surprise_conditional_labels.parquet | 13229 | 0 |
| 60 | 2026-07-10 | NSE | GOLDBEES | train | 376 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=GOLDBEES\event_surprise_conditional_labels.parquet | 13295 | 0 |
| 60 | 2026-07-10 | NSE | HCLTECH | train | 377 | 8 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=HCLTECH\event_surprise_conditional_labels.parquet | 13402 | 0 |
| 60 | 2026-07-10 | NSE | HDFCBANK | train | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=HDFCBANK\event_surprise_conditional_labels.parquet | 13317 | 0 |
| 60 | 2026-07-10 | NSE | HINDUNILVR | train | 377 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=HINDUNILVR\event_surprise_conditional_labels.parquet | 13243 | 0 |
| 60 | 2026-07-10 | NSE | ICICIBANK | train | 377 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=ICICIBANK\event_surprise_conditional_labels.parquet | 13292 | 0 |
| 60 | 2026-07-10 | NSE | INFY | train | 376 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=INFY\event_surprise_conditional_labels.parquet | 13242 | 0 |
| 60 | 2026-07-10 | NSE | ITBEES | train | 376 | 3 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=ITBEES\event_surprise_conditional_labels.parquet | 13070 | 0 |
| 60 | 2026-07-10 | NSE | ITC | train | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=ITC\event_surprise_conditional_labels.parquet | 13287 | 0 |
| 60 | 2026-07-10 | NSE | JUNIORBEES | train | 375 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=JUNIORBEES\event_surprise_conditional_labels.parquet | 13212 | 0 |
| 60 | 2026-07-10 | NSE | KOTAKBANK | train | 377 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=KOTAKBANK\event_surprise_conditional_labels.parquet | 13289 | 0 |
| 60 | 2026-07-10 | NSE | LT | train | 377 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=LT\event_surprise_conditional_labels.parquet | 13202 | 0 |
| 60 | 2026-07-10 | NSE | M&M | train | 377 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=M&M\event_surprise_conditional_labels.parquet | 13203 | 0 |
| 60 | 2026-07-10 | NSE | MARUTI | train | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=MARUTI\event_surprise_conditional_labels.parquet | 13307 | 0 |
| 60 | 2026-07-10 | NSE | NESTLEIND | train | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=NESTLEIND\event_surprise_conditional_labels.parquet | 13327 | 0 |
| 60 | 2026-07-10 | NSE | NIFTYBEES | train | 376 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=NIFTYBEES\event_surprise_conditional_labels.parquet | 13267 | 0 |
| 60 | 2026-07-10 | NSE | ONGC | train | 377 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=ONGC\event_surprise_conditional_labels.parquet | 13265 | 0 |
| 60 | 2026-07-10 | NSE | RELIANCE | train | 376 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=RELIANCE\event_surprise_conditional_labels.parquet | 13215 | 0 |
| 60 | 2026-07-10 | NSE | SBIN | train | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=SBIN\event_surprise_conditional_labels.parquet | 13297 | 0 |
| 60 | 2026-07-10 | NSE | SUNPHARMA | train | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=SUNPHARMA\event_surprise_conditional_labels.parquet | 13286 | 0 |
| 60 | 2026-07-10 | NSE | TCS | train | 376 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=TCS\event_surprise_conditional_labels.parquet | 13187 | 0 |
| 60 | 2026-07-10 | NSE | TECHM | train | 377 | 2 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=TECHM\event_surprise_conditional_labels.parquet | 13338 | 0 |
| 60 | 2026-07-10 | NSE | ULTRACEMCO | train | 377 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=ULTRACEMCO\event_surprise_conditional_labels.parquet | 13290 | 0 |
| 60 | 2026-07-10 | NSE | WIPRO | train | 377 | 8 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-10\exchange=NSE\symbol=WIPRO\event_surprise_conditional_labels.parquet | 13399 | 0 |
| 60 | 2026-07-13 | NSE | ADANIPORTS | validation | 377 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=ADANIPORTS\event_surprise_conditional_labels.parquet | 13320 | 0 |
| 60 | 2026-07-13 | NSE | AXISBANK | validation | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=AXISBANK\event_surprise_conditional_labels.parquet | 13371 | 0 |
| 60 | 2026-07-13 | NSE | BAJAJ-AUTO | validation | 377 | 6 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=BAJAJ-AUTO\event_surprise_conditional_labels.parquet | 13442 | 0 |
| 60 | 2026-07-13 | NSE | BANKBEES | validation | 376 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=BANKBEES\event_surprise_conditional_labels.parquet | 13233 | 0 |
| 60 | 2026-07-13 | NSE | BHARTIARTL | validation | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=BHARTIARTL\event_surprise_conditional_labels.parquet | 13378 | 0 |
| 60 | 2026-07-13 | NSE | BPCL | validation | 377 | 4 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=BPCL\event_surprise_conditional_labels.parquet | 13390 | 0 |
| 60 | 2026-07-13 | NSE | BRITANNIA | validation | 377 | 3 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=BRITANNIA\event_surprise_conditional_labels.parquet | 13419 | 0 |
| 60 | 2026-07-13 | NSE | CIPLA | validation | 377 | 2 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=CIPLA\event_surprise_conditional_labels.parquet | 13336 | 0 |
| 60 | 2026-07-13 | NSE | DRREDDY | validation | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=DRREDDY\event_surprise_conditional_labels.parquet | 13352 | 0 |
| 60 | 2026-07-13 | NSE | GOLDBEES | validation | 376 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=GOLDBEES\event_surprise_conditional_labels.parquet | 13286 | 0 |
| 60 | 2026-07-13 | NSE | HCLTECH | validation | 377 | 15 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=HCLTECH\event_surprise_conditional_labels.parquet | 13503 | 0 |
| 60 | 2026-07-13 | NSE | HDFCBANK | validation | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=HDFCBANK\event_surprise_conditional_labels.parquet | 13340 | 0 |
| 60 | 2026-07-13 | NSE | HINDUNILVR | validation | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=HINDUNILVR\event_surprise_conditional_labels.parquet | 13377 | 0 |
| 60 | 2026-07-13 | NSE | ICICIBANK | validation | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=ICICIBANK\event_surprise_conditional_labels.parquet | 13379 | 0 |
| 60 | 2026-07-13 | NSE | INFY | validation | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=INFY\event_surprise_conditional_labels.parquet | 13350 | 0 |
| 60 | 2026-07-13 | NSE | ITBEES | validation | 376 | 24 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=ITBEES\event_surprise_conditional_labels.parquet | 13502 | 0 |
| 60 | 2026-07-13 | NSE | ITC | validation | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=ITC\event_surprise_conditional_labels.parquet | 13338 | 0 |
| 60 | 2026-07-13 | NSE | JUNIORBEES | validation | 376 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=JUNIORBEES\event_surprise_conditional_labels.parquet | 13242 | 0 |
| 60 | 2026-07-13 | NSE | KOTAKBANK | validation | 377 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=KOTAKBANK\event_surprise_conditional_labels.parquet | 13312 | 0 |
| 60 | 2026-07-13 | NSE | LT | validation | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=LT\event_surprise_conditional_labels.parquet | 13337 | 0 |
| 60 | 2026-07-13 | NSE | M&M | validation | 377 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=M&M\event_surprise_conditional_labels.parquet | 13228 | 0 |
| 60 | 2026-07-13 | NSE | MARUTI | validation | 377 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=MARUTI\event_surprise_conditional_labels.parquet | 13299 | 0 |
| 60 | 2026-07-13 | NSE | NESTLEIND | validation | 377 | 5 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=NESTLEIND\event_surprise_conditional_labels.parquet | 13397 | 0 |
| 60 | 2026-07-13 | NSE | NIFTYBEES | validation | 376 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=NIFTYBEES\event_surprise_conditional_labels.parquet | 13293 | 0 |
| 60 | 2026-07-13 | NSE | ONGC | validation | 377 | 0 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=ONGC\event_surprise_conditional_labels.parquet | 13289 | 0 |
| 60 | 2026-07-13 | NSE | RELIANCE | validation | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=RELIANCE\event_surprise_conditional_labels.parquet | 13370 | 0 |
| 60 | 2026-07-13 | NSE | SBIN | validation | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=SBIN\event_surprise_conditional_labels.parquet | 13350 | 0 |
| 60 | 2026-07-13 | NSE | SUNPHARMA | validation | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=SUNPHARMA\event_surprise_conditional_labels.parquet | 13310 | 0 |
| 60 | 2026-07-13 | NSE | TCS | validation | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=TCS\event_surprise_conditional_labels.parquet | 13342 | 0 |
| 60 | 2026-07-13 | NSE | TECHM | validation | 377 | 13 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=TECHM\event_surprise_conditional_labels.parquet | 13503 | 0 |
| 60 | 2026-07-13 | NSE | ULTRACEMCO | validation | 377 | 1 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=ULTRACEMCO\event_surprise_conditional_labels.parquet | 13378 | 0 |
| 60 | 2026-07-13 | NSE | WIPRO | validation | 377 | 8 | derived_phase214_event_surprise_conditional_labels\horizon=60s\trade_date=2026-07-13\exchange=NSE\symbol=WIPRO\event_surprise_conditional_labels.parquet | 13431 | 0 |

## Label Partition Quality

| horizon_sec | trade_date | exchange | symbol | split_role | rows | event_surprise_rows | up_positive_rate | down_positive_rate | vol_expansion_positive_rate | min_baseline_rows | fallback_baseline_rows | sparse_event_surprise_partition | quality_pass | model_fit_allowed | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-07-08 | NSE | ADANIPORTS | train | 3617 | 0 | 0 | 0 | 0 | 1381 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | AXISBANK | train | 5829 | 0 | 0 | 0 | 0 | 1626 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | BAJAJ-AUTO | train | 3323 | 0 | 0 | 0 | 0 | 1430 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | BANKBEES | train | 5645 | 0 | 0 | 0 | 0 | 2279 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | BHARTIARTL | train | 3952 | 0 | 0 | 0 | 0 | 1585 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | BPCL | train | 2852 | 0 | 0 | 0 | 0 | 827 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | BRITANNIA | train | 2151 | 0 | 0 | 0 | 0 | 789 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | CIPLA | train | 2953 | 0 | 0 | 0 | 0 | 1049 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | DRREDDY | train | 2935 | 0 | 0 | 0 | 0 | 1257 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | GOLDBEES | train | 4078 | 0 | 0 | 0 | 0 | 1287 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | HCLTECH | train | 2706 | 0 | 0 | 0 | 0 | 1301 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | HDFCBANK | train | 6816 | 0 | 0 | 0 | 0 | 2462 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | HINDUNILVR | train | 3470 | 0 | 0 | 0 | 0 | 1603 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | ICICIBANK | train | 6210 | 0 | 0 | 0 | 0 | 1979 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | INFY | train | 5152 | 0 | 0 | 0 | 0 | 1933 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | ITBEES | train | 2355 | 0 | 0 | 0 | 0 | 3211 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | ITC | train | 4271 | 0 | 0 | 0 | 0 | 818 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | JUNIORBEES | train | 5241 | 0 | 0 | 0 | 0 | 2488 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | KOTAKBANK | train | 4944 | 0 | 0 | 0 | 0 | 1346 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | LT | train | 6328 | 0 | 0 | 0 | 0 | 2369 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | M&M | train | 6037 | 0 | 0 | 0 | 0 | 2021 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | MARUTI | train | 4917 | 0 | 0 | 0 | 0 | 1584 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | NESTLEIND | train | 2943 | 0 | 0 | 0 | 0 | 1150 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | NIFTYBEES | train | 5016 | 0 | 0 | 0 | 0 | 1770 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | ONGC | train | 4121 | 0 | 0 | 0 | 0 | 1651 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | RELIANCE | train | 6547 | 0 | 0 | 0 | 0 | 1512 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | SBIN | train | 5499 | 0 | 0 | 0 | 0 | 1314 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | SUNPHARMA | train | 3352 | 0 | 0 | 0 | 0 | 1520 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | TCS | train | 3904 | 0 | 0 | 0 | 0 | 1835 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | TECHM | train | 2802 | 0 | 0 | 0 | 0 | 862 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | ULTRACEMCO | train | 3043 | 0 | 0 | 0 | 0 | 778 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | WIPRO | train | 2625 | 0 | 0 | 0 | 0 | 1426 | 0 | 1 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | ADANIPORTS | train | 5553 | 509 | 0.0144066 | 0.0145867 | 0.0291734 | 94 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | AXISBANK | train | 7446 | 529 | 0.0123556 | 0.0128928 | 0.0253828 | 79 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | BAJAJ-AUTO | train | 5049 | 328 | 0.00851654 | 0.0126758 | 0.0215884 | 94 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | BANKBEES | train | 8885 | 855 | 0.0275746 | 0.0267867 | 0.0535734 | 138 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | BHARTIARTL | train | 9411 | 960 | 0.0310275 | 0.0248645 | 0.0547232 | 125 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | BPCL | train | 4696 | 365 | 0.0100085 | 0.0104344 | 0.0204429 | 43 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | BRITANNIA | train | 4229 | 909 | 0.043982 | 0.0446914 | 0.0900922 | 132 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | CIPLA | train | 4886 | 421 | 0.00675399 | 0.00695866 | 0.014122 | 66 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | DRREDDY | train | 9053 | 5218 | 0.126588 | 0.108583 | 0.237601 | 515 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | GOLDBEES | train | 6407 | 590 | 0.0104573 | 0.00998907 | 0.0204464 | 77 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | HCLTECH | train | 5477 | 1575 | 0.042359 | 0.0447325 | 0.0878218 | 176 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | HDFCBANK | train | 9419 | 866 | 0.021446 | 0.0215522 | 0.0433167 | 179 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | HINDUNILVR | train | 6946 | 659 | 0.0218831 | 0.0201555 | 0.0417506 | 96 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | ICICIBANK | train | 9152 | 822 | 0.0196678 | 0.0215253 | 0.0409747 | 115 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | INFY | train | 7566 | 541 | 0.01401 | 0.0144066 | 0.0285488 | 135 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | ITBEES | train | 3872 | 705 | 0.0173037 | 0.0157541 | 0.0335744 | 6 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | ITC | train | 7309 | 789 | 0.0102613 | 0.0109454 | 0.0216172 | 67 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | JUNIORBEES | train | 8589 | 815 | 0.0312027 | 0.0279427 | 0.059029 | 185 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | KOTAKBANK | train | 8943 | 760 | 0.0124119 | 0.0159902 | 0.0285139 | 72 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | LT | train | 9072 | 805 | 0.0203924 | 0.0224868 | 0.0429894 | 125 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | M&M | train | 7704 | 592 | 0.0138889 | 0.0189512 | 0.0332295 | 91 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | MARUTI | train | 7379 | 729 | 0.0181596 | 0.0140941 | 0.0321182 | 102 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | NESTLEIND | train | 4454 | 287 | 0.0123485 | 0.0159407 | 0.0282892 | 59 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | NIFTYBEES | train | 8019 | 657 | 0.0119716 | 0.00997631 | 0.0220726 | 107 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | ONGC | train | 5782 | 543 | 0.0169492 | 0.0110688 | 0.0281909 | 113 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | RELIANCE | train | 9017 | 790 | 0.0187424 | 0.0165243 | 0.0353776 | 104 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | SBIN | train | 7833 | 590 | 0.0139155 | 0.0178731 | 0.0321716 | 86 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | SUNPHARMA | train | 7322 | 773 | 0.0202131 | 0.018301 | 0.0386506 | 106 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | TCS | train | 7969 | 807 | 0.0252227 | 0.0282344 | 0.0582256 | 148 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | TECHM | train | 4929 | 1291 | 0.0454453 | 0.0432136 | 0.0890647 | 135 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | ULTRACEMCO | train | 3979 | 185 | 0.00653431 | 0.00854486 | 0.0150792 | 83 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | WIPRO | train | 5788 | 1976 | 0.0583967 | 0.069454 | 0.128369 | 272 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | ADANIPORTS | train | 9546 | 704 | 0.0100566 | 0.0113136 | 0.021475 | 94 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | AXISBANK | train | 10801 | 565 | 0.0069438 | 0.00833256 | 0.0152764 | 79 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | BAJAJ-AUTO | train | 9727 | 711 | 0.0136733 | 0.0140845 | 0.0279634 | 94 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | BANKBEES | train | 9229 | 593 | 0.0112688 | 0.0101853 | 0.0197204 | 138 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | BHARTIARTL | train | 11365 | 663 | 0.0123185 | 0.0103828 | 0.0242851 | 125 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | BPCL | train | 6758 | 290 | 0.00266351 | 0.0032554 | 0.00591891 | 43 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | BRITANNIA | train | 6029 | 879 | 0.0165865 | 0.0225576 | 0.0391441 | 132 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | CIPLA | train | 7907 | 437 | 0.00746174 | 0.00543822 | 0.0129 | 66 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | DRREDDY | train | 13141 | 925 | 0.0161327 | 0.0142303 | 0.0304391 | 515 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | GOLDBEES | train | 9148 | 715 | 0.00721469 | 0.00754263 | 0.0148666 | 77 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | HCLTECH | train | 14317 | 1321 | 0.015506 | 0.0134805 | 0.0291961 | 176 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | HDFCBANK | train | 15043 | 1255 | 0.0116333 | 0.00963903 | 0.0214053 | 179 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | HINDUNILVR | train | 8661 | 533 | 0.00958319 | 0.010045 | 0.0195128 | 96 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | ICICIBANK | train | 11236 | 612 | 0.00614098 | 0.00783197 | 0.0130829 | 115 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | INFY | train | 15210 | 1263 | 0.0175542 | 0.0157133 | 0.0332018 | 135 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | ITBEES | train | 6822 | 1249 | 0.0109938 | 0.0124597 | 0.0234535 | 528 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | ITC | train | 11084 | 617 | 0.00658607 | 0.00541321 | 0.0120895 | 67 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | JUNIORBEES | train | 13252 | 1165 | 0.0241473 | 0.0189405 | 0.0374283 | 185 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | KOTAKBANK | train | 10164 | 452 | 0.00531287 | 0.00619835 | 0.0116096 | 72 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | LT | train | 10640 | 544 | 0.00827068 | 0.00704887 | 0.0152256 | 125 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | M&M | train | 9987 | 472 | 0.00610794 | 0.00590768 | 0.0120156 | 91 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | MARUTI | train | 11104 | 680 | 0.0105367 | 0.00864553 | 0.0193624 | 102 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | NESTLEIND | train | 7878 | 419 | 0.00799695 | 0.00748921 | 0.0156131 | 59 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | NIFTYBEES | train | 11226 | 697 | 0.00596829 | 0.00668092 | 0.0127383 | 107 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | ONGC | train | 9395 | 693 | 0.00872805 | 0.00819585 | 0.0169239 | 113 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | RELIANCE | train | 11459 | 656 | 0.00986124 | 0.00767955 | 0.0177153 | 104 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | SBIN | train | 12205 | 809 | 0.0124539 | 0.0154035 | 0.0275297 | 86 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | SUNPHARMA | train | 9908 | 443 | 0.0115059 | 0.00797335 | 0.0192774 | 106 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | TCS | train | 16259 | 1457 | 0.0233102 | 0.0261394 | 0.0464358 | 148 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | TECHM | train | 9551 | 683 | 0.0190556 | 0.0151817 | 0.0332949 | 135 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | ULTRACEMCO | train | 6525 | 1107 | 0.0219157 | 0.0265134 | 0.0487356 | 83 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-10 | NSE | WIPRO | train | 10157 | 914 | 0.014079 | 0.0126021 | 0.026878 | 272 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | ADANIPORTS | validation | 9453 | 709 | 0.0159738 | 0.0155506 | 0.031736 | 94 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | AXISBANK | validation | 10797 | 565 | 0.00815041 | 0.0107437 | 0.0190794 | 79 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | BAJAJ-AUTO | validation | 14298 | 1285 | 0.0177647 | 0.0194433 | 0.0372779 | 94 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | BANKBEES | validation | 13183 | 1133 | 0.0128195 | 0.0128954 | 0.0231359 | 138 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | BHARTIARTL | validation | 11538 | 667 | 0.0103137 | 0.0102271 | 0.0246143 | 125 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | BPCL | validation | 8034 | 1851 | 0.0144386 | 0.0170525 | 0.0314912 | 43 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | BRITANNIA | validation | 6759 | 1368 | 0.0198254 | 0.0202693 | 0.0400947 | 132 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | CIPLA | validation | 8387 | 528 | 0.00834625 | 0.0101347 | 0.018481 | 66 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | DRREDDY | validation | 8735 | 207 | 0.00583858 | 0.00515169 | 0.0109903 | 515 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | GOLDBEES | validation | 8947 | 661 | 0.00760031 | 0.00782385 | 0.0155359 | 77 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | HCLTECH | validation | 14296 | 1317 | 0.0297985 | 0.0260213 | 0.0565193 | 176 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | HDFCBANK | validation | 16565 | 1513 | 0.0228796 | 0.020827 | 0.0441292 | 179 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | HINDUNILVR | validation | 8591 | 529 | 0.0102433 | 0.00919567 | 0.0194389 | 96 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | ICICIBANK | validation | 13716 | 1031 | 0.0170604 | 0.0147273 | 0.0306212 | 115 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | INFY | validation | 16206 | 1459 | 0.0248056 | 0.0251759 | 0.0488708 | 135 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | ITBEES | validation | 8304 | 2136 | 0.0209538 | 0.0243256 | 0.0557563 | 6 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | ITC | validation | 8757 | 217 | 0.00114194 | 0.00228389 | 0.00342583 | 67 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | JUNIORBEES | validation | 11801 | 933 | 0.0174561 | 0.0164393 | 0.0316075 | 185 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | KOTAKBANK | validation | 9402 | 322 | 0.00499894 | 0.00478622 | 0.00978515 | 72 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | LT | validation | 11478 | 670 | 0.0132427 | 0.0164663 | 0.0301446 | 125 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | M&M | validation | 14145 | 1139 | 0.019088 | 0.0234712 | 0.0426299 | 91 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | MARUTI | validation | 15406 | 1359 | 0.0170064 | 0.0162274 | 0.0336233 | 102 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | NESTLEIND | validation | 9035 | 586 | 0.00752629 | 0.00996126 | 0.0174875 | 59 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | NIFTYBEES | validation | 13039 | 980 | 0.0129611 | 0.0108137 | 0.0238515 | 107 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | ONGC | validation | 10644 | 853 | 0.0125893 | 0.0136227 | 0.0264938 | 113 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | RELIANCE | validation | 13219 | 962 | 0.0114986 | 0.0148271 | 0.0265527 | 104 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | SBIN | validation | 13084 | 932 | 0.0126873 | 0.0141394 | 0.0254509 | 86 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | SUNPHARMA | validation | 9572 | 713 | 0.0141036 | 0.0111784 | 0.0252821 | 106 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | TCS | validation | 16806 | 1550 | 0.0304653 | 0.0326074 | 0.0602166 | 148 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | TECHM | validation | 11316 | 954 | 0.0183811 | 0.0215624 | 0.038176 | 135 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | ULTRACEMCO | validation | 6783 | 1317 | 0.0232935 | 0.0315495 | 0.0552853 | 83 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2026-07-13 | NSE | WIPRO | validation | 11490 | 1011 | 0.0210618 | 0.0236728 | 0.0449956 | 272 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | ADANIPORTS | train | 1617 | 0 | 0 | 0 | 0 | 599 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | AXISBANK | train | 1699 | 0 | 0 | 0 | 0 | 573 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | BAJAJ-AUTO | train | 1594 | 0 | 0 | 0 | 0 | 612 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | BANKBEES | train | 1693 | 0 | 0 | 0 | 0 | 816 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | BHARTIARTL | train | 1616 | 0 | 0 | 0 | 0 | 610 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | BPCL | train | 1578 | 0 | 0 | 0 | 0 | 446 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | BRITANNIA | train | 1525 | 0 | 0 | 0 | 0 | 486 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | CIPLA | train | 1572 | 0 | 0 | 0 | 0 | 538 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | DRREDDY | train | 1582 | 0 | 0 | 0 | 0 | 556 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | GOLDBEES | train | 1642 | 0 | 0 | 0 | 0 | 559 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | HCLTECH | train | 1564 | 0 | 0 | 0 | 0 | 419 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | HDFCBANK | train | 1745 | 0 | 0 | 0 | 0 | 578 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | HINDUNILVR | train | 1618 | 0 | 0 | 0 | 0 | 707 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | ICICIBANK | train | 1722 | 0 | 0 | 0 | 0 | 620 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | INFY | train | 1682 | 0 | 0 | 0 | 0 | 595 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | ITBEES | train | 1585 | 0 | 0 | 0 | 0 | 1804 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | ITC | train | 1643 | 0 | 0 | 0 | 0 | 588 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | JUNIORBEES | train | 1685 | 0 | 0 | 0 | 0 | 747 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | KOTAKBANK | train | 1664 | 0 | 0 | 0 | 0 | 485 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | LT | train | 1733 | 0 | 0 | 0 | 0 | 767 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | M&M | train | 1714 | 0 | 0 | 0 | 0 | 776 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | MARUTI | train | 1679 | 0 | 0 | 0 | 0 | 547 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | NESTLEIND | train | 1580 | 0 | 0 | 0 | 0 | 648 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | NIFTYBEES | train | 1687 | 0 | 0 | 0 | 0 | 601 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | ONGC | train | 1628 | 0 | 0 | 0 | 0 | 686 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | RELIANCE | train | 1731 | 0 | 0 | 0 | 0 | 471 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | SBIN | train | 1686 | 0 | 0 | 0 | 0 | 436 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | SUNPHARMA | train | 1600 | 0 | 0 | 0 | 0 | 613 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | TCS | train | 1651 | 0 | 0 | 0 | 0 | 530 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | TECHM | train | 1574 | 0 | 0 | 0 | 0 | 483 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | ULTRACEMCO | train | 1577 | 0 | 0 | 0 | 0 | 439 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | WIPRO | train | 1569 | 0 | 0 | 0 | 0 | 667 | 0 | 1 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | ADANIPORTS | train | 2448 | 240 | 0.0416667 | 0.0347222 | 0.0751634 | 49 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | AXISBANK | train | 2522 | 268 | 0.0352895 | 0.0404441 | 0.0713719 | 40 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | BAJAJ-AUTO | train | 2390 | 210 | 0.0305439 | 0.0292887 | 0.0535565 | 59 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | BANKBEES | train | 2537 | 318 | 0.0524241 | 0.0484825 | 0.0878991 | 50 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | BHARTIARTL | train | 2558 | 667 | 0.107115 | 0.111415 | 0.181001 | 72 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | BPCL | train | 2421 | 192 | 0.0185874 | 0.0185874 | 0.039653 | 24 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | BRITANNIA | train | 2364 | 732 | 0.10533 | 0.116328 | 0.204315 | 94 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | CIPLA | train | 2407 | 209 | 0.0162027 | 0.0191109 | 0.0348982 | 40 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | DRREDDY | train | 2539 | 1216 | 0.204411 | 0.15833 | 0.329657 | 150 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | GOLDBEES | train | 2469 | 316 | 0.0311867 | 0.0336168 | 0.0652086 | 32 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | HCLTECH | train | 2462 | 664 | 0.0731113 | 0.0889521 | 0.170593 | 111 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | HDFCBANK | train | 2557 | 459 | 0.0801721 | 0.0672663 | 0.135315 | 84 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | HINDUNILVR | train | 2484 | 428 | 0.0772947 | 0.0704509 | 0.126812 | 56 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | ICICIBANK | train | 2548 | 441 | 0.0678964 | 0.0702512 | 0.125589 | 58 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | INFY | train | 2532 | 296 | 0.0477883 | 0.0473934 | 0.0971564 | 72 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | ITBEES | train | 2350 | 431 | 0.0302128 | 0.027234 | 0.0570213 | 3 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | ITC | train | 2527 | 403 | 0.0368025 | 0.0439256 | 0.0811239 | 58 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | JUNIORBEES | train | 2525 | 325 | 0.0491089 | 0.0522772 | 0.089505 | 67 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | KOTAKBANK | train | 2555 | 489 | 0.053229 | 0.0720157 | 0.118591 | 39 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | LT | train | 2557 | 446 | 0.0664842 | 0.0782167 | 0.124756 | 59 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | M&M | train | 2505 | 321 | 0.0471058 | 0.0522954 | 0.0898204 | 39 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | MARUTI | train | 2493 | 410 | 0.0505415 | 0.0529483 | 0.0962696 | 46 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | NESTLEIND | train | 2386 | 165 | 0.0251467 | 0.0305951 | 0.0465214 | 32 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | NIFTYBEES | train | 2514 | 237 | 0.0310263 | 0.0278441 | 0.0580748 | 40 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | ONGC | train | 2451 | 220 | 0.0322317 | 0.0265198 | 0.0571195 | 53 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | RELIANCE | train | 2539 | 402 | 0.0614415 | 0.0630169 | 0.113824 | 42 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | SBIN | train | 2520 | 387 | 0.0611111 | 0.0642857 | 0.109921 | 52 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | SUNPHARMA | train | 2517 | 487 | 0.0754867 | 0.0711164 | 0.130711 | 65 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | TCS | train | 2530 | 506 | 0.0833992 | 0.0889328 | 0.150988 | 73 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | TECHM | train | 2392 | 586 | 0.0685619 | 0.0869565 | 0.139214 | 68 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | ULTRACEMCO | train | 2358 | 99 | 0.00975403 | 0.0135708 | 0.024173 | 46 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | WIPRO | train | 2447 | 779 | 0.115652 | 0.119738 | 0.222313 | 124 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | ADANIPORTS | train | 4276 | 379 | 0.0297007 | 0.0224509 | 0.047942 | 49 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | AXISBANK | train | 4310 | 253 | 0.0160093 | 0.0204176 | 0.0350348 | 40 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | BAJAJ-AUTO | train | 4202 | 435 | 0.0340314 | 0.0368872 | 0.0642551 | 59 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | BANKBEES | train | 4105 | 201 | 0.0177832 | 0.0146163 | 0.0302071 | 50 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | BHARTIARTL | train | 4351 | 256 | 0.0195357 | 0.0199954 | 0.0351643 | 72 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | BPCL | train | 4073 | 155 | 0.00662902 | 0.00613798 | 0.0137491 | 24 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | BRITANNIA | train | 3917 | 509 | 0.0262956 | 0.030891 | 0.0518254 | 94 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | CIPLA | train | 4190 | 256 | 0.0162291 | 0.0147971 | 0.0300716 | 40 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | DRREDDY | train | 4375 | 504 | 0.0425143 | 0.0461714 | 0.08 | 150 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | GOLDBEES | train | 4250 | 311 | 0.0117647 | 0.0178824 | 0.0310588 | 32 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | HCLTECH | train | 4425 | 1091 | 0.0822599 | 0.0700565 | 0.15322 | 111 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | HDFCBANK | train | 4448 | 525 | 0.0355216 | 0.0321493 | 0.0660971 | 84 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | HINDUNILVR | train | 4184 | 239 | 0.0186424 | 0.0162524 | 0.0313098 | 56 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | ICICIBANK | train | 4342 | 254 | 0.0202672 | 0.0175035 | 0.0333947 | 58 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | INFY | train | 4460 | 671 | 0.0526906 | 0.0533632 | 0.0921525 | 72 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | ITBEES | train | 4066 | 696 | 0.0172159 | 0.0226267 | 0.0398426 | 269 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | ITC | train | 4335 | 364 | 0.0163783 | 0.0163783 | 0.0327566 | 58 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | JUNIORBEES | train | 4329 | 456 | 0.040425 | 0.036729 | 0.0644491 | 67 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | KOTAKBANK | train | 4285 | 181 | 0.00886814 | 0.0121354 | 0.0231039 | 39 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | LT | train | 4270 | 199 | 0.0166276 | 0.0138173 | 0.0257611 | 59 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | M&M | train | 4236 | 185 | 0.0125118 | 0.0113314 | 0.0221907 | 39 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | MARUTI | train | 4273 | 281 | 0.0210625 | 0.0227007 | 0.0439972 | 46 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | NESTLEIND | train | 4127 | 260 | 0.0215653 | 0.0159922 | 0.0392537 | 32 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | NIFTYBEES | train | 4295 | 297 | 0.0169965 | 0.0169965 | 0.0302678 | 40 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | ONGC | train | 4237 | 340 | 0.0226575 | 0.0243097 | 0.0457871 | 53 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | RELIANCE | train | 4360 | 241 | 0.0151376 | 0.0155963 | 0.0300459 | 42 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | SBIN | train | 4354 | 383 | 0.0339917 | 0.0355994 | 0.0564998 | 52 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | SUNPHARMA | train | 4285 | 221 | 0.0235706 | 0.0189032 | 0.0359393 | 65 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | TCS | train | 4481 | 815 | 0.0702968 | 0.0839098 | 0.116046 | 73 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | TECHM | train | 4254 | 456 | 0.0479549 | 0.0399624 | 0.0763987 | 68 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | ULTRACEMCO | train | 4018 | 627 | 0.033101 | 0.0355898 | 0.0659532 | 46 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-10 | NSE | WIPRO | train | 4321 | 532 | 0.043277 | 0.0402685 | 0.0830826 | 124 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | ADANIPORTS | validation | 4268 | 364 | 0.0320993 | 0.0335052 | 0.0627929 | 49 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | AXISBANK | validation | 4285 | 345 | 0.0256709 | 0.0298716 | 0.050175 | 40 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | BAJAJ-AUTO | validation | 4384 | 969 | 0.0873631 | 0.084854 | 0.153513 | 59 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | BANKBEES | validation | 4285 | 427 | 0.0284714 | 0.0359393 | 0.0578763 | 50 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | BHARTIARTL | validation | 4367 | 320 | 0.0247309 | 0.0261049 | 0.0494619 | 72 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | BPCL | validation | 4189 | 901 | 0.0312724 | 0.0319885 | 0.0756744 | 24 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | BRITANNIA | validation | 4043 | 795 | 0.0301756 | 0.031165 | 0.0601039 | 94 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | CIPLA | validation | 4212 | 328 | 0.0156695 | 0.0251662 | 0.0413105 | 40 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | DRREDDY | validation | 4258 | 96 | 0.00939408 | 0.00868953 | 0.0178488 | 150 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | GOLDBEES | validation | 4227 | 306 | 0.0175065 | 0.018926 | 0.0380885 | 32 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | HCLTECH | validation | 4400 | 961 | 0.1025 | 0.0834091 | 0.172045 | 111 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | HDFCBANK | validation | 4473 | 677 | 0.0592444 | 0.0625978 | 0.117594 | 84 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | HINDUNILVR | validation | 4217 | 257 | 0.0184966 | 0.0211051 | 0.0353332 | 56 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | ICICIBANK | validation | 4388 | 488 | 0.0439836 | 0.0385141 | 0.0699635 | 58 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | INFY | validation | 4471 | 789 | 0.0722433 | 0.0789533 | 0.13308 | 72 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | ITBEES | validation | 4192 | 950 | 0.0522424 | 0.0479485 | 0.100191 | 3 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | ITC | validation | 4227 | 119 | 0.00425834 | 0.00331204 | 0.00757038 | 58 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | JUNIORBEES | validation | 4245 | 401 | 0.0336867 | 0.0360424 | 0.059364 | 67 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | KOTAKBANK | validation | 4253 | 176 | 0.0101105 | 0.0131672 | 0.0268046 | 39 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | LT | validation | 4319 | 320 | 0.0277842 | 0.0331095 | 0.0520954 | 59 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | M&M | validation | 4396 | 552 | 0.0509554 | 0.055505 | 0.0821201 | 39 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | MARUTI | validation | 4442 | 580 | 0.0502026 | 0.0416479 | 0.09095 | 46 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | NESTLEIND | validation | 4206 | 424 | 0.0273419 | 0.0304327 | 0.0589634 | 32 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | NIFTYBEES | validation | 4323 | 447 | 0.0395559 | 0.0298404 | 0.0656951 | 40 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | ONGC | validation | 4308 | 507 | 0.0392293 | 0.036676 | 0.0733519 | 53 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | RELIANCE | validation | 4366 | 587 | 0.0396244 | 0.0437471 | 0.0781035 | 42 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | SBIN | validation | 4353 | 499 | 0.0399724 | 0.0443372 | 0.0707558 | 52 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | SUNPHARMA | validation | 4236 | 387 | 0.0372993 | 0.029509 | 0.0609065 | 65 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | TCS | validation | 4484 | 911 | 0.0869759 | 0.0916592 | 0.15388 | 73 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | TECHM | validation | 4288 | 713 | 0.0678638 | 0.076959 | 0.131763 | 68 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | ULTRACEMCO | validation | 4084 | 764 | 0.0374633 | 0.0472576 | 0.0857003 | 46 | 0 | 0 | 1 | 0 | 0 |
| 5 | 2026-07-13 | NSE | WIPRO | validation | 4288 | 712 | 0.0664646 | 0.0711287 | 0.123601 | 124 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | ADANIPORTS | train | 583 | 0 | 0 | 0 | 0 | 223 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | AXISBANK | train | 583 | 0 | 0 | 0 | 0 | 217 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | BAJAJ-AUTO | train | 583 | 0 | 0 | 0 | 0 | 256 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | BANKBEES | train | 583 | 0 | 0 | 0 | 0 | 302 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | BHARTIARTL | train | 583 | 0 | 0 | 0 | 0 | 228 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | BPCL | train | 583 | 0 | 0 | 0 | 0 | 180 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | BRITANNIA | train | 583 | 0 | 0 | 0 | 0 | 210 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | CIPLA | train | 583 | 0 | 0 | 0 | 0 | 222 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | DRREDDY | train | 583 | 0 | 0 | 0 | 0 | 189 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | GOLDBEES | train | 583 | 0 | 0 | 0 | 0 | 214 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | HCLTECH | train | 583 | 0 | 0 | 0 | 0 | 174 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | HDFCBANK | train | 583 | 0 | 0 | 0 | 0 | 236 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | HINDUNILVR | train | 583 | 0 | 0 | 0 | 0 | 266 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | ICICIBANK | train | 583 | 0 | 0 | 0 | 0 | 191 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | INFY | train | 583 | 0 | 0 | 0 | 0 | 188 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | ITBEES | train | 583 | 0 | 0 | 0 | 0 | 752 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | ITC | train | 583 | 0 | 0 | 0 | 0 | 232 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | JUNIORBEES | train | 583 | 0 | 0 | 0 | 0 | 281 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | KOTAKBANK | train | 583 | 0 | 0 | 0 | 0 | 195 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | LT | train | 583 | 0 | 0 | 0 | 0 | 268 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | M&M | train | 583 | 0 | 0 | 0 | 0 | 263 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | MARUTI | train | 583 | 0 | 0 | 0 | 0 | 201 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | NESTLEIND | train | 583 | 0 | 0 | 0 | 0 | 237 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | NIFTYBEES | train | 583 | 0 | 0 | 0 | 0 | 219 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | ONGC | train | 583 | 0 | 0 | 0 | 0 | 280 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | RELIANCE | train | 583 | 0 | 0 | 0 | 0 | 181 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | SBIN | train | 583 | 0 | 0 | 0 | 0 | 188 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | SUNPHARMA | train | 583 | 0 | 0 | 0 | 0 | 228 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | TCS | train | 583 | 0 | 0 | 0 | 0 | 209 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | TECHM | train | 583 | 0 | 0 | 0 | 0 | 152 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | ULTRACEMCO | train | 583 | 0 | 0 | 0 | 0 | 177 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | WIPRO | train | 583 | 0 | 0 | 0 | 0 | 254 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | ADANIPORTS | train | 858 | 5 | 0.0011655 | 0.0011655 | 0.002331 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | AXISBANK | train | 858 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | BAJAJ-AUTO | train | 858 | 11 | 0.00582751 | 0.0034965 | 0.00815851 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | BANKBEES | train | 859 | 0 | 0 | 0 | 0 | 302 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | BHARTIARTL | train | 858 | 14 | 0.004662 | 0.004662 | 0.00699301 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | BPCL | train | 858 | 8 | 0.004662 | 0.0034965 | 0.00699301 | 2 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | BRITANNIA | train | 857 | 175 | 0.0898483 | 0.0816803 | 0.150525 | 21 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | CIPLA | train | 858 | 10 | 0.00582751 | 0.0034965 | 0.00582751 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | DRREDDY | train | 858 | 525 | 0.299534 | 0.280886 | 0.434732 | 43 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | GOLDBEES | train | 859 | 0 | 0 | 0 | 0 | 214 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | HCLTECH | train | 858 | 129 | 0.0617716 | 0.0687646 | 0.101399 | 20 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | HDFCBANK | train | 858 | 0 | 0 | 0 | 0 | 236 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | HINDUNILVR | train | 858 | 52 | 0.0268065 | 0.025641 | 0.0361305 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | ICICIBANK | train | 858 | 0 | 0 | 0 | 0 | 191 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | INFY | train | 858 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | ITBEES | train | 859 | 85 | 0.0314319 | 0.0221187 | 0.0535506 | 3 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | ITC | train | 858 | 4 | 0.0011655 | 0.0011655 | 0.0011655 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | JUNIORBEES | train | 859 | 0 | 0 | 0 | 0 | 281 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | KOTAKBANK | train | 858 | 0 | 0 | 0 | 0 | 195 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | LT | train | 858 | 0 | 0 | 0 | 0 | 268 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | M&M | train | 858 | 0 | 0 | 0 | 0 | 263 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | MARUTI | train | 858 | 3 | 0.0011655 | 0.0011655 | 0.0011655 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | NESTLEIND | train | 858 | 10 | 0.0034965 | 0.00582751 | 0.00582751 | 2 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | NIFTYBEES | train | 859 | 0 | 0 | 0 | 0 | 219 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | ONGC | train | 858 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | RELIANCE | train | 858 | 0 | 0 | 0 | 0 | 181 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | SBIN | train | 858 | 0 | 0 | 0 | 0 | 188 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | SUNPHARMA | train | 858 | 90 | 0.0431235 | 0.04662 | 0.0699301 | 4 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | TCS | train | 858 | 10 | 0.002331 | 0.0034965 | 0.004662 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | TECHM | train | 858 | 43 | 0.020979 | 0.02331 | 0.032634 | 4 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | ULTRACEMCO | train | 858 | 2 | 0.002331 | 0 | 0 | 4 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | WIPRO | train | 858 | 180 | 0.104895 | 0.100233 | 0.164336 | 22 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | ADANIPORTS | train | 1502 | 2 | 0.000665779 | 0.000665779 | 0.000665779 | 2 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | AXISBANK | train | 1502 | 0 | 0 | 0 | 0 | 217 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | BAJAJ-AUTO | train | 1502 | 7 | 0.00133156 | 0.00266312 | 0.00199734 | 2 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | BANKBEES | train | 1501 | 0 | 0 | 0 | 0 | 302 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | BHARTIARTL | train | 1502 | 0 | 0 | 0 | 0 | 228 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | BPCL | train | 1502 | 5 | 0.000665779 | 0.00133156 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | BRITANNIA | train | 1501 | 70 | 0.0173218 | 0.0113258 | 0.0219853 | 21 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | CIPLA | train | 1502 | 9 | 0.00133156 | 0.00266312 | 0.00199734 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | DRREDDY | train | 1502 | 2 | 0 | 0.00133156 | 0.000665779 | 43 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | GOLDBEES | train | 1501 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | HCLTECH | train | 1502 | 131 | 0.0419441 | 0.0372836 | 0.0645806 | 20 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | HDFCBANK | train | 1502 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | HINDUNILVR | train | 1502 | 0 | 0 | 0 | 0 | 266 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | ICICIBANK | train | 1502 | 0 | 0 | 0 | 0 | 191 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | INFY | train | 1501 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | ITBEES | train | 1501 | 56 | 0.00732845 | 0.00399734 | 0.0159893 | 20 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | ITC | train | 1502 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | JUNIORBEES | train | 1500 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | KOTAKBANK | train | 1502 | 0 | 0 | 0 | 0 | 195 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | LT | train | 1502 | 0 | 0 | 0 | 0 | 268 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | M&M | train | 1502 | 0 | 0 | 0 | 0 | 263 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | MARUTI | train | 1502 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | NESTLEIND | train | 1502 | 21 | 0.00732357 | 0.00532623 | 0.0113182 | 2 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | NIFTYBEES | train | 1501 | 0 | 0 | 0 | 0 | 219 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | ONGC | train | 1502 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | RELIANCE | train | 1501 | 0 | 0 | 0 | 0 | 181 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | SBIN | train | 1502 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | SUNPHARMA | train | 1502 | 2 | 0 | 0.000665779 | 0.00133156 | 7 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | TCS | train | 1501 | 1 | 0.000666223 | 0 | 0 | 3 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | TECHM | train | 1502 | 28 | 0.00998668 | 0.00732357 | 0.0146471 | 2 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | ULTRACEMCO | train | 1501 | 28 | 0.005996 | 0.00732845 | 0.00999334 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | WIPRO | train | 1502 | 61 | 0.017976 | 0.017976 | 0.0226365 | 22 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | ADANIPORTS | validation | 1502 | 6 | 0.00332889 | 0 | 0.00266312 | 1 | 3 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | AXISBANK | validation | 1502 | 3 | 0.000665779 | 0.00133156 | 0.00199734 | 217 | 3 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | BAJAJ-AUTO | validation | 1502 | 66 | 0.0219707 | 0.0213049 | 0.0339547 | 1 | 6 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | BANKBEES | validation | 1502 | 0 | 0 | 0 | 0 | 302 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | BHARTIARTL | validation | 1502 | 1 | 0 | 0.000665779 | 0.000665779 | 228 | 1 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | BPCL | validation | 1502 | 47 | 0.00599201 | 0.0126498 | 0.0139814 | 1 | 32 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | BRITANNIA | validation | 1502 | 77 | 0.0153129 | 0.0159787 | 0.0266312 | 21 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | CIPLA | validation | 1502 | 22 | 0.00599201 | 0.00798935 | 0.011984 | 1 | 2 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | DRREDDY | validation | 1502 | 1 | 0 | 0.000665779 | 0.000665779 | 43 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | GOLDBEES | validation | 1502 | 4 | 0.00133156 | 0.000665779 | 0.00199734 | 1 | 3 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | HCLTECH | validation | 1502 | 179 | 0.0645806 | 0.0479361 | 0.0898802 | 20 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | HDFCBANK | validation | 1502 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | HINDUNILVR | validation | 1502 | 4 | 0.000665779 | 0.00199734 | 0.00133156 | 7 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | ICICIBANK | validation | 1502 | 1 | 0 | 0.000665779 | 0.000665779 | 191 | 1 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | INFY | validation | 1502 | 1 | 0 | 0.000665779 | 0.000665779 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | ITBEES | validation | 1502 | 151 | 0.0372836 | 0.0279627 | 0.0639148 | 3 | 20 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | ITC | validation | 1502 | 2 | 0.000665779 | 0.000665779 | 0.00133156 | 1 | 1 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | JUNIORBEES | validation | 1502 | 0 | 0 | 0 | 0 | 281 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | KOTAKBANK | validation | 1502 | 0 | 0 | 0 | 0 | 195 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | LT | validation | 1502 | 1 | 0 | 0.000665779 | 0.000665779 | 268 | 1 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | M&M | validation | 1502 | 0 | 0 | 0 | 0 | 263 | 0 | 1 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | MARUTI | validation | 1502 | 1 | 0.000665779 | 0 | 0.000665779 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | NESTLEIND | validation | 1502 | 31 | 0.00798935 | 0.0126498 | 0.0146471 | 2 | 3 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | NIFTYBEES | validation | 1502 | 1 | 0 | 0.000665779 | 0.000665779 | 219 | 1 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | ONGC | validation | 1502 | 6 | 0.00133156 | 0.00266312 | 0.00332889 | 1 | 5 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | RELIANCE | validation | 1502 | 4 | 0.00133156 | 0.00133156 | 0.00266312 | 181 | 4 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | SBIN | validation | 1502 | 2 | 0.000665779 | 0.000665779 | 0.00133156 | 188 | 2 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | SUNPHARMA | validation | 1502 | 3 | 0.000665779 | 0.00133156 | 0.00199734 | 4 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | TCS | validation | 1502 | 3 | 0.000665779 | 0.00133156 | 0.00199734 | 1 | 1 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | TECHM | validation | 1502 | 106 | 0.0372836 | 0.0326232 | 0.0539281 | 2 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | ULTRACEMCO | validation | 1502 | 29 | 0.0113182 | 0.00665779 | 0.0113182 | 1 | 0 | 0 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | WIPRO | validation | 1502 | 92 | 0.023968 | 0.0372836 | 0.0446072 | 22 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | ADANIPORTS | train | 147 | 0 | 0 | 0 | 0 | 51 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | AXISBANK | train | 147 | 0 | 0 | 0 | 0 | 54 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | BAJAJ-AUTO | train | 147 | 0 | 0 | 0 | 0 | 63 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | BANKBEES | train | 147 | 0 | 0 | 0 | 0 | 71 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | BHARTIARTL | train | 147 | 0 | 0 | 0 | 0 | 52 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | BPCL | train | 147 | 0 | 0 | 0 | 0 | 34 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | BRITANNIA | train | 147 | 0 | 0 | 0 | 0 | 30 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | CIPLA | train | 147 | 0 | 0 | 0 | 0 | 54 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | DRREDDY | train | 147 | 0 | 0 | 0 | 0 | 46 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | GOLDBEES | train | 147 | 0 | 0 | 0 | 0 | 49 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | HCLTECH | train | 147 | 0 | 0 | 0 | 0 | 54 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | HDFCBANK | train | 147 | 0 | 0 | 0 | 0 | 53 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | HINDUNILVR | train | 147 | 0 | 0 | 0 | 0 | 69 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | ICICIBANK | train | 147 | 0 | 0 | 0 | 0 | 39 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | INFY | train | 147 | 0 | 0 | 0 | 0 | 57 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | ITBEES | train | 147 | 0 | 0 | 0 | 0 | 11 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | ITC | train | 147 | 0 | 0 | 0 | 0 | 57 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | JUNIORBEES | train | 147 | 0 | 0 | 0 | 0 | 72 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | KOTAKBANK | train | 147 | 0 | 0 | 0 | 0 | 98 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | LT | train | 147 | 0 | 0 | 0 | 0 | 67 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | M&M | train | 147 | 0 | 0 | 0 | 0 | 70 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | MARUTI | train | 147 | 0 | 0 | 0 | 0 | 50 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | NESTLEIND | train | 147 | 0 | 0 | 0 | 0 | 54 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | NIFTYBEES | train | 147 | 0 | 0 | 0 | 0 | 49 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | ONGC | train | 147 | 0 | 0 | 0 | 0 | 63 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | RELIANCE | train | 147 | 0 | 0 | 0 | 0 | 57 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | SBIN | train | 147 | 0 | 0 | 0 | 0 | 36 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | SUNPHARMA | train | 147 | 0 | 0 | 0 | 0 | 60 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | TCS | train | 147 | 0 | 0 | 0 | 0 | 56 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | TECHM | train | 147 | 0 | 0 | 0 | 0 | 34 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | ULTRACEMCO | train | 147 | 0 | 0 | 0 | 0 | 45 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-08 | NSE | WIPRO | train | 147 | 0 | 0 | 0 | 0 | 61 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | ADANIPORTS | train | 216 | 0 | 0 | 0 | 0 | 51 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | AXISBANK | train | 216 | 0 | 0 | 0 | 0 | 54 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | BAJAJ-AUTO | train | 216 | 0 | 0 | 0 | 0 | 63 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | BANKBEES | train | 216 | 0 | 0 | 0 | 0 | 71 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | BHARTIARTL | train | 216 | 0 | 0 | 0 | 0 | 52 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | BPCL | train | 216 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | BRITANNIA | train | 215 | 20 | 0.0418605 | 0.0325581 | 0.055814 | 1 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | CIPLA | train | 216 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | DRREDDY | train | 216 | 143 | 0.324074 | 0.324074 | 0.486111 | 7 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | GOLDBEES | train | 216 | 0 | 0 | 0 | 0 | 49 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | HCLTECH | train | 216 | 21 | 0.037037 | 0.0509259 | 0.0601852 | 1 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | HDFCBANK | train | 216 | 0 | 0 | 0 | 0 | 53 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | HINDUNILVR | train | 216 | 3 | 0.00462963 | 0.00462963 | 0.00925926 | 1 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | ICICIBANK | train | 216 | 0 | 0 | 0 | 0 | 39 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | INFY | train | 216 | 0 | 0 | 0 | 0 | 57 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | ITBEES | train | 216 | 5 | 0.00925926 | 0.00925926 | 0.0138889 | 2 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | ITC | train | 216 | 0 | 0 | 0 | 0 | 57 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | JUNIORBEES | train | 216 | 0 | 0 | 0 | 0 | 72 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | KOTAKBANK | train | 216 | 0 | 0 | 0 | 0 | 39 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | LT | train | 216 | 0 | 0 | 0 | 0 | 67 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | M&M | train | 216 | 0 | 0 | 0 | 0 | 70 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | MARUTI | train | 216 | 0 | 0 | 0 | 0 | 50 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | NESTLEIND | train | 216 | 0 | 0 | 0 | 0 | 54 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | NIFTYBEES | train | 216 | 0 | 0 | 0 | 0 | 49 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | ONGC | train | 216 | 0 | 0 | 0 | 0 | 63 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | RELIANCE | train | 216 | 0 | 0 | 0 | 0 | 57 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | SBIN | train | 216 | 0 | 0 | 0 | 0 | 36 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | SUNPHARMA | train | 216 | 10 | 0.0138889 | 0.00925926 | 0.0138889 | 1 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | TCS | train | 216 | 0 | 0 | 0 | 0 | 56 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | TECHM | train | 216 | 6 | 0.00925926 | 0.00462963 | 0.0138889 | 1 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | ULTRACEMCO | train | 216 | 0 | 0 | 0 | 0 | 45 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-09 | NSE | WIPRO | train | 216 | 42 | 0.087963 | 0.0833333 | 0.12037 | 2 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | ADANIPORTS | train | 377 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | AXISBANK | train | 377 | 0 | 0 | 0 | 0 | 54 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | BAJAJ-AUTO | train | 377 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | BANKBEES | train | 376 | 0 | 0 | 0 | 0 | 71 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | BHARTIARTL | train | 377 | 0 | 0 | 0 | 0 | 52 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | BPCL | train | 377 | 0 | 0 | 0 | 0 | 34 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | BRITANNIA | train | 377 | 3 | 0 | 0.00530504 | 0.00265252 | 3 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | CIPLA | train | 377 | 0 | 0 | 0 | 0 | 54 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | DRREDDY | train | 377 | 0 | 0 | 0 | 0 | 46 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | GOLDBEES | train | 376 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | HCLTECH | train | 377 | 8 | 0.0132626 | 0.00530504 | 0.0185676 | 2 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | HDFCBANK | train | 377 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | HINDUNILVR | train | 377 | 0 | 0 | 0 | 0 | 69 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | ICICIBANK | train | 377 | 0 | 0 | 0 | 0 | 39 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | INFY | train | 376 | 0 | 0 | 0 | 0 | 57 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | ITBEES | train | 376 | 3 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | ITC | train | 377 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | JUNIORBEES | train | 375 | 0 | 0 | 0 | 0 | 72 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | KOTAKBANK | train | 377 | 0 | 0 | 0 | 0 | 39 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | LT | train | 377 | 0 | 0 | 0 | 0 | 67 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | M&M | train | 377 | 0 | 0 | 0 | 0 | 70 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | MARUTI | train | 377 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | NESTLEIND | train | 377 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | NIFTYBEES | train | 376 | 0 | 0 | 0 | 0 | 49 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | ONGC | train | 377 | 0 | 0 | 0 | 0 | 63 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | RELIANCE | train | 376 | 0 | 0 | 0 | 0 | 57 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | SBIN | train | 377 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | SUNPHARMA | train | 377 | 1 | 0 | 0.00265252 | 0.00265252 | 2 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | TCS | train | 376 | 0 | 0 | 0 | 0 | 56 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | TECHM | train | 377 | 2 | 0 | 0.00265252 | 0.00265252 | 1 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | ULTRACEMCO | train | 377 | 0 | 0 | 0 | 0 | 45 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-10 | NSE | WIPRO | train | 377 | 8 | 0.00795756 | 0.0106101 | 0.0106101 | 4 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | ADANIPORTS | validation | 377 | 0 | 0 | 0 | 0 | 51 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | AXISBANK | validation | 377 | 1 | 0 | 0.00265252 | 0.00265252 | 54 | 1 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | BAJAJ-AUTO | validation | 377 | 6 | 0.00795756 | 0.00530504 | 0.0132626 | 1 | 5 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | BANKBEES | validation | 376 | 0 | 0 | 0 | 0 | 71 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | BHARTIARTL | validation | 377 | 1 | 0 | 0.00265252 | 0.00265252 | 52 | 1 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | BPCL | validation | 377 | 4 | 0.00265252 | 0.00795756 | 0.00795756 | 34 | 4 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | BRITANNIA | validation | 377 | 3 | 0.00530504 | 0.00265252 | 0.00530504 | 4 | 1 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | CIPLA | validation | 377 | 2 | 0.00530504 | 0 | 0.00530504 | 54 | 2 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | DRREDDY | validation | 377 | 1 | 0 | 0.00265252 | 0.00265252 | 10 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | GOLDBEES | validation | 376 | 0 | 0 | 0 | 0 | 49 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | HCLTECH | validation | 377 | 15 | 0.0132626 | 0.0265252 | 0.0265252 | 1 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | HDFCBANK | validation | 377 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | HINDUNILVR | validation | 377 | 1 | 0 | 0.00265252 | 0.00265252 | 69 | 1 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | ICICIBANK | validation | 377 | 1 | 0 | 0.00265252 | 0.00265252 | 39 | 1 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | INFY | validation | 377 | 1 | 0 | 0.00265252 | 0.00265252 | 57 | 1 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | ITBEES | validation | 376 | 24 | 0.0452128 | 0.0159574 | 0.0345745 | 1 | 8 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | ITC | validation | 377 | 1 | 0 | 0.00265252 | 0.00265252 | 57 | 1 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | JUNIORBEES | validation | 376 | 0 | 0 | 0 | 0 | 72 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | KOTAKBANK | validation | 377 | 0 | 0 | 0 | 0 | 39 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | LT | validation | 377 | 1 | 0 | 0.00265252 | 0.00265252 | 67 | 1 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | M&M | validation | 377 | 0 | 0 | 0 | 0 | 70 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | MARUTI | validation | 377 | 0 | 0 | 0 | 0 | 50 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | NESTLEIND | validation | 377 | 5 | 0.00530504 | 0.00795756 | 0.0132626 | 54 | 5 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | NIFTYBEES | validation | 376 | 0 | 0 | 0 | 0 | 49 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | ONGC | validation | 377 | 0 | 0 | 0 | 0 | 63 | 0 | 1 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | RELIANCE | validation | 377 | 1 | 0 | 0.00265252 | 0.00265252 | 57 | 1 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | SBIN | validation | 377 | 1 | 0 | 0.00265252 | 0.00265252 | 36 | 1 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | SUNPHARMA | validation | 377 | 1 | 0 | 0.00265252 | 0.00265252 | 1 | 0 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | TCS | validation | 377 | 1 | 0 | 0.00265252 | 0.00265252 | 56 | 1 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | TECHM | validation | 377 | 13 | 0.0106101 | 0.0238727 | 0.0291777 | 1 | 5 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | ULTRACEMCO | validation | 377 | 1 | 0 | 0.00265252 | 0.00265252 | 45 | 1 | 0 | 1 | 0 | 0 |
| 60 | 2026-07-13 | NSE | WIPRO | validation | 377 | 8 | 0.0132626 | 0.00795756 | 0.0159151 | 2 | 0 | 0 | 1 | 0 | 0 |

## Split Balance Summary

| split_role | horizon_sec | partition_rows | total_rows | event_surprise_rows | mean_up_positive_rate | mean_down_positive_rate | mean_vol_expansion_positive_rate | quality_pass_rows | model_fit_allowed | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train | 1 | 96 | 693503 | 52764 | 0.011833 | 0.0116941 | 0.0235504 | 96 | 0 | 0 |
| train | 5 | 96 | 268273 | 25922 | 0.0289357 | 0.0292557 | 0.0534895 | 96 | 0 | 0 |
| train | 15 | 96 | 94169 | 1792 | 0.00857876 | 0.00809487 | 0.0130643 | 96 | 0 | 0 |
| train | 60 | 96 | 23670 | 285 | 0.00572075 | 0.00567911 | 0.00844314 | 96 | 0 | 0 |
| validation | 1 | 32 | 363786 | 31457 | 0.0151348 | 0.0160367 | 0.0313369 | 32 | 0 | 0 |
| validation | 5 | 32 | 137477 | 17072 | 0.0409329 | 0.0419709 | 0.0767712 | 32 | 0 | 0 |
| validation | 15 | 32 | 48064 | 845 | 0.00761485 | 0.00746921 | 0.0121921 | 32 | 0 | 0 |
| validation | 60 | 32 | 12059 | 94 | 0.00340229 | 0.00414589 | 0.00580525 | 32 | 0 | 0 |

## Sealed Test Inventory

| horizon_sec | trade_date | exchange | symbol | split_role | sealed_test_rows_available | sealed_test_rows_used | materialized_in_phase214 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-07-14 | NSE | ADANIPORTS | test_untouched | 9870 | 0 | 0 |
| 1 | 2026-07-14 | NSE | AXISBANK | test_untouched | 12367 | 0 | 0 |
| 1 | 2026-07-14 | NSE | BAJAJ-AUTO | test_untouched | 15118 | 0 | 0 |
| 1 | 2026-07-14 | NSE | BANKBEES | test_untouched | 12039 | 0 | 0 |
| 1 | 2026-07-14 | NSE | BHARTIARTL | test_untouched | 13067 | 0 | 0 |
| 1 | 2026-07-14 | NSE | BPCL | test_untouched | 8728 | 0 | 0 |
| 1 | 2026-07-14 | NSE | BRITANNIA | test_untouched | 8237 | 0 | 0 |
| 1 | 2026-07-14 | NSE | CIPLA | test_untouched | 8977 | 0 | 0 |
| 1 | 2026-07-14 | NSE | DRREDDY | test_untouched | 8455 | 0 | 0 |
| 1 | 2026-07-14 | NSE | GOLDBEES | test_untouched | 9931 | 0 | 0 |
| 1 | 2026-07-14 | NSE | HCLTECH | test_untouched | 15676 | 0 | 0 |
| 1 | 2026-07-14 | NSE | HDFCBANK | test_untouched | 15863 | 0 | 0 |
| 1 | 2026-07-14 | NSE | HINDUNILVR | test_untouched | 10845 | 0 | 0 |
| 1 | 2026-07-14 | NSE | ICICIBANK | test_untouched | 13573 | 0 | 0 |
| 1 | 2026-07-14 | NSE | INFY | test_untouched | 15628 | 0 | 0 |
| 1 | 2026-07-14 | NSE | ITBEES | test_untouched | 6615 | 0 | 0 |
| 1 | 2026-07-14 | NSE | ITC | test_untouched | 12348 | 0 | 0 |
| 1 | 2026-07-14 | NSE | JUNIORBEES | test_untouched | 11960 | 0 | 0 |
| 1 | 2026-07-14 | NSE | KOTAKBANK | test_untouched | 11202 | 0 | 0 |
| 1 | 2026-07-14 | NSE | LT | test_untouched | 12560 | 0 | 0 |
| 1 | 2026-07-14 | NSE | M&M | test_untouched | 13067 | 0 | 0 |
| 1 | 2026-07-14 | NSE | MARUTI | test_untouched | 11007 | 0 | 0 |
| 1 | 2026-07-14 | NSE | NESTLEIND | test_untouched | 9367 | 0 | 0 |
| 1 | 2026-07-14 | NSE | NIFTYBEES | test_untouched | 11587 | 0 | 0 |
| 1 | 2026-07-14 | NSE | ONGC | test_untouched | 10277 | 0 | 0 |
| 1 | 2026-07-14 | NSE | RELIANCE | test_untouched | 13623 | 0 | 0 |
| 1 | 2026-07-14 | NSE | SBIN | test_untouched | 12762 | 0 | 0 |
| 1 | 2026-07-14 | NSE | SUNPHARMA | test_untouched | 11508 | 0 | 0 |
| 1 | 2026-07-14 | NSE | TCS | test_untouched | 15791 | 0 | 0 |
| 1 | 2026-07-14 | NSE | TECHM | test_untouched | 11094 | 0 | 0 |
| 1 | 2026-07-14 | NSE | ULTRACEMCO | test_untouched | 7964 | 0 | 0 |
| 1 | 2026-07-14 | NSE | WIPRO | test_untouched | 9394 | 0 | 0 |
| 5 | 2026-07-14 | NSE | ADANIPORTS | test_untouched | 4199 | 0 | 0 |
| 5 | 2026-07-14 | NSE | AXISBANK | test_untouched | 4332 | 0 | 0 |
| 5 | 2026-07-14 | NSE | BAJAJ-AUTO | test_untouched | 4438 | 0 | 0 |
| 5 | 2026-07-14 | NSE | BANKBEES | test_untouched | 4241 | 0 | 0 |
| 5 | 2026-07-14 | NSE | BHARTIARTL | test_untouched | 4402 | 0 | 0 |
| 5 | 2026-07-14 | NSE | BPCL | test_untouched | 4127 | 0 | 0 |
| 5 | 2026-07-14 | NSE | BRITANNIA | test_untouched | 4099 | 0 | 0 |
| 5 | 2026-07-14 | NSE | CIPLA | test_untouched | 4185 | 0 | 0 |
| 5 | 2026-07-14 | NSE | DRREDDY | test_untouched | 4169 | 0 | 0 |
| 5 | 2026-07-14 | NSE | GOLDBEES | test_untouched | 4174 | 0 | 0 |
| 5 | 2026-07-14 | NSE | HCLTECH | test_untouched | 4472 | 0 | 0 |
| 5 | 2026-07-14 | NSE | HDFCBANK | test_untouched | 4476 | 0 | 0 |
| 5 | 2026-07-14 | NSE | HINDUNILVR | test_untouched | 4212 | 0 | 0 |
| 5 | 2026-07-14 | NSE | ICICIBANK | test_untouched | 4377 | 0 | 0 |
| 5 | 2026-07-14 | NSE | INFY | test_untouched | 4475 | 0 | 0 |
| 5 | 2026-07-14 | NSE | ITBEES | test_untouched | 3980 | 0 | 0 |
| 5 | 2026-07-14 | NSE | ITC | test_untouched | 4325 | 0 | 0 |
| 5 | 2026-07-14 | NSE | JUNIORBEES | test_untouched | 4249 | 0 | 0 |
| 5 | 2026-07-14 | NSE | KOTAKBANK | test_untouched | 4266 | 0 | 0 |
| 5 | 2026-07-14 | NSE | LT | test_untouched | 4364 | 0 | 0 |
| 5 | 2026-07-14 | NSE | M&M | test_untouched | 4369 | 0 | 0 |
| 5 | 2026-07-14 | NSE | MARUTI | test_untouched | 4222 | 0 | 0 |
| 5 | 2026-07-14 | NSE | NESTLEIND | test_untouched | 4193 | 0 | 0 |
| 5 | 2026-07-14 | NSE | NIFTYBEES | test_untouched | 4239 | 0 | 0 |
| 5 | 2026-07-14 | NSE | ONGC | test_untouched | 4246 | 0 | 0 |
| 5 | 2026-07-14 | NSE | RELIANCE | test_untouched | 4383 | 0 | 0 |
| 5 | 2026-07-14 | NSE | SBIN | test_untouched | 4350 | 0 | 0 |
| 5 | 2026-07-14 | NSE | SUNPHARMA | test_untouched | 4263 | 0 | 0 |
| 5 | 2026-07-14 | NSE | TCS | test_untouched | 4473 | 0 | 0 |
| 5 | 2026-07-14 | NSE | TECHM | test_untouched | 4289 | 0 | 0 |
| 5 | 2026-07-14 | NSE | ULTRACEMCO | test_untouched | 4080 | 0 | 0 |
| 5 | 2026-07-14 | NSE | WIPRO | test_untouched | 4204 | 0 | 0 |
| 15 | 2026-07-14 | NSE | ADANIPORTS | test_untouched | 1501 | 0 | 0 |
| 15 | 2026-07-14 | NSE | AXISBANK | test_untouched | 1501 | 0 | 0 |
| 15 | 2026-07-14 | NSE | BAJAJ-AUTO | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | BANKBEES | test_untouched | 1499 | 0 | 0 |
| 15 | 2026-07-14 | NSE | BHARTIARTL | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | BPCL | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | BRITANNIA | test_untouched | 1500 | 0 | 0 |
| 15 | 2026-07-14 | NSE | CIPLA | test_untouched | 1501 | 0 | 0 |
| 15 | 2026-07-14 | NSE | DRREDDY | test_untouched | 1500 | 0 | 0 |
| 15 | 2026-07-14 | NSE | GOLDBEES | test_untouched | 1500 | 0 | 0 |
| 15 | 2026-07-14 | NSE | HCLTECH | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | HDFCBANK | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | HINDUNILVR | test_untouched | 1499 | 0 | 0 |
| 15 | 2026-07-14 | NSE | ICICIBANK | test_untouched | 1501 | 0 | 0 |
| 15 | 2026-07-14 | NSE | INFY | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | ITBEES | test_untouched | 1499 | 0 | 0 |
| 15 | 2026-07-14 | NSE | ITC | test_untouched | 1501 | 0 | 0 |
| 15 | 2026-07-14 | NSE | JUNIORBEES | test_untouched | 1499 | 0 | 0 |
| 15 | 2026-07-14 | NSE | KOTAKBANK | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | LT | test_untouched | 1501 | 0 | 0 |
| 15 | 2026-07-14 | NSE | M&M | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | MARUTI | test_untouched | 1501 | 0 | 0 |
| 15 | 2026-07-14 | NSE | NESTLEIND | test_untouched | 1501 | 0 | 0 |
| 15 | 2026-07-14 | NSE | NIFTYBEES | test_untouched | 1501 | 0 | 0 |
| 15 | 2026-07-14 | NSE | ONGC | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | RELIANCE | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | SBIN | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | SUNPHARMA | test_untouched | 1501 | 0 | 0 |
| 15 | 2026-07-14 | NSE | TCS | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | TECHM | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | ULTRACEMCO | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | WIPRO | test_untouched | 1502 | 0 | 0 |
| 60 | 2026-07-14 | NSE | ADANIPORTS | test_untouched | 376 | 0 | 0 |
| 60 | 2026-07-14 | NSE | AXISBANK | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | BAJAJ-AUTO | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | BANKBEES | test_untouched | 376 | 0 | 0 |
| 60 | 2026-07-14 | NSE | BHARTIARTL | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | BPCL | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | BRITANNIA | test_untouched | 376 | 0 | 0 |
| 60 | 2026-07-14 | NSE | CIPLA | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | DRREDDY | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | GOLDBEES | test_untouched | 376 | 0 | 0 |
| 60 | 2026-07-14 | NSE | HCLTECH | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | HDFCBANK | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | HINDUNILVR | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | ICICIBANK | test_untouched | 376 | 0 | 0 |
| 60 | 2026-07-14 | NSE | INFY | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | ITBEES | test_untouched | 376 | 0 | 0 |
| 60 | 2026-07-14 | NSE | ITC | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | JUNIORBEES | test_untouched | 375 | 0 | 0 |
| 60 | 2026-07-14 | NSE | KOTAKBANK | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | LT | test_untouched | 376 | 0 | 0 |
| 60 | 2026-07-14 | NSE | M&M | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | MARUTI | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | NESTLEIND | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | NIFTYBEES | test_untouched | 376 | 0 | 0 |
| 60 | 2026-07-14 | NSE | ONGC | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | RELIANCE | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | SBIN | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | SUNPHARMA | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | TCS | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | TECHM | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | ULTRACEMCO | test_untouched | 377 | 0 | 0 |
| 60 | 2026-07-14 | NSE | WIPRO | test_untouched | 377 | 0 | 0 |

## Forbidden Execution Ledger

| forbidden_output | emitted_in_phase214 | allowed_in_phase214 | rationale |
| --- | --- | --- | --- |
| model_fit | 0 | 0 | Phase214 materializes conditional labels only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| model_prediction | 0 | 0 | Phase214 materializes conditional labels only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| strategy_replay | 0 | 0 | Phase214 materializes conditional labels only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| test_replay_execution | 0 | 0 | Phase214 materializes conditional labels only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| test_result | 0 | 0 | Phase214 materializes conditional labels only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| promotion | 0 | 0 | Phase214 materializes conditional labels only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| paper_live_acceptance | 0 | 0 | Phase214 materializes conditional labels only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| order_arrival | 0 | 0 | Phase214 materializes conditional labels only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| fill_model | 0 | 0 | Phase214 materializes conditional labels only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| pnl_replay | 0 | 0 | Phase214 materializes conditional labels only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| profitability_claim | 0 | 0 | Phase214 materializes conditional labels only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| threshold_widening | 0 | 0 | Phase214 materializes conditional labels only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| row_level_prediction_export | 0 | 0 | Phase214 materializes conditional labels only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P214_PHASE213_COMPLETE | True | phase213_complete=1 | hard |
| P214_LABEL_PARTITIONS_MATERIALIZED | True | partition_rows=512 | hard |
| P214_LABEL_ROWS_POSITIVE | True | materialized_rows=1641001 | hard |
| P214_EVENT_SURPRISE_ROWS_POSITIVE | True | event_surprise_rows=130231 | hard |
| P214_QUALITY_ROWS_PASS | True | quality_pass_rows=512; quality_rows=512 | hard |
| P214_SPLIT_BALANCE_RECORDED | True | balance_rows=8 | hard |
| P214_SEALED_TEST_INVENTORY_UNUSED | True | sealed_rows=128; sealed_used=0 | hard |
| P214_FORBIDDEN_OUTPUTS_CLEAN | True | forbidden_emitted=0; replay_flags=0 | hard |
