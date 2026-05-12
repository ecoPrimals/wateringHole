<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Squirrel v0.1.0-alpha.32 — Build Fix & Capability-Domain Decoupling Wave 2

**Date**: April 3, 2026
**Primal**: Squirrel (AI Coordination)
**Version**: 0.1.0-alpha.32
**Tests**: 7,165 passing / 0 failures / 110 ignored
**Quality**: `fmt` ✓, `clippy -D warnings` ✓, `deny` ✓, `doc` ✓

## Summary

primalSpring audit remediation: fix broken integration test build, then migrate
remaining actionable Songbird name-coupling to capability-domain abstractions.

## Changes

### 1. Integration Test Build Fix (BLOCKING)

`squirrel-ai-tools` integration test (`tests/basic_test.rs`) failed to compile:
- `MockAIClient` gated behind `cfg(any(test, feature = "testing"))`, but integration
  test binaries don't receive `cfg(test)` for the library crate.
- E0282 type inference error on `list_models()` return.

**Fix**: Mock-dependent tests wrapped in `#[cfg(feature = "testing")]` module.
`cargo test` compiles clean (2 tests); `cargo test --all-features` runs all 4.
Type annotation `Vec<String>` added for inference.

### 2. Flaky Test Fix

`test_find_biomeos_socket_env_override` asserted `find_biomeos_socket().is_none()`
after setting env to non-existent path. Fails on hosts where real biomeOS sockets
exist in fallback paths. Now only validates the env-override path wasn't returned.

### 3. Capability-Domain Decoupling (Wave 2)

All remaining actionable Songbird name-coupling in production code migrated:

| Before | After | Location |
|--------|-------|----------|
| `register_songbird_service()` | `register_orchestration_service()` | `orchestration_adapter.rs` |
| `delegate_to_songbird()` | `delegate_to_http_proxy()` | `ipc.rs` |
| `metric_names::songbird` | `metric_names::orchestration` | `metric_names.rs` |
| `SongbirdIntegration` | `ServiceMeshIntegration` | `orchestration/mod.rs` |
| `ConfigBuilder::songbird()` | `ConfigBuilder::orchestration()` | `config/builder.rs` |
| "Songbird" in examples | capability-domain names | `universal_adapters_demo.rs`, `observability_demo.rs` |
| "Production uses Unix sockets → Songbird" | "via capability discovery" | `ai-tools/Cargo.toml` comments |

### 4. Remaining Songbird References (Acceptable)

~325 total references remain across the workspace. All are in acceptable categories:
- `primal_names` constants (logging/interning only, not dispatch)
- Deprecated type aliases with `#[deprecated]` attributes
- `#[serde(alias = "songbird_endpoint")]` for backward compatibility
- Env var fallback chains (`.or_else(|_| std::env::var("SONGBIRD_*"))`)
- Doc comments explaining migration history
- Test assertions

No `SONGBIRD_HOST` or `SONGBIRD_URL` env vars exist in the codebase.

## Verification

```
cargo fmt --all -- --check     → PASS
cargo clippy --workspace --all-targets --all-features -- -D warnings → PASS
cargo test --workspace --all-features → 7,165 passed, 0 failed
cargo deny check               → advisories ok, bans ok, licenses ok, sources ok
```
