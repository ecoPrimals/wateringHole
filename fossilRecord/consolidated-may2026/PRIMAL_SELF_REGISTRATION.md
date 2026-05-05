# Primal Self-Registration Pattern

**Version:** 1.0.0
**Date:** April 28, 2026
**Origin:** primalSpring Phase 48 — Tower Discovery Gap Analysis
**License:** AGPL-3.0-or-later

---

## The Problem

When a NUCLEUS deploys, 11 primals start and serve on UDS. But none of them
register with Songbird (the discovery primal in Tower). The result:

- `ipc.list` returns empty — no primal knows about any other primal
- Capability resolution only works via filesystem (hardcoded socket paths)
- Primals can't discover each other at runtime without external help

**Today's workaround:** The composition launcher (`composition_nucleus.sh`)
registers all primals with Songbird post-startup. This works but means the
composition layer does what primals should do themselves.

## The Pattern

Every primal should self-register at startup. The key principle:
**primals don't know Songbird exists**. They discover a generic "discovery"
capability and register with whatever provides it.

### Startup Sequence

```
1. Start UDS server (existing behavior)
2. Probe for discovery capability:
   a. Check DISCOVERY_SOCKET env var
   b. Fall back to {SOCKET_DIR}/discovery-{FAMILY_ID}.sock
   c. Fall back to {XDG_RUNTIME_DIR}/biomeos/discovery-{FAMILY_ID}.sock
3. If found:
   - Send ipc.register with own primal_id, capabilities, endpoint
   - Log "registered with Tower discovery"
4. If not found:
   - Continue in standalone mode (existing behavior)
   - Log "no discovery service — standalone mode"
```

### The IPC Call

```json
{
  "jsonrpc": "2.0",
  "method": "ipc.register",
  "params": {
    "primal_id": "barracuda",
    "capabilities": ["tensor", "math", "stats", "linalg", "ml"],
    "endpoint": "unix:///run/user/1000/biomeos/barracuda-{family_id}.sock"
  },
  "id": 1
}
```

Response:

```json
{
  "jsonrpc": "2.0",
  "result": {
    "capabilities": ["tensor", "math", "stats", "linalg", "ml"],
    "native_endpoint": "unix:///.../barracuda-{family_id}.sock",
    "virtual_endpoint": "/primal/barracuda"
  },
  "id": 1
}
```

### Capability Resolution (for consumers)

Once registered, any primal can resolve capabilities through Tower:

```json
{"method": "ipc.resolve",    "params": {"capability": "tensor"}}
{"method": "ipc.discover",   "params": {"capability": "dag"}}
{"method": "ipc.resolve_by_name", "params": {"name": "barracuda"}}
```

This is **port-free, name-free discovery**. A primal asks "who provides
tensor math?" and gets a UDS endpoint back. No ports. No hardcoded names.

## Environment Variables

| Variable | Purpose | Set By |
|----------|---------|--------|
| `DISCOVERY_SOCKET` | Path to discovery capability socket | Composition launcher |
| `BIOMEOS_SOCKET_DIR` | Shared socket directory | Composition launcher |
| `FAMILY_ID` | Socket namespace | Composition launcher |

The composition launcher already exports `DISCOVERY_SOCKET`. Primals that
evolve self-registration will find it immediately.

## Niche Alignment

Most primals already declare `discovery.register` as a niche dependency:

```rust
NicheDependency {
    capability: "discovery.register",
    required: false,
    fallback: "skip",
}
```

The self-registration implementation should honor this: probe, register if
available, skip if not. `required: false` means standalone mode always works.

## Verified Live

Tested against Desktop NUCLEUS (April 2026):

- 10/10 primals registered via composition launcher
- 17/17 capability lookups resolve correctly through Songbird
- `ipc.resolve`, `ipc.discover`, `ipc.resolve_by_name` all functional
- Zero ports. Pure UDS. Full service mesh.

## Per-Primal Capabilities

| Primal | Capabilities |
|--------|-------------|
| BearDog | security, crypto, btsp, encryption, genetic, secrets, tls |
| Songbird | discovery, ipc, http, stun, igd, mesh, relay, onion, punch |
| ToadStool | compute |
| barraCuda | tensor, math, stats, linalg, spectral, activation, ml, fhe, noise |
| coralReef | shader, gpu_compile |
| NestGate | storage |
| rhizoCrypt | dag, merkle, provenance |
| loamSpine | ledger, certificate, bonding, anchor, proof |
| sweetGrass | attribution, braid, provenance, compression, contribution |
| Squirrel | ai, inference, context, tool, graph |
| petalTongue | visualization, motor, sensor, interaction, modality, audio |

## Implementation Priority

1. **BearDog + Songbird** — Tower should self-wire (Songbird registers BearDog, BearDog finds Songbird via env)
2. **NestGate, rhizoCrypt** — Nest primals benefit most from discovery (cross-references)
3. **barraCuda, ToadStool** — Node primals for compute delegation
4. **All others** — follow the same pattern

The composition launcher handles this today. Primals evolve self-registration
as they're able, and the launcher gracefully becomes a no-op for registered
primals.
