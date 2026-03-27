# SweetGrass v0.7.8 — Deep Debt Evolution: Zero-Copy + Benchmarks + Config

**Date**: March 14, 2026
**From**: v0.7.7 → v0.7.8
**Status**: Complete — all checks pass

---

## Summary

Comprehensive debt resolution and modernization. Zero-copy types expanded across all identifier types, `BraidSignature` evolved to `Cow<'static, str>`, JSON-LD context uses `IndexMap` for deterministic serialization, all `#[allow]` attributes evolved to precise `#[expect(..., reason)]`, criterion benchmarks added, TOML config file support with XDG-compliant hierarchy, large files smart-refactored, primal identity constants centralized, hardcoded test addresses extracted to constants.

---

## Zero-Copy Evolution

### `ActivityId(String)` → `ActivityId(Arc<str>)`

All four identifier types now use `Arc<str>` for O(1) clone:

| Type | Backing | Clone Cost |
|------|---------|------------|
| `ContentHash` | `Arc<str>` | O(1) |
| `BraidId` | `Arc<str>` | O(1) |
| `Did` | `Arc<str>` | O(1) |
| `ActivityId` | `Arc<str>` | O(1) — **new in v0.7.8** |

Custom `Deserialize`, `From<&str>`, `From<String>` impls added for ergonomic conversion.

### `BraidSignature` → `Cow<'static, str>`

Static values like `"Ed25519Signature2020"` and `"assertionMethod"` are now `Cow::Borrowed` (zero heap allocation). Dynamic values (DID key refs, base64 signatures) use `Cow::Owned`. Named constants extracted: `SIG_TYPE_ED25519`, `PROOF_PURPOSE_ASSERTION`, etc.

### `BraidContext.imports` → `IndexMap`

Guarantees deterministic serialization order — critical for content-addressed hashing and reproducible JSON-LD output.

---

## Primal Identity Centralization

New `sweet_grass_core::identity` module:

```rust
pub mod identity {
    pub const PRIMAL_NAME: &str = "sweetgrass";
    pub const PRIMAL_DISPLAY_NAME: &str = "SweetGrass";
}
```

Eliminates scattered string literals in `primal_info.rs`, `config.rs`, `health.rs`, `uds.rs`, `bootstrap.rs`. All now reference the centralized constants.

**Inter-primal impact**: Other primals should follow this pattern — centralize identity constants rather than scattering string literals.

---

## `#[allow]` → `#[expect(..., reason)]`

All ~50+ `#[allow]` attributes across all 10 crates evolved to precise `#[expect]` with explicit reason strings. Each expectation is trimmed to only the lints actually triggered — unfulfilled expectations are compile errors, providing ongoing enforcement.

**Pattern for other primals**:

```rust
#[cfg(test)]
#[expect(
    clippy::expect_used,
    clippy::unwrap_used,
    reason = "test module: expect/unwrap are standard in tests"
)]
mod tests { ... }
```

---

## Criterion Benchmarks

New `crates/sweet-grass-service/benches/core_operations.rs` with 7 benchmark groups:

| Group | Operation |
|-------|-----------|
| `braid_creation` | `BraidFactory::from_data()` at 1KB/10KB/100KB |
| `store_operations` | `MemoryStore::put()` and `get()` |
| `content_hashing` | SHA-256 and `compute_signing_hash()` |
| `store_query_100_braids` | `MemoryStore::query()` over 100 braids |
| `attribution_calculate_single` | Single attribution calculation |
| `compression_single_braid` | 0/1/Many compression model |
| `provenance_graph_traversal` | 3-node provenance chain traversal |

Run with: `cargo bench --package sweet-grass-service`

---

## TOML Config File Support

`SweetGrassConfig::load()` implements full wateringHole hierarchy: **CLI args > env vars > config file > defaults**.

Config file search order:
1. `$SWEETGRASS_CONFIG` environment variable
2. `$XDG_CONFIG_HOME/sweetgrass/config.toml`
3. `~/.config/sweetgrass/config.toml`

New `ConfigError::Io` and `ConfigError::Parse` variants for file errors.

**Inter-primal impact**: Establishes the config file pattern. Other primals should implement equivalent TOML loading with the same hierarchy.

---

## Smart Refactoring

| File | Before | After |
|------|--------|-------|
| `factory.rs` | 820 lines | `factory/mod.rs` (~310L) + `factory/tests.rs` (~330L) |
| `listener/mod.rs` | 703 lines | `mod.rs` (~320L) + `testing.rs` + `tests.rs` |

All files remain under 1000 LOC. Largest is `config.rs` at 879 lines (gained TOML support).

---

## Test Address Constants

Centralized in `sweet-grass-integration/src/testing.rs`:

| Constant | Value | Purpose |
|----------|-------|---------|
| `TEST_BIND_ADDR` | `"127.0.0.1:0"` | OS-allocated bind addresses |
| `TEST_REST_URL` | `"http://localhost:8080"` | Discovery REST fixtures |
| `TEST_TARPC_ADDR` | `"localhost:9000"` | Discovery tarpc fixtures |
| `TEST_INVALID_ADDR` | `"127.0.0.1:1"` | Connection-failure tests |

---

## Metrics

| Metric | v0.7.7 | v0.7.8 |
|--------|--------|--------|
| Tests | 849 | **853** |
| Region coverage | 91% | 91% |
| Zero-copy types | 3 | **4** + Cow on BraidSignature |
| `#[allow]` in prod | ~3 | **0** (all `#[expect]`) |
| Benchmark groups | 0 | **7** |
| Config file support | No | **Yes** (TOML, XDG) |
| Largest file | 828L | 879L |

---

## Verification

```
cargo fmt --all -- --check         ✓
cargo clippy --all-targets -- -D warnings  ✓
cargo test --workspace --all-features      ✓ (853 tests)
RUSTDOCFLAGS="-D warnings" cargo doc       ✓
```
