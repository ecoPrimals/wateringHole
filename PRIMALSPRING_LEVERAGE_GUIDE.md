# SPDX-License-Identifier: AGPL-3.0-only
#
# primalSpring Leverage Guide — How Every Primal Can Use Coordination Validation
#
# Status: Active
# Last Updated: March 22, 2026
# primalSpring Version: v0.3.0-dev (Phase 3 — capability-first architecture, topological waves, 236 tests)
# biomeOS alignment: v2.67 (5-tier centralized discovery, GeneticLineage→BearDog, niche self-knowledge)

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

### 1.4 IPC Resilience Stack (v0.2.0)

primalSpring provides a converged IPC resilience stack adopted across the ecosystem:

| Component | Purpose |
|-----------|---------|
| **IpcError** | 8 typed variants: `SocketNotFound`, `ConnectionRefused`, `ConnectionReset`, `Timeout`, `ProtocolError`, `MethodNotFound`, `ApplicationError`, `SerializationError`. Query methods: `is_retriable()`, `is_timeout_likely()`, `is_method_not_found()`, `is_connection_error()` |
| **CircuitBreaker** | Fail-fast when a primal is down; `failure_threshold`, `recovery_timeout`, `Closed`/`Open`/`HalfOpen` states |
| **RetryPolicy** | Exponential backoff (`max_retries`, `base_delay`, `max_delay`) |
| **resilient_call()** | Wraps IPC calls with circuit-breaking and retry; retries only on `is_retriable()` errors |

### 1.5 DispatchOutcome\<T\> and Result Extraction

| Component | Purpose |
|-----------|---------|
| **DispatchOutcome\<T\>** | Three-way classification: `Success`, `ProtocolError`, `ApplicationError`. `should_retry()` for retry decisions |
| **extract_rpc_result\<T\>** | Centralized JSON-RPC result extraction — handles errors, missing results, deserialization |
| **extract_rpc_dispatch\<T\>** | Preserves protocol vs application error distinction for `should_retry()` |

### 1.6 4-Format Capability Parsing

`extract_capability_names()` handles all ecosystem wire formats:

- **Format A** — flat string array: `["crypto.sign", "crypto.verify"]`
- **Format B** — object array: `[{"method": "crypto.sign"}]`
- **Format C** — nested `method_info`: `{"method_info": [{"name": "crypto.sign"}]}`
- **Format D** — double-nested `semantic_mappings`: `{"semantic_mappings": {"crypto": {"sign": {}}}}`

### 1.7 Health Probes and Self-Knowledge

| Capability | Purpose |
|------------|---------|
| **health.liveness** | Kubernetes-style liveness — is the primal process alive? |
| **health.readiness** | Kubernetes-style readiness — ready to serve? (Neural API + discovered primals) |
| **PRIMAL_NAME** / **PRIMAL_DOMAIN** | Self-knowledge constants (`primalspring`, `coordination`) |
| **safe_cast module** | `micros_u64`, `u128_to_u64`, `usize_to_u32`, `f64_to_usize` — safe numeric casts for metrics |
| **OrExit\<T\> trait** | Clean fatal exit for validation binaries (`.or_exit(msg)`) |
| **ValidationSink trait** | Pluggable output: `StdoutSink`, `NullSink` for CI/headless runs |

### 1.8 Niche Self-Knowledge (v0.2.0)

| Component | Details |
|-----------|---------|
| **niche.rs** | 21 capabilities, 7 semantic domains, operation dependencies, cost estimates |
| **register_with_target()** | Registers capabilities with biomeOS for BYOB scheduling |
| **capabilities.list RPC** | Returns structured niche: capabilities array, semantic mappings, operation deps, cost estimates |

### 1.9 Deploy Graph Validation + Topological Ordering (v0.3.0)

| Component | Details |
|-----------|---------|
| **deploy.rs** | Parses biomeOS TOML deploy graphs, validates structure, topological ordering, live probing |
| **topological_waves()** | Kahn's algorithm startup wave computation from graph dependency edges |
| **graph_required_capabilities()** | Extracts capability roster from `by_capability` fields |
| **validate_live_by_capability()** | Probes nodes using capability-first discovery |
| **graph.list RPC** | Structurally validates all graphs in the deploy directory |
| **graph.validate RPC** | Validates a specific graph (structural or live probing) |
| **graph.waves RPC** | Returns topological startup wave ordering |
| **graph.capabilities RPC** | Returns required capabilities from a graph |
| **Deploy graphs** | 11 TOMLs, all nodes declare `by_capability` (enforced by test) |

### 1.10 Capability-First Architecture (v0.3.0)

| Component | Details |
|-----------|---------|
| **discover_by_capability()** | Discovers providers by what they offer, not by name |
| **check_capability_health()** | Capability-based health probe helper for experiments |
| **validate_composition_by_capability()** | Validates compositions using capability resolution |
| **IpcErrorPhase** | Phase-aware IPC error context (Connect/Serialize/Send/Receive/Parse) |
| **discover_remote_tools()** | Cross-spring MCP tool discovery via `mcp.tools.list` |

### 1.11 Test and Experiment Evolution

| Metric | v0.1.0 | v0.2.0 | v0.3.0-dev |
|--------|--------|--------|------------|
| Tests | 69 | 157 | **236** (225 unit + 10 integration + 1 doc-test) |
| RPC endpoints | 8 | 11 | **17** |
| Deploy graphs | 6 | 6 | **11** (all `by_capability`) |
| Capability-based experiments | 0 | 0 | **6** (exp001-004, exp006, exp051) |

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
Phase 1 (done): Neural API integration, real IPC, server mode, 69 tests
Phase 2 (current): Ecosystem absorption, niche self-knowledge, deploy graph validation, 157 tests
Phase 2b: Live primals — Tower Atomic with real BearDog + Songbird IPC
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
