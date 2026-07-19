# Phase129 Allowed-Context Label Matrix

Generated UTC: 2026-07-19T23:48:23.644442+00:00

Phase129 materializes the Phase128 no-replay label designs into a diagnostic label matrix.
The labels are context labels only: no buy/sell side, no order/fill simulation, no P&L replay, and no profitability claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase129_label_matrix_rows | 228 | Allowed-context no-replay label matrix rows |
| phase129_symbols | 32 | Symbols represented in Phase129 |
| phase129_months | 8 | Months represented in Phase129 |
| phase129_label_summary_rows | 4 | Label summary rows emitted |
| phase129_binary_labels_with_variation | 3 | Binary diagnostic labels with both classes |
| phase129_gate_rows | 6 | Gates evaluated |
| phase129_all_gates_pass | 1 | 1 means Phase129 obeys no-replay guardrails |
| phase129_strategy_replay_allowed | 0 | Strategy replay remains closed |
| phase129_current_ready_real_anchor_days | 1 | Real anchor days currently ready from Phase117 |
| phase129_additional_real_anchor_days_needed | 4 | Additional real anchor days needed before replay unlock |
| phase129_next_best_action | fit_phase130_no_replay_diagnostic_baselines_or_continue_real_anchor_acquisition | Recommended next milestone |
| phase129_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Cost model retained for audit continuity |

## Label Summary

| label_id | rows | positive_rows | negative_rows | positive_rate | has_class_variation | strategy_replay_allowed | value_counts |
| --- | --- | --- | --- | --- | --- | --- | --- |
| p129_regime_stability_label | 228 | 116 | 112 | 0.508772 | 1 | 0 | {"0": 112, "1": 116} |
| p129_liquidity_opportunity_label | 228 | 44 | 184 | 0.192982 | 1 | 0 | {"0": 184, "1": 44} |
| p129_cost_toxicity_refinement_label | 228 | 84 | 144 | 0.368421 | 1 | 0 | {"0": 144, "1": 84} |
| p129_cost_toxicity_refinement_bucket | 228 |  |  |  | 1 | 0 | {"adverse_touch_cost_toxic": 47, "broad_cost_toxic_no_adverse_touch": 144, "high_adverse_wide_spread_cost_toxic": 37} |

## Thresholds and Rules

| threshold_name | value |
| --- | --- |
| feed_imperfection_median | 0.015872 |
| p90_spread_median | 2.21282 |
| p90_spread_q75 | 2.92923 |
| l1_depth_median | 793.216 |
| l5_depth_median | 6742.37 |
| one_tick_return_std_median | 7.20637e-05 |
| passive_min_adverse_rate_median | 0 |
| passive_min_adverse_rate_q75 | 0.990991 |
| regime_stability_rule | feed_imperfection<=median and p90_spread<=q75 and regime_realism_risk_label=0 and realism_review_flag=0 |
| liquidity_opportunity_rule | l1_depth>=median and l5_depth>=median and one_tick_return_std>=median and p90_spread>=median |
| cost_toxicity_refinement_rule | bucket broad universal cost-toxicity using passive_min_adverse_rate and p90_spread |

## Label Matrix Sample

| trade_month | symbol | priority_bucket | realism_review_flag | candidate_generation_allowed | rows_scanned | feed_imperfection_rate | median_spread_bps | p90_spread_bps | mean_l1_depth | mean_l5_depth | one_tick_return_std | passive_min_adverse_rate | passive_max_cost_clearing_rate | cost_toxicity_label | regime_realism_risk_label | opportunity_abstention_label | p129_regime_stability_label | p129_liquidity_opportunity_label | p129_cost_toxicity_refinement_label | p129_cost_toxicity_refinement_bucket | phase129_scope | strategy_replay_allowed | forbidden_outputs | label_source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | ADANIPORTS | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 2.15994 | 2.1901 | 793.856 | 6747.8 | 0.00010176 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | AXISBANK | P1_clean_allowed | 0 | 1 | 250000 | 0 | 1.47874 | 1.50602 | 794.301 | 6751.73 | 7.9916e-05 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | BAJAJ-AUTO | P2_allowed_with_realism_review | 1 | 1 | 250000 | 0.023808 | 2.85823 | 2.90346 | 792.714 | 6738.09 | 9.29248e-05 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | BANKBEES | P2_allowed_with_realism_review | 1 | 1 | 250000 | 0.023808 | 3.45611 | 3.48224 | 784.619 | 6669.29 | 4.41933e-05 | 0.987179 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | adverse_touch_cost_toxic | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | BHARTIARTL | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 1.54631 | 1.56691 | 792.602 | 6736.89 | 5.25021e-05 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | BPCL | P1_clean_allowed | 0 | 1 | 250000 | 0 | 1.60077 | 1.62127 | 796.047 | 6766.4 | 7.89895e-05 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | BRITANNIA | P1_clean_allowed | 0 | 1 | 250000 | 0 | 3.65464 | 3.70233 | 788.284 | 6700.62 | 6.52266e-05 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | CIPLA | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 2.74348 | 2.78087 | 791.366 | 6726.51 | 7.64578e-05 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | high_adverse_wide_spread_cost_toxic | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | DRREDDY | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 2.38796 | 2.41255 | 787.78 | 6696.35 | 6.11781e-05 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | GOLDBEES | P2_allowed_with_realism_review | 1 | 1 | 250000 | 0.023808 | 0.840477 | 0.850268 | 783.255 | 6657.54 | 5.66937e-05 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | HCLTECH | P2_allowed_with_realism_review | 1 | 1 | 250000 | 0.023808 | 2.40828 | 2.44618 | 796.462 | 6769.73 | 0.000116489 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | high_adverse_wide_spread_cost_toxic | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | HDFCBANK | P2_allowed_with_realism_review | 1 | 1 | 250000 | 0.055552 | 1.19239 | 1.21507 | 795.223 | 6759.47 | 9.86125e-05 | 0.975694 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | adverse_touch_cost_toxic | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | HINDUNILVR | P1_clean_allowed | 0 | 1 | 250000 | 0 | 1.84111 | 1.86428 | 786.493 | 6685 | 7.00539e-05 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | ICICIBANK | P1_clean_allowed | 0 | 1 | 250000 | 0 | 1.3885 | 1.41473 | 794.921 | 6756.75 | 8.20483e-05 | 0.987179 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | adverse_touch_cost_toxic | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | INFY | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 1.77117 | 1.80148 | 797.143 | 6775.83 | 9.20345e-05 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | ITC | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 1.75162 | 1.77022 | 785.651 | 6677.98 | 7.49469e-05 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | adverse_touch_cost_toxic | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | KOTAKBANK | P1_clean_allowed | 0 | 1 | 250000 | 0 | 2.575 | 2.62467 | 795.762 | 6763.86 | 9.47069e-05 | 0 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | LT | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 1.24894 | 1.26557 | 791.827 | 6730.54 | 9.32361e-05 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | M&M | P2_allowed_with_realism_review | 1 | 1 | 250000 | 0.055552 | 1.24054 | 1.2598 | 793.047 | 6740.84 | 0.000102897 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | MARUTI | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 2.84252 | 2.89331 | 793.095 | 6741.22 | 7.79683e-05 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | NESTLEIND | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 2.73504 | 2.77085 | 787.619 | 6694.67 | 8.68305e-05 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | high_adverse_wide_spread_cost_toxic | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | NIFTYBEES | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 1.42964 | 1.44587 | 783.063 | 6655.86 | 6.58799e-05 | 0.990991 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | adverse_touch_cost_toxic | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | ONGC | P1_clean_allowed | 0 | 1 | 250000 | 0 | 1.97973 | 2.01159 | 796.981 | 6774.24 | 9.29665e-05 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | RELIANCE | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 1.5075 | 1.5294 | 796.618 | 6771.28 | 7.08266e-05 | 0.993827 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | adverse_touch_cost_toxic | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | SBIN | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 1.87582 | 1.91644 | 795.682 | 6763.24 | 0.000103729 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | SUNPHARMA | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 2.03863 | 2.06537 | 786.572 | 6685.8 | 8.00573e-05 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | adverse_touch_cost_toxic | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | TCS | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 1.798 | 1.82017 | 796.398 | 6769.17 | 7.69784e-05 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | TECHM | P1_clean_allowed | 0 | 1 | 250000 | 0 | 3.24844 | 3.29663 | 796.492 | 6770.15 | 6.94144e-05 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | ULTRACEMCO | P2_allowed_with_realism_review | 1 | 1 | 250000 | 0.023808 | 2.54151 | 2.5729 | 791.573 | 6728.3 | 9.40858e-05 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | high_adverse_wide_spread_cost_toxic | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-01 | WIPRO | P2_allowed_with_realism_review | 1 | 1 | 250000 | 0.023808 | 2.19479 | 2.22841 | 795.096 | 6758.39 | 7.18543e-05 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-02 | ADANIPORTS | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 2.20325 | 2.21043 | 798.477 | 6786.93 | 6.68748e-05 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-02 | AXISBANK | P2_allowed_with_realism_review | 1 | 1 | 250000 | 0.023808 | 1.50761 | 1.514 | 797.584 | 6779.58 | 5.76769e-05 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-02 | BAJAJ-AUTO | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 2.90135 | 2.91871 | 797.763 | 6780.88 | 8.60896e-05 | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-02 | BANKBEES | P2_allowed_with_realism_review | 1 | 1 | 250000 | 0.023808 | 3.49307 | 3.5021 | 785.428 | 6676.26 | 3.81787e-05 | 0.987179 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | adverse_touch_cost_toxic | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-02 | BHARTIARTL | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 1.56063 | 1.57011 | 796.378 | 6769.08 | 6.87151e-05 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-02 | BPCL | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 1.62153 | 1.63132 | 796.841 | 6773.37 | 6.18573e-05 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-02 | BRITANNIA | P2_allowed_with_realism_review | 1 | 1 | 250000 | 0.031744 | 3.7303 | 3.74462 | 788.571 | 6702.73 | 6.70689e-05 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-02 | CIPLA | P2_allowed_with_realism_review | 1 | 1 | 250000 | 0.031744 | 2.79408 | 2.80308 | 787.823 | 6696.4 | 5.58202e-05 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | high_adverse_wide_spread_cost_toxic | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-02 | DRREDDY | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 2.42346 | 2.43348 | 788.554 | 6702.72 | 4.71197e-05 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-02 | GOLDBEES | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 0.848896 | 0.853825 | 786.936 | 6688.91 | 5.86634e-05 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-02 | HCLTECH | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 2.4422 | 2.45339 | 800.602 | 6805.12 | 6.61073e-05 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | high_adverse_wide_spread_cost_toxic | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-02 | HDFCBANK | P2_allowed_with_realism_review | 1 | 1 | 250000 | 0.023808 | 1.21205 | 1.2184 | 799.286 | 6793.74 | 8.1597e-05 | 0.975694 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | adverse_touch_cost_toxic | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-02 | HINDUNILVR | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 1.87935 | 1.88501 | 789.094 | 6707.19 | 5.35569e-05 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-02 | ICICIBANK | P2_allowed_with_realism_review | 1 | 1 | 250000 | 0.023808 | 1.42157 | 1.42786 | 798.381 | 6786.13 | 6.63121e-05 | 0.987179 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | adverse_touch_cost_toxic | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-02 | INFY | P2_allowed_with_realism_review | 1 | 1 | 250000 | 0.031744 | 1.8044 | 1.81291 | 799.937 | 6799.37 | 7.92862e-05 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-02 | ITBEES | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 3.09502 | 3.10945 | 786.97 | 6688.9 | 5.44865e-05 | 0.996034 | 0 | 1 | 0 | 1 | 0 | 0 | 1 | high_adverse_wide_spread_cost_toxic | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-02 | ITC | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 1.78253 | 1.78859 | 788.921 | 6705.92 | 5.2697e-05 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | adverse_touch_cost_toxic | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-02 | JUNIORBEES | P1_clean_allowed | 0 | 1 | 250000 | 0 | 3.58648 | 3.60092 | 785.444 | 6676.41 | 5.55112e-05 | 0.986111 | 0 | 1 | 0 | 1 | 0 | 0 | 1 | adverse_touch_cost_toxic | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-02 | KOTAKBANK | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 2.61575 | 2.62674 | 799.715 | 6797.8 | 6.97825e-05 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |
| 2026-02 | LT | P1_clean_allowed | 0 | 1 | 250000 | 0 | 1.27136 | 1.27551 | 797.108 | 6775.31 | 7.11801e-05 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | allowed_context_no_replay_label_matrix | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | phase79_partition_profile_plus_phase120_stage02_passive_toxicity;phase128_design_specs |

## Blocked Context Audit

| audit_id | blocked_rows | label_matrix_rows | overlap_rows | overlap_sample | gate_pass |
| --- | --- | --- | --- | --- | --- |
| P129_BLOCKED_CONTEXT_OVERLAP | 156 | 228 | 0 |  | 1 |

## Guardrails

| guardrail_id | requirement | enforcement |
| --- | --- | --- |
| P129_ALLOWED_CONTEXTS_ONLY | The label matrix may contain only rows from the Phase128 allowed feature snapshot. | Rows inherit candidate_generation_allowed=1 and are audited against the blocked exclusion ledger. |
| P129_LABELS_NOT_SIGNALS | Labels describe context diagnostics, not orders, sides, fills, or P&L. | forbidden_outputs=buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| P129_CLASS_VARIATION_REQUIRED | Every binary Phase129 diagnostic label should have class variation before future baseline modeling. | label_summary records has_class_variation for all emitted labels. |
| P129_NO_REPLAY | Strategy replay remains closed. | strategy_replay_allowed=0 across label matrix and summaries. |

## Gate Evaluation

| gate_id | gate_pass | evidence |
| --- | --- | --- |
| P129_LABEL_MATRIX_EXISTS | 1 | label_matrix_rows=228 |
| P129_ALL_ROWS_ALLOWED | 1 | candidate_generation_allowed=1 for every matrix row |
| P129_BLOCKED_CONTEXTS_EXCLUDED | 1 | overlap_rows=0 |
| P129_BINARY_LABEL_CLASS_VARIATION | 1 | binary_labels_checked=3 |
| P129_NO_REPLAY | 1 | strategy_replay_allowed remains 0 |
| P129_REAL_ANCHOR_STILL_PRIMARY | 1 | ready_real_anchor_days=1; days_needed=4 |
