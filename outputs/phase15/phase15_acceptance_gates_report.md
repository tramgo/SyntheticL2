# Phase 15 Strategy Acceptance Gates Report

Generated UTC: 2026-07-13T18:57:41.282079+00:00

## Scope

This phase evaluates whether each strategy may advance from synthetic screening.
Current evidence is insufficient for promotion; all promotion_allowed flags are false.

## Gate Status Summary

| gate_id | gate_name | gate_status | strategies |
| --- | --- | --- | --- |
| G01_predictive | Predictive gate | blocked | 11 |
| G02_economic | Economic gate | blocked | 11 |
| G03_robustness | Robustness gate | blocked | 11 |
| G04_risk | Risk gate | blocked | 11 |
| G05_realism | Realism gate | blocked | 11 |

## Strategy Summary

| strategy_id | name | support_level | passed_gates | blocked_gates | promotion_allowed | acceptance_status |
| --- | --- | --- | --- | --- | --- | --- |
| S01 | Momentum/breakout filtered by MLOFI | runnable_proxy | 0 | 5 | False | blocked_not_promotable |
| S02 | Pure multi-level OFI directional model | runnable_proxy | 0 | 5 | False | blocked_not_promotable |
| S03 | Liquidity-vacuum breakout | partial_missing_required_features | 0 | 5 | False | blocked_not_promotable |
| S04 | Trade-flow plus depth confirmation | partial_missing_required_features | 0 | 5 | False | blocked_not_promotable |
| S05 | Microprice entry/exit filter | runnable_proxy | 0 | 5 | False | blocked_not_promotable |
| S06 | Absorption and exhaustion reversal | partial_missing_required_features | 0 | 5 | False | blocked_not_promotable |
| S07 | Mean reversion after imbalance | runnable_proxy | 0 | 5 | False | blocked_not_promotable |
| S08 | Cross-ticker/index lead-lag OFI | partial_missing_required_features | 0 | 5 | False | blocked_not_promotable |
| S09 | Pure queue-imbalance scalping | runnable_proxy | 0 | 5 | False | blocked_not_promotable |
| S10 | Passive market making | not_supported_by_current_product | 0 | 5 | False | blocked_not_promotable |
| S11 | Spoof-like wall filter | not_supported_by_current_product | 0 | 5 | False | blocked_not_promotable |

## Top Blockers

| strategy_id | gate_id | gate_name | blocker | evidence_source |
| --- | --- | --- | --- | --- |
| S01 | G01_predictive | Predictive gate | No acceptance-level predictive evidence; current diagnostics are proxy-only and/or directional accuracy below threshold. | outputs/phase11/strategy_signal_diagnostics.csv |
| S01 | G02_economic | Economic gate | stressed profile mean_net_return not positive; statutory/brokerage charges are not verified; current cost schedule is placeholder only; execution result is still a 5-minute proxy and not acceptance evidence | outputs/phase12/execution_summary.csv; outputs/phase12/cost_schedule.csv |
| S01 | G03_robustness | Robustness gate | Phase 13 experiments are planned_not_run; no completed multi-seed/walk-forward/parameter-smoothness evidence. | outputs/phase13/experiment_registry.csv |
| S01 | G04_risk | Risk gate | Only sampled proxy risk-control evidence exists; no acceptance-grade full-run drawdown, position-limit, tail-loss or daily-loss-limit validation exists. | outputs/phase12/execution_summary.csv; outputs/phase12_order_lifecycle/risk_control_summary.csv |
| S01 | G05_realism | Realism gate | Synthetic quality has warnings and/or strategy only has proxy/partial support; no holdout generator evidence. | outputs/phase14/quality_gate_summary.csv; outputs/phase11/strategy_validation_matrix.csv |
| S02 | G01_predictive | Predictive gate | No acceptance-level predictive evidence; current diagnostics are proxy-only and/or directional accuracy below threshold. | outputs/phase11/strategy_signal_diagnostics.csv |
| S02 | G02_economic | Economic gate | retail profile mean_net_return not positive; stressed profile mean_net_return not positive; statutory/brokerage charges are not verified; current cost schedule is placeholder only; execution result is still a 5-minute proxy and not acceptance evidence | outputs/phase12/execution_summary.csv; outputs/phase12/cost_schedule.csv |
| S02 | G03_robustness | Robustness gate | Phase 13 experiments are planned_not_run; no completed multi-seed/walk-forward/parameter-smoothness evidence. | outputs/phase13/experiment_registry.csv |
| S02 | G04_risk | Risk gate | Only sampled proxy risk-control evidence exists; no acceptance-grade full-run drawdown, position-limit, tail-loss or daily-loss-limit validation exists. | outputs/phase12/execution_summary.csv; outputs/phase12_order_lifecycle/risk_control_summary.csv |
| S02 | G05_realism | Realism gate | Synthetic quality has warnings and/or strategy only has proxy/partial support; no holdout generator evidence. | outputs/phase14/quality_gate_summary.csv; outputs/phase11/strategy_validation_matrix.csv |
| S03 | G01_predictive | Predictive gate | No acceptance-level predictive evidence; current diagnostics are proxy-only and/or directional accuracy below threshold. | outputs/phase11/strategy_signal_diagnostics.csv |
| S03 | G02_economic | Economic gate | stressed profile mean_net_return not positive; statutory/brokerage charges are not verified; current cost schedule is placeholder only; execution result is still a 5-minute proxy and not acceptance evidence | outputs/phase12/execution_summary.csv; outputs/phase12/cost_schedule.csv |
| S03 | G03_robustness | Robustness gate | Phase 13 experiments are planned_not_run; no completed multi-seed/walk-forward/parameter-smoothness evidence. | outputs/phase13/experiment_registry.csv |
| S03 | G04_risk | Risk gate | Only sampled proxy risk-control evidence exists; no acceptance-grade full-run drawdown, position-limit, tail-loss or daily-loss-limit validation exists. | outputs/phase12/execution_summary.csv; outputs/phase12_order_lifecycle/risk_control_summary.csv |
| S03 | G05_realism | Realism gate | Synthetic quality has warnings and/or strategy only has proxy/partial support; no holdout generator evidence. | outputs/phase14/quality_gate_summary.csv; outputs/phase11/strategy_validation_matrix.csv |
| S04 | G01_predictive | Predictive gate | No acceptance-level predictive evidence; current diagnostics are proxy-only and/or directional accuracy below threshold. | outputs/phase11/strategy_signal_diagnostics.csv |
| S04 | G02_economic | Economic gate | stressed profile mean_net_return not positive; statutory/brokerage charges are not verified; current cost schedule is placeholder only; execution result is still a 5-minute proxy and not acceptance evidence | outputs/phase12/execution_summary.csv; outputs/phase12/cost_schedule.csv |
| S04 | G03_robustness | Robustness gate | Phase 13 experiments are planned_not_run; no completed multi-seed/walk-forward/parameter-smoothness evidence. | outputs/phase13/experiment_registry.csv |
| S04 | G04_risk | Risk gate | Only sampled proxy risk-control evidence exists; no acceptance-grade full-run drawdown, position-limit, tail-loss or daily-loss-limit validation exists. | outputs/phase12/execution_summary.csv; outputs/phase12_order_lifecycle/risk_control_summary.csv |
| S04 | G05_realism | Realism gate | Synthetic quality has warnings and/or strategy only has proxy/partial support; no holdout generator evidence. | outputs/phase14/quality_gate_summary.csv; outputs/phase11/strategy_validation_matrix.csv |
| S05 | G01_predictive | Predictive gate | No acceptance-level predictive evidence; current diagnostics are proxy-only and/or directional accuracy below threshold. | outputs/phase11/strategy_signal_diagnostics.csv |
| S05 | G02_economic | Economic gate | retail profile mean_net_return not positive; stressed profile mean_net_return not positive; statutory/brokerage charges are not verified; current cost schedule is placeholder only; execution result is still a 5-minute proxy and not acceptance evidence | outputs/phase12/execution_summary.csv; outputs/phase12/cost_schedule.csv |
| S05 | G03_robustness | Robustness gate | Phase 13 experiments are planned_not_run; no completed multi-seed/walk-forward/parameter-smoothness evidence. | outputs/phase13/experiment_registry.csv |
| S05 | G04_risk | Risk gate | Only sampled proxy risk-control evidence exists; no acceptance-grade full-run drawdown, position-limit, tail-loss or daily-loss-limit validation exists. | outputs/phase12/execution_summary.csv; outputs/phase12_order_lifecycle/risk_control_summary.csv |
| S05 | G05_realism | Realism gate | Synthetic quality has warnings and/or strategy only has proxy/partial support; no holdout generator evidence. | outputs/phase14/quality_gate_summary.csv; outputs/phase11/strategy_validation_matrix.csv |
| S06 | G01_predictive | Predictive gate | No acceptance-level predictive evidence; current diagnostics are proxy-only and/or directional accuracy below threshold. | outputs/phase11/strategy_signal_diagnostics.csv |
| S06 | G02_economic | Economic gate | retail profile mean_net_return not positive; stressed profile mean_net_return not positive; statutory/brokerage charges are not verified; current cost schedule is placeholder only; execution result is still a 5-minute proxy and not acceptance evidence | outputs/phase12/execution_summary.csv; outputs/phase12/cost_schedule.csv |
| S06 | G03_robustness | Robustness gate | Phase 13 experiments are planned_not_run; no completed multi-seed/walk-forward/parameter-smoothness evidence. | outputs/phase13/experiment_registry.csv |
| S06 | G04_risk | Risk gate | Only sampled proxy risk-control evidence exists; no acceptance-grade full-run drawdown, position-limit, tail-loss or daily-loss-limit validation exists. | outputs/phase12/execution_summary.csv; outputs/phase12_order_lifecycle/risk_control_summary.csv |
| S06 | G05_realism | Realism gate | Synthetic quality has warnings and/or strategy only has proxy/partial support; no holdout generator evidence. | outputs/phase14/quality_gate_summary.csv; outputs/phase11/strategy_validation_matrix.csv |
