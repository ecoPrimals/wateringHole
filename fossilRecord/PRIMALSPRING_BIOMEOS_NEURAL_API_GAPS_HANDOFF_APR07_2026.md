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

## GAP-019: `discover_capability` lacks domain prefix matching — **RESOLVED**

**Source**: primalSpring capability routing audit, April 7, 2026

**Issue**: `NeuralRouter::discover_capability(capability)` uses exact key
lookup in the `capability_registry` HashMap. When primals register individual
methods (e.g., `"dag.session.create"`, `"dag.event.append"`), a domain-only
query like `"dag"` fails unless `"dag"` is also explicitly registered.

**Current workaround**: Deploy graphs now include bare domain names in the
`capabilities` array alongside full method names:
```toml
capabilities = ["dag", "dag.session.create", "dag.event.append", ...]
```
This works because `load_translations_from_graph` registers every entry in
`capabilities` as a key. Graph-loaded primals are now discoverable by domain.

**Why this is still a gap**: Primals that join late via lazy socket rescan
(`probe_primal_capabilities_standalone`) only register the methods from their
`capabilities.list` response — they do NOT register synthetic domain aliases.
If a trio primal restarts after initial graph loading, `discover_capability("dag")`
fails until the next `topology.rescan`.

**Proposed fix** (one of):
1. **Prefix matching fallback** in `try_registry_lookup`: If exact key miss,
   scan for keys starting with `"{capability}."` — returns any primal whose
   methods start with the domain.
2. **Leverage `capability_domains.rs` at call time**: The fallback table
   already maps `"dag"` → `"rhizocrypt"`. Use it in `discover_capability`
   as a last resort before erroring.
3. **Auto-register domain aliases in lazy rescan**: When registering
   `"dag.session.create"` for a primal, also register `"dag"`.

Option 1 is simplest (5-10 LOC) and preserves the existing architecture.
The `discover_by_capability_category` match arms should also be extended
to include trio domains (`"dag"`, `"spine"`, `"entry"`, `"session"`,
`"braid"`, `"attribution"`, `"provenance"`, `"anchoring"`, `"certificate"`).

**Fix applied** (biomeOS v2.92): Added `try_prefix_lookup` step in
`discover_capability` that scans the registry for keys starting with
`"{domain}."`. Also added `capability_to_provider_fallback` as last resort
before erroring. Resolution order is now:
1. Exact key → 2. Lazy rescan → 3. Prefix match → 4. Composite atomics →
5. Category discovery → 6. Domain table fallback.

4 new tests cover prefix matching. Deploy graphs retain bare domain aliases
as belt-and-suspenders.

---

## Related context

- Trio witness evolution complete — `WireWitnessRef` standardized across
  rhizoCrypt, loamSpine, sweetGrass. See
  `PRIMALSPRING_TRIO_WITNESS_HARVEST_HANDOFF_APR07_2026.md`.
- RootPulse graphs exist in `biomeOS/graphs/` and wire the trio correctly.
- primalSpring exp075 (biomeOS live), exp080 (cross-spring ecology) validate
  biomeOS graph execution when neural-api is healthy.
- biomeOS version: 0.1.0 (workspace), edition 2024.
