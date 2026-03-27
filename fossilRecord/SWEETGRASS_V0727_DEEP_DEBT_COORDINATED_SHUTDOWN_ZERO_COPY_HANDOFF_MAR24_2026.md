# SweetGrass v0.7.27 — Deep Debt: Coordinated Shutdown, Zero-Copy Phase 3, Type Safety

**Date**: March 24, 2026
**From**: v0.7.26 → v0.7.27
**Status**: All green — 1,128 tests, 90.23% line coverage, 0 clippy warnings, 0 doc warnings, 0 unsafe, 0 fmt issues

---

## Summary

SweetGrass v0.7.27 resolves 11 deep debt items identified by comprehensive
audit: coordinated graceful shutdown replaces fire-and-forget spawns,
BraidMetadata fields complete zero-copy Phase 3 migration, JSON-LD versioning
gets type safety, store batch operations surface errors, and registry RPC
gets structured error types.

---

## Changes

### Coordinated Graceful Shutdown
- **`tokio::sync::watch` channel** coordinates HTTP, tarpc, and UDS server
  shutdown; HTTP shutdown signal triggers tarpc and UDS drain via shared
  `watch::Receiver<bool>`
- **`start_tarpc_server`** and **`start_uds_listener`** accept shutdown
  receivers and use `tokio::select!` to exit cleanly
- Replaces fire-and-forget `tokio::spawn` pattern — servers now drain
  in-flight requests before binary exits

### Zero-Copy Phase 3: BraidMetadata
- `BraidMetadata.title`: `Option<String>` → `Option<Arc<str>>`
- `BraidMetadata.description`: `Option<String>` → `Option<Arc<str>>`
- `BraidMetadata.tags`: `Vec<String>` → `Vec<Arc<str>>`
- Tag index: `HashMap<String, HashSet<BraidId>>` → `HashMap<Arc<str>, HashSet<BraidId>>`
- Cross-crate migration across all 10 crates, 4 store backends, examples,
  integration tests, and JSON-RPC handlers

### Type Safety: JsonLdVersion
- `BraidContext.@version` evolved from `f32` to custom `JsonLdVersion` type
- Always serializes to `1.1`; deserialization validates the value
- Eliminates float precision drift in content-addressed hashing

### Store Error Surfacing
- `BraidStore::get_batch` returns `(Vec<Option<Braid>>, Vec<StoreError>)`
- Matches `put_batch` error pattern; store errors are now visible instead of
  silently swallowed as "not found"

### Structured Registry Errors
- `RegistryRpc` trait: `Result<T, String>` → `Result<T, RegistryError>`
- `RegistryError` enum: `NotFound`, `RegistrationFailed`, `Internal`
- `RegistryDiscovery` adapters map structured errors to `DiscoveryError`

### Discoverable Vocab URIs
- `ecop_vocab_uri()` / `ecop_base_uri()` resolve from `ECOP_VOCAB_URI` /
  `ECOP_BASE_URI` env vars with `DEFAULT_*` fallbacks
- `BraidContext::default()` uses discoverable functions; no hardcoded URIs

### Attribution Notice Evolution
- Removed `notice_text: String` field from `AttributionNotice`
- `Display` impl generates text from structured data — single source of truth
- Eliminates drift risk between stored text and structured fields

### Minor Improvements
- `CachedDiscovery.find_one` sorts by `last_seen` for deterministic selection
- `http_health_check` uses numeric status code parsing (any 2xx)
- Chaos test `println!` → `tracing::info!`
- `RewardShare.share`/`amount` documented as informational ratios

---

## Audited — No Action Needed
- **Tests**: 1,128 passing (unchanged), 0 failures
- **Coverage**: 90.23% line coverage (llvm-cov)
- **Clippy**: 0 warnings (pedantic + nursery, `-D warnings`)
- **Docs**: 0 warnings (`cargo doc --all-features --no-deps`)
- **Format**: 0 diffs (`cargo fmt --all -- --check`)
- **Unsafe**: 0 blocks (`#![forbid(unsafe_code)]` on all crates + binary)
- **TODOs**: 0 `TODO`/`FIXME`/`HACK`/`XXX` in any .rs file
- **Unwraps**: 0 production unwraps (`unwrap_used`/`expect_used` = `deny`)
- **File sizes**: All under 826 lines (max: `store-redb/tests.rs`)
- **Mocks**: All behind `#[cfg(any(test, feature = "test"))]`
- **Archive/debris**: None — clean tree

---

## Deferred to v0.8 (Profile-Driven)
- **StorageResultExt** — needs profiling to justify abstraction
- **Tokio feature slimming** — per-crate feature audit needed
- **Fuzz target for JSON-RPC dispatch** — infrastructure exists (fuzz/ crate)
- **async-trait removal** — blocked on stable `dyn Trait` with async fn

---

## Cross-Ecosystem Signals

| Pattern | Source | Status in sweetGrass |
|---------|--------|---------------------|
| `tokio::sync::watch` shutdown | Ecosystem best practice | ✅ Adopted |
| `Arc<str>` for metadata fields | Zero-copy Phase 3 | ✅ Complete |
| `JsonLdVersion` type safety | Content-addressed precision | ✅ Adopted |
| Structured RPC errors | tarpc best practice | ✅ Adopted |
| Discoverable vocab URIs | Capability-based discovery | ✅ Adopted |
| `Display` single source of truth | loamSpine pattern | ✅ Adopted |
| Deterministic find_one ordering | Stable selection | ✅ Fixed |

---

## Verification

```
cargo fmt:     PASS (0 diffs)
cargo clippy:  PASS (0 warnings, -D warnings)
cargo doc:     PASS (0 warnings)
cargo test:    1,128 passed, 0 failed, 56 ignored
cargo llvm-cov: 90.23% line coverage
cargo build --release: PASS
unsafe blocks: 0
```
