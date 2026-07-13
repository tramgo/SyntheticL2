# SyntheticL2

SyntheticL2 is a research workspace for validating a Zerodha retail top-five market-depth synthetic L2 data strategy plan.

The repository contains:

- the implementation plan in `Plan/`;
- phase runners in `scripts/`;
- reusable phase modules in `src/synthetic_l2/`;
- lightweight generated evidence artifacts in `outputs/`, such as CSV, JSON and Markdown reports.

Large generated data products, DuckDB databases, Parquet files and raw real-data samples are intentionally excluded from git. Recreate them locally with the phase runner scripts when needed.

Current research scope includes:

- real sample schema/data-quality audit;
- received-tick feature reconstruction;
- empirical calibration and regime taxonomy;
- synthetic scenario calendar, price paths and five-level book states;
- retail feed emulation and tiered data products;
- storage sizing and DuckDB query workspace;
- strategy validation matrix, execution proxy, quality gates, acceptance gates and reporting;
- deterministic replay tooling over Phase 9 tiered products.
- horizon-readiness gating for dense-panel versus event-driven 1-second feature use.

No strategy is currently promoted for live use. Existing outputs are engineering/proxy evidence unless a later acceptance gate explicitly marks them as acceptance-grade.

Useful guardrail:

- `python scripts/run_horizon_readiness_gate.py` refreshes the horizon-readiness decisions from Stage A1 coverage evidence.
- `python scripts/run_reproducibility_gate.py` fails if Phase 19 native reproducibility coverage regresses from the current 26/26 exact-ready audited manifests.
