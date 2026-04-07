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

## GAP-017: neural-api fails to start in benchScale — **RESOLVED**

**Source**: esotericWebb `EVOLUTION_GAPS.md` GAP-017

**Root cause** (diagnosed April 7): The bug was in `benchScale/scripts/deploy-ecoprimals.sh`,
not in biomeOS code. The `build_launch_cmd` for biomeos was:
```
BIOMEOS_HTTP_PORT=$port $DEPLOY_DIR/bin/biomeos neural-api
```
Three defects:
1. `BIOMEOS_HTTP_PORT` env var is **not read** by the `biomeos` binary — it uses `--port`
2. Without `--graphs-dir`, biomeOS defaults to `./graphs` (relative, doesn't exist in container)
3. Without `--family-id`, auto-discovery fails in container context

biomeOS's `health.liveness` handler is trivial (returns `{"status": "alive"}` with no deps),
but the server never reached the accept loop because startup stalled without graphs.

**Fix applied**: Deploy script now emits:
```
$DEPLOY_DIR/bin/biomeos neural-api --graphs-dir $DEPLOY_DIR/graphs --port $port --family-id '$family_id'
```
Health check upgraded from 5s single-shot to 15s initial grace + 3 retries at 10s intervals.

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
