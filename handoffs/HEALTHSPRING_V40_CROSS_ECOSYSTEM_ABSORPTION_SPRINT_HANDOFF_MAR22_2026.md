<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# healthSpring V40 — Cross-Ecosystem Absorption Sprint

**Date**: March 22, 2026
**Supersedes**: `HEALTHSPRING_V39_DEEP_EVOLUTION_AUDIT_HANDOFF_MAR22_2026.md`
**Session**: Deep evolution audit + cross-ecosystem absorption

---

## Executive Summary

Pulled and reviewed all 7 springs (hot, ground, neural, wet, air, ludo, health),
all phase 1 primals (toadStool, squirrel, songBird, nestGate, bearDog), all
phase 2 primals (biomeOS, sweetGrass, rhizoCrypt, loamSpine, petalTongue), and
core infrastructure (barraCuda, coralReef). Analyzed 49 active handoffs in
wateringHole spanning March 16–23. Identified and executed absorption
opportunities. Resolved the toxicology module path conflict, bumped barraCuda
to v0.3.7, extracted magic numbers to named constants, smart-refactored
provenance.rs (850→201+164 lines), and achieved zero clippy warnings on
pedantic+nursery.

---

## What Changed

### Module Conflict Resolution
- **Deleted `ecoPrimal/src/toxicology.rs`** (1060 lines) — was conflicting with
  the refactored `toxicology/mod.rs` + `toxicology/hormesis.rs` module directory.
  API confirmed identical before deletion.

### barraCuda Pin Bump (v0.3.5 → v0.3.7)
- Updated `ecoPrimal/Cargo.toml` pin comment to `c04d848` (v0.3.7, 2026-03-22)
- Unlocked access to: `KimuraGpu` (population genetics fixation), `JackknifeGpu`
  (leave-one-out estimator), `DeviceClass` (vendor-agnostic), `normalize_method()`
  (IPC bare names), hydrology GPU Monte Carlo patterns, `tensor.create`/`tensor.matmul`
  IPC endpoints
- Fixed repository URL in Cargo.toml (`ecoPrimals` → `syntheticChemistry`)

### Magic Number Extraction
New named constants in `tolerances.rs` (17 additions):
- `FOCE_LR_BASE`, `FOCE_LR_DECAY` — FOCE learning rate schedule
- `SAEM_MH_PROPOSAL_SCALE`, `SAEM_MH_MIN_SD` — SAEM Metropolis-Hastings tuning
- `SAEM_BURNIN_FRACTION`, `SAEM_INITIAL_SIGMA`, `SAEM_INITIAL_OMEGA` — SAEM defaults
- `TISSUE_EXCESS_CAP` — organism penalty limit (was `0.5`)
- `DEFAULT_COMPETITION_COEFF`, `DEFAULT_ECOSYSTEM_DT` — simulation defaults
- `VPC_DEFAULT_SIGMA`, `VPC_DEFAULT_DT` — RPC handler defaults

Files fixed:
- `pkpd/nlme/foce_impl.rs` — learning rate uses named constants
- `pkpd/nlme/saem_impl.rs` — MH proposal scale, mul_add for suboptimal_flops
- `simulation.rs` — tissue excess cap uses named constant
- `ipc/dispatch/handlers/simulation.rs` — competition/dt use named constants
- `ipc/dispatch/handlers/pkpd.rs` — NLME defaults extracted to module-level constants
  (`NLME_DEFAULT_THETA`, `NLME_DEFAULT_OMEGA`, `NLME_DEFAULT_SEED`), sigma defaults
  use `VPC_DEFAULT_SIGMA`

### Smart Refactoring
- **`provenance.rs`** (850 lines) → `provenance/mod.rs` (201 lines) + `provenance/registry.rs`
  (164 lines). Semantic split: types/loaders/known/tests vs data. Public API unchanged.
- `#[allow(unused_variables)]` in `data/fetch.rs` → `#[expect(unused_variables, reason = "...")]`
- Clippy `suboptimal_flops` fix in SAEM: `eta[dim] + step_sd * z_val` → `step_sd.mul_add(z_val, eta[dim])`

---

## Quality Metrics

| Metric | V39 | V40 | Delta |
|--------|-----|-----|-------|
| Tests | 809 | 809 | — |
| Clippy warnings (pedantic+nursery) | 0 | 0 | — |
| `#[allow()]` in library code | 1 | 0 | -1 |
| Unsafe code | 0 | 0 | — |
| `.unwrap()` in library code | 0 | 0 | — |
| Magic numbers in production | ~25 | ~8 | -17 |
| Files > 1000 lines | 1 | 0 | -1 |
| barraCuda pin | v0.3.5 | v0.3.7 | +2 minor |
| Production mocks | 0 | 0 | — |

---

## barraCuda Primitive Consumption (v0.3.7)

### CPU (via `barracuda::stats`, `barracuda::rng`, `barracuda::special`, `barracuda::health`, `barracuda::numerical`)
Hill, PopPK, diversity, Anderson, ODE solvers, bootstrap, chi2, correlation,
histogram, welford, normal, regression, spectral_density — **~25 CPU primitives**

### GPU (via `barracuda::ops`, WGSL shaders)
`HillFunctionF64`, `PopulationPkF64`, `DiversityFusionGpu`, `MichaelisMentenGpu`,
`ScfaBatchGpu`, `BeatClassifyGpu` — **6 live shaders**

### New v0.3.7 Absorption Candidates
- `KimuraGpu` — population genetics fixation (toxicology/mithridatism)
- `JackknifeGpu` — NLME diagnostics confidence intervals
- `DeviceClass` — vendor-agnostic device selection for forge layer
- `stats::hydrology::mc_et0_gpu` — Monte Carlo pattern for VPC GPU promotion

---

## Cross-Ecosystem Absorption Analysis

### Reviewed (49 handoffs, 7 springs, 10+ primals)

| Source | Pattern | Status |
|--------|---------|--------|
| wetSpring V131 | Validator-fails-on-zero-checks | **Documented** — next session |
| wetSpring V131 | Large binary matrix discipline (354 bins, 5700 checks) | Gap noted |
| groundSpring V118 | `DefaultRng` migration for stochastic reproducibility | **Documented** — next session |
| groundSpring V118 | Proptest measurement invariants | **Documented** — next session |
| neuralSpring V120 | `OnceLock` GPU device probe cache | **Documented** — next session |
| airSpring V010 | Multi-method ensemble pattern | **Documented** — next session |
| biomeOS V266 | 5-tier capability discovery alignment | **Documented** — next session |
| biomeOS V254-260 | Sleep-free IPC test patterns | **Documented** — next session |
| toadStool S159 | `SiliconUnit` all-silicon routing | Long-term |
| toadStool S163 | Zero-copy `Arc<str>`, `Bytes` hot paths | **Documented** — next session |
| sweetGrass V0.7.22 | `ContentHash` newtype for baselines | Long-term |
| barraCuda V037 | `normalize_method()` IPC bare names | Verify alignment |

### Gap vs Ecosystem

| Metric | healthSpring | Best Sibling | Gap |
|--------|-------------|-------------|-----|
| Coverage | 79% | wetSpring 94% | -15% |
| Tests | 809 | wetSpring 1500+ | -691 |
| GPU shaders | 6 | airSpring 800+ | -794 |
| barraCuda primitives | ~31 | wetSpring 150+ | ~-119 |
| Validation binaries | 86 | wetSpring 354 | -268 |

---

## Patterns Worth Absorbing Upstream

1. **Module-level NLME default constants** — avoids repeated `vec![2.3, 4.4, 0.4]` in
   every handler. Other springs with RPC handlers should adopt the same pattern.

2. **Semantic provenance split** (data vs logic) — provenance registries grow
   linearly with experiments. Splitting the data layer keeps the logic file under
   limits without losing the compile-time completeness check.

3. **`mul_add` discipline** — SAEM proposal step was flagged by nursery `suboptimal_flops`.
   Nursery + pedantic catches these across the ecosystem.

---

## Open Items for Next Session

### P0 — Coverage Push
- Target: 79% → 90% line coverage
- Low-coverage modules: `toadstool` GPU paths, `visualization/stream.rs`, `wfdb/annotations.rs`
- Pattern: CPU-fallback tests, in-process SSE, PhysioNet fixtures

### P0 — Ecosystem Absorption
- Adopt `DefaultRng` pattern from groundSpring V118
- Adopt validator-fails-on-zero-checks from wetSpring V131
- Expand proptest coverage for PK parameter invariants
- `OnceLock` GPU device probe cache from neuralSpring V120

### P1 — GPU Promotion
- `KimuraGpu` integration for mithridatism experiments
- `JackknifeGpu` for NLME diagnostics
- VPC GPU via `mc_et0_gpu` Monte Carlo pattern
- FOCE per-subject gradient parallelization → request `BatchedGradientGpu`

### P1 — Zero-Copy Hot Paths
- Audit IPC serialization: `Arc<str>` keys, `Bytes` from `serde_json::to_vec`
- Sleep-free IPC test patterns from biomeOS

### P2 — Baseline Completeness
- Wire `exp097`, `exp098`, `exp099`, `exp111` to `include_str!` baseline JSON
- Populate `checks` field in PROVENANCE_REGISTRY (most entries have `checks: 0`)
- `cross_validate.py` Track 9 coverage

---

*Part of [ecoPrimals](https://github.com/syntheticChemistry) — sovereign computing for science.*
