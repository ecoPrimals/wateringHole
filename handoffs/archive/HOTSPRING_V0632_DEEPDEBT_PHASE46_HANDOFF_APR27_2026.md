# SPDX-License-Identifier: AGPL-3.0-or-later

# hotSpring v0.6.32 — Deep Debt Evolution + Phase 46 Composition Handoff

**Spring:** hotSpring (BarraCuda crate)  
**Date:** April 27, 2026  
**From:** hotSpring team  
**For:** primalSpring team, all primal teams, sibling spring teams  
**Phase:** Phase 46 (Composition Template) + Deep Debt Evolution  
**primalSpring:** v0.9.17 (guideStone v1.2.0)  
**Test count:** 993/993 lib tests, 166 binaries, 64/64 validation suites, 128 WGSL shaders  

---

## Summary

hotSpring has completed two major evolution milestones in the same cycle:

1. **Phase 46 Composition Template Absorption** — event-driven QCD computation lane
2. **Deep Debt Evolution** — capability-based discovery, smart refactoring, modern idiomatic Rust

Both are ready for upstream audit. This handoff documents patterns, decisions, and active gaps for primal teams and sibling springs.

---

## 1. Phase 46 — Event-Driven Computation + DAG Memoization

### What hotSpring Built

| Artifact | Purpose |
|----------|---------|
| `tools/hotspring_composition.sh` | Domain-specific composition script with 5 hooks |
| `tools/nucleus_composition_lib.sh` | primalSpring's 41-function NUCLEUS wiring library (copied) |

### Domain Hooks Implemented

1. **`domain_on_tick()`** — Async tick model. QCD simulations converge rather than tick at fixed rate. The hook checks convergence (`delta_plaq < CONVERGENCE_THRESHOLD`) and terminates when physics converges, not when a timer fires. Springs with real-time requirements (ludoSpring, healthSpring) will use different tick semantics.

2. **`domain_on_branch()`** — DAG memoization for parameter sweeps. Each lattice configuration (β, lattice dimensions, algorithm) is a vertex. Branching = different coupling constants. `VERTEX_STACK` and `BRANCH_STACK` track the DAG. Memoized vertices skip recomputation — critical for large parameter scans.

3. **`domain_on_seal()`** — Ledger sealing via loamSpine. Each simulation run produces a sealed spine entry (run ID, coupling constant, lattice dimensions, sweeps, plaquette, delta). Enables reproducibility: can the result be reconstructed from the ledger alone?

4. **`domain_on_braid()`** — Scientific provenance via sweetGrass. Braid metadata includes coupling constant, lattice dimensions, Monte Carlo sweeps, algorithm, convergence tolerance — the minimum a peer reviewer needs to evaluate the result.

5. **`domain_on_dispatch()`** — Compute dispatch through toadStool/barraCuda. Tensor workloads (gauge field initialization, SU(3) matrix operations) dispatched through the composition rather than direct library calls.

### Bare Mode Verification

All library functions gracefully degrade when primals are absent. The composition script runs end-to-end in bare mode with SKIP semantics for IPC-dependent operations. This matches the guideStone bare/NUCLEUS additive pattern.

### Patterns for Sibling Adoption

Springs copying the composition template should:
1. Source `nucleus_composition_lib.sh` from `tools/`
2. Override the 5 `domain_on_*()` hooks with domain logic
3. Set `COMPOSITION_NAME` to their spring name
4. Test bare mode (no primals) — all hooks must gracefully degrade
5. Test NUCLEUS mode (primals running) — IPC calls through the lib functions

---

## 2. Deep Debt Evolution — Capability-Based Discovery

### Problem

hotSpring had hardcoded primal name→domain mappings scattered across `composition.rs` and `primal_bridge.rs`. Named accessors (`toadstool()`, `beardog()`, `coralreef()`) coupled production code to specific primal identities rather than capability domains.

### Solution

**Single source of truth**: `niche::DEPENDENCIES` array (already existed for lifecycle registration) now drives all primal requirement derivation in `composition.rs`:

- `required_domains()` → set of capability domains needed for the composition
- `required_primals()` → derived from `required_domains()` via `dependency_for_domain()`
- `domain_for_dependency()` / `dependency_for_domain()` → bidirectional domain↔dependency lookup

**Production migration**: All 8 call sites across 6 files migrated from named accessors to `by_domain()`:
- `by_domain("compute")` instead of `toadstool()`
- `by_domain("math")` instead of `barracuda()` (self-call for sovereign dispatch)
- `by_domain("crypto")` instead of `beardog()`

**Data-driven aliases**: `PRIMAL_ALIASES` constant in `primal_bridge.rs` replaces a hardcoded `"coralreef"` fallback. New primals aliased to old names are handled by a table lookup, not if-else chains.

**Deprecated but available**: Named accessors carry `#[deprecated(since = "0.6.33", note = "use by_domain(...) instead")]` — they still work, emitting compile warnings. This gives downstream consumers (including test suites) time to migrate.

### Pattern for Upstream Primals

This pattern should propagate to the primalSpring composition library:

```rust
// Derive primal requirements from the spring's declared DEPENDENCIES
pub fn required_domains() -> BTreeSet<&'static str> {
    niche::DEPENDENCIES.iter().map(|d| d.domain).collect()
}

// Route by domain, not by name
pub fn by_domain(&self, domain: &str) -> Option<&PrimalEndpoint> {
    self.discovered.values().find(|ep| ep.domain == domain)
}
```

This eliminates the need for springs to know primal names at compile time — they only need capability domains.

---

## 3. Smart File Refactoring

### `lattice/rhmc.rs` (989 lines → module directory)

| File | Lines | Content |
|------|-------|---------|
| `lattice/rhmc/mod.rs` | 802 | Core RHMC physics: `RhmcParams`, `RhmcDiagnostics`, gauge force, CG solver, molecular dynamics |
| `lattice/rhmc/remez.rs` | 190 | Remez exchange algorithm + Gaussian elimination — pure numerical routines with no physics coupling |

The split boundary is the **Remez exchange algorithm** (rational approximation for the fermion determinant). It's a self-contained numerical routine that can be independently tested and potentially reused by other springs doing rational approximation.

### `nuclear_eos_helpers.rs` (978 lines → module directory)

| File | Lines | Content |
|------|-------|---------|
| `nuclear_eos_helpers/mod.rs` | 824 | Residual metrics, analysis, reporting, parameter management |
| `nuclear_eos_helpers/objectives.rs` | 174 | L1/L2 optimization objectives (`l1_objective_nmp`, `l2_objective_nmp_exp_data`, etc.) |

The split boundary is the **optimization objective functions** — pure functions that take parameters and return scalar loss values. They depend on the helper types but not vice versa.

### Refactoring Guidance for Other Springs

When refactoring large files (>800 lines), prefer splitting along **semantic boundaries** (numerical routines, objective functions, protocol handlers) rather than arbitrary line counts. The extracted module should be independently testable and have a clear, narrow interface with the parent.

---

## 4. Pre-Existing Compile Error Fixes

`nuclear_eos_l2_ref.rs` and `nuclear_eos_l2_hetero.rs` were broken by upstream barraCuda's `DiscoveredDevice` API change:

```rust
// Before: assumed Auto::new() returns Arc<WgpuDevice>
let device = rt.block_on(barracuda::device::Auto::new())
    .expect("GPU device");

// After: Auto::new() returns DiscoveredDevice enum
let discovered = rt.block_on(barracuda::device::Auto::new())
    .expect("GPU device");
let device = discovered
    .wgpu_device()
    .expect("requires local wgpu device, not sovereign IPC")
    .clone();
```

**For barraCuda team**: Consider whether `Auto::new()` should have a convenience method like `.into_wgpu()` that handles the common case and provides a clear error when the device is sovereign IPC rather than local.

---

## 5. EVOLUTION Markers (Active Technical Debt)

hotSpring has 3 active EVOLUTION marker families in Rust source — these are **not stale**, they're blocked on upstream:

| Marker | Files | Blocked On |
|--------|-------|------------|
| `EVOLUTION(B2)` | `dynamical.rs`, `resident_cg.rs`, `hasenbusch.rs`, `resident_cg_brain.rs` | Fused gauge-action + fermion-force pipeline in barraCuda TensorSession |
| `EVOLUTION(B3)` | `gpu_rhmc_selftuning.rs` | Upstream barraCuda RhmcCalibrator unidirectional mode stabilization |
| `EVOLUTION(GPU)` | `hfb_deformed_gpu/mod.rs` | Deformed HFB WGSL shaders for full GPU-resident pipeline |

**For barraCuda team**: B2 and B3 are the highest-impact items. When TensorSession supports fused pipelines, hotSpring's GPU HMC path will eliminate the current host-device round-trip for force computation.

---

## 6. Active PRIMAL_GAPS

### Requiring Upstream Primal Work

| Gap | Primal | Severity | Summary |
|-----|--------|----------|---------|
| GAP-HS-001 | Squirrel | Low | End-to-end validation pending neuralSpring stabilization |
| GAP-HS-005 | Songbird | Medium | Cross-family GPU lease for ionic runtime |
| GAP-HS-006 | BearDog | Medium | TensorSession crypto wire format |
| GAP-HS-027 | barraCuda | Medium | TensorSession adoption for fused GPU pipelines |
| GAP-HS-028 | NestGate | Medium | LIME/ILDG zero-copy I/O for lattice configs |
| GAP-HS-039 | rhizoCrypt | Low | DAG graceful degradation under PG-45 conditions |
| GAP-HS-040 | toadStool | Low | Short timeout sensitivity in composition dispatch |
| GAP-HS-041 | barraCuda | Low | `stats.entropy` endpoint missing from IPC surface |
| GAP-HS-042 | petalTongue | Low | plasmidBin threading for concurrent deployments |

### Cross-Spring Recommendations

| Gap | Primal | Recommendation |
|-----|--------|---------------|
| GAP-HS-029 | toadStool | Fork isolation pattern should be in ecosystem standard |
| GAP-HS-030 | toadStool | Ember functionality should absorb into toadStool long-term |

---

## 7. Composition Patterns for NUCLEUS Deployment via neuralAPI/biomeOS

hotSpring's event-driven computation lane surfaces these composition patterns relevant to deployment:

### Convergence-Based Tick vs Fixed-Rate Tick

Most NUCLEUS examples assume fixed-rate ticks (game loops, sensor polling). Scientific computation converges — the tick rate is determined by the physics, not a timer. The composition template's `domain_on_tick()` should document this as a lane variant.

### DAG Memoization for Parameter Sweeps

Parameter sweeps are a universal scientific pattern. The DAG structure (vertex = configuration, edge = parameter change, memoization = don't recompute visited vertices) should be offered as a composition primitive in `nucleus_composition_lib.sh`, not just a hotSpring domain hook.

### Scientific Provenance via Braids

Peer-review audit metadata in sweetGrass braids is hotSpring-specific today but generalizable. Any spring producing reproducible results needs: input parameters, algorithm version, convergence criteria, output hash. Consider a `braid_science_provenance()` helper in the composition library.

### Ledger-Based Reproducibility

The question "can you reproduce results from the ledger alone?" is the scientific equivalent of guideStone Property 1 (Deterministic Output). loamSpine spine sealing should document this pattern as a reproducibility primitive.

---

## 8. Files Changed

### hotSpring Repository

| File | Change |
|------|--------|
| `barracuda/src/composition.rs` | Capability-based discovery from `niche::DEPENDENCIES` |
| `barracuda/src/primal_bridge.rs` | Deprecated named accessors, `by_domain()`, `PRIMAL_ALIASES` |
| `barracuda/src/lattice/rhmc/mod.rs` | Refactored from `rhmc.rs` (802L) |
| `barracuda/src/lattice/rhmc/remez.rs` | Extracted Remez exchange (190L) |
| `barracuda/src/nuclear_eos_helpers/mod.rs` | Refactored from `nuclear_eos_helpers.rs` (824L) |
| `barracuda/src/nuclear_eos_helpers/objectives.rs` | Extracted L1/L2 objectives (174L) |
| `barracuda/src/bin/nuclear_eos_l2_ref.rs` | DiscoveredDevice API fix |
| `barracuda/src/bin/nuclear_eos_l2_hetero.rs` | DiscoveredDevice API fix |
| `tools/hotspring_composition.sh` | Phase 46 composition script |
| `tools/nucleus_composition_lib.sh` | Copied from primalSpring |
| `CHANGELOG.md` | Deep debt + Phase 46 entries |
| `docs/PRIMAL_GAPS.md` | GAP-HS-002 resolved, GAP-HS-038/043 resolved |

### Ecosystem (infra/wateringHole)

| File | Change |
|------|--------|
| `NUCLEUS_SPRING_ALIGNMENT.md` | Phase 46 section, hotSpring active status, deep debt summary |
| `handoffs/HOTSPRING_V0632_DEEPDEBT_PHASE46_HANDOFF_APR27_2026.md` | This document |

---

## 9. Verification

```
cargo check          # zero errors
cargo test --lib     # 993 tests, 0 failures, 6 ignored
cargo clippy --lib   # zero warnings
```

All changes committed and pushed to `origin/main`. Ready for upstream audit.

---

**License**: AGPL-3.0-or-later
