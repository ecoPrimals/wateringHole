# Songbird v0.2.1 Wave 144 — dyn→Static Dispatch Evolution

**Date**: April 16, 2026
**Commit**: `cd1f410e`
**Branch**: `main`

## Summary

Systematic elimination of dynamic dispatch (`dyn Trait`) in favor of enum/concrete
dispatch across 5 trait hierarchies. This enables native async fn in traits (AFIT)
and removes `#[async_trait]` heap allocation overhead for converted code paths.

## Converted Trait Hierarchies

### 1. PeerConnection (songbird-orchestrator)
- **Before**: `#[async_trait] trait PeerConnection` + 6 `impl PeerConnection for X` + `&dyn PeerConnection`
- **After**: `Connection` enum with match dispatch macro, inherent methods on concrete types
- **Annotations removed**: 7

### 2. BtspProvider (songbird-network-federation)
- **Before**: `Arc<dyn BtspProvider>` with 2 impls (Local, Http)
- **After**: `BtspProviderImpl` enum, factory returns concrete type
- **Annotations removed**: 3

### 3. Federation SecurityProvider + Supertraits (songbird-network-federation)
- **Before**: `Box<dyn SecurityProvider>` requiring `LineageProvider + BirdSongCrypto + LineageRelay`
- **After**: `SecurityProviderImpl` enum (Production/NoOp/Mock), all 4 traits use native AFIT
- **Annotations removed**: ~10
- **Note**: `async-trait` dropped from crate entirely

### 4. ConsentStorageBackend (songbird-orchestrator)
- **Before**: `Arc<dyn ConsentStorageBackend>` with 2 impls
- **After**: `ConsentStorage` enum (Memory/Ipc)

### 5. TaskStorageBackend (songbird-orchestrator)
- **Before**: `Arc<dyn TaskStorageBackend>` with 2 impls
- **After**: `TaskStorage` enum (Memory/Ipc)

## async-trait Reduction

| Metric | Before | After |
|--------|--------|-------|
| `#[async_trait]` annotations | 141 | 113 |
| Crates depending on `async-trait` | 17 | 11 |
| Crates dropped | — | canonical, config, execution-agent, network-federation, registry, stun |

## Deep Debt Cleanup

- **discovery_handler.rs** (1030L) smart-refactored into 4-file module: handler (291L), content distribution (82L), types (44L), tests (530L)
- **`/tmp/service.log`** in ssh.rs → `{remote_path}.log`
- **`localhost:8080`** in process_manager.rs → `LOCALHOST`:`DEFAULT_HTTP_PORT`

## Remaining dyn Dispatch (113 annotations)

Highest-impact targets for future waves:
- **Platform IPC** (6 OS backends): `PlatformIPC`, `PlatformListener` — runtime multi-backend
- **Canonical Provider tree** (songbird-types): Plugin/registry API surface
- **Lineage-relay**: `RelayAuthority`, `BirdSongCrypto` (relay version)
- **Discovery**: `DiscoveryProvider`, `ProviderFactory`, streams
- **HTTP handlers**: `HttpClientFactory`, `HttpClientCapability`, `CryptoCapabilityDiscovery`
- **Crypto capability**: `CryptoCapability` (TLS crypto backends)

## Verification

- Tests: 7,360 passed, 0 failures
- Clippy: zero warnings (`-D warnings`)
- Cargo deny: clean (advisories ok, bans ok, licenses ok, sources ok)
- Format: clean
- Files >800L: 0
