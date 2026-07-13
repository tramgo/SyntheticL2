# Replay Tool Validation Report

Generated UTC: 2026-07-13T16:15:36.515643+00:00

## Scope

This validates deterministic replay ordering for Phase 9 Tier A, Tier B and Tier C Parquet products.
The replay tool supports tier selection, symbol/date/profile filters, column projection, row limits and ordered Parquet export.

## Validation Summary

| Tier | Sample rows | Deterministic ordering | Order columns | SHA256 |
| --- | ---: | --- | --- | --- |
| tier_a | 5000 | True | trade_date;feed_profile;quarter_profile;symbol;event_ts;source_sequence;event_id | 77d76a3bb116fb4d453653da91b8a9020560ce3f3130edd015d9fcc4b6ad9272 |
| tier_b | 5000 | True | trade_date;feed_profile;quarter_profile;symbol;bar_index;collector_received_utc_ms;receive_sequence;source_sequence | 97cddc8c16b99f135f50c0f85f7fe794a99fce9972db2320a8517fe531e42650 |
| tier_c | 5000 | True | trade_date;feed_profile;quarter_profile;symbol;bar_index;collector_received_utc_ms | afedaebedb7b52f087a3761518eaf5840f0e3a91802120aa022a37e82af35d5b |
