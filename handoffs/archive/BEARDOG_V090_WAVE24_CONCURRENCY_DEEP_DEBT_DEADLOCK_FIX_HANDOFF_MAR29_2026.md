# BearDog v0.9.0 Wave 24: Concurrency Deep Debt — ABBA Deadlock Fix & Sleep Elimination

**Date**: March 29, 2026
**Primal**: beardog
**Version**: 0.9.0
**Wave**: 24

---

## Summary

Resolved intermittent ~30% test hang rate caused by an ABBA deadlock in e2e test infrastructure. Eliminated all non-chaos test sleeps. Evolved `HybridIntelligenceSystem::initialize()` from sync `blocking_write()` to async. Cleaned 49.6 KB of dead android_strongbox files and audit.log debris.

## Root Cause: ABBA Deadlock

Three global `OnceLock<Mutex<HashMap>>` statics in `tests/e2e/hsm_operations.rs` (`HSM_INIT_STATUS`, `HSM_HEALTH_MAP`, `HSM_OPERATION_COUNTS`) were shared across all parallel tests. Two functions acquired locks in opposite order:

- `initialize_hsm()`: locked `init_map` then `health_map` (A→B)
- `check_hsm_health()`: locked `health_map` then `init_map` (B→A)

When two tests ran concurrently, each holding one lock and waiting for the other — classic deadlock. This caused the `e2e_real_scenarios` binary to hang approximately 3/10 runs.

## Changes

### Concurrency Fixes
- **`tests/e2e/hsm_operations.rs`** — 3 global `OnceLock<Mutex<HashMap>>` → per-test `HsmTestContext` struct
- **`tests/e2e/rate_limiting.rs`** — 3 global `OnceLock<AtomicUsize>` → `thread_local! Cell`
- **`tests/e2e/disaster_recovery/*.rs`** — 4 files: `OnceLock<Mutex>` → per-invocation context structs

### Production Code Evolution
- **`HybridIntelligenceSystem::initialize()`** — `fn initialize(&self)` → `async fn initialize(&self)` with `.write().await`
- **`GeneticCryptoProvider::verify()`** — Restored correct API: accepts public key bytes (was incorrectly expecting private seed)
- **`generate_proof()`** — Nanosecond timestamp + UUID instead of second-resolution (eliminates uniqueness sleep)

### Sleep Elimination (non-chaos tests)
| File | Before | After |
|------|--------|-------|
| `proof_verifier.rs` | 1000ms | 0ms (UUID) |
| `security_integration_tests.rs` | 1100ms | 0ms (zero interval) |
| `btsp_provider/types.rs` | 100ms | 0ms |
| `core_edge_cases_oct22.rs` | 56ms | 0ms (configurable cooldown) |
| `request_cache.rs` (4 tests) | 2-40ms | 0ms (past timestamps) |
| Plus ~6 more files | various | 0ms or 1ms minimum |

### Dead Code & Debris Cleanup
- Deleted 8 orphan files from `android_strongbox/` (49.6 KB total)
- Removed `audit.log` artifacts from repo root and 2 crate directories
- Updated method count assertion from 92 → 93

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| **Passed** | 15,161 | **15,184** |
| **Failed** | 2 | **0** |
| **Ignored** | 139 | **138** |
| **Hang rate** | ~30% | **0%** |
| **RUST_TEST_THREADS=1** | Required | **Not needed** |
| **Test sleeps eliminated** | — | **~2.4s total** |
| **Dead code removed** | — | **49.6 KB** |

## Remaining Ignored Tests (138)

- **6 hardware**: FIDO2/HSM/Android (require physical devices)
- **2 TTY**: entropy collection (require interactive terminal)
- **1 UPA**: requires live endpoint
- **~129 doc tests**: `rust,ignore` (incomplete examples, deprecated APIs)

## Known Debt (unchanged)

- Vault/USM secrets backends not implemented (blocking — Phase 2)
- RSA Marvin advisory suppressed in deny.toml (risk acceptance)
- Workspace layout has two `BearDogCore` types (system.rs vs beardog_core.rs)
- `println`-to-tracing migration in non-CLI code (ongoing)
- AI/hybrid intelligence placeholders (stubs, not production)
- MSRV 1.93.0 (aggressive but stable)
- KEY_STORE global singleton (production pattern, not test debt)
