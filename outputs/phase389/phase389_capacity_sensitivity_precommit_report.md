# Phase389 Capacity Sensitivity Precommit

Generated: 2026-08-11T20:15:49.545257+00:00

| metric | value | description |
| --- | --- | --- |
| phase389_capacity_sensitivity_precommit_complete | 1 | Phase389 complete |
| phase389_capacity_ladder | 2;3;4 | Capacities to test |
| phase389_baseline_capacity_selected_trades | 21 | Baseline selected trades |
| phase389_raw_scheduled_candidates | 30 | Raw scheduled candidates |
| phase389_selected_trade_gap | 9 | Selected-trade gap |
| phase389_alpha_parameter_change_allowed | 0 | No alpha parameter changes |
| phase389_promotion_from_sensitivity_allowed | 0 | No promotion from sensitivity |
| phase389_next_best_action | execute_phase390_capacity_rule_sensitivity_no_paper_live | Recommended next action |

| contract_id | source_phase | frozen_primary_scenario_id | capacity_ladder | baseline_capacity | baseline_capacity_selected_trades | raw_scheduled_candidates | selected_trade_gap | alpha_parameter_change_allowed | cost_model_change_allowed | depth_rule_change_allowed | capital_adjustment_required_for_capacity_gt_2 | promotion_from_sensitivity_allowed | paper_live_or_profit_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P389_CAPACITY_RULE_SENSITIVITY_PRECOMMIT | Phase388 | P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | 2;3;4 | 2 | 21 | 30 | 9 | 0 | 0 | 0 | 1 | 0 | 0 |

| gate_id | passed | evidence |
| --- | --- | --- |
| P389_PHASE388_PRESENT | 1 | Phase388 complete |
| P389_CAPACITY_BOTTLENECK_PRESENT | 1 | raw=30; selected=21; gap=9 |
| P389_ALPHA_COST_DEPTH_FROZEN | 1 | capacity sensitivity only |
| P389_CAPITAL_ADJUSTMENT_REQUIRED | 1 | annualized returns use max(250k, capacity*100k) |
| P389_NO_PROMOTION_PAPER_LIVE | 1 | diagnostic_only |
