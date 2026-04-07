# primalSpring v0.9.3 — Live Validation GAP-MATRIX + Primal Work Items

**Date**: April 7, 2026  
**From**: primalSpring (coordination spring)  
**To**: biomeOS team, BearDog team, Songbird team, NestGate team, provenance trio teams, Squirrel team, ToadStool team, downstream springs  
**Phase**: 26 — Mixed Composition + Live Validation Matrix

---

## Context

primalSpring ran its first systematic live validation matrix against Eastgate,
probing each primal through direct JSON-RPC IPC and through the biomeOS Neural
API. The particle model (Tower=electron, Node=proton, Nest=neutron) provides
the compositional framework. Six gap items were identified, documented in
`specs/CROSS_SPRING_EVOLUTION.md` and `specs/NUCLEUS_VALIDATION_MATRIX.md`.

This handoff assigns work to each primal team based on the gaps found.

---

## biomeOS Team — GAP-MATRIX-01 + GAP-MATRIX-02 (Critical + Medium)

### GAP-MATRIX-01: Neural API Capability Registration (CRITICAL)

**Problem**: Neural API v2 detects primal sockets and confirms them "healthy"
but reports `0 capabilities` for each. BearDog advertises 9 capability groups
via `capabilities.list` (Format A: string array). biomeOS's internal
`probe_primal_capabilities_standalone` does not extract capabilities from the
response.

**Evidence**:
```
biomeOS log: "beardog healthy with 0 capabilities"
biomeOS log: "songbird healthy with 0 capabilities"
Direct probe: BearDog capabilities.list → 9 groups (security, crypto, beacon, ...)
```

**Impact**: All `capability.call` routing fails. Direct IPC works. This blocks
the Neural API routing path that all springs and products rely on.

**Recommended Fix**: Align the capability probe in `neural_router/discovery.rs`
with the 4 wire formats primals actually use:
- Format A: `["security", "crypto", "beacon", ...]` (BearDog, Songbird)
- Format B: `[{"name": "...", "methods": [...]}]` (primalSpring)
- Format C: `{"method_info": {"group": [...]}}` (some primals)
- Format D: `{"semantic_mappings": {...}}` (semantic-aware primals)

primalSpring already has a 4-format parser in `ipc/discover.rs` → `extract_capability_names()`.

### GAP-MATRIX-02: Graph Parser (Medium)

**Problem**: biomeOS rejects `tower_atomic_bootstrap.toml` with "Failed to
parse TOML". The file is valid TOML (Python parser confirms). biomeOS may
require specific fields (e.g., `id`) or a different node structure than
`[[graph.nodes]]`.

**Recommended Fix**: Document the exact biomeOS internal TOML schema. Accept
the `[[graph.nodes]]` format or provide a migration guide.

---

## Songbird Team — GAP-MATRIX-03 (Low)

### TLS 1.3 Cipher Suite Compatibility

**Problem**: Some HTTPS targets fail TLS handshake through Songbird (httpbin.org)
while others succeed (ifconfig.me). The custom TLS 1.3 stack may not support
all cipher suites required by common servers.

**Evidence**:
```
ifconfig.me → HTTP 200 (283ms) ✓
httpbin.org → TLS handshake failure ✗
```

**Recommended Fix**: Ensure support for at minimum:
- `TLS_AES_128_GCM_SHA256`
- `TLS_AES_256_GCM_SHA384`
- `TLS_CHACHA20_POLY1305_SHA256`

The recent TLS 1.3 CSPRNG fix (rebased April 7) may be related.

---

## NestGate Team — GAP-MATRIX-04 (Medium)

### IPC Model Divergence

**Problem**: NestGate uses HTTP REST, not JSON-RPC over UDS. Every other primal
(BearDog, Songbird, Squirrel, biomeOS, primalSpring) uses JSON-RPC 2.0 over
Unix domain sockets. NestGate's `--help` has historically been unstable.

**Impact**: NestGate cannot be probed with the same `socat`/`PrimalClient` tools
used for all other primals. Integration requires a separate HTTP bridge.

**Options**:
1. **Add JSON-RPC over UDS mode** to NestGate alongside HTTP REST
2. **Build a thin bridge primal** (`nestgate-bridge`) that translates JSON-RPC ↔ HTTP
3. **Document the HTTP REST API** so primalSpring can probe it directly

Option 1 is preferred for ecosystem consistency.

---

## Provenance Trio Teams — GAP-MATRIX-05 (Medium)

### rhizoCrypt, loamSpine, sweetGrass Not Live-Tested

**Problem**: These primals were not running during the live validation matrix.
Their L0 routing through Neural API and L1 composition patterns are
structural-only (validated by primalSpring Rust code, not live IPC).

**Work**:
1. Confirm each primal starts and creates a socket
2. Verify `health.liveness` responds correctly
3. Verify `capabilities.list` returns capabilities in a format biomeOS can parse
4. Report any CLI flags needed for socket creation

Note: The provenance trio's `plasmidBin` binaries were updated April 7.

---

## Squirrel Team — GAP-MATRIX-05 (Medium)

### Squirrel Not Live-Tested

**Problem**: Squirrel uses abstract sockets (`@squirrel`) which biomeOS routes
to filesystem sockets. Not tested in this validation run.

**Work**:
1. Confirm Squirrel starts and advertises capabilities
2. Verify abstract socket is discoverable by biomeOS
3. Test `ai.health` and `capabilities.list` through Neural API

---

## ToadStool Team — GAP-MATRIX-05 (Medium)

### ToadStool Not Live-Tested

**Problem**: ToadStool is CLI-only (no persistent server mode). Not tested
in this validation run.

**Work**:
1. If a server/daemon mode exists, document the CLI flags
2. Verify `capabilities.list` returns compute capabilities
3. Test GPU capability routing through Neural API

---

## BearDog Team — Maintenance Only

BearDog passed all live probes. No action items from GAP-MATRIX.

**Validated**:
- `health.liveness` ✓ (v0.9.0)
- `crypto.sign_ed25519` ✓
- `crypto.blake3_hash` ✓
- `capabilities.list` ✓ (9 groups: security, crypto, beacon, mito, genetic, federation, secrets, hash, key)

The only work is ensuring the capability wire format is documented so biomeOS
can parse it (see GAP-MATRIX-01 — biomeOS team owns this fix).

---

## Ecosystem — GAP-MATRIX-06 (Low)

### plasmidBin Binary Freshness

Current state:
| Binary | Date | Source |
|--------|------|--------|
| primalspring_primal | Apr 7 | Rebuilt Phase 26 |
| beardog | Mar 27 | plasmidBin |
| songbird | Mar 27 | plasmidBin (Apr 7 from-source on Eastgate) |
| nestgate | Mar 28 | plasmidBin |
| squirrel | Mar 27 | plasmidBin |
| toadstool | Mar 27 | plasmidBin |
| rhizocrypt | Apr 7 | Rebuilt |
| loamspine | Apr 7 | Rebuilt |
| sweetgrass | Apr 7 | Rebuilt |
| biomeos | Apr 7 | From-source on Eastgate |

**Recommended**: Periodic `plasmidBin` rebuild from source to keep all binaries
within 1 week of latest evolution. Update `manifest.toml` + `checksums.toml`.

---

## What primalSpring Provides

For all teams, primalSpring now provides:

1. **Particle model** (`specs/MIXED_COMPOSITION_PATTERNS.md`) — compositional reasoning framework
2. **17 sketch graphs** (`graphs/sketches/`) — generic patterns for springs to specialize
3. **Validation matrix** (`specs/NUCLEUS_VALIDATION_MATRIX.md`) — systematic capability assessment
4. **4-format capability parser** (`ipc/discover.rs`) — reference implementation for biomeOS
5. **Live probe methodology** — reproducible JSON-RPC probing via `socat` against UDS

---

**License**: AGPL-3.0-or-later
