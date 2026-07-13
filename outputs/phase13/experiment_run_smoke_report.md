# Phase 13 Experiment Run Smoke Report

Generated UTC: 2026-07-13T21:22:38.719980+00:00

## Scope

This is a deterministic engineering smoke ledger over the pre-registered Phase 13 initial experiment rows.
It uses existing Phase 11 signal diagnostics and Phase 12 execution summaries; it is not a full experiment execution, parameter search, walk-forward result or promotion result.

## Manifest Summary

- Registered rows evaluated: 324
- Strategies: 9
- Controls: 4
- Execution profile: retail_marketable_default
- Acceptance eligible: False

## Strategy Robustness Smoke Summary

| strategy_id | run_rows | base_rows | negative_control_rows | interpretable_negative_control_rows | passed_negative_control_rows | positive_base_rows | median_base_net_return | worst_control_net_return | robustness_smoke_status | acceptance_eligible | blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | 36 | 9 | 27 | 27 | 18 | 9 | 0.006451115540031 | -0.006451115540031 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S02 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0011430818376006 | -0.00040007864316021 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S03 | 36 | 9 | 27 | 27 | 18 | 9 | 0.0050215903769418 | -0.0050215903769418 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S04 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0004006507711948 | -0.00014022776991817998 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S05 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0022514659545176 | -0.0007880130840811601 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S06 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0017628356795214 | -0.0006169924878324899 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S07 | 36 | 9 | 27 | 0 | 0 | 0 | -0.001066182425619 | -0.00037316384896665 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S08 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0010654318680528 | -0.00037290115381847995 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S09 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0010539616922056 | -0.00036888659227196 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |

## Control Summary

| control_id | run_rows | strategies | mean_proxy_net_return | mean_proxy_signal_fraction | interpretable_rows |
| --- | --- | --- | --- | --- | --- |
| BASE | 81 | 9 | 0.00030323285425122224 | 0.17267142188000106 | 0 |
| NC01 | 81 | 9 | 1.5161642712561107e-05 | 0.17267142188000106 | 18 |
| NC02 | 81 | 9 | 0.00010613149898792776 | 0.15540427969200096 | 18 |
| NC03 | 81 | 9 | -0.00030323285425122224 | 0.17267142188000106 | 18 |

## Caveat

The output closes the bookkeeping gap between a planned registry and an auditable proxy run ledger, but it does not close the acceptance-grade robustness gate.
