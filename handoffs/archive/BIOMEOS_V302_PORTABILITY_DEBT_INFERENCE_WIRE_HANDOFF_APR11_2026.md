# biomeOS v3.02 — Portability Debt Audit Response + Inference Wire

**Date:** April 11, 2026
**Source:** primalSpring portability debt audit (April 11, 2026)
**Scope:** biomeOS BM-* monitoring gap + Squirrel inference wire infrastructure

---

## Context

primalSpring portability debt audit reported:

1. **biomeOS BM-01 through BM-11**: All RESOLVED. Monitor `capability.resolve`
   consumption by springs now that Songbird provides it.
2. **Squirrel**: Needs `inference.register_provider` wire method, stable ecoBin
   binary, canonical `inference.*` namespace consumption. Defined by Songbird
   Wave 134.

This handoff documents biomeOS v3.02 changes that resolve both items.

---

## 1. capability.resolve Metrics/Monitoring (BM-* Monitoring Gap — RESOLVED)

**Problem:** `capability.resolve` had only a `debug!` log — no `RoutingMetrics`,
no visibility into which springs consume it, no latency tracking. In contrast,
`capability.route` had full metrics instrumentation.

**Fix:** `resolve()` now records `RoutingMetrics` on every call:
- Success path: capability, endpoint, primals routed through, latency
- Failure path: capability, error message, latency
- All metrics appear in `capability.metrics` / `neural_api.get_routing_metrics`
- Upgraded from `debug!` to `info!` on success for operational visibility

**Handler:** `crates/biomeos-atomic-deploy/src/handlers/capability.rs`
**Route:** `"capability.resolve"` → `Route::CapabilityResolveSingle`

**Monitoring:** Springs calling `capability.resolve` now appear in the
`capability.metrics` response. Dashboard consumers (ludoSpring, primalSpring)
can track resolution patterns, latency, and failure rates per capability domain.

---

## 2. inference.register_provider Wire Method (Squirrel Gap — RESOLVED)

**Problem:** neuralSpring (and other inference backends) could not register
themselves as providers. Squirrel's routing depended on runtime socket discovery
but had no structured registration path.

**Fix:** New `inference.register_provider` JSON-RPC method:

```json
{
  "jsonrpc": "2.0",
  "method": "inference.register_provider",
  "params": {
    "name": "neuralSpring",
    "endpoint": "/run/biomeos/neuralspring.sock",
    "capabilities": ["complete", "embed", "models"]
  },
  "id": 1
}
```

Response:
```json
{
  "registered": true,
  "name": "neuralSpring",
  "endpoint": "/run/biomeos/neuralspring.sock",
  "capabilities": ["complete", "embed", "models"]
}
```

**Behavior:**
- Re-registration replaces existing entry (idempotent, safe for restarts)
- Default capabilities: `["complete", "embed", "models"]` if not specified
- Also registers through `capability.register` for standard discovery
- Provider health tracked (`healthy: true` on registration)

**Handler:** `crates/biomeos-atomic-deploy/src/handlers/inference.rs`
**Route:** `"inference.register_provider"` → `Route::InferenceRegisterProvider`

---

## 3. Canonical inference.* Namespace Expansion (RESOLVED)

**Problem:** Only `inference.schedule` and `inference.gates` existed. Springs
and Squirrel needed `inference.complete`, `inference.embed`, `inference.models`
as first-class routes (not just semantic fallback).

**Fix:** 5 new routes added (7 total `inference.*` methods):

| Method | Route | Handler |
|--------|-------|---------|
| `inference.schedule` | `InferenceSchedule` | Cross-gate VRAM-aware scheduling |
| `inference.gates` | `InferenceGates` | List gates with GPU capabilities |
| `inference.register_provider` | `InferenceRegisterProvider` | Register inference backend |
| `inference.providers` | `InferenceProviders` | List registered providers |
| `inference.complete` | `InferenceComplete` | Route completion to best provider |
| `inference.embed` | `InferenceEmbed` | Route embedding to best provider |
| `inference.models` | `InferenceModels` | List models across providers |

**Routing strategy:** `inference.complete`, `inference.embed`, `inference.models`
first check the dedicated provider registry (populated by `inference.register_provider`).
If no healthy provider exists, they fall back to capability-layer discovery
(`router.discover_capability("inference")`), which finds Squirrel via standard
socket scanning.

**Handler:** `crates/biomeos-atomic-deploy/src/handlers/inference.rs`
**Routing:** `crates/biomeos-atomic-deploy/src/neural_api_server/routing.rs`

---

## For Squirrel Team

biomeOS now provides the full wire infrastructure Squirrel needs:

1. **`inference.register_provider`** — neuralSpring can call this to register
   itself as an inference backend. Squirrel can also call this if it wants to
   advertise itself as the canonical inference router.

2. **`inference.complete` / `inference.embed` / `inference.models`** — these
   route to the best registered provider. If Squirrel registers as a provider,
   it receives these requests. If neuralSpring registers, requests go there
   instead (or fall back to Squirrel via capability discovery).

3. **`inference.providers`** — Squirrel can query this to see which backends
   are registered and their health status.

**Next:** Squirrel should:
- Implement `inference.register_provider` acceptance (register neuralSpring)
- Route `inference.complete` → Ollama/API backends
- Consume canonical `inference.*` namespace per wateringHole §7

---

## For neuralSpring Team

The wire is live. neuralSpring can now:

1. Call `inference.register_provider` on biomeOS Neural API to register itself
2. biomeOS will route `inference.complete` / `inference.embed` / `inference.models`
   to neuralSpring's endpoint
3. No discovery heuristics needed — explicit registration via JSON-RPC

---

## Tests Added

| Area | Count | Coverage |
|------|-------|----------|
| `capability.resolve` handler | 8 | Missing params, domain alias, registered cap, metrics logging, failure metrics |
| `capability.resolve` routing | 2 | Success path, missing capability error |
| `inference.register_provider` handler | 6 | Success, custom caps, missing fields, replacement, provider listing |
| `inference.*` routing | 7 | All 5 new routes + error paths |
| **Total** | **23** | |

---

## Quality Gates

- 7,749 tests (0 failures)
- clippy PASS (pedantic + nursery, `-D warnings`)
- fmt PASS
- doc PASS
- `cargo deny check` PASS
