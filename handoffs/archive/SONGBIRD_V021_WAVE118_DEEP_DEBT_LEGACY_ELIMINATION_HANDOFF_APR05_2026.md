# Songbird v0.2.1 — Wave 117-118: Test Infrastructure Hardening + Legacy Elimination + Coverage Expansion

**Date**: April 5, 2026
**Primal**: songBird
**Previous**: Wave 113 (SONGBIRD_V021_WAVE113_TEST_QUALITY_COVERAGE_DOCS_HANDOFF_APR05_2026.md)

---

## Summary

Waves 117-118 hardened the test infrastructure for fully concurrent deterministic execution, eliminated legacy primal name identifiers from production code, expanded adapter test coverage, and converted lint suppressions to `#[expect(reason)]`.

## Wave 117 — Test Infrastructure Hardening

### Sleep Elimination (25+ removed)
- 5-second sleep in `tests_discovery_bridge.rs` → `std::future::pending()` + `tokio::time::advance(3s)`
- 500ms + 100ms sleeps in `capability_registration/tests.rs` → `tokio::spawn` + `advance()`
- 200ms sleep in `circuit_breaker_tests.rs` → `std::future::pending()`
- 2x 50ms sleeps in `service_registry_tests.rs` → `advance(50ms)`
- 9 sleeps in `connection_pool_tests.rs` → all converted to `advance()` under `start_paused`
- 1ms yield sleeps → `tokio::task::yield_now().await`
- 20ms sleep in `crypto_tests.rs` → `advance(20ms)`

### Production Code Evolution
- `ConnectionPool` migrated from `std::time::Instant` → `tokio::time::Instant` for deterministic testing

### Hardcoded Port Elimination
- TLS e2e tests: ports 18443-18446 → `TcpListener::bind("127.0.0.1:0")` + oneshot readiness
- All startup sleep waits removed (replaced by readiness channels)

## Wave 118 — Legacy Primal Name Elimination

### Identifier Removal (50+ functions, types, modules)

| Crate | Items Removed |
|-------|--------------|
| `songbird-sovereign-onion` | 19 `*_via_beardog` functions → `*_via_security_provider`; `BeardogCryptoClient` type; `beardog_crypto` module |
| `songbird-crypto-provider` | `BEARDOG_MODE`/`BEARDOG_SOCKET` kept as deprecated env fallbacks only |
| `songbird-tls` | `BeardogCryptoClient` → `LegacySecurityTlsCryptoClient`; `CertGenerationMode::BearDog` → `LegacySecurityProvider` |
| `songbird-execution-agent` | `BearDogSecurityValidator` → `LegacySecurityProviderValidator`; `security_beardog` → `security_provider_legacy` |
| `songbird-nfc` | `beardog_socket()` removed |
| `songbird-config` | Deprecated accessor methods removed (0 callers); `PrimalConfig` deprecated fields removed; deprecated standalone functions removed |
| `songbird-types` | `primal_names::{BEARDOG,SQUIRREL,TOADSTOOL,NESTGATE}` removed; `LineageError::BearDogError` removed; deprecated socket candidate functions removed |
| `songbird-quic` | `BeardogQuicCrypto` type alias removed |
| `songbird-http-client` | `beardog_client` module, `BearDogProvider`, `BearDogClient`, `BearDogMode`, `BearDogRpc`, `discover_beardog_socket` removed |
| `songbird-network-federation` | `has_beardog()`, `requires_beardog()` removed |
| `songbird-orchestrator` | `TokenType::BearDog` removed; `BearDogClient` trust alias removed |
| `songbird-universal` | `pub mod toadstool` removed; `ToadStoolMetricsAdapter` removed |

### Lint Hardening
- ~1,092 `#[allow(` → `#[expect(` in production code
- ~352 stable `#[expect(reason)]` in production
- Reverted where cfg/test interaction causes unfulfilled-expectation errors

### Coverage Expansion
- 42 new adapter tests (10 compute, 21 security, 11 AI) using `MockTransport`
- `songbird-universal` lib tests: 738 → 780

### async-trait Audit
- All 99 remaining `#[async_trait]` confirmed to require `dyn Trait` dispatch — no migration possible

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Tests | 12,665 | 12,693 |
| Legacy primal identifiers | ~342 | ~12 (env var strings only) |
| `#[expect(reason)]` in production | ~25 | ~352 |
| Test sleeps eliminated | — | 25+ |
| Hardcoded port binds | 4 (18443-18446) | 0 |

## Verification

- `cargo fmt --check` — clean
- `cargo clippy --workspace --all-targets -- -D warnings` — clean
- `cargo doc --workspace --no-deps` — clean
- `cargo test --workspace` — 12,693 passed, 0 failed, 252 ignored
- `cargo deny check` — clean

## Remaining Work

See `REMAINING_WORK.md` for full status. Key items:
- Coverage: ~77% → 90% target
- Security provider crypto e2e validation (blocked on live provider)
- Platform backends (Android, iOS, WASM)
- Real hardware IGD tests
