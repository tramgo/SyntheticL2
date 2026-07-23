# Phase131 Evaluation Rules

These rules are immutable for Phases 132-136 of the deep-book passive branch.

1. A feature or strategy clears only if it clears both cost regimes: `base` and `harsh`.
2. No cost-stress ordering reversal is allowed. A candidate that ranks above the Phase130 L1/context baselines under `base` but falls below them under `harsh` is rejected as brittle.
3. Positive-pockets exception is disallowed. Full-sample verdict under `harsh` decides the outcome.
4. `strategy_replay_allowed` remains `0` throughout this plan unless separate real-anchor gates outside this plan unlock replay.
5. Phase131 and Phase132 may emit feature diagnostics only. They may not emit strategy code, buy/sell signals, order-arrival streams, live-tagged fill models, P&L replay, or profitability claims.

Baseline comparison margin for Phase132: Brier improvement must be greater than `0.005` versus the matching Phase130 selected diagnostic baseline.
Pinned cost model: `zerodha_equity_intraday_nse_order_formula_v2_2026_07_14`.
Allowed dataset: `outputs/phase129/allowed_context_label_matrix.csv`.
