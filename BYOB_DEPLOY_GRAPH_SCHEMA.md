<!--
SPDX-License-Identifier: AGPL-3.0-or-later
Documentation and creative text in this file: CC-BY-SA-4.0
-->

# BYOB Deploy Graph TOML Schema

**Status:** Standard
**Date:** April 3, 2026
**Version:** 1.0
**License:** AGPL-3.0-or-later

The canonical TOML schema for Build Your Own Biome (BYOB) deploy graphs in
the ecoPrimals ecosystem. Springs, gardens, and primals independently
implement parsing from this spec. No shared crate — this document is the
shared artifact.

---

## Purpose

A BYOB deploy graph declares what primals a composition needs, in what order,
with what capabilities, and with what health contracts. It is used by:

- **Springs** to validate primal composition (parse, structural validate,
  topological order, discover, probe health)
- **Gardens** to declare product deployments (what primals the product needs)
- **biomeOS** to orchestrate runtime startup (ingesting the TOML and spawning
  primals in dependency order)

BYOB graphs describe **what** to deploy. biomeOS execution graphs
(`[[nodes]]` / `[[graph.nodes]]`) describe **how** to execute. biomeOS should
ingest BYOB graphs by converting them to execution graphs internally.

---

## Schema

### Top-Level Structure

```toml
[graph]
name = "my_niche_deploy"
description = "Human-readable description of this composition"
version = "1.0.0"
coordination = "sequential"

[[graph.node]]
# ... one or more nodes
```

The top-level table is `[graph]`. Nodes are an array of tables under
`[[graph.node]]` (note: singular `node`, not `nodes`).

### `[graph]` Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | String | Yes | — | Graph identifier (snake_case, e.g. `"ludospring_tower_deploy"`) |
| `description` | String | No | `""` | Human-readable description |
| `version` | String | No | `""` | Semantic version of this graph |
| `coordination` | String | No | `null` | Coordination pattern: `"sequential"`, `"parallel"`, `"continuous"` |

### `[[graph.node]]` Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | String | Yes | — | Primal name (e.g. `"beardog"`, `"ludospring"`) |
| `binary` | String | Yes | — | Binary to invoke (e.g. `"beardog_primal"`, `"ludospring"`) |
| `order` | Integer | Yes | — | Startup order (lower = earlier; nodes with same order start in parallel) |
| `required` | Boolean | No | `false` | If `true`, deployment fails when this node can't start |
| `spawn` | Boolean | No | `true` | If `false`, node is pre-existing (e.g. biomeOS substrate); not spawned by harness |
| `depends_on` | Array of String | No | `[]` | Node names that must be healthy before this one starts |
| `health_method` | String | Yes | — | JSON-RPC method to probe health (e.g. `"health.liveness"`, `"health.check"`) |
| `by_capability` | String | No | `null` | Capability domain for discovery resolution (e.g. `"security"`, `"game"`, `"ai"`) |
| `capabilities` | Array of String | No | `[]` | Specific capabilities this node provides (e.g. `["crypto.sign", "crypto.verify"]`) |
| `args` | Array of String | No | `[]` | CLI arguments passed to the binary (e.g. `["server"]`, `["serve"]`) |
| `fallback` | String | No | `null` | Fallback behavior when node fails: `"skip"` (continue without) |
| `port` | Integer | No | `null` | TCP port hint for network-based discovery |

### Node Name Convention

Node names are lowercase, no hyphens: `beardog`, `songbird`, `ludospring`,
`esotericwebb`, `biomeos_neural_api`. The name is used as the key in
`depends_on` arrays.

### Capability Naming

Capabilities follow the semantic method naming standard:
`domain.verb[.variant]`. Examples:

- `crypto.sign`, `crypto.verify`, `crypto.identity`
- `game.evaluate_flow`, `game.begin_session`
- `ai.query`, `ai.suggest`, `ai.analyze`
- `visualization.render.scene`, `visualization.render.dashboard`
- `dag.session.create`, `dag.event.append`

See `SEMANTIC_METHOD_NAMING_STANDARD.md` for the full convention.

---

## Phase Convention

BYOB graphs follow a phased structure:

| Phase | What | Convention |
|-------|------|-----------|
| 0 | biomeOS substrate | `spawn = false`, `required = true`, `order = 0` |
| 1 | Tower Atomic | BearDog + Songbird, `required = true`, `order = 1-2` |
| 2-N | Extensions | Domain primals, `required` varies, `order = 3+` |
| N+1 | Product | The spring/garden binary, `required = true` |
| 99 | Validation | Optional health check node, `spawn = false`, `order = 99` |

Phase 0 (biomeOS) is always present and always `spawn = false` — it is a
pre-existing substrate that the graph runs on top of.

---

## Topological Ordering

Nodes can be grouped into **waves** using Kahn's algorithm on the dependency
graph (`depends_on`). Nodes in the same wave have no mutual dependencies and
can start in parallel. The `order` field is a hint; the actual startup order
is determined by dependency resolution.

**Invariants:**
- `biomeos_neural_api` is always in wave 0 (no dependencies)
- Tower primals (BearDog, Songbird) are in wave 1
- The dependency graph must be acyclic (cycles are structural errors)
- Every target in `depends_on` must exist as a node `name` in the graph

---

## Health Contract

The `health_method` field specifies the JSON-RPC method a harness calls to
determine if a node is healthy. The canonical method is `health.liveness`.

**Expected response format:**

```json
{
  "jsonrpc": "2.0",
  "result": {
    "name": "<primal_name>",
    "status": "healthy",
    "version": "<semantic_version>",
    "capabilities": ["domain.method_one", "domain.method_two"]
  },
  "id": 1
}
```

**Field normalization:** The response MUST include `name` (matching the node
name in the graph). Some implementations return `primal` instead of `name` —
both should be accepted by consumers, but `name` is canonical.

---

## Structural Validation Rules

A valid BYOB deploy graph satisfies:

1. `graph.name` is non-empty
2. `graph.node` contains at least one node
3. Every node has a non-empty `name` and `binary`
4. Every node has a non-empty `health_method`
5. Every entry in `depends_on` references an existing node `name`
6. The dependency graph is acyclic
7. Node names are unique within the graph

---

## Example: Minimum Viable BYOB Graph

```toml
[graph]
name = "example_tower_deploy"
description = "Minimum viable: biomeOS + Tower + your binary"
version = "1.0.0"
coordination = "sequential"

[[graph.node]]
name = "biomeos_neural_api"
binary = "biomeos"
order = 0
required = true
spawn = false
health_method = "graph.list"
by_capability = "orchestration"
capabilities = ["graph.deploy", "capability.discover"]

[[graph.node]]
name = "beardog"
binary = "beardog_primal"
order = 1
required = true
depends_on = ["biomeos_neural_api"]
health_method = "health.check"
by_capability = "security"
capabilities = ["crypto.sign", "crypto.verify", "crypto.identity"]

[[graph.node]]
name = "songbird"
binary = "songbird_primal"
order = 2
required = true
depends_on = ["biomeos_neural_api"]
health_method = "health.check"
by_capability = "discovery"
capabilities = ["net.discovery", "net.mesh"]

[[graph.node]]
name = "your_binary"
binary = "your_binary"
order = 3
required = true
depends_on = ["beardog", "songbird"]
args = ["serve"]
health_method = "health.liveness"
by_capability = "your_domain"
capabilities = ["your_domain.method_one", "your_domain.method_two"]
```

---

## Relationship to biomeOS Execution Graphs

biomeOS execution graphs (`[[nodes]]` / `[[graph.nodes]]`) use a different
field schema optimized for runtime orchestration (budgets, gates, feedback).
The relationship:

| BYOB field | biomeOS execution equivalent |
|------------|----------------------------|
| `name` | `id` |
| `binary` | (resolved from capability registry) |
| `order` | (computed from dependency graph) |
| `depends_on` | (edges in execution graph) |
| `by_capability` | `capability` |
| `capabilities` | (registered at startup via `capability.register`) |
| `health_method` | (health probe configuration) |
| `required` | (failure handling configuration) |
| `spawn` | (pre-existing vs spawned) |

biomeOS should accept BYOB TOML by detecting `[[graph.node]]` (vs `[[nodes]]`
or `[[graph.nodes]]`) and converting to its internal execution schema.

---

## Implementations

This schema is independently implemented by:

- **primalSpring** (`ecoPrimal/src/deploy/mod.rs`) — canonical first implementation
- **ludoSpring** (`barracuda/src/deploy/mod.rs`) — independent game science validation
- **esotericWebb** (`graphs/*.toml`) — product deploy graphs consumed by launcher
- **biomeOS** — pending `[[graph.node]]` ingestion (GAP-020)

No implementation imports another. Each parses the same TOML schema from this
spec. Schema drift is caught by cross-validation: `primalspring validate-graph`
(when implemented) checks any TOML against this standard.

---

## References

- `SEMANTIC_METHOD_NAMING_STANDARD.md` — capability naming convention
- `CAPABILITY_BASED_DISCOVERY_STANDARD.md` — discovery and resolution
- `PRIMAL_SPRING_GARDEN_TAXONOMY.md` — layer responsibilities
- `primalSpring/graphs/spring_byob_template.toml` — BYOB template with comments
