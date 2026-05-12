# hotSpring → Upstream Primal Teams Handoff

**Date**: May 9, 2026
**From**: hotSpring v0.6.32 (Interstadial Eukaryotic + Deep Debt Phase 3)
**To**: barraCuda, toadStool, coralReef, bearDog, songBird, nestGate, rhizoCrypt,
       loamSpine, sweetGrass, squirrel, primalSpring
**License**: AGPL-3.0-or-later

---

## Purpose

This handoff summarizes hotSpring's current primal integration state, identifies
gaps requiring upstream action, and documents composition patterns and learnings
relevant to NUCLEUS evolution and biomeOS/neuralAPI deployment.

---

## hotSpring Status: STRONG

- **1002** lib tests, 0 failures
- **148** binaries (validate_*, production, benchmarks, UniBin)
- **Zero**: clippy warnings, bare `#[allow]`, hardcoded paths, TODO/FIXME markers
- **Eukaryotic UniBin** (`hotspring_unibin`): certify / validate / status / version
- **Certification**: L0-L5 via `certification::certify(max_layer)`
- **Validation**: 6 Tier 1 (Rust) scenarios via `ScenarioRegistry`
- **IPC**: consolidated `ipc::` namespace (discovery, composition, glowplug,
  ember, fleet, squirrel, toadstool, signing)

---

## Gaps Requiring Upstream Action

### barraCuda (PRIORITY: pollster version)

- **pollster 0.3→0.4**: barraCuda still depends on pollster 0.3, creating a
  duplicate in hotSpring's lockfile. Bump to 0.4 for tree deduplication.
- **Absorption candidates**: hotSpring has evolved RHMC (rational approximation
  + multi-shift CG + self-tuning calibrator), gradient flow (LSCFRK 2N-storage),
  and measurement infrastructure (autocorrelation, jackknife, ensemble stats)
  that could benefit the upstream crate.

### primalSpring (PRIORITY: method registry)

- **GAP-HS-044**: 13 hotSpring methods not in primalSpring's canonical registry:
  `composition.health`, `compute.df64`, `compute.dispatch.capabilities`,
  `compute.f64`, `physics.fluid`, `physics.hmc_trajectory`,
  `physics.lattice_gauge_update`, `physics.lattice_qcd`,
  `physics.molecular_dynamics`, `physics.nuclear_eos`, `physics.radiation`,
  `physics.thermal`, `physics.wilson_dirac`.
  Action: PR to add these to the canonical method registry.

### nestGate / hotSpring (PRIORITY: IPC gap)

- **No IPC validation for nestGate**: `niche.rs` declares nestGate with
  capability domain "storage", but no non-test code performs IPC against
  `"nestgate"` or `storage.*` methods. `validate_nucleus_nest.rs` exercises
  rhizoCrypt/loamSpine/sweetGrass but not nestGate.
  Action: Add `storage.*` IPC probes to nest validation and certification.

### projectNUCLEUS (PRIORITY: workload fix)

- **GAP-HS-047**: `projectNUCLEUS/workloads/hotspring/hotspring-md-validation.toml`
  references `validate_sarkas_md` but hotSpring ships `validate_md` and
  `sarkas_gpu`. Live Science API shows `checks_passing: 0`.
  Action: Update workload TOML to correct binary name. Add workload TOMLs
  for nuclear_eos, lattice_qcd, spectral domains.

### coralReef (INFO: sovereign pipeline status)

- Sovereign GPU pipeline is COMPLETE. 10/10 HMC shaders compile to native
  SASS on SM35 (Kepler) + SM70 (Volta) + SM120 (Blackwell).
- GV100 sovereign boot still requires approach pivot (WPR not used by closed
  driver, GAP-HS-048). K80 blocked on PGOB GPC gating.
- Ember fleet architecture operational. `fleet_client.rs` now uses
  `std::env::temp_dir()` instead of hardcoded `/tmp`.

---

## Composition Patterns Learned

### 1. IPC Module Organization

hotSpring consolidated all IPC code under `barracuda/src/ipc/mod.rs` as a
re-export layer. This provides a unified `ipc::` namespace while maintaining
backward compatibility with existing module paths:

```
ipc::discovery    → primal_bridge (NucleusContext, PrimalEndpoint)
ipc::composition  → composition (AtomicType, validate_*, health checks)
ipc::glowplug     → glowplug_client (GlowplugClient, SovereignBootResult)
ipc::ember        → fleet_ember (EmberClient, FleetEmberHub)
ipc::fleet        → fleet_client (FleetDiscovery)
ipc::squirrel     → squirrel_client
ipc::toadstool    → toadstool_report
ipc::signing      → receipt_signing
```

**Recommendation**: This re-export pattern could be standardized across springs.

### 2. Certification as Library (not just binary)

hotSpring evolved guideStone from a binary-only tool into a library function
`certification::certify(max_layer) -> ValidationResult`. This allows:
- Other binaries to call certification programmatically
- Composition with UniBin CLI and validation scenarios
- Testing certification logic without spawning processes

### 3. Validation Scenario Registry

`ScenarioMeta` provides provenance tracking for absorbed experiments:
```rust
pub struct ScenarioMeta {
    pub id: &'static str,
    pub track: Track,
    pub tier: Tier,
    pub provenance_crate: &'static str,
    pub provenance_date: &'static str,
    pub description: &'static str,
}
```

Tracks: nuclear-physics, lattice-qcd, spectral-theory, molecular-dynamics,
composition-parity, domain-science. This enables filtering by domain or tier.

### 4. Capability-Based Primal Discovery

`niche.rs` defines `DEPENDENCIES` (capability domain → primal name) and
`ROUTED_CAPABILITIES` (method → provider primal) as the single source of
truth. `composition.rs` derives atomic requirements from `niche::DEPENDENCIES`.
This means hotSpring only has self-knowledge — primal routing is resolved
at runtime via socket discovery (`niche::socket_dirs()`).

### 5. Dual Discovery Stack Issue

hotSpring uses both `NucleusContext` (local discovery) and `CompositionContext`
(primalSpring composition API). These should be aligned or unified. The
certification module uses `CompositionContext::from_live_discovery_with_fallback()`
while most validators use `NucleusContext`. Springs should converge on one.

---

## For Downstream Systems (foundation, projectNUCLEUS)

### Deploy Graph

`graphs/hotspring_qcd_deploy.toml` declares 10 primals with bonding policy
and spawn order for biomeOS. Downstream systems should reference this graph
for composition deployment.

### Workload Integration

hotSpring validates physics across these domains:
- Molecular dynamics (Yukawa OCP, DSF, VACF, transport coefficients)
- Nuclear structure (SEMF, HFB, deformed HFB, 2042 nuclei)
- Lattice QCD (pure gauge, dynamical fermion, gradient flow, RHMC)
- Spectral theory (Anderson, Hofstadter, Lanczos)
- Dielectric response (Drude-Lorentz, Mermin)
- Average-atom (Thomas-Fermi/Kohn-Sham, partial)

Each domain has validation binaries that can be wired as workload TOMLs
for projectNUCLEUS Live Science API.

### neuralAPI Deployment

`niche.rs` provides `resolve_neural_api_socket()` for biomeOS neuralAPI
integration. Registration with biomeOS occurs via `register_with_target()`
using the `neural-api-{family_id}.sock` socket pattern.

---

## Delta Spring Teams

### For spring teams in our river delta:

1. **IPC consolidation pattern**: Create `src/ipc/mod.rs` re-export layer
   to unify IPC client code under one namespace. Keep original modules.

2. **Eukaryotic evolution**: Absorb representative experiments into
   `validation/scenarios/` with `ScenarioMeta` provenance. Create a UniBin
   with `certify`, `validate`, `status`, `version` subcommands via `clap`.

3. **Code hygiene targets**: Zero bare `#[allow]` (add `reason`), zero
   hardcoded paths (use `niche::socket_dirs()` or `temp_dir()`), zero
   TODO/FIXME in active code. `impl Into<String>` for builder APIs.

4. **Smart refactoring**: Extract cohesive subsystems (math, solvers) into
   submodules. Deduplicate config builders with shared helpers. Don't just
   split files — extract by domain cohesion.
