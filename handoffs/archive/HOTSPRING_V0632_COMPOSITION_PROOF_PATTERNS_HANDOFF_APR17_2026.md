# hotSpring v0.6.32 — Composition Proof Patterns & Ecosystem Handoff

**From:** hotSpring (BarraCuda / `hotspring_primal`)
**To:** primalSpring, barraCuda, biomeOS, sibling springs, ecosystem maintainers
**Date:** April 17, 2026
**Version:** 0.6.32
**Wire Standard:** L2 (JSON-RPC 2.0, UDS)
**License:** AGPL-3.0-or-later

---

## Purpose

This handoff captures **patterns, lessons, and requests** that emerged as hotSpring completed
its three-tier validation arc (Python → Rust → Primal Composition). It is structured for
consumption by primalSpring auditors and sibling spring teams adopting the same patterns.

---

## 1. Three-Tier Validation Arc — What We Proved

| Tier | Baseline | Target | What "green" means |
|------|----------|--------|---------------------|
| **1** | Published Python / HPC | Rust CPU + GPU | Rust matches Python within named tolerances |
| **2** | Rust standalone | `validate_*` suites | 62/62 suites pass, 985 lib tests, all deterministic |
| **3** | Rust in-process | IPC-routed primal | Same science observable, routed through NUCLEUS composition, matches within composition-tier tolerances |

**Key insight**: Tier 3 does not re-derive Python. It validates that the **deployment topology**
(discovery → trust → compile → dispatch → math → storage) does not corrupt the science that
Tier 2 already proved against Python. The tolerances can therefore be tighter (1e-10 relative
for SEMF, 1e-12 absolute for plaquette) because both sides execute the same Rust code —
the only variable is IPC serialization/routing.

---

## 2. Composition Tolerance Pattern

### Named, centralized, justified

All composition parity tolerances live in `tolerances/physics.rs` with full docstrings:

```rust
pub const COMPOSITION_SEMF_PARITY_REL: f64 = 1e-10;
pub const COMPOSITION_PLAQUETTE_PARITY_ABS: f64 = 1e-12;
```

**Rationale pattern**: "Local Rust vs IPC — both execute identical code paths; the only
difference is JSON serialization round-trip. Tolerance accommodates f64→JSON→f64 fidelity."

**Recommendation for sibling springs**: Follow this pattern. Do not inline `1e-10` in
composition validators — import from `tolerances::*` so audits can grep one file.

---

## 3. Science Parity Probes — The Recipe

Each probe follows a three-step pattern:

1. **Compute locally** — call the same Rust function the server handler calls.
2. **Call via IPC** — `call_by_capability(domain, method, params)` through `NucleusContext`.
3. **Compare** — assert within centralized tolerance; fail loud if outside.

hotSpring implements three probes:

| Probe | Local call | IPC method | Tolerance |
|-------|------------|------------|-----------|
| SEMF binding energy (Pb-208) | `physics::semf_binding_energy(82, 208)` | `physics.nuclear_eos` | `COMPOSITION_SEMF_PARITY_REL` (1e-10 relative) |
| Wilson plaquette (small lattice) | `lattice::wilson::Lattice::hot_start(…).average_plaquette()` | `physics.lattice_qcd` | `COMPOSITION_PLAQUETTE_PARITY_ABS` (1e-12 absolute) |
| HMC trajectory | Same code path as handler | `physics.hmc_trajectory` | Response shape + finite values |

**Sibling spring template**: Pick your domain's most sensitive observable. Compute it locally.
Route through IPC. Compare. Name the tolerance. Document why that tolerance is correct.

---

## 4. Stadial Invariants — What We Learned

### `deny.toml` ecoBin enforcement

Two `deny.toml` files (barracuda + metalForge/forge) enforce:
- C-dependency bans (`ring`, `openssl`, `pkg-config`, `khronos-egl`, `cc` except via wrappers)
- `async-trait` crate ban (stadial invariant)
- License allowlist (AGPL-3.0, MIT, Apache-2.0, BSD, ISC, Zlib, Unicode)

**Lesson**: `blake3` and `cc` need wrapper exceptions because wgpu's dependency tree
pulls them transitively. Document the exception, don't just `skip`.

### `#[expect]` over `#[allow]`

All production binary code (11 files, ~20 sites) migrated. Library code retains `#[allow]`
inside `#[cfg(test)]` blocks — this is the correct convention (test code is not "production").

**Lesson**: Before migrating, verify the lint actually fires. `#[expect]` on a lint that
never triggers is a compile error — it forces you to remove dead suppressions.

### `dyn` dispatch elimination

Two concrete replacements:
- `Box<dyn RegisterMap>` → `GpuRegisterMap` enum (3 variants: GV100, GFX906, Generic)
- `Arc<dyn ValidationSink>` → `ValidationSink` enum (Stdout, Null, Ndjson)

**Retained with justification**: Benchmark harnesses (`bench/compute_backend.rs`,
`bench/md_backend.rs`) keep `dyn` dispatch because benchmark trait objects are load-bearing
for the measurement framework — annotated with `#[expect]` and rationale.

### `unsafe` elimination

`unsafe { std::env::set_var("FAMILY_ID", …) }` replaced with `OnceLock<String>`:

```rust
static FAMILY_ID_OVERRIDE: OnceLock<String> = OnceLock::new();
pub fn set_family_id(id: String) { FAMILY_ID_OVERRIDE.set(id).ok(); }
pub fn family_id() -> String { /* OnceLock → env var → "default" */ }
```

**Lesson**: `std::env::set_var` became `unsafe` in Edition 2024. Any spring still doing
this should migrate to `OnceLock` before the stadial gate.

---

## 5. Downstream Manifest Alignment

hotSpring's entry in `primalSpring/graphs/downstream/downstream_manifest.toml`:

```toml
[[downstream]]
spring_name = "hotspring"
owner = "hotSpring"
domain = "qcd_physics"
particle_profile = "proton_heavy"
fragments = ["tower_atomic", "node_atomic", "nest_atomic"]
depends_on = ["beardog", "songbird", "coralreef", "toadstool", "barracuda", "nestgate"]
validation_capabilities = [
    "physics.lattice_qcd", "physics.hmc_trajectory", "physics.nuclear_eos",
    "physics.molecular_dynamics", "compute.df64", "compute.cg_solver",
    "compute.gradient_flow", "crypto.hash",
]
```

**Lessons for sibling springs**:
- `validation_capabilities` must list the actual methods your server dispatches, not
  aspirational ones. We fixed this from generic `tensor.matmul`/`stats.mean` to real methods.
- `depends_on` must include all primals in your fragment set — we added `nestgate` because
  `nest_atomic` implies it.
- `spring_validate_manifest.toml` capabilities must mirror `niche.rs::LOCAL_CAPABILITIES`.

---

## 6. Deploy Graph Patterns

`graphs/hotspring_qcd_deploy.toml` declares:

- **10 primal nodes** as peers with spawn-order dependencies
- **Metallic bonding** + **InternalNucleus trust** + tiered encryption per atomic boundary
- `by_capability` routing (not `by_identity`) — e.g. coralReef resolved by `shader` capability

**Lesson**: The deploy graph `by_capability` field must match the fragment definitions.
We fixed `shader_compile` → `shader` to align with `tower_atomic` fragment.

---

## 7. biomeOS Registration Pattern

On server startup, `hotspring_primal` calls:

1. `lifecycle.register` — announces version, capabilities, socket path
2. `capability.register` — advertises `LOCAL_CAPABILITIES` (13 methods) + routed coordination set

Standalone mode (`HOTSPRING_NO_NUCLEUS=1`) skips registration gracefully.

**Recommendation**: Every spring binary should call `register_with_target()` after socket
bind. Discovery-empty states should degrade to local execution, not crash.

---

## 8. Absorption-Ready Inventory for barraCuda

| Module | WGSL Shader(s) | Validation | Priority |
|--------|----------------|------------|----------|
| Staggered Dirac | `dirac_staggered_f64.wgsl` | 8/8 checks | Tier 1 |
| CG solver (3 kernels) | `cg_kernels_f64.wgsl` (dot, axpy, xpay) | 9/9 checks | Tier 1 |
| Pseudofermion HMC | `pseudofermion_*.wgsl`, `hmc_leapfrog_f64.wgsl` | 7/7 CPU, 13/13 streaming | Tier 1 |
| ESN reservoir | `esn_reservoir_update.wgsl`, `esn_readout.wgsl` | NPU validated | Tier 1 |
| HFB deformed suite | 5+ WGSL shaders | GPU-validated | Tier 2 |

**TensorSession request (GAP-HS-027)**: Fused multi-op pipeline for lattice workloads
(leapfrog + force + gauge update as single session) — reduces host sync overhead.

---

## 9. Active Gaps Handed Back

| Gap | Primal | Status | Action |
|-----|--------|--------|--------|
| GAP-HS-001 | Squirrel | Wired, pending native inference | Confirm parity when neuralSpring WGSL ML lands |
| GAP-HS-005 | BearDog/Songbird | Blocked upstream | IONIC cross-family GPU lease |
| GAP-HS-006 | barraCuda/BearDog | Blocked upstream | BTSP session crypto Phase 3 |
| GAP-HS-027 | barraCuda | Deferred | TensorSession fused pipeline API |
| GAP-HS-028 | hotSpring | Active | LIME/ILDG zero-copy I/O |
| GAP-HS-029 | coralReef/toadStool | Implemented, needs standardization | Fork-isolation pattern for hardware fault containment |
| GAP-HS-030 | toadStool/coralReef | Deferred | Ember absorption into toadStool |
| GAP-HS-031 | coralReef | Blocked (kernel) | K80 VFIO legacy group EBUSY |

---

## 10. Composition Patterns for NUCLEUS Deployment via neuralAPI

### neuralAPI contract (what biomeOS expects from a spring)

| Method | Purpose |
|--------|---------|
| `lifecycle.register` | Spring comes online with versioned metadata |
| `capability.register` | Advertise `LOCAL_CAPABILITIES` + routed coordination |
| `capability.list` | Introspection for graph composition and CI |
| `health.liveness` | Is the process alive? |
| `health.readiness` | Is the process ready to serve? |

### Routing convention

```
call_by_capability(domain, method, params)
```

Prefer domain-first routing over legacy name-only accessors. `primal_bridge.rs` retains
named helpers (`toadstool()`, `beardog()`) but `by_domain()` is canonical.

### Standalone mode

`HOTSPRING_NO_NUCLEUS=1` — skip registration + IPC; physics stays local. Composition
validators skip-pass rather than false-fail. Exit code 2 = all checks skipped.

---

## Related Handoffs

| Document | Purpose |
|----------|---------|
| `HOTSPRING_V0632_STADIAL_AUDIT_HANDOFF_APR17_2026.md` | deny.toml, `#[expect]`, validate_all expansion, dyn elimination |
| `HOTSPRING_V0632_PRIMAL_ABSORPTION_HANDOFF_APR17_2026.md` | Per-primal team absorption targets, IPC contracts, deployment patterns |
| `springs/hotSpring/docs/PRIMAL_GAPS.md` | Full gap ledger with resolved + active items |
| `springs/hotSpring/whitePaper/baseCamp/nucleus_composition_evolution.md` | Tier-3 briefing |

---

*End of handoff.*
