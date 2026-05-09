# hotSpring Phase 60 Cross-Spring Parity Absorption — Handoff

**Date:** May 8, 2026
**Spring:** hotSpring v0.6.32
**Upstream audit:** primalSpring Phase 60 Cross-Spring Composition Parity Audit
**Score:** STRONG (3 evolution targets, 1 skipped)
**License:** AGPL-3.0-or-later

---

## Summary

hotSpring absorbed 3 of 4 evolution targets from primalSpring Phase 60:

| # | Target | Status | Detail |
|---|--------|--------|--------|
| 1 | Deploy graphs 1 → 5+ | **DONE** | 4 new domain-specific graphs |
| 2 | Registry cross-sync test | **DONE** | Shell script + Rust integration test |
| 3 | barraCuda optional dep | **DONE** | `optional = true` + `barracuda-local` default feature |
| 4 | Exp binary → workspace crates | **SKIPPED** | Hardware-specific, not composition experiments |

---

## Target 1: Deploy Graphs (1 → 5)

Created 4 new domain-specific NUCLEUS deployment profiles in `graphs/`:

| Graph | Composition | Science Domain |
|-------|-------------|----------------|
| `hotspring_plasma_md_deploy.toml` | Tower + Node (no coralReef) | Yukawa OCP, transport |
| `hotspring_nuclear_eos_deploy.toml` | Tower + Node + Nest | SEMF/HFB binding energies |
| `hotspring_spectral_deploy.toml` | Tower + barraCuda only | Anderson, Hofstadter, Lanczos |
| `hotspring_sovereign_gpu_deploy.toml` | Full NUCLEUS + coralReef | Sovereign GPU WGSL-to-SASS |

All graphs follow the existing `hotspring_qcd_deploy.toml` schema. The Rust
integration test `deploy_graphs_reference_only_registered_capabilities`
validates that all graph capabilities are in the local registry.

---

## Target 2: Registry Cross-Sync Test

### Shell script: `tools/check_method_strings.sh`

Adapted from primalSpring PG-65 pattern. Two checks:

1. **Local**: All dotted method strings in `barracuda/src/` must appear in
   `barracuda/config/capability_registry.toml`
2. **Cross**: All methods in hotSpring's registry must appear in
   primalSpring's canonical 389-method registry (when available)

Current findings:
- **111 local drift items** — method strings used in source for IPC calls
  to external primals (ember, device, qcd, tensor, etc.) that aren't in
  hotSpring's own capability registry. These are legitimate external method
  calls that should be triaged over time.
- **13 cross-registry drift items** — hotSpring-specific methods not yet in
  primalSpring's canonical registry (see below).

### Rust test: `tests/integration_registry_sync.rs`

Three tests:
- `local_registry_parses_cleanly` — validates TOML parse and >20 methods (**PASS**)
- `deploy_graphs_reference_only_registered_capabilities` — all graph capabilities registered (**PASS**)
- `cross_registry_sync_with_primalspring` — **IGNORED** (13 methods pending upstream)

### Upstream ask: Add 13 hotSpring methods to primalSpring canonical

These methods need to be added to `primalSpring/config/capability_registry.toml`:

```
composition.health
compute.df64
compute.dispatch.capabilities
compute.f64
physics.fluid
physics.hmc_trajectory
physics.lattice_gauge_update
physics.lattice_qcd
physics.molecular_dynamics
physics.nuclear_eos
physics.radiation
physics.thermal
physics.wilson_dirac
```

Suggested section: `[physics]` with `owner = "hotspring"` for the physics
domain methods, and existing `[composition]`/`[compute]` sections for the others.

---

## Target 3: barraCuda Optional Dependency

`barracuda/Cargo.toml` changes:

```toml
[features]
default = ["barracuda-local"]
barracuda-local = ["dep:barracuda"]

[dependencies]
barracuda = { path = "...", optional = true }
```

**Effect:** `cargo build` continues to work unchanged (default feature enabled).
`cargo build --no-default-features` gives IPC-only mode — a declaration of
intent matching ludoSpring's pattern. Full `#[cfg(feature)]` gating of all
70+ files using `barracuda::` imports is a future evolution (tracked as
GAP-HS-045 in `docs/PRIMAL_GAPS.md`).

---

## Target 4: Experiment Crate Migration (SKIPPED)

The 8 experiment binaries (`exp070` through `exp167`, 3,105 LOC) are all
hardware-specific GPU investigation tools (register dumps, SEC2 ACR, K80
FECS, warm handoff). They are correctly feature-gated (`low-level`,
`sovereign-dispatch`) and do not pollute the default build. Migration to
workspace crates adds organizational overhead without composition benefit.

If/when hotSpring adds composition-oriented experiments (NUCLEUS parity
tests), those should go in a new `experiments/` workspace from the start.

---

## Validation State

- **993 lib tests pass** (0 failures)
- **cargo clippy --lib --tests** clean (no new warnings)
- **3 registry sync tests**: 2 pass, 1 ignored (advisory cross-sync)
- **All 5 deploy graphs** parse and validate cleanly

---

## Files Changed

| File | Change |
|------|--------|
| `graphs/hotspring_plasma_md_deploy.toml` | NEW |
| `graphs/hotspring_nuclear_eos_deploy.toml` | NEW |
| `graphs/hotspring_spectral_deploy.toml` | NEW |
| `graphs/hotspring_sovereign_gpu_deploy.toml` | NEW |
| `tools/check_method_strings.sh` | NEW |
| `barracuda/tests/integration_registry_sync.rs` | NEW |
| `barracuda/Cargo.toml` | barraCuda optional + barracuda-local feature |
| `README.md` | Deploy graphs section, status date update |
| `CHANGELOG.md` | Phase 60 absorption entry |
| `docs/PRIMAL_GAPS.md` | GAP-HS-044 (registry drift), GAP-HS-045 (IPC-only) |
