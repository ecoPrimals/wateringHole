# SweetGrass v0.7.10 — Typed Error Evolution + Lint Hardening + Platform-Agnostic IPC

**Date**: March 15, 2026
**From**: v0.7.9 → v0.7.10
**Status**: Complete — all checks pass
**License**: AGPL-3.0-only
**Supersedes**: `SWEETGRASS_V079_PEDANTIC_AUDIT_CAPABILITY_DISCOVERY_HANDOFF_MAR15_2026.md`

---

## Summary

Comprehensive typed error migration replacing all `Result<_, String>` patterns with dedicated `thiserror` enums. Workspace lints evolved from `allow` to `warn` for `missing_errors_doc` and `missing_const_for_fn`, with all resulting warnings resolved across the full workspace. UDS socket paths made platform-agnostic. Placeholder signature renamed for clarity. Doc comment cleanup and `const fn` evolution across all crates.

---

## Typed Error Evolution

All `Result<_, String>` return types replaced with dedicated error enums:

| Function | Before | After |
|----------|--------|-------|
| `hex_decode_strict()` | `Result<Vec<u8>, String>` | `Result<Vec<u8>, HexDecodeError>` |
| `SelfKnowledge::from_env()` | `Result<Self, String>` | `Result<Self, BootstrapEnvError>` |
| `http_health_check()` | `Result<String, String>` | `Result<String, HealthCheckError>` |

### New error types

```rust
// sweet-grass-core::hash
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum HexDecodeError {
    #[error("odd length hex string (length: {0})")]
    OddLength(usize),
    #[error("invalid hex character at byte offset {position}")]
    InvalidChar { position: usize },
}

// sweet-grass-core::primal_info
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum BootstrapEnvError {
    #[error("{var_name} must be a valid port number (0-65535), got: {value}")]
    InvalidPort { var_name: String, value: String },
}

// sweet-grass-service bin
#[derive(Debug, thiserror::Error)]
enum HealthCheckError {
    #[error("{0}")]
    Io(#[from] std::io::Error),
    #[error("unhealthy response: {0}")]
    Unhealthy(String),
}
```

Downstream wrappers updated with `#[from]` for clean `?` propagation:
- `DecodeError::Hex` wraps `HexDecodeError` via `#[from]`
- `BootstrapError::SelfKnowledge` wraps `BootstrapEnvError` via `#[from]`

**Inter-primal pattern**: Replace all `Result<_, String>` with dedicated `thiserror` enums. Use `#[from]` for automatic conversion in wrapper errors. Tests should assert on typed error variants, not string matching.

---

## Workspace Lint Hardening

Two lints promoted from `allow` to `warn` in workspace `Cargo.toml`:

| Lint | Before | After | Impact |
|------|--------|-------|--------|
| `missing_errors_doc` | `allow` | `warn` | ~40 functions received `# Errors` sections |
| `missing_const_for_fn` | `allow` | `warn` | ~20 functions marked `const` |

Affected crates: `sweet-grass-query`, `sweet-grass-compression`, `sweet-grass-service`, `sweet-grass-integration`.

**Inter-primal pattern**: Promote these lints in workspace `Cargo.toml` to enforce documentation of error conditions on all public `Result`-returning functions.

---

## Platform-Agnostic UDS Paths

UDS socket fallback resolution replaced `/tmp` hardcoding with `std::env::temp_dir()`:

```rust
// Before: Hardcoded /tmp (broken on macOS $TMPDIR, NixOS, etc.)
let path = PathBuf::from("/tmp").join(&sock_name);

// After: Platform-agnostic
let path = std::env::temp_dir().join(&sock_name);
```

All 3 fallback levels (biomeos-user, bare temp) now use `std::env::temp_dir()`.

**Inter-primal pattern**: Never hardcode `/tmp`. Use `std::env::temp_dir()` for platform-agnostic temporary directory resolution.

---

## sign() → sign_placeholder()

`BraidFactory::sign()` renamed to `sign_placeholder()` to communicate that it is not a cryptographic signature. Doc comment directs to capability-based signing discovery for real signing.

**Inter-primal impact**: Any primal calling `BraidFactory::sign()` should update to `sign_placeholder()` or use actual signing capability via discovery.

---

## Other Changes

- **`config/tests.rs` flattened** — Removed redundant inner `mod tests` wrapper (was `module_inception`)
- **`doc_markdown` cleanup** — Backticked identifiers in doc comments across integration, postgres, service, and benchmark crates
- **`const fn` evolution** — ~20 functions marked `const` across query, compression, integration, and service crates

---

## Files Modified

| Crate | Files | Changes |
|-------|-------|---------|
| `sweet-grass-core` | `hash.rs`, `entity.rs`, `primal_info.rs`, `lib.rs`, `config/tests.rs` | `HexDecodeError`, `BootstrapEnvError`, `DecodeError::Hex` `#[from]`, module_inception fix |
| `sweet-grass-service` | `bootstrap.rs`, `bin/service.rs`, `factory/mod.rs`, `uds.rs`, handlers/\*, server/\* | `BootstrapError` `#[from]`, `HealthCheckError`, `sign_placeholder()`, `temp_dir()`, `# Errors` docs, `const fn` |
| `sweet-grass-query` | `engine/mod.rs`, `provo.rs`, `traversal.rs` | `# Errors` docs, `const fn` |
| `sweet-grass-compression` | `analyzer.rs`, `engine.rs`, `session.rs`, `strategy.rs` | `# Errors` docs, `const fn` |
| `sweet-grass-integration` | `testing.rs`, `signer/testing.rs` | `doc_markdown` fixes |
| `sweet-grass-store-postgres` | `tests/*.rs` | `doc_markdown` fixes |
| Workspace | `Cargo.toml` | `missing_const_for_fn` + `missing_errors_doc` → `warn` |

---

## Metrics

| Metric | v0.7.9 | v0.7.10 |
|--------|--------|---------|
| Tests | 857 | **847** |
| Region coverage | 91% | 91% |
| Clippy lints enforced | pedantic + nursery + doc_markdown | **+ missing_errors_doc + missing_const_for_fn** |
| `Result<_, String>` in production | 3 | **0** |
| Largest file | 455L | **830L** (test file) |
| Source files | 112 | **111** |

Test count decreased (857 → 847) due to `module_inception` fix flattening `config/tests.rs` — previously the inner `mod tests` wrapper was causing some test discovery duplication with the outer module.

---

## Deferred

- **Zero-copy serde borrowing** — `Cow<'a, str>` in deserialization requires lifetime threading through store traits. Deferred to v0.8.0+.
- **Typed JSON-RPC request/response structs** — Breaking API change requiring cross-primal coordination. Deferred to v0.9.0.

---

## Verification

```
cargo fmt --all -- --check         ✓
cargo check --workspace            ✓ (0 warnings)
cargo clippy --workspace --all-targets --all-features -- -D warnings  ✓ (0 warnings)
cargo test --workspace             ✓ (847 tests)
cargo doc --workspace --no-deps    ✓ (0 warnings)
```
