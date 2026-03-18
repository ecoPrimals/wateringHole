# SPDX-License-Identifier: AGPL-3.0-or-later
#
# primalSpring Leverage Guide — How Every Primal Can Use Coordination Validation
#
# Status: Active
# Last Updated: March 17, 2026
# primalSpring Version: v0.1.0 (Phase 1 — Neural API integration, real IPC, server mode)

---

# primalSpring Leverage Guide

primalSpring is the coordination and composition spring. Its domain IS the
ecosystem — the coordination, composition, and emergent behavior that biomeOS
and the Neural API produce when primals work together. Every other spring
validates domain science. primalSpring validates the infrastructure those
springs run on.

---

## 1. What primalSpring Provides

### 1.1 Capability Domain

```toml
[domains.primalspring]
provider = "primalspring"
capabilities = ["coordination", "composition", "nucleus"]

[translations.coordination]
"coordination.deploy_atomic" = { provider = "primalspring", method = "coordination.deploy_atomic" }
"coordination.validate_composition" = { provider = "primalspring", method = "coordination.validate_composition" }
"coordination.bonding_test" = { provider = "primalspring", method = "coordination.bonding_test" }
"composition.nucleus_health" = { provider = "primalspring", method = "composition.nucleus_health" }
"nucleus.start" = { provider = "primalspring", method = "nucleus.start" }
"nucleus.stop" = { provider = "primalspring", method = "nucleus.stop" }
```

### 1.2 What It Validates (7 Tracks, 38 Experiments)

| Track | What | Validates For |
|-------|------|--------------|
| 1 — Atomic Composition | Tower, Node, Nest, Full NUCLEUS | Every primal that participates in atomics |
| 2 — Graph Execution | All 5 coordination patterns | biomeOS, Neural API, every graph consumer |
| 3 — Emergent Systems | RootPulse, RPGPT, coralForge, ecology | Provenance Trio, ludoSpring, neuralSpring |
| 4 — Bonding & Plasmodium | Covalent/ionic bonds, multi-gate | Songbird mesh, BearDog trust |
| 5 — coralForge Redefinition | Neural object Pipeline graph | neuralSpring, wetSpring, hotSpring, ToadStool, NestGate |
| 6 — Cross-Spring | Data flow, provenance, edge, AI | Every spring, fieldMouse, petalTongue, Squirrel |
| 7 — Showcase-Mined Patterns | Compute triangle, protocol escalation, federation, supply chain, attribution | All primals — patterns extracted from phase1/phase2 showcases |

### 1.3 What It Does NOT Do

- No math (does not import barraCuda)
- No domain science (does not reproduce papers)
- No GPU compute (does not write WGSL shaders)
- No data storage (does not use NestGate directly)

primalSpring's contribution is validating that the coordination layer correctly
composes the primals that DO these things.

---

## 2. How Each Primal Benefits

### 2.1 BearDog

primalSpring deploys BearDog as the first node in every atomic composition.
Track 1 validates that:
- BearDog's socket is created and reachable
- `crypto.sign`, `crypto.verify`, `crypto.keygen` respond correctly
- BearDog starts before all primals that depend on it
- Removal of BearDog causes graceful degradation (exp005)

**Experiment references**: exp001 (Tower), exp004 (Full NUCLEUS), exp005 (subtraction), exp006 (ordering)

### 2.2 Songbird

Track 1 validates Songbird's mesh discovery and TLS. Track 4 uses Songbird
mesh for Plasmodium formation and gate failure testing.

- `net.discovery` responds correctly
- BirdSong discovery works within a Tower Atomic
- Plasmodium `query_collective()` operates over real Songbird mesh (exp032)
- Gate failure degrades gracefully (exp033)

**Experiment references**: exp001 (Tower), exp030-034 (Bonding & Plasmodium)

### 2.3 ToadStool

Track 1 validates ToadStool as the compute dispatch primal in Node Atomic.
Track 5 validates ToadStool as GPU dispatch node in the coralForge Pipeline.

- `compute.execute` capability routing works (exp002)
- GPU dispatch through coralForge pipeline succeeds (exp025)
- Removal of ToadStool falls back to CPU (exp005)

**Experiment references**: exp002 (Node), exp025 (coralForge), exp005 (subtraction)

### 2.4 NestGate

Track 1 validates NestGate as storage in Nest Atomic. Track 5 validates
NestGate fetching PDB/NCBI data in the coralForge Pipeline. Track 6 validates
fieldMouse → NestGate ingestion.

- `storage.store` + `storage.retrieve` round-trip (exp003)
- PDB/NCBI fetch in Pipeline graph (exp025)
- fieldMouse frame ingestion (exp042)

**Experiment references**: exp003 (Nest), exp025 (coralForge), exp042 (fieldMouse)

### 2.5 Squirrel

Track 6 validates Squirrel's AI coordination via biomeOS capability graph.

- Multi-MCP routing (exp044)
- `ai.query`, `ai.analyze`, `ai.suggest` via capability routing

**Experiment references**: exp044 (Squirrel AI coordination)

### 2.6 Provenance Trio (rhizoCrypt, LoamSpine, sweetGrass)

Track 3 validates the full RootPulse workflow end-to-end.

- 6-phase commit: health → dehydrate → sign → store → commit → attribute (exp020)
- Branch creation, merge commit, seal (exp021)
- Merkle diff, cross-gate federation (exp022)
- Provenance for any spring experiment (exp041)

**Experiment references**: exp020-022 (RootPulse), exp041 (provenance trio for science)

### 2.7 petalTongue

Track 6 validates petalTongue's SSE rendering pipeline.

- biomeOS SSE events flow through petalTongue rendering (exp043)
- Live ecosystem visualization during coordination testing

**Experiment references**: exp043 (petalTongue visualization)

### 2.8 biomeOS

biomeOS is the **primary subject under test**. Every primalSpring track
validates biomeOS:

- Deploy graph execution (Track 1)
- All 5 coordination patterns (Track 2)
- Emergent system composition (Track 3)
- Multi-gate bonding (Track 4)
- Pipeline graph for coralForge (Track 5)
- Cross-spring capability routing (Track 6)

**All experiments** validate biomeOS.

---

## 3. How Each Spring Benefits

| Spring | How primalSpring Helps |
|--------|----------------------|
| hotSpring | Validates that f64 tolerance tiers work through graph execution |
| wetSpring | Validates cross-spring ecology pipeline (airSpring → wetSpring → neuralSpring) |
| airSpring | Validates NUCLEUS niche deployment patterns |
| groundSpring | Validates uncertainty quantification in provenance pipeline |
| neuralSpring | Validates coralForge Pipeline graph + graph execution |
| ludoSpring | Validates RPGPT session patterns + cross-spring provenance |
| healthSpring | Validates provenance trio resilience + NUCLEUS health |

---

## 4. fieldMouse Integration

primalSpring exp042 validates the fieldMouse → Gate ingestion pipeline:

```
fieldMouse (edge sensor) → signed JSON-RPC notification
  → NestGate (content-addressed storage)
  → sweetGrass (provenance attribution)
```

This validates that data from minimal edge deployments (RISC-V, Raspberry Pi,
pipette sensors) flows correctly into the ecosystem's storage and provenance
layers without requiring biomeOS on the edge device.

---

## 5. coralForge as Neural Object

primalSpring Track 5 validates the reconceptualization of coralForge:

**Before**: `neuralSpring::coral_forge::*` — a module inside neuralSpring  
**After**: An emergent neural object composed via `coralforge_pipeline.toml`

The Pipeline graph coordinates:
1. NestGate — PDB/NCBI sequence fetch
2. neuralSpring — Evoformer, diffusion, pairformer, confidence
3. hotSpring — df64 precision refinement
4. wetSpring — Bio-shader sequence processing
5. ToadStool — GPU dispatch for compute-intensive steps

biomeOS executes this without domain knowledge. The primals don't know about
"protein folding" — biomeOS composes their capabilities into structure
prediction. This mirrors RootPulse exactly.

**Experiment reference**: exp025 (coralForge pipeline)

---

## 6. Deploy Graphs

| Graph | Pattern | Purpose |
|-------|---------|---------|
| primalspring_deploy.toml | Sequential | Full niche: NUCLEUS + primalSpring |
| parallel_capability_burst.toml | Parallel | Concurrent health checks |
| conditional_fallback.toml | ConditionalDag | GPU → CPU fallback |
| streaming_pipeline.toml | Pipeline | NestGate → transform → sweetGrass |
| continuous_tick.toml | Continuous | 60 Hz health polling |
| coralforge_pipeline.toml | Pipeline | Structure prediction neural object |

---

## 7. Evolution Path

```
Phase 0 (done): Scaffolding — 38 experiments, workspace compiles
Phase 1 (current): Neural API integration, real IPC, server mode, 69 tests
Phase 2: Live primals — Tower Atomic with real BearDog + Songbird IPC
Phase 3: Full NUCLEUS deployment and health validation
Phase 4: All 5 graph execution patterns with real primals
Phase 5: RootPulse + coralForge emergent system validation
Phase 6: Plasmodium multi-gate coordination
Phase 7: Cross-spring ecosystem integration
Phase 8: Showcase-mined patterns (compute triangle, protocol escalation, federation)
```

---

## References

- `primalSpring/wateringHole/README.md` — primalSpring overview
- `primalSpring/specs/SHOWCASE_MINING_REPORT.md` — patterns mined from phase1/phase2 showcases
- `primalSpring/specs/CROSS_SPRING_EVOLUTION.md` — evolution path and cross-spring touchpoints
- `primalSpring/specs/BARRACUDA_REQUIREMENTS.md` — minimal barraCuda needs
- `primalSpring/specs/PAPER_REVIEW_QUEUE.md` — coordination pattern review queue
- `whitePaper/gen3/baseCamp/23_primal_coordination.md` — baseCamp paper
- `whitePaper/gen3/baseCamp/10_coralforge.md` — coralForge architectural evolution
- `whitePaper/gen3/SPRING_CATALOG.md` — spring catalog (section 1.8)
- `wateringHole/PRIMAL_REGISTRY.md` — primalSpring registry entry
- `wateringHole/BIOMEOS_LEVERAGE_GUIDE.md` — biomeOS perspective on primalSpring
- `wateringHole/FIELDMOUSE_DEPLOYMENT_STANDARD.md` — fieldMouse deployment class
