# Phase 23 Key Risk Register

Generated UTC: 2026-07-14T17:42:35.503767+00:00

This register converts the plan's key-risk section into auditable current-state controls.
It is a governance artifact, not strategy-promotion evidence.

## Summary

| metric | value | description |
| --- | --- | --- |
| phase23_risks | 5 | Key risk rows from the plan |
| phase23_high_risks | 4 | High-severity risk rows |
| phase23_open_acceptance_blocking_risks | 5 | Risks still blocking acceptance or promotion |
| phase23_mitigation_rows | 31 | Mitigation ledger rows |
| phase23_promotion_steps | 7 | Governed promotion path steps |
| phase23_promotion_ready | 0 | No strategy is ready to advance beyond synthetic screening |

## Risk Register

| risk_id | risk_title | risk_category | risk_description | severity | current_status | observed_value | plan_mitigations | required_next_action | acceptance_blocking |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R23_01_synthetic_alpha | Synthetic alpha | model_artifact | The generator may accidentally encode a predictable relationship that strategies exploit. | high | open_controls_proxy_only | negative_control_open_rows=11; holdout_or_artifact_open_rows=22; phase21_extension_or_paper_ready=0 | negative-control generators; multiple model families; hidden holdout generator; parameter perturbation; real-data paper testing; generator-blind strategy development | Run acceptance-grade negative controls, holdout-generator strategy reruns and real-data paper tests before promotion. | True |
| R23_02_one_day_overfitting | One-day overfitting | data_coverage | The sample day may be unusual. | high | open_until_multiday_class_b_capture | class_b_event_grade_days=0; ready_recalibration_tasks=0 | pooled shrinkage; broad stress ranges; explicit uncertainty bands; multiple synthetic normal-day configurations; immediate recalibration with new real days | Collect Class B event-grade multi-day data and rerun Phase 22 recalibration tasks. | True |
| R23_03_unrealistic_fills | Unrealistic fills | execution_model | Execution assumptions may overstate attainable fills and understate adverse selection. | high | open_until_broker_reconciled_lifecycle | risk_open_rows=88; economic_open_rows=88 | pessimistic execution; marketable-order focus initially; latency simulation; partial fills; depth walk; adverse-selection modelling | Run broker/exchange fill provenance, contract-note reconciliation and full lifecycle execution replay. | True |
| R23_04_excessive_data_volume | Excessive data volume | storage_compute | Raw and synthetic L2 data volume may make repeated experiments slow or costly. | medium | mitigated_by_current_storage_design_monitor | duckdb_report_present=True; full_year_conservative_total_gb=83.240 | event-driven generation; integer encoding; Parquet/Zstandard; delta-state representation; separate raw and feature tiers; selected dense tickers; feature-only datasets for repeated experiments | Keep Parquet/Zstandard durable storage and DuckDB query layer; re-estimate before materializing larger horizons. | True |
| R23_05_false_confidence_three_months | False confidence from three months | governance | Three synthetic months are a screening laboratory, not a profitability proof. | high | open_governance_gate | phase20_acceptance_ready_rows=0; phase21_extension_or_paper_ready=0 | synthetic engineering test; synthetic multi-regime stress test; real-data historical test; live paper trading; shadow execution; very small capital; gradual scale-up | Preserve staged promotion path; do not skip from synthetic screening to capital deployment. | True |

## Mitigation Ledger

| risk_id | mitigation_rank | mitigation | mitigation_status | current_evidence_status |
| --- | --- | --- | --- | --- |
| R23_01_synthetic_alpha | 1 | negative-control generators | required_before_acceptance | open_controls_proxy_only |
| R23_01_synthetic_alpha | 2 | multiple model families | required_before_acceptance | open_controls_proxy_only |
| R23_01_synthetic_alpha | 3 | hidden holdout generator | required_before_acceptance | open_controls_proxy_only |
| R23_01_synthetic_alpha | 4 | parameter perturbation | required_before_acceptance | open_controls_proxy_only |
| R23_01_synthetic_alpha | 5 | real-data paper testing | required_before_acceptance | open_controls_proxy_only |
| R23_01_synthetic_alpha | 6 | generator-blind strategy development | required_before_acceptance | open_controls_proxy_only |
| R23_02_one_day_overfitting | 1 | pooled shrinkage | required_before_acceptance | open_until_multiday_class_b_capture |
| R23_02_one_day_overfitting | 2 | broad stress ranges | required_before_acceptance | open_until_multiday_class_b_capture |
| R23_02_one_day_overfitting | 3 | explicit uncertainty bands | required_before_acceptance | open_until_multiday_class_b_capture |
| R23_02_one_day_overfitting | 4 | multiple synthetic normal-day configurations | required_before_acceptance | open_until_multiday_class_b_capture |
| R23_02_one_day_overfitting | 5 | immediate recalibration with new real days | required_before_acceptance | open_until_multiday_class_b_capture |
| R23_03_unrealistic_fills | 1 | pessimistic execution | required_before_acceptance | open_until_broker_reconciled_lifecycle |
| R23_03_unrealistic_fills | 2 | marketable-order focus initially | required_before_acceptance | open_until_broker_reconciled_lifecycle |
| R23_03_unrealistic_fills | 3 | latency simulation | required_before_acceptance | open_until_broker_reconciled_lifecycle |
| R23_03_unrealistic_fills | 4 | partial fills | required_before_acceptance | open_until_broker_reconciled_lifecycle |
| R23_03_unrealistic_fills | 5 | depth walk | required_before_acceptance | open_until_broker_reconciled_lifecycle |
| R23_03_unrealistic_fills | 6 | adverse-selection modelling | required_before_acceptance | open_until_broker_reconciled_lifecycle |
| R23_04_excessive_data_volume | 1 | event-driven generation | implemented_or_monitored_currently | mitigated_by_current_storage_design_monitor |
| R23_04_excessive_data_volume | 2 | integer encoding | implemented_or_monitored_currently | mitigated_by_current_storage_design_monitor |
| R23_04_excessive_data_volume | 3 | Parquet/Zstandard | implemented_or_monitored_currently | mitigated_by_current_storage_design_monitor |
| R23_04_excessive_data_volume | 4 | delta-state representation | implemented_or_monitored_currently | mitigated_by_current_storage_design_monitor |
| R23_04_excessive_data_volume | 5 | separate raw and feature tiers | implemented_or_monitored_currently | mitigated_by_current_storage_design_monitor |
| R23_04_excessive_data_volume | 6 | selected dense tickers | implemented_or_monitored_currently | mitigated_by_current_storage_design_monitor |
| R23_04_excessive_data_volume | 7 | feature-only datasets for repeated experiments | implemented_or_monitored_currently | mitigated_by_current_storage_design_monitor |
| R23_05_false_confidence_three_months | 1 | synthetic engineering test | required_before_acceptance | open_governance_gate |
| R23_05_false_confidence_three_months | 2 | synthetic multi-regime stress test | required_before_acceptance | open_governance_gate |
| R23_05_false_confidence_three_months | 3 | real-data historical test | required_before_acceptance | open_governance_gate |
| R23_05_false_confidence_three_months | 4 | live paper trading | required_before_acceptance | open_governance_gate |
| R23_05_false_confidence_three_months | 5 | shadow execution | required_before_acceptance | open_governance_gate |
| R23_05_false_confidence_three_months | 6 | very small capital | required_before_acceptance | open_governance_gate |
| R23_05_false_confidence_three_months | 7 | gradual scale-up | required_before_acceptance | open_governance_gate |

## Promotion Path Guardrail

| promotion_step_id | promotion_order | promotion_step | current_status | skip_allowed |
| --- | --- | --- | --- | --- |
| P23_01 | 1 | Synthetic engineering test | current_proxy_running | False |
| P23_02 | 2 | Synthetic multi-regime stress test | proxy_partial_not_acceptance | False |
| P23_03 | 3 | Real-data historical test | blocked_missing_class_b_multiday | False |
| P23_04 | 4 | Live paper trading | blocked_until_historical_acceptance | False |
| P23_05 | 5 | Shadow execution | blocked_until_paper_trading | False |
| P23_06 | 6 | Very small capital | blocked_until_shadow_execution | False |
| P23_07 | 7 | Gradual scale-up | blocked_until_small_capital_risk_limits | False |
