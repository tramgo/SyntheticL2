# Phase107 Symbol-Aware Calibration Contract

Generated UTC: 2026-07-19T22:16:12.493268+00:00

Phase107 converts the Phase106 full-symbol realism gaps into executable calibration patch items.
It does not reopen strategy replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase107_phase106_gap_rows | 50 | Phase106 failed symbol-metric anchors triaged |
| phase107_override_rows | 50 | Concrete symbol/metric override proposals emitted |
| phase107_patch_items | 3 | Distinct implementation patch items required |
| phase107_all_gaps_have_actions | 1 | 1 means every Phase106 gap has a proposed action |
| phase107_phase106_gap_fraction | 0.1953125 | Inherited Phase106 full-symbol gap fraction |
| phase107_phase106_severe_metric_gap_count | 1 | Inherited Phase106 severe metric count |
| phase107_ready_for_symbol_aware_generator_patch | 1 | 1 means Phase108 can implement overrides |
| phase107_strategy_replay_allowed | 0 | Strategy replay remains closed |

## Patch Contract

| priority | patch_item | symbols_affected | failed_metric_rows | representative_symbols | acceptance_gate |
| --- | --- | --- | --- | --- | --- |
| 1 | add_symbol_depth_scale_override | 9 | 16 | BAJAJ-AUTO;BRITANNIA;GOLDBEES;ITBEES;ITC;LT;M&M;MARUTI | Rerun Phase106-style 32-symbol calibrated realism audit; target <=25% total gaps, no severe metric gap, and strategy replay still locked. |
| 2 | add_symbol_l1_imbalance_skew_override | 15 | 15 | AXISBANK;BAJAJ-AUTO;BHARTIARTL;BPCL;BRITANNIA;HINDUNILVR;INFY;KOTAKBANK | Rerun Phase106-style 32-symbol calibrated realism audit; target <=25% total gaps, no severe metric gap, and strategy replay still locked. |
| 3 | add_symbol_tail_idle_cadence_model | 19 | 19 | ADANIPORTS;AXISBANK;BHARTIARTL;BPCL;BRITANNIA;CIPLA;DRREDDY;GOLDBEES | Rerun Phase106-style 32-symbol calibrated realism audit; target <=25% total gaps, no severe metric gap, and strategy replay still locked. |

## Override Proposal

| symbol | metric | gap_direction | real_value | synthetic_value | synthetic_to_real_ratio | proposed_action | proposed_raw_multiplier | implementation_rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AXISBANK | median_abs_l1_imbalance | synthetic_too_low | 0.549598 | 0.022409 | 0.0407734 | add_symbol_l1_imbalance_skew_override | 4 | L1 imbalance is too damped for this symbol; amplify side imbalance while preserving positive quantities. |
| BAJAJ-AUTO | median_abs_l1_imbalance | synthetic_too_low | 0.578947 | 0 | 0 | add_symbol_l1_imbalance_skew_override | 4 | L1 imbalance is too damped for this symbol; amplify side imbalance while preserving positive quantities. |
| BHARTIARTL | median_abs_l1_imbalance | synthetic_too_low | 0.547826 | 0.0797721 | 0.145616 | add_symbol_l1_imbalance_skew_override | 4 | L1 imbalance is too damped for this symbol; amplify side imbalance while preserving positive quantities. |
| BPCL | median_abs_l1_imbalance | synthetic_too_low | 0.653486 | 0.0528053 | 0.0808055 | add_symbol_l1_imbalance_skew_override | 4 | L1 imbalance is too damped for this symbol; amplify side imbalance while preserving positive quantities. |
| BRITANNIA | median_abs_l1_imbalance | synthetic_too_low | 0.542036 | 0 | 0 | add_symbol_l1_imbalance_skew_override | 4 | L1 imbalance is too damped for this symbol; amplify side imbalance while preserving positive quantities. |
| HINDUNILVR | median_abs_l1_imbalance | synthetic_too_low | 0.627765 | 0.0730897 | 0.116428 | add_symbol_l1_imbalance_skew_override | 4 | L1 imbalance is too damped for this symbol; amplify side imbalance while preserving positive quantities. |
| INFY | median_abs_l1_imbalance | synthetic_too_low | 0.758157 | 0.1875 | 0.24731 | add_symbol_l1_imbalance_skew_override | 4 | L1 imbalance is too damped for this symbol; amplify side imbalance while preserving positive quantities. |
| KOTAKBANK | median_abs_l1_imbalance | synthetic_too_low | 0.670857 | 0.150568 | 0.224441 | add_symbol_l1_imbalance_skew_override | 4 | L1 imbalance is too damped for this symbol; amplify side imbalance while preserving positive quantities. |
| LT | median_abs_l1_imbalance | synthetic_too_low | 0.549296 | 0.0903955 | 0.164566 | add_symbol_l1_imbalance_skew_override | 4 | L1 imbalance is too damped for this symbol; amplify side imbalance while preserving positive quantities. |
| MARUTI | median_abs_l1_imbalance | synthetic_too_low | 0.592949 | 0.132653 | 0.223718 | add_symbol_l1_imbalance_skew_override | 4 | L1 imbalance is too damped for this symbol; amplify side imbalance while preserving positive quantities. |
| ONGC | median_abs_l1_imbalance | synthetic_too_low | 0.612081 | 0.047619 | 0.0777987 | add_symbol_l1_imbalance_skew_override | 4 | L1 imbalance is too damped for this symbol; amplify side imbalance while preserving positive quantities. |
| SBIN | median_abs_l1_imbalance | synthetic_too_low | 0.648919 | 0.047619 | 0.0733821 | add_symbol_l1_imbalance_skew_override | 4 | L1 imbalance is too damped for this symbol; amplify side imbalance while preserving positive quantities. |
| TCS | median_abs_l1_imbalance | synthetic_too_low | 0.682609 | 0.00717703 | 0.0105141 | add_symbol_l1_imbalance_skew_override | 4 | L1 imbalance is too damped for this symbol; amplify side imbalance while preserving positive quantities. |
| TECHM | median_abs_l1_imbalance | synthetic_too_low | 0.625668 | 0.125 | 0.199786 | add_symbol_l1_imbalance_skew_override | 4 | L1 imbalance is too damped for this symbol; amplify side imbalance while preserving positive quantities. |
| WIPRO | median_abs_l1_imbalance | synthetic_too_low | 0.701962 | 0.0960452 | 0.136824 | add_symbol_l1_imbalance_skew_override | 4 | L1 imbalance is too damped for this symbol; amplify side imbalance while preserving positive quantities. |
| BAJAJ-AUTO | median_l1_depth | synthetic_too_high | 61 | 806 | 13.2131 | add_symbol_depth_scale_override | 0.0756824 | Displayed book depth differs by symbol/instrument class; apply symbol-level quantity scale before dense audit. |
| BRITANNIA | median_l1_depth | synthetic_too_high | 35 | 802 | 22.9143 | add_symbol_depth_scale_override | 0.0436409 | Displayed book depth differs by symbol/instrument class; apply symbol-level quantity scale before dense audit. |
| GOLDBEES | median_l1_depth | synthetic_too_low | 11211.5 | 800 | 0.0713553 | add_symbol_depth_scale_override | 14.0144 | Displayed book depth differs by symbol/instrument class; apply symbol-level quantity scale before dense audit. |
| ITBEES | median_l1_depth | synthetic_too_low | 134432 | 802 | 0.00596584 | add_symbol_depth_scale_override | 167.621 | Displayed book depth differs by symbol/instrument class; apply symbol-level quantity scale before dense audit. |
| M&M | median_l1_depth | synthetic_too_high | 47 | 806 | 17.1489 | add_symbol_depth_scale_override | 0.0583127 | Displayed book depth differs by symbol/instrument class; apply symbol-level quantity scale before dense audit. |
| MARUTI | median_l1_depth | synthetic_too_high | 40 | 806 | 20.15 | add_symbol_depth_scale_override | 0.0496278 | Displayed book depth differs by symbol/instrument class; apply symbol-level quantity scale before dense audit. |
| ULTRACEMCO | median_l1_depth | synthetic_too_high | 30 | 808 | 26.9333 | add_symbol_depth_scale_override | 0.0371287 | Displayed book depth differs by symbol/instrument class; apply symbol-level quantity scale before dense audit. |
| BAJAJ-AUTO | median_l5_depth | synthetic_too_high | 366 | 6852.5 | 18.7227 | add_symbol_depth_scale_override | 0.0534112 | Displayed book depth differs by symbol/instrument class; apply symbol-level quantity scale before dense audit. |
| BRITANNIA | median_l5_depth | synthetic_too_high | 406.5 | 6816 | 16.7675 | add_symbol_depth_scale_override | 0.0596391 | Displayed book depth differs by symbol/instrument class; apply symbol-level quantity scale before dense audit. |
| GOLDBEES | median_l5_depth | synthetic_too_low | 95705.5 | 6800 | 0.0710513 | add_symbol_depth_scale_override | 14.0743 | Displayed book depth differs by symbol/instrument class; apply symbol-level quantity scale before dense audit. |
| ITBEES | median_l5_depth | synthetic_too_low | 2.15215e+06 | 6816 | 0.00316706 | add_symbol_depth_scale_override | 315.75 | Displayed book depth differs by symbol/instrument class; apply symbol-level quantity scale before dense audit. |
| ITC | median_l5_depth | synthetic_too_low | 113657 | 6800 | 0.0598291 | add_symbol_depth_scale_override | 16.7143 | Displayed book depth differs by symbol/instrument class; apply symbol-level quantity scale before dense audit. |
| LT | median_l5_depth | synthetic_too_high | 481 | 6850 | 14.2412 | add_symbol_depth_scale_override | 0.070219 | Displayed book depth differs by symbol/instrument class; apply symbol-level quantity scale before dense audit. |
| M&M | median_l5_depth | synthetic_too_high | 447 | 6850 | 15.3244 | add_symbol_depth_scale_override | 0.0652555 | Displayed book depth differs by symbol/instrument class; apply symbol-level quantity scale before dense audit. |
| MARUTI | median_l5_depth | synthetic_too_high | 411 | 6851 | 16.6691 | add_symbol_depth_scale_override | 0.0599912 | Displayed book depth differs by symbol/instrument class; apply symbol-level quantity scale before dense audit. |
| ULTRACEMCO | median_l5_depth | synthetic_too_high | 309 | 6868 | 22.2265 | add_symbol_depth_scale_override | 0.0449913 | Displayed book depth differs by symbol/instrument class; apply symbol-level quantity scale before dense audit. |
| ADANIPORTS | p90_gap_ms | synthetic_too_low | 439477 | 692 | 0.0015746 | add_symbol_tail_idle_cadence_model | 635.082 | Median cadence is mostly inside gate, so p90 gaps need symbol-specific idle/tail spacing rather than one global multiplier. |
| AXISBANK | p90_gap_ms | synthetic_too_low | 305453 | 692 | 0.00226549 | add_symbol_tail_idle_cadence_model | 441.406 | Median cadence is mostly inside gate, so p90 gaps need symbol-specific idle/tail spacing rather than one global multiplier. |
| BHARTIARTL | p90_gap_ms | synthetic_too_low | 3949.1 | 692 | 0.17523 | add_symbol_tail_idle_cadence_model | 5.70679 | Median cadence is mostly inside gate, so p90 gaps need symbol-specific idle/tail spacing rather than one global multiplier. |
| BPCL | p90_gap_ms | synthetic_too_low | 448824 | 692 | 0.00154181 | add_symbol_tail_idle_cadence_model | 648.59 | Median cadence is mostly inside gate, so p90 gaps need symbol-specific idle/tail spacing rather than one global multiplier. |
| BRITANNIA | p90_gap_ms | synthetic_too_low | 450023 | 692 | 0.0015377 | add_symbol_tail_idle_cadence_model | 650.322 | Median cadence is mostly inside gate, so p90 gaps need symbol-specific idle/tail spacing rather than one global multiplier. |
| CIPLA | p90_gap_ms | synthetic_too_low | 447132 | 692 | 0.00154764 | add_symbol_tail_idle_cadence_model | 646.144 | Median cadence is mostly inside gate, so p90 gaps need symbol-specific idle/tail spacing rather than one global multiplier. |
| DRREDDY | p90_gap_ms | synthetic_too_low | 446827 | 692 | 0.0015487 | add_symbol_tail_idle_cadence_model | 645.704 | Median cadence is mostly inside gate, so p90 gaps need symbol-specific idle/tail spacing rather than one global multiplier. |
| GOLDBEES | p90_gap_ms | synthetic_too_low | 439314 | 692 | 0.00157518 | add_symbol_tail_idle_cadence_model | 634.847 | Median cadence is mostly inside gate, so p90 gaps need symbol-specific idle/tail spacing rather than one global multiplier. |
| HINDUNILVR | p90_gap_ms | synthetic_too_low | 442440 | 692 | 0.00156405 | add_symbol_tail_idle_cadence_model | 639.364 | Median cadence is mostly inside gate, so p90 gaps need symbol-specific idle/tail spacing rather than one global multiplier. |
| ITBEES | p90_gap_ms | synthetic_too_low | 446258 | 692 | 0.00155067 | add_symbol_tail_idle_cadence_model | 644.881 | Median cadence is mostly inside gate, so p90 gaps need symbol-specific idle/tail spacing rather than one global multiplier. |
| ITC | p90_gap_ms | synthetic_too_low | 443821 | 692 | 0.00155919 | add_symbol_tail_idle_cadence_model | 641.36 | Median cadence is mostly inside gate, so p90 gaps need symbol-specific idle/tail spacing rather than one global multiplier. |
| JUNIORBEES | p90_gap_ms | synthetic_too_low | 4750 | 692 | 0.145684 | add_symbol_tail_idle_cadence_model | 6.86416 | Median cadence is mostly inside gate, so p90 gaps need symbol-specific idle/tail spacing rather than one global multiplier. |
| KOTAKBANK | p90_gap_ms | synthetic_too_low | 6375 | 692 | 0.108549 | add_symbol_tail_idle_cadence_model | 9.21243 | Median cadence is mostly inside gate, so p90 gaps need symbol-specific idle/tail spacing rather than one global multiplier. |
| LT | p90_gap_ms | synthetic_too_low | 3750.7 | 692 | 0.184499 | add_symbol_tail_idle_cadence_model | 5.42009 | Median cadence is mostly inside gate, so p90 gaps need symbol-specific idle/tail spacing rather than one global multiplier. |
| NESTLEIND | p90_gap_ms | synthetic_too_low | 443604 | 692 | 0.00155995 | add_symbol_tail_idle_cadence_model | 641.046 | Median cadence is mostly inside gate, so p90 gaps need symbol-specific idle/tail spacing rather than one global multiplier. |
| ONGC | p90_gap_ms | synthetic_too_low | 4017 | 692 | 0.172268 | add_symbol_tail_idle_cadence_model | 5.80491 | Median cadence is mostly inside gate, so p90 gaps need symbol-specific idle/tail spacing rather than one global multiplier. |
| SUNPHARMA | p90_gap_ms | synthetic_too_low | 436729 | 692 | 0.00158451 | add_symbol_tail_idle_cadence_model | 631.111 | Median cadence is mostly inside gate, so p90 gaps need symbol-specific idle/tail spacing rather than one global multiplier. |
| TECHM | p90_gap_ms | synthetic_too_low | 3499.7 | 692 | 0.197731 | add_symbol_tail_idle_cadence_model | 5.05737 | Median cadence is mostly inside gate, so p90 gaps need symbol-specific idle/tail spacing rather than one global multiplier. |
| ULTRACEMCO | p90_gap_ms | synthetic_too_low | 450515 | 692 | 0.00153602 | add_symbol_tail_idle_cadence_model | 651.034 | Median cadence is mostly inside gate, so p90 gaps need symbol-specific idle/tail spacing rather than one global multiplier. |
