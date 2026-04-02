<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# barraCuda v0.3.11 — Cross-Spring Deep Absorption

**Date**: 2026-03-29
**Sprint**: 22g
**Version**: 0.3.11
**Scope**: Deep cross-spring absorption (hotSpring silicon routing patterns, healthSpring GPU shaders, ludoSpring discovery robustification), `SiliconProfile` model, `SUBGROUP` feature detection, 6-format capability parser, env-configurable IPC tolerances
**Previous**: BARRACUDA_V0311_SPRING_ABSORPTION_DEEP_DEBT_HANDOFF_MAR29_2026

---

## Summary

Comprehensive cross-spring absorption executing on hotSpring V0632, healthSpring V44, and
ludoSpring V34 handoffs. Core absorptions: TMU-accelerated PRNG pattern (Box-Muller via texture
lookup), subgroup-accelerated reduction (warp-level `subgroupAdd`), ROP fixed-point force
accumulation (barrier-free multi-pole dispatch), Hill dose-response / population PK Monte Carlo /
Shannon-Simpson diversity GPU shaders with full Rust dispatch + CPU reference implementations.
Infrastructure: `SiliconProfile` silicon personality model for tier-based workload routing,
`wgpu::Features::SUBGROUP` negotiation, 6-format primal capability parser, env-configurable
IPC timeouts. 4,030+ tests, 0 failures. Clippy pedantic+nursery clean.

## hotSpring Absorption (V0632 Silicon Saturation)

### WGSL Shaders (4 new)

| Shader | Silicon Unit | Pattern |
|--------|-------------|---------|
| `su3_random_momenta_tmu_f64.wgsl` | TMU (Tier 0) | Texture lookup replaces ALU transcendentals |
| `sum_reduce_subgroup_f64.wgsl` | Subgroup (Tier 4) | `subgroupAdd` → fewer barriers, no shared memory for intra-warp |
| `su3_fermion_force_accumulate_rop_f64.wgsl` | ROP (Tier 3) | Fixed-point `atomicAdd(i32)` for barrier-free multi-pole |
| `su3_force_atomic_to_momentum_f64.wgsl` | ROP (Tier 3) | i32 fixed-point → f64 momentum conversion |

### Rust Modules (3 new)

- **`ops/lattice/tmu_tables.rs`**: `TmuLookupTables` — builds R32Float log table + Rg32Float
  trig table (4096x1 each) via `wgpu::TextureDescriptor`. Reusable across trajectories.
- **`ops/lattice/rop_force_accum.rs`**: Fixed-point accumulation params (`make_pole_params`,
  `make_convert_params`), workgroup count helpers. Scale = 2^20 (~6 digits, sufficient for
  O(dt^2) integrator error).
- **`device/silicon_profile.rs`**: `SiliconProfile` + `SiliconUnit` + `UnitThroughput` +
  `CompositionEntry` + `GpuVendorTag`. `route_workload()` selects cheapest silicon for a
  workload given measured throughput. JSON serialization for profile persistence.

## healthSpring Absorption (V44)

### WGSL Shaders (3 new)

| Shader | Domain | Dispatch |
|--------|--------|----------|
| `hill_dose_response_f64.wgsl` | PK/PD | `E(c) = Emax * c^n / (c^n + EC50^n)` via f32 exp/log bridge |
| `population_pk_f64.wgsl` | Pop PK | Wang hash + xorshift32 PRNG, single-compartment AUC |
| `diversity_f64.wgsl` | Ecology | Shannon + Simpson via workgroup tree reduction |

### Rust Modules (3 new)

- **`ops/health/hill_dose_response.rs`**: `HillDoseResponseGpu` + `HillConfig` + CPU reference.
- **`ops/health/population_pk.rs`**: `PopulationPkGpu` + `PopPkConfig` + CPU reference with
  matching Wang hash + xorshift32 for GPU parity validation.
- **`ops/health/diversity.rs`**: `DiversityGpu` + `DiversityResult` + CPU reference for
  Shannon entropy and Simpson diversity.

## ludoSpring Absorption (V34)

### 6-Format Capability Parser

- **`discovery/capabilities.rs`**: Normalises 6 JSON capability shapes into `Vec<String>`:
  - Format A: Flat string array
  - Format B: Object array with `name` field
  - Format C: Nested `{"capabilities": [...]}`
  - Format D: Double-nested `{"capabilities": {"capabilities": [...]}}`
  - Format E: BearDog `provided_capabilities` with method lists
  - Format F: Top-level flat array (Songbird)
  Includes `generate_semantic_aliases()` and `inject_base_capabilities()`.

### Env-Configurable IPC Tolerances

- **`discovery/tolerances.rs`**: `rpc_timeout_secs()`, `probe_timeout_ms()`,
  `connect_probe_timeout_ms()` with `BARRACUDA_*` env var overrides.

## Infrastructure

### `SUBGROUP` Feature Detection

- **`wgpu::Features::SUBGROUP`** added to `desired_features()` and `desired_features_extended()`
  in device creation — negotiated at adapter init, not assumed.
- **`WgpuDevice::has_subgroups()`** accessor.
- **`DeviceCapabilities::has_subgroups`** field wired into `from_device()`.
- Enables conditional use of `sum_reduce_subgroup_f64.wgsl` over shared-memory-only reduction.
- **naga caveat**: Do NOT add `enable subgroups;` to WGSL — naga 28 generates broken SPIR-V.
  The device feature flag alone is sufficient.

## Quality

- **Tests**: 4,030+ pass, 0 failures, 15 skipped (CI profile)
- **Clippy**: pedantic + nursery, zero errors, zero new warnings
- **New test count**: +46 tests from absorption modules
- **Shader count**: 823 WGSL shaders (up from 816)

## For Other Primals

### New Capabilities Available

1. **`SiliconProfile`**: Any primal can now build/load a silicon personality for a GPU and use
   `route_workload()` to select the cheapest functional unit for each dispatch phase.
2. **Subgroup shaders**: `sum_reduce_subgroup_f64.wgsl` is a template for subgroup-accelerated
   reductions. Springs can copy the pattern for their domain-specific reductions.
3. **TMU pattern**: Texture lookup tables for transcendentals (Box-Muller, stencil access).
   The `TmuLookupTables` builder is reusable for any 4096-entry f32 lookup.
4. **ROP accumulation**: Fixed-point atomic scatter-add pattern for multi-phase force
   accumulation without inter-phase barriers.
5. **6-format capability parser**: `discovery::capabilities::extract_from_any()` handles
   all known primal JSON response shapes.
6. **Health GPU ops**: 6 health domain shaders now in barraCuda (MM batch, SCFA, beat classify,
   Hill, population PK, diversity). healthSpring can go lean on these.

---

*Generated by barraCuda Sprint 22g*
