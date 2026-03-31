# 🔗 Inter-Primal Interactions - Production Implementation Plan

**Based on RootPulse Architecture**  
**Status**: Phase 1 & 2 Complete — Phase 3 Provenance Trio Validated — Phase 4 Composition Decomposition (March 31, 2026)  
**Date**: March 31, 2026 (updated from March 14, 2026)

---

## 🎯 Purpose

This document translates the **RootPulse white paper concepts** into **concrete implementation plans** for inter-primal coordination. Phase 1 and 2 primals are production-ready. Now we plan their orchestrated interactions.

---

## ✅ Current Status: Phase 1 & 2 Complete!

### Production-Ready Primals

| Primal | Status | Version | Role |
|--------|--------|---------|------|
| **BearDog** | ✅ Production | v0.15.0 | Genetic lineage, BirdSong encryption |
| **Songbird** | ✅ Production | v3.6 | Encrypted UDP discovery |
| **biomeOS** | ✅ 85% Ready | Infrastructure | Orchestration, health monitoring |
| **PetalTongue** | ⏳ Ready for Integration | - | Visualization UI |

**Key Achievement**: Songbird v3.6 + BearDog v0.15.0 = **Working encrypted auto-trust!** 🎊

---

## 🌳 RootPulse Vision: Emergent Coordination

### Core Principle

> **"Primals don't know about RootPulse. BiomeOS coordinates them, and version control emerges."**

This applies to **all** inter-primal interactions:
- Primals provide **primitive capabilities**
- biomeOS coordinates them into **higher-order behaviors**
- Complex systems **emerge** from simple composition

### The Actors (From RootPulse)

```
🔐 rhizoCrypt = Piano      (ephemeral workspace, DAG present/future)
🦴 LoamSpine  = Drums      (immutable history, linear past)
🏰 NestGate   = Bass       (content-addressed storage)
🐻 BearDog    = Lead       (security, genetic lineage)
🌱 SweetGrass = Strings    (semantic attribution)
🎵 Songbird   = Conductor  (discovery, coordination)
```

**biomeOS** is the composer — writes the symphony (coordination patterns).

---

## 🎼 Current Working Interactions (Phase 1 & 2)

### 1. Songbird ↔ BearDog (Encrypted Discovery)

**Status**: ✅ **PRODUCTION WORKING** (Jan 3, 2026)

**Flow**:
```
Songbird v3.6
  ↓ Create identity payload
  ↓ HTTP POST /api/v2/birdsong/encrypt
BearDog v0.15.0
  ↓ ChaCha20-Poly1305 encryption
  ↓ Return ciphertext + nonce
Songbird
  ↓ Build BirdSongPacket v2
  ↓ UDP multicast 239.255.0.1:4200
Network
  ↓ Receiving towers
Songbird (Receiver)
  ↓ Parse, check family_id
  ↓ HTTP POST /api/v2/birdsong/decrypt
BearDog
  ↓ Decrypt, return plaintext
Songbird
  ↓ Parse identity, evaluate trust
  ↓ Auto-trust if same family!
```

**Implemented In**:
- Songbird: `songbird-orchestrator-v3.6-api-wrapper`
- BearDog: `beardog-server-v0.15.0-with-v2-api`
- Protocol: `wateringHole/birdsong/BIRDSONG_PROTOCOL.md`

**Success Metrics**:
- ✅ Encryption working
- ✅ Base64 serialization correct
- ✅ UDP multicast transmission
- ✅ Cross-tower discovery
- ✅ Auto-trust within family

---

### 2. biomeOS ↔ All Primals (Health Monitoring)

**Status**: ✅ **INFRASTRUCTURE COMPLETE** (Jan 3, 2026)

**Flow**:
```
biomeOS PrimalHealthMonitor
  ↓ Every 30s
  ↓ HTTP GET /api/v1/health (BearDog, Songbird, etc.)
Primal
  ↓ Return health status
biomeOS
  ↓ Track state (Healthy/Degraded/Unhealthy)
  ↓ Automatic recovery attempts
  ↓ SSE events to PetalTongue
```

**Implemented In**:
- biomeOS: `crates/biomeos-core/src/primal_health.rs`
- Integration: `crates/biomeos-api/src/state.rs`
- Tests: 6/6 passing

**Success Metrics**:
- ✅ Continuous health checks
- ✅ State tracking with thresholds
- ✅ Automatic recovery
- ✅ Production-grade patterns

---

### 3. biomeOS ↔ PetalTongue (Real-Time Events)

**Status**: ✅ **API READY** (Waiting for PetalTongue integration)

**Flow**:
```
biomeOS API
  ↓ Discover primals
  ↓ Monitor health changes
  ↓ Detect topology changes
  ↓ SSE /api/v1/events/stream
PetalTongue
  ↓ EventSource subscription
  ↓ Receive events:
    - PrimalDiscovered
    - HealthChanged
    - TopologyChanged
    - FamilyJoined
    - TrustUpdated
  ↓ Update visualization in real-time
```

**Implemented In**:
- biomeOS: `crates/biomeos-api/src/handlers/events.rs`
- Events: 6 types with change detection
- Documentation: `docs/jan3-session/ENHANCED_SSE_EVENTS_JAN_3_2026.md`

**Success Metrics**:
- ✅ SSE endpoint live
- ✅ 6 event types
- ✅ Change detection (5s interval)
- ⏳ PetalTongue integration pending

---

## 🚀 Planned Interactions (Phase 3)

### 4. rhizoCrypt ↔ LoamSpine (Dehydration)

**Status**: ✅ **VALIDATED** (March 13, 2026 — live trio e2e test)

**Concept** (From RootPulse):
- **rhizoCrypt**: Fast ephemeral workspace (DAG, present/future)
- **LoamSpine**: Immutable linear history (past)
- **Dehydration**: Temporal collapse from DAG → Linear

**Flow**:
```
rhizoCrypt Session
  ↓ Lock-free concurrent ops
  ↓ DAG of vertices
  ↓ Merkle proofs at any point
  ↓ DEHYDRATE command
rhizoCrypt
  ↓ Compute Merkle root
  ↓ Create dehydration summary
  ↓ Attestations from all agents
LoamSpine
  ↓ Append linear entry
  ↓ Immutable historical record
  ↓ Inclusion proofs available
```

**Validated**:
- LoamSpine v0.9.5 (`session.commit` + `permanent-storage.commitSession` compat, `DispatchOutcome`, `StreamItem` streaming) ✅
- rhizoCrypt v0.13.0 dehydration produces `DehydrationSummary` ✅
- Wire format aligned: rhizoCrypt → LoamSpine serde contract validated ✅
- biomeOS `rootpulse_commit.toml` graph orchestrates the full workflow ✅

**Use Cases**:
- Version control commits (RootPulse)
- Multi-agent collaboration
- Scientific experiment logging
- Game state snapshots

---

### 5. NestGate ↔ LoamSpine (Content Storage)

**Status**: ⏳ **PLANNED**

**Concept** (From RootPulse):
- **NestGate**: Content-addressed storage (trees, blobs)
- **LoamSpine**: Commit history (references to content)

**Flow**:
```
User commits
  ↓ Hash working directory → tree
NestGate
  ↓ store_tree(tree) → tree_hash
  ↓ store_blob(file) → blob_hash
Create commit object
  ↓ { tree: tree_hash, message, author, timestamp }
BearDog
  ↓ sign(commit) → signature
LoamSpine
  ↓ append(commit, signature) → commit_hash
```

**Required**:
- NestGate implementation
- LoamSpine implementation (v0.9.5 -- `entry.append`, `proof.generate_inclusion`)
- biomeOS commit coordinator

**Design Notes**:
- NestGate doesn't know about "commits"
- LoamSpine doesn't know about "files"
- Coordination pattern makes version control emerge!

---

### 6. SweetGrass ↔ LoamSpine (Attribution)

**Status**: ✅ **VALIDATED** (March 13, 2026 — SweetGrass v0.7.3, `braid.commit` + `contribution.recordDehydration`, 746 tests, 94% coverage)

**Concept** (From RootPulse):
- **SweetGrass**: Semantic attribution (who contributed what)
- **LoamSpine**: Historical record (when it happened)

**Flow**:
```
Commit created
  ↓ Analyze semantic changes
SweetGrass
  ↓ record_contribution({
       author: DID,
       entity: "Module::function",
       change_type: Refactor,
       timestamp: now()
     })
  ↓ create_braid(author → module)
LoamSpine
  ↓ append_commit(commit_hash)
Query later
  ↓ "Who created this module?"
SweetGrass
  ↓ traverse braids → author
  ↓ with timestamp from LoamSpine
```

**Validated**:
- `contribution.recordDehydration` accepts rhizoCrypt `DehydrationSummary` ✅
- `braid.create` with data_hash, mime_type, size ✅
- sweetGrass accommodates rhizoCrypt output through optional/defaulted fields ✅
- biomeOS `rootpulse_commit.toml` includes attribution phase ✅

**Benefits**:
- **Semantic** attribution (not line-based!)
- Tracks contributions to features, not just files
- Persistent across refactors

---

### 7. Songbird ↔ Songbird (Federation)

**Status**: ⏳ **PLANNED** (Infrastructure ready)

**Concept**:
- Multi-tower discovery
- Cross-family routing
- Federated repository discovery

**Flow**:
```
Songbird Tower 1
  ↓ Broadcast BirdSongPacket (family A)
  ↓ UDP multicast
Songbird Tower 2
  ↓ Receive, check family_id
  ↓ Same family → decrypt → auto-trust
  ↓ Different family → ignore
Songbird Tower 3 (Bridge)
  ↓ Member of both families
  ↓ Can route between families
  ↓ Enables federation!
```

**Required**:
- Multi-family credential management
- Routing protocol
- Policy engine (who can bridge?)

**Use Cases**:
- Multi-organization collaboration
- Public ↔ private family bridges
- Federated code hosting

---

### 8. biomeOS ↔ All Primals (Retry & Circuit Breaker)

**Status**: ✅ **INFRASTRUCTURE COMPLETE** (Jan 3, 2026)

**Flow**:
```
biomeOS RetryPolicy
  ↓ Exponential backoff (100ms, 200ms, 400ms...)
  ↓ Random jitter (prevent thundering herd)
  ↓ Max 3 attempts
Primal API call
  ↓ If transient failure → retry
  ↓ If success → reset counter

biomeOS CircuitBreaker
  ↓ Track failures per primal
  ↓ If 5 failures → OPEN circuit
  ↓ Fail fast for 30s
  ↓ Then HALF-OPEN (test recovery)
  ↓ If 2 successes → CLOSED
```

**Implemented In**:
- biomeOS: `crates/biomeos-core/src/retry.rs`
- Tests: 8/8 passing
- Production-ready patterns

**Benefits**:
- ✅ Handles transient failures
- ✅ Prevents cascade failures
- ✅ Automatic recovery
- ✅ 10-100x faster than naive retry

---

## 🎨 Composition Patterns (From RootPulse)

### Pattern 1: Sequential Composition

**When**: Steps depend on previous results

**Example**: Commit workflow
```rust
async fn commit() {
    let tree_hash = nestgate.store_tree(tree).await?;    // Step 1
    let signature = beardog.sign(&commit).await?;         // Step 2 (needs commit)
    let commit_hash = loamspine.append(commit, sig).await?; // Step 3 (needs sig)
}
```

**Applied To**:
- ✅ Songbird encryption (payload → encrypt → packet → send)
- ⏳ RootPulse commits (tree → commit → sign → append)

---

### Pattern 2: Parallel Composition

**When**: Steps are independent

**Example**: Multi-source discovery
```rust
async fn discover() {
    let (mDNS, http, env) = tokio::join!(
        songbird.discover_mdns(),     // Parallel
        http_discovery.discover(),    // Parallel
        env_discovery.discover(),     // Parallel
    );
    combine(mDNS, http, env)
}
```

**Applied To**:
- ✅ biomeOS primal discovery (multiple sources)
- ⏳ Federated repository search

---

### Pattern 3: Conditional Composition

**When**: Optional features

**Example**: Commit with optional attribution
```rust
async fn commit(use_attribution: bool) {
    let commit_hash = loamspine.append(commit).await?;  // Always
    
    if use_attribution {
        sweetgrass.record(contribution).await?;  // Optional
    }
}
```

**Applied To**:
- ⏳ RootPulse with/without SweetGrass
- ⏳ CI/CD integration (ToadStool optional)

---

### Pattern 4: Feedback Composition

**When**: Decisions need context from multiple primals

**Example**: Merge resolution with AI
```rust
async fn pull_with_merge() {
    let conflicts = detect_conflicts(local, remote)?;
    
    if !conflicts.is_empty() {
        let resolution = squirrel.suggest_merge(conflicts).await?;
        apply_merge(resolution)?;
    }
    
    loamspine.append(merged_commit).await?;
}
```

**Applied To**:
- ⏳ Intelligent merge (Squirrel + LoamSpine)
- ⏳ Adaptive health monitoring (biomeOS + primals)

---

## 📋 Implementation Roadmap

### Phase 3.1: LoamSpine + NestGate (Core VCS)

**Timeline**: 2-3 months

**Deliverables**:
1. LoamSpine implementation (DONE -- v0.9.5)
   - Append-only log with hash chain
   - Inclusion proofs
   - Session commit + braid commit integration
   - permanent-storage.* compatibility for rhizoCrypt

2. NestGate implementation
   - Content-addressed storage
   - ZFS integration
   - Blob/tree storage

3. biomeOS coordination
   - Commit workflow
   - Push/pull patterns
   - Object transfer

**Milestone**: Basic version control working!

---

### Phase 3.2: rhizoCrypt Integration (Performance)

**Timeline**: 1-2 months (rhizoCrypt v0.13.0 exists!)

**Deliverables**:
1. Dehydration protocol
   - rhizoCrypt → LoamSpine bridge
   - Temporal collapse logic
   - Multi-agent attestations

2. Session management
   - Create ephemeral sessions
   - Lock-free operations
   - Merkle proof generation

3. Performance optimization
   - 10-100x faster than Git
   - Real-time collaboration

**Milestone**: High-performance VCS with collaborative features!

---

### Phase 3.3: SweetGrass Attribution (Semantic)

**Timeline**: Ready (SweetGrass v0.7.3 — 746 tests, 94% coverage, Provenance Trio coordination, `braid.commit` + `contribution.recordDehydration`, ecoBin, AGPL-3.0-only)

**Deliverables**:
1. Semantic analysis
   - Code entity extraction
   - Change type classification
   - Contribution tracking

2. Braid creation
   - Author → module relationships
   - Persistent across refactors
   - Query interface

3. biomeOS coordination
   - Integrate with commit workflow
   - Attribution UI in PetalTongue

**Milestone**: Semantic attribution working!

---

### Phase 3.4: Federation (Multi-Tower)

**Timeline**: 2-3 months

**Deliverables**:
1. Multi-family support
   - Credential management
   - Routing protocol
   - Bridge policies

2. Repository discovery
   - Federated search
   - Cross-tower push/pull
   - Trust propagation

3. Production deployment
   - Multi-tower testing
   - Federation examples

**Milestone**: True federated version control!

---

## 🏆 Success Criteria

### Technical Metrics

| Metric | Target | Phase 1/2 Status |
|--------|--------|------------------|
| **Discovery Latency** | < 100ms | ✅ Working |
| **Encryption** | < 10ms | ✅ Working |
| **Health Checks** | < 30s interval | ✅ Working |
| **Auto-Trust** | 100% within family | ✅ Working |
| **Fault Tolerance** | Circuit breaker | ✅ Complete |
| **Real-time Events** | < 5s latency | ✅ Complete |

### Phase 3 Targets

| Metric | Target |
|--------|--------|
| **Commit Speed** | 10-100x faster than Git |
| **Dehydration** | < 1s for typical session |
| **Attribution** | Semantic entity tracking |
| **Federation** | Cross-tower discovery < 1s |

---

## 💡 Design Principles (From RootPulse)

### 1. Interface Segregation

**Principle**: Each primal exposes narrow, focused interfaces

**Example**:
```rust
// LoamSpine doesn't know about "commits"
pub trait AppendOnly {
    async fn append(&self, entry: Entry, proof: Signature) -> Result<Hash>;
    async fn get(&self, hash: Hash) -> Result<Entry>;
}
```

**Benefits**:
- Reusable across applications
- Easy to test
- Clear boundaries

---

### 2. Dependency Inversion

**Principle**: Primals depend on abstract capabilities, not concrete implementations

**Example**:
```rust
// Good: Abstract dependency
impl LoamSpine {
    fn new(storage: impl BlobStorage) -> Self {
        // Works with NestGate, S3, filesystem, etc.
    }
}
```

**Benefits**:
- Swap implementations
- Mock for testing
- Flexible deployment

---

### 3. Message Passing

**Principle**: Primals communicate via messages, not shared state

**Example**:
```rust
async fn commit(biome: &BiomeOS, commit: Commit) {
    biome.loamspine().send(Message::Append(commit)).await?;
    biome.sweetgrass().send(Message::RecordAttribution(commit)).await?;
}
```

**Benefits**:
- No locks
- No race conditions
- Inherently concurrent

---

### 4. Single Responsibility

**Principle**: Each primal does ONE thing

**Examples**:
- **LoamSpine**: ONLY immutable history
- **NestGate**: ONLY content storage
- **BearDog**: ONLY security
- **SweetGrass**: ONLY attribution

**Benefits**:
- Easy to understand
- Easy to test
- Easy to maintain

---

## 🔗 Integration Points

### Current (Phase 1 & 2)

1. **Songbird → BearDog**
   - API: `/api/v2/birdsong/encrypt`, `/api/v2/birdsong/decrypt`
   - Protocol: BirdSong v2 (documented)
   - Status: ✅ Working

2. **biomeOS → All Primals**
   - API: `/api/v1/health`, `/api/v1/identity`
   - Protocol: HTTP REST
   - Status: ✅ Working

3. **biomeOS → PetalTongue**
   - API: `/api/v1/events/stream` (SSE)
   - Protocol: Server-Sent Events
   - Status: ✅ Ready

---

### Future (Phase 3)

4. **rhizoCrypt → LoamSpine**
   - API: `dag.dehydrate` → `permanence.commit_session` (JSON-RPC 2.0)
   - Protocol: Temporal collapse (`DehydrationSummary` wire format)
   - Status: ✅ Validated (March 13, 2026)

5. **NestGate → LoamSpine**
   - API: Content storage (TBD)
   - Protocol: Content-addressed references
   - Status: ⏳ Planned

6. **SweetGrass → LoamSpine**
   - API: `contribution.recordDehydration`, `braid.create` (JSON-RPC 2.0)
   - Protocol: W3C PROV-O semantic braids
   - Status: ✅ Validated (March 13, 2026)

---

## 📚 Documentation References

### Implemented

- **BearDog**: `wateringHole/btsp/BEARDOG_TECHNICAL_STACK.md`
- **BirdSong**: `wateringHole/birdsong/BIRDSONG_PROTOCOL.md`
- **biomeOS Infrastructure**: `biomeOS/docs/jan3-session/INFRASTRUCTURE_COMPLETE_JAN_3_2026.md`
- **Adaptive Client**: `biomeOS/crates/biomeos-core/src/adaptive_client.rs`
- **Health Monitoring**: `biomeOS/crates/biomeos-core/src/primal_health.rs`
- **Retry & Circuit Breaker**: `biomeOS/crates/biomeos-core/src/retry.rs`

### Conceptual

- **RootPulse Architecture**: `whitePaper/RootPulse/02_ARCHITECTURE.md`
- **Primal Composition**: `whitePaper/RootPulse/03_PRIMAL_COMPOSITION.md`
- **DAG vs Linear**: `whitePaper/RootPulse/04_DAG_VS_LINEAR.md`

---

## 🎯 Next Steps

### Immediate (Next Session)

1. **Multi-family validation** - Prove deterministic behavior across families
2. **PetalTongue integration** - Connect ecosystem visualization to live trio
3. **ludoSpring continuous coordination** - 60 Hz game engine via ContinuousExecutor

### Short-term (1-2 months)

1. **NestGate ↔ LoamSpine** - Content-addressed storage backing immutable history
2. **Cross-Spring provenance** - wetSpring, airSpring consuming provenance_pipeline.toml
3. **Songbird federation** - Multi-tower discovery and routing

### Completed (March 13, 2026)

1. ✅ **LoamSpine v0.9.5** - Immutable linear history, 1,226 tests, 90%+ function coverage, `DispatchOutcome`, `StreamItem` streaming, `OrExit`
2. ✅ **rhizoCrypt ↔ LoamSpine dehydration** - Validated end-to-end with live binaries
3. ✅ **sweetGrass attribution** - `contribution.recordDehydration` + `braid.create` validated
4. ✅ **Provenance trio e2e** - Full 6-phase RootPulse commit workflow validated
5. ✅ **ludoSpring exp052** - Game session provenance via trio (37/37 checks)
6. ✅ **biomeOS ContinuousExecutor** - 60 Hz tick coordination (15 tests)

---

**Status**: **Phase 3 Provenance Trio Validated (March 13, 2026)**  
**Foundation**: Production-grade infrastructure ✅  
**Trio**: rhizoCrypt + LoamSpine + sweetGrass validated end-to-end ✅  
**Next**: NestGate integration, federation, cross-Spring provenance

🌳 **The ecosystem is ready to evolve!** 🌸

---

## Plasmodium: Over-NUCLEUS Collective Coordination (February 2026)

When two or more NUCLEUS instances bond **covalently** (shared `family_seed`, BirdSong mesh, genetic trust), they form a collective organism called **Plasmodium** -- named after the slime mold *Physarum polycephalum*.

Plasmodium is the emergent coordination layer in biomeOS that:
- Aggregates capabilities across all bonded gates into a **collective view**
- Routes workloads to the best gate based on **capability, resources, and load**
- Operates with **no central brain** -- any gate can query the collective
- Degrades gracefully when gates go offline (**sclerotium** state)

### Relationship to Inter-Primal Interactions

Plasmodium builds on the existing inter-primal coordination primitives:
- **Songbird** `mesh.peers` / `mesh.status` for gate discovery
- **BearDog** genetic lineage for trust verification
- **AtomicClient** JSON-RPC for all IPC
- **BirdSong** encrypted UDP for heartbeat/pulse coordination

Plasmodium is NOT a new primal -- it is a biomeOS coordination pattern that uses existing primal primitives exclusively.

**Full specification**: `phase2/biomeOS/specs/PLASMODIUM_OVER_NUCLEUS_SPEC.md`  
**Implementation**: `biomeos-core::plasmodium` module  
**CLI**: `biomeos plasmodium status|gates|models`

---

---

## Phase 4: Composition Decomposition (March 31, 2026)

### Status: Active — primalSpring Phase 23f

primalSpring has decomposed the monolithic interactive gateway into 7 independently deployable compositions, each validating a specific subsystem:

| ID | Composition | Primals | Status |
|----|------------|---------|--------|
| C1 | Render Standalone | biomeOS + petalTongue | Partial (dashboard renders, export works, scene stores) |
| C2 | Narration AI | biomeOS + Squirrel | Partial (query works, Ollama routing needs wiring) |
| C3 | Session | biomeOS + Tower + esotericWebb | Pass (full lifecycle validated) |
| C4 | Game Science | biomeOS + Tower + ludoSpring | Pass (flow, Fitts, WFC, engagement validated) |
| C5 | Persistence | biomeOS + Tower + NestGate | Partial (store/retrieve work, listing needs fix) |
| C6 | Proprioception | biomeOS + petalTongue | Partial (subscribe works, poll/apply need IPC evolution) |
| C7 | Full Interactive | All NUCLEUS + all subsystems | Partial (blocked by BM-04 capability registration) |

### Critical Interaction Gaps Identified

| Gap | Interaction | Impact |
|-----|------------|--------|
| **BM-04** | biomeOS → All Primals (capability discovery) | Primals starting after biomeOS are invisible to Neural API. Blocks capability routing in all multi-primal graphs. |
| **RC-01** | rhizoCrypt → biomeOS (registration) | TCP-only transport, no UDS socket. Cannot participate in standard compositions. |
| **LS-03** | loamSpine → biomeOS (startup) | Tokio nested runtime panic. Cannot start. Blocks all Provenance Trio interactions. |
| **PT-01** | petalTongue → biomeOS (discovery) | Socket not in standard `biomeos/` directory. Not discoverable by biomeOS scan. |
| **SQ-01** | Squirrel → biomeOS (discovery) | Abstract socket only. Invisible to `readdir()`. Not discoverable by filesystem scan. |

### toadStool S169 Overstep Resolution Impact

toadStool's S169 cleanup removed 30+ overstepping JSON-RPC methods that were
proxying concerns belonging to Squirrel (AI), coralReef (shader compile),
biomeOS (discovery/deploy), and songBird (HTTP). This cleanup:

- **Clarified deploy graphs**: Springs must now route AI to Squirrel, shader compile to coralReef directly
- **Reduced toadStool to its core**: hardware inventory + compute dispatch (`shader.dispatch`, `compute.*`)
- **Exposed hidden couplings**: Some springs may have been routing through toadStool as a "convenience hub" — they must now use proper capability routing

See `wateringHole/handoffs/TOADSTOOL_S169_OVERSTEP_CLEANUP_DEEP_DEBT_HANDOFF_MAR31_2026.md` for full details.

### ludoSpring V37.1 Validation Results

ludoSpring's live plasmidBin validation (experiments 084-098) achieved 95/141 checks (67.4%):

- **barraCuda math pipeline**: 42/42 (tensor, activation, stats) — but Fitts/Hick formulas diverge from Python baselines
- **NUCLEUS game session**: Working at 60Hz tick cycle
- **Session provenance**: Blocked by RC-01 (rhizoCrypt UDS) and LS-03 (loamSpine panic)
- **Projected with fixes**: 130/141 (92.2%)

### Related Documents

- `primalSpring/docs/PRIMAL_GAPS.md` — 32-gap registry with severity, impact, and fix paths
- `wateringHole/PRIMAL_RESPONSIBILITY_MATRIX.md` V2 — Tiered evolution actions
- `wateringHole/IPC_COMPLIANCE_MATRIX.md` v1.3 — Capability registration compliance
- `wateringHole/SPRING_EVOLUTION_ISSUES.md` — ISSUE-011 through ISSUE-015

---

*"Primals are the instruments. biomeOS is the composer. Together, they create symphonies."*

