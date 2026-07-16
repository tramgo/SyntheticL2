# Phase 19 Reproducibility Gate Result

Generated UTC: 2026-07-16T13:47:13.215272+00:00
Passed: True
Audited artifacts: 57
Field checks: 570

| gate | passed | observed | expected | detail |
| --- | --- | --- | --- | --- |
| all_audited_artifacts_native_exact_ready | True | 57/57 | 57/57 | Artifacts not exact-ready: none |
| no_missing_source_manifest_fields | True | 0 | 0 | Artifacts with missing fields: none |
| no_missing_or_unreadable_manifests | True | 0 | 0 | Artifacts with missing/unreadable manifests: none |
| all_normalized_overlays_ready | True | 57/57 | 57/57 | Overlay artifacts not ready: none |
| no_normalizer_default_fields | True | 0 | 0 | All normalized overlay values should be sourced from exact or alias fields in source manifests. |
| remediation_is_complete_exact_only | True | {'complete_exact': 570} | {'complete_exact': 570} | Remediation rows should not require add-field, alias-normalization or manifest recovery actions. |
