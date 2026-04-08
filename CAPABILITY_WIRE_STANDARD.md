# Capability Wire Standard

**Version:** 1.0.0
**Date:** April 8, 2026
**Status:** Active — all primals and springs MUST adopt this
**Authority:** wateringHole (ecoPrimals Core Standards)
**Derived from:** Live validation runs 1–4 (primalSpring Phase 26)
**Related:** `CAPABILITY_BASED_DISCOVERY_STANDARD.md`, `PRIMAL_SELF_KNOWLEDGE_STANDARD.md`, `SEMANTIC_METHOD_NAMING_STANDARD.md`

---

## Abstract

The Capability Wire Standard defines the JSON-RPC response format for primal self-advertisement over IPC. When biomeOS (or any orchestrator) sends `capabilities.list` or `identity.get` to a primal, the response MUST follow this specification. The standard enables automatic capability discovery, composition completeness validation, and AI-assisted routing without hardcoded knowledge of individual primals.

---

## Problem Statement

Prior to this standard, 5 independent wire formats evolved across the ecosystem:

| Format | Shape | Primals |
|--------|-------|---------|
| A | `result: ["method.name", ...]` (bare array) | Songbird |
| B | `result: {capabilities: [...], methods: [...], ...}` | sweetGrass |
| C | `result: {method_info: [{name, ...}]}` | (reference parser) |
| D | `result: {semantic_mappings: {domain: {method: {}}}}` | loamSpine (tests) |
| E | `result: {provided_capabilities: [{type, methods}]}` | BearDog, rhizoCrypt |

biomeOS maintained a 5-format parser to extract method names from each. Rich metadata (cost estimates, operation dependencies, consumed capabilities) was discarded. Method name translation tables introduced errors (GAP-MATRIX-09: `braid.create` mistranslated to `provenance.create_braid`). No primal advertised what it consumed, making composition validation impossible without hardcoded graphs.

---

## Specification

### 1. capabilities.list Response — Required Envelope

Every primal MUST return a JSON-RPC 2.0 response to `capabilities.list` (or the alias `capability.list`) containing AT MINIMUM:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "primal": "<canonical_name>",
    "version": "<semver_or_dev>",
    "methods": [
      "<domain>.<operation>",
      ...
    ]
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `primal` | String | **MUST** | Canonical primal name, lowercase, no spaces (e.g., `rhizocrypt`, `beardog`, `songbird`) |
| `version` | String | **MUST** | SemVer or dev version string (e.g., `0.14.0`, `0.9.0-dev`) |
| `methods` | String[] | **MUST** | Every callable JSON-RPC method, fully qualified with dotted notation (`domain.operation`). This is the primary routing signal for biomeOS. |

The `methods` array MUST contain every method the primal will accept as a JSON-RPC `method` field. If a method name appears in `methods`, the primal MUST NOT return "method not found" when that method is called (parameter validation errors are acceptable).

### 2. Structured Capabilities — Recommended

Primals SHOULD include capability grouping for structured routing and observability:

```json
{
  "result": {
    "primal": "rhizocrypt",
    "version": "0.14.0",
    "methods": ["dag.session.create", "dag.session.list", ...],
    "provided_capabilities": [
      {
        "type": "dag",
        "methods": ["session.create", "session.list", "event.append"],
        "version": "0.14.0",
        "description": "Ephemeral content-addressed DAG engine"
      }
    ]
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `provided_capabilities` | Object[] | SHOULD | Capability groups |
| `provided_capabilities[].type` | String | MUST (if group present) | Domain name (e.g., `dag`, `crypto`, `braid`) |
| `provided_capabilities[].methods` | String[] | MUST (if group present) | Short method names within this domain |
| `provided_capabilities[].version` | String | MAY | Group-level version |
| `provided_capabilities[].description` | String | MAY | Human-readable group description |

When `provided_capabilities` is present, biomeOS registers both the group type name (e.g., `dag`) and qualified names (e.g., `dag.session.create`) in its routing table.

### 3. Dependency & Cost Metadata — Optional

Primals MAY include metadata for AI advisors, composition planners, and billing:

```json
{
  "result": {
    "primal": "sweetgrass",
    "version": "0.7.27",
    "methods": [...],
    "provided_capabilities": [...],
    "consumed_capabilities": ["crypto.sign", "storage.artifact.store", "dag.session.create"],
    "cost_estimates": {
      "braid.create": { "cpu": "low", "latency_ms": 2 },
      "attribution.chain": { "cpu": "high", "latency_ms": 50 }
    },
    "operation_dependencies": {
      "anchoring.anchor": ["braid.create"],
      "attribution.chain": ["braid.create"]
    }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `consumed_capabilities` | String[] | Methods this primal needs FROM other primals. Enables composition completeness validation. |
| `cost_estimates` | Object | Per-method or per-domain cost hints (`cpu`: low/medium/high, `latency_ms`, `memory_bytes`, `gpu_eligible`). |
| `operation_dependencies` | Object | Method DAG — `{method: [prerequisite_methods]}`. Enables execution planners to sequence operations. |
| `protocol` | String | IPC protocol (e.g., `jsonrpc-2.0`) |
| `transport` | String[] | Available transports (e.g., `["uds", "tcp", "http"]`) |

### 4. identity.get — Recommended

Primals SHOULD implement the `identity.get` JSON-RPC method:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "primal": "rhizocrypt",
    "version": "0.14.0",
    "domain": "dag",
    "license": "AGPL-3.0-or-later"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `primal` | String | MUST | Same as `capabilities.list` `primal` field |
| `version` | String | MUST | Same as `capabilities.list` `version` field |
| `domain` | String | SHOULD | Primary capability domain |
| `license` | String | MAY | SPDX license identifier |

biomeOS probes `identity.get` alongside `capabilities.list` for observability. If absent, biomeOS falls back to socket-name inference.

---

## Method Naming Convention

All method names in the `methods` array MUST follow the **Semantic Method Naming Standard**:

```
<domain>.<operation>
```

- `domain`: lowercase, no dots (e.g., `dag`, `crypto`, `braid`, `health`)
- `operation`: lowercase, underscores for multi-word (e.g., `session.create`, `blake3_hash`)
- Health triad: every primal SHOULD implement `health.liveness`, `health.check`, `health.readiness`
- Meta methods: `capabilities.list`, `identity.get`

---

## biomeOS Parser Behavior

biomeOS v2.93+ reads `capabilities.list` responses with the following priority:

1. `result.methods` (this standard) → use directly, no format detection
2. `result.provided_capabilities` (Format E) → expand `type.method`
3. `result.capabilities` (Format A/B) → use directly if string array
4. `result.method_info` (Format C) → extract `name` fields
5. `result.semantic_mappings` (Format D) → traverse nested keys
6. `result` is bare array (Format A) → use directly

When `result.methods` is present, biomeOS skips format detection entirely. Legacy formats remain supported for backward compatibility but SHOULD be deprecated.

---

## Compliance Levels

### Level 1: Routable (minimum for biomeOS discovery)

- [ ] `capabilities.list` returns a response biomeOS can parse (any format A-E)
- [ ] At least one callable method is advertised
- [ ] `health.liveness` implemented

### Level 2: Standard (target for all primals)

- [ ] All Level 1 requirements
- [ ] `capabilities.list` returns `{primal, version, methods}` envelope
- [ ] `identity.get` implemented
- [ ] All methods in `methods` array are callable (no "method not found" for advertised methods)
- [ ] Method names follow Semantic Method Naming Standard

### Level 3: Composable (target for NUCLEUS-participating primals)

- [ ] All Level 2 requirements
- [ ] `provided_capabilities` grouping included
- [ ] `consumed_capabilities` declared
- [ ] `cost_estimates` for at least high-cost methods
- [ ] `operation_dependencies` for methods with prerequisites

### Current Primal Compliance (April 8, 2026)

| Primal | Level 1 | Level 2 | Level 3 | Gap |
|--------|---------|---------|---------|-----|
| BearDog | ✓ | Partial | — | Needs `methods` flat array, `identity.get` |
| Songbird | ✓ | Partial | — | Has `capabilities.methods` token→method map (Wave 123); needs `{primal, version, methods}` envelope, `identity.get` |
| rhizoCrypt | ✓ | ✓ | ✓ | Full L3: `methods`, `consumed_capabilities`, `cost_estimates`, `operation_dependencies` |
| loamSpine | ✓ | Partial | Partial | Needs top-level `methods`, `identity.get` |
| sweetGrass | ✓ | ✓ | ✓ | Full L3 compliance (April 8, 2026) |

---

## Audit Checklist

This checklist is used during primalSpring deep-debt audits and cross-spring evolution reviews:

```
CAPABILITY_WIRE_STANDARD v1.0 — Audit Checklist

Primal: ___________  Version: ___________  Date: ___________

Level 1 (Routable):
  [ ] capabilities.list responds to JSON-RPC probe over UDS
  [ ] Response parseable by biomeOS (any format)
  [ ] health.liveness responds with {status: "alive"} or {alive: true}

Level 2 (Standard):
  [ ] result contains "primal" field (canonical name)
  [ ] result contains "version" field (SemVer)
  [ ] result contains "methods" flat string array
  [ ] Every entry in "methods" is callable (returns result or param error, not method-not-found)
  [ ] Method names follow domain.operation dotted convention
  [ ] identity.get implemented and returns {primal, version}
  [ ] health.liveness, health.check, health.readiness all implemented

Level 3 (Composable):
  [ ] provided_capabilities grouping present with type + methods per group
  [ ] consumed_capabilities lists all cross-primal dependencies
  [ ] cost_estimates present for high-cost methods
  [ ] operation_dependencies present for methods with prerequisites
```

---

## What This Unlocks

### Composition Completeness Validation

With `consumed_capabilities`, biomeOS validates that a deploy graph satisfies all dependencies without hardcoded knowledge:

```
sweetGrass consumes: [crypto.sign, storage.artifact.store, dag.session.create]
BearDog provides:   [crypto.sign, ...]        ✓
NestGate provides:  [storage.artifact.store]   ✓
rhizoCrypt provides:[dag.session.create, ...]  ✓
→ Composition complete
```

### AI-Assisted Routing (Squirrel)

With `cost_estimates` and `operation_dependencies`, Squirrel can plan optimal execution:

```
Goal: anchor a provenance braid
Path: braid.create (low) → anchoring.anchor (high) → proof.generate (medium)
Total: high
```

### Self-Describing Deploy Graphs

A composition's capability surface = union of all `methods` minus all `consumed_capabilities`. No hardcoded `CapabilityTaxonomy` tables needed. biomeOS's translation layer becomes a compatibility shim, not the source of truth.

---

## Relationship to Other Standards

| Standard | Scope | Relationship |
|----------|-------|-------------|
| **UniBin** | Binary structure (subcommands, `--help`, `--version`) | Prerequisite — primal must be a UniBin |
| **ecoBin** | Build portability (pure Rust, no C deps, musl-static) | Prerequisite — primal must be an ecoBin |
| **genomeBin** | Deployment attestation (checksums, lineage) | Extends — genomeBin MAY embed capability manifest |
| **Capability Wire Standard** (this) | IPC self-advertisement | Complements — defines what the binary says about itself at runtime |
| **Semantic Method Naming** | Method name convention | Referenced — `methods` array follows this convention |

The binary ladder: **UniBin → ecoBin → genomeBin**
The runtime ladder: **health.liveness → capabilities.list (Level 1) → Standard (Level 2) → Composable (Level 3)**

---

**License**: AGPL-3.0-or-later
