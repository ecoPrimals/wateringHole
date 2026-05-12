# ludoSpring V40 — Audit, Composition Evolution & NUCLEUS Deployment Handoff

**Date:** April 11, 2026
**From:** ludoSpring
**To:** primalSpring, barraCuda, toadStool, coralReef, Squirrel, petalTongue, biomeOS, NestGate, rhizoCrypt, loamSpine, sweetGrass
**Status:** CI-green, 733 tests, 100 experiments, 10 documented gaps

---

## Executive Summary

ludoSpring V40 completes a full-stack audit against ecoPrimals ecosystem standards. The three-layer validation chain (Python → Rust → IPC composition → NUCLEUS deployment) is operational with 100 experiments proving 13 HCI/game-science models. This handoff documents composition patterns, evolution paths, and absorption candidates for primal and spring teams.

## What Changed in V40

### CI Remediation (207 → 0 clippy errors)
- **deny.toml**: Migrated from deprecated cargo-deny 0.14 schema to 0.19+; added CC0-1.0 license (hexf-parse transitive); wildcards warn (not deny) for workspace path deps
- **Library clippy (24 errors)**: Refactored `neural.rs` visualization delegation (228-line monolith → 3 focused helpers, all <100 LOC); added `#[expect]` for GPU f64→f32 casts in `gpu.rs`; fixed `map_unwrap_or` in `delegation.rs`; collapsed nested ifs in `capabilities.rs`
- **Test clippy (~183 errors)**: `#[allow(clippy::unwrap_used, clippy::expect_used)]` on 26+ test modules; fixed real code quality issues (redundant clones, `collect()` removal, `hypot()`, `mul_add()`, case-insensitive extension checks)
- **Formatting**: 2 diffs auto-fixed
- **exp054**: Added missing `license.workspace = true`

### Documentation
- **10 primal gaps documented** (GAP-01 through GAP-10): GAP-09 = nest_atomic stubs vs missing proto-nucleate fragment; GAP-10 = game.* provider identity in deployment graph
- **Test counts reconciled**: 733 workspace (605 lib + 102 test targets + 26 forge)
- **load_baseline_f64**: Dead code → 4 unit tests validating the JSON baseline loader
- **Provenance verified**: `4b683e3e` resolves to valid commit; 13 experiments use semantic labels (exp083-v2 style)

## Three-Layer Validation Chain

| Layer | Experiment | What It Proves | Status |
|-------|-----------|----------------|--------|
| 1. Python ↔ Rust | `python_parity.rs` (51 tests) | Every Rust model matches Python baseline within named tolerances | ✓ Green |
| 2. Rust ↔ IPC | exp099 (13 checks) | Direct library calls produce identical results to JSON-RPC over UDS | ✓ Green |
| 3. NUCLEUS composition | exp100 (27 checks) | Niche integrity, health probes, capability discovery, science parity via deployed graph | ✓ Green |

This chain establishes that **peer-reviewed science patterns validated in Python** survive faithfully through **Rust implementation**, **IPC serialization**, and **NUCLEUS primal composition**.

## For barraCuda Team

### Current Usage
ludoSpring consumes barraCuda v0.3.11 (CPU-only default) via re-export module `barcuda_math`:
- **Activations**: sigmoid, relu, gelu, mish, softplus, swish (+ batch variants)
- **RNG**: lcg_step, state_to_f64, uniform_f64_sequence
- **Stats**: dot, l2_norm, mae, mean, percentile, rmse, covariance, pearson_correlation, std_dev, variance
- **GPU**: WgpuDevice + TensorSession exposed but not in product paths (GAP-04)

### Absorption Candidates (Write → Validate → Handoff → Absorb → Lean)
These local WGSL shaders duplicate or extend barraCuda tensor ops:

| Local Shader | barraCuda Target | Status |
|-------------|-----------------|--------|
| `exp030/shaders/sigmoid.wgsl` | `barracuda::activations::sigmoid` GPU path | Ready — validated against CPU |
| `exp030/shaders/relu.wgsl` | `barracuda::activations::relu` GPU path | Ready |
| `exp030/shaders/softmax.wgsl` | `barracuda::nn::softmax` GPU path | Ready |
| `exp030/shaders/dot_product.wgsl` | `barracuda::stats::dot` GPU path | Ready |
| `exp030/shaders/reduce_sum.wgsl` | `barracuda::ops::reduce` GPU path | Ready |
| `exp030/shaders/lcg.wgsl` | `barracuda::rng::lcg_step` GPU path | Ready |
| `exp030/shaders/scale.wgsl` | `barracuda::ops::scale` GPU path | Ready |
| `exp030/shaders/abs.wgsl` | `barracuda::ops::abs` GPU path | Ready |
| `barracuda/shaders/game/validated/perlin_2d.wgsl` | New: `barracuda::procedural::perlin_2d` | Candidate — game-domain specific |
| `barracuda/shaders/game/validated/dda_raycast.wgsl` | New: `barracuda::spatial::dda_raycast` | Candidate — game-domain specific |
| `barracuda/shaders/game/fog_of_war.wgsl` | New: `barracuda::spatial::fog_of_war` | Game-specific, less general |
| `barracuda/shaders/game/tile_lighting.wgsl` | New: `barracuda::spatial::tile_lighting` | Game-specific |
| `barracuda/shaders/game/pathfind_wavefront.wgsl` | New: `barracuda::spatial::pathfind` | Game-specific |

The first 8 are direct tier-A absorption candidates (ludoSpring leans on upstream once absorbed). The remaining 5 are domain-specific and may stay local or become a `barracuda::spatial` module.

### GAP-04: TensorSession
`GpuContext::tensor_session()` returns `TensorSession::with_device` but no product code exercises fused multi-op pipelines. When barraCuda's `TensorSession` API stabilizes, ludoSpring should migrate game GPU ops from individual WGSL dispatch to fused tensor pipelines.

## For toadStool Team

ludoSpring dispatches GPU work via `toadstool::dispatch_submit(shader, entry, workgroup_size, dispatch_size, buffers)`. The `ComputeResult` and `SubstrateCapabilities` types are well-used. Current dispatches:
- fog_of_war, tile_lighting, pathfind_wavefront, perlin_terrain, batch_raycast

**Request:** When toadStool evolves `compute.dispatch.submit` to support buffer format negotiation, ludoSpring's `GpuOp` enum can provide structured buffer schemas instead of ad-hoc JSON storage maps.

## For coralReef Team

`coralreef.rs` has a typed client (`compile_wgsl`, `list_shaders`), validated in exp085. **GAP-01:** The game engine still embeds WGSL source directly instead of routing through coralReef for sovereign compilation. Migration path: replace `GpuOp::wgsl_source()` embedded strings with `coralreef::compile_wgsl()` calls.

## For biomeOS / Neural API Team

### NUCLEUS Composition Pattern
ludoSpring's proto-nucleate declares: biomeOS → BearDog → Songbird → toadStool → coralReef → barraCuda → Squirrel → petalTongue → NestGate

**GAP-10: game.* Provider Identity**
The proto-nucleate names `barraCuda` as the `tensor.*` compute node. But ludoSpring's stable IPC surface is `game.*` (27 capabilities). biomeOS needs to either:
1. Add ludoSpring as a separate graph node (`game` domain, `game.*` capabilities)
2. Or document that ludoSpring is the **deployer** of the graph, not a node within it

### Neural API Domain Registration
`biomeos/mod.rs` registers the `game` domain with capabilities. Health probes (`health.liveness`, `health.readiness`, `capability.list`) are implemented. The `NeuralBridge` is the primary discovery mechanism.

### Capability-Based Routing
All inter-primal calls use `by_capability` routing through NeuralBridge, never by primal identity. This pattern should be the standard for all springs.

## For Provenance Trio (rhizoCrypt, loamSpine, sweetGrass)

**GAP-09: nest_atomic Stubs vs Proto-nucleate**
ludoSpring has typed IPC clients for all three provenance primals:
- `rhizocrypt.rs`: `dag.*` operations (session create, vertex append, query)
- `loamspine.rs`: `session.*` lifecycle (begin, complete, list)
- `sweetgrass.rs`: `braid.*` attestation (mint, verify, revoke)

These are **functional stubs** that degrade gracefully when primals are absent. The proto-nucleate does NOT declare `nest_atomic` as a fragment. Either:
1. Upgrade the proto-nucleate to include nest_atomic (making ludoSpring a full NUCLEUS)
2. Or mark these as aspirational composition targets (Node + Meta only)

## For Squirrel / neuralSpring Team

Squirrel integration is live via `squirrel.rs`: `npc_dialogue`, `narrate_action`, `voice_check`. The `inference.*` capability surface (inference.complete, inference.embed, inference.models) is available through Squirrel discovery. No ludoSpring code changes needed as neuralSpring evolves WGSL shader ML — Squirrel handles provider discovery and fallback.

## For petalTongue Team

Visualization delegation is fully wired (`neural.rs` handlers). The refactored code cleanly separates:
- Render family: render, stream, scene, dashboard
- Management: export, validate, subscribe
- Degradation: structured responses when no peer is discovered

## For primalSpring (Ecosystem)

### Patterns to Absorb
1. **ValidationHarness + BaselineProvenance**: Standardized hotSpring pattern with provenance metadata, named tolerances, and exit codes. Every spring should use this.
2. **Capability extraction from diverse formats**: `capabilities.rs` handles 6 different JSON shapes primals return — this should become a shared utility in primalSpring or barraCuda.
3. **NeuralBridge degradation pattern**: All IPC clients return structured `{ available, data }` results; never panic on missing primals.
4. **Three-layer validation chain**: Python → Rust → IPC → NUCLEUS. Every spring should implement this progression.

### Gaps to Feed Back
All 10 gaps (GAP-01 through GAP-10) are documented in `docs/PRIMAL_GAPS.md` and tracked in `config/capability_registry.toml`.

## Composition Maturity Assessment

| Dimension | Score | Notes |
|-----------|-------|-------|
| Python baselines | 10/10 | All models have provenance, no drift |
| Rust validation | 9/10 | 605 tests, all tolerances named and centralized |
| IPC composition | 8/10 | 5 typed clients, graceful degradation, exp099 parity |
| NUCLEUS deployment | 7/10 | exp100 validates niche+health+science; gaps in nest_atomic and game.* identity |
| GPU evolution | 6/10 | 16 WGSL shaders, TensorSession wired but unused in product paths |
| Ecosystem alignment | 8/10 | ecoBin compliant, SCYBORG licensed, deny.toml clean, CI green |

**Overall: 8/10 — Production-ready for Node + Meta composition; Nest integration aspirational.**

---

**Next Steps:**
1. barraCuda absorbs tier-A shaders (sigmoid, relu, softmax, dot, reduce, lcg, scale, abs)
2. primalSpring resolves GAP-09 (nest_atomic fragment) and GAP-10 (game.* node identity)
3. ludoSpring migrates game GPU ops from embedded WGSL to coralReef-compiled shaders (GAP-01)
4. ludoSpring exercises TensorSession in product paths (GAP-04)
5. biomeOS deployment tooling handles spring-as-graph-deployer vs spring-as-graph-node distinction
