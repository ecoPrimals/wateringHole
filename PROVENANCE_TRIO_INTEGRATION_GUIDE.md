# Provenance Trio Integration Guide

**Version:** 1.0.0
**Date:** April 27, 2026
**Audience:** Springs, gardens, and any composition wiring rhizoCrypt + loamSpine + sweetGrass
**Status:** Active
**License:** AGPL-3.0-or-later

---

## Purpose

The provenance trio — **rhizoCrypt** (ephemeral DAG), **loamSpine**
(immutable ledger), and **sweetGrass** (semantic attribution) — is the most
referenced subsystem across all springs. It is also the most common blocker
(PG-52: UDS empty responses from all three).

This document provides the operational integration guide: how to wire the trio
into a composition, what to expect from each primal, known failure modes, and
workarounds. It consolidates and promotes the patterns from
`fossilRecord/consolidated-apr2026/SCYBORG_PROVENANCE_TRIO_GUIDANCE.md` and
the cross-spring convergence analysis.

For the licensing framework built on the trio, see
`fossilRecord/consolidated-apr2026/SCYBORG_PROVENANCE_TRIO_GUIDANCE.md`.

---

## The Three Roles

```
Working Memory          Permanent Record          Attribution
┌──────────┐           ┌──────────┐           ┌──────────┐
│rhizoCrypt│──dehydrate──▶│loamSpine │◀──certify───│sweetGrass│
│          │           │          │           │          │
│ DAG      │           │ Ledger   │           │ Braids   │
│ Sessions │           │ Certs    │           │ W3C PROV │
│ Merkle   │           │ DID      │           │ Roles    │
└──────────┘           └──────────┘           └──────────┘
```

| Primal | Domain | IPC Capability | What It Owns |
|--------|--------|---------------|-------------|
| **rhizoCrypt** | Ephemeral memory | `dag` | Content-addressed DAG, session lifecycle, Merkle trees, dehydration to loamSpine |
| **loamSpine** | Permanence | `ledger` | Immutable append-only ledger, DID ownership, certificate lifecycle (mint/transfer/loan), temporal anchoring |
| **sweetGrass** | Attribution | `attribution` | W3C PROV-O braids, 12 contributor roles, derivation chains, privacy controls, attribution calculation |

---

## Deploy Graph Pattern

Include the trio in your deploy graph with `fallback = "skip"` on all three
nodes. This is the canonical pattern — every spring and garden uses it.

```toml
# Provenance trio — optional enrichment
[[graph.node]]
name = "rhizocrypt"
binary = "rhizocrypt"
order = 10
required = false
depends_on = ["beardog"]
health_method = "health.liveness"
by_capability = "dag"
capabilities = ["dag.create_session", "dag.add_vertex", "dag.dehydrate"]
fallback = "skip"

[[graph.node]]
name = "loamspine"
binary = "loamspine"
order = 11
required = false
depends_on = ["beardog"]
health_method = "health.liveness"
by_capability = "ledger"
capabilities = ["ledger.commit", "ledger.mint_certificate", "ledger.verify"]
fallback = "skip"

[[graph.node]]
name = "sweetgrass"
binary = "sweetgrass"
order = 12
required = false
depends_on = ["beardog"]
health_method = "health.liveness"
by_capability = "attribution"
capabilities = ["attribution.create_braid", "attribution.add_contribution", "attribution.calculate"]
fallback = "skip"
```

**Why `depends_on = ["beardog"]`**: The trio uses BearDog for cryptographic
signing of DAG vertices, ledger entries, and attribution records.

**Why `fallback = "skip"`**: Science and product logic must work without
provenance. Recording provenance is enrichment — it does not gate computation.

---

## The Commit Flow

The standard provenance commit flow composes all three primals in sequence.
biomeOS orchestrates this as the `rootpulse_commit` graph.

```
1. rhizoCrypt.dag.create_session(name)
   → session_id

2. [Your work happens — add vertices to the DAG]
   rhizoCrypt.dag.add_vertex(session_id, content, parents)
   → vertex_id (content-addressed)

3. sweetGrass.attribution.create_braid(artifact_id)
   sweetGrass.attribution.add_contribution(braid_id, agent, role, weight)
   → braid with contributor records

4. rhizoCrypt.dag.dehydrate(session_id)
   → transfers session state to loamSpine

5. loamSpine.ledger.commit(dehydrated_state, signature)
   → immutable ledger entry with temporal anchor

6. sweetGrass.attribution.seal(braid_id, ledger_ref)
   → braid sealed with loamSpine reference
```

**The result**: An immutable record that says WHO did WHAT, WHEN, with
cryptographic proof from BearDog and a permanent ledger entry from loamSpine.

---

## JSON-RPC Methods Reference

### rhizoCrypt (capability: `dag`)

| Method | Params | Response | Notes |
|--------|--------|----------|-------|
| `health.liveness` | `{}` | `{"status": "alive", "name": "rhizocrypt"}` | Standard health probe |
| `dag.create_session` | `{"name": "my_experiment"}` | `{"session_id": "..."}` | Creates working memory scope |
| `dag.add_vertex` | `{"session_id": "...", "content": "...", "parents": [...]}` | `{"vertex_id": "..."}` | Content-addressed; parents form DAG edges |
| `dag.get_vertex` | `{"vertex_id": "..."}` | `{"content": "...", "parents": [...], "metadata": {...}}` | Retrieve by content hash |
| `dag.dehydrate` | `{"session_id": "..."}` | `{"state": "..."}` | Serialize session for loamSpine commit |
| `dag.merkle_root` | `{"session_id": "..."}` | `{"root": "..."}` | Merkle tree root of session state |

### loamSpine (capability: `ledger`)

| Method | Params | Response | Notes |
|--------|--------|----------|-------|
| `health.liveness` | `{}` | `{"status": "alive", "name": "loamspine"}` | Standard health probe |
| `ledger.commit` | `{"state": "...", "signature": "..."}` | `{"entry_id": "...", "timestamp": "..."}` | Immutable append; requires BearDog signature |
| `ledger.verify` | `{"entry_id": "..."}` | `{"valid": true, "timestamp": "..."}` | Verify ledger entry integrity |
| `ledger.mint_certificate` | `{"type": "...", "subject": "...", "attributes": {...}}` | `{"cert_id": "..."}` | Issue a loam certificate |
| `ledger.get_entry` | `{"entry_id": "..."}` | `{"state": "...", "signature": "...", "timestamp": "..."}` | Retrieve ledger entry |

### sweetGrass (capability: `attribution`)

| Method | Params | Response | Notes |
|--------|--------|----------|-------|
| `health.liveness` | `{}` | `{"status": "alive", "name": "sweetgrass"}` | Standard health probe |
| `attribution.create_braid` | `{"artifact_id": "..."}` | `{"braid_id": "..."}` | Create attribution braid for an artifact |
| `attribution.add_contribution` | `{"braid_id": "...", "agent": "...", "role": "Creator", "weight": 0.5}` | `{"contribution_id": "..."}` | Add contributor to braid |
| `attribution.calculate` | `{"braid_id": "..."}` | `{"contributions": [...], "total_weight": 1.0}` | Calculate attribution distribution |
| `attribution.seal` | `{"braid_id": "...", "ledger_ref": "..."}` | `{"sealed": true}` | Seal braid with loamSpine reference |
| `attribution.export_prov` | `{"braid_id": "..."}` | `{"prov_o": {...}}` | Export as W3C PROV-O JSON-LD |

---

## Graceful Degradation Pattern

Every spring MUST degrade gracefully when the trio is absent. This is the
pattern from airSpring, absorbed by all delta springs:

```rust
pub struct ProvenanceContext {
    rhizocrypt: Option<PathBuf>,
    loamspine: Option<PathBuf>,
    sweetgrass: Option<PathBuf>,
}

impl ProvenanceContext {
    pub fn discover(socket_dir: &Path) -> Self {
        Self {
            rhizocrypt: probe_socket(socket_dir, "rhizocrypt"),
            loamspine: probe_socket(socket_dir, "loamspine"),
            sweetgrass: probe_socket(socket_dir, "sweetgrass"),
        }
    }

    pub fn is_available(&self) -> bool {
        self.rhizocrypt.is_some()
            && self.loamspine.is_some()
            && self.sweetgrass.is_some()
    }

    pub fn record_if_available(&self, artifact: &str) -> ProvenanceResult {
        if !self.is_available() {
            return ProvenanceResult { recorded: false, reason: "trio unavailable" };
        }
        // ... wire the commit flow above ...
        ProvenanceResult { recorded: true, reason: "committed" }
    }
}
```

**Rule**: Domain logic returns `Ok` with `recorded: false` when the trio is
missing — never an error. Experiments run without provenance. Provenance is
recorded when available.

---

## Shell Composition Library Support

The `nucleus_composition_lib.sh` (41 functions) provides trio wiring for
interactive compositions:

```bash
source tools/nucleus_composition_lib.sh

# Check trio availability
trio_check || warn "Provenance trio not available — continuing without"

# Record provenance (no-op if trio unavailable)
trio_record_experiment "my_experiment" "session_001"
```

The library uses the `_uds_send()` fallback chain (socat → python3 → nc)
so trio wiring works on any system with at least one transport tool.

---

## Known Issues and Workarounds

### PG-52: UDS Empty Responses (OPEN — upstream)

**Problem**: rhizoCrypt, loamSpine, and sweetGrass sometimes return empty
responses to JSON-RPC calls over UDS. The socket connects, the payload sends,
but the response is zero bytes.

**Severity**: High — blocks provenance recording for all springs.

**Affected**: All three trio primals.

**Workaround**: Retry with backoff. The shell composition library implements
this:

```bash
trio_call_with_retry() {
    local sock="$1" method="$2" params="$3" retries="${4:-3}"
    local attempt=0
    while [ $attempt -lt $retries ]; do
        local resp
        resp=$(send_rpc "$sock" "$method" "$params")
        if [ -n "$resp" ] && [ "$resp" != "null" ]; then
            echo "$resp"
            return 0
        fi
        attempt=$((attempt + 1))
        sleep 0.5
    done
    warn "trio call failed after $retries attempts: $method"
    return 1
}
```

**Root cause**: Suspected race between socket accept and handler readiness
in the trio primals' async runtime. Under investigation by primal teams.

**Tracking**: `primalSpring/docs/PRIMAL_GAPS.md` PG-52.

### PG-48: petalTongue musl Binary Threading Panic

**Problem**: petalTongue's musl binary panics on `winit` thread creation
in desktop mode.

**Relevance**: If your garden uses petalTongue for desktop rendering, you
need glibc builds or headless mode.

**Workaround**: Use `petaltongue server --headless` for non-desktop, or
build petalTongue with glibc target (`x86_64-unknown-linux-gnu`).

**Tracking**: `primalSpring/docs/PRIMAL_GAPS.md` PG-48.

### PG-53: Incomplete `proprioception.get` in Server Mode

**Problem**: petalTongue's `proprioception.get` returns incomplete data
when running in `server` mode vs desktop mode.

**Relevance**: Gardens querying petalTongue's self-knowledge may get
incomplete capability lists in headless deployments.

**Workaround**: Use `capabilities.list` instead of `proprioception.get`
for capability discovery.

**Tracking**: `primalSpring/docs/PRIMAL_GAPS.md` PG-53.

---

## Cross-Spring Provenance Patterns

### Experiment Provenance (all science springs)

Every science experiment can record its lineage:

```
1. Create DAG session: "wetspring_exp403_primal_parity"
2. Add vertex: Python baseline (content hash of expected values)
3. Add vertex: Rust computation result (content hash of output)
4. Add vertex: Parity comparison (depends on both above)
5. Create braid: attribute the experiment to spring + operator
6. Dehydrate → commit → seal
```

### Cross-Spring Attribution

When healthSpring routes a model through wetSpring (gut diversity) →
neuralSpring (surrogate) → hotSpring (Anderson spectral), the provenance
trio tracks the full cross-spring lineage:

```
sweetGrass braid:
  - wetSpring: Creator (gut diversity model), weight 0.4
  - neuralSpring: Contributor (surrogate training), weight 0.3
  - hotSpring: Validator (spectral verification), weight 0.2
  - healthSpring: Publisher (clinical routing), weight 0.1
```

This pattern enables the "radiating attribution" model from the
`SUNCLOUD_ECONOMIC_MODEL.md` — value distribution proportional to
contribution across spring boundaries.

### Novel Ferment Transcripts

Digital objects that gain value from accumulated, verifiable history:

```
Artifact: "Gonzales Drug Candidate #7"
  └─ rhizoCrypt DAG: 47 vertices (exploration → validation → screening)
  └─ loamSpine Ledger: 12 entries (each experiment pass sealed)
  └─ sweetGrass Braid: 8 contributors across 3 springs
  └─ Loam Certificate: provenance chain from published paper → reproduction → pipeline
```

See `whitePaper/gen4/economics/NOVEL_FERMENT_TRANSCRIPTS.md` for the
economic model.

---

## Evolution Path

### Current (April 2026)

- Trio primals operational, UDS IPC functional (with PG-52 caveat)
- All delta springs have graceful degradation wired
- Shell composition library supports trio
- `rootpulse_commit` graph validated end-to-end

### Near Term

- PG-52 UDS empty response fix (upstream primal teams)
- First-class `provenance.*` JSON-RPC surface in rhizoCrypt
- License metadata in trio (scyBorg Phase 1 — schema in existing metadata maps)
- Cross-spring provenance braids in production compositions

### Medium Term

- Attribution notice generation API in sweetGrass
- Loam certificate mesh for cross-gate provenance
- `ProvenanceQueryable` trait implementation in rhizoCrypt
- sunCloud economic integration — radiating attribution becomes value distribution

---

## Related Documents

- `fossilRecord/consolidated-apr2026/SCYBORG_PROVENANCE_TRIO_GUIDANCE.md` — scyBorg licensing via trio
- `DEPLOYMENT_AND_COMPOSITION.md` — Deploy graph patterns
- `SPRING_COMPOSITION_PATTERNS.md` §7 — Graceful degradation pattern
- `GARDEN_COMPOSITION_ONRAMP.md` — Garden product integration
- `primalSpring/docs/PRIMAL_GAPS.md` — PG-52 and related gaps
- `whitePaper/gen4/economics/NOVEL_FERMENT_TRANSCRIPTS.md` — NFT economics
- `whitePaper/economics/SUNCLOUD_ECONOMIC_MODEL.md` — Radiating attribution

---

**The trio records what happened. The ledger proves it. The braid attributes it. Together they make provenance structural, not aspirational.**
