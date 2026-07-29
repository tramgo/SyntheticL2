# Phase231 Material New Strategy Forms

Generated UTC: 2026-07-29T06:13:12.649617+00:00

Phase231 executes materially new longer-horizon event-bar strategy forms after Phase230 showed that
filtering or inverting the old Phase164 signals could not clear realistic modeled costs.
This is still synthetic-only candidate evidence, not strategy promotion, paper/live acceptance, or a deployable profitability claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase231_material_new_strategy_forms_complete | 1 | Phase231 replay completed |
| phase231_event_bar_rows | 160150 | Event-bar rows scanned |
| phase231_candidate_rows | 72 | Candidate strategy forms replayed |
| phase231_trade_ledger_rows | 50020 | Selected candidate trade rows |
| phase231_train_pass_candidates | 7 | Candidates passing train gates |
| phase231_test_pass_candidates | 8 | Candidates passing test gates |
| phase231_synthetic_candidate_rows | 3 | Candidates passing both train and test gates |
| phase231_best_candidate_id | P231_MICROPRICE_REVERSAL_H3_Q0_9 | Best candidate by pass status and test P&L |
| phase231_best_family_id | P231_MICROPRICE_REVERSAL | Best candidate family |
| phase231_best_train_net_pnl_inr | 353035 | Best candidate train net P&L |
| phase231_best_test_net_pnl_inr | 229963 | Best candidate test net P&L |
| phase231_best_test_precision_cost_clear | 0.59726 | Best candidate test precision cost-clear fraction |
| phase231_strategy_promotion_allowed | 0 | No promotion from synthetic candidate search alone |
| phase231_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from synthetic candidate search alone |
| phase231_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from synthetic candidate search alone |
| phase231_next_best_action | run_phase232_validate_phase231_candidates_on_stricter_holdout_and_negative_controls_no_paper_live | Next validation milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | interpretation |
| --- | --- | --- | --- | --- |
| P231_PHASE230_HANDOFF_CONFIRMED | True | 0 | 0 positive Phase230 expanded groups | Phase231 is justified by Phase230 failure of old signal variants. |
| P231_MATERIAL_NEW_CANDIDATES_REPLAYED | True | 72 | >=18 candidates | Materially new event-bar strategy forms were replayed. |
| P231_TRAIN_PASS_CANDIDATES_FOUND | True | 7 | >0 train-pass candidates | At least one new candidate clears train economics and breadth gates. |
| P231_TEST_PASS_CANDIDATES_FOUND | True | 8 | >0 test-pass candidates | At least one new candidate clears test economics and breadth gates. |
| P231_SYNTHETIC_CANDIDATES_FOUND | True | 3 | >0 train+test pass candidates | Positive synthetic candidates exist, subject to stricter holdout and realism checks before any promotion. |

## Top Candidate Summary

| candidate_id | family_id | signal_source | direction | feature_filter | horizon_event_bars | threshold_quantile | event_window_score_threshold | abs_bar_return_bps_threshold | abs_l5_imbalance_threshold | abs_microprice_dev_threshold | train_months | test_months | train_trades | train_symbols | train_days | train_net_pnl_inr | train_gross_pnl_inr | train_cost_pnl_drag_inr | train_precision_cost_clear | train_positive_months | train_max_day_trade_fraction | train_max_month_contribution_abs | train_max_symbol_contribution_abs | train_gross_to_cost_ratio | test_trades | test_symbols | test_days | test_net_pnl_inr | test_gross_pnl_inr | test_cost_pnl_drag_inr | test_precision_cost_clear | test_positive_months | test_max_day_trade_fraction | test_max_month_contribution_abs | test_max_symbol_contribution_abs | test_gross_to_cost_ratio | train_pass | test_pass | phase231_synthetic_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | P231_MICROPRICE_REVERSAL | avg_microprice_dev | reversal | event_window_score_and_abs_microprice_dev | 3 | 0.9 | 54.3162 | 124.334 | 0.57389 | 0.00010257 | 6 | 6 | 471 | 8 | 18 | 353035 | 420199 | 67164.4 | 0.55414 | 6 | 0.214437 | 0.477958 | 0.289776 | 6.25628 | 365 | 8 | 19 | 229963 | 280316 | 50353.1 | 0.59726 | 4 | 0.156164 | 0.491447 | 0.315216 | 5.567 | True | True | True |
| P231_L5_IMBALANCE_REVERSAL_H3_Q0_9 | P231_L5_IMBALANCE_REVERSAL | avg_l5_imbalance | reversal | event_window_score_and_abs_l5_imbalance | 3 | 0.9 | 54.3162 | 124.334 | 0.57389 | 0.00010257 | 6 | 6 | 376 | 5 | 30 | 63582.2 | 109659 | 46076.5 | 0.553191 | 5 | 0.119681 | 0.380852 | 1.02324 | 2.37993 | 364 | 5 | 28 | 89257.6 | 131819 | 42561.7 | 0.571429 | 4 | 0.0961538 | 0.818469 | 0.564834 | 3.09714 | True | True | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_95 | P231_MICROPRICE_REVERSAL | avg_microprice_dev | reversal | event_window_score_and_abs_microprice_dev | 3 | 0.95 | 72.3652 | 166.608 | 0.697571 | 0.000129284 | 5 | 5 | 165 | 6 | 7 | 113918 | 139137 | 25218.4 | 0.533333 | 3 | 0.266667 | 0.676068 | 0.532067 | 5.51726 | 97 | 5 | 10 | 83574.3 | 97933.8 | 14359.6 | 0.608247 | 3 | 0.226804 | 0.522739 | 0.362964 | 6.82012 | True | True | True |
| P231_EVENT_REVERSAL_H6_Q0_9 | P231_EVENT_REVERSAL | bar_return | reversal | event_window_score_and_abs_bar_return | 6 | 0.9 | 54.3162 | 124.334 | 0.57389 | 0.00010257 | 6 | 6 | 1616 | 32 | 32 | -857379 | -675123 | 182256 | 0.334777 | 2 | 0.10953 | 1.07091 | 0.105864 | 3.70425 | 1994 | 32 | 27 | 1.11159e+06 | 1.33524e+06 | 223654 | 0.569709 | 4 | 0.0882648 | 0.769464 | 0.0687619 | 5.97013 | False | True | False |
| P231_EVENT_REVERSAL_H3_Q0_9 | P231_EVENT_REVERSAL | bar_return | reversal | event_window_score_and_abs_bar_return | 3 | 0.9 | 54.3162 | 124.334 | 0.57389 | 0.00010257 | 6 | 6 | 4625 | 32 | 43 | -945950 | -397369 | 548581 | 0.527784 | 3 | 0.105297 | 1.74613 | 0.0985909 | 0.724358 | 4493 | 32 | 39 | 971630 | 1.49001e+06 | 518377 | 0.60316 | 4 | 0.0892499 | 0.961696 | 0.0891979 | 2.87437 | False | True | False |
| P231_EVENT_REVERSAL_H6_Q0_95 | P231_EVENT_REVERSAL | bar_return | reversal | event_window_score_and_abs_bar_return | 6 | 0.95 | 72.3652 | 166.608 | 0.697571 | 0.000129284 | 5 | 5 | 691 | 32 | 17 | -132571 | -52943.6 | 79627.1 | 0.392185 | 2 | 0.195369 | 4.91053 | 0.338376 | 0.664893 | 1039 | 32 | 17 | 800138 | 915922 | 115785 | 0.617902 | 3 | 0.156882 | 0.870785 | 0.0758821 | 7.91056 | False | True | False |
| P231_EVENT_REVERSAL_H3_Q0_95 | P231_EVENT_REVERSAL | bar_return | reversal | event_window_score_and_abs_bar_return | 3 | 0.95 | 72.3652 | 166.608 | 0.697571 | 0.000129284 | 6 | 6 | 2110 | 32 | 28 | -307734 | -48054.7 | 259680 | 0.543602 | 3 | 0.170142 | 3.46467 | 0.23315 | 0.185054 | 2123 | 32 | 25 | 665199 | 911966 | 246767 | 0.636835 | 4 | 0.111634 | 0.831663 | 0.110104 | 3.69566 | False | True | False |
| P231_EVENT_REVERSAL_H6_Q0_975 | P231_EVENT_REVERSAL | bar_return | reversal | event_window_score_and_abs_bar_return | 6 | 0.975 | 89.9766 | 215.813 | 0.739808 | 0.000152911 | 4 | 5 | 301 | 25 | 7 | -145222 | -110402 | 34819.7 | 0.312292 | 1 | 0.322259 | 2.79463 | 0.200479 | 3.17068 | 538 | 32 | 11 | 270391 | 329651 | 59259.7 | 0.585502 | 3 | 0.297398 | 1.4377 | 0.145175 | 5.56282 | False | False | False |
| P231_EVENT_REVERSAL_H3_Q0_975 | P231_EVENT_REVERSAL | bar_return | reversal | event_window_score_and_abs_bar_return | 3 | 0.975 | 89.9766 | 215.813 | 0.739808 | 0.000152911 | 5 | 6 | 1002 | 32 | 16 | -480271 | -354166 | 126105 | 0.45509 | 2 | 0.239521 | 1.5449 | 0.162868 | 2.80849 | 940 | 32 | 18 | 102745 | 212301 | 109556 | 0.585106 | 3 | 0.170213 | 3.67683 | 0.404799 | 1.93783 | False | True | False |
| P231_MICROPRICE_REVERSAL_H6_Q0_9 | P231_MICROPRICE_REVERSAL | avg_microprice_dev | reversal | event_window_score_and_abs_microprice_dev | 6 | 0.9 | 54.3162 | 124.334 | 0.57389 | 0.00010257 | 4 | 5 | 97 | 8 | 11 | 140921 | 153651 | 12730.3 | 0.628866 | 1 | 0.381443 | 1.03272 | 0.253032 | 12.0698 | 125 | 7 | 14 | 77227.7 | 93125.6 | 15897.9 | 0.584 | 2 | 0.28 | 1.27439 | 0.572806 | 5.85774 | True | False | False |
| P231_MICROPRICE_REVERSAL_H6_Q0_95 | P231_MICROPRICE_REVERSAL | avg_microprice_dev | reversal | event_window_score_and_abs_microprice_dev | 6 | 0.95 | 72.3652 | 166.608 | 0.697571 | 0.000129284 | 2 | 2 | 8 | 4 | 2 | 29275.6 | 30465.1 | 1189.53 | 0.875 | 2 | 0.75 | 0.974019 | 0.853824 | 25.611 | 21 | 3 | 4 | 46677.2 | 49476.6 | 2799.42 | 0.809524 | 2 | 0.47619 | 0.763327 | 0.779088 | 17.6739 | False | False | False |
| P231_L5_IMBALANCE_CONTINUATION_H6_Q0_95 | P231_L5_IMBALANCE_CONTINUATION | avg_l5_imbalance | continuation | event_window_score_and_abs_l5_imbalance | 6 | 0.95 | 72.3652 | 166.608 | 0.697571 | 0.000129284 | 3 | 4 | 10 | 1 | 3 | 24656.6 | 25823.6 | 1167.05 | 1 | 3 | 0.5 | 0.658884 | 1 | 22.1273 | 24 | 2 | 4 | 38455.5 | 41269 | 2813.5 | 0.791667 | 4 | 0.416667 | 0.422457 | 1.04871 | 14.6682 | False | False | False |
| P231_EVENT_CONTINUATION_H3_Q0_99 | P231_EVENT_CONTINUATION | bar_return | continuation | event_window_score_and_abs_bar_return | 3 | 0.99 | 115.817 | 278.876 | 0.741112 | 0.000227005 | 5 | 5 | 314 | 32 | 7 | 172461 | 213625 | 41163.5 | 0.506369 | 3 | 0.308917 | 1.32256 | 0.401948 | 5.18966 | 331 | 31 | 8 | 29090.8 | 67993.2 | 38902.4 | 0.392749 | 2 | 0.356495 | 7.27263 | 0.70646 | 1.74779 | False | False | False |
| P231_L5_IMBALANCE_REVERSAL_H6_Q0_9 | P231_L5_IMBALANCE_REVERSAL | avg_l5_imbalance | reversal | event_window_score_and_abs_l5_imbalance | 6 | 0.9 | 54.3162 | 124.334 | 0.57389 | 0.00010257 | 5 | 6 | 115 | 5 | 19 | 20274.8 | 33297.8 | 13023 | 0.452174 | 3 | 0.165217 | 0.785071 | 2.16438 | 2.55684 | 168 | 5 | 17 | 26519.2 | 45560.5 | 19041.3 | 0.517857 | 3 | 0.119048 | 2.75501 | 2.75889 | 2.39272 | False | False | False |
| P231_MICROPRICE_REVERSAL_H3_Q0_975 | P231_MICROPRICE_REVERSAL | avg_microprice_dev | reversal | event_window_score_and_abs_microprice_dev | 3 | 0.975 | 89.9766 | 215.813 | 0.739808 | 0.000152911 | 5 | 5 | 51 | 3 | 6 | 19507.3 | 27268.4 | 7761.06 | 0.607843 | 3 | 0.333333 | 0.94701 | 1.42616 | 3.51348 | 30 | 3 | 7 | 11826.4 | 16193.3 | 4366.97 | 0.733333 | 3 | 0.333333 | 0.925229 | 0.539706 | 3.70815 | True | False | False |

## Family Summary

| family_id | candidate_rows | train_pass_rows | test_pass_rows | synthetic_candidate_rows | best_train_net_pnl_inr | best_test_net_pnl_inr | best_test_precision_cost_clear |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P231_MICROPRICE_REVERSAL | 12 | 4 | 2 | 2 | 353035 | 229963 | 0.809524 |
| P231_L5_IMBALANCE_REVERSAL | 12 | 1 | 1 | 1 | 63582.2 | 89257.6 | 0.571429 |
| P231_EVENT_REVERSAL | 12 | 0 | 5 | 0 | 0 | 1.11159e+06 | 0.636835 |
| P231_L5_IMBALANCE_CONTINUATION | 12 | 0 | 0 | 0 | 25006.8 | 38455.5 | 0.791667 |
| P231_EVENT_CONTINUATION | 12 | 2 | 0 | 0 | 492866 | 29090.8 | 0.407222 |
| P231_MICROPRICE_CONTINUATION | 12 | 0 | 0 | 0 | 0 | 0 | 0.4 |
