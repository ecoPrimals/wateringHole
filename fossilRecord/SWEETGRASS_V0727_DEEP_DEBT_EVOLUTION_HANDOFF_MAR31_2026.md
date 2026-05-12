# SweetGrass v0.7.27 — Deep Debt & Evolution Handoff

**Date**: 2026-03-31
**Primal**: sweetGrass
**Version**: v0.7.27
**Status**: Healthy, UDS conformant, ecosystem-ready

---

## Summary

Comprehensive deep-debt resolution and codebase evolution session. All production
code is now modern idiomatic Rust with zero cfg(test) leakage, zero hardcoded
primal names, centralized vocab URIs, and full cargo-deny compliance.

---

## Changes Executed

### 1. cargo-deny Fixed (was: 11 duplicate crate failures)

- Removed stale `RUSTSEC-2026-0009` advisory ignore
- Added `skip-tree` entries for transitive dev-dependency chains: `sled`,
  `criterion`, `proptest`, `testcontainers`, `testcontainers-modules`
- Added `skip` for `hashbrown 0.15.5` (sqlx → hashlink vs indexmap 0.16)
- **Result**: `advisories ok, bans ok, licenses ok, sources ok`

### 2. `#![forbid(unsafe_code)]` Standardized

All 4 crate roots that used conditional `cfg_attr(not(test), forbid)` /
`cfg_attr(test, deny)` changed to unconditional `#![forbid(unsafe_code)]`.
No test code uses unsafe — the conditional was unnecessary.

### 3. Deprecated `primal_names::names` Removed

The hardcoded primal name registry (`RHIZOCRYPT`, `LOAMSPINE`, `BEARDOG`, etc.)
has been deleted. Zero external callers existed. Generic helpers (`socket_env_var`,
`address_env_var`, `env_vars` module) are preserved for capability-agnostic use.

### 4. Mock Factory Functions Evolved

Removed `#[cfg(any(test, feature = "test"))]` compile-time branching from 3
production factory functions:

- `create_signing_client_async` — always returns real tarpc client
- `create_session_events_client_async` — always returns real tarpc client
- `create_anchoring_client_async` — always returns real tarpc client

Tests now construct mock clients directly. Zero cfg(test) leakage in production paths.

### 5. Hardcoded Vocab URIs Centralized

- `provo/mod.rs` now imports from `sweet_grass_core::braid::types` constants
- Added `RDFS_VOCAB_URI` to centralized vocab constants
- ecoPrimals namespace honours `ECOP_VOCAB_URI` env var at runtime
- Added `MIME_META_BRAID`, `MIME_CERTIFICATE` to `core::identity`
- Factory code uses centralized constants

### 6. Test Coverage Improved

- 16 new tests across config, compression, signer, listener, anchor
- Coverage: **90.90% region / 89.58% line** (llvm-cov)
- 1,175 tests passing, zero failures
- Remaining line gap is infrastructure-dependent (Postgres/Docker, tarpc servers)

### 7. Dependency Analysis

- `async-trait`: Required — 5+ traits dispatch through `dyn`
- `parking_lot`: Deliberately chosen for infallible non-poisoning RwLock
- `sled`: Already deprecated with migration docs, feature-gated
- All deps pure Rust, `deny.toml` enforced

### 8. Root Docs Updated

- README.md: Updated test count (1,175), coverage (90.90%), file count (137),
  max file (705 lines), protocol stack table, `--port` flag, env vars
- All referenced docs verified to exist

---

## Current Protocol Stack

| Protocol | Env Var | Status |
|----------|---------|--------|
| tarpc | `SWEETGRASS_TARPC_ADDRESS` | Active |
| TCP JSON-RPC | `SWEETGRASS_PORT` | Active (UniBin `--port`) |
| UDS JSON-RPC | `SWEETGRASS_SOCKET` | Active at `/run/user/1000/biomeos/sweetgrass.sock` |
| HTTP JSON-RPC | `SWEETGRASS_HTTP_ADDRESS` | Active (27 methods) |
| REST | `SWEETGRASS_HTTP_ADDRESS` | Active |

Capability-domain symlink: `provenance.sock -> sweetgrass.sock`

---

## Verification

```
cargo fmt --all -- --check     ✓ clean
cargo clippy -D warnings       ✓ zero warnings (pedantic + nursery)
cargo test --all-features      ✓ 1,175 tests, 0 failures
cargo deny check               ✓ advisories ok, bans ok, licenses ok, sources ok
cargo doc --no-deps            ✓ zero warnings
cargo llvm-cov                 ✓ 90.90% region / 89.58% line
```

---

## Blocking On

- ~~**rhizoCrypt** (RC-01): No UDS socket yet — blocks provenance trio compositions~~ **RESOLVED** (v0.14.0-dev session 23, March 31, 2026)
- **loamSpine** (LS-03): Startup panic — blocks anchoring pipeline

Once both fix, sweetGrass is ready for provenance pipeline, session provenance,
and RootPulse workflows.

---

## No Open Debt

All identified items resolved:

- [x] cargo-deny duplicates
- [x] forbid(unsafe_code) standardization
- [x] Deprecated primal names removal
- [x] Mock factory evolution
- [x] Hardcoded vocab centralization
- [x] Coverage push above 90% region
- [x] Dependency analysis and documentation
- [x] Root docs updated
