<!--
SPDX-License-Identifier: AGPL-3.0-or-later
Documentation and creative text in this file: CC-BY-SA-4.0
-->

# ludoSpring V18 — Deploy Graph Schema Unification

**Date:** April 3, 2026
**From:** ludoSpring (game science spring)
**To:** biomeOS team, primalSpring team
**Status:** Active
**License:** AGPL-3.0-or-later

---

## The Problem (GAP-020)

The ecosystem has two deploy graph TOML schemas that serve different purposes
and don't cross-validate:

### Schema 1: BYOB (`[[graph.node]]`)

Used by springs and gardens to declare what primals a composition needs.

- **Implementations:** primalSpring, ludoSpring, esotericWebb
- **Files:** 18+ TOML files across the ecosystem
- **Array key:** `[[graph.node]]` (singular)

### Schema 2: Execution (`[[nodes]]` / `[[graph.nodes]]`)

Used by biomeOS internally to execute capability graphs.

- **Implementation:** `biomeos-graph`, `biomeos-atomic-deploy`
- **Array keys:** `[[nodes]]` (top-level) or `[[graph.nodes]]` (nested)
- **Extra fields:** `config`, `gate`, `budget_ms`, `feedback_to`

### The Gap

`neural_graph.rs` (line ~82) detects `[[nodes]]` and `[[graph.nodes]]` but
not `[[graph.node]]`. When a garden or spring writes `biomeos deploy --graph
my_deploy.toml` with a BYOB graph, biomeOS cannot parse it. The translation is
opaque — there is no documented conversion path.

---

## The Resolution

### 1. BYOB schema is now a wateringHole standard

`wateringHole/BYOB_DEPLOY_GRAPH_SCHEMA.md` documents the canonical TOML
schema with field definitions, node structure, coordination modes, phase
convention, and health contract. This is the "RFC" that everyone implements
against. No shared crate — each layer independently implements from the spec.

### 2. biomeOS absorbs `[[graph.node]]` ingestion

biomeOS adds a detection path in `neural_graph.rs`:

```
if value["graph"]["node"] exists:
    parse as BYOB → convert to execution schema
elif value["nodes"] exists:
    parse as neural_graph (existing path)
elif value["graph"]["nodes"] exists:
    parse as deployment_graph (existing path)
```

The conversion from BYOB to execution is documented in the schema spec
(field mapping table). The key conversions:

| BYOB field | Execution field |
|------------|----------------|
| `name` | `id` |
| `by_capability` | `capability` |
| `depends_on` | edge list |
| `order` | (recomputed from dependency graph) |
| `required` | failure handling |
| `spawn` | pre-existing flag |
| `health_method` | health probe config |

### 3. primalSpring implements `validate-graph`

`primalspring validate-graph <path.toml>` parses any TOML, detects the schema
(BYOB vs execution), runs structural validation against the wateringHole spec,
and cross-references capabilities against the primal registry. This is the
schema compliance tool Webb GAP-020 requests.

---

## What This Does NOT Do

- **No shared crate.** Each consumer independently parses TOML from the spec.
- **No schema merger.** BYOB and execution remain separate schemas for separate
  purposes. biomeOS converts between them, not replaces one with the other.
- **No spring ownership of primal code.** Springs proved the pattern; biomeOS
  absorbs the ingestion capability independently.

---

## Evidence

### Independent implementations that validated the BYOB schema

| Implementation | Location | Tests |
|---------------|----------|-------|
| primalSpring | `ecoPrimal/src/deploy/mod.rs` | AtomicHarness loads graphs |
| ludoSpring | `barracuda/src/deploy/mod.rs` | 14 deploy tests, 9 graphs + 9 sketches |
| esotericWebb | `graphs/*.toml` consumed by launcher | 8 product graphs |

### `lifecycle.status` field naming inconsistency

ludoSpring's server returns `primal` in the health response; its discovery
module probes for `name`. Both implementations work because they only check
`capabilities`, but this is fragile. The BYOB schema spec normalizes `name`
as canonical with `primal` as an accepted alias.

---

## Timeline

| Step | Owner | Priority |
|------|-------|----------|
| BYOB schema spec published (this handoff) | wateringHole (done) | Complete |
| biomeOS adds `[[graph.node]]` detection | biomeOS | P1 |
| primalSpring implements `validate-graph` | primalSpring | P1 |
| Field naming normalization (`name` canonical) | All primals | P2 |

---

## Cross-References

- `wateringHole/BYOB_DEPLOY_GRAPH_SCHEMA.md` — the schema standard
- `gardens/esotericWebb/EVOLUTION_GAPS.md` (GAP-020) — original gap report
- `primals/biomeOS/crates/biomeos-atomic-deploy/src/neural_graph.rs` — current parser
- `springs/ludoSpring/specs/ECOSYSTEM_EVOLUTION_MAP.md` — full gap analysis
