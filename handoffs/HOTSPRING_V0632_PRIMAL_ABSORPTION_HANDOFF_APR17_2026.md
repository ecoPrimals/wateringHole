# hotSpring v0.6.32 — Primal Absorption & NUCLEUS Composition Handoff

**From:** hotSpring (BarraCuda / `hotspring_primal`)  
**To:** barraCuda, toadStool, coralReef, BearDog / Songbird, provenance trio (rhizoCrypt / loamSpine / sweetGrass), biomeOS, Squirrel / neuralSpring, sibling springs, primalSpring maintainers  
**Date:** April 17, 2026  
**Version:** 0.6.32 (deploy graph `version = "0.6.32"` in `graphs/hotspring_qcd_deploy.toml`)  
**Wire:** JSON-RPC 2.0 over UDS (L2)  
**License:** AGPL-3.0-or-later  

---

## Executive Summary

hotSpring has completed the **third tier** of its validation arc: **Primal Composition** — IPC-routed NUCLEUS primals checked against in-crate Rust baselines, plus **full server dispatch** for every `LOCAL_CAPABILITIES` method (**GAP-HS-026 resolved**, April 17, 2026). This handoff packages **absorption-ready WGSL**, **validated IPC paths**, **ecosystem requests**, and **deployment patterns** for downstream teams.

---

## For barraCuda

### Absorption-ready WGSL (hotSpring → ecosystem)

These shaders are exercised from hotSpring validation / sovereign compile lists and are suitable for barraCuda catalog ingestion. Paths are relative to `springs/hotSpring/barracuda/`.

| Focus | WGSL / bundle | Primary validation surface | Check notes |
|-------|----------------|---------------------------|-------------|
| **Dirac / SpMV lane** | `src/lattice/shaders/dirac_staggered_f64.wgsl` (`WGSL_DIRAC_STAGGERED_F64`) | `validate_gpu_cg`, lattice GPU pipelines | CG suite: cold/hot/6⁴ convergence + residual vs CPU `cg_solve` |
| **CG solver (3 kernels)** | `src/lattice/shaders/cg_kernels_f64.wgsl` — `complex_dot_re`, `axpy`, `xpay` | Same + `ReduceScalarPipeline` | Tied to `WGSL_COMPLEX_DOT_RE_F64`, `WGSL_AXPY_F64`, `WGSL_XPAY_F64` in CG binary |
| **CSR SpMV (spectral)** | `WGSL_SPMV_CSR_F64` (inline / `spectral` module) | `validate_gpu_spmv`, `validate_gpu_lanczos` | Multiple `check_upper` matrix families (see `validate_gpu_spmv.rs`) |
| **Pseudofermion / HMC** | `src/lattice/shaders/pseudofermion_heatbath_f64.wgsl`, `pseudofermion_force_f64.wgsl`, `hmc_leapfrog_f64.wgsl` | GPU HMC / streaming validators, sovereign compile matrix | Part of dynamical / RHMC tooling chain |
| **ESN reservoir** | `src/md/shaders/esn_reservoir_update.wgsl`, `esn_readout.wgsl` | `validate_sovereign_compile`, streaming / mixed pipelines, `esn_baseline_validation` | Cross-substrate benchmarks use GPU path |
| **HFB deformed (5)** | `batched_hfb_density_f64.wgsl`, `batched_hfb_energy_f64.wgsl`, `batched_hfb_hamiltonian_f64.wgsl`, `deformed_density_energy_f64.wgsl`, `deformed_potentials_f64.wgsl` (plus extended family: `deformed_gradient_f64`, `deformed_hamiltonian_f64`, `deformed_wavefunction_f64` in tree) | `validate_sovereign_compile`, `validate_barracuda_hfb`, nuclear EOS validators | Deformed HFB GPU track |

### TensorSession request (GAP-HS-027)

hotSpring still uses **`TensorContext`** paths for lattice GPU work; **`TensorSession`** (fused multi-op pipeline) is **not adopted** yet. Requested evolution: a **stable fused session API** for lattice workloads so a full HMC trajectory slice (leapfrog + force + gauge update + reductions) can dispatch with minimal host sync — see `docs/PRIMAL_GAPS.md` **GAP-HS-027**.

### Pin / toolchain

| Item | Value |
|------|--------|
| **barraCuda git pin** | `b95e9c59` (v0.3.11 per hotSpring `PRIMAL_GAPS` / CHANGELOG reconciliation) |
| **wgpu** | 28-aligned across hotSpring ↔ barraCuda |
| **Forge probe** | `hotspring-forge` (`metalForge/forge`) used for substrate / FP64 strategy hints (see `gpu_hmc` classification comments) |

---

## For toadStool

| Item | Detail |
|------|--------|
| **Validated path** | `validate_compute_dispatch` (`barracuda/src/bin/validate_compute_dispatch.rs`) — Experiment 152 style: composition health → DAG session → **compute dispatch** → standalone blake3 witness |
| **GPU capability detection** | Routed IPC: `validate_nucleus_node.rs` probes `compute.capabilities` on live ToadStool; `compute_dispatch::query_capabilities` uses `compute.dispatch.capabilities` and parses `result.capabilities` array |
| **Request** | **`shader.dispatch`** (or equivalent) for **sovereign pipeline completion** — symmetry with `compute.dispatch.*` so coralReef-compiled WGSL can be invoked on the same completion path production expects |

### `compute.dispatch.capabilities` JSON shape (documented contract)

Request (via capability domain `compute`):

```json
{ "jsonrpc": "2.0", "method": "compute.dispatch.capabilities", "params": {}, "id": 1 }
```

Expected result envelope (hotSpring parsing in `compute_dispatch.rs`):

```json
{
  "result": {
    "capabilities": ["gpu.f64", "gpu.f32"]
  }
}
```

`capabilities` MUST be a JSON array of strings. Empty array ⇒ reachable but no GPU backends registered.

---

## For coralReef

| Item | Detail |
|------|--------|
| **Sovereign round-trip** | `validate_sovereign_roundtrip` (in `validate_all` suite) — WGSL → native ISA → execution path |
| **QCD shader corpus** | **24/24** QCD shaders compile to native GFX ISA (per hotSpring README / sovereign validation wave) |
| **AMD** | Scratch / local memory paths operational on validated AMD hardware (README claims RX 6950 XT class) |
| **Request** | Stable **`shader.compile.wgsl`** JSON-RPC for **production dispatch** — same method name hotSpring already registers as routed (`niche::ROUTED_CAPABILITIES`) |

---

## For BearDog / Songbird (Tower atomic)

| Item | Detail |
|------|--------|
| **Tower validation** | `validate_nucleus_tower` — `crypto.sign_ed25519` round-trip, Songbird discovery capabilities |
| **GAP-HS-005** | **IONIC** cross-**family** GPU lease still **blocked upstream** (`crypto.sign_contract` / propose-accept-seal not complete) — see `docs/PRIMAL_GAPS.md` |
| **Tower Atomic delegation** | `barracuda/deny.toml` bans **ring** / **openssl** / native TLS stacks — crypto C/asm is delegated to BearDog per ecoBin policy |

---

## For provenance trio (rhizoCrypt / loamSpine / sweetGrass)

| Item | Detail |
|------|--------|
| **Nest atomic** | `validate_nucleus_nest` — storage + DAG + ledger + attribution probes |
| **rhizoCrypt** | `dag.create_session` IPC probe (session id in result) — see `validate_nucleus_nest.rs` |
| **NestGate / loamSpine / sweetGrass** | Storage path + `health.liveness` probes as wired in `validate_nucleus_nest.rs` |
| **Witness** | `validate_compute_dispatch` — **blake3** digest → `WireWitnessRef` → serialize / deserialize round-trip (local phase always runs) |
| **GAP-HS-006** | **BTSP** session crypto for multi-process BarraCuda IPC — **blocked upstream** (Phase 3 wire encryption) |

---

## For biomeOS

| Topic | Implementation / artifact |
|-------|---------------------------|
| **Registration** | `register_with_target()` emits **`lifecycle.register`** + **`capability.register`** over JSON-RPC after socket bind (`niche.rs` + server startup) |
| **Deploy graph** | `springs/hotSpring/graphs/hotspring_qcd_deploy.toml` — **Metallic** bonding, **InternalNucleus** trust, **tiered encryption** per atomic boundary |
| **Spring manifest** | `primalSpring/graphs/spring_deploy/spring_deploy_manifest.toml` — **hotSpring is the 6th spring** (`spring_name = "hotspring"`, `spring_binary = "hotspring_primal"`) |
| **Capabilities** | **19** entries in `LOCAL_CAPABILITIES` — **13** physics/compute methods + **6** composition/health/MCP surface (`composition.health`, `health.*`, `capabilities.list`, `mcp.tools.list`, etc.) |

---

## For Squirrel / neuralSpring

| Item | Detail |
|------|--------|
| **Validator** | `validate_squirrel_roundtrip` — `inference.models`, `inference.complete`, `inference.embed` when `inference` domain is alive |
| **Honest skip** | **Exit code `2`** when Squirrel is absent — uses `CompositionResult::exit_code_skip_aware()` |
| **Request** | Confirm **parity** when **native WGSL inference** (neuralSpring) replaces Ollama-style backends — track under **GAP-HS-001** |

---

## For sibling springs (patterns to copy)

| Deliverable | Location / usage |
|-------------|------------------|
| **ValidationSink enum** | `barracuda/src/validation/composition.rs` — concrete sinks, no `Arc<dyn …>` |
| **CompositionResult + OrExit** | same module — NDJSON CI + `.or_exit()` ergonomics |
| **check_skip / check_or_skip** | honest optional-primal semantics |
| **Science parity probe template** | `primalSpring/graphs/downstream/NICHE_STARTER_PATTERNS.md` |
| **deny.toml template** | `barracuda/deny.toml` — ecoBin C-dep bans, **ring/openssl** bans, stadial notes |
| **`#[expect(lint, reason)]`** | Production bins migrated from bare `#[allow]` (see stadial audit handoff) |

---

## NUCLEUS deployment patterns (quick reference)

### neuralAPI expectations (from biomeOS)

- **`lifecycle.register`** — spring binary comes online with versioned metadata.  
- **`capability.register`** — advertise `LOCAL_CAPABILITIES` + routed coordination set.  
- **`capability.list`** — introspection for graph composition and CI.

### Routing

```text
call_by_capability(domain, method, params)
```

Prefer domain-first routing over legacy name-only accessors (`primal_bridge.rs` retains named helpers but capability routing is canonical).

### Standalone mode

- **`HOTSPRING_NO_NUCLEUS=1`** — skip registration + IPC; physics stays local.  
- **Empty discovery** — composition validators **skip-pass** rather than false-fail where designed.

### Typical graph fragments

`tower_atomic` + `node_atomic` + `nest_atomic` + optional **`nucleus`** + **`provenance_trio`** (+ `meta_tier` when Squirrel is enabled) — see `spring_deploy_manifest.toml` hotSpring entry vs local `graphs/hotspring_qcd_deploy.toml`.

### Bonding

**Metallic** + **InternalNucleus** + **tiered encryption** at Tower / Node / Nest boundaries — already expressed in `hotspring_qcd_deploy.toml` `[graph.bonding_policy]`.

---

## Related handoffs / docs

| Doc | Purpose |
|-----|---------|
| `infra/wateringHole/handoffs/HOTSPRING_V0632_STADIAL_AUDIT_HANDOFF_APR17_2026.md` | deny.toml, `#[expect]`, validate_all expansion, ValidationSink dyn elimination |
| `springs/hotSpring/docs/PRIMAL_GAPS.md` | GAP-HS-005,006,027,028 + resolved ledger |
| `springs/hotSpring/whitePaper/baseCamp/nucleus_composition_evolution.md` | Tier-3 briefing (this wave’s technical narrative) |

---

## Suggested receiver actions

| Team | Action |
|------|--------|
| **barraCuda** | TensorSession lattice fusion design (**GAP-HS-027**); keep wgpu-28 alignment on pin `b95e9c59` |
| **toadStool** | `shader.dispatch` sovereignty completion; keep `compute.dispatch.*` JSON stable |
| **coralReef** | Production-grade `shader.compile.wgsl` RPC SLA |
| **BearDog / Songbird** | Unblock IONIC lease spec (**GAP-HS-005**) |
| **Provenance trio** | BTSP Phase 3 for IPC-heavy deployments (**GAP-HS-006**) |
| **biomeOS** | Consume `hotspring_qcd_deploy.toml` + manifest row on deploy |
| **neuralSpring / Squirrel** | Native inference parity vs `validate_squirrel_roundtrip` |

---

*End of handoff.*
