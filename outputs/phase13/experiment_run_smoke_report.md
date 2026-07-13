# Phase 13 Experiment Run Smoke Report

Generated UTC: 2026-07-13T19:04:20.034054+00:00

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
| S01 | 36 | 9 | 27 | 27 | 18 | 9 | 0.0070974050013031 | -0.0070974050013031 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S02 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0004680759018443 | -0.000163826565645505 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S03 | 36 | 9 | 27 | 27 | 18 | 9 | 0.0057049313943136 | -0.0057049313943136 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S04 | 36 | 9 | 27 | 27 | 18 | 9 | 0.0002777712811128 | -0.0002777712811128 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S05 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0015733648681609 | -0.000550677703856315 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S06 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0011334731433737 | -0.00039671560018079494 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S07 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0003894661605982 | -0.00013631315620936998 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S08 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0003902348806092 | -0.00013658220821322 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S09 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0003762153116148 | -0.00013167535906517998 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |

## Control Summary

| control_id | run_rows | strategies | mean_proxy_net_return | mean_proxy_signal_fraction | interpretable_rows |
| --- | --- | --- | --- | --- | --- |
| BASE | 81 | 9 | 0.0009721419345031556 | 0.172239021400988 | 0 |
| NC01 | 81 | 9 | 4.860709672515778e-05 | 0.172239021400988 | 27 |
| NC02 | 81 | 9 | 0.0003402496770761044 | 0.15501511926088923 | 27 |
| NC03 | 81 | 9 | -0.0009721419345031556 | 0.172239021400988 | 27 |

## Caveat

The output closes the bookkeeping gap between a planned registry and an auditable proxy run ledger, but it does not close the acceptance-grade robustness gate.
