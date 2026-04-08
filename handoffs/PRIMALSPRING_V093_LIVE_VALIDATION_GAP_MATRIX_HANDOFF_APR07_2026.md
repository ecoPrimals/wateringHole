# primalSpring v0.9.3 — Live Validation GAP-MATRIX + Primal Work Items

**Date**: April 7, 2026  
**From**: primalSpring (coordination spring)  
**To**: biomeOS team, BearDog team, Songbird team, NestGate team, provenance trio teams, Squirrel team, ToadStool team, downstream springs  
**Phase**: 26 — Mixed Composition + Live Validation Matrix

---

## Context

primalSpring ran three live validation runs against Eastgate, probing each primal
through direct JSON-RPC IPC and through the biomeOS Neural API. The particle
model (Tower=electron, Node=proton, Nest=neutron) provides the compositional
framework. Three runs tracked biomeOS evolution from v2.81 → v2.92 → v2.93.

**Run 3 (biomeOS v2.93)**: 52 capabilities auto-discovered from 2 primals.
7 of 9 capability.call methods forwarded end-to-end through Neural API.
GAP-MATRIX-01, 01b, 07 all RESOLVED. New medium/low issues identified.

This handoff assigns remaining work to each primal team based on the gaps found.

---

## biomeOS Team — Remaining: GAP-MATRIX-02 (Medium, partial) + GAP-MATRIX-09 (Low)

### ~~GAP-MATRIX-01~~ RESOLVED (v2.93) + ~~GAP-MATRIX-01b~~ RESOLVED (v2.93) + ~~GAP-MATRIX-07~~ RESOLVED (v2.93)

biomeOS v2.93 (commit `13ca2328`) resolved all three critical/medium gaps:
- **Format E parser** added for BearDog's `provided_capabilities` wire format → 38 BearDog capabilities now registered
- **`unix://` URI scheme** handled in `TransportEndpoint::parse()` → proxy forwarding works end-to-end
- Combined: **52 capabilities from 2 primals**, 7/9 capability.call tests pass

### ~~GAP-MATRIX-07b~~ RESOLVED (v2.94) + ~~GAP-MATRIX-08~~ RESOLVED (v2.94) + ~~GAP-MATRIX-02b~~ RESOLVED (v2.94)

biomeOS v2.94 (commit `f67097d8`) resolved the second wave:
- **GAP-07b**: `forward_request()` preserves primal JSON-RPC error codes via `try_call()` + downcast. No more swallowed `-32601`/`-32602`.
- **GAP-08**: `NeuralRouter.self_socket_path` excludes own socket from `lazy_rescan_sockets()`, eliminating self-registration pollution.
- **GAP-02b**: `graph.list` falls back to `biomeos_graph::GraphLoader` when neural parser fails, so `DeploymentGraph`-format TOMLs appear in listings.
- 4 new tests, 7,658 total (0 failures), clippy PASS.

**Recommended Fix**: Exclude the Neural API's own socket path from
auto-discovery scans.

### GAP-MATRIX-02: Graph Parser (Medium, PARTIAL)

biomeOS v2.93 added `#[serde(default)]` to `GraphDefinition.name/version`.
The graph loader path now parses TOML successfully (confirmed via debug logs).
However, the bootstrap code path still fails on `tower_atomic_bootstrap.toml`
and `graph.list` returns empty despite parsing success.

**Remaining**: Unify bootstrap parser with graph loader, or surface parsed
graphs in the `graph.list` endpoint.

---

## Songbird Team — GAP-MATRIX-03 (Low) + Capability Method Gap

### TLS 1.3 Cipher Suite Compatibility (GAP-MATRIX-03)

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

### Capability Advertisement vs Method Implementation

**Problem**: Songbird lists domain descriptors in `capabilities.list` (e.g.,
`network.discovery`, `network.federation`, `ipc.jsonrpc`) but returns "unknown
JSON-RPC method" when these are called directly. These are capability markers,
not method endpoints.

**Evidence**:
```
capabilities.list → ["network.discovery", "ipc.jsonrpc", ...]  ✓
method: "network.discovery" → "unknown JSON-RPC method"  ✗
```

**Impact**: biomeOS forwards the exact capability name as a JSON-RPC method.
Songbird rejects it because it doesn't implement that method.

**Options**:
1. Implement advertised capability names as callable JSON-RPC methods
2. Extend `capabilities.list` response to include actual method names
3. Provide a `method_info` response format so biomeOS can map names

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

### ~~rhizoCrypt~~ RESOLVED + loamSpine, sweetGrass Not Live-Tested

**rhizoCrypt — GAP-MATRIX-05 RESOLVED (April 2026)**:

Live-validated on release binary with `--unix` flag:
1. ✅ Socket created at `$XDG_RUNTIME_DIR/biomeos/rhizocrypt.sock`
2. ✅ `health.liveness` → `{"status":"alive"}` (TCP newline + UDS)
3. ✅ `health.check` → `{"healthy":true,"state":"running",...}` (TCP newline)
4. ✅ `health.readiness` → `{"status":"ready","primal":"rhizocrypt",...}` (TCP newline)
5. ✅ `identity.get` → `{"primal":"rhizocrypt","version":"0.14.0-dev","domain":"dag",...}` (TCP newline + UDS) — **NEW**: was missing, now implemented
6. ✅ `capabilities.list` → biomeOS Format E (`provided_capabilities`) with 5 domains, 28 methods (TCP newline + UDS) — **FIXED**: was non-standard array format, now Format E wrapper

**CLI**: `rhizocrypt server --unix [--port 9400]` — tarpc 9400, JSON-RPC 9401 (dual HTTP + newline), UDS at biomeos path.

**loamSpine, sweetGrass** remain untested. Original work items apply:
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

BearDog passed all live probes through Neural API (biomeOS v2.93). No action items.

**Validated end-to-end through Neural API**:
- `health.liveness` ✓ (v0.9.0)
- `crypto.sign_ed25519` ✓ (Neural API → BearDog → signature)
- `crypto.blake3_hash` ✓ (Neural API → BearDog → hash)
- `crypto.hmac_sha256` ✓ (Neural API → BearDog → HMAC)
- `security.evaluate` ✓ (Neural API → BearDog → trust evaluation)
- `trust.evaluate` ✓ (Neural API → BearDog → trust evaluation)
- `tls.derive_secrets` ✓ (Neural API → BearDog → key derivation)
- `capabilities.list` ✓ (38 capabilities parsed via Format E)

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
3. **Validation matrix** (`specs/NUCLEUS_VALIDATION_MATRIX.md`) — systematic capability assessment (columns A-P)
4. **5-format capability parser** (`ipc/discover.rs`) — reference implementation (Formats A-E)
5. **Live probe methodology** — reproducible JSON-RPC probing via `socat` against UDS
6. **Run 4 baseline** — 162 capabilities, 12/14 capability.call PASS, biomeOS v2.94 validated
7. **Capability Wire Standard v1.0** (`infra/wateringHole/CAPABILITY_WIRE_STANDARD.md`) — formal IPC self-advertisement spec with 3 compliance levels and audit checklist

---

## Capability Wire Standard — All Primal Teams

**Spec**: `infra/wateringHole/CAPABILITY_WIRE_STANDARD.md`

All primals MUST evolve toward Level 2 compliance. This is now part of the NUCLEUS validation matrix (column P) and will be checked in every future deep-debt audit and cross-spring evolution review.

### Level 2 Target (Standard) — per-primal migration

| Primal | Current | To reach Level 2 |
|--------|---------|-------------------|
| sweetGrass | Near-L2 | Add `provided_capabilities` grouping → L3 ready |
| rhizoCrypt | Near-L2 | Add flat `methods` array at top level |
| loamSpine | Partial-L2 | Promote nested `methods` to top level, add `identity.get` |
| BearDog | Partial-L2 | Add flat `methods` array, add `identity.get` |
| Songbird | L1 only | Wrap bare array in `{primal, version, methods}` envelope, add `identity.get`, remove non-callable entries |

### Tier 1 Migration (non-breaking, immediate)

Every primal: add `"methods": [...]` flat array + `"primal"` + `"version"` to `capabilities.list` result alongside existing fields. Existing biomeOS parser handles both old and new format.

### Audit Protocol

Every primalSpring deep-debt audit MUST run the Level 2 checklist from the spec against each primal in the composition. Column P in the NUCLEUS Validation Matrix tracks per-spring Wire Standard compliance.

---

**License**: AGPL-3.0-or-later
