<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# rhizoCrypt Leverage Guide — Standalone, Trio, and Ecosystem Compositions

**Date**: March 16, 2026
**Primal**: rhizoCrypt v0.13.0-dev (Edition 2024)
**Audience**: All springs, all primals, biomeOS integrators
**Status**: Active

---

## Purpose

This document describes how rhizoCrypt can be leveraged — alone and in
composition with other primals — by springs and ecosystem consumers. Each
primal in the ecosystem will produce an equivalent guide. Together, these
guides form a combinatorial recipe book for emergent behaviors.

rhizoCrypt provides **ephemeral, content-addressed DAG sessions** with
lock-free concurrency, Merkle integrity proofs, and dehydration to permanent
storage. It is the "working memory" of the ecosystem.

**Philosophy**: Ephemeral by default, persistent by consent. rhizoCrypt
never stores permanently — it holds state until you decide what matters.

---

## IPC Methods (Semantic Naming)

All methods follow `{domain}.{operation}[.{variant}]` per the
[Semantic Method Naming Standard](./SEMANTIC_METHOD_NAMING_STANDARD.md).

| Method | What It Does |
|--------|-------------|
| `dag.session.create` | Open a new scoped DAG workspace |
| `dag.session.get` | Retrieve session metadata |
| `dag.session.list` | List all active sessions |
| `dag.session.discard` | Discard and clean up a session |
| `dag.event.append` | Add a content-addressed event (BLAKE3 hash, multi-parent) |
| `dag.event.append_batch` | Append multiple vertices in a batch |
| `dag.vertex.get` | Retrieve a vertex by hash |
| `dag.vertex.query` | Query vertices with type, agent, limit filters |
| `dag.vertex.children` | Get all children of a vertex |
| `dag.frontier.get` | Get the current DAG tips (latest unresolved vertices) |
| `dag.genesis.get` | Get root vertices of a session |
| `dag.merkle.root` | Compute the Merkle root for a session |
| `dag.merkle.proof` | Generate an inclusion proof for a vertex |
| `dag.merkle.verify` | Verify a Merkle inclusion proof |
| `dag.slice.checkout` | Checkout a snapshot from permanent storage |
| `dag.slice.get` | Retrieve slice metadata |
| `dag.slice.list` | List all active slices |
| `dag.slice.resolve` | Resolve a slice to underlying session data |
| `dag.dehydration.trigger` | Collapse session into a permanent summary |
| `dag.dehydration.status` | Check dehydration operation status |
| `health.check` | Service health with status, version, uptime |
| `health.metrics` | Operational metrics (sessions, latency, errors) |
| `capability.list` | List all capabilities this primal provides |

**Transport**: JSON-RPC 2.0 over HTTP (required), tarpc/bincode (optional).
**Registry**: `capability_registry.toml` (23 methods, 7 domains).

### Self-Knowledge (`niche.rs`)

rhizoCrypt follows the ecosystem niche pattern (established by squirrel,
groundSpring, airSpring). The `niche.rs` module is the single source of
truth for identity, capabilities, and scheduling hints:

| Constant / Function | Purpose |
|---------------------|---------|
| `PRIMAL_ID` | `"rhizocrypt"` — identity for biomeOS registration |
| `CAPABILITIES` | All 23 exposed methods |
| `CONSUMED_CAPABILITIES` | What rhizoCrypt calls on other primals |
| `COST_ESTIMATES` | Per-method latency hints for Pathway Learner scheduling |
| `operation_dependencies()` | Parallelization DAG for Pathway Learner |
| `capability_list()` | Enhanced `capability.list` response with per-method cost and deps |

### Enhanced `capability.list` Response

The `capability.list` response includes per-method cost tier and dependency
information, aligned with loamSpine and sweetGrass:

```json
{
  "primal": "rhizocrypt",
  "version": "0.13.0-dev",
  "methods": [
    { "method": "dag.session.create", "domain": "dag", "cost": "low",  "deps": [] },
    { "method": "dag.event.append",   "domain": "dag", "cost": "low",  "deps": ["dag.session.create"] },
    { "method": "dag.merkle.root",    "domain": "dag", "cost": "medium", "deps": ["dag.event.append"] },
    { "method": "dag.dehydration.trigger", "domain": "dag", "cost": "high", "deps": ["dag.session.create", "dag.event.append"] }
  ]
}
```

biomeOS Pathway Learner uses this to optimize graph execution order and
parallelize independent operations.

---

## 1. rhizoCrypt Standalone

These patterns use rhizoCrypt alone — no other primals required.

### 1.1 Experiment Session Tracking

**For**: Any spring running validated experiments.

Every experiment run becomes a DAG session. Each computation step is a
vertex. Parent links encode the dependency graph. The Merkle root at the
end provides a single hash that proves the entire run's integrity.

```
dag.create_session { name: "wetspring-dada2-run-047" }
  → session_id

dag.append_vertex { session_id, payload: { step: "quality_filter", ... }, parents: [] }
  → vertex_a (BLAKE3 hash)

dag.append_vertex { session_id, payload: { step: "denoise", ... }, parents: [vertex_a] }
  → vertex_b

dag.append_vertex { session_id, payload: { step: "taxonomy", ... }, parents: [vertex_b] }
  → vertex_c

dag.merkle_root { session_id }
  → root_hash (proves entire pipeline integrity)
```

**Spring applications**:

| Spring | Session Represents |
|--------|-------------------|
| wetSpring | 16S rRNA pipeline: filter → denoise → chimera → taxonomy |
| airSpring | FAO-56 ET₀ computation: sensor ingest → Penman-Monteith → irrigation decision |
| hotSpring | Nuclear EOS parameter sweep: HFB → Yukawa → lattice QCD |
| neuralSpring | Training run: data prep → forward pass → loss → backprop → checkpoint |
| groundSpring | Calibration chain: raw measurement → bias correction → uncertainty propagation |
| healthSpring | Clinical pipeline: PK/PD model → dosing → outcome prediction |
| ludoSpring | Game session: player input → game state → DDA adjustment → engagement score |

### 1.2 Multi-Agent Collaboration

**For**: Any scenario where multiple agents contribute to the same workspace.

rhizoCrypt sessions are lock-free (`DashMap`). Multiple agents can append
vertices concurrently. Each agent's DID is recorded on their vertices,
enabling per-agent event counting and role tracking.

```
Agent A: dag.append_vertex { session_id, payload: {...}, agent_did: "did:eco:alice" }
Agent B: dag.append_vertex { session_id, payload: {...}, agent_did: "did:eco:bob" }
```

The DAG naturally captures branching and merging — no explicit merge
protocol needed. The frontier (`dag.get_frontier`) shows all unresolved
tips.

**Applications**: Multi-researcher experiments, multiplayer game sessions,
federated sensor networks, collaborative model training.

### 1.3 Content-Addressed Deduplication

**For**: Any spring handling large volumes of repeated or similar data.

Vertices are content-addressed via BLAKE3. Identical payloads produce
identical hashes. rhizoCrypt deduplicates at the vertex level — appending
the same content twice returns the existing hash without storage overhead.

**Applications**: Genomic sequence dedup (wetSpring), repeated sensor
readings (groundSpring, airSpring), cached shader compilation results
(via barraCuda).

### 1.4 Merkle Proof Exchange

**For**: Any scenario requiring proof that a specific result exists within
a larger computation.

`dag.merkle_proof` generates a compact inclusion proof for any vertex.
A verifier needs only the proof and the root hash — not the full session.

```
dag.merkle_proof { session_id, vertex_id }
  → { root, proof_path, leaf_hash }

dag.verify_proof { root, proof_path, leaf_hash }
  → true/false
```

**Applications**: Proving a specific measurement was part of a calibration
run (groundSpring), proving a drug interaction check happened in a clinical
pipeline (healthSpring), proving a game event occurred in a session
(ludoSpring).

### 1.5 Slice Semantics for Checkout

**For**: Any spring that needs to reference past results with different
ownership semantics.

Six slice modes control how data is checked out from permanent storage:

| Mode | Semantics | Use Case |
|------|-----------|----------|
| **Copy** | Full independent copy | Fork an experiment to try a different parameter |
| **Loan** | Temporary read-only access, must return | Borrow a reference dataset for a limited analysis |
| **Consignment** | Transfer to another agent for processing | Send data to another spring for cross-domain analysis |
| **Escrow** | Held by a neutral party until conditions met | Peer review: results locked until review complete |
| **Mirror** | Read-only synchronized replica | Dashboard showing live experiment state |
| **Provenance** | Read-only with full attribution chain | Audit trail for regulatory compliance |

---

## 2. rhizoCrypt + Trio Compositions

The **Memory & Attribution Stack** (rhizoCrypt + LoamSpine + sweetGrass)
forms a three-layer architecture coordinated by biomeOS:

```
sweetGrass (Attribution)  — who did what, fair contribution
      |
 LoamSpine (Permanence)   — immutable history, certificates
      |
 rhizoCrypt (Working Memory) — ephemeral DAG, dehydration
```

### 2.1 rhizoCrypt + LoamSpine: Ephemeral → Permanent

**The core dehydration pattern.** Work happens in rhizoCrypt (fast,
lock-free, disposable). When results matter, dehydrate to LoamSpine
(immutable, provable, forever).

```
1. dag.create_session → work in ephemeral DAG
2. dag.append_vertex (many times, branching, merging)
3. dag.dehydrate { session_id }
   → summary: { root_hash, vertex_count, frontier }
4. commit.session { dehydrated_summary }
   → LoamSpine entry (permanent, hash-chained, append-only)
```

**Why this matters**: Most data should be temporary. Sensor readings,
intermediate computations, failed experiments, draft game states — these
live and die in rhizoCrypt. Only distilled results earn permanence.

**Spring applications**:
- wetSpring: 1000 intermediate DADA2 steps → 1 permanent taxonomy result
- hotSpring: 10,000 lattice QCD iterations → 1 permanent EOS point
- airSpring: Daily ET₀ computations → weekly irrigation summary committed

### 2.2 rhizoCrypt + sweetGrass: Attributed Workspaces

**Every vertex carries agent DID. sweetGrass reads the DAG to compute
fair attribution.**

```
1. Multiple agents work in rhizoCrypt session
2. provenance.create_braid { session_id, agents: [...] }
   → sweetGrass creates a W3C PROV-O braid from the DAG
3. Attribution shares computed from vertex counts, roles, derivation chains
```

**Spring applications**:
- neuralSpring: Track which researcher contributed which training data
- ludoSpring: Fair attribution in collaborative game design (art, mechanics, levels)
- healthSpring: Clinical trial contribution tracking for multi-site studies

### 2.3 rhizoCrypt + LoamSpine + sweetGrass: Full RootPulse

**The complete provenance-backed workflow.** This is the canonical
composition — the "git commit" of the ecosystem.

```
1. dag.create_session       → ephemeral workspace
2. (work happens)           → vertices accumulate
3. dag.dehydrate            → collapse to summary
4. crypto.sign              → BearDog signs the summary
5. storage.store            → NestGate stores the payload
6. commit.session           → LoamSpine commits permanently
7. provenance.create_braid  → sweetGrass records attribution
```

biomeOS orchestrates this as a single graph execution via
`rootpulse_commit.toml`. Springs call
`NeuralBridge::capability_call("rootpulse", "commit", args)`.

---

## 3. rhizoCrypt + Other Primals

### 3.1 rhizoCrypt + BearDog: Signed DAGs

**Every vertex or session can be cryptographically signed.**

```
dag.append_vertex { payload: {...} } → vertex_hash
crypto.sign { data: vertex_hash }   → signature
```

**Applications**: Tamper-evident experiment logs, signed sensor
readings for regulatory compliance, signed game state for anti-cheat.

### 3.2 rhizoCrypt + NestGate: Content-Addressed Storage Bridge

**rhizoCrypt's BLAKE3 hashes are directly compatible with NestGate's
content-addressed storage.**

```
dag.dehydrate { session_id } → { vertex_hashes, payloads }
storage.put { hash, data }   → NestGate stores by content hash
```

The same hash that identifies a vertex in rhizoCrypt identifies the
blob in NestGate. No mapping table needed.

### 3.3 rhizoCrypt + Songbird: Session Discovery

**Other primals can discover active rhizoCrypt sessions via Songbird.**

```
discovery.announce { capability: "dag", session_id, metadata: {...} }
discovery.query   { capability: "dag" }
  → [ { primal: "rhizocrypt-abc123", sessions: [...] } ]
```

**Applications**: Multi-device experiment monitoring (groundSpring
sensors feeding a shared session), real-time collaboration discovery.

### 3.4 rhizoCrypt + petalTongue: Live DAG Visualization

**petalTongue can render a rhizoCrypt DAG as a live, interactive graph.**

```
dag.get_session_vertices { session_id } → vertices with parent links
visualization.render { grammar: { data: vertices, geom: "graph", ... } }
```

**Applications**: Live experiment pipeline visualization, game state
graph rendering, multi-agent collaboration dashboards.

### 3.5 rhizoCrypt + ToadStool: Compute-Tracked Sessions

**Track which compute substrates processed each step.**

```
dag.append_vertex { payload: { step: "gpu_matmul", substrate: "nvidia_sm89" } }
compute.submit { shader: "matmul_f64", ... } → result
dag.append_vertex { payload: { step: "result", result_hash, substrate } }
```

**Applications**: GPU provenance (which hardware computed which result),
cross-device reproducibility verification, cost tracking.

### 3.6 rhizoCrypt + Squirrel: AI-Augmented Sessions

**AI agents participate in DAG sessions like any other agent.**

```
dag.append_vertex { agent_did: "did:eco:squirrel", payload: { suggestion: "..." } }
```

Squirrel can also analyze session DAGs for patterns:

```
ai.analyze { context: session_vertices }
  → { patterns, anomalies, suggestions }
```

**Applications**: AI-assisted experiment design (neuralSpring), intelligent
merge conflict resolution (RootPulse), game balance suggestions
(ludoSpring).

### 3.7 rhizoCrypt + skunkBat: Anomaly-Monitored Sessions

**skunkBat can monitor session patterns for anomalous behavior.**

```
dag.get_session_vertices → event stream
(skunkBat baseline analysis)
  → alert if unusual vertex patterns, unexpected agents, or timing anomalies
```

**Applications**: Detecting unauthorized modifications to clinical data
(healthSpring), intrusion detection in federated sensor networks
(groundSpring).

---

## 4. Novel Spring Compositions

These are higher-order patterns that emerge from combining rhizoCrypt
with multiple primals simultaneously.

### 4.1 Provenance-Backed Scientific Pipeline

**Springs**: any + rhizoCrypt + LoamSpine + sweetGrass + BearDog

Every scientific computation becomes a signed, attributed, permanently
committed chain. From raw data to published result, every step is in
the DAG, every intermediate is content-addressed, the final result is
permanently committed with fair attribution.

```
Raw data (vertex) → Processing (vertex) → Analysis (vertex) → Result (vertex)
  ↓ dehydrate              ↓ sign                    ↓ commit    ↓ attribute
                  (full provenance chain — reproducible, auditable, fair)
```

This is the "lab notebook that can't lie" pattern. Applicable to every
spring's domain.

### 4.2 Cross-Spring Data Handoff with Escrow

**Springs**: wetSpring + airSpring + rhizoCrypt (Escrow slice)

Soil microbiome data (wetSpring) is needed by irrigation models
(airSpring). Rather than direct coupling:

```
1. wetSpring: dag.create_session → process 16S data → dag.dehydrate
2. wetSpring: dag.slice { mode: "Escrow", conditions: { consumer: "airSpring" } }
3. airSpring: (discovers escrow via Songbird)
4. airSpring: dag.slice { mode: "Copy", escrow_id }
   → data released only when conditions met
```

The Escrow pattern prevents data leakage while enabling cross-domain
collaboration. Applicable to any spring pair.

### 4.3 Real-Time Multi-Spring Dashboard

**Springs**: any + rhizoCrypt + petalTongue + Songbird

Multiple springs feed vertices into a shared session. petalTongue renders
the combined DAG as a live ecosystem graph. Songbird discovers all
participants.

```
groundSpring → dag.append_vertex { payload: { soil_moisture: 0.32 } }
airSpring    → dag.append_vertex { payload: { et0: 4.2 } }
wetSpring    → dag.append_vertex { payload: { community_diversity: 3.7 } }
petalTongue  → visualization.render.stream { session_id }
```

### 4.4 Consent-Gated Clinical Data with Loan Semantics

**Springs**: healthSpring + rhizoCrypt + BearDog + LoamSpine

Patient data enters a signed session. Researchers receive a Loan slice
with time-limited access. The loan automatically expires, and the
original session's Merkle root proves the data was not modified.

```
1. healthSpring: dag.create_session { name: "patient-abc-pk-model" }
2. healthSpring: (append clinical vertices, each BearDog-signed)
3. Researcher:   dag.slice { mode: "Loan", duration: "7d" }
4. (7 days later: loan expires, slice becomes inaccessible)
5. Audit:        dag.merkle_proof → proves integrity during loan period
```

### 4.5 GPU Compute Provenance Chain

**Springs**: any + rhizoCrypt + ToadStool + barraCuda + coralReef

Track the full sovereign compute pipeline in a DAG:

```
dag.append_vertex { payload: { step: "shader_author", wgsl_hash } }       (barraCuda)
dag.append_vertex { payload: { step: "compile", spirv_hash, target } }    (coralReef)
dag.append_vertex { payload: { step: "dispatch", gpu_id, timing } }       (ToadStool)
dag.append_vertex { payload: { step: "result", output_hash } }            (Spring)
dag.dehydrate → commit.session → provenance.create_braid
```

Every shader → compilation → dispatch → result is traceable. Hardware
fingerprints are captured. Reproducibility is provable.

### 4.6 Federated Experiment with Mirror Slices

**Springs**: any + rhizoCrypt + Songbird + LoamSpine

A multi-site experiment (e.g., clinical trial across hospitals,
multi-station weather monitoring) uses Mirror slices for synchronized
read-only replicas:

```
Site A: dag.create_session → append vertices (primary)
Site B: dag.slice { mode: "Mirror", source_session }
  → read-only synchronized replica, updated in real-time
Site C: dag.slice { mode: "Mirror", source_session }
  → another replica

dag.dehydrate → commit.session (single permanent record from primary)
```

### 4.7 Game State with Undo/Branch via DAG

**Springs**: ludoSpring + rhizoCrypt + sweetGrass

The DAG naturally supports undo (walk back to parent) and branching
(multiple children from one vertex). Game sessions can explore multiple
timelines and attribute each branch to different players or AI agents.

```
dag.append_vertex { payload: { turn: 1, state: {...} }, parents: [root] }
  → vertex_a
dag.append_vertex { payload: { turn: 2a, state: {...} }, parents: [vertex_a] }
  → branch_a (player explores path A)
dag.append_vertex { payload: { turn: 2b, state: {...} }, parents: [vertex_a] }
  → branch_b (AI explores path B)
dag.get_frontier → [branch_a, branch_b] (two active timelines)
```

---

## 5. Integration Patterns for Springs

### Minimal Integration (standalone rhizoCrypt only)

Add to your spring's `Cargo.toml` under an optional feature:

```toml
[dependencies]
neural-api-client-sync = { path = "../../phase2/biomeOS/crates/neural-api-client-sync", optional = true }

[features]
provenance = ["neural-api-client-sync"]
```

Then call via the Neural API bridge:

```rust
use neural_api_client_sync::NeuralBridge;

let bridge = NeuralBridge::discover()?;
let session = bridge.capability_call("dag", "create_session", &args)?;
```

The spring never imports rhizoCrypt directly. It discovers the capability
at runtime. If rhizoCrypt is not running, the call fails gracefully.

### Full Trio Integration

Use the same `NeuralBridge` for all trio operations:

```rust
let bridge = NeuralBridge::discover()?;

// Ephemeral work
bridge.capability_call("dag", "create_session", &session_args)?;
bridge.capability_call("dag", "append_vertex", &vertex_args)?;

// Permanence
bridge.capability_call("dag", "dehydrate", &dehydrate_args)?;
bridge.capability_call("commit", "session", &commit_args)?;

// Attribution
bridge.capability_call("provenance", "create_braid", &braid_args)?;
```

### Deploy Graph (biomeOS orchestration)

For automated workflows, define a TOML deploy graph:

```toml
[graph]
name = "spring_experiment_commit"
pattern = "Sequential"

[[graph.steps]]
name = "create_session"
capability = "dag"
operation = "create_session"

[[graph.steps]]
name = "dehydrate"
capability = "dag"
operation = "dehydrate"
depends_on = ["create_session"]

[[graph.steps]]
name = "commit"
capability = "commit"
operation = "session"
depends_on = ["dehydrate"]
```

---

## 6. What rhizoCrypt Does NOT Do

| Concern | Who Handles It |
|---------|---------------|
| Permanent storage | LoamSpine (commit/checkout) |
| Content blob storage | NestGate (put/get by hash) |
| Signing / encryption | BearDog (crypto.*) |
| Attribution / provenance | sweetGrass (provenance.*) |
| Discovery / networking | Songbird (discovery.*) |
| Compute dispatch | ToadStool (compute.*) |
| Visualization | petalTongue (visualization.*) |
| AI inference | Squirrel (ai.*) |
| Orchestration | biomeOS (Neural API) |

rhizoCrypt holds the ephemeral state. Everything else is discovered at
runtime and composed by biomeOS. This is fundamental — complexity
through coordination, not through coupling.
