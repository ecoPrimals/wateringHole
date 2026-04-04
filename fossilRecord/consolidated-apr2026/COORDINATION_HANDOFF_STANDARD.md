# Coordination Handoff Standard

**Version:** 1.0.0  
**Date:** March 18, 2026  
**Status:** Active — defines how biomeOS externalizes coordination to primalSpring  
**Companion:** `CAPABILITY_BASED_DISCOVERY_STANDARD.md`

## Principle

> biomeOS develops coordination patterns. primalSpring validates and teaches them.
> Springs cross-learn through primalSpring, not through direct coupling.

biomeOS is the primal that runs NUCLEUS. It launches processes, manages
lifecycle, routes capabilities via the Neural API, and handles deployment.
But **coordination validation** — confirming that compositions are healthy,
graphs execute correctly, and bonding works — belongs in primalSpring.

This standard defines what patterns primalSpring must absorb, how springs
reference them, and how cross-learning flows through the ecosystem.

---

## Extractable Base Structures

These biomeOS types and algorithms are **capability-based** (no hardcoded
primal names) and form the shared vocabulary for all springs.

### Atomic Type System

**Source:** `biomeos-types/src/atomic.rs`

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

**Key property:** `ProviderHealthMap` is keyed by capability identifier
(`"crypto"`, `"discovery"`), not by primal name. Providers are discovered
at runtime via `topology.metrics` or `capability.discover`.

### Concurrent Startup Waves

**Source:** `biomeos-core/src/concurrent_startup.rs`

```
Input: primals with provides/requires capability sets
  ↓
DependencyGraph::build() → map capabilities to providers
  ↓
topological_waves() → Vec<Vec<PrimalId>>  (Kahn's algorithm)
  ↓
start_in_waves() → concurrent within wave, sequential between waves
```

**Key property:** Uses `ManagedPrimal::provides()` and `requires()` —
pure capability names. No primal roster. Cycle detection built in.

### Coordination Patterns

**Source:** `biomeos-graph/src/graph.rs`

| Pattern | When to Use |
|---------|------------|
| **Sequential** | Dependency-ordered startup (Tower → Node → Nest) |
| **Parallel** | Independent nodes with no mutual dependencies |
| **ConditionalDag** | Branching logic (`condition`, `skip_if` predicates) |
| **Pipeline** | Streaming data between nodes (bounded mpsc channels) |
| **Continuous** | Fixed-timestep loop (game engine tick, telemetry) |

### Validation Sink

**Source:** `biomeos-types/src/validation.rs`

```rust
pub trait ValidationSink {
    fn emit(&mut self, finding: ValidationFinding);
    fn error(&mut self, rule, message);
    fn warning(&mut self, rule, message);
    fn info(&mut self, rule, message);
}
```

Pluggable output: stderr (interactive), buffer (programmatic), JSON (CI).

### Plasmodium Agent Routing

**Source:** `biomeos-atomic-deploy/src/neural_api_server/agents/`

```rust
pub struct PlasmodiumAgent {
    routing_table: HashMap<String, Vec<CapabilityRoute>>,
    // ...
}

impl PlasmodiumAgent {
    pub fn meld(&mut self, other: &PlasmodiumAgent);   // merge routing tables
    pub fn split(&mut self, gate_id: &str) -> Option<PlasmodiumAgent>;
    pub fn resolve(&self, capability_domain: &str) -> Option<&CapabilityRoute>;
}
```

---

## Validation Matrix (Capability-Based)

primalSpring validates each atomic tier by discovering capabilities, not
primals. The validation matrix:

### Tower

| Check | Method | Pass Criteria |
|-------|--------|--------------|
| Security provider reachable | `capability.discover("security")` | socket found |
| Discovery provider reachable | `capability.discover("discovery")` | socket found |
| Security provider healthy | `health.check` via discovered socket | `true` |
| Discovery provider healthy | `health.check` via discovered socket | `true` |
| Beacon chain available | `beacon.generate` → `beacon.encrypt` → `beacon.try_decrypt` | roundtrip |
| Network exchange available | `network.beacon_exchange` | delivery |

### Node (Tower + Compute)

| Check | Method | Pass Criteria |
|-------|--------|--------------|
| All Tower checks | (above) | (above) |
| Compute provider reachable | `capability.discover("compute")` | socket found |
| Compute provider healthy | `health.check` | `true` |
| GPU/resource detection | `compute.query_capabilities` | capabilities array |

### Nest (Tower + Storage)

| Check | Method | Pass Criteria |
|-------|--------|--------------|
| All Tower checks | (above) | (above) |
| Storage provider reachable | `capability.discover("storage")` | socket found |
| Storage provider healthy | `health.check` | `true` |
| Store/retrieve cycle | `storage.store` → `storage.retrieve` | data matches |

### Full NUCLEUS (all capabilities)

| Check | Method | Pass Criteria |
|-------|--------|--------------|
| All Tower + Node + Nest | (above) | (above) |
| AI provider | `capability.discover("ai")` → `health.check` | healthy |
| Provenance trio | `capability.discover("dag")`, `("commit")`, `("provenance")` | all healthy |
| Degradation level | `FullNucleus::degradation_level()` | `"Full NUCLEUS"` |

---

## Deploy Graph TOML Schema

All springs use this schema for BYOB deploy graphs:

```toml
[graph]
name = "spring_name_niche"
version = "0.1.0"
description = "What this graph deploys"
coordination = "Sequential"

[graph.metadata]
internal_bond_type = "covalent"     # covalent | ionic | metallic | isolated
trust_model = "genetic_lineage"     # genetic_lineage | contractual | zero_trust

[[graph.node]]
name = "node_label"
binary = "primal_binary_name"
order = 1
required = true
depends_on = []
health_method = "health.liveness"
by_capability = "security"          # PREFERRED: capability-first discovery
capabilities = ["beacon.generate"]  # what this node provides
condition = "env.HAS_GPU"           # optional: ConditionalDag predicate
skip_if = "env.HEADLESS"            # optional: skip predicate
```

**Rule:** New graphs SHOULD use `by_capability` for all nodes.
`name` is retained for human readability but MUST NOT be used for discovery.

---

## Beacon Coordination Protocol

The zero-metadata handshake pattern, validated by primalSpring:

```
1. capability.call("beacon", "generate")           → family-scoped seed
2. capability.call("beacon", "encrypt", {data})     → AEAD ciphertext (noise)
3. capability.call("network", "beacon_exchange", {beacon, peer})  → relay
4. capability.call("beacon", "try_decrypt", {ciphertext})         → plaintext | null
5. Rendezvous: store only ciphertext, match by hashed lineage
```

**Properties validated:**
- Ciphertext is indistinguishable from random (zero metadata leak)
- Only family members can decrypt (mitochondrial DNA scope)
- Lineage matching uses hashed identity, not plaintext
- Tower stores nothing identifiable

---

## Bonding Validation

primalSpring validates multi-NUCLEUS bonding:

| Bond | Test | Validation |
|------|------|-----------|
| **Covalent** | Two NUCLEUS instances with same family seed | `meld()` merges routing tables, mutual discovery via mesh |
| **Ionic** | Two NUCLEUS instances, different families | Limited `capability.call` across bond, no shared state |
| **Metallic** | Centralized orchestrator + workers | Electron sea routing, specialization |
| **Weak** | Unknown peer | Read-only access, ephemeral, `split()` on disconnect |

---

## Cross-Learning Flow

```
biomeOS ──[develops patterns]──→ docs/PRIMALSPRING_COORDINATION_HANDOFF.md
    ↓
primalSpring ──[absorbs, validates]──→ experiments/ + tests/
    ↓
springs ──[replicate BYOB graphs]──→ their own deploy graphs
    ↓
springs ──[discover new patterns]──→ primalSpring experiments
    ↓
primalSpring ──[promotes validated patterns]──→ wateringHole standards
    ↓
biomeOS ──[absorbs promoted patterns]──→ next version
```

Example: barraCuda shader growth in groundSpring → validated in
primalSpring exp050 (compute triangle) → promoted to wateringHole
`SOVEREIGN_COMPUTE_EVOLUTION.md` → absorbed by biomeOS's ToadStool
capability translation.

---

## What Stays Where

### biomeOS owns:
- Process lifecycle (launch, monitor, restart)
- Neural API server (routing, capability translation)
- HTTP endpoints (rendezvous, genome distribution)
- CLI (`biomeos validate`, `biomeos deploy`)
- Device-specific deployment (Pixel8a, LiveSpore)
- GenomeBin packaging

### primalSpring owns:
- Composition validation (are all capabilities available?)
- Deploy graph validation (structural + live)
- Startup wave computation (topological sort)
- Bonding validation (meld/split/resolve)
- Beacon coordination validation (capability chain available?)
- Cross-spring ecology validation
- BYOB graph templates and graduation criteria

### wateringHole owns:
- Standards documents (this file, `CAPABILITY_BASED_DISCOVERY_STANDARD.md`)
- Handoff records
- Cross-ecosystem leverage guides
