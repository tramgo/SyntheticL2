# Phase435 Supervised Full-Depth Event Ranker Execution

Phase435 executes the Phase434 materially new source: a train-only supervised event ranker using L1-L5 book-state features and cost-aware forward labels.

This is an execution result, not a promotion or paper/live decision.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase435_supervised_full_depth_event_ranker_complete | 1 | Phase435 execution completed |
| phase435_thesis_id | P435_SUPERVISED_FULL_DEPTH_EVENT_RANKER_EXECUTION | Execution thesis |
| phase435_synthetic_event_rows | 960 | Synthetic event-label rows |
| phase435_best_scenario_id | P435_full_depth_ranker_validation | Primary validation scenario |
| phase435_best_completed_round_trips | 32 | Primary completed round trips |
| phase435_best_trade_dates | 1 | Primary validation trade dates |
| phase435_best_symbols | 4 | Primary validation symbols |
| phase435_best_positive_date_fraction | 0 | Primary positive-date fraction |
| phase435_best_gross_pnl_inr | 76.56 | Primary gross P&L |
| phase435_best_cost200_inr | 5244.09 | Primary cost200 charges |
| phase435_best_net_pnl_inr | -5167.53 | Primary net P&L |
| phase435_best_annualized_return_pct | -130.222 | Primary annualized return |
| phase435_real_anchor_round_trips | 88 | Real-anchor selected trades |
| phase435_cost200_acceptance_survivor_rows | 0 | Accepted rows after all gates |
| phase435_strategy_promotion_allowed | 0 | No promotion |
| phase435_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase435_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase435_hard_gate_pass_rows | 8 | Passed hard gates |
| phase435_hard_gate_rows | 14 | Hard gates |
| phase435_next_best_action | interpret_phase435_supervised_full_depth_event_ranker_no_paper_live | Recommended next action |

## Scenario Summary

| panel | scenario_id | completed_round_trips | trade_dates | symbols | positive_date_fraction | gross_pnl_inr | cost200_inr | net_pnl_inr | annualized_return_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| synthetic_validation | P435_full_depth_ranker_validation | 32 | 1 | 4 | 0 | 76.56 | 5244.09 | -5167.53 | -130.222 |
| synthetic_validation | P435_l1_only_ablation_validation | 32 | 1 | 4 | 0 | 52.05 | 5243.3 | -5191.25 | -130.82 |
| synthetic_validation | P435_side_flip_control_validation | 32 | 1 | 4 | 0 | -1650.45 | 5243.26 | -6893.71 | -173.722 |
| synthetic_validation | P435_time_shuffle_control_validation | 32 | 1 | 4 | 0 | 2684.55 | 5243.2 | -2558.65 | -64.478 |

## Real-Anchor Summary

| panel | scenario_id | completed_round_trips | trade_dates | symbols | positive_date_fraction | gross_pnl_inr | cost200_inr | net_pnl_inr | annualized_return_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| real_anchor | P435_full_depth_ranker_real_anchor | 88 | 2 | 7 | 0 | -3353.02 | 14497.6 | -17850.6 | -224.917 |

## Learned Weights

| feature | weight | mean | std |
| --- | --- | --- | --- |
| spread_bps_feature | 0.153207 | 2.53329 | 0.747777 |
| book_slope | 0.0608423 | -0.0713259 | 0.0558984 |
| l2_l5_imbalance | -0.0533118 | 0.16526 | 0.120681 |
| top5_imbalance | -0.0520166 | 0.166213 | 0.120036 |
| l1_imbalance | -0.0416156 | 0.173366 | 0.115815 |
| order_churn | 0.0248142 | 0.000670913 | 0.00693001 |
| ask_depth_change | 0.0240852 | 5.91614e-05 | 0.00687304 |
| total_depth_change | 0.0230291 | 0.000194735 | 0.00763688 |
| bid_depth_change | 0.0221321 | 0.000297067 | 0.00836893 |
| book_slope_change | 0.0203458 | -5.80813e-05 | 0.000653066 |
| microtrend_bps | -0.0112282 | 0.425217 | 3.58504 |
| spread_change | 0.0039805 | -0.000106573 | 0.000887817 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P435_PHASE434_PRECOMMIT_USED | True | run_phase435_supervised_full_depth_event_ranker_no_paper_live | phase434_next_action | hard |
| P435_TRAIN_VALIDATION_SPLIT_PRESENT | True | 1 | >0 validation dates | hard |
| P435_FULL_DEPTH_FEATURE_WEIGHTS_NONZERO | True | 0.284557 | >0 | hard |
| P435_L2_L5_MATERIALITY_OVER_L1 | False | 0.59775 | >=5 pct pts | hard |
| P435_SIDE_FLIP_CONTROL_NOT_DOMINANT | True | -173.722 | primary>=side_flip | hard |
| P435_TIME_SHUFFLE_CONTROL_NOT_DOMINANT | False | -64.478 | primary>=time_shuffle | hard |
| P435_COST200_FIXED_CAPITAL | True | cost=2.0;capital=1000000.0;notional=100000.0 | cost200_fixed_capital | hard |
| P435_EVENT_FLOOR | True | 32 | >=30 | hard |
| P435_DATE_BREADTH | False | 1 | >=5 | hard |
| P435_SYMBOL_BREADTH | False | 4 | >=5 | hard |
| P435_POSITIVE_DATE_FRACTION | False | 0 | >=0.6 | hard |
| P435_ANNUALIZED_FLOOR | False | -130.222 | >=12.0 | hard |
| P435_REAL_ANCHOR_CROSS_CHECK | True | -224.917 | same_sign | hard |
| P435_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: no strategy promotion, paper/live acceptance or deployable profitability claim is opened by Phase435.
