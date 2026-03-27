<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->

# ludoSpring V20 → barraCuda + toadStool Deep Primal Integration Handoff

**Date:** March 16, 2026
**From:** ludoSpring V20 — 75 experiments, 1692 checks, 394 tests + 12 proptest, 74 .rs files, 18,758 lines Rust
**To:** barraCuda team (math primitives, absorption candidates), toadStool team (GPU dispatch, shader absorption)
**Supersedes:** ludoSpring V18 barraCuda/toadStool Niche Absorption (ecoPrimals wateringHole)
**License:** AGPL-3.0-or-later

---

## Executive Summary

- ludoSpring V20 completed deep primal integration: 19 IPC methods aligned to canonical JSON-RPC specs
- New `capability_domains.rs` pattern for structured capability introspection — reusable by barraCuda/toadStool
- Tolerance constants decomposed into 6 domain-specific submodules — template for organized constants
- Typed provenance pipeline (`DehydrationSummary`/`TrioStage`) for robust session completion
- Game engine core deepened: RulesetCert validation, concrete effect application, raycaster bridge
- 11 WGSL shaders + 3 game-specific shaders ready for toadStool absorption (unchanged from V19)
- Perlin noise absorption remains P1 priority for barraCuda (cross-spring: wetSpring, airSpring, neuralSpring, ludoSpring all use it)

---

## Part 1: What ludoSpring Learned (Relevant to barraCuda/toadStool)

### IPC Method Name Alignment

ludoSpring had 19 IPC method names that diverged from canonical primal JSON-RPC specs. V20 fixed all of them. Lesson: **verify method names against the authoritative primal spec**, not inferred conventions.

Common patterns discovered:
- NestGate uses `storage.store`/`storage.retrieve` (not `put`/`get`)
- Squirrel uses `ai.query`/`ai.suggest`/`ai.analyze` (not `chat`/`text_generation`/`inference`)
- rhizoCrypt nests methods: `dag.session.create`, `dag.vertex.append`, `dag.frontier.get`
- sweetGrass separates domains: `provenance.graph`, `attribution.chain`, `braid.create`

**barraCuda action:** Audit any JSON-RPC clients for method name drift.
**toadStool action:** Audit `compute.submit` and any primal dispatch clients.

### Capability Domains Pattern

ludoSpring created `capability_domains.rs` with `Domain` and `Method` structs:

```rust
pub struct Domain { pub prefix: &'static str, pub description: &'static str, pub methods: &'static [Method] }
pub struct Method { pub name: &'static str, pub fqn: &'static str, pub external: bool }
```

The `external` flag tells biomeOS which capabilities require IPC routing. The `capability.list` RPC response now includes operation dependencies and cost estimates from `niche.rs`.

**barraCuda action:** Adopt this pattern for barraCuda's own `capability.list`. The types are small and reusable.
**toadStool action:** The external/local classification helps dispatch planning — external capabilities need IPC; local ones are in-process.

### Tolerance Organization

Grew from 1 file (~290 lines) to 6 focused submodules:

| Submodule | Constants | Domain |
|-----------|-----------|--------|
| `game.rs` | `DEFAULT_SIGHT_RADIUS`, `TRIGGER_DETECTION_RANGE`, `NPC_PROXIMITY_TILES`, etc. | Game engine |
| `interaction.rs` | Fitts, Hick, Steering, Flow, DDA bounds | HCI models |
| `ipc.rs` | `RPC_TIMEOUT_SECS`, `PROBE_TIMEOUT_MS` | Network |
| `metrics.rs` | Tufte ratios, engagement bounds | Metrics |
| `procedural.rs` | Raycaster, noise, chemistry | PCG |
| `validation.rs` | Test tolerances (analytical, noise, UI) | Quality |

All re-exported via `mod.rs` for backward compat. This pattern scales: barraCuda's tolerance constants could follow the same decomposition.

### Typed Provenance Pipeline

The session completion pipeline is now typed with `DehydrationSummary` (merkle_root, frontier, vertex_count) and `TrioStage` (Unavailable → Dehydrated → Committed → Complete). Partial completions are handled gracefully.

**toadStool action:** If toadStool integrates provenance (session tracking for GPU compute jobs), this pipeline is the reference implementation.

---

## Part 2: Absorption Candidates (barraCuda)

### P1: Perlin Noise (cross-spring priority)

`ludospring-barracuda/src/procedural/noise.rs` (~200 lines): Perlin 2D/3D + fBm with octaves, persistence, lacunarity. GPU-ready (Tier A). Used by wetSpring, airSpring, neuralSpring, and ludoSpring. The WGSL shader `perlin_2d.wgsl` validates CPU-GPU parity at < 1e-3.

**12 proptest invariants** protect these:
- `perlin_2d_bounded`: output always in [-1.0, 1.0]
- `perlin_2d_deterministic`: same seed → same output
- `fbm_amplitude_bounded`: output bounded by geometric sum

### P1: Capability Domains Pattern

`capability_domains.rs` (~100 lines): Small, reusable pattern for structured capability introspection. Every primal needs `capability.list` — this provides the structured response format.

### P2: WFC + BSP

`procedural::wfc` (~265 lines): Wave Function Collapse with entropy-driven cell selection. Needs barrier sync for GPU.
`procedural::bsp` (~220 lines): Binary Space Partitioning with deterministic LCG seeding. Recursive → iterative for GPU.

---

## Part 3: Shader Absorption (toadStool)

### Game-Specific Shaders (3)

| Shader | Workgroup | CPU Reference | Tolerance | Notes |
|--------|-----------|---------------|-----------|-------|
| `fog_of_war.wgsl` | 64 | `game::engine::gpu::compute_fov()` | exact | Per-tile visibility |
| `tile_lighting.wgsl` | 64 | `game::engine::gpu::compute_lighting()` | < 1e-4 | 1/d² falloff |
| `pathfind_wavefront.wgsl` | 64 | `game::engine::gpu::compute_pathfind()` | exact | BFS per dispatch |

### Tier A Parity Shaders (11, from exp030)

| Shader | Workgroup | Tolerance |
|--------|-----------|-----------|
| `perlin_2d.wgsl` | 64 | < 1e-3 |
| `engagement_batch.wgsl` | 64 | < 1e-4 |
| `dda_raycast.wgsl` | 64 | < 0.5 |
| `sigmoid.wgsl` | 64 | < 1e-5 |
| `dot_product.wgsl` | 64 | exact |
| `reduce_sum.wgsl` | 64 | < 1e-5 |
| `softmax.wgsl` | 64 | < 1e-5 |
| `lcg.wgsl` | 64 | exact |
| `relu.wgsl` | 64 | exact |
| `scale.wgsl` | 64 | exact |
| `abs.wgsl` | 256 | exact |

Integration surface: `GpuOp` enum in `game/engine/gpu.rs` with `ToadStoolDispatchRequest`/`ToadStoolDispatchResponse` wire types.

---

## Part 4: Game Engine Evolution (V20 Additions)

### RulesetCert Integration

`GameSession` now validates commands against an active ruleset's `available_actions` via `Command::verb()`. This means game planes enforce what actions are legal — a Dialogue plane might allow `talk`, `examine`, `wait` but not `attack`.

### GridMap Bridge

`From<&TileWorld> for GridMap` converts the high-level tile world into the raycaster's boolean grid. Tiles with `blocks_sight()` become solid. This bridges the game state to GPU-promotable raycasting.

### Concrete Effect Application

`apply()` now handles `ItemAcquired` (despawn), `Damaged` (HP decrement), `Interacted` (property set) — the game state actually changes in response to actions.

---

## Part 5: ludoSpring barraCuda Consumption (Current)

| Primitive | Consumer | Purpose |
|-----------|----------|---------|
| `activations::sigmoid` | `interaction::flow::DifficultyCurve` | Challenge-skill mapping |
| `rng::lcg_step` | `procedural::bsp::generate_bsp` | Deterministic BSP |
| `rng::state_to_f64` | `procedural::bsp::generate_bsp` | Float from LCG state |
| `rng::uniform_f64_sequence` | `exp058_conjugant` | Roguelite RNG |
| `stats::dot` | `metrics::engagement::compute_engagement` | Weighted composite |
| `stats::l2_norm` | `metrics::engagement` | Normalization |
| `stats::mean` | `metrics::engagement` | Central tendency |

ludoSpring re-exports these via `ludospring_barracuda::barcuda_math`.

---

## Part 6: What ludoSpring Does NOT Need

- ludoSpring does not need barraCuda to change any API — we consume via re-export
- ludoSpring does not need toadStool changes — we use the `compute.submit` wire format
- Perlin absorption into barraCuda would let us drop our local implementation (P1 when ready)
- No urgency — ludoSpring's local implementations are validated and correct

---

## License

AGPL-3.0-or-later
