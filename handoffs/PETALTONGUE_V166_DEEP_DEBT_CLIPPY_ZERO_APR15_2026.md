# petalTongue v1.6.6 — Deep Debt: Clippy Zero, Typed Errors, Modern Rust

**Date**: April 15, 2026
**Commit**: `fb23e49` on `main`
**Author**: westgate

---

## Summary

Comprehensive deep debt pass across the petalTongue workspace. All 35 clippy
warnings eliminated; `Box<dyn Error>` returns evolved to typed errors; RPITIT
impls simplified to native `async fn`; large enum variants boxed. All mocks
verified as test-only.

## Changes

### Clippy Zero (35 → 0 warnings)

| Category | Count | Action |
|----------|-------|--------|
| Unused imports | 5 | Removed or `#[cfg(feature)]` gated |
| `const fn` upgrades | 4 | `show_metrics`, `with_persistence`, `minimal_config_toml`, `WadFile::new` |
| `async fn` simplification | 6 | RPITIT `impl Future<Output=…> + Send` → native `async fn` |
| Redundant closure | 1 | `PoisonError::into_inner` method reference |
| Large variant sizes | 2 | `Mdns(Box<…>)`, `Https(Box<…>)` |
| Privacy/visibility | 8 | `pub(super)` for doom-core, `pub` for test types under `#[cfg(test)]` |
| Missing docs | 6 | Doc comments on test-only enum variants |
| Module naming | 1 | Renamed inner `mod tests` to avoid `module_inception` |

### Typed Error Returns

`unix_socket_server.rs` `handle_uds_with_btsp` and `handle_tcp_with_btsp`
evolved from `Box<dyn std::error::Error + Send + Sync>` to typed
`ConnectionError` — the only errors these functions propagate are `io::Error`
and `serde_json::Error`, both already covered by `ConnectionError` variants.

### Mock Audit

All mocks confirmed properly gated:

- `MockComputeProvider` — `#[cfg(test)]`
- `mock_adapters` module — `#[cfg(test)]`
- `MockInputAdapter` / `QueuedInputAdapter` — `#[cfg(test)]`
- `mock_server` (NeuralApiProvider) — `#[cfg(test)]`
- `DemoDeviceProvider` — `#[cfg(feature = "mock")]`
- `BiomeOSClient` fixture methods — `#[cfg(any(test, feature = "test-fixtures"))]`
- Panel test doubles — `#[cfg(test)]`

### Remaining `dyn` Audit

| Usage | Location | Status |
|-------|----------|--------|
| `Box<dyn Fn(BiomeOSEvent) + Send + Sync>` | events.rs | Idiomatic callback |
| `Box<dyn Fn(EcosystemEvent) + Send + Sync>` | sse.rs | Idiomatic callback |
| `&dyn std::error::Error` | panel_registry | Standard error trait |
| Comments only | 8 files | Document prior `Box<dyn>` elimination |

## Test Results

- `cargo test --workspace --all-features` — **6,144 tests**, 0 failures
- `cargo clippy --workspace --all-targets` — **0 warnings**
- No `TODO`/`FIXME`/`HACK` markers in production code
- No hardcoded addresses in production code
- All external deps are pure Rust (no C/FFI in direct deps)
