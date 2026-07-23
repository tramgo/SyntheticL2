# Phase165 Phase164 Full-year Replay Verdict

Generated UTC: 2026-07-23T12:15:29.109019+00:00

Phase165 turns the completed Phase164 synthetic-only full-year replay into a verdict.
It does not promote strategies, does not claim paper/live readiness, and does not claim deployable profitability.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase165_outcome | A_SYNTHETIC_FULL_YEAR_REPLAY_FALSIFIED | Selected Phase165 outcome |
| phase165_full_year_complete | 1 | Inherited Phase164 full-year completion |
| phase165_positive_after_cost_rows | 0 | Inherited Phase164 positive rows |
| phase165_synthetic_replay_candidate_rows | 0 | Inherited Phase164 candidate rows |
| phase165_best_strategy_id | P164_S06_ABSORPTION_REVERSAL | Best Phase164 strategy/profile by annual net P&L |
| phase165_best_annual_net_pnl_inr | -189513 | Best annual net P&L remains synthetic-only |
| phase165_strategy_promotion_allowed | 0 | Strategy promotion remains closed |
| phase165_paper_or_live_acceptance_allowed | 0 | Paper/live broker acceptance remains closed |
| phase165_next_best_action | stop_current_phase164_strategy_forms_or_design_new_precommitted_non_blocklisted_hypothesis | Recommended next milestone |

## Verdict

| verdict_id | outcome | decision | phase164_full_year_complete | phase164_positive_after_cost_rows | phase164_synthetic_replay_candidate_rows | best_strategy_id | best_execution_profile | best_annual_net_pnl_inr | strategy_promotion_allowed | paper_or_live_acceptance_allowed | deployable_profitability_claim_allowed | next_best_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| phase165_phase164_full_year_replay_verdict | A_SYNTHETIC_FULL_YEAR_REPLAY_FALSIFIED | close_phase164_current_guarded_diagnostic_forms | 1 | 0 | 0 | P164_S06_ABSORPTION_REVERSAL | zero_latency_spread_only_control | -189513 | 0 | 0 | 0 | stop_current_phase164_strategy_forms_or_design_new_precommitted_non_blocklisted_hypothesis |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | interpretation |
| --- | --- | --- | --- | --- |
| P165_FULL_YEAR_REPLAY_COMPLETE | True | 384 | 384 | Phase164 covered every Phase162 dense month/symbol shard. |
| P165_POSITIVE_AFTER_COST_ECONOMICS | False | 0 | >0 strategy/profile rows | At least one strategy/profile must be net-positive after Zerodha-style costs to continue as a candidate. |
| P165_SYNTHETIC_REPLAY_CANDIDATE | False | 0 | >0 positive plus risk-proxy-pass rows | A replay candidate must clear both economics and risk proxy screens. |
| P165_BEST_PROFILE_NET_POSITIVE | False | -189513 | >0 INR annual net P&L | Best observed Phase164 strategy/profile is still negative if this gate fails. |
| P165_PROMOTION_BOUNDARY_CLOSED | True | 0 | 0 | Synthetic replay verdict must not promote a strategy. |
| P165_BROKER_BOUNDARY_CLOSED | True | 0 | 0 | Synthetic replay verdict must not claim paper/live or broker readiness. |
| P165_DEPLOYABLE_CLAIM_CLOSED | True | 0 | 0 | Synthetic replay verdict must not make a deployable profitability claim. |

## Blocklist Candidate Update

| blocked_family_id | source_strategy_id | phase164_strategy_ids | best_annual_net_pnl_inr | positive_after_cost_rows | synthetic_replay_candidate_rows | recommended_status | unlock_condition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PHASE164_S01_GUARDED_DIAGNOSTIC | S01 | P164_S01_MLOFI_BREAKOUT | -4.73255e+06 | 0 | 0 | block_current_phase164_form | new precommitted feature hypothesis, changed label/execution contract, or real-anchor evidence; do not rerun same Phase164 form hoping for profit |
| PHASE164_S02_GUARDED_DIAGNOSTIC | S02 | P164_S02_MULTI_LEVEL_OFI | -1.04276e+07 | 0 | 0 | block_current_phase164_form | new precommitted feature hypothesis, changed label/execution contract, or real-anchor evidence; do not rerun same Phase164 form hoping for profit |
| PHASE164_S03_GUARDED_DIAGNOSTIC | S03 | P164_S03_LIQUIDITY_VACUUM | -3.3266e+06 | 0 | 0 | block_current_phase164_form | new precommitted feature hypothesis, changed label/execution contract, or real-anchor evidence; do not rerun same Phase164 form hoping for profit |
| PHASE164_S04_GUARDED_DIAGNOSTIC | S04 | P164_S04_TRADE_FLOW_DEPTH | -809134 | 0 | 0 | block_current_phase164_form | new precommitted feature hypothesis, changed label/execution contract, or real-anchor evidence; do not rerun same Phase164 form hoping for profit |
| PHASE164_S05_GUARDED_DIAGNOSTIC | S05 | P164_S05_MICROPRICE_FILTER | -320466 | 0 | 0 | block_current_phase164_form | new precommitted feature hypothesis, changed label/execution contract, or real-anchor evidence; do not rerun same Phase164 form hoping for profit |
| PHASE164_S06_GUARDED_DIAGNOSTIC | S06 | P164_S06_ABSORPTION_REVERSAL | -189513 | 0 | 0 | block_current_phase164_form | new precommitted feature hypothesis, changed label/execution contract, or real-anchor evidence; do not rerun same Phase164 form hoping for profit |
| PHASE164_S07_GUARDED_DIAGNOSTIC | S07 | P164_S07_IMBALANCE_MEAN_REVERSION | -1.15997e+07 | 0 | 0 | block_current_phase164_form | new precommitted feature hypothesis, changed label/execution contract, or real-anchor evidence; do not rerun same Phase164 form hoping for profit |
| PHASE164_S09_GUARDED_DIAGNOSTIC | S09 | P164_S09_QUEUE_IMBALANCE_SCALP | -692233 | 0 | 0 | block_current_phase164_form | new precommitted feature hypothesis, changed label/execution contract, or real-anchor evidence; do not rerun same Phase164 form hoping for profit |

## Phase164 Strategy Summary

| strategy_id | source_strategy_id | feature_family | feature_status | execution_profile | trade_dates | trades | annual_net_pnl_inr | mean_net_return_per_trade | mean_gross_return_per_trade | mean_cost_return_per_trade | worst_daily_net_pnl_inr | max_drawdown_inr | worst_trade_pnl_inr | positive_day_fraction | annualized_sharpe_proxy | positive_after_costs | risk_proxy_pass | synthetic_replay_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P164_S06_ABSORPTION_REVERSAL | S06 | absorption_exhaustion_reversal | replayable_from_local_l1_l5_book_state | zero_latency_spread_only_control | 233 | 9603 | -189513 | -0.000197347 | 0 | 0.000197347 | -13555.1 | -189505 | -43.1143 | 0 | -6.52241 | False | True | False |
| P164_S05_MICROPRICE_FILTER | S05 | microprice_with_depth_filter | replayable_from_local_l1_l5_book_state | zero_latency_spread_only_control | 61 | 35518 | -320466 | -9.02264e-05 | 3.32689e-07 | 9.05591e-05 | -45908.3 | -317921 | -1793.05 | 0 | -10.9357 | False | False | False |
| P164_S09_QUEUE_IMBALANCE_SCALP | S09 | queue_imbalance_scalping_guarded | replayable_from_local_l1_l5_book_state_guarded_not_phase52_dense_id | zero_latency_spread_only_control | 95 | 79552 | -692233 | -8.70165e-05 | 1.03155e-06 | 8.8048e-05 | -34334.6 | -687912 | -741.707 | 0 | -21.182 | False | False | False |
| P164_S04_TRADE_FLOW_DEPTH | S04 | trade_flow_depth_confirmation | replayable_from_local_l1_l5_book_state | zero_latency_spread_only_control | 225 | 41762 | -809134 | -0.000193749 | 0 | 0.000193749 | -41666.2 | -808314 | -51.471 | 0 | -7.80341 | False | False | False |
| P164_S06_ABSORPTION_REVERSAL | S06 | absorption_exhaustion_reversal | replayable_from_local_l1_l5_book_state | retail_marketable_default | 233 | 9417 | -1.38206e+06 | -0.00146762 | 0 | 0.00146762 | -81625 | -1.38195e+06 | -217.024 | 0 | -7.96365 | False | False | False |
| P164_S06_ABSORPTION_REVERSAL | S06 | absorption_exhaustion_reversal | replayable_from_local_l1_l5_book_state | stressed_retail | 233 | 9417 | -1.89422e+06 | -0.00201149 | 0 | 0.00201149 | -115444 | -1.89408e+06 | -318.253 | 0 | -7.72096 | False | False | False |
| P164_S03_LIQUIDITY_VACUUM | S03 | liquidity_vacuum_breakout | replayable_from_local_l1_l5_book_state | zero_latency_spread_only_control | 55 | 274177 | -3.3266e+06 | -0.00012133 | 0 | 0.00012133 | -278691 | -3.25044e+06 | -51.5187 | 0 | -13.9373 | False | False | False |
| P164_S05_MICROPRICE_FILTER | S05 | microprice_with_depth_filter | replayable_from_local_l1_l5_book_state | retail_marketable_default | 67 | 35249 | -4.04311e+06 | -0.00114701 | 2.77814e-07 | 0.00114729 | -434670 | -4.00765e+06 | -1896.16 | 0 | -13.0501 | False | False | False |
| P164_S01_MLOFI_BREAKOUT | S01 | momentum_breakout_mlofi | replayable_from_local_l1_l5_book_state | zero_latency_spread_only_control | 240 | 224845 | -4.73255e+06 | -0.000210481 | -9.95981e-07 | 0.000209485 | -334617 | -4.73202e+06 | -755.755 | 0 | -6.68854 | False | False | False |
| P164_S05_MICROPRICE_FILTER | S05 | microprice_with_depth_filter | replayable_from_local_l1_l5_book_state | stressed_retail | 67 | 35235 | -5.20578e+06 | -0.00147745 | 2.77925e-07 | 0.00147772 | -573650 | -5.16066e+06 | -1926.59 | 0 | -12.8122 | False | False | False |
| P164_S04_TRADE_FLOW_DEPTH | S04 | trade_flow_depth_confirmation | replayable_from_local_l1_l5_book_state | retail_marketable_default | 225 | 41392 | -6.03399e+06 | -0.00145777 | 0 | 0.00145777 | -275080 | -6.02609e+06 | -242.094 | 0 | -8.85837 | False | False | False |
| P164_S04_TRADE_FLOW_DEPTH | S04 | trade_flow_depth_confirmation | replayable_from_local_l1_l5_book_state | stressed_retail | 225 | 41392 | -8.258e+06 | -0.00199507 | 0 | 0.00199507 | -383596 | -8.24753e+06 | -360.036 | 0 | -8.69616 | False | False | False |
| P164_S09_QUEUE_IMBALANCE_SCALP | S09 | queue_imbalance_scalping_guarded | replayable_from_local_l1_l5_book_state_guarded_not_phase52_dense_id | retail_marketable_default | 102 | 79404 | -9.05188e+06 | -0.00113998 | 1.04392e-06 | 0.00114102 | -426719 | -8.98262e+06 | -847.756 | 0 | -21.0213 | False | False | False |
| P164_S02_MULTI_LEVEL_OFI | S02 | multi_level_order_flow_imbalance | replayable_from_local_l1_l5_book_state | zero_latency_spread_only_control | 211 | 851193 | -1.04276e+07 | -0.000122506 | -1.17587e-06 | 0.00012133 | -329721 | -1.03858e+07 | -1793.05 | 0 | -12.266 | False | False | False |
| P164_S07_IMBALANCE_MEAN_REVERSION | S07 | imbalance_mean_reversion | replayable_from_local_l1_l5_book_state | zero_latency_spread_only_control | 205 | 1034938 | -1.15997e+07 | -0.000112081 | 7.01067e-07 | 0.000112782 | -370151 | -1.15743e+07 | -3251.44 | 0 | -14.8963 | False | False | False |
| P164_S09_QUEUE_IMBALANCE_SCALP | S09 | queue_imbalance_scalping_guarded | replayable_from_local_l1_l5_book_state_guarded_not_phase52_dense_id | stressed_retail | 102 | 79384 | -1.1639e+07 | -0.00146616 | 1.04418e-06 | 0.00146721 | -549309 | -1.15513e+07 | -881.123 | 0 | -20.9647 | False | False | False |
| P164_S01_MLOFI_BREAKOUT | S01 | momentum_breakout_mlofi | replayable_from_local_l1_l5_book_state | retail_marketable_default | 240 | 222626 | -3.35295e+07 | -0.00150609 | -1.00643e-06 | 0.00150508 | -2.08476e+06 | -3.35235e+07 | -896.846 | 0 | -7.70636 | False | False | False |
| P164_S03_LIQUIDITY_VACUUM | S03 | liquidity_vacuum_breakout | replayable_from_local_l1_l5_book_state | retail_marketable_default | 55 | 271703 | -3.37073e+07 | -0.00124059 | 0 | 0.00124059 | -1.81802e+06 | -3.27935e+07 | -242.237 | 0 | -16.4724 | False | False | False |
| P164_S03_LIQUIDITY_VACUUM | S03 | liquidity_vacuum_breakout | replayable_from_local_l1_l5_book_state | stressed_retail | 55 | 271703 | -4.43722e+07 | -0.00163312 | 0 | 0.00163312 | -2.5387e+06 | -4.31901e+07 | -360.275 | 0 | -16.2898 | False | False | False |
| P164_S01_MLOFI_BREAKOUT | S01 | momentum_breakout_mlofi | replayable_from_local_l1_l5_book_state | stressed_retail | 240 | 222610 | -4.61887e+07 | -0.00207487 | -1.0065e-06 | 0.00207387 | -2.93467e+06 | -4.6181e+07 | -965.257 | 0 | -7.54174 | False | False | False |
| P164_S02_MULTI_LEVEL_OFI | S02 | multi_level_order_flow_imbalance | replayable_from_local_l1_l5_book_state | retail_marketable_default | 218 | 844099 | -1.04826e+08 | -0.00124187 | -1.16599e-06 | 0.00124071 | -3.49757e+06 | -1.04407e+08 | -1896.16 | 0 | -11.6637 | False | False | False |
| P164_S07_IMBALANCE_MEAN_REVERSION | S07 | imbalance_mean_reversion | replayable_from_local_l1_l5_book_state | retail_marketable_default | 217 | 1026340 | -1.24628e+08 | -0.0012143 | 6.88635e-07 | 0.00121499 | -3.71707e+06 | -1.24328e+08 | -3361.85 | 0 | -15.0182 | False | False | False |
| P164_S02_MULTI_LEVEL_OFI | S02 | multi_level_order_flow_imbalance | replayable_from_local_l1_l5_book_state | stressed_retail | 218 | 844075 | -1.37964e+08 | -0.0016345 | -1.16603e-06 | 0.00163334 | -4.57532e+06 | -1.3741e+08 | -1926.59 | 0 | -11.7037 | False | False | False |
| P164_S07_IMBALANCE_MEAN_REVERSION | S07 | imbalance_mean_reversion | replayable_from_local_l1_l5_book_state | stressed_retail | 217 | 1026316 | -1.63162e+08 | -0.00158978 | 6.88651e-07 | 0.00159047 | -4.90239e+06 | -1.62772e+08 | -3399.59 | 0 | -14.9347 | False | False | False |
