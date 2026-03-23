<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# LoamSpine Leverage Guide — Standalone, Trio, and Ecosystem Compositions

**Date**: March 17, 2026
**Primal**: LoamSpine v0.9.6
**Audience**: All springs, all primals, biomeOS integrators
**Status**: Active

---

## Purpose

This document describes how LoamSpine can be leveraged — alone and in
composition with other primals — by springs and ecosystem consumers. Each
primal in the ecosystem will produce an equivalent guide. Together, these
guides form a combinatorial recipe book for emergent behaviors.

LoamSpine provides **selective, immutable permanence** via append-only
hash-chained spines, Loam Certificates for memory-bound ownership, and
cryptographic inclusion proofs. It is the "permanent ledger" of the
ecosystem — the place where ephemeral work graduates to history.

**Philosophy**: Ephemeral work earns permanence by consent. LoamSpine
never captures automatically — you choose what matters, and once
committed, history cannot be rewritten.

---

## IPC Methods (Semantic Naming)

All methods follow `{domain}.{operation}[.{variant}]` per the
[Semantic Method Naming Standard](./SEMANTIC_METHOD_NAMING_STANDARD.md).

| Method | What It Does |
|--------|-------------|
| `spine.create` | Create a sovereign append-only ledger (owner DID, metadata) |
| `spine.get` | Retrieve spine metadata (height, tip, owner, state) |
| `spine.seal` | Seal a spine — no further entries, immutable forever |
| `entry.append` | Append an immutable entry to a spine (15+ entry types) |
| `entry.get` | Retrieve an entry by its Blake3 hash |
| `entry.get_tip` | Get the latest entry (chain head) |
| `certificate.mint` | Mint a memory-bound ownership certificate |
| `certificate.transfer` | Transfer certificate ownership to another DID |
| `certificate.loan` | Loan a certificate with time-limited access and terms |
| `certificate.return` | Return a loaned certificate (end loan period) |
| `certificate.get` | Query certificate state and history |
| `certificate.verify` | Verify certificate integrity and chain of custody |
| `certificate.lifecycle` | Full ownership and loan history for a certificate |
| `certificate.hold` | Hold a certificate in escrow with transfer conditions |
| `certificate.release` | Release a held certificate (conditions met) |
| `certificate.cancel_escrow` | Cancel an escrow hold (return to previous state) |
| `slice.anchor` | Anchor borrowed state at a waypoint spine |
| `slice.checkout` | Check out a slice from a waypoint |
| `slice.record_operation` | Record an operation within a waypoint |
| `slice.depart` | Depart from a waypoint (with departure reason) |
| `proof.generate_inclusion` | Generate a cryptographic inclusion proof for an entry |
| `proof.verify_inclusion` | Verify an inclusion proof (entry exists in spine) |
| `commit.session` | Commit a rhizoCrypt dehydration summary permanently |
| `braid.commit` | Commit a sweetGrass attribution braid permanently |
| `health.check` | Service status, backend, and uptime |
| `health.liveness` | Liveness probe |
| `health.readiness` | Readiness probe |
| `capability.list` | List all available capabilities and their status |

**Compatibility** (rhizoCrypt wire format):

| Method | What It Does |
|--------|-------------|
| `permanent-storage.commitSession` | Commit via rhizoCrypt's native format |
| `permanent-storage.verifyCommit` | Verify a commit by entry hash |
| `permanent-storage.getCommit` | Retrieve a commit as JSON |
| `permanent-storage.healthCheck` | Health check for rhizoCrypt clients |

**Transport**: JSON-RPC 2.0 over Unix socket (primary), tarpc/bincode
(high-perf primal-to-primal), HTTP (admin/debug).

---

## 1. LoamSpine Standalone

These patterns use LoamSpine alone — no other primals required.

### 1.1 Append-Only Audit Log

**For**: Any spring that needs an immutable, tamper-evident event record.

A spine is a linear, append-only chain. Each entry links to the previous
via Blake3 hash. Once appended, entries cannot be modified or deleted.
Any break in the hash chain is detectable.

```
spine.create { owner: "did:eco:alice", metadata: { niche: "wetspring" } }
  → spine_id (UUIDv7)

entry.append { spine_id, entry_type: "DataAnchor", payload: { ... } }
  → entry_hash_a (Blake3)

entry.append { spine_id, entry_type: "DataAnchor", payload: { ... } }
  → entry_hash_b (links to entry_hash_a)

entry.get_tip { spine_id }
  → latest entry (with full chain back to genesis)
```

**Spring applications**:

| Spring | What Gets Logged Permanently |
|--------|----------------------------|
| wetSpring | DADA2 pipeline outcomes, PFAS screening results, instrument calibrations |
| airSpring | Irrigation decisions, ET₀ model parameters, sensor calibration events |
| hotSpring | EOS fit parameters, MD simulation checkpoints, lattice QCD plaquettes |
| neuralSpring | Training milestones, model checkpoints, hyperparameter selections |
| groundSpring | Calibration chain results, seismic event detections, bias corrections |
| healthSpring | Dosing decisions, PK/PD model publications, consent events |
| ludoSpring | Game release snapshots, balance patch records, tournament results |
| primalSpring | Validates LoamSpine's role in RootPulse — exp020 tests commit, exp021 tests branch+merge, exp022 tests diff+federate. |

### 1.2 Loam Certificates — Memory-Bound Ownership

**For**: Any spring managing ownership, access rights, or custodial transfer.

Certificates are memory-bound objects that represent ownership of data,
credentials, instruments, or computational resources. They carry a full
lifecycle: mint → transfer → loan → return.

```
certificate.mint {
  owner: "did:eco:alice",
  certificate_type: "DataOwnership",
  metadata: { dataset: "soil-microbiome-2026-03", format: "parquet" }
}
  → certificate_id

certificate.loan {
  certificate_id,
  borrower: "did:eco:bob",
  terms: { duration: "30d", read_only: true, attribution_required: true }
}
  → loan_id (certificate now held by bob under terms)

certificate.return { certificate_id, loan_id }
  → certificate returns to alice
```

The entire certificate history (mint, every transfer, every loan) is
recorded as entries on the owner's spine — a permanent, auditable
chain of custody.

**Spring applications**:

| Spring | Certificate Use |
|--------|----------------|
| wetSpring | Specimen ownership, sequencing instrument access, reference genome custody |
| airSpring | Weather station data rights, model IP ownership, sensor calibration deeds |
| hotSpring | Simulation code ownership, HPC allocation certificates, dataset access deeds |
| neuralSpring | Model weight ownership, training data licenses, GPU allocation certificates |
| groundSpring | Sensor deployment certificates, calibration standard ownership |
| healthSpring | Patient consent certificates, clinical trial data custodianship |
| ludoSpring | Game asset ownership, mechanic IP certificates, content licenses |

### 1.3 Inclusion Proofs — Prove Without Revealing

**For**: Any spring that needs to prove a record exists without exposing
the full chain.

An inclusion proof shows that a specific entry exists within a spine at
a given position, without requiring the verifier to hold the entire spine.
The proof is a compact hash path from the entry to the tip.

```
proof.generate_inclusion { spine_id, entry_hash }
  → { entry, proof_path, tip_hash }

proof.verify_inclusion { proof_path, entry_hash, tip_hash }
  → true/false
```

**Applications**: Proving a measurement was part of a calibration chain
without revealing other measurements (groundSpring), proving a clinical
event happened without disclosing patient identity (healthSpring),
proving a game event was recorded without revealing game state
(ludoSpring), proving an irrigation decision was justified without
revealing proprietary model parameters (airSpring).

### 1.4 Sealed Archives — Immutable Forever

**For**: Any spring that needs to close a record permanently.

Sealing a spine appends a `SpineSealed` entry and transitions the spine
to an immutable state. No further entries can be appended. The sealed
spine becomes a perfect archive — its entire history is fixed.

```
spine.create { owner: "did:eco:alice" }   → spine_id
(... append entries over days, weeks, months ...)
spine.seal { spine_id }                   → sealed (SpineSealed entry appended)
entry.append { spine_id, ... }            → ERROR: spine is sealed
```

**Applications**: Closing a completed clinical trial (healthSpring),
archiving a completed field season (airSpring, groundSpring), sealing
a published game version (ludoSpring), locking a released model
(neuralSpring), finalizing a regulatory submission (wetSpring).

### 1.5 Multi-Spine Organization

**For**: Any spring managing multiple independent record chains.

Each spine is an independent ledger. Springs can create multiple spines
to organize records by experiment, dataset, time period, or certificate
domain. Spines are lightweight — creating a new one is cheap.

```
spine.create { metadata: { niche: "et0-2026-q1" } }   → spine_q1
spine.create { metadata: { niche: "et0-2026-q2" } }   → spine_q2
spine.create { metadata: { niche: "certificates" } }   → spine_certs

entry.append { spine_id: spine_q1, ... }  → separate chain
entry.append { spine_id: spine_q2, ... }  → separate chain
```

**Applications**: Per-experiment spines (any spring), per-patient
clinical chains (healthSpring), per-instrument calibration histories
(groundSpring), per-game-session audit trails (ludoSpring), per-model
training histories (neuralSpring).

### 1.6 Entry Type Taxonomy

LoamSpine defines 15+ entry types, giving structure to the ledger:

| Entry Type | Purpose |
|------------|---------|
| `Genesis` | First entry in a spine — establishes identity and ownership |
| `MetadataUpdate` | Update spine metadata without breaking the chain |
| `SessionCommit` | Anchor a rhizoCrypt dehydration (session_id, merkle_root, vertex_count) |
| `BraidCommit` | Anchor a sweetGrass attribution braid (braid_id, braid_hash) |
| `DataAnchor` | Anchor arbitrary data by content hash (Blake3, mime type, size) |
| `CertificateMint` | Record certificate creation |
| `CertificateTransfer` | Record ownership transfer |
| `CertificateLoan` | Record loan initiation with terms |
| `CertificateReturn` | Record loan completion |
| `SliceAnchor` | Anchor borrowed state at a waypoint |
| `SliceCheckout` | Record a slice checkout event |
| `SliceReturn` | Record a slice return event |
| `SliceOperation` | Record an operation within a waypoint |
| `SliceDeparture` | Record departure from a waypoint |
| `TemporalMoment` | Timestamp anchor for time-sensitive records |
| `Custom` | Extension point (type_uri + arbitrary payload) |

Springs can use `DataAnchor` for simple content permanence, `Custom`
for domain-specific structured data, and the session/braid types for
trio integration — all on the same spine.

---

## 2. LoamSpine + Trio Compositions

The **Provenance Trio** (rhizoCrypt + LoamSpine + sweetGrass) forms a
three-layer architecture:

```
sweetGrass (Attribution)      — who did what, fair contribution
      ↕
 LoamSpine (Permanence)       — immutable history, certificates
      ↕
 rhizoCrypt (Working Memory)  — ephemeral DAG, dehydration
```

LoamSpine sits at the center. It receives dehydrations from below
(rhizoCrypt) and anchors attributions from above (sweetGrass). It is
the trust anchor — the layer where history becomes unforgeable.

### 2.1 LoamSpine + rhizoCrypt: Dehydration → Permanent Commit

**The core permanence pattern.** rhizoCrypt holds ephemeral work.
When results matter, they dehydrate to LoamSpine.

```
1. (rhizoCrypt session completes)
2. dag.dehydrate { session_id }
   → { merkle_root, vertex_count, frontier, operations, agents }
3. commit.session {
     session_id, merkle_root, vertex_count,
     committer: "did:eco:alice"
   }
   → LoamSpine entry: SessionCommit (permanent, hash-chained)
   → entry_hash, entry_index, spine_id
```

The `SessionCommit` entry records the Merkle root of the entire DAG
session. Anyone holding the root can verify any vertex via
`dag.merkle_proof` against the committed root. The dehydration summary
is stored permanently; the ephemeral vertices can be garbage collected.

**Selectivity is the point**: 10,000 intermediate DAG vertices collapse
to one permanent commit. LoamSpine stores what matters; rhizoCrypt
handled what was exploratory.

**Spring applications**:
- wetSpring: 1,000 DADA2 intermediate steps → 1 permanent taxonomy commit
- hotSpring: 50,000 lattice QCD sweeps → 1 permanent EOS data point
- airSpring: Continuous ET₀ computations → daily irrigation decision commit
- neuralSpring: Millions of gradient steps → epoch checkpoint commits
- groundSpring: Thousands of raw sensor readings → permanent calibration result
- healthSpring: Iterative PK/PD modeling → final dosing recommendation commit
- ludoSpring: 60 Hz game telemetry → session outcome commit

### 2.2 LoamSpine + sweetGrass: Anchored Attribution

**Attribution that cannot be altered.** sweetGrass braids record who
contributed what. Committing them to LoamSpine makes that record permanent.

```
1. braid.create { agents: [...], activity: {...}, entity: {...} }
   → braid_id, braid_hash (content-addressed)
2. braid.commit { braid_id, spine_id, committer: "did:eco:alice" }
   → LoamSpine entry: BraidCommit (braid_id, braid_hash, subject_hash)
   → entry_hash (permanent)
```

Once a braid is committed, the attribution shares are frozen in the
hash chain. No retroactive modification of credit is possible. This is
critical for reward distribution, publication credit, and regulatory
compliance.

**Applications**: Freezing publication credit before journal submission
(wetSpring, hotSpring), locking royalty splits for game content
(ludoSpring), creating immutable clinical contribution records
(healthSpring), anchoring AI training attribution before model release
(neuralSpring).

### 2.3 LoamSpine + rhizoCrypt + sweetGrass: Full Provenance Pipeline

**The canonical composition — biomeOS orchestrates as a graph.**

```
1. dag.create_session          → ephemeral workspace (rhizoCrypt)
2. (spring work happens)       → vertices accumulate
3. dag.dehydrate               → collapse to summary (rhizoCrypt)
4. crypto.sign                 → BearDog signs the summary
5. storage.store               → NestGate stores the payload
6. commit.session              → LoamSpine commits permanently
7. contribution.record_dehydration → sweetGrass records attribution
```

From LoamSpine's perspective, step 6 is the pivotal moment — ephemeral
work crosses the permanence threshold. The entry's Blake3 hash becomes
the canonical reference for the entire pipeline's output. Steps 4, 5,
and 7 can be verified against this anchor.

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

### 2.4 LoamSpine as Cross-Trio Query Point

**LoamSpine is the natural query surface for historical provenance.**

Because both session commits and braid commits land on LoamSpine, it
can answer questions that span rhizoCrypt (what was computed) and
sweetGrass (who contributed):

```
entry.get { entry_hash }
  → SessionCommit: merkle_root, vertex_count, session_id
  → or BraidCommit: braid_id, braid_hash, subject_hash

proof.generate_inclusion { spine_id, entry_hash }
  → compact proof that this commit exists in the chain

(provenance chain query)
  → all entries for a given data hash, across session and braid commits
```

rhizoCrypt sessions may be garbage collected. sweetGrass braids may be
compressed. LoamSpine entries persist forever — they are the long-term
reference for the entire trio's output.

---

## 3. LoamSpine + Other Primals

### 3.1 LoamSpine + BearDog: Signed Immutable Records

**Every entry can be cryptographically signed before commit.**

```
entry.append { payload: { data_hash, ... } } → entry_hash
crypto.sign { data: entry_hash, signer: "did:eco:alice" }
  → signature (Ed25519)
```

Signed entries prove two things: (1) the data exists in the chain
(hash linkage), and (2) a specific identity endorsed it (signature).
Combined with inclusion proofs, this creates verifiable, non-repudiable
audit trails.

**Applications**: Signed regulatory submissions (healthSpring, wetSpring),
tamper-evident sensor logs (groundSpring, airSpring), notarized game
tournament results (ludoSpring), signed model release records
(neuralSpring).

### 3.2 LoamSpine + NestGate: Hash-Linked Blob Storage

**Entry hashes in LoamSpine can reference blobs stored in NestGate.**

```
storage.put { data: large_dataset }
  → content_hash (Blake3)

entry.append { spine_id, entry_type: "DataAnchor",
  payload: { content_hash, size: 4_200_000, mime_type: "application/parquet" }
}
  → entry_hash (the spine records *what* was stored)
```

The spine stores lightweight anchors (hashes, sizes, metadata).
NestGate stores the heavy payloads. The Blake3 hash links them
without duplication. To verify, fetch from NestGate, hash, compare
against the spine entry.

**Applications**: Large dataset permanence (wetSpring genomic data,
airSpring weather archives, hotSpring simulation outputs), model
weight archival (neuralSpring), game asset registries (ludoSpring).

### 3.3 LoamSpine + Songbird: Spine Discovery

**Other primals discover LoamSpine instances and their capabilities
via Songbird's discovery layer.**

```
discovery.announce { capability: "permanence", spine_ids: [...], metadata: {...} }
discovery.query { capability: "permanence" }
  → [ { primal: "loamspine-abc123", spines: [...] } ]
```

In a federated deployment, multiple LoamSpine instances may exist
(per-site, per-tenant). Songbird enables cross-site spine discovery
without hardcoded addresses.

**Applications**: Multi-site clinical trials discovering each site's
spine (healthSpring), federated weather station networks (airSpring),
multi-lab experiment coordination (wetSpring, hotSpring).

### 3.4 LoamSpine + petalTongue: Timeline Visualization

**petalTongue can render spines as interactive timelines and
certificate chains as ownership graphs.**

```
spine.get { spine_id }           → height, tip, metadata
entry.get_tip { spine_id }       → latest entry + chain back to genesis

visualization.render {
  grammar: {
    data: spine_entries,
    geom: "timeline",
    color: "entry_type",
    tooltip: "payload_summary"
  }
}
```

Certificate history renders naturally as a directed graph:
mint → transfer → loan → return → transfer.

**Applications**: Experiment history dashboards (any spring),
certificate chain-of-custody viewers (healthSpring consent,
ludoSpring asset ownership), regulatory timeline exports
(wetSpring, airSpring).

### 3.5 LoamSpine + ToadStool: Compute Result Permanence

**Compute results committed permanently with hardware provenance.**

```
compute.submit { shader: "fft_f64", input_hash } → result_hash, substrate

entry.append { spine_id, entry_type: "DataAnchor",
  payload: { result_hash, compute_substrate: "nvidia_sm89", shader: "fft_f64" }
}
  → permanent record of which hardware produced which result
```

This closes the reproducibility gap — if results differ on different
hardware, the spine records which substrate was used for each.

**Applications**: GPU computation audit trails (hotSpring lattice QCD),
certified numerical results (groundSpring seismic inversion),
bit-exact reproducibility records (neuralSpring training).

### 3.6 LoamSpine + Squirrel: AI-Analyzed Commit Patterns

**Squirrel can analyze spine commit patterns to detect anomalies
and suggest optimizations.**

```
(read spine entries over time)
ai.analyze { context: commit_pattern_summary }
  → { anomalies: [...], patterns: [...], suggestions: [...] }
```

**Applications**: Detecting unusual commit frequency (possible
data integrity issue), identifying underused spines that could be
consolidated, suggesting when to seal completed experiment spines,
flagging certificate chains with suspicious transfer patterns.

### 3.7 LoamSpine + skunkBat: Tamper Detection

**skunkBat can monitor spine integrity in real-time.**

```
(skunkBat periodically verifies hash chains)
entry.get_tip { spine_id } → tip
(walk chain, verify each entry's hash links to previous)
  → alert if chain integrity is violated
  → alert if unexpected entry types appear
  → alert if unauthorized committers are detected
```

**Applications**: Continuous integrity monitoring for regulatory
spines (healthSpring), tamper-evident sensor logs (groundSpring),
detecting unauthorized data commits (any spring).

### 3.8 LoamSpine + coralReef + barraCuda: Sovereign Math Permanence

**The full sovereign compute → permanence pipeline.**

```
1. barraCuda authors WGSL shader       → wgsl_hash
2. coralReef compiles to SPIR-V        → spirv_hash, target_gpu
3. ToadStool dispatches to GPU         → result_hash, timing
4. entry.append { spine_id, entry_type: "DataAnchor",
     payload: {
       wgsl_hash, spirv_hash, result_hash,
       target_gpu, timing_ms
     }
   }
   → permanent record of the entire compute chain
```

Every mathematical result traces back through compilation, shader
source, and hardware — all stored permanently with no vendor SDK
dependencies.

---

## 4. Novel Spring Compositions

These are higher-order patterns that emerge from combining LoamSpine
with multiple primals simultaneously.

### 4.1 Digital Deed Registry

**Springs**: any + LoamSpine + BearDog + sweetGrass

Loam Certificates become digital deeds for any valuable asset in
the ecosystem. Combined with BearDog signatures and sweetGrass
attribution, they form a complete ownership system.

```
1. certificate.mint { owner: "did:eco:alice", type: "DatasetOwnership",
     metadata: { dataset: "soil-metagenome-2026", records: 1_400_000 } }
   → certificate_id

2. crypto.sign { data: certificate_id, signer: "did:eco:alice" }
   → signed ownership claim

3. braid.create { activity: { type: "data_collection" },
     agents: [{ did: "did:eco:alice", role: "Creator" }],
     entity: { certificate_id } }
   → attribution braid linking creator to deed

4. certificate.transfer { certificate_id, to: "did:eco:bob" }
   → ownership transfers (previous history preserved on spine)

5. certificate.loan { certificate_id, borrower: "did:eco:carol",
     terms: { duration: "90d", attribution_required: true } }
   → temporary access with enforceable terms
```

**Domain applications**:
- **wetSpring**: Sequencing dataset deeds — track who owns reference
  genomes, with loan terms requiring attribution in publications
- **neuralSpring**: Model weight deeds — ownership of trained models
  with licensing terms for inference use
- **ludoSpring**: Game asset deeds — tileset, mechanic, and level
  ownership with royalty-bearing transfer
- **healthSpring**: Clinical data custodianship — consent-gated
  patient data with loan terms matching IRB protocols
- **airSpring**: Weather model IP — proprietary ET₀ model parameters
  with research-use loan provisions

### 4.2 Regulatory Compliance Package

**Springs**: healthSpring/wetSpring/airSpring + LoamSpine + BearDog + sweetGrass

For regulated domains (HIPAA, EPA, FDA, USDA), LoamSpine provides the
immutable backbone for audit packages:

```
1. Every experiment step committed (SessionCommit entries)
2. Every entry BearDog-signed (tamper-evident)
3. Every contributor attributed (BraidCommit entries)
4. Spine sealed after submission (SpineSealed — no retroactive changes)
5. Inclusion proofs for specific entries (proof.generate_inclusion)
   → regulator verifies without accessing entire chain
```

The sealed spine is the regulatory submission. The inclusion proofs
allow selective disclosure. The signatures prove non-repudiation.
The attribution braids satisfy contribution reporting requirements.

**Domain examples**:
- **healthSpring + FDA**: Every dosing decision traced from PK model
  parameters through computation to recommendation, sealed and signed
- **wetSpring + EPA**: PFAS screening results with instrument
  calibration provenance, sealed analytical chain
- **airSpring + USDA**: Water rights justification with ET₀ computation
  chain, sensor provenance, and model version history
- **hotSpring + DOE**: Nuclear simulation parameter provenance for
  safety-critical EOS calculations

### 4.3 Cross-Spring Checkpoint Federation

**Springs**: multiple + LoamSpine + rhizoCrypt + Songbird

When multiple springs contribute to a shared scientific question,
their checkpoints converge on a shared LoamSpine:

```
wetSpring:    commit.session { soil_microbiome_session }    → entry_a
airSpring:    commit.session { et0_model_session }          → entry_b
groundSpring: commit.session { sensor_calibration_session } → entry_c

All on the same spine (discovered via Songbird):
  spine = "ecology-study-2026-field-season"

entry.get_tip → entry_c (latest, links back through b → a → genesis)

proof.generate_inclusion { spine_id, entry_hash: entry_a }
  → proves soil data was part of the federated study
```

**Applications**:
- **Ecology study**: wetSpring (microbiome) + airSpring (climate) +
  groundSpring (soil sensors) converge on one spine
- **Drug development**: healthSpring (PK/PD) + wetSpring (gut microbiome) +
  neuralSpring (biomarker model) converge on one trial spine
- **Game science**: ludoSpring (player data) + neuralSpring (ML balance) +
  hotSpring (physics simulation) converge on one game study spine

### 4.4 Time-Boxed Experiment Archives

**Springs**: any + LoamSpine + biomeOS

biomeOS can orchestrate time-boxed spine lifecycles — open a spine
at experiment start, commit results during the run, seal it at
completion. No manual intervention.

```toml
# biomeOS deploy graph: experiment_archive.toml
[[graph.steps]]
name = "open_spine"
capability = "spine"
operation = "create"

[[graph.steps]]
name = "run_experiment"
capability = "dag"
operation = "create_session"
depends_on = ["open_spine"]

[[graph.steps]]
name = "commit_results"
capability = "commit"
operation = "session"
depends_on = ["run_experiment"]

[[graph.steps]]
name = "seal_archive"
capability = "spine"
operation = "seal"
depends_on = ["commit_results"]
condition = "experiment.status == 'complete'"
```

The sealed spine becomes a self-contained, tamper-evident archive
of the entire experiment. Multiple such archives can exist in
parallel across springs.

### 4.5 Certificate-Gated Data Marketplace

**Springs**: any + LoamSpine + rhizoCrypt + BearDog + Songbird

Certificates control who can access what data. Combined with
rhizoCrypt slice semantics and Songbird discovery, this creates
a decentralized data marketplace:

```
1. Producer: certificate.mint { type: "DataAccess", metadata: { dataset, price, terms } }
2. Consumer: discovers certificate via Songbird
3. Consumer: certificate.loan { terms: { duration: "30d", attribution_required: true } }
4. Consumer: dag.slice { mode: "Consignment", certificate_id }
   → data released only with valid certificate loan
5. Consumer uses data → results attributed back to producer via derivation chain
6. certificate.return → access revoked, loan recorded on spine
```

The certificate's spine history proves every access event. The
producer can audit who used their data, when, and for how long.

**Applications**: Genomic data sharing (wetSpring), weather model
licensing (airSpring), clinical data collaboration (healthSpring),
game content marketplace (ludoSpring), trained model licensing
(neuralSpring).

### 4.6 Provenance-Backed Reproducibility Certificates

**Springs**: any + LoamSpine + rhizoCrypt + sweetGrass + BearDog

A "reproducibility certificate" is a sealed spine that proves a result
can be reproduced from its inputs:

```
1. Original: commit.session { original_experiment } → entry_original
2. Reproduction: commit.session { reproduction_attempt } → entry_repro
   (same spine, linked by derivation)
3. Comparison:
   proof.generate_inclusion { entry_original } → proof_a
   proof.generate_inclusion { entry_repro }    → proof_b
   → both proofs verify against the same spine tip
4. Seal: spine.seal → permanent reproducibility record
5. sweetGrass attributes both original and reproducing teams
```

**Applications**: Journal reproducibility badges (wetSpring, hotSpring),
certified instrument calibration (groundSpring), validated clinical
protocols (healthSpring), bit-exact GPU computation verification
(neuralSpring + ToadStool).

### 4.7 Immutable Game World History

**Springs**: ludoSpring + LoamSpine + rhizoCrypt + sweetGrass + petalTongue

Game worlds accumulate history that players and AI agents create
together. LoamSpine makes that history permanent and queryable:

```
1. ludoSpring game session → rhizoCrypt DAG (60 Hz telemetry)
2. Session ends → dehydrate → commit.session (permanent)
3. sweetGrass attributes player and AI contributions
4. petalTongue renders world history timeline from spine entries
5. New game session can query past spine entries for world state
```

The spine becomes the "world chronicle" — an append-only history
that survives server restarts, player departures, and game updates.
Players can prove they were present for historical events via
inclusion proofs.

### 4.8 Multi-Site Clinical Trial Spine

**Springs**: healthSpring + LoamSpine + Songbird + BearDog + sweetGrass

A multi-site clinical trial uses one logical spine per trial, with
each site committing independently:

```
Site A (hospital): commit.session { patient_cohort_a }  → entry
Site B (university): commit.session { patient_cohort_b } → entry
Site C (clinic): commit.session { patient_cohort_c }     → entry

Each commit is:
  - BearDog-signed by the site's institutional DID
  - sweetGrass-attributed to the site's research team
  - Ordered by LoamSpine's append-only chain

spine.seal → trial complete, no further data accepted
proof.generate_inclusion → per-site proofs for regulatory review
```

HIPAA compliance: privacy levels on sweetGrass braids control what
each site can see about other sites. The spine proves participation
without revealing individual patient data.

---

## 5. Integration Patterns for Springs

### Minimal Integration (standalone LoamSpine only)

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

let spine = bridge.capability_call("spine", "create", &json!({
    "owner": agent_did,
    "metadata": { "niche": "airspring", "purpose": "et0-archive" }
}))?;

bridge.capability_call("entry", "append", &json!({
    "spine_id": spine["spine_id"],
    "entry_type": "DataAnchor",
    "payload": { "content_hash": result_hash, "experiment_id": exp_id }
}))?;
```

The spring never imports LoamSpine directly. It discovers the capability
at runtime. If LoamSpine is not running, the call fails gracefully.

### Full Trio Integration

Use the same `NeuralBridge` for all trio operations:

```rust
let bridge = NeuralBridge::discover()?;

// Ephemeral work in rhizoCrypt
bridge.capability_call("dag", "create_session", &session_args)?;
bridge.capability_call("dag", "append_vertex", &vertex_args)?;

// Dehydrate and commit to LoamSpine
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

### Certificate Operations (standalone)

```rust
let bridge = NeuralBridge::discover()?;

let cert = bridge.capability_call("certificate", "mint", &json!({
    "owner": agent_did,
    "certificate_type": "DataOwnership",
    "metadata": { "dataset": dataset_id, "license": "CC-BY-SA-4.0" }
}))?;

bridge.capability_call("certificate", "loan", &json!({
    "certificate_id": cert["certificate_id"],
    "borrower": collaborator_did,
    "terms": { "duration": "30d", "read_only": true }
}))?;
```

---

## 6. What LoamSpine Does NOT Do

| Concern | Who Handles It |
|---------|---------------|
| Ephemeral working state | rhizoCrypt (dag.*) |
| Attribution / provenance | sweetGrass (provenance.*, braid.create) |
| Content blob storage | NestGate (storage.*) |
| Signing / encryption | BearDog (crypto.*) |
| Discovery / networking | Songbird (discovery.*) |
| Compute dispatch | ToadStool (compute.*) |
| Visualization | petalTongue (visualization.*) |
| AI inference | Squirrel (ai.*) |
| Security monitoring | skunkBat (security.*) |
| Orchestration | biomeOS (Neural API) |
| Reward distribution | sunCloud (reward.*) |

LoamSpine answers "what happened permanently?" It does not store blobs,
run computations, or attribute contributions. It records that those things
occurred, immutably. Everything else is discovered at runtime and composed
by biomeOS. Complexity through coordination, not through coupling.

---

## References

- `wateringHole/RHIZOCRYPT_LEVERAGE_GUIDE.md` — Companion guide for rhizoCrypt
- `wateringHole/SWEETGRASS_LEVERAGE_GUIDE.md` — Companion guide for sweetGrass
- `wateringHole/SPRING_PROVENANCE_TRIO_INTEGRATION_PATTERN.md` — Integration template
- `wateringHole/CROSS_SPRING_DATA_FLOW_STANDARD.md` — Time series exchange format
- `wateringHole/INTER_PRIMAL_INTERACTIONS.md` — RootPulse coordination flows
- `whitePaper/gen3/PRIMAL_CATALOG.md` — Full primal catalogue
- `whitePaper/gen3/ECOSYSTEM_ARCHITECTURE.md` — NUCLEUS architecture
- `wateringHole/BIOMEOS_LEVERAGE_GUIDE.md` — fieldMouse (minimal deployable unit) vs. niche
- `phase2/loamSpine/specs/` — LoamSpine specification documents
