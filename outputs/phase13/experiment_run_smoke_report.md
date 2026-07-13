# Phase 13 Experiment Run Smoke Report

Generated UTC: 2026-07-13T20:47:02.130086+00:00

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
| S01 | 36 | 9 | 27 | 27 | 18 | 9 | 0.0062170868335706 | -0.0062170868335706 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S02 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0013769304654395 | -0.000481925662903825 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S03 | 36 | 9 | 27 | 27 | 18 | 9 | 0.004786972092235 | -0.004786972092235 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S04 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0006351917982472 | -0.00022231712938651998 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S05 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0024854949298585 | -0.000869923225450475 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S06 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0019972368383924 | -0.00069903289343734 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S07 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0013001708088885 | -0.000455059783110975 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S08 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0012993403451723 | -0.00045476912081030495 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S09 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0012877923140321 | -0.000450727309911235 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |

## Control Summary

| control_id | run_rows | strategies | mean_proxy_net_return | mean_proxy_signal_fraction | interpretable_rows |
| --- | --- | --- | --- | --- | --- |
| BASE | 81 | 9 | 6.910015841945541e-05 | 0.17267142188000106 | 0 |
| NC01 | 81 | 9 | 3.45500792097277e-06 | 0.17267142188000106 | 18 |
| NC02 | 81 | 9 | 2.4185055446809358e-05 | 0.15540427969200096 | 18 |
| NC03 | 81 | 9 | -6.910015841945541e-05 | 0.17267142188000106 | 18 |

## Caveat

The output closes the bookkeeping gap between a planned registry and an auditable proxy run ledger, but it does not close the acceptance-grade robustness gate.
