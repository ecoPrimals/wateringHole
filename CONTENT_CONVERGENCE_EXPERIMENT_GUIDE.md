<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# Content Convergence Experiment Guide — Spring Participation

**Date**: March 16, 2026
**Origin**: sweetGrass v0.7.15 / `specs/CONTENT_CONVERGENCE.md`
**Audience**: All Springs, rhizoCrypt, loamSpine
**Coordination**: ISSUE-013 in `SPRING_EVOLUTION_ISSUES.md`
**Status**: Proposed — seeking Spring participants

---

## What Is Content Convergence?

When two independent agents or processes produce data with the same content hash,
we call that **content convergence**. Currently, sweetGrass's content hash index
is "collision-lossy" — the later arrival overwrites the earlier mapping. This
discards valuable provenance information.

The insight comes from hash collision research: instead of treating collisions as
problems to resolve, we ask **what data lies at the collision?** The convergence
point itself carries semantic meaning:

- **Reproducibility**: Independent paths arrived at the same result
- **Consensus**: Multiple agents agree on the same artifact
- **Pattern**: Structural similarity across sessions or domains

### The Cross-Hatched Letter Analogy

Before cheap paper, writers saved space by rotating the page 90° and writing
across existing text. Both layers of information survived because the reader
could distinguish them by orientation. Content convergence is the digital
equivalent — multiple provenance layers on the same content "surface."

### Linear ↔ Branching Duality

Biology teaches that linear growth (hypha extension) and branching (anastomosis)
are not opposites but coexisting modes that evolve into each other:

| Mode | Analog | In ecoPrimals |
|------|--------|---------------|
| **Linear** | Spine growth, append-only log | loamSpine chains, `IndexMap` temporal order |
| **Branching** | Mycelium network, DAG | rhizoCrypt DAG, `was_derived_from` edges |
| **Convergence** | Anastomosis, hyphal fusion | Content hash collision, provenance intersection |

The experiment explores where linear storage meets branching provenance — and
what emerges at the intersection.

---

## How Springs Participate

### Phase A: Identify Convergence Candidates (Now)

Each Spring should audit their data production patterns and identify scenarios
where independent processes might produce identical content hashes:

| Spring | Candidate Scenario |
|--------|-------------------|
| **wetSpring** | Same molecule computed with different basis sets yielding identical optimized geometry |
| **groundSpring** | Overlapping sensor grids producing identical measurement vectors |
| **hotSpring** | Independent plasma simulations converging on same equilibrium state |
| **airSpring** | Multiple ET₀ methods producing identical daily values from different physics |
| **neuralSpring** | Ensemble models producing identical predictions for the same input |
| **ludoSpring** | Independent game agents discovering identical optimal strategies |
| **healthSpring** | Multiple diagnostic pathways arriving at the same clinical assessment |

**Action**: Document your convergence candidates in your Spring's experiment log.
Reference this guide and ISSUE-013.

### Phase B: Produce Convergent Braids (After sweetGrass Phase 1)

Once sweetGrass implements `ContentConvergence` tracking:

1. **Create two Braids with the same `data_hash` from different agents**
2. **Use different `was_derived_from` paths** — the content is the same but
   the provenance is independent
3. **Query `convergence.query`** to verify both arrivals are recorded
4. **Report**: How often does natural convergence occur in your domain?

```json
// Example: wetSpring produces convergent molecular geometry
// Agent 1: DFT with B3LYP/6-31G*
{
  "jsonrpc": "2.0",
  "method": "braid.create",
  "params": {
    "data_hash": "sha256:abc123...",
    "mime_type": "chemical/x-xyz",
    "was_attributed_to": "did:key:z6MkWetAgent1",
    "was_derived_from": [
      { "data_hash": "sha256:b3lyp_input..." }
    ]
  },
  "id": 1
}

// Agent 2: DFT with PBE0/cc-pVTZ (different method, same result)
{
  "jsonrpc": "2.0",
  "method": "braid.create",
  "params": {
    "data_hash": "sha256:abc123...",
    "mime_type": "chemical/x-xyz",
    "was_attributed_to": "did:key:z6MkWetAgent2",
    "was_derived_from": [
      { "data_hash": "sha256:pbe0_input..." }
    ]
  },
  "id": 2
}

// Query convergence
{
  "jsonrpc": "2.0",
  "method": "convergence.query",
  "params": { "content_hash": "sha256:abc123..." },
  "id": 3
}
```

### Phase C: Convergence Analysis (After sweetGrass Phase 3)

Once convergence data accumulates:

1. **Convergence rate**: What fraction of content hashes have multiple arrivals?
2. **Agent clustering**: Do certain agents converge more often?
3. **Temporal patterns**: Do convergent arrivals cluster in time?
4. **Derivation path analysis**: What do the independent paths have in common?
5. **Domain-specific signals**: Does convergence predict reproducibility?

---

## Hash Table Sizing Experiments

The sub-hashing insight suggests that by **intentionally adjusting hash granularity**,
we can control convergence rates and discover different kinds of patterns:

### Experiment 1: Truncated Hashes (Similarity Clustering)

Use a truncated content hash (e.g., first 16 bytes of SHA-256) as a secondary
index. This creates intentional "convergence" among similar-but-not-identical
content, enabling approximate similarity search.

**Spring candidates**: wetSpring (molecular similarity), neuralSpring (embedding
proximity), groundSpring (measurement clustering)

### Experiment 2: Domain-Specific Hashes (Semantic Convergence)

Compute a domain-specific hash that captures semantic content rather than
byte-level identity. For example, a molecular fingerprint hash that is identical
for stereoisomers.

**Spring candidates**: wetSpring (molecular fingerprints), healthSpring
(diagnostic codes), ludoSpring (game state equivalence classes)

### Experiment 3: Locality-Sensitive Hashing (Approximate Convergence)

Use LSH to create hash functions where similar inputs map to the same bucket.
This connects to rhizoCrypt's ISSUE-012 (Content Similarity Index).

**Spring candidates**: neuralSpring (embedding LSH), airSpring (time-series
similarity), hotSpring (simulation state proximity)

---

## Coordination with rhizoCrypt ISSUE-012

rhizoCrypt's Content Similarity Index (ISSUE-012) proposes LSH for cross-session
similarity within the DAG. Content Convergence in sweetGrass operates at the
provenance layer above. The two experiments are complementary:

| Layer | rhizoCrypt ISSUE-012 | sweetGrass ISSUE-013 |
|-------|---------------------|---------------------|
| **Scope** | Vertex similarity within DAGs | Braid convergence across agents |
| **Hash type** | Locality-sensitive | Content-addressed (SHA-256) |
| **Signal** | Structural similarity | Provenance convergence |
| **Resolution** | More DAG edges | `ContentConvergence` records |

Springs participating in both experiments can cross-reference findings:
do rhizoCrypt-similar vertices produce sweetGrass-convergent Braids?

---

## Deliverables

Each participating Spring should produce:

1. **Convergence audit** — Document in your experiment log which data production
   scenarios can produce convergent content hashes
2. **Test Braids** — After sweetGrass Phase 1, produce at least 2 convergent
   Braid pairs via `braid.create`
3. **Analysis report** — After sweetGrass Phase 3, analyze convergence patterns
   in your domain and report findings to wateringHole

---

## Timeline

| Phase | When | Who |
|-------|------|-----|
| **Phase A** (audit) | Now | All interested Springs |
| **sweetGrass Phase 1** (core types) | v0.8.x | sweetGrass team |
| **Phase B** (produce convergent Braids) | After sweetGrass Phase 1 | Participating Springs |
| **sweetGrass Phase 3** (PROV-O integration) | v0.9.x | sweetGrass team |
| **Phase C** (analysis) | After sweetGrass Phase 3 | Participating Springs |

---

## References

- `sweetGrass/specs/CONTENT_CONVERGENCE.md` — Full specification
- `SPRING_EVOLUTION_ISSUES.md` ISSUE-013 — Coordination issue
- `SPRING_EVOLUTION_ISSUES.md` ISSUE-012 — Related rhizoCrypt LSH experiment
- `SWEETGRASS_LEVERAGE_GUIDE.md` — sweetGrass IPC methods
- `RHIZOCRYPT_LEVERAGE_GUIDE.md` — rhizoCrypt DAG and vertex APIs

---

*When independent paths converge on the same content, the convergence itself is provenance.*
