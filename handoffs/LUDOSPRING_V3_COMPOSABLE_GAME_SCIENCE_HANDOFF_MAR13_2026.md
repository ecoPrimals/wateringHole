# ludoSpring V3 — Composable Game Science Handoff

**Date**: 2026-03-13
**Scope**: 54 experiments, 795 validation checks, provenance trio integration, extraction shooter fraud detection, composable primal architecture
**From**: ludoSpring
**To**: toadStool, barraCuda, biomeOS, songbird, petalTongue

## Summary

ludoSpring V3 validates 13 HCI/game science models across 54 experiments with 795
validation checks (zero failures), 138 cargo tests (zero failures), zero `unsafe`,
zero clippy warnings (pedantic+nursery), all files under 1000 LOC. New work since
V2: ingestible ruleset architecture (RPGPT), distributed human computation
(Games@Home), provenance trio as direct Cargo dependencies, extraction shooter with
12 fraud types and zone topology, and composable primal architecture proving
infrastructure primals interact via JSON-RPC 2.0 without chimeric dependencies.

## Part 1 — What Evolved Since V2

### New Experiments (exp045–054)

| Exp | Track | Checks | What it proves |
|-----|-------|--------|---------------|
| 045 | RPGPT | 49 | PF2e, FATE Core, Cairn ingested as loamSpine certs; action economy validated |
| 046 | RPGPT | 33 | Session DAG with branching narrative, rhizoCrypt vertex tracking |
| 047 | RPGPT | 23 | MTG card mint/trade/transform with loamSpine certs + sweetGrass attribution |
| 048 | Games@Home | 36 | Stack resolution ≡ protein folding (same components, different order → different outcomes) |
| 049 | Games@Home | 33 | Game tree ~10^358, birthday bound ~10^179 — every game is novel data |
| 050 | Games@Home | 30 | Tree complexity as measurable design metric; Commander hypothesis validated |
| 051 | Games@Home | 28 | Folding@Home isomorphism: 12 concepts mapped 1:1, 7 cross-domain transfers |
| 052 | Provenance | 37 | rhizoCrypt DAG + loamSpine certs + sweetGrass braids wired into game sessions |
| 053 | Extraction Shooter | 65 | 12 fraud types, zone topology, spatial detection, consumable lifecycle |
| 054 | Composable Viz | 40 | biomeOS graph + songbird discovery + petalTongue viz — zero chimeric deps |

### Quality Gates Met

- `#![forbid(unsafe_code)]` in all crate roots
- `cargo clippy -W clippy::pedantic -W clippy::nursery` — 0 warnings
- `cargo fmt --check` — clean
- `cargo doc --workspace --no-deps` — clean
- All files < 1000 LOC
- Zero TODO/FIXME/HACK in source

## Part 2 — barraCuda Consumption

### Direct Primitive Usage

| barraCuda Primitive | Consumer | Purpose |
|--------------------|---------|---------|
| `activations::sigmoid` | `interaction::flow::DifficultyCurve` | Sigmoid activation for flow curves |
| `stats::dot` | `metrics::engagement::compute_engagement` | Weighted composite engagement score |
| `rng::lcg_step` | `procedural::bsp::generate_bsp` | Deterministic spatial subdivision |
| `rng::state_to_f64` | `procedural::bsp::generate_bsp` | Float conversion from LCG state |

### Module Consumption by Experiments

| Module | Experiments Using It | GPU-Ready |
|--------|---------------------|-----------|
| `game::raycaster` | 001, 024 | Tier A |
| `game::voxel` | 002, 024 | Tier A |
| `game::ruleset` | 045 | CPU only (Tier C) |
| `interaction::input_laws` | 005–007, 015, 019 | Tier A |
| `interaction::goms` | 011, 019 | Tier A |
| `interaction::flow` | 010, 012, 020, 025 | Tier A |
| `interaction::difficulty` | 004, 020, 025 | Tier A |
| `procedural::noise` | 002, 009, 014, 023, 039, 044 | Tier A |
| `procedural::wfc` | 008, 014, 023 | Tier B |
| `procedural::bsp` | 017, 023, 024 | Tier B |
| `procedural::lsystem` | 013 | Tier B |
| `metrics::engagement` | 010, 021, 025 | Tier A |
| `metrics::fun_keys` | 018, 021, 025 | Tier A |
| `metrics::tufte_gaming` | 003, 016, 022 | Tier A |
| `telemetry` | 026–029 | N/A (I/O) |
| `validation::ValidationResult` | All 52 validation experiments | N/A (harness) |
| `visualization` | Dashboard binaries | N/A (IPC) |

## Part 3 — GPU Promotion Readiness

### Tier A — Pure Math, Ready Now

These modules are embarrassingly parallel with no barriers:

| Module | GPU Target | Blocking |
|--------|-----------|----------|
| `procedural::noise` | Perlin/fBm compute shader | Nothing — pure math |
| `game::raycaster` | Per-column DDA (embarrassingly parallel) | Nothing |
| `metrics::engagement` | Batch evaluation | Nothing — dot product |
| `metrics::fun_keys` | Batch classification | Nothing — weighted sum |
| `interaction::flow` | Batch flow evaluation | Nothing — comparisons |
| `interaction::input_laws` | Batch Fitts/Hick/Steering | Nothing — log2 only |
| `interaction::goms` | Batch KLM task time | Nothing — sum of ops |

### Tier B — Needs Adaptation

| Module | GPU Target | Blocking |
|--------|-----------|----------|
| `procedural::wfc` | Parallel constraint propagation | Barrier sync needed |
| `procedural::bsp` | Recursive → iterative conversion | Stack elimination |
| `procedural::lsystem` | Parallel string rewriting | Variable-length output |

### Tier C — CPU Only

| Module | Why |
|--------|-----|
| `game::ruleset` | Complex trait dispatch, string processing, branching — not suitable for GPU |
| `telemetry` | I/O, serialization |
| `visualization` | IPC, JSON marshaling |
| `ipc` | Network, Unix sockets |

### Dead Feature: `gpu`

The `gpu` feature exists in `barracuda/Cargo.toml` but gates no code. Either wire
it to actual WGSL dispatch or remove it. exp030 validates CPU-vs-GPU parity using
`wgpu` directly — the feature flag should gate that path.

## Part 4 — Composable Architecture Lessons

### The Key Insight

Infrastructure primals (biomeOS, songbird, petalTongue) are NOT Cargo dependencies.
They are independent binaries that communicate via JSON-RPC 2.0 over Unix sockets.
Adding them as `[dependencies]` creates chimeric binaries — tight coupling that
contradicts the ecosystem's composable design.

### What Works

- **Data primals** (rhizoCrypt, loamSpine, sweetGrass) ARE direct Cargo dependencies.
  They provide pure data structures (DAGs, certificates, braids) with no runtime
  side effects. This is correct.
- **Protocol types** are defined locally in each consuming primal's code, matching
  the wire format of the infrastructure primal. See `exp054/src/protocol.rs` for
  the pattern: 268 lines of `serde`-compatible structs that precisely match
  petalTongue `DataBinding`, songbird registration/discovery, and biomeOS
  lifecycle/capability messages.
- **Discovery** happens at runtime via songbird. Each primal registers capabilities
  and discovers peers by capability name, not by compile-time dependency.

### What NOT To Do

- Do NOT add `biomeos-graph`, `songbird-types`, or `petal-tongue-core` to
  `[dependencies]`. This creates chimeric binaries.
- Do NOT hard-code socket paths or primal names. Use songbird discovery.
- Do NOT use `tarpc` trait-level coupling between primals. Use JSON-RPC 2.0
  wire format.

## Part 5 — Provenance Trio Integration

### Direct Dependencies (Correct)

```toml
rhizo-crypt-core = { path = "../../phase2/rhizoCrypt/crates/rhizo-crypt-core" }
loam-spine-core = { path = "../../phase1/loamSpine/crates/loam-spine-core" }
sweet-grass-core = { path = "../../phase1/sweetGrass/crates/sweet-grass-core" }
```

### Usage Pattern

- **rhizoCrypt**: `SessionBuilder::new()` → `session.append_vertex()` with
  `EventType::AgentAction`. Every game action (spawn, move, fire, loot, heal,
  extract) becomes a DAG vertex. Content-addressed via BLAKE3.
- **loamSpine**: `mint_certificate()` for items (weapons, ammo, medical, food).
  Each item has a UUID cert. Certs are immutable — transform creates new cert.
- **sweetGrass**: `BraidBuilder::new()` → `.add_contribution()` with DID identity.
  PROV-O attribution links game actions to players.

### Cross-Primal Round-Trip (exp052, 37 checks)

Vertex hex → braid data hash → DID identity preserved across all three primals.
biomeOS topology: 4-node graph (ludoSpring → rhizoCrypt → loamSpine + sweetGrass)
fits in 16.67ms tick at 60 Hz.

## Part 6 — Extraction Shooter as GPU Test Bed

### 12 Fraud Types Across 3 Tiers

| Tier | Fraud Type | Detection Method |
|------|-----------|-----------------|
| Basic | Orphan item | Item in inventory with no LootPickup or Spawn vertex |
| Basic | Duplicate cert | Two items sharing same loamSpine certificate |
| Basic | Speed violation | Distance/time exceeds max speed |
| Basic | Impossible kill | Range exceeds weapon effective range |
| Basic | Unattributed loot | Loot vertex with no corresponding Kill vertex |
| Basic | Headshot anomaly | Headshot rate > statistical threshold |
| Consumable | Phantom round | Fire event for round with no mint cert |
| Consumable | Over-consumption | Medical/food consumed more times than acquired |
| Spatial | Identity spoof | DAG timeline mismatch between claimed and actual zone |
| Spatial | Ghost action | Kill/loot in zone with no prior Spawn/Move vertex |
| Spatial | Through-wall shot | Shooter and target in zones without line-of-sight |
| Spatial | Teleport | Non-adjacent zone transitions with no Move vertices |

### GPU Candidate: Batched Fraud Analysis

The spatial fraud detectors (through-wall, teleport, ghost action) operate on
zone adjacency and line-of-sight matrices. These are graph operations suitable
for GPU parallelization:

- `ZoneTopology` adjacency matrix → GPU sparse matrix
- Per-action zone lookup → GPU texture/buffer lookup
- Batch all actions in a tick for parallel fraud checking
- Result: binary fraud/clean flag per action

This is a natural candidate for barraCuda GPU dispatch once Tier A shaders exist.

## Part 7 — Action Items for toadStool/barraCuda

### Immediate (No Dependencies)

1. **Wire GPU noise into `procedural::noise`**: barraCuda core already has WGSL
   Perlin. ludoSpring's `procedural::noise` should dispatch to GPU when available.
   exp030 validates the parity path.

2. **Implement Tier A WGSL shaders**: raycaster (per-column DDA), engagement
   (batch dot product), flow (batch comparison), input_laws (batch log2),
   goms (batch sum). All are embarrassingly parallel.

3. **Remove or implement `gpu` feature**: Currently gates nothing. Either wire
   it to actual WGSL dispatch or delete it.

4. **Adopt `PRIMAL_NAMESPACE` pattern in ludoSpring**: Replace any hardcoded
   primal names with a constant (barraCuda already did this in v0.3.5).

### Medium-Term (Needs Coordination)

5. **Fraud detection batching**: Port `detection.rs` spatial checkers to WGSL
   compute shaders. Input: action buffer + zone adjacency matrix. Output:
   fraud flag buffer. Natural batch workload.

6. **Dispatch trait for toadStool substrate**: ludoSpring modules should be
   dispatchable to any substrate (CPU, wgpu, coralReef, toadStool) via a
   common trait. The exp031 dispatch routing experiment validates the discovery
   path.

7. **Tier B shader work**: WFC barrier sync, BSP stack elimination, L-system
   variable-length output. These need compute shader patterns from barraCuda core.

### Long-Term (Ecosystem-Level)

8. **Live composable deployment**: biomeOS `DeploymentGraph` with real songbird
   discovery and petalTongue visualization. exp054 validates the protocol —
   the binaries need to exist.

9. **AR card gaming stack**: loamSpine 1:1 mirror for physical cards. Needs
   camera input → card recognition → cert lookup pipeline. ludoSpring provides
   the game science (stack resolution, provenance), barraCuda provides the
   compute (image processing, GPU inference).

## Quality Gates

| Check | Result |
|-------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --pedantic --nursery` | 0 warnings |
| `cargo test --workspace` | 138 tests, 0 failures |
| `cargo doc --workspace --no-deps` | Clean |
| 55 validation binaries | 795 checks, 0 failures |
| `#![forbid(unsafe_code)]` | All crate roots |
| Files > 1000 LOC | None |
| TODO/FIXME/HACK in source | None |

## Files of Interest

- `barracuda/src/game/ruleset.rs` — 420 lines, ingestible ruleset abstraction
- `experiments/exp053_extraction_shooter_provenance/src/detection.rs` — 12 fraud detectors
- `experiments/exp053_extraction_shooter_provenance/src/raid.rs` — zone topology, consumable lifecycle
- `experiments/exp054_composable_raid_visualization/src/protocol.rs` — JSON-RPC wire types for 3 infrastructure primals
- `experiments/exp054_composable_raid_visualization/src/coordination.rs` — biomeOS DeploymentGraph + songbird discovery
- `experiments/exp054_composable_raid_visualization/src/simulation.rs` — 2-player raid with provenance trio
- `specs/RPGPT_ARCHITECTURE_SKETCH.md` — sovereign RPG engine architecture
