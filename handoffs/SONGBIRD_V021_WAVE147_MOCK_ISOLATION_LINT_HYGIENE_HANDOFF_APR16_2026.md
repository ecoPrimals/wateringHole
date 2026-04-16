# Songbird v0.2.1 Wave 147 — Mock Isolation + Hardcoded Elimination + Lint Hygiene

**Date**: April 16, 2026
**Commit**: `cf900b69` (Wave 147)
**Previous**: `5099ecd1` (Wave 146), `d237c9c2` (Wave 145)
**Branch**: `main`

## Summary

Wave 147 closes the final deep-debt hygiene gaps identified by the comprehensive audit:
production mock isolation, raw IP/path elimination, and lint reason string completeness.
Builds on Waves 145 (async-trait elimination) and 146 (dyn audit + ring analysis).

## Wave 147 Changes

### Mock Isolation (birdsong::mocks)
- `birdsong::mocks` module gated behind `#[cfg(any(test, feature = "test-mocks"))]`
- All 9 mock `BirdSongEncryption` enum variants cfg-gated — zero mock types in production builds
- New `test-mocks` feature in `songbird-discovery/Cargo.toml`
- `songbird-orchestrator` enables `test-mocks` as dev-dependency
- Integration tests (`dark_forest`, `fault_injection`, `chaos_engineering`) gated with `#![cfg(feature = "test-mocks")]`

### Hardcoded IP/Path Elimination
- `fallback.rs`: raw `"127.0.0.1"` → `LOCALHOST` constant (3 sites)
- `relay.rs`: raw `"0.0.0.0:0"` → `EPHEMERAL_BIND_ADDR` constant
- `strategy.rs`: raw `"/var/run"` → `SYSTEM_RUNTIME_DIR` constant
- `paths.rs`: raw `"/var/run/biomeos/security.sock"` → `BIOMEOS_SYSTEM_RUNTIME_DIR` join
- New constants: `EPHEMERAL_BIND_ADDR`, `SYSTEM_RUNTIME_DIR`, `BIOMEOS_SYSTEM_RUNTIME_DIR`

### Lint Hygiene
- All remaining bare `#[allow(...)]` given `reason` strings:
  - `clippy::type_complexity` (rendezvous_handler.rs)
  - `clippy::too_many_lines` (dispatch.rs)
  - `unused_mut` (capability_providers.rs)
  - `deprecated` (security.rs, crypto/mod.rs)
  - `#![allow(deprecated)]` in 6 e2e test files

### Documentation Alignment
- README.md, CONTEXT.md, CONTRIBUTING.md test counts aligned to 7,377
- Python example clients dates updated (Nov 2025 → Apr 2026)

## Cumulative Status (Wave 144→147)

| Metric | Wave 144 | Wave 147 |
|--------|----------|----------|
| `#[async_trait]` | 113 | **0** |
| `dyn` dispatch (finite-implementor) | 19 | **0** |
| Production mocks | birdsong::mocks leaked | **0** (cfg-gated) |
| Raw IP strings in production | 4 files | **0** (constants) |
| Bare `#[allow()]` without reason | ~10 | **0** |
| Tests (lib) | 7,360 | **7,377** |
| Clippy warnings | 0 | **0** |
| Unsafe blocks | 0 | **0** |
| Files >800L | 0 | **0** |

## Verification

- `cargo check --workspace`: clean
- `cargo clippy --workspace -- -D warnings`: zero warnings
- `cargo fmt --all --check`: clean
- `cargo deny check`: advisories ok, bans ok, licenses ok, sources ok
- `cargo test --workspace --lib`: 7,377 passed, 0 failed

## Remaining Deep Debt (backlog)

- BTSP Phase 3: cipher negotiation + encrypted framing
- Line coverage: 72.29% → target 90%
- `ring` in Cargo.lock: upstream `rustls-rustcrypto` release needed (documented in deny.toml)
- 6 files in 700-763L range (below 800L threshold, monitor for growth)
