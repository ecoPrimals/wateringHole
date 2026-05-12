# Provenance Trio Operational Handoff — May 2026

**Source**: projectNUCLEUS provenance pipeline elevation on ironGate
**Audience**: rhizoCrypt, loamSpine, sweetGrass primal teams
**Date**: 2026-05-05

---

## Context

The provenance trio was deployed and exercised end-to-end as part of a Nest Atomic + ToadStool composition (9 primals) on ironGate. The pipeline processed 10 wetSpring bioinformatics workloads with real NCBI data (PRJNA488170, 11.9M reads) and wrapped every artifact and step in a full provenance chain.

Integration used **direct JSON-RPC over TCP/HTTP** (not Neural API routing). This is the first operational validation of the trio outside of primalSpring experiments.

---

## Deployment Configuration

| Primal | Port | Protocol | Socket |
|--------|------|----------|--------|
| rhizoCrypt | 9600 (tarpc), **9601** (JSON-RPC) | Newline-delimited JSON-RPC on TCP | `/tmp/biomeos/biomeos/rhizocrypt.sock` |
| loamSpine | 9001 (tarpc), **9700** (JSON-RPC) | HTTP JSON-RPC | `/tmp/biomeos/biomeos/loamspine.sock` |
| sweetGrass | dynamic (tarpc), **`--http-port`** (HTTP, v0.7.30+) | HTTP JSON-RPC at `/jsonrpc` | `/tmp/biomeos/biomeos/sweetgrass-{family}.sock` |

Startup commands used:
```bash
rhizocrypt server --port 9600
loamspine server --port 9700
sweetgrass server --port 9850 --http-port 8080   # TCP 9850 (avoids biomeOS 9800); HTTP on 8080
```

---

## JSON-RPC Methods Exercised

### rhizoCrypt

**`dag.session.create`** — Creates a new DAG session
```json
{"method": "dag.session.create", "params": {"name": "abg-pipeline-20260504"}}
// Returns: session UUID string
```

**`dag.event.append`** — Appends a vertex to the session DAG
```json
{"method": "dag.event.append", "params": {
    "session_id": "<uuid>",
    "event_type": {"DataCreate": {}},
    "data": {"key": "ncbi:SRR7760408:R1", "blake3": "<hex>", "size": 2223544784}
}}
// Returns: BLAKE3 vertex hash (hex string)
```

Valid `event_type` struct variants: `DataCreate{}`, `ExperimentStart{"protocol": "..."}`, `Result{"confidence_percent": 100}`, `Custom{"domain": "...", "label": "..."}`, and others (`SessionStart`, `AgentAction`, `DataModify`, `Observation`, `Analysis`, etc.)

**`dag.merkle.root`** — Computes Merkle root of all session vertices
```json
{"method": "dag.merkle.root", "params": {"session_id": "<uuid>"}}
// Returns: BLAKE3 hex string (64 chars)
```

**`dag.session.list`** — Lists all sessions with vertex counts
```json
{"method": "dag.session.list", "params": {}}
// Returns: array of {id, vertex_count, state, created_at, session_type}
```

### loamSpine

**`spine.create`** — Creates a new permanent ledger spine
```json
{"method": "spine.create", "params": {"name": "abg-pipeline", "owner": "ecoPrimal"}}
// Returns: {spine_id, genesis_hash: [u8; 32]}
```

**`entry.append`** with `DataAnchor` — Records a data artifact
```json
{"method": "entry.append", "params": {
    "spine_id": "<uuid>",
    "entry_type": {"DataAnchor": {
        "data_hash": [161,157,106,...],   // [u8; 32] — NOT hex string
        "source": "ncbi_fastq",
        "size": 2223544784
    }},
    "committer": "did:primal:ecoPrimal",
    "data": {"key": "ncbi:SRR7760408:R1", "blake3": "<hex>"}
}}
// Returns: {entry_hash: [u8; 32], index: N}
```

**`entry.append`** with `SessionCommit` — Commits a DAG session to permanent ledger
```json
{"method": "entry.append", "params": {
    "spine_id": "<uuid>",
    "entry_type": {"SessionCommit": {
        "session_id": "<uuid>",
        "merkle_root": [41,46,187,...],   // [u8; 32] — NOT hex string
        "vertex_count": 24,
        "committer": "did:primal:ecoPrimal"
    }},
    "committer": "did:primal:ecoPrimal",
    "data": {"pipeline": "abg-pipeline-20260504", "event_count": 24}
}}
// Returns: {entry_hash: [u8; 32], index: N}
```

Valid `entry_type` variants: `Genesis`, `MetadataUpdate`, `SpineSealed`, `SessionCommit`, `DataAnchor`, `BraidCommit`, `CertificateMint`, `CertificateTransfer`, `CertificateLoan`, `CertificateReturn`, `SliceAnchor`, `SliceOperation`, `Custom`, and others.

### sweetGrass

**`braid.create`** — Creates an attribution braid with ed25519 witness
```json
{"method": "braid.create", "params": {
    "data_hash": "<64-char hex string>",
    "name": "abg-pipeline-20260504",
    "mime_type": "application/x-provenance-pipeline",
    "description": "ABG Full Pipeline — 24 events across wetSpring validators",
    "size": 24
}}
// Returns: Full W3C PROV-O JSON-LD document with:
//   @id: "urn:braid:<data_hash>"
//   witness: {algorithm: "ed25519", evidence: "<base64>", agent: "did:key:..."}
//   was_attributed_to: "did:primal:<uuid>"
//   @context with prov:, schema:, ecop: namespaces
```

---

## Key Findings and API Feedback

### 1. Byte Arrays vs Hex Strings (High Priority)

loamSpine `data_hash` and `merkle_root` require `[u8; 32]` JSON byte arrays. rhizoCrypt returns Merkle roots as hex strings. sweetGrass accepts hex strings for `data_hash`.

This forces every caller to convert between hex and byte arrays:
```python
# Required in every shell script call to loamSpine
bytes.fromhex("292ebbcf8f02...") → [41, 46, 187, ...]
```

**Recommendation**: Accept both hex strings and `[u8; 32]` arrays in all JSON-RPC params that take hashes. Return hex strings consistently. This is a serde `#[serde(deserialize_with)]` change.

### 2. SessionCommit Requires Redundant `committer` Field

`SessionCommit` requires `committer` both inside the struct variant AND as a top-level `entry.append` param. The inner `committer` should be sufficient, or the outer one should be inherited.

### 3. sweetGrass TCP Requires BTSP Handshake — RESOLVED (v0.7.30)

~~The `--port 9800` TCP port requires a BTSP frame handshake before accepting JSON-RPC.~~

**Resolved in v0.7.30**: `detect_protocol` now skips leading ASCII whitespace before classifying connections. Clients sending `\n{"jsonrpc":"2.0",...}` are correctly routed to JSON-RPC. TCP port recommendation changed to **9850** to avoid biomeOS conflict at 9800.

### 4. sweetGrass HTTP Port is Dynamic — RESOLVED (v0.7.30)

~~The HTTP port is not configurable via the `--port` flag.~~

**Resolved in v0.7.30**: New `--http-port` / `SWEETGRASS_HTTP_PORT` flag for direct HTTP port configuration. HTTP is documented as the primary integration surface. Example: `sweetgrass server --http-port 8080`.

### 5. Event Type Discovery

`dag.event.append` error messages list all valid `event_type` variants, which is helpful. But there's no `rpc.discover` or `methods.list` introspection method.

**Recommendation**: Implement `rpc.discover` returning available methods and their parameter schemas (JSON Schema or similar).

---

## What Was Proven

- The trio **composes correctly** outside of primalSpring test harnesses
- Direct JSON-RPC integration works for shell-script-level orchestration
- 24 DAG events → Merkle root → permanent ledger → attribution braid in one pipeline run
- BLAKE3 content addressing is consistent across the stack (rhizoCrypt vertices, NestGate keys)
- ed25519 witness signatures are automatically applied by sweetGrass via Tower delegation

---

## Provenance Chain Produced

| Layer | Value |
|-------|-------|
| Session | `019df42d-0fba-7170-a216-2f3b282e3fb9` |
| Merkle Root | `292ebbcf8f02561aaa6c67b532ebbefc14c32192cf3dfb733ce81e45fba50f9e` |
| Spine | `019df41b-40c5-7b93-bf35-79dbd95a2cb3` |
| Commit Index | 55 |
| Braid | `urn:braid:292ebbcf8f02561aaa6c67b532ebbefc14c32192cf3dfb733ce81e45fba50f9e` |
| Witness | ed25519 by `did:key:z6MkQOXw_ZknlVNOL7iNEkxq5tTyBTSrJ4YBWRx8bGEqwS8` |
