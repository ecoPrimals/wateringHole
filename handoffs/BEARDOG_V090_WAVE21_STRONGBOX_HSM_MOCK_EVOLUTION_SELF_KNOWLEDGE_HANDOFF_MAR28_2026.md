# BearDog v0.9.0 — Wave 21: StrongBox HSM Abstraction, Production Mock Evolution, Self-Knowledge & Debt Elimination

**Date**: March 28, 2026
**Primal**: BearDog
**Version**: 0.9.0
**Coverage**: 90.05% line | 89.22% region | 84.84% function
**Tests**: 15,100+ passing, 0 failures

---

## Context

primalSpring is deploying on a Pixel with StrongBox hardware HSM for encryption. BearDog needed a unified HSM abstraction that supports both hardware (Android StrongBox) and software (RustCrypto) backends while remaining ecoBin-compliant (zero C dependencies on non-Android targets). This wave also continued the broader deep debt resolution: evolving production mocks to real implementations, eliminating hardcoded primal names in favor of self-knowledge, cleaning dead code, and pushing coverage past the 90% target.

---

## What Changed

### StrongBox HSM Abstraction (Canonical `HsmKeyProvider`)

**New canonical trait** (`beardog-traits::hsm::HsmKeyProvider`):
- Object-safe, `#[async_trait]`, `Send + Sync`
- Methods: `provider_id`, `provider_type`, `is_available`, `capabilities`, `generate_key`, `delete_key`, `key_exists`, `encrypt`, `decrypt`, `sign`, `verify`
- `provider_id` returns `&'static str` (clippy `unnecessary_literal_bound` resolution)

**Supporting types** (`beardog-types::hsm::provider_types`):
- `HsmProviderType`: `Software`, `AndroidStrongBox`, `IosSecureEnclave`, `Pkcs11`, `Tpm`
- `HsmAlgorithm`: 9 algorithms (AES-256-GCM, ChaCha20-Poly1305, Ed25519, ECDSA-P256/P384, X25519, HMAC-SHA256, RSA-2048/4096)
- `SelectionPreference`: `PreferHardware` (default), `RequireHardware`, `SoftwareOnly`
- `KeyGenParams`, `KeyHandle`, `HsmCapabilitySet`

**Software provider**: `RustSoftwareHsm` implements `HsmKeyProvider`, maps internal `KeyType` to canonical `HsmAlgorithm`.

**Android StrongBox provider**: `AndroidStrongBoxHsm` implements `HsmKeyProvider`. `keystore.rs` rewritten with:
- `#[cfg(target_os = "android")]` JNI bridge (key generation stubbed pending parameter builder wiring)
- `#[cfg(not(target_os = "android"))]` stubs returning `not_implemented` (expected behavior on dev machines)

**Provider registry** (`HsmProviderRegistry`):
- `discover()`: Probes available providers (always software, Android StrongBox on Android targets)
- `select(preference)`: Returns best `Arc<dyn HsmKeyProvider>` matching preference
- `software_fallback()`: Guaranteed software provider
- Wired into `HsmManager` via `canonical_registry` field

**5 legacy traits deprecated** (doc-comment migration notices, not `#[deprecated]` attributes — avoids breaking `-D warnings`):
- `beardog_types::hsm::CryptoProvider`
- `HsmProviderTrait` / `HsmCapabilities` (zero_cost_provider.rs)
- `beardog_traits::unified::providers::HsmProvider`
- `beardog_traits::canonical::hsm::HsmProvider`
- `beardog_tunnel::hsm::manager::implementation::HsmProvider`

### Production Mock Evolution

- **Adapter timing**: `duration_ms` in universal adapter responses uses real `std::time::Instant` (was hardcoded)
- **Canonical validation**: `validate_canonical_usage()` validates semver format (was empty Ok)
- **Ecosystem spawner**: `UniversalHsmManager` tracks real uptime (`Instant`), provider count (`AtomicUsize`), returns live status JSON

### Self-Knowledge / Zero Hardcoding

- `SongbirdClient` → `OrchestratorRegistryClient` (alias for backward compat)
- `BiomeOSPaths` → `PlatformPaths` (alias for backward compat)
- "BiomeOS"/"Songbird"/"NestGate" string literals genericized in production log/error paths
- 3 new `DEFAULT_*` constants (`DEFAULT_SOCKET_PATH`, `DEFAULT_IPC_PORT_FILE`, `DEFAULT_KEY_STORAGE_DIR`) replace inline `/tmp/beardog*` paths
- Dead orphan files deleted: `songbird_client.rs`, `discovery_adapter.rs` (never in mod tree)

### Documentation & Infrastructure

- All root docs updated to current metrics (15,100+ tests, 90.05% coverage)
- specs/README.md: Fixed broken PRODUCTION_READINESS link
- specs/PROJECT_STATUS.md: Pointer updated
- beardog-ipc README: Updated to reference `OrchestratorRegistryClient`
- CI security job pinned to 1.93.0 (was `@stable`)
- Stale infrastructure archived to fossilRecord: k8s/, production-deployment/, docker/Dockerfile.production

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --all -- --check` | Clean |
| `cargo clippy --workspace --all-targets -- -D warnings` | 0 errors |
| `cargo test --workspace` | 15,100+ passing, 0 failures |
| `cargo llvm-cov --workspace` | 90.05% line |
| `cargo doc --workspace --no-deps` | Clean |
| TODO/FIXME in .rs | 0 |
| Files > 1000 LOC | 0 |

---

## Remaining Phase 2 / Future Work

- **Android StrongBox JNI**: Key generation parameter builder wiring (stubbed with `not_implemented`)
- **iOS Secure Enclave**: Provider implementation via Security.framework FFI
- **PKCS#11 / TPM**: Provider implementations for external HSMs
- **Legacy trait removal**: Remove 5 deprecated traits in v0.10.0
- **FIDO2/CTAP2**: Complete Phase 2 attestation and assertion flows
- **Genesis CLI**: Human-witnessed node genesis command
- **Trust visualization**: Expose trust levels in `key info` output

---

## Cross-Primal Notes

- **primalSpring**: Pixel StrongBox deployment validated in exp075/exp076. BearDog's `HsmProviderRegistry` with `PreferHardware` will automatically select StrongBox on Android when the JNI bridge is complete.
- **Other primals**: No API changes. JSON-RPC methods unchanged. The HSM abstraction is internal to BearDog's crypto implementation.
- **ecoBin compliance**: Maintained. Android JNI bridge is `cfg`-gated; non-Android builds remain pure Rust with zero C dependencies.
