# primalSpring v0.9.14 — Composition Gateway + Upstream Validation Handoff

**Date**: April 13, 2026
**Owner**: primalSpring
**For**: All primals (esp. barraCuda, NestGate, biomeOS) + downstream springs
**License**: AGPL-3.0-or-later

---

## What Changed (primalSpring local)

### 1. CompositionContext Gateway Routing

Refactored `CompositionContext` with `CapabilityRoute` enum:
- **`Direct`**: UDS or TCP `PrimalClient` (existing behavior)
- **`Gateway`**: Routes through biomeOS `capability.call` JSON-RPC

When `REMOTE_GATE_HOST` is set, `from_live_discovery_with_fallback()` creates
gateway routes for all missing capabilities. This discovers **9 capabilities**
through biomeOS (security, discovery, compute, tensor, shader, storage, ai, dag, commit).

### 2. capability.call Wire Contract Fix

`neural_api_capability_call()` was sending `{ domain, params }` but biomeOS
expects `{ capability, args }`. Fixed — all routing experiments now reach biomeOS
correctly.

### 3. Experiment Evolution

| Experiment | Change | Result |
|------------|--------|--------|
| exp085 | `multi_protocol_health` Songbird pre-check | ALL PASS (5 skips) |
| exp087 | `capability.call` params fixed; discovery shape updated | **5/5 ALL PASS** |
| exp090 | `localhost` → `tower_host()` + multi-protocol probes | **2/2 ALL PASS** |
| exp094 | Gateway routing + new checks: `tensor.batch.submit`, `storage.store_blob`, `storage.retrieve_range`, `storage.object.size`, `storage.namespaces.list` | 1/16 PASS (9 caps) |
| exp095 | **NEW** — Proto-nucleate parity template for downstream springs | Template ready |

### 4. benchScale Deploy Script

Added Phase 4 to `deploy-ecoprimals.sh`: enumerates TOML graphs on each node
and sends `graph.load` JSON-RPC to biomeOS post-health-check.

---

## Upstream Evolution Absorbed (Pulls April 13)

### barraCuda (Sprint 42 Phases 5-9)

- **4,377 tests**, 32 JSON-RPC methods, ~80.5% coverage
- `tensor.batch.submit` — fused pipeline (new 32nd method)
- LD-05: TCP bind-before-discovery in UDS mode
- LD-10: BTSP guard line replay for non-BTSP clients
- `TENSOR_WIRE_CONTRACT.md` for typed extractors

### NestGate (Session 43e-43k)

- **11,816 tests**, 47 UDS methods, ~80% coverage
- **Streaming storage**: `store_blob`, `retrieve_blob`, `retrieve_range`, `object.size`
- **Namespace isolation**: optional `namespace` on all `storage.*`, `namespaces.list`
- **Zero `async-trait`**, zero `Box<dyn Error>` in production
- `capability_registry.toml` with 12 groups + `normalize_method()`

### biomeOS (v3.05-v3.08)

- **7,784 tests**, 33 capabilities, zero C dependencies
- `--tcp-only` mode for Docker/mobile substrates
- `graph.execute` cross-gate semantics aligned with `capability.call`
- `composition.health` probes Songbird `mesh.status`
- `PrimalOperationExecutor` native async traits (partial: 71 remaining)

---

## Remaining Open Gaps

| Priority | Gap | Owner |
|----------|-----|-------|
| Medium | biomeOS UDS forwarding in Docker (primals must register TCP endpoints) | biomeOS |
| Medium | `BatchGuard` migration guide for springs | barraCuda |
| Low | 29 shader absorption candidates | barraCuda/neuralSpring |
| Low | RAWR GPU kernel (CPU-only) | barraCuda/groundSpring |
| Low | Batched `OdeRK45F64` | barraCuda/airSpring |

---

## For Downstream Springs

**exp095** (`experiments/exp095_proto_nucleate_template/`) is a starter crate.
Copy it, replace the niche parity section with your domain-specific checks, and
run against a live composition. Uses `CompositionContext::from_live_discovery_with_fallback()`
so it works on both native (UDS) and Docker (biomeOS gateway) deployments.

See also `graphs/downstream/NICHE_STARTER_PATTERNS.md` for per-spring examples.

---

**License**: AGPL-3.0-or-later
