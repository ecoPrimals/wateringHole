# BearDog v0.9.0 — Wave 53: Stadial Parity Gate

**Date**: April 16, 2026
**From**: BearDog primal team
**License**: AGPL-3.0-or-later

---

## Summary

BearDog clears the stadial parity gate. All `#[async_trait]` attributes eliminated,
`async-trait` removed from every Cargo.toml, all finite-implementor `dyn Trait`
dispatch replaced with enum dispatch. Zero `ring`/`sled`/`openssl` in Cargo.lock.

## Stadial Gate Status

| Criterion | Status |
|-----------|--------|
| `async-trait` in any `Cargo.toml` | **ZERO** (removed from 17 manifests) |
| `#[async_trait]` in `.rs` files | **ZERO** (was ~49, migrated to native async) |
| `Box<dyn Trait>` / `Arc<dyn Trait>` for finite-implementor traits | **ZERO** (18 enum dispatch types created) |
| `ring` in `Cargo.lock` | **ZERO** |
| `sled` in `Cargo.lock` | **ZERO** |
| `openssl` in `Cargo.lock` | **ZERO** |
| Edition 2024 | **Yes** |
| `cargo clippy -- -D warnings` | **Pass** |
| `cargo doc` with `-D warnings` | **Pass** |
| `cargo fmt --check` | **Pass** |

## Enum Dispatch Types Created

| Enum | Trait | Variants |
|------|-------|----------|
| `MethodHandlerKind` | `MethodHandler` | 13 RPC handlers |
| `HsmKeyProviderBackend` | `HsmKeyProvider` | Software, AndroidStrongBox + test stubs |
| `HsmProviderBackend` | `HsmProvider` | RustSoftware + test mocks |
| `CryptoProviderBackend` | `CryptoProvider` | RustCrypto, Genetic, Dispatch |
| `UniversalCryptoBackend` | `UniversalCryptoProvider` | RustCrypto |
| `KeyManagementBackend` | `KeyManagementCapability` | SoftwareHsm, SecureSoftware |
| `ServiceDiscoveryBackend` | `ServiceDiscoveryCapability` | DnsHttp, Kubernetes |
| `BondPersistenceBackend` | `BondPersistence` | InMemory, CapabilityDiscovery |
| `IpcHandlerBackend` | `IpcHandler` | Default + test variants |
| `PlatformListenerBackend` | `PlatformListener` | Unix, Android |
| `StorageBackend` | `StorageBackendTrait` | File, InMemory, Memory |
| `EncryptionKeyBackend` | `EncryptionKeyTrait` | Default |
| `AuditLoggerBackend` | `AuditLogger` | Default |
| `KeystoreTransportBackend` | `KeystoreTransport` | Stub |
| `AttestationTransportBackend` | `AttestationTransport` | Stub |
| `HealthMetricsTransportBackend` | `HealthMetricsTransport` | Stub, AndroidJni |
| `Ctap2TransportBackend` | `Ctap2Transport` | Hid + test mock |
| `HidDeviceBackend` | `HidDevice` | Linux |

## Lockfile Note

`async-trait` remains in `Cargo.lock` as a **transitive** dependency via
`hickory-proto 0.24.4` (DNS resolver). Upgrading to `hickory-resolver 0.26` would
remove `async-trait` but introduces `ring 0.17` as a transitive dep, which is worse.
BearDog has zero direct or workspace `async-trait` dependency.

## Quality Gates

| Metric | Value |
|--------|-------|
| Tests | 14,786+ passed, 0 failures |
| Clippy | Clean (`-D warnings`) |
| Rustdoc | Clean (`-D warnings`) |
| Format | Clean (`cargo fmt --check`) |
| Coverage | 90.51% (llvm-cov) |

## Previous Wave

Wave 52 (archived): syn elimination, smart file refactoring, async-trait reduction
from ~115 to ~49.

---

**License**: AGPL-3.0-or-later
