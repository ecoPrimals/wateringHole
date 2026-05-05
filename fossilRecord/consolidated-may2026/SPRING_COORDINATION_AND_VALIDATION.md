# Spring Coordination and Validation — Handoffs, Provenance, and Assignments

**Version**: 1.0.0  
**Date**: April 4, 2026  
**Status**: Active  

This document consolidates: `COORDINATION_HANDOFF_STANDARD.md`, `PRIMALSPRING_COMPOSITION_GUIDANCE.md`, `SPRING_PROVENANCE_TRIO_INTEGRATION_PATTERN.md`, `SPRING_VALIDATION_ASSIGNMENTS.md`, `INTER_PRIMAL_INTERACTIONS.md`.

---

## Coordination Handoff

**Companion**: `CAPABILITY_BASED_DISCOVERY_STANDARD.md`.

### Principle

biomeOS develops coordination patterns (NUCLEUS, lifecycle, Neural API, deployment). **primalSpring** validates compositions, graphs, bonding, and cross-spring ecology. Springs cross-learn through primalSpring, not direct coupling.

### Extractable base structures (biomeOS)

**Atomic types** (`biomeos-types/src/atomic.rs`):

```rust
pub enum AtomicTier { Tower, Node, Nest, Full }
pub enum AtomicCapability { SecureIpc, ComputeDispatch, DataStorage, AiInference, ... }
pub enum PrimalHealth { Healthy, Degraded, Unavailable, NotRequired }
pub type ProviderHealthMap = BTreeMap<String, PrimalHealth>;
pub struct TowerAtomic { node_id, providers: ProviderHealthMap, socket_path }
pub struct NodeAtomic { tower: TowerAtomic, compute: PrimalHealth }
pub struct NestAtomic { tower: TowerAtomic, storage: PrimalHealth }
pub struct FullNucleus { node: NodeAtomic, storage, inference: PrimalHealth }
```

`ProviderHealthMap` is keyed by capability id, not primal name.

**Concurrent startup waves** (`biomeos-core/src/concurrent_startup.rs`): `DependencyGraph::build()` from `provides`/`requires` → `topological_waves()` (Kahn) → `start_in_waves()` (concurrent within wave, sequential between).

**Coordination patterns** (`biomeos-graph/src/graph.rs`):

| Pattern | Use |
|---------|-----|
| Sequential | Ordered startup |
| Parallel | Independent nodes |
| ConditionalDag | `condition`, `skip_if` |
| Pipeline | Streaming (bounded mpsc) |
| Continuous | Fixed timestep loops |

**ValidationSink** (`biomeos-types/src/validation.rs`):

```rust
pub trait ValidationSink {
    fn emit(&mut self, finding: ValidationFinding);
    fn error(&mut self, rule, message);
    fn warning(&mut self, rule, message);
    fn info(&mut self, rule, message);
}
```

**PlasmodiumAgent** (`biomeos-atomic-deploy/.../agents/`): `meld`, `split`, `resolve(capability_domain)`.

### Validation matrix (capability-based)

**Tower**: `capability.discover("security"|"discovery")`; `health.check`; beacon chain `beacon.generate` → `beacon.encrypt` → `beacon.try_decrypt`; `network.beacon_exchange`.

**Node**: Tower + `capability.discover("compute")`; `compute.query_capabilities`.

**Nest**: Tower + `capability.discover("storage")`; `storage.store` → `storage.retrieve`.

**Full NUCLEUS**: Tower + Node + Nest + AI + provenance trio (`dag`, `commit`, `provenance`); `FullNucleus::degradation_level()`.

### Deploy graph TOML (BYOB)

```toml
[graph]
name = "spring_name_niche"
version = "0.1.0"
description = "What this graph deploys"
coordination = "Sequential"

[graph.metadata]
internal_bond_type = "covalent"
trust_model = "genetic_lineage"

[[graph.node]]
name = "node_label"
binary = "primal_binary_name"
order = 1
required = true
depends_on = []
health_method = "health.liveness"
by_capability = "security"
capabilities = ["beacon.generate"]
condition = "env.HAS_GPU"
skip_if = "env.HEADLESS"
```

**Rule**: `by_capability` on all nodes; `name` is human-only, not for discovery.

### Beacon coordination (zero-metadata handshake)

1. `capability.call("beacon","generate")`  
2. `capability.call("beacon","encrypt",{data})`  
3. `capability.call("network","beacon_exchange",{beacon,peer})`  
4. `capability.call("beacon","try_decrypt",{ciphertext})`  
5. Rendezvous: ciphertext only; match by hashed lineage.

### Bonding validation

| Bond | Tests |
|------|--------|
| Covalent | Same family seed; `meld()` routing |
| Ionic | Different families; limited cross-call |
| Metallic | Orchestrator + workers |
| Weak | Read-only; ephemeral; `split()` on disconnect |

### Cross-learning flow

biomeOS develops → primalSpring absorbs/validates → springs replicate BYOB graphs → discoveries → primalSpring promotes → wateringHole standards → biomeOS next version.

### Division of ownership

| Owner | Responsibility |
|-------|------------------|
| biomeOS | Lifecycle, Neural API, HTTP, CLI, deploy, genomeBin |
| primalSpring | Composition validation, graph validation, waves, bonding, beacon validation, cross-spring ecology, BYOB templates |
| wateringHole | Standards, handoffs, leverage guides |

---

## primalSpring Composition Guidance

**Source**: primalSpring v0.7.0 patterns.

### Capabilities exposed

| Method | Role |
|--------|------|
| `coordination.validate_composition` | Tower/Node/Nest/FullNucleus |
| `coordination.discovery_sweep` | Enumerate primals |
| `coordination.neural_api_status` | Neural API health |
| `health.check` / `health.liveness` / `health.readiness` | Probes |
| `capabilities.list` | Coordination capabilities |
| `lifecycle.status` | Version, domain, status |

### Modes (summary)

1. **Standalone**: discovery sweep (empty ok), Neural API status, honest skip when no primals.
2. **Tower** (exp001, exp005, exp006): BearDog + Songbird; crypto; ordering; degradation skips.
3. **Node** (exp002, exp050): + ToadStool; compute routing; coralReef → toadStool → barraCuda triangle.
4. **Nest** (exp003, exp042): + NestGate; storage round-trip; fieldMouse path.
5. **Full NUCLEUS** (exp004, exp044): eight primals; Squirrel AI; Neural API composition discovery.
6. **Provenance trio** (exp020–022, exp041): rhizoCrypt + loamSpine + sweetGrass; six-phase commit; Merkle/federation.
7. **Cross-spring** (exp024): airSpring → wetSpring → neuralSpring; exp041 provenance for science.
8. **Sovereign compute** (exp050): coralReef → toadStool → barraCuda.

**Patterns**: `resilient_call`, `CircuitBreaker`, `RetryPolicy`, `extract_rpc_result` / `extract_rpc_dispatch`, `IpcError::is_method_not_found()`, `ValidationSink`.

### Discovery protocol

Runtime only: env → XDG → tmp → manifest → Neural API. No compile-time primal imports.

### Cross-architecture (v0.7.0)

`x86_64-unknown-linux-musl` and `aarch64-unknown-linux-musl` — coordination logic identical; transport differs (filesystem vs abstract sockets on Android). genomeBin for multi-arch packaging.

### Graph-driven overlays (v0.7.0)

Tier-independent primals (Squirrel, petalTongue, biomeOS) as optional overlays via deploy graphs. `required = false`, `spawn = true/false`, `by_capability`, `merge_graphs()`. biomeOS `graph.compose` for runtime merge.

### Squirrel free-roaming (v0.7.0)

3-tier discovery: env `{CAPABILITY}_PROVIDER_SOCKET` → Neural API registry → `$XDG_RUNTIME_DIR/biomeos/` scan. Wired env examples: `STORAGE_*_PROVIDER_SOCKET`, `COMPUTE_*`, `HTTP_REQUEST_PROVIDER_SOCKET`, `CRYPTO_SIGN_PROVIDER_SOCKET`. Experiments: exp070, integration tests listed in source.

### Expectations for composed primals

- JSON-RPC: `health.liveness`, `health.readiness`, `health.check`, `capabilities.list`.
- 5-tier discovery; no hardcoded peer names in production.
- ecoBin targets: musl static, strip, LTO.
- Honest `check_skip` — never fake pass.

---

## Provenance Trio Integration

**Pattern**: Springs integrate rhizoCrypt + loamSpine + sweetGrass **only** via biomeOS `capability.call` (UDS to Neural API) — no direct trio crate imports in production.

### Routing

| capability.call | Routes to |
|-----------------|-----------|
| `dag.*` | rhizoCrypt |
| `commit.*` | loamSpine |
| `provenance.*` | sweetGrass |

### Types (`provenance-trio-types`)

`DehydrationSummary`, `PipelineRequest`, `PipelineResult`, `ProvenancePipeline`, `SimpleProvenancePipeline`.

### Neural API socket discovery (template)

Priority: `NEURAL_API_SOCKET` → `BIOMEOS_SOCKET_DIR/neural-api-{family}.sock` → `XDG_RUNTIME_DIR/biomeos/neural-api-{family}.sock` → `/tmp/neural-api-{family}.sock`.

### `capability.call` helper shape

```json
{
  "jsonrpc": "2.0",
  "method": "capability.call",
  "params": { "capability": "<domain>", "operation": "<op>", "args": { } },
  "id": 1
}
```

Newline after payload; read one response line; parse `result` / `error`.

### Session lifecycle (adapt names)

- `dag` / `create_session` — begin  
- `dag` / `append_event` — record step  
- Complete: `dag` / `dehydrate` → `commit` / `session` → `provenance` / `create_braid`

### Graceful degradation

| Condition | Behavior |
|-----------|----------|
| No socket | `Ok`, provenance `"unavailable"` |
| Dehydrate fails | `Ok`, `"unavailable"` |
| Commit fails | `Ok`, `"partial"` |
| Braid fails | `Ok`, `"complete"`, empty `braid_id` |

Domain logic must not fail solely because provenance is unavailable.

### Capability routing reference

| capability | operation | Underlying JSON-RPC (typical) |
|------------|-----------|-------------------------------|
| dag | create_session | `dag.session.create` |
| dag | append_event | `dag.event.append` |
| dag | dehydrate | `dag.dehydration.trigger` |
| commit | session | `commit.session` |
| provenance | create_braid | `braid.create` |
| provenance | record_dehydration | `contribution.record_dehydration` |

### Checklist

- [ ] `ipc/provenance.rs` from template  
- [ ] Domain-specific session/event names  
- [ ] Handlers return availability status  
- [ ] Optional `provenance-trio-types` for `ProvenancePipeline`  
- [ ] Tests: socket unset + biomeOS running  

---

## Spring Validation Assignments

**Principle**: barraCuda validates dispatch; **springs** validate correct science under real conditions.

### Responsibility split

```
barraCuda → dispatch, precision, shaders, buffers
├── hotSpring → f64/cancellation, conservation, spectral convergence
├── wetSpring → bio-stats, ODEs, Welford
├── airSpring → PDEs, seasonal pipelines, GPU/CPU parity
├── groundSpring → Anderson, tolerance tiers, noise
├── neuralSpring → training, attention, evolution numerics
└── healthSpring → PK/PD, population MC, eigensolve
```

### Validation matrix (excerpt)

| Spring | Module / area | Success criteria (examples) |
|--------|---------------|-----------------------------|
| hotSpring | `ops::md::forces` | Energy drift ≤ 10⁻⁶ / 1000 steps |
| hotSpring | `linalg::sparse` CG | Residual ≤ 10⁻¹² in ≤ 500 iters |
| hotSpring | DF64 / plasma W(z) | ULP ≤ 4; rel error ≤ 1% near cancellation |
| wetSpring | `ops::bio::*` | Match Python tier 8 |
| wetSpring | `numerical::rk45` | Endpoint within atol/rtol |
| airSpring | `pde::richards_gpu` | Physical bounds, mass conservation |
| airSpring | seasonal pipeline | ≤ 0.04% vs CPU over 365 days |
| groundSpring | `spectral::anderson` | 1D λ within ~5% of analytic |
| groundSpring | tolerance tiers | Monotonic refinement |
| neuralSpring | attention | Softmax rows sum to 1 ± 10⁻⁶ |
| healthSpring | `ops::hill_f64` | EC50 within 1% |

Full matrix and per-spring bullet lists: see source `SPRING_VALIDATION_ASSIGNMENTS.md` (barraCuda pin v0.3.5 at time of writing).

### Workflow

barraCuda release → each spring updates pin → run assigned validations → report evidence → failures → `SPRING_EVOLUTION_ISSUES.md` → fix in barraCuda → re-validate.

---

## Inter-Primal Interactions

**Basis**: RootPulse architecture — primals expose capabilities; biomeOS composes; version control and higher-order behavior emerge.

### Actor metaphor (conceptual)

- rhizoCrypt: ephemeral DAG workspace  
- LoamSpine: immutable linear history  
- NestGate: content-addressed storage  
- BearDog: security / lineage  
- SweetGrass: semantic attribution  
- Songbird: discovery / coordination  

biomeOS composes orchestration.

### Working interactions (Phase 1–2)

**Songbird ↔ BearDog (BirdSong v2)**  
Flow: identity payload → HTTP POST `/api/v2/birdsong/encrypt` → ChaCha20-Poly1305 → BirdSongPacket v2 → UDP multicast `239.255.0.1:4200` → receive → decrypt → auto-trust within family.  
Protocol: `wateringHole/birdsong/BIRDSONG_PROTOCOL.md`.

**biomeOS ↔ primals (health)**  
`PrimalHealthMonitor` ~30s interval; HTTP GET `/api/v1/health`; states Healthy/Degraded/Unhealthy; recovery; SSE to PetalTongue. Code: `biomeos-core/src/primal_health.rs`.

**biomeOS ↔ PetalTongue (SSE)**  
`/api/v1/events/stream` — PrimalDiscovered, HealthChanged, TopologyChanged, FamilyJoined, TrustUpdated. PetalTongue integration was pending at doc time.

### Phase 3 provenance trio (validated March 2026)

**rhizoCrypt → LoamSpine (dehydration)**  
Session DAG → dehydrate → `DehydrationSummary` → loamSpine commit path. biomeOS `rootpulse_commit.toml` orchestrates.

**SweetGrass ↔ LoamSpine**  
`contribution.recordDehydration`, `braid.create`; semantic attribution vs linear history.

**NestGate ↔ LoamSpine**  
Planned: tree/blob storage → commit objects → BearDog sign → loamSpine append.

### Planned / partial

**Songbird federation**: multi-tower, cross-family routing, bridge policies — infrastructure-oriented roadmap.

**Retry & circuit breaker (biomeOS)**  
Exponential backoff + jitter; max attempts; circuit open after N failures; half-open recovery. `biomeos-core/src/retry.rs`.

### Composition patterns

1. **Sequential**: e.g. tree → sign → append commit.  
2. **Parallel**: `tokio::join!` multi-source discovery.  
3. **Conditional**: optional SweetGrass after commit.  
4. **Feedback**: e.g. Squirrel-assisted merge resolution.

### Roadmap snapshots (from source)

- Phase 3.1: LoamSpine + NestGate VCS core  
- Phase 3.2: rhizoCrypt performance / sessions  
- Phase 3.3: SweetGrass semantic attribution (much already validated)  
- Phase 3.4: Federation  

### Success metrics (targets)

Discovery < 100ms; encryption < 10ms; health interval 30s; circuit breaker complete; Phase 3: commit speed vs Git, dehydration < 1s typical, federation discovery < 1s.

### Design principles

Interface segregation; dependency inversion (capabilities); message passing; single responsibility per primal.

### Plasmodium (over-NUCLEUS)

Covalent bonding → collective capability view; routing by capability/load; no central brain; graceful degradation (“sclerotium”). Uses Songbird mesh, BearDog lineage, JSON-RPC — not a new primal. Spec: `PLASMODIUM_OVER_NUCLEUS_SPEC.md`; `biomeos-core::plasmodium`.

### Phase 4: Composition decomposition (March 31, 2026 — primalSpring Phase 23f)

Seven deployable compositions (C1–C7): render, narration AI, session, game science, persistence, proprioception, full interactive — statuses partial/pass as in source.

**Gap matrix (evolving)**  
BM-04 capability discovery: noted resolved in source (v2.81 `topology.rescan`). RC-01 rhizoCrypt UDS: resolved (`--unix`). LS-03 loamSpine: resolved (graceful infant discovery). PT-01 petalTongue, SQ-01 Squirrel: noted resolved.

**toadStool S169**  
Removed proxy methods that belonged to Squirrel, coralReef, biomeOS, Songbird — springs must route AI to Squirrel, shaders to coralReef per capability.

**ludoSpring V37.1**  
Live plasmidBin validation statistics and projected pass rates in source; barraCuda math pipeline checks; Fitts/Hick fixes referenced as Sprint 25.

**Related**: `PRIMAL_GAPS.md`, `PRIMAL_RESPONSIBILITY_MATRIX.md`, `IPC_COMPLIANCE_MATRIX.md`, `SPRING_EVOLUTION_ISSUES.md` ISSUE-011–015.

---

## Version History

| Version | Date | Summary |
|---------|------|---------|
| 1.0.0 | 2026-04-04 | Consolidated five wateringHole coordination/validation documents into this single reference. Emoji and decorative markup from `INTER_PRIMAL_INTERACTIONS.md` omitted per consolidation rules. |
| (prior) | 2026-03-10 — 2026-03-31 | Per-source file versions and dates preserved in git history of individual files. |
