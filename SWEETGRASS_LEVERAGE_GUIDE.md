<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# sweetGrass Leverage Guide — Standalone, Trio, and Ecosystem Compositions

**Date**: March 16, 2026
**Primal**: sweetGrass v0.7.22
**Audience**: All springs, all primals, biomeOS integrators
**Status**: Active

---

## Purpose

This document describes how sweetGrass can be leveraged — alone and in
composition with other primals — by springs and ecosystem consumers. Each
primal in the ecosystem will produce an equivalent guide. Together, these
guides form a combinatorial recipe book for emergent behaviors.

sweetGrass provides **semantic provenance and attribution** via W3C PROV-O
braids. It tracks who created what, how, and when — and computes fair
attribution shares across multi-agent collaborations.

**Philosophy**: Every piece of data has a story. sweetGrass makes that
story queryable, attributable, and permanently linkable.

---

## IPC Methods (Semantic Naming)

All methods follow `{domain}.{operation}[.{variant}]` per the
[Semantic Method Naming Standard](./SEMANTIC_METHOD_NAMING_STANDARD.md).

| Method | What It Does |
|--------|-------------|
| `braid.create` | Create a new provenance braid (Activity + Agent + Entity) |
| `braid.get` | Retrieve a braid by ID |
| `braid.get_by_hash` | Retrieve a braid by content hash |
| `braid.query` | Query braids by agent, activity type, time range |
| `braid.delete` | Delete a braid by ID |
| `braid.commit` | Anchor a braid to LoamSpine (BraidId → UUID, ContentHash → `[u8; 32]`) |
| `anchoring.anchor` | Cryptographically anchor a braid |
| `anchoring.verify` | Verify an anchor receipt |
| `provenance.graph` | Export the full provenance graph |
| `provenance.export_provo` | Export single braid as W3C PROV-O JSON-LD |
| `provenance.export_graph_provo` | Export full graph as W3C PROV-O JSON-LD |
| `attribution.chain` | Compute attribution chain for a braid |
| `attribution.calculate_rewards` | Calculate economic reward distribution |
| `attribution.top_contributors` | List top contributors by attribution weight |
| `compression.compress_session` | Compress session braids (0/1/Many) |
| `compression.create_meta_braid` | Create meta-braid from compressed session |
| `contribution.record` | Record an inter-primal contribution |
| `contribution.record_session` | Record a session contribution (session_id, source_primal) |
| `contribution.record_dehydration` | Record a full rhizoCrypt dehydration as attributed braids |
| `health.check` | Health check with store backend and uptime |
| `capability.list` | Advertise capabilities, dependencies, and costs |

**Transport**: JSON-RPC 2.0 over HTTP (primary), tarpc/bincode (high-perf),
Unix domain sockets (biomeOS IPC), REST (admin/debug).

---

## 1. sweetGrass Standalone

These patterns use sweetGrass alone — no other primals required.

### 1.1 Experiment Attribution

**For**: Any spring tracking who contributed what to a result.

Every experiment involves agents (researchers, AI, sensors) producing
entities (data, models, analyses) through activities (computations,
measurements, decisions). sweetGrass captures this as a W3C PROV-O braid.

```
braid.create {
  activity: { type: "dada2_analysis", started: "2026-03-14T10:00:00Z" },
  agents: [
    { did: "did:eco:alice", role: "DataCollector", weight: 0.4 },
    { did: "did:eco:bob", role: "Analyst", weight: 0.3 },
    { did: "did:eco:squirrel", role: "ModelTrainer", weight: 0.3 }
  ],
  entity: { data: <base64>, mime_type: "application/json" }
}
  → braid_id (content-addressed hash, URN format)
```

12 configurable roles with weights: `Creator`, `DataCollector`, `Analyst`,
`ModelTrainer`, `Reviewer`, `Curator`, `Annotator`, `Validator`,
`Publisher`, `Funder`, `Maintainer`, `Sponsor`.

**Spring applications**:

| Spring | What Gets Attributed |
|--------|---------------------|
| wetSpring | 16S taxonomy results — who ran the pipeline, who provided samples |
| airSpring | Irrigation decisions — sensor operators, modelers, field agronomists |
| hotSpring | EOS fit results — which researcher ran which parameter sweep |
| neuralSpring | Model weights — training data contributors, hyperparameter tuners, GPU providers |
| groundSpring | Calibration results — instrument operators, correction algorithm authors |
| healthSpring | Clinical outcomes — clinicians, lab technicians, AI diagnostic agents |
| ludoSpring | Game content — artists, mechanic designers, level builders, AI balance agents |

### 1.2 Derivation Chain Tracking

**For**: Any spring where results depend on earlier results.

sweetGrass braids can declare derivations — "this braid was derived from
those braids". This creates a queryable dependency graph with time-decay
attribution that propagates through the chain.

```
braid.create { ..., derived_from: [braid_a, braid_b] }
  → braid_c (carries attribution from a, b, and its own agents)

provenance.lineage { braid_id: braid_c }
  → full derivation tree back to root braids
```

**Applications**: Tracking how a final publication derives from raw
measurements (groundSpring), how a trained model derives from data
preprocessing steps (neuralSpring), how a game balance patch derives
from telemetry analysis (ludoSpring).

### 1.3 Privacy-Aware Provenance

**For**: Any spring handling sensitive or consent-gated data.

sweetGrass implements GDPR-inspired 5-level privacy controls:

| Level | Visibility | Use Case |
|-------|-----------|----------|
| **Public** | Full provenance visible | Open science results |
| **Attributed** | Agent DIDs visible, data redacted | Published papers |
| **Pseudonymous** | Agent DIDs replaced with pseudonyms | Clinical trials |
| **Statistical** | Only aggregate statistics | Population health |
| **Private** | Provenance exists but is opaque | Patient records |

Data subject rights: access, erasure, portability, selective disclosure.

**Applications**: healthSpring (HIPAA), wetSpring (consent-gated vault
specimens), groundSpring (classified sensor locations), ludoSpring
(minor player protection).

### 1.4 Session Compression (0/1/Many)

**For**: Any spring with high-frequency events that need summarization.

sweetGrass's compression engine collapses verbose provenance into
canonical forms:

| Pattern | What It Does |
|---------|-------------|
| **0 (null session)** | Empty or failed sessions — recorded as absence |
| **1 (singleton)** | Single meaningful result — kept as-is |
| **Many (aggregate)** | Repeated events — compressed to summary with statistics |

```
compression.analyze { session_id, events: [...] }
  → { pattern: "Many", compressed_count: 847, summary: {...} }
```

**Applications**: 60 Hz game telemetry compressed to session summary
(ludoSpring), daily sensor readings compressed to weekly aggregate
(airSpring), repeated PK measurements compressed to curve parameters
(healthSpring).

### 1.5 PROV-O Export

**For**: Any spring needing standards-compliant provenance output.

sweetGrass exports W3C PROV-O JSON-LD natively. This is the international
standard for provenance interchange — accepted by journals, regulators,
and archival systems.

```
provenance.graph { braid_id }
  → {
    "@context": "http://www.w3.org/ns/prov#",
    "entity": [...],
    "activity": [...],
    "agent": [...],
    "wasGeneratedBy": [...],
    "wasAttributedTo": [...]
  }
```

**Applications**: Journal submission provenance (wetSpring, hotSpring),
regulatory audit trails (healthSpring, airSpring), reproducibility
certificates (any spring).

---

## 2. sweetGrass + Trio Compositions

The **Provenance Trio** (sweetGrass + rhizoCrypt + LoamSpine) forms a
three-layer architecture:

```
sweetGrass (Attribution)      — who did what, fair contribution
      ↕
 LoamSpine (Permanence)       — immutable history, certificates
      ↕
 rhizoCrypt (Working Memory)  — ephemeral DAG, dehydration
```

### 2.1 sweetGrass + rhizoCrypt: Dehydration Attribution

**The core attribution pattern.** rhizoCrypt dehydrates a session and
pushes the summary to sweetGrass, which creates attributed braids.

```
1. (rhizoCrypt session completes)
2. contribution.record_dehydration {
     source_primal: "rhizoCrypt",
     session_id: "...",
     merkle_root: "...",
     vertex_count: 47,
     agents: ["did:eco:alice", "did:eco:bob"],
     operations: ["filter", "denoise", "taxonomy"],
     niche: "wetspring"
   }
   → { braids_created: 3, braid_ids: [...] }
```

sweetGrass reads the agent list and operation history from the dehydration
summary to compute attribution shares. No manual attribution entry needed —
the DAG's structure is the ground truth.

**Spring applications**:
- wetSpring: Pipeline finishes → rhizoCrypt dehydrates → sweetGrass
  attributes each researcher's contribution to the taxonomy result
- neuralSpring: Training run ends → dehydration → attribution of data
  providers, GPU operators, and hyperparameter tuners
- ludoSpring: Game session ends → dehydration → attribution of player
  actions, AI suggestions, and mechanic contributions

### 2.2 sweetGrass + LoamSpine: Anchored Attribution

**Attribution that can't be altered.** sweetGrass braids are anchored
to LoamSpine, making the attribution record immutable.

```
1. braid.create { ... }        → braid_id
2. braid.commit {
     braid_id, spine_id,
     committer: "did:eco:alice"
   }
   → LoamSpine entry (permanent, hash-chained)
```

Once anchored, attribution shares are frozen. This is critical for
reward distribution — sunCloud reads the anchored braids to compute
fair payments.

**Applications**: Publication credit (wetSpring, hotSpring), royalty
distribution (ludoSpring game content), regulatory compliance records
(healthSpring, airSpring).

### 2.3 sweetGrass + rhizoCrypt + LoamSpine: Full Provenance Pipeline

**The complete flow — biomeOS orchestrates as `provenance_pipeline.toml`.**

```
1. dag.create_session          → ephemeral workspace (rhizoCrypt)
2. (spring work happens)       → vertices accumulate
3. dag.dehydrate               → collapse to summary (rhizoCrypt)
4. crypto.sign                 → BearDog signs the summary
5. storage.store               → NestGate stores the payload
6. commit.session              → LoamSpine commits permanently
7. contribution.record_dehydration → sweetGrass records attribution
```

Springs invoke this as a single graph:

```rust
bridge.capability_call("graph", "execute", &json!({
  "graph": "provenance_pipeline",
  "params": {
    "SESSION_ID": session_id,
    "AGENT_DID": agent_did,
    "EXPERIMENT_ID": experiment_id,
    "NICHE": "wetspring"
  }
}))?;
```

---

## 3. sweetGrass + Other Primals

### 3.1 sweetGrass + BearDog: Signed Attribution

**Every braid can be cryptographically signed by its creator.**

```
braid.create { ... }           → braid_id, content_hash
crypto.sign { data: content_hash, signer: "did:eco:alice" }
  → signature (Ed25519)
```

Signed braids prove that the attributed agent actually endorsed the
attribution. This prevents false attribution — you can't claim someone
contributed without their signature.

**Applications**: Peer-reviewed attribution (wetSpring, hotSpring),
signed game authorship (ludoSpring), tamper-evident clinical records
(healthSpring).

### 3.2 sweetGrass + NestGate: Content-Addressed Braids

**Braid content hashes are directly compatible with NestGate storage.**

```
braid.create { entity: { data: large_dataset } }
  → braid_id (sha256 content hash)

storage.put { hash: braid_id, data: braid_payload }
  → NestGate stores the full braid by its content hash
```

The same hash that identifies a braid in sweetGrass identifies the
blob in NestGate. Large provenance graphs can be stored in NestGate
and referenced by hash.

### 3.3 sweetGrass + Songbird: Attribution Discovery

**Other primals can discover what attributions exist for their data.**

```
discovery.query { capability: "provenance", filter: { agent: "did:eco:alice" } }
  → [ { primal: "sweetgrass-abc123", braids: [...] } ]
```

**Applications**: A researcher queries "what have I been attributed to
across the ecosystem?" — Songbird discovers all sweetGrass instances
that have braids for their DID.

### 3.4 sweetGrass + petalTongue: Attribution Visualization

**petalTongue can render provenance graphs as interactive visualizations.**

```
provenance.graph { braid_id }   → PROV-O JSON-LD graph
visualization.render {
  grammar: {
    data: prov_graph,
    geom: "graph",
    color: "agent_role",
    size: "attribution_share"
  }
}
```

**Applications**: Research contribution dashboards (any spring),
game credit visualizations (ludoSpring), clinical audit trail
viewers (healthSpring), ecosystem-wide attribution maps.

### 3.5 sweetGrass + ToadStool: Compute Attribution

**Track which compute substrates contributed to a result.**

```
braid.create {
  activity: { type: "gpu_computation" },
  agents: [
    { did: "did:eco:toadstool:gpu-0", role: "ComputeProvider" },
    { did: "did:eco:alice", role: "Creator" }
  ],
  entity: { data: result_hash }
}
```

ToadStool's GPU/NPU/CPU substrate identity becomes an agent in the
braid. Fair attribution can include compute providers alongside
researchers.

**Applications**: GPU time attribution (hotSpring HPC runs),
shader computation credit (barraCuda), federated training
contribution (neuralSpring).

### 3.6 sweetGrass + Squirrel: AI Attribution

**AI agents get proper attribution for their contributions.**

```
braid.create {
  agents: [
    { did: "did:eco:squirrel:gpt-4", role: "Analyst", weight: 0.2 },
    { did: "did:eco:alice", role: "Creator", weight: 0.8 }
  ]
}
```

Squirrel can also analyze provenance graphs to suggest missing
attributions or detect attribution anomalies:

```
ai.analyze { context: provenance_graph }
  → { missing_attributions: [...], anomalies: [...] }
```

**Applications**: AI-assisted literature review attribution
(wetSpring), AI game balance co-authorship (ludoSpring),
AI-suggested experiment improvements credited properly
(neuralSpring).

### 3.7 sweetGrass + skunkBat: Attribution Integrity Monitoring

**skunkBat can monitor attribution patterns for anomalies.**

```
provenance.attribution { braid_id } → attribution_shares
(skunkBat anomaly detection)
  → alert if: self-attribution spikes, phantom agents,
    attribution without matching DAG vertices
```

**Applications**: Detecting ghost authorship in clinical trials
(healthSpring), detecting automated attribution farming (any spring),
detecting unauthorized data access via provenance audit trail.

### 3.8 sweetGrass + coralReef + barraCuda: Shader Provenance

**Track the full lifecycle of sovereign math operations.**

```
1. barraCuda authors a WGSL shader   → agent: "did:eco:barracuda"
2. coralReef compiles to SPIR-V     → agent: "did:eco:coralreef"
3. ToadStool dispatches to GPU      → agent: "did:eco:toadstool:gpu-0"
4. Spring consumes result           → agent: "did:eco:alice"
5. sweetGrass creates braid         → full compute provenance chain
```

Every math operation can trace back to shader source, compilation,
hardware, and consumer — fully sovereign, no vendor lock-in.

---

## 4. Novel Spring Compositions

These are higher-order patterns that emerge from combining sweetGrass
with multiple primals simultaneously.

### 4.1 Fair Reward Pipeline (sweetGrass + sunCloud)

**Springs**: any + sweetGrass + LoamSpine + sunCloud

Attribution braids anchored to LoamSpine become the input for sunCloud's
fair reward distribution. The complete flow:

```
1. Spring produces results        → rhizoCrypt session
2. Session dehydrates             → sweetGrass creates attributed braids
3. Braids anchor to LoamSpine     → permanent attribution record
4. sunCloud reads braids          → computes fair payment shares
5. Payment distributed            → proportional to attribution weights
```

This is the "code to cash" pipeline — every contributor from data
collector to GPU provider gets fair compensation based on their
actual contribution.

### 4.2 Cross-Spring Attribution Graph

**Springs**: wetSpring + airSpring + sweetGrass + Songbird

When data flows between springs, sweetGrass tracks the cross-domain
derivation chain. Per the `CROSS_SPRING_DATA_FLOW_STANDARD`, time
series flowing through the trio get their `source` field replaced
with a sweetGrass braid reference.

```
1. wetSpring:  braid.create { entity: soil_microbiome_data }     → braid_a
2. airSpring:  braid.create { entity: irrigation_model,
                              derived_from: [braid_a] }          → braid_b
3. sweetGrass: provenance.lineage { braid_id: braid_b }
   → { chain: [braid_b ← braid_a], agents: [wetSpring_team, airSpring_team] }
```

Attribution propagates across spring boundaries. If airSpring's
irrigation model wins an award, wetSpring's data collectors are
automatically credited through the derivation chain.

### 4.3 Regulatory Audit Package

**Springs**: healthSpring/wetSpring/airSpring + sweetGrass + LoamSpine + BearDog

For regulated domains (HIPAA, EPA, FDA), sweetGrass can produce a
complete audit package:

```
1. All experiment steps attributed (braids)
2. All braids BearDog-signed (tamper-evident)
3. All braids LoamSpine-anchored (immutable)
4. PROV-O export for regulator  (standards-compliant)
5. Privacy levels applied       (redaction per audience)
```

The result is an unforgeable, standards-compliant provenance chain
that any regulator can verify independently.

**Domain examples**:
- **healthSpring**: HIPAA audit — every data access attributed, consent
  verified, access logs immutable
- **wetSpring**: EPA PFAS compliance — every analytical step attributed,
  instrument calibration provenance included
- **airSpring**: Water rights audit — irrigation decisions traced back
  to weather data, ET₀ model, soil measurements

### 4.4 Collaborative Game Content Attribution

**Springs**: ludoSpring + sweetGrass + rhizoCrypt + petalTongue

Game content creation involves multiple contributors across domains —
artists, mechanic designers, level builders, AI balance agents, playtesters.
sweetGrass tracks the full creative provenance:

```
1. Artist creates tileset          → braid (role: Creator)
2. Mechanic designer uses tiles    → braid (derived_from: tileset, role: Creator)
3. AI suggests balance tweaks      → braid (role: Analyst, low weight)
4. Playtester validates            → braid (role: Validator)
5. Level published                 → final braid with all derivations
6. petalTongue: credit roll visualization from provenance graph
```

The scyBorg layer adds license metadata (`CC-BY-SA`, `AGPL-3.0`).
Creative Commons attribution is automatically generated from the
braid's agent list.

### 4.5 Reproducibility Certificate

**Springs**: any + sweetGrass + rhizoCrypt + LoamSpine + BearDog

A "reproducibility certificate" proves that a published result can be
reproduced from its inputs:

```
1. Original experiment: braid_original
   → agents, inputs, computation steps, hardware, software versions
2. Reproduction attempt: braid_reproduction
   → derived_from: [braid_original], same inputs, same or different hardware
3. Comparison:
   provenance.lineage { braid_id: braid_reproduction }
   → shows exact divergence point (if any) between original and reproduction
4. Certificate:
   braid.commit → LoamSpine
   → permanent record: "braid_reproduction reproduces braid_original"
```

**Applications**: Journal reproducibility badges (wetSpring, hotSpring),
certified calibration (groundSpring), validated clinical protocols
(healthSpring).

### 4.6 Multi-Spring Ecosystem Attribution Map

**Springs**: all + sweetGrass + Songbird + petalTongue

An ecosystem-wide query across all springs:

```
1. Songbird discovers all sweetGrass instances
2. provenance.graph { agent: "did:eco:alice" }
   → all braids across all springs involving this agent
3. petalTongue renders a unified attribution map:
   - wetSpring: 12 braids (taxonomy, PFAS)
   - airSpring: 4 braids (irrigation)
   - neuralSpring: 8 braids (model training)
   - ludoSpring: 3 braids (game mechanics)
   → total attribution share: 0.23 across ecosystem
```

This is the "researcher portfolio" pattern — a single view of all
contributions across all domains, automatically derived from provenance.

### 4.7 Consent-Aware Data Marketplace

**Springs**: any + sweetGrass + LoamSpine + BearDog + rhizoCrypt

Data producers can share data with attribution and consent controls:

```
1. Producer: braid.create { entity: dataset, privacy: "Attributed" }
2. Producer: braid.commit → LoamSpine (permanent offer)
3. Consumer: discovers braid via Songbird
4. Consumer: rhizoCrypt slice { mode: "Consignment", conditions: { attribution_required: true } }
5. Consumer uses data → creates derived braid
   → automatic attribution back to producer through derivation chain
```

The producer is guaranteed attribution for any downstream use. The
privacy level controls what the consumer can see. This is the foundation
for fair data economics.

---

## 5. Integration Patterns for Springs

### Minimal Integration (standalone sweetGrass only)

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
let braid = bridge.capability_call("provenance", "create_braid", &json!({
    "activity": { "type": "experiment_run" },
    "agents": [{ "did": agent_did, "role": "Creator" }],
    "entity": { "data": result_hash, "mime_type": "application/json" }
}))?;
```

The spring never imports sweetGrass directly. It discovers the capability
at runtime. If sweetGrass is not running, the call fails gracefully.

### Full Trio Integration

Use the same `NeuralBridge` for all trio operations:

```rust
let bridge = NeuralBridge::discover()?;

// Ephemeral work in rhizoCrypt
bridge.capability_call("dag", "create_session", &session_args)?;
bridge.capability_call("dag", "append_vertex", &vertex_args)?;

// Dehydrate and commit
bridge.capability_call("dag", "dehydrate", &dehydrate_args)?;
bridge.capability_call("commit", "session", &commit_args)?;

// Attribution via sweetGrass
bridge.capability_call("provenance", "create_braid", &braid_args)?;
```

### Deploy Graph (biomeOS orchestration)

For automated workflows, use the `provenance_pipeline.toml` graph:

```rust
bridge.capability_call("graph", "execute", &json!({
    "graph": "provenance_pipeline",
    "params": {
        "SESSION_ID": session_id,
        "AGENT_DID": agent_did,
        "EXPERIMENT_ID": experiment_id,
        "NICHE": "wetspring"
    }
}))?;
```

---

## 6. What sweetGrass Does NOT Do

| Concern | Who Handles It |
|---------|---------------|
| Ephemeral working state | rhizoCrypt (dag.*) |
| Permanent storage | LoamSpine (commit.*/spine.*) |
| Content blob storage | NestGate (storage.*) |
| Signing / encryption | BearDog (crypto.*) |
| Discovery / networking | Songbird (discovery.*) |
| Compute dispatch | ToadStool (compute.*) |
| Visualization | petalTongue (visualization.*) |
| AI inference | Squirrel (ai.*) |
| Security monitoring | skunkBat (security.*) |
| Orchestration | biomeOS (Neural API) |
| Reward distribution | sunCloud (reward.*) |

sweetGrass answers "who did what?" Everything else is discovered at
runtime and composed by biomeOS. Complexity through coordination,
not through coupling.

---

## 7. scyBorg: License-Aware Attribution

sweetGrass includes the scyBorg module for Creative Commons and
open-source license metadata on braids:

| Type | Purpose |
|------|---------|
| `ContentCategory` | Code, GameMechanics, CreativeContent, Reserved |
| `LicenseId` | CC-BY-4.0, CC-BY-SA-4.0, AGPL-3.0-only, MIT, etc. |
| `LicenseExpression` | SPDX expressions (e.g. `MIT OR Apache-2.0`) |
| `AttributionNotice` | Auto-generated attribution text from braid agents |

```
braid.create {
  agents: [...],
  metadata: {
    "scyborg.license": "CC-BY-SA-4.0",
    "scyborg.content_category": "CreativeContent"
  }
}
```

The `AttributionCalculator` produces human-readable attribution notices
from braid provenance — the "CC-BY line" generated automatically from
the contribution record.

**Applications**: Open-source credit (all springs), creative content
licensing (ludoSpring), dataset licensing (wetSpring, hotSpring),
model licensing (neuralSpring).

---

## 8. Content Convergence (Proposed — v0.8.x)

When independent agents produce braids with the same content hash via different
provenance paths, sweetGrass will capture this as **content convergence** rather
than silently overwriting the earlier index entry.

| Concept | Description |
|---------|-------------|
| `ContentConvergence` | Primary braid + all convergent arrivals for a content hash |
| `ConvergentArrival` | Agent, timestamp, and derivation path for each convergent path |
| `convergence.query` | New JSON-RPC method to query convergence records |
| `convergence.agents` | List agents who independently converged on same content |
| `convergence.statistics` | Aggregate convergence metrics |

**Why it matters for Springs**: Convergence is a reproducibility signal. When your
Spring and another Spring independently produce the same content hash, sweetGrass
will record both paths and their intersection — enabling cross-Spring validation
and reproducibility analysis without additional coordination.

**Participation**: See `CONTENT_CONVERGENCE_EXPERIMENT_GUIDE.md` and ISSUE-013
in `SPRING_EVOLUTION_ISSUES.md`.

**Full spec**: `sweetGrass/specs/CONTENT_CONVERGENCE.md`
