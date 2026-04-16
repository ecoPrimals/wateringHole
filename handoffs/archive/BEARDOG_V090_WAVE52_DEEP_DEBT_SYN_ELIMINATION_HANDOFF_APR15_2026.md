# BearDog v0.9.0 — Wave 52: Deep Debt & syn Elimination Handoff

**Date:** April 15, 2026
**Primal:** BearDog
**Version:** 0.9.0
**Wave:** 52

## Summary

Wave 52 focuses on deep debt elimination: removing unused `syn`/`async-trait` compilation overhead and smart-refactoring large production files by domain concern.

## Changes

### async-trait / syn Elimination

Removed unused `async-trait` dependency from 5 crates that declared it but never used the macro:

- `beardog-discovery`
- `beardog-ipc`
- `beardog-adapters`
- `beardog-workflows`
- `beardog-integration`

This reduces the `syn` proc-macro compilation surface. The remaining 48 `#[async_trait]` instances are all on `dyn Trait` definitions — required for object safety until RPITIT dyn-compatibility lands in stable Rust.

### Smart File Refactoring

Refactored 3 production files approaching the 800 LOC threshold by domain concern (not arbitrary splits):

| Original File | Before (LOC) | After (max file) | Structure |
|---------------|:---:|:---:|-----------|
| `android_strongbox/core.rs` | 796 | 298 | `core/` dir: mod.rs, unified.rs, manager_hsm.rs, hsm_key_provider.rs |
| `production/monitoring.rs` | 794 | 340 | `monitoring/` dir: mod.rs, config.rs, data.rs, collectors.rs |
| `crypto_handlers_tor.rs` | 792 | 184 | `crypto_handlers_tor/` dir: mod.rs, constants.rs, primitives.rs, ntor_client.rs, ntor_server.rs, cell.rs, kdf.rs |

All public APIs preserved. Test modules remain in their existing sibling files.

### Clippy Compliance

- Added `# Errors` doc sections to 13 public `Result`-returning functions
- Derived `Default` for `HealthStatus` enum (replacing manual impl)
- Fixed `doc_markdown` lint for `ChaCha20` in module docs

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace -D warnings` | Clean |
| `RUSTDOCFLAGS="-D warnings" cargo doc` | Clean |
| `cargo test --workspace` | **14,787** pass, **0** fail |

## Remaining Cross-Primal Items

From primalSpring audit (status unchanged from Wave 51):

1. **Bond persistence IPC wiring** — `CapabilityDiscoveryBondPersistence` implemented; awaiting loamSpine `bonding.ledger.*` RPCs for integration testing
2. **HSM/Titan M2 dispatch** — `HsmProviderRegistry::discover()` flow implemented; awaiting hardware test environment
3. **async-trait: 48 remaining** — all on `dyn Trait` objects, requires RPITIT dyn-compatibility

## Debt Survey (Clean)

| Category | Count |
|----------|:-----:|
| `unsafe` blocks | 0 |
| `TODO/FIXME` markers | 0 |
| `Box<dyn Error>` in production | 0 |
| Production mocks | 0 |
| Files > 800 LOC (production) | 0 |
