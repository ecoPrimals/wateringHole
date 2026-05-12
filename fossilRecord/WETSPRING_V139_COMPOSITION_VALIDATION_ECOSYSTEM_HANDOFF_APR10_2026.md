# WETSPRING V139 — Composition Validation Ecosystem Handoff

| Field | Value |
|-------|-------|
| Date | 2026-04-10 |
| From | wetSpring V139 |
| To | barraCuda, toadStool, primalSpring, biomeOS, all spring teams |
| License | AGPL-3.0-or-later |
| Supersedes | WETSPRING_V138_PRIMAL_COMPOSITION_PATTERNS_HANDOFF_APR07_2026 |

## Evolution Summary

wetSpring has completed the third validation tier:

```
Tier 1: Python → Rust       (58 baselines, 1,580 tests, 356 binaries)
Tier 2: Rust → GPU           (44 GPU modules, full lean on barraCuda)
Tier 3: Rust+Python → NUCLEUS (97/97 proto-nucleate alignment, Exp400)
```

The spring is now **harvest-ready** for plasmidBin at v0.8.0.

## For barraCuda Team

### What wetSpring Consumes

- **150+ primitives** across stats, linalg, ops, dispatch, nn, spectral, nautilus
- **0 local WGSL** — full lean achieved, all ODE shaders via `generate_shader()`
- **TensorSession** for fused multi-op GPU pipelines (PCoA, Kriging, Anderson)
- **Version pinned:** v0.3.7 in `reproduction_manifest.toml`

### Upstream Bug: Feature Gate in `tolerances/precision.rs`

`tolerances/precision.rs:138` references `crate::device` without
`#[cfg(feature = "gpu")]` gating. When wetSpring activates `ipc` or
`facade` features (which activate `json` → `serde` in barraCuda), the
upstream crate fails to compile because `device` is gated behind `gpu`.

**Impact:** IPC integration tests and facade binary cannot be compiled
directly. Workaround: `cargo test --workspace --features json` uses
resolver-2 to avoid the problematic feature combination.

**Fix:** Gate `precision.rs:138` behind `#[cfg(feature = "gpu")]` or
make the struct field conditional.

### Absorption Opportunities

wetSpring has proven these patterns that barraCuda could absorb:

| Pattern | Location | Absorption Target |
|---------|----------|-------------------|
| Diversity index battery (Shannon, Simpson, Chao1, Pielou) | `bio/diversity.rs` | `barracuda::stats` |
| Gonzales dose-response (Hill equation) | `bio/gonzales/` | `barracuda::ops::dose_response` |
| PK exponential decay | `bio/gonzales/pk.rs` | `barracuda::ops::exponential_decay` |
| Anderson tissue lattice | `bio/gonzales/tissue.rs` | `barracuda::spectral` |

## For toadStool Team

### Runtime Discovery Patterns

wetSpring discovers toadStool via Neural API `capability.discover` with
domain `"compute"`. The composition health handler (`composition.node_health`)
probes this to verify the Node atomic tier is operational.

### Socket Convention

All IPC uses `$XDG_RUNTIME_DIR/biomeos/` with fallback to
`std::env::temp_dir()`. Socket names follow `{primal}-{family_id}.sock`
or `{primal}-default.sock`.

### NPU Discovery

`niche.rs` provides `discover_npu_device()`:
1. `$WETSPRING_NPU_DEVICE` (explicit override)
2. toadStool IPC `toadstool.device.npu` (runtime)
3. `/dev/akida0` (BrainChip AKD1000 default)

## For primalSpring Team

### Proto-Nucleate Alignment: 11/11 Primals Covered

| Primal | Role | Niche Status | Composition Probe |
|--------|------|-------------|-------------------|
| beardog | security | required | `probe_capability("security")` |
| songbird | discovery | required | `probe_capability("discovery")` |
| rhizocrypt | dag | required | `probe_capability("provenance")` |
| loamspine | commit | required | `probe_capability("ledger")` |
| sweetgrass | provenance | required | `probe_capability("attribution")` |
| nestgate | storage | optional | `probe_capability("storage")` |
| toadstool | compute | optional | `probe_capability("compute")` |
| petaltongue | visualization | optional | via IPC (grammar rendering) |
| squirrel | ai | optional | via `ai.ecology_interpret` |
| barracuda | math | path dep | compile-time (150+ primitives) |
| coralreef | shader | transitive | via barraCuda shader compilation |

### Domain Label Mismatch (Document or Standardize)

Niche dependency labels vs Neural API probe domains differ for the
provenance trio:

| Primal | `NicheDependency.capability` | `probe_capability()` domain |
|--------|------------------------------|----------------------------|
| rhizocrypt | `dag` | `provenance` |
| loamspine | `commit` | `ledger` |
| sweetgrass | `provenance` | `attribution` |

This is a deliberate mapping layer but should be documented in
`CAPABILITY_DOMAIN_REGISTRY.md` or `COMPOSITION_HEALTH_STANDARD.md`.

### Coordination Validator

The proto-nucleate declares a `validate_wetspring_lifescience` node with
binary `primalspring_primal` and capability `coordination.validate_composition`.
Confirm primalSpring implements this external coordination validator.

### Deploy Graph Schema

Three schema variants exist across wetSpring's 7 graphs:

| Schema | Graphs | Notes |
|--------|--------|-------|
| `[[nodes]]` | `wetspring_deploy.toml` | Legacy germination format |
| `[[graph.node]]` | 6 graphs | Canonical primalSpring format |

Propose: retire `[[nodes]]` variant and standardize on `[[graph.node]]`.
`graph_validate.rs` currently validates `[[graph.node]]` only.

## For biomeOS Team

### Neural API Socket Standardization

Composition health probes require `FAMILY_ID` + `XDG_RUNTIME_DIR` to
discover the Neural API socket. When neither is set, all composition
tiers report "unreachable" (not failure — honest degradation).

**Proposal:** biomeOS provide `BIOMEOS_NEURAL_API_SOCKET` as a direct
override environment variable, bypassing the `FAMILY_ID` + path
construction pattern.

### Composition Health Handlers

wetSpring exposes 5 composition health methods via IPC:

| Method | Returns |
|--------|---------|
| `composition.science_health` | `{ healthy, spring, deploy_graph, subsystems, science_domains, bonding_support }` |
| `composition.tower_health` | `{ healthy, atomic: "Tower", components: { beardog, songbird } }` |
| `composition.node_health` | `{ healthy, atomic: "Node", components: { beardog, toadstool } }` |
| `composition.nest_health` | `{ healthy, atomic: "Nest", components: { beardog, nestgate } }` |
| `composition.nucleus_health` | `{ healthy, atomic: "NUCLEUS", tiers: { tower, node, nest, provenance_trio }, components: { 7 primals } }` |

All return `healthy: bool` as the top-level gate. `tiers` in
`nucleus_health` are flat booleans, not nested `{ "healthy": ... }`.

## For All Spring Teams

### Composition Validation Pattern

wetSpring's `validate_composition_nucleus_v1` (Exp400) establishes the
pattern for composition validation binaries:

1. **D01: Health triad** — liveness, readiness, check
2. **D02: Capability surface** — all advertised caps present
3. **D03: Composition health shapes** — JSON schema validation
4. **D04: Deploy graph structure** — TOML validity, node declarations
5. **D05: Proto-nucleate coverage** — all declared primals reachable
6. **D06: Niche self-knowledge** — dependencies, mappings, graph ref

Any spring can replicate this pattern by:
1. Declaring niche dependencies in `niche.rs`
2. Implementing `composition.*_health` handlers
3. Creating a `validate_composition_*` binary that runs D01–D06

### ecoBin Harvest Path

```bash
cargo build --release --features ipc --bin wetspring
cp target/release/wetspring ../../infra/plasmidBin/wetspring/wetspring
cd ../../infra/plasmidBin && ./harvest.sh wetspring --tag v0.8.0
```

### Open Gaps (Unchanged)

See `wetSpring/GAPS.md` — 7 gaps, all owned by external teams:

| # | Gap | Owner |
|---|-----|-------|
| 1 | Ionic contract negotiation | primalSpring Track 4 |
| 2 | Cross-spring data exchange | RootPulse |
| 3 | Public chain anchor | loamSpine |
| 4 | Client WASM renderer | petalTongue |
| 5 | Interactive composition | ludoSpring + esotericWebb |
| 6 | Physics simulations | hotSpring |
| 7 | Radiating attribution | sweetGrass + sunCloud |

---

*wetSpring V139 — Python validates Rust. Rust + Python validate NUCLEUS.
The composition tier is the proof that sovereign springs can coordinate
via capability-based IPC without compile-time coupling.*
