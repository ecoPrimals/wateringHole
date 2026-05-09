# hotSpring v0.6.32 — Downstream Patterns & Absorption Handoff

**Date:** May 8, 2026
**From:** hotSpring team
**To:** projectNUCLEUS, foundation, sibling springs, product teams

---

## What hotSpring Exports

### Validation Binaries (for plasmidBin / toadStool workloads)

| Binary | Domain | Checks | Status |
|--------|--------|--------|--------|
| `validate_md` | Yukawa OCP MD | 9/9 | GREEN |
| `validate_ttm` | TTM laser-plasma | Pass | GREEN |
| `validate_nuclear_eos` | Nuclear EOS (195 nuclei) | 195/195 | GREEN |
| `validate_stanton_murillo` | Transport coefficients | 13/13 | GREEN |
| `validate_screened_coulomb` | Murillo-Weisheit | 23/23 | GREEN |
| `validate_pure_gauge` | SU(3) pure gauge | 16/16 | GREEN |
| `validate_production_qcd` | Production β-scan | 10/10 | GREEN |
| `validate_dynamical_qcd` | Dynamical fermions | 7/7 | GREEN |
| `validate_spectral` | Anderson/Aubry-André | 10/10 | GREEN |
| `validate_lanczos` | Lanczos eigensolve | 11/11 | GREEN |
| `validate_all` | Umbrella (64 suites) | 64/64 | GREEN |
| `hotspring_guidestone` | Level 5 guideStone | 30/30 bare | GREEN |

**Note for projectNUCLEUS:** The workload TOML at
`workloads/hotspring/hotspring-md-validation.toml` references
`validate_sarkas_md` — this binary does not exist. Update to
`validate_md` or create a wrapper.

### Deploy Graphs (5 TOML compositions)

| Graph | Atomics | Purpose |
|-------|---------|---------|
| `hotspring_qcd_deploy.toml` | Tower + Node + Nest | Lattice QCD |
| `hotspring_plasma_md_deploy.toml` | Tower + Node | Plasma MD |
| `hotspring_nuclear_eos_deploy.toml` | Tower + Node + Nest | Nuclear EOS |
| `hotspring_spectral_deploy.toml` | Tower + barraCuda | Spectral theory |
| `hotspring_sovereign_gpu_deploy.toml` | Full NUCLEUS + coralReef | Sovereign GPU |

### GPU Shaders (128 WGSL, AGPL-3.0-only)

- f64 SEMF batch, chi2 batch, pure GPU SEMF
- Dielectric (standard + completed Mermin), multi-component
- BGK relaxation, Euler HLL, coupled kinetic-fluid
- SpMV CSR f64 (spectral), Lanczos
- QCD: plaquette, HMC force, CG solver, Dirac, gradient flow
- Cross-spring compatible via toadStool dispatch

---

## Patterns for Sibling Springs to Absorb

### 1. Three-Tier Validation Arc

```
Python baseline (peer-reviewed physics)
  → Rust CPU reproduction (same tolerances)
    → NUCLEUS IPC validation (additive parity)
```

Each tier uses `ValidationHarness` with:
- `check_upper/check_lower/check_bool` for tolerance-gated assertions
- Exit code 0 = pass, 1 = fail, 2 = all skipped (CI-friendly)
- `TelemetryWriter` for NDJSON structured output

### 2. Capability-Based Primal Discovery

```rust
// niche.rs declares what this spring needs
pub const DEPENDENCIES: &[PrimalDependency] = &[
    PrimalDependency { name: "beardog", capability_domain: "crypto", required: true },
    PrimalDependency { name: "toadstool", capability_domain: "compute", optional: true },
    // ...
];

// composition.rs derives required primals from DEPENDENCIES
pub fn required_primals() -> Vec<&'static str> {
    DEPENDENCIES.iter().filter(|d| d.required).map(|d| d.name).collect()
}

// primal_bridge.rs discovers via socket scan + capability.list
let ctx = NucleusContext::detect();
let compute = ctx.by_domain("compute"); // finds toadStool by capability, not name
```

### 3. Deploy Graph Contract

```toml
[graph]
name = "myspring_domain_deploy"
version = "1.0.0"
coordination = "sequential"
bonding_policy = "btsp_required"

[[graph.nodes]]
name = "tower"
atomic = "tower_atomic"
capabilities = ["health.liveness", "discovery.register"]
```

### 4. guideStone Level 5 Certification

`hotspring_guidestone` validates:
- Property 1: SPDX license headers
- Property 2: deny.toml (dependency bans)
- Property 3: BLAKE3 checksums
- Property 4: NUCLEUS IPC parity (additive over bare)
- Property 5: primal proof (full composition)

---

## For foundation Team

### Thread 2 (Plasma Physics / Lattice QCD)

hotSpring is the primary spring for Thread 2. Current data anchors in
`data/sources/thread02_plasma.toml` reference hotSpring validation targets.

**Missing:** Thread 2 expression document (placeholder `expression = ""` in
`THREAD_INDEX.toml`). hotSpring should contribute plasma/QCD expression
material parallel to WCM's `ABG_WHOLE_CELL_REBUILD.md`.

### Validation Pipeline Integration

When foundation adds hotSpring workloads to `workloads/`:
- Use `validate_all` for umbrella validation
- Use `validate_nuclear_eos` for Thread 2 nuclear physics anchor
- Register BLAKE3 hashes via NestGate for `validation/run-*` traceability

---

## For projectNUCLEUS Team

### Workload Updates Needed

1. Fix `hotspring-md-validation.toml` binary path: `validate_sarkas_md` →
   `validate_md`
2. Add workload TOMLs for: `nuclear_eos`, `lattice_qcd`, `spectral`
3. Update Live Science API: hotSpring currently shows `checks_passing: 0`

### Gate Manifest

hotSpring validates on `nest+node` atomic (ironGate config). Composition
proven with all 10 primals via `validate_nucleus_composition`.

---

## Known Gaps (for upstream resolution)

| ID | Gap | Owner |
|----|-----|-------|
| GAP-HS-044 | 13 methods pending in primalSpring canonical registry | primalSpring |
| GAP-HS-046 | atoMEC average-atom charge conservation (2/9 failures) | hotSpring physics |
| GAP-HS-047 | projectNUCLEUS workload binary name mismatch | projectNUCLEUS |
| — | `ai` vs `inference` domain naming for squirrel | squirrel / primalSpring |
| — | `capabilities.list` vs `capability.list` method name | primalSpring Wire Standard |
