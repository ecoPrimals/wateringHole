# Content Similarity Experiment Guide — Spring Participation

**Status**: Proposed Experiment  
**Version**: 1.0.0  
**Last Updated**: March 16, 2026  
**Spec Reference**: `rhizoCrypt/specs/CONTENT_INDEX_EXPERIMENT.md`  
**Coordination**: wateringHole cross-primal

---

## Overview

rhizoCrypt is exploring a **locality-sensitive content index** — a secondary
hash structure that intentionally creates "collisions" to discover structurally
similar vertices across sessions. This is inspired by hash collision
sub-indexing and the biological model of fungal anastomosis.

This guide describes how Springs can participate in and benefit from this
experiment.

---

## Background: Linear ↔ Branch Coexistence

The ecoPrimals ecosystem has two complementary data structures:

| Layer | Primal | Nature | Structure |
|-------|--------|--------|-----------|
| Working memory | rhizoCrypt | Branching | DAG (directed acyclic graph) |
| Permanent storage | LoamSpine | Linear | Append-only spine entries |

Both primals are independently exploring how intentional hash collision
resolution can create new data access patterns:

- **rhizoCrypt**: Cross-session vertex similarity via LSH (branch-to-branch)
- **LoamSpine**: Linear collision layering within spine entries (linear-to-linear)

Springs sit at the intersection — they produce data that flows through both
layers. By understanding both access patterns, Springs can design their data
structures to benefit from content similarity discovery.

---

## How Springs Can Participate

### 1. Produce Vertices with Consistent Structural Patterns

The content index hashes structural properties, not raw content:

```
LSH input = (event_type, sorted_metadata_keys, agent_prefix, parent_count)
```

Springs that produce vertices with consistent event types and metadata schemas
will naturally create useful index buckets. Recommendation:

- **Standardize event types** per domain (e.g., `compute.step`, `compute.result`,
  `analysis.sample`, `analysis.conclusion`)
- **Use consistent metadata key sets** within a domain
- **Include agent DID prefix** for attribution analysis

### 2. Query the Content Index

When the `content-index` feature is enabled, Springs can query rhizoCrypt for
similar vertices via JSON-RPC:

```json
{
  "jsonrpc": "2.0",
  "method": "dag.content.find_similar",
  "params": {
    "vertex_id": "<blake3-hash>",
    "session_id": "<source-session>",
    "max_results": 50
  },
  "id": 1
}
```

```json
{
  "jsonrpc": "2.0",
  "method": "dag.content.find_by_pattern",
  "params": {
    "event_type": "compute.step",
    "metadata_keys": ["model", "precision", "batch_size"],
    "max_results": 50
  },
  "id": 2
}
```

### 3. Contribute Domain-Specific LSH Features

Different domains may benefit from different LSH input features. Springs
can propose domain-specific additions to the LSH function:

| Spring | Proposed Feature | Rationale |
|--------|-----------------|-----------|
| neuralSpring | `model_architecture` | Group similar model runs |
| wetSpring | `variable_set` hash | Group similar climate analyses |
| airSpring | `crop_type` + `growth_stage` | Group phenologically similar computations |
| groundSpring | `soil_texture_class` | Group by soil similarity |
| healthSpring | `measurement_domain` | Group by health data category |
| hotSpring | `device_class` | Group by hardware similarity |
| ludoSpring | `game_type` + `player_count` | Group similar game sessions |

To propose a feature, add an entry to `SPRING_EVOLUTION_ISSUES.md` with:
- The proposed LSH input field(s)
- Expected bucket sizes (how many vertices would share a hash?)
- Use case (what cross-session discovery does this enable?)

---

## Experiment Phases for Springs

### Phase A: Structural Audit (Any Spring, Now)

Audit your current vertex production. For each session your Spring creates
in rhizoCrypt, document:

1. What event types do you emit?
2. What metadata keys are consistent across sessions?
3. How many vertices per session?
4. Do you reuse sessions, or create fresh ones per invocation?

This requires no code changes — it's an analysis exercise.

### Phase B: Schema Consistency (After rhizoCrypt Phase 1)

Once rhizoCrypt ships the `content-index` feature:

1. Ensure your event types follow `{domain}.{action}` naming
2. Normalize metadata key sets (remove optional keys from LSH consideration)
3. Run test workloads and check bucket distribution via
   `dag.content.find_by_pattern`

### Phase C: Cross-Session Discovery (After rhizoCrypt Phase 2)

Build domain-specific features on top of the content index:

- **neuralSpring**: Find similar training runs across experiments
- **wetSpring**: Discover climate analysis sessions with similar variable sets
- **airSpring**: Track crop model convergence across growing seasons
- **groundSpring**: Compare soil profile analyses across sites
- **healthSpring**: Aggregate similar health assessments
- **hotSpring**: Correlate GPU workload patterns across devices
- **ludoSpring**: Match gameplay patterns for analysis

---

## Data Privacy Considerations

The content index reveals structural patterns, not content:

- **Event types** are domain-level categories (not sensitive)
- **Metadata keys** reveal schema, not values
- **Agent prefixes** are already public (DID-based)
- **Parent count** reveals topology, not content

Springs handling sensitive data (healthSpring, etc.) should evaluate whether
structural similarity patterns could leak information in their specific
domain. If so, they can opt out of the content index by not enabling the
feature gate.

---

## Timeline

| Phase | When | Who |
|-------|------|-----|
| Spec review | Now | All Springs |
| Phase A: Structural audit | Spring sprint cycles | Individual Springs |
| Phase 1: LSH + redb table | Next rhizoCrypt sprint | rhizoCrypt team |
| Phase B: Schema consistency | After Phase 1 ships | Springs with rhizoCrypt sessions |
| Phase 2: Query integration | rhizoCrypt sprint +1 | rhizoCrypt team |
| Phase C: Domain features | After Phase 2 ships | Individual Springs |
| Phase 3: Capability discovery | rhizoCrypt sprint +2 | rhizoCrypt + biomeOS |

---

## Related Documents

- `rhizoCrypt/specs/CONTENT_INDEX_EXPERIMENT.md` — Full technical spec
- `wateringHole/SPRING_AS_PROVIDER_PATTERN.md` — How Springs register capabilities
- `wateringHole/SPRING_PROVENANCE_TRIO_INTEGRATION_PATTERN.md` — rhizoCrypt + LoamSpine + sweetGrass pattern
- `wateringHole/SPRING_EVOLUTION_ISSUES.md` — Issue tracker for cross-primal coordination

---

*Collisions are connections. The index reveals the mycelium.*
