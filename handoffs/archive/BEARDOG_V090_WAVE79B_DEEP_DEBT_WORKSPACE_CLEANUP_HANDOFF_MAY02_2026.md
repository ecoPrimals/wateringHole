# BearDog v0.9.0 — Wave 79b: Deep Debt Pass — Workspace Dependency Drift, Build Cleanup & Dead Code Removal

**Date**: May 2, 2026
**Primal**: BearDog (Tower Atomic — Security/Crypto)
**Wave**: 79b

---

## Summary

Full deep debt audit and cleanup pass. 16 workspace dependency drifts normalized, stale build.rs cfg emission removed, dead tarpc_server source tree deleted, stale path references fixed across docs and showcases, root documentation dates and metrics harmonized.

## Changes

### Workspace Dependency Normalization (16 deps)

External crate version pins in individual `Cargo.toml` files centralized to root `[workspace.dependencies]`:

- `aes`, `ctr` (beardog-utils)
- `ahash`, `urlencoding`, `approx` (beardog-core)
- `local-ip-address` (beardog-discovery)
- `ecdsa`, `x509-parser`, `arrayref`, `data-encoding` (beardog-tunnel)
- `path-absolutize`, `console`, `indicatif` (beardog-deploy)
- `rpassword`, `whoami`, `assert_cmd`, `predicates` (beardog-cli)
- `directories` (beardog-installer)

### Build Script Cleanup

- Removed stale `cargo:rustc-cfg=feature="android_native"` emission from `beardog-tunnel/build.rs` (feature removed from `[features]` in Wave 78b but build.rs still emitted it on Android targets).

### Dead Code Removal

- Deleted `crates/beardog-ipc/src/tarpc_server/` (12 files) — tarpc dependency removed in January 2026 but source files remained on disk, unwired from `lib.rs`.
- Reclassified `tempfile` from `[dependencies]` to `[dev-dependencies]` in `beardog-security` (zero production usage).

### Documentation Reconciliation

- All root docs (README, STATUS, ROADMAP, ARCHITECTURE, CONTEXT, START_HERE) bumped to May 2, 2026.
- Test count harmonized to 14,800+ (actual: 14,806) across all docs.
- Stale `eastgate`/`phase1/beardog` paths fixed in `docs/references/RUN_ENTROPY_TEST.md`, `docs/PRIMAL_CONTRACTS.md`, `specs/current/security/LIVESPORE_FINAL_ARCHITECTURE.md`, and 2 showcase READMEs.
- CONTRIBUTING.md: file size limit corrected (1000 → 800 LOC), tarpc reference removed.
- README: BTSP method listing updated for Phase 3.
- `solokey_testing_suite.rs` example: stale `hidapi` reference → `beardog-hid`.

### Deep Debt Audit Confirmed Clean

| Dimension | Result |
|-----------|--------|
| Files >800 LOC (production) | 0 |
| `unsafe` blocks | 0 |
| `todo!()` / `unimplemented!()` | 0 |
| `#[async_trait]` | 0 |
| `Box<dyn Error>` in production | 0 |
| Hardcoded peer primal names | 0 (runtime logic) |
| Production mocks outside `#[cfg(test)]` | 0 |
| `TODO` / `FIXME` / `HACK` comments | 0 |

## CI Results

- `cargo check --workspace`: clean
- `cargo fmt --check`: clean
- `cargo deny check`: advisories ok, bans ok, licenses ok, sources ok
- `cargo test --workspace`: 14,806 passed, 0 new failures (1 pre-existing flaky test in beardog-cli)

## Files Changed

- `Cargo.toml` (root) — 16 new workspace deps
- `crates/beardog-utils/Cargo.toml`
- `crates/beardog-core/Cargo.toml`
- `crates/beardog-discovery/Cargo.toml`
- `crates/beardog-tunnel/Cargo.toml`
- `crates/beardog-tunnel/build.rs`
- `crates/beardog-deploy/Cargo.toml`
- `crates/beardog-cli/Cargo.toml`
- `crates/beardog-installer/Cargo.toml`
- `crates/beardog-security/Cargo.toml`
- `crates/beardog-ipc/src/tarpc_server/` — DELETED (12 files)
- Root docs: README.md, STATUS.md, ROADMAP.md, ARCHITECTURE.md, CONTEXT.md, START_HERE.md, CONTRIBUTING.md, CHANGELOG.md
- `docs/references/RUN_ENTROPY_TEST.md`
- `docs/PRIMAL_CONTRACTS.md`
- `specs/current/security/LIVESPORE_FINAL_ARCHITECTURE.md`
- `showcase/00-local-primal/01-hello-beardog/README.md`
- `showcase/02-ecosystem-integration/01-songbird-btsp/README.md`
- `examples/solokey_testing_suite.rs`
