# DuckDB Workspace Report

Generated UTC: 2026-07-13T19:17:11.148181+00:00

## Storage Decision

Use Parquet as durable storage and DuckDB as the local analytic query engine over registered views.
Use SQLite only later if we need a small transactional run registry or manual annotation database.

## Validation

- Stage A1 symbols: 32
- Stage A1 rows: 620853
- Compact tick rows: 620853
- Normalized tick rows: 620853
- Received delta rows: 620853
- Phase 2 symbols: 32
- Phase 3 intraday bins: 77
- Phase 4 calendar rows: 189
- Phase 4 profiles: 3
- Phase 5 price bar rows: 453600
- Phase 5 daily rows: 6048
- Phase 5 symbols: 32
- Phase 6 L2 book rows: 453600
- Phase 6 symbols: 32
- Phase 6 crossed L1 rows: 0
- Phase 7 shock events: 1504
- Phase 7 market events: 200
- Phase 7 ticker events: 1304
- Phase 7 target symbols: 32
- Phase 8 feed observation rows: 2259039
- Phase 8 feed profiles: 5
- Phase 8 dropped rows: 15600
- Phase 8 duplicate rows: 6639
- Phase 9 Tier A events: 2276143
- Phase 9 Tier B rows: 2259039
- Phase 9 Tier C rows: 2259039
- Phase 9 Tier B crossed L1 rows: 0
- Phase 10 measured storage layers: 5
- Phase 10 generation profiles: 5
- Phase 10 feature intervals: 5
- Phase 10 Medium estimated total GB: 2.8227162677794695
- Phase 10 Full estimated total GB: 11.290865073911846
- Phase 10 consolidated inventory datasets: 7
- Phase 10 consolidated schema columns: 309
- Phase 10 partition recommendation rows: 7
- Phase 10 consolidated Medium estimated total GB: 25.06
- Phase 10 consolidated Full estimated total GB: 100.25
- Phase 10 type optimization candidates: 207
- Phase 11 strategies: 11
- Phase 11 baselines: 7
- Phase 11 runnable proxy strategies: 5
- Phase 11 partial/missing-feature strategies: 4
- Phase 11 unsupported-by-current-product strategies: 2
- Phase 11 rows evaluated per strategy: 2259039
- Phase 12 execution summary rows: 27
- Phase 12 execution profiles: 3
- Phase 12 strategies simulated: 9
- Phase 12 total simulated trades: 10350654
- Phase 12 trade sample rows: 249993
- Phase 12 cost components: 6
- Phase 12 lifecycle rows: 749979
- Phase 12 fill models: 3
- Phase 12 partial-fill summary rows: 81
- Phase 12 risk-control summary rows: 81
- Phase 12 position-limit breach rows: 233010
- Phase 12 daily-loss-limit breach rows: 23317
- Phase 13 split rows: 189
- Phase 13 seed rows: 30
- Phase 13 initial engineering seeds: 9
- Phase 13 walk-forward windows: 48
- Phase 13 parameter sets: 63
- Phase 13 negative controls: 9
- Phase 13 planned experiment registry rows: 324
- Phase 13 proxy smoke run rows: 324
- Phase 13 proxy smoke strategies: 9
- Phase 13 proxy smoke controls: 4
- Phase 13 proxy smoke summary rows: 9
- Phase 13 acceptance-eligible smoke rows: 0
- Phase 14 quality checks: 24
- Phase 14 pass checks: 23
- Phase 14 warn checks: 1
- Phase 14 fail checks: 0
- Phase 15 gate rows: 55
- Phase 15 promoted strategies: 0
- Phase 15 blocked strategies: 11
- Phase 15 blocker rows: 55
- Phase 16 metric catalog rows: 27
- Phase 16 predictive scoreboard rows: 11
- Phase 16 predictive proxy rows: 9
- Phase 16 predictive signal bucket rows: 27
- Phase 16 missing predictive metrics: 3
- Phase 16 missing trading metrics: 0
- Phase 16 trading scoreboard rows: 27
- Phase 16 markout/MAE/MFE summary rows: 27
- Phase 16 markout sample trades: 243958
- Phase 16 adverse-selection metric status: sample_proxy
- Phase 16 MAE/MFE metric status: sample_proxy
- Phase 16 breakdown rows: 12
- Phase 16 acceptance-grade metrics: 0
- Phase 16 non-acceptance-grade metrics: 27
- Phase 17 work packages: 10
- Phase 17 deliverables: 55
- Phase 17 implemented deliverables: 23
- Phase 17 proxy/partial deliverables: 32
- Phase 17 missing deliverables: 0
- Phase 17 blocked work packages: 0
- Phase 17 P0 gaps: 0
- Replay validation tiers: 3
- Replay deterministic tiers: 3
- Phase 18 stack decision rows: 21
- Phase 18 dependency rows: 15
- Phase 18 required-now dependencies: 5
- Phase 18 missing required-now dependencies: 0
- Phase 18 deferred/optional stack items: 11
- Phase 19 required fields: 10
- Phase 19 audited artifacts: 21
- Phase 19 field checks: 210
- Phase 19 exact-regeneration-ready artifacts: 0
- Phase 19 artifacts with missing fields: 20
- Phase 19 manifest-missing/unreadable artifacts: 1
- Phase 19 gap rows: 20
- Dense full-session 1s below 90% symbols: 32
- Dense full-session 5s supported symbols: 30
- Open 09:15-09:20 dense 1s supported symbols: 0
- Open 09:15-09:20 event-driven 1s supported symbols: 12

## Phase 4 Days Per Profile

| Profile | Days |
| --- | --- |
| Q-A | 63 |
| Q-B | 63 |
| Q-C | 63 |
