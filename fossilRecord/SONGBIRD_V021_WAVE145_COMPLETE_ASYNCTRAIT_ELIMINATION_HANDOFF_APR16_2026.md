# Songbird v0.2.1 Wave 145+146 — Complete async-trait Elimination + Stadial Parity Gate

**Date**: April 16, 2026
**Commit**: `5099ecd1` (Wave 146), `d237c9c2` (Wave 145)
**Branch**: `main`

## Summary

Complete elimination of the `async-trait` crate from the entire Songbird workspace.
Every `#[async_trait]` annotation (141 total) converted to native async fn in traits (AFIT),
enum dispatch, or concrete types. The `async-trait` dependency is removed from all 30 crates
and the workspace `Cargo.toml`. SB-06 tracking item resolved.

## Wave 145 Conversions

### Platform IPC (songbird-universal-ipc)
- `PlatformIPC`/`PlatformListener` → cfg-gated `PlatformIpcImpl`/`PlatformListenerImpl` enums
- `AsyncStream` → `AsyncStreamImpl` enum replacing `Box<dyn AsyncStream>`

### HTTP/Network Handlers (songbird-universal-ipc)
- `HttpClientCapability`/`HttpClientFactory`/`CryptoCapabilityDiscovery` → concrete enums
- `PeerConnector` → enum (Udp + test variants)
- `RendezvousClient` → enum (Http + test variants)
- `DiscoveryStrategy` → enum (Environment/Filesystem/MappedEnvironment/DnsSrv)
- `EnvReader` (dyn Fn) → `HashMap<String, String>` overrides

### Lineage Relay (songbird-lineage-relay)
- `RelayAuthority` → enum (Security/Mock/StubAllow/StubDeny)
- `BirdSongCrypto` → enum (Security/Mock/StubPassthrough/StubMockEncrypted)

### Discovery (songbird-discovery)
- `BirdSongEncryption` → enum (9 variants)
- `DiscoveryMechanism` → enum

### Remaining Crates
- `CryptoCapability` (http-client) → native AFIT
- `QuicCryptoProvider` (quic) → inherent impl
- `NfcBackend` (nfc) → `NfcBackendImpl` enum
- `HealthCheckAsync` (observability) → native AFIT
- `PrimalBridge`/`PrimalDiscovery` (primal-coordination) → enums
- `CoordinationBridge` (genesis) → enum
- Canonical Provider tree (songbird-types) → all 10 traits native AFIT
- `CapabilityTransport` (songbird-universal) → enum dispatch
- `PeerRegistry` (universal-ipc) → native AFIT

### Additional Cleanup
- Axum route params: 30+ routes migrated from legacy `:param` to `{param}` syntax
- Stale doc comments cleaned

## async-trait Metrics

| Metric | Wave 144 | Wave 145 |
|--------|----------|----------|
| `#[async_trait]` annotations | 113 | **0** |
| Crates depending on `async-trait` | 11 | **0** |
| `async-trait` in workspace Cargo.toml | yes | **no** |

## Verification

- Tests: 7,377 passed, 0 failures
- Clippy: zero warnings (`-D warnings`)
- Cargo deny: clean
- Format: clean
- Files >800L: 0
- Unsafe blocks: 0

## Wave 146 — Stadial Parity Gate (commit `5099ecd1`)

### dyn Audit (376 usages classified)
- **19 finite-implementor dyn eliminated**: AsyncStream → enum (http-client), OnionStorageBackend → enum (sovereign-onion), DiscoveryProvider + ProviderFactory → enums (discovery)
- **Remaining ~350 are stadial-compliant**: dyn Error (~195), dyn Future/Stream (~18), dyn Fn (~3), dyn Any (~10), test code (~165), doc comments (~95), open plugin (2), external (1)

### ring Lockfile Analysis
- `cargo tree -i ring --edges normal` = empty (NOT in dependency graph)
- `cargo deny check bans` = passes (ring banned, not compiled)
- Cargo.lock stanza is a Cargo resolver artifact (optional dep version locking)
- Upstream blocked: `rustls-rustcrypto` git master drops webpki 0.102 but uses incompatible pre-release crypto; no crates.io release
