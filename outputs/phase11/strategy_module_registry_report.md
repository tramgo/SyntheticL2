# Phase 11 Strategy Module Registry Report

Generated UTC: 2026-07-13T20:34:56.154742+00:00

## Scope

This artifact converts S01-S11 from strategy concepts into explicit module registry rows.
It does not promote or accept any strategy. S10 is an execution/risk module proxy, and S11 is a risk-filter specification that must not be interpreted as manipulation detection.

## Coverage

| coverage_check | value | target | passed | evidence |
| --- | --- | --- | --- | --- |
| s01_s11_module_rows | 11 | 11 | True | strategy_module_registry.csv |
| implemented_proxy_modules | 11 | 11 | True | strategy_module_registry.csv |
| acceptance_grade_modules | 0 | 0 | True | strategy_module_registry.csv |
| promotion_ready_modules | 0 | 0 | True | strategy_module_registry.csv |
| non_alpha_or_risk_modules | 2 | 2 | True | S10/S11 module_type rows |

## Status Summary

| module_type | implementation_status | modules |
| --- | --- | --- |
| execution_risk_module_proxy | implemented_proxy_non_alpha | 1 |
| partial_signal_module_proxy | implemented_proxy_with_missing_acceptance_features | 4 |
| risk_filter_module_proxy | implemented_proxy_non_manipulation_label | 1 |
| signal_module_proxy | implemented_proxy_signal_diagnostic | 5 |

## Module Registry

| strategy_id | name | role | module_type | implementation_status | support_level | signal_status | module_rows_or_requirements | proxy_features_present | proxy_features_absent | metric_requirements | scenario_requirements | evidence_path | execution_integration | acceptance_grade | promotion_ready | limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | Momentum/breakout filtered by MLOFI | priority | signal_module_proxy | implemented_proxy_signal_diagnostic | runnable_proxy | signal_proxy_available | 164253 | 5 | 0 | 7 | 7 | outputs/phase11/strategy_signal_diagnostics.csv | phase12_execution_summary | False | False | Current proxy uses 5-minute synthetic features, not true 1/5/15/30 second MLOFI lookbacks. |
| S02 | Pure multi-level OFI directional model | priority | signal_module_proxy | implemented_proxy_signal_diagnostic | runnable_proxy | signal_proxy_available | 898620 | 4 | 0 | 7 | 6 | outputs/phase11/strategy_signal_diagnostics.csv | phase12_execution_summary | False | False | Current proxy can compare static imbalance and mlofi_qty at 5-minute event spacing only. |
| S03 | Liquidity-vacuum breakout | priority | partial_signal_module_proxy | implemented_proxy_with_missing_acceptance_features | partial_missing_required_features | partial_signal_proxy_available | 280476 | 4 | 0 | 6 | 7 | outputs/phase11/strategy_feature_availability.csv | phase12_execution_summary | False | False | Only a weak proxy exists because Phase 9 Tier C does not yet carry explicit withdrawal/replenishment rates. |
| S04 | Trade-flow plus depth confirmation | priority | partial_signal_module_proxy | implemented_proxy_with_missing_acceptance_features | partial_missing_required_features | partial_signal_proxy_available | 424887 | 4 | 0 | 5 | 5 | outputs/phase11/strategy_feature_availability.csv | phase12_execution_summary | False | False | Event intensity is not a substitute for signed aggressive trade imbalance. |
| S05 | Microprice entry/exit filter | filter | signal_module_proxy | implemented_proxy_signal_diagnostic | runnable_proxy | signal_proxy_available | 445798 | 4 | 0 | 5 | 5 | outputs/phase11/strategy_signal_diagnostics.csv | phase12_execution_summary | False | False | Standalone microprice results are diagnostic only; plan says not to promote it as a standalone annual-return strategy. |
| S06 | Absorption and exhaustion reversal | priority | partial_signal_module_proxy | implemented_proxy_with_missing_acceptance_features | partial_missing_required_features | partial_signal_proxy_available | 33993 | 4 | 0 | 5 | 6 | outputs/phase11/strategy_feature_availability.csv | phase12_execution_summary | False | False | Can only label absorption-like proxies; top-five market-by-price cannot prove iceberg/participant identity. |
| S07 | Mean reversion after imbalance | priority | signal_module_proxy | implemented_proxy_signal_diagnostic | runnable_proxy | signal_proxy_available | 234925 | 4 | 0 | 5 | 6 | outputs/phase11/strategy_signal_diagnostics.csv | phase12_execution_summary | False | False | Proxy uses imbalance/intensity and regime_code; explicit replenishment is still missing. |
| S08 | Cross-ticker/index lead-lag OFI | research | partial_signal_module_proxy | implemented_proxy_with_missing_acceptance_features | partial_missing_required_features | partial_signal_proxy_available | 442644 | 5 | 0 | 5 | 6 | outputs/phase11/strategy_feature_availability.csv | phase12_execution_summary | False | False | Can compute market-level proxy factors, but causal lead-lag validation requires dedicated synthetic controls. |
| S09 | Pure queue-imbalance scalping | benchmark | signal_module_proxy | implemented_proxy_signal_diagnostic | runnable_proxy | signal_proxy_available | 585341 | 3 | 0 | 4 | 5 | outputs/phase11/strategy_signal_diagnostics.csv | phase12_execution_summary | False | False | Benchmark only. Accuracy above 50% is not sufficient without spread/cost survival. |
| S10 | Passive market making | research_only | execution_risk_module_proxy | implemented_proxy_non_alpha | not_supported_by_current_product | not_alpha_signal | 757 | 0 | 0 | 6 | 7 | outputs/phase12/event_backtest_order_summary.csv | phase12_event_backtester | False | False | Passive market-making module is execution/risk plumbing only; true queue fills are not observed. |
| S11 | Spoof-like wall filter | risk_filter_only | risk_filter_module_proxy | implemented_proxy_non_manipulation_label | not_supported_by_current_product | not_alpha_signal | 5 | 0 | 0 | 4 | 5 | outputs/phase11/strategy_scenario_requirements.csv | risk_filter_requirements_only | False | False | Spoof-like wall module is a risk-filter specification only; it does not classify manipulation or participants. |
