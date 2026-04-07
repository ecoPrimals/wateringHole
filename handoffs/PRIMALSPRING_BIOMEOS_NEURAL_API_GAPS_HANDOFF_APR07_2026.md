# biomeOS Neural API Gaps — primalSpring Handoff

**Date**: 2026-04-07
**From**: primalSpring (coordination spring)
**To**: biomeOS team
**Context**: esotericWebb garden composition, cross-spring acceleration

---

## Summary

esotericWebb (first gen4 garden) and all springs depend on biomeOS Neural API
for graph-based composition. Two gaps block reliable orchestrated deployment.
These are the highest priority primal evolutions for garden readiness.

---

## GAP-017: neural-api fails to start in benchScale (CRITICAL)

**Source**: esotericWebb `EVOLUTION_GAPS.md` GAP-017

**Evidence**: In a benchScale `tower-2node` live run, BearDog and Songbird
come up `LIVE`, but biomeOS `neural-api` is `ZOMBIE` (fails health check
after startup). This blocks the "biomeOS-orchestrated composition" use case
where graphs are submitted to neural-api and routed to primals.

**Impact**: All consumers (Webb, wetSpring, ludoSpring) that want to use
`graph.execute` or `capability.call` routing fall back to direct primal IPC.
Webb works around this via `PrimalBridge` direct discovery, but loses the
composition graph execution model. wetSpring's provenance trio calls via
`capability.call` degrade gracefully but miss the Neural API orchestration
layer.

**Expected**: biomeOS neural-api starts healthy in benchScale topologies and
responds to `health.liveness` within the configured timeout.

**Current workaround**: Gardens and springs compose directly to primals via
their own discovery + bridge, bypassing biomeOS orchestration entirely.

**Ask**: Investigate the benchScale startup sequence. Is neural-api failing
on a missing dependency (NestGate? Songbird mesh?)? Is the health check
timeout too aggressive for the startup ordering? A fix here unblocks all
graph-based composition for gardens.

---

## GAP-018: Neural API executor exposure (HIGH) — PARTIALLY RESOLVED

**Source**: esotericWebb `EVOLUTION_GAPS.md` GAP-018

**Original claim**: `ConditionalDag`, `Pipeline`, `ContinuousExecutor`, and
`PathwayLearner` are not exposed as JSON-RPC methods.

**Current state** (verified in `biomeos-atomic-deploy` routing.rs):

| Executor | JSON-RPC method | Status |
|----------|----------------|--------|
| Pipeline | `graph.execute_pipeline` | EXPOSED |
| ContinuousExecutor | `graph.start_continuous`, `graph.pause_continuous`, `graph.resume_continuous`, `graph.stop_continuous` | EXPOSED |
| PathwayLearner | `graph.suggest_optimizations` | PARTIALLY — exposed as suggest, but `pathway.learn` / `pathway.suggest` not present as named in gap |
| ConditionalDag | *(none — dispatched via `graph.execute` when coordination = ConditionalDag)* | NOT A SEPARATE RPC — uses `graph.execute` path |

**What's resolved**: Pipeline and ContinuousExecutor are now on JSON-RPC.
This is the majority of what Webb needs for its storytelling loop (player
input -> narrate -> evaluate -> push scene -> repeat).

**What remains**:
1. **ConditionalDag as named RPC**: Currently handled implicitly by
   `graph.execute`. If consumers need to distinguish ConditionalDag execution
   from Sequential, a `graph.execute_conditional` method would make the API
   explicit. Low priority — `graph.execute` handles it.
2. **PathwayLearner `pathway.learn` / `pathway.suggest`**: The gap expected
   these as separate domain methods. Currently only
   `graph.suggest_optimizations` exists. If adaptive graph optimization is
   needed, `pathway.learn` (submit execution trace) and `pathway.suggest`
   (get optimized routing) should be exposed. Medium priority.

**Ask**: Update esotericWebb's `EVOLUTION_GAPS.md` GAP-018 to reflect the
partial resolution. Consider whether `pathway.learn` / `pathway.suggest`
named methods are needed for the upcoming RootPulse optimization work.

---

## GAP-017 is the real blocker

GAP-018 is mostly resolved in code. Even if Pipeline and ContinuousExecutor
RPCs exist, they are unusable if neural-api is ZOMBIE (GAP-017). Fixing
GAP-017 unblocks:

- esotericWebb graph-based orchestration (currently uses PrimalBridge workaround)
- wetSpring provenance trio via `capability.call` (currently degrades gracefully)
- Cross-spring ecology graphs (primalSpring exp080)
- RootPulse commit/branch/merge/diff/federate workflows
- All garden deploy graphs that include biomeOS as orchestrator node

---

## Related context

- Trio witness evolution complete — `WireWitnessRef` standardized across
  rhizoCrypt, loamSpine, sweetGrass. See
  `PRIMALSPRING_TRIO_WITNESS_HARVEST_HANDOFF_APR07_2026.md`.
- RootPulse graphs exist in `biomeOS/graphs/` and wire the trio correctly.
- primalSpring exp075 (biomeOS live), exp080 (cross-spring ecology) validate
  biomeOS graph execution when neural-api is healthy.
- biomeOS version: 0.1.0 (workspace), edition 2024.
