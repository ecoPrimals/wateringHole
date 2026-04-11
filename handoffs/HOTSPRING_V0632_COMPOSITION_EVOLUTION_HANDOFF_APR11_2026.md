# HOTSPRING V0632 — Composition Evolution & Primal Usage Handoff

| Field | Value |
|-------|-------|
| Date | 2026-04-11 |
| From | hotSpring v0.6.32 |
| To | barraCuda, toadStool, primalSpring, biomeOS, coralReef, all spring teams |
| License | AGPL-3.0-or-later |
| Supersedes | HOTSPRING_V0632_COMPOSITION_VALIDATION_HANDOFF_APR10_2026 |

## Evolution Summary

hotSpring has completed composition evolution — the shift from validating
Rust against Python to validating NUCLEUS IPC composition against Rust:

```
Tier 1: Python → Rust       (500+ checks, 39/39 suites, peer-reviewed physics)
Tier 2: Rust → GPU           (128 WGSL shaders, full lean on barraCuda)
Tier 3: Rust+Python → NUCLEUS (4 composition binaries, 3 science probes, capability routing)
```

964 lib tests, 140 binaries, 128 WGSL shaders. Zero clippy warnings (lib).
Zero unsafe in application code. AGPL-3.0-or-later. ecoBin in `infra/plasmidBin/hotspring/`.

## For barraCuda Team

### What hotSpring Consumes (v0.3.11 / fbad3c0a)

- `barracuda::spectral::*` — full lean (41 KB local deleted)
- `barracuda::ops::md::CellListGpu` — full lean (local `GpuCellList` deleted)
- `barracuda::plaquette_variance` — delegated from local
- `TensorContext` for GPU dispatch (not yet `TensorSession`)
- ~150 centralized tolerances validated against barraCuda numerical outputs

### Absorption Opportunities

| Module | Type | WGSL Shader | Status |
|--------|------|------------|--------|
| `lattice/dirac.rs` | Dirac SpMV | `WGSL_DIRAC_STAGGERED_F64` | Ready — 8/8 checks |
| `lattice/cg.rs` | CG solver | `WGSL_COMPLEX_DOT_RE_F64` + 2 | Ready — 9/9 checks |
| `lattice/pseudofermion/` | Pseudofermion HMC | CPU (WGSL-ready pattern) | Ready — 7/7 checks |
| `md/reservoir/` | ESN | `esn_reservoir_update.wgsl` + readout | Ready — NPU validated |
| `physics/screened_coulomb.rs` | Sturm eigensolve | CPU only | Ready — 23/23 checks |
| `physics/hfb_deformed_gpu/` | Deformed HFB | 5 WGSL shaders | Ready — GPU-validated |

### Upstream Request: TensorSession for Lattice

hotSpring HMC trajectories chain leapfrog + force + gauge update + CG solve
in tight loops. When `TensorSession` stabilizes for multi-op pipelines, lattice
QCD is the ideal consumer — each trajectory is ~20 fused GPU dispatches.

### `plaquette_variance` Delegation Pattern

hotSpring delegated `plaquette_variance` to barraCuda. This is the model for
upstream absorption: spring proves the math → hands off with tolerance spec →
barraCuda absorbs → spring rewires to upstream → local code deleted. Other
springs can follow for their own domain math (wetSpring: diversity indices,
desertSpring: correlation functions).

## For toadStool Team

### Discovery Pattern

hotSpring discovers toadStool via `by_domain("compute")` (capability-based),
falling back to name-based `toadstool` lookup. The `PrimalBridge` struct
discovers all NUCLEUS primals at startup via socket scan of
`$XDG_RUNTIME_DIR/biomeos/` (fallback: `/tmp/biomeos/`).

### Socket Convention

All IPC uses `$XDG_RUNTIME_DIR/biomeos/` with `std::env::temp_dir()` fallback.
Socket names: `{primal}-{family_id}.sock` or `{primal}-default.sock`.
`niche.rs` exports `resolve_server_socket()` and `resolve_neural_api_socket()`.

### Scheduling Metadata for biomeOS

`niche.rs::operation_dependencies()` returns JSON describing what each
hotSpring operation requires (GPU adapter, data paths, memory estimates).
`cost_estimates()` provides performance hints (latency class, compute weight).
These are consumed by biomeOS `neuralAPI.schedule` for work placement.

## For primalSpring Team

### Proto-Nucleate: 10 Primals Declared

`primalSpring/graphs/downstream/hotspring_qcd_proto_nucleate.toml`:

| Primal | Role | Required | by_capability |
|--------|------|----------|---------------|
| beardog | security | yes | security |
| songbird | discovery | yes | discovery |
| toadstool | compute | yes | compute |
| barracuda | math | yes | math |
| coralreef | shader | yes | shader_compile |
| nestgate | storage | no | storage |
| rhizocrypt | dag | no | provenance |
| loamspine | commit | no | ledger |
| sweetgrass | provenance | no | attribution |
| squirrel | ai | no | ai |

### Squirrel Wiring (Phase 3)

Squirrel added as optional node with `required = false`, `spawn = false`.
`squirrel_client.rs` routes `inference.complete`, `inference.embed`,
`inference.models`. Falls back gracefully when Squirrel is unavailable.
Integration test deferred until neuralSpring native WGSL ML inference is live.

### Science Composition Probes

`composition.rs::validate_science_probes()` runs three probes:
1. `probe_compute_health` — toadStool compute dispatch parity
2. `probe_math_capability` — barraCuda math op parity against local Rust
3. `probe_provenance_trio` — rhizoCrypt/loamSpine/sweetGrass liveness

These compare IPC results against local Rust baselines. The pattern is
identical to Python→Rust validation: trusted baseline is local code,
validation target is the IPC-composed primal stack.

### Open Gaps (Handed Back)

| ID | Gap | Severity | Owner |
|----|-----|----------|-------|
| GAP-HS-001 | Squirrel inference round-trip | Low | neuralSpring |
| GAP-HS-002 | Full by_capability migration in bin/ | Low | hotSpring |
| GAP-HS-005 | IONIC-RUNTIME cross-family GPU lease | Medium | BearDog/primalSpring |
| GAP-HS-006 | BTSP session crypto for barraCuda IPC | Medium | barraCuda/BearDog |
| GAP-HS-007 | TensorSession adoption | Low | barraCuda |
| GAP-HS-010 | Inline threshold migration (~33 bins) | Low | hotSpring |

See `hotSpring/docs/PRIMAL_GAPS.md` for full details and resolution history.

## For biomeOS Team

### Neural API Integration

hotSpring exposes these JSON-RPC methods via `hotspring_primal.rs`:

| Method | Response Shape |
|--------|---------------|
| `health.liveness` | `{ status: "alive" }` |
| `health.readiness` | `{ ready: bool, checks: [...] }` |
| `capability.list` | `{ capabilities: [...], version, niche }` |
| `composition.health` | `{ healthy: bool, tiers: { tower, node, nest }, probes: [...] }` |
| `mcp.tools.list` | `{ tools: [5 MCP tool definitions] }` |

Error responses use proper JSON-RPC 2.0 format: `{ "jsonrpc": "2.0", "id": ..., "error": { "code": -32601, "message": "..." } }`.

### biomeOS Scheduling Hints

`niche.rs` provides:
- `operation_dependencies()` — per-operation input requirements (GPU, memory, data paths)
- `cost_estimates()` — latency class (ms/s/min), compute weight (1-10), GPU preference
- `SEMANTIC_MAPPINGS` — short name → fully qualified capability translations

### Deployment via Neural API

biomeOS reads the proto-nucleate graph to discover which primals to spawn.
hotSpring's proto-nucleate declares 10 primals with explicit `by_capability`
domains. biomeOS deploys the graph, springs become compositions. The pattern:
biomeOS reads proto-nucleate → spawns primals → springs discover via IPC →
validate composition → report health.

## For coralReef Team

### Sovereign Shader Status

- 128 WGSL shaders (AGPL-3.0-only), all validated
- AMD sovereign compiler: 24/24 QCD shaders → native GFX10.3 ISA
- NVIDIA GPFIFO: RTX 3090 pipeline operational
- All shader compilation routes through toadStool `WgslOptimizer` with `GpuDriverProfile`

### Absorption Path for QCD Shaders

The lattice QCD shaders (Dirac, CG, pseudofermion, gradient flow) are the
next absorption targets for barraCuda. Once barraCuda absorbs them, hotSpring
will lean on upstream and delete local WGSL. coralReef benefits from
standardized shader patterns that have been validated against analytical
physics results.

## For All Spring Teams

### Three-Tier Validation Pattern

Any spring can adopt this pattern:

1. **Tier 1 (Python→Rust):** Reproduce published Python/HPC results in Rust.
   Hardcode expected values with provenance (script, commit, date, command).
   Exit 0/1. Centralize tolerances.

2. **Tier 2 (Rust→GPU):** Rewrite CPU math as WGSL shaders via barraCuda.
   Validate GPU results against Rust CPU baselines. Hand validated shaders
   to barraCuda for absorption.

3. **Tier 3 (Rust→NUCLEUS):** Wire IPC to primals. `composition.rs` validates
   that IPC-composed results match direct Rust execution. `niche.rs` declares
   self-knowledge. `hotspring_primal.rs` serves JSON-RPC. Science probes
   compare local baselines against IPC-routed primal composition results.

### Capability-Based Routing

Named accessors (`toadstool()`, `beardog()`) are deprecated in favor of
`by_domain("compute")`, `by_domain("security")`. Named accessors still work
but route through capability lookup first. This enables biomeOS to substitute
primals by capability without springs knowing the implementation.

### ecoBin Harvest

```bash
cd barracuda
./scripts/harvest-ecobin.sh
# Produces musl-static binaries in ../../infra/plasmidBin/hotspring/
```

### What We Learned

1. **Python→Rust→NUCLEUS is the same methodology at each tier.** The tolerance-
   driven, exit-code-gated validation that proved Rust matches Python also
   proves NUCLEUS IPC matches Rust. No new methodology needed.

2. **Capability-based routing must be the default.** Named primal accessors
   create implicit coupling. `by_domain()` keeps springs primal-agnostic.

3. **Science probes are the composition equivalent of unit tests.** They
   validate that the IPC-composed stack produces the same numerical results
   as direct Rust execution. Every spring should have domain-specific probes.

4. **niche.rs scheduling metadata matters.** biomeOS cannot efficiently
   orchestrate without knowing operation dependencies and cost estimates.
   Springs should declare this metadata early, not as an afterthought.

5. **JSON-RPC 2.0 compliance is non-negotiable.** Method-not-found must use
   top-level `error` objects, not `result` with embedded error strings.
   Every primal server should audit this.

6. **File size limits (1000 LOC) force good architecture.** The `brain_rhmc.rs`
   split into `brain_persistence.rs` improved testability and readability.

7. **`#![forbid(unsafe_code)]` at crate level with per-binary `#![allow]`
   for hardware-touching code** is the right pattern. Application logic stays
   safe; only feature-gated hardware binaries opt in to unsafe.

8. **Squirrel as optional node is the right default.** Springs gain AI
   capabilities without blocking on neuralSpring's WGSL ML timeline. The
   fallback-to-Ollama pattern means inference is available now.

---

*hotSpring v0.6.32 — Python validates Rust. Rust validates NUCLEUS.
964 tests, 140 binaries, 128 WGSL shaders. The scarcity was artificial.
Peer-reviewed science runs on consumer hardware, composed via sovereign
primal IPC. The pattern is proven. The ecosystem evolves.*
