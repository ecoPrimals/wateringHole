# hotSpring v0.6.32 — Primal Evolution & NUCLEUS Deployment Handoff

**Date:** April 10, 2026
**From:** hotSpring (springs/hotSpring)
**To:** barraCuda, toadStool, coralReef, primalSpring, biomeOS teams
**Version:** hotSpring v0.6.32, barraCuda `fbad3c0a`, toadStool S168, coralReef Iter 47
**License:** AGPL-3.0-or-later

---

## Purpose

This handoff documents:

1. What hotSpring learned about primal use patterns during the Python→Rust→NUCLEUS
   composition validation evolution
2. Absorption candidates ready for upstream primals
3. NUCLEUS composition validation patterns for sibling springs
4. neuralAPI / biomeOS deployment patterns discovered
5. Gaps that require upstream primal evolution

---

## Phase Transition: Python→Rust→NUCLEUS

hotSpring has completed a three-layer validation hierarchy:

```
Layer 1: Python baselines validate Rust implementations
Layer 2: Rust implementations validate NUCLEUS IPC compositions
Layer 3: NUCLEUS compositions ready for biomeOS deployment
```

The key insight: the same tolerance-driven, exit-code-gated validation pattern
that proved Rust matches Python now proves IPC-composed primals match direct Rust
execution. Every `validate_nucleus_*` binary can run standalone (skip-passes for CI)
or against live primals (full IPC validation).

---

## For barraCuda Team

### Current Usage

hotSpring imports `barracuda::` in 241 `.rs` files. Primary surfaces:

- `barracuda::device` — GPU discovery, `WgpuDevice`, `GpuDriverProfile`, `Fp64Strategy`
- `barracuda::ops::linalg` — eigensolve, matrix ops, Gauss-Jordan
- `barracuda::ops::md` — CellListGpu, Yukawa forces, Verlet
- `barracuda::spectral` — Anderson, Lanczos, CSR SpMV (fully leaning on upstream)
- `barracuda::special` — Bessel, Fermi-Dirac, Polylog
- `barracuda::numerical` — LSCFRK integrators
- `barracuda::optimize` — Nelder-Mead, grid search
- `barracuda::shaders::precision::ShaderTemplate` — WGSL template merging
- `barracuda::nautilus` — NautilusShell, Brain API

### Absorption Candidates (Updated April 2026)

**Tier 1 — High Priority:**

| Module | Location | Tests | Status |
|--------|----------|-------|--------|
| ESN Reservoir | `md/reservoir/` + 2 WGSL | 16+ | Ready — GPU+NPU validated |
| GPU Polyakov loop | `lattice/shaders/polyakov_loop_f64.wgsl` | 6/6 | Ready — bidirectional with toadStool |
| Naga-safe SU(3) math | `lattice/shaders/su3_math_f64.wgsl` | 13/13 | Ready — composition-safe, 74 LOC |

**Tier 2 — Medium Priority:**

| Module | Location | Tests |
|--------|----------|-------|
| Screened Coulomb | `physics/screened_coulomb.rs` | 23/23 |
| Wilson action | `lattice/wilson.rs` | 12/12 |
| HMC integrator | `lattice/hmc.rs` | validated |
| Abelian Higgs | `lattice/abelian_higgs.rs` | 17/17 |

### Gap: TensorSession (GAP-HS-007)

hotSpring uses `TensorContext` but not `TensorSession` fused multi-op pipelines.
When `TensorSession` stabilizes for lattice workloads, hotSpring's HMC trajectory
(leapfrog + force + gauge update) is a natural first adoption target. This would
reduce GPU dispatch overhead for the multi-step physics pipeline.

### Gap: BTSP Session Crypto (GAP-HS-006)

barraCuda session creation does not yet use BTSP stream encryption. For hotSpring
this only matters in multi-process IPC scenarios (in-process Rust import is fine).
When BTSP Phase 3 lands, hotSpring will wire it for composition validation binaries
that call barraCuda ops through `toadstool.compute.dispatch.submit`.

---

## For toadStool Team

### Current IPC Surface

hotSpring calls toadStool via JSON-RPC at `$XDG_RUNTIME_DIR/biomeos/toadstool-{FAMILY_ID}.sock`:

| Method | Module | Purpose |
|--------|--------|---------|
| `compute.dispatch.capabilities` | `compute_dispatch.rs` | Query available compute substrates |
| `compute.dispatch.submit` | `compute_dispatch.rs` | Submit GPU workloads |
| `compute.dispatch.result` | `compute_dispatch.rs` | Retrieve dispatch results |
| `compute.capability_query` | `toadstool_report.rs` | Performance surface query |
| `compute.shader.register` | `toadstool_report.rs` | Register hotSpring shaders for dispatch |
| `compute.performance_surface.report` | `toadstool_report.rs` | Silicon characterization data |
| `health.liveness` | `primal_bridge.rs` | Composition health check |
| `capability.list` | `primal_bridge.rs` | Capability discovery |

### toadStool S168 Integration

hotSpring is synced to S168 which adds `shader.dispatch` completing the orchestration
layer. The `WgslOptimizer` + `GpuDriverProfile` integration is used for all shader
compilation (hardware-accurate ILP scheduling, loop unrolling, instruction reordering).

### WGSL Shader Inventory for Absorption

128 WGSL shaders total in hotSpring. See `barracuda/ABSORPTION_MANIFEST.md` for
the full absorption status. Key ready-for-absorption shaders:

- `su3_math_f64.wgsl` — naga-safe SU(3) pure math (74 LOC, no ptr I/O)
- `polyakov_loop_f64.wgsl` — GPU-resident temporal Wilson line
- `esn_reservoir_update.wgsl` + `esn_readout.wgsl` — Echo State Network

25 physics-specific shaders (HFB, BCS, SEMF, transport) stay local.
16 sovereign compile shaders (`coral_sovereign/`) stay local.

---

## For coralReef Team

### Current IPC Surface

hotSpring discovers coralReef via `$XDG_RUNTIME_DIR/biomeos/coralreef-{FAMILY_ID}.sock`
or the `coral-glowplug` persistent broker:

| Method | Module | Purpose |
|--------|--------|---------|
| `health.liveness` | `primal_bridge.rs`, `chuna_validate_shader.rs` | Composition health |
| `shader.compile` | `validate_sovereign_compile.rs` | WGSL → native binary |
| `device.list` | `glowplug_client.rs` | GPU device enumeration |
| `device.dispatch` | `glowplug_client.rs` | GPU workload dispatch |
| `device.resurrect` | `glowplug_client.rs` | Fault recovery |
| `daemon.status` | `glowplug_client.rs` | Fleet health |

### Sovereign Compile Status

45/46 standalone shaders compile to SM70/SM86 SASS via coralReef in-process
(`sovereign-dispatch` feature). 1 gap: `deformed_potentials_f64` SSARef
truncation (different code path from Iter 29 fix).

24/24 QCD shaders compile via AMD sovereign compiler to GFX10.3 ISA.

### Ember Fleet Integration

hotSpring's `fleet_client.rs` (612 LOC) + `fleet_ember.rs` (740 LOC) implement
fleet-wide GPU management through ember RPCs: per-device isolation, hot-standby
pool, fault-informed resurrection, flood testing. Pattern: glowplug orchestrates,
ember holds VFIO fds. `EmberClient` covers 40+ RPC methods including
`ember.firmware.inventory`, `ember.firmware.load`, `ember.sovereign.init`.

---

## For primalSpring Team

### Proto-nucleate Status

hotSpring reads `hotspring_qcd_proto_nucleate.toml` and declares:
- **Fragments:** `tower_atomic`, `node_atomic`, `nest_atomic`
- **Particle profile:** `proton_heavy` (Node atomic dominant)
- **Science domain:** `high_performance_compute`
- **12 primals listed**, 11 IPC-wired (Squirrel pending)

### Composition Validation Pattern

hotSpring pioneered composition validation binaries for springs:

```
validate_nucleus_composition — full NUCLEUS (all atomics)
validate_nucleus_tower      — Tower atomic (BearDog + Songbird)
validate_nucleus_node       — Node atomic (ToadStool + barraCuda + coralReef)
validate_nucleus_nest       — Nest atomic (rhizoCrypt + loamSpine + sweetGrass + NestGate)
```

Each binary:
1. Calls `NucleusContext::detect()` to discover primals at `$XDG_RUNTIME_DIR/biomeos/*.sock`
2. Validates atomic composition via `composition::validate_atomic()`
3. Probes specific capabilities on each primal
4. Reports pass/fail via `ValidationHarness` with exit code 0/1
5. Skip-passes in standalone mode (`HOTSPRING_NO_NUCLEUS=1`)

**Recommendation for sibling springs:** Adopt this pattern. Each spring should have
`validate_nucleus_*` binaries that prove its proto-nucleate composition is live and
functional. The `composition.rs` module is spring-specific but the pattern is reusable.

### Gaps Handed Back

See `docs/PRIMAL_GAPS.md` (9 gaps documented):

| ID | Gap | Severity | Status |
|----|-----|----------|--------|
| GAP-HS-001 | Squirrel not wired | Medium | Deferred (no immediate physics need) |
| GAP-HS-002 | by_capability discovery not pure | Low | Partial (named accessors coexist) |
| GAP-HS-003 | MCP tool surface missing | Medium | **Resolved** — `mcp_tools.rs` created |
| GAP-HS-004 | health.readiness | Low | **Resolved** |
| GAP-HS-005 | IONIC-RUNTIME cross-family GPU lease | Medium | Blocked upstream (BearDog) |
| GAP-HS-006 | BTSP-BARRACUDA-WIRE session crypto | Medium | Blocked upstream |
| GAP-HS-007 | TensorSession not adopted | Low | Deferred (awaiting API stability) |
| GAP-HS-008 | Composition validation binaries | Info | **Resolved** |
| GAP-HS-009 | ecoBin / plasmidBin packaging | Medium | **Resolved** |

---

## NUCLEUS Deployment via neuralAPI from biomeOS

### Discovery Pattern

hotSpring is discoverable by biomeOS at `$XDG_RUNTIME_DIR/biomeos/hotspring-physics.sock`
(fallback: `/tmp/biomeos/hotspring-physics.sock`). It serves:

| Endpoint | Purpose |
|----------|---------|
| `health.liveness` | Always responds — spring is alive |
| `health.readiness` | GPU substrates initialized, validation capable |
| `capability.list` | Full capability set (40+ methods) |
| `composition.health` | Overall NUCLEUS composition health |
| `composition.tower_health` | Tower atomic (crypto + discovery) |
| `composition.node_health` | Node atomic (compute + shader) |
| `composition.nest_health` | Nest atomic (provenance + storage) |
| `mcp.tools.list` | 5 MCP tool schemas for AI/LLM integration |

### neuralAPI Integration Path

For biomeOS to deploy hotSpring as a NUCLEUS composition:

1. **Deploy graph:** biomeOS reads the proto-nucleate TOML and spawns primals
   in dependency order (Tower → Node → Nest → hotSpring)
2. **Socket registration:** Each primal advertises at `$XDG_RUNTIME_DIR/biomeos/{name}-{family}.sock`
3. **Health probe:** biomeOS calls `health.liveness` then `health.readiness` on each
4. **Composition validation:** biomeOS can invoke `composition.health` on hotSpring
   to verify the full NUCLEUS composition is wired and functional
5. **Capability routing:** `capability.list` returns all available methods;
   `composition.get_by_capability` resolves which primal handles a given domain

### Squirrel / neuralSpring Path (GAP-HS-001)

When Squirrel is added to hotSpring's composition:
- hotSpring gains `inference.complete`, `inference.embed`, `inference.models`
- Use case: AI-guided HMC parameter tuning (step size, thermostat coupling)
- No hotSpring code changes needed — Squirrel discovers neuralSpring as provider
- neuralSpring's WGSL shader ML evolves independently; hotSpring gets it via IPC

### MCP Tool Surface

`mcp_tools.rs` exposes 5 tools for AI/LLM integration:

| Tool | Purpose |
|------|---------|
| `hotspring.validate_status` | Current validation suite status |
| `hotspring.tolerance_check` | Query tolerance thresholds and justifications |
| `hotspring.gpu_capability_report` | GPU hardware capabilities and substrate info |
| `hotspring.provenance_query` | Trace validation values to Python baselines |
| `hotspring.experiment_list` | List experiments with status and key findings |

---

## ecoBin Compliance

hotSpring's `harvest-ecobin.sh` builds musl-static `hotspring_primal` for
`x86_64-unknown-linux-musl` (and optionally `aarch64-unknown-linux-musl`).
Output: statically linked, zero C dependencies, b3sum checksums, `metadata.toml`
per ecoBin v3.0. Proto-nucleate notes hotSpring binary is "not in plasmidBin"
(springs are not primals) but the harvest script enables opt-in submission
for composition testing.

---

## Cross-Spring Lessons

Patterns discovered that benefit sibling springs:

1. **Tolerance module tree** — centralized `tolerances/` with `mod.rs` + domain files.
   All validation binaries wire to `tolerances::*`. Zero inline magic numbers.
2. **Provenance centralization** — `BaselineProvenance` records trace every hardcoded
   value to its Python origin (script, commit, date, command, environment).
3. **ValidationHarness** — structured pass/fail with `check_upper()`, `check_lower()`,
   `check_rel()`, `print_provenance()`, exit code 0/1.
4. **Module split at 1000 LOC** — `fleet_client.rs` (1373 LOC) split into
   `fleet_client.rs` (612) + `fleet_ember.rs` (740) with re-exports.
5. **`#[expect()]` over `#[allow()]`** — all dead_code allowances now use
   `#[expect(dead_code, reason = "...")]` for documented intent.
6. **EVOLUTION annotations** — structured `// EVOLUTION(B2): ...` comments replace
   generic TODOs, linking to documented evolution milestones.
7. **Standalone mode** — `HOTSPRING_NO_NUCLEUS=1` env var skip-passes all composition
   checks for CI without live primals. Every composition binary supports this.
8. **Niche self-knowledge** — `niche.rs` declares name, version, proto-nucleate,
   capabilities, dependencies, bond type, trust model. Any spring should have this.

---

## Files Created/Modified in This Evolution

| File | Purpose |
|------|---------|
| `barracuda/src/composition.rs` | Atomic health probes, capability routing |
| `barracuda/src/niche.rs` | Spring self-knowledge |
| `barracuda/src/mcp_tools.rs` | MCP tool schemas |
| `barracuda/src/fleet_ember.rs` | EmberClient RPCs (split from fleet_client) |
| `barracuda/src/bin/validate_nucleus_composition.rs` | Full NUCLEUS validation |
| `barracuda/src/bin/validate_nucleus_tower.rs` | Tower atomic validation |
| `barracuda/src/bin/validate_nucleus_node.rs` | Node atomic validation |
| `barracuda/src/bin/validate_nucleus_nest.rs` | Nest atomic validation |
| `scripts/harvest-ecobin.sh` | ecoBin musl-static build + plasmidBin |
| `scripts/ci-coverage-gate.sh` | CI coverage threshold enforcement |
| `docs/PRIMAL_GAPS.md` | Composition gaps (handback protocol) |
