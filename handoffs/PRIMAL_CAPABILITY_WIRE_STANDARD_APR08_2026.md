# Primal Capability Wire Standard v1.0

**Date**: April 8, 2026
**From**: primalSpring (coordination spring)
**To**: All primal teams, biomeOS team, downstream springs
**Context**: Live validation runs 1–4 exposed 5 independent wire formats for `capabilities.list`. This standard defines the convergence target.

---

## Problem

biomeOS must parse `capabilities.list` responses from every primal to build its routing table. Today it maintains a 5-format parser because each primal evolved independently:

| Format | Primal(s) | Shape | What biomeOS extracts |
|--------|-----------|-------|----------------------|
| **A** | Songbird | `result: ["network.discovery", ...]` | Method names directly |
| **B** | sweetGrass | `result: {capabilities: [...], methods: [...], domains: {...}, ...}` | `methods` or `capabilities` array |
| **C** | (reference) | `result: {method_info: [{name, ...}]}` | `method_info[].name` |
| **D** | loamSpine (tests) | `result: {semantic_mappings: {domain: {method: {}}}}` | Nested key traversal |
| **E** | BearDog, rhizoCrypt | `result: {provided_capabilities: [{type, methods}]}` | Group type + qualified `type.method` |

biomeOS ignores everything except method names. The rich metadata (cost estimates, dependencies, descriptions, versions) is discarded during routing.

---

## What Each Primal Actually Returns

### identity.get

| Primal | Implements? | Fields |
|--------|-------------|--------|
| BearDog | **No** | — |
| Songbird | **No** | — |
| rhizoCrypt | **Yes** | `primal`, `version`, `domain`, `license`, `description`, `protocol`, `transport` |
| loamSpine | **No** | — |
| sweetGrass | **Yes** | `name`, `version` |

### capabilities.list — Envelope Fields

| Field | BearDog | Songbird | rhizoCrypt | loamSpine | sweetGrass |
|-------|---------|----------|------------|-----------|------------|
| `primal` (name) | ✓ | — | ✓ | ✓ | ✓ |
| `version` | ✓ | — | ✓ | ✓ | ✓ |
| `methods` (flat array) | — | ✓ (is result) | — | — | ✓ |
| `provided_capabilities` | ✓ | — | ✓ | — | — |
| `capabilities` (flat) | — | — | — | ✓ | ✓ |
| `domains` (grouped) | — | — | — | — | ✓ |
| `descriptors` (rich) | — | — | ✓ | — | — |
| `cost_estimates` | — | — | ✓ (per method) | ✓ (structured) | ✓ (per domain) |
| `deps` / `depends_on` | — | — | ✓ | ✓ | ✓ |
| `consumed_capabilities` | — | — | — | — | ✓ |
| `operation_dependencies` | — | — | — | ✓ | ✓ |
| `description` | ✓ (per group) | — | — | — | ✓ |
| `protocol` / `transport` | ✓ | — | — | — | ✓ |
| `family_id` / `node_id` | ✓ | — | — | — | — |

### What Worked in Live Validation

biomeOS v2.93 successfully discovered capabilities from all 5 primals. The patterns that worked best:

1. **Format E** (BearDog, rhizoCrypt): biomeOS extracted both group names AND qualified method names. 38 + 33 = 71 capabilities. This format gives biomeOS the most routing information.

2. **Format A** (Songbird, loamSpine flat): Simplest to parse. biomeOS extracted all names directly. 14 + 21 = 35 capabilities. Works when method names are already fully qualified.

3. **sweetGrass dual format**: Provided BOTH `capabilities` (flat) AND `methods` (flat) AND `domains` (grouped). biomeOS picked up the flat array. The richest response overall.

---

## Convergence Standard

### Required Envelope (MUST)

Every primal's `capabilities.list` response MUST include these fields in `result`:

```json
{
  "primal": "rhizocrypt",
  "version": "0.14.0",
  "methods": [
    "dag.session.create",
    "dag.session.list",
    "health.liveness",
    "identity.get",
    "capabilities.list"
  ]
}
```

- **`primal`**: String. The primal's canonical name (lowercase, no spaces).
- **`version`**: String. SemVer or dev version.
- **`methods`**: Array of strings. Every callable JSON-RPC method name, fully qualified with dotted notation (`domain.operation`). This is what biomeOS uses for routing.

### Recommended Metadata (SHOULD)

Primals SHOULD include structured capability groups for richer routing and observability:

```json
{
  "primal": "rhizocrypt",
  "version": "0.14.0",
  "methods": ["dag.session.create", "dag.session.list", ...],
  "provided_capabilities": [
    {
      "type": "dag",
      "methods": ["session.create", "session.list", "event.append", ...],
      "version": "0.14.0",
      "description": "Ephemeral content-addressed DAG engine"
    }
  ]
}
```

- **`provided_capabilities`**: Array of group objects. Each group has:
  - `type`: String. Domain name (becomes the prefix for qualified names).
  - `methods`: Array of strings. Short method names within this domain.
  - `version`: String (optional). Group-level version.
  - `description`: String (optional). Human-readable group description.

### Optional Enrichment (MAY)

Primals MAY include additional metadata for AI advisors, monitoring, and billing:

```json
{
  "primal": "rhizocrypt",
  "version": "0.14.0",
  "methods": [...],
  "provided_capabilities": [...],
  "consumed_capabilities": ["crypto.sign", "storage.artifact.store"],
  "cost_estimates": {
    "dag.session.create": {"cpu": "low", "latency_ms": 1},
    "dag.dehydration.trigger": {"cpu": "high", "latency_ms": 50}
  },
  "operation_dependencies": {
    "dag.dehydration.trigger": ["dag.session.create", "dag.event.append"]
  },
  "protocol": "jsonrpc-2.0",
  "transport": ["uds", "tcp"]
}
```

- **`consumed_capabilities`**: What this primal needs FROM other primals. Enables biomeOS to validate composition completeness.
- **`cost_estimates`**: Per-method or per-domain cost hints. AI advisors and schedulers use this for optimization.
- **`operation_dependencies`**: Method DAG — what must be called before what. Enables graph execution planners to sequence operations.
- **`protocol`** / **`transport`**: How to reach this primal.

### identity.get Standard

Every primal SHOULD implement `identity.get` returning:

```json
{
  "primal": "rhizocrypt",
  "version": "0.14.0",
  "domain": "dag",
  "license": "AGPL-3.0-or-later"
}
```

biomeOS probes `identity.get` alongside `capabilities.list` for observability. It's gracefully optional — biomeOS falls back to socket-name inference when absent.

---

## Migration Path

### Tier 1 — Immediate (no breaking changes)

Add `methods` flat array to existing responses. Every primal already knows its method names internally.

| Primal | Work |
|--------|------|
| BearDog | Add `methods` array alongside existing `provided_capabilities` |
| Songbird | Wrap existing flat array in `{primal, version, methods}` envelope |
| rhizoCrypt | Already has both `provided_capabilities` and `descriptors` — add flat `methods` |
| loamSpine | Already has `methods` array in response — add `primal` field, promote `methods` to top level |
| sweetGrass | Already has `methods` array — already compliant after adding `primal` (has it) |

### Tier 2 — Short-term

- Add `identity.get` to BearDog, Songbird, loamSpine
- Add `provided_capabilities` grouping to Songbird, loamSpine
- Add `consumed_capabilities` to all primals that depend on others

### Tier 3 — Medium-term

- Ship `CapabilityAdvertisement` trait in `ecoBin` crate so new primals get this for free
- biomeOS prefers `methods` array when present, falls back to multi-format parser
- Deprecate Format C/D parsing (keep for backward compat, log warnings)

---

## Why Not Just Format E?

Format E (`provided_capabilities`) is the richest structured format, but it doesn't carry the flat `methods` array that biomeOS needs for routing without transformation. biomeOS must expand `type.method` from each group to build the routing table.

The standard says: **give biomeOS what it needs (flat `methods`)** AND **give observers what they want (structured groups)**. Both in the same response. The `methods` array is the shared opsin — the molecular signal every receptor can read. The `provided_capabilities` grouping is the structural diversity — different eyes for different organisms.

---

## Relationship to biomeOS Parser

biomeOS v2.93's 5-format parser remains the adaptive sensing layer. When `methods` is present, biomeOS reads it directly (O(1) parse, no format detection). When absent, biomeOS falls through to format detection (Formats A-E). Over time, as primals converge, the fallback paths become legacy.

The parser priority becomes:
1. `result.methods` (standard) → use directly
2. `result.provided_capabilities` (Format E) → expand `type.method`
3. `result.capabilities` (Format A/B) → use directly
4. `result.method_info` (Format C) → extract names
5. `result.semantic_mappings` (Format D) → traverse keys
6. `result` is array (Format A bare) → use directly

---

## What This Unlocks

### Composition Completeness Validation

With `consumed_capabilities`, biomeOS can verify that a composition graph satisfies all dependencies:

```
sweetGrass consumes: ["crypto.sign", "storage.artifact.store", "dag.session.create"]
BearDog provides: ["crypto.sign", ...]  ✓
NestGate provides: ["storage.artifact.store", ...]  ✓
rhizoCrypt provides: ["dag.session.create", ...]  ✓
→ Composition complete
```

### AI-Assisted Routing

With `cost_estimates` and `operation_dependencies`, Squirrel can plan optimal execution paths:

```
Goal: anchor a provenance braid
Path: braid.create (low) → anchoring.anchor (high, depends on braid.create) → proof.generate_inclusion (medium)
Estimated cost: low + high + medium = high
```

### Self-Describing Compositions

With the full standard, a composition's capability surface is the union of all primals' `methods` arrays minus their `consumed_capabilities`. No hardcoded knowledge needed.

---

**License**: AGPL-3.0-or-later
