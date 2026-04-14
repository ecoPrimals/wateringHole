# biomeOS Forwarding Architecture — Tower Atomic Is the Electron

**Date**: April 13, 2026
**From**: primalSpring (benchScale validation)
**For**: biomeOS team
**License**: AGPL-3.0-or-later

---

## Core Architectural Principle

**biomeOS MUST NOT do its own HTTP or direct socket forwarding to primals.**

Tower Atomic (BearDog + Songbird) is the ecosystem's communication substrate —
the electron. Every primal-to-primal and gate-to-gate call flows through Tower.
This is not optional. This is the architecture.

Any HTTP implementation outside Tower Atomic pulls in C dependencies (ring,
openssl, hyper). The entire ecosystem's zero-C-dependency stance depends on
Tower being the sole transport layer. biomeOS doing its own forwarding breaks
the model at the foundation.

---

## What biomeOS Should Do

When biomeOS receives `capability.call(security, crypto.hash, {...})`:

```
1. biomeOS asks Songbird: "who provides security?"
      → Songbird mesh discovery → "beardog at tcp://...:9100"

2. biomeOS delegates to Tower: "route this to beardog"
      → Songbird relays through mesh
      → BearDog authenticates via BTSP
      → call arrives at beardog with method "crypto.hash" (no prefix)

3. Result flows back through Tower → biomeOS → caller
```

biomeOS is the *orchestrator*. Tower is the *transport*. biomeOS decides
what should happen (capability routing, graph execution, topology management).
Tower decides how it gets there (mesh routing, BTSP security, protocol negotiation).

---

## What biomeOS Should NOT Do

- Build socket paths and connect to primal UDS sockets directly
- Implement HTTP POST to reach HTTP-serving primals
- Maintain its own 5-tier socket resolution for primal discovery
- Translate method names by prepending domain prefixes

Songbird already knows every primal's location, protocol, and capabilities.
biomeOS duplicating this creates the socket alignment, naming, and protocol
mismatches we found in benchScale validation.

---

## Findings From benchScale Validation

### Problem 1: Socket Path Mismatch

biomeOS `path_builder.rs` resolves sockets via 5-tier fallback ending at
`/tmp/biomeos/{primal}-{family}.sock`. Primals create sockets at
`/tmp/{primal}.sock`. Different directories, different naming schemes.

This entire resolution layer is unnecessary if biomeOS delegates to Tower.
Songbird's mesh already knows where every primal listens.

### Problem 2: Method Name Translation

biomeOS prepends the domain as a prefix when forwarding:
`capability.call(security, crypto.hash)` → forwards `security.crypto.hash`
to BearDog. BearDog knows the method as `crypto.hash`.

The domain is a *routing key*, not part of the method namespace. Tower's
mesh handles routing. The method name passes through unmodified.

### Problem 3: Protocol Mismatch

biomeOS tries raw JSON-RPC over UDS to all primals. But:
- Songbird serves HTTP on TCP, JSON-RPC on UDS
- BearDog serves BTSP on TCP, not raw JSON-RPC

Tower already handles protocol negotiation. Songbird knows which primals
speak HTTP, which speak JSON-RPC, which speak BTSP. biomeOS doing its own
protocol detection reinvents what Tower already does.

---

## Architecture: biomeOS ↔ Tower Contract

biomeOS needs exactly **two** connections to Tower:

1. **Songbird** (discovery + mesh relay)
   - `ipc.resolve(capability)` → get primal endpoint
   - `mesh.relay(target, method, params)` → route call through mesh
   - Already available on UDS (`songbird.sock`) and HTTP (`/jsonrpc` on TCP)

2. **BearDog** (security + BTSP)
   - All security-scoped calls flow through BearDog BTSP
   - BTSP handles authentication, encryption, trust verification
   - biomeOS never sends cleartext security calls

Everything else — which primal is where, what protocol it speaks, what
socket path it uses, how to cross gates — is Tower's responsibility.

---

## Cross-Container / Cross-Gate Pattern

```
┌─── Container A ────────────┐    ┌─── Container B ────────────┐
│ biomeOS                    │    │                             │
│   ↓ capability.call        │    │  toadStool (compute)       │
│ Songbird ←→ mesh ←─────TCP────→ Songbird (mesh peer)        │
│ BearDog  ←→ BTSP ←─────TCP────→ BearDog (BTSP peer)        │
│                            │    │  barraCuda (tensor)        │
│                            │    │  nestgate (storage)        │
└────────────────────────────┘    └────────────────────────────┘
```

Songbird's mesh auto-discovers peers across containers/gates via TCP.
BearDog's BTSP secures the cross-gate channel. biomeOS talks to its local
Tower. Tower handles everything else.

---

## Immediate Workaround (primalSpring Side)

While biomeOS evolves toward Tower-routed forwarding, primalSpring's
`CompositionContext` now routes directly:

- `DirectTcp` — JSON-RPC primals reachable on TCP
- `HttpTcp` — HTTP primals (Songbird) via `POST /jsonrpc`
- `Gateway` — biomeOS `capability.call` (for when forwarding works)
- `Direct` — UDS when co-located

This is a workaround. The proper architecture is biomeOS → Tower → primal.

---

## Socket Alignment (Interim Fix)

For the current biomeOS forwarding code, `deploy-ecoprimals.sh` Phase 2.5
creates symlinks from biomeOS's expected paths to actual primal sockets:

```bash
ln -sf /tmp/songbird.sock /tmp/biomeos/songbird-${family_id}.sock
```

And the `ecoprimals-nucleus-full.yaml` topology sets `BIOMEOS_SOCKET_DIR=/tmp`
to align directories.

These are temporary. When biomeOS routes through Tower, socket path resolution
moves entirely to Songbird's mesh discovery where it belongs.

---

## Summary

| Current biomeOS Approach | Problem | Tower Atomic Solution |
|--------------------------|---------|----------------------|
| 5-tier socket path resolution | Path mismatch in Docker | Songbird mesh knows all endpoints |
| Direct UDS forwarding to primals | Socket naming + protocol mismatch | Songbird relays through mesh |
| Domain prefix on forwarded methods | Primals don't know prefixed names | Method name passes through unmodified |
| HTTP health probes | Pulls in C deps (ring/openssl) | Songbird already serves HTTP |
| BTSP socket forwarding attempts | Can't do cleartext to BearDog | BearDog IS the BTSP layer |

**Tower Atomic is the electron. Route through it.**

---

**License**: AGPL-3.0-or-later
