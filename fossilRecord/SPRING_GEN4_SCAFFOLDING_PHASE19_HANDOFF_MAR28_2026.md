# Spring Gen4 Scaffolding — Phase 19 Handoff

**Date**: March 28, 2026
**Scope**: Resolved broken path dependencies across 7 spring repositories, built 5/6 spring primal binaries, updated plasmidBin, created gen4 spring composition graph, updated spring validation graphs and launch profiles.

---

## What Was Done

### 1. Dependency Resolution (Symlinks)

Created local symlinks under `springs/` so that `path = "..."` dependencies in spring `Cargo.toml` files resolve correctly:

| Symlink | Target | Springs Unblocked |
|---------|--------|-------------------|
| `springs/barraCuda` | `../primals/barraCuda` | airSpring, groundSpring, neuralSpring, wetSpring |
| `springs/primalTools/bingoCube` | `../../primals/bingoCube` | airSpring, wetSpring |
| `springs/phase1/toadStool` | `../../primals/toadstool` | groundSpring, wetSpring |
| `springs/phase1/toadstool` | `../../primals/toadstool` | (case variant) |
| `springs/coralReef` | `../primals/coralReef` | neuralSpring |
| `springs/phase2/loamSpine` | `../../primals/loamSpine` | ludoSpring |
| `springs/phase2/rhizoCrypt` | `../../primals/rhizoCrypt` | ludoSpring |
| `springs/phase2/sweetGrass` | `../../primals/sweetGrass` | ludoSpring |

These symlinks are a local-only prerequisite for compilation; they are not committed to any repository.

### 2. Upstream Primal Patches

**barraCuda (v0.3.5 → v0.3.7)**:
- Version bump in root `Cargo.toml` to satisfy `airSpring` version requirement
- Feature-gated `plasma_dispersion` module and `analyze_weight_matrix` behind `#[cfg(feature = "gpu")]` (these depend on GPU-only `Complex64` / `eigh` functions)
- Added `F16` variant to `Precision` enum and all associated match arms (`scalar`, `vec2`, `vec4`, `has_vec4`, `bytes_per_element`, `required_feature`, `op_preamble`)
- Added `F16` case to `precision_to_coral_strategy` in `coral_compiler/types.rs`
- Added 4 missing methods to `DeviceCapabilities` (`precision_routing`, `fp64_strategy`, `needs_exp_f64_workaround`, `check_allocation_safe`)
- Added `pub rel_tolerance: Option<f64>` to `Check` struct (all construction sites init to `None`)
- Re-exported `PrecisionRoutingAdvice` from `device::capabilities` module

**bingoCube/nautilus**:
- Added no-op `json = []` feature gate (springs requested this feature; `serde_json` was already unconditional)
- Added `pub input_dim: usize` to `ShellConfig` with `Default` init

### 3. Spring Primal Binaries Built

| Spring | Binary | Build Flags | Size (stripped) |
|--------|--------|-------------|-----------------|
| groundSpring | `groundspring` | `--no-default-features --features biomeos` | Deployed to plasmidBin/springs/ |
| healthSpring | `healthspring_primal` | full features | Deployed to plasmidBin/springs/ |
| ludoSpring | `ludospring` | full features | Deployed to plasmidBin/springs/ |
| neuralSpring | `neuralspring` | full features | Deployed to plasmidBin/springs/ |
| wetSpring | `wetspring` | `--no-default-features` | Deployed to plasmidBin/springs/ |
| airSpring | `airspring_primal` | — | **BLOCKED**: internal `data::Provider` trait / `data::NestGateProvider` struct missing |

All built binaries were stripped with `strip` and checksummed with `b3sum` (Blake3).

### 4. plasmidBin Updates

- `manifest.toml`: Added metadata entries for all 5 built springs (`produces_binary`, `stripped`, `arch`, per-arch sections)
- `sources.toml`: Added `[sources.<spring>]` entries with `repo`, `build_from_source`, `binary_name`, build flags
- `checksums.toml`: Added blake3 hashes for `x86_64-linux-musl` binaries
- `doctor.sh`: Added "Spring binary inventory" section checking presence, static linking, and stripping

### 5. gen4 Spring Composition Graph

Created `graphs/gen4/gen4_spring_composition.toml`:
- Deploys Tower (BearDog + Songbird), biomeOS substrate, then all 5 spring primals
- Concludes with a `cross_spring_validation` node that depends on all springs
- All nodes declare `by_capability`

### 6. Spring Validation Graph Updates

All 7 `graphs/spring_validation/*.toml` files updated:
- Inserted `start_biomeos` node (order 2) as the biomeOS substrate layer
- Spring primal nodes now `depends_on = ["start_biomeos"]`

### 7. Launch Profiles

Added profiles for 6 springs to `config/primal_launch_profiles.toml`:
- `airspring`, `groundspring`, `healthspring`, `hotspring`, `ludospring`, `neuralspring`, `wetspring`
- Each profile configures `extra_env` (mode, ports) and `env_sockets` (primal socket paths, biomeOS socket dir)

---

## Known Blockers

### airSpring Binary
`airSpring` expects `data::Provider` trait and `data::NestGateProvider` struct which are not present in its crate's `data` module. This is internal API drift within `airSpring` itself — not a dependency issue. Requires refactoring the `data` module or updating consumer code.

### Symlinks are Local-Only
The symlinks under `springs/` are not committed to any repository. Each developer must create them (or the ecosystem must be restructured to place primals where springs expect them). The plan document (`spring_gen4_scaffolding_0423829b.plan.md`) was the source of truth.

---

## Files Modified (primalSpring)

| File | Change |
|------|--------|
| `README.md` | Updated graph counts, added gen4 spring scaffolding section |
| `whitePaper/baseCamp/README.md` | Phase 19 changelog, updated status |
| `specs/CROSS_SPRING_EVOLUTION.md` | Phase 19 entry, renumbered future phases |
| `config/primal_launch_profiles.toml` | 6 spring launch profiles |
| `graphs/gen4/gen4_spring_composition.toml` | **NEW** — master spring composition graph |
| `graphs/spring_validation/*.toml` (7 files) | biomeOS substrate node inserted |

## Files Modified (ecoPrimals infra)

| File | Change |
|------|--------|
| `infra/plasmidBin/manifest.toml` | 5 spring binary entries |
| `infra/plasmidBin/sources.toml` | 5 spring build source entries |
| `infra/plasmidBin/checksums.toml` | 5 blake3 checksums |
| `infra/plasmidBin/doctor.sh` | Spring binary inventory section |

## Files Modified (upstream primals)

| File | Change |
|------|--------|
| `primals/barraCuda/Cargo.toml` | Version 0.3.5→0.3.7 |
| `primals/barraCuda/crates/barracuda/src/special/mod.rs` | GPU feature-gate plasma_dispersion |
| `primals/barraCuda/crates/barracuda/src/spectral/stats.rs` | GPU feature-gate analyze_weight_matrix |
| `primals/barraCuda/crates/barracuda/src/spectral/mod.rs` | Updated re-exports |
| `primals/barraCuda/crates/barracuda/src/device/capabilities/wgpu_caps.rs` | 4 missing methods |
| `primals/barraCuda/crates/barracuda/src/device/capabilities/mod.rs` | PrecisionRoutingAdvice re-export |
| `primals/barraCuda/crates/barracuda/src/shaders/precision/mod.rs` | F16 variant |
| `primals/barraCuda/crates/barracuda/src/device/coral_compiler/types.rs` | F16 in coral strategy |
| `primals/barraCuda/crates/barracuda/src/validation.rs` | rel_tolerance field |
| `primals/bingoCube/nautilus/Cargo.toml` | json feature gate |
| `primals/bingoCube/nautilus/src/shell.rs` | input_dim field |

---

**Next**: airSpring data module refactor, full ecosystem restructure (move primals to where springs expect them), LAN covalent deployment.
