# Phase 18 Technology Stack Report

Generated UTC: 2026-07-13T20:47:21.734631+00:00

## Scope

This phase records the working technology-stack decision and checks local availability of required/optional dependencies.
The current direction remains single-machine Python, Parquet/Zstandard and DuckDB. Distributed tools are deferred until measured local limits require them.

## Decision Summary

| decision_status | items |
| --- | --- |
| adopted | 4 |
| adopted_now | 3 |
| defer | 3 |
| optional_later | 8 |
| partial_current | 2 |
| recommended_next | 1 |

## Dependency Availability Summary

| requirement_status | available_now | dependencies |
| --- | --- | --- |
| optional_later | False | 6 |
| optional_later | True | 2 |
| recommended_next | False | 1 |
| recommended_next | True | 1 |
| required_now | True | 5 |

## Missing Required Dependencies

_No rows._

## Stack Decisions

| component | selected_option | decision_status | rationale |
| --- | --- | --- | --- |
| Language | Python | adopted | Current pipeline is Python scripts/modules. |
| DataFrame engine | Pandas | adopted_now | Used for summaries and moderate-size CSV/Parquet operations. |
| DataFrame engine | PyArrow | adopted_now | Used for Parquet IO and schema handling. |
| DataFrame engine | Polars | optional_later | Useful for larger scans; not required by current pipeline. |
| Storage | Parquet + Zstandard | adopted | Durable data products are Parquet with compression. |
| Query | DuckDB | adopted | Local analytical layer over Parquet/CSV outputs. |
| Numerical work | NumPy | adopted | Used by generation and simulation phases. |
| Numerical work | SciPy | optional_later | Useful for richer distribution fitting; not required by current scripts. |
| Statistical models | statsmodels | optional_later | Needed only for formal statistical modeling phases. |
| Statistical models | scikit-learn | optional_later | Needed for discriminator/model validation beyond current proxies. |
| Tree models | LightGBM/XGBoost | defer | Do not add until acceptance experiments require tree models. |
| Configuration | JSON/YAML + Pydantic optional | partial_current | Current outputs use JSON manifests; schema validation can be added later. |
| Experiment tracking | Structured local metadata | adopted_now | Current manifests and registries are local structured metadata. |
| Experiment tracking | MLflow | defer | Avoid until experiment volume requires a tracking server or richer UI. |
| Parallel generation | multiprocessing | optional_later | Use only after single-machine bottlenecks are measured. |
| Parallel generation | Ray/Dask | defer | Avoid distributed infrastructure before local limits are measured. |
| Testing | pytest | recommended_next | Add formal tests around phase invariants and generators. |
| Testing | hypothesis | optional_later | Property-based tests are useful for book/price invariants. |
| Visualization | Matplotlib | optional_later | Useful for static reports. |
| Visualization | Plotly | optional_later | Useful for interactive dashboard once Phase 17 WP10 dashboard starts. |
| Versioning | Git + data manifests + generator hashes | partial_current | Data manifests exist; this folder is not currently a Git repo. |
