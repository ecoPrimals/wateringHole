# NestGate v4.7.0-dev — Session 34c Handoff: Doc Ground Truth & Debris

**Date**: April 7, 2026
**Commit**: `9ef5da8f`
**Branch**: `main`

---

## Summary

Comprehensive documentation ground truth alignment, debris cleanup, and capability mappings update across 15 files.

## Documentation Fixes

### Dates
- All root docs aligned to April 7, 2026 (10 files)

### Test Counts
- `tests/DISABLED_TESTS_REFERENCE.md`: ~11,826 → ~11,834
- `docs/guides/TESTING.md`: ~11,826 → ~11,834

### Accuracy Corrections
- **Serial test count**: "5 total — 4 in env-process-shim" → "1 — CLI argument tests in nestgate-bin"
- **`#[allow(` claim**: Narrowed to `#[allow(clippy::…)]` (accurate for production code)
- **tests/README.md**: EnvSource/MapEnv now primary env isolation guidance (temp_env legacy-only)
- **DOCUMENTATION_INDEX.md**: All dates updated from April 5

### Capability Mappings
- Added `storage.fetch_external` to methods list (10 total methods)
- Updated TLS ownership: NestGate owns external HTTPS fetch boundary (not Songbird)
- Capability matrix: storage row 9 → 10 methods

## Debris Cleaned

| Item | Fix |
|------|-----|
| `hardcode_elimination_test.rs` | Removed stale `nestgate-network` path reference |
| `.env.test` | `NESTGATE_ZFS_POOL=nestpool` → `nestgate` (matches setup script) |
| `multi_service_workflow_integration.rs` | `nestgate-network` → `nestgate-rpc` |
| `CHANGELOG.md` | Fixed stale `todo_implementation_tests.rs` reference |

## Metrics

| Metric | Value |
|--------|-------|
| Tests passing | 11,834 |
| Tests ignored | 461 |
| Tests failed | 0 |
| Clippy warnings | 0 |
| Files changed | 15 |

## Remaining Known Doc Debt (fossil record)

| Item | Notes |
|------|-------|
| `docs/architecture/ARCHITECTURE_OVERVIEW.md` | Historical Nov 2025 — Version 0.11.0, legacy examples |
| `docs/guides/TESTING.md` body | Historical baseline — banner updated, body still Nov 2025 |
| Root `benches/*.rs` | 10 unwired files with status documentation |
| 3 disabled fuzz targets | Non-trivial, need import fixes |
