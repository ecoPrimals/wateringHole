# Songbird v0.2.1 — Wave 127: Coverage Expansion — MockTransport Adapters

**Date**: April 8, 2026  
**Primal**: Songbird  
**Wave**: 127  
**Status**: Complete  
**Commit**: `0a23d8a8`

---

## Summary

Comprehensive MockTransport-based test coverage for all high-priority low-coverage modules. All 8 modules from the coverage priority table now have dedicated unit tests using the `MockTransport`/`DelayTransport` pattern.

## Changes

### AI Adapter (+6 tests, Wave 127)
- `collect_metrics` via MockTransport with valid JSON response
- `collect_metrics` via DelayTransport with short timeout → error string
- `collect_metrics` via MockTransport returning HTTP error → passthrough
- `check_health` delegation to `collect_metrics`
- `AIProvider` trait methods with MockTransport
- `SQUIRREL_ENDPOINT` legacy env var deprecation warning capture via tracing

### Storage Adapter (+10 tests, Wave 127)
- `StorageAdapter::new()` with tarpc, unix, HTTP, HTTPS URLs
- `build_default_transport()` error paths (invalid tarpc, empty unix path)
- Discovery env fallback chain: `SONGBIRD_STORAGE_ENDPOINT` → `STORAGE_PROVIDER_ENDPOINT` → `STORAGE_ENDPOINT` → `NESTGATE_ENDPOINT`
- Custom `SONGBIRD_HOST` + `SONGBIRD_STORAGE_PORT` resolution
- `collect_metrics` via MockTransport, DelayTransport timeout, error passthrough

### tarpc_client/ops (+5 tests, Wave 127)
- `discover("")` with empty capability string
- `unregister("")` with empty service ID
- Sequential operations on single client (discover → health → version → protocols)
- `ProtocolInfo` serde round-trip with empty info field
- `HealthStatus` serde round-trip with zero values

### Security Adapter (+9 tests, Wave 126)
- Discovery fallback chain with mock IPC
- `BEARDOG_ENDPOINT` deprecation warning capture
- `collect_metrics` / `check_health` via MockTransport

### tower_atomic (+6 tests, Wave 126)
- Malformed JSON wire handling
- Concurrent client round-trips
- Oversized NDJSON requests

### Test Infrastructure
- `discovery_test_sync.rs`: Global mutex for parallel discovery tests across all adapters
- Prevents flaky env var clobbering between concurrent test threads

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 12,916 passed, 0 failed, 252 ignored |
| New tests | +30 (Waves 126-127) |
| Clippy | Clean (pedantic + nursery, `-D warnings`) |
| Format | Clean |
| Files >800L | 0 |

## Next Steps

- Re-measure coverage with `cargo llvm-cov --workspace --lib` to quantify gains
- Orchestrator aggregate coverage (~56%) — consent/task lifecycle paths
- Config aggregate coverage (~68%) — validation edge cases
